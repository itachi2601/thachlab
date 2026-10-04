---
name: project_thachlab_de_lop10_24_25
description: "Số hoá bộ đề Vật lí 10 năm 24-25 (364 bộ trong 1190 file, thư mục CT2025_VietnamTeach) bằng script scripts/dang-de-l10-24-25.py — thí điểm 6 bộ xong 4/10/2026 (exam 475–480, mục 53 lesson 113 đang ẩn); còn 358 bộ chờ chạy --all; lời giải + nhãn Chủ đề chưa có; tự luận bị cắt"
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

**Còn chờ:** (a) chạy hết: `python3 scripts/dang-de-l10-24-25.py --all` (364 bộ, ~3 phút/bộ, có `--limit/--offset`), xem
run.json: OK / SKIP>20% / LỆCH / LỖI, bộ LỆCH+LỖI để thầy xem; (b) nhãn Chủ đề/Dạng = 0 cho mọi câu (script không gọi được Edge
Function classify) → cần đợt gắn nhãn sau (API hoặc trang Đăng đề); (c) lời giải: viết script API theo mẫu
`scripts/backfill-distractor-notes.mts`; (d) tên đề tự suy từ đầu file ("Giữa HK1 2024–2025 – THPT X – Tỉnh"), thầy sửa ở
/quan-tri/sua-de nếu lệch; (e) tự luận (xem quyết định 4). Liên quan: [[feedback_batch_agent_upload_efficiency]],
[[project_thachlab_periodic_exam]].
