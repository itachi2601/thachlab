"""Bài tập mẫu Chuyên đề 13 "Chuyển động cơ học và đồ thị chuyển động" (khoá Vật lí HSG & chuyên, KHTN 9) — lesson_id 162.
Nguồn: content/hsg9/cd13-chuyen-dong-va-do-thi/nguon.md (mục C dạng bài, D ví dụ, E tự luyện, G nâng cao; đã tự giải lại từng bài).
YCCĐ "bài tương tự": lớp 10 b5 (id 50) và b7 (id 52) — topic 107–111, xem trường `topic` của từng dạng.
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-162.py   (idempotent; không ghi DB)

Lỗi/điểm sửa so với nguồn:
 - G2 (hai canô trên hồ tròn): nguồn kết luận C = 720 m, nhưng "lần gặp thứ hai cách B 90 m" còn một khả năng nữa (chưa tới B) cho C = 1080 m, và còn khả năng thứ ba (canô 1 đã chạy hết một vòng, v1:v2 = 5:1) cho C = 360 m
   (dò lại bằng Python: C = 360, 720, 1080) → đề ghi rõ ba khả năng.
 - G1: nguồn dùng "tính đối xứng" không chứng minh → giải lại bằng cách so sánh thời gian của hai người đi bộ.
 - G4: nguồn trộn "thước thẳng" với "thước kẹp panme" khi đo s và d → ghi lại rõ dụng cụ.
Mọi đáp số được tự tính lại bằng Python ở cuối file (assert) trước khi ghi."""
import json, math, os, sys
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

J = os.path.join(HERE, "162.json")
NOTE = "Hình minh hoạ, không đúng tỉ lệ."
GREY = "#94a3b8"


# ═════════════ TIỆN ÍCH HÌNH ═════════════
def R(x, y, w, h, c="currentColor", sw=2, fill="none", rx=0, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{c}" '
            f'stroke-width="{sw}"{d} opacity="{op}"/>')

def circ(x, y, r, c="currentColor", sw=2, fill="none"):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{c}" stroke-width="{sw}"/>'

import re as _re
def rich(s, size=13):
    """`v_tb` hoặc `v_{bơi}` → chỉ số dưới (tspan hạ dòng rồi trả lại)."""
    out, pos = "", 0
    ms = list(_re.finditer(r"_\{([^}]+)\}|_([A-Za-z0-9]+)", s))
    for k, m in enumerate(ms):
        out += s[pos:m.start()] if k == 0 else ""
        out += f'<tspan dy="4" font-size="{size - 3}">{m.group(1) or m.group(2)}</tspan>'
        nxt = ms[k + 1].start() if k + 1 < len(ms) else len(s)
        rest = s[m.end():nxt]
        if rest:
            out += f'<tspan dy="-4">{rest}</tspan>'
        pos = m.end()
    return out if ms else s

def txt(x, y, s, c="currentColor", size=13, anchor="start", weight="700"):
    return lbl(x, y, rich(s, size), c, size, anchor, weight)

def trk(pts, dur, inner):
    """Nhóm chạy MỘT lần khi bấm nút, đi qua các điểm (dx, dy) cách đều thời gian; nội suy tuyến tính giữa các mẫu."""
    vals = ";".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    return (f'<g transform="translate({pts[0][0]:.1f} {pts[0][1]:.1f})"><animateTransform attributeName="transform" type="translate" '
            f'values="{vals}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>{inner}</g>')

def dotg(label="", c=GRN, lc="currentColor"):
    return circ(0, 0, 6, "currentColor", 1.6, c) + (txt(0, -12, label, lc, 12, "middle") if label else "")

def xcar(label="", lc="currentColor"):
    """Ô tô nhìn ngang, gốc ở giữa đáy bánh xe."""
    return (R(-17, -17, 34, 11, "currentColor", 2.4, rx=3) + f'<polyline points="-9,-17 -5,-24 7,-24 11,-17" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/>'
            + circ(-9, -4, 4.5, "currentColor", 2.2) + circ(9, -4, 4.5, "currentColor", 2.2) + (txt(0, -30, label, lc, 12, "middle") if label else ""))

def moto(label="", lc="currentColor"):
    return (circ(-11, -6, 6, "currentColor", 2.2) + circ(11, -6, 6, "currentColor", 2.2)
            + f'<path d="M-11,-6 L-3,-15 L6,-15 L11,-6 M-3,-15 L-6,-21 M6,-15 L3,-22" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/>' + (txt(0, -30, label, lc, 12, "middle") if label else ""))

def train(L, h=20, c="currentColor", op=1, wheels=True, cars=3):
    """Đoàn tàu dài L px, đáy ở y=0, đuôi ở x=0, đầu ở x=L (vát nhẹ)."""
    pts = f"0,0 0,{-h} {L - 8:.1f},{-h} {L:.1f},{-h + 9} {L:.1f},0"
    b = f'<polygon points="{pts}" fill="none" stroke="{c}" stroke-width="2.4" stroke-linejoin="round" opacity="{op}"/>'
    for i in range(1, cars):
        b += seg(L * i / cars, 0, L * i / cars, -h, c, 1.4, "", op)
    if wheels:
        for i in range(cars):
            b += circ(L * (i + .22) / cars + 2, 3, 3, c, 1.8) + circ(L * (i + .78) / cars - 2, 3, 3, c, 1.8)
    return b


def tick(x, y, s=7):
    return seg(x, y - s, x, y + s, "currentColor", 2)


# ═════════════ HÌNH ═════════════
# ───────────── Dạng 1 · xe đạp điện AB = 24 km ─────────────
def d1(kk):
    p = f"d1{kk}"; X0, X1, PK = 30, 390, 15      # 24 km → 360 px
    xm = X0 + 12 * PK
    b = defs(p)
    if kk == 0:
        steps = 9; hq = Fr(1, 6)                      # 9 mẫu × 1/6 h = 1,5 h
        def pos_a(t):  return 12 * t if t <= 1 else 12 + 24 * (t - 1)
        def pos_b(t):  return 12 * t if t <= Fr(2, 3) else min(24, 8 + 24 * (t - Fr(2, 3)))
        xa = [X0 + PK * float(pos_a(hq * k)) for k in range(steps + 1)]
        xb = [X0 + PK * float(pos_b(hq * k)) for k in range(steps + 1)]
        dur = 4.5                                      # 1 giờ thật = 3 giây
        b += txt(16, 22, "Lần a: chia theo quãng đường", "currentColor", 13) + txt(X1, 22, "v_tb = ?", RED, 13, "end")
        b += seg(X0, 62, X1, 62, "currentColor", 3) + tick(X0, 62) + tick(xm, 62) + tick(X1, 62)
        b += txt((X0 + xm) / 2, 46, "12 km/h", BLUE, 13, "middle") + txt((xm + X1) / 2, 46, "24 km/h", ORG, 13, "middle")
        b += txt(X0, 86, "A", "currentColor", 13, "middle") + txt(X1, 86, "B", "currentColor", 13, "middle") + txt(xm, 86, "AB = 24 km", "currentColor", 12, "middle", "400")
        b += (f'<circle cx="{xa[0]:.1f}" cy="62" r="6" fill="{GRN}" stroke="currentColor" stroke-width="1.6">{smil("cx", xa, dur)}</circle>')
        b += txt(16, 114, "Lần b: chia theo thời gian", "currentColor", 13) + txt(X1, 114, "v_tb = ?", RED, 13, "end")
        b += txt(16, 134, "Nửa thời gian đầu: 12 km/h", BLUE, 12, "start", "400") + txt(16, 152, "Nửa thời gian sau: 24 km/h", ORG, 12, "start", "400")
        b += seg(X0, 174, X1, 174, "currentColor", 3) + tick(X0, 174) + tick(X1, 174)
        b += txt(X0, 198, "A", "currentColor", 13, "middle") + txt(X1, 198, "B", "currentColor", 13, "middle")
        b += (f'<circle cx="{xb[0]:.1f}" cy="174" r="6" fill="{GRN}" stroke="currentColor" stroke-width="1.6">{smil("cx", xb, dur)}</circle>')
        return fig("c13-1-0", "0 0 420 208", "Hai lần xe đạp điện đi từ A đến B dài 24 km, lần thứ nhất chia đôi quãng đường, lần thứ hai chia đôi thời gian",
                   b, "Mô phỏng: hai lần đi cùng xuất phát từ A, chạy nhanh 1200 lần (1 giờ thật = 3 giây).")
    # tĩnh: phần phân tích
    b += txt(16, 22, "a) Hai chặng có quãng đường bằng nhau", "currentColor", 13)
    b += seg(X0, 58, X1, 58, "currentColor", 3) + tick(X0, 58) + tick(xm, 58) + tick(X1, 58)
    b += txt((X0 + xm) / 2, 44, "12 km/h", BLUE, 13, "middle") + txt((xm + X1) / 2, 44, "24 km/h", ORG, 13, "middle")
    b += dim(p, "b", X0 + 2, 78, xm - 2, 78, "12 km", (X0 + xm) / 2, 98, "middle") + dim(p, "b", xm + 2, 78, X1 - 2, 78, "12 km", (xm + X1) / 2, 98, "middle")
    b += txt(16, 128, "b) Hai chặng có thời gian bằng nhau", "currentColor", 13)
    b += R(X0, 142, xm - X0, 26, BLUE, 2.4) + R(xm, 142, X1 - xm, 26, ORG, 2.4)
    b += txt((X0 + xm) / 2, 160, "12 km/h", BLUE, 13, "middle") + txt((xm + X1) / 2, 160, "24 km/h", ORG, 13, "middle")
    b += dim(p, "b", X0 + 2, 184, xm - 2, 184, "t/2", (X0 + xm) / 2, 204, "middle") + dim(p, "b", xm + 2, 184, X1 - 2, 184, "t/2", (xm + X1) / 2, 204, "middle")
    return fig("c13-1-2", "0 0 420 214", "Hai cách chia hành trình: chia theo quãng đường và chia theo thời gian",
               b, "Dữ kiện: ở câu a mỗi chặng dài 12 km ; ở câu b mỗi chặng kéo dài nửa tổng thời gian. " + NOTE)


# ───────────── Dạng 2 · ô tô từ A (60 km/h) gặp xe máy từ B (40 km/h), AB = 150 km ─────────────
def d2(kk):
    p = f"d2{kk}"; X0, X1 = 30, 390; PK = 2.4        # 150 km → 360 px
    b = defs(p)
    Y1, Y2 = (70, 118) if kk == 0 else (78, 128)
    if kk == 0:
        ts = [0.5 * k for k in range(5)]               # 0 … 2 h (dừng trước mốc 2,5 h để không lộ đáp án câu c)
        p1 = [(X0 + PK * 60 * t, Y1) for t in ts]
        p2 = [(X1 - PK * 40 * t, Y2) for t in ts]
        dur = 4.0                                      # 1 giờ thật = 2 giây
        b += seg(X0, Y1, X1, Y1, "currentColor", 2.4) + seg(X0, Y2, X1, Y2, "currentColor", 2.4)
        b += seg(X0, 40, X0, 134, GREY, 1.4, "5 4", .7) + seg(X1, 40, X1, 134, GREY, 1.4, "5 4", .7)
        b += txt(X0, 174, "A", "currentColor", 13, "middle") + txt(X1, 174, "B", "currentColor", 13, "middle")
        b += dim(p, "b", X0 + 4, 150, X1 - 4, 150, "", 0, 0) + txt(210, 144, "AB = 150 km", BLUE, 13, "middle")
        b += txt(16, 20, "Ô tô từ A, xe máy từ B, cùng lúc", "currentColor", 13) + txt(X1, 20, "gặp nhau: ?", RED, 13, "end")
        b += trk(p1, dur, xcar("60 km/h", BLUE)) + trk(p2, dur, moto("40 km/h", ORG))
        return fig("c13-2-0", "0 0 420 184", "Ô tô đi từ A về B và xe máy đi từ B về A, ngược chiều nhau",
                   b, "Mô phỏng: ô tô (xanh, 60 km/h) và xe máy (cam, 40 km/h) 1 giờ thật ứng với 2 giây mô phỏng.")
    b += seg(X0, Y1, X1, Y1, "currentColor", 2.4) + seg(X0, Y2, X1, Y2, "currentColor", 2.4)
    b += txt(X0, 172, "A", "currentColor", 13, "middle") + txt(X1, 172, "B", "currentColor", 13, "middle")
    K = 0.8                                            # px mỗi km/h, cùng k cho mọi vectơ vận tốc
    b += f'<g transform="translate({X0} {Y1})">{xcar()}</g>' + f'<g transform="translate({X1} {Y2})">{moto()}</g>'
    b += vec_luc("r", X0 + 24, Y1 - 12, 1, 0, 60, K, 3)[0] + txt(X0 + 24 + 60 * K + 6, Y1 - 8, "v₁ = 60 km/h", RED, 12)
    b += vec_luc("g", X1 - 24, Y2 - 12, -1, 0, 40, K, 3)[0] + txt(X1 - 24 - 40 * K - 6, Y2 - 8, "v₂ = 40 km/h", GRN, 12, "end")
    # trục toạ độ
    b += arrow(p, "b", X0, 152, X1 + 14, 152, 2) + txt(X1 + 16, 156, "x", BLUE, 13) + txt(X0 + 8, 146, "O ≡ A", BLUE, 12, "start", "400") + txt(X1 - 8, 146, "x₀₂ = 150 km", BLUE, 12, "end", "400")
    b += txt(16, 20, "Gốc O tại A, chiều dương từ A đến B", "currentColor", 13)
    return fig("c13-2-2", "0 0 420 180", "Trục toạ độ gốc tại A, ô tô đi theo chiều dương, xe máy đi ngược chiều dương",
               b, "Dữ kiện: ô tô có v > 0, xe máy có v < 0 ; hai xe xuất phát cùng lúc. Mũi tên vẽ đúng tỉ lệ độ lớn vận tốc.")


# ───────────── Dạng 3 · đoàn tàu L₁ = 180 m, 54 km/h; cầu S = 420 m ─────────────
def d3(kk):
    p = f"d3{kk}"; b = defs(p)
    if kk == 0:
        PX = 0.5                                       # px mỗi mét
        Lp, Sp = 180 * PX, 420 * PX
        bx0 = 110; bx1 = bx0 + Sp; Y = 110
        b += seg(16, Y, bx0, Y, "currentColor", 2.4) + seg(bx1, Y, 408, Y, "currentColor", 2.4)
        b += seg(bx0, Y + 3, bx1, Y + 3, "currentColor", 6) + seg(bx0 + 40, Y + 6, bx0 + 40, Y + 36, "currentColor", 4) + seg(bx1 - 40, Y + 6, bx1 - 40, Y + 36, "currentColor", 4)
        b += f'<path d="M{bx0 + 40},{Y + 36} Q{(bx0 + bx1) / 2},{Y + 30} {bx1 - 40},{Y + 36}" fill="none" stroke="{BLUE}" stroke-width="1.6" opacity=".6"/>'
        b += dim(p, "b", bx0, Y + 54, bx1, Y + 54, "", 0, 0) + txt((bx0 + bx1) / 2, Y + 72, "cầu dài S = 420 m", BLUE, 13, "middle")
        b += txt(16, 20, "Tàu dài L₁ = 180 m, v = 54 km/h", "currentColor", 13) + txt(408, 20, "t = ?", RED, 13, "end")
        b += trk([(bx0 - Lp, Y), (bx0 - Lp + (Lp + Sp), Y)], 4, train(Lp))
        return fig("c13-3-0", "0 0 420 196", "Đoàn tàu dài 180 mét chạy qua cây cầu dài 420 mét, tính từ lúc đầu tàu lên cầu đến lúc đuôi tàu rời cầu",
                   b, "Mô phỏng: từ lúc đầu tàu lên cầu đến lúc đuôi tàu rời cầu (1 s mô phỏng ứng với 10 s thật). Chiều dài tàu và cầu vẽ đúng tỉ lệ.")
    PX = 0.4
    Lp, Sp = 180 * PX, 420 * PX
    bx0 = 120; bx1 = bx0 + Sp; Y = 70
    b += seg(16, Y, bx0, Y, "currentColor", 2.4) + seg(bx1, Y, 408, Y, "currentColor", 2.4) + seg(bx0, Y + 3, bx1, Y + 3, "currentColor", 6)
    b += f'<g transform="translate({bx0 - Lp} {Y})">{train(Lp, 18, "currentColor", 1)}</g>'
    b += f'<g transform="translate({bx1} {Y})">{train(Lp, 18, "currentColor", .4)}</g>'
    b += txt(bx0 - Lp / 2, Y - 26, "L₁", RED, 13, "middle") + txt((bx0 + bx1) / 2, Y + 28, "S", BLUE, 13, "middle") + txt(bx1 + Lp / 2, Y - 26, "L₁", RED, 13, "middle")
    b += dim(p, "r", bx0, Y - 44, bx1 + Lp, Y - 44, "", 0, 0) + txt(210, 16, "đầu tàu đi được quãng đường nào?", RED, 12, "middle", "400")
    # hai tàu ngược chiều: vectơ vận tốc tỉ lệ (0,9 px mỗi km/h)
    Y2 = 160; PX2 = 0.4
    L1p, L2p = 180 * PX2, 140 * PX2
    t1x = 20; t2x = 290
    b += seg(16, Y2, 408, Y2, "currentColor", 2.4)
    b += f'<g transform="translate({t1x} {Y2})">{train(L1p, 18)}</g>' + f'<g transform="translate({t2x} {Y2})">{train(L2p, 18)}</g>'
    b += vec_luc("r", t1x + L1p + 4, Y2 - 9, 1, 0, 54, 0.9, 3)[0] + txt(t1x + L1p + 4 + 54 * .45, Y2 + 20, "54 km/h", RED, 12, "middle")
    b += vec_luc("g", t2x - 4, Y2 - 9, -1, 0, 36, 0.9, 3)[0] + txt(t2x - 4 - 36 * .45, Y2 + 20, "36 km/h", GRN, 12, "middle")
    b += txt(t1x + L1p / 2, Y2 - 26, "L₁", RED, 13, "middle") + txt(t2x + L2p / 2, Y2 - 26, "L₂ = 140 m", GRN, 13, "middle")
    b += txt(16, 118, "Hai tàu ngược chiều gặp nhau", "currentColor", 13)
    return fig("c13-3-2", "0 0 420 186", "Đoàn tàu qua cầu và hai đoàn tàu ngược chiều gặp nhau",
               b, "Dữ kiện: tàu có chiều dài nên phải chọn điểm chuẩn (đầu tàu). Mũi tên vận tốc vẽ đúng tỉ lệ độ lớn ; chiều dài tàu và cầu vẽ đúng tỉ lệ.")


