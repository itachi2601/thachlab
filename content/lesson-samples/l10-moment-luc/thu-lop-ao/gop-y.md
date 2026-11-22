# Góp ý sau chạy thử lớp ảo — Bài 21 Moment lực

File gọi tắt: **src** = tren-lop.src.html · **ghi chú** = tren-lop-ghi-chu.html · **.mjs** = scripts/ruot-tap/l10-bai21.mjs. Bằng chứng trích hs-1…hs-7 và sach-hs; mục chỉ từ phần soát tài liệu của thầy ghi "soát" (chưa có HS trải nghiệm). HS ảo vô tình thấy một phần khối RIÊNG THẦY nên không dùng tỉ lệ đúng; chỉ tin chỗ "(đoán)" và chỗ lệch tài liệu.

## A. Ưu tiên CAO

| # | File · vị trí | Vấn đề (bằng chứng) | Sửa thành |
|---|---|---|---|
| 1 | .mjs · ô 4·1 (tiêu đề + dòng kiểm) + src màn 6b + ghi chú "Tập chưa có ô ghi điểm đề 1242" | hs-7: "không biết chắc ghi điểm ở lề ô 4·1 hay chỗ khác (thầy nói lề ô 4·1)"; soát: ô 4·1 chỉ 6 câu, đề 1242 20 câu | Đổi tiêu đề ô 4·1: "Kết quả tự kiểm tra (Câu 1–6) · Đề 1242: ……/20 · câu sai ……" (giữ số trang); màn 6b ghi "ghi điểm vào dòng tiêu đề ô 4·1"; ghi chú sửa theo |
| 2 | .mjs · ô 2·4 bảng $F_2$ (cột 20 cm) + src màn 3d bước 1 | soát: bảng in sẵn 1,52 N trước câu "móc ở 20 cm"; hs-3 chọn B nhưng lời "Úp Tập xuống" chỉ dặn miệng, HS ảo không úp được | Cột $F_2$ chỉ in hai hàng đầu (10, 15 cm), hai hàng 20, 30 cm để trống (HS điền khi xem bảng cuối clip); sửa chữ ghi chú "bảng đã in sẵn số" |
| 3 | .mjs · ô 3·3 (ba bẫy) vị trí và nội dung | soát: tr.3 in sẵn lời giải bẫy 1–3 cùng trang với 3·1, 3·2; hs-4 "đánh dấu bẫy 3" ngay; Câu 5 trùng ý bẫy 3 in sẵn | Chuyển 3·3 sang tr.4 hoặc in dạng "bẫy chưa lộ lời giải" (chỉ ghi câu sai, lời giải hiện sau khi lớp làm Câu 3, 4, 5); hoặc bỏ phần "Đo vuông góc… $d=r\sin\alpha$" và "tổng lực bằng 0 mà vẫn quay" |
| 4 | src · màn 2e, 3b, 4d: nhãn "Bẫy 1/2/3" ở góc màn trước biểu quyết | soát: nhãn báo trước đây là câu bẫy; hs-2, hs-3, hs-4 đều "tick bẫy" ngay sau khi sai | Đổi nhãn thành "Tự kiểm tra · Câu N"; nhãn "Bẫy N" chỉ hiện trong khối đáp án sau khi mở |
| 5 | src · màn 4c, 4d; .mjs ô 3·2 dòng Thử | soát: Câu 5 dùng đúng số liệu dòng Thử vô lăng (20 N, 0,36 m) mà màn 4c vừa dạy tổng = 0; hs-4 "làm được" dòng Thử | Đổi số liệu Câu 5 (vd. 25 N, 0,30 m, moment 7,5 N·m) hoặc đổi đối tượng (bánh lái); phương án giữ cấu trúc, đáp án đổi |
| 6 | ghi chú + src · phân bổ ĐD4 (ô 3·1 + 3·2 + clip + Câu 5 = 23 chỗ trong 5 phút) | soát; hs-4: chép 7 + 14 chỗ "theo chữ thầy đọc", không hiểu trọng tâm | Dời dòng Thử tấm ván (3·1) và 3 chỗ cuối ô 3·2 về nhà hoặc sang ĐD5; kéo ĐD4 thành 6 phút bằng cách rút ĐD1 xuống 2 phút |
| 7 | .mjs + src màn 6c · mục Đề BTVN (tr.5 mục 1), "Điền bước còn thiếu", Phân tích đề, Giải | hs-7: "chưa biết thầy giao đề ở đâu trên web, sẽ hỏi"; soát: các mục này không có mã ô | Đánh mã 5·1 cho Đề BTVN; 4·3 Phân tích đề, 4·4 Giải, 4·5 Điền bước (đổi 4·2 thành bài toán mẫu đề bài); sửa mọi màn nhắc ô; thêm dòng "Thầy giao đề trên web: thachlab → lớp → bài 21 → Bài tập về nhà" vào màn 6c |
| 8 | src màn 6c + .mjs 4·1 · "Bạn cùng bàn kiểm Trả bài" | hs-5: "em chưa chắc bạn đúng"; soát: dòng kiểm in ở tr.4 ô 4·1 mà Trả bài ở tr.5 ô 5·3, trùng với bảng 6 câu | Chuyển dòng "Bạn cùng bàn kiểm: ……/6 · chưa thuộc … → đọc lại ô …" sang ngay dưới 5·3 (tr.5); xoá khỏi 4·1; đổi màn 6c |

