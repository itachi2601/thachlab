"""Bài tập mẫu Chuyên đề 05 "Công suất điện, định luật Joule–Lenz" (khoá Vật lí HSG & chuyên, KHTN 9) — lesson_id 165.
Nguồn: content/hsg9/cd05-cong-suat-dien-joule-lenz/nguon.md (mục C dạng bài, D ví dụ, E tự luyện, G nâng cao; đã tự giải lại từng bài).
YCCĐ "bài tương tự": topic của KHTN 9 bài 91 (id 93, 94) và lớp 11 bài 25 (id 193, 194) — xem trường `topic` từng dạng.
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-165.py   (idempotent; không ghi DB)

Điểm sửa so với nguồn (đã dò lại bằng Python, xem kiem_so() ở cuối):
 - G4 (aptomat + dây): nguồn kết luận "aptomat 32 A và dây 6 mm² (dòng cho phép 30 A)" — tự mâu thuẫn: S ≥ 32/5 = 6,4 mm² > 6 mm², và aptomat 32 A
   vượt dòng cho phép 30 A của dây 6 mm². Dãy dây đề cho (1,5 – 6 mm²) không có cỡ phù hợp → đáp án đúng là TÁCH NHÁNH RIÊNG cho bình nóng lạnh.
 - G3(e): "đun 1 kg nước với hiệu suất 80% mất 7 phút" mâu thuẫn với D6 cùng nguồn (1 kg, cùng bếp: 9 phút, H ≈ 62,2%): đun ít nước thì H giảm.
   Dạng 3 dùng đúng số D6 và dựng mô hình tổn hao (nhiệt dung ấm + công suất toả ra môi trường) để dự đoán lại.
 - Mục "Lưu ý" của Dạng 6 nguồn: "hai giá trị R đối xứng qua R₀ (2 Ω và 8 Ω)" — không đối xứng theo hiệu (4−2 ≠ 8−4), mà theo tích R₁·R₂ = R₀².
 - G2: cách khắc phục "mắc nối tiếp mỗi đèn với một điện trở phù hợp" mơ hồ; Dạng 4 làm rõ bằng điện trở mắc SONG SONG với đèn có dòng định mức nhỏ.
Mọi đáp số được tự tính lại bằng Python ở cuối file (assert) trước khi ghi."""
import json, math, os, sys
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

J = os.path.join(HERE, "165.json")
NOTE = "Hình minh hoạ, không đúng tỉ lệ."
GREY = "#94a3b8"
YEL = "#fbbf24"

import re as _re
def rich(s, size=13):
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

def R(x, y, w, h, c="currentColor", sw=2, fill="none", rx=0, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{c}" '
            f'stroke-width="{sw}"{d} opacity="{op}"/>')

def circ(x, y, r, c="currentColor", sw=2, fill="none"):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{c}" stroke-width="{sw}"/>'

def lamp(x, y, c, r=13):
    d = r * 0.7071
    return circ(x, y, r, c, 2.4) + seg(x - d, y - d, x + d, y + d, c, 2) + seg(x - d, y + d, x + d, y - d, c, 2)

def battery(x, y):
    """Pin trên dây dọc tại x, tâm y; cực dương (vạch dài) ở trên."""
    return (seg(x, y - 22, x, y - 6) + seg(x - 12, y - 6, x + 12, y - 6, "currentColor", 2.4)
            + seg(x - 7, y + 2, x + 7, y + 2, "currentColor", 4) + seg(x, y + 2, x, y + 22))

def anim(attr, vals, dur):
    return f'<animate attributeName="{attr}" values="{";".join(str(v) for v in vals)}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>'

def thermo(x, y0, h, f1, dur, c, lo="20 °C", hi="100 °C", w=22):
    """Nhiệt kế: cột chất lỏng dâng từ đáy lên tới tỉ lệ f1 trong dur giây (chạy MỘT lần khi bấm)."""
    yb = y0 + h
    ys = [round(yb - 2, 1), round(yb - h * f1, 1)]; hs = [2, round(h * f1, 1)]
    b = R(x, y0, w, h, "currentColor", 2.4, "none", 8)
    b += (f'<rect x="{x + 4}" y="{ys[0]}" width="{w - 8}" height="{hs[0]}" fill="{c}" stroke="none">'
          f'{anim("y", ys, dur)}{anim("height", hs, dur)}</rect>')
    b += txt(x + w + 6, yb + 4, lo, "currentColor", 12, "start", "400") + txt(x + w + 6, y0 + 10, hi, "currentColor", 12, "start", "400")
    return b

def curve_pts(U, R0, X, Y, r0=0.5, r1=30, n=60):
    return [(X(r), Y(U * U * r / (r + R0) ** 2)) for r in [r0 + (r1 - r0) * i / n for i in range(n + 1)]]


# ═════════════ HÌNH ═════════════
# ───────────── Dạng 1 · bếp 220 V–1000 W mắc vào 200 V ─────────────
def d1(kk):
    b = ""
    if kk == 0:
        K = 0.30                                     # px mỗi oát (thang chung)
        pa, pb = 1000, 1000 * (200 / 220) ** 2
        X0 = 30
        b += txt(16, 22, "Công suất của cùng một bếp", "currentColor", 13)
        b += txt(X0, 50, "Ở 220 V (định mức)", BLUE, 13) + R(X0, 58, K * pa, 24, BLUE, 2.4, BLUE, 3, "", .25)
        b += txt(X0 + K * pa + 8, 76, "1000 W", BLUE, 13)
        b += txt(X0, 112, "Ở 200 V", ORG, 13) + R(X0, 120, K * pb, 24, ORG, 2.4, "none", 3)
        b += (f'<rect x="{X0}" y="120" width="2" height="24" rx="3" fill="{ORG}" fill-opacity=".35" stroke="none">{anim("width", [2, round(K * pb, 1)], 2.5)}</rect>')
        b += txt(X0 + K * pb + 8, 138, "P' = ?", ORG, 13)
        b += seg(X0 + K * pa, 52, X0 + K * pa, 150, GREY, 1.4, "5 4", .8)
        b += txt(16, 178, "Thang chung: hai thanh vẽ cùng tỉ lệ oát", "currentColor", 12, "start", "400")
        return fig("c05-1-0", "0 0 420 190", "Hai thanh công suất của cùng một bếp, ở hiệu điện thế 220 V và 200 V",
                   b, "Mô phỏng: thanh công suất ở 200 V lớn dần cho tới giá trị thực của nó (cùng thang với thanh trên). Không ghi số cho P'.")
    X0, X1, YT, YB = 40, 330, 50, 140
    b += seg(X0, YT, 150, YT) + seg(222, YT, X1, YT) + seg(X1, YT, X1, YB) + seg(X1, YB, X0, YB) + seg(X0, YB, X0, 100) + seg(X0, 78, X0, YT)
    b += battery(X0, 89)
    b += R(150, YT - 8, 72, 16, ORG, 2.4, "none", 3) + txt(186, YT - 14, "bếp: R", ORG, 13, "middle")
    b += txt(X0 + 18, 96, "nguồn 200 V", RED, 13) + txt(186, YB + 22, "Cùng R, nhưng U' < U_{đm}", "currentColor", 12, "middle", "400")
    b += R(236, 70, 86, 56, "currentColor", 1.6, "none", 6, "5 4", .8) + txt(279, 88, "Nhãn bếp:", "currentColor", 12, "middle", "400") + txt(279, 104, "220 V", "currentColor", 12, "middle") + txt(279, 120, "1000 W", "currentColor", 12, "middle")
    return fig("c05-1-2", "0 0 420 176", "Bếp ghi 220 V–1000 W mắc vào nguồn 200 V",
               b, "Dữ kiện: bảng ghi ở hình là số định mức ; nguồn thực tế chỉ 200 V. Điện trở R của bếp tính từ số ghi. " + NOTE)


# ───────────── Dạng 2 · ấm 220 V–1200 W đun 1,5 kg nước, H = 84% ─────────────
def d2(kk):
    b = ""
    if kk == 0:
        b += thermo(40, 18, 130, 1.0, 5.0, RED)
        b += txt(120, 60, "Ấm 220 V – 1200 W", "currentColor", 14) + txt(120, 84, "1,5 kg nước", "currentColor", 13, "start", "400")
        b += txt(120, 108, "Hiệu suất 84%", "currentColor", 13, "start", "400") + txt(120, 140, "t = ?", RED, 14)
        return fig("c05-2-0", "0 0 420 186", "Nhiệt kế chỉ nhiệt độ nước tăng từ 20 độ đến 100 độ C trong ấm điện",
                   b, "Mô phỏng: nước nóng dần từ 20 °C đến 100 °C (1 s mô phỏng ứng với khoảng 100 s thật). Chưa ghi thời gian đun.")
    X0, W = 40, 300
    b += txt(16, 22, "Điện năng A = P·t chia làm hai phần", "currentColor", 13)
    b += R(X0, 40, W, 34, "currentColor", 2.4)
    b += R(X0, 40, 0.84 * W, 34, BLUE, 2.4, BLUE, 0, "", .25) + R(X0 + 0.84 * W, 40, 0.16 * W, 34, ORG, 2.4, ORG, 0, "", .25)
    b += txt(X0 + 0.42 * W, 62, "Q_{ích} = mcΔt", BLUE, 13, "middle") + txt(X0 + 0.92 * W, 62, "hao", ORG, 12, "middle")
    b += txt(X0, 96, "A: điện năng tiêu thụ", "currentColor", 13) + txt(X0 + 0.92 * W, 96, "16%", ORG, 13, "middle")
    b += txt(X0, 130, "Muốn tìm thời gian: Q_{ích} → A → t", "currentColor", 12, "start", "400")
    return fig("c05-2-2", "0 0 420 150", "Thanh điện năng A gồm phần nhiệt có ích 84 phần trăm và phần hao phí 16 phần trăm",
               b, "Dữ kiện: 84% điện năng thành nhiệt có ích (làm nóng nước), phần còn lại hao phí. Độ dài các phần vẽ đúng tỉ lệ 84 : 16.")


# ───────────── Dạng 3 · hai lần đun: 3 kg / 21 phút và 1 kg / 9 phút ─────────────
def d3(kk):
    b = ""
    if kk == 0:
        b += txt(16, 20, "Cùng bếp, cùng ấm, cùng 20 °C → 100 °C", "currentColor", 13)
        b += thermo(50, 36, 120, 1.0, 4.2, BLUE) + txt(40, 196, "3 kg: 21 phút", BLUE, 13)
        b += thermo(250, 36, 120, 1.0, 1.8, ORG) + txt(240, 196, "1 kg: 9 phút", ORG, 13)
        return fig("c05-3-0", "0 0 420 206", "Hai nhiệt kế: đun 3 kg nước mất 21 phút, đun 1 kg nước mất 9 phút",
                   b, "Mô phỏng: hai lần đun chạy cùng lúc, nhanh 300 lần (1 s = 5 phút thật): lần 1 mất 4,2 s, lần 2 mất 1,8 s.")
    K = 0.24
    b += txt(16, 20, "Điện năng của mỗi lần: nhiệt có ích + hao phí", "currentColor", 13)
    qa, ha = 1008, 252
    qb, hb = 336, 204
    b += txt(16, 50, "Lần 1 (3 kg, 21 phút)", BLUE, 12) + R(30, 56, K * qa, 24, BLUE, 2.4, BLUE, 0, "", .25) + R(30 + K * qa, 56, K * ha, 24, ORG, 2.4, ORG, 0, "", .25)
    b += txt(16, 106, "Lần 2 (1 kg, 9 phút)", ORG, 12) + R(30, 112, K * qb, 24, BLUE, 2.4, BLUE, 0, "", .25) + R(30 + K * qb, 112, K * hb, 24, ORG, 2.4, ORG, 0, "", .25)
    b += txt(30 + K * qa / 2, 73, "Q_{ích}", BLUE, 12, "middle") + txt(30 + K * (qa + ha / 2), 73, "hao phí", ORG, 12, "middle")
    b += txt(30 + K * qb / 2, 129, "Q_{ích}", BLUE, 12, "middle") + txt(30 + K * (qb + hb / 2), 129, "hao phí", ORG, 12, "middle")
    b += txt(16, 162, "Hao phí = nhiệt làm nóng ấm + nhiệt toả ra môi trường", "currentColor", 12, "start", "400")
    return fig("c05-3-2", "0 0 420 176", "Hai thanh điện năng của hai lần đun, mỗi thanh gồm phần nhiệt có ích và phần hao phí",
               b, "Dữ kiện: độ dài thanh vẽ đúng tỉ lệ điện năng P·t của mỗi lần (A = P·t, P = 1000 W) ; phần xanh là nhiệt có ích mcΔt.")


