---
name: soan-bai-ly-thuyet-tuong-tac
description: Soạn một bài LÝ THUYẾT có tương tác cho thachlab theo phong cách chốt 2/10/2026 của thầy Thạch, dùng để chiếu giảng trực tiếp và học sinh tự học lại — mục tiêu đầu bài, mở bằng tình huống đời thường, câu dự đoán trước khi học (先猜后学), từ khoá 3–6 chữ cho mỗi kiến thức, mỗi kiến thức kèm ví dụ/thí nghiệm Làm–Quan sát–Rút ra, bắt các "cái bẫy" của bài (易错点), trắc nghiệm tự chấm ngay có phân tích lỗi sai, mục "Trả bài" trước bài tập, bài toán mẫu đọc đề từng câu, luyện biến thể (变式) và thử thách phân tầng ⭐–⭐⭐⭐; KHÔNG dùng vai "thầy" trong bài; hình SVG tự vẽ; ghi thí nghiệm vào kho dữ liệu cho giai đoạn mô phỏng; đóng gói theory.html + bundle.json + bản xem thử (Chrome headless). Dùng khi thầy nói "soạn bài lý thuyết tương tác", "tạo bài lý thuyết có ví dụ thực tế", "làm bài học mới cho chương X", "vẽ hình cho bài lý thuyết", "ghi thí nghiệm của bài", "soạn theo phong cách bài Mô tả sóng". Khác dang-bai-hoc-thachlab (đăng .tex có sẵn) và soan-quiz-ly-thuyet (bộ 20 câu Kiểm tra nhanh cuối bài). Soạn, vẽ, kiểm chạy được trên cloud; ĐĂNG lên DB phải chạy trên Mac.
---

# Soạn bài lý thuyết tương tác

## Mục đích (thầy xác nhận 1/10/2026)

Không phải video bài giảng. Đây là **bài đọc lý thuyết có tương tác**, dùng được cả hai cách: (1) thầy **chiếu và giảng trực tiếp** trên lớp, mỗi lần bấm `<details>`/chọn đáp án là một nhịp giảng; (2) học sinh **tự xem lại** ở nhà, nên mọi lời giảng quan trọng phải nằm trong bài chứ không chỉ trong lời thầy nói.

Ba thói quen dạy của thầy, bài nào cũng phải có đủ:
1. **Mỗi kiến thức cần nhớ đi kèm một ví dụ hoặc thí nghiệm thực tế.** Không có gạch đầu dòng kiến thức nào đứng trơ. Thí nghiệm viết theo ba bước Làm – Quan sát – Rút ra (`.tl-box--exp`); ví dụ ngắn thì viết ngay trong gạch đầu dòng.
2. **Trả bài trước khi giải bài tập.** Một mục `<h3>` "Trả bài" gồm 4–6 câu hỏi nhớ lại (phát biểu, công thức + ký hiệu, đặc điểm, điểm dễ nhầm, công thức suy ra từ đâu), mỗi câu một `<details>` để học sinh tự đọc to rồi mới bấm xem đáp án. Mục này đứng **trước** bài toán mẫu.
3. **Bài toán mẫu: đọc đề đến đâu, nêu dữ liệu và kiến thức đến đó.** Chép đề trong hộp "Đề bài", rồi bảng ba cột **Câu trong đề | Dữ liệu | Kiến thức liên quan** (`.tl-table--data`), mỗi hàng một câu/cụm của đề. Sau bảng mới đến lời giải (ẩn trong `<details>`, các bước đánh số bằng `.tl-steps`), cuối cùng bước kiểm tra kết quả.

Bài mẫu chuẩn (đọc để bắt chước nhịp): `assets/mau-bai-dl3-newton/` trong skill, bản đầy đủ ở `content/lesson-samples/l10-dinh-luat-3-newton/` của repo.
Bài mẫu thứ hai — **mới nhất, có đủ bộ công cụ xem thử**: `content/lesson-samples/l11-mo-ta-song/` (Bài 8 Mô tả sóng, lớp 11)
và `content/lesson-samples/l11-giao-thoa-song/` (Bài 12 Giao thoa sóng, đã đăng).
Trạng thái: **mẫu đầu tiên chưa được thầy xem trên web** — mọi quy ước dưới đây rút từ lần làm đó, sẽ chỉnh khi thầy phản hồi (xem mục cuối).

## Đóng gói và phụ thuộc

