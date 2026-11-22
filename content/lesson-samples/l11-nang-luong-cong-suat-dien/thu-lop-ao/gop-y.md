# Góp ý bài 25 sau lớp ảo (lượt 2)

Ghi chú: HS ảo đi đúng thứ tự nên rò rỉ "nhìn trước" chỉ chứng minh gián tiếp; bằng chứng ghi rõ chỗ nào trực tiếp (hs) và chỗ nào từ nhật ký thầy (nk).
Viết tắt file: SRC = tren-lop.src.html · GC = tren-lop-ghi-chu.html · MJS = scripts/ruot-tap/l11-bai25.mjs

| # | file · vị trí | sửa gì | ưu tiên | bằng chứng |
|---|---|---|---|---|
| 1 | MJS · ô 40·1 (`.trap`, ba bẫy) | Bỏ tên bẫy dạng câu sai khỏi chữ in ("kW và kWh là một"…): đổi thành tiêu đề trung tính "Bẫy 1: kW và kWh", "Bẫy 2: công suất nguồn và mạch ngoài", "Bẫy 3: đèn nào sáng hơn" | cao | nk 1; hs-5 chọn đúng cả ba |
| 2 | MJS · ô 40·1 Bẫy 3 | Bỏ chữ "R lớn nhận nhiều hơn" khỏi dòng in; chỉ để "Nối tiếp (cùng I): P = ▭ · Song song: P = ▭" | cao | nk 2; hs-5 chọn C "vì R lớn hơn" ngay |
| 3 | SRC · màn m5d (thẻ đầu "5/6 · Bẫy 2: nguồn ≠ mạch ngoài") | Đổi thẻ đầu thành "5/6 · Bẫy 2" để không nói trước đáp án | cao | nk 1 |
| 4 | MJS · ô 39·2 dòng Rút ra "H có đạt 100 % không?" | Đổi thành "R tăng thì H ▭." và chuyển câu 100 % sang bước sau clip (hoặc để ▭ ở dòng khác sau điểm dừng ②); GC dừng ② ghi thời điểm điền | cao | nk 2; hs-4 chọn D, ô 63 lặp đáp án |
| 5 | MJS · ô 38·3 dòng Rút ra "R ▭ vì dây tóc ▭" và tiêu đề | Bỏ chữ "Đèn mờ thì R … vì dây tóc …" khỏi bản in cho tới sau clip, hoặc đổi thành "Nhận xét: ▭" | vừa | nk 2; hs-3 điền "nhỏ hơn / nguội" từ gợi ý chữ |
| 6 | MJS · ô 38·3 hàng I (cột 6,0 V) và ô 39·2 hàng U (cột 9,0 Ω) | Để trống I ở 6,0 V (cột đầu tiên clip dừng ① hỏi) và U ở 9,0 Ω; hoặc đổi câu dừng ① thành "nếu hạ xuống 3,0 V…" (không có trong bảng) ở SRC m3c, m4c | vừa | nk 3; hs-3 vẫn đoán 5 W dù có I nên rò rỉ chưa kiểm được trên HS thật |
| 7 | MJS · ô 38·4 + SRC · màn m3e | Cho cùng dạng: thêm vào Tập "Chọn A–D: ▭" rồi dòng "Vì sao không phải 50 W: P = ▭"; bỏ chữ "Vì sao không phải 50 W?" khỏi câu hỏi in (nó nói B sai) | vừa | nk 4; hs-3 chỉ ghi "không tỉ lệ thuận" |
| 8 | MJS · ô 38·1 + SRC · màn m2d | Màn 2d thêm hỏi kWh sau kJ (một dòng: "đổi sang kWh: ▭") hoặc bỏ "kWh" khỏi ô 38·1 | vừa | nk 4; hs-2 "đoán phần đổi kWh" |
| 9 | MJS · ô 38·2 dòng "Từ nhãn: I_đm = ▭ ; R = ▭ = ▭" | Đổi thành "R = U_đm²/P_đm = ▭" hoặc nói rõ trong màn m3b cách đổi nhãn → R; hiện HS đoán U/I | vừa | hs-3 (ô 33–34 ghi "đoán"); đáp án màn U²/P |
| 10 | SRC · màn m4b + MJS · ô 39·2 dòng "quạt, động cơ, pin đang sạc" | Thay "động cơ" bằng "quạt, pin đang sạc" (đã nhắc ở 2a) và thêm một câu "vì phần năng lượng này không thành nhiệt trong R" cho dòng U/𝓔 | vừa | nk 11; hs-4 "chưa rõ vì sao" |
| 11 | SRC · màn m4c clip dừng ② (phương án C/D) | Bỏ "tiến tới 100 % nhưng không chạm", đổi hai phương án thành đường cong tăng chậm dần vs. tăng thẳng/đạt 100 % rồi dừng, hoặc kèm gợi ý H = R/(R+r) ở đề; GC ghi cách giải thích "giới hạn" bằng lời | vừa | nk 11; hs-4 chọn D "đoán" |
| 12 | SRC · màn m2a (đầu điểm dừng 2) + MJS · ô 37·3 | Thêm dòng "Ô 37·3 để dành, lúc cuối tiết"; ô 37·3 đổi thành câu mới cùng ý (tủ lạnh 50 W chạy 1 ngày = ▭ số điện) thay vì quay lại câu 100 W | vừa | nk 5; hs-6 tự khai không độc lập |
| 13 | SRC · màn m6a + ô 40·2 | Ghi trên màn "câu 1 và 3 trên lớp, câu 2·4·5·6 về nhà" và in "(về nhà)" cạnh câu 2, 4, 5, 6 trong Tập | vừa | nk 13; hs-6 |
| 14 | MJS · ô 41·3 (`K.btvn().replace('<i>1</i>','<i>3</i>')`) | Truyền mã để hiện nhãn "Tập 41·3" như ô khác; kiểm khối BTVN chung | vừa | nk 7; hs-6 không tìm thấy nhãn |
| 15 | MJS · hình `H.noiTiep()` và ô 40·1 Bẫy 3 | Hình ghi "220 V – 100 W / 220 V – 40 W" ngay trên hai đèn; thêm chỗ ghi R₁, R₂ (▭ Ω) | vừa | nk 8; hs-5 phải dùng R=1210 Ω từ đáp án |
| 16 | SRC · màn m3c, m4c và GC · điểm dừng 3, 4 | Căn lại mốc giây dừng ①②③ với thời điểm lộ đáp án trong clip (13,6 s hiện 21 W, 17,9 s hiện 7,8 W trước thẻ đáp án 18,2 s; 14,3 s dừng ① clip 4c trước 14,63 s); ghi vào GC "dừng đúng giây X" và chỗ cắt | vừa | nk 9 (chưa xem khung hình, cần chụp lại) |
| 17 | GC · điểm dừng 3 và 4 (hướng dẫn "lớp tính ba hàng còn lại") | Sửa "ba hàng" thành "ba ô"; nói rõ ô 13,95 W (9,0 V) không lộ trong clip nên cho lớp tính ở dừng ③ | thấp | nk 10; hs-3 |
| 18 | GC · bảng nhịp điểm dừng | Thêm cột "bỏ nếu thiếu giờ": ĐD3 giữ 38·4 ngắn, ĐD5 bỏ 5d (đã có) và ghi số ô tối thiểu/điểm dừng | thấp | nk 12; hs-3 24 ô, hs-5 17 ô |
| 19 | SRC · màn m0 (mục tiêu) + GC | Màn mở đọc đúng chữ ô 37·1 hoặc bảo tích ☐ cuối tiết; thêm "tích ☐ ở 40·1" ở màn m5c | thấp | nk 6 |
| 20 | MJS · ô 39·2 và SRC · m5b | Định nghĩa "aptomat" một cụm (cầu chì tự ngắt) hoặc bỏ chữ; "định luật Jun–Len-xơ" ở 2b chú thích "đã học lớp 9" | thấp | nk 11; hs-5 không vướng nhưng khó với HS yếu |
| 21 | GC · mục "Đề 1220" | Ghi rõ chưa đối chiếu 19 câu; lập danh sách câu hỏi về khái niệm chưa dạy (động cơ, giới hạn H) trước khi dạy | thấp | nk 14; hs-6 không kiểm được |

## Đã xử lý (22/11/2026)
Làm: 1, 2, 3, 4, 5 (đổi dòng Rút ra ô 38·3 thành "Đèn mờ: ▭"), 9 (thêm gợi ý cách tính R từ nhãn), 10 (bỏ "động cơ", thêm lý do), 11 (phương án C/D bỏ "tiến tới… không chạm"), 12 (màn 2a ghi "37·1, 37·3 để dành"; chưa đổi câu ô 37·3), 13 (màn 6a), 14 (màn 6c/ghi chú gọi "khối Đề BTVN tr.41"), 16 (chỉ dừng ① clip 4c dời 14,3 → 14,7 s; mốc clip 3c giữ vì panel chữ không phải khung video, khung video tại 13,6 và 17,9 s chưa lộ đáp án), 17.
Bỏ/để lại: 6 (bảng I/U in sẵn, giữ vì HS ảo vẫn đoán; cần HS thật), 7, 8 (Tập tự luận khác màn A–D: giữ, đổi Tập sẽ lệch trang), 15 (hình Bẫy 3: chưa sửa hình), 18–21 (thấp).
Ruột tập: PDF vẫn 12 trang. Kiểm máy ĐẠT.