## B. Ưu tiên VỪA

| # | File · vị trí | Vấn đề (bằng chứng) | Sửa thành |
|---|---|---|---|
| 9 | src · màn 2c Câu 1 phương án C = 0,0083 N | soát: loại ngay bằng độ lớn | Đổi C thành $0{,}83$ N hoặc $12$ N (kết quả nhầm $36/3=12$) |
| 10 | src · màn 5c Câu 6 phương án D, và đề Câu 6 | hs-5: chọn B vì "hai lực bằng nhau thì cân bằng", sai; soát: D dùng "nhỏ hơn trọng lượng thanh" không thuộc điều đã học; Câu 6 phụ thuộc $P_1=20$ N | Thêm vào đề "Túi gạo $20$ N (kết quả vừa tìm)" để HS không tính lại; D: "Không cần, thanh đã cân bằng sẵn" |
| 11 | .mjs · ô 1·2 hình búa; src màn 1 + màn 6b | hs-1: "không thấy rõ chỗ trục", "không biết đo khoảng cách từ trục tới giá kiểu nào"; hs-6: "số 8 cm và 30 cm em đọc từ hình (đoán)" | Hình búa: đánh dấu rõ điểm tì ($O$), hai đoạn 8 cm và 30 cm; dòng Quay lại búa in chữ "$OM=0{,}08$ m, $OT=0{,}30$ m" hoặc nhắc đọc hình ở màn 6b |
| 12 | src · màn 2d, .mjs ô 2·1 dòng "đề cho góc … dùng sin/cos" | hs-2: "chưa hiểu vì sao góc với OA dùng sin còn góc với phương vuông góc dùng cos"; hs-7 "không chắc sin hay cos" ở ★★ | Thêm màn nhỏ: hình tam giác chỉ rõ cạnh đối = $d$; 1 câu: "góc 60° với mặt cửa → d = 0,9·sin60°"; ghi chú nhắc hỏi lớp "góc nào đối diện cánh tay đòn" |
| 13 | .mjs ô 2·4 dòng "vì" (1 dòng) + ghi chú | hs-3: "dòng vì chưa viết, thầy cho về nhà"; "vì sao d2 càng xa số chỉ càng nhỏ" chưa hiểu | Hoặc chuyển dòng "vì" sang về nhà (ghi vào màn 6c), hoặc thêm 1 phút nói "$F_2d_2$ không đổi nên $d_2$ tăng thì $F_2$ giảm" |
| 14 | src · màn 3c ô 2·3 + .mjs hint "(độ lớn, cùng làm quay chiều kim)" | hs-3: "thuận/ngược phải nhìn hình mới biết chiều nào"; soát: hint dễ làm điền sai $M_1'+\dots$ | Bỏ hint trong ngoặc; màn 3c thêm hình hai mũi tên cong thuận/ngược |
| 15 | src · màn 4a ô 3·1 "bất kì", ghi chú | hs-6: "không chắc có cụm 'điểm bất kì'"; hs-7: "'điểm bất kì' nghĩa là gì trong thực tế" | Thêm câu "bất kì = em tự chọn, cho phương trình gọn nhất" trên màn 4a |
| 16 | src · màn 5b Giải; .mjs khung Giải (2+3+2+2 dòng) | hs-5: "khung Giải 2 dòng không đủ"; "không tự hiểu vì sao chọn O" | Tăng chỗ viết dòng 1 và 3 (3 dòng); màn 5b mở "vì sao O" trước khi tính |
| 17 | ghi chú · thứ tự lật (≈10 lần) | soát: tr.1→4→2→4→3→4→5→1; hs-2 "viết tắt" ở bảng 4·1 | Đổi thứ tự chiếu Câu theo số (1,2,3…) ở những chỗ có thể; hoặc in bảng 4·1 trên tr.3 cạnh ô cần dùng; ghi chú cho thêm "gấp góc tr.4" |
| 18 | ghi chú + src màn 6b "Quay lại búa" · ô 1·1 | soát: ô 1·1 không có màn; hs-6 tự đánh dấu 3/4 (đoán) | Thêm dòng "tr.1 ô 1·1: đánh dấu mục tiêu em đã làm được" vào màn 6b |
| 19 | src · màn 3d, 4b mốc 14.3→14.4, 8.9→9.0 | soát: cách 0,1 s dưới ngưỡng 0,3 s | Đo lại khung hình; dời mốc kế tiếp ≥ 0,3 s (14.6, 9.2) |

