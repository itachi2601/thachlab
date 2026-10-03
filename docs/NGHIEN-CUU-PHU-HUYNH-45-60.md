# Nghiên cứu UX: Phụ huynh Việt Nam 45–60 tuổi dùng điện thoại theo dõi việc học của con

**Mục đích:** brief nền tảng để lập trình viên dịch thành quy tắc thiết kế web cụ thể (cỡ chữ px, tỉ lệ tương phản, kích thước đích chạm, bố cục).
**Đối tượng:** phụ huynh 45–60 tuổi, có con học cấp 2–3 (THCS–THPT), dùng điện thoại là thiết bị chính.

Phần lớn bằng chứng quốc tế về tuổi được đo trên mẫu 60–80+ tuổi (đặc biệt là Nielsen Norman Group và W3C WAI-AGE). Vì vậy nhiều khuyến nghị dưới đây là **ngoại suy xuống 45–60** và được đánh dấu rõ.

---

## 0. Quy ước nhãn bằng chứng — đọc trước

| Nhãn | Nghĩa |
|---|---|
| `[ĐO]` | Dữ liệu đo được, có nghiên cứu/tiêu chuẩn đứng sau; số liệu lấy đúng như nguồn nói. |
| `[SUY LUẬN]` | Ngoại suy từ `[ĐO]` sang nhóm 45–60 hoặc sang bối cảnh Việt Nam; **chưa có nghiên cứu trực tiếp**. |
| `[CHƯA CÓ NGUỒN]` | Nhận định thuần kinh nghiệm, không tìm được nguồn. Dùng được nhưng phải kiểm chứng lại. |

Cảnh báo về độ tuổi: Nielsen Norman Group định nghĩa "older adults" là **65+**; nghiên cứu 2019 của họ có **123 người tham gia 65+** tại Mỹ, Canada, Úc, Đức, Nhật `[ĐO]` (`NNG2019`). Nhóm 45–60 nằm giữa "mainstream" (25–60) và "senior" (65+), nên **không áp nguyên bộ guideline senior**, nhưng cũng **không dùng mặc định cho người 25 tuổi**.

---

## 1. Chân dung người dùng

### 1.1 Nhân khẩu và quy mô

- Dân số Việt Nam đầu 2025: **101 triệu**; nhóm **45–54 tuổi = 12,7%** và **55–64 tuổi = 10,4%** → khoảng **23,1% dân số (~23,3 triệu người)** trong hoặc sát khung 45–60 `[ĐO]` (`DataReportal2025`).
- Việt Nam có **79,8 triệu người dùng internet (78,8%)** và **76,2 triệu tài khoản mạng xã hội (75,2%)** đầu 2025 `[ĐO]` (cùng nguồn). Tỉ lệ dùng internet ở nhóm 45–60 thấp hơn mức trung bình này `[SUY LUẬN]` — báo cáo không tách theo tuổi.
- **40,5% dân số ở đô thị**, 59,5% nông thôn `[ĐO]` (cùng nguồn) → phải chấp nhận mạng chậm và màn hình rẻ ở một phần đáng kể người dùng `[SUY LUẬN]`.

### 1.2 Họ dùng điện thoại thế nào

- **Zalo là kênh số 1, không phải email.** Theo Bộ Thông tin và Truyền thông, Zalo có **76,5 triệu người dùng thường xuyên hàng tháng (30/6/2024)**, vượt Facebook (72 triệu), TikTok (67 triệu), YouTube (63 triệu); VNG báo cáo **77,6 triệu MAU** quý 3/2024. Zalo chiếm **~70%** trong ~110 triệu tài khoản mạng xã hội nội địa; Decision Lab ghi nhận **tỉ lệ sử dụng 85%** (Facebook 59%, Messenger 52%) và Zalo dẫn đầu mức yêu thích **57%** quý thứ 16 liên tiếp `[ĐO]` (`Zalo2024`).
- **Hệ quả `[SUY LUẬN]`:** thông báo quan trọng phải đi qua Zalo (Zalo OA / ZNS / deep link) hoặc **cuộc gọi**. Nút "Gọi giáo viên" và "Nhắn Zalo" phải là hành động hạng nhất, không ẩn trong menu.

### 1.3 Bối cảnh sử dụng

- NN/g 2018–19 quan sát người lớn tuổi dùng web/app **trên desktop, tablet và điện thoại**, gồm cả phiên trợ giúp công nghệ tại trung tâm cho người 65+ `[ĐO]` (`NNG2019`).
- NN/g: đích chạm tối thiểu **1cm × 1cm** để chọn nhanh và chính xác; và liệt kê rõ nhóm người dùng hưởng lợi gồm **"người truy cập thiết bị bằng một tay"** `[ĐO]` (`NNG-touch`). Chính tác giả bài này mô tả việc dùng điện thoại một tay trong lúc bế con — trùng với bối cảnh phụ huynh `[SUY LUẬN]`.
- Bối cảnh cụ thể của phụ huynh VN — **buổi tối sau khi con ngủ, tranh thủ giữa giờ làm, một tay cầm máy, ánh sáng phòng không lý tưởng** — `[CHƯA CÓ NGUỒN — suy luận]`. Hệ quả vẫn chắc vì dữ liệu thị giác (mục 2) cho thấy nhóm này cần nhiều sáng hơn và nhạy chói hơn.
- **Mạng và thiết bị:** ~21,2% dân số vẫn offline đầu 2025 `[ĐO]` (`DataReportal2025`) → **không giả định app native hay kết nối ổn định** `[SUY LUẬN]`.

### 1.4 Động cơ

- **Đầu tư cho con:** chi cho học tập là đầu tư dài hạn, không phải tiêu dùng `[CHƯA CÓ NGUỒN]`.
- **Sợ mất tiền/thời gian vô ích:** biểu hiện của **loss aversion** — "thua thiệt đau hơn được lợi". Prospect theory của Kahneman & Tversky (1979) được **tái lập trên 19 quốc gia, 13 ngôn ngữ, 4.098 người trả lời, mức tái lập 90%** cho các tương phản lý thuyết cốt lõi `[ĐO]` (`Ruggeri2020`).
- **Muốn thấy bằng chứng tiến bộ:** NN/g ghi nhận người lớn tuổi **chủ động gỡ app "làm mất thời gian"** và **chặn quảng cáo** — họ không thụ động, họ cắt thứ không sinh giá trị `[ĐO]` (`NNG2019`).

