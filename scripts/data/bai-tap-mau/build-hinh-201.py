"""Bài tập mẫu lesson 201 "Chủ đề thêm. Từ trường ngoài SGK hay gặp trong đề thi" (Vật lí 12, Ch.3 Từ trường).
4 mảng ngoài SGK GDPT 2018 mà đề thi thử trường/sở hay ra (đề thường cho sẵn công thức): dòng điện thẳng, ống dây,
hai dòng điện song song, hạt mang điện trong từ trường (khối phổ kế) + thanh trượt trên ray.
Chuẩn "một dạng — một hình": hình duy nhất = cong_cu (họ tu_truong, de:true), không <figure> trong problem/analysis.
Ký hiệu thống nhất lý thuyết: B = 2·10⁻⁷ I/r ; ống dây B = 4π·10⁻⁷ (N/ℓ) I ; F = 2·10⁻⁷ I₁I₂ℓ/r ; f = |q|vB sinα ; e = Bvℓ.
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-201.py   (idempotent; không ghi DB)."""
import json, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import write, inject, sol, buoc, M, P, A

J = os.path.join(HERE, "201.json")
T_DONG = "Từ trường của nam châm và của dòng điện"
T_THONG = "Từ thông qua khung dây"
T_LUC = "Tính lực từ F = BIl·sinθ"
T_HAT = "Lực từ. Cảm ứng từ"
T_THANH = "Suất điện động do thanh dẫn chuyển động"

# ═════════════ SỐ LIỆU (tự giải lại, assert khớp dap_so) ═════════════
def r2(x): return round(x + 1e-12, 2)
# D1 — dây thẳng I = 5,0 A ; OM = 4,0 cm ; ON = 12 cm
BM = 2e-7 * 5.0 / 0.040 * 1e6; BN = 2e-7 * 5.0 / 0.12 * 1e6
# D2 — ống dây ℓ = 40 cm, D = 4,0 cm, dây d = 0,80 mm quấn sát một lớp, I = 2,0 A
n2 = 1 / 0.80e-3; N2 = 0.40 / 0.80e-3; B2 = 4 * math.pi * 1e-7 * n2 * 2.0
S2 = math.pi * 0.020 ** 2; PHI2 = N2 * B2 * S2
# D3 — hai dây song song r = 10 cm, I1 = 4,0 A, I2 = 5,0 A, đoạn ℓ = 50 cm
B13 = 2e-7 * 4.0 / 0.10 * 1e6; F3 = 2e-7 * 4.0 * 5.0 * 0.50 / 0.10 * 1e6
# D4 — prôtôn, U = 500 V, B = 0,10 T
q, m, U, B4 = 1.6e-19, 1.67e-27, 500, 0.10
v4 = math.sqrt(2 * q * U / m); R4 = m * v4 / (q * B4); T4 = 2 * math.pi * m / (q * B4)
v4b = math.sqrt(2 * q * 4 * U / m); R4b = m * v4b / (q * B4)
# D5 — thanh trượt ℓ = 20 cm, R = 0,50 Ω, B = 0,50 T, v = 4,0 m/s
e5 = 0.50 * 4.0 * 0.20; I5 = e5 / 0.50; F5 = 0.50 * I5 * 0.20; Pk5 = F5 * 4.0; PR5 = I5 ** 2 * 0.50
ANS = dict(BM=r2(BM), BN=r2(BN), n2=n2, N2=N2, B2=r2(B2 * 1e3), S2=r2(S2 * 1e4), PHI2=r2(PHI2 * 1e3),
           B13=r2(B13), F3=r2(F3), v4=r2(v4 / 1e5), R4=r2(R4 * 100), d4=r2(2 * R4 * 100), t4=r2(T4 / 2 * 1e7),
           ti_le_d=r2(R4b / R4), e5=r2(e5), I5=r2(I5), F5=r2(F5), Pk5=r2(Pk5), PR5=r2(PR5))
print("Tự giải lại:", ANS)
assert ANS == dict(BM=25.0, BN=8.33, n2=1250.0, N2=500.0, B2=3.14, S2=12.57, PHI2=1.97, B13=8.0, F3=20.0, v4=3.1,
                   R4=3.23, d4=6.46, t4=3.28, ti_le_d=2.0, e5=0.4, I5=0.8, F5=0.08, Pk5=0.32, PR5=0.32), ANS
