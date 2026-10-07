"""Bài 55 · Bài 10. Sự rơi tự do (Vật lí 10, chương 2) — dựng file scripts/data/bai-tap-mau/55.json từ đầu (write()).
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-55.py   (mẫu cấu trúc: build-hinh-57.py)
Quy ước theo lý thuyết bài 55: gốc toạ độ tại điểm thả, chiều dương hướng xuống, mốc thời gian lúc thả; v = gt, s = ½gt², v² = 2gs."""
import json, math, re, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

HERE = os.path.dirname(os.path.abspath(__file__))
J = os.path.join(HERE, "55.json")
OLD = json.load(open(os.path.join(HERE, "old/55.json")))["questions"]
VB = "0 0 420 250"
NOTE = "Hình minh hoạ, không đúng tỉ lệ."
VIO = "#a78bfa"


def fall(x, O, s, g, T, dt=0.1, delay=0.0):
    """Mẫu vị trí (px) của vật rơi tự do, cách đều thời gian dt; delay = số giây đứng yên ở O trước khi thả."""
    n = int(round(T / dt)); d = int(round(delay / dt))
    return [(x, O + s * 0.5 * g * (max(i - d, 0) * dt) ** 2) for i in range(n + 1)]


def yat(O, s, g, t):
    return O + s * 0.5 * g * t * t


def wall(O, gy, x0=16, x1=128):
    return f'<rect x="{x0}" y="{O}" width="{x1 - x0}" height="{gy - O:.1f}" fill="none" stroke="currentColor" stroke-width="2.2"/>'


# ───────────── Dạng 1: biết t → h, v (g = 9,8; t = 4 s) ─────────────
def d1(k):
    g = 9.8; h = 78.4; O = 36; s = 170 / h; gy = O + s * h; x = 140; p = f"e1{k}"
    deck = f'<rect x="16" y="{O}" width="112" height="10" fill="none" stroke="currentColor" stroke-width="2.2"/>'
    b = defs(p) + ground(gy) + deck + lbl(24, gy + 26, "mặt sông", "currentColor", 12, "start", "400")
    b += seg(x, O, x, gy, GRN, 1.6, "5 4", .7) + dot(x, O, 4.5, "currentColor")
    if k == 0:
        for tt in (1, 2, 3):
            y = yat(O, s, g, tt); b += dot(x, y, 3.5, GRN) + lbl(x + 12, y + 4, f"{tt} s", "currentColor", 12, "start", "400")
        b += dot(x, gy, 4.5, GRN)
        b += dim(p, "o", 70, O + 12, 70, gy, "h = ?", 78, (O + gy) / 2 + 4)
        b += arrow(p, "r", x, gy - 52, x, gy - 4, 3) + lbl(x + 12, gy - 24, "v = ?", RED, 13, "start", "700")
        b += lbl(250, 60, "Thả nhẹ: v₀ = 0", "currentColor", 13, "start", "400") + lbl(250, 82, "t = 4,0 s lúc chạm nước", ORG, 13, "start", "700")
        b += ball(fall(x, O, s, g, 4), 0, 0.1)
        return fig("e1-0", VB, "Hòn đá thả từ mép cầu rơi thẳng xuống mặt sông sau 4 giây, các chấm đánh dấu sau mỗi giây", b,
                   "Mô phỏng: hòn đá rơi tự do (đúng thời gian thật, 4 s; bấm Chạy mô phỏng); chấm đánh dấu sau mỗi 1 s. Vị trí tính theo công thức.")
    b += dot(x, gy, 4.5, ORG) + lbl(x + 12, gy - 10, "chạm nước: s = h", ORG, 13, "start", "700")
    b += arrow(p, "g", 250, O, 250, O + 96, 2) + lbl(258, O + 104, "+ (hướng xuống)", GRN, 13, "start", "700") + lbl(x + 12, O - 8, "O: thả, t = 0", "currentColor", 12, "start", "700")
    b += dim(p, "o", 70, O + 12, 70, gy, "h", 78, (O + gy) / 2 + 4)
    b += lbl(250, 160, "Đề cho: t", "currentColor", 13, "start", "400") + lbl(250, 180, "Hỏi: h, v", ORG, 13, "start", "700")
    return fig("e1-2", VB, "Gốc tại chỗ thả, chiều dương hướng xuống; khi chạm nước thì quãng rơi bằng độ cao", b, "Dữ kiện: gốc O ở chỗ thả, chiều dương xuống. " + NOTE)


