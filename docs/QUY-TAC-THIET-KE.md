# Quy tắc thiết kế giao diện học sinh — dựa trên nghiên cứu tâm lý & thị giác

**Bắt buộc đọc trước khi tạo/sửa bất kỳ UI nào học sinh nhìn thấy** (`/lop-hoc/**`, `/kiem-tra/**`,
trang chủ HS, bảng xếp hạng, phụ đạo, thông báo). Mọi đề xuất hay thay đổi UI phải **nêu mã quy tắc**
(ví dụ `N2`, `C3`) thay vì tranh luận lại từ đầu; nếu cố ý phá quy tắc thì ghi lý do ngay trong PR/commit.
Thầy không cần nhắc lại các lưu ý này nữa — thiếu là lỗi của agent.

Người dùng mục tiêu: học sinh 14–18 tuổi, học chủ yếu trên **điện thoại 360–430px**, thường học buổi tối,
vừa học vừa có Zalo/TikTok chạy nền, ý chí tập trung có hạn. Giáo viên là người dùng phụ.

---

## 0. Ba nguyên lý gốc (mọi quy tắc bên dưới suy ra từ đây)

| Mã | Nguyên lý | Nghiên cứu nền |
|---|---|---|
| G1 | **Trí nhớ làm việc rất hẹp**: chỉ giữ được ~4 khối thông tin cùng lúc. Mọi thứ trên màn hình không phục vụ việc đang học đều chiếm chỗ của bài. | Cowan 2001 (4±1 chunk); Sweller 1988, Lí thuyết tải nhận thức |
| G2 | **Não tuổi vị thành niên nhạy với phần thưởng/mới lạ hơn khả năng tự kiềm chế**: huy hiệu, thông báo, chuyển động, màu sặc sỡ kéo chú ý mạnh hơn người lớn và khó quay lại bài hơn. | Steinberg 2008 & Casey–Jones–Hare 2008 (mô hình hai hệ thống); Stothart–Mitchum–Yehnert 2015 (thông báo chưa mở cũng làm giảm chú ý) |
| G3 | **Học bằng mắt là quét, không phải đọc hết**: người dùng đọc ~20–28% chữ trên trang, quét theo hình F/ lớp, dừng ở chỗ nổi bật. Thiết kế phải quyết định *chỗ nào* mắt dừng, không để ngẫu nhiên. | Nielsen 2006/2008 (F-pattern, tỉ lệ đọc); Treisman & Gelade 1980 (chú ý tiền ý thức với màu/chuyển động) |

---

## 1. Tải nhận thức (N) — ít thứ hơn, đúng lúc hơn

- **N1 Một màn hình = một việc.** Trang đang *đọc lý thuyết* chỉ hiện lý thuyết + điều hướng tối thiểu. Công cụ cho việc khác (trình chiếu, ghi chú, câu sai, xếp hạng) ẩn sau 1 chạm hoặc để cuối. *Mayer – nguyên tắc mạch lạc (coherence): bỏ chi tiết hấp dẫn nhưng không liên quan làm tăng điểm nhớ & vận dụng; Harp & Mayer 1998 "seductive details".*
- **N2 Tối đa 4 lựa chọn/thao tác nhìn thấy cùng lúc** ở mỗi vùng (thanh tab, thanh đáy, toolbar). Nhiều hơn → gom vào "Thêm". *Hick 1952 (thời gian chọn tăng theo log số lựa chọn); Iyengar & Lepper 2000 (quá tải lựa chọn làm giảm hành động).*
- **N3 Không hiện trạng thái rỗng dưới dạng thẻ.** "Chưa có câu sai nào", "Chỗ này em chưa hiểu…" khi chưa có dữ liệu là nhiễu thuần tuý (G1). Ẩn hẳn hoặc gộp thành 1 dòng mờ.
- **N4 Không lặp thông tin.** Tiêu đề bài không xuất hiện 3 lần (breadcrumb + h1 + tab title); mục lục chương không chiếm cả cột khi đang ở trong bài (đã có ở trang lớp). *Mayer – nguyên tắc dư thừa (redundancy).*
- **N5 Chia nhỏ theo nhịp người học kiểm soát** (segmenting): mục lý thuyết dài chia theo mốc I/II/III, mỗi mốc có tiêu đề + 1 câu hỏi kiểm tra nhanh; học sinh bấm "tiếp" chứ không cuộn vô tận. *Mayer & Chandler 2001.*
- **N6 Ví dụ có lời giải trước bài tự làm**, rồi giảm dần gợi ý (fading). Người mới học bằng ví dụ mẫu hiệu quả hơn tự giải; người đã vững thì ngược lại → bài tập mẫu thu gọn được cho HS đã đạt mastery. *Sweller & Cooper 1985 (worked-example effect); Kalyuga 2003 (expertise reversal).*
- **N7 Báo hiệu (signaling) đúng 1 cấp**: từ khoá in đậm, công thức đóng khung, kết luận có nền nhạt — nhưng mỗi đoạn chỉ 1 kiểu nhấn. Nhấn mọi thứ = không nhấn gì. *Mayer – signaling; Von Restorff 1933 (hiệu ứng cô lập chỉ có khi phần tử nổi bật là *duy nhất*).*
- **N8 Chữ và hình phải ở cạnh nhau** (hình ngay dưới/bên câu nó minh hoạ, chú thích gắn vào hình, không bắt mắt nhảy qua lại). *Chandler & Sweller 1992 (split-attention); Mayer – spatial contiguity.*