- Skill sống trong repo `thachlab` tại `.claude/skills/soan-bai-ly-thuyet-tuong-tac/` và có file cài đặt `dist-skills/soan-bai-ly-thuyet-tuong-tac.skill` (zip, mở bằng skill-creator hoặc kéo vào Library). Đồng bộ ra Library plugin + `~/.codex` trên Mac: `bash scripts/sync-skill.sh soan-bai-ly-thuyet-tuong-tac`.
- Đi kèm: `assets/tl-components.css` (bản sao CSS linh kiện `.tl-*`; bản chuẩn ở cuối `app/globals.css`), `assets/mau-bai-dl3-newton/` (bài mẫu đầy đủ + 2 mục dữ liệu thí nghiệm), `references/`, `scripts/`.
- Cần chạy từ **gốc repo thachlab**: `validate_bundle.mts` import `services/lesson-import.ts`; `thi_nghiem.py` ghi vào `content/thi-nghiem/`; `preview.mjs` cần `node_modules/katex` và Chromium (`/opt/pw-browsers`). Ngoài repo chỉ đọc được SKILL.md, references, assets và `svg_lib.py`/`lint_theory.py`.
- Đăng DB không làm được trên cloud (Supabase bị chặn): luôn dừng ở `bundle.json` rồi đưa lệnh cho thầy chạy trên Mac.

## Quy trình

1. **Chọn bài + nguồn.** Lớp → Chương → Bài (xem `public/data/catalog.json`). **Soạn lại bài đã đăng thì đọc trước bài đang có trên web (`lesson_items` mục `ly_thuyet`) và mô tả bài/YCCĐ của nó**, liệt kê các ý bắt buộc để bản mới không bỏ sót (bài Mô tả sóng cũ thiếu hẳn phương trình sóng và trễ pha dù mô tả bài có ghi). Nội dung lấy từ chương trình/SGK làm ý tưởng và số liệu; **không chép nguyên văn, không dùng ảnh của sách có bản quyền** (Halliday, SGK...) trên trang công khai — vẽ lại bằng SVG.
2. **Phiếu bài** (trong đầu/scratchpad): 1 ví dụ đời thường mở bài · khái niệm/định luật + phát biểu chuẩn · công thức + ký hiệu + đơn vị · 1–2 **hiểu lầm kinh điển** của học sinh · 1 ví dụ số · 3–4 ứng dụng đời sống. Hiểu lầm kinh điển là xương sống của bài — chọn đúng chỗ học sinh hay sai.
3. **Viết `theory.html`** theo dàn ý dưới + linh kiện trong `references/linh-kien-html.md`.
4. **Vẽ hình** 2–4 hình SVG theo `references/hinh-svg.md`, dùng `scripts/svg_lib.py` (sinh bằng script, chèn idempotent như `build_figs.py` của bài mẫu).
4b. **Ghi thí nghiệm vào kho dữ liệu** `content/thi-nghiem/` (một file JSON cho mỗi thí nghiệm hoặc ví dụ: dụng cụ, các bước, tham số + khoảng giá trị, phương trình, số liệu mẫu, hiểu lầm hay gặp, gợi ý mô phỏng). Đây là dữ liệu nguồn cho giai đoạn **làm mô phỏng** tiếp theo, nên không để thí nghiệm chỉ nằm trong HTML. Gắn `data-exp="<id>"` lên hộp `.tl-box--exp` / `<figure>` tương ứng. Quy ước đầy đủ: `content/thi-nghiem/README.md`.
5. **Kiểm.** `python3 .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/lint_theory.py <theory.html>` (lỗi cấu trúc) → `python3 .../scripts/lint_do_dai.py <theory.html>` (**hạn mức độ dài**: tổng từ hiện ngay, từng mục, đoạn liền không có nhịp, "tới việc đầu" = từ mốc `<h3>` đầu tới quiz/câu dự đoán đầu tiên ≤ 150 từ — mục vượt 600 từ phải tách mục con; exit 1 nếu có lỗi cứng, xem `docs/PHUONG-PHAP-NOI-DUNG-LY-THUYET.md`) → `python3 .../scripts/check_quizzes.py <theory.html>` (kiểm logic tự chấm của mọi `.tl-quiz` **không cần trình duyệt**: đúng 1 đáp án `tl-ok`, input đứng ngay trước label, hai hộp phản hồi là con trực tiếp) → `python3 .../scripts/thi_nghiem.py <theory.html>` (kiểm kho thí nghiệm + liên kết `data-exp`, sinh `index.json`) → **xem thử**:
   - **Trên Mac (không có Playwright/`/opt/pw-browsers`)**: `python3 .../scripts/build_preview.py <theory.html> [thư-mục-ra]` rồi `python3 .../scripts/chup_anh.py <thư-mục-ra>` — dùng Google Chrome headless + CDP, đúng **375 CSS px** (Chrome trên Mac ép cửa sổ tối thiểu 500px nên `--window-size` không dùng được), tự cắt nền, lưu WebP (`xem-thu-desktop`, `sec-<n>`, `fig-<n>`, `mau-tra-loi-sai`). Ảnh `sec-*` đã mở sẵn `<details>` + đặt sẵn `checked` vào đáp án đúng nên **không cần JS** để thấy phản hồi. Soát tràn ngang trước khi chụp: `python3 .../scripts/chup_anh.py <thư-mục-ra> --kiem-tran`.
   - **Trên cloud (có Chromium `/opt/pw-browsers`)**: `node .../scripts/preview.mjs <theory.html> <thư-mục-ra>` (chụp 375px từng hình + tự bấm mọi đáp án kiểm phản hồi).
   - Trang `xem-thu/xem-thu.html` mở bằng Chrome là bấm thử được ngay (có nút "Mở tất cả đáp án") — đưa link/ảnh này cho thầy xem trước khi đăng.
   **Phải xem ảnh bằng mắt** — nhãn chồng chữ/cắt biên không script nào bắt được. Lưu ý bẫy đã gặp: trang xem thử thiếu lề phải làm chữ chạm mép; cửa sổ chụp hình quá thấp làm mất `figcaption`.
