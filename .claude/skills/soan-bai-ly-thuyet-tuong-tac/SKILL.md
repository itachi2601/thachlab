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
4c. **Video (clip YouTube thật).** Hai chỗ khai, đều **không viết khối `<div class="tl-box--video">` bằng tay**:
   - **Clip mở bài** (đặt vấn đề bằng hiện tượng thật) → `content/thi-nghiem/video-theo-bai.json`, `vi_tri: "mo_bai"`; script chèn ngay trước hộp "Dự đoán trước khi học" của mục I. Clip chỉ quay hiện tượng, không giải thích cơ chế, không lộ đáp án (V7).
   - **Clip của từng hộp thí nghiệm** → field `video` trong chính `tn-*.json` đó (`youtube_id`, `nhin_vao` bắt buộc ≤ 25 từ, `giay_bat_dau`/`giay_ket_thuc` ≤ 90 giây); `vi_tri` cũng nhận `truoc:<data-exp>`/`sau:<data-exp>` cho mốc bất kỳ.
   Chèn: `npx tsx scripts/chen-video-thi-nghiem.mts --bai <slug> --apply` (tự chèn sau hộp `.tl-box--exp`/trước hộp Dự đoán, đồng bộ `theory.src.html` + `theory.html` + `theory_html` trong `bundle.json`, chạy lại không nhân đôi); kiểm link sống/nhúng được: `--kiem [--apply]`. Clip dùng nhiều bài: khai một lần ở `content/thi-nghiem/video-dung-chung.json`. Quy tắc V1–V7 ở `docs/QUY-TAC-THIET-KE.md` mục 5b; kiểm dữ liệu bằng `thi_nghiem.py`.
5. **Kiểm.** `python3 .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/lint_theory.py <theory.html>` (lỗi cấu trúc) → `python3 .../scripts/lint_do_dai.py <theory.html>` (**hạn mức độ dài**: tổng từ hiện ngay, từng mục, đoạn liền không có nhịp, "tới việc đầu" = từ mốc `<h3>` đầu tới quiz/câu dự đoán đầu tiên ≤ 150 từ — mục vượt 600 từ phải tách mục con; exit 1 nếu có lỗi cứng, xem `docs/PHUONG-PHAP-NOI-DUNG-LY-THUYET.md`) → `python3 .../scripts/check_quizzes.py <theory.html>` (kiểm logic tự chấm của mọi `.tl-quiz` **không cần trình duyệt**: đúng 1 đáp án `tl-ok`, input đứng ngay trước label, hai hộp phản hồi là con trực tiếp) → `python3 .../scripts/thi_nghiem.py <theory.html>` (kiểm kho thí nghiệm + liên kết `data-exp`, sinh `index.json`) → **xem thử**:
   - **Trên Mac (không có Playwright/`/opt/pw-browsers`)**: `python3 .../scripts/build_preview.py <theory.html> [thư-mục-ra]` rồi `python3 .../scripts/chup_anh.py <thư-mục-ra>` — dùng Google Chrome headless + CDP, đúng **375 CSS px** (Chrome trên Mac ép cửa sổ tối thiểu 500px nên `--window-size` không dùng được), tự cắt nền, lưu WebP (`xem-thu-desktop`, `sec-<n>`, `fig-<n>`, `mau-tra-loi-sai`). Ảnh `sec-*` đã mở sẵn `<details>` + đặt sẵn `checked` vào đáp án đúng nên **không cần JS** để thấy phản hồi. Soát tràn ngang trước khi chụp: `python3 .../scripts/chup_anh.py <thư-mục-ra> --kiem-tran`.
   - **Trên cloud (có Chromium `/opt/pw-browsers`)**: `node .../scripts/preview.mjs <theory.html> <thư-mục-ra>` (chụp 375px từng hình + tự bấm mọi đáp án kiểm phản hồi).
   - Trang `xem-thu/xem-thu.html` mở bằng Chrome là bấm thử được ngay (có nút "Mở tất cả đáp án") — đưa link/ảnh này cho thầy xem trước khi đăng.
   **Phải xem ảnh bằng mắt** — nhãn chồng chữ/cắt biên không script nào bắt được. Lưu ý bẫy đã gặp: trang xem thử thiếu lề phải làm chữ chạm mép; cửa sổ chụp hình quá thấp làm mất `figcaption`.
6. **Đóng gói `bundle.json`** (schema `thachlab.lesson-bundle/v1`): `theory_html` + `worked_examples: []` + `exam` gồm các câu tự kiểm tra trong bài (validate bắt buộc ≥1 câu). Kiểm: `npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts <bundle.json>` (dùng đúng `validateBundle` của trang nhập bài). Phải `ok: true`.
7. **Báo thầy** (ngắn): bài gì, hình nào ở đâu, đã kiểm gì. Nhắc lệnh trên Mac, **mặc định chỉ đẩy phần lý thuyết** (không đụng đề, bài tập mẫu, tiêu đề, tiến độ học). **Bồi dặp video vào bài ĐÃ ĐĂNG thì thêm `--chi-video`** (chỉ ghi nếu phần ngoài khối video giống hệt DB — chặn ghi đè bản sửa trực tiếp trên web); kiểm loạt trước bằng `npx tsx scripts/so-file-voi-db.mts` (chỉ đọc, 1 truy vấn) — bài nào file ≠ DB sẽ bị chặn, phải xem tay rồi mới quyết:
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

