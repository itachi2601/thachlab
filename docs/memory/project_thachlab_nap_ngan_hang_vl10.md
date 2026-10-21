---
name: project_thachlab_nap_ngan_hang_vl10
description: Nạp câu từ bộ Word "Vật Lý 10 - Dùng cho 3 sách" vào ngân hàng — Ch.II–VI đã nạp (952 câu Hiện), còn Ch.I/VII + Cơ năng; quy trình + lỗi nguồn đã biết
metadata:
  type: project
---

**Mục tiêu (thầy, 2026-10-20):** tăng số câu ngân hàng lớp 10 từ `Documents/THPT/số hoá THPT/Vật Lý 10 - Dùng cho 3 sách - Bộ 1 - Theo form mới 2025(Xong)/{HKI,HKII}/<chương>/*.docx`. Ưu tiên CHÍNH XÁC tuyệt đối, không vội; tiết kiệm token phiên → việc thô đẩy qua Anthropic Batch (không có key DeepSeek). Câu lệch/mơ hồ/thiếu hình → XOÁ luôn, không giải lại (xem [[feedback_bo_cau_mo_ho_thay_vi_giai_lai]]).

**Đã nạp (đang Hiện, tất cả note `nap-vl10-cN-20261020`, hoàn tác: `delete from question_bank where note=…`):**
- Ch.III Động lực học: 319 câu (c3, dữ liệu ở gốc `scripts/data/nap-ngan-hang-vl10/`)
- Ch.II Động học: 420 câu (`c2/`)
- Ch.IV Năng lượng: 124 câu (`c4/`), mới 4/5 file
- Ch.V Động lượng: 33 câu (`c5/`, 21/10; 158 bóc → 119 trùng bỏ → 39 giải → 3 xoá). Hiện 33.
- Ch.VI Chuyển động tròn: 56 câu (`c6/`, 21/10; 129 dựng → 55 trùng → 74 giải → 7 xoá + 12 loại vì nguồn thiếu lời giải/gạch chân kiểu lạ). Hiện 56.
- Tổng 952 câu. Word nguồn đã xong được chuyển vào `đã đăng lên thachlab/Vật Lý 10 …/<HK>/<chương>/` (Ch.II 8 file, Ch.III 9, Ch.IV 4).
- Mỗi chương còn các câu bị loại (`loai-ra.json`: có hình EMF/PNG, không gạch chân đáp án, bảng ĐS lỗi…) — chưa xử lý.

**CÒN LÀM:** Ch.I Mở đầu (HKI), Ch.VII Biến dạng (HKII); Ch.IV Chủ đề 5 Cơ năng (pandoc sập "maximum: empty list", đã thử bỏ bảng/hình/textbox, soffice không ra file → thử lưu lại file bằng Word rồi bóc lại); câu có hình (cần chuyển WMF/EMF→PNG, dò bằng mắt). Chủ đề id lớp 10: Ch.I 103–106, Ch.II 107–118, Ch.III 119–131, Ch.IV 132–141, Ch.V 142–145, Ch.VI 146–149, Ch.VII 150–153 (`c*/…/chu-de-lop10.json` ở gốc).

**Quy trình chương mới (đã chốt, thứ tự quan trọng):** `export VL10_DIR=scripts/data/nap-ngan-hang-vl10/cN VL10_NOTE=nap-vl10-cN-20261020 VL10_CHI_HAI_MAY_DONG_Y=1` → copy docx vào `cN/nguon/` + `mtef_to_omml_v2.py convert` (trên bản sao; công cụ ở `Documents/THPT/Lop12/NamHoc/2026-2027/06_Azota_so_hoa/_CongCu/`) → pandoc (`pandoc-an-toan.py`) ra `md/` → `parse.py` → `dung-cau.py` → **LỌC TRÙNG NGAY** `scripts/loc-trung-vl10.mts` → `batch-nap-vl10.mts nop --model=haiku` + `thu`, đổi tên ket-qua*/batch-state*, rồi `nop --model=sonnet --chi-cau-chua-khop-trong=ket-qua-haiku.json` + `thu` → `lap-duyet.py` (tự loại câu Haiku≠Sonnet; trang `cN/duyet/duyet.html`) → [thầy duyệt, lưu phan-hoi.json, thường rơi vào ~/Downloads] → `ap-duyet.py` → quét mẫu lỗi nguồn (dưới) → `batch-gan-nhan-vl10.mts nop <id-đầu>-<id-cuối>` + `thu` → `ghi-ngan-hang-vl10.mts` (dry-run rồi `--apply`, ghi Ẩn) → `batch-do-lan2-vl10.mts nop/thu` → `hien-vl10.mts` (dry-run, kiểm KaTeX, `--apply`; `cN/loai-them.json` = câu lỗi phát hiện thêm) → xoá các câu còn Ẩn (mẫu `c4/bo-cau-an.sql`) → chuyển Word. KHÔNG `git add` cả thư mục cN (nguon/media nặng đã vào .gitignore); chạy lệnh có mạng trong tab terminal (Bash bị sandbox chặn).

