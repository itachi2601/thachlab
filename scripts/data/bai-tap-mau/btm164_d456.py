"""Bài tập mẫu CĐ16 "Truyền nhiệt và sự nở vì nhiệt" (lesson 164) — Dạng 4–6 (sự nở vì nhiệt). Module được build-hinh-164.py import.
Dàn ý: content/hsg9/cd16-truyen-nhiet-no-vi-nhiet/nguon.md mục "Bài tập mẫu" (số liệu dùng nguyên). Dạng sau dùng lại dạng trước:
  D4 nở dài Δl = l0·α·Δt (khe hở ray, độ dãn cầu, thước bị nở → số đọc sai)
  D5 nở khối: D = D0/(1+βΔt) khi khối lượng không đổi; thể tích tràn = dầu nở − can nở (dùng ΔV = V0·β·Δt như D4)
  D6 hai vật khác chất cùng nở: hiệu chiều dài không đổi (hai độ dãn bằng nhau) + cầu vừa lọt vòng (hai kích thước bằng nhau).
Xuất DANG, BUILD, ANALYSIS, SOLS, STEPS (3 phần tử mỗi list) và kiem_so()."""
import math, os, re, sys
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *  # noqa: F401,F403  (fig, seg, lbl, dot, poly, chevron, arrow, sol, M, P, A, buoc …)

TOPIC = "Nhiệt độ và cân bằng nhiệt"   # KHTN 9 chưa có YCCĐ nở vì nhiệt → dùng tạm YCCĐ L12 (198), xem nguon.md
NOTE = "Hình minh hoạ, không đúng tỉ lệ."
GREY = "#94a3b8"
OIL = "#f59e0b"

# ═════════════ SỐ LIỆU (mọi đáp số tính ở đây, kiem_so() kiểm lại) ═════════════
A_FE, A_CU, A_AL = F(12, 10**6), F(17, 10**6), F(24, 10**6)
# D4
L_RAY, T_LAP, T_MAX = F(25, 2), 15, 55
DL_RAY_MM = L_RAY * A_FE * (T_MAX - T_LAP) * 1000          # 6 mm
L_CAU, T_C0, T_C1 = 500, 10, 50
DL_CAU_CM = L_CAU * A_FE * (T_C1 - T_C0) * 100            # 24 cm
L_DOC, T_KHAC, T_DO = 2, 20, 45
L_THAT = L_DOC * (1 + A_FE * (T_DO - T_KHAC))             # 2,0006 m
# D5
D20, BETA, T_MUA = 800, F(1, 1000), 35
D35 = D20 / (1 + BETA * (T_MUA - 20))                     # 160000/203 ≈ 788,18 kg/m³
M_THIEU = (D20 - D35) * 1                                 # 1000 L = 1 m³ → ≈ 11,82 kg
V_THIEU_L = M_THIEU / D20 * 1000                          # ≈ 14,78 L dầu đong ở 20 °C
V_CAN, B_THEP, T_CAN = 20, F(36, 10**6), 40
DV_DAU_ML = V_CAN * BETA * (T_CAN - 20) * 1000            # 400 mL
DV_CAN_ML = V_CAN * B_THEP * (T_CAN - 20) * 1000          # 14,4 mL
V_TRAN_ML = DV_DAU_ML - DV_CAN_ML                         # 385,6 mL ≈ 0,39 L
# D6
HIEU = 5
L_CU = A_FE * HIEU / (A_CU - A_FE)                        # 12 cm
L_FE = L_CU + HIEU                                        # 17 cm
D_LO, D_CAU = F(4990, 1000), F(5)
RATE_UM = (D_LO * A_AL - D_CAU * A_FE) * 10**4            # 0,5976 µm/°C (1 µm = 10⁻⁴ cm)
DT6 = (D_CAU - D_LO) * 10**4 / RATE_UM                    # ≈ 167,3 °C
T6 = 20 + DT6                                             # ≈ 187,3 °C


def rich(s, size=13):
    """Nhãn SVG có chỉ số dưới _{…} và số mũ ^{…} → tspan dy (chỉ số Unicode hiện như dấu phẩy ở một số máy)."""
    ms = list(re.finditer(r"([_^])\{([^}]+)\}", s))
    if not ms:
        return s
    out, cur = s[:ms[0].start()], 0
    for k, m in enumerate(ms):
        tgt = 4 if m.group(1) == "_" else -6
        out += f'<tspan dy="{tgt - cur}" font-size="{max(12, size - 2)}">{m.group(2)}</tspan>'
        cur = tgt
        nxt = ms[k + 1].start() if k + 1 < len(ms) else len(s)
        if s[m.end():nxt]:
            out += f'<tspan dy="{-cur}">{s[m.end():nxt]}</tspan>'
            cur = 0
    return out

def txt(x, y, s, c="currentColor", size=14, anchor="start", weight="700", extra=""):
    size = max(size, 14)                                 # nhãn ≥ 14 đơn vị (viewBox 420 → ≈ 12,5 px ở 375 px)
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

def rect(x, y, w, h, c="currentColor", sw=2, fill="none", op=1, rx=0, inner=""):
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" fill-opacity="{op}" '
            f'stroke="{c}" stroke-width="{sw}">{inner}</rect>')

def thermo(x, y0, y1, lab0, lab1, dur, k1=1.0):
    """Nhiệt kế: cột đỏ dâng từ đáy (lab0) lên đỉnh (lab1) trong [0, k1·dur]."""
    h = y1 - y0
    b = rect(x - 5, y0, 10, h, "currentColor", 1.6, "none", 1, 5)
    b += f'<circle cx="{x}" cy="{y1 + 6}" r="8" fill="{RED}" stroke="currentColor" stroke-width="1.6"/>'
    yb = y1 - 4
    b += rect(x - 2.5, yb, 5, 4, RED, 0, RED, 1, 0,
              anim_kt("y", [yb, y0 + 4, y0 + 4], [0, k1, 1], dur) + anim_kt("height", [4, h - 4, h - 4], [0, k1, 1], dur))
    b += txt(x - 12, y0 + 8, lab1, RED, 12, "end") + txt(x - 12, y1, lab0, "currentColor", 12, "end")
    return b

def dimline(x1, x2, y, label, c=ORG, ly=None, anchor="middle"):
    """Kích thước ngang hai đầu V."""
    return (seg(x1, y, x2, y, c, 1.6) + chevron(x1, y, -1, 0, c, 1.6, 8) + chevron(x2, y, 1, 0, c, 1.6, 8)
            + seg(x1, y - 6, x1, y + 6, c, 1.2) + seg(x2, y - 6, x2, y + 6, c, 1.2)
            + txt((x1 + x2) / 2 if anchor == "middle" else x1, (ly if ly is not None else y - 7), label, c, 13, anchor))

def brk(x, y0, y1):
    """Dấu ngắt (không theo tỉ lệ) trên một thanh."""
    return seg(x - 4, y1 + 3, x + 2, y0 - 3, "currentColor", 1.6) + seg(x + 6, y1 + 3, x + 12, y0 - 3, "currentColor", 1.6)


