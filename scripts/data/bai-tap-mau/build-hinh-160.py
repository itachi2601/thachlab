"""Bài tập mẫu Chuyên đề 00 "Kỹ năng nền: công cụ toán học, đọc đồ thị, sai số và thực hành" (khoá Vật lí HSG & chuyên, KHTN 9)
— lesson_id 160.  Nguồn: content/hsg9/cd00-ky-nang-nen/nguon.md.
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-160.py   (idempotent)

Chuyên đề không có YCCĐ riêng → `topic` lấy YCCĐ con có sẵn trong scripts/data/question-topics.json sát từng dạng
(dạng sai số dùng đúng chủ đề lớp 10 bài 3). Phiên chính có thể đổi `topic` rồi chạy lại nếu muốn bài tương tự khác."""
import json, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *
from svg_lib import chevron

J = os.path.join(HERE, "160.json")
NOTE = "Hình minh hoạ, không đúng tỉ lệ."


# ═════════════ tiện ích hình ═════════════
def R(x, y, w, h, c="currentColor", sw=2, fill="none", rx=0, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{c}" '
            f'stroke-width="{sw}"{d} opacity="{op}"/>')

def circ(x, y, r, c="currentColor", sw=2, fill="none"):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{c}" stroke-width="{sw}"/>'

def rich(s, size=13):
    """`F_ms` → F với chỉ số dưới ms."""
    parts = re.split(r"_([A-Za-z0-9]+)", s)
    out = parts[0]
    for i in range(1, len(parts), 2):
        out += f'<tspan dy="4" font-size="{size - 3}">{parts[i]}</tspan>'
        if parts[i + 1]:
            out += f'<tspan dy="-4">{parts[i + 1]}</tspan>'
    return out

def txt(x, y, s, c="currentColor", size=13, anchor="start", weight="700"):
    return lbl(x, y, rich(s, size), c, size, anchor, weight)

def anim(attr, vals, dur, keytimes=None, fmt="{:.1f}"):
    """<animate> chạy MỘT lần khi bấm (begin=indefinite, dừng ở khung cuối)."""
    v = ";".join(fmt.format(x) for x in vals)
    kt = f' keyTimes="{";".join(f"{k:.3f}" for k in keytimes)}"' if keytimes else ""
    return f'<animate attributeName="{attr}" values="{v}"{kt} dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>'

def blk(x, y, w, h, c):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{c}" fill-opacity=".2" stroke="{c}" stroke-width="2"/>'

def zig(x0, y, w, c="currentColor"):
    pts = [(x0, y), (x0 + w / 8, y - 7), (x0 + 3 * w / 8, y + 7), (x0 + 5 * w / 8, y - 7), (x0 + 7 * w / 8, y + 7), (x0 + w, y)]
    return poly(pts, c, 2.2)

def loop(x, y, w, h, res, amm=False):
    """Mạch kín: pin ở đáy, các điện trở (nhãn, là-biến-trở?) trên cạnh trên, ampe kế ở cạnh phải."""
    b = ""; bx = x + w / 2; n = len(res); half = 26; K = "currentColor"
    cxs = [x + w * (i + 1) / (n + 1) for i in range(n)]
    b += seg(x, y + h, x, y, K, 2.2)
    prev = x
    for (lab, var), cx in zip(res, cxs):
        b += seg(prev, y, cx - half, y, K, 2.2) + zig(cx - half, y, 2 * half) + txt(cx, y - 16, lab, K, 12, "middle")
        if var:
            b += arrow("", "o", cx - 18, y + 16, cx + 18, y - 16, 2)
        prev = cx + half
    b += seg(prev, y, x + w, y, K, 2.2)
    ym = y + h / 2
    if amm:
        b += seg(x + w, y, x + w, ym - 13, K, 2.2) + circ(x + w, ym, 13, K, 2.2) + txt(x + w, ym + 5, "A", K, 13, "middle")
        b += seg(x + w, ym + 13, x + w, y + h, K, 2.2)
    else:
        b += seg(x + w, y, x + w, y + h, K, 2.2)
    b += seg(x + w, y + h, bx + 8, y + h, K, 2.2) + seg(bx - 8, y + h, x, y + h, K, 2.2)
    b += seg(bx - 8, y + h - 12, bx - 8, y + h + 12, K, 3.2) + seg(bx + 8, y + h - 6, bx + 8, y + h + 6, K, 3.2)
    return b

# ── hệ trục đồ thị U–I ──
GX0, GY0, SXI, SYU = 56, 190, 740.0, 26.0
def gx(i): return GX0 + i * SXI
def gy(u): return GY0 - u * SYU

def graph_axes():
    K = "currentColor"
    b = seg(GX0, GY0, GX0 + 348, GY0, K, 2) + seg(GX0, GY0, GX0, GY0 - 172, K, 2)
    b += chevron(GX0 + 348, GY0, 1, 0, K, 2, 10) + chevron(GX0, GY0 - 172, 0, -1, K, 2, 10)
    for k in range(5):
        i = k / 10
        b += seg(gx(i), GY0, gx(i), GY0 + 5, K, 1.6) + txt(gx(i), GY0 + 19, str(i).replace(".", ",") if k else "0", K, 11, "middle", "400")
    for u in range(1, 7):
        b += seg(GX0 - 5, gy(u), GX0, gy(u), K, 1.6) + seg(GX0, gy(u), GX0 + 340, gy(u), K, 1, "3 5", .25) + txt(GX0 - 9, gy(u) + 4, str(u), K, 11, "end", "400")
    b += txt(GX0 + 346, GY0 - 8, "I (A)", K, 12, "end", "400") + txt(GX0 + 8, GY0 - 170, "U (V)", K, 12, "start", "400")
    return b

def graph_line(pts, c, dur=None):
    ie, ue = pts[-1]
    if dur:
        b = (f'<line x1="{GX0}" y1="{GY0}" x2="{GX0}" y2="{GY0}" stroke="{c}" stroke-width="2.4">'
             f'{anim("x2", [GX0, gx(ie)], dur)}{anim("y2", [GY0, gy(ue)], dur)}</line>')
    else:
        b = seg(GX0, GY0, gx(ie), gy(ue), c, 2.4)
    for i, u in pts:
        f = i / ie
        o = (f'<circle cx="{gx(i):.1f}" cy="{gy(u):.1f}" r="4.5" fill="{c}" opacity="0">'
             f'{anim("opacity", [0, 0, 1], dur, [0, f * 0.96, min(f * 0.96 + 0.03, 1)], "{:g}")}</circle>') if dur else dot(gx(i), gy(u), 4.5, c)
        b += o
    return b

PTS_A = [(0.1, 1.2), (0.2, 2.4), (0.3, 3.6), (0.4, 4.8)]
PTS_B = [(0.05, 1.5), (0.10, 3.0), (0.15, 4.5), (0.20, 6.0)]


# ═════════════ ĐỀ CÁC DẠNG (dễ → khó) ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Rút tỉ số: tỉ lệ thuận, tỉ lệ nghịch và tỉ lệ với bình phương",
      topic="Định luật Ohm cho một điện trở",
      problem_html=r"""<p>Một dây dẫn có điện trở $R$ không đổi. Khi đặt vào hai đầu dây hiệu điện thế $U_1=4{,}5\ \text{V}$ thì cường độ dòng điện là $I_1=0{,}18\ \text{A}$.</p><ol type="a"><li>Lập tỉ số, không cần tính $R$, để tìm cường độ dòng điện $I_2$ khi hiệu điện thế là $U_2=6{,}0\ \text{V}$.</li><li>Mắc điện trở $R_0=10\ \Omega$ nối tiếp với một biến trở vào nguồn có hiệu điện thế $U$ không đổi. Khi biến trở có giá trị $R_1=20\ \Omega$ thì dòng điện trong mạch là $0{,}4\ \text{A}$. Tăng biến trở lên $R_2=50\ \Omega$. Một bạn viết $\dfrac{I_2}{I_1}=\dfrac{R_1}{R_2}$ để tính dòng điện lúc này. Cách viết đó đúng hay sai? Tính $I_2$ đúng.</li><li>Một điện trở $20\ \Omega$ toả nhiệt với công suất $P_1=0{,}80\ \text{W}$ khi dòng điện qua nó là $0{,}20\ \text{A}$. Tăng dòng điện lên $0{,}30\ \text{A}$ thì công suất tăng bao nhiêu lần và bằng bao nhiêu oát?</li></ol>"""),
 dict(label="Dạng 2 · Dễ · Đổi đơn vị, kiểm tra thứ nguyên và phán đoán tính hợp lí",
      topic="Khái niệm và đơn vị đo năng lượng",
      problem_html=r"""<p>Làm từng câu, ghi đơn vị ở mọi bước.</p><ol type="a"><li>Dùng đơn vị để kiểm tra công thức $P=\dfrac{U^2}{R}$ (tính công suất) có cho kết quả đơn vị oát hay không.</li><li>Một người đi bộ được quãng đường $3{,}6\ \text{km}$ trong $40$ phút. Tính tốc độ theo m/s và theo km/h; kết quả có hợp lí với người đi bộ không?</li><li>Một lò sưởi ghi $220\ \text{V}-2\ \text{kW}$ hoạt động $3$ giờ ở hiệu điện thế $220\ \text{V}$. Tính điện năng tiêu thụ theo kWh và theo J.</li><li>Tính cường độ dòng điện qua lò sưởi và nhận xét độ lớn.</li></ol>"""),
 dict(label="Dạng 3 · Trung bình · Đọc đồ thị U–I: điện trở, độ dốc, nội suy và ngoại suy",
      topic="Tính vận tốc từ độ dốc đồ thị",
      problem_html=r"""<p>Khảo sát hai dây dẫn A và B bằng cách đo hiệu điện thế $U$ giữa hai đầu dây và cường độ dòng điện $I$ qua dây. Đồ thị $U$–$I$ (trục hoành là $I$, trục tung là $U$) được vẽ từ các số liệu sau.</p><div class="table-scroll"><table class="tl-table"><thead><tr><th>Dây</th><th>$I$ (A)</th><th>$U$ (V)</th></tr></thead><tbody><tr><td>A</td><td>$0{,}10$ ; $0{,}20$ ; $0{,}30$ ; $0{,}40$</td><td>$1{,}2$ ; $2{,}4$ ; $3{,}6$ ; $4{,}8$</td></tr><tr><td>B</td><td>$0{,}05$ ; $0{,}10$ ; $0{,}15$ ; $0{,}20$</td><td>$1{,}5$ ; $3{,}0$ ; $4{,}5$ ; $6{,}0$</td></tr></tbody></table></div><ol type="a"><li>Tính điện trở của mỗi dây từ đồ thị.</li><li>Trên cùng một hệ trục, đường của dây nào dốc hơn? Giải thích.</li><li>Nội suy cường độ dòng điện qua dây A khi $U=2{,}7\ \text{V}$.</li><li>Nếu vẽ lại đồ thị $I$–$U$ (trục hoành là $U$) cho dây A thì hệ số góc của đường thẳng bằng bao nhiêu, đơn vị gì?</li><li>Ngoại suy hiệu điện thế giữa hai đầu dây B khi $I=0{,}25\ \text{A}$; nói rõ độ tin cậy của kết quả.</li></ol>"""),
 dict(label="Dạng 4 · Trung bình · Diện tích dưới đồ thị v–t bậc thang: quãng đường và tốc độ trung bình",
      topic="Tốc độ trung bình và vận tốc trung bình",
      problem_html=r"""<p>Một người đi xe đạp trên đường thẳng, luôn theo một chiều. Đồ thị vận tốc theo thời gian gồm bốn giai đoạn liên tiếp:</p><ul><li>từ $0$ đến $20\ \text{s}$: vận tốc $4\ \text{m/s}$;</li><li>từ $20\ \text{s}$ đến $35\ \text{s}$: vận tốc $6\ \text{m/s}$;</li><li>từ $35\ \text{s}$ đến $45\ \text{s}$: dừng ở đèn đỏ;</li><li>từ $45\ \text{s}$ đến $65\ \text{s}$: vận tốc $5\ \text{m/s}$.</li></ul><ol type="a"><li>Tính tổng quãng đường xe đi được.</li><li>Tính tốc độ trung bình trên toàn hành trình.</li><li>Lúc $t=50\ \text{s}$ xe cách điểm xuất phát bao nhiêu mét?</li><li>Xe đi được $150\ \text{m}$ đầu tiên vào thời điểm nào?</li></ol>"""),
 dict(label="Dạng 5 · Khó · Sai số: giá trị trung bình, sai số tuyệt đối, sai số tương đối và ghi kết quả đo",
      topic="Sai số tuyệt đối, sai số tỉ đối",
      problem_html=r"""<p>Một nhóm đo thời gian $t$ để một xe lăn đi hết quãng đường $s=1{,}20\ \text{m}$ trên máng bằng đồng hồ bấm giây có độ chia nhỏ nhất (ĐCNN) $0{,}1\ \text{s}$. Năm lần đo cho kết quả: $2{,}4$ ; $2{,}7$ ; $2{,}5$ ; $2{,}3$ ; $2{,}6$ (đơn vị giây). Quãng đường $s$ có sai số tuyệt đối $\Delta s=0{,}01\ \text{m}$.</p><ol type="a"><li>Tính giá trị trung bình $t_{tb}$.</li><li>Tính sai số tuyệt đối $\Delta t$ (sai số ngẫu nhiên cộng sai số dụng cụ bằng nửa ĐCNN), làm tròn đến một chữ số có nghĩa.</li><li>Tính sai số tương đối $\delta_t$.</li><li>Ghi kết quả đo $t$ đúng quy cách.</li><li>Tính tốc độ trung bình $v=\dfrac{s}{t}$ và sai số $\Delta v$; ghi kết quả đo $v$.</li></ol>"""),
 dict(label="Dạng 6 · Khó · Bài tổng hợp: tóm tắt, đổi đơn vị, hiệu suất, điện năng, tiền điện và rút tỉ số",
      topic="Tính điện năng tiêu thụ và tiền điện",
      problem_html=r"""<p>Một ấm điện ghi $220\ \text{V}-1800\ \text{W}$ được dùng ở hiệu điện thế $220\ \text{V}$ để đun $1{,}8$ lít nước từ $20\ ^\circ\text{C}$ đến $100\ ^\circ\text{C}$. Hiệu suất của ấm là $84\%$. Nhiệt dung riêng của nước là $4200\ \text{J/(kg·K)}$, khối lượng riêng của nước là $1000\ \text{kg/m}^3$.</p><ol type="a"><li>Tính thời gian đun.</li><li>Mỗi ngày đun hai lần như vậy. Tính tiền điện của ấm trong $30$ ngày, giá $2000$ đồng một kWh.</li><li>Nếu cắm nhầm ấm vào nguồn $110\ \text{V}$ (điện trở dây đun và hiệu suất không đổi) thì thời gian đun mỗi lần là bao lâu?</li></ol><p>Trình bày theo bốn bước: tóm tắt, đặt ký hiệu, lập luận từng bước, kết luận có đơn vị.</p>"""),
]
topics = json.load(open(os.path.join(HERE, "../question-topics.json")))
for q in DANG:   # topic phải có đúng một dòng trong question-topics.json
    assert len([t for t in topics if t["name"].strip() == q["topic"]]) == 1, q["topic"]