### 1.5 Lo lắng

| Lo lắng | Bằng chứng |
|---|---|
| Con học kém mà không biết | `[CHƯA CÓ NGUỒN — suy luận]` |
| Thầy dạy có tâm không | `[CHƯA CÓ NGUỒN — suy luận]` |
| Học phí ẩn, phát sinh | `[CHƯA CÓ NGUỒN — suy luận]` |
| Bị "quê" trước công nghệ | `[ĐO]` một phần — xem 1.6 |

### 1.6 Nỗi sợ bị "quê" trước công nghệ (self-efficacy thấp, tech anxiety)

- Có tổng quan hệ thống về **technophobia và lo âu máy tính ở người lớn tuổi** cùng các yếu tố ảnh hưởng `[ĐO]` (`BMC-tech`). Đây là mẫu tuổi cao hơn 45–60; mức ở 45–60 nhẹ hơn `[SUY LUẬN]`.
- NN/g: **digital literacy của người lớn tuổi đang tăng** (thế hệ Baby Boomer đã dùng máy tính tại nơi làm việc) và họ **tự tin hơn** nhiều so với nghiên cứu 2001 `[ĐO]` (`NNG2019`).
- **Hệ quả `[SUY LUẬN]`:** giảm bề mặt phải học. Mỗi màn hình mới, mỗi thuật ngữ mới, mỗi icon lạ là một lần người dùng có nguy cơ kết luận "mình không làm được" — và bỏ. Ngôn ngữ phải là tiếng Việt đời thường của phụ huynh, không phải ngôn ngữ sản phẩm.

---

## 2. Thị giác

Đây là phần có bằng chứng mạnh nhất và quyết định phần lớn quy tắc CSS.

### 2.1 Lão thị (presbyopia)

- Lão thị bắt đầu **ngay sau tuổi 40**: thuỷ tinh thể cứng hơn, không đổi hình dạng dễ dàng, khiến đọc gần khó hơn; người bệnh **thường đưa tài liệu ra xa hơn để nhìn rõ** `[ĐO]` (`AAO`).
- W3C: **suy giảm thị lực thường bắt đầu từ giữa tuổi 40**; **86% người Úc trên 40 tuổi cần kính đọc** để chỉnh thị lực gần `[ĐO]` (`W3C-AGE`).
- Tiến triển tới 60: nghiên cứu trên **1.310 người 35–60 tuổi** cho thấy **74,1% có lão thị**, tuổi trung bình nhóm lão thị **49,5 ± 5,8**, và nhóm tác giả phải lập **bảng cộng kính (near addition) theo tuổi** vì nhu cầu tăng dần theo tuổi `[ĐO]` (`Smret2023`).
- **Quan trọng cho sản phẩm:** một nghiên cứu khác trên **953 người, tuổi trung bình 61,4 ± 7,2**, đã **sàng lọc là có đủ kỹ năng số học, khéo léo và nhận thức để dùng smartphone** vẫn cho **tỉ lệ lão thị 62,6% (KTC 95%: 59,5–65,7)**; nhóm tác giả kết luận lão thị không chỉnh kính **có thể cản trở khả năng dùng dịch vụ ngân hàng trực tuyến trên điện thoại** `[ĐO]` (`THRIFT2026`).

> **Kết luận `[SUY LUẬN]`:** với phụ huynh 45–60, một tỉ lệ lớn đã có lão thị — kể cả người "vẫn nhìn tốt". Cỡ chữ mặc định phải phục vụ người đang ở giai đoạn đầu–giữa của lão thị, không phải người 25 tuổi.

### 2.2 Giảm độ nhạy tương phản (contrast sensitivity)

- W3C: **người 80 tuổi thường có độ nhạy tương phản thấp hơn 80% so với người 20 tuổi**; một phần do **đồng tử co nhỏ hơn** → **cần nhiều ánh sáng hơn và tương phản cao hơn** `[ĐO]` (`W3C-AGE`). Con số đo ở tuổi 80; ở 45–60 mức giảm nhỏ hơn nhiều `[SUY LUẬN]`.
- Nghiên cứu dân số Nhật 40–79 tuổi: **giảm độ nhạy tương phản có ý nghĩa thống kê ở mọi tần số không gian khi tuổi tăng (p<.001)**, kể cả khi chỉ tính người có thị lực chỉnh kính ≥1.0. **9,4% mắt có thị lực tốt vẫn nhạy tương phản kém ở tần số cao; tỉ lệ này đạt 21,1% ở nhóm 70–79** `[ĐO]` (`Nomura2003`).
- Điểm mấu chốt: **thị lực 20/20 không đồng nghĩa nhạy tương phản tốt.** Không thể lấy "chữ này tôi đọc được" làm tiêu chuẩn.

### 2.3 Thuỷ tinh thể ngả vàng và tán xạ ánh sáng

- W3C: **ít ánh sáng tím được ghi nhận hơn**, nên **đỏ và vàng dễ thấy hơn lam và lục**, và **xanh đậm thường không phân biệt được với đen** `[ĐO]` (`W3C-AGE`).
- Piepenbrock et al. nêu rõ cơ chế: **tán xạ ánh sáng do cặn trong thuỷ tinh thể và dịch kính đã lão hoá** — chính hiện tượng này là lý do đáng lẽ có thể đảo ngược lợi thế của nền sáng, nhưng thực nghiệm cho thấy **không đảo ngược** `[ĐO]` (`Piepenbrock2013`).

### 2.4 Đồng tử nhỏ hơn → cần nhiều ánh sáng hơn (hệ số bao nhiêu lần?)

