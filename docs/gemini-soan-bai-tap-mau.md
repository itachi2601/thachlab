# Gói cho Gemini: skill "soan-bai-tap-mau" (thachlab)

Bạn (Gemini) chỉ cần ĐỌC để hiểu quy trình và phong cách soạn mục Bài tập mẫu. Các đường dẫn `scripts/...`, `docs/...` là file trong repo của thầy, bạn không có — bỏ qua phần chạy lệnh, chỉ lấy quy tắc nội dung (cấu trúc dạng bài, bảng phân tích đề, lời giải theo bước, mô phỏng không lộ đáp số).

---
# PHẦN 1 — SKILL.md


# Soạn Bài tập mẫu có cấu trúc (thầy chốt 6/10/2026)

Mục **Bài tập mẫu** (`lesson_items.kind='bai_tap_mau'`, cột `questions`) thay nội dung cũ bằng các **dạng bài** có cấu trúc. Web (`components/lessons/WorkedQuestionsGrid.tsx`) hiện mỗi dạng: **đề + mô phỏng hiện tượng → tự thử trên giấy → nút "Phân tích đề" (hình dữ kiện + bảng) → "Xem lời giải đầy đủ" → nút "Làm bài tương tự"** (`SimilarBankPractice.tsx`, bốc 3 câu cùng YCCĐ/Dạng từ `question_bank` qua RPC `get_similar_bank_questions`, chấm ngay, "Làm 3 câu khác"). Dạng cũ chỉ có `body_html` vẫn hiển thị bình thường.

Đầu ra: `scripts/data/bai-tap-mau/<lesson_id>.json`. Đăng: `scripts/publish-bai-tap-mau.mts` (Mac, chỉ ghi cột `questions` của đúng mục, tự sao lưu). Skill **không cần DB/key**.

## Phong cách thầy Thạch — đọc `docs/AI-TUTOR.md` mục 9 trước khi viết (nguồn chuẩn, đừng chép lại ở đây)

Áp vào từng dạng:
1. **Bảng phân tích đề mở đầu bằng điều kiện áp dụng** (9.1): hàng ⚠ nêu điều kiện dùng được định luật/công thức (bỏ qua cản, cùng độ cao, chỉ có trọng lực…). Thứ tự kiến thức ở cột 3: khái niệm → định luật → công thức → điều kiện. Cột 3 của hàng "cần tìm" chỉ ghi công thức, không ghi số.
2. **Đọc đề đến đâu, nêu dữ liệu và kiến thức đến đó**: mỗi hàng bảng trích đúng một cụm của đề (như bài toán mẫu trong lý thuyết), ghi dữ liệu kèm đơn vị; chữ ngắn.
3. **Lời giải**: bắt đầu bằng khung "Kiến thức cần gọi lại" (khái niệm → định luật → công thức → điều kiện), rồi giải từng bước đánh số, **kiểm đơn vị/hợp lí của kết quả**, kết bằng 1 dòng "Dạng này nhận ra khi… → làm…" (nhận dạng). Số liệu 3–4 chữ số có nghĩa, ghi đơn vị (9.4 tình huống 1).
4. **Câu khái niệm** thì nói thẳng ngắn gọn rồi khái quát (9.5); **không** hỏi ngược trong lời giải.
5. **Retrieval** (9.3): web đã đặt chữ "gấp lại, tự trình bày từ đầu" trước nút bài tương tự; trong lời giải, dòng cuối nhắc "3 ngày sau che lời giải, giải lại".
6. **Nền trước, kỹ năng sau** (9.2): các dạng trong một bài xếp **từ cơ bản → kết hợp**, dạng sau dùng lại cách làm dạng trước. Dạng khó nhất là dạng 3–4.
7. **KHÔNG dùng vai "thầy/cô"** trong nội dung (feedback 2/10/2026, validator chặn). Giọng trung tính, câu ngắn, đánh số khi nhiều ý, không mở bằng lời khen.

## Mô phỏng dưới đề + Phân tích đề thay gợi ý (thầy chốt 7/10/2026)