## 2. Đọc & chữ (C)

- **C1 Cỡ chữ thân bài 16–18px trên điện thoại, 17–18px desktop; không bao giờ < 14px cho chữ cần đọc** (chú thích, nhãn mục lục vẫn ≥ 13px). Tiếng Việt có dấu chồng tầng cần `line-height ≥ 1.55` để dấu không chạm dòng trên. *WCAG 1.4.12 (line-height ≥ 1.5); Legge & Bigelow 2011 (cỡ chữ tới hạn).*
- **C2 Độ dài dòng 50–75 ký tự** (tiếng Việt ~55–70). Cột đọc desktop ≈ 560–640px với chữ 17px. Dài hơn mắt khó tìm đầu dòng kế; ngắn hơn ngắt mạch. *Dyson & Haselgrove 2001; Bringhurst.*
- **C3 Tối đa 4 cỡ chữ + 2 độ đậm trong vùng nội dung** (tiêu đề bài, tiêu đề mục, thân, chú thích). Thang cỡ nhất quán toàn site (tokens), không đặt px lẻ trong component.
- **C4 Đoạn ≤ 4–5 dòng trên điện thoại**; khái niệm → 1 câu định nghĩa + 1 câu "nghĩa là". Danh sách khi ≥ 3 ý song song.
- **C5 Công thức dùng một cơ chế dựng duy nhất** (KaTeX) kể cả inline; không trộn chữ nghiêng thường với KaTeX trong cùng đoạn (mắt coi là 2 thứ khác nhau → mất tín hiệu "đây là công thức").
- **C6 Căn trái, không justify** (justify tạo "sông" trắng, khó với người đọc yếu). Không viết hoa toàn bộ câu dài (giảm tốc độ đọc ~10–15%).
- **C7 Chữ không phải ảnh**: không dùng ảnh chụp đoạn chữ/công thức khi có thể gõ lại — không zoom được, không tìm được, mờ trên màn hình nhỏ.

## 3. Màu, nền, tương phản (M)

- **M1 Đọc dài mặc định trên nền sáng** (chữ tối trên nền sáng — "positive polarity"): nhiều thí nghiệm cho thấy đọc nhanh hơn, soát lỗi tốt hơn ở mọi lứa tuổi; ưu thế càng rõ với chữ nhỏ. Nền tối giữ làm **tuỳ chọn** cho học buổi tối, nhớ lựa chọn của HS. *Piepenbrock, Mayr, Mund & Buchner 2013; Buchner & Baumgartner 2007; Dobres et al. 2017.* → Trang bài học/làm đề: mặc định sáng hoặc theo `prefers-color-scheme`, không ép tối theo trang chủ.
- **M2 Tương phản thân bài ≥ 4.5:1, chữ phụ ≥ 3:1** nhưng **không trắng tinh trên đen tinh** (chói, chữ "rung" với người loạn thị). Nền tối dùng xám rất đậm + chữ ~87% trắng (như đang làm `#E2E8F0` trên `#05070B` là đúng). *WCAG 2.1 1.4.3; Material dark theme guidance.*
- **M3 Một màu nhấn cho hành động, một màu cho trạng thái đúng/sai, còn lại trung tính.** Màu nhấn chỉ xuất hiện ở thứ bấm được hoặc đang chọn. Tránh ≥ 3 sắc độ bão hoà trên cùng màn hình (G2: màu bão hoà kéo chú ý tiền ý thức).
- **M4 Không truyền nghĩa chỉ bằng màu**: đúng/sai, đã học/chưa học phải kèm icon/chữ. ~8% nam sinh mù màu đỏ–lục. *Birch 2012; WCAG 1.4.1.*
- **M5 Ảnh nền trắng trên nền tối phải được xử lý**: hoặc bọc ảnh trong khung sáng có đệm 12–16px (khung sáng cố ý, đều nhau), hoặc dùng SVG nền trong suốt nét theo theme. Ô trắng chói giữa nền đen tạo loá cục bộ và làm đồng tử co giãn liên tục khi cuộn → mỏi mắt. (Lý do thị giác: thích nghi độ sáng cục bộ, loá tương phản; áp dụng cả cho ảnh scan đề.)
- **M6 Quầng sáng/gradient/blur trang trí chỉ ở trang giới thiệu**, không ở vùng đọc/làm bài (N1, G3).
- **M7 Nền sáng là mặc định toàn site** (từ 11/10/2026): chế độ tối chỉ bật khi học sinh tự chọn, không theo `prefers-color-scheme`. Bảng màu, số đo tương phản và bảng quy đổi idiom `bg-white/5`/`bg-[#0B1020]` → token nằm ở [`docs/MAU-NEN-SANG.md`](MAU-NEN-SANG.md); kiểm bằng `npm run check:a11y` và xem bằng `/dev/giao-dien`. Một màu nhấn duy nhất + ba màu trạng thái (M3), không thêm sắc độ bão hoà thứ ba cho trang trí.

