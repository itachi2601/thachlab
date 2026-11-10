"""Bài tập mẫu Bài 24 "Nguồn điện" (Vật lí 11) — lesson_id 43. 4 dạng, hình: hinh_43.py. Mục bài tập mẫu cũ rỗng, viết mới.
Quét dạng (từ lý thuyết bài lt-43 + 90 câu bai_tap ngân hàng topic 191/192: A=ℰq, đọc số chỉ vôn kế, hai lần đo → ℰ, r, ghép nguồn, I = ℰ/(R+r)):
 1 Dễ (cấp 1)         · suất điện động ℰ = A/q: điện tích, thời gian, công khi đổi nguồn          · topic 191
 2 Trung bình (cấp 2) · hở mạch U = ℰ, có dòng U \lt ℰ: tìm ℰ, I, r, dòng đoản mạch              · topic 191
 3 Khó (cấp 3)        · hai lần đo (R, U): tìm I mỗi lần, r (trừ vế), ℰ, dòng đoản mạch          · topic 191
 4 Khó (cấp 4)        · bộ nguồn hỗn hợp đối xứng: ℰ_b, r_b, I, U hai cực, dòng qua mỗi pin        · topic 192
Chỉ dùng kiến thức trong bài: ℰ = A/q, q = It, U = ℰ − Ir, I = ℰ/(R+r), I_đm = ℰ/r, ghép nối tiếp/song song/hỗn hợp. KHÔNG dùng công suất/hiệu suất (bài không có).
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-43.py   (idempotent, ghi 43.json với review.checked=false)"""
import json, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from hinh_43 import *

J = os.path.join(HERE, "43.json")
ROOT = os.path.abspath(os.path.join(HERE, "../../.."))
TOPICS = {t["id"]: t["name"] for t in json.load(open(os.path.join(ROOT, "scripts/data/question-topics.json"))) if t["lesson_id"] == 43}
T191, T192 = TOPICS[191], TOPICS[192]
assert T191 == "Suất điện động và điện trở trong của nguồn" and T192 == "Định luật Ohm cho toàn mạch"


def near(x, y, tol): return abs(x - y) <= tol