# ───────────── Dạng 2: giây thứ n (g = 10; h = 125 m) ─────────────
def d2(k):
    g = 10; O = 36; x = 146; p = f"e2{k}"
    if k == 0:   # minh hoạ số liệu KHÁC đề (80 m, 4 s) để không lộ thời gian rơi của đề
        h = 80; s = 170 / h; gy = O + s * h
        b = defs(p) + ground(gy) + wall(O, gy) + seg(x, O, x, gy, GRN, 1.6, "5 4", .7) + dot(x, O, 4.5, "currentColor")
        y2, y3 = yat(O, s, g, 2), yat(O, s, g, 3)
        for tt in (1, 2, 3):
            y = yat(O, s, g, tt); b += dot(x, y, 3.5, GRN) + lbl(x + 10, y + 4, f"{tt} s", "currentColor", 12, "start", "400")
        b += dot(x, gy, 4.5, GRN)
        b += lbl(24, O + 40, "Ví dụ khác:", "currentColor", 12, "start", "700") + lbl(24, O + 58, "rơi 80 m, 4 s", "currentColor", 12, "start", "400")
        b += dim(p, "o", 300, y2, 300, y3, "giây thứ 3: ?", 308, (y2 + y3) / 2 + 4)
        b += dim(p, "b", 196, O, 196, y3, "3 s đầu: ?", 204, (O + y3) / 2 + 4)
        b += lbl(250, 190, "Đề: h = 125 m, t rơi hết = ?", ORG, 12, "start", "700")
        b += ball(fall(x, O, s, g, 4), 0, 0.1)
        return fig("e2-0", VB, "Minh hoạ một vật rơi tự do từ cột cao 80 m trong 4 giây, các chấm đánh dấu sau mỗi giây; đoạn 3 giây đầu và đoạn giây thứ 3 được ghi dấu hỏi", b,
                   "Mô phỏng MINH HOẠ số liệu khác đề (80 m, 4 s; đúng thời gian thật; bấm Chạy mô phỏng) để thấy '3 s đầu' và 'giây thứ 3' là những đoạn nào. Vị trí tính theo công thức.")
    h = 125; s = 170 / h; gy = O + s * h
    y2, y3 = yat(O, s, g, 2), yat(O, s, g, 3)
    b = defs(p) + ground(gy) + wall(O, gy) + seg(x, O, x, gy, GRN, 1.6, "5 4", .7) + dot(x, O, 4.5, "currentColor")
    for tt in (2, 3):
        y = yat(O, s, g, tt); b += dot(x, y, 3.5, GRN) + lbl(x + 10, y + 4, f"{tt} s", "currentColor", 12, "start", "400")
    b += dot(x, gy, 4.5, GRN) + dim(p, "o", 36, O, 36, gy, "h = 125 m", 44, (O + gy) / 2 + 4)
    b += dim(p, "b", 196, O, 196, y3, "0 → 3 s", 204, (O + y3) / 2 + 4)
    b += dim(p, "o", 300, y2, 300, y3, "t = 2 → 3 s", 308, (y2 + y3) / 2 + 4)
    b += lbl(250, 160, "Đề cho: h, g", "currentColor", 13, "start", "400") + lbl(250, 180, "Hỏi: t, s₃, Δs", ORG, 12, "start", "700")
    return fig("e2-2", VB, "Quãng 3 giây đầu tính từ lúc thả; quãng giây thứ 3 chỉ là đoạn từ giây thứ 2 đến giây thứ 3", b, "Dữ kiện: '3 s đầu' ≠ 'giây thứ 3'. " + NOTE)


# ───────────── Dạng 3: giây cuối → t, h (g = 9,8; Δs = 24,5 m). Mô phỏng: thả thử cao 122,5 m ─────────────
def d3(k):
    g = 9.8; O = 36; x = 150; p = f"e3{k}"
    if k == 0:
        h = 78.4; s = 170 / h; gy = O + s * h
        b = defs(p) + ground(gy) + wall(O, gy) + seg(x, O, x, gy, GRN, 1.6, "5 4", .7) + dot(x, O, 4.5, "currentColor")
        for tt in (1, 2, 3):
            y = yat(O, s, g, tt); b += dot(x, y, 3.5, GRN) + lbl(x + 10, y + 4, f"{tt} s", "currentColor", 12, "start", "400")
        y4 = yat(O, s, g, 3)
        b += dot(x, gy, 4.5, GRN)
        b += dim(p, "o", 230, y4, 230, gy, "giây cuối", 238, (y4 + gy) / 2 + 4)
        b += lbl(250, 40, "Ví dụ khác: rơi 4 s", "currentColor", 12, "start", "700")
        b += dim(p, "b", 36, O, 36, gy, "h = ?", 44, (O + gy) / 2 + 4)
        b += lbl(250, 62, "Đề: thả từ cửa sổ, v₀ = 0", "currentColor", 12, "start", "400") + lbl(250, 84, "Đề: t rơi = ?", ORG, 12, "start", "700")
        b += ball(fall(x, O, s, g, 4), 0, 0.1)
        return fig("e3-0", VB, "Viên sỏi thả rơi từ cửa sổ xuống sân; đoạn đường rơi trong giây cuối trước khi chạm sân được đánh dấu", b,
                   "Mô phỏng: thả thử một viên sỏi khác (rơi 4 s, ví dụ KHÁC đề; bấm Chạy mô phỏng) để thấy 'giây cuối' là đoạn nào. Vị trí tính theo công thức.")
    h = 100; s = 170 / h; gy = O + s * h; a = O + s * 52
    b = defs(p) + ground(gy) + wall(O, gy) + seg(x, O, x, gy, GRN, 1.6, "5 4", .7) + dot(x, O, 4.5, "currentColor") + dot(x, a, 4.5, ORG) + dot(x, gy, 4.5, GRN)
    b += lbl(x + 12, O + 4, "thả: t = 0", "currentColor", 12, "start", "400") + lbl(x + 12, a + 4, "lúc t − 1", ORG, 12, "start", "700") + lbl(x + 12, gy - 8, "chạm sân: t", GRN, 12, "start", "700")
    b += dim(p, "o", 270, a, 270, gy, "giây cuối: 24,5 m", 278, (a + gy) / 2 + 4)
    b += dim(p, "b", 36, O, 36, gy, "h = ?", 44, (O + gy) / 2 + 4)
    return fig("e3-2", VB, "Quãng rơi trong giây cuối là đoạn từ vị trí lúc t trừ 1 giây đến lúc chạm sân; thời gian rơi t chưa biết", b, "Dữ kiện: giây cuối = đoạn từ lúc t − 1 đến lúc t. " + NOTE)