Thầy bỏ cách "3 gợi ý mở dần" và bỏ hình động trong gợi ý. Mỗi dạng giờ có:
1. **Mô phỏng hiện tượng nằm DƯỚI đề** (`problem_html` = đề + `<figure>` hình động): quả cầu chạy dọc quỹ đạo TÍNH THẬT từ công thức, kèm dữ kiện ghi trên hình, dấu "?" ở đại lượng cần tìm. Không để lộ đáp số (bài ngược như Dạng 3, 6 chỉ chạy một lần bắn mẫu). Ghi tốc độ phát trong chú thích ("đúng thời gian thật" hoặc "chạy chậm k lần").
2. **`analysis_html` = hình dữ kiện tĩnh + bảng** `.tl-table--data` ba cột *Câu trong đề | Dữ liệu | Kiến thức liên quan*, **mỗi hàng trích một cụm của đề** (đúng cách bài toán mẫu trong bài lý thuyết). Hàng điều kiện áp dụng mở đầu cột 3 bằng **⚠** (AI-TUTOR 9.1) — validator báo lỗi nếu không có ⚠. Hàng "cần tìm" ghi công thức dùng, KHÔNG ghi số.
3. Lời giải đầy đủ như cũ.

Dựng bằng `scripts/hinh.py` (`ngang_geom`, `xien_geom`, `dim`, `arc`, `axes`…) và mẫu `scripts/data/bai-tap-mau/build-hinh-57.py` (`ball()` hình động SMIL, `tbl()` + `ANALYSIS` cho bảng; idempotent). Màu theo `svg_lib.py`: đỏ v · xanh dương vₓ · cam v_y/độ cao · xanh lá quỹ đạo. SMIL: lấy mẫu cách đều thời gian rồi nội suy tuyến tính ⇒ đúng vật lí; ≈ 3 KB/hình, không JS; `ContentHtml` tự bỏ `<animate>` khi bật "giảm chuyển động". **Chạy MỘT lần khi bấm (B4, thầy chốt 7/10/2026)**: mọi `<animate>` có `begin="indefinite" fill="freeze"`, quả cầu có `cx/cy` ban đầu = điểm xuất phát; `hinh.fig()` tự thêm nút `button.bt-run` khi thân hình có `<animate`; `ContentHtml` xử lý bấm: `beginElement()` các `<animate>/<animateTransform>` trong figure rồi đổi nhãn thành "↻ Chạy lại"; giảm chuyển động → bỏ cả `<animate>` lẫn nút. Hình dừng ở khung cuối. Muốn nút tạm dừng/thanh trượt thì phải làm component dùng chung (lazy + `LazyErrorBoundary`). Khi kiểm bằng trình duyệt nhúng: tab phải ở tiền cảnh (`tabs_select` + chụp ảnh), nếu `document.visibilityState==='hidden'` thì SMIL không chạy.
**Xem bằng mắt trước khi đăng** (ghi ra HTML, `python3 -m http.server`, chụp): lỗi hay gặp là nhãn cắt mép, nhãn đè mũi tên/quỹ đạo, thước đo dưới mặt đất thiếu chỗ ở viewBox.

### Lời giải ngắt dòng (thầy chốt 7/10/2026)
Lời giải viết liền khó đọc → mỗi lời giải dựng bằng `sol()` trong `build-hinh-57.py` theo `docs/QUY-TAC-THIET-KE.md` C1/C4/H5/B3/N7: khung "Kiến thức cần gọi lại" (≤ 5 dòng, mỗi dòng một ý) → **mỗi bước một khối** `bt-step` (số + tiêu đề đậm, 1 câu dẫn ≤ 1 dòng, **mỗi công thức một dòng `$$…$$`**, tách "công thức chữ" / "thế số" / "kết quả" thành 3 dòng, kết quả trong ô nền nhạt `bt-ans`) → ô **Đáp số** mỗi ý một dòng → dòng "Nhận dạng" nhỏ, mờ. Khoảng cách trong bước (6–10px) < giữa các bước (22px). CSS ở cuối `app/globals.css` (`.bt-*`). Không viết `<ol class="tl-steps">` liền nhiều công thức trong một dòng nữa. Đã xem ở 375px: không tràn ngang, công thức dài tự cuộn trong dòng.