# ═════════════ SỐ LIỆU + TỰ GIẢI ĐỘC LẬP (assert) ═════════════
# Dạng 1: ℰ = 12 V, I = 0,50 A, A = 1,8 kJ
Em1, I1, Ac1, E1b = 12.0, 0.50, 1.8e3, 1.5
q1 = Ac1 / Em1; t1 = q1 / I1; A1b = E1b * q1
assert near(q1, 150, 1e-9) and near(t1, 300, 1e-9) and near(A1b, 225, 1e-9) and near(Ac1 / E1b / q1, 8, 1e-9)
assert Em1 * Ac1 != q1 and Ac1 / I1 != t1 and near(Ac1 / I1, 3600, 1e-9)                   # sai: q = ℰ·A ; t = A/I
assert near(Ac1 / E1b, 1200, 1e-9) and 1200 != A1b and Ac1 != A1b and near(q1 / E1b, 100, 1e-9) and 100 != A1b   # sai: A' = A/ℰ' ; giữ A ; q/ℰ'
# Dạng 2: hở mạch 9,0 V; R = 30 Ω; vôn kế 7,5 V
Eo2, R2, U2 = 9.0, 30.0, 7.5
I2 = U2 / R2; r2 = (Eo2 - U2) / I2; Idm2 = Eo2 / r2
assert near(I2, 0.25, 1e-12) and near(r2, 6.0, 1e-12) and near(Idm2, 1.5, 1e-12)
assert near(Eo2 / (R2 + r2), I2, 1e-12)                                                    # kiểm: Ohm toàn mạch
assert near(Eo2 / R2, 0.30, 1e-12) and 0.30 != I2                                          # sai: I = ℰ/R (bỏ r)
assert near(U2 / I2, 30.0, 1e-12) and 30.0 != r2 and near(Eo2 / I2, 36.0, 1e-12) and 36.0 != r2 and near(Eo2 - U2, 1.5, 1e-12)   # sai: r = U/I ; ℰ/I ; chỉ ℰ − U
assert 1.5 == Idm2 and near(U2 / r2, 1.25, 1e-12) and 1.25 != Idm2                         # sai: I_đm = U/r (dù trùng 1,5 ở Ir = 1,5 V, khác đại lượng)
# Dạng 3: R1 = 3,0 Ω, U1 = 3,6 V; R2 = 10 Ω, U2 = 5,0 V — hệ phương trình độc lập (numpy-free, Cramer)
R31, U31, R32, U32 = 3.0, 3.6, 10.0, 5.0
I31, I32 = U31 / R31, U32 / R32
# ℰ − I1 r = U1 ; ℰ − I2 r = U2
det = (1) * (-I32) - (1) * (-I31)
E3 = (U31 * (-I32) - U32 * (-I31)) / det
r3 = (1 * U32 - 1 * U31) / det
assert near(I31, 1.2, 1e-12) and near(I32, 0.5, 1e-12) and near(r3, 2.0, 1e-9) and near(E3, 6.0, 1e-9)
Idm3 = E3 / r3
assert near(Idm3, 3.0, 1e-9)
assert near(E3 - I32 * r3, U32, 1e-9) and near(E3 / (R31 + r3), I31, 1e-9) and near(E3 / (R32 + r3), I32, 1e-9)   # kiểm hai lần đo
assert near((U32 - U31) / (I31 + I32), 1.4 / 1.7, 1e-12) and (U32 - U31) / (I31 + I32) != r3                        # sai: chia cho tổng hai dòng
assert near(U31 + U32, 8.6, 1e-12) and 8.6 != E3 and U32 != E3 and U31 != E3 and near(U31 / R32, 0.36, 1e-12) and 0.36 != I31   # sai: ℰ = U1+U2 ; ℰ = U ; I = U1/R2
assert near(E3 / R31, 2.0, 1e-12) and 2.0 != Idm3 and near(U32 / r3, 2.5, 1e-12) and 2.5 != Idm3                  # sai: I_đm = ℰ/R1 ; U/r
# Dạng 4: 8 pin, ℰ0 = 1,5 V, r0 = 0,50 Ω, n = 2 dãy, m = 4 pin/dãy, R = 3,0 Ω
E0, r0, n4, m4, R4 = 1.5, 0.5, 2, 4, 3.0
Eb4 = m4 * E0; rb4 = m4 * r0 / n4; I4 = Eb4 / (R4 + rb4); U4 = I4 * R4; Ipin4 = I4 / n4
assert near(Eb4, 6.0, 1e-12) and near(rb4, 1.0, 1e-12) and near(I4, 1.5, 1e-12) and near(U4, 4.5, 1e-12) and near(Ipin4, 0.75, 1e-12)
assert near(Eb4 - I4 * rb4, U4, 1e-12) and near(m4 * E0 - Ipin4 * m4 * r0, U4, 1e-12)  # kiểm chéo qua một dãy
# tích phân số độc lập: giải hệ Kirchhoff hai dãy giống nhau (ẩn I1, I2 qua mỗi dãy): ℰ_dãy − I_k·(m r0) = U ; I1 + I2 = I ; U = I R
import itertools
Ed, rd = m4 * E0, m4 * r0
Ik = (Ed - U4) / rd
assert near(Ik, Ipin4, 1e-12) and near(n4 * Ik * R4, U4, 1e-12)
# sai: r_b = m·n·r0 ; r_b = r0/(m·n) ; ℰ_b = 8 ℰ0 ; I = ℰ0/(R + r0) ; I = ℰ_b/R ; U = ℰ_b ; U = I r_b ; dòng pin = I ; I/8 ; hoán đổi m ↔ n
assert near(m4 * n4 * r0, 4.0, 1e-12) and 4.0 != rb4 and near(r0 / (m4 * n4), 0.0625, 1e-12) and near(m4 * n4 * E0, 12.0, 1e-12) and 12.0 != Eb4
assert near(E0 / (R4 + r0), 1.5 / 3.5, 1e-12) and 1.5 / 3.5 != I4 and near(Eb4 / R4, 2.0, 1e-12) and 2.0 != I4
assert Eb4 != U4 and near(I4 * rb4, 1.5, 1e-12) and 1.5 != U4 and I4 != Ipin4 and near(I4 / (m4 * n4), 0.1875, 1e-12) and 0.1875 != Ipin4
Eb_sw, rb_sw = n4 * E0, n4 * r0 / m4                                                       # hoán đổi n ↔ m
assert near(Eb_sw, 3.0, 1e-12) and near(rb_sw, 0.25, 1e-12) and (Eb_sw != Eb4) and (rb_sw != rb4)
# Số liệu của hình mô phỏng khác số liệu của đề (không lộ đáp số)
assert (4.5, 12.0, 3.0) != (Eo2, R2, r2) and near(4.5 / (12 + 3.0), 0.30, 1e-12) and near(4.5 - 0.30 * 3.0, 3.6, 1e-12) and 0.30 != I2
assert near(1.2 / 0.3, 4.0, 1e-12) and 4.0 != Idm3 and (1.2, 0.3) != (E3, r3)                           # đồ thị mẫu
assert (2 * 1.5, 2 * 0.5 / 3) != (Eb4, rb4)                                                   # bộ mẫu 3 dãy × 2 pin

