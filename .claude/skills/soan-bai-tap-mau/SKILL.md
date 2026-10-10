---
name: soan-bai-tap-mau
description: Soạn mục BÀI TẬP MẪU của một bài học thachlab — làm TRỰC TIẾP trên Mac trong phiên Claude Code (không Batch API trừ khi thầy bảo), 2–6 dạng theo quét, mỗi dạng có buoc[] để học sinh tự giải từng bước, mỗi dạng có đề + MÔ PHỎNG chuyển động ngay dưới đề, bảng PHÂN TÍCH ĐỀ (Câu trong đề | Dữ liệu | Kiến thức liên quan, như bài toán mẫu trong lý thuyết), lời giải đầy đủ theo phong cách thầy Thạch (AI-TUTOR 9.1/9.3/9.5), gắn YCCĐ để web tự tìm 3 bài tương tự trong ngân hàng câu hỏi sau khi học sinh đọc xong. Dùng khi thầy nói "soạn bài tập mẫu cho bài X", "làm các dạng bài tập của bài…", "thêm bài tập mẫu có gợi ý", "bài tập mẫu theo phong cách của tôi". Khác soan-bai-ly-thuyet-tuong-tac (bài lý thuyết, có sẵn "bài toán mẫu" nằm TRONG lý thuyết) và dang-bai-hoc-thachlab (đăng .tex). Soạn + kiểm chạy được trên cloud; ĐĂNG lên DB phải chạy trên Mac.
---

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
**Vectơ trong hình (thầy chốt 10/10/2026):** đầu mũi tên chữ V 30° (hàm `arrow()` của `svg_lib` đã vẽ sẵn, không còn marker tam giác) và **độ dài tỉ lệ độ lớn** — tính số liệu thật rồi chọn một hệ số `k` px/N cho cả hình, vẽ bằng `vec_luc(màu, x, y, dx, dy, F, k)`; quá ngắn thì tăng `k`/viewBox, đừng kéo dài giả. Lực không vẽ cùng tỉ lệ được (vd. P=15000 N cạnh F_c=450 N) thì vẽ thành phần cần dùng (P·h/l) và nói rõ. Hình động tự vẽ `<line marker-end>` cũng phải đổi sang line + `chevron` trượt theo. Kiểm: `grep -c marker-end scripts/data/bai-tap-mau/<id>.json` phải = 0. Chi tiết: `soan-bai-ly-thuyet-tuong-tac/references/hinh-svg.md`.
**Xem bằng mắt trước khi đăng** (ghi ra HTML, `python3 -m http.server`, chụp): lỗi hay gặp là nhãn cắt mép, nhãn đè mũi tên/quỹ đạo, thước đo dưới mặt đất thiếu chỗ ở viewBox.

### Lời giải ngắt dòng (thầy chốt 7/10/2026)
Lời giải viết liền khó đọc → mỗi lời giải dựng bằng `sol()` trong `build-hinh-57.py` theo `docs/QUY-TAC-THIET-KE.md` C1/C4/H5/B3/N7: khung "Kiến thức cần gọi lại" (≤ 5 dòng, mỗi dòng một ý) → **mỗi bước một khối** `bt-step` (số + tiêu đề đậm, 1 câu dẫn ≤ 1 dòng, **mỗi công thức một dòng `$$…$$`**, tách "công thức chữ" / "thế số" / "kết quả" thành 3 dòng, kết quả trong ô nền nhạt `bt-ans`) → ô **Đáp số** mỗi ý một dòng → dòng "Nhận dạng" nhỏ, mờ. Khoảng cách trong bước (6–10px) < giữa các bước (22px). CSS ở cuối `app/globals.css` (`.bt-*`). Không viết `<ol class="tl-steps">` liền nhiều công thức trong một dòng nữa. Đã xem ở 375px: không tràn ngang, công thức dài tự cuộn trong dòng.

## Học sinh tự giải từng bước trước khi xem (thầy chốt 9/10/2026) — 5 quy tắc mới