# ═════════════ HÌNH ═════════════
# ───────────── Dạng 4 · nở dài ─────────────
def d4(kk):
    b = ""
    if kk == 0:
        TT, G = 4.0, 24                                  # khe vẽ 24 px — phóng đại, không theo tỉ lệ
        b += txt(16, 22, "Ray nóng dần từ lúc lắp tới lúc nóng nhất", "currentColor", 13)
        for x in range(22, 410, 38):
            b += rect(x, 126, 18, 10, GREY, 1.4, GREY, .3)
        b += rect(10, 112, 188, 14, BLUE, 2, BLUE, .18, 0, anim_kt("width", [188, 188 + G / 2], [0, 1], TT))
        b += rect(198 + G, 112, 188, 14, BLUE, 2, BLUE, .18, 0,
                  anim_kt("x", [198 + G, 198 + G / 2], [0, 1], TT) + anim_kt("width", [188, 188 + G / 2], [0, 1], TT))
        b += txt(210, 96, "khe hở", ORG, 12, "middle", "600") + seg(210, 100, 210, 108, ORG, 1.4) + chevron(210, 108, 0, 1, ORG, 1.4, 6)
        b += thermo(392, 30, 84, "15 °C", "55 °C", TT)
        b += txt(16, 160, "hai đầu ray vừa chạm nhau", RED, 13, "start", "700", 'opacity="0"').replace("</text>", show_at(TT * 0.995, TT) + "</text>", 1)
        b += txt(16, 184, "Mỗi thanh dài l_{0} = 12,5 m lúc lắp", "currentColor", 12, "start", "600")
        return fig("c16-4-0", "0 0 420 196", "Hai thanh ray nóng lên, dãn dài ra và khe hở giữa chúng hẹp dần",
                   b, "Mô phỏng: nhiệt kế dâng từ lúc lắp tới lúc nóng nhất, hai thanh ray dãn về phía khe. "
                      "Độ dãn và khe hở vẽ phóng đại rất nhiều lần, không theo tỉ lệ.")
    # hình dữ kiện
    b += txt(16, 22, "a) Ray: lắp ở 15 °C ; nóng nhất 55 °C", "currentColor", 13)
    b += txt(106, 40, "l_{0} = 12,5 m", "currentColor", 12, "middle", "600")
    b += rect(16, 46, 180, 12, BLUE, 2, BLUE, .18) + rect(224, 46, 180, 12, BLUE, 2, BLUE, .18)
    b += dimline(196, 224, 70, "khe tối thiểu = ?", RED, 90)
    b += txt(16, 118, "b) Cầu thép dài 500 m ; trong năm từ 10 °C đến 50 °C", "currentColor", 13)
    b += txt(205, 134, "Δl = ?", RED, 13, "middle")
    b += rect(40, 140, 330, 10, "currentColor", 2, GREY, .25)
    b += rect(40, 150, 16, 26, "currentColor", 2)
    b += (f'<circle cx="356" cy="155" r="5" fill="none" stroke="currentColor" stroke-width="1.8"/>'
          f'<circle cx="370" cy="155" r="5" fill="none" stroke="currentColor" stroke-width="1.8"/>')
    b += rect(346, 160, 34, 16, "currentColor", 2) + txt(363, 192, "con lăn", "currentColor", 11, "middle", "400")
    b += txt(16, 216, "c) Thước thép khắc vạch đúng ở 20 °C, dùng ở 45 °C", "currentColor", 13)
    b += rect(40, 228, 300, 10, "currentColor", 1.6, GREY, .3) + txt(348, 237, "ống", "currentColor", 12, "start", "600")
    b += rect(40, 242, 300, 14, ORG, 1.8, ORG, .15)
    for i in range(21):
        x = 40 + 15 * i
        b += seg(x, 242, x, 242 + (9 if i % 5 == 0 else 5), ORG, 1.2)
    b += txt(40, 272, "0", ORG, 12, "middle", "600") + txt(340, 272, "đọc: 2,000 m", ORG, 12, "middle", "600")
    b += txt(16, 292, "Chiều dài thật của ống l = ?", RED, 13)
    return fig("c16-4-2", "0 0 420 300", "Ba tình huống nở dài: khe hở ray, cầu thép đặt trên con lăn, thước thép đo một ống",
               b, "Dữ kiện: nhiệt độ lúc lắp, lúc khắc vạch và lúc dùng ghi trên hình ; dấu ? là đại lượng cần tìm. " + NOTE)


# ───────────── Dạng 5 · nở khối ─────────────
def d5(kk):
    b = ""
    if kk == 0:
        TT, K = 4.5, 0.5
        b += txt(16, 22, "Can đầy dầu tới miệng, nóng dần từ 20 °C lên 40 °C", "currentColor", 13)
        b += seg(96, 200, 360, 200, "currentColor", 2)
        b += rect(152, 70, 116, 129, OIL, 0, OIL, .35, 0,
                  anim_kt("y", [70, 63, 63], [0, K, 1], TT) + anim_kt("height", [129, 136, 136], [0, K, 1], TT))
        b += (f'<path d="M150,70 L150,200 L270,200 L270,70" fill="none" stroke="currentColor" stroke-width="2.6"/>'
              f'<path d="M180,70 C180,46 240,46 240,70" fill="none" stroke="currentColor" stroke-width="2.2"/>')
        b += (f'<path d="M268,64 C284,64 286,78 284,96 L284,197" fill="none" stroke="{OIL}" stroke-width="4" opacity="0">'
              f'{show_at(K * TT, TT)}</path>')
        b += (f'<ellipse cx="306" cy="200" rx="0" ry="3.5" fill="{OIL}" fill-opacity=".7">'
              f'{anim_kt("rx", [0, 0, 26], [0, K, 1], TT)}</ellipse>')
        b += txt(306, 222, "V_{tràn} = ?", RED, 13, "middle", "700", 'opacity="0"').replace("</text>", show_at(TT * 0.995, TT) + "</text>", 1)
        b += thermo(70, 60, 170, "20 °C", "40 °C", TT, K)
        b += txt(210, 140, "dầu", "currentColor", 13, "middle", "600")
        return fig("c16-5-0", "0 0 420 230", "Can thép đựng đầy dầu tới miệng; khi nóng lên, mặt dầu dâng quá miệng và dầu tràn ra ngoài",
                   b, "Mô phỏng: cả can và dầu nóng lên cùng lúc ; dầu nở nhiều hơn dung tích can nên tràn ra. "
                      "Phần dầu dâng và tràn vẽ phóng đại, không theo tỉ lệ.")
    # hình dữ kiện
    b += txt(16, 22, "Cùng 1000 L dầu, đong ở hai nhiệt độ", "currentColor", 13)
    for (x0, lab, nn, sp, dl) in ((30, "1000 L ở 20 °C", 6, 12.5, "D_{20} = 800 kg/m^{3}"), (170, "1000 L ở 35 °C", 5, 15, "D_{35} = ?")):
        b += txt(x0 + 40, 44, lab, "currentColor", 12, "middle", "600") + rect(x0, 52, 80, 80, "currentColor", 2, OIL, .12)
        off = (80 - sp * (nn - 1)) / 2
        for i in range(nn):
            for j in range(nn):
                b += dot(x0 + off + sp * i, 52 + off + sp * j, 2.6, OIL)
        b += txt(x0 + 40, 152, dl, RED if "?" in dl else "currentColor", 12, "middle", "700")
    b += txt(270, 84, "β_{dầu} = 1·10^{-3} K^{-1}", "currentColor", 12, "start", "600")
    b += txt(270, 104, "m không đổi khi nở", "currentColor", 12, "start", "600")
    b += txt(16, 186, "Can thép đầy dầu tới miệng ở 20 °C", "currentColor", 13)
    b += rect(32, 214, 66, 72, OIL, 0, OIL, .35)
    b += f'<path d="M30,214 L30,288 L100,288 L100,214" fill="none" stroke="currentColor" stroke-width="2.4"/>'
    b += txt(120, 214, "V_{0} = 20 L ; nung cả can và dầu tới 40 °C", "currentColor", 12, "start", "600")
    b += txt(120, 236, "β_{thép} = 36·10^{-6} K^{-1}", "currentColor", 12, "start", "600")
    b += txt(120, 266, "V_{tràn} = ?", RED, 13)
    return fig("c16-5-2", "0 0 420 300", "Hai thùng 1000 lít dầu ở 20 và 35 độ C, và một can thép đầy dầu được nung nóng",
               b, "Dữ kiện: cùng thể tích 1000 L nhưng đong ở hai nhiệt độ ; can đầy tới miệng ở 20 °C. "
                  "Chấm tròn chỉ để gợi các phân tử xa nhau hơn khi nóng, không đếm. " + NOTE)


