-- Nút "Xem như SV CTTC (CNC · Tiện phay · SHCN)" ở góc trái dưới dành cho admin.
--
-- Cách hoạt động: ghi danh CHÍNH tài khoản admin đang đăng nhập vào khóa mới nhất còn mở
-- của 3 môn cnc / tien-phay / gddd-ptnn (status active, không cần duyệt), rồi trình duyệt
-- ghi đè role=student + track=cttc để mọi trang sinh viên chạy đúng đường thật (RLS thật,
-- dữ liệu thật). Bấm "Thoát" thì gỡ 3 dòng ghi danh này đi để admin không nằm trong
-- danh sách lớp. Track thật của admin được trả lại như cũ ngay trong hàm (trigger
-- trg_set_track_cttc sẽ đổi nó thành 'cttc' khi insert).
--
-- Chạy: supabase db query --linked -f docs/supabase-migration-preview-cttc-student.sql

create or replace function public.preview_cttc_enroll()
returns jsonb
language plpgsql security definer set search_path = public
as $$
declare
  v_uid uuid := auth.uid();
  v_prev_track text;
  v_codes text[] := array['cnc', 'tien-phay', 'gddd-ptnn'];
  v_code text;
  v_i integer := 0;
  v_course_id bigint;
  v_course_name text;
  v_result jsonb := '[]'::jsonb;
begin
  if v_uid is null or not public.is_admin() then
    raise exception 'Chỉ tài khoản admin mới dùng được chế độ xem thử này.';
  end if;

  select track into v_prev_track from public.profiles where id = v_uid;

  foreach v_code in array v_codes loop
    v_i := v_i + 1;
    v_course_id := null;
    v_course_name := null;

    select o.id, o.name into v_course_id, v_course_name
    from public.course_offerings o
    join public.subjects s on s.id = o.subject_id
    where s.code = v_code and o.status = 'active'
    order by o.school_year desc, o.created_at desc
    limit 1;

    if v_course_id is not null then
      -- enrolled_at tăng dần theo thứ tự cnc → tiện phay → SHCN để /tai-khoan (lấy ghi danh
      -- mới nhất) mở ra lớp chủ nhiệm; CNC và Tiện phay có trang riêng /lop-hoc/cnc, /lop-hoc/tien-phay.
      insert into public.course_enrollments (course_id, student_id, enrolled_at, status, approved_at, approved_by)
      values (v_course_id, v_uid, now() - make_interval(secs => array_length(v_codes, 1) - v_i), 'active', now(), v_uid)
      on conflict (course_id, student_id) do update
        set status = 'active',
            enrolled_at = excluded.enrolled_at,
            approved_at = coalesce(public.course_enrollments.approved_at, now());
    end if;

    v_result := v_result || jsonb_build_object('subject', v_code, 'course_id', v_course_id, 'course_name', v_course_name);
  end loop;

  -- Trả lại track thật của admin (trigger vừa đổi thành 'cttc'); track giả lập chỉ ghi đè trên trình duyệt.
  update public.profiles set track = v_prev_track where id = v_uid and track is distinct from v_prev_track;

  return v_result;
end;
$$;

create or replace function public.preview_cttc_unenroll()
returns integer
language plpgsql security definer set search_path = public
as $$
declare
  v_uid uuid := auth.uid();
  v_n integer;
begin
  if v_uid is null or not public.is_admin() then
    raise exception 'Chỉ tài khoản admin mới dùng được chế độ xem thử này.';
  end if;

  delete from public.course_enrollments e
  using public.course_offerings o, public.subjects s
  where e.course_id = o.id and o.subject_id = s.id
    and e.student_id = v_uid
    and s.code in ('cnc', 'tien-phay', 'gddd-ptnn');
  get diagnostics v_n = row_count;
  return v_n;
end;
$$;

grant execute on function public.preview_cttc_enroll() to authenticated;
grant execute on function public.preview_cttc_unenroll() to authenticated;
