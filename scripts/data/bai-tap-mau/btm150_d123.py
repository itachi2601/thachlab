"""Bài tập mẫu CĐ15 "Âm thanh" (lesson 150) — Dạng 1–3. Module được build-hinh-150.py import.
Dàn ý + quy ước số liệu: content/hsg9/cd15-am-thanh/nguon.md (v_kk = 340 m/s, v_nước = 1500 m/s, tai người 20 Hz – 20 000 Hz,
tiếng vang khi âm phản xạ chậm hơn âm trực tiếp ít nhất 1/15 s).
Đề tránh trùng câu dự đoán của lý thuyết (sấm sau 3 s). Mọi đáp số tính lại bằng Python trong kiem_so()."""
import math
from fractions import Fraction as Fr
from dung import *   # sol, buoc, M/P/A, fig, seg, lbl, poly, arrow, chevron, RED/BLUE/ORG/GRN

GREY = "#94a3b8"
YEL = "#fbbf24"
TOPIC = "Bước sóng, chu kì, tần số, tốc độ truyền sóng"
V_KK, V_NUOC = 340, 1500


def anim(attr, vals, dur, kt=None):
    k = f' keyTimes="{kt}"' if kt else ""
    return f'<animate attributeName="{attr}" values="{vals}"{k} dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>'


def anim_tr(vals, dur, kt=None):
    k = f' keyTimes="{kt}"' if kt else ""
    return f'<animateTransform attributeName="transform" type="translate" values="{vals}"{k} dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>'


def stick(x, g, c="currentColor"):
    """Người đứng dạng que, chân chạm mặt đất y = g; trả (svg, toạ độ tai)."""
    hy = g - 62
    b = f'<circle cx="{x}" cy="{hy}" r="9" fill="none" stroke="{c}" stroke-width="2.2"/>'
    b += seg(x, hy + 9, x, g - 24, c, 2.2) + seg(x, g - 24, x - 9, g, c, 2.2) + seg(x, g - 24, x + 9, g, c, 2.2)
    b += seg(x, hy + 20, x - 12, hy + 34, c, 2.2) + seg(x, hy + 20, x + 12, hy + 34, c, 2.2)
    return b, (x, hy)


def cloud(x, y):
    p = (f'M{x - 44},{y + 14} q-4,-22 18,-22 q6,-18 28,-12 q14,-14 30,2 q22,-2 20,20 q8,14 -8,14 Z')
    return f'<path d="{p}" fill="none" stroke="{GREY}" stroke-width="2.4"/>'


def bolt(x, y, c=YEL):
    pts = [(x + 4, y), (x - 8, y + 34), (x + 4, y + 34), (x - 10, y + 76)]
    return poly(pts, c, 3)


# ═════════════ HÌNH ═════════════
# ───────────── Dạng 1 · chớp và sấm ─────────────
def d1(kk):
    G = 170
    b = ""
    if kk == 0:
        T_REAL = 4.5                      # chạy đúng thời gian thật
        b += f'<rect x="0" y="0" width="420" height="{G}" fill="{YEL}" opacity="0" stroke="none">{anim("opacity", "0;0.35;0;0", T_REAL, "0;0.02;0.06;1")}</rect>'
        b += cloud(62, 40) + bolt(56, 54)
        man, ear = stick(372, G)
        b += man + seg(16, G, 410, G, "currentColor", 2)
        sx, sy = 54, 110
        R = math.hypot(ear[0] - sx, ear[1] - sy) - 9
        b += (f'<circle cx="{sx}" cy="{sy}" r="0" fill="none" stroke="{ORG}" stroke-width="2.6" stroke-dasharray="7 5">'
              f'{anim("r", f"0;{R:.1f}", T_REAL)}</circle>')
        b += (f'<circle cx="{ear[0]}" cy="{ear[1]}" r="17" fill="none" stroke="{ORG}" stroke-width="2.4" opacity="0">'
              f'{anim("opacity", "0;0;1", T_REAL, "0;0.985;1")}</circle>')
        b += lbl(210, 24, "Thấy chớp lúc 0 s", YEL, 13, "middle", "700")
        b += lbl(210, 44, "Nghe sấm sau 4,5 s", ORG, 13, "middle", "700")
        b += arrow("", "g", 210, G + 18, 54, G + 18, 1.8) + arrow("", "g", 210, G + 18, 372, G + 18, 1.8)
        b += lbl(210, G + 14, "d = ?", GRN, 13, "middle", "700")
        return fig("c15-1-0", "0 0 420 196", "Tia chớp ở xa, mặt sóng âm của tiếng sấm lan dần tới người quan sát",
                   b, "Mô phỏng chạy đúng thời gian thật: tia chớp loé lúc 0 s, mặt sóng âm (vòng cam) tới tai sau 4,5 s. "
                      "Ánh sáng tới gần như tức thời. Hình không đúng tỉ lệ khoảng cách.")
    X0, X1, Y = 40, 380, 70
    K = (X1 - X0) / 5.0                  # px mỗi giây
    b += lbl(16, 22, "Mốc thời gian (tính từ lúc thấy chớp)", "currentColor", 13, "start", "700")
    b += seg(X0, Y, X1 + 14, Y, "currentColor", 1.8) + chevron(X1 + 14, Y, 1, 0, "currentColor", 1.8, 9)
    for s in range(6):
        b += seg(X0 + K * s, Y - 5, X0 + K * s, Y + 5, "currentColor", 1.4) + lbl(X0 + K * s, Y + 22, str(s), "currentColor", 12, "middle", "400")
    b += lbl(X1 + 14, Y + 40, "t (s)", "currentColor", 12, "end", "400")
    b += f'<circle cx="{X0}" cy="{Y}" r="5" fill="{YEL}"/>' + lbl(X0, Y - 12, "chớp", YEL, 12, "middle", "700")
    b += f'<circle cx="{X0 + K * 4.5:.1f}" cy="{Y}" r="5" fill="{ORG}"/>' + lbl(X0 + K * 4.5, Y - 12, "sấm (lần 1)", ORG, 12, "middle", "700")
    b += f'<circle cx="{X0 + K * 2:.1f}" cy="{Y}" r="5" fill="{BLUE}"/>' + lbl(X0 + K * 2, Y - 12, "sấm (lần sau)", BLUE, 12, "middle", "700")
    b += lbl(16, 124, "Âm đi một chiều: từ chỗ chớp tới tai", "currentColor", 12, "start", "400")
    b += lbl(16, 144, "v = 340 m/s trong không khí", "currentColor", 12, "start", "400")
    return fig("c15-1-2", "0 0 420 158", "Trục thời gian: chớp lúc 0 giây, sấm lần đầu nghe sau 4,5 giây, lần sau nghe sau 2 giây",
               b, "Dữ kiện: thời gian đo từ lúc thấy chớp tới lúc nghe sấm ; trục thời gian vẽ đúng tỉ lệ.")


