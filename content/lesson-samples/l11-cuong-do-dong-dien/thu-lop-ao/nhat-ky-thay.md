# Nhật ký thầy · bài 22 Cường độ dòng điện

## Soát trước giờ (lượt 1)
Đối chiếu màn (tren-lop.src.html), ghi chú (tren-lop-ghi-chu.html), Tập (scripts/ruot-tap/l11-bai22.mjs tr.1–5):
1. **Số ô điền ghi chú ≠ Tập.** Ghi chú DP4: "4 chỗ điền + bảng 6 ô + 2 đồ thị phác + 2 ô luôn/không luôn": hàng "Đồ thị" đã nằm trong bảng 6 ô nên đếm trùng 2 ô. DP5/ô 3·3: ghi chú "7", Tập có "Đèn sáng ngay vì ___" **và** thêm một dòng kẻ trống bên dưới (lines(1)) nên thực tế 8 chỗ.
2. **Ô 2·3 lệch thứ tự dạy.** Tập đặt dòng "đổi mAh" ở đầu ô, trước bảng; ghi chú bảo điền sau lần dừng ③ của clip. Học sinh nhìn thấy "1 mAh = 10⁻³ A · ___ s" trước khi clip hỏi. Hàng 10 phút (900 C) đã in sẵn trong Tập, nhưng màn clip dừng ② liệt kê cả 900 như phải điền. Màn dừng ② hỏi "10 phút = ? s" mà Tập không có ô nào cho số 600 s.
3. **Khung đồ thị trong Tập (ô 2·3) bị bỏ rơi.** Tập có khung đồ thị $\Delta q$ theo $\Delta t$, màn chỉ ghi "Kết quả: đồ thị" và "đường thẳng qua gốc", ghi chú không nói ai vẽ, vẽ lúc nào.
4. **Màn "Rút ra" 3e có "90 C/phút = 1,50 A"** mà Tập không có ô nào ứng; học sinh sẽ không biết chép vào đâu. Ô "độ dốc đồ thị là ___" có đáp án $I$ nhưng màn chưa nói độ dốc nghĩa là gì trước đó.
5. **Bẫy 1 lộ đáp án trước khi biểu quyết:** ô 3·2 có dòng "Tăng $I$ trong cùng một dây là tăng ___, không phải tăng ___" điền ở màn 5b ngay trước biểu quyết Bẫy 1 (đáp án D = tăng $v$ không phải $n$). Học sinh điền dòng đó xong thì câu D đã rõ. Cũng ở Tập 4·1 bẫy 1 ghi "$n$ giữ nguyên, $v$ gấp đôi".
6. **Màn 3b hard-code "0,30 A" ở cột Minh hoạ**, còn ghi chú nói số thật có thể 0,2–0,3 A tuỳ bóng; màn nói "thang 1 A", ghi chú nói vạn năng DCA cỡ 1 A hoặc 10 A (thang 10 A đọc 0,3 A sai số lớn).
7. **Phút:** DP6 gồm 2 câu trả bài × 1,5 phút viết + đọc đáp án + quay lại công tắc + 20 giây ô 1·1 trong khung 27–30 phút; màn "Quay lại công tắc" ghi phút 29–30 chỉ 1 phút. DP3 (8 phút) chứa thí nghiệm 3 phút + clip 2 phút + rút ra + sai số + điền 9 chỗ: gần chắc vượt.
8. **Thứ tự lật trang:** DP2 phải lật tr.1 → tr.2 (ô 2·2) rồi DP3 lại về đầu tr.2 (ô 2·1) — ghi chú có nhắc, nhưng màn 3a ghi nhãn "ô 2·1" ngay sau màn 2c "ô 2·2" nên dễ nhầm số tăng/giảm.
9. **Khái niệm chưa dạy dùng trước:** "tiết diện thẳng" (màn 2a) chưa giải thích trước khi điền; "mật độ hạt tải $n$ (hạt/m³)", "điện trường lan dọc dây" dùng ở DP1 phương án D và DP5 khi chưa học; "chỉnh lưu" (màn 4c) chưa giải thích.
10. Màn 6c nói "làm đề 1217" nhưng trong 15 phút cuối chỉ có 20 câu; ghi chú tự cảnh báo ít nhất 5 câu trùng câu tự kiểm tra, trong đó cáp kích 50 mm² (bài toán mẫu 5·1, về nhà) và 300 mC (Bẫy 3, chỉ nói qua) là phần học sinh chưa làm trên lớp.

## Lượt 2 (sau khi học sinh làm)
(chưa làm)

### Lượt 2 · điều học sinh ảo cho thấy
- Xác nhận lượt 1 mục 5: Bẫy 1 lộ qua dòng "(do vật liệu, cho sẵn)" ở ô 3·2 (hs-5 d.4). Xác nhận mục 2: dòng đổi mAh + "Δt = ? s" + cột mAh/Δq gây nhầm (hs-3 d.11).
- Mới: câu "mắc song song thì dòng rất lớn" học sinh không hiểu (chưa học điện trở); "điện trường lan dọc dây" phải đoán; hàng "Chiều" hai cột giống nhau làm học sinh tưởng thiếu; ô 61–62 không ai hướng dẫn.
- Chưa kiểm chứng được: giờ giấc (mục 7), số thật ampe kế, nhìn hình (a)(b) từ bàn cuối. Học sinh ảo không thấy hình/clip.
- Tỉ lệ đúng không đáng tin: 5 ô điểm dừng 2–3 chỉ là chép/tính, đúng gần hết.
