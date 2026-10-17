# CĐ08. Cảm ứng điện từ và dòng điện xoay chiều (bài 152, khoá Vật lí HSG & chuyên KHTN 9) — dàn ý chung

Nguồn: docx `08` (đã trích ở `nguon.txt` cùng thư mục — mục A, B, C, I dùng làm khung; ví dụ D/E/G/H trong docx KHÔNG chép,
số liệu dưới đây là số mới tự đặt, tính bằng `tinh.py` cùng thư mục — chạy `python3 tinh.py` để xem lại). Viết lại bằng lời mình.

**Phạm vi (docx đã đối chiếu CT 2018, giữ nguyên ý):** YCCĐ KHTN 9 mạch Điện từ chỉ có 3 dòng — (1) thí nghiệm: số đường sức từ
xuyên qua tiết diện cuộn dây kín biến thiên ⇒ có dòng cảm ứng; (2) nguyên tắc tạo dòng xoay chiều; (3) ví dụ tác dụng nhiệt, phát sáng,
từ, sinh lí của dòng xoay chiều. Nam châm/từ trường/đường sức là ôn tập (KHTN 7). **Máy biến áp và truyền tải điện năng là NỘI DUNG
BỔ SUNG NGOÀI YCCĐ lớp 9** (đề HSG, chuyên vẫn ra) — trong bài ghi nhãn "Mở rộng HSG". Cảm ứng điện từ chỉ ĐỊNH TÍNH: không
$e=-\Delta\Phi/\Delta t$, không $\Phi = BS\cos\alpha$; "từ thông" chỉ là tên gọi của "số đường sức từ xuyên qua tiết diện".

**Ranh giới với CĐ05 (bài 165, công suất điện – điện năng – Joule–Lenz):** $P = UI$, $Q = I^2Rt$, $A = Pt$, tiền điện, hiệu suất nguồn
đã dạy ở CĐ05 (dạng trong `165.json`: "Công suất điện của dụng cụ và số ghi trên thiết bị", "Tính điện năng tiêu thụ và tiền điện",
"Hiệu suất nguồn điện, an toàn điện", "Công và công suất của nguồn điện"). CĐ08 chỉ DÙNG LẠI (nhắc 1 dòng), không dạy lại, không làm
dạng tính tiền điện. $R = \rho\,\ell/S$ đã có ở CĐ04 (bài 157) — dùng lại. Lực từ / quy tắc bàn tay trái: KHÔNG làm (xem "Cần thầy quyết").
Tuần dùng: buổi 16 (gửi 16/01, dùng tuần 23/01): thứ Hai đọc lý thuyết (40 phút), thứ Ba bài tập mẫu **"hao phí khi truyền tải"** (60 phút)
— nên D4–D6 (3/6 dạng) là truyền tải.

## Quy ước số liệu & ký hiệu (mọi file dùng chung)
- Dùng tên **máy biến áp** (KHTN 9), nhắc một lần "còn gọi là máy biến thế". Cuộn **sơ cấp** (nối nguồn) chỉ số 1: $N_1, U_1, I_1$;
  **thứ cấp** (nối tải) chỉ số 2: $N_2, U_2, I_2$. Công thức: $\dfrac{U_1}{U_2}=\dfrac{N_1}{N_2}$; lí tưởng $U_1I_1=U_2I_2$ ⇒ $\dfrac{I_1}{I_2}=\dfrac{N_2}{N_1}$.
  Hiệu suất máy thực $H_{\text{BA}} = P_2/P_1$.
