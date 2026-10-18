---
name: project-thachlab-casio-vat-ly
description: Ôn thi Giải Vật lí trên máy tính cầm tay (Casio) — kế hoạch 12 gói WP-00..11; WP-01,03,04,05,06 đã soạn xong (18/10/2026), chờ thầy bấm thử máy và công văn thể lệ
metadata:
  type: project
---

Kế hoạch + bảng trạng thái từng gói: `docs/KE-HOACH-CASIO-VAT-LY.md` (có prompt mẫu giao Opus và nhật ký rút kinh nghiệm). Nội dung: `content/casio-vat-ly/wp-0X-*/` (mỗi gói: `ky-thuat.md` hoặc `so-tay.md`, `bai-luyen.md`, `mini-test.md`, `tinh.py`, `README.md`).

**Tiến độ (2026-10-18, đã commit trên main):**
- WP-01 sổ tay fx-580VN X (8 mục + 20 bài luyện), WP-03 dao động cơ, WP-04 sóng cơ, WP-05 điện xoay chiều, WP-06 điện từ + sóng ánh sáng: mỗi chuyên đề 3 trang kỹ thuật + 12 bài (4⭐/6⭐⭐/2⭐⭐⭐) + mini-test 4 bài. Đã kiểm 2 lần: `tinh.py` và `kiem-code` giải độc lập (mọi đáp số khớp).
- Chưa làm: WP-00 (tóm tắt thể lệ), WP-02 (quy tắc ghi/làm tròn), WP-07 (lượng tử + hạt nhân), WP-08 (nhiệt, khí, từ trường), WP-09 (tổng hợp + thực nghiệm), WP-10 (6 đề thi thử), WP-11 (sổ lỗi máy).

**Còn chờ:**
- Thầy bấm thử máy (2026-10-18 thầy nói sẽ thử rồi báo): ưu tiên SOLVE (S1), TABLE (T1), số phức (X1), hồi quy mũ (St3), phím biến `D`, tên mục menu (Var, Reg, Dot, CMPLX, CONV). Mọi tên phím/menu CHƯA thử trên máy thật.
- Công văn thể lệ năm 2026–2027 (Công văn 5704/SGDĐT-GDPT là của 2025–2026, chưa đọc được nội dung): đến khi có, làm tròn dùng tạm 4 chữ số có nghĩa, thời gian/số bài chưa biết. Có công văn thì làm WP-00 + WP-02 rồi rà lại cả 5 gói.
- Dòng chỉ mục trong `docs/memory/MEMORY.md` thêm 2026-10-18 nhưng chưa commit (file đó còn thay đổi dở của phiên khác).

**Quyết định đã chốt (không suy ra được từ code):**
- Biến nhớ trên fx-580VN X chỉ có A–F, X, Y, M (không có W, Z); `X` dành cho SOLVE/TABLE. Dùng `D` cho ω/λ trong lệnh bấm.
- Đáp số trong tài liệu phải sinh từ `tinh.py` (kể cả số trong mục Bẫy); công thức luôn ghi điều kiện áp dụng (r<d, N nguyên, A≥0, nguồn kết hợp…).
- Đề cho số (h, c, g) thì dùng số đề cho, không dùng hằng số có sẵn trong máy.

**Rút kinh nghiệm (2026-10-18):**
- Tách đề khỏi đáp án để kiểm độc lập bằng `split('## Đáp án')[0]`, rồi kiểm file đề không lọt đáp án; `sed` theo mẫu `**M1.` từng bắt cả khối đáp án (WP-03/04 mini-test phải kiểm lại, 12/12 khớp).
- `kiem-code` hay bắt lỗi ở công thức/điều kiện và số phụ trong Bẫy dù đáp số đúng; tên phím/biến máy phải nhờ rà ngay từ gói đầu (lỗi `W` lan sang 4 gói).
- Tốn token ít khi mỗi gói chạy đúng một vòng: tinh.py → viết → 1 agent kiểm → sửa → commit.

Xem [[project-thachlab-khoa-hsg9-vat-ly]] cho quy trình soạn tương tự.
