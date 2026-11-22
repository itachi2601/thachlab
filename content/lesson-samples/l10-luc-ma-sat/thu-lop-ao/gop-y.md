# Góp ý sau chạy thử lớp ảo — Bài 18 Lực ma sát

File gọi tắt: **src** = tren-lop.src.html · **ghi chú** = tren-lop-ghi-chu.html · **.mjs** = scripts/ruot-tap/l10-bai18.mjs. Bằng chứng trích hs-1, hs-2, hs-3 và sach-hs; mục chỉ từ phần soát tài liệu của thầy (chưa có học sinh trải nghiệm) ghi rõ "soát".

## A. Ưu tiên CAO

| # | File · vị trí | Vấn đề (bằng chứng) | Sửa thành |
|---|---|---|---|
| 1 | src · màn 2b (clip kéo hộp), bảng dừng cuối | hs-1: "Màn 2b chiếu 'Đáp án C' ngay trong clip, còn màn 1b nói đáp án để cuối tiết"; hs-3: "màn lộ đáp án trước làm em mất ý nghĩ" | Dòng "Đáp án C: …" nằm trong `.an[hidden]`, chỉ hiện khi Enter sau khi lớp đã giơ tay; bảng "Còn yên / Bật đi 0,7 N / Trượt đều 0,6 N" hiện trước, chữ "Đáp án C" sau |
| 2 | src · màn 3b (clip trượt hay lăn), bảng sau lần 2–3 | hs-2: "dòng 'Câu 1: C' hiện chung màn với kết quả lần 2–3, em thấy đáp án trước khi hết giờ nghĩ" | Tách: bảng "Dựng đứng 1,2 N · nhanh hơn 1,2 N" hiện ở bước lần 2–3; "Câu 1: C" thành bước riêng sau Dừng ① và phải bấm Enter mới hiện |
| 3 | .mjs · ô 4·2 (tiêu đề) + ghi chú · mục "Tập chưa có ô ghi điểm đề 1239" | hs-3: "Đề 1239: em biết ghi '…/20' vì thầy nói; Tập không in ô, nếu không nghe em không biết. Ô 4·2 đã chật." | Đổi tiêu đề ô 4·2: "Kết quả tự kiểm tra (Câu 1–6) · Đề 1239: ……/20 · câu sai ……" (đổi chữ tiêu đề, giữ số trang); ghi chú bỏ câu "ghi vào lề dưới ô 4·2", đổi thành "ghi vào dòng tiêu đề ô 4·2" |
| 4 | src · màn "Về nhà" · dòng tr.4 | hs-3: "ô 4·2 Câu 4, 6 'bài lý thuyết trên web' em không rõ làm ở đâu (đề 1239 hay bài web khác?)" | Đổi thành: "tr.4 ô 4·2 Câu 4, 6: vào thachlab → Bài 18 → mục Lý thuyết → Tự kiểm tra ngay, làm Câu 4 và Câu 6 (Câu 1, 2, 3, 5 đã làm trên lớp)"; ghi chú cùng chỗ |
| 5 | src · màn 5c (Giải), bước $Ox$ | hs-3: "em chép 'sinα = 0,5; cos30° ≈ 0,87' từ màn chứ tự không biết"; "m triệt tiêu thầy nói em mới hiểu" | Sau dòng $a=g(\sin\alpha-\mu\cos\alpha)$ thêm dòng ở bước mở: "Thay số: $\sin30^\circ=0{,}5$; $\cos30^\circ\approx0{,}87$; $a=9{,}8(0{,}5-0{,}20\cdot0{,}87)\approx3{,}2$" và dòng "$m$ có ở cả hai vế → triệt tiêu" |
| 6 | src · màn 5b, cột 2 "Dữ liệu → kiến thức" | hs-3: "chỗ trống 63–66 em chỉ đoán được vì câu hỏi bảng 'Dữ liệu → kiến thức' khó hiểu; 1 phút đủ cho 1–2 ô"; "ô 66 v²=2as em chưa học công thức này" | Đổi tiêu đề cột thành "Viết ra: con số hoặc công thức"; dòng mẫu đã in thêm "→ $v_0=0$" làm ví dụ; mở thêm "$v^2=2as$ (công thức không có thời gian, chương Động học)"; ghi chú ĐD5 cho 2 phút phân tích, bù bằng 30 giây cắt từ Câu 5 |
| 7 | src · màn 2e, 4b, 5a (nhãn đầu màn "Bẫy 1/2/3") + ghi chú · mục "Bốn câu 1,2,3,5" | soát: nhãn "Bẫy" hiện trước khi biểu quyết; hs-2: Câu 2 em chọn D "chắc, vì màn 4a vừa mở" — đáp án đã ngay trước mặt | Đổi nhãn thành "Câu 3 · 30 giây" (bỏ chữ Bẫy); chữ "Bẫy n" hiện ở bước mở đáp án ("Đây là bẫy 1: …"); ở ghi chú bỏ dặn "đánh dấu bẫy trước" |
| 8 | ghi chú · mục điểm dừng, thứ tự lật Tập | hs-2: "ô Câu 1 nằm tr.4, phải lật từ tr.2 ra tr.4 rồi quay lại, tốn thời gian, 3c đã chiếu mất"; hs-1: lật 3 lần trong ĐD2 | Cho ghi lựa chọn Câu 1, 2, 3, 5 (chữ cái) vào lề trang đang mở, rồi chép cả bốn sang ô 4·2 trong 30 giây sau màn 5a; ghi chú sửa "lật 9–10 lần" thành "lật 4 lần" |

