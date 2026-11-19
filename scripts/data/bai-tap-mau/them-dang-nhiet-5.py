"""Thêm HAI dạng vào bài tập mẫu lesson 5 (Vật lí 12, Bài 4. Thực hành đo nhiệt dung riêng, nhiệt nóng chảy riêng, nhiệt hoá hơi riêng).
Đọc old/5.json (bản dump DB, KHÔNG sửa), dựng 5.json gồm 6 dạng: D1, D2, [A mới], [B mới], D3 cũ, D4 cũ.
  A (Dạng 3, cấp 2, giau_buoc_cuoi, mẹo Đòn bẩy nhiệt): đo c kim loại bằng cách trộn, có vỏ nhiệt lượng kế.
  B (Dạng 4, cấp 3, giau_tu_buoc_2, mẹo Quỹ nhiệt): thả đá 0 °C vào nước ấm, đá có tan hết không.
Hình: họ thanh_nang_luong (hop_he), cong_cu.de = true; không có <figure> trong đề/phân tích.
Idempotent: luôn dựng lại từ old/5.json. Không ghi DB.
Chạy: python3 scripts/data/bai-tap-mau/them-dang-nhiet-5.py"""
import copy, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import sol, buoc, tbl, M, P, A
from meo_nhiet import don_bay_nhiet, quy_nhiet

OLD = os.path.join(HERE, "old", "5.json")
OUT = os.path.join(HERE, "5.json")

# ───────────── số liệu + assert ─────────────
# Dạng A
mn, cn, Cv, mk = 0.200, 4200, 40, 0.150
tn, tk, tcb = 20.0, 100.0, 25.0
C1 = mn * cn + Cv
Qthu = C1 * (tcb - tn)
dtk = tk - tcb
cA = Qthu / (mk * dtk)
assert C1 == 880 and abs(Qthu - 4400) < 1e-9 and dtk == 75 and round(cA) == 391, (C1, Qthu, dtk, cA)
c_quen_vo = mn * cn * (tcb - tn) / (mk * dtk)           # quên vỏ
c_dt80 = Qthu / (mk * (tk - tn))                         # lấy Δt = 100 − 20
c_dt5 = Qthu / (mk * (tcb - tn))                         # lấy Δt của kim loại = độ tăng của nước
c_mn = Qthu / (mn * dtk)                                 # dùng khối lượng nước làm mẫu số
assert round(c_quen_vo) == 373 and round(c_dt80) == 367
for w in (c_quen_vo, c_dt80, c_dt5, c_mn, Qthu / dtk, C1 * tcb / (mk * dtk)):
    assert abs(w - 391) > 4, w                           # mọi cách sai nằm ngoài sai_so của bước c
assert abs(Cv + 0 - 40) == 0
dong, sat, nhom = 380, 460, 880
assert abs(cA - dong) < abs(cA - sat) < abs(cA - nhom)
assert [round(abs(cA - x)) for x in (dong, sat, nhom)] == [11, 69, 489]
mc_kl = Qthu / dtk
assert round(mc_kl, 1) == 58.7 and round(C1 / mc_kl) == 15 and (tk - tcb) / (tcb - tn) == 15
assert abs(mk * 391 * dtk - 4400) < 3

# Dạng B
md, mw, tw, lam = 0.150, 0.300, 30.0, 3.34e5
Q0 = mw * cn * tw
Qtan = lam * md
assert abs(Q0 - 37800) < 1e-6 and abs(Qtan - 50100) < 1e-6 and Q0 < Qtan
mtan = Q0 / lam
mcon = md - mtan
assert round(mtan, 4) == 0.1132 and round(mcon, 4) == 0.0368 and round(mcon * 1000, 1) == 36.8
t_sai = (Q0 - Qtan) / (mw * cn + md * cn)               # giả định tan hết: 0,3·4200·(30−t) = λ·0,15 + 0,15·4200·t
assert round(t_sai, 1) == -6.5
assert abs(mtan + mcon - md) < 1e-12
assert abs(mtan - 0.113) < 0.002 and abs(mcon * 1000 - 36.8) < 1.0
assert abs(round(mtan, 3) * 1000 - 113) < 1 and abs((md - round(mtan, 3)) * 1000 - 36.8) < 1.0   # làm tròn sớm vẫn trong sai_so

TOPIC_A = "Tính nhiệt lượng theo nhiệt dung riêng"
TOPIC_B = "Nhiệt nóng chảy riêng và nhiệt hoá hơi riêng"

