# 6 bài thi phay CNC — G01, G02, G03 + khoan lỗ sâu 4 mm

Bản vẽ chung (phôi 50 × 50, gốc phôi W ở góc dưới trái, đơn vị mm):

- Biên dạng: hình vuông có 4 góc lượn **R5**, các cạnh nằm ở X, Y = **3** và **47**. Các điểm bắt đầu/kết thúc cung: 8 và 42.
- 4 lỗ **Ø4**: A(25, 38) · B(12, 25) · C(38, 25) · D(25, 12).
- Chiều sâu cắt (cả đường viền lẫn lỗ): **Z-4**. Mặt phôi Z0, lùi an toàn Z5.
- Dao: dao phay ngón **Ø6** (bài 1, 2, 5: đường viền chạy bằng tâm dao, không bù), mũi khoan **Ø4**.
- Quy ước mã theo xưởng Win-NC32: gốc G54, bù bán kính **G41/G42 H11** (ô H11 = 3.000), chu trình khoan G81/G83, G80 huỷ chu trình. Mã chuẩn FANUC dùng **D01** thay H11 — theo ô bù thật trên máy.
- Tốc độ gợi ý: phay S1500 F200, khoan S2000 F60. Z-4 một nhát cho phôi nhôm; thép/phôi cứng → dùng bài 5 (hai lớp).

Điểm chung ở mọi bài: **phay trước, khoan sau**, trừ bài 4 (khoan trước). Hết chương trình: M30.

Các điểm cung (tâm dao đi trên đường biên dạng):

| Góc | Từ | Đến | Tâm cung |
|---|---|---|---|
| Dưới phải | (42, 3) | (47, 8) | (42, 8) |
| Trên phải | (47, 42) | (42, 47) | (42, 42) |
| Trên trái | (8, 47) | (3, 42) | (8, 42) |
| Dưới trái | (3, 8) | (8, 3) | (8, 8) |

---

## Bài 1 — Viền ngược chiều kim đồng hồ (G01 + G03), khoan bằng G81

**Đề:** Phay đường viền R5 sâu 4 mm bằng G01 và G03 (dùng I, J), tâm dao đi trên đường biên dạng, xuất phát tại (8, 3). Sau đó khoan 4 lỗ theo thứ tự A → B → D → C bằng chu trình G81.

```
O0001
G90 G54 G17 G21
T1 M06
S1500 M03
G00 X8 Y3
G00 Z5
G01 Z-4 F100
G01 X42 Y3 F200
G03 X47 Y8 I0 J5
G01 X47 Y42
G03 X42 Y47 I-5 J0
G01 X8 Y47
G03 X3 Y42 I0 J-5
G01 X3 Y8
G03 X8 Y3 I5 J0
G00 Z5
T2 M06
S2000 M03
G81 X25 Y38 Z-4 R2 F60
X12 Y25
X25 Y12
X38 Y25
G80
G00 Z50
M05
M30
```

**Cần chấm:** đúng chiều G03 ở cả 4 góc · I, J đúng dấu · Z-4 · G80 huỷ chu trình.

---

## Bài 2 — Viền cùng chiều kim đồng hồ (G01 + G02), khoan bằng G01

**Đề:** Như bài 1 nhưng đi theo chiều kim đồng hồ (G02), xuất phát (8, 3), và khoan 4 lỗ **không dùng chu trình**: mỗi lỗ gồm G00 tới vị trí → G01 xuống Z-4 → G00 lên Z5. Thứ tự A → C → D → B.

```
O0002
G90 G54 G17 G21
T1 M06
S1500 M03
G00 X8 Y3
G00 Z5
G01 Z-4 F100
G02 X3 Y8 I0 J5 F200
G01 X3 Y42
G02 X8 Y47 I5 J0
G01 X42 Y47
G02 X47 Y42 I0 J-5
G01 X47 Y8
G02 X42 Y3 I-5 J0
G01 X8 Y3
G00 Z5
T2 M06
S2000 M03
G00 X25 Y38
G01 Z-4 F60
G00 Z5
G00 X38 Y25
G01 Z-4 F60
G00 Z5
G00 X25 Y12
G01 Z-4 F60
G00 Z5
G00 X12 Y25
G01 Z-4 F60
G00 Z50
M05
M30
```

**Cần chấm:** G02 đúng tâm cung (I, J đổi dấu so với bài 1) · lùi Z5 giữa các lỗ · không bỏ sót lỗ.

---

## Bài 3 — Phay vách trong biên dạng có bù G41, vào/ra cung tiếp tuyến

**Đề:** Hốc đã khoét thô, phay tinh vách trong theo biên dạng R5, dao Ø6, chạy **ngược chiều kim đồng hồ** (dao nằm bên trái hướng chạy → **G41**). Vào cắt bằng đoạn thẳng G01 tại (8, 3 + bù), ra khỏi biên dạng bằng G40. Khoan 4 lỗ bằng G81 theo đường ngắn nhất A → B → D → C.

```
O0003
G90 G54 G17 G21
T1 M06
S1500 M03
G00 X20 Y20
G00 Z5
G01 Z-4 F100
G41 G01 H11 X8 Y3 F200
G01 X42 Y3
G03 X47 Y8 I0 J5
G01 X47 Y42
G03 X42 Y47 I-5 J0
G01 X8 Y47
G03 X3 Y42 I0 J-5
G01 X3 Y8
G03 X8 Y3 I5 J0
G01 X20 Y3
G40 G01 X20 Y20
G00 Z5
T2 M06
S2000 M03
G81 X25 Y38 Z-4 R2 F60
X12 Y25
X25 Y12
X38 Y25
G80
G00 Z50
M05
M30
```

