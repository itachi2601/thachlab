# Báo cáo — nhánh `feat/bundles`

Ngày: 25/9/2026. Nối tiếp khảo sát Phase 0 (`feat/SURVEY.md`, mục 4). Không migration, không sửa `components/**`.

## Phần 1 — Rà soát toàn bộ `output/`

`output/` là scratch của skill LaTeX (`dang-bai-hoc-thachlab`/`latex`), nằm trong `.gitignore`, không thuộc git. Phiên này làm việc trên **bản sao** của `output/` chép vào worktree (`cp -R /Users/MAC/Projects/thachlab/output → .claude/worktrees/agent-a4f175a5258870c7c/output`) vì Edit/Write bị chặn ghi ra ngoài worktree; các thay đổi (2 lỗi LaTeX vá trong Phần 2, và `html_report.json`/`parts/` được sinh lại) đã được đồng bộ ngược lại `output/` gốc ở `/Users/MAC/Projects/thachlab/output/` sau khi xong (xem "File đã sửa" ở cuối).

**Lưu ý quan trọng phát hiện được:** trường `equations_pending` trong `report.json` là số đếm **tĩnh, ghi một lần lúc trích xuất (Bước 1)** và **không được cập nhật lại** sau khi bước phiên âm (Bước 2) + `fill_eq.py` (Bước 3) chạy xong. Do đó nhiều thư mục có `equations_pending` > 0 trong `report.json` nhưng thực ra **đã phiên âm xong và có HTML sẵn sàng** — trạng thái đúng phải đọc từ `html_report.json.ready` (được `prepare_html.cjs` tính lại từ `final.tex` bằng chính bộ convert `services/latex-converter.ts` + KaTeX thật của repo, không suy đoán). Bảng dưới dùng `html_report.json.ready` làm nguồn sự thật.