# ───────────── Dạng 4 · canô trên sông AB = 90 km ─────────────
def d4(kk):
    p = f"d4{kk}"; X0, X1 = 30, 390; b = defs(p)
    if kk == 0:
        def lane(y, label):
            r = R(X0 - 14, y - 22, X1 - X0 + 28, 50, GREY, 1.4, "none", 6, "", .8)
            r += field_line(70, y + 14, 120, y + 14, BLUE, 1.6, "6 4", 9) + field_line(250, y + 14, 300, y + 14, BLUE, 1.6, "6 4", 9)
            return r + txt(X0 - 14, y - 30, label, "currentColor", 13) + txt(185, y + 18, "dòng nước", BLUE, 12, "middle", "400")
        b += lane(60, "Lượt xuôi dòng: A → B") + lane(136, "Lượt ngược dòng: B → A")
        ts = list(range(6))                              # 0 … 5 h
        pa = [(X0 + 360 * min(t, 3) / 3, 56) for t in ts]
        pb = [(X1 - 360 * t / 5, 132) for t in ts]
        boat = '<path d="M-14,-6 L14,-6 L8,6 L-8,6 Z" fill="' + GRN + '" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>'
        b += trk(pa, 6, boat) + trk(pb, 6, boat)
        b += txt(X0, 204, "A", "currentColor", 13, "middle") + txt(X1, 204, "B", "currentColor", 13, "middle")
        b += dim(p, "b", X0 + 4, 186, X1 - 4, 186, "", 0, 0) + txt(210, 180, "AB = 90 km", BLUE, 13, "middle")
        return fig("c13-4-0", "0 0 420 212", "Canô đi xuôi dòng từ A đến B mất 3 giờ rồi đi ngược dòng từ B về A mất 5 giờ",
                   b, "Mô phỏng: hai lượt chạy cùng lúc, nhanh 3000 lần (1 giờ thật = 1,2 giây). Nét đứt chỉ chiều dòng nước.")
    # tĩnh: thanh thời gian cùng thang
    K = 50                                             # px mỗi giờ
    b += txt(16, 22, "Cùng quãng đường AB, hai thời gian khác nhau", "currentColor", 13)
    b += R(X0, 40, 3 * K, 24, ORG, 2.4) + txt(X0 + 3 * K / 2, 57, "xuôi 3 h", ORG, 13, "middle")
    b += R(X0, 78, 5 * K, 24, BLUE, 2.4) + txt(X0 + 5 * K / 2, 95, "ngược 5 h", BLUE, 13, "middle")
    b += R(X0, 116, 7 * K, 24, GRN, 2.4, "none", 0, "6 4") + txt(X0 + 7 * K / 2, 133, "bè trôi: t = ?", GRN, 13, "middle")
    b += txt(16, 168, "Bè không có máy: chỉ dòng nước đưa đi", "currentColor", 12, "start", "400")
    b += txt(16, 186, "Phao rơi cũng chỉ trôi theo dòng nước", "currentColor", 12, "start", "400")
    return fig("c13-4-2", "0 0 420 196", "Thanh thời gian: xuôi dòng 3 giờ, ngược dòng 5 giờ, bè trôi chưa biết",
               b, "Dữ kiện: thời gian xuôi và ngược cho cùng một quãng đường 90 km. Độ dài thanh bè trôi chỉ là chỗ trống, chưa theo đáp số.")


# ───────────── Dạng 5 · đồ thị x–t của xe A và xe B ─────────────
def d5_graph(p):
    OX, OY, KT, KX = 56, 214, 75, 1.3                  # px mỗi giờ; px mỗi km
    b = ""
    for t in range(5):
        b += seg(OX + KT * t, OY, OX + KT * t, OY - 150 * KX, GREY, 1, "4 4", .45) + txt(OX + KT * t, OY + 18, str(t), "currentColor", 12, "middle", "400")
    for x in range(0, 151, 30):
        b += seg(OX, OY - KX * x, OX + 4 * KT + 6, OY - KX * x, GREY, 1, "4 4", .45) + txt(OX - 8, OY - KX * x + 4, str(x), "currentColor", 12, "end", "400")
    b += arrow(p, "g", OX, OY, OX + 4 * KT + 26, OY, 2) + txt(OX + 4 * KT + 28, OY + 5, "t (h)", GRN, 12)
    b += arrow(p, "g", OX, OY, OX, OY - 150 * KX - 24, 2) + txt(OX + 6, OY - 150 * KX - 28, "x (km)", GRN, 12)
    A = [(0, 0), (1, 60), (1.5, 60), (3, 150)]
    B = [(0, 120), (4, 0)]
    b += poly([(OX + KT * t, OY - KX * x) for t, x in A], ORG, 3) + poly([(OX + KT * t, OY - KX * x) for t, x in B], BLUE, 3)
    for t, x in A: b += dot(OX + KT * t, OY - KX * x, 4, ORG)
    for t, x in B: b += dot(OX + KT * t, OY - KX * x, 4, BLUE)
    b += txt(OX + KT * 3 + 8, OY - KX * 150 + 14, "xe A", ORG, 13) + txt(OX + 10, OY - KX * 120 - 8, "xe B", BLUE, 13)
    return b

def d5(kk):
    p = f"d5{kk}"; b = defs(p)
    if kk == 0:
        g = fig("c13-5-g", "0 0 420 246", "Đồ thị toạ độ – thời gian của xe A và xe B",
                defs(p + "g") + d5_graph(p + "g"), "Đồ thị x–t của hai xe. Mỗi ô lưới: 1 h theo trục t, 30 km theo trục x.")
        X0, X1 = 30, 390; PK = 360 / 150; Y = 70
        ts = [0.25 * k for k in range(13)]              # 0 … 3 h
        def xa(t): return 60 * t if t <= 1 else (60 if t <= 1.5 else 60 + 60 * (t - 1.5))
        def xb(t): return 120 - 30 * t
        pa = [(X0 + PK * xa(t), Y) for t in ts]
        pb = [(X0 + PK * xb(t), Y + 34) for t in ts]
        s = seg(X0, Y, X1, Y, "currentColor", 2.4) + seg(X0, Y + 34, X1, Y + 34, "currentColor", 2.4)
        s += txt(X0, Y + 62, "O", "currentColor", 13, "middle") + txt(X1, Y + 62, "x = 150 km", "currentColor", 12, "end", "400")
        s += trk(pa, 4.5, dotg("A", ORG)) + trk(pb, 4.5, dotg("B", BLUE))
        s += txt(16, 20, "Chuyển động của hai xe theo đồ thị", "currentColor", 13) + txt(X1, 20, "gặp nhau: ?", RED, 13, "end")
        sim = fig("c13-5-0", "0 0 420 140", "Hai xe A và B chuyển động trên cùng một đường thẳng theo đồ thị", s,
                  "Mô phỏng: 3 giờ đầu, nhanh 2400 lần (1 giờ thật = 1,5 giây). Xe A dừng nghỉ trong lúc xe B vẫn chạy.")
        return g + sim
    # tĩnh: độ dốc từng đoạn (không ghi số), kèm ba giai đoạn
    OX, OY, KT, KX = 56, 214, 75, 1.3
    b += d5_graph(p)
    b += txt(OX + KT * 1.25, OY - KX * 60 - 8, "nghỉ", ORG, 12, "middle", "400")
    b += txt(OX + KT * 0.5, OY - KX * 20, "giai đoạn 1", ORG, 12, "start", "400")
    b += txt(OX + KT * 1.7, OY - KX * 140, "giai đoạn 3", ORG, 12, "end", "400")
    b += txt(OX + KT * 2.9, OY - KX * 48, "xe B đi xuống", BLUE, 12, "start", "400")
    return fig("c13-5-2", "0 0 420 246", "Đồ thị x–t: ba giai đoạn của xe A và đoạn đi xuống của xe B",
               b, "Dữ kiện: độ dốc mỗi đoạn là vận tốc ; đoạn nằm ngang là đứng yên ; đoạn đi xuống là chuyển động ngược chiều dương. Giao điểm hai đường là lúc và nơi gặp nhau.")


# ───────────── Dạng 6 · bơi qua sông rộng 96 m ─────────────
def d6(kk):
    p = f"d6{kk}"; b = defs(p)
    if kk == 0:
        XA = 150; YA, YB = 148, 52                       # A bờ dưới, B bờ trên, 96 m ↔ 96 px
        b += seg(16, YB, 408, YB, "currentColor", 3) + seg(16, YA, 408, YA, "currentColor", 3)
        for y in (78, 100, 122):
            b += field_line(236, y, 296, y, BLUE, 1.6, "6 4", 9)
        b += txt(250, 66, "dòng nước", BLUE, 12, "start", "400")
        b += circ(XA, YA, 4, "currentColor", 2, "currentColor") + txt(XA - 12, YA + 18, "A", "currentColor", 13, "middle")
        b += circ(XA, YB, 4, "currentColor", 2, "currentColor") + txt(XA - 12, YB - 8, "B", "currentColor", 13, "middle")
        b += dim(p, "o", XA - 44, YA - 3, XA - 44, YB + 3, "", 0, 0) + txt(XA - 50, (YA + YB) / 2 + 4, "AB = 96 m", ORG, 13, "end")
        b += seg(XA, YA, XA, YB, GREY, 1.4, "5 4", .8)
        b += trk([(XA, YA), (XA, YB)], 4, dotg("", GRN))
        b += txt(16, 22, "v_{bơi} = 2,0 m/s (so với nước)", "currentColor", 13) + txt(16, 40, "v_{nước} = 1,2 m/s", BLUE, 13) + txt(408, 22, "α = ?", RED, 13, "end")
        return fig("c13-6-0", "0 0 420 176", "Người bơi sang đúng điểm B ở bờ đối diện, nước chảy song song bờ",
                   b, "Mô phỏng: người đi thẳng từ A đến B (1 s mô phỏng ứng với 15 s thật). Hình không vẽ hướng đầu người bơi.")
    # tĩnh: cách ghép vectơ, vẽ đúng tỉ lệ độ lớn của đề (1,2 : 1,6 : 2,0 = 3 : 4 : 5; 24 px mỗi 0,4 m/s)
    ox, oy = 210, 150
    b += txt(16, 22, "Ghép vectơ vận tốc", "currentColor", 13)
    b += arrow(p, "r", ox, oy, ox - 72, oy - 96, 3) + txt(ox - 44, oy - 50, "v_{bơi}", RED, 13, "end")
    b += arrow(p, "b", ox - 72, oy - 96, ox, oy - 96, 3) + txt(ox - 36, oy - 106, "v_{nước}", BLUE, 13, "middle")
    b += arrow(p, "g", ox, oy, ox, oy - 96, 3) + txt(ox + 8, oy - 50, "v_{thực}", GRN, 13)
    b += seg(ox - 10, oy - 96, ox - 10, oy - 86, GREY, 1.4) + seg(ox - 10, oy - 86, ox, oy - 86, GREY, 1.4)
    b += arc(ox, oy, 30, 90, 90 + math.degrees(math.atan2(72, 96)), RED, 1.8) + txt(ox - 22, oy - 38, "α", RED, 13)
    b += txt(ox + 40, oy - 96, "v_{thực} = v_{bơi} + v_{nước}", "currentColor", 12, "start", "400")
    b += txt(ox + 40, oy - 76, "v_{thực} ⟂ bờ", "currentColor", 12, "start", "400")
    b += seg(16, oy + 6, 408, oy + 6, "currentColor", 2.4) + txt(408, oy + 24, "bờ sông", "currentColor", 12, "end", "400")
    return fig("c13-6-2", "0 0 420 182", "Tam giác vận tốc: vận tốc thực vuông góc với bờ bằng tổng của vận tốc bơi và vận tốc dòng nước",
               b, "Các mũi tên vẽ đúng tỉ lệ độ lớn các vận tốc trong đề (tam giác vận tốc có ba cạnh tỉ lệ 3 : 4 : 5).")


BUILD = [d1, d2, d3, d4, d5, d6]