### Lỗi kiểm chéo bắt được ở cả 14 bài lớp 12 (4/10/2026) — soát trước khi giao

Đợt 14 bài, **bài nào cũng bị bắt ít nhất một lỗi `chan`**; đây là các nhóm lỗi lặp lại, kiểm trước khi trình thầy:

20. **Không để `$…$` trong `<text>` của SVG.** KaTeX auto-render chèn `<span>` HTML vào trong SVG → **chữ biến mất** (bài 6 Boyle/Charles mất nhãn V, p, T₁, T₂; chỉ lộ khi xem ảnh). Nhãn hình viết chữ thường + `<tspan baseline-shift="sub">` cho chỉ số dưới.
21. **Phản hồi sai phải gọi tên đúng phương án ĐANG hiển thị.** Xoá/xáo phương án mà quên sửa `.tl-fb--no` → học sinh đọc "D — bỏ hệ số 931,5" trong khi bài chỉ có A, B, C (bài 15 hạt nhân, bài 5). Kiểm chéo phải so **từng chữ cái trong phản hồi** với danh sách phương án thật.
22. **Số liệu bảng thí nghiệm phải khớp phương trình `mo_hinh` của chính file JSON.** Đợt này bắt được: bảng Boyle lệch ~7 % so với `L = 21,8·760/(760+h)`; bảng lưỡng cực khớp `m = 0,02 A·m²` nhưng `tham_so` khai 0,5 (lệch 25 lần); "6,8·10¹¹ J ≈ hai vạn tấn than" (đúng là 23 tấn); "chậm hơn hàng nghìn lần" trong khi tỉ số là 2 vạn. Quy tắc: **tính lại bằng script**, đừng ước lượng bằng mắt.
23. **Hình SVG phải kiểm bằng TOẠ ĐỘ, không chỉ bằng mắt:** chấm dữ liệu phải nằm trên đường (bài 7: chấm đỏ lệch 26 px khỏi hypebol), trục phải chia tuyến tính (bài 7: 27 K và 60 K vẽ dài bằng nhau), mũi tên phải đúng chiều vật lí (bài 9: hai mũi "hút nhau" lại chĩa ra ngoài; từ trường chữ U vẽ S→N), đầu mũi phải nằm trên cung. `--kiem-tran` **không** bắt được nhóm lỗi này.
24. **Đáp án đúng không được dồn một chữ cái.** Bài 5 có 6/8 quiz đúng ở A (đoán A ăn 75 %). Xáo vị trí rồi **đổi luôn hậu tố `id`** cho khớp chữ cái mới, và đừng để nhóm "Em chắc" trùng `name` với một phương án.
25. **Thí nghiệm "đo" phải khớp ở ba chỗ:** bước *Làm* (số lần đo) ↔ bảng trong `theory.html` ↔ `so_lieu_mau` của file JSON. Bài 6 nói đẩy tới 3,0 ml mà bảng chỉ 4 hàng; nói ngâm "nước sôi" mà bảng dừng ở 75 °C.
26. **Số phút trong khung "🎯 Mục tiêu" phải khớp `lint_do_dai.py`** (bài 9 ghi 13 phút, đo ra 17,7; bài 18 ghi 15, đo ra 17,8). Chạy lint rồi mới điền số.
27. **Số hình theo đúng thứ tự xuất hiện** trong bài (bài 15 hạt nhân: 1 → 4 → 2 → 3).
28. **Đối chiếu TỪNG gạch đầu dòng của bản cũ trước khi bỏ.** Đợt này bỏ sót: định nghĩa mặt nam/mặt bắc của dòng điện tròn (bài 9), áp suất theo cột nước + trường hợp bịt kín hai đầu (bài 6), đặc điểm giống tạo bằng chiếu xạ + cảnh báo (bài 18). Ghi danh sách "ý bắt buộc" ra trước khi viết, rồi so lại sau.
29. **Viết ~2.300 từ hiện ngay, chừa chỗ cho lời giải.** Thêm lời giải bài toán mẫu và khối "điền bước trống" ở vòng sửa dễ đẩy bài qua 2.500 từ rồi phải cắt lại (bài 6 từng 2.840 → 2.464; bài 7 phải cắt để nhét lời giải).

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
- **Rà hiện trạng bằng DB, đừng tin `public/data/`.** `public/data/lessons/<id>.json` là bản build tĩnh cuối
  cùng, **không phải DB**: bài 2 hiện `tl=false` trong file tĩnh nhưng DB đã có bản tương tác từ trước → suýt
  chọn lại bài đã xong và suýt đăng đè. Trước khi chọn bài phải `select kind, body_html from lesson_items`
  (`kind='ly_thuyet'`) rồi mới kết luận bài nào còn thiếu.
- **Tiền tố id theo `lesson_id`, không theo "Bài N".** Lớp 12 có **hai "Bài 14"** (chương Từ trường id 125 và
  chương Hạt nhân id 15) — đánh theo số bài là trùng và khó tra. Đặt `tl125-…`, `tl15-…` theo id; nhờ vậy mới
  phát hiện phiên khác đang dùng `tl15-` cho bài 15 (khác bài với `tl15-` của mình).