# ═════════════════════════ DẠNG A ═════════════════════════
A_PROBLEM = (
    r"<p>Một nhóm đo nhiệt dung riêng của một miếng kim loại bằng cách trộn. Miếng kim loại khối lượng $0{,}150\ \text{kg}$ "
    r"được ngâm lâu trong nước đang sôi (coi là $100\ ^\circ\text{C}$), vớt ra thật nhanh, lau khô rồi thả vào nhiệt lượng kế "
    r"chứa $0{,}200\ \text{kg}$ nước ở $20{,}0\ ^\circ\text{C}$. Vỏ nhiệt lượng kế cùng que khuấy có nhiệt dung $40\ \text{J/K}$, "
    r"ban đầu cũng ở $20{,}0\ ^\circ\text{C}$. Khuấy nhẹ cho đều; nhiệt độ ổn định ở $25{,}0\ ^\circ\text{C}$. "
    r"Nhiệt dung riêng của nước là $4200\ \text{J/(kg·K)}$. Coi nhiệt dung riêng các chất không đổi trong khoảng nhiệt độ này; "
    r"bỏ qua nhiệt do khuấy và sự trao đổi nhiệt với môi trường; kim loại không phản ứng với nước.</p>"
    r"<ol type='a'><li>Tính nhiệt dung riêng $c$ của kim loại.</li>"
    r"<li>Đối chiếu bảng (đồng $380$; sắt $460$; nhôm $880\ \text{J/(kg·K)}$): kim loại này gần chất nào nhất?</li></ol>"
)

A_ANALYSIS = [
    (r"\"Miếng kim loại $0{,}150$ kg được ngâm lâu trong nước đang sôi\"",
     r"$m_{kl}=0{,}150\ \text{kg}$ ; $t_{kl}=100\ ^\circ\text{C}$ (đồng đều)",
     "Vật nóng hơn sẽ toả nhiệt, nhiệt độ giảm đến nhiệt độ cân bằng"),
    (r"\"vớt ra thật nhanh, lau khô … không phản ứng với nước\"",
     "Chỉ kim loại toả nhiệt vào nhiệt lượng kế",
     "⚠ Không vật nào chuyển thể, không mang thêm nước nóng vào, không có hoà tan hay phản ứng toả/thu nhiệt"),
    (r"\"$0{,}200$ kg nước ở $20{,}0\ ^\circ$C\"",
     r"$m_n=0{,}200\ \text{kg}$ ; $c_n=4200\ \text{J/(kg·K)}$ ; $t_n=20{,}0\ ^\circ\text{C}$",
     r"Nhiệt lượng $Q=mc\,\Delta t$ ; vật thu nhiệt có nhiệt độ tăng"),
    (r"\"Vỏ nhiệt lượng kế cùng que khuấy có nhiệt dung $40$ J/K, cũng ở $20{,}0\ ^\circ$C\"",
     r"$C_v=40\ \text{J/K}$ ; cùng $20{,}0\ ^\circ\text{C}$ với nước",
     r"Nhiệt dung $C=mc$ là nhiệt cần để vật nóng thêm $1\ \text{K}$ ; hai vật cùng nhiệt độ đầu và cuối thì gộp được nhiệt dung"),
    (r"\"Khuấy nhẹ … bỏ qua trao đổi nhiệt với môi trường … $c$ không đổi\"",
     "Hệ cô lập: chỉ kim loại, nước và vỏ trao đổi nhiệt",
     r"⚠ Chỉ khi bỏ qua nhiệt do khuấy và trao đổi với môi trường, $c$ không đổi trong khoảng nhiệt độ thì mới dùng $Q_{toả}=Q_{thu}$"),
    (r"\"nhiệt độ ổn định ở $25{,}0\ ^\circ$C\"",
     r"$t_{cb}=25{,}0\ ^\circ\text{C}$",
     r"Cân bằng: mọi vật cùng nhiệt độ cuối ; $\Delta t$ luôn lấy độ tăng (vật thu) hoặc độ giảm (vật toả), dương"),
    (r"\"Tính nhiệt dung riêng $c$ của kim loại\"",
     r"Cần tìm $c$",
     r"$Q_{toả}=Q_{thu}$ với $Q=mc\,\Delta t$"),
    (r"\"gần chất nào nhất?\"",
     r"So $c$ vừa tính với ba giá trị của bảng",
     "Chất nào có giá trị bảng chênh lệch ít nhất với kết quả?"),
]


