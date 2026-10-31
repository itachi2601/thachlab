---
name: ra-soat-bai-hoc
description: Rà soát nội dung + hình SVG các bài lý thuyết thachlab ĐÃ SOẠN theo lô một chương (1–6 bài) — mỗi bài một agent Opus song song tính lại số liệu/quiz, sửa lỗi chắc chắn, chụp từng hình 375px, chấm đạt/chưa đạt, vẽ lại hình chưa đạt trong build_figs.py; phiên chính kiểm diff + số mũ nguồn ảnh, agent kiem-code soát độc lập hình vẽ lại, commit từng bài, gửi ảnh cho thầy duyệt, đặt lịch đăng (cap-nhat-ly-thuyet.sh) ngoài giờ học sinh. Dùng khi thầy nói "kiểm tra lại nội dung bài học chương X", "vẽ lại các hình SVG chưa đạt", "rà hình bài X", "soát lại chương 4 lớp 12", "/ra-soat-bai-hoc". KHÁC cap-nhat-bai-hoc-theo-gemini (học sinh ảo góp ý sư phạm, bài tập mẫu), cap-nhat-thi-nghiem-l12 (chỉ phần thí nghiệm), soan-bai-ly-thuyet-tuong-tac (soạn bài mới). Rà + vẽ + commit chạy được trên cloud nếu có Chrome; ĐĂNG DB chạy trên Mac.
---

# Rà soát nội dung + vẽ lại hình SVG theo chương

Quy trình rút từ đợt Chương 4 L12 (30/10/2026: 5 bài, 10/21 hình vẽ lại, 4 lỗi nội dung). Nguồn quy tắc, không chép lại:
`.claude/skills/soan-bai-ly-thuyet-tuong-tac/references/hinh-svg.md` (quy ước hình), mục 20/23/27 của
`.claude/skills/soan-bai-ly-thuyet-tuong-tac/SKILL.md` (không `$` trong SVG, kiểm bằng toạ độ, số hình theo thứ tự),
`docs/QUY-TAC-THIET-KE.md` (UI học sinh).

## 0. Chốt phạm vi (phiên chính, vài lệnh)
- `git fetch origin && git merge origin/main`. Một lượt = một chương, ≤ 6 bài (nhiều hơn thì chia lượt).
- Tìm thư mục bài: `grep -l '"chapter_title": "Chương N' content/lesson-samples/l1?-*/bundle.json` (không phải bài nào cũng có `chapter_title` — đối chiếu tên bài).
  Mỗi bài cần `theory.src.html` (mốc `<!--FIGn-->`) → `build_figs.py` → `theory.html` → `build_bundle.py` → `bundle.json`.
- Ghi lại số `<sup class="tl-fn">` của mỗi bài ở HEAD (bước 3 cần): `git show HEAD:<bài>/theory.html | grep -o 'tl-fn"' | wc -l`.

## 1. Thuê agent — mỗi bài một agent, song song
- `Agent` `general-purpose`, `model: opus` (SVG là chỗ hay sai nhất), gửi cùng một tin nhắn để chạy song song.
- Prompt = brief trong `prompts.md` (chép vào scratchpad, điền đường dẫn) + một dòng "Bài của bạn: <thư mục> (<tên bài>)". **Kiểm prompt có nội dung thật trước khi gửi** — đợt đầu lỡ gửi chữ giữ chỗ, phải dừng agent.
- Thư mục bài tách biệt nên không giẫm nhau; cấm agent sửa file dùng chung (`svg_lib.py`, `_margin_fig.py`), commit, ghi DB.
- Agent treo "stalled 600s" là chuyện thường (4/5 lần đầu): `SendMessage` tới agent đó "tiếp tục từ chỗ dở, kiểm git diff -- <bài>" — không thuê lại. Mac không có lệnh `timeout`; dặn đặt timeout bằng tham số Bash.