# ───────────── Dạng 6 · hai vật nở khác nhau ─────────────
def d6(kk):
    b = ""
    if kk == 0:
        TT, KH = 5.0, 0.75
        RT, CX = 150, 220
        h0, h1, r0, r1 = 38, 44, 40, 44                   # nửa lỗ và bán kính cầu (px) — độ nở phóng đại
        cys, kts = [], []
        for i in range(11):
            s = i / 10
            h, r = h0 + (h1 - h0) * s, r0 + (r1 - r0) * s
            cys.append(RT - math.sqrt(max(r * r - h * h, 0)))
            kts.append(KH * s)
        cys.append(RT + 14 + r1 + 4); kts.append(1)
        b += txt(16, 22, "Nung vòng nhôm và quả cầu thép cùng lúc", "currentColor", 13)
        b += rect(CX - h0 - 46, RT, 46, 14, GREY, 2, GREY, .35, 2,
                  anim_kt("x", [CX - h0 - 46, CX - h1 - 46, CX - h1 - 46], [0, KH, 1], TT))
        b += rect(CX + h0, RT, 46, 14, GREY, 2, GREY, .35, 2,
                  anim_kt("x", [CX + h0, CX + h1, CX + h1], [0, KH, 1], TT))
        b += (f'<circle cx="{CX}" cy="{cys[0]:.1f}" r="{r0}" fill="{BLUE}" fill-opacity=".25" stroke="currentColor" stroke-width="2">'
              f'{anim_kt("r", [r0, r1, r1], [0, KH, 1], TT)}{anim_kt("cy", cys, kts, TT)}</circle>')
        b += txt(CX - 75, RT + 34, "vòng nhôm", "currentColor", 12, "middle", "600")
        b += txt(CX + 40, 92, "cầu thép", BLUE, 12, "start", "600")
        b += thermo(56, 50, 150, "20 °C", "t = ?", TT, KH)
        b += txt(276, 236, "cầu lọt qua vòng", RED, 13, "start", "700", 'opacity="0"').replace("</text>", show_at(TT * 0.995, TT) + "</text>", 1)
        return fig("c16-6-0", "0 0 420 256", "Quả cầu thép nằm trên lỗ vòng nhôm; khi nung, lỗ rộng ra nhanh hơn quả cầu và quả cầu lọt qua",
                   b, "Mô phỏng: hình cắt ngang vòng nhôm, quả cầu đặt trên lỗ ; nung cả hai cùng lúc. "
                      "Độ nở vẽ phóng đại rất nhiều lần, không theo tỉ lệ ; không ghi nhiệt độ lúc lọt.")
    # hình dữ kiện
    b += txt(16, 22, "a) Hai thanh luôn cùng nhiệt độ", "currentColor", 13)
    b += txt(30, 46, "Thanh đồng: α_{Cu} = 17·10^{-6} K^{-1} ; l_{Cu} = ?", "currentColor", 12, "start", "600")
    b += rect(30, 54, 165, 12, ORG, 2, ORG, .2) + rect(205, 54, 165, 12, ORG, 2, ORG, .2) + brk(197, 54, 66)
    b += txt(30, 92, "Thanh thép: α_{Fe} = 12·10^{-6} K^{-1} ; l_{Fe} = ?", "currentColor", 12, "start", "600")
    b += rect(30, 100, 165, 12, GREY, 2, GREY, .3) + rect(205, 100, 165, 12, GREY, 2, GREY, .3) + brk(197, 100, 112)
    b += txt(30, 136, "Ở mọi nhiệt độ: hiệu chiều dài hai thanh luôn là 5 cm", BLUE, 12, "start", "700")
    b += txt(16, 170, "b) Ở 20 °C, trước khi nung", "currentColor", 13)
    RT, CX = 222, 110
    b += rect(CX - 16 - 42, RT, 42, 12, GREY, 2, GREY, .35, 2) + rect(CX + 16, RT, 42, 12, GREY, 2, GREY, .35, 2)
    b += (f'<circle cx="{CX}" cy="{RT - math.sqrt(18 * 18 - 16 * 16):.1f}" r="18" fill="{BLUE}" fill-opacity=".25" '
          f'stroke="currentColor" stroke-width="2"/>')
    b += txt(200, 196, "Quả cầu thép: d_{cầu} = 5,000 cm", "currentColor", 12, "start", "600")
    b += txt(200, 216, "Vòng nhôm: d_{lỗ} = 4,990 cm", "currentColor", 12, "start", "600")
    b += txt(200, 236, "α_{Al} = 24·10^{-6} K^{-1}", "currentColor", 12, "start", "600")
    b += txt(16, 274, "Nung cả hai tới cùng nhiệt độ t thì cầu vừa lọt: t = ?", RED, 13)
    return fig("c16-6-2", "0 0 420 286", "Hai thanh đồng và thép; quả cầu thép đặt trên lỗ của một vòng nhôm",
               b, "Dữ kiện: hai thanh vẽ bằng nhau và có dấu ngắt, không cho biết thanh nào dài hơn ; "
                  "độ chênh giữa quả cầu và lỗ vẽ phóng đại. " + NOTE)


BUILD = [d4, d5, d6]

# ═════════════ ĐỀ ═════════════
DANG = [
dict(label="Dạng 4 · Nâng cao · Nở dài: khe hở đường ray, độ dãn của cầu, thước bị nở",
     topic=TOPIC,
     problem_html=r"""<p>Thép có hệ số nở dài $\alpha=12\cdot10^{-6}\ \text{K}^{-1}$. Trong cả bài, coi mỗi vật nóng đều, có cùng nhiệt độ ở mọi chỗ và được dãn tự do.</p><ol type="a"><li>Một đường ray lắp bằng các thanh thép giống nhau, mỗi thanh dài $12{,}5\ \text{m}$, lắp lúc nhiệt độ $15\ ^\circ\text{C}$. Mùa hè ray nóng nhất tới $55\ ^\circ\text{C}$. Lúc lắp, khe hở giữa đầu hai thanh liền nhau phải tối thiểu bao nhiêu milimét để ray không bị cong?</li><li>Một cây cầu thép dài $500\ \text{m}$ ở $10\ ^\circ\text{C}$, một đầu đặt trên con lăn. Nhiệt độ trong năm thay đổi từ $10\ ^\circ\text{C}$ đến $50\ ^\circ\text{C}$. Chiều dài cầu thay đổi nhiều nhất bao nhiêu xentimét?</li><li>Một thước thép có vạch chia khắc đúng ở $20\ ^\circ\text{C}$. Ở $45\ ^\circ\text{C}$, thước và ống cùng nhiệt độ, dùng thước đo một ống thì đọc được $2{,}000\ \text{m}$. Số đọc này lớn hơn hay nhỏ hơn chiều dài thật của ống lúc đó? Tính chiều dài thật.</li></ol>"""),
dict(label="Dạng 5 · Nâng cao · Nở khối: khối lượng riêng theo nhiệt độ và thể tích chất lỏng tràn khỏi bình",
     topic=TOPIC,
     problem_html=r"""<p>Dầu hoả có khối lượng riêng $800\ \text{kg/m}^3$ ở $20\ ^\circ\text{C}$ và hệ số nở khối $\beta=1\cdot10^{-3}\ \text{K}^{-1}$. Khi dầu nở ra, khối lượng của lượng dầu đó không đổi.</p><ol type="a"><li>Tính khối lượng riêng của dầu ở $35\ ^\circ\text{C}$.</li><li>Một người mua $1000$ lít dầu, đong lúc dầu ở $35\ ^\circ\text{C}$. So với mua $1000$ lít đong lúc dầu ở $20\ ^\circ\text{C}$, người đó nhận ít hơn bao nhiêu kilôgam dầu?</li><li>Một can thép có dung tích $20$ lít ở $20\ ^\circ\text{C}$, được đổ đầy dầu tới miệng ở $20\ ^\circ\text{C}$. Để can ngoài nắng, cả can và dầu cùng nóng lên tới $40\ ^\circ\text{C}$. Hệ số nở khối của thép là $36\cdot10^{-6}\ \text{K}^{-1}$. Bỏ qua sự bay hơi, tính thể tích dầu tràn ra khỏi can.</li></ol>"""),
dict(label="Dạng 6 · Vận dụng cao · Mở rộng HSG: Hai vật khác chất cùng nở vì nhiệt",
     topic=TOPIC,
     problem_html=r"""<p>Hệ số nở dài: đồng $\alpha_{Cu}=17\cdot10^{-6}\ \text{K}^{-1}$, thép $\alpha_{Fe}=12\cdot10^{-6}\ \text{K}^{-1}$, nhôm $\alpha_{Al}=24\cdot10^{-6}\ \text{K}^{-1}$. Các vật luôn có cùng nhiệt độ với nhau và dãn tự do.</p><ol type="a"><li>Một thanh đồng và một thanh thép được chọn sao cho ở mọi nhiệt độ, hiệu chiều dài của hai thanh luôn bằng $5\ \text{cm}$. Tính chiều dài mỗi thanh ở $0\ ^\circ\text{C}$. Thanh nào dài hơn?</li><li>Ở $20\ ^\circ\text{C}$, một vòng nhôm có đường kính trong $4{,}990\ \text{cm}$, một quả cầu thép có đường kính $5{,}000\ \text{cm}$. Nung nóng cả vòng và cầu tới cùng một nhiệt độ $t$ thì quả cầu vừa lọt qua vòng. Tính $t$.</li></ol>"""),
]

