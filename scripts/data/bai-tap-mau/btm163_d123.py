"""Bài tập mẫu CĐ09 "Năng lượng với cuộc sống" (lesson 163) — Dạng 1–3. Module được build-hinh-163.py import.
Dàn ý + số liệu đã tính: content/hsg9/cd09-nang-luong-cuoc-song/nguon.md (mục "Bài tập mẫu", D1–D3 dùng nguyên số; tinh.py).
Quy ước: d = 10D = 10 000 N/m³; lưu lượng L (m³/s, không dùng Q); H chuỗi = H1·H2·H3; than q = 2,7·10^7 J/kg, k = 2,5 kg CO2/kg;
1 kWh = 3,6·10^6 J; 1 ngày = 86 400 s; "bỏ qua hao phí trên đường dây". Không làm tiền điện bậc thang (đơn giá cho sẵn một số).
Mọi đáp số tính lại bằng Python trong kiem_so(); mọi lựa chọn sai của chon_buoc_ke được assert cho số khác đáp án đúng."""
import math
import re
from dung import *   # sol, buoc, M/P/A, fig, seg, lbl, poly, arrow, chevron, RED/BLUE/ORG/GRN

GREY = "#94a3b8"
SUN = "#f59e0b"
TOPIC_HS = "Tính hiệu suất của máy và động cơ"
TOPIC_TT = "Các dạng năng lượng tái tạo và nguồn gốc"
TOPIC_TK = "Sử dụng năng lượng tiết kiệm, hiệu quả"
KWH = 3.6e6
NGAY = 86400
Q_THAN, K_THAN = 2.7e7, 2.5

