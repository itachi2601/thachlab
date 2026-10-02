---
name: soan-bai-ly-thuyet-tuong-tac
description: Soạn một bài LÝ THUYẾT có tương tác cho thachlab theo cách dạy của thầy Thạch, dùng để thầy chiếu giảng trực tiếp và học sinh tự học lại — mở bằng ví dụ đời thường và câu dự đoán; mỗi kiến thức kèm ví dụ/thí nghiệm; có mục "Trả bài" lý thuyết/công thức trước bài tập; bài toán mẫu đọc đề từng câu (dữ liệu và kiến thức liên quan); trắc nghiệm tự chấm ngay trong bài; hình SVG tự vẽ — rồi ghi thí nghiệm vào kho dữ liệu cho giai đoạn mô phỏng và đóng gói theory.html + bundle.json. Dùng khi thầy nói "soạn bài lý thuyết tương tác", "tạo bài lý thuyết có ví dụ thực tế", "làm bài học mới cho chương X", "vẽ hình cho bài lý thuyết", "ghi thí nghiệm của bài". Khác dang-bai-hoc-thachlab (đăng .tex có sẵn) và soan-quiz-ly-thuyet (bộ 20 câu Kiểm tra nhanh cuối bài). Soạn, vẽ, kiểm chạy được trên cloud; ĐĂNG lên DB phải chạy trên Mac.
---

# Soạn bài lý thuyết tương tác

## Mục đích (thầy xác nhận 1/10/2026)

Không phải video bài giảng. Đây là **bài đọc lý thuyết có tương tác**, dùng được cả hai cách: (1) thầy **chiếu và giảng trực tiếp** trên lớp, mỗi lần bấm `<details>`/chọn đáp án là một nhịp giảng; (2) học sinh **tự xem lại** ở nhà, nên mọi lời giảng quan trọng phải nằm trong bài chứ không chỉ trong lời thầy nói.

Ba thói quen dạy của thầy, bài nào cũng phải có đủ:
1. **Mỗi kiến thức cần nhớ đi kèm một ví dụ hoặc thí nghiệm thực tế.** Không có gạch đầu dòng kiến thức nào đứng trơ. Thí nghiệm viết theo ba bước Làm – Quan sát – Rút ra (`.tl-box--exp`); ví dụ ngắn thì viết ngay trong gạch đầu dòng.
2. **Trả bài trước khi giải bài tập.** Một mục `<h3>` "Trả bài" gồm 4–6 câu hỏi nhớ lại (phát biểu, công thức + ký hiệu, đặc điểm, điểm dễ nhầm, công thức suy ra từ đâu), mỗi câu một `<details>` để học sinh tự đọc to rồi mới bấm xem đáp án. Mục này đứng **trước** bài toán mẫu.
3. **Bài toán mẫu: đọc đề đến đâu, nêu dữ liệu và kiến thức đến đó.** Chép đề trong hộp "Đề bài", rồi bảng ba cột **Câu trong đề | Dữ liệu | Kiến thức liên quan** (`.tl-table--data`), mỗi hàng một câu/cụm của đề. Sau bảng mới đến lời giải (ẩn trong `<details>`, các bước đánh số bằng `.tl-steps`), cuối cùng bước kiểm tra kết quả.

Bài mẫu chuẩn (đọc để bắt chước nhịp): `assets/mau-bai-dl3-newton/` trong skill, bản đầy đủ ở `content/lesson-samples/l10-dinh-luat-3-newton/` của repo.
Trạng thái: **mẫu đầu tiên chưa được thầy xem trên web** — mọi quy ước dưới đây rút từ lần làm đó, sẽ chỉnh khi thầy phản hồi (xem mục cuối).

## Đóng gói và phụ thuộc

- Skill sống trong repo `thachlab` tại `.claude/skills/soan-bai-ly-thuyet-tuong-tac/` và có file cài đặt `dist-skills/soan-bai-ly-thuyet-tuong-tac.skill` (zip, mở bằng skill-creator hoặc kéo vào Library). Đồng bộ ra Library plugin + `~/.codex` trên Mac: `bash scripts/sync-skill.sh soan-bai-ly-thuyet-tuong-tac`.
- Đi kèm: `assets/tl-components.css` (bản sao CSS linh kiện `.tl-*`; bản chuẩn ở cuối `app/globals.css`), `assets/mau-bai-dl3-newton/` (bài mẫu đầy đủ + 2 mục dữ liệu thí nghiệm), `references/`, `scripts/`.
- Cần chạy từ **gốc repo thachlab**: `validate_bundle.mts` import `services/lesson-import.ts`; `thi_nghiem.py` ghi vào `content/thi-nghiem/`; `preview.mjs` cần `node_modules/katex` và Chromium (`/opt/pw-browsers`). Ngoài repo chỉ đọc được SKILL.md, references, assets và `svg_lib.py`/`lint_theory.py`.
- Đăng DB không làm được trên cloud (Supabase bị chặn): luôn dừng ở `bundle.json` rồi đưa lệnh cho thầy chạy trên Mac.

## Quy trình

