"""Phần A: Bài 1, 2, 3 (mảng Chuyển động) của bộ 12 bài tự luận Cơ học -> part-A.json (lesson 167).
Số liệu tính bằng Python ở mục SỐ LIỆU rồi mới ghép vào chuỗi. Chạy: python3 build-A.py"""
import sys, json, os
SK = "/Users/MAC/Projects/thachlab/.claude/skills/soan-bai-tap-mau/scripts"
sys.path.insert(0, SK)
from dung import *          # hinh.py: fig, seg, dot, lbl, arrow, dim, RED, BLUE, ORG, GRN ; dung.py: sol, M, P, A, tbl, buoc
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "part-A.json")

def f(x, n=1):
    s = f"{x:.{n}f}".rstrip("0").rstrip(".") if n else f"{x:.0f}"
    return s.replace(".", "{,}")

# ───────────── SỐ LIỆU ─────────────
AB1, v1, v2, vm = 60, 40, 20, 50
t1 = AB1 / (v1 + v2); s1 = v1 * t1; sm = vm * t1
s2som = v2 * 0.25; d7 = AB1 - s2som; tc = d7 / (v1 + v2); sc = v1 * tc
assert (t1, s1, sm, d7) == (1, 40, 50, 55) and round(tc * 60) == 55 and abs(sc - 36.667) < 1e-2

w1, w2, w3 = 18, 20, 4            # bài 2
w23 = (w2 + w3) / 2               # 12
r21 = w1 / w23                    # t2/t1 = 1.5 (cùng quãng đường -> thời gian tỉ lệ nghịch tốc độ)
ttot = 1 + r21                    # 2.5 t1,  t1 = s/(2*18)
vtb = 1 / ((1 / (2 * w1)) * ttot)
T2 = 5 / 3; AB2 = vtb * T2
assert w23 == 12 and r21 == 1.5 and abs(vtb - 14.4) < 1e-9 and abs(AB2 - 24) < 1e-9

AB3, tx, tn = 60, 2, 3            # bài 3
vx, vn = AB3 / tx, AB3 / tn; u = (vx - vn) / 2; v = (vx + vn) / 2
tbe = AB3 / u; dB = AB3 - u * tx; tp = dB / (vn + u); tg = tx + tp; sg = u * tg
assert (vx, vn, u, v, tbe, dB, tp, tg, sg) == (30, 20, 5, 25, 12, 50, 2, 4, 20)

# ───────────── HÌNH ─────────────
def Tx(x, y, s, c="currentColor", size=12, anchor="middle", w="700"): return lbl(x, y, s, c, size, anchor, w)

def car(cx, y, flip=False):
    """Ô tô nhìn ngang, tâm cx, bánh chạm y."""
    cab = "-6,-14 -2,-20 8,-20 12,-14" if not flip else "6,-14 2,-20 -8,-20 -12,-14"
    return (f'<rect x="{cx-15:.1f}" y="{y-14:.1f}" width="30" height="10" rx="2" fill="none" stroke="currentColor" stroke-width="2.2"/>'
            f'<polyline points="' + " ".join(f"{cx+float(p.split(',')[0]):.1f},{y+float(p.split(',')[1])+0:.1f}" for p in cab.split()) + '" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/>'
            f'<circle cx="{cx-8:.1f}" cy="{y-3.5:.1f}" r="3.5" fill="none" stroke="currentColor" stroke-width="2"/>'
            f'<circle cx="{cx+8:.1f}" cy="{y-3.5:.1f}" r="3.5" fill="none" stroke="currentColor" stroke-width="2"/>')

def moto(cx, y):
    return (f'<circle cx="{cx-8:.1f}" cy="{y-4:.1f}" r="4" fill="none" stroke="currentColor" stroke-width="2"/>'
            f'<circle cx="{cx+8:.1f}" cy="{y-4:.1f}" r="4" fill="none" stroke="currentColor" stroke-width="2"/>'
            f'<polyline points="{cx-8:.1f},{y-4:.1f} {cx-1:.1f},{y-12:.1f} {cx+6:.1f},{y-12:.1f} {cx+8:.1f},{y-4:.1f}" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>'
            f'<circle cx="{cx-1:.1f}" cy="{y-22:.1f}" r="3.5" fill="none" stroke="currentColor" stroke-width="1.8"/>'
            f'<line x1="{cx-1:.1f}" y1="{y-18:.1f}" x2="{cx:.1f}" y2="{y-12:.1f}" stroke="currentColor" stroke-width="1.8"/>')

def grp(vals, dur, inner, keytimes=None):
    kt = f' keyTimes="{";".join(f"{k:.4f}" for k in keytimes)}"' if keytimes else ""
    v = ";".join(f"{x:.1f} {y:.1f}" for x, y in vals)
    x0, y0 = vals[0]
    return (f'<g transform="translate({x0:.1f} {y0:.1f})"><animateTransform attributeName="transform" type="translate" values="{v}"{kt} '
            f'dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>{inner}</g>')

# ---- Bài 1 ----
XA, XB = 40, 380
PX = (XB - XA) / AB1            # px / km
def x1_(km): return XA + km * PX

def moto_turns():
    """Các điểm quay đầu của xe máy: [(t, km)]. xe1: 40t ; xe2: 60-20t."""
    t, m, tgt = 0.0, 0.0, 2; pts = [(0.0, 0.0)]
    for _ in range(40):
        if tgt == 2: dt = ((AB1 - v2 * t) - m) / (vm + v2); m += vm * dt
        else:        dt = (m - v1 * t) / (vm + v1);        m -= vm * dt
        t += dt; pts.append((t, m)); tgt = 1 if tgt == 2 else 2
        if t > 0.9995: break
    pts.append((1.0, s1)); return pts