Mục tiêu: học sinh làm việc ở lúc tự nghĩ, không chỉ đọc lời giải có sẵn (retrieval, AI-TUTOR 9.3). Áp cho mọi dạng soạn mới; bài đã đăng (10, 49–55) soạn lại dần khi đụng tới. UI đã có (`components/lessons/StepwiseSolution.tsx` + `WorkedQuestionsGrid.tsx` + `SimilarBankPractice.tsx`, bài 57 là mẫu, 9/10/2026); validator trong `scripts/lib.ts` (`validateSteps`). **Xem thử trước khi đăng, không cần DB**: `npx tsx scripts/publish-bai-tap-mau.mts --lesson <id> --xem-thu` → mở `http://localhost:3000/dev/btm` (thêm `?mock=1` để giả RPC bài tương tự, xem được luồng chấm + gỡ rối khi chưa đăng nhập).

1. **Lời giải mặc định đóng, mở theo bước.** Mỗi bước `bt-step` có câu hỏi `hoi` + ô trả lời (số có đơn vị → `dap_so` ± `sai_so`; chọn → `lua_chon`). Đúng → mở bước đó và hiện câu hỏi bước kế. Sai → hiện `loi_hay_gap` của bước (lỗi + vì sao sai), cho làm lại 1 lần, rồi mới cho "Xem bước này". Luôn có nút "Xem cả lời giải" nhưng đặt nhỏ, dưới cùng.
2. **Ví dụ mờ dần theo cấp** (`fading`, mặc định theo cấp, cùng cấp được tăng thêm, **không giảm** theo thứ tự dạng): `mo_het` (cấp 1) → `giau_buoc_cuoi` (giấu bước cuối **có câu hỏi**; bước "Kiểm tra" không hỏi thì không tính) → `giau_tu_buoc_2` → `giau_het` (chỉ đề + bảng phân tích, mọi bước tự làm). Bước không có `hoi` không bao giờ bị giấu. "Làm bài tương tự" chỉ hiện khi đã mở hết các bước.
3. **Chọn bước kế trước khi xem** (`chon_buoc_ke`): trước mỗi bước (trừ bước 1) hỏi "Bước tiếp theo là gì?" với **3 lựa chọn** — 1 đúng, 2 là cách làm sai học sinh hay chọn (bỏ qua điều kiện, dùng công thức của dạng trước, đổi đơn vị sai…). Chọn sai → 1 dòng giải thích vì sao sai rồi cho chọn lại. Không dùng lựa chọn vô nghĩa cho đủ 3.
4. **Câu nhận dạng** (`nhan_dang`, bắt buộc mỗi dạng, 1 câu ≤ 25 chữ): "Thấy **…** trong đề → nghĩ tới **…**". Hiện ở đầu dạng (trước đề, dạng thẻ nhỏ) **và** cuối lời giải. Từ khoá in đậm là chữ sẽ gặp trong đề thi, không phải tên định luật.
5. **Bài tương tự có thang gỡ rối** (`go_roi`): học sinh sai bài tương tự → không chỉ báo sai, mà hỏi 1 câu chẩn đoán ("Em tính đến bước nào?" chọn trong danh sách bước) rồi nhảy về đúng bước đó của dạng mẫu, mở đúng bước ấy. Mỗi dạng ghi `go_roi.buoc_hay_sai` = chỉ số bước hay gây lỗi nhất (từ `loi_hay_gap`), dùng làm mặc định khi học sinh không chọn.

Khi soạn: viết `buoc[]` cùng lúc với `sol()` trong `build-hinh-<id>.py` (helper `buoc()` trong `dung.py`, truyền `STEPS` làm tham số thứ 5 của `inject()`); số bước phải khớp 1-1 với `.bt-step` của lời giải. `loi_hay_gap` và lựa chọn sai lấy từ câu học sinh hay sai trong ngân hàng cùng chủ đề — kiểm chéo `kiem-code` phải xác nhận lựa chọn sai **thật sự sai** và đáp số bước **tính lại khớp**. **Không lộ đáp số của bước trong `tieu_de`/`hoi`/lựa chọn** (validator chặn với đáp số ≥ 2 chữ số; `loi_hay_gap` cũng không nêu số suy ra được đáp số, như góc phụ). Validator kiểm: `nhan_dang` (≤ 25 chữ), ≥ 2 bước khớp số `.bt-step`, bước có `hoi` phải có `dap_so`+`sai_so` hoặc `lua_chon` và `loi_hay_gap`, `chon_buoc_ke` đúng 3 mục/1 đúng/mục sai có `vi_sao`, `cap_do` 1–4 và `fading` không giảm, `go_roi.buoc_hay_sai` trong phạm vi.