# ── số liệu D1 (nhiệt điện than) ──
H1, H2, H3 = 0.90, 0.42, 0.96
H_D1 = H1 * H2 * H3                      # 0,36288
PD1 = 330e6
PNL = PD1 / H_D1                         # ≈ 909,4 MW
PHP = PNL - PD1
LOSS = (PNL * (1 - H1), PNL * H1 * (1 - H2), PNL * H1 * H2 * (1 - H3))
MS = PNL / Q_THAN                        # kg/s
THAN_NGAY = MS * NGAY / 1e3              # tấn
CO2_NGAY = THAN_NGAY * K_THAN
H_D1B = H1 * 0.45 * H3
THAN_NGAY_B = PD1 / H_D1B / Q_THAN * NGAY / 1e3
TK_THAN = THAN_NGAY - THAN_NGAY_B
A_D1_MWH = PD1 * 24 / 1e6               # 7920 MWh (Dạng 4 dùng lại)
# ── số liệu D2 (thuỷ điện) ──
HT, HM = 0.92, 0.96
H_D2 = HT * HM
PN_MUA = 1e4 * 250 * 95
PD_MUA = H_D2 * PN_MUA
PD_KHO = H_D2 * 1e4 * 160 * 80
L_CAN = 150e6 / (H_D2 * 1e4 * 80)
A_MUA_J = PD_MUA * NGAY
A_MUA_MWH = A_MUA_J / KWH / 1e3
V_NGAY = 250 * NGAY
THAN_THAY = A_MUA_J / H_D1 / Q_THAN / 1e3   # tấn
CO2_THAY = THAN_THAY * K_THAN
# ── số liệu D3 (pin Mặt Trời) ──
A_NGAY3 = 375 / 30
P_TAM = 0.20 * 1000 * 2.0                # W
A_TAM = P_TAM * 4.0 * 0.95 / 1000        # kWh/ngày
N_TAM = math.ceil(A_NGAY3 / A_TAM)
N_MAI = int(14 // 2.0)
THIEU_THANG = (A_NGAY3 - N_MAI * A_TAM) * 30
TK_THANG = 375 * 2800
HV_NAM = 67.5e6 / TK_THANG / 12


def anim(attr, vals, dur, kt=None):
    k = f' keyTimes="{kt}"' if kt else ""
    return f'<animate attributeName="{attr}" values="{vals}"{k} dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>'


def tx(x, y, s, c="currentColor", size=14, anchor="start", weight="600"):
    """Nhãn SVG có chỉ số dưới viết dạng X_{ab} → <tspan dy> (chỉ số Unicode hiện như dấu phẩy)."""
    out, pos, down = "", 0, False
    for m in re.finditer(r"_\{([^}]*)\}", s):
        out += f'<tspan dy="-4">{s[pos:m.start()]}</tspan>' if down else s[pos:m.start()]
        out += f'<tspan dy="4" font-size="{size - 3}">{m.group(1)}</tspan>'
        pos, down = m.end(), True
    rest = s[pos:]
    if rest:
        out += f'<tspan dy="-4">{rest}</tspan>' if down else rest
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="{anchor}">{out}</text>')


def box(x0, y0, x1, y1, c, lines):
    b = f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" rx="7" fill="none" stroke="{c}" stroke-width="2.2"/>'
    n = len(lines)
    for i, (s, w) in enumerate(lines):
        yy = (y0 + y1) / 2 + (i - (n - 1) / 2) * 18 + 5
        b += tx((x0 + x1) / 2, yy, s, c if i == 0 else "currentColor", 14, "middle", w)
    return b


def packet(path, t0, t1, dur, c=ORG, r=5):
    """Chấm năng lượng chạy dọc đường gấp khúc `path` từ thời điểm t0 tới t1 (phần của dur), tốc độ đều; ẩn trước/sau."""
    cum = [0.0]
    for (xa, ya), (xb, yb) in zip(path, path[1:]):
        cum.append(cum[-1] + math.hypot(xb - xa, yb - ya))
    ts = [t0 + (t1 - t0) * cc / cum[-1] for cc in cum]
    kt = "0;" + ";".join(f"{t:.4f}" for t in ts) + ";1"
    xs = [path[0][0]] + [p[0] for p in path] + [path[-1][0]]
    ys = [path[0][1]] + [p[1] for p in path] + [path[-1][1]]
    ok = f"0;{t0:.4f};{t0 + 0.01:.4f};{t1:.4f};{min(t1 + 0.015, 0.999):.4f};1"
    return (f'<circle cx="{path[0][0]}" cy="{path[0][1]}" r="{r}" fill="{c}" opacity="0">'
            f'{anim("cx", ";".join(f"{v:.1f}" for v in xs), dur, kt)}{anim("cy", ";".join(f"{v:.1f}" for v in ys), dur, kt)}'
            f'{anim("opacity", "0;0;1;1;0;0", dur, ok)}</circle>')


# ═════════════ HÌNH ═════════════
# ───────────── Dạng 1 · dòng năng lượng nhà máy nhiệt điện ─────────────
def d1(kk):
    b = ""
    if kk == 0:
        DUR = 7.0
        Y = 95
        b += box(6, 72, 58, 118, "currentColor", [("Than", "700")])
        bx = [(78, 146, "Lò hơi", "90 %"), (178, 246, "Tuabin", "42 %"), (278, 346, "Máy phát", "96 %")]
        for x0, x1, nm, h in bx:                 # tên ở trên, hiệu suất ở dưới: chấm năng lượng chạy giữa hai dòng chữ
            b += box(x0, 62, x1, 130, ORG, [])
            b += lbl((x0 + x1) / 2, 80, nm, ORG, 14, "middle", "700") + lbl((x0 + x1) / 2, 122, h, "currentColor", 14, "middle", "400")
        b += seg(58, Y, 78, Y, ORG, 2.4) + seg(146, Y, 178, Y, ORG, 2.4) + seg(246, Y, 278, Y, ORG, 2.4)
        b += arrow("", "o", 346, Y, 410, Y, 2.6)
        b += lbl(380, 86, "330 MW", "currentColor", 14, "middle", "700") + lbl(380, 114, "lưới", "currentColor", 14, "middle", "400")
        b += tx(8, 56, "P_{nl} = ?", ORG, 15, "start", "700")
        for x0, x1, _, _ in bx:
            xc = (x0 + x1) / 2
            b += arrow("", "o", xc, 130, xc, 178, 2.2, "5 4") + lbl(xc + 8, 164, "?", ORG, 15, "start", "700")
        b += lbl(212, 200, "nhiệt toả ra môi trường (hao phí)", "currentColor", 14, "middle", "400")
        dest = [3, 1, 0, 1, 2, 1, 3, 1]          # 0 lò hơi · 1 tuabin · 2 máy phát · 3 lưới (KHÔNG theo tỉ lệ)
        for i, k in enumerate(dest):
            if k == 3:
                path = [(32, Y), (408, Y)]
            else:
                xc = (bx[k][0] + bx[k][1]) / 2
                path = [(32, Y), (xc, Y), (xc, 180)]
            t0 = 0.03 + 0.075 * i
            b += packet(path, t0, min(t0 + 0.38, 0.98), DUR)
        return fig("c9-1-0", "0 0 420 212",
                   "Sơ đồ nhà máy nhiệt điện: than, lò hơi, tuabin, máy phát nối tiếp; chấm năng lượng chạy sang phải, một phần rẽ xuống thành nhiệt hao phí ở mỗi khâu",
                   b, "Mô phỏng: mỗi chấm là một phần năng lượng của than; ở mỗi khâu một phần rẽ xuống thành nhiệt toả ra môi trường. "
                      "Số chấm không theo tỉ lệ công suất.")
    # hình dữ kiện: công suất vào/ra từng khâu
    for (x0, x1, nm, hs) in [(60, 140, "Lò hơi", "H_{1} = 90 %"), (170, 250, "Tuabin", "H_{2} = 42 %"), (280, 360, "Máy phát", "H_{3} = 96 %")]:
        b += box(x0, 60, x1, 108, ORG, [(nm, "700"), (hs, "400")])
        xc = (x0 + x1) / 2
        b += arrow("", "o", xc, 108, xc, 146, 2.2, "5 4")
    b += arrow("", "o", 8, 84, 58, 84, 2.4) + arrow("", "o", 140, 84, 168, 84, 2.4) + arrow("", "o", 250, 84, 278, 84, 2.4)
    b += arrow("", "o", 360, 84, 412, 84, 2.4)
    b += tx(10, 74, "P_{nl}", ORG, 14, "start", "700") + tx(155, 74, "P_{1}", ORG, 14, "middle", "700") + tx(265, 74, "P_{2}", ORG, 14, "middle", "700")
    b += tx(414, 46, "P_{đ} = 330 MW", ORG, 14, "end", "700")
    b += tx(100, 166, "(1 − H_{1})·P_{nl}", "currentColor", 14, "middle", "400")
    b += tx(210, 166, "(1 − H_{2})·P_{1}", "currentColor", 14, "middle", "400")
    b += tx(320, 166, "(1 − H_{3})·P_{2}", "currentColor", 14, "middle", "400")
    b += lbl(210, 194, "Ra của khâu trước = vào của khâu sau", GRN, 14, "middle", "700")
    return fig("c9-1-2", "0 0 420 206", "Ba khâu nối tiếp, công suất ra của khâu trước là công suất vào của khâu sau; mỗi khâu hao phí một phần bằng một trừ hiệu suất nhân công suất vào",
               b, "Dữ kiện: hiệu suất ba khâu và công suất điện ra cuối cùng.")


# ───────────── Dạng 2 · thuỷ điện ─────────────
def d2(kk):
    b = ""
    if kk == 0:
        DUR = 6.0
        SURF, BOT, TY = 52, 150, 214            # mặt hồ, đáy hồ, cao độ tuabin
        b += (f'<path d="M10,{SURF} L150,{SURF} L150,{BOT} L10,{BOT} Z" fill="{BLUE}" opacity="0.22" stroke="none"/>'
              + seg(10, SURF, 150, SURF, BLUE, 1.8))
        b += f'<path d="M150,36 L178,36 L206,{TY + 10} L150,{TY + 10} Z" fill="none" stroke="currentColor" stroke-width="2.4"/>'
        b += lbl(16, SURF + 22, "hồ chứa", BLUE, 14, "start", "700")
        # ống dẫn
        P0, P1 = (156, 138), (282, 206)
        b += seg(P0[0], P0[1] - 7, P1[0], P1[1] - 7, "currentColor", 2) + seg(P0[0], P0[1] + 7, P1[0], P1[1] + 7, "currentColor", 2)
        b += lbl(214, 150, "ống dẫn", "currentColor", 14, "start", "400")
        b += lbl(16, BOT + 24, "L = 250 m³/s", BLUE, 14, "start", "700")
        # nhà máy + tuabin quay
        b += f'<rect x="282" y="180" width="70" height="44" rx="4" fill="none" stroke="currentColor" stroke-width="2.2"/>'
        CX, CY = 305, TY - 12
        b += (f'<g><circle cx="{CX}" cy="{CY}" r="11" fill="none" stroke="{ORG}" stroke-width="2.2"/>'
              f'{seg(CX - 11, CY, CX + 11, CY, ORG, 2)}{seg(CX, CY - 11, CX, CY + 11, ORG, 2)}'
              f'<animateTransform attributeName="transform" type="rotate" values="0 {CX} {CY};1440 {CX} {CY}" dur="{DUR:.2f}s" begin="indefinite" fill="freeze"/></g>')
        b += lbl(332, 206, "~", ORG, 18, "middle", "700")
        b += lbl(282, 246, "tuabin 92 %", "currentColor", 14, "start", "400") + lbl(282, 264, "máy phát 96 %", "currentColor", 14, "start", "400")
        b += arrow("", "o", 352, 196, 386, 196, 2.4) + tx(388, 178, "P_{đ} = ?", ORG, 14, "end", "700")
        b += seg(352, 226, 392, 226, BLUE, 1.8)
        # độ cao h: mặt hồ → tuabin
        b += seg(150, SURF, 410, SURF, GREY, 1.2, "4 3") + seg(390, TY, 410, TY, GREY, 1.2, "4 3")
        b += arrow("", "o", 404, SURF + 2, 404, TY - 2, 1.8) + arrow("", "o", 404, TY - 2, 404, SURF + 2, 1.8)
        b += lbl(398, 112, "h = 95 m", ORG, 14, "end", "700")
        # giọt nước chạy trong ống
        for i in range(6):
            t0 = 0.04 + 0.14 * i
            b += packet([(150, 120), P0, P1, (300, 212)], t0, min(t0 + 0.2, 0.98), DUR, BLUE, 4.5)
        return fig("c9-2-0", "0 0 420 272",
                   "Hồ chứa sau đập, nước chảy qua ống dẫn xuống tuabin đặt thấp hơn mặt hồ một độ cao h, tuabin quay máy phát",
                   b, "Mô phỏng: nước từ hồ chảy qua ống xuống làm quay tuabin. Hình không theo tỉ lệ.")
    # hình dữ kiện: chuỗi tính + hai mùa
    b += box(10, 14, 130, 62, BLUE, [("Mỗi giây", "700"), ("nước nặng d·L", "400")])
    b += box(150, 14, 270, 62, ORG, [("× h", "700"), ("→ công suất P_{n}", "400")])
    b += box(290, 14, 410, 62, GRN, [("× H", "700"), ("→ công suất P_{đ}", "400")])
    b += arrow("", "o", 130, 38, 148, 38, 2.2) + arrow("", "o", 270, 38, 288, 38, 2.2)
    b += lbl(16, 96, "Mùa mưa", BLUE, 15, "start", "700") + lbl(16, 118, "h = 95 m", "currentColor", 14, "start", "400")
    b += lbl(16, 138, "L = 250 m³/s", "currentColor", 14, "start", "400")
    b += lbl(220, 96, "Mùa khô", ORG, 15, "start", "700") + lbl(220, 118, "h = 80 m", "currentColor", 14, "start", "400")
    b += lbl(220, 138, "L = 160 m³/s", "currentColor", 14, "start", "400")
    b += lbl(16, 170, "Hai khâu nối tiếp: tuabin rồi máy phát", "currentColor", 14, "start", "400")
    b += lbl(16, 190, "H = H(tuabin) × H(máy phát)", GRN, 14, "start", "700")
    return fig("c9-2-2", "0 0 420 202", "Chuỗi tính công suất thuỷ điện: trọng lượng nước chảy mỗi giây nhân độ cao ra công suất dòng nước, nhân hiệu suất ra công suất điện; số liệu hai mùa",
               b, "Dữ kiện hai mùa; chưa tính công suất.")


# ───────────── Dạng 3 · pin Mặt Trời, giờ nắng đỉnh ─────────────
OX, OY, XH = 52, 200, 340 / 12          # gốc trục; px mỗi giờ (6 h → 18 h)
YW = 140 / 1000                          # px mỗi W/m²
IMAX = 4000 * math.pi / 24               # đường hình sin có diện tích 4000 Wh/m² = 1000 W/m² × 4 h


def ipt(h):
    I = IMAX * math.sin(math.pi * (h - 6) / 12) if 6 <= h <= 18 else 0
    return OX + XH * (h - 6), OY - YW * I


def d3(kk):
    b = ""
    if kk == 0:
        DUR = 6.0
        b += seg(OX, OY, OX + 356, OY, "currentColor", 1.8) + chevron(OX + 356, OY, 1, 0, "currentColor", 1.8, 9)
        b += seg(OX, OY, OX, 36, "currentColor", 1.8) + chevron(OX, 36, 0, -1, "currentColor", 1.8, 9)
        b += lbl(OX + 6, 34, "I (W/m²)", "currentColor", 14, "start", "400")
        b += lbl(OX + 356, OY + 36, "giờ trong ngày", "currentColor", 14, "end", "400")
        for h in (6, 9, 12, 15, 18):
            x = OX + XH * (h - 6)
            b += seg(x, OY, x, OY + 5, "currentColor", 1.4) + lbl(x, OY + 19, f"{h} h", "currentColor", 14, "middle", "400")
        y1000 = OY - YW * 1000
        b += seg(OX, y1000, OX + 340, y1000, GREY, 1.2, "4 3") + lbl(OX - 6, y1000 + 5, "1000", "currentColor", 14, "end", "400")
        b += lbl(OX - 6, OY + 5, "0", "currentColor", 14, "end", "400")
        pts = [ipt(6 + 12 * i / 60) for i in range(61)]
        area = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f" L{pts[-1][0]:.1f},{OY} L{pts[0][0]:.1f},{OY} Z"
        b += (f'<clipPath id="c9-3-clip"><rect x="{OX}" y="30" width="0" height="180">'
              f'{anim("width", "0;340;340", DUR, "0;0.6;1")}</rect></clipPath>')
        b += f'<path d="{area}" fill="{SUN}" opacity="0.30" stroke="none" clip-path="url(#c9-3-clip)"/>'
        b += poly(pts, SUN, 2.6)
        kt = ";".join(f"{0.6 * i / 60:.4f}" for i in range(61)) + ";1"
        b += (f'<circle cx="{pts[0][0]:.1f}" cy="{pts[0][1]:.1f}" r="7" fill="{SUN}" stroke="currentColor" stroke-width="1.4">'
              f'{anim("cx", ";".join(f"{x:.1f}" for x, _ in pts) + f";{pts[-1][0]:.1f}", DUR, kt)}'
              f'{anim("cy", ";".join(f"{y:.1f}" for _, y in pts) + f";{pts[-1][1]:.1f}", DUR, kt)}</circle>')
        xa, xb = OX + XH * 4, OX + XH * 8      # 10 h → 14 h
        b += (f'<g opacity="0">{anim("opacity", "0;0;1;1", DUR, "0;0.68;0.82;1")}'
              f'<rect x="{xa:.1f}" y="{y1000:.1f}" width="{xb - xa:.1f}" height="{OY - y1000:.1f}" fill="none" stroke="{RED}" stroke-width="2.2" stroke-dasharray="6 4"/>'
              f'{tx((xa + xb) / 2, y1000 - 8, "t_{đ} = 4 h", RED, 14, "middle", "700")}</g>')
        return fig("c9-3-0", "0 0 420 244",
                   "Cường độ nắng tăng từ sáng tới trưa rồi giảm tới chiều; vùng dưới đường cong được tô dần, sau đó hiện hình chữ nhật cao 1000 oát trên mét vuông rộng 4 giờ có cùng diện tích",
                   b, "Mô phỏng một ngày nắng: diện tích tô màu (năng lượng nắng cả ngày trên 1 m²) bằng diện tích hình chữ nhật nét đứt "
                      "cao 1000 W/m², rộng bằng số giờ nắng đỉnh.")
    # hình dữ kiện: chuỗi tính cho một tấm
    b += box(10, 12, 132, 60, SUN, [("Nắng", "700"), ("I = 1000 W/m²", "400")])
    b += box(150, 12, 270, 60, ORG, [("Tấm pin", "700"), ("S = 2 m², 20 %", "400")])
    b += box(288, 12, 410, 60, GRN, [("Biến tần", "700"), ("95 %", "400")])
    b += arrow("", "o", 132, 36, 148, 36, 2.2) + arrow("", "o", 270, 36, 286, 36, 2.2)
    b += tx(16, 96, "Công suất đỉnh 1 tấm: P_{đỉnh} = H_{pin}·I·S", "currentColor", 14, "start", "400")
    b += tx(16, 120, "Điện 1 tấm/ngày = P_{đỉnh}·t_{đ}·H_{bt}", "currentColor", 14, "start", "400")
    b += lbl(16, 144, "Nhu cầu: 375 kWh/tháng (30 ngày)", "currentColor", 14, "start", "400")
    b += lbl(16, 172, "So cùng một khoảng thời gian", GRN, 14, "start", "700")
    return fig("c9-3-2", "0 0 420 186", "Chuỗi năng lượng từ nắng qua tấm pin và biến tần tới gia đình, kèm công thức công suất đỉnh và điện năng một tấm mỗi ngày",
               b, "Dữ kiện của một tấm và nhu cầu của gia đình.")


BUILD = [d1, d2, d3]

# ═════════════ ĐỀ ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Chuỗi hiệu suất nhà máy nhiệt điện than: công suất nhiên liệu, hao phí từng khâu, than và CO₂",
      topic=TOPIC_HS,
      problem_html=r"""<p>Một nhà máy nhiệt điện đốt than gồm ba khâu nối tiếp: lò hơi (hiệu suất $H_1=90\,\%$) biến năng lượng của than thành nhiệt của hơi nước; tuabin ($H_2=42\,\%$) biến nhiệt của hơi thành cơ năng; máy phát ($H_3=96\,\%$) biến cơ năng thành điện năng. Nhà máy chạy liên tục, phát lên lưới công suất điện $330\ \text{MW}$. Than có năng suất toả nhiệt $q=2{,}7\cdot10^7\ \text{J/kg}$; mỗi kilôgam than cháy hết thải ra $k=2{,}5\ \text{kg}$ khí CO₂. Bỏ qua hao phí trên đường dây tải điện.</p><ol type="a"><li>Tính hiệu suất của cả nhà máy.</li><li>Tính công suất nhiên liệu (năng lượng than toả ra trong mỗi giây), tổng công suất hao phí và công suất hao phí ở từng khâu. Khâu nào hao phí nhiều nhất?</li><li>Tính khối lượng than nhà máy đốt trong một giờ, trong một ngày, và khối lượng CO₂ thải ra trong một ngày.</li><li>Cải tiến tuabin để hiệu suất tuabin tăng lên $45\,\%$ (hai khâu kia giữ nguyên), nhà máy vẫn phát $330\ \text{MW}$. Mỗi ngày nhà máy đốt bớt được bao nhiêu tấn than?</li></ol>"""),
 dict(label="Dạng 2 · Trung bình · Công suất thuỷ điện từ lưu lượng và độ cao cột nước; so với nhiệt điện than",
      topic=TOPIC_TT,
      problem_html=r"""<p>Một nhà máy thuỷ điện lấy nước từ hồ chứa qua ống dẫn xuống tuabin. Mùa mưa, độ cao cột nước (từ mặt hồ tới tuabin) là $h=95\ \text{m}$, lưu lượng nước qua tuabin là $L=250\ \text{m}^3\text{/s}$. Hiệu suất của tuabin là $92\,\%$, của máy phát là $96\,\%$. Khối lượng riêng của nước $D=1000\ \text{kg/m}^3$, trọng lượng riêng $d=10\,000\ \text{N/m}^3$. Bỏ qua hao phí trên đường dây tải điện.</p><ol type="a"><li>Tính công suất của dòng nước và công suất điện của nhà máy trong mùa mưa.</li><li>Mùa khô, độ cao cột nước giảm còn $80\ \text{m}$ và lưu lượng giảm còn $160\ \text{m}^3\text{/s}$. Tính công suất điện; công suất này bằng bao nhiêu phần trăm công suất mùa mưa?</li><li>Mùa khô (độ cao cột nước $80\ \text{m}$), muốn nhà máy giữ công suất điện $150\ \text{MW}$ thì lưu lượng nước qua tuabin phải bằng bao nhiêu?</li><li>Trong một ngày mùa mưa nhà máy chạy liên tục. Tính điện năng phát ra (MWh) và thể tích nước đã chảy qua tuabin. Nếu cùng lượng điện đó do nhà máy nhiệt điện than ở Dạng 1 làm ra (hiệu suất $36{,}288\,\%$; $q=2{,}7\cdot10^7\ \text{J/kg}$; mỗi kilôgam than thải $2{,}5\ \text{kg}$ CO₂) thì phải đốt bao nhiêu tấn than và thải ra bao nhiêu tấn CO₂?</li></ol>"""),
 dict(label="Dạng 3 · Trung bình · Pin Mặt Trời cho một gia đình: giờ nắng đỉnh, số tấm làm tròn lên, thời gian hoàn vốn",
      topic=TOPIC_TK,
      problem_html=r"""<p>Một gia đình dùng trung bình $375\ \text{kWh}$ điện mỗi tháng (tính $30$ ngày) và muốn lắp pin Mặt Trời trên mái. Mỗi tấm pin có diện tích $2{,}0\ \text{m}^2$, hiệu suất $20\,\%$. Ở nơi đó nắng mạnh nhất có cường độ $I=1000\ \text{W/m}^2$, và số giờ nắng đỉnh trung bình là $t_{\text{đ}}=4{,}0$ giờ mỗi ngày (năng lượng nắng cả ngày trên mỗi mét vuông bằng năng lượng nhận được nếu nắng $1000\ \text{W/m}^2$ chiếu đều trong $4$ giờ). Điện từ pin phải qua bộ biến tần có hiệu suất $95\,\%$ mới dùng được trong nhà.</p><ol type="a"><li>Tính công suất đỉnh của một tấm pin và điện năng một tấm cho mỗi ngày (sau biến tần).</li><li>Cần ít nhất bao nhiêu tấm để đủ điện cho gia đình? Công suất đỉnh của cả hệ là bao nhiêu?</li><li>Mái nhà chỉ đặt được $14\ \text{m}^2$ pin. Mỗi tháng gia đình còn phải mua của lưới điện bao nhiêu kWh?</li><li>Lắp đủ số tấm ở câu b hết $67{,}5$ triệu đồng; giá điện lưới là $2\,800$ đồng/kWh. Coi toàn bộ $375\ \text{kWh}$ mỗi tháng do hệ pin cấp, phần điện dư không bán được. Sau bao nhiêu năm thì tiền điện tiết kiệm được đủ bù tiền lắp đặt?</li></ol>"""),
]