def fig1(anim):
    y = 150; ym = 96
    b = seg(XA - 16, y, XB + 16, y, "currentColor", 2.4) + dot(XA, y, 3.5) + dot(XB, y, 3.5)
    b += Tx(XA, y + 18, "A", size=14) + Tx(XB, y + 18, "B", size=14)
    b += seg(XA - 16, ym, XB + 16, ym, "currentColor", 1.2, "5 4", 0.45) + Tx(XB + 14, ym - 6, "làn xe máy", "currentColor", 10, "end", "400")
    b += dim("", "b", XA, y + 34, XB, y + 34, "AB = 60 km", (XA + XB) / 2, y + 52, "middle")
    def veh_car(cx, flip, vv, col, lab):
        d = -1 if flip else 1
        return car(cx, y, flip) + arrow("", col, cx, y - 32, cx + d * vv, y - 32, 2.6) + Tx(cx, y - 40, lab, {"r": RED, "b": BLUE, "g": GRN, "o": ORG}[col], 12)
    def veh_moto(cx):
        return moto(cx, ym) + arrow("", "o", cx, ym - 34, cx + vm, ym - 34, 2.6) + Tx(cx + 5, ym - 42, "50 km/h", ORG, 12)
    if not anim:
        b += veh_car(XA + 16, False, v1, "r", "40 km/h") + veh_car(XB - 16, True, v2, "b", "20 km/h") + veh_moto(XA + 16)
        return fig("c167-1-2", "0 0 420 214", "Hai địa điểm A và B cách nhau 60 km; hai xe đi ngược chiều, xe máy chạy giữa hai xe",
                   b, "Dữ kiện: hai xe xuất phát cùng lúc 7 h từ hai đầu. Độ dài mũi tên vận tốc tỉ lệ với tốc độ (1 px ứng với 1 km/h).")
    d = 5.0
    # nhóm có nội dung: dựng ở gốc (0) rồi tịnh tiến (translate y=0 vì nội dung đã có toạ độ y thật)
    g1 = grp([(XA + 16, 0), (XA + 16 + v1 * 1 * PX, 0)], d, car(0, y, False))
    g2 = grp([(XB - 16, 0), (XB - 16 - v2 * 1 * PX, 0)], d, car(0, y, True))
    b += Tx(16, 18, "xe 1 : 40 km/h", RED, 12, "start") + Tx(150, 18, "xe 2 : 20 km/h", BLUE, 12, "start") + Tx(284, 18, "xe máy : 50 km/h", ORG, 12, "start")
    tp = moto_turns()
    g3 = grp([(XA + 16 + km * PX, 0) for t, km in tp], d, moto(0, ym), [t for t, km in tp])
    b += g1 + g2 + g3 + Tx(XA + 40 * PX, y + 18, "gặp nhau", RED, 11, "middle", "400")
    return fig("c167-1-0", "0 0 420 214", "Mô phỏng hai xe đi ngược chiều gặp nhau, xe máy chạy qua lại giữa hai xe",
               b, "Mô phỏng 1 h chuyển động (1 s mô phỏng ứng với 12 phút thật). Xe máy quay đầu mỗi lần gặp một xe, cho tới khi hai xe gặp nhau.")

# ---- Bài 2 ----
def fig2(anim):
    L = 24; y = 120; x0, x1 = 40, 380; px = (x1 - x0) / L
    X = lambda km: x0 + km * px
    b = seg(x0 - 14, y, x1 + 14, y, "currentColor", 2.4) + dot(x0, y, 3.5) + dot(x1, y, 3.5) + dot(X(12), y, 3.5)
    b += Tx(x0, y + 18, "A", size=14) + Tx(x1, y + 18, "B", size=14) + Tx(X(12), y + 18, "C", size=14)
    b += dim("", "b", x0, y - 34, X(12), y - 34, "nửa đầu: 18 km/h", (x0 + X(12)) / 2, y - 42, "middle")
    b += dim("", "g", X(12), y - 34, x1, y - 34, "nửa sau", (X(12) + x1) / 2, y - 42, "middle")
    b += seg(X(12), y + 4, X(22), y + 4, ORG, 5, "", 0.9) + seg(X(22), y + 4, x1, y + 4, RED, 5, "", 0.9)
    b += Tx((X(12) + X(22)) / 2, y + 34, "nửa thời gian đầu: 20 km/h", ORG, 12) + Tx(x1 + 14, y + 52, "nửa thời gian sau: 4 km/h", RED, 12, "end")
    if not anim:
        return fig("c167-2-2", "0 0 420 190", "Đoạn đường AB chia hai nửa; nửa sau chia theo thời gian",
                   b, "Dữ kiện: nửa đầu chia theo quãng đường, nửa sau chia theo thời gian (hai phần nửa sau có thời gian bằng nhau, quãng đường khác nhau).")
    tk = [0, 2 / 3, 2 / 3 + 0.5, 5 / 3]; kt = [t / (5 / 3) for t in tk]; ks = [0, 12, 22, 24]
    vals = ";".join(f"{X(k):.1f}" for k in ks); kts = ";".join(f"{k:.4f}" for k in kt)
    b += (f'<circle cx="{X(0):.1f}" cy="{y - 8}" r="6" fill="{GRN}" stroke="currentColor" stroke-width="1.6">'
          f'<animate attributeName="cx" values="{vals}" keyTimes="{kts}" dur="6.00s" begin="indefinite" fill="freeze"/></circle>')
    return fig("c167-2-0", "0 0 420 190", "Mô phỏng người đi xe đạp từ A đến B với ba tốc độ khác nhau",
               b, "Mô phỏng 1 h 40 phút chuyển động (1 s mô phỏng ứng với 1 phút 40 giây thật). Vạch cam và đỏ ở nửa sau là hai khoảng thời gian bằng nhau.")

