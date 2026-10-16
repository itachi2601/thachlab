"""Bài tập mẫu CĐ15 "Âm thanh" (lesson 150) — Dạng 4–6 (phần khó). Module được build-hinh-150.py import.
Dàn ý: content/hsg9/cd15-am-thanh/nguon.md mục "Bài tập mẫu". Dạng sau dùng lại cách làm dạng trước:
  D4 hai tiếng qua hai môi trường (dùng s = v·t của D1, hai lần, rồi trừ thời gian)
  D5 nguồn chuyển động + tiếng vang (dùng d = v·t/2 của D3, nhưng xe đi thêm)
  D6 bước sóng khi đổi môi trường (λ = v/f, f do nguồn giữ nguyên) + tiếng vang trong nước.
Xuất DANG, BUILD, ANALYSIS, SOLS, STEPS (3 phần tử mỗi list) và kiem_so()."""
import math, os, re, sys
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *  # noqa: F401,F403  (fig, seg, lbl, dot, poly, chevron, arrow, sol, M, P, A, buoc …)

TOPIC = "Bước sóng, chu kì, tần số, tốc độ truyền sóng"
NOTE = "Hình minh hoạ, không đúng tỉ lệ."
GREY = "#94a3b8"
WAT = "#38bdf8"

# ═════════════ SỐ LIỆU (mọi đáp số tính ở đây, kiem_so() kiểm lại) ═════════════
# D4
VKK, VTHEP, DT4 = F(340), F(6120), F("0.85")
L4 = DT4 / (1 / VKK - 1 / VTHEP)                       # 306 m
LG, DTG = F(952), F("2.6")
TKK_G = LG / VKK                                       # 2,8 s
TG = TKK_G - DTG                                       # 0,2 s
VG = LG / TG                                           # 4760 m/s
# D5
D5, T5 = F(875), F(5)                                 # cho: khoảng cách lúc bóp còi, thời gian tới lúc nghe vang
SAM = VKK * T5                                         # 1700 m
SXE = 2 * D5 - SAM                                     # 50 m
VXE = SXE / T5                                         # 10 m/s
VXE_KMH = VXE * F(36, 10)                              # 36 km/h
D5B = D5 - SXE                                         # 825 m
T5B = 2 * D5B / (VKK + VXE)                            # 33/7 ≈ 4,71 s
# D6
F6, VN, T6 = F(500), F(1500), F("0.04")
LKK = VKK / F6                                         # 0,68 m
LN = VN / F6                                           # 3 m
H6 = VN * T6 / 2                                       # 30 m
N6 = H6 / LN                                           # 10


def rich(s, size=13):
    """Nhãn SVG có chỉ số dưới: 'v_{kk}' → tspan dy (chỉ số Unicode hiện như dấu phẩy ở một số máy)."""
    ms = list(re.finditer(r"_\{([^}]+)\}", s))
    if not ms:
        return s
    out = s[:ms[0].start()]
    for k, m in enumerate(ms):
        out += f'<tspan dy="4" font-size="{size - 3}">{m.group(1)}</tspan>'
        nxt = ms[k + 1].start() if k + 1 < len(ms) else len(s)
        if s[m.end():nxt]:
            out += f'<tspan dy="-4">{s[m.end():nxt]}</tspan>'
    return out

def txt(x, y, s, c="currentColor", size=13, anchor="start", weight="700", extra=""):
    t = lbl(x, y, rich(s, size), c, size, anchor, weight)
    return t.replace("<text ", f"<text {extra} ", 1) if extra else t

def show_at(t, dur):
    """Hiện (opacity 0 → 1) đúng lúc t trong mô phỏng dài dur giây — chạy một lần khi bấm."""
    k = max(0.001, min(0.999, t / dur))
    return (f'<animate attributeName="opacity" values="0;1" keyTimes="0;{k:.4f}" calcMode="discrete" dur="{dur:.2f}s" '
            f'begin="indefinite" fill="freeze"/>')

def anim_kt(attr, vals, kts, dur):
    return (f'<animate attributeName="{attr}" values="{";".join(f"{v:.1f}" for v in vals)}" '
            f'keyTimes="{";".join(f"{k:.4f}" for k in kts)}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>')

def rect(x, y, w, h, c="currentColor", sw=2, fill="none", op=1, rx=0):
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" fill-opacity="{op}" '
            f'stroke="{c}" stroke-width="{sw}"/>')

def hammer(x, y):
    return seg(x, y, x - 16, y - 22, "currentColor", 3) + rect(x - 26, y - 32, 20, 10, "currentColor", 2.4, "none", 1, 2)

def ear(x, y):
    return (f'<path d="M{x - 2},{y - 12} C{x + 12},{y - 14} {x + 14},{y + 6} {x + 2},{y + 12}" fill="none" stroke="currentColor" stroke-width="2.4"/>'
            + f'<path d="M{x + 2},{y - 5} C{x + 7},{y - 4} {x + 7},{y + 3} {x + 2},{y + 4}" fill="none" stroke="currentColor" stroke-width="1.8"/>')

def car(x, y):
    """Ô tô nhìn nghiêng, đầu xe (mũi) tại x, bánh chạm đường tại y."""
    return (rect(x - 40, y - 20, 40, 13, "currentColor", 2.2, "none", 1, 3)
            + f'<path d="M{x - 33},{y - 20} L{x - 27},{y - 30} L{x - 12},{y - 30} L{x - 6},{y - 20}" fill="none" stroke="currentColor" stroke-width="2"/>'
            + f'<circle cx="{x - 31}" cy="{y - 4}" r="4" fill="none" stroke="currentColor" stroke-width="2"/>'
            + f'<circle cx="{x - 9}" cy="{y - 4}" r="4" fill="none" stroke="currentColor" stroke-width="2"/>')

def wall(x, y0, y1):
    b = rect(x, y0, 14, y1 - y0, "currentColor", 2.2)
    for yy in range(int(y0) + 8, int(y1), 12):
        b += seg(x, yy + 8, x + 14, yy, "currentColor", 1.2, "", .7)
    return b

def dimline(x1, x2, y, label, c=ORG, ly=None, anchor="middle"):
    """Kích thước ngang hai đầu V."""
    return (seg(x1, y, x2, y, c, 1.6) + chevron(x1, y, -1, 0, c, 1.6, 8) + chevron(x2, y, 1, 0, c, 1.6, 8)
            + seg(x1, y - 6, x1, y + 6, c, 1.2) + seg(x2, y - 6, x2, y + 6, c, 1.2)
            + txt((x1 + x2) / 2 if anchor == "middle" else x1, (ly if ly is not None else y - 7), label, c, 13, anchor))