# ═════════════ BẢNG PHÂN TÍCH ĐỀ ═════════════
ANALYSIS = [
 # Dạng 1
 [(r'"ba khâu nối tiếp: lò hơi ($H_1=90\,\%$) … tuabin ($H_2=42\,\%$) … máy phát ($H_3=96\,\%$)"', r"$H_1$; $H_2$; $H_3$",
   r"⚠ khâu sau chỉ nhận phần năng lượng có ích của khâu trước: nối tiếp thì $H=H_1H_2H_3$<br>Không cộng, không lấy trung bình"),
  (r'"phát lên lưới công suất điện $330\ \text{MW}$"', r"$P_{\text{đ}}=330\ \text{MW}$ (có ích)",
   r"$H=\dfrac{P_{\text{ích}}}{P_{\text{tp}}}$, công suất toàn phần là của than"),
  (r'"Bỏ qua hao phí trên đường dây"', r"Điện ra khỏi máy phát tới lưới đủ", r"⚠ hao phí chỉ tính trong ba khâu của nhà máy"),
  (r'"$q=2{,}7\cdot10^7\ \text{J/kg}$; mỗi kilôgam than … thải ra $k=2{,}5\ \text{kg}$ CO₂"', r"$q$; $k$",
   r"Năng lượng than toả $Q=qm$<br>$m_{\text{CO}_2}=k\,m$"),
  (r'"hiệu suất của cả nhà máy"', r"Cần $H$", r"$H=H_1H_2H_3$"),
  (r'"công suất nhiên liệu … hao phí ở từng khâu"', r"Cần $P_{nl}$, $P_{hp}$ và hao phí mỗi khâu",
   r"$P_{nl}=\dfrac{P_{\text{đ}}}{H}$<br>Mỗi khâu hao $(1-H_i)\times$ công suất <b>vào</b> khâu đó"),
  (r'"khối lượng than … trong một giờ, trong một ngày"', r"Cần $m$; $t=3600\ \text{s}$; $t=86\,400\ \text{s}$",
   r"$m=\dfrac{P_{nl}\,t}{q}$ (W = J/s nên $t$ tính bằng giây)"),
  (r'"hiệu suất tuabin tăng lên $45\,\%$ … vẫn phát $330\ \text{MW}$"', r"$H_2'=45\,\%$",
   r"$H$ cả nhà máy thay đổi thế nào? Lượng than mới so với lượng than cũ?")],
 # Dạng 2
 [(r'"độ cao cột nước (từ mặt hồ tới tuabin) là $h=95\ \text{m}$"', r"$h=95\ \text{m}$",
   r"Nước rơi độ cao $h$: trọng lực sinh công $A=P\,h$ (trọng lượng nhân độ cao)"),
  (r'"lưu lượng … $L=250\ \text{m}^3\text{/s}$"; "$d=10\,000\ \text{N/m}^3$"', r"$L$; $d$",
   r"Mỗi giây có thể tích $L$ chảy qua, trọng lượng $d\,L$<br>Công suất dòng nước $P_n=d\,L\,h$"),
  (r'"Hiệu suất của tuabin là $92\,\%$, của máy phát là $96\,\%$"', r"$H_t$; $H_m$",
   r"⚠ hai khâu nối tiếp: $H=H_tH_m$, rồi $P_{\text{đ}}=H\,P_n$<br>⚠ dùng $d=10D$, không dùng $D$"),
  (r'"Mùa khô … $80\ \text{m}$ … $160\ \text{m}^3\text{/s}$"', r"$h'$; $L'$", r"$P_{\text{đ}}$ tỉ lệ với cả $h$ lẫn $L$"),
  (r'"giữ công suất điện $150\ \text{MW}$"', r"Cần $L$", r"Rút $L$ từ $P_{\text{đ}}=H\,d\,L\,h$"),
  (r'"một ngày … điện năng phát ra (MWh) và thể tích nước"', r"$t=24\ \text{h}=86\,400\ \text{s}$",
   r"$A=P_{\text{đ}}\,t$ (MW nhân giờ ra MWh)<br>$V=L\,t$"),
  (r'"do nhà máy nhiệt điện than … hiệu suất $36{,}288\,\%$ … phải đốt bao nhiêu tấn than"', r"Cần $m$, $m_{\text{CO}_2}$",
   r"Cùng lượng điện thì than phải toả nhiều hơn hay ít hơn điện năng? $H$ của nhà máy than vào chỗ nào?")],
 # Dạng 3
 [(r'"$375\ \text{kWh}$ điện mỗi tháng (tính $30$ ngày)"', r"$A_{\text{th}}=375\ \text{kWh}$",
   r"So với điện một tấm cho trong <b>một ngày</b> thì phải đổi về cùng khoảng thời gian"),
  (r'"tấm pin … $2{,}0\ \text{m}^2$, hiệu suất $20\,\%$"; "$I=1000\ \text{W/m}^2$"', r"$S$; $H_{pin}$; $I$",
   r"Công suất đỉnh $P_{\text{đỉnh}}=H_{pin}\,I\,S$"),
  (r'"số giờ nắng đỉnh … $t_{\text{đ}}=4{,}0$ giờ mỗi ngày"', r"$t_{\text{đ}}=4\ \text{h}$",
   r"⚠ năng lượng nắng cả ngày đã quy về $1000\ \text{W/m}^2$ trong $t_{\text{đ}}$ giờ: không dùng số giờ trời sáng"),
  (r'"qua bộ biến tần có hiệu suất $95\,\%$"', r"$H_{bt}=0{,}95$",
   r"⚠ điện dùng được $=H_{bt}\times$ điện pin phát: phải nhân thêm"),
  (r'"Cần ít nhất bao nhiêu tấm"', r"Cần $n$ (số nguyên)", r"$n=\dfrac{\text{nhu cầu ngày}}{\text{điện 1 tấm/ngày}}$; làm tròn theo hướng nào thì mới đủ điện?"),
  (r'"Mái nhà chỉ đặt được $14\ \text{m}^2$"', r"$S_{\text{mái}}=14\ \text{m}^2$", r"Đặt được bao nhiêu tấm? Phần thiếu so với nhu cầu, rồi nhân số ngày"),
  (r'"hết $67{,}5$ triệu đồng; giá điện … $2\,800$ đồng/kWh … phần điện dư không bán"', r"Cần thời gian hoàn vốn",
   r"Mỗi tháng tiết kiệm tiền của bao nhiêu kWh? Đổi số tháng ra năm thế nào?")],
]