# chiều (tích có hướng, trục x phải, y lên, z ra phía người nhìn)
def cross(a, b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
assert cross((0, 0, 1), (1, 0, 0)) == (0, 1, 0)          # D1: I ra (⊙), M bên phải ⇒ B_M hướng lên
assert cross((0, 1, 0), (1, 0, 0)) == (0, 0, -1)         # D3: I1 hướng lên, dây 2 bên phải ⇒ B1 hướng vào ⊗
assert cross((0, 1, 0), (0, 0, -1)) == (-1, 0, 0)        # D3: F lên I2 hướng về dây 1 ⇒ hút
assert cross((0, 1, 0), (0, 0, -1)) == (-1, 0, 0)        # D4: q>0, v lên, B ⊗ ⇒ f sang trái
assert cross((1, 0, 0), (0, 0, -1)) == (0, 1, 0)         # D5: v sang phải, B ⊗ ⇒ lực lên hạt (+) hướng lên: N → M
assert cross((0, 1, 0), (0, 0, -1)) == (-1, 0, 0)        # D5: I N→M, B ⊗ ⇒ F sang trái, ngược v

# ═════════════ HÌNH (cong_cu tu_truong) — toạ độ 0..20 × 0..11, y lên ═════════════
def ghi(t):
    assert len(t) <= 36, (len(t), t)
    return {"loai": "ghi", "text": t}

def chu(x, y, t, a="middle", mau=None, het=None):
    it = {"loai": "chu", "x": x, "y": y, "text": t, "a": a}
    if mau: it["mau"] = mau
    if het: it["het"] = het
    return it


def cc_d1():
    O = (4, 5.5)
    return {"loai": "tu_truong", "de": True,
            "hinh": [
                {"loai": "vong", "x": 4, "y": 5.5, "r": 2, "mau": "b", "dut": True, "het": 1},
                {"loai": "vong", "x": 4, "y": 5.5, "r": 4, "mau": "b", "dut": True, "het": 1},
                {"loai": "day", "tu": [4, 5.5], "den": [17.5, 5.5], "mau": "chu", "dut": True},
                {"loai": "tiet_dien", "x": 4, "y": 5.5, "chieu": "ra"},
                chu(3.0, 4.2, "O", "end"),
                {"loai": "diem", "x": 8, "y": 5.5, "ten": "M", "vi": "duoi"},
                {"loai": "diem", "x": 16, "y": 5.5, "ten": "N", "vi": "duoi"},
                chu(0.3, 9.9, "I = 5,0 A", "start", "i"),
                chu(19.6, 10.0, "OM = 4,0 cm", "end"),
                chu(19.6, 8.3, "ON = 12 cm", "end")],
            "lop": [
                [{"loai": "vong", "x": 4, "y": 5.5, "r": 2, "mau": "b", "dut": True, "chieu": "nguoc"},
                 {"loai": "vong", "x": 4, "y": 5.5, "r": 4, "mau": "b", "dut": True, "chieu": "nguoc"},
                 ghi("I ra ⊙ ⇒ ngược chiều kim đồng hồ")],
                [{"loai": "vec", "x": 8, "y": 5.5, "goc": 90, "dai": 2.5, "mau": "b", "nhan": "B_M"},
                 ghi("B_M tiếp tuyến đường sức: hướng lên")],
                [ghi("B_M = 2·10⁻⁷·5,0 : 0,040 = 25 μT")],
                [{"loai": "vec", "x": 16, "y": 5.5, "goc": 90, "dai": 0.83, "mau": "b", "nhan": "B_N"},
                 ghi("r gấp 3 ⇒ B_N = 25 : 3 ≈ 8,33 μT")],
                [ghi("Xa dây gấp 3 thì B nhỏ đi 3 lần ✓")],
            ]}


def cc_d2():
    vong = [{"loai": "elip", "x": 4 + k, "y": 5.5, "rx": 0.3, "ry": 2.0, "mau": "i"} for k in range(13)]
    return {"loai": "tu_truong", "de": True,
            "hinh": vong + [
                {"loai": "duong", "diem": [[2.5, 5.5], [17.5, 5.5]], "mau": "b", "dut": True},
                {"loai": "duong", "diem": [[2.5, 4.6], [17.5, 4.6]], "mau": "b", "dut": True},
                {"loai": "duong", "diem": [[2.5, 6.4], [17.5, 6.4]], "mau": "b", "dut": True},
                {"loai": "day", "tu": [4, 2.6], "den": [16, 2.6], "mau": "chu", "dut": True},
                chu(10, 1.0, "ℓ = 40 cm"),
                chu(0.3, 9.9, "D = 4,0 cm", "start"),
                chu(19.7, 9.9, "I = 2,0 A", "end", "i"),
                chu(19.7, 8.2, "d = 0,80 mm", "end")],
            "lop": [
                [ghi("Quấn sát: N/ℓ = 1/d = 1250 vòng/m")],
                [ghi("N = ℓ/d = 0,40 : 0,00080 = 500")],
                [ghi("B đều trong ống: B ≈ 3,14 mT")],
                [ghi("S = π(D/2)² = π·2,0² ≈ 12,57 cm²")],
                [ghi("Φ = NBS ≈ 1,97 mWb")],
                [ghi("Φ một vòng ≈ 3,9 μWb; ×500 ✓")],
            ]}


def cc_d3():
    return {"loai": "tu_truong", "de": True,
            "hinh": [
                {"loai": "day", "tu": [7, 0.6], "den": [7, 10.4], "mau": "chu"},
                {"loai": "day", "tu": [13, 0.6], "den": [13, 10.4], "mau": "chu"},
                {"loai": "dong", "tu": [6.2, 7.2], "den": [6.2, 9.4], "nhan": "I_1"},
                {"loai": "dong", "tu": [13.8, 7.2], "den": [13.8, 9.4], "nhan": "I_2", "het": 5},
                chu(7, 0.0, "(1)"), chu(13, 0.0, "(2)"),
                {"loai": "day", "tu": [7, 2.0], "den": [13, 2.0], "mau": "chu", "dut": True},
                chu(10, 2.4, "r = 10 cm"),
                chu(0.3, 10.0, "I₁ = 4,0 A", "start", "i"),
                chu(19.7, 10.0, "I₂ = 5,0 A", "end", "i"),
                chu(19.7, 1.0, "ℓ = 50 cm", "end")],
            "lop": [
                [{"loai": "tiet_dien", "x": 16.5, "y": 3.2, "chieu": "vao", "ten": "B_1", "het": 5},
                 ghi("Nắm tay phải: B_1 tại (2) vào ⊗")],
                [ghi("B_1 = 2·10⁻⁷·4,0 : 0,10 = 8,0 μT")],
                [{"loai": "vec", "x": 13, "y": 5.0, "goc": 180, "dai": 2.2, "mau": "luc", "nhan": "F", "het": 5},
                 {"loai": "vec", "x": 7, "y": 5.0, "goc": 0, "dai": 2.2, "mau": "luc", "dut": True, "het": 5},
                 ghi("Bàn tay trái: F về phía (1) ⇒ hút")],
                [ghi("F = B_1·I_2·ℓ = 20 μN")],
                [{"loai": "dong", "tu": [13.8, 9.4], "den": [13.8, 7.2], "nhan": "I_2"},
                 {"loai": "vec", "x": 13, "y": 5.0, "goc": 0, "dai": 2.2, "mau": "luc", "nhan": "F"},
                 {"loai": "vec", "x": 7, "y": 5.0, "goc": 180, "dai": 2.2, "mau": "luc", "dut": True},
                 ghi("Ngược chiều ⇒ đẩy, F như cũ")],
                [ghi("Cùng chiều hút, ngược chiều đẩy ✓")],
            ]}


def cc_d4():
    Sx, Sy, Rf = 14, 2.6, 4.0
    cung = [[round(Sx - Rf + Rf * math.cos(math.radians(a)), 3), round(Sy + Rf * math.sin(math.radians(a)), 3)]
            for a in range(0, 181, 10)]
    return {"loai": "tu_truong", "de": True, "nen": {"kieu": "vao", "nhan": "B = 0,10 T"},
            "hinh": [
                {"loai": "day", "tu": [1.5, Sy], "den": [13.4, Sy], "mau": "chu"},
                {"loai": "day", "tu": [14.6, Sy], "den": [19.5, Sy], "mau": "chu"},
                chu(19.6, 1.4, "phim", "end"),
                chu(14.8, 1.4, "S", "start"),
                {"loai": "vec", "x": Sx, "y": Sy, "goc": 90, "dai": 2.0, "mau": "chu", "nhan": "v"},
                chu(19.6, 10.0, "prôtôn, U = 500 V", "end")],
            "lop": [
                [ghi("|q|U = ½mv² ⇒ v ≈ 3,10·10⁵ m/s")],
                [{"loai": "vec", "x": Sx, "y": Sy + 1.0, "goc": 180, "dai": 1.6, "mau": "luc", "nhan": "f"},
                 {"loai": "duong", "diem": cung, "mau": "i", "mui": 2},
                 {"loai": "diem", "x": Sx - 2 * Rf, "y": Sy, "ten": "A", "vi": "duoi"},
                 ghi("f hướng trái ⇒ đập bên trái S")],
                [ghi("|q|vB = mv²/R ⇒ R ≈ 3,23 cm")],
                [{"loai": "day", "tu": [Sx - 2 * Rf, Sy - 0.9], "den": [Sx, Sy - 0.9], "mau": "chu", "dut": True},
                 ghi("Nửa vòng: SA = 2R ≈ 6,46 cm")],
                [ghi("t = T/2 = πm/(|q|B) ≈ 3,28·10⁻⁷ s")],
                [ghi("U ×4 ⇒ v, R, SA ×2; t không đổi")],
                [ghi("R cỡ vài cm: vừa khối phổ kế ✓")],
            ]}


def cc_d5():
    return {"loai": "tu_truong", "de": True, "nen": {"kieu": "vao", "nhan": "B = 0,50 T"},
            "hinh": [
                {"loai": "day", "tu": [3, 8.5], "den": [18.5, 8.5], "mau": "chu"},
                {"loai": "day", "tu": [3, 2.5], "den": [18.5, 2.5], "mau": "chu"},
                {"loai": "day", "tu": [3, 2.5], "den": [3, 4.4], "mau": "chu"},
                {"loai": "day", "tu": [3, 6.6], "den": [3, 8.5], "mau": "chu"},
                {"loai": "duong", "diem": [[2.6, 4.4], [3.4, 4.4], [3.4, 6.6], [2.6, 6.6]], "kin": True, "mau": "chu"},
                {"loai": "day", "tu": [12, 1.9], "den": [12, 9.1], "mau": "chu"},
                chu(12, 9.5, "M"), chu(12, 1.0, "N"),
                {"loai": "vec", "x": 12, "y": 7.2, "goc": 0, "dai": 2.4, "mau": "chu", "nhan": "v"},
                chu(13.0, 1.0, "ℓ = 20 cm", "start"),
                chu(19.6, 9.3, "v = 4,0 m/s", "end"),
                chu(3.8, 6.0, "R = 0,50 Ω", "start")],
            "lop": [
                [ghi("e = Bvℓ = 0,50·4,0·0,20 = 0,40 V")],
                [ghi("I = e : R = 0,40 : 0,50 = 0,80 A")],
                [{"loai": "dong", "tu": [11.3, 5.0], "den": [11.3, 7.0], "nhan": "I"},
                 ghi("Φ tăng ⇒ trong thanh I từ N đến M")],
                [{"loai": "vec", "x": 12, "y": 4.0, "goc": 180, "dai": 2.4, "mau": "luc", "nhan": "F"},
                 ghi("F ngược chiều v: cản chuyển động")],
                [{"loai": "vec", "x": 12, "y": 4.0, "goc": 0, "dai": 2.4, "mau": "chu", "dut": True, "nhan": "F_k"},
                 ghi("Đều ⇒ F_k = BIℓ = 0,080 N")],
                [ghi("P_k = F_k·v = 0,080·4,0 = 0,32 W")],
                [ghi("P_R = I²R = 0,80²·0,50 = 0,32 W")],
                [ghi("P_k = P_R: công kéo → nhiệt ✓")],
            ]}


CONG_CU = [cc_d1, cc_d2, cc_d3, cc_d4, cc_d5]

# ═════════════ DẠNG (đề) ═════════════
DANG = [
    dict(label="Dạng 1 · Dễ · Từ trường của dòng điện thẳng dài: chiều và độ lớn tại một điểm", topic=T_DONG,
         problem_html=r"""<p>Một dây dẫn thẳng rất dài đặt thẳng đứng trong không khí, có dòng điện $I=5{,}0\ \text{A}$ chạy từ dưới lên. Hình vẽ nhìn từ trên xuống: dây đi qua O, vuông góc với mặt phẳng hình, dòng điện hướng ra phía người nhìn (⊙). Điểm M nằm bên phải dây, cách dây $4{,}0\ \text{cm}$; điểm N nằm trên tia OM, cách dây $12\ \text{cm}$. Biết cảm ứng từ do dòng điện thẳng rất dài gây ra tại điểm cách dây một khoảng $r$ là $B=2\cdot10^{-7}\dfrac{I}{r}$ ($B$ tính bằng T, $I$ bằng A, $r$ bằng m).</p><ol type="a"><li>Đường sức từ của dòng điện trong mặt phẳng hình có dạng gì, chiều thế nào?</li><li>Vectơ cảm ứng từ tại M có phương, chiều thế nào?</li><li>Tính độ lớn cảm ứng từ tại M và tại N theo đơn vị μT (làm tròn đến hai chữ số sau dấu phẩy).</li></ol>"""),
    dict(label="Dạng 2 · Trung bình · Ống dây quấn sát một lớp: cảm ứng từ trong lòng ống và từ thông qua ống", topic=T_THONG,
         problem_html=r"""<p>Một ống dây dài $\ell=40\ \text{cm}$, đường kính ống $D=4{,}0\ \text{cm}$, được quấn bằng dây đồng có đường kính $d=0{,}80\ \text{mm}$ (lớp sơn cách điện rất mỏng), các vòng quấn sát nhau thành một lớp. Cho dòng điện $I=2{,}0\ \text{A}$ chạy qua ống dây đặt trong không khí. Biết cảm ứng từ trong lòng ống dây dài là $B=4\pi\cdot10^{-7}\dfrac{N}{\ell}I$, với $N$ là tổng số vòng dây.</p><ol type="a"><li>Tính số vòng dây trên mỗi mét chiều dài ống và tổng số vòng dây.</li><li>Tính cảm ứng từ trong lòng ống dây theo đơn vị mT (làm tròn đến hai chữ số sau dấu phẩy).</li><li>Tính từ thông qua ống dây $\Phi=NBS$ theo đơn vị mWb (làm tròn đến hai chữ số sau dấu phẩy).</li></ol>"""),
    dict(label="Dạng 3 · Trung bình · Hai dòng điện thẳng song song: hút hay đẩy, lực tương tác", topic=T_LUC,
         problem_html=r"""<p>Hai dây dẫn thẳng rất dài đặt song song trong không khí, cách nhau $r=10\ \text{cm}$. Dây (1) bên trái mang dòng điện $I_1=4{,}0\ \text{A}$, dây (2) bên phải mang dòng điện $I_2=5{,}0\ \text{A}$; hai dòng điện cùng chiều, hướng lên trong mặt phẳng hình vẽ. Biết $B=2\cdot10^{-7}\dfrac{I}{r}$ và lực từ giữa hai dòng điện song song tác dụng lên đoạn dây dài $\ell$ là $F=2\cdot10^{-7}\dfrac{I_1I_2\ell}{r}$.</p><ol type="a"><li>Từ trường do dây (1) gây ra tại chỗ đặt dây (2) có chiều thế nào, độ lớn bao nhiêu μT?</li><li>Hai dây hút hay đẩy nhau? Tính lực từ tác dụng lên mỗi đoạn dài $50\ \text{cm}$ của dây (2) theo đơn vị μN.</li><li>Đổi chiều dòng điện trong dây (2), giữ nguyên cường độ. Lực tương tác giữa hai dây thay đổi thế nào?</li></ol>"""),
    dict(label="Dạng 4 · Khó · Hạt mang điện bay vào từ trường đều (khối phổ kế): bán kính, điểm đập, thời gian bay", topic=T_HAT,
         problem_html=r"""<p>Một prôtôn ($q=+1{,}6\cdot10^{-19}\ \text{C}$, $m=1{,}67\cdot10^{-27}\ \text{kg}$) ban đầu đứng yên, được tăng tốc qua hiệu điện thế $U=500\ \text{V}$ rồi đi qua khe S vào vùng từ trường đều $B=0{,}10\ \text{T}$ theo hướng vuông góc với đường sức. Trong hình vẽ, đường sức từ hướng vào mặt phẳng hình (⊗), prôtôn đi qua khe S theo hướng lên trên; tấm phim ảnh nằm ngang, đi qua S. Bỏ qua trọng lực. Biết khi $\vec v\perp\vec B$, lực từ tác dụng lên hạt có độ lớn $f=|q|vB$.</p><ol type="a"><li>Tính tốc độ của prôtôn khi qua khe S theo đơn vị $10^5\ \text{m/s}$ (làm tròn đến hai chữ số sau dấu phẩy).</li><li>Prôtôn đập vào phim ở bên trái hay bên phải khe S, cách S bao nhiêu cm (làm tròn đến hai chữ số sau dấu phẩy)?</li><li>Tính thời gian prôtôn bay trong từ trường từ S đến phim theo đơn vị $10^{-7}\ \text{s}$ (làm tròn đến hai chữ số sau dấu phẩy).</li><li>Tăng hiệu điện thế tăng tốc lên 4 lần. Khoảng cách từ S đến điểm đập và thời gian bay thay đổi thế nào?</li></ol>"""),
    dict(label="Dạng 5 · Khó · Thanh dẫn trượt trên hai ray trong từ trường: dòng cảm ứng, lực cản, công suất", topic=T_THANH,
         problem_html=r"""<p>Hai thanh ray kim loại song song nằm ngang, cách nhau $\ell=20\ \text{cm}$, một đầu nối với điện trở $R=0{,}50\ \Omega$. Thanh kim loại MN đặt vuông góc với hai ray, trượt sang phải (ra xa điện trở) với tốc độ không đổi $v=4{,}0\ \text{m/s}$. Trong hình nhìn từ trên xuống, M ở ray trên, N ở ray dưới. Hệ đặt trong từ trường đều $B=0{,}50\ \text{T}$ có đường sức thẳng đứng, hướng vào mặt phẳng hình (⊗). Bỏ qua điện trở của thanh, của ray và ma sát. Biết suất điện động cảm ứng trong thanh là $e=Bv\ell$ và lực từ tác dụng lên thanh có độ lớn $F=BI\ell$.</p><ol type="a"><li>Tính suất điện động cảm ứng và cường độ dòng điện qua $R$.</li><li>Dòng điện trong thanh chạy theo chiều nào?</li><li>Lực từ tác dụng lên thanh có chiều nào? Để thanh chuyển động đều cần lực kéo bao nhiêu niutơn?</li><li>Tính công suất của lực kéo và công suất toả nhiệt trên $R$; nhận xét.</li></ol>"""),
]

# ═════════════ BẢNG PHÂN TÍCH ĐỀ (cột 3 không ghi số đáp án) ═════════════
ANALYSIS = [
    [(r'"dây dẫn thẳng rất dài … dòng điện $I=5{,}0\ \text{A}$"', r"$I=5{,}0\ \text{A}$", "Từ trường của dòng điện thẳng: đường sức là các vòng tròn đồng tâm, tâm trên dây"),
     (r'"dòng điện hướng ra phía người nhìn (⊙)"', "Chiều $I$ ra khỏi mặt phẳng hình", "Quy tắc nắm tay phải: ngón cái theo chiều $I$, bốn ngón khum cho chiều đường sức"),
     (r'"M … cách dây $4{,}0\ \text{cm}$"', r"$r_M=4{,}0\ \text{cm}$", r"⚠ $B=2\cdot10^{-7}\dfrac{I}{r}$ chỉ đúng với dây thẳng rất dài, $r$ đổi ra mét"),
     (r'"Vectơ cảm ứng từ tại M có phương, chiều"', r"Cần chiều $\vec B_M$", "$\\vec B$ tiếp tuyến với đường sức tại điểm đó, cùng chiều đường sức"),
     (r'"N … cách dây $12\ \text{cm}$"', r"$r_N=12\ \text{cm}$", "$B$ phụ thuộc $r$ thế nào?"),
     (r'"độ lớn cảm ứng từ tại M và tại N"', r"Cần $B_M$, $B_N$ (μT)", r"$B=2\cdot10^{-7}\dfrac{I}{r}$ ; $1\ \mu\text{T}=10^{-6}\ \text{T}$")],
    [(r'"ống dây dài $\ell=40\ \text{cm}$, đường kính ống $D=4{,}0\ \text{cm}$"', r"$\ell=40\ \text{cm}$ ; $D=4{,}0\ \text{cm}$", "Đổi ra mét; $D$ dùng cho tiết diện ống"),
     (r'"dây đồng … đường kính $d=0{,}80\ \text{mm}$ … quấn sát nhau thành một lớp"', r"$d=0{,}80\ \text{mm}$", r"⚠ Quấn sát một lớp: mỗi vòng chiếm đúng một bề rộng $d$ trên chiều dài ống ⇒ $\dfrac{N}{\ell}=\dfrac{1}{d}$"),
     (r'"dòng điện $I=2{,}0\ \text{A}$"', r"$I=2{,}0\ \text{A}$", r"$B=4\pi\cdot10^{-7}\dfrac{N}{\ell}I$ (từ trường đều trong lòng ống dài)"),
     (r'"số vòng dây trên mỗi mét … tổng số vòng dây"', r"Cần $\dfrac{N}{\ell}$ ; $N$", r"$N=\dfrac{N}{\ell}\cdot\ell$"),
     (r'"cảm ứng từ trong lòng ống dây"', r"Cần $B$ (mT)", r"$B=4\pi\cdot10^{-7}\dfrac{N}{\ell}I$"),
     (r'"từ thông qua ống dây $\Phi=NBS$"', r"Cần $\Phi$ (mWb)", r"$S=\pi\left(\dfrac{D}{2}\right)^2$ đổi ra m² ; mặt vòng dây vuông góc $\vec B$")],
    [(r'"Hai dây dẫn thẳng rất dài đặt song song … cách nhau $r=10\ \text{cm}$"', r"$r=10\ \text{cm}$", r"⚠ Công thức $B$ và $F$ chỉ đúng với dây thẳng rất dài, song song; $r$ đổi ra mét"),
     (r'"$I_1=4{,}0\ \text{A}$ … $I_2=5{,}0\ \text{A}$ … cùng chiều, hướng lên"', r"$I_1$, $I_2$ cùng chiều", "Dây (1) tạo từ trường tại chỗ đặt dây (2); dây (2) mang dòng nằm trong từ trường đó"),
     (r'"Từ trường do dây (1) gây ra tại chỗ đặt dây (2)"', r"Cần chiều và độ lớn $B_1$", r"Nắm tay phải ; $B_1=2\cdot10^{-7}\dfrac{I_1}{r}$"),
     (r'"Hai dây hút hay đẩy nhau?"', "Cần chiều lực lên dây (2)", "Quy tắc bàn tay trái với $I_2$ và $\\vec B_1$"),
     (r'"mỗi đoạn dài $50\ \text{cm}$ của dây (2)"', r"$\ell=50\ \text{cm}$", r"$F=2\cdot10^{-7}\dfrac{I_1I_2\ell}{r}=B_1I_2\ell$"),
     (r'"Đổi chiều dòng điện trong dây (2)"', r"$I_2$ ngược chiều $I_1$", "Đổi chiều $I_2$ thì chiều lực lên dây (2) đổi thế nào? Độ lớn phụ thuộc chiều không?")],
    [(r'"prôtôn ($q=+1{,}6\cdot10^{-19}\ \text{C}$, $m=1{,}67\cdot10^{-27}\ \text{kg}$) ban đầu đứng yên"', "Hạt mang điện dương, $v_0=0$", "Điện tích dương: dùng bàn tay trái trực tiếp (electron thì lấy chiều ngược lại)"),
     (r'"được tăng tốc qua hiệu điện thế $U=500\ \text{V}$"', r"$U=500\ \text{V}$", r"Định lí động năng: $|q|U=\tfrac12mv^2$"),
     (r'"vào vùng từ trường đều $B=0{,}10\ \text{T}$ theo hướng vuông góc với đường sức"', r"$B=0{,}10\ \text{T}$ ; $\vec v\perp\vec B$", r"⚠ $\vec v\perp\vec B$ và bỏ qua trọng lực thì lực từ $f=|q|vB$ luôn vuông góc $\vec v$ ⇒ chuyển động tròn đều"),
     (r'"đường sức … (⊗), prôtôn đi qua khe S theo hướng lên trên"', "Chiều $\\vec B$, chiều $\\vec v$ tại S", "Quy tắc bàn tay trái cho chiều lực tại S ⇒ phía lệch"),
     (r'"đập vào phim … cách S bao nhiêu cm"', "Cần phía và khoảng cách SA", r"Lực từ đóng vai trò lực hướng tâm: $|q|vB=\dfrac{mv^2}{R}$ ; hạt đi nửa vòng"),
     (r'"thời gian prôtôn bay … từ S đến phim"', "Cần $t$", r"Chu kì chuyển động tròn $T=\dfrac{2\pi R}{v}$"),
     (r'"Tăng hiệu điện thế … lên 4 lần"', r"$U'=4U$", "$v$, $R$, $T$ phụ thuộc $U$ thế nào?")],
    [(r'"Hai thanh ray … cách nhau $\ell=20\ \text{cm}$ … nối với điện trở $R=0{,}50\ \Omega$"', r"$\ell=20\ \text{cm}$ ; $R=0{,}50\ \Omega$", "Thanh, hai ray và $R$ tạo thành mạch kín"),
     (r'"trượt sang phải (ra xa điện trở) với tốc độ không đổi $v=4{,}0\ \text{m/s}$"', r"$v=4{,}0\ \text{m/s}$ ; diện tích mạch tăng", "Từ thông qua mạch thay đổi ⇒ có dòng cảm ứng"),
     (r'"từ trường đều $B=0{,}50\ \text{T}$ … hướng vào mặt phẳng hình (⊗)"', r"$B=0{,}50\ \text{T}$ ; $\vec B\perp$ mặt phẳng ray", r"⚠ $e=Bv\ell$ dùng khi $\vec v$, $\vec B$, thanh vuông góc từng đôi; bỏ qua điện trở thanh, ray"),
     (r'"Dòng điện trong thanh chạy theo chiều nào?"', "Cần chiều $I$ trong MN", "Định luật Lenz: dòng cảm ứng sinh từ trường chống lại sự tăng từ thông"),
     (r'"Lực từ … chiều nào? … cần lực kéo bao nhiêu"', "Cần chiều $F$ ; $F_k$", "Quy tắc bàn tay trái ; thanh chuyển động đều ⇒ hợp lực bằng 0"),
     (r'"công suất của lực kéo và công suất toả nhiệt trên $R$"', "Cần $P_k$, $P_R$", r"$P_k=F_kv$ ; $P_R=I^2R$ ; bảo toàn năng lượng")],
]

# ═════════════ LỜI GIẢI + buoc[] (số bước khớp 1-1) ═════════════
SOLS, STEPS = [], []

# ───── D1 ─────
SOLS.append(sol(
    [r"<strong>Khái niệm:</strong> đường sức từ của dòng điện thẳng là các vòng tròn đồng tâm nằm trong mặt phẳng vuông góc với dây, tâm trên dây.",
     r"<strong>Quy tắc:</strong> nắm tay phải, ngón cái theo chiều dòng điện, bốn ngón khum lại chỉ chiều đường sức.",
     r"<strong>Công thức:</strong> $B=2\cdot10^{-7}\dfrac{I}{r}$ ; $\vec B$ tiếp tuyến với đường sức.",
     r"⚠ <strong>Điều kiện:</strong> dây thẳng rất dài; $r$ tính bằng mét."],
    [("Chiều đường sức", [P("Ngón cái hướng ra phía người nhìn (⊙), bốn ngón khum lại:"),
                          A("T:Các vòng tròn đồng tâm O, chiều ngược chiều kim đồng hồ.")]),
     ("Chiều vectơ B tại M", [P("M nằm bên phải O; tiếp tuyến của vòng tròn ngược chiều kim đồng hồ tại điểm bên phải hướng lên:"),
                              A(r"T:$\vec B_M$ vuông góc với OM, hướng lên trong mặt phẳng hình.")]),
     ("Độ lớn B tại M", [M(r"B_M=2\cdot10^{-7}\dfrac{I}{r_M}=2\cdot10^{-7}\cdot\dfrac{5{,}0}{0{,}040}"),
                         M(r"B_M=2{,}5\cdot10^{-5}\ \text{T}"), A(r"B_M=25{,}00\ \mu\text{T}")]),
     ("Độ lớn B tại N", [P("$B$ tỉ lệ nghịch với $r$; $r_N=3r_M$ :"),
                         M(r"B_N=2\cdot10^{-7}\cdot\dfrac{5{,}0}{0{,}12}=\dfrac{B_M}{3}"), A(r"B_N\approx8{,}33\ \mu\text{T}")]),
     ("Kiểm tra", [P("Cỡ chục μT, bằng cỡ từ trường Trái Đất — hợp lí với dòng điện vài ampe ở cách vài xentimét."),
                   P(r"$B_M\cdot r_M=B_N\cdot r_N=10^{-6}\ \text{T}\cdot\text{m}$ ✓")])],
    ["a) Vòng tròn đồng tâm O, ngược chiều kim đồng hồ.", r"b) $\vec B_M\perp OM$, hướng lên.",
     r"c) $B_M=25{,}00\ \mu\text{T}$ ; $B_N\approx8{,}33\ \mu\text{T}$."],
    r"Nhận dạng: thấy <b>dây thẳng dài, điểm cách dây r</b> → nắm tay phải cho chiều, $B=2\cdot10^{-7}I/r$ cho độ lớn."))
STEPS.append(dict(
    nhan_dang=r"Thấy <b>dây dẫn thẳng dài, điểm cách dây r</b> → nghĩ tới <b>nắm tay phải</b> và <b>B = 2·10⁻⁷·I/r</b>",
    cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 1},
    tom_de={"cho": [r"$I=5{,}0\ \text{A}$ hướng ra (⊙)", r"$OM=4{,}0\ \text{cm}$ ; $ON=12\ \text{cm}$"],
            "tim": ["a) dạng, chiều đường sức", r"b) chiều $\vec B_M$", r"c) $B_M$, $B_N$ (μT)"]},
    buoc=[
        buoc("Chiều đường sức", "Trong hình nhìn từ trên xuống, đường sức từ quanh dây có dạng và chiều thế nào?",
             loi="Đặt ngón cái theo chiều dòng điện nhưng đọc chiều quay như khi nhìn từ phía dưới, nên ra ngược lại.",
             lua_chon=[("Vòng tròn đồng tâm O, ngược chiều kim đồng hồ", True),
                       ("Vòng tròn đồng tâm O, cùng chiều kim đồng hồ", "Ngón cái hướng ra phía người nhìn thì bốn ngón khum lại theo chiều ngược kim đồng hồ."),
                       ("Đường thẳng song song với dây", "Đường sức của dòng điện thẳng là vòng tròn trong mặt phẳng vuông góc với dây, tâm trên dây.")]),
        buoc("Chiều vectơ B tại M", "Vectơ cảm ứng từ tại M hướng về đâu trong mặt phẳng hình?",
             loi="Vẽ $\\vec B$ dọc theo bán kính OM, quên rằng $\\vec B$ tiếp tuyến với đường sức.",
             lua_chon=[("Hướng lên, vuông góc với OM", True),
                       ("Hướng sang phải, ra xa dây", "$\\vec B$ tiếp tuyến với đường sức tròn nên vuông góc với bán kính OM, không nằm dọc OM."),
                       ("Hướng xuống, vuông góc với OM", "Đó là chiều khi dòng điện đi vào mặt phẳng hình; ở đây đường sức ngược chiều kim đồng hồ.")],
             ke=[("Vẽ đường sức qua M rồi lấy tiếp tuyến theo chiều đường sức", True),
                 ("Lấy $\\vec B$ cùng phương với OM", "$\\vec B$ tiếp tuyến với đường sức, vuông góc với bán kính."),
                 ("Lấy $\\vec B$ cùng chiều dòng điện", "$\\vec B$ nằm trong mặt phẳng vuông góc với dây, không song song dây.")]),
        buoc("Độ lớn B tại M", "Cảm ứng từ tại M bằng bao nhiêu μT?", dap_so=25, don_vi="μT", sai_so=0.3,
             loi=r"Giữ $r$ bằng xentimét khi thế số (B lệch 100 lần) hoặc dùng nhầm $2\pi\cdot10^{-7}$ của vòng dây tròn.",
             ke=[(r"Thế $I$ và $r_M$ (đổi ra mét) vào $B=2\cdot10^{-7}\dfrac{I}{r}$", True),
                 (r"Thế $r_M$ giữ đơn vị cm", "Công thức dùng $r$ bằng mét; giữ cm làm kết quả lệch 100 lần."),
                 (r"Dùng $B=2\pi\cdot10^{-7}\dfrac{I}{r}$", "Đó là công thức tại tâm vòng dây tròn, không phải dòng điện thẳng.")]),
        buoc("Độ lớn B tại N", "Cảm ứng từ tại N bằng bao nhiêu μT?", dap_so=8.33, don_vi="μT", sai_so=0.05,
             loi=r"Coi $B$ tỉ lệ nghịch với $r^2$ nên chia $B_M$ cho 9.",
             ke=[(r"$B$ tỉ lệ nghịch với $r$: so $r_N$ với $r_M$", True),
                 (r"$B$ tỉ lệ nghịch với $r^2$", "Đó là kiểu giảm của điện trường điện tích điểm; dòng điện thẳng cho $B\\sim 1/r$."),
                 (r"$B_N=B_M$ vì cùng một dòng điện", "$B$ phụ thuộc khoảng cách tới dây, càng xa càng yếu.")]),
        buoc("Kiểm tra"),
    ]))

