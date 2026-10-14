-- ============================================================================
-- Bản đồ xuất phát cho em mới vào (thầy chốt 14/10/2026)
-- Kiểm tra đầu vào có thêm "độ chắc" mỗi câu (chac / hoi / doan) → mỗi bài rơi vào 1 trong 4 nhóm:
--   vung (đúng và chắc) · chua_vung (đúng nhưng đoán/hơi chắc, hoặc sai 1 câu) ·
--   hieu_sai (sai mà chắc ≥1 câu — ảo tưởng hiểu) · chua_biet (sai ≥2 câu, đều không chắc).
-- hieu_sai và chua_biet mở tutoring_needs (note 'chẩn đoán đầu vào · hiểu sai' / '· chưa biết'); chua_vung chỉ ghi nhận.
-- Nhóm chi tiết CHỈ thầy/trợ giảng/chính em thấy: phụ huynh nhận perTopic cắt còn topicId/correct/total (thầy chốt 14/10).
-- Thêm: diagnostic_submit (thay thế, vẫn nhận kết quả cũ không có độ chắc), diagnostic_get (cắt cho phụ huynh),
--       diagnostic_maps(uuid[]) cho trợ giảng xem hàng loạt. Không đổi bảng, không đụng dữ liệu cũ.
-- Cách chạy: bash scripts/run-migrations.sh --yes --only N — ngoài giờ HS làm bài không bắt buộc (chỉ thay hàm).
-- Rollback: perf/rollback/20261014140000_chan_doan_ban_do_xuat_phat.down.sql
-- ============================================================================

-- Xem kết quả: phụ huynh (chỉ là phụ huynh) nhận bản cắt, những người còn lại nhận đủ nhóm + độ chắc.
create or replace function public.diagnostic_get(p_student uuid)
returns jsonb
language plpgsql stable security definer set search_path = public
as $$
declare
  r public.entry_diagnostics%rowtype;
  v_full boolean;
  v_topics jsonb;
begin
  if not public.diagnostic_can_read(p_student) then
    raise exception 'Không có quyền xem kết quả này' using errcode = '42501';
  end if;
  select * into r from public.entry_diagnostics where student_id = p_student;
  if not found then return jsonb_build_object('done', false); end if;

  v_full := auth.uid() = p_student or public.teaches_student(p_student) or public.is_admin();
  if v_full then
    v_topics := r.per_topic;
  else
    select coalesce(jsonb_agg(jsonb_build_object('topicId', e->'topicId', 'correct', e->'correct', 'total', e->'total')), '[]'::jsonb)
      into v_topics
    from jsonb_array_elements(r.per_topic) e;
  end if;
  return jsonb_build_object('done', true, 'createdAt', r.created_at, 'needCount', r.need_count, 'perTopic', v_topics);
end;
$$;
revoke all on function public.diagnostic_get(uuid) from public, anon;
grant execute on function public.diagnostic_get(uuid) to authenticated;

-- Trợ giảng/thầy xem bản đồ của cả lớp một lần (không gọi từng em).
create or replace function public.diagnostic_maps(p_students uuid[])
returns table (student_id uuid, created_at timestamptz, per_topic jsonb)
language sql stable security definer set search_path = public
as $$
  select d.student_id, d.created_at, d.per_topic
  from public.entry_diagnostics d
  where d.student_id = any (p_students)
    and auth.uid() is not null
    and (public.teaches_student(d.student_id) or public.is_admin());
$$;
revoke all on function public.diagnostic_maps(uuid[]) from public, anon;
grant execute on function public.diagnostic_maps(uuid[]) to authenticated;

-- Em nộp bài. p_results = [{topicId, correct, total, seq?, probe?, answers?: [{ok, conf}]}].
-- Nhóm tính ở đây (không tin client): wrong = total - correct;
-- sure_wrong = số câu sai mà conf='chac'; shaky_right = số câu đúng mà conf in ('hoi','doan').
create or replace function public.diagnostic_submit(p_student uuid, p_results jsonb)
returns jsonb
language plpgsql security definer set search_path = public
as $$
declare
  v_class bigint;
  v_name text;
  v_clean jsonb := '[]'::jsonb;
  v_needs int := 0;
  v_topics text;
  rec record;
  v_wrong int;
  v_sure int;
  v_shaky int;
  v_level text;
  v_note text;
