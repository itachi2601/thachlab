"""Bài tập mẫu bài 46 — Bài 1. Làm quen với Vật lí (Lớp 10). 3 dạng định tính + số ít, dễ → khó.
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-46.py  → ghi scripts/data/bai-tap-mau/46.json (review.checked=false)
Chủ đề ngân hàng: 'Đối tượng và phương pháp nghiên cứu Vật lí' (bài tập thật rất ít → form 'ly_thuyet' cho bài tương tự)."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

HERE = os.path.dirname(os.path.abspath(__file__))
J = os.path.join(HERE, "46.json")
VB = "0 0 420 200"
NOTE = "Hình minh hoạ, không theo tỉ lệ."
TOPIC = "Đối tượng và phương pháp nghiên cứu Vật lí"

# ───────────── số liệu (tự kiểm) ─────────────
S, V = 2.4, 0.30
T_LT = S / V                       # lí thuyết (Nam)
LAN_HA = [8.6, 8.7, 8.5]; SS_HA = 0.2
T_TN = sum(LAN_HA) / 3; CHENH2 = T_TN - T_LT
assert abs(T_LT - 8.0) < 1e-9 and abs(T_TN - 8.6) < 1e-9 and abs(CHENH2 - 0.6) < 1e-9 and CHENH2 > SS_HA
assert all(abs(x - T_TN) <= SS_HA + 1e-9 for x in LAN_HA)           # ba lần đo nhất quán
KL = [14.2, 13.8, 14.0]; XOP = [22.5, 23.1, 22.8]; SS_COC = 0.5
mkl, mx = sum(KL) / 3, sum(XOP) / 3
assert abs(mkl - 14.0) < 1e-9 and abs(mx - 22.8) < 1e-9 and abs((mx - mkl) - 8.8) < 1e-9 and (mx - mkl) > 10 * SS_COC
assert all(abs(x - mkl) <= 0.3 for x in KL) and all(abs(x - mx) <= 0.4 for x in XOP)

# ───────────── Dạng 1: thang kích thước, vi mô – vĩ mô ─────────────
def scale(k):
    b = seg(30, 110, 388, 110, "currentColor", 2) + chevron(388, 110, 1, 0, "currentColor", 2)
    b += seg(210, 62, 210, 150, MUTE, 1.6, "5 4")
    b += lbl(120, 60, "vi mô", RED, 15, "middle", "700") + lbl(120, 80, "mắt thường không thấy", "currentColor", 12, "middle", "400")
    b += lbl(300, 60, "vĩ mô", BLUE, 15, "middle", "700") + lbl(300, 80, "mắt thường thấy được", "currentColor", 12, "middle", "400")
    b += lbl(210, 172, "ranh giới: mắt thường", MUTE, 12, "middle", "400") + lbl(388, 134, "kích thước tăng", "currentColor", 12, "end", "400")
    if k == 0:
        pts = [(40 + 340 * t / 30, 110) for t in range(31)]
        b += ball(pts, 0, 0.1)
        return fig("d1-0", VB, "Thang kích thước: bên trái ranh giới mắt thường là vi mô, bên phải là vĩ mô; chấm chạy từ nhỏ đến lớn",
                   b, "Mô phỏng: chấm đi từ vật rất nhỏ đến vật rất lớn, băng qua ranh giới mắt thường. " + NOTE)
    b += lbl(120, 102, "?", RED, 18, "middle", "700") + lbl(300, 102, "?", BLUE, 18, "middle", "700")
    return fig("d1-2", VB, "Thang kích thước với ranh giới mắt thường", b, "Dữ kiện: tiêu chí phân loại là mắt thường thấy hay không. " + NOTE)

MUTE = "#94a3b8"

# ───────────── Dạng 2: xe đồ chơi, lí thuyết và thực nghiệm ─────────────
def car(x0):
    return (f'<rect x="{x0}" y="92" width="44" height="16" rx="3" fill="none" stroke="currentColor" stroke-width="2"/>'
            f'<circle cx="{x0 + 10}" cy="111" r="5" fill="currentColor"/><circle cx="{x0 + 34}" cy="111" r="5" fill="currentColor"/>')

def track(k):
    b = seg(40, 120, 380, 120, "currentColor", 2)
    for x, s in ((50, "0"), (370, "2,4 m" if k == 0 else "")):
        b += seg(x, 120, x, 130, "currentColor", 2) + lbl(x, 148, s, "currentColor", 13, "middle", "600")
    if k == 0:
        b += (f'<g>{car(28)}<animateTransform attributeName="transform" type="translate" values="0 0;320 0" dur="2s" begin="indefinite" fill="freeze"/></g>')
        b += lbl(210, 62, "v = 0,30 m/s (xe chạy đều theo mô hình)", ORG, 13, "middle", "700")
        return fig("d2-0", VB, "Xe đồ chơi chạy trên đường dài 2,4 m", b, "Mô phỏng: xe chạy đều theo mô hình, chạy nhanh 4 lần so với thật. " + NOTE)
    b += car(28) + dim("", "o", 50, 80, 370, 80, "2,4 m", 210, 70, "middle")
    b += lbl(210, 178, "t = ? (tính và đo)", RED, 14, "middle", "700")
    return fig("d2-2", VB, "Xe đồ chơi và quãng đường 2,4 m", b, "Dữ kiện: quãng đường 2,4 m, tốc độ 0,30 m/s. " + NOTE)

# ───────────── Dạng 3: hai cốc đá ─────────────
def cup(x, label, thick, k, melt):
    b = (f'<path d="M{x},60 L{x + 8},160 L{x + 72},160 L{x + 80},60" fill="none" stroke="currentColor" stroke-width="{thick}" stroke-linejoin="round"/>')
    h0 = 80
    if k == 0:
        h1 = h0 * (1 - melt)
        b += (f'<rect x="{x + 6}" y="{160 - h0}" width="68" height="{h0}" fill="{BLUE}" opacity="0.55">'
              f'{smil("y", [160 - h0, 160 - h1], 7)}{smil("height", [h0, h1], 7)}</rect>')
    else:
        b += f'<rect x="{x + 6}" y="{160 - h0}" width="68" height="{h0}" fill="{BLUE}" opacity="0.55"/>'
    return b + lbl(x + 40, 184, label, "currentColor", 13, "middle", "700")

def cups(k):
    b = cup(90, "cốc kim loại", 4, k, 1.0) + cup(250, "cốc xốp", 2, k, 14.0 / 22.8)
    if k == 0:
        return fig("d3-0", VB, "Hai cốc cùng đựng đá lạnh, cốc kim loại và cốc xốp, đá tan dần", b,
                   "Mô phỏng đơn giản: đá tan dần ở hai cốc, 1 s mô phỏng ≈ 2 phút thật (không phải số đo). " + NOTE)
    b += lbl(130, 50, "t = ?", RED, 14, "middle", "700") + lbl(290, 50, "t = ?", RED, 14, "middle", "700")
    return fig("d3-2", VB, "Hai cốc đá, thời gian tan cần tìm", b, "Dữ kiện: hai cốc cùng dung tích, cùng lượng đá. " + NOTE)

BUILD = [scale, track, cups]

# ───────────── đề ─────────────
DANG = [
 dict(label="Dạng 1 · Dễ · Phân loại vi mô – vĩ mô và lĩnh vực ứng dụng của Vật lí", topic=TOPIC,
      problem_html=(r"<p>Một học sinh ghi lại bốn đối tượng gặp trong buổi học: <strong>(1)</strong> một nguyên tử đồng trong sợi dây điện; "
                    r"<strong>(2)</strong> chiếc máy tính bảng đặt trên bàn; <strong>(3)</strong> Mặt Trăng; <strong>(4)</strong> một phân tử nước trong cốc.</p>"
                    r"<p>Ba ứng dụng của Vật lí em thấy trong tuần: <strong>(I)</strong> máy siêu âm khám thai; <strong>(II)</strong> đèn LED chiếu sáng cho rau trong nhà kính; "
                    r"<strong>(III)</strong> kính hiển vi điện tử để nghiên cứu cấu trúc tế bào.</p>"
                    r"<p>a) Đối tượng nào thuộc cấp độ vi mô, đối tượng nào thuộc vĩ mô?</p>"
                    r"<p>b) Mỗi ứng dụng (I), (II), (III) thuộc lĩnh vực nào trong năm lĩnh vực: thông tin liên lạc, y tế, công nghiệp, nông nghiệp, nghiên cứu?</p>")),
 dict(label="Dạng 2 · Trung bình · Phương pháp lí thuyết và thực nghiệm: so dự đoán với số đo", topic=TOPIC,
      problem_html=(r"<p>Nhóm Nam và Hà muốn biết một xe đồ chơi chạy hết đường dài $2{,}4\ \text{m}$ mất bao lâu. Nam coi xe chạy đều với tốc độ $0{,}30\ \text{m/s}$ "
                    r"và tính $t = \dfrac{s}{v}$. Hà thả xe rồi bấm đồng hồ ba lần, được $8{,}6\ \text{s}$; $8{,}7\ \text{s}$; $8{,}5\ \text{s}$. Sai số của mỗi phép đo thời gian là $\pm 0{,}2\ \text{s}$.</p>"
                    r"<p>a) Cách làm của Nam và của Hà thuộc phương pháp nghiên cứu nào?</p>"
                    r"<p>b) Giá trị trung bình của Hà lệch bao nhiêu so với kết quả Nam tính?</p>"
                    r"<p>c) Độ lệch đó có vượt sai số không? Nhóm nên làm gì tiếp theo?</p>")),
 dict(label="Dạng 3 · Khó · Quy trình 5 bước: nhận ra giả thuyết, đọc số liệu và kết luận", topic=TOPIC,
      problem_html=(r"<p>Hoa thấy đá lạnh trong cốc kim loại tan nhanh hơn trong cốc xốp. Hoa hỏi: \"Vì sao đá trong cốc kim loại tan nhanh hơn?\" rồi nói: "
                    r"\"Chắc do kim loại truyền nhiệt từ không khí vào đá nhanh hơn.\" Hoa dùng hai cốc cùng dung tích, cho cùng lượng đá, đặt cùng chỗ và đo thời gian đá tan hết, mỗi cốc ba lần "
                    r"(phút), sai số mỗi lần đo $\pm 0{,}5$ phút:</p>"
                    r"<div class=\"table-scroll\"><table class=\"tl-table\"><thead><tr><th>Cốc</th><th>Lần 1</th><th>Lần 2</th><th>Lần 3</th></tr></thead><tbody>"
                    r"<tr><td>Kim loại</td><td>14,2</td><td>13,8</td><td>14,0</td></tr><tr><td>Xốp</td><td>22,5</td><td>23,1</td><td>22,8</td></tr></tbody></table></div>"
                    r"<p>a) Câu nào của Hoa là <strong>giả thuyết</strong>? b) Thời gian tan trung bình của hai cốc chênh nhau bao nhiêu phút? "
                    r"c) Chênh lệch đó so với sai số thế nào? d) Rút ra kết luận phù hợp.</p>")),
]

# ───────────── bảng phân tích đề ─────────────
ANALYSIS = [
 [("\"một nguyên tử đồng ... một phân tử nước\"", "Hai đối tượng (1), (4)", r"⚠ Vi mô và vĩ mô phân theo tiêu chí nào: mắt thường thấy được hay không?"),
  ("\"chiếc máy tính bảng ... Mặt Trăng\"", "Hai đối tượng (2), (3)", r"Vật quan sát được bằng mắt thường thuộc cấp độ nào?"),
  ("\"máy siêu âm khám thai\"", "Thiết bị (I)", r"Thiết bị phục vụ mục đích gì? Thuộc lĩnh vực nào trong năm lĩnh vực?"),
  ("\"đèn LED chiếu sáng cho rau trong nhà kính\"", "Thiết bị (II)", r"Đèn dùng cho việc gì? Lĩnh vực nào?"),
  ("\"kính hiển vi điện tử để nghiên cứu cấu trúc tế bào\"", "Thiết bị (III)", r"Dùng để làm gì? Lĩnh vực nào?")],
 [("\"Nam coi xe chạy đều ... tính $t = s/v$\"", "$s = 2{,}4\\ \\text{m}$, $v = 0{,}30\\ \\text{m/s}$", r"Dùng công thức và toán học để dự đoán: phương pháp nào?"),
  ("\"Hà ... bấm đồng hồ ba lần\"", "$8{,}6;\\ 8{,}7;\\ 8{,}5\\ \\text{s}$", r"Dùng phép đo thực tế: phương pháp nào? Dùng mấy lần đo để so sánh?"),
  ("\"Sai số của mỗi phép đo ... $\\pm 0{,}2\\ \\text{s}$\"", "$\\Delta t = 0{,}2\\ \\text{s}$",
   r"⚠ Hai số đo luôn khác nhau chút ít: chênh lệch chỉ có ý nghĩa khi so với đại lượng nào?"),
  ("\"lệch bao nhiêu so với kết quả Nam tính\"", "Cần tìm độ lệch", r"Giá trị trung bình của các lần đo trừ giá trị tính trước."),
  ("\"nhóm nên làm gì tiếp theo\"", "Độ lệch so với sai số", r"Nếu lệch vượt sai số thì gợi ý điều gì về mô hình của Nam? Bước nào của quy trình?")],
 [("\"Vì sao đá trong cốc kim loại tan nhanh hơn?\"", "Câu thứ nhất của Hoa", r"Câu hỏi thuộc bước nào của quy trình 5 bước?"),
  ("\"Chắc do kim loại truyền nhiệt ... nhanh hơn\"", "Câu thứ hai của Hoa", r"⚠ Lời đoán nguyên nhân chưa kiểm tra là bước nào? Phân biệt với quan sát và với kết luận."),
  ("\"cùng dung tích, cùng lượng đá, cùng chỗ\"", "Cách kiểm tra", r"Đặt như vậy để so sánh điều gì mà không bị yếu tố khác làm nhiễu?"),
  ("\"ba lần, sai số $\\pm 0{,}5$ phút\"", "Hai nhóm số đo", r"Tính gì từ ba lần đo của mỗi cốc? Chênh lệch giữa hai cốc so với sai số thế nào?"),
  ("\"Rút ra kết luận phù hợp\"", "Kết quả đo", r"Kết quả đo ủng hộ hay bác bỏ giả thuyết? Kết luận áp dụng đến đâu?")],
]

# ───────────── lời giải ─────────────
R1 = [r"<strong>Khái niệm:</strong> Vật lí nghiên cứu vận động của vật chất và năng lượng ở mọi cấp độ.",
      r"<strong>Phân cấp:</strong> vi mô — mắt thường không thấy (nguyên tử, phân tử); vĩ mô — mắt thường thấy được.",
      r"<strong>Ảnh hưởng của Vật lí:</strong> thông tin liên lạc, y tế, công nghiệp, nông nghiệp, nghiên cứu.",
      r"⚠ <strong>Điều kiện:</strong> phân loại theo việc mắt thường có thấy hay không, không theo cảm giác \"to\" hay \"nhỏ\"."]
R2 = [r"<strong>Phương pháp lí thuyết:</strong> dùng toán học và suy luận để dự đoán kết quả.",
      r"<strong>Phương pháp thực nghiệm:</strong> dùng thí nghiệm và phép đo để kiểm chứng.",
      r"<strong>Hai phương pháp bổ sung nhau:</strong> chênh lệch thì tìm nguyên nhân, không bỏ bên nào.",
      r"⚠ <strong>Điều kiện:</strong> chênh lệch chỉ có ý nghĩa khi lớn hơn sai số của phép đo; dự đoán chỉ đúng với điều đã đưa vào mô hình."]
R3 = [r"<strong>Quy trình 5 bước:</strong> quan sát → vấn đề → giả thuyết → kiểm tra → kết luận.",
      r"<strong>Giả thuyết:</strong> lời đoán nguyên nhân, chưa được kiểm tra; khác quan sát (điều thấy) và câu hỏi.",
      r"<strong>Sai số:</strong> chênh lệch lớn hơn sai số thì khác thật; trong phạm vi sai số thì chưa kết luận được.",
      r"⚠ <strong>Điều kiện:</strong> kết luận chỉ áp dụng cho điều kiện đã thử; giả thuyết bị bác bỏ vẫn là kết quả có giá trị."]

SOLS = [
 sol(R1, [
  ("Phân loại vi mô – vĩ mô", [P(r"Nguyên tử đồng (1) và phân tử nước (4) mắt thường không thấy: vi mô. Máy tính bảng (2) và Mặt Trăng (3) mắt thường thấy được: vĩ mô."),
                              A(r"T:Vi mô: (1), (4). Vĩ mô: (2), (3).")]),
  ("Máy siêu âm khám thai", [P(r"Thiết bị dùng để chẩn đoán, chăm sóc sức khoẻ con người:"), A(r"T:Lĩnh vực <strong>y tế</strong>.")]),
  ("Đèn LED cho rau trong nhà kính", [P(r"Ánh sáng nhân tạo giúp cây trồng phát triển:"), A(r"T:Lĩnh vực <strong>nông nghiệp</strong>.")]),
  ("Kính hiển vi điện tử", [P(r"Thiết bị quan sát cấu trúc rất nhỏ như tế bào để nghiên cứu: <strong>nghiên cứu</strong>. Cùng một môn Vật lí mà có mặt ở cả năm lĩnh vực, "
                              r"vì nó khám phá quy luật tổng quát của vật chất và năng lượng.")])],
  [r"a) Vi mô: (1), (4) · Vĩ mô: (2), (3)", r"b) (I) y tế · (II) nông nghiệp · (III) nghiên cứu"],
  r"Nhận dạng: đề hỏi <strong>cấp độ hoặc lĩnh vực ứng dụng</strong> → vi mô là mắt thường không thấy; thiết bị phục vụ việc gì thì thuộc lĩnh vực đó."),
 sol(R2, [
  ("Phân loại cách làm", [P(r"Nam dùng công thức để dự đoán trước khi đo: <strong>phương pháp lí thuyết</strong>. Hà dùng đồng hồ đo thực tế: <strong>phương pháp thực nghiệm</strong>.")]),
  ("Độ lệch giữa số đo và dự đoán", [P(r"Giá trị lí thuyết của Nam:"), M(r"t_{\text{LT}} = \dfrac{s}{v} = \dfrac{2{,}4}{0{,}30} = 8{,}0\ \text{s}"),
                                      P(r"Giá trị trung bình của Hà:"), M(r"\overline{t} = \dfrac{8{,}6 + 8{,}7 + 8{,}5}{3} = 8{,}6\ \text{s}"),
                                      M(r"\overline{t} - t_{\text{LT}} = 8{,}6 - 8{,}0"), A(r"0{,}6\ \text{s}")]),
  ("So độ lệch với sai số", [P(r"Sai số của phép đo là $0{,}2\ \text{s}$; ba lần đo của Hà đều nằm trong $\pm 0{,}2\ \text{s}$ quanh $8{,}6\ \text{s}$ nên nhất quán."),
                             A(r"T:Độ lệch $0{,}6\ \text{s}$ lớn hơn sai số $0{,}2\ \text{s}$: hai kết quả <strong>khác nhau thật</strong>.")]),
  ("Việc nên làm tiếp", [P(r"Độ lệch lớn hơn sai số cho thấy mô hình \"xe chạy đều\" của Nam bỏ sót yếu tố nào đó (ví dụ lúc đầu xe chưa đạt ngay $0{,}30\ \text{m/s}$). "
                             r"Không sửa số đo cho khớp, cũng không vứt công thức."),
                         A(r"T:Đoán nguyên nhân (giả thuyết) rồi thiết kế phép đo để kiểm tra.")])],
  [r"a) Nam: lí thuyết · Hà: thực nghiệm", r"b) Lệch $0{,}6\ \text{s}$ (số đo lớn hơn dự đoán)", r"c) Vượt sai số $0{,}2\ \text{s}$; nên đặt giả thuyết về yếu tố bị bỏ sót rồi đo kiểm tra"],
  r"Nhận dạng: đề cho <strong>kết quả tính trước và số đo</strong> → so độ lệch với sai số; vượt sai số thì tìm nguyên nhân, không bỏ bên nào."),
 sol(R3, [
  ("Nhận ra giả thuyết", [P(r"Hoa thấy đá tan nhanh hơn ở cốc kim loại: <em>quan sát</em>. Câu \"Vì sao ...?\": <em>vấn đề</em>. Câu \"Chắc do kim loại truyền nhiệt nhanh hơn\" "
                                r"là lời đoán nguyên nhân chưa kiểm tra:"), A(r"T:Đó là <strong>giả thuyết</strong>.")]),
  ("Chênh lệch thời gian tan", [P(r"Trung bình mỗi cốc:"), M(r"\overline{t}_{\text{kim loại}} = \dfrac{14{,}2 + 13{,}8 + 14{,}0}{3} = 14{,}0\ \text{phút}"),
                               M(r"\overline{t}_{\text{xốp}} = \dfrac{22{,}5 + 23{,}1 + 22{,}8}{3} = 22{,}8\ \text{phút}"),
                               M(r"\overline{t}_{\text{xốp}} - \overline{t}_{\text{kim loại}} = 22{,}8 - 14{,}0"), A(r"8{,}8\ \text{phút}")]),
  ("So chênh lệch với sai số", [P(r"Sai số mỗi lần đo là $0{,}5$ phút; các lần đo của mỗi cốc chỉ lệch quanh trung bình không quá $0{,}4$ phút."),
                                A(r"T:Chênh lệch $8{,}8$ phút lớn hơn rất nhiều sai số $0{,}5$ phút: hai cốc <strong>khác nhau thật</strong>.")]),
  ("Kết luận", [P(r"Kết quả đo khớp dự đoán \"cốc kim loại làm đá tan nhanh hơn\" nên giả thuyết được ủng hộ. Mới thử hai cốc nên kết luận chỉ áp dụng cho điều kiện đã thử."),
                A(r"T:Giả thuyết được ủng hộ; chưa thể nói \"đúng với mọi vật liệu\".")])],
  [r"a) \"Chắc do kim loại truyền nhiệt từ không khí vào đá nhanh hơn\"", r"b) $8{,}8$ phút", r"c) Lớn hơn nhiều so với sai số $0{,}5$ phút nên khác thật", r"d) Giả thuyết được ủng hộ trong điều kiện đã thử"],
  r"Nhận dạng: đề đi hết <strong>quy trình và có số đo kèm sai số</strong> → tìm lời đoán nguyên nhân, so chênh lệch với sai số, kết luận trong phạm vi đã thử."),
]

# ───────────── tự giải từng bước ─────────────
STEPS = [
 dict(nhan_dang=r"Thấy <b>vi mô, vĩ mô hoặc thiết bị ứng dụng</b> → xét <b>mắt thường thấy không</b> và <b>thiết bị phục vụ việc gì</b>",
      cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Phân loại vi mô – vĩ mô", "Trong bốn đối tượng (1), (2), (3), (4) có bao nhiêu đối tượng thuộc cấp độ vi mô?", dap_so=2, don_vi="", sai_so=0,
       loi=r"Xếp theo \"to hay nhỏ\" so với người: cho rằng máy tính bảng là vi mô vì nhỏ hơn Mặt Trăng rất nhiều."),
  buoc("Máy siêu âm khám thai", "Máy siêu âm khám thai thuộc lĩnh vực nào?", loi=r"Thấy từ \"máy\" và \"điện\" nên xếp vào công nghiệp, thay vì xét thiết bị phục vụ việc gì.",
       lua_chon=[(r"Y tế", True), (r"Công nghiệp", r"Công nghiệp là sản xuất, tự động hoá, robot; siêu âm khám thai phục vụ chăm sóc sức khoẻ."),
                 (r"Nghiên cứu khoa học", r"Nghiên cứu là các thiết bị khảo sát vật chất như kính hiển vi điện tử; siêu âm khám thai dùng để chẩn đoán bệnh nhân.")]),
  buoc("Đèn LED cho rau trong nhà kính", "Đèn LED chiếu sáng cho rau trong nhà kính thuộc lĩnh vực nào?", loi=r"Nghĩ đây là chuyện điện và ánh sáng nên xếp vào công nghiệp hoặc thông tin liên lạc.",
       lua_chon=[(r"Nông nghiệp", True), (r"Công nghiệp", r"Đèn dùng để trồng rau, giúp cây phát triển: đó là nông nghiệp, không phải sản xuất công nghiệp."),
                 (r"Thông tin liên lạc", r"Đèn ở đây chỉ chiếu sáng cho cây, không truyền thông tin.")]),
  buoc("Kính hiển vi điện tử", "Kính hiển vi điện tử dùng để nghiên cứu cấu trúc tế bào thuộc lĩnh vực nào?", loi=r"Thấy có tế bào nên xếp vào y tế.",
       lua_chon=[(r"Nghiên cứu", True), (r"Y tế", r"Đề nói dùng để nghiên cứu cấu trúc tế bào, chưa phải khám chữa bệnh cho người."),
                 (r"Thông tin liên lạc", r"Kính hiển vi không truyền thông tin.")])]),
 dict(nhan_dang=r"Thấy <b>kết quả tính trước và số đo thật</b> → nghĩ tới <b>so độ lệch với sai số</b>, rồi đặt giả thuyết",
      cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Phân loại cách làm", "Cách làm của Nam và của Hà thuộc phương pháp nào?", loi=r"Thấy Nam \"có số\" và Hà \"có dụng cụ\" nên xếp ngược hai phương pháp.",
       lua_chon=[(r"Nam: lí thuyết · Hà: thực nghiệm", True),
                 (r"Nam: thực nghiệm · Hà: lí thuyết", r"Nam chỉ tính bằng công thức, chưa đo gì: đó là lí thuyết; Hà đo trực tiếp bằng đồng hồ: đó là thực nghiệm."),
                 (r"Cả hai đều là thực nghiệm vì cùng ra con số", r"Có con số chưa chắc là thực nghiệm; thực nghiệm là phải đo thật bằng thí nghiệm.")]),
  buoc("Độ lệch giữa số đo và dự đoán", "Giá trị trung bình của Hà lệch bao nhiêu giây so với kết quả Nam tính?", dap_so=0.6, don_vi="s", sai_so=0.05,
       loi=r"Lấy lần đo lớn nhất, hoặc cộng ba lần đo rồi trừ giá trị tính trước, thay vì dùng giá trị trung bình.",
       ke=[(r"Tính giá trị trung bình của ba lần đo rồi trừ giá trị Nam tính", True),
           (r"Lấy lần đo lớn nhất trừ giá trị Nam tính", r"Một lần đo không đại diện cho cả ba; phải dùng giá trị trung bình."),
           (r"Cộng ba lần đo rồi trừ giá trị Nam tính", r"Tổng ba lần là thời gian của ba lượt chạy, không so được với thời gian một lượt.")]),
  buoc("So độ lệch với sai số", "Độ lệch này so với sai số của phép đo như thế nào?", loi=r"So độ lệch với chính giá trị 8 s rồi cho là \"nhỏ\", thay vì so với sai số của phép đo.",
       lua_chon=[(r"Lớn hơn sai số: hai kết quả khác nhau thật", True), (r"Nhỏ hơn sai số: hai kết quả như nhau", r"Sai số của phép đo nhỏ hơn độ lệch; ba lần đo của Hà còn nhất quán với nhau."),
                 (r"Không so được vì mỗi bạn dùng một phương pháp", r"Hai phương pháp bổ sung nhau chính vì ta so được kết quả của chúng.")],
       ke=[(r"So độ lệch với sai số của phép đo", True),
           (r"Chỉ cần xem hai số có khác nhau không", r"Hai số đo luôn khác nhau chút ít; chỉ khi chênh lệch vượt sai số mới kết luận khác thật."),
           (r"So độ lệch với giá trị tính trước", r"So với một thời gian dài thì chênh lệch nào cũng có vẻ nhỏ; chuẩn so là sai số của phép đo.")]),
  buoc("Việc nên làm tiếp", "Việc hợp lí nhất nhóm nên làm tiếp theo là gì?", loi=r"Sửa số đo cho khớp dự đoán, hoặc bỏ luôn công thức vì thấy lệch.",
       lua_chon=[(r"Đoán yếu tố mô hình bỏ sót (giả thuyết) rồi đo kiểm tra", True),
                 (r"Sửa số đo của Hà cho bằng kết quả Nam tính", r"Chỉnh số đo cho hợp dự đoán là làm sai kết quả thực nghiệm."),
                 (r"Bỏ công thức của Nam vì sai hoàn toàn", r"Công thức đúng với xe chạy đều; chênh lệch chỉ cho thấy mô hình còn thiếu yếu tố.")],
       ke=[(r"Từ độ lệch vượt sai số, đặt giả thuyết về yếu tố bị bỏ sót", True),
           (r"Đo thêm cho tới khi ra đúng kết quả Nam tính", r"Dừng khi ra đúng ý là chọn số liệu; các lần đo đã nhất quán với nhau."),
           (r"Kết luận ngay Hà đo sai", r"Ba lần đo đều nhất quán trong sai số, chưa có lí do coi là sai.")])]),
 dict(nhan_dang=r"Thấy <b>quy trình kèm số đo và sai số</b> → tìm <b>giả thuyết</b>, <b>so với sai số</b>, kết luận trong phạm vi thử",
      cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Nhận ra giả thuyết", "Câu nào của Hoa là giả thuyết?", loi=r"Chọn câu quan sát hoặc câu hỏi, vì cả ba câu đều nói về chuyện đá tan.",
       lua_chon=[(r"\"Chắc do kim loại truyền nhiệt từ không khí vào đá nhanh hơn.\"", True),
                 (r"\"Đá trong cốc kim loại tan nhanh hơn cốc xốp.\"", r"Đó là điều quan sát được, chưa phải lời đoán nguyên nhân."),
                 (r"\"Vì sao đá trong cốc kim loại tan nhanh hơn?\"", r"Đó là câu hỏi (đề xuất vấn đề); giả thuyết là lời đoán trả lời cho câu hỏi.")]),
  buoc("Chênh lệch thời gian tan", "Thời gian tan trung bình của hai cốc chênh nhau bao nhiêu phút?", dap_so=8.8, don_vi="phút", sai_so=0.1,
       loi=r"Trừ trực tiếp hai lần đo đầu, hoặc lấy tổng ba lần của mỗi cốc rồi trừ.",
       ke=[(r"Tính trung bình ba lần của mỗi cốc rồi lấy hiệu hai trung bình", True),
           (r"Lấy hiệu hai lần đo đầu tiên của hai cốc", r"Một lần đo mang sai số riêng; trung bình ba lần mới đại diện cho mỗi cốc."),
           (r"Cộng ba lần của mỗi cốc rồi lấy hiệu hai tổng", r"Hiệu hai tổng gấp ba lần chênh lệch thật, không phải thời gian tan của một lần.")]),
  buoc("So chênh lệch với sai số", "Chênh lệch giữa hai cốc so với sai số mỗi lần đo như thế nào?", loi=r"Cho rằng chênh vài phút là \"nhỏ\" rồi kết luận hai cốc như nhau.",
       lua_chon=[(r"Lớn hơn nhiều sai số: hai cốc khác nhau thật", True), (r"Nhỏ hơn sai số: chưa kết luận được", r"Chênh lệch giữa hai cốc lớn hơn nhiều sai số mỗi lần đo."),
                 (r"Chỉ ba lần đo nên chưa so được", r"Ba lần đo mỗi cốc nhất quán trong sai số, và chênh lệch giữa hai cốc lớn hơn nhiều sai số, nên đã đủ để thấy sự khác nhau.")],
       ke=[(r"So chênh lệch trung bình với sai số của mỗi lần đo", True),
           (r"So hai số đo của lần 1 của hai cốc", r"Một lần đo không đại diện; phải dùng giá trị trung bình."),
           (r"So chênh lệch với thời gian tan của cốc kim loại", r"Chuẩn so là sai số của phép đo, không phải thời gian tan.")]),
  buoc("Kết luận", "Kết luận nào phù hợp nhất với kết quả của Hoa?", loi=r"Kết luận quá rộng (\"mọi vật liệu\") hoặc cho rằng giả thuyết bị bác bỏ vì đá vẫn tan ở cốc xốp.",
       lua_chon=[(r"Giả thuyết được ủng hộ trong điều kiện đã thử (hai cốc này)", True),
                 (r"Giả thuyết đã được chứng minh đúng với mọi vật liệu", r"Mới thử hai cốc nên kết luận chỉ áp dụng cho điều kiện đã thử."),
                 (r"Giả thuyết bị bác bỏ vì đá vẫn tan ở cốc xốp", r"Giả thuyết nói đá tan nhanh hơn ở cốc kim loại, không nói đá không tan ở cốc xốp; số đo khớp dự đoán.")],
       ke=[(r"Đối chiếu kết quả đo với dự đoán của giả thuyết, rồi kết luận trong phạm vi đã thử", True),
           (r"Kết luận ngay rằng kim loại luôn truyền nhiệt tốt hơn mọi vật liệu", r"Thí nghiệm chỉ có hai cốc nên chưa đủ để khái quát cho mọi vật liệu."),
           (r"Làm lại thí nghiệm cho tới khi ra kết quả mong muốn", r"Dừng khi ra kết quả mong muốn là chọn số liệu; kết quả hiện có đã nhất quán.")])]),
]

write(J, 46, "Bài 1. Làm quen với Vật lí", DANG, BUILD, ANALYSIS, SOLS)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)

# chuỗi raw r"..." giữ nguyên dấu \" → bỏ gạch chéo thừa trong JSON
_t = open(J).read().replace('\\\\\\"', '\\"')
open(J, "w").write(_t)