# ───── D2 ─────
SOLS.append(sol(
    [r"<strong>Khái niệm:</strong> trong lòng ống dây dài, từ trường đều, đường sức song song trục ống.",
     r"<strong>Công thức:</strong> $B=4\pi\cdot10^{-7}\dfrac{N}{\ell}I$ ; từ thông qua ống $\Phi=NBS$.",
     r"<strong>Quấn sát một lớp:</strong> mỗi vòng chiếm bề rộng $d$ nên $\dfrac{N}{\ell}=\dfrac{1}{d}$.",
     r"⚠ <strong>Điều kiện:</strong> ống dài so với đường kính; mọi đại lượng đổi ra SI ($d$, $\ell$ ra m; $S$ ra m²)."],
    [("Số vòng trên mỗi mét", [M(r"\dfrac{N}{\ell}=\dfrac{1}{d}=\dfrac{1}{0{,}80\cdot10^{-3}}"), A(r"\dfrac{N}{\ell}=1250\ \text{vòng/m}")]),
     ("Tổng số vòng dây", [M(r"N=\dfrac{N}{\ell}\cdot\ell=1250\cdot0{,}40"), A(r"N=500\ \text{vòng}")]),
     ("Cảm ứng từ trong lòng ống", [M(r"B=4\pi\cdot10^{-7}\cdot1250\cdot2{,}0"), M(r"B=\pi\cdot10^{-3}\ \text{T}"), A(r"B\approx3{,}14\ \text{mT}")]),
     ("Tiết diện ống", [M(r"S=\pi\left(\dfrac{D}{2}\right)^2=\pi\cdot2{,}0^2\ \text{cm}^2"), A(r"S\approx12{,}57\ \text{cm}^2=1{,}257\cdot10^{-3}\ \text{m}^2")]),
     ("Từ thông qua ống dây", [M(r"\Phi=NBS=500\cdot3{,}14\cdot10^{-3}\cdot1{,}257\cdot10^{-3}"), M(r"\Phi\approx1{,}97\cdot10^{-3}\ \text{Wb}"), A(r"\Phi\approx1{,}97\ \text{mWb}")]),
     ("Kiểm tra", [P(r"Từ thông qua một vòng $BS\approx3{,}9\cdot10^{-6}\ \text{Wb}$, nhân 500 vòng ra cỡ mWb ✓."),
                   P(r"Đơn vị: $\text{T}\cdot\text{m}^2=\text{Wb}$ ✓.")])],
    [r"a) $\dfrac{N}{\ell}=1250\ \text{vòng/m}$ ; $N=500$ vòng.", r"b) $B\approx3{,}14\ \text{mT}$.", r"c) $\Phi\approx1{,}97\ \text{mWb}$."],
    r"Nhận dạng: thấy <b>quấn sát một lớp, đường kính dây d</b> → $N/\ell=1/d$, rồi $B=4\pi\cdot10^{-7}(N/\ell)I$."))