## Nhân ra nhiều bài (chương)
Mỗi bài một subagent theo `references/huong-dan-nhan-ra.md` (mẫu = bài 57), chạy song song; sau đó **mỗi bài thêm một subagent `kiem-code` khác tự giải độc lập** (không nhìn lời giải) → sửa → `review.checked=true` → phiên chính publish từng bài (`--lesson <id>`, dạng cũ vào `tu_luan` nên KHÔNG dùng `--giu-cu`) rồi deploy một lần. Dạng cũ lấy từ `scripts/dump-bai-tap-mau-cu.mts <id…>` → `scripts/data/bai-tap-mau/old/<id>.json` (chạy trước khi publish ghi đè). Xem thử bằng `scripts/xem-thu.py` (Chrome headless, khung cuối của mô phỏng).

## Quy trình

1. **Chọn bài** (`lesson_id`). Đọc `public/data/lessons/<id>.json` mục `ly_thuyet` (để dạng bài **khớp đúng kiến thức bài đã dạy**, cùng ký hiệu), và mục `bai_tap_mau` hiện có (không để mất ví dụ hay đang có — đưa lại thành 1 dạng nếu tốt). Nếu thiếu `public/data`: `npm ci && node scripts/build-content.mjs`.
2. **Chốt 2–4 dạng** (mặc định thử **1 bài trước**, thầy duyệt rồi mới nhân ra cả chương). Mỗi dạng = một kiểu bài học sinh sẽ gặp lặp lại trong đề (không phải 4 bài số khác nhau của cùng một cách làm). Với mỗi dạng chọn **`topic` = tên YCCĐ con** sát dạng nhất trong `scripts/data/question-topics.json` (đúng `lesson_id` của bài; sao chép nguyên văn). Vì bài tương tự lấy theo YCCĐ, YCCĐ quá rộng → bài lạc dạng; chỉ có chủ đề cha → ghi rõ cho thầy.
   - Soát nhanh ngân hàng trước khi chốt: `topic` đó có bao nhiêu câu `bai_tap` chưa lưu trữ (`select count(*) from question_bank where topic_id=… and form='bai_tap' and not archived`, chạy trên Mac). < 6 câu → báo thầy, vì nút bài tương tự sẽ nhanh hết.
3. **Soạn từng dạng** (rồi dựng mô phỏng + bảng phân tích ở mục trên) (đề riêng, số liệu mới; không chép câu có trong ngân hàng nguyên văn): `problem_html`, `analysis_html` (hình + bảng), `solution_html`. LaTeX `$…$`; `<`/`>` trong công thức viết `\lt`/`\gt`. Hình cần thiết: SVG tự vẽ như bài lý thuyết (`soan-bai-ly-thuyet-tuong-tac/references/hinh-svg.md`), ảnh nén ≤ ~1200px (AGENTS.md "Đăng nội dung").
4. **Kiểm chéo bắt buộc**: giao subagent `kiem-code` đọc lại **từng dạng**, tự giải độc lập (không nhìn lời giải) rồi so; trả đúng/sai/nghi ngờ + lý do. Sai số, đơn vị, hoặc bảng phân tích/mô phỏng lộ đáp số → sửa. Chỉ đặt `review.checked: true` sau bước này.
5. **Validate**: `npx tsx .claude/skills/soan-bai-tap-mau/scripts/validate.mts scripts/data/bai-tap-mau/<id>.json`.
6. **Báo cáo** + in lệnh cho thầy trên Mac (xem mục "Đăng"). Viết "Rút kinh nghiệm" theo AGENTS.md vào Nhật ký cuối file này.

## Dạng file