- **Giữ bộ ba nguồn `theory.src.html` + `build_figs.py` + `build_bundle.py`.** Nguồn chứa mốc `<!--FIGn-->`;
  `build_figs.py` sinh hình rồi dựng `theory.html`; `build_bundle.py` dựng `bundle.json` từ `theory.html`.
  Ba bản luôn khớp byte, sửa một chỗ không sợ quên đồng bộ (13 bài đợt này đều theo khuôn đó).
- **Đăng theo lô rồi deploy MỘT lần.** 13 bài ghi DB mất ~2 phút (`cap-nhat-ly-thuyet.sh … --yes` trong vòng
  lặp, log `scripts/logs/dang-13-bai-l12-*.log`); chỉ deploy một lần ở cuối, đừng deploy từng bài.
- **Kiểm chứng ba tầng sau khi đăng** (đừng tin "chắc là lên rồi"): (1) **DB** — `lesson_items` của đúng bài có
  `tl-quiz`; (2) **bản build** — đọc `out/data/lessons/<id>.json` trong worktree deploy xem có `tl-quiz`;
  (3) **web thật** — `curl https://thachlab.id.vn/data/lessons/<id>.json`. Hosting chỉ kéo bản mới sau **5–10
  phút**, nên lần `curl` đầu vẫn ra bài cũ là bình thường — phải chờ rồi kiểm lại mới kết luận.

**Đo đợt 4/10/2026 (14 bài Vật lí 12, trừ bài thực hành đo + kiểm tra):** 1 bài chạy thử một mình + 3 lô
(3 + 5 + 5 bài) + 1 vòng kiểm lại 5 bài = **~50 lượt subagent**, khoảng **2 giờ** tính từ lúc bắt đầu soạn đến
lúc đăng xong; **mọi bài đều có ít nhất một lỗi `chan`** do bản kiểm chéo bắt được (nhiều nhất 4 lỗi/bài),
5 bài phải sửa hai vòng. Kết quả: 13 bài đăng DB + deploy (bài 15 id 126 bỏ vì phiên khác đăng trước).

## Chọn mô hình Claude cho từng việc (đề xuất 4/10/2026; đã đo 5/10/2026 trên 2 đợt thật — xem Nhật ký)

Mỗi bài có 4 loại việc đòi hỏi khác nhau; chọn mô hình theo việc, không theo bài:

| Việc | Mô hình | Vì sao |
|---|---|---|
| Soạn nội dung (giọng không vai "thầy", mở bài, câu dự đoán, bẫy, phân tích lỗi sai) + **vẽ SVG** | **Opus 5.5** (agent soạn) | Cần cảm quan sư phạm và suy luận không gian; SVG là chỗ hay sai nhất (chương 1 VL12 gặp 6 lỗi hình, mũi tên ngược chiều, nhãn chồng chữ). Mô hình mạnh hơn ít vòng sửa hơn. |
| Kiểm chéo (giải lại từng quiz, tính lại số liệu, soát ràng buộc) | **Sonnet 5.5** | Việc đối chiếu, rẻ hơn nhiều, đủ dùng. Nên là mô hình KHÁC agent soạn để không lặp cùng điểm mù. |
| Bài thực hành / bài ứng dụng đơn giản (khuôn lặp, ít hình) | **Sonnet 5.5** soạn thẳng | Tiết kiệm; vẫn qua kiểm chéo như thường. |
| Đóng gói bundle, xem thử, validate, ghi DB | script (`build_bundle.py`, `validate_bundle`, `cap-nhat-ly-thuyet.sh`) | Không cần mô hình mạnh. **Không dùng Haiku để soạn.** |

- Khối nhiều hình vector/đường sức (Vật lí 10 động học–động lực học, Vật lí 11 điện trường) → ưu tiên Opus cho agent soạn.
- Chỉ định mô hình bằng tham số `model` của công cụ Agent khi thuê agent soạn/kiểm (xem mục "thuê subagent song song").
- **Luồng chính (điều phối) chạy Sonnet**, không chạy Fable/Opus: nó chỉ chia việc, đọc JSON tóm tắt và chạy script. Fable dùng cho **đúng agent soạn nội dung** khi thầy yêu cầu, và agent đó soạn **trọn bài** (nội dung + SVG + bundle) — không tách "Fable viết chữ, Sonnet code hình" (đo 5/10/2026: tách làm mỗi bài qua 2 agent full-context + thêm agent "sửa hình", tốn gấp đôi).
- Làm theo **lô theo chương** (ví dụ 6 bài Điện trường L11) để dùng chung thư viện SVG và khung bài.
- Muốn chắc: soạn **cùng một bài** bằng hai mô hình, so số lỗi `chan` mà bản kiểm chéo bắt được rồi cập nhật bảng này.

## Nhật ký rút kinh nghiệm (bắt buộc cập nhật cuối MỖI phiên dùng skill này — xem `AGENTS.md`)

Cuối phiên, thêm vào đây mỗi bài học một dòng `- YYYY-MM-DD · <sự cố/phát hiện> → <cách làm đúng>`; nếu bài học làm
một bước phía trên sai/thiếu thì sửa luôn bước đó. Phiên không có bài học mới thì ghi "không có bài học mới" trong câu trả lời, không cần thêm dòng.

