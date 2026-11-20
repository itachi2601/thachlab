# Góp ý sau buổi chạy thử bài 20 Điện thế (học sinh ảo, 7 lượt)

Ba file nói tới: **src** = `content/lesson-samples/l11-dien-the/tren-lop.src.html` · **ghi chú** = `tren-lop-ghi-chu.html` · **.mjs** = `scripts/ruot-tap/l11-bai20.mjs`.
Số ô [n] là số chỗ trống trong `thu-lop-ao/sach-trong.md`. Bằng chứng trích từ `hs-N.md` và `sach-hs.md`.

**Kết quả chung:** học sinh ảo điền đúng gần hết các ô làm trên lớp: 66/66 ô, riêng [98] thiếu một ý. Biểu quyết đúng 5/5 câu (lần 3, dời ngang, Câu 5, c), Câu 1 chim sửa được ở cuối giờ). Vì vậy các góp ý dưới đây chủ yếu dựa vào **chỗ học sinh nói là mơ hồ, phải đoán** và **chỗ tài liệu lệch nhau**, không dựa vào tỉ lệ sai.

---

## A. Ưu tiên CAO

| # | File · vị trí | Vấn đề (bằng chứng) | Sửa thành |
|---|---|---|---|
| 1 | **.mjs** p4 ô 4·3 (`h3(3,'Kết quả tự kiểm tra (8 câu trên web)','4·3')` + `rkHai([1,2,3,4],[5,6,7,8])`) | Tập có bảng 8 câu, nhưng cuối tiết làm đề 1215 có 20 câu. Màn "Về nhà" vẫn giao "ô 4·3". hs-7 câu 2: "em không biết 8 câu nào". | Đổi tiêu đề thành "Đề 1215 (20 câu, cuối tiết)". Thay `rkHai` bằng 1 dòng: "Điểm: …/20 · Câu sai: ____ · Câu đoán mò: ____". Hoặc bảng 20 ô nhỏ (Câu · Em chọn). Bỏ "ô 4·3" khỏi màn Về nhà (src `#m-ve-nha`/màn cuối), vì đề đã làm trên lớp. |
| 2 | **.mjs** p4 `K.btvn()` (mục "4 · Đề BTVN") + **src** màn cuối "Về nhà" | Mục không có mã ô, màn Về nhà không nhắc tới. hs-7: "không biết làm khi nào". | Gán mã **4·4** (`h3(4,'Đề BTVN','4·4')` hoặc tham số cho `btvn`). Thêm vào màn Về nhà dòng "tr.4 ô 4·4: ghi đề BTVN thầy giao trên web". Nếu bài 20 không có BTVN riêng thì bỏ mục này khỏi p4. |
| 3 | **src** màn 1b (phương án C, D) + **.mjs** p1 ô 1·2 `opt('C',…)`, `opt('D',…)` | Câu dự đoán dùng "điện thế", "hiệu điện thế" trước khi học. Học sinh bỏ qua C vì không hiểu chữ, không phải vì lập luận (hs-1: "chưa học điện thế nên… đành bỏ qua"). D tự loại được ngay bằng 220 V < 500 kV. | C: "Hai chân chạm hai chỗ trên **cùng một dây**, giữa hai chân hầu như không có chênh lệch điện". D thay bằng nhiễu mạnh hơn, ví dụ "Chim nhẹ nên dòng điện qua chim rất nhỏ". Giữ chữ "điện thế" cho ô 1·3 lúc sửa. |
| 4 | **src** màn 1b ↔ **.mjs** p1 ô 1·2 | Màn rút gọn A, B, D, khác chữ trong Tập. hs-1: "không biết giơ tay theo bản nào". hs-7 nhắc lại. | Chép **y nguyên** chữ của Tập lên màn (chữ 5,2vh vẫn vừa 4 dòng), hoặc rút gọn cả trong Tập cho trùng. |
| 5 | **src** ĐD6: thêm màn sau `#m6a`, trước `#m6b` + **ghi chú** ĐD6 | Ở ô 1·3, ghi chú chỉ nói "ghi đáp án C". Lời giải con chim nằm ở ô mở của màn 1b ("A: chạm cùng lúc dây và cột là chết…") và không được chiếu lại. Hậu quả: [4] học sinh viết "chim không chạm đất **nên không có hiệu điện thế**" — sai khái niệm, mà lớp không có gì để đối chiếu. | Thêm màn "6/6 · Quay lại con chim": hình chim + hình vôn kế lần 3, đặt cạnh nhau. Ô mở 1: "C. Hai chân = hai que trên cùng dây → U ≈ 0". Ô mở 2: "Người đứng đất: dây 500 kV – đất 0 V → U = 500 kV". Ghi chú ĐD6: "chiếu màn này, hỏi 'chim chạm cả dây lẫn cột thì sao?'". Bỏ chữ "(C)" ở nhãn `#m6b` ("ô 1·3: ghi đáp án con chim (C)"). |
| 6 | **src** `#m4e` (Bẫy · Câu 5) | Trên màn không có hình, không có "N lệch theo chiều đường sức", và ghi "lệch" trong khi Tập ghi "hợp". hs-5 và hs-7: "cos hay sin, 'lệch đường sức' mơ hồ". Ô [74] ("chỉ đúng khi MN nằm …") không màn nào có chữ để đối chiếu. | Đưa hình `hinhChieu` (ô 4·1) lên màn, có tô cạnh kề $d$. Đề: "$MN=5$ cm **hợp với** đường sức $60^\circ$, N lệch theo chiều đường sức". Ô mở thêm dòng: "$U=E\cdot MN$ chỉ đúng khi MN **dọc đường sức**; $\alpha$ đo giữa MN và đường sức → dùng $\cos$". |
| 7 | **Thời lượng** ĐD4 (ghi chú bảng phút + src `#m4a`–`#m4e`) | 5 câu đoán nối nhau, 2 thí nghiệm, 9 ô trong 8 phút (16–24). Lượt chạy thử phải chia ĐD4 làm 2 lượt. hs-7: "dồn nhiều nhất là điểm dừng 2 và 4". | Mặc định **bỏ** clip `#m4b` dừng ③ (bảng 4 số đã in trong Tập ô 3·3) và gộp câu "x gấp đôi" vào `#m4c`. Giữ `#m4b` cho lớp không có PhET. Ghi chú: ĐD4 = 16–25, ĐD5 = 25–28, trả bài 28–30. |

