-- Rollback 20261014140000: trả diagnostic_get / diagnostic_submit về bản 20261012120000, bỏ diagnostic_maps.
-- Dữ liệu entry_diagnostics đã nộp theo bản mới vẫn đọc được (phần tử có thêm khoá level/sureWrong, bản cũ bỏ qua).
drop function if exists public.diagnostic_maps(uuid[]);

create or replace function public.diagnostic_get(p_student uuid)
returns jsonb
language plpgsql stable security definer set search_path = public
as $$
declare r public.entry_diagnostics%rowtype;
begin
  if not public.diagnostic_can_read(p_student) then
    raise exception 'Không có quyền xem kết quả này' using errcode = '42501';
  end if;
  select * into r from public.entry_diagnostics where student_id = p_student;
  if not found then return jsonb_build_object('done', false); end if;
  return jsonb_build_object('done', true, 'createdAt', r.created_at, 'needCount', r.need_count, 'perTopic', r.per_topic);
end;
$$;
revoke all on function public.diagnostic_get(uuid) from public, anon;
grant execute on function public.diagnostic_get(uuid) to authenticated;

-- Em nộp bài (chỉ chính em, một lần). p_results = [{topicId, correct, total}], topicId phải là chủ đề tầng bài.
create or replace function public.diagnostic_submit(p_student uuid, p_results jsonb)
returns jsonb
language plpgsql security definer set search_path = public
as $$
declare
  v_class bigint;
  v_name text;
  v_clean jsonb;
  v_needs int := 0;
  v_topics text;
  rec record;
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

  -- Chỉ nhận bài tầng bài học, số câu hợp lý (1..5), đúng không vượt tổng.
  select coalesce(jsonb_agg(jsonb_build_object('topicId', t.id, 'correct', x.correct, 'total', x.total)), '[]'::jsonb)
    into v_clean
  from jsonb_to_recordset(p_results) as x("topicId" bigint, correct int, total int)
  join public.question_topics t on t.id = x."topicId" and t.parent_id is null
  where x.total between 1 and 5 and x.correct between 0 and x.total;
  if jsonb_array_length(v_clean) = 0 then
    raise exception 'Kết quả không hợp lệ';
  end if;

  select uc.class_id into v_class
  from public.user_classes uc
  where uc.user_id = p_student and uc.status = 'active'
  order by uc.class_id desc limit 1;

  for rec in
    select (e->>'topicId')::bigint as topic_id, (e->>'correct')::int as correct, (e->>'total')::int as total
    from jsonb_array_elements(v_clean) e
  loop
    if rec.total >= 2 and (rec.total - rec.correct) >= 2
       and (rec.total - rec.correct) * 100.0 / rec.total >= 60 then
      insert into public.tutoring_needs
        (student_id, class_id, topic_id, form, wrong, total, pct, source, status, note)
      values (p_student, v_class, rec.topic_id, '', rec.total - rec.correct, rec.total,
              round((rec.total - rec.correct) * 100.0 / rec.total)::int, 'auto', 'open', 'chẩn đoán đầu vào')
      on conflict (student_id, topic_id, form) do update set
        wrong = excluded.wrong, total = excluded.total, pct = excluded.pct,
        class_id = coalesce(excluded.class_id, tutoring_needs.class_id),
        last_seen_at = now(),
        status = case when tutoring_needs.status in ('cleared', 'dismissed') then 'open' else tutoring_needs.status end,
        cleared_at = case when tutoring_needs.status in ('cleared', 'dismissed') then null else tutoring_needs.cleared_at end,
        note = case when tutoring_needs.status in ('cleared', 'dismissed') or tutoring_needs.note = ''
                    then 'chẩn đoán đầu vào' else tutoring_needs.note end;
      v_needs := v_needs + 1;
    end if;
  end loop;

  insert into public.entry_diagnostics (student_id, per_topic, need_count)
  values (p_student, v_clean, v_needs);

  select coalesce(nullif(full_name, ''), 'Học sinh') into v_name from public.profiles where id = p_student;
  select string_agg(t.name, ', ' order by t.sort_order)
    into v_topics
  from public.question_topics t
  where t.id in (select (e->>'topicId')::bigint from jsonb_array_elements(v_clean) e
                 where (e->>'total')::int - (e->>'correct')::int >= 2
                   and ((e->>'total')::int - (e->>'correct')::int) * 100.0 / (e->>'total')::int >= 60);

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

  return jsonb_build_object('needCount', v_needs);
end;
$$;
revoke all on function public.diagnostic_submit(uuid, jsonb) from public, anon;
grant execute on function public.diagnostic_submit(uuid, jsonb) to authenticated;