# ───────────── Dạng 4: hang sâu (g = 10; v_âm = 320; T = 4,25 s). Mô phỏng: thả thử hang sâu 45 m ─────────────
def d4(k):
    g = 10; O = 40; p = f"e4{k}"
    if k == 0:
        h = 45; s = 150 / h; gy = O + s * h; x = 165
        cave = seg(110, O, 110, gy, "currentColor", 2.2) + seg(220, O, 220, gy, "currentColor", 2.2) + seg(110, gy, 220, gy, "currentColor", 2.2) + seg(16, O, 110, O, "currentColor", 2.2) + seg(220, O, 330, O, "currentColor", 2.2)
        b = defs(p) + cave + dot(x, O, 4.5, "currentColor") + lbl(120, O - 10, "miệng hang", "currentColor", 12, "start", "400")
        b += dim(p, "b", 90, O, 90, gy, "h = ?", 24, (O + gy) / 2 + 4)
        b += lbl(250, 90, "Đá rơi: t₁", GRN, 13, "start", "700") + lbl(250, 112, "Âm đi lên: t₂", ORG, 13, "start", "700") + lbl(250, 134, "Đề: nghe sau t₁ + t₂ = 4,25 s", "currentColor", 12, "start", "400") + lbl(250, 160, "Ví dụ khác: hang sâu 45 m", "currentColor", 12, "start", "700")
        n_fall, n_snd = 30, 3
        ptsB = fall(x, O, s, g, 3.0)
        b += ball(ptsB, 0, 0.1)
        xs = 200; Ys = [gy] * n_fall + [gy - (gy - O) * j / n_snd for j in range(n_snd + 1)]
        dur = 0.1 * (len(Ys) - 1)
        b += (f'<circle cx="{xs}" r="5" fill="{ORG}" opacity="0">{smil("cy", Ys, dur)}{smil("opacity", [0] * n_fall + [1] * (n_snd + 1), dur)}</circle>')
        return fig("e4-0", "0 0 420 230", "Hòn đá thả vào hang sâu rơi xuống đáy, rồi tiếng động của va chạm đi ngược lên miệng hang", b,
                   "Mô phỏng: thả thử vào một hang khác (sâu 45 m, KHÔNG phải số liệu của đề; bấm Chạy mô phỏng). Đá rơi đúng thời gian thật, tiếng động đi lên được chiếu chậm khoảng 2 lần.")
    h = 100; s = 150 / h; gy = O + s * h; x = 165
    cave = seg(110, O, 110, gy, "currentColor", 2.2) + seg(220, O, 220, gy, "currentColor", 2.2) + seg(110, gy, 220, gy, "currentColor", 2.2) + seg(16, O, 110, O, "currentColor", 2.2) + seg(220, O, 330, O, "currentColor", 2.2)
    b = defs(p) + cave + dot(x, O, 4.5, "currentColor") + dot(x, gy, 4.5, GRN)
    b += arrow(p, "g", x - 14, O + 8, x - 14, gy - 6, 3) + lbl(x - 22, (O + gy) / 2 + 4, "t₁", GRN, 14, "end", "700")
    b += arrow(p, "o", x + 24, gy - 6, x + 24, O + 8, 3) + lbl(x + 32, (O + gy) / 2 + 4, "t₂", ORG, 14, "start", "700")
    b += lbl(250, 90, "t₁: đá rơi tự do", GRN, 13, "start", "700") + lbl(250, 112, "t₂: âm truyền thẳng đều", ORG, 13, "start", "700") + lbl(250, 134, "t₁ + t₂ = 4,25 s", "currentColor", 13, "start", "700")
    b += dim(p, "b", 90, O, 90, gy, "h", 70, (O + gy) / 2 + 4, "end")
    return fig("e4-2", "0 0 420 230", "Hai giai đoạn cùng đi quãng đường bằng độ sâu hang: đá rơi xuống rồi âm truyền lên", b, "Dữ kiện: hai giai đoạn, cùng quãng đường h. " + NOTE)