## B. Ưu tiên VỪA

| # | File · vị trí | Vấn đề (bằng chứng) | Sửa thành |
|---|---|---|---|
| 8 | **src** `#m2a` + **ghi chú** ĐD2 | $A_{MN}=qEd$ có $d$ nhưng không nói $d$ là gì; ô 1·4 dòng 3 bị để về nhà. hs-2: "điền qEd nhưng không chắc d đo thế nào". | Thêm dòng trên màn: "$d$: hình chiếu của MN lên đường sức (có dấu)". Đưa ô 1·4 dòng 3 ([9]–[11]) vào phần điền trên lớp: +3 ô, nhưng ĐD4 đỡ phải giải thích lại. |
| 9 | **src** `#m2b` | "Vô cực" chỉ có ký hiệu $A_{M\infty}$, thầy nói miệng. hs-2: "mơ hồ ra xa vô cùng là bao xa". | Thêm sau công thức: "($A_{M\infty}$: công đưa $q$ từ M ra **vô cực** — xa tới mức không còn lực)". |
| 10 | **src** `#m2c` (ô mở kết quả) | Chỉ có kết quả sim, không có lí do. hs-2: "chưa biết vì sao Q dương cho V dương". Từ "Mặt đẳng thế" dễ hiểu nhầm là khái niệm mặt đẳng thế. | Thêm dòng: "$Q>0$ đẩy $q>0$ ra xa → $A_{M\infty}>0$ → $V>0$". Đổi chữ: "đầu đo (trong sim tên là 'Mặt đẳng thế')". |
| 11 | **src** `#m2d` | "Theo chiều đường sức, điện thế giảm" chỉ nói một chiều. hs-4: "đi ngược mà tăng, khá rối". | Thêm: "Đường sức đi từ $V$ cao xuống $V$ thấp (như nước chảy xuống)". |
| 12 | **src** `#m3b` (ô mở rút ra) + phương án D | Thiếu ý mấu chốt "mọi điểm trên dây không có dòng cùng điện thế". D mơ hồ. hs-3: "không biết điện thế dây giống cực (+) không"; "'xa nhau' là xa gì". | Ô mở thêm: "Dây nối cực (+), không có dòng: mọi điểm trên dây cùng $V$ với cực (+)". D: "hai que càng xa nhau trên dây, số càng lớn". |
| 13 | **src** `#m4a` | Chỉ có chữ "dọc/ngang đường sức", không có hình. hs-4: "không biết ngang là hướng nào". | Thêm SVG nhỏ: mũi tên E nằm ngang, mũi tên "dọc" trùng E, mũi tên "ngang" vuông góc E. |
| 14 | **src** `#m4b` (bước data-t 10.8) | Không nói que đen = mốc thì số chỉ = điện thế que đỏ. hs-4: "chưa hiểu vì sao máy không đo được điện thế một điểm". | Bước "Que đen ở lá âm: mốc 0 V" thêm: "→ số chỉ = điện thế tại que đỏ". |
| 15 | **src** `#m4c` (ô mở) | Đơn vị V/m chưa xuất hiện mà đã hỏi "độ dốc là gì". hs-5: "em chỉ biết N/C". | Ô mở thêm "1 V/m = 1 N/C". |
| 16 | **src** `#m4d` ↔ **ghi chú** ĐD4 | Câu gợi mở "ô 2·3 có công thức công nào?" thừa, vì màn đã in sẵn hai công thức. hs-5: "phải quay lại ô 2·3, lúng túng". | Cho dòng $A_{MN}=qEd\quad A_{MN}=qU_{MN}$ hiện từng vế bằng Enter **sau khi** lớp tự nêu, hoặc bỏ câu gợi mở trong ghi chú. |
| 17 | **src** `#m5c` + **.mjs** p5 ô 5·1 bảng đọc đề | Thứ tự trừ của $U_{\text{đầu–cuối}}$ không có trên màn. Ô "mốc ở bản âm" chỉ một dòng hẹp nên học sinh thiếu $V_+$. hs-6: [98] chỉ ghi $V_-=0$; "phải đoán thứ tự trừ". | `#m5c` thêm dòng "$U=V_{\text{đầu}}-V_{\text{cuối}}$, electron $q=-e$". Đây cũng là ô [38], [39] (ô 2·3 dòng 5–6) đang để về nhà mà ĐD5 lại cần (hs-7: "ô 38, 39 chưa được dạy rõ"). .mjs: dòng "mốc ở bản âm" in sẵn khung "$V_-=$ ……, $V_+=$ ……". |
| 18 | **.mjs** p3 ô 3·3 + **src** `#m4b`, `#m4c` (nhãn "về nhà") | Ô 3·3 giao về nhà, nhưng mọi kết quả (60 V/m, "đều", "không đổi") đã mở trên lớp, nên về nhà chỉ còn chép. | Cho điền [62]–[69] ngay sau `#m4c` (30 giây), hoặc đổi số liệu ô 3·3 trong Tập (ví dụ nguồn 9 V) để bài về nhà là bài mới. |
| 19 | **src** ĐD2 `#m2a`–`#m2d` + **ghi chú** ĐD2 | 23 ô chép một lúc, không rõ chữ nào là chỗ trống. hs-2: "phải tự chọn từ"; hs-7: "chép nhiều ô một lúc, không rõ thứ tự". | Trên màn, gạch chân hoặc tô màu đúng các chữ ứng với ô trống trong Tập. Góc màn ghi "ô 2·1 dòng 1–4". |