# ───────────── Dạng 2 · đồ thị dao động hai âm ─────────────
X0G, PXMS, UNIT = 44, 34, 15          # gốc trục t, px mỗi ms, px mỗi đơn vị li độ
T_A, A_A, T_B, A_B = 4.0, 3, 2.5, 2   # chu kì (ms) và biên độ (đơn vị) của hai âm


def panel(yc, name, T, Amp, c, dur=None):
    b = ""
    for i in range(11):
        x = X0G + PXMS * i
        b += seg(x, yc - 3 * UNIT, x, yc + 3 * UNIT, GREY, 0.8, "", .55)
    for j in range(-3, 4):
        y = yc - UNIT * j
        b += seg(X0G, y, X0G + 10 * PXMS, y, GREY, 1.4 if j == 0 else 0.8, "", .9 if j == 0 else .55)
        b += lbl(X0G - 6, y + 4, ("+" if j > 0 else "") + str(j).replace("-", "−"), "currentColor", 11, "end", "400")
    for i in range(0, 11, 2):
        b += lbl(X0G + PXMS * i, yc + 3 * UNIT + 16, str(i), "currentColor", 12, "middle", "400")
    b += lbl(X0G + 10 * PXMS, yc + 3 * UNIT + 32, "t (ms)", "currentColor", 12, "end", "400")
    b += lbl(16, yc - 3 * UNIT - 8, name, c, 13, "start", "700")
    N = 400
    pts = [(X0G + PXMS * t, yc - UNIT * Amp * math.sin(2 * math.pi * t / T)) for t in [10 * k / N for k in range(N + 1)]]
    line = poly(pts, c, 2.6)
    if dur:
        # vẽ dần bằng stroke-dashoffset, mốc thời gian lấy theo t (keyTimes) nên đầu bút chạy đều theo thời gian thật
        cum = [0.0]
        for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
            cum.append(cum[-1] + math.hypot(xb - xa, yb - ya))
        L = cum[-1]; ks = range(0, N + 1, 10)
        vals = ";".join(f"{L - cum[k]:.1f}" for k in ks); kt = ";".join(f"{k / N:.3f}" for k in ks)
        line = line.replace("/>", f' stroke-dasharray="{L + 2:.1f}" stroke-dashoffset="0">{anim("stroke-dashoffset", vals, dur, kt)}</polyline>')
    return b + line


def d2(kk):
    b = ""
    if kk == 0:
        DUR = 5.0                                  # 10 ms thật → 5 s: chậm 500 lần
        b += panel(70, "Âm A", T_A, A_A, BLUE, DUR) + panel(226, "Âm B", T_B, A_B, ORG, DUR)
        return fig("c15-2-0", "0 0 420 304", "Màn hình dao động kí vẽ đồ thị dao động âm A (trên) và âm B (dưới) theo thời gian, có lưới ô vuông",
                   b, "Mô phỏng: màn hình vẽ dần đồ thị, chậm 500 lần (10 ms thật = 5 s). Mỗi ô ngang 1 ms ; mỗi ô dọc 1 đơn vị li độ, cùng thang cho hai âm.")
    yc, amp, Tpx, x0 = 92, 34, 120, 70
    pts = [(x0 + t, yc - amp * math.cos(2 * math.pi * t / Tpx)) for t in range(0, 302, 2)]
    b += seg(x0, yc, x0 + 300, yc, "currentColor", 1.6) + poly(pts, GRN, 2.4)
    xp1, xp2 = x0, x0 + Tpx                 # hai đỉnh liền nhau (hình mẫu, không có thang)
    b += seg(xp1, yc - amp, xp1, yc - amp - 18, GREY, 1.4, "4 3") + seg(xp2, yc - amp, xp2, yc - amp - 18, GREY, 1.4, "4 3")
    b += arrow("", "r", (xp1 + xp2) / 2, yc - amp - 14, xp1, yc - amp - 14, 1.8) + arrow("", "r", (xp1 + xp2) / 2, yc - amp - 14, xp2, yc - amp - 14, 1.8)
    b += lbl((xp1 + xp2) / 2, yc - amp - 22, "1 dao động = chu kì T", RED, 12, "middle", "700")
    xa = x0 + 1.5 * Tpx
    b += arrow("", "b", xa, yc, xa, yc + amp, 1.8) + lbl(xa, yc + amp + 18, "biên độ", BLUE, 12, "middle", "700")
    b += lbl(16, 172, "T: đo theo trục thời gian, đỉnh tới đỉnh kế tiếp", "currentColor", 12, "start", "400")
    b += lbl(16, 192, "Biên độ: đo theo trục li độ, từ đường 0 tới đỉnh", "currentColor", 12, "start", "400")
    return fig("c15-2-2", "0 0 420 204", "Đồ thị dao động mẫu: chu kì đo giữa hai đỉnh liền nhau, biên độ đo từ đường 0 tới đỉnh",
               b, "Hình mẫu cách đọc đồ thị (không theo thang của đề): đọc chu kì và biên độ trên lưới của đề.")


# ───────────── Dạng 3 · sonar + tiếng vang ─────────────
def pulse(x, y, down, c):
    """Ba cung nhỏ của xung âm tại (x, y), lồi theo hướng đi."""
    s = 1 if down else -1
    out = ""
    for k, w in enumerate((10, 16, 22)):
        yy = y - s * 6 * k
        out += f'<path d="M{x - w},{yy:.1f} Q{x},{yy + s * 9:.1f} {x + w},{yy:.1f}" fill="none" stroke="{c}" stroke-width="2.4"/>'
    return out


def ship(x, y):
    hull = f'<path d="M{x - 40},{y - 12} L{x + 40},{y - 12} L{x + 28},{y + 6} L{x - 28},{y + 6} Z" fill="none" stroke="currentColor" stroke-width="2.4"/>'
    return hull + f'<rect x="{x - 14}" y="{y - 28}" width="28" height="16" fill="none" stroke="currentColor" stroke-width="2"/>'