# ═════════════ ĐỀ CÁC DẠNG (dễ → khó) ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Tốc độ trung bình: chia theo quãng đường, chia theo thời gian, đi rồi về",
      topic="Tốc độ trung bình và vận tốc trung bình",
      problem_html=r"""<p>Một xe đạp điện chạy trên đoạn đường thẳng $AB$ dài $24\ \text{km}$.</p><ol type="a"><li>Nửa quãng đường đầu xe chạy với tốc độ $12\ \text{km/h}$, nửa quãng đường sau chạy với tốc độ $24\ \text{km/h}$. Tính tốc độ trung bình của xe trên cả đoạn $AB$.</li><li>Ở một lần đi khác, xe chạy $12\ \text{km/h}$ trong nửa thời gian đầu và $24\ \text{km/h}$ trong nửa thời gian sau. Tính tốc độ trung bình của xe trên đoạn $AB$ trong lần đi này.</li><li>Quay lại lần đi ở câu a: đến $B$ xe quay về $A$ theo đúng đường cũ, lượt về cũng mất thời gian bằng lượt đi. Tính tốc độ trung bình và độ lớn vận tốc trung bình trên cả hành trình đi và về.</li></ol>"""),
 dict(label="Dạng 2 · Trung bình · Hai xe chuyển động ngược chiều: thời điểm gặp, vị trí gặp, lúc cách nhau một khoảng cho trước",
      topic="Tổng hợp vận tốc, tính tương đối của chuyển động",
      problem_html=r"""<p>Hai thành phố $A$ và $B$ cách nhau $150\ \text{km}$. Lúc $6$ giờ, một ô tô xuất phát từ $A$ đi về $B$ với tốc độ $60\ \text{km/h}$. Cùng lúc đó, một xe máy xuất phát từ $B$ đi về $A$ với tốc độ $40\ \text{km/h}$. Coi hai xe chuyển động thẳng đều.</p><ol type="a"><li>Hai xe gặp nhau lúc mấy giờ? Chỗ gặp cách $A$ bao nhiêu kilômét?</li><li>Lúc mấy giờ hai xe cách nhau $30\ \text{km}$? (Xét cả hai khả năng.)</li><li>Khi ô tô đến $B$, xe máy còn cách $A$ bao nhiêu kilômét?</li></ol>"""),
 dict(label="Dạng 3 · Trung bình · Vật có chiều dài: đoàn tàu qua người, qua cầu, gặp và vượt đoàn tàu khác",
      topic="Tổng hợp vận tốc, tính tương đối của chuyển động",
      problem_html=r"""<p>Một đoàn tàu dài $L_1=180\ \text{m}$ chạy đều với tốc độ $54\ \text{km/h}$.</p><ol type="a"><li>Tàu chạy qua một người đứng yên bên đường mất bao lâu?</li><li>Tàu chạy qua một cây cầu dài $S=420\ \text{m}$ mất bao lâu (tính từ lúc đầu tàu lên cầu đến lúc đuôi tàu rời cầu)?</li><li>Tàu gặp một đoàn tàu thứ hai dài $L_2=140\ \text{m}$ chạy ngược chiều trên đường ray song song với tốc độ $36\ \text{km/h}$. Tính thời gian từ lúc hai đầu tàu ngang nhau đến lúc hai đuôi tàu rời nhau.</li><li>Nếu đoàn tàu thứ hai chạy cùng chiều, ở phía trước, với tốc độ $36\ \text{km/h}$ thì tàu thứ nhất vượt qua nó mất bao lâu (từ lúc đầu tàu thứ nhất ngang đuôi tàu thứ hai đến lúc đuôi tàu thứ nhất ngang đầu tàu thứ hai)?</li></ol>"""),
 dict(label="Dạng 4 · Khó · Chuyển động trên dòng nước: xuôi dòng, ngược dòng, bè trôi, phao rơi",
      topic="Tổng hợp vận tốc, tính tương đối của chuyển động",
      problem_html=r"""<p>Hai bến $A$ và $B$ trên một khúc sông thẳng cách nhau $90\ \text{km}$. Một canô chạy xuôi dòng từ $A$ đến $B$ mất $3$ giờ và chạy ngược dòng từ $B$ về $A$ mất $5$ giờ. Tốc độ riêng của canô (so với nước) và tốc độ dòng nước đều không đổi.</p><ol type="a"><li>Tính tốc độ của dòng nước và tốc độ riêng của canô.</li><li>Một chiếc bè thả trôi theo dòng nước từ $A$ thì mất bao lâu để tới $B$?</li><li>Một lần khác, canô đang chạy ngược dòng thì làm rơi một chiếc phao nổi (phao trôi theo dòng nước). Sau $20$ phút người lái mới phát hiện, lập tức quay đầu chạy xuôi dòng (giữ nguyên tốc độ riêng) để vớt phao. Tính thời gian từ lúc quay đầu đến lúc vớt được phao và quãng đường phao đã trôi kể từ chỗ rơi.</li></ol>"""),
 dict(label="Dạng 5 · Khó · Đọc đồ thị toạ độ – thời gian: vận tốc từ độ dốc, phương trình từng giai đoạn, điểm gặp nhau",
      topic="Đọc đồ thị độ dịch chuyển – thời gian",
      problem_html=r"""<p>Hình dưới là đồ thị toạ độ – thời gian $(x\text{–}t)$ của hai xe $A$ và $B$ chuyển động trên cùng một đường thẳng ($x$ tính bằng $\text{km}$, $t$ tính bằng giờ).</p><ul><li>Xe $A$: xuất phát từ $x=0$, lúc $t=1\ \text{h}$ ở $x=60\ \text{km}$, nghỉ từ $t=1\ \text{h}$ đến $t=1{,}5\ \text{h}$, rồi đi tiếp thẳng đều đến $x=150\ \text{km}$ lúc $t=3\ \text{h}$.</li><li>Xe $B$: xuất phát từ $x=120\ \text{km}$ lúc $t=0$, chuyển động thẳng đều về phía gốc toạ độ và tới $x=0$ lúc $t=4\ \text{h}$.</li></ul><ol type="a"><li>Tính tốc độ của xe $A$ ở từng giai đoạn và của xe $B$. Nói rõ xe $B$ chuyển động theo chiều nào.</li><li>Viết phương trình toạ độ của mỗi xe (xe $A$ theo từng giai đoạn).</li><li>Hai xe gặp nhau lúc nào và ở đâu?</li></ol>"""),
 dict(label="Dạng 6 · Nâng cao · Tổng hợp vận tốc: bơi qua sông sang đúng điểm đối diện và bơi vuông góc bờ",
      topic="Tổng hợp vận tốc, tính tương đối của chuyển động",
      problem_html=r"""<p>Một người muốn bơi từ điểm $A$ ở bờ này sang điểm $B$ ở bờ đối diện, $AB$ vuông góc với bờ và dài $96\ \text{m}$. Tốc độ bơi của người so với nước là $2{,}0\ \text{m/s}$. Nước chảy song song với bờ, tốc độ $1{,}2\ \text{m/s}$. Coi các tốc độ không đổi.</p><ol type="a"><li>Người đó phải bơi theo hướng hợp với $AB$ một góc $\alpha$ có $\sin\alpha$ bằng bao nhiêu và chếch về phía nào để sang đúng $B$? Tính thời gian bơi.</li><li>Nếu người đó luôn bơi vuông góc với bờ thì mất bao lâu để sang đến bờ bên kia và bị nước đẩy trôi xuống phía dưới $B$ một đoạn bao nhiêu?</li><li>Cách bơi nào đưa người sang bờ bên kia nhanh hơn? Cách bơi nào đưa người đến đúng $B$?</li></ol>"""),
]

# ═════════════ BẢNG PHÂN TÍCH ĐỀ ═════════════
ANALYSIS = [
 # Dạng 1
 [(r'"đoạn đường thẳng $AB$ dài $24$ km"', r"$AB=24$ km", r"Tốc độ trung bình $v_{tb}=\dfrac{s_{\text{tổng}}}{t_{\text{tổng}}}$ ; ⚠ không phải trung bình cộng các tốc độ"),
  (r'"nửa quãng đường đầu $12$ km/h, nửa sau $24$ km/h"', r"$s_1=s_2=12$ km ; $v_1=12$, $v_2=24$ km/h", r"$t_i=\dfrac{s_i}{v_i}$ ; ⚠ hai chặng dài bằng nhau nên thời gian không bằng nhau"),
  (r'"tốc độ trung bình trên cả đoạn $AB$" (câu a)', r"Cần $v_{tb}$", r"$v_{tb}=\dfrac{s_{\text{tổng}}}{t_{\text{tổng}}}$"),
  (r'"nửa thời gian đầu $12$ km/h, nửa thời gian sau $24$ km/h"', r"$t_1=t_2=\dfrac{t}{2}$ ; $v_1=12$, $v_2=24$ km/h", r"$s_i=v_it_i$ ; ⚠ gọi tổng thời gian là $t$ rồi cộng quãng đường hai chặng"),
  (r'"quay về $A$ theo đúng đường cũ … thời gian bằng lượt đi"', r"Đi và về đều dài $24$ km, cùng thời gian", r"⚠ Tốc độ trung bình dùng tổng quãng đường ; vận tốc trung bình dùng độ dịch chuyển (về đúng chỗ xuất phát thì bằng $0$)"),
  (r'"tốc độ trung bình và độ lớn vận tốc trung bình"', r"Cần $v_{tb}$ và $|\vec v_{tb}|$ cả hành trình", r"$v_{tb}=\dfrac{s}{t}$ ; $|\vec v_{tb}|=\dfrac{|\Delta x|}{t}$")],
 # Dạng 2
 [(r'"$A$ và $B$ cách nhau $150$ km"', r"$AB=150$ km", r"Gốc $O$ tại $A$, chiều dương từ $A$ đến $B$ : $x=x_0+vt$"),
  (r'"lúc $6$ giờ … ô tô từ $A$ … $60$ km/h"', r"$x_{01}=0$ ; $v_1=+60$ km/h", r"$x_1=60t$"),
  (r'"cùng lúc … xe máy từ $B$ … $40$ km/h"', r"$x_{02}=150$ km ; $v_2=-40$ km/h", r"⚠ Xe máy đi ngược chiều dương nên $v_2\lt0$ ; hai xe cùng mốc thời gian : $x_2=150-40t$"),
  (r'"gặp nhau lúc mấy giờ, cách $A$ bao nhiêu"', r"Cần $t$ và $x$", r"Gặp nhau khi $x_1=x_2$"),
  (r'"cách nhau $30$ km"', r"$d=30$ km", r"$d=|x_1-x_2|$ ; ⚠ có hai khả năng : chưa gặp ($x_2\gt x_1$) và đã qua nhau ($x_1\gt x_2$)"),
  (r'"khi ô tô đến $B$, xe máy còn cách $A$"', r"Điều kiện $x_1=150$", r"Tìm $t$ lúc $x_1=150$ rồi tính $x_2$ ; khoảng cách tới $A$ chính là $x_2$")],
 # Dạng 3
 [(r'"đoàn tàu dài $L_1=180$ m … $54$ km/h"', r"$L_1=180$ m ; $v_1=54$ km/h", r"⚠ Đổi cùng hệ đơn vị : $54$ km/h $=\dfrac{54}{3{,}6}$ m/s ; chọn đầu tàu làm điểm chuẩn"),
  (r'"qua một người đứng yên"', r"Người coi như một điểm", r"Đầu tàu phải đi đúng chiều dài tàu : $s=L_1$"),
  (r'"cầu dài $S=420$ m … từ lúc đầu tàu lên cầu đến lúc đuôi tàu rời cầu"', r"$S=420$ m", r"⚠ Đầu tàu đi từ đầu cầu đến lúc đuôi tàu rời cầu : $s=L_1+S$"),
  (r'"tàu thứ hai dài $140$ m ngược chiều $36$ km/h"', r"$L_2=140$ m ; $v_2=36$ km/h", r"Ngược chiều : $v_{\text{tđ}}=v_1+v_2$ ; $s_{\text{tđ}}=L_1+L_2$"),
  (r'"từ lúc hai đầu tàu ngang nhau đến lúc hai đuôi tàu rời nhau"', r"Mốc đầu và mốc cuối của sự gặp nhau", r"$t=\dfrac{L_1+L_2}{v_1+v_2}$"),
  (r'"cùng chiều … tàu thứ nhất vượt qua"', r"Cùng chiều, $v_1\gt v_2$", r"⚠ Cùng chiều : $v_{\text{tđ}}=v_1-v_2$ (chỉ vượt được khi $v_1\gt v_2$) ; $s_{\text{tđ}}=L_1+L_2$")],
 # Dạng 4
 [(r'"khúc sông thẳng $AB=90$ km"', r"$s=90$ km", r"$v=\dfrac{s}{t}$ trên mỗi lượt"),
  (r'"xuôi dòng mất $3$ giờ, ngược dòng mất $5$ giờ"', r"$t_x=3$ h ; $t_{ng}=5$ h", r"$v_x=v_t+v_n=\dfrac{s}{t_x}$ ; $v_{ng}=v_t-v_n=\dfrac{s}{t_{ng}}$"),
  (r'"tốc độ riêng … và dòng nước không đổi"', r"$v_t$ và $v_n$ không đổi", r"⚠ $v_t$ là tốc độ so với nước ; $v_n=\dfrac{v_x-v_{ng}}{2}$"),
  (r'"bè thả trôi theo dòng nước"', r"Tốc độ bè $=v_n$", r"$t=\dfrac{s}{v_n}$ ; ⚠ bè không có tốc độ riêng"),
  (r'"phao nổi, trôi theo dòng nước"', r"Phao chuyển động như dòng nước", r"⚠ Trong hệ quy chiếu gắn với nước, phao đứng yên"),
  (r'"sau $20$ phút mới phát hiện, quay đầu, giữ nguyên tốc độ riêng"', r"$t_1=20$ phút", r"Canô rời phao và quay lại với cùng tốc độ riêng $v_t$ nên $t_2=t_1$"),
  (r'"quãng đường phao đã trôi kể từ chỗ rơi"', r"Cần $s_{phao}$", r"$s_{phao}=v_n(t_1+t_2)$")],
 # Dạng 5
 [(r'"đồ thị $x$–$t$ của hai xe"', r"Đọc toạ độ và thời gian trên lưới", r"Độ dốc đoạn thẳng : $v=\dfrac{\Delta x}{\Delta t}$"),
  (r'"xe $A$ … nghỉ từ $1$ h đến $1{,}5$ h"', r"Đoạn nằm ngang", r"⚠ Đoạn nằm ngang : $\Delta x=0$ nên $v=0$ ; mỗi phương trình chỉ đúng trong khoảng thời gian của giai đoạn đó"),
  (r'"đi tiếp thẳng đều đến $x=150$ km lúc $t=3$ h"', r"$(1{,}5\ \text{h};60\ \text{km})\to(3\ \text{h};150\ \text{km})$", r"$x=x_0+v(t-t_0)$ với mốc là điểm đầu giai đoạn"),
  (r'"xe $B$ … $120$ km … về gốc … $t=4$ h"', r"$(0;120)\to(4;0)$", r"⚠ Đồ thị đi xuống : $v\lt0$ (ngược chiều dương), tốc độ là $|v|$"),
  (r'"viết phương trình toạ độ"', r"Cần $x_A(t)$ từng giai đoạn, $x_B(t)$", r"$x=x_0+v(t-t_0)$"),
  (r'"gặp nhau lúc nào, ở đâu"', r"Cần $t_g$, $x_g$", r"Giao điểm : $x_A=x_B$ ; ⚠ nghiệm phải thuộc khoảng thời gian của giai đoạn đang xét")],
 # Dạng 6
 [(r'"sông … $AB$ vuông góc với bờ, $AB=96$ m"', r"$d=96$ m", r"Thời gian sang bờ $t=\dfrac{d}{v_\perp}$ với $v_\perp$ là thành phần vận tốc vuông góc bờ"),
  (r'"tốc độ bơi so với nước $2{,}0$ m/s"', r"$v_b=2{,}0$ m/s (so với nước)", r"Quy tắc cộng : $\vec v_{\text{thực}}=\vec v_b+\vec v_n$"),
  (r'"nước chảy song song với bờ $1{,}2$ m/s"', r"$v_n=1{,}2$ m/s", r"⚠ Nước chỉ đẩy dọc bờ, không giúp hay cản việc sang bờ"),
  (r'"sang đúng $B$"', r"$\vec v_{\text{thực}}\perp$ bờ", r"⚠ Thành phần dọc bờ phải triệt tiêu : $v_b\sin\alpha=v_n$ ; $v_{\text{thực}}=\sqrt{v_b^2-v_n^2}$"),
  (r'"bơi vuông góc với bờ"', r"Hướng bơi $\perp$ bờ", r"$t=\dfrac{d}{v_b}$ ; trôi dọc bờ $\ell=v_nt$"),
  (r'"cách nào nhanh hơn / đến đúng $B$"', r"So hai thời gian và vị trí tới", r"So sánh $t_a$ với $t_b$ ; chỉ cách a tới đúng $B$")],
]

# ═════════════ LỜI GIẢI (mỗi bước một khối, mỗi công thức một dòng) ═════════════
R1 = [r"<strong>Khái niệm:</strong> tốc độ trung bình là quãng đường đã đi chia thời gian đi ; vận tốc trung bình là độ dịch chuyển chia thời gian.",
      r"<strong>Công thức:</strong> $v_{tb}=\dfrac{s_{\text{tổng}}}{t_{\text{tổng}}}$ ; $t_i=\dfrac{s_i}{v_i}$ ; $s_i=v_it_i$.",
      r"Chia đều quãng đường : $v_{tb}=\dfrac{2v_1v_2}{v_1+v_2}$ · Chia đều thời gian : $v_{tb}=\dfrac{v_1+v_2}{2}$.",
      r"⚠ <strong>Điều kiện:</strong> trung bình cộng các tốc độ chỉ đúng khi các chặng có thời gian bằng nhau ; đi rồi về đúng chỗ cũ thì vận tốc trung bình bằng $0$."]
R2 = [r"<strong>Khái niệm:</strong> toạ độ $x$ tính từ gốc $O$ ; vật chuyển động thẳng đều có $x=x_0+vt$ ($v\gt0$ theo chiều dương, $v\lt0$ ngược chiều dương).",
      r"<strong>Định luật:</strong> hai vật gặp nhau khi toạ độ bằng nhau $x_1=x_2$ ; khoảng cách giữa chúng $d=|x_1-x_2|$.",
      r"<strong>Công thức:</strong> $x_1=v_1t$ ; $x_2=x_{02}-v_2t$ (xe thứ hai đi ngược chiều dương).",
      r"⚠ <strong>Điều kiện:</strong> hai xe cùng mốc thời gian ; $d=30$ có hai nghiệm (chưa gặp và đã qua nhau)."]
R3 = [r"<strong>Khái niệm:</strong> vật có kích thước đáng kể thì chọn một điểm chuẩn (đầu tàu) ; quãng đường điểm chuẩn đi được là chiều dài thực của sự dịch chuyển.",
      r"<strong>Công thức:</strong> $s=vt$ ; qua vật đứng yên : $s=L_1$ ; qua cầu : $s=L_1+S$ ; hai tàu : $t=\dfrac{L_1+L_2}{v_{\text{tđ}}}$.",
      r"Ngược chiều : $v_{\text{tđ}}=v_1+v_2$ · Cùng chiều : $v_{\text{tđ}}=v_1-v_2$.",
      r"⚠ <strong>Điều kiện:</strong> đổi tốc độ ra m/s khi chiều dài tính bằng mét ; xác định đúng mốc bắt đầu và mốc kết thúc."]
