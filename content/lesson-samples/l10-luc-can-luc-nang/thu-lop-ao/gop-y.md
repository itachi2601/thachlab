# Góp ý sau buổi chạy thử bài 19 Lực cản và lực nâng (học sinh ảo, 3 lượt gộp 6 điểm dừng)

Ba file: **src** = `content/lesson-samples/l10-luc-can-luc-nang/tren-lop.src.html` · **ghi chú** = `tren-lop-ghi-chu.html` · **.mjs** = `scripts/ruot-tap/l10-bai19.mjs`.
Số ô [n] là số chỗ trống trong `thu-lop-ao/sach-trong.md`. Bằng chứng từ `hs-N.md`, `sach-hs.md`.

**Kết quả chung:** học sinh ảo điền đúng 94 ô làm trên lớp (phần về nhà để nguyên); biểu quyết đúng cả 5 câu (hai tờ giấy chọn B, Bẫy 1 A, bình tràn A, nhôm B). Nên góp ý dựa vào chỗ HS **phải đoán** và chỗ **tài liệu lệch nhau**. Số trang giữ nguyên với mọi sửa chữ trong ô của .mjs.

---

## A. Ưu tiên CAO

| # | File · vị trí | Vấn đề (bằng chứng) | Sửa thành |
|---|---|---|---|
| 1 | **.mjs** p4 ô 4·3 `rkHai([1,2,3],[4,5,6])` + **src** `#m6b` | Tập 6 dòng, đề 1240 có 19 câu. hs-3: "em không biết ghi 6 câu nào, nhiều bạn sẽ bỏ ô này". | Đổi tiêu đề ô 4·3 thành "Đề 1240 (19 câu, cuối tiết)"; thay `rkHai` bằng một dòng: "Điểm: ……/19 · câu sai: ………… · câu đoán mò: …………" (giữ số trang). Màn `#m6b`: thêm "ghi điểm vào ô 4·3". |
| 2 | **src** `#m3b` + **.mjs** p2 ô 2·2 dòng "Ghi số 1, 2, 3…" | HS không biết số nào ứng vạch nào: hs-2 "[32][33][34] ghi 1, 2, 3 theo thứ tự nhưng không biết ô nào ứng với vạch nào (đoán)". | `#m3b` đặt nhãn "GĐ 1, GĐ 2, GĐ 3" cùng cỡ chữ lên hình; .mjs đổi câu thành "Ghi GĐ 1, 2, 3 vào ba ô dưới đồ thị, từ trái sang phải". |
| 3 | **src** `#m3` ĐD3 + **ghi chú** ĐD3 | ĐD3 4 màn, ~20 ô trong 5 phút; hs-3 "dồn nhất ĐD3… chép theo thầy, không kịp nghĩ". | Chuyển màn 3d (lực nâng, [39]–[41]) về nhà và ghi vào màn Về nhà; ghi chú ĐD3 đặt sẵn "bỏ 3d trước" thay vì "nếu thiếu giờ". |
| 4 | **src** ĐD5 `#m5a`–`#m5d` + **ghi chú** ĐD5 | 4 màn trong 4 phút; hs-3: "ĐD5 em chép theo thầy, không kịp nghĩ". | Mặc định bỏ màn 5a Δp (chốt hai dòng, [61] về nhà) hoặc dời 5d "giải" về nhà; ghi chú đổi phút ĐD4 17–22, ĐD5 22–27. |
| 5 | **src** `#m2a` + **ghi chú** ĐD2 màn 2b | `#m2a` chiếu sẵn "Độ lớn phụ thuộc hình dạng và tốc độ"; hs-1: [14][15] điền được từ màn 2a, không cần PhET; PhET không có ô: "em không biết cần ghi kết quả vào đâu". | Bỏ dòng "Độ lớn…" khỏi `#m2a` (hai ô [14][15] điền sau PhET ở màn kết quả `#m2b`), hoặc thêm vào Tập ô 1·5 dòng "PhET: lần 2 ngắn/dài hơn [ ]". |
| 6 | **.mjs** p5 "Phân tích đề", "Giải" + **src** nhãn màn 5c/5d | Hai mục không mã ô, mã nhảy 5·1 → 5·4. hs-3: "không có mã ô trong Tập, em điền bằng số [83]–[90] của file". | `h3(2,'Phân tích đề','5·2')`, `h3(3,'Giải','5·3')`; nhãn `#m5d` đổi "tr.5 · ô 5·2, 5·3". |
| 7 | **.mjs** p2 ô 2·3 / 2·4 thứ tự + p3 ô 3·1 / 3·2 | Thứ tự lật lệch lớp: hs-2 "Tập ô 2·3 đứng trước 2·4 nhưng thầy làm 2·4 trước… 3·1 nằm trên 3·2". | Đổi thứ tự mục trong p2 (Làm nhanh 2·4 lên trước lực nâng) và p3 (bình tràn lên trước Archimedes), hoặc đổi thứ tự màn: lực nâng trước Bẫy 1; Archimedes trước bình tràn là không hợp, nên đổi Tập. Phải kiểm số trang. |