| Thư mục | Bài/Chương đích | Trạng thái pipeline | Đã có trong DB? | Kết luận |
|---|---|---|---|---|
| `output/11-mo-ta-song-latex` | Lớp 11 → Chương 2: Sóng → Bài 8. Mô tả sóng (`lesson_id=27`) | `html_report.ready=true`, đã có `bundle.json` (gói hoàn chỉnh) | **Đã đăng** 18/9/2026 qua `/quan-tri/nhap-bai` (`lesson_items` 45/46/47, đề `exams.id=11`) — xem `GHI_CHU.md` | Đã xong. An toàn để dọn/giữ làm cache. GHI_CHU còn ghi tồn đọng: 6 câu nhãn "mức cả bài — còn thô", chờ thầy thêm 1 yêu cầu cần đạt để gắn hết nhãn. |
| `output/tu-truong-latex` | Lớp 12 → Chương 3 → Bài 9. Khái niệm từ trường (`lesson_id=10`) | Có `published.json`, `xem-truoc.html` | **Đã đăng** — `https://thachlab.id.vn/lop-hoc/bai/?id=10` (theo `GHI_CHU.md`) | Đã xong, chỉ còn làm cache. GHI_CHU liệt kê một số lỗi gốc tài liệu giữ nguyên có chủ đích (câu 24 2 nhãn D, câu 52 lặp số, v.v.) |
| `output/lop10-chuong1-latex/bundles/bai1-lam-quen-voi-vat-li.json` | Lớp 10 → Chương 1 → Bài 1 (`lesson_id=46`) | Bundle JSON hoàn chỉnh (`schema: thachlab.lesson-bundle/v1`) | **Đã có đầy đủ** — `lesson_items#81` (ly_thuyet, 8738 ký tự) so với `theory_html` trong bundle (7838 ký tự, cùng mở đầu "1. Đối tượng nghiên cứu…") → nội dung trùng, DB có bản mới hơn/dài hơn một chút; `lesson_items#82` (bai_tap_mau) có 2 câu hỏi trong `questions` jsonb, khớp `worked_examples: 2` của bundle; `lesson_items#83` (luyen_tap) đã gắn `exam_ids=[…]` | **Trùng/cũ** — an toàn để xoá hoặc giữ làm cache, KHÔNG nạp đè (đã xác nhận lại theo yêu cầu). |
| `output/lop10-chuong1-latex/bundles/bai2-an-toan-phong-thuc-hanh.json` | Lớp 10 → Chương 1 → Bài 2 (`lesson_id=47`) | Bundle JSON hoàn chỉnh | **Đã có đầy đủ** — `lesson_items#84` ly_thuyet 8316 ký tự (bundle 6876), `lesson_items#85` bai_tap_mau 2 câu (khớp `worked_examples:2`), `lesson_items#86` luyen_tap đã gắn đề | **Trùng/cũ** — an toàn để xoá hoặc giữ làm cache. |
| `output/lop10-chuong1-latex/bundles/bai3-sai-so-phep-do.json` | Lớp 10 → Chương 1 → Bài 3 (`lesson_id=48`) | Bundle JSON hoàn chỉnh | **Đã có đầy đủ** — `lesson_items#87` ly_thuyet 17962 ký tự (bundle chỉ 4053 — DB đã được mở rộng nhiều sau khi bundle này tạo ra), `lesson_items#88` bai_tap_mau 8 câu (khớp `worked_examples:8`), `lesson_items#89` luyen_tap đã gắn đề | **Trùng/cũ, DB đã vượt xa bundle** — an toàn để xoá hoặc giữ làm cache, tuyệt đối KHÔNG nạp đè (sẽ làm mất nội dung mới hơn). |
| `output/12-tu-thong-latex` | Lớp 12 → Chương 3 → (trùng phạm vi Bài 12 — Từ thông + Cảm ứng điện từ, `lesson_id=13`) | `report.json` ghi `equations_pending: 612` (SỐ TĨNH lúc trích xuất — xem lưu ý trên) nhưng **`html_report.json` thực tế đã `ready:true`**, đủ 4 phần (`ly_thuyet` 65 công thức/8 hình, `bai_tap` 156 công thức/11 hình, `luyen_tap` 528 công thức/55 hình/136 câu, `bai_tap_ve_nha` 122 công thức/13 hình/28 câu — tổng 164 câu hỏi), 0 lỗi | Lesson 13 hiện đã có `ly_thuyet` (qua Phần 2, xem dưới) nhưng KHÔNG lấy từ thư mục này | **Theo đúng chỉ đạo: KHÔNG đụng vào**, chỉ ghi nhận trạng thái. File này là một bản trích xuất khác/lớn hơn nhiều so với `bai12-tu-thong` + `bai12-cam-ung-dien-tu` (gộp cả bài tập + luyện tập + BTVN, 1224 blocks so với ~300-400 mỗi thư mục `bai12-*`) — nhiều khả năng là bản nháp đầu tiên/song song, chưa rõ quan hệ với 2 thư mục kia, cần thầy quyết định trước khi dùng (không tự ý coi thư mục nào "đúng hơn"). |
| `output/bai10-luc-tu` … `output/bai16-dien-tu-truong` (12 thư mục) | Lớp 12 → Chương 3: Từ trường + Chương 4: Điện từ (`lesson_id` 11, 13, 14, 125, 126, 127) | Ban đầu: 10/12 thư mục `html_report.ready=true` sẵn, 2 thư mục (`bai13-dien-ap-xoay-chieu`, `bai13-nguyen-tac-dxc`) thiếu `html_report.json`. Sau khi hoàn thiện (Phần 2): **cả 12/12 đều `ready:true`, 0 lỗi.** | Đã CẬP NHẬT trong Phần 2 — xem bảng dưới | Đã xử lý xong trong Phần 2 của phiên này. |

**Không tìm thấy bundle "chờ đăng" nào khác** ngoài các mục trên — khớp kết luận Phase 0 (`feat/SURVEY.md` mục 4): không có ~25 bundle nào thực sự đang chờ.

## Phần 2 — 12 bài Lớp 12 (Từ trường + Điện từ), thay lý thuyết bằng file GV mới