# ───────────── Dạng 4 · hai đèn 12 V–6 W và 12 V–12 W nối tiếp vào 24 V ─────────────
def d4(kk):
    X0, X1, YT, YB = 40, 360, 56, 140
    b = ""
    w1 = seg(X0, YT, 96, YT) + seg(144, YT, 232, YT) + seg(280, YT, X1, YT)       # dây trên: pin — Đ₁ — Đ₂ — pin
    b += w1 + seg(X1, YT, X1, YB) + seg(X1, YB, X0, YB) + seg(X0, YB, X0, 112) + seg(X0, 66, X0, YT)
    b += battery(X0, 89) + txt(X0 + 8, 130, "24 V", RED, 13)
    b += lamp(120, YT, RED, 24) + lamp(256, YT, BLUE, 24)
    b += txt(120, YT - 36, "Đ_{1}: 12 V – 6 W", RED, 14, "middle") + txt(256, YT - 36, "Đ_{2}: 12 V – 12 W", BLUE, 14, "middle")
    if kk == 0:
        for xx, rr, c in ((120, 22, YEL), (256, 10, YEL)):
            b += (f'<circle cx="{xx}" cy="{YT}" r="2" fill="{c}" fill-opacity="0" stroke="none">{anim("r", [2, rr + 14], 2.0)}{anim("fill-opacity", [0, 0.5], 2.0)}</circle>')
        b += txt(200, 178, "Hai đèn sáng lên khi đóng mạch", "currentColor", 12, "middle", "400")
        return fig("c05-4-0", "0 0 420 190", "Hai đèn có số ghi khác nhau mắc nối tiếp vào nguồn 24 V, độ sáng mỗi đèn khác nhau",
                   b, "Mô phỏng: quầng sáng vẽ đúng thứ tự độ sáng thực tế của hai đèn khi nối tiếp vào 24 V (không ghi số).")
    b += seg(76, YT, 76, 100, GREY, 1.6, "5 4") + seg(164, YT, 164, 100, GREY, 1.6, "5 4") + seg(76, 100, 100, 100, GREY, 1.6, "5 4") + seg(140, 100, 164, 100, GREY, 1.6, "5 4")
    b += R(100, 90, 40, 20, GREY, 1.8, "none", 4, "5 4", .95) + txt(120, 126, "R_x ?", GREY, 13, "middle") + txt(200, 178, "Câu c: R_x mắc song song với Đ₁", "currentColor", 12, "middle", "400")
    return fig("c05-4-2", "0 0 420 190", "Mạch nối tiếp hai đèn vào nguồn 24 V, có chỗ dành cho điện trở R_x song song với đèn thứ nhất",
               b, "Dữ kiện: số ghi định mức của hai đèn và nguồn 24 V ; nét đứt là chỗ mắc điện trở phụ ở câu c. " + NOTE)


# ───────────── Dạng 5 · R₀ = 6 Ω nối tiếp biến trở, U = 24 V ─────────────
def d5(kk):
    b = ""
    if kk == 0:
        OX, OY, KR, KP = 50, 190, 11.0, 6.4
        X = lambda r: OX + KR * r
        Y = lambda p: OY - KP * p
        b += seg(OX, OY, 400, OY, "currentColor", 1.8) + chevron(400, OY, 1, 0, "currentColor", 1.8, 9) + seg(OX, OY, OX, 26, "currentColor", 1.8) + chevron(OX, 26, 0, -1, "currentColor", 1.8, 9)
        b += txt(400, OY - 8, "R (Ω)", "currentColor", 13, "end") + txt(OX + 8, 30, "P_R", "currentColor", 13)
        for r in (10, 20, 30):
            b += seg(X(r), OY, X(r), OY + 5, "currentColor", 1.4) + txt(X(r), OY + 21, str(r), "currentColor", 12, "middle", "400")
        pts = curve_pts(24, 6, X, Y)
        b += poly(pts, GREY, 2.4, "", .9)
        b += ball(pts, 0, 0.08)
        b += txt(210, 70, "Biến trở trượt từ nhỏ đến lớn", "currentColor", 12, "start", "400")
        return fig("c05-5-0", "0 0 420 214", "Chấm chạy dọc đồ thị công suất trên biến trở khi giá trị biến trở tăng dần",
                   b, "Mô phỏng: chấm chạy dọc đường P_R theo R (vẽ đúng công thức) khi kéo biến trở từ nhỏ đến lớn. Trục P chưa ghi thang.")
    X0, X1, YT, YB = 40, 340, 50, 130
    b += seg(X0, YT, 100, YT) + seg(148, YT, 210, YT) + seg(300, YT, X1, YT) + seg(X1, YT, X1, YB) + seg(X1, YB, X0, YB) + seg(X0, YB, X0, 112) + seg(X0, 66, X0, YT)
    b += battery(X0, 89) + txt(X0 + 16, 94, "U = 24 V", RED, 13)
    b += R(100, YT - 8, 48, 16, BLUE, 2.4, "none", 3) + txt(124, YT - 16, "R_0 = 6 Ω", BLUE, 13, "middle")
    b += R(210, YT - 8, 90, 16, ORG, 2.4, "none", 3) + seg(222, YT + 24, 288, YT - 20, ORG, 2.4) + chevron(288, YT - 20, 66, -44, ORG, 2.4, 9)
    b += txt(255, YT + 42, "biến trở R", ORG, 13, "middle") + txt(255, YB + 26, "Tìm R để P_R lớn nhất", "currentColor", 12, "middle", "400")
    return fig("c05-5-2", "0 0 420 176", "Điện trở R0 bằng 6 ôm mắc nối tiếp với biến trở R, nguồn 24 vôn",
               b, "Dữ kiện: R₀ cố định nối tiếp với biến trở R, hiệu điện thế nguồn không đổi. " + NOTE)


# ───────────── Dạng 6 · truyền tải điện + aptomat, dây ─────────────
def d6(kk):
    b = ""
    if kk == 0:
        b += R(14, 52, 80, 60, "currentColor", 2.2, "none", 5) + txt(54, 78, "Trạm phát", "currentColor", 13, "middle") + txt(54, 98, "60 kW", "currentColor", 13, "middle", "400")
        b += R(326, 52, 80, 60, "currentColor", 2.2, "none", 5) + txt(366, 78, "Nơi dùng", "currentColor", 13, "middle")
        for y in (68, 96):
            b += (f'<line x1="94" y1="{y}" x2="326" y2="{y}" stroke="{ORG}" stroke-width="2.6" stroke-dasharray="8 8">{anim("stroke-dashoffset", [0, -64], 2.5)}</line>')
        b += txt(210, 130, "Đường dây: R = 8 Ω (cả hai dây)", "currentColor", 12, "middle", "400")
        b += txt(210, 150, "Điện chạy từ trạm tới nơi dùng", "currentColor", 12, "middle", "400")
        return fig("c05-6-0", "0 0 420 160", "Trạm phát truyền điện năng tới nơi dùng qua hai dây dẫn có điện trở 8 ôm",
                   b, "Mô phỏng: dòng điện chạy từ trạm tới nơi dùng qua đường dây có điện trở R.")
    b += txt(16, 20, "Nhánh mạch 220 V", "currentColor", 13)
    b += R(20, 36, 70, 26, RED, 2.2, "none", 4) + txt(55, 54, "aptomat ?", RED, 12, "middle")
    b += seg(90, 49, 400, 49) + seg(20, 49, 14, 49) + seg(14, 49, 14, 150) + seg(14, 150, 400, 150) + seg(400, 49, 400, 150)
    for lab, x in (("bếp", 130), ("nồi cơm", 210), ("bàn là", 290), ("8 đèn", 360)):
        b += seg(x, 49, x, 82) + R(x - 30, 82, 60, 36, BLUE, 2, "none", 3) + txt(x, 105, lab, BLUE, 12, "middle", "400") + seg(x, 118, x, 150)
    b += txt(16, 176, "Dây dẫn: tiết diện ? (J ≤ 5 A/mm²)", "currentColor", 12, "start", "400")
    return fig("c05-6-2", "0 0 420 188", "Nhánh mạch nhà 220 vôn gồm aptomat nối tiếp rồi bốn nhóm thiết bị mắc song song",
               b, "Dữ kiện: các thiết bị mắc song song vào nhánh, aptomat và dây dẫn mắc nối tiếp ở đầu nhánh. " + NOTE)


BUILD = [d1, d2, d3, d4, d5, d6]