## Bước 0 — quét số dạng và tên dạng TRƯỚC khi nháp (thầy chốt 9/10/2026)
Số dạng không cố định 4 (thường 2–6). Không viết nháp khi chưa có danh sách dạng đã quét.
- **Dạng lấy từ lý thuyết của bài và ngân hàng câu hỏi cùng chủ đề** (`question_topics` + `question_bank`, lọc `archived = false`). Dạng không có câu tương ứng thì bỏ.
- **Cấp độ 1–4**, không giảm khi đi xuống danh sách; cùng cấp có thể nhiều dạng.
- **Model: Sonnet 5.5, effort medium.** Chạy trong phiên Claude Code (subagent Sonnet) hoặc batch `--che-do quet-dang` (mặc định Sonnet, medium).
- **Prompt:** `references/PROMPT-SONNET-QUET-DANG.md`. Đầu ra JSON: `dang` (tên, cấp, `nguon_chu_de`, `so_cau_ngan_hang`, `yccd`, `ly_do`, `cau_noi`), `khong_dua_vao`, `ghi_chu`.
- **Kết quả:** `scripts/logs/batch-ra-soat/ket-qua/<id>.quet-dang.json`. Nháp và viết lại đọc đúng các dạng trong file này.
- **Kiểm trước khi đi tiếp:** 2–6 dạng, cấp 1–4 không giảm, không trùng tên, dạng không có chủ đề nguồn phải có ghi chú; bài chưa có YCCĐ thì `yccd` rỗng và ghi chú lại.

## Nháp do Claude viết (Gemini đã bỏ — thầy chốt 9/10/2026)
Nháp theo **hệ bắc cầu cấp độ 1–4** (Áp dụng trực tiếp → Có điều kiện/bẫy → Kết hợp nhiều bước → Tình huống mới; số dạng theo bước 0). Nháp phải đi đủ: kiểm máy → tự viết lại theo "Phong cách" → kiểm chéo độc lập (`kiem-code`) → validate → đăng. Không còn đường dán tay qua Gemini; file `PROMPT-GEMINI-BAI-TAP-MAU.md` và `kiem-ban-nhap-gemini.py` không còn là bước của quy trình.

## Tuỳ chọn: hàng loạt qua Batch API (CHỈ khi thầy nói rõ "chạy batch" — thầy chốt 9/10/2026: đường chính là làm trực tiếp trên Mac trong phiên Claude Code, không đốt credit API)
Ba chế độ nối nhau trong `scripts/batch-ra-soat-bai.mts` (chạy trong tab terminal của thầy; bài phải có dòng trong `content/gemini/hang-doi.md`):
0. `--che-do quet-dang --gui --lop 12` → `--nhan --cho` (hoặc quét trong phiên Claude Code): danh sách dạng, phải xong trước bước 1.
1. `--che-do bai-tap-mau --gui --lop 12` → `--nhan --cho`: nháp theo danh sách quét + kiểm máy → `scripts/logs/batch-ra-soat/ket-qua/<id>.bai-tap-mau.nhap.json`.
2. `--che-do viet-bai-tap-mau --gui …` → `--nhan --cho`: API viết hoàn chỉnh (HTML + SVG mô phỏng + bảng phân tích + lời giải + `buoc[]`/`nhan_dang`/`cap_do`/`fading`/`go_roi` tự giải từng bước — từ 9/10/2026, dạng mẫu trong system prompt là bài 57 dạng 2) theo
   `references/PROMPT-CLAUDE-VIET-BAI-TAP-MAU.md`, system prompt nhúng AI-TUTOR mục 9 + dạng 2 bài 10 làm mẫu) → ghi
   `scripts/data/bai-tap-mau/<id>.json` (`review.checked=false`, bản cũ sao lưu `old/<id>.truoc-api-*.json`), chạy `validate.mts`, chụp
   `scripts/logs/batch-ra-soat/xem-thu/<id>/dang-N.png`.
3. `--che-do kiem-cheo --gui …` → `--nhan --cho`: request khác tự giải độc lập (`references/PROMPT-CLAUDE-KIEM-CHEO.md`, kiểm cả `buoc[]`: đáp số bước, lựa chọn sai thật, không lộ đáp số); cả 4 "dung" →
   `review.checked=true`. Có "sai"/"nghi_ngo" → ghi vào `review.kiem_cheo`, Claude Code sửa tay rồi chạy lại kiem-cheo cho bài đó.