# ───────────── Dạng 5: hai bi thả cách nhau 1 s (g = 10; h = 125 m) ─────────────
def d5(k):
    g = 10; h = 125; O = 36; s = 170 / h; gy = O + s * h; xa, xb = 160, 196; p = f"e5{k}"
    tower = f'<rect x="16" y="{O}" width="112" height="{gy - O:.1f}" fill="none" stroke="currentColor" stroke-width="2.2"/>'
    b = defs(p) + ground(gy) + tower + dot(xa, O, 4, GRN) + dot(xb, O, 4, VIO)
    if k == 0:
        h2 = 80; s2 = 170 / h2; gy2 = O + s2 * h2   # minh hoạ cột 80 m (số liệu khác đề)
        PA = fall(xa, O, s2, g, 4); PB = fall(xb, O, s2, g, 4, delay=1.0); dur = 0.1 * 40
        b += lbl(xa - 10, O - 10, "A", GRN, 14, "end", "700") + lbl(xb + 10, O - 10, "B", VIO, 14, "start", "700")
        b += (f'<circle cx="{xa}" cy="{O}" r="5.5" fill="{GRN}" stroke="currentColor" stroke-width="1.5">{smil("cy", [q[1] for q in PA], dur)}</circle>'
              f'<circle cx="{xb}" cy="{O}" r="5.5" fill="{VIO}" stroke="currentColor" stroke-width="1.5">{smil("cy", [q[1] for q in PB], dur)}</circle>')
        b += (f'<line x1="{xa}" x2="{xb}" y1="{O}" y2="{O}" stroke="{ORG}" stroke-width="2" stroke-dasharray="4 3">{smil("y1", [q[1] for q in PA], dur)}{smil("y2", [q[1] for q in PB], dur)}</line>')
        b += lbl(250, 60, "A: thả lúc t = 0", GRN, 13, "start", "700") + lbl(250, 82, "B: thả sau A một giây", VIO, 13, "start", "700") + lbl(250, 104, "d = khoảng cách AB", ORG, 13, "start", "700")
        b += lbl(250, 126, "Ví dụ khác: cột cao 80 m", "currentColor", 12, "start", "700")
        return fig("e5-0", VB, "Hai viên bi A và B thả từ cùng một điểm trên cột cao, B thả sau A một giây; đoạn nối hai bi dài dần", b,
                   "Mô phỏng MINH HOẠ số liệu khác đề (cột 80 m): A rơi 4 s tới đất, B thả sau 1 s (đúng thời gian thật; bấm Chạy mô phỏng). Hai bi vẽ lệch ngang cho khỏi chồng nhau, thực tế cùng một đường thẳng đứng.")
    yA, yB = yat(O, s, g, 3), yat(O, s, g, 2)
    b += dot(xa, yA, 5.5, GRN) + dot(xb, yB, 5.5, VIO) + seg(xa, O, xa, yA, GRN, 1.6, "5 4", .7) + seg(xb, O, xb, yB, VIO, 1.6, "5 4", .7)
    b += dim(p, "o", 240, yB, 240, yA, "d", 248, (yA + yB) / 2 + 4)
    b += lbl(xa - 10, yA + 4, "sA", GRN, 13, "end", "700") + lbl(xb + 10, yB + 4 - 14, "sB", VIO, 13, "start", "700")
    b += lbl(250, 150, "t tính từ lúc thả A", "currentColor", 13, "start", "700") + lbl(250, 172, "B rơi muộn 1 s: tB = t − 1", VIO, 12, "start", "700")
    return fig("e5-2", VB, "Tại một thời điểm, bi A đã rơi quãng sA, bi B đã rơi quãng sB nhỏ hơn; khoảng cách d là hiệu hai quãng", b, "Dữ kiện: d = sA − sB. " + NOTE)


BUILD = [d1, d2, d3, d4, d5]

