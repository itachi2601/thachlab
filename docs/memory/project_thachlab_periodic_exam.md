---
name: project_thachlab_periodic_exam
description: Kiểm tra định kỳ trên LMS — lesson_kind, tách KT giữa/cuối kì khỏi chương; thực tế DB chỉ có 1 mục giữa kì + 15 kiểm tra chương
metadata:
  type: project
---

`lessons.lesson_kind` phân loại bài: `bai_hoc`, `kiem_tra_chuong`, `kiem_tra_giua_ki`, `kiem_tra_cuoi_ki` (migration đã chạy: `docs/supabase-migration-lessons-periodic-exam.sql` + `-chapter-exam.sql`).

**2026-09-19 — tách KT giữa/cuối học kì ra khỏi chương.** Trên `/lop-hoc` (`app/lop-hoc/page.tsx`), bài loại `kiem_tra_giua_ki`/`kiem_tra_cuoi_ki` không còn nằm trong accordion của chương: hiện thành thẻ riêng cùng cấp chương, ngay sau chương được gắn, và **không tính vào % tiến độ chương**. Helper `isSemesterExam()` ở `features/lessons/types.ts`. `kiem_tra_chuong` vẫn nằm trong chương như cũ. Chương gắn bài chỉ quyết định vị trí đứng sau — đó là cách teacher đặt thứ tự. Commit 52363b1d + 6d84f7be, **đã deploy**.

**Dữ liệu đã tạo (2026-09-19).** `scripts/create-periodic-exams.mjs --apply` đã chạy xong: thêm 11 bài, đổi tên bài cũ (id 96) thành "Kiểm tra giữa học kì 1". Phân phối trong bảng `PLAN` đầu script — lớp 11 & 12 (4 chương): sau chương 1/2/3/4 = giữa HK1 / cuối HK1 / giữa HK2 / cuối HK2; lớp 10 (7 chương): sau chương 2/4/5/7. **KHTN 9 chưa làm** vì chưa rõ cách chia học kì.

**Trạng thái DB thực tế (kiểm lại 2026-09-19 bằng anon key, `lessons?lesson_kind=neq.bai_hoc`):** chỉ có **1** bài `kiem_tra_giua_ki` (id 96 — "Kiểm tra giữa học kì 1", chương 2 = Chương 1 Vật lí nhiệt lớp 12) và **15** bài `kiem_tra_chuong`, tất cả `published = true`. **Không có bài `kiem_tra_cuoi_ki` nào**, và lớp 10/11 chưa có mục giữa/cuối kì. Nghĩa là `create-periodic-exams.mjs --apply` chưa chạy trọn (hoặc đã bị lùi) — muốn có "Kiểm tra cuối học kì 1" thì phải chạy lại script đó với service role key. Đừng tin con số "11 mục" ghi trước đây.

Liên quan: [[project_thachlab_lesson_sections]], [[project_thachlab_up_de_skill]]
