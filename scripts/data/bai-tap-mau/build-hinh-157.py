"""Bài tập mẫu Chuyên đề 04 "Đoạn mạch nối tiếp, song song, hỗn hợp" (khoá Vật lí HSG & chuyên, KHTN 9) — lesson_id 157.
Nguồn: content/hsg9/cd04-mach-noi-tiep-song-song/nguon.md (mục C dạng bài, D/E/G ví dụ; mọi số liệu đã tự giải lại bằng Fraction ở cuối file).
YCCĐ "bài tương tự": lớp 11 b23 (id 42) "Điện trở. Định luật Ohm" — chủ đề cha (chưa có YCCĐ con về mạch nối tiếp/song song).
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-157.py   (idempotent; không ghi DB). Hình dùng content/hsg9/cd04-mach-noi-tiep-song-song/mach.py.

Lỗi/điểm sửa so với nguồn:
 - Dạng 7 (a) ghép ba điện trở r: nguồn liệt kê 3 cách (18, 4, 2 Ω) — thiếu cách "hai song song nối tiếp một" = 3r/2 = 9 Ω; đủ 4 cách (tu_luan bài 1).
 - D5 (biến trở + khoá K "song song với R2", R2 // R1): nguồn nói K đóng chỉ nối tắt R2 → Rtđ tăng 30→40 Ω và "đóng khoá dòng giảm". SAI: K nối hai nút M, N nên nối tắt cả R1 lẫn R2 → Rtđ = Rb = 10 Ω (giảm), dòng 1,8 A, vôn kế 0 (Dạng 3 và tu_luan bài 3).
 - G3 (c) "điện thế tại P = 12 V, tại Q = 13,5 V (lấy M làm mốc)": số 12 và 13,5 là điện thế so với N; so với M (cực dương) là −6 V và −4,5 V. Kết luận Q cao hơn P vẫn đúng (tu_luan bài 6).
 - Dạng 4/G2: ba bài về dụng cụ đo thực dùng nguyên số của nguồn nhưng sai số "so với câu a" phải ghi rõ là so với giá trị lí tưởng; số liệu đã kiểm lại đúng."""
import json, math, os, sys
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
sys.path.insert(0, os.path.join(HERE, "../../../content/hsg9/cd04-mach-noi-tiep-song-song"))
from dung import *
import mach as mc

J = os.path.join(HERE, "157.json")
TOPIC = "Điện trở. Định luật Ohm"
par = lambda *r: 1 / sum(Fr(1) / x for x in r)

# ═════════════ KIỂM SỐ LIỆU (Fraction) ═════════════
# Dạng 1
R23 = par(15, 10); Rt = 4 + R23; I = Fr(30) / Rt; U1 = I * 4; U23 = 30 - U1
assert (R23, Rt, I, U1, U23, U23 / 15, U23 / 10) == (6, 10, 3, 12, 18, Fr(6, 5), Fr(9, 5))
assert Fr(30, 2) - 6 == 9 and 2 * 6 == 30 - 2 * 9
# Dạng 2
assert (Fr(12, 90), Fr(12, 90) * 60) == (Fr(2, 15), 8)
Rd = par(60, 60); Rt2 = 30 + Rd; I2 = Fr(12) / Rt2
assert (Rd, Rt2, I2, I2 * Rd, (8 - I2 * Rd) / 8) == (30, 60, Fr(1, 5), 6, Fr(1, 4))
Rt2c = 3 + 30 + Rd; I2c = Fr(12) / Rt2c; V2c = I2c * Rd
assert (Rt2c, I2c, V2c) == (63, Fr(4, 21), Fr(40, 7)) and abs(float((8 - V2c) / 8) - .2857) < 1e-3
RV = Fr(1980); Rd1 = par(60, RV); V1 = Fr(12) * Rd1 / (30 + Rd1)
assert V1 == Fr(99, 100) * 8 and (8 - V1) / 8 == Fr(1, 100)
assert Fr(30) * Fr(792, 100) / Fr(408, 100) == Fr(30 * 792, 408) and Fr(60) * Fr(30 * 792, 408) / (60 - Fr(30 * 792, 408)) == 1980
# Dạng 3
assert Fr(12, 2) == 6 and Fr(12) / Fr(12, 10) - 6 == 4 and Fr(12 * 6, 12 + 6) == 4
R23_ = Fr(12) / Fr(6, 5) - 6; R3_ = 1 / (1 / R23_ - Fr(1, 12))
U23_ = Fr(6, 5) * R23_
assert (R23_, R3_, U23_, U23_ / 12, U23_ / R3_, 6 * Fr(6, 5)) == (4, 6, Fr(24, 5), Fr(2, 5), Fr(4, 5), Fr(36, 5))
assert Fr(2, 5) + Fr(4, 5) == Fr(6, 5) and Fr(36, 5) + Fr(24, 5) == 12
# Dạng 4
Rss = par(12, 12); I4 = Fr(18) / (6 + Rss)
assert (Rss, I4, I4 * Rss) == (6, Fr(3, 2), 9)
Uss = 8; U1_ = 18 - Uss; Ib = Fr(U1_, 6); Rss_ = Fr(Uss) / Ib
assert (Ib, Rss_, 1 / (1 / Rss_ - Fr(1, 12))) == (Fr(5, 3), Fr(24, 5), 8)
assert (Fr(18) / (6 + par(24, 12)), Fr(18) / 6, Fr(18) * par(24, 12) / (6 + par(24, 12))) == (Fr(9, 7), 3, Fr(72, 7))
assert abs(float(Fr(9, 7)) - 1.2857) < 1e-3 and float(Fr(72, 7)) < 11
# Dạng 5
assert 6 * 15 == 9 * 10 and par(6, 9) + par(10, 15) == Fr(48, 5) == Fr(16 * 24, 40)
assert (Fr(30, 16), Fr(30, 24), Fr(30, 16) + Fr(30, 24)) == (Fr(15, 8), Fr(5, 4), Fr(25, 8)) and Fr(25, 8) == Fr(30) / Fr(48, 5)
assert Fr(15, 8) * 10 == Fr(5, 4) * 15       # V_P = V_Q (so với N)
# Dạng 6
U4 = 1 * 12; Ux = Fr(18); Iy = (Ux - U4) / 4; I2_ = Ux / 12; I_ = I2_ + Iy
assert (Iy, I2_, I_, 24 - Ux, I_ * 2) == (Fr(3, 2), Fr(3, 2), 3, 6, 6) and 24 - Ux == I_ * 2
assert 24 - Ux == 2 * (Ux / 12 + (Ux - 12) / 4)            # phương trình ẩn U_X: nghiệm 18
I5_ = Iy - 1; assert (I5_, Fr(12) / I5_) == (Fr(1, 2), 24)
assert 2 + par(12, 4 + par(12, 24)) == 8 and Fr(24, 8) == 3

NOTE = "Hình minh hoạ, không đúng tỉ lệ."
FAST = 55.0


def figr(bt, vb, alt, body, cap, run=False):
    return mc.fig(bt, vb, alt, body, cap, run)


# ═════════════ HÌNH ═════════════
def d1(k):
    if k == 0:
        b, g = mc.c_hh("R_1|4 Ω", "R_2|15 Ω", "R_3|10 Ω", U="U|30 V", xv=410)
        b += mc.sim_hh(g, 3, 1.2, 1.8, vA=FAST)
        return figr("d157-1-0", "0 0 450 190", "Mạch R1 nối tiếp với R2 song song R3, ampe kế ở nhánh chính, vôn kế song song đoạn song song", b,
                    "Mạch của bài. Chấm xanh là điện tích dương đi từ cực + của nguồn ra ngoài.<br>Chấm đi càng nhanh ở nhánh nào, dòng điện nhánh đó càng lớn (chạy chậm, không đúng thời gian thật).", True)
    b = mc.c_red("R_1|4 Ω", "R_{23}|?", note=("R_{23}=R_{2}R_{3}/(R_{2}+R_{3})", "R_{td}=R_{1}+R_{23}"))
    return figr("d157-1-2", "0 0 480 190", "Mạch đã thu gọn: R1 nối tiếp R23", b, "Sau bước 1: chỉ còn $R_1$ nối tiếp $R_{23}$. " + NOTE)


def d2(k):
    if k == 0:
        b, g = mc.c_hh("R_1|30 Ω", "R_2|60 Ω", None, U="U|12 V")
        b += mc.sim_hh(g, 2 / 15 * 5, 2 / 15 * 5, vA=FAST / 5)
        return figr("d157-2-0", "0 0 450 190", "R1 nối tiếp R2, ampe kế ở nhánh chính, vôn kế song song với R2", b,
                    "Mạch của bài. Chấm xanh đi từ cực + của nguồn ra ngoài (chạy chậm, không đúng thời gian thật).", True)
    b, g = mc.c_hh("R_1|30 Ω", "R_2|60 Ω", None, Akind="RA", Alabel="R_A", Vkind="RV", Vlabel="R_V", U="U|12 V")
    return figr("d157-2-2", "0 0 450 190", "Mạch thực: ampe kế thành điện trở RA nối tiếp, vôn kế thành điện trở RV song song với R2", b,
                "Đưa dụng cụ vào sơ đồ: $R_A$ nối tiếp, $R_V$ song song với $R_2$. " + NOTE)


def d3(k):
    if k == 0:
        b, g = mc.c_hh("R_1|?", "R_2|12 Ω", "R_3|?", A=True, V=False, shortK="open", U="U|12 V")
        b += mc.sim([(g["src"][1], g["src"][0], 1), (g["r1"][0], g["r1"][1], 1), (g["r2"][0], g["r2"][1], 1), (g["r3"][0], g["r3"][1], 1), (g["bot"][0], g["bot"][1], 1)], 50)
        return figr("d157-3-0", "0 0 450 200", "R1 nối tiếp đoạn song song R2, R3; khoá K song song với R2; ampe kế ở nhánh chính", b,
                    "Mạch của bài, K đang mở. Chấm xanh chỉ chiều dòng điện, mọi chấm cùng tốc độ (không biểu diễn độ lớn).", True)
    b, g = mc.c_hh("R_1|?", "R_2|12 Ω", "R_3|?", A=True, V=False, shortK="closed", grey=("R2", "R3"), U="U|12 V")
    return figr("d157-3-2", "0 0 450 200", "Khoá K đóng nối M với N: R2 và R3 bị nối tắt, chỉ còn R1", b,
                "K đóng: M và N cùng điện thế, $R_2$ và $R_3$ (màu nhạt) không có dòng. " + NOTE)


