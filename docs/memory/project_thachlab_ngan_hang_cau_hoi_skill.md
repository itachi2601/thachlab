---
name: project_thachlab_ngan_hang_cau_hoi_skill
description: "Skill ngan-hang-cau-hoi (chuẩn hoá file ngân hàng câu hỏi ôn tập, không PHẦN I/II/III) — bước 7 xuat_thachlab.py mới viết, đăng qua /quan-tri/dang-de để tự vào bảng question_bank"
metadata: 
  node_type: memory
  type: project
  originSessionId: 7c9fccc2-7d0b-42e9-9bfa-9484e15d84c0
  modified: 2026-09-19T16:45:25.841Z
---

Skill `ngan-hang-cau-hoi` thầy tự tạo (skill-creator) 2026-09-19, ban đầu chỉ có ở bản Library
(`.../skills-plugin/.../skills/ngan-hang-cau-hoi/`), chưa có ở `~/.codex/skills/`. Đã tạo bản
`~/.codex/skills/ngan-hang-cau-hoi/` khớp y hệt — từ nay **sống ở hai chỗ như azota, phải sửa cả
hai** (xem [[project_thachlab_azota_skill]]).

Việc: chuẩn hoá file trắc nghiệm kiểu "1000+ câu hỏi ôn tập theo chủ đề" (Câu n. → 4 phương án →
Lời giải ngay dưới, KHÔNG PHẦN I/II/III, đáp án KHÔNG đánh dấu sẵn) → đọc lời giải xác định đáp
án → bảng "Câu | Đáp án" 2 cột cuối file → `..._ChuanHoa.docx`.

Sửa 2026-09-19 để khớp chuẩn `/quan-tri/dang-de`:
- Bước 4: chốt CHỈ MỘT hình dạng bảng đáp án (2 cột dọc, không còn lựa chọn "bảng ngang") để
  script đọc lại được.
- Thêm **Bước 7** + `scripts/xuat_thachlab.py de_ChuanHoa.docx nhan.json de_thachlab.docx --grade 12`
  (viết mới, KHÔNG phải bản của azota — format nguồn khác, không PHẦN/HẾT). Dùng lại
  `convert_docx.py` VÀ vài hàm của `xuat_thachlab.py` bên azota (`FORM_OK`, `fetch_topics`,
  `is_listed`, `mark_star`, `norm`) qua `importlib.util.spec_from_file_location` — KHÔNG dùng
  `import xuat_thachlab` thường vì hai script trùng tên, gây circular import (đã tự đụng bug này,
  đã sửa và test lại). Script: chèn `*` trước đáp án đúng ngay trong câu, thêm 2 dòng
  `Chủ đề:`/`Dạng:` từ nhan.json (khoá = số câu, không chia phần), **loại hẳn khỏi file xuất** câu
  còn `?` ở bảng đáp án bước 4 (không đoán đại). Đã test bằng file .docx tự tạo (3 câu, 1 câu `?`):
  parse đúng 3 câu, xuất đúng 2 câu, `*` và nhãn đúng vị trí — chưa test với file thật của thầy.
- Cả hai skill (azota + ngan-hang-cau-hoi) đã thêm dòng disambiguation ngược nhau trong
  `description` để Skill tool trigger đúng cái (có PHẦN I/II/III → azota; không có → skill này).

**Why:** ngân hàng câu hỏi trên LMS (`/quan-tri/ngan-hang-cau-hoi`, bảng `question_bank`) KHÔNG có
form nhập riêng — tự đồng bộ bằng trigger từ `exams.questions` mỗi khi một đề được đăng/sửa qua
`/quan-tri/dang-de`. Vậy nên "đưa ngân hàng câu hỏi lên thachlab" thực chất là đăng nó như MỘT ĐỀ
qua trang Đăng đề, y hệt luồng của azota — chỉ khác việc chuyển định dạng nguồn.
**How to apply:** khi thầy đưa file `_ChuanHoa.docx` muốn "up lên thachlab"/"vào ngân hàng câu
hỏi", chạy bước 7 rồi đăng qua `/quan-tri/dang-de`, chọn mục Luyện tập/BTVN (không phải Kiểm tra).
Xem [[project_thachlab_question_bank]], [[project_thachlab_dang_de_tags]].

**Cập nhật 2026-09-19 (test với file thật — Chủ đề 4 Vật lý hạt nhân, 4 file, 183 câu):**
`scripts/xuat_thachlab.py` của skill này (dùng lại `convert_docx.py`/block engine của azota) **hỏng
với file ngân hàng câu hỏi thật**, không dùng được:
- `convert_docx.blocks()` chỉ duyệt `body.iterchildren()` cấp 1 → **bỏ sót hẳn câu nằm trong bảng
  1-câu-2-cột** (kiểu "Câu N (nguồn): ảnh bên | " — file GV hay dùng bảng để ghép ảnh cạnh đề).
- `RE_CAU = r"^\s*Câu\s*(\d+)\s*[:.]"` đòi số câu theo NGAY sau bởi `.`/`:` → bỏ sót nhãn dạng
  "Câu 13 (Sở Hà Tĩnh): ..." (có ngoặc nguồn xen giữa) — rất phổ biến ở file ngân hàng câu hỏi thật.
