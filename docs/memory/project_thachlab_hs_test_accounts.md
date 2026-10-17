---
name: project_thachlab_hs_test_accounts
description: "2 tài khoản HS Test (lớp 12) + script gieo/dọn dữ liệu thử; test luồng danh hiệu/khung/bảng tuần/phụ đạo/thoát phụ đạo 15/10/2026, đã sửa 5 lỗi (5a977bddd), CHƯA deploy"
metadata:
  type: project
---

**Mục tiêu:** thử luồng HS thật (danh hiệu, đeo, khung, bảng tuần, phụ đạo, thoát phụ đạo) mà không dùng em thật.

**Tài khoản (production, 2026-10-15):** `hs.test1@thachlab.local`, `hs.test2@thachlab.local`, tên "HS Test 1/2", role student, track THPT, ghi danh lớp 12 (class_id 18, `user_classes.status='active'` — `approved` KHÔNG vào được lớp). Mật khẩu tạm in ra lúc tạo, không lưu file; quên thì tạo lại bằng `--xoa` rồi chạy lại.
- `node --env-file=.env.local scripts/tao-hs-test.mjs` (tạo/cập nhật; `--xoa` xoá tài khoản).
- `node --env-file=.env.local scripts/gieo-hs-test.mjs` gieo 1 danh hiệu (mùa 4) + 1 mục phụ đạo `note='TEST-SEED'` cho HS Test 1; `--xoa` dọn mọi dòng (reviews, exit attempts, registrations, needs, awards, danh hiệu đang đeo). Đã chạy `--xoa` xong 2026-10-15, không còn dữ liệu gieo.
- Script dùng service role: phải nằm trong repo và chạy trong tab terminal (Bash bị sandbox chặn supabase.co).

**Đã thử OK (dev local, 1024px):** bảng tuần lớp, nhận + đeo danh hiệu, khung rank, đăng ký/huỷ buổi phụ đạo, xem lại lý thuyết (cổng 45–480 giây server chặn đúng), bài thoát 20 câu đường chưa đạt (10%, chờ 24 giờ).

**Đã sửa (commit 5a977bddd, CHƯA deploy):** nhóm radio `-conf` bị đếm là câu tự kiểm tra; danh hiệu đã nhận bị ẩn khi ngoài chương trình lớp; mô tả thành tích lặp; buổi phụ đạo đã đăng ký không hiện chủ đề (`fetchMyRegistrationTopics`); lời chào em mới "quay lại".

**Còn chờ:** deploy 5a977bddd; thử đường đạt ≥80% (xoá lượt thử hoặc chờ 24 giờ, cần giải đúng 20 câu hỗn hợp trắc nghiệm + đáp số); chụp 375px; cổng xem lại lý thuyết tối đa 480 giây là thiết kế (40% thời gian đọc ước tính, `tutoring_review_start`) — thầy muốn giảm thì sửa hằng số bằng migration.

Liên quan: [[project_thachlab_phu_dao]], [[project_thachlab_rank_system]], [[project_thachlab_title_showcase]]
