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

## 9. Nguồn chính (để tra khi cần, không cần đọc lại trước mỗi việc)

Sweller 1988; Sweller & Cooper 1985; Chandler & Sweller 1992; Kalyuga 2003 · Mayer, *Multimedia Learning* (2009/2020): coherence, signaling, redundancy, spatial/temporal contiguity, segmenting, pre-training; Harp & Mayer 1998; Mayer & Chandler 2001 · Cowan 2001 · Steinberg 2008; Casey, Jones & Hare 2008; Stothart, Mitchum & Yehnert 2015; Ophir, Nass & Wagner 2009 · Nielsen 2006 (F-pattern), 2008 (how little users read), 10 heuristics 1994 · Treisman & Gelade 1980; Franconeri & Simons 2003; Von Restorff 1933; Wertheimer 1923; Palmer 1992 · Hick 1952; Fitts 1954; Iyengar & Lepper 2000 · Dyson & Haselgrove 2001; Legge & Bigelow 2011; Bringhurst *Elements of Typographic Style* · Piepenbrock, Mayr, Mund & Buchner 2013; Buchner & Baumgartner 2007; Dobres et al. 2017; WCAG 2.1 (1.4.1, 1.4.3, 1.4.12, 2.5.8); Material Design dark theme; Birch 2012 · Apple HIG; Hoober 2013 · Roediger & Karpicke 2006; Butler, Karpicke & Roediger 2007; Cepeda et al. 2006; Hattie & Timperley 2007; Kivetz, Urminsky & Zheng 2006; Nunes & Drèze 2006; Deci, Koestner & Ryan 1999; Hanus & Fox 2015; Zeigarnik 1927.

---

## Phụ lục A — Rà trang bài học `/lop-hoc/bai` ngày 2/10/2026 (bản production, bài 3 lớp 12, chưa đăng nhập)

Đo được: 27 nút + 46 liên kết trên trang; vùng nội dung có **15 cỡ chữ khác nhau**; nội dung học bắt đầu ở
**471px/812px (58%)** trên điện thoại; cột đọc desktop 626px ≈ 84 ký tự/dòng; thân bài 16px/26px; nền `#05070B`.

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

Điểm tốt nên giữ: một màu nhấn duy nhất; tiêu đề mục đánh số rõ; ví dụ đóng khung nền nhạt ngay dưới khái niệm (N8);
thân bài 16px/1.6; mục lục bài sticky ≤ 7 mục (B7); tương phản chữ `#E2E8F0`/`#05070B` đúng M2.