# ═════════════ BẢNG PHÂN TÍCH ĐỀ (cột 1 nguyên văn đề ; cột 2 chỉ dữ liệu có trong đề ; cột 3 kiến thức nền + câu hỏi gợi) ═════════════
ANALYSIS = [
 # Dạng 4
 [(r'"coi mỗi vật nóng đều, có cùng nhiệt độ ở mọi chỗ và được dãn tự do"', r"vật dãn tự do, nóng đều", r"⚠ điều kiện để dùng $\Delta l=l_0\alpha\Delta t$ cho cả vật. Nếu bị chặn hai đầu thì sao ?"),
  (r'"Thép có hệ số nở dài $\alpha=12\cdot10^{-6}\ \text{K}^{-1}$"', r"$\alpha=12\cdot10^{-6}\ \text{K}^{-1}$", r"$\alpha$ cho biết điều gì về $1\ \text{m}$ thép khi tăng $1\ ^\circ\text{C}$ ?"),
  (r'"mỗi thanh dài $12{,}5\ \text{m}$, lắp lúc nhiệt độ $15\ ^\circ\text{C}$", "nóng nhất tới $55\ ^\circ\text{C}$"', r"$l_0=12{,}5\ \text{m}$ ; $15\ ^\circ\text{C}$ ; $55\ ^\circ\text{C}$", r"$\Delta t$ tính từ nhiệt độ nào tới nhiệt độ nào ?"),
  (r'"khe hở giữa đầu hai thanh liền nhau phải tối thiểu"', r"khe $=?$", r"Mỗi thanh dãn về cả hai đầu. Một khe nhận phần dãn của những thanh nào ?"),
  (r'"cầu thép dài $500\ \text{m}$", "từ $10\ ^\circ\text{C}$ đến $50\ ^\circ\text{C}$"', r"$l_0=500\ \text{m}$ ; $\Delta l=?$", r"Cùng công thức nở dài. So với ray, $\Delta t$ và $l_0$ khác gì ?"),
  (r'"vạch chia khắc đúng ở $20\ ^\circ\text{C}$", "Ở $45\ ^\circ\text{C}$ … đọc được $2{,}000\ \text{m}$"', r"$20\ ^\circ\text{C}$ ; $45\ ^\circ\text{C}$ ; $l_{đọc}=2{,}000\ \text{m}$ ; $l=?$", r"Ở $45\ ^\circ\text{C}$ một khoảng chia ghi “$1\ \text{cm}$” thật dài bao nhiêu ? Cùng ống thì đặt được nhiều hay ít khoảng chia hơn ?")],
 # Dạng 5
 [(r'"Khi dầu nở ra, khối lượng của lượng dầu đó không đổi"', r"$m$ không đổi", r"⚠ điều kiện để nối $D$ với $V$ : $D=\dfrac{m}{V}$. $V$ tăng thì $D$ thế nào ?"),
  (r'"khối lượng riêng $800\ \text{kg/m}^3$ ở $20\ ^\circ\text{C}$", "hệ số nở khối $\beta=1\cdot10^{-3}\ \text{K}^{-1}$"', r"$D_{20}=800\ \text{kg/m}^3$ ; $\beta=1\cdot10^{-3}\ \text{K}^{-1}$", r"Nở khối : $V=V_0(1+\beta\Delta t)$"),
  (r'"Tính khối lượng riêng của dầu ở $35\ ^\circ\text{C}$"', r"$D_{35}=?$", r"Viết $m$ ở hai nhiệt độ rồi cho bằng nhau. $\Delta t$ bằng bao nhiêu ?"),
  (r'"mua $1000$ lít dầu, đong lúc dầu ở $35\ ^\circ\text{C}$"', r"$V=1000\ \text{L}$ ; $\Delta m=?$", r"Cùng $1000\ \text{L}$, ở nhiệt độ nào nặng hơn ? $1000\ \text{L}$ bằng bao nhiêu $\text{m}^3$ ?"),
  (r'"đổ đầy dầu tới miệng ở $20\ ^\circ\text{C}$"', r"$V_{dầu}=V_{can}=20\ \text{L}$ lúc đầu", r"⚠ lúc đầu dầu vừa đúng bằng dung tích can"),
  (r'"cả can và dầu cùng nóng lên tới $40\ ^\circ\text{C}$", "nở khối của thép là $36\cdot10^{-6}\ \text{K}^{-1}$"', r"$\Delta t$ chung ; $\beta_{thép}=36\cdot10^{-6}\ \text{K}^{-1}$", r"Dung tích của can có đổi khi can nóng lên không ? Nở theo hệ số nào ?"),
  (r'"tính thể tích dầu tràn ra khỏi can"', r"$V_{tràn}=?$", r"Sau khi nóng, so sánh thể tích dầu với dung tích can. Phần nào không còn chỗ chứa ?")],
 # Dạng 6
 [(r'"Các vật luôn có cùng nhiệt độ với nhau và dãn tự do"', r"cùng $\Delta t$", r"⚠ hai vật cùng tăng một $\Delta t$ thì mới so được độ dãn"),
  (r'"ở mọi nhiệt độ, hiệu chiều dài của hai thanh luôn bằng $5\ \text{cm}$"', r"$|l_{Fe}-l_{Cu}|=5\ \text{cm}$ ở mọi $t$", r"Hiệu không đổi khi cùng tăng $\Delta t$ thì độ dãn hai thanh phải thế nào ?"),
  (r'"đồng $\alpha_{Cu}=17\cdot10^{-6}$", "thép $\alpha_{Fe}=12\cdot10^{-6}$"', r"$\alpha_{Cu}$ ; $\alpha_{Fe}$", r"Độ dãn $\Delta l=l_0\alpha\Delta t$. Thanh có $\alpha$ lớn thì cần dài hay ngắn để dãn bằng thanh kia ?"),
  (r'"vòng nhôm có đường kính trong $4{,}990\ \text{cm}$"', r"$d_{lỗ}=4{,}990\ \text{cm}$ ; $\alpha_{Al}$", r"Khi vòng nóng lên, lỗ của vòng rộng ra, hẹp lại hay giữ nguyên ?"),
  (r'"quả cầu thép có đường kính $5{,}000\ \text{cm}$"', r"$d_{cầu}=5{,}000\ \text{cm}$ ; $\alpha_{Fe}$", r"Cầu có nở không ? Đường kính cầu viết theo $\Delta t$ thế nào ?"),
  (r'"Nung nóng cả vòng và cầu tới cùng một nhiệt độ $t$ thì quả cầu vừa lọt"', r"$t=?$", r"“Vừa lọt” là điều kiện gì giữa hai đường kính ? Nhớ $t=20\ ^\circ\text{C}+\Delta t$")],
]