- Máy phát: $f = n\,p$ ($f$ Hz, $n$ vòng/s, $p$ số **cặp** cực). Lưới Việt Nam $50$ Hz, $220$ V (giá trị hiệu dụng). Mỗi chu kì dòng đổi chiều 2 lần.
- Truyền tải: $P$ = công suất ở **đầu** đường dây; $U$ = hiệu điện thế ở **đầu** đường dây; $R$ = điện trở **tổng cả hai dây**
  ($R = \rho\dfrac{2\ell}{S}$, $\ell$ là khoảng cách). $I = \dfrac{P}{U}$; $P_{\text{hp}} = RI^2 = \dfrac{P^2R}{U^2}$; $H = 1-\dfrac{P_{\text{hp}}}{P}$;
  $\Delta U = IR$; $U_{\text{tt}} = U - \Delta U$; $P_{\text{tt}} = P - P_{\text{hp}}$ (chỉ số "tt" = nơi tiêu thụ).
  Trong $…$ viết `P_{\text{hp}}`, `U_{\text{tt}}`, số thập phân `a{,}b`.
- $\rho_{\text{đồng}} = 1{,}7\cdot10^{-8}$, $\rho_{\text{nhôm}} = 2{,}8\cdot10^{-8}$ Ω·m; $D_{\text{đồng}} = 8900$, $D_{\text{nhôm}} = 2700$ kg/m³ (đề cho số).
- Bỏ qua hệ số công suất (lớp 9): coi công suất xoay chiều $= UI$ với giá trị hiệu dụng. Giả thiết "máy biến áp lí tưởng" phải GHI trong đề.
- Hình: đường sức từ NÉT ĐỨT, mũi tên chevron 30° (`field_line`/`field_path`/`chevron` trong `svg_lib.py`); nam châm thẳng tô 2 nửa N/S.

## Lý thuyết (theory.src.html) — 7 mục, ~40 phút
I. **Mở bài:** điện từ nhà máy thuỷ điện ở xa hàng trăm km về tới ổ cắm 220 V — vì sao đường dây Bắc–Nam lại dùng tới 500 kV?
   Câu dự đoán: (1) giữ nguyên công suất và đường dây, tăng hiệu điện thế truyền tải lên gấp đôi thì hao phí trên dây giảm mấy lần
   (2? 4? không đổi?); (2) một nam châm nằm yên trong lòng cuộn dây nối điện kế — kim có lệch không?
II. **Nam châm – từ trường – đường sức từ (ôn tập + nắm tay phải):** hai cực, cùng tên đẩy/khác tên hút, bẻ đôi vẫn đủ 2 cực;
   từ trường quanh nam châm, dòng điện, Trái Đất; nhận biết bằng kim nam châm thử; từ phổ; đường sức "ra Bắc – vào Nam" bên ngoài,
   trong nam châm đi từ S sang N (đường khép kín), chỗ dày = từ trường mạnh; từ trường đều trong khe nam châm chữ U.
   Ống dây có dòng điện ≈ nam châm thẳng; **quy tắc nắm tay phải** (4 ngón theo chiều dòng, ngón cái chỉ chiều đường sức trong lòng ống = hướng cực Bắc);
   mẹo kiểm: nhìn vào một đầu ống thấy dòng ngược chiều kim đồng hồ ⇒ đầu đó là cực Bắc. Nam châm điện (lõi sắt non) và cách làm mạnh lên.
   Hình SVG: nam châm thẳng + đường sức nét đứt; ống dây + bàn tay phải (chú thích mỗi ý một dòng).
III. **Hiện tượng cảm ứng điện từ:** thí nghiệm Làm–Quan sát–Rút ra (đưa vào/giữ yên/kéo ra; đóng–ngắt khoá của nam châm điện; dịch con chạy biến trở);
   **điều kiện:** số đường sức từ xuyên qua tiết diện cuộn dây KÍN **biến thiên** (không phải "nhiều", không phải "có chuyển động").
   **Định luật Lenz (định tính, mở rộng HSG):** dòng cảm ứng sinh từ trường chống lại sự biến thiên ⇒ nam châm lại gần thì mặt cuộn dây đối diện
   thành cực cùng tên (đẩy), ra xa thì thành cực khác tên (hút). Vì sao phải "chống lại": nếu không, điện năng tự sinh ra mà không tốn công — trái bảo toàn năng lượng.
   Ví dụ phản trực giác: quay nam châm thẳng quanh chính trục dọc của nó trước cuộn dây đồng trục ⇒ KHÔNG có dòng (số đường sức không đổi).
