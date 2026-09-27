-- ============================================================================
-- Vá lỗ hổng phân quyền ở /kiem-tra/lam: học sinh đã đăng nhập làm được và
-- NỘP được BẤT KỲ đề "published" nào nếu biết/đoán được exam id (kể cả đề
-- không gán cho lớp của mình), vì:
--
--   1) app/kiem-tra/lam/page.tsx bọc <RequireAuth> không truyền area/adminOnly
--      -> components/auth/RequireAuth.tsx chỉ kiểm tra "đã đăng nhập", không
--      kiểm tra lớp.
--   2) RLS "students read published exams" trên public.exams chỉ yêu cầu
--      published = true, không đối chiếu exam_classes ↔ user_classes.
--   3) RLS insert trên public.exam_results / public.exam_question_results chỉ
--      yêu cầu student_id = auth.uid(), không kiểm tra lớp -> bài nộp sai lớp
--      vẫn được ghi, ảnh hưởng rank/leaderboard/thống kê phụ đạo.
--
-- Mô hình gán lớp cho đề ĐÃ CÓ SẴN và đang chạy thật: bảng exam_classes (M2M
-- exam_id ↔ class_id), được ghi bởi mọi luồng đăng đề hiện hành
-- (AzotaExamComposer, LessonImporter, ExamLibraryAdmin, homework.ts qua
-- services/classes.ts#setItemClasses). "Không có dòng nào trong exam_classes"
-- = đề toàn trường — CHỦ Ý, đúng logic đã dùng để lọc danh sách đề hiển thị
-- (services/content.ts#visibleTo). Vá này dùng lại đúng logic đó, không tự
-- nghĩ thêm quy tắc mới.
--
-- KHÔNG dùng đường lesson_items -> lessons -> chapters -> chapter_classes:
-- đó là M2M khác (gate hiển thị mục trong bài học theo lớp), không phải
-- quyền làm đề. Một exam_id có thể được nhiều lesson_items ở nhiều
-- lớp/bài/chương khác nhau cùng tham chiếu (đề ngân hàng câu hỏi dùng chung,
-- đề thi thử trường/sở mục 277) — dùng exam_classes là đúng nguồn thật.
--
-- Chỉ SIẾT THÊM đúng 1 điều kiện lớp, và chỉ áp dụng cho tài khoản không phải
-- staff (admin/instructor/tro_giang):
--   - Dùng policy "as restrictive" (AND với các policy permissive hiện có)
--     nên KHÔNG đụng, KHÔNG thay hành vi is_admin()/published/cnc_key hiện
--     tại — chỉ AND thêm điều kiện lớp cho học sinh.
--   - Ngân hàng CNC (exams.cnc_key is not null) vẫn được đọc như cũ (không
--     qua exam_classes) — tránh vỡ tính năng /quan-tri/cnc-* không liên quan
--     đến lỗ hổng đang vá.
--   - Staff (admin/instructor/tro_giang) không bị chặn — khớp hành vi hiện
--     tại của /quan-tri/dang-de, /quan-tri/sua-de (đọc mọi đề published bất
--     kể lớp) và việc Thạch tự làm thử đề bằng tài khoản admin (xem
--     20260926110000_rank_exclude_staff.sql).
--
-- Idempotent (drop policy/function trước khi tạo lại).
-- Chạy: bash scripts/run-migrations.sh (hoặc supabase db query --linked -f <file>)
-- KHÔNG dùng `supabase db push`. Rollback: perf/rollback/20260927150000_exam_class_access.down.sql
-- ============================================================================

begin;

create or replace function public.is_staff()
returns boolean
language sql security definer stable set search_path = public
as $$
  select exists (
    select 1 from public.profiles
    where id = (select auth.uid()) and role in ('admin', 'instructor', 'tro_giang')
  );
$$;

-- true nếu đề này "toàn trường" (không gán lớp nào) hoặc học sinh có 1 dòng
-- active trong user_classes khớp với 1 trong các lớp đề đã gán.
create or replace function public.exam_open_to_student(p_exam_id bigint, p_user_id uuid)
returns boolean
language sql security definer stable set search_path = public
as $$
  select
    not exists (select 1 from public.exam_classes ec where ec.exam_id = p_exam_id)
    or exists (
      select 1
      from public.exam_classes ec
      join public.user_classes uc on uc.class_id = ec.class_id
      where ec.exam_id = p_exam_id
        and uc.user_id = p_user_id
        and uc.status = 'active'
    );
$$;

drop policy if exists "students only see own-class exams" on public.exams;
create policy "students only see own-class exams" on public.exams
  as restrictive
  for select
  to authenticated
  using (
    public.is_staff()
    or exams.cnc_key is not null
    or public.exam_open_to_student(exams.id, (select auth.uid()))
  );

drop policy if exists "students insert results only for own-class exams" on public.exam_results;
create policy "students insert results only for own-class exams" on public.exam_results
  as restrictive
  for insert
  to authenticated
  with check (
    public.is_staff()
    or exists (
      select 1 from public.exams e where e.id = exam_results.exam_id and e.cnc_key is not null
    )
    or public.exam_open_to_student(exam_results.exam_id, (select auth.uid()))
  );

drop policy if exists "students insert question results only for own-class exams" on public.exam_question_results;
create policy "students insert question results only for own-class exams" on public.exam_question_results
  as restrictive
  for insert
  to authenticated
  with check (
    public.is_staff()
    or exists (
      select 1 from public.exams e where e.id = exam_question_results.exam_id and e.cnc_key is not null
    )
    or public.exam_open_to_student(exam_question_results.exam_id, (select auth.uid()))
  );

commit;
