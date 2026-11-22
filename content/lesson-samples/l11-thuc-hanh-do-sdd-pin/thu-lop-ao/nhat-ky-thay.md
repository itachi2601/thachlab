# Nhật ký thầy — chạy thử bài 26 Thực hành đo ℰ, r của pin với học sinh ảo

Nguồn đối chiếu: `../tren-lop.src.html` (19 màn), `../tren-lop-ghi-chu.html`, `scripts/ruot-tap/l11-bai26.mjs` (p1–p5, tr.49–53). Số chỗ trống trong `sach-trong.md`: [__1__]…[__92__]. Học sinh biết tới hết bài 25. Chưa xem hình SVG của Tập, chưa xem khung hình clip (chỉ đọc ghi chú trong src); những chỗ liên quan ghi "chưa kiểm".

## Soát trước giờ (đọc ba tài liệu, chưa dạy)

**Khớp (đã đối chiếu, không lệch):** mã ô tuyệt đối trên mọi màn khớp Tập (tr.49 = trang 1, tr.50 = 2, tr.51 = 3, tr.52 = 4, tr.53 = 5). 19 màn đúng như ghi chú. Phân bổ 0–2 · 2–7 · 7–13 · 13–22 · 22–27 · 27–30 · đề 30–45 khớp bảng ghi chú. Số liệu các màn tự nhất quán: $r=0{,}80$ (2b), $5{,}0$ A và $0{,}65$ A (3b), $0{,}80\ \Omega$ từ lần 1 và 6 (0,42/0,52), $1{,}10$ V (5a), $0{,}80\ \Omega$ (5b), 5% và 50% (6a).

### Chỗ màn / ghi chú / Tập lệch nhau

1. **Pin mới có hai bộ số khác nhau.** Màn 3b và ô 50·2 (Tập) cho "pin mới $\mathcal E=1{,}50$ V, $r=0{,}30\ \Omega$ (cho sẵn)", còn màn 4e và clip pin mới ra $\mathcal E=1{,}58$ V, $r\approx0{,}26\ \Omega$. Học sinh để ý thì tưởng một trong hai sai (cùng "pin mới"). Nên ghi "pin mới ví dụ" ở 3b/50·2, hoặc cho 3b dùng số khác nhãn.
2. **Ô 53·2 có cột Điểm A, Điểm B và dòng sai số $\Delta r$; không màn nào nhắc.** Màn 4b dừng ③ chỉ nói "tính $r$ (ô 53·2)", màn 4c nói "lần 1 và lần 6" nhưng không bảo ghi tọa độ vào cột A, B; dòng sai số của $r$ (công thức $\Delta r/r$, [__88__] [__89__] [__90__]) không có màn nào dạy và **màn "Về nhà" không liệt kê nó**.
3. **Sáu cặp $(I,U)$ pin mới chỉ có trong clip**, không có màn tĩnh nào liệt kê (màn 4c chỉ có pin cũ). Clip trôi nhanh: học sinh chép 12 số (ô 52·1 bên phải) và cần số đó để điền A, B của pin mới ở 53·2. Chưa kiểm clip có dừng đủ lâu cho chép không. Số liệu pin mới ở ô 53·2 [__84__]–[__87__] chỉ có "1,58" và "≈ 0,26" lộ ở đáp án màn 4e, không có cặp A, B.
4. **Màn 6a gắn nhãn "ô 52·2, 52·3" nhưng nội dung chỉ là 52·3 và một câu hỏi bỏ ngỏ.** Câu "Vôn kế kẹp sát hai cực pin hay qua dây dài?" không có đáp án trong nút mở; bảng 5 hàng "nguyên nhân → khắc phục" của ô 52·2 ([__68__]–[__72__]) và hai dòng ☐ (ampe kế đặt trong/ngoài đoạn M–N; điện trở ampe kế có/không cộng vào $r$) không có màn, không có dòng trong ghi chú dạy. Màn "Về nhà" ghi "ô 52·2 sai số", nên học sinh về nhà tự điền không có hướng dẫn nào.
5. **Thứ tự lật Tập khác ghi chú.** Ghi chú: tr.49 → 50 → 51 → 52 → 53 → 49. Thực tế theo màn: 49 → 50 (3a–3c) → 51 (4a) → 52/53 (4b–4c, hai trang cùng lúc) → 52 (4d) → 53 (4e) → 51 (5a, 5b) → 52 (6a) → 53 (6b) → 49 (quay lại xe) → 50 (đề, ô 50·4). Học sinh lật khoảng 10 lần trong 15 phút cuối; ba lần lùi trang (53 → 51, 52 → 53 → 49).
6. **Đề cuối tiết: màn, Tập và ghi chú nói 20 câu, 15 phút (mã 1221, mục 216), nhưng `../exam.json` cục bộ chỉ có 6 câu, 8 phút** ("Kiểm tra nhanh — Đo suất điện động và điện trở trong của pin"). Ghi chú dạy đã tự nhận "chưa đối chiếu từng câu, cần tra DB". Chưa rõ đề 1221 trên web là 20 câu hay 6 câu; nếu 6 câu thì ô 50·4 "Điểm …/20" và màn QR sai số. Cần tra DB trước khi dạy.
7. **Màn 5a "Vôn kế hai đầu động cơ" ≠ ô 51·2 "Vôn kế đọc" (hai đầu pin).** Ô 51·2 và đáp án "hở mạch 1,50 V" chỉ đúng khi vôn kế đo hai cực pin; màn nói hai đầu động cơ, nếu mạch hở ở chỗ khác thì vôn kế chỉ 0. Học sinh giỏi sẽ thắc mắc.
8. **Công thức hai điểm trên màn 2a dùng chỉ số điểm (1), (2) và $I_2-I_1$; màn 4c dùng chỉ số lần đo ($U_1$, $U_6$).** Đúng nhưng đổi quy ước giữa hai màn; ô 49·4 [__10__] phụ thuộc hình điểm (1), (2) trong Tập (chưa kiểm hình nào có $I_2>I_1$).
9. **Khối "Đề BTVN" trên tr.51 đánh số mục 4 nhưng không có mã ô** (các mục khác đều có mã); màn "Về nhà" nhắc "khối Đề BTVN (tr.51)" không kèm mã.
10. **Phút chồng nhau:** màn 4a "phút 13–16" và màn 4c "phút 14–22"; hai màn clip ghi "khoảng 2 phút" không có phút. Màn 0 ghi "15 phút cuối làm đề". Chỉ ghi lại; không sai nghĩa.
11. **Điểm dừng 4 dày:** chép 12 số (pin cũ) + tính 5 hiệu $U$ + chọn điểm tính $r$ + điền A, B, ℰ, r, trong khoảng 9 phút; clip tự hiện đáp án B của dừng ① sau dừng ② chỉ 2 giây (giây 17,6 → 19,5), nên ít thời gian đối chiếu với câu đã đoán.