def a_sol():
    return sol(
        [
            r"<strong>Khái niệm:</strong> nhiệt lượng $Q=mc\,\Delta t$ ; nhiệt dung $C=mc$ (J/K) ; vật cùng nhiệt độ đầu và cuối thì cộng nhiệt dung.",
            r"<strong>Định luật:</strong> hệ cô lập đạt cân bằng nhiệt thì $Q_{toả}=Q_{thu}$.",
            r"<strong>Công thức:</strong> $m_{kl}c\,(t_{kl}-t_{cb})=(m_nc_n+C_v)(t_{cb}-t_n)$, suy ra $c$.",
            r"⚠ <strong>Điều kiện:</strong> bỏ qua nhiệt do khuấy và trao đổi với môi trường ; không chuyển thể ; $c$ coi không đổi.",
        ],
        [
            ("Nhiệt dung của phần lạnh",
             [P(r"Nước và vỏ cùng ở $20{,}0\ ^\circ\text{C}$ nên cùng nóng lên tới $25{,}0\ ^\circ\text{C}$: gộp thành một vật."),
              M(r"C_1=m_nc_n+C_v=0{,}200\cdot4200+40"),
              A(r"C_1=880\ \text{J/K}")]),
            ("Nhiệt lượng phần lạnh thu vào",
             [M(r"Q_{thu}=C_1\,(t_{cb}-t_n)=880\cdot(25{,}0-20{,}0)"),
              A(r"Q_{thu}=4400\ \text{J}")]),
            ("Độ giảm nhiệt độ của kim loại",
             [P(r"Kim loại nguội từ $100\ ^\circ\text{C}$ xuống nhiệt độ cân bằng:"),
              M(r"\Delta t_{kl}=t_{kl}-t_{cb}=100-25{,}0"),
              A(r"\Delta t_{kl}=75{,}0\ \text{K}")]),
            ("Nhiệt dung riêng của kim loại",
             [P(r"Hệ cô lập nên $Q_{toả}=Q_{thu}$, với $Q_{toả}=m_{kl}c\,\Delta t_{kl}$:"),
              M(r"c=\dfrac{Q_{thu}}{m_{kl}\,\Delta t_{kl}}=\dfrac{4400}{0{,}150\cdot75{,}0}"),
              A(r"c\approx391\ \text{J/(kg·K)}")]),
            ("Đối chiếu với bảng",
             [P("Chênh lệch giữa kết quả và từng giá trị của bảng (đồng, sắt, nhôm):"),
              M(r"|391-380|=11\ ;\ |391-460|=69\ ;\ |391-880|=489"),
              A(r"T:Chênh lệch nhỏ nhất ở đồng ($380\ \text{J/(kg·K)}$): kim loại này gần đồng.")]),
            ("Kiểm tra",
             [P(r"Thế ngược: $0{,}150\cdot391\cdot75{,}0\approx4400\ \text{J}$, khớp $Q_{thu}$."),
              P(r"$c$ cùng bậc $10^{2}$ với các kim loại trong bảng và nhỏ hơn $c$ của nước nhiều, hợp lí: kim loại nóng lên, nguội đi nhanh hơn nước.")]),
        ],
        [r"a) $c\approx391\ \text{J/(kg·K)}$", "b) gần đồng nhất"],
        r"Nhận dạng: đề cho <strong>vật nóng thả vào nước có vỏ nhiệt lượng kế</strong> và hỏi <strong>c</strong> → gộp nước với vỏ, lập $Q_{toả}=Q_{thu}$.",
    )


