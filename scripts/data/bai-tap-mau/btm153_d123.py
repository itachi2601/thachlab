"""Bài tập mẫu CĐ12 "Nhiệt học nâng cao: cân bằng nhiệt và chuyển thể" (lesson 153) — Dạng 1–3. Module được build-hinh-153.py import.
Dàn ý + số liệu đã tính: content/hsg9/cd12-nhiet-hoc/nguon.md (mục "Bài tập mẫu", D1–D3 dùng nguyên số).
Quy ước: c_nước 4200, c_{\text{đ}}á 2100, nhôm 880, đồng 380 J/(kg·K); λ_{\text{đ}}á 3,4·10^5 J/kg. Đề luôn ghi "bỏ qua môi trường" và có/không tính bình.
Mọi đáp số tính lại bằng Python trong kiem_so(); mọi lựa chọn sai của chon_buoc_ke được assert cho số khác đáp án đúng."""
import math
from fractions import Fraction as Fr
from dung import *   # sol, buoc, M/P/A, fig, seg, lbl, poly, arrow, chevron, RED/BLUE/ORG/GRN

GREY = "#94a3b8"
ICE = "#a5f3fc"
TOPIC_CB = "Nhiệt độ và cân bằng nhiệt"
TOPIC_CT = "Nhiệt nóng chảy riêng và nhiệt hoá hơi riêng"
C_N, C_DA, C_AL, C_CU, LAM = 4200, 2100, 880, 380, 340000

# số liệu D1
M_AL, M_N1, T1, M_CU, T_CU = Fr(15, 100), Fr(4, 10), 20, Fr(5, 10), 120
C_TOA = M_CU * C_CU                       # 190 J/K
C_THU = M_N1 * C_N + M_AL * C_AL          # 1812 J/K
T_CB1 = (C_TOA * T_CU + C_THU * T1) / (C_TOA + C_THU)
T_QUEN = (C_TOA * T_CU + M_N1 * C_N * T1) / (C_TOA + M_N1 * C_N)
Q_BINH = M_AL * C_AL * (T_CB1 - T1)
# số liệu D2
M_N2, T_N2, M_DA, T_DA = 1, 30, Fr(3, 10), -10
Q_TOA_MAX = M_N2 * C_N * (T_N2 - 0)       # 126 000 J
Q1 = M_DA * C_DA * (0 - T_DA)             # 6300 J
Q2 = M_DA * LAM                           # 102 000 J
T_CB2 = (Q_TOA_MAX - Q1 - Q2) / ((M_N2 + M_DA) * C_N)
Q_TOA_B = (M_N2 + M_DA) * C_N * T_CB2     # 17 700 J
M_TAN = (Q_TOA_B - Q1) / LAM              # kg
M_CON = M_DA - M_TAN
# số liệu D3
P3, M3 = 200, Fr(1, 2)
MOC = [(0, 20), (2, 80), (7, 80), (9, 120)]   # (phút, °C)
C_RAN = P3 * 120 / (M3 * 60)
LAM3 = P3 * 300 / M3
C_LONG = P3 * 120 / (M3 * 40)


def anim(attr, vals, dur, kt=None):
    k = f' keyTimes="{kt}"' if kt else ""
    return f'<animate attributeName="{attr}" values="{vals}"{k} dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>'


def vn(x, nd=1):
    return f"{x:.{nd}f}".replace(".", ",")


# ═════════════ HÌNH ═════════════
def cup(x0, y0, x1, y1, lab=None):
    """Bình (thành + đáy), trả svg."""
    b = (f'<path d="M{x0},{y0} L{x0},{y1} L{x1},{y1} L{x1},{y0}" fill="none" stroke="currentColor" stroke-width="2.6"/>')
    if lab:
        b += lbl((x0 + x1) / 2, y1 + 18, lab, "currentColor", 14, "middle", "400")
    return b


# ───────────── Dạng 1 · nhiệt lượng kế + miếng đồng ─────────────
def d1(kk):
    b = ""
    if kk == 0:
        DUR = 6.0
        X0, X1, YT, YB = 70, 270, 74, 214           # nhiệt lượng kế (nhôm)
        WY = 128                                      # mặt nước
        b += f'<rect x="{X0 + 2}" y="{WY}" width="{X1 - X0 - 4}" height="{YB - WY - 2}" fill="{BLUE}" opacity="0.22" stroke="none"/>'
        b += seg(X0 + 2, WY, X1 - 2, WY, BLUE, 1.6)
        b += cup(X0, YT, X1, YB)
        b += lbl(X0 - 8, YB - 6, "nhôm", GREY, 14, "end", "700")
        b += lbl(X0 + 10, WY + 20, "nước", BLUE, 14, "start", "700")
        # miếng đồng rơi xuống rồi nguội dần (đỏ cam → nhạt)
        bx0, by0, by1 = 140, 24, 176
        b += (f'<rect x="{bx0}" y="{by0}" width="44" height="30" rx="3" fill="{ORG}" stroke="{ORG}" stroke-width="2" fill-opacity="0.9">'
              f'{anim("y", f"{by0};{by1};{by1}", DUR, "0;0.16;1")}'
              f'{anim("fill-opacity", "0.9;0.9;0.15", DUR, "0;0.16;1")}</rect>')
        b += (f'<text x="{bx0 + 52}" y="{by0 + 20}" fill="{ORG}" font-size="14" font-weight="700">đồng 120 °C'
              f'{anim("opacity", "1;0;0", DUR, "0;0.1;1")}</text>')
        # nhiệt kế cắm trong nước: chỉ ghi một mốc 20 °C (không có thang để đọc ra đáp số)
        TX, BULB = 236, 196
        b += f'<rect x="{TX - 6}" y="40" width="12" height="{BULB - 48}" rx="6" fill="none" stroke="currentColor" stroke-width="1.8"/>'
        b += f'<circle cx="{TX}" cy="{BULB}" r="9" fill="{RED}" stroke="currentColor" stroke-width="1.8"/>'
        PX = 3.2                                      # px mỗi °C (không ghi thang)
        y20 = 168
        K = 1.1
        ts = [i / 20 for i in range(21)]
        lv = []
        for s in ts:
            tau = max(0.0, (s - 0.16) / 0.84) * 5
            frac = (1 - math.exp(-tau / K)) / (1 - math.exp(-5 / K))
            lv.append(y20 - PX * float(T_CB1 - T1) * frac)
        b += (f'<rect x="{TX - 2.5}" y="{y20}" width="5" height="{BULB - y20}" fill="{RED}" stroke="none">'
              f'{anim("y", ";".join(f"{v:.1f}" for v in lv), DUR, ";".join(f"{s:.2f}" for s in ts))}'
              f'{anim("height", ";".join(f"{BULB - v:.1f}" for v in lv), DUR, ";".join(f"{s:.2f}" for s in ts))}</rect>')
        b += seg(TX + 6, y20, TX + 16, y20, "currentColor", 1.6) + seg(TX + 16, y20, X1 + 14, y20, GREY, 1.2, "3 3")
        b += lbl(X1 + 18, y20 + 4, "20 °C (lúc đầu)", "currentColor", 14, "start", "700")
        yf = lv[-1]
        b += (f'<g opacity="0">{anim("opacity", "0;0;1", DUR, "0;0.97;1")}'
              f'{seg(TX + 6, yf, X1 + 14, yf, GRN, 1.4, "3 3")}'
              f'<text x="{X1 + 18}" y="{yf + 4:.1f}" fill="{GRN}" font-size="15" font-weight="700">t = ?</text></g>')
        b += lbl(300, 60, "nhiệt kế", "currentColor", 14, "start", "400") + seg(296, 56, TX + 8, 60, GREY, 1.2)
        return fig("c12-1-0", "0 0 420 236",
                   "Nhiệt lượng kế nhôm chứa nước, miếng đồng nóng rơi vào, cột nhiệt kế dâng dần rồi dừng ở nhiệt độ cân bằng chưa biết",
                   b, "Mô phỏng chạy nhanh (quá trình thật kéo dài vài phút): miếng đồng nguội dần, cột nhiệt kế dâng rồi đứng yên khi cân bằng. "
                      "Nhiệt kế chỉ ghi mốc lúc đầu, không có thang để đọc.")
    # hình dữ kiện: ai toả, ai thu
    b += f'<rect x="20" y="20" width="150" height="62" rx="8" fill="none" stroke="{ORG}" stroke-width="2.2"/>'
    b += lbl(95, 42, "Miếng đồng", ORG, 15, "middle", "700") + lbl(95, 62, "0,5 kg · 120 °C → t", "currentColor", 14, "middle", "400")
    b += f'<rect x="250" y="12" width="156" height="56" rx="8" fill="none" stroke="{BLUE}" stroke-width="2.2"/>'
    b += lbl(328, 34, "Nước", BLUE, 15, "middle", "700") + lbl(328, 54, "0,4 kg · 20 °C → t", "currentColor", 14, "middle", "400")
    b += f'<rect x="250" y="86" width="156" height="56" rx="8" fill="none" stroke="{GREY}" stroke-width="2.2"/>'
    b += lbl(328, 108, "Bình nhôm", GREY, 15, "middle", "700") + lbl(328, 128, "0,15 kg · 20 °C → t", "currentColor", 14, "middle", "400")
    b += arrow("", "o", 170, 46, 246, 40, 2.4) + arrow("", "o", 170, 60, 246, 112, 2.4)
    b += lbl(200, 30, "toả", ORG, 14, "middle", "700") + lbl(190, 98, "toả", ORG, 14, "middle", "700")
    b += lbl(20, 118, "Vật toả: nhiệt độ giảm", "currentColor", 14, "start", "400")
    b += lbl(20, 138, "Vật thu: nhiệt độ tăng", "currentColor", 14, "start", "400")
    b += lbl(20, 166, "Cùng dừng ở một nhiệt độ t", GRN, 14, "start", "700")
    return fig("c12-1-2", "0 0 420 180", "Sơ đồ trao đổi nhiệt: miếng đồng toả nhiệt cho nước và cho bình nhôm, cả ba cùng tới nhiệt độ t",
               b, "Dữ kiện: hai vật thu nhiệt (nước và bình) cùng bắt đầu ở 20 °C.")