# ═════════════ LỜI GIẢI ═════════════
R4 = [r"<strong>Khái niệm:</strong> vật rắn nóng lên thì dài ra ; $\alpha$ là độ dãn của $1\ \text{m}$ khi tăng $1\ ^\circ\text{C}$.",
      r"<strong>Công thức:</strong> $\Delta l=l_0\alpha\Delta t$ ; $l=l_0(1+\alpha\Delta t)$.",
      r"<strong>Hiệu nhiệt độ:</strong> $\Delta t$ tính từ lúc vật có chiều dài $l_0$ ; $1\ ^\circ\text{C}$ chênh lệch $=1\ \text{K}$.",
      r"<strong>Điều kiện:</strong> vật nóng đều, dãn tự do."]
R5 = [r"<strong>Khái niệm:</strong> chất lỏng nóng lên thì thể tích tăng, khối lượng giữ nguyên.",
      r"<strong>Công thức:</strong> $V=V_0(1+\beta\Delta t)$ ; $\Delta V=V_0\beta\Delta t$.",
      r"<strong>Khối lượng riêng:</strong> $m$ không đổi nên $D=\dfrac{D_0}{1+\beta\Delta t}$.",
      r"<strong>Bình chứa:</strong> dung tích bình nở như một khối đặc cùng chất làm bình."]
R6 = [r"<strong>Khái niệm:</strong> các chất khác nhau có hệ số nở khác nhau.",
      r"<strong>Công thức:</strong> $l=l_0(1+\alpha\Delta t)$, $\Delta l=l_0\alpha\Delta t$, áp dụng cho từng vật.",
      r"<strong>Lỗ trong vật:</strong> lỗ nở như một miếng đặc cùng chất, cùng cỡ.",
      r"<strong>Điều kiện:</strong> các vật cùng nhiệt độ, cùng tăng $\Delta t$."]