## C. Ưu tiên THẤP

| # | File · vị trí | Vấn đề | Sửa thành |
|---|---|---|---|
| 20 | **.mjs** p2–p4 + **src** `#m4e` + **ghi chú** ĐD4 | Có Câu 1, 2, 3, 5 nhưng không có Câu 4 (phát hiện khi soát, học sinh không nêu). | Đổi "Câu 5" thành "Câu 4" ở cả ba nơi. |
| 21 | **src** `#m3a`, `#m3b`, `#m3c` | Số ghi lẫn 1,50 V và 1,5 V. hs-3: "không biết ghi 1,5 hay 1,50". | Thống nhất 1,50 V; −1,50 V; 0,00 V. |
| 22 | **src** `#m1b` | Nút "Mở đáp án" nằm trong chuỗi Enter, bấm nhầm ở phút 2 là lộ đáp án (phát hiện khi soát). | Bỏ ô mở ở 1b, chuyển sang màn "Quay lại con chim" (mục 5). |
| 23 | **ghi chú** ĐD6 | Mục tiêu 1·1 có ô ☐ nhưng không có lúc nào cho đánh dấu. hs-1: "chưa đánh dấu ô nào". | Thêm "20 giây: đánh dấu ô 1·1" sau ô 1·3. |
| 24 | **ghi chú** ĐD5 | "b) tự làm 30 giây": phải tính E rồi nhân, đổi cm. hs-6 (học sinh ảo tự báo, bằng chứng yếu). | 45–60 giây. Đáp lại bằng cách bỏ biểu quyết c) nếu thiếu giờ, như ghi chú đã có. |
| 25 | **.mjs** p5 ô 5·1 bảng đọc đề | Không nói viết dài ngắn thế nào; học sinh viết cả lời giải vào ô. | Thêm gợi ý nhỏ "(một dòng: dữ liệu → điều suy ra)" dưới tiêu đề cột. |