# ───────────── Dạng 2 · thả đá vào nước ─────────────
def cube(x, y, s, extra=""):
    return f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="3" fill="{ICE}" fill-opacity="0.55" stroke="{BLUE}" stroke-width="2">{extra}</rect>'


def d2(kk):
    b = ""
    if kk == 0:
        DUR = 4.0
        X0, X1, YT, YB, WY = 110, 310, 70, 214, 120
        b += f'<rect x="{X0 + 2}" y="{WY}" width="{X1 - X0 - 4}" height="{YB - WY - 2}" fill="{BLUE}" opacity="0.22" stroke="none"/>'
        b += seg(X0 + 2, WY, X1 - 2, WY, BLUE, 1.6) + cup(X0, YT, X1, YB)
        b += lbl(X0 - 8, WY + 22, "nước", BLUE, 14, "end", "700") + lbl(X0 - 8, WY + 40, "1 kg · 30 °C", "currentColor", 14, "end", "400")
        for i, cx in enumerate((150, 196, 242)):
            y0, y1 = 20 + 4 * i, 112 + 6 * i
            b += cube(cx, y0, 26, anim("y", f"{y0};{y1};{y1}", DUR, "0;0.25;1")
                      + anim("fill-opacity", "0.55;0.55;0.12", DUR, "0;0.6;1"))
        b += lbl(X1 + 8, 40, "đá 300 g", BLUE, 14, "start", "700") + lbl(X1 + 8, 58, "−10 °C", "currentColor", 14, "start", "400")
        # mũi tên nhiệt từ nước vào đá hiện dần
        b += (f'<g opacity="0">{anim("opacity", "0;0;1;1", DUR, "0;0.3;0.45;1")}'
              f'{arrow("", "o", 140, 196, 166, 158, 2.2)}{arrow("", "o", 300, 196, 270, 160, 2.2)}'
              f'{lbl(150, 208, "nhiệt", ORG, 14, "start", "700")}</g>')
        b += (f'<g opacity="0">{anim("opacity", "0;0;1", DUR, "0;0.96;1")}'
              f'<text x="210" y="100" fill="{GRN}" font-size="16" font-weight="700" text-anchor="middle">Tan hết hay còn đá ?</text></g>')
        return fig("c12-2-0", "0 0 420 236",
                   "Ba viên nước đá rơi vào bình nước, nước truyền nhiệt cho đá, mô phỏng dừng ở câu hỏi đá tan hết hay còn",
                   b, "Mô phỏng dừng trước trạng thái cuối: tan hết hay còn đá phải biện luận bằng nhiệt lượng, không đoán theo hình.")
    # hình dữ kiện: thang nhiệt độ, ba nhiệt lượng cần so (đều là ?)
    X, Y30, Y0, YM10 = 70, 30, 120, 150          # 3 px/°C
    b += seg(X, 18, X, 168, "currentColor", 1.8)
    for yy, s in ((Y30, "30 °C"), (Y0, "0 °C"), (YM10, "−10 °C")):
        b += seg(X - 5, yy, X + 5, yy, "currentColor", 1.6) + lbl(X - 9, yy + 4, s, "currentColor", 14, "end", "400")
    b += seg(X, Y0, 404, Y0, GREY, 1.2, "4 3")
    b += arrow("", "b", 120, Y30, 120, Y0 - 4, 2.4) + lbl(130, 66, "nước hạ về 0 °C", BLUE, 14, "start", "700")
    b += f'<text x="130" y="84" fill="{BLUE}" font-size="14" font-weight="400">toả tối đa Q<tspan dy="4" font-size="12">toả,max</tspan><tspan dy="-4"> = ?</tspan></text>'
    b += arrow("", "o", 120, YM10, 120, Y0 + 4, 2.4) + f'<text x="130" y="148" fill="{ORG}" font-size="14" font-weight="400">đá lên 0 °C: Q<tspan dy="4" font-size="12">1</tspan><tspan dy="-4"> = ?</tspan></text>'
    b += arrow("", "r", 130, 178, 250, 178, 2.4) + f'<text x="258" y="183" fill="{RED}" font-size="14" font-weight="400">Q<tspan dy="4" font-size="12">tan</tspan><tspan dy="-4"> = ?</tspan></text>'
    b += lbl(130, 168, "rồi tan hết ở 0 °C", RED, 14, "start", "700")
    b += f'<text x="16" y="212" fill="currentColor" font-size="14" font-weight="700">Đá tan hết cần Q<tspan dy="4" font-size="12">2</tspan><tspan dy="-4"> = Q</tspan><tspan dy="4" font-size="12">1</tspan><tspan dy="-4"> + Q</tspan><tspan dy="4" font-size="12">tan</tspan></text>'
    return fig("c12-2-2", "0 0 420 222", "Thang nhiệt độ: nước từ 30 độ hạ về 0 độ, đá từ âm 10 độ lên 0 độ rồi tan, ba nhiệt lượng chưa biết",
               b, "Dữ kiện: mốc so sánh là 0 °C. Tính ba nhiệt lượng rồi so trước khi viết phương trình. Hình không theo tỉ lệ nhiệt lượng.")


# ───────────── Dạng 3 · đồ thị T–t ─────────────
GX0, GY0, PXMIN, PXDEG = 62, 214, 36, 1.35


def gpt(tm, T):
    return GX0 + PXMIN * tm, GY0 - PXDEG * T