## B. Ưu tiên VỪA

| # | File · vị trí | Vấn đề (bằng chứng) | Sửa thành |
|---|---|---|---|
| 9 | src · màn 2c đồ thị + màn 2b | hs-1: "thầy nói đồ thị trong clip là F theo thời gian, đồ thị này là ma sát theo lực kéo, em hơi rối hai đồ thị" | Mỗi đồ thị có chú thích chữ lớn một dòng: màn 2b "Trục ngang: thời gian"; màn 2c "Trục ngang: lực kéo"; ghi chú bỏ câu nói miệng |
| 10 | src · màn 2c, bước mở; src · màn 3c/4b/5a mở đáp án | hs-1: em bỏ trống ☐ tăng/☐ không đổi (BC) và ☐ Đúng Câu 3; hs-2: ☐ Đúng Câu 2 bỏ trống; hs-3: Câu 5 ☐ Đúng bỏ trống | Cuối mỗi bước mở đáp án thêm dòng nhỏ "✔ Tích 'Đúng' (ô 4·2) / tích 'không đổi' (ô 1·4)" |
| 11 | .mjs · ô 2·2 dòng Rút ra; src · màn 3c | hs-2: "ô 22 ghi 'ma sát trượt [__] theo diện tích, tốc độ': em điền 'không đổi' nhưng không chắc có phải 'không phụ thuộc'" | .mjs: "ma sát trượt [__] khi đổi diện tích, đổi tốc độ; ma sát lăn [__] ma sát trượt rất nhiều" (giữ số trang); src màn 3c dùng "không đổi" ở cả hai chỗ |
| 12 | ghi chú · ĐD3 màn 3d; src · màn 3d | hs-2: "thầy cho 20 giây, em chỉ tính kịp hàng 1; 3 hàng còn lại chép sau khi màn mở" | Ghi chú: cho dùng máy tính điện thoại, 40 giây; hàng 1 thầy làm mẫu trên màn, ba dãy mỗi dãy một hàng; mốc ĐD3 vẫn 7 phút bằng cách đưa dòng "Rút ra" cho chép trong lúc clip dừng |
| 13 | src · màn 4a (Áp lực N) | hs-2: "em đoán 'nhỏ hơn mg' trước khi mở nhờ hình, nhưng không hiểu vì sao có sinα (chưa học phân tích lực chếch)" | Trước nút mở thêm dòng "$F$ có thành phần thẳng đứng $F\sin\alpha$ kéo vật lên → vật đè sàn nhẹ hơn" cạnh hình kéo chếch |
| 14 | src · màn 4c · bước mở + ghi chú | hs-2: "'α≈20°' và '0,36' em không tự kiểm được, vì không có máy tính bấm tan"; hs-2: chép | Mở thêm bước tính: "$\sin\alpha=0{,}34$ → $\cos\alpha=\sqrt{1-0{,}34^2}\approx0{,}94$ → $\mu_n=\tan\alpha=0{,}34/0{,}94\approx0{,}36$"; ghi chú: cho bấm máy 20 giây |
| 15 | .mjs · ô 2·3 dòng "kém tin cậy nhất" | hs-3: "ô 2·3 'sai số tương đối 0,05 N : lực đọc được' chưa hiểu cách tính" | "Lần đo kém tin cậy nhất: lần [__] (tỉ số 0,05 N chia cho lực trượt đọc được là lớn nhất), vì" (giữ số trang) |
| 16 | .mjs · ô 5·3 | hs-3: "em không biết ô 5·3 'câu đổi chiều' cần dùng công thức nào" | Đầu ô thêm gợi ý một dòng nhỏ "gợi ý: từ $v$, $s$ tìm $a$ → lực → $\mu$" (thay bớt một dòng kẻ trong 5 dòng, giữ số trang) |
| 17 | ghi chú · ĐD6 trả bài + src màn Trả bài | hs-3: "câu 1 mất hơn 1 phút vì 3 ý"; chỉ 1,5 phút chung hai câu | Cho 2 phút; hoặc đổi câu 1 chỉ chấm "khi nào + chiều" (độ lớn mở bằng nút riêng) |
| 18 | src · màn 3a dòng cuối; .mjs ô 2·1 dòng 2 | hs-2: "'(N)' sau [18] làm em phân vân điền 'áp lực' hay 'áp lực (N)'" | .mjs: "$N$: [__], đơn vị niutơn (viết N)" thay cho "$N$: [__] (N)"; src bỏ dòng chú thích N nghiêng/đứng |

