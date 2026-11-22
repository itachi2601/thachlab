# Góp ý sau buổi chạy thử bài 17 Trọng lực và lực căng (học sinh ảo, 6 điểm dừng)

Ba file nói tới: **src** = `content/lesson-samples/l10-trong-luc-luc-cang/tren-lop.src.html` · **ghi chú** = `tren-lop-ghi-chu.html` · **.mjs** = `scripts/ruot-tap/l10-bai17.mjs`.
Số ô [n] là số chỗ trống trong `thu-lop-ao/sach-trong.md`. Bằng chứng trích từ `hs-N.md` (mục "Em thấy khó"), `sach-hs.md`, hoặc `nhat-ky-thay.md` (ghi rõ).

**Kết quả chung:** học sinh ảo điền được cả 6 điểm dừng; biểu quyết 4 quả (C), Mặt Trăng (C), kéo ngang (B), con lắc (D), lực căng bài mẫu (B), đĩa CD sau khi học (B). Tỉ lệ đúng không dùng làm bằng chứng. Các góp ý dưới đây dựa vào **chỗ học sinh nói phải đoán / không khớp** và **chỗ tài liệu lệch nhau**. Đề 1238 lớp ảo không làm nên chưa kiểm được; ghi chú dạy tự nêu câu 7, 8, 9, 17, 18 (Đúng/Sai) cần kiểm trên web có đủ ý a)–d).

---

## A. Ưu tiên CAO

| # | File · vị trí | Vấn đề | Sửa thành | Bằng chứng |
|---|---|---|---|---|
| 1 | **.mjs** p4 `h3(2,'Kết quả tự kiểm tra (đề chiếu trên lớp)','4·2')` + `rkHai([1,2,3],[4,5,6])` (ô 52·2); **src** màn 6c; **ghi chú** ĐD6 | Tập có bảng 6 câu, đề 1238 có 18 câu; Tập không có chỗ ghi điểm. | Thay `rkHai` bằng một dòng: "Điểm: …/18 · Câu sai: ____ · Câu đoán mò: ____" (như bài mẫu L11). Màn 6c ghi "ghi điểm vào ô 52·2". | hs-6 "Em thấy khó" mục 1; dung-6 màn 6c; nhat-ky-thay "Soát trước giờ" |
| 2 | **src** màn 5f (Bẫy 2); **ghi chú** ĐD5; **.mjs** p3 bảng ô 51·4 cột 1 | Cột "(lên nhanh dần, xuống chậm dần) ⇒ $\vec a$ hướng lên" chỉ ghi kết quả; không nói vì sao xuống chậm dần thì $\vec a$ hướng lên. HS chép theo màn, chưa hiểu, cuối buổi vẫn là chỗ khó nhất. | Màn 5f thêm hình hai mũi tên $\vec v$, $\vec a$ cho hai trường hợp (xuống chậm dần: $\vec v$ xuống, $\vec a$ lên) + dòng "$\vec a$ ngược $\vec v$ khi vận tốc giảm". Ghi chú ĐD5 thêm câu này. | hs-5 "Em thấy khó" mục 4; hs-6 mục 4; sach-hs ô 51·4 bảng |
| 3 | **src** màn 2a (Trọng lực) ↔ **.mjs** p1 ô 49·4 | Màn ghi công thức $P=mg$ trong khung riêng, không có nhãn "Độ lớn:"; Tập có chỗ trống "Độ lớn: $P=$ ___". HS không biết "khung lớn" là gì. | Màn ghi thẳng: "Độ lớn: $P=mg$" trong dòng của danh sách. | hs-2 "Em thấy khó" mục [__8__]; dung-2 màn 2a |
| 4 | **.mjs** p1 ô 49·1 (mục tiêu 4 ☐) + **ghi chú** ĐD6 (cuối tiết) | Mục tiêu dùng chữ "trọng tâm" khi HS chưa học và không ai nói khi nào đánh dấu ☐. Cuối buổi HS đánh dấu cả 4 mục kể cả mục "giải bài hệ vật" mà em tự nhận cần luyện thêm. | Ghi chú ĐD6: "đánh dấu ô 49·1 khi đã tự làm được (hệ vật: sau ô 53·2)". Màn mở đầu hoặc màn "Về nhà" thêm dòng "tr.49 ô 49·1: đánh dấu mục em làm được". | hs-1 "Em thấy khó"; hs-6 mục 5 |
| 5 | **ghi chú** ĐD2 + **src** màn 2d (thí nghiệm tấm bìa, ô mở "Ít nhất 2 lần") | "Ít nhất 2 lần, lần 3 để kiểm tra" không có lý do; HS phải nhớ "hai đường thẳng cắt nhau", không tự thấy. | Ô mở thêm dòng: "Mỗi lần treo cho một đường thẳng chứa $G$; hai đường (không song song) cắt nhau đúng một điểm". | hs-2 "Em thấy khó" (dòng cuối); phan-hoi-2 |