# ═════════════ ĐỀ ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Suất điện động: công của lực lạ, điện tích dịch chuyển và thời gian", topic=T191,
      problem_html=r"""<p>Một ắc quy có suất điện động $\mathcal{E}=12\ \text{V}$ cấp điện cho một mạch kín. Trong thời gian dòng điện không đổi $I=0{,}50\ \text{A}$ chạy qua nguồn, lực lạ bên trong ắc quy thực hiện công $A=1{,}8\cdot10^{3}\ \text{J}$ để đưa điện tích dương từ cực âm sang cực dương.</p><ol type="a"><li>Tính điện tích đã dịch chuyển qua nguồn.</li><li>Tính khoảng thời gian dòng điện chạy.</li><li>Một pin $1{,}5\ \text{V}$ muốn đưa cùng lượng điện tích đó qua nguồn thì lực lạ trong pin phải thực hiện công bao nhiêu?</li></ol>"""),
 dict(label="Dạng 2 · Trung bình · Hai số chỉ của vôn kế: suất điện động, dòng điện, điện trở trong và dòng khi nối tắt", topic=T191,
      problem_html=r"""<p>Một pin đã dùng lâu. Vôn kế lí tưởng mắc ở hai cực pin chỉ $9{,}0\ \text{V}$ khi mạch hở. Nối hai cực pin với điện trở $R=30\ \Omega$ (bỏ qua điện trở dây nối), vôn kế vẫn mắc ở hai cực pin chỉ $7{,}5\ \text{V}$.</p><ol type="a"><li>Suất điện động của pin bằng bao nhiêu?</li><li>Tính cường độ dòng điện trong mạch kín.</li><li>Tính điện trở trong của pin.</li><li>Nối tắt hai cực pin bằng dây dẫn có điện trở không đáng kể thì dòng điện chạy qua pin bằng bao nhiêu?</li></ol>"""),
 dict(label="Dạng 3 · Khó · Hai lần đo cùng một nguồn: lập hệ để tìm điện trở trong và suất điện động", topic=T191,
      problem_html=r"""<p>Để xác định suất điện động $\mathcal{E}$ và điện trở trong $r$ của một nguồn, người ta nối nguồn lần lượt với hai điện trở $R_1=3{,}0\ \Omega$ và $R_2=10\ \Omega$ (bỏ qua điện trở dây nối). Vôn kế lí tưởng mắc ở hai cực nguồn chỉ $U_1=3{,}6\ \text{V}$ và $U_2=5{,}0\ \text{V}$ tương ứng.</p><ol type="a"><li>Tính cường độ dòng điện trong mỗi lần đo.</li><li>Tính điện trở trong $r$ và suất điện động $\mathcal{E}$ của nguồn.</li><li>Nối tắt hai cực nguồn thì dòng điện bằng bao nhiêu?</li></ol>"""),
 dict(label="Dạng 4 · Khó · Bộ nguồn hỗn hợp đối xứng: suất điện động, điện trở trong, dòng điện và dòng qua mỗi pin", topic=T192,
      problem_html=r"""<p>Một đèn pin dùng bộ nguồn gồm $8$ pin giống nhau, mỗi pin có suất điện động $\mathcal{E}_0=1{,}5\ \text{V}$ và điện trở trong $r_0=0{,}50\ \Omega$, ghép thành $2$ dãy song song, mỗi dãy có $4$ pin nối tiếp. Bóng đèn coi như điện trở $R=3{,}0\ \Omega$ nối vào hai cực của bộ nguồn; bỏ qua điện trở dây nối.</p><ol type="a"><li>Tính suất điện động và điện trở trong của bộ nguồn.</li><li>Tính cường độ dòng điện qua bóng đèn.</li><li>Tính hiệu điện thế giữa hai cực của bộ nguồn.</li><li>Tính cường độ dòng điện qua mỗi pin.</li></ol>"""),
]

# ═════════════ PHÂN TÍCH ĐỀ (cột 3: khái niệm / điều kiện chung / câu hỏi gợi; không số đáp án, không kết luận bước bị giấu) ═════════════
ANALYSIS = [
 [(r'"ắc quy có suất điện động $\mathcal{E}=12$ V"', r"$\mathcal{E}=12$ V", r"Suất điện động: công của lực lạ trên mỗi coulomb điện tích dương đi qua nguồn"),
  (r'"dòng điện không đổi $I=0{,}50$ A"', r"$I=0{,}50$ A", r"Liên hệ giữa điện tích, cường độ dòng điện và thời gian"),
  (r'"lực lạ … thực hiện công $A=1{,}8\cdot10^{3}$ J … từ cực âm sang cực dương"', r"$A=1{,}8\cdot10^{3}$ J", r"⚠ $A$ là công của lực lạ trong nguồn, không phải công của lực điện ở mạch ngoài"),
  (r'"điện tích đã dịch chuyển qua nguồn"', r"Cần $q$", r"Đại lượng cần tìm: liên hệ $\mathcal{E}$, $A$, $q$"),
  (r'"khoảng thời gian dòng điện chạy"', r"Cần $t$", r"Đại lượng cần tìm"),
  (r'"pin $1{,}5$ V … cùng lượng điện tích đó"', r"$\mathcal{E}'=1{,}5$ V; cùng $q$", r"Cùng điện tích mà suất điện động khác thì công của lực lạ có khác không? Cần $A'$")],
 [(r'"vôn kế lí tưởng mắc ở hai cực pin"', "Vôn kế lí tưởng", r"⚠ Vôn kế lí tưởng không lấy dòng; số chỉ là hiệu điện thế giữa hai cực pin"),
  (r'"khi mạch hở, vôn kế chỉ $9{,}0$ V"', r"$U_{\text{hở}}=9{,}0$ V", r"Khi hở mạch, cường độ dòng điện và độ giảm thế trong nguồn là bao nhiêu?"),
  (r'"nối hai cực pin với điện trở $R=30\ \Omega$ … vôn kế chỉ $7{,}5$ V"', r"$R=30\ \Omega$; $U=7{,}5$ V", r"Hai cực pin nối thẳng với $R$: hiệu điện thế giữa hai đầu $R$ là số nào?"),
  (r'"bỏ qua điện trở dây nối"', "Mạch ngoài chỉ có $R$", r"⚠ Mọi điện trở ngoài đã nằm trong $R$"),
  (r'"suất điện động của pin"', r"Cần $\mathcal{E}$", r"Đại lượng cần tìm: số chỉ nào ứng với $I=0$?"),
  (r'"cường độ dòng điện trong mạch kín"', r"Cần $I$", r"Đại lượng cần tìm: định luật Ohm cho điện trở $R$"),
  (r'"điện trở trong của pin"', r"Cần $r$", r"Đại lượng cần tìm: liên hệ $\mathcal{E}$, $U$, $I$, $r$"),
  (r'"nối tắt hai cực pin"', r"Dây nối tắt có điện trở không đáng kể", r"Khi nối tắt, mạch ngoài còn lại điện trở nào?")],
 [(r'"lần lượt hai điện trở $R_1=3{,}0\ \Omega$ và $R_2=10\ \Omega$"', r"$R_1=3{,}0\ \Omega$; $R_2=10\ \Omega$", r"Hai lần đo trên cùng một nguồn: $\mathcal{E}$ và $r$ không đổi"),
  (r'"vôn kế lí tưởng mắc ở hai cực nguồn chỉ $U_1=3{,}6$ V và $U_2=5{,}0$ V"', r"$U_1=3{,}6$ V; $U_2=5{,}0$ V", r"⚠ Vôn kế đo lúc có dòng: số chỉ là hiệu điện thế hai cực, chưa phải suất điện động"),
  (r'"bỏ qua điện trở dây nối"', r"$R$ là toàn bộ mạch ngoài", r"⚠ Hiệu điện thế hai cực chính là hiệu điện thế hai đầu $R$"),
  (r'"cường độ dòng điện trong mỗi lần đo"', r"Cần $I_1$, $I_2$", r"Đại lượng cần tìm: dùng $R$ và hiệu điện thế hai đầu $R$"),
  (r'"điện trở trong $r$ và suất điện động $\mathcal{E}$"', r"Cần $r$, $\mathcal{E}$", r"Đại lượng cần tìm: hai ẩn thì cần mấy phương trình? Có thể khử ẩn nào?"),
  (r'"nối tắt hai cực nguồn"', "Mạch ngoài không đáng kể", r"Khi nối tắt, dòng điện bị giới hạn bởi điện trở nào?")],
 [(r'"$8$ pin giống nhau, mỗi pin $\mathcal{E}_0=1{,}5$ V, $r_0=0{,}50\ \Omega$"', r"$\mathcal{E}_0=1{,}5$ V; $r_0=0{,}50\ \Omega$", r"⚠ Pin giống nhau nên các dãy giống nhau và chia đều dòng"),
  (r'"ghép thành $2$ dãy song song, mỗi dãy có $4$ pin nối tiếp"', r"$n=2$ dãy; $m=4$ pin mỗi dãy", r"Pin cùng dãy ghép kiểu gì, các dãy ghép với nhau kiểu gì?"),
  (r'"bóng đèn coi như điện trở $R=3{,}0\ \Omega$ nối vào hai cực của bộ nguồn"', r"$R=3{,}0\ \Omega$", r"⚠ $R$ nối vào hai cực của cả bộ nguồn"),
  (r'"bỏ qua điện trở dây nối"', "Mạch ngoài chỉ có $R$", r"⚠ Mọi điện trở ngoài đã nằm trong $R$"),
  (r'"suất điện động và điện trở trong của bộ nguồn"', r"Cần $\mathcal{E}_b$, $r_b$", r"Đại lượng cần tìm"),
  (r'"cường độ dòng điện qua bóng đèn"', r"Cần $I$", r"Đại lượng cần tìm"),
  (r'"hiệu điện thế giữa hai cực của bộ nguồn"', r"Cần $U$", r"Đại lượng cần tìm"),
  (r'"cường độ dòng điện qua mỗi pin"', r"Cần dòng qua một pin", r"Đại lượng cần tìm: dòng chính chia cho các dãy thế nào?")],
]

