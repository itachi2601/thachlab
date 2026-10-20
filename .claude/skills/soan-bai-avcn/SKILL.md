---
name: soan-bai-avcn
description: Soạn MỘT chương Anh văn chuyên ngành Cơ khí (AVCN, lớp `avcn` trên thachlab, sinh viên CĐ Cao Thắng trình độ yếu, mục tiêu nhớ từ chuyên ngành + thi cuối kỳ ≥ 5/10) từ giáo trình Technical English for Mechanical Engineering — bóc chương từ .docx, điền `data/bai.json` (20 từ ⭐ chia 4 cụm có quiz, Article từng câu chạm hiện dịch, 2 mẫu câu, gắn nhãn hình, SOP điền từ, Trả bài, đề mẫu 5 Part tự chấm, 23 câu luyện tập), dựng theory.html + bundle.json bằng script, ảnh Wikimedia Commons có giấy phép, xem thử 375 px, đăng bằng upload-lesson.mts. Dùng khi thầy nói "soạn chương X AVCN", "làm Chapter 3 Hand Tools", "bài anh văn chuyên ngành", "/soan-bai-avcn". Có đường để Gemini điền bai.json rồi Claude đối chiếu. KHÁC soan-bai-ly-thuyet-tuong-tac (bài Vật lí). Soạn + dựng + kiểm chạy được trên cloud; ĐĂNG DB và deploy chạy trên Mac.
---

# Soạn một chương AVCN (Anh văn chuyên ngành Cơ khí)

Bài mẫu đã duyệt (thầy chốt 13/10/2026): `content/lesson-samples/avcn-chapter-8-chipping-machining/`. Đề xuất gốc và
lý do sư phạm: `docs/DE-XUAT-AVCN-CHUONG-8-2026-10-12.md`. **Mọi nội dung nằm trong `data/bai.json`; script dàn trang**,
nên 9 chương còn lại chỉ cần điền JSON đúng schema (`references/schema-bai-json.md`).

## Vì sao bài có dạng này (đọc để không phá)
- Đề cuối kỳ 5 Part: Part 1 (10 câu định nghĩa/ảnh → từ) + Part 2 (Article chép nguyên văn giáo trình → điền 1 từ, Đúng/Sai)
  + Part 3 (điền từ có hộp) = **7 điểm, toàn nhận diện**. Part 4–5 dịch = 3 điểm. Em yếu qua 5 điểm bằng Part 1–3.
- Vì vậy tab Học = 8 mục: thi gì → đoán ảnh → 20 từ ⭐ (4 cụm × 5 từ, quiz sau mỗi cụm) → Article: **đoán nghĩa từ in đậm trước**
  (cách thầy dạy: em tự dịch từ quan trọng, đoán nghĩa, rồi mới đọc và làm). Mỗi câu (thầy chốt 16/10/2026): **tối đa 2 từ đố**
  (từ ⭐/từ dễ bị đục ở Part 2), mỗi từ trắc nghiệm **3 phương án**, chọn rồi mới hiện đáp án + giải thích; **từ thường** em
  yếu cũng không biết (remove, surface, hollow…) chỉ chạm hiện nghĩa, không đố (G1/N2: đố hết thì quá tải, em bỏ). Từng câu chạm hiện dịch,
  bài tập kiểu Part 2 → 2 mẫu câu → gắn nhãn hình → SOP kiểu Part 3 → Trả bài. Tab Bài mẫu = đề 5 Part, Part 1–3 là quiz
  tự chấm, Part 4–5 bản dịch mở dần. Tab Luyện tập = 20 trắc nghiệm + 3 đúng/sai (engine đề có sẵn; không có kiểu
  "điền một từ" vì `short_answer` chỉ nhận số).
