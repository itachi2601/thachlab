"""Hình cho bài tập mẫu Bài 15 "Một số ứng dụng của cảm ứng điện từ" (Vật lí 12), lesson_id 126.
Mỗi dạng d<k>(kk): kk=0 mô phỏng chạy MỘT lần khi bấm (đặt dưới đề); kk=2 hình dữ kiện tĩnh cho phần phân tích.
Dây đàn dao động (d1), đường sức đổi chiều theo dòng xoay chiều (d2, d4), các tình huống của đề (d3) đều tính/vẽ từ dữ kiện đề;
KHÔNG vẽ dòng cảm ứng, KHÔNG vẽ điện áp thứ cấp, KHÔNG thể hiện nhiệt độ hay lực hãm. Đường sức nét đứt, đầu mũi tên chữ V 30°
(field_line của svg_lib)."""
import math, os, re as _re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *
from svg_lib import field_line

NOTE = "Hình minh hoạ, không đúng tỉ lệ."
GREY = "#94a3b8"


def rich(s, size=13):
    """`p_N` → p với chỉ số dưới N."""
    parts = _re.split(r"_([A-Za-z0-9]+)", s)
    out = parts[0]
    for i in range(1, len(parts), 2):
        out += f'<tspan dy="4" font-size="{size - 3}">{parts[i]}</tspan>'
        if parts[i + 1]:
            out += f'<tspan dy="-4">{parts[i + 1]}</tspan>'
    return out


def txt(x, y, s, c="currentColor", size=13, anchor="start", weight="700"):
    return lbl(x, y, rich(s, size), c, size, anchor, weight)


def rect(x, y, w, h, c="currentColor", sw=2, fill="none", rx=0):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{c}" stroke-width="{sw}"/>'


def pth(d, c="currentColor", sw=2, dash=""):
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{sw}"{ds}/>'


def anim(attr, vals, dur, nd=1):
    return (f'<animate attributeName="{attr}" values="{";".join(f"{v:.{nd}f}" for v in vals)}" dur="{dur:.2f}s" '
            f'begin="indefinite" fill="freeze"/>')


def alt_lines(xs, y_lo, y_hi, animate, ncyc=3, step=0.19, c=BLUE):
    """Đường sức thẳng đứng nét đứt. Nhóm A hướng lên, nhóm B hướng xuống, hiện xen kẽ như dòng xoay chiều đổi chiều.
    Khung đầu: không đường sức nào; khung cuối: nhóm A."""
    A = "".join(field_line(x, y_lo, x, y_hi, c, 1.6, "5 4", 9) for x in xs)
    B = "".join(field_line(x, y_hi, x, y_lo, c, 1.6, "5 4", 9) for x in xs)
    if not animate:
        return f'<g opacity=".9">{A}</g>'
    n = 8 * ncyc + 2
    ph = [math.sin(2 * math.pi * k / 8) for k in range(n + 1)]
    oa = [max(0, p) for p in ph]
    ob = [max(0, -p) for p in ph]
    dur = step * n
    return f'<g opacity="0">{A}{anim("opacity", oa, dur)}</g><g opacity="0">{B}{anim("opacity", ob, dur)}</g>'


def coil_row(x0, cy, n, gap, rx, ry, c=ORG):
    return "".join(f'<ellipse cx="{x0 + i * gap}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{c}" stroke-width="2"/>' for i in range(n))


# ───────────── Dạng 1 · dây La 110 Hz dao động trên bộ cảm ứng, N = 6 000 vòng ─────────────
Y0, AMP = 90, 16


def _sd(a):
    return f"M40,{Y0} Q210,{Y0 + 2 * a:.1f} 380,{Y0}"