DANG = [
 dict(label="Dạng 1 · Dễ · Biết thời gian rơi: tìm độ cao và vận tốc lúc chạm", topic="Tính thời gian, quãng đường, vận tốc khi rơi tự do",
      problem_html='<p>Một người thả nhẹ hòn đá từ mép một cây cầu xuống mặt sông và đo được thời gian rơi là $t=4{,}0\\ \\text{s}$. Bỏ qua lực cản của không khí, lấy $g=9{,}8\\ \\text{m/s}^2$.</p><ol type="a"><li>Mặt cầu cao bao nhiêu so với mặt sông?</li><li>Vận tốc của hòn đá lúc chạm mặt sông là bao nhiêu?</li></ol>'),
 dict(label="Dạng 2 · Trung bình · Quãng đường trong n giây đầu và trong giây thứ n", topic="Tính thời gian, quãng đường, vận tốc khi rơi tự do",
      problem_html='<p>Một vật được thả rơi tự do từ đỉnh một cột cao $h=125\\ \\text{m}$. Bỏ qua lực cản của không khí, lấy $g=10\\ \\text{m/s}^2$.</p><ol type="a"><li>Sau bao lâu vật chạm đất?</li><li>Tính quãng đường vật rơi được trong $3\\ \\text{s}$ đầu tiên.</li><li>Tính quãng đường vật rơi được trong giây thứ $3$.</li></ol>'),
 dict(label="Dạng 3 · Trung bình · Biết quãng đường trong giây cuối: tìm thời gian rơi và độ cao", topic="Tính thời gian, quãng đường, vận tốc khi rơi tự do",
      problem_html='<p>Một viên sỏi được thả rơi tự do từ cửa sổ một toà nhà xuống sân. Trong giây cuối cùng trước khi chạm sân, viên sỏi rơi được quãng đường $24{,}5\\ \\text{m}$. Bỏ qua lực cản của không khí, lấy $g=9{,}8\\ \\text{m/s}^2$.</p><ol type="a"><li>Viên sỏi rơi trong bao lâu?</li><li>Cửa sổ cao bao nhiêu so với mặt sân?</li><li>Tính vận tốc của viên sỏi lúc chạm sân.</li></ol>'),
 dict(label="Dạng 4 · Khó · Rơi tự do kết hợp truyền âm: tìm độ sâu của hang", topic="Tính thời gian, quãng đường, vận tốc khi rơi tự do",
      problem_html='<p>Một người thả hòn đá rơi tự do vào một cái hang sâu. Sau $4{,}25\\ \\text{s}$ kể từ lúc thả thì người đó nghe thấy tiếng hòn đá chạm đáy hang. Vận tốc truyền âm trong không khí lấy bằng $320\\ \\text{m/s}$; bỏ qua lực cản của không khí, lấy $g=10\\ \\text{m/s}^2$.</p><ol type="a"><li>Tính chiều sâu của hang.</li><li>Nếu bỏ qua thời gian truyền âm thì độ sâu tính ra là bao nhiêu và sai lệch bao nhiêu so với kết quả câu a?</li></ol>'),
 dict(label="Dạng 5 · Khó · Hai vật thả cách nhau một khoảng thời gian: khoảng cách giữa chúng", topic="Tính thời gian, quãng đường, vận tốc khi rơi tự do",
      problem_html='<p>Từ đỉnh một cột cao $125\\ \\text{m}$ thả rơi tự do viên bi A. Đúng $1\\ \\text{s}$ sau, thả tiếp viên bi B từ cùng điểm đó, không vận tốc đầu. Bỏ qua lực cản của không khí, lấy $g=10\\ \\text{m/s}^2$. Mốc thời gian $t=0$ là lúc thả bi A; xét lúc cả hai bi còn đang rơi.</p><ol type="a"><li>Khi bi A đã rơi được $3\\ \\text{s}$, hai bi cách nhau bao nhiêu?</li><li>Sau lúc thả bi A bao lâu thì hai bi cách nhau $35\\ \\text{m}$?</li><li>Hiệu vận tốc $v_A-v_B$ của hai bi là bao nhiêu? Khoảng cách giữa hai bi tăng thêm bao nhiêu mét sau mỗi giây?</li></ol>'),
]

