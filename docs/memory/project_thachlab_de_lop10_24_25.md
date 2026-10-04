---
name: project_thachlab_de_lop10_24_25
description: "Số hoá bộ đề Vật lí 10 năm 24-25 (364 bộ/1190 file) bằng scripts/dang-de-l10-24-25.py — 4/10/2026 chạy hết: 176 đề (exam 475–650) vào 4 mục Kiểm tra giữa/cuối kì lớp 10 ĐANG ẨN (lesson 113–116); 167 bộ chưa đăng được liệt kê ở scripts/data/de-l10-24-25-can-xem.md; lời giải + nhãn Chủ đề chưa có; tự luận bị cắt"
metadata:
  type: project
---

Nguồn: `/Users/MAC/Documents/THPT/Lop10/00_Dung_chung/Thu_vien_tai_lieu/CT2025_VietnamTeach/đề thi /24-25/ĐỀ VẬT LÍ 10 2025`
(1190 file, 660 MB; 6 thư mục GHK1/HK1/GHK2/HK2/TỔNG HỢP/HSG). Khảo sát 4/10/2026 bằng
`scripts/data/khao-sat-de-l10-24-25/khao-sat.py` (0 token AI); `python3 scripts/dang-de-l10-24-25.py --list` cho 364 bộ
(bộ = thư mục con hoặc file lẻ; thư mục gom nhiều đề khác nhau không mã đề → mỗi file một bộ).

**Đặc điểm quyết định cách làm (khác hẳn đợt thi thử TN):** mã đề 101–104 là bản xáo của nhau → chỉ lấy 1 file/bộ;
**0 file đánh dấu `*`**, đáp án nằm RỜI (xlsx McMix "Đề\câu", docx đáp án, hoặc mục ĐÁP ÁN sau HẾT); OLE MathType ở ~85% file;
phương án thường viết chung dòng "A. x<tab>B. y" hoặc bố cục 2 cột A C / B D; nhiều đề có tự luận; chỉ 25 file có lời giải.

**4 quyết định thầy chốt 4/10/2026:** (1) đích = 4 mục Kiểm tra giữa/cuối kì lớp 10 — lesson 113/114/115/116, item
53/54/55/56 (đang ẨN, thầy "Hiện" sau khi xem); TỔNG HỢP (đề HK1 các trường TP HCM) vào HK1; HSG bỏ. (2) Bộ không có đáp án: bỏ,
không cho AI giải. (3) Đăng trước, lời giải sinh sau bằng script API. (4) Tự luận giữ dạng essay — NHƯNG parser
`docx-exam-parser.ts` chưa nhận câu tự luận từ .docx nên script hiện CẮT phần tự luận (ghi chú "đã cắt từ đoạn N (TỰ LUẬN)"),
cần làm thêm nếu thầy vẫn muốn giữ.

**Pipeline (`scripts/dang-de-l10-24-25.py`, tài liệu ở đầu file):** chọn file đại diện → .doc qua soffice → đáp án: xlsx đọc
thẳng (cả kiểu Đ/S đánh số liên tục), docx đáp án đọc bảng quen, lạ thì gọi API Sonnet effort low (~2k token/bộ, không tốn token
phiên) → tách phương án chung dòng + sắp A→D + chèn dấu cách → gán đáp án theo SỐ CÂU (đề nhảy số 13→15 vẫn đúng) → nối
"BẢNG ĐÁP ÁN" 3 bảng đúng bố cục convert_docx.py → mtef → convert_docx → xuat_thachlab (nhãn trống) →
`upload-exam-docx.mts --drop-bad --min-keep 10 --drop-mathtype` (cờ mới: câu còn ⟦CT⟧ bị bỏ thay vì chặn cả đề). Lưới an toàn:
số câu convert đọc được ≠ số đáp án → trạng thái LỆCH, không đăng. File trung gian + convert.log ở `scripts/logs/de-l10-24-25/<bộ>/`
(gitignore), kết quả ở `scripts/data/de-l10-24-25-run.json`, log đã đăng `scripts/data/de-l10-24-25-log.json`.