# ═════════════ HÌNH ═════════════
# ───────────── Dạng 1 ─────────────
def d1(kk):
    p = f"d1{kk}"; K = "currentColor"
    if kk == 0:
        b = txt(99, 26, "Trạng thái 1", K, 13, "middle") + loop(24, 52, 150, 76, [("R", False)], True)
        b += txt(99, 154, "U₁ = 4,5 V", K, 13, "middle") + txt(99, 174, "I₁ = 0,18 A", K, 13, "middle")
        g = txt(321, 26, "Trạng thái 2", K, 13, "middle") + loop(246, 52, 150, 76, [("R", False)], True)
        g += txt(321, 154, "U₂ = 6,0 V", K, 13, "middle") + txt(321, 174, "I₂ = ?", ORG, 13, "middle")
        b += f'<g opacity="0.25">{g}{anim("opacity", [0.25, 1], 2.5, fmt="{:g}")}</g>'
        b += txt(210, 198, "cùng một điện trở R, không đổi", K, 12, "middle", "400")
        return fig("c0-1-0", "0 0 420 206", "Cùng một điện trở R được đặt vào hai hiệu điện thế khác nhau; ở trạng thái 2 dòng điện chưa biết",
                   b, "Mô phỏng: chuyển từ trạng thái 1 sang trạng thái 2 (đổi hiệu điện thế, giữ nguyên R).")
    b = loop(20, 60, 200, 80, [("R₀ = 10 Ω", False), ("biến trở R", True)])
    b += txt(120, 172, "U không đổi", K, 13, "middle", "400")
    b += txt(238, 56, "R toàn mạch = R₀ + R", K, 13) + txt(238, 82, "I = U / (R₀ + R)", ORG, 14)
    b += txt(238, 114, "⚠ I không tỉ lệ nghịch", K, 13, "start", "400") + txt(238, 134, "với riêng R", K, 13, "start", "400")
    return fig("c0-1-2", "0 0 420 190", "Biến trở mắc nối tiếp với điện trở R0 và nguồn; dòng điện tỉ lệ nghịch với tổng R0 cộng R",
               b, "Dữ kiện: R₀ không đổi nối tiếp với biến trở. " + NOTE)


# ───────────── Dạng 2 ─────────────
def d2(kk):
    p = f"d2{kk}"; K = "currentColor"
    if kk == 0:
        yg = 112
        b = seg(30, yg, 392, yg, K, 3) + seg(30, yg - 6, 30, yg + 6, K, 2) + txt(30, yg + 26, "xuất phát", K, 12, "middle", "400")
        man = (circ(0, -46, 6, K, 2.2) + seg(0, -40, 0, -20, K, 2.2) + seg(0, -34, -10, -24, K, 2.2) + seg(0, -34, 10, -24, K, 2.2)
               + seg(0, -20, -8, 0, K, 2.2) + seg(0, -20, 8, 0, K, 2.2))
        b += f'<g transform="translate(30 {yg})"><g>{R(-10, -52, 20, 52, K, 1.4, "none", 0, "4 3", .35)}<animateTransform attributeName="transform" type="translate" values="0 0;340 0" dur="5.00s" begin="indefinite" fill="freeze"/>{man}</g></g>'
        b += txt(16, 24, "đi bộ 3,6 km", K, 13) + txt(16, 44, "trong 40 phút", K, 13)
        b += txt(250, 24, "v = ?  (m/s)", ORG, 13) + txt(250, 44, "v = ?  (km/h)", ORG, 13)
        return fig("c0-2-0", "0 0 420 150", "Một người đi bộ đi hết quãng đường 3,6 km trong 40 phút",
                   b, "Mô phỏng: người đi bộ đều hết quãng đường (tốc độ minh hoạ, chạy 5 s).")
    rows = [("km/h → m/s", "chia 3,6"), ("phút → s", "nhân 60"), ("giờ → s", "nhân 3600"), ("kWh → J", "nhân 3,6·10⁶"), ("kW → W", "nhân 1000")]
    b = ""
    for k, (a, c) in enumerate(rows):
        y = 28 + k * 28
        b += R(16, y - 18, 388, 26, K, 1.2, "none", 6, "", .35) + txt(30, y, a, BLUE, 13) + txt(220, y, c, K, 13)
    b += txt(16, 188, "V²/Ω = V·A = W : kiểm bằng đơn vị", K, 13, "start", "400")
    return fig("c0-2-2", "0 0 420 202", "Bảng các phép đổi đơn vị thường dùng: km/h sang m/s, phút sang giây, giờ sang giây, kWh sang J, kW sang W",
               b, "Dữ kiện: đổi mọi đại lượng về cùng hệ đơn vị trước khi thay số.")


# ───────────── Dạng 3 ─────────────
def d3(kk):
    p = f"d3{kk}"; K = "currentColor"
    if kk == 0:
        b = graph_axes() + graph_line(PTS_A, BLUE, 4.5) + graph_line(PTS_B, ORG, 4.5)
        b += txt(gx(0.4) + 8, gy(4.8) + 4, "A", BLUE, 14) + txt(gx(0.2) + 8, gy(6.0) + 4, "B", ORG, 14)
        return fig("c0-3-0", "0 0 420 214", "Đồ thị U theo I của hai dây dẫn A và B là hai đường thẳng đi qua gốc toạ độ",
                   b, "Mô phỏng: hai đường thẳng được vẽ dần qua các điểm đo (trục hoành là I, trục tung là U).")
    b = graph_axes() + graph_line(PTS_A, BLUE) + graph_line(PTS_B, ORG)
    b += txt(gx(0.4) - 6, gy(4.8) - 10, "A", BLUE, 14) + txt(gx(0.2) + 8, gy(6.0) + 4, "B", ORG, 14)
    b += seg(gx(0.1), gy(1.2), gx(0.4), gy(1.2), K, 1.8, "5 4") + seg(gx(0.4), gy(1.2), gx(0.4), gy(4.8), K, 1.8, "5 4")
    b += txt((gx(0.1) + gx(0.4)) / 2, gy(1.2) + 17, "ΔI", K, 13, "middle") + txt(gx(0.4) + 7, (gy(1.2) + gy(4.8)) / 2 + 4, "ΔU", K, 13)
    b += txt(66, 52, "hệ số góc = ΔU / ΔI", K, 13) + txt(66, 70, "đơn vị V/A = Ω", K, 12, "start", "400")
    return fig("c0-3-2", "0 0 420 214", "Đồ thị U–I của hai dây dẫn với tam giác chỉ hệ số góc delta U chia delta I của dây A",
               b, "Dữ kiện: trên đồ thị U–I, hệ số góc ΔU/ΔI bằng điện trở. Đổi trục thì hệ số góc thành 1/R.")


# ───────────── Dạng 4 ─────────────
def s_t(t):
    return 4 * t if t <= 20 else 80 + 6 * (t - 20) if t <= 35 else 170 if t <= 45 else 170 + 5 * (t - 45)

def d4(kk):
    p = f"d4{kk}"; K = "currentColor"
    if kk == 0:
        yg = 74; X0 = 40; PXM = 1.2
        xs = [PXM * s_t(t) for t in range(0, 66, 5)]
        vals = ";".join(f"{x:.1f} 0" for x in xs)
        bike = (circ(-13, -8, 8, K, 2.2) + circ(13, -8, 8, K, 2.2) + poly([(-13, -8), (-3, -24), (9, -24), (13, -8)], K, 2.2)
                + seg(-3, -24, -6, -32, K, 2.2) + circ(2, -42, 5, K, 2) + seg(2, -37, -3, -24, K, 2.2) + seg(2, -35, 10, -26, K, 2))
        b = seg(24, yg, 398, yg, K, 3) + seg(X0, yg - 6, X0, yg + 6, K, 2) + txt(X0, yg + 24, "xuất phát", K, 12, "middle", "400")
        b += (f'<g transform="translate({X0} {yg})"><g><animateTransform attributeName="transform" type="translate" values="{vals}" '
              f'dur="13.00s" begin="indefinite" fill="freeze"/>{bike}</g></g>')
        b += txt(16, 24, "s = ?     v_tb = ?", ORG, 13)
        for k, t in enumerate(["0–20 s : 4 m/s", "20–35 s : 6 m/s", "35–45 s : dừng", "45–65 s : 5 m/s"]):
            b += txt(16, 128 + k * 20, t, K, 13, "start", "400")
        return fig("c0-4-0", "0 0 420 214", "Người đi xe đạp chạy theo bốn giai đoạn: 4 m/s, 6 m/s, dừng, 5 m/s",
                   b, "Mô phỏng: xe chạy theo đúng bốn giai đoạn, nhanh gấp 5 lần thời gian thật (65 s thành 13 s).")
    ox, oy, SX, SV = 56, 170, 5.0, 20.0
    b = seg(ox, oy, ox + 336, oy, K, 2) + seg(ox, oy, ox, oy - 140, K, 2) + chevron(ox + 336, oy, 1, 0, K, 2, 10) + chevron(ox, oy - 140, 0, -1, K, 2, 10)
    for t in (0, 20, 35, 45, 65):
        b += seg(ox + t * SX, oy, ox + t * SX, oy + 5, K, 1.6) + txt(ox + t * SX, oy + 19, str(t), K, 11, "middle", "400")
    for v in (2, 4, 6):
        b += seg(ox - 5, oy - v * SV, ox, oy - v * SV, K, 1.6) + txt(ox - 9, oy - v * SV + 4, str(v), K, 11, "end", "400")
    b += txt(ox + 340, oy + 19, "t (s)", K, 12, "start", "400") + txt(ox + 8, oy - 138, "v (m/s)", K, 12, "start", "400")
    for (t0, t1, v, c, n) in ((0, 20, 4, BLUE, "①"), (20, 35, 6, GRN, "②"), (45, 65, 5, ORG, "④")):
        b += blk(ox + t0 * SX, oy - v * SV, (t1 - t0) * SX, v * SV, c) + txt(ox + (t0 + t1) / 2 * SX, oy - v * SV / 2 + 5, n, c, 15, "middle")
    b += seg(ox + 35 * SX, oy - 1, ox + 45 * SX, oy - 1, RED, 3.2) + txt(ox + 40 * SX, oy - 10, "③", RED, 15, "middle")
    b += txt(ox + 190, oy - 128, "diện tích = quãng đường", K, 13, "start", "400") + txt(ox + 190, oy - 108, "v_tb = s / t (tổng / tổng)", K, 13, "start", "400")
    return fig("c0-4-2", "0 0 420 202", "Đồ thị vận tốc theo thời gian gồm bốn giai đoạn; mỗi giai đoạn là một hình chữ nhật",
               b, "Dữ kiện: diện tích mỗi hình chữ nhật là quãng đường của giai đoạn; giai đoạn dừng có diện tích bằng 0.")


# ───────────── Dạng 5 ─────────────
T5 = [2.4, 2.7, 2.5, 2.3, 2.6]
def tx(t): return 40 + (t - 2.0) * 283.3

def axis5(y=118):
    K = "currentColor"
    b = seg(30, y, 394, y, K, 2) + chevron(394, y, 1, 0, K, 2, 10)
    for k in range(13):
        t = 2.0 + k / 10
        b += seg(tx(t), y, tx(t), y + (7 if k % 2 == 0 else 4), K, 1.4)
        if k % 2 == 0:
            b += txt(tx(t), y + 22, f"{t:.1f}".replace(".", ","), K, 11, "middle", "400")
    b += txt(398, y - 10, "t (s)", K, 11, "end", "400")
    return b

def d5(kk):
    p = f"d5{kk}"; K = "currentColor"
    if kk == 0:
        b = txt(16, 24, "Năm lần đo thời gian t", K, 13) + txt(16, 44, "ĐCNN của đồng hồ : 0,1 s", K, 13, "start", "400")
        b += txt(250, 24, "t_tb = ?", ORG, 13) + txt(250, 44, "Δt = ?", ORG, 13) + axis5()
        for k, t in enumerate(T5):
            f = (k + 1) / 6
            kt = [0, f, min(f + 0.03, 1)]
            b += (f'<g opacity="0">{circ(tx(t), 118, 6, BLUE, 2, BLUE)}{txt(tx(t), 98, str(k + 1), BLUE, 13, "middle")}'
                  f'{anim("opacity", [0, 0, 1], 5, kt, "{:g}")}</g>')
        return fig("c0-5-0", "0 0 420 166", "Năm kết quả đo thời gian xếp trên trục thời gian từ 2,0 đến 3,2 giây",
                   b, "Mô phỏng: năm lần đo lần lượt hiện lên trục thời gian (số trên chấm là thứ tự lần đo).")
    b = txt(16, 24, "t_tb = (t_1 + … + t_5) / 5", K, 13) + txt(16, 46, "Δt_ng = (Σ|t_i − t_tb|) / 5", K, 13)
    b += txt(16, 68, "Δt = Δt_ng + Δt_dc ,  Δt_dc = ½ ĐCNN", K, 13) + txt(16, 90, "δ = Δt / t_tb · 100%", ORG, 13)
    yb = 150
    b += seg(150, yb, 270, yb, BLUE, 3) + seg(150, yb - 8, 150, yb + 8, BLUE, 3) + seg(270, yb - 8, 270, yb + 8, BLUE, 3) + seg(210, yb - 8, 210, yb + 8, K, 2.4)
    b += txt(210, yb - 14, "t_tb", K, 13, "middle") + txt(150, yb + 24, "t_tb − Δt", BLUE, 12, "middle") + txt(270, yb + 24, "t_tb + Δt", BLUE, 12, "middle")
    b += txt(16, yb + 52, "Ghi kết quả : t = t_tb ± Δt", K, 13, "start", "400")
    return fig("c0-5-2", "0 0 420 218", "Các công thức tính giá trị trung bình, sai số tuyệt đối, sai số tương đối và khoảng giá trị t trung bình cộng trừ delta t",
               b, "Dữ kiện: kết quả đo là một khoảng quanh giá trị trung bình. " + NOTE)


