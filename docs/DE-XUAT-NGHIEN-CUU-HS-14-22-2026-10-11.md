# Đề xuất cải tiến từ nghiên cứu hành vi học sinh 14–22 tuổi (11/10/2026)

Đối chiếu 5 nhóm nghiên cứu thầy gửi (CLT/Mayer, Gloria Mark, Dahl–Steinberg, Ryan–Deci, Deterding + Freeman 2014)
với những gì thachlab đã làm: `docs/QUY-TAC-THIET-KE.md` (G1–G3, N/C/M/B/H/V/D/L), `docs/PHUONG-PHAP-NOI-DUNG-LY-THUYET.md`,
`docs/ROADMAP.md` GĐ 1b, `docs/mastery-rules.md`, kho bẫy (`20261011150000/190000`), live học (`20261011210000`).
Kết luận ngắn: **nền lý thuyết đã có đủ, cái thiếu là bằng chứng và vài chỗ chưa thích ứng theo từng em.** Chưa làm gì;
chờ thầy chốt mục 5.

---

## 1. Đọc lại các nghiên cứu — chỗ tóm tắt nói quá, chỗ dùng được

| Nghiên cứu | Kết luận thật | Tóm tắt nói quá ở đâu | thachlab |
|---|---|---|---|
| Sweller 1988 (CLT); Mayer *Multimedia Learning* | 3 loại tải; nguyên tắc coherence, signaling, segmenting, redundancy, worked example (Sweller & Cooper 1985), **expertise reversal** (Kalyuga 2003: ví dụ mẫu có hại với em đã vững) | Không nói quá | Đã là nền của G1, N1–N8, hạn mức từ + `lint_do_dai.py`. **Thiếu: expertise reversal chưa thích ứng theo HS** (fading gắn cứng trong nội dung) |
| Gloria Mark (UC Irvine) | Thời gian trên một màn hình: 150 s (2004) → 75 s (2012) → **47 s (2016–2021)**. Mẫu là **nhân viên văn phòng**, không phải học sinh; phần lớn chuyển hướng là **tự ngắt**, không do thông báo | Gán "47–75 giây" cho Gen Z/Alpha là sai mẫu; "TikTok làm suy giảm kiên trì" là suy diễn (Yan 2024 EEG chỉ thấy tương quan, điểm làm bài không giảm — đã ghi ở PHUONG-PHAP §1) | Không thiết kế cho 47 giây. Thiết kế cho **ngưỡng bỏ cuộc khi chưa thấy phần thưởng** ("tới việc đầu" ≤150 từ) và **chi phí quay lại thấp** ("Tiếp tục · n/N"). Thiếu: số đo thật trên HS mình |
| Dahl & Steinberg (não vị thành niên) | Hệ viền chín trước vỏ não trước trán; **nhạy địa vị với bạn cùng lứa** hơn người lớn; nhịp ngủ lùi về khuya | Không nói quá | Đã: bảng xếp hạng chỉ so cùng bậc, Danh sách thứ Hai (ghi nhận qua thầy), ngày tính từ 3h. Thiếu: giờ gửi nhắc, "quyền được sai" nói rõ |
| Ryan & Deci (SDT); Deci–Koestner–Ryan 1999; Hanus & Fox 2015 | 3 nhu cầu tự chủ–năng lực–gắn kết. **Phần thưởng hữu hình có điều kiện làm giảm động lực nội tại** với việc vốn thú vị; huy hiệu + bảng xếp hạng trong 1 học kỳ làm **giảm** động lực và điểm (Hanus & Fox) | Tóm tắt bỏ qua rủi ro này hoàn toàn | thachlab đang ở phía rủi ro: RP, 96 huy hiệu, streak, bảng tuần, vinh danh. ROADMAP đã tự nhận "chưa có bằng chứng". GĐ 1b (so với chính em, mục tiêu lớp, bậc) đúng hướng SDT |
| Deterding et al. 2011; Sailer & Homner 2020 (meta-analysis) | Deterding chỉ **định nghĩa** gamification, không chứng minh hiệu quả. Sailer & Homner: hiệu ứng nhỏ–vừa (g ≈ 0,49 nhận thức, 0,36 động lực, 0,25 hành vi), mạnh hơn khi có **hợp tác** và **kể chuyện** | Tóm tắt dùng Deterding như bằng chứng | Mục tiêu chung lớp (hợp tác) đúng hướng; kho bẫy trộn 85% đúng (Wilson 2019) đúng hướng |
| Freeman et al. 2014 PNAS | 225 nghiên cứu **đại học** STEM: học chủ động tăng điểm +0,47 SD, rớt 21,8% vs 33,8% (×1,55). Cơ chế: làm > nghe | Áp thẳng cho THPT là ngoại suy, nhưng cơ chế bền | Tự học: bài lý thuyết có dự đoán/quiz/thí nghiệm = chủ động. **Trên lớp**: Đố vui `/choi` đã code, chưa thử |