4. Xem ảnh `dang-N.png` bằng mắt (subagent, không đọc ảnh ở phiên chính), sửa hình hỏng, rồi đăng `publish-bai-tap-mau.mts --lesson <id> --yes`
   (`--giu-cu` nếu bài có dạng cũ). Báo cáo gộp: `--tong-hop` → `BAO-CAO-VIET-BTM.md`.

## Nhân ra nhiều bài (chương)
Mỗi bài một subagent theo `references/huong-dan-nhan-ra.md` (mẫu = bài 57), chạy song song; sau đó **mỗi bài thêm một subagent `kiem-code` khác tự giải độc lập** (không nhìn lời giải) → sửa → `review.checked=true` → phiên chính publish từng bài (`--lesson <id>`, dạng cũ vào `tu_luan` nên KHÔNG dùng `--giu-cu`) rồi deploy một lần. Dạng cũ lấy từ `scripts/dump-bai-tap-mau-cu.mts <id…>` → `scripts/data/bai-tap-mau/old/<id>.json` (chạy trước khi publish ghi đè). Xem thử bằng `scripts/xem-thu.py` (Chrome headless, khung cuối của mô phỏng).

## Quy trình — ĐƯỜNG CHÍNH: làm trực tiếp trên Mac trong phiên Claude Code (thầy chốt 9/10/2026)

Một bài ≈ 1 phiên, mẫu là bài 57 (`scripts/data/bai-tap-mau/build-hinh-57.py`). Không gọi Batch API trừ khi thầy bảo. Giữ token thấp:
đọc đoạn, không đọc cả file; ảnh chỉ xem trong subagent; không báo tiến độ giữa chừng.

1. **Chọn bài + đọc đúng thứ cần**: `grep -c`/`python3 -c` lấy mục `ly_thuyet` của `public/data/lessons/<id>.json` (file 100+ KB — **không** `grep` thẳng, không đọc cả file), mục `bai_tap_mau` hiện có (dump: `scripts/dump-bai-tap-mau-cu.mts <id>`), YCCĐ của bài trong `scripts/data/question-topics.json` (lọc theo `lesson_id`). Thiếu `public/data`: `node scripts/build-content.mjs`.
2. **Bước 0 quét dạng** (mục trên) bằng **subagent Sonnet** (prompt `references/PROMPT-SONNET-QUET-DANG.md`, trả JSON ngắn) → 2–6 dạng, cấp 1–4 không giảm, `topic` = YCCĐ con nguyên văn. Soát ngân hàng: `topic` có < 6 câu `bai_tap` → báo thầy.
3. **Viết `build-hinh-<id>.py`** (chép khung bài 57): `BUILD` (hình mô phỏng + hình dữ kiện bằng `hinh.py`), `ANALYSIS` (bảng), `SOLS` (`sol()`), `STEPS` (`buoc()` — viết cùng lúc với `sol()`, số bước khớp), rồi `inject(J, BUILD, ANALYSIS, SOLS, STEPS)`. Đề + số liệu + lời giải tự viết trong phiên chính (hoặc một subagent Sonnet mỗi bài khi nhân ra chương). LaTeX `\lt`/`\gt`.
4. **Validate**: `npx tsx .claude/skills/soan-bai-tap-mau/scripts/validate.mts scripts/data/bai-tap-mau/<id>.json` — sửa tới khi sạch (lộ đáp số, lệch số bước… bắt ở đây, rẻ).
5. **Kiểm chéo bắt buộc**: subagent `kiem-code` tự giải từng dạng từ đề (không nhìn lời giải) + kiểm `buoc[]` (đáp số bước, lựa chọn sai thật, không lộ) → sửa → `review.checked: true`.
6. **Xem hình** (rẻ nhất): `python3 .claude/skills/soan-bai-tap-mau/scripts/xem-thu.py scripts/data/bai-tap-mau/<id>.json <thư mục>` rồi subagent xem ảnh, phiên chính không đọc ảnh. UI từng bước **không cần chụp lại** (đã cố định; chỉ chụp khi đổi component) — muốn xem thì `publish-bai-tap-mau.mts --lesson <id> --xem-thu` → `/dev/btm?mock=1`.
7. **Đăng + deploy** (mục "Đăng", tab terminal). Viết "Rút kinh nghiệm" vào Nhật ký cuối file này.