R4 = [r"<strong>Khái niệm:</strong> $v_t$ là tốc độ canô so với nước, $v_n$ là tốc độ dòng nước so với bờ.",
      r"<strong>Định luật:</strong> cộng vận tốc : xuôi dòng $v_x=v_t+v_n$ · ngược dòng $v_{ng}=v_t-v_n$.",
      r"<strong>Công thức:</strong> $v_n=\dfrac{v_x-v_{ng}}{2}$ ; $v_t=\dfrac{v_x+v_{ng}}{2}$ ; bè trôi : $t=\dfrac{s}{v_n}$.",
      r"⚠ <strong>Điều kiện:</strong> $v_t\gt v_n$ mới ngược dòng được ; vật trôi theo dòng đứng yên trong hệ quy chiếu gắn với nước."]
R5 = [r"<strong>Khái niệm:</strong> đồ thị $x$–$t$ : độ dốc là vận tốc ; đoạn nằm ngang là đứng yên ; đoạn đi xuống là chuyển động ngược chiều dương.",
      r"<strong>Công thức:</strong> $v=\dfrac{\Delta x}{\Delta t}$ ; $x=x_0+v(t-t_0)$ với $(t_0;x_0)$ là điểm đầu giai đoạn.",
      r"Hai xe gặp nhau khi $x_A=x_B$ (giao điểm của hai đường).",
      r"⚠ <strong>Điều kiện:</strong> mỗi phương trình chỉ đúng trong khoảng thời gian của giai đoạn đó ; nghiệm nằm ngoài khoảng thì loại."]
R6 = [r"<strong>Khái niệm:</strong> vận tốc của người so với bờ là tổng vectơ của vận tốc bơi (so với nước) và vận tốc dòng nước.",
      r"<strong>Định luật:</strong> $\vec v_{\text{thực}}=\vec v_b+\vec v_n$ ; hai chuyển động thành phần độc lập với nhau.",
      r"<strong>Công thức:</strong> sang đúng $B$ : $v_b\sin\alpha=v_n$, $v_{\text{thực}}=\sqrt{v_b^2-v_n^2}$ ; thời gian $t=\dfrac{d}{v_\perp}$.",
      r"⚠ <strong>Điều kiện:</strong> chỉ thành phần vuông góc bờ đưa người sang bờ ; nước chảy dọc bờ chỉ làm trôi người, không đổi thời gian sang bờ."]

SOLS = [
 sol(R1, [
  ("Thời gian đi hết $AB$ ở câu a", [P(r"Nửa quãng đường : $s_1=s_2=\dfrac{24}{2}=12\ \text{km}$."), M(r"t_1=\dfrac{s_1}{v_1}=\dfrac{12}{12}=1\ \text{h}"), M(r"t_2=\dfrac{s_2}{v_2}=\dfrac{12}{24}=0{,}5\ \text{h}"),
     M(r"t=t_1+t_2"), A(r"t=1{,}5\ \text{h}")]),
  ("Tốc độ trung bình ở câu a", [P("Lấy tổng quãng đường chia tổng thời gian :"), M(r"v_{tb}=\dfrac{s}{t}=\dfrac{24}{1{,}5}"), A(r"v_{tb}=16\ \text{km/h}"),
     P(r"Gần $12$ hơn $24$ vì xe mất nhiều thời gian ở chặng chậm.")]),
  ("Tốc độ trung bình ở câu b", [P(r"Gọi $t$ là tổng thời gian ; mỗi nửa kéo dài $\dfrac{t}{2}$ :"), M(r"s=12\cdot\dfrac{t}{2}+24\cdot\dfrac{t}{2}=18\,t"),
     M(r"v_{tb}=\dfrac{s}{t}=\dfrac{18\,t}{t}"), A(r"v_{tb}=18\ \text{km/h}"),
     P(r"Bằng trung bình cộng vì hai chặng có thời gian bằng nhau. Kiểm tra : $t=\dfrac{24}{18}=\dfrac43\ \text{h}$, mỗi nửa $\dfrac23\ \text{h}$ đi được $8\ \text{km}$ và $16\ \text{km}$, tổng $24\ \text{km}$ ✓.")]),
  ("Tốc độ trung bình cả đi lẫn về", [P(r"Quãng đường cả hành trình $s=2\cdot24=48\ \text{km}$ ; thời gian $t=1{,}5+1{,}5=3\ \text{h}$ :"), M(r"v_{tb}=\dfrac{48}{3}"), A(r"v_{tb}=16\ \text{km/h}")]),
  ("Vận tốc trung bình cả đi lẫn về", [P(r"Xe về đúng $A$ nên độ dịch chuyển bằng $0$ :"), M(r"|\vec v_{tb}|=\dfrac{|\Delta x|}{t}=\dfrac{0}{3}"), A(r"|\vec v_{tb}|=0")]),
  ("Kiểm tra", [P(r"Tốc độ trung bình luôn dương khi xe đang chạy ; vận tốc trung bình có thể bằng $0$ dù xe đã đi $48\ \text{km}$."),
     P(r"Câu a nhỏ hơn câu b vì ở câu a xe chạy chậm lâu hơn (chặng $12\ \text{km/h}$ mất $1\ \text{h}$, chặng $24\ \text{km/h}$ chỉ $0{,}5\ \text{h}$)."),
     P(r"Cả hai kết quả nằm giữa $12$ và $24\ \text{km/h}$ ✓.")])],
  [r"a) $v_{tb}=16\ \text{km/h}$", r"b) $v_{tb}=18\ \text{km/h}$", r"c) tốc độ trung bình $16\ \text{km/h}$ · vận tốc trung bình $0$"],
  r"Nhận dạng: thấy <strong>nửa quãng đường</strong> → cộng thời gian từng chặng rồi chia ; thấy <strong>nửa thời gian</strong> → cộng quãng đường từng chặng ; thấy <strong>đi rồi về</strong> → vận tốc trung bình bằng $0$."),
 sol(R2, [
  ("Thời điểm gặp nhau", [P("Gốc $O$ tại $A$, chiều dương từ $A$ đến $B$, mốc thời gian lúc $6$ giờ :"), M(r"x_1=60\,t"), M(r"x_2=150-40\,t"),
     P(r"Gặp nhau khi $x_1=x_2$ :"), M(r"60\,t=150-40\,t"), M(r"t=\dfrac{150}{100}"), A(r"t=1{,}5\ \text{h}"), P(r"Lúc $6+1{,}5$, tức $7$ giờ $30$ phút.")]),
  ("Vị trí gặp nhau", [M(r"x=x_1=60\cdot1{,}5"), A(r"x=90\ \text{km}"), P(r"Chỗ gặp nhau cách $A$ $90\ \text{km}$, nghiêng về phía $B$ vì ô tô chạy nhanh hơn.")]),
  (r"Cách nhau $30\ \text{km}$: lúc chưa gặp", [P(r"Chưa gặp nhau thì $x_2\gt x_1$, nên $d=x_2-x_1$ :"), M(r"150-40\,t-60\,t=30"), M(r"100\,t=120"), A(r"t=1{,}2\ \text{h}"),
     P(r"Lúc $6$ giờ $+\ 1{,}2\ \text{h}$ $=$ $7$ giờ $12$ phút.")]),
  (r"Cách nhau $30\ \text{km}$: lúc đã qua nhau", [P(r"Đã qua nhau thì $x_1\gt x_2$, nên $d=x_1-x_2$ :"), M(r"60\,t-(150-40\,t)=30"), M(r"100\,t=180"), A(r"t=1{,}8\ \text{h}"),
     P(r"Lúc $6$ giờ $+\ 1{,}8\ \text{h}$ $=$ $7$ giờ $48$ phút.")]),
  ("Xe máy khi ô tô đến $B$", [P(r"Ô tô đến $B$ khi $x_1=150$ :"), M(r"t=\dfrac{150}{60}=2{,}5\ \text{h}"), P("Lúc đó toạ độ xe máy :"), M(r"x_2=150-40\cdot2{,}5"), A(r"x_2=50\ \text{km}"),
     P(r"Gốc $O$ đặt tại $A$ nên xe máy còn cách $A$ $50\ \text{km}$.")]),
  ("Kiểm tra", [P(r"Lúc $t=1{,}2\ \text{h}$ : $x_1=72$, $x_2=102$, $d=30\ \text{km}$ ✓."), P(r"Lúc $t=1{,}8\ \text{h}$ : $x_1=108$, $x_2=78$, $d=30\ \text{km}$ ✓."),
     P(r"Hai thời điểm đối xứng quanh lúc gặp nhau ($1{,}5\pm0{,}3\ \text{h}$) vì tốc độ lại gần và tốc độ ra xa đều là $100\ \text{km/h}$.")])],
  [r"a) $7$ giờ $30$ phút · cách $A$ $90\ \text{km}$", r"b) $7$ giờ $12$ phút và $7$ giờ $48$ phút", r"c) $50\ \text{km}$"],
  r"Nhận dạng: hai xe <strong>đi ngược chiều, xuất phát cùng lúc</strong> → chọn gốc ở một bến, giải $x_1=x_2$ ; hỏi <strong>cách nhau $d$</strong> → xét $x_2-x_1=\pm d$."),
 sol(R3, [
  ("Đổi đơn vị", [P(r"Chiều dài tính bằng mét nên đổi tốc độ ra m/s :"), M(r"v_1=\dfrac{54}{3{,}6}"), A(r"v_1=15\ \text{m/s}"), P(r"Tàu thứ hai : $v_2=\dfrac{36}{3{,}6}=10\ \text{m/s}$.")]),
  ("Qua người đứng yên", [P(r"Đầu tàu phải đi đúng chiều dài tàu : $s=L_1=180\ \text{m}$."), M(r"t=\dfrac{s}{v_1}=\dfrac{180}{15}"), A(r"t=12\ \text{s}")]),
  ("Qua cầu", [P(r"Từ lúc đầu tàu lên cầu đến lúc đuôi tàu rời cầu, đầu tàu đi :"), M(r"s=L_1+S=180+420=600\ \text{m}"), M(r"t=\dfrac{s}{v_1}=\dfrac{600}{15}"), A(r"t=40\ \text{s}")]),
  ("Hai tàu ngược chiều", [P(r"Vận tốc tương đối và quãng đường tương đối :"), M(r"v_{\text{tđ}}=v_1+v_2=15+10=25\ \text{m/s}"), M(r"s_{\text{tđ}}=L_1+L_2=180+140=320\ \text{m}"),
     M(r"t=\dfrac{s_{\text{tđ}}}{v_{\text{tđ}}}=\dfrac{320}{25}"), A(r"t=12{,}8\ \text{s}")]),
  ("Hai tàu cùng chiều", [P(r"Cùng chiều thì tốc độ lại gần nhau là hiệu :"), M(r"v_{\text{tđ}}=v_1-v_2=15-10=5\ \text{m/s}"), M(r"t=\dfrac{L_1+L_2}{v_{\text{tđ}}}=\dfrac{320}{5}"), A(r"t=64\ \text{s}")]),
  ("Kiểm tra", [P(r"Cùng chiều lâu hơn ngược chiều ($64\ \text{s}\gt12{,}8\ \text{s}$) vì hai tàu lại gần nhau chậm hơn nhiều ($5\ \text{m/s}$ so với $25\ \text{m/s}$) ✓."),
     P(r"Nếu quên chiều dài tàu ở câu b sẽ ra $\dfrac{420}{15}=28\ \text{s}$, ngắn hơn thực tế."),
     P(r"Đổi lại : $12{,}8\ \text{s}\times25\ \text{m/s}=320\ \text{m}=L_1+L_2$ ✓.")])],
  [r"a) $12\ \text{s}$", r"b) $40\ \text{s}$", r"c) $12{,}8\ \text{s}$", r"d) $64\ \text{s}$"],
  r"Nhận dạng: thấy <strong>tàu có chiều dài</strong> → quãng đường tính theo đầu tàu cộng chiều dài cần vượt ($L_1$, $L_1+S$ hoặc $L_1+L_2$) ; hai tàu <strong>ngược chiều</strong> cộng tốc độ, <strong>cùng chiều</strong> trừ tốc độ."),
 sol(R4, [
  ("Tốc độ xuôi dòng và ngược dòng", [M(r"v_x=\dfrac{s}{t_x}=\dfrac{90}{3}"), A(r"v_x=30\ \text{km/h}"), M(r"v_{ng}=\dfrac{s}{t_{ng}}=\dfrac{90}{5}=18\ \text{km/h}")]),
  ("Tốc độ dòng nước và tốc độ riêng", [P(r"Xuôi dòng cộng $v_n$, ngược dòng trừ $v_n$ :"), M(r"v_t+v_n=30"), M(r"v_t-v_n=18"), P("Trừ vế theo vế :"), M(r"2\,v_n=12"), A(r"v_n=6\ \text{km/h}"),
     P(r"Cộng vế theo vế : $2\,v_t=48$, suy ra $v_t=24\ \text{km/h}$.")]),
  ("Thời gian bè trôi", [P(r"Bè không có máy, tốc độ so với bờ đúng bằng tốc độ dòng nước :"), M(r"t=\dfrac{s}{v_n}=\dfrac{90}{6}"), A(r"t=15\ \text{h}"),
     P(r"Công thức nhanh : $\dfrac{2\,t_x\,t_{ng}}{t_{ng}-t_x}=\dfrac{2\cdot3\cdot5}{5-3}=15\ \text{h}$ ✓.")]),
  ("Thời gian quay lại vớt phao", [P(r"Chọn hệ quy chiếu gắn với dòng nước : phao đứng yên ; canô rời phao với tốc độ riêng $v_t$ trong $t_1=20$ phút rồi quay lại với đúng tốc độ riêng $v_t$."),
     M(r"t_2=t_1"), A(r"t_2=20\ \text{phút}"), P("Đi ra xa và quay về cùng tốc độ nên cùng thời gian.")]),
  ("Quãng đường phao đã trôi", [P(r"Phao trôi theo dòng nước suốt $20+20=40$ phút $=\dfrac23\ \text{h}$ :"), M(r"s_{phao}=v_n\,(t_1+t_2)=6\cdot\dfrac23"), A(r"s_{phao}=4\ \text{km}")]),
  ("Kiểm tra", [P(r"Theo hệ quy chiếu gắn với bờ, trong $20$ phút đầu canô đi ngược dòng được $18\cdot\dfrac13=6\ \text{km}$ còn phao trôi xuống $6\cdot\dfrac13=2\ \text{km}$ : hai bên cách nhau $8\ \text{km}$."),
     P(r"Sau khi quay đầu, canô đi xuôi ($30\ \text{km/h}$) đuổi phao ($6\ \text{km/h}$) nên tiến lại gần với tốc độ $24\ \text{km/h}$ :"), M(r"t_2=\dfrac{8}{24}=\dfrac13\ \text{h}=20\ \text{phút}"), P("✓ Khớp với cách giải trong hệ quy chiếu gắn với nước.")])],
  [r"a) $v_n=6\ \text{km/h}$ · $v_t=24\ \text{km/h}$", r"b) $15\ \text{giờ}$", r"c) $20\ \text{phút}$ · phao trôi $4\ \text{km}$"],
  r"Nhận dạng: thấy <strong>bè trôi</strong> hoặc <strong>phao rơi</strong> → vật đó chỉ có tốc độ $v_n$ ; thấy <strong>xuôi và ngược</strong> → lập hai phương trình $v_t\pm v_n$ ; bài phao thì chuyển sang hệ quy chiếu gắn với nước."),
 sol(R5, [
  ("Xe $B$: độ dốc của đồ thị", [P(r"Đồ thị đi xuống, độ dốc :"), M(r"v_B=\dfrac{0-120}{4-0}=-30\ \text{km/h}"), A(r"|v_B|=30\ \text{km/h}"),
     P("Dấu âm : xe $B$ chuyển động ngược chiều dương, tức là về phía gốc $O$.")]),
  ("Xe $A$: giai đoạn cuối", [P(r"Giai đoạn $1$ ($0\to1\ \text{h}$) : $v=\dfrac{60-0}{1-0}=60\ \text{km/h}$. Giai đoạn $2$ ($1\to1{,}5\ \text{h}$) : đoạn nằm ngang nên $v=0$ (nghỉ)."),
     P("Giai đoạn $3$ ($1{,}5\\to3\\ \\text{h}$) :"), M(r"v=\dfrac{150-60}{3-1{,}5}=\dfrac{90}{1{,}5}"), A(r"v=60\ \text{km/h}")]),
  ("Phương trình xe $A$ giai đoạn cuối", [P(r"Giai đoạn $3$ bắt đầu ở $(1{,}5\ \text{h};60\ \text{km})$ :"), M(r"x_A=60+60\,(t-1{,}5)=60\,t-30"), P(r"Tại $t=2\ \text{h}$ :"), M(r"x_A=60\cdot2-30"), A(r"x_A=90\ \text{km}"),
     P(r"Tóm lại : $x_A=60t$ ($0\le t\le1$) · $x_A=60$ ($1\le t\le1{,}5$) · $x_A=60t-30$ ($1{,}5\le t\le3$) · $x_B=120-30t$ ($0\le t\le4$).")]),
  ("Thời điểm gặp nhau", [P(r"Thử giai đoạn $1$ : $60t=120-30t$ cho $t=\dfrac43\ \text{h}\gt1$ nên loại. Giai đoạn $2$ : $60=120-30t$ cho $t=2\ \text{h}\gt1{,}5$ nên loại."),
     P("Giai đoạn $3$ :"), M(r"60\,t-30=120-30\,t"), M(r"90\,t=150"), A(r"t=\dfrac53\ \text{h}\approx1{,}67\ \text{h}"), P(r"Nằm trong $[1{,}5;3]$ nên nhận.")]),
  ("Vị trí gặp nhau", [M(r"x=x_B=120-30\cdot\dfrac53"), A(r"x=70\ \text{km}")]),
  ("Kiểm tra", [P(r"Thế vào xe $A$ : $60\cdot\dfrac53-30=70\ \text{km}$ ✓ (trùng với xe $B$)."), P(r"$t=\dfrac53\ \text{h}\lt4\ \text{h}$ nên xe $B$ vẫn đang chạy ✓."),
     P(r"Giao điểm không nằm đúng nút lưới nên đọc bằng mắt chỉ cho giá trị gần đúng ; phải giải phương trình.")])],
  [r"a) $v_A$ : $60\ \text{km/h}$ · $0$ · $60\ \text{km/h}$ ; $|v_B|=30\ \text{km/h}$ (ngược chiều dương)", r"b) $x_A$ theo ba giai đoạn như trên ; $x_B=120-30t$", r"c) $t=\dfrac53\ \text{h}\approx1\ \text{h}\ 40\ \text{phút}$ · $x=70\ \text{km}$"],
  r"Nhận dạng: đề cho <strong>đồ thị $x$–$t$ có nhiều đoạn</strong> → độ dốc từng đoạn là vận tốc ; <strong>gặp nhau</strong> → giải $x_A=x_B$ rồi kiểm tra nghiệm có thuộc đoạn đang xét."),
 sol(R6, [
  ("Hướng bơi để sang đúng $B$", [P(r"Muốn đi thẳng từ $A$ đến $B$, thành phần vận tốc bơi dọc bờ phải triệt tiêu vận tốc dòng nước : $v_b\sin\alpha=v_n$."), M(r"\sin\alpha=\dfrac{v_n}{v_b}=\dfrac{1{,}2}{2{,}0}"), A(r"\sin\alpha=0{,}6"),
     P(r"$\alpha\approx36{,}9^\circ$ ; người bơi chếch về phía ngược dòng.")]),
  ("Tốc độ thực so với bờ", [P(r"Vận tốc thực vuông góc với bờ ; $v_b$ là cạnh huyền của tam giác vận tốc :"), M(r"v=\sqrt{v_b^2-v_n^2}=\sqrt{2{,}0^2-1{,}2^2}=\sqrt{2{,}56}"), A(r"v=1{,}6\ \text{m/s}")]),
  ("Thời gian bơi sang đúng $B$", [M(r"t_a=\dfrac{AB}{v}=\dfrac{96}{1{,}6}"), A(r"t_a=60\ \text{s}")]),
  ("Bơi vuông góc bờ: thời gian", [P(r"Hướng bơi vuông góc với bờ nên thành phần sang bờ chính là $v_b$ :"), M(r"t_b=\dfrac{AB}{v_b}=\dfrac{96}{2{,}0}"), A(r"t_b=48\ \text{s}")]),
  ("Bơi vuông góc bờ: bị trôi", [P("Nước đẩy người dọc bờ trong suốt thời gian bơi :"), M(r"\ell=v_n\,t_b=1{,}2\cdot48"), A(r"\ell=57{,}6\ \text{m}")]),
  ("So sánh hai cách", [P(r"$t_b=48\ \text{s}\lt t_a=60\ \text{s}$ : bơi vuông góc bờ sang nhanh hơn nhưng bị trôi $57{,}6\ \text{m}$, không tới $B$."),
     P(r"Bơi chếch ngược dòng (câu a) chậm hơn nhưng tới đúng $B$."),
     P(r"Kiểm tra : $v_b\cos\alpha=2{,}0\cdot0{,}8=1{,}6\ \text{m/s}=v$ ✓ ; $v_b\sin\alpha=1{,}2=v_n$ ✓."),
     A("T:Bơi vuông góc bờ <strong>nhanh hơn</strong> ; bơi chếch ngược dòng <strong>đến đúng $B$</strong>.")])],
  [r"a) $\sin\alpha=0{,}6$ (chếch ngược dòng) · $t=60\ \text{s}$", r"b) $t=48\ \text{s}$ · trôi $57{,}6\ \text{m}$", r"c) vuông góc bờ nhanh hơn ; chếch ngược dòng tới đúng $B$"],
  r"Nhận dạng: thấy <strong>sang đúng điểm đối diện</strong> → $v_b\sin\alpha=v_n$, $v=\sqrt{v_b^2-v_n^2}$ ; thấy <strong>bơi vuông góc bờ</strong> → $t=\dfrac{d}{v_b}$ và trôi $\ell=v_nt$."),
]


