# Kiểm chuỗi phím fx-580VN X (WP-01, WP-03..06): đối chiếu nguồn, không bấm máy thật

Ngày kiểm: 19/10/2026. Phạm vi: `so-tay.md`, `ky-thuat.md`, `bai-luyen.md`, `mini-test.md` của 5 gói.
Không có máy thật, không dùng được trình giả lập: bản giả lập fx-580VN X chính hãng là phần mềm Windows (không chạy được trong phiên này). Cũng không có giả lập web chính thức. Thay vào đó, các mục được đối chiếu với nguồn bên dưới.

## Nguồn

| Mã | Nguồn | Ghi chú |
|---|---|---|
| **M** | Sách hướng dẫn **chính hãng** fx-580VN X (tiếng Việt, HTML) của Casio: https://support.casio.com/global/vi/fx/manual/fx-580VNX_VI/ | Nguồn chính. Phím trên trang là ảnh, mỗi ảnh có mã số. Bảng mã do người kiểm tự giải, đối chiếu với trang chú giải phím (`before_using_calculator/getting_started/markings.html`) và các ví dụ: 57398 = SHIFT, 57388 = ALPHA, 57419 = MENU, 57420 = OPTN, 57421 = **STO**, 57390 = CALC, 57383 = ENG (thành *i* trong Complex), 57364 = `(`, 57365 = `)`, 57431 = phím **x**, 57344 = AC, 57356 = 7, 57357 = 8. |
| M/var | `basic_calculations/memory_functions/variables.html` | biến, STO, RECALL |
| M/solve | `function_calculations/using_solve/` | SOLVE |
| M/calc | `function_calculations/using_calc/` | CALC |
| M/table | `using_calculation_modes/creating_number/` | TABLE |
| M/err | `technical_informatoin/errors/error_messages.html` | thông báo lỗi |
| M/setup | `calculation_calculator/configuring_calculator/available.html` | SETUP |
| M/cplx | `using_calculation_modes/complex_number/` | số phức |
| M/vct | `using_calculation_modes/vector_calculations/items.html`, `examples.html` | vectơ |
| M/stat | `using_calculation_modes/statistical_calculations/` (các trang `using.html`, `inputting.html`, `linear.html`, `single_variable_commands.html`) | thống kê |
| M/const | `function_calculations/scientific_constants.html` | CONST |
| M/conv | `function_calculations/metric_conversion.html` | CONV |
| M/abs | `function_calculations/absolute.html` | Abs |
| M/eng | `basic_calculations/engineering_symbols.html` | ký hiệu kỹ thuật |
| **P** | Bài báo trên Tạp chí Khoa học ĐH Đồng Tháp số 38 (6/2019), viết về fx-580VN X: https://dthujs.vn/index.php/dthujs/article/view/403 | Có các ví dụ "ấn STO A", "SOLVE (SHIFT CALC)", "MENU 8" (Table), "MENU 2" (Complex) kèm OPTN, và "ấn = =" sau khi nhập giá trị đầu. |
| **DW** | Duke Pratt wiki "Calculator Tips/Classwiz": https://pundit.pratt.duke.edu/wiki/Calculator_Tips/Classwiz | Dòng ClassWiz cùng thế hệ: ∠ = SHIFT ENG, chuyển dạng phức qua OPTN, phím STO riêng, có phím ×10^x. |
| **ES** | Sách hướng dẫn fx-570ES PLUS (tiếng Việt): https://support.casio.com/global/vi/calc/manual/fx-570ESPLUS_991ESPLUS_vi/using_calculation_modes/cmplx.html | Dùng để chỉ ra nguồn gốc lỗi: `SHIFT 2 (CMPLX)`, `SHIFT 1 (STAT)`, `SHIFT RCL (STO)`, `SHIFT hyp (Abs)` là phím của đời **ES PLUS** (fx-570VN PLUS), không phải fx-580VN X. |
| **GV** | GEARVN, cách bấm Abs trên fx-580VN X: https://gearvn.com/blogs/thu-thuat-giai-dap/cach-bam-gia-tri-tuyet-doi-tren-casio-fx580vn-x | Nguồn phụ, khớp với M/abs. |
| **PY** | Python (script trong scratchpad của phiên) chạy lại từng chuỗi phép tính theo đúng thứ tự bấm. SOLVE được giả lập bằng phương pháp Newton; M/solve xác nhận máy dùng phương pháp này. | Giả lập Newton chỉ cho biết khả năng hội tụ. Máy thật có thể khác ở bước lặp. |

Nhãn: **ĐÃ XÁC NHẬN** (có nguồn trực tiếp) · **CÓ VẺ ĐÚNG** (hợp lý, chưa có nguồn trực tiếp hoặc chỉ giả lập) · **SAI/NGHI SAI** · **KHÔNG KIỂM ĐƯỢC**.