IV. **Dòng điện xoay chiều & máy phát:** nguyên tắc (khung dây quay trong từ trường, hoặc nam châm quay trước cuộn dây) ⇒ số đường sức biến thiên tuần hoàn,
   dòng đổi chiều 2 lần mỗi vòng (mỗi chu kì). Máy phát: rôto/stato, hai loại (cuộn dây quay cần vành khuyên + chổi quét; nam châm quay — loại nhà máy dùng).
   Mở rộng: $f = np$ (đổi vòng/phút → vòng/s; "4 cực" = 2 cặp). **Tác dụng của dòng xoay chiều:** nhiệt, phát sáng, từ, sinh lí (mỗi tác dụng một dòng + ví dụ);
   giá trị hiệu dụng định tính (số 220 V là giá trị hiệu dụng; ghi chú mở rộng: cực đại ≈ 311 V, không dùng trong bài tính).
V. **Máy biến áp (Mở rộng HSG):** cấu tạo (lõi lá thép mỏng ghép cách điện + 2 cuộn); nguyên tắc: dòng xoay chiều ở sơ cấp ⇒ từ trường biến thiên trong lõi ⇒
   cảm ứng ở thứ cấp; $U_1/U_2 = N_1/N_2$, tăng áp/hạ áp; lí tưởng $U_1I_1 = U_2I_2$ (tăng áp bao nhiêu lần thì dòng giảm bấy nhiêu lần);
   vì sao không dùng với nguồn một chiều; máy thực có hao phí (điện trở cuộn dây, dòng Fu-cô trong lõi, từ thông rò) ⇒ $U_2$ đo được hơi nhỏ hơn lí thuyết.
   Máy biến áp không tạo ra năng lượng.
VI. **Truyền tải điện năng đi xa (Mở rộng HSG, trọng tâm tuần):** dây nóng lên ⇒ hao phí $P_{\text{hp}} = RI^2$ (nhắc CĐ05), $I = P/U$ ⇒ $P_{\text{hp}} = P^2R/U^2$;
   **tăng $U$ lên $k$ lần ⇒ hao phí giảm $k^2$ lần**; so sánh hai cách giảm hao phí (tăng tiết diện tốn kim loại, tăng $U$ chỉ cần máy tăng áp);
   hiệu suất $H$, độ giảm thế $\Delta U = IR$, $U_{\text{tt}} = U - \Delta U$; bài toán chọn $U$ tối thiểu ⇒ tỉ số vòng máy tăng áp;
   sơ đồ nhiều cấp: máy phát → tăng áp → 500/220/110 kV → hạ áp trạm → 22 kV → hạ áp khu dân cư → 0,4 kV/220 V. An toàn: tránh xa dây cao thế.
   Bài toán mẫu đọc đề từng câu (số liệu KHÁC D4–D6).
VII. **Trả bài và mang về** (6 câu tự trả lời): điều kiện có dòng cảm ứng; chiều dòng cảm ứng khi nam châm ra xa; vì sao máy biến áp cần dòng xoay chiều;
   tăng U 5 lần thì hao phí?; vì sao phải hạ áp trước khi vào nhà; $f$ của máy 2 cặp cực quay 1500 vòng/phút.

**Bẫy** (từ mục I docx, viết lại): nghĩ "có nam châm gần là có dòng" / "phải có chuyển động mới có dòng"; nhầm "từ thông lớn" với "từ thông biến thiên";
Lenz nói thành "chống lại từ trường ngoài" (đúng: chống lại SỰ BIẾN THIÊN); viết ngược $U_1/U_2 = N_2/N_1$ hoặc gán nhầm cuộn sơ cấp;
nhầm số cực với số cặp cực, quên đổi vòng/phút; tăng U 10 lần tưởng hao phí giảm 10 lần; dùng $U_{\text{tt}}$ hoặc $U$ của thiết bị trong $I = P/U$;
quên nhân đôi chiều dài dây; tính ra $P_{\text{hp}} > P$ mà không thấy vô lí; nghĩ máy biến áp "tạo ra" điện năng; đề xuất dùng điện lưới 220 V cho thí nghiệm học sinh.