DK = "⚠ Chỉ có trọng lực: rơi tự do, $a=g$, chiều dương hướng xuống"
ANALYSIS = [
 [("\"thả nhẹ hòn đá từ mép cầu\"", "$v_0=0$; mốc thời gian lúc thả", "Rơi tự do: $v_0=0$, $a=g$, gốc tại chỗ thả"),
  ("\"bỏ qua lực cản của không khí\"", "Chỉ có trọng lực", DK),
  ("\"thời gian rơi là $t=4{,}0$ s\"", "$t=4{,}0$ s", "Quãng đường rơi: $s=\\dfrac{1}{2}gt^2$"),
  ("\"mặt cầu cao bao nhiêu so với mặt sông\"", "Cần $h$; chạm sông khi $s=h$", "$h=s=\\dfrac{1}{2}gt^2$"),
  ("\"vận tốc lúc chạm mặt sông\"", "Cần $v$ tại $t=4{,}0$ s", "$v=gt$ (kiểm bằng $v^2=2gh$)")],
 [("\"thả rơi tự do từ đỉnh cột cao $h=125$ m\"", "$v_0=0$; $h=125$ m", "Chạm đất khi $s=h$: $t=\\sqrt{\\dfrac{2h}{g}}$"),
  ("\"bỏ qua lực cản; $g=10$\"", "Chỉ có trọng lực; $g=10$", DK),
  ("\"quãng đường trong $3$ s đầu tiên\"", "Từ $t=0$ đến $t=3$ s", "$s=\\dfrac{1}{2}gt^2$ với $t=3$ s: cả đoạn tính từ lúc thả"),
  ("\"quãng đường trong giây thứ $3$\"", "Từ $t=2$ s đến $t=3$ s", "⚠ Chỉ là một đoạn của $3$ s đầu: $\\Delta s=s(3)-s(2)$")],
 [("\"thả rơi tự do từ cửa sổ\"", "$v_0=0$; $t$, $h$ chưa biết", "Rơi tự do: $s=\\dfrac{1}{2}gt^2$"),
  ("\"bỏ qua lực cản; $g=9{,}8$\"", "Chỉ có trọng lực; $g=9{,}8$", DK),
  ("\"trong giây cuối cùng trước khi chạm sân\"", "Từ $t-1$ đến $t$ ($t$ là thời gian rơi, chưa biết)", "⚠ $\\Delta s=s(t)-s(t-1)$, không phải $s(t)$"),
  ("\"rơi được quãng đường $24{,}5$ m\"", "$\\Delta s=24{,}5$ m", "$\\Delta s=\\dfrac{1}{2}g\\left[t^2-(t-1)^2\\right]$ → giải ra $t$"),
  ("\"cửa sổ cao bao nhiêu so với mặt sân\"", "Cần $h$", "$h=\\dfrac{1}{2}gt^2$ (chạm sân khi $s=h$)"),
  ("\"vận tốc của viên sỏi lúc chạm sân\"", "Cần $v$", "$v=gt$")],
 [("\"thả hòn đá rơi tự do vào hang sâu\"", "$v_0=0$; đá rơi trong $t_1$", "Rơi tự do: $h=\\dfrac{1}{2}gt_1^2$"),
  ("\"bỏ qua lực cản; $g=10$\"", "Chỉ có trọng lực; $g=10$", "⚠ Chỉ đá chịu trọng lực; tiếng động truyền thẳng đều với vận tốc không đổi"),
  ("\"sau $4{,}25$ s kể từ lúc thả thì nghe thấy tiếng\"", "$t_1+t_2=4{,}25$ s", "⚠ $4{,}25$ s là tổng hai giai đoạn, không phải riêng thời gian rơi"),
  ("\"vận tốc truyền âm $320$ m/s\"", "$v_{\\text{âm}}=320$ m/s", "Âm đi lên đều: $t_2=\\dfrac{h}{v_{\\text{âm}}}$"),
  ("\"tính chiều sâu của hang\"", "Cần $h$ (chung cho cả hai giai đoạn)", "Biểu diễn $t_2$ theo $t_1$ → phương trình bậc hai ẩn $t_1$"),
  ("\"nếu bỏ qua thời gian truyền âm\"", "Coi $t_2=0$ nên $t_1=4{,}25$ s", "$h'=\\dfrac{1}{2}g\\cdot4{,}25^2$ rồi so với $h$")],
 [("\"thả rơi tự do viên bi A từ cột cao $125$ m\"", "$v_0=0$; mốc $t=0$ lúc thả A", "Rơi tự do: $s_A=\\dfrac{1}{2}gt^2$"),
  ("\"$1$ s sau, thả tiếp viên bi B từ cùng điểm\"", "B rơi trễ $1$ s: $t_B=t-1$", "$s_B=\\dfrac{1}{2}g(t-1)^2$ (chỉ khi $t\\ge1$)"),
  ("\"bỏ qua lực cản; xét lúc cả hai còn đang rơi\"", "Chỉ có trọng lực; chưa bi nào chạm đất", "⚠ Công thức chỉ đúng khi $s_A\\lt125$ m (A chưa chạm đất)"),
  ("\"hai bi cách nhau bao nhiêu\"", "$d=s_A-s_B$", "$d=\\dfrac{1}{2}g\\left[t^2-(t-1)^2\\right]$"),
  ("\"khi bi A đã rơi $3$ s\"", "$t=3$ s", "Thay $t$ vào $d(t)$"),
  ("\"cách nhau $35$ m\"", "$d=35$ m, cần $t$", "Giải $d(t)=35$"),
  ("\"hiệu vận tốc $v_A-v_B$\"", "$v_A=gt$; $v_B=g(t-1)$", "Trừ hai vận tốc cùng thời điểm")],
]

RF = ["<strong>Khái niệm:</strong> rơi tự do là sự rơi chỉ dưới tác dụng của trọng lực, $v_0=0$.",
      "<strong>Định luật:</strong> chuyển động thẳng nhanh dần đều, gia tốc $a=g$, chiều dương hướng xuống.",
      "$v=gt$ · $s=\\dfrac{1}{2}gt^2$ · $v^2=2gs$",
      "Chạm đất khi $s=h$: $t=\\sqrt{\\dfrac{2h}{g}}$",
      "⚠ <strong>Điều kiện:</strong> bỏ qua lực cản, chỉ có trọng lực."]

