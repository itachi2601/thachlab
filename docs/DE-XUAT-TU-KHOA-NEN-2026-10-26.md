# Đề xuất: nén dòng từ khoá 🔑 thành "mẹo vài chữ có tên" — rà 3 khối lớp 10–12 (26/10/2026)

Xuất phát từ video tóm tắt bài *Thuyết động học phân tử chất khí*: ba chữ **NHỎ – LOẠN – ĐẬP** dễ nhớ hơn dòng 🔑 gốc
"Kích thước bé xíu · Hỗn loạn không ngừng · Va chạm gây áp suất". Thầy muốn rà toàn bộ L10–L12 xem chỗ nào làm được như vậy.

Nguồn rà: 95 thư mục `content/lesson-samples/l10-*`, `l11-*`, `l12-*` (file `theory.src.html`), trích mọi dòng 🔑 (≈560 dòng).
Không mở DB. Bài nào đã đăng mà nguồn lệch DB thì khi sửa phải lấy bản DB làm gốc.

## 1. Tư vấn ngắn theo nghiên cứu đã có trong repo

- **Hợp G1** (`docs/QUY-TAC-THIET-KE.md`: trí nhớ làm việc ~4 khối, Cowan) và CLT (`docs/DE-XUAT-NGHIEN-CUU-HS-14-22-2026-10-11.md`):
  3–4 chữ đơn, mỗi chữ móc đúng một ý, là đúng cỡ khối mà HS 14–18 giữ được; dòng 🔑 hiện tại 9–14 chữ là 2–3 khối gộp.
- **Điều kiện để mẹo có tác dụng** (retrieval practice, mục 9 `docs/AI-TUTOR.md`): chữ mẹo phải (a) ánh xạ 1–1 với ý, (b) được *hỏi lại* ở
  Trả bài và quiz ("Loạn nghĩa là gì?"), (c) dùng *cùng một chữ* ở mọi bài có cùng ý. Mẹo chỉ đọc một lần rồi bỏ thì không hơn dòng 🔑.
- **Rủi ro**: mẹo vui nhưng mơ hồ ("Mù điện", "Ba cùng" dùng cho hai bài khác nhau) làm HS nhớ chữ mà không nhớ ý → mỗi chữ mẹo
  phải tra ngược được ra ý trong một nhịp; không dùng một mẹo cho hai nội dung khác nhau trong cùng khối lớp.
- **Không nén**: công thức, con số, cặp đối lập đã 2–4 chữ ("Phân tử nhanh · Mùi lan chậm"), bước thực hành. Nén ở đó chỉ thêm một tầng mã hoá.
- **Đo**: so điểm 6 câu Trả bài (web đã có) và câu quiz "đếm đủ N ý" giữa bài có mẹo và bài chưa có; sau một chương là đủ số liệu.

## 2. Tiêu chí chọn chỗ nén

Nén khi dòng 🔑 là **danh sách 3–5 ý song song** mà đề thi hay hỏi "đủ/thiếu" (điều kiện, đặc điểm, nội dung của thuyết, các bước),
và mỗi ý rút được về **một chữ đơn hoặc kép** vẫn đúng vật lí. Dòng 🔑 cũ **giữ lại** ngay dưới mẹo (mẹo là tầng nhớ, 🔑 là tầng nghĩa).

Dạng trình bày đề xuất (đã dùng trong video):
```
<p class="tl-meo">🧠 <b>NHỎ – LOẠN – ĐẬP</b></p>
<p class="tl-key">🔑 Kích thước bé xíu · Hỗn loạn không ngừng · Va chạm gây áp suất</p>
```
Ở "Mang về sau bài học": dòng đầu của mỗi mục là chữ mẹo; cuối khung thêm dòng "N hình = cả bài" (một hình ảnh/mục, N ≤ 5)
giống video — phiên fork đã tư vấn ý này, thầy duyệt chung ở đây.

## 3. Danh sách đề xuất theo lớp

Ký hiệu: ★ nên làm trước (ý đề thi hay hỏi đủ/thiếu, hoặc lặp ở nhiều bài); ○ làm nếu còn thời gian; ✗ không nén, giữ nguyên.

