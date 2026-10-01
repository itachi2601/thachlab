---
name: project_thachlab_mtef_decoder_v2
description: Bản decoder MTEF→OMML đã vá lỗi (thay cho mtef_to_omml/ cũ trong _CongCu) — dùng cho mọi việc chuyển công thức MathType hàng loạt
metadata:
  node_type: memory
  type: project
  originSessionId: b3a690b0-c751-48c5-b129-65e08a458da9
  modified: 2026-09-26T01:17:46.661Z
---

Vị trí chính thức (dự án, không phải skill): `THPT/Lop12/NamHoc/2026-2027/06_Azota_so_hoa/_CongCu/mtef_to_omml_v2.py`
(kèm `mtef_to_omml_v2_README.md` cùng thư mục). CLI: `python3 mtef_to_omml_v2.py scan|convert *.docx`.

Bản `_CongCu/mtef_to_omml/` cũ (3 file mtef.py/omml_gen.py/convert_mtef.py) có bug hệ thống ở
`parse_tmpl()`: thiếu đọc 1 byte "options" đầu record TMPL → lệch byte toàn bộ phần sau → 94.9%
công thức lỗi dồn vào "unknown-tag:102". Đã thử vá đúng phần đó nhưng KHÔNG đủ (kết quả không đổi
trên 2 file test) — nguyên nhân gốc còn ở chỗ khác trong bộ 3 file đó, chưa tìm tiếp vì đã có bản
thay thế hoạt động tốt hơn nhiều.

`mtef_to_omml_v2.py` (984 dòng, tự chứa, chỉ cần `olefile`+`lxml`) là bản độc lập, viết/test
25/9/2026 (khớp ảnh gốc 100% trên 13 file mẫu ban đầu), rồi vá thêm 1 lỗi top-level (công thức có
"hàng" phụ phía sau, ví dụ watermark dính theo, bị dừng đọc sớm → "trailing bytes"). Chạy trên toàn
bộ `01_De_da_chuyen_2025/` (219 file): 8987 → 11 công thức MT7 còn sót, 213/219 file sạch hoàn toàn.
11 công thức còn lại (6 file) là ca lẻ tẻ không cùng nguyên nhân — để sửa tay sau nếu cần.

Bản sao lưu thứ hai (đề phòng): `~/.claude/projects/-Users-MAC-Projects-thachlab/memory/_backup_mtef_script/`
— giữ vì skill gốc `mathtype-sang-omml` sống ở `~/.claude/skills/synced/...` chỉ là bản đồng bộ từ
claude.ai, sửa trực tiếp ở đó KHÔNG bền (thầy xác nhận: sửa phải qua claude.ai rồi đồng bộ xuống).
Script trong `_CongCu/` (nằm trong thư mục dự án, do Git/Finder quản lý bình thường) mới là nơi bền.

**Why:** batch "MT7-OMML-Azota" hàng loạt cực tốn token nếu để agent tự viết lại decoder mỗi lần —
xem [[project_thachlab_azota_skill]] phần "bài học đắt giá" (552.927 token cho 13 file do không kiểm
tra công cụ có sẵn trước).

**25/9/2026 (tiếp) — kiểm tra chuẩn Azota cho 219 file:** viết script đọc trực tiếp 3 bảng đáp án
(nhận diện theo nội dung ô — hàng đầu "Câu" hoặc dãy số 1..N — KHÔNG theo vị trí bảng cuối cùng, vì
nhiều đề có bảng dữ liệu số liệu xen giữa các câu làm lệch vị trí). Kết quả: 216/219 file đúng chuẩn
hoàn toàn. 2 file lỗi thật (không phải lỗi định dạng, mà lỗi NỘI DUNG đề gốc — đã sửa 25/9/2026):
- `122. SO GIAO DUC VA DAO TAO HAI DUONG 2025 LAN 2_Azota.docx` câu 15: đề gốc ghi đáp án "E" nhưng
  đề chỉ có 4 phương án A-D. Thầy chốt: **A**.
- `25. THPT PHU CU HUNG YEN 2024 - 2025_Azota.docx` câu 13: lời giải gốc ghi "câu này đúng với cả 4
  đáp án". Thầy chốt: **D**.