def sea(y, x0=16, x1=404):
    pts = [(x, y + 3 * math.sin(x / 9)) for x in range(x0, x1 + 1, 4)]
    return poly(pts, BLUE, 2, "", .9)


def fish_school(x, y, c=ORG):
    """Đàn cá: vài con cá nhỏ (thân elip + đuôi) quanh (x, y)."""
    out = ""
    for dx, dy in ((-30, -4), (-6, 6), (18, -6), (40, 4), (-48, 8)):
        cx, cy = x + dx, y + dy
        out += (f'<ellipse cx="{cx}" cy="{cy}" rx="9" ry="4.5" fill="none" stroke="{c}" stroke-width="2"/>'
                f'<path d="M{cx + 9},{cy} L{cx + 15},{cy - 4} L{cx + 15},{cy + 4} Z" fill="none" stroke="{c}" stroke-width="1.6"/>')
    return out


def seabed(y, x0=16, x1=404):
    pts = [(x, y + 5 * math.sin(x / 23) + 3 * math.sin(x / 7)) for x in range(x0, x1 + 1, 6)]
    return poly(pts, ORG, 2.4)


def d3(kk):
    b = ""
    if kk == 0:
        SX, SURF, BED = 150, 46, 206
        D = BED - 12 - (SURF + 14)           # quãng đường xung đi (px)
        DUR = 2.4                             # 0,24 s thật → 2,4 s: chậm 10 lần
        b += sea(SURF) + fish_school(SX, BED) + ship(SX, SURF)
        b += lbl(250, 82, "nước: v = 1500 m/s", BLUE, 12, "start", "700")
        b += lbl(250, 104, "đi và về: 0,24 s", "currentColor", 12, "start", "700")
        b += seg(SX + 64, SURF + 8, SX + 64, BED - 6, GRN, 1.6, "5 4") + lbl(SX + 72, (SURF + BED) / 2 + 30, "h = ?", GRN, 13, "start", "700")
        y0 = SURF + 14
        b += (f'<g>{anim_tr(f"0,0;0,{D};0,{D}", DUR, "0;0.5;1")}{anim("opacity", "1;1;0;0", DUR, "0;0.5;0.52;1")}'
              f'{pulse(SX, y0, True, BLUE)}</g>')
        b += (f'<g opacity="0">{anim_tr(f"0,{D};0,{D};0,0", DUR, "0;0.5;1")}{anim("opacity", "0;0;1;1", DUR, "0;0.5;0.52;1")}'
              f'{pulse(SX, y0, False, ORG)}</g>')
        b += (f'<circle cx="{SX}" cy="{SURF - 4}" r="26" fill="none" stroke="{ORG}" stroke-width="2.2" opacity="0">'
              f'{anim("opacity", "0;0;1", DUR, "0;0.985;1")}</circle>')
        b += lbl(SX, BED + 26, "đàn cá", ORG, 12, "middle", "700")
        return fig("c15-3-0", "0 0 420 236", "Tàu cá phát xung siêu âm thẳng xuống, xung phản xạ ở đàn cá rồi trở lại tàu",
                   b, "Mô phỏng chạy chậm 10 lần (1 s mô phỏng = 0,1 s thật): xung xanh đi xuống, phản xạ ở đàn cá thành xung cam đi lên. "
                      "Hình không đúng tỉ lệ độ sâu.")
    # trái: sonar ; phải: người – tường 8 m
    SX, SURF, BED = 80, 40, 176
    b += sea(SURF, 16, 190) + fish_school(SX, BED + 4) + ship(SX, SURF)
    b += arrow("", "b", SX - 12, SURF + 12, SX - 12, BED - 10, 2.2) + lbl(SX - 20, (SURF + BED) / 2, "đi", BLUE, 12, "end", "700")
    b += arrow("", "o", SX + 12, BED - 10, SX + 12, SURF + 12, 2.2) + lbl(SX + 20, (SURF + BED) / 2, "về", ORG, 12, "start", "700")
    b += lbl(150, 96, "h = ?", GRN, 13, "start", "700")
    b += lbl(16, 206, "0,24 s = thời gian đi + về", "currentColor", 12, "start", "400")
    G, WX, PX = 176, 392, 262
    b += seg(222, G, 404, G, "currentColor", 2) + seg(WX, 60, WX, G, "currentColor", 4)
    for yy in range(66, G, 14):
        b += seg(WX + 2, yy, WX + 10, yy - 8, GREY, 1.2)
    man, ear = stick(PX, G)
    b += man
    b += arrow("", "b", PX + 16, ear[1] - 4, WX - 6, ear[1] - 4, 2) + arrow("", "o", WX - 6, ear[1] + 10, PX + 16, ear[1] + 10, 2)
    b += arrow("", "g", (PX + WX) / 2, G + 14, PX, G + 14, 1.6) + arrow("", "g", (PX + WX) / 2, G + 14, WX, G + 14, 1.6)
    b += lbl((PX + WX) / 2, G + 30, "8 m", GRN, 13, "middle", "700")
    b += lbl(222, 30, "Âm trực tiếp tới tai ngay", "currentColor", 12, "start", "400")
    return fig("c15-3-2", "0 0 420 216", "Bên trái: siêu âm đi từ tàu xuống đàn cá rồi về. Bên phải: người nói cách tường 8 mét, âm tới tường rồi dội lại",
               b, "Dữ kiện: thời gian đo được ở tàu gồm cả lượt đi và lượt về ; người vừa là nguồn âm vừa là người nghe. Hình không đúng tỉ lệ.")


BUILD = [d1, d2, d3]