# ═════════════ LỜI GIẢI ═════════════
R1 = [r"<strong>Khái niệm:</strong> lực lạ đưa điện tích dương từ cực (−) sang cực (+) trong nguồn.",
      r"Suất điện động: $\mathcal{E}=\dfrac{A}{q}$ ($A$: công của lực lạ, $q$: điện tích dịch chuyển trong nguồn)",
      r"Điện tích qua một tiết diện: $q=It$",
      r"⚠ <strong>Điều kiện:</strong> $A$ là công của lực lạ trong nguồn; công của lực điện ở mạch ngoài là $Uq$, nhỏ hơn $\mathcal{E}q$ khi có dòng."]
R2 = [r"<strong>Khái niệm:</strong> hở mạch ($I=0$) thì không có độ giảm thế trong nguồn; có dòng thì $U$ nhỏ hơn $\mathcal{E}$.",
      r"Hiệu điện thế hai cực: $U=\mathcal{E}-Ir$ · định luật Ohm cho điện trở ngoài: $I=\dfrac{U}{R}$",
      r"Nối tắt ($R\to0$): $I_{\text{đm}}=\dfrac{\mathcal{E}}{r}$",
      r"⚠ <strong>Điều kiện:</strong> vôn kế lí tưởng; bỏ qua điện trở dây nối nên $R$ là toàn bộ mạch ngoài."]
R3 = [r"<strong>Khái niệm:</strong> cùng một nguồn nên $\mathcal{E}$ và $r$ không đổi; đổi $R$ thì $I$ và $U$ đổi.",
      r"Mỗi lần đo: $I=\dfrac{U}{R}$ và $U=\mathcal{E}-Ir$",
      r"Hai ẩn $\mathcal{E}$, $r$ cần hai phương trình; trừ vế để khử $\mathcal{E}$.",
      r"Nối tắt: $I_{\text{đm}}=\dfrac{\mathcal{E}}{r}$",
      r"⚠ <strong>Điều kiện:</strong> vôn kế lí tưởng, đo lúc có dòng nên cả hai số chỉ đều nhỏ hơn $\mathcal{E}$."]
R4 = [r"<strong>Khái niệm:</strong> pin cùng dãy nối tiếp: cộng $\mathcal{E}$, cộng $r$. Các dãy giống nhau song song: giữ $\mathcal{E}$, chia $r$.",
      r"Bộ hỗn hợp đối xứng ($n$ dãy, mỗi dãy $m$ pin): $\mathcal{E}_b=m\mathcal{E}_0$ · $r_b=\dfrac{mr_0}{n}$",
      r"Toàn mạch: $I=\dfrac{\mathcal{E}_b}{R+r_b}$ · $U=IR$",
      r"⚠ <strong>Điều kiện:</strong> pin giống nhau nên các dãy chia đều dòng; bỏ qua điện trở dây nối."]