## 2. Bản đồ: nghiên cứu → đã có / chưa có

| Nhánh | Đã có | Chưa có |
|---|---|---|
| Tải nhận thức | Hạn mức từ/mục/đoạn liền; `TheoryBlock` mở từng `<h3>`; quiz tự chấm có phân tích lỗi; hợp đồng đầu bài; nền sáng; 1 màu nhấn | Fading theo mastery; đo "mục nào HS rơi"; đề dài làm theo phần; lint hình |
| Chú ý/tự ngắt | "Tới việc đầu" ≤150 từ; "Tiếp tục n/N" nhớ chỗ dở; không toast giữa bài (B4, L6) | Số đo phiên thật (độ dài phiên, điểm rơi) |
| Não vị thành niên | Bậc, so với chính em, Danh sách thứ Hai, chuỗi có đóng băng, 3h sáng | Giờ nhắc; nhãn "không tính điểm" ở chỗ luyện |
| SDT | Mục tiêu tuần thích ứng, tiến bộ tuần, mục tiêu lớp, "đang mở khoá" thay "cần phụ đạo", live "bao nhiêu bạn đang học" | Thông báo RP mang thông tin năng lực; cho chọn giữa 2 việc; bằng chứng mùa 1 |
| Học chủ động/safe-to-fail | Luyện tự do, kho bẫy, Luyện từng câu kiểu Duolingo, 9 mô phỏng SVG, 290 thí nghiệm JSON | Phòng thí nghiệm ảo (PhET) gắn YCCĐ; Đố vui trên lớp chưa chạy thật |

## 3. Đề xuất — xếp theo giá trị ÷ công

Mỗi việc ghi: **Vì sao** (cơ chế nghiên cứu + điều đang thấy ở thachlab), **Lợi ích kỳ vọng** (có giả định, ghi rõ là
giả định — số thật chỉ có sau khi đo), **Đo bằng gì**, **Công**. Số liệu thachlab lấy từ memory: mùa 4 ngày 12/35 có
177 HS, 120 Tân Binh (68%), 71% qua cửa Tinh Anh; làm lại cùng đề 4,64 → 8,48; ngày 11/10 có 36 lượt luyện; 70 đề thi
thử 40 câu/50 phút; bài lý thuyết dài nhất 2 465 từ; 290 thí nghiệm JSON chưa có mô phỏng.

### A. Đo trước khi thêm (không migration, 0–1 ngày mỗi việc)

**A1 Số liệu mùa 1** — script chỉ đọc `scripts/do-mua-1.mts`, in 6 số của ROADMAP GĐ 1 + nền 4 tuần trước 21/9, tách
nhóm 25% thấp nhất.
- *Vì sao*: Hanus & Fox 2015 theo dõi 1 học kỳ: lớp có huy hiệu + bảng xếp hạng **giảm** động lực nội tại, giảm
  thoả mãn và giảm điểm cuối kỳ so với lớp không có; Deci–Koestner–Ryan 1999 (128 thí nghiệm): phần thưởng hữu hình
  có điều kiện làm giảm động lực nội tại, nhất là với việc vốn hấp dẫn. thachlab đã chồng 5 lớp thưởng (RP, huy hiệu,
  streak, bảng tuần, vinh danh) trong 3 tuần mà **chưa có một con số nào** cho biết nhóm dưới có học nhiều hơn hay
  bỏ nhiều hơn. Sự cố 10/10 (em 4,5 điểm nhận 90 RP) cho thấy hệ đang được chỉnh bằng cảm nhận, không bằng số.
- *Lợi ích kỳ vọng*: biết được mùa 1 làm tăng hay giảm số HS làm bài/tuần ở nhóm 25% dưới — đây là câu hỏi quyết
  định mùa 2 có giữ bảng tuần hay không. Giả định: nếu nhóm dưới giữ được ≥60% còn làm bài ở tuần 4–5 thì hệ đang
  giữ chân; dưới 40% thì hệ đang nới khoảng cách (ROADMAP GĐ 1b đã đặt ngưỡng này). Tránh được chi phí lớn nhất:
  xây thêm lớp thưởng mùa 2 trên một hệ đang làm nhóm dưới bỏ cuộc.