1. **Chọn bài + nguồn.** Lớp → Chương → Bài (xem `public/data/catalog.json`). Nội dung lấy từ chương trình/SGK làm ý tưởng và số liệu; **không chép nguyên văn, không dùng ảnh của sách có bản quyền** (Halliday, SGK...) trên trang công khai — vẽ lại bằng SVG.
2. **Phiếu bài** (trong đầu/scratchpad): 1 ví dụ đời thường mở bài · khái niệm/định luật + phát biểu chuẩn · công thức + ký hiệu + đơn vị · 1–2 **hiểu lầm kinh điển** của học sinh · 1 ví dụ số · 3–4 ứng dụng đời sống. Hiểu lầm kinh điển là xương sống của bài — chọn đúng chỗ học sinh hay sai.
3. **Viết `theory.html`** theo dàn ý dưới + linh kiện trong `references/linh-kien-html.md`.
4. **Vẽ hình** 2–4 hình SVG theo `references/hinh-svg.md`, dùng `scripts/svg_lib.py` (sinh bằng script, chèn idempotent như `build_figs.py` của bài mẫu).
4b. **Ghi thí nghiệm vào kho dữ liệu** `content/thi-nghiem/` (một file JSON cho mỗi thí nghiệm hoặc ví dụ: dụng cụ, các bước, tham số + khoảng giá trị, phương trình, số liệu mẫu, hiểu lầm hay gặp, gợi ý mô phỏng). Đây là dữ liệu nguồn cho giai đoạn **làm mô phỏng** tiếp theo, nên không để thí nghiệm chỉ nằm trong HTML. Gắn `data-exp="<id>"` lên hộp `.tl-box--exp` / `<figure>` tương ứng. Quy ước đầy đủ: `content/thi-nghiem/README.md`.
5. **Kiểm.** `python3 .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/lint_theory.py <theory.html>` (lỗi cấu trúc) → `python3 .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/thi_nghiem.py <theory.html>` (kiểm kho thí nghiệm + liên kết `data-exp`, sinh `index.json`) → `node .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/preview.mjs <theory.html> <thư-mục-ra>` (chụp 375px từng hình + tự bấm mọi đáp án kiểm phản hồi). **Phải xem ảnh bằng mắt** — nhãn chồng chữ/cắt biên không script nào bắt được.
6. **Đóng gói `bundle.json`** (schema `thachlab.lesson-bundle/v1`): `theory_html` + `worked_examples: []` + `exam` gồm các câu tự kiểm tra trong bài (validate bắt buộc ≥1 câu). Kiểm: `npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts <bundle.json>` (dùng đúng `validateBundle` của trang nhập bài). Phải `ok: true`.
7. **Báo thầy** (ngắn): bài gì, hình nào ở đâu, đã kiểm gì. Nhắc lệnh trên Mac, **mặc định chỉ đẩy phần lý thuyết** (không đụng đề, bài tập mẫu, tiêu đề, tiến độ học):
   ```
   cd /Users/MAC/Projects/thachlab && git pull origin main
   bash scripts/cap-nhat-ly-thuyet.sh content/lesson-samples/<thư-mục-bài>/theory.html <lesson_id>
   bash scripts/deploy.sh      # chỉ khi CSS .tl-* chưa có trên production
   ```
   Script tự: lint → dry-run + sao lưu `body_html` cũ ra `scripts/logs/` → hỏi xác nhận → chỉ ghi cột `body_html` của mục `ly_thuyet`. Hoàn tác: `npx tsx scripts/khoi-phuc-ly-thuyet.mts <file sao lưu>`. Chỉ dùng `upload-lesson.mts` (tạo cả đề Luyện tập) khi thầy nói rõ muốn đăng cả đề. Commit chỉ đúng thư mục bài + file đã đụng; không tự đăng DB.
   **Lưu ý HTML:** trong `$…$` viết `\lt`, `\gt` thay cho `<`, `>` (ký tự `<k` bị HTML hiểu là thẻ và làm hỏng công thức).

## Dàn ý bài (nhịp 5 phần, mỗi phần là một `<h3>` đánh số I., II.…)

Dùng `<h3>` làm mốc — `wrapTheorySections` cắt đoạn theo `<h3>` để nút "Ôn ngay" của quiz cuộn đúng chỗ. Không dùng `<h2>` "LÝ THUYẾT" ngoài `<h3>`.