# ───────────── Dạng 6 ─────────────
def d6(kk):
    p = f"d6{kk}"; K = "currentColor"
    if kk == 0:
        b = R(30, 74, 90, 66, K, 2.4, "none", 8) + poly([(120, 90), (140, 80), (146, 84)], K, 2.4) + f'<path d="M30,88 C8,88 8,126 30,126" fill="none" stroke="{K}" stroke-width="2.4"/>'
        b += seg(60, 140, 60, 156, K, 2.2) + seg(60, 156, 40, 156, K, 2.2) + txt(30, 176, "220 V – 1800 W", K, 12, "start", "400") + txt(30, 192, "H = 84%", K, 12, "start", "400")
        b += R(212, 30, 16, 120, K, 2.2, "none", 8) + circ(220, 160, 13, RED, 2.2, RED)
        b += (f'<rect x="216" y="128" width="8" height="22" fill="{RED}">{anim("y", [128, 40], 6)}{anim("height", [22, 110], 6)}</rect>')
        b += seg(232, 40, 240, 40, K, 1.6) + txt(244, 44, "100 °C", K, 12, "start", "400") + seg(232, 128, 240, 128, K, 1.6) + txt(244, 132, "20 °C", K, 12, "start", "400")
        b += txt(290, 30, "1,8 lít nước", K, 13, "start", "400") + txt(290, 74, "t = ?", ORG, 14) + txt(290, 98, "tiền điện 30 ngày = ?", ORG, 13)
        b += txt(290, 122, "t′ ở 110 V = ?", ORG, 13)
        return fig("c0-6-0", "0 0 420 200", "Ấm điện đun 1,8 lít nước; nhiệt kế cho thấy nhiệt độ nước tăng từ 20 độ C lên 100 độ C",
                   b, "Mô phỏng: nhiệt độ nước tăng từ 20 °C đến 100 °C (không theo thời gian thật; thời gian đun là điều cần tìm).")
    boxes = [("khối lượng", "m = D·V"), ("nhiệt có ích", "Q = m·c·Δt"), ("điện năng", "A = Q / H"), ("thời gian", "t = A / P")]
    b = ""
    for i, (a, c) in enumerate(boxes):
        x = 12 + i * 104
        b += txt(x + 43, 22, a, K, 12, "middle", "400") + R(x, 30, 86, 40, K, 2.2, "none", 8) + txt(x + 43, 55, c, ORG if i == 2 else K, 13, "middle")
        if i < 3:
            b += arrow("", "b", x + 88, 50, x + 102, 50, 2)
    b += txt(16, 106, "⚠ A là điện năng (toàn phần), Q là nhiệt có ích", K, 13, "start", "400")
    b += txt(16, 128, "1 kWh = 3,6·10⁶ J", K, 13, "start", "400")
    b += txt(16, 150, "R không đổi : P = U²/R, tỉ lệ với U²", K, 13, "start", "400")
    b += txt(16, 172, "U giảm 2 lần → P giảm 4 lần", K, 13, "start", "400")
    return fig("c0-6-2", "0 0 420 186", "Chuỗi tính từ khối lượng nước đến nhiệt có ích, điện năng và thời gian đun",
               b, "Dữ kiện: chuỗi tính từ khối lượng nước đến thời gian đun. " + NOTE)


BUILD = [d1, d2, d3, d4, d5, d6]


# ═════════════ BẢNG PHÂN TÍCH ĐỀ ═════════════
ANALYSIS = [
 [(r'"điện trở $R$ không đổi"', r"$R$ không đổi", r"⚠ Chỉ khi $R$ không đổi mới có $I$ tỉ lệ thuận $U$ ; lập tỉ số để $R$ triệt tiêu"),
  (r'"$U_1=4{,}5$ V thì $I_1=0{,}18$ A"', r"$U_1=4{,}5$ V ; $I_1=0{,}18$ A", r"$I=\dfrac{U}{R}$ cho trạng thái 1"),
  (r'"khi hiệu điện thế là $U_2=6{,}0$ V"', r"$U_2=6{,}0$ V", r"$I=\dfrac{U}{R}$ cho trạng thái 2 ; chia vế theo vế"),
  (r'"biến trở nối tiếp $R_0=10\ \Omega$ … $R_1=20\ \Omega$ … $R_2=50\ \Omega$"', r"$R_0=10\ \Omega$ ; $R_1=20\ \Omega$ ; $R_2=50\ \Omega$ ; $I_1=0{,}4$ A", r"⚠ Điện trở toàn mạch là $R_0+R$ ; $I$ tỉ lệ nghịch với tổng này, không phải với riêng $R$"),
  (r'"nguồn có hiệu điện thế $U$ không đổi"', r"$U$ giữ nguyên ở hai trạng thái", r"$U=I\,(R_0+R)$"),
  (r'"dòng điện từ $0{,}20$ A lên $0{,}30$ A … $20\ \Omega$ … $0{,}80$ W"', r"$R=20\ \Omega$ ; $I_1=0{,}20$ A ; $I_2=0{,}30$ A ; $P_1=0{,}80$ W", r"$P=I^2R$ ; $R$ không đổi nên tỉ số phải bình phương"),
  (r'"công suất tăng bao nhiêu lần … bằng bao nhiêu oát"', r"Cần $\dfrac{P_2}{P_1}$ và $P_2$", r"$\dfrac{P_2}{P_1}=\left(\dfrac{I_2}{I_1}\right)^2$")],
 [(r'"công thức $P=\dfrac{U^2}{R}$ … đơn vị oát"', r"Hai vế phải cùng đơn vị", r"⚠ Thay đơn vị từng đại lượng rồi rút gọn như đại số ; đúng đơn vị chưa chắc đúng hệ số"),
  (r'"$3{,}6$ km trong $40$ phút"', r"$s=3{,}6$ km ; $t=40$ phút", r"⚠ Đổi về m và s trước khi chia ; $v=\dfrac{s}{t}$"),
  (r'"tốc độ theo m/s và theo km/h … hợp lí"', r"Cần $v$ (m/s), $v$ (km/h)", r"$1\ \text{m/s}=3{,}6\ \text{km/h}$ ; so với mốc quen thuộc của người đi bộ"),
  (r'"lò sưởi $220\ \text{V}-2\ \text{kW}$ … $3$ giờ"', r"$P=2$ kW ; $U=220$ V ; $t=3$ h", r"⚠ Dùng đúng hiệu điện thế định mức nên công suất bằng số ghi ; $A=P\,t$"),
  (r'"điện năng theo kWh và theo J"', r"Cần $A$ (kWh), $A$ (J)", r"$A=P\,t$ ; $1\ \text{kWh}=3{,}6\cdot10^6\ \text{J}$"),
  (r'"cường độ dòng điện qua lò sưởi"', r"Cần $I$", r"$P=U\,I$ nên $I=\dfrac{P}{U}$ (đổi kW ra W)"),
  (r'"nhận xét độ lớn"', r"So với mốc đời sống", r"Bóng đèn cỡ vài phần mười ampe ; thiết bị toả nhiệt công suất lớn cỡ vài ampe đến chục ampe")],
 [(r'"trục hoành là $I$, trục tung là $U$"', r"Trục hoành $I$ (A) ; trục tung $U$ (V)", r"⚠ Đọc đúng trục trước : hệ số góc của $U$–$I$ là $R$, của $I$–$U$ là $\dfrac{1}{R}$"),
  (r'"dây A : $I=0{,}10\dots0{,}40$ A ; $U=1{,}2\dots4{,}8$ V"', r"4 điểm thẳng hàng, qua gốc", r"$U$ tỉ lệ thuận $I$ ; $R=\dfrac{U}{I}=\dfrac{\Delta U}{\Delta I}$"),
  (r'"dây B : $I=0{,}05\dots0{,}20$ A ; $U=1{,}5\dots6{,}0$ V"', r"4 điểm thẳng hàng, qua gốc", r"$R=\dfrac{\Delta U}{\Delta I}$"),
  (r'"đường của dây nào dốc hơn"', r"So hệ số góc hai đường", r"Dốc hơn ⇔ hệ số góc lớn hơn ⇔ $R$ lớn hơn"),
  (r'"nội suy … dây A khi $U=2{,}7$ V"', r"$U=2{,}7$ V nằm giữa hai điểm đo", r"⚠ Nội suy chỉ dùng trong khoảng đã đo ; $I=\dfrac{U}{R}$ hoặc nội suy tuyến tính hai điểm kề"),
  (r'"đồ thị $I$–$U$ cho dây A … hệ số góc"', r"Đổi vai hai trục", r"$k=\dfrac{\Delta I}{\Delta U}=\dfrac{1}{R}$ (đơn vị A/V)"),
  (r'"ngoại suy … dây B khi $I=0{,}25$ A"', r"$I=0{,}25$ A vượt điểm đo cuối", r"⚠ Ngoại suy chỉ khi vượt ngắn và đường đã rõ dạng ; ghi rõ là giá trị dự đoán")],
 [(r'"luôn theo một chiều … bốn giai đoạn liên tiếp"', r"4 hình chữ nhật dưới đồ thị $v$–$t$", r"⚠ Quãng đường bằng diện tích dưới đồ thị $v$–$t$ chỉ khi không đổi chiều"),
  (r'"$0$ đến $20$ s : $4$ m/s"', r"$v_1=4$ m/s ; $t_1=20$ s", r"$s_1=v_1t_1$"),
  (r'"$20$ s đến $35$ s : $6$ m/s"', r"$v_2=6$ m/s ; $t_2=15$ s", r"$s_2=v_2t_2$ ; $t_2$ là độ dài đoạn (mốc cuối trừ mốc đầu)"),
  (r'"$35$ s đến $45$ s : dừng ở đèn đỏ"', r"$v_3=0$ ; $t_3=10$ s", r"⚠ Đoạn dừng có diện tích 0 nhưng vẫn tính vào thời gian"),
  (r'"$45$ s đến $65$ s : $5$ m/s"', r"$v_4=5$ m/s ; $t_4=20$ s", r"$s_4=v_4t_4$"),
  (r'"tổng quãng đường … tốc độ trung bình"', r"Cần $s$ và $v_{tb}$", r"$s=s_1+s_2+s_3+s_4$ ; $v_{tb}=\dfrac{s}{t}$ (tổng chia tổng)"),
  (r'"lúc $t=50$ s … cách điểm xuất phát"', r"$t=50$ s", r"Cộng diện tích đến thời điểm đó"),
  (r'"đi được $150$ m đầu tiên vào thời điểm nào"', r"$s=150$ m", r"Tìm giai đoạn chứa $150$ m rồi giải $s=v\,t$ trong đoạn đó")],
 [(r'"đồng hồ bấm giây có ĐCNN $0{,}1$ s"', r"$\text{ĐCNN}=0{,}1$ s", r"⚠ Dụng cụ chỉ có vạch chia thì sai số dụng cụ bằng nửa ĐCNN"),
  (r'"năm lần đo : $2{,}4$ ; $2{,}7$ ; $2{,}5$ ; $2{,}3$ ; $2{,}6$"', r"$n=5$ giá trị $t_i$", r"$t_{tb}=\dfrac{\sum t_i}{n}$ ; độ lệch $|t_i-t_{tb}|$ lấy trị tuyệt đối"),
  (r'"sai số tuyệt đối $\Delta t$ … làm tròn một chữ số có nghĩa"', r"Cần $\Delta t$", r"$\Delta t=\Delta t_{ng}+\Delta t_{dc}$"),
  (r'"sai số tương đối $\delta_t$"', r"Cần $\delta_t$", r"$\delta_t=\dfrac{\Delta t}{t_{tb}}\cdot100\%$"),
  (r'"ghi kết quả đo $t$ đúng quy cách"', r"Cần $t=t_{tb}\pm\Delta t$", r"⚠ Giá trị trung bình làm tròn cùng hàng thập phân với sai số"),
  (r'"$s=1{,}20$ m, $\Delta s=0{,}01$ m"', r"$s=1{,}20$ m ; $\Delta s=0{,}01$ m", r"$\delta_s=\dfrac{\Delta s}{s}$ ; phép chia cộng các sai số tương đối : $\delta_v=\delta_s+\delta_t$"),
  (r'"tốc độ $v=\dfrac{s}{t}$ và sai số $\Delta v$"', r"Cần $v$, $\Delta v$", r"$v=\dfrac{s}{t_{tb}}$ ; $\Delta v=v\,\delta_v$")],
 [(r'"ấm $220\ \text{V}-1800\ \text{W}$ dùng ở $220\ \text{V}$"', r"$U=220$ V ; $P=1800$ W", r"⚠ Đúng hiệu điện thế định mức nên công suất thực bằng công suất ghi"),
  (r'"$1{,}8$ lít nước từ $20\ ^\circ\text{C}$ đến $100\ ^\circ\text{C}$"', r"$V=1{,}8$ lít ; $t_1=20\ ^\circ\text{C}$ ; $t_2=100\ ^\circ\text{C}$ ; $D=1000\ \text{kg/m}^3$", r"$m=D\,V$ (đổi lít ra $\text{m}^3$) ; $Q_{ich}=m\,c\,\Delta t$"),
  (r'"hiệu suất $84\%$"', r"$H=0{,}84$", r"⚠ $H=\dfrac{Q_{ich}}{A}$ : $A$ là điện năng toàn phần, lớn hơn nhiệt có ích"),
  (r'"thời gian đun"', r"Cần $t$", r"$A=P\,t$ nên $t=\dfrac{A}{P}$ (J và W)"),
  (r'"hai lần mỗi ngày, $30$ ngày, $2000$ đồng một kWh"', r"$2\cdot30$ lần ; giá $2000$ đồng/kWh", r"$1\ \text{kWh}=3{,}6\cdot10^6\ \text{J}$ ; tiền $=A_{kWh}\cdot$ giá"),
  (r'"cắm nhầm vào nguồn $110$ V"', r"$U'=110$ V ; $R$ và $H$ không đổi", r"⚠ $P=\dfrac{U^2}{R}$ : công suất tỉ lệ với $U^2$ ; rút tỉ số $\dfrac{P'}{P}$"),
  (r'"thời gian đun mỗi lần ở $110$ V"', r"Cần $t'$", r"Cùng điện năng $A$ : $t'=\dfrac{A}{P'}$")],
]


# ═════════════ LỜI GIẢI (mỗi bước một khối, mỗi công thức một dòng) ═════════════
R1 = [r"<strong>Khái niệm:</strong> hai đại lượng tỉ lệ thuận khi thương không đổi ($y=kx$), tỉ lệ nghịch khi tích không đổi ($y=\dfrac{k}{x}$).",
      r"<strong>Định luật:</strong> $I=\dfrac{U}{R}$ ; với hai trạng thái của cùng một hệ, chia vế theo vế để hằng số triệt tiêu.",
      r"<strong>Công thức:</strong> $P=I^2R$ nên $\dfrac{P_2}{P_1}=\left(\dfrac{I_2}{I_1}\right)^2$ khi $R$ không đổi.",
      r"⚠ <strong>Điều kiện:</strong> chỉ lập tỉ số trực tiếp khi đại lượng ở mẫu là đại lượng duy nhất thay đổi ; mạch có biến trở nối tiếp thì $I$ tỉ lệ nghịch với tổng $R_0+R$."]
R2 = [r"<strong>Khái niệm:</strong> hai vế của một công thức đúng phải có cùng đơn vị (thứ nguyên).",
      r"<strong>Công thức:</strong> $P=UI=\dfrac{U^2}{R}$ ; $A=P\,t$ ; $v=\dfrac{s}{t}$.",
      r"$1\ \text{m/s}=3{,}6\ \text{km/h}$ ; $1\ \text{kWh}=3{,}6\cdot10^6\ \text{J}$ ; $1\ \text{kW}=1000\ \text{W}$.",
      r"⚠ <strong>Điều kiện:</strong> đổi mọi đại lượng về cùng hệ đơn vị trước khi thay số ; kiểm tra đơn vị không bắt được sai hệ số, nên cần thêm kiểm tra độ lớn."]