# ═════════════ ĐỀ CÁC DẠNG (dễ → khó) ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Công suất định mức và công suất thực tế: bếp mắc vào hiệu điện thế thấp hơn định mức",
      topic="Công suất điện của dụng cụ và số ghi trên thiết bị",
      problem_html=r"""<p>Một bếp điện ghi $220\ \text{V}-1000\ \text{W}$. Do đường dây yếu, hiệu điện thế ở ổ cắm chỉ còn $200\ \text{V}$. Coi điện trở của bếp không đổi.</p><ol type="a"><li>Tính điện trở của bếp và cường độ dòng điện khi bếp làm việc ở đúng định mức.</li><li>Tính công suất thực tế của bếp ở $200\ \text{V}$, rồi so với công suất định mức (tính theo phần trăm).</li><li>Tính nhiệt lượng bếp toả ra trong $10$ phút ở $200\ \text{V}$.</li></ol>"""),
 dict(label="Dạng 2 · Cơ bản · Hiệu suất bếp, ấm: nhiệt lượng có ích, điện năng, thời gian đun, tiền điện",
      topic="Tính điện năng tiêu thụ và tiền điện",
      problem_html=r"""<p>Một ấm điện ghi $220\ \text{V}-1200\ \text{W}$ đun $1{,}5\ \text{kg}$ nước từ $20\ ^\circ\text{C}$ đến sôi ($100\ ^\circ\text{C}$), hiệu suất của ấm là $84\%$. Cho $c_{nước}=4200\ \text{J/(kg·K)}$; giá điện $3000$ đồng/kWh.</p><ol type="a"><li>Tính nhiệt lượng có ích và điện năng ấm tiêu thụ.</li><li>Tính thời gian đun (ở đúng $220\ \text{V}$) và tiền điện của một lần đun.</li><li>Nếu hiệu điện thế chỉ còn $200\ \text{V}$ (điện trở ấm không đổi, hiệu suất vẫn $84\%$) thì thời gian đun là bao lâu?</li></ol>"""),
 dict(label="Dạng 3 · Nâng cao · Tổn hao khi đun nước: hai lần đun, tìm công suất toả ra môi trường và nhiệt dung của ấm",
      topic="Hiệu suất nguồn điện, an toàn điện",
      problem_html=r"""<p>Một bếp $220\ \text{V}-1000\ \text{W}$ (luôn ở đúng định mức) đun nước trong một ấm, từ $20\ ^\circ\text{C}$ đến $100\ ^\circ\text{C}$. Lần 1 đun $3\ \text{kg}$ nước mất $21$ phút. Lần 2 đun $1\ \text{kg}$ nước mất $9$ phút. Cho $c_{nước}=4200\ \text{J/(kg·K)}$.</p><p>Giả sử hao phí gồm hai phần: nhiệt làm nóng ấm (ấm có nhiệt dung $C$ không đổi, nóng từ $20\ ^\circ\text{C}$ đến $100\ ^\circ\text{C}$ ở mỗi lần) và nhiệt toả ra môi trường với công suất $p$ không đổi trong suốt thời gian đun.</p><ol type="a"><li>Tính hiệu suất của mỗi lần đun.</li><li>Tìm $p$ và $C$.</li><li>Dự đoán thời gian đun $2\ \text{kg}$ nước.</li></ol>"""),
 dict(label="Dạng 4 · Nâng cao · Hai đèn định mức mắc nối tiếp: độ sáng, dòng tối đa, điện trở phụ",
      topic="Công suất điện của dụng cụ và số ghi trên thiết bị",
      problem_html=r"""<p>Đèn $Đ_1$ ghi $12\ \text{V}-6\ \text{W}$, đèn $Đ_2$ ghi $12\ \text{V}-12\ \text{W}$. Coi điện trở mỗi đèn không đổi.</p><ol type="a"><li>Mắc nối tiếp hai đèn vào nguồn $24\ \text{V}$. Tính công suất thực tế của mỗi đèn. Đèn nào sáng quá định mức, đèn nào yếu hơn định mức?</li><li>Hiệu điện thế lớn nhất đặt vào hai đèn mắc nối tiếp để không đèn nào vượt định mức là bao nhiêu?</li><li>Với nguồn $24\ \text{V}$, để cả hai đèn sáng đúng định mức, người ta mắc thêm điện trở $R_x$ song song với $Đ_1$ (cụm đó nối tiếp với $Đ_2$). Tính $R_x$ và công suất tiêu thụ trên $R_x$.</li></ol>"""),
 dict(label="Dạng 5 · Nâng cao · Cực đại công suất trên biến trở: giá trị R, công suất cực đại, hiệu suất",
      topic="Công và công suất của nguồn điện",
      problem_html=r"""<p>Điện trở $R_0=6\ \Omega$ mắc nối tiếp với biến trở $R$, đặt vào hiệu điện thế không đổi $U=24\ \text{V}$.</p><ol type="a"><li>Tìm $R$ để công suất tiêu thụ trên biến trở lớn nhất (chỉ dùng $(R-R_0)^2\ge0$, không dùng đạo hàm hay Cô-si) và tính $P_{max}$.</li><li>Khi đó tính công suất toàn mạch và hiệu suất của mạch (công suất có ích là công suất trên $R$).</li><li>Tìm các giá trị $R$ để $P_R=18\ \text{W}$.</li></ol>"""),
 dict(label="Dạng 6 · Vận dụng cao · Dòng điện lớn trên dây: hao phí khi truyền tải, chọn aptomat và tiết diện dây",
      topic="Hiệu suất nguồn điện, an toàn điện",
      problem_html=r"""<ol type="a"><li>Trạm phát truyền công suất $60\ \text{kW}$ qua đường dây có tổng điện trở $8\ \Omega$. Tính công suất hao phí trên dây khi truyền ở $6\ \text{kV}$, rồi khi tăng lên $12\ \text{kV}$.</li><li>Một nhánh mạch nhà $220\ \text{V}$ có bếp $1500\ \text{W}$, nồi cơm $600\ \text{W}$, bàn là $1000\ \text{W}$ và $8$ bóng LED, mỗi bóng $10\ \text{W}$, cùng hoạt động. Dãy aptomat: $6$; $10$; $16$; $20$; $25$; $32\ \text{A}$. Dãy dây đồng: $1{,}5$; $2{,}5$; $4$; $6\ \text{mm}^2$, quy ước $J\le5\ \text{A/mm}^2$ (dòng cho phép của dây $=5S$). Quy tắc chọn: $I_{làm\ việc}\lt I_{aptomat}\le5S$. Chọn aptomat và tiết diện dây nhỏ nhất thoả mãn.</li><li>Lắp thêm bình nóng lạnh $2500\ \text{W}$ vào cùng nhánh. Phương án ở câu b còn dùng được không? Nêu phương án khắc phục.</li></ol>"""),
]

# ═════════════ BẢNG PHÂN TÍCH ĐỀ ═════════════
ANALYSIS = [
 # Dạng 1
 [(r'"bếp ghi $220\ \text{V}-1000\ \text{W}$"', r"$U_{đm}=220\ \text{V}$ ; $P_{đm}=1000\ \text{W}$", r"Số ghi là giá trị định mức : $I_{đm}=\dfrac{P_{đm}}{U_{đm}}$ ; $R=\dfrac{U_{đm}^2}{P_{đm}}$"),
  (r'"coi điện trở của bếp không đổi"', r"$R$ giữ nguyên khi $U$ đổi", r"⚠ điều kiện dùng $P\propto U^2$ ; thực tế $R$ phụ thuộc nhiệt độ"),
  (r'"hiệu điện thế ở ổ cắm chỉ còn $200\ \text{V}$"', r"$U'=200\ \text{V}$", r"$P'=\dfrac{U'^2}{R}$ ; so với $P_{đm}$ theo phần trăm"),
  (r'"nhiệt lượng toả ra trong $10$ phút"', r"$t=10\ \text{phút}$", r"$Q=P't$ ; ⚠ đổi $t$ ra giây")],
 # Dạng 2
 [(r'"đun $1{,}5\ \text{kg}$ nước từ $20\ ^\circ\text{C}$ đến sôi"', r"$m=1{,}5\ \text{kg}$ ; $\Delta t=100-20=80\ ^\circ\text{C}$", r"$Q_{ích}=mc\Delta t$ với $c=4200\ \text{J/(kg·K)}$"),
  (r'"hiệu suất $84\%$"', r"$H=0{,}84$", r"$H=\dfrac{Q_{ích}}{A}$ ; ⚠ $A$ là điện năng toàn phần, lớn hơn $Q_{ích}$"),
  (r'"ấm $220\ \text{V}-1200\ \text{W}$", "thời gian đun"', r"$P=1200\ \text{W}$ ở $220\ \text{V}$", r"$t=\dfrac{A}{P}$"),
  (r'"tiền điện", "giá $3000$ đồng/kWh"', r"giá $3000$ đồng/kWh", r"đổi $A$ ra kWh : $1\ \text{kWh}=3{,}6\cdot10^6\ \text{J}$"),
  (r'"hiệu điện thế chỉ còn $200\ \text{V}$"', r"$U'=200\ \text{V}$ ; $R$ và $H$ không đổi", r"$P'=P\left(\dfrac{U'}{U}\right)^2$ ; nhiệt cần đun không đổi nên $A$ không đổi")],
 # Dạng 3
 [(r'"bếp $220\ \text{V}-1000\ \text{W}$ (luôn ở đúng định mức)"', r"$P=1000\ \text{W}$ ở cả hai lần", r"$A=Pt$ ; ⚠ công suất không đổi nên điện năng tỉ lệ với thời gian"),
  (r'"lần 1: $3\ \text{kg}$, $21$ phút ; lần 2: $1\ \text{kg}$, $9$ phút"', r"$m_1=3,\ t_1=1260\ \text{s}$ ; $m_2=1,\ t_2=540\ \text{s}$", r"$Q_{ích}=mc\Delta t$ ; $H=\dfrac{Q_{ích}}{A}$ ; $Q_{hp}=A-Q_{ích}$"),
  (r'"hao phí gồm nhiệt làm nóng ấm và nhiệt toả ra môi trường"', r"$Q_{hp}=C\Delta t+p\,t$", r"⚠ $C$ và $p$ không đổi giữa hai lần : lập hai phương trình, hai ẩn"),
  (r'"dự đoán thời gian đun $2\ \text{kg}$"', r"Cần $t$", r"$P\,t=(mc+C)\Delta t+p\,t$")],
 # Dạng 4
 [(r'"$Đ_1$: $12\ \text{V}-6\ \text{W}$ ; $Đ_2$: $12\ \text{V}-12\ \text{W}$"', r"$U_{đm}=12\ \text{V}$ ; $P_{đm1}=6\ \text{W}$ ; $P_{đm2}=12\ \text{W}$", r"$R=\dfrac{U_{đm}^2}{P_{đm}}$ ; $I_{đm}=\dfrac{P_{đm}}{U_{đm}}$"),
  (r'"mắc nối tiếp vào nguồn $24\ \text{V}$"', r"Cùng dòng $I$ ; $U=U_1+U_2$", r"⚠ nối tiếp : $I=\dfrac{U}{R_1+R_2}$, $P=I^2R$ (không phải $U^2/R$ với cả $24\ \text{V}$)"),
  (r'"hiệu điện thế lớn nhất … không đèn nào vượt định mức"', r"$I\le I_{đm1}$ và $I\le I_{đm2}$", r"$I_{max}=\min(I_{đm1},I_{đm2})$ ; $U_{max}=I_{max}(R_1+R_2)$"),
  (r'"$R_x$ song song với $Đ_1$, cả hai đèn đúng định mức"', r"$I_2=I_{đm2}$ ; $I_1=I_{đm1}$ ; $U_{x}=U_{đm}$", r"$I_x=I_2-I_1$ ; $R_x=\dfrac{U_{đm}}{I_x}$ ; $P_x=U_{đm}I_x$")],
 # Dạng 5
 [(r'"$R_0=6\ \Omega$ nối tiếp biến trở $R$, $U=24\ \text{V}$"', r"$R_0=6\ \Omega$ ; $U=24\ \text{V}$ không đổi", r"⚠ điều kiện của $R=R_0$ : một điện trở cố định nối tiếp biến trở, $U$ cả mạch không đổi"),
  (r'"công suất trên biến trở lớn nhất"', r"$P_R=I^2R=\dfrac{U^2R}{(R+R_0)^2}$", r"$(R+R_0)^2=(R-R_0)^2+4RR_0$ ; $(R-R_0)^2\ge0$"),
  (r'"công suất toàn mạch và hiệu suất"', r"$P_{toàn}=UI$ ; có ích là $P_R$", r"$H=\dfrac{P_R}{P_{toàn}}=\dfrac{R}{R+R_0}$"),
  (r'"giá trị $R$ khác cho $P_R=18\ \text{W}$"', r"$P_R=18\ \text{W}$ (nhỏ hơn $P_{max}$)", r"Giải $\dfrac{U^2R}{(R+R_0)^2}=18$ : phương trình bậc hai ; $R_1R_2=R_0^2$")],
 # Dạng 6
 [(r'"truyền $60\ \text{kW}$ … đường dây $8\ \Omega$ … $6\ \text{kV}$ rồi $12\ \text{kV}$"', r"$P=60\ \text{kW}$ ; $R=8\ \Omega$ ; $U=6$ rồi $12\ \text{kV}$", r"$I=\dfrac{P}{U}$ ; $P_{hp}=I^2R$ ; ⚠ $U$ là hiệu điện thế ở trạm, không phải độ sụt áp trên dây"),
  (r'"bếp, nồi cơm, bàn là, $8$ đèn LED cùng hoạt động"', r"$P=1500+600+1000+8\cdot10$ ; $U=220\ \text{V}$", r"Mắc song song : $P=\sum P_i$ ; $I=\dfrac{P}{U}$"),
  (r'"chọn aptomat và tiết diện dây nhỏ nhất"', r"$J\le5\ \text{A/mm}^2$ ; dãy aptomat, dãy dây", r"⚠ $I_{làm\ việc}\lt I_{apt}\le5S$ : aptomat không được vượt dòng cho phép của dây"),
  (r'"lắp thêm bình nóng lạnh $2500\ \text{W}$"', r"$P'=P+2500$", r"Tính lại $I'$ rồi so với dòng cho phép của dây ; nếu không có cỡ phù hợp thì tách nhánh")],
]