A_STEPS = dict(
    nhan_dang="Thấy <b>vật nóng thả vào nước, vỏ nhiệt lượng kế có nhiệt dung</b> → nghĩ tới <b>Q_toả = Q_thu</b>, gộp nước với vỏ",
    cap_do=2,
    fading="giau_buoc_cuoi",
    go_roi={"buoc_hay_sai": 0},
    buoc=[
        buoc("Nhiệt dung của phần lạnh",
             hoi="Phần lạnh (nước cùng vỏ nhiệt lượng kế) cần nhận bao nhiêu J để nóng thêm 1 K?",
             dap_so=880, don_vi="J/K", sai_so=5,
             loi="Chỉ tính nước, bỏ vỏ nhiệt lượng kế dù đề đã cho nhiệt dung của vỏ; hoặc cộng khối lượng với nhiệt dung."),
        buoc("Nhiệt lượng phần lạnh thu vào",
             hoi="Phần lạnh thu vào bao nhiêu nhiệt lượng?",
             dap_so=4400, don_vi="J", sai_so=20,
             ke=[("Nhiệt dung phần lạnh nhân độ tăng nhiệt độ của nó", True),
                 ("Nhiệt dung phần lạnh nhân độ giảm nhiệt độ của kim loại", "Đó là độ giảm của vật toả nhiệt; phần lạnh nóng lên từ nhiệt độ đầu của nó tới nhiệt độ cân bằng."),
                 ("Nhiệt dung phần lạnh nhân nhiệt độ cân bằng", "Nhiệt lượng tỉ lệ với độ tăng nhiệt độ, không phải nhiệt độ tính từ 0 °C.")],
             loi="Lấy nhiệt độ cân bằng thay cho độ tăng nhiệt độ của phần lạnh."),
        buoc("Độ giảm nhiệt độ của kim loại",
             hoi="Kim loại nguội đi bao nhiêu K khi đạt cân bằng nhiệt?",
             dap_so=75, don_vi="K", sai_so=0.5,
             ke=[("Nhiệt độ đầu của kim loại trừ nhiệt độ cân bằng", True),
                 ("Nhiệt độ đầu của kim loại trừ nhiệt độ đầu của nước", "Kim loại chỉ nguội tới nhiệt độ cân bằng chung, không nguội tới nhiệt độ đầu của nước."),
                 ("Nhiệt độ cân bằng trừ nhiệt độ đầu của nước", "Đó là độ tăng của phần lạnh, không phải độ giảm của kim loại.")],
             loi="Lấy mốc cuối của kim loại là nhiệt độ đầu của nước thay vì nhiệt độ cân bằng."),
        buoc("Nhiệt dung riêng của kim loại",
             hoi="Nhiệt dung riêng của kim loại là bao nhiêu J/(kg·K)?",
             dap_so=391, don_vi="J/(kg·K)", sai_so=4,
             ke=[("Cho nhiệt toả bằng nhiệt thu, với nhiệt toả bằng khối lượng kim loại nhân c nhân độ giảm nhiệt độ, rồi giải ra c", True),
                 ("Lấy nhiệt thu chia cho độ giảm nhiệt độ của kim loại, không cần khối lượng", "c tính cho 1 kg nên phải chia thêm cho khối lượng của vật toả nhiệt."),
                 ("Lấy nhiệt thu chia cho khối lượng nước và độ giảm nhiệt độ của kim loại", "Vật toả nhiệt là kim loại nên mẫu số dùng khối lượng của kim loại, không dùng khối lượng của nước.")],
             loi="Dùng khối lượng nước thay cho khối lượng miếng kim loại ở mẫu số."),
        buoc("Đối chiếu với bảng",
             hoi="Kim loại này gần chất nào nhất trong ba chất của bảng?",
             lua_chon=[("Đồng", True),
                       ("Sắt", "So từng giá trị của bảng với kết quả của bước trước rồi chọn chất có chênh lệch nhỏ nhất, không chọn theo thứ tự trong bảng."),
                       ("Nhôm", "Giá trị của nhôm cách xa kết quả vài lần; chọn chất có chênh lệch nhỏ nhất, không phải lớn nhất.")],
             ke=[("So kết quả với từng giá trị của bảng, chọn chất chênh lệch nhỏ nhất", True),
                 ("Chọn chất có nhiệt dung riêng lớn nhất trong bảng", "Đề hỏi chất gần với kết quả đo, không phải chất có c lớn nhất."),
                 ("Chọn chất đứng đầu bảng", "Thứ tự trong bảng không liên quan tới kết quả đo.")],
             loi="Chọn theo thứ tự trong bảng thay vì so độ chênh lệch."),
        buoc("Kiểm tra"),
    ],
)

A_TOM_DE = {
    "cho": [
        r"Kim loại $0{,}150\ \text{kg}$, $100\ ^\circ\text{C}$ thả vào $0{,}200\ \text{kg}$ nước $20{,}0\ ^\circ\text{C}$ ; vỏ kèm que khuấy $40\ \text{J/K}$",
        r"Cân bằng ở $25{,}0\ ^\circ\text{C}$ ; $c_{nước}=4200\ \text{J/(kg·K)}$",
        r"Bảng: đồng $380$ ; sắt $460$ ; nhôm $880\ \text{J/(kg·K)}$",
    ],
    "tim": [r"a) $c$ của kim loại", "b) gần chất nào trong bảng"],
}

A_CONG_CU = {
    "loai": "thanh_nang_luong", "de": True,
    "canh": {"kieu": "hop_he", "ten": "nước+vỏ"},
    "cot": [{"ten": "Q_toả", "mau": "max"}, {"ten": "Q_thu", "mau": "min"}],
    "max": 5000, "don_vi": "J",
    "hinh": [
        {"loai": "mui", "vao": True, "nhan": "100°C", "hang": 0},
        {"loai": "mui", "vao": False, "nhan": "20°C", "hang": 0},
    ],
    "lop": [
        [{"loai": "ghi", "text": "C₁ = 0,2·4200 + 40 = 880 J/K"}],
        [{"loai": "cot", "ten": "Q_thu", "gia_tri": 4400, "nhan": "4400"},
         {"loai": "ghi", "text": "Q_thu = 880·(25 − 20) = 4400 J"}],
        [{"loai": "ghi", "text": "Kim loại nguội 100 − 25 = 75 K"}],
        [{"loai": "cot", "ten": "Q_toả", "gia_tri": 4400, "nhan": "4400"},
         {"loai": "ghi", "text": "c = 4400 : (0,15·75) ≈ 391 J/(kg·K)"}],
        [{"loai": "ghi", "text": "Gần đồng (380): chênh nhỏ nhất"}],
        [{"loai": "ghi", "text": "Kiểm: 0,15·391·75 ≈ 4400 J ✓"}],
    ],
}