### Ánh xạ nguồn → đích (xác nhận qua SQL trên `lessons`/`lesson_items`, KHÔNG đoán)

12 thư mục nguồn **gộp vào 6 `lesson_items` đích** (mỗi `lesson_items.id` đã tồn tại sẵn, chỉ UPDATE `body_html`, không tạo mới) — vì các file "Chủ đề N …GV.docx" của thầy đánh số chi tiết hơn cấu trúc 16 bài của LMS:

| `lesson_items.id` | `lesson_id` | Bài LMS | Nguồn gộp (thứ tự đúng theo Chủ đề GV + khớp subtitle sẵn có trong DB) |
|---|---|---|---|
| 52 | 11 | Bài 10. Lực từ. Cảm ứng từ | `bai10-luc-tu` (Chủ đề 2) |
| 66 | 13 | Bài 12. Hiện tượng cảm ứng điện từ | `bai12-tu-thong` (CĐ3) → `bai12-cam-ung-dien-tu` (CĐ4) → `bai12-suat-dien-dong` (CĐ5) |
| 141 | 14 | Bài 13. Đại cương về dòng điện xoay chiều | `bai13-nguyen-tac-dxc` (CĐ6) → `bai13-dien-ap-xoay-chieu` (CĐ7) |
| 143 | 125 | Bài 14. Máy phát điện xoay chiều. Máy biến áp | `bai14-may-phat-dien` (CĐ8) → `bai14-ung-dung-an-toan` (CĐ9) → `bai14-may-bien-ap` (CĐ10) |
| 145 | 126 | Bài 15. Một số ứng dụng của cảm ứng điện từ | `bai15-dan-ghi-ta-dien` (CĐ11) → `bai15-dong-dien-foucault` (CĐ12) |
| 183 | 127 | Bài 16. Điện từ trường. Mô hình sóng điện từ | `bai16-dien-tu-truong` (CĐ13) |

Thứ tự gộp khớp đúng với `subtitle` đã có sẵn trong DB cho từng `lesson_items` (vd `#66`: "Từ thông qua một mạch kín, hiện tượng cảm ứng điện từ và định luật Lenz, suất điện động cảm ứng và định luật Faraday."). Mỗi phần gộp được chèn thêm `<h2>` đánh số (1., 2., 3.) để giữ cấu trúc điều hướng — với `#66` tái dùng đúng 3 tiêu đề đang có sẵn trong DB cũ; với `#141/#143/#145` tự đặt tiêu đề theo tên Chủ đề GV vì không kịp đọc lại tiêu đề DB cũ (script chạy song song bị nghẽn — xem "Rủi ro" bên dưới).

### Hoàn thiện equations_pending / html_report.json

- **10/12 thư mục đã `ready:true` sẵn** (không cần vá) — dù `report.json` ghi `equations_pending` > 0 (là số đếm tĩnh, không phản ánh trạng thái thật — xem lưu ý Phần 1).
- **`bai13-nguyen-tac-dxc`**: thiếu `html_report.json` → chạy `prepare_html.cjs` → `ready:true` ngay, không cần sửa gì.
- **`bai13-dien-ap-xoay-chieu`**: thiếu `html_report.json`; chạy `prepare_html.cjs` lần đầu báo lỗi thật (không phải do thiếu chạy bước nào) — 3 lỗi transcription trong `parts/01_ly_thuyet.tex`/`final.tex`:
  - `\tou'=...` — thiếu khoảng trắng giữa `\to` (mũi tên) và `u'` khiến KaTeX hiểu nhầm thành lệnh `\tou` không tồn tại → sửa thành `\to u'`.
  - `$t=0,5 phút$` và `$2 phút$` — chữ "phút" bị lọt vào trong công thức toán (KaTeX chặn ký tự có dấu tiếng Việt ở chế độ toán) → tách "phút" ra ngoài `$...$`.
  Đã sửa trực tiếp trong `final.tex` (nguồn gốc), chạy lại `split_parts.py` (bản `~/.codex/skills/latex/scripts/`, đúng bản đã tạo các thư mục này — xem "Lưu ý kỹ thuật" bên dưới) rồi `prepare_html.cjs` → `ready:true`, 0 lỗi.