def d4(k):
    if k == 0:
        b, g = mc.c_hh("R_1|6 Ω", "R_b|0–24 Ω", "R_2|12 Ω", kind2="Rb", U="U|18 V", xv=410)
        b += mc.sim_hh(g, 1.5, .75, .75, vA=FAST)
        return figr("d157-4-0", "0 0 450 190", "R1 nối tiếp với biến trở Rb song song R2, ampe kế nhánh chính, vôn kế song song đoạn song song", b,
                    "Mạch của bài (minh hoạ lúc $R_b=12\\ \\Omega$). Chấm xanh đi từ cực + của nguồn (chạy chậm, không đúng thời gian thật).", True)
    b = mc.c_red("R_1|6 Ω", "R_{ss}|?", note=("R_{ss}=R_{b}R_{2}/(R_{b}+R_{2})", "R_{td}=R_{1}+R_{ss}", "U_{ss}=U-IR_{1}"))
    return figr("d157-4-2", "0 0 480 190", "Mạch thu gọn: R1 nối tiếp Rss, với Rss là điện trở của Rb song song R2", b, "Biến trở và $R_2$ thu gọn thành $R_{ss}$. " + NOTE)


def d5(k):
    if k == 0:
        b, g = mc.c_bridge("R_1|6 Ω", "R_2|9 Ω", "R_3|10 Ω", "R_4|?", mid=("V", ""), U="U|30 V")
        b += mc.sim([((50, 170), (50, 30), 1), ((50, 30), (170, 30), 1), ((170, 30), (170, 170), 1), ((300, 30), (300, 170), 1), ((170, 170), (50, 170), 1)], 50)
        return figr("d157-5-0", "0 0 400 200", "Cầu: nhánh trái R1 rồi R3, nhánh phải R2 rồi R4 chưa biết, vôn kế lí tưởng giữa P và Q chỉ 0", b,
                    "Mạch của bài. Chấm xanh chỉ chiều dòng điện, mọi chấm cùng tốc độ (không biểu diễn độ lớn).", True)
    b, g = mc.c_bridge("R_1|6 Ω", "R_2|9 Ω", "R_3|10 Ω", "R_4|?", mid=None, U="U|30 V")
    b += mc.lab(335, 105, "P ≡ Q", "currentColor", 13, "start", "700")
    return figr("d157-5-2", "0 0 400 200", "Cầu cân bằng: chập P với Q thì còn hai khối song song nối tiếp nhau", b,
                "Cầu cân bằng: P và Q cùng điện thế, chập lại được. Còn $(R_1\\parallel R_2)$ nối tiếp $(R_3\\parallel R_4)$. " + NOTE)


def d6(k):
    if k == 0:
        b, g = mc.c_3tier("R_1|2 Ω", "R_2|12 Ω", "R_3|4 Ω", "R_4|12 Ω", "R_5|?", U="U|24 V")
        v = 50
        b += mc.sim([(g["src"][1], g["src"][0], 1), (g["r1"][0], g["r1"][1], 1), (g["r2"][0], g["r2"][1], 1), (g["r3"][0], g["r3"][1], 1),
                     (g["r4"][0], g["r4"][1], 1), (g["r5"][0], g["r5"][1], 1), (g["bot"][0], g["bot"][1], 1)], v)
        return figr("d157-6-0", "0 0 490 250", "R1 nối tiếp (R2 song song với (R3 nối tiếp (R4 song song R5))), hai ampe kế A1 và A2", b,
                    "Mạch của bài. Chấm xanh chỉ chiều dòng điện, mọi chấm cùng tốc độ (không biểu diễn độ lớn).", True)
    b, g = mc.c_3tier("R_1|2 Ω", "R_2|12 Ω", "R_3|4 Ω", "R_4|12 Ω", "R_5|?", U="U|24 V", boxes=True)
    return figr("d157-6-2", "0 0 490 250", "Ba tầng: R45 là R4 song song R5; Y là R3 nối tiếp R45; Y song song R2; rồi nối tiếp R1", b,
                "Thu gọn từ trong ra: $R_{45}$, rồi $Y=R_3+R_{45}$, rồi $R_2\\parallel Y$, cuối cùng nối tiếp $R_1$. " + NOTE)


BUILD = [d1, d2, d3, d4, d5, d6]

# ═════════════ ĐỀ (chữ) ═════════════
DANG = [
    dict(label="Dạng 1 · Cơ bản · Mạch hỗn hợp R1 nối tiếp (R2 // R3): bốn bước và tính ngược", topic=TOPIC, problem_html=(
        r'<p>Điện trở $R_1=4\ \Omega$ nối tiếp với đoạn song song gồm $R_2=15\ \Omega$ và $R_3=10\ \Omega$, mắc vào nguồn $U=30\ \text{V}$. '
        r'Ampe kế lí tưởng ở nhánh chính; vôn kế lí tưởng song song với đoạn song song.</p>'
        r'<ol type="a"><li>Tính điện trở tương đương của cả mạch và số chỉ ampe kế.</li>'
        r'<li>Tính số chỉ vôn kế và cường độ dòng điện qua $R_2$, $R_3$.</li>'
        r'<li>Giữ nguyên $U$, $R_2$, $R_3$; thay $R_1$ bằng $R_{1}^{\prime}$ để ampe kế chỉ $2\ \text{A}$. Tính $R_{1}^{\prime}$.</li></ol>')),
    dict(label="Dạng 2 · Trung bình · Ampe kế, vôn kế thực: sai số và điều kiện chọn dụng cụ", topic=TOPIC, problem_html=(
        r'<p>Nguồn $U=12\ \text{V}$; $R_1=30\ \Omega$ nối tiếp $R_2=60\ \Omega$. Ampe kế mắc nối tiếp trong mạch, vôn kế mắc song song với $R_2$.</p>'
        r'<ol type="a"><li>Dụng cụ lí tưởng: tính số chỉ ampe kế và vôn kế.</li>'
        r'<li>Vôn kế có $R_V=60\ \Omega$, ampe kế lí tưởng. Tính số chỉ hai dụng cụ và sai số tương đối của số chỉ vôn kế so với câu a.</li>'
        r'<li>Giữ vôn kế câu b, ampe kế có $R_A=3\ \Omega$. Tính số chỉ hai dụng cụ.</li>'
        r'<li>Ampe kế lí tưởng. Vôn kế phải có $R_V$ tối thiểu bao nhiêu để sai số tương đối của số chỉ vôn kế không quá $1\%$?</li></ol>')),
    dict(label="Dạng 3 · Trung bình · Khoá K nối tắt đoạn song song và ẩn số điện trở", topic=TOPIC, problem_html=(
        r'<p>Nguồn $U=12\ \text{V}$ không đổi. Điện trở $R_1$ chưa biết nối tiếp với đoạn song song gồm $R_2=12\ \Omega$ và $R_3$ chưa biết. '
        r'Khoá K mắc song song với $R_2$. Ampe kế lí tưởng ở nhánh chính chỉ $2\ \text{A}$ khi K đóng và $1{,}2\ \text{A}$ khi K mở.</p>'
        r'<ol type="a"><li>Khi K đóng, những điện trở nào còn có dòng điện? Tính $R_1$.</li>'
        r'<li>Tính $R_3$.</li>'
        r'<li>Khi K mở, tính hiệu điện thế giữa hai đầu $R_3$ và cường độ dòng điện qua $R_2$.</li></ol>')),
    dict(label="Dạng 4 · Kết hợp · Biến trở trong mạch hỗn hợp: giá trị cần chỉnh và miền số chỉ", topic=TOPIC, problem_html=(
        r'<p>Nguồn $U=18\ \text{V}$; $R_1=6\ \Omega$ nối tiếp với đoạn song song gồm biến trở $R_b$ (từ $0$ đến $24\ \Omega$) và $R_2=12\ \Omega$. '
        r'Ampe kế lí tưởng ở nhánh chính; vôn kế lí tưởng song song với đoạn song song.</p>'
        r'<ol type="a"><li>Với $R_b=12\ \Omega$, tính số chỉ ampe kế và vôn kế.</li>'
        r'<li>Điều chỉnh $R_b$ bằng bao nhiêu để vôn kế chỉ $8\ \text{V}$?</li>'
        r'<li>Khi $R_b$ chạy hết dải, số chỉ ampe kế biến thiên trong khoảng nào?</li>'
        r'<li>Có thể làm vôn kế chỉ $11\ \text{V}$ không? Vì sao?</li></ol>')),
    dict(label="Dạng 5 · Kết hợp · Mạch cầu cân bằng, chập hai điểm cùng điện thế", topic=TOPIC, problem_html=(
        r'<p>Giữa hai điểm M, N có hiệu điện thế không đổi $U=30\ \text{V}$ mắc hai nhánh song song: nhánh trái gồm $R_1=6\ \Omega$ nối tiếp $R_3=10\ \Omega$ (điểm nối P), '
        r'nhánh phải gồm $R_2=9\ \Omega$ nối tiếp $R_4$ chưa biết (điểm nối Q). Vôn kế lí tưởng mắc giữa P và Q chỉ $0\ \text{V}$.</p>'
        r'<ol type="a"><li>Tìm $R_4$.</li>'
        r'<li>Tính điện trở tương đương, cường độ dòng điện mạch chính và ở mỗi nhánh.</li>'
        r'<li>Thay vôn kế bằng điện trở $R_5=20\ \Omega$. Dòng điện qua $R_5$ bằng bao nhiêu? Điện trở tương đương có đổi không?</li>'
        r'<li>Tính lại điện trở tương đương bằng cách chập P với Q và so sánh.</li></ol>')),
    dict(label="Dạng 6 · Nâng cao · Mạch ba tầng, đọc ampe kế nhánh trong, tính ngược tìm điện trở chưa biết", topic=TOPIC, problem_html=(
        r'<p>Nguồn $U=24\ \text{V}$; $R_1=2\ \Omega$ nối tiếp đoạn X. Đoạn X gồm $R_2=12\ \Omega$ song song đoạn Y; đoạn Y gồm $R_3=4\ \Omega$ nối tiếp đoạn gồm $R_4=12\ \Omega$ song song $R_5$ chưa biết. '
        r'Ampe kế lí tưởng $A_1$ mắc nối tiếp $R_4$ chỉ $1\ \text{A}$; ampe kế lí tưởng $A_2$ ở nhánh chính.</p>'
        r'<ol type="a"><li>Tính $R_5$.</li>'
        r'<li>Tính số chỉ ampe kế $A_2$.</li></ol>')),
]

