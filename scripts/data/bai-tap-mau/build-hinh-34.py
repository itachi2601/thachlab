"""Bài tập mẫu Bài 15 "Thực hành: Đo tốc độ truyền âm" (Vật lí 11) — lesson_id 34. 4 dạng. Hình: hinh_34.py.
Chủ đề: dạng 1 gắn 175 (Đặc trưng vật lí và sinh lí của âm); dạng 2–4 gắn 176 (Đo tốc độ truyền âm bằng ống cộng hưởng).
Chỉ dùng kiến thức có trong lý thuyết bài: v = λf, v ≈ 331 + 0,6t, l + e = (2k+1)λ/4, λ = 2(l₂ − l₁), sai số (Δλ = 2(Δl₁ + Δl₂),
Δv/v = Δλ/λ + Δf/f, Δl = độ lệch TB + sai số dụng cụ), L = 10 lg(I/I₀), độ cao–f, độ to–L.
Mục bài tập mẫu hiện rỗng nên không có tự luận cũ. Chạy: python3 scripts/data/bai-tap-mau/build-hinh-34.py (idempotent, review.checked=false)."""
import json, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from hinh_34 import *

J = os.path.join(HERE, "34.json")
ROOT = os.path.abspath(os.path.join(HERE, "../../.."))
TOPICS = {t["id"]: t["name"] for t in json.load(open(os.path.join(ROOT, "scripts/data/question-topics.json"))) if t["lesson_id"] == 34}
T175, T176 = TOPICS[175], TOPICS[176]
lg = math.log10


def near(x, y, tol): return abs(x - y) <= tol


# ═════════════ SỐ LIỆU + TỰ GIẢI ĐỘC LẬP (assert) ═════════════
# Dạng 1: mức cường độ âm
I0 = 1e-12; I1 = 4.0e-7
L1_ = 10 * lg(I1 / I0); L1b = 10 * lg(100 * I1 / I0); I1c = I0 * 10 ** (85 / 10)
assert near(L1_, 56.0, 0.03) and near(L1b, 76.0, 0.03) and near(L1b - L1_, 20, 1e-9) and near(I1c, 3.16e-4, 1e-6)
assert abs(100 * L1_ - L1b) > 100 and abs((L1_ + 100) - L1b) > 10                       # sai: nhân L với 100 / cộng 100 dB khác đáp số
assert abs(I0 * 85 / 10 - I1c) > 1e-5 and abs(I0 * 10 ** 85 - I1c) > 1                  # sai: I = I0·L/10, I = 10^L·I0 khác đáp số
assert abs(10 * lg(I1) - L1_) > 5                                                        # sai: quên chia cho I0
# Dạng 2: dự đoán vị trí cộng hưởng; f = 600 Hz, 15 °C, e = 0,5 cm, ống 67 cm
f2, t2, e2, Lt2 = 600.0, 15.0, 0.005, 0.67
v2 = 331 + 0.6 * t2; lam2 = v2 / f2
l1_2 = lam2 / 4 - e2; l2_2 = 3 * lam2 / 4 - e2; l3_2 = 5 * lam2 / 4 - e2
assert near(v2, 340.0, 1e-9) and near(lam2 * 100, 56.67, 0.01) and near(l1_2 * 100, 13.67, 0.01) and near(l2_2 * 100, 42.0, 0.01) and near(l3_2 * 100, 70.33, 0.01)
assert l2_2 < Lt2 < l3_2                                                                # hai vị trí trong ống, lần ba ngoài ống
assert near(l2_2 - l1_2, lam2 / 2, 1e-12)
assert abs(343 - v2) > 1                                                                 # sai: dùng 343 m/s (bước 1, sai_so 1) khác đáp số
assert abs(lam2 / 4 * 100 - 13.67) > 0.2 and abs(lam2 / 2 * 100 - 13.67) > 10          # sai: quên trừ e / λ/2
assert abs(2 * l1_2 * 100 - 42.0) > 5 and abs((l1_2 + lam2) * 100 - 42.0) > 5          # sai: l2 = 2l1, l1 + λ
assert abs(v2 * f2 - 56.67) > 100 and abs(f2 / v2 - 0.5667) > 1                         # sai: λ = v·f, λ = f/v
# Dạng 3: f = 640 Hz, 28 °C, l1 = 13,0 cm, l2 = 39,9 cm
f3, t3, l1_3, l2_3 = 640.0, 28.0, 13.0, 39.9
lam3 = 2 * (l2_3 - l1_3); v3 = lam3 / 100 * f3; e3 = lam3 / 4 - l1_3; vtk3 = 331 + 0.6 * t3; pc3 = abs(v3 - vtk3) / vtk3 * 100
assert near(lam3, 53.8, 1e-9) and near(v3, 344.32, 1e-6) and near(e3, 0.45, 1e-9) and near(vtk3, 347.8, 1e-9) and near(pc3, 1.0006, 0.001)
assert abs(4 * l1_3 - lam3) > 1 and abs(lam3 * f3 - v3) > 1000 and abs(lam3 / 2 - l1_3 - e3) > 5 and abs(lam3 / 4 + l1_3 - e3) > 5     # sai: 4l1, cm/s, λ/2 − l1
assert abs((l2_3 - l1_3) - lam3 / 2) < 1e-9                                              # l2 − l1 − λ/2 = 0 (cách sai cho 0)
assert near(abs(v3 - 343) / 343 * 100, 0.385, 0.01) and abs(abs(v3 - 343) / 343 * 100 - pc3) > 0.15 and abs(v3 / vtk3 * 100 - pc3) > 90   # sai: dùng 343 (0,39 %), đọc tỉ số (99 %)
assert near(abs(344 - vtk3) / vtk3 * 100, 1.1, 0.01)           # HS làm tròn v = 344 vẫn trong sai số 0,15
assert abs(lam3 / 100 * f3 / 640 - 0.538) < 1e-9
# Dạng 4: bảng 5 lần, f = 400 ± 1 Hz, 30 °C, dụng cụ 0,1 cm
f4, df4, dc4, t4 = 400.0, 1.0, 0.1, 30.0
L1s = [21.5, 21.7, 21.6, 21.8, 21.4]; L2s = [65.2, 65.1, 65.3, 65.2, 65.2]
m1 = sum(L1s) / 5; m2 = sum(L2s) / 5
dm1 = sum(abs(x - m1) for x in L1s) / 5; dm2 = sum(abs(x - m2) for x in L2s) / 5
dl1, dl2 = dm1 + dc4, dm2 + dc4
lam4 = 2 * (m2 - m1); v4 = lam4 / 100 * f4
dlam4 = 2 * (dl1 + dl2); eps4 = dlam4 / lam4 + df4 / f4; dv4 = v4 * eps4; vtk4 = 331 + 0.6 * t4
assert near(m1, 21.6, 1e-9) and near(m2, 65.2, 1e-9) and near(dm1, 0.12, 1e-9) and near(dm2, 0.04, 1e-9)
assert near(dl1, 0.22, 1e-9) and near(dl2, 0.14, 1e-9) and near(lam4, 87.2, 1e-9) and near(v4, 348.8, 1e-9)
assert near(dlam4, 0.72, 1e-9) and near(dlam4 / lam4 * 100, 0.826, 0.001) and near(eps4 * 100, 1.076, 0.001) and near(dv4, 3.753, 0.002)
assert near(vtk4, 349.0, 1e-9) and v4 - dv4 <= vtk4 <= v4 + dv4 and not (v4 - dv4 <= 343 <= v4 + dv4)     # 349 trong khoảng; 343 ngoài
vr = [2 * (b - a) / 100 * f4 for a, b in zip(L1s, L2s)]
assert near(sum(vr) / 5, v4, 1e-9) and all(abs(x - v4) <= dv4 for x in vr) and near(min(vr), 347.2, 1e-9) and near(max(vr), 350.4, 1e-9)
assert abs(2 * (dl2 - dl1) - dlam4) > 0.3 and abs((dlam4 / 2) - dlam4) > 0.3 and abs(2 * (dm1 + dm2) - dlam4) > 0.3   # sai: hiệu / thiếu 2 / thiếu dc
assert abs(v4 * dlam4 / lam4 - dv4) > 0.8 and abs(dlam4 + df4 - dv4) > 0.1                                      # sai: bỏ Δf/f / cộng tuyệt đối
assert abs(4 * m1 - lam4) > 0.3                                                                                    # sai: 4 l1
# Số liệu của mô phỏng mẫu khác đề (không lộ đáp số)
assert not (f2 == 500 or t2 == 20) and not (f3 == 500) and 343.0 != vtk4
assert abs((331 + 0.6 * 20) / 500 / 4 * 100 - 0.5 - 16.7) < 0.1                          # mẫu D2: l1 = 16,7 cm ≠ 13,7 cm của đề