## 4. Bố cục & chú ý (B)

- **B1 Nội dung học bắt đầu trong 40% màn hình đầu** (≤ ~320px từ mép trên ở 375×812; desktop ≤ 260px). Trên đó tối đa **2 hàng điều hướng** (navbar + 1 hàng tab/breadcrumb). Mọi "thẻ giới thiệu tính năng", banner, toolbar lớn đều vi phạm.
- **B2 Mỗi màn hình đúng một điểm nổi bật** (nút chính / câu hỏi đang trả lời / kết luận). Thứ hai muốn nổi phải hạ cấp (viền thay nền, chữ thay nút). *Von Restorff; Nielsen – visual hierarchy.*
- **B3 Nhóm bằng khoảng cách và nền chung, hạn chế viền.** Khoảng cách trong nhóm < giữa nhóm (tỉ lệ ≥ 1:2). Viền hộp lồng hộp ≥ 3 cấp là dấu hiệu rối. *Gestalt – proximity (Wertheimer 1923), common region (Palmer 1992).*
- **B4 Không có gì chuyển động khi người học đang đọc/làm bài**: không hoạt hình lặp, không badge nhấp nháy, không toast tự hiện giữa bài (G2; Franconeri & Simons 2003: khởi phát chuyển động bắt chú ý không tự chủ). Hoạt hình chỉ dùng để *giải thích* (mô phỏng) và do HS bấm chạy.
- **B5 Vị trí cố định, nhất quán giữa các trang**: nút "Tiếp", "Nộp", "Bài sau" luôn cùng chỗ; mục lục luôn cùng cạnh. Nhận ra dễ hơn nhớ lại. *Nielsen heuristic #6 (recognition over recall).*
- **B6 Thanh cố định (sticky/fixed) tổng cộng ≤ 15% chiều cao màn hình điện thoại**, không bao giờ 2 thanh dưới đáy; đích cuộn có `scroll-margin-top` bằng chiều cao thanh trên (xem memory `feedback_mobile_first_ui`).
- **B7 Mục lục trong bài ≤ 7 mục nhìn thấy**; dài hơn thì thu theo cấp.
- **B8 Thứ tự đọc = thứ tự DOM = thứ tự học**: mục tiêu bài → nội dung → tự kiểm tra → bài tập; không chèn khối "khác" vào giữa.

## 5. Hình, công thức, bảng (H)

- **H1 Mỗi hình trả lời một câu hỏi**; hình trang trí (clipart, ảnh minh hoạ chung chung) bỏ. *Mayer – coherence; Harp & Mayer 1998.*
- **H2 Bảng 2 cột "chữ | hình" từ Word phải xếp dọc trên điện thoại** (hình dưới chữ, rộng 100%), không cuộn ngang. Cuộn ngang trong vùng đọc chỉ cho bảng số liệu thật sự.
- **H3 Nhãn đặt ngay trên hình** (SVG có chữ) thay vì chú giải tách rời. *Spatial contiguity.*
- **H4 Hình vẽ cho bài học là SVG nét 2px, 2–3 màu, nền trong suốt**, chữ trong SVG ≥ 13px khi hiển thị ở 360px.
- **H5 Công thức khối đứng riêng dòng, căn giữa, có khoảng thở ≥ 12px**; ký hiệu được giải thích ngay dưới trong ≤ 1 dòng mỗi ký hiệu.

## 5b. Video thí nghiệm trong bài lý thuyết (V)