## B. Ưu tiên VỪA

| # | File · vị trí | Vấn đề (bằng chứng) | Sửa thành |
|---|---|---|---|
| 8 | **src** `#m2d` mở "rút ra" + **.mjs** ô 2·1 | hs-1: "[23] 'v²' em đoán… nếu thầy không nói, em sẽ viết 'tốc độ'". | Ô mở thêm câu: "$v^2/n$ không đổi ⇒ $F_c \sim v^2$"; .mjs đổi chỗ trống thành "lực cản tăng gần theo ( ) của tốc độ" (giữ số trang). |
| 9 | **src** `#m2c` + **.mjs** p2 | Biểu quyết A/B/C phễu không có ô trong Tập; hs-1: "em giơ tay B nhưng không có chỗ ghi". | Thêm vào ô 2·1 dòng "Đoán: ☐A ☐B ☐C" (một dòng, giữ số trang) hoặc ghi chú ghi rõ "chỉ giơ tay, không ghi". |
| 10 | **src** `#m3c` ↔ **.mjs** ô 2·4 | Tập là câu viết ("còn trọng lực không? Lực cản so với trọng lượng, hợp lực?"), màn là A–D. | Màn `#m3c` thêm dòng "Ghi vào ô 2·4: còn trọng lực không? lực cản so với trọng lượng? hợp lực?" dưới đáp án; hoặc đổi Tập thành A–D. |
| 11 | **.mjs** p4 ô 4·4 và 2·4 | "Câu 1." trùng ở hai ô (2·4 và 4·4). | 2·4 → "Câu 1 (Bẫy 1)", 4·4 → "Câu 2" hoặc "Khối gỗ" (giữ số trang). |
| 12 | **src** `#m4c` + **.mjs** p3 ô 3·1 dòng "Độ lớn" | hs-2: "[47][48] ρgV rồi dV theo màn 4c; nếu không có màn em sẽ viết d·V trước. Thứ tự hai chỗ không rõ." | .mjs đổi thành "bằng trọng lượng phần ( ) bị chiếm chỗ: F_A = ( ) = ( )" kèm "đầu: dạng dùng d; sau: dùng ρ" hoặc màn 4c ghi "F_A = dV = ρgV" đúng thứ tự Tập. |
| 13 | **.mjs** p3 ô 3·2 + **src** `#m4b` | Tập ghi "hạ sâu thêm vẫn 1,67 N", clip không có (ghi chú đã nói). g = 9,8 ở đây, 10 ở nơi khác (hs-2). | Trong Tập: bỏ "hạ sâu thêm vẫn 1,67 N" ra khỏi dòng quan sát, hoặc ghi "(thầy hạ sâu thêm trên lớp)" và làm thật nếu có lực kế. Màn `#m4b` ghi "g = 9,8 ở ô này; các ô khác g = 10". |
| 14 | **src** `#m4b` + **.mjs** hành trang 1·4 | hs-2: "[52] đổi 100 cm³ = 10⁻⁴ m³… hành trang chỉ nhắc 1 cm³ = 10⁻⁶; em phải tự nhân 100". | Màn `#m4b` thêm dòng "$100\ \text{cm}^3=100\cdot10^{-6}=10^{-4}\ \text{m}^3$" trong ô "Mở: tính". |
| 15 | **src** `#m4a` | Biểu quyết A không có cái neo: hs-2: "em giơ A do nước tràn được vẽ to trên hình". | Thêm câu gợi trên màn trước ▶: "Nước tràn ra là nước ở đâu? (chỗ vật chiếm)". |
| 16 | **src** `#m5a` + **.mjs** p3 ô 3·3 | [59] dấu hay chữ? [60] chữ gì? [61] Δh·S = V không rõ (hs-3). | .mjs ô 3·3: "F₂ ( >, <, = ) F₁; các mặt bên ( )" và "…= ρg·(Δh·S) = ρgV"; màn 5a ghi thêm "Δh·S = V thể tích hộp". |
| 17 | **src** `#m5b` ghi chú ĐD5 | [65] "bằng" mới nói lần đầu (hs-3: "trước đó em sẽ chọn 'lớn hơn' vì vật nổi lên"). | Thầy hỏi miệng trước khi mở: "vật nằm yên mặt nước thì hợp lực?"; ghi chú ĐD5 thêm câu hỏi này. |
| 18 | **src** màn `m6giay` (Quay lại hai tờ giấy) | hs-3: "chán vì đã nghe B từ đầu giờ"; D (lực đẩy không khí) chưa giải thích bằng công thức. | Thêm một dòng ô mở: "D: $F_A=\rho_{kk} gV$ với $\rho_{kk}\approx1{,}2\ \text{kg/m}^3$, nhỏ hơn 800 lần nước, nên không đáng kể". Đổi hỏi D trước, rồi mới mở đáp án B. |

