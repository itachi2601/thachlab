"""Bài tập mẫu CĐ06 "Khúc xạ ánh sáng, phản xạ toàn phần, lăng kính và tán sắc" (lesson 151) — Dạng 1–3. Module được build-hinh-151.py import.
Dàn ý + số liệu đã tính: content/hsg9/cd06-khuc-xa-phan-xa-toan-phan/nguon.md (mục "Bài tập mẫu", D1–D3 dùng nguyên số; tinh.py).
Quy ước: góc đo so với PHÁP TUYẾN; n_kk = 1; n_nước = 4/3; c = 3·10^8 m/s; $n_1\sin i=n_2\sin r$.
Thầy chốt 17/10/2026: BỎ ý D1(d) góc Brewster.
Mọi đáp số tính lại bằng Python trong kiem_so(); mọi lựa chọn sai của chon_buoc_ke được assert cho số khác đáp án đúng."""
import math
from dung import *   # sol, buoc, M/P/A, fig, seg, lbl, poly, arc, arrow, chevron, RED/BLUE/ORG/GRN

GREY = "#94a3b8"
YEL = "#facc15"
TOPIC_KX = "Chiết suất và định luật khúc xạ ánh sáng"
TOPIC_MT = "Mô tả hiện tượng khúc xạ, vẽ đường truyền tia sáng"
TOPIC_PX = "Điều kiện xảy ra phản xạ toàn phần"
C_AS = 3e8
N_W = 4 / 3


def sind(a):
    return math.sin(math.radians(a))


def tand(a):
    return math.tan(math.radians(a))


def asind(x):
    return math.degrees(math.asin(x))


# số liệu D1
I1, R1_ = 60, 36
N1 = sind(I1) / sind(R1_)                 # ≈ 1,4734
V1 = C_AS / N1                            # ≈ 2,04·10^8 m/s
SIN_RB = N1 * sind(30)                    # ≈ 0,7367
R_B = asind(SIN_RB)                       # ≈ 47,4°
GOC_C = 180 - I1 - R1_                    # 84°
# số liệu D2
N_DAU, E_DAU, E_NUOC, H_CA, H_DEN = 1.4, 14, 80, 36, 150
H_DAY = E_DAU / N_DAU + E_NUOC / N_W      # 70 cm
NANG = E_DAU + E_NUOC - H_DAY             # 24 cm
H_CA_BK = E_DAU / N_DAU + H_CA / N_W      # 37 cm
D_DEN = N_W * (H_CA / N_W + E_DAU / N_DAU + H_DEN)   # ≈ 249,3 cm
CAO_DEN = D_DEN - H_CA - E_DAU            # ≈ 199,3 cm
# số liệu D3
H3 = 0.9
IGH = asind(1 / N_W)                      # ≈ 48,6°
R3 = H3 * tand(IGH)                       # ≈ 1,02 m
S3 = math.pi * R3 ** 2                    # ≈ 3,27 m²
IGH16 = asind(1 / 1.6)                    # ≈ 38,7°
R3B = H3 * tand(IGH16)                    # ≈ 0,72 m
R_DIA = 0.5
H_MAX = R_DIA / tand(IGH)                 # ≈ 0,44 m


def anim(attr, vals, dur, kt=None):
    k = f' keyTimes="{kt}"' if kt else ""
    return f'<animate attributeName="{attr}" values="{vals}"{k} dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>'


def ray(x1, y1, x2, y2, c=RED, w=2.4, dash=""):
    """Tia sáng: nét liền + đầu V ở giữa tia (quy ước hình quang của khoá)."""
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    return seg(x1, y1, x2, y2, c, w, dash) + chevron(mx + (x2 - x1) * 0.04, my + (y2 - y1) * 0.04, x2 - x1, y2 - y1, c, w, 10)


def subt(x, y, base, s, c="currentColor", size=14, anchor="start", weight="700", tail=""):
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">'
            f'{base}<tspan dy="4" font-size="12">{s}</tspan><tspan dy="-4">{tail}</tspan></text>')


# ═════════════ HÌNH ═════════════
# ───────────── Dạng 1 · tia laser vào chất lỏng ─────────────
def d1(kk):
    b = ""
    if kk == 0:
        SY, IX = 120, 210
        b += f'<rect x="20" y="{SY}" width="380" height="118" fill="{BLUE}" opacity="0.18" stroke="none"/>'
        b += seg(20, SY, 400, SY, BLUE, 2)
        b += lbl(30, SY - 10, "không khí", "currentColor", 14, "start", "700")
        b += lbl(30, SY + 24, "chất lỏng", BLUE, 14, "start", "700")
        b += lbl(30, SY + 44, "n = ?", BLUE, 14, "start", "700")
        b += seg(IX, 22, IX, 232, GREY, 1.4, "5 4") + lbl(IX + 6, 32, "pháp tuyến", GREY, 14, "start", "400")
        L1, L2 = 120, 116
        sx, sy = IX - L1 * sind(I1), SY - L1 * math.cos(math.radians(I1))
        ex, ey = IX + L2 * sind(R1_), SY + L2 * math.cos(math.radians(R1_))
        # đèn laser (hộp nhỏ dọc theo tia)
        ux, uy = (IX - sx) / L1, (SY - sy) / L1
        bx0, by0 = sx - 30 * ux, sy - 30 * uy
        b += (f'<line x1="{bx0:.1f}" y1="{by0:.1f}" x2="{sx:.1f}" y2="{sy:.1f}" stroke="currentColor" stroke-width="9" stroke-linecap="round"/>')
        b += lbl(bx0 - 2, by0 - 10, "laser", "currentColor", 14, "start", "400")
        b += ray(sx, sy, IX, SY) + ray(IX, SY, ex, ey)
        b += arc(IX, SY, 34, 90, 90 + I1, ORG, 1.8) + lbl(IX - 40, SY - 40, "60°", ORG, 14, "end", "700")
        b += arc(IX, SY, 40, -90, -90 + R1_, GRN, 1.8) + lbl(IX - 8, SY + 56, "36°", GRN, 14, "end", "700")
        # chấm sáng: tốc độ trong chất lỏng = tốc độ trong không khí / n
        V_PX = 60.0                                   # px/s trong không khí
        t1 = L1 / V_PX
        t2 = L2 / (V_PX / N1)
        DUR = t1 + t2
        kt = f"0;{t1 / DUR:.4f};1"
        b += (f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="5.5" fill="{YEL}" stroke="currentColor" stroke-width="1.5">'
              f'{anim("cx", f"{sx:.1f};{IX};{ex:.1f}", DUR, kt)}{anim("cy", f"{sy:.1f};{SY};{ey:.1f}", DUR, kt)}</circle>')
        return fig("c06-1-0", "0 0 420 240",
                   "Tia laser từ không khí tới mặt chất lỏng với góc tới 60 độ, khúc xạ vào chất lỏng với góc khúc xạ 36 độ, chiết suất chưa biết",
                   b, "Mô phỏng: chấm sáng đi theo tia tới rồi theo tia khúc xạ; vào chất lỏng nó đi chậm lại. "
                      "Hai góc vẽ đúng số liệu đề cho, đo so với pháp tuyến. Phần ánh sáng phản xạ chưa vẽ.")
    # hình dữ kiện: sơ đồ ba tia (góc vẽ không theo số liệu đề)
    SY, IX = 100, 210
    b += f'<rect x="20" y="{SY}" width="380" height="96" fill="{BLUE}" opacity="0.18" stroke="none"/>' + seg(20, SY, 400, SY, BLUE, 2)
    b += seg(IX, 14, IX, 192, GREY, 1.4, "5 4")
    a_i, a_r, L = 50, 30, 92
    sx, sy = IX - L * sind(a_i), SY - L * math.cos(math.radians(a_i))
    px, py = IX + L * sind(a_i), SY - L * math.cos(math.radians(a_i))
    ex, ey = IX + L * sind(a_r), SY + L * math.cos(math.radians(a_r))
    b += ray(sx, sy, IX, SY) + ray(IX, SY, px, py, RED, 2.0) + ray(IX, SY, ex, ey)
    b += arc(IX, SY, 30, 90, 90 + a_i, ORG, 1.6) + lbl(IX - 26, SY - 34, "i", ORG, 15, "end", "700")
    b += arc(IX, SY, 30, 90 - a_i, 90, ORG, 1.6) + lbl(IX + 26, SY - 34, "i'", ORG, 15, "start", "700")
    b += arc(IX, SY, 34, -90, -90 + a_r, GRN, 1.6) + lbl(IX - 8, SY + 46, "r", GRN, 15, "end", "700")
    b += arc(IX, SY, 58, -90 + a_r, 90 - a_i, RED, 1.6) + lbl(IX + 76, SY + 6, "?", RED, 16, "start", "700")
    b += lbl(px + 4, py - 4, "tia phản xạ", "currentColor", 14, "start", "400")
    b += lbl(ex + 6, ey + 4, "tia khúc xạ", "currentColor", 14, "start", "400")
    b += lbl(sx - 4, sy - 6, "tia tới", "currentColor", 14, "end", "400")
    return fig("c06-1-2", "0 0 420 200",
               "Sơ đồ tia tới, tia phản xạ và tia khúc xạ tại một điểm tới, các góc i, i phẩy, r đo so với pháp tuyến, góc giữa tia phản xạ và tia khúc xạ là ẩn",
               b, "Sơ đồ ba tia tại điểm tới (góc vẽ không theo số liệu của đề). Dấu ? là góc câu c hỏi.")