# ═════════════ LỜI GIẢI ═════════════
R1 = [r"<strong>Khái niệm:</strong> số ghi trên thiết bị là hiệu điện thế và công suất <em>định mức</em> (đạt khi mắc đúng định mức).",
      r"<strong>Công thức:</strong> $R=\dfrac{U_{đm}^2}{P_{đm}}$ ; $P'=\dfrac{U'^2}{R}=P_{đm}\left(\dfrac{U'}{U_{đm}}\right)^2$ ; $Q=P't$.",
      r"<strong>Điều kiện:</strong> $R$ không đổi ; $t$ đổi ra giây."]
R2 = [r"<strong>Khái niệm:</strong> hiệu suất là tỉ số nhiệt có ích trên điện năng tiêu thụ.",
      r"<strong>Công thức:</strong> $Q_{ích}=mc\Delta t$ ; $A=\dfrac{Q_{ích}}{H}$ ; $t=\dfrac{A}{P}$ ; $1\ \text{kWh}=3{,}6\cdot10^6\ \text{J}$.",
      r"<strong>Điều kiện:</strong> $P$ là công suất điện toàn phần ; đổi $A$ ra kWh trước khi nhân đơn giá."]
R3 = [r"<strong>Khái niệm:</strong> hao phí $=A-Q_{ích}$, gồm nhiệt làm nóng ấm và nhiệt toả ra môi trường.",
      r"<strong>Công thức:</strong> $Q_{hp}=C\Delta t+p\,t$ ; $A=Pt$ ; $P\,t=(mc+C)\Delta t+p\,t$.",
      r"<strong>Điều kiện:</strong> $C$ và $p$ không đổi giữa các lần đun (mô hình của đề)."]
R4 = [r"<strong>Khái niệm:</strong> đèn sáng đúng định mức khi dòng qua nó bằng $I_{đm}$ ; nối tiếp thì dòng chung.",
      r"<strong>Công thức:</strong> $R=\dfrac{U_{đm}^2}{P_{đm}}$ ; $I_{đm}=\dfrac{P_{đm}}{U_{đm}}$ ; $P=I^2R$ ; $U_{max}=I_{max}(R_1+R_2)$.",
      r"<strong>Điều kiện:</strong> $R$ không đổi ; nối tiếp thì $P\propto R$, song song thì dòng chia theo nhánh."]
R5 = [r"<strong>Khái niệm:</strong> công suất trên biến trở phụ thuộc $R$ : nhỏ khi $R$ rất bé hoặc rất lớn.",
      r"<strong>Công thức:</strong> $P_R=\dfrac{U^2R}{(R+R_0)^2}=\dfrac{U^2}{\frac{(R-R_0)^2}{R}+4R_0}$ ; $H=\dfrac{R}{R+R_0}$.",
      r"<strong>Điều kiện:</strong> $R_0$ cố định nối tiếp $R$ ; $U$ không đổi."]
R6 = [r"<strong>Khái niệm:</strong> hao phí trên dây là nhiệt $I^2R$ ; aptomat ngắt khi quá dòng ; dây chịu được $I\le J\cdot S$.",
      r"<strong>Công thức:</strong> $I=\dfrac{P}{U}$ ; $P_{hp}=I^2R=\dfrac{P^2R}{U^2}$ ; $I_{cho\ phép}=5S$ ; $I_{làm\ việc}\lt I_{apt}\le I_{cho\ phép}$.",
      r"<strong>Điều kiện:</strong> thiết bị mắc song song ; $U$ trong $I=P/U$ là hiệu điện thế ở đầu đường dây."]