- **V1 Mỗi hộp thí nghiệm (`.tl-box--exp`) tối đa MỘT clip, đặt ngay sau hộp đó.** Clip không thay phần chữ Làm–Quan sát–Rút ra, chỉ để xác nhận hiện tượng thật. Media thêm cạnh chữ đã đủ ý làm giảm học, không tăng. *Mayer – multimedia & coherence (Harp & Mayer 1998).*
- **V2 Bắt buộc có dòng "Nhìn vào:" một câu ≤ 25 từ** nêu đúng hiện tượng cần quan sát. Video phòng thí nghiệm thật thường nhiễu (tay, bàn, chữ kênh); không hướng chú ý thì học sinh xem mà không rút ra gì. *Mayer – signaling; de Koning et al. 2009.*
- **V3 Cắt còn ≤ 90 giây** đúng đoạn có hiện tượng (`giay_bat_dau`/`giay_ket_thuc`) — bỏ intro, quảng cáo, đoạn nói lan man.
- **V4 Ưu tiên clip tiếng Việt hoặc không lời.** Clip tiếng Anh chỉ dùng khi phần chữ trong bài đã đủ để hiểu, không bắt học sinh nghe hiểu tiếng Anh.
- **V5 Không nạp player trước khi bấm**: khối video hiện **ảnh bìa + nút phát**, player chỉ nhúng khi học sinh bấm (`ContentHtml.tsx`). Mỗi iframe YouTube kéo theo ~1 MB JS; bài có 4 video là ~4 MB cho thứ phần lớn em không xem (B4, mục "Đăng nội dung — tối ưu tốc độ" của `AGENTS.md`).
- **V6 Không thêm video cho chỗ bài đã có mô phỏng/SVG thể hiện rõ hiện tượng** (trùng nội dung — N1, H1), và không dùng video thay thí nghiệm học sinh làm được ngay tại lớp.
- **V7 Clip MỞ BÀI khi tình huống mở bài có thật ngoài đời** (xe phanh gấp, cầu thủ sút, dây đàn, hai loa…): đặt **ngay trước hộp "Dự đoán trước khi học"** để học sinh thấy hiện tượng rồi mới dự đoán. Clip **chỉ quay hiện tượng, không giải thích cơ chế, không lộ đáp án** (nếu lộ thì mất luôn câu dự đoán); `nhin_vao` hỏi đúng câu hỏi mở bài; nên ≤ 60 giây. Tình huống mở bài là giả định trong đầu (không có cảnh thật) thì bỏ qua, không bịa clip.

## 6. Điện thoại & thao tác (D)

- **D1 Thiết kế ở 375px trước, desktop sau.** Chụp 375×812 (và 360) trước khi báo xong.
- **D2 Đích chạm ≥ 44×44pt, cách nhau ≥ 8px**; nhãn nút ≤ 2 từ hoặc ≤ 1 dòng (nút 3 dòng = lỗi). *Apple HIG; Material 48dp; WCAG 2.5.8.*
- **D3 Hành động chính nằm vùng ngón cái** (nửa dưới màn hình, không góc trên); hành động phá huỷ (thoát, nộp sớm) xa vùng này. *Hoober 2013 (49% cầm một tay).*
- **D4 Thanh tab ngang phải lộ hết tab ở 360px** (≤ 4 tab, chữ ngắn) hoặc có dấu hiệu còn tab ẩn; tab "Kiểm tra" bị trôi khỏi màn hình là mất tính năng với HS.
- **D5 Không hover để tiết lộ thông tin** (điện thoại không có hover); tooltip chỉ là bổ sung.
- **D6 Nhập liệu**: bàn phím phù hợp (`inputmode="decimal"` cho đáp số), không mất trạng thái khi xoay máy/quay lại tab.

## 7. Động lực, phản hồi, tiến độ (L)

- **L1 Kiểm tra nhanh ngay sau mỗi khối lý thuyết** (truy xuất > đọc lại); phản hồi **tức thì và giải thích vì sao sai**, không chỉ đúng/sai. *Roediger & Karpicke 2006 (testing effect); Butler, Karpicke & Roediger 2007; Hattie & Timperley 2007.*
- **L2 Tiến độ hiển thị theo bài đang học, không theo cả lớp** ở trang bài (0/27 bài ở góc trang bài là thông tin của trang lớp). Thanh tiến độ bài nhỏ, có điểm xuất phát > 0 khi đã làm 1 phần. *Kivetz, Urminsky & Zheng 2006 (goal-gradient); Nunes & Drèze 2006 (endowed progress).*
- **L3 Phần thưởng ngoài (huy hiệu, rank, điểm) không hiện trong lúc học**; chỉ hiện ở màn hình kết thúc/tổng kết. Lạm dụng phần thưởng ngoài làm giảm động lực nội tại và bảng xếp hạng làm nản HS yếu. *Deci, Koestner & Ryan 1999 (meta-analysis); Hanus & Fox 2015.*
- **L4 Ngôn ngữ phản hồi hướng vào nỗ lực và việc tiếp theo** ("Xem lại mục 2 rồi thử câu tương tự" > "Sai rồi"), không vai "thầy" (xem `feedback_giong-van-bai-ly-thuyet`).
- **L5 "Tiếp tục học" trỏ đúng chỗ dở** (hiệu ứng việc dở – Zeigarnik), là nút duy nhất nổi ở trang lớp/trang chủ HS.
- **L6 Thông báo gom theo phiên**, không đẩy giữa lúc làm bài; sau khi nộp mới hiện (G2).

---

## 8. Checklist trước khi báo "xong" một thay đổi UI học sinh