# ═════════════ ĐỀ ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Mức cường độ âm: từ cường độ ra dB, từ dB ra cường độ, và cảm giác của tai", topic=T175,
      problem_html=r"""<p>Trong phòng thực hành, một loa phát âm đơn sắc tần số $800\ \text{Hz}$. Máy đo đặt tại bàn nhóm ghi cường độ âm $I=4{,}0\cdot10^{-7}\ \text{W/m}^2$. Lấy ngưỡng nghe $I_0=10^{-12}\ \text{W/m}^2$.</p><ol type="a"><li>Tính mức cường độ âm $L$ tại bàn nhóm.</li><li>Tăng công suất loa sao cho cường độ âm tại bàn nhóm tăng gấp $100$ lần. Mức cường độ âm lúc này bằng bao nhiêu?</li><li>Ở một bàn khác, máy đo hiện $L=85\ \text{dB}$. Tính cường độ âm tại bàn đó.</li><li>Đổi loa sang tần số $1600\ \text{Hz}$, giữ nguyên mức cường độ âm. Coi độ to chỉ do mức cường độ âm quyết định. Tai nghe thấy âm cao hơn hay thấp hơn, to hơn hay nhỏ hơn?</li></ol>"""),
 dict(label="Dạng 2 · Trung bình · Ống một đầu kín: dự đoán các vị trí cộng hưởng", topic=T176,
      problem_html=r"""<p>Một nhóm chuẩn bị thí nghiệm ống cộng hưởng: ống trụ thẳng đứng, miệng hở, đáy có nước; loa đặt sát miệng ống phát âm đơn sắc tần số $f=600\ \text{Hz}$. Phòng thực hành ở $15\ ^\circ\text{C}$. Bụng sóng nằm cao hơn miệng ống một đoạn $e=0{,}5\ \text{cm}$. Ống dài $67\ \text{cm}$, mặt nước hạ dần từ miệng ống xuống đáy. Chiều dài cột khí $l$ đo từ miệng ống tới mặt nước.</p><ol type="a"><li>Tính tốc độ truyền âm và bước sóng.</li><li>Dự đoán $l_1$ và $l_2$ của hai lần nghe to nhất đầu tiên.</li><li>Trong ống dài $67\ \text{cm}$, có thể nghe được lần to nhất thứ ba không?</li></ol>"""),
 dict(label="Dạng 3 · Trung bình · Từ hai lần cộng hưởng tính bước sóng, tốc độ và đoạn e", topic=T176,
      problem_html=r"""<p>Một nhóm đo tốc độ truyền âm bằng ống cộng hưởng. Âm thoa có tần số $f=640\ \text{Hz}$ (coi chính xác), nhiệt độ phòng $28\ ^\circ\text{C}$. Hạ nước từ từ, nghe to nhất lần thứ nhất khi $l_1=13{,}0\ \text{cm}$ và lần thứ hai khi $l_2=39{,}9\ \text{cm}$ ($l$ đo từ miệng ống tới mặt nước; số liệu minh hoạ).</p><ol type="a"><li>Tính bước sóng $\lambda$ và tốc độ truyền âm $v$ mà nhóm đo được.</li><li>Tính đoạn $e$ mà bụng nằm cao hơn miệng ống.</li><li>Tính tốc độ truyền âm theo nhiệt độ phòng và cho biết kết quả đo lệch bao nhiêu phần trăm so với giá trị đó.</li></ol>"""),
 dict(label="Dạng 4 · Khó · Xử lý bảng số liệu: sai số và so với giá trị tham khảo", topic=T176,
      problem_html=r"""<p>Một nhóm đo tốc độ truyền âm bằng ống cộng hưởng (ống dài $70\ \text{cm}$) trong phòng ở $30\ ^\circ\text{C}$, máy phát $f=400\pm1\ \text{Hz}$. Mỗi lần đo ghi hai vị trí nghe to nhất (số liệu minh hoạ):</p><div class="table-scroll"><table class="tl-table"><thead><tr><th>Lần đo</th><th>$l_1\ (\text{cm})$</th><th>$l_2\ (\text{cm})$</th></tr></thead><tbody><tr><td>1</td><td>$21{,}5$</td><td>$65{,}2$</td></tr><tr><td>2</td><td>$21{,}7$</td><td>$65{,}1$</td></tr><tr><td>3</td><td>$21{,}6$</td><td>$65{,}3$</td></tr><tr><td>4</td><td>$21{,}8$</td><td>$65{,}2$</td></tr><tr><td>5</td><td>$21{,}4$</td><td>$65{,}2$</td></tr></tbody></table></div><p>Thước chia tới $1\ \text{mm}$, lấy sai số dụng cụ $\Delta l_{\text{dc}}=0{,}1\ \text{cm}$. Sai số tuyệt đối của mỗi giá trị trung bình $\bar l$ bằng độ lệch tuyệt đối trung bình cộng $\Delta l_{\text{dc}}$.</p><ol type="a"><li>Tính bước sóng trung bình $\bar\lambda$ và tốc độ truyền âm trung bình $\bar v$.</li><li>Tính $\Delta\lambda$ và $\Delta v$, viết kết quả dạng $v=\bar v\pm\Delta v$.</li><li>So với giá trị tham khảo tính theo nhiệt độ phòng, phép đo có phù hợp không?</li></ol>"""),
]