def d1(kk):
    run = kk == 0
    b = txt(14, 20, "dây La: f = 110 Hz") + txt(14, 38, "cuộn dây: N = 6 000 vòng")
    b += txt(406, 20, "dòng cảm ứng? e_c = ?", ORG, 13, "end")
    b += seg(40, 72, 40, 112, "currentColor", 5) + seg(380, 72, 380, 112, "currentColor", 5)
    b += txt(50, 110, "dây thép", "currentColor", 11, "start", "400")
    # bộ cảm ứng: nam châm trong cuộn dây
    for yy in range(136, 200, 8):
        b += seg(165, yy, 190, yy, ORG, 1.4) + seg(230, yy, 255, yy, ORG, 1.4)
    b += rect(165, 130, 90, 70, ORG, 2) + rect(190, 118, 40, 84, "currentColor", 2)
    b += txt(210, 135, "N", RED, 12, "middle") + txt(210, 196, "S", BLUE, 12, "middle")
    b += pth("M255,184 H300", ORG, 1.8) + pth("M165,184 H140 V222 H350 V198", ORG, 1.8)
    b += rect(300, 170, 100, 28, "currentColor", 1.8, rx=4) + txt(350, 188, "Máy tăng âm", "currentColor", 11, "middle", "600")
    b += txt(210, 214, "bộ cảm ứng (pickup)", "currentColor", 11, "middle", "400")
    if run:
        T, cyc, per = 0.545, 8, 12
        vals = [_sd(-AMP * math.sin(2 * math.pi * k / per)) for k in range(cyc * per + 1)]
        b += (f'<path d="{vals[0]}" fill="none" stroke="currentColor" stroke-width="2.4">'
              f'<animate attributeName="d" values="{";".join(vals)}" dur="{T * cyc:.2f}s" begin="indefinite" fill="freeze"/></path>')
        return fig("d1-0", "0 0 420 236", "Dây thép của đàn ghi ta điện dao động ngay phía trên bộ cảm ứng gồm nam châm quấn cuộn dây nối với máy tăng âm", b,
                   "Mô phỏng: dây thép dao động trên bộ cảm ứng, chạy chậm 60 lần. Hình không vẽ dòng cảm ứng. " + NOTE)
    b += seg(40, Y0, 380, Y0, GREY, 1.3, "4 4")
    b += pth(_sd(-AMP), ORG, 1.6, "5 4") + pth(_sd(AMP), ORG, 1.6, "5 4")
    xo = 300; ao = AMP * 2 * 0.765 * 0.235          # độ lệch của đường cong tại x = 300
    b += arrow("", "o", xo, Y0, xo, Y0 - ao, 1.8) + arrow("", "o", xo, Y0, xo, Y0 + ao, 1.8) + txt(xo + 24, 124, "nửa chu kì", ORG, 12, "middle", "700")
    b += txt(14, 56, "|ΔΦ| = 0,30 µWb mỗi vòng, trong nửa chu kì", "currentColor", 12, "start", "600")
    return fig("d1-2", "0 0 420 236", "Dữ kiện: dây thép dao động giữa hai vị trí biên trên bộ cảm ứng; từ thông qua mỗi vòng dây biến thiên trong nửa chu kì", b,
               "Dữ kiện: nét đứt cam là hai vị trí biên của dây, nét xám là vị trí cân bằng; từ thông qua mỗi vòng biến thiên trong nửa chu kì. " + NOTE)


