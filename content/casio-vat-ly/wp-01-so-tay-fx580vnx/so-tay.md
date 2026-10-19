# Sổ tay fx-580VN X cho Vật lí (WP-01)

> **Quy ước phím.** `SHIFT x` là phím vàng phía trên phím x; `ALPHA x` là chữ đỏ. Tên chế độ và thứ tự menu đã đối chiếu sách hướng dẫn chính hãng fx-580VN X và thầy đã thử máy thật (19/10/2026; xem `README.md`).
> Phím `x` là phím biến x riêng của máy (không phải `ALPHA )`, phím này cho ra y).
> Phím `STO` là phím riêng, không cần ALPHA.
> **Hằng số:** đề cho giá trị nào thì dùng giá trị đó; hằng số có sẵn trong máy khác SGK ở chữ số thứ 4–6 (xem mục 8).

---

## 1. Chuẩn bị máy (làm đầu mỗi buổi thi và mỗi buổi luyện)

**Dùng khi:** luôn luôn, trước bài đầu tiên.

1. `SHIFT MENU` (SETUP) → **Đơn vị góc**: chọn **Độ** khi đề cho góc bằng độ; chọn **Rad** khi có `ωt`, `π`, `cos(5πt − π/3)`.
2. SETUP → **Dạng hiển thị** (Input/Output). Tên các dạng trên máy:
   - MathI/MathO: hiện phân số, căn.
   - MathI/DecimalO: nhập dạng toán, ra số thập phân ngay.
   - LineI/LineO.
   - LineI/DecimalO.
   - Muốn ra số thập phân thì chọn MathI/DecimalO, hoặc bấm `SHIFT =` (≈) sau khi tính.
3. Số chữ số: SETUP → **Fix / Sci / Norm**. Giữ **Norm** khi tính trung gian; chỉ đặt Fix hoặc Sci khi cần đọc kết quả theo quy tắc làm tròn của thể lệ.
4. Biến nhớ: lưu bằng phím `STO` (phím riêng) rồi phím biến, không cần ALPHA.
   - Máy có 9 biến **A, B, C, D, E, F, x, y, z**, cộng bộ nhớ độc lập M. Không có W, t, f.
   - `x` đang dùng cho SOLVE/TABLE nên đừng dùng làm ô lưu.
   - Gọi biến bằng `ALPHA` + phím biến.
   - Xem giá trị các biến: `SHIFT STO` (RECALL).
5. `Ans` là kết quả lần tính liền trước; `Ans` giữ **đủ chữ số** dù màn hình hiện ít.

**Bẫy**
- Quên đổi Rad ↔ Độ: lỗi số 1 ở dao động và sóng. Nhìn biểu tượng **D** hoặc **R** trên thanh trạng thái trước mỗi bài có hàm lượng giác.
- Tính trung gian rồi gõ lại số đã làm tròn trên màn hình: sai ở chữ số cuối. Luôn dùng `Ans` hoặc biến nhớ.

---

## 2. SOLVE: giải phương trình theo một ẩn

**Dùng khi:** phương trình không giải gọn bằng đại số (hàm lượng giác, mũ, nhiều số hạng). Bài luyện S1–S3.

**Quy trình**
1. Gõ vế trái, bấm `ALPHA CALC` (dấu `=`), gõ vế phải. Ẩn gõ bằng **phím `x`** (hoặc `ALPHA (`); không dùng `ALPHA )` vì phím này cho ra y.
2. Bấm `SHIFT CALC` (SOLVE). SOLVE chỉ dùng được trong phương thức Calculate.
3. Máy hỏi giá trị đầu của x: nhập số **gần nghiệm cần tìm**, bấm `=`, rồi bấm `=` thêm một lần nữa để giải.
4. Đọc nghiệm x. Máy còn hiện **L−R** (hiệu hai vế): L−R gần 0 mới tin nghiệm.

**Cách chọn giá trị đầu**
- Phương trình lượng giác có vô số nghiệm: **mỗi giá trị đầu cho một nghiệm khác nhau**. Muốn nghiệm dương nhỏ nhất thì cho giá trị đầu nhỏ nhưng dương, rồi kiểm lại bằng cách thử nghiệm nhỏ hơn.
- Phương trình có nghiệm vật lí rõ khoảng nào (nhiệt độ cân bằng nằm giữa hai nhiệt độ ban đầu) thì lấy giá trị đầu trong khoảng đó.

**Bẫy**
- SOLVE cho **một** nghiệm rồi dừng. Đề hỏi "lần thứ n" hay "thời điểm đầu tiên" thì phải tự kiểm có nghiệm nhỏ hơn hay không.
- Biến khác x (đã gán A, B…) vẫn giữ giá trị cũ. Xoá hoặc gán lại trước bài mới.

---

## 3. CALC: tính lại cùng một công thức với số liệu khác

**Dùng khi:** một công thức, nhiều bộ số (con lắc ở nhiều chiều dài, công suất ở nhiều giá trị R). Bài luyện C1, C2.