# ═════════════ PHÂN TÍCH ĐỀ (cột 3: khái niệm / điều kiện, không ghi kết luận hay hướng giải của bước bị giấu) ═════════════
ANALYSIS = [
 [(r'"loa phát âm đơn sắc tần số $800$ Hz"', r"$f=800$ Hz", "Độ cao của âm ứng với tần số"),
  (r'"cường độ âm $I=4{,}0\cdot10^{-7}$ W/m²"', r"$I=4{,}0\cdot10^{-7}$ W/m²", "Độ to ứng với mức cường độ âm $L$ (dB)"),
  (r'"ngưỡng nghe $I_0=10^{-12}$ W/m²"', r"$I_0=10^{-12}$ W/m²", "⚠ $I_0$ là mốc so sánh; $I$ và $I_0$ phải cùng đơn vị, $\\lg$ là logarit thập phân"),
  (r'"tăng gấp $100$ lần"', r"$I'=100\,I$", "Liên hệ giữa $L$ và $I$ qua logarit"),
  (r'"máy đo hiện $L=85$ dB"', r"$L=85$ dB", "Đảo lại để tìm $I$"),
  (r'"đổi loa sang $1600$ Hz, giữ nguyên mức cường độ âm"', r"$f$ gấp đôi; $L$ không đổi", "Mỗi cảm giác của tai ứng với một đại lượng vật lí"),
  (r'"tính $L$ … mức … cường độ … cao hơn hay thấp hơn, to hơn hay nhỏ hơn"', r"Cần $L$, $L'$, $I$ và so sánh cảm giác", "Đại lượng cần tìm")],
 [(r'"ống trụ thẳng đứng, miệng hở, đáy có nước; loa sát miệng ống phát âm đơn sắc $f=600$ Hz"', r"$f=600$ Hz", "Mặt nước là nút, miệng ống là bụng; $v=\\lambda f$"),
  (r'"phòng thực hành ở $15\ ^\circ$C"', r"$t=15\ ^\circ$C", "Tốc độ âm trong không khí phụ thuộc nhiệt độ"),
  (r'"bụng sóng nằm cao hơn miệng ống đoạn $e=0{,}5$ cm"', r"$e=0{,}5$ cm", "⚠ $l$ đo từ miệng ống tới mặt nước, còn bụng cao hơn miệng ống đoạn $e$"),
  (r'"ống dài $67$ cm, mặt nước hạ dần"', r"Chiều dài ống $67$ cm", "⚠ Chỉ gặp cộng hưởng ở các vị trí nằm trong ống"),
  (r'"tốc độ truyền âm và bước sóng"', r"Cần $v$, $\lambda$", "Đại lượng cần tìm"),
  (r'"$l_1$ và $l_2$ của hai lần nghe to nhất đầu tiên"', r"Cần $l_1$, $l_2$", "Đại lượng cần tìm: từ nút tới bụng liền kề là một phần mấy bước sóng?"),
  (r'"có thể nghe được lần to nhất thứ ba không"', r"Cần so vị trí lần ba với chiều dài ống", "Lần thứ ba ứng với $k$ bằng mấy? Vị trí đó có nằm trong ống không?")],
 [(r'"âm thoa có tần số $f=640$ Hz (coi chính xác)"', r"$f=640$ Hz", "Nguồn quyết định tần số; $v=\\lambda f$"),
  (r'"nhiệt độ phòng $28\ ^\circ$C"', r"$t=28\ ^\circ$C", "⚠ Giá trị tham khảo của $v$ phụ thuộc nhiệt độ"),
  (r'"nghe to nhất lần thứ nhất khi $l_1=13{,}0$ cm"', r"$l_1=13{,}0$ cm", "Lần thứ nhất ứng với $k$ bằng mấy?"),
  (r'"lần thứ hai khi $l_2=39{,}9$ cm"', r"$l_2=39{,}9$ cm", "Lần thứ hai ứng với $k$ bằng mấy?"),
  (r'"$l$ đo từ miệng ống tới mặt nước"', r"Chưa biết $e$", "⚠ Bụng cao hơn miệng ống một đoạn $e$ chưa biết"),
  (r'"tính bước sóng $\lambda$ và tốc độ truyền âm $v$"', r"Cần $\lambda$, $v$", "Hiệu hai lần cộng hưởng liên tiếp bằng mấy lần $\\lambda$? Phép trừ làm $e$ biến mất ra sao?"),
  (r'"tính đoạn $e$"', r"Cần $e$", "Dùng điều kiện cộng hưởng của một lần cụ thể"),
  (r'"lệch bao nhiêu phần trăm so với giá trị theo nhiệt độ phòng"', r"Cần sai lệch tương đối", "Giá trị tham khảo lấy từ đâu? Chia cho đại lượng nào?")],
 [(r'"phòng ở $30\ ^\circ$C"', r"$t=30\ ^\circ$C", "⚠ Giá trị tham khảo của $v$ phụ thuộc nhiệt độ phòng"),
  (r'"máy phát $f=400\pm1$ Hz"', r"$f=400$ Hz; $\Delta f=1$ Hz", "Sai số của $f$ góp vào sai số của $v$ thế nào?"),
  (r'"mỗi lần đo ghi hai vị trí nghe to nhất" (5 lần)', r"5 cặp $(l_1,\,l_2)$", "Giá trị trung bình; độ lệch tuyệt đối trung bình"),
  (r'"sai số dụng cụ $\Delta l_{\text{dc}}=0{,}1$ cm"', r"$\Delta l_{\text{dc}}=0{,}1$ cm", "⚠ Mỗi $\\Delta\\bar l$ = độ lệch tuyệt đối trung bình + sai số dụng cụ"),
  (r'"tính $\bar\lambda$ và $\bar v$"', r"Cần $\bar\lambda$, $\bar v$", "Hiệu hai lần cộng hưởng liên tiếp bằng mấy lần $\\lambda$?"),
  (r'"tính $\Delta\lambda$ và $\Delta v$, viết $v=\bar v\pm\Delta v$"', r"Cần $\Delta\lambda$, $\Delta v$", "Tổng hoặc hiệu thì cộng loại sai số nào? Tích hoặc thương thì cộng loại nào?"),
  (r'"so với giá trị tham khảo theo nhiệt độ phòng"', "Cần kết luận có phù hợp không", "Giá trị tham khảo lấy ở đâu? So với khoảng nào?")],
]

