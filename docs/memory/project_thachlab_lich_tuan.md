---
name: project_thachlab_lich_tuan
description: Lịch công tác tuần của thầy (skill lich-tuan) — mục Lịch tuần ở /tai-khoan, mốc bài Vật lí + HSG 9, script ghi mốc; deploy 2026-10-18
metadata:
  type: project
---

**Mục tiêu:** một chỗ duy nhất thầy mở điện thoại là thấy tuần này dạy gì, tới bài nào, họp gì, tập lúc nào — skill `.claude/skills/lich-tuan/` (SKILL.md là quy trình trọn vẹn, bước 0–6).

**Đã xong (2026-10-18, commit 9cbdbc0bd, 07b27a362, b9c817b93; đã push main + deploy 23:54):**
- `components/account/StaffWeekPlan.tsx`: mobile dải 7 ngày + xem từng ngày (vuốt), desktop lưới 7 cột, dòng "Tiếp theo/Đang diễn ra/Mở đầu tuần", tổng kết buổi dạy/trượt băng/gym (cảnh báo thiếu), chú giải màu, ghi chú dài gập `<details>`, tiêu đề ghi tuần. Dữ liệu `staff_week_plans` (RLS chủ tài khoản), mỗi mục có `lesson` (dòng mốc bài hiện rõ) và `note` (gập).
- `scripts/lich-tuan.mts`: buổi Vật lí ghi `lesson` = "Đã tới: <current_topic_id> · Tiếp: <chủ đề tầng bài kế tiếp cùng khối>", `note` = nhịp buổi (`buoi_day.nhip` trong `references/lich-co-dinh.json`: tự ôn 10–15′ → KT bài cũ 20–25′ → sửa bài & ôn 30′ → bài mới); khoá ôn thi không mốc → `buoi_day.ghi_chu_khoa[id]` (12L1 B7=7, B8=8 "Ôn thi học kì 1"). Buổi "Dạy HSG KHTN 9" lấy mốc từ `scripts/data/btvn-hsg9/tuan.json` (khớp `ngay` dd/mm với thứ Bảy).
- `scripts/ghi-moc-bai.mts`: `--khoa` (xem mốc), `--tim "<tên>"` (id chủ đề tầng bài), `<course>:<topic>:<ngày>` ghi qua `teaching_set` với `set_config(request.jwt.claims, sub=uid thầy)` bằng `supabase db query --linked` (chạy trong tab terminal, Bash bị chặn supabase.co).
- Mốc đã ghi 2026-10-18 theo thầy báo: 10L3 (1) & 10L4 (2) → 22 Tổng hợp và phân tích lực; 11L4 (3) giữ 45 Giao thoa sóng (đã học tới giao thoa ánh sáng, là chủ đề con); 11L5 (4) → 46 Sóng dừng; 12L1 A4 (5) & A5 (6) → 68 Đại cương dòng điện xoay chiều. Thầy xác nhận đúng.

**Bổ sung 2026-10-19 (commit c6c26b64f, 545bf175c, 032e3a03d; deploy nhánh deploy 5eef2ee, kiểm trên site thật):**
- Mục công tác có chữ "Thạch" = thầy → luôn giữ (`ten_thay` trong `lich-co-dinh.json`, note "CÓ TÊN THẦY"); cả trường chỉ một người tên Thạch.
- Lịch công tác được ưu tiên: việc khác trùng giờ chỉ ghi cảnh báo "cần nhờ người dạy/dự thay" (khung "Cần chú ý — nhờ người xem hộ" ở đầu mục Lịch tuần), không tự bỏ; hai mục công tác trùng nhau thì thầy chọn mục dự (script bước 5b).
- Tuần 19–25/10 có cảnh báo Thứ 6 23/10: hội thảo kỹ năng xanh 07:30–11:30 (có tên thầy) trùng dạy TACN tiết 1–2, duyệt đồ án, và hội thảo khuôn mẫu Duy Tân 10:00. Chờ thầy nhờ người xem hộ, chưa cập nhật lịch theo lựa chọn nào.
- Giờ tiết Cao Thắng đã chốt: 45 phút, nghỉ 5 phút, nghỉ 10 phút giữa tiết 3–4; sáng 6h30, chiều 12h30 (ghi trong SKILL.md). TKB đọc từ portal sau khi thầy tự đăng nhập trong tab trình duyệt.

**Bổ sung 2026-10-19 (tối):** nội dung từng buổi trượt băng/gym (`noi_dung_tap` trong `lich-co-dinh.json`, bước 5a trong `lich-tuan.mts`) đã ghi vào `staff_week_plans` tuần 19/10 (34 mục). Nhận xét lịch đã nêu với thầy: T3 gym rồi 2 giờ sau lên băng (giải quyết bằng gym thân trên), T7 băng 17:30 sau ngày dài → buổi Ôn nhẹ, T2 giữ là ngày nghỉ tập. Thầy chưa cho địa điểm sân băng/gym.

**Quyết định không suy ra từ code:** thầy nêu lớp theo "thứ" có thể lệch `thpt_course_schedules` (nói "lớp 10 thứ 2" trong khi 10L3 dạy thứ 3) → đối chiếu theo tên khoá, nêu cách hiểu khi báo. Mốc chỉ nhận chủ đề `parent_id null` đúng khối (RPC từ chối chủ đề con).

**Còn chờ:**
- Thầy chạy `bash scripts/cai-skill.sh` sau khi pull để bản skill ngoài repo cập nhật.
- Dòng "Tiếp theo · còn X phút" chỉ hiện khi xem tuần hiện tại — chưa thấy trên dữ liệu thật (tuần 19/10 là tuần tới lúc làm). Vuốt chuyển ngày chưa thử trên điện thoại thật.
- Chưa có cách tự động nhận tiến độ: mỗi tuần thầy vẫn phải báo "lớp X tới bài Y" (hoặc tick ở dashboard giáo viên → tiến trình) rồi chạy lại `lich-tuan.mts --ghi`.
- Địa điểm trượt băng/gym, nội dung "việc khác 10h T2", giờ tiết tối Cao Thắng: vẫn trống trong `lich-co-dinh.json`.