def d3(kk):
    b = ""
    if kk == 0:
        DUR = 9.0                                     # 1 s mô phỏng = 1 min thật
        b += seg(GX0, GY0, GX0 + PXMIN * 9.6, GY0, "currentColor", 1.8) + chevron(GX0 + PXMIN * 9.6, GY0, 1, 0, "currentColor", 1.8, 9)
        b += seg(GX0, GY0, GX0, 22, "currentColor", 1.8) + chevron(GX0, 22, 0, -1, "currentColor", 1.8, 9)
        b += lbl(GX0 + PXMIN * 9.6, GY0 + 38, "τ (min)", "currentColor", 14, "end", "400")
        b += lbl(GX0 + 8, 26, "t (°C)", "currentColor", 14, "start", "400")
        pts = [gpt(*p) for p in MOC]
        for tm in (2, 7, 9):
            x, _ = gpt(tm, 0)
            yv = gpt(tm, dict(MOC)[tm])[1]
            b += seg(x, yv, x, GY0, GREY, 1.1, "4 3")
        for tm in (0, 2, 7, 9):
            b += lbl(gpt(tm, 0)[0], GY0 + 18, str(tm), "currentColor", 14, "middle", "400")
        for T in (20, 80, 120):
            y = gpt(0, T)[1]
            xe = gpt({20: 0, 80: 2, 120: 9}[T], 0)[0]
            if T != 20:
                b += seg(GX0, y, xe, y, GREY, 1.1, "4 3")
            b += lbl(GX0 - 6, y + 4, str(T), "currentColor", 14, "end", "400")
        for (x, y), s in zip(pts, "ABCD"):
            b += lbl(*{"A": (x + 8, y + 14, s, "currentColor", 15, "start", "700"), "C": (x - 4, y - 8, s, "currentColor", 15, "end", "700")}.get(s, (x + 6, y - 8, s, "currentColor", 15, "start", "700")))
        cum = [0.0]
        for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
            cum.append(cum[-1] + math.hypot(xb - xa, yb - ya))
        L = cum[-1]
        kt = ";".join(f"{tm / 9:.4f}" for tm, _ in MOC)
        line = poly(pts, RED, 2.8).replace("/>", f' stroke-dasharray="{L + 2:.1f}" stroke-dashoffset="0">'
                                           f'{anim("stroke-dashoffset", ";".join(f"{L - c:.1f}" for c in cum), DUR, kt)}</polyline>')
        b += line
        b += (f'<circle cx="{pts[0][0]:.1f}" cy="{pts[0][1]:.1f}" r="5.5" fill="{GRN}" stroke="currentColor" stroke-width="1.5">'
              f'{anim("cx", ";".join(f"{x:.1f}" for x, _ in pts), DUR, kt)}{anim("cy", ";".join(f"{y:.1f}" for _, y in pts), DUR, kt)}</circle>')
        b += lbl(150, 168, "nguồn cấp đều 200 W", ORG, 14, "start", "700") + lbl(150, 150, "chất: 0,5 kg", "currentColor", 14, "start", "400")
        return fig("c12-3-0", "0 0 420 258",
                   "Đồ thị nhiệt độ theo thời gian đun: A 0 phút 20 độ, B 2 phút 80 độ, C 7 phút 80 độ, D 9 phút 120 độ",
                   b, "Mô phỏng: chấm chạy dọc đồ thị, chạy nhanh 60 lần (1 s mô phỏng = 1 min thật). Trục chỉ ghi các mốc đề cho.")
    # hình mẫu cách đọc (không theo số của đề)
    x0, y0 = 40, 150
    sp = [(x0, y0), (x0 + 90, 70), (x0 + 220, 70), (x0 + 330, 22)]
    b += seg(x0, y0, x0 + 350, y0, "currentColor", 1.6) + seg(x0, y0, x0, 14, "currentColor", 1.6) + poly(sp, GRN, 2.4)
    b += lbl(x0 + 46, 124, "đoạn dốc:", BLUE, 14, "start", "700") + lbl(x0 + 46, 140, "nhiệt độ thay đổi", "currentColor", 14, "start", "400")
    b += lbl((sp[1][0] + sp[2][0]) / 2 - 20, 60, "đoạn ngang: nhiệt độ không đổi", RED, 14, "middle", "700")
    b += lbl((sp[1][0] + sp[2][0]) / 2, 96, "chất vẫn đang nhận nhiệt", "currentColor", 14, "middle", "400")
    b += lbl(16, 174, "Mỗi đoạn: Δτ trên trục ngang, Δt trên trục đứng", "currentColor", 14, "start", "400")
    return fig("c12-3-2", "0 0 420 186", "Đồ thị mẫu gồm đoạn dốc và đoạn nằm ngang, nhắc cách đọc thời gian và độ tăng nhiệt độ của từng đoạn",
               b, "Hình mẫu cách đọc đồ thị (không theo số liệu của đề).")


BUILD = [d1, d2, d3]

# ═════════════ ĐỀ ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Cân bằng nhiệt có kể nhiệt lượng kế: nhiệt độ cân bằng và sai lệch khi quên bình",
      topic=TOPIC_CB,
      problem_html=r"""<p>Một nhiệt lượng kế bằng nhôm khối lượng $150\ \text{g}$ chứa $400\ \text{g}$ nước; nhiệt lượng kế và nước cùng ở $20\ ^{\circ}\text{C}$. Thả vào nước một miếng đồng khối lượng $500\ \text{g}$ đã nung tới $120\ ^{\circ}\text{C}$. Bỏ qua sự trao đổi nhiệt với môi trường; nhiệt lượng kế có tham gia trao đổi nhiệt. Nhiệt dung riêng của nước, nhôm, đồng lần lượt là $4200$; $880$; $380\ \text{J/(kg·K)}$.</p><ol type="a"><li>Tìm nhiệt độ của hệ khi có cân bằng nhiệt.</li><li>Nhiệt lượng kế đã thu vào bao nhiêu nhiệt lượng?</li><li>Một bạn quên nhiệt lượng kế khi lập phương trình cân bằng nhiệt. Bạn đó tính ra nhiệt độ cân bằng bằng bao nhiêu, lệch bao nhiêu so với câu a?</li></ol>"""),
 dict(label="Dạng 2 · Trung bình · Biện luận chuyển thể: thả nước đá vào nước, đá tan hết hay chỉ tan một phần",
      topic=TOPIC_CT,
      problem_html=r"""<p>Một bình cách nhiệt chứa $1\ \text{kg}$ nước ở $30\ ^{\circ}\text{C}$. Bỏ qua nhiệt dung của bình và sự trao đổi nhiệt với môi trường. Nhiệt dung riêng của nước là $4200\ \text{J/(kg·K)}$, của nước đá là $2100\ \text{J/(kg·K)}$; nhiệt nóng chảy riêng của nước đá là $\lambda=3{,}4\cdot10^5\ \text{J/kg}$.</p><ol type="a"><li>Thả vào bình $300\ \text{g}$ nước đá ở $-10\ ^{\circ}\text{C}$. Đá có tan hết không? Tìm nhiệt độ của bình khi cân bằng nhiệt.</li><li>Khi đã cân bằng, thả tiếp vào bình $300\ \text{g}$ nước đá ở $-10\ ^{\circ}\text{C}$. Tìm nhiệt độ cuối cùng của bình và khối lượng nước đá còn lại.</li></ol>"""),
 dict(label="Dạng 3 · Trung bình · Đọc đồ thị nhiệt độ – thời gian đun: nhiệt dung riêng và nhiệt nóng chảy riêng",
      topic=TOPIC_CT,
      problem_html=r"""<p>Một nguồn nhiệt cung cấp đều đặn cho $0{,}5\ \text{kg}$ một chất rắn, mỗi giây chất nhận được $200\ \text{J}$ (công suất có ích $200\ \text{W}$; bỏ qua nhiệt lượng hao phí ra môi trường). Đồ thị nhiệt độ $t$ của chất theo thời gian đun $\tau$ như hình dưới, các mốc ghi trên trục.</p><ol type="a"><li>Trên đoạn nào chất đang nóng chảy? Nhiệt độ nóng chảy của chất là bao nhiêu?</li><li>Tính nhiệt dung riêng của chất ở thể rắn.</li><li>Tính nhiệt nóng chảy riêng $\lambda$ của chất.</li><li>Tính nhiệt dung riêng của chất ở thể lỏng.</li></ol>"""),
]