### Lớp 10

| Bài | Mục | 🔑 hiện có | Mẹo đề xuất | Ghi chú |
|---|---|---|---|---|
| ★ dinh-luat-3-newton | 2. Bốn đặc điểm cặp lực–phản lực | Cùng lúc · Cùng loại · Bằng nhau, ngược chiều · Khác vật | **BA CÙNG – MỘT NGƯỢC – MỘT KHÁC** (cùng lúc, cùng loại, cùng độ lớn; ngược chiều; khác vật) | Dùng lại y nguyên ở bẫy "cùng vật: cân bằng · khác vật: lực–phản lực" (bài tổng hợp lực, ma sát) |
| ★ dinh-luat-2-newton + giai-bai-toan-dong-luc-hoc | 5. Các bước / 1. Bốn bước | Chọn vật · vẽ lực · chọn chiều · F = ma  // Vẽ · Kể lực · Viết ΣF = ma · Chiếu và giải | **VẼ – KỂ – VIẾT – CHIẾU** (một mẹo cho cả hai bài) | Hiện hai bài ghi hai bộ bước khác nhau → HS học hai quy trình. Thống nhất là việc chính |
| ★ lam-quen-voi-vat-li | 5. Quy trình 5 bước | Quan sát → vấn đề → giả thuyết → kiểm tra → kết luận | **THẤY – HỎI – ĐOÁN – THỬ – CHỐT** | Hỏi lại ở Trả bài: "Đoán là bước nào?" |
| ★ luc-ma-sat | 1–2–5 (ba loại) | ba dòng 🔑 riêng | **NGHỈ – TRƯỢT – LĂN** + mỗi chữ một móc: *Nghỉ: cân bằng, chưa trượt · Trượt: μN · Lăn: nhẹ nhất* | Thêm bảng gộp 3 cột ở cuối mục 5; bẫy "đứng yên không dùng μN" treo vào chữ NGHỈ |
| ★ do-dich-chuyen-quang-duong | 2. Hệ quy chiếu | Vật mốc + trục toạ độ + đồng hồ | **MỐC – TRỤC – GIỜ** | |
| ★ chuyen-dong-nem | 1. Hai thành phần | Ngang: thẳng đều · Dọc: rơi tự do | **NGANG ĐỀU – DỌC RƠI** | Dùng lại ở điện trường đều L11 (hạt bay vào vuông góc): *Ngang đều – Dọc nhanh dần* |
| ○ moment-luc | 4. Ngẫu lực | Song song · ngược chiều · bằng nhau · cùng vật | **SONG – NGƯỢC – BẰNG – CÙNG** | Đối chiếu với BA CÙNG–MỘT NGƯỢC–MỘT KHÁC: ngẫu lực là *cùng vật*, lực–phản lực là *khác vật* — đặt hai mẹo cạnh nhau ở bẫy |
| ○ nang-luong-cong-co-hoc | 1. Năng lượng | Nhiều dạng · Chuyển hoá · Truyền đi · Không tự mất | **DẠNG – HOÁ – TRUYỀN – GIỮ** | đã 4 cụm ngắn, chỉ cần đặt tên |
| ○ chuyen-dong-tron-deu | 4. Vectơ vận tốc | Phương tiếp tuyến · Độ lớn không đổi · Hướng luôn đổi | **TIẾP – GIỮ LỚN – ĐỔI HƯỚNG** | |
| ○ su-roi-tu-do | 2. Đặc điểm | Thẳng đứng · Trên xuống · Nhanh dần đều | **THẲNG – XUỐNG – NHANH DẦN ĐỀU** | đã ngắn; đặt tên là đủ |
| ○ khoi-luong-rieng-ap-suat | 5. Bình thông nhau | Cùng chất lỏng · cùng mức ngang · cùng áp suất | **CÙNG CHẤT – CÙNG MỨC – CÙNG ÁP** | KHÔNG gọi "ba cùng" (trùng Newton 3) |
| ○ luc-can-luc-nang | 1. Lực cản | Ngược chiều · tăng theo tốc độ · tuỳ hình dạng | **NGƯỢC – NHANH THÌ LỚN – TUỲ DÁNG** | |
| ○ an-toan-phong-thuc-hanh | 3. Mười quy tắc | 10 từ khoá | giữ 10 từ, thêm tên 4 nhóm: **ĐỌC – ĐIỆN – TAY – DỌN** | 10 từ đã là mẹo; chỉ thiếu tầng nhóm |
| ✗ cong-suat, hieu-suat, dong-luong, dong-nang-the-nang, co-nang, trong-luc, tong-hop-luc, chuyen-dong-thang-bien-doi-deu, do-thi, toc-do-van-toc, 5 bài thực hành | | công thức, cặp đối lập 2 ý, bước đo | giữ nguyên | 🔑 hiện tại đã đúng cỡ |