## 2. Tiêu chí chấm hình (agent áp, kiem-code soát lại)
- **Vật lí, kiểm bằng toạ độ trong build_figs.py**: chiều mũi tên/lệch tia, số hạt vẽ khớp nhãn, trục tuyến tính (hoặc log đúng công thức), chấm dữ liệu trên đường, tỉ lệ độ dài vectơ.
- **Cỡ chữ**: `font-size` ≥ 14 trong viewBox 420–440 (12 → chỉ ~9–10 px ở 375 px; đây là lỗi số 1 của đợt đầu). Không nhãn chồng nét/chồng chữ, không cắt mép, caption còn.
- **Quy ước**: đầu mũi tên V 30° (`chevron`/`arrow`, không `marker-end` tam giác), đường sức nét đứt, marker id có tiền tố riêng, mỗi ý chú thích một dòng (không nối "·", ";"), ≤ ~8 phần tử có nhãn.
- **Nhãn đại lượng đúng loại**: nguyên tử ≠ hạt nhân, liều /năm ≠ liều một lần, trung bình ≠ tức thời.
- **Thẩm mỹ**: hình "que" sơ sài, khoảng trắng thừa lớn, bố cục lệch → chưa đạt.
- Ảnh `<img>` (OpenStax, Commons) không vẽ lại — chỉ soát caption/nguồn khớp ảnh. Bản xem thử cục bộ không hiện ảnh `/assets/...` là bình thường.

## 3. Phiên chính kiểm khi agent báo về (không đọc ảnh ở phiên chính)
- Diff ngoài hình đúng phạm vi: `git diff -- <bài>/theory.html | grep '^[-+][^-+]' | grep -vc '<svg\|<figure\|figcaption\|</svg>'` — khác 0 thì phải khớp đúng các sửa nội dung agent báo.
- **Số mũ nguồn ảnh không mất**: đếm `tl-fn"` so với bước 0. Chạy lại `build_figs.py` làm mất `<sup class="tl-fn">` khi hình không có `<p>` ngay trước (`_margin_fig.py`) → chèn lại tay vào `theory.html` rồi `build_bundle.py`.
- Chỗ agent ghi "nghi ngờ, chưa sửa": tự đọc dòng đó (grep, vài dòng quanh), sửa ngay nếu chắc (sửa CẢ `theory.src.html` và `theory.html`, rồi `build_bundle.py`); còn lại đưa thầy quyết.

## 4. Soát độc lập hình vẽ lại
- Một agent `kiem-code` (khác agent vẽ — agent vẽ tự chấm "đạt" cả hình còn chữ 9 px): danh sách đường dẫn `xem-thu/fig-*.webp` + `build_figs.py`, tiêu chí mục 2, trả bảng ĐẠT/CHƯA ĐẠT kèm toạ độ.
- Hình CHƯA ĐẠT → `SendMessage` về đúng agent đã vẽ bài đó (còn ngữ cảnh) với lỗi cụ thể. Hình sửa vòng 2 nhiều → cho kiem-code soát lại vòng 2; ít thì ghi rõ "vòng 2 chưa soát độc lập" trong báo cáo.

## 5. Commit từng bài, ngay khi bài đó đạt
- `git add <bài> && git commit -- <bài>` (gồm `xem-thu/` mới sinh). Thông điệp: hình nào vẽ lại vì lỗi gì, sửa nội dung gì, "chỉ ở repo, CHƯA đăng DB", mã quy tắc.
- Xong hết: thêm Nhật ký (mục 8), `git fetch && git merge origin/main`, push (nhánh `claude/*` tự gộp main).

## 6. Thầy duyệt
- `SendUserFile` các `fig-*.webp` đã vẽ lại (display `render`, caption ghi thứ tự bài · hình). Kèm bảng ngắn: bài · hình · lỗi · đã sửa; các chỗ nghi ngờ cần thầy chốt.
- Đánh số bài theo `lesson_title` trong `bundle.json`, đừng theo thứ tự thư mục (đợt đầu báo nhầm Bài 15/16).