**Cần chấm:** G41 gọi khi dao còn trong hốc (chưa chạm vách), có đoạn vào ≥ bán kính dao · G40 trước khi nhấc dao · bù 3.000 không nhập sai.

---

## Bài 4 — Khoan trước, viền sau bằng G02 + G42 (cung dùng R)

**Đề:** Khoan 4 lỗ Ø4 sâu 4 mm trước bằng G81 (thứ tự C → A → B → D), rồi phay viền chạy **theo chiều kim đồng hồ** (G02, dao bên phải → **G42**), mọi cung ghi bằng **R** (R5, cung ≤ 180° nên R dương).

```
O0004
G90 G54 G17 G21
T2 M06
S2000 M03
G81 X38 Y25 Z-4 R2 F60
X25 Y38
X12 Y25
X25 Y12
G80
G00 Z5
T1 M06
S1500 M03
G00 X20 Y20
G00 Z5
G01 Z-4 F100
G42 G01 H11 X8 Y3 F200
G02 X3 Y8 R5
G01 X3 Y42
G02 X8 Y47 R5
G01 X42 Y47
G02 X47 Y42 R5
G01 X47 Y8
G02 X42 Y3 R5
G01 X20 Y3
G40 G01 X20 Y20
G00 Z50
M05
M30
```

**Cần chấm:** G42 khớp G02 (cặp G41–G03, G42–G02 cho vách trong) · mọi cung có R5 (không dùng R âm) · thứ tự khoan–phay như đề.

---

## Bài 5 — Hai lớp cắt (Z-2 rồi Z-4), khoan từng nhát G83

**Đề:** Phay viền G03 làm **2 lớp**, mỗi lớp 2 mm (Z-2, sau đó Z-4), tâm dao đi trên biên dạng, xuất phát (3, 8). Khoan 4 lỗ bằng **G83** (khoan từng nhát, mỗi nhát Q2), thứ tự B → A → C → D.

```
O0005
G90 G54 G17 G21
T1 M06
S1500 M03
G00 X3 Y8
G00 Z5
G01 Z-2 F100
G01 X3 Y8 F200
G03 X8 Y3 I5 J0
G01 X42 Y3
G03 X47 Y8 I0 J5
G01 X47 Y42
G03 X42 Y47 I-5 J0
G01 X8 Y47
G03 X3 Y42 I0 J-5
G01 X3 Y8
G01 Z-4 F100
G03 X8 Y3 I5 J0 F200
G01 X42 Y3
G03 X47 Y8 I0 J5
G01 X47 Y42
G03 X42 Y47 I-5 J0
G01 X8 Y47
G03 X3 Y42 I0 J-5
G01 X3 Y8
G00 Z5
T2 M06
S2000 M03
G83 X12 Y25 Z-4 R2 Q2 F60
X25 Y38
X38 Y25
X25 Y12
G80
G00 Z50
M05
M30
```

**Cần chấm:** lớp 1 ăn Z-2, lớp 2 ăn Z-4 (không sai tổng sâu) · lớp 2 lặp đúng đường lớp 1 · Q2 và G80.

---

## Bài 6 — Điểm xuất phát giữa cạnh, viền lập trình tương đối (G91)

**Đề:** Đường viền xuất phát ở giữa cạnh trái (3, 25), đi **ngược chiều kim đồng hồ** (G03), dao ăn Z-4 tại điểm xuất phát. Đoạn viền viết ở chế độ **tương đối G91** (toạ độ là lượng dịch so với điểm hiện tại; I, J luôn tính từ điểm đầu cung nên không đổi). Khoan 4 lỗ ở G90 bằng G81, thứ tự B → D → C → A.

Bảng lượng dịch G91 (kiểm tổng X = 0, tổng Y = 0 để dao về đúng điểm xuất phát):

| Đoạn | Dịch X | Dịch Y |
|---|---|---|
| Xuống cạnh trái | 0 | −17 |
| Cung G03 dưới trái | +5 | −5 |
| Cạnh dưới | +34 | 0 |
| Cung G03 dưới phải | +5 | +5 |
| Cạnh phải | 0 | +34 |
| Cung G03 trên phải | −5 | +5 |
| Cạnh trên | −34 | 0 |
| Cung G03 trên trái | −5 | −5 |
| Cạnh trái (về điểm đầu) | 0 | −17 |

```
O0006
G90 G54 G17 G21
T1 M06
S1500 M03
G00 X3 Y25
G00 Z5
G01 Z-4 F100
G91
G01 Y-17 F200
G03 X5 Y-5 I5 J0
G01 X34
G03 X5 Y5 I0 J5
G01 Y34
G03 X-5 Y5 I-5 J0
G01 X-34
G03 X-5 Y-5 I0 J-5
G01 Y-17
G90
G00 Z5
T2 M06
S2000 M03
G81 X12 Y25 Z-4 R2 F60
X25 Y12
X38 Y25
X25 Y38
G80
G00 Z50
M05
M30
```

**Cần chấm:** G91 bật trước đoạn viền và **G90 trở lại** ngay sau đó (quên G90 → các lỗ chạy lệch) · tổng dịch X, Y về 0 · I, J giữ nguyên (tính từ điểm đầu cung) · điểm xuất phát (3, 25) nằm trên đoạn thẳng.

---

## Thang chấm gợi ý (mỗi bài 10 điểm)

| Mục | Điểm |
|---|---|
| Đầu/cuối chương trình (G90 G54, T, S, M03, M05, M30) | 1 |
| Đường viền đúng biên dạng (toạ độ, chiều cung, I J hoặc R) | 4 |
| Chiều sâu Z-4, lùi an toàn Z5 | 1 |
| 4 lỗ đủ, đúng vị trí, G80 | 2 |
| Mô phỏng WinNC 3D View không báo lỗi/không va chạm | 2 |