A_NOI = (
    r"<p>Ở dạng này: nước và vỏ nhiệt lượng kế cùng ở $20{,}0\ ^\circ\text{C}$ nên gộp thành <b>một</b> quả nặng $0{,}200\cdot4200+40=880\ \text{J/K}$. "
    r"Tay đòn bên phần lạnh là $5{,}0\ \text{K}$, bên kim loại là $75{,}0\ \text{K}$: quả nặng kim loại nhẹ hơn khoảng $15$ lần, "
    r"tức $mc\approx58{,}7\ \text{J/K}$. Quên vỏ là bớt quả nặng bên lạnh: điểm tựa trượt về phía kim loại nên $c$ tính ra nhỏ hơn thật.</p>"
)

# ═════════════════════════ DẠNG B ═════════════════════════
B_PROBLEM = (
    r"<p>Thả $0{,}150\ \text{kg}$ nước đá ở $0\ ^\circ\text{C}$ vào nhiệt lượng kế chứa $0{,}300\ \text{kg}$ nước ở $30{,}0\ ^\circ\text{C}$. "
    r"Nhiệt dung của nhiệt lượng kế không đáng kể. Nhiệt dung riêng của nước là $4200\ \text{J/(kg·K)}$, "
    r"nhiệt nóng chảy riêng của nước đá là $\lambda=3{,}34\cdot10^{5}\ \text{J/kg}$. Nước đá nguyên chất, không lẫn nước lỏng; "
    r"áp suất khí quyển thường; bỏ qua nhiệt do khuấy và sự trao đổi nhiệt với môi trường.</p>"
    r"<ol type='a'><li>Nước đá có tan hết không?</li>"
    r"<li>Tìm nhiệt độ cuối của hệ và khối lượng nước đá còn lại (nếu có).</li></ol>"
)

B_ANALYSIS = [
    (r"\"$0{,}150$ kg nước đá ở $0\ ^\circ$C\"",
     r"$m_đ=0{,}150\ \text{kg}$ ; $t_đ=0\ ^\circ\text{C}$ (nguyên chất, không lẫn nước)",
     r"Đá đã ở nhiệt độ nóng chảy, chỉ có thể tan: $Q=\lambda m$ ; đá tan ở $0\ ^\circ\text{C}$ thì nhiệt độ không đổi"),
    (r"\"nhiệt lượng kế chứa $0{,}300$ kg nước ở $30{,}0\ ^\circ$C\"",
     r"$m_n=0{,}300\ \text{kg}$ ; $t_n=30{,}0\ ^\circ\text{C}$ ; $c_n=4200\ \text{J/(kg·K)}$",
     r"Nước nguội đi thì toả nhiệt: $Q=mc\,\Delta t$"),
    (r"\"Nhiệt dung của nhiệt lượng kế không đáng kể\"",
     "Nhiệt lượng kế không thu nhiệt",
     "⚠ Chỉ khi nhiệt dung của vỏ không đáng kể mới bỏ vỏ ra khỏi tính toán; nếu có, phải cộng vào phần nước nguội"),
    (r"\"áp suất khí quyển thường … bỏ qua trao đổi nhiệt với môi trường\"",
     "Hệ cô lập ; đá và nước ở áp suất thường",
     r"⚠ Mốc là nước lỏng ở $0\ ^\circ\text{C}$ (nước tinh khiết, áp suất thường) ; $c$ và $\lambda$ không đổi ; không có công khuấy đáng kể"),
    (r"\"Nước đá có tan hết không?\"",
     "Cần biết đá có tan hết hay không trước khi tìm nhiệt độ",
     "Nước nguội tối đa tới đâu thì còn nhiệt cho đá? Nhiệt đó so với nhiệt đá cần để tan hết thì sao?"),
    (r"\"nhiệt độ cuối … khối lượng nước đá còn lại\"",
     r"Cần tìm $t$ và $m_{còn}$",
     "Kết luận của câu a quyết định cách tính nhiệt độ cuối và khối lượng đá còn lại"),
]