**Quy trình**
1. Gõ công thức, dùng chữ biến thay cho số thay đổi (`ALPHA` + phím biến).
2. Bấm `CALC`. Máy hỏi từng biến, nhập giá trị, bấm `=`.
3. Xong một bộ số, bấm `CALC` lần nữa để nhập bộ khác. Giữ nguyên biến nào không đổi bằng cách bấm `=` khi máy hỏi lại.

**Bẫy**
- Công thức có biến cũ còn nhớ giá trị: máy hiện giá trị cũ làm mặc định. Đọc kỹ rồi mới bấm `=`.
- Gõ `4π²` phải có ngoặc đúng chỗ. Ví dụ `2π√(l/g)`: căn bao cả `l/g`.

---

## 4. TABLE: bảng giá trị hàm f(x)

**Dùng khi:** tìm cực đại/cực tiểu gần đúng, đếm số giá trị nguyên, so sánh hàm trên một khoảng. Bài luyện T1–T3.

**Quy trình**
1. `MENU` → **Bảng giá trị** (Table).
2. Muốn máy không hỏi g(x): vào SETUP → Table → **f(x)** trước (khi đó bảng tối đa 45 dòng). Nhập `f(x)` (x gõ bằng **phím `x`**).
   - Biến khác x trong f(x) được coi là hằng số, nên `ALPHA )` (y) sẽ ra bảng hằng mà máy không báo lỗi.
3. Nhập **Start**, **End**, **Step**, mỗi giá trị kết thúc bằng `=`.
4. Cuộn bằng phím mũi tên để đọc.
5. **Thu hẹp:** thấy cực trị gần X₀ thì chạy lại bảng quanh X₀ với bước nhỏ hơn.

**Bẫy**
- Số hàng bảng bị giới hạn: tối đa 45 dòng với f(x), 30 dòng với f(x),g(x). (End − Start) / Step không được quá lớn. Báo **Range ERROR** thì tăng Step hoặc thu hẹp khoảng.
- Bảng chỉ cho giá trị gần đúng theo bước đã chọn. Đáp số cuối của đề tự luận nên kiểm lại bằng công thức (ví dụ f₀ = 1/(2π√LC)).

---

## 5. Số phức (CMPLX)

**Dùng khi:** tổng hợp dao động điều hoà cùng tần số, mạch RLC nối tiếp, tìm phần tử trong hộp đen. Bài luyện X1–X4.

**Quy trình**
1. `MENU` → **Số phức**. Đơn vị góc phải khớp (Độ hoặc Rad).
2. Nhập số phức theo kiểu **cực**: `A ∠ φ`, với `∠` là `SHIFT ENG` (cùng phím với *i*). Hoặc kiểu đại số `a + b i`, `i` là phím `ENG`.
3. Chọn dạng kết quả, bấm ở cuối biểu thức:
   - `OPTN ▼ 1` (▶r∠θ): xem biên độ và pha.
   - `OPTN ▼ 2` (▶a+bi): xem phần thực, ảo.
   - Có thể đặt dạng mặc định ở SETUP → ▼ → Complex.
4. Lấy riêng từng thành phần:
   - Môđun: `SHIFT (` (Abs).
   - Argument: `OPTN 1` (Arg).
   - Liên hợp: `OPTN 2` (Conjg).
   - Phần thực: `OPTN 3` (ReP).
   - Phần ảo: `OPTN 4` (ImP).

**Ba phép hay dùng**
- Tổng hợp dao động: `A₁∠φ₁ + A₂∠φ₂` → biên độ A, pha ban đầu φ.
- Dòng điện phức: `I = U / Z`, với `Z = R + (Z_L − Z_C) i`. Nhập `U` cực, `Z` đại số.
- Tìm dao động thành phần: `x₂ = x − x₁`.

**Quy ước biên độ:** dùng biên độ thì ra biên độ; dùng giá trị hiệu dụng thì ra hiệu dụng. Đừng trộn.

**Bẫy**
- Góc φ ra Độ hay Rad tuỳ SETUP; ghi đúng đơn vị đề hỏi.
- Máy cho θ trong khoảng (−180°; 180°].
- Phương trình `u = U₀cos(ωt + φ)` ứng với số phức `U₀∠φ`; pha `sin` phải đổi sang `cos` (trừ π/2) trước khi nhập.

---

## 6. Vectơ

**Dùng khi:** tích có hướng (lực từ `F = q v × B`, momen), tích vô hướng (công `A = F·s`, góc giữa hai vectơ). Bài luyện V1, V2.

**Quy trình**
1. `MENU` → **Vectơ**. Chọn VctA, đặt số chiều (2 hoặc 3), nhập các toạ độ. Lặp lại cho VctB.
2. `AC` về màn hình tính. Gọi vectơ bằng `OPTN`:
   - VctA = `OPTN 3`.
   - VctB = `OPTN 4`.
   - VctAns = `OPTN ▼ 1`.
3. **Tích có hướng:** `VctA × VctB`. **Tích vô hướng:** `OPTN ▼ 2` (Dot Product), màn hình hiện dấu "•". **Độ dài:** `Abs(VctA)`, tức `SHIFT (` rồi `OPTN 3` rồi `)`.
4. **Góc giữa hai vectơ**, hai cách:
   - `cos⁻¹( (VctA • VctB) / (Abs(VctA) × Abs(VctB)) )`, đơn vị góc đặt Độ.
   - Ngắn hơn: `Angle(VctA,VctB)` (`OPTN ▼ 3`); dấu phẩy gõ bằng `SHIFT )`.