# ═════════════ HÌNH ═════════════
# ───────────── Dạng 4 · ray thép, hai tiếng ─────────────
def d4(kk):
    X0, X1 = 52, 372
    b = ""
    if kk == 0:
        TA = 5.4                                        # thời gian mô phỏng của âm trong không khí
        TS = TA * float(VKK / VTHEP)                    # đúng tỉ lệ thời gian thật giữa hai đường (1/18)
        b += txt(16, 22, "Gõ búa ở một đầu, áp tai ở đầu kia", "currentColor", 13)
        b += hammer(X0, 104) + ear(X1 + 8, 112)
        b += seg(X0, 62, X1, 62, ORG, 1.6, "6 5", .8) + txt(X0 + 30, 82, "đường âm trong không khí", ORG, 12, "start", "600")
        b += rect(X0, 108, X1 - X0, 10, BLUE, 2.2, BLUE, .18) + txt(X0 + 6, 138, "đường ray thép", BLUE, 12, "start", "600")
        b += (f'<circle cx="{X0}" cy="113" r="6" fill="{BLUE}" stroke="currentColor" stroke-width="1.4">'
              f'{anim_kt("cx", [X0, X1, X1], [0, TS / TA, 1], TA)}</circle>')
        b += (f'<circle cx="{X0}" cy="62" r="6" fill="{ORG}" stroke="currentColor" stroke-width="1.4">'
              f'{anim_kt("cx", [X0, X1], [0, 1], TA)}</circle>')
        b += txt(X1 - 4, 92, "tiếng 1", BLUE, 13, "end", "700", 'opacity="0"').replace("</text>", show_at(TS, TA) + "</text>", 1)
        b += txt(X1 - 4, 40, "tiếng 2", ORG, 13, "end", "700", 'opacity="0"').replace("</text>", show_at(TA * 0.995, TA) + "</text>", 1)
        b += dimline(X0, X1, 166, "L = ?", "currentColor", 186)
        return fig("c15-4-0", "0 0 420 196", "Xung âm chạy song song trong đường ray thép và trong không khí từ chỗ gõ búa tới tai",
                   b, "Mô phỏng: hai xung âm xuất phát cùng lúc từ chỗ gõ; xung trong thép (xanh) và trong không khí (cam). "
                      "Chạy chậm, giữ đúng tỉ lệ thời gian giữa hai đường. Không ghi chiều dài ray.")
    # hình dữ kiện: trục thời gian ở tai người nghe
    OY = 96
    b += txt(16, 22, "Thời điểm hai tiếng tới tai (gõ lúc t = 0)", "currentColor", 13)
    b += seg(40, OY, 396, OY, "currentColor", 1.8) + chevron(396, OY, 1, 0, "currentColor", 1.8, 9) + txt(398, OY + 22, "t", "currentColor", 13, "end")
    xs, xa = 92, 330
    b += seg(40, OY - 6, 40, OY + 6, "currentColor", 1.6) + txt(40, OY - 12, "0", "currentColor", 12, "middle", "400")
    b += seg(xs, OY - 10, xs, OY + 10, "currentColor", 2.4) + txt(xs, OY + 26, "tiếng thứ nhất", "currentColor", 12, "middle", "600")
    b += seg(xa, OY - 10, xa, OY + 10, "currentColor", 2.4) + txt(xa, OY + 26, "tiếng thứ hai", "currentColor", 12, "middle", "600")
    b += dimline(xs, xa, OY - 30, "Δt = 0,85 s", RED)
    b += txt(16, 160, "v_{thép} = 6120 m/s ; v_{kk} = 340 m/s ; L = ?", "currentColor", 12, "start", "600")
    return fig("c15-4-2", "0 0 420 176", "Trục thời gian: hai tiếng gõ tới tai cách nhau 0,85 giây",
               b, "Dữ kiện: hai vạch là hai lúc tiếng gõ tới tai ; khoảng cách giữa hai vạch là Δt. " + NOTE)


# ───────────── Dạng 5 · ô tô chạy về vách núi, bóp còi ─────────────
def d5(kk):
    b = ""
    RY = 160                                             # mặt đường
    XW = 386                                             # mặt vách núi
    if kk == 0:
        XA, XB, TT, K1 = 52, 112, 5.0, 0.56              # KHÔNG đúng tỉ lệ: chỉ giữ thứ tự sự kiện
        b += txt(16, 22, "Xe chạy về phía vách núi, bóp còi lúc t = 0", "currentColor", 13)
        b += wall(XW, 40, RY) + seg(10, RY, 236, RY, "currentColor", 2) + seg(250, RY, XW, RY, "currentColor", 2)
        b += seg(230, RY + 8, 240, RY - 8, "currentColor", 1.8) + seg(244, RY + 8, 254, RY - 8, "currentColor", 1.8)
        b += (f'<g>{car(XA, RY)}<animateTransform attributeName="transform" type="translate" from="0 0" to="{XB - XA} 0" '
              f'dur="{TT:.2f}s" begin="indefinite" fill="freeze"/></g>')
        b += (f'<circle cx="{XA}" cy="118" r="6" fill="{ORG}" stroke="currentColor" stroke-width="1.4">'
              f'{anim_kt("cx", [XA, XW, XB], [0, K1, 1], TT)}</circle>')
        b += txt(16, 112, "còi", ORG, 12, "start", "600")
        b += txt(XW - 8, 96, "phản xạ", ORG, 12, "end", "600", 'opacity="0"').replace("</text>", show_at(K1 * TT, TT) + "</text>", 1)
        b += txt(16, 196, "nghe tiếng vang", RED, 13, "start", "700", 'opacity="0"').replace("</text>", show_at(TT * 0.995, TT) + "</text>", 1)
        return fig("c15-5-0", "0 0 420 206", "Ô tô chạy về phía vách núi; xung âm từ còi đi tới vách, phản xạ và gặp lại xe",
                   b, "Mô phỏng: xung âm (cam) đi tới vách rồi quay về gặp xe đang tiến lại gần. Chỉ giữ thứ tự sự kiện ; "
                      "khoảng cách và tốc độ không vẽ theo tỉ lệ (dấu ngắt trên đường).")
    XA, XB = 70, 170                                      # không đúng tỉ lệ
    b += wall(XW, 40, RY) + seg(10, RY, XW, RY, "currentColor", 2)
    b += car(XA, RY) + txt(XA - 20, RY + 18, "A", "currentColor", 13, "middle")
    b += f'<g opacity=".55">{car(XB, RY)}</g>' + txt(XB - 20, RY + 18, "B", "currentColor", 13, "middle")
    b += arrow("", "o", XA, 74, XW - 4, 74, 2.2) + arrow("", "o", XW - 4, 96, XB, 96, 2.2, "6 4")
    b += txt(XA, 64, "âm đi tới vách", ORG, 12, "start", "600") + txt(XB + 6, 116, "âm phản xạ về", ORG, 12, "start", "600")
    b += dimline(XA, XB, 200, "s_{xe} = ?", GRN)
    b += dimline(XA, XW, 236, "d = 875 m (lúc bóp còi)", BLUE, 254)
    b += dimline(XB, XW, 272, "d' = ? (lúc nghe)", RED, 290)
    b += txt(16, 22, "Từ A tới B: t = 5 s ; v_{âm} = 340 m/s ; v_{xe} = ?", "currentColor", 13)
    return fig("c15-5-2", "0 0 420 300", "Xe bóp còi tại A, nghe tiếng vang tại B; âm đi từ A tới vách rồi về B",
               b, "Dữ kiện: trong cùng 5 s, âm đi A → vách → B còn xe đi A → B. " + NOTE)