# ═════════════ ĐỀ ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Tốc độ truyền âm: thấy chớp rồi mới nghe sấm, quãng đường và thời gian truyền",
      topic=TOPIC,
      problem_html=r"""<p>Trong một cơn giông, một bạn thấy tia chớp, sau $4{,}5\ \text{s}$ mới nghe tiếng sấm. Tốc độ âm trong không khí là $340\ \text{m/s}$ ; coi ánh sáng truyền tới mắt tức thời.</p><ol type="a"><li>Chỗ có tia chớp cách bạn bao xa?</li><li>Một lúc sau, bạn thấy tia chớp khác và nghe sấm sau $2{,}0\ \text{s}$. Cơn giông đang tiến lại gần hay đi ra xa? Chỗ có tia chớp lúc này cách bạn bao xa?</li><li>Nếu một tiếng nổ phát ra trong nước và truyền đúng quãng đường ở câu a thì sau bao lâu âm tới nơi? Biết tốc độ âm trong nước là $1500\ \text{m/s}$. Âm trong nước nhanh hơn trong không khí bao nhiêu lần?</li></ol>"""),
 dict(label="Dạng 2 · Cơ bản · Tần số, độ cao, độ to: đọc đồ thị dao động hai âm, xếp hạ âm – siêu âm",
      topic=TOPIC,
      problem_html=r"""<p>Hình dưới là đồ thị dao động của hai âm A và B thu bằng micro, hiện trên màn hình dao động kí. Mỗi ô theo trục ngang ứng với $1\ \text{ms}$ ($1\ \text{ms}=10^{-3}\ \text{s}$) ; mỗi ô theo trục dọc ứng với $1$ đơn vị li độ, cùng thang cho hai âm.</p><ol type="a"><li>Tìm chu kì và tần số của mỗi âm.</li><li>Âm nào cao hơn? Âm nào to hơn? Giải thích.</li><li>Nguồn C là một tấm thép mỏng dao động $1500$ lần trong $2$ phút. Nguồn D là một còi xua chuột, màng còi dao động $45\,000$ lần trong $1{,}5\ \text{s}$. Tính tần số của C và D. Tai người nghe được âm của những nguồn nào trong bốn nguồn A, B, C, D? Biết tai người nghe được âm có tần số từ $20\ \text{Hz}$ đến $20\,000\ \text{Hz}$.</li></ol>"""),
 dict(label="Dạng 3 · Cơ bản · Tiếng vang: máy dò cá bằng siêu âm, khoảng cách tối thiểu để nghe tiếng vang",
      topic=TOPIC,
      problem_html=r"""<p>Biết tốc độ âm trong nước là $1500\ \text{m/s}$, trong không khí là $340\ \text{m/s}$. Tai nghe được tiếng vang khi âm phản xạ tới tai chậm hơn âm phát ra trực tiếp ít nhất $\dfrac{1}{15}\ \text{s}$.</p><ol type="a"><li>Máy dò cá trên một tàu đánh cá phát xung siêu âm thẳng xuống, sau $0{,}24\ \text{s}$ thì thu được xung phản xạ từ một đàn cá. Đàn cá ở độ sâu bao nhiêu mét so với tàu?</li><li>Một người đứng trước một vách đá và nói to. Người đó phải đứng cách vách ít nhất bao nhiêu mét thì nghe được tiếng vang của chính mình?</li><li>Trong một hội trường, người nói đứng cách bức tường phía sau $8\ \text{m}$. Âm phản xạ từ bức tường tới tai người nói chậm hơn âm trực tiếp bao nhiêu giây? Người đó có nghe được tiếng vang không?</li></ol>"""),
]

# ═════════════ BẢNG PHÂN TÍCH ĐỀ ═════════════
ANALYSIS = [
 # Dạng 1
 [(r'"thấy tia chớp, sau $4{,}5\ \text{s}$ mới nghe tiếng sấm"', r"$t_1=4{,}5\ \text{s}$", r"Chớp và sấm sinh ra cùng lúc<br>Thời gian chênh là thời gian âm đi tới tai"),
  (r'"coi ánh sáng truyền tới mắt tức thời"', r"Bỏ qua thời gian ánh sáng đi", r"⚠ giả thiết dùng được vì ánh sáng ($\approx3\cdot10^8\ \text{m/s}$) nhanh hơn âm rất nhiều"),
  (r'"Tốc độ âm trong không khí là $340\ \text{m/s}$"', r"$v=340\ \text{m/s}$", r"Âm truyền đều : $s=v\,t$<br>Âm đi một chiều hay đi rồi về?"),
  (r'"nghe sấm sau $2{,}0\ \text{s}$"', r"$t_2=2{,}0\ \text{s}$", r"Thời gian ngắn hơn thì chỗ chớp gần hơn hay xa hơn?"),
  (r'"tiếng nổ phát ra trong nước và truyền đúng quãng đường ở câu a … tốc độ âm trong nước là $1500\ \text{m/s}$"', r"$v_n=1500\ \text{m/s}$ ; quãng đường như câu a", r"$t=\dfrac{s}{v_n}$<br>So sánh hai tốc độ bằng tỉ số $\dfrac{v_n}{v}$")],
 # Dạng 2
 [(r'"Mỗi ô theo trục ngang ứng với $1\ \text{ms}$"', r"$1\ \text{ô}=1\ \text{ms}=10^{-3}\ \text{s}$", r"Chu kì $T$ = thời gian của một dao động<br>⚠ đếm trọn dao động : đỉnh tới đỉnh kế tiếp<br>Đổi ms ra s trước khi tính $f$"),
  (r'"Tìm chu kì và tần số của mỗi âm"', r"Đọc $T_A$, $T_B$ trên lưới", r"$f=\dfrac{1}{T}$<br>Đỉnh của âm B có rơi đúng vạch lưới không? Nếu không, đọc $T_B$ thế nào cho chính xác?"),
  (r'"Âm nào cao hơn? Âm nào to hơn?"', r"So sánh tần số và biên độ", r"Tần số lớn → âm cao<br>Biên độ lớn → âm to<br>⚠ hai tiêu chí độc lập nhau"),
  (r'"dao động $1500$ lần trong $2$ phút" ; "dao động $45\,000$ lần trong $1{,}5\ \text{s}$"', r"$N_C=1500$, $t_C=2\ \text{phút}$ ; $N_D=45\,000$, $t_D=1{,}5\ \text{s}$", r"$f=\dfrac{N}{t}$ với $t$ tính bằng giây"),
  (r'"tai người nghe được âm có tần số từ $20\ \text{Hz}$ đến $20\,000\ \text{Hz}$"', r"Ngưỡng nghe của tai", r"Dưới $20\ \text{Hz}$ : hạ âm<br>Trên $20\,000\ \text{Hz}$ : siêu âm")],
 # Dạng 3
 [(r'"phát xung siêu âm thẳng xuống, sau $0{,}24\ \text{s}$ thì thu được xung phản xạ từ một đàn cá"', r"$t=0{,}24\ \text{s}$ ; $v=1500\ \text{m/s}$", r"⚠ thời gian đo gồm cả lượt đi xuống và lượt về"),
  (r'"Đàn cá ở độ sâu bao nhiêu mét so với tàu?"', r"Cần $h$", r"Quãng đường âm đi bằng mấy lần $h$?"),
  (r'"chậm hơn âm phát ra trực tiếp ít nhất $\dfrac{1}{15}\ \text{s}$"', r"$\Delta t\ge\dfrac{1}{15}\ \text{s}$ ; $v=340\ \text{m/s}$", r"Âm phản xạ đi thêm quãng $2d$ so với âm trực tiếp<br>$\Delta t=\dfrac{2d}{v}$"),
  (r'"người nói đứng cách bức tường phía sau $8\ \text{m}$"', r"$d=8\ \text{m}$", r"Tính $\Delta t$ rồi so với $\dfrac{1}{15}\ \text{s}$<br>⚠ vật phản xạ phải đủ xa mới tách được hai âm")],
]