- 2026-10-05 · Đo 2 đợt thật cùng skill, cùng loại bài (L11): đợt chương 3 (6 bài, Sonnet điều phối, Opus soạn trọn bài, Sonnet kiểm chéo + sửa, 19 agent) tốn 0,55 triệu output / 46 triệu cache đọc; đợt chương 4 (5 bài, **Fable điều phối**, Fable soạn chữ + Sonnet code hình riêng, kiểm chéo, Fable sửa, Sonnet sửa hình, có bài kiểm chéo vòng 2, 22 agent) tốn 1,03 triệu output / 70 triệu cache đọc — gấp ~2 lần token mỗi bài (207k vs 92k output/bài), tiền còn chênh hơn vì Fable đắt nhất → giữ đúng bảng chọn mô hình ở trên: **luồng chính Sonnet; một agent soạn trọn bài (chữ + SVG + bundle); 1 vòng kiểm chéo; chỉ thuê agent sửa khi có lỗi.** Thầy nói "Fable làm nội dung" nghĩa là agent soạn, không phải phiên chính.
- 2026-10-05 · Luồng chính chạy Fable có 7 lượt gọi output ≥10k token (thinking ẩn tới 32k/lượt) chỉ để chia việc và đọc JSON trả về → điều phối không cần mô hình mạnh; phiên Sonnet lượt lớn nhất 12,6k.
- 2026-10-05 · Agent "code hình" của Sonnet đọc 204 lượt ảnh xem thử (34 MB base64, 56 ảnh PNG kích thước gốc ~570 KB, **112 lượt đọc lại cùng một file**), 2 agent nặng nhất 94 và 67 lượt gọi với 38 và 27 lần Read ảnh → trong prompt agent ghi rõ: chỉ xem ảnh `.webp` do `chup_anh.py` sinh (không chụp PNG gốc ở `/private/tmp`), **mỗi ảnh đọc một lần sau mỗi lần sửa**, sửa hình nhỏ thì `chup_anh.py --chi-hinh` rồi chỉ xem đúng `fig-<n>` đã sửa.
- 2026-10-05 · Prompt giao việc đợt chương 4 dài ~7,5k ký tự/agent (chép cả hướng dẫn vào prompt) so với ~3,3k đợt chương 3 → prompt chỉ cần: danh tính bài, danh sách file **phải đọc** (SKILL.md, references, bài mẫu), ràng buộc cứng, lệnh kiểm, định dạng JSON trả về — không chép lại nội dung skill.
- 2026-10-05 · Đợt chương 4 chạm hạn mức giữa chừng rồi chạy tiếp, thêm vòng khởi động lại → đợt >4 bài nên chia 2 lô và chốt (commit + ghi DB) xong lô 1 trước khi mở lô 2.
- 2026-10-05 · Đợt 5 bài Chương 4 VL11 (id 41–45) chia việc **Fable soạn nội dung / Sonnet viết code SVG + bundle / Sonnet kiểm chéo**, bàn giao qua `figs-spec.md` + `exam.json` trong thư mục bài → cách chia chạy được: ~30 lượt agent (5 soạn + 5 code + 5 kiểm v1 + 5 Fable sửa + 4 Sonnet sửa hình + 5 kiểm v2), vòng 2 chỉ còn 1–3 góp ý nhỏ/bài, phiên chính vá tay được. Vòng 1 **4/5 bài có lỗi `chan` về nội dung**, 0 lỗi chặn do code → mô hình mạnh hơn không thay được kiểm chéo.
- 2026-10-05 · `figs-spec.md` ghi TOẠ ĐỘ PIXEL cho nhãn/điểm thì gần như bài nào cũng sai (bài 26 điểm dóng lệch 10 px, bài 24 nhiều nhãn đè đường, bài 23 electron trùng hàng ion) → spec chỉ ghi vật lí, nhãn, phương trình và ràng buộc; agent code **tính lại từ phương trình** và có lớp kiểm hộp nhãn ↔ vật cản (không chồng, không vượt viewBox, không bị đường thẳng cắt xuyên) trước khi chụp ảnh.
- 2026-10-05 · Chữ 11 px trên viewBox 440 chỉ còn ~8,6 px ở 375 px — **cả 5 bài đều bị kiểm chéo bắt** → nhãn SVG ≥ 13–14 đơn vị viewBox (chỉ số dưới ≥ 11) hoặc viewBox ≤ 380 rộng; ghi thẳng vào spec từ đầu, đừng đợi kiểm chéo.
- 2026-10-05 · Marker mũi tên của `svg_lib` co theo bề dày nét: nét 3 cho đầu mũi 21 px đè nhãn → nét > 2,4 dùng `markerUnits="userSpaceOnUse"`.
- 2026-10-05 · Ký tự ℰ (U+2130) trong `<text>` SVG vẽ nhỏ như ε trên Mac, có thể thiếu font Android → dùng E nghiêng serif nhất quán cả bài, và I/U/R trong SVG cũng nghiêng serif (sans-serif 'I' nhìn như vạch đứng).
- 2026-10-05 · Thí nghiệm có LED (bài 24): pin 1,5 V không thắp được LED đỏ (Vf ≈ 1,8–2 V) và LED không phải điện trở thuần nên không dùng mô hình RC hàm mũ → thí nghiệm có LED phải kiểm Vf so với nguồn; mô hình chỉ áp cho tải thuần trở.
- 2026-10-05 · Bảng 3 cột "Câu trong đề / Dữ liệu / Kiến thức" có công thức trong ô vẫn gãy giữa công thức ở 375 px dù `--kiem-tran` sạch (bài 24, 25) → ô chỉ ghi giá trị số, hoặc đổi 2 cột "Câu trong đề | Dữ liệu → kiến thức".
- 2026-10-05 · `lint_do_dai.py` không đếm `<details>` và `.tl-fb` → muốn giảm số từ phải cắt phần hiện ngay; cắt phản hồi quiz vô ích. Lộ đáp án: `<details>` giải thích đặt TRƯỚC quiz làm hỏng "Em chắc bao nhiêu?" (bài 23) → details giải thích luôn đặt SAU quiz.
- 2026-10-05 · Tham chiếu kiểu "câu C ở quiz hiệu suất" mơ hồ khi bài có hai quiz cùng chủ đề và học sinh không thấy số quiz → trích nguyên văn phương án và tên mục.
- 2026-10-05 · Sửa sau kiểm chéo phải TUẦN TỰ Fable (nội dung) → Sonnet (code): cả hai đều chạy `build_figs.py` ghi `theory.html`/`bundle.json`/`xem-thu/`, chạy song song sẽ giẫm nhau.
- 2026-10-05 · Đợt 6 bài Chương 3 VL10 (id 59, 60, 62, 63, 64, 66; Sonnet điều phối, **Opus soạn trọn bài**, Sonnet kiểm chéo, chia 2 lô 3+3, ~24 lượt agent, mỗi agent soạn ~200–230k token) → 0 lỗi `chan` do code, chỉ 1 lỗi `chan` (bài 62: lời nhận xét bảng "hàng đầu lệch nhiều nhất" sai so với chính bảng — nhóm lỗi mục 22); nhắc lỗi lô 1 trong prompt lô 2 → bài lô 2 không còn `chan`. Sửa sau kiểm chéo: gửi nguyên danh sách lỗi cho **chính agent soạn** bằng SendMessage (còn ngữ cảnh, ~3–14 lượt/bài, rẻ hơn thuê agent mới).
- 2026-10-05 · Bảng "Câu trong đề / Dữ liệu / Kiến thức" 3 cột gãy chữ ở 375px dù ô ngắn (bài 63, 64, 66 đều dính) → mặc định dùng bảng 2 cột "Câu trong đề | Dữ liệu → kiến thức". Đơn vị viết ngoài `$…$` (`$1{,}67$ N`) bị xuống dòng tách khỏi số → để đơn vị trong công thức (`\ \text{N}`). Số thập phân sinh bằng script chèn vào `$…$` phải là `{,}`.
- 2026-10-05 · Hình mở bài ghi sẵn số liệu (8 cm/30 cm) làm lộ đáp án câu dự đoán (bài 66) → hình mở bài chỉ vẽ lực/đối tượng, số đo để ở lời giải. Mũi tên lực trên sơ đồ chất điểm phải cùng gốc ở trọng tâm; mũi tên cánh tay đòn phải trùng đường tác dụng.
- 2026-10-05 · Số liệu minh hoạ/giả định (người nhảy dù, lực hãm xe tải, bảng TN sinh từ mô hình) phải ghi "minh hoạ/giả định" NGAY trong hộp chữ, không chỉ ở chú thích hình/JSON; số liệu g=9,8 trong bảng mà bài mẫu dùng g=10 phải nêu g. Khẳng định "ABS giữ ở ma sát nghỉ", "tắt động cơ" kiểu Voyager là nói quá → dùng "gần ngưỡng", "không còn tăng tốc".
- 2026-10-05 · `thi_nghiem.py` chỉ nhận `muc_do` ∈ {co_ban, trung_binh, nang_cao}; fill SVG không dùng `var(--background)` (biến không tồn tại) → dùng none/rgba. Bản cũ có thể chứa lời giải sai (bài 63 VD11, VD12) → đừng chép lại, tính lại bằng script.
- 2026-10-05 · Đợt 11 bài còn thiếu Chương 1–2 VL10 (id 46–56; Sonnet điều phối; Opus soạn bài 49, 50, 52, 53, 54, 55; Sonnet soạn bài 46, 47, 48, 51, 56; Sonnet kiểm chéo; sửa bằng SendMessage cho chính agent soạn; 2 lô 5+6, ~45 lượt agent) → **0 lỗi `chan` do code/SVG; 3 lỗi `chan` đều là nội dung** (bài 50 nhận xét "lệch nhiều nhất" sai vì hai giá trị bằng nhau + max() trên số thực; bài 56 Câu 3 ngược chiều Bẫy 1/Hình 3; không bài nào còn lỗi sau 1 vòng sửa). Bài Sonnet soạn (thực hành/mở đầu) không kém Opus về số lỗi `chan`; khác biệt nằm ở số lỗi `nen_sua`.
- 2026-10-05 · "Lệch nhiều nhất/ít nhất" trong bảng số liệu: so TẬP các giá trị cực đại có dung sai 1e-6, không dùng `max()` trên số thực (8,3−8,0 và 8,0−7,7 khác nhau ở chữ số thứ 16 nên script tự kiểm lọt) → viết "lần 2 và lần 4 cùng lệch nhiều nhất" khi bằng nhau.
- 2026-10-05 · Bài thực hành đo: cách đo `s`/`h` (tâm hay mép bi) phải khớp ở ba chỗ — bước Làm, Bẫy, Hình — và chiều sai lệch trong quiz phải theo đúng Bẫy (bài 56). Hình có kết quả của bài mẫu đặt trong `<details>` SAU quiz (bài 54 lộ đáp án vì chú thích Hình 4).
- 2026-10-05 · Đáp án đúng luôn dài nhất kèm "vì…/nên…" (bài 46, 6/8 quiz) làm đoán theo độ dài ăn điểm → rút gọn đáp án đúng, kéo dài đáp án sai tương đương. Hộp "Rút ra"/bảng đặt trước quiz không được nói sẵn đáp án.
- 2026-10-05 · Bảng 2 cột nhãn hàng dài ở 375px vẫn vỡ chữ ("Nhó/m"): đổi sang danh sách gạch đầu dòng "Nhóm (hình dạng): kí hiệu" tốt hơn rút nhãn cột. Dấu "·" giữa các công thức trong một dòng đọc như dấu nhân → tách gạch đầu dòng hoặc dùng chấm phẩy.
- 2026-10-05 · Số lượng ghi trong tiêu đề phải đếm lại với bảng ("10 quy tắc" nhưng bảng 11 gạch, bài 47); mục tiêu hứa "thiết kế phương án đo bằng video" phải có bước thực hiện (bài 51).
- 2026-10-05 · Đợt 5 bài Chương 4 VL10 (id 68–72; Sonnet điều phối; Opus soạn 68, 70, 71, Sonnet soạn 69, 72; Sonnet kiểm chéo; sửa bằng SendMessage cho chính agent soạn; lô 3+2, ~20 lượt agent) → lỗi `chan` còn lại gần như toàn là **bảng/hộp đặt trước quiz dùng lại đúng tình huống/phương án nhiễu của quiz** (bài 71: cả 3 Bẫy) và **đơn vị ngoài `$…$`** (bài 72: ~90 chỗ dù prompt đã nhắc) → trong prompt soạn ghi thẳng: ví dụ trong bảng Bẫy phải KHÁC tình huống quiz đứng sau nó; chạy regex tìm `\$[^$]*\$ ?(m|kg|N|J|W|s)\b` trước khi báo xong.
- 2026-10-05 · Agent soạn có thể "treo" 600 s (stream watchdog) khi ghi file lớn → file nguồn `theory.src.html` vẫn còn trên đĩa; SendMessage "đọc lại và làm tiếp từ đó" là đủ, không phải soạn lại.
- 2026-10-05 · Phương án quiz: nếu phương án nhiễu có "vì…" thì đáp án đúng cũng phải có (hoặc bỏ "vì" ở cả bốn) — dính ở bài 70, 71, 72; bài thực hành có bảng số đo: sai lệch giữa F đưa vào bảng và F mô hình phải nằm trong sai số dụng cụ mà chính bài nêu (bài 72).
- 2026-10-05 · Bảng 2 cột có bất đẳng thức góc (`0^\circ \le \alpha \lt 90^\circ`) gãy dòng ở 375px dù `--kiem-tran` sạch (bài 68) → dùng gạch đầu dòng. "Bay khỏi mép lên 3,4 m" chỉ đúng khi thành thẳng đứng (bài 71) → nêu điều kiện hoặc hỏi tốc độ tại mép.
- 2026-10-06 · Thêm video thí nghiệm bằng cách chèn tay vào `theory.src.html` + `theory.html` + `bundle.json` (bài Giao thoa, commit `a614821d2`) là **3 chỗ phải sửa cho mỗi clip** và không tái dùng được cho bài khác → từ nay ghi `video` vào `tn-*.json` rồi để `scripts/chen-video-thi-nghiem.mts` chèn (một nguồn dữ liệu, chạy lại được, có `--apply` mới ghi).
- 2026-10-06 · Nhúng thẳng `<iframe>` YouTube trong HTML làm mỗi clip kéo theo ~1 MB JS player ngay khi cuộn tới (bài Giao thoa 4 clip) → `ContentHtml.tsx` đổi thành ảnh bìa + nút phát, chỉ nhúng player khi bấm (V5); nội dung HTML trong DB **không phải sửa** vì đổi ở khâu render.
- 2026-10-06 · Video thật thường nhiễu, không có câu hướng chú ý thì học sinh xem mà không rút ra gì → `video.nhin_vao` là trường **bắt buộc** (V2), `thi_nghiem.py` báo lỗi nếu thiếu hoặc dài quá 40 từ.
- 2026-10-06 · Đăng nhiều bài lý thuyết phải gọi `cap-nhat-ly-thuyet.sh` từng bài rồi deploy từng lần → dùng `bash scripts/cap-nhat-ly-thuyet-hang-loat.sh <slug>:<lesson_id> …` (vẫn hỏi từng bài, mặc định `--yes` mới chạy thẳng, ghi nhật ký `scripts/logs/`).
- 2026-10-06 · Clip **mở bài** phải là chỗ riêng chứ không chỉ hộp thí nghiệm (thầy yêu cầu): khai ở `content/thi-nghiem/video-theo-bai.json`, `vi_tri: "mo_bai"` → chèn ngay **trước hộp "Dự đoán trước khi học"** (thấy hiện tượng rồi mới dự đoán, đúng thứ tự bài Giao thoa); clip mở bài không được giải thích cơ chế/lộ đáp án, nếu không là mất luôn câu dự đoán (V7).
- 2026-10-06 · Cờ `--kiem --apply` của `chen-video-thi-nghiem.mts` in "đã ghi" nhưng **không hề gọi `writeFileSync`** — chỉ phát hiện khi đọc lại file sau khi chạy. Mọi script có `--apply` phải kiểm bằng cách đọc lại/`diff` file thật, đừng tin dòng log tự in.
- 2026-10-06 · Ghi lại JSON không giữ kiểu trình bày gốc làm diff loe cả file: `bundle.json`/`tn-*.json` là indent 1 **không** newline cuối, `index.json` là indent 2 **có** newline cuối, và ngay giữa các `bundle.json` cũng khác nhau → dùng helper đọc file gốc để giữ đúng indent + newline (`ghiJsonGiuDinhDang` trong `chen-video-thi-nghiem.mts`).
- 2026-10-06 · Sửa bài 126 (do phiên khác soạn, mất thư mục nguồn) sau phản biện → khi mất nguồn, kéo `body_html` mục `ly_thuyet` từ DB (REST, service key) về `content/lesson-samples/<slug>/theory.html` rồi sửa và đăng bằng `update-ly-thuyet-from-bundle.mts`. Số minh hoạ phải ghi rõ "chưa phải số đo thật"; bài toán mẫu dùng "vòng tương đương" thì nói rõ là mô hình, đừng khẳng định con số khớp thực tế. Dồn công thức ôn lại vào `<details>` để khỏi tăng từ hiện ngay (`lint_do_dai` chỉ đếm phần hiện). `thi_nghiem.py` tự ghi đè `content/thi-nghiem/index.json` mỗi lần chạy → `git checkout` lại nếu chỉ đang kiểm.
- 2026-10-06 · File `scripts/logs/ly-thuyet-bai<N>-backup-*.json` được tạo **trước** nhánh `if (dry) … exit` của `update-ly-thuyet-from-bundle.mts` → chạy xem thử (không `--yes`) cũng sinh backup. **Không dùng sự tồn tại của backup để kết luận bài đã ghi DB**; muốn biết chắc thì đọc log ghi thật (`scripts/logs/dang-*.log`, dòng `… ok`) hoặc đọc lại `body_html` trong DB.
- 2026-10-06 · Rà 20 bài L11 bằng 5 agent `kiem-code`: lỗi lặp ở nhiều bài mà lint không bắt → (a) quiz thiếu câu hỏi (`l11-mo-ta-song`, `l11-tat-dan-cuong-buc`, `l11-luc-coulomb`): trước mỗi `.tl-quiz` phải có một `<p>` đề, đối chiếu `bundle.json` → `exam.questions`; (b) vai "thầy" lọt (`l11-giao-thoa-song`, `l11-dao-dong-dieu-hoa`): tìm bằng `grep -i 'thầy'` KHÔNG dùng `\b` (không khớp chữ có dấu); (c) bảng "Bẫy" dùng đúng số/tình huống của quiz đứng sau → lộ đáp án: đổi ví dụ trong bảng; (d) đáp án đúng dài nhất, đơn vị ngoài `$…$`, nhãn SVG <13, bảng 3 cột gãy ở 375px, bảng số "đo" sinh từ mô hình mà không ghi "số liệu minh hoạ". Nên thêm các kiểm này vào `lint_theory.py`/`check_quizzes.py`.
- 2026-10-06 · Sửa 20 bài L11 sau kiểm chéo: hình/chú thích/bảng "Bẫy"/hộp "Rút ra" có chữ trùng đáp án quiz đứng sau → đặt SAU quiz (`<details>`) hoặc đổi ví dụ, đừng viết lại quiz; hình mở bài chỉ vẽ cảnh, không ghi kết quả. Thêm "vì" vào phương án làm tăng từ hiện ngay → chạy `lint_do_dai.py` sau mỗi đợt sửa (bài sát trần 2500 dễ chạm lỗi cứng). Gộp đơn vị ngoài `$…$` bằng regex chỉ an toàn ở bài ít chữ (sóng: 49/73 chỗ); bài nhiều chữ tiếng Việt dễ nhầm ("J đưa") → viết đúng `\ \text{..}` ngay từ lúc soạn thay vì sửa sau. Bài không có `build_bundle.py` phải cập nhật `bundle.json` bằng tay → bài mới nên có sẵn script đóng gói.
- 2026-10-06 · Rà 18 bài L12 bằng 6 agent `kiem-code`, sửa bằng 6 agent `general-purpose` (mỗi nhóm 3 bài, thư mục riêng nên không đụng nhau): lỗi lặp mà lint không bắt → (a) **số liệu thí nghiệm ngược chiều lời giải thích sai số** (bài Nội năng: c đo 4093 < 4180 nhưng "Rút ra" nói mất nhiệt làm c cao hơn) — tính trung bình rồi so với giá trị chuẩn trước khi viết "Rút ra", sửa luôn file `tn-*.json`; (b) **phản hồi của phương án nhiễu tính sai** (bài Thực hành nhiệt: 3/3 nhiễu giải thích bằng phép tính không ra số đã ghi) — chọn nhiễu theo lỗi thật rồi tính lại bằng script; (c) **mũi tên SVG đảo chiều so với nhãn** (bài Nội năng: cả 4 hình) — kiểm `y1`/`y2` của `<line marker-end>`, không chỉ nhìn "có mũi tên"; (d) **vẽ từ trường/vòng dây không đúng mặt phẳng** (bài Ứng dụng cảm ứng: B nằm trong trang thì từ thông = 0) — B vuông góc tấm thì vẽ ⊗/⊙; (e) đáp án dồn A/B lặp lại ở hầu hết bài mới (có bài 8/8 là A) — chạy kiểm trước khi giao; (f) số phút ở khung Mục tiêu lệch `lint_do_dai.py` (13 vs 18) — ghi theo số lint đo; (g) bài soạn trước chuẩn 2–4/10 (`l12-cam-ung-dien-tu`) còn vai "thầy" và thiếu mục bắt buộc → `grep -n thầy` và đối chiếu "Dàn ý" trước khi coi là xong.
- 2026-10-06 · Xáo đáp án quiz bằng hàm đọc/ghi lại từng dòng phương án thì id không lệch; phần phải sửa tay là **chữ cái trong phản hồi sai** (`tl-fb--no`) và `bundle.json`; `id` phương án viết thường (`q3b`) còn chữ hiển thị viết hoa (`B.`) — regex đổi chữ nhớ cả hai. Đổi số hình chỉ cần đổi chữ "Hình N." trong chú thích ở `build_figs.py`, không đổi mốc `<!--FIGn-->`. Lint "đoạn liền" tính cả chữ trong `<details>` dài → tách `<details>` ngắn thay vì bỏ lồng. Thêm bảng/đoạn vào bài sát trần 2500 từ thì phải cắt chỗ khác.
- 2026-10-06 · Hai phiên cùng soạn một bài (`l12-ung-dung-cam-ung`) → `main` đã có bản riêng, merge ra 10 file xung đột add/add. Trước khi soạn bài mới: `git fetch && git log origin/main -- content/lesson-samples/<slug>`; merge vào `main` khi working tree đầy WIP thì dùng `git worktree add <thư mục> main` + `git merge`, không `checkout main` (bị chặn vì file dở trùng file đã có trong `main`).
- 2026-10-06 · `thi_nghiem.py` ghi đè `content/thi-nghiem/index.json` và làm rơi các mục của bài khác (thiếu 10 mục) → chạy xong phải `git diff` index.json, khôi phục nếu mất mục; bài mới (`l12-ung-dung-cam-ung`) vẫn thiếu 5 mục `udcamung` trong index. Số liệu "đo" cần kiểm độ thực tế vật lí (vòng khói NH₄Cl "12 s ở 24 cm" không thực), không chỉ kiểm bảng khớp JSON; ghi rõ "số minh hoạ".
- 2026-10-06 · Rà + sửa 25 bài L10: `build_figs.py`/`build_thi_nghiem.py` tự ghi lại `content/thi-nghiem/tn-*.json` của bài → muốn sửa số/chữ trong JSON thì sửa chuỗi trong script rồi build, không sửa tay JSON (sẽ bị ghi đè); build xong `git diff content/thi-nghiem` kiểm chỉ khác chỗ định đổi.
- 2026-10-06 · Số phút ở khung Mục tiêu bị `round()` kiểu banker (16,5 → 16, lệch lint đo 16,5) → làm tròn LÊN (`math.ceil`/`int(x+0.5)`), rồi so với `lint_do_dai`.
- 2026-10-06 · Agent kiểm tay báo "số liệu lệch quy luật" (bảng công cơ học, 0,56 N → 0,54 N) nhưng SAI: tính lại bằng đúng mô hình + độ chia dụng cụ của chính bài thì số cũ đúng → trước khi sửa số bị báo lệch, tính lại bằng mô hình trong `tn-*.json` (có `mo_hinh`/μ/độ chia); và sau mỗi lượt sửa luôn cho một agent `kiem-code` soát độc lập (lượt này bắt thêm 3 lỗi do chính lượt sửa tạo: sai tham chiếu "mục I", phản hồi quiz nhắc sai phép tính, SVG còn nhãn <14px).
- 2026-10-06 · Ví dụ "xưởng cơ khí/CNC" (máy tiện, phay, mài, phôi, cầu trục, máy hàn, cờ lê lực, thước cặp…) lẫn vào ~50 bài L10–L12 (mở bài, bài toán mẫu, quiz, hình SVG, `tn-*.json`) → phải thay hàng loạt bằng 7 agent. Quy tắc: ví dụ, tình huống, số liệu và nhãn hình phải là thứ HS 15–18 tuổi gặp hằng ngày (xe đạp/xe máy, thang máy chung cư, máy giặt, bếp từ, nồi cơm, sân bóng, siêu thị, cầu trượt…); không mượn bối cảnh xưởng/công nghiệp mà HS chưa có khái niệm. Giữ "nhà máy điện/thuỷ điện/hạt nhân" khi đó là nội dung bài. Sau khi soạn: `grep -riE "xưởng|CNC|phôi|cầu trục|máy tiện|cơ khí"` trong `theory.src.html`, `build_*.py`, `bundle.json`, `content/thi-nghiem/` phải rỗng. Khi thay tình huống: sửa NGUỒN (`theory.src.html`/`build_*.py`), tính lại số–đáp án–phương án nhiễu–hình, rồi build lại.