## C. Ưu tiên THẤP

| # | File · vị trí | Vấn đề (bằng chứng) | Sửa thành |
|---|---|---|---|
| 20 | src · ô 3·2 "trọng tâm" | hs-4: "chưa biết trọng tâm là gì, điền theo chữ thầy đọc" | Màn 4c thêm gợi ý "trọng tâm = điểm đặt trọng lực" |
| 21 | .mjs ô 5·2 ba dòng "(2 dòng)" | hs-7: "có thể không đủ" | Tăng ★★ lên 3 dòng, ★★★ lên 4 dòng nếu còn chỗ trên trang |
| 22 | ghi chú · phần clip | soát: màn cần mạng | Giữ; thêm dòng "tải trước hai clip về máy" |

## Ghi chú của thầy cho phiên sửa

- Làm A1, A2, A3, A7, A8 (đụng .mjs: giữ số trang PDF), rồi A4–A6 (src + ghi chú), rồi nhóm B.
- Đáp số đối chiếu BTVN của HS: ★ 3 N·m đúng; ★★ cách đúng là $40\cdot0{,}9\cdot\sin60^\circ\approx31{,}2$ N·m (HS ảo ra 18 là dùng cos, chính là lệch ở #12); ★★★ $N_A=180$ N, $N_B=120$ N đúng; Điền bước ($OA=0{,}3$): $OG=0{,}3$ m, $P_1=40$ N, $N=80$ N đúng.

## Đã xử lý

Làm 19, bỏ 3 (#20–22: ưu tiên thấp theo chỉ đạo; #22 đã có sẵn dòng "bấm ▶ rồi ↺ để tải trước", thêm "tải trước hai clip" vào ghi chú).

- 1 làm: tiêu đề ô 4·1 thành "Kết quả tự kiểm tra (Câu 1–6) · Đề 1242: ……/20 · câu sai ……"; màn 6b và ghi chú nhắc đúng chỗ.
- 2 làm: bảng 2·4 chỉ in hai hàng 10, 15 cm; hàng 20, 30 cm để trống; ghi chú bỏ chữ "úp Tập".
- 3 làm: ô 3·3 giữ ba câu sai, lời giải thay bằng "Sai ở đâu?" để điền sau Câu 3, 4, 5.
- 4 làm: nhãn màn thành "Tự kiểm tra · Câu N"; chữ "Bẫy N" chỉ nằm trong khối đáp án (ẩn); bỏ tham chiếu ô 3·3 ở góc màn.
- 5 làm: Câu 5 đổi sang 25 N, 0,30 m (M = 7,5 N·m); phương án và lời giải đổi theo; dòng Thử vô lăng giữ 20 N, 0,36 m.
- 6 làm: hai dòng "Thử" (ván, vô lăng) in nhãn "về nhà"; điểm dừng 1 rút còn 2 phút, điểm dừng 4 có 6 phút (mốc phút trên các màn đổi theo).
- 7 làm: mã ô 4·3 Phân tích đề, 4·4 Giải, 4·5 Điền bước, 5·1 Đề BTVN; màn 6c ghi đường dẫn "thachlab → lớp → bài 21 → Bài tập về nhà".
- 8 làm: dòng "Bạn cùng bàn kiểm" chuyển xuống cuối ô 5·3 (tr.5); để vừa trang, câu 1 Trả bài còn 1 dòng và ô 5·4 dòng 1 còn 1 dòng.
- 9 làm: phương án C câu 1 thành 0,83 N (chia ngược 30/36).
- 10 làm: Câu 6 ghi "(kết quả vừa tìm)"; D thành "Không cần, thanh đã cân bằng sẵn".
- 11 làm một phần: màn búa có dòng "điểm tì O, Minh cách 8 cm, anh Tuấn cách 30 cm"; chưa sửa hình búa trong Tập (không chắc, cần xem hình in).
- 12 làm: thêm màn m2d2 (tam giác OAH, d đối diện α, thử 0,5 m, 40°); ghi chú có câu hỏi "góc nào đối diện d".
- 13 làm: dòng "vì" ô 2·4 chuyển về nhà (màn 6c), màn 3e thêm câu "F2·d2 không đổi nên d2 tăng thì F2 giảm".
- 14 làm: bỏ hint trong ngoặc ở Tập; màn 3c ghi ↻ thuận, ↺ ngược (không vẽ hình mới).
- 15 làm: màn 4a thêm "bất kì = em tự chọn, cho phương trình gọn nhất".
- 16 làm: khung Giải dòng 1 và 3 lên 3 dòng; màn 5b hỏi "Vì sao chọn trục qua O?" trước.
- 17 làm một phần: ghi chú thêm "gấp góc tr.4"; không đổi thứ tự chiếu Câu (gắn với ý từng điểm dừng).
- 18 làm: màn 6bua và ghi chú nhắc tr.1 ô 1·1 đánh dấu mục tiêu.
- 19 làm: mốc chữ 14.4 → 14.6 và 9.0 → 9.2 (chỉ đổi mốc hiện chữ, không đổi điểm dừng; chưa xem lại khung hình vì không có file mp4 trong máy).
- 20 bỏ: thấp, theo chỉ đạo. 21 bỏ: thấp, trang 5 chỉ còn dư 2 mm. 22 bỏ: thấp, giữ hiện trạng.
- Thêm ngoài danh sách: 5 màn (m0, m3e, m4d, m5a, m6bua) tràn khi mở đáp án ở font thật Be Vietnam Pro (có từ trước, m0 và m5a cũng tràn ở bản cũ) → thu cỡ chữ .72–.93 bằng lớp z72…z93 (chỉ màn rộng).