```json
{ "lesson_id": 57, "lesson_title": "Chuyển động ném", "generated_at": "2026-10-06",
  "review": { "checked": true, "notes": "…" },
  "dang_bai": [ {
    "label": "Dạng 1 · Ném ngang: tìm thời gian bay và tầm xa",
    "topic": "<tên YCCĐ con, nguyên văn>", "form": "bai_tap",
    "problem_html": "<p>…</p>",
    "analysis_html": "<figure …hình dữ kiện…></figure><div class=\"table-scroll\"><table class=\"tl-table tl-table--data\">…</table></div>",
    "solution_html": "<div class=\"tl-box\">…Kiến thức cần gọi lại…</div><ol class=\"tl-steps\">…</ol><p>Nhận dạng: …</p>" } ] }
```
Hình trong `problem_html`/`analysis_html` do `build-hinh-<id>.py` chèn. `topic_id` và `body_html` (gộp để chỗ cũ đọc được) do script đăng sinh — không tự điền. Dùng linh kiện `.tl-*` có sẵn (`tl-box`, `tl-steps`, `tl-table--data`) cho khớp bài lý thuyết.

## Đăng (Mac)

Điều kiện: migration `20261006180000_similar_bank_questions.sql` đã chạy (không thì nút "Làm bài tương tự" báo "Chưa tải được"; phần còn lại vẫn chạy).
```
cd /Users/MAC/Projects/thachlab && git pull origin main
npx tsx scripts/publish-bai-tap-mau.mts --lesson <id> --dry-run
npx tsx scripts/publish-bai-tap-mau.mts --lesson <id> --giu-cu   # bỏ --giu-cu = GHI ĐÈ toàn bộ dạng cũ
bash scripts/deploy.sh
```
Chạy lệnh dài trong tab terminal (AGENTS.md). Phiên cloud: chỉ soạn + validate, in lệnh cho thầy.

## Giới hạn đã biết

- **Bài đã có dạng cũ (bài 57 có 19 dạng) → luôn đăng bằng `--giu-cu`** (dạng mới lên đầu, dạng cũ nối sau). Không cờ này là ghi đè hết.

- Bài tương tự lấy theo **YCCĐ (+ `form`)**, ngân hàng không có nhãn "dạng bài con" → độ sát phụ thuộc YCCĐ chọn đúng.
- RPC lộ đáp án cho HS đăng nhập (như PracticeSession); không dùng cho bài tính điểm. Chưa ghi kết quả bài tương tự vào `practice_sessions`/mastery (RPC không trả mã đề nguồn) — làm sau nếu thầy muốn.

## Nhật ký rút kinh nghiệm (bắt buộc cập nhật cuối MỖI phiên dùng skill này — xem `AGENTS.md`)

- 2026-10-06 · Pilot bài 57 (3 dạng) → kiểm chéo bắt đề Dạng 3 mơ hồ ("đứng trên mái nhà" không rõ điểm ném, vật cản không nằm trên đường bay) → đề bài có hình học phải nói rõ **điểm ném, mốc đo khoảng cách, vật cản nằm đâu**; khung "Kiến thức" phải chứa mọi ký hiệu lời giải dùng (L).
- 2026-10-06 · Validator chặn `<`/`>` trong `$…$` ngay lần chạy đầu (tôi viết `$v>v_0$`) → viết `\lt`/`\gt` từ đầu.
- 2026-10-06 · YCCĐ trong bank có 2 con/bài (bài 57) nên Dạng 1 và 3 cùng `topic` → bài tương tự của hai dạng sẽ trùng nguồn; chấp nhận, nhưng ngân hàng không có nhãn "dạng bài con".