### Chữ in sẵn lộ đáp án

- **Màn 1 (ô 49·2):** phương án C là phương án duy nhất nêu cơ chế ("sụt áp bên trong, pin cũ sụt nhiều"); A, B, D ngắn và mơ hồ. Học sinh khá chọn C chỉ nhờ độ dài/độ cụ thể.
- **Màn 3c:** phương án B tự giải thích ("nối tắt hai cực: dòng rất lớn, pin nóng"), A và C chỉ nêu hiện tượng. Cùng mẫu với màn 1: phương án đúng dài nhất, có cơ chế.
- **Màn 2a, 4a:** chữ gạch chân hiện ngay (không có nút ẩn), lớp chỉ chép. Đúng ý "chiếu xong mới chép" nhưng ô 49·4 và ô 51·1 [__27__]–[__30__] không còn gì để tự nghĩ.
- **Màn 3a:** danh sách dụng cụ đã in "ampe kế (thang 2 A), vôn kế (thang 2 V)" trước khi tới màn 4a mới điền thang ([__27__] [__28__]).
- **Màn 6a:** câu hỏi đã in sẵn "hiệu $U$ là 0,42 V" và "0,04 V", nên [__73__] và [__75__] chỉ chép lại; chỉ còn [__74__] [__76__] là tính.
- **Màn 5a trùng số với 2b:** 2b cho $\mathcal E=1{,}50$ V và điểm $(0{,}50\ \text{A};\ 1{,}10\ \text{V})$, 5a cho $\mathcal E=1{,}50$ V, $r=0{,}8$, $I=0{,}50$ A và đáp án $1{,}10$ V. Học sinh thấy số quen, không còn là "bẫy".
- **Màn 6b hỏi lại điều màn 4e vừa mở** (pin nào $r$ lớn hơn, vì sao xe yếu): [__91__] chỉ còn chép lại.
- Phần đáp án của clip (dừng ①, ②) không lộ trước điểm dừng; tiêu đề dừng ② "Đường pin mới thoải hơn" chỉ hiện sau điểm dừng (đã ghi ở `dung-5.md` sau dòng ngăn).

### Phương án / câu dùng khái niệm chưa dạy (học sinh biết tới hết bài 25)

- **Màn 1 phương án C, D, B:** "sụt áp bên trong" (bài 24 có $U=\mathcal E-Ir$, nên chấp nhận được nhưng từ "sụt áp" chưa chắc đã gặp), "điện áp ảo" (từ bịa, học sinh không có chuẩn để loại), "hút bớt suất điện động".
- **Màn 3c / ô 50·3:** điện trở của ampe kế "rất nhỏ", vôn kế "rất lớn" (lớp 9/ bài về mạch điện có thể đã học; chưa kiểm bài 22–25 có nhắc không).
- **Màn 4b dừng ①, phương án A "tụt đều, mỗi nấc như nhau":** hiểu theo nấc $R_x$ hay theo $I$ không rõ; vì $U$ giảm tỉ lệ với $\Delta I$ mà $\Delta I$ giữa các nấc không đều, học sinh biết $U=\mathcal E-Ir$ có thể suy ra B hoặc đoán lung tung; đáp án B cần so từng hiệu $U$ nên không "đoán trước" được từ lý thuyết.
- **Màn 6a, ô 52·3, ô 53·2 (dòng $\Delta r$):** "sai số của hiệu hai số", "sai số tỉ đối", công thức $\Delta r/r=\Delta(U_A-U_B)/(U_A-U_B)+\Delta(I_B-I_A)/(I_B-I_A)$ (cộng sai số tỉ đối). Không có bài nào trước (22–25) dạy cách ước lượng sai số của hiệu hai số; chưa kiểm bài lớp 10/thực hành có dạy không.
- **Màn 4d dừng ①, ô 53·2:** "hệ số góc", "cắt trục $U$ gần chỗ cũ", "thoải/dốc" của đường thẳng; học sinh biết đồ thị đường thẳng (đã nhắc ở 2a) nhưng phải suy ra độ dốc = $-r$ từ màn 2a mới trả lời được.
- **Câu cuối clip pin mới, "trong pin, điều gì làm $r$ tăng?"** bỏ ngỏ; học sinh chưa có kiến thức (hoá học/cấu tạo pin).

