---
name: project-thachlab-kiem-tra-dau-vao
description: Kiểm tra đầu vào (chẩn đoán) cho em vào lớp trễ — đã chạy migration + deploy 12/10/2026, chưa thử HS thật
metadata:
  type: project
---

Em vào trễ chưa có bài nào nên không có mục phụ đạo → thẻ `EntryDiagnosticCard` (trang chủ HS + `/phu-huynh`) mời làm bài chẩn đoán: tối đa 6 bài × 3 câu (2 dễ + 1 TB, bỏ câu khó), sai 2 câu thì dừng bài; không tính điểm/xếp hạng. RPC `diagnostic_submit` mở `tutoring_needs` (sai ≥2 và ≥60%, note "chẩn đoán đầu vào") và báo em + phụ huynh + trợ giảng. Mỗi em một lần. Migration `20261012120000_kiem_tra_dau_vao` đã chạy, code deploy 12/10 tối.

**Why:** thầy chốt 12/10: gợi ý chứ không bắt buộc, có gửi phụ huynh.
**How to apply:** chỉ hiện với em có `thpt_registrations.joined_late` (catchup/active); em thêm thẳng vào lớp không qua đăng ký sẽ không thấy thẻ. 13/10: đã thêm `components/dashboard/DiagnosticAdmin.tsx` — chip "đã chẩn đoán + Cho làm lại" ở danh sách lớp (em vào trễ, mục Đang bù bài/Đã vào lớp) + thẻ chi tiết từng bài ở Hồ sơ học sinh (chưa commit, chưa thử trình duyệt). Còn thiếu: thử bằng tài khoản HS thật + chụp 375px. Liên quan [[project-thachlab-phu-dao]].

**2026-10-15:** migration `20261014150000_giao_em_cho_tro_giang` đã chạy (10:57): bảng `ta_student_handoffs` + 4 hàm `ta_handoff_*` + 1 trigger tự gán mục phụ đạo cho trợ giảng được giao. Nút "Giao trợ giảng" (DiagnosticAdmin/hồ sơ HS) đã deploy từ trước nhưng CHƯA thử thao tác thật (giao 1 em, kiểm TA thấy thông báo + mục phụ đạo). `20261014140000_chan_doan_ban_do_xuat_phat` cũng đã chạy từ 14/10 14:00 và đã trong main.