- 2026-10-06 · Đăng bài 57 không cờ giữ cũ → ghi đè 19 dạng cũ bằng 3 dạng mới (có sao lưu, đã nối lại) → script đăng phải mặc định cảnh báo số dạng cũ sẽ mất; dùng `--giu-cu` cho bài đã có nội dung.
- 2026-10-07 · Thầy: gợi ý bằng hình hiệu quả hơn lời → mỗi gợi ý có hình (4 hình/dạng, dựng từ quỹ đạo tính thật); lần chạy đầu 12/24 hình lỗi bố cục (cắt mép, nhãn đè) → luôn chụp xem từng hình trước khi đăng; thước đo dưới mặt đất cần viewBox cao hơn `ground+40`.
- 2026-10-07 · Hình động SMIL cho bài ném: dựng quỹ đạo từ công thức (mẫu cách đều t), 2 hình ≈ +7 KB thô; bố cục chữ vẫn phải chụp xem (nhãn dài bị cắt mép trái).
- 2026-10-07 · Thầy bỏ gợi ý 3 tầng và hình động trong gợi ý; chuyển mô phỏng xuống dưới đề, thay gợi ý bằng bảng phân tích đề như bài mẫu trong lý thuyết → bản 3-gợi ý không còn là mặc định (UI vẫn đọc `hints_html` cũ). Hỏi lại ý thầy sớm khi cấu trúc UI đổi nhiều lần trong một buổi.
- 2026-10-07 · Lời giải viết liền → ngắt theo bước/dòng công thức, dựng bằng `sol()` + CSS `.bt-*`; xem thật ở dev server (đừng kết luận CSS lỗi khi dev chưa nạp: `touch app/globals.css` + tải lại). Lời giải 14 bài tự luận cũ vẫn viết liền (chưa biên tập).
- 2026-10-07 · Mô phỏng tự lặp trái B4 → chuyển sang chạy một lần khi bấm (SMIL `begin=indefinite` + nút + `beginElement()` trong ContentHtml). Test SMIL trong tab ẩn cho kết quả sai (đứng yên) — đưa tab lên tiền cảnh trước khi kết luận lỗi.
- 2026-10-07 · Nhân ra chương 2 (6 bài: 49,50,52,53,54,55; 51/56 là thực hành nên bỏ) bằng 1 builder + 1 kiểm chéo độc lập mỗi bài → kiểm chéo luôn bắt được: bảng phân tích lộ đáp số, hình đề đo được đáp án bằng tỉ lệ, số liệu phi thực tế, LaTeX hỏng ở tự luận cũ → để builder sửa rồi mới đặt review.checked; nội dung bài mẫu lấy từ DB lúc chạy (file tĩnh không chứa questions) nên đăng xong KHÔNG cần deploy.
- 2026-10-07 · Tự luận cũ phụ thuộc hình gốc mà agent không xem được (bài 53: Bài 13, 14) → số suy từ lời giải cũ, thầy cần đối chiếu hình; câu nào không đối chiếu được thì bỏ khỏi tu_luan.
- 2026-10-07 · Bài định tính (lesson 10, Khái niệm từ trường): mô phỏng "kim chạy theo đường sức" lộ luôn đáp án chiều → dùng mô phỏng không có chiều (mạt sắt hiện dần/vòng tròn lan ra); đường sức thanh nam châm tính bằng mô hình hai cực điểm (tích phân số), chọn góc xuất phát φ≈78–130° để vòng không tràn viewBox. Bảng phân tích không được ghi hướng/phép cộng-trừ của câu hỏi (kiem-code bắt ở dạng 3, 4). Bài `lesson 10` KHÔNG có mục `bai_tap_mau` trong DB → `publish-bai-tap-mau.mts` sẽ báo "cần đúng 1" cho tới khi tạo mục.
- 2026-10-07 · Thầy bảo "sửa tiêu đề bài mẫu theo đúng số dạng" mà không nói bài nào → đừng đoán: đọc thẳng DB bằng REST anon (`lesson_items?kind=eq.bai_tap_mau&select=lesson_id,questions`, curl chạy được từ Bash) rồi đối chiếu số "Dạng N" từng bài với file `scripts/data/bai-tap-mau/<id>.json`. Nhãn phải liên tục 1..N đúng thứ tự mảng `dang_bai` (mục tự luận cuối không đánh số). Bài 10, 49–57 khớp; các bài cũ lệch số (5, 11, 44, 70, 83, 129–131) chưa soạn lại bằng skill này → chỉ sửa khi thầy chỉ đích danh. Sửa nhãn: sửa `label` trong JSON rồi `publish-bai-tap-mau.mts --lesson <id> --giu-cu` (+ deploy).
- 2026-10-07 · Thầy: "sửa tiêu đề bài mẫu theo đúng số dạng" = dòng phụ đề đầu mục ("19 dạng bài kèm lời giải") còn số của 19 dạng cũ trong khi chỉ hiện 7 dạng; các nhãn "Dạng N" thì đúng → `publish-bai-tap-mau.mts` giờ ghi luôn `subtitle` = "<số dạng thật> dạng bài kèm lời giải"; sau khi thay dạng của bài đã có nội dung phải chạy lại script cho bài đó rồi deploy, và kiểm cả subtitle chứ không chỉ nhãn từng dạng.