STEPS.append(dict(
    nhan_dang=r"Thấy <b>ống dây quấn sát một lớp, đường kính dây d</b> → nghĩ tới <b>N/ℓ = 1/d</b> rồi <b>B = 4π·10⁻⁷(N/ℓ)I</b>",
    cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 0},
    tom_de={"cho": [r"$\ell=40\ \text{cm}$ ; $D=4{,}0\ \text{cm}$", r"dây $d=0{,}80\ \text{mm}$ quấn sát một lớp", r"$I=2{,}0\ \text{A}$"],
            "tim": [r"a) $N/\ell$ ; $N$", r"b) $B$ (mT)", r"c) $\Phi=NBS$ (mWb)"]},
    buoc=[
        buoc("Số vòng trên mỗi mét", "Số vòng dây trên mỗi mét chiều dài ống là bao nhiêu?", dap_so=1250, don_vi="vòng/m", sai_so=2,
             loi="Lấy $1/d$ khi $d$ còn tính bằng milimét, hoặc đổi $0{,}80\\ \\text{mm}$ sai thành $8\\cdot10^{-3}\\ \\text{m}$."),
        buoc("Tổng số vòng dây", "Tổng số vòng dây N bằng bao nhiêu?", dap_so=500, don_vi="vòng", sai_so=1,
             loi="Chia số vòng trên mét cho $\\ell$ thay vì nhân, hoặc giữ $\\ell$ bằng xentimét.",
             ke=[(r"$N=\dfrac{N}{\ell}\cdot\ell$ với $\ell$ đổi ra mét", True),
                 (r"$N=\dfrac{N}{\ell}:\ell$", "Số vòng trên mỗi mét nhân với số mét mới ra tổng số vòng."),
                 ("N bằng chu vi ống chia cho $d$", "Chu vi ống là chiều dài một vòng; số vòng phụ thuộc chiều dài ống $\\ell$.")]),
        buoc("Cảm ứng từ trong lòng ống", "Cảm ứng từ trong lòng ống dây bằng bao nhiêu mT?", dap_so=3.14, don_vi="mT", sai_so=0.02,
             loi="Dùng công thức dòng điện thẳng với $r$ là bán kính ống, hoặc quên đổi T sang mT.",
             ke=[(r"Thế $\dfrac{N}{\ell}$ và $I$ vào $B=4\pi\cdot10^{-7}\dfrac{N}{\ell}I$", True),
                 (r"Dùng $B=2\cdot10^{-7}\dfrac{I}{r}$ với $r$ là bán kính ống", "Đó là công thức dòng điện thẳng; trong lòng ống dây dài $B$ tính theo số vòng trên mét."),
                 (r"Thế $N$ (tổng số vòng) thay cho $\dfrac{N}{\ell}$", "Công thức cần số vòng trên mỗi mét; thế $N$ là bỏ mất phép chia cho $\\ell$.")]),
        buoc("Tiết diện ống", "Tiết diện của ống S bằng bao nhiêu cm²?", dap_so=12.57, don_vi="cm²", sai_so=0.1,
             loi="Dùng đường kính thay bán kính (ra gấp 4 lần) hoặc lấy tiết diện sợi dây đồng.",
             ke=[(r"$S=\pi\left(\dfrac{D}{2}\right)^2$", True),
                 (r"$S=\pi D^2$", "$D$ là đường kính; phải lấy bán kính $D/2$, dùng $D$ ra gấp 4 lần."),
                 (r"$S=\pi\left(\dfrac{d}{2}\right)^2$ với $d$ của dây đồng", "Từ thông đi qua lòng ống, tiết diện là của ống, không phải của sợi dây.")]),
        buoc("Từ thông qua ống dây", "Từ thông qua ống dây bằng bao nhiêu mWb?", dap_so=1.97, don_vi="mWb", sai_so=0.02,
             loi="Bỏ $N$ (ra từ thông qua một vòng) hoặc giữ $S$ theo cm² khi thế số.",
             ke=[(r"$\Phi=NBS$ với $B$ ra T, $S$ ra m²", True),
                 (r"$\Phi=BS$", "Đó là từ thông qua một vòng; đề hỏi từ thông qua cả ống N vòng."),
                 (r"$\Phi=NBS$ với $S$ giữ cm²", "Phải đổi $1\\ \\text{cm}^2=10^{-4}\\ \\text{m}^2$ thì $\\Phi$ mới ra Wb.")]),
        buoc("Kiểm tra"),
    ]))

