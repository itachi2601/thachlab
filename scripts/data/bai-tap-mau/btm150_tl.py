# -*- coding: utf-8 -*-
"""CĐ15 Âm thanh (lesson 150) — Bài tập tự luận (xếp từ dễ đến khó).
Xuất tu_luan() (dict label + body_html) và kiem_so() (assert mọi đáp số).
Tự soạn 16/10/2026, phỏng theo kiểu đề HSG 9 / tuyển sinh 10 chuyên phổ biến, không chép đề cụ thể nào.
Số liệu khác 6 dạng mẫu (btm150_d123.py, btm150_d456.py)."""
from fractions import Fraction as F
from math import isclose, sqrt

TL = [
 # ── Bài 1 · Dễ: vật phản xạ / hấp thụ âm, chống ô nhiễm tiếng ồn (câu giải thích)
 ("Dễ", r"""<p>a) Xếp các vật sau thành hai nhóm: phản xạ âm tốt và phản xạ âm kém (hấp thụ âm tốt): tấm kính cửa sổ, rèm nhung dày, tường gạch trát vữa nhẵn, thảm len, mặt sàn đá hoa, tấm mút xốp, áo bông.</p>
<p>b) Trong một căn phòng trống vừa xây xong, nói to nghe âm "ồm ồm", kéo dài. Sau khi kê tủ sách, sofa, treo rèm thì tiếng nói nghe rõ hơn. Giải thích.</p>
<p>c) Nhà bạn An ở sát một xưởng mộc chạy máy cưa cả ngày. Hãy đề xuất ba biện pháp chống ô nhiễm tiếng ồn, mỗi biện pháp thuộc một hướng khác nhau.</p>""",
  r"""<p>a) Phản xạ âm tốt (cứng, nhẵn): tấm kính, tường gạch trát vữa nhẵn, mặt sàn đá hoa.</p>
<p>Phản xạ âm kém, hấp thụ âm tốt (mềm, xốp, bề mặt gồ ghề): rèm nhung, thảm len, tấm mút xốp, áo bông.</p>
<p>b) Phòng trống chỉ có tường, trần, sàn cứng nhẵn nên âm phản xạ nhiều lần, các âm phản xạ tới tai liên tiếp ngay sau âm trực tiếp, chồng lên nó làm tiếng nghe kéo dài, không rõ chữ.</p>
<p>Đồ đạc, rèm, sofa là vật mềm, xốp, gồ ghề nên hấp thụ bớt âm và làm âm phản xạ tản đi, âm phản xạ yếu hẳn nên tiếng nói rõ hơn.</p>
<p>c) Giảm tiếng ồn tại nguồn: đề nghị xưởng tra dầu, bọc cao su chân máy, đặt máy trong buồng kín, không chạy máy vào giờ nghỉ.</p>
<p>Ngăn đường truyền âm: xây tường cao hoặc trồng hàng cây dày giữa nhà và xưởng, đóng cửa kính hai lớp phía giáp xưởng.</p>
<p>Hấp thụ âm và làm âm truyền theo hướng khác: treo rèm dày, ốp tấm tiêu âm (mút xốp, gỗ có rãnh) ở tường phía xưởng.</p>
<p>Lỗi hay gặp: chỉ nêu "bịt tai" hoặc "chuyển nhà" — đó không phải biện pháp chống ô nhiễm tiếng ồn theo ba hướng trên.</p>"""),

 # ── Bài 2 · Dễ: đồ thị dao động
 ("Dễ", r"""<p>Trên màn hình một máy hiện sóng (dao động kí), mỗi ô theo chiều ngang ứng với $2\ \text{ms}$. Đồ thị của âm A: $2$ dao động trọn vẹn chiếm đúng $5$ ô ngang, đỉnh sóng cao $3$ ô so với đường giữa. Đồ thị của âm B: $5$ dao động trọn vẹn chiếm đúng $5$ ô ngang, đỉnh sóng cao $1{,}5$ ô.</p>
<p>a) Tính chu kì và tần số của mỗi âm.</p>
<p>b) Âm nào cao hơn? Âm nào to hơn? Vì sao?</p>
<p>c) Trong $3\ \text{s}$ nguồn âm B thực hiện bao nhiêu dao động?</p>""",
  r"""<p>a) Âm A: một dao động chiếm $5:2=2{,}5$ ô, nên $T_A=2{,}5\cdot2=5\ \text{ms}=0{,}005\ \text{s}$.</p>
<p>$f_A=\dfrac{1}{T_A}=\dfrac{1}{0{,}005}=200\ \text{Hz}$.</p>
<p>Âm B: một dao động chiếm $1$ ô, nên $T_B=2\ \text{ms}=0{,}002\ \text{s}$.</p>
<p>$f_B=\dfrac{1}{0{,}002}=500\ \text{Hz}$.</p>
<p>b) $f_B\gt f_A$ nên âm B cao (bổng) hơn.</p>
<p>Biên độ của A ($3$ ô) lớn hơn của B ($1{,}5$ ô) nên âm A to hơn.</p>
<p>c) $N=f_B\,t=500\cdot3=1500$ dao động.</p>
<p>Lỗi hay gặp: nhìn sóng "cao hơn" trên màn hình rồi kết luận âm đó cao hơn — chiều cao đỉnh sóng là biên độ (độ to), độ cao của âm đọc từ chu kì theo trục ngang.</p>
<p>Lỗi hay gặp: lấy cả $5$ ô làm một chu kì của A, quên chia cho số dao động trọn vẹn.</p>"""),

 # ── Bài 3 · Trung bình: dơi, cá heo dùng siêu âm
 ("Trung bình", r"""<p>a) Một con dơi phát sóng siêu âm tần số $40\,000\ \text{Hz}$ trong không khí (tốc độ âm $340\ \text{m/s}$) và nhận được âm dội lại từ một con muỗi sau $0{,}02\ \text{s}$. Coi dơi và muỗi gần như đứng yên trong thời gian rất ngắn đó. Tính khoảng cách từ dơi tới muỗi.</p>
<p>b) Tai người có nghe được âm dơi phát ra không? Tính bước sóng của âm này trong không khí.</p>
<p>c) Một con cá heo phát siêu âm trong nước biển (tốc độ âm $1500\ \text{m/s}$) và nhận được âm dội từ một đàn cá sau $0{,}04\ \text{s}$. Tính khoảng cách từ cá heo tới đàn cá.</p>""",
  r"""<p>a) Âm đi tới muỗi rồi quay về, quãng đường bằng $2d$.</p>
<p>$d=\dfrac{v\,t}{2}=\dfrac{340\cdot0{,}02}{2}=3{,}4\ \text{m}$.</p>
<p>b) $40\,000\ \text{Hz}\gt20\,000\ \text{Hz}$ nên đó là siêu âm, tai người không nghe được.</p>
<p>$\lambda=\dfrac{v}{f}=\dfrac{340}{40\,000}=0{,}0085\ \text{m}=8{,}5\ \text{mm}$.</p>
<p>Bước sóng rất ngắn, cỡ kích thước con mồi, nên siêu âm dội lại rõ trên vật nhỏ như muỗi.</p>
<p>c) Trong nước $v=1500\ \text{m/s}$, nên $d=\dfrac{1500\cdot0{,}04}{2}=30\ \text{m}$.</p>
<p>Lỗi hay gặp: quên chia 2 (ra $6{,}8\ \text{m}$ và $60\ \text{m}$).</p>
<p>Lỗi hay gặp: dùng $340\ \text{m/s}$ cho cá heo trong khi âm đang truyền trong nước.</p>"""),

 # ── Bài 4 · Trung bình: đo tốc độ âm bằng tiếng vang
 ("Trung bình", r"""<p>Để đo tốc độ âm trong không khí, một nhóm học sinh đứng cách một bức tường lớn $85\ \text{m}$ rồi vỗ tay đều đặn. Bạn vỗ tay chỉnh nhịp cho tới khi tiếng vang của mỗi cái vỗ trùng đúng lúc với cái vỗ tiếp theo. Bạn khác bấm đồng hồ: từ cái vỗ thứ nhất đến cái vỗ thứ $31$ hết $15\ \text{s}$.</p>
<p>a) Tính tốc độ âm trong không khí theo kết quả đo.</p>
<p>b) Nếu nhóm đứng cách tường chỉ $10\ \text{m}$ thì có nghe được tiếng vang tách khỏi tiếng vỗ tay không? Lấy $v=340\ \text{m/s}$, biết tai chỉ phân biệt được tiếng vang khi nó tới chậm hơn âm trực tiếp ít nhất $\tfrac{1}{15}\ \text{s}$.</p>""",
  r"""<p>a) Từ cái vỗ thứ $1$ đến thứ $31$ có $30$ khoảng thời gian.</p>
<p>Mỗi khoảng: $\Delta t=\dfrac{15}{30}=0{,}5\ \text{s}$.</p>
<p>Trong $\Delta t$ âm đi tới tường rồi về: $2d=v\,\Delta t$.</p>
<p>$v=\dfrac{2d}{\Delta t}=\dfrac{2\cdot85}{0{,}5}=340\ \text{m/s}$.</p>
<p>b) Thời gian âm đi và về: $t=\dfrac{2\cdot10}{340}\approx0{,}059\ \text{s}$.</p>
<p>$\tfrac{1}{15}\approx0{,}067\ \text{s}$, mà $0{,}059\lt0{,}067$ nên không nghe được tiếng vang tách riêng, chỉ thấy tiếng vỗ kéo dài hơn.</p>
<p>Lỗi hay gặp: chia $15$ cho $31$ (đếm số lần vỗ thay vì số khoảng giữa các lần vỗ).</p>
<p>Lỗi hay gặp: viết $v=\dfrac{d}{\Delta t}$, quên âm phải đi cả lượt về.</p>"""),

 # ── Bài 5 · Khó: người đứng giữa hai vách, hai (ba) lần nghe tiếng vang
 ("Khó", r"""<p>Một người đứng giữa hai vách núi song song, trên đường thẳng vuông góc với hai vách, hét lên một tiếng. Người đó nghe tiếng vang thứ nhất sau $1{,}2\ \text{s}$ và tiếng vang thứ hai sau $2\ \text{s}$ kể từ lúc hét.</p>
<p>a) Tính khoảng cách từ người tới mỗi vách và khoảng cách giữa hai vách.</p>
<p>b) Sau bao lâu kể từ lúc hét, người đó nghe tiếng vang thứ ba? Vì sao tiếng vang thứ ba thường nghe to hơn ta tưởng?</p>
<p>c) Nếu người đó đứng ở chính giữa hai vách thì nghe thấy gì khác?</p>""",
  r"""<p>a) Vách gần: $d_1=\dfrac{340\cdot1{,}2}{2}=204\ \text{m}$.</p>
<p>Vách xa: $d_2=\dfrac{340\cdot2}{2}=340\ \text{m}$.</p>
<p>Khoảng cách hai vách: $D=d_1+d_2=544\ \text{m}$.</p>
<p>b) Tiếng vang thứ ba là âm phản xạ trên cả hai vách: đi tới vách gần, về qua người, tới vách xa rồi về người (hoặc theo thứ tự ngược lại).</p>
<p>Quãng đường: $2d_1+2d_2=2\cdot544=1088\ \text{m}$.</p>
<p>$t_3=\dfrac{1088}{340}=3{,}2\ \text{s}$ (cũng bằng $t_1+t_2$).</p>
<p>Hai đường đi theo hai thứ tự ngược nhau dài bằng nhau nên hai âm phản xạ tới tai cùng lúc, cộng lại.</p>
<p>c) Khi $d_1=d_2$ thì hai tiếng vang đầu tới cùng lúc, người chỉ nghe một tiếng vang (to hơn) thay vì hai tiếng tách rời.</p>
<p>Lỗi hay gặp: cho rằng tiếng vang thứ ba tới sau $2t_1=2{,}4\ \text{s}$ — âm không thể phản xạ hai lần liền trên cùng một vách mà không đi qua vách kia.</p>
<p>Lỗi hay gặp: lấy $D=\dfrac{340\cdot(2-1{,}2)}{2}$, nhầm hiệu thời gian với tổng khoảng cách.</p>"""),

 # ── Bài 6 · Khó: kết hợp chuyển động (thuyền chạy ra xa vách)
 ("Khó", r"""<p>Một chiếc ca nô chạy thẳng đều với tốc độ $10\ \text{m/s}$ ra xa một vách đá dựng đứng theo phương vuông góc với vách. Khi ca nô cách vách $150\ \text{m}$ thì kéo còi. Tốc độ âm trong không khí là $340\ \text{m/s}$.</p>
<p>a) Sau bao lâu người lái ca nô nghe được tiếng vang? Lúc đó ca nô cách vách bao xa?</p>
<p>b) Muốn nghe tiếng vang sau đúng $1\ \text{s}$ kể từ lúc kéo còi thì phải kéo còi khi ca nô cách vách bao xa?</p>""",
  r"""<p>a) Gọi $t$ là thời gian từ lúc kéo còi đến lúc nghe tiếng vang.</p>
<p>Âm đi $150\ \text{m}$ tới vách, rồi đuổi theo ca nô đang ở cách vách $150+10t$.</p>
<p>Quãng đường âm: $340t=150+(150+10t)$.</p>
<p>$330t=300$, nên $t=\dfrac{10}{11}\approx0{,}91\ \text{s}$.</p>
<p>Khoảng cách lúc nghe: $150+10\cdot\dfrac{10}{11}\approx159{,}1\ \text{m}$.</p>
<p>b) $340\cdot1=d+(d+10\cdot1)$, nên $2d=330$ và $d=165\ \text{m}$.</p>
<p>Lỗi hay gặp: dùng ngay $d=\dfrac{v\,t}{2}$ như khi nguồn đứng yên, quên ca nô đã đi thêm trong lúc âm truyền.</p>
<p>Lỗi hay gặp: viết $340t+10t=300$ như trường hợp ca nô chạy lại gần vách — phải xét đúng chiều chuyển động.</p>"""),

 # ── Bài 7 · Nâng cao: tiếng nổ trực tiếp và tiếng vang từ vách song song
 ("Nâng cao", r"""<p>Hai người A và B đứng trên một bãi đất phẳng, đường nối A với B song song với một vách núi dài, phẳng, thẳng đứng. A bắn một phát súng hoả mai. B thấy khói súng, sau $2\ \text{s}$ thì nghe tiếng nổ, rồi sau thêm $0{,}5\ \text{s}$ nữa thì nghe tiếng vang từ vách núi. Coi ánh sáng truyền tức thời, tốc độ âm $340\ \text{m/s}$.</p>
<p>a) Tính khoảng cách AB.</p>
<p>b) Tính khoảng cách từ đường AB tới vách núi.</p>
<p>c) Tiếng vang có tách khỏi tiếng nổ trực tiếp không? Giải thích.</p>""",
  r"""<p>a) Ánh sáng tới B gần như tức thời, nên $2\ \text{s}$ là thời gian âm đi thẳng từ A tới B.</p>
<p>$AB=340\cdot2=680\ \text{m}$.</p>
<p>b) Tiếng vang tới B sau $2+0{,}5=2{,}5\ \text{s}$ kể từ lúc bắn.</p>
<p>Đường đi của âm phản xạ: $AI+IB=340\cdot2{,}5=850\ \text{m}$, với $I$ là điểm phản xạ trên vách.</p>
<p>Âm phản xạ theo quy luật góc phản xạ bằng góc tới, A và B cách vách như nhau, nên $I$ nằm đối diện trung điểm $H$ của AB và $AI=IB=425\ \text{m}$.</p>
<p>Tam giác vuông $AHI$: $AH=340\ \text{m}$, nên khoảng cách tới vách $h=HI=\sqrt{425^2-340^2}=255\ \text{m}$.</p>
<p>c) Tiếng vang chậm hơn tiếng nổ $0{,}5\ \text{s}\gt\tfrac{1}{15}\ \text{s}$ nên B nghe được hai tiếng tách rời.</p>
<p>Lỗi hay gặp: coi đường đi của tiếng vang là $2h$ (như khi nguồn và người nghe cùng một chỗ), ra $h=425\ \text{m}$.</p>
<p>Lỗi hay gặp: dùng $0{,}5\ \text{s}$ làm toàn bộ thời gian đi của tiếng vang.</p>"""),

 # ── Bài 8 · Nâng cao: tàu ngầm chạy về phía vách đá ngầm, hai lần phát siêu âm
 ("Nâng cao", r"""<p>Một tàu ngầm chạy thẳng đều về phía một vách đá ngầm thẳng đứng, theo phương vuông góc với vách. Tàu phát một xung siêu âm và nhận được xung phản xạ sau $t_1=3\ \text{s}$. Đúng $63\ \text{s}$ sau lần phát thứ nhất, tàu phát xung thứ hai và nhận xung phản xạ sau $t_2=2\ \text{s}$. Tốc độ âm trong nước biển là $1500\ \text{m/s}$.</p>
<p>a) Tính tốc độ của tàu ngầm.</p>
<p>b) Tính khoảng cách từ tàu tới vách lúc phát xung thứ nhất.</p>
<p>c) Nếu giữ nguyên hướng và tốc độ thì sau bao lâu kể từ lần phát thứ nhất tàu sẽ chạm vách?</p>""",
  r"""<p>Gọi $v=1500\ \text{m/s}$, $u$ là tốc độ tàu, $L_1$ và $L_2$ là khoảng cách tới vách lúc phát xung thứ nhất và thứ hai.</p>
<p>Xung thứ nhất: âm đi $L_1$ tới vách rồi quay lại gặp tàu đã tiến thêm $u\,t_1$, nên $v\,t_1=2L_1-u\,t_1$.</p>
<p>Do đó $L_1=\dfrac{(v+u)\,t_1}{2}$.</p>
<p>Tương tự xung thứ hai: $L_2=\dfrac{(v+u)\,t_2}{2}$.</p>
<p>Giữa hai lần phát, tàu đi được $L_1-L_2=u\cdot63$.</p>
<p>a) $\dfrac{(v+u)(t_1-t_2)}{2}=63u$, tức $(1500+u)\cdot0{,}5=63u$.</p>
<p>$750=62{,}5u$, nên $u=12\ \text{m/s}$ (khoảng $43\ \text{km/h}$).</p>
<p>b) $L_1=\dfrac{(1500+12)\cdot3}{2}=2268\ \text{m}$.</p>
<p>Kiểm tra: $L_2=2268-12\cdot63=1512\ \text{m}$ và $\dfrac{(1500+12)\cdot2}{2}=1512\ \text{m}$ ✓.</p>
<p>c) $t=\dfrac{L_1}{u}=\dfrac{2268}{12}=189\ \text{s}$.</p>
<p>Lỗi hay gặp: dùng $L=\dfrac{v\,t}{2}$ như tàu đứng yên, ra $L_1-L_2=750\ \text{m}$ rồi $u\approx11{,}9\ \text{m/s}$ — sai vì bỏ quãng đường tàu đi trong lúc chờ xung dội về.</p>
<p>Lỗi hay gặp: lấy $63\ \text{s}$ trừ đi $t_1$ — đề cho $63\ \text{s}$ tính giữa hai lần phát, không phải giữa lần nhận và lần phát.</p>"""),
]