6. **Đóng gói `bundle.json`** (schema `thachlab.lesson-bundle/v1`): `theory_html` + `worked_examples: []` + `exam` gồm các câu tự kiểm tra trong bài (validate bắt buộc ≥1 câu). Kiểm: `npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts <bundle.json>` (dùng đúng `validateBundle` của trang nhập bài). Phải `ok: true`.
7. **Báo thầy** (ngắn): bài gì, hình nào ở đâu, đã kiểm gì. Nhắc lệnh trên Mac, **mặc định chỉ đẩy phần lý thuyết** (không đụng đề, bài tập mẫu, tiêu đề, tiến độ học):
   ```
   cd /Users/MAC/Projects/thachlab && git pull origin main
   bash scripts/cap-nhat-ly-thuyet.sh content/lesson-samples/<thư-mục-bài>/theory.html <lesson_id>
   # SAU KHI GHI DB BẮT BUỘC deploy (site tĩnh: build đọc DB lúc build). Deploy từ worktree sạch:
   git -C .claude/worktrees/deploy-tree checkout --detach origin/main && (cd .claude/worktrees/deploy-tree && bash scripts/deploy.sh)
   ```
   Script tự: lint → dry-run **in rõ phạm vi** (mục nào ghi, mục nào của bài bị bỏ qua) + sao lưu `body_html` cũ ra `scripts/logs/` → hỏi xác nhận → chỉ ghi cột `body_html` của mục `ly_thuyet` (UPDATE ràng buộc cả `id` lẫn `kind='ly_thuyet'`, đòi đúng 1 dòng), rồi **chụp toàn bộ `lesson_items` của bài trước/sau và đối chiếu**: ngoài mục Lý thuyết, mọi cột/mục khác phải y nguyên, lệch là exit 1 kèm lệnh hoàn tác. Quy tắc thầy chốt 4/10/2026: **đăng bài lý thuyết chỉ chạm đúng mục Lý thuyết của bài đó, không làm ảnh hưởng phần còn lại** (Luyện tập, Kiểm tra, Bài tập mẫu, tiêu đề, tiến độ học) — script thực thi quy tắc này chứ không dựa vào việc người chạy nhớ. Hoàn tác: `npx tsx scripts/khoi-phuc-ly-thuyet.mts <file sao lưu>`. Chỉ dùng `upload-lesson.mts` (tạo cả đề Luyện tập) khi thầy nói rõ muốn đăng cả đề. Commit chỉ đúng thư mục bài + file đã đụng; không tự đăng DB.
   **Lưu ý HTML:** trong `$…$` viết `\lt`, `\gt` thay cho `<`, `>` (ký tự `<k` bị HTML hiểu là thẻ và làm hỏng công thức).

## Dàn ý bài (nhịp 6 phần, mỗi phần là một `<h3>` đánh số I., II.…)

Dùng `<h3>` làm mốc — `wrapTheorySections` cắt đoạn theo `<h3>` để nút "Ôn ngay" của quiz cuộn đúng chỗ. Không dùng `<h2>` "LÝ THUYẾT" ngoài `<h3>`.