**Phát hiện chung:** phần lớn chuỗi phím sai trong sổ tay là phím của đời **fx-570VN PLUS (ES PLUS)**: `SHIFT 1/2/5`, `SHIFT RCL`, `SHIFT hyp`, `ALPHA )`. fx-580VN X là đời ClassWiz. Các chức năng phụ của đời này nằm trong **OPTN**, máy có phím **STO** và phím **x** riêng. Riêng phần số liệu thì khớp: mọi đáp số chạy lại bằng Python đều khớp với tài liệu ở 4 chữ số có nghĩa, trừ 3 lệnh bấm dùng sai biến (D1, D11, E11) và một ghi chú làm tròn (M4).

---

## Bảng kiểm

| Gói | Lệnh / quy tắc trong tài liệu | Nhãn | Nguồn | Ghi chú |
|---|---|---|---|---|
| WP-01 sổ tay §1 | SETUP = `SHIFT MENU` | ĐÃ XÁC NHẬN | M/setup | |
| WP-01 §1 | Đơn vị góc Độ/Rad trong SETUP | ĐÃ XÁC NHẬN | M/setup | Đường bấm: SETUP → Angle Unit → Degree hoặc Radian. |
| WP-01 §1 | Tên dạng hiển thị "LineIO", "MathIO" | SAI/NGHI SAI | M/setup | Tên trên máy: MathI/MathO, MathI/DecimalO, LineI/LineO, LineI/DecimalO. Muốn ra số thập phân ngay thì chọn **MathI/DecimalO** hoặc bấm `SHIFT =` (≈). |
| WP-01 §1 | SETUP → Fix / Sci / Norm | ĐÃ XÁC NHẬN | M/setup | Nằm ở mục Number Format. |
| WP-01 §1 | STO = `SHIFT RCL` | SAI/NGHI SAI | M/var, P, DW, ES | fx-580VN X có **phím STO riêng**: bấm `STO` rồi phím biến, không cần ALPHA. `SHIFT STO` là RECALL (xem bảng giá trị các biến). `SHIFT RCL` là cách bấm của đời ES PLUS. |
| WP-01 §1 | "Chỉ có A–F, X, Y, M (không có W, Z…)" | SAI/NGHI SAI | M/var | Máy có 9 biến **A, B, C, D, E, F, x, y, z**, cộng thêm bộ nhớ độc lập M. Không có W là đúng; có **z**. |
| WP-01 §1 | Gọi biến bằng `ALPHA` + phím biến | ĐÃ XÁC NHẬN | M/var | |
| WP-01 §1 | Ans giữ đủ chữ số | CÓ VẺ ĐÚNG | M (trang Ans) | Trang chỉ nói Ans lưu kết quả; không nêu số chữ số. Có thêm PreAns (chỉ dùng trong Calculate). |
| WP-01 §1 | Nhìn chỉ báo D/R trên thanh trạng thái | CÓ VẺ ĐÚNG | M (`getting_started/display.html`) | Trang xác nhận có chỉ báo Degree/Radian/Gradian, nhưng ký hiệu là ảnh nên không đọc được chữ. |
| WP-01 §2 | Dấu `=` của phương trình: `ALPHA CALC` | ĐÃ XÁC NHẬN | M/solve, M/calc | |
| WP-01 §2, §4 | Ẩn X gõ bằng `ALPHA )` | SAI/NGHI SAI | M/var, M/solve, M/table | Trên 580VN X, `ALPHA )` cho ra **y**. Ẩn **x** gõ bằng **phím x riêng** hoặc `ALPHA (`. Ở TABLE, mọi biến khác x bị coi là **hằng số**, nên gõ `ALPHA )` sẽ ra bảng hằng mà máy không báo lỗi. |
| WP-01 §2 | SOLVE = `SHIFT CALC` | ĐÃ XÁC NHẬN | M/solve, P | SOLVE chỉ dùng được trong phương thức Calculate. |
| WP-01 §2 | "Nhập giá trị đầu, bấm `=`" (một lần) | SAI/NGHI SAI | M/solve (ví dụ 2), P | Máy hiện danh sách giá trị hiện tại của các biến. Nhập giá trị đầu của x rồi bấm `=`, sau đó bấm **`=` thêm một lần** để giải. Bài báo P ghi "ấn = =". Nếu biểu thức có biến khác (A, B…), máy hỏi lần lượt từng biến. |
| WP-01 §2 | Màn hình nghiệm hiện hai vế "Left, Right" | SAI/NGHI SAI | M/solve | Máy hiện **L−R** (vế trái trừ vế phải). L−R càng gần 0, nghiệm càng tin được. |
| WP-01 §2 | SOLVE trả một nghiệm, phụ thuộc giá trị đầu | ĐÃ XÁC NHẬN | M/solve | Máy dùng phương pháp Newton. Khi chưa hội tụ, máy hỏi "Continue:[=]"; có thể báo "Cannot Solve". |
| WP-01 §2 | Biến khác X giữ giá trị cũ | ĐÃ XÁC NHẬN | M/solve | Máy hiện giá trị hiện tại của từng biến để người bấm sửa. |
| WP-01 §3 | CALC: bấm `CALC`, máy hỏi từng biến, nhập rồi `=` | ĐÃ XÁC NHẬN | M/calc | Nhập xong biến cuối cần bấm thêm `=` để tính. Đổi bộ số: `CALC` (hoặc `=`). |
| WP-01 §3 | Giữ biến không đổi bằng cách bấm `=` | ĐÃ XÁC NHẬN | M/calc | |
| WP-01 §4 | TABLE: `MENU` → Table | ĐÃ XÁC NHẬN | M/table, P | Tên mục trên máy là "Table", phím tắt `MENU 8` (P). Sổ tay gọi "Bảng giá trị": nên ghi thêm tên máy. |
| WP-01 §4 | "Máy hỏi g(X) thì bấm `=` bỏ qua" | KHÔNG KIỂM ĐƯỢC | M/setup, M/table | Mặc định máy dùng f(x),g(x), tối đa 30 dòng. Nguồn không nói bấm `=` với g(x) trống thì sao. Cách chắc chắn: SETUP → ▼▼ → Table → f(x), được 45 dòng và máy không hỏi g(x). |
| WP-01 §4 | Start / End / Step, mỗi mục kết thúc bằng `=` | ĐÃ XÁC NHẬN | M/table | Mặc định 1 / 5 / 1. |
| WP-01 §4 | Quá số hàng thì báo "Argument ERROR" | SAI/NGHI SAI | M/err, M/table | Máy báo **Range ERROR**. Tối đa **45 dòng** với f(x), **30 dòng** với f(x),g(x). Mọi bảng trong 5 gói đều ≤ 21 dòng nên chạy được với cả hai cài đặt. |
| WP-01 §5 | Số phức: `MENU` → Complex | ĐÃ XÁC NHẬN | M/cplx, P | Phím tắt `MENU 2`. |
| WP-01 §5 | ∠ = `SHIFT (−)` | SAI/NGHI SAI | M/cplx, DW | ∠ nằm trên **phím ENG**: bấm `SHIFT ENG` (cùng phím với *i*). Vị trí `SHIFT (−)` là của đời ES PLUS. |
| WP-01 §5 | *i* là phím `ENG` | ĐÃ XÁC NHẬN | M/cplx, M/eng, DW | Chỉ khi ở phương thức Complex. |
| WP-01 §5 | Chuyển dạng: `SHIFT 2` (CMPLX) → r∠θ / a+bi | SAI/NGHI SAI | M/cplx, DW, ES | Trên 580VN X, bấm ở cuối biểu thức: `OPTN ▼ 1` (▶r∠θ) hoặc `OPTN ▼ 2` (▶a+bi). Có thể đặt dạng mặc định ở SETUP → ▼ → Complex. `SHIFT 2 (CMPLX)` là của ES PLUS. |
| WP-01 §5 | Abs = `SHIFT hyp` | SAI/NGHI SAI | M/abs, M/cplx, GV | Abs = **`SHIFT (`**. 580VN X không có phím hyp. |
| WP-01 §5 | arg = `SHIFT 2` → arg | SAI/NGHI SAI | M/cplx | `OPTN 1` (Argument). Ngoài ra: Conjg = `OPTN 2`, ReP = `OPTN 3`, ImP = `OPTN 4`. |
| WP-01 §5 | Góc θ tuỳ SETUP; đơn vị phải khớp | ĐÃ XÁC NHẬN | M/cplx | Máy cho θ trong khoảng (−180°; 180°]. Vì vậy X4 ra 98,26° là đúng. |
| WP-01 §6 | Vectơ: `MENU` → Vector, chọn VctA, chọn số chiều 2/3, nhập toạ độ | ĐÃ XÁC NHẬN | M/vct | Máy có VctA..VctD. Định nghĩa lại vectơ bằng `OPTN 1` (Define Vector). |
| WP-01 §6 | Gọi vectơ bằng `SHIFT 5` (VECTOR) → VctA | SAI/NGHI SAI | M/vct | VctA = `OPTN 3`, VctB = `OPTN 4`, VctAns = `OPTN ▼ 1`. |
| WP-01 §6 | Tích có hướng `VctA × VctB` (phím ×) | ĐÃ XÁC NHẬN | M/vct (ví dụ 6) | |
| WP-01 §6, V2 | Tích vô hướng: `SHIFT 5` → Dot | SAI/NGHI SAI | M/vct | `OPTN ▼ 2` (Dot Product). Màn hình hiện dấu "•", không hiện chữ "Dot". |
| WP-01 §6 | Độ dài `Abs(VctA)` bằng `SHIFT hyp` | SAI/NGHI SAI | M/vct (ví dụ 7) | `SHIFT (` (Abs) → `OPTN 3` → `)`. |
| WP-01 §6, V2 | Góc giữa hai vectơ bằng `cos⁻¹(Dot/(Abs×Abs))` | CÓ VẺ ĐÚNG | M/vct (ví dụ 8), PY | Công thức đúng, ra 59,43°. Máy có sẵn hàm **Angle(** (`OPTN ▼ 3`): `Angle(VctA, VctB)`, ít phím hơn. Dấu phẩy gõ bằng `SHIFT )`. |
| WP-01 §6 | Hai vectơ phải cùng số chiều | ĐÃ XÁC NHẬN | M/err | Sai thì máy báo Dimension ERROR. |
| WP-01 §7 | `MENU` → Statistics; loại 1-Variable | ĐÃ XÁC NHẬN | M/stat | |
| WP-01 §7, St2, St3 | Tên loại "A+Bx", "e^x"; hệ số A, B | SAI/NGHI SAI | M/stat | Tên trên máy: **y=a+bx** (phím 2) và **y=a·e^(bx)** (▼ 1). Hệ số ghi **chữ thường a, b**. Kiểu "A+Bx" là cách ghi của đời ES PLUS. |
| WP-01 §7 | Nhập cột X (và Y); `AC` thoát bảng | ĐÃ XÁC NHẬN | M/stat | Bấm `AC` để sang màn hình tính thống kê. |
| WP-01 §7, St1–St3 | `SHIFT 1` (STAT) → Var / Reg | SAI/NGHI SAI | M/stat | Xem cả bảng: `OPTN` → 1-Variable Calc / 2-Variable Calc / Regression Calc. Lấy từng giá trị: `OPTN ▼ 2` (Variable: x̄, σx, sx, n…) và `OPTN ▼ 4` (Regression: a, b, r, x̂, ŷ). |
| WP-01 §7 | σx chia n, sx chia n−1 | ĐÃ XÁC NHẬN | M/stat | |
| WP-01 §7 | "Đổi kiểu hồi quy thì bảng nhập bị xoá" | SAI/NGHI SAI | M/stat | Dữ liệu bị xoá khi ra khỏi Statistics, khi đổi giữa **1 biến ↔ 2 biến**, hoặc khi đổi cài đặt Statistics (cột Freq). Nguồn không nói đổi giữa hai kiểu hồi quy 2 biến thì xoá. |
| WP-01 §7 | Xoá dữ liệu cũ, kiểm `n` | ĐÃ XÁC NHẬN | M/stat | Xoá hết bằng `OPTN 2` (Editor) → Delete All. |
| WP-01 §7 | Hồi quy mũ cần mọi y > 0 | CÓ VẺ ĐÚNG | (toán) | Hồi quy mũ cần ln y. Chưa thấy nguồn nêu máy báo lỗi gì khi có y ≤ 0. |
| WP-01 §8 | CONST = `SHIFT 7` | ĐÃ XÁC NHẬN | M/const | |
| WP-01 §8 | Chọn hằng số "theo mã số in ở nắp máy" | SAI/NGHI SAI | M/const | 580VN X không dùng mã số. `SHIFT 7` mở menu **danh mục** (Universal, Electromagnetic, Atomic&Nuclear, Physico-Chem, Adopted Values, Other), sau đó chọn số mục. Ví dụ h = `SHIFT 7 1 1`, c₀ = `SHIFT 7 1 3`, e = `SHIFT 7 2 3`. Kiểu chọn theo mã số là của đời ES PLUS. |
| WP-01 §8 | CONV = `SHIFT 8` | ĐÃ XÁC NHẬN | M/conv | |
| WP-01 §8 | Đổi km/h ↔ m/s, atm ↔ Pa bằng CONV | ĐÃ XÁC NHẬN | M/conv | Nằm ở Velocity (▼ 1) và Pressure (▼ 2). |
| WP-01 §8 | Đổi eV ↔ J bằng CONV | SAI/NGHI SAI | M/conv | CONV **không có** cặp eV ↔ J. Phải nhân/chia bằng e: dùng số đề cho, hoặc lấy e từ `SHIFT 7 2 3`. |
| WP-01 §8 | "Tiền tố SI: dùng `ENG`" | SAI/NGHI SAI | M/eng | `ENG` chỉ đổi cách **hiển thị** kết quả. Muốn **nhập** k, m, μ, n, p thì dùng `OPTN` → Engineer Symbol, hoặc gõ ×10^x. |
| WP-01 §8, WP-06 | Dùng phím ×10^x, tránh gõ "E" | CÓ VẺ ĐÚNG | DW | Dòng ClassWiz có phím ×10^x. |
| WP-01 §8 | Hằng số trong máy khác SGK ở chữ số 4–6 | ĐÃ XÁC NHẬN | M/const, PY | Máy lưu h = 6,626070040·10⁻³⁴ và e = 1,6021766208·10⁻¹⁹ (bộ hằng số CODATA 2014). Với K1, các hằng này cho 3,973·10⁻¹⁹ J = 2,480 eV, khác đáp số dùng số đề cho (3,976·10⁻¹⁹ J; 2,482 eV). Ghi chú K1 đúng. |
| WP-01 S1 | SOLVE `4cos(5πX−π÷3)=2`, giá trị đầu 0,1 | CÓ VẺ ĐÚNG | PY | Newton từ 0,1 hội tụ về 2/15 = 0,1333. Từ 0,05 thì về t = 0, khớp cảnh báo trong bài. |
| WP-01 S2, S3 | SOLVE, giá trị đầu 50 và 5 | CÓ VẺ ĐÚNG | PY | Ra 28,97 và 9,154. |
| WP-01 C1, C2 | CALC theo biến A | ĐÃ XÁC NHẬN | M/calc, PY | Số khớp. |
| WP-01 T1–T3 | TABLE: 9 / 11 / 13 / 20 dòng | ĐÃ XÁC NHẬN | M/table, PY | Số dòng ≤ 30. Kết quả khớp: 100 Hz (1,9997 A), 100,5 Hz, f₀ = 100,66; 11 điểm; X = 4. |
| WP-01 X1 | `SHIFT 2` → r∠θ | SAI/NGHI SAI | M/cplx | Bấm `OPTN ▼ 1` (▶r∠θ) ở cuối biểu thức. Số 5∠6,870° khớp. Góc âm (−30) gõ bằng phím `(−)`. |
| WP-01 X2, X4 | Phép chia, phép trừ số phức (Rad) | ĐÃ XÁC NHẬN | PY | Ra 2√2∠−0,9273 và 3,230∠1,715 (98,26°). Phím ∠ theo sửa ở §5. |
| WP-01 X3 | "Ans phần ảo (`SHIFT 2` → ImP)" | SAI/NGHI SAI | M/cplx | ImP = `OPTN 4`. Số 50 + 86,60*i*, L = 0,2757 khớp. |
| WP-01 V1 | `Abs(Ans)` sau phép tính vectơ | KHÔNG KIỂM ĐƯỢC | M/vct | M chỉ dùng VctAns (`OPTN ▼ 1`); không nói phím Ans trong Vector có cho ra VctAns không. Nên ghi `Abs(VctAns)`. Số 2,884·10⁻¹⁴ khớp. |
| WP-01 St2 | Gõ `4π² ÷ B` (B lấy từ Reg) | SAI/NGHI SAI | M/stat | Phải chèn hệ số **b** bằng `OPTN ▼ 4` → b. Gõ `ALPHA B` sẽ lấy **biến nhớ B** (giá trị cũ) và máy không báo lỗi. Đáp số 10,01 khớp. |
| WP-01 St3 | `ln(2) ÷ (−B)` | SAI/NGHI SAI | M/stat | Lỗi giống St2: dùng `OPTN ▼ 4` → b. Đáp số 3,108 khớp. |
| WP-01 St1, K1–K3 | Chuỗi số học | ĐÃ XÁC NHẬN | PY | Các số khớp. |
| WP-03 D1 | `W²×0.06` cho a_max | SAI/NGHI SAI | M/var, PY | Máy **không có biến W**. Phải là `D²×0.06` (ω đã lưu ở D), ra 15,00. README WP-03 ghi đã đổi W thành D nhưng dòng này còn sót. |
| WP-03 D11 | `50×π÷A` cho thời gian dừng | SAI/NGHI SAI | PY | Bài này không gán A; ω nằm ở D. Nếu A còn giữ 0,05 từ D9 thì máy ra 3141,6. Đúng: `50×π÷D` = 7,025 s. |
| WP-03 D3, D7, D8, D9 | `STO B`, `STO A`, `STO D`, `A−Ans` | ĐÃ XÁC NHẬN | M/var, PY | Phím STO riêng. Các số khớp. |
| WP-03 D2, D10 | Độ cho cos góc độ; gần đúng ở Rad | ĐÃ XÁC NHẬN | PY | Ra 0,3784 / 0,3787 và 2,678 / 1,566. Bẫy `cos(8)` ở Rad cho 4,106: đúng là số vô nghĩa. |
| WP-03 D4, D12 | Số phức ở Độ: `8∠30+8∠90`; `6∠60+5.196∠−90` | CÓ VẺ ĐÚNG | PY | D4 ra 13,86∠60. D12 gõ 5,196 đã làm tròn nên ra 3∠0,0029°, không đúng 0. Nên lưu −6cos150 vào biến rồi dùng biến đó. |
| WP-03 D5 | SOLVE giá trị đầu 0,1 | CÓ VẺ ĐÚNG | PY | Newton cho 0,1500. |
| WP-03 D12 | TABLE bước 1 rồi bước 0,1 | ĐÃ XÁC NHẬN | M/table, PY | 11 và 16 dòng. Nhỏ nhất tại 5 và 5,2. |
| WP-03 kỹ thuật | Góc độ nhập `60×π÷180` ở Rad | ĐÃ XÁC NHẬN | (toán) | |
| WP-03 mini M4 | "Thế φ đã làm tròn −0,1199 thì ra 0,1858" | SAI/NGHI SAI | PY | Thế −0,1199 vẫn ra 0,185749, tức 0,1857 như khi dùng pha chính xác. Ghi chú chênh 0,0001 không đúng. Chuỗi SOLVE từ giá trị đầu 0,2 thì ổn. |
| WP-03 mini M1–M3 | Chuỗi số | ĐÃ XÁC NHẬN | PY | Các số khớp. |
| WP-04 kỹ thuật tr.1 | "Lưu λ vào D, rồi `CALC` với x và t" | SAI/NGHI SAI | M/var | Máy **không có biến t**. Dùng **x và y**, hoặc A, B, làm biến của CALC. |
| WP-04 kỹ thuật | TABLE `f(X)=X÷λ` với λ lưu trong D | ĐÃ XÁC NHẬN | M/table | Mọi biến khác x được coi là hằng nên D giữ nguyên. |
| WP-04 kỹ thuật, W2, W12 | `log(…)` thập phân, `10^(…)` | CÓ VẺ ĐÚNG | PY | Các số khớp: 86,00; 6,021; 45,19; 48,20. |
| WP-04 W1 | `STO D`, `STO B`, Rad | ĐÃ XÁC NHẬN | M/var, PY | Ra 20; 7,854; 1,763. |
| WP-04 W10 | SOLVE `√(X²+400)−X=18`, giá trị đầu 2 | CÓ VẺ ĐÚNG | PY | Ra 2,111. Kiểm k = 1 cho 65,17. |
| WP-04 W11 | `cos⁻¹` trả độ ở chế độ Độ | ĐÃ XÁC NHẬN | M/setup, PY | Ra 0,3918 T = 0,07837 s. |
| WP-04 W5–W8, mini | Đếm cực trị, TABLE 8 và 13 dòng | ĐÃ XÁC NHẬN | PY | 11/12, 10/11, 7/6, 180 và 220 Hz; mini 15/16. |
| WP-05 chung | Dùng D cho ω, `STO F` (E2), `STO C` (E11) | ĐÃ XÁC NHẬN | M/var | D, F, C đều có trên máy. |
| WP-05 E3 | "Gấp đôi U: `Ans÷4` ở bước hao phí" | SAI/NGHI SAI | PY | Sau khi bấm `1−Ans÷100000`, Ans đã là H = 0,9877, không còn là ΔP. Phải bấm `Ans÷4` ngay sau bước ΔP, hoặc lưu ΔP vào biến trước (`STO A`). Các số 1235 W và 308,6 W khớp. |
| WP-05 E5 | Số phức Rad `(120√2∠0)÷(40+70i)` | ĐÃ XÁC NHẬN | PY | Ra 2,105∠−1,052; u_L 273,6∠0,5191; u_C 126,3∠−2,622. Phím ∠ theo sửa ở §5. |
| WP-05 E10 | Độ `(200∠0)÷(2∠45)`, "chuyển a+bi", "+100i" | CÓ VẺ ĐÚNG | M/cplx, PY | Chuyển a+bi bằng `OPTN ▼ 2`. Phần ảo lấy bằng `OPTN 4`. Kết quả 70,71 + 29,29*i*, L = 0,09323 khớp. |
| WP-05 E11 | `CALC` công thức theo f; `60÷Z`, `30÷Z` | SAI/NGHI SAI | M/var, M/calc, PY | Máy không có biến f: dùng x. Z chưa từng được lưu (máy chỉ có z thường). Lưu kết quả Z(40) = 69,63 vào một biến (ví dụ `STO E`) rồi dùng `60÷E`, `30÷E`. Các số khớp. |
| WP-05 E6, E7 | TABLE 21 và 11 dòng | ĐÃ XÁC NHẬN | M/table, PY | Lớn nhất tại 41 và 62,5. |
| WP-05 E1, E2, E4, E8, E9, E12, mini | Chuỗi số học | ĐÃ XÁC NHẬN | PY | Các số khớp. |
| WP-05 kỹ thuật | Góc φ ra Độ hay Rad tuỳ SETUP | ĐÃ XÁC NHẬN | M/cplx | |
| WP-06 kỹ thuật | Lưu ω vào D; viết `×10^−12` | CÓ VẺ ĐÚNG | M/var, DW | |
| WP-06 Q5 | SOLVE `cos(2π÷D×X)=0.5`, giá trị đầu `10^−5` | CÓ VẺ ĐÚNG | PY | Ra 1,987·10⁻⁵ = T/6. |
| WP-06 Q12 | TABLE `3.5÷X`, Start 4, End 10 (7 dòng) | ĐÃ XÁC NHẬN | M/table, PY | Vân sáng k = 5…9, vân tối k = 5…8. |
| WP-06 Q4, Q10, mini M3 | `sin⁻¹`, `tan` ở Độ | ĐÃ XÁC NHẬN | PY | Ra 25,37 / 41,81; 9,050 / 9,006 mm; 48,59 / 58,99. |
| WP-06 Q6 | `180×(87.95−10)÷(250−10)` dùng C đã làm tròn | ĐÃ XÁC NHẬN | PY | Ra 58,4625°. Với C đủ chữ số thì ra 58,4643°. Cả hai làm tròn thành 58,46°. |
| WP-06 Q1–Q3, Q7–Q9, Q11, mini | Chuỗi số học | ĐÃ XÁC NHẬN | PY | Các số khớp. |
| Tất cả | Mô phỏng bằng trình giả lập | KHÔNG KIỂM ĐƯỢC | | Không chạy được giả lập fx-580VN X (bản chính hãng là phần mềm Windows; không có bản web chính thức). |

### Đếm nhãn (theo số dòng của bảng)
ĐÃ XÁC NHẬN 48 · CÓ VẺ ĐÚNG 14 · SAI/NGHI SAI 30 · KHÔNG KIỂM ĐƯỢC 3 (tổng 95 dòng).

---

## Sửa đề xuất (mỗi ý một dòng)

- `so-tay.md` §1: STO là **phím `STO` riêng**, không phải `SHIFT RCL`; `SHIFT STO` (RECALL) để xem giá trị các biến.
- `so-tay.md` §1: biến có sẵn là A, B, C, D, E, F, x, y, z, cộng bộ nhớ M; sửa câu "không có Z".
- `so-tay.md` §1: đổi tên dạng hiển thị thành MathI/MathO, MathI/DecimalO, LineI/LineO, LineI/DecimalO; muốn ra số thập phân chọn MathI/DecimalO hoặc bấm `SHIFT =`.
- `so-tay.md` §2 và §4: ẩn x gõ bằng **phím x** (hoặc `ALPHA (`), không phải `ALPHA )` (phím này cho ra y).
- `so-tay.md` §2: sau khi nhập giá trị đầu, bấm `=` rồi bấm `=` thêm lần nữa để giải.
- `so-tay.md` §2: màn hình nghiệm hiện L−R (hiệu hai vế), không hiện Left, Right riêng; SOLVE chỉ dùng trong Calculate.
- `so-tay.md` §4: lỗi khi bảng quá dài là **Range ERROR**; tối đa 45 dòng với f(x), 30 dòng với f(x),g(x).
- `so-tay.md` §4: thêm bước SETUP → Table → f(x) để máy không hỏi g(x).
- `so-tay.md` §5: ∠ = `SHIFT ENG`.
- `so-tay.md` §5: chuyển dạng kết quả bằng `OPTN ▼ 1` (▶r∠θ) và `OPTN ▼ 2` (▶a+bi), hoặc đặt ở SETUP → Complex.
- `so-tay.md` §5: Abs = `SHIFT (`; Arg = `OPTN 1`; ReP = `OPTN 3`; ImP = `OPTN 4`.
- `so-tay.md` §6: VctA = `OPTN 3`, VctB = `OPTN 4`, VctAns = `OPTN ▼ 1`; tích vô hướng `OPTN ▼ 2` (Dot Product).
- `so-tay.md` §6: Abs vectơ = `SHIFT (`; thêm hàm `Angle(VctA,VctB)` (`OPTN ▼ 3`) để tính góc.
- `so-tay.md` §7: tên loại là y=a+bx và y=a·e^(bx); hệ số viết chữ thường a, b.
- `so-tay.md` §7: lấy kết quả bằng `OPTN` → 1-Variable Calc / Regression Calc, hoặc `OPTN ▼ 2` (Variable) và `OPTN ▼ 4` (Regression); bỏ `SHIFT 1`.
- `so-tay.md` §7: thêm bẫy: gõ `ALPHA B` lấy biến nhớ B, không phải hệ số hồi quy b.
- `so-tay.md` §7: sửa câu "đổi kiểu hồi quy thì bảng bị xoá" thành: dữ liệu bị xoá khi ra khỏi Statistics, khi đổi giữa 1 biến và 2 biến, hoặc khi đổi cài đặt Statistics.
- `so-tay.md` §8: CONST chọn theo menu danh mục rồi số mục (ví dụ h = `SHIFT 7 1 1`); bỏ "mã số in ở nắp máy".
- `so-tay.md` §8: bỏ eV ↔ J khỏi danh sách CONV, vì CONV không có cặp này; dùng e đề cho hoặc `SHIFT 7 2 3`.
- `so-tay.md` §8: nhập tiền tố SI bằng `OPTN` → Engineer Symbol; `ENG` chỉ đổi cách hiển thị.
- `wp-01/README.md`: bỏ câu "Var, Reg, Dot, CMPLX… theo dòng fx-570/580VN"; ghi rõ sổ tay đã đối chiếu sách hướng dẫn chính hãng fx-580VN X.
- `wp-01/bai-luyen.md` X1: thay `SHIFT 2` → r∠θ bằng `OPTN ▼ 1`.
- `wp-01/bai-luyen.md` X3: thay `SHIFT 2` → ImP bằng `OPTN 4`.
- `wp-01/bai-luyen.md` V1: ghi `Abs(VctAns)` (VctAns = `OPTN ▼ 1`) thay cho `Abs(Ans)`.
- `wp-01/bai-luyen.md` V2: Dot = `OPTN ▼ 2`; thêm cách tính góc bằng `Angle(VctA,VctB)`.
- `wp-01/bai-luyen.md` St1: thay `SHIFT 1` → Var bằng `OPTN` → 1-Variable Calc.
- `wp-01/bai-luyen.md` St2: thay `SHIFT 1` → Reg bằng `OPTN` → Regression Calc; `4π² ÷ b` với b chèn bằng `OPTN ▼ 4` → b.
- `wp-01/bai-luyen.md` St3: `ln(2) ÷ (−b)`, b chèn bằng `OPTN ▼ 4` → b; đổi "e^x" thành y=a·e^(bx).
- `wp-01/bai-luyen.md` St2: đổi "A+Bx" thành y=a+bx.
- `wp-03/bai-luyen.md` D1: `W²×0.06` → `D²×0.06`.
- `wp-03/bai-luyen.md` D11: `50×π÷A` → `50×π÷D`.
- `wp-03/bai-luyen.md` D12: thêm gợi ý lưu −6cos150 vào biến để số phức ra đúng 3∠0.
- `wp-03/mini-test.md` M4: bỏ câu "thế φ đã làm tròn thì ra 0,1858", vì vẫn ra 0,1857.
- `wp-04/ky-thuat.md` trang 1: "CALC với x và t" → "CALC với x và y" (máy không có biến t).
- `wp-05/bai-luyen.md` E3: ghi rõ bấm `Ans÷4` ngay sau bước ΔP, hoặc lưu ΔP bằng `STO A` rồi tính `A÷4`.
- `wp-05/bai-luyen.md` E10: ghi rõ chuyển a+bi bằng `OPTN ▼ 2`; phần ảo lấy bằng `OPTN 4`.
- `wp-05/bai-luyen.md` E11: dùng biến x trong công thức CALC; lưu Z vào một biến (ví dụ `STO E`) rồi tính `60÷E` và `30÷E`.
- `wp-03/README.md`, `wp-04/README.md`, `wp-05/README.md`: dòng "đã đổi W thành D" chưa đúng hết cho WP-03 (D1 còn W); sửa lại sau khi vá D1.
- Bấm thử trên máy thật vẫn cần, ưu tiên các chỗ chỉ suy từ nguồn: bấm `=` hai lần trong SOLVE; `=` với g(x) trống trong TABLE; Ans trong Vector; hồi quy mũ khi có y ≤ 0.

## Tóm tắt
- Có 95 dòng kiểm (mỗi dòng là một lệnh hoặc một nhóm lệnh cùng loại): 48 ĐÃ XÁC NHẬN, 14 CÓ VẺ ĐÚNG, 30 SAI/NGHI SAI, 3 KHÔNG KIỂM ĐƯỢC.
- Phần số liệu: mọi đáp số chạy lại bằng Python đều khớp ở 4 chữ số có nghĩa. Lỗi chỉ nằm ở chuỗi phím và biến nhớ.
- Nguyên nhân chính: sổ tay viết theo phím của fx-570VN PLUS (đời ES PLUS), không theo fx-580VN X (đời ClassWiz, chức năng phụ nằm trong OPTN).

## Đã áp dụng (19/10/2026, sau khi thầy bấm thử máy thật)

- `wp-01/so-tay.md`: STO là phím riêng, `SHIFT STO` xem biến; biến A–F, x, y, z, M; tên dạng hiển thị MathI/MathO…; ẩn x gõ bằng phím `x` (SOLVE, TABLE); bấm `=` hai lần trong SOLVE, L−R; Range ERROR 45/30 dòng, SETUP → Table → f(x); ∠ = `SHIFT ENG`, `OPTN ▼ 1`/`OPTN ▼ 2`, Abs = `SHIFT (`, Arg/Conjg/ReP/ImP = `OPTN 1/2/3/4`; VctA/VctB/VctAns, Dot `OPTN ▼ 2`, Angle; y=a+bx và y=a·e^(bx), `OPTN` thay `SHIFT 1`, bẫy `ALPHA B`, điều kiện xoá dữ liệu; CONST theo menu danh mục, bỏ eV↔J khỏi CONV, Engineer Symbol.
- `wp-01/bai-luyen.md`: S1–S3, T1–T3 (phím x, `=` hai lần, SETUP Table f(x)); X1, X3 (`OPTN`); V1 (`Abs(VctAns)`); V2 (Dot, Angle); St1–St3 (`OPTN`, a/b chữ thường, b chèn bằng `OPTN ▼ 4`).
- `wp-01/README.md`, `wp-03..06/README.md`: ghi đã đối chiếu sách chính hãng và thầy đã thử máy thật 19/10/2026.
- `wp-03/bai-luyen.md`: D1 `D²×0.06`; D11 `50×π÷D`; D12 lưu `−6cos150` vào A; D5 phím x; D4 ∠/▶r∠θ. `wp-03/mini-test.md` M4 bỏ câu 0,1858. `wp-03/ky-thuat.md`: f(x).
- `wp-04/ky-thuat.md`: CALC với x và y; f(X)→f(x) (3 dòng). `wp-04/bai-luyen.md`: X→x ở TABLE/SOLVE (W5, W7, W10).
- `wp-05/bai-luyen.md`: E3 lưu ΔP bằng `STO A`; E5, E10 `OPTN ▼ 1`/`OPTN ▼ 2`/`OPTN 4`; E11 biến x, lưu Z vào E (thêm: công thức dùng `C×10^−6` vì C lưu theo μF); E6, E8 phím x. `wp-05/ky-thuat.md`: tên Complex, f(x).
- `wp-06/bai-luyen.md` (Q5, Q12), `wp-06/ky-thuat.md`: phím x (TABLE/SOLVE).
- Ngoài danh sách: đã quét cả 5 gói, không còn `ALPHA )`, `SHIFT 1/2/5`, `SHIFT RCL`, `SHIFT hyp`, `SHIFT (−)`, "Argument ERROR", "A+Bx", W/Z/t/f làm biến. Chạy lại `python3 tinh.py` ở 5 gói: không lỗi; E11 kiểm bằng Python ra Z = 69,63; 0,8617; 0,4309.