## C. Thấp

| # | File · vị trí | Vấn đề (bằng chứng) | Sửa thành |
|---|---|---|---|
| 19 | .mjs · ô 3·1 | soát: "so với bảng ở Tập 62·3" lẫn số trang quyển | Đổi "62·3" thành "ô 2·3" |
| 20 | ghi chú · ĐD2 màn 2a | hs-3: "chán nhất: đoạn chép từng dòng ở ĐD2 vì đọc chữ xanh rồi chép" | Trước khi mở mỗi dòng hỏi lớp "ma sát nghỉ hướng nào?" (đoán miệng 10 giây), rồi mở chữ xanh |
| 21 | .mjs · ô 1·4 đồ thị ☐ tăng / ☐ không đổi | hs-1: em bỏ trống chỗ này, ô nằm giữa câu | Đưa ☐ xuống đầu dòng riêng "BC: ☐ tăng ☐ không đổi" rồi "nhỏ hơn ở A khoảng [__] N" ở dòng sau (giữ số trang nếu còn chỗ) |
| 22 | src · màn 6/6 "Quay lại thùng nước" | soát: ô 1·3 + ô 1·1 + hai lớp "Mở" trong 1 phút; hs-3: đủ giờ | Giữ nguyên; không sửa |
| 23 | ghi chú · mục "Nếu thiếu giờ" | soát: ĐD3 18 chỗ + clip trong 7 phút; hs-3: "dồn nhất ĐD2 và ĐD3" | Thêm: "Thiếu giờ ở ĐD3 thì để ô 2·2 dòng Rút ra về nhà" |

## Đã xử lý (2026-11-22)