| Phần | Nội dung | Linh kiện |
|---|---|---|
| I. Mở bài | Tình huống đời thường gần học sinh (sân băng, xưởng CNC, xe đạp, bếp...), kể bằng người dẫn chuyện trung tính (**KHÔNG** dùng vai "thầy"), kết bằng câu hỏi "tại sao?" | hộp **dự đoán** (radio) |
| II. Kiến thức | **Từ khoá để nhớ** (xem mục "Ít chữ") + phát biểu dạng gạch đầu dòng + công thức + ký hiệu; mỗi ý có **ví dụ**; ít nhất một **thí nghiệm** Làm–Quan sát–Rút ra, trong đó **ít nhất một thí nghiệm đo có bảng số liệu thật + câu hỏi về sai số** (học sinh đọc bảng, không cần tự đo) | hộp **định nghĩa** + hình + `.tl-box--exp` + `<details>` "xem thêm" |
| III. Bẫy | 2–3 "cái bẫy" của riêng bài, vì sao sai; mỗi bẫy một **bảng đối chiếu hai khái niệm dễ lẫn** + tự kiểm tra | bảng + hình + **tự kiểm tra** |
| IV. Trả bài | 5–6 câu nhớ lại lý thuyết/công thức, chưa giải bài; mỗi câu nhắc "nói bằng lời của em rồi mới bấm xem" | `<details>` trong hộp `tl-box--think` |
| V. Bài toán mẫu | Đề bài → bảng *Câu trong đề / Dữ liệu / Kiến thức liên quan* → lời giải từng bước → kiểm tra kết quả → **một bài để trống 1–2 bước cho học sinh điền** → **biến thể** (đổi số, đổi chiều, đổi vị trí điểm) | `.tl-table--data` + `.tl-steps` + hình + quiz |
| VI. Đời sống + tổng kết | 3–4 ứng dụng; **thử thách phân tầng ⭐ ⭐⭐ ⭐⭐⭐**; khung "Mang về sau bài học" dạng chuỗi từ khoá (có ý về cách đọc đề) | `<details>` + hộp định nghĩa |

## Giọng văn (thầy chốt lại 2/10/2026)

- **KHÔNG dùng vai "thầy" trong bài đọc.** Bỏ hẳn các câu kiểu "Ở lớp, thầy cho cả lớp…", "Thầy hỏi: …",
  "Mỗi câu của đề, thầy tự hỏi: …". Bài là bài đọc cho học sinh, không phải biên bản lời giảng; ai đọc cũng
  thấy mình là người được nói tới. Viết lại thành câu trung tính/hướng dẫn: "Thử ngay tại lớp: …",
  "Câu hỏi để nghĩ trước khi đọc tiếp: …", "Với mỗi câu của đề, tự hỏi hai điều: …".
- Gọi người học là "em". Câu ngắn. Mở bằng cảnh thật, **không** mở bằng định nghĩa.
- **Được phép** trích lời học sinh ("Thầy ơi, em đẩy thành chứ có đẩy mình đâu…") — đó là lời thoại của
  học sinh, khác với người dẫn chuyện đóng vai thầy. Mẹo nhớ có tên (4 chữ, 1 câu hỏi kiểm tra).
- Sai thì **giải thích vì sao sai** và gợi cách nghĩ lại, không chỉ báo "sai". Đúng thì củng cố lý do.
- Thầy dạy vật lí THPT + CNC/chế tạo máy + trượt băng: ưu tiên ví dụ từ ba mảng đó. Trả lời chung gọn, vào thẳng kết quả.

## Phong cách chốt cho MỌI bài sau (bảng đầy đủ: `references/phuong-phap-day-tq.md`)

Bài Mô tả sóng (`content/lesson-samples/l11-mo-ta-song/`) là bài mẫu thứ hai, soạn sau bài Newton và Giao thoa —
nhịp dưới đây là chuẩn, lượt sau không hỏi lại:

1. Khung **🎯 Mục tiêu bài học** ở đầu bài (2–4 gạch đầu dòng + "cuối bài phải tự trả lời được N câu ở mục Trả bài").
2. **情境导入** — mở bằng một cảnh học sinh đã thấy, không mở bằng định nghĩa.
3. **先猜后学** — hộp dự đoán 3–4 phương án ngay sau cảnh mở bài, phản hồi giải thích vì sao.
4. Mỗi ý kiến thức: **dòng 🔑 3–6 từ** → gạch đầu dòng ngắn → ví dụ/thí nghiệm (Làm–Quan sát–Rút ra) → quiz tự chấm.
5. **易错点辨析** — 2–3 "cái bẫy" của riêng bài, mỗi bẫy kèm bảng đối chiếu hai khái niệm dễ lẫn.
6. **当堂检测 + 错因分析** — 6–8 quiz rải khắp bài; phản hồi sai phải gọi tên lỗi cụ thể, không chỉ báo sai.
7. **变式训练 + 分层练习** — sau bài toán mẫu có "Thử sức đổi số / đổi chiều" và thử thách ⭐ ⭐⭐ ⭐⭐⭐.
8. **归纳小结** — khung "✅ Mang về sau bài học" toàn từ khoá, có một dòng về cách đọc đề.
9. Mẹo/口诀 riêng cho từng công thức khó nhớ; `<details>` cho phần mở rộng (không giấu kiến thức bắt buộc).
10. **Ba nét từ nghiên cứu tự học** (chi tiết + lý do ở `references/phuong-phap-day-tq.md`): tự giải thích trước khi xem đáp án (mục Trả bài); bài giải **để trống 1–2 bước** giữa bài mẫu và biến thể; dòng "Em chắc bao nhiêu?" trước 2–3 quiz quan trọng.

## Ít chữ — nhớ bằng từ khoá (thầy yêu cầu 2/10/2026, áp dụng cho MỌI bài sau)

Bài mẫu còn nhiều chữ. Phong cách thầy: **mỗi kiến thức/định luật/tính chất được cô đọng thành vài từ khoá để học sinh nhớ**, văn xuôi chỉ để dẫn vào hoặc giải thích vì sao.