## B. Ưu tiên VỪA

| # | File · vị trí | Vấn đề | Sửa thành | Bằng chứng |
|---|---|---|---|---|
| 6 | **src** màn 3b (clip lực kế, bảng cuối) + **.mjs** p2 bảng ô 50·4 | Cột $P/m$: tính ra 9,75 (hàng cuối) nhưng màn ghi 9,8 và không nói quy tắc làm tròn; HS ghi 9,75, không biết có lệch không. | Tiêu đề cột "$P/m$ (N/kg, làm tròn 0,1)" hoặc màn ghi "9,75 ≈ 9,8". Ghi chú ĐD3 thêm "làm tròn tới 0,1". | hs-3 "Em thấy khó" mục [__34__]–[__37__]; sach-hs ô 50·4 |
| 7 | **.mjs** p3 ô 51·4 dòng "Em nặng 50 kg" ↔ **src** màn 3d (Bẫy 1) | Câu nhà du hành (trắc nghiệm) chỉ có trên màn; Tập chỉ có hai chỗ trống "kg đo ___; trọng lượng đo bằng ___". | Tập thêm một dòng cho đáp án câu nhà du hành ("Em chọn ___ vì ___") hoặc màn ghi "(ví dụ trên màn, không có trong Tập)". | hs-3 "Em thấy khó" mục cuối |
| 8 | **src** màn 4d (Bẫy 3) ↔ **.mjs** p3 ô 51·4 dòng 3 | Màn là trắc nghiệm A–D, Tập là "Gốc $\vec T$ ở ___, mũi chĩa ___" + chỗ vẽ; đáp án màn "gốc ở chỗ buộc" mơ hồ (buộc vào vật hay vào đinh). | Đáp án màn: "Gốc ở chỗ dây buộc **vào quả cầu**, mũi dọc dây chĩa **về điểm treo**". Ghi chú nói rõ "chỗ buộc = chỗ dây chạm vật". | hs-4 "Em thấy khó" mục [__43__]/[__67__] và dòng Bẫy 3; nhat-ky-thay ĐD4 |
| 9 | **src** màn 4b (hình đèn, ô mở) + **.mjs** p3 ô 51·1 hình | Màn chỉ ghi "kéo móc xuống", Tập chỉ ghi "vẽ $\vec T$ lên móc"; HS không rõ $\vec T$ lên móc hướng xuống. Ô vẽ [__48__], [__68__] không có chỗ tự đối chiếu ngoài khi thầy mở. | Ô mở màn 4b ghi: "$\vec T$ lên đèn: lên, gốc ở đèn · $\vec T$ lên móc: xuống, gốc ở móc". | hs-4 "Em thấy khó" mục 3 và 2 |
| 10 | **src** màn 2c (Trọng tâm) | "Sự phân bố khối lượng của vật" ([__18__]) HS chưa hình dung. | Thêm ví dụ một dòng: "hai quả cầu cùng cỡ, một đặc, một rỗng nửa bên: trọng tâm khác nhau". | hs-2 "Em thấy khó" mục [__18__] |
| 11 | **src** màn 3a (dòng $1$ N/kg $=1$ m/s²) | Chỉ ghi kết quả, không nói vì sao. | Thêm một dòng: "$g=P/m$ nên N/kg; $1\ \mathrm N=1\ \mathrm{kg\cdot m/s^2}$". | hs-3 "Em thấy khó" mục [__33__] |
| 12 | **src** màn 3a, 5c, 5f (bảng "Mở bảng") | Bảng ẩn nên HS chỉ chép được sau khi mở; chép gấp 6 ô một lúc. | Ghi chú: đọc từng hàng cho lớp ghi trước khi mở; hoặc hiện sẵn cột kiến thức, chỉ ẩn cột đáp án. | hs-3 "Em thấy khó" mục màn 3a |
| 13 | **ghi chú** bảng phút + thứ tự lật Tập | Ô 51·4 điền rải 3 lần (dòng 1 ở ĐD3, dòng 3 ở ĐD4, dòng 2 + bảng ở ĐD5) và lật tr.51 → 52 → 51 trong 5 phút; ĐD2 và ĐD5 nhiều màn trong 5–8 phút (nhật ký thầy ghi "chặt"). | Gom Bẫy 1, 2, 3 thành một lượt điền cuối ĐD5 hoặc đưa Bẫy 1 sang ô liền kề; hoặc cho phép chép bảng Bẫy 2 ở nhà (ghi chú đã cho phép, ghi lên màn). | nhat-ky-thay ĐD3, ĐD4, ĐD5 (không phải lời học sinh) |
| 14 | **ghi chú** ĐD5 (bài mẫu) | Chọn chiều dương khi chưa biết chiều chuyển động không được nói; HS hỏi. | Thêm một câu: "chọn một chiều dương, giải ra $a<0$ thì chiều thật ngược lại". | hs-5 "Em thấy khó" mục [__52__] |