R3 = [r"<strong>Khái niệm:</strong> dây dẫn tuân theo định luật Ôm có $U$ tỉ lệ thuận $I$ : đồ thị là đường thẳng qua gốc toạ độ.",
      r"<strong>Định luật:</strong> $R=\dfrac{U}{I}$ ; trên đồ thị $U$–$I$ hệ số góc $\dfrac{\Delta U}{\Delta I}=R$ (V/A = Ω) ; trên đồ thị $I$–$U$ hệ số góc là $\dfrac{1}{R}$.",
      r"<strong>Công thức:</strong> nội suy tuyến tính $y=y_1+(y_2-y_1)\dfrac{x-x_1}{x_2-x_1}$.",
      r"⚠ <strong>Điều kiện:</strong> đọc đúng trục trước ; nội suy chỉ trong khoảng đã đo ; giá trị ngoại suy phải ghi rõ là dự đoán."]
R4 = [r"<strong>Khái niệm:</strong> trên đồ thị $v$–$t$, diện tích giữa đường biểu diễn và trục hoành là quãng đường ; đoạn dừng có diện tích bằng 0.",
      r"<strong>Công thức:</strong> mỗi giai đoạn đều $s_k=v_k\,t_k$ (hình chữ nhật) ; $v_{tb}=\dfrac{s_{\text{tổng}}}{t_{\text{tổng}}}$.",
      r"Độ dài mỗi giai đoạn $t_k$ bằng mốc cuối trừ mốc đầu.",
      r"⚠ <strong>Điều kiện:</strong> quãng đường bằng diện tích khi xe không đổi chiều ; thời gian dừng vẫn tính vào $t_{\text{tổng}}$ ; không lấy trung bình cộng các vận tốc."]
R5 = [r"<strong>Khái niệm:</strong> sai số ngẫu nhiên do mỗi lần đo khác nhau một chút ; sai số dụng cụ do vạch chia của dụng cụ.",
      r"<strong>Công thức:</strong> $t_{tb}=\dfrac{\sum t_i}{n}$ ; $\Delta t_{ng}=\dfrac{\sum|t_i-t_{tb}|}{n}$ ; $\Delta t_{dc}=\dfrac{\text{ĐCNN}}{2}$ ; $\Delta t=\Delta t_{ng}+\Delta t_{dc}$ ; $\delta=\dfrac{\Delta t}{t_{tb}}$.",
      r"Phép chia $v=\dfrac{s}{t}$ : $\delta_v=\delta_s+\delta_t$ và $\Delta v=v\,\delta_v$.",
      r"⚠ <strong>Điều kiện:</strong> độ lệch lấy trị tuyệt đối ; sai số làm tròn đến một chữ số có nghĩa, giá trị trung bình làm tròn cùng hàng thập phân với sai số."]
R6 = [r"<strong>Khái niệm:</strong> nhiệt lượng có ích làm nóng nước ; điện năng là năng lượng toàn phần ấm tiêu thụ ; hiệu suất đo phần có ích.",
      r"<strong>Công thức:</strong> $m=D\,V$ ; $Q_{ich}=m\,c\,\Delta t$ ; $H=\dfrac{Q_{ich}}{A}$ ; $A=P\,t$ ; $P=\dfrac{U^2}{R}$.",
      r"$1\ \text{lít}=10^{-3}\ \text{m}^3$ ; $1\ \text{kWh}=3{,}6\cdot10^6\ \text{J}$.",
      r"⚠ <strong>Điều kiện:</strong> dùng đúng hiệu điện thế định mức thì công suất bằng số ghi ; đổi mọi đại lượng về SI rồi mới thay số ; giữ ký hiệu chữ đến bước cuối."]

SOLS = [
 sol(R1, [
  ("Lập tỉ số cho dây dẫn", [P(r"$R$ không đổi nên $I$ tỉ lệ thuận với $U$:"), M(r"\dfrac{I_2}{I_1}=\dfrac{U_2}{U_1}"),
     M(r"I_2=I_1\,\dfrac{U_2}{U_1}=0{,}18\cdot\dfrac{6{,}0}{4{,}5}"), A(r"I_2=0{,}24\ \text{A}")]),
  ("Hiệu điện thế của nguồn", [P(r"Hai điện trở nối tiếp, điện trở toàn mạch là $R_0+R_1$:"), M(r"U=I_1\,(R_0+R_1)=0{,}4\cdot(10+20)"), A(r"U=12\ \text{V}")]),
  ("Dòng điện khi tăng biến trở", [P(r"$U$ không đổi, điện trở toàn mạch lúc sau là $R_0+R_2$:"), M(r"I_2=\dfrac{U}{R_0+R_2}=\dfrac{12}{10+50}"), A(r"I_2=0{,}2\ \text{A}"),
     P(r"Cách viết $\dfrac{I_2}{I_1}=\dfrac{R_1}{R_2}$ cho $0{,}16\ \text{A}$ : <strong>sai</strong>, vì còn $R_0$ nối tiếp không đổi."),
     P(r"Tỉ số đúng là $\dfrac{I_2}{I_1}=\dfrac{R_0+R_1}{R_0+R_2}=\dfrac{30}{60}$.")]),
  ("Công suất khi dòng điện tăng", [P(r"$R$ không đổi, $P=I^2R$ nên:"), M(r"\dfrac{P_2}{P_1}=\left(\dfrac{I_2}{I_1}\right)^2=\left(\dfrac{0{,}30}{0{,}20}\right)^2=2{,}25"),
     M(r"P_2=2{,}25\cdot0{,}80"), A(r"P_2=1{,}8\ \text{W}"), P("Dòng điện tăng 1,5 lần thì công suất tăng 2,25 lần, không phải 1,5 lần.")]),
  ("Kiểm tra", [P(r"Câu a: $R=\dfrac{4{,}5}{0{,}18}=25\ \Omega$ và $\dfrac{6{,}0}{0{,}24}=25\ \Omega$ ✓ cùng một giá trị."),
     P(r"Câu b: điện trở toàn mạch tăng từ $30\ \Omega$ lên $60\ \Omega$ (gấp 2) nên dòng điện giảm một nửa, từ $0{,}4\ \text{A}$ xuống $0{,}2\ \text{A}$ ✓."),
     P(r"Câu c: $0{,}20^2\cdot20=0{,}80\ \text{W}$ và $0{,}30^2\cdot20=1{,}8\ \text{W}$ ✓.")])],
  [r"a) $I_2=0{,}24\ \text{A}$", r"b) Cách viết của bạn sai ; $U=12\ \text{V}$ và $I_2=0{,}2\ \text{A}$", r"c) Công suất tăng $2{,}25$ lần ; $P_2=1{,}8\ \text{W}$"],
  r"Nhận dạng: <strong>hai trạng thái của cùng một hệ</strong> → chia hai phương trình vế theo vế ; <strong>biến trở nối tiếp</strong> → tỉ lệ nghịch với $R_0+R$, không phải $R$ riêng."),
 sol(R2, [
  ("Thứ nguyên của $P=U^2/R$", [P("Thay đơn vị rồi rút gọn như phân số đại số:"), M(r"\dfrac{\text{V}^2}{\Omega}=\text{V}\cdot\dfrac{\text{V}}{\Omega}=\text{V}\cdot\text{A}"),
     A(r"\text{V}\cdot\text{A}=\text{W}"), P("Vế phải có đơn vị oát, đúng bằng đơn vị công suất : công thức hợp lí về đơn vị.")]),
  ("Tốc độ đi bộ", [P(r"Đổi $s=3{,}6\ \text{km}=3600\ \text{m}$ ; $t=40\ \text{phút}=2400\ \text{s}$."), M(r"v=\dfrac{s}{t}=\dfrac{3600}{2400}"), A(r"v=1{,}5\ \text{m/s}"),
     M(r"v=1{,}5\cdot3{,}6=5{,}4\ \text{km/h}"), P(r"Người đi bộ thông thường đi cỡ $4$ đến $6\ \text{km/h}$ : kết quả hợp lí.")]),
  ("Điện năng theo kWh", [P("Công suất theo kW và thời gian theo giờ thì điện năng ra thẳng kWh:"), M(r"A=P\,t=2\cdot3"), A(r"A=6\ \text{kWh}")]),
  ("Đổi ra jun", [M(r"A=6\cdot3{,}6\cdot10^6=21{,}6\cdot10^6\ \text{J}"), A(r"A=21{,}6\ \text{MJ}=2{,}16\cdot10^7\ \text{J}"),
     P(r"Kiểm tra theo SI: $2000\ \text{W}\cdot10800\ \text{s}=2{,}16\cdot10^7\ \text{J}$ ✓.")]),
  ("Cường độ dòng điện", [P(r"Đổi $P=2\ \text{kW}=2000\ \text{W}$ ; lò dùng đúng $220\ \text{V}$:"), M(r"I=\dfrac{P}{U}=\dfrac{2000}{220}"), A(r"I\approx9{,}09\ \text{A}")]),
  ("Kiểm tra", [P("Bóng đèn dây tóc cỡ vài phần mười ampe ; lò sưởi $2\\ \\text{kW}$ cỡ vài ampe đến chục ampe : $9{,}09\\ \\text{A}$ hợp lí."),
     P(r"Nếu ra $0{,}09\ \text{A}$ hay $909\ \text{A}$ thì đã sai một bậc thập phân (quên đổi kW ra W, hoặc đổi ngược)."),
     P("Dây dẫn cấp điện cho lò phải chịu được dòng gần $10\\ \\text{A}$.")])],
  [r"a) $\dfrac{\text{V}^2}{\Omega}=\text{V}\cdot\text{A}=\text{W}$ : đúng đơn vị", r"b) $v=1{,}5\ \text{m/s}=5{,}4\ \text{km/h}$ ; hợp lí", r"c) $A=6\ \text{kWh}=21{,}6\ \text{MJ}$", r"d) $I\approx9{,}09\ \text{A}$ ; hợp lí"],
  r"Nhận dạng: đề có <strong>kWh, km/h, phút</strong> → đổi về SI trước khi thay số ; gặp <strong>công thức lạ</strong> → kiểm tra đơn vị hai vế rồi kiểm tra độ lớn."),
 sol(R3, [
  ("Điện trở dây A", [P(r"Lấy một điểm trên đường thẳng, ví dụ $(0{,}40\ \text{A};\ 4{,}8\ \text{V})$:"), M(r"R_A=\dfrac{U}{I}=\dfrac{4{,}8}{0{,}40}"), A(r"R_A=12\ \Omega"),
     P(r"Điểm $(0{,}10;\ 1{,}2)$ cho $\dfrac{1{,}2}{0{,}10}=12\ \Omega$ : khớp, hệ số góc $\dfrac{\Delta U}{\Delta I}$ không đổi.")]),
  ("Điện trở dây B", [P(r"Điểm cuối $(0{,}20\ \text{A};\ 6{,}0\ \text{V})$:"), M(r"R_B=\dfrac{U}{I}=\dfrac{6{,}0}{0{,}20}"), A(r"R_B=30\ \Omega")]),
  ("So sánh độ dốc", [P("Hệ số góc của đồ thị $U$–$I$ chính là $R$:"), M(r"R_B=30\ \Omega\gt R_A=12\ \Omega"),
     A("T:Đường của dây B <strong>dốc hơn</strong> : cùng cường độ $I$ thì $U$ của dây B lớn hơn."), P("Độ dốc không phụ thuộc đường vẽ dài hay ngắn.")]),
  ("Nội suy cường độ dòng điện", [P(r"$U=2{,}7\ \text{V}$ nằm giữa hai điểm đo $(0{,}20;\ 2{,}4)$ và $(0{,}30;\ 3{,}6)$."),
     M(r"I=0{,}20+(0{,}30-0{,}20)\cdot\dfrac{2{,}7-2{,}4}{3{,}6-2{,}4}"), M(r"I=0{,}20+0{,}10\cdot0{,}25"), A(r"I=0{,}225\ \text{A}"),
     P(r"Cách khác : $I=\dfrac{U}{R_A}=\dfrac{2{,}7}{12}=0{,}225\ \text{A}$ ✓.")]),
  ("Hệ số góc của đồ thị I–U", [P("Đổi hai trục thì hệ số góc thành nghịch đảo:"), M(r"k=\dfrac{\Delta I}{\Delta U}=\dfrac{1}{R_A}=\dfrac{1}{12}"), A(r"k\approx0{,}0833\ \text{A/V}"),
     P(r"Đơn vị $\text{A/V}=\dfrac{1}{\Omega}$.")]),
  ("Ngoại suy hiệu điện thế", [P(r"$I=0{,}25\ \text{A}$ vượt điểm đo cuối ($0{,}20\ \text{A}$) một đoạn ngắn ; đường thẳng qua gốc nên:"), M(r"U=I\,R_B=0{,}25\cdot30"), A(r"U=7{,}5\ \text{V}"),
     P("Đây là giá trị dự đoán (ngoại suy), cần kiểm tra bằng phép đo thực.")]),
  ("Kiểm tra", [P(r"Dây A: $\dfrac{3{,}6}{0{,}30}=12\ \Omega$ và $\dfrac{2{,}4}{0{,}20}=12\ \Omega$ ✓ ; dây B: $\dfrac{4{,}5}{0{,}15}=30\ \Omega$ ✓."),
     P(r"Đồ thị $I$–$U$ của dây B có hệ số góc $\dfrac{1}{30}\approx0{,}033\ \text{A/V}$, nhỏ hơn của dây A : dây có $R$ lớn thì dốc hơn trên đồ thị $U$–$I$ và thoải hơn trên đồ thị $I$–$U$."),
     P("Đọc nhầm trục là lỗi mất điểm phổ biến nhất của dạng này.")])],
  [r"a) $R_A=12\ \Omega$ ; $R_B=30\ \Omega$", r"b) Đường của dây B dốc hơn", r"c) $I=0{,}225\ \text{A}$", r"d) $k\approx0{,}0833\ \text{A/V}$", r"e) $U\approx7{,}5\ \text{V}$ (giá trị dự đoán)"],
  r"Nhận dạng: <strong>đồ thị $U$–$I$ là đường thẳng qua gốc</strong> → hệ số góc là $R$ ; đổi sang <strong>$I$–$U$</strong> thì hệ số góc là $\dfrac{1}{R}$."),
 sol(R4, [
  ("Tổng quãng đường", [P(r"Độ dài các giai đoạn: $20\ \text{s}$, $15\ \text{s}$, $10\ \text{s}$, $20\ \text{s}$."), M(r"s_1=4\cdot20=80\ \text{m}"), M(r"s_2=6\cdot15=90\ \text{m}"),
     M(r"s_3=0\cdot10=0\ \text{m}"), M(r"s_4=5\cdot20=100\ \text{m}"), M(r"s=80+90+0+100"), A(r"s=270\ \text{m}")]),
  ("Tốc độ trung bình", [P(r"Tổng thời gian, kể cả lúc dừng:"), M(r"t=65\ \text{s}"), M(r"v_{tb}=\dfrac{s}{t}=\dfrac{270}{65}"), A(r"v_{tb}\approx4{,}15\ \text{m/s}"),
     P(r"Trung bình cộng bốn vận tốc cho $3{,}75\ \text{m/s}$ : <strong>sai</strong>, vì các giai đoạn dài ngắn khác nhau."),
     P(r"Bỏ $10\ \text{s}$ dừng sẽ ra $4{,}91\ \text{m/s}$ : <strong>sai</strong>, thời gian dừng vẫn tính.")]),
  ("Vị trí lúc $t=50$ s", [P(r"Đến $t=45\ \text{s}$ xe đã đi $80+90+0=170\ \text{m}$ ; từ giây 45 đến giây 50 xe chạy $5\ \text{m/s}$ trong $5\ \text{s}$."),
     M(r"s(50)=170+5\cdot(50-45)"), A(r"s(50)=195\ \text{m}")]),
  ("Thời điểm đi được 150 m", [P(r"Hết giai đoạn 1 xe đi $80\ \text{m}$ ($t=20\ \text{s}$) ; hết giai đoạn 2 xe đi $170\ \text{m}$ : mốc $150\ \text{m}$ nằm trong giai đoạn 2."),
     M(r"s_{\text{còn}}=150-80=70\ \text{m},\qquad v=6\ \text{m/s}"), M(r"\Delta t=\dfrac{70}{6}\approx11{,}67\ \text{s}"), M(r"t=20+11{,}67"), A(r"t\approx31{,}7\ \text{s}")]),
  ("Kiểm tra", [P(r"Đồ thị $s$–$t$ có hệ số góc $4$, $6$, $0$, $5\ \text{m/s}$ trên bốn đoạn và kết thúc ở $270\ \text{m}$ ✓."),
     P(r"$s(31{,}7)=80+6\cdot11{,}7\approx150\ \text{m}$ ✓ ; $v_{tb}=4{,}15\ \text{m/s}$ nằm giữa $0$ và $6\ \text{m/s}$ ✓."),
     P("Quãng đường cộng dồn theo thời gian không bao giờ giảm (xe không đổi chiều).")])],
  [r"a) $s=270\ \text{m}$", r"b) $v_{tb}\approx4{,}15\ \text{m/s}$", r"c) $s(50)=195\ \text{m}$", r"d) $t\approx31{,}7\ \text{s}$"],
  r"Nhận dạng: đề cho <strong>đồ thị $v$–$t$ bậc thang</strong> → mỗi bậc là một hình chữ nhật, diện tích là quãng đường ; <strong>tốc độ trung bình</strong> = tổng quãng đường chia tổng thời gian (kể cả lúc dừng)."),
 sol(R5, [
  ("Giá trị trung bình", [M(r"t_{tb}=\dfrac{2{,}4+2{,}7+2{,}5+2{,}3+2{,}6}{5}=\dfrac{12{,}5}{5}"), A(r"t_{tb}=2{,}50\ \text{s}")]),
  ("Sai số ngẫu nhiên", [P("Độ lệch tuyệt đối của từng lần so với giá trị trung bình:"), M(r"0{,}1;\ \ 0{,}2;\ \ 0;\ \ 0{,}2;\ \ 0{,}1\ \ (\text{s})"),
     M(r"\Delta t_{ng}=\dfrac{0{,}1+0{,}2+0+0{,}2+0{,}1}{5}=\dfrac{0{,}6}{5}"), A(r"\Delta t_{ng}=0{,}12\ \text{s}")]),
  ("Sai số tuyệt đối", [P("Sai số dụng cụ bằng nửa ĐCNN:"), M(r"\Delta t_{dc}=\dfrac{0{,}1}{2}=0{,}05\ \text{s}"), M(r"\Delta t=0{,}12+0{,}05=0{,}17\ \text{s}"),
     P("Làm tròn đến một chữ số có nghĩa:"), A(r"\Delta t\approx0{,}2\ \text{s}"),
     P(r"Bỏ sai số dụng cụ sẽ ra $0{,}12\ \text{s}$, làm tròn thành $0{,}1\ \text{s}$ : <strong>sai</strong>.")]),
  ("Sai số tương đối và ghi kết quả", [M(r"\delta_t=\dfrac{\Delta t}{t_{tb}}\cdot100\%=\dfrac{0{,}17}{2{,}50}\cdot100\%"), A(r"\delta_t\approx7\%"),
     P(r"Dùng $\Delta t$ chưa làm tròn ($0{,}17\ \text{s}$) ; dùng $0{,}2\ \text{s}$ đã làm tròn sẽ ra $8\%$, lệch thêm một chút."),
     P("Giá trị trung bình làm tròn cùng hàng thập phân với sai số:"), A(r"t=2{,}5\ \text{s}\pm0{,}2\ \text{s}")]),
  ("Sai số của tốc độ", [M(r"\delta_s=\dfrac{0{,}01}{1{,}20}\approx0{,}83\%"), M(r"v=\dfrac{s}{t_{tb}}=\dfrac{1{,}20}{2{,}50}=0{,}48\ \text{m/s}"),
     P("Phép chia cộng các sai số tương đối:"), M(r"\delta_v=\delta_s+\delta_t\approx0{,}83\%+6{,}8\%\approx7{,}6\%"),
     M(r"\Delta v=v\,\delta_v\approx0{,}48\cdot0{,}076\approx0{,}037\ \text{m/s}"), A(r"\Delta v\approx0{,}04\ \text{m/s}"), A(r"v=0{,}48\ \text{m/s}\pm0{,}04\ \text{m/s}")]),
  ("Kiểm tra", [P(r"Ghi đúng quy cách : $t=2{,}5\ \text{s}\pm0{,}2\ \text{s}$ (không ghi $2{,}50\pm0{,}2$) ; $v=0{,}48\ \text{m/s}\pm0{,}04\ \text{m/s}$ cùng hàng thập phân."),
     P(r"Sai số ngẫu nhiên ($0{,}12\ \text{s}$) lớn hơn sai số dụng cụ ($0{,}05\ \text{s}$) : thao tác bấm đồng hồ mới là nguồn sai số chính."),
     P(r"Sai số tương đối của $t$ (cỡ $7\%$) lớn hơn của $s$ (cỡ $0{,}8\%$) nên quyết định sai số của $v$."),
     P(r"Quy ước một chữ số có nghĩa cho sai số là cách ghi thông dụng ở trường ; đề yêu cầu hai chữ số thì làm theo đề.")])],
  [r"a) $t_{tb}=2{,}50\ \text{s}$", r"b) $\Delta t\approx0{,}2\ \text{s}$", r"c) $\delta_t\approx7\%$", r"d) $t=2{,}5\ \text{s}\pm0{,}2\ \text{s}$", r"e) $v=0{,}48\ \text{m/s}\pm0{,}04\ \text{m/s}$"],
  r"Nhận dạng: <strong>bảng nhiều lần đo kèm ĐCNN</strong> → trung bình, độ lệch tuyệt đối, cộng <strong>nửa ĐCNN</strong>, ghi $A\pm\Delta A$ cùng hàng thập phân."),
 sol(R6, [
  ("Tóm tắt và khối lượng nước", [P(r"Tóm tắt: $U=220\ \text{V}$ ; $P=1800\ \text{W}$ ; $t_1=20\ ^\circ\text{C}$ ; $t_2=100\ ^\circ\text{C}$ ; $H=0{,}84$ ; $c=4200\ \text{J/(kg·K)}$."),
     P(r"$V=1{,}8\ \text{lít}=1{,}8\cdot10^{-3}\ \text{m}^3$ ; $D=1000\ \text{kg/m}^3$:"), M(r"m=D\,V=1000\cdot1{,}8\cdot10^{-3}"), A(r"m=1{,}8\ \text{kg}"),
     P("Cần tìm : $t$ ; tiền điện 30 ngày ; $t'$ khi dùng $110\\ \\text{V}$.")]),
  ("Nhiệt lượng có ích", [M(r"\Delta t=t_2-t_1=100-20=80\ \text{K}"), M(r"Q_{ich}=m\,c\,\Delta t=1{,}8\cdot4200\cdot80"), A(r"Q_{ich}=604800\ \text{J}=604{,}8\ \text{kJ}")]),
  ("Điện năng một lần đun", [P("Từ hiệu suất:"), M(r"H=\dfrac{Q_{ich}}{A}\ \Rightarrow\ A=\dfrac{Q_{ich}}{H}=\dfrac{604800}{0{,}84}"), A(r"A=720000\ \text{J}=720\ \text{kJ}")]),
  ("Thời gian đun", [P(r"Ấm dùng đúng $220\ \text{V}$ nên $P=1800\ \text{W}$:"), M(r"t=\dfrac{A}{P}=\dfrac{720000}{1800}"), A(r"t=400\ \text{s}\approx6\ \text{phút}\ 40\ \text{giây}")]),
  ("Tiền điện 30 ngày", [M(r"A=\dfrac{720000}{3{,}6\cdot10^6}=0{,}2\ \text{kWh}"), P("Số lần đun trong 30 ngày: $2\\cdot30=60$ lần."),
     M(r"A_{30}=60\cdot0{,}2=12\ \text{kWh}"), M(r"\text{Tiền}=12\cdot2000"), A(r"\text{Tiền}=24000\ \text{đồng}")]),
  ("Cắm nhầm vào 110 V", [P(r"Điện trở $R$ không đổi nên $P=\dfrac{U^2}{R}$ tỉ lệ với $U^2$:"), M(r"\dfrac{P'}{P}=\left(\dfrac{U'}{U}\right)^2=\left(\dfrac{110}{220}\right)^2=\dfrac14"),
     P(r"Hiệu suất không đổi nên điện năng cần dùng vẫn là $A$ ; $t=\dfrac{A}{P}$:"), M(r"t'=\dfrac{A}{P'}=4t=4\cdot400"), A(r"t'=1600\ \text{s}\approx26\ \text{phút}\ 40\ \text{giây}")]),
  ("Kiểm tra", [P(r"Dòng điện định mức $I=\dfrac{P}{U}=\dfrac{1800}{220}\approx8{,}2\ \text{A}$ : hợp lí với ấm điện."),
     P(r"Đun $1{,}8$ lít nước trong khoảng $6{,}7$ phút bằng ấm $1800\ \text{W}$ : hợp lí."),
     P(r"Thử ngược: $0{,}84\cdot1800\cdot400=604800\ \text{J}=Q_{ich}$ ✓."),
     P("Kết luận bằng một câu có đơn vị, mỗi bước một dòng, giữ ký hiệu chữ đến bước cuối.")])],
  [r"a) Thời gian đun $t=400\ \text{s}\approx6\ \text{phút}\ 40\ \text{giây}$", r"b) Tiền điện 30 ngày khoảng $24000\ \text{đồng}$", r"c) Ở $110\ \text{V}$: $t'=1600\ \text{s}\approx26\ \text{phút}\ 40\ \text{giây}$"],
  r"Nhận dạng: đề có <strong>hiệu suất, lít, kWh</strong> cùng lúc → tóm tắt đổi về SI, giữ ký hiệu chữ, <strong>kiểm tra đơn vị</strong> ở cuối ; đổi hiệu điện thế → <strong>rút tỉ số $P\sim U^2$</strong>."),
]