# ───────────── Dạng 2 · độ sâu biểu kiến qua hai lớp ─────────────
def d2_rays(Y0, Y1, Y2, X, tw, back_to=None):
    """Tia từ S(X, Y2) đi lên: nước góc tw, dầu, không khí — góc tính bằng định luật khúc xạ thật.
    Độ dày lớp vẽ KHÔNG theo tỉ lệ đề. Trả (danh sách điểm phải, góc không khí, độ dịch ngang ở mặt dầu)."""
    so = N_W * sind(tw) / N_DAU
    ta = asind(N_DAU * so)
    to = asind(so)
    x1 = X + (Y2 - Y1) * tand(tw)
    x0 = x1 + (Y1 - Y0) * tand(to)
    return (X, Y2), (x1, Y1), (x0, Y0), ta


def d2(kk):
    b = ""
    X0, X1 = 70, 350
    Y0, Y1, Y2 = 72, 118, 244          # mặt dầu, mặt dầu–nước, đáy (không theo tỉ lệ)
    XC = 210
    if kk == 0:
        b += f'<rect x="{X0}" y="{Y0}" width="{X1 - X0}" height="{Y1 - Y0}" fill="{ORG}" opacity="0.22" stroke="none"/>'
        b += f'<rect x="{X0}" y="{Y1}" width="{X1 - X0}" height="{Y2 - Y1}" fill="{BLUE}" opacity="0.18" stroke="none"/>'
        b += seg(X0, Y0, X1, Y0, ORG, 1.8) + seg(X0, Y1, X1, Y1, BLUE, 1.6)
        b += f'<path d="M{X0},{Y0 - 30} L{X0},{Y2} L{X1},{Y2} L{X1},{Y0 - 30}" fill="none" stroke="currentColor" stroke-width="2.4"/>'
        b += lbl(X1 + 6, Y0 + 20, "dầu", ORG, 14, "start", "700") + lbl(X1 + 6, Y0 + 38, "14 cm", "currentColor", 14, "start", "400")
        b += lbl(X1 + 6, Y1 + 40, "nước", BLUE, 14, "start", "700") + lbl(X1 + 6, Y1 + 58, "80 cm", "currentColor", 14, "start", "400")
        b += seg(XC, Y0 - 26, XC, Y2, GREY, 1.2, "5 4")
        # mắt nhìn từ trên xuống
        b += (f'<path d="M{XC - 16},{20} Q{XC},{6} {XC + 16},{20} Q{XC},{34} {XC - 16},{20} Z" fill="none" stroke="currentColor" stroke-width="2"/>'
              f'<circle cx="{XC}" cy="20" r="4.5" fill="currentColor"/>')
        b += lbl(XC + 24, 24, "mắt", "currentColor", 14, "start", "400")
        b += f'<circle cx="{XC}" cy="{Y2 - 2}" r="5" fill="{RED}" stroke="currentColor" stroke-width="1.2"/>'
        b += lbl(XC - 10, Y2 - 8, "S", RED, 15, "end", "700")
        DUR = 4.0
        S, P1, P0, ta = d2_rays(Y0, Y1, Y2, XC, 16)
        LA = 46
        tops = []
        for sg in (1, -1):
            p1 = (XC + sg * (P1[0] - XC), Y1); p0 = (XC + sg * (P0[0] - XC), Y0)
            top = (p0[0] + sg * LA * sind(ta), Y0 - LA * math.cos(math.radians(ta)))
            tops.append(top)
            path = [S, p1, p0, top]
            L = sum(math.hypot(q[0] - p[0], q[1] - p[1]) for p, q in zip(path, path[1:]))
            b += (f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in path)}" fill="none" stroke="{RED}" stroke-width="2.2" '
                  f'stroke-dasharray="{L + 2:.1f}" stroke-dashoffset="{L + 2:.1f}">{anim("stroke-dashoffset", f"{L + 2:.1f};0;0", DUR, "0;0.55;1")}</polyline>')
            b += (f'<g opacity="0">{anim("opacity", "0;0;1", DUR, "0;0.55;1")}'
                  f'{chevron((p1[0] + p0[0]) / 2, (Y1 + Y0) / 2, p0[0] - p1[0], Y0 - Y1, RED, 2.2, 9)}'
                  f'{chevron((p0[0] + top[0]) / 2, (Y0 + top[1]) / 2, top[0] - p0[0], top[1] - Y0, RED, 2.2, 9)}</g>')
        # đường kéo dài (nét đứt) gặp nhau ở ảnh S'
        yi = Y0 + (P0[0] - XC) / tand(ta)
        ext = "".join(seg(XC + sg * (P0[0] - XC), Y0, XC, yi, RED, 1.6, "5 4") for sg in (1, -1))
        b += (f'<g opacity="0">{anim("opacity", "0;0;1;1", DUR, "0;0.6;0.85;1")}{ext}'
              f'<circle cx="{XC}" cy="{yi:.1f}" r="4.5" fill="none" stroke="{RED}" stroke-width="2"/>'
              f'{seg(XC + 6, yi, XC + 52, yi, GREY, 1.2)}<text x="{XC + 56}" y="{yi + 5:.1f}" fill="{RED}" font-size="15" font-weight="700">S\' = ?</text></g>')
        b += lbl(X0 + 8, Y2 - 10, "đáy", "currentColor", 14, "start", "400")
        return fig("c06-2-0", "0 0 420 256",
                   "Bể có lớp dầu nổi trên lớp nước, tia sáng từ điểm S ở đáy đi lên, gãy khúc ở hai mặt phân cách, đường kéo dài của tia ló cắt nhau ở ảnh S phẩy chưa biết vị trí",
                   b, "Mô phỏng: tia sáng từ đáy đi lên, gãy khúc ở hai mặt phân cách rồi tới mắt; đường kéo dài (nét đứt) cho ảnh S'. "
                      "Góc tia phóng to cho dễ thấy, độ dày các lớp không theo tỉ lệ.")
    # hình dữ kiện: ba tình huống quan sát (không theo tỉ lệ)
    b += f'<rect x="{X0}" y="{Y0}" width="{X1 - X0 - 120}" height="{Y1 - Y0}" fill="{ORG}" opacity="0.22" stroke="none"/>'
    b += f'<rect x="{X0}" y="{Y1}" width="{X1 - X0 - 120}" height="{Y2 - Y1}" fill="{BLUE}" opacity="0.18" stroke="none"/>'
    XR = X1 - 120
    b += seg(X0, Y0, XR, Y0, ORG, 1.8) + seg(X0, Y1, XR, Y1, BLUE, 1.6) + seg(X0, Y2, XR, Y2, "currentColor", 2.2)
    b += lbl(X0 + 6, Y0 + 20, "dầu n = 1,4", ORG, 14, "start", "700")
    b += lbl(X0 + 6, Y1 + 20, "nước n = 4/3", BLUE, 14, "start", "700")
    xd = 150
    b += seg(xd, 18, xd, Y0, GREY, 1.2, "4 3")
    b += f'<circle cx="{xd}" cy="18" r="6" fill="{YEL}" stroke="currentColor" stroke-width="1.4"/>' + lbl(xd + 10, 22, "đèn", "currentColor", 14, "start", "400")
    yc = 176
    b += (f'<path d="M{xd - 14},{yc} Q{xd},{yc - 9} {xd + 12},{yc} Q{xd},{yc + 9} {xd - 14},{yc} Z M{xd + 12},{yc} L{xd + 20},{yc - 6} L{xd + 20},{yc + 6} Z" '
          f'fill="none" stroke="currentColor" stroke-width="1.8"/>') + lbl(xd - 20, yc + 5, "cá", "currentColor", 14, "end", "400")
    XD = XR + 14
    for ya, yb, s in ((Y0, Y1, "14 cm"), (Y1, Y2, "80 cm")):
        b += arrow("", "o", XD, (ya + yb) / 2, XD, ya + 2, 1.6) + arrow("", "o", XD, (ya + yb) / 2, XD, yb - 2, 1.6)
        b += lbl(XD + 6, (ya + yb) / 2 + 5, s, "currentColor", 14, "start", "700")
    b += arrow("", "o", xd + 30, (Y1 + yc) / 2, xd + 30, Y1 + 2, 1.6) + arrow("", "o", xd + 30, (Y1 + yc) / 2, xd + 30, yc - 2, 1.6)
    b += lbl(xd + 36, (Y1 + yc) / 2 + 5, "36 cm", "currentColor", 14, "start", "700")
    b += arrow("", "o", xd + 30, (18 + Y0) / 2, xd + 30, 20, 1.6) + arrow("", "o", xd + 30, (18 + Y0) / 2, xd + 30, Y0 - 2, 1.6)
    b += lbl(xd + 36, (18 + Y0) / 2 + 5, "150 cm", "currentColor", 14, "start", "700")
    b += lbl(XD + 54, 60, "a), b) mắt ở", "currentColor", 14, "start", "400") + lbl(XD + 54, 78, "không khí", "currentColor", 14, "start", "400")
    b += lbl(XD + 54, 96, "nhìn đáy, cá", "currentColor", 14, "start", "400")
    b += lbl(XD + 54, 150, "c) mắt cá", BLUE, 14, "start", "700") + lbl(XD + 54, 168, "ở trong nước", BLUE, 14, "start", "700")
    b += lbl(XD + 54, 186, "nhìn đèn", BLUE, 14, "start", "700")
    return fig("c06-2-2", "0 0 420 256",
               "Sơ đồ bể: lớp dầu 14 xăng-ti-mét chiết suất 1,4 trên lớp nước 80 xăng-ti-mét chiết suất bốn phần ba, cá dưới mặt dầu nước 36 xăng-ti-mét, đèn cao 150 xăng-ti-mét trên mặt dầu",
               b, "Dữ kiện (không theo tỉ lệ): mắt người ở không khí, mắt cá ở trong nước. Chỉ các lớp nằm giữa vật và mắt mới làm ảnh dịch chỗ.")