# ═════════════ BẢNG PHÂN TÍCH ĐỀ ═════════════
ANALYSIS = [
 # Dạng 1
 [(r'"nhiệt lượng kế bằng nhôm khối lượng $150\ \text{g}$ chứa $400\ \text{g}$ nước; … cùng ở $20\ ^{\circ}\text{C}$"',
   r"$m_b=0{,}15\ \text{kg}$; $m_n=0{,}4\ \text{kg}$; $t_1=20\ ^{\circ}\text{C}$",
   r"Bình và nước cùng nhiệt độ đầu, cùng nóng lên tới $t$<br>Cả hai là vật thu nhiệt"),
  (r'"miếng đồng khối lượng $500\ \text{g}$ đã nung tới $120\ ^{\circ}\text{C}$"', r"$m_{\text{đ}}=0{,}5\ \text{kg}$; $t_2=120\ ^{\circ}\text{C}$",
   r"Vật nóng toả nhiệt: $Q=mc\,(t_2-t)$"),
  (r'"Bỏ qua sự trao đổi nhiệt với môi trường; nhiệt lượng kế có tham gia trao đổi nhiệt"', r"Hệ kín gồm đồng, nước, bình",
   r"⚠ chỉ khi bỏ qua môi trường mới có $Q_{\text{toả}}=Q_{\text{thu}}$<br>⚠ phía thu phải kể cả bình"),
  (r'"Nhiệt dung riêng … $4200$; $880$; $380\ \text{J/(kg·K)}$"', r"$c_n$; $c_b$; $c_{\text{đ}}$",
   r"Nhiệt dung của vật $C=mc$<br>Đổi g ra kg trước khi nhân"),
  (r'"Tìm nhiệt độ của hệ khi có cân bằng nhiệt"', r"Cần $t$", r"$Q_{\text{toả}}=Q_{\text{thu}}$<br>$t$ phải nằm giữa $20$ và $120\ ^{\circ}\text{C}$"),
  (r'"Nhiệt lượng kế đã thu vào bao nhiêu"', r"Cần $Q_b$", r"$Q_b=m_b c_b\,(t-t_1)$"),
  (r'"quên nhiệt lượng kế khi lập phương trình"', r"Cần $t'$ và $t'-t$", r"Phương trình mất số hạng nào?")],
 # Dạng 2
 [(r'"bình cách nhiệt … Bỏ qua nhiệt dung của bình và sự trao đổi nhiệt với môi trường"', r"Chỉ có nước và đá trao đổi nhiệt",
   r"⚠ $Q_{\text{toả}}=Q_{\text{thu}}$ chỉ gồm nước và đá"),
  (r'"$1\ \text{kg}$ nước ở $30\ ^{\circ}\text{C}$"', r"$m_n=1\ \text{kg}$; $t_n=30\ ^{\circ}\text{C}$",
   r"Nếu nước hạ hẳn về $0\ ^{\circ}\text{C}$ thì toả ra nhiều nhất bao nhiêu?"),
  (r'"$300\ \text{g}$ nước đá ở $-10\ ^{\circ}\text{C}$"', r"$m_{\text{đ}}=0{,}3\ \text{kg}$; $t_{\text{đ}}=-10\ ^{\circ}\text{C}$",
   r"Đá nóng lên tới $0\ ^{\circ}\text{C}$: $Q_1=m_{\text{đ}} c_{\text{đ}}\cdot10$<br>Rồi mới tan ở $0\ ^{\circ}\text{C}$: $Q_{\text{tan}}=\lambda m_{\text{đ}}$<br>Tan hết cần $Q_2=Q_1+Q_{\text{tan}}$"),
  (r'"Đá có tan hết không?"', r"Chưa biết trạng thái cuối",
   r"⚠ chưa biết đá tan hết hay không thì chưa viết được phương trình<br>So $Q_{\text{toả,max}}$ với $Q_1$ và với $Q_2$"),
  (r'"Tìm nhiệt độ của bình khi cân bằng"', r"Cần $t$", r"Nếu đá tan hết: nước do đá tan ra cũng phải nóng lên từ $0\ ^{\circ}\text{C}$"),
  (r'"thả tiếp vào bình $300\ \text{g}$ nước đá ở $-10\ ^{\circ}\text{C}$"', r"Nước lúc này: lượng và nhiệt độ của câu a",
   r"Biện luận lại từ đầu với lượng nước mới"),
  (r'"khối lượng nước đá còn lại"', r"Cần $m_{\text{còn}}$", r"Đá tan được bao nhiêu? Lượng còn lại tính từ khối đá nào?")],
 # Dạng 3
 [(r'"mỗi giây chất nhận được $200\ \text{J}$ (… bỏ qua nhiệt lượng hao phí ra môi trường)"', r"$P=200\ \text{W}$",
   r"⚠ bỏ qua hao phí: toàn bộ nhiệt nguồn cấp đều vào chất<br>Nhiệt nhận được $Q=P\,\Delta\tau$, $\Delta\tau$ tính bằng giây"),
  (r'"$0{,}5\ \text{kg}$ một chất rắn"', r"$m=0{,}5\ \text{kg}$", r"Khối lượng không đổi trong suốt quá trình"),
  (r'"Trên đoạn nào chất đang nóng chảy?"', r"Ba đoạn AB, BC, CD", r"Đoạn nào nhiệt độ không đổi dù chất vẫn nhận nhiệt?"),
  (r'"nhiệt dung riêng của chất ở thể rắn"', r"Cần $c_r$", r"$Q=mc\,\Delta t$ trên đoạn chất còn rắn"),
  (r'"nhiệt nóng chảy riêng $\lambda$"', r"Cần $\lambda$", r"$Q=\lambda m$ trên đoạn chuyển thể"),
  (r'"nhiệt dung riêng của chất ở thể lỏng"', r"Cần $c_l$", r"Đoạn nào chất đã lỏng hoàn toàn? Đọc $\Delta\tau$ và $\Delta t$ của đoạn đó")],
]

# ═════════════ LỜI GIẢI ═════════════
R1 = [r"<strong>Khái niệm:</strong> nhiệt truyền từ vật nóng hơn sang vật lạnh hơn tới khi nhiệt độ bằng nhau.",
      r"<strong>Định luật:</strong> phương trình cân bằng nhiệt $Q_{\text{toả}}=Q_{\text{thu}}$.",
      r"<strong>Công thức:</strong> $Q=mc\,\Delta t$; nhiệt dung của vật $C=mc$.",
      r"<strong>Điều kiện:</strong> bỏ qua trao đổi nhiệt với môi trường; kể đủ mọi vật thu nhiệt, kể cả bình."]
R2 = [r"<strong>Khái niệm:</strong> nước đá ở dưới $0\ ^{\circ}\text{C}$ phải nóng lên tới $0\ ^{\circ}\text{C}$ rồi mới tan; trong lúc tan nhiệt độ giữ ở $0\ ^{\circ}\text{C}$.",
      r"<strong>Công thức:</strong> $Q=mc\,\Delta t$ (một thể); $Q=\lambda m$ (nóng chảy); đá tan hết cần $Q_2=Q_1+Q_{\text{tan}}$, với $Q_1$ đưa đá lên $0\ ^{\circ}\text{C}$, $Q_{\text{tan}}=\lambda m_{\text{đ}}$.",
      r"<strong>Biện luận:</strong> so nhiệt nước toả tối đa khi về $0\ ^{\circ}\text{C}$ với nhiệt đưa đá lên $0\ ^{\circ}\text{C}$ và nhiệt làm tan hết đá.",
      r"<strong>Điều kiện:</strong> bỏ qua nhiệt dung bình và môi trường: $Q_{\text{toả}}=Q_{\text{thu}}$ chỉ gồm nước và đá."]