1. Chụp 375×812 (light + dark nếu có) và 1440: nội dung học bắt đầu trong 40% màn đầu? (B1)
2. Đếm: ≤ 4 thao tác nhìn thấy mỗi vùng (N2); ≤ 4 cỡ chữ vùng nội dung (C3); ≤ 1 điểm nổi bật mỗi màn (B2).
3. Không thẻ trạng thái rỗng (N3), không lặp tiêu đề (N4), không thẻ giới thiệu tính năng chen giữa bài (N1).
4. Thân bài ≥ 16px, line-height ≥ 1.55, dòng 50–75 ký tự (C1, C2); công thức toàn KaTeX (C5).
5. Ảnh trắng trên nền tối đã có khung/đệm thống nhất hoặc SVG trong suốt (M5); bảng chữ|hình xếp dọc trên mobile (H2).
6. Đích chạm ≥ 44pt, nhãn nút ≤ 1 dòng (D2); tab lộ hết ở 360px (D4); thanh cố định ≤ 15% (B6).
7. Không có gì tự chuyển động/tự bật trong lúc đọc hoặc làm bài (B4, L6).
8. Nêu mã quy tắc đã áp dụng trong mô tả commit; nếu phá quy tắc, ghi lý do.
9. Video: mở bài 1 clip hiện tượng trước hộp Dự đoán (V7), mỗi hộp thí nghiệm 1 clip, đều có dòng "Nhìn vào", ≤ 90 giây, không nạp player trước khi bấm (V1–V7).

## 9. Nguồn chính (để tra khi cần, không cần đọc lại trước mỗi việc)

Sweller 1988; Sweller & Cooper 1985; Chandler & Sweller 1992; Kalyuga 2003 · Mayer, *Multimedia Learning* (2009/2020): coherence, signaling, redundancy, spatial/temporal contiguity, segmenting, pre-training; Harp & Mayer 1998; Mayer & Chandler 2001 · Cowan 2001 · Steinberg 2008; Casey, Jones & Hare 2008; Stothart, Mitchum & Yehnert 2015; Ophir, Nass & Wagner 2009 · Nielsen 2006 (F-pattern), 2008 (how little users read), 10 heuristics 1994 · Treisman & Gelade 1980; Franconeri & Simons 2003; Von Restorff 1933; Wertheimer 1923; Palmer 1992 · Hick 1952; Fitts 1954; Iyengar & Lepper 2000 · Dyson & Haselgrove 2001; Legge & Bigelow 2011; Bringhurst *Elements of Typographic Style* · Piepenbrock, Mayr, Mund & Buchner 2013; Buchner & Baumgartner 2007; Dobres et al. 2017; WCAG 2.1 (1.4.1, 1.4.3, 1.4.12, 2.5.8); Material Design dark theme; Birch 2012 · Apple HIG; Hoober 2013 · Roediger & Karpicke 2006; Butler, Karpicke & Roediger 2007; Cepeda et al. 2006; Hattie & Timperley 2007; Kivetz, Urminsky & Zheng 2006; Nunes & Drèze 2006; Deci, Koestner & Ryan 1999; Hanus & Fox 2015; Zeigarnik 1927.

---

## Phụ lục A — Rà trang bài học `/lop-hoc/bai` ngày 2/10/2026 (bản production, bài 3 lớp 12, chưa đăng nhập)

Đo được: 27 nút + 46 liên kết trên trang; vùng nội dung có **15 cỡ chữ khác nhau**; nội dung học bắt đầu ở
**471px/812px (58%)** trên điện thoại; cột đọc desktop 626px ≈ 84 ký tự/dòng; thân bài 16px/26px; nền `#05070B`.

> **Cập nhật 11/10/2026:** nền mặc định nay là **nền sáng `#f5f7fa`** (M7, xem `docs/MAU-NEN-SANG.md`);
> các số đo về bố cục/cỡ chữ trong phụ lục này vẫn còn nguyên giá trị, riêng kết luận "nền tối" thì thay bằng
> "theme tối tuỳ chọn".