- **Weale (NIOSH/CDC, 1975):** đường kính đồng tử giảm theo tuổi, làm giảm lượng sáng truyền qua thuỷ tinh thể. **Mắt người 60 tuổi cần khoảng 3 lần lượng sáng so với mắt người 20 tuổi trong điều kiện ngưỡng (threshold conditions)** — tức khi ánh sáng sẵn có ít. Ông cũng ghi nhận **tương quan giữa giảm độ nhạy của mắt theo tuổi và sự hiện diện của chói**, và **xác suất mắc một khuyết tật mắt nào đó tới tuổi 70 là 92%** `[ĐO]` (`Weale1975`).
- **Hệ quả `[SUY LUẬN]`:** không được thiết kế dựa vào việc người dùng ngồi trong phòng đủ sáng. Tương phản phải đủ cao để đọc được khi ánh sáng phòng yếu, và không dùng nét chữ mảnh.

### 2.5 Chói / loá (glare, halation)

- **Nhạy chói tăng theo tuổi:** Weale ghi nhận tương quan giữa giảm độ nhạy của mắt theo tuổi và sự hiện diện của chói, và **môi trường sáng của người lớn tuổi có thể cải thiện bằng cách giảm số nguồn chói trong trường nhìn** `[ĐO]` (`Weale1975`).
- Piepenbrock et al.: tán xạ ánh sáng từ thuỷ tinh thể/dịch kính lão hoá là cơ chế đã được nêu cho hiện tượng loá ở nhóm này `[ĐO]` (`Piepenbrock2013`).
- W3C nêu **chữ sáng trên nền tối là điểm rủi ro** cho nhóm này `[SUY LUẬN]`; W3C chỉ nêu vấn đề tán xạ và tương phản chung `[ĐO một phần]` (`W3C-AGE`) — kết luận ở mục 2.9.
- **Hệ quả `[SUY LUẬN]`:** tránh nền gradient, tránh ảnh nền sau chữ, tránh glow/bóng đổ nặng, tránh viền phát sáng; không dùng chữ trắng tinh trên nền đen tuyệt đối.

### 2.6 Giảm phân biệt màu xanh–tím

- W3C: **ít ánh sáng tím được ghi nhận → xanh đậm và đen có thể không phân biệt được**; đỏ/vàng dễ thấy hơn lam/lục `[ĐO]` (`W3C-AGE`).
- **Hệ quả `[SUY LUẬN]`:** không bao giờ dùng màu làm kênh thông tin duy nhất. Mọi mã màu phải kèm **nhãn chữ hoặc icon**. Không dùng cặp "xanh dương nhạt vs tím" để phân biệt trạng thái.

### 2.7 Thu hẹp "useful field of view" và tìm mục tiêu ngoại vi

- So sánh người trẻ (tuổi TB 24) và người lớn tuổi (tuổi TB 64): **người lớn tuổi gặp nhiều khó khăn hơn khi định vị mục tiêu ở ngoại vi**, đặc biệt khi mục tiêu nằm giữa các distractor không đồng nhất. Độ lệch tâm thử nghiệm **từ 4° đến 14°**. Khác biệt về thời gian phản ứng theo tuổi **biến mất khi loại trừ ảnh hưởng của số lượng saccade** — tức khác biệt chủ yếu do **phải lia mắt nhiều hơn**, không phải do chú ý chọn lọc `[ĐO]` (`Scialfa1994`).
- **Hệ quả bố cục `[SUY LUẬN, bám sát dữ liệu trên]`:**
  - Thông tin quan trọng (điểm, cảnh báo, nút hành động) **ở giữa cột nội dung**, không ở rìa màn hình, không ở góc trên phải.
  - **Không bắt lia mắt** để nối hai mẩu thông tin liên quan (nhãn ở trái, giá trị ở phải của hàng rộng). Đặt nhãn và giá trị **cạnh nhau, cùng khối**.
  - **Tránh bố cục nhiều cột** và tránh bảng rộng phải cuộn ngang.

### 2.8 Bảng thông số thị giác — kết luận cho code

| Hạng mục | Tối thiểu (bắt buộc) | Khuyến nghị cho 45–60 | Căn cứ |
|---|---|---|---|
| Cỡ chữ thân bài / cỡ nhỏ nhất | 16px; không dùng 12–13px cho câu cần đọc | **17–18px** (chốt 18px) | WCAG coi ≥18,5px (14pt đậm) / ≥24px (18pt) là "large text" `[ĐO]` (`WCAG1.4.3`); NN/g khuyến nghị **≥12pt (~16px) cho người cao tuổi** `[ĐO]` (`NNG2002`); người 40+ cần chữ lớn hơn `[ĐO]` (`NNG2019`). Con số 17–18px là `[SUY LUẬN]` |
| Nhãn phụ / metadata | 14px | **15–16px** | `[SUY LUẬN]` |
| Tiêu đề màn hình | 24px | 24–28px, đậm | Ngưỡng "large text" WCAG = 24px (18pt) `[ĐO]` (`WCAG1.4.3`) |
| Tương phản chữ thân bài | **4,5:1** (AA) | **7:1** (AAA) | WCAG: 4,5:1 bù thị lực 20/40 (**20/40 là thị lực điển hình của người ~80 tuổi**); **7:1 bù 20/80** `[ĐO]` (`WCAG1.4.3`) |
| Tương phản UI, viền, trạng thái, focus | **3:1** | 4,5:1 | `[ĐO]` (`WCAG1.4.11`) |
| Line-height / khoảng cách đoạn | **≥1,5** / ≥2 lần cỡ chữ | **1,6–1,7** (chữ Việt có dấu) | `[ĐO]` (`WCAG1.4.12`); phần dấu tiếng Việt là `[SUY LUẬN]` |
| Letter-spacing / word-spacing chịu được | ≥0,12em / ≥0,16em | không siết chặt chữ | `[ĐO]` (`WCAG1.4.12`) |
| Độ dài dòng | **≤80 ký tự** (40 nếu CJK) | **55–70 ký tự**; mobile ~35–45 | `[ĐO]` (`WCAG1.4.8`); 55–70 là `[SUY LUẬN]` |
| Căn lề | **KHÔNG căn đều hai bên** | căn trái | `[ĐO]` (`WCAG1.4.8`; F88 là lỗi) |
| Zoom / resize | **200%** không mất nội dung, không cuộn ngang | kiểm ở 200% | `[ĐO]` (`WCAG1.4.8`) |
| Reflow | không cuộn ngang ở **320 CSS px** | kiểm ở 320px | `[ĐO]` (`WCAG1.4.10`) |
| Đích chạm | **24×24 CSS px** (AA) | **≥44×44** (AAA); CTA chính **≥48×48**, cách nhau ≥8px | `[ĐO]` (`WCAG2.5.8` — trang này nêu 24×24, khuyến nghị nhắm tới tiêu chí chặt hơn 2.5.5 với 44px, và minh hoạ nút 44px); NN/g: **tối thiểu 1cm × 1cm**, đầu ngón tay 1,6–2cm, ngón cái 2,5cm `[ĐO]` (`NNG-touch`) |
| Font chữ | — | nét đủ dày; **không dùng nét mảnh/italic cho đoạn dài** | font mảnh làm tương phản thực tế thấp hơn danh nghĩa `[ĐO]` (`WCAG1.4.3`); phần italic là `[SUY LUẬN]` |