- 1 làm: m2b bước cuối hiện bảng trước, "Đáp án C" nằm trong ô ẩn; JS: ở màn clip, Enter/Phát mở ô đáp án còn đóng của bước đang hiện trước khi phát tiếp.
- 2 làm: m3b tách thành dừng 19,4 (bảng ba số $1{,}2$ N + nút "Mở: đáp án Câu 1") và dừng 19,6 (câu lăn); "Lăn: D" ở bước cuối cũng ẩn sau nút. Đã ghi "4 điểm dừng".
- 3 làm: .mjs đổi tiêu đề ô 4·2 thành "Tự kiểm tra Câu 1–6 · Đề 1239: ……/20 · sai câu ………"; ghi chú + màn QR trỏ về dòng tiêu đề này.
- 4 làm: màn Về nhà + ghi chú ghi đường đi thachlab → Bài 18 → Lý thuyết → Tự kiểm tra ngay.
- 5 làm: m5c thêm "$m$ có ở cả hai vế, triệt tiêu" và dòng thay số $\sin30^\circ$, $\cos30^\circ$.
- 6 làm: cột đổi tên "Viết ra: con số hoặc công thức" (cả .mjs và màn); dòng $v^2=2as$ ghi "(không có $t$)". Đây là công thức Động học HS đã học, không coi là kiến thức mới. Ghi chú: phân tích đề 2 phút, bù 30 giây từ Câu 5. Dòng mẫu $v_0=0$ vốn đã in.
- 7 làm: nhãn đầu màn thành "Câu 3/2/5 · 30 giây"; chữ "Đây là bẫy n" chỉ hiện khi mở đáp án; ghi chú bỏ dặn đánh dấu bẫy trước.
- 8 làm: câu biểu quyết ghi chữ cái ra lề, sau màn 5a chép cả bốn vào ô 4·2 (dòng nhắc trên màn 5a); ghi chú "lật 4 lần".
- 9 làm: m2b dòng "trục ngang: thời gian", m2c dòng "Trục ngang: lực kéo".
- 10 làm: dòng ✔ nhắc tích ở d2 (ô 1·4), Câu 3, Câu 2, Câu 1; Câu 5 gộp vào dòng nhắc chép ở 5a.
- 11 làm: .mjs "ma sát trượt ___ khi đổi diện tích, đổi tốc độ"; màn 3c dùng đúng câu đó.
- 12 làm: m3d hàng 1 hiện sẵn làm mẫu, dòng "máy tính điện thoại · 40 giây · mỗi dãy một hàng"; ghi chú bù giờ bằng cách chép "Rút ra" lúc clip dừng.
- 13 làm: m4a thêm dòng $F\sin\alpha$ kéo vật lên → đè sàn nhẹ hơn.
- 14 làm: m4c mở đủ bước $\sin\to\cos=\sqrt{1-\sin^2}\to\tan$ cho cả $0{,}36$ và $0{,}30$; ghi chú bấm máy 20 giây.
- 15 làm: .mjs "lần ___ (tỉ số 0,05 N : lực trượt đọc được lớn nhất), vì". Chữ ngắn hơn đề xuất vì dòng đầy.
- 16 làm: .mjs ô 5·3 thêm dòng gợi ý, bớt một dòng kẻ (5 → 4).
- 17 làm: Trả bài viết 2 phút (màn + ghi chú).
- 18 làm: .mjs "N: ___, đơn vị N". Chữ "niutơn" làm tr.2 tràn 4 mm nên bỏ, đồng thời thu hẹp hai chỗ trống. Màn 3a bỏ dòng chú thích nghiêng/đứng.
- 19 làm: .mjs "so với bảng ở ô 2·3".
- 20 làm: ghi chú ĐD2, đoán miệng 10 giây trước khi mở mỗi dòng.
- 21 làm: .mjs tách "BC: ☐ tăng ☐ không đổi" thành dòng riêng.
- 22 bỏ: góp ý tự ghi "giữ nguyên".
- 23 làm: ghi chú thêm "Thiếu giờ ở điểm dừng 3: để dòng Rút ra ô 2·2 về nhà".
- Thêm (phiên chính giao): .mjs gắn mã ô 5·1 cho "Đề BTVN" (`K.tag('5·1')`, không sửa khung.mjs); màn Về nhà ghi "ô 5·1".
- Kiểm: PDF Tập 12 trang trước và sau, không trang nào tràn (tr.2 dư 1 mm, tr.4 dư 1 mm), katexErr 0. Bản chiếu: 1280×720 và 1920×1080 không tràn ở mọi bước clip và mọi ô mở; 375px không cuộn ngang; katex-error 0.