**Lỗi nguồn/pipeline đã gặp & cách chặn:** đáp án MC = chữ gạch chân trong Word (30/1548 không có → loại); Đúng–Sai Ch.II không có bảng Đ–S (suy từ "**đúng**/**sai**" trong lời giải → cờ `ds-tu-loi-giai`); bảng pipe-markdown bị nối phẳng → `bang.py`; `~sub~`/`^sup^` làm hỏng công thức → `inline()` bỏ qua trong `$…$`; `\Deltat`/`\leqt` dính liền → clean_math chèn cách; `&gt;`/`&lt;` trong công thức → hien-vl10 đổi `\gt`/`\lt`; `**` thừa; **MathType làm mất "g = 10 m/s²" thành "Lấy $2.$"** (Ch.IV, 11 câu, đã vá g=10 theo lời giải gốc; quét `[Ll]ấy\s*\$\s*[0-9]*\s*\.?\s*\$` ở chương mới); lib `katexLoi` báo lỗi giả với `$$…$$`; Sonnet chạy 2 lần cho đáp án khác nhau ở câu mơ hồ → không lấy đa số.

**Ch.V (21/10) rút kinh nghiệm:** pandoc xuất bảng Đ–S dạng HTML `<table>` khi ô nhiều đoạn → parse.py đã vá (mở lại 14 câu Đ–S; Ch.II/III/IV có thể từng loại oan loại `bang-dung-sai-khong-du-4-y` — chưa rà lại); file bọc blockquote `> ` phải bỏ `> ` trước parse; `\overset{\rightarrow}` MathType bị tách qua 2 `<p>` trong lời giải do AI → hien-vl10 có `noiVecto`; câu mất vectơ khiến 2 phương án cùng đúng (mc-008) hoặc trùng nhau (mc-021) → xoá. Dò lần 2 cờ `katex-loi` với chữ Việt là báo giả.

**Ch.VI (21/10) rút kinh nghiệm:** lời giải "Hướng dẫn giải" của Word lọt vào đề (3 câu sa) hoặc vào phương án D (mc-039) → cắt trước ghi; 4 phương án giống hệt (mc-036) → xoá; `sua-noi-dung.json` (options) vá được phương án lỗi mà không giải lại; `$$$` cuối phương án gây KaTeX lỗi. Ch.II–V có thể còn sót "Hướng dẫn giải" trong đề — chưa rà.

**Bài học vận hành (rút kinh nghiệm):** lọc trùng TRƯỚC khi giải (làm ngược ở Ch.III tốn thừa 67 câu); Batch `max_tokens` Haiku ≥2000 (200 làm cụt JSON); `custom_id` Batch không có ':' và phải duy nhất (Word đánh lại số câu → dùng số thứ tự); đổi chỉ số nhóm regex phải rà mọi `m.group(i)`; so khớp chữ cái trần với ngân hàng chỉ là ước lượng; chi phí cả đợt ~$7 (Haiku ~$0,1/chương, Sonnet dò lần 2 ~$1–3/chương). Skill `ngan-hang-cau-hoi`/`azota` nằm ngoài repo → nhắc thầy cập nhật nếu muốn đưa quy trình này vào skill.