## 7. Đăng (chỉ khi thầy chốt; mặc định ngoài giờ học sinh làm bài)
- `lesson_id`: tra memory `docs/memory/project_*.md` của chương; không có thì tra DB chỉ đọc. Bước dry-run của script in tiêu đề — lệch thì dừng, không đoán id.
- Lệnh, mỗi bài: `bash scripts/cap-nhat-ly-thuyet.sh <bài>/bundle.json <lesson_id> --yes` (chỉ ghi mục `ly_thuyet`; không dùng `upload-lesson.mts`).
- Thầy hẹn giờ (vd "sau 22h") → `mcp__scheduled-tasks__create_scheduled_task` với `fireAt`, prompt tự đủ: pull main, kiểm `tl-fn`, đăng từng bài, dừng khi lỗi, `curl -s https://thachlab.id.vn/data/lessons/<id>.json | grep -c '<chuỗi chỉ bản mới có>'` (chọn chuỗi trong hình vẽ lại, kiểm trước bằng grep `bundle.json`), bài có bản tĩnh còn cũ → `bash scripts/deploy.sh`, ghi `docs/STATE-archive.md`. Báo thầy: chế độ quyền của lịch, và app phải mở lúc đó.
- Phiên cloud: không đăng được — in khối lệnh cho thầy chạy trên Mac.

## 8. Cuối phiên
- Memory: sửa `docs/memory/project_*.md` của chương (commit, việc treo, lesson_id, chỗ nghi ngờ chưa chốt).
- Nhật ký bên dưới: lỗi mới gặp → quy tắc làm đúng. Không có gì mới → ghi "không có bài học mới".