def b_sol():
    return sol(
        [
            r"<strong>Khái niệm:</strong> nước nguội toả $Q=mc\,\Delta t$ ; đá tan ở $0\ ^\circ\text{C}$ thu $Q=\lambda m$ mà nhiệt độ không đổi.",
            r"<strong>Định luật:</strong> $Q_{toả}=Q_{thu}$ cho hệ cô lập, chỉ lập sau khi biết mỗi chất đang ở trạng thái nào.",
            r"<strong>Cách làm:</strong> lấy mốc $0\ ^\circ\text{C}$, so quỹ nhiệt $Q_0$ của nước (nguội về $0\ ^\circ\text{C}$) với nhiệt $\lambda m$ đá cần để tan hết.",
            r"⚠ <strong>Điều kiện:</strong> nhiệt dung nhiệt lượng kế không đáng kể ; bỏ qua môi trường ; áp suất thường, nước tinh khiết.",
        ],
        [
            ("Quỹ nhiệt của nước",
             [P(r"Nước nguội nhiều nhất tới $0\ ^\circ\text{C}$ thì toả được:"),
              M(r"Q_0=m_nc_n\,(30{,}0-0)=0{,}300\cdot4200\cdot30{,}0"),
              A(r"Q_0=37\,800\ \text{J}")]),
            ("Nhiệt để đá tan hết",
             [M(r"Q_{tan}=\lambda\,m_đ=3{,}34\cdot10^{5}\cdot0{,}150"),
              A(r"Q_{tan}=50\,100\ \text{J}")]),
            ("Đá có tan hết không",
             [P(r"Nước chỉ có $37\,800\ \text{J}$, đá cần $50\,100\ \text{J}$ để tan hết:"),
              M(r"Q_0\lt Q_{tan}"),
              A(r"T:Không tan hết: còn đá và nước cùng ở $0\ ^\circ\text{C}$, nên $t=0\ ^\circ\text{C}$."),
              P(r"Nếu cứ giả định tan hết rồi lập $Q_{toả}=Q_{thu}$, nghiệm ra khoảng $-6{,}5\ ^\circ\text{C}$: vô lí với nước lỏng, giả định sai.")]),
            ("Khối lượng đá đã tan",
             [P(r"Nước nguội về $0\ ^\circ\text{C}$ rồi thì hết nhiệt; toàn bộ $Q_0$ làm tan đá:"),
              M(r"m_{tan}=\dfrac{Q_0}{\lambda}=\dfrac{37\,800}{3{,}34\cdot10^{5}}"),
              A(r"m_{tan}\approx0{,}1132\ \text{kg}")]),
            ("Khối lượng đá còn lại",
             [M(r"m_{còn}=m_đ-m_{tan}=0{,}150-0{,}1132"),
              A(r"m_{còn}\approx0{,}0368\ \text{kg}\approx36{,}8\ \text{g}")]),
            ("Kiểm tra",
             [P(r"Đá tan cộng đá còn lại: $0{,}1132+0{,}0368=0{,}150\ \text{kg}$, đúng khối lượng đá ban đầu."),
              P(r"Còn $36{,}8\ \text{g}$ đá lẫn $0{,}300+0{,}1132=0{,}4132\ \text{kg}$ nước, cùng ở $0\ ^\circ\text{C}$: hợp lí với đá chưa tan hết.")]),
        ],
        [r"a) không tan hết ($Q_0=37\,800\ \text{J}\lt50\,100\ \text{J}$)",
         r"b) $t=0\ ^\circ\text{C}$ ; $m_{còn}\approx36{,}8\ \text{g}$ ($\approx0{,}0368\ \text{kg}$)"],
        r"Nhận dạng: đề <strong>thả nước đá vào nước ấm</strong> và hỏi <strong>nhiệt độ cuối</strong> → so quỹ nhiệt của nước với nhiệt đá cần để tan hết trước, rồi mới tính.",
    )