Đã điền thẳng vào ô đáp án trống trong bảng (giữ nguyên định dạng run có sẵn, không tạo run mới).

**26/9/2026 — chuyển nốt 34 file chưa qua Azota:** 34 file trong `01_De_da_chuyen` hoá ra chưa từng
qua bước Azota (dù MT7 đã sạch) — cấu trúc gốc: câu nằm trong bảng riêng, PHẦN I lặp 2-3 lần (nhiều mã
đề gộp 1 file). Test `_CongCu/convert_docx.py` trên 3 file mẫu khác nguồn → xử lý đúng cả (script tự
xử lý multi-mã-đề, không cần sửa gì). Chạy tay từng file (không dùng vòng lặp `while read < file` —
vòng lặp này bị TREO khi chạy nền, 33 phút 0 tiến triển, nguyên nhân chưa rõ; gọi từng lệnh riêng biệt
thì chạy bình thường vài giây/file) → **33/34 thành công**, sạch hoàn toàn. Ngoại lệ:
- File 38 (`TRUNG TAM LUYEN THI DAI HOC SU PHAM DE 9+ NAM 2026 LAN 10`): crash `IndexError` ở
  `build()` dòng ~604 (`"abcd"[j]`) — đề gốc bị lẫn nội dung 2 câu Phần II vào chung 1 khối, khiến
  `parse()` đếm ra 5 "ý" cho 1 câu thay vì 4. Chưa sửa, để dành điều tra riêng.
- File 29 (`TRUNG TAM LUYEN THI DAI HOC SU PHAM DE 9+ NAM 2026 LAN 05`): thiếu lời giải câu 11-18
  Phần I (script báo rõ, chưa bổ sung).
- File 35 (`THPT CAM PHA QUANG NINH 2026`) trùng nội dung với `Lop12_ThiThuTN_CamPha_QuangNinh...`
  đã biết trước — cùng thiếu đáp án Phần III câu 6 (đề gốc thiếu dữ kiện "V").
- Rất nhiều file có cảnh báo "đoạn dẫn/bảng dùng chung" (câu liền kề dùng chung dữ kiện) — chưa rà,
  cần bước 4 của skill azota (đọc lại, xem có phải khoá thứ tự khi trộn đề không).
33 file đã chuyển gom vào `/Users/MAC/Documents/THPT/số hoá THPT/các đề đã xong` theo yêu cầu thầy
(sau đó gom nốt 219+143 file đã xử lý từ trước vào cùng thư mục — tổng ~363 file).

**Bài học điều phối subagent:** giao "soát chất lượng 6-7 file" cho 1 agent — ít nhất 2/5 agent lại
tự ý TÁCH THÊM thành 6-7 agent con (mỗi agent con 1 file) thay vì tự làm trong 1 lượt, dù prompt không
hề gợi ý làm vậy. Kết quả: đúng kiểu phân mảnh quá nhỏ (fixed cost nạp skill/tool nhân lên) mà cả phiên
25-26/9/2026 đang cố tránh (xem phần "bài học đắt giá" ở trên). **How to apply:** khi giao 1 agent xử
lý một LÔ nhiều file, phải ghi rõ trong prompt: "tự làm trực tiếp, KHÔNG được gọi Agent/Task để tách
thêm subagent con" — nếu không dặn, agent có xu hướng tự tách nhỏ việc ra.

**Cạm bẫy khi tự viết script kiểm tra bảng Word (python-docx):** `len(table.columns)` đếm theo lưới
`tblGrid` của Word, có thể LỆCH với số ô thực (`len(row.cells)`) khi nội dung dài (số thập phân dấu
phẩy như "0,04") làm Word co giãn lưới cột — gây báo lỗi giả. Luôn đối chiếu bằng mắt (`row.cells`)
trước khi kết luận file lỗi. Đã tự vấp lỗi này 3 lần liên tiếp trong phiên 25/9/2026 trước khi ra được
kết quả đúng.
**How to apply:** bất cứ khi nào cần chuyển MT7→OMML hàng loạt, dùng thẳng
`_CongCu/mtef_to_omml_v2.py convert *.docx` trước — script thuần, gần như miễn phí token — chỉ giao
việc cho AI/agent với các file/công thức mà script này báo lỗi (xem log để biết chính xác công thức
nào, đừng giao cả file).