SOLS = [
 sol(R1, [
  ("Điện trở và dòng điện định mức", [P(r"Số ghi cho $U_{đm}=220\ \text{V}$ và $P_{đm}=1000\ \text{W}$ :"), M(r"R=\dfrac{U_{đm}^2}{P_{đm}}=\dfrac{220^2}{1000}"), A(r"R=48{,}4\ \Omega"),
     M(r"I_{đm}=\dfrac{P_{đm}}{U_{đm}}=\dfrac{1000}{220}"), A(r"I_{đm}\approx4{,}55\ \text{A}")]),
  ("Công suất thực tế ở $200\\ \\text{V}$", [P(r"$R$ không đổi, hiệu điện thế mới $U'=200\ \text{V}$ :"), M(r"P'=\dfrac{U'^2}{R}=\dfrac{200^2}{48{,}4}"), A(r"P'\approx826\ \text{W}"),
     P(r"So với định mức : $\dfrac{826}{1000}\approx82{,}6\%$. Kiểm tra bằng tỉ lệ : $\left(\dfrac{200}{220}\right)^2\approx0{,}826$ ✓.")]),
  ("Nhiệt lượng trong $10$ phút", [P(r"Đổi $t=10\ \text{phút}=600\ \text{s}$ :"), M(r"Q=P't=826\cdot600"), A(r"Q\approx4{,}96\cdot10^5\ \text{J}")]),
  ("Kiểm tra", [P(r"Dòng thực tế $I'=\dfrac{U'}{R}=\dfrac{200}{48{,}4}\approx4{,}13\ \text{A}$ ; $Q=I'^2Rt\approx4{,}95\text{–}4{,}96\cdot10^5\ \text{J}$ (lệch nhẹ do làm tròn $I'$) ✓."),
     P(r"Bếp ở $200\ \text{V}$ toả nhiệt ít hơn lúc định mức ($1000\cdot600=6\cdot10^5\ \text{J}$) ✓.")])],
  [r"a) $R=48{,}4\ \Omega$ ; $I_{đm}\approx4{,}55\ \text{A}$", r"b) $P'\approx826\ \text{W}$, bằng $82{,}6\%$ định mức", r"c) $Q\approx4{,}96\cdot10^5\ \text{J}$"],
  r"Nhận dạng: thấy <strong>hiệu điện thế khác số ghi</strong> → tìm $R=U_{đm}^2/P_{đm}$ rồi tính $P'=U'^2/R$ ; thấy <strong>thời gian bằng phút</strong> → đổi ra giây."),
 sol(R2, [
  ("Nhiệt lượng có ích", [P(r"$\Delta t=100-20=80\ ^\circ\text{C}$ :"), M(r"Q_{ích}=mc\Delta t=1{,}5\cdot4200\cdot80"), A(r"Q_{ích}=504\,000\ \text{J}")]),
  ("Điện năng tiêu thụ", [P(r"Hiệu suất $84\%$ nghĩa là $84\%$ điện năng thành nhiệt có ích :"), M(r"A=\dfrac{Q_{ích}}{H}=\dfrac{504\,000}{0{,}84}"), A(r"A=600\,000\ \text{J}")]),
  ("Thời gian đun", [P(r"Công suất $1200\ \text{W}$ là công suất điện toàn phần :"), M(r"t=\dfrac{A}{P}=\dfrac{600\,000}{1200}"), A(r"t=500\ \text{s}\approx8\ \text{phút}\ 20\ \text{giây}")]),
  ("Tiền điện", [P("Đổi sang kWh trước khi nhân đơn giá :"), M(r"A=\dfrac{600\,000}{3\,600\,000}=\dfrac16\ \text{kWh}"), M(r"\text{Tiền}=\dfrac16\cdot3000"), A(r"\text{Tiền}=500\ \text{đồng}")]),
  ("Thời gian đun ở $200\\ \\text{V}$", [P(r"Nhiệt cần đun và hiệu suất không đổi nên $A=600\,000\ \text{J}$ ; chỉ công suất đổi :"), M(r"P'=P\left(\dfrac{200}{220}\right)^2=1200\cdot0{,}826\approx991{,}7\ \text{W}"),
     M(r"t'=\dfrac{A}{P'}=\dfrac{600\,000}{991{,}7}"), A(r"t'\approx605\ \text{s}\approx10\ \text{phút}\ 5\ \text{giây}")]),
  ("Kiểm tra", [P(r"$t'=t\left(\dfrac{220}{200}\right)^2=500\cdot1{,}21=605\ \text{s}$ ✓ : công suất giảm $0{,}826$ lần thì thời gian tăng $1{,}21$ lần."),
     P(r"Nếu quên hiệu suất ($t=Q_{ích}/P=420\ \text{s}$) sẽ ra ngắn hơn thực tế ✓ đã tránh.")])],
  [r"a) $Q_{ích}=504\,000\ \text{J}$ ; $A=600\,000\ \text{J}$", r"b) $t=500\ \text{s}$ ($8$ phút $20$ giây) ; tiền điện $500$ đồng", r"c) $t'\approx605\ \text{s}$ (khoảng $10$ phút $5$ giây)"],
  r"Nhận dạng: thấy <strong>hiệu suất</strong> và <strong>thời gian đun</strong> → $Q_{ích}=mc\Delta t$, chia cho $H$ ra $A$, chia cho $P$ ra $t$ ; thấy <strong>tiền điện</strong> → đổi $A$ sang kWh."),
 sol(R3, [
  ("Hiệu suất hai lần đun", [P(r"Lần 1 : $Q_1=3\cdot4200\cdot80=1\,008\,000\ \text{J}$, $A_1=1000\cdot1260=1\,260\,000\ \text{J}$, nên $H_1=\dfrac{1\,008\,000}{1\,260\,000}=80\%$."),
     P(r"Lần 2 : $Q_2=1\cdot4200\cdot80=336\,000\ \text{J}$, $A_2=1000\cdot540=540\,000\ \text{J}$ :"), M(r"H_2=\dfrac{Q_2}{A_2}=\dfrac{336\,000}{540\,000}"), A(r"H_2\approx62{,}2\%")]),
  ("Hao phí mỗi lần", [M(r"Q_{hp1}=A_1-Q_1=1\,260\,000-1\,008\,000"), A(r"Q_{hp1}=252\,000\ \text{J}"), M(r"Q_{hp2}=540\,000-336\,000=204\,000\ \text{J}"),
     P(r"Hao phí lần 1 lớn hơn nhưng hiệu suất lần 1 lại cao hơn : hao phí chiếm tỉ lệ nhỏ hơn khi đun nhiều nước.")]),
  ("Công suất toả ra môi trường", [P(r"Hai phương trình theo mô hình : $Q_{hp}=C\Delta t+p\,t$."), M(r"252\,000=80\,C+1260\,p"), M(r"204\,000=80\,C+540\,p"),
     P(r"Trừ vế với vế : $48\,000=720\,p$."), A(r"p\approx66{,}7\ \text{W}")]),
  ("Nhiệt dung của ấm", [P(r"Thế $p=\dfrac{200}{3}\ \text{W}$ vào phương trình lần 2 :"), M(r"80\,C=204\,000-540\cdot\dfrac{200}{3}=168\,000"), A(r"C=2100\ \text{J/K}")]),
  ("Thời gian đun $2\\ \\text{kg}$", [P(r"Điện năng $=$ nhiệt có ích $+$ nhiệt làm nóng ấm $+$ nhiệt toả ra môi trường :"), M(r"1000\,t=(2\cdot4200+2100)\cdot80+\dfrac{200}{3}\,t"),
     M(r"\left(1000-\dfrac{200}{3}\right)t=840\,000"), A(r"t=900\ \text{s}=15\ \text{phút}")]),
  ("Kiểm tra", [P(r"$H_3=\dfrac{2\cdot4200\cdot80}{1000\cdot900}=\dfrac{672\,000}{900\,000}\approx74{,}7\%$, nằm giữa $62{,}2\%$ ($1\ \text{kg}$) và $80\%$ ($3\ \text{kg}$) ✓."),
     P(r"Thời gian đun tăng đều theo khối lượng : $540\to900\to1260\ \text{s}$ ứng với $1\to2\to3\ \text{kg}$ ✓ (mỗi kg thêm $360\ \text{s}$).")])],
  [r"a) $H_1=80\%$ ; $H_2\approx62{,}2\%$", r"b) $p\approx66{,}7\ \text{W}$ ; $C=2100\ \text{J/K}$", r"c) $t=900\ \text{s}=15$ phút"],
  r"Nhận dạng: thấy <strong>hai lần đun, khối lượng khác nhau</strong> → hiệu suất mỗi lần, lập hao phí $=C\Delta t+p\,t$ cho hai lần rồi giải hệ."),
 sol(R4, [
  ("Điện trở của hai đèn", [P(r"Từ số ghi của mỗi đèn :"), M(r"R_1=\dfrac{12^2}{6}"), A(r"R_1=24\ \Omega"), M(r"R_2=\dfrac{12^2}{12}"), A(r"R_2=12\ \Omega")]),
  ("Công suất thực tế khi nối tiếp vào $24\\ \\text{V}$", [M(r"I=\dfrac{U}{R_1+R_2}=\dfrac{24}{36}\approx0{,}667\ \text{A}"), M(r"P_1=I^2R_1=0{,}667^2\cdot24"), A(r"P_1\approx10{,}7\ \text{W}"),
     M(r"P_2=I^2R_2\approx0{,}667^2\cdot12\approx5{,}33\ \text{W}"),
     P(r"$P_1\gt P_{đm1}=6\ \text{W}$ : $Đ_1$ sáng quá định mức, có nguy cơ cháy. $P_2\lt P_{đm2}=12\ \text{W}$ : $Đ_2$ sáng yếu.")]),
  ("Dòng điện tối đa", [P(r"Dòng định mức : $I_{đm1}=\dfrac{6}{12}=0{,}5\ \text{A}$ ; $I_{đm2}=\dfrac{12}{12}=1\ \text{A}$."), P(r"Nối tiếp thì hai đèn chung một dòng, nên dòng không được vượt dòng định mức nhỏ hơn :"), A(r"I_{max}=0{,}5\ \text{A}")]),
  ("Hiệu điện thế tối đa", [M(r"U_{max}=I_{max}(R_1+R_2)=0{,}5\cdot36"), A(r"U_{max}=18\ \text{V}")]),
  ("Dòng qua $R_x$", [P(r"$Đ_2$ sáng đúng định mức nên dòng mạch chính là $I=I_{đm2}=1\ \text{A}$ ; $Đ_1$ chỉ cần $I_{đm1}=0{,}5\ \text{A}$."), P(r"Phần dòng thừa đi qua $R_x$ :"), M(r"I_x=I-I_1=1-0{,}5"), A(r"I_x=0{,}5\ \text{A}")]),
  ("Giá trị $R_x$ và công suất trên $R_x$", [P(r"Cụm $Đ_1//R_x$ nhận đúng $12\ \text{V}$ (vì $Đ_1$ đúng định mức) :"), M(r"R_x=\dfrac{U_x}{I_x}=\dfrac{12}{0{,}5}"), A(r"R_x=24\ \Omega"), M(r"P_x=U_xI_x=12\cdot0{,}5=6\ \text{W}")]),
  ("Kiểm tra", [P(r"Cụm song song : $\dfrac{24\cdot24}{24+24}=12\ \Omega$ ; cả mạch $12+12=24\ \Omega$, $I=\dfrac{24}{24}=1\ \text{A}$ ✓."), P(r"Tổng công suất $=24\cdot1=24\ \text{W}=6+12+6$ ✓ ($Đ_1$, $Đ_2$, $R_x$).")])],
  [r"a) $P_1\approx10{,}7\ \text{W}$ (quá định mức) ; $P_2\approx5{,}33\ \text{W}$ (yếu)", r"b) $U_{max}=18\ \text{V}$", r"c) $R_x=24\ \Omega$ ; $P_x=6\ \text{W}$"],
  r"Nhận dạng: thấy <strong>đèn định mức mắc nối tiếp</strong> → dòng chung ; lấy <strong>dòng định mức nhỏ hơn</strong> làm dòng tối đa ; thấy <strong>điện trở phụ</strong> → phần dòng thừa đi qua nó."),
 sol(R5, [
  ("Công suất trên biến trở theo $R$", [P(r"Dòng chung của mạch nối tiếp :"), M(r"I=\dfrac{U}{R+R_0}"), M(r"P_R=I^2R=\dfrac{U^2R}{(R+R_0)^2}")]),
  ("Giá trị $R$ cho công suất lớn nhất", [P(r"Dùng $(R+R_0)^2=(R-R_0)^2+4RR_0$ rồi chia tử và mẫu cho $R\gt0$ :"), M(r"P_R=\dfrac{U^2}{\dfrac{(R-R_0)^2}{R}+4R_0}"),
     P(r"Vì $(R-R_0)^2\ge0$ nên mẫu số $\ge4R_0$. Dấu bằng xảy ra khi $R=R_0$ :"), A(r"R=R_0=6\ \Omega")]),
  ("Công suất cực đại", [M(r"P_{max}=\dfrac{U^2}{4R_0}=\dfrac{24^2}{4\cdot6}"), A(r"P_{max}=24\ \text{W}")]),
  ("Công suất toàn mạch và hiệu suất", [P(r"Khi $R=6\ \Omega$ : $I=\dfrac{24}{12}=2\ \text{A}$."), M(r"P_{toàn}=UI=24\cdot2=48\ \text{W}"), M(r"H=\dfrac{P_R}{P_{toàn}}=\dfrac{24}{48}"), A(r"H=50\%"),
     P(r"Một nửa điện năng toả nhiệt trên $R_0$.")]),
  ("Hai giá trị $R$ cùng một công suất", [P(r"Cho $P_R=18\ \text{W}$ :"), M(r"\dfrac{24^2R}{(R+6)^2}=18\ \Rightarrow\ 32R=(R+6)^2"), M(r"R^2-20R+36=0"), P(r"Nghiệm $R=2\ \Omega$ hoặc $R=18\ \Omega$. Giá trị khác ở câu a :"), A(r"R=18\ \Omega\ \ (\text{và}\ R=2\ \Omega)")]),
  ("Kiểm tra", [P(r"$R=2$ : $\dfrac{576\cdot2}{8^2}=18\ \text{W}$ ✓ ; $R=18$ : $\dfrac{576\cdot18}{24^2}=18\ \text{W}$ ✓."), P(r"$R_1R_2=2\cdot18=36=R_0^2$ : hai nghiệm đối xứng theo <em>tích</em>, không theo hiệu."),
     P(r"Khi $R=18\ \Omega$, $H=\dfrac{18}{24}=75\%$ cao hơn $50\%$ nhưng công suất trên $R$ thấp hơn $24\ \text{W}$ ✓.")])],
  [r"a) $R=6\ \Omega$ ; $P_{max}=24\ \text{W}$", r"b) $P_{toàn}=48\ \text{W}$ ; $H=50\%$", r"c) $R=18\ \Omega$ (và $R=2\ \Omega$)"],
  r"Nhận dạng: thấy <strong>công suất lớn nhất trên biến trở</strong> nối tiếp một điện trở → $R=R_0$, $P_{max}=U^2/4R_0$ ; thấy <strong>cùng một công suất</strong> → hai nghiệm, $R_1R_2=R_0^2$."),
 sol(R6, [
  ("Dòng trên đường dây", [P(r"Trạm truyền $P=60\ \text{kW}=60\,000\ \text{W}$ ở $U=6\ \text{kV}$ :"), M(r"I=\dfrac{P}{U}=\dfrac{60\,000}{6000}"), A(r"I=10\ \text{A}")]),
  ("Hao phí ở $6\\ \\text{kV}$", [M(r"P_{hp}=I^2R=10^2\cdot8"), A(r"P_{hp}=800\ \text{W}"), P(r"Tỉ lệ $\dfrac{800}{60\,000}\approx1{,}3\%$.")]),
  ("Hao phí ở $12\\ \\text{kV}$", [P(r"$U$ tăng $2$ lần nên $I$ giảm $2$ lần, còn $5\ \text{A}$ :"), M(r"P_{hp}=5^2\cdot8"), A(r"P_{hp}=200\ \text{W}"), P(r"Giảm $4$ lần, đúng $P_{hp}=\dfrac{P^2R}{U^2}\propto\dfrac1{U^2}$.")]),
  ("Dòng điện của nhánh nhà", [M(r"P=1500+600+1000+8\cdot10=3180\ \text{W}"), M(r"I=\dfrac{P}{U}=\dfrac{3180}{220}"), A(r"I\approx14{,}5\ \text{A}")]),
  ("Aptomat và tiết diện dây", [P(r"Aptomat nhỏ nhất lớn hơn $14{,}5\ \text{A}$ trong dãy : $16\ \text{A}$."), M(r"S\ge\dfrac{I_{apt}}{J}=\dfrac{16}{5}=3{,}2\ \text{mm}^2"), A(r"S=4\ \text{mm}^2"),
     P(r"Kiểm tra : dòng cho phép $5\cdot4=20\ \text{A}\ge16\ \text{A}$ ✓ nên aptomat ngắt trước khi dây quá nóng.")]),
  ("Dòng nhánh khi thêm bình nóng lạnh", [M(r"P'=3180+2500=5680\ \text{W}"), M(r"I'=\dfrac{5680}{220}"), A(r"I'\approx25{,}8\ \text{A}"), P(r"Vượt $20\ \text{A}$ của dây $4\ \text{mm}^2$ và vượt aptomat $16\ \text{A}$ : phương án câu b không dùng được.")]),
  ("Phương án khắc phục", [P(r"Giữ nguyên aptomat $16\ \text{A}$ thì sẽ nhảy liên tục ; đổi aptomat $32\ \text{A}$ phải có $S\ge\dfrac{32}{5}=6{,}4\ \text{mm}^2$, mà dãy dây chỉ tới $6\ \text{mm}^2$, nên aptomat $32\ \text{A}$ vượt dòng cho phép của dây."),
     P(r"Cách đúng : <strong>đi nhánh riêng cho bình nóng lạnh</strong> : $I=\dfrac{2500}{220}\approx11{,}4\ \text{A}$ ; aptomat $16\ \text{A}$ ; dây $4\ \text{mm}^2$ (dòng cho phép $20\ \text{A}$). Dây $2{,}5\ \text{mm}^2$ chỉ chịu $12{,}5\ \text{A}$, không có aptomat nào trong dãy nằm giữa $11{,}4$ và $12{,}5\ \text{A}$.")]),
  ("Kiểm tra", [P(r"Nhánh cũ giữ nguyên $3180\ \text{W}$, $14{,}5\ \text{A}\lt16\ \text{A}\le20\ \text{A}$ ✓."), P(r"Nhánh bình : $11{,}4\ \text{A}\lt16\ \text{A}\le20\ \text{A}$ ✓."),
     P(r"Hao phí truyền tải tính bằng $I^2R$ với $I=P/U$, không dùng $U^2/R$ ✓.")])],
  [r"a) $P_{hp}=800\ \text{W}$ ($6\ \text{kV}$) ; $200\ \text{W}$ ($12\ \text{kV}$)", r"b) aptomat $16\ \text{A}$ ; dây $4\ \text{mm}^2$", r"c) $I'\approx25{,}8\ \text{A}$ : không dùng được ; tách nhánh riêng cho bình nóng lạnh (aptomat $16\ \text{A}$, dây $4\ \text{mm}^2$)"],
  r"Nhận dạng: thấy <strong>truyền tải, hao phí</strong> → $I=P/U$, $P_{hp}=I^2R$ ; thấy <strong>chọn aptomat, dây</strong> → $I_{làm\ việc}\lt I_{apt}\le5S$, rồi tính ngược để kiểm lại."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC (buoc[]) ═════════════
STEPS = [
 # ── Dạng 1 ──
 dict(nhan_dang=r"Thấy <b>hiệu điện thế khác số ghi</b> → tìm $R=U_{đm}^2/P_{đm}$ rồi tính $P'=U'^2/R$.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Điện trở của bếp", "Điện trở của bếp bằng bao nhiêu?", 48.4, "Ω", 0.1,
       loi=r"Viết nhầm $R=\dfrac{P}{U^2}$ hoặc $R=\dfrac{U}{P}$ ; đơn vị của $\dfrac{U^2}{P}$ mới là ôm."),
  buoc("Công suất thực tế ở $200\\ \\text{V}$", "Công suất thực tế của bếp ở $200\\ \\text{V}$?", 826, "W", 3,
       loi=r"Giữ $P=P_{đm}$ vì cho rằng số ghi luôn đúng, hoặc cho $P$ tỉ lệ bậc nhất với $U$.",
       ke=[(r"$P'=\dfrac{U'^2}{R}$ với $R$ đã tính", True),
           (r"$P'=P_{đm}$ vì bếp vẫn là bếp ghi sẵn công suất", r"Số ghi chỉ là công suất ở đúng hiệu điện thế định mức ; ở $U'$ khác thì $P'$ khác."),
           (r"$P'=P_{đm}\cdot\dfrac{U'}{U_{đm}}$", r"Khi $R$ không đổi, $P$ tỉ lệ với bình phương hiệu điện thế chứ không tỉ lệ bậc nhất.")]),
  buoc("Nhiệt lượng trong $10$ phút", "Nhiệt lượng toả ra trong $10$ phút là bao nhiêu kJ?", 496, "kJ", 2,
       loi=r"Quên đổi phút ra giây, hoặc dùng công suất định mức thay vì công suất thực tế.",
       ke=[(r"Đổi $t$ ra giây rồi tính $Q=P't$", True),
           (r"$Q=P_{đm}t$ với $t$ đã đổi ra giây", r"Bếp đang chạy ở hiệu điện thế thấp hơn định mức nên công suất thực tế nhỏ hơn $P_{đm}$."),
           (r"$Q=P't$ với $t=10$ (phút)", r"$P$ tính bằng oát ($\text{J/s}$) nên $t$ phải tính bằng giây.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 2 ──
 dict(nhan_dang=r"Thấy <b>hiệu suất</b> và <b>thời gian đun</b> → $Q_{ích}=mc\Delta t$ → $A=Q_{ích}/H$ → $t=A/P$.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Nhiệt lượng có ích", "Nhiệt lượng có ích để đun sôi nước là bao nhiêu kJ?", 504, "kJ", 1,
       loi=r"Lấy $\Delta t=100$ thay vì $100-20$, hoặc dùng sai khối lượng."),
  buoc("Điện năng tiêu thụ", "Điện năng ấm tiêu thụ là bao nhiêu kJ?", 600, "kJ", 2,
       loi=r"Nhân $Q_{ích}$ với $H$ thay vì chia, vì nghĩ điện năng phải nhỏ hơn nhiệt có ích.",
       ke=[(r"$A=\dfrac{Q_{ích}}{H}$", True),
           (r"$A=Q_{ích}\cdot H$", r"Điện năng phải lớn hơn nhiệt có ích vì có hao phí ; nhân với $H\lt1$ làm $A$ nhỏ đi."),
           (r"$A=Q_{ích}$", r"Như vậy là bỏ hao phí ; hiệu suất $84\%$ nghĩa là $16\%$ điện năng không thành nhiệt có ích.")]),
  buoc("Thời gian đun", "Thời gian đun là bao nhiêu giây?", 500, "s", 3,
       loi=r"Lấy $t=\dfrac{Q_{ích}}{P}$ rồi quên hao phí.",
       ke=[(r"$t=\dfrac{A}{P}$ với $A$ là điện năng toàn phần", True),
           (r"$t=\dfrac{Q_{ích}}{P}$", r"Công suất của ấm là công suất điện toàn phần ; dùng $Q_{ích}$ là bỏ qua hao phí nên thời gian ra ngắn hơn thực tế."),
           (r"$t=A\cdot P$", r"Đơn vị $\text{J}\cdot\text{W}$ không phải giây ; từ $P=\dfrac{A}{t}$ suy ra $t=\dfrac{A}{P}$.")]),
  buoc("Tiền điện", "Tiền điện của một lần đun là bao nhiêu đồng?", 500, "đồng", 5,
       loi=r"Nhân thẳng số jun với đơn giá theo kWh mà quên đổi.",
       ke=[(r"Đổi $A$ sang kWh rồi nhân đơn giá", True),
           (r"Lấy $A$ tính bằng jun nhân với đơn giá", r"Đơn giá tính theo kWh ; $1\ \text{kWh}=3{,}6\cdot10^6\ \text{J}$ nên không đổi thì sai hàng triệu lần."),
           (r"Lấy $P\cdot t$ với $P$ để nguyên theo oát, $t$ theo giờ", r"Phải đổi $P$ ra kilôoát ; để oát thì kết quả lớn gấp $1000$ lần.")]),
  buoc("Thời gian đun ở $200\\ \\text{V}$", "Thời gian đun ở $200\\ \\text{V}$ là bao nhiêu giây?", 605, "s", 3,
       loi=r"Vẫn dùng $P=1200\ \text{W}$, hoặc nhân điện năng với $(U'/U)^2$ trong khi nhiệt cần đun không đổi.",
       ke=[(r"$A$ vẫn bằng $\dfrac{Q_{ích}}{H}$, chỉ công suất đổi : $t'=\dfrac{A}{P'}$", True),
           (r"$t'=\dfrac{A}{P}$ vẫn dùng công suất ghi trên ấm", r"Ở hiệu điện thế khác định mức thì công suất không còn là số ghi ; $P'=P\left(\dfrac{U'}{U}\right)^2$."),
           (r"$A'=A\left(\dfrac{U'}{U}\right)^2$", r"Nhiệt cần đun không đổi và hiệu suất không đổi nên điện năng cần dùng không đổi ; chỉ khả năng cấp công suất thay đổi.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 3 ──
 dict(nhan_dang=r"Thấy <b>hai lần đun, khối lượng khác nhau</b> → lập $Q_{hp}=C\Delta t+p\,t$ cho từng lần rồi giải hệ.",
  cap_do=3, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Hiệu suất lần đun $1\\ \\text{kg}$", "Hiệu suất của lần đun $1\\ \\text{kg}$ nước là bao nhiêu phần trăm?", 62.2, "%", 0.3,
       loi=r"Dùng nhiệt có ích của lần đun $3\ \text{kg}$ cho lần này, hoặc để thời gian theo phút khi tính điện năng."),
  buoc("Hao phí lần đun $3\\ \\text{kg}$", "Điện năng hao phí của lần đun $3\\ \\text{kg}$ là bao nhiêu kJ?", 252, "kJ", 1,
       loi=r"Tính hao phí bằng $A\cdot H$ (đó là nhiệt có ích) hoặc coi hao phí bằng nhiệt có ích.",
       ke=[(r"$Q_{hp}=A-Q_{ích}$ với $A=Pt$", True),
           (r"$Q_{hp}=A\cdot H$", r"$A\cdot H$ chính là nhiệt có ích ; hao phí là $A(1-H)$."),
           (r"$Q_{hp}=Q_{ích}$", r"Hao phí và nhiệt có ích cộng lại mới bằng điện năng ; hai số này không bằng nhau.")]),
  buoc("Công suất toả ra môi trường", "Công suất $p$ toả ra môi trường là bao nhiêu oát?", 66.7, "W", 0.5,
       loi=r"Coi hao phí hai lần bằng nhau, hoặc chia toàn bộ hao phí cho thời gian rồi cho là chỉ toả ra môi trường.",
       ke=[(r"Viết $Q_{hp}=C\Delta t+p\,t$ cho hai lần rồi trừ vế với vế", True),
           (r"Lấy $p=\dfrac{Q_{hp}}{t}$ của lần đầu", r"Như vậy bỏ sót nhiệt làm nóng ấm ; cần hai phương trình để tách $C$ và $p$."),
           (r"Cho hao phí hai lần bằng nhau vì dùng cùng một bếp", r"Hai lần có hao phí khác nhau vì thời gian đun khác nhau ; chính hiệu của chúng chứa thông tin về $p$.")]),
  buoc("Nhiệt dung của ấm", "Nhiệt dung $C$ của ấm là bao nhiêu $\\text{J/K}$?", 2100, "J/K", 20,
       loi=r"Chia toàn bộ hao phí cho độ tăng nhiệt, bỏ phần toả ra môi trường.",
       ke=[(r"Thế $p$ vào một phương trình : $C=\dfrac{Q_{hp}-p\,t}{\Delta t}$", True),
           (r"$C=\dfrac{Q_{hp}}{\Delta t}$", r"Phần toả ra môi trường $p\,t$ cũng nằm trong hao phí ; bỏ nó thì $C$ ra lớn hơn thực tế."),
           (r"$C=\dfrac{p}{\Delta t}$", r"$p$ là công suất (oát) còn $C$ là nhiệt dung ($\text{J/K}$) ; đơn vị không khớp.")]),
  buoc("Thời gian đun $2\\ \\text{kg}$", "Thời gian đun $2\\ \\text{kg}$ nước là bao nhiêu giây?", 900, "s", 5,
       loi=r"Cho thời gian tỉ lệ thuận với khối lượng, hoặc bỏ qua nhiệt làm nóng ấm và toả ra môi trường.",
       ke=[(r"Viết $Pt=(mc+C)\Delta t+p\,t$ rồi giải $t$", True),
           (r"Tỉ lệ thuận : $t=\dfrac23\cdot1260$", r"Ấm vẫn phải nóng thêm cùng một mức và môi trường vẫn lấy nhiệt nên thời gian không tỉ lệ thuận với khối lượng."),
           (r"Chỉ tính nhiệt có ích : $t=\dfrac{mc\Delta t}{P}$", r"Như vậy bỏ qua hao phí nên thời gian ra quá ngắn.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 4 ──
 dict(nhan_dang=r"Thấy <b>đèn định mức mắc nối tiếp</b> → dòng chung ; dòng tối đa là <b>dòng định mức nhỏ hơn</b>.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Điện trở của hai đèn", "Điện trở của $Đ_1$ bằng bao nhiêu?", 24, "Ω", 0.1,
       loi=r"Viết $R=\dfrac{U}{P}$ hoặc lấy số ghi $P$ làm điện trở."),
  buoc("Công suất thực tế khi nối tiếp vào $24\\ \\text{V}$", "Công suất thực tế của $Đ_1$ khi nối tiếp vào $24\\ \\text{V}$?", 10.7, "W", 0.1,
       loi=r"Cho mỗi đèn nhận một nửa hiệu điện thế nguồn, hoặc dùng $\dfrac{U^2}{R}$ với cả hiệu điện thế nguồn.",
       ke=[(r"Tìm dòng chung $I=\dfrac{U}{R_1+R_2}$ rồi $P_1=I^2R_1$", True),
           (r"Cho mỗi đèn nhận một nửa hiệu điện thế nguồn", r"Hiệu điện thế chỉ chia đều khi hai đèn có điện trở bằng nhau ; ở đây hai điện trở khác nhau."),
           (r"$P_1=\dfrac{U^2}{R_1}$ với $U$ là hiệu điện thế nguồn", r"Cả nguồn đặt vào hai đèn nối tiếp ; mỗi đèn chỉ nhận một phần của nó.")]),
  buoc("Dòng điện tối đa", "Dòng điện lớn nhất qua hai đèn nối tiếp mà không đèn nào vượt định mức?", 0.5, "A", 0.01,
       loi=r"Cộng hai dòng định mức, hoặc lấy dòng định mức lớn hơn.",
       ke=[(r"Lấy dòng định mức nhỏ hơn trong hai đèn", True),
           (r"Cộng hai dòng định mức", r"Nối tiếp thì hai đèn chung một dòng, không cộng được."),
           (r"Lấy dòng định mức lớn hơn", r"Khi đó đèn có dòng định mức nhỏ hơn bị quá tải.")]),
  buoc("Hiệu điện thế tối đa", "Hiệu điện thế lớn nhất đặt vào hai đèn nối tiếp là bao nhiêu?", 18, "V", 0.1,
       loi=r"Cộng hai hiệu điện thế định mức, trong khi hai đèn chưa chắc cùng đúng định mức.",
       ke=[(r"$U_{max}=I_{max}(R_1+R_2)$", True),
           (r"$U_{max}=U_{đm1}+U_{đm2}$", r"Tổng hai hiệu điện thế định mức chỉ đạt khi cả hai đèn cùng đúng định mức, mà điều đó cần hai dòng định mức bằng nhau."),
           (r"$U_{max}=U_{đm}$ của một đèn", r"Hai đèn nối tiếp chia hiệu điện thế nên cả cụm chịu được nhiều hơn một hiệu điện thế định mức.")]),
  buoc("Dòng qua $R_x$", "Dòng điện qua $R_x$ là bao nhiêu?", 0.5, "A", 0.01,
       loi=r"Cho $R_x$ nhận dòng định mức của $Đ_2$ hoặc cho là bằng không vì $Đ_1$ đã đủ.",
       ke=[(r"Dòng mạch chính trừ phần dòng $Đ_1$ cần", True),
           (r"Bằng dòng mạch chính", r"Dòng mạch chính chia hai nhánh ; $R_x$ chỉ nhận phần $Đ_1$ không dùng."),
           (r"Bằng không vì $Đ_1$ đã sáng đủ", r"$Đ_1$ chỉ cần một nửa dòng mạch chính ; nửa còn lại phải đi qua $R_x$.")]),
  buoc("Giá trị $R_x$ và công suất trên $R_x$", "Giá trị của $R_x$ là bao nhiêu?", 24, "Ω", 0.2,
       loi=r"Dùng hiệu điện thế của cả nguồn thay vì hiệu điện thế trên cụm song song.",
       ke=[(r"$R_x=\dfrac{U_{đm}}{I_x}$ với $U_{đm}$ là hiệu điện thế trên $Đ_1$", True),
           (r"$R_x=\dfrac{U_{nguồn}}{I_x}$", r"$R_x$ chỉ nhận hiệu điện thế của cụm song song với $Đ_1$, không phải cả nguồn."),
           (r"Mắc $R_x$ song song với $Đ_2$ thay vì $Đ_1$", r"Đèn có dòng định mức nhỏ hơn mới cần chia bớt dòng ; mắc cạnh $Đ_2$ làm nó thiếu dòng thêm.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 5 ──
 dict(nhan_dang=r"Thấy <b>công suất lớn nhất trên biến trở</b> nối tiếp điện trở cố định → $R=R_0$, $P_{max}=\dfrac{U^2}{4R_0}$.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Công suất trên biến trở theo $R$", "Biểu thức nào đúng cho công suất trên biến trở?",
       lua_chon=[(r"$P_R=\dfrac{U^2R}{(R+R_0)^2}$", True),
                 (r"$P_R=\dfrac{U^2}{R}$", r"Đó là công suất nếu cả $U$ đặt lên $R$ ; ở đây $R$ nối tiếp $R_0$ nên chỉ nhận một phần của $U$."),
                 (r"$P_R=\dfrac{U^2}{R+R_0}$", r"Đó là công suất của toàn mạch, không phải của riêng biến trở.")],
       loi=r"Dùng cả $U$ cho biến trở hoặc nhầm công suất biến trở với công suất toàn mạch."),
  buoc("Giá trị $R$ cho công suất lớn nhất", "Giá trị $R$ để công suất trên biến trở lớn nhất?", 6, "Ω", 0.1,
       loi=r"Cho $R$ rất nhỏ (dòng lớn) hoặc rất lớn (điện trở lớn) vì nghĩ công suất luôn tăng.",
       ke=[(r"Đổi $P_R$ thành $\dfrac{U^2}{\frac{(R-R_0)^2}{R}+4R_0}$ rồi xét dấu bằng", True),
           (r"Cho $R\to0$ để dòng điện lớn nhất", r"Khi $R=0$ thì $P_R=I^2R=0$ ; dòng lớn nhất làm công suất toàn mạch lớn nhất, không phải của biến trở."),
           (r"Cho $R$ thật lớn vì $P=I^2R$ tăng theo $R$", r"$R$ tăng làm $I$ giảm nhanh hơn ; $P_R$ tiến về $0$ khi $R$ rất lớn.")]),
  buoc("Công suất cực đại", "Công suất cực đại trên biến trở là bao nhiêu oát?", 24, "W", 0.2,
       loi=r"Lấy $\dfrac{U^2}{R_0}$ (cả hiệu điện thế đặt lên $R_0$) hoặc $\dfrac{U^2}{2R_0}$ (công suất toàn mạch).",
       ke=[(r"$P_{max}=\dfrac{U^2}{4R_0}$", True),
           (r"$P_{max}=\dfrac{U^2}{R_0}$", r"Đó là công suất nếu cả $U$ đặt lên $R_0$ ; nối tiếp với $R=R_0$ thì $U$ chia đôi nên công suất chỉ còn một phần tư."),
           (r"$P_{max}=\dfrac{U^2}{2R_0}$", r"Đó là công suất toàn mạch khi $R=R_0$, gồm cả phần toả ở $R_0$.")]),
  buoc("Công suất toàn mạch và hiệu suất", "Hiệu suất của mạch khi công suất trên biến trở cực đại là bao nhiêu phần trăm?", 50, "%", 0.5,
       loi=r"Cho hiệu suất $100\%$ vì nghĩ biến trở là phần có ích duy nhất, quên điện năng toả trên $R_0$.",
       ke=[(r"$H=\dfrac{P_R}{P_{toàn}}=\dfrac{R}{R+R_0}$", True),
           (r"$H=\dfrac{P_R}{U^2/R_0}$", r"$\dfrac{U^2}{R_0}$ không phải công suất toàn mạch ; toàn mạch có điện trở $R+R_0$."),
           (r"Hiệu suất bằng $1$ vì không có hao phí", r"Phần toả nhiệt trên $R_0$ cũng là điện năng không có ích ; bằng đúng phần trên $R$ khi $R=R_0$.")]),
  buoc("Hai giá trị $R$ cùng một công suất", "Trong các giá trị $R$ cho công suất nêu ở câu c, giá trị lớn hơn $R_0$ là bao nhiêu?", 18, "Ω", 0.2,
       loi=r"Lấy giá trị đối xứng qua $R_0$ theo hiệu, thay vì giải phương trình bậc hai.",
       ke=[(r"Lập $\dfrac{U^2R}{(R+R_0)^2}$ bằng công suất đó rồi giải phương trình bậc hai", True),
           (r"Lấy $R$ cách $R_0$ cùng một khoảng ở phía lớn hơn", r"Hai nghiệm không đối xứng theo hiệu mà theo tích : $R_1R_2=R_0^2$."),
           (r"Cho rằng chỉ có đúng một giá trị $R$", r"Đồ thị tăng rồi giảm nên mỗi mức công suất dưới đỉnh có hai giá trị $R$.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 6 ──
 dict(nhan_dang=r"Thấy <b>truyền tải, hao phí</b> → $I=P/U$, $P_{hp}=I^2R$ ; thấy <b>chọn aptomat, dây</b> → $I_{làm\ việc}\lt I_{apt}\le5S$.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 4}, buoc=[
  buoc("Dòng trên đường dây", "Dòng điện trên đường dây khi truyền ở $6\\ \\text{kV}$?", 10, "A", 0.1,
       loi=r"Dùng $P=60$ (kW) với $U=6000$ (V) mà không đổi cùng đơn vị."),
  buoc("Hao phí ở $6\\ \\text{kV}$", "Công suất hao phí trên dây khi truyền ở $6\\ \\text{kV}$ là bao nhiêu oát?", 800, "W", 5,
       loi=r"Dùng $\dfrac{U^2}{R}$ với $U$ của trạm : đó không phải hiệu điện thế trên dây.",
       ke=[(r"$P_{hp}=I^2R$ với $I=\dfrac{P}{U}$", True),
           (r"$P_{hp}=\dfrac{U^2}{R}$ với $U$ của trạm", r"Hiệu điện thế trên dây chỉ là độ sụt áp $I\cdot R$, nhỏ hơn nhiều $U$ của trạm."),
           (r"$P_{hp}=U\cdot I$", r"Đó là công suất của cả đường truyền, không phải phần hao phí trên dây.")]),
  buoc("Hao phí ở $12\\ \\text{kV}$", "Công suất hao phí khi truyền ở $12\\ \\text{kV}$ là bao nhiêu oát?", 200, "W", 3,
       loi=r"Cho hao phí giảm $2$ lần theo $U$, quên rằng hao phí tỉ lệ với $\dfrac{1}{U^2}$.",
       ke=[(r"$I$ giảm $2$ lần nên $P_{hp}=I^2R$ giảm $4$ lần", True),
           (r"$P_{hp}$ giảm $2$ lần vì $U$ tăng $2$ lần", r"Hao phí tỉ lệ với $I^2$ chứ không với $I$ ; $I$ giảm $2$ lần thì $I^2$ giảm $4$ lần."),
           (r"$P_{hp}$ không đổi vì công suất truyền không đổi", r"Công suất truyền không đổi nhưng dòng điện giảm nên hao phí trên dây giảm.")]),
  buoc("Dòng điện của nhánh nhà", "Dòng điện của nhánh nhà khi các thiết bị cùng hoạt động?", 14.5, "A", 0.1,
       loi=r"Quên nhân $8$ bóng LED hoặc không đổi cùng đơn vị khi tính $\dfrac{P}{U}$.",
       ke=[(r"Cộng công suất rồi chia cho $220\ \text{V}$", True),
           (r"Cộng dòng điện rồi chia thêm cho số thiết bị", r"Mắc song song thì dòng cộng lại (không chia) ; $I=\dfrac{\sum P}{U}$."),
           (r"Chỉ tính thiết bị công suất lớn nhất", r"Mọi thiết bị cùng hoạt động đều góp dòng ; bỏ sót thì chọn aptomat quá nhỏ.")]),
  buoc("Aptomat và tiết diện dây", "Tiết diện dây nhỏ nhất trong dãy cho aptomat đã chọn (mm²)?", 4, "mm²", 0.01,
       loi=r"Chọn dây theo dòng làm việc rồi gắn aptomat lớn hơn dòng cho phép của dây.",
       ke=[(r"Chọn aptomat nhỏ nhất lớn hơn dòng làm việc rồi $S\ge\dfrac{I_{apt}}{J}$", True),
           (r"$S\ge\dfrac{I}{J}$ theo dòng làm việc rồi chọn aptomat bất kỳ", r"Aptomat không được lớn hơn dòng cho phép của dây ; không thì dây nóng trước khi aptomat ngắt."),
           (r"Chọn aptomat bé nhất trong dãy cho chắc", r"Aptomat bé hơn dòng làm việc sẽ nhảy liên tục khi các thiết bị cùng chạy.")]),
  buoc("Dòng nhánh khi thêm bình nóng lạnh", "Dòng điện của nhánh sau khi thêm bình nóng lạnh?", 25.8, "A", 0.1,
       loi=r"Chỉ cộng dòng của bình rồi bỏ dòng cũ, hoặc không so lại với dòng cho phép của dây.",
       ke=[(r"Cộng công suất mới rồi chia $220\ \text{V}$, so với dòng cho phép của dây", True),
           (r"Chỉ tính dòng riêng của bình", r"Nhánh dùng chung nên dòng nhánh gồm cả thiết bị cũ lẫn bình mới."),
           (r"Giữ nguyên dòng cũ vì bình nóng lạnh dùng ít", r"Công suất bình rất lớn nên làm dòng nhánh tăng mạnh bất kể thời gian dùng.")]),
  buoc("Phương án khắc phục",
       "Phương án nào đúng?",
       lua_chon=[(r"Tách bình nóng lạnh sang nhánh riêng, dây $4\ \text{mm}^2$, aptomat $16\ \text{A}$", True),
                 (r"Giữ nhánh cũ, thay aptomat $32\ \text{A}$", r"Dây $4\ \text{mm}^2$ chỉ chịu $20\ \text{A}$ ; aptomat $32\ \text{A}$ không ngắt khi dòng tới $25\ \text{A}$ nên dây nóng chảy."),
                 (r"Giữ dây $4\ \text{mm}^2$, dùng aptomat $25\ \text{A}$", r"Dòng nhánh vượt $25\ \text{A}$ nên vẫn nhảy ; đồng thời aptomat $25\ \text{A}$ vượt dòng cho phép $20\ \text{A}$ của dây.")],
       loi=r"Chỉ nâng aptomat mà giữ dây cũ, khiến dây nóng trước khi aptomat ngắt."),
  buoc("Kiểm tra")]),
]

# ═════════════ BÀI TẬP TỰ LUẬN (còn lại của chuyên đề) ═════════════
TL = [
 ("Dễ", r"""<p>Đầu tháng công tơ điện của một gia đình chỉ $2450\ \text{kWh}$, cuối tháng chỉ $2596\ \text{kWh}$. Tính điện năng tiêu thụ trong tháng (kWh và J) và tiền điện, biết giá $2000$ đồng/kWh.</p>""",
  r"""<p>$A=2596-2450=146\ \text{kWh}=146\cdot3{,}6\cdot10^6=5{,}256\cdot10^8\ \text{J}$.</p><p>Tiền điện $=146\cdot2000=292\,000$ đồng.</p><p>Lỗi hay gặp: nhân đơn giá với số jun mà không đổi sang kWh.</p>"""),
 ("Trung bình", r"""<p>Một bóng đèn dây tóc $220\ \text{V}-60\ \text{W}$ và một bóng LED $220\ \text{V}-10\ \text{W}$ cho cùng độ sáng. Mỗi ngày dùng $5$ giờ trong $30$ ngày. Tính điện năng tiêu thụ của mỗi bóng và số tiền tiết kiệm khi dùng LED (giá $2000$ đồng/kWh).</p>""",
  r"""<p>Dây tóc : $0{,}06\cdot5\cdot30=9\ \text{kWh}$. LED : $0{,}01\cdot5\cdot30=1{,}5\ \text{kWh}$.</p><p>Tiết kiệm $7{,}5\ \text{kWh}$, tức $7{,}5\cdot2000=15\,000$ đồng.</p><p>Chỉ so sánh được vì hai bóng cho <em>cùng độ sáng</em> (cùng quang năng phát ra).</p>"""),
 ("Khó", r"""<p>Hai bóng đèn $Đ_1$: $110\ \text{V}-40\ \text{W}$ và $Đ_2$: $110\ \text{V}-100\ \text{W}$ mắc nối tiếp vào $220\ \text{V}$. Coi điện trở không đổi. Tính công suất thực tế mỗi đèn, nêu đèn nào có nguy cơ cháy.</p>""",
  r"""<p>$R_1=\dfrac{110^2}{40}=302{,}5\ \Omega$, $R_2=\dfrac{110^2}{100}=121\ \Omega$ ; $I=\dfrac{220}{423{,}5}\approx0{,}519\ \text{A}$.</p><p>$P_1=I^2R_1\approx81{,}6\ \text{W}$ (gấp hơn $2$ lần định mức, $U_1\approx157\ \text{V}$) ; $P_2\approx32{,}7\ \text{W}$ (sáng yếu).</p><p>$Đ_1$ có nguy cơ cháy. Trong mạch nối tiếp, đèn có định mức nhỏ hơn (điện trở lớn hơn) lại chịu nhiều hơn.</p>"""),
 ("Nâng cao", r"""<p>$U=18\ \text{V}$ không đổi ; $R_1=6\ \Omega$ nối tiếp với đoạn gồm $R_2=12\ \Omega$ song song biến trở $R$. Tìm $R$ để công suất trên biến trở lớn nhất, tính $P_{max}$ và hiệu suất của mạch (có ích là công suất trên biến trở).</p>""",
  r"""<p>Từ hai đầu biến trở, phần còn lại có điện trở $\dfrac{R_1R_2}{R_1+R_2}=4\ \Omega$ nên cực đại tại $R=4\ \Omega$.</p><p>Khi đó đoạn song song $3\ \Omega$, toàn mạch $9\ \Omega$, $I=2\ \text{A}$, $U_{R}=6\ \text{V}$ nên $P_{max}=\dfrac{36}{4}=9\ \text{W}$.</p><p>$P_1=24\ \text{W}$, $P_2=3\ \text{W}$, $P_{toàn}=36\ \text{W}$ nên $H=\dfrac{9}{36}=25\%$. Kiểm tra $24+3+9=36$ ✓.</p>"""),
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
    R_ = F(220**2, 1000); assert R_ == F(242, 5) and F(1000, 220) == F(50, 11)
    P2 = F(200**2) / R_; assert abs(float(P2) - 826.446) < .001 and abs(float(P2 / 1000) - 0.8264) < 1e-4
    Q = float(P2) * 600; assert abs(Q - 495868) < 1 and abs(200 / 48.4 - 4.1322) < 1e-3 and abs((200 / 48.4) ** 2 * 48.4 * 600 - Q) < 1
    # D2
    Qi = F(15, 10) * 4200 * 80; A = Qi / F(84, 100); assert (Qi, A, A / 1200) == (504000, 600000, 500)
    assert A / 3600000 * 3000 == 500 and abs(float(A / (1200 * F(200, 220) ** 2)) - 605) < 1e-9 and Qi / 1200 == 420
    # D3
    P = 1000; q1, a1 = 3 * 4200 * 80, P * 1260; q2, a2 = 4200 * 80, P * 540
    assert (F(q1, a1), q1, a1) == (F(4, 5), 1008000, 1260000) and abs(q2 / a2 - 0.6222) < 1e-4
    h1, h2 = a1 - q1, a2 - q2; assert (h1, h2) == (252000, 204000)
    p = F(h1 - h2, 1260 - 540); C = (h2 - p * 540) / 80; assert p == F(200, 3) and C == 2100 and abs(float(p) - 66.667) < 1e-3
    t3 = F((2 * 4200 + C) * 80) / (P - p); assert t3 == 900 and F(672000, 900000) == F(56, 75) and abs(56 / 75 - 0.7467) < 1e-3
    assert [(1000 * 360 * k) for k in (1, 2, 3)] == [360000, 720000, 1080000] and 540 + 360 == 900 and 900 + 360 == 1260
    # D4
    r1, r2 = F(12**2, 6), F(12**2, 12); assert (r1, r2) == (24, 12)
    I = F(24) / (r1 + r2); assert I == F(2, 3) and abs(float(I**2 * r1) - 10.667) < 1e-3 and abs(float(I**2 * r2) - 5.333) < 1e-3
    imax = min(F(6, 12), F(12, 12)); assert imax == F(1, 2) and imax * (r1 + r2) == 18
    i_, i1 = F(12, 12), F(6, 12); ix = i_ - i1; rx = F(12) / ix; assert (ix, rx, 12 * ix) == (F(1, 2), 24, 6)
    par = F(24 * 24, 48); assert par == 12 and par + 12 == 24 and F(24) / 24 == 1 and 24 * 1 == 6 + 12 + 6
    # D5
    PR = lambda R, U=24, R0=6: F(U * U * R, (R + R0) ** 2)
    assert PR(6) == 24 and F(24**2, 4 * 6) == 24 and F(24, 12) == 2 and 24 * 2 == 48 and F(24, 48) == F(1, 2)
    sol_ = [R for R in range(1, 200) if PR(R) == 18]; assert sol_ == [2, 18] and 2 * 18 == 36 == 6 * 6 and F(18, 24) == F(3, 4)
    assert max(PR(R) for R in range(1, 100)) == 24 and 576 * 2 / 64 == 18 and 576 * 18 / 576 == 18
    # D6
    assert F(60000, 6000) == 10 and 10**2 * 8 == 800 and F(800, 60000) == F(1, 75) and 5**2 * 8 == 200 and F(60000, 12000) == 5
    Pn = 1500 + 600 + 1000 + 80; assert Pn == 3180 and abs(Pn / 220 - 14.4545) < 1e-3 and F(16, 5) == F(16, 5) and 16 / 5 == 3.2
    assert 5 * 4 == 20 and 5680 / 220 > 25.8 and abs(5680 / 220 - 25.818) < 1e-3 and 32 / 5 == 6.4 > 6
    assert abs(2500 / 220 - 11.364) < 1e-3 and 5 * 2.5 == 12.5 and not any(11.364 < a <= 12.5 for a in (6, 10, 16, 20, 25, 32))
    # tự luận
    assert 2596 - 2450 == 146 and 146 * 2000 == 292000 and 146 * 3600000 == 525600000
    assert .06 * 5 * 30 == 9 and abs(.01 * 5 * 30 - 1.5) < 1e-9 and abs((9 - 1.5) * 2000 - 15000) < 1e-6
    i = 220 / (302.5 + 121); assert abs(i - .5195) < 1e-3 and abs(i * i * 302.5 - 81.6) < .05 and abs(i * i * 121 - 32.7) < .05 and abs(i * 302.5 - 157.1) < .1
    PRg = lambda R: F(18**2 * 12**2 * R, (72 + 18 * R) ** 2); assert PRg(4) == 9 and PRg(2) == PRg(8) == 8 and F(6 * 12, 18) == 4
    assert (6 + F(12 * 4, 16), F(18) / 9, F(18) / 9 * 3) == (9, 2, 6) and 2**2 * 6 == 24 and F(36, 12) == 3 and 24 + 3 + 9 == 36 and F(9, 36) == F(1, 4)
    print("kiểm số liệu: đạt")

kiem_so()

# ═════════════ GHI FILE ═════════════
write(J, 165, "Chuyên đề 05. Công suất điện, định luật Joule–Lenz", DANG, BUILD, ANALYSIS, SOLS, tu_luan())
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-12"
d["review"] = {"checked": True, "notes": "Kiểm chéo độc lập (kiem-code) 12/10/2026: tự giải 6 dạng khớp; đã sửa đề D5c, D6, hình D4/D6, lời q3/q4/VII theo báo cáo."}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
print("xong", J)