### Ô trong Tập không điểm dừng nào nhắc (học sinh phải tự đoán hoặc bỏ trống)

- **49·1** ba ô ☐ mục tiêu (không màn, không dòng nào trong ghi chú).
- **50·1:** bốn hàng của bảng dụng cụ ([__12__] pin, [__13__] biến trở, [__14__] $R_0$, [__17__] khoá K); màn 3a chỉ hỏi ampe kế và vôn kế. "Để làm gì" của $R_x$, $R_0$, K không ai nói.
- **52·1 dòng Quan sát** ([__62__]–[__67__]): ghi chú dạy và màn không nhắc.
- **52·2** bảng nguyên nhân sai số và hai dòng ☐ về ampe kế: xem mục 4 trên.
- **53·1** đồ thị (ghi chú: "làm ở nhà vì không đủ giờ"; đã có trong "Về nhà") nhưng nhiều ô trên màn 4b/4c nói "đường thẳng" mà lớp chưa tự vẽ lần nào.
- **53·2 dòng $\Delta r$** ([__88__]–[__90__]): không điểm dừng và **không có trong "Về nhà"**.
- **53·3 câu 2** ([__92__]): "ghi ở nhà", có trong "Về nhà".
- **Khối Đề BTVN (tr.51):** có trong "Về nhà".

### Số câu đề cuối tiết

Màn 6q, Tập ô 50·4 và ghi chú: **20 câu, 15 phút, đề 1221** (mục 216). `exam.json` trong thư mục bài: **6 câu, 8 phút** (đề "Kiểm tra nhanh" của bài). Chưa tra DB; xem mục 6 trên. Nếu đề thật chỉ 6 câu thì 15 phút làm đề là thừa; nếu 20 câu thì `exam.json` cần thay.

## Lượt 2 (sau khi học sinh làm)

(Chưa làm. Chờ `hs-*.md`, `sach-hs.md`.)

## Lượt 2 (sau khi học sinh làm; đọc hs-1..6, sach-hs)

Không tin tỉ lệ đúng; tập trung chỗ phải đoán. Lưu ý: học sinh ảo không xem được clip (màn 4b, 4d) nên chưa kiểm được khung hình; ghi theo lời hs.

1. **Pin mới hai bộ số (đã nêu ở mục 1 phần soát) có hậu quả thật**: hs-5 dòng 10 và 39 đoán E pin mới = 1,50 V vì 3b/50·2 cho 1,50 V, rồi "sai". Học sinh thật cũng sẽ tin số đã cho sẵn.
2. **Pin mới 6 cặp chỉ có trong clip 4d**: hs-5 dòng 7–13 để trống cả 12 ô 52·1 và A, B 53·2. Lớp thật có clip nhưng clip trôi nhanh; không có bảng tĩnh dự phòng như màn 4c cho pin cũ. Đúng như mục 3 phần soát, nay có bằng chứng.
3. **"6 hay 12 lần đo"**: hs-4 dòng 9, 33, 42 và sach-hs 51·1 dòng 3 vẫn "đoán 12". Câu chữ màn 4a thiếu "mỗi pin".
4. **Ô 50·1 bốn hàng không đáp án** (pin, biến trở, R₀, K): hs-3 dòng 31. Mục mới.
5. **Ô 52·2 bảng 5 hàng và hai ☐ ampe kế không có đáp án nào** (mục 4 phần soát): hs-6 dòng 40 xác nhận; hs điền đúng nhưng "đoán".
6. **Hình (1), (2) ở ô 49·4**: hs-2 dòng 16, 21. Màn 2a không chỉ rõ điểm nào là (1), (2); hs không xem được hình Tập nên đây có thể là giới hạn lớp ảo, ghi "chưa kiểm hình".
7. **Dừng ① clip 4b**: hs-4 chọn A (đều); đáp án B chỉ có trong clip giây 19,5, không có câu giải thích bằng chữ.
8. Tài liệu khớp nhau (không lệch): 0,80 Ω ở 2b, 5b, 53·3; 4,8 % ≈ 5 %; 1,10 V; 5,0 A và 0,65 A. hs không phát hiện lệch ở các số này.