- Mỗi ý chính của phần II (và khung "Mang về") có một **dòng từ khoá** in đậm, 3–6 từ, dạng cụm danh từ/vế ngắn, bỏ từ nối. Ví dụ: `Cùng độ lớn · Ngược chiều · Cùng phương · Khác vật` hay mẹo 4 chữ có tên. Đặt ngay dưới tiêu đề ý, **trước** phần giải thích.
- Phát biểu định luật/tính chất: tách thành **gạch đầu dòng ngắn** (mỗi dòng một đặc điểm, ≤ 8 từ) hoặc bảng 2 cột *Từ khoá → Nghĩa*, không viết thành đoạn văn dài. Công thức kèm chú thích ký hiệu 1 dòng.
- Đoạn văn xuôi tối đa 2–3 câu liền nhau; quá thì tách thành từ khoá + bullet, phần còn lại chuyển vào `<details>` "xem thêm".
- Khung "Mang về sau bài học" = **chuỗi từ khoá** (mỗi ý 1 dòng ≤ 10 từ), không viết lại bài.
- Mục "Trả bài" (IV): đáp án trong `<details>` cũng là từ khoá, không câu dài.
- Trước khi giao: rà từng `<h3>`, đếm đoạn `<p>` > 3 câu → rút gọn. Mở bài và lời giải bài toán mẫu giữ giọng kể, nhưng cũng vào thẳng ý.

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
10. **Không viết vai "thầy" vào bài** (thầy nhắc 2/10/2026 khi đọc bài Mô tả sóng): "thầy cho cả lớp…", "Thầy hỏi: …", "thầy tự hỏi: …" đều phải bỏ. Đây là lỗi giọng văn dễ tái phát nhất vì bài mẫu cũ (`l10-dinh-luat-3-newton`) còn dùng.
11. **Trang xem thử phải có `.wrap` (lề 16px + max-width 720px)** cho cả trang từng mục: thiếu nó, chữ chạm mép phải ở 375px mà đọc ảnh mới thấy.
12. **Chụp ảnh phải ép đúng 375 CSS px qua CDP** (`chup_anh.py` bản hiện tại dùng `Emulation.setDeviceMetricsOverride` + `captureBeyondViewport`): Chrome macOS ép cửa sổ tối thiểu 500px nên bản cũ `--window-size` cho ảnh "375px" thực chất là layout 500px, duyệt nhầm bố cục. Bản CDP chụp trọn trang nên không còn lo cửa sổ thấp làm mất `figcaption`. Chép script từ thư mục bài sang skill **cả hai chiều** mỗi khi sửa (đã lệch một lần 2/10/2026).
13. **Bảng ở 375px: tối đa 3 cột.** Bảng 4 cột (Đại lượng | Ký hiệu | Nghĩa | Hệ thức) phải gộp lại thành 3 cột *Đại lượng | Ký hiệu (đơn vị) | Nghĩa ngắn và hệ thức*; bảng rộng hơn thì `.table-scroll` cho cuộn ngang chứ đừng để chữ bị bóp.
14. **Trang bài thật (`.lesson-page`) bỏ khung viền của `.katex-display`** và đặt `.katex` nội dòng thành `display:inline; overflow:visible` → **công thức nội dòng không tự cuộn được**, dài quá ~300px là đẩy tràn trang. Công thức khối vẫn là scroll container: rộng hơn ~343px thì học sinh phải vuốt mới thấy hết → **chẻ thành 2 dòng `$$…$$`**. `--kiem-tran` báo cả hai loại (`cong thuc khoi phai cuon: 343px khung / 390px noi dung`).
15. **Chrome trên macOS ép cửa sổ tối thiểu 500px**: `--window-size=375` cho ra layout **500px**, ảnh "375px" là giả (dính 2/10/2026, chỉ lộ ra khi in `innerWidth`). Phải dùng CDP `Emulation.setDeviceMetricsOverride` + `captureBeyondViewport` — `scripts/chup_anh.py` làm sẵn (tự viết WebSocket client bằng thư viện chuẩn; không cần Playwright, không cần gói `ws`).
16. **Trang xem thử phải nạp đủ CSS như trang thật**: cắt `globals.css` từ mốc `/* ---------- Nội dung đề thi (chuyển từ Azota/Word) ---------- */` — bắt đầu ở khối "Hình vẽ SVG nội tuyến" sẽ **thiếu rule `.katex`/`.katex-display`**; và **bọc trong `.lesson-page`**, nếu không preview khác trang thật (công thức khối còn khung, cỡ chữ 1.125rem thay vì 1rem).
17. **Chrome headless không tự thoát** sau khi ghi ảnh/`--dump-dom` (treo vô hạn trên Mac) → luôn mở bằng `start_new_session=True` rồi `os.killpg` đúng nhóm tiến trình; đừng `pkill -f "Google Chrome"` (giết cả Chrome của thầy). `--dump-dom` không dùng được để kiểm quiz; thay bằng `check_quizzes.py` (đọc HTML) hoặc đặt sẵn `checked` rồi chụp.
18. **Bài Mô tả sóng KHÔNG còn là khuôn về độ dài** (đo lại 2/10/2026): 3.021 từ hiện ngay (~22 phút), mục con "Năm đại lượng đặc trưng" 489 từ trong một `<h4>`, một đoạn 478 từ liền không có gì để làm — trong khi ba bài ngắn (1.103–1.537 từ, 8–11 phút) mới là mức đọc thoải mái. Đã cắt còn 2.457 từ (0 lỗi cứng). Trước khi giao bài, chạy `scripts/lint_do_dai.py`; mục vượt 480 từ phải tách mục con. Hạn mức + lý do: `docs/PHUONG-PHAP-NOI-DUNG-LY-THUYET.md`.
19. **Bảng 3 cột ở 375px rất dễ bị bóp chữ** (phát hiện 2/10/2026 khi xem ảnh bài Mô tả sóng): bảng "Đại lượng | Ký hiệu (đơn vị) | Nghĩa…" làm header cột giữa xuống dòng từng chữ, bảng so sánh có ô header rỗng làm nhãn hàng gãy giữa chữ ("Phu/thu/ộc"). Script `--kiem-tran` chỉ bắt tràn ngang, **không bắt được cái này** — phải xem ảnh. Cách sửa: gộp về **bảng 2 cột** (ô đầu = đối tượng, ô sau = nghĩa), hoặc đổi thành 2 khối/danh sách song song. Giữ 3 cột chỉ khi cả 3 header đều ngắn (kiểu bảng *Câu trong đề / Dữ liệu / Kiến thức*).

## Cần kiểm tra khi thầy xem được bài mẫu (điền tiếp)

- [ ] Radio tự chấm hiện đúng trong app thật (không bị React/`ContentHtml` render lại làm mất chọn)?
- [ ] `<details>` mở/đóng ổn trên điện thoại?
- [ ] Độ dài bài (bài Mô tả sóng 51 KB, 6 phần) có vừa ý; mật độ tương tác (7 quiz) có quá nhiều/ít?
- [ ] Hình SVG: kiểu que có chấp nhận được hay cần vẽ đẹp hơn?
- [ ] Giọng văn sau khi bỏ vai "thầy": đã đúng ý chưa?

## Chốt nhanh sau khi thầy duyệt (rút kinh nghiệm 2/10/2026 — tiết kiệm token)