# ═════════════ PHÂN TÍCH ĐỀ ═════════════
ANALYSIS = [
    [  # D1
        ("“$R_1$ nối tiếp với đoạn song song gồm $R_2$ và $R_3$”", r"$R_1=4$, $R_2=15$, $R_3=10\ \Omega$", r"⚠ Nối tiếp: $I$ chung · song song: $U$ chung · $R_{td}=R_1+R_{23}$"),
        ("“mắc vào nguồn $U=30\ \text{V}$”", r"$U=30\ \text{V}$", r"⚠ Nguồn lí tưởng: $U$ là hiệu điện thế hai đầu cả mạch"),
        ("“ampe kế, vôn kế lí tưởng”", r"$R_A=0$, $R_V=\infty$", r"Ampe kế chỉ $I$ chính · vôn kế chỉ $U_{23}$"),
        ("a) “điện trở tương đương, số chỉ ampe kế”", "cần tìm $R_{td}$, $I$", r"$R_{td}=R_1+\dfrac{R_2R_3}{R_2+R_3}$ · $I=\dfrac U{R_{td}}$"),
        ("b) “số chỉ vôn kế, dòng qua $R_2$, $R_3$”", r"cần tìm $U_{23}$, $I_2$, $I_3$", r"$U_{23}=U-IR_1$ · $I_k=\dfrac{U_{23}}{R_k}$"),
        ("c) “thay $R_1$ để ampe kế chỉ $2\ \text{A}$”", r"$I'=2\ \text{A}$", r"$R_{td}'=\dfrac U{I'}$ · $R_1'=R_{td}'-R_{23}$"),
    ],
    [  # D2
        ("“$R_1$ nối tiếp $R_2$; vôn kế song song với $R_2$”", r"$R_1=30$, $R_2=60\ \Omega$", r"⚠ Vôn kế đo $U_2$ ; thực thì $R_V$ song song $R_2$"),
        ("“ampe kế nối tiếp”", "vị trí nhánh chính", r"⚠ Ampe kế thực: $R_A$ nối tiếp trong mạch"),
        ("a) “dụng cụ lí tưởng”", r"$R_A=0$, $R_V=\infty$", r"$I=\dfrac U{R_1+R_2}$ · $U_V=IR_2$"),
        ("b) “$R_V=60\ \Omega$”, “sai số tương đối”", r"$R_V=60\ \Omega$", r"$R_{doan}=\dfrac{R_2R_V}{R_2+R_V}$ · $\delta=\dfrac{U_{that}-U_{do}}{U_{that}}$"),
        ("c) “$R_A=3\ \Omega$”", r"$R_A=3\ \Omega$", r"$R_{td}=R_A+R_1+R_{doan}$"),
        ("d) “$R_V$ tối thiểu”, “không quá $1\%$”", r"$\delta\le1\%$", r"$U_V\ge0{,}99\,U_{that}$ ⇒ tìm $R_{doan}$ ⇒ tìm $R_V$"),
    ],
    [  # D3
        ("“K song song với $R_2$”", r"K nối hai đầu $R_2$", r"⚠ Hai đầu $R_2$ cũng là hai nút M, N của đoạn song song"),
        ("“K đóng chỉ $2\ \text{A}$”", r"$I_{dong}=2\ \text{A}$", r"K đóng: dây nối M với N ⇒ $R_{td}=R_1$ ⇒ $R_1=\dfrac U{I_{dong}}$"),
        ("“K mở chỉ $1{,}2\ \text{A}$”", r"$I_{mo}=1{,}2\ \text{A}$", r"$R_{td}=\dfrac U{I_{mo}}$ ⇒ $R_{23}=R_{td}-R_1$"),
        ("“$R_2=12\ \Omega$, $R_3$ chưa biết”", r"$R_2=12\ \Omega$", r"$\dfrac1{R_3}=\dfrac1{R_{23}}-\dfrac1{R_2}$"),
        ("c) “hiệu điện thế hai đầu $R_3$, dòng qua $R_2$”", "K mở", r"$U_{23}=I_{mo}R_{23}$ · $I_2=\dfrac{U_{23}}{R_2}$"),
    ],
    [  # D4
        ("“$R_1$ nối tiếp đoạn song song gồm $R_b$ và $R_2$”", r"$R_1=6$, $R_2=12\ \Omega$", r"⚠ $R_b$ và $R_2$ chung hai nút nên song song"),
        ("“$R_b$ từ $0$ đến $24\ \Omega$”", r"$0\le R_b\le24\ \Omega$", r"⚠ Nghiệm tìm được phải nằm trong khoảng này"),
        ("a) “$R_b=12\ \Omega$”", r"$R_b=12\ \Omega$", r"$R_{ss}=\dfrac{R_bR_2}{R_b+R_2}$ · $I=\dfrac U{R_1+R_{ss}}$"),
        ("b) “vôn kế chỉ $8\ \text{V}$”", r"$U_{ss}=8\ \text{V}$", r"$I=\dfrac{U-U_{ss}}{R_1}$ · $R_{ss}=\dfrac{U_{ss}}I$ · $\dfrac1{R_b}=\dfrac1{R_{ss}}-\dfrac1{R_2}$"),
        ("c) “biến thiên trong khoảng nào”", "hai đầu mút của $R_b$", r"$I$ nhỏ nhất khi $R_{td}$ lớn nhất ($R_b$ lớn nhất)"),
        ("d) “vôn kế chỉ $11\ \text{V}$ được không”", r"$U_{ss,max}=?$", r"$U_{ss}$ lớn nhất khi $R_{ss}$ lớn nhất"),
    ],
    [  # D5
        ("“hai nhánh song song M–N; vôn kế giữa P và Q”", r"$R_1=6$, $R_3=10$, $R_2=9\ \Omega$", r"⚠ Cầu: nhánh trái $R_1\to P\to R_3$, nhánh phải $R_2\to Q\to R_4$"),
        ("“vôn kế lí tưởng chỉ $0\ \text{V}$”", r"$U_{PQ}=0$", r"⚠ Cầu cân bằng: $R_1R_4=R_2R_3$"),
        ("a) “tìm $R_4$”", r"$R_4=?$", r"$R_4=\dfrac{R_2R_3}{R_1}$"),
        ("b) “điện trở tương đương, dòng mỗi nhánh”", "cần tìm $R_{td}$, $I_1$, $I_2$", r"$R_{td}=\dfrac{(R_1+R_3)(R_2+R_4)}{R_1+R_2+R_3+R_4}$ · $I_k=\dfrac U{R_{nhanh}}$"),
        ("c) “thay vôn kế bằng $R_5=20\ \Omega$”", r"$R_5=20\ \Omega$", r"$V_P=V_Q$ ⇒ $I_5=0$ ⇒ $R_{td}$ không đổi"),
        ("d) “chập P với Q”", "P ≡ Q", r"$(R_1\parallel R_2)+(R_3\parallel R_4)$"),
    ],
    [  # D6
        ("“$R_1$ nối tiếp X; X = $R_2$ // Y; Y = $R_3$ nối tiếp ($R_4$ // $R_5$)”", r"$R_1=2$, $R_2=12$, $R_3=4$, $R_4=12\ \Omega$", r"⚠ Thu gọn từ trong ra: $R_{45}\to Y\to X\to R_{td}$"),
        ("“$A_1$ nối tiếp $R_4$ chỉ $1\ \text{A}$”", r"$I_4=1\ \text{A}$", r"$U_{45}=I_4R_4$ (cũng là hiệu điện thế hai đầu $R_5$)"),
        ("“$R_5$ chưa biết”", r"$R_5=?$", r"⚠ Đặt $U_X$ là ẩn: $I=\dfrac{U_X}{R_2}+\dfrac{U_X-U_{45}}{R_3}$ và $U-U_X=IR_1$"),
        ("a) “tính $R_5$”", r"$R_5=?$", r"$I_5=I_Y-I_4$ · $R_5=\dfrac{U_{45}}{I_5}$"),
        ("b) “$A_2$ ở nhánh chính”", r"$A_2$ chỉ $I$", r"$I=I_2+I_Y$"),
    ],
]