# ───────────── Dạng 6 · âm từ không khí vào nước ─────────────
LA_PX = 13.0
def wave_pts(x0, xi, x1, yc, amp):
    lw = LA_PX * 2.6                                   # dài hơn nhưng KHÔNG đúng tỉ lệ v_n/v_kk
    pts, x = [], x0
    while x <= x1 + .01:
        ph = (x - x0) / LA_PX if x <= xi else (xi - x0) / LA_PX + (x - xi) / lw
        pts.append((x, yc - amp * math.sin(2 * math.pi * ph)))
        x += 1.0
    return pts, lw

def d6(kk):
    b = ""
    X0, XI, X1, YC = 22, 172, 404, 104
    if kk == 0:
        pts, lw = wave_pts(X0, XI, X1, YC, 18)
        va = 50.0                                         # px/s trong không khí (chạy chậm)
        ta = (XI - X0) / va
        tw = (X1 - XI) / (va * 2.6)                       # cùng tần số: nhanh hơn đúng bằng tỉ lệ bước sóng đã vẽ
        T = ta + tw
        b += rect(XI, 40, X1 - XI + 6, 120, WAT, 0, WAT, .14)
        b += seg(XI, 36, XI, 164, "currentColor", 1.6, "5 4", .8)
        b += txt(X0, 30, "không khí", "currentColor", 13) + txt(X1, 30, "nước", WAT, 13, "end")
        b += (f'<clipPath id="c15-6-clip"><rect x="{X0 - 2}" y="40" width="{X1 - X0 + 4}" height="130">'
              f'{anim_kt("width", [0, XI - X0 + 2, X1 - X0 + 4], [0, ta / T, 1], T)}</rect></clipPath>')
        b += f'<g clip-path="url(#c15-6-clip)">{poly(pts, GRN, 2.4)}</g>'
        b += txt(16, 186, "Cùng một nguồn phát, sóng lan từ trái sang phải", "currentColor", 12, "start", "400")
        return fig("c15-6-0", "0 0 420 196", "Sóng âm lan từ không khí vào nước, khoảng cách giữa hai đỉnh sóng dài ra khi sang nước",
                   b, "Mô phỏng: sóng lan dần từ không khí sang nước (chạy chậm rất nhiều lần). Sang nước sóng lan nhanh hơn, "
                      "khoảng cách giữa hai đỉnh dài ra ; không vẽ theo tỉ lệ.")
    # hình dữ kiện: mặt cắt hồ
    YS, YB = 52, 176
    b += rect(30, YS, 360, YB - YS, WAT, 0, WAT, .14) + seg(20, YS, 400, YS, WAT, 2.2) + seg(30, YB, 390, YB, "currentColor", 2.4)
    for xx in range(40, 390, 18):
        b += seg(xx, YB + 8, xx + 8, YB, "currentColor", 1.2, "", .7)
    b += rect(100, YS - 20, 26, 18, "currentColor", 2.2, "none", 1, 3) + txt(132, YS - 8, "loa: f = 500 Hz", "currentColor", 13)
    b += arrow("", "b", 106, YS + 6, 106, YB - 6, 2.2) + arrow("", "b", 122, YB - 6, 122, YS + 6, 2.2, "6 4")
    b += txt(136, 100, "đi xuống rồi về mặt nước:", BLUE, 12, "start", "600") + txt(136, 118, "t = 0,04 s", BLUE, 13)
    b += txt(136, 146, "v_{n} = 1500 m/s", BLUE, 12, "start", "600")
    b += seg(340, YS, 340, YB, ORG, 1.6) + chevron(340, YS, 0, -1, ORG, 1.6, 8) + chevron(340, YB, 0, 1, ORG, 1.6, 8)
    b += txt(348, 118, "h = ?", ORG, 13)
    b += txt(16, 22, "Trên mặt nước: không khí, v_{kk} = 340 m/s", "currentColor", 12, "start", "600")
    return fig("c15-6-2", "0 0 420 196", "Mặt cắt hồ: loa trên mặt nước, âm đi thẳng đứng xuống đáy rồi phản xạ về",
               b, "Dữ kiện: 0,04 s là thời gian âm đi xuống đáy rồi về tới mặt nước ; tần số do loa quyết định. " + NOTE)


BUILD = [d4, d5, d6]