# ───── D3 ─────
SOLS.append(sol(
    [r"<strong>Cách nghĩ:</strong> dây (1) tạo từ trường tại chỗ đặt dây (2); dây (2) mang dòng điện nằm trong từ trường đó nên chịu lực từ.",
     r"<strong>Quy tắc:</strong> nắm tay phải cho chiều $\vec B_1$ ; bàn tay trái cho chiều lực lên dây (2).",
     r"<strong>Công thức:</strong> $B_1=2\cdot10^{-7}\dfrac{I_1}{r}$ ; $F=B_1I_2\ell=2\cdot10^{-7}\dfrac{I_1I_2\ell}{r}$.",
     r"⚠ <strong>Điều kiện:</strong> hai dây thẳng rất dài, song song; $r$, $\ell$ đổi ra mét. Cùng chiều thì hút, ngược chiều thì đẩy."],
    [("Chiều từ trường của dây (1) tại dây (2)", [P("Ngón cái tay phải hướng lên theo $I_1$; bên phải dây (1), bốn ngón đi vào mặt phẳng hình:"),
                                                 A(r"T:$\vec B_1$ tại dây (2) hướng vào mặt phẳng hình (⊗).")]),
     ("Độ lớn từ trường tại dây (2)", [M(r"B_1=2\cdot10^{-7}\dfrac{I_1}{r}=2\cdot10^{-7}\cdot\dfrac{4{,}0}{0{,}10}"), A(r"B_1=8{,}0\cdot10^{-6}\ \text{T}=8{,}0\ \mu\text{T}")]),
     ("Hút hay đẩy", [P("Bàn tay trái: đường sức (⊗) đâm vào lòng bàn tay, chiều cổ tay → ngón tay theo $I_2$ (lên), ngón cái chỉ sang trái:"),
                      A("T:Lực lên dây (2) hướng về dây (1): hai dây hút nhau.")]),
     ("Lực từ lên đoạn 50 cm", [M(r"F=2\cdot10^{-7}\dfrac{I_1I_2\ell}{r}=2\cdot10^{-7}\cdot\dfrac{4{,}0\cdot5{,}0\cdot0{,}50}{0{,}10}"),
                                M(r"F=2{,}0\cdot10^{-5}\ \text{N}"), A(r"F=20\ \mu\text{N}")]),
     ("Đổi chiều dòng điện trong dây (2)", [P(r"$\vec B_1$ giữ nguyên, $I_2$ đổi chiều nên lực lên dây (2) đổi chiều; độ lớn chỉ phụ thuộc $I_1$, $I_2$, $\ell$, $r$:"),
                                            A("T:Hai dây đẩy nhau, độ lớn lực vẫn như cũ.")]),
     ("Kiểm tra", [P(r"Cách hai: $F=B_1I_2\ell=8{,}0\cdot10^{-6}\cdot5{,}0\cdot0{,}50=2{,}0\cdot10^{-5}\ \text{N}$ ✓."),
                   P("Lực lên dây (1) cùng độ lớn, ngược chiều (định luật III Newton).")])],
    [r"a) $\vec B_1$ hướng vào mặt phẳng hình, $B_1=8{,}0\ \mu\text{T}$.", r"b) Hút nhau ; $F=20\ \mu\text{N}$.", "c) Đẩy nhau, độ lớn không đổi."],
    r"Nhận dạng: thấy <b>hai dây song song mang dòng điện</b> → cùng chiều hút, ngược chiều đẩy; $F=2\cdot10^{-7}I_1I_2\ell/r$."))