SOLS = [
 sol(RF, [
  ("Độ cao của mặt cầu", [P("Chạm sông khi $s=h$, $v_0=0$:"), M(r"h=s=\dfrac{1}{2}gt^2"), M(r"h=\dfrac{1}{2}\cdot9{,}8\cdot4^2"), A(r"h=78{,}4\ \text{m}")]),
  ("Vận tốc lúc chạm sông", [M(r"v=gt=9{,}8\cdot4"), A(r"v=39{,}2\ \text{m/s}")]),
  ("Kiểm tra", [P("Cách khác:"), M(r"v^2=2gh=2\cdot9{,}8\cdot78{,}4=1536{,}64\ \Rightarrow\ v=39{,}2\ \text{m/s}\ \checkmark"), P("Đơn vị: m/s² · s² = m ✓")])],
  ["a) $h=78{,}4\\ \\text{m}$", "b) $v=39{,}2\\ \\text{m/s}$"],
  "Nhận dạng: đề cho <strong>thời gian rơi</strong> (hoặc độ cao) và hỏi độ cao / vận tốc → $v_0=0$, dùng $s=\\dfrac{1}{2}gt^2$ và $v=gt$."),
 sol(RF + ["Giây thứ $n$ là đoạn từ $t=n-1$ đến $t=n$: $\\Delta s=s(n)-s(n-1)$."], [
  ("Thời gian rơi hết độ cao", [M(r"t=\sqrt{\dfrac{2h}{g}}=\sqrt{\dfrac{2\cdot125}{10}}=\sqrt{25}"), A(r"t=5\ \text{s}")]),
  ("Quãng đường trong 3 s đầu", [P("Tính từ lúc thả:"), M(r"s_3=\dfrac{1}{2}gt^2=\dfrac{1}{2}\cdot10\cdot3^2"), A(r"s_3=45\ \text{m}")]),
  ("Quãng đường trong 2 s đầu", [M(r"s_2=\dfrac{1}{2}\cdot10\cdot2^2=20\ \text{m}")]),
  ("Quãng đường trong giây thứ 3", [P("Giây thứ 3 là đoạn từ $t=2$ s đến $t=3$ s:"), M(r"\Delta s=s_3-s_2=45-20"), A(r"\Delta s=25\ \text{m}")]),
  ("Kiểm tra", [P("Các giây liên tiếp rơi $5$ m, $15$ m, $25$ m: đúng tỉ lệ $1:3:5$ ✓"), P("$3$ s đầu ($45$ m) khác giây thứ $3$ ($25$ m).")])],
  ["a) $t=5\\ \\text{s}$", "b) $s_3=45\\ \\text{m}$", "c) $\\Delta s=25\\ \\text{m}$"],
  "Nhận dạng: đề hỏi <strong>'trong giây thứ n'</strong> → lấy $s(n)-s(n-1)$; <strong>'trong n giây đầu'</strong> → chỉ $s(n)$."),
 sol(RF + ["Giây cuối là đoạn từ $t-1$ đến $t$: $\\Delta s=s(t)-s(t-1)$."], [
  ("Lập quãng đường trong giây cuối", [P("Gọi $t$ là thời gian rơi:"), M(r"\Delta s=\dfrac{1}{2}gt^2-\dfrac{1}{2}g(t-1)^2"), M(r"\Delta s=\dfrac{1}{2}g(2t-1)")]),
  ("Giải tìm thời gian rơi", [M(r"24{,}5=\dfrac{1}{2}\cdot9{,}8\cdot(2t-1)=4{,}9\,(2t-1)"), M(r"2t-1=5"), A(r"t=3\ \text{s}")]),
  ("Độ cao của cửa sổ", [M(r"h=\dfrac{1}{2}gt^2=\dfrac{1}{2}\cdot9{,}8\cdot3^2"), A(r"h=44{,}1\ \text{m}")]),
  ("Vận tốc lúc chạm sân", [M(r"v=gt=9{,}8\cdot3"), A(r"v=29{,}4\ \text{m/s}")]),
  ("Kiểm tra", [P("Quãng rơi trong $2$ s đầu:"), M(r"s_2=\dfrac{1}{2}\cdot9{,}8\cdot2^2=19{,}6\ \text{m}"), P("Giây cuối:"), M(r"44{,}1-19{,}6=24{,}5\ \text{m}\ \checkmark")])],
  ["a) $t=3\\ \\text{s}$", "b) $h=44{,}1\\ \\text{m}$", "c) $v=29{,}4\\ \\text{m/s}$"],
  "Nhận dạng: đề cho <strong>quãng đường trong giây cuối</strong> rồi hỏi thời gian / độ cao → lập $s(t)-s(t-1)$, giải ra $t$ trước."),
 sol(RF + ["Âm truyền thẳng đều: $t_2=\\dfrac{h}{v_{\\text{âm}}}$ · tổng thời gian: $t_1+t_2=4{,}25\\ \\text{s}$."], [
  ("Hai giai đoạn, cùng quãng đường $h$", [P("Gọi $t_1$ là thời gian đá rơi, $t_2$ là thời gian âm đi lên:"), M(r"h=\dfrac{1}{2}gt_1^2=5t_1^2"), M(r"t_2=\dfrac{h}{v_{\text{âm}}}=\dfrac{5t_1^2}{320}=\dfrac{t_1^2}{64}")]),
  ("Phương trình theo $t_1$", [M(r"t_1+t_2=4{,}25"), M(r"t_1+\dfrac{t_1^2}{64}=4{,}25"), M(r"t_1^2+64t_1-272=0")]),
  ("Giải phương trình", [M(r"\Delta=64^2+4\cdot272=5184,\quad\sqrt{\Delta}=72"), M(r"t_1=\dfrac{-64+72}{2}=4\ \text{s}"), P("Nghiệm $t_1=-68$ s bị loại vì $t_1\\gt0$.")]),
  ("Chiều sâu của hang", [M(r"h=5t_1^2=5\cdot4^2"), A(r"h=80\ \text{m}"), P("Kiểm tra: $t_2=\\dfrac{80}{320}=0{,}25$ s và $t_1+t_2=4{,}25$ s ✓")]),
  ("Nếu bỏ qua thời gian truyền âm", [P("Coi cả $4{,}25$ s là thời gian rơi:"), M(r"h'=\dfrac{1}{2}\cdot10\cdot4{,}25^2\approx90{,}3\ \text{m}"), M(r"h'-h\approx90{,}3-80=10{,}3\ \text{m}\ \ (\approx13\%\ \text{so với}\ 80\ \text{m})")])],
  ["a) $h=80\\ \\text{m}$", "b) $h'\\approx90{,}3\\ \\text{m}$, lệch khoảng $10{,}3\\ \\text{m}$ ($\\approx13\\%$)"],
  "Nhận dạng: <strong>nghe tiếng sau thời gian T</strong> → T gồm thời gian rơi và thời gian âm truyền; cùng quãng đường $h$ nên viết cả hai theo một ẩn."),
 sol(RF + ["Hai vật cùng rơi tự do: vật thả sau $\\tau$ có thời gian rơi $t-\\tau$."], [
  ("Quãng đường mỗi bi", [P("$t$ tính từ lúc thả A; B thả trễ $1$ s nên rơi được $t-1$ giây:"), M(r"s_A=\dfrac{1}{2}gt^2=5t^2"), M(r"s_B=\dfrac{1}{2}g(t-1)^2=5(t-1)^2")]),
  ("Khoảng cách giữa hai bi", [M(r"d=s_A-s_B=5t^2-5(t-1)^2"), M(r"d=5(2t-1)=10t-5")]),
  ("Câu a: khi $t=3$ s", [M(r"d=10\cdot3-5"), A(r"d=25\ \text{m}")]),
  ("Câu b: khi $d=35$ m", [M(r"10t-5=35"), A(r"t=4\ \text{s}"), P("Kiểm tra bi A chưa chạm đất: $s_A=5\\cdot4^2=80\\ \\text{m}\\lt125\\ \\text{m}$ ✓")]),
  ("Câu c: hiệu vận tốc", [M(r"v_A-v_B=gt-g(t-1)=g\cdot1"), A(r"v_A-v_B=10\ \text{m/s}"), P("Không đổi theo thời gian, nên khoảng cách tăng đều $10$ m mỗi giây:"), M(r"d(4)-d(3)=35-25=10\ \text{m}\ \checkmark")])],
  ["a) $d=25\\ \\text{m}$", "b) $t=4\\ \\text{s}$", "c) $v_A-v_B=10\\ \\text{m/s}$; khoảng cách tăng $10\\ \\text{m}$ mỗi giây"],
  "Nhận dạng: <strong>hai vật thả lệch nhau một khoảng thời gian</strong> → viết $s$ của từng vật theo cùng một mốc $t$, lấy hiệu."),
]