# ---- Bài 3 ----
def fig3(anim):
    xa, xb = 50, 370; px = (xb - xa) / AB3; X = lambda km: xa + km * px
    yt, yb = 80, 160            # hai bờ
    b = seg(14, yt, 406, yt, "currentColor", 2.4) + seg(14, yb, 406, yb, "currentColor", 2.4)
    b += f'<rect x="14" y="{yt}" width="392" height="{yb-yt}" fill="{BLUE}" opacity="0.10"/>'
    for xx in (80, 190, 300):
        b += seg(xx, 130, xx + 38, 130, BLUE, 1.6, "", 0.8) + chevron(xx + 38, 130, 1, 0, BLUE, 1.6, 8)
    b += Tx(210, 66, "dòng nước chảy từ A về B", BLUE, 12, "middle", "600")
    b += seg(xa, yb, xa, yb + 14, "currentColor", 2) + seg(xb, yb, xb, yb + 14, "currentColor", 2)
    b += Tx(xa, yb + 30, "A", size=14) + Tx(xb, yb + 30, "B", size=14)
    b += dim("", "g", xa, yb + 46, xb, yb + 46, "AB = 60 km", (xa + xb) / 2, yb + 64, "middle")
    def canoe(cx, y): return (f'<polygon points="{cx-16:.1f},{y-10:.1f} {cx+16:.1f},{y-10:.1f} {cx+10:.1f},{y:.1f} {cx-10:.1f},{y:.1f}" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/>'
                              f'<line x1="{cx:.1f}" y1="{y-10:.1f}" x2="{cx:.1f}" y2="{y-20:.1f}" stroke="currentColor" stroke-width="2"/>')
    def be(cx, y): return (f'<rect x="{cx-14:.1f}" y="{y-5:.1f}" width="28" height="7" rx="1.5" fill="none" stroke="currentColor" stroke-width="2"/>'
                           f'<line x1="{cx-5:.1f}" y1="{y-5:.1f}" x2="{cx-5:.1f}" y2="{y+2:.1f}" stroke="currentColor" stroke-width="1.2"/><line x1="{cx+5:.1f}" y1="{y-5:.1f}" x2="{cx+5:.1f}" y2="{y+2:.1f}" stroke="currentColor" stroke-width="1.2"/>')
    yc, ybe = 120, 150
    if not anim:
        b += canoe(xa, yc) + Tx(xa + 6, yc - 26, "ca nô", RED, 12) + be(xa, ybe) + Tx(xa + 34, ybe + 4, "bè gỗ", ORG, 12, "start")
        return fig("c167-3-2", "0 0 420 236", "Sông chảy từ A về B, ca nô và bè gỗ cùng xuất phát từ A",
                   b, "Dữ kiện: ca nô và bè gỗ cùng rời A lúc 6 h. Hình vẽ đúng tỉ lệ khoảng cách AB.")
    d = 5.0
    tk = [0, tx, tg]; kt = [t / tg for t in tk]
    cano = grp([(X(0), 0), (X(60), 0), (X(sg), 0)], d, canoe(0, yc) + Tx(0, yc - 26, "ca nô", RED, 12), kt)
    bee = grp([(X(0), 0), (X(sg), 0)], d, be(0, ybe) + Tx(34, ybe + 4, "bè gỗ", ORG, 12, "start"))
    b += bee + cano
    return fig("c167-3-0", "0 0 420 236", "Mô phỏng ca nô xuôi dòng tới B rồi quay về gặp bè gỗ đang trôi",
               b, "Mô phỏng 4 h chuyển động (1 s mô phỏng ứng với 48 phút thật). Bè trôi đều theo dòng; ca nô xuôi đến B, quay đầu và gặp bè.")

# ───────────── BẢNG PHÂN TÍCH ─────────────
AN1 = [
 ('"cách nhau 60 km … xe thứ nhất từ A … 40 km/h … xe thứ hai từ B … 20 km/h"', r'$AB=60$ km ; $v_1=40$ km/h ; $v_2=20$ km/h ; cùng xuất phát lúc 7 h',
  r'⚠ Hai xe đi <strong>ngược chiều</strong>, cùng xuất phát : khoảng cách giảm với tốc độ $v_1+v_2$ ; gặp nhau khi tổng quãng đường hai xe đi được bằng $AB$'),
 ('"Hai xe gặp nhau lúc mấy giờ ? Chỗ gặp cách A bao xa ?"', r'Cần tìm $t$ và $s_1$', r'$t=\dfrac{AB}{v_1+v_2}$ ; $s_1=v_1t$ (xe thứ nhất xuất phát từ A nên $s_1$ chính là khoảng cách tới A)'),
 ('"xe máy … từ A với tốc độ 50 km/h, chạy liên tục … quay đầu ngay … cho đến khi hai xe gặp nhau"', r'$v_m=50$ km/h không đổi ; chạy từ 7 h tới lúc hai xe gặp',
  r'⚠ Tốc độ không đổi và không nghỉ nên $s_m=v_mt$ với $t$ là <strong>thời gian chạy</strong> ; không cần cộng từng lượt đi–về'),
 ('"xe thứ hai xuất phát sớm hơn 15 phút (lúc 6 h 45)"', r'$t_0=15$ phút', r'⚠ Đổi phút ra giờ ; xe thứ hai đã đi một mình $v_2t_0$ nên lúc 7 h hai xe <strong>không còn cách nhau</strong> $AB$'),
 ('"hai xe gặp nhau lúc mấy giờ, cách A bao xa" (câu c)', r'Cần tìm giờ gặp và $s_1$', r'Quãng đường còn lại lúc 7 h : $d=AB-v_2t_0$ ; $t=\dfrac{d}{v_1+v_2}$ ; $s_1=v_1t$'),
]
AN2 = [
 ('"Nửa quãng đường đầu … 18 km/h"', r'$s_1=\dfrac s2$ ; $v_1=18$ km/h', r'$t_1=\dfrac{s/2}{v_1}$'),
 ('"nửa quãng đường còn lại, nửa thời gian đầu 20 km/h, nửa thời gian sau 4 km/h"', r'$s_2=\dfrac s2$ ; hai khoảng thời gian bằng nhau $t_a=t_b=t^\prime$',
  r'⚠ Hai đoạn nhỏ có <strong>cùng thời gian</strong> : $v_{tb2}=\dfrac{20t^\prime+4t^\prime}{2t^\prime}$ — chỉ trong trường hợp này mới bằng trung bình cộng hai tốc độ'),
 ('"tốc độ trung bình trên cả quãng đường AB"', r'Cần tìm $v_{tb}$', r'⚠ $v_{tb}=\dfrac{s}{t_1+t_2}$ : tổng quãng đường chia tổng thời gian, <strong>không phải</strong> trung bình cộng các tốc độ ; hai nửa quãng đường bằng nhau thì thời gian tỉ lệ nghịch với tốc độ'),
 ('"tổng thời gian đi từ A đến B là 1 h 40 phút. Tính AB"', r'$t=1$ h $40$ phút', r'Đổi ra giờ rồi $s=v_{tb}\cdot t$ ; cần tìm $AB$'),
]
AN3 = [
 ('"xuôi dòng từ A đến B hết 2 h … ngược dòng từ B về A hết 3 h … AB = 60 km"', r'$t_x=2$ h ; $t_n=3$ h ; $AB=60$ km',
  r'⚠ Tốc độ so với bờ : xuôi $v+u$, ngược $v-u$ ($v$ : ca nô đối với nước, $u$ : dòng nước) ; $v_x=\dfrac{AB}{t_x}$, $v_n=\dfrac{AB}{t_n}$'),
 ('"tốc độ của dòng nước và tốc độ của ca nô đối với nước"', r'Cần tìm $u$ và $v$', r'Giải hệ hai phương trình : $u=\dfrac{v_x-v_n}{2}$ ; $v=\dfrac{v_x+v_n}{2}$'),
 ('"một bè gỗ thả trôi theo dòng"', r'Bè không có động cơ', r'⚠ Bè trôi cùng tốc độ dòng nước nên tốc độ so với bờ là $u$ (không phải $v$) ; $t=\dfrac{AB}{u}$'),
 ('"Lúc 6 h … ca nô xuất phát từ A … tới B quay đầu ngay và chạy ngược về A"', r'Ca nô tới B sau $t_x$ ; bè vẫn trôi trong thời gian đó',
  r'⚠ Khi ca nô quay đầu, ca nô ngược dòng (tốc độ so với bờ $v_n$) còn bè xuôi dòng ($u$) : hai vật <strong>ngược chiều</strong>, tốc độ lại gần $v_n+u$'),
 ('"gặp lại bè lúc mấy giờ, tại điểm cách A bao xa"', r'Cần tìm giờ gặp và vị trí', r'Giờ gặp $=6$ h $+$ tổng thời gian ; vị trí cách A $=u\cdot t_{\text{tổng}}$ (đó là quãng đường bè trôi được)'),
]