# ───────────── Dạng 3 · vùng sáng tròn trên mặt nước ─────────────
TH_VE = 40.0                     # góc giới hạn VẼ minh hoạ (không theo số liệu đề)
N_VE = 1 / sind(TH_VE)


def d3(kk):
    b = ""
    if kk == 0:
        SY, BY, XC = 70, 176, 210
        HP = BY - SY
        b += f'<rect x="20" y="{SY}" width="380" height="{HP}" fill="{BLUE}" opacity="0.18" stroke="none"/>'
        b += seg(20, SY, 400, SY, BLUE, 2) + seg(20, BY, 400, BY, "currentColor", 2.4)
        b += lbl(26, SY - 10, "không khí", "currentColor", 14, "start", "700") + lbl(26, BY - 10, "nước", BLUE, 14, "start", "700")
        b += f'<circle cx="{XC}" cy="{BY - 4}" r="6" fill="{YEL}" stroke="currentColor" stroke-width="1.4"/>'
        b += lbl(XC, BY + 18, "đèn", "currentColor", 14, "middle", "700")
        ANG = [8, 18, 28, TH_VE, 48, 55]
        DUR = 7.0
        n_ = len(ANG)
        for k, th in enumerate(ANG):
            t0 = 0.08 + k * 0.14
            show = f'{anim("opacity", "0;0;1;1", DUR, f"0;{t0:.3f};{t0 + 0.06:.3f};1")}'
            g = ""
            for sg in (1,):
                xs = XC + sg * HP * tand(th)
                g += ray(XC, BY - 4, xs, SY, RED, 2.0)
                if th < TH_VE - 0.01:
                    ta = asind(N_VE * sind(th))
                    g += ray(xs, SY, xs + sg * 54 * sind(ta), SY - 54 * math.cos(math.radians(ta)), RED, 2.0)
                    g += seg(xs, SY, xs + sg * 30 * sind(th), SY + 30 * math.cos(math.radians(th)), RED, 1.2, "", 0.35)
                elif th <= TH_VE + 0.01:
                    g += ray(xs, SY, xs + sg * 44, SY - 3, RED, 2.0)
                else:
                    g += ray(xs, SY, xs + sg * 40 * sind(th), SY + 40 * math.cos(math.radians(th)), RED, 2.0)
            b += f'<g opacity="0">{show}{g}</g>'
        xr = XC + HP * tand(TH_VE)
        t_end = 0.08 + n_ * 0.14
        b += (f'<g opacity="0">{anim("opacity", "0;0;1", DUR, f"0;{min(t_end, 0.96):.3f};1")}'
              f'<line x1="{2 * XC - xr:.1f}" y1="{SY}" x2="{xr:.1f}" y2="{SY}" stroke="{YEL}" stroke-width="7" stroke-linecap="round" opacity="0.9"/>'
              f'<text x="{XC - 60}" y="{SY + 30}" fill="currentColor" font-size="15" font-weight="700" text-anchor="middle">vùng sáng</text>'
              f'<text x="{XC - 60}" y="{SY + 50}" fill="currentColor" font-size="15" font-weight="700" text-anchor="middle">bán kính R = ?</text></g>')
        return fig("c06-3-0", "0 0 420 200",
                   "Đèn ở đáy bể nước phát tia theo nhiều hướng, tia gần phương thẳng đứng ló ra không khí, tia nghiêng nhiều bị phản xạ toàn phần, trên mặt nước hiện vùng sáng tròn chưa biết bán kính",
                   b, "Mô phỏng (vẽ nửa bên phải, nửa trái đối xứng): lần lượt các tia nghiêng dần. Tia nghiêng ít ló ra không khí (kèm một phần phản xạ mờ); tới một góc thì tia ló đi là là mặt nước; "
                      "nghiêng hơn nữa thì phản xạ toàn phần. Góc vẽ minh hoạ, không theo số liệu của đề.")
    # hình dữ kiện
    SY, BY, XC = 54, 196, 170
    HP = BY - SY
    b += f'<rect x="20" y="{SY}" width="320" height="{HP}" fill="{BLUE}" opacity="0.18" stroke="none"/>'
    b += seg(20, SY, 340, SY, BLUE, 2) + seg(20, BY, 340, BY, "currentColor", 2.4)
    xr = XC + HP * tand(TH_VE)
    b += f'<rect x="{2 * XC - xr:.1f}" y="{SY - 7}" width="{2 * (xr - XC):.1f}" height="6" fill="currentColor" opacity="0.75"/>'
    b += lbl(XC, SY - 14, "đĩa chắn", "currentColor", 14, "middle", "700")
    b += f'<circle cx="{XC}" cy="{BY - 4}" r="6" fill="{YEL}" stroke="currentColor" stroke-width="1.4"/>' + lbl(XC - 10, BY + 16, "S", "currentColor", 15, "end", "700")
    b += seg(XC, SY, XC, BY - 4, GREY, 1.2, "5 4")
    b += ray(XC, BY - 4, xr, SY, RED, 2.2)
    b += seg(xr, SY - 26, xr, SY + 40, GREY, 1.2, "5 4")
    b += arc(XC, BY - 4, 40, 90 - TH_VE, 90, ORG, 1.6) + subt(XC + 10, BY - 52, "i", "gh", ORG, 15)
    b += arc(xr, SY, 30, -90 - TH_VE, -90, ORG, 1.6) + subt(xr - 30, SY + 46, "i", "gh", ORG, 15)
    b += arrow("", "o", XC - 34, (SY + BY) / 2, XC - 34, SY + 2, 1.6) + arrow("", "o", XC - 34, (SY + BY) / 2, XC - 34, BY - 2, 1.6)
    b += lbl(XC - 40, (SY + BY) / 2 + 5, "h", ORG, 15, "end", "700")
    b += arrow("", "g", (XC + xr) / 2, SY + 14, XC + 2, SY + 14, 1.6) + arrow("", "g", (XC + xr) / 2, SY + 14, xr - 2, SY + 14, 1.6)
    b += lbl((XC + xr) / 2, SY + 32, "R = ?", GRN, 15, "middle", "700")
    b += lbl(348, 90, "Mép vùng", "currentColor", 14, "start", "400") + lbl(348, 108, "sáng: tia", "currentColor", 14, "start", "400")
    b += lbl(348, 126, "tới với", "currentColor", 14, "start", "400") + subt(348, 146, "i = i", "gh", RED, 14)
    return fig("c06-3-2", "0 0 420 216",
               "Sơ đồ mặt cắt: nguồn S ở đáy, tia tới mép vùng sáng hợp với pháp tuyến góc giới hạn, độ sâu h, bán kính R chưa biết, đĩa chắn nổi trên mặt nước",
               b, "Sơ đồ mặt cắt (không theo tỉ lệ): góc tại S bằng góc tới ở mép vùng sáng vì hai pháp tuyến song song.")