R3 = [r"<strong>Khái niệm:</strong> trong lúc nóng chảy nhiệt độ không đổi dù chất vẫn nhận nhiệt.",
      r"<strong>Công thức:</strong> nhiệt nhận được $Q=P\,\Delta\tau$.",
      r"<strong>Đoạn dốc:</strong> $P\,\Delta\tau=mc\,\Delta t$; <strong>đoạn ngang:</strong> $P\,\Delta\tau=\lambda m$.",
      r"<strong>Điều kiện:</strong> bỏ qua hao phí, $\Delta\tau$ đổi ra giây."]

SOLS = [
 sol(R1, [
  ("Nhiệt dung của từng vật", [P(r"Đổi ra kg rồi tính $C=mc$:"),
     M(r"C_{\text{đ}}=0{,}5\cdot380=190\ \text{J/K}"), M(r"C_n=0{,}4\cdot4200=1680\ \text{J/K}"), M(r"C_b=0{,}15\cdot880=132\ \text{J/K}"),
     A(r"C_{\text{thu}}=C_n+C_b=1812\ \text{J/K}")]),
  ("Phương trình cân bằng nhiệt", [P(r"Đồng toả nhiệt; nước và bình thu nhiệt:"),
     M(r"C_{\text{đ}}\,(120-t)=C_{\text{thu}}\,(t-20)"), M(r"190\,(120-t)=1812\,(t-20)"),
     M(r"t=\dfrac{190\cdot120+1812\cdot20}{190+1812}=\dfrac{59\,040}{2002}"), A(r"t\approx29{,}5\ ^{\circ}\text{C}")]),
  ("Nhiệt lượng bình nhôm thu", [P(r"Bình nóng lên từ $20\ ^{\circ}\text{C}$ tới $t\approx29{,}49\ ^{\circ}\text{C}$:"),
     M(r"Q_b=m_b c_b\,(t-20)=132\cdot(29{,}49-20)"), A(r"Q_b\approx1253\ \text{J}")]),
  ("Nếu quên nhiệt lượng kế", [P(r"Phương trình mất số hạng của bình:"),
     M(r"190\,(120-t')=1680\,(t'-20)"), M(r"t'=\dfrac{190\cdot120+1680\cdot20}{190+1680}=\dfrac{56\,400}{1870}"), A(r"t'\approx30{,}2\ ^{\circ}\text{C}"),
     P(r"Lệch $t'-t\approx0{,}7\ ^{\circ}\text{C}$: quên bình thì phía thu ít đi, tính ra nhiệt độ cao hơn thật.")]),
  ("Kiểm tra", [P(r"$20\ ^{\circ}\text{C}\lt t\lt120\ ^{\circ}\text{C}$ ✓; $t$ gần $20\ ^{\circ}\text{C}$ vì nhiệt dung phía thu ($1812\ \text{J/K}$) lớn gấp gần $10$ lần của đồng ✓."),
     P(r"Nhiệt đồng toả $190\cdot(120-29{,}49)\approx17\,197\ \text{J}$; nhiệt nước và bình thu $1812\cdot(29{,}49-20)\approx17\,197\ \text{J}$ ✓."),
     P(r"Đơn vị: $\text{kg}\cdot\dfrac{\text{J}}{\text{kg·K}}\cdot\text{K}=\text{J}$ ✓.")])],
  [r"a) $t\approx29{,}5\ ^{\circ}\text{C}$", r"b) $Q_b\approx1253\ \text{J}$ (khoảng $1{,}25\ \text{kJ}$)", r"c) $t'\approx30{,}2\ ^{\circ}\text{C}$, lệch khoảng $0{,}7\ ^{\circ}\text{C}$"],
  r"Nhận dạng: thấy <strong>nhiệt lượng kế, thả vật nóng vào</strong> → $Q_{\text{toả}}=Q_{\text{thu}}$, phía thu kể cả bình."),
 sol(R2, [
  ("Nhiệt nước toả tối đa", [P(r"Giả sử nước hạ hẳn về $0\ ^{\circ}\text{C}$:"), M(r"Q_{\text{toả,max}}=m_n c_n\,(30-0)=1\cdot4200\cdot30"), A(r"Q_{\text{toả,max}}=126\,000\ \text{J}")]),
  ("Nhiệt cần để đá tan hết", [M(r"Q_1=m_{\text{đ}} c_{\text{đ}}\,(0-(-10))=0{,}3\cdot2100\cdot10=6300\ \text{J}"), M(r"Q_{\text{tan}}=\lambda m_{\text{đ}}=3{,}4\cdot10^5\cdot0{,}3=102\,000\ \text{J}"),
     A(r"Q_2=Q_1+Q_{\text{tan}}=108\,300\ \text{J}")]),
  ("Biện luận câu a", [P(r"$Q_{\text{toả,max}}=126\,000\ \text{J}\gt Q_2=108\,300\ \text{J}$: nước còn dư nhiệt sau khi làm tan hết đá."),
     P(r"Kết luận: <strong>đá tan hết</strong>, nhiệt độ cân bằng $t\gt0\ ^{\circ}\text{C}$. Lúc này mới viết phương trình.")]),
  ("Nhiệt độ cân bằng câu a", [P(r"Nước ban đầu toả từ $30\ ^{\circ}\text{C}$ xuống $t$; đá lên $0\ ^{\circ}\text{C}$, tan, rồi nước do đá tan nóng lên tới $t$:"),
     M(r"1\cdot4200\,(30-t)=6300+102\,000+0{,}3\cdot4200\,t"), M(r"t=\dfrac{126\,000-108\,300}{1{,}3\cdot4200}=\dfrac{17\,700}{5460}"), A(r"t\approx3{,}24\ ^{\circ}\text{C}")]),
  ("Biện luận câu b", [P(r"Trong bình có $1{,}3\ \text{kg}$ nước ở $t\approx3{,}24\ ^{\circ}\text{C}$. Hạ về $0\ ^{\circ}\text{C}$, nước toả tối đa:"),
     M(r"Q'_{\text{toả,max}}=1{,}3\cdot4200\cdot3{,}24\approx17\,700\ \text{J}"),
     P(r"Đưa $300\ \text{g}$ đá mới lên $0\ ^{\circ}\text{C}$ cần $Q_1=6300\ \text{J}$; làm tan hết cần $108\,300\ \text{J}$."),
     P(r"$6300\ \text{J}\lt17\,700\ \text{J}\lt108\,300\ \text{J}$: đá lên được $0\ ^{\circ}\text{C}$ nhưng chỉ <strong>tan một phần</strong>, nhiệt độ cuối $t''=0\ ^{\circ}\text{C}$.")]),
  ("Khối lượng đá tan", [P(r"Nhiệt còn lại sau khi đưa đá lên $0\ ^{\circ}\text{C}$ dùng để làm tan $\Delta m$ đá:"),
     M(r"\lambda\,\Delta m=Q'_{\text{toả,max}}-Q_1=17\,700-6300=11\,400\ \text{J}"), M(r"\Delta m=\dfrac{11\,400}{3{,}4\cdot10^5}\ \text{kg}"), A(r"\Delta m\approx33{,}5\ \text{g}")]),
  ("Khối lượng đá còn lại", [P(r"Đá của câu a đã tan hết, chỉ còn đá của lần thả sau:"), M(r"m_{\text{còn}}=300-33{,}5"), A(r"m_{\text{còn}}\approx266{,}5\ \text{g}")]),
  ("Kiểm tra", [P(r"Câu a: $0\lt3{,}24\lt30\ ^{\circ}\text{C}$ ✓."),
     P(r"Câu b: nếu giả sử ngay $t''\gt0\ ^{\circ}\text{C}$ rồi giải phương trình sẽ ra $t''$ âm, vô lí; đó là lí do phải biện luận trước."),
     P(r"Nếu nước toả tối đa còn nhỏ hơn $Q_1$ thì đá chưa lên tới $0\ ^{\circ}\text{C}$ và một phần nước sẽ đông lại: khả năng này không xảy ra ở đây ✓.")])],
  [r"a) Đá tan hết; $t\approx3{,}24\ ^{\circ}\text{C}$", r"b) $t''=0\ ^{\circ}\text{C}$; còn khoảng $266{,}5\ \text{g}$ nước đá"],
  r"Nhận dạng: thấy <strong>thả nước đá vào nước</strong> → tính $Q_{\text{toả,max}}$ về $0\ ^{\circ}\text{C}$, so với $Q_1$, $Q_2$ rồi mới viết phương trình."),
 sol(R3, [
  ("Đoạn nóng chảy", [P(r"Trên đoạn BC (từ phút $2$ tới phút $7$) chất vẫn nhận nhiệt nhưng nhiệt độ không đổi: đó là lúc nóng chảy."),
     A(r"\text{BC},\ t_{\text{nc}}=80\ ^{\circ}\text{C}")]),
  ("Nhiệt nhận được trên đoạn AB", [P(r"Đoạn AB kéo dài $2\ \text{min}=120\ \text{s}$:"), M(r"Q_{AB}=P\,\Delta\tau=200\cdot120"), A(r"Q_{AB}=24\,000\ \text{J}")]),
  ("Nhiệt dung riêng thể rắn", [P(r"Trên AB chất còn rắn, nóng từ $20$ lên $80\ ^{\circ}\text{C}$: $\Delta t=60\ ^{\circ}\text{C}$."),
     M(r"c_r=\dfrac{Q_{AB}}{m\,\Delta t}=\dfrac{24\,000}{0{,}5\cdot60}"), A(r"c_r=800\ \text{J/(kg·K)}")]),
  ("Nhiệt nóng chảy riêng", [P(r"Đoạn BC kéo dài $7-2=5\ \text{min}=300\ \text{s}$:"),
     M(r"\lambda=\dfrac{P\,\Delta\tau}{m}=\dfrac{200\cdot300}{0{,}5}"), A(r"\lambda=1{,}2\cdot10^5\ \text{J/kg}=120\ \text{kJ/kg}")]),
  ("Nhiệt dung riêng thể lỏng", [P(r"Trên CD chất đã lỏng hoàn toàn: $\Delta\tau=9-7=2\ \text{min}=120\ \text{s}$; $\Delta t=120-80=40\ ^{\circ}\text{C}$."),
     M(r"c_l=\dfrac{P\,\Delta\tau}{m\,\Delta t}=\dfrac{200\cdot120}{0{,}5\cdot40}"), A(r"c_l=1200\ \text{J/(kg·K)}")]),
  ("Kiểm tra", [P(r"AB và CD cùng kéo dài $2\ \text{min}$ (cùng nhiệt lượng) nhưng CD tăng ít độ hơn ($40$ so với $60\ ^{\circ}\text{C}$): nhiệt dung riêng thể lỏng phải lớn hơn ✓, đúng tỉ lệ $\dfrac{c_l}{c_r}=\dfrac{60}{40}=1{,}5$ ✓."),
     P(r"Đơn vị: $\dfrac{\text{W}\cdot\text{s}}{\text{kg}}=\dfrac{\text{J}}{\text{kg}}$ ✓.")])],
  [r"a) Đoạn BC; $t_{\text{nc}}=80\ ^{\circ}\text{C}$", r"b) $c_r=800\ \text{J/(kg·K)}$", r"c) $\lambda=1{,}2\cdot10^5\ \text{J/kg}$", r"d) $c_l=1200\ \text{J/(kg·K)}$"],
  r"Nhận dạng: thấy <strong>đồ thị nhiệt độ theo thời gian đun có đoạn nằm ngang</strong> → đoạn ngang: $P\Delta\tau=\lambda m$; đoạn dốc: $P\Delta\tau=mc\Delta t$."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC ═════════════
STEPS = [
 # ── Dạng 1 ──
 dict(nhan_dang=r"Thấy <b>nhiệt lượng kế, thả vật nóng vào</b> → $Q_{\text{toả}}=Q_{\text{thu}}$, phía thu kể cả bình.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Nhiệt dung của từng vật", "Tổng nhiệt dung của nước và nhiệt lượng kế là bao nhiêu J/K?", 1812, "J/K", 2,
       loi=r"Để khối lượng theo gam khi nhân với nhiệt dung riêng, hoặc chỉ tính riêng nước mà bỏ bình."),
  buoc("Phương trình cân bằng nhiệt", "Nhiệt độ cân bằng là bao nhiêu °C?", 29.5, "°C", 0.1,
       loi=r"Lấy trung bình cộng của hai nhiệt độ đầu; trung bình cộng chỉ đúng khi hai bên có nhiệt dung bằng nhau.",
       ke=[(r"Viết $190\,(120-t)=1812\,(t-20)$ rồi giải tìm $t$", True),
           (r"Lấy $t=\dfrac{120+20}{2}$", r"Nhiệt dung hai phía chênh nhau gần $10$ lần, nên $t$ không phải trung bình cộng."),
           (r"Lấy trung bình theo khối lượng $t=\dfrac{0{,}5\cdot120+0{,}4\cdot20}{0{,}5+0{,}4}$", r"Các vật khác chất nên phải dùng nhiệt dung $mc$, khối lượng thôi chưa đủ; cách này còn bỏ sót bình.")]),
  buoc("Nhiệt lượng bình nhôm thu", "Nhiệt lượng kế đã thu vào bao nhiêu jun?", 1253, "J", 15,
       loi=r"Nhân với nhiệt độ cân bằng thay vì độ tăng nhiệt độ của bình.",
       ke=[(r"Tính $Q_b=m_b c_b\,(t-20)$", True),
           (r"Tính $Q_b=m_b c_b\,t$", r"Nhiệt lượng tính theo độ tăng nhiệt độ $t-20$, không theo nhiệt độ cuối."),
           (r"Tính $Q_b=m_b c_b\,(120-t)$", r"$120\ ^{\circ}\text{C}$ là nhiệt độ đầu của đồng; bình bắt đầu ở $20\ ^{\circ}\text{C}$ cùng nước.")]),
  buoc("Nếu quên nhiệt lượng kế", "Bạn quên bình tính ra nhiệt độ cân bằng bao nhiêu °C?", 30.2, "°C", 0.1,
       loi=r"Bỏ số hạng của bình nhưng vẫn giữ tổng nhiệt dung cũ ở mẫu số.",
       ke=[(r"Bỏ số hạng của bình: $190\,(120-t')=1680\,(t'-20)$", True),
           (r"Giữ nguyên kết quả câu a vì bình chỉ để đựng nước", r"Bình nóng lên cùng nước nên cũng thu nhiệt; bỏ nó thì phương trình thay đổi."),
           (r"Chuyển nhiệt dung của bình sang phía toả", r"Bình bắt đầu ở $20\ ^{\circ}\text{C}$ và nóng lên, nó thu nhiệt chứ không toả.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 2 ──
 dict(nhan_dang=r"Thấy <b>thả nước đá vào nước</b> → biện luận đá tan hết hay không trước, rồi mới viết phương trình.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Nhiệt nước toả tối đa", "Nếu nước hạ hẳn về 0 °C thì toả ra bao nhiêu jun?", 126000, "J", 500,
       loi=r"Lấy độ giảm nhiệt độ của nước tới tận nhiệt độ của đá; trong phép thử này nước chỉ hạ về $0\ ^{\circ}\text{C}$, mốc chuyển thể."),
  buoc("Nhiệt cần để đá tan hết", "Đưa đá lên 0 °C rồi làm tan hết cần tổng cộng Q₂ bao nhiêu jun?", 108300, "J", 300,
       loi=r"Chỉ tính nhiệt làm tan $\lambda m$, quên đá phải nóng lên tới $0\ ^{\circ}\text{C}$ trước.",
       ke=[(r"Cộng $Q_1=m_{\text{đ}} c_{\text{đ}}\cdot10$ (đá lên $0\ ^{\circ}\text{C}$) với $Q_{\text{tan}}=\lambda m_{\text{đ}}$ (tan hết)", True),
           (r"Chỉ tính $Q_{\text{tan}}=\lambda m_{\text{đ}}$", r"Đá đang ở $-10\ ^{\circ}\text{C}$, phải nhận nhiệt để lên $0\ ^{\circ}\text{C}$ rồi mới bắt đầu tan."),
           (r"Tính $Q_1$ với nhiệt dung riêng của nước rồi cộng $Q_{\text{tan}}$", r"Lúc nóng từ $-10$ lên $0\ ^{\circ}\text{C}$ chất vẫn là nước đá, phải dùng $c_{\text{đ}}=2100\ \text{J/(kg·K)}$.")]),
  buoc("Biện luận câu a", "Kết luận nào đúng về trạng thái cuối ở câu a?",
       lua_chon=[(r"Đá tan hết, nhiệt độ cân bằng lớn hơn $0\ ^{\circ}\text{C}$", True),
                 (r"Đá chỉ tan một phần, nhiệt độ cân bằng là $0\ ^{\circ}\text{C}$", r"Nhiệt nước toả khi về $0\ ^{\circ}\text{C}$ lớn hơn nhiệt cần để tan hết đá, nên còn dư nhiệt."),
                 (r"Chưa kết luận được, cứ giả sử nhiệt độ cuối trên $0\ ^{\circ}\text{C}$ rồi giải", r"Hai nhiệt lượng vừa tính đã đủ để kết luận; giả sử trước dễ ra nhiệt độ âm vô lí.")],
       loi=r"Bỏ qua bước so sánh, viết ngay phương trình với nhiệt độ cuối trên $0\ ^{\circ}\text{C}$.",
       ke=[(r"So nhiệt nước toả tối đa với nhiệt cần để đá tan hết", True),
           (r"Viết ngay phương trình $Q_{\text{toả}}=Q_{\text{thu}}$ với $t\gt0\ ^{\circ}\text{C}$", r"Chưa biết đá tan hết hay không; nếu đá chỉ tan một phần, phương trình đó sai và cho nhiệt độ âm."),
           (r"So khối lượng đá với khối lượng nước", r"Đá tan hết hay không phụ thuộc nhiệt lượng, không phụ thuộc riêng khối lượng.")]),
  buoc("Nhiệt độ cân bằng câu a", "Nhiệt độ cân bằng ở câu a là bao nhiêu °C?", 3.24, "°C", 0.06,
       loi=r"Chia phần nhiệt dư cho riêng khối lượng nước ban đầu, quên nước do đá tan ra cũng phải nóng lên từ $0\ ^{\circ}\text{C}$.",
       ke=[(r"Phần nhiệt dư làm nóng toàn bộ nước trong bình (nước cũ và nước do đá tan) từ $0\ ^{\circ}\text{C}$", True),
           (r"Chia phần nhiệt dư cho nhiệt dung của $1\ \text{kg}$ nước ban đầu", r"Nước do đá tan ra cũng ở trong bình và cũng nóng lên tới cùng nhiệt độ."),
           (r"Chia phần nhiệt dư cho nhiệt dung của $0{,}3\ \text{kg}$ nước do đá tan", r"Nước ban đầu cũng ở nhiệt độ cuối đó; phần dư chia cho cả $1{,}3\ \text{kg}$ nước.")]),
  buoc("Biện luận câu b", "Khi thả tiếp đá, trạng thái cuối là gì?",
       lua_chon=[(r"Đá tan một phần, nhiệt độ cuối $0\ ^{\circ}\text{C}$", True),
                 (r"Đá tan hết, nhiệt độ cuối trên $0\ ^{\circ}\text{C}$", r"Nước giờ chỉ hơn $0\ ^{\circ}\text{C}$ vài độ, nhiệt toả tối đa nhỏ hơn nhiều so với nhiệt cần để tan hết đá."),
                 (r"Đá không tan chút nào, nhiệt độ cuối dưới $0\ ^{\circ}\text{C}$", r"Nhiệt toả tối đa vẫn lớn hơn nhiệt cần để đưa đá lên $0\ ^{\circ}\text{C}$, nên còn dư để làm tan một phần.")],
       loi=r"Dùng lại nhiệt toả tối đa của câu a, quên nước lúc này chỉ còn hơn $0\ ^{\circ}\text{C}$ vài độ.",
       ke=[(r"Tính lại nhiệt toả tối đa của toàn bộ nước hiện có khi hạ về $0\ ^{\circ}\text{C}$, rồi so", True),
           (r"Dùng lại nhiệt toả tối đa đã tính ở câu a", r"Sau câu a nước đã nguội tới gần $0\ ^{\circ}\text{C}$ và có khối lượng mới; phải tính lại."),
           (r"Giả sử nhiệt độ cuối trên $0\ ^{\circ}\text{C}$ rồi viết phương trình", r"Giải ra nhiệt độ âm, mâu thuẫn với giả sử; phải biện luận trước.")]),
  buoc("Khối lượng đá tan", "Khối lượng đá tan thêm là bao nhiêu gam?", 33.5, "g", 0.5,
       loi=r"Cho toàn bộ nhiệt nước toả tối đa vào việc làm tan đá, quên phần nhiệt đưa đá từ $-10\ ^{\circ}\text{C}$ lên $0\ ^{\circ}\text{C}$.",
       ke=[(r"Cho $\lambda\,\Delta m$ bằng nhiệt toả tối đa trừ nhiệt đưa đá lên $0\ ^{\circ}\text{C}$", True),
           (r"Cho $\lambda\,\Delta m$ bằng nhiệt toả tối đa", r"Một phần nhiệt đó phải dùng để đưa đá lên $0\ ^{\circ}\text{C}$ trước khi đá tan."),
           (r"Cho $\lambda\,\Delta m$ bằng nhiệt đưa đá lên $0\ ^{\circ}\text{C}$", r"Đó là phần nhiệt đá nhận để nóng lên, không phải phần nhiệt còn lại để làm tan.")]),
  buoc("Khối lượng đá còn lại", "Trong bình còn lại bao nhiêu gam nước đá?", 266.5, "g", 1,
       loi=r"Trừ phần tan khỏi tổng hai lần thả đá, quên đá của câu a đã tan hết.",
       ke=[(r"Lấy khối lượng đá của lần thả sau trừ phần đã tan", True),
           (r"Lấy tổng đá của hai lần thả trừ phần đã tan", r"Đá của lần thả đầu đã tan hết ở câu a, chỉ còn đá của lần sau."),
           (r"Cộng phần đã tan vào khối lượng đá lần sau", r"Phần tan biến thành nước, nên khối đá giảm đi chứ không tăng.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 3 ──
 dict(nhan_dang=r"Thấy <b>đồ thị nhiệt độ theo thời gian đun có đoạn nằm ngang</b> → đoạn ngang: $Q=\lambda m$; đoạn dốc: $Q=mc\Delta t$.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 3}, buoc=[
  buoc("Đoạn nóng chảy", "Chất nóng chảy trên đoạn nào?",
       lua_chon=[(r"Đoạn BC, nhiệt độ không đổi dù vẫn nhận nhiệt", True),
                 (r"Đoạn AB, vì nhiệt độ tăng nhanh nhất", r"Nhiệt độ đang tăng nghĩa là chất chưa chuyển thể; khi nóng chảy nhiệt độ giữ nguyên."),
                 (r"Đoạn CD, vì lúc đó chất đã thành chất lỏng", r"Trên CD chất đã chảy hết và đang nóng lên ở thể lỏng; quá trình chảy đã xong trước đó.")],
       loi=r"Nghĩ rằng nhiệt độ không đổi thì chất không nhận nhiệt nên không có gì xảy ra."),
  buoc("Nhiệt nhận được trên đoạn AB", "Trên đoạn AB chất nhận bao nhiêu jun?", 24000, "J", 100,
       loi=r"Để thời gian theo phút khi nhân với công suất.",
       ke=[(r"Tính $Q=P\,\Delta\tau$ với $\Delta\tau$ đổi ra giây", True),
           (r"Tính $Q=P\,\Delta\tau$ với $\Delta\tau$ để theo phút", r"Oát là jun trên giây; để thời gian theo phút thì nhiệt lượng nhỏ đi $60$ lần."),
           (r"Tính $Q=mc\,\Delta t$", r"Nhiệt dung riêng thể rắn chưa biết, đó chính là ẩn; nhiệt lượng phải lấy từ nguồn.")]),
  buoc("Nhiệt dung riêng thể rắn", "Nhiệt dung riêng của chất ở thể rắn là bao nhiêu J/(kg·K)?", 800, "J/(kg·K)", 10,
       loi=r"Lấy nhiệt độ cuối của đoạn làm độ tăng nhiệt độ thay vì hiệu hai mốc.",
       ke=[(r"Chia nhiệt lượng cho $m\,\Delta t$ với $\Delta t$ là hiệu hai mốc nhiệt độ của đoạn AB", True),
           (r"Chia nhiệt lượng cho $m$ nhân nhiệt độ ở B", r"Cần độ tăng nhiệt độ của đoạn, không phải nhiệt độ cuối."),
           (r"Chia nhiệt lượng cho $m$ (không có $\Delta t$)", r"Thương đó có đơn vị J/kg, là dạng của $\lambda$, không phải nhiệt dung riêng.")]),
  buoc("Nhiệt nóng chảy riêng", "Nhiệt nóng chảy riêng của chất là bao nhiêu kJ/kg?", 120, "kJ/kg", 1,
       loi=r"Lấy thời gian là mốc cuối của đoạn BC thay vì hiệu hai mốc thời gian.",
       ke=[(r"Cho $P\,\Delta\tau=\lambda m$ với $\Delta\tau$ là hiệu hai mốc thời gian của BC", True),
           (r"Cho $P\,\Delta\tau=mc\,\Delta t$ trên BC", r"Trên BC nhiệt độ không đổi, $\Delta t=0$; nhiệt nhận được dùng để chuyển thể."),
           (r"Cho $P\,\Delta\tau=\lambda m$ với $\Delta\tau$ tính từ lúc bắt đầu đun tới C", r"Thời gian đó gồm cả đoạn AB, khi chất còn đang nóng lên chưa chảy.")]),
  buoc("Nhiệt dung riêng thể lỏng", "Nhiệt dung riêng của chất ở thể lỏng là bao nhiêu J/(kg·K)?", 1200, "J/(kg·K)", 10,
       loi=r"Lấy độ tăng nhiệt độ của đoạn CD từ $0\ ^{\circ}\text{C}$ thay vì từ nhiệt độ nóng chảy.",
       ke=[(r"Trên CD, chia $P\,\Delta\tau$ cho $m\,\Delta t$, mỗi đại lượng lấy hiệu hai mốc của CD", True),
           (r"Trên CD, lấy $\Delta t$ bằng nhiệt độ ở D", r"Chất bắt đầu nóng lên ở thể lỏng từ nhiệt độ nóng chảy, không phải từ $0\ ^{\circ}\text{C}$."),
           (r"Trên CD, lấy $\Delta\tau$ bằng toàn bộ thời gian đun", r"Chỉ đoạn CD chất ở thể lỏng; các đoạn trước chất còn rắn hoặc đang chảy.")]),
  buoc("Kiểm tra")]),
]


def kiem_so():
    F = Fr
    # D1
    assert C_TOA == 190 and C_THU == 1812 and M_N1 * C_N == 1680 and M_AL * C_AL == 132
    assert T_CB1 == F(59040, 2002) and abs(float(T_CB1) - 29.4905) < 1e-3 and round(float(T_CB1), 1) == 29.5
    assert T_QUEN == F(56400, 1870) and round(float(T_QUEN), 1) == 30.2 and round(float(T_QUEN - T_CB1), 1) == 0.7
    assert abs(float(Q_BINH) - 1252.7) < 0.5
    assert abs(float(C_TOA * (T_CU - T_CB1)) - 17197) < 1 and C_TOA * (T_CU - T_CB1) == C_THU * (T_CB1 - T1)
    # cách sai D1 cho số khác đáp án
    assert abs((120 + 20) / 2 - 29.5) > 1 and abs((0.5 * 120 + 0.4 * 20) / 0.9 - 29.5) > 1
    assert abs(float(M_AL * C_AL * T_CB1) - 1253) > 100 and abs(float(M_AL * C_AL * (T_CU - T_CB1)) - 1253) > 100
    assert abs(float((C_TOA + M_AL * C_AL) * T_CU + M_N1 * C_N * T1) / float(C_TOA + M_AL * C_AL + M_N1 * C_N) - 30.2) > 1
    assert abs(float(T_CB1) - 30.2) > 0.5                 # "giữ nguyên câu a" khác đáp án c
    assert abs(float(M_N1 * C_N) - 1812) > 10 and abs(float(150 * 880 + 400 * 4200) - 1812) > 10
    # D2
    assert Q_TOA_MAX == 126000 and Q1 == 6300 and Q2 == 102000 and Q1 + Q2 == 108300 < Q_TOA_MAX
    assert T_CB2 == F(17700, 5460) and round(float(T_CB2), 2) == 3.24 and 0 < T_CB2 < 30
    assert Q_TOA_B == 17700 and Q1 < Q_TOA_B < Q1 + Q2
    assert abs(float(M_TAN) * 1000 - 33.53) < 0.01 and abs(float(M_CON) * 1000 - 266.47) < 0.01
    assert 1 * C_N * 40 != Q_TOA_MAX                                  # lỗi lấy 30 − (−10)
    assert Q2 != Q1 + Q2 and F(3, 10) * C_N * 10 + Q2 != Q1 + Q2         # bỏ Q1; dùng c nước cho đá
    assert abs(float((Q_TOA_MAX - Q1 - Q2) / C_N) - 3.24) > 0.5 and abs(float((Q_TOA_MAX - Q1 - Q2) / (F(3, 10) * C_N)) - 3.24) > 0.5
    assert abs(float(Q_TOA_B / LAM) * 1000 - 33.5) > 1 and abs(float(Q1 / LAM) * 1000 - 33.5) > 1
    assert abs(600 - float(M_TAN) * 1000 - 266.5) > 1 and abs(300 + float(M_TAN) * 1000 - 266.5) > 1
    # giả sử t'' > 0 ở câu b thì ra âm
    t_gs = (Q_TOA_B - Q1 - Q2) / (F(16, 10) * C_N); assert t_gs < 0
    # D3
    assert P3 * 120 == 24000 and C_RAN == 800 and LAM3 == 120000 and C_LONG == 1200 and C_LONG / C_RAN == F(3, 2)
    assert P3 * 2 != 24000 and abs(24000 / (0.5 * 80) - 800) > 10 and 24000 / 0.5 != 800
    assert P3 * 420 / M3 / 1000 != 120                                  # Δτ = 7 min
    assert abs(24000 / (0.5 * 120) - 1200) > 10 and abs(P3 * 540 / (0.5 * 40) - 1200) > 10
    print("kiểm số liệu D1–D3 (bài 153): đạt")