## Bài tập mẫu (scripts/data/bai-tap-mau/152.json) — 6 dạng, cấp không giảm. SỐ LIỆU ĐÃ TÍNH (tinh.py), dùng nguyên.
D1 (cấp 1) **Điều kiện xuất hiện và chiều dòng cảm ứng (định tính).** Cuộn dây kín nối điện kế, đầu A hướng về cực Bắc của nam châm thẳng đồng trục.
   (a) Đưa nam châm lại gần: có dòng; A thành cực **Bắc** (đẩy nam châm), nhìn từ phía nam châm dòng chạy **ngược** chiều kim đồng hồ.
   (b) Giữ yên trong lòng cuộn dây: không có dòng. (c) Kéo ra xa: có dòng, A thành cực **Nam** (hút), dòng **cùng** chiều kim đồng hồ (nhìn từ nam châm).
   (d) Quay nam châm quanh trục dọc của chính nó: KHÔNG có dòng. (e) Thay nam châm bằng nam châm điện có khoá K: đóng K — dòng thoáng qua;
   giữ K đóng — không; ngắt K — dòng thoáng qua ngược chiều lúc đóng. Hình SVG: cuộn dây + nam châm, đường sức nét đứt; mỗi ý một dòng. topic: "Từ thông qua khung dây".
D2 (cấp 1–2) **Máy phát xoay chiều $f = np$.** (a) Máy thuỷ điện có rôto 6 cặp cực, phát 50 Hz ⇒ $n \approx 8{,}33$ vòng/s $= 500$ vòng/phút.
   (b) Tuabin chậm lại còn 480 vòng/phút ⇒ $f = 48$ Hz (lệch lưới, phải tăng lưu lượng nước). (c) Dinamô xe đạp: núm đường kính 2 cm lăn không trượt
   trên lốp, xe đi 18 km/h (5 m/s), nam châm 4 cực ⇒ $p = 2$, $n = \dfrac{v}{\pi d} \approx 79{,}6$ vòng/s, $f \approx 159$ Hz (nếu nhầm $p = 4$ ⇒ 318 Hz).
   (d) Lưới 50 Hz: dòng đổi chiều 100 lần mỗi giây. topic: "Nguyên tắc tạo ra dòng điện xoay chiều".
D3 (cấp 2) **Máy biến áp: số vòng, dòng điện, quấn nhầm.** Biến áp hạ áp cho 2 đèn 12 V – 24 W mắc song song, sơ cấp 1650 vòng nối 220 V (coi lí tưởng).
   (a) $N_2 = 90$ vòng. (b) $I_2 = 4$ A, $I_1 \approx 0{,}218$ A; nếu máy thực có $H_{\text{BA}} = 94\%$ (đèn vẫn sáng bình thường) ⇒ $I_1 \approx 0{,}232$ A.
   (c) Lấy thêm đầu ra 6 V: rút đầu dây ở vòng thứ 45 của cuộn thứ cấp. (d) Lắp nhầm: đưa 220 V vào cuộn 90 vòng ⇒ $U \approx 4033$ V ở cuộn 1650 vòng — nguy hiểm.
   topic: "Máy biến áp".
D4 (cấp 2) **Hao phí truyền tải và tác dụng của việc tăng U.** $P = 600$ kW, $R = 24$ Ω. (a) $U = 15$ kV: $I = 40$ A, $P_{\text{hp}} = 38{,}4$ kW, $H = 93{,}6\%$.
   (b) Tăng lên 60 kV ($k = 4$): $I = 10$ A, $P_{\text{hp}} = 2{,}4$ kW (giảm 16 lần), $H = 99{,}6\%$. (c) Muốn $P_{\text{hp}} \le 1\%P$: $U \ge 37\,947$ V ≈ 37,9 kV,
   tức tăng ít nhất ≈ 2,53 lần so với 15 kV. (d) Nếu giữ 15 kV mà muốn hao phí giảm 16 lần như (b): $R$ còn 1,5 Ω ⇒ tiết diện dây gấp 16 lần (khối lượng kim loại gấp 16) — so sánh.
   topic: "Máy biến áp" (xem "Cần thầy quyết").