- Quy tắc trình bày thầy chốt: **mỗi ý một dòng** (chiến thuật, ghi chú, phản hồi quiz là mảng hoặc tự tách câu);
  nhãn đáp án `a. b. c. d.` chữ thường như đề thật; định nghĩa tiếng Anh giữ nguyên kiểu Part 1; không vai "thầy".
- HTML lưu DB **không chứa `<script>`/`on*=`**: quiz là radio + CSS (`.tl-quiz`), bản dịch là `<details>`, nút nghe là
  `<button data-tl-speak>` (trang bài học đọc bằng speechSynthesis).

## Quy trình

1. **Bóc chương**: `python3 .claude/skills/soan-bai-avcn/scripts/trich_chuong.py "<giáo trình.docx>" <n>` → in text chương n
   (Reading, bài tập, Vocabulary, Speaking). Giáo trình hiện hành:
   `/Users/MAC/Documents/CTTC/1 - Giảng dạy/Anh văn chuyên ngành/2026/technical english-final-2.docx`. Đề cũ để đối chiếu dạng:
   `…/AVCN (tổng hợp)/TACN (đáp án)/`.
2. **Tạo thư mục** `content/lesson-samples/avcn-chapter-<n>-<slug>/data/` và điền `bai.json` theo
   `references/schema-bai-json.md`. Hai cách:
   - Claude tự điền (mặc định, phiên Mac, không gọi API).
   - **Gemini điền**: in `references/prompt-gemini.md` kèm text chương (bước 1) cho thầy dán vào gemini.google.com; nhận JSON
     về → lưu `data/bai.json` → Claude **đối chiếu** từng định nghĩa/đáp án với giáo trình trước khi dựng (model ngoài hay
     bịa IPA và đổi nghĩa). Dữ liệu định danh sinh viên không bao giờ vào prompt.
   Chọn từ: 20 từ ⭐ = từ **chắc chắn ra Part 1** (có trong bài tập giáo trình/đề cũ), 12 từ ⭐⭐ = bộ phận/từ mô tả.
   Article: chép đúng câu giáo trình (đề Part 2 copy nguyên văn), chỉ sửa lỗi chính tả rõ ràng (sward→swarf); dịch tự soạn.
   Từ đố mỗi câu: phương án sai phải có lý (nghĩa đời thường của từ: thread = sợi chỉ, boring = nhàm chán, mill = cối xay;
   từ gần nghĩa: phôi/phoi) — không lố, không trùng nghĩa; xoay vị trí đáp án đúng a/b/c; `giai` một câu nói vì sao.
3. **Ảnh**: tìm Wikimedia Commons bằng API (mẫu lệnh trong `references/anh-commons.md`), chỉ nhận CC0 / CC BY / CC BY-SA /
   Public domain (loại NC, ND), tải bản 1000 px → WebP ≤ 150 KB vào `public/assets/avcn/chapter-<n>/<key>.webp`, ghi
   `credits.json` (file, license, author, page, w, h). Ảnh giáo trình gốc không rõ nguồn → **không dùng**. Xem ảnh bằng mắt
   (ghép contact sheet) trước khi gắn `img` trong JSON. Hình kỹ thuật (gắn nhãn) vẽ SVG, nhãn chỉ số.
4. **Dựng**: `python3 .claude/skills/soan-bai-avcn/scripts/build_avcn.py content/lesson-samples/avcn-chapter-<n>-<slug>`
   → `theory.html` + `bundle.json`. (Thư mục bài có thể giữ `build.py` 4 dòng gọi script này.)