BUILD = [d1, d2, d3]

# ═════════════ ĐỀ ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Định luật khúc xạ: chiết suất, tốc độ ánh sáng, chiếu ngược chiều và góc giữa tia phản xạ – tia khúc xạ",
      topic=TOPIC_KX,
      problem_html=r"""<p>Chiếu một tia laser từ không khí tới mặt thoáng phẳng của một chất lỏng trong suốt với góc tới $i=60^{\circ}$; đo được góc khúc xạ $r=36^{\circ}$. Cho $\sin60^{\circ}\approx0{,}8660$; $\sin36^{\circ}\approx0{,}5878$; tốc độ ánh sáng trong không khí $c=3\cdot10^8\ \text{m/s}$, chiết suất không khí bằng $1$. Dùng máy tính khi cần tìm góc từ giá trị sin.</p><ol type="a"><li>Tính chiết suất của chất lỏng và tốc độ ánh sáng trong chất lỏng.</li><li>Chiếu một tia sáng từ trong chất lỏng ra không khí với góc tới $30^{\circ}$. Tính góc khúc xạ. Tia khúc xạ lệch gần hay lệch xa pháp tuyến hơn tia tới?</li><li>Trở lại tia laser ở câu a: tại điểm tới, một phần ánh sáng bị phản xạ trên mặt thoáng. Tính góc hợp bởi tia phản xạ và tia khúc xạ.</li></ol>"""),
 dict(label="Dạng 2 · Trung bình · Độ sâu biểu kiến qua nhiều lớp chất lỏng: người nhìn xuống đáy, cá nhìn lên đèn",
      topic=TOPIC_MT,
      problem_html=r"""<p>Một bể chứa lớp nước dày $80\ \text{cm}$; trên mặt nước nổi một lớp dầu dày $14\ \text{cm}$. Chiết suất của dầu là $1{,}4$, của nước là $\dfrac43$, của không khí là $1$. Mọi lần quan sát đều nhìn theo phương gần vuông góc với mặt chất lỏng.</p><ol type="a"><li>Một người ở trên nhìn thẳng xuống đáy bể. Đáy bể trông như cách mặt dầu bao nhiêu? Đáy bể như được nâng lên bao nhiêu?</li><li>Một con cá nằm trong nước, ở dưới mặt phân cách dầu – nước $36\ \text{cm}$. Người đó thấy cá như cách mặt dầu bao nhiêu?</li><li>Ngay phía trên con cá, cách mặt dầu $150\ \text{cm}$, treo một bóng đèn nhỏ. Con cá nhìn lên thấy bóng đèn như cách nó bao nhiêu, và như ở độ cao bao nhiêu so với mặt dầu (mặt phẳng thật của lớp dầu)?</li></ol>"""),
 dict(label="Dạng 3 · Trung bình · Phản xạ toàn phần: vùng sáng tròn trên mặt nước và đĩa chắn sáng",
      topic=TOPIC_PX,
      problem_html=r"""<p>Một bóng đèn nhỏ (coi là nguồn sáng điểm) đặt ở đáy một bể nước sâu $0{,}9\ \text{m}$. Chiết suất của nước là $\dfrac43$, của không khí là $1$. Mặt nước phẳng, lặng; bỏ qua ánh sáng phản xạ ở thành bể và đáy bể.</p><ol type="a"><li>Ánh sáng từ đèn chỉ ló ra không khí qua một vùng tròn trên mặt nước. Tính bán kính và diện tích vùng đó. Một đĩa chắn sáng tròn, mỏng, thả nổi trên mặt nước, tâm đĩa ở ngay trên đèn, phải có bán kính tối thiểu bao nhiêu để không tia sáng nào từ đèn ló ra không khí?</li><li>Thay nước bằng một chất lỏng trong suốt có chiết suất $1{,}6$, độ sâu vẫn $0{,}9\ \text{m}$. Tính bán kính vùng sáng.</li><li>Trở lại bể nước. Chỉ có một đĩa chắn bán kính $0{,}5\ \text{m}$ thả nổi trên mặt nước. Đèn phải đặt ngay dưới tâm đĩa, ở độ sâu lớn nhất bằng bao nhiêu để không tia sáng nào ló ra không khí?</li></ol>"""),
]

# ═════════════ BẢNG PHÂN TÍCH ĐỀ ═════════════
ANALYSIS = [
 # Dạng 1
 [(r'"từ không khí tới mặt thoáng phẳng của một chất lỏng"', r"$n_1=1$ (chứa tia tới); $n_2=n$",
   r"Định luật khúc xạ $n_1\sin i=n_2\sin r$<br>Môi trường 1 là môi trường chứa tia tới"),
  (r'"góc tới $i=60^{\circ}$; … góc khúc xạ $r=36^{\circ}$"', r"$i=60^{\circ}$; $r=36^{\circ}$",
   r"⚠ góc tới, góc khúc xạ đo so với <strong>pháp tuyến</strong>, không đo so với mặt thoáng"),
  (r'"$c=3\cdot10^8\ \text{m/s}$"', r"$c$", r"Chiết suất tuyệt đối $n=\dfrac cv$"),
  (r'"Tính chiết suất … và tốc độ ánh sáng trong chất lỏng"', r"Cần $n$, $v$", r"$n=\dfrac{\sin i}{\sin r}$; $v=\dfrac cn$"),
  (r'"từ trong chất lỏng ra không khí với góc tới $30^{\circ}$"', r"Bây giờ $n_1=n$, $n_2=1$; $i=30^{\circ}$",
   r"Môi trường chứa tia tới đã đổi<br>Ánh sáng đi sang môi trường chiết quang hơn hay kém hơn?"),
  (r'"một phần ánh sáng bị phản xạ trên mặt thoáng"', r"Tia phản xạ cùng điểm tới", r"Định luật phản xạ: góc phản xạ $i'=i$"),
  (r'"góc hợp bởi tia phản xạ và tia khúc xạ"', r"Cần góc giữa hai tia", r"Vẽ hình: góc cần tìm ghép từ những góc nào quanh điểm tới?")],
 # Dạng 2
 [(r'"lớp nước dày $80\ \text{cm}$ … lớp dầu dày $14\ \text{cm}$"', r"$e_{\text{d}}=14\ \text{cm}$; $e_{\text{n}}=80\ \text{cm}$",
   r"Mỗi lớp nằm giữa vật và mắt làm ảnh dịch chỗ"),
  (r'"Chiết suất của dầu là $1{,}4$, của nước là $\dfrac43$"', r"$n_{\text{d}}=1{,}4$; $n_{\text{n}}=\dfrac43$",
   r"Lớp dày $e$ chiết suất $n$, mắt ở không khí: trông dày $\dfrac en$"),
  (r'"nhìn theo phương gần vuông góc"', r"Góc tới rất nhỏ",
   r"⚠ chỉ khi nhìn gần vuông góc mới dùng được $h'=\dfrac hn$ (xấp xỉ góc nhỏ $\tan\approx\sin$); nhìn xiên thì khác"),
  (r'"Đáy bể trông như cách mặt dầu bao nhiêu? … nâng lên bao nhiêu?"', r"Cần $h'$ và $\Delta h$",
   r"$h'=\sum\dfrac{e_k}{n_k}$; độ nâng $\Delta h=$ độ sâu thật $-\ h'$"),
  (r'"cá … ở dưới mặt phân cách dầu – nước $36\ \text{cm}$"', r"Nước giữa cá và mặt phân cách: $36\ \text{cm}$",
   r"Chỉ tính phần nước nằm giữa cá và mắt, không lấy cả $80\ \text{cm}$"),
  (r'"bóng đèn … cách mặt dầu $150\ \text{cm}$; con cá nhìn lên"', r"$H=150\ \text{cm}$; mắt ở trong nước",
   r"Vật ở không khí, mắt ở nước: lớp không khí dày $H$ trông dày $nH$<br>Mắt ở trong nước thì khoảng cách biểu kiến phải đổi về môi trường nào?"),
  (r'"như ở độ cao bao nhiêu so với mặt dầu"', r"Cần độ cao của ảnh đèn", r"Ảnh nằm ở đâu so với cá? Giữa cá và mặt dầu có những lớp nào?")],
 # Dạng 3
 [(r'"bóng đèn nhỏ (coi là nguồn sáng điểm) … đáy một bể nước sâu $0{,}9\ \text{m}$"', r"$h=0{,}9\ \text{m}$",
   r"Đèn phát tia theo mọi hướng, góc tới ở mặt nước tăng dần khi tia nghiêng dần"),
  (r'"Chiết suất của nước là $\dfrac43$, của không khí là $1$"', r"$n_1=\dfrac43$; $n_2=1$",
   r"⚠ phản xạ toàn phần cần <strong>đủ hai điều kiện</strong>: ánh sáng đi từ môi trường chiết quang hơn sang kém hơn <strong>và</strong> $i\ge i_{gh}$"),
  (r'"chỉ ló ra không khí qua một vùng tròn … bán kính và diện tích"', r"Cần $R$, $S$",
   r"Mép vùng sáng ứng với tia có $i=i_{gh}$, $\sin i_{gh}=\dfrac{n_2}{n_1}$<br>$R=h\tan i_{gh}$; $S=\pi R^2$"),
  (r'"đĩa chắn … bán kính tối thiểu … không tia sáng nào ló ra"', r"Cần $r_{\min}$", r"Những tia nào còn ló được ra không khí? Đĩa phải che chỗ nào?"),
  (r'"chất lỏng trong suốt có chiết suất $1{,}6$"', r"$n_1=1{,}6$; $h=0{,}9\ \text{m}$", r"$i_{gh}$ đổi theo chiết suất, tính lại rồi mới tính $R$"),
  (r'"đĩa chắn bán kính $0{,}5\ \text{m}$ … độ sâu lớn nhất"', r"$r_{\text{đ}}=0{,}5\ \text{m}$; cần $h_{\max}$",
   r"Đèn càng sâu thì vùng sáng càng rộng hay càng hẹp? So vùng sáng với đĩa")],
]