# ═════════════ LỜI GIẢI ═════════════
R1 = [r"<strong>Khái niệm:</strong> năng lượng không tự mất đi; phần hao phí ở mỗi khâu biến thành nhiệt toả ra môi trường.",
      r"<strong>Định nghĩa:</strong> hiệu suất $H=\dfrac{P_{\text{ích}}}{P_{\text{tp}}}\lt1$; hao phí $P_{hp}=P_{\text{tp}}-P_{\text{ích}}$.",
      r"<strong>Công thức:</strong> nhiều khâu nối tiếp $H=H_1H_2H_3$; than toả $Q=qm$; $m_{\text{CO}_2}=k\,m$.",
      r"<strong>Điều kiện:</strong> khâu sau chỉ nhận phần có ích của khâu trước; công suất (W) nhân thời gian (s) ra năng lượng (J)."]
R2 = [r"<strong>Khái niệm:</strong> nước trên hồ có thế năng; khi chảy xuống độ cao $h$, trọng lực sinh công làm quay tuabin.",
      r"<strong>Công thức:</strong> mỗi giây trọng lượng nước chảy qua là $d\,L$, nên công suất dòng nước $P_n=d\,L\,h$.",
      r"<strong>Hiệu suất:</strong> $P_{\text{đ}}=H\,P_n$ với $H=H_tH_m$ (tuabin nối tiếp máy phát).",
      r"<strong>Điều kiện:</strong> $d=10D=10\,000\ \text{N/m}^3$; bỏ qua hao phí trên đường dây."]