4b. **Giọng đọc neural (từ 16/10/2026, thầy chọn en-US-AriaNeural)**: nút 🔊 phát mp3 dựng sẵn bằng Azure Speech, thiếu file thì
   tự rơi về giọng trình duyệt. Sau bước 4: `python3 .claude/skills/soan-bai-avcn/scripts/tao_giong_doc.py content/lesson-samples/avcn-chapter-<n>-<slug>`
   (ghi `public/assets/avcn/chapter-<n>/audio/*.mp3` + `audio.json`; chạy lại không sinh trùng) rồi **dựng lại** bước 4 để nút có `data-tl-audio`;
   dựng lại flashcard nếu có. Cần `AZURE_SPEECH_KEY`, `AZURE_SPEECH_REGION` trong `.env.local` (tầng F0 miễn phí ~500 nghìn ký tự/tháng,
   một chương ~5.000). `--dry-run` đếm ký tự không gọi Azure. mp3 nằm trong `public/` nên phải **commit + deploy** mới nghe được; sửa chữ trong
   bài thì chạy lại script (chuỗi mới được sinh thêm). Không dùng edge-tts trong pipeline (không chính thức, chỉ dùng thử giọng).
   **Lời nhân vật nam (thợ cả) phải là giọng nam** (thầy chốt 20/10/2026): khai `meta.boi_canh.cau_noi` + `"giong":"nam"` → build gắn
   `data-tl-giong="nam"`, script đọc bằng `AZURE_SPEECH_VOICE_NAM` (mặc định `en-US-GuyNeural`, tên file băm kèm giọng nên không đè bản nữ),
   manifest khoá `nam|chuỗi`; trang rơi về giọng máy cũng chọn giọng nam theo `data-tl-giong` (`ContentHtml.tsx`). Nhãn dòng nghe khai `boi_canh.nhan_nghe` theo vai người nói (khách/email/ghi chú ≠ "thợ cả").
5. **Kiểm** (từ gốc repo; `S=.claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts`):
   `python3 $S/lint_theory.py theory.html` · `python3 $S/check_quizzes.py theory.html` · `python3 $S/lint_do_dai.py theory.html`
   (bài từ vựng 10–13 quiz là bình thường, lỗi "quiz > 8" bỏ qua; tổng từ hiện ngay ≤ 2.200) ·
   `npx tsx $S/validate_bundle.mts <bundle.json>` phải `ok: true` · quiz tab Bài mẫu:
   `python3 -c "import json;print(''.join(w['body_html'] for w in json.load(open('bundle.json'))['worked_examples']))" > /tmp/de-mau.html && python3 $S/check_quizzes.py /tmp/de-mau.html`.
6. **Xem thử**: `bash .claude/skills/soan-bai-avcn/scripts/xem_thu.sh content/lesson-samples/avcn-chapter-<n>-<slug>` → `xem-thu/`
   (tab Học, bấm được, 🔊 đọc) + `xem-thu-de-mau/` + ảnh 375 px. **Xem ảnh bằng mắt** (giao agent `kiem-code` đọc ảnh để
   tiết kiệm token phiên chính): ảnh thẻ hiển thị, thẻ không ảnh chiếm cả hàng, bảng không bẻ chữ, số SVG đọc được.
   Gửi `xem-thu/xem-thu.html` + `xem-thu-de-mau/xem-thu.html` cho thầy duyệt.
7. **Đăng (Mac, tab terminal)**: bài đã có hàng `lessons` (migration `20261013100000_lop_avcn…` tạo 10 bài, Chapter n = `sort_order` n; từ 20/10/2026 mỗi bài nằm trong **chương riêng** cùng `sort_order` — migration `20261020190000_avcn_tach_10_chuong`, tiêu đề chương bỏ tiền tố "Chapter n:",
   9 bài còn `published=false`). Lấy id: `supabase db query --linked "select y.id,y.title,y.published from lessons y join chapters x on x.id=y.chapter_id where x.subject_code='avcn' order by y.sort_order"`.
   Rồi `npx tsx scripts/upload-lesson.mts content/lesson-samples/avcn-chapter-<n>-<slug>/bundle.json --lesson <id>` (ghi ly_thuyet,
   bai_tap_mau, exam + luyen_tap). Bật bài: `update lessons set published=true where id=<id>`. Deploy theo `scripts/deploy.sh`
   (site tĩnh, build đọc DB). Commit theo đường dẫn cụ thể.