SOLS = [
 sol(R1, [
  ("Điện tích dịch chuyển qua nguồn", [P(r"Từ định nghĩa suất điện động, suy ra $q$:"), M(r"q=\dfrac{A}{\mathcal{E}}=\dfrac{1{,}8\cdot10^{3}}{12}"), A(r"q=150\ \text{C}")]),
  ("Khoảng thời gian", [P(r"Từ $q=It$:"), M(r"t=\dfrac{q}{I}=\dfrac{150}{0{,}50}"), A(r"t=300\ \text{s}=5{,}0\ \text{phút}")]),
  ("Công của lực lạ trong pin $1{,}5\\ \\text{V}$", [P(r"Cùng điện tích $q=150\ \text{C}$, suất điện động $\mathcal{E}'=1{,}5\ \text{V}$:"), M(r"A'=\mathcal{E}'q=1{,}5\cdot150"), A(r"A'=225\ \text{J}")]),
  ("Kiểm tra", [P(r"Đơn vị: $\text{J}/\text{C}=\text{V}$ ✓"), P(r"$\mathcal{E}$ giảm $\dfrac{12}{1{,}5}=8$ lần nên công giảm 8 lần: $\dfrac{1{,}8\cdot10^{3}}{8}=225\ \text{J}$ ✓")])],
  [r"a) $q=150\ \text{C}$", r"b) $t=300\ \text{s}$", r"c) $A'=225\ \text{J}$"],
  r"Nhận dạng: đề cho <strong>công của lực lạ</strong> hoặc hỏi công lực lạ khi đưa điện tích qua nguồn → dùng $\mathcal{E}=\dfrac{A}{q}$."),
 sol(R2, [
  ("Suất điện động", [P(r"Khi hở mạch $I=0$ nên $Ir=0$:"), M(r"U=\mathcal{E}-Ir=\mathcal{E}"), A(r"\mathcal{E}=9{,}0\ \text{V}"), P(r"Số chỉ $7{,}5\ \text{V}$ đo lúc có dòng nên nhỏ hơn $\mathcal{E}$.")]),
  ("Cường độ dòng điện", [P(r"Hai cực pin nối thẳng với $R$ nên hiệu điện thế hai đầu $R$ bằng số chỉ vôn kế lúc có dòng:"), M(r"I=\dfrac{U}{R}=\dfrac{7{,}5}{30}"), A(r"I=0{,}25\ \text{A}")]),
  ("Điện trở trong", [P(r"Độ giảm thế trong nguồn:"), M(r"Ir=\mathcal{E}-U=9{,}0-7{,}5=1{,}5\ \text{V}"), M(r"r=\dfrac{\mathcal{E}-U}{I}=\dfrac{1{,}5}{0{,}25}"), A(r"r=6{,}0\ \Omega")]),
  ("Dòng điện khi nối tắt", [P(r"Nối tắt: $R\to0$, chỉ còn $r$ giữ dòng:"), M(r"I_{\text{đm}}=\dfrac{\mathcal{E}}{r}=\dfrac{9{,}0}{6{,}0}"), A(r"I_{\text{đm}}=1{,}5\ \text{A}")]),
  ("Kiểm tra", [P(r"Toàn mạch: $I=\dfrac{\mathcal{E}}{R+r}=\dfrac{9{,}0}{30+6{,}0}=0{,}25\ \text{A}$ ✓"), P(r"Dòng nối tắt gấp $\dfrac{1{,}5}{0{,}25}=6$ lần dòng khi có $R$, bằng $\dfrac{R+r}{r}=\dfrac{36}{6}$ ✓")])],
  [r"a) $\mathcal{E}=9{,}0\ \text{V}$", r"b) $I=0{,}25\ \text{A}$", r"c) $r=6{,}0\ \Omega$", r"d) $I_{\text{đm}}=1{,}5\ \text{A}$"],
  r"Nhận dạng: đề cho <strong>số chỉ vôn kế khi hở mạch và khi nối $R$</strong> → hở mạch cho $\mathcal{E}$, hiệu hai số chỉ chia cho $I$ cho $r$."),
 sol(R3, [
  ("Dòng trong hai lần đo", [P(r"Hiệu điện thế hai cực chính là hiệu điện thế hai đầu $R$:"), M(r"I_1=\dfrac{U_1}{R_1}=\dfrac{3{,}6}{3{,}0}=1{,}2\ \text{A}"), M(r"I_2=\dfrac{U_2}{R_2}=\dfrac{5{,}0}{10}=0{,}50\ \text{A}"), A(r"I_1=1{,}2\ \text{A};\ I_2=0{,}50\ \text{A}")]),
  ("Điện trở trong", [P(r"Mỗi lần đo có $U=\mathcal{E}-Ir$:"), M(r"3{,}6=\mathcal{E}-1{,}2\,r"), M(r"5{,}0=\mathcal{E}-0{,}50\,r"), P(r"Trừ vế theo vế để khử $\mathcal{E}$:"), M(r"5{,}0-3{,}6=(1{,}2-0{,}50)\,r"), M(r"r=\dfrac{1{,}4}{0{,}70}"), A(r"r=2{,}0\ \Omega")]),
  ("Suất điện động", [P(r"Thế $r$ vào phương trình của lần đo thứ nhất:"), M(r"\mathcal{E}=U_1+I_1r=3{,}6+1{,}2\cdot2{,}0"), A(r"\mathcal{E}=6{,}0\ \text{V}")]),
  ("Dòng điện khi nối tắt", [M(r"I_{\text{đm}}=\dfrac{\mathcal{E}}{r}=\dfrac{6{,}0}{2{,}0}"), A(r"I_{\text{đm}}=3{,}0\ \text{A}")]),
  ("Kiểm tra", [P(r"Lần 2: $\mathcal{E}-I_2r=6{,}0-0{,}50\cdot2{,}0=5{,}0\ \text{V}=U_2$ ✓"), P(r"Toàn mạch lần 1: $I_1=\dfrac{\mathcal{E}}{R_1+r}=\dfrac{6{,}0}{3{,}0+2{,}0}=1{,}2\ \text{A}$ ✓")])],
  [r"a) $I_1=1{,}2\ \text{A}$; $I_2=0{,}50\ \text{A}$", r"b) $r=2{,}0\ \Omega$; $\mathcal{E}=6{,}0\ \text{V}$", r"c) $I_{\text{đm}}=3{,}0\ \text{A}$"],
  r"Nhận dạng: đề cho <strong>hai lần đo $(R,U)$ trên cùng một nguồn</strong> → tính $I$ mỗi lần, viết hai phương trình $U=\mathcal{E}-Ir$ rồi trừ vế."),
 sol(R4, [
  ("Suất điện động của bộ", [P(r"Mỗi dãy có $m=4$ pin nối tiếp nên $\mathcal{E}$ cộng lại; hai dãy song song giữ nguyên $\mathcal{E}$ của dãy:"), M(r"\mathcal{E}_b=m\mathcal{E}_0=4\cdot1{,}5"), A(r"\mathcal{E}_b=6{,}0\ \text{V}")]),
  ("Điện trở trong của bộ", [P(r"Một dãy: $mr_0=4\cdot0{,}50=2{,}0\ \Omega$. Hai dãy giống nhau song song nên chia đôi:"), M(r"r_b=\dfrac{mr_0}{n}=\dfrac{2{,}0}{2}"), A(r"r_b=1{,}0\ \Omega")]),
  ("Dòng qua bóng đèn", [P(r"Bộ nguồn tương đương một nguồn $(\mathcal{E}_b,r_b)$ nối với $R$:"), M(r"I=\dfrac{\mathcal{E}_b}{R+r_b}=\dfrac{6{,}0}{3{,}0+1{,}0}"), A(r"I=1{,}5\ \text{A}")]),
  ("Hiệu điện thế hai cực của bộ", [M(r"U=IR=1{,}5\cdot3{,}0"), P(r"Cách khác:"), M(r"U=\mathcal{E}_b-Ir_b=6{,}0-1{,}5\cdot1{,}0"), A(r"U=4{,}5\ \text{V}")]),
  ("Dòng qua mỗi pin", [P(r"Hai dãy giống nhau chia đều dòng chính; các pin trong một dãy nối tiếp có cùng dòng:"), M(r"I_{\text{pin}}=\dfrac{I}{n}=\dfrac{1{,}5}{2}"), A(r"I_{\text{pin}}=0{,}75\ \text{A}")]),
  ("Kiểm tra", [P(r"Xét một dãy: $4\mathcal{E}_0-I_{\text{pin}}\cdot4r_0=6{,}0-0{,}75\cdot2{,}0=4{,}5\ \text{V}=U$ ✓"), P(r"Hai cách tính $U$ ở bước 4 cho cùng kết quả ✓")])],
  [r"a) $\mathcal{E}_b=6{,}0\ \text{V}$; $r_b=1{,}0\ \Omega$", r"b) $I=1{,}5\ \text{A}$", r"c) $U=4{,}5\ \text{V}$", r"d) $I_{\text{pin}}=0{,}75\ \text{A}$"],
  r"Nhận dạng: đề cho <strong>$n$ dãy song song, mỗi dãy $m$ pin nối tiếp</strong> → $\mathcal{E}_b=m\mathcal{E}_0$, $r_b=\dfrac{mr_0}{n}$, rồi giải toàn mạch."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC ═════════════
STEPS = [
 dict(nhan_dang="Thấy <b>công của lực lạ khi đưa điện tích qua nguồn</b> → nghĩ tới <b>ℰ = A/q</b>, và q = I·t.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Điện tích dịch chuyển qua nguồn", "Điện tích q đã dịch chuyển qua nguồn bằng bao nhiêu C?", 150, "C", 1,
       loi="Nhân thay vì chia ($q=\\mathcal{E}A$), hoặc dùng công của lực điện ở mạch ngoài thay cho công của lực lạ."),
  buoc("Khoảng thời gian", "Dòng điện đã chạy trong bao nhiêu giây?", 300, "s", 3,
       loi="Lấy $t=A/I$ (chia công cho cường độ) thay vì chia điện tích cho cường độ.",
       ke=[("Từ $q=It$ suy ra thời gian bằng điện tích chia cho cường độ dòng điện", True),
           ("Lấy công của lực lạ chia cho cường độ dòng điện", "$A/I$ có đơn vị J/A, không phải giây; thời gian phải tính từ điện tích đã dịch chuyển."),
           ("Lấy công của lực lạ chia cho suất điện động", "$A/\\mathcal{E}$ chính là điện tích $q$ (đơn vị C), chưa phải thời gian.")]),
  buoc("Công của lực lạ trong pin 1,5 V", "Pin $1{,}5\\ \\text{V}$ đưa cùng lượng điện tích đó thì lực lạ làm công bao nhiêu J?", 225, "J", 2,
       loi="Giữ nguyên công cũ vì \"cùng điện tích\", quên rằng công trên mỗi coulomb chính là suất điện động nên phụ thuộc vào nguồn.",
       ke=[("Nhân suất điện động của pin mới với điện tích đã tìm", True),
           ("Giữ nguyên công của ắc quy vì điện tích như nhau", "Công của lực lạ trên mỗi coulomb chính là $\\mathcal{E}$ nên công phụ thuộc vào $\\mathcal{E}$ của nguồn, không giữ nguyên."),
           ("Chia điện tích cho suất điện động của pin mới", "Đó là $q/\\mathcal{E}'$ có đơn vị C/V, không phải jun; từ $\\mathcal{E}=A/q$ phải nhân $\\mathcal{E}'$ với $q$.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang="Thấy <b>vôn kế chỉ khi hở mạch và khi nối R</b> → nghĩ tới <b>hở mạch: U = ℰ</b>; độ tụt = Ir.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Suất điện động", "Suất điện động của pin bằng bao nhiêu V?", 9.0, "V", 0.05,
       lua_chon=[("$9{,}0\\ \\text{V}$: số chỉ lúc hở mạch", True),
                 ("$7{,}5\\ \\text{V}$: số chỉ lúc có dòng", "Có dòng thì trong pin mất $Ir$, hai cực chỉ còn $U=\\mathcal{E}-Ir$ nhỏ hơn $\\mathcal{E}$."),
                 ("Chưa tính được vì chưa biết điện trở trong", "Hở mạch $I=0$ nên $Ir=0$ và $U=\\mathcal{E}$; không cần biết $r$.")],
       loi="Lấy số chỉ lúc nối điện trở làm suất điện động."),
  buoc("Cường độ dòng điện", "Cường độ dòng điện trong mạch kín bằng bao nhiêu A?", 0.25, "A", 0.01,
       loi="Lấy $I=\\mathcal{E}/R$ như thể pin không có điện trở trong; số chỉ lúc nối $R$ mới là hiệu điện thế hai đầu $R$.",
       ke=[("Áp dụng định luật Ohm cho điện trở ngoài với hiệu điện thế hai đầu $R$", True),
           ("Chia suất điện động cho $R$", "Cách này bỏ qua điện trở trong: $\\mathcal{E}/R$ chỉ đúng khi $r=0$."),
           ("Chia số chỉ lúc nối $R$ cho tổng $R+r$", "$7{,}5\\ \\text{V}/(R+r)$ không phải $I$: $7{,}5\\ \\text{V}$ đã là hiệu điện thế hai cực, còn $\\mathcal{E}$ mới là hiệu điện thế của cả mạch (ngoài và trong).")]),
  buoc("Điện trở trong", "Điện trở trong r của pin bằng bao nhiêu Ω?", 6.0, "Ω", 0.1,
       loi="Lấy $r=U/I$ (đó là điện trở ngoài $R$), hoặc quên chia độ giảm thế trong nguồn cho cường độ dòng điện.",
       ke=[("Lấy độ giảm thế trong nguồn $\\mathcal{E}-U$ chia cho cường độ dòng điện", True),
           ("Lấy số chỉ lúc có dòng chia cho cường độ dòng điện", "$U/I$ là điện trở của mạch ngoài $R$, không phải $r$."),
           ("Lấy suất điện động chia cho cường độ dòng điện", "$\\mathcal{E}/I$ là tổng $R+r$, không phải riêng $r$.")]),
  buoc("Dòng điện khi nối tắt", "Nối tắt hai cực pin thì dòng điện bằng bao nhiêu A?", 1.5, "A", 0.05,
       loi="Dùng $\\mathcal{E}/R$ với $R$ cũ, hoặc dùng số chỉ vôn kế khi có dòng thay cho suất điện động.",
       ke=[("Mạch ngoài không còn điện trở: chia suất điện động cho điện trở trong", True),
           ("Chia suất điện động cho $R$ của đề", "Nối tắt thì điện trở ngoài về gần $0$, không còn là $R$."),
           ("Chia số chỉ lúc có dòng cho điện trở trong", "Dòng khi nối tắt phải dùng suất điện động; số chỉ lúc có dòng đã bị trừ $Ir$.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang="Thấy <b>một nguồn, hai điện trở lần lượt, hai số chỉ vôn kế</b> → nghĩ tới <b>hai phương trình</b> cho ℰ và r.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Dòng trong hai lần đo", "Cường độ dòng điện I₁ ở lần đo thứ nhất bằng bao nhiêu A?", 1.2, "A", 0.02,
       loi="Lấy $U_1/R_2$ (nhầm cặp số của hai lần đo), hoặc coi số chỉ vôn kế là suất điện động rồi chia cho $R$."),
  buoc("Điện trở trong", "Điện trở trong r của nguồn bằng bao nhiêu Ω?", 2.0, "Ω", 0.05,
       loi="Chia hiệu hai số chỉ vôn kế cho tổng hai dòng điện, hoặc chia cho một dòng thay vì hiệu hai dòng.",
       ke=[("Viết $U=\\mathcal{E}-Ir$ cho mỗi lần đo rồi trừ vế để khử $\\mathcal{E}$", True),
           ("Lấy một trong hai số chỉ vôn kế làm suất điện động", "Cả hai số chỉ đều đo lúc có dòng nên đều nhỏ hơn $\\mathcal{E}$; không số nào là $\\mathcal{E}$."),
           ("Cộng hai phương trình theo vế", "Cộng không khử được $\\mathcal{E}$ (còn $2\\mathcal{E}$) nên không tìm được $r$ trực tiếp.")]),
  buoc("Suất điện động", "Suất điện động ℰ của nguồn bằng bao nhiêu V?", 6.0, "V", 0.05,
       loi="Lấy $\\mathcal{E}=U_1$ hoặc $\\mathcal{E}=U_1+U_2$, quên hạng tử $Ir$.",
       ke=[("Thế $r$ vừa tìm vào một phương trình $U=\\mathcal{E}-Ir$ rồi giải ra $\\mathcal{E}$", True),
           ("Cộng hai số chỉ vôn kế", "Hai số chỉ ứng với hai lần đo khác nhau; cộng chúng không có ý nghĩa vật lí."),
           ("Lấy $\\mathcal{E}=I_1R_1$", "Đó chỉ là hiệu điện thế ở ngoài; thiếu độ giảm thế $Ir$ trong nguồn.")]),
  buoc("Dòng điện khi nối tắt", "Nối tắt hai cực nguồn thì dòng điện bằng bao nhiêu A?", 3.0, "A", 0.05,
       loi="Dùng $\\mathcal{E}/R_1$ với một trong hai điện trở của đề thay vì $\\mathcal{E}/r$.",
       ke=[("Chia suất điện động cho điện trở trong", True),
           ("Chia suất điện động cho $R_1$", "Nối tắt thì mạch ngoài không còn $R_1$; chỉ còn điện trở trong giữ dòng."),
           ("Chia số chỉ vôn kế lần 2 cho điện trở trong", "Dòng nối tắt phải dùng suất điện động, không phải số chỉ lúc có dòng.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang="Thấy <b>nhiều pin giống nhau ghép dãy song song, mỗi dãy nối tiếp</b> → nghĩ tới <b>bộ nguồn tương đương</b>.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Suất điện động của bộ", "Suất điện động ℰ_b của bộ nguồn bằng bao nhiêu V?", 6.0, "V", 0.05,
       loi="Cộng suất điện động của cả 8 pin, hoặc lấy suất điện động của một pin vì \"có song song\"."),
  buoc("Điện trở trong của bộ", "Điện trở trong r_b của bộ nguồn bằng bao nhiêu Ω?", 1.0, "Ω", 0.02,
       loi="Cộng điện trở trong của cả 8 pin, hoặc chia $r_0$ cho 8 như thể 8 pin đều song song.",
       ke=[("Điện trở một dãy bằng tổng các điện trở trong của pin trong dãy, rồi chia cho số dãy song song", True),
           ("Cộng điện trở trong của cả 8 pin", "Chỉ các pin cùng dãy (nối tiếp) mới cộng; hai dãy song song thì điện trở chung giảm đi."),
           ("Chia điện trở trong của một pin cho 8", "Các pin trong một dãy nối tiếp, không phải song song; chia chỉ đúng với các nhánh song song.")]),
  buoc("Dòng qua bóng đèn", "Cường độ dòng điện qua bóng đèn bằng bao nhiêu A?", 1.5, "A", 0.05,
       loi="Dùng $\\mathcal{E}_0/(R+r_0)$ của một pin, hoặc bỏ $r_b$ khỏi mẫu số ($\\mathcal{E}_b/R$).",
       ke=[("Coi bộ nguồn là một nguồn $(\\mathcal{E}_b,r_b)$ rồi dùng định luật Ohm cho toàn mạch", True),
           ("Dùng suất điện động và điện trở trong của một pin", "Đèn được cấp điện bởi cả bộ nguồn, không phải một pin."),
           ("Chia $\\mathcal{E}_b$ cho $R$", "Bỏ qua điện trở trong của bộ; dòng phải chia cho $R+r_b$.")]),
  buoc("Hiệu điện thế hai cực của bộ", "Hiệu điện thế giữa hai cực của bộ nguồn bằng bao nhiêu V?", 4.5, "V", 0.05,
       loi="Lấy $U=\\mathcal{E}_b$ (chỉ đúng khi hở mạch), hoặc lấy $U=Ir_b$ (đó là độ giảm thế trong nguồn).",
       ke=[("Lấy dòng điện nhân với điện trở ngoài (hoặc $\\mathcal{E}_b-Ir_b$)", True),
           ("Lấy $U$ bằng suất điện động của bộ", "Chỉ đúng khi hở mạch; có dòng thì $U=\\mathcal{E}_b-Ir_b$ nhỏ hơn."),
           ("Lấy dòng điện nhân với điện trở trong của bộ", "$Ir_b$ là phần mất đi bên trong nguồn, không phải hiệu điện thế hai cực.")]),
  buoc("Dòng qua mỗi pin", "Cường độ dòng điện qua mỗi pin bằng bao nhiêu A?", 0.75, "A", 0.02,
       loi="Cho mỗi pin chịu cả dòng chính, hoặc chia dòng chính cho 8 pin.",
       ke=[("Chia dòng chính cho số dãy song song; các pin cùng dãy có cùng dòng", True),
           ("Mỗi pin chịu cả dòng chính", "Hai dãy song song chia nhau dòng chính nên mỗi dãy chỉ nhận một phần."),
           ("Chia dòng chính cho 8 pin", "Các pin trong một dãy nối tiếp nên có cùng dòng; chỉ chia cho số dãy.")]),
  buoc("Kiểm tra")]),
]

# ═════════════ GHI FILE ═════════════
BUILD = [d1, d2, d3, d4]
write(J, 43, "Bài 24. Nguồn điện", DANG, BUILD, ANALYSIS, SOLS)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-11-02"
d["review"] = {"checked": False, "notes": "chờ kiểm chéo (kiem-code)"}
raw = json.dumps(d, ensure_ascii=False, indent=1)


def _walk(x):
    if isinstance(x, str): yield x
    elif isinstance(x, dict):
        for v in x.values(): yield from _walk(v)
    elif isinstance(x, list):
        for v in x: yield from _walk(v)
for _s in _walk(d):
    assert not re.search(r"[\x00-\x1f]", _s), "còn ký tự điều khiển/TAB: " + repr(_s[:60])
    assert '\\"' not in _s, "còn dấu gạch chéo trước nháy: " + _s[:60]
open(J, "w").write(raw)
print("xong", J, "marker-end:", raw.count("marker-end"))