SOLS = [
 sol(R4, [
  ("Khe hở tối thiểu", [P(r"Mỗi thanh dãn thêm $\Delta l$, nửa về mỗi đầu. Một khe nhận nửa độ dãn của hai thanh liền nhau, tổng đúng $\Delta l$ :"),
     M(r"\Delta l=l_0\alpha\Delta t"), M(r"\Delta l=12{,}5\cdot12\cdot10^{-6}\cdot(55-15)"), A(r"\Delta l=6\cdot10^{-3}\ \text{m}=6\ \text{mm}")]),
  ("Độ thay đổi chiều dài cầu", [P(r"Nhiệt độ thay đổi nhiều nhất $\Delta t=50-10=40\ ^\circ\text{C}$ :"),
     M(r"\Delta l=500\cdot12\cdot10^{-6}\cdot40"), A(r"\Delta l=0{,}24\ \text{m}=24\ \text{cm}")]),
  ("Số đọc lớn hay nhỏ hơn", [P(r"Ở $45\ ^\circ\text{C}$ thước dãn : mỗi khoảng chia dài hơn giá trị ghi trên vạch."),
     P(r"Cùng một ống, số khoảng chia đặt vừa ít hơn."),
     A(r"T:Số đọc nhỏ hơn chiều dài thật (thước đọc thiếu).")]),
  ("Chiều dài thật của ống", [P(r"Đoạn thước ghi $2{,}000\ \text{m}$ đã dãn từ $20\ ^\circ\text{C}$ tới $45\ ^\circ\text{C}$ :"),
     M(r"l=l_{đọc}(1+\alpha\Delta t)"), M(r"l=2{,}000\cdot(1+12\cdot10^{-6}\cdot25)"), A(r"l=2{,}0006\ \text{m}")]),
  ("Kiểm tra", [P(r"a) $\dfrac{6\ \text{mm}}{12{,}5\ \text{m}}\approx0{,}05\%$ : độ dãn nhỏ, khe ray vài milimét là hợp lí ✓."),
     P(r"b) Cùng $\Delta t=40\ ^\circ\text{C}$ như câu a, cầu dài gấp $40$ lần một thanh ray nên dãn gấp $40$ lần : $40\cdot6\ \text{mm}=240\ \text{mm}$ ✓."),
     P(r"c) Thước đọc thiếu $0{,}6\ \text{mm}$ trên $2\ \text{m}$ : chỉ đáng kể khi cần đo rất chính xác ✓.")])],
  [r"a) Khe hở tối thiểu $6\ \text{mm}$", r"b) Chiều dài cầu thay đổi nhiều nhất $24\ \text{cm}$", r"c) Số đọc nhỏ hơn chiều dài thật ; $l=2{,}0006\ \text{m}$"],
  r"Nhận dạng: thấy <strong>khe hở, độ dãn, thước khắc đúng ở một nhiệt độ</strong> → $\Delta l=l_0\alpha\Delta t$, $\Delta t$ tính từ lúc vật có chiều dài $l_0$ ; thước nóng thì đọc thiếu."),
 sol(R5, [
  ("Khối lượng riêng ở 35 °C", [P(r"Cùng lượng dầu : $m=D_{20}V_0=D_{35}V_0(1+\beta\Delta t)$ :"),
     M(r"D_{35}=\dfrac{D_{20}}{1+\beta\Delta t}=\dfrac{800}{1+10^{-3}\cdot15}"), A(r"D_{35}\approx788{,}2\ \text{kg/m}^3")]),
  ("Lượng dầu nhận thiếu", [P(r"$1000\ \text{L}=1\ \text{m}^3$. Đong ở $35\ ^\circ\text{C}$ được $m_{35}=788{,}2\ \text{kg}$, đong ở $20\ ^\circ\text{C}$ được $800\ \text{kg}$ :"),
     M(r"\Delta m=(D_{20}-D_{35})V=(800-788{,}2)\cdot1"), A(r"\Delta m\approx11{,}8\ \text{kg}")]),
  ("Dầu nở thêm", [P(r"Dầu tăng từ $20\ ^\circ\text{C}$ lên $40\ ^\circ\text{C}$, $\Delta t=20\ ^\circ\text{C}$ :"),
     M(r"\Delta V_{dầu}=V_0\beta\Delta t=20\cdot10^{-3}\cdot20"), A(r"\Delta V_{dầu}=0{,}4\ \text{L}=400\ \text{mL}")]),
  ("Dung tích can tăng thêm", [P(r"Dung tích can nở như một khối thép đặc cùng hình dạng :"),
     M(r"\Delta V_{can}=V_0\beta_{thép}\Delta t=20\cdot36\cdot10^{-6}\cdot20"), A(r"\Delta V_{can}=0{,}0144\ \text{L}=14{,}4\ \text{mL}")]),
  ("Thể tích dầu tràn", [P(r"Phần dầu nở vượt quá phần dung tích can tăng thêm thì tràn ra :"),
     M(r"V_{tràn}=\Delta V_{dầu}-\Delta V_{can}=400-14{,}4"), A(r"V_{tràn}\approx386\ \text{mL}\approx0{,}39\ \text{L}")]),
  ("Kiểm tra", [P(r"Câu b : lượng thiếu bằng khoảng $\dfrac{11{,}8}{800}\approx1{,}5\%$, đúng cỡ $\beta\Delta t=1{,}5\%$ ✓ ; ứng với $\dfrac{11{,}8}{0{,}8}\approx14{,}8$ lít dầu đong ở $20\ ^\circ\text{C}$."),
     P(r"Câu c : $\dfrac{\beta_{dầu}}{\beta_{thép}}\approx28$ nên can nở rất ít so với dầu, phần trừ đi nhỏ ✓.")])],
  [r"a) $D_{35}\approx788{,}2\ \text{kg/m}^3$", r"b) Nhận ít hơn khoảng $11{,}8\ \text{kg}$", r"c) $V_{tràn}\approx0{,}39\ \text{L}$ (khoảng $386\ \text{mL}$)"],
  r"Nhận dạng: thấy <strong>đong chất lỏng ở nhiệt độ khác</strong> → $D=\dfrac{D_0}{1+\beta\Delta t}$ ; thấy <strong>bình đầy tới miệng rồi nóng lên</strong> → tràn = phần chất lỏng nở − phần dung tích bình nở."),
 sol(R6, [
  ("Điều kiện hiệu không đổi", [P(r"Hiệu chiều dài giữ nguyên khi cùng tăng $\Delta t$ nghĩa là hai thanh dãn thêm đúng bằng nhau."),
     A(r"T:Hai độ dãn bằng nhau: $l_{Cu}\alpha_{Cu}\Delta t=l_{Fe}\alpha_{Fe}\Delta t$.")]),
  ("Chiều dài hai thanh", [M(r"l_{Cu}\alpha_{Cu}=l_{Fe}\alpha_{Fe}\ \Rightarrow\ 17\,l_{Cu}=12\,l_{Fe}"),
     P(r"Thanh đồng có $\alpha$ lớn hơn nên phải ngắn hơn : $l_{Fe}=l_{Cu}+5$ :"),
     M(r"17\,l_{Cu}=12\,(l_{Cu}+5)\ \Rightarrow\ 5\,l_{Cu}=60"), A(r"l_{Cu}=12\ \text{cm}\ ;\ l_{Fe}=17\ \text{cm}")]),
  ("Phần chênh giảm sau mỗi độ", [P(r"Lỗ của vòng nở theo nhôm, cầu nở theo thép. Mỗi khi tăng $1\ ^\circ\text{C}$ :"),
     M(r"\Delta d_{lỗ}=4{,}990\cdot24\cdot10^{-6}=1{,}1976\cdot10^{-4}\ \text{cm}"),
     M(r"\Delta d_{cầu}=5{,}000\cdot12\cdot10^{-6}=0{,}6\cdot10^{-4}\ \text{cm}"),
     P(r"Lỗ rộng nhanh hơn cầu, phần chênh giảm ($10^{-4}\ \text{cm}=1\ \mu\text{m}$) :"),
     A(r"(1{,}1976-0{,}6)\cdot10^{-4}\ \text{cm}\approx0{,}598\ \mu\text{m}")]),
  ("Độ tăng nhiệt độ", [P(r"Vừa lọt khi hai đường kính bằng nhau :"),
     M(r"4{,}990(1+24\cdot10^{-6}\Delta t)=5{,}000(1+12\cdot10^{-6}\Delta t)"),
     P(r"Phần chênh ban đầu $5{,}000-4{,}990=0{,}010\ \text{cm}=100\ \mu\text{m}$, mỗi độ giảm $0{,}5976\ \mu\text{m}$ :"),
     M(r"\Delta t=\dfrac{100}{0{,}5976}"),
     A(r"\Delta t\approx167\ ^\circ\text{C}")]),
  ("Nhiệt độ nung", [M(r"t=20+\Delta t=20+167"), A(r"t\approx187\ ^\circ\text{C}")]),
  ("Kiểm tra", [P(r"a) $12\cdot17\cdot10^{-6}=17\cdot12\cdot10^{-6}$ : hai thanh dãn bằng nhau ✓ ; $17-12=5\ \text{cm}$ ✓."),
     P(r"b) Với $\Delta t\approx167{,}3\ ^\circ\text{C}$ : $d_{lỗ}\approx4{,}990\cdot1{,}004016\approx5{,}0100\ \text{cm}$ ; $d_{cầu}\approx5{,}000\cdot1{,}002008\approx5{,}0100\ \text{cm}$ ✓.")])],
  [r"a) $l_{Cu}=12\ \text{cm}$, $l_{Fe}=17\ \text{cm}$ ; thanh thép dài hơn", r"b) $t\approx187\ ^\circ\text{C}$"],
  r"Nhận dạng: thấy <strong>hai vật khác chất cùng nung</strong> → viết kích thước từng vật theo $l_0(1+\alpha\Delta t)$ rồi đặt điều kiện của đề (độ dãn bằng nhau, kích thước bằng nhau) ; lỗ nở như miếng đặc."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC ═════════════
STEPS = [
 # ── Dạng 4 ──
 dict(nhan_dang=r"Thấy <b>khe hở</b>, <b>độ dãn</b>, <b>thước khắc đúng ở … °C</b> → nghĩ tới <b>$\Delta l=l_0\alpha\Delta t$</b>",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Khe hở tối thiểu", "Khe hở tối thiểu lúc lắp bằng bao nhiêu milimét?", float(DL_RAY_MM), "mm", 0.05,
       loi=r"Lấy $\Delta t$ bằng nhiệt độ nóng nhất (tính từ $0\ ^\circ\text{C}$) thay vì từ lúc lắp ; hoặc quên đổi mét sang milimét."),
  buoc("Độ thay đổi chiều dài cầu", "Chiều dài cầu thay đổi nhiều nhất bao nhiêu xentimét?", float(DL_CAU_CM), "cm", 0.2,
       loi=r"Lấy chiều dài lúc nóng $l_0(1+\alpha\Delta t)$ làm đáp số, trong khi đề hỏi phần thay đổi $\Delta l$.",
       ke=[(r"$\Delta l=l_0\alpha\Delta t$ với $\Delta t$ là chênh lệch giữa nhiệt độ cao nhất và thấp nhất", True),
           (r"$\Delta l=l_0\alpha t$ với $t$ là nhiệt độ cao nhất", r"$\alpha$ nhân với độ tăng nhiệt độ tính từ lúc cầu dài $l_0$, không nhân với nhiệt độ cuối."),
           (r"$\Delta l=l_0(1+\alpha\Delta t)$", r"Đó là chiều dài cầu lúc nóng, không phải phần thay đổi.")]),
  buoc("Số đọc lớn hay nhỏ hơn", "Ở 45 °C, số đọc trên thước so với chiều dài thật của ống thế nào?",
       lua_chon=[(r"Nhỏ hơn chiều dài thật, vì mỗi khoảng chia của thước đã dãn dài ra", True),
                 (r"Lớn hơn chiều dài thật, vì thước dài ra nên đo được nhiều hơn", r"Thước dài ra thì mỗi khoảng chia dài hơn giá trị ghi ; cùng một ống chỉ chứa được ít khoảng chia hơn."),
                 (r"Bằng chiều dài thật, vì thước và ống cùng nóng lên", r"Đề chỉ cho thước khắc đúng ở một nhiệt độ ; chiều dài thật của ống lúc đó là thứ cần tìm, so với thước đã dãn.")],
       loi=r"Nghĩ thước dài ra thì số đọc lớn hơn ; thật ra mỗi vạch ghi một giá trị cố định mà khoảng chia đã dài ra.",
       ke=[(r"So sánh độ dài thật của một khoảng chia lúc dãn với giá trị ghi trên vạch", True),
           (r"Tính luôn $l=l_{đọc}(1-\alpha\Delta t)$", r"Chưa xét thước dãn làm số đọc lệch về phía nào đã chọn dấu ; cần lập luận trước rồi mới viết công thức."),
           (r"Coi thước không đổi vì thép nở rất ít", r"Độ nở nhỏ nhưng đề hỏi đúng phần lệch nhỏ đó ; bỏ qua thì không trả lời được câu c.")]),
  buoc("Chiều dài thật của ống", "Chiều dài thật của ống bằng bao nhiêu mét?", float(L_THAT), "m", 0.00005,
       loi=r"Chia số đọc cho $(1+\alpha\Delta t)$ — làm chiều dài thật ngắn hơn số đọc, ngược với bước trước ; hoặc lấy $\Delta t$ tính từ $0\ ^\circ\text{C}$.",
       ke=[(r"$l=l_{đọc}(1+\alpha\Delta t)$, $\Delta t$ tính từ nhiệt độ khắc vạch", True),
           (r"$l=\dfrac{l_{đọc}}{1+\alpha\Delta t}$", r"Kết quả nhỏ hơn số đọc, trái với bước trước : thước dãn thì số đọc nhỏ hơn chiều dài thật."),
           (r"$l=l_{đọc}(1+\alpha\cdot45)$", r"Vạch khắc đúng ở $20\ ^\circ\text{C}$ nên độ tăng nhiệt độ tính từ $20\ ^\circ\text{C}$, không từ $0\ ^\circ\text{C}$.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 5 ──
 dict(nhan_dang=r"Thấy <b>đong ở nhiệt độ khác</b> hoặc <b>bình đầy tới miệng rồi nóng lên</b> → nghĩ tới <b>nở khối của chất lỏng và bình</b>",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 4}, buoc=[
  buoc("Khối lượng riêng ở 35 °C", "Khối lượng riêng của dầu ở 35 °C bằng bao nhiêu kg/m³?", float(D35), "kg/m³", 0.2,
       loi=r"Nhân $D_0$ với $(1+\beta\Delta t)$ như công thức thể tích ; dầu nở ra thì khối lượng riêng phải giảm."),
  buoc("Lượng dầu nhận thiếu", "Mua 1000 L đong lúc 35 °C, người đó nhận ít hơn bao nhiêu kg so với đong lúc 20 °C?", float(M_THIEU), "kg", 0.2,
       loi=r"Lấy khối lượng nhận được làm đáp số, hoặc đổi $1000\ \text{L}$ thành $1000\ \text{m}^3$.",
       ke=[(r"$\Delta m=(D_{20}-D_{35})V$ với $V=1000\ \text{L}=1\ \text{m}^3$", True),
           (r"$\Delta m=D_{35}V$", r"Đó là khối lượng dầu nhận được, đề hỏi phần nhận ít hơn."),
           (r"$\Delta m=(D_{20}-D_{35})V$ với $V=1000\ \text{m}^3$", r"$1\ \text{m}^3=1000\ \text{L}$ nên $1000\ \text{L}$ chỉ là $1\ \text{m}^3$.")]),
  buoc("Dầu nở thêm", "Từ 20 °C lên 40 °C, thể tích dầu tăng thêm bao nhiêu mL?", float(DV_DAU_ML), "mL", 2,
       loi=r"Lấy $\Delta t$ bằng nhiệt độ cuối, hoặc lấy thể tích mới $V_0(1+\beta\Delta t)$ làm phần tăng.",
       ke=[(r"$\Delta V_{dầu}=V_0\beta\Delta t$ với $\Delta t$ tính từ lúc đổ đầy", True),
           (r"$\Delta V_{dầu}=V_0\beta t$ với $t$ là nhiệt độ cuối", r"Độ nở tính theo độ tăng nhiệt độ từ lúc dầu có thể tích $V_0$, không theo nhiệt độ cuối."),
           (r"$\Delta V_{dầu}=V_0(1+\beta\Delta t)$", r"Đó là thể tích dầu lúc nóng, không phải phần tăng thêm.")]),
  buoc("Dung tích can tăng thêm", "Dung tích can tăng thêm bao nhiêu mL?", float(DV_CAN_ML), "mL", 0.2,
       loi=r"Coi dung tích can giữ nguyên, hoặc cho rằng thép nở lấn vào trong làm dung tích giảm.",
       ke=[(r"$\Delta V_{can}=V_0\beta_{thép}\Delta t$ : dung tích nở như khối thép đặc cùng hình dạng", True),
           (r"Dung tích can giữ nguyên vì thành can mỏng", r"Mọi kích thước của can đều dãn theo thép, kể cả khoảng trống bên trong ; thành mỏng hay dày không đổi điều đó."),
           (r"Dung tích can giảm vì thép nở lấn vào phía trong", r"Thép dãn đều mọi phía nên khoảng trống bên trong cũng lớn lên, như khi phóng to cả can.")]),
  buoc("Thể tích dầu tràn", "Thể tích dầu tràn ra bằng bao nhiêu mL?", float(V_TRAN_ML), "mL", 4.5,
       loi=r"Lấy phần dầu nở làm thể tích tràn (quên can cũng nở), hoặc cộng thêm phần can nở.",
       ke=[(r"$V_{tràn}=\Delta V_{dầu}-\Delta V_{can}$", True),
           (r"$V_{tràn}=\Delta V_{dầu}$", r"Can cũng nở nên giữ thêm được một phần dầu ; phải trừ phần dung tích tăng thêm."),
           (r"$V_{tràn}=\Delta V_{dầu}+\Delta V_{can}$", r"Can nở tạo thêm chỗ chứa, làm dầu tràn ít đi chứ không nhiều thêm.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 6 ──
 dict(nhan_dang=r"Thấy <b>hai vật khác chất cùng nung nóng</b> → viết <b>kích thước từng vật theo $l_0(1+\alpha\Delta t)$</b> rồi đặt điều kiện đề cho",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Điều kiện hiệu không đổi", "Hiệu chiều dài hai thanh không đổi ở mọi nhiệt độ khi nào?",
       lua_chon=[(r"Khi cùng tăng nhiệt độ, hai thanh dãn thêm đúng bằng nhau", True),
                 (r"Khi hai thanh có cùng hệ số nở dài", r"Đồng và thép có hệ số nở khác nhau ; điều kiện phải nói về độ dãn $l_0\alpha\Delta t$, không chỉ về $\alpha$."),
                 (r"Khi hai thanh dài bằng nhau", r"Hai thanh bằng nhau thì hiệu bằng $0$, không phải $5\ \text{cm}$ ; dài bằng nhau mà khác $\alpha$ thì dãn khác nhau.")],
       loi=r"Nghĩ chỉ cần cùng chất (cùng $\alpha$) ; thật ra độ dãn còn tỉ lệ với chiều dài ban đầu."),
  buoc("Chiều dài hai thanh", "Chiều dài thanh đồng ở 0 °C bằng bao nhiêu cm?", float(L_CU), "cm", 0.05,
       loi=r"Viết tỉ lệ thuận $\dfrac{l_{Cu}}{l_{Fe}}=\dfrac{\alpha_{Cu}}{\alpha_{Fe}}$, cho thanh có $\alpha$ lớn dài hơn — khi đó thanh đó dãn nhiều hơn, hiệu thay đổi.",
       ke=[(r"$l_{Cu}\alpha_{Cu}=l_{Fe}\alpha_{Fe}$ kết hợp hiệu chiều dài, thanh có $\alpha$ lớn hơn là thanh ngắn hơn", True),
           (r"$\dfrac{l_{Cu}}{l_{Fe}}=\dfrac{\alpha_{Cu}}{\alpha_{Fe}}$ kết hợp hiệu chiều dài", r"Tỉ lệ ngược : thanh dài hơn lại có $\alpha$ lớn hơn thì dãn nhiều hơn hẳn, hiệu không giữ nguyên."),
           (r"$l_{Cu}\alpha_{Cu}=l_{Fe}\alpha_{Fe}$ và coi thanh đồng dài hơn thanh thép $5\ \text{cm}$", r"Thay vào sẽ ra chiều dài âm : thanh có $\alpha$ lớn hơn phải ngắn hơn mới dãn bằng thanh kia.")]),
  buoc("Phần chênh giảm sau mỗi độ", "Mỗi khi tăng thêm 1 °C, phần chênh (đường kính cầu − đường kính lỗ) giảm bao nhiêu µm? (1 µm = 10⁻⁴ cm)", float(RATE_UM), "µm", 0.01,
       loi=r"Cho lỗ hẹp lại khi nung vì nhôm nở lấn vào trong, hoặc quên cầu thép cũng nở.",
       ke=[(r"Lỗ nở theo $\alpha_{Al}$ như miếng nhôm đặc, cầu nở theo $\alpha_{Fe}$ ; lấy hiệu hai độ tăng đường kính", True),
           (r"Chỉ tính lỗ nở theo $\alpha_{Al}$, coi cầu giữ nguyên", r"Cầu thép cũng nóng lên cùng nhiệt độ nên cũng nở, làm phần chênh giảm chậm hơn."),
           (r"Lỗ hẹp lại theo $\alpha_{Al}$ vì nhôm nở lấn vào trong", r"Vòng dãn đều mọi phía như phóng to cả vòng ; lỗ rộng ra như một đĩa nhôm đặc cùng cỡ.")]),
  buoc("Độ tăng nhiệt độ", "Cần tăng nhiệt độ thêm bao nhiêu °C thì cầu vừa lọt?", float(DT6), "°C", 1,
       loi=r"Chỉ cho vòng nở (quên cầu nở), hoặc đổi chỗ hệ số nở của nhôm và thép.",
       ke=[(r"Cho hai đường kính lúc nung bằng nhau : $d_{lỗ}(1+\alpha_{Al}\Delta t)=d_{cầu}(1+\alpha_{Fe}\Delta t)$", True),
           (r"$\Delta t=\dfrac{d_{cầu}-d_{lỗ}}{d_{lỗ}\alpha_{Al}}$", r"Bỏ quên cầu thép cũng nở ; nhiệt độ tìm được thấp quá, cầu chưa lọt."),
           (r"$d_{lỗ}(1+\alpha_{Fe}\Delta t)=d_{cầu}(1+\alpha_{Al}\Delta t)$", r"Đổi chỗ hệ số : vòng là nhôm, cầu là thép ; viết như vậy ra $\Delta t$ âm, cầu không bao giờ lọt.")]),
  buoc("Nhiệt độ nung", "Nhiệt độ nung t bằng bao nhiêu °C?", float(T6), "°C", 1,
       loi=r"Lấy luôn $\Delta t$ làm nhiệt độ nung, quên nhiệt độ ban đầu của vòng và cầu.",
       ke=[(r"$t=t_0+\Delta t$ với $t_0$ là nhiệt độ lúc đo hai đường kính", True),
           (r"$t=\Delta t$", r"$\Delta t$ là độ tăng nhiệt độ ; vòng và cầu bắt đầu từ nhiệt độ ban đầu chứ không từ $0\ ^\circ\text{C}$."),
           (r"$t=\Delta t-t_0$", r"Nung nóng thì nhiệt độ tăng thêm $\Delta t$ so với lúc đầu, phải cộng chứ không trừ.")]),
  buoc("Kiểm tra")]),
]


# KaTeX: chỉ số dưới có dấu tiếng Việt → \text{…} (V_{tràn} → V_{\text{tràn}})
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
    def khac(a, b, tol):                      # cách sai cho kết quả nằm NGOÀI dung sai của đáp án đúng
        return abs(float(a) - float(b)) > tol
    # D4
    assert DL_RAY_MM == 6 and DL_CAU_CM == 24 and L_THAT == F(20006, 10000)
    assert khac(L_RAY * A_FE * T_MAX * 1000, DL_RAY_MM, 0.05)                 # Δt từ 0 °C
    assert khac(L_RAY * A_FE * (T_MAX - T_LAP), DL_RAY_MM, 0.05)              # quên đổi m → mm
    assert khac(L_CAU * A_FE * T_C1 * 100, DL_CAU_CM, 0.2)                    # α·t cuối
    assert khac(L_CAU * (1 + A_FE * (T_C1 - T_C0)) * 100, DL_CAU_CM, 0.2)     # lấy chiều dài lúc nóng
    assert L_THAT > L_DOC                                                     # thước nóng → đọc thiếu
    assert khac(F(L_DOC) / (1 + A_FE * (T_DO - T_KHAC)), L_THAT, 0.00005)     # chia thay vì nhân
    assert khac(L_DOC * (1 + A_FE * T_DO), L_THAT, 0.00005)                   # Δt từ 0 °C
    assert khac(L_DOC * (1 - A_FE * (T_DO - T_KHAC)), L_THAT, 0.00005)
    assert DL_CAU_CM * 10 == 40 * DL_RAY_MM                                   # kiểm tra câu b
    # D5
    assert D35 == F(160000, 203) and abs(float(D35) - 788.18) < 0.005
    assert abs(float(M_THIEU) - 11.82) < 0.005 and abs(float(V_THIEU_L) - 14.78) < 0.005
    assert khac(D20 * (1 + BETA * 15), D35, 0.2) and khac(D20 / (1 + BETA * 35), D35, 0.2)
    assert khac(D35 * 1, M_THIEU, 0.2) and khac((D20 - D35) * 1000, M_THIEU, 0.2)
    assert DV_DAU_ML == 400 and DV_CAN_ML == F(144, 10) and V_TRAN_ML == F(3856, 10)
    assert khac(V_CAN * BETA * T_CAN * 1000, DV_DAU_ML, 2) and khac(V_CAN * (1 + BETA * 20) * 1000, DV_DAU_ML, 2)
    assert khac(0, DV_CAN_ML, 0.2) and khac(-DV_CAN_ML, DV_CAN_ML, 0.2)
    assert khac(DV_DAU_ML, V_TRAN_ML, 4.5) and khac(DV_DAU_ML + DV_CAN_ML, V_TRAN_ML, 4.5)
    assert abs(float(V_TRAN_ML) - 390) < 4.5                                   # 0,39 L được chấm đúng
    # D6
    assert L_CU == 12 and L_FE == 17 and L_CU * A_CU == L_FE * A_FE
    k = F(HIEU) / (17 - 12); assert khac(17 * k, L_CU, 0.05)                    # tỉ lệ thuận → l_Cu = 17
    assert A_CU * HIEU / (A_FE - A_CU) < 0                                    # coi đồng dài hơn → l_Fe âm
    assert RATE_UM == F(5976, 10000)
    assert khac(D_LO * A_AL * 10**4, RATE_UM, 0.01) and khac((D_LO * A_AL + D_CAU * A_FE) * 10**4, RATE_UM, 0.01)
    assert abs(float(DT6) - 167.34) < 0.01 and abs(float(T6) - 187.34) < 0.01
    assert D_LO * (1 + A_AL * DT6) == D_CAU * (1 + A_FE * DT6)
    assert khac((D_CAU - D_LO) / (D_LO * A_AL), DT6, 1)                        # quên cầu nở
    assert D_LO * A_FE - D_CAU * A_AL < 0                                      # đổi chỗ hệ số → Δt âm
    assert khac(DT6, T6, 1) and khac(DT6 - 20, T6, 1)
    # lựa chọn ĐÚNG của mọi bước không chứa đáp số của bước đó (không lộ)
    for s in STEPS:
        for bb in s["buoc"]:
            if "dap_so" in bb and bb["dap_so"] >= 10:
                v = f"{bb['dap_so']:.1f}".rstrip("0").rstrip(".").replace(".", "{,}")
                for ch in bb.get("chon_buoc_ke", []) + [{"text": bb.get("hoi", "")}, {"text": bb["tieu_de"]}, {"text": bb.get("loi_hay_gap", "")}]:
                    assert v not in ch["text"], (bb["tieu_de"], v)
    for n, s in enumerate(STEPS):
        assert s["cap_do"] in (3, 4) and len(s["buoc"]) == SOLS[n].count('class="bt-step"'), n
    print("btm164_d456: kiểm số liệu đạt")


if __name__ == "__main__":
    kiem_so()