**Bẫy**
- Thứ tự `v × B` khác `B × v` (đổi dấu).
- Hai vectơ phải cùng số chiều.

---

## 7. Thống kê và hồi quy

**Dùng khi:** trung bình ± độ lệch chuẩn của nhiều lần đo; vẽ đường thẳng qua các điểm đo (T² theo l, U theo I); hồi quy mũ cho phóng xạ. Bài luyện St1–St3.

**Quy trình**
1. `MENU` → **Thống kê**. Chọn kiểu:
   - **1 biến** (trung bình, độ lệch chuẩn),
   - **y=a+bx** (đường thẳng; phím 2),
   - **y=a·e^(bx)** (hàm mũ; ▼ 1). Hệ số ghi chữ thường **a, b**.
2. Nhập dữ liệu vào cột X (và Y). Bấm `AC` thoát bảng.
3. Xem cả bảng kết quả: `OPTN` → 1-Variable Calc / 2-Variable Calc / Regression Calc. Lấy từng giá trị để chèn vào phép tính:
   - `OPTN ▼ 2` (Variable): `n`, `x̄`, `σx` (chia n), `sx` (chia n−1).
   - `OPTN ▼ 4` (Regression): `a`, `b`, `r` (hệ số tương quan).
4. Dự đoán điểm mới: `OPTN ▼ 4` (Regression) → `ŷ`, `x̂`.

**Chọn độ lệch chuẩn nào:** đề Casio thường nêu cách tính sai số. Chưa có thể lệ thì ghi rõ dùng `sx` (n−1) hay `σx` (n).

**Bẫy**
- Quên xoá dữ liệu cũ: nhập bảng mới đè lên bảng cũ, còn dòng thừa. Kiểm `n`.
- Dữ liệu bị xoá khi ra khỏi Statistics, khi đổi giữa 1 biến và 2 biến, hoặc khi đổi cài đặt Statistics (cột Freq). Xoá hết bằng `OPTN 2` (Editor) → Delete All.
- Gõ `ALPHA B` lấy **biến nhớ B** (giá trị cũ), không phải hệ số hồi quy b; máy không báo lỗi. Hệ số b phải chèn bằng `OPTN ▼ 4` → b.
- Hồi quy mũ yêu cầu mọi `y > 0`.

---

## 8. Hằng số và đổi đơn vị

**Dùng khi:** thế hằng số vật lí vào công thức; đổi km/h ↔ m/s, atm ↔ Pa; eV ↔ J thì nhân/chia với e. Bài luyện K1–K3.

**Quy trình**
- Hằng số: `SHIFT 7` (CONST) mở menu **danh mục** (Universal, Electromagnetic, Atomic&Nuclear, Physico-Chem, Adopted Values, Other), rồi chọn số mục. Máy chèn giá trị đủ chữ số.
  - h = `SHIFT 7 1 1`.
  - c₀ = `SHIFT 7 1 3`.
  - e = `SHIFT 7 2 3`.
- Đổi đơn vị: `SHIFT 8` (CONV), chọn cặp đơn vị có trong bảng (có km/h ↔ m/s ở Velocity, atm ↔ Pa ở Pressure; **không có** eV ↔ J: dùng e đề cho hoặc `SHIFT 7 2 3`).
- Tiền tố SI khi **nhập** (k, m, μ, n, p): `OPTN` → Engineer Symbol, hoặc gõ ×10^x. Phím `ENG` chỉ đổi cách **hiển thị** kết quả.
- Gõ luỹ thừa 10 bằng phím `×10^x`, đừng gõ "E".

**Quy tắc chọn giá trị**
- Đề **cho số** (h = 6,625.10⁻³⁴ J.s…) thì dùng số đề cho, **không** gọi hằng số có sẵn, vì hai kết quả có thể khác ở chữ số có nghĩa thứ 4–5.
- Đề **không cho** thì dùng hằng số trong máy và ghi giá trị đã dùng.

**Bẫy**
- Đổi sai khối (cm³ → m³ nhân 10⁻⁶, không phải 10⁻³).
- Khối lượng hạt nhân: đề cho theo u thì nhân 931,5 MeV/c² (hoặc giá trị đề cho), đừng đổi ra kg rồi nhân c² nếu không cần.

---

## Bảng tra nhanh: chọn công cụ nào?

| Tình huống | Công cụ |
|---|---|
| Tìm t, x, l… trong phương trình có sin/cos/mũ | SOLVE |
| Một công thức, nhiều bộ số | CALC |
| Cực trị gần đúng, đếm giá trị nguyên | TABLE |
| Tổng hợp dao động, mạch RLC, hộp đen | Số phức |
| Lực từ, công, góc giữa vectơ | Vectơ |
| Nhiều lần đo, đường thẳng, phóng xạ thực nghiệm | Thống kê |
| Thế hằng số, đổi đơn vị | CONST / CONV |