# ───────────── Dạng 2 · sạc không dây: N1 = 24, U1 = 12 V, N2 = 16, vôn kế 7,2 V ─────────────
def d2(kk):
    run = kk == 0
    b = txt(14, 16, "sơ cấp: N_1 = 24 vòng · U_1 = 12 V", "currentColor", 12) + txt(14, 32, "thứ cấp: N_2 = 16 vòng", "currentColor", 12)
    b += txt(410, 244, "U_2 lí tưởng = ?", ORG, 13, "end")
    # điện thoại + cuộn thứ cấp
    b += rect(100, 62, 220, 80, "currentColor", 2, rx=10) + coil_row(150, 110, 5, 24, 7, 15)
    b += txt(150, 138, "cuộn thứ cấp (sau lưng điện thoại)", "currentColor", 10, "start", "400")
    # đế sạc + cuộn sơ cấp
    b += rect(100, 164, 220, 64, "currentColor", 2, rx=6) + coil_row(150, 196, 5, 24, 7, 15)
    b += txt(150, 224, "cuộn sơ cấp (trong đế sạc)", "currentColor", 10, "start", "400")
    b += alt_lines((165, 205, 245), 186, 122, run)
    # nguồn xoay chiều nối cuộn sơ cấp
    b += f'<circle cx="60" cy="196" r="16" fill="none" stroke="currentColor" stroke-width="1.8"/>' + txt(60, 201, "~", "currentColor", 16, "middle")
    b += pth("M76,196 H143", ORG, 1.8) + pth("M257,196 H290 V232 H60 V212", ORG, 1.8)
    # vôn kế nối cuộn thứ cấp
    b += f'<circle cx="370" cy="110" r="18" fill="none" stroke="currentColor" stroke-width="1.8"/>' + txt(370, 116, "V", "currentColor", 15, "middle")
    b += pth("M143,110 V48 H370 V92", ORG, 1.8) + pth("M257,110 H352", ORG, 1.8)
    b += txt(370, 144, "7,2 V", "currentColor", 12, "middle")
    if run:
        return fig("d2-0", "0 0 420 252", "Đế sạc không dây với cuộn sơ cấp nối nguồn xoay chiều, phía trên là điện thoại có cuộn thứ cấp nối vôn kế; đường sức từ nét đứt đổi chiều", b,
                   "Mô phỏng: dòng xoay chiều ở cuộn sơ cấp đổi chiều nên từ trường xuyên qua hai cuộn đổi chiều (nét đứt, đầu mũi tên đổi theo). "
                   "Hình không vẽ điện áp thứ cấp. Số vòng vẽ thu gọn. " + NOTE)
    return fig("d2-2", "0 0 420 252", "Dữ kiện: hai cuộn đặt đồng trục không có lõi sắt chung, cuộn sơ cấp nối nguồn xoay chiều, cuộn thứ cấp nối vôn kế", b,
               "Dữ kiện: hai cuộn đồng trục, áp sát, không có lõi sắt chung; vôn kế nối cuộn thứ cấp. Số vòng vẽ thu gọn. " + NOTE)


# ───────────── Dạng 3 · bốn tình huống với tấm nhôm ─────────────
PW, PH = 198, 110
PANELS = ((6, 8), (216, 8), (6, 126), (216, 126))


def pole(x, y, w, h, letter, c):
    return rect(x, y, w, h, c, 2) + (txt(x + w / 2, y + h / 2 + 5, letter, c, 14, "middle") if letter else "")


def plate(x, y, h=30):
    return rect(x, y, 6, h, ORG, 2.6)


def gap_lines(px, py, opacity_anim=False):
    ls = "".join(field_line(px + 58, py + yy, px + 140, py + yy, BLUE, 1.5, "5 4", 9) for yy in (58, 70, 82))
    if opacity_anim:
        return f'<g opacity=".15">{ls}{anim("opacity", [0.15, 1.0], 3.0)}</g>'
    return f'<g>{ls}</g>'