# ═════════════ LỜI GIẢI ═════════════
R1 = ["<strong>Khái niệm:</strong> độ cao ứng với tần số $f$; độ to ứng với mức cường độ âm $L$ (dB).",
      r"<strong>Công thức:</strong> $L=10\lg\dfrac{I}{I_0}$ với $I_0=10^{-12}\ \text{W/m}^2$ (ngưỡng nghe).",
      "Mỗi lần $I$ gấp $10$ lần thì $L$ tăng $10\\ \\text{dB}$.",
      "⚠ <strong>Điều kiện:</strong> $I$ và $I_0$ cùng đơn vị; $\\lg$ là logarit thập phân."]
R2 = [r"<strong>Khái niệm:</strong> mặt nước là nút, bụng cao hơn miệng ống một đoạn $e$; $l$ đo từ miệng ống tới mặt nước.",
      r"<strong>Điều kiện cộng hưởng:</strong> $l+e=(2k+1)\dfrac{\lambda}{4}$, $k=0,1,2,\dots$",
      r"Tốc độ âm: $v\approx331+0{,}6\,t$ · bước sóng: $\lambda=\dfrac{v}{f}$",
      "⚠ <strong>Điều kiện:</strong> chỉ có cộng hưởng ở những $l$ nằm trong ống."]
R3 = [r"<strong>Khái niệm:</strong> hai lần cộng hưởng liên tiếp: $l_1+e=\dfrac{\lambda}{4}$ và $l_2+e=\dfrac{3\lambda}{4}$.",
      r"Trừ vế với vế, $e$ mất đi: $\lambda=2\,(l_2-l_1)$ · $v=\lambda f$",
      r"Giá trị tham khảo: $v\approx331+0{,}6\,t$ · sai lệch tương đối $=\dfrac{|v-v_{\text{tk}}|}{v_{\text{tk}}}$",
      "⚠ <strong>Điều kiện:</strong> $l$ đo từ miệng ống; so ở đúng nhiệt độ phòng."]
R4 = [r"<strong>Khái niệm:</strong> $\bar\lambda=2(\bar l_2-\bar l_1)$ · $\bar v=\bar\lambda f$.",
      r"$\Delta\bar l=$ độ lệch tuyệt đối trung bình $+\ \Delta l_{\text{dc}}$.",
      r"Hiệu: cộng sai số tuyệt đối, $\Delta\lambda=2(\Delta l_1+\Delta l_2)$ · tích: cộng sai số tỉ đối, $\dfrac{\Delta v}{\bar v}=\dfrac{\Delta\lambda}{\bar\lambda}+\dfrac{\Delta f}{f}$.",
      r"Phù hợp khi giá trị tham khảo $v\approx331+0{,}6\,t$ nằm trong $\bar v\pm\Delta v$.",
      "⚠ <strong>Điều kiện:</strong> so với giá trị tham khảo ở đúng nhiệt độ phòng, không dùng số của nhiệt độ khác."]