D5 (cấp 3) **Đường dây thật: điện trở từ $\rho$, độ giảm thế, chọn tỉ số máy tăng áp.** Nhà máy phát $P = 2$ MW ở $U_0 = 6$ kV; khu dân cư cách 20 km; dây đôi nhôm $S = 70$ mm².
   (a) $R = \rho\dfrac{2\ell}{S} = 16$ Ω. Truyền thẳng ở 6 kV: $I \approx 333$ A, $P_{\text{hp}} \approx 1{,}78$ MW (≈ 89 %), $\Delta U \approx 5333$ V, $U_{\text{tt}} \approx 667$ V — không dùng được.
   (b) Yêu cầu $P_{\text{hp}} \le 2\%P$ ⇒ $U \ge 40$ kV ⇒ máy tăng áp tỉ số $N_2/N_1 \ge 20/3 \approx 6{,}67$; sơ cấp 300 vòng ⇒ thứ cấp ít nhất 2000 vòng.
   (c) Ở 40 kV: $I = 50$ A, $P_{\text{hp}} = 40$ kW, $\Delta U = 800$ V, $U_{\text{tt}} = 39\,200$ V; máy hạ áp cuối đường dây về 400 V cần $N_3/N_4 = 98$.
   (d) Nếu chỉ được dùng 22 kV mà vẫn đòi ≤ 2 %: $R \le 4{,}84$ Ω ⇒ $S \ge 231$ mm² (≈ 3,3 lần dây 70 mm²). topic: "Máy biến áp".
D6 (cấp 4) **Công suất nơi tiêu thụ cho trước — phương trình bậc hai và bẫy "P không đổi".** Đường dây $R = 10$ Ω, đầu dây $U = 10$ kV, nơi tiêu thụ cần $P_{\text{tt}} = 1{,}6$ MW.
   (a) $UI - RI^2 = P_{\text{tt}}$ ⇒ $I^2 - 1000I + 160\,000 = 0$ ⇒ $I = 200$ A hoặc $800$ A. Chọn $I = 200$ A: $P = 2$ MW, $P_{\text{hp}} = 0{,}4$ MW, $H = 80\%$, $\Delta U = 2$ kV, $U_{\text{tt}} = 8$ kV.
   (Nghiệm 800 A: $P = 8$ MW, $H = 20\%$, $U_{\text{tt}} = 2$ kV — vẫn đúng toán nhưng loại vì phí 6,4 MW.)
   (b) Giữ $P_{\text{tt}} = 1{,}6$ MW, muốn $H = 95\%$: $\dfrac{U_2}{U_1} = \sqrt{\dfrac{H_1(1-H_1)}{H_2(1-H_2)}} \approx 1{,}835$ ⇒ $U_2 \approx 18{,}35$ kV
   (kiểm: $P_2 \approx 1{,}684$ MW, $I_2 \approx 91{,}8$ A, $P_2/I_2 \approx 18\,353$ V ✓). Dẫn từ $1-H = \dfrac{PR}{U^2}$ và $P = P_{\text{tt}}/H$.
   (c) Bẫy: coi công suất ĐẦU dây không đổi ⇒ $\sqrt{(1-H_1)/(1-H_2)} = 2$ lần — sai vì $P$ đã thay đổi (từ 2 MW xuống ≈ 1,684 MW). topic: "Máy biến áp".