def d3(kk):
    run = kk == 0
    b = ""
    for i, (px, py) in enumerate(PANELS):
        b += rect(px, py, PW, PH, GREY, 1, rx=4)
    # (1) tấm và nam châm đứng yên
    px, py = PANELS[0]
    b += txt(px + 6, py + 14, "(1) tấm và nam châm đứng yên", "currentColor", 12, "start", "600")
    b += pole(px + 26, py + 62, 35, 24, "N", RED) + pole(px + 61, py + 62, 35, 24, "S", BLUE) + plate(px + 140, py + 56)
    b += txt(px + 61, py + 102, "nam châm", "currentColor", 11, "middle", "400") + txt(px + 143, py + 102, "tấm", "currentColor", 11, "middle", "400")
    # (2) tấm rơi qua khe
    px, py = PANELS[1]
    b += txt(px + 6, py + 14, "(2) tấm rơi qua khe giữa hai cực", "currentColor", 12, "start", "600")
    b += pole(px + 30, py + 44, 28, 54, "N", RED) + pole(px + 140, py + 44, 28, 54, "S", BLUE) + gap_lines(px, py)
    if run:
        b += (f'<g><animateTransform attributeName="transform" type="translate" values="0 0;0 50" dur="3s" begin="indefinite" fill="freeze"/>'
              f'{plate(px + 96, py + 18)}</g>')
    else:
        b += plate(px + 96, py + 18) + f'<rect x="{px + 96}" y="{py + 68}" width="6" height="30" fill="none" stroke="{GREY}" stroke-width="1.4" stroke-dasharray="4 3"/>'
    # (3) nam châm điện, dòng tăng
    px, py = PANELS[2]
    b += txt(px + 6, py + 14, "(3) dòng nuôi nam châm tăng", "currentColor", 12, "start", "600")
    for xx in (px + 30, px + 140):
        b += rect(xx, py + 44, 28, 54, "currentColor", 2)
        b += "".join(seg(xx, yy, xx + 28, yy, ORG, 1.3) for yy in range(py + 50, py + 98, 8))
    b += gap_lines(px, py, run) + plate(px + 96, py + 58)
    # (4) lò nướng
    px, py = PANELS[3]
    b += txt(px + 6, py + 14, "(4) trong lò nướng nóng", "currentColor", 12, "start", "600")
    b += rect(px + 26, py + 30, 146, 70, "currentColor", 2, rx=4) + plate(px + 96, py + 54)
    for x0 in (px + 40, px + 118):
        w = pth(f"M{x0},{py + 92} q4,-6 8,0 t8,0 t8,0 t8,0", ORG, 1.5)
        b += f'<g opacity=".4">{w}{anim("opacity", [0.4, 1.0, 0.5, 1.0], 3.0)}</g>' if run else w
    if run:
        return fig("d3-0", "0 0 420 244", "Bốn tình huống với tấm nhôm: nằm yên cạnh nam châm, rơi qua khe nam châm, nằm yên trong nam châm điện có dòng tăng dần, nằm trong lò nướng", b,
                   "Mô phỏng: minh hoạ các tình huống đúng như đề mô tả (có chỗ đổi, có chỗ không). "
                   "Tốc độ đi xuống của tấm trong hình không thể hiện lực hãm; không vẽ dòng cảm ứng. " + NOTE)
    return fig("d3-2", "0 0 420 244", "Dữ kiện: bốn tình huống với tấm nhôm, đường sức nét đứt giữa hai cực nam châm ở tình huống hai và ba", b,
               "Dữ kiện: bốn tình huống. Ở (2) tấm bắt đầu từ vị trí phía trên khe, nét đứt xám là vị trí khi đã vào khe. " + NOTE)


# ───────────── Dạng 4 · bếp từ 2 000 W, H = 80 %, 1,2 lít nước 25 °C → 100 °C ─────────────
def d4(kk):
    run = kk == 0
    b = txt(14, 18, "bếp từ: 2 000 W · H = 80 %", "currentColor", 13) + txt(14, 36, "1,2 lít nước: 25 °C → 100 °C", "currentColor", 13)
    b += txt(406, 18, "nồi nào? Q = ? t = ?", ORG, 13, "end")
    b += rect(70, 170, 280, 48, "currentColor", 2, rx=4) + coil_row(110, 194, 8, 28, 7, 14)
    b += rect(70, 156, 280, 8, BLUE, 1.6) + txt(356, 163, "mặt kính", "currentColor", 10, "start", "400") + txt(210, 232, "cuộn dây dưới mặt kính, dòng xoay chiều tần số cao", "currentColor", 11, "middle", "400")
    b += f'<rect x="114" y="92" width="192" height="54" fill="{BLUE}" opacity=".22"/>'
    b += pth("M118,150 L108,66 H312 L302,150 Z", "currentColor", 2.4)
    b += txt(210, 84, "nồi gang hoặc nhôm", "currentColor", 12, "middle", "600") + txt(210, 125, "nước", BLUE, 13, "middle")
    b += alt_lines((150, 185, 235, 270), 180, 136, run)
    if run:
        return fig("d4-0", "0 0 420 240", "Mặt cắt bếp từ: cuộn dây dưới mặt kính, nồi nước trên mặt kính, đường sức từ nét đứt đổi chiều xuyên qua kính vào đáy nồi", b,
                   "Mô phỏng: dòng xoay chiều đổi chiều trong cuộn dây nên từ trường của cuộn dây đổi chiều (nét đứt, đầu mũi tên đổi theo). "
                   "Hình không vẽ dòng cảm ứng và không thể hiện nhiệt độ. " + NOTE)
    return fig("d4-2", "0 0 420 240", "Dữ kiện: bếp từ công suất 2000 oát hiệu suất 80 phần trăm, nồi chứa 1,2 lít nước trên mặt kính", b,
               "Dữ kiện: bếp từ, mặt kính, nồi chứa nước. " + NOTE)


BUILD = [d1, d2, d3, d4]