# ═════════════ ĐỀ ═════════════
DANG = [
dict(label="Dạng 4 · Nâng cao · Hai tiếng qua hai môi trường: tìm chiều dài hoặc tốc độ âm",
     topic=TOPIC,
     problem_html=r"""<p>Một bạn áp tai vào một đầu của một đường ray thép thẳng. Ở đầu kia, cách đó một khoảng $L$, một bạn khác gõ mạnh búa vào thanh ray. Bạn áp tai nghe thấy hai tiếng gõ, tiếng sau cách tiếng trước $\Delta t=0{,}85\ \text{s}$. Tốc độ âm trong không khí là $340\ \text{m/s}$, trong thép là $6120\ \text{m/s}$. Coi âm đi thẳng dọc theo ray trong cả hai môi trường.</p><ol type="a"><li>Vì sao nghe được hai tiếng? Tiếng nào tới trước?</li><li>Tính $L$.</li><li>Làm lại thí nghiệm với một ống gang thẳng dài $952\ \text{m}$ thì hai tiếng cách nhau $2{,}6\ \text{s}$. Tính tốc độ âm trong gang.</li></ol>"""),
dict(label="Dạng 5 · Vận dụng cao · Nguồn âm chuyển động và tiếng vang: tìm tốc độ xe từ tiếng còi",
     topic=TOPIC,
     problem_html=r"""<p>Một ô tô chạy thẳng đều trên một đoạn đường thẳng, hướng thẳng về phía một vách núi. Khi xe cách vách núi $875\ \text{m}$, người lái bóp một hồi còi ngắn. Sau $5\ \text{s}$ kể từ lúc bóp còi, người lái nghe thấy tiếng vang từ vách núi. Tốc độ âm trong không khí là $340\ \text{m/s}$, coi như không có gió.</p><ol type="a"><li>Tính tốc độ của xe theo $\text{km/h}$.</li><li>Tính khoảng cách từ xe đến vách núi lúc người lái nghe thấy tiếng vang.</li><li>Ngay lúc nghe tiếng vang, người lái bóp còi lần thứ hai, xe vẫn chạy như cũ. Sau bao lâu kể từ lần bóp còi thứ hai thì người lái nghe tiếng vang lần thứ hai?</li></ol>"""),
dict(label="Dạng 6 · Vận dụng cao · Mở rộng HSG: Bước sóng khi âm đổi môi trường, kết hợp tiếng vang",
     topic=TOPIC,
     problem_html=r"""<p>Một chiếc loa đặt sát mặt nước của một hồ phát ra âm có tần số $500\ \text{Hz}$. Tốc độ âm trong không khí là $340\ \text{m/s}$, trong nước là $1500\ \text{m/s}$.</p><ol type="a"><li>Tính bước sóng của âm này trong không khí.</li><li>Âm truyền vào nước. Trong nước, tần số và bước sóng của âm bằng bao nhiêu?</li><li>Trong nước, âm đi thẳng đứng xuống đáy hồ, phản xạ rồi trở lại mặt nước sau $0{,}04\ \text{s}$ kể từ lúc vào nước. Tính độ sâu của hồ. Quãng từ mặt nước xuống đáy dài bằng bao nhiêu bước sóng của âm trong nước?</li></ol>"""),
]

# ═════════════ BẢNG PHÂN TÍCH ĐỀ (cột 1 nguyên văn đề ; cột 2 chỉ dữ liệu có trong đề ; cột 3 kiến thức nền + câu hỏi gợi) ═════════════
ANALYSIS = [
 # Dạng 4
 [(r'"gõ mạnh búa vào thanh ray", "nghe thấy hai tiếng gõ"', r"hai tiếng gõ", r"Âm truyền được trong chất rắn và chất khí. Hai tiếng đi theo những đường nào ? Đường nào nhanh hơn ?"),
  (r'"Coi âm đi thẳng dọc theo ray trong cả hai môi trường"', r"âm đi thẳng, dọc ray", r"⚠ điều kiện để dùng $t=\dfrac{s}{v}$ cho từng đường. Hai đường dài bao nhiêu ?"),
  (r'"Tốc độ âm trong không khí là $340\ \text{m/s}$, trong thép là $6120\ \text{m/s}$"', r"$v_{kk}=340\ \text{m/s}$ ; $v_{thép}=6120\ \text{m/s}$", r"Thời gian truyền mỗi đường : $t=\dfrac{s}{v}$"),
  (r'"tiếng sau cách tiếng trước $\Delta t=0{,}85\ \text{s}$"', r"$\Delta t=0{,}85\ \text{s}$", r"$\Delta t$ là hiệu hay tổng của hai thời gian truyền ?"),
  (r'"Tính $L$."', r"$L=?$", r"Viết hai thời gian truyền theo $L$, rồi nối chúng với $\Delta t$ thế nào ?"),
  (r'"một ống gang thẳng dài $952\ \text{m}$ thì hai tiếng cách nhau $2{,}6\ \text{s}$"', r"$L'=952\ \text{m}$ ; $\Delta t'=2{,}6\ \text{s}$ ; $v_{gang}=?$", r"Thời gian của đường nào tính được ngay ? Tiếng qua gang tới sớm hay muộn hơn ? $v=\dfrac{s}{t}$")],
 # Dạng 5
 [(r'"chạy thẳng đều trên một đoạn đường thẳng, hướng thẳng về phía một vách núi"', r"xe chạy thẳng đều về phía vách", r"⚠ xe, âm đi và âm về trên cùng một đường thẳng. Trong lúc âm đi và về, xe làm gì ?"),
  (r'"Khi xe cách vách núi $875\ \text{m}$, người lái bóp một hồi còi ngắn"', r"$d=875\ \text{m}$ (lúc bóp còi)", r"Khoảng cách đo ở thời điểm nào ?"),
  (r'"Sau $5\ \text{s}$ kể từ lúc bóp còi, người lái nghe thấy tiếng vang"', r"$t=5\ \text{s}$", r"Trong $t$, âm đi những đoạn nào, xe đi đoạn nào ? $s=vt$"),
  (r'"Tốc độ âm trong không khí là $340\ \text{m/s}$, coi như không có gió"', r"$v_{âm}=340\ \text{m/s}$", r"⚠ tốc độ âm có phụ thuộc chuyển động của xe không ?"),
  (r'"Tính tốc độ của xe theo $\text{km/h}$"', r"$v_{xe}=?$", r"Trên hình, quãng âm, quãng xe và $d$ liên hệ thế nào ? $1\ \text{m/s}=3{,}6\ \text{km/h}$"),
  (r'"khoảng cách từ xe đến vách núi lúc người lái nghe thấy tiếng vang"', r"$d'=?$", r"So với lúc bóp còi, khoảng cách tăng hay giảm, bao nhiêu ?"),
  (r'"Sau bao lâu kể từ lần bóp còi thứ hai"', r"$t_2=?$", r"Giống câu a nhưng đại lượng nào đã biết, đại lượng nào là ẩn ?")],
 # Dạng 6
 [(r'"phát ra âm có tần số $500\ \text{Hz}$"', r"$f=500\ \text{Hz}$", r"Tần số do cái gì quyết định : nguồn hay môi trường ?"),
  (r'"Tốc độ âm trong không khí là $340\ \text{m/s}$, trong nước là $1500\ \text{m/s}$"', r"$v_{kk}=340\ \text{m/s}$ ; $v_{n}=1500\ \text{m/s}$", r"Tốc độ do cái gì quyết định : nguồn hay môi trường ?"),
  (r'"Tính bước sóng của âm này trong không khí"', r"$\lambda_{kk}=?$", r"$\lambda=\dfrac{v}{f}=vT$"),
  (r'"Âm truyền vào nước. Trong nước, tần số và bước sóng"', r"$f_n=?$ ; $\lambda_n=?$", r"⚠ khi đổi môi trường, đại lượng nào giữ nguyên, đại lượng nào đổi ?"),
  (r'"phản xạ rồi trở lại mặt nước sau $0{,}04\ \text{s}$"', r"$t=0{,}04\ \text{s}$", r"Tiếng vang : $t$ gồm những đoạn nào ? ⚠ dùng tốc độ của môi trường nào ?"),
  (r'"dài bằng bao nhiêu bước sóng của âm trong nước"', r"$N=?$", r"Chia quãng đường cho bước sóng của môi trường nào ?")],
]