B_STEPS = dict(
    nhan_dang="Thấy <b>nước đá thả vào nước ấm, hỏi nhiệt độ cuối</b> → nghĩ tới <b>so nhiệt nước toả với nhiệt đá cần tan hết</b> trước",
    cap_do=3,
    fading="giau_tu_buoc_2",
    go_roi={"buoc_hay_sai": 2},
    buoc=[
        buoc("Quỹ nhiệt của nước",
             hoi="Nước nguội về 0 °C thì toả được nhiều nhất bao nhiêu nhiệt lượng?",
             dap_so=37800, don_vi="J", sai_so=200,
             loi="Dùng khối lượng nước đá thay cho khối lượng nước (nước mới là vật toả nhiệt)."),
        buoc("Nhiệt để đá tan hết",
             hoi="Muốn đá tan hết cần cung cấp bao nhiêu nhiệt lượng?",
             dap_so=50100, don_vi="J", sai_so=200,
             ke=[("Nhiệt nóng chảy riêng nhân khối lượng đá", True),
                 ("Khối lượng đá nhân nhiệt dung riêng và độ tăng nhiệt độ", "Đá ở 0 °C đang tan, nhiệt độ không tăng; nhiệt dùng để phá liên kết, không làm nóng."),
                 ("Nhiệt nóng chảy riêng nhân khối lượng nước", "λ ứng với khối lượng chất chuyển thể, tức khối lượng đá, không phải khối lượng nước.")],
             loi="Lấy mcΔt cho đá thay vì λm: đá ở 0 °C chưa nóng lên mà đang chuyển thể."),
        buoc("Đá có tan hết không",
             hoi="Đá có tan hết không, và nhiệt độ cuối của hệ là bao nhiêu?",
             lua_chon=[("Không tan hết; hệ gồm đá và nước ở $0\\ ^\\circ\\text{C}$", True),
                       ("Tan hết; lập $Q_{toả}=Q_{thu}$ cho cả hệ để tìm $t$",
                        "Chưa kiểm tra đá có tan hết không. Giải theo giả thiết đó cho nhiệt độ dưới 0 °C, vô lí với nước lỏng, nên giả thiết sai."),
                       ("Không tan hết; nhiệt độ cuối nằm giữa $0$ và $30\\ ^\\circ\\text{C}$",
                        "Còn đá thì nước và đá phải cùng ở 0 °C; nước không thể ấm hơn đá khi đá còn đang tan.")],
             ke=[("So nhiệt nước toả tối đa với nhiệt đá cần để tan hết", True),
                 ("So khối lượng nước với khối lượng đá", "Khối lượng chưa quyết định: nhiệt dung riêng và nhiệt nóng chảy riêng khác nhau, phải so nhiệt lượng."),
                 ("Lập ngay Q_toả = Q_thu với nhiệt độ cuối chưa biết", "Phương trình đó chỉ đúng khi đá tan hết; chưa kiểm tra thì có thể ra nghiệm vô lí.")],
             loi="Lập ngay Q_toả = Q_thu cho cả hệ rồi giải tìm t, không so nhiệt của nước với nhiệt đá cần để tan hết."),
        buoc("Khối lượng đá đã tan",
             hoi="Toàn bộ nhiệt của nước làm tan bao nhiêu kg đá?",
             dap_so=0.113, don_vi="kg", sai_so=0.002,
             ke=[("Chia nhiệt nước toả cho nhiệt nóng chảy riêng", True),
                 ("Chia nhiệt nước toả cho nhiệt dung riêng và độ giảm nhiệt độ của nước", "Cách chia đó cho khối lượng nước, không phải khối lượng đá tan."),
                 ("Chia nhiệt đá cần để tan hết cho nhiệt nóng chảy riêng", "Cách chia đó cho đúng khối lượng đá ban đầu, nhưng nước chỉ cung cấp phần nhiệt của mình.")],
             loi="Chia nhiệt cho c thay vì λ: đá tan là chuyển thể, không phải tăng nhiệt độ."),
        buoc("Khối lượng đá còn lại",
             hoi="Khối lượng nước đá còn lại là bao nhiêu gam?",
             dap_so=36.8, don_vi="g", sai_so=1,
             ke=[("Khối lượng đá ban đầu trừ khối lượng đá đã tan", True),
                 ("Khối lượng đá đã tan", "Đó là phần đã tan, đề hỏi phần còn lại."),
                 ("Khối lượng nước ban đầu trừ khối lượng đá đã tan", "Nước là chất lỏng trong bình, không phải đá còn lại.")],
             loi="Lấy phần đã tan làm đáp số, hoặc quên đổi kg sang g."),
        buoc("Kiểm tra"),
    ],
)

B_TOM_DE = {
    "cho": [
        r"Nước đá $0{,}150\ \text{kg}$ ở $0\ ^\circ\text{C}$ thả vào $0{,}300\ \text{kg}$ nước $30{,}0\ ^\circ\text{C}$",
        r"Nhiệt lượng kế không đáng kể ; $c_{nước}=4200\ \text{J/(kg·K)}$ ; $\lambda=3{,}34\cdot10^{5}\ \text{J/kg}$",
    ],
    "tim": ["a) đá có tan hết không", "b) nhiệt độ cuối và khối lượng đá còn lại"],
}

B_CONG_CU = {
    "loai": "thanh_nang_luong", "de": True,
    "canh": {"kieu": "hop_he", "ten": "nước ấm"},
    "cot": [{"ten": "Q_toả", "mau": "max"}, {"ten": "Q_cần", "mau": "min"}],
    "max": 55000, "don_vi": "J",
    "hinh": [
        {"loai": "mui", "vao": True, "nhan": "0°C", "hang": 0},
        {"loai": "mui", "vao": False, "nhan": "30°C", "hang": 0},
    ],
    "lop": [
        [{"loai": "cot", "ten": "Q_toả", "gia_tri": 37800, "nhan": "37800"},
         {"loai": "ghi", "text": "Q₀ = 0,3·4200·30 = 37800 J"}],
        [{"loai": "cot", "ten": "Q_cần", "gia_tri": 50100, "nhan": "50100"},
         {"loai": "ghi", "text": "Q_tan = 3,34·10⁵·0,15 = 50100 J"}],
        [{"loai": "ghi", "text": "Q₀ < Q_tan: còn đá, t = 0 °C"}],
        [{"loai": "ghi", "text": "m_tan = 37800 : 3,34·10⁵ ≈ 0,1132 kg"}],
        [{"loai": "ghi", "text": "m_còn = 0,150 − 0,1132 ≈ 36,8 g"}],
        [{"loai": "ghi", "text": "Kiểm: 113,2 + 36,8 = 150 g ✓"}],
    ],
}