# ═════════════ TỰ GIẢI TỪNG BƯỚC ═════════════
STEPS = [
 # ── Dạng 1 ──
 dict(nhan_dang=r"Thấy <b>hai trạng thái, cùng điện trở</b> → <b>chia vế theo vế</b> ; có <b>biến trở nối tiếp</b> → dùng <b>R₀ + R</b>.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Lập tỉ số cho dây dẫn", r"Cường độ dòng điện $I_2$ khi $U_2=6{,}0\ \text{V}$?", 0.24, "A", 0.005,
       loi=r"Lập ngược $\dfrac{I_2}{I_1}=\dfrac{U_1}{U_2}$ nên dòng điện giảm dù hiệu điện thế tăng ; $I$ tỉ lệ thuận với $U$."),
  buoc("Hiệu điện thế của nguồn", r"Hiệu điện thế $U$ của nguồn (V)?", 12, "V", 0.2,
       loi=r"Lấy $U=I\,R_1$ — quên điện trở $R_0$ nối tiếp ; nguồn cấp điện cho cả hai điện trở.",
       ke=[(r"$U=I\,(R_0+R_1)$ vì hai điện trở mắc nối tiếp", True),
           (r"$U=I\,R_1$ vì chỉ biến trở thay đổi", r"Nguồn cấp điện cho cả $R_0$ và biến trở ; điện trở toàn mạch là $R_0+R_1$."),
           (r"$U=I\,R_0$", r"Dòng điện còn chạy qua biến trở ; hiệu điện thế nguồn là tổng hai phần.")]),
  buoc("Dòng điện khi tăng biến trở", r"Dòng điện $I_2$ trong mạch khi biến trở là $R_2$?", 0.2, "A", 0.005,
       loi=r"Viết $\dfrac{I_2}{I_1}=\dfrac{R_1}{R_2}$ — sai vì $I$ tỉ lệ nghịch với tổng $R_0+R$, không phải với riêng biến trở.",
       ke=[(r"$I_2=\dfrac{U}{R_0+R_2}$ với $U$ vừa tìm", True),
           (r"$I_2=I_1\dfrac{R_1}{R_2}$", r"Chỉ đúng khi $R_1$, $R_2$ là toàn bộ điện trở mạch ; ở đây còn $R_0$ không đổi nối tiếp."),
           (r"$I_2=I_1\dfrac{R_2}{R_1}$", r"Điện trở tăng thì dòng điện giảm, không tăng.")]),
  buoc("Công suất khi dòng điện tăng", r"Công suất mới $P_2$ của điện trở khi dòng điện là $0{,}30\ \text{A}$ (W)?", 1.8, "W", 0.05,
       loi=r"Coi $P$ tỉ lệ thuận với $I$ (tăng 1,5 lần) nên quên bình phương.",
       ke=[(r"$\dfrac{P_2}{P_1}=\left(\dfrac{I_2}{I_1}\right)^2$", True),
           (r"$\dfrac{P_2}{P_1}=\dfrac{I_2}{I_1}$", r"$P=I^2R$ chứa $I^2$ nên tỉ số phải bình phương."),
           (r"$\dfrac{P_2}{P_1}=\dfrac{I_1}{I_2}$", r"Dòng điện tăng thì công suất tăng, không giảm.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 2 ──
 dict(nhan_dang=r"Thấy <b>kWh, km/h, phút</b> trong đề → đổi về <b>SI</b> trước ; gặp <b>công thức lạ</b> → kiểm tra <b>đơn vị hai vế</b>.",
  cap_do=1, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 3}, buoc=[
  buoc("Thứ nguyên của $P=U^2/R$", r"Vế phải của $P=\dfrac{U^2}{R}$ có đơn vị nào?",
       loi=r"Rút gọn dở dang ($\text{V}/\Omega=\text{A}$) rồi dừng, bỏ sót thừa số $\text{V}$ còn lại.",
       lua_chon=[(r"Oát (W), vì $\dfrac{\text{V}^2}{\Omega}=\text{V}\cdot\dfrac{\text{V}}{\Omega}=\text{V}\cdot\text{A}$", True),
                 (r"Jun (J), vì vế phải là năng lượng", r"$\text{J}=\text{W}\cdot\text{s}$ ; vế phải không có thừa số thời gian nên là công suất, không phải năng lượng."),
                 (r"Ampe (A), vì $\text{V}/\Omega=\text{A}$", r"Mới rút gọn một lần $\text{V}/\Omega=\text{A}$ ; còn thừa một $\text{V}$ nên được $\text{V}\cdot\text{A}=\text{W}$.")]),
  buoc("Tốc độ đi bộ", r"Tốc độ của người đi bộ theo m/s?", 1.5, "m/s", 0.02,
       loi=r"Quên đổi phút ra giây (chia thẳng $3600$ cho $40$) hoặc đổi km sai (ra $3{,}6\ \text{m}$).",
       ke=[(r"Đổi $3{,}6\ \text{km}=3600\ \text{m}$ và $40\ \text{phút}=2400\ \text{s}$ rồi $v=\dfrac{s}{t}$", True),
           (r"$v=\dfrac{3{,}6}{40}$ rồi chia $3{,}6$ để ra m/s", r"Đó là km/phút ; chia $3{,}6$ chỉ dùng đổi km/h sang m/s. Km/phút sang m/s phải nhân $\dfrac{1000}{60}$."),
           (r"$v=\dfrac{3600}{40}$", r"Mẫu số phải là $40\ \text{phút}$ đổi ra giây ($2400\ \text{s}$), không dùng số phút.")]),
  buoc("Điện năng theo kWh", r"Điện năng lò sưởi tiêu thụ (kWh)?", 6, "kWh", 0.05,
       loi=r"Ghi $2000\cdot3=6000$ nhưng quên đổi Wh ra kWh, hoặc đổi $3$ giờ ra giây rồi nhân với kW.",
       ke=[(r"$A=P\,t$ với $P$ theo kW và $t$ theo giờ", True),
           (r"$A=\dfrac{P}{t}$", r"Công suất chia thời gian ra đơn vị khác ; điện năng là tích $P\,t$."),
           (r"$A=2000\cdot3=6000\ \text{kWh}$", r"$2000\ \text{W}\cdot3\ \text{h}$ cho $6000\ \text{Wh}$, tức $6\ \text{kWh}$ ; thiếu bước đổi Wh ra kWh nên sai $1000$ lần.")]),
  buoc("Đổi ra jun", r"Điện năng đó bằng bao nhiêu MJ?", 21.6, "MJ", 0.1,
       loi=r"Nhân với $3600$ thay vì $3{,}6\cdot10^6$ (quên $1\ \text{kWh}=1000\ \text{W}\cdot3600\ \text{s}$).",
       ke=[(r"$1\ \text{kWh}=3{,}6\cdot10^6\ \text{J}$ nên nhân $A$ với số này", True),
           (r"$1\ \text{kWh}=3600\ \text{J}$", r"$3600$ chỉ là số giây trong một giờ ; còn phải nhân $1000$ vì kW = 1000 W."),
           (r"$1\ \text{kWh}=1000\ \text{J}$", r"Tiền tố k chỉ nhân $1000$ cho oát ; còn phải nhân $3600$ giây của một giờ.")]),
  buoc("Cường độ dòng điện", r"Cường độ dòng điện qua lò sưởi (A)?", 9.09, "A", 0.05,
       loi=r"Dùng $I=\dfrac{U}{P}$ hoặc thế $P=2$ (kW) vào công thức mà không đổi ra W.",
       ke=[(r"$I=\dfrac{P}{U}$ với $P=2000\ \text{W}$", True),
           (r"$I=\dfrac{U}{P}$", r"Ngược rồi : $P=UI$ nên $I=\dfrac{P}{U}$."),
           (r"$I=\dfrac{P}{U}$ với $P=2$ (kW)", r"Phải đổi $2\ \text{kW}=2000\ \text{W}$ trước ; dùng $2$ sẽ ra giá trị bé hơn $1000$ lần.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 3 ──
 dict(nhan_dang=r"Thấy <b>đồ thị U–I thẳng qua gốc</b> → hệ số góc là <b>R</b> ; đổi sang <b>I–U</b> thì là <b>1/R</b>.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 4}, buoc=[
  buoc("Điện trở dây A", r"Điện trở dây A (Ω)?", 12, "Ω", 0.2,
       loi=r"Chia ngược $\dfrac{I}{U}$ (ra $\dfrac{1}{R}$) hoặc chia hai toạ độ của hai điểm khác nhau."),
  buoc("Điện trở dây B", r"Điện trở dây B (Ω)?", 30, "Ω", 0.5,
       loi=r"Thấy trục hoành là $I$ nên viết $R=\dfrac{I}{U}$ ; điện trở luôn là $\dfrac{U}{I}$.",
       ke=[(r"Lấy một điểm trên đường thẳng : $R=\dfrac{U}{I}=\dfrac{\Delta U}{\Delta I}$", True),
           (r"$R=\dfrac{I}{U}$ vì trục hoành là $I$", r"$R=\dfrac{U}{I}$ không phụ thuộc cách đặt trục ; $\dfrac{I}{U}$ là $\dfrac{1}{R}$ (đơn vị A/V)."),
           (r"$R=U\cdot I$", r"$U\cdot I$ là công suất (đơn vị W), không phải điện trở.")]),
  buoc("So sánh độ dốc", r"Trên đồ thị $U$–$I$ cùng hệ trục, đường của dây nào dốc hơn và vì sao?",
       loi=r"Cho rằng đường nào dài hơn (kết thúc ở $I$ lớn hơn) thì dốc hơn ; độ dốc là hệ số góc $\dfrac{\Delta U}{\Delta I}$.",
       lua_chon=[(r"Dây B dốc hơn, vì cùng $I$ thì $U$ lớn hơn, tức hệ số góc $R$ lớn hơn", True),
                 (r"Dây A dốc hơn vì đường của nó dài hơn", r"Độ dốc là hệ số góc $\dfrac{\Delta U}{\Delta I}$, không phụ thuộc đường vẽ dài hay ngắn."),
                 (r"Hai dây dốc như nhau vì đều là đường thẳng qua gốc", r"Đều tỉ lệ thuận nhưng hệ số góc (điện trở) khác nhau nên độ dốc khác nhau.")],
       ke=[(r"So hệ số góc : lớn hơn nghĩa là điện trở lớn hơn", True),
           (r"Đường nào vẽ dài hơn thì dốc hơn", r"Độ dài đoạn vẽ chỉ do khoảng đo, không quyết định độ dốc ; độ dốc là tỉ số $\dfrac{\Delta U}{\Delta I}$."),
           (r"Đường nào kết thúc ở $I$ lớn hơn thì dốc hơn", r"Điểm cuối của dây A có $I$ lớn hơn nhưng $U$ lại nhỏ hơn ; độ dốc là tỉ số $\dfrac{\Delta U}{\Delta I}$.")]),
  buoc("Nội suy cường độ dòng điện", r"Dây A: cường độ dòng điện khi $U=2{,}7\ \text{V}$ (nội suy)?", 0.225, "A", 0.003,
       loi=r"Lấy trung bình hai dòng điện của hai điểm kề, chỉ đúng khi $U$ nằm chính giữa hai điểm đó.",
       ke=[(r"$I=\dfrac{U}{R_A}$ hoặc nội suy tuyến tính giữa $(0{,}20;\ 2{,}4)$ và $(0{,}30;\ 3{,}6)$", True),
           (r"$I=R_A\cdot U$", r"Nhân điện trở với hiệu điện thế ra đơn vị $\Omega\cdot\text{V}$, không phải ampe ; $I=\dfrac{U}{R}$."),
           (r"Lấy trung bình hai dòng điện $0{,}20\ \text{A}$ và $0{,}30\ \text{A}$", r"Chỉ đúng khi $U$ nằm chính giữa hai điểm ; $2{,}7\ \text{V}$ gần $2{,}4\ \text{V}$ hơn $3{,}6\ \text{V}$ nên $I$ gần $0{,}20\ \text{A}$ hơn.")]),
  buoc("Hệ số góc của đồ thị I–U", r"Đồ thị $I$–$U$ của dây A có hệ số góc bằng bao nhiêu (A/V)?", 0.0833, "A/V", 0.002,
       loi=r"Cho rằng đổi trục thì hệ số góc vẫn là $R_A$ ; thực ra thành nghịch đảo $\dfrac{1}{R}$.",
       ke=[(r"$k=\dfrac{\Delta I}{\Delta U}=\dfrac{1}{R_A}$", True),
           (r"Vẫn bằng $R_A$ vì cùng một dây", r"Đổi trục thì hệ số góc thành nghịch đảo : $\dfrac{1}{R}$ (đơn vị A/V)."),
           (r"Bằng $-R_A$", r"Đường vẫn đi lên ($U$ tăng thì $I$ tăng) nên hệ số góc dương.")]),
  buoc("Ngoại suy hiệu điện thế", r"Dây B: hiệu điện thế khi $I=0{,}25\ \text{A}$ (giá trị dự đoán, ngoại suy)?", 7.5, "V", 0.1,
       loi=r"Viết $U=\dfrac{I}{R}$ (ngược) hoặc từ chối tính vì $0{,}25\ \text{A}$ ngoài các điểm đo.",
       ke=[(r"$U=I\,R_B$ vì đường thẳng qua gốc, ghi rõ là giá trị dự đoán", True),
           (r"Không tính được vì $0{,}25\ \text{A}$ nằm ngoài các điểm đo", r"Đường thẳng qua gốc, vượt ngắn nên ngoại suy được, miễn ghi rõ là dự đoán."),
           (r"$U=\dfrac{I}{R_B}$", r"Ngược rồi : $U=I\,R$.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 4 ──
 dict(nhan_dang=r"Thấy <b>đồ thị v–t bậc thang</b> → <b>diện tích</b> là quãng đường ; <b>tốc độ trung bình</b> = <b>tổng s / tổng t</b>.",
  cap_do=2, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Tổng quãng đường", r"Tổng quãng đường xe đi được?", 270, "m", 1,
       loi=r"Lấy trung bình cộng bốn vận tốc nhân với tổng thời gian ; hoặc lấy mốc cuối của giai đoạn làm độ dài giai đoạn (ví dụ $6\cdot35$)."),
  buoc("Tốc độ trung bình", r"Tốc độ trung bình trên toàn hành trình (m/s)?", 4.15, "m/s", 0.02,
       loi=r"Lấy trung bình cộng bốn vận tốc ($3{,}75\ \text{m/s}$) hoặc chia cho thời gian chuyển động, bỏ lúc dừng.",
       ke=[(r"$v_{tb}=\dfrac{s_{\text{tổng}}}{t_{\text{tổng}}}$ với $t_{\text{tổng}}$ gồm cả lúc dừng", True),
           (r"$v_{tb}=\dfrac{4+6+0+5}{4}$", r"Các giai đoạn dài ngắn khác nhau nên không được lấy trung bình cộng các vận tốc."),
           (r"$v_{tb}=\dfrac{s_{\text{tổng}}}{t_{\text{chạy}}}$ (bỏ lúc dừng)", r"Tốc độ trung bình tính trên toàn bộ thời gian, kể cả lúc dừng.")]),
  buoc("Vị trí lúc $t=50$ s", r"Lúc $t=50\ \text{s}$ xe cách điểm xuất phát bao nhiêu mét?", 195, "m", 1,
       loi=r"Lấy $5\cdot50$ vì lúc đó $v=5\ \text{m/s}$ ; vận tốc này chỉ có từ giây 45 trở đi.",
       ke=[(r"Cộng diện tích đến $t=45\ \text{s}$ rồi thêm $5\cdot(50-45)$", True),
           (r"$s(50)=5\cdot50$ vì lúc này $v=5\ \text{m/s}$", r"Vận tốc $5\ \text{m/s}$ chỉ có từ giây 45 ; phải cộng cả quãng đường của các giai đoạn trước."),
           (r"$s(50)=s_{\text{tổng}}\cdot\dfrac{50}{65}$", r"Xe không chạy đều nên quãng đường không tỉ lệ với thời gian.")]),
  buoc("Thời điểm đi được 150 m", r"Xe đi được $150\ \text{m}$ đầu tiên vào thời điểm nào (s)?", 31.7, "s", 0.1,
       loi=r"Chia $150$ cho một vận tốc duy nhất (coi xe chạy đều cả quãng).",
       ke=[(r"Giai đoạn 1 đi $80\ \text{m}$, còn $70\ \text{m}$ đi với $6\ \text{m/s}$ rồi cộng $20\ \text{s}$", True),
           (r"$t=\dfrac{150}{4}$ (vận tốc giai đoạn đầu)", r"Xe chỉ chạy $4\ \text{m/s}$ trong $20\ \text{s}$ đầu ($80\ \text{m}$) ; sau đó chạy nhanh hơn."),
           (r"$t=\dfrac{150}{4{,}15}$ (dùng tốc độ trung bình)", r"Tốc độ trung bình của cả hành trình không áp dụng cho từng đoạn.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 5 ──
 dict(nhan_dang=r"Thấy <b>bảng nhiều lần đo kèm ĐCNN</b> → trung bình, độ lệch tuyệt đối, <b>nửa ĐCNN</b>, ghi <b>A ± ΔA</b>.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Giá trị trung bình", r"Giá trị trung bình $t_{tb}$ của năm lần đo (s)?", 2.5, "s", 0.01,
       loi=r"Chia tổng cho $4$ thay vì $5$ ; hoặc bỏ sót một lần đo khi cộng."),
  buoc("Sai số ngẫu nhiên", r"Sai số ngẫu nhiên trung bình $\Delta t_{ng}$ (s)?", 0.12, "s", 0.005,
       loi=r"Cộng đại số các độ lệch nên dương và âm triệt tiêu, ra gần $0$ một cách vô lí.",
       ke=[(r"Lấy trị tuyệt đối từng độ lệch $|t_i-t_{tb}|$ rồi lấy trung bình", True),
           (r"Cộng đại số các độ lệch $t_i-t_{tb}$ rồi chia cho $5$", r"Độ lệch dương và âm triệt tiêu nhau nên ra gần $0$ một cách vô lí."),
           (r"Bình phương các độ lệch rồi cộng lại", r"Cách tính ở đây lấy trung bình độ lệch tuyệt đối, không bình phương.")]),
  buoc("Sai số tuyệt đối", r"Sai số tuyệt đối $\Delta t$, làm tròn một chữ số có nghĩa (s)?", 0.2, "s", 0.01,
       loi=r"Bỏ sai số dụng cụ, hoặc cộng cả ĐCNN thay vì một nửa ĐCNN.",
       ke=[(r"$\Delta t=\Delta t_{ng}+\Delta t_{dc}$ với $\Delta t_{dc}=\dfrac{\text{ĐCNN}}{2}$ rồi làm tròn", True),
           (r"$\Delta t=\Delta t_{ng}$ (bỏ sai số dụng cụ)", r"Sai số dụng cụ luôn có mặt, bằng nửa ĐCNN ; phải cộng vào. Bỏ đi thì ra $0{,}12\ \text{s}$, làm tròn thành $0{,}1\ \text{s}$, khác kết quả đúng."),
           (r"$\Delta t=\Delta t_{ng}+\text{ĐCNN}$", r"Sai số dụng cụ lấy bằng nửa độ chia nhỏ nhất, không phải cả độ chia : được $0{,}22\ \text{s}$ thay vì $0{,}17\ \text{s}$ ; hai số cùng làm tròn thành $0{,}2\ \text{s}$ chỉ là trùng hợp, phương pháp vẫn sai.")]),
  buoc("Sai số tương đối", r"Sai số tương đối $\delta_t$ (%), dùng $\Delta t$ chưa làm tròn ($0{,}17\ \text{s}$)?", 7, "%", 0.5,
       loi=r"Quên đổi ra phần trăm (ghi $0{,}08\%$) hoặc chia ngược $\dfrac{t_{tb}}{\Delta t}$.",
       ke=[(r"$\delta_t=\dfrac{\Delta t}{t_{tb}}\cdot100\%$", True),
           (r"$\delta_t=\dfrac{t_{tb}}{\Delta t}\cdot100\%$", r"Ngược tử và mẫu : sai số tương đối là sai số chia cho giá trị đo."),
           (r"$\delta_t=\Delta t\cdot100\%$", r"Phải chia cho $t_{tb}$ ; sai số tương đối không có đơn vị.")]),
  buoc("Sai số của tốc độ", r"Sai số tuyệt đối $\Delta v$ của $v=\dfrac{s}{t}$ (m/s)?", 0.04, "m/s", 0.005,
       loi=r"Chia hai sai số tuyệt đối cho nhau, hoặc trừ hai sai số tương đối thay vì cộng.",
       ke=[(r"Cộng sai số tương đối : $\delta_v=\delta_s+\delta_t$ rồi $\Delta v=v\,\delta_v$", True),
           (r"$\Delta v=\dfrac{\Delta s}{\Delta t}$", r"Không chia hai sai số tuyệt đối cho nhau ; phép chia cộng các sai số tương đối."),
           (r"$\delta_v=\delta_s-\delta_t$", r"Phép chia vẫn cộng các sai số tương đối ; sai số không bù trừ cho nhau.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 6 ──
 dict(nhan_dang=r"Thấy <b>hiệu suất, lít, kWh</b> cùng lúc → tóm tắt đổi về <b>SI</b>, giữ ký hiệu chữ, <b>kiểm tra đơn vị</b> cuối bài.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Tóm tắt và khối lượng nước", r"Khối lượng nước cần đun (kg)?", 1.8, "kg", 0.02,
       loi=r"Nhầm $1$ lít ra $1$ gam hoặc ra $1$ tấn ; $1$ lít nước nặng $1$ kg."),
  buoc("Nhiệt lượng có ích", r"Nhiệt lượng có ích làm nóng nước (kJ)?", 604.8, "kJ", 0.5,
       loi=r"Dùng nhiệt độ cuối thay cho độ tăng nhiệt độ $\Delta t$.",
       ke=[(r"$Q_{ich}=m\,c\,\Delta t$ với $\Delta t=t_2-t_1$", True),
           (r"$Q_{ich}=m\,c\,t_2$ với $t_2$ là nhiệt độ cuối", r"Nhiệt lượng phụ thuộc độ tăng nhiệt độ $\Delta t=t_2-t_1$, không phải nhiệt độ cuối."),
           (r"$Q_{ich}=P\,t$", r"Đó là điện năng ấm tiêu thụ ; chưa biết $t$, và còn có hao phí.")]),
  buoc("Điện năng một lần đun", r"Điện năng ấm tiêu thụ cho một lần đun (kJ)?", 720, "kJ", 1,
       loi=r"Nhân $Q_{ich}$ với $H$ thay vì chia ; điện năng toàn phần phải lớn hơn nhiệt có ích.",
       ke=[(r"$A=\dfrac{Q_{ich}}{H}$ vì $H=\dfrac{Q_{ich}}{A}$", True),
           (r"$A=Q_{ich}\cdot H$", r"Hiệu suất nhỏ hơn $1$ nên phép nhân ra điện năng nhỏ hơn nhiệt có ích — vô lí."),
           (r"$A=Q_{ich}$ vì ấm toả hết nhiệt vào nước", r"Hiệu suất nhỏ hơn $100\%$ nghĩa là một phần nhiệt toả ra ấm và môi trường ; điện năng lớn hơn nhiệt có ích.")]),
  buoc("Thời gian đun", r"Thời gian đun một lần (s)?", 400, "s", 1,
       loi=r"Chia kJ cho W mà không đổi ra J (sai $1000$ lần).",
       ke=[(r"$t=\dfrac{A}{P}$ với $A$ đổi ra J, $P$ theo W", True),
           (r"$t=\dfrac{A}{P}$ lấy $A$ theo kJ", r"$A$ theo kJ phải đổi ra J (nhân $1000$) rồi chia cho oát, nếu không sai $1000$ lần."),
           (r"$t=P\cdot A$", r"Nhân sẽ ra đơn vị $\text{W}\cdot\text{J}$ ; $A=P\,t$ nên $t=\dfrac{A}{P}$.")]),
  buoc("Tiền điện 30 ngày", r"Tiền điện của ấm trong $30$ ngày (nghìn đồng)?", 24, "nghìn đồng", 0.1,
       loi=r"Nhân kJ với giá điện (giá tính theo kWh) hoặc chỉ tính một lần đun mỗi ngày.",
       ke=[(r"Đổi mỗi lần ra kWh, nhân $2\cdot30$ lần rồi nhân giá", True),
           (r"Nhân $A=720\ \text{kJ}$ với giá $2000$ đồng", r"Giá tính theo kWh ; phải đổi kJ ra kWh (chia $3600$) rồi mới nhân."),
           (r"Chỉ tính một lần đun mỗi ngày", r"Đề cho đun hai lần mỗi ngày : số lần là $2\cdot30$.")]),
  buoc("Cắm nhầm vào 110 V", r"Thời gian đun mỗi lần khi cắm vào $110\ \text{V}$ (s)?", 1600, "s", 5,
       loi=r"Cho rằng $U$ giảm một nửa thì $P$ giảm một nửa ; $P=\dfrac{U^2}{R}$ giảm $4$ lần.",
       ke=[(r"$P'=\dfrac{P}{4}$ vì $P\sim U^2$ ; cùng điện năng nên $t'=4t$", True),
           (r"$P'=\dfrac{P}{2}$ nên $t'=2t$", r"$P=\dfrac{U^2}{R}$ tỉ lệ với bình phương $U$ ; $U$ giảm một nửa thì $P$ giảm $4$ lần."),
           (r"Thời gian không đổi vì điện năng cần dùng không đổi", r"Điện năng không đổi nhưng công suất nhỏ hơn nên thời gian dài hơn : $t=\dfrac{A}{P}$.")]),
  buoc("Kiểm tra")]),
]


# ═════════════ BÀI TỰ LUẬN (ví dụ D, luyện E, nâng cao G của nguồn) ═════════════
def L(*lines):
    return "".join(f"<p>{x}</p>" for x in lines)

def table(head, rows):
    h = "".join(f"<th>{x}</th>" for x in head)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="table-scroll"><table class="tl-table"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'

TL = [
 ("Dễ", L(r"Một dây dẫn có điện trở không đổi. Khi đặt hiệu điện thế $6\ \text{V}$ thì cường độ dòng điện là $0{,}25\ \text{A}$.", r"a) Tính điện trở của dây.", r"b) Tính cường độ dòng điện khi hiệu điện thế là $9\ \text{V}$.", r"c) Nêu đại lượng nào tỉ lệ thuận với đại lượng nào trong câu b."),
        L(r"a) $R=\dfrac{U}{I}=\dfrac{6}{0{,}25}=24\ \Omega$.", r"b) $\dfrac{I'}{I}=\dfrac{U'}{U}\Rightarrow I'=0{,}25\cdot\dfrac{9}{6}=0{,}375\ \text{A}$.", r"c) $R$ không đổi nên $I$ tỉ lệ thuận với $U$ : hiệu điện thế tăng $1{,}5$ lần thì dòng điện cũng tăng $1{,}5$ lần.")),
 ("Dễ", L(r"Đổi các đơn vị sau.", r"a) $36\ \text{km/h}$ ra m/s.", r"b) $1{,}2\ \text{kWh}$ ra J.", r"c) $2500\ \Omega$ ra $\text{k}\Omega$.", r"d) $0{,}45\ \text{A}$ ra mA.", r"e) $2{,}5\cdot10^6\ \text{J}$ ra kWh."),
        L(r"a) $\dfrac{36}{3{,}6}=10\ \text{m/s}$.", r"b) $1{,}2\cdot3{,}6\cdot10^6=4{,}32\cdot10^6\ \text{J}$.", r"c) $\dfrac{2500}{1000}=2{,}5\ \text{k}\Omega$.", r"d) $0{,}45\cdot1000=450\ \text{mA}$.", r"e) $\dfrac{2{,}5\cdot10^6}{3{,}6\cdot10^6}\approx0{,}69\ \text{kWh}$.")),
 ("Dễ", L(r"Một vật chuyển động đều. Đồ thị quãng đường theo thời gian của vật là đường thẳng đi qua gốc toạ độ và qua điểm có toạ độ $(5\ \text{s};\ 20\ \text{m})$.", r"a) Tính vận tốc của vật.", r"b) Tính quãng đường vật đi được sau $12\ \text{s}$.", r"c) Nêu ý nghĩa hệ số góc của đồ thị này."),
        L(r"a) $v=\dfrac{20}{5}=4\ \text{m/s}$.", r"b) $s=v\,t=4\cdot12=48\ \text{m}$.", r"c) Hệ số góc $\dfrac{\Delta s}{\Delta t}$ của đồ thị $s$–$t$ bằng vận tốc của vật, đơn vị m/s.")),
 ("Dễ", L(r"Một quạt điện có công suất $55\ \text{W}$, mỗi ngày chạy $6$ giờ.", r"a) Tính điện năng quạt tiêu thụ trong $30$ ngày, ra kWh.", r"b) Tính tiền điện của quạt trong $30$ ngày, giá $1800$ đồng một kWh."),
        L(r"a) $A=55\cdot6\cdot30=9900\ \text{Wh}=9{,}9\ \text{kWh}$.", r"b) Tiền $=9{,}9\cdot1800=17820\ \text{đồng}$.")),
 ("Dễ", L(r"Kiểm tra đơn vị của hai công thức sau.", r"a) $Q=I^2Rt$.", r"b) $R=\rho\dfrac{l}{S}$, từ đó suy ra đơn vị của điện trở suất $\rho$."),
        L(r"a) Đơn vị vế phải : $\text{A}^2\cdot\Omega\cdot\text{s}$. Vì $\Omega=\dfrac{\text{V}}{\text{A}}$ nên $\text{A}^2\cdot\dfrac{\text{V}}{\text{A}}\cdot\text{s}=\text{A}\cdot\text{V}\cdot\text{s}=\text{J}$, đúng đơn vị của $Q$.", r"b) $\rho=\dfrac{R\,S}{l}$ có đơn vị $\dfrac{\Omega\cdot\text{m}^2}{\text{m}}=\Omega\cdot\text{m}$ (ôm mét).")),
 ("Dễ", L(r"Một gia đình thay bóng đèn sợi đốt $60\ \text{W}$ bằng bóng đèn LED $9\ \text{W}$ có cùng độ sáng, mỗi ngày dùng $5$ giờ.", r"a) Tính điện năng tiết kiệm được trong $30$ ngày, ra kWh.", r"b) Với giá $2000$ đồng một kWh, mỗi tháng tiết kiệm được bao nhiêu tiền?"),
        L(r"a) Công suất tiết kiệm : $60-9=51\ \text{W}$ ; điện năng : $51\cdot5\cdot30=7650\ \text{Wh}=7{,}65\ \text{kWh}$.", r"b) Tiền tiết kiệm : $7{,}65\cdot2000=15300\ \text{đồng}$.")),
]
TL += [
 ("Trung bình", L(r"Hai điện trở $R_1=10\ \Omega$ và $R_2$ mắc nối tiếp vào hiệu điện thế $U=12\ \text{V}$ thì cường độ dòng điện trong mạch là $0{,}4\ \text{A}$.", r"a) Tính điện trở tương đương và $R_2$.", r"b) Tính hiệu điện thế hai đầu mỗi điện trở và kiểm tra tỉ số $\dfrac{U_1}{U_2}$ có bằng $\dfrac{R_1}{R_2}$ không."),
        L(r"a) $R_{td}=\dfrac{U}{I}=\dfrac{12}{0{,}4}=30\ \Omega$ ; $R_2=R_{td}-R_1=30-10=20\ \Omega$.", r"b) Dòng điện qua hai điện trở bằng nhau : $U_1=I\,R_1=0{,}4\cdot10=4\ \text{V}$ ; $U_2=I\,R_2=0{,}4\cdot20=8\ \text{V}$ ; $U_1+U_2=12\ \text{V}$ ✓.", r"$\dfrac{U_1}{U_2}=\dfrac{4}{8}=\dfrac{1}{2}$ và $\dfrac{R_1}{R_2}=\dfrac{10}{20}=\dfrac{1}{2}$ : bằng nhau, đúng với hệ thức $\dfrac{U_1}{U_2}=\dfrac{R_1}{R_2}$ của mạch nối tiếp.")),
 ("Trung bình", L(r"Hai điện trở $R_1=15\ \Omega$ và $R_2=30\ \Omega$ mắc song song vào hiệu điện thế $9\ \text{V}$.", r"a) Tính cường độ dòng điện qua mỗi điện trở và dòng điện mạch chính.", r"b) Chứng tỏ $\dfrac{I_1}{I_2}=\dfrac{R_2}{R_1}$."),
        L(r"a) Mắc song song nên $U_1=U_2=9\ \text{V}$ : $I_1=\dfrac{9}{15}=0{,}6\ \text{A}$ ; $I_2=\dfrac{9}{30}=0{,}3\ \text{A}$ ; $I=I_1+I_2=0{,}9\ \text{A}$.", r"b) $U=I_1R_1=I_2R_2$ nên $\dfrac{I_1}{I_2}=\dfrac{R_2}{R_1}$. Số : $\dfrac{0{,}6}{0{,}3}=2=\dfrac{30}{15}$ ✓.")),
 ("Trung bình", L(r"Chứng minh rằng trong đoạn mạch nối tiếp, tỉ số công suất toả nhiệt trên hai điện trở bằng tỉ số hai điện trở : $\dfrac{P_1}{P_2}=\dfrac{R_1}{R_2}$. Áp dụng cho $R_1=6\ \Omega$, $R_2=18\ \Omega$, dòng điện trong mạch là $0{,}5\ \text{A}$ : tính $P_1$, $P_2$ rồi kiểm tra tỉ số."),
        L(r"Trong mạch nối tiếp, hai điện trở có cùng dòng điện $I$ : $P_1=I^2R_1$ và $P_2=I^2R_2$. Chia vế theo vế : $\dfrac{P_1}{P_2}=\dfrac{R_1}{R_2}$.", r"Số : $P_1=0{,}5^2\cdot6=1{,}5\ \text{W}$ ; $P_2=0{,}5^2\cdot18=4{,}5\ \text{W}$ ; $\dfrac{P_1}{P_2}=\dfrac{1}{3}=\dfrac{6}{18}$ ✓.")),
 ("Trung bình", L(r"Cho bảng số liệu của một dây dẫn.", table(["$U$ (V)", "$2$", "$4$", "$6$", "$8$"], [["$I$ (A)", "$0{,}16$", "$0{,}32$", "$0{,}48$", "$0{,}64$"]]), r"a) Vẽ đồ thị $U$–$I$ (trục hoành là $I$, trục tung là $U$).", r"b) Tính điện trở của dây.", r"c) Nội suy cường độ dòng điện khi $U=5\ \text{V}$.", r"d) Ngoại suy hiệu điện thế khi $I=0{,}8\ \text{A}$."),
        L(r"a) Trục hoành $I$ (A), trục tung $U$ (V). Các điểm $(0;0)$, $(0{,}16;2)$, $(0{,}32;4)$, $(0{,}48;6)$, $(0{,}64;8)$ thẳng hàng và đi qua gốc.", r"b) $R=\dfrac{2}{0{,}16}=12{,}5\ \Omega$.", r"c) $I=\dfrac{5}{12{,}5}=0{,}4\ \text{A}$ (nội suy giữa $(0{,}32;4)$ và $(0{,}48;6)$ cũng cho $0{,}4\ \text{A}$).", r"d) $U=I\,R=0{,}8\cdot12{,}5=10\ \text{V}$ (giá trị dự đoán, vượt điểm đo cuối $0{,}64\ \text{A}$).")),
 ("Trung bình", L(r"Đo điện trở bằng cách thay đổi hiệu điện thế :", table(["Lần đo", "$U$ (V)", "$I$ (A)"], [["1", "$3{,}0$", "$0{,}20$"], ["2", "$6{,}0$", "$0{,}40$"], ["3", "$9{,}0$", "$0{,}60$"], ["4", "$12{,}0$", "$0{,}81$"]]), r"Tính điện trở ở mỗi lần đo và giá trị trung bình. Hàng nào có dấu hiệu bất thường? Nhận xét."),
        L(r"$R_1=\dfrac{3{,}0}{0{,}20}=15\ \Omega$ ; $R_2=15\ \Omega$ ; $R_3=15\ \Omega$ ; $R_4=\dfrac{12{,}0}{0{,}81}\approx14{,}8\ \Omega$.", r"Trung bình $\approx\dfrac{15+15+15+14{,}8}{4}\approx14{,}95\ \Omega$, làm tròn $15\ \Omega$.", r"Hàng 4 lệch khoảng $0{,}2\ \Omega$, tương đương sai số đọc $0{,}01\ \text{A}$ : không đáng kể, giữ lại. Nếu lệch trên $1\ \Omega$ thì phải kiểm tra lại phép đọc và có thể loại, kèm lí do.")),
 ("Trung bình", L(r"Dùng thước có ĐCNN $0{,}1\ \text{cm}$ đo chiều dài một vật : $25{,}0$ ; $25{,}2$ ; $24{,}9$ ; $25{,}1$ ; $25{,}3$ (cm). Tính giá trị trung bình, sai số tuyệt đối, sai số tương đối và ghi kết quả đo."),
        L(r"$L_{tb}=\dfrac{125{,}5}{5}=25{,}10\ \text{cm}$.", r"Độ lệch : $0{,}10$ ; $0{,}10$ ; $0{,}20$ ; $0{,}00$ ; $0{,}20$ ; trung bình $\Delta L_{ng}=\dfrac{0{,}60}{5}=0{,}12\ \text{cm}$. Sai số dụng cụ $0{,}05\ \text{cm}$.", r"$\Delta L=0{,}12+0{,}05=0{,}17\ \text{cm}$. Làm tròn một chữ số có nghĩa : $0{,}2\ \text{cm}$ ; $\delta L=\dfrac{0{,}17}{25{,}1}\approx0{,}7\%$.", r"Kết quả : $L=25{,}1\ \text{cm}\pm0{,}2\ \text{cm}$.")),
 ("Trung bình", L(r"Một bếp điện hoạt động hai giai đoạn : $5$ phút đầu công suất $800\ \text{W}$, $10$ phút sau công suất $1200\ \text{W}$. Biết $80\%$ điện năng chuyển thành nhiệt làm nóng nước từ $25\ ^\circ\text{C}$ đến $100\ ^\circ\text{C}$ ; $c=4200\ \text{J/(kg·K)}$.", r"a) Tính điện năng tiêu thụ, ra J và kWh.", r"b) Tính khối lượng nước đun được.", r"c) Giá điện $2000$ đồng một kWh : tính tiền điện cho $15$ phút hoạt động đó."),
        L(r"a) Điện năng là diện tích dưới đồ thị $P$–$t$ : $A_1=800\cdot300=240000\ \text{J}$ ; $A_2=1200\cdot600=720000\ \text{J}$ ; $A=960000\ \text{J}=\dfrac{960000}{3{,}6\cdot10^6}\approx0{,}267\ \text{kWh}$.", r"b) $Q=H\,A=0{,}8\cdot960000=768000\ \text{J}$ ; $m=\dfrac{Q}{c\,\Delta t}=\dfrac{768000}{4200\cdot75}\approx2{,}44\ \text{kg}$.", r"c) Tiền $=0{,}267\cdot2000\approx533\ \text{đồng}$.")),
 ("Trung bình", L(r"Một bàn là ghi $220\ \text{V}-1000\ \text{W}$ được dùng ở hiệu điện thế $220\ \text{V}$ trong $20$ phút.", r"a) Tính điện năng tiêu thụ, ra J và kWh.", r"b) Tính nhiệt lượng bàn là toả ra, biết hiệu suất $100\%$.", r"c) Trình bày theo bốn bước : tóm tắt, đặt ký hiệu, lập luận, kết luận có đơn vị."),
        L(r"Tóm tắt : $U=220\ \text{V}$ ; $P=1000\ \text{W}$ ; $t=20\ \text{phút}=1200\ \text{s}$ ; $H=100\%$. Cần tìm $A$, $Q$.", r"a) $A=P\,t=1000\cdot1200=1{,}2\cdot10^6\ \text{J}=\dfrac{1{,}2\cdot10^6}{3{,}6\cdot10^6}\approx0{,}333\ \text{kWh}$.", r"b) Hiệu suất $100\%$ nên $Q=A=1{,}2\cdot10^6\ \text{J}$.", r"c) Kết luận : bàn là tiêu thụ $1{,}2\cdot10^6\ \text{J}$ ($0{,}333\ \text{kWh}$) và toả ra nhiệt lượng bằng đúng điện năng đó.")),
 ("Khó", L(r"Trong bài thực hành đo tiêu cự thấu kính hội tụ, ảnh hiện rõ nét trên màn và bằng vật khi $d=d'=2f$, suy ra $f=\dfrac{d}{2}$. Đo $d$ bằng thước ĐCNN $0{,}1\ \text{cm}$ : $20{,}0$ ; $20{,}2$ ; $19{,}8$ ; $20{,}1$ ; $20{,}4$ (cm).", r"a) Tính giá trị trung bình của $d$.", r"b) Tính sai số tuyệt đối và sai số tương đối của $d$.", r"c) Tính $f$ và sai số của $f$ ; ghi kết quả.", r"d) Nêu một nguyên nhân gây sai số hệ thống và một nguyên nhân gây sai số ngẫu nhiên."),
        L(r"a) $d_{tb}=\dfrac{100{,}5}{5}=20{,}10\ \text{cm}$.", r"b) Độ lệch : $0{,}10$ ; $0{,}10$ ; $0{,}30$ ; $0{,}00$ ; $0{,}30$ ; $\Delta d_{ng}=\dfrac{0{,}80}{5}=0{,}16\ \text{cm}$ ; $\Delta d_{dc}=0{,}05\ \text{cm}$ ; $\Delta d=0{,}21\ \text{cm}\approx0{,}2\ \text{cm}$ ; $\delta d=\dfrac{0{,}21}{20{,}10}\approx1{,}0\%$.", r"c) $f=\dfrac{d_{tb}}{2}=10{,}05\ \text{cm}$. Hệ số $\dfrac12$ là số đúng nên $\delta f=\delta d\approx1{,}0\%$ ; $\Delta f=f\,\delta f\approx0{,}105\ \text{cm}\approx0{,}1\ \text{cm}$. Kết quả : $f=10{,}1\ \text{cm}\pm0{,}1\ \text{cm}$.", r"d) Sai số hệ thống : thước lệch vạch $0$, hoặc luôn đánh giá độ nét lệch về một phía, hoặc giá đỡ thấu kính không vuông góc với băng quang học. Sai số ngẫu nhiên : mỗi lần mắt ước lượng độ nét và đọc vị trí hơi khác nhau.")),
 ("Khó", L(r"Điện trở $R_0=3\ \Omega$ mắc nối tiếp với một biến trở $R$, hai đầu mạch nối vào nguồn $U=12\ \text{V}$ không đổi.", r"a) Lập bảng công suất $P_R$ trên biến trở khi $R=1;\ 2;\ 3;\ 4;\ 6;\ 9\ \Omega$.", r"b) Nhận xét dạng đồ thị $P_R$ theo $R$.", r"c) Chứng minh $P_R$ lớn nhất khi $R=R_0$ và tính giá trị đó.", r"d) Tìm hai giá trị của $R$ cho cùng $P_R=9\ \text{W}$."),
        L(r"a) $I=\dfrac{U}{R_0+R}$ ; $P_R=I^2R=\dfrac{144\,R}{(R+3)^2}$.", table(["$R$ ($\\Omega$)", "$1$", "$2$", "$3$", "$4$", "$6$", "$9$"], [["$I$ (A)", "$3$", "$2{,}4$", "$2$", "$1{,}714$", "$1{,}333$", "$1$"], ["$P_R$ (W)", "$9$", "$11{,}52$", "$12$", "$11{,}76$", "$10{,}67$", "$9$"]]),
          r"b) Đồ thị là đường cong : tăng từ $9\ \text{W}$ đến cực đại $12\ \text{W}$ tại $R=3\ \Omega$ rồi giảm. $P_R$ không tỉ lệ thuận cũng không tỉ lệ nghịch đơn thuần với $R$ vì mẫu số chứa $(R+R_0)^2$.",
          r"c) $(R+R_0)^2-4RR_0=(R-R_0)^2\ge0$ nên $(R+R_0)^2\ge4RR_0$. Do đó $P_R=\dfrac{U^2R}{(R+R_0)^2}\le\dfrac{U^2}{4R_0}$, dấu bằng khi $R=R_0$. $P_{max}=\dfrac{144}{4\cdot3}=12\ \text{W}$.",
          r"d) $\dfrac{144R}{(R+3)^2}=9\Rightarrow16R=R^2+6R+9\Rightarrow R^2-10R+9=0\Rightarrow(R-1)(R-9)=0$. Vậy $R=1\ \Omega$ hoặc $R=9\ \Omega$ : một giá trị nhỏ hơn và một giá trị lớn hơn $R_0$.")),
 ("Nâng cao", L(r"Khảo sát một bóng đèn dây tóc :", table(["$U$ (V)", "$2{,}0$", "$3{,}0$", "$4{,}2$", "$5{,}6$"], [["$I$ (A)", "$0{,}40$", "$0{,}50$", "$0{,}60$", "$0{,}70$"]]),
          r"a) Tính điện trở của đèn ở mỗi hàng và nhận xét.", r"b) Đèn có tuân theo định luật Ôm không? Giải thích.", r"c) Nội suy cường độ dòng điện khi $U=3{,}5\ \text{V}$ và tính điện trở tại điểm đó.",
          r"d) Mắc đèn nối tiếp với $R_0=4\ \Omega$ vào nguồn $8\ \text{V}$ không đổi. Dùng số liệu trên, tìm dòng điện trong mạch, hiệu điện thế hai đầu đèn, công suất của đèn và của $R_0$."),
        L(r"a) $R=\dfrac{U}{I}$ : $5{,}0$ ; $6{,}0$ ; $7{,}0$ ; $8{,}0\ \Omega$. Điện trở tăng khi hiệu điện thế tăng vì dây tóc nóng lên.", r"b) Các điểm không nằm trên đường thẳng qua gốc ($U$ không tỉ lệ thuận $I$) nên đèn không tuân theo định luật Ôm trong khoảng khảo sát.",
          r"c) Giữa $(0{,}50;3{,}0)$ và $(0{,}60;4{,}2)$ : hệ số góc $\dfrac{0{,}10}{1{,}2}\approx0{,}0833\ \text{A/V}$ ; $I=0{,}50+0{,}0833\cdot0{,}5\approx0{,}542\ \text{A}$ ; $R=\dfrac{3{,}5}{0{,}542}\approx6{,}46\ \Omega$ (nằm giữa $6{,}0$ và $7{,}0\ \Omega$ : hợp lí).",
          r"d) Hai điện trở nối tiếp : $U_{den}=8-4I$. Trên đoạn gần giao điểm, đường đặc trưng của đèn : $U_{den}=4{,}2+14\,(I-0{,}60)$. Cho hai biểu thức bằng nhau : $14I-4{,}2=8-4I\Rightarrow18I=12{,}2\Rightarrow I\approx0{,}678\ \text{A}$ ; $U_{den}=8-4\cdot0{,}678\approx5{,}29\ \text{V}$ (kiểm : $4{,}2+14\cdot0{,}078\approx5{,}29\ \text{V}$ ✓).",
          r"$P_{den}=U_{den}I\approx5{,}29\cdot0{,}678\approx3{,}59\ \text{W}$ ; $P_0=I^2R_0\approx0{,}678^2\cdot4\approx1{,}84\ \text{W}$ ; tổng $\approx5{,}43\ \text{W}$, bằng công suất nguồn $8\cdot0{,}678\approx5{,}42\ \text{W}$ (bảo toàn năng lượng).")),
]

def tu_luan():
    parts = []
    for k, (muc, de, gi) in enumerate(TL, 1):
        parts.append(f"<h4>Bài {k} · {muc}</h4>{de}<details><summary>Hướng dẫn giải</summary>{gi}</details>")
    return dict(label="Bài tập tự luận (xếp từ dễ đến khó)",
                body_html="<p>Các bài còn lại của chuyên đề, xếp từ dễ đến khó. Tự giải trên giấy rồi mới mở hướng dẫn.</p>" + "".join(parts))


# ═════════════ GHI FILE ═════════════
write(J, 160, "Chuyên đề 00. Kỹ năng nền: công cụ toán học, đọc đồ thị, sai số và thực hành", DANG, BUILD, ANALYSIS, SOLS, tu_luan())
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-10"
d["review"] = {"checked": False, "notes": "Chờ kiểm chéo (kiem-code) tự giải lại 6 dạng + buoc[]. Chuyên đề không có YCCĐ riêng: topic lấy YCCĐ con sát từng dạng."}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
print("xong", J)