# ═════════════ LỜI GIẢI ═════════════
R4 = [r"<strong>Khái niệm:</strong> âm truyền trong chất rắn nhanh hơn trong chất khí.",
      r"<strong>Công thức:</strong> thời gian âm đi quãng $L$ với tốc độ $v$ : $t=\dfrac{L}{v}$.",
      r"<strong>Hai tiếng:</strong> $\Delta t=t_{chậm}-t_{nhanh}=\dfrac{L}{v_{kk}}-\dfrac{L}{v_{thép}}$.",
      r"<strong>Điều kiện:</strong> hai đường cùng dài $L$ ; tốc độ trong mỗi môi trường không đổi."]
R5 = [r"<strong>Khái niệm:</strong> tiếng vang là âm phản xạ từ vật cản quay về tai.",
      r"<strong>Công thức:</strong> $s=vt$ cho cả xe và âm, cùng thời gian $t$.",
      r"<strong>Hình học:</strong> âm đi tới vách rồi về gặp xe, xe đi thêm $s_{xe}$ : $s_{âm}+s_{xe}=2d$.",
      r"<strong>Điều kiện:</strong> chuyển động trên một đường thẳng ; không có gió ; $1\ \text{m/s}=3{,}6\ \text{km/h}$."]
R6 = [r"<strong>Khái niệm:</strong> bước sóng là quãng đường sóng truyền trong một chu kì.",
      r"<strong>Công thức:</strong> $\lambda=vT=\dfrac{v}{f}$.",
      r"<strong>Đổi môi trường:</strong> tần số do nguồn quyết định nên giữ nguyên ; tốc độ đổi nên bước sóng đổi.",
      r"<strong>Tiếng vang:</strong> $h=\dfrac{vt}{2}$ với $v$ của môi trường âm đang đi."]