def tu_luan():
    parts = []
    for k, (muc, de, gi) in enumerate(TL, 1):
        parts.append(f"<h4>Bài {k} · {muc}</h4>{de}<details><summary>Hướng dẫn giải</summary>{gi}</details>")
    return dict(label="Bài tập tự luận (xếp từ dễ đến khó)",
                body_html="<p>Các bài còn lại của chuyên đề, xếp từ dễ đến khó. Tự giải trên giấy rồi mới mở hướng dẫn.</p>"
                          + "".join(parts))


def kiem_so():
    v, vn = 340, 1500
    # Bài 2
    TA, TB = F(5, 2) * 2 / 1000, F(1) * 2 / 1000
    assert TA == F(1, 200) and 1 / TA == 200 and TB == F(1, 500) and 1 / TB == 500 and 500 * 3 == 1500
    # Bài 3
    assert isclose(v * 0.02 / 2, 3.4) and F(v, 40000) == F(85, 10000) and isclose(vn * 0.04 / 2, 30)
    assert isclose(v * 0.02, 6.8) and isclose(vn * 0.04, 60)
    # Bài 4
    dt = F(15, 30); assert dt == F(1, 2) and 2 * 85 / dt == 340
    t10 = 2 * 10 / v; assert abs(t10 - 0.059) < 5e-4 and t10 < 1 / 15 and abs(1 / 15 - 0.067) < 5e-4
    # Bài 5
    d1, d2 = F(v) * F(12, 10) / 2, F(v) * 2 / 2
    assert (d1, d2, d1 + d2) == (204, 340, 544) and 2 * (d1 + d2) == 1088 and F(1088, v) == F(16, 5) == F(12, 10) + 2
    # Bài 6
    t = F(300, 330); assert t == F(10, 11) and abs(float(t) - 0.91) < 5e-3 and v * t == 150 + 150 + 10 * t
    assert abs(float(150 + 10 * t) - 159.1) < 0.05 and 2 * 165 + 10 == 340
    # Bài 7
    AB, path = v * 2, v * F(5, 2); assert AB == 680 and path == 850
    h = sqrt(425 ** 2 - 340 ** 2); assert h == 255 and sqrt((AB / 2) ** 2 + h ** 2) * 2 == 850 and 0.5 > 1 / 15
    # Bài 8
    t1, t2, tau = F(3), F(2), 63
    u = F(vn) * (t1 - t2) / (2 * tau - (t1 - t2)); assert u == 12 and abs(12 * 3.6 - 43) < 0.5
    assert (vn + u) * (t1 - t2) / 2 == 756 == 63 * u and F(750, F(125, 2)) == 12
    L1, L2 = (vn + u) * t1 / 2, (vn + u) * t2 / 2
    assert (L1, L2) == (2268, 1512) and L1 - u * tau == L2 and L1 / u == 189
    assert vn * t1 == 2 * L1 - u * t1 and vn * t2 == 2 * L2 - u * t2
    sai = F(vn) * (t1 - t2) / 2; assert sai == 750 and abs(float(sai / tau) - 11.9) < 0.05
    print("kiểm số liệu tự luận 150: đạt")


if __name__ == "__main__":
    kiem_so()
    print(len(tu_luan()["body_html"]))