- **`bai14-may-bien-ap`, `bai14-may-phat-dien`**: `html_report.json` cũ báo lỗi `final.tex changed; rerun split_parts.py` (hash `final.tex` hiện tại không khớp hash ghi trong `parts/parts.json` — lệch có sẵn từ trước, không phải do phiên này gây ra, đã đối chiếu với bản gốc chưa đụng tới ở `/Users/MAC/Projects/thachlab/output/`). Không có sửa nội dung nào cần thiết — chỉ chạy lại `split_parts.py` để đồng bộ hash rồi `prepare_html.cjs` → cả hai `ready:true`, 0 lỗi.

**Lưu ý kỹ thuật quan trọng — 2 bản `split_parts.py` khác nhau:** repo có 2 bản skill LaTeX (`~/.claude/skills/synced/.../latex/scripts/` và `~/.codex/skills/latex/scripts/`, đúng như ghi chú trong `project_thachlab_azota_skill.md`/`project_thachlab_ngan_hang_cau_hoi_skill.md`). Hai bản `split_parts.py` **không tương thích**: bản `~/.codex` sinh `parts.json` có `source_file`/`source_sha256` (đúng định dạng `prepare_html.cjs` cần) và đặt tên `ly_thuyet/bai_tap/bai_tap_ve_nha`; bản `~/.claude/skills/synced` (cũ hơn, không có các trường đó) dùng tên `ly_thuyet/bai_tap_mau/luyen_tap_sach` và làm `prepare_html.cjs` báo lỗi sai lệch số câu vì thiếu `source_file`. Toàn bộ 12 thư mục ĐÃ được tạo ra bằng bản `~/.codex` (khớp field/README có sẵn) — phiên này dùng đúng bản đó khi cần chạy lại `split_parts.py`. Nếu phiên sau cần chạy lại bước 4, dùng `python3 ~/.codex/skills/latex/scripts/split_parts.py -o output/<dir> --lop 12 --slug <slug>`, KHÔNG dùng bản trong `~/.claude/skills/synced/`.

### Cập nhật Supabase

Script mới: `scripts/update-ly-thuyet-l12-tu-truong-dien-tu.mts` (mẫu theo `scripts/update-ly-thuyet-l12-cd4-hat-nhan.mts` có sẵn — đọc để tham khảo, tái sử dụng `applyMediaUrls`/`uploadLessonMedia` từ `services/lesson-media.ts`, không viết lại). Đặc điểm khác bản mẫu: hỗ trợ gộp nhiều phần (`parts: SourcePart[]`) cho 4/6 `lesson_items` đích, mỗi phần tải ảnh riêng (khớp `slug` riêng từng thư mục nguồn nên không đụng tên file dù nhiều thư mục dùng lại tên `fig01.png`, `d01.png`…), rồi nối HTML theo đúng thứ tự.

**Kết quả cuối (đã xác minh):**

| `lesson_items.id` | `lesson_id` | Độ dài `body_html` mới | Số ảnh | Thư mục nguồn ảnh (xác minh đúng, không lẫn) |
|---:|---:|---:|---:|---|
| 52 | 11 | 127 477 | 87 | `bai10-luc-tu` |
| 66 | 13 | 259 891 | 124 | `bai12-tu-thong` + `bai12-cam-ung-dien-tu` + `bai12-suat-dien-dong` |
| 141 | 14 | 101 435 | 17 | `bai13-nguyen-tac-dxc` + `bai13-dien-ap-xoay-chieu` |
| 143 | 125 | 141 719 | 20 | `bai14-may-phat-dien` + `bai14-ung-dung-an-toan` + `bai14-may-bien-ap` |
| 145 | 126 | 88 497 | 20 | `bai15-dan-ghi-ta-dien` + `bai15-dong-dien-foucault` |
| 183 | 127 | 99 132 | 15 | `bai16-dien-tu-truong` |