### 2.9 Nền tối hay nền sáng cho người 45–60?

Bằng chứng **cả hai chiều**:

- **Ủng hộ nền tối (negative polarity — chữ sáng trên nền tối):** Piepenbrock et al. nêu giả thuyết rằng **tán xạ ánh sáng do cặn trong thuỷ tinh thể và dịch kính lão hoá có thể đảo ngược lợi thế của nền sáng** ở người lớn tuổi; nền tối cũng giảm tổng lượng sáng phát ra nên dễ chịu hơn trong phòng tối `[ĐO một phần]` (`Piepenbrock2013`).
- **Ủng hộ nền sáng (positive polarity):** chính nghiên cứu đó **đo thực nghiệm** bằng bài kiểm tra thị lực và bài soát lỗi trên **cả nhóm trẻ và nhóm lớn tuổi** — kết quả là **lợi thế thuộc về positive polarity (chữ đậm trên nền sáng) ở cả hai nhóm**. Kết luận của tác giả: **nên dùng positive polarity cho mọi lứa tuổi**; lý do là thay đổi theo tuổi làm **giảm độ rọi trên võng mạc (retinal illuminance)**, nên nền sáng hơn giúp bù lại `[ĐO]`.
- **Bổ trợ:** suy giảm nhạy tương phản do đồng tử co nhỏ dẫn tới **cần nhiều ánh sáng hơn và tương phản cao hơn** `[ĐO]` (`W3C-AGE`); mắt 60 tuổi cần ~3× ánh sáng `[ĐO]` (`Weale1975`).

> **KẾT LUẬN `[SUY LUẬN]` dựa trên dữ liệu `[ĐO]`:** **mặc định nền sáng, chữ đậm.** Nền tối là tuỳ chọn phụ, và nếu có thì phải: (a) không dùng trắng tinh trên đen tuyệt đối; (b) nâng tương phản lên **≥7:1**; (c) không giảm cỡ chữ; (d) tôn trọng `prefers-color-scheme` nhưng không tự đổi theme giữa phiên. Không dùng nền tối làm mặc định cho sản phẩm này.

---

## 3. Nhận thức

### 3.1 Tốc độ xử lý chậm hơn — có số đo

- **NN/g đo được: từ 25 đến 60 tuổi, thời gian hoàn thành tác vụ web tăng 0,8% mỗi năm** (ý nghĩa thống kê ở mức 5%, n=61). Người 40 tuổi chậm hơn người 30 tuổi 8%; người 50 tuổi chậm thêm 8% nữa. Cơ chế: **+0,5% thời gian mỗi trang** và **+0,3% số trang mỗi tác vụ** `[ĐO]` (`NNG2008`).
- Cùng nguồn: người 65+ **chậm hơn 74%**; và đường cong suy giảm có **hình gậy khúc côn cầu (hockey-stick)** — tăng tốc mạnh quanh 60 và đặc biệt sau 70 `[ĐO]` (`NNG2008`). Nghĩa là **45–60 là vùng dốc thoải**, khác hẳn 65+.
- **Cảnh báo cân bằng:** NN/g nhấn mạnh **khác biệt cá nhân lấn át khác biệt tuổi** — "5-5-5 rule": 5% người chậm nhất chậm gấp ~5 lần 5% nhanh nhất (cần thêm 400% thời gian). Một người 50 tuổi nhanh sẽ thắng một người 30 tuổi chậm `[ĐO]` (`NNG2008`).
- Cơ chế: Salthouse (1996) kết luận **một tỉ lệ lớn phương sai liên quan tuổi trong nhiều thước đo tốc độ là chia sẻ chung**, và **nhân tố tốc độ chung đóng vai trò quan trọng trong việc trung gian hoá khác biệt tuổi về trí nhớ** `[ĐO]` (`Salthouse1996`).

### 3.2 Trí nhớ làm việc giảm

- Park & Reuter-Lorenz (2009): có **suy giảm theo tuổi về tốc độ xử lý, trí nhớ làm việc, chức năng ức chế và trí nhớ dài hạn**, cùng giảm kích thước cấu trúc não và tính toàn vẹn chất trắng `[ĐO]` (`Park2009`).
- W3C: **hạn chế trí nhớ ngắn hạn có thể khiến người dùng quên mục đích truy cập site nếu họ mất định hướng**; kèm **khó tập trung và bị phân tán bởi chuyển động/nội dung không liên quan**; **~20% người trên 70 có suy giảm nhận thức nhẹ (MCI)** `[ĐO]` (`W3C-AGE`).
- **Hệ quả `[SUY LUẬN]`:** nếu tác vụ cần nhớ thông tin từ màn hình trước (mã lớp, mã học sinh, mã đơn), phải **hiển thị lại thông tin đó ngay tại chỗ dùng**. Không bắt nhớ rồi nhập lại.

### 3.3 Khó chia chú ý / ức chế nhiễu