## Tự luận (tu_luan) — 8 bài dễ → khó, mỗi bài có Hướng dẫn giải trong <details>. Số liệu KHÁC bài tập mẫu và KHÁC docx.
1 (Dễ) Kim nam châm đặt gần đầu ống dây: dùng nắm tay phải tìm cực ống dây khi biết chiều dòng, kim quay đầu nào về ống; đổi chiều dòng thì sao.
2 (Dễ) Khung dây kín tịnh tiến qua vùng từ trường đều (đi vào – nằm hẳn trong – đi ra): giai đoạn nào có dòng cảm ứng, vì sao; nam châm rơi qua vòng nhôm rơi chậm hơn rơi tự do (Lenz).
3 (TB) Biến áp nhiều đầu ra: sơ cấp 1100 vòng, 220 V ⇒ đầu ra 3/6/9/12 V cần 15/30/45/60 vòng; nối nối tiếp cuộn 60 vòng với cuộn 30 vòng cùng chiều quấn ⇒ 18 V, ngược chiều ⇒ 6 V.
4 (TB) Biến áp lí tưởng 2000/100 vòng, 220 V ⇒ 11 V; đèn 11 V – 20 W mắc song song; cầu chì sơ cấp 0,5 A ⇒ $P_1 \le 110$ W ⇒ tối đa 5 đèn ($I_2 \approx 9{,}09$ A, $I_1 \approx 0{,}455$ A; 6 đèn ⇒ 0,545 A, đứt).
5 (TB) $P = 300$ kW, $R = 8$ Ω: ở 6 kV $I = 50$ A, $P_{\text{hp}} = 20$ kW, điện năng hao phí 480 kWh/ngày; ở 30 kV $P_{\text{hp}} = 0{,}8$ kW, 19,2 kWh/ngày; bớt 460,8 kWh/ngày (chỉ kWh, không tính tiền — tránh dạng CĐ05).
6 (Khó) Dây đồng và dây nhôm cùng chiều dài, cùng khối lượng: $R \propto \rho D$ ⇒ $R_{\text{nhôm}}/R_{\text{đồng}} \approx 0{,}50$ (hao phí dây nhôm ≈ một nửa, tiết diện nhôm gấp ≈ 3,3 lần) — giải thích vì sao dây cao thế làm bằng nhôm (lõi thép).
7 (Khó) Đo từ hai đầu: vôn kế đầu dây 6000 V, cuối dây 5700 V; công tơ đầu và cuối chênh 216 kWh sau 24 h ⇒ $P_{\text{hp}} = 9$ kW, $I = 30$ A, $R = 10$ Ω, $P = 180$ kW, $H = 95\%$;
   muốn hao phí còn 1 % (cùng $P$) ⇒ $U \approx 13\,416$ V, tăng $\sqrt5 \approx 2{,}24$ lần.
8 (Nâng cao) Hệ hai máy biến áp: máy phát 200 kW, 1 kV → tăng áp 1:10 → dây $R = 20$ Ω → hạ áp về 220 V: $I = 20$ A, $P_{\text{hp}} = 8$ kW, $H = 96\%$, $\Delta U = 400$ V,
   $U$ vào hạ áp 9600 V ⇒ $N_3/N_4 \approx 43{,}6$; $P_{\text{tt}} = 192$ kW. Bỏ máy tăng áp: $I = 200$ A, $\Delta U = 4000$ V $> 1000$ V ⇒ không thể truyền — biện luận.

## Luyện tập (8 câu, tự chấm, nhãn như đề thật): 4 Phần I (A–D), 2 Phần II (a)–d) Đúng/Sai), 2 Phần III (đáp số).
- I.1 Trường hợp KHÔNG có dòng cảm ứng: nam châm quay quanh trục dọc của chính nó trước cuộn dây đồng trục (nhiễu: đưa lại gần, kéo ra, ngắt khoá nam châm điện).
- I.2 Nắm tay phải: cho chiều dòng trên ống dây (hình SVG), hỏi đầu nào là cực Bắc.
- I.3 Biến áp 1200/60 vòng, $U_1 = 220$ V ⇒ $U_2 = 11$ V (nhiễu 4400 V – viết ngược tỉ số; 22 V; 110 V).
- I.4 Cùng $P$, cùng dây, tăng $U$ 3 lần ⇒ hao phí giảm 9 lần (nhiễu: giảm 3 lần, tăng 9 lần, giảm 6 lần).
- II.1 Máy phát 4 cặp cực, 750 vòng/phút: a) $f = 50$ Hz — Đ; b) dòng đổi chiều 50 lần mỗi giây — S (100); c) máy 2 cặp cực cùng $f$ phải quay 1500 vòng/phút — Đ;
  d) dòng xoay chiều không có tác dụng từ vì đổi chiều liên tục — S.