# ───────────── LỜI GIẢI + BƯỚC ─────────────
S1 = sol(
 [r"<strong>Khái niệm:</strong> hai vật ngược chiều, cùng xuất phát : mỗi giờ khoảng cách giảm $v_1+v_2$.",
  r"<strong>Công thức:</strong> $t=\dfrac{AB}{v_1+v_2}$ ; $s=vt$.",
  r"Vật chuyển động đều, không nghỉ : $s=v\cdot t$ với $t$ là toàn bộ thời gian chuyển động.",
  r"⚠ <strong>Điều kiện:</strong> phút đổi ra giờ ; xe xuất phát sớm hơn thì trừ phần nó đã đi trước vào khoảng cách."],
 [("Thời gian hai xe gặp nhau", [P(r"Hai xe ngược chiều nên tốc độ lại gần nhau là tổng hai tốc độ :"), M(r"t=\dfrac{AB}{v_1+v_2}=\dfrac{60}{40+20}"), A(r"t=1\ \text{h}"), P("Gặp nhau lúc $7\\ \\text{h}+1\\ \\text{h}=8\\ \\text{h}$.")]),
  ("Chỗ gặp cách A", [P("Xe thứ nhất xuất phát từ A nên quãng đường nó đi được chính là khoảng cách từ A tới chỗ gặp :"), M(r"s_1=v_1t=40\cdot1"), A(r"s_1=40\ \text{km}")]),
  ("Quãng đường xe máy", [P("Xe máy chạy liên tục với tốc độ không đổi từ 7 h tới lúc hai xe gặp, tức đúng $t=1\\ \\text{h}$ :"), M(r"s_m=v_mt=50\cdot1"), A(r"s_m=50\ \text{km}"), P("Không cần cộng từng lượt đi–về.")]),
  ("Khoảng cách hai xe lúc 7 h", [P(r"Trong $15$ phút $=0{,}25\ \text{h}$ xe thứ hai đã đi :"), M(r"s_0=v_2\cdot0{,}25=20\cdot0{,}25=5\ \text{km}"), M(r"d=AB-s_0=60-5"), A(r"d=55\ \text{km}")]),
  ("Thời gian gặp kể từ 7 h", [P("Từ 7 h, hai xe cùng chạy nên làm lại như câu a với khoảng cách mới :"), M(r"t=\dfrac{d}{v_1+v_2}=\dfrac{55}{60}\ \text{h}"), A(r"t=55\ \text{phút}"), P("Gặp nhau lúc $7\\ \\text{h}\\ 55$ phút.")]),
  ("Chỗ gặp cách A", [P("Xe thứ nhất chỉ đi từ 7 h, trong $t=\\dfrac{55}{60}\\ \\text{h}$ :"), M(r"s_1=v_1t=40\cdot\dfrac{55}{60}"), A(r"s_1\approx36{,}7\ \text{km}")]),
  ("Kiểm tra", [P(r"Hai xe đi được tổng cộng : $40\cdot\dfrac{55}{60}+20\cdot\left(\dfrac{55}{60}+0{,}25\right)=36{,}7+23{,}3=60\ \text{km}=AB$ ✓."), P("Xe thứ hai đi sớm nên gặp sớm hơn câu a (7 h 55 so với 8 h) và chỗ gặp gần A hơn ✓.")])],
 ["a) $8\\ \\text{h}$ ; cách A $40\\ \\text{km}$", "b) $50\\ \\text{km}$", "c) $7\\ \\text{h}\\ 55$ ; cách A khoảng $36{,}7\\ \\text{km}$"],
 "Nhận dạng: thấy <strong>hai vật ngược chiều, hỏi lúc gặp</strong> → chia khoảng cách cho <strong>tổng tốc độ</strong> ; vật thứ ba chạy qua lại → chỉ cần <strong>tổng thời gian</strong>.")