- Thầy nói "duyệt/đăng đi" → **chạy ngay trên Mac của thầy** `bash scripts/cap-nhat-ly-thuyet.sh <theory.html> <lesson_id> --yes` (chỉ ghi phần lý thuyết, tự sao lưu) **rồi deploy luôn** (ghi DB xong mà chưa deploy thì web vẫn hiện bài cũ — đã dính 2/10/2026), thầy đã cho phép deploy tự động. **Không** mở PR, không hỏi lại, không chờ merge: script đọc file local. Commit file bài lên nhánh và PR chỉ làm khi thầy yêu cầu.
- Chỉ chạy lệnh DB khi thầy đã duyệt bằng lời; trước đó dừng ở `theory.html` + ảnh xem thử.
- Cắt việc thừa: đã có lệnh, **không** đọc lại bài mẫu 27 KB, `linh-kien-html.md` hay catalog/bài cũ khi không cần; không chạy lại toàn bộ kiểm khi chỉ sửa chữ (chỉ `lint_theory.py` + `validate_bundle.mts`).
- Xem thử: trên Mac một lệnh `build_preview.py` + `chup_anh.py` là có đủ ảnh 375px, ảnh từng hình và trang bấm thử (`xem-thu.html`); không lặp "cuộn từng hình → chụp". Chỉ sửa hình nhỏ thì chạy `chup_anh.py <thư-mục> --chi-hinh`.
- `<` / `>` trong `$…$` viết `\lt`/`\gt` ngay từ đầu để khỏi sửa lại.
- Đừng giải thích dài giữa chừng; báo một lần cuối: đã đăng chưa, link bài, file sao lưu.

## Làm nhiều bài một đợt — thuê subagent song song (chốt 4/10/2026)

Thầy hỏi 4/10/2026: "gọi subagent làm song song các bài có tiết kiệm token hơn không?" — **Có, nhưng tiết kiệm
token của PHIÊN CHÍNH, không phải tổng token của cả hệ thống.** Mỗi lượt trong phiên chính gửi lại toàn bộ
ngữ cảnh; soạn 14 bài trong phiên chính thì ngữ cảnh phình theo cấp số cộng (14 bài cũ + 14 bản nháp + log
lint + ảnh), tốn hơn hẳn khoản lặp ~30–50k token mà mỗi subagent phải trả để đọc lại SKILL.md + bài mẫu.
Subagent có ngữ cảnh riêng, xong là vứt; phiên chính chỉ nhận một bản tóm tắt JSON.

**Quy tắc chọn:**
- Đợt **≥ 3 bài** → chia lô 4–5 bài, mỗi bài một subagent soạn, chạy song song; mỗi bài thêm một subagent
  **kiểm chéo độc lập**; chỉ gọi subagent thứ ba (sửa) khi bản kiểm chéo có lỗi.
- Đợt **1–2 bài** → tự làm trong phiên chính; thuê agent chỉ tốn thêm mà không được lợi gì.

**Prompt cho agent soạn phải TỰ CHỨA** (agent KHÔNG thấy hội thoại, không thấy skill nếu không được chỉ):
repo (chạy mọi lệnh từ gốc `thachlab`) · `lesson_id` + tên bài + chương · thư mục bài mới · tiền tố id quiz
(`tl<bài>-`) và tiền tố file thí nghiệm (`tn-l12-<slug>-NN.json`) · danh sách file **phải đọc** (SKILL.md,
`references/linh-kien-html.md`, `references/hinh-svg.md`, `references/phuong-phap-day-tq.md`, một bài mẫu mới
nhất, `content/thi-nghiem/README.md` + 1 file mẫu, `public/data/lessons/<id>.json` để giữ đủ ý bắt buộc) ·
sản phẩm (theory.html 6 phần, `build_figs.py`, file thí nghiệm, `bundle.json`) · **ràng buộc cứng chép nguyên**
(`.tl-quiz` input ngay trước label + anh em trực tiếp, cấm `<script>/<style>/on*=`, `\lt`/`\gt`, bảng ≤3 cột,
cấm vai "thầy", độ dài ~2.000–2.500 từ) · **lệnh kiểm chính xác** (lint_theory, lint_do_dai, check_quizzes,
thi_nghiem, build_preview, chup_anh `--kiem-tran`, chup_anh, validate_bundle) · yêu cầu **xem ảnh bằng mắt**
(`--kiem-tran` không bắt được nhãn chồng chữ) · **cấm** git commit/push, ghi DB, sửa `app/globals.css`, sửa
file của bài khác · định dạng JSON trả về.