# ═════════════ LỜI GIẢI ═════════════
SOLS = [
    sol([r"<strong>Khái niệm:</strong> nối tiếp thì $I$ chung ; song song thì $U$ chung.",
         r"<strong>Công thức:</strong> $R_{23}=\dfrac{R_2R_3}{R_2+R_3}$ ; $R_{td}=R_1+R_{23}$ ; $I=\dfrac U{R_{td}}$ ; $I_k=\dfrac{U_{23}}{R_k}$.",
         r"⚠ <strong>Điều kiện:</strong> ampe kế, vôn kế lí tưởng ; thu gọn từ trong ra ngoài, tính ngược từ ngoài vào trong."],
        [("Thu gọn đoạn song song", [P(r"$R_2$ và $R_3$ cùng nối vào hai nút M, N nên song song :"), M(r"R_{23}=\dfrac{R_2R_3}{R_2+R_3}"), M(r"R_{23}=\dfrac{15\cdot10}{15+10}"), A(r"R_{23}=6\ \Omega")]),
         ("Dòng điện mạch chính", [P(r"$R_1$ nối tiếp với $R_{23}$ :"), M(r"R_{td}=R_1+R_{23}=4+6=10\ \Omega"), M(r"I=\dfrac U{R_{td}}=\dfrac{30}{10}"), A(r"I=3\ \text{A}"), P("Ampe kế lí tưởng chỉ đúng $I$.")]),
         ("Hiệu điện thế đoạn song song", [P(r"Tính $U_1$ trước rồi suy ra $U_{23}$ :"), M(r"U_1=IR_1=3\cdot4=12\ \text{V}"), M(r"U_{23}=U-U_1=30-12"), A(r"U_{23}=18\ \text{V}"), P("Vôn kế lí tưởng chỉ $U_{23}$.")]),
         ("Dòng qua từng nhánh", [M(r"I_2=\dfrac{U_{23}}{R_2}=\dfrac{18}{15}"), A(r"I_2=1{,}2\ \text{A}"), M(r"I_3=\dfrac{U_{23}}{R_3}=\dfrac{18}{10}"), A(r"I_3=1{,}8\ \text{A}")]),
         ("Tính ngược: đổi $R_1$", [P(r"Ampe kế chỉ $2\ \text{A}$ thì điện trở cả mạch là :"), M(r"R_{td}'=\dfrac U{I'}=\dfrac{30}2=15\ \Omega"), P(r"$R_{23}$ vẫn nằm trong mạch nên :"), M(r"R_1'=R_{td}'-R_{23}=15-6"), A(r"R_1'=9\ \Omega")]),
         ("Kiểm tra", [P(r"$I_2+I_3=1{,}2+1{,}8=3\ \text{A}=I$ ✓ ; $U_1+U_{23}=12+18=30\ \text{V}=U$ ✓."), P(r"Câu c : $U_1'=2\cdot9=18\ \text{V}$ nên $U_{23}'=12\ \text{V}=2\cdot6$ ✓.")])],
        [r"a) $R_{td}=10\ \Omega$ ; ampe kế chỉ $3\ \text{A}$.", r"b) Vôn kế chỉ $18\ \text{V}$ ; $I_2=1{,}2\ \text{A}$, $I_3=1{,}8\ \text{A}$.", r"c) $R_1'=9\ \Omega$."],
        r"Nhận dạng : thấy <strong>nối tiếp với đoạn song song</strong> → thu gọn $R_{23}$ trước, cộng $R_1$, rồi tính ngược bằng $U_1=IR_1$ và $U_{23}=U-U_1$."),
    sol([r"<strong>Khái niệm:</strong> ampe kế thực có điện trở $R_A$ mắc nối tiếp ; vôn kế thực có điện trở $R_V$ mắc song song với đoạn đo.",
         r"<strong>Công thức:</strong> $R_{doan}=\dfrac{R_2R_V}{R_2+R_V}$ ; $\delta=\dfrac{U_{that}-U_{do}}{U_{that}}\cdot100\%$.",
         r"⚠ <strong>Điều kiện:</strong> $U_{that}$ là số chỉ của vôn kế lí tưởng (câu a) ; câu b, d ampe kế lí tưởng ; $R_V$ lớn thì sai số nhỏ."],
        [("Dụng cụ lí tưởng", [M(r"I=\dfrac U{R_1+R_2}=\dfrac{12}{90}=\dfrac2{15}\ \text{A}"), P("Ampe kế chỉ khoảng $0{,}133\ \text{A}$ ; vôn kế chỉ :"), M(r"U_V=IR_2=\dfrac2{15}\cdot60"), A(r"U_V=8\ \text{V}")]),
         ("Đưa $R_V$ vào sơ đồ", [P(r"Vôn kế thực song song với $R_2$ :"), M(r"R_{doan}=\dfrac{R_2R_V}{R_2+R_V}=\dfrac{60\cdot60}{120}"), A(r"R_{doan}=30\ \Omega")]),
         ("Số chỉ khi vôn kế thực", [M(r"R_{td}=R_1+R_{doan}=30+30=60\ \Omega"), M(r"I=\dfrac{12}{60}=0{,}2\ \text{A}"), M(r"U_V=IR_{doan}=0{,}2\cdot30"), A(r"U_V=6\ \text{V}"), M(r"\delta=\dfrac{8-6}8\cdot100\%=25\%")]),
         ("Thêm điện trở ampe kế", [M(r"R_{td}=R_A+R_1+R_{doan}=3+30+30=63\ \Omega"), M(r"I=\dfrac{12}{63}\approx0{,}190\ \text{A}"), M(r"U_V=IR_{doan}=\dfrac4{21}\cdot30"), A(r"U_V\approx5{,}71\ \text{V}"), P(r"Sai số $\approx28{,}6\%$ : ampe kế thực cũng làm vôn kế chỉ thấp đi.")]),
         ("Tìm $R_V$ tối thiểu", [P(r"$\delta\le1\%$ nghĩa là $U_V\ge0{,}99\cdot8=7{,}92\ \text{V}$ (ampe kế lí tưởng) :"), M(r"U_1=12-7{,}92=4{,}08\ \text{V}"), M(r"R_{doan}=R_1\dfrac{U_V}{U_1}=30\cdot\dfrac{7{,}92}{4{,}08}\approx58{,}24\ \Omega"),
                                   P(r"Rồi đảo công thức song song :"), M(r"\dfrac1{R_V}=\dfrac1{R_{doan}}-\dfrac1{R_2}=\dfrac1{58{,}24}-\dfrac1{60}"), A(r"R_V\approx1\,980\ \Omega")]),
         ("Kiểm tra", [P(r"Với $R_V=1\,980\ \Omega$ : $R_{doan}=\dfrac{60\cdot1980}{2040}\approx58{,}24\ \Omega$ ; $I=\dfrac{12}{88{,}24}\approx0{,}136\ \text{A}$ ; $U_V\approx7{,}92\ \text{V}$ ✓."), P(r"Vôn kế phải có điện trở cỡ $33$ lần $R_2$ mới sai số dưới $1\%$ : $R_V$ càng lớn càng chính xác.")])],
        [r"a) Ampe kế $\approx0{,}133\ \text{A}$ ; vôn kế $8\ \text{V}$.", r"b) Ampe kế $0{,}2\ \text{A}$ ; vôn kế $6\ \text{V}$ ; $\delta=25\%$.", r"c) Ampe kế $\approx0{,}190\ \text{A}$ ; vôn kế $\approx5{,}71\ \text{V}$.", r"d) $R_V\ge1\,980\ \Omega$."],
        r"Nhận dạng : thấy <strong>vôn kế, ampe kế có điện trở</strong> → vẽ $R_A$ nối tiếp, $R_V$ song song vào sơ đồ rồi giải như mạch thường."),
    sol([r"<strong>Khái niệm:</strong> khoá K đóng là dây dẫn : hai đầu K cùng điện thế (chập lại).",
         r"<strong>Công thức:</strong> $R_1=\dfrac U{I_{dong}}$ ; $R_{23}=\dfrac U{I_{mo}}-R_1$ ; $\dfrac1{R_3}=\dfrac1{R_{23}}-\dfrac1{R_2}$.",
         r"⚠ <strong>Điều kiện:</strong> K song song $R_2$ mà $R_2\parallel R_3$ thì K nối tắt cả đoạn song song, không chỉ $R_2$."],
        [("K đóng nối tắt những gì", [P(r"K nối hai đầu $R_2$, mà hai đầu $R_2$ cũng là hai nút M, N của đoạn song song."), P(r"K đóng : M và N cùng điện thế, nên $R_2$ và $R_3$ đều không có dòng ; chỉ $R_1$ còn trong mạch.")]),
         ("Tính $R_1$", [M(r"R_{td}=R_1,\quad I_{dong}=\dfrac U{R_1}"), M(r"R_1=\dfrac U{I_{dong}}=\dfrac{12}2"), A(r"R_1=6\ \Omega")]),
         ("Đoạn song song khi K mở", [M(r"R_{td}=\dfrac U{I_{mo}}=\dfrac{12}{1{,}2}=10\ \Omega"), M(r"R_{23}=R_{td}-R_1=10-6"), A(r"R_{23}=4\ \Omega")]),
         ("Tính $R_3$", [P(r"$R_{23}=4\ \Omega$ nhỏ hơn $R_2=12\ \Omega$ : hợp lí vì song song. Đảo công thức :"), M(r"\dfrac1{R_3}=\dfrac1{R_{23}}-\dfrac1{R_2}=\dfrac14-\dfrac1{12}=\dfrac16"), A(r"R_3=6\ \Omega")]),
         ("Số liệu khi K mở", [M(r"U_{23}=I_{mo}R_{23}=1{,}2\cdot4"), A(r"U_{23}=4{,}8\ \text{V}"), M(r"I_2=\dfrac{U_{23}}{R_2}=\dfrac{4{,}8}{12}=0{,}4\ \text{A}")]),
         ("Kiểm tra", [P(r"$I_3=\dfrac{4{,}8}6=0{,}8\ \text{A}$ ; $I_2+I_3=1{,}2\ \text{A}=I_{mo}$ ✓."), P(r"$U_1=1{,}2\cdot6=7{,}2\ \text{V}$ ; $U_1+U_{23}=12\ \text{V}=U$ ✓.")])],
        [r"a) Chỉ $R_1$ còn dòng ; $R_1=6\ \Omega$.", r"b) $R_3=6\ \Omega$.", r"c) $U_3=4{,}8\ \text{V}$ ; $I_2=0{,}4\ \text{A}$."],
        r"Nhận dạng : thấy <strong>khoá K nối hai nút</strong> → K đóng chập hai nút, nối tắt mọi thứ nằm giữa hai nút ; hai số chỉ ở hai trạng thái cho hai phương trình."),
    sol([r"<strong>Khái niệm:</strong> $R_b$ và $R_2$ chung hai nút nên song song ; $U_{ss}=U-IR_1$.",
         r"<strong>Công thức:</strong> $R_{ss}=\dfrac{R_bR_2}{R_b+R_2}$ ; $I=\dfrac U{R_1+R_{ss}}$ ; $\dfrac1{R_b}=\dfrac1{R_{ss}}-\dfrac1{R_2}$.",
         r"⚠ <strong>Điều kiện:</strong> nghiệm $R_b$ phải thoả $0\le R_b\le24\ \Omega$ ; $R_{ss}$ tăng khi $R_b$ tăng."],
        [("Đoạn song song khi $R_b=12$", [M(r"R_{ss}=\dfrac{12\cdot12}{12+12}"), A(r"R_{ss}=6\ \Omega")]),
         ("Số chỉ hai dụng cụ", [M(r"R_{td}=R_1+R_{ss}=6+6=12\ \Omega"), M(r"I=\dfrac{18}{12}"), A(r"I=1{,}5\ \text{A}"), M(r"U_{ss}=IR_{ss}=1{,}5\cdot6=9\ \text{V}"), P("Ampe kế chỉ $1{,}5\ \text{A}$ ; vôn kế chỉ $9\ \text{V}$.")]),
         ("Tính ngược cho vôn kế $8\ \text{V}$", [M(r"U_1=U-U_{ss}=18-8=10\ \text{V}"), M(r"I=\dfrac{U_1}{R_1}=\dfrac{10}6=\dfrac53\ \text{A}"), M(r"R_{ss}=\dfrac{U_{ss}}I=\dfrac{8}{5/3}=4{,}8\ \Omega"),
                                                M(r"\dfrac1{R_b}=\dfrac1{4{,}8}-\dfrac1{12}=\dfrac18"), A(r"R_b=8\ \Omega"), P("Nằm trong $0\\ldots24\\ \\Omega$ nên nhận.")]),
         ("Dòng nhỏ nhất", [P(r"$R_b$ càng lớn, $R_{ss}$ càng lớn, $R_{td}$ càng lớn, dòng càng nhỏ. Nhỏ nhất khi $R_b=24\ \Omega$ :"), M(r"R_{ss}=\dfrac{24\cdot12}{36}=8\ \Omega,\quad R_{td}=14\ \Omega"), M(r"I_{min}=\dfrac{18}{14}"), A(r"I_{min}\approx1{,}29\ \text{A}"),
                           P(r"Lớn nhất khi $R_b=0$ (nối tắt đoạn song song) : $I_{max}=\dfrac{18}6=3\ \text{A}$. Vậy $1{,}29\ \text{A}\le I\le3\ \text{A}$.")]),
         ("Vôn kế lớn nhất", [P(r"$U_{ss}$ lớn nhất khi $R_{ss}$ lớn nhất, tức $R_b=24\ \Omega$ :"), M(r"U_{ss,max}=U\dfrac{R_{ss}}{R_1+R_{ss}}=18\cdot\dfrac8{14}"), A(r"U_{ss,max}\approx10{,}29\ \text{V}"), P(r"Nhỏ hơn $11\ \text{V}$ nên <strong>không thể</strong> : $R_b\le24\ \Omega$ giới hạn $R_{ss}\le8\ \Omega$, phần còn lại của $U$ rơi trên $R_1$.")]),
         ("Kiểm tra", [P(r"Với $R_b=8\ \Omega$ : $R_{ss}=\dfrac{8\cdot12}{20}=4{,}8\ \Omega$ ; $I=\dfrac{18}{10{,}8}=\dfrac53\ \text{A}$ ; $U_{ss}=\dfrac53\cdot4{,}8=8\ \text{V}$ ✓."), P(r"$R_b=0$ cho vôn kế $0\ \text{V}$ ; $R_b=24$ cho $10{,}29\ \text{V}$ : vôn kế chỉ trong khoảng $0\ldots10{,}29\ \text{V}$.")])],
        [r"a) Ampe kế $1{,}5\ \text{A}$ ; vôn kế $9\ \text{V}$.", r"b) $R_b=8\ \Omega$.", r"c) $\dfrac97\ \text{A}\approx1{,}29\ \text{A}$ đến $3\ \text{A}$.", r"d) Không : vôn kế chỉ tối đa $\dfrac{72}7\approx10{,}29\ \text{V}$."],
        r"Nhận dạng : thấy <strong>biến trở chạy trong dải</strong> → xét hai đầu mút, nghiệm phải thuộc dải cho phép."),
    sol([r"<strong>Khái niệm:</strong> hai điểm cùng điện thế thì dòng qua phần tử nối giữa chúng bằng $0$ ; có thể bỏ nó hoặc chập hai điểm.",
         r"<strong>Công thức:</strong> cầu cân bằng khi $R_1R_4=R_2R_3$ ; $R_{td}=\dfrac{(R_1+R_3)(R_2+R_4)}{R_1+R_2+R_3+R_4}$.",
         r"⚠ <strong>Điều kiện:</strong> vôn kế lí tưởng chỉ $0$ nghĩa là $V_P=V_Q$, tức cầu cân bằng."],
        [("Điều kiện cầu cân bằng", [M(r"R_1R_4=R_2R_3\ \Rightarrow\ R_4=\dfrac{R_2R_3}{R_1}=\dfrac{9\cdot10}6"), A(r"R_4=15\ \Omega")]),
         ("Điện trở mỗi nhánh", [P(r"Hai điện trở cùng nhánh nối tiếp ; hai nhánh song song :"), M(r"R_{trai}=R_1+R_3=16\ \Omega"), M(r"R_{phai}=R_2+R_4=9+15"), A(r"R_{phai}=24\ \Omega")]),
         ("Điện trở tương đương", [M(r"R_{td}=\dfrac{R_{trai}R_{phai}}{R_{trai}+R_{phai}}=\dfrac{16\cdot24}{40}"), A(r"R_{td}=9{,}6\ \Omega")]),
         ("Dòng điện ở mỗi nhánh", [P(r"Cả nhánh chịu hiệu điện thế $U$ :"), M(r"I_{trai}=\dfrac U{R_{trai}}=\dfrac{30}{16}"), A(r"I_{trai}=1{,}875\ \text{A}"), M(r"I_{phai}=\dfrac{30}{24}=1{,}25\ \text{A}"), M(r"I=I_{trai}+I_{phai}=\dfrac{30}{9{,}6}=3{,}125\ \text{A}")]),
         ("Thay vôn kế bằng $R_5$", [P(r"$U_{PQ}=0$ vì cầu cân bằng ; cân bằng chỉ phụ thuộc $R_1\ldots R_4$, không phụ thuộc phần tử giữa P và Q :"), A(r"I_5=0"), P(r"Điện trở tương đương vẫn là $9{,}6\ \Omega$.")]),
         ("Kiểm tra bằng cách chập P với Q", [P(r"$(R_1\parallel R_2)+(R_3\parallel R_4)=\dfrac{6\cdot9}{15}+\dfrac{10\cdot15}{25}=3{,}6+6=9{,}6\ \Omega$ ✓."), P(r"Điện thế hai điểm P, Q so với N : $1{,}875\cdot10=18{,}75\ \text{V}$ và $1{,}25\cdot15=18{,}75\ \text{V}$ : bằng nhau ✓.")])],
        [r"a) $R_4=15\ \Omega$.", r"b) $R_{td}=9{,}6\ \Omega$ ; $I=3{,}125\ \text{A}$ ; $I_{trai}=1{,}875\ \text{A}$, $I_{phai}=1{,}25\ \text{A}$.", r"c) $I_5=0$ ; $R_{td}$ không đổi.", r"d) Chập P với Q cho $9{,}6\ \Omega$, trùng câu b."],
        r"Nhận dạng : thấy <strong>vôn kế chỉ 0 giữa hai điểm giữa của hai nhánh</strong> → cầu cân bằng, nhân chéo $R_1R_4=R_2R_3$ rồi bỏ nhánh PQ."),
    sol([r"<strong>Khái niệm:</strong> thu gọn từ trong ra : $R_{45}\to Y\to X\to R_{td}$ ; ampe kế lí tưởng là dây nối.",
         r"<strong>Công thức:</strong> $U_{45}=I_4R_4$ ; $I_Y=\dfrac{U_X-U_{45}}{R_3}$ ; $I=\dfrac{U_X}{R_2}+I_Y$ ; $U-U_X=IR_1$.",
         r"⚠ <strong>Điều kiện:</strong> $A_1$ chỉ dòng qua $R_4$ (không phải dòng qua cả nhánh Y và không phải dòng chính) ; $U_X$ là ẩn, giải một phương trình bậc nhất."],
        [("Hiệu điện thế hai đầu $R_4$", [M(r"U_{45}=I_4R_4=1\cdot12"), A(r"U_{45}=12\ \text{V}"), P(r"$R_5$ song song $R_4$ nên cũng có $12\ \text{V}$.")]),
         ("Giải ẩn $U_X$", [P(r"Đặt $U_X$ là hiệu điện thế hai đầu $R_2$ (hai nút M, N). $R_3$ chịu $U_X-12$ :"), M(r"I=\dfrac{U_X}{12}+\dfrac{U_X-12}4"), M(r"U-U_X=IR_1\ \Rightarrow\ 24-U_X=2\left(\dfrac{U_X}{12}+\dfrac{U_X-12}4\right)"),
                            M(r"24-U_X=\dfrac23U_X-6\ \Rightarrow\ \dfrac53U_X=30"), A(r"U_X=18\ \text{V}")]),
         ("Dòng qua $R_3$", [M(r"I_Y=\dfrac{U_X-U_{45}}{R_3}=\dfrac{18-12}4"), A(r"I_Y=1{,}5\ \text{A}")]),
         ("Tìm $R_5$", [P(r"Dòng $I_Y$ chia cho $R_4$ và $R_5$ :"), M(r"I_5=I_Y-I_4=1{,}5-1=0{,}5\ \text{A}"), M(r"R_5=\dfrac{U_{45}}{I_5}=\dfrac{12}{0{,}5}"), A(r"R_5=24\ \Omega")]),
         ("Số chỉ $A_2$", [M(r"I_2=\dfrac{U_X}{R_2}=\dfrac{18}{12}=1{,}5\ \text{A}"), M(r"I=I_2+I_Y=1{,}5+1{,}5"), A(r"I=3\ \text{A}")]),
         ("Kiểm tra", [P(r"$U_1=IR_1=3\cdot2=6\ \text{V}$ ; $U_1+U_X=6+18=24\ \text{V}=U$ ✓."), P(r"Thu gọn lại : $R_{45}=\dfrac{12\cdot24}{36}=8\ \Omega$ ; $Y=4+8=12\ \Omega$ ; $X=\dfrac{12\cdot12}{24}=6\ \Omega$ ; $R_{td}=2+6=8\ \Omega$ ; $I=\dfrac{24}8=3\ \text{A}$ ✓.")])],
        [r"a) $R_5=24\ \Omega$.", r"b) Ampe kế $A_2$ chỉ $3\ \text{A}$."],
        r"Nhận dạng : thấy <strong>số chỉ ampe kế ở nhánh trong và một điện trở chưa biết</strong> → đặt hiệu điện thế một đoạn làm ẩn, lập phương trình dòng ở nút."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC ═════════════
def ke3(ok, w1, v1, w2, v2):
    return [(ok, True), (w1, v1), (w2, v2)]

STEPS = [
    dict(nhan_dang=r"Thấy <b>nối tiếp với đoạn song song</b> → thu gọn <b>$R_{23}$</b> trước, rồi <b>$I=U/R_{td}$</b> và tính ngược.",
         cap_do=1, fading="mo_het", go_roi=dict(buoc_hay_sai=0), buoc=[
        buoc("Thu gọn đoạn song song", r"Điện trở tương đương $R_{23}$ của đoạn $R_2\parallel R_3$ bằng bao nhiêu?", 6, "Ω", .05,
             r"Cộng $15+10$ như mạch nối tiếp, hoặc cộng $\tfrac1{15}+\tfrac1{10}$ rồi quên đảo ngược."),
        buoc("Dòng điện mạch chính", "Ampe kế chỉ bao nhiêu?", 3, "A", .02,
             r"Lấy $U$ chia cho $R_1$ hoặc cho $R_{23}$ thay vì cho $R_{td}=R_1+R_{23}$."),
        buoc("Hiệu điện thế đoạn song song", "Vôn kế chỉ bao nhiêu?", 18, "V", .1,
             r"Cho vôn kế chỉ bằng $U$ của nguồn hoặc bằng $U_1$: vôn kế đo đoạn song song, tức $U-U_1$."),
        buoc("Dòng qua từng nhánh", r"Cường độ dòng điện qua $R_2$ bằng bao nhiêu?", 1.2, "A", .02,
             r"Dùng dòng mạch chính cho $R_2$, hoặc chia $U$ (không phải $U_{23}$) cho $R_2$."),
        buoc(r"Tính ngược: đổi $R_1$", r"Phải thay $R_1$ bằng bao nhiêu để ampe kế chỉ $2\ \text{A}$?", 9, "Ω", .1,
             r"Cho $R_1'=\dfrac{U}{I'}$ mà quên $R_{23}$ vẫn nằm trong mạch."),
        buoc("Kiểm tra")]),
    dict(nhan_dang=r"Thấy <b>vôn kế, ampe kế có điện trở</b> → vẽ <b>$R_A$ nối tiếp, $R_V$ song song</b> vào sơ đồ rồi giải.",
         cap_do=2, fading="giau_buoc_cuoi", go_roi=dict(buoc_hay_sai=1), buoc=[
        buoc("Dụng cụ lí tưởng", "Vôn kế lí tưởng chỉ bao nhiêu?", 8, "V", .1,
             r"Lấy luôn $U=12\ \text{V}$ của nguồn cho vôn kế : $R_1$ cũng chịu một phần hiệu điện thế."),
        buoc(r"Đưa $R_V$ vào sơ đồ", r"Điện trở của đoạn gồm $R_2$ song song với vôn kế bằng bao nhiêu?", 30, "Ω", .2,
             r"Cộng $R_2+R_V$ như nối tiếp: vôn kế đo hai đầu $R_2$ nên song song với $R_2$."),
        buoc("Số chỉ khi vôn kế thực", "Vôn kế thực chỉ bao nhiêu?", 6, "V", .05,
             r"Vẫn dùng $R_2=60\ \Omega$ làm điện trở của đoạn đo, nên cho kết quả $8\ \text{V}$ như câu a."),
        buoc("Thêm điện trở ampe kế", r"Với $R_A=3\ \Omega$ thì vôn kế chỉ bao nhiêu?", 5.71, "V", .02,
             r"Quên cộng $R_A$ vào $R_{td}$, hoặc cộng $R_A$ vào đoạn song song thay vì vào mạch chính."),
        buoc(r"Tìm $R_V$ tối thiểu", r"$R_V$ tối thiểu bằng bao nhiêu để sai số không quá $1\%$?", 1980, "Ω", 10,
             r"Giải ngược sai: lấy $U_V=0{,}99\,U$ (bỏ $R_1$) hoặc quên đảo công thức song song khi tìm $R_V$.",
             ke=ke3(r"Đặt $U_V\ge0{,}99$ lần số chỉ lí tưởng, suy $U_1$, $R_{doan}$, rồi đảo công thức song song tìm $R_V$",
                    r"Cho $R_V=\infty$ vì sai số nhỏ nhất", r"$R_V=\infty$ là vôn kế lí tưởng chứ không phải giá trị cần tìm ; đề hỏi $R_V$ nhỏ nhất vẫn đạt $1\%$.",
                    r"Cho $R_V=100\,R_2$ vì $1\%=\tfrac1{100}$", r"Đó chỉ là điều kiện đủ ước chừng, không phải giá trị tối thiểu ; phải tính từ $U_V=0{,}99$ lần giá trị thật."))
        , buoc("Kiểm tra")]),
    dict(nhan_dang=r"Thấy <b>khoá K nối hai nút của đoạn song song</b> → K đóng <b>nối tắt cả đoạn</b> ; hai số chỉ cho hai phương trình.",
         cap_do=2, fading="giau_buoc_cuoi", go_roi=dict(buoc_hay_sai=0), buoc=[
        buoc("K đóng nối tắt những gì", "Khi K đóng, những điện trở nào còn có dòng điện chạy qua?", loi=r"Cho rằng K chỉ nối tắt $R_2$ vì nó đứng cạnh $R_2$, bỏ qua việc hai đầu $R_2$ cũng là hai nút của $R_3$.",
             lua_chon=[(r"Chỉ $R_1$", True), (r"$R_1$ và $R_3$ (chỉ $R_2$ bị nối tắt)", r"$R_3$ nối vào đúng hai nút M, N như $R_2$, nên cũng bị K nối tắt."), (r"Cả $R_1$, $R_2$, $R_3$", r"K đóng là dây dẫn nối M với N ; dòng chọn đường dây, không qua $R_2$ và $R_3$.")]),
        buoc(r"Tính $R_1$", r"Điện trở $R_1$ bằng bao nhiêu?", 6, "Ω", .05,
             r"Dùng $I=\dfrac{U}{R_1+R_2}$ hoặc $R_1+R_3$ : sai vì chỉ còn $R_1$ trong mạch."),
        buoc("Đoạn song song khi K mở", r"Khi K mở, điện trở $R_{23}$ của đoạn song song bằng bao nhiêu?", 4, "Ω", .05,
             r"Quên trừ $R_1$ : lấy $R_{23}=\dfrac U{I_{mo}}$.",
             ke=ke3(r"$R_{td}=\dfrac U{I_{mo}}$ rồi trừ $R_1$", r"$R_{23}=\dfrac U{I_{mo}}$", r"$\dfrac U{I_{mo}}$ là điện trở của cả mạch, còn gồm cả $R_1$ nối tiếp.", r"$R_{23}=R_1\cdot\dfrac{I_{dong}}{I_{mo}}$", r"Biểu thức này bằng chính $R_{td}$ (còn gồm $R_1$) ; $R_{23}$ phải lấy từ $R_{td}-R_1$.")),
        buoc(r"Tính $R_3$", r"$R_3$ bằng bao nhiêu?", 6, "Ω", .05,
             r"Cho $R_3=R_{23}-R_2$ hoặc $R_3=R_{23}$ : nhầm công thức song song với nối tiếp.",
             ke=ke3(r"Đảo công thức song song : $\dfrac1{R_3}=\dfrac1{R_{23}}-\dfrac1{R_2}$", r"$R_3=R_{23}-R_2$", r"Công thức nối tiếp : đoạn này là song song nên điện trở thành phần lớn hơn $R_{23}$.", r"$R_3=R_{23}\cdot R_2$", r"Không có công thức nhân đó ; điện trở song song là tích chia tổng.")),
        buoc("Số liệu khi K mở", r"Hiệu điện thế giữa hai đầu $R_3$ khi K mở bằng bao nhiêu?", 4.8, "V", .05,
             r"Lấy $U_3=U=12\ \text{V}$ hoặc $U_3=I_{mo}R_3$ (dòng chính nhân $R_3$ : dòng qua $R_3$ chỉ là một phần).",
             ke=ke3(r"$U_3=U_{23}=I_{mo}R_{23}$", r"$U_3=I_{mo}R_3$", r"$I_{mo}$ là dòng mạch chính, chưa phải dòng qua $R_3$.", r"$U_3=U-I_{mo}R_2$", r"Hiệu điện thế trên $R_1$ mới là $I_{mo}R_1$ ; $R_2$ song song với $R_3$ chứ không nối tiếp.")),
        buoc("Kiểm tra")]),
    dict(nhan_dang=r"Thấy <b>biến trở chạy trong dải</b> → thu gọn <b>$R_{ss}$</b>, xét hai đầu mút, nghiệm phải thuộc dải cho phép.",
         cap_do=3, fading="giau_tu_buoc_2", go_roi=dict(buoc_hay_sai=2), buoc=[
        buoc(r"Đoạn song song khi $R_b=12$", r"Điện trở của đoạn gồm $R_b$ song song $R_2$ bằng bao nhiêu?", 6, "Ω", .05,
             r"Cộng $R_b+R_2$ như nối tiếp."),
        buoc("Số chỉ hai dụng cụ", "Ampe kế chỉ bao nhiêu?", 1.5, "A", .02,
             r"Cộng cả ba điện trở hoặc lấy $\dfrac U{R_{ss}}$ thay vì $\dfrac U{R_1+R_{ss}}$.",
             ke=ke3(r"$R_{td}=R_1+R_{ss}$ rồi $I=\dfrac U{R_{td}}$", r"$R_{td}=R_1+R_b+R_2$", r"$R_b$ và $R_2$ chung hai nút nên song song, không cộng.", r"$I=\dfrac U{R_{ss}}$", r"$R_{ss}$ chỉ là một phần của mạch ; hiệu điện thế hai đầu nó nhỏ hơn $U$ vì còn $R_1$.")),
        buoc("Tính ngược cho vôn kế $8\ \text{V}$", r"Phải chỉnh $R_b$ bằng bao nhiêu để vôn kế chỉ $8\ \text{V}$?", 8, "Ω", .1,
             r"Cho $I=\dfrac U{R_1}$ rồi $R_b=\dfrac{U_{ss}}I$ : quên $R_2$ song song và $U_1$ chỉ là $U-U_{ss}$.",
             ke=ke3(r"$U_1=U-U_{ss}$, rồi $I$, rồi $R_{ss}=\dfrac{U_{ss}}I$, rồi đảo công thức song song tìm $R_b$", r"Cho $I=\dfrac U{R_1}$", r"$R_1$ chỉ chịu $U-U_{ss}$ chứ không chịu toàn bộ $U$.", r"Cho $R_b=R_{ss}$", r"$R_{ss}$ là điện trở của $R_b$ song song $R_2$, nhỏ hơn $R_b$ ; phải đảo công thức song song.")),
        buoc("Dòng nhỏ nhất", "Ampe kế chỉ nhỏ nhất bằng bao nhiêu?", 1.29, "A", .01,
             r"Chọn $R_b=0$ cho dòng nhỏ nhất : đó là lúc đoạn song song bị nối tắt và dòng lớn nhất.",
             ke=ke3(r"Dòng nhỏ nhất khi $R_{td}$ lớn nhất, tức $R_b$ lớn nhất", r"Dòng nhỏ nhất khi $R_b=0$", r"$R_b=0$ làm đoạn song song bị nối tắt, $R_{td}$ nhỏ nhất, dòng lớn nhất.", r"Dòng nhỏ nhất khi $R_b$ chỉ bằng nửa dải", r"$R_{td}$ tăng đơn điệu theo $R_b$ nên cực trị chỉ nằm ở hai đầu mút của dải.")),
        buoc("Vôn kế lớn nhất", "Vôn kế chỉ lớn nhất bằng bao nhiêu?", 10.29, "V", .02,
             r"Cho vôn kế chỉ tới $U$ của nguồn : quên $R_1$ còn chịu một phần hiệu điện thế.",
             ke=ke3(r"$U_{ss}$ lớn nhất khi $R_{ss}$ lớn nhất, tức $R_b=24\ \Omega$", r"$U_{ss}$ lớn nhất khi $R_b=0$", r"$R_b=0$ nối tắt đoạn song song nên $U_{ss}=0$.", r"$U_{ss}$ có thể bằng $U$ khi $R_b$ rất lớn", r"Còn $R_b\le24\ \Omega$ nên $R_{ss}\le8\ \Omega$ ; $R_1$ luôn chịu một phần hiệu điện thế.")),
        buoc("Kiểm tra")]),
    dict(nhan_dang=r"Thấy <b>vôn kế chỉ 0 giữa hai điểm giữa của hai nhánh</b> → cầu cân bằng, nhân chéo, <b>bỏ nhánh PQ</b>.",
         cap_do=3, fading="giau_tu_buoc_2", go_roi=dict(buoc_hay_sai=0), buoc=[
        buoc("Điều kiện cầu cân bằng", r"$R_4$ bằng bao nhiêu?", 15, "Ω", .1,
             r"Nhân chéo sai cặp : $R_4=\dfrac{R_1R_3}{R_2}$, hoặc cộng thay vì nhân."),
        buoc("Điện trở mỗi nhánh", "Điện trở của nhánh phải ($R_2$ rồi $R_4$) bằng bao nhiêu?", 24, "Ω", .1,
             r"Coi $R_2$ và $R_4$ song song : hai điện trở cùng nhánh nối tiếp nhau.",
             ke=ke3(r"Hai điện trở cùng nhánh nối tiếp : cộng", r"$R_2$ và $R_4$ song song : tích chia tổng", r"Cùng nhánh thì dòng đi qua lần lượt cả hai điện trở, tức nối tiếp.", r"Chỉ lấy $R_4$", r"Dòng đi qua cả $R_2$ lẫn $R_4$ nên phải cộng cả hai.")),
        buoc("Điện trở tương đương", "Điện trở tương đương của cả mạch bằng bao nhiêu?", 9.6, "Ω", .05,
             r"Cộng cả bốn điện trở hoặc tính $(R_1\parallel R_3)+(R_2\parallel R_4)$.",
             ke=ke3(r"Hai nhánh (mỗi nhánh nối tiếp) song song nhau, bỏ nhánh PQ", r"Cộng cả bốn : $R_1+R_2+R_3+R_4$", r"Đó là nối tiếp cả bốn ; hai nhánh có chung hai nút M, N nên song song.", r"$(R_1\parallel R_3)+(R_2\parallel R_4)$", r"$R_1$ và $R_3$ cùng nhánh nên nối tiếp, không song song.")),
        buoc("Dòng điện ở mỗi nhánh", r"Dòng điện qua nhánh trái ($R_1$ nối tiếp $R_3$) bằng bao nhiêu?", 1.875, "A", .01,
             r"Chia $U$ cho $R_1$ thay vì cho $R_1+R_3$, hoặc chia đều dòng chính cho hai nhánh.",
             ke=ke3(r"$I_{trai}=\dfrac U{R_1+R_3}$ vì cả nhánh chịu $U$", r"$I_{trai}=\dfrac U{R_1}$", r"$R_1$ chỉ là một phần của nhánh ; hiệu điện thế hai đầu $R_1$ nhỏ hơn $U$.", r"Dòng chính chia đều cho hai nhánh", r"Dòng chia theo điện trở (tỉ lệ nghịch) ; hai nhánh có điện trở khác nhau nên dòng khác nhau.")),
        buoc("Thay vôn kế bằng $R_5$", r"Dòng điện qua $R_5$ bằng bao nhiêu?", 0, "A", .005,
             r"Dùng $\dfrac U{R_5}$ hoặc hiệu hai dòng nhánh : dòng qua $R_5$ chỉ phụ thuộc hiệu điện thế giữa P và Q.",
             ke=ke3(r"$V_P=V_Q$ vì cầu cân bằng nên không có dòng qua $R_5$", r"$I_5=\dfrac U{R_5}$", r"$R_5$ không nối trực tiếp vào hai cực nguồn ; nó chỉ chịu $U_{PQ}$.", r"$I_5=I_{trai}-I_{phai}$", r"Hiệu hai dòng nhánh không phải dòng qua $R_5$ ; dòng qua $R_5$ do $U_{PQ}$ quyết định.")),
        buoc("Kiểm tra bằng cách chập P với Q")]),
    dict(nhan_dang=r"Thấy <b>ampe kế ở nhánh trong, điện trở chưa biết</b> → lấy <b>hiệu điện thế một đoạn làm ẩn</b>, lập phương trình dòng.",
         cap_do=4, fading="giau_het", go_roi=dict(buoc_hay_sai=1), buoc=[
        buoc("Hiệu điện thế hai đầu $R_4$", r"Hiệu điện thế hai đầu $R_4$ bằng bao nhiêu?", 12, "V", .1,
             r"Lấy $U_{45}=U$ hoặc dùng dòng của ampe kế $A_2$ thay vì $A_1$."),
        buoc(r"Giải ẩn $U_X$", r"Hiệu điện thế giữa hai nút M và N (hai đầu $R_2$) bằng bao nhiêu?", 18, "V", .1,
             r"Coi dòng chính bằng số chỉ $A_1$ : thiếu dòng qua $R_2$ và qua $R_5$.",
             ke=ke3(r"Đặt $U_X$ làm ẩn : $I=\dfrac{U_X}{R_2}+\dfrac{U_X-U_{45}}{R_3}$ và $U-U_X=IR_1$", r"Cho dòng chính bằng số chỉ $A_1$", r"$A_1$ chỉ dòng qua $R_4$, chỉ là một phần của dòng nhánh Y ; dòng chính còn gồm cả nhánh $R_2$.", r"Cho $U_X=U-U_{45}$", r"$U_{45}$ là hiệu điện thế hai đầu $R_4$ chứ không phải hiệu điện thế rơi trên $R_1$.")),
        buoc("Dòng qua $R_3$", r"Dòng điện qua $R_3$ bằng bao nhiêu?", 1.5, "A", .02,
             r"Chia cả $U_X$ cho $R_3$ : $R_3$ chỉ chịu $U_X-U_{45}$.",
             ke=ke3(r"$I_Y=\dfrac{U_X-U_{45}}{R_3}$", r"$I_Y=\dfrac{U_X}{R_3}$", r"$R_3$ chỉ chịu một phần của $U_X$ ; phần còn lại nằm trên $R_4\parallel R_5$.", r"$I_Y=I_4$", r"Dòng qua $R_3$ gồm cả dòng qua $R_4$ lẫn dòng qua $R_5$.")),
        buoc(r"Tìm $R_5$", r"$R_5$ bằng bao nhiêu?", 24, "Ω", .2,
             r"Chia $U_{45}$ cho dòng $I_Y$ (tổng hai nhánh) thay vì cho riêng dòng qua $R_5$.",
             ke=ke3(r"$I_5=I_Y-I_4$ rồi $R_5=\dfrac{U_{45}}{I_5}$", r"$R_5=\dfrac{U_{45}}{I_Y}$", r"$I_Y$ là tổng dòng qua $R_4$ và $R_5$ ; phải trừ phần của $R_4$.", r"$R_5=R_4$ vì cùng hiệu điện thế", r"Cùng hiệu điện thế chỉ cho cùng điện trở khi cùng dòng điện, mà dòng qua $R_4$ và $R_5$ khác nhau.")),
        buoc("Số chỉ $A_2$", r"Ampe kế $A_2$ chỉ bao nhiêu?", 3, "A", .02,
             r"Lấy $I=I_Y$ : bỏ sót dòng qua $R_2$.",
             ke=ke3(r"$I=I_2+I_Y$", r"$I=I_Y$", r"Dòng chính còn chia vào nhánh $R_2$.", r"$I=\dfrac U{R_1+R_2}$", r"$R_2$ song song với Y chứ không nối tiếp $R_1$.")),
        buoc("Kiểm tra")]),
]


# ═════════════ BÀI TẬP TỰ LUẬN ═════════════
def tu_luan():
    r = Fr(6)
    assert sorted({3 * r, 3 * r / 2, 2 * r / 3, r / 3}) == [2, 4, 9, 18]
    mx = max(x * (60 - x) / 60 for x in range(1, 60)); assert mx == 15
    # bài 3
    Rss3 = par(30, 60); assert (Fr(18) / (10 + Rss3), Fr(18) / (10 + Rss3) * Rss3, Fr(18) / 10) == (Fr(3, 5), 12, Fr(9, 5))
    # bài 4: vôn kế nối tiếp
    I4_ = Fr(9) / (12 + 6 + 600); assert (float(I4_ * 600), float(I4_ * 12), float(I4_ * 6)) == (9 * 600 / 618, 9 * 12 / 618, 9 * 6 / 618)
    # bài 5: cầu đối xứng r = 6
    assert par(12, 12) == 6 and Fr(12, 6) == 2
    # bài 6
    I1, I2 = Fr(18, 45), Fr(18, 40); assert (I1 * 15, I2 * 10, I2 * 10 - I1 * 15 + 0 * 1) == (6, Fr(9, 2), Fr(-3, 2)) and I1 * 15 - I2 * 10 == Fr(3, 2)
    B = []
    def bai(k, muc, de, loi):
        B.append(f'<h4>Bài {k} · {muc}</h4><p>{de}</p><details><summary>Hướng dẫn giải</summary>{loi}</details>')
    bai(1, "Dễ", r"Có ba điện trở giống nhau, mỗi điện trở $r=6\ \Omega$. Dùng cả ba điện trở, hãy kể mọi cách ghép và tính điện trở tương đương của mỗi cách.",
        r"<p>Bốn cách :</p><p>Cả ba nối tiếp : $3r=18\ \Omega$.</p><p>Hai song song rồi nối tiếp điện trở thứ ba : $\dfrac r2+r=\dfrac{3r}2=9\ \Omega$.</p>"
        r"<p>Hai nối tiếp rồi song song điện trở thứ ba : $\dfrac{2r\cdot r}{3r}=\dfrac{2r}3=4\ \Omega$.</p><p>Cả ba song song : $\dfrac r3=2\ \Omega$.</p>"
        r"<p>Kiểm tra : $18\gt9\gt4\gt2$ ; không có cách nào cho $3\ \Omega$.</p>")
    bai(2, "Trung bình", r"Một dây dẫn có điện trở $R=60\ \Omega$ được cắt thành hai đoạn có điện trở $x$ và $60-x$ (đơn vị ôm). a) Viết biểu thức điện trở tương đương khi mắc hai đoạn song song. b) Tìm $x$ để điện trở này lớn nhất và tính giá trị đó. c) Nếu mắc nối tiếp thì sao?",
        r"<p>a) $R_{td}=\dfrac{x(60-x)}{60}$.</p><p>b) Hai số dương $x$ và $60-x$ có tổng không đổi nên tích lớn nhất khi $x=60-x$, tức $x=30\ \Omega$.</p>"
        r"<p>$R_{td,max}=\dfrac{30\cdot30}{60}=15\ \Omega$ (bằng $\dfrac R4$).</p><p>c) Nối tiếp : $R_{td}=60\ \Omega$ với mọi $x$.</p>")
    bai(3, "Trung bình", r"Nguồn $U=18\ \text{V}$. Biến trở $R_b=10\ \Omega$ nối tiếp với đoạn song song gồm $R_1=30\ \Omega$ và $R_2=60\ \Omega$. Ampe kế lí tưởng ở nhánh chính; vôn kế lí tưởng song song đoạn song song. Khoá K mắc song song với $R_2$. Tính số chỉ hai dụng cụ khi a) K mở, b) K đóng. Nhận xét.",
        r"<p>a) K mở : $R_{ss}=\dfrac{30\cdot60}{90}=20\ \Omega$ ; $R_{td}=10+20=30\ \Omega$ ; $I=\dfrac{18}{30}=0{,}6\ \text{A}$ ; $U_V=0{,}6\cdot20=12\ \text{V}$.</p>"
        r"<p>b) K nối hai đầu $R_2$, cũng là hai nút của đoạn song song, nên K đóng nối tắt <strong>cả</strong> $R_1$ và $R_2$. Còn $R_{td}=R_b=10\ \Omega$ ; $I=\dfrac{18}{10}=1{,}8\ \text{A}$ ; $U_V=0$.</p>"
        r"<p>Nhận xét : đóng khoá làm điện trở giảm từ $30$ xuống $10\ \Omega$, dòng tăng từ $0{,}6$ lên $1{,}8\ \text{A}$.</p>")
    bai(4, "Khó", r"Nguồn $U=9\ \text{V}$; $R_1=12\ \Omega$ nối tiếp $R_2=6\ \Omega$. Do mắc nhầm, một vôn kế có $R_V=600\ \Omega$ được mắc <strong>nối tiếp</strong> với cả hai điện trở. Tính số chỉ của vôn kế, hiệu điện thế trên mỗi điện trở và nhận xét.",
        r"<p>$R_{td}=12+6+600=618\ \Omega$ ; $I=\dfrac9{618}\approx0{,}01456\ \text{A}$.</p><p>Vôn kế : $U_V=I\cdot600\approx8{,}74\ \text{V}$, gần bằng $U$ của nguồn.</p>"
        r"<p>$U_1=I\cdot12\approx0{,}175\ \text{V}$ ; $U_2=I\cdot6\approx0{,}087\ \text{V}$.</p><p>Nhận xét : vôn kế nối tiếp là điện trở rất lớn, dòng gần bằng $0$ nên hai điện trở gần như không có hiệu điện thế (mạch coi như hở).</p>")
    bai(5, "Khó", r"Bốn điện trở giống nhau $r=6\ \Omega$ ghép thành cầu : nhánh trái gồm $R_1$ rồi $R_3$ (điểm nối P), nhánh phải gồm $R_2$ rồi $R_4$ (điểm nối Q). Điện trở $R_5=10\ \Omega$ nối P với Q, nguồn $U=12\ \text{V}$ nối hai đầu cầu. Tính điện trở tương đương, dòng mạch chính và dòng qua $R_5$.",
        r"<p>Hai nhánh giống hệt nhau nên $V_P=V_Q$ (đối xứng) : cầu cân bằng, $I_5=0$ dù $R_5$ lớn nhỏ thế nào.</p><p>Mỗi nhánh $12\ \Omega$ ; $R_{td}=\dfrac{12\cdot12}{24}=6\ \Omega$ ; $I=\dfrac{12}6=2\ \text{A}$.</p>"
        r"<p>Kiểm tra bằng chập P với Q : $(r\parallel r)+(r\parallel r)=3+3=6\ \Omega$ ✓.</p>")
    bai(6, "Nâng cao", r"Cực dương nguồn $U=18\ \text{V}$ nối M, cực âm nối N. Nhánh trái gồm $R_1=15\ \Omega$ rồi $R_3=30\ \Omega$ (điểm nối P). Nhánh phải gồm $R_2=10\ \Omega$ rồi $R_4=30\ \Omega$ (điểm nối Q). Vôn kế lí tưởng nối P với Q. Vôn kế chỉ bao nhiêu và điểm nào có điện thế cao hơn?",
        r"<p>$\dfrac{R_1}{R_2}=1{,}5\neq\dfrac{R_3}{R_4}=1$ : cầu <strong>không</strong> cân bằng.</p><p>Nhánh trái : $I_1=\dfrac{18}{45}=0{,}4\ \text{A}$ ; $U_{MP}=0{,}4\cdot15=6\ \text{V}$.</p>"
        r"<p>Nhánh phải : $I_2=\dfrac{18}{40}=0{,}45\ \text{A}$ ; $U_{MQ}=0{,}45\cdot10=4{,}5\ \text{V}$.</p><p>Từ M (điện thế cao hơn) xuống P giảm $6\ \text{V}$, xuống Q chỉ giảm $4{,}5\ \text{V}$ nên Q cao hơn P : vôn kế chỉ $6-4{,}5=1{,}5\ \text{V}$.</p>")
    return dict(label="Bài tập tự luận (xếp từ dễ đến khó)", body_html="<p>Các bài còn lại của chuyên đề, xếp từ dễ đến khó. Tự giải trên giấy rồi mới mở hướng dẫn.</p>" + "".join(B))


write(J, 157, "Chuyên đề 04. Đoạn mạch nối tiếp, song song, hỗn hợp", DANG, BUILD, ANALYSIS, SOLS, tu_luan())
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
def _fix(o):
    if isinstance(o, str): return o.replace("\text", "\\text").replace("\t", "\\t") if False else o.replace("\t" + "ext", "\\text")
    if isinstance(o, list): return [_fix(x) for x in o]
    if isinstance(o, dict): return {k: _fix(v) for k, v in o.items()}
    return o
d = _fix(d)   # chuỗi không raw chứa "\text" bị Python đổi thành TAB+"ext"
d["generated_at"] = "2026-10-12"
d["review"] = {"checked": True, "notes": "Kiểm chéo độc lập (kiem-code) 12/10/2026: tự giải lại 6 dạng + 6 bài tự luận khớp; đã sửa lỗi TAB trong \\text, R1' trong đề, vi_sao D3 bước 3, lí do D4 câu d, ký hiệu tự luận bài 6."}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