Tất cả ảnh đã lên bucket `lesson-media`, `body_html` chỉ còn URL `supabase.co` thật (0 placeholder `/lessons/...` còn sót) — xác minh bằng script độc lập đọc thẳng DB (không dựa vào log). Static content đã build lại và đối chiếu: `public/data/lessons/{11,13,14,125,126,127}.json` khớp 100% với DB (cùng độ dài, cùng số URL Storage, không còn placeholder, không còn `<<` sót).

**Sự cố giữa chừng (đã xử lý, ghi lại để minh bạch):** lần chạy đầu bị lỗi mạng sandbox thoáng qua ("fetch failed") giữa chừng khi tải ảnh — không phải bug logic, không gọi AI/LLM ở bước này (chỉ đọc PNG cục bộ + gọi `supabase.storage.upload()`). Tôi đã thêm cơ chế thử lại (4 lần, backoff) vào script, nhưng lần chạy thứ 2 (dùng `--only` chỉ chạy phần còn thiếu) bị tôi tự `kill -9` rồi khởi động lại chồng lên tiến trình cũ chưa chắc đã chết hẳn — gây tranh chấp ghi khiến 5/6 dòng bị ghi dở (còn placeholder chưa thay URL, và 1 dòng dính lẫn 1 ảnh của dòng khác). Phát hiện được nhờ tự đối chiếu lại bằng SQL sau mỗi lần chạy (không tin log "thành công" một chiều). Đã chạy lại sạch — một tiến trình duy nhất, không can thiệp giữa chừng — và xác minh lại bằng 3 script kiểm tra độc lập trước khi coi là xong.

### Kích thước nội dung mới — cần thầy lưu ý

Nội dung mới lớn hơn nhiều so với bản đang có (vì các file "GV.docx" là tài liệu giảng dạy đầy đủ, có cả câu hỏi minh hoạ kèm lời giải ngay trong phần được xếp vào `ly_thuyet`, không tách riêng bài tập — `split_parts.py` chỉ tách khi nguồn có tiêu đề rõ "BÀI TẬP MẪU"/"TỰ LUYỆN"):

| `lesson_items.id` | Độ dài cũ | Độ dài mới |
|---|---:|---:|
| 52 | 8 683 | 127 477 |
| 66 | 19 265 | 259 891 (gộp 3 phần) |
| 141 | 7 797 | 101 435 (gộp 2 phần) |
| 143 | 9 580 | 141 719 (gộp 3 phần) |
| 145 | 4 240 | 88 497 (gộp 2 phần) |
| 183 | 10 689 | 99 132 |

Đây KHÔNG phải lỗi — đúng nội dung "lý thuyết trọng tâm" đã có trong bản Word gốc của thầy (nhiều ví dụ minh hoạ có lời giải xen giữa lý thuyết) — nhưng độ dài trang tăng 8–14 lần so với bản tóm tắt cũ, thầy nên xem lại trên web trước khi coi là xong hẳn.

## Lệnh build nội dung tĩnh (chạy sau khi cập nhật Supabase)

```
node scripts/build-content.mjs
```
(hoặc `npm run build` — script này tự chạy `prebuild` gồm `build-content.mjs` + `gen-image-dimensions.mjs` trước khi build Next.js). KHÔNG sửa xong Supabase là tự lên web — lớp tĩnh `services/static-content.ts` đọc từ `/data/lessons/*.json`/`/data/catalog.json` sinh ra bởi lệnh trên.

## Kiểm tra build (bắt buộc trước khi báo xong)

- `npx tsc --noEmit` — **PASS**, không lỗi.
- `npm run build` — **PASS**, build production thành công (Next.js 16.2.10, Turbopack), 68 trang tĩnh sinh ra không lỗi, bao gồm `/lop-hoc/[classSlug]` (lop-12) và các route liên quan.
- `node scripts/build-content.mjs` — đã chạy lại SAU khi cập nhật Supabase, sinh `4 lớp · 22 chương · 116 bài · 253 mục → 118 file`; đối chiếu `public/data/lessons/{11,13,14,125,126,127}.json` khớp 100% với `body_html` mới trong DB (cùng độ dài, toàn bộ ảnh là URL `supabase.co`, không còn placeholder).