- `RE_OPT` chỉ khớp nếu phương án là **đầu dòng của cả paragraph** → format phổ biến "A. x\tB. y"
  (2 phương án/dòng, cách nhau tab) bị coi là 1 phương án duy nhất, B/C/D không tách được.

→ Đã viết **`build_thachlab.py` thay thế hoàn toàn** (không import convert_docx nữa), tự đọc thẳng
từ `_ChuanHoa.docx` bằng `document.iter_inner_content()` (duyệt đúng thứ tự kể cả trong bảng), gộp
mọi paragraph một câu thành "block" bằng ranh giới `Câu N` kế tiếp, tìm 1-2 dòng phương án bằng
cách dò ngược từ trước "Lời giải/Hướng dẫn" (dừng sớm khi đã thấy đủ A,B,C,D — tránh ăn lấn vào đề
dẫn nếu đề dẫn tình cờ có mẫu "khoảng trắng+A."), chèn `*` bằng thao tác run-level (tách run nếu
chữ cái nằm giữa run, không đụng OMML công thức phía sau). Đáp án đọc THẲNG từ bảng "Câu|Đáp án" ở
cuối file `_ChuanHoa.docx` (không dùng lại JSON đáp án cũ nếu file đã bị đánh số lại ở bước 2 — số
cũ/mới lệch nhau).

Phát hiện thêm 3 lỗi định dạng nguồn hay gặp, script mới tự sửa cả 3 (không phải lỗi máy mình gây
ra, mà lỗi có sẵn trong file GV gốc):
1. **Đáp án đúng bị tô nền sẵn trong thân đề** (dù skill giả định "không đánh dấu sẵn") — file
   "FileGV" thực ra CÓ tô màu highlight (`w:highlight`, thường TURQUOISE) ngay trên phương án đúng.
   Phải strip hết `run.font.highlight_color` trước khi giao file cho học sinh (không thì lộ đáp
   án), việc này làm ở bước 2 (`_ChuanHoa.docx`) chứ không phải bước 7. Ngược lại, có thể DÙNG màu
   tô này để đối chiếu chéo (cross-check) đáp án xác định qua lời giải — khớp 100% ở lần test này.
2. **Nhãn "A." đôi khi không phải text mà là số thứ tự tự động của Word** (`w:numPr`) — paragraph
   phương án đầu tiên trông như thiếu hẳn "A." (chỉ có "2.\tB. 1...") vì "A." chỉ hiện qua numbering
   definition, không nằm trong nội dung — y hệt lý do skill cấm đánh số CÂU tự động
   (`docs/DANG-DE-TU-WORD.md`), áp dụng luôn cho cả nhãn phương án. Phải chèn lại "A. " dạng text
   VÀ gỡ `w:numPr` (không gỡ thì hiện trùng "1.A. ...").
3. **Nhãn phương án gõ sai tay**: lặp "D." hai lần thiếu "B." (thứ tự thật: A,D,C,D), hoặc dư
   khoảng trắng "D ." thay vì "D." — sửa bằng cách chuẩn hoá 4 mốc chữ cái đầu tiên tìm được về
   đúng A,B,C,D theo thứ tự xuất hiện (không đụng nội dung phía sau dấu chấm).

File nguồn cũng có thể lẫn câu TRÙNG SỐ (ví dụ "Câu 41" in nguyên văn 2 lần liên tiếp — lỗi copy-
paste khi gộp file) — bước 2 (`_ChuanHoa.docx`) phải đánh số lại liên tục 1..N cho toàn bộ occurrence
(không phải theo nhãn gốc) mới đúng tinh thần "không xoá câu hỏi nào".

Nếu 1 file nguồn gộp nội dung của **nhiều "Bài" khác nhau trong LMS** (ví dụ file "Phóng xạ" vừa có
câu hiện tượng phóng xạ vừa có câu an toàn phóng xạ — 2 bài riêng trong `lessons`), `build_thachlab.py`
hỗ trợ `--lesson <id> --renumber`: xoá hẳn (không chỉ bỏ qua) các câu không thuộc lesson đang tách
— **bản đầu tiên viết code này có bug xoá nhầm chỉ SKIP xử lý mà không xoá paragraph**, khiến câu
bài khác vẫn nằm nguyên trong file xuất, không có `*`/nhãn — đã sửa bằng `delete_block()` xoá hẳn
paragraph (hoặc cả bảng nếu câu nằm trong bảng 1-câu).

**How to apply:** lần sau chạy skill này tới bước 7, ĐỪNG dùng `xuat_thachlab.py` gốc của skill —
dùng bản thay thế đã viết (cần tìm lại/khôi phục từ session này hoặc viết lại theo đúng cách tiếp
cận trên: đọc thẳng `_ChuanHoa.docx` bằng `iter_inner_content()`, không qua `convert_docx.blocks()`).
Đã spawn task riêng để vá lại script chính thức trong thư mục skill.

**Cập nhật 2026-09-25:** `xuat_thachlab.py` (bản ~/.codex; bản synced không có scripts) gọi `cd.chuyen_anh_vector_sang_png()` sau khi lưu Word để EMF/WMF thành PNG. Xem [[project_thachlab_missing_figures]].