- W3C nêu **mất tập trung vì chuyển động hoặc nội dung không liên quan** và **khó xử lý quá tải thông tin** `[ĐO]` (`W3C-AGE`).
- Park & Reuter-Lorenz xếp **chức năng ức chế (inhibitory function)** vào nhóm suy giảm theo tuổi `[ĐO]` (`Park2009`).
- **Hệ quả `[SUY LUẬN]`:** cắt mọi thứ không phục vụ quyết định của phụ huynh — không carousel tự chạy, không animation nền, không âm thanh tự phát, không banner động.

### 3.4 "Trí tuệ kết tinh" ổn định

- Park & Reuter-Lorenz: dù có suy giảm về tốc độ/trí nhớ làm việc/ức chế, hình ảnh chức năng cho thấy **tăng hoạt hoá vùng trước trán một cách đáng tin cậy** — dấu hiệu của **bộ não thích ứng, tham gia "giàn giáo" bù trừ (compensatory scaffolding)**; cơ chế này **bảo vệ chức năng nhận thức** và được tăng cường bởi **gắn kết nhận thức và vận động** `[ĐO]` (`Park2009`).
- Mô hình **chọn lọc – tối ưu hoá – bù trừ (SOC: Selection, Optimization, Compensation)** do **Baltes & Baltes (1990)** đề xuất, được nhắc trong tổng quan về lão hoá lành mạnh `[ĐO, trích dẫn gián tiếp]` (`Baltes1990`).
- **Hệ quả `[SUY LUẬN]`:** đừng "dạy lại" người dùng những khái niệm họ đã có. Phụ huynh 45–60 hiểu rất rõ: điểm số, học kỳ, xếp loại, học phí, cô giáo chủ nhiệm. **Dùng vốn từ và khái niệm họ đã có**, chỉ đổi cách trình bày.

### 3.5 Chi phí chuyển ngữ cảnh cao

- `[CHƯA CÓ NGUỒN trực tiếp cho 45–60]`. Bằng chứng gián tiếp: **thời gian mỗi trang tăng 0,5%/năm** đúng là dấu hiệu của việc cần nhiều thời gian hơn để hiểu trang `[ĐO]` (`NNG2008`).
- **Hệ quả `[SUY LUẬN]`:** không nhảy ngữ cảnh giữa các màn hình (bấm "xem chi tiết" mở trang mới rồi phải quay lại và tìm đúng vị trí cũ). Dùng **modal/drawer giữ nguyên ngữ cảnh** hoặc **giữ vị trí cuộn** khi quay lại.

### 3.6 Học giao diện mới chậm hơn

- NN/g heuristic #4 **Consistency and Standards**: **không giữ nhất quán sẽ làm tăng cognitive load bằng cách buộc người dùng học điều mới**; theo **Jakob's Law**, người dùng dành phần lớn thời gian trên sản phẩm **khác** của bạn, và kỳ vọng của họ được đặt bởi các sản phẩm đó `[ĐO]` (`NNG-heuristics`).
- NN/g heuristic #6 **Recognition rather than recall**: giảm tải trí nhớ bằng cách làm cho **đối tượng, hành động và lựa chọn hiển thị rõ ràng** `[ĐO]` (`NNG-heuristics`).

### 3.7 Hệ quả nhận thức — kết luận cho code

| Hạng mục | Quy tắc | Căn cứ |
|---|---|---|
| Số lựa chọn mỗi vùng | ≤ 5–7 mục chính; phần còn lại vào "Xem thêm" | `[SUY LUẬN]` |
| Số bước tới thông tin quan trọng | ≤ 2 lần chạm từ trang chủ | `[SUY LUẬN]` |
| Icon | **luôn kèm nhãn chữ**; không dùng icon trần cho hành động quan trọng | `[SUY LUẬN]`; heuristic #2 (dùng ngôn ngữ của người dùng) `[ĐO]` (`NNG-heuristics`) |
| Ngõ cụt | Cấm. Mọi màn hình có đường thoát (Quay lại / Huỷ / Trang chủ) | heuristic #3 "User Control and Freedom": hỗ trợ Undo/Redo, có nút Cancel rõ, nhãn thoát dễ thấy `[ĐO]` (`NNG-heuristics`) |
| Hoàn tác | Mọi hành động có Undo, hoặc xác nhận trước | heuristics #3 và #5 "Error Prevention" (**kiểm tra và đưa lựa chọn xác nhận trước khi người dùng cam kết**) `[ĐO]` (`NNG-heuristics`) |
| Hành động phá huỷ | Bắt buộc xác nhận, nút mặc định là "Huỷ" | `[SUY LUẬN]` trên cơ sở heuristic #5 `[ĐO]` |
| Trạng thái hệ thống | Phản hồi tức thì; không hành động nào có hậu quả mà không thông báo | heuristic #1 `[ĐO]` (`NNG-heuristics`) |
| Phiên đăng nhập | Không tự hết hạn ngắn; hoặc cảnh báo trước và cho gia hạn | `[SUY LUẬN]` từ hạn chế trí nhớ làm việc `[ĐO]` (`W3C-AGE`, `Park2009`) |
| Thông báo lỗi | Tiếng Việt, nói rõ cần làm gì; không mã lỗi trần | heuristic #9 `[ĐO]` (`NNG-heuristics`) |

---

## 4. Tâm lý & động cơ trong quan hệ với giáo viên

### 4.1 Niềm tin cá nhân > form/email

- Zalo chiếm ~70% thị trường mạng xã hội nội địa, 85% tỉ lệ sử dụng, 16 quý liên tiếp dẫn đầu mức yêu thích `[ĐO]` (`Zalo2024`). Đây là hạ tầng niềm tin, không chỉ là kênh phân phối.
- **`[SUY LUẬN]`:** phụ huynh tin một **cuộc gọi/tin nhắn từ người thật** hơn một **form gửi đi rồi không biết ai nhận**. Không tìm được nghiên cứu trực tiếp.
- **Hệ quả:** nếu có form liên hệ, phải hiện **cam kết thời gian phản hồi cụ thể** ("cô Hương trả lời trong 24h") `[SUY LUẬN]`.