## Dạng file

```json
{ "lesson_id": 57, "lesson_title": "Chuyển động ném", "generated_at": "2026-10-06",
  "review": { "checked": true, "notes": "…" },
  "dang_bai": [ {
    "label": "Dạng 1 · Ném ngang: tìm thời gian bay và tầm xa",
    "topic": "<tên YCCĐ con, nguyên văn>", "form": "bai_tap",
    "problem_html": "<p>…</p>",
    "analysis_html": "<figure …hình dữ kiện…></figure><div class=\"table-scroll\"><table class=\"tl-table tl-table--data\">…</table></div>",
    "solution_html": "<div class=\"tl-box\">…Kiến thức cần gọi lại…</div><ol class=\"tl-steps\">…</ol><p>Nhận dạng: …</p>",
    "cap_do": 2, "fading": "giau_buoc_cuoi",
    "nhan_dang": "Thấy <b>ném ngang từ độ cao h</b> → nghĩ tới <b>t = √(2h/g)</b>, tầm xa = v₀·t",
    "buoc": [ {
      "tieu_de": "Tìm thời gian bay", "hoi": "Thời gian bay t bằng bao nhiêu?",
      "dap_so": 2.0, "don_vi": "s", "sai_so": 0.05,
      "loi_hay_gap": "Dùng h = v₀t (coi rơi đều) — sai vì theo phương thẳng đứng vật rơi tự do, h = ½gt²." },
    { "tieu_de": "Tìm tầm xa", "hoi": "Tầm xa L bằng bao nhiêu?",
      "dap_so": 30, "don_vi": "m", "sai_so": 0.5,
      "chon_buoc_ke": [ { "text": "L = v₀·t", "dung": true },
        { "text": "L = ½·v₀·t", "dung": false, "vi_sao": "Theo phương ngang vật chuyển động đều, không có ½." },
        { "text": "L = √(2h/g)", "dung": false, "vi_sao": "Đó là công thức thời gian, chưa nhân với v₀." } ],
      "loi_hay_gap": "Lấy L = v₀·t nhưng thế t sai đơn vị (ms thay vì s)." } ],
    "go_roi": { "buoc_hay_sai": 0 } } ] }
```
`cap_do` 1–4 theo bước 0; `fading` ∈ `mo_het` · `giau_buoc_cuoi` · `giau_tu_buoc_2` · `giau_het` (bài 57: dạng 1–6 = mo_het, giau_buoc_cuoi, giau_buoc_cuoi, giau_tu_buoc_2, giau_tu_buoc_2, giau_het). `chon_buoc_ke` chỉ có ở bước ≥ 2 (UI chỉ hỏi khi bước đó bị giấu). Câu định tính dùng `lua_chon` (mảng như `chon_buoc_ke`) thay `dap_so`. Bước phụ ("Kiểm tra") không có `hoi`.
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
- 2026-10-08 · Thêm đường "bản nháp Gemini" (prompt + `kiem-ban-nhap-gemini.py`) → chưa chạy vòng thật; sau bài đầu ghi: lỗi số học/đơn vị Gemini hay mắc, mức công Claude phải viết lại.
- 2026-10-08 · Nháp 4 dạng có thể sinh hàng loạt bằng `scripts/batch-ra-soat-bai.mts --che-do bai-tap-mau` (Claude qua Batch API, credit API) — vẫn là BẢN NHÁP, đi đủ kiểm máy → viết lại → kiem-code → đăng (từ 8/10/2026 thầy không duyệt trước; trợ giảng rà trên web).
- 2026-10-08 · Thầy chốt: nháp BTM không cần Gemini, đi thẳng batch Claude (`--che-do bai-tap-mau`); Claude viết lại, kiểm chéo rồi đăng luôn, trợ giảng người thật rà trên web. Bài 10 đã có `scripts/data/bai-tap-mau/10.json` (4 dạng, review.checked) từ 7/10 và DB nay đã có mục `bai_tap_mau` ("Các dạng bài tập") → chỉ cần publish.
- 2026-10-08 · Viết hai chế độ batch `viet-bai-tap-mau` + `kiem-cheo` để API làm trọn phần chữ + SVG, Claude Code chỉ xem ảnh/sửa hình. CHƯA chạy thật — sau bài đầu ghi: tỉ lệ validate sạch, chất lượng SVG do API vẽ (nhãn cắt mép? lộ đáp số?), tỉ lệ kiem-cheo đạt.
- 2026-10-09 · Số dạng không cố định 4: bước 0 quét dạng (Sonnet, effort medium) trước khi nháp; `viet-bai-tap-mau` và prompt nháp đọc số dạng từ `ket-qua/<id>.quet-dang.json`, không còn `SO_DANG = 4`. Batch `bai-tap-mau` từ chối bài chưa quét. → Bài có nháp cũ 4 dạng mà quét ra số khác (bài 17: 4 → 5) phải nháp lại, không dùng lại.
- 2026-10-09 · Lỗi tự gây: ghi "bài chưa có danh mục YCCĐ" dựa trên file lý thuyết, nhưng danh mục thật lấy từ chủ đề ngân hàng (`danhMucYccd`). → Trước khi ghi "không có YCCĐ", chạy `kiem-ban-nhap-gemini.py` để xem danh mục thật.
- 2026-10-09 · Subagent soạn nháp (Opus) làm lệch công thức ngoài bài (E = P·t ở Dạng 5, không có trong lý thuyết) và sai một câu bẫy (Δm). → Kiểm chéo bằng Sonnet độc lập bắt được cả hai; luôn kiểm chéo trước khi đánh dấu `review.checked`.
- 2026-10-09 · Kiểm chéo đã tự giải trước rồi mới mở lời giải; chỉ kiểm lại đúng dạng bị sửa, không chạy lại cả bài.
- 2026-10-09 · Thầy chốt: KHÔNG dùng hết credit API — đường chính là làm trực tiếp trên Mac trong phiên Claude Code (quét dạng + viết `build-hinh-<id>.py` + kiem-code), Batch API chỉ khi thầy bảo. Token lớn nhất của phiên là xem ảnh trình duyệt → chỉ chụp khi đổi UI.
- 2026-10-09 · Prompt `viet-bai-tap-mau` + schema batch sinh luôn `buoc[]` (trường trống = null/[] vì schema strict; `gonBuoc` bỏ null trước khi ghi); kiem-cheo kiểm cả bước. CHƯA chạy thật — bài đầu tiên chạy xong ghi: tỉ lệ validator bắt lộ đáp số, chất lượng lựa chọn sai, số bước API chia có khớp `.bt-step` không.
- 2026-10-09 · Dựng UI + validator tự giải từng bước trên bài 57 (6 dạng, 26 bước, kiem-code tự giải 20/20 đáp số khớp). Bắt được: lựa chọn "bước kế" của dạng 6 ghi thẳng "α≈24,3°" = đáp số của bước → validator thêm kiểm lộ đáp số; `loi_hay_gap` nêu "37,4°" cũng suy ra 52,6° (góc phụ) → bỏ số. Fading "giấu bước cuối" ban đầu giấu bước "Kiểm tra" (không có câu hỏi) nên không giấu gì → "bước cuối" = bước cuối có `hoi`. Trang `/dev/btm` + `--xem-thu` + `?mock=1` tiết kiệm nhiều lần đăng thử lên DB; RPC bài tương tự trả 401 khi chưa đăng nhập nên phải mock.
- 2026-10-09 · Thầy bỏ đường nháp Gemini (mục đã gỡ khỏi quy trình, file prompt/kiem-ban-nhap-gemini.py còn nhưng không còn là bước) và chốt 5 quy tắc "tự giải từng bước": lời giải đóng mở theo bước, ví dụ mờ dần theo cấp, chọn bước kế, câu nhận dạng, bài tương tự gỡ rối về đúng bước → JSON thêm `buoc[]`/`nhan_dang`/`fading`/`go_roi`. CHƯA có UI, validator, prompt viết bài tương ứng — làm trên bài 57 trước rồi mới nhân ra.
- 2026-10-09 · Nhân ra chương 2 L11 (bài 27, 28, 30, 31, 32, 33; 29/34 thực hành bỏ) bằng 6 subagent Sonnet song song + 6 `kiem-code` độc lập: kiểm chéo bắt đúng loại lỗi cũ — bảng phân tích/hình đề/caption lộ đáp số (28 D3, 30 D1 "13:1", 32 D3 vẽ sẵn 5 bó, 33 D1 nhãn P), `vi_sao` sai vật lí (31 D3 d₂−d₁=AB), số mũ sai ở tự luận cũ (33 Bài 10) → builder phải để cột 3 chỉ ghi câu hỏi gợi, hình vẽ mẫu khác số đề + caption ghi rõ.
- 2026-10-09 · Chạy song song: `xem-thu.py` ghi `dang-N.png` đè nhau trong scratchpad chung → mỗi bài một thư mục con, đường dẫn tuyệt đối. `question_bank` bị RLS với anon (trả 0) → đếm câu bằng REST service key chỉ đọc. Bài định tính (ngân hàng thiếu `bai_tap`, vd 28) → `form="ly_thuyet"` cho dạng khái niệm. `write()` không nhận STEPS → gọi `inject(..., STEPS)` lần hai. Sửa builder bằng `del` theo số dòng đã làm hỏng build (xoá nhầm dòng gán `xP`) → sửa bằng replace chuỗi rồi chạy lại build; patch JSON sau build sẽ mất khi build lại.
- 2026-10-09 · Nhân ra chương 1 L11 (bài 20–26, 7 bài) bằng 7 subagent Sonnet + 7 `kiem-code`: 4 agent treo 600s giữa chừng (file đã ghi một phần) → `SendMessage` nối lại chạy tiếp được, không phải làm lại. `kiem-code` không có Edit nên lần đầu từ chối sửa → ghi rõ trong prompt "sửa bằng Bash/python trong builder". Kiểm chéo lại bắt đúng loại lỗi cũ: `loi_hay_gap`/`vi_sao`/hình phân tích lộ đáp số hoặc thu hẹp lựa chọn (21 ×6, 23, 24 D4 đồ thị Et/Eđ lộ T'=T/2, 25), lựa chọn "sai" thực ra đúng (25 D4/D5, 23 D4), `vi_sao` sai vật lí (20 D5). Bài 26 không có chủ đề riêng trong question-topics → dùng chủ đề bài 24; bài 20/23 dùng chung chủ đề bài 21/22 nên bài tương tự trùng nguồn.

- 2026-10-10 · Khoá HSG (CĐ01/02, 7 dạng/bài): kiểm chéo bắt được (a) figcaption mô phỏng lộ đáp số ("gấp 6 lần", "gấp đôi"), (b) hình có đồ thị/đường vẽ sẵn lộ kết quả (h = H/2), (c) lựa chọn sai của `chon_buoc_ke` thật ra đúng, (d) đề không nói cách mắc ròng rọc → viết đề + hình + `loi_hay_gap` rồi tự hỏi "đọc hình/chú thích có suy ra đáp số không"; số `loi_hay_gap` chỉ nói bằng lời. Bài chưa có trong DB: dùng id tạm (9001…) rồi `git mv` + `sed` sang id thật sau khi chạy migration seed.
- 2026-10-10 · Bài 161/166 (HSG9) ra mũi tên tam giác đặc, độ dài tuỳ tiện dù quy tắc V 30° đã chốt 7/10: `arrow()` mặc định vẫn là marker, quy tắc chỉ nằm trong tài liệu → sửa hàm gốc (`arrow()` vẽ chevron) + thêm `vec_luc()` ép độ dài = k·F; sau khi chốt quy tắc hình phải sửa hàm mặc định ngay, không chỉ ghi tài liệu.
- 2026-10-10 · HSG9 đợt 1 (CĐ13/10/11/00): kiểm chéo vẫn bắt được lỗi dù agent soạn đã tự giải: (a) bài nhiều trường hợp thiếu nghiệm (hai canô trên hồ tròn có 3 chu vi, không phải 2) → dò cả khoảng bằng vòng lặp rồi `assert` danh sách nghiệm; (b) chuỗi Python không `r""` chứa `\text` → `\t` thành tab, hỏng KaTeX → quét ký tự điều khiển trong JSON sau mỗi build; (c) khung cuối mô phỏng và chú thích tỉ lệ thời gian lộ đáp số → kiểm khung cuối, chỉ ghi "1 s = n s thật"; (d) số liệu chọn sao cho T = P hoặc làm tròn trùng nhau thì phương án nhiễu không phân biệt cách sai → thêm `assert` mọi cách sai cho kết quả khác đáp án đúng; (e) đề "540 g (chưa kể sắt)" phải ghi rõ khối lượng gồm/không gồm vật gắn kèm; (f) quy ước góc (so với thẳng đứng hay ngang) và làm tròn sai số phải thống nhất giữa lý thuyết, bài tập mẫu, tự luận.
- 2026-10-10 · Đợt 1 L12 (bài 2,3,4,6,7,8; builder Sonnet + kiem-code mỗi bài): kiểm chéo bắt lỗi ở 6/6 bài, chủ yếu **lộ đáp số ngoài `hoi`/lựa chọn** — trong `loi_hay_gap` (nêu đúng số đáp án), ô ⚠ và bảng phân tích (ghi sẵn công thức/kết luận), chú thích hình → dặn builder rà ba chỗ này từ đầu. Chuỗi Python thường chứa `\text` thành TAB làm hỏng KaTeX → dùng `r"…"` cho mọi chuỗi có `\`, và quét ký tự điều khiển trong JSON sau build. Bài chưa có mục `bai_tap_mau` trong DB (bài 6,7,8) làm `publish` dừng → kiểm `lesson_items` trước khi giao lệnh, chạy `tao-muc-bai-tap-mau.mts --lesson <id> --mau 224` (khuôn L12). Xem ảnh cả trang rất tốn token và không đọc được nhãn đè → cắt từng hình.
- 2026-10-10 · Đợt L11 (bài 35,36,37,39,40,41,42,44; builder Sonnet song song + kiem-code từng bài, 2 vòng): kiểm chéo bắt lỗi ở 8/8 bài — **đề trùng ví dụ/quiz trong lý thuyết** (bài 42 dạng 2,5), **số liệu khiến lựa chọn nhiễu trở thành đáp án** (bài 35 dạng 4: CB=AB), chú thích hình nói ngược vật lí (bài 41), nhãn trục ngoài viewBox (41, 42), bảng phân tích/`loi_hay_gap` ghi sẵn cách giải (36, 42). → dặn builder đối chiếu ĐỀ với bài toán mẫu + quiz trong lý thuyết trước khi chọn số. **Nhiều phiên cùng ghi một `scripts/data/bai-tap-mau/<id>.json`/`build-hinh-<id>.py` (bài 37, 40) làm agent này ghi đè agent kia** → trước khi giao builder, `ls -la --time-style` + `git status` thư mục này; 40 phải ghép tay (v1 nền + dạng 3 của v2). `build-hinh` ghi `tu_luan` qua `re.sub` chỉ đổi `&gt;`, còn `>` thô sau khi decode → quét JSON `$…$` có `<`/`>` sau build. Kiểm chéo nên chạy xong MỚI đặt `review.checked`, và kiểm lại bản vừa sửa nhiều (viết lại dạng) bằng một kiem-code thứ hai.
- 2026-10-10 · Đợt L12 2–3 + L10 A (35 bài, builder Sonnet + kiem-code mỗi bài, sửa qua SendMessage cho builder cũ): kiểm chéo vẫn bắt lỗi ở 29/29 bài. Lỗi quay lại nhiều nhất: (a) **lộ đáp số/hướng giải** ở `loi_hay_gap`, `vi_sao` (so sánh lớn/nhỏ, chiều), ô ⚠ + hàng bảng phân tích, `nhan_dang`, lựa chọn ĐÚNG của `chon_buoc_ke` có chứa kết quả; (b) `\t` trong chuỗi Python thường → TAB làm hỏng KaTeX (`validate.mts` không bắt, phải quét ký tự điều khiển sau mỗi build) và `\"` thừa trong raw string; (c) số hiển thị lệch do làm tròn sớm; (d) `tu_luan` cũ sai số/phụ thuộc hình không kiểm được → BỎ. Dặn builder đọc một file brief chung (đã có danh sách lỗi) giảm vòng sửa; ô nhập luỹ thừa 10 dùng "hệ số a của a·10ⁿ" (UI chỉ chấm hệ số, chưa xác nhận hiển thị).
- 2026-10-10 · Hai phiên cùng soạn BTM L11 35–44 (phiên kia ghi đè `build-hinh-40.py`, thêm `40.v2.json`): trước khi mở đợt mới chạy `git status`/`ls -la scripts/data/bai-tap-mau` xem có file `<id>.json` lạ do phiên khác ghi không; gặp thì dừng, hỏi thầy (đã xảy ra, thầy bảo phiên kia làm, phiên này dừng).