S2 = sol(
 [r"<strong>Khái niệm:</strong> tốc độ trung bình $=\dfrac{\text{tổng quãng đường}}{\text{tổng thời gian}}$.",
  r"Hai đoạn <strong>cùng thời gian</strong> : $v_{tb}=\dfrac{v_a+v_b}{2}$.",
  r"Hai đoạn <strong>cùng quãng đường</strong> : thời gian tỉ lệ nghịch với tốc độ, $v_{tb}\neq\dfrac{v_a+v_b}{2}$.",
  r"⚠ <strong>Điều kiện:</strong> đổi $1$ h $40$ phút ra giờ ($40$ phút $=\dfrac{40}{60}$ h) trước khi nhân với km/h."],
 [("Tốc độ trung bình nửa quãng đường sau", [P(r"Hai khoảng thời gian bằng nhau, gọi mỗi khoảng là $t^\prime$ :"), M(r"s_2=20t^\prime+4t^\prime=24t^\prime"), M(r"v_{tb2}=\dfrac{s_2}{2t^\prime}=\dfrac{24t^\prime}{2t^\prime}"), A(r"v_{tb2}=12\ \text{km/h}")]),
  ("So sánh thời gian hai nửa quãng đường", [P(r"Hai nửa quãng đường bằng nhau nên thời gian tỉ lệ nghịch với tốc độ trung bình của mỗi nửa :"), M(r"\dfrac{t_2}{t_1}=\dfrac{v_1}{v_{tb2}}=\dfrac{18}{12}"), A(r"\dfrac{t_2}{t_1}=1{,}5")]),
  ("Tốc độ trung bình cả quãng đường", [P(r"Đặt $AB=s$ : $t_1=\dfrac{s/2}{18}=\dfrac{s}{36}$ và $t_2=1{,}5\,t_1$."), M(r"v_{tb}=\dfrac{s}{t_1+t_2}=\dfrac{s}{2{,}5\cdot\dfrac{s}{36}}=\dfrac{36}{2{,}5}"), A(r"v_{tb}=14{,}4\ \text{km/h}"), P(r"Trung bình cộng ba tốc độ là $\dfrac{18+20+4}{3}=14$ km/h : sai vì các đoạn không cùng thời gian.")]),
  ("Đổi thời gian ra giờ", [M(r"t=1\ \text{h}+\dfrac{40}{60}\ \text{h}"), A(r"t\approx1{,}67\ \text{h}")]),
  ("Quãng đường AB", [M(r"AB=v_{tb}\cdot t=14{,}4\cdot\dfrac{5}{3}"), A(r"AB=24\ \text{km}")]),
  ("Kiểm tra", [P(r"Nửa đầu $12$ km ở $18$ km/h mất $\dfrac{12}{18}=\dfrac23$ h ; nửa sau $12$ km ở $12$ km/h mất $1$ h ; tổng $\dfrac53$ h $=1$ h $40$ phút ✓."), P(r"Nửa sau : $20\cdot0{,}5+4\cdot0{,}5=12$ km đúng bằng nửa quãng đường ✓.")])],
 ["a) $12\\ \\text{km/h}$", "b) $14{,}4\\ \\text{km/h}$", "c) $24\\ \\text{km}$"],
 "Nhận dạng: thấy <strong>nửa quãng đường / nửa thời gian</strong> → đặt $s$ hoặc $t$ làm ẩn, lập <strong>tổng quãng đường / tổng thời gian</strong>.")

S3 = sol(
 [r"<strong>Khái niệm:</strong> $v$ : tốc độ ca nô đối với nước ; $u$ : tốc độ dòng nước ; bè trôi với tốc độ $u$.",
  r"<strong>Công thức:</strong> xuôi dòng $v_x=v+u$ ; ngược dòng $v_n=v-u$ ; $s=vt$.",
  r"Hai vật ngược chiều : tốc độ lại gần $=$ tổng hai tốc độ so với bờ.",
  r"⚠ <strong>Điều kiện:</strong> mọi tốc độ trong $s=vt$ phải cùng lấy so với bờ ; bè vẫn trôi suốt thời gian ca nô đi xuôi."],
 [("Tốc độ xuôi dòng", [M(r"v_x=\dfrac{AB}{t_x}=\dfrac{60}{2}"), A(r"v_x=30\ \text{km/h}")]),
  ("Tốc độ ngược dòng", [M(r"v_n=\dfrac{AB}{t_n}=\dfrac{60}{3}"), A(r"v_n=20\ \text{km/h}")]),
  ("Tốc độ dòng nước", [P("Lấy hiệu hai phương trình $v+u$ và $v-u$ :"), M(r"v_x-v_n=2u\ \Rightarrow\ u=\dfrac{30-20}{2}"), A(r"u=5\ \text{km/h}")]),
  ("Tốc độ ca nô đối với nước", [P("Lấy tổng hai phương trình :"), M(r"v_x+v_n=2v\ \Rightarrow\ v=\dfrac{30+20}{2}"), A(r"v=25\ \text{km/h}")]),
  ("Thời gian bè trôi từ A đến B", [P("Bè trôi cùng tốc độ dòng nước :"), M(r"t=\dfrac{AB}{u}=\dfrac{60}{5}"), A(r"t=12\ \text{h}")]),
  ("Bè cách B khi ca nô tới B", [P("Ca nô tới B sau $t_x=2$ h ; trong thời gian đó bè đã trôi $u\\,t_x=10$ km :"), M(r"d=AB-u\,t_x=60-5\cdot2"), A(r"d=50\ \text{km}")]),
  ("Thời gian từ lúc quay đầu đến lúc gặp", [P("Ca nô ngược dòng, bè xuôi dòng : hai vật ngược chiều, tốc độ lại gần là tổng :"), M(r"v_n+u=20+5=25\ \text{km/h}"), M(r"t^\prime=\dfrac{d}{v_n+u}=\dfrac{50}{25}"), A(r"t^\prime=2\ \text{h}")]),
  ("Giờ gặp nhau", [P("Tính từ lúc 6 h, tổng thời gian chuyển động của cả hai là :"), M(r"t_{\text{tổng}}=t_x+t^\prime=2+2=4\ \text{h}"), A(r"\text{Gặp nhau lúc }10\ \text{h}")]),
  ("Chỗ gặp cách A", [P("Chỗ gặp cũng là nơi bè trôi tới sau $4$ h :"), M(r"s=u\,t_{\text{tổng}}=5\cdot4"), A(r"s=20\ \text{km}")]),
  ("Kiểm tra", [P(r"Ca nô đi ngược từ B trong $2$ h : $20\cdot2=40$ km, tới vị trí cách A là $60-40=20$ km ✓ trùng với chỗ bè tới."),
                P(r"Cách khác (so với nước) : nước coi như đứng yên, bè đứng yên, ca nô rời bè với tốc độ $v$ trong $2$ h rồi quay lại với cùng tốc độ $v$ nên cũng mất $2$ h ✓.")])],
 ["a) $u=5\\ \\text{km/h}$ ; $v=25\\ \\text{km/h}$", "b) $12\\ \\text{h}$", "c) $10\\ \\text{h}$ ; cách A $20\\ \\text{km}$"],
 "Nhận dạng: thấy <strong>xuôi – ngược dòng, bè trôi</strong> → lập hệ $v+u$, $v-u$ ; gặp bè thì xét <strong>hai vật ngược chiều</strong> hoặc xét <strong>so với dòng nước</strong>.")