# ═════════════ LỜI GIẢI ═════════════
R1 = [r"<strong>Khái niệm:</strong> âm cần môi trường để truyền ; trong một môi trường đồng nhất, âm truyền với tốc độ không đổi.",
      r"<strong>Công thức:</strong> $s=v\,t$ ; $t=\dfrac{s}{v}$.",
      r"<strong>Điều kiện:</strong> ánh sáng tới gần như tức thời nên thời gian chênh giữa chớp và sấm là thời gian âm truyền."]
R2 = [r"<strong>Khái niệm:</strong> chu kì $T$ là thời gian một dao động ; tần số $f$ là số dao động trong $1\ \text{s}$.",
      r"<strong>Công thức:</strong> $f=\dfrac{1}{T}=\dfrac{N}{t}$ (đơn vị Hz).",
      r"<strong>Độ cao – độ to:</strong> tần số lớn thì âm cao ; biên độ lớn thì âm to.",
      r"<strong>Ngưỡng nghe:</strong> tai người nghe từ $20\ \text{Hz}$ đến $20\,000\ \text{Hz}$ ; dưới là hạ âm, trên là siêu âm.",
      r"<strong>Điều kiện:</strong> $T$ và $t$ đổi ra giây trước khi tính $f$."]
R3 = [r"<strong>Khái niệm:</strong> âm gặp vật cản bị phản xạ ; tiếng vang là âm phản xạ tới tai sau âm trực tiếp ít nhất $\dfrac{1}{15}\ \text{s}$.",
      r"<strong>Công thức:</strong> âm đi tới vật cản cách $d$ rồi về : quãng đường $2d=v\,t$ ; $\Delta t=\dfrac{2d}{v}$.",
      r"<strong>Điều kiện:</strong> nguồn âm và nơi thu đặt cùng chỗ ; âm đi thẳng tới vật cản rồi dội ngược lại."]