B_NOI = (
    r"<p>Ở dạng này: quỹ của nước là $Q_0=0{,}300\cdot4200\cdot30{,}0=37\,800\ \text{J}$, còn đá cần $\lambda m=50\,100\ \text{J}$ để tan hết. "
    r"Quỹ cạn trước khi đá tan hết, nên còn đá và hệ dừng ở $0\ ^\circ\text{C}$. Đá ở $0\ ^\circ\text{C}$ nên không rút thêm nấc làm nóng; "
    r"số nhiệt đã tiêu chia cho $\lambda$ cho biết đá đã tan bao nhiêu.</p>"
)


def co_chu(cc, ten):
    """Cỡ chữ px ở 375 px (1 đơn vị ≈ 15,9 px), công thức ThanhNangLuong.tsx; assert ≥ 13 px."""
    U = 15.9
    ds = lambda t: len(re.sub(r"_\{([^}]*)\}", r"\1", t).replace("_", ""))
    out = []
    items = list(cc["hinh"]) + [it for l in cc["lop"] for it in l]
    for it in items:
        if it["loai"] == "mui":
            out.append(("mui " + it["nhan"], min(1.05, 2.9 / (ds(it["nhan"]) * 0.6)) * U))
        elif it["loai"] == "cot":
            out.append(("cot " + it["nhan"], min(0.95, 3.0 / (ds(it["nhan"]) * 0.6)) * U))
        elif it["loai"] == "ghi":
            W = 14.2 + 2.5 * len(cc["cot"]) + 0.2
            out.append(("ghi " + it["text"], min(1.05, (W - 0.2) / (ds(it["text"]) * 0.6)) * U))
    out.append(("ten cột", 1.05 * U))
    m = min(out, key=lambda x: x[1])
    print(" ", ten, "cỡ chữ nhỏ nhất", round(m[1], 1), "px:", m[0])
    assert m[1] >= 13, m


def main():
    co_chu(A_CONG_CU, "Dạng 3"); co_chu(B_CONG_CU, "Dạng 4")
    old = json.load(open(OLD))
    qs = old["questions"]
    assert len(qs) == 4, "old/5.json phải có đúng 4 dạng chuẩn"
    keep = []
    for q in qs:
        q = copy.deepcopy(q)
        q.pop("topic_id", None)   # do script đăng sinh
        q.pop("body_html", None)  # do script đăng sinh (composeBody)
        keep.append(q)

    def mk(label, topic, problem, analysis, solution, steps, tom_de, cong_cu, meo):
        analysis = [tuple(c.replace('\\"', '"') for c in row) for row in analysis]
        d = dict(form="bai_tap", label=label, topic=topic, problem_html=problem,
                 analysis_html=tbl(analysis), solution_html=solution, tom_de=tom_de, cong_cu=cong_cu, meo=meo)
        d.update(copy.deepcopy(steps))
        assert len(d["buoc"]) == len(cong_cu["lop"])
        return d

    dA = mk("Dạng 3 · Trung bình · Đo nhiệt dung riêng kim loại bằng cách trộn: gộp nước với vỏ nhiệt lượng kế",
            TOPIC_A, A_PROBLEM, A_ANALYSIS, a_sol(), A_STEPS, A_TOM_DE, A_CONG_CU, don_bay_nhiet(A_NOI))
    dB = mk("Dạng 4 · Khó · Thả đá vào nước ấm: đá có tan hết không, còn lại bao nhiêu",
            TOPIC_B, B_PROBLEM, B_ANALYSIS, b_sol(), B_STEPS, B_TOM_DE, B_CONG_CU, quy_nhiet(B_NOI))

    dang = [keep[0], keep[1], dA, dB, keep[2], keep[3]]
    for i, d in enumerate(dang, 1):
        d["label"] = re.sub(r"^Dạng \d+", f"Dạng {i}", d["label"])
    out = {
        "lesson_id": 5,
        "lesson_title": "Bài 4. Thực hành đo nhiệt dung riêng, nhiệt nóng chảy riêng, nhiệt hoá hơi riêng",
        "generated_at": "2026-11-17",
        "review": {"checked": True, "notes": "kiem-code 17/11/2026: Dạng 3, 4 mới tự giải độc lập khớp đáp số, sai_so tách các cách sai, không lộ đáp số — ĐẠT; Dạng 1, 2, 5, 6 giữ nguyên bản đã đăng (kiểm chéo trước đó)"},
        "dang_bai": dang,
    }
    json.dump(out, open(OUT, "w"), ensure_ascii=False, indent=1)
    print("ghi", OUT, len(dang), "dạng")
    for d in dang:
        print(" ", d["label"][:70], "| cap", d["cap_do"], d["fading"], "| buoc", len(d["buoc"]))


if __name__ == "__main__":
    main()