# ---- buoc[] ----
B1 = dict(
 nhan_dang="Thấy <b>hai xe ngược chiều</b> → chia khoảng cách cho <b>tổng tốc độ</b> ; xe máy qua lại → nhân <b>tổng thời gian</b>.",
 cap_do=3, fading="giau_het", go_roi={"buoc_hay_sai": 3},
 buoc=[
  buoc("Thời gian hai xe gặp nhau", "Kể từ 7 h, sau bao lâu hai xe gặp nhau ?", 1, "h", 0.02,
       "Chia $AB$ cho một tốc độ (ví dụ $60/40$) hoặc cho hiệu hai tốc độ — hai xe ngược chiều nên phải dùng tổng $v_1+v_2$."),
  buoc("Chỗ gặp cách A", "Chỗ gặp cách A bao nhiêu km ?", 40, "km", 0.5,
       "Lấy quãng đường cả hai xe cùng đi ($v_1+v_2$ nhân $t$) rồi coi là khoảng cách tới A ; hoặc nhân tốc độ xe thứ hai với $t$ (đó là khoảng cách tới B).",
       ke=[("Quãng đường xe thứ nhất đi được : $s_1=v_1t$", True),
           ("$s=(v_1+v_2)t$", "Đó là tổng quãng đường cả hai xe đi, bằng đúng $AB$ ; chưa phải khoảng cách từ A."),
           ("$s=v_2t$", "Xe thứ hai đi từ B, nên $v_2t$ là khoảng cách từ chỗ gặp tới B chứ không phải tới A.")]),
  buoc("Quãng đường xe máy", "Tổng quãng đường người đi xe máy đã đi là bao nhiêu km ?", 50, "km", 0.5,
       "Cố cộng từng lượt đi–về hoặc lấy quãng đường $AB$ ; thực ra xe máy chạy với tốc độ không đổi suốt thời gian hai xe tới khi gặp.",
       ke=[("Nhân tốc độ xe máy với thời gian hai xe tới khi gặp : $s_m=v_mt$", True),
           ("$s_m=AB$, vì xe máy chạy từ A tới B", "Xe máy quay đầu liên tục chứ không đi một chiều tới B ; quãng đường của nó dài hơn đoạn nó dịch chuyển được."),
           ("$s_m=\\dfrac12v_mt$, vì xe đi rồi quay lại", "Tốc độ không đổi nên quãng đường mọi chiều đều cộng dồn, không bị chia đôi.")]),
  buoc("Khoảng cách hai xe lúc 7 h", "Xe thứ hai xuất phát lúc 6 h 45. Đến 7 h, hai xe còn cách nhau bao nhiêu km ?", 55, "km", 0.2,
       "Quên đổi $15$ phút ra giờ (lấy $20\\cdot15$), hoặc coi lúc 7 h hai xe vẫn cách nhau $AB$.",
       ke=[("Trừ quãng đường xe thứ hai đã đi trong $0{,}25$ h khỏi $AB$", True),
           ("Vẫn dùng khoảng cách $AB$ rồi trừ $0{,}25$ h khỏi thời gian gặp ở câu a", "Thời gian đang là giờ còn khoảng cách là km ; phải đổi phần đi sớm ra quãng đường rồi mới trừ vào khoảng cách."),
           ("Cộng quãng đường xe thứ hai đã đi vào $AB$", "Xe đi sớm làm hai xe lại gần nhau, nên khoảng cách còn lại giảm đi chứ không tăng.")]),
  buoc("Thời gian gặp kể từ 7 h", "Từ 7 h, hai xe gặp nhau sau bao nhiêu phút ?", 55, "phút", 0.5,
       "Chia cho tổng tốc độ nhưng để nguyên kết quả đơn vị giờ rồi ghi thành phút, hoặc tính mốc thời gian từ 6 h 45 thay vì 7 h.",
       ke=[("Chia khoảng cách còn lại cho $v_1+v_2$, rồi đổi giờ ra phút", True),
           ("Chia $AB$ cho $v_1+v_2$ rồi cộng thêm $15$ phút", "Lúc 7 h hai xe không còn cách nhau $AB$ ; phải dùng khoảng cách đã giảm."),
           ("Chia khoảng cách còn lại cho $v_1$ (chỉ xe thứ nhất)", "Cả hai xe đều chạy lại gần nhau, nên mẫu số là tổng hai tốc độ.")]),
  buoc("Chỗ gặp cách A", "Chỗ gặp bây giờ cách A bao nhiêu km ?", 36.7, "km", 0.2,
       "Nhân $v_1$ với thời gian tính từ 6 h 45 (xe thứ nhất chưa xuất phát lúc đó), hoặc để thời gian là phút khi nhân với km/h.",
       ke=[("$s_1=v_1t$ với $t$ là thời gian xe thứ nhất đi (tính từ 7 h, đổi ra giờ)", True),
           ("$s_1=v_1(t+0{,}25)$", "Xe thứ nhất chỉ xuất phát lúc 7 h, không phải 6 h 45."),
           ("$s_1=v_1t$ với $t$ để nguyên số phút", "Tốc độ tính bằng km/h nên $t$ phải đổi ra giờ trước khi nhân.")]),
  buoc("Kiểm tra")])