### Lớp 11

| Bài | Mục | 🔑 hiện có | Mẹo đề xuất | Ghi chú |
|---|---|---|---|---|
| ★ **dao-dong-dieu-hoa** | toàn bài | **0 dòng 🔑** | soạn 🔑 cho 5 mục + mẹo | Bài duy nhất chưa có từ khoá — lệch chuẩn skill; làm trước mọi việc khác |
| ★ giao-thoa-song | 1. Hai nguồn kết hợp | cùng phương dao động · cùng tần số · lệch pha không đổi | **PHƯƠNG – TẦN – PHA** | đề hay hỏi thiếu một điều kiện |
| ★ tat-dan-cuong-buc | 1–4 (ba loại + cộng hưởng) | bốn dòng 🔑 riêng | **MẤT – BÙ – THEO – TRÙNG** (tắt dần mất năng lượng · duy trì bù đúng lúc · cưỡng bức theo lực · cộng hưởng trùng tần số) | Mục 6 "Ba loại nhìn một lượt" đã có bảng → thêm hàng mẹo |
| ★ song-dung | 1 + 3 + 5 | Cố định → ngược pha · Tự do → cùng pha; nguyên λ/2 · lẻ λ/4 | bảng 2 cột: **CỐ ĐỊNH: NÚT – NGƯỢC – NGUYÊN λ/2** / **TỰ DO: BỤNG – CÙNG – LẺ λ/4** | ba ý đang rải ở 3 mục → gom một chỗ |
| ★ khai-niem-dien-truong | 4. Đường sức điện | Tiếp tuyến là giá E · Ra từ dương · Vào ở âm · Mau thì mạnh | **TIẾP – RA – VÀO – MAU** | Đối chiếu L12 đường sức từ: **TIẾP – KÍN – KHÔNG CẮT – MAU** (xem L12) — HS thấy ngay khác nhau ở chữ thứ 2–3 |
| ★ cuong-do-dong-dien | 4. Hạt tải điện | Nhiều hạt · chạy nhanh · tiết diện to | **ĐÔNG – NHANH – TO** (I = nSve) | |
| ○ dien-truong-deu | 1. Đường sức | E như nhau · thẳng, song song, cách đều | **THẲNG – SONG – ĐỀU** | |
| ○ song-ngang-song-doc | 1–2 | Ngang: ⊥ truyền · Dọc: ∥ truyền | **NGANG VUÔNG – DỌC DỌC** | hoặc "Ngang vuông – Dọc song" |
| ○ tu-dien | 3. C do cấu tạo | S lớn · d nhỏ · ε lớn → C lớn | **RỘNG – SÁT – MÔI** | |
| ○ nguon-dien | 5. Ghép nguồn | Nối tiếp cộng E, cộng r · song song giữ E, chia r | **TIẾP: CỘNG–CỘNG · SONG: GIỮ–CHIA** | |
| ○ luc-coulomb | 2. Định luật; 5. Cân bằng | Phương nối · tỉ lệ tích · nghịch bình phương; hợp lực 0 · cùng phương · ngược chiều · bằng độ lớn | **NỐI – TÍCH – NGHỊCH VUÔNG**; cân bằng dùng lại **PHƯƠNG – NGƯỢC – BẰNG** (chung với cân bằng 2 lực L10) | |
| ✗ bai-tap-* (3 bài), mo-ta-song, mo-ta-dao-dong, van-toc-gia-toc, the-nang-dien, dien-the, dien-tro, nang-luong-cong-suat-dien, song-dien-tu, 3 bài thực hành | | công thức / đã có mẹo số (12·8·6·4) | giữ nguyên | |