### 4.2 Bằng chứng cụ thể (con số, ngày tháng, bài đã làm)

- **Loss aversion** (Kahneman & Tversky 1979; tái lập 19 quốc gia, mức tái lập 90%) nghĩa là **khung "mất" mạnh hơn khung "được"** trong ra quyết định `[ĐO]` (`Ruggeri2020`).
- **Hệ quả `[SUY LUẬN]`:** mọi màn hình kết quả phải trả lời được: **"Con tôi đã làm gì, ngày nào, kết quả bao nhiêu, so với chính con lúc trước thế nào."** Không hiển thị "Đang học" chung chung. Con số cụ thể (7/10, 12/15 câu đúng, 3 bài trong tuần này) làm giảm cảm giác "tiền đổ vào chỗ không biết".

### 4.3 Mong muốn đối chiếu với lớp / kỳ vọng

- `[CHƯA CÓ NGUỒN]` cho nhu cầu so sánh với lớp ở phụ huynh VN.
- **Cảnh báo thiết kế `[SUY LUẬN]`:** so sánh với lớp là dao hai lưỡi. Nếu hiển thị "con bạn xếp thứ 32/40", theo loss aversion `[ĐO]` (`Ruggeri2020`), phụ huynh sẽ phản ứng bằng áp lực lên con — hại quan hệ với giáo viên. Nên đối chiếu theo **chuẩn/ngưỡng** ("đạt yêu cầu môn Toán học kỳ này") hơn là **thứ hạng**.

### 4.4 E ngại bị phán xét về con mình

- `[CHƯA CÓ NGUỒN]` trực tiếp. Cơ sở gián tiếp: NN/g ghi nhận người lớn tuổi **chủ động gỡ app và xoá tài khoản** khi cảm thấy bị lấy quá nhiều dữ liệu hoặc bị làm phiền `[ĐO]` (`NNG2019`).
- **Quy tắc `[SUY LUẬN]`:**
  - Tuyệt đối **không dùng từ ngữ phán xét**: "yếu", "kém", "chậm tiến bộ", "đáng lo".
  - Dùng **mô tả trung tính + hướng hành động**: "Chưa nắm: 3 dạng toán về hàm số. Gợi ý: cho con làm lại 5 câu này."
  - Không hiển thị so sánh giữa **anh/chị/em trong cùng nhà**.
  - Phụ huynh là chủ thể của câu: "Quý phụ huynh xem được...", không phải "Con bạn đã thất bại ở...".

### 4.5 Loss aversion với tương lai của con

- `[ĐO]` (cơ chế): loss aversion tái lập mạnh trên 19 quốc gia `[ĐO]` (`Ruggeri2020`).
- `[SUY LUẬN]` (áp dụng cho VN): với phụ huynh, "mất" = con mất cơ hội, học phí không sinh kết quả, thời gian đã bỏ ra vô ích. **Khung truyền thông nên là "bảo vệ khoản đầu tư của anh/chị"** kèm bằng chứng tiến bộ, không phải "mua thêm khoá học".
- `[SUY LUẬN]` ngược lại: **không lạm dụng loss aversion để gây hoảng** ("con bạn đang tụt lại!"). Điều này phá niềm tin và làm tăng tech anxiety (`BMC-tech`).

### 4.6 Vai trò giới — mẹ có phải người theo dõi chính?

- **`[CHƯA CÓ NGUỒN — suy luận]`.** Tôi **không tìm được nghiên cứu đủ tin cậy, cập nhật, cho Việt Nam** về việc ai là người theo dõi việc học của con. Các tài liệu tìm thấy hoặc quá cũ (tạp chí xã hội học thập niên 1980) hoặc không xác minh được quốc gia/năm, nên **không dùng để chống đỡ khẳng định nào**.
- **Khuyến nghị thực dụng:** **thiết kế và ngôn ngữ trung tính về giới** ("Quý phụ huynh", "Anh/chị"); không mặc định avatar/nhân vật là mẹ, nhưng **không loại trừ** khả năng mẹ là người dùng chính. Cần tự khảo sát (5–8 phỏng vấn) trước khi quyết định cá nhân hoá.

### 4.7 Khác biệt văn hoá Việt Nam

- `[CHƯA CÓ NGUỒN — suy luận]` cho toàn bộ mục này. Các nét dự kiến: quan hệ thầy–trò và phụ huynh–giáo viên mang tính kính trọng, ngại "làm phiền thầy cô"; hỏi điểm con có thể bị coi là nghi ngờ thầy cô; nhiều phụ huynh không muốn con biết mình đang theo dõi.
- **Hệ quả thiết kế:** phải có cơ chế liên hệ **không đối đầu** ("Gửi câu hỏi cho cô giáo" thay vì "Khiếu nại điểm"), và cho phép phụ huynh xem mà **không** tự động thông báo cho học sinh rằng phụ huynh đã xem.

---

## 5. Bảng "NÊN / KHÔNG NÊN" (viết được thành code)