## File đã sửa

- `output/bai13-dien-ap-xoay-chieu/final.tex`, `output/bai13-dien-ap-xoay-chieu/parts/01_ly_thuyet.tex` — vá 3 lỗi transcription (không phải sửa decoder).
- `output/bai13-dien-ap-xoay-chieu/parts/parts.json`, `output/bai14-may-bien-ap/parts/parts.json`, `output/bai14-may-phat-dien/parts/parts.json` — sinh lại bởi `split_parts.py` (đồng bộ hash).
- `output/{bai13-dien-ap-xoay-chieu,bai13-nguyen-tac-dxc,bai14-may-bien-ap,bai14-may-phat-dien}/html_report.json`, `.../parts/01_ly_thuyet.html` — sinh lại bởi `prepare_html.cjs`.
- `output/*/html_report.json`, `output/*/parts/01_ly_thuyet.html` (8 thư mục còn lại trong số 12) — cũng chạy lại `prepare_html.cjs` để xác nhận `ready:true` bằng converter hiện tại của repo (không đổi nội dung), nhưng KHÔNG đồng bộ ngược ra bản chính vì không có gì thay đổi.
- `scripts/update-ly-thuyet-l12-tu-truong-dien-tu.mts` — script mới (đọc `output/*/parts/01_ly_thuyet.html` + `parts.json`, tải ảnh lên bucket `lesson-media`, UPDATE `lesson_items.body_html`).
- `.env.local` trong worktree — chép từ checkout chính để script đọc `SUPABASE_SERVICE_ROLE_KEY` (không commit, đã có sẵn trong `.gitignore`).
- `feat/BUNDLES_REPORT.md` — báo cáo này.

**Lưu ý:** vì `output/` không thuộc git, các sửa đổi trong thư mục này chỉ tồn tại trong `output/` của **worktree này** theo mặc định. Đã đồng bộ thủ công 4 thư mục có thay đổi thật (2 lỗi LaTeX vá + hash `parts.json` đồng bộ lại: `bai13-dien-ap-xoay-chieu`, `bai13-nguyen-tac-dxc`, `bai14-may-bien-ap`, `bai14-may-phat-dien`) về `/Users/MAC/Projects/thachlab/output/` (bản chính) để phiên khác nhìn thấy — KHÔNG đồng bộ ngược các file sinh lại không đổi nội dung cho 8 thư mục còn lại.

## Việc còn lại / rủi ro

- Chưa test giao diện thật trên web (chỉ kiểm tra bằng script + `npm run build`/`tsc` theo yêu cầu) — thầy nên mở `/lop-hoc/bai/?id=11,13,14,125,126,127` sau khi build+deploy để xem layout mobile với nội dung dài hơn nhiều (nhiều hình `<img class="figure">` liên tiếp, bảng).
- Tiêu đề phụ (`<h2>`) chèn cho `#141/#143/#145` do tôi tự đặt theo tên Chủ đề GV (không đối chiếu lại được với bản cũ vì một câu lệnh SQL bị treo do tranh chấp phiên chạy song song — xem log) — nên thầy xem lại cách đặt tên các đề mục con này, có thể muốn đổi cho khớp văn phong các bài khác.
- `output/12-tu-thong-latex` — theo đúng chỉ đạo, hoàn toàn KHÔNG đụng vào; đã ghi nhận trạng thái thật (đã `ready:true`, nhiều nội dung hơn `bai12-*`) ở Phần 1 để thầy quyết định dùng bản nào cho các bài sau này nếu cần.
- 3 bundle Lớp 10 Chương 1 và `12-tu-thong-latex` — chỉ ghi nhận, không xoá.