### Lớp 12

| Bài | Mục | 🔑 hiện có | Mẹo đề xuất | Ghi chú |
|---|---|---|---|---|
| ★ thuyet-dong-hoc-phan-tu | 2. Ba nội dung | Kích thước bé xíu · Hỗn loạn không ngừng · Va chạm gây áp suất | **NHỎ – LOẠN – ĐẬP** | đã chốt từ video |
| ★ thuyet-dong-hoc-phan-tu | 4. Khí lí tưởng | Bỏ kích thước · Bỏ lực tương tác · Va chạm đàn hồi (**thiếu ý 3 "thẳng đều"**, bài nói 4 nội dung) | **CHẤM – KHÔNG LỰC – THẲNG – NẢY** | sửa luôn lỗi 🔑 thiếu ý |
| ★ ap-suat-dong-nang | 1. Mô hình nhìn từ thành bình | Phân tử nhỏ · Hỗn loạn · Va chạm đàn hồi | dùng lại **NHỎ – LOẠN – ĐẬP** + chữ **NẢY** | hiện hai bài liền nhau dùng hai bộ chữ cho cùng một thuyết |
| ★ su-chuyen-the | 1. Mô hình động học về cấu tạo chất | Hạt riêng biệt · Chuyển động không ngừng · Lực hút – lực đẩy | **RỜI – LOẠN – HÚT ĐẨY** | bài 1 chương 1 và bài 1 chương 2 chung chữ LOẠN → HS thấy mạch "cùng một mô hình" |
| ★ dong-dien-xoay-chieu + may-phat-dien-bien-ap | II.1 (cả hai bài, 🔑 giống hệt) | Quay khung · Từ thông đổi · Suất điện động xoay chiều | **QUAY – ĐỔI – SINH** (một mẹo, hai bài) | |
| ★ cam-ung-dien-tu | III. Điều kiện có dòng cảm ứng | Mạch kín · Từ thông biến thiên · Dòng cảm ứng | **KÍN – ĐỔI – DÒNG**; Lenz giữ chữ **CHỐNG** | đề hay hỏi "khung hở có dòng không" |
| ★ luc-tu-cam-ung-tu | 1. Lực từ lên đoạn dây | Điểm đặt giữa dây · Vuông góc dây và đường sức · Chiều bàn tay trái | **GIỮA – VUÔNG – TAY TRÁI** | |
| ★ khai-niem-tu-truong | 3. Đường sức từ | Vẽ theo quy ước · Khép kín · Không cắt nhau (+ mục 4: mau thì mạnh) | **TIẾP – KÍN – KHÔNG CẮT – MAU** | cặp với đường sức điện L11 |
| ○ nang-luong-lien-ket | 1. Lực hạt nhân; 4. Độ hụt khối | Hút rất mạnh · Không phụ thuộc điện tích · Tầm 10⁻¹⁵ m; Tách tốn · Tạo toả · Chia A so bền | **MẠNH – KHÔNG KỂ ĐIỆN – NGẮN**; **TÁCH TỐN – HỢP TOẢ – CHIA A** | |
| ○ phan-hach-nhiet-hach | 6. Điều kiện nhiệt hạch | Nhiệt độ cực cao · Mật độ lớn · Đủ lâu | **NÓNG – ĐẶC – LÂU** | |
| ○ ung-dung-cam-ung-dien-tu | 3. Dòng Foucault | Khép kín trong khối · Hãm · Toả nhiệt Joule | **XOÁY – HÃM – NÓNG** | thư mục `ung-dung-cam-ung.cu` là bản cũ, bỏ qua |
| ○ phong-xa | 2. Bốn loại tia | Nặng · Nhẹ · Sóng điện từ (**3 chữ cho "bốn loại"**) | **α NẶNG – β⁻ β⁺ NHẸ – γ SÓNG** | sửa lỗi đếm thiếu |
| ○ boyle-charles + phuong-trinh-trang-thai | ba đẳng quá trình | rải ở 2 bài | một bảng chung: **GIỮ T → pV · GIỮ p → V/T · GIỮ V → p/T** ("giữ cái nào thì bỏ nó khỏi pV/T") | mục 3 bài PTTT đã nói ý này; chỉ cần đặt bảng y nhau ở cả hai bài |
| ✓ an-toan-phong-xa (Nhanh · Xa · Chắn đủ), phong-xa §1 (Tự phát · Ngẫu nhiên · Miễn nhiễm), noi-nang §2 (Công · Nhiệt) | | **đã là mẹo 2–3 chữ** | giữ, chỉ thêm khung `tl-meo` cho đồng bộ | mẫu tốt để đối chiếu |
| ✗ thang-nhiet-do, hat-nhan, dien-tu-truong, 2 bài thực hành | | con số / công thức / đã ngắn | giữ nguyên | |