- *Đo*: chính 6 số đó, chạy lại mỗi tuần trong mùa 2.
- *Công*: 0,5 ngày SQL; dữ liệu đã có đủ trong `exam_results`, `practice_sessions`, `rank_rp_ledger`, `tutoring_needs`.

**A2 Ghi đoạn đang đọc về DB** — thêm cột `sections_opened jsonb` vào upsert heartbeat đã có ở `InlineLessonAccordion`.
- *Vì sao*: Nielsen 2008: người dùng đọc 20–28% chữ trên trang và rơi theo vị trí, không theo độ khó. PHUONG-PHAP §5
  nói rõ phép đo "mục nào bị bỏ" trả lời trực tiếp mọi tranh luận về độ dài, nhưng tới giờ chỉ có `localStorage`
  trên máy HS, không về DB. Hạn mức 2 000/2 500 từ đang là số rút từ 5 bài, chưa được HS xác nhận. Gloria Mark
  đo trên nhân viên văn phòng; số của HS thachlab phải tự đo.
- *Lợi ích kỳ vọng*: sau 2 tuần có bản đồ rơi theo mục cho ~60 bài đã lên web. Giả định theo F-pattern: mục IV–V
  của bài 6 mục chỉ còn 30–40% HS mở; nếu đúng thì mỗi bài soạn lại chỉ cần cắt/đảo đúng 1–2 mục đó thay vì cắt
  cả bài, tiết kiệm phần lớn công soạn lại 20 bài L12 đang treo. Nếu sai (HS đọc hết) thì bỏ luôn nỗi lo "bài dài",
  không phải cắt gì.
- *Đo*: % HS mở từng mục; tương quan với điểm quiz đoạn đó.
- *Công*: 1 cột + 10 dòng client; migration nhỏ chạy lúc nào cũng được.

**A3 Phễu bài lý thuyết** — mở bài → quiz đầu → `rank_theory_submit` → làm Luyện tập; 1 SQL + 1 bảng ở `/quan-tri/xep-hang`.
- *Vì sao*: cơ chế "phần thưởng bị trì hoãn" (PHUONG-PHAP §1) dự đoán điểm rơi lớn nhất nằm **trước việc đầu
  tiên**; mọi hạn mức "tới việc đầu ≤150 từ" đang dựa vào dự đoán đó. Phễu cho biết điểm rơi thật nằm ở đâu.
- *Lợi ích kỳ vọng*: giả định phễu điển hình 100 → 70 → 45 → 25 (mở → quiz đầu → nộp → luyện). Biết được bước nào
  mất nhiều nhất thì sửa đúng bước đó: mất ở "mở → quiz đầu" là lỗi mở bài; mất ở "nộp → luyện" là lỗi nút chuyển.
  Một sửa đúng chỗ ở bước mất 25 điểm % đáng giá hơn mọi sửa UI khác trong quý.
- *Đo*: 4 số của phễu theo bài và theo lớp.
- *Công*: 0,5 ngày.

### B. Tải nhận thức — việc nhỏ, dùng dữ liệu trang đã tải

**B1 Fading theo mastery** — `StepwiseSolution` đã có 3 mức `fading` nhưng ghi cứng theo câu; chọn theo nhãn của
`LessonMasteryCard` đã tải: Chưa đạt → lời giải đầy đủ; Cần luyện → giấu từ bước 2; Nắm vững → giấu hết + "tự giải rồi
đối chiếu".
- *Vì sao*: Sweller & Cooper 1985: người mới học bằng ví dụ có lời giải tốt hơn tự giải. Kalyuga 2003 (expertise
  reversal): **cùng ví dụ đó làm em đã vững học kém đi**, vì phải xử lý thông tin thừa so với sơ đồ đã có. Hiện
  nay bài tập mẫu hiện cùng một mức cho cả em 3 điểm và em 9 điểm; thachlab có sẵn nhãn mastery theo YCCĐ
  (`docs/mastery-rules.md`) nhưng chưa dùng nó để đổi cách hiện. Thầy cũng chốt (AI-TUTOR 9.3): em đã hiểu thì
  "gấp vở tự giải", không nhìn lời giải.