**Prompt cho agent kiểm chéo:** đọc `theory.html` + file thí nghiệm + `bundle.json`; tự giải lại **từng quiz**
và xác nhận đúng 1 đáp án đúng / các đáp án sai chắc chắn sai; tính lại mọi số liệu trong bảng, bài toán mẫu,
biến thể, thử thách; soát ràng buộc cấu trúc; đối chiếu bản cũ xem có bỏ sót ý bắt buộc; trả JSON
`{ok, issues:[{muc_do, vi_tri, van_de, cach_sua}]}`. Agent này KHÔNG sửa bài.

**Việc phiên chính phải tự làm (đừng giao agent):**
1. Chạy `thi_nghiem.py` **một lần cuối** để sinh `content/thi-nghiem/index.json` — file dùng chung, chạy song
   song thì lần ghi sau đè lần trước và có thể thiếu mục.
2. `git commit` (chỉ file của đợt), ghi DB `bash scripts/cap-nhat-ly-thuyet.sh <theory.html> <lesson_id> --yes`,
   deploy, cập nhật `docs/STATE.md` + memory.

**Chạy song song an toàn:** `chup_anh.py` mở Chrome với `--user-data-dir` tạm riêng + cổng debug ngẫu nhiên nên
chạy song song được, nhưng 14 Chrome cùng lúc ngốn RAM → chạy theo lô 4–5 bài. `thi_nghiem.py` ghi `index.json`
dùng chung: agent vẫn nên chạy nó để tự kiểm liên kết `data-exp`, nếu báo lỗi do file của bài khác đang ghi dở
thì chạy lại một lần, **tuyệt đối không sửa file của bài khác**.

**Bài học vận hành (bắt buộc, đã trả giá 4/10/2026):**
- **Đưa ĐỦ danh sách lỗi cho agent sửa.** Bản kiểm chéo trả 8–14 lỗi/bài; cắt ngắn JSON (từng cắt ở 4 000 ký
  tự) làm agent sửa chỉ thấy 6 lỗi đầu → vòng kiểm sau tìm lại đúng những lỗi đã bị bỏ. Cho nguyên JSON
  (`slice(0, 30000)`) và yêu cầu sửa **cả `chan` lẫn `nen_sua`**, kèm lý do cho mục không sửa.
- **Kiểm hai vòng là bình thường, không phải làm lại.** Vòng 2 trên 5 bài vẫn bắt được 3–4 lỗi `chan`/bài
  (số liệu thí nghiệm mâu thuẫn, mũi tên SVG ngược chiều, phản hồi quiz gọi tên phương án không tồn tại, số
  hình không theo thứ tự). Đừng tin báo cáo "đã sửa hết" của agent soạn.
- **Nhiều phiên cùng chạy → không ghi đè.** Đợt này một phiên khác đã soạn và đăng bài 15 (id 126) trước;
  bài đó bị **bỏ khỏi danh sách đăng**, bản của mình để nguyên, không ghi đè (đúng luật "xung đột" trong
  `AGENTS.md`). Trước khi đăng phải `select` lại `lesson_items` để biết bài nào vừa được phiên khác đăng.
- **`chup_anh.py` cắt mục dài thành khúc.** Mục II nhiều mục con chụp ở scale=2 có thể cao 15 000–20 000 px:
  WebP/VP8 cứng trần 16 383 px (script chết giữa vòng) và ảnh đó cũng không ai soi được. Từ 4/10/2026 script
  tự cắt thành `sec-2a`, `sec-2b`… mỗi khúc ≤ 5 000 px và xoá khúc cũ của lần chạy trước.
- **`xem-thu/` không commit.** 13 bài lớp 12 cho ra 43 MB ảnh — nặng vĩnh viễn cho repo, mà sinh lại được
  bằng hai lệnh (`build_preview.py` rồi `chup_anh.py`). Commit `theory.html` + `theory.src.html` +
  `build_figs.py` + `build_bundle.py` + `bundle.json` là đủ; để `xem-thu/` lại trên máy cho thầy xem.

**Đo đợt 4/10/2026 (14 bài Vật lí 12, trừ bài thực hành đo + kiểm tra):** 1 bài chạy thử một mình + 3 lô
(3 + 5 + 5 bài) + 1 vòng kiểm lại 5 bài = **~50 lượt subagent**, khoảng **2 giờ** tính từ lúc bắt đầu soạn đến
lúc đăng xong; **mọi bài đều có ít nhất một lỗi `chan`** do bản kiểm chéo bắt được (nhiều nhất 4 lỗi/bài),
5 bài phải sửa hai vòng. Kết quả: 13 bài đăng DB + deploy (bài 15 id 126 bỏ vì phiên khác đăng trước).