STEPS.append(dict(
    nhan_dang=r"Thấy <b>hai dây dẫn song song có dòng điện</b> → nghĩ tới <b>cùng chiều hút, ngược chiều đẩy</b>, F = 2·10⁻⁷·I₁I₂ℓ/r",
    cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2},
    tom_de={"cho": [r"$r=10\ \text{cm}$", r"$I_1=4{,}0\ \text{A}$, $I_2=5{,}0\ \text{A}$ cùng chiều", r"đoạn $\ell=50\ \text{cm}$"],
            "tim": [r"a) chiều, độ lớn $B_1$ tại dây (2)", r"b) hút/đẩy ; $F$ (μN)", "c) đổi chiều $I_2$"]},
    buoc=[
        buoc("Chiều từ trường của dây (1) tại dây (2)", "Từ trường do dây (1) gây ra tại chỗ đặt dây (2) có chiều nào?",
             loi="Lấy chiều $\\vec B_1$ cùng chiều dòng điện $I_1$, quên rằng $\\vec B$ vuông góc với dây.",
             lua_chon=[("Vào mặt phẳng hình (⊗)", True),
                       ("Ra khỏi mặt phẳng hình (⊙)", "Đó là chiều bên trái dây (1); dây (2) ở bên phải nên bốn ngón tay đi vào mặt phẳng hình."),
                       ("Hướng lên, song song với dây", "Đường sức của dòng điện thẳng vuông góc với dây, không song song dây.")]),
        buoc("Độ lớn từ trường tại dây (2)", "Cảm ứng từ do dây (1) gây ra tại dây (2) bằng bao nhiêu μT?", dap_so=8, don_vi="μT", sai_so=0.1,
             loi=r"Thế $I_2$ thay cho $I_1$ (từ trường tại dây (2) do dây (1) tạo nên chỉ phụ thuộc $I_1$), hoặc giữ $r$ bằng cm.",
             ke=[(r"$B_1=2\cdot10^{-7}\dfrac{I_1}{r}$ với $r$ đổi ra mét", True),
                 (r"$B_1=2\cdot10^{-7}\dfrac{I_2}{r}$", "Từ trường tại dây (2) do dòng $I_1$ của dây (1) tạo ra."),
                 (r"$B_1=2\cdot10^{-7}\dfrac{I_1+I_2}{r}$", "Dây (2) không tự tác dụng lực lên chính nó; chỉ xét từ trường của dây (1).")]),
        buoc("Hút hay đẩy", "Lực từ tác dụng lên dây (2) hướng về đâu?",
             loi="Dùng tay phải thay cho tay trái, ra lực hướng ra xa dây (1).",
             lua_chon=[("Về phía dây (1): hai dây hút nhau", True),
                       ("Ra xa dây (1): hai dây đẩy nhau", "Đó là khi hai dòng điện ngược chiều; ở đây cùng chiều."),
                       ("Dọc theo dây (2)", "Lực từ vuông góc với dòng điện $I_2$ nên vuông góc với dây.")],
             ke=[(r"Bàn tay trái với $I_2$ và $\vec B_1$", True),
                 ("Quy tắc nắm tay phải với $I_2$", "Nắm tay phải cho chiều đường sức quanh dòng điện, không cho chiều lực."),
                 (r"Lấy lực cùng chiều $\vec B_1$", "Lực từ vuông góc với $\\vec B$, không cùng chiều.")]),
        buoc("Lực từ lên đoạn 50 cm", "Lực từ tác dụng lên đoạn 50 cm của dây (2) bằng bao nhiêu μN?", dap_so=20, don_vi="μN", sai_so=0.3,
             loi=r"Bỏ $\ell$ (ra lực trên mỗi mét) hoặc dùng $B_1I_1\ell$ thay cho $B_1I_2\ell$.",
             ke=[(r"Thế vào $F=2\cdot10^{-7}\dfrac{I_1I_2\ell}{r}$, đổi $\ell$, $r$ ra mét", True),
                 (r"$F=2\cdot10^{-7}\dfrac{I_1I_2}{r}$, bỏ $\ell$", "Công thức cho lực trên đoạn dài $\\ell$; bỏ $\\ell$ là tính lực trên 1 m."),
                 (r"$F=B_1I_1\ell$", "Lực lên dây (2) là từ trường của dây (1) tác dụng lên dòng $I_2$.")]),
        buoc("Đổi chiều dòng điện trong dây (2)", "Đổi chiều dòng điện trong dây (2), lực tương tác thay đổi thế nào?",
             loi="Nghĩ rằng hai dòng ngược chiều triệt tiêu nhau nên không còn lực.",
             lua_chon=[("Đẩy nhau, độ lớn không đổi", True),
                       ("Vẫn hút nhau, độ lớn giảm", "$I_2$ đổi chiều thì lực đổi chiều; độ lớn chỉ phụ thuộc $I_1I_2\\ell/r$."),
                       ("Không còn lực tương tác", "Hai dòng điện vẫn có, từ trường dây (1) vẫn tác dụng lên dòng $I_2$.")],
             ke=[(r"Giữ $\vec B_1$, đổi chiều $I_2$ rồi dùng lại bàn tay trái", True),
                 (r"Đổi cả chiều $\vec B_1$", "$\\vec B_1$ do $I_1$ tạo ra, $I_1$ không đổi nên $\\vec B_1$ giữ nguyên."),
                 ("Cộng hai dòng điện ngược chiều thành hiệu", "Hai dòng nằm ở hai dây khác nhau, không cộng trừ với nhau.")]),
        buoc("Kiểm tra"),
    ]))

# ───── D4 ─────
SOLS.append(sol(
    [r"<strong>Tăng tốc:</strong> định lí động năng $|q|U=\tfrac12mv^2$.",
     r"<strong>Lực từ lên hạt:</strong> $f=|q|vB$ khi $\vec v\perp\vec B$; chiều theo bàn tay trái với điện tích dương (electron: chiều ngược lại).",
     r"<strong>Chuyển động tròn đều:</strong> $|q|vB=\dfrac{mv^2}{R}$ ⇒ $R=\dfrac{mv}{|q|B}$ ; $T=\dfrac{2\pi m}{|q|B}$ không phụ thuộc $v$.",
     r"⚠ <strong>Điều kiện:</strong> $\vec v\perp\vec B$, từ trường đều, bỏ qua trọng lực."],
    [("Tốc độ khi qua khe S", [M(r"|q|U=\tfrac12mv^2\ \Rightarrow\ v=\sqrt{\dfrac{2|q|U}{m}}"),
                               M(r"v=\sqrt{\dfrac{2\cdot1{,}6\cdot10^{-19}\cdot500}{1{,}67\cdot10^{-27}}}"), A(r"v\approx3{,}10\cdot10^5\ \text{m/s}")]),
     ("Phía bị lệch", [P("Bàn tay trái: đường sức (⊗) đâm vào lòng bàn tay, chiều cổ tay → ngón tay theo $\\vec v$ (lên), prôtôn mang điện dương nên ngón cái chỉ chiều lực:"),
                       A("T:Lực từ tại S hướng sang trái ⇒ prôtôn đi nửa vòng tròn, đập vào phim bên trái S.")]),
     ("Bán kính quỹ đạo", [M(r"|q|vB=\dfrac{mv^2}{R}\ \Rightarrow\ R=\dfrac{mv}{|q|B}"),
                           M(r"R=\dfrac{1{,}67\cdot10^{-27}\cdot3{,}095\cdot10^5}{1{,}6\cdot10^{-19}\cdot0{,}10}"), A(r"R\approx3{,}23\cdot10^{-2}\ \text{m}=3{,}23\ \text{cm}")]),
     ("Khoảng cách từ S đến điểm đập", [P("S và điểm đập A là hai đầu một đường kính:"), M(r"SA=2R"), A(r"SA\approx6{,}46\ \text{cm}")]),
     ("Thời gian bay", [P("Hạt đi nửa vòng:"), M(r"t=\dfrac{T}{2}=\dfrac{\pi m}{|q|B}=\dfrac{\pi\cdot1{,}67\cdot10^{-27}}{1{,}6\cdot10^{-19}\cdot0{,}10}"),
                        A(r"t\approx3{,}28\cdot10^{-7}\ \text{s}")]),
     ("Tăng hiệu điện thế 4 lần", [M(r"v\sim\sqrt U\ \Rightarrow\ v'=2v"), M(r"R=\dfrac{mv}{|q|B}\ \Rightarrow\ SA'=2\,SA"),
                                   A(r"T:$SA$ tăng gấp 2 ; $t=\dfrac{\pi m}{|q|B}$ không phụ thuộc $v$ nên không đổi.")]),
     ("Kiểm tra", [P(r"Đơn vị $R$: $\dfrac{\text{kg}\cdot\text{m/s}}{\text{C}\cdot\text{T}}=\text{m}$ ✓ ; bán kính vài xentimét vừa với khối phổ kế."),
                   P(r"Thử lại $t=\dfrac{\pi R}{v}=\dfrac{\pi\cdot0{,}0323}{3{,}095\cdot10^5}\approx3{,}28\cdot10^{-7}\ \text{s}$ ✓.")])],
    [r"a) $v\approx3{,}10\cdot10^5\ \text{m/s}$.", r"b) Bên trái S, $SA\approx6{,}46\ \text{cm}$.", r"c) $t\approx3{,}28\cdot10^{-7}\ \text{s}$.",
     "d) Khoảng cách tăng gấp 2, thời gian bay không đổi."],
    r"Nhận dạng: thấy <b>hạt tăng tốc qua U rồi bay vào từ trường, đập vào phim</b> → $|q|U=\tfrac12mv^2$, $R=mv/(|q|B)$, khoảng cách $2R$."))