- *Lợi ích kỳ vọng*: giả định lớp chia 30% Chưa đạt / 45% Cần luyện / 25% Nắm vững theo YCCĐ. Nhóm 25% trên chuyển
  từ "đọc lời giải" (nhóm nhớ ~36% ở Karpicke & Roediger 2008) sang "tự giải rồi đối chiếu" (nhóm ~80%) — ngay trên
  bài tập mẫu đang có, không cần soạn thêm. Nhóm dưới vẫn thấy đủ lời giải, không mất gì. Kỳ vọng điểm câu Khó
  cùng YCCĐ của nhóm trên tăng sau 3 tuần; bài tập mẫu bớt "đọc rồi quên".
- *Đo*: so mastery YCCĐ trước/sau cho nhóm Nắm vững; tỉ lệ bấm "đối chiếu" sau khi tự giải.
- *Công*: client-only, 0,5–1 ngày; không RPC mới (mastery đã tải trên trang bài).

**B2 Đề dài làm theo phần** — chế độ "Luyện theo phần" chỉ cho mục Luyện tập; dùng `groupQuestionIndexesByType` đã
chia Phần I/II/III; mỗi phần một lượt, lưu dở bằng exam resume đã có; chấm không đổi.
- *Vì sao*: Mayer & Chandler 2001 (segmenting): chia theo nhịp người học kiểm soát tăng chuyển giao kiến thức.
  Kivetz–Urminsky–Zheng 2006 (goal-gradient): càng gần đích càng nỗ lực; đích 40 câu ở xa hơn đích 18 câu Phần I.
  Thực tế thachlab: 70 đề thi thử 40 câu/50 phút được bật làm nguồn RP, HS làm trên điện thoại buổi tối, có Zalo
  chạy nền (QUY-TAC §0). Một lượt 50 phút liền là đúng loại việc mà Yan 2024 nói HS "làm được nhưng phải cố nhiều
  hơn". Delgado 2018: đọc màn hình kém giấy **nhất là khi dài và có áp lực thời gian** — đề thi thử trúng cả hai.
- *Lợi ích kỳ vọng*: giả định hiện ~40% lượt mở đề thi thử bị bỏ dở (cần kiểm bằng `exam_results` chưa nộp / exam
  resume). Chia 3 phần đưa mỗi lượt về 12–18 câu, 15–20 phút; kỳ vọng tỉ lệ hoàn thành trọn đề tăng lên 60–70%
  vì mỗi phần đều "đóng" được trong một lần ngồi. Phụ: dữ liệu theo phần cho biết em yếu Phần II (đúng–sai) hay
  Phần III (trả lời ngắn) — đúng cấu trúc đề tốt nghiệp từ 2025.
- *Đo*: tỉ lệ nộp trọn đề/lượt mở, trước và sau; điểm trung bình theo phần.
- *Công*: 1–2 ngày client; không migration (exam resume đã lưu trạng thái).
- *Ràng buộc*: Kiểm tra giữ nguyên một lượt (năng lực làm liền 50 phút vẫn phải rèn — PHUONG-PHAP §1 điểm cân bằng).

**B3 Lint hình** — thêm vào `lint_theory.py`: SVG >3 màu, chữ <13px ở 360px, `<figure>` thiếu `figcaption`, hình không
được chữ tham chiếu.
- *Vì sao*: Harp & Mayer 1998 (seductive details): hình/chi tiết hấp dẫn nhưng không phục vụ ý chính làm **giảm**
  nhớ và vận dụng. Quy tắc H1/H4 đã có nhưng chỉ kiểm bằng mắt; `lint_do_dai` đã chứng minh một cổng tự động chặn
  được phình chữ (bài Mô tả sóng từ 3 021 về 2 457 từ) — hình chưa có cổng tương đương, và 13 bài L12 soạn bằng
  subagent song song đều có lỗi hình phải sửa 1–2 vòng.
- *Lợi ích kỳ vọng*: mỗi đợt 4–13 bài giảm một vòng kiểm chéo hình (tiết kiệm ~1/3 lượt subagent của đợt 4/10:
  ~50 lượt). Chất lượng ổn định không phụ thuộc người soạn.
- *Đo*: số lỗi hình kiểm chéo bắt được ở đợt kế.
- *Công*: 0,5 ngày Python.

### C. Động lực — sửa cái có, không thêm lớp (đúng nguyên tắc GĐ 1)

