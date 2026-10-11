---
name: bao-cao-hoc-tap-tuan
description: Báo cáo tình hình học tập hằng tuần theo lớp (hoạt động, điểm, chủ đề hay sai, phụ đạo), phân nhóm học sinh không làm bài để thúc đẩy (nhắc trong web, danh sách cho trợ giảng gọi, phụ huynh khi thầy đồng ý), và dọn tài khoản không hoạt động quá 30 ngày theo 3 bước (cảnh báo → vô hiệu hoá → xoá định danh). Dùng khi thầy nói "báo cáo học tập tuần này", "em nào bỏ học", "nhắc học sinh không làm bài", "dọn tài khoản không hoạt động", "/bao-cao-hoc-tap-tuan".
---

# Báo cáo học tập tuần + kéo học sinh quay lại + dọn tài khoản bỏ

**Trạng thái: THIẾT KẾ (11/10/2026), chưa có script.** Thầy chốt: 3 bước dọn tài khoản; "hoạt động" = làm bài hoặc mở bài học (đăng nhập suông không tính); báo cáo bản tuần cho thầy chạy theo lệnh, kèm danh sách cho trợ giảng, nhắc học sinh trong web, và phụ huynh (chỉ khi thầy đồng ý từng đợt).

## Nguồn hoạt động (một em "hoạt động" nếu có ít nhất một trong)
`exam_results.created_at`, `lesson_progress.done_at`, `student_learning_presence.last_seen_at`. Ngày hoạt động cuối = lớn nhất của ba nguồn. Chưa có nguồn nào → "chưa từng làm bài", tính mốc từ `profiles.created_at`.

## Nội dung báo cáo (mỗi lớp một mục)
1. **Tóm tắt**: số em hoạt động 7 ngày / sĩ số, số bài nộp, điểm TB, so với tuần trước.
2. **Phân nhóm**: 🟢 đều (≤7 ngày) · 🟡 chững (8–14) · 🟠 nguy cơ bỏ (15–23) · 🔴 sắp bị dọn (24–29). Mỗi em: tên, lớp, ngày hoạt động cuối, bài dở dang, số lần đã nhắc.
3. **Không làm bài**: tách "chưa từng làm" và "học rồi dừng"; gợi ý hành động (nhắc web / trợ giảng gọi / phụ huynh).
4. **Bức tranh học tập**: phân bố điểm, top 5 chủ đề/YCCĐ hay sai (`tutoring_needs`), em chờ phụ đạo / đã thoát phụ đạo, rank và chuỗi ngày.
5. **Nổi bật** để khen: tăng điểm nhiều nhất, quay lại sau nghỉ, chuỗi dài nhất.
6. **Trợ giảng**: lượt tiếp xúc và phụ đạo trong tuần (lấy từ `kiem-tra-tro-giang-tuan`, không làm lại).
7. **Chân báo cáo**: tài khoản sắp bị vô hiệu hoá trong 7 ngày; số tài khoản đã vô hiệu hoá / xoá định danh trong tuần (chỉ đếm, không in lại dữ liệu cá nhân).

## Thúc đẩy (nhắc)
- Học sinh: thông báo trong web (`notifications`), giọng thân thiện, **tối đa 1 tin / 3 ngày / em**, mức nhắc tăng dần theo lịch sử, không dọa. Theo `docs/QUY-TAC-THIET-KE.md` (không gây xấu hổ, không so sánh tên em khác).
- Trợ giảng: danh sách em cần gọi, chỉ lớp mình phụ trách.
- Phụ huynh: chỉ khi thầy bảo, theo `docs/QUY-TAC-THIET-KE-PHU-HUYNH.md`.

## Dọn tài khoản không hoạt động > 30 ngày — 3 bước, KHÔNG xoá cứng
1. **Ngày 23**: cảnh báo trong web + liệt kê ở báo cáo ("còn 7 ngày").
2. **Ngày 30**: vô hiệu hoá (`profiles.disabled_at`, chặn đăng nhập), dữ liệu còn nguyên, mở lại được.
3. **Ngày 30 + 60**: xoá định danh (tên, mã HS, SĐT/email, liên kết phụ huynh), giữ số liệu ẩn danh cho thống kê. Sao lưu trước.
- **Loại trừ**: role ≠ học sinh (admin, trợ giảng, phụ huynh), tài khoản tạo <30 ngày, em trong bảng đóng băng `hoc_sinh_dong_bang`, em thuộc lớp có kỳ kiểm tra sắp tới, và **cả lớp nếu đang nghỉ hè/Tết** (thầy báo).
- Mặc định **dry-run**; bước 2 và 3 chỉ chạy khi thầy đồng ý (`--yes`), ghi log `scripts/logs/`.

## Việc còn lại để skill chạy được
- [ ] Migration (agent không tự chạy production): `profiles.disabled_at`, `hoc_sinh_dong_bang`, `hoc_tap_reminders` (lịch sử nhắc), RLS bật + revoke anon/authenticated; chặn đăng nhập khi `disabled_at` có giá trị.
- [ ] `scripts/bao-cao-tuan.mts` (chỉ đọc, ghi `scripts/logs/hoc-tap-<thứ Hai>.json` + Markdown), `scripts/nhac-hoc-sinh.mts`, `scripts/don-tai-khoan.mts`.
- [ ] Lịch tự động (nếu có) chỉ tạo bản nháp, không tự `--yes`.

## Nhật ký rút kinh nghiệm
- 2026-10-11 · tạo thiết kế · xoá cứng ở ngày 30 sẽ mất điểm/rank khi nghỉ hè → chọn 3 bước có hoàn tác.
