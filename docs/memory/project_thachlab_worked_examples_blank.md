---
name: project_thachlab_worked_examples_blank
description: "Sự cố 4/10/2026 — tab \"Bài mẫu\" bài 57 (Chuyển động ném, lớp 10) trống trên máy thầy dù DB còn đủ 19 dạng bài; nguyên nhân cơ chế file tĩnh không chứa lời giải + lượt đối chiếu Supabase hỏng thì trang im lặng; đã vá + deploy, nguyên nhân gốc trên máy thầy CHƯA xác nhận"
metadata:
  node_type: memory
  type: project
  originSessionId: a348d763-65c1-43e0-a9ee-8058c42454d6
  modified: 2026-10-04T03:20:02.706Z
---

**Hiện tượng (4/10/2026):** thầy đăng nhập, xem trang chính thức bài 57 → tab Bài mẫu chỉ có phụ đề
"19 dạng bài kèm lời giải", lưới trống. DB `lesson_items` id 106 vẫn đủ 19 câu; mở ẩn danh thấy đủ.
Cập nhật lý thuyết tối 3/10 (`cap-nhat-ly-thuyet.sh`) KHÔNG đụng mục này (có backup `scripts/logs/ly-thuyet-bai57-*`).

**Cơ chế gây trống:** `/data/lessons/<id>.json` cố ý không chứa `questions` (chỉ `questions_count`);
`services/static-content.ts` → `revalidateLesson` gọi Supabase (lessons + lesson_items lồng) để lấy lời giải.
Lượt đó lỗi (undefined) → giữ bản tĩnh, không báo gì, và promise lỗi bị nhớ trong `revalidatedLessons`
cho tới khi reload cứng.

**Đã vá (commit 5967310a8, deploy e4b20a7 ~10:40 4/10):** giữ `questions_count` trên LessonItem; lỗi → thử
select phẳng `lesson_items(id,questions)`; vẫn lỗi → bỏ cache + trang hiện "Chưa tải được N dạng bài" + nút
Tải lại (`retryLessonRevalidate`). Đã thử 3 đường trên dev.

**Còn treo:** chưa biết VÌ SAO lượt Supabase hỏng trên máy thầy khi đăng nhập (nghi phiên/JWT hết hạn sau khi
thử tính năng đặt lại mật khẩu, hoặc cache promise lỗi). Sau deploy, nếu thầy vẫn thấy dòng "Chưa tải được…"
thì nguyên nhân là Supabase từ chối request của phiên đăng nhập → kiểm token/đăng xuất-đăng nhập lại.

**How to apply:** HS/thầy báo "mất bài tập mẫu" → kiểm DB trước (REST `lesson_items?lesson_id=eq.<id>&kind=eq.bai_tap_mau`),
rồi mở ẩn danh; đừng vội khôi phục dữ liệu. Liên quan [[project_thachlab_perf_optimization]] (lớp đọc tĩnh),
[[project_thachlab_cap_nhat_ly_thuyet]].
