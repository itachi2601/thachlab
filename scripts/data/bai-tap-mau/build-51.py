"""Dựng scripts/data/bai-tap-mau/51.json — L10 Bài 6. Thực hành: Đo tốc độ của vật chuyển động (soạn 10/11/2026).
Bốn dạng bám bài lý thuyết mới (bi thép, máng nghiêng, hai cổng quang E–F, đồng hồ hiện số MODE A↔B / B).
Hình của dạng = bảng số liệu ngay trong đề (bài thực hành: học sinh đọc bảng, không cần mô phỏng).
Quy ước sai số như Bài 3: ΔA = lệch trung bình + sai số dụng cụ; vạch chia lấy nửa ĐCNN, hiện số lấy một ĐCNN.

  python3 scripts/data/bai-tap-mau/build-51.py        # ghi 51.json (giữ review nếu đã kiểm chéo)
"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import tbl, sol, buoc, M, P, A

OUT = os.path.join(HERE, "51.json")
T_DO = "Tốc độ trung bình và vận tốc trung bình"
T_SS = "Sai số tuyệt đối, sai số tỉ đối"
T_GHI = "Ghi kết quả đo và chữ số có nghĩa"


def bang(dau, hang):
    return ('<div class="table-scroll"><table class="tl-table"><thead><tr>' + "".join(f"<th>{c}</th>" for c in dau) + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in h) + "</tr>" for h in hang) + "</tbody></table></div>")


# ───────────── Số liệu + tự kiểm (đổi số ở đây thì assert báo ngay chỗ lệch) ─────────────
# Dạng 1
s1, t1, d1, tF1 = 0.400, 0.712, 0.0200, 0.022
assert round(s1 / t1, 3) == 0.562 and round(d1 / tF1, 2) == 0.91
# Dạng 2
s2, ds2, ts2 = 0.650, 0.0005, [0.899, 0.903, 0.904]
tb2 = sum(ts2) / 3; lech2 = sum(abs(x - tb2) for x in ts2) / 3; dt2 = round(lech2, 3) + 0.001
v2 = s2 / tb2; dv_pt2 = (ds2 / s2 + dt2 / tb2) * 100
assert round(tb2, 3) == 0.902 and round(lech2, 4) == 0.002 and round(dt2, 3) == 0.003
assert round(v2, 3) == 0.721 and round(dv_pt2, 2) == 0.41 and round(v2 * dv_pt2 / 100, 3) == 0.003
# Dạng 3
d3, dd3, t3, dt3 = 16.0, 0.05, 0.020, 0.001
v3 = d3 / 1000 / t3; pd3 = dd3 / d3 * 100; pt3 = dt3 / t3 * 100
assert round(v3, 2) == 0.80 and round(pd3, 2) == 0.31 and round(pt3, 1) == 5.0 and round(pd3 + pt3, 1) == 5.3
assert round(v3 * (pd3 + pt3) / 100, 2) == 0.04
# Dạng 4
R4, h4, t4 = 10.0, 8.0, 0.015
c4 = 2 * math.sqrt(R4**2 - h4**2)
assert round(c4, 1) == 12.0 and round(c4 / 1000 / t4, 2) == 0.80 and round(2 * R4 / 1000 / t4, 2) == 1.33
assert round((2 * R4 - c4) / c4 * 100, 1) == 66.7

DANG = []

# ═════════════ Dạng 1 ═════════════
DANG.append(dict(
    label="Dạng 1 · Dễ · Chọn chế độ đo của đồng hồ và tính tốc độ từ số hiển thị",
    topic=T_DO,
    problem_html=(
        "<p>Viên bi thép lăn trên máng nghiêng qua hai cổng quang E và F nối với đồng hồ đo thời gian hiện số. "
        "Thước trên máng cho $EF = 0{,}400\\ \\text{m}$; thước kẹp cho đường kính bi $d = 20{,}0\\ \\text{mm}$. Đồng hồ hiện hai số sau:</p>"
        + bang(["Lần thả", "Chế độ (MODE)", "Số hiển thị (s)"], [["1", "A↔B", "0,712"], ["2", "B (chỉ cổng F)", "0,022"]])
        + "<p>a) Mỗi số hiển thị là thời gian của việc gì?</p>"
        "<p>b) Tính tốc độ trung bình của bi trên đoạn EF.</p>"
        "<p>c) Tính tốc độ tức thời của bi khi qua cổng F.</p>"),
    tom_de=dict(cho=["$EF = 0{,}400\\ \\text{m}$; $d = 20{,}0\\ \\text{mm}$", "MODE A↔B: $0{,}712\\ \\text{s}$", "MODE B: $0{,}022\\ \\text{s}$"],
                tim=["a) Ý nghĩa từng số", "b) $v_{tb}$ trên EF", "c) $v_F$"]),
    analysis=[
        ("\"MODE A↔B … 0,712\"", "$t = 0{,}712\\ \\text{s}$", "Thời gian bi đi <strong>từ cổng E tới cổng F</strong>"),
        ("\"MODE B … 0,022\"", "$t_F = 0{,}022\\ \\text{s}$", "Thời gian bi <strong>chắn tia</strong> ở cổng F"),
        ("\"EF = 0,400 m\"", "$s = 0{,}400\\ \\text{m}$", "$v_{tb} = \\dfrac{s}{t}$"),
        ("\"đường kính bi d = 20,0 mm\"", "$d = 0{,}0200\\ \\text{m}$", "$v_F = \\dfrac{d}{t_F}$ · ⚠ đổi mm sang m trước khi chia"),
        ("\"tốc độ tức thời … khi qua cổng F\"", "Cần $v_F$", "⚠ $d/t_F$ chỉ thay được tốc độ tức thời khi $t_F$ rất ngắn"),
    ],
    sol=sol(
        ["<strong>Khái niệm:</strong> MODE A↔B đo thời gian đi giữa hai cổng; MODE A hoặc B đo thời gian chắn tia ở một cổng.",
         "Tốc độ trung bình: $v_{tb} = \\dfrac{s}{t}$.",
         "Tốc độ tức thời (gần đúng): $v = \\dfrac{d}{t}$ với $d$ là đường kính bi.",
         "⚠ <strong>Điều kiện:</strong> quãng đường nào đi với thời gian nấy; không lấy $EF$ chia cho thời gian chắn tia."],
        [("Đọc ý nghĩa hai số", [P("$0{,}712\\ \\text{s}$ (MODE A↔B): thời gian bi đi từ E tới F."),
                                 P("$0{,}022\\ \\text{s}$ (MODE B): thời gian bi chắn tia ở cổng F.")]),
         ("Tốc độ trung bình trên EF", [M("v_{tb} = \\dfrac{s}{t} = \\dfrac{0{,}400}{0{,}712}"), A("v_{tb} \\approx 0{,}562\\ \\text{m/s}")]),
         ("Chọn quãng đường cho cổng F", [P("Trong lúc chắn tia, bi đi được đúng một đường kính:"), M("d = 20{,}0\\ \\text{mm} = 0{,}0200\\ \\text{m}")]),
         ("Tốc độ tức thời tại F", [M("v_F = \\dfrac{d}{t_F} = \\dfrac{0{,}0200}{0{,}022}"), A("v_F \\approx 0{,}91\\ \\text{m/s}")]),
         ("Kiểm tra", [P("Bi lăn nhanh dần nên tốc độ ở cuối đoạn phải lớn hơn tốc độ trung bình cả đoạn: $0{,}91 \\gt 0{,}562$, hợp lí.")])],
        ["a) $0{,}712\\ \\text{s}$: thời gian đi E → F; $0{,}022\\ \\text{s}$: thời gian chắn tia ở F.",
         "b) $v_{tb} \\approx 0{,}562\\ \\text{m/s}$.", "c) $v_F \\approx 0{,}91\\ \\text{m/s}$."],
        "Mấu chốt: mỗi MODE đi với một quãng đường riêng — A↔B đi với $EF$, một cổng đi với đường kính bi."),
    nhan_dang="Thấy <b>MODE A↔B</b> → chia $EF$; thấy <b>MODE một cổng</b> → chia đường kính bi.",
    cap_do=1, fading="mo_het", go_roi=dict(buoc_hay_sai=2),
    buoc=[
        buoc("Đọc ý nghĩa hai số", "Số $0{,}022\\ \\text{s}$ ở MODE B là thời gian của việc gì?",
             lua_chon=[("Bi chắn tia sáng ở cổng F", True),
                       ("Bi đi từ cổng E tới cổng F", "Đó là số đo ở MODE A↔B: bắt đầu đếm ở E, dừng ở F."),
                       ("Bi đi từ lúc thả tới cổng F", "Đồng hồ chỉ đếm khi có tia bị chắn, không biết lúc nào bi được thả.")],
             loi="Nhìn số nhỏ tưởng máy đo sai; thật ra MODE một cổng chỉ đếm lúc bi che tia."),
        buoc("Tốc độ trung bình trên EF", "Tính $v_{tb}$ trên đoạn EF (m/s, lấy 3 chữ số sau dấu phẩy).", 0.562, "m/s", 0.002,
             loi="Lấy $0{,}400$ chia cho $0{,}022$: ghép quãng đường EF với thời gian chắn tia.",
             ke=[("Lấy $EF$ chia cho số đo ở MODE A↔B", True),
                 ("Lấy $EF$ chia cho số đo ở MODE B", "Số ở MODE B là thời gian chắn tia, không phải thời gian đi hết EF."),
                 ("Lấy đường kính bi chia cho số đo ở MODE A↔B", "Trong thời gian đó bi đi cả đoạn EF, không phải một đường kính.")]),
        buoc("Chọn quãng đường cho cổng F", "Trong thời gian chắn tia ở F, bi đi được quãng đường nào?",
             lua_chon=[("Một đường kính bi", True),
                       ("Cả đoạn EF", "Đoạn EF đi với thời gian ở MODE A↔B."),
                       ("Một bán kính bi", "Tia bị che từ mép trước tới mép sau của bi, tức cả đường kính.")],
             loi="Quên đổi $20{,}0\\ \\text{mm}$ sang mét trước khi chia.",
             ke=[("Tìm quãng đường bi đi trong lúc chắn tia", True),
                 ("Lấy luôn $v_{tb}$ làm tốc độ tại F", "Bi nhanh dần: tốc độ ở F lớn hơn tốc độ trung bình trên EF."),
                 ("Lấy $EF$ chia cho thời gian chắn tia", "Quãng đường và thời gian không thuộc cùng một chuyển động.")]),
        buoc("Tốc độ tức thời tại F", "Tính $v_F$ (m/s, lấy 2 chữ số sau dấu phẩy).", 0.91, "m/s", 0.005,
             loi="Để nguyên $d = 20{,}0$ rồi chia, ra con số lớn gấp 1000 lần.",
             ke=[("Đổi $d$ sang mét rồi chia cho thời gian chắn tia", True),
                 ("Chia thời gian chắn tia cho $d$", "Tốc độ là quãng đường chia thời gian, không đảo lại."),
                 ("Nhân $d$ với thời gian chắn tia", "Tích đó có đơn vị m·s, không phải m/s.")]),
        buoc("Kiểm tra"),
    ]))

# ═════════════ Dạng 2 ═════════════
DANG.append(dict(
    label="Dạng 2 · Trung bình · Xử lí bảng số liệu tốc độ trung bình và viết kết quả có sai số",
    topic=T_GHI,
    problem_html=(
        "<p>Đo tốc độ trung bình của viên bi trên đoạn EF của máng nghiêng. Thước trên máng có độ chia nhỏ nhất $1\\ \\text{mm}$, đọc được "
        "$s = EF = 0{,}650\\ \\text{m}$. Đồng hồ hiện số (độ chia nhỏ nhất $0{,}001\\ \\text{s}$) đặt MODE A↔B, thả bi ba lần từ cùng một vị trí:</p>"
        + bang(["Lần đo", "1", "2", "3"], [["$t$ (s)", "0,899", "0,903", "0,904"]])
        + "<p>a) Tính $\\bar t$ và sai số tuyệt đối $\\Delta t$.</p>"
        "<p>b) Tính tốc độ trung bình $\\bar v$.</p>"
        "<p>c) Viết kết quả $v = \\bar v \\pm \\Delta v$.</p>"),
    tom_de=dict(cho=["$s = 0{,}650\\ \\text{m}$, thước chia tới $1\\ \\text{mm}$", "$t$: $0{,}899;\\ 0{,}903;\\ 0{,}904\\ \\text{s}$", "Đồng hồ chia tới $0{,}001\\ \\text{s}$"],
                tim=["a) $\\bar t$, $\\Delta t$", "b) $\\bar v$", "c) $v = \\bar v \\pm \\Delta v$"]),
    analysis=[
        ("\"thước … độ chia nhỏ nhất 1 mm\"", "$\\Delta s = 0{,}5\\ \\text{mm} = 0{,}0005\\ \\text{m}$", "⚠ Dụng cụ có vạch chia: sai số dụng cụ lấy <strong>nửa</strong> độ chia nhỏ nhất"),
        ("\"đồng hồ hiện số … 0,001 s\"", "$\\Delta t_{\\text{dc}} = 0{,}001\\ \\text{s}$", "⚠ Dụng cụ hiện số: sai số dụng cụ lấy <strong>một</strong> độ chia nhỏ nhất"),
        ("\"thả bi ba lần\"", "$t_1, t_2, t_3$", "$\\bar t$ = trung bình cộng · $\\Delta t = \\overline{\\Delta t} + \\Delta t_{\\text{dc}}$"),
        ("\"tốc độ trung bình\"", "Cần $\\bar v$", "$\\bar v = \\dfrac{s}{\\bar t}$"),
        ("\"viết kết quả\"", "Cần $\\Delta v$", "Chia thì cộng phần trăm: $\\delta v = \\delta s + \\delta t$; $\\Delta v = \\bar v \\cdot \\delta v$"),
    ],
    sol=sol(
        ["<strong>Khái niệm:</strong> sai số tuyệt đối = lệch trung bình + sai số dụng cụ.",
         "Sai số tỉ đối của thương: $\\delta v = \\delta s + \\delta t$.",
         "Kết quả: $v = \\bar v \\pm \\Delta v$, với $\\Delta v = \\bar v \\cdot \\delta v$.",
         "⚠ <strong>Điều kiện:</strong> $\\Delta v$ giữ một chữ số khác 0; $\\bar v$ viết tới cùng hàng thập phân với $\\Delta v$."],
        [("Thời gian trung bình", [M("\\bar t = \\dfrac{0{,}899 + 0{,}903 + 0{,}904}{3}"), A("\\bar t = 0{,}902\\ \\text{s}")]),
         ("Sai số tuyệt đối của t", [P("Ba độ lệch so với $\\bar t$: $0{,}003$; $0{,}001$; $0{,}002\\ \\text{s}$."),
                                     M("\\overline{\\Delta t} = \\dfrac{0{,}003 + 0{,}001 + 0{,}002}{3} = 0{,}002\\ \\text{s}"),
                                     M("\\Delta t = \\overline{\\Delta t} + \\Delta t_{\\text{dc}} = 0{,}002 + 0{,}001"), A("\\Delta t = 0{,}003\\ \\text{s}")]),
         ("Tốc độ trung bình", [M("\\bar v = \\dfrac{s}{\\bar t} = \\dfrac{0{,}650}{0{,}902}"), A("\\bar v \\approx 0{,}721\\ \\text{m/s}")]),
         ("Sai số tỉ đối của v", [M("\\delta s = \\dfrac{0{,}0005}{0{,}650} \\approx 0{,}08\\ \\%"), M("\\delta t = \\dfrac{0{,}003}{0{,}902} \\approx 0{,}33\\ \\%"),
                                  A("\\delta v = \\delta s + \\delta t \\approx 0{,}41\\ \\%")]),
         ("Sai số tuyệt đối và kết quả", [M("\\Delta v = \\bar v \\cdot \\delta v = 0{,}721 \\cdot 0{,}0041 \\approx 0{,}003\\ \\text{m/s}"),
                                          A("v = 0{,}721 \\pm 0{,}003\\ \\text{m/s}")])],
        ["a) $\\bar t = 0{,}902\\ \\text{s}$; $\\Delta t = 0{,}003\\ \\text{s}$.", "b) $\\bar v \\approx 0{,}721\\ \\text{m/s}$.",
         "c) $v = 0{,}721 \\pm 0{,}003\\ \\text{m/s}$."],
        "Mấu chốt: đi theo đúng chuỗi $\\bar t$ → $\\Delta t$ → $\\bar v$ → $\\delta v$ → $\\Delta v$; phần trăm của $t$ lớn hơn của $s$ nhiều lần."),
    nhan_dang="Thấy <b>bảng ba lần đo</b> → $\\bar t$, $\\Delta t$ rồi cộng phần trăm.",
    cap_do=2, fading="giau_buoc_cuoi", go_roi=dict(buoc_hay_sai=1),
    buoc=[
        buoc("Thời gian trung bình", "Tính $\\bar t$ (s, lấy 3 chữ số sau dấu phẩy).", 0.902, "s", 0.0005,
             loi="Lấy giá trị ở giữa bảng thay cho trung bình cộng của ba lần."),
        buoc("Sai số tuyệt đối của t", "Tính $\\Delta t$ (s), gồm cả sai số dụng cụ.", 0.003, "s", 0.0002,
             loi="Chỉ lấy lệch trung bình, quên cộng sai số dụng cụ của đồng hồ.",
             ke=[("Lấy trung bình ba độ lệch rồi cộng sai số dụng cụ", True),
                 ("Lấy số đo lớn nhất trừ số đo nhỏ nhất", "Hiệu đó là khoảng trải của số liệu, không phải quy ước sai số của bài."),
                 ("Chỉ lấy độ chia nhỏ nhất của đồng hồ", "Ba lần đo lệch nhau nên còn phần sai số ngẫu nhiên phải cộng thêm.")]),
        buoc("Tốc độ trung bình", "Tính $\\bar v$ (m/s, lấy 3 chữ số sau dấu phẩy).", 0.721, "m/s", 0.001,
             loi="Tính ba tốc độ từ ba lần rồi mới lấy trung bình cũng được, nhưng dài hơn và dễ bấm nhầm.",
             ke=[("Lấy $s$ chia cho $\\bar t$", True),
                 ("Lấy $s$ chia cho $\\Delta t$", "$\\Delta t$ là sai số của thời gian, không phải thời gian đi."),
                 ("Lấy $\\bar t$ chia cho $s$", "Thương đó là thời gian đi mỗi mét, không phải tốc độ.")]),
        buoc("Sai số tỉ đối của v", "Tính $\\delta v$ (%, lấy 2 chữ số sau dấu phẩy).", 0.41, "%", 0.02,
             loi="Lấy $\\delta t - \\delta s$ vì $v$ là phép chia; nhân hay chia thì sai số tỉ đối đều cộng.",
             ke=[("Cộng sai số tỉ đối của $s$ và của $t$", True),
                 ("Cộng thẳng $\\Delta s$ với $\\Delta t$", "Hai sai số tuyệt đối khác đơn vị (m và s), không cộng được."),
                 ("Lấy sai số tỉ đối của $t$ trừ của $s$", "Sai số không bù trừ nhau; thương hay tích đều cộng phần trăm.")]),
        buoc("Sai số tuyệt đối và kết quả", "Tính $\\Delta v$ (m/s, giữ một chữ số khác 0).", 0.003, "m/s", 0.0005,
             loi="Nhân $\\bar v$ với $0{,}41$ thay vì $0{,}0041$: quên đổi phần trăm ra số thập phân.",
             ke=[("Nhân $\\bar v$ với $\\delta v$ đã đổi ra số thập phân", True),
                 ("Lấy luôn $\\Delta t$ làm $\\Delta v$", "Hai đại lượng khác đơn vị; phải đi qua sai số tỉ đối."),
                 ("Chia $\\bar v$ cho $\\delta v$", "Sai số tuyệt đối là một phần nhỏ của giá trị đo, nên phải nhân.")]),
    ]))

# ═════════════ Dạng 3 ═════════════
DANG.append(dict(
    label="Dạng 3 · Trung bình · Tốc độ tức thời từ thời gian chắn tia: vì sao sai số lớn",
    topic=T_SS,
    problem_html=(
        "<p>Đo tốc độ tức thời của viên bi tại cổng quang F. Thước kẹp (độ chia nhỏ nhất $0{,}1\\ \\text{mm}$) cho đường kính bi "
        "$d = 16{,}0\\ \\text{mm}$. Đồng hồ hiện số (độ chia nhỏ nhất $0{,}001\\ \\text{s}$) đặt MODE B; cả ba lần thả bi đều hiện "
        "$t = 0{,}020\\ \\text{s}$.</p>"
        "<p>a) Tính tốc độ tức thời $\\bar v$ của bi tại F.</p>"
        "<p>b) Tính sai số tỉ đối $\\delta v$ và viết kết quả $v = \\bar v \\pm \\Delta v$.</p>"
        "<p>c) Muốn kết quả chính xác hơn thì cần cải thiện phép đo đại lượng nào trước?</p>"),
    tom_de=dict(cho=["$d = 16{,}0\\ \\text{mm}$, thước kẹp chia tới $0{,}1\\ \\text{mm}$", "$t = 0{,}020\\ \\text{s}$ (ba lần như nhau)", "Đồng hồ chia tới $0{,}001\\ \\text{s}$"],
                tim=["a) $\\bar v$ tại F", "b) $\\delta v$, $v = \\bar v \\pm \\Delta v$", "c) Đại lượng cần đo kĩ hơn"]),
    analysis=[
        ("\"thước kẹp … 0,1 mm … d = 16,0 mm\"", "$\\Delta d = 0{,}05\\ \\text{mm}$", "Vạch chia: nửa độ chia nhỏ nhất · $\\delta d = \\dfrac{\\Delta d}{d}$"),
        ("\"cả ba lần … đều hiện t = 0,020 s\"", "$\\bar t = 0{,}020\\ \\text{s}$; lệch trung bình bằng 0", "⚠ Ba lần trùng nhau <strong>không</strong> có nghĩa là hết sai số: vẫn còn $\\Delta t_{\\text{dc}} = 0{,}001\\ \\text{s}$"),
        ("\"tốc độ tức thời … tại F\"", "Cần $\\bar v$", "$\\bar v = \\dfrac{d}{\\bar t}$ · ⚠ đổi mm sang m"),
        ("\"sai số tỉ đối\"", "Cần $\\delta v$", "$\\delta v = \\delta d + \\delta t$"),
        ("\"cải thiện phép đo đại lượng nào\"", "So $\\delta d$ với $\\delta t$", "Phần trăm nào lớn hơn thì quyết định sai số của kết quả"),
    ],
    sol=sol(
        ["<strong>Khái niệm:</strong> tốc độ tức thời (gần đúng) $v = \\dfrac{d}{t}$, $t$ là thời gian chắn tia.",
         "Sai số tỉ đối: $\\delta d = \\dfrac{\\Delta d}{d}$, $\\delta t = \\dfrac{\\Delta t}{\\bar t}$, $\\delta v = \\delta d + \\delta t$.",
         "⚠ <strong>Điều kiện:</strong> so sai số với chính giá trị đo; $0{,}001\\ \\text{s}$ là nhỏ với $0{,}9\\ \\text{s}$ nhưng lớn với $0{,}020\\ \\text{s}$."],
        [("Tốc độ tức thời", [M("\\bar v = \\dfrac{d}{\\bar t} = \\dfrac{0{,}0160}{0{,}020}"), A("\\bar v = 0{,}80\\ \\text{m/s}")]),
         ("Sai số tỉ đối của t", [P("Ba lần trùng nhau nên lệch trung bình bằng 0, còn sai số dụng cụ:"), M("\\Delta t = 0 + 0{,}001 = 0{,}001\\ \\text{s}"),
                                  A("\\delta t = \\dfrac{0{,}001}{0{,}020} = 5\\ \\%")]),
         ("Sai số tỉ đối của v", [M("\\delta d = \\dfrac{0{,}05}{16{,}0} \\approx 0{,}3\\ \\%"), A("\\delta v = \\delta d + \\delta t \\approx 5{,}3\\ \\%")]),
         ("Viết kết quả", [M("\\Delta v = \\bar v \\cdot \\delta v = 0{,}80 \\cdot 0{,}053 \\approx 0{,}04\\ \\text{m/s}"), A("v = 0{,}80 \\pm 0{,}04\\ \\text{m/s}")]),
         ("Đại lượng cần đo kĩ hơn", [P("$\\delta t = 5\\ \\%$ lớn gấp khoảng 16 lần $\\delta d \\approx 0{,}3\\ \\%$."),
                                      A("T:Cần cải thiện phép đo thời gian (đồng hồ chia nhỏ hơn), đo $d$ kĩ thêm gần như không giúp gì.")])],
        ["a) $\\bar v = 0{,}80\\ \\text{m/s}$.", "b) $\\delta v \\approx 5{,}3\\ \\%$; $v = 0{,}80 \\pm 0{,}04\\ \\text{m/s}$.",
         "c) Cải thiện phép đo thời gian chắn tia."],
        "Mấu chốt: thời gian chắn tia chỉ gồm vài chục độ chia của đồng hồ nên một độ chia đã là vài phần trăm."),
    nhan_dang="Thấy <b>thời gian chắn tia rất ngắn</b> → sai số phần trăm của $t$ quyết định kết quả.",
    cap_do=2, fading="giau_buoc_cuoi", go_roi=dict(buoc_hay_sai=1),
    buoc=[
        buoc("Tốc độ tức thời", "Tính $\\bar v$ tại F (m/s).", 0.8, "m/s", 0.005,
             loi="Quên đổi $16{,}0\\ \\text{mm}$ sang mét, ra kết quả lớn gấp 1000 lần."),
        buoc("Sai số tỉ đối của t", "Tính $\\delta t$ (%).", 5, "%", 0.1,
             loi="Thấy ba lần đo trùng nhau nên cho $\\Delta t = 0$; sai số dụng cụ vẫn còn.",
             ke=[("Lấy sai số dụng cụ của đồng hồ chia cho $\\bar t$", True),
                 ("Cho $\\delta t = 0$ vì ba lần đo giống nhau", "Ba lần trùng nhau chỉ làm lệch trung bình bằng 0; sai số dụng cụ vẫn còn."),
                 ("Lấy sai số dụng cụ của đồng hồ chia cho $d$", "Sai số tỉ đối của đại lượng nào thì chia cho chính đại lượng ấy.")]),
        buoc("Sai số tỉ đối của v", "Tính $\\delta v$ (%, lấy 1 chữ số sau dấu phẩy).", 5.3, "%", 0.05,
             loi="Tính $\\delta d$ bằng độ chia nhỏ nhất $0{,}1\\ \\text{mm}$ thay vì nửa độ chia.",
             ke=[("Tính $\\delta d$ rồi cộng với $\\delta t$", True),
                 ("Lấy $\\delta t$ nhân với $\\delta d$", "Sai số tỉ đối của một thương là tổng, không phải tích."),
                 ("Bỏ hẳn $\\delta d$ vì đã có $\\delta t$", "$\\delta d$ nhỏ nhưng vẫn phải cộng trước khi làm tròn.")]),
        buoc("Viết kết quả", "Tính $\\Delta v$ (m/s, giữ một chữ số khác 0).", 0.04, "m/s", 0.005,
             loi="Viết $v = 0{,}8 \\pm 0{,}04$: giá trị trung bình phải viết tới cùng hàng thập phân với sai số.",
             ke=[("Nhân $\\bar v$ với $\\delta v$ đã đổi ra số thập phân", True),
                 ("Lấy $\\Delta t$ làm $\\Delta v$", "Hai đại lượng khác đơn vị; phải đi qua sai số tỉ đối."),
                 ("Cộng $\\Delta d$ với $\\Delta t$", "Mét và giây không cộng được với nhau.")]),
        buoc("Đại lượng cần đo kĩ hơn", "Cần cải thiện phép đo nào trước để giảm $\\delta v$?",
             lua_chon=[("Thời gian chắn tia: dùng đồng hồ có độ chia nhỏ hơn", True),
                       ("Đường kính bi: dùng thước chia nhỏ hơn", "$\\delta d$ chỉ khoảng $0{,}3\\ \\%$; giảm tiếp gần như không đổi được $\\delta v$."),
                       ("Không cần gì thêm vì ba lần đo đã trùng nhau", "Trùng nhau chỉ cho thấy đồng hồ không đủ nhạy để thấy chỗ khác nhau.")],
             loi="Chọn dụng cụ theo sai số tuyệt đối nhỏ; phải so theo phần trăm.",
             ke=[("So $\\delta d$ với $\\delta t$, cái nào lớn hơn thì sửa trước", True),
                 ("So $\\Delta d$ với $\\Delta t$", "Hai sai số tuyệt đối khác đơn vị, không so trực tiếp được."),
                 ("Thả bi thêm nhiều lần nữa", "Sai số dụng cụ không giảm khi lặp lại phép đo.")]),
    ]))

# ═════════════ Dạng 4 ═════════════
DANG.append(dict(
    label="Dạng 4 · Khó · Tia sáng lệch tâm bi: tìm sai số hệ thống của phép đo tốc độ tức thời",
    topic=T_SS,
    problem_html=(
        "<p>Viên bi thép đường kính $d = 20{,}0\\ \\text{mm}$ lăn qua cổng quang F. Do cổng lắp thấp, tia sáng không đi qua tâm bi mà "
        "cắt bi theo một dây cung cách tâm $h = 8{,}0\\ \\text{mm}$. Đồng hồ đặt MODE B hiện $t = 0{,}015\\ \\text{s}$. "
        "Một nhóm vẫn tính tốc độ bằng $d/t$.</p>"
        "<p>a) Trong lúc chắn tia, bi thật sự đi được quãng đường bao nhiêu?</p>"
        "<p>b) Tính tốc độ đúng của bi tại F.</p>"
        "<p>c) Kết quả $d/t$ của nhóm lớn hơn tốc độ đúng bao nhiêu phần trăm?</p>"
        "<p>d) Thả bi thêm nhiều lần rồi lấy trung bình có làm mất độ lệch này không?</p>"),
    tom_de=dict(cho=["$d = 20{,}0\\ \\text{mm}$", "Tia cách tâm bi $h = 8{,}0\\ \\text{mm}$", "MODE B: $t = 0{,}015\\ \\text{s}$"],
                tim=["a) Quãng đường chắn tia", "b) Tốc độ đúng tại F", "c) $d/t$ lệch bao nhiêu %", "d) Lấy trung bình có hết lệch không"]),
    analysis=[
        ("\"đường kính d = 20,0 mm\"", "Bán kính $R = 10{,}0\\ \\text{mm}$", "Dùng $R$ cho tam giác vuông tâm – trung điểm dây – mép bi"),
        ("\"tia … cắt bi theo một dây cung cách tâm h = 8,0 mm\"", "$h = 8{,}0\\ \\text{mm}$", "⚠ $d/t$ chỉ đúng khi tia qua <strong>tâm</strong> bi; lệch tâm thì quãng đường chắn tia là dây cung $c = 2\\sqrt{R^2 - h^2}$"),
        ("\"MODE B hiện t = 0,015 s\"", "$t = 0{,}015\\ \\text{s}$", "Tốc độ đúng: $v = \\dfrac{c}{t}$"),
        ("\"lớn hơn … bao nhiêu phần trăm\"", "So $d/t$ với $c/t$", "Cùng $t$ nên tỉ số tốc độ bằng tỉ số $d/c$"),
        ("\"lấy trung bình có làm mất độ lệch\"", "Lệch cùng một phía ở mọi lần đo", "⚠ Sai số hệ thống: lặp lại không giảm, phải sửa cách lắp"),
    ],
    sol=sol(
        ["<strong>Khái niệm:</strong> thời gian chắn tia ứng với đoạn bi che tia, không phải lúc nào cũng là đường kính.",
         "Dây cung cách tâm $h$: $c = 2\\sqrt{R^2 - h^2}$ (định lí Pythagore).",
         "Sai số ngẫu nhiên: lệch lúc nhiều lúc ít, lấy trung bình thì giảm. Sai số hệ thống: lệch một phía, lấy trung bình không giảm.",
         "⚠ <strong>Điều kiện:</strong> chỉ dùng $v = d/t$ khi tia đi qua tâm bi."],
        [("Quãng đường chắn tia", [M("R = \\dfrac{d}{2} = 10{,}0\\ \\text{mm}"), M("c = 2\\sqrt{R^2 - h^2} = 2\\sqrt{10{,}0^2 - 8{,}0^2} = 2 \\cdot 6{,}0"),
                                    A("c = 12{,}0\\ \\text{mm}")]),
         ("Tốc độ đúng tại F", [M("v = \\dfrac{c}{t} = \\dfrac{0{,}0120}{0{,}015}"), A("v = 0{,}80\\ \\text{m/s}")]),
         ("Độ lệch của d/t", [M("\\dfrac{d}{t} = \\dfrac{0{,}0200}{0{,}015} \\approx 1{,}33\\ \\text{m/s}"),
                              M("\\dfrac{d/t - c/t}{c/t} = \\dfrac{d - c}{c} = \\dfrac{20{,}0 - 12{,}0}{12{,}0}"), A("\\approx 66{,}7\\ \\%")]),
         ("Lấy trung bình có hết lệch không", [P("Lần thả nào tia cũng cắt đúng dây cung ấy nên lần nào $d/t$ cũng lớn hơn tốc độ đúng."),
                                              A("T:Không. Đây là sai số hệ thống; phải chỉnh cổng cho tia đi qua tâm bi.")])],
        ["a) $c = 12{,}0\\ \\text{mm}$.", "b) $v = 0{,}80\\ \\text{m/s}$.", "c) Lớn hơn khoảng $66{,}7\\ \\%$.",
         "d) Không; phải chỉnh lại độ cao cổng quang."],
        "Mấu chốt: trước khi chia $d/t$, hỏi \"tia có qua tâm bi không?\" — lệch tâm thì quãng đường chắn tia ngắn hơn đường kính."),
    nhan_dang="Thấy <b>tia lệch tâm bi</b> → quãng đường chắn tia là dây cung, ngắn hơn đường kính.",
    cap_do=3, fading="giau_tu_buoc_2", go_roi=dict(buoc_hay_sai=0),
    buoc=[
        buoc("Quãng đường chắn tia", "Tính độ dài dây cung $c$ mà tia cắt trên bi (mm).", 12, "mm", 0.1,
             loi="Dùng đường kính thay cho bán kính trong tam giác vuông, hoặc quên nhân đôi nửa dây cung."),
        buoc("Tốc độ đúng tại F", "Tính tốc độ đúng của bi tại F (m/s).", 0.8, "m/s", 0.005,
             loi="Vẫn lấy đường kính chia cho $t$ theo thói quen.",
             ke=[("Lấy dây cung $c$ (đổi ra mét) chia cho $t$", True),
                 ("Lấy đường kính $d$ chia cho $t$", "Tia không qua tâm nên trong thời gian $t$ bi không đi hết một đường kính."),
                 ("Lấy khoảng cách $h$ chia cho $t$", "$h$ là độ lệch của tia so với tâm, không phải quãng đường bi đi.")]),
        buoc("Độ lệch của d/t", "Kết quả $d/t$ lớn hơn tốc độ đúng bao nhiêu phần trăm (lấy 1 chữ số sau dấu phẩy)?", 66.7, "%", 0.5,
             loi="Chia hiệu cho $d$ (ra 40 %): mốc so sánh phải là tốc độ đúng, tức chia cho $c$.",
             ke=[("Lấy $(d - c)$ chia cho $c$", True),
                 ("Lấy $(d - c)$ chia cho $d$", "Đề hỏi lớn hơn bao nhiêu so với tốc độ đúng nên mốc là $c$."),
                 ("Lấy $h$ chia cho $R$", "Tỉ số đó cho biết tia lệch tâm bao nhiêu, không phải tốc độ lệch bao nhiêu.")]),
        buoc("Lấy trung bình có hết lệch không", "Thả bi thêm nhiều lần rồi lấy trung bình thì độ lệch này thế nào?",
             lua_chon=[("Giữ nguyên, vì lần nào cũng lệch về cùng một phía", True),
                       ("Giảm dần, vì lấy trung bình luôn làm giảm sai số", "Lấy trung bình chỉ giảm sai số ngẫu nhiên, lúc lệch lên lúc lệch xuống."),
                       ("Mất hẳn nếu thả đủ nhiều lần", "Cổng vẫn lắp lệch thì lần đo nào tia cũng cắt cùng một dây cung.")],
             loi="Coi mọi sai số đều giảm khi đo nhiều lần; sai số hệ thống phải sửa ở cách bố trí.",
             ke=[("Xét xem độ lệch có đổi dấu giữa các lần đo không", True),
                 ("Tính lại sai số dụng cụ của đồng hồ", "Độ lệch này do vị trí tia, không do độ chia của đồng hồ."),
                 ("Đổi sang MODE A↔B rồi đo lại", "MODE A↔B đo tốc độ trung bình trên EF, không phải tốc độ tại F.")]),
    ]))

# ───────────── Ghi file ─────────────
old = json.load(open(OUT)) if os.path.exists(OUT) else {}
out = {"lesson_id": 51, "lesson_title": "Bài 6. Thực hành: Đo tốc độ của vật chuyển động", "generated_at": "2026-11-10",
       "review": old.get("review", {"checked": False, "notes": "chờ kiểm chéo"}), "dang_bai": []}
for x in DANG:
    q = dict(form="bai_tap", label=x["label"], topic=x["topic"], problem_html=x["problem_html"], solution_html=x["sol"],
             analysis_html=tbl(x["analysis"]), nhan_dang=x["nhan_dang"], cap_do=x["cap_do"], fading=x["fading"], go_roi=x["go_roi"],
             buoc=x["buoc"], tom_de=x["tom_de"])
    out["dang_bai"].append(q)
json.dump(out, open(OUT, "w"), ensure_ascii=False, indent=1)
print("ok", len(out["dang_bai"]), "dạng →", OUT)
