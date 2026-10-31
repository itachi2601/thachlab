---
name: soan-bai-ly-thuyet-tuong-tac
description: Soạn bài LÝ THUYẾT tương tác thachlab theo phong cách thầy Thạch (tình huống mở bài, dự đoán trước khi học, từ khoá, thí nghiệm Làm–Quan sát–Rút ra, bẫy, quiz tự chấm, Trả bài, bài toán mẫu, thử thách ⭐), hình SVG tự vẽ, đóng gói theory.html + bundle.json. Dùng khi thầy nói "soạn bài lý thuyết tương tác", "làm bài học mới cho chương X", "vẽ hình cho bài lý thuyết". KHÁC dang-bai-hoc-thachlab, soan-quiz-ly-thuyet. ĐĂNG DB chạy trên Mac.
---

# Soạn bài lý thuyết tương tác

## Mục đích (thầy xác nhận 1/10/2026)

Không phải video bài giảng. Đây là **bài đọc lý thuyết có tương tác**, dùng được cả hai cách: (1) thầy **chiếu và giảng trực tiếp** trên lớp, mỗi lần bấm `<details>`/chọn đáp án là một nhịp giảng; (2) học sinh **tự xem lại** ở nhà, nên mọi lời giảng quan trọng phải nằm trong bài chứ không chỉ trong lời thầy nói.

Ba thói quen dạy của thầy, bài nào cũng phải có đủ:
1. **Mỗi kiến thức cần nhớ đi kèm một ví dụ hoặc thí nghiệm thực tế.** Không có gạch đầu dòng kiến thức nào đứng trơ. Thí nghiệm viết theo ba bước Làm – Quan sát – Rút ra (`.tl-box--exp`); ví dụ ngắn thì viết ngay trong gạch đầu dòng.
2. **Trả bài trước khi giải bài tập.** Một mục `<h3>` "Trả bài" gồm 4–6 câu hỏi nhớ lại (phát biểu, công thức + ký hiệu, đặc điểm, điểm dễ nhầm, công thức suy ra từ đâu), mỗi câu một `<details>` (không kèm dòng nhắc, tiêu đề câu hỏi tự nói rõ việc cần làm). Mục này đứng **trước** bài toán mẫu.
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

**Lưu mốc sau mỗi chặng (thầy chốt 17/10/2026 — phiên có thể dừng giữa chừng vì hết hạn mức, container cloud có thể bị thu hồi):**
- Xong mỗi chặng (viết `theory.html`, vẽ hình, kiểm, sửa, đóng gói) → `git commit -- content/lesson-samples/<thư-mục-bài>/ …` ngay; phiên cloud thì **push** luôn. Chưa ghi DB không có nghĩa là an toàn: file chưa commit mất là mất cả bài.
- Kiểm xong (lint, kiem-code, xem ảnh) → ghi danh sách lỗi ra `content/lesson-samples/<thư-mục-bài>/ra-soat.md` dạng `- [ ] <lỗi> — <chỗ>`; sửa xong mục nào tick `[x]` rồi commit cùng bản sửa. Ghi thêm dòng đầu file: chặng hiện tại + bước kế tiếp.
- Phiên sau (hoặc thầy nói "tiếp bài X"): đọc `ra-soat.md` + `git log -3 -- <thư-mục-bài>` thay vì kiểm lại từ đầu hay nạp lại phiên cũ.