| # | NÊN | KHÔNG NÊN | Nguồn |
|---|---|---|---|
| 1 | Cỡ chữ thân bài **≥17px** (chốt 18px); nhãn phụ / metadata **≥15px** | Không dùng 12–13px cho câu cần đọc; không để nhãn phụ 11–12px | `WCAG1.4.3`, `NNG2002`, `NNG2019` |
| 2 | Tương phản chữ thân bài **≥7:1** (AAA); tuyệt đối không dưới **4,5:1** | Không xám nhạt trên trắng; không hạ dưới 4,5:1 kể cả chữ lớn | `WCAG1.4.3` (7:1 bù thị lực 20/80) |
| 3 | Tương phản viền / trạng thái / focus **≥3:1** và **vẽ viền cho mọi control** | Không dùng viền xám mờ; không flat không viền cho control | `WCAG1.4.11` |
| 4 | Line-height **≥1,5** (khuyến nghị 1,6–1,7); khoảng cách đoạn **≥2×** cỡ chữ | Không để line-height 1,1–1,2 | `WCAG1.4.12` |
| 5 | Dòng **≤80 ký tự** (mobile 35–45); căn **trái** | Không để dòng tràn hết màn hình; không căn đều hai bên (lỗi F88) | `WCAG1.4.8` |
| 6 | Đích chạm **≥44×44px**, CTA chính ≥48×48, cách ≥8px | Không dùng đích <24×24px; không xếp sát nhau | `WCAG2.5.8`, `NNG-touch` |
| 7 | **Zoom 200%** và reflow đúng ở **320 CSS px**, không mất nội dung, không cuộn ngang | Không khoá `user-scalable=no`; không tạo bảng/cột phải cuộn ngang | `WCAG1.4.8`, `WCAG1.4.10` |
| 8 | **Mặc định nền sáng, chữ đậm** (positive polarity) | Không để nền tối là mặc định | `Piepenbrock2013` (khuyến nghị cho mọi lứa tuổi) |
| 9 | Nếu có dark mode: tương phản **≥7:1**, không trắng-tinh/đen-tuyệt-đối, không tự đổi theme | Không tự chuyển theme giữa phiên | `[SUY LUẬN]` từ `Piepenbrock2013`, `W3C-AGE` |
| 10 | Font **nét đủ dày** cho nội dung dài | Không dùng font nét mảnh / italic cho đoạn dài | `WCAG1.4.3`; italic là `[SUY LUẬN]` |
| 11 | Thông tin quan trọng **ở giữa cột**; nhãn và giá trị **cùng một khối**; **một cột** trên mobile | Không để điểm/cảnh báo/nút chính ở rìa; không nhãn trái – giá trị phải hàng rộng; không 2–3 cột màn hẹp | `Scialfa1994` |
| 12 | Mọi icon **kèm nhãn chữ** | Không dùng icon trần cho hành động quan trọng | `NNG-heuristics` (#2, #4) |
| 13 | **Nhận ra thay vì nhớ lại**: hiện lại lựa chọn, lịch sử, gợi ý | Không bắt nhớ mã / nhập lại thông tin từ màn trước | `NNG-heuristics` (#6), `W3C-AGE`, `Park2009` |
| 14 | **Xác nhận trước hành động phá huỷ** (mặc định là Huỷ); **Undo mọi nơi**; có Cancel; không ngõ cụt | Không xoá/gửi một phát không hỏi; không để màn hình không có đường thoát | `NNG-heuristics` (#3, #5) |
| 15 | **Giữ nhất quán điều hướng và nhãn** giữa các màn hình | Không đổi tên gọi / vị trí menu giữa các lần phát hành | `NNG-heuristics` (#4) |
| 16 | **Zalo / gọi điện là hành động hạng nhất**; có cam kết thời gian phản hồi | Không dựa vào email làm kênh chính; không để form gửi đi vào hư vô | `Zalo2024` |
| 17 | Mọi kết quả kèm **con số + ngày tháng + bài đã làm** | Không hiển thị "đang học"/"ổn" chung chung | `Ruggeri2020` → `[SUY LUẬN]` cho VN |
| 18 | Ngôn ngữ **trung tính + gợi ý hành động** | Không dùng "yếu/kém/chậm tiến bộ"; không so sánh anh chị em | `[CHƯA CÓ NGUỒN — suy luận]` |
| 19 | **Đối chiếu theo ngưỡng/chuẩn** ("đạt yêu cầu môn Toán") | Không hiển thị thứ hạng cá nhân mặc định | `[SUY LUẬN]` từ `Ruggeri2020` |
| 20 | **Trung tính về giới** trong ngôn ngữ và hình ảnh | Không mặc định "mẹ" là người dùng duy nhất | `[CHƯA CÓ NGUỒN — suy luận]` (mục 4.6) |
| 21 | Cắt lộn xộn thị giác; **≤5–7 lựa chọn** mỗi vùng | Không carousel tự chạy, animation nền, âm thanh tự phát; không >10 mục cùng cấp | `W3C-AGE` (mất tập trung vì chuyển động) |
| 22 | Phản hồi **tức thì**, hiện trạng thái hệ thống | Không để bấm rồi không biết có ăn hay không | `NNG-heuristics` (#1) |
| 23 | Cho phụ huynh **điều chỉnh cỡ chữ** ngay trong app | Không phó mặc cho cài đặt trình duyệt | `NNG2002` |
| 24 | Nội dung **đọc được trong phòng thiếu sáng** (tương phản cao, nét dày) | Không thiết kế giả định phòng đủ sáng | `Weale1975` (mắt 60 tuổi cần ~3× sáng) |
| 25 | **Không dùng màu làm kênh thông tin duy nhất** | Không dùng xanh dương nhạt vs tím để phân biệt trạng thái | `W3C-AGE` (giảm ghi nhận ánh sáng tím) |

---

## 6. Danh mục nguồn (26 nguồn — vượt nhẹ mức 12–25 đề nghị, để giữ đủ phần Baltes và nghiên cứu lão thị – smartphone mà bạn yêu cầu)

**Thị giác / lão hoá**

1. W3C Web Accessibility Initiative — *Overview of "Web Accessibility for Older Users: A Literature Review"* (WAI-AGE, 2008; cập nhật 2018) — https://www.w3.org/WAI/older-users/literature/ — **`W3C-AGE`**
2. American Academy of Ophthalmology — *What Is Presbyopia?* (EyeSmart) — https://www.aao.org/eye-health/diseases/what-is-presbyopia — **`AAO`**
3. Nomura H, Ando F, Niino N, Shimokata H, Miyake Y — *Age-related change in contrast sensitivity among Japanese adults*, Jpn J Ophthalmol 47(3):299–303, 2003 — https://pubmed.ncbi.nlm.nih.gov/12782168/ — **`Nomura2003`**
4. Scialfa CT, Thomas DM, Joffe KM — *Age differences in the useful field of view: an eye movement analysis*, Optom Vis Sci 71(12):736–742, 1994 — https://pubmed.ncbi.nlm.nih.gov/7898880/ — **`Scialfa1994`**
5. Weale RA — *Lighting, performance and age variation*, NIOSH/CDC Stacks (DHEW Pub. 75-142), 1975 — https://stacks.cdc.gov/view/cdc/179858 — **`Weale1975`**
6. Piepenbrock C, Mayr S, Mund I, Buchner A — *Positive display polarity is advantageous for both younger and older adults*, Ergonomics 56(7):1116–1124, 2013 — https://pubmed.ncbi.nlm.nih.gov/23654206/ — **`Piepenbrock2013`**
7. Smret TM et al. — *Understanding Presbyopia in Asmara: Prevalence, Association with Refractive Error, and Age-Based Addition*, Clin Optom 15:213–224, 2023 — https://europepmc.org/articles/PMC10516207 — **`Smret2023`**
8. Aftab IB, Chakma T, Pant S et al. — *Prevalence of presbyopia among social safety net beneficiaries with the cognitive, numeracy and dexterity skills required for smartphone use: a cross-sectional analysis of THRIFT RCT screening data from Kurigram, Bangladesh*, BMJ Open 16(4):e108327, 2026 — https://europepmc.org/articles/PMC13064153 — **`THRIFT2026`**

**Tiêu chuẩn WCAG 2.2 (W3C WAI)**

9. *Understanding SC 1.4.3 Contrast (Minimum)* — https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html — **`WCAG1.4.3`** (cũng là nguồn cho tỉ lệ 7:1 của 1.4.6 và ngưỡng "large text" 18pt/14pt)
10. *Understanding SC 1.4.8 Visual Presentation* — https://www.w3.org/WAI/WCAG22/Understanding/visual-presentation.html — **`WCAG1.4.8`**
11. *Understanding SC 1.4.10 Reflow* — https://www.w3.org/WAI/WCAG22/Understanding/reflow.html — **`WCAG1.4.10`**
12. *Understanding SC 1.4.11 Non-text Contrast* — https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html — **`WCAG1.4.11`**
13. *Understanding SC 1.4.12 Text Spacing* — https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html — **`WCAG1.4.12`**
14. *Understanding SC 2.5.8 Target Size (Minimum)* — https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html — **`WCAG2.5.8`** (trang này cũng khuyến nghị nhắm tới 2.5.5 Target Size Enhanced, 44px)

**Nielsen Norman Group**

15. Kane L — *Usability for Older Adults: Challenges and Changes* (2019) — https://www.nngroup.com/articles/usability-for-senior-citizens/ — **`NNG2019`**
16. Nielsen J — *Middle-Aged Users' Declining Web Performance* (2008) — https://www.nngroup.com/articles/middle-aged-web-users/ — **`NNG2008`**
17. Nielsen J — *Let Users Control Font Size* (2002) — https://www.nngroup.com/articles/let-users-control-font-size/ — **`NNG2002`**
18. Harley A — *Touch Targets on Touchscreens* (2019) — https://www.nngroup.com/articles/touch-target-size/ — **`NNG-touch`**
19. Nielsen J — *10 Usability Heuristics for User Interface Design* (1994, rev. 2024) — https://www.nngroup.com/articles/ten-usability-heuristics/ — **`NNG-heuristics`**

**Nhận thức / lão hoá tâm lý**

20. Salthouse TA — *General and specific speed mediation of adult age differences in memory*, J Gerontol B 51(1):P30–42, 1996 — https://pubmed.ncbi.nlm.nih.gov/8548516/ — **`Salthouse1996`**
21. Park DC, Reuter-Lorenz P — *The adaptive brain: aging and neurocognitive scaffolding*, Annu Rev Psychol 60:173–196, 2009 — https://pubmed.ncbi.nlm.nih.gov/19035823/ (toàn văn: https://pmc.ncbi.nlm.nih.gov/articles/PMC3359129/) — **`Park2009`**
22. *60 years of healthy aging: On definitions, biomarkers, scores and challenges* (nhắc Baltes & Baltes 1990 — mô hình SOC), Ageing Research Reviews — https://www.sciencedirect.com/science/article/pii/S1568163723000934 — **`Baltes1990`** *(trích dẫn gián tiếp; chưa fetch được bài gốc Baltes & Baltes 1990)*

**Tâm lý quyết định / công nghệ**

23. Ruggeri K et al. — *Global study confirms influential theory behind loss aversion* (tái lập prospect theory Kahneman & Tversky 1979; Nature Human Behaviour 2020, DOI 10.1038/s41562-020-0886-x), qua EurekAlert — https://www.eurekalert.org/news-releases/463819 — **`Ruggeri2020`**
24. *Technophobia and computer anxiety in older adults: a systematic review of the influencing factors*, BMC Public Health — https://link.springer.com/article/10.1186/s12889-026-27337-w — **`BMC-tech`**

**Việt Nam**

25. Báo Nhân Dân — *Mạng xã hội Việt Nam đạt trăm triệu người dùng, Zalo chiếm gần 70%* (29/11/2024; dẫn báo cáo Bộ TT&TT và VNG) — https://nhandan.vn/mang-xa-hoi-viet-nam-dat-tram-trieu-nguoi-dung-zalo-chiem-gan-70-post847689.html — **`Zalo2024`**
26. DataReportal / We Are Social / Meltwater — *Digital 2025: Vietnam* — https://datareportal.com/reports/digital-2025-vietnam — **`DataReportal2025`**

---

## 7. Việc cần làm trước khi tin tuyệt đối tài liệu này

1. **Khảo sát trực tiếp 5–8 phụ huynh 45–60** tại Việt Nam (một tay, buổi tối, dùng Zalo) — mọi mục `[SUY LUẬN]` và `[CHƯA CÓ NGUỒN]` phải được kiểm chứng, đặc biệt mục 4.6 (vai trò giới) và 4.7 (văn hoá).
2. **Đo cỡ chữ và đích chạm thật trong DOM** (`getBoundingClientRect`) — đối chiếu bảng mục 2.8.
3. **Kiểm tương phản** toàn bộ cặp màu bằng công cụ tính contrast ratio; mục tiêu thân bài ≥7:1.
4. **Test với người dùng đeo kính lão** — đây là khác biệt lớn nhất so với test với người 25 tuổi.