**Thí điểm 6 bộ (4/10/2026) → exam 475 Bình Đông, 476 Đoàn Kết, 477 Nho Quan B, 478 Lý Nhân Tông, 479 Trần Nguyên Hãn, 480 A Nghĩa
Hưng, đều GHK1 → item 53.** Đã đối chiếu tay đáp án 3 đề với khoá gốc: khớp 100%. Câu bị bỏ: thiếu hình (2), còn MathType hỏng
(1, mtef "unhandled tag 131"), phương án kiểu bảng/sắp xếp (1)(2)(3) (4). Tốn ~0 token phiên cho phần chạy; token phiên chủ yếu
để viết/sửa script.

**Việc phát sinh đã làm:** `services/omml-to-latex.ts` bỏ ngoặc với biến 1 chữ → `\vecv`, `\overlineE` (KaTeX lỗi đỏ) — đã vá
code + vá dữ liệu 187/448 đề trên DB (1141 chỗ) qua REST PATCH, sao lưu questions gốc ở
`scripts/logs/fix-accent-backup-2026-10-04.json` (gitignore — đừng xoá).

**Chạy hết 4/10/2026 (2 lượt, lượt 2 sau khi vá script: xlsx cột dài/cột=mã/chuỗi ĐSSĐ, đánh số tự động, suy PHẦN theo
cấu trúc, trải bảng phương án):** 355 bộ → **176 OK** (GHK1 61 → item 53; HK1 72 + TỔNG HỢP 8 → item 54; GHK2 20 → item 55;
HK2 15 → item 56), 12 TRÙNG, 118 SKIP>20%, 46 LỆCH, 3 LỖI. Lý do chưa đăng: 56 bộ không có đáp án ở đâu cả, 50 bộ phương án/đáp án
không đọc được (>20%), 36 lệch số câu, 13 đề nằm trong hộp văn bản/bảng lạ, 10 thiếu hình. Danh sách + lý do từng bộ:
`scripts/data/de-l10-24-25-can-xem.md` (kèm 20 đề đã đăng có phương án trùng chữ, đề 593 có 50 câu). Kiểm máy trên 176 đề: 0 câu
thiếu đáp án, 0 mốc ⟦⟧, 0 lệnh LaTeX dính chữ. Thầy chưa "Hiện" 4 mục.

**Còn chờ:** (a) thầy xem can-xem.md, sửa file gốc rồi chạy lại từng bộ bằng `--sets "<tên>"`; bật "Hiện" 4 mục; (b) nhãn Chủ đề/Dạng = 0 cho mọi câu (script không gọi được Edge
Function classify) → cần đợt gắn nhãn sau (API hoặc trang Đăng đề); (c) lời giải: viết script API theo mẫu
`scripts/backfill-distractor-notes.mts`; (d) tên đề tự suy từ đầu file ("Giữa HK1 2024–2025 – THPT X – Tỉnh"), thầy sửa ở
/quan-tri/sua-de nếu lệch; (e) tự luận (xem quyết định 4). Liên quan: [[feedback_batch_agent_upload_efficiency]],
[[project_thachlab_periodic_exam]].

**Bộ /23 (năm 2023, 4/10/2026):** cùng script, thêm cờ `--nam 23` (`python3 scripts/dang-de-l10-24-25.py --nam 23 --list|--sets|--all`; log riêng `scripts/data/de-l10-23-{log,run}.json`, work `scripts/logs/de-l10-23/`). Nguồn `…/đề thi /23` (3026 file) → 444 bộ (GHK1 141, HK1 203, GHK2 68, HK2 32), kho "BỘ N ĐỀ"/"BO DE" tách mỗi file một bộ; đích vẫn lesson 113–116 (ẩn). Thí điểm: exam 651–656 (đã sửa tay tên 654–656); ~nửa bộ SKIP vì không có đáp án trong file. Chưa chạy `--all`. Script chưa commit.
**Chạy hết /23 xong (4/10/2026):** 444 bộ → 100 OK (HK1 36 → item 54; GHK1 30 → 53; GHK2 21 → 55; HK2 13 → 56; exam 651+), 9 TRÙNG, 309 SKIP>20% (đa số không có đáp án trong file), 21 LỆCH, 5 LỖI. Chi tiết ở `scripts/data/de-l10-23-run.json`. 4 mục vẫn ẨN; chưa soát từng đề, chưa nhãn/lời giải.