1. **Chọn bài + nguồn.** Lớp → Chương → Bài (xem `public/data/catalog.json`). **Soạn lại bài đã đăng thì đọc trước bài đang có trên web (`lesson_items` mục `ly_thuyet`) và mô tả bài/YCCĐ của nó**, liệt kê các ý bắt buộc để bản mới không bỏ sót (bài Mô tả sóng cũ thiếu hẳn phương trình sóng và trễ pha dù mô tả bài có ghi). Nội dung lấy từ chương trình/SGK làm ý tưởng và số liệu; **không chép nguyên văn, không dùng ảnh của sách có bản quyền** (Halliday, SGK...) trên trang công khai — vẽ lại bằng SVG.
2. **Phiếu bài** (trong đầu/scratchpad): 1 ví dụ đời thường mở bài · khái niệm/định luật + phát biểu chuẩn · công thức + ký hiệu + đơn vị · 1–2 **hiểu lầm kinh điển** của học sinh · 1 ví dụ số · 3–4 ứng dụng đời sống. Hiểu lầm kinh điển là xương sống của bài — chọn đúng chỗ học sinh hay sai.
3. **Viết `theory.html`** theo dàn ý dưới + linh kiện trong `references/linh-kien-html.md`.
4. **Vẽ hình** 2–4 hình SVG theo `references/hinh-svg.md`, dùng `scripts/svg_lib.py` (sinh bằng script, chèn idempotent như `build_figs.py` của bài mẫu).
4b. **Ghi thí nghiệm vào kho dữ liệu** `content/thi-nghiem/` (một file JSON cho mỗi thí nghiệm hoặc ví dụ: dụng cụ, các bước, tham số + khoảng giá trị, phương trình, số liệu mẫu, hiểu lầm hay gặp, gợi ý mô phỏng). Đây là dữ liệu nguồn cho giai đoạn **làm mô phỏng** tiếp theo, nên không để thí nghiệm chỉ nằm trong HTML. Gắn `data-exp="<id>"` lên hộp `.tl-box--exp` / `<figure>` tương ứng. Quy ước đầy đủ: `content/thi-nghiem/README.md`.
4c. **Video (clip YouTube thật).** Hai chỗ khai, đều **không viết khối `<div class="tl-box--video">` bằng tay**:
   - **Clip mở bài** (đặt vấn đề bằng hiện tượng thật) → `content/thi-nghiem/video-theo-bai.json`, `vi_tri: "mo_bai"`; script chèn ngay trước hộp "Dự đoán trước khi học" của mục I. Clip chỉ quay hiện tượng, không giải thích cơ chế, không lộ đáp án (V7).
   - **Clip của từng hộp thí nghiệm** → field `video` trong chính `tn-*.json` đó (`youtube_id`, `nhin_vao` bắt buộc ≤ 25 từ, `giay_bat_dau`/`giay_ket_thuc` ≤ 90 giây); `vi_tri` cũng nhận `truoc:<data-exp>`/`sau:<data-exp>` cho mốc bất kỳ.
   **Tìm ứng viên:** `python3 scripts/tim-clip-youtube.py "từ khoá 1" "từ khoá 2"` (cào trang kết quả YouTube + kiểm oEmbed, in id | tiêu đề | kênh). Không dùng WebSearch để tìm clip — nó không trả link YouTube. Script chưa xem nội dung clip: ghi vào bảng `video-de-xuat-*.md` cho thầy soát V1–V7, đừng tự tick.
   **Khái niệm TRỪU TƯỢNG (thầy chốt 16/10/2026):** khi bài có đoạn lý thuyết khó hình dung (sóng, trường, dao động, nhiệt, cảm ứng…), ngoài clip thí nghiệm, tìm thêm clip giải thích trực giác ở playlist **Crash Course Physics** TRƯỚC (danh mục tập + quy trình cắt mốc bằng phụ đề: `references/video-crash-course-physics.md`), rồi mới dùng `tim-clip-youtube.py`.
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
| IV. Trả bài | 5–6 câu nhớ lại lý thuyết/công thức, chưa giải bài; mỗi câu là một `<summary>` không kèm chữ nhắc | `<details>` trong hộp `tl-box--think` |
| V. Bài toán mẫu | Đề bài → bảng *Câu trong đề / Dữ liệu / Kiến thức liên quan* → lời giải từng bước → kiểm tra kết quả → **một bài để trống 1–2 bước cho học sinh điền** → **biến thể** (đổi số, đổi chiều, đổi vị trí điểm) | `.tl-table--data` + `.tl-steps` + hình + quiz |
| VI. Đời sống + tổng kết | 3–4 ứng dụng; **thử thách phân tầng ⭐ ⭐⭐ ⭐⭐⭐**; khung "Mang về sau bài học" dạng chuỗi từ khoá (có ý về cách đọc đề) | `<details>` + hộp định nghĩa |