---
# PHẦN 2 — references/huong-dan-nhan-ra.md

# Hướng dẫn soạn bài tập mẫu cho MỘT bài (dành cho subagent — nhân ra cả chương)

Mẫu hoàn chỉnh đã đăng: **bài 57** — `scripts/data/bai-tap-mau/build-hinh-57.py` (đọc toàn bộ file này trước, nó là chuẩn), `57.json` (kết quả).
Thư viện: `.claude/skills/soan-bai-tap-mau/scripts/dung.py` (sol/tbl/ball/smil/write/tu_luan_tu), `hinh.py` (fig/arrow/dim/arc/axes/poly/ground…, màu theo `svg_lib.py`). Đọc `SKILL.md` cùng thư mục (quy tắc phong cách) và `docs/AI-TUTOR.md` mục 9.1/9.3/9.5.

## Việc phải làm cho bài `<ID>`
1. Đọc lý thuyết của bài: `public/data/lessons/<ID>.json` (mục `ly_thuyet`: ký hiệu, giá trị g, công thức, thứ tự kiến thức) — dạng bài soạn phải **khớp đúng ký hiệu/quy ước của lý thuyết** bài đó. Đọc **toàn bộ** ví dụ cũ ở `scripts/data/bai-tap-mau/old/<ID>.json` (có đề + lời giải + ảnh `<img>`).
2. Chốt **4–6 dạng**, xếp **DỄ → KHÓ** (dạng sau dùng lại cách của dạng trước), mỗi dạng = một kiểu bài học sinh gặp lặp lại. Nhãn `Dạng k · Dễ|Trung bình|Khó · <tên>`.
3. Ví dụ cũ nào hợp một dạng → **biên tập lại thành dạng đó** (đổi số cho đẹp/thực tế, đề rõ nghĩa: điểm đo, mốc, chiều dương, cùng/khác độ cao…). Ví dụ cũ còn lại → gom vào `tu_luan` bằng `tu_luan_tu(old, order, muc)` xếp dễ→khó (giữ nguyên lời giải gốc, KHÔNG sửa).
4. Mỗi dạng cần: `label`, `topic` (**tên YCCĐ con nguyên văn** từ `scripts/data/question-topics.json`, đúng `lesson_id` của bài; ưu tiên con, cha chỉ khi bài không có con), `problem_html` (đề chữ, LaTeX `$…$`; `<`/`>` viết `\lt`/`\gt`), `BUILD[i](k)` (k=0: **mô phỏng hiện tượng nằm DƯỚI đề**, chạy một lần khi bấm; k=2: hình dữ kiện tĩnh cho phần phân tích), `ANALYSIS[i]` (bảng **Câu trong đề | Dữ liệu | Kiến thức liên quan**, mỗi hàng trích một cụm của đề, có hàng ⚠ điều kiện áp dụng; cột 3 chỉ công thức/ý, KHÔNG ghi số đáp án), `SOLS[i]` = `sol(recall, steps, finals, note)` (mỗi bước một khối, **mỗi công thức một dòng**, tách công thức chữ / thế số / kết quả; ô đáp số; "Nhận dạng").
5. Viết script `scripts/data/bai-tap-mau/build-hinh-<ID>.py` theo mẫu 57, kết thúc bằng `write(J, <ID>, "<tên bài>", DANG, BUILD, ANALYSIS, SOLS, TU_LUAN)`. Chạy → sinh `scripts/data/bai-tap-mau/<ID>.json`. Helper riêng của bài đặt trong chính file build (hoặc `scripts/data/bai-tap-mau/hinh_<ID>.py`), **không sửa** `dung.py`/`hinh.py`.