- II.2 $P = 500$ kW, $U = 25$ kV, $R = 50$ Ω: a) $I = 20$ A — Đ; b) $P_{\text{hp}} = 20$ kW — Đ; c) $H = 98\%$ — S (96 %); d) dùng 50 kV thì hao phí còn 10 kW — S (5 kW).
- III.1 Biến áp lí tưởng 880/48 vòng, 220 V, thứ cấp cấp 2,5 A ⇒ $U_2 = 12$ V, $I_1 \approx 0{,}136$ A. Đáp số: **0,14** (A).
- III.2 $P = 1$ MW, $R = 10$ Ω, hao phí ≤ 4 % ⇒ $U_{\min} \approx 15{,}8$ kV. Đáp số: **15,8** (kV).

## YCCĐ cho "Làm bài tương tự"
KHTN 9 chưa có YCCĐ điện từ trong ngân hàng. Dùng các topic đã có trong ngân hàng (tên tra được trong `scripts/data/bai-tap-mau/125.json`, `126.json`):
"Từ trường của nam châm và của dòng điện", "Từ thông qua khung dây", "Nguyên tắc tạo ra dòng điện xoay chiều", "Ứng dụng hiện tượng cảm ứng điện từ",
"Giá trị hiệu dụng của dòng điện xoay chiều", "Máy biến áp". (id topic chưa tra — agent đăng tra bảng topics theo tên.) Không có topic riêng cho truyền tải.

## Sai sót docx (đã thấy khi rà, không chép sang bài)
- D6: "nguồn xoay chiều **hạ áp an toàn** ... đặt ở $U_1 = 220$ V" — mâu thuẫn (220 V là điện lưới, không phải hạ áp an toàn); trái chính Dạng 7 "không dùng 220 V cho thí nghiệm học sinh".
- G2 c): đề nói $P = 11$ kW là công suất **nơi tiêu thụ (sau máy hạ áp)** nhưng lời giải dùng làm công suất đầu dây ($I = P/U_2$) — lẫn hai đại lượng (đúng như bẫy docx tự nêu).
- G2 b): $U_3 = 220$ V bỏ qua $\Delta U = IR = 10$ V trên dây mà không nói ở đề; tính đúng $U$ vào hạ áp 4390 V ⇒ $U_3 = 219{,}5$ V (tinh.py). Lỗi nhỏ, ghi để bài mới luôn ghi giả thiết.
- Dạng 7 c): suy "vôn trên mỗi vòng" từ $U_2$ đo được để tính số vòng quấn thêm — chỉ gần đúng (hao phí đổi khi đổi số vòng); nếu dùng phải nói "ước lượng".
- Docx dùng "máy biến thế"; KHTN 9 dùng "máy biến áp" — bài mới dùng "máy biến áp".

## Cần thầy quyết
1. Lực từ + quy tắc bàn tay trái (docx Dạng 2): ngoài YCCĐ KHTN 9 và ngoài danh sách việc giao — hiện KHÔNG đưa vào. Có muốn thêm 1 mục ngắn ở II + 1 câu luyện tập không?
2. Chưa có YCCĐ "Truyền tải điện năng đi xa": tạm gắn D4–D6 vào "Máy biến áp" (bài tương tự sẽ lệch về máy biến áp) hay tạo topic mới (cần migration)?