# ═════════════ LỜI GIẢI ═════════════
K1 = [r"<strong>Khái niệm:</strong> khúc xạ là hiện tượng tia sáng gãy khúc tại mặt phân cách hai môi trường trong suốt; góc đo so với pháp tuyến.",
      r"<strong>Định luật:</strong> $n_1\sin i=n_2\sin r$, tia khúc xạ nằm bên kia pháp tuyến so với tia tới.",
      r"<strong>Công thức:</strong> $n=\dfrac cv$; góc phản xạ $i'=i$.",
      r"<strong>Điều kiện:</strong> $n_1$ là chiết suất môi trường chứa tia tới; đổi chiều truyền thì đổi vai $n_1$, $n_2$."]
K2 = [r"<strong>Khái niệm:</strong> nhìn vật qua mặt phân cách, ta thấy ảnh ảo của vật, dịch về phía môi trường chiết quang kém hơn.",
      r"<strong>Công thức:</strong> mắt ở không khí, lớp dày $e_k$ chiết suất $n_k$ trông dày $\dfrac{e_k}{n_k}$; nhiều lớp $h'=\sum\dfrac{e_k}{n_k}$.",
      r"<strong>Mắt trong môi trường chiết suất $n$:</strong> khoảng cách biểu kiến $=n\cdot\sum\dfrac{e_k}{n_k}$ (lớp không khí dày $H$ trông dày $nH$).",
      r"<strong>Điều kiện:</strong> nhìn gần vuông góc với mặt phân cách; chỉ tính các lớp nằm giữa vật và mắt."]
K3 = [r"<strong>Khái niệm:</strong> phản xạ toàn phần là hiện tượng toàn bộ ánh sáng bị phản xạ, không còn tia khúc xạ.",
      r"<strong>Điều kiện:</strong> đi từ môi trường chiết quang hơn sang kém hơn và $i\ge i_{gh}$.",
      r"<strong>Công thức:</strong> $\sin i_{gh}=\dfrac{n_2}{n_1}$; vùng sáng $R=h\tan i_{gh}$, $S=\pi R^2$.",
      r"<strong>Hình học:</strong> góc tại nguồn (giữa đường thẳng đứng và tia) bằng góc tới ở mặt nước vì hai pháp tuyến song song."]