## C. Ưu tiên THẤP

| # | File · vị trí | Vấn đề | Sửa thành | Bằng chứng |
|---|---|---|---|---|
| 15 | **src** màn 5d ↔ **.mjs** p4 ô 52·3 | Màn ghi "A (sang phải)", Tập ghi "chiều dương về phía ròng rọc". | Thống nhất "về phía ròng rọc" ở cả hai nơi. | hs-5 "Em thấy khó" mục [__86__] |
| 16 | **src** màn 5c dòng 3 | "a, T = ? → F=ma từng vật" tắt so với bước cần làm. | "$a$, $T$ chưa biết → viết $F=ma$ cho từng vật". | hs-5 "Em thấy khó" mục cuối |
| 17 | **.mjs** p4 ô 52·1 (mỗi câu một dòng `lines(1)`) | Câu 2, 5 trả lời dài, một dòng không đủ. | Cho `lines(2)` ở câu 2, 5 hoặc ghi chú: "viết gọn ý, không viết cả câu". | hs-6 "Em thấy khó" mục 2 |
| 18 | **.mjs** p4 dòng "Bạn cùng bàn kiểm" + **ghi chú** ĐD6 | HS không biết kiểm lúc nào. | Ghi chú: "sau khi lớp tự sửa, đổi bài cho bạn bên cạnh, mỗi câu đúng một ☐". | hs-6 "Em thấy khó" mục [__75__]/[__76__] |
| 19 | **.mjs** p2 ô 50·4 "P/m gần bằng ___" (`f(12)`) | HS viết "g ≈ 9,8 N/kg" dài hơn chỗ trống. | Mở rộng chỗ trống `f(25)`. | hs-3 "Em thấy khó" mục [__39__] |

## Đã xử lý (22/11/2026)