B2 = dict(
 nhan_dang="Thấy <b>nửa quãng đường / nửa thời gian</b> → đặt <b>s hoặc t</b> làm ẩn, lập <b>tổng quãng đường / tổng thời gian</b>.",
 cap_do=3, fading="giau_het", go_roi={"buoc_hay_sai": 2},
 buoc=[
  buoc("Tốc độ trung bình nửa quãng đường sau", "Tốc độ trung bình của người đó trên nửa quãng đường sau là bao nhiêu km/h ?", 12, "km/h", 0.1,
       "Dùng công thức cho đoạn cùng quãng đường ($2v_av_b/(v_a+v_b)\\approx6{,}7$) trong khi hai khoảng thời gian ở đây bằng nhau."),
  buoc("So sánh thời gian hai nửa quãng đường", "Hai nửa quãng đường bằng nhau : thời gian đi nửa sau gấp bao nhiêu lần thời gian đi nửa đầu ?", 1.5, "lần", 0.02,
       "Lấy tỉ số ngược ($v_{tb2}/v_1$) hoặc cho hai nửa có thời gian bằng nhau vì nửa quãng đường bằng nhau.",
       ke=[("Cùng quãng đường thì thời gian tỉ lệ nghịch với tốc độ : $\\dfrac{t_2}{t_1}=\\dfrac{v_1}{v_{tb2}}$", True),
           ("Hai nửa quãng đường bằng nhau nên thời gian cũng bằng nhau", "Quãng đường bằng nhau nhưng tốc độ khác nhau nên thời gian khác nhau."),
           ("$\\dfrac{t_2}{t_1}=\\dfrac{v_{tb2}}{v_1}$", "Tốc độ lớn đi nhanh hơn nên mất ít thời gian hơn ; tỉ số thời gian là tỉ số nghịch đảo của tỉ số tốc độ.")]),
  buoc("Tốc độ trung bình cả quãng đường", "Tốc độ trung bình trên cả quãng đường AB là bao nhiêu km/h ?", 14.4, "km/h", 0.05,
       "Lấy trung bình cộng ba tốc độ ($\\dfrac{18+20+4}{3}=14$) hoặc trung bình cộng hai tốc độ của hai nửa quãng đường.",
       ke=[("$v_{tb}=\\dfrac{s}{t_1+t_2}$ với $t_1=\\dfrac{s}{36}$ và $t_2=1{,}5\\,t_1$", True),
           ("$v_{tb}=\\dfrac{18+20+4}{3}$", "Trung bình cộng chỉ đúng khi các đoạn có cùng thời gian ; các đoạn này thì không."),
           ("$v_{tb}=\\dfrac{18+12}{2}$", "Hai nửa quãng đường bằng nhau nhưng thời gian đi khác nhau, nên không lấy trung bình cộng hai tốc độ.")]),
  buoc("Đổi thời gian ra giờ", "Đổi 1 h 40 phút ra giờ (làm tròn hai chữ số thập phân) :", 1.67, "h", 0.01,
       "Viết $1$ h $40$ phút $=1{,}40$ h (coi $40$ phút là $0{,}40$ h).",
       ke=[("$1\\ \\text{h}+\\dfrac{40}{60}\\ \\text{h}$", True),
           ("$1{,}40\\ \\text{h}$, vì chữ số sau dấu phẩy là $40$", "Một giờ có $60$ phút nên $40$ phút là $\\dfrac{40}{60}$ giờ, không phải $0{,}40$ giờ."),
           ("Không cần đổi vì tốc độ trung bình đã tính bằng km/h", "Tốc độ tính theo km/h nên thời gian phải tính theo giờ thì quãng đường mới ra km.")]),
  buoc("Quãng đường AB", "Tính độ dài quãng đường AB :", 24, "km", 0.2,
       "Nhân thời gian với tốc độ $18$ km/h (tốc độ nửa đầu) thay vì tốc độ trung bình cả đường.",
       ke=[("$AB=v_{tb}\\cdot t$ với $v_{tb}$ của cả quãng đường", True),
           ("$AB=v_1\\cdot t$ với $v_1$ là tốc độ nửa đầu", "Tốc độ nửa đầu chỉ đúng cho nửa quãng đường đầu ; cả quãng đường phải dùng tốc độ trung bình toàn bộ."),
           ("$AB=\\dfrac{v_{tb}}{t}$", "Quãng đường bằng tốc độ nhân thời gian, không chia.")]),
  buoc("Kiểm tra")])

B3 = dict(
 nhan_dang="Thấy <b>xuôi – ngược dòng, bè trôi</b> → lập hệ <b>v + u, v − u</b> ; gặp bè → xét <b>so với nước</b>.",
 cap_do=3, fading="giau_het", go_roi={"buoc_hay_sai": 6},
 buoc=[
  buoc("Tốc độ xuôi dòng", "Khi xuôi dòng, tốc độ của ca nô so với bờ là bao nhiêu km/h ?", 30, "km/h", 0.2,
       "Lấy $AB$ chia cho tổng hai thời gian ($60/5$), hoặc chia cho thời gian ngược dòng."),
  buoc("Tốc độ ngược dòng", "Khi ngược dòng, tốc độ của ca nô so với bờ là bao nhiêu km/h ?", 20, "km/h", 0.2,
       "Chia $AB$ cho thời gian xuôi dòng, hoặc chia cho tổng hai thời gian.",
       ke=[("$v_n=\\dfrac{AB}{t_n}$ với $t_n$ là thời gian đi ngược dòng", True),
           ("$v_n=\\dfrac{AB}{t_x}$", "Thời gian $t_x$ là lúc xuôi dòng ; tốc độ ngược dòng phải dùng thời gian chiều ngược."),
           ("$v_n=\\dfrac{AB}{t_x+t_n}$", "Tổng hai thời gian là cả đi lẫn về, quãng đường tương ứng là $2AB$ nên không dùng được với $AB$.")]),
  buoc("Tốc độ dòng nước", "Tốc độ của dòng nước là bao nhiêu km/h ?", 5, "km/h", 0.1,
       "Lấy hiệu hai tốc độ mà quên chia $2$ : khi đó ra $2u$ chứ không phải $u$.",
       ke=[("$u=\\dfrac{v_x-v_n}{2}$", True),
           ("$u=v_x-v_n$", "Hiệu $v_x-v_n=2u$ (vì $u$ xuất hiện cả hai lần), nên phải chia $2$."),
           ("$u=\\dfrac{v_x+v_n}{2}$", "Đó là tốc độ ca nô đối với nước ; $u$ xuất hiện ở hiệu chứ không phải ở tổng.")]),
  buoc("Tốc độ ca nô đối với nước", "Tốc độ của ca nô đối với nước là bao nhiêu km/h ?", 25, "km/h", 0.2,
       "Lấy hiệu $v_x-v_n$, hoặc cộng $u$ vào $v_x$.",
       ke=[("$v=\\dfrac{v_x+v_n}{2}$", True),
           ("$v=v_x+u$", "Tốc độ xuôi dòng $v_x$ đã gồm sẵn $u$ rồi ; cộng thêm là tính hai lần."),
           ("$v=v_x-v_n$", "Hiệu hai tốc độ so với bờ bằng $2u$, không phải $v$.")]),
  buoc("Thời gian bè trôi từ A đến B", "Một bè gỗ thả trôi từ A đến B mất bao nhiêu giờ ?", 12, "h", 0.1,
       "Dùng tốc độ ca nô đối với nước làm tốc độ của bè, hoặc lấy trung bình thời gian xuôi và ngược.",
       ke=[("Bè trôi cùng tốc độ dòng nước : $t=\\dfrac{AB}{u}$", True),
           ("$t=\\dfrac{AB}{v}$", "Bè không có động cơ nên không có tốc độ riêng $v$ ; nó chỉ chuyển động theo dòng nước."),
           ("$t=\\dfrac{t_x+t_n}{2}$", "Trung bình hai thời gian không có ý nghĩa vật lí ở đây ; bè chuyển động theo dòng với tốc độ $u$.")]),
  buoc("Bè cách B khi ca nô tới B", "Khi ca nô tới B, bè còn cách B bao nhiêu km ?", 50, "km", 0.5,
       "Coi bè đứng yên ở A, hoặc tính quãng đường bè trôi với tốc độ ca nô.",
       ke=[("$d=AB-u\\,t_x$ : bè đã trôi trong $t_x$", True),
           ("$d=AB$, vì bè thả ở A", "Bè không đứng yên mà vẫn trôi theo dòng suốt thời gian ca nô đi xuôi."),
           ("$d=AB-v\\,t_x$", "Bè trôi với tốc độ dòng nước $u$ chứ không phải $v$.")]),
  buoc("Thời gian từ lúc quay đầu đến lúc gặp", "Từ lúc ca nô quay đầu ở B, sau bao lâu thì ca nô gặp bè ?", 2, "h", 0.05,
       "Lấy hiệu hai tốc độ ($v_n-u$) như đuổi nhau, hoặc coi bè đứng yên.",
       ke=[("Hai vật ngược chiều : $t^\\prime=\\dfrac{d}{v_n+u}$", True),
           ("Tốc độ lại gần là $v_n-u$", "Ca nô đi ngược dòng còn bè đi xuôi dòng, hai vật ngược chiều nên tốc độ lại gần là tổng."),
           ("$t^\\prime=\\dfrac{d}{v_n}$, coi bè đứng yên", "Bè vẫn trôi về phía ca nô với tốc độ $u$ nên hai vật lại gần nhanh hơn $v_n$.")]),
  buoc("Giờ gặp nhau", "Ca nô gặp lại bè lúc mấy giờ (ghi số giờ trong ngày) ?", 10, "h", 0.05,
       "Quên cộng thời gian ca nô đi xuôi ($t_x$) ; chỉ lấy $6+t^\\prime$.",
       ke=[("Mốc 6 h cộng $t_x+t^\\prime$", True),
           ("Mốc 6 h cộng $t^\\prime$", "Thiếu thời gian ca nô đi xuôi từ A tới B trước khi quay đầu."),
           ("Mốc 6 h cộng $t_x$", "Lúc đó ca nô mới tới B, hai vật chưa gặp nhau.")]),
  buoc("Chỗ gặp cách A", "Chỗ gặp cách A bao nhiêu km ?", 20, "km", 0.2,
       "Tính từ B hoặc chỉ lấy thời gian sau khi quay đầu.",
       ke=[("Quãng đường bè trôi được : $s=u\\,t_{\\text{tổng}}$", True),
           ("$s=u\\,t^\\prime$", "Bè đã trôi từ lúc 6 h, không chỉ từ lúc ca nô quay đầu."),
           ("$s=v_n\\,t^\\prime$", "Đó là quãng đường ca nô đi ngược từ B, tức khoảng cách tới B chứ không phải tới A.")]),
  buoc("Kiểm tra")])