SOLS = [
 sol(R1, [
  ("Mức cường độ âm tại bàn nhóm", [M(r"L=10\lg\dfrac{I}{I_0}=10\lg\dfrac{4{,}0\cdot10^{-7}}{10^{-12}}"), M(r"L=10\lg\left(4{,}0\cdot10^{5}\right)"), A(r"L\approx56{,}0\ \text{dB}")]),
  ("Khi cường độ gấp 100 lần", [P(r"$I'=100\,I$, tính lại với $I'$:"), M(r"L'=10\lg\dfrac{100\,I}{I_0}=10\lg100+10\lg\dfrac{I}{I_0}=20+56{,}0"), A(r"L'\approx76{,}0\ \text{dB}"), P("Cường độ gấp $100$ lần chỉ làm $L$ tăng thêm $20\\ \\text{dB}$.")]),
  ("Từ mức ra cường độ", [P(r"Đảo công thức: $\dfrac{I}{I_0}=10^{L/10}$."), M(r"I=I_0\cdot10^{8{,}5}=10^{-12}\cdot10^{8{,}5}=10^{-3{,}5}"), A(r"I\approx3{,}16\cdot10^{-4}\ \text{W/m}^2")]),
  ("Cảm giác của tai khi đổi tần số", [P("Độ cao ứng với tần số: $f$ gấp đôi nên âm nghe <strong>cao hơn</strong> (thanh hơn)."), P("Độ to ứng với mức cường độ âm: $L$ giữ nguyên nên độ to <strong>không đổi</strong>."), A("T:Cao hơn, độ to như nhau.")]),
  ("Kiểm tra", [P(r"$L=56{,}0\ \text{dB}$, $76{,}0\ \text{dB}$, $85\ \text{dB}$ đều nằm giữa $0\ \text{dB}$ (ngưỡng nghe) và cỡ $130\ \text{dB}$ (ngưỡng đau) ✓"), P(r"Bàn có $85\ \text{dB}$ to hơn bàn có $56{,}0\ \text{dB}$ nên cường độ phải lớn hơn $4{,}0\cdot10^{-7}\ \text{W/m}^2$: $3{,}16\cdot10^{-4}$ ✓")])],
  [r"a) $L\approx56{,}0\ \text{dB}$", r"b) $L'\approx76{,}0\ \text{dB}$ (tăng $20\ \text{dB}$)", r"c) $I\approx3{,}16\cdot10^{-4}\ \text{W/m}^2$", "d) Cao hơn; độ to không đổi"],
  "Nhận dạng: đề cho <strong>cường độ âm kèm $I_0$</strong> hoặc cho <strong>mức dB</strong> → dùng $L=10\\lg\\dfrac{I}{I_0}$; độ cao ứng với $f$, độ to ứng với $L$."),
 sol(R2, [
  ("Tốc độ truyền âm", [M(r"v\approx331+0{,}6\,t=331+0{,}6\cdot15"), A(r"v\approx340\ \text{m/s}")]),
  ("Bước sóng", [M(r"\lambda=\dfrac{v}{f}=\dfrac{340}{600}\approx0{,}567\ \text{m}"), A(r"\lambda\approx56{,}7\ \text{cm}")]),
  ("Lần cộng hưởng thứ nhất ($k=0$)", [P(r"Điều kiện cộng hưởng với $k=0$: $l_1+e=\dfrac{\lambda}{4}$."), M(r"l_1=\dfrac{\lambda}{4}-e=\dfrac{56{,}7}{4}-0{,}5"), A(r"l_1\approx13{,}7\ \text{cm}")]),
  ("Lần cộng hưởng thứ hai ($k=1$)", [P(r"Với $k=1$: $l_2+e=\dfrac{3\lambda}{4}$."), M(r"l_2=\dfrac{3\lambda}{4}-e=\dfrac{3\cdot56{,}7}{4}-0{,}5"), A(r"l_2\approx42{,}0\ \text{cm}")]),
  ("Lần cộng hưởng thứ ba trong ống 67 cm", [P(r"Với $k=2$: $l_3+e=\dfrac{5\lambda}{4}$."), M(r"l_3=\dfrac{5\lambda}{4}-e=\dfrac{5\cdot56{,}7}{4}-0{,}5\approx70{,}3\ \text{cm}"), M(r"l_3=70{,}3\ \text{cm}\gt67\ \text{cm}"), A("T:<strong>Không</strong> nghe được lần to nhất thứ ba: vị trí đó nằm sâu hơn đáy ống.")]),
  ("Kiểm tra", [P(r"$l_2-l_1\approx28{,}3\ \text{cm}=\dfrac{\lambda}{2}$ ✓ ($e$ triệt tiêu khi lấy hiệu)."), P(r"Trong ống chỉ có hai vị trí $l_1$, $l_2$, đều nhỏ hơn $67\ \text{cm}$ ✓")])],
  [r"a) $v\approx340\ \text{m/s}$; $\lambda\approx56{,}7\ \text{cm}$", r"b) $l_1\approx13{,}7\ \text{cm}$; $l_2\approx42{,}0\ \text{cm}$", "c) Không: lần thứ ba ở cỡ $70\\ \\text{cm}$, dài hơn ống"],
  "Nhận dạng: đề cho <strong>ống một đầu kín, tần số và nhiệt độ</strong>, hỏi <strong>vị trí nghe to nhất</strong> → $v$ theo nhiệt độ, $\\lambda=\\dfrac{v}{f}$, rồi $l+e=(2k+1)\\dfrac{\\lambda}{4}$."),
 sol(R3, [
  ("Bước sóng từ hiệu hai lần to", [M(r"l_2-l_1=\dfrac{\lambda}{2}\Rightarrow\lambda=2\,(l_2-l_1)=2\,(39{,}9-13{,}0)"), A(r"\lambda=53{,}8\ \text{cm}")]),
  ("Tốc độ truyền âm đo được", [P(r"Đổi $\lambda=0{,}538\ \text{m}$."), M(r"v=\lambda f=0{,}538\cdot640"), A(r"v\approx344{,}3\ \text{m/s}")]),
  ("Đoạn e", [P(r"Lần thứ nhất: $l_1+e=\dfrac{\lambda}{4}$."), M(r"e=\dfrac{\lambda}{4}-l_1=\dfrac{53{,}8}{4}-13{,}0=13{,}45-13{,}0"), A(r"e\approx0{,}45\ \text{cm}")]),
  ("So với giá trị theo nhiệt độ phòng", [M(r"v_{\text{tk}}\approx331+0{,}6\cdot28=347{,}8\ \text{m/s}"), M(r"\dfrac{|v-v_{\text{tk}}|}{v_{\text{tk}}}=\dfrac{|344{,}3-347{,}8|}{347{,}8}"), A(r"\approx1{,}0\,\%")]),
  ("Kiểm tra", [P(r"$e\approx0{,}45\ \text{cm}$ là cỡ $0{,}6$ lần bán kính của ống có đường kính trong cỡ $1{,}5\ \text{cm}$: hợp lí ✓"), P(r"Độ lệch cỡ $1\,\%$ là nhỏ nên phép đo phù hợp với giá trị tham khảo ở $28\ ^\circ\text{C}$ ✓")])],
  [r"a) $\lambda=53{,}8\ \text{cm}$; $v\approx344{,}3\ \text{m/s}$", r"b) $e\approx0{,}45\ \text{cm}$", r"c) $v_{\text{tk}}\approx347{,}8\ \text{m/s}$; lệch cỡ $1{,}0\,\%$"],
  "Nhận dạng: đề cho <strong>hai lần nghe to nhất liên tiếp</strong> $l_1$, $l_2$ → $\\lambda=2(l_2-l_1)$ ($e$ triệt tiêu); muốn biết $e$ thì dùng điều kiện cộng hưởng của một lần."),
 sol(R4, [
  ("Bước sóng trung bình", [P(r"$\bar l_1=\dfrac{21{,}5+21{,}7+21{,}6+21{,}8+21{,}4}{5}=21{,}6\ \text{cm}$; $\bar l_2=65{,}2\ \text{cm}$."), M(r"\bar\lambda=2\,(\bar l_2-\bar l_1)=2\,(65{,}2-21{,}6)"), A(r"\bar\lambda=87{,}2\ \text{cm}")]),
  ("Tốc độ trung bình", [P(r"Đổi $\bar\lambda=0{,}872\ \text{m}$."), M(r"\bar v=\bar\lambda f=0{,}872\cdot400"), A(r"\bar v=348{,}8\ \text{m/s}")]),
  ("Sai số của bước sóng", [P(r"Độ lệch của $l_1$: $0{,}1;\ 0{,}1;\ 0;\ 0{,}2;\ 0{,}2$, trung bình $0{,}12\ \text{cm}$, nên $\Delta\bar l_1=0{,}12+0{,}1=0{,}22\ \text{cm}$."), P(r"Độ lệch của $l_2$: $0;\ 0{,}1;\ 0{,}1;\ 0;\ 0$, trung bình $0{,}04\ \text{cm}$, nên $\Delta\bar l_2=0{,}04+0{,}1=0{,}14\ \text{cm}$."), M(r"\Delta\lambda=2\,(\Delta\bar l_1+\Delta\bar l_2)=2\,(0{,}22+0{,}14)"), A(r"\Delta\lambda=0{,}72\ \text{cm}")]),
  ("Sai số của tốc độ", [M(r"\dfrac{\Delta v}{\bar v}=\dfrac{\Delta\lambda}{\bar\lambda}+\dfrac{\Delta f}{f}=\dfrac{0{,}72}{87{,}2}+\dfrac{1}{400}\approx0{,}0083+0{,}0025"), M(r"\Delta v\approx348{,}8\cdot0{,}0108"), A(r"\Delta v\approx3{,}8\ \text{m/s}"), P(r"Kết quả: $v=348{,}8\pm3{,}8\ \text{m/s}$, tức khoảng $345{,}0$ đến $352{,}6\ \text{m/s}$.")]),
  ("So với giá trị tham khảo", [P(r"Phòng $30\ ^\circ\text{C}$: $v_{\text{tk}}\approx331+0{,}6\cdot30=349\ \text{m/s}$."), M(r"345{,}0\ \text{m/s}\lt349\ \text{m/s}\lt352{,}6\ \text{m/s}"), A("T:Giá trị tham khảo nằm trong khoảng đo: phép đo <strong>phù hợp</strong>.")]),
  ("Kiểm tra", [P(r"Tốc độ từng lần đo: $349{,}6;\ 347{,}2;\ 349{,}6;\ 347{,}2;\ 350{,}4\ \text{m/s}$, đều nằm trong $\bar v\pm\Delta v$ ✓"), P(r"Nếu so với $343\ \text{m/s}$ của $20\ ^\circ\text{C}$ thì giá trị đó nằm ngoài khoảng đo và rút ra kết luận sai: phải dùng nhiệt độ phòng ✓")])],
  [r"a) $\bar\lambda=87{,}2\ \text{cm}$; $\bar v=348{,}8\ \text{m/s}$", r"b) $\Delta\lambda=0{,}72\ \text{cm}$; $\Delta v\approx3{,}8\ \text{m/s}$; $v=348{,}8\pm3{,}8\ \text{m/s}$", r"c) Phù hợp: $v_{\text{tk}}=349\ \text{m/s}$ nằm trong khoảng đo"],
  "Nhận dạng: đề cho <strong>bảng nhiều lần đo kèm sai số dụng cụ</strong>, hỏi <strong>kết quả và so với tham khảo</strong> → trung bình, cộng sai số (hiệu: tuyệt đối; tích: tỉ đối), so khoảng $\\bar v\\pm\\Delta v$ ở đúng nhiệt độ phòng."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC ═════════════
STEPS = [
 dict(nhan_dang="Thấy <b>cường độ âm I (W/m²)</b> hoặc <b>mức … dB</b> trong đề → nghĩ tới <b>L = 10 lg(I/I₀)</b>.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Mức cường độ âm", "Mức cường độ âm tại bàn nhóm bằng bao nhiêu dB?", 56.0, "dB", 0.3,
       loi="Quên chia $I$ cho $I_0$ (lấy logarit của chính $I$), hoặc quên hệ số $10$ trước $\\lg$."),
  buoc("Cường độ tăng gấp 100 lần", "Sau khi cường độ tăng gấp $100$ lần, mức cường độ âm bằng bao nhiêu dB?", 76.0, "dB", 0.3,
       loi="Cho rằng $I$ tăng bao nhiêu lần thì $L$ tăng bấy nhiêu lần, hoặc cộng thẳng số lần vào $L$.",
       ke=[("Tính lại $L'=10\\lg\\dfrac{I'}{I_0}$ với $I'$ mới (hoặc cộng thêm $10\\lg100$)", True),
           ("Nhân $L$ với $100$ vì cường độ tăng gấp $100$", "$L$ là logarit của tỉ số $I/I_0$, không tỉ lệ thuận với $I$: nhân $I$ lên chỉ cộng thêm một lượng vào $L$."),
           ("Cộng thêm $100\\ \\text{dB}$ vào $L$", "Lượng cộng thêm là $10\\lg100$ chứ không phải số lần $100$.")]),
  buoc("Từ mức ra cường độ", "Ở bàn khác có $L=85\\ \\text{dB}$. Cường độ âm tại đó bằng bao nhiêu (tính theo đơn vị $10^{-4}\\ \\text{W/m}^2$)?", 3.16, "×10⁻⁴ W/m²", 0.06,
       loi="Đảo sai công thức logarit (chia thay vì luỹ thừa) hoặc quên nhân với $I_0$ sau khi luỹ thừa.",
       ke=[("Đảo công thức: $\\dfrac{I}{I_0}=10^{L/10}$ rồi nhân với $I_0$", True),
           ("Lấy $I=I_0\\cdot\\dfrac{L}{10}$", "$L$ là logarit của $I/I_0$ nên đảo bằng luỹ thừa $10$, không phải phép chia."),
           ("Lấy $I=10^{L}\\cdot I_0$", "Hệ số đứng trước $\\lg$ là $10$, nên số mũ là $L/10$, không phải $L$.")]),
  buoc("Cảm giác của tai khi đổi tần số", "Giữ nguyên $L$, tăng $f$ gấp đôi: tai nghe thấy thế nào?",
       lua_chon=[("Cao hơn, độ to không đổi", True),
                 ("To hơn vì tần số lớn", "Độ to ứng với mức cường độ âm $L$; $L$ không đổi thì độ to không đổi."),
                 ("Thấp hơn vì bước sóng ngắn lại", "Độ cao ứng với tần số: $f$ lớn thì nghe cao (thanh) hơn.")],
       loi="Lẫn độ cao với độ to: cho rằng tần số lớn thì nghe to hơn.",
       ke=[("Ghép từng cảm giác (độ cao, độ to) với đại lượng vật lí tương ứng", True),
           ("Chỉ xét bước sóng vì $f$ tăng thì $\\lambda$ đổi", "Bước sóng không phải là cảm giác của tai; độ cao do tần số quyết định."),
           ("Tính lại $L$ với tần số mới bằng công thức mức cường độ âm", "Công thức của $L$ không chứa tần số, và đề đã giữ nguyên $L$.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang="Thấy <b>ống một đầu kín</b> hỏi <b>vị trí nghe to nhất</b> → nghĩ tới <b>l + e = (2k+1)λ/4</b>.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Tốc độ truyền âm", "Tốc độ truyền âm ở $15\\ ^\\circ\\text{C}$ bằng bao nhiêu m/s?", 340, "m/s", 1,
       loi="Lấy giá trị của $20\\ ^\\circ\\text{C}$ thay vì tính theo nhiệt độ phòng của đề."),
  buoc("Bước sóng", "Bước sóng $\\lambda$ bằng bao nhiêu cm?", 56.7, "cm", 0.3,
       loi="Nhân $v$ với $f$ thay vì chia, hoặc quên đổi từ mét sang cm.",
       ke=[("Từ $v=\\lambda f$ suy ra $\\lambda=\\dfrac{v}{f}$", True),
           ("Lấy $\\lambda=v\\cdot f$", "Từ $v=\\lambda f$ suy ra $\\lambda=v/f$, không phải tích."),
           ("Lấy $\\lambda=\\dfrac{f}{v}$", "Đảo tỉ số nên đơn vị là $\\text{Hz}/(\\text{m/s})$, không phải mét.")]),
  buoc("Lần cộng hưởng thứ nhất", "Chiều dài cột khí $l_1$ bằng bao nhiêu cm?", 13.7, "cm", 0.2,
       loi="Bỏ qua $e$ (lấy $l_1=\\dfrac{\\lambda}{4}$) hoặc cộng $e$ thay vì trừ.",
       ke=[("Từ $l_1+e=\\dfrac{\\lambda}{4}$ suy ra $l_1$", True),
           ("Lấy $l_1=\\dfrac{\\lambda}{2}$ vì lần đầu ứng với nửa bước sóng", "Từ nút (mặt nước) tới bụng liền kề chỉ là $\\lambda/4$; $\\lambda/2$ là khoảng cách giữa hai lần cộng hưởng liên tiếp."),
           ("Lấy $l_1=\\dfrac{\\lambda}{4}$ vì bụng nằm đúng ở miệng ống", "Bụng cao hơn miệng ống một đoạn $e$, nên cột khí đo từ miệng ngắn hơn $\\lambda/4$ đúng đoạn $e$.")]),
  buoc("Lần cộng hưởng thứ hai", "Chiều dài cột khí $l_2$ bằng bao nhiêu cm?", 42.0, "cm", 0.3,
       loi="Quên trừ $e$ (lấy $l_2=\\dfrac{3\\lambda}{4}$) hoặc dùng hệ số của lần thứ nhất.",
       ke=[("Từ $l_2+e=\\dfrac{3\\lambda}{4}$ ($k=1$) suy ra $l_2$", True),
           ("Lấy $l_2=2\\,l_1$ vì gấp đôi lần đầu", "Hai lần cộng hưởng liên tiếp cách nhau $\\lambda/2$ và còn phần $e$, nên $l_2$ không bằng $2\\,l_1$."),
           ("Lấy $l_2=l_1+\\lambda$ vì cách nhau một bước sóng", "Hai lần cộng hưởng liên tiếp cách nhau $\\lambda/2$, không phải cả bước sóng.")]),
  buoc("Lần thứ ba trong ống 67 cm", "Trong ống dài $67\\ \\text{cm}$ có nghe được lần to nhất thứ ba không?",
       lua_chon=[("Không: vị trí cộng hưởng thứ ba nằm sâu hơn đáy ống", True),
                 ("Có: cứ hạ thêm nước là còn nghe thêm lần to nữa", "Chỉ có cộng hưởng ở những vị trí $l$ rời rạc; hết chiều dài ống thì không còn vị trí nào."),
                 ("Có: lần thứ ba cách lần thứ hai chỉ $\\lambda/4$", "Hai lần liên tiếp cách nhau $\\lambda/2$ chứ không phải $\\lambda/4$.")],
       loi="Không so vị trí lần ba với chiều dài ống, hoặc coi lần ba cách lần hai $\\lambda/4$.",
       ke=[("Tính $l_3$ từ $l_3+e=\\dfrac{5\\lambda}{4}$ rồi so với chiều dài ống", True),
           ("Chia chiều dài ống cho $\\lambda/2$ để đếm số lần", "Lần đầu không ở cách miệng ống $\\lambda/2$ mà ở $\\lambda/4-e$, nên cách chia này sai."),
           ("Cho rằng ống càng dài thì còn nhiều lần, không cần tính", "Số lần cộng hưởng bị giới hạn bởi chiều dài ống; phải tính $l_3$ rồi so sánh.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang="Thấy <b>hai lần nghe to nhất liên tiếp</b> $l_1$, $l_2$ → nghĩ tới <b>λ = 2(l₂ − l₁)</b>, e triệt tiêu.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Bước sóng từ hiệu hai lần to", "Bước sóng $\\lambda$ bằng bao nhiêu cm?", 53.8, "cm", 0.2,
       loi="Dùng $\\lambda=4\\,l_1$ (bỏ qua $e$), hoặc lấy hiệu hai vị trí mà quên nhân $2$."),
  buoc("Tốc độ truyền âm đo được", "Tốc độ truyền âm mà nhóm đo được bằng bao nhiêu m/s?", 344.3, "m/s", 0.6,
       loi="Giữ $\\lambda$ ở đơn vị cm khi nhân với $f$, hoặc lấy thương thay vì tích.",
       ke=[("Đổi $\\lambda$ ra mét rồi lấy $v=\\lambda f$", True),
           ("Lấy $v=\\lambda f$ với $\\lambda$ giữ nguyên đơn vị cm", "Kết quả sẽ có đơn vị cm/s; phải đổi $\\lambda$ ra mét để có m/s."),
           ("Lấy $v=\\dfrac{\\lambda}{f}$", "$v=\\lambda f$ chứ không phải thương; thương có đơn vị mét chia hertz, không phải m/s.")]),
  buoc("Đoạn e", "Đoạn $e$ bằng bao nhiêu cm?", 0.45, "cm", 0.05,
       loi="Lấy nhầm cặp: ghép $l_2$ với $\\dfrac{\\lambda}{4}$ hoặc $l_1$ với $\\dfrac{3\\lambda}{4}$.",
       ke=[("Dùng lần thứ nhất: $e=\\dfrac{\\lambda}{4}-l_1$", True),
           ("Lấy $e=\\dfrac{\\lambda}{2}-l_1$ vì lần thứ nhất ứng với nửa bước sóng", "Lần thứ nhất ứng với $\\lambda/4$ giữa nút và bụng; $\\lambda/2$ là khoảng cách giữa hai lần cộng hưởng."),
           ("Lấy $e=\\dfrac{\\lambda}{4}+l_1$", "Bụng cao hơn miệng ống nên cột khí $l_1$ ngắn hơn $\\dfrac{\\lambda}{4}$: $e=\\dfrac{\\lambda}{4}-l_1$, không phải tổng.")]),
  buoc("So với giá trị theo nhiệt độ phòng", "Kết quả đo lệch bao nhiêu phần trăm so với giá trị tính theo nhiệt độ phòng?", 1.0, "%", 0.15,
       loi="Lấy $343\\ \\text{m/s}$ làm giá trị tham khảo dù phòng không ở $20\\ ^\\circ\\text{C}$, hoặc đọc tỉ số $v/v_{\\text{tk}}$ thành độ lệch.",
       ke=[("Tính $v_{\\text{tk}}=331+0{,}6\\,t$ rồi lấy $\\dfrac{|v-v_{\\text{tk}}|}{v_{\\text{tk}}}$", True),
           ("Dùng $v_{\\text{tk}}=343\\ \\text{m/s}$ vì đó là giá trị thường nhớ", "$343\\ \\text{m/s}$ ứng với $20\\ ^\\circ\\text{C}$; phòng nóng hơn thì giá trị tham khảo lớn hơn."),
           ("Lấy tỉ số $\\dfrac{v}{v_{\\text{tk}}}$ rồi đọc luôn thành phần trăm lệch", "Tỉ số cho biết $v$ bằng bao nhiêu phần trăm của $v_{\\text{tk}}$; độ lệch là phần chênh khỏi $100\\,\\%$.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang="Thấy <b>bảng nhiều lần đo, sai số dụng cụ</b> → nghĩ tới <b>trung bình, cộng sai số, khoảng v ± Δv</b>.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Bước sóng trung bình", "Bước sóng trung bình $\\bar\\lambda$ bằng bao nhiêu cm?", 87.2, "cm", 0.3,
       loi="Tính từ $\\bar l_1$ rồi nhân $4$ (bỏ qua $e$), hoặc lấy hiệu hai trung bình mà quên nhân $2$."),
  buoc("Tốc độ trung bình", "Tốc độ truyền âm trung bình $\\bar v$ bằng bao nhiêu m/s?", 348.8, "m/s", 0.6,
       loi="Quên đổi cm sang m làm kết quả lệch $100$ lần, hoặc lấy thương $\\bar\\lambda/f$.",
       ke=[("Đổi $\\bar\\lambda$ ra mét rồi lấy $\\bar v=\\bar\\lambda f$", True),
           ("Giữ $\\bar\\lambda$ ở đơn vị cm khi nhân với $f$", "Kết quả sẽ có đơn vị cm/s; phải đổi $\\bar\\lambda$ ra mét để có m/s."),
           ("Lấy $\\bar v=\\dfrac{\\bar\\lambda}{f}$", "$v=\\lambda f$ chứ không phải thương.")]),
  buoc("Sai số của bước sóng", "Sai số tuyệt đối $\\Delta\\lambda$ của bước sóng bằng bao nhiêu cm?", 0.72, "cm", 0.03,
       loi="Lấy hiệu $\\Delta l_2-\\Delta l_1$ thay vì tổng, quên hệ số $2$, hoặc bỏ sai số dụng cụ.",
       ke=[("Tính $\\Delta\\bar l_1$, $\\Delta\\bar l_2$ (độ lệch trung bình $+\\ \\Delta l_{\\text{dc}}$) rồi $\\Delta\\lambda=2(\\Delta\\bar l_1+\\Delta\\bar l_2)$", True),
           ("Lấy $\\Delta\\lambda=2(\\Delta\\bar l_2-\\Delta\\bar l_1)$ vì $\\lambda=2(l_2-l_1)$", "Với hiệu hai đại lượng, sai số tuyệt đối vẫn cộng lại (trường hợp xấu nhất), không trừ."),
           ("Chỉ lấy độ lệch trung bình, bỏ qua sai số của thước", "Đề yêu cầu cộng sai số dụng cụ vào mỗi giá trị trung bình; chỉ có độ lệch trung bình là thiếu.")]),
  buoc("Sai số của tốc độ", "Sai số tuyệt đối $\\Delta v$ của tốc độ bằng bao nhiêu m/s?", 3.75, "m/s", 0.15,
       loi="Cộng sai số tuyệt đối của $\\lambda$ và $f$, hoặc quên cộng $\\dfrac{\\Delta f}{f}$.",
       ke=[("Cộng sai số tỉ đối $\\dfrac{\\Delta v}{\\bar v}=\\dfrac{\\Delta\\lambda}{\\bar\\lambda}+\\dfrac{\\Delta f}{f}$ rồi nhân $\\bar v$", True),
           ("Cộng sai số tuyệt đối $\\Delta v=\\Delta\\lambda+\\Delta f$", "$\\lambda$ và $f$ khác đơn vị nên không cộng tuyệt đối được; với tích phải cộng sai số tỉ đối."),
           ("Chỉ dùng $\\dfrac{\\Delta\\lambda}{\\bar\\lambda}$ vì coi $f$ là chính xác", "Đề cho $\\Delta f=1\\ \\text{Hz}$, nên $\\dfrac{\\Delta f}{f}$ vẫn phải cộng vào.")]),
  buoc("So với giá trị tham khảo", "Phép đo có phù hợp với giá trị tham khảo ở nhiệt độ phòng không?",
       lua_chon=[("Phù hợp: giá trị tham khảo theo nhiệt độ phòng nằm trong khoảng $\\bar v\\pm\\Delta v$", True),
                 ("Không phù hợp: $343\\ \\text{m/s}$ nằm ngoài khoảng đo", "$343\\ \\text{m/s}$ ứng với $20\\ ^\\circ\\text{C}$; phòng $30\\ ^\\circ\\text{C}$ phải dùng giá trị tính theo nhiệt độ phòng."),
                 ("Không so sánh được vì số đo có sai số", "Chính khoảng $\\bar v\\pm\\Delta v$ là thứ đem so với giá trị tham khảo.")],
       loi="Lấy $343\\ \\text{m/s}$ của $20\\ ^\\circ\\text{C}$ làm giá trị tham khảo dù phòng nóng hơn.",
       ke=[("Tính $v_{\\text{tk}}=331+0{,}6\\,t$ ở nhiệt độ phòng rồi xem có thuộc $\\bar v\\pm\\Delta v$ không", True),
           ("So $\\bar v$ với $343\\ \\text{m/s}$ vì đây là giá trị quen thuộc", "$343\\ \\text{m/s}$ chỉ đúng ở $20\\ ^\\circ\\text{C}$."),
           ("Chỉ kết luận phù hợp khi $\\bar v$ trùng đúng giá trị tham khảo", "Mọi phép đo có sai số; chỉ cần giá trị tham khảo nằm trong khoảng $\\bar v\\pm\\Delta v$.")]),
  buoc("Kiểm tra")]),
]

# ═════════════ GHI FILE ═════════════
BUILD = [d1, d2, d3, d4]
write(J, 34, "Bài 15. Thực hành: Đo tốc độ truyền âm", DANG, BUILD, ANALYSIS, SOLS)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-11-02"
d["review"] = {"checked": False, "notes": "chờ kiểm chéo (kiem-code)"}
raw = json.dumps(d, ensure_ascii=False, indent=1)


def _walk(x):
    if isinstance(x, str): yield x
    elif isinstance(x, dict):
        for v in x.values(): yield from _walk(v)
    elif isinstance(x, list):
        for v in x: yield from _walk(v)
for _s in _walk(d):
    assert not re.search(r"[\x00-\x1f]", _s), "còn ký tự điều khiển/TAB: " + repr(_s[:60])
    assert '\\"' not in _s, "còn dấu gạch chéo trước nháy: " + _s[:60]
    for m in re.findall(r"\$[^$]*\$", _s):
        assert "<" not in m and ">" not in m, "< hoặc > trong $…$: " + m
open(J, "w").write(raw)
print("xong", J, "marker-end:", raw.count("marker-end"))
