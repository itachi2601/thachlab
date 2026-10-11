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

### A. Đo trước khi thêm (không migration, 0–1 ngày mỗi việc)
- **A1 Số liệu mùa 1** (hết 25/10, còn 2 tuần): script chỉ đọc `scripts/do-mua-1.mts` in 6 số của ROADMAP GĐ 1 (HS làm bài/tuần, bài/HS, % nhận ≥1 danh hiệu 2 tuần đầu, % còn làm ở tuần 4–5, số vào phụ đạo, tỉ lệ thoát) + nền 4 tuần trước 21/9, tách riêng nhóm 25% thấp nhất (tab "Đo nhóm thấp" đã có). Đây là thứ Hanus & Fox đòi; mọi quyết định mùa 2 (C5) đi từ đây.
- **A2 Ghi đoạn đang đọc về DB**: heartbeat `student_learning_presence` đã chạy từ `InlineLessonAccordion`; thêm 1 cột `sections_opened jsonb` vào chính lệnh upsert đó (không thêm round-trip). Từ đó biết mục nào HS rơi — trả lời "bài dài quá không" bằng số thay cho con số 47 giây. Là nợ ở PHUONG-PHAP §7.
- **A3 Phễu bài lý thuyết**: mở bài → tới quiz đầu → `rank_theory_submit` → làm Luyện tập. Dữ liệu đã có (presence, `rank_theory_*`, `practice_sessions`); chỉ 1 SQL + 1 bảng ở `/quan-tri/xep-hang`.

### B. Tải nhận thức — việc nhỏ, dùng dữ liệu trang đã tải
- **B1 Fading theo mastery** (Kalyuga; N6): `StepwiseSolution` đã có 3 mức `fading` nhưng ghi cứng theo câu. Chọn mức theo `LessonMasteryCard` đã tải trên trang: Chưa đạt → lời giải đầy đủ; Cần luyện → giấu từ bước 2; Nắm vững → giấu hết + nút "tự giải rồi đối chiếu" (AI-TUTOR 9.3). Client-only, không RPC mới.
- **B2 Đề dài làm theo phần** (segmenting; goal-gradient): 70 đề thi thử 40 câu/50 phút trên điện thoại buổi tối. `groupQuestionIndexesByType` đã chia Phần I/II/III; thêm chế độ "Luyện theo phần" **chỉ cho mục Luyện tập** (Kiểm tra giữ nguyên): mỗi phần một lượt, lưu dở (exam resume đã có), chấm không đổi.
- **B3 Lint hình** (H1, H4): `lint_theory.py` chưa kiểm hình. Thêm: SVG >3 màu, chữ <13px ở 360px, `<figure>` thiếu `figcaption`, hình không được tham chiếu trong chữ. Chặn phình hình như `lint_do_dai` đã chặn chữ.

### C. Động lực — sửa cái có, không thêm lớp (đúng nguyên tắc GĐ 1)
- **C1 Thông báo RP mang thông tin năng lực** (Deci: phần thưởng *thông tin* ít hại hơn phần thưởng *kiểm soát*): `notify_rp_thuong` đổi câu "+20 RP" → "+20 RP · đúng 8/10 câu *Động lượng – va chạm mềm*, hơn tuần trước 2 câu". Chỉ đổi chuỗi trong hàm đã có; dữ liệu YCCĐ có trong `exam_question_results`.
- **C2 "Quyền được sai" nói rõ**: nhãn "Luyện tự do — không tính điểm, không ghi sổ" ở thang luyện; màn kết quả luyện thêm 1 dòng L4 "Sai ở đây rẻ hơn sai trong đề; 3 câu này sẽ quay lại sau 2 ngày". Kho bẫy đã đúng cơ chế, chỉ thiếu lời nói ra.
- **C3 Tự chủ tối thiểu**: `TodayCard` giữ 1 nút nổi; khi việc chính là "mở khoá chủ đề", cho chọn 1 trong 2 chủ đề yếu (`WeakestSkillsCard` đã có 3). Chọn giữa 2 việc tương đương = tự chủ mà không tăng tải (N2).
- **C4 Giờ nhắc** (M4 push, chưa làm): mặc định 20h, không gửi sau 22h, HS tự đổi. Dahl: ép nhịp ngủ ngược lại chỉ tốn tin nhắn.
- **C5 Không thêm huy hiệu/thành tích/bảng mới** tới khi A1 có số. Nếu 3 số nhóm 25% không nhúc nhích: **tắt bảng tuần cho nhóm dưới trước**, giữ tiến bộ tuần (Hanus & Fox chỉ đúng với bảng xếp hạng, không với phản hồi tiến bộ).