**Hộp thí nghiệm có tên trong chương trình** (Rutherford, Joule, Boyle, Faraday, đo nhiệt dung riêng…) viết theo khung 6 ô
Giả thuyết → Dự đoán nếu đúng → Dụng cụ & cách đo → Quan sát → Rút ra → Chưa nói được gì, đúng thứ tự đề TN THPT hỏi;
kết quả không lộ trước hộp Dự đoán; quiz sau hộp kiểu "phát biểu nào sai" trộn hiện tượng–kết luận–cơ chế–giới hạn.
Quy tắc T1–T12 + checklist: `docs/QUY-TAC-THI-NGHIEM-TRONG-BAI.md` (thử nghiệm đầu: L12 Bài 14, 25/10/2026).

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
   - *(Đang thử từ 13/10)* Ngay sau hộp dự đoán, trước mục II: khối **🧰 Kiểm tra hành trang** — 2–3 quiz về kiến thức CŨ bài sẽ dùng + `<details>` Nhắc nhanh. Soạn `content/hanh-trang/<slug>.json` rồi `python3 scripts/chen-hanh-trang.py --bai <slug> --apply` (không viết tay). Lý do + giới hạn: `docs/PHUONG-PHAP-NOI-DUNG-LY-THUYET.md` §4.2b.
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
- **Mẹo chữ đơn** (thêm 26/10/2026): kiến thức có cấu trúc đếm được (3 nội dung, 4 giả thiết…) thì cô thành mẹo 2–4 chữ đơn, mỗi chữ mở đầu một gạch đầu dòng (ví dụ `NHỎ – LOẠN – ĐẬP`); ý phụ là hệ quả của một chữ thì lồng làm gạch con dưới chữ đó, ghi "Hệ quả của NHỎ: …" để học sinh không đếm thành ý thứ tư. Chỉ dùng khi chữ đơn tự nhiên, không ép vần; không dùng được thì giữ dòng từ khoá 3–6 chữ như cũ. Không giữ cả mẹo lẫn dòng từ khoá cũ (N7).
- **Khung "Mang về" = "Nhớ N hình = nhớ cả bài"**, N ≤ 5 (G1): mỗi dòng ≤ 10 từ, một hình ảnh cụ thể đã có trong bài (thí nghiệm, so sánh, vật đời thường) → đúng một mục kiến thức; dòng "Đọc đề: …" giữ ở cuối. Hình ảnh phải được **đặt tên ngay tại mục đó** (nhãn hộp thí nghiệm, câu "Hình dung…") để học sinh đọc lại bài tìm thấy. Mẫu: `l12-thuyet-dong-hoc-phan-tu`.
- **Dòng 🧠 mẹo trên 🔑** (thầy chốt 26/10/2026, thay hai điểm của gạch "Mẹo chữ đơn" ở trên: **giữ** dòng 🔑 ngay dưới mẹo; **hoa chữ đầu**, không HOA cả dòng): mục có 3–5 ý song song → thêm dòng 🧠 mẹo 3–5 chữ đơn, đậm, hoa chữ đầu, đặt trên 🔑 — `<p class="tl-meo">🧠 <b>Nhỏ – Loạn – Đập</b></p>` rồi `<p><strong>🔑 …</strong></p>`; chữ mẹo lặp ở Trả bài và Mang về; tra `docs/BANG-MEO-TU-KHOA.md` trước khi đặt mẹo mới, cùng ý thì dùng cùng chữ (và ghi mẹo mới vào bảng); cuối Mang về có dòng 'N hình = cả bài'. Quiz ngay sau hỏi đúng ý mà chữ mẹo gợi đáp án → dời khối mẹo + 🔑 xuống sau quiz. Mẹo ≤ ~28 ký tự để nằm một dòng ở 375px (CSS `.tl-meo` 1.05rem).

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

## Làm nhiều bài một đợt / chọn mô hình

Soạn ≥2 bài một đợt hoặc thuê subagent → đọc `references/lam-nhieu-bai.md` (subagent song song, brief, kiểm chéo, bảng chọn mô hình Claude). Soạn một bài thì bỏ qua.

## Khối trình bày vùng đọc (thầy duyệt 26/10/2026 — lấy từ cách Apple trình bày, CSS sẵn trong `app/globals.css`)