SOLS = [
 sol(R1, [
  ("Khoảng cách tới tia chớp lần đầu", [P(r"Âm đi từ chỗ chớp tới tai trong $t_1=4{,}5\ \text{s}$ :"), M(r"d_1=v\,t_1=340\cdot4{,}5"), A(r"d_1=1530\ \text{m}\approx1{,}53\ \text{km}")]),
  ("Khoảng cách tới tia chớp lần sau", [P(r"Thời gian nghe sấm ngắn hơn ($2{,}0\ \text{s}\lt4{,}5\ \text{s}$) nên chỗ chớp gần hơn : cơn giông đang tiến lại gần."),
     M(r"d_2=v\,t_2=340\cdot2{,}0"), A(r"d_2=680\ \text{m}"),
     P(r"Chỗ chớp đã dịch lại gần thêm $1530-680=850\ \text{m}$.")]),
  ("Thời gian truyền trong nước", [P(r"Cùng quãng đường $d_1=1530\ \text{m}$, tốc độ $v_n=1500\ \text{m/s}$ :"), M(r"t_n=\dfrac{d_1}{v_n}=\dfrac{1530}{1500}"), A(r"t_n=1{,}02\ \text{s}"),
     M(r"\dfrac{v_n}{v}=\dfrac{1500}{340}\approx4{,}41")]),
  ("Kiểm tra", [P(r"Đơn vị : $\text{m/s}\cdot\text{s}=\text{m}$ ✓."),
     P(r"Tỉ số thời gian $\dfrac{4{,}5}{1{,}02}\approx4{,}41$ đúng bằng tỉ số tốc độ ✓ : cùng quãng đường, tốc độ lớn gấp bao nhiêu lần thì thời gian nhỏ đi bấy nhiêu lần."),
     P(r"Ước lượng nhanh : cứ khoảng $3\ \text{s}$ là âm đi được khoảng $1\ \text{km}$ ; $4{,}5\ \text{s}$ ứng với khoảng $1{,}5\ \text{km}$ ✓.")])],
  [r"a) $d_1=1530\ \text{m}$", r"b) Cơn giông tiến lại gần ; $d_2=680\ \text{m}$", r"c) $t_n=1{,}02\ \text{s}$ ; âm trong nước nhanh hơn khoảng $4{,}41$ lần"],
  r"Nhận dạng: thấy <strong>tia chớp, sau t giây mới nghe sấm</strong> → âm đi một chiều, $s=v\,t$ (không chia 2)."),
 sol(R2, [
  ("Chu kì âm A", [P(r"Đồ thị A có đỉnh tại $t=1\ \text{ms}$ và đỉnh kế tiếp tại $t=5\ \text{ms}$ :"), M(r"T_A=5-1"), A(r"T_A=4\ \text{ms}=0{,}004\ \text{s}"),
     M(r"f_A=\dfrac{1}{T_A}=\dfrac{1}{0{,}004}=250\ \text{Hz}")]),
  ("Tần số âm B", [P(r"Đỉnh của B không rơi đúng vạch lưới, nên đếm số dao động trọn vẹn : trong $10\ \text{ms}$ có đúng $4$ dao động (B cắt đường 0 đi lên tại $0$ ; $2{,}5$ ; $5$ ; $7{,}5$ ; $10\ \text{ms}$)."),
     M(r"T_B=\dfrac{10\ \text{ms}}{4}=2{,}5\ \text{ms}=0{,}0025\ \text{s}"), M(r"f_B=\dfrac{1}{T_B}=\dfrac{1}{0{,}0025}"), A(r"f_B=400\ \text{Hz}")]),
  ("Âm cao hơn, âm to hơn", [P(r"$f_B=400\ \text{Hz}\gt f_A=250\ \text{Hz}$ nên <strong>âm B cao hơn</strong>."),
     P(r"Biên độ A là $3$ ô, của B là $2$ ô (cùng thang) nên <strong>âm A to hơn</strong>."),
     P(r"Âm to hơn chưa chắc cao hơn : độ to theo biên độ, độ cao theo tần số.")]),
  ("Tần số nguồn C", [P(r"Đổi $t_C=2\ \text{phút}=120\ \text{s}$ :"), M(r"f_C=\dfrac{N_C}{t_C}=\dfrac{1500}{120}"), A(r"f_C=12{,}5\ \text{Hz}")]),
  ("Tần số nguồn D", [M(r"f_D=\dfrac{N_D}{t_D}=\dfrac{45\,000}{1{,}5}"), A(r"f_D=30\,000\ \text{Hz}")]),
  ("Nguồn tai người nghe được", [P(r"$f_C=12{,}5\ \text{Hz}\lt20\ \text{Hz}$ : C phát <strong>hạ âm</strong>."),
     P(r"$f_D=30\,000\ \text{Hz}\gt20\,000\ \text{Hz}$ : D phát <strong>siêu âm</strong>."),
     P(r"$250\ \text{Hz}$ và $400\ \text{Hz}$ nằm trong khoảng nghe được : tai người chỉ nghe được <strong>A và B</strong>."),
     P(r"Kiểm tra : $T_A/T_B=4/2{,}5=1{,}6=f_B/f_A$ ✓."),
     P(r"Đơn vị : tần số tính bằng $1/\text{s}=\text{Hz}$ ✓.")])],
  [r"a) $T_A=4\ \text{ms}$, $f_A=250\ \text{Hz}$ ; $T_B=2{,}5\ \text{ms}$, $f_B=400\ \text{Hz}$", r"b) Âm B cao hơn (tần số lớn hơn) ; âm A to hơn (biên độ lớn hơn)",
   r"c) $f_C=12{,}5\ \text{Hz}$ (hạ âm) ; $f_D=30\,000\ \text{Hz}$ (siêu âm) ; tai người nghe được A và B"],
  r"Nhận dạng: thấy <strong>đồ thị dao động, mỗi ô … ms</strong> → đếm trọn dao động ra $T$, $f=1/T$ ; độ cao theo $f$, độ to theo biên độ."),
 sol(R3, [
  ("Quãng đường xung siêu âm đi", [P(r"Trong $0{,}24\ \text{s}$ xung đi từ tàu xuống đàn cá rồi trở lại tàu :"), M(r"s=v\,t=1500\cdot0{,}24"), A(r"s=360\ \text{m}")]),
  ("Độ sâu của đàn cá", [P(r"Quãng đường $s$ gồm lượt đi và lượt về, mỗi lượt bằng độ sâu :"), M(r"h=\dfrac{s}{2}=\dfrac{360}{2}"), A(r"h=180\ \text{m}")]),
  ("Khoảng cách tối thiểu để nghe tiếng vang", [P(r"Âm phản xạ đi thêm quãng $2d$ ; cần $\Delta t=\dfrac{2d}{v}\ge\dfrac{1}{15}\ \text{s}$ :"),
     M(r"2d\ge v\cdot\dfrac{1}{15}=\dfrac{340}{15}"), M(r"d\ge\dfrac{340}{2\cdot15}"), A(r"d_{min}\approx11{,}3\ \text{m}")]),
  ("Thời gian chênh giữa âm phản xạ và âm trực tiếp", [P(r"Âm trực tiếp tới tai người nói ngay ; âm phản xạ đi tới tường rồi về, quãng $2d=16\ \text{m}$ :"),
     M(r"\Delta t=\dfrac{2d}{v}=\dfrac{16}{340}"), A(r"\Delta t\approx0{,}047\ \text{s}")]),
  ("Có nghe được tiếng vang không", [P(r"So sánh : $\dfrac{1}{15}\ \text{s}\approx0{,}067\ \text{s}$ ; $\Delta t\approx0{,}047\ \text{s}\lt0{,}067\ \text{s}$."),
     P(r"Âm phản xạ tới quá sớm, hoà vào âm trực tiếp : người nói <strong>không nghe được tiếng vang</strong> (chỉ thấy tiếng nói kéo dài, nghe ồm hơn)."),
     P(r"Khớp với câu b : $8\ \text{m}\lt11{,}3\ \text{m}$ ✓.")]),
  ("Kiểm tra", [P(r"Đàn cá ở độ sâu $180\ \text{m}$ là hợp lí ✓."),
     P(r"Nếu quên chia 2 sẽ ra gấp đôi độ sâu thật."),
     P(r"Đơn vị : $\dfrac{\text{m}}{\text{m/s}}=\text{s}$ ✓.")])],
  [r"a) $h=180\ \text{m}$", r"b) $d_{min}\approx11{,}3\ \text{m}$", r"c) $\Delta t\approx0{,}047\ \text{s}\lt\dfrac{1}{15}\ \text{s}$ : không nghe được tiếng vang"],
  r"Nhận dạng: thấy <strong>phát rồi thu lại âm phản xạ</strong> → âm đi hai lượt, $2d=v\,t$ ; thấy <strong>tiếng vang</strong> → so $\Delta t=2d/v$ với $\tfrac{1}{15}\ \text{s}$."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC ═════════════
STEPS = [
 # ── Dạng 1 ──
 dict(nhan_dang=r"Thấy <b>tia chớp, sau t giây mới nghe sấm</b> → âm đi một chiều : $s=v\,t$.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Khoảng cách tới tia chớp lần đầu", "Chỗ có tia chớp lần đầu cách bạn bao nhiêu mét?", 1530, "m", 5,
       loi=r"Chia đôi kết quả như bài tiếng vang ; ở đây âm chỉ đi một chiều, từ chỗ chớp tới tai."),
  buoc("Khoảng cách tới tia chớp lần sau", "Chỗ có tia chớp lần sau cách bạn bao nhiêu mét?", 680, "m", 3,
       loi=r"Lấy hiệu hai thời gian nhân với tốc độ âm ; con số đó là đoạn cơn giông đã dịch lại, không phải khoảng cách lúc sau.",
       ke=[(r"Tính $d_2=v\,t_2$ với thời gian nghe sấm của lần sau", True),
           (r"Tính $v\,(t_1-t_2)$", r"Đó là đoạn chỗ chớp đã dịch lại gần, không phải khoảng cách từ chỗ chớp mới tới bạn."),
           (r"Tính $\dfrac{v\,t_2}{2}$", r"Âm sấm đi thẳng một chiều tới tai, không phản xạ nên không chia 2.")]),
  buoc("Thời gian truyền trong nước", "Âm truyền trong nước hết bao nhiêu giây?", 1.02, "s", 0.02,
       loi=r"Giữ nguyên thời gian của không khí vì nghĩ cùng quãng đường thì cùng thời gian, hoặc nhân với tỉ số tốc độ theo chiều ngược.",
       ke=[(r"Tính $t_n=\dfrac{d_1}{v_n}$ với tốc độ âm trong nước", True),
           (r"Giữ $t=4{,}5\ \text{s}$ vì quãng đường không đổi", r"Cùng quãng đường nhưng tốc độ khác thì thời gian khác ; âm trong nước nhanh hơn nên tới sớm hơn."),
           (r"Tính $t_n=4{,}5\cdot\dfrac{v_n}{v}$", r"Tỉ số đặt ngược : tốc độ lớn hơn thì thời gian phải nhỏ hơn, nên phải nhân với $\dfrac{v}{v_n}$.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 2 ──
 dict(nhan_dang=r"Thấy <b>đồ thị dao động, mỗi ô … ms</b> → đếm trọn dao động ra $T$ ; cao theo $f$, to theo biên độ.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Chu kì âm A", "Chu kì của âm A là bao nhiêu mili giây?", 4, "ms", 0.1,
       loi=r"Đo từ một đỉnh tới đáy liền kề ; khoảng đó chỉ là nửa dao động."),
  buoc("Tần số âm B", "Tần số của âm B là bao nhiêu Hz?", 400, "Hz", 5,
       loi=r"Đếm số đỉnh trên màn hình rồi coi đó là tần số, hoặc để chu kì theo ms khi lấy nghịch đảo.",
       ke=[(r"Đếm số dao động trọn vẹn trong $10\ \text{ms}$ để ra $T_B$, đổi ra giây rồi lấy $f=\dfrac{1}{T}$", True),
           (r"Đo $T_B$ từ một đỉnh tới đáy liền kề", r"Từ đỉnh tới đáy liền kề chỉ là nửa dao động ; tần số sẽ ra gấp đôi."),
           (r"Lấy $f=\dfrac{1}{T_B}$ với $T_B$ để nguyên theo ms", r"Hz là số dao động trong một giây ; để $T$ theo ms thì $f$ nhỏ đi $1000$ lần.")]),
  buoc("Âm cao hơn, âm to hơn", "Kết luận nào đúng?",
       lua_chon=[(r"Âm B cao hơn ; âm A to hơn", True),
                 (r"Âm A vừa cao hơn vừa to hơn", r"Biên độ chỉ quyết định độ to ; độ cao do tần số quyết định."),
                 (r"Âm B to hơn vì dao động dày hơn", r"Dao động dày hơn nghĩa là tần số lớn hơn, tức âm cao hơn, chưa nói gì về độ to.")],
       loi=r"Gộp độ to với độ cao : cho rằng âm có biên độ lớn thì cũng cao hơn.",
       ke=[(r"So sánh tần số để xét độ cao, so sánh biên độ để xét độ to", True),
           (r"So sánh biên độ để xét cả độ cao lẫn độ to", r"Biên độ chỉ cho biết độ to ; độ cao phải xét bằng tần số."),
           (r"So sánh chu kì : chu kì lớn hơn thì âm cao hơn", r"Chu kì lớn thì tần số nhỏ, âm trầm hơn chứ không cao hơn.")]),
  buoc("Tần số nguồn C", "Tần số của nguồn C là bao nhiêu Hz?", 12.5, "Hz", 0.2,
       loi=r"Để thời gian theo phút khi chia, hoặc lấy thời gian chia số dao động (ra chu kì chứ không phải tần số).",
       ke=[(r"Đổi $2$ phút ra giây rồi tính $f=\dfrac{N}{t}$", True),
           (r"Tính $f=\dfrac{N}{t}$ với $t=2$", r"Tần số là số dao động trong một giây ; để $t$ theo phút thì kết quả lớn gấp $60$ lần."),
           (r"Tính $f=\dfrac{t}{N}$", r"$\dfrac{t}{N}$ là thời gian một dao động, tức chu kì, không phải tần số.")]),
  buoc("Tần số nguồn D", "Tần số của nguồn D là bao nhiêu Hz?", 30000, "Hz", 100,
       loi=r"Nhân số dao động với thời gian thay vì chia.",
       ke=[(r"Tính $f=\dfrac{N}{t}$ với $t=1{,}5\ \text{s}$", True),
           (r"Tính $f=N\cdot t$", r"Tần số là số dao động trong một giây nên phải chia số dao động cho thời gian."),
           (r"Lấy luôn $f=N$", r"$N$ là số dao động trong $1{,}5\ \text{s}$, không phải trong $1\ \text{s}$.")]),
  buoc("Nguồn tai người nghe được", "Tai người nghe được âm của những nguồn nào?",
       lua_chon=[(r"Chỉ A và B", True),
                 (r"A, B và D", r"Tần số của D vượt $20\,000\ \text{Hz}$ : đó là siêu âm, tai người không nghe được."),
                 (r"Cả bốn nguồn, vì nguồn nào cũng đang dao động", r"Vật dao động luôn phát âm, nhưng tai chỉ nghe được âm có tần số từ $20\ \text{Hz}$ đến $20\,000\ \text{Hz}$.")],
       loi=r"Nghĩ rằng cứ vật dao động là tai nghe được ; quên so tần số với ngưỡng nghe của tai.",
       ke=[(r"So từng tần số với khoảng $20\ \text{Hz}$ – $20\,000\ \text{Hz}$", True),
           (r"Chọn nguồn có biên độ lớn vì âm to thì nghe được", r"Hạ âm, siêu âm dù to vẫn không nghe được ; điều kiện nghe là tần số."),
           (r"Chọn nguồn dao động nhiều lần nhất", r"Số lần dao động phải chia cho thời gian mới ra tần số ; nhiều lần chưa chắc nằm trong ngưỡng nghe.")])]),
 # ── Dạng 3 ──
 dict(nhan_dang=r"Thấy <b>phát âm rồi thu âm phản xạ</b> → âm đi hai lượt : $2d=v\,t$.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Quãng đường xung siêu âm đi", "Trong thời gian đo được, xung siêu âm đi được quãng đường bao nhiêu mét?", 360, "m", 2,
       loi=r"Dùng tốc độ âm trong không khí cho xung đi trong nước."),
  buoc("Độ sâu của đàn cá", "Đàn cá ở độ sâu bao nhiêu mét?", 180, "m", 1,
       loi=r"Lấy luôn quãng đường xung đi làm độ sâu, quên rằng xung đi xuống rồi mới trở về.",
       ke=[(r"Chia quãng đường cho 2 vì gồm lượt đi và lượt về", True),
           (r"Lấy độ sâu bằng quãng đường xung đã đi", r"Thời gian đo là từ lúc phát tới lúc thu lại, gồm cả đi xuống và đi lên."),
           (r"Tính lại với $v=340\ \text{m/s}$ rồi chia 2", r"Xung truyền trong nước nên dùng tốc độ âm trong nước.")]),
  buoc("Khoảng cách tối thiểu để nghe tiếng vang", "Người đó phải đứng cách vách ít nhất bao nhiêu mét?", 11.3, "m", 0.1,
       loi=r"Lấy $d=v\cdot\dfrac{1}{15}$ ; quên âm phải đi tới vách rồi quay về.",
       ke=[(r"Cho quãng đi – về $2d=v\cdot\dfrac{1}{15}$", True),
           (r"Cho $d=v\cdot\dfrac{1}{15}$", r"Trong $\dfrac{1}{15}\ \text{s}$ âm phải đi tới vách rồi về, tức quãng $2d$, nên kết quả này gấp đôi."),
           (r"Cho $d=\dfrac{v\cdot15}{2}$", r"Thời gian tối thiểu là $\dfrac{1}{15}\ \text{s}$ chứ không phải $15\ \text{s}$ : phép nhân này đặt nhầm chỗ.")]),
  buoc("Thời gian chênh giữa âm phản xạ và âm trực tiếp", "Âm phản xạ tới tai chậm hơn âm trực tiếp bao nhiêu giây?", 0.047, "s", 0.004,
       loi=r"Chỉ tính thời gian âm đi tới tường, bỏ lượt dội về.",
       ke=[(r"Tính $\Delta t=\dfrac{2d}{v}$", True),
           (r"Tính $\Delta t=\dfrac{d}{v}$", r"Âm phản xạ phải đi tới tường rồi quay về tai, quãng đường là $2d$."),
           (r"Tính $\Delta t=2d\cdot v$", r"Thời gian bằng quãng đường chia tốc độ ; nhân hai đại lượng cho đơn vị $\text{m}^2/\text{s}$, không phải giây.")]),
  buoc("Có nghe được tiếng vang không", "Người nói có nghe được tiếng vang không?",
       lua_chon=[(r"Không, vì thời gian chênh nhỏ hơn $\dfrac{1}{15}\ \text{s}$", True),
                 (r"Có, vì tường cứng, nhẵn phản xạ âm tốt", r"Phản xạ tốt là cần nhưng chưa đủ ; âm phản xạ còn phải tới chậm hơn ít nhất $\dfrac{1}{15}\ \text{s}$."),
                 (r"Có, vì âm phản xạ luôn tới tai sau âm trực tiếp", r"Tới sau nhưng quá sớm thì tai không tách được hai âm ; cần chậm ít nhất $\dfrac{1}{15}\ \text{s}$.")],
       loi=r"Cho rằng cứ có tường phản xạ là nghe được tiếng vang, không so thời gian chênh với $\dfrac{1}{15}\ \text{s}$.",
       ke=[(r"So thời gian chênh vừa tính với $\dfrac{1}{15}\ \text{s}$", True),
           (r"Xét tường có cứng, nhẵn không", r"Tường nào cũng phản xạ một phần ; điều kiện quyết định tiếng vang là thời gian chênh."),
           (r"Xét người nói to hay nhỏ", r"Độ to chỉ làm âm phản xạ to hay nhỏ ; tai tách được tiếng vang hay không là do thời gian chênh.")]),
  buoc("Kiểm tra")]),
]


def kiem_so():
    F = Fr
    # D1
    d1 = V_KK * F(45, 10); assert d1 == 1530
    d2 = V_KK * 2; assert d2 == 680 and d1 - d2 == 850 and d2 < d1
    tn = d1 / V_NUOC; assert tn == F(102, 100)
    assert abs(V_NUOC / V_KK - 4.4118) < 1e-3 and abs(4.5 / 1.02 - 4.4118) < 1e-3
    # cách sai cho số khác đáp án
    assert d1 / 2 != d1 and V_KK * (4.5 - 2) == 850 != d2 and d2 / 2 != d2 and 4.5 * V_NUOC / V_KK != tn
    # D2 — đồ thị: A có đỉnh tại 1 và 5 ms ; B có 4 dao động trong 10 ms
    sA = lambda t: A_A * math.sin(2 * math.pi * t / T_A)
    assert abs(sA(1) - 3) < 1e-9 and abs(sA(5) - 3) < 1e-9 and abs(10 / T_B - 4) < 1e-12
    fA, fB = 1 / (T_A / 1000), 1 / (T_B / 1000); assert round(fA) == 250 and round(fB) == 400 and abs(T_A / T_B - fB / fA) < 1e-12
    assert A_A > A_B and fB > fA                                    # B cao hơn, A to hơn
    assert abs(1 / ((T_B / 2) / 1000) - 800) < 1e-9 and 1 / T_B == 0.4   # cách sai (nửa chu kì, để ms)
    fC = F(1500, 120); fD = F(45000) / F(15, 10)
    assert fC == F(25, 2) and fD == 30000 and fC < 20 and fD > 20000 and all(20 <= f <= 20000 for f in (fA, fB))
    assert F(1500, 2) == 750 != fC and F(120, 1500) != fC and 45000 * 1.5 != fD
    # D3
    s = V_NUOC * F(24, 100); assert s == 360 and s / 2 == 180 and V_KK * F(24, 100) / 2 != 180
    dmin = F(V_KK, 2 * 15); assert abs(float(dmin) - 11.333) < 1e-3 and F(V_KK, 15) != dmin
    dt = F(16, V_KK); assert abs(float(dt) - 0.04706) < 1e-4 and dt < F(1, 15) and abs(1 / 15 - 0.0667) < 1e-4 and 8 < dmin
    assert abs(float(F(8, V_KK)) - 0.047) > 0.002      # cách sai d/v cho số khác (≈0,024 s)
    # hình D1: thời gian mô phỏng đúng thực ; hình D3: chậm 2 lần
    assert abs(2.4 / 0.24 - 10) < 1e-9
    print("kiểm số liệu D1–D3: đạt")