## C. Thấp

| # | File · vị trí | Vấn đề (bằng chứng) | Sửa thành |
|---|---|---|---|
| 19 | **.mjs** p4 ô 4·2 "mỗi câu có ☐" + ô 4·1 | hs-3: ô 4·1 "tích bẫy em từng sập" mơ hồ nếu chưa sập; ☐ ở 4·2 không nói khi nào tích. | 4·1: "tích bẫy em dễ sập nhất (hoặc cả ba nếu em cẩn thận)"; 4·2: thêm "☐ = đã kiểm với bạn" (giữ số trang). |
| 20 | **src** `#m6c` Về nhà + **ghi chú** | Tàu thép và 5·5 không có gợi ý (hs-3: "[66] chưa biết trả lời… không có ví dụ tương tự trên lớp"). Màn Về nhà không nhắc ô 4·3. | `#m6c` thêm "tr.3 ô 3·4 tàu thép: gợi ý: tàu rỗng, phần chìm lớn?" và "tr.4 ô 4·3 ghi điểm đề 1240"; ghi chú ĐD6 thêm 1 ví dụ tương tự 5·5 nói miệng ("chìm, lực kế giảm 1 N thì V = ?"). |
| 21 | **src** `#m5c` | Biểu quyết A–D không có ô trong Tập; hs-3: "em tính trên giấy nháp". | Ghi chú: "chỉ giơ tay, không ghi" hoặc lấy kết quả điền vào ô 5·4 lề. |
| 22 | **ghi chú** bảng đề cuối tiết | "Chưa đối chiếu từng câu đề 1240 với phần học trên lớp". | Trước khi dạy, chạy đề 1240 qua `ra-soat` đối chiếu từng câu với ô 1·1 mục tiêu; ghi mục tiêu nào có/không có câu. |
