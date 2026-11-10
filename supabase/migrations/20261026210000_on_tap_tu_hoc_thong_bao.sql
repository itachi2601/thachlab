-- Ôn tập theo chặng — Tự học ở nhà: thông báo trong chuông trỏ thẳng /lop-hoc/on-tap/ (trước đây không có,
-- học sinh bấm thông báo BTVN thì rơi vào /tai-khoan). Chỉ thay review_create_self, thêm vòng thông báo.
create or replace function public.review_create_self(
  p_class bigint, p_title text, p_threshold int, p_stages jsonb, p_due_at timestamptz, p_sequential boolean
)
returns bigint
language plpgsql security definer set search_path = public
as $$
declare
  v_id bigint;
  s jsonb;
  r record;
begin
  if not public.is_staff() then raise exception 'forbidden'; end if;
  if jsonb_typeof(p_stages) <> 'array' or jsonb_array_length(p_stages) not between 1 and 12 then
    raise exception 'stages_invalid';
  end if;
  if p_due_at is null or p_due_at <= now() then raise exception 'due_invalid'; end if;
  for s in select * from jsonb_array_elements(p_stages) loop
    if not exists (select 1 from public.exams e where e.id = (s ->> 'exam_id')::bigint) then
      raise exception 'exam_not_found:%', s ->> 'exam_id';
    end if;
  end loop;
  insert into public.review_sessions (class_id, title, threshold, stages, mode, due_at, sequential,
                                      current_stage, stage_started_at, status)
  values (p_class, btrim(p_title), coalesce(p_threshold, 80), p_stages, 'self', p_due_at, coalesce(p_sequential, false),
          jsonb_array_length(p_stages) - 1, now(), 'running')
  returning id into v_id;

  for r in
    select uc.user_id from public.user_classes uc
    join public.profiles p on p.id = uc.user_id
    where uc.class_id = p_class and uc.status = 'active' and p.role = 'student'
  loop
    perform public.notify_user(
      r.user_id, 'review_self_new', 'Ôn tập ở nhà: ' || btrim(p_title),
      'Hạn ' || to_char(p_due_at at time zone 'Asia/Ho_Chi_Minh', 'HH24:MI DD/MM') || ' · bấm để vào làm.',
      '/lop-hoc/on-tap/');
  end loop;
  return v_id;
end;
$$;

-- ROLLBACK: chạy lại phần create or replace review_create_self trong 20261025100000_on_tap_tu_hoc_ve_nha.sql