### D. Học chủ động / phòng thí nghiệm ảo (Freeman; safe-to-fail)
- **D1 PhET nhúng** (kéo sớm GĐ 3, không viết mô phỏng mới): 5 sim khớp chương đang dạy — Dao động L11 (*Masses and Springs*, *Pendulum Lab*), Động học L10 (*Projectile Motion*), L12 (*Faraday's Law*, *Gas Properties*); PhET có bản tiếng Việt, HTML5, miễn phí. Mỗi sim là một hộp `.tl-box--exp` Làm–Quan sát–Rút ra với 3 nhiệm vụ đổi thông số + 3 câu gắn YCCĐ; iframe nạp khi bấm (V5). Giữ điều kiện ROADMAP "mô phỏng phải gắn bài + bộ câu".
- **D2 Đố vui lớp học `/choi`**: thử 2 điện thoại (đang treo) rồi dùng 5 phút mỗi tiết. Đây chính là thứ Freeman đo, và là việc rẻ nhất vì code đã có.
- **D3 Bài toán kịch bản**: mỗi chương một "Thử thách ⭐⭐⭐" dạng điều tra — đã nằm trong skill `soan-bai-ly-thuyet-tuong-tac`, chỉ nhắc khi soạn, không việc mới.

### E. Sinh viên 18–22 (CNC/CTTC)
ROADMAP đóng băng CNC. Ghi một ý để sau: lớp đảo ngược = đăng lý thuyết + quiz trước buổi, điểm danh bằng quiz. Không làm bây giờ.

## 4. Không nên làm (dù tóm tắt gợi ý)
- **Cắt bài thành clip 5–7 phút / "TikTok hoá"**: PHUONG-PHAP §1 "điểm cân bằng" — đề thi vẫn đòi đọc liền 10–20 phút; giữ bài toán mẫu buộc đọc liền. Video ngắn chỉ là cửa vào (§4.5).
- **Đồng hồ Pomodoro trong app**: thêm chuyển động + tải ngoại lai khi đang đọc (B4, N1). B2 (làm theo phần) đạt cùng mục đích mà không thêm gì lên màn hình.
- **Mô phỏng 3D**: nặng JS trên điện thoại; SVG + PhET đủ cho THPT.
- **Thêm lớp động lực mới** trước khi có A1.

## 5. Thứ tự 4 tuần (chờ thầy chốt)
| Tuần | Việc | Ghi chú |
|---|---|---|
| 1 (→18/10) | A1, A2, D2 | A1 phải xong trước 25/10 để có nền mùa 2 |
| 2 (→25/10) | A3, C1, C2, B1 | đều client/SQL đọc, không migration trừ A2 (1 cột) |
| 3–4 | quyết mùa 2 từ A1 (C5); B2; D1 sim đầu (Dao động L11 đang dạy) | D1 cần thầy duyệt 3 nhiệm vụ/sim |

## 6. Nguồn
Sweller 1988; Sweller & Cooper 1985; Kalyuga, Ayres, Chandler & Sweller 2003 (expertise reversal); Mayer *Multimedia Learning* 2009/2020 ·
Mark, G. *Attention Span* 2023 (47 s, mẫu nhân viên văn phòng); Yan et al. 2024 *Front. Hum. Neurosci.* ·
Dahl 2004 *Ann. N.Y. Acad. Sci.*; Steinberg 2008 *Dev. Rev.*; Blakemore & Mills 2014 ·
Ryan & Deci 2000 *Am. Psychol.*; Deci, Koestner & Ryan 1999 *Psychol. Bull.*; Hanus & Fox 2015 *Computers & Education* ·
Deterding, Dixon, Khaled & Nacke 2011; Sailer & Homner 2020 *Educ. Psychol. Rev.* ·
Freeman et al. 2014 *PNAS* 111(23) · Wilson et al. 2019 *Nat. Commun.* (85% rule) · Karpicke & Roediger 2008 *Science*.