**C1 Thông báo RP mang thông tin năng lực** — đổi chuỗi trong `notify_rp_thuong`: "+20 RP · đúng 8/10 câu *Động lượng –
va chạm mềm*, hơn tuần trước 2 câu".
- *Vì sao*: SDT phân biệt phần thưởng **kiểm soát** ("làm đi thì được điểm") và phần thưởng **thông tin** ("em vừa
  làm được điều này"). Deci 1999: loại kiểm soát làm giảm động lực nội tại; loại thông tin nuôi nhu cầu năng lực và
  không gây hại. Cùng 20 RP, chỉ khác câu chữ. Hattie & Timperley 2007: phản hồi hiệu quả nhất trả lời "em đang ở
  đâu, đi đâu tiếp" — con số RP không trả lời câu nào trong hai câu đó.
- *Lợi ích kỳ vọng*: không thêm RP, không thêm bảng; biến mỗi thông báo thành một lần ghi nhận năng lực theo YCCĐ.
  Giả định: với ~177 HS × ~3 thông báo/tuần = ~500 điểm chạm/tuần đổi nội dung mà không tốn gì ở phía HS. Kỳ vọng
  tỉ lệ bấm vào thông báo rồi mở bài tăng; lâu dài giảm phần rủi ro Hanus & Fox mà không phải tắt RP.
- *Đo*: tỉ lệ mở thông báo → vào bài trong 10 phút, trước/sau.
- *Công*: 0,5 ngày SQL (hàm đã có, dữ liệu YCCĐ có trong `exam_question_results`).

**C2 "Quyền được sai" nói rõ** — nhãn "Luyện tự do — không tính điểm, không ghi sổ"; màn kết quả luyện thêm 1 dòng
"Sai ở đây rẻ hơn sai trong đề; 3 câu này sẽ quay lại sau 2 ngày".
- *Vì sao*: Dahl–Steinberg: tuổi này nhạy với đánh giá của bạn/thầy, nên "sai có bị ghi không" là câu hỏi ngầm quyết
  định em có dám bấm thử không. thachlab **đã** có cơ chế đúng (luyện tự do không ghi; kho bẫy trộn 85% đúng theo
  Wilson 2019; lượt đầu mới tính RP) nhưng không nói ra trên màn hình, nên với HS mọi nút đều "có vẻ" tính điểm.
  Dweck: thông điệp "sai là bước của việc học" chỉ có tác dụng khi gắn vào hành động cụ thể, không phải khẩu hiệu.
- *Lợi ích kỳ vọng*: giả định nhóm 25% dưới hiện né luyện vì sợ sai; nói rõ "không tính" kỳ vọng tăng số lượt
  luyện tự do của nhóm này. Số 11/10 cho thấy 36 lượt luyện/ngày cho ~177 HS, tức ~1/5 HS luyện mỗi ngày — còn
  nhiều chỗ tăng. Chi phí gần bằng 0.
- *Đo*: lượt luyện tự do/tuần của nhóm 25% dưới; % câu bẫy được ôn đúng hạn.
- *Công*: vài giờ, chỉ chữ.

**C3 Tự chủ tối thiểu** — khi việc chính của `TodayCard` là "mở khoá chủ đề", cho chọn 1 trong 2 chủ đề yếu
(`WeakestSkillsCard` đã có 3).
- *Vì sao*: SDT: tự chủ là nhu cầu đầu tiên; Patall, Cooper & Robinson 2008 (meta-analysis về lựa chọn): được chọn
  giữa vài phương án tương đương tăng động lực nội tại và nỗ lực, hiệu ứng mạnh nhất khi 2–4 lựa chọn (quá nhiều
  thì ngược lại — Iyengar & Lepper 2000, đúng với N2). Hiện TodayCard đưa 1 lệnh; một lệnh với HS 15 tuổi dễ đọc
  thành "bị bắt".
- *Lợi ích kỳ vọng*: giả định tỉ lệ bấm nút chính của TodayCard hiện ~30%; cho chọn 1/2 kỳ vọng nhích lên vài
  điểm % mà không tăng tải (vẫn 1 nút nổi, 2 lựa chọn tương đương). Cả hai lựa chọn đều là chủ đề yếu nên dù chọn
  gì cũng đúng việc cần làm.
- *Đo*: tỉ lệ bấm nút chính TodayCard, trước/sau.
- *Công*: vài giờ client.

**C4 Giờ nhắc (M4 push)** — mặc định 20h, không gửi sau 22h, HS tự đổi.
- *Vì sao*: Dahl 2004, Carskadon: nhịp sinh học tuổi vị thành niên lùi về khuya, nhiều em học 23h–1h (thachlab đã
  tính ngày từ 3h sáng vì thế). Nhưng nhắc sau 22h chỉ làm em mở điện thoại rồi sang TikTok (Stothart 2015: thông
  báo chưa mở cũng đã kéo chú ý). Nhắc 20h rơi vào lúc em còn ở bàn học.
- *Lợi ích kỳ vọng*: tránh tiếng xấu "web làm phiền" từ phụ huynh (UI phụ huynh 45–60 đang xây); tỉ lệ mở nhắc →
  làm bài cao hơn so với nhắc khuya. Giả định: nhắc 20h có tỉ lệ vào bài gấp đôi nhắc 23h.
- *Đo*: tỉ lệ nhắc → vào bài trong 30 phút theo giờ gửi.
- *Công*: 0 thêm so với spec M4 (chỉ mặc định).

**C5 Không thêm huy hiệu/thành tích/bảng mới** tới khi A1 có số; nếu 3 số nhóm 25% không nhúc nhích, tắt bảng tuần
cho nhóm dưới trước, giữ tiến bộ tuần.
- *Vì sao*: Hanus & Fox chỉ tìm thấy tác hại ở **bảng xếp hạng + huy hiệu**, không ở phản hồi tiến bộ cá nhân;
  Steinberg: so sánh địa vị với bạn là thứ tuổi này nhạy nhất — em đứng cuối bảng tuần biết rõ mình đứng cuối dù
  đã giấu số thứ tự. ROADMAP GĐ 1 đã đặt nguyên tắc "không thêm lớp động lực mới tới hết mùa 1"; mục này chỉ nói rõ
  **cắt cái gì trước** nếu số xấu.
- *Lợi ích kỳ vọng*: tránh mùa 2 lặp sai lầm có tên trong tài liệu. Giả định: nếu phải tắt, nhóm dưới mất 0 (họ
  không lên bảng), nhóm trên mất một kênh khoe nhưng còn danh hiệu + vinh danh thầy đọc tên.
- *Đo*: như A1.
- *Công*: 0.

### D. Học chủ động / phòng thí nghiệm ảo (Freeman; safe-to-fail)

**D1 PhET nhúng** — 5 sim khớp chương đang dạy: Dao động L11 (*Masses and Springs*, *Pendulum Lab*), Động học L10
(*Projectile Motion*), L12 (*Faraday's Law*, *Gas Properties*). Mỗi sim là một hộp `.tl-box--exp` Làm–Quan sát–Rút ra
với 3 nhiệm vụ đổi thông số + 3 câu gắn YCCĐ; iframe nạp khi bấm (V5).
- *Vì sao*: Freeman 2014: làm > nghe. "Quyền được sai" (Dahl–Steinberg, SDT năng lực): phòng thí nghiệm ảo cho
  em thử sai không bị chấm; PhET được thiết kế đúng theo nguyên tắc tối giản của Mayer (chỉ làm nổi đại lượng cần
  quan sát — Wieman, Adams & Perkins 2008). thachlab có 290 thí nghiệm JSON ghi sẵn nhưng mới 9 mô phỏng SVG tự
  viết, mỗi cái tốn nhiều ngày; ROADMAP đặt GĐ 3 từ Q1/2027 với 1–2 mô phỏng/tháng. PhET miễn phí, HTML5, có bản
  tiếng Việt, chạy trên điện thoại — 5 sim này phủ đúng 3 chương đang dạy mà không viết mô phỏng nào.
- *Lợi ích kỳ vọng*: kéo GĐ 3 sớm 3 tháng với công ~1 ngày/sim (viết 3 nhiệm vụ + 3 câu YCCĐ), thay vì ~1 tuần/sim
  tự viết. Giả định: bài có sim được HS mở lâu hơn và quiz YCCĐ liên quan có tỉ lệ đúng cao hơn bài không có; nếu
  không thấy khác biệt sau 1 tháng thì dừng, không mất công viết mô phỏng riêng.
- *Đo*: % HS bấm mở sim; mastery YCCĐ gắn sim trước/sau; thời gian trên bài.
- *Ràng buộc*: giữ điều kiện ROADMAP "mô phỏng phải gắn bài + bộ câu"; iframe ~2–5 MB nên bắt buộc nạp khi bấm; cần
  thầy duyệt 3 nhiệm vụ/sim vì đó là nội dung dạy.
- *Công*: 1 ngày/sim; không migration (hộp nằm trong `body_html`, câu vào ngân hàng theo quy trình có sẵn).

**D2 Đố vui lớp học `/choi`** — thử 2 điện thoại (đang treo) rồi dùng 5 phút mỗi tiết.
- *Vì sao*: đây chính là dạng "active learning" Freeman đo (câu hỏi trong giờ, cả lớp trả lời, chữa ngay). Roediger
  & Karpicke 2006: truy xuất trong giờ nhớ lâu hơn nghe lại. Code đã có, migration `20261006150000_quiz_live` chưa
  rõ đã chạy — là việc rẻ nhất trong danh sách vì chỉ cần thử.
- *Lợi ích kỳ vọng*: giả định 5 phút/tiết × 3 tiết/tuần = 15 phút truy xuất có phản hồi tức thì cho cả lớp; mỗi câu
  đố ghi được kết quả theo YCCĐ (nếu gắn), nuôi luôn mastery và kho bẫy mà không cần em tự làm ở nhà. Nhóm 25% dưới
  được truy xuất trong giờ — nơi duy nhất chắc chắn có mặt.
- *Đo*: số tiết dùng/tuần; tỉ lệ đúng theo câu; mastery YCCĐ của nhóm dưới sau 1 tháng.
- *Công*: 0 code, 1 buổi thử.

**D3 Bài toán kịch bản** — mỗi chương một "Thử thách ⭐⭐⭐" dạng điều tra; đã nằm trong skill, chỉ nhắc khi soạn.
- *Vì sao*: PBL hiệu quả ở mức vận dụng, không thay được luyện cơ bản (Kirschner, Sweller & Clark 2006 cảnh báo
  PBL với người mới). Nên để ở ⭐⭐⭐ cuối bài, đúng chỗ của em đã vững.
- *Lợi ích kỳ vọng*: cho nhóm trên một lý do ở lại bài sau khi xong quiz; không ảnh hưởng nhóm dưới.
- *Công*: 0 mới.

### E. Sinh viên 18–22 (CNC/CTTC)
ROADMAP đóng băng CNC. Ghi một ý để sau: lớp đảo ngược = đăng lý thuyết + quiz trước buổi, điểm danh bằng quiz
(Freeman áp đúng lứa này). Không làm bây giờ.

### Tóm tắt lợi ích theo nhóm (giả định)

| Nhóm HS | Việc tác động trực tiếp | Kỳ vọng |
|---|---|---|
| 25% dưới | C2, C5, D2, C1 | dám luyện vì không bị ghi; truy xuất trong giờ; không bị bảng tuần đè |
| 50% giữa | B2, C3, A2→sửa bài, D1 | hoàn thành đề dài; chọn việc; bài ngắn đúng chỗ; thí nghiệm ảo |
| 25% trên | B1, D3 | tự giải thay vì đọc lời giải; thử thách |
| Thầy | A1, A3, B3 | quyết mùa 2 bằng số; biết bước nào mất HS; bớt vòng kiểm hình |

## 4. Không nên làm (dù tóm tắt gợi ý)
- **Cắt bài thành clip 5–7 phút / "TikTok hoá"**: PHUONG-PHAP §1 "điểm cân bằng" — đề thi vẫn đòi đọc liền 10–20 phút; giữ bài toán mẫu buộc đọc liền. Video ngắn chỉ là cửa vào (§4.5).
- **Đồng hồ Pomodoro trong app**: thêm chuyển động + tải ngoại lai khi đang đọc (B4, N1). B2 (làm theo phần) đạt cùng mục đích mà không thêm gì lên màn hình.
- **Mô phỏng 3D**: nặng JS trên điện thoại; SVG + PhET đủ cho THPT.
- **Thêm lớp động lực mới** trước khi có A1.

## 5. Thứ tự làm (chốt đề xuất 11/10/2026)

Tiêu chí xếp: (1) có hạn — mùa 1 hết 25/10; (2) việc đo đứng trước việc sửa vì sửa mù là lãng phí; (3) giá trị ÷ công;
(4) việc không migration đi trước việc có migration; (5) việc cần thầy duyệt nội dung xếp sau để thầy có thời gian xem.

| # | Việc | Vì sao đứng ở đây | Công | Phụ thuộc |
|---|---|---|---|---|
| 1 | **D2** thử Đố vui `/choi` 2 điện thoại | 0 code, chỉ kiểm migration `20261006150000_quiz_live` đã chạy chưa rồi thử; dùng được ngay tuần này trên lớp | 1 buổi | — |
| 2 | **A1** script đo mùa 1 | Có hạn 25/10; mọi quyết định mùa 2 (C5) đi từ số này; chỉ SQL đọc | 0,5 ngày | — |
| 3 | **C2** nhãn "không tính điểm" + dòng kết quả luyện | Chỉ chữ, tác động thẳng nhóm 25% dưới, không rủi ro | vài giờ | — |
| 4 | **A2** ghi đoạn đang đọc vào heartbeat | Migration nhỏ, cần chạy sớm để tới cuối tháng có 2 tuần dữ liệu cho việc soạn lại 20 bài L12 | 0,5 ngày | migration 1 cột |
| 5 | **A3** phễu bài lý thuyết | Dữ liệu đã có, 1 SQL; đọc cùng A2 mới biết sửa bài ở đâu | 0,5 ngày | — |
| 6 | **C1** thông báo RP kèm thông tin YCCĐ | Chỉ đổi chuỗi trong hàm; làm sau A1 để không lẫn tác động vào số mùa 1 | 0,5 ngày | sau A1 chốt số |
| 7 | **B1** fading theo mastery | Client-only, lợi cho nhóm trên; cần vài ngày thử bằng tài khoản HS trước khi deploy | 1 ngày | — |
| 8 | **C3** chọn 1 trong 2 chủ đề yếu ở TodayCard | Nhỏ, nhưng TodayCard vừa sửa 7/10 nên để ổn định trước | vài giờ | — |
| 9 | **C5** quyết mùa 2 từ số A1 | Chỉ làm được sau 25/10 khi có đủ 5 tuần | 0 | A1 |
| 10 | **B2** luyện đề dài theo phần | Giá trị cao nhưng công 1–2 ngày và đụng ExamRunner (file nhạy, có bug chuyển câu chưa rõ) — làm khi mùa 1 đã chốt | 1–2 ngày | — |
| 11 | **D1** PhET sim đầu: Dao động L11 | Cần thầy duyệt 3 nhiệm vụ + 3 câu YCCĐ; chương đang dạy nên làm trước Động học L10 | 1 ngày/sim | thầy duyệt nội dung |
| 12 | **B3** lint hình | Chỉ cần trước đợt soạn bài kế (Đợt 1 L11 Dao động) | 0,5 ngày | — |
| 13 | **C4** giờ nhắc mặc định 20h | Gắn vào M4 push, M4 chưa làm (còn VAPID + deploy) | 0 thêm | M4 |
| 14 | **D3**, **E** | Chỉ nhắc khi soạn / để sau | 0 | — |

Theo tuần: **tuần 1 (→18/10)** #1–#5 · **tuần 2 (→25/10)** #6–#8 · **tuần 3–4** #9–#12 · **sau** #13–#14.
Việc nào thầy không đồng ý thì gạch, thứ tự còn lại giữ nguyên.

## 6. Nguồn
Sweller 1988; Sweller & Cooper 1985; Kalyuga, Ayres, Chandler & Sweller 2003 (expertise reversal); Mayer *Multimedia Learning* 2009/2020 ·
Mark, G. *Attention Span* 2023 (47 s, mẫu nhân viên văn phòng); Yan et al. 2024 *Front. Hum. Neurosci.* ·
Dahl 2004 *Ann. N.Y. Acad. Sci.*; Steinberg 2008 *Dev. Rev.*; Blakemore & Mills 2014 ·
Ryan & Deci 2000 *Am. Psychol.*; Deci, Koestner & Ryan 1999 *Psychol. Bull.*; Hanus & Fox 2015 *Computers & Education* ·
Deterding, Dixon, Khaled & Nacke 2011; Sailer & Homner 2020 *Educ. Psychol. Rev.* ·
Freeman et al. 2014 *PNAS* 111(23) · Wilson et al. 2019 *Nat. Commun.* (85% rule) · Karpicke & Roediger 2008 *Science* ·
Patall, Cooper & Robinson 2008 *Psychol. Bull.* (lựa chọn) · Wieman, Adams & Perkins 2008 *Science* (PhET) ·
Kirschner, Sweller & Clark 2006 *Educ. Psychol.* (giới hạn PBL) · Hattie & Timperley 2007 *Rev. Educ. Res.* · Delgado et al. 2018.