## D. Thời lượng (ước tính, chưa đo được)

- ĐD2 (23 ô + PhET) và ĐD4 (5 câu đoán) là hai chỗ dễ vượt giờ. Mục 7, 8 và 19 giúp giảm tải. Riêng mục 8 thêm 3 ô cho ĐD2 nhưng bớt phần giải thích lại ở ĐD4.
- Nếu làm mục 5 (màn quay lại con chim, khoảng 1 phút) thì cần lấy bớt chỗ khác: bỏ clip `#m4b` dừng ③ (mục 7).

## E. Lỗi do tài liệu và lỗi do cách chạy thử / học sinh ảo

- **Lỗi tài liệu** (đã sửa được thì nên sửa): mục 1–6, 8–21. Bằng chứng là câu hỏi cụ thể của học sinh ở đúng ô đó, hoặc chỗ ba file lệch nhau.
- **Lỗi của người chạy thử (thầy ảo)**: lượt 5 dặn "chưa điền", nên các ô 3·2 và 4·1 bị trễ một lượt. Ô "Rút ra" 3·1 cũng bị dời một lượt. Đây không phải lỗi tài liệu.
- **Giới hạn của học sinh ảo**:
  - Học sinh không xem clip hay PhET, chỉ nghe mô tả. Vì vậy "bàn cuối không thấy que chạm đâu" (hs-3) và "30 giây gấp" (hs-6) là bằng chứng yếu; cần thử ở lớp thật.
  - Học sinh ảo đúng gần như mọi câu, nên các lỗi hay gặp mà ghi chú lường trước (dùng sin, ra 90 V, −120 eV, chọn A ở lần 3) **chưa được kiểm**.
  - Không đo được phút thật.
- **Không thử**: đề 1215 trên web, mã QR, cỡ chữ ở bàn cuối, nhiễu 0,01 V của đồng hồ.