SOLS = [
 sol(K1, [
  ("Chiết suất của chất lỏng", [P(r"Tia đi từ không khí ($n_1=1$) vào chất lỏng ($n_2=n$):"),
     M(r"1\cdot\sin i=n\sin r"), M(r"n=\dfrac{\sin60^{\circ}}{\sin36^{\circ}}=\dfrac{0{,}8660}{0{,}5878}"), A(r"n\approx1{,}473\approx1{,}47")]),
  ("Tốc độ ánh sáng trong chất lỏng", [M(r"v=\dfrac cn"), M(r"v=\dfrac{3\cdot10^8}{1{,}473}"), A(r"v\approx2{,}04\cdot10^8\ \text{m/s}")]),
  ("Chiếu ngược ra không khí", [P(r"Bây giờ môi trường chứa tia tới là chất lỏng: $n_1=n$, $n_2=1$, $i=30^{\circ}$."),
     M(r"n\sin30^{\circ}=1\cdot\sin r"), M(r"\sin r=1{,}473\cdot0{,}5\approx0{,}737"), A(r"r\approx47{,}4^{\circ}"),
     P(r"$r\gt i$: đi sang môi trường chiết quang kém hơn, tia khúc xạ <strong>lệch xa pháp tuyến</strong> hơn tia tới.")]),
  ("Góc giữa tia phản xạ và tia khúc xạ", [P(r"Tia phản xạ ở phía không khí, hợp với pháp tuyến góc $i'=i=60^{\circ}$, tức hợp với mặt thoáng góc $90^{\circ}-60^{\circ}=30^{\circ}$."),
     P(r"Tia khúc xạ ở phía chất lỏng, hợp với mặt thoáng góc $90^{\circ}-36^{\circ}=54^{\circ}$."),
     P(r"Hai tia cùng ở bên phải pháp tuyến, một tia trên và một tia dưới mặt thoáng, nên góc giữa chúng là tổng hai góc với mặt thoáng:"),
     M(r"\alpha=(90^{\circ}-i')+(90^{\circ}-r)=180^{\circ}-i-r"), M(r"\alpha=180^{\circ}-60^{\circ}-36^{\circ}"), A(r"\alpha=84^{\circ}")]),
  ("Kiểm tra", [P(r"$n\gt1$ ✓ (chất lỏng chiết quang hơn không khí) và $v\lt c$ ✓."),
     P(r"Câu b: kiểm ngược $\dfrac{\sin47{,}4^{\circ}}{\sin30^{\circ}}\approx\dfrac{0{,}736}{0{,}5}\approx1{,}47=n$ ✓."),
     P(r"Câu c: góc tìm được nằm giữa $0^{\circ}$ và $180^{\circ}$ ✓; khi $i$ tăng thì cả hai tia đều nghiêng về phía mặt thoáng hơn nên góc giữa chúng nhỏ lại, đúng chiều với công thức $180^{\circ}-i-r$ ✓.")])],
  [r"a) $n\approx1{,}47$; $v\approx2{,}04\cdot10^8\ \text{m/s}$", r"b) $r\approx47{,}4^{\circ}$, tia khúc xạ lệch xa pháp tuyến", r"c) $84^{\circ}$"],
  r"Nhận dạng: thấy <strong>góc tới, góc khúc xạ, tốc độ ánh sáng</strong> → $n_1\sin i=n_2\sin r$ và $n=\dfrac cv$; đổi chiều thì đổi vai $n_1$, $n_2$."),
 sol(K2, [
  ("Lớp dầu trông dày bao nhiêu", [P(r"Mắt ở không khí, lớp dầu dày $14\ \text{cm}$:"), M(r"e'_{\text{d}}=\dfrac{e_{\text{d}}}{n_{\text{d}}}=\dfrac{14}{1{,}4}"), A(r"e'_{\text{d}}=10\ \text{cm}")]),
  ("Đáy bể trông sâu bao nhiêu", [P(r"Cộng phần đóng góp của hai lớp:"), M(r"h'=\dfrac{14}{1{,}4}+\dfrac{80}{4/3}=10+60"), A(r"h'=70\ \text{cm}"),
     P(r"Độ sâu thật $14+80=94\ \text{cm}$, nên đáy như được nâng lên $\Delta h=94-70=24\ \text{cm}$.")]),
  ("Người thấy cá ở đâu", [P(r"Giữa cá và mắt chỉ có $14\ \text{cm}$ dầu và $36\ \text{cm}$ nước:"),
     M(r"h'_{\text{cá}}=\dfrac{14}{1{,}4}+\dfrac{36}{4/3}=10+27"), A(r"h'_{\text{cá}}=37\ \text{cm}")]),
  ("Cá thấy đèn cách nó bao nhiêu", [P(r"Đổi từng lớp giữa đèn và cá ra 'độ dày tương đương trong không khí' rồi nhân với chiết suất nước (mắt cá ở trong nước):"),
     M(r"d'=n_{\text{n}}\left(\dfrac{36}{4/3}+\dfrac{14}{1{,}4}+\dfrac{150}{1}\right)"), M(r"d'=\dfrac43\cdot(27+10+150)=\dfrac43\cdot187"), A(r"d'\approx249{,}3\ \text{cm}"),
     P(r"Khoảng cách thật từ cá tới đèn là $36+14+150=200\ \text{cm}$: cá thấy đèn xa hơn thật.")]),
  ("Độ cao của ảnh đèn so với mặt dầu", [P(r"Ảnh của đèn nằm trên đường thẳng đứng qua cá; từ cá lên tới mặt dầu là $36+14=50\ \text{cm}$:"),
     M(r"H'=d'-50=249{,}3-50"), A(r"H'\approx199{,}3\ \text{cm}")]),
  ("Kiểm tra", [P(r"Mắt ở không khí: ảnh dịch lại gần mắt (đáy nông hơn thật) ✓. Mắt ở nước: ảnh của vật ngoài không khí dịch ra xa (đèn cao hơn thật) ✓ — đúng quy tắc ảnh dịch về phía môi trường chiết quang kém."),
     P(r"$H'$ rất gần $\dfrac43\cdot150=200\ \text{cm}$ vì lớp dầu mỏng và chiết suất dầu gần chiết suất nước; bỏ hẳn lớp dầu thì sai khoảng $0{,}7\ \text{cm}$."),
     P(r"Đơn vị: chỉ cộng các độ dài cùng đơn vị cm ✓.")])],
  [r"a) Đáy trông cách mặt dầu $70\ \text{cm}$, như được nâng lên $24\ \text{cm}$", r"b) Cá trông cách mặt dầu $37\ \text{cm}$",
   r"c) Đèn trông cách cá khoảng $249\ \text{cm}$, cao khoảng $199\ \text{cm}$ so với mặt dầu"],
  r"Nhận dạng: thấy <strong>nhìn gần vuông góc qua nhiều lớp</strong> → mỗi lớp đổi thành $\dfrac{e_k}{n_k}$; mắt ở trong chất lỏng thì nhân thêm chiết suất của chất lỏng đó."),
 sol(K3, [
  ("Góc giới hạn nước – không khí", [P(r"Ánh sáng đi từ nước ($n_1=\frac43$) ra không khí ($n_2=1$), có thể phản xạ toàn phần:"),
     M(r"\sin i_{gh}=\dfrac{n_2}{n_1}=\dfrac{1}{4/3}=0{,}75"), A(r"i_{gh}\approx48{,}6^{\circ}")]),
  ("Bán kính vùng sáng", [P(r"Tia tới mép vùng sáng có $i=i_{gh}$; ra ngoài mép thì $i\gt i_{gh}$, phản xạ toàn phần. Trong tam giác vuông có cạnh $h$ và $R$:"),
     M(r"R=h\tan i_{gh}=0{,}9\cdot\tan48{,}6^{\circ}"), M(r"R\approx0{,}9\cdot1{,}134"), A(r"R\approx1{,}02\ \text{m}")]),
  ("Diện tích vùng sáng", [M(r"S=\pi R^2=3{,}14\cdot1{,}0205^2"), A(r"S\approx3{,}27\ \text{m}^2")]),
  ("Bán kính tối thiểu của đĩa chắn", [P(r"Chỉ các tia rơi vào trong vùng sáng mới ló ra; tia rơi ra ngoài vùng đó đã bị phản xạ toàn phần."),
     P(r"Đĩa tâm ngay trên đèn chỉ cần phủ kín vùng sáng: $r_{\min}=R\approx1{,}02\ \text{m}$.")]),
  ("Bán kính vùng sáng với chất lỏng chiết suất 1,6", [M(r"\sin i'_{gh}=\dfrac{1}{1{,}6}=0{,}625\Rightarrow i'_{gh}\approx38{,}7^{\circ}"),
     M(r"R'=0{,}9\cdot\tan38{,}7^{\circ}\approx0{,}9\cdot0{,}801"), A(r"R'\approx0{,}72\ \text{m}"),
     P(r"Chiết suất lớn hơn thì góc giới hạn nhỏ hơn, vùng sáng thu hẹp.")]),
  ("Độ sâu lớn nhất của đèn", [P(r"Đèn càng sâu thì vùng sáng càng rộng. Không tia nào ló ra khi vùng sáng nằm gọn trong đĩa: $h\tan i_{gh}\le r_{\text{đ}}$."),
     M(r"h_{\max}=\dfrac{r_{\text{đ}}}{\tan i_{gh}}=\dfrac{0{,}5}{1{,}134}"), A(r"h_{\max}\approx0{,}44\ \text{m}")]),
  ("Kiểm tra", [P(r"$\sin i_{gh}=0{,}75\lt1$ ✓ (nếu viết ngược $\dfrac{n_1}{n_2}$ sẽ ra $\dfrac43\gt1$, vô lí)."),
     P(r"Câu c: $0{,}44\cdot1{,}134\approx0{,}50\ \text{m}$ đúng bằng bán kính đĩa ✓; $0{,}44\ \text{m}\lt0{,}9\ \text{m}$ nên đèn treo lơ lửng trong nước, không ở đáy."),
     P(r"Đơn vị: $R$ cùng đơn vị với $h$ (m) vì $\tan$ không có đơn vị ✓.")])],
  [r"a) $R\approx1{,}02\ \text{m}$; $S\approx3{,}27\ \text{m}^2$; đĩa chắn bán kính tối thiểu $\approx1{,}02\ \text{m}$", r"b) $R'\approx0{,}72\ \text{m}$", r"c) $h_{\max}\approx0{,}44\ \text{m}$"],
  r"Nhận dạng: thấy <strong>nguồn sáng dưới nước, vùng sáng trên mặt nước, đĩa che</strong> → mép vùng sáng ứng với $i=i_{gh}$, $R=h\tan i_{gh}$."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC ═════════════
STEPS = [
 # ── Dạng 1 ──
 dict(nhan_dang=r"Thấy <b>góc tới, góc khúc xạ, tốc độ ánh sáng</b> → $n_1\sin i=n_2\sin r$ và $n=\dfrac cv$.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Chiết suất của chất lỏng", "Chiết suất của chất lỏng bằng bao nhiêu?", 1.47, "", 0.01,
       loi=r"Viết ngược tỉ số thành $\dfrac{\sin r}{\sin i}$, ra một số nhỏ hơn $1$; chất lỏng chiết quang hơn không khí nên $n$ phải lớn hơn $1$."),
  buoc("Tốc độ ánh sáng trong chất lỏng", "Tốc độ ánh sáng trong chất lỏng là a·10⁸ m/s. Nhập hệ số a.", 2.04, "·10⁸ m/s", 0.02,
       loi=r"Nhân $c$ với $n$, nghĩ rằng chiết suất lớn thì ánh sáng đi nhanh; thực ra chiết suất lớn thì ánh sáng đi chậm.",
       ke=[(r"Dùng $v=\dfrac cn$", True),
           (r"Dùng $v=c\cdot n$", r"Chiết suất cho biết ánh sáng đi chậm đi bao nhiêu lần, nên phải chia cho $n$; nhân sẽ ra tốc độ lớn hơn $c$, vô lí."),
           (r"Giữ $v=c$ vì tốc độ ánh sáng không đổi", r"Chỉ trong chân không (gần đúng là không khí) ánh sáng mới đi với tốc độ $c$; trong chất lỏng nó đi chậm hơn.")]),
  buoc("Chiếu ngược ra không khí", "Góc khúc xạ khi tia đi từ chất lỏng ra không khí với góc tới 30° là bao nhiêu độ?", 47.4, "°", 0.3,
       loi=r"Giữ công thức của câu a ($\sin r=\dfrac{\sin i}{n}$) dù tia giờ đi ngược chiều, ra góc khúc xạ nhỏ hơn góc tới.",
       ke=[(r"Viết $n\sin30^{\circ}=1\cdot\sin r$ (chất lỏng giờ là môi trường chứa tia tới)", True),
           (r"Viết $\sin r=\dfrac{\sin30^{\circ}}{n}$ như câu a", r"Ở câu a tia đi từ không khí vào; bây giờ tia đi từ chất lỏng ra nên $n$ đứng cạnh $\sin i$."),
           (r"Lấy $r=36^{\circ}$ theo tính thuận nghịch", r"Thuận nghịch chỉ áp dụng khi tia đi ngược đúng đường cũ, tức góc tới trong chất lỏng bằng $36^{\circ}$; ở đây góc tới là $30^{\circ}$.")]),
  buoc("Góc giữa tia phản xạ và tia khúc xạ", "Góc hợp bởi tia phản xạ và tia khúc xạ là bao nhiêu độ?", 84, "°", 0.5,
       loi=r"Cộng thẳng góc phản xạ với góc khúc xạ; hai góc đó đo từ hai nửa khác nhau của pháp tuyến nên không ghép liền nhau.",
       ke=[(r"Cộng hai góc mà tia phản xạ và tia khúc xạ hợp với mặt thoáng", True),
           (r"Cộng góc phản xạ với góc khúc xạ $i'+r$", r"Tia phản xạ đo từ nửa pháp tuyến phía trên, tia khúc xạ đo từ nửa phía dưới; hai góc này không nằm kề nhau nên tổng không phải góc giữa hai tia."),
           (r"Lấy hiệu $i-r$", r"Hiệu đó là góc lệch giữa phương tia tới và tia khúc xạ, không liên quan tới tia phản xạ.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 2 ──
 dict(nhan_dang=r"Thấy <b>nhìn gần vuông góc qua nhiều lớp chất lỏng</b> → mỗi lớp trông dày $\dfrac{e}{n}$, rồi cộng.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 3}, buoc=[
  buoc("Lớp dầu trông dày bao nhiêu", "Nhìn từ trên xuống, lớp dầu trông dày bao nhiêu cm?", 10, "cm", 0.1,
       loi=r"Nhân độ dày với chiết suất thay vì chia; mắt ở không khí nhìn vào chất lỏng thì lớp chất lỏng trông mỏng đi."),
  buoc("Đáy bể trông sâu bao nhiêu", "Đáy bể trông như cách mặt dầu bao nhiêu cm?", 70, "cm", 0.3,
       loi=r"Cộng hai độ dày thật rồi chia cho một chiết suất trung bình; mỗi lớp phải chia cho chiết suất của chính nó.",
       ke=[(r"Cộng $\dfrac{e_{\text{d}}}{n_{\text{d}}}+\dfrac{e_{\text{n}}}{n_{\text{n}}}$", True),
           (r"Lấy $\dfrac{14+80}{n_{\text{d}}}$, chia cả bể cho chiết suất của lớp trên cùng", r"Nước có chiết suất riêng; chia cả bể cho chiết suất dầu là coi lớp nước như dầu."),
           (r"Lấy $\dfrac{14+80}{n_{\text{d}}\cdot n_{\text{n}}}$", r"Chiết suất các lớp không nhân với nhau; mỗi lớp chỉ làm ngắn chính độ dày của nó.")]),
  buoc("Người thấy cá ở đâu", "Người nhìn thấy cá như cách mặt dầu bao nhiêu cm?", 37, "cm", 0.5,
       loi=r"Lấy cả lớp nước $80\ \text{cm}$ thay vì chỉ phần nước nằm giữa cá và mặt phân cách.",
       ke=[(r"Cộng phần dầu chia $n_{\text{d}}$ với phần nước nằm giữa cá và mặt phân cách chia $n_{\text{n}}$", True),
           (r"Lấy độ sâu biểu kiến của đáy trừ độ dày thật của lớp nước nằm dưới cá", r"Trừ một độ dài thật khỏi một độ dài biểu kiến là trộn hai loại độ dài; phần nước dưới cá cũng phải đổi ra độ dày biểu kiến."),
           (r"Chỉ chia phần nước giữa cá và mặt phân cách cho $n_{\text{n}}$", r"Ánh sáng từ cá còn đi qua lớp dầu trước khi tới mắt, lớp dầu cũng làm ảnh dịch.")]),
  buoc("Cá thấy đèn cách nó bao nhiêu", "Con cá thấy bóng đèn như cách nó bao nhiêu cm?", 249.3, "cm", 0.5,
       loi=r"Đổi các lớp ra độ dày tương đương trong không khí rồi dừng ở đó; mắt cá ở trong nước nên còn phải nhân với chiết suất nước.",
       ke=[(r"Đổi mọi lớp giữa đèn và cá ra độ dày tương đương trong không khí, cộng lại rồi nhân với chiết suất nước", True),
           (r"Cộng thẳng các độ dài thật $36+14+150$", r"Cách đó bỏ qua khúc xạ ở hai mặt phân cách; đó là khoảng cách thật, không phải khoảng cách cá trông thấy."),
           (r"Đổi mọi lớp ra độ dày tương đương trong không khí, cộng lại và dừng ở đó", r"Kết quả đó đúng cho mắt đặt trong không khí; mắt cá ở trong nước nên phải đổi sang nước.")]),
  buoc("Độ cao của ảnh đèn so với mặt dầu", "Con cá thấy bóng đèn như ở độ cao bao nhiêu cm so với mặt dầu (mặt phẳng thật của lớp dầu)?", 199.3, "cm", 0.5,
       loi=r"Lấy $n_{\text{n}}\cdot150$ ngay, bỏ qua ảnh hưởng của lớp dầu; kết quả gần đúng nhưng lệch, vì lớp dầu mắt cá nhìn thấy cũng dày khác thật.",
       ke=[(r"Lấy khoảng cách biểu kiến cá – đèn trừ khoảng cách thật từ cá lên mặt dầu", True),
           (r"Lấy khoảng cách biểu kiến cá – đèn trừ $36\ \text{cm}$", r"Giữa cá và mặt dầu có cả nước lẫn dầu; trừ $36\ \text{cm}$ mới tới mặt phân cách dầu – nước."),
           (r"Lấy $n_{\text{n}}\cdot150$, bỏ qua lớp dầu", r"Ảnh của đèn tính từ vị trí cá; bỏ lớp dầu là bỏ sự dịch chỗ do chính lớp dầu gây ra, kết quả bị lệch.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 3 ──
 dict(nhan_dang=r"Thấy <b>đèn dưới nước, vùng sáng tròn trên mặt nước, đĩa che</b> → mép vùng sáng là tia có $i=i_{gh}$.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Góc giới hạn nước – không khí", "Góc giới hạn khi ánh sáng đi từ nước ra không khí là bao nhiêu độ?", 48.6, "°", 0.2,
       loi=r"Viết $\sin i_{gh}=\dfrac{n_1}{n_2}$, ra số lớn hơn $1$ (máy tính báo lỗi); phải lấy chiết suất nhỏ chia chiết suất lớn."),
  buoc("Bán kính vùng sáng", "Bán kính vùng sáng trên mặt nước là bao nhiêu mét?", 1.02, "m", 0.01,
       loi=r"Dùng $\sin i_{gh}$ thay cho $\tan i_{gh}$; trong tam giác vuông, $R$ là cạnh đối, $h$ là cạnh kề nên dùng tang.",
       ke=[(r"Dùng $R=h\tan i_{gh}$", True),
           (r"Dùng $R=h\sin i_{gh}$", r"Trong tam giác vuông tạo bởi $h$ và $R$, $h$ là cạnh góc vuông chứ không phải cạnh huyền; tỉ số cạnh đối trên cạnh kề là tang."),
           (r"Dùng $R=\dfrac{h}{\tan i_{gh}}$", r"Góc $i_{gh}$ đo từ đường thẳng đứng, $R$ là cạnh đối diện với góc đó nên phải nhân với tang, không chia.")]),
  buoc("Diện tích vùng sáng", "Diện tích vùng sáng là bao nhiêu m²?", 3.27, "m²", 0.04,
       loi=r"Dùng $S=2\pi R$ (chu vi) hoặc quên bình phương bán kính.",
       ke=[(r"Dùng $S=\pi R^2$", True),
           (r"Dùng $S=2\pi R$", r"Đó là chu vi của vùng tròn, đơn vị mét, không phải diện tích."),
           (r"Dùng $S=\pi h^2$", r"Vùng sáng có bán kính $R$ chứ không phải độ sâu $h$.")]),
  buoc("Bán kính tối thiểu của đĩa chắn", "Đĩa chắn phải có bán kính tối thiểu bằng bao nhiêu?",
       lua_chon=[(r"Bằng bán kính vùng sáng $R$", True),
                 (r"Bằng độ sâu $h$ của bể", r"Đĩa bằng $h$ thì vẫn còn một vành của vùng sáng ló ra ngoài mép đĩa."),
                 (r"Nhỏ hơn $R$ một chút, vì tia sát mép đã bị phản xạ toàn phần", r"Tia sát mép (bên trong) có góc tới nhỏ hơn $i_{gh}$ một chút nên vẫn ló ra; đĩa phải che tới đúng mép.")],
       loi=r"Nghĩ rằng chỉ cần che chỗ sáng nhất ngay trên đèn; mọi điểm trong vùng tròn đều có tia ló ra.",
       ke=[(r"Xét xem tia nào còn ló được ra không khí, đĩa phải che hết các điểm đó", True),
           (r"Lấy bán kính đĩa bằng độ sâu của bể", r"Không có lí do hình học nào để bán kính đĩa bằng độ sâu; vùng cần che do góc giới hạn quyết định."),
           (r"Lấy bán kính đĩa bằng nửa bán kính vùng sáng", r"Ngoài nửa đó vẫn còn tia có góc tới nhỏ hơn góc giới hạn, vẫn ló ra được.")]),
  buoc("Bán kính vùng sáng với chất lỏng chiết suất 1,6", "Với chất lỏng chiết suất 1,6, bán kính vùng sáng là bao nhiêu mét?", 0.72, "m", 0.01,
       loi=r"Chia bán kính câu a theo tỉ lệ chiết suất, coi bán kính tỉ lệ nghịch với $n$; tang không tỉ lệ với sin nên phải tính lại góc giới hạn.",
       ke=[(r"Tính lại $i_{gh}$ với $\sin i_{gh}=\dfrac{1}{1{,}6}$ rồi dùng $R=h\tan i_{gh}$", True),
           (r"Lấy $R$ câu a nhân $\dfrac{4/3}{1{,}6}$", r"$R=h\tan i_{gh}$ mà tang không tỉ lệ với sin, nên $R$ không tỉ lệ nghịch đơn giản với $n$."),
           (r"Giữ $i_{gh}$ của nước, vì độ sâu không đổi", r"Góc giới hạn chỉ phụ thuộc chiết suất hai môi trường; đổi chất lỏng là đổi góc giới hạn.")]),
  buoc("Độ sâu lớn nhất của đèn", "Đèn đặt sâu nhất bao nhiêu mét dưới tâm đĩa để không tia nào ló ra?", 0.44, "m", 0.01,
       loi=r"Nhân bán kính đĩa với $\tan i_{gh}$ thay vì chia; ở đây biết $R$, cần tìm $h$.",
       ke=[(r"Cho vùng sáng vừa bằng đĩa: $h\tan i_{gh}=r_{\text{đ}}$, rồi giải tìm $h$", True),
           (r"Lấy $h=r_{\text{đ}}\tan i_{gh}$", r"Đó là đổi chỗ sai: từ $R=h\tan i_{gh}$ thì $h=\dfrac{R}{\tan i_{gh}}$."),
           (r"Lấy $h=\dfrac{r_{\text{đ}}}{\sin i_{gh}}$", r"$\dfrac{r_{\text{đ}}}{\sin i_{gh}}$ là độ dài đường đi của tia tới mép đĩa (cạnh huyền), không phải độ sâu.")]),
  buoc("Kiểm tra")]),
]


def kiem_so():
    # D1
    assert abs(N1 - 1.4734) < 1e-3 and round(N1, 2) == 1.47
    assert round(V1 / 1e8, 2) == 2.04
    assert abs(SIN_RB - 0.7367) < 1e-3 and round(R_B, 1) == 47.4
    assert abs(asind(1.47 * 0.5) - 47.4) < 0.3            # dùng n đã làm tròn vẫn trong sai số
    assert GOC_C == 84
    # cách sai D1 cho số khác đáp án
    assert abs(sind(R1_) / sind(I1) - 1.47) > 0.3          # viết ngược tỉ số
    assert abs(3 * N1 - 2.04) > 1 and abs(3.0 - 2.04) > 0.5  # v = c·n ; v = c
    assert abs(asind(sind(30) / N1) - 47.4) > 5 and abs(36 - 47.4) > 5
    assert abs((I1 + R1_) - 84) > 5 and abs((I1 - R1_) - 84) > 5
    # D2
    assert abs(H_DAY - 70) < 1e-9 and abs(NANG - 24) < 1e-9 and abs(E_DAU / N_DAU - 10) < 1e-9
    assert abs(H_CA_BK - 37) < 1e-9
    assert abs(D_DEN - 249.333) < 0.01 and abs(CAO_DEN - 199.333) < 0.01 and abs(CAO_DEN - (D_DEN - 50)) < 1e-9
    # cách sai D2
    assert abs(14 * 1.4 - 10) > 1                           # nhân thay vì chia
    assert abs(94 / N_DAU - 70) > 0.5 and abs(94 / (1.4 * N_W) - 70) > 0.5
    assert abs((H_DAY - (E_NUOC - H_CA)) - 37) > 0.5 and abs(H_CA / N_W - 37) > 0.5 and H_CA_BK != H_CA
    assert abs((H_CA + 14 + 150) - D_DEN) > 0.5 and abs((27 + 10 + 150) - D_DEN) > 0.5
    assert abs((D_DEN - H_CA) - CAO_DEN) > 0.5 and abs(N_W * 150 - CAO_DEN) > 0.5 and abs(199 - CAO_DEN) <= 0.5    # 200 bị loại, 199 được (sai số 0,5)
    # D3
    assert abs(IGH - 48.59) < 0.01 and round(IGH, 1) == 48.6
    assert abs(tand(IGH) - 3 / math.sqrt(7)) < 1e-12
    assert round(R3, 2) == 1.02 and round(S3, 2) == 3.27
    assert abs(IGH16 - 38.68) < 0.01 and round(R3B, 2) == 0.72
    assert round(H_MAX, 2) == 0.44 and H_MAX < H3
    # cách sai D3
    assert N_W > 1                                           # sin igh = n1/n2 > 1
    assert abs(H3 * sind(IGH) - 1.02) > 0.1 and abs(H3 / tand(IGH) - 1.02) > 0.1
    assert abs(2 * math.pi * R3 - 3.27) > 1 and abs(math.pi * H3 ** 2 - 3.27) > 0.5
    assert abs(R3 * N_W / 1.6 - 0.72) > 0.05 and abs(R3 - 0.72) > 0.05
    assert abs(R_DIA * tand(IGH) - 0.44) > 0.05 and abs(R_DIA / sind(IGH) - 0.44) > 0.05
    # hình mô phỏng D3 vẽ góc minh hoạ khác góc thật (không đo được đáp số)
    assert abs(TH_VE - IGH) > 5
    print("kiểm số liệu D1–D3 (bài 151): đạt")