# ───────────── GHÉP ─────────────
def dang(label, topic, de, fn, analysis, solution, steps):
    return dict(label=label, topic=topic, form="bai_tap", problem_html=de + fn(True), analysis_html=fn(False) + tbl(analysis),
                solution_html=solution, **steps)

DE1 = ("<p>Hai địa điểm A, B cách nhau $60\\ \\text{km}$. Lúc $7$ h, xe thứ nhất đi từ A về B với tốc độ không đổi $40\\ \\text{km/h}$ ; cùng lúc đó xe thứ hai đi từ B về A với tốc độ không đổi $20\\ \\text{km/h}$.</p>"
       "<ol type=\"a\"><li>Hai xe gặp nhau lúc mấy giờ ? Chỗ gặp cách A bao xa ?</li>"
       "<li>Cũng lúc $7$ h, một người đi xe máy xuất phát từ A với tốc độ $50\\ \\text{km/h}$, chạy liên tục giữa hai xe : gặp xe này thì quay đầu ngay chạy về phía xe kia, cho đến khi hai xe gặp nhau. Tính tổng quãng đường người đi xe máy đã đi.</li>"
       "<li>Nếu xe thứ hai xuất phát sớm hơn $15$ phút (lúc $6$ h $45$), hai xe gặp nhau lúc mấy giờ, cách A bao xa ?</li></ol>")
DE2 = ("<p>Một người đi xe đạp từ A đến B. Nửa quãng đường đầu người đó đi với tốc độ $18\\ \\text{km/h}$. Trên nửa quãng đường còn lại, nửa thời gian đầu đi với tốc độ $20\\ \\text{km/h}$, nửa thời gian sau đi với tốc độ $4\\ \\text{km/h}$ (đường xấu).</p>"
       "<ol type=\"a\"><li>Tính tốc độ trung bình trên nửa quãng đường sau.</li><li>Tính tốc độ trung bình trên cả quãng đường AB.</li>"
       "<li>Biết tổng thời gian đi từ A đến B là $1$ h $40$ phút. Tính AB.</li></ol>")
DE3 = ("<p>Một ca nô xuôi dòng từ A đến B hết $2$ h và ngược dòng từ B về A hết $3$ h. Biết $AB=60\\ \\text{km}$ ; tốc độ của ca nô đối với nước và tốc độ của dòng nước đều không đổi.</p>"
       "<ol type=\"a\"><li>Tính tốc độ của dòng nước và tốc độ của ca nô đối với nước.</li><li>Một bè gỗ thả trôi theo dòng từ A đến B mất bao lâu ?</li>"
       "<li>Lúc $6$ h, bè bắt đầu trôi từ A ; cùng lúc ca nô xuất phát từ A xuôi về B, tới B quay đầu ngay và chạy ngược về A. Ca nô gặp lại bè lúc mấy giờ, tại điểm cách A bao xa ?</li></ol>")

out = {"lesson_id": 167, "lesson_title": "Bài tập tuần này: 12 bài tự luận Cơ học",
       "review": {"checked": True, "notes": "tạm, chờ kiểm chéo"},
       "dang_bai": [
        dang("Bài 1 · Vận dụng · Hai xe và người đưa thư · CN 11/10", "Tổng hợp vận tốc, tính tương đối của chuyển động", DE1, fig1, AN1, S1, B1),
        dang("Bài 2 · Vận dụng · Tốc độ trung bình — nửa quãng đường, nửa thời gian · Thứ Hai 12/10", "Tốc độ trung bình và vận tốc trung bình", DE2, fig2, AN2, S2, B2),
        dang("Bài 3 · Vận dụng cao · Ca nô và bè gỗ · CN 11/10", "Tổng hợp vận tốc, tính tương đối của chuyển động", DE3, fig3, AN3, S3, B3)]}
json.dump(out, open(OUT, "w"), ensure_ascii=False, indent=1)
print("ghi", OUT)