STEPS.append(dict(
    nhan_dang=r"Thấy <b>hạt bay vào từ trường vuông góc đường sức</b> → nghĩ tới <b>|q|vB = mv²/R</b>, đi nửa vòng thì cách khe 2R",
    cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 2},
    tom_de={"cho": [r"prôtôn $q=+1{,}6\cdot10^{-19}\ \text{C}$, $m=1{,}67\cdot10^{-27}\ \text{kg}$", r"$U=500\ \text{V}$ ; $B=0{,}10\ \text{T}$ (⊗)", r"qua S hướng lên, $\vec v\perp\vec B$"],
            "tim": [r"a) $v$", "b) phía và khoảng cách điểm đập", "c) thời gian bay", "d) khi U tăng 4 lần"]},
    buoc=[
        buoc("Tốc độ khi qua khe S", r"Tốc độ của prôtôn khi qua khe S bằng bao nhiêu (đơn vị $10^5$ m/s)?", dap_so=3.10, don_vi="·10⁵ m/s", sai_so=0.02,
             loi=r"Quên hệ số $\tfrac12$ (viết $|q|U=mv^2$) hoặc quên lấy căn bậc hai."),
        buoc("Phía bị lệch", "Lực từ tại S hướng về đâu, prôtôn đập vào phim ở phía nào?",
             loi="Dùng bàn tay trái nhưng để ngón tay theo chiều đường sức, hoặc đổi chiều như với electron.",
             lua_chon=[("Lực sang trái; đập vào phim bên trái S", True),
                       ("Lực sang phải; đập vào phim bên phải S", "Đó là chiều với electron (điện tích âm); prôtôn mang điện dương lấy đúng chiều ngón cái tay trái."),
                       ("Lực hướng lên; prôtôn bay thẳng không lệch", "Lực từ luôn vuông góc với $\\vec v$ nên hạt bị lệch, quỹ đạo tròn.")],
             ke=[("Bàn tay trái: đường sức vào lòng bàn tay, chiều cổ tay → ngón tay theo $\\vec v$", True),
                 ("Quy tắc nắm tay phải", "Nắm tay phải tìm chiều đường sức quanh dòng điện, không tìm chiều lực."),
                 ("Lấy lực cùng chiều đường sức", "Lực từ vuông góc với đường sức, không cùng chiều.")]),
        buoc("Bán kính quỹ đạo", "Bán kính quỹ đạo của prôtôn bằng bao nhiêu cm?", dap_so=3.23, don_vi="cm", sai_so=0.03,
             loi=r"Đảo phân số thành $R=\dfrac{|q|B}{mv}$, hoặc quên đổi mét ra xentimét.",
             ke=[(r"Lực từ là lực hướng tâm: $|q|vB=\dfrac{mv^2}{R}$", True),
                 (r"$R=\dfrac{|q|B}{mv}$", "Phân số bị đảo; kiểm đơn vị thấy không ra mét."),
                 (r"Cho $|q|vB=mg$", "Đề bỏ qua trọng lực; lực từ làm hạt đổi hướng, không cân bằng với trọng lực.")]),
        buoc("Khoảng cách từ S đến điểm đập", "Điểm đập cách khe S bao nhiêu cm?", dap_so=6.46, don_vi="cm", sai_so=0.05,
             loi=r"Lấy khoảng cách bằng $R$, hoặc bằng độ dài cung $\pi R$.",
             ke=[("Hạt đi nửa vòng tròn: khoảng cách bằng đường kính 2R", True),
                 ("Khoảng cách bằng R", "S và điểm đập là hai đầu một đường kính, không phải bán kính."),
                 (r"Khoảng cách bằng $\pi R$", "$\\pi R$ là quãng đường đi theo cung, không phải khoảng cách thẳng trên phim.")]),
        buoc("Thời gian bay", r"Thời gian prôtôn bay từ S đến phim bằng bao nhiêu (đơn vị $10^{-7}$ s)?", dap_so=3.28, don_vi="·10⁻⁷ s", sai_so=0.03,
             loi=r"Lấy cả chu kì $T$ (hạt chỉ đi nửa vòng), hoặc lấy $t=\dfrac{2R}{v}$ như đi thẳng.",
             ke=[(r"$t=\dfrac{T}{2}$ với $T=\dfrac{2\pi m}{|q|B}$", True),
                 ("$t=T$", "Hạt chỉ đi nửa vòng tới phim."),
                 (r"$t=\dfrac{2R}{v}$", "Hạt đi theo cung tròn dài $\\pi R$, không đi thẳng đoạn $2R$.")]),
        buoc("Tăng hiệu điện thế 4 lần", "Tăng U lên 4 lần thì khoảng cách từ S đến điểm đập và thời gian bay thay đổi thế nào?",
             loi=r"Cho $v$ tỉ lệ thuận với $U$ (ra khoảng cách gấp 4) hoặc cho thời gian giảm vì hạt nhanh hơn.",
             lua_chon=[("Khoảng cách gấp 2, thời gian bay không đổi", True),
                       ("Khoảng cách gấp 4, thời gian bay không đổi", "$v\\sim\\sqrt U$ nên U gấp 4 thì $v$ chỉ gấp 2, $R$ gấp 2."),
                       ("Khoảng cách gấp 2, thời gian bay giảm một nửa", "$T=2\\pi m/(|q|B)$ không phụ thuộc $v$: hạt nhanh hơn nhưng đi vòng lớn hơn đúng bấy nhiêu.")],
             ke=[("Xét $v$, $R$, $T$ phụ thuộc $U$ thế nào", True),
                 ("Cho khoảng cách tỉ lệ thuận với $U$", "Khoảng cách $2R\\sim v\\sim\\sqrt U$, không tỉ lệ thuận với $U$."),
                 ("Cho thời gian bay tỉ lệ nghịch với $v$", "Quãng đường cũng tăng theo $v$; chu kì không phụ thuộc $v$.")]),
        buoc("Kiểm tra"),
    ]))

# ───── D5 ─────
SOLS.append(sol(
    [r"<strong>Hiện tượng:</strong> thanh chuyển động cắt đường sức, từ thông qua mạch kín biến thiên ⇒ có suất điện động cảm ứng $e=Bv\ell$.",
     r"<strong>Định luật Lenz:</strong> dòng cảm ứng chống lại sự biến thiên từ thông ⇒ lực từ lên thanh cản chuyển động.",
     r"<strong>Công thức:</strong> $I=\dfrac{e}{R}$ ; $F=BI\ell$ ; $P_k=F_kv$ ; $P_R=I^2R$.",
     r"⚠ <strong>Điều kiện:</strong> thanh, $\vec v$, $\vec B$ vuông góc từng đôi; bỏ qua điện trở thanh, ray và ma sát."],
    [("Suất điện động cảm ứng", [M(r"e=Bv\ell=0{,}50\cdot4{,}0\cdot0{,}20"), A(r"e=0{,}40\ \text{V}")]),
     ("Cường độ dòng điện", [M(r"I=\dfrac{e}{R}=\dfrac{0{,}40}{0{,}50}"), A(r"I=0{,}80\ \text{A}")]),
     ("Chiều dòng điện trong thanh", [P("Thanh ra xa $R$ ⇒ diện tích mạch tăng ⇒ từ thông (⊗) tăng. Từ trường cảm ứng phải hướng ra (⊙) ⇒ dòng điện ngược chiều kim đồng hồ:"),
                                      A("T:Trong thanh, dòng điện chạy từ N đến M.")]),
     ("Chiều lực từ", [P("Bàn tay trái: đường sức (⊗) vào lòng bàn tay, dòng điện từ N lên M, ngón cái chỉ sang trái:"),
                       A("T:Lực từ ngược chiều $\\vec v$, cản chuyển động của thanh.")]),
     ("Lực kéo", [P("Thanh chuyển động đều ⇒ lực kéo cân bằng lực từ:"), M(r"F_k=F=BI\ell=0{,}50\cdot0{,}80\cdot0{,}20"), A(r"F_k=0{,}080\ \text{N}")]),
     ("Công suất lực kéo", [M(r"P_k=F_kv=0{,}080\cdot4{,}0"), A(r"P_k=0{,}32\ \text{W}")]),
     ("Công suất toả nhiệt", [M(r"P_R=I^2R=0{,}80^2\cdot0{,}50"), A(r"P_R=0{,}32\ \text{W}")]),
     ("Kiểm tra", [P(r"$P_k=P_R$: toàn bộ công của lực kéo chuyển thành nhiệt trên $R$ (bảo toàn năng lượng) ✓."),
                   P(r"Cũng có $P=eI=0{,}40\cdot0{,}80=0{,}32\ \text{W}$ ✓.")])],
    [r"a) $e=0{,}40\ \text{V}$ ; $I=0{,}80\ \text{A}$.", "b) Từ N đến M.", r"c) Lực từ ngược chiều $\vec v$ ; $F_k=0{,}080\ \text{N}$.",
     r"d) $P_k=P_R=0{,}32\ \text{W}$: công kéo chuyển hết thành nhiệt."],
    r"Nhận dạng: thấy <b>thanh trượt trên hai ray trong từ trường</b> → $e=Bv\ell$, Lenz cho chiều, lực từ luôn cản chuyển động."))