# Ví dụ cũ: 1 → Dạng 1 · 2, 5 → Dạng 2 · 4, 7 → Dạng 3 · 6 → Dạng 4 · (Dạng 5 là dạng mới, gần ví dụ 3 nhưng không cần ném lên)
# Còn lại (ném lên thẳng đứng, ngoài lý thuyết bài này): 8, 9, 3 → tự luận, xếp dễ → khó.
TU_LUAN = tu_luan_tu(OLD, [7, 8, 2], {7: "Trung bình", 8: "Khó", 2: "Nâng cao"})

def _sua_latex(h):
    """Sửa NHẸ lỗi chuỗi của ví dụ cũ (không đổi nội dung vật lí): h0^2 dính, \\ trong $…$, thập phân thiếu {,}."""
    h = h.replace("2(-g)h0^{2}-30^{2}", "2(-g)h\\Rightarrow 0^{2}-30^{2}").replace("2.(-g).h0^{2}-7,5^{2}", "2.(-g).h\\Rightarrow 0^{2}-7,5^{2}")
    h = h.replace("gt^{'^{2}}", "gt'^{2}")
    parts = h.replace("$$", "\x00").split("$")
    for i in range(1, len(parts), 2):
        parts[i] = parts[i].replace(" \\\\ ", "\\quad ")
        parts[i] = re.sub(r"(?<=\d),(?=\d)", "{,}", parts[i])
    return "$".join(parts).replace("\x00", "$$")
TU_LUAN["body_html"] = _sua_latex(TU_LUAN["body_html"])

write(J, 55, "Bài 10. Sự rơi tự do", DANG, BUILD, ANALYSIS, SOLS, TU_LUAN)
