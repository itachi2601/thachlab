---
name: project_thachlab_up_de_skill
description: "Skill \"up-de-kiem-tra\" — đường chính (9/2026) là văn bản Azota + dòng Chủ đề/Dạng dán vào /quan-tri/dang-de; gói JSON nhap-bai chỉ dự phòng"
metadata: 
  node_type: memory
  type: project
  originSessionId: 9791774d-af3d-44ae-90eb-7bbb877b8b0d
  modified: 2026-09-20T04:58:55.921Z
---

Ngày 2026-09-08 user yêu cầu tạo skill tự động hoá việc up một file đề kiểm tra Word lên thachlab.

Skill nằm ở `.claude/skills/up-de-kiem-tra/` **trong repo thachlab** (project skill, không phải
plugin store như [[project_thachlab_lesson_importer]] / dang-bai-hoc-thachlab / de-vat-ly-thpt).
Nếu user muốn nó nằm chung thư viện skill toàn cục thì phải tạo lại qua skill creator trên claude.ai.

Pipeline: file đề **.pdf (nhanh nhất — user tự xuất PDF từ Word)** hoặc .docx (Azota-style, đáp
án đánh dấu `*`, công thức MathType) → đọc bằng Read → soạn `draft.json` → `scripts/build_bundle.py`
(tự chạy bộ validate của trang admin) → dán vào `/quan-tri/nhap-bai`, tick **Kiểm tra**, Đăng.

~~LibreOffice trên máy user đang hỏng~~ — 2026-09-09: đã cài lại, `soffice --headless --convert-to pdf`
chạy tốt, đọc được cả bảng đáp án + lời giải chi tiết trong file (đề "đã chuyển" có sẵn phần này).

**Lần chạy 2026-09-09 (đề Nguyễn Khuyến LTT, giữa HK1 lớp 12 → bài id 96):** vài chỗ vướng, ghi lại:
- **Browser pane trong app KHÔNG share login thachlab** (là Chrome riêng). Phải dùng
  `mcp__claude-in-chrome` (Chrome thật của user). User đăng nhập ở tab thường → tab MCP cùng hồ sơ
  nhận session (Supabase lưu localStorage).
- **Dán bundle 30KB vào textarea:** `form_input` tự `JSON.parse` giá trị → hỏng ("[object Object]").
  Cách chạy được: commit bundle lên 1 nhánh git tạm → `fetch` raw.githubusercontent (CORS `*`) trong
  page context → set `textarea.value` qua native setter + dispatch `input`. Xong xoá nhánh.
- **Checkbox "Gắn vào Kiểm tra" ở /quan-tri/nhap-bai:** set qua `form_input`/`javascript` KHÔNG vào
  React state — trang vẫn dùng mặc định (Luyện tập). Kết quả: đề bị gắn `luyen_tap`. Phải vào
  `/quan-tri/bai-hoc` → Soạn mục → Sửa mục đó → đổi loại select sang "📝 Kiểm tra" (cái này set
  qua form_input thì ăn) + xoá mục `bai_tap_mau` rỗng trang tự tạo.
- **`window.confirm()` làm treo renderer qua CDP** (claude-in-chrome). Patch `window.confirm=()=>true`
  bằng javascript_tool TRƯỚC khi bấm nút "Xóa". Nếu đã treo: `navigate` đi chỗ khác để thoát.

Khác `dang-bai-hoc-thachlab` (đăng trọn bài từ .tex) — skill này chỉ lo khối `exam`, vẫn phải
kèm một `theory_html` "Công thức trọng tâm" ngắn vì validator chặn theory rỗng.

**Why:** "Kiểm tra"/"Luyện tập" (`lesson_items.exam_ids`) không nhập câu hỏi trực tiếp được — chỉ
trỏ tới bảng `exams`; trang Bài học chỉ cho tick đề đã có. Đây là chỗ user hay kẹt "không nhập được".
**How to apply:** user thả file .docx đề + nói up lên lớp/bài nào → chạy skill up-de-kiem-tra.

**Sửa 2026-09-14 (chưa commit):** `SKILL.md` giờ bắt **đọc ảnh trang PNG trong subagent
`general-purpose`, không đọc thẳng ở phiên chính** — 1 trang ≈ 1,5k token nằm lại đến hết
phiên, đề 13 trang × vài trăm request là hàng chục triệu token. Đề ≤ 3 trang thì đọc thẳng
vẫn được. Xem [[feedback-token-discipline]].

**Sửa 2026-09-19 (đã commit):** SKILL.md đổi đường chính sang `/quan-tri/dang-de`: soạn `de.txt`
kiểu Azota (dấu `*`, `Lời giải:` nhiều dòng, hai dòng `Chủ đề:`/`Dạng:` mỗi câu) → soát bằng
`scripts/soat_nhan.py de.txt --grade 12 --fix` (danh mục thật, gợi ý tên gần nhất) → dán qua
`paste_relay.py de.txt --target https://thachlab.id.vn/quan-tri/dang-de/` → kiểm bảng Phân loại câu
n/n → Đăng. Gói JSON `build_bundle.py` + nhap-bai giữ làm đường dự phòng khi cần SVG/ảnh scan.
Liên quan [[project_thachlab_dang_de_tags]], [[project_thachlab_azota_skill]].