| Ưu tiên | Vấn đề | Vi phạm | Hướng sửa |
|---|---|---|---|
| 1 | Trên điện thoại, 58% màn hình đầu là khung (navbar, hàng back/Aa/menu, breadcrumb, h1, badge "Bài học · 4 mục · 4 phần", tab, thẻ "Trình chiếu bài giảng") | B1, N4 | Gộp breadcrumb + h1 (bỏ breadcrumb lặp tên bài); bỏ badge/đếm mục; chuyển thẻ Trình chiếu thành icon nhỏ cạnh "Aa" và **chỉ hiện cho tài khoản GV** (hiện mọi người đều thấy, `page.tsx` ~dòng 1705) |
| 1 | Thẻ "Trình chiếu bài giảng" là công cụ của giáo viên nhưng chen giữa tab và bài, nổi bằng màu nhấn | N1, B2 | Như trên |
| 1 | Bảng "chữ | hình" từ Word cuộn ngang trên điện thoại, cột hình bị cắt | H2, N8 | CSS: `.table-scroll table` 2 cột không số liệu → `display:block` xếp dọc dưới 640px (hoặc chuyển khi đăng bài) |
| 1 | Ảnh nền trắng (Ideal/Real gas, pit-tông, hình ΔU) chói trên nền đen, kích thước và kiểu khung không đồng nhất | M5 | Bọc ảnh raster trong khung sáng đệm 12px thống nhất; hình mới vẽ SVG nền trong suốt |
| 2 | Cột phải desktop: "Câu sai liên quan" (rỗng) và "Ghi chú của em" (rỗng) là 2 thẻ trạng thái rỗng | N3, N1 | Ẩn khi rỗng; ghi chú thành nút nhỏ mở ra; câu sai chỉ hiện khi có |
| 2 | Cột trái lặp toàn bộ mục lục chương của lớp + vòng tiến độ 0/27 + "Tiếp tục học" + ô tìm kiếm | N4, L2 | Trong bài chỉ cần: bài trước / bài sau + link về chương; tiến độ của *bài này* |
| 2 | Thanh đáy điện thoại: nút "Đánh dấu đã học xong bài này" 3 dòng chữ, 3 nút sát nhau | D2, N2 | Nhãn "Đã học xong" 1 dòng; hoặc đưa vào cuối bài thay vì thanh cố định |
| 2 | Tab "Kiểm tra" trôi khỏi màn hình 375px, không có dấu hiệu còn tab | D4 | Rút chữ tab, bỏ badge đếm, hoặc 4 tab chia đều chiều rộng |
| 2 | Breadcrumb đè lên toolbar "Dịu mắt / A− / A+" ở 1440px (y≈100–135) | B3 | Tách hàng hoặc đưa toolbar vào hàng tab |
| 2 | Mặc định nền tối cho trang đọc dài | M1 | Trang bài/làm đề theo `prefers-color-scheme` hoặc mặc định sáng, nhớ lựa chọn "Dịu mắt" của HS |
| 3 | 15 cỡ chữ trong vùng nội dung; công thức `Q = mc(T₂ − T₁)` là chữ nghiêng thường xen KaTeX | C3, C5 | Token cỡ chữ 4 mức; dựng lại công thức thường thành `$…$` khi đăng |
| 3 | Cột đọc 626px ≈ 84 ký tự/dòng với chữ 16px | C2 | 17px + cột 600px, hoặc giữ cột và tăng chữ lên 18px |
| 3 | Thẻ "Kiểm tra nhanh — Đăng nhập để làm" + nút "Mục tiếp theo" + nút nổi "Báo lỗi / Góp ý" cùng xuất hiện cuối bài | B2 | Một nút chính ("Làm kiểm tra nhanh"), phần còn lại dạng chữ liên kết |

**Tiến độ sửa (3/10/2026):** ưu tiên 1 xong (`8bad25b13`). Ưu tiên 2 xong: cột phải chỉ còn thẻ khi có dữ liệu (câu sai) + ghi chú là `<details>` thu gọn; cột trái trong bài chỉ còn bài trước/sau (cây chương đầy đủ ở ngăn kéo điện thoại); thanh đáy nhãn "Đã học xong" 1 dòng; 5 tab vừa 360/375px (bỏ badge, "Bài mẫu"); breadcrumb và công cụ đọc không chồng ở ≥1024px; theme đọc theo `prefers-color-scheme` khi chưa lưu lựa chọn (đã đúng từ trước — bản rà thấy tối vì trình duyệt đặt tối). Ưu tiên 3: cỡ chữ vùng nội dung còn 3 mức (token `--fs-cap/-sm/-body` ở `:root`, đo 12/14/16px); **còn treo:** công thức viết thường xen KaTeX (C5, sửa ở nội dung khi đăng), cột đọc 626px (C2), 3 nút cuối bài (B2).

Điểm tốt nên giữ: một màu nhấn duy nhất; tiêu đề mục đánh số rõ; ví dụ đóng khung nền nhạt ngay dưới khái niệm (N8);
thân bài 16px/1.6; mục lục bài sticky ≤ 7 mục (B7); tương phản chữ `#E2E8F0`/`#05070B` đúng M2.

---

## Phụ lục B — Rà 3 trang HS ngày 3/10/2026 (đọc code, chưa chụp màn hình vì cần đăng nhập HS thật)

Phạm vi: trang chủ HS (`/tai-khoan` → `components/dashboard/ThptStudentHome.tsx` + `WelcomePanel`), `/lop-hoc/ket-qua`
(`StudentResultsDashboard.tsx`), `/kiem-tra/lam` (`ExamRunner.tsx`). Cần chụp 375px bằng tài khoản HS để xác nhận số đo.