begin
  if auth.uid() is null or auth.uid() <> p_student then
    raise exception 'Chỉ chính em mới nộp được bài này' using errcode = '42501';
  end if;
  if jsonb_typeof(p_results) <> 'array' or jsonb_array_length(p_results) = 0 or jsonb_array_length(p_results) > 12 then
    raise exception 'Kết quả không hợp lệ';
  end if;
  if exists (select 1 from public.entry_diagnostics where student_id = p_student) then
    raise exception 'Em đã làm bài kiểm tra đầu vào rồi';
  end if;

  select uc.class_id into v_class
  from public.user_classes uc
  where uc.user_id = p_student and uc.status = 'active'
  order by uc.class_id desc limit 1;

  -- Chỉ nhận bài tầng bài học (mỗi bài một lần), số câu 1..5, đúng không vượt tổng.
  for rec in
    select distinct on (x."topicId") x."topicId" as topic_id, x.correct, x.total, x.seq, x.probe, x.answers
    from jsonb_to_recordset(p_results) as x("topicId" bigint, correct int, total int, seq int, probe boolean, answers jsonb)
    join public.question_topics t on t.id = x."topicId" and t.parent_id is null
    where x.total between 1 and 5 and x.correct between 0 and x.total
    order by x."topicId"
  loop
    v_wrong := rec.total - rec.correct;
    v_sure := 0;
    v_shaky := 0;
    if rec.answers is not null and jsonb_typeof(rec.answers) = 'array' then
      select count(*) filter (where not coalesce((a->>'ok')::boolean, false) and a->>'conf' = 'chac'),
             count(*) filter (where coalesce((a->>'ok')::boolean, false) and a->>'conf' in ('hoi', 'doan'))
        into v_sure, v_shaky
      from jsonb_array_elements(rec.answers) a;
      -- Không để số câu trong answers vượt số câu đã nộp.
      v_sure := least(v_sure, v_wrong);
      v_shaky := least(v_shaky, rec.correct);
    end if;

    if rec.total >= 2 and v_wrong >= 2 and v_wrong * 100.0 / rec.total >= 60 then
      v_level := case when v_sure >= 1 then 'hieu_sai' else 'chua_biet' end;
    elsif v_sure >= 1 then
      v_level := 'hieu_sai';
    elsif v_wrong >= 1 or v_shaky * 2 >= rec.total then
      v_level := 'chua_vung';
    else
      v_level := 'vung';
    end if;

    v_clean := v_clean || jsonb_build_array(jsonb_build_object(
      'topicId', rec.topic_id, 'correct', rec.correct, 'total', rec.total,
      'level', v_level, 'sureWrong', v_sure, 'shakyRight', v_shaky,
      'seq', rec.seq, 'probe', coalesce(rec.probe, false)));

    if v_level in ('hieu_sai', 'chua_biet') then
      v_note := 'chẩn đoán đầu vào · ' || case v_level when 'hieu_sai' then 'hiểu sai' else 'chưa biết' end;
      insert into public.tutoring_needs
        (student_id, class_id, topic_id, form, wrong, total, pct, source, status, note)
      values (p_student, v_class, rec.topic_id, '', v_wrong, rec.total,
              round(v_wrong * 100.0 / rec.total)::int, 'auto', 'open', v_note)
      on conflict (student_id, topic_id, form) do update set
        wrong = excluded.wrong, total = excluded.total, pct = excluded.pct,
        class_id = coalesce(excluded.class_id, tutoring_needs.class_id),
        last_seen_at = now(),
        status = case when tutoring_needs.status in ('cleared', 'dismissed') then 'open' else tutoring_needs.status end,
        cleared_at = case when tutoring_needs.status in ('cleared', 'dismissed') then null else tutoring_needs.cleared_at end,
        note = case when tutoring_needs.status in ('cleared', 'dismissed') or tutoring_needs.note = ''
                    then v_note else tutoring_needs.note end;
      v_needs := v_needs + 1;
    end if;
  end loop;

  if jsonb_array_length(v_clean) = 0 then
    raise exception 'Kết quả không hợp lệ';
  end if;

  insert into public.entry_diagnostics (student_id, per_topic, need_count)
  values (p_student, v_clean, v_needs);

  select coalesce(nullif(full_name, ''), 'Học sinh') into v_name from public.profiles where id = p_student;
  select string_agg(t.name, ', ' order by t.sort_order)
    into v_topics
  from public.question_topics t
  where t.id in (select (e->>'topicId')::bigint from jsonb_array_elements(v_clean) e
                 where e->>'level' in ('hieu_sai', 'chua_biet'));

  -- Phụ huynh chỉ nhận lời báo chung (không nói "hiểu sai"/"chưa biết").
  perform public.notify_student_side(
    p_student, 'diagnostic_done',
    'Kết quả kiểm tra đầu vào',
    case when v_needs = 0 then v_name || ' đã làm kiểm tra đầu vào — nền tảng ổn, chưa có phần nào cần phụ đạo gấp.'
         else v_name || ' đã làm kiểm tra đầu vào — cần củng cố: ' || coalesce(v_topics, '') || '. Có thể đăng ký buổi phụ đạo ngay.' end,
    '/', '/phu-huynh');
  if v_class is not null then
    perform public.notify_class_staff(
      v_class, 'diagnostic_done', 'Kiểm tra đầu vào: ' || v_name,
      case when v_needs = 0 then 'Chưa có phần nào hổng.' else 'Mở ' || v_needs || ' mục phụ đạo: ' || coalesce(v_topics, '') end,
      '/dashboard-thpt');
  end if;

  return jsonb_build_object('needCount', v_needs, 'perTopic', v_clean);
end;
$$;
revoke all on function public.diagnostic_submit(uuid, jsonb) from public, anon;
grant execute on function public.diagnostic_submit(uuid, jsonb) to authenticated;