R3 = [r"<strong>Khái niệm:</strong> số giờ nắng đỉnh $t_{\text{đ}}$ là số giờ quy đổi: năng lượng nắng cả ngày bằng nắng $1000\ \text{W/m}^2$ chiếu trong $t_{\text{đ}}$ giờ.",
      r"<strong>Công thức:</strong> $P_{\text{đỉnh}}=H_{pin}\,I\,S$; điện một tấm mỗi ngày $A_1=P_{\text{đỉnh}}\,t_{\text{đ}}\,H_{bt}$.",
      r"<strong>Số tấm:</strong> $n=\dfrac{A_{\text{ngày}}}{A_1}$, làm tròn <b>lên</b> để đủ điện.",
      r"<strong>Điều kiện:</strong> nhu cầu và sản lượng phải cùng một khoảng thời gian (cùng một ngày hoặc cùng một tháng)."]

SOLS = [
 sol(R1, [
  ("Hiệu suất cả nhà máy", [P(r"Ba khâu nối tiếp nên nhân các hiệu suất:"),
     M(r"H=H_1H_2H_3=0{,}90\cdot0{,}42\cdot0{,}96=0{,}36288"), A(r"H\approx36{,}3\,\%")]),
  ("Công suất nhiên liệu và tổng hao phí", [P(r"Công suất có ích là công suất điện, công suất toàn phần là của than:"),
     M(r"P_{nl}=\dfrac{P_{\text{đ}}}{H}=\dfrac{330}{0{,}36288}"), A(r"P_{nl}\approx909{,}4\ \text{MW}"),
     M(r"P_{hp}=P_{nl}-P_{\text{đ}}\approx909{,}4-330"), A(r"P_{hp}\approx579{,}4\ \text{MW}")]),
  ("Hao phí từng khâu", [P(r"Mỗi khâu hao $(1-H_i)$ nhân công suất <b>vào</b> khâu đó:"),
     M(r"\text{Lò hơi: }0{,}10\cdot909{,}4\approx90{,}9\ \text{MW};\quad P_1=0{,}90\cdot909{,}4\approx818{,}5\ \text{MW}"),
     M(r"\text{Tuabin: }0{,}58\cdot818{,}5\approx474{,}7\ \text{MW};\quad P_2=0{,}42\cdot818{,}5\approx343{,}8\ \text{MW}"),
     M(r"\text{Máy phát: }0{,}04\cdot343{,}8\approx13{,}75\ \text{MW}"),
     A(r"\text{Tuabin hao nhiều nhất}\ (\approx474{,}7\ \text{MW})"),
     P(r"Cộng lại: $90{,}9+474{,}7+13{,}75\approx579{,}4\ \text{MW}$, khớp tổng hao phí.")]),
  ("Than đốt trong một giờ, một ngày", [P(r"Mỗi giây than toả $P_{nl}$ jun:"),
     M(r"\dfrac{m}{t}=\dfrac{P_{nl}}{q}=\dfrac{909{,}4\cdot10^6}{2{,}7\cdot10^7}\approx33{,}68\ \text{kg/s}"),
     M(r"m_{\text{giờ}}=33{,}68\cdot3600\approx121\,250\ \text{kg}\approx121{,}3\ \text{tấn}"),
     M(r"m_{\text{ngày}}=33{,}68\cdot86\,400\ \text{kg}"), A(r"m_{\text{ngày}}\approx2910\ \text{tấn}"),
     P(r"Cùng một ngày nhà máy phát $A=330\ \text{MW}\cdot24\ \text{h}=7920\ \text{MWh}$ điện.")]),
  ("CO₂ thải trong một ngày", [M(r"m_{\text{CO}_2}=k\,m_{\text{ngày}}=2{,}5\cdot2910"), A(r"m_{\text{CO}_2}\approx7275\ \text{tấn}")]),
  ("Cải tiến tuabin", [M(r"H'=0{,}90\cdot0{,}45\cdot0{,}96=0{,}3888"),
     P(r"Cùng công suất điện, lượng than tỉ lệ nghịch với $H$:"),
     M(r"m'_{\text{ngày}}=2910\cdot\dfrac{0{,}36288}{0{,}3888}\approx2716\ \text{tấn}"),
     M(r"\Delta m=2910-2716"), A(r"\Delta m\approx194\ \text{tấn/ngày}\ (\approx6{,}7\,\%)")]),
  ("Kiểm tra", [P(r"$H\approx36\,\%\lt1$, đúng cỡ hiệu suất nhà máy nhiệt điện than thực tế ($30$–$40\,\%$) ✓."),
     P(r"Tổng hao phí ba khâu bằng $P_{nl}-P_{\text{đ}}$ ✓. Hao phí lớn nhất ở khâu nhiệt → cơ (tuabin), không phải máy phát ✓."),
     P(r"Đơn vị: $\dfrac{\text{W}\cdot\text{s}}{\text{J/kg}}=\dfrac{\text{J}}{\text{J/kg}}=\text{kg}$ ✓.")])],
  [r"a) $H\approx36{,}3\,\%$", r"b) $P_{nl}\approx909{,}4\ \text{MW}$; $P_{hp}\approx579{,}4\ \text{MW}$",
   r"b) Lò hơi $\approx90{,}9\ \text{MW}$; tuabin $\approx474{,}7\ \text{MW}$ (nhiều nhất); máy phát $\approx13{,}75\ \text{MW}$",
   r"c) Khoảng $121{,}3$ tấn than mỗi giờ; $2910$ tấn mỗi ngày", r"c) Khoảng $7275$ tấn CO₂ mỗi ngày",
   r"d) Bớt khoảng $194$ tấn than mỗi ngày"],
  r"Nhận dạng: thấy <strong>nhiều khâu nối tiếp, mỗi khâu một hiệu suất</strong> → nhân các hiệu suất; công suất than $=P_{\text{ích}}/H$."),
 sol(R2, [
  ("Công suất dòng nước mùa mưa", [P(r"Mỗi giây có $250\ \text{m}^3$ nước nặng $d\,L$ rơi độ cao $95\ \text{m}$:"),
     M(r"P_n=d\,L\,h=10\,000\cdot250\cdot95"), A(r"P_n=2{,}375\cdot10^8\ \text{W}=237{,}5\ \text{MW}")]),
  ("Công suất điện mùa mưa", [M(r"H=0{,}92\cdot0{,}96=0{,}8832"), M(r"P_{\text{đ}}=H\,P_n=0{,}8832\cdot237{,}5"),
     A(r"P_{\text{đ}}\approx209{,}8\ \text{MW}")]),
  ("Công suất điện mùa khô", [P(r"Cả $h$ lẫn $L$ cùng giảm:"), M(r"P'_{\text{đ}}=0{,}8832\cdot10\,000\cdot160\cdot80"),
     A(r"P'_{\text{đ}}\approx113{,}0\ \text{MW}"),
     M(r"\dfrac{P'_{\text{đ}}}{P_{\text{đ}}}=\dfrac{160\cdot80}{250\cdot95}\approx0{,}539"),
     P(r"Mùa khô chỉ còn khoảng $54\,\%$ công suất mùa mưa.")]),
  ("Lưu lượng để giữ 150 MW", [M(r"L=\dfrac{P_{\text{đ}}}{H\,d\,h}=\dfrac{150\cdot10^6}{0{,}8832\cdot10\,000\cdot80}"),
     A(r"L\approx212{,}3\ \text{m}^3\text{/s}")]),
  ("Điện năng trong một ngày", [M(r"A=P_{\text{đ}}\,t=209{,}76\ \text{MW}\cdot24\ \text{h}"), A(r"A\approx5034\ \text{MWh}")]),
  ("Thể tích nước trong một ngày", [P(r"Mỗi giây có $L$ mét khối chảy qua, một ngày có $86\,400\ \text{s}$:"),
     M(r"V=L\,t=250\cdot86\,400"), A(r"V=2{,}16\cdot10^7\ \text{m}^3")]),
  ("Than nếu dùng nhiệt điện", [P(r"Đổi $A$ ra jun: $A\approx5034\cdot3{,}6\cdot10^9\approx1{,}812\cdot10^{13}\ \text{J}$. Than phải toả $A/H_{than}$:"),
     M(r"m=\dfrac{A}{H_{than}\,q}=\dfrac{1{,}812\cdot10^{13}}{0{,}36288\cdot2{,}7\cdot10^7}\ \text{kg}"),
     A(r"m\approx1850\ \text{tấn}")]),
  ("CO₂ thải ra", [M(r"m_{\text{CO}_2}=k\,m=2{,}5\cdot1849{,}7"), A(r"m_{\text{CO}_2}\approx4624\ \text{tấn}")]),
  ("Kiểm tra", [P(r"$P_{\text{đ}}\lt P_n$ ✓. Mùa khô $h$ giảm $16\,\%$, $L$ giảm $36\,\%$, công suất giảm gần một nửa: hai thừa số cùng giảm ✓."),
     P(r"Đơn vị: $\dfrac{\text{N}}{\text{m}^3}\cdot\dfrac{\text{m}^3}{\text{s}}\cdot\text{m}=\dfrac{\text{N·m}}{\text{s}}=\text{W}$ ✓."),
     P(r"Một ngày mùa mưa nhà máy thuỷ điện này giúp tránh đốt gần $2$ nghìn tấn than ✓.")])],
  [r"a) $P_n=237{,}5\ \text{MW}$; $P_{\text{đ}}\approx209{,}8\ \text{MW}$", r"b) $P'_{\text{đ}}\approx113{,}0\ \text{MW}$, khoảng $54\,\%$ mùa mưa",
   r"c) $L\approx212{,}3\ \text{m}^3\text{/s}$", r"d) $A\approx5034\ \text{MWh}$; $V=2{,}16\cdot10^7\ \text{m}^3$",
   r"d) Khoảng $1850$ tấn than; khoảng $4624$ tấn CO₂"],
  r"Nhận dạng: thấy <strong>lưu lượng nước và độ cao cột nước</strong> → $P_n=d\,L\,h$, rồi nhân hiệu suất ra công suất điện."),
 sol(R3, [
  ("Nhu cầu mỗi ngày", [M(r"A_{\text{ngày}}=\dfrac{375}{30}"), A(r"A_{\text{ngày}}=12{,}5\ \text{kWh}")]),
  ("Công suất đỉnh một tấm", [M(r"P_{\text{đỉnh}}=H_{pin}\,I\,S=0{,}20\cdot1000\cdot2{,}0"), A(r"P_{\text{đỉnh}}=400\ \text{W}")]),
  ("Điện một tấm mỗi ngày", [P(r"Nhân với số giờ nắng đỉnh rồi với hiệu suất biến tần:"),
     M(r"A_1=P_{\text{đỉnh}}\,t_{\text{đ}}\,H_{bt}=400\cdot4\cdot0{,}95=1520\ \text{Wh}"), A(r"A_1=1{,}52\ \text{kWh}")]),
  ("Số tấm tối thiểu", [M(r"n=\dfrac{A_{\text{ngày}}}{A_1}=\dfrac{12{,}5}{1{,}52}\approx8{,}22"),
     P(r"$8$ tấm cho $8\cdot1{,}52=12{,}16\ \text{kWh}\lt12{,}5\ \text{kWh}$: thiếu. Phải làm tròn <b>lên</b>:"),
     A(r"n=9\ \text{tấm}"), M(r"P_{\text{hệ}}=9\cdot400\ \text{W}=3{,}6\ \text{kW}")]),
  ("Mái chỉ có 14 m²", [M(r"n_{\text{mái}}=\dfrac{14}{2{,}0}=7\ \text{tấm};\quad A_{\text{mái}}=7\cdot1{,}52=10{,}64\ \text{kWh/ngày}"),
     M(r"\text{Thiếu mỗi ngày: }12{,}5-10{,}64=1{,}86\ \text{kWh}"),
     M(r"\text{Mỗi tháng: }1{,}86\cdot30"), A(r"55{,}8\ \text{kWh/tháng}")]),
  ("Thời gian hoàn vốn", [P(r"Phần điện dư không bán nên mỗi tháng chỉ tiết kiệm tiền của đúng $375\ \text{kWh}$:"),
     M(r"\text{Tiết kiệm mỗi tháng}=375\cdot2800=1\,050\,000\ \text{đồng}"),
     M(r"\text{Số tháng}=\dfrac{67\,500\,000}{1\,050\,000}\approx64{,}3"), A(r"\approx5{,}4\ \text{năm}")]),
  ("Kiểm tra", [P(r"$9$ tấm cho $9\cdot1{,}52=13{,}68\ \text{kWh/ngày}\ge12{,}5$ ✓; chiếm $18\ \text{m}^2$ mái."),
     P(r"Nếu lấy $12$ giờ trời sáng thay cho $4$ giờ nắng đỉnh sẽ ra chưa tới $3$ tấm: quá ít, vì nắng chỉ mạnh vào giữa trưa."),
     P(r"Hoàn vốn khoảng $5$ năm, ngắn hơn tuổi thọ thường gặp của tấm pin (khoảng $20$ năm trở lên) ✓.")])],
  [r"a) $P_{\text{đỉnh}}=400\ \text{W}$; mỗi tấm $1{,}52\ \text{kWh/ngày}$", r"b) $9$ tấm; công suất đỉnh hệ $3{,}6\ \text{kW}$",
   r"c) Mua thêm $55{,}8\ \text{kWh}$ mỗi tháng", r"d) Khoảng $64$ tháng, tức khoảng $5{,}4$ năm"],
  r"Nhận dạng: thấy <strong>số giờ nắng đỉnh, diện tích tấm, hiệu suất pin</strong> → $A_1=H\,I\,S\,t_{\text{đ}}H_{bt}$; số tấm làm tròn lên."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC ═════════════
STEPS = [
 # ── Dạng 1 ──
 dict(nhan_dang=r"Thấy <b>nhiều khâu nối tiếp, mỗi khâu một hiệu suất</b> → nhân các hiệu suất; công suất than bằng công suất có ích chia $H$.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Hiệu suất cả nhà máy", "Hiệu suất của cả nhà máy là bao nhiêu %?", 36.3, "%", 0.1,
       loi=r"Cộng ba hiệu suất hoặc lấy trung bình cộng; năng lượng đi qua lần lượt từng khâu, khâu sau chỉ nhận phần có ích của khâu trước, nên phải nhân."),
  buoc("Công suất nhiên liệu và tổng hao phí", "Công suất nhiên liệu P_nl bằng bao nhiêu MW?", 909.4, "MW", 8,
       loi=r"Nhân công suất điện với $H$ thay vì chia; công suất vào phải lớn hơn công suất ra.",
       ke=[(r"Tính $P_{nl}=\dfrac{P_{\text{đ}}}{H}$", True),
           (r"Tính $P_{nl}=P_{\text{đ}}\cdot H$", r"Nhân với $H\lt1$ cho số nhỏ hơn công suất điện, vô lí: than phải cấp nhiều hơn điện thu được."),
           (r"Tính $P_{nl}=\dfrac{P_{\text{đ}}}{H_3}$", r"Chia cho riêng $H_3$ mới lùi về đầu vào máy phát, chưa lùi qua tuabin và lò hơi tới than.")]),
  buoc("Hao phí từng khâu", "Công suất hao phí ở tuabin bằng bao nhiêu MW?", 474.7, "MW", 1.5,
       loi=r"Nhân $(1-H_2)$ với công suất của than; tuabin chỉ nhận phần lò hơi đưa ra, không nhận toàn bộ $P_{nl}$.",
       ke=[(r"Nhân $(1-H_2)$ với công suất vào tuabin $P_1=H_1P_{nl}$", True),
           (r"Nhân $(1-H_2)$ với $P_{nl}$", r"Lò hơi đã hao một phần trước đó, nên công suất vào tuabin nhỏ hơn $P_{nl}$."),
           (r"Nhân $(1-H_2)$ với $P_{\text{đ}}$", r"Công suất điện là đầu ra của máy phát, khâu cuối; tuabin nhận công suất lớn hơn nhiều.")]),
  buoc("Than đốt trong một giờ, một ngày", "Mỗi ngày nhà máy đốt bao nhiêu tấn than?", 2910, "tấn", 5,
       loi=r"Dùng công suất điện để tính than; than phải cấp cả phần năng lượng hao phí.",
       ke=[(r"Tính $m=\dfrac{P_{nl}\,t}{q}$ với $t=86\,400\ \text{s}$", True),
           (r"Tính $m=\dfrac{P_{\text{đ}}\,t}{q}$", r"Công suất điện chỉ là phần có ích; than phải cấp toàn bộ công suất nhiên liệu."),
           (r"Tính $m=\dfrac{P_{nl}\,t}{q}$ với $t=24$", r"Oát là jun trên giây, nên thời gian phải đổi ra giây.")]),
  buoc("CO₂ thải trong một ngày", "Mỗi ngày nhà máy thải ra bao nhiêu tấn CO₂?", 7275, "tấn", 15,
       loi=r"Chia khối lượng than cho $k$; $k$ là số kilôgam CO₂ ứng với mỗi kilôgam than nên phải nhân.",
       ke=[(r"Tính $m_{\text{CO}_2}=k\,m_{\text{than}}$", True),
           (r"Tính $m_{\text{CO}_2}=\dfrac{m_{\text{than}}}{k}$", r"$k=2{,}5$ kg CO₂ trên mỗi kg than: than càng nhiều CO₂ càng nhiều, nên nhân."),
           (r"Lấy $m_{\text{CO}_2}=m_{\text{than}}$", r"Khi cháy, than kết hợp thêm khí oxi của không khí nên khối lượng CO₂ khác khối lượng than; dùng hệ số $k$ đề cho.")]),
  buoc("Cải tiến tuabin", "Mỗi ngày nhà máy đốt bớt được bao nhiêu tấn than?", 194, "tấn", 3,
       loi=r"Lấy lượng than cũ nhân với mức tăng 3 điểm phần trăm của tuabin; lượng than tỉ lệ nghịch với hiệu suất cả nhà máy.",
       ke=[(r"Tính $H'=H_1\cdot0{,}45\cdot H_3$, tính lượng than mới rồi trừ khỏi lượng cũ", True),
           (r"Lấy lượng than cũ nhân $(45\,\%-42\,\%)$", r"Mức tăng 3 điểm phần trăm là của riêng tuabin, không phải tỉ lệ than giảm."),
           (r"Cộng thêm 3 điểm phần trăm vào hiệu suất cả nhà máy rồi tính lại than", r"Tuabin chỉ là một khâu; $H$ cả nhà máy còn nhân với $H_1$, $H_3$ nên tăng ít hơn 3 điểm phần trăm.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 2 ──
 dict(nhan_dang=r"Thấy <b>lưu lượng nước và độ cao cột nước</b> → $P_n=d\,L\,h$, rồi nhân hiệu suất ra công suất điện.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Công suất dòng nước mùa mưa", "Công suất của dòng nước mùa mưa là bao nhiêu MW?", 237.5, "MW", 0.5,
       loi=r"Dùng khối lượng riêng $D$ thay cho trọng lượng riêng $d=10D$: công là trọng lượng (N) nhân độ cao, không phải khối lượng nhân độ cao."),
  buoc("Công suất điện mùa mưa", "Công suất điện mùa mưa bằng bao nhiêu MW?", 209.8, "MW", 0.3,
       loi=r"Chỉ nhân hiệu suất tuabin, quên máy phát cũng hao một phần.",
       ke=[(r"Nhân $P_n$ với $H=0{,}92\cdot0{,}96$", True),
           (r"Nhân $P_n$ với $0{,}92$", r"Điện lấy ra ở máy phát, nên còn hao ở máy phát; phải nhân cả $0{,}96$."),
           (r"Nhân $P_n$ với trung bình $\dfrac{0{,}92+0{,}96}{2}$", r"Hai khâu nối tiếp thì hiệu suất nhân với nhau, không lấy trung bình.")]),
  buoc("Công suất điện mùa khô", "Công suất điện mùa khô bằng bao nhiêu MW?", 113.05, "MW", 0.6,
       loi=r"Chỉ đổi một trong hai đại lượng $h$, $L$; mùa khô cả hai cùng giảm.",
       ke=[(r"Tính lại $P_{\text{đ}}=H\,d\,L\,h$ với cả $h$ và $L$ mới", True),
           (r"Chỉ đổi $h$, giữ $L=250\ \text{m}^3\text{/s}$", r"Mùa khô lưu lượng cũng giảm; công suất tỉ lệ với cả hai thừa số."),
           (r"Chỉ đổi $L$, giữ $h=95\ \text{m}$", r"Mực hồ hạ nên độ cao cột nước cũng giảm.")]),
  buoc("Lưu lượng để giữ 150 MW", "Lưu lượng cần thiết là bao nhiêu m³/s?", 212.3, "m³/s", 0.5,
       loi=r"Quên chia cho hiệu suất: công suất cho trước là công suất điện, dòng nước phải cấp nhiều hơn thế.",
       ke=[(r"Tính $L=\dfrac{P_{\text{đ}}}{H\,d\,h}$", True),
           (r"Tính $L=\dfrac{P_{\text{đ}}}{d\,h}$", r"Bỏ mất hiệu suất: phần hao ở tuabin và máy phát cũng phải do dòng nước cấp."),
           (r"Tính $L=\dfrac{H\,P_{\text{đ}}}{d\,h}$", r"Nhân $H$ làm lưu lượng nhỏ đi; muốn ra đủ điện thì nước vào phải nhiều hơn, nên chia cho $H$.")]),
  buoc("Điện năng trong một ngày", "Điện năng phát ra trong một ngày mùa mưa là bao nhiêu MWh?", 5034, "MWh", 5,
       loi=r"Nhân công suất với số giây nhưng vẫn ghi đơn vị MWh; MW nhân giây ra MJ.",
       ke=[(r"Tính $A=P_{\text{đ}}\cdot24\ \text{h}$", True),
           (r"Tính $A=P_n\cdot24\ \text{h}$", r"$P_n$ là công suất của dòng nước, chưa trừ hao phí ở tuabin và máy phát."),
           (r"Tính $A=P_{\text{đ}}\cdot86\,400$ rồi ghi đơn vị MWh", r"MW nhân giây ra MJ; muốn có MWh phải nhân với số giờ.")]),
  buoc("Thể tích nước trong một ngày", "Thể tích nước qua tuabin trong một ngày là a·10⁷ m³. Hệ số a bằng bao nhiêu?", 2.16, "", 0.02,
       loi=r"Nhân lưu lượng với số giờ thay vì số giây; lưu lượng tính theo mét khối mỗi giây.",
       ke=[(r"Tính $V=L\,t$ với $t=86\,400\ \text{s}$", True),
           (r"Tính $V=L\cdot24$", r"$L$ là mét khối trong mỗi giây, nên thời gian phải đổi ra giây."),
           (r"Tính lưu lượng từ công suất điện $\dfrac{P_{\text{đ}}}{d\,h}$ rồi nhân $t$", r"Công suất điện đã trừ hao phí; lượng nước thật chảy qua tuabin chính là $L$ đề cho.")]),
  buoc("Than nếu dùng nhiệt điện", "Nhà máy than phải đốt bao nhiêu tấn than?", 1850, "tấn", 6,
       loi=r"Quên chia cho hiệu suất của nhà máy than; chỉ một phần năng lượng than toả ra thành điện.",
       ke=[(r"Tính $m=\dfrac{A}{H_{than}\,q}$ với $A$ đổi ra jun", True),
           (r"Tính $m=\dfrac{H_{than}\,A}{q}$", r"Than phải toả nhiều năng lượng hơn điện thu được, nên chia cho $H_{than}$ chứ không nhân."),
           (r"Tính $m=\dfrac{A}{q}$", r"Bỏ qua hao phí của nhà máy than; phần lớn năng lượng than thành nhiệt thải.")]),
  buoc("CO₂ thải ra", "Nhà máy than thải ra bao nhiêu tấn CO₂?", 4624, "tấn", 15,
       loi=r"Chia khối lượng than cho $k$ hoặc nhân $k$ với điện năng; $k$ là số kilôgam CO₂ trên mỗi kilôgam than.",
       ke=[(r"Tính $m_{\text{CO}_2}=k\,m_{\text{than}}$", True),
           (r"Tính $m_{\text{CO}_2}=\dfrac{m_{\text{than}}}{k}$", r"Than càng nhiều thì CO₂ càng nhiều; $k$ kg CO₂ ứng với mỗi kg than nên phải nhân."),
           (r"Nhân $k$ với điện năng tính bằng MWh", r"$k$ tính trên khối lượng than đốt, không tính trên điện năng.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 3 ──
 dict(nhan_dang=r"Thấy <b>số giờ nắng đỉnh, diện tích tấm, hiệu suất pin</b> → điện một tấm $=H\,I\,S\,t_{\text{đ}}H_{bt}$; số tấm làm tròn lên.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Nhu cầu mỗi ngày", "Mỗi ngày gia đình cần bao nhiêu kWh?", 12.5, "kWh", 0.05,
       loi=r"Chia cho số giờ hoặc số tháng thay vì số ngày đề cho trong tháng."),
  buoc("Công suất đỉnh một tấm", "Công suất đỉnh của một tấm pin là bao nhiêu W?", 400, "W", 2,
       loi=r"Quên nhân hiệu suất pin: tấm chỉ biến một phần năng lượng nắng thành điện.",
       ke=[(r"Tính $P_{\text{đỉnh}}=H_{pin}\,I\,S$", True),
           (r"Tính $P=I\,S$", r"Đó là công suất nắng chiếu lên tấm; pin chỉ biến $20\,\%$ thành điện."),
           (r"Tính $P=H_{pin}\,I$", r"Đó là công suất điện trên $1\ \text{m}^2$; tấm có diện tích $2\ \text{m}^2$.")]),
  buoc("Điện một tấm mỗi ngày", "Mỗi ngày một tấm cho bao nhiêu kWh sau biến tần?", 1.52, "kWh", 0.02,
       loi=r"Lấy số giờ trời sáng thay cho số giờ nắng đỉnh; nắng chỉ mạnh vào giữa trưa, số giờ nắng đỉnh đã quy đổi sẵn.",
       ke=[(r"Nhân $P_{\text{đỉnh}}$ với $t_{\text{đ}}=4\ \text{h}$ rồi với $0{,}95$", True),
           (r"Nhân $P_{\text{đỉnh}}$ với $12\ \text{h}$ trời sáng rồi với $0{,}95$", r"Nắng không giữ $1000\ \text{W/m}^2$ suốt 12 giờ; công suất đỉnh chỉ đạt khi nắng mạnh nhất."),
           (r"Nhân $P_{\text{đỉnh}}$ với $4\ \text{h}$, không nhân $0{,}95$", r"Điện phải qua biến tần mới dùng được, biến tần hao $5\,\%$.")]),
  buoc("Số tấm tối thiểu", "Cần ít nhất bao nhiêu tấm pin?", 9, "tấm", 0,
       loi=r"Làm tròn xuống (hoặc làm tròn theo quy tắc thông thường) khiến hệ thiếu điện.",
       ke=[(r"Chia nhu cầu ngày cho điện một tấm mỗi ngày, làm tròn lên", True),
           (r"Chia nhu cầu ngày cho điện một tấm mỗi ngày, làm tròn theo quy tắc thông thường", r"Làm tròn xuống thì tổng điện nhỏ hơn nhu cầu; số tấm tối thiểu phải làm tròn lên."),
           (r"Chia nhu cầu cả tháng cho điện một tấm mỗi ngày", r"Hai đại lượng phải cùng một khoảng thời gian; tháng chia ngày ra số vô nghĩa.")]),
  buoc("Mái chỉ có 14 m²", "Mỗi tháng gia đình phải mua của lưới bao nhiêu kWh?", 55.8, "kWh", 0.5,
       loi=r"So với số tấm của câu b thay vì so với nhu cầu: hệ ở câu b đã dư điện.",
       ke=[(r"Tìm số tấm đặt vừa mái, điện các tấm đó cho mỗi ngày; lấy nhu cầu ngày trừ đi rồi nhân $30$", True),
           (r"Lấy số tấm còn thiếu so với câu b nhân điện một tấm, rồi nhân $30$", r"Hệ ở câu b cho dư điện, nên phần thiếu phải so với nhu cầu chứ không so với số tấm câu b."),
           (r"Lấy nhu cầu ngày trừ điện các tấm đặt vừa mái, không nhân thêm", r"Đó là phần thiếu trong một ngày; đề hỏi cả tháng.")]),
  buoc("Thời gian hoàn vốn", "Sau bao nhiêu năm thì hoàn vốn?", 5.36, "năm", 0.1,
       loi=r"Tính tiền tiết kiệm theo toàn bộ điện hệ pin phát ra; phần dư không bán nên không thành tiền.",
       ke=[(r"Tiền tiết kiệm mỗi tháng là tiền của $375\ \text{kWh}$; chia tiền lắp đặt cho số đó rồi đổi tháng ra năm", True),
           (r"Tính tiền tiết kiệm theo toàn bộ điện năng 9 tấm phát ra mỗi tháng", r"Phần điện dư không bán được nên không tiết kiệm thêm đồng nào."),
           (r"Chia tiền lắp đặt cho tiền điện một ngày rồi chia cho $12$", r"Thương đó là số ngày; đổi ngày ra năm phải chia cho $365$, không chia cho $12$.")]),
  buoc("Kiểm tra")]),
]


def kiem_so():
    # D1
    assert abs(H_D1 - 0.36288) < 1e-9 and round(H_D1 * 100, 1) == 36.3
    assert round(PNL / 1e6, 1) == 909.4 and round(PHP / 1e6, 1) == 579.4
    assert [round(x / 1e6, 2) for x in LOSS] == [90.94, 474.70, 13.75] and abs(sum(LOSS) - PHP) < 1
    assert round(MS, 2) == 33.68 and round(MS * 3600 / 1e3, 1) == 121.3 and round(THAN_NGAY) == 2910 and round(CO2_NGAY) == 7275
    assert abs(H_D1B - 0.3888) < 1e-9 and round(THAN_NGAY_B) == 2716 and round(TK_THAN) == 194 and A_D1_MWH == 7920
    # cách sai D1 cho số khác đáp án
    assert abs(PD1 * H_D1 / 1e6 - 909.4) > 100 and abs(PD1 / H3 / 1e6 - 909.4) > 100
    assert abs(PNL * (1 - H2) / 1e6 - 474.7) > 20 and abs(PD1 * (1 - H2) / 1e6 - 474.7) > 20
    assert abs(PD1 * NGAY / Q_THAN / 1e3 - 2910) > 100 and abs(PNL * 24 / Q_THAN / 1e3 - 2910) > 100
    assert abs(THAN_NGAY / K_THAN - 7275) > 100 and abs(THAN_NGAY - 7275) > 100
    assert abs(THAN_NGAY * 0.03 - 194) > 20
    assert abs(THAN_NGAY - THAN_NGAY * H_D1 / (H_D1 + 0.03) - 194) > 20
    assert abs((0.90 + 0.42 + 0.96) / 3 * 100 - 36.3) > 5
    # D2
    assert abs(H_D2 - 0.8832) < 1e-9 and PN_MUA == 237.5e6 and round(PD_MUA / 1e6, 2) == 209.76
    assert abs(PD_KHO / 1e6 - 113.05) < 0.001 and round(PD_KHO / PD_MUA, 3) == 0.539
    assert round(L_CAN, 1) == 212.3 and round(A_MUA_MWH) == 5034 and V_NGAY == 2.16e7
    assert abs(THAN_THAY - 1849.74) < 0.1 and abs(CO2_THAY - 4624.3) < 0.1
    assert abs(1e3 * 250 * 95 / 1e6 - 237.5) > 50                                     # dùng D thay d
    assert abs(0.92 * PN_MUA / 1e6 - 209.8) > 3 and abs((0.92 + 0.96) / 2 * PN_MUA / 1e6 - 209.8) > 3
    assert abs(H_D2 * 1e4 * 250 * 80 / 1e6 - 113.05) > 10 and abs(H_D2 * 1e4 * 160 * 95 / 1e6 - 113.05) > 10
    assert abs(150e6 / (1e4 * 80) - 212.3) > 5 and abs(150e6 * H_D2 / (1e4 * 80) - 212.3) > 5
    assert abs(PN_MUA * 24 / 1e6 - 5034) > 100 and abs(PD_MUA * NGAY / 1e6 - 5034) > 100
    assert abs(250 * 24 / 1e7 - 2.16) > 0.5 and abs(PD_MUA / (1e4 * 95) * NGAY / 1e7 - 2.16) > 0.1   # V sai
    assert round(CO2_THAY) == 4624 and abs(THAN_THAY / K_THAN - 4624) > 100 and abs(K_THAN * A_MUA_MWH - 4624) > 100
    assert abs(PNL / 1e6 - 909.4) < 8 and abs(PD1 / 0.36 / 1e6 - 909.4) < 8 and abs(PD1 * H_D1 / 1e6 - 909.4) > 8 and abs(PD1 / H3 / 1e6 - 909.4) > 8
    assert abs(0.88 * 1e4 * 160 * 80 / 1e6 - 113.05) < 0.6 and abs(H_D2 * 1e4 * 250 * 80 / 1e6 - 113.05) > 0.6 and abs(H_D2 * 1e4 * 160 * 95 / 1e6 - 113.05) > 0.6
    assert abs(A_MUA_J * H_D1 / Q_THAN / 1e3 - 1850) > 100 and abs(A_MUA_J / Q_THAN / 1e3 - 1850) > 100
    # D3
    assert A_NGAY3 == 12.5 and P_TAM == 400 and abs(A_TAM - 1.52) < 1e-9 and N_TAM == 9
    assert abs(A_NGAY3 / A_TAM - 8.2237) < 1e-3 and 8 * A_TAM < A_NGAY3 <= 9 * A_TAM
    assert N_MAI == 7 and abs(THIEU_THANG - 55.8) < 1e-6 and TK_THANG == 1050000 and abs(HV_NAM - 5.357) < 1e-3
    assert abs(67.5e6 / TK_THANG - 64.29) < 0.01
    assert abs(1000 * 2.0 - 400) > 10 and abs(0.2 * 1000 - 400) > 10
    assert abs(P_TAM * 12 * 0.95 / 1000 - 1.52) > 0.1 and abs(P_TAM * 4 / 1000 - 1.52) > 0.03
    assert round(A_NGAY3 / A_TAM) == 8 and abs(375 / A_TAM - 9) > 5                    # làm tròn thường; tháng/ngày
    assert abs((N_TAM - N_MAI) * A_TAM * 30 - 55.8) > 5 and abs((A_NGAY3 - N_MAI * A_TAM) - 55.8) > 5
    assert abs(67.5e6 / (N_TAM * A_TAM * 30 * 2800) / 12 - 5.36) > 0.3                  # tính cả điện dư
    assert abs(67.5e6 / (A_NGAY3 * 2800) / 12 - 5.36) > 10                               # số ngày chia 12
    assert abs(A_NGAY3 / (P_TAM * 12 * 0.95 / 1000) - 2.74) < 0.01                       # bẫy 12 h (nêu trong Kiểm tra)
    print("kiểm số liệu D1–D3 (bài 163): đạt")