| # | Kết quả | Ghi chú |
|---|---|---|
| 1 | Làm | .mjs ô 52·2: bỏ `rkHai` 6 câu, thay dòng "Điểm …/18 · Câu sai · Câu đoán mò"; màn 6/6 QR đã ghi "ô 52·2 ghi điểm"; ghi chú ĐD6 ghi rõ ba mục. |
| 2 | Làm một phần | Thêm màn mới "Hướng của gia tốc" (m5v) trước Bẫy 2: hình vật treo với $\vec v$ xuống, biểu quyết $\vec a$ lên/xuống, hình đáp án thêm $\vec a$ lên + "vận tốc giảm ⇒ $\vec a$ ngược $\vec v$"; ghi chú ĐD5 thêm. Tập chưa thêm dòng này: thêm vào ô 51·4 làm tr.51 tràn 6 mm (trang 3 đang dư 0 mm). |
| 3 | Làm | Màn 2a: bỏ khung $P=mg$ riêng, ghi "Độ lớn: $P=$ <u>mg</u>" trong danh sách như Tập. |
| 4 | Làm | Màn "Về nhà" thêm dòng "tr.49 ô 49·1: đánh dấu mục em đã tự làm được (hệ vật: sau ô 53·2)"; ghi chú ĐD6 thêm. Chữ "trọng tâm" trong mục tiêu giữ nguyên (mục tiêu nêu cái sẽ học). |
| 5 | Làm | Ô mở màn 2d: "mỗi lần một đường chứa $G$, hai đường cắt nhau tại $G$. Lần 3: kiểm tra." |
| 6 | Làm | Màn 3b: cột "$P/m$ (làm tròn 0,1)"; Tập ô 50·4 thêm "P/m làm tròn 0,1" vào dòng câu hỏi (đổi tiêu đề cột làm tr.50 tràn 2 mm); ghi chú ĐD3 thêm ví dụ 9,67 → 9,7; 9,75 → 9,8. |
| 7 | Làm | Chọn cách rẻ: màn 3d ghi "(chỉ trên màn, trả lời miệng)"; ghi chú ĐD3 nói rõ. Không thêm dòng vào Tập (tr.51 không còn chỗ). |
| 8 | Làm | Đáp án màn 4d: "Gốc ở chỗ dây buộc vào quả cầu, mũi dọc dây chĩa về điểm treo"; ghi chú ĐD4 "chỗ buộc = chỗ dây chạm vật". |
| 9 | Làm | Ô mở màn 4b: "Lên đèn: hướng lên, gốc ở đèn · Lên móc: hướng xuống, gốc ở móc"; ghi chú ĐD4 sửa theo. |
| 10 | Làm | Màn 2c thêm ví dụ cái búa (trọng tâm lệch về đầu sắt). Không dùng ví dụ quả cầu rỗng nửa bên: khó hình dung hơn. |
| 11 | Làm | Màn 3a thêm "vì $1$ N $=1$ kg·m/s²"; ghi chú ĐD3 thêm câu nói "$g=P/m$ nên N/kg". |
| 12 | Làm | Ghi chú phần chuẩn bị: hỏi và ghi từng hàng rồi mới Mở bảng. Cột kiến thức đã hiện sẵn, chỉ cột đáp án ẩn, nên không sửa màn. |
| 13 | Làm một phần | Màn Bẫy 2 thêm "chưa kịp chép bảng thì chép ở nhà"; ghi chú ĐD5 thêm. Không gom ba Bẫy về một lượt: mỗi Bẫy đi ngay sau phần kiến thức của nó, gom cuối giờ làm Bẫy xa ngữ cảnh. |
| 14 | Làm | Ghi chú ĐD5: chọn một chiều dương; giải ra $a\lt0$ thì chiều thật ngược lại. |
| 15 | Làm | Màn 5d: "$A$ (về phía ròng rọc)", khớp Tập. Vật $B$ giữ "(xuống)" cho vừa màn. |
| 16 | Làm | Màn 5c: "$a$, $T$ chưa biết → viết $F=ma$ cho từng vật". |
| 17 | Làm | .mjs ô 52·1: câu 2 và câu 5 thành `lines(2)` (tr.52 vẫn dư 4 mm); ghi chú: viết gọn ý. |
| 18 | Làm | Ghi chú ĐD6: sau khi tự sửa, đổi Tập cho bạn bên cạnh ghi dòng "Bạn cùng bàn kiểm". |
| 19 | Làm một phần | Chỗ trống "P/m gần bằng" từ `f(12)` lên `f(20)` (không lên `f(25)`: tr.50 tràn 2 mm). |

Ruột tập: PDF giữ 12 trang (trước 12, sau 12; mỗi trang dư ≥ 0 mm). Bản chiếu: 27 màn; kiem.mjs: 1280×720 và 1920×1080 không tràn, katex-error 0, "$" còn 0; 375px scrollWidth 375.