# ═════════════ TỰ GIẢI TỪNG BƯỚC ═════════════
STEPS = [
 # ── Dạng 1 ──
 dict(nhan_dang=r"Thấy <b>nửa quãng đường</b> → cộng thời gian từng chặng ; <b>nửa thời gian</b> → cộng quãng đường từng chặng.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Thời gian đi hết $AB$ ở câu a", "Tổng thời gian xe đi hết $AB$ ở câu a?", 1.5, "h", 0.02,
       loi=r"Lấy cả $24\ \text{km}$ chia cho từng tốc độ, thay vì chỉ chia nửa quãng đường cho tốc độ của chính nửa đó."),
  buoc("Tốc độ trung bình ở câu a", "Tốc độ trung bình của xe ở câu a?", 16, "km/h", 0.1,
       loi=r"Lấy trung bình cộng hai tốc độ — chỉ đúng khi hai chặng có thời gian bằng nhau.",
       ke=[(r"$v_{tb}=\dfrac{s_{\text{tổng}}}{t_{\text{tổng}}}$ với $t_{\text{tổng}}$ vừa tính", True),
           (r"$v_{tb}=\dfrac{v_1+v_2}{2}$", r"Trung bình cộng chỉ đúng khi hai chặng có thời gian bằng nhau ; ở đây hai chặng có quãng đường bằng nhau nên chặng chậm chiếm nhiều thời gian hơn."),
           (r"$v_{tb}=v_1+v_2$", r"Tốc độ trung bình không thể lớn hơn tốc độ lớn nhất của các chặng.")]),
  buoc("Tốc độ trung bình ở câu b", "Tốc độ trung bình của xe ở câu b?", 18, "km/h", 0.1,
       loi=r"Dùng lại cách làm câu a (hai chặng cùng quãng đường) trong khi câu b chia theo thời gian.",
       ke=[(r"Gọi $t$ là tổng thời gian, mỗi nửa $\dfrac{t}{2}$ ; cộng quãng đường hai chặng", True),
           (r"Tính $t_1=\dfrac{12}{12}$ và $t_2=\dfrac{12}{24}$ như câu a", r"Câu b không cho mỗi chặng dài $12\ \text{km}$ ; hai chặng có thời gian bằng nhau nên quãng đường khác nhau."),
           (r"$v_{tb}=\dfrac{2v_1v_2}{v_1+v_2}$", r"Công thức đó dành cho chia đều quãng đường ; câu b chia đều thời gian.")]),
  buoc("Tốc độ trung bình cả đi lẫn về", "Tốc độ trung bình trên cả hành trình đi và về?", 16, "km/h", 0.1,
       loi=r"Chỉ tính quãng đường lượt đi, hoặc lẫn tốc độ trung bình với vận tốc trung bình.",
       ke=[(r"$v_{tb}=\dfrac{\text{tổng quãng đường đi và về}}{\text{tổng thời gian}}$", True),
           (r"$v_{tb}=\dfrac{0}{3}$ vì về đúng chỗ xuất phát", r"Đó là vận tốc trung bình (dùng độ dịch chuyển). Tốc độ trung bình dùng tổng quãng đường đã đi nên không triệt tiêu khi đổi chiều."),
           (r"$v_{tb}=\dfrac{24}{3}$ (chỉ tính lượt đi)", r"Tổng quãng đường phải gồm cả lượt về.")]),
  buoc("Vận tốc trung bình cả đi lẫn về", "Độ lớn vận tốc trung bình trên cả hành trình?", 0, "km/h", 0.05,
       loi=r"Lấy bằng tốc độ trung bình vì quên rằng vận tốc trung bình dùng độ dịch chuyển, mà xe đã về đúng chỗ xuất phát.",
       ke=[(r"$|\vec v_{tb}|=\dfrac{|\Delta x|}{t}$ với độ dịch chuyển của cả hành trình", True),
           (r"$|\vec v_{tb}|=\dfrac{48}{3}$", r"$48\ \text{km}$ là quãng đường, không phải độ dịch chuyển ; về đúng điểm xuất phát nên độ dịch chuyển bằng $0$."),
           (r"$|\vec v_{tb}|=\dfrac{24}{1{,}5}$ (lấy riêng lượt đi)", r"Câu hỏi nói cả hành trình đi và về ; lượt đi và lượt về có độ dịch chuyển ngược dấu nên triệt tiêu nhau.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 2 ──
 dict(nhan_dang=r"Thấy <b>hai xe ngược chiều, xuất phát cùng lúc</b> → giải $x_1=x_2$ ; hỏi <b>cách nhau d</b> → xét hai khả năng.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Thời điểm gặp nhau", "Hai xe gặp nhau sau bao lâu kể từ lúc xuất phát?", 1.5, "h", 0.02,
       loi=r"Quên đổi dấu vận tốc của xe máy (viết $x_2=150+40t$) hoặc lấy hiệu hai tốc độ thay vì giải $x_1=x_2$."),
  buoc("Vị trí gặp nhau", "Chỗ gặp nhau cách $A$ bao nhiêu kilômét?", 90, "km", 0.5,
       loi=r"Lấy quãng đường xe máy đi (tính từ $B$) làm khoảng cách tới $A$ ; hoặc cho rằng hai xe gặp nhau ở trung điểm.",
       ke=[(r"Thế thời gian gặp vào phương trình toạ độ của ô tô", True),
           (r"Lấy $x=v_2t$ của xe máy", r"Xe máy xuất phát từ $B$ nên toạ độ của nó là $150-v_2t$ ; $v_2t$ chỉ là quãng đường nó đã đi."),
           (r"Lấy $x=\dfrac{150}{2}$ vì hai xe gặp ở giữa", r"Hai xe có tốc độ khác nhau nên không gặp ở trung điểm ; xe nhanh đi được quãng đường dài hơn.")]),
  buoc("Cách nhau $30\\ \\text{km}$: lúc chưa gặp", "Hai xe cách nhau $30\\ \\text{km}$ lần thứ nhất sau bao lâu?", 1.2, "h", 0.02,
       loi=r"Chỉ giải $x_1-x_2=30$ (chiều đã qua nhau) nên ra nghiệm lớn hơn thời gian gặp ; hoặc quên rằng có hai nghiệm.",
       ke=[(r"Viết $d=x_2-x_1=30$ với $x_2\gt x_1$ (chưa gặp) rồi giải", True),
           (r"Viết $x_1-x_2=30$", r"Đó là trường hợp đã qua nhau ; lần cách nhau $30\ \text{km}$ đầu tiên là lúc xe máy còn ở phía trước ô tô."),
           (r"Lấy $\dfrac{30}{60+40}$", r"$30\ \text{km}$ là khoảng cách còn lại, không phải quãng đường hai xe cùng đi được từ lúc xuất phát.")]),
  buoc("Cách nhau $30\\ \\text{km}$: lúc đã qua nhau", "Hai xe cách nhau $30\\ \\text{km}$ lần thứ hai sau bao lâu?", 1.8, "h", 0.02,
       loi=r"Dùng lại phương trình của lần trước ($x_2-x_1=30$) hoặc viết toạ độ xe máy là $40t$.",
       ke=[(r"Viết $d=x_1-x_2=30$ với $x_1\gt x_2$ (đã qua nhau) rồi giải", True),
           (r"Giải lại $x_2-x_1=30$ như lần trước", r"Phương trình đó chỉ cho đúng một nghiệm (lúc chưa gặp). Sau khi gặp, ô tô ở phía xa hơn nên $x_1\gt x_2$."),
           (r"Viết $x_1-x_2=30$ nhưng thay $x_2=40t$", r"Toạ độ xe máy là $150-40t$ ; $40t$ chỉ là quãng đường nó đi được.")]),
  buoc("Xe máy khi ô tô đến $B$", "Khi ô tô đến $B$, xe máy cách $A$ bao nhiêu kilômét?", 50, "km", 0.5,
       loi=r"Lấy thời gian gặp nhau thay cho thời gian ô tô đến $B$ ; hoặc tính quãng đường xe máy đã đi thay vì khoảng cách tới $A$.",
       ke=[(r"Tìm lúc ô tô đến $B$ ($x_1=AB$) rồi tính $x_2$ tại đó", True),
           (r"Tính $x_2$ tại thời điểm hai xe gặp nhau", r"Đó là lúc hai xe gặp nhau ; ô tô còn phải đi tiếp đến $B$."),
           (r"Tính $x_2$ lúc xe máy đến $A$", r"Đó là lúc $x_2=0$ ; cần thời điểm ô tô đến $B$ chứ không phải lúc xe máy đến $A$.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 3 ──
 dict(nhan_dang=r"Thấy <b>tàu có chiều dài</b> → quãng đường cộng thêm chiều dài cần vượt ; <b>ngược chiều</b> cộng tốc độ, <b>cùng chiều</b> trừ tốc độ.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Đổi đơn vị", "Tốc độ của tàu thứ nhất bằng bao nhiêu mét trên giây?", 15, "m/s", 0.1,
       loi=r"Nhân với $3{,}6$ thay vì chia, hoặc thay thẳng $54$ vào công thức với chiều dài tính bằng mét."),
  buoc("Qua người đứng yên", "Tàu qua hết người đứng yên bên đường mất bao lâu?", 12, "s", 0.1,
       loi=r"Coi tàu là một điểm nên cho thời gian bằng $0$, hoặc chia chiều dài cho $54$ chưa đổi đơn vị.",
       ke=[(r"Đầu tàu đi đúng chiều dài tàu : $s=L_1$", True),
           (r"Coi tàu là điểm : $s=0$", r"Đoàn tàu dài $180\ \text{m}$ nên người chỉ qua hết khi cả đuôi tàu đã qua người."),
           (r"$s=L_1$ nhưng dùng $v=54$ trực tiếp", r"Chiều dài tính bằng mét còn tốc độ tính bằng km/h : phải đổi cùng hệ đơn vị trước khi chia.")]),
  buoc("Qua cầu", "Tàu qua hết cầu (đầu tàu lên cầu → đuôi tàu rời cầu) mất bao lâu?", 40, "s", 0.5,
       loi=r"Chỉ lấy chiều dài cầu ($420\ \text{m}$) hoặc lấy hiệu hai chiều dài.",
       ke=[(r"$s=L_1+S$", True),
           (r"$s=S$", r"Tàu chỉ qua hết cầu khi đuôi tàu rời cầu : đầu tàu còn phải đi thêm đúng chiều dài tàu sau khi ra khỏi cầu."),
           (r"$s=S-L_1$", r"Hiệu đó là quãng đường mũi tàu đi trong khoảng thời gian cả đoàn tàu nằm trọn trên cầu, chưa phải từ lúc đầu tàu lên cầu đến lúc đuôi tàu rời cầu.")]),
  buoc("Hai tàu ngược chiều", "Hai tàu ngược chiều vượt qua nhau hoàn toàn mất bao lâu?", 12.8, "s", 0.1,
       loi=r"Lấy hiệu hai tốc độ (đó là trường hợp cùng chiều) hoặc chỉ cộng một chiều dài tàu.",
       ke=[(r"Tốc độ tương đối $v_1+v_2$ ; quãng đường tương đối $L_1+L_2$", True),
           (r"Tốc độ tương đối $v_1-v_2$", r"Hai tàu ngược chiều nên tốc độ lại gần nhau là tổng ; hiệu chỉ dùng khi cùng chiều."),
           (r"Quãng đường tương đối chỉ là $L_1$", r"Hai tàu vượt nhau hoàn toàn khi cả hai đoàn đã qua nhau : phải cộng chiều dài của cả hai.")]),
  buoc("Hai tàu cùng chiều", "Tàu thứ nhất vượt qua hết tàu thứ hai (cùng chiều) mất bao lâu?", 64, "s", 0.5,
       loi=r"Cộng hai tốc độ như trường hợp ngược chiều, hoặc chỉ lấy $L_1$ làm quãng đường tương đối.",
       ke=[(r"Tốc độ tương đối $v_1-v_2$ ; quãng đường tương đối $L_1+L_2$", True),
           (r"Tốc độ tương đối $v_1+v_2$ như câu c", r"Cùng chiều thì tàu nhanh chỉ tiến lại gần tàu chậm với tốc độ bằng hiệu hai tốc độ."),
           (r"Quãng đường tương đối $L_1$", r"Tàu thứ nhất phải vượt hết chiều dài tàu thứ hai và cả chiều dài của chính nó : $L_1+L_2$.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 4 ──
 dict(nhan_dang=r"Thấy <b>bè trôi</b> hoặc <b>phao rơi</b> → tốc độ chỉ bằng dòng nước ; thấy <b>xuôi và ngược</b> → lập $v_t\pm v_n$.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Tốc độ xuôi dòng", "Tốc độ của canô so với bờ khi xuôi dòng?", 30, "km/h", 0.2,
       loi=r"Chia thời gian cho quãng đường (đảo ngược $v=\dfrac{s}{t}$) hoặc cho rằng tốc độ xuôi là tốc độ riêng của canô."),
  buoc("Tốc độ dòng nước", "Tốc độ dòng nước bằng bao nhiêu?", 6, "km/h", 0.1,
       loi=r"Lấy hiệu hai tốc độ mà không chia $2$, hoặc lấy trung bình cộng (đó là tốc độ riêng của canô).",
       ke=[(r"Lập hệ $v_t+v_n=v_x$ và $v_t-v_n=v_{ng}$ rồi trừ vế theo vế : $v_n=\dfrac{v_x-v_{ng}}{2}$", True),
           (r"$v_n=v_x-v_{ng}$", r"Hiệu hai tốc độ bằng $2v_n$ (xuôi cộng $v_n$, ngược trừ $v_n$) nên phải chia đôi."),
           (r"$v_n=\dfrac{v_x+v_{ng}}{2}$", r"Đó là tốc độ riêng $v_t$ của canô, không phải của dòng nước.")]),
  buoc("Thời gian bè trôi", "Bè trôi từ $A$ đến $B$ mất bao nhiêu giờ?", 15, "h", 0.1,
       loi=r"Dùng tốc độ riêng của canô cho bè, hoặc cộng thời gian xuôi và ngược.",
       ke=[(r"Bè trôi với tốc độ đúng bằng tốc độ dòng nước : $t=\dfrac{s}{v_n}$", True),
           (r"$t=\dfrac{s}{v_t}$", r"Bè không có máy : tốc độ của bè so với bờ chỉ là tốc độ dòng nước, không phải tốc độ riêng của canô."),
           (r"$t=t_x+t_{ng}$", r"Cộng hai thời gian của canô không liên quan tới chuyển động của bè.")]),
  buoc("Thời gian quay lại vớt phao", "Từ lúc quay đầu đến lúc vớt được phao mất bao nhiêu phút?", 20, "phút", 0.5,
       loi=r"Lấy quãng đường canô đã đi ngược dòng (so với bờ) chia cho tốc độ xuôi dòng — quên rằng phao cũng đang trôi.",
       ke=[(r"Xét trong hệ quy chiếu gắn với dòng nước : phao đứng yên, canô rời ra rồi quay lại với cùng tốc độ riêng", True),
           (r"Lấy thời gian quay lại bằng quãng đường canô đã đi ngược dòng (so với bờ) chia $v_x$", r"Phao cũng trôi theo dòng nên quãng đường canô cần đuổi không bằng quãng đường canô đã đi so với bờ ; kết quả sai."),
           (r"Quay lại xuôi dòng nhanh hơn nên mất ít thời gian hơn lúc rời đi", r"Dòng nước đẩy cả canô lẫn phao như nhau, nên so với phao thì xuôi hay ngược không làm tốc độ canô thay đổi.")]),
  buoc("Quãng đường phao đã trôi", "Phao đã trôi cách chỗ rơi bao nhiêu kilômét?", 4, "km", 0.1,
       loi=r"Chỉ tính phao trôi trong $20$ phút đầu, hoặc lấy bằng quãng đường canô đi xuôi dòng khi quay lại.",
       ke=[(r"Phao trôi đều với tốc độ dòng nước suốt thời gian từ lúc rơi đến lúc được vớt", True),
           (r"Phao chỉ trôi trong $20$ phút đầu", r"Phao vẫn trôi trong lúc canô quay lại ; thời gian trôi là tổng của hai khoảng."),
           (r"Quãng đường phao trôi bằng quãng đường canô đi xuôi khi quay lại", r"Canô chạy nhanh hơn dòng nước nên quãng đường của canô lúc quay lại lớn hơn quãng đường phao trôi.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 5 ──
 dict(nhan_dang=r"Thấy <b>đồ thị x–t nhiều đoạn</b> → độ dốc là vận tốc ; <b>gặp nhau</b> → giải $x_A=x_B$ rồi kiểm tra đoạn.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 3}, buoc=[
  buoc("Xe $B$: độ dốc của đồ thị", "Độ lớn tốc độ của xe $B$ bằng bao nhiêu?", 30, "km/h", 0.2,
       loi=r"Lấy toạ độ cuối chia thời gian (không trừ toạ độ đầu), hoặc nghĩ rằng dấu âm của vận tốc nghĩa là xe chậm đi."),
  buoc("Xe $A$: giai đoạn cuối", "Tốc độ của xe $A$ ở giai đoạn đi tiếp (sau lúc nghỉ)?", 60, "km/h", 0.5,
       loi=r"Lấy cả hành trình chia cả thời gian (tính luôn lúc nghỉ) thay vì chỉ lấy độ biến thiên trên đoạn đi tiếp.",
       ke=[(r"$v=\dfrac{\Delta x}{\Delta t}$ trên đoạn từ $t=1{,}5\ \text{h}$ đến $t=3\ \text{h}$", True),
           (r"$v=\dfrac{150}{3}$ (từ gốc đến cuối)", r"Đó là tốc độ trung bình cả hành trình, tính cả lúc nghỉ ; giai đoạn cuối phải dùng độ biến thiên trên chính đoạn đó."),
           (r"Tính độ dốc từ $t=1\ \text{h}$ đến $t=3\ \text{h}$", r"Khoảng này có cả lúc nghỉ ; giai đoạn đi tiếp chỉ bắt đầu từ $t=1{,}5\ \text{h}$.")]),
  buoc("Phương trình xe $A$ giai đoạn cuối", "Theo phương trình của xe $A$ ở giai đoạn đi tiếp, toạ độ xe $A$ lúc $t=2\\ \\text{h}$ bằng bao nhiêu?", 90, "km", 0.5,
       loi=r"Viết $x_A=60t$ (phương trình giai đoạn đầu) hoặc thiếu mốc thời gian lúc bắt đầu giai đoạn đi tiếp.",
       ke=[(r"$x_A=x_0+v(t-t_0)$ với $(t_0;x_0)$ là điểm đầu giai đoạn đi tiếp", True),
           (r"$x_A=60t$", r"Đó là phương trình giai đoạn đầu (từ gốc) ; giai đoạn đi tiếp bắt đầu từ $x=60$ lúc $t=1{,}5\ \text{h}$ nên phải có $t-1{,}5$."),
           (r"$x_A=60+60t$", r"Thiếu mốc thời gian : giai đoạn này bắt đầu lúc $t=1{,}5\ \text{h}$ chứ không phải lúc $t=0$.")]),
  buoc("Thời điểm gặp nhau", "Hai xe gặp nhau sau bao lâu (giờ)?", 1.667, "h", 0.01,
       loi=r"Giải $x_A=x_B$ bằng phương trình giai đoạn đầu rồi nhận nghiệm nằm ngoài đoạn $0\le t\le1$ ; hoặc cho hai vận tốc bằng nhau.",
       ke=[(r"Giải $x_A=x_B$ với phương trình xe $A$ ở giai đoạn đi tiếp, rồi kiểm tra $t$ có thuộc đoạn đó không", True),
           (r"Giải $x_A=x_B$ với $x_A=60t$ (giai đoạn đầu) vì xe $A$ xuất phát từ gốc", r"Mỗi phương trình chỉ đúng trong khoảng thời gian của giai đoạn : giai đoạn đầu chỉ tới $t=1\ \text{h}$, nghiệm ngoài đoạn đó vô nghĩa."),
           (r"Cho hai vận tốc bằng nhau", r"Hai xe gặp nhau khi toạ độ bằng nhau, không phải khi vận tốc bằng nhau.")]),
  buoc("Vị trí gặp nhau", "Hai xe gặp nhau ở toạ độ nào?", 70, "km", 0.5,
       loi=r"Đọc toạ độ từ lưới ô vuông bằng mắt, hoặc lấy toạ độ lúc xe $A$ đang nghỉ.",
       ke=[(r"Thế thời điểm gặp vào phương trình của một trong hai xe", True),
           (r"Đọc toạ độ giao điểm từ lưới ô vuông", r"Giao điểm không nằm đúng nút lưới ($t$ không tròn) nên đọc bằng mắt chỉ gần đúng ; phải tính."),
           (r"Lấy toạ độ xe $A$ lúc nghỉ", r"Xe $A$ nghỉ trong khoảng $1\ \text{h}$ đến $1{,}5\ \text{h}$, trước lúc hai xe gặp nhau.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 6 ──
 dict(nhan_dang=r"Thấy <b>sang đúng điểm đối diện</b> → $v_b\sin\alpha=v_n$ ; thấy <b>bơi vuông góc bờ</b> → $t=\dfrac{d}{v_b}$ và trôi $\ell=v_nt$.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Hướng bơi để sang đúng $B$", "$\\sin\\alpha$ bằng bao nhiêu (α hợp giữa hướng bơi và $AB$)?", 0.6, "", 0.01,
       loi=r"Dùng $\tan\alpha$ hoặc lẫn $\sin$ với $\cos$ ; hoặc cho rằng cứ bơi thẳng về phía $B$ là sang đúng $B$."),
  buoc("Tốc độ thực so với bờ", "Độ lớn vận tốc của người so với bờ khi sang đúng $B$?", 1.6, "m/s", 0.02,
       loi=r"Lấy hiệu hai tốc độ $v_b-v_n$ hoặc cộng bình phương như tam giác vuông cạnh huyền là vận tốc thực.",
       ke=[(r"$\vec v$ vuông góc bờ nên $v_b$ là cạnh huyền : $v=\sqrt{v_b^2-v_n^2}$", True),
           (r"$v=v_b-v_n$", r"Hai vectơ không cùng phương nên không trừ độ lớn trực tiếp ; vận tốc thực là tổng vectơ."),
           (r"$v=\sqrt{v_b^2+v_n^2}$", r"Căn tổng bình phương dùng khi $v_b$ và $v_n$ vuông góc nhau (bơi vuông góc bờ). Ở đây vận tốc thực vuông góc với dòng nước nên $v_b$ là cạnh huyền.")]),
  buoc("Thời gian bơi sang đúng $B$", "Thời gian bơi sang đúng $B$?", 60, "s", 0.5,
       loi=r"Chia $AB$ cho $v_b$ (quên rằng người không đi theo hướng bơi) hoặc chia cho $v_n$.",
       ke=[(r"$t=\dfrac{AB}{v}$ với $v$ là tốc độ thực vừa tính", True),
           (r"$t=\dfrac{AB}{v_b}$", r"Người không đi theo hướng bơi : so với bờ chỉ tiến sang bờ kia với tốc độ thực $v$ nhỏ hơn $v_b$."),
           (r"$t=\dfrac{AB}{v_n}$", r"Dòng nước chảy dọc bờ, không giúp người sang bờ ; thành phần sang bờ là thành phần vuông góc.")]),
  buoc("Bơi vuông góc bờ: thời gian", "Bơi luôn vuông góc bờ thì mất bao lâu để sang bờ bên kia?", 48, "s", 0.5,
       loi=r"Dùng tốc độ thực của câu a, hoặc chia $AB$ cho độ lớn vận tốc thực chéo.",
       ke=[(r"Hướng bơi vuông góc bờ nên thành phần sang bờ chính là $v_b$ : $t=\dfrac{d}{v_b}$", True),
           (r"$t=\dfrac{d}{v}$ với $v$ của câu a", r"Tốc độ $v$ ở câu a ứng với hướng bơi chếch ; câu b bơi vuông góc nên tốc độ sang bờ là $v_b$."),
           (r"$t=\dfrac{d}{\sqrt{v_b^2+v_n^2}}$", r"$d$ không phải quãng đường đi chéo ; thời gian sang bờ chỉ phụ thuộc thành phần vuông góc bờ, tức là $v_b$.")]),
  buoc("Bơi vuông góc bờ: bị trôi", "Khi sang đến bờ bên kia, người bị nước đẩy trôi xuống phía dưới $B$ bao nhiêu mét?", 57.6, "m", 0.5,
       loi=r"Dùng thời gian của câu a, hoặc lấy tốc độ bơi $v_b$ thay cho tốc độ dòng nước.",
       ke=[(r"Trôi theo dòng nước trong suốt thời gian bơi : $\ell=v_nt$", True),
           (r"$\ell=v_bt$", r"Nước đẩy người dọc bờ với $v_n$ ; $v_b$ là tốc độ bơi vuông góc bờ."),
           (r"$\ell=v_nt$ với $t$ của câu a", r"Thời gian câu a ứng với cách bơi chếch ; câu b phải dùng thời gian của chính lần bơi vuông góc.")]),
  buoc("So sánh hai cách", "Chọn kết luận đúng.",
       loi=r"Cho rằng cách tới đúng $B$ cũng là cách nhanh nhất.",
       lua_chon=[(r"Bơi vuông góc bờ sang nhanh hơn nhưng bị trôi ; bơi chếch ngược dòng chậm hơn nhưng tới đúng $B$", True),
                 (r"Bơi chếch ngược dòng vừa nhanh hơn vừa tới đúng $B$", r"Thời gian câu a lớn hơn câu b vì thành phần vận tốc sang bờ nhỏ hơn."),
                 (r"Bơi vuông góc bờ vừa nhanh hơn vừa tới đúng $B$", r"Bơi vuông góc thì dòng nước làm người lệch xuống phía dưới nên không tới đúng $B$.")],
       ke=[(r"So thời gian $t_b$ với $t_a$ và so vị trí tới bờ bên kia", True),
           (r"Chỉ so thời gian", r"Câu hỏi còn hỏi cách nào tới đúng $B$ : phải xét cả vị trí tới."),
           (r"Chỉ so vị trí tới", r"Câu hỏi còn hỏi cách nào nhanh hơn : phải so cả thời gian.")])]),
]


# ═════════════ BÀI TỰ LUẬN (ví dụ D, luyện E, nâng cao G của nguồn) ═════════════
def L(*lines):
    return "".join(f"<p>{x}</p>" for x in lines)

def g3_fig():
    p = "g3"; OX, OY, KT, KX = 56, 196, 150, 2.4
    b = defs(p)
    for t in (0, 0.5, 1, 1.5, 2):
        b += seg(OX + KT * t, OY, OX + KT * t, OY - 60 * KX, GREY, 1, "4 4", .45) + txt(OX + KT * t, OY + 18, ("0" if t == 0 else f"{t:g}".replace(".", ",")), "currentColor", 12, "middle", "400")
    for x in (0, 15, 30, 45, 60):
        b += seg(OX, OY - KX * x, OX + 2 * KT + 6, OY - KX * x, GREY, 1, "4 4", .45) + txt(OX - 8, OY - KX * x + 4, str(x), "currentColor", 12, "end", "400")
    b += arrow(p, "g", OX, OY, OX + 2 * KT + 28, OY, 2) + txt(OX + 2 * KT + 30, OY + 5, "t (h)", GRN, 12)
    b += arrow(p, "g", OX, OY, OX, OY - 60 * KX - 24, 2) + txt(OX + 6, OY - 60 * KX - 28, "x (km)", GRN, 12)
    car = [(0, 0), (0.25, 15), (1, 15), (2, 60)]
    b += poly([(OX + KT * t, OY - KX * x) for t, x in car], ORG, 3) + poly([(OX, OY), (OX + 2 * KT, OY - 60 * KX)], BLUE, 3)
    for t, x in car: b += dot(OX + KT * t, OY - KX * x, 4, ORG)
    b += dot(OX + 2 * KT, OY - 60 * KX, 4, BLUE)
    b += txt(OX + KT * 0.63, OY - KX * 15 + 18, "ôtô nghỉ", ORG, 12, "middle", "400") + txt(OX + KT * 0.35, OY - KX * 38, "xe đạp", BLUE, 13, "start") + txt(OX + KT * 1.5, OY - KX * 30, "ôtô", ORG, 13, "start")
    return fig("c13-g3", "0 0 420 222", "Đồ thị toạ độ – thời gian của ôtô (có đoạn nghỉ) và xe đạp, hai xe đến B cùng lúc",
               b, "Đáp án câu a : xe đạp là đoạn thẳng từ gốc đến (2 h ; 60 km) ; ôtô gồm ba đoạn, đoạn giữa nằm ngang.")

TL = [
 ("Dễ", L(r"Một ô tô chuyển động trên đoạn đường $120\ \text{km}$. Trong nửa thời gian đầu xe chạy với tốc độ $40\ \text{km/h}$, nửa thời gian sau chạy với tốc độ $60\ \text{km/h}$. Tính tốc độ trung bình của ô tô."),
        L(r"Gọi $t$ là tổng thời gian ; mỗi nửa kéo dài $\dfrac t2$.", r"$s=40\cdot\dfrac t2+60\cdot\dfrac t2=50\,t$.", r"$v_{tb}=\dfrac st=50\ \text{km/h}$.",
          r"Kiểm tra : $t=\dfrac{120}{50}=2{,}4\ \text{h}$ ; mỗi nửa $1{,}2\ \text{h}$ đi được $48\ \text{km}$ và $72\ \text{km}$, tổng $120\ \text{km}$ ✓.")),
 ("Dễ", L(r"Một người đi bộ trên quãng đường $s$. Nửa quãng đường đầu đi với tốc độ $6\ \text{km/h}$, nửa quãng đường sau đi với tốc độ $4\ \text{km/h}$. Tính tốc độ trung bình của người đó."),
        L(r"$t_1=\dfrac{s/2}{6}=\dfrac{s}{12}$ ; $t_2=\dfrac{s/2}{4}=\dfrac{s}{8}$.", r"$t=t_1+t_2=\dfrac{5s}{24}$.", r"$v_{tb}=\dfrac st=\dfrac{24}{5}=4{,}8\ \text{km/h}$.",
          r"Nhỏ hơn trung bình cộng $5\ \text{km/h}$ vì người đi chậm lâu hơn ✓.")),
 ("Dễ", L(r"Một ô tô chuyển động nhanh dần : giây thứ nhất đi được $2\ \text{m}$, giây thứ hai $4\ \text{m}$, giây thứ ba $6\ \text{m}$, … (mỗi giây đi hơn giây trước $2\ \text{m}$). Tính tốc độ trung bình của xe trong $10$ giây đầu."),
        L(r"Quãng đường $10$ giây đầu : $s=2+4+6+\dots+20=2\,(1+2+\dots+10)=2\cdot55=110\ \text{m}$.", r"$v_{tb}=\dfrac{110}{10}=11\ \text{m/s}$.")),
 ("Dễ", L(r"Quãng đường của một vật theo thời gian là $s=2t^2$ ($s$ tính bằng mét, $t$ bằng giây). Tính tốc độ trung bình của vật từ $t=1\ \text{s}$ đến $t=4\ \text{s}$."),
        L(r"$s(1)=2\cdot1^2=2\ \text{m}$ ; $s(4)=2\cdot4^2=32\ \text{m}$.", r"$\Delta s=32-2=30\ \text{m}$ ; $\Delta t=4-1=3\ \text{s}$.", r"$v_{tb}=\dfrac{\Delta s}{\Delta t}=\dfrac{30}{3}=10\ \text{m/s}$.")),
 ("Dễ", L(r"Một đoàn tàu hoả dài $200\ \text{m}$ chạy với tốc độ $72\ \text{km/h}$ vượt qua một đoàn tàu khác dài $150\ \text{m}$ đang đứng yên trên đường ray bên cạnh (từ lúc đầu tàu thứ nhất ngang đuôi tàu thứ hai đến lúc đuôi tàu thứ nhất ngang đầu tàu thứ hai). Tính thời gian vượt qua."),
        L(r"$v=\dfrac{72}{3{,}6}=20\ \text{m/s}$.", r"Quãng đường tương đối $s=L_1+L_2=200+150=350\ \text{m}$.", r"$t=\dfrac sv=\dfrac{350}{20}=17{,}5\ \text{s}$.")),
 ("Trung bình", L(r"Một người đi từ $A$ đến $B$. Trên $\dfrac13$ quãng đường đầu đi với tốc độ $20\ \text{km/h}$, trên $\dfrac13$ quãng đường tiếp theo đi với tốc độ $30\ \text{km/h}$, trên $\dfrac13$ quãng đường cuối đi với tốc độ $60\ \text{km/h}$. Tính tốc độ trung bình trên cả quãng đường $AB$."),
        L(r"Gọi $s$ là độ dài $AB$ ; mỗi đoạn dài $\dfrac s3$.", r"$t_1=\dfrac{s/3}{20}=\dfrac{s}{60}$ ; $t_2=\dfrac{s/3}{30}=\dfrac{s}{90}$ ; $t_3=\dfrac{s/3}{60}=\dfrac{s}{180}$.",
          r"$t=s\left(\dfrac{3+2+1}{180}\right)=\dfrac{s}{30}$.", r"$v_{tb}=\dfrac st=30\ \text{km/h}$.", r"Nhỏ hơn trung bình cộng $\dfrac{20+30+60}{3}\approx36{,}7\ \text{km/h}$ ✓.")),
 ("Trung bình", L(r"Hai xe cùng đi từ $A$ về $B$ ($AB=90\ \text{km}$). Xe thứ nhất chạy với tốc độ $45\ \text{km/h}$. Xe thứ hai chạy với tốc độ $30\ \text{km/h}$ nhưng xuất phát trước xe thứ nhất $30$ phút. Xe nào đến $B$ trước và trước bao lâu?"),
        L(r"Xe thứ nhất đi hết $\dfrac{90}{45}=2\ \text{h}$ ; xe thứ hai đi hết $\dfrac{90}{30}=3\ \text{h}$.", r"Lấy mốc là lúc xe thứ nhất xuất phát : xe thứ hai xuất phát lúc $-0{,}5\ \text{h}$ nên đến $B$ lúc $3-0{,}5=2{,}5\ \text{h}$.",
          r"Xe thứ nhất đến lúc $2\ \text{h}$, sớm hơn $0{,}5\ \text{h}$ = $30$ phút.")),
 ("Trung bình", L(r"Lúc $6$ giờ, một người đi xe đạp từ $A$ về $B$ với tốc độ $15\ \text{km/h}$. Đến $7$ giờ, một người đi xe máy cũng từ $A$ về $B$ với tốc độ $35\ \text{km/h}$. Quãng đường $AB$ dài $70\ \text{km}$.", r"a) Người đi xe máy đuổi kịp người đi xe đạp lúc mấy giờ và ở chỗ cách $A$ bao nhiêu?", r"b) Lúc mấy giờ hai người cách nhau $10\ \text{km}$?"),
        L(r"a) Lúc $7$ giờ, xe đạp đã đi $15\cdot1=15\ \text{km}$ : khoảng cách giữa hai người là $15\ \text{km}$.", r"Tốc độ lại gần nhau (cùng chiều) : $35-15=20\ \text{km/h}$.", r"$t=\dfrac{15}{20}=0{,}75\ \text{h}=45$ phút, tức $7$ giờ $45$ phút ; chỗ gặp cách $A$ $35\cdot0{,}75=26{,}25\ \text{km}$.",
          r"b) Chưa kịp : $\dfrac{15-10}{20}=0{,}25\ \text{h}$ sau $7$ giờ, tức $7$ giờ $15$ phút.", r"Đã vượt : $\dfrac{15+10}{20}=1{,}25\ \text{h}$ sau $7$ giờ, tức $8$ giờ $15$ phút (xe máy lúc này cách $A$ $43{,}75\ \text{km}\lt70\ \text{km}$ nên vẫn hợp lí).")),
 ("Trung bình", L(r"Hai người đi xe đạp xuất phát cùng lúc từ hai điểm $A$ và $B$ cách nhau $30\ \text{km}$, đi ngược chiều nhau. Tốc độ người từ $A$ là $12\ \text{km/h}$, người từ $B$ là $18\ \text{km/h}$. Một chú chim bay với tốc độ $30\ \text{km/h}$, xuất phát cùng lúc từ $A$ bay đến gặp người từ $B$, rồi quay lại gặp người từ $A$, cứ như vậy cho đến khi hai người gặp nhau. Tính tổng quãng đường chim bay được."),
        L(r"Hai người gặp nhau sau $t=\dfrac{30}{12+18}=1\ \text{h}$.", r"Chim bay liên tục trong đúng $1\ \text{h}$ nên tổng quãng đường $s=30\cdot1=30\ \text{km}$.", r"Không cần cộng từng chặng bay qua lại.")),
 ("Trung bình", L(r"Hai đoàn tàu dài bằng nhau $L=100\ \text{m}$ chạy trên hai đường ray song song. Nếu chạy cùng chiều, tàu nhanh vượt tàu chậm trong $t_1=40\ \text{s}$. Nếu chạy ngược chiều, thời gian từ lúc hai đầu tàu gặp nhau đến lúc hai đuôi tàu rời nhau là $t_2=8\ \text{s}$. Tính tốc độ của mỗi đoàn tàu."),
        L(r"Tổng chiều dài $200\ \text{m}$. Gọi $v_1\gt v_2$.", r"Cùng chiều : $v_1-v_2=\dfrac{200}{40}=5\ \text{m/s}$.", r"Ngược chiều : $v_1+v_2=\dfrac{200}{8}=25\ \text{m/s}$.",
          r"Cộng : $2v_1=30$ nên $v_1=15\ \text{m/s}=54\ \text{km/h}$.", r"Trừ : $2v_2=20$ nên $v_2=10\ \text{m/s}=36\ \text{km/h}$.")),
 ("Trung bình", L(r"Một canô chạy xuôi dòng một khúc sông mất $1$ giờ $30$ phút và chạy ngược dòng khúc sông đó mất $2$ giờ $30$ phút. Nếu tắt máy để canô trôi theo dòng nước thì mất bao lâu?"),
        L(r"Gọi $s$ là chiều dài khúc sông : $v_x=\dfrac{s}{1{,}5}$, $v_{ng}=\dfrac{s}{2{,}5}$.", r"$v_n=\dfrac{v_x-v_{ng}}{2}=\dfrac s2\left(\dfrac1{1{,}5}-\dfrac1{2{,}5}\right)=\dfrac{s}{7{,}5}$.",
          r"$t_{\text{trôi}}=\dfrac{s}{v_n}=7{,}5\ \text{h}$ (công thức nhanh : $\dfrac{2\cdot1{,}5\cdot2{,}5}{2{,}5-1{,}5}=7{,}5$ ✓).")),
 ("Trung bình", L(r"Đúng $12$ giờ trưa, kim giờ và kim phút của một đồng hồ trùng nhau.", r"a) Sau ít nhất bao lâu thì hai kim lại trùng nhau ?", r"b) Sau ít nhất bao lâu thì hai kim tạo với nhau một góc vuông ($90^\circ$)?"),
        L(r"Kim phút : $1$ vòng/giờ ; kim giờ : $\dfrac1{12}$ vòng/giờ. Tốc độ tương đối $v_{\text{tđ}}=1-\dfrac1{12}=\dfrac{11}{12}$ vòng/giờ.", r"a) Kim phút phải hơn kim giờ đúng $1$ vòng : $t=\dfrac{1}{11/12}=\dfrac{12}{11}\ \text{h}\approx1$ giờ $5$ phút $27$ giây.",
          r"b) Kim phút phải hơn kim giờ $\dfrac14$ vòng : $t=\dfrac{1/4}{11/12}=\dfrac3{11}\ \text{h}\approx16$ phút $22$ giây.")),
 ("Trung bình", L(r"Kim giờ và kim phút của một đồng hồ trùng nhau lúc $12$ giờ. Hỏi vào thời điểm nào tiếp theo hai kim tạo với nhau một góc $180^\circ$ (thẳng hàng, ngược hướng)?"),
        L(r"Kim phút phải hơn kim giờ $\dfrac12$ vòng.", r"$t=\dfrac{1/2}{11/12}=\dfrac6{11}\ \text{h}\approx32$ phút $44$ giây.", r"Tức khoảng $12$ giờ $32$ phút $44$ giây.")),
 ("Khó", L(r"Một canô xuôi dòng từ $A$ đến $B$ rồi lập tức quay về $A$ mất tổng cộng $5$ giờ. Biết $AB=60\ \text{km}$ và tốc độ dòng nước là $5\ \text{km/h}$. Tính tốc độ riêng của canô."),
        L(r"Gọi $v$ là tốc độ riêng ($v\gt5$) : $\dfrac{60}{v+5}+\dfrac{60}{v-5}=5$.", r"Chia hai vế cho $5$ : $\dfrac{12}{v+5}+\dfrac{12}{v-5}=1$.", r"Quy đồng : $12(v-5)+12(v+5)=(v+5)(v-5)$, tức $24v=v^2-25$.",
          r"$v^2-24v-25=0$ cho $v=25$ hoặc $v=-1$ (loại).", r"Tốc độ riêng của canô là $25\ \text{km/h}$.")),
 ("Khó", L(r"Một người bơi ngược dòng nước đánh rơi một chiếc mũ nổi. Sau $15$ phút người đó mới phát hiện, lập tức quay lại bơi đuổi theo mũ (tốc độ bơi so với nước không đổi) và đuổi kịp mũ ở chỗ cách nơi làm rơi $1{,}5\ \text{km}$. Tính tốc độ dòng nước."),
        L(r"Trong hệ quy chiếu gắn với dòng nước, mũ đứng yên : người bơi ra xa mũ $15$ phút thì bơi quay lại gặp mũ cũng mất $15$ phút.", r"Mũ trôi theo dòng nước suốt $15+15=30$ phút $=0{,}5\ \text{h}$.", r"$v_n=\dfrac{1{,}5}{0{,}5}=3\ \text{km/h}$.")),
 ("Khó", L(r"Một chiếc thuyền đi từ $A$ đến $B$ xuôi dòng, tổng thời gian đi (kể cả lúc chết máy) là $3$ giờ. Giữa đường thuyền chết máy, trôi tự do theo dòng nước $1$ giờ thì sửa xong, rồi chạy tiếp $1$ giờ nữa thì tới $B$. Tốc độ dòng nước là $2\ \text{km/h}$ ; tốc độ thuyền khi nước yên lặng là $8\ \text{km/h}$. Nếu thuyền không chết máy thì đi từ $A$ đến $B$ mất bao lâu?"),
        L(r"Tốc độ xuôi dòng khi chạy : $8+2=10\ \text{km/h}$.", r"Thời gian chạy bình thường : $3-1=2\ \text{h}$ ($1\ \text{h}$ trước và $1\ \text{h}$ sau lúc chết máy). Khi chết máy thuyền trôi $2\cdot1=2\ \text{km}$.",
          r"$AB=10\cdot2+2=22\ \text{km}$.", r"Không chết máy : $t=\dfrac{22}{10}=2{,}2\ \text{h}$ ($2$ giờ $12$ phút).")),
 ("Khó", L(r"Một người đi từ $A$ đến $B$ gồm đoạn dốc lên $AC$ rồi đoạn dốc xuống $CB$. Lên dốc đi với tốc độ $15\ \text{km/h}$, xuống dốc đi với tốc độ $30\ \text{km/h}$. Thời gian đi từ $A$ đến $B$ là $2{,}5$ giờ, thời gian về từ $B$ đến $A$ là $3{,}5$ giờ. Tính chiều dài $AC$ và $CB$."),
        L(r"Đi : $\dfrac{AC}{15}+\dfrac{CB}{30}=2{,}5$, tức $2\,AC+CB=75$.", r"Về (đoạn $CB$ thành dốc lên, $AC$ thành dốc xuống) : $\dfrac{CB}{15}+\dfrac{AC}{30}=3{,}5$, tức $AC+2\,CB=105$.",
          r"Giải hệ : $AC=15\ \text{km}$ ; $CB=45\ \text{km}$.", r"Kiểm tra : $\dfrac{15}{15}+\dfrac{45}{30}=2{,}5$ ✓ ; $\dfrac{45}{15}+\dfrac{15}{30}=3{,}5$ ✓.")),
 ("Khó", L(r"Một người đứng ở điểm $A$ trên bờ sông rộng $60\ \text{m}$ muốn bơi sang điểm $B$ ở bờ đối diện ($AB$ vuông góc với bờ). Tốc độ bơi của người so với nước là $1{,}5\ \text{m/s}$, tốc độ dòng nước là $0{,}9\ \text{m/s}$.", r"a) Người đó phải bơi theo hướng nào để sang đúng $B$?", r"b) Tính thời gian bơi sang."),
        L(r"a) Vận tốc thực vuông góc với bờ : $v_b\sin\alpha=v_n$ nên $\sin\alpha=\dfrac{0{,}9}{1{,}5}=0{,}6$, $\alpha\approx36{,}9^\circ$ (chếch ngược dòng so với $AB$).",
          r"b) $v=\sqrt{1{,}5^2-0{,}9^2}=\sqrt{1{,}44}=1{,}2\ \text{m/s}$.", r"$t=\dfrac{60}{1{,}2}=50\ \text{s}$.")),
 ("Nâng cao", L(r"Một ôtô và một xe đạp cùng khởi hành từ $A$ đi về $B$ trên đường thẳng, $AB=60\ \text{km}$. Xe đạp có tốc độ không đổi $30\ \text{km/h}$. Ôtô ban đầu chạy với tốc độ $60\ \text{km/h}$ ; sau khi chạy được thời gian $t_1$ thì dừng nghỉ $45$ phút rồi chạy tiếp về $B$ với tốc độ $45\ \text{km/h}$. Ôtô đến $B$ cùng lúc với xe đạp.",
                 r"a) Vẽ đồ thị toạ độ – thời gian của hai xe trên cùng hệ trục.", r"b) Tìm $t_1$."),
        L(r"a) Xe đạp đến $B$ sau $\dfrac{60}{30}=2\ \text{h}$ : đoạn thẳng từ $(0;0)$ đến $(2;60)$.", r"Ôtô gồm ba đoạn : $(0;0)\to(t_1;60t_1)$ ; đoạn nằm ngang dài $0{,}75\ \text{h}$ ; rồi đến $(2;60)$ với độ dốc $45\ \text{km/h}$.",
          r"b) Ôtô nghỉ $0{,}75\ \text{h}$ nên chạy tổng cộng $2-0{,}75=1{,}25\ \text{h}$ : $t_3=1{,}25-t_1$.", r"$60\,t_1+45\,(1{,}25-t_1)=60$, tức $15\,t_1=3{,}75$.", r"$t_1=0{,}25\ \text{h}=15$ phút.",
          r"Kiểm tra : $s_1=60\cdot0{,}25=15\ \text{km}$ ; $t_3=1\ \text{h}$, $s_3=45\ \text{km}$ ; $15+45=60\ \text{km}$ ✓. Ôtô nghỉ từ phút $15$ đến phút $60$ rồi chạy $1\ \text{h}$, đến $B$ lúc $t=2\ \text{h}$.") + g3_fig()),
 ("Nâng cao", L(r"Ba người đi từ thị trấn $A$ đến thị trấn $B$ cách nhau $30\ \text{km}$ với một chiếc xe máy chỉ chở được tối đa hai người (kể cả người lái). Tốc độ đi bộ $5\ \text{km/h}$, tốc độ xe máy $30\ \text{km/h}$. Để cả ba người đến $B$ cùng lúc, người lái chở người thứ hai đi trước một đoạn rồi thả người đó đi bộ tiếp, quay xe lại đón người thứ ba đang đi bộ từ $A$. Coi chuyển động là thẳng đều, thời gian quay xe không đáng kể.",
                  r"a) Tính quãng đường người thứ ba đã đi bộ.", r"b) Tính thời gian cả ba người đi từ $A$ đến $B$."),
        L(r"Gọi $y$ là quãng đường xe chở người thứ hai ; người thứ ba đi bộ quãng $x$ rồi lên xe.",
          r"Người thứ hai : đi xe $y$, đi bộ $30-y$. Người thứ ba : đi bộ $x$, đi xe $30-x$. Hai người cùng đến $B$ một lúc nên $\dfrac{y}{30}+\dfrac{30-y}{5}=\dfrac{x}{5}+\dfrac{30-x}{30}$, suy ra $(x+y-30)\left(\dfrac15-\dfrac1{30}\right)=0$.",
          r"Vậy $x+y=30$ : hai người đi bộ cùng một quãng $x$, và $y=30-x$.",
          r"Xe máy gặp người thứ ba tại điểm cách $A$ đoạn $x$ : người thứ ba mất $\dfrac x5$ để đi bộ tới đó ; xe máy đi $y$ rồi quay về $y-x$ nên mất $\dfrac{y+(y-x)}{30}=\dfrac{2y-x}{30}$.",
          r"$\dfrac x5=\dfrac{2(30-x)-x}{30}$, suy ra $6x=60-3x$ và $9x=60$.",
          r"$x=\dfrac{60}{9}=\dfrac{20}{3}\approx6{,}67\ \text{km}$.", r"a) Người thứ ba đi bộ $\dfrac{20}{3}\ \text{km}\approx6{,}67\ \text{km}$ ; xe chở người thứ hai $y=30-\dfrac{20}{3}=\dfrac{70}{3}\ \text{km}$.",
          r"b) $t=\dfrac y{30}+\dfrac x5=\dfrac{70/3}{30}+\dfrac{20/3}{5}=\dfrac79+\dfrac43=\dfrac{19}{9}\ \text{h}\approx2$ giờ $6$ phút $40$ giây.")),
 ("Nâng cao", L(r"Hai canô khởi hành cùng lúc từ hai điểm $A$ và $B$ ở hai đầu một đường kính của một hồ nước hình tròn. Canô $1$ chạy đều theo chiều kim đồng hồ, canô $2$ chạy đều ngược chiều kim đồng hồ. Lần gặp nhau thứ nhất cách $A$ một cung dài $150\ \text{m}$ ; lần gặp nhau thứ hai cách $B$ một cung dài $90\ \text{m}$. Tính chu vi hồ (có ba kết quả thoả mãn đề)."),
        L(r"Gọi $C$ là chu vi. Lần gặp thứ nhất : hai canô chạy ngược chiều, tổng quãng đường là nửa vòng $\dfrac C2$, trong đó canô $1$ đi $150\ \text{m}$ : $\dfrac{v_1}{v_1+v_2}=\dfrac{150}{C/2}=\dfrac{300}{C}$.",
          r"Từ lần gặp thứ nhất đến lần gặp thứ hai, tổng quãng đường hai canô đi được là một vòng $C$, nên canô $1$ đi thêm $C\cdot\dfrac{300}{C}=300\ \text{m}$.", r"Vậy từ $A$ đến lần gặp thứ hai, canô $1$ đi tổng cộng $150+300=450\ \text{m}$.",
          r"Lần gặp thứ hai cách $B$ một cung $90\ \text{m}$ (cung ngắn, $90\le\dfrac C2$). Vị trí của canô $1$ sau khi đi $450\ \text{m}$ kể từ $A$ có ba khả năng :", r"(i) Chưa tới $B$ : $\dfrac C2-90=450$ nên $C=1080\ \text{m}$.", r"(ii) Đã qua $B$, chưa hết vòng : $\dfrac C2+90=450$ nên $C=720\ \text{m}$.", r"(iii) Đã chạy hết một vòng, qua $A$ rồi mới tới chỗ gặp, còn cách $B$ cung $90\ \text{m}$ : $450-C=\dfrac C2-90$ nên $C=360\ \text{m}$. (Trường hợp $450-C=\dfrac C2+90$ cho $C=240\ \text{m}$ không thoả $C\gt300\ \text{m}$ nên loại.)",
          r"Kiểm tra (ii) : $\dfrac{v_1}{v_1+v_2}=\dfrac{300}{720}=\dfrac5{12}$ ; lần $1$ canô $1$ đi $150\ \text{m}$, canô $2$ đi $210\ \text{m}$, tổng $360=\dfrac C2$ ✓.", r"Kiểm tra (i) : $\dfrac{300}{1080}=\dfrac5{18}$ ; lần $1$ canô $1$ đi $150\ \text{m}$, canô $2$ đi $390\ \text{m}$, tổng $540=\dfrac C2$ ✓.",
          r"Kiểm tra (iii) : $\dfrac{300}{360}=\dfrac56$ nên $v_1:v_2=5:1$ ; lần $1$ canô $1$ đi $150\ \text{m}$, canô $2$ đi $30\ \text{m}$, tổng $180=\dfrac C2$ ✓ ; đến lần $2$ canô $1$ đi $450\ \text{m}$ ($=360+90$, đã vượt một vòng), canô $2$ đi $90\ \text{m}$ và cách $B$ đúng $90\ \text{m}$ ✓.",
          r"Đáp số : ba kết quả $C=360\ \text{m}$, $C=720\ \text{m}$ hoặc $C=1080\ \text{m}$.")),
 ("Nâng cao", L(r"Trong phòng thực hành có một máng nghiêng thẳng, một viên bi thép nhỏ, một thước thẳng có độ chia nhỏ nhất $1\ \text{mm}$, một thước kẹp (hoặc panme) để đo đường kính viên bi, hai cổng quang điện $E$ và $F$ nối với đồng hồ đo thời gian hiện số (độ chính xác $0{,}001\ \text{s}$).",
                  r"a) Trình bày các bước bố trí và tiến hành thí nghiệm để đo vận tốc trung bình của viên bi trên đoạn $EF$ và vận tốc tức thời của viên bi khi qua cổng $E$.", r"b) Thiết lập công thức tính sai số của phép đo vận tốc trung bình.", r"c) Làm thế nào để kiểm tra chuyển động của viên bi trên máng là nhanh dần hay đều?"),
        L(r"<strong>a) Vận tốc trung bình trên $EF$.</strong>", r"Bước 1 : đặt máng nghiêng một góc nhỏ so với mặt bàn, gắn hai cổng $E$, $F$ trên máng cách nhau một đoạn $s$ (khoảng $30$–$50\ \text{cm}$).",
          r"Bước 2 : nối cổng $E$ vào ổ $A$, cổng $F$ vào ổ $B$ của đồng hồ ; chọn chế độ đo thời gian từ lúc chắn cổng $E$ đến lúc chắn cổng $F$.", r"Bước 3 : dùng thước thẳng đo khoảng cách $s$ giữa hai cổng.",
          r"Bước 4 : thả viên bi không vận tốc đầu từ một vạch đánh dấu cố định trên máng ; đọc thời gian $t$ trên đồng hồ.", r"Bước 5 : lặp lại $5$ lần, lấy giá trị trung bình $t_{tb}$ ; tính $v_{tb}=\dfrac{s}{t_{tb}}$.",
          r"<strong>Vận tốc tức thời tại $E$.</strong>", r"Chuyển đồng hồ sang chế độ đo thời gian bi chắn riêng cổng $E$ : $\Delta t_E$. Đo đường kính $d$ của bi bằng thước kẹp.", r"$v_E\approx\dfrac{d}{\Delta t_E}$ (chính xác hơn khi $\Delta t_E$ càng nhỏ).",
          r"<strong>b) Sai số.</strong>", r"$v=\dfrac st$ nên sai số tương đối $\delta v=\delta s+\delta t=\dfrac{\Delta s}{s_{tb}}+\dfrac{\Delta t}{t_{tb}}$.", r"Sai số tuyệt đối $\Delta v=v_{tb}\cdot\delta v$ ; ghi kết quả $v=v_{tb}\pm\Delta v$ (kèm đơn vị m/s).",
          r"<strong>c) Kiểm tra tính chất chuyển động.</strong>", r"Chia máng thành ba đoạn liên tiếp dài bằng nhau $s_1=s_2=s_3$ ; đo thời gian bi đi qua từng đoạn : $t_1$, $t_2$, $t_3$.",
          r"Nếu $t_1=t_2=t_3$ : chuyển động đều.", r"Nếu $t_1\gt t_2\gt t_3$ : vận tốc tăng dần, chuyển động nhanh dần.")),
]

def tu_luan():
    parts = []
    for k, (muc, de, gi) in enumerate(TL, 1):
        parts.append(f"<h4>Bài {k} · {muc}</h4>{de}<details><summary>Hướng dẫn giải</summary>{gi}</details>")
    return dict(label="Bài tập tự luận (xếp từ dễ đến khó)",
                body_html="<p>Các bài còn lại của chuyên đề, xếp từ dễ đến khó. Tự giải trên giấy rồi mới mở hướng dẫn.</p>" + "".join(parts))


# ═════════════ TỰ KIỂM SỐ LIỆU (độc lập với chữ trong đề) ═════════════
def kiem_so():
    F = Fr
    # D1
    t_a = F(12, 12) + F(12, 24); assert t_a == F(3, 2) and F(24) / t_a == 16
    assert (12 + 24) / 2 == 18 and 2 * 12 * 24 / (12 + 24) == 16 and F(48) / (2 * t_a) == 16
    tb = F(24, 18); assert 12 * tb / 2 + 24 * tb / 2 == 24
    # D2
    t = F(150, 60 + 40); assert t == F(3, 2) and 60 * t == 90 == 150 - 40 * t
    assert [x for x in (F(120, 100), F(180, 100)) if abs((150 - 40 * x) - 60 * x) == 30] == [F(6, 5), F(9, 5)]
    assert 150 - 40 * F(150, 60) == 50
    # D3
    v1, v2 = F(54 * 10, 36), F(10); assert v1 == 15
    assert F(180) / v1 == 12 and F(600) / v1 == 40 and F(320) / (v1 + v2) == F(64, 5) and F(320) / (v1 - v2) == 64
    # D4
    vx, vng = F(90, 3), F(90, 5); vn = (vx - vng) / 2; vt = (vx + vng) / 2
    assert (vx, vng, vn, vt) == (30, 18, 6, 24) and F(90) / vn == 15 and 2 * 3 * 5 / (5 - 3) == 15
    assert vn * (F(20, 60) + F(20, 60)) == 4
    d_sep = (vt - vn) * F(20, 60) + vn * F(20, 60)            # canô đi ngược 18·(1/3) = 6 km, phao trôi xuống 2 km
    assert d_sep == 8 and d_sep / (vt + vn - vn) == F(1, 3)
    # D5
    xA = lambda t: 60 * t if t <= 1 else (60 if t <= F(3, 2) else 60 + 60 * (t - F(3, 2)))
    xB = lambda t: 120 - 30 * t
    tg = F(150, 90); assert tg == F(5, 3) and F(3, 2) <= tg <= 3 and xA(tg) == xB(tg) == 70
    assert xA(F(2)) == 90 and F(4, 3) > 1 and F(2) > F(3, 2)
    # D6
    assert F(12, 20) == F(3, 5); v = math.sqrt(2.0 ** 2 - 1.2 ** 2)
    assert abs(v - 1.6) < 1e-9 and abs(96 / v - 60) < 1e-9 and 96 / 2.0 == 48 and abs(1.2 * 48 - 57.6) < 1e-9
    # tự luận
    assert F(120, 50) == F(12, 5) and 40 * 1.2 + 60 * 1.2 == 120 and F(24, 5) == F(48, 10)
    assert sum(range(2, 21, 2)) == 110 and 2 * 16 - 2 == 30
    assert F(350, 20) == F(35, 2)
    assert F(1, 60) + F(1, 90) + F(1, 180) == F(1, 30)
    assert F(90, 45) == 2 and F(90, 30) - F(1, 2) == F(5, 2)
    assert F(15, 35 - 15) == F(3, 4) and 35 * F(3, 4) == F(105, 4) and F(5, 20) == F(1, 4) and F(25, 20) == F(5, 4) and 35 * F(5, 4) == F(175, 4) < 70
    assert F(30, 12 + 18) == 1
    assert F(200, 40) == 5 and F(200, 8) == 25 and (5 + 25) / 2 == 15 and (25 - 5) / 2 == 10
    assert 2 * F(3, 2) * F(5, 2) / (F(5, 2) - F(3, 2)) == F(15, 2)
    assert F(12, 11) * 60 == F(720, 11) and F(3, 11) * 3600 == F(10800, 11) and F(6, 11) * 60 == F(360, 11)
    v = 25; assert F(60, v + 5) + F(60, v - 5) == 5
    assert 1.5 / 0.5 == 3
    assert 10 * 2 + 2 * 1 == 22 and F(22, 10) == F(11, 5)
    assert F(15, 15) + F(45, 30) == F(5, 2) and F(45, 15) + F(15, 30) == F(7, 2)
    assert math.isclose(math.sqrt(1.5 ** 2 - 0.9 ** 2), 1.2) and 60 / 1.2 == 50
    assert 60 * F(1, 4) + 45 * (F(5, 4) - F(1, 4)) == 60 and F(1, 4) + F(3, 4) + 1 == 2
    # G1
    s_, a, b_ = F(30), F(5), F(30); x = 2 * a * s_ / (b_ + 3 * a); y = s_ - x
    assert x == F(20, 3) and y == F(70, 3) and y / b_ + x / a == F(19, 9) == x / a + (s_ - x) / b_
    assert x / a == (y + (y - x)) / b_
    # G2
    nghiem = []
    for C in range(302, 3001):                         # dò trực tiếp: lần 1 cách A cung 150, lần 2 cách B cung 90
        r = F(300, C); p = (r * F(3 * C, 2)) % C; dl = abs(p - F(C, 2))
        if min(dl, C - dl) == 90: nghiem.append(C)
    assert nghiem == [360, 720, 1080], nghiem
    print("kiểm số liệu: đạt")

kiem_so()

# ═════════════ GHI FILE ═════════════
write(J, 162, "Chuyên đề 13. Chuyển động cơ học và đồ thị chuyển động", DANG, BUILD, ANALYSIS, SOLS, tu_luan())
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-10"
d["review"] = {"checked": False, "notes": "Soạn 10/10/2026 (lesson_id 162). Chờ kiểm chéo độc lập (kiem-code): tự giải từng dạng + kiểm buoc[]."}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
print("xong", J)