## Mô phỏng & hình (quan trọng)
- Hình **tính thật từ công thức** (mẫu cách đều thời gian, nội suy tuyến tính), không vẽ tay quỹ đạo/đồ thị. Chuyển động thẳng: vật chạy dọc trục có thước; đồ thị: điểm chạy trên đồ thị + vạch đứng; rơi tự do: vật rơi kèm các vị trí cách đều thời gian…
- **Chạy MỘT lần khi bấm**: dùng `ball()`/`smil()` (begin="indefinite", fill="freeze"); `fig()` tự thêm nút. Chạy đúng thời gian thật hoặc ghi "chạy chậm k lần" trong chú thích. Đối tượng phải **đúng vật lí** (ví dụ vật mang vận tốc của phương tiện: xe + hàng cùng chạy).
- **Không lộ đáp số** trong hình đề (chỉ dữ kiện đề cho, dấu "?" cho đại lượng cần tìm). Bài ngược chạy một lần "thử" hợp lí.
- Bố cục: mỗi hình ≤ ~8 nhãn, chữ ≥ 12, viewBox đủ chỗ cho thước đo (đừng đặt nhãn dưới mặt đất ngoài viewBox), nhãn không đè mũi tên/quỹ đạo, không chữ cắt mép. Marker mỗi hình một tiền tố (`defs(p)`).
- Đồ thị cần trục có đơn vị, vạch chia, nhãn đại lượng; dùng đúng màu quy ước bài lý thuyết.

## Kiểm (bắt buộc, tự làm trước khi báo xong)
- `npx tsx .claude/skills/soan-bai-tap-mau/scripts/validate.mts scripts/data/bai-tap-mau/<ID>.json` phải qua (review.checked sẽ false → lỗi duy nhất được phép; phiên chính sẽ đặt true sau kiểm chéo).
- **Tự giải lại mọi dạng bằng Python** (số học độc lập với lời giải) và ghi so sánh; số liệu thực tế (không v₀ = 70 km/h cho người nhảy xa…), đẹp (tròn, căn đẹp).
- Xem hình bằng mắt: `python3 .claude/skills/soan-bai-tap-mau/scripts/xem-thu.py scripts/data/bai-tap-mau/<ID>.json <thư mục scratchpad của bạn> [--dang 1,3]` rồi **Read các PNG** (đề + mô phỏng ở khung CUỐI + phân tích + lời giải). Sửa lỗi bố cục/chữ cắt/nhãn đè rồi chụp lại (mỗi hình ít nhất 1 lần sau sửa). KHÔNG dùng browser pane (nhiều agent cùng chạy sẽ đụng nhau).
- Tuân `docs/QUY-TAC-THIET-KE.md` (C1/C4/H5/B3/N7, B4).

## Ranh giới
- CHỈ tạo/sửa: `scripts/data/bai-tap-mau/<ID>.json`, `build-hinh-<ID>.py`, `hinh_<ID>.py` (tuỳ chọn) và file tạm trong scratchpad. KHÔNG sửa file chung (`dung.py`, `hinh.py`, `SKILL.md`, `globals.css`, `AGENTS.md`, `STATE.md`…), KHÔNG chạy `publish-*`, KHÔNG ghi DB, KHÔNG `git add/commit`, KHÔNG deploy, KHÔNG đụng bài khác. Không dùng vai "thầy/cô" trong nội dung.

## Báo cáo cuối (ngắn, ≤ 25 dòng)
Danh sách dạng (nhãn + mức + topic); ví dụ cũ nào đã biên tập thành dạng nào, nào vào tự luận (số lượng); kết quả tự giải lại (khớp/lệch); lỗi hình đã sửa; điều còn nghi ngờ cho phiên chính.