### B1. Trang chủ HS (`ThptStudentHome`)
| Ưu tiên | Vấn đề | Vi phạm | Hướng sửa |
|---|---|---|---|
| 1 | Trước "Việc cần làm hôm nay" có: WelcomePanel + thẻ hero (avatar, danh hiệu, thanh năng lượng, điểm TB) + Cần chú ý + RankCard + TitleShowcase + DailyStreakCard + ClassRankBoard + HonorVisibilityPicker. Việc học bắt đầu rất xa quá 40% màn đầu | B1, N1, L3, G2 | Đưa "Học tiếp" (nút duy nhất nổi) lên ngay dưới hero; gom rank/danh hiệu/streak/bảng lớp/chọn hiển thị thành 1 hàng thu gọn hoặc trang riêng `/lop-hoc/xep-hang` |
| 1 | Cùng lúc có ≥ 3 khối thưởng ngoài + 2 thanh tiến độ (năng lượng, streak) → cạnh tranh chú ý | L3, B2, N7 | Chỉ 1 điểm nổi bật (Học tiếp); phần thưởng hạ cấp thành chữ/viền |
| 1 | Hero: gradient + quầng blur + thanh gradient có glow | M6, M3 | Nền phẳng; thanh tiến độ 1 màu nhấn, bỏ shadow glow |
| 2 | Thẻ rỗng: "Chưa có việc gì mới…", "Chưa có bài tập về nhà mới", "Chưa có chủ đề nào đang chờ mở khoá…", "Chưa có buổi phụ đạo…" | N3 | Ẩn hẳn Section khi rỗng (cả Section "Bài tập về nhà", "Chủ đề đang mở khoá") |
| 2 | Chữ 12px ở nhãn ("Điểm TB", "Học tiếp theo", chú thích) và `text-xs` cho nội dung cần đọc (đoạn hướng dẫn mở khoá, mô tả BTVN) | C1 | Nội dung ≥ 14px; nhãn ≥ 13px |
| 2 | Đoạn dài giải thích "Để mở khoá một chủ đề…" (4–5 dòng ở 375px, xs) | C4 | Rút còn 1–2 câu hoặc thu vào "Cách mở khoá" |
| 2 | Nút "Đăng ký" py-2 text-xs ≈ 32px; chip "Tự kiểm tra" py-1 ≈ 26px; nút đăng xuất 40px | D2 | Đích chạm ≥ 44px, cách nhau ≥ 8px |
| 3 | `WelcomePanel` lặp lời chào với h1 "Chào {tên} 👋" của hero (2 lời chào) | N4 | Với HS đã có lớp, bỏ WelcomePanel hoặc bỏ h1 |
| 3 | Lời chào có tên + emoji, thanh "Năng lượng học tập" đếm theo cả lớp (%) | L2 | Giữ 1 con số: bài đang dở; % cả lớp để ở trang lớp |