## 4. Lỗi phát hiện khi rà (sửa cùng đợt, không chờ duyệt mẹo)

1. `l11-dao-dong-dieu-hoa`: không có dòng 🔑 nào.
2. `l12-thuyet-dong-hoc-phan-tu` mục 4: 🔑 3 ý nhưng bài và Trả bài nói 4 nội dung (thiếu "thẳng đều giữa hai va chạm").
3. `l12-phong-xa` mục 2: tiêu đề "bốn loại tia", 🔑 3 chữ.
4. `l10-dinh-luat-2-newton` §5 và `l10-giai-bai-toan-dong-luc-hoc` §1: hai bộ bước giải khác nhau cho cùng quy trình.
5. `l12-ap-suat-dong-nang` §1 và `l12-thuyet-dong-hoc-phan-tu` §2: cùng thuyết, hai bộ từ khoá.
6. `l11-bai-tap-dao-dong` §4: hai dòng 🔑 dính liền không ngắt (kiểm `<br>`/thẻ đóng).

## 5. Cách làm, chia đợt

- **Đợt 1 (★, 20 chỗ, 17 bài)**: sửa `theory.src.html` → build → `cap-nhat-ly-thuyet.sh` từng bài (chỉ ghi `ly_thuyet`). Mỗi bài thêm:
  dòng `tl-meo` trên 🔑; chữ mẹo vào đáp án Trả bài tương ứng; một câu quiz "chữ X trong mẹo nghĩa là gì" nếu mục chưa có quiz;
  khung Mang về: dòng đầu mỗi mục là chữ mẹo + dòng cuối "N hình = cả bài".
- **Đợt 2 (○, ~17 chỗ)** sau khi có số liệu Trả bài của đợt 1 một chương.
- **Quy tắc vào skill `soan-bai-ly-thuyet-tuong-tac`** (chỉ thêm sau khi thầy duyệt): "Mục có 3–5 ý song song → thêm dòng 🧠 mẹo 3–5 chữ đơn,
  đặt trên 🔑; chữ mẹo lặp lại ở Trả bài và Mang về; cùng ý ở bài khác dùng cùng chữ (tra bảng mẹo chung `docs/BANG-MEO-TU-KHOA.md`)".
  Bảng mẹo chung là file mới, một dòng/mẹo, để các phiên sau không đặt hai mẹo cho một ý.
- **CSS**: thêm `.tl-meo` (chữ đậm, cỡ 🔑 + 2px, màu nhấn nền sáng theo `docs/MAU-NEN-SANG.md`), kiểm 375px.
- **Không đụng** `bundle.json`/quiz 20 câu của `soan-quiz-ly-thuyet`; chỉ mục lý thuyết.

## 6. Việc thầy cần chốt

1. Duyệt danh sách ★ (có thể gạch bỏ mẹo nào thấy gượng; chỗ gạch giữ 🔑 cũ).
2. Chữ mẹo có viết HOA toàn bộ như video, hay chỉ viết hoa chữ đầu (dễ đọc hơn trên điện thoại theo quy tắc C-nhóm trong QUY-TAC-THIET-KE)?
3. Có thêm dòng "N hình = cả bài" vào Mang về của mọi bài, hay chỉ bài có video?