| Phần | Nội dung | Linh kiện |
|---|---|---|
| I. Mở bài | Tình huống đời thường gần học sinh (sân băng, xưởng CNC, xe đạp, bếp...), kể bằng giọng thầy, kết bằng câu hỏi "tại sao?" | hộp **dự đoán** (radio) |
| II. Kiến thức | Phát biểu + công thức + ký hiệu; mỗi ý có **ví dụ**; ít nhất một **thí nghiệm** Làm–Quan sát–Rút ra | hộp **định nghĩa** + hình + `.tl-box--exp` + `<details>` "xem thêm" |
| III. Bẫy | Hiểu lầm kinh điển, vì sao sai; bảng so sánh đúng/sai | bảng + hình + **tự kiểm tra** |
| IV. Trả bài | 4–6 câu nhớ lại lý thuyết/công thức, chưa giải bài | `<details>` trong hộp `tl-box--think` |
| V. Bài toán mẫu | Đề bài → bảng *Câu trong đề / Dữ liệu / Kiến thức liên quan* → lời giải từng bước → kiểm tra kết quả; sau đó 1–2 câu "Thử sức" đổi số | `.tl-table--data` + `.tl-steps` + hình + quiz |
| VI. Đời sống + tổng kết | 3–4 ứng dụng; 1 thử thách ẩn gợi ý; khung "Mang về sau bài học" 3–4 ý (có ý về cách đọc đề) | `<details>` + hộp định nghĩa |

## Giọng văn thầy Thạch

- Xưng "thầy", gọi "em/các em". Câu ngắn. Mở bằng cảnh thật, **không** mở bằng định nghĩa.
- Có người thật nói câu thật ("Thầy ơi, em đẩy thành chứ có đẩy mình đâu…"). Mẹo nhớ có tên (4 chữ, 1 câu hỏi kiểm tra "đặt lên mấy vật?").
- Sai thì **giải thích vì sao sai** và gợi cách nghĩ lại, không chỉ báo "sai". Đúng thì củng cố lý do.
- Thầy dạy vật lí THPT + CNC/chế tạo máy + trượt băng: ưu tiên ví dụ từ ba mảng đó. Trả lời chung gọn, vào thẳng kết quả.

## Bài học rút ra từ bài mẫu (đừng lặp lại lỗi)

1. **HTML trong DB cấm `<script>`, `<style>`, `on*=`** (`checkTags` trong `services/lesson-import.ts` chặn). Tương tác chỉ bằng `<details>` và radio + CSS `:checked`. CSS nằm ở `app/globals.css` (khối `.tl-*`) — sửa linh kiện = sửa CSS + deploy.
2. **Cấu trúc `.tl-quiz` rất nhạy:** `<input>` ngay trước `<label>` của nó, tất cả + các `.tl-fb` là **anh em trực tiếp** trong cùng `.tl-quiz`. Mỗi câu một `name`; `id` duy nhất toàn trang → đặt tiền tố theo bài (`tl3-q1a`: bài 3, câu 1, đáp án a). Bọc thêm `<div>` giữa chừng là hỏng phản hồi.
3. **Mỗi đáp án sai phải sai chắc chắn.** Bài mẫu suýt có hai đáp án đúng (sách ép bàn/bàn đỡ sách cũng là cặp lực–phản lực). Với mỗi câu: tự trả lời lại từng phương án một, và nhờ subagent kiểm chéo nếu câu khó.
4. **Đáp án đúng cho nhãn `tl-ok`, sai cho `tl-no`** — hiện phản hồi theo `:has()`. Chỉ màu hiện khi đã chọn nên không lộ đáp án trước.
5. **`ContentHtml` xử lý chuỗi:** `<p>` mở đầu bằng "- "/"•" bị đổi thành gạch đầu dòng; chuỗi "...." (≥4 chấm) bị xoá; `<table>` tự bọc `.table-scroll`; `$…$`/`$$…$$` là công thức KaTeX (không dùng `$` cho tiền); số dấu `$` phải chẵn. KaTeX chạy sau khi tải xong → `<details>` đã mở có thể đóng lại đúng lúc render đầu (chấp nhận được).
6. **Hình SVG tự vẽ, không ảnh raster** (quy tắc tốc độ trong `AGENTS.md`): vài KB, không request thêm, nét theo `currentColor` nên tối/sáng đều đọc. Nếu thật sự cần ảnh: `.webp` ≤1200px, ≤150 KB, qua Storage — không base64 trong HTML.
7. **Bundle bắt buộc có `exam` ≥1 câu**; dùng chính các câu tự kiểm tra trong bài làm đề Luyện tập nhỏ (3–5 câu, kèm `explanation`).
8. **Kiểm bằng mắt ở 375px** (thầy học sinh dùng điện thoại): bài mẫu bị cắt nhãn "Thành sân" và chồng chữ "mặt băng"/"em trượt lùi" cho tới khi chụp ảnh mới thấy.
9. **Chưa test trong app thật** (Next.js tĩnh): preview chỉ dùng CSS + KaTeX rời. Khi có trình duyệt xem được `/lop-hoc/bai`, kiểm lại bài đăng thật trước khi nhân rộng.

## Cần kiểm tra khi thầy xem được bài mẫu (điền tiếp)

- [ ] Radio tự chấm hiện đúng trong app thật (không bị React/`ContentHtml` render lại làm mất chọn)?
- [ ] `<details>` mở/đóng ổn trên điện thoại?
- [ ] Độ dài bài (≈20 KB, 5 phần) có vừa ý; mật độ tương tác có quá nhiều/ít?
- [ ] Hình SVG: kiểu que có chấp nhận được hay cần vẽ đẹp hơn?
- [ ] Giọng văn: chỗ nào chưa giống thầy?