**Đã sửa 7/10/2026 (thầy chốt sau khi kiểm lại góp ý):** trang chủ còn 5 khối theo thứ tự hero (kèm link "Chương trình lớp") →
`TodayCard` "Hôm nay em làm gì" (một nút nổi + ≤3 việc phụ, nguồn thứ tự duy nhất là `rankNextSteps`; thay `NextStepsCard`,
khối "Việc cần làm" và dòng gợi ý ở thẻ chuỗi ngày — N4, B2, L5) → BTVN → `WeakestSkillsCard` + `CatchupCard` (bỏ danh sách
buổi, chỉ bài cần bù) + `TutoringSection` (một khối, chỉ hiện khi có chủ đề/buổi/cửa sổ kiểm tra — N3; bỏ cách "luôn hiện lịch
trống" của 3a42d5a92) → `RankCard` + `DailyStreakCard`. `TitleShowcase`, `ClassRankBoard`, `HonorVisibilityPicker` chuyển sang
`/lop-hoc/xep-hang` (L3, N1). Các thẻ phụ hạ cấp: nền panel, nút viền (B2); nút Đăng ký ≥44px (D2). **Chưa chụp 375px bằng tài
khoản HS** — cần kiểm trước khi deploy.

### B2. `/lop-hoc/ket-qua` (`StudentResultsDashboard`)
| Ưu tiên | Vấn đề | Vi phạm | Hướng sửa |
|---|---|---|---|
| 1 | `RankCard` đầu trang trước điểm: phần thưởng ngoài chen vào trang kết quả | L3, B1 | Chuyển xuống cuối hoặc thành 1 dòng + link `/lop-hoc/xep-hang` |
| 1 | Biểu đồ điểm SVG `min-w-[420px]` → cuộn ngang ở 375px, chữ trục nhỏ | D1, H4 | viewBox co giãn 100% rộng, chữ trục ≥ 13px; hoặc thay bằng danh sách 5 điểm gần nhất + mũi tên xu hướng |
| 1 | Thẻ rỗng: "Em chưa làm bài kiểm tra nào", "Chưa có dữ liệu — hoặc em chưa sai câu nào", "Bài đã làm" rỗng | N3 | Ẩn Section khi rỗng; 1 dòng mờ duy nhất nếu hoàn toàn chưa có gì |
| 2 | 4 khối đứng cạnh nhau cùng cấp (Cần chú ý, Điểm theo thời gian, Bài đã làm, Mở khoá, Chủ đề cần ôn) → không rõ cái nào làm trước | B2, B8 | Thứ tự: Cần chú ý (nếu có) → Chủ đề cần ôn (hành động) → Bài đã làm → biểu đồ. 1 nút nổi: "Ôn chủ đề yếu nhất" |
| 2 | Ngôn ngữ phản hồi: "Điểm kiểm tra của em đang thấp…", "Em còn bài kiểm tra chưa làm — hãy hoàn thành sớm" | L4 | Hướng việc tiếp theo: "Làm lại mục … rồi thử câu tương tự" |
| 2 | Điểm chỉ phân biệt màu (đạt/chưa đạt `PASS = 6.5`) ở vài chỗ | M4 | Kèm chữ "Đạt/Chưa đạt" hoặc icon |
| 2 | Chữ `text-xs` (12px) cho phụ đề từng dòng, danh sách câu sai `text-sm` + `line-clamp-2` | C1 | Phụ đề ≥ 13px; câu sai ≥ 14px |
| 3 | Mỗi chủ đề là thẻ mở rộng chứa nút + danh sách câu: lồng viền 3 cấp (thẻ → khối → mục) | B3 | Bỏ viền mục con, dùng khoảng cách |

### B3. `/kiem-tra/lam` (`ExamRunner`)
| Ưu tiên | Vấn đề | Vi phạm | Hướng sửa |
|---|---|---|---|
| 1 | Thanh sticky đầu bài: hàng "Câu x/y · đã làm" + đồng hồ + 2 nút ("Bảng câu hỏi", "Nộp bài") → ở 375px xuống 2–3 dòng, mở bảng câu thêm ≤ 30vh; chiếm quá 15% màn | B6, D2 | 1 hàng: đồng hồ + "x/y" + nút ⋯ (Bảng câu/Nộp). Bảng câu mở dạng sheet từ đáy |
| 1 | "Nộp bài" (phá huỷ) nằm ngay cạnh "Bảng câu hỏi" ở góc trên, và lặp lại ở cuối; "Nộp bài" cùng cấp "Câu sau" | D3, B2 | Bỏ nút nộp ở thanh trên; chỉ ở câu cuối + trong bảng câu; "Câu sau" là nút nổi duy nhất |
| 1 | Ô số trong bảng câu `h-8 w-8` (32px) cách 6px | D2 | 44px, 5–6 ô/hàng ở 375px |
| 1 | Ô nhập đáp số không có `inputMode="decimal"` (bàn phím chữ hiện ra) | D6 | `inputMode="decimal"` + `autoComplete="off"` |
| 2 | Hàng dưới 3 nút (Câu trước, Đánh dấu, Câu sau) `flex-wrap` → xuống 2 dòng ở 360px; nhãn "Đánh dấu xem lại" 3 từ | D2, N2 | Nhãn "Đánh dấu"; cố định vị trí "Câu sau" bên phải (B5) |
| 2 | Banner vi phạm tự hiện giữa bài (8 giây) | B4, L6 | Giữ (do chống gian lận) nhưng dạng dải mảnh 1 dòng, không đẩy nội dung xuống (overlay) |
| 2 | Chuyển câu bằng trượt + mờ (framer-motion) | B4 | Chấp nhận nếu < 200ms và tôn trọng `prefers-reduced-motion`; kiểm tra |
| 2 | Màn intro: đồng hồ/ghi chú 12–14px màu `slate-500` (tương phản ≈ 3:1 trên nền tối) | M2, C1 | Chữ phụ `slate-400` trở lên, ≥ 13px |
| 2 | Nền: trang làm đề đọc dài nhưng theme theo mặc định chung (tối) | M1 | `ReadingZone` mặc định sáng/`prefers-color-scheme` (hiện chỉ `/phu-huynh` ép sáng) |
| 3 | Ảnh đề scan nền trắng trên nền tối | M5 | Khung sáng đệm 12px thống nhất |
| 3 | Trạng thái lỗi/đang tải của `ExamLoader` là chữ trơ không căn hợp mạch ("Thiếu mã đề", "Đang tải đề…") | N3, L4 | Thêm link "Về trang lớp" |

### Thứ tự đề xuất sửa (giá trị cao / công ít)
1. `/kiem-tra/lam`: `inputMode`, thanh sticky 1 hàng, đích chạm 44px, bỏ "Nộp bài" ở thanh trên.
2. Trang chủ HS: ẩn Section rỗng, đưa "Học tiếp" lên đầu, gom khối rank/streak/bảng lớp xuống dưới.
3. `/lop-hoc/ket-qua`: ẩn trạng thái rỗng, biểu đồ co giãn, hạ RankCard.