## Nhật ký rút kinh nghiệm
- 2026-10-30 · Đợt đầu (Ch.4 L12, 5 bài): 10/21 hình chưa đạt, lỗi chữ nhỏ chiếm đa số; 4 lỗi nội dung (số hình sai thứ tự, "hạt nhân" thay "nguyên tử" He-4, phản hồi quiz khen phương án sai, nhầm liều kỹ thuật viên với liều điều trị); kiem-code bắt thêm 4 hình agent vẽ tự cho là đạt → giữ bước 4 bắt buộc.
- 2026-10-30 · Đợt 2 (Ch.2 L11, 8 bài, 2 lượt 6+2 — mở lượt 2 ngay khi có agent xong): lỗi dồn đáp án quiz vào chữ B (2 bài) và "Mang về: N hình" lệch số hình thật (2 bài) → thêm vào việc rà của agent; bài có `svg_lib.py` cũ trong thư mục (không chevron, marker thiếu defs → mũi tên mất đầu) thì import svg_lib của skill; bài không có `build_bundle.py` → thay riêng trường `theory_html`, giữ `indent=1` cho diff gọn; bài không đổi nguồn → `git restore` xem-thu/ thay vì commit ảnh chụp lại.
- 2026-10-30 · Đợt 3 (Ch.5–7 L10, 6 bài): 18/20 hình SVG "chưa đạt" chỉ vì `build_figs.py` từng bài có `defs()/arrow()` riêng dùng `marker-end` tam giác → bước 0 chạy `grep -l 'marker-end' <bài>/theory.html` để báo agent sửa hàm `arrow` một lần (thân + `chevron`), đừng chấm từng hình. `build_figs.py` (Bài 29) ghi đè `content/thi-nghiem/tn-*.json` làm mất trường `video` → dặn agent `git diff -- content/thi-nghiem` sau build, restore nếu đổi. kiem-code đọc ảnh báo "hai xe khác bán kính" sai (toạ độ vốn đúng) → lỗi vật lí kiem-code nêu từ ảnh: agent vẽ đo lại bằng toạ độ + thêm assert trước khi vẽ lại.
- 2026-10-30 · Ch.1 L11 (6 bài, 19 hình SVG): 14 hình vẽ lại, 1 lỗi vật lí (Bài 6 Hình 1: ghế xích đu đang đi LÊN trong khi bài nói "nhún lúc đi xuống") + 2 câu trỏ số hình cũ sau khi Hình 3 đổi thành ảnh OpenStax; kiem-code bắt 2 hình xích đu người que chồng nét (nhãn chạm chân, đùi song song mặt ghế thành chữ Z) mà `kiem_nhan` của agent chỉ kiểm tâm ghế → hình có người: kiểm nhãn phải tính cả hông/gối/bàn chân; chiều chuyển động trong hình phải đối chiếu lời văn mở bài. Chương có 7 bài → chia lượt, Bài 1 (build.py, không có build_figs.py) để lượt sau. Vòng 2 của 2 hình xích đu chưa soát độc lập.
- 2026-10-30 · Ch.4 L10 (5 bài, 22 hình): 14 hình vẽ lại, nội dung chỉ 1 lỗi gọi tên (0° gọi là góc nhọn). Agent tách dòng "Nhãn: F lực · d dịch chuyển" của ảnh OpenStax thành 2 dòng nhưng bỏ tiền tố "Nhãn:" → `_margin_fig.py` không còn nhận ra legend, mất dòng "Nhãn trong hình" ở lề (số mũ vẫn khớp nên kiểm `tl-fn` không bắt được) → bước 3 kiểm thêm `git diff -- <bài>/theory.html | grep "^-.*Nhãn trong hình"`; tách dòng legend thì giữ "Nhãn:" ở dòng đầu. kiem-code bắt 2 hình agent tự chấm đạt (lực đặt lệch tâm ván 13 px, chữ "s" không có đoạn đo).
- 2026-10-30 · Rà lại Ch.2 L11 lần 2 (8 agent Opus ≈ 1,07 M token) dù đợt 2 sáng cùng ngày đã rà: chỉ còn 4 hình chỉnh nhẹ + 1 lỗi làm tròn → bước 0 phải `grep -i 'chương N\|<tên bài>' docs/memory/MEMORY.md` + đọc Nhật ký này; chương đã rà thì chỉ quét máy (`grep font-size="1[0-3]"`, `marker-end`) và hỏi thầy trước khi thuê agent. kiem-code bắt chỉ số dưới `tspan font-size=11` mà agent không thấy → quét cỡ chữ phải gồm cả `tspan`.
- 2026-10-30 · Ch.2 L10 (9 bài, lượt 6 + 3, mở bài mới ngay khi có agent xong; brief để ở scratchpad, prompt chỉ trỏ đường dẫn + 1 dòng bài → rẻ, không lỗi chữ giữ chỗ): cả 9 bài dùng `svg_lib.py` cục bộ cũ (marker tam giác) → mọi agent đổi import sang svg_lib skill. 3 lỗi vật lí/hình agent tự bắt (Bài 12 vectơ v không tiếp tuyến quỹ đạo; Bài 9 lời văn "xe máy" mà hình ô tô; Bài 8 vùng diện tích bị đường khác cắt) + kiem-code bắt 1 hình agent tự chấm đạt (Bài 6 cổng quang: tia dọc hướng chạy, xe đâm chân cổng — lỗi cũ không nằm trong diff) và nhãn `v₀` ký tự Unicode (~7 px) → quét cỡ chữ phải tìm cả ký tự chỉ số Unicode `[₀-₉⁰-⁹]` trong SVG, đổi sang tspan 12. 2 bài sai "Mang về: N hình" (lặp lại đợt 2 — giữ việc rà). Góp ý không chặn của kiem-code (caption nhiều ý, bi dính, chân xuyên thân) gửi lại đúng agent còn ngữ cảnh: mỗi bài ~30 giây.
- 2026-10-30 · Ch.4 L11 (5 bài, 19 hình SVG + 1 ảnh OpenStax): cả 19 hình chưa đạt vì cùng một gốc — `svg_lib.py` cục bộ (marker tam giác) + chữ 13 → brief ghi sẵn "đổi import, sửa hàm arrow một lần" nên mỗi agent chỉ ~3 phút, không stall; nội dung 0 lỗi chắc chắn (bài đã qua kiểm 2 vòng 5/10). Agent vẫn để lại trang xem thử `sec-*.html` đã chụp lại (2/5 bài) dù brief dặn → phiên chính luôn `git status -- <bài>` và restore trước commit. Góp ý không chặn của kiem-code (nhãn sát mép, xa đường, thiếu dấu cắt trục) gửi lại agent còn ngữ cảnh ~35 giây/bài.
- 2026-10-31 · Phần còn lại L10/L11 (20 bài: L10 B1–3, B13–22; L11 B1, B16–21; ~150K token/agent, chạy cuốn chiếu 6–7 agent, mở bài mới ngay khi có agent xong; brief để scratchpad nên prompt chỉ 1 dòng). Hầu hết bài vẫn dùng `svg_lib.py` cục bộ (marker tam giác) → brief ghi sẵn "đổi import, xoá file cục bộ". Lỗi lặp lại: "Mang về: N hình" lệch số hình thật (6/20 bài) và chỉ số `tspan` cỡ 11–13: kiem-code tính chỉ số <14 là CHƯA ĐẠT nhẹ → **ghi thẳng ngưỡng chỉ số ≥14 vào brief** (đợt này brief nói "12+", làm 5 vòng sửa chỉ số qua SendMessage, mỗi vòng ~30 giây nhưng đủ 12 bài). Lỗi vật lí agent tự bắt: tỉ lệ vectơ sai (P/N/N′ khác độ dài, F12 dài hơn P ở đèn treo), vật treo trong nước thấp hơn vật ngoài khí. kiem-code bắt thêm: mũi tên lực vẽ đè mặt đất, người que sơ sài (bước đi) mà agent vẽ tự chấm đạt. Chạy `build_figs.py` làm mất `figlead` + số mũ H3 (Bài 13, 20 — agent tự chèn lại bằng script) và ghi đè `content/thi-nghiem/tn-*.json` (Bài 22): dặn `git diff -- content/thi-nghiem` sau build. Bài 20 L10: `theory.html` ở HEAD lệch `theory.src.html` (video đặt sai chỗ) → build từ nguồn tự sửa, nhớ báo thầy. L11 B1 quiz đáp án dồn B → đảo thứ tự phương án trong nguồn; khi đăng phải `cap-nhat-ly-thuyet.sh` (đổi chỗ phương án).
- 2026-10-31 · Ch.3 L12 (8 bài, lượt 6 + 2; 17 hình vẽ lại, ~150K token/agent, kiem-code 2 lượt): brief để scratchpad với ngưỡng chỉ số ≥14 ghi sẵn → 0 vòng sửa chỉ số. Viết brief bằng heredoc không dấu nháy làm shell nuốt các lệnh trong backtick (`git restore`, `git diff`) → dùng `<<'E'`. kiem-code bắt 1 hình agent tự chấm đạt (Hình 5 Trái Đất: đường sức ngoài cắt mép viewBox, vòng L=3,4·RE) và 1 nhãn sai loại ("số đo" gắn lên số liệu minh hoạ không nguồn) → soát phải kiểm cả mép viewBox và nhãn "số đo/thực nghiệm" của dữ liệu tự bịa. Lỗi lặp lại: "Mang về: N hình" lệch (4/8 bài), số hình không theo thứ tự (Bài 15), đáp án quiz dồn B (Bài 15). Thư mục thừa `l12-ung-dung-cam-ung.cu` (trùng tiêu đề Bài 15, nguồn lệch) bỏ qua, chờ thầy xoá.
- 2026-10-31 · Ch.1 L12 (4 bài, 11 hình SVG; 10 vẽ lại, ~150K token/agent, không stall): bước 0 quét máy (`font-size` <14, Unicode chỉ số) đủ để biết chương chưa rà — không cần đọc memory dài. Brief thêm mục "Bổ sung từ các đợt trước" (chỉ số ≥14, Unicode, mép viewBox, "Mang về", quiz dồn chữ, `content/thi-nghiem`, sec-*.html) → kiem-code đạt 10/10 vòng 1, 0 vòng sửa chặn. Lỗi vật lí agent tự bắt: đá chìm dưới mặt nước, bầu nhiệt kế trong viên đá, đoạn rắn/lỏng đồ thị T–t dốc gần bằng nhau (phải 2:1 theo c), mạch điện trở nối vào đáy chữ U (hai chân thừa). Agent lỡ `git restore` cả hình mình vừa vẽ khi dọn xem-thu (Bài 4, tự chụp lại) → dặn: chỉ restore fig KHÔNG nằm trong danh sách hình đã vẽ lại. "Mang về: 5 hình" liệt kê hình không có (Bài 1) — lặp lại lần thứ 5, giữ việc rà.