Chỉ HTML + CSS, không JS, lọt qua DOMPurify. Bài cũ chưa có thì vẫn hiển thị bình thường.
1. **Câu chốt đầu mục** (N5, G3): ngay sau `<h3>` thêm `<p class="tl-claim">Đang chuyển thể thì nhiệt độ đứng yên.</p>` — một câu
   kết luận ≤ 12 chữ, lấy từ từ khoá 🔑 của mục. Có câu chốt thì `<h3>` tự thu thành nhãn nhỏ in hoa.
2. **Mỗi đoạn một chỗ in đậm** (N7): kiểm bằng `npx tsx scripts/kiem-dam-moi-doan.mts <file>` (thoát mã 1 khi vi phạm). Nhãn đầu
   dòng `<strong>Rời:</strong>`, dòng 🔑, ô quiz không tính.
3. **Ô "Số cần nhớ"** (L1, truy xuất): `<div class="tl-nums"><details class="tl-num"><summary>Nước đá tan</summary><p>0 °C</p></details>…</div>`
   — số bị che, học sinh nhớ rồi bấm. 2–4 ô, chỉ hằng số/ngưỡng thật sự phải thuộc.
4. **Bảng đặt cạnh nhau cho bẫy**: `<table class="tl-table tl-cmp">`, hàng = tiêu chí (`<th>` đầu hàng), ô khác nhau `<td class="tl-diff">`.
   ≤ 3 cột để vừa 375px.
5. **Nhịp mục**: tự động (CSS) — giữa hai mốc `<h3>` cách ~56px. Không chèn `<br>`/đoạn rỗng để tạo khoảng.
6. **Thuật ngữ mở tại chỗ** (N8): `<span class="tl-term"><input type="checkbox" id="tl<lớp>b<bài>-t1"><label for="…">ngưng tụ</label><span class="tl-def">định nghĩa 1 câu</span></span>`.
   Chú thích số mũ CHỈ cho nguồn/điều kiện đo: `<sup class="tl-fn"><a href="#tl-fn-1">1</a></sup>` + cuối bài `<ol class="tl-fns"><li id="tl-fn-1">…</li></ol>`.
   **Nguồn ảnh (OpenStax, Commons…)**: `</figure>` LIỀN `<ol class="tl-fns">` (code dựa vào đó: ≥1280 đưa nguồn ra cột lề ngang đầu hình,
   màn hẹp và hình trong `.tl-box`/`.tl-trap` thì nằm dưới hình). Số mũ dẫn tới nguồn ảnh
   chỉ gắn khi có `<p>` cấp đầu đứng SÁT hình (không chen danh sách/hộp/công thức); không gắn ở dòng 🔑, đoạn xa, hay ngoài `<details>`
   chứa hình — không có chỗ sát thì bỏ số mũ (`_margin_fig.py` đã làm vậy). Ảnh là một ô của hình sách → ghi số kèm ô (14.11a).
7. **Cột lề phải ≥ 1280px** (tự động, `features/lessons/margin-notes.ts`): thuật ngữ, chú thích số nằm trong một `<p>` ở cấp đầu
   (không trong `.tl-box`/quiz/bảng) và `.tl-nums` đặt NGAY sau đoạn nó thuộc về thì lên lề, ngang đoạn đó. Trong hộp thì giữ
   như mục 6. Mỗi đoạn tối đa ~2 ghi chú + 1 ô số, định nghĩa ≤ 1 câu, để cột lề (140–240px) không dài hơn đoạn.

## Nhật ký rút kinh nghiệm (bắt buộc cập nhật cuối MỖI phiên dùng skill này — xem `AGENTS.md`)

Nhật ký đầy đủ (120+ dòng từ 2/10/2026) ở `references/nhat-ky.md` — **không đọc hết**. Trước khi soạn, tra đúng việc:
`grep -n "<chương|tên bài|svg|quiz|build_figs|agent…>" .claude/skills/soan-bai-ly-thuyet-tuong-tac/references/nhat-ky.md`.
Cuối phiên, thêm vào CUỐI `references/nhat-ky.md` mỗi bài học một dòng `- YYYY-MM-DD · <sự cố/phát hiện> → <cách làm đúng>`; nếu bài học làm
một bước phía trên sai/thiếu thì sửa luôn bước đó trong SKILL.md (quy tắc áp cho mọi bài phải nằm ở phần trên, không chỉ trong nhật ký). Phiên không có bài học mới thì ghi "không có bài học mới" trong câu trả lời.