8. **Rút kinh nghiệm** vào mục cuối file này (bắt buộc với bài có nội dung).
9. **Sửa nội dung đã đăng mà không đổi đề** (lý thuyết + bài tập mẫu, giữ kết quả HS đã làm): dựng lại bundle rồi
   `npx tsx scripts/cap-nhat-avcn-noi-dung.mts --dry-run` → `--apply` (chỉ ghi `ly_thuyet.body_html` +
   `bai_tap_mau.questions/subtitle` của 10 chương, tự sao lưu `scripts/logs/` và đối chiếu sau ghi). Sau đó deploy.

## Ranh giới
- Không chép nguyên văn giải thích của sách khác; định nghĩa Part 1 viết lại ngắn kiểu đề (một mệnh đề danh từ).
- Không thêm thưởng/xếp hạng cho lớp này; điểm luyện tập không vào bảng điểm (SDT, em yếu dám làm lại).
- Đổi dàn trang (thêm mục, đổi thứ tự) → sửa `build_avcn.py` một chỗ, không sửa HTML tay từng bài.

## Nhật ký rút kinh nghiệm
- 2026-10-13 · Bản nháp cũ (Cursor/Gemini) dùng `<script>` + `onclick` → lên web không bấm được; ảnh giáo trình 400 KB PNG không rõ nguồn → quy tắc: tương tác chỉ radio/CSS/details, ảnh chỉ Commons có giấy phép, nén WebP.
- 2026-10-13 · Ảnh chụp headless thấy ô ảnh trắng vì `loading="lazy"` → `xem_thu.sh` bỏ `loading="lazy"` trong bản xem thử (site thật vẫn lazy).
- 2026-10-13 · Phản hồi quiz bị "Đúng. Đúng." vì data lặp từ mở đầu → script tự cắt tiền tố; viết phản hồi không mở bằng "Đúng."/"Chưa đúng.".
- 2026-10-13 · Thầy nhắc lần hai quy tắc mỗi ý một dòng (chiến thuật, ghi chú) → `nl()` trong script: mảng → `<ul>`, chuỗi nhiều câu → `<br>`; khi viết JSON, chỗ nhiều ý dùng mảng.
- 2026-10-16 · Thầy góp ý: mỗi câu chỉ một từ đoán là quá ít với em yếu (cần biết ~95% từ mới hiểu câu) → mỗi câu ≤2 từ đố 3 phương án + gloss chạm-hiện cho từ thường (`cau[i][2] = {doan, nghia}`); `lint_do_dai.py` đếm sai khi `<details>` lồng nhau (báo Article dài hơn thật) — bỏ qua lỗi đó ở mục Article.
- 2026-10-16 · Link "Mở bộ Flashcard" được thêm thẳng vào DB trỏ `/flashcard/avcn-chapter-8.html` nhưng trang chưa từng được tạo → 404 → mỗi chương có `meta.flashcard` thì chạy `python3 .claude/skills/soan-bai-avcn/scripts/build_flashcard.py <thư mục bài>` (ghi `public/flashcard/…`), commit file `public/` rồi deploy; kiểm link bằng `curl` trên web thật sau deploy.
- 2026-10-16 · Sửa lý thuyết bài đã đăng: dry-run `update-ly-thuyet-from-bundle.mts` lộ hộp Flashcard ai đó thêm thẳng trên DB (link `/flashcard/avcn-chapter-8.html` đang 404) → luôn đọc khác biệt dry-run trước khi ghi, đưa phần thêm-tay vào `bai.json` thay vì ghi đè. Trang bài chỉ đối chiếu DB theo tiêu đề/cấu trúc mục, KHÔNG theo `body_html` → đổi lý thuyết xong phải `bash scripts/deploy.sh` mới hiện.
- 2026-10-16 · Chapter 5 (Fasteners) không có máy tiện → mục gắn nhãn/SOP/bảng so sánh/tiêu đề Đoán đang viết cứng cho Chapter 8 → thêm khoá tuỳ chọn (`gan_nhan.svg`, `bang`, `sop.tieu_de`, `meta.doan_tieu_de`…, xem schema); dựng lại Chapter 8 phải ra file y hệt (`cmp`) trước khi commit script.
- 2026-10-16 · Chọn 20 từ ⭐: grep đề cũ (`AVCN (tổng hợp)/đề thi 2026`, `TACN (đáp án)`) trước — Part 2 chương 5 lấy nguyên Article 2 (Bolts)/3 (Rivets) và đục grooves, helical, clockwise, Allen… → các từ đó phải là từ đố trong Article; đề mẫu câu ảnh dùng `img` thật (kiểm chéo bắt `[hình: …]` lộ đáp án); ảnh Commons cho khái niệm trừu tượng (grade, clockwise) thường không rõ ở 128 px → để thẻ không ảnh.
- 2026-10-16 · Giọng 🔊 nghe máy móc vì chỉ lấy giọng en-US đầu tiên của máy → xếp hạng giọng (Premium/Neural…) làm dự phòng, giọng chính là mp3 Azure Aria dựng sẵn (bước 4b). Thử giọng bằng trang HTML nhúng base64 ≤ 512 KB (Browser pane không mở file lớn hơn, mp3 rời không nạp được trong file pane).
- 2026-10-16 · Soạn song song 7 chương (1,2,3,4,6,7,10) bằng 7 agent, mỗi agent một chương → kiem-code soát chéo bắt được lỗi mà agent tự kiểm bỏ sót: Part 2 không nguyên văn giáo trình (câu bị viết lại), số câu/số mục ghi sai ("Mục 2" đánh từ 0 trong khi tiêu đề La Mã), phương án nhiễu cũng đúng (`ladle` có trong ảnh, `nails`, `tension`), ảnh sai vật/nền đen/lẫn vật thừa/ảnh cắt 2 lần từ cùng một nguồn → mọi bài AVCN phải qua kiem-code (tự giải lại + MỞ TỪNG ẢNH) trước khi trình thầy.
- 2026-10-16 · Ảnh cho từ ⭐⭐ trước đây không có chỗ gắn → `tu_vung_them[i].img` (thẻ ảnh trong hộp ⭐⭐). Dụng cụ/danh từ nghề là vật cụ thể thì PHẢI có ảnh thật hoặc SVG tự vẽ; `img:null` chỉ cho khái niệm trừu tượng. Ảnh tự vẽ ghi trong credits.json với page không phải Commons → script ghi "Hình tự vẽ", không ghi "Wikimedia Commons".
- 2026-10-16 · CC BY/BY-SA đòi ghi tác giả mà thẻ ảnh không có chú thích → `build_avcn.py` tự thêm mục thu gọn "Nguồn ảnh" cuối tab Học (chỉ ảnh Commons). Chương 8 đã đăng chưa có mục này: dựng lại + `cap-nhat-ly-thuyet.sh` khi thầy đồng ý.
- 2026-10-16 · Chạy nhiều agent song song: mỗi agent dùng thư mục scratch riêng (agent ghi đè `cm.py` của nhau); `xem_thu.sh` dùng Chrome nên chạy tuần tự (WebSocket đóng khi tranh nhau); `tao_giong_doc.py` đọc theory.html nên thứ tự đúng là dựng → giọng → dựng lại → flashcard; Commons trả 429 nếu gọi liên tục → sleep ≥2,5 s, tải theo `titles=`.
- 2026-10-16 · `lint_theory` báo giả "quiz #2 có 2 đáp án tl-ok" ở mọi chương có nút Flashcard (class `tl-ok` của link) — bỏ qua, `check_quizzes` mới là thước đo.
- 2026-10-20 · Mở bài bằng "Chương này cho bao nhiêu điểm" làm SV yếu thấy xa nghề → mở bằng tình huống xưởng (`meta.boi_canh`), mục tiêu + bảng Part gập lại; chương mới: chạy `scripts/sinh-boi-canh-avcn.mts` (API, ~10 lời gọi ngắn, `max_tokens` ≥6000 vì mô hình có suy nghĩ), đọc lại từng bản trước `--ap-dung`. Mẫu tình huống hơi giống nhau giữa các chương ("thợ cả nước ngoài… em đứng ngẩn") — chương sau nên đổi vai/cảnh (khách hàng, email đặt vật tư, nhãn máy, catalogue).
- 2026-10-20 · Chapter 9 (CAD/CAM): giáo trình không có hộp từ cho Vocabulary/Listening → Part 3 tự viết lại; `kiem-code` bắt được: phương án nhiễu cũng đúng (Design/Drafting khi đoạn mở bằng "Computer Aided Design"), bỏ dòng gạch đầu dòng giáo trình nhưng câu hỏi vẫn dựa vào đó, đường dẫn số trong SVG băng qua ô khác, đề mẫu Part 1 chỉ 6/10 câu, mô tả ảnh sai màu → viết bai.json bằng script Python (gen.py) để sửa hàng loạt; ghi chú mọi chỗ sửa chính tả giáo trình trong `nghia`; `.env.local` mất khoá Azure sau sự cố 17/10 nên chưa sinh mp3 (bước 4b).
- 2026-10-20 · Thầy góp ý 10 bài AVCN còn nói nhiều về điểm số (mở bài "bao nhiêu điểm", bảng "Part · 2,5 đ", "trên 7 điểm", "vẫn có điểm thành phần") → bỏ con số điểm khỏi mọi chỗ HS thấy: mở bằng `meta.boi_canh`, bảng Part chỉ nêu việc cần làm, chiến thuật Part 4–5 viết "phần đúng vẫn được ghi nhận". Số điểm chỉ giữ trong tài liệu nội bộ (skill, đề xuất). Đã cập nhật 10 chương bằng `scripts/cap-nhat-avcn-noi-dung.mts` (chỉ ly_thuyet + bai_tap_mau, sao lưu + đối chiếu sau ghi).
- 2026-10-20 · Câu mở bài có lời thoại thợ cả nhưng **không có nút nghe** (mục Trả bài lại hỏi "nghe lại câu dặn"), và mọi nút đang đọc bằng Aria nữ → khai `boi_canh.cau_noi` + `"giong":"nam"`, build gắn `data-tl-giong="nam"`, `tao_giong_doc.py` đọc bằng `AZURE_SPEECH_VOICE_NAM` (Guy) và ghi manifest khoá `nam|chuỗi`; `ContentHtml.tsx` rơi về giọng máy cũng ưu tiên giọng nam. Kiểm: `--dry-run` in dòng `nam: …`, `grep 'data-tl-giong="nam"' theory.html` = 1; thử tra manifest bằng một khoá giả rồi hoàn lại để chắc `data-tl-audio` được gắn.
- 2026-10-20 · Áp giọng nam cho **cả 10 chương**: `cau_noi` lấy đúng câu trong `tinh_huong` (ch4 không có câu thoại → tự viết 1 câu theo từ khoá của bài), `nhan_nghe` theo vai (ch1 anh kỹ sư, ch9 khách email). Sinh mp3: 9 chương thiếu 1 câu, ch9 thiếu **cả chương** (0 mp3 từ 17/10) → sinh 160 file. `lint_theory.py` báo giả "quiz #2 có 2 đáp án tl-ok" vì nút Flashcard dùng `<a class="tl-opt tl-ok">`, chặn `cap-nhat-ly-thuyet.sh` ở 7 chương → sửa lint chỉ đếm `<label … tl-opt tl-ok>` (đã thử: 2 label → báo 2, chỉ link → 1).