SOLS = [
 sol(R4, [
  ("Tiếng tới trước", [P(r"Tiếng gõ truyền tới tai theo hai đường cùng dài $L$ : trong thép và trong không khí."),
     P(r"Âm trong thép nhanh hơn nên tới trước ; âm trong không khí tới sau."),
     A(r"T:Tiếng thứ nhất truyền qua thép, tiếng thứ hai truyền qua không khí.")]),
  ("Tìm $L$", [P(r"Hiệu hai thời gian truyền bằng $\Delta t$ :"), M(r"\Delta t=\dfrac{L}{v_{kk}}-\dfrac{L}{v_{thép}}\ \Rightarrow\ L=\dfrac{\Delta t}{\dfrac{1}{v_{kk}}-\dfrac{1}{v_{thép}}}"),
     M(r"L=\dfrac{0{,}85}{\dfrac{1}{340}-\dfrac{1}{6120}}=0{,}85\cdot360"), A(r"L=306\ \text{m}")]),
  ("Thời gian qua không khí", [P(r"Biết chiều dài ống $L'=952\ \text{m}$ :"), M(r"t_{kk}=\dfrac{L'}{v_{kk}}=\dfrac{952}{340}"), A(r"t_{kk}=2{,}8\ \text{s}")]),
  ("Thời gian qua gang", [P(r"Âm trong gang tới trước, sớm hơn đúng $\Delta t'$ :"), M(r"t_{gang}=t_{kk}-\Delta t'=2{,}8-2{,}6"), A(r"t_{gang}=0{,}2\ \text{s}")]),
  ("Tốc độ âm trong gang", [M(r"v_{gang}=\dfrac{L'}{t_{gang}}=\dfrac{952}{0{,}2}"), A(r"v_{gang}=4760\ \text{m/s}")]),
  ("Kiểm tra", [P(r"Câu b : $t_{kk}=\dfrac{306}{340}=0{,}9\ \text{s}$ ; $t_{thép}=\dfrac{306}{6120}=0{,}05\ \text{s}$ ; hiệu $0{,}85\ \text{s}$ ✓."),
     P(r"$v_{gang}=4760\ \text{m/s}$ lớn hơn nhiều $340\ \text{m/s}$ và cùng cỡ với thép : hợp lí với chất rắn ✓.")])],
  [r"a) Âm qua thép tới trước, âm qua không khí tới sau", r"b) $L=306\ \text{m}$", r"c) $v_{gang}=4760\ \text{m/s}$"],
  r"Nhận dạng: thấy <strong>nghe hai tiếng cách nhau Δt</strong> qua ray, ống → hai thời gian $L/v$ trừ nhau bằng $\Delta t$ ; biết $L$ thì tìm thời gian qua chất rắn rồi ra $v$."),
 sol(R5, [
  ("Quãng đường âm", [P(r"Từ lúc bóp còi tới lúc nghe tiếng vang, âm đi A → vách → gặp xe tại B :"), M(r"s_{âm}=v_{âm}t=340\cdot5"), A(r"s_{âm}=1700\ \text{m}")]),
  ("Quãng đường xe", [P(r"Âm đi $d$ tới vách rồi quay về $d-s_{xe}$, nên $s_{âm}+s_{xe}=2d$ :"), M(r"s_{xe}=2d-s_{âm}=2\cdot875-1700"), A(r"s_{xe}=50\ \text{m}")]),
  ("Tốc độ xe", [M(r"v_{xe}=\dfrac{s_{xe}}{t}=\dfrac{50}{5}=10\ \text{m/s}"), M(r"v_{xe}=10\cdot3{,}6"), A(r"v_{xe}=36\ \text{km/h}")]),
  ("Khoảng cách lúc nghe", [P(r"Xe đã tiến lại gần vách $s_{xe}$ :"), M(r"d'=d-s_{xe}=875-50"), A(r"d'=825\ \text{m}")]),
  ("Thời gian tới tiếng vang lần hai", [P(r"Giống câu a, nay biết khoảng cách $d'$ và tốc độ xe, ẩn là thời gian $t_2$ :"), M(r"v_{âm}t_2+v_{xe}t_2=2d'"),
     M(r"t_2=\dfrac{2d'}{v_{âm}+v_{xe}}=\dfrac{2\cdot825}{340+10}=\dfrac{33}{7}"), A(r"t_2\approx4{,}71\ \text{s}")]),
  ("Kiểm tra", [P(r"Câu a : âm đi tới vách $875\ \text{m}$, quay về $875-50=825\ \text{m}$ ; tổng $1700\ \text{m}=340\cdot5$ ✓."),
     P(r"$t_2\lt5\ \text{s}$ vì lần hai xe gần vách hơn ✓.")])],
  [r"a) $v_{xe}=10\ \text{m/s}=36\ \text{km/h}$", r"b) $d'=825\ \text{m}$", r"c) $t_2=\dfrac{33}{7}\ \text{s}\approx4{,}71\ \text{s}$"],
  r"Nhận dạng: thấy <strong>xe chạy về phía vách</strong> và <strong>bóp còi, sau t nghe tiếng vang</strong> → vẽ đường đi của âm và xe trong cùng thời gian, $s_{âm}+s_{xe}=2d$."),
 sol(R6, [
  ("Bước sóng trong không khí", [M(r"\lambda_{kk}=\dfrac{v_{kk}}{f}=\dfrac{340}{500}"), A(r"\lambda_{kk}=0{,}68\ \text{m}")]),
  ("Tần số trong nước", [P(r"Tần số là số dao động trong một giây, do loa quyết định ; nước dao động theo đúng nhịp của sóng tới."),
     A(r"T:Tần số giữ nguyên: $f_n=f=500\ \text{Hz}$.")]),
  ("Bước sóng trong nước", [P(r"Tốc độ đổi, tần số giữ nguyên :"), M(r"\lambda_n=\dfrac{v_n}{f}=\dfrac{1500}{500}"), A(r"\lambda_n=3\ \text{m}")]),
  ("Độ sâu của hồ", [P(r"$0{,}04\ \text{s}$ là thời gian cả đi lẫn về trong nước :"), M(r"h=\dfrac{v_n t}{2}=\dfrac{1500\cdot0{,}04}{2}"), A(r"h=30\ \text{m}")]),
  ("Số bước sóng trên quãng $h$", [M(r"N=\dfrac{h}{\lambda_n}=\dfrac{30}{3}"), A(r"N=10")]),
  ("Kiểm tra", [P(r"$\dfrac{\lambda_n}{\lambda_{kk}}=\dfrac{3}{0{,}68}\approx4{,}41=\dfrac{v_n}{v_{kk}}$ ✓ : cùng tần số thì bước sóng tỉ lệ với tốc độ."),
     P(r"Đơn vị : $\dfrac{\text{m/s}}{\text{Hz}}=\dfrac{\text{m/s}}{1/\text{s}}=\text{m}$ ✓.")])],
  [r"a) $\lambda_{kk}=0{,}68\ \text{m}$", r"b) $f_n=500\ \text{Hz}$ ; $\lambda_n=3\ \text{m}$", r"c) $h=30\ \text{m}$ ; quãng đó dài bằng $10$ bước sóng"],
  r"Nhận dạng: thấy <strong>âm đi sang môi trường khác</strong> → tần số giữ nguyên, tính lại $\lambda=v/f$ với $v$ mới ; tiếng vang trong môi trường nào thì dùng $v$ của môi trường đó."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC ═════════════
STEPS = [
 # ── Dạng 4 ──
 dict(nhan_dang=r"Thấy <b>nghe hai tiếng</b> qua <b>ray, ống kim loại</b> → nghĩ tới <b>hai thời gian $L/v$ trừ nhau bằng $\Delta t$</b>",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Tiếng tới trước", "Tiếng nào tới tai trước?",
       lua_chon=[(r"Tiếng truyền qua thép, vì âm trong chất rắn nhanh hơn", True),
                 (r"Tiếng truyền qua không khí, vì không khí không cản âm", r"Tốc độ âm trong không khí ($340\ \text{m/s}$) nhỏ hơn nhiều trong thép ; cùng quãng thì đi lâu hơn."),
                 (r"Hai tiếng tới cùng lúc, tiếng sau là tiếng vang", r"Đề không có vật phản xạ ; hai tiếng là hai đường truyền khác tốc độ.")],
       loi=r"Nghĩ chất khí truyền âm tốt nhất vì hằng ngày nghe qua không khí ; thực ra $v_{rắn}\gt v_{lỏng}\gt v_{khí}$."),
  buoc("Tìm $L$", "Chiều dài $L$ bằng bao nhiêu mét?", float(L4), "m", 1,
       loi=r"Lấy $\Delta t$ làm thời gian âm đi trong không khí, hoặc trừ hai tốc độ thay vì trừ hai thời gian.",
       ke=[(r"$\Delta t=\dfrac{L}{v_{kk}}-\dfrac{L}{v_{thép}}$ rồi giải ra $L$", True),
           (r"$L=v_{kk}\cdot\Delta t$", r"$\Delta t$ là khoảng cách giữa hai tiếng, không phải thời gian âm đi hết ray trong không khí."),
           (r"$L=(v_{thép}-v_{kk})\cdot\Delta t$", r"Hiệu thời gian không tính bằng hiệu tốc độ nhân $\Delta t$ ; phải trừ hai thời gian $\dfrac{L}{v}$.")]),
  buoc("Thời gian qua không khí", "Âm truyền trong không khí dọc ống gang mất bao nhiêu giây?", float(TKK_G), "s", 0.01,
       loi=r"Lấy luôn $\Delta t'$ làm thời gian truyền trong không khí.",
       ke=[(r"$t_{kk}=\dfrac{L'}{v_{kk}}$ vì đã biết chiều dài ống", True),
           (r"$t_{kk}=\Delta t'$", r"$\Delta t'$ là hiệu hai thời gian ; âm qua gang cũng mất một khoảng thời gian, không bằng $0$."),
           (r"$t=\dfrac{L'}{v_{thép}}$", r"Ống bằng gang, không phải thép ; tốc độ âm trong gang đang là ẩn.")]),
  buoc("Thời gian qua gang", "Âm truyền trong gang mất bao nhiêu giây?", float(TG), "s", 0.005,
       loi=r"Cộng $\Delta t'$ vào thay vì trừ, quên rằng âm trong chất rắn tới trước.",
       ke=[(r"$t_{gang}=t_{kk}-\Delta t'$", True),
           (r"$t_{gang}=t_{kk}+\Delta t'$", r"Âm trong gang nhanh hơn nên tới sớm hơn ; thời gian của nó ngắn hơn, phải trừ."),
           (r"$t_{gang}=\Delta t'$", r"$\Delta t'$ là khoảng cách giữa hai tiếng, không phải thời gian âm đi trong gang.")]),
  buoc("Tốc độ âm trong gang", "Tốc độ âm trong gang bằng bao nhiêu m/s?", float(VG), "m/s", 10,
       loi=r"Chia chiều dài ống cho $\Delta t'$ ; kết quả chỉ cỡ tốc độ âm trong không khí là dấu hiệu sai.",
       ke=[(r"$v_{gang}=\dfrac{L'}{t_{gang}}$", True),
           (r"$v_{gang}=\dfrac{L'}{\Delta t'}$", r"Chia cho khoảng cách giữa hai tiếng sẽ ra tốc độ chỉ cỡ tốc độ âm trong không khí — quá nhỏ với chất rắn."),
           (r"$v_{gang}=\dfrac{L'}{t_{kk}}$", r"Đó chính là tốc độ âm trong không khí, không phải trong gang.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 5 ──
 dict(nhan_dang=r"Thấy <b>xe chạy về phía vách</b>, <b>bóp còi rồi nghe tiếng vang</b> → <b>vẽ đường đi của âm và xe trong cùng thời gian</b>",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Quãng đường âm", "Từ lúc bóp còi tới lúc nghe tiếng vang, âm đi được bao nhiêu mét?", float(SAM), "m", 1,
       loi=r"Viết $s_{âm}=\dfrac{v_{âm}t}{2}$ : sai, $s_{âm}=v_{âm}t$, không có $\tfrac12$ ; chia 2 chỉ dùng khi tìm $d$."),
  buoc("Quãng đường xe", "Trong thời gian đó xe đi được bao nhiêu mét?", float(SXE), "m", 0.5,
       loi=r"Coi âm đi đúng $2d$ như khi nguồn đứng yên, nên không còn chỗ cho quãng xe đi ; hoặc trừ ngược ra số âm.",
       ke=[(r"Vẽ đường đi : $s_{âm}+s_{xe}=2d$, suy ra $s_{xe}$", True),
           (r"$s_{xe}=s_{âm}-2d$", r"Âm phải đi ít hơn $2d$ vì xe tiến lại gặp âm phản xạ ; trừ ngược sẽ ra số âm."),
           (r"$s_{xe}=d-\dfrac{s_{âm}}{2}$", r"Tổng quãng âm và quãng xe bằng $2d$, không phải $d$ ; tính như vậy chỉ ra một nửa quãng xe đi.")]),
  buoc("Tốc độ xe", "Tốc độ của xe bằng bao nhiêu km/h?", float(VXE_KMH), "km/h", 0.2,
       loi=r"Dừng ở đơn vị m/s mà đề hỏi km/h, hoặc chia quãng xe cho nửa thời gian.",
       ke=[(r"$v_{xe}=\dfrac{s_{xe}}{t}$ rồi đổi sang km/h", True),
           (r"$v_{xe}=\dfrac{s_{xe}}{t/2}$", r"Xe chạy suốt thời gian $t$ (cả lúc âm đi lẫn lúc âm về), không phải nửa thời gian."),
           (r"$v_{xe}=\dfrac{s_{xe}}{t}$ và giữ nguyên số đó làm km/h", r"$\dfrac{\text{m}}{\text{s}}$ không phải km/h ; $1\ \text{m/s}=3{,}6\ \text{km/h}$.")]),
  buoc("Khoảng cách lúc nghe", "Lúc nghe tiếng vang, xe cách vách bao nhiêu mét?", float(D5B), "m", 1,
       loi=r"Lấy luôn khoảng cách lúc bóp còi, quên xe đã tiến lại gần vách.",
       ke=[(r"$d'=d-s_{xe}$", True),
           (r"$d'=d$", r"Xe vẫn chạy trong lúc chờ tiếng vang nên đã gần vách hơn lúc bóp còi."),
           (r"$d'=d+s_{xe}$", r"Xe chạy về phía vách nên khoảng cách giảm, không tăng.")]),
  buoc("Thời gian tới tiếng vang lần hai", "Sau bao nhiêu giây kể từ lần bóp còi thứ hai thì nghe tiếng vang lần hai?", float(T5B), "s", 0.02,
       loi=r"Dùng $t_2=\dfrac{2d'}{v_{âm}}$ như xe đứng yên, hoặc trừ tốc độ xe thay vì cộng.",
       ke=[(r"$v_{âm}t_2+v_{xe}t_2=2d'$ rồi giải $t_2$", True),
           (r"$t_2=\dfrac{2d'}{v_{âm}}$", r"Lại coi xe đứng yên ; xe tiến tới gặp âm phản xạ nên nghe sớm hơn."),
           (r"$t_2=\dfrac{2d'}{v_{âm}-v_{xe}}$", r"Âm phản xạ và xe đi ngược chiều nhau, tiến lại gần nhau : quãng đường cộng lại nên tốc độ cộng, không trừ.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 6 ──
 dict(nhan_dang=r"Thấy <b>âm đi từ không khí vào nước</b> → xét đại lượng nào do <b>nguồn</b> quyết định, rồi dùng <b>$\lambda=v/f$</b>",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Bước sóng trong không khí", "Bước sóng của âm trong không khí bằng bao nhiêu mét?", float(LKK), "m", 0.005,
       loi=r"Viết $\lambda=v\cdot f$ hoặc $\lambda=\dfrac{f}{v}$ ; kiểm đơn vị : $\dfrac{\text{m/s}}{\text{Hz}}$ mới ra mét."),
  buoc("Tần số trong nước", "Khi âm vào nước, tần số thay đổi thế nào?",
       lua_chon=[(r"Giữ nguyên như tần số của loa", True),
                 (r"Tăng lên theo tốc độ, vì âm trong nước nhanh hơn", r"Tốc độ tăng nhưng nhịp dao động do loa áp đặt ; nước dao động theo đúng nhịp đó."),
                 (r"Giảm đi, vì nước cản dao động mạnh hơn không khí", r"Nước không làm chậm nhịp dao động ; loa dao động bao nhiêu lần mỗi giây thì nước dao động bấy nhiêu lần.")],
       loi=r"Nghĩ tần số đổi theo tốc độ, hoặc giữ bước sóng như trong không khí.",
       ke=[(r"Xét xem đại lượng nào do nguồn quyết định khi âm đổi môi trường", True),
           (r"Lấy $f_n=\dfrac{v_n}{\lambda_{kk}}$", r"Bước sóng trong không khí không dùng được cho nước ; mỗi môi trường có bước sóng riêng."),
           (r"Coi mọi đại lượng của sóng giữ nguyên khi vào nước", r"Tốc độ đã đổi (đề cho hai giá trị khác nhau) nên không thể mọi đại lượng đều giữ nguyên.")]),
  buoc("Bước sóng trong nước", "Bước sóng của âm trong nước bằng bao nhiêu mét?", float(LN), "m", 0.02,
       loi=r"Giữ nguyên bước sóng như trong không khí, hoặc cho bước sóng tỉ lệ nghịch với tốc độ.",
       ke=[(r"$\lambda_n=\dfrac{v_n}{f}$ với tần số vừa xét", True),
           (r"$\lambda_n=\lambda_{kk}$", r"Tốc độ đổi mà tần số giữ nguyên thì bước sóng phải đổi theo, vì $\lambda=\dfrac{v}{f}$."),
           (r"$\lambda_n=\lambda_{kk}\cdot\dfrac{v_{kk}}{v_n}$", r"Cùng tần số thì bước sóng tỉ lệ THUẬN với tốc độ, không tỉ lệ nghịch.")]),
  buoc("Độ sâu của hồ", "Độ sâu của hồ là bao nhiêu mét?", float(H6), "m", 0.2,
       loi=r"Quên chia 2, hoặc dùng tốc độ âm trong không khí cho đoạn đường trong nước.",
       ke=[(r"$h=\dfrac{v_n t}{2}$", True),
           (r"$h=v_n t$", r"$0{,}04\ \text{s}$ là thời gian cả đi xuống lẫn đi lên ; quãng xuống chỉ bằng một nửa."),
           (r"$h=\dfrac{v_{kk}t}{2}$", r"Âm đang đi trong nước nên dùng tốc độ trong nước.")]),
  buoc("Số bước sóng trên quãng $h$", "Quãng từ mặt nước xuống đáy dài bằng bao nhiêu bước sóng?", float(N6), "", 0.1,
       loi=r"Chia cho bước sóng trong không khí, hoặc tính cả quãng đi lẫn về.",
       ke=[(r"$N=\dfrac{h}{\lambda_n}$", True),
           (r"$N=\dfrac{h}{\lambda_{kk}}$", r"Quãng $h$ nằm trong nước ; bước sóng ở đó là $\lambda_n$, không phải $\lambda_{kk}$."),
           (r"$N=\dfrac{2h}{\lambda_n}$", r"Đề hỏi quãng từ mặt nước xuống đáy, chỉ một chiều.")]),
  buoc("Kiểm tra")]),
]


# KaTeX: chỉ số dưới có dấu tiếng Việt → \text{…} (v_{thép} → v_{\text{thép}})
_SUBVN = re.compile(r"_\{([^{}\\]*[^\x00-\x7f][^{}\\]*)\}")
def _tx(x):
    if isinstance(x, str):
        return _SUBVN.sub(lambda m: "_{\\text{" + m.group(1) + "}}", x)
    if isinstance(x, list):
        return [_tx(v) for v in x]
    if isinstance(x, tuple):
        return tuple(_tx(v) for v in x)
    if isinstance(x, dict):
        return {k: _tx(v) for k, v in x.items()}
    return x
DANG, ANALYSIS, SOLS, STEPS = _tx(DANG), _tx(ANALYSIS), _tx(SOLS), _tx(STEPS)


def kiem_so():
    # D4
    assert 1 / VKK - 1 / VTHEP == F(1, 360)
    assert L4 == 306 and L4 / VKK == F(9, 10) and L4 / VTHEP == F(1, 20) and L4 / VKK - L4 / VTHEP == DT4
    assert TKK_G == F(14, 5) and TG == F(1, 5) and VG == 4760
    assert VKK * DT4 != L4 and (VTHEP - VKK) * DT4 != L4                     # hai cách sai bước 2
    assert TKK_G + DTG != TG and DTG != TG and VKK < LG / DTG < 400 and LG / TKK_G == VKK
    # D5 (bài ngược: cho d, t → v_xe)
    assert SAM == 1700 and SXE == 50 and VXE == 10 and VXE_KMH == 36 and D5B == 825 and T5B == F(33, 7)
    assert D5 + (D5 - SXE) == SAM                                          # âm đi tới vách rồi quay về gặp xe
    assert (VKK + VXE) * T5 == 2 * D5                                      # nghiệm lại câu a
    assert SAM - 2 * D5 < 0 and D5 - SAM / 2 != SXE                        # hai cách sai bước 2
    assert SXE / (T5 / 2) * F(36, 10) != VXE_KMH and VXE != VXE_KMH        # hai cách sai bước 3
    assert D5 + SXE != D5B and D5 != D5B
    assert 2 * D5B / VKK != T5B and 2 * D5B / (VKK - VXE) == T5 != T5B and T5B < T5
    assert abs(float(T5B) - 4.714) < 0.001
    # không trùng bài toán mẫu lý thuyết (xe 20 m/s, 4 s, 720/640 m)
    assert VXE != 20 and T5 != 4 and D5 not in (720, 640) and D5B not in (720, 640)
    # D6
    assert LKK == F(17, 25) and LN == 3 and H6 == 30 and N6 == 10
    assert VN * T6 != H6 and VKK * T6 / 2 != H6 and H6 / LKK != N6 and 2 * H6 / LN != N6
    assert LKK * VKK / VN != LN and VN / LKK != F6
    assert abs(float(LN / LKK) - float(VN / VKK)) < 1e-12
    for n, s in enumerate(STEPS):
        assert s["cap_do"] in (3, 4) and len(s["buoc"]) == SOLS[n].count('class="bt-step"'), n
    print("btm150_d456: kiểm số liệu đạt")


if __name__ == "__main__":
    kiem_so()