STEPS.append(dict(
    nhan_dang=r"Thấy <b>thanh trượt trên hai ray trong từ trường</b> → nghĩ tới <b>e = Bvℓ</b>, Lenz cho chiều, <b>lực từ cản</b> chuyển động",
    cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 2},
    tom_de={"cho": [r"$\ell=20\ \text{cm}$ ; $R=0{,}50\ \Omega$", r"$v=4{,}0\ \text{m/s}$ ra xa $R$", r"$B=0{,}50\ \text{T}$ (⊗)"],
            "tim": [r"a) $e$, $I$", "b) chiều $I$ trong thanh", r"c) chiều lực từ ; $F_k$", r"d) $P_k$, $P_R$"]},
    buoc=[
        buoc("Suất điện động cảm ứng", "Suất điện động cảm ứng trong thanh bằng bao nhiêu vôn?", dap_so=0.4, don_vi="V", sai_so=0.005,
             loi=r"Giữ $\ell$ bằng xentimét khi thế số (ra lớn gấp 100 lần)."),
        buoc("Cường độ dòng điện", "Cường độ dòng điện qua R bằng bao nhiêu ampe?", dap_so=0.8, don_vi="A", sai_so=0.01,
             loi=r"Nhân $e$ với $R$ thay vì chia.",
             ke=[(r"Định luật Ôm cho mạch kín: $I=\dfrac{e}{R}$", True),
                 (r"$I=eR$", "Đơn vị V·Ω không phải ampe; định luật Ôm là chia cho R."),
                 (r"$I=\dfrac{e}{R+\ell}$", "$\\ell$ là chiều dài, không phải điện trở; đề bỏ qua điện trở thanh.")]),
        buoc("Chiều dòng điện trong thanh", "Dòng điện trong thanh chạy theo chiều nào?",
             loi="Cho rằng thanh chạy đều nên không có dòng điện, hoặc dùng bàn tay trái với $\\vec v$ và $\\vec B$.",
             lua_chon=[("Từ N đến M", True),
                       ("Từ M đến N", "Từ thông (⊗) tăng nên từ trường cảm ứng hướng ra, dòng ngược chiều kim đồng hồ: trong thanh đi lên từ N đến M."),
                       ("Không có dòng điện vì thanh chuyển động đều", "Thanh chạy đều nhưng diện tích mạch vẫn tăng, từ thông vẫn biến thiên.")],
             ke=[("Xét từ thông qua mạch tăng hay giảm rồi dùng định luật Lenz", True),
                 ("Dùng bàn tay trái với $\\vec v$ và $\\vec B$", "Bàn tay trái cho chiều lực lên dòng điện; chiều dòng cảm ứng tìm bằng Lenz hoặc bàn tay phải."),
                 ("Cho dòng điện cùng chiều $\\vec v$", "Dòng điện chạy dọc thanh, vuông góc với $\\vec v$.")]),
        buoc("Chiều lực từ", "Lực từ tác dụng lên thanh có chiều nào?",
             loi="Cho lực từ cùng chiều chuyển động, quên rằng theo Lenz dòng cảm ứng luôn chống lại nguyên nhân sinh ra nó.",
             lua_chon=[("Ngược chiều $\\vec v$, cản chuyển động", True),
                       ("Cùng chiều $\\vec v$, đẩy thanh nhanh hơn", "Nếu vậy thanh tự tăng tốc mà không cần kéo — trái định luật Lenz và bảo toàn năng lượng."),
                       ("Dọc theo thanh", "Lực từ vuông góc với dòng điện trong thanh, nên vuông góc với thanh.")],
             ke=[("Bàn tay trái với dòng điện vừa tìm và $\\vec B$", True),
                 ("Nắm tay phải quanh thanh", "Nắm tay phải cho chiều đường sức quanh dòng điện, không cho chiều lực."),
                 ("Lấy lực cùng chiều dòng điện", "Lực từ vuông góc với dòng điện.")]),
        buoc("Lực kéo", "Để thanh chuyển động đều cần lực kéo bao nhiêu niutơn?", dap_so=0.08, don_vi="N", sai_so=0.002,
             loi=r"Cho rằng chuyển động đều thì không cần lực kéo, hoặc lấy nhầm $Bv\ell$.",
             ke=[(r"Chuyển động đều: $F_k=F=BI\ell$", True),
                 ("$F_k=0$ vì thanh chuyển động đều", "Thanh chịu lực từ cản; muốn đều phải có lực kéo cân bằng lực từ."),
                 (r"$F_k=Bv\ell$", "$Bv\\ell$ là suất điện động (V), không phải lực.")]),
        buoc("Công suất lực kéo", "Công suất của lực kéo bằng bao nhiêu oát?", dap_so=0.32, don_vi="W", sai_so=0.005,
             loi=r"Nhân lực với chiều dài thanh thay cho tốc độ.",
             ke=[(r"$P_k=F_kv$", True),
                 (r"$P_k=F_k\ell$", "$\\ell$ là chiều dài thanh; công suất bằng lực nhân tốc độ."),
                 (r"$P_k=\dfrac{F_k}{v}$", "Công suất bằng lực nhân tốc độ, không chia.")]),
        buoc("Công suất toả nhiệt", "Công suất toả nhiệt trên R bằng bao nhiêu oát?", dap_so=0.32, don_vi="W", sai_so=0.005,
             loi=r"Dùng $P=IR$ (đó là hiệu điện thế) hoặc quên bình phương $I$.",
             ke=[(r"$P_R=I^2R$", True),
                 (r"$P_R=IR$", "$IR$ là hiệu điện thế (V), không phải công suất."),
                 (r"$P_R=\dfrac{e}{R}$", "$e/R$ là cường độ dòng điện.")]),
        buoc("Kiểm tra"),
    ]))

assert len(DANG) == len(ANALYSIS) == len(SOLS) == len(STEPS) == len(CONG_CU) == 5
for s, c in zip(STEPS, CONG_CU):
    assert len(c()["lop"]) == len(s["buoc"]), (len(c()["lop"]), len(s["buoc"]))

# ═════════════ Ghi file ═════════════
BUILD = [lambda k: ""] * len(DANG)          # "một dạng — một hình": không còn <figure>
write(J, 201, "Chủ đề thêm. Từ trường ngoài SGK hay gặp trong đề thi", DANG, BUILD, ANALYSIS, SOLS)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-11-18"
d["review"] = {"checked": True, "notes": "đáp số mọi bước tự giải lại bằng python (assert trong build-hinh-201.py), chiều bằng tích có hướng; "
               "chưa qua kiem-code độc lập; chưa xem /dev/btm"}
for i, q in enumerate(d["dang_bai"]):
    q["cong_cu"] = CONG_CU[i]()
# tu_luan: bài mới không có ví dụ cũ → bỏ khoá (tu_luan [] làm validate/publish đọc .label lỗi)
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
txt = open(J, encoding="utf8").read()
assert "marker-end" not in txt and "<figure" not in txt
# đối chiếu dap_so bước với số tự giải
DS = {(0, 2): ANS["BM"], (0, 3): ANS["BN"], (1, 0): ANS["n2"], (1, 1): ANS["N2"], (1, 2): ANS["B2"], (1, 3): ANS["S2"],
      (1, 4): ANS["PHI2"], (2, 1): ANS["B13"], (2, 3): ANS["F3"], (3, 0): ANS["v4"], (3, 2): ANS["R4"], (3, 3): ANS["d4"],
      (3, 4): ANS["t4"], (4, 0): ANS["e5"], (4, 1): ANS["I5"], (4, 4): ANS["F5"], (4, 5): ANS["Pk5"], (4, 6): ANS["PR5"]}
for (i, j), v in DS.items():
    s = d["dang_bai"][i]["buoc"][j]
    assert abs(s["dap_so"] - v) <= s["sai_so"] / 2 + 1e-9, (i, j, s["dap_so"], v)
print("ghi", J, len(d["dang_bai"]), "dạng; dap_so khớp", len(DS), "bước số")