**Lần chạy 2026-09-19 (đề Bài 4 Điện xoay chiều → lesson 14, BTVN):** file docx nguồn có 43 công
thức OLE MathType chưa convert + 3 ảnh nhúng thật (đồ thị u–t, 2 giản đồ tròn ở lời giải) → phải
đi đường dự phòng (`build_bundle.py` + `/quan-tri/nhap-bai`), không dùng được `de.txt`/`dang-de`.
Trước khi tin lời giải gốc: **đối chiếu `pdftotext -layout`** với bản subagent chép từ ảnh — subagent
làm rơi mất dấu căn/số mũ ở vài chỗ (vd "100 V" lẽ ra là "100√6 V" ở một câu vuông pha, khớp lại
được nhờ đáp án cuối bài phải ra đúng số cho trước). Ảnh nhúng thật trong .docx: `unzip -o de.docx
"word/media/*"` rồi mở từng ảnh xem — nhiều ảnh chỉ là icon trang trí (π, √, máy phát điện...), vài
ảnh là chính lời giải/hình vẽ cần giữ nguyên (xem cách nhận diện trong
[[project_thachlab_bai13_dien_xoay_chieu]]). Mục tiêu BTVN nhưng `/quan-tri/nhap-bai` không có ô
đó — cách đăng gọn xem [[project-thachlab-lesson-sections]].

**Lần chạy 2026-09-20 (đề KTTX tuần 8 GHKI → Lớp 10, Kiểm tra chương 2 "Động học", lesson 102):**
docx có 41 OLE MathType + 5 ảnh nhúng thật (trục toạ độ, 2 đồ thị d-t, đường tròn P-Q-R-S, đồ thị
v-t hình thang) → đường dự phòng `build_bundle.py --grade 10` + `/quan-tri/nhap-bai`, dùng
**Browser pane có sẵn** (`mcp__Claude_Browser__*`, không phải claude-in-chrome — trang này đã có
sẵn phiên admin đăng nhập, không bị vấn đề "không share login" ghi ở lần chạy 2026-09-09).
Thao tác bằng `javascript_tool` (`.click()` native + native setter cho textarea) ăn đúng React
state, không cần `form_input`.

**Bug mới phát hiện — đề bị tự gắn thêm vào Luyện tập dù chỉ tick Kiểm tra:** sau khi bấm "Đăng
bài học", log báo cả `kiem_tra: đã cập nhật (gắn đề 23)` LẪN `luyen_tap: đã thêm (gắn đề 23)` —
trang tự tạo mới một `lesson_items` dòng `luyen_tap` và gắn cùng đề, dù tôi chỉ bấm checkbox
"Gắn vào Kiểm tra" (không đụng tới "Gắn vào Luyện tập"). Rủi ro thật: Luyện tập cho xem đáp án
ngay, lộ đề trước khi học sinh làm bài Kiểm tra thật. Nghi do commit `5ee6a43c` (refactor
nhap-bai dùng chung UI với trang Đăng đề, làm cùng ngày bởi một phiên khác đang chạy song song —
xem [[project_thachlab_concurrent_sessions]]) đổi default-checked của checkbox Luyện tập.
**Cách sửa (không xoá đề khỏi kho):** `/quan-tri/bai-hoc` → chọn Lớp/Chương → Soạn bài → Soạn mục
→ Sửa mục Luyện tập → bấm "Bỏ chọn" đề đó trong khung "Đề đã chọn" → Lưu mục.
**How to apply — bắt buộc cho lần chạy sau:** ngay sau khi bấm Đăng bài học, luôn
`curl .../rest/v1/lesson_items?select=*&lesson_id=eq.<id>` bằng anon-key để soát `exam_ids` của
TỪNG mục (kiem_tra, luyen_tap, bai_tap_ve_nha...) — đừng chỉ tin dòng log trên trang. Còn gắn vào
mục không xin thì gỡ theo cách trên.

Lesson 102 còn 1 mục `kiem_tra` tên rác "kiểm tra chương 1" (id 41, tạo 2026-09-16, trước đó
`exam_ids: [8]` trỏ tới đề đã bị xoá khỏi bảng `exams` — dữ liệu mồ côi từ lần test nào đó) và 1
mục `kiem_tra` rỗng tên "Kiểm tra" (id 31). Trang chọn mục 41 để gắn đề mới (không phải mục 31)
khi tick "Gắn vào Kiểm tra" + "Thay liên kết" — cơ chế chọn mục nào trong nhiều mục cùng `kind`
chưa rõ, cẩn thận nếu bài khác cũng có nhiều mục trùng loại.
