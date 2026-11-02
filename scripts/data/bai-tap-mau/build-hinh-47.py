"""Bài tập mẫu bài 47 — Bài 2. Quy tắc an toàn trong phòng thực hành (Lớp 10). 3 dạng, dễ → khó.
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-47.py  → ghi scripts/data/bai-tap-mau/47.json (review.checked=false)
Chủ đề ngân hàng: 'Quy tắc an toàn trong phòng thực hành' (hầu như không có bài tập tính) → dạng định tính dùng lua_chon, một dạng có số đo."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

HERE = os.path.dirname(os.path.abspath(__file__))
J = os.path.join(HERE, "47.json")
VB = "0 0 420 200"
NOTE = "Hình minh hoạ, không theo tỉ lệ."
TOPIC = "Quy tắc an toàn trong phòng thực hành"
MUTE = "#94a3b8"

# ───────────── số liệu dạng 3 (tự kiểm) ─────────────
T_PHONG, SS = 25.0, 1.0
KC = [3, 8, 15, 30]; NHIET = [70.0, 33.0, 27.0, 25.5]
DT = [t - T_PHONG for t in NHIET]
assert DT == [45.0, 8.0, 2.0, 0.5]
GIAM_3_8 = DT[0] - DT[1]
assert GIAM_3_8 == 37.0
trong_ss = [k for k, d in zip(KC, DT) if d <= SS]
assert trong_ss == [30]                                   # chỉ 30 cm nằm trong sai số của nhiệt độ phòng
assert DT[2] > SS                                         # 15 cm vẫn nóng hơn phòng thật

# ───────────── Dạng 1: nhãn adapter ─────────────
def adapter(k):
    b = (f'<rect x="130" y="60" width="150" height="90" rx="8" fill="none" stroke="currentColor" stroke-width="2.5"/>'
         + lbl(205, 90, "BỘ SẠC", "currentColor", 14, "middle", "700")
         + seg(70, 105, 130, 105, "currentColor", 2.5) + seg(280, 105, 340, 105, "currentColor", 2.5)
         + lbl(100, 92, "IN", ORG, 13, "middle", "700") + lbl(310, 92, "OUT", ORG, 13, "middle", "700")
         + lbl(205, 118, "Input: 100–240 V ~", "currentColor", 12, "middle", "400")
         + lbl(205, 136, "Output: 5 V ⎓ 2 A", "currentColor", 12, "middle", "400"))
    b += (f'<circle cx="360" cy="105" r="18" fill="none" stroke="currentColor" stroke-width="2.5"/>'
          + lbl(360, 110, "M", "currentColor", 15, "middle", "700") + lbl(360, 150, "quạt mini 5 V DC", "currentColor", 12, "middle", "400"))
    b += lbl(40, 108, "ổ cắm", "currentColor", 12, "middle", "400")
    if k == 0:
        pts = [(70 + 270 * t / 30, 105) for t in range(31)]
        b += ball(pts, 0, 0.1)
        return fig("d1-0", VB, "Bộ sạc có nhãn Input và Output, nối với quạt mini ghi 5 V DC", b,
                   "Mô phỏng: điện đi từ ổ cắm vào Input, ra Output rồi tới quạt. " + NOTE)
    b += lbl(100, 40, "?", RED, 18, "middle", "700") + lbl(310, 40, "?", RED, 18, "middle", "700")
    return fig("d1-2", VB, "Bộ sạc: đầu vào và đầu ra cần xác định loại dòng điện", b, "Dữ kiện: nhãn bộ sạc và nhãn quạt. " + NOTE)

# ───────────── Dạng 2: bốn nhãn trên thùng ─────────────
def nhan(k):
    b = ""
    # (1) tam giác cảnh báo
    b += poly([(40, 120), (80, 50), (120, 120), (40, 120)], ORG, 3) + lbl(80, 108, "độc", ORG, 14, "middle", "700")
    # (2) tròn đỏ gạch chéo
    b += f'<circle cx="170" cy="85" r="34" fill="none" stroke="{RED}" stroke-width="4"/>' + seg(146, 61, 194, 109, RED, 4) + lbl(170, 132, "rác", "currentColor", 12, "middle", "600")
    # (3) tròn xanh
    b += f'<circle cx="260" cy="85" r="34" fill="none" stroke="{BLUE}" stroke-width="4"/>' + lbl(260, 90, "mặt nạ", BLUE, 12, "middle", "700")
    # (4) không khung: cốc vỡ
    b += '<path d="M330,60 L338,110 L372,110 L380,60" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linejoin="round"/>' + seg(340, 78, 354, 92, "currentColor", 2) + seg(354, 92, 346, 104, "currentColor", 2)
    names = [(80, "(1)"), (170, "(2)"), (260, "(3)"), (355, "(4)")]
    for x, s in names:
        b += lbl(x, 150, s, "currentColor", 14, "middle", "700")
    if k == 0:
        b += ball([(80, 40), (170, 40), (260, 40), (355, 40)], 0, 0.8)
        return fig("d2-0", VB, "Bốn nhãn trên thùng thu pin cũ: tam giác, tròn đỏ gạch chéo, tròn xanh và nhãn không khung", b,
                   "Bốn nhãn dán trên thùng; hình vẽ đơn giản hoá, chữ thay cho hình bên trong nhãn. " + NOTE)
    b += lbl(80, 175, "khung?", MUTE, 12, "middle", "400") + lbl(170, 175, "khung?", MUTE, 12, "middle", "400") + lbl(260, 175, "khung?", MUTE, 12, "middle", "400") + lbl(355, 175, "không khung", MUTE, 12, "middle", "400")
    return fig("d2-2", VB, "Bốn nhãn cần phân nhóm theo hình dạng và màu", b, "Dữ kiện: hình dạng và màu từng nhãn. " + NOTE)

# ───────────── Dạng 3: nhiệt độ theo khoảng cách ─────────────
def nhiet(k):
    X0, X1 = 70, 380
    pos = {3: 100, 8: 160, 15: 240, 30: 360}
    b = seg(60, 120, 400, 120, "currentColor", 2) + f'<ellipse cx="50" cy="104" rx="9" ry="14" fill="{ORG}" opacity="0.8"/>' + lbl(50, 146, "đèn cồn", "currentColor", 12, "middle", "400")
    for d in KC:
        x = pos[d]
        b += seg(x, 112, x, 128, "currentColor", 2) + lbl(x, 146, f"{d} cm", "currentColor", 12, "middle", "600")
    if k == 0:
        b += ball([(pos[d], 120) for d in KC], 0, 0.8)
        for d, t in zip(KC, NHIET):
            b += lbl(pos[d], 98, f"{t:g} °C".replace(".", ","), RED if t > 40 else BLUE, 13, "middle", "700")
        return fig("d3-0", VB, "Nhiệt độ đo được cách ngọn đèn cồn 3, 8, 15 và 30 cm", b, "Dữ kiện: nhiệt độ phòng 25 °C, sai số ±1 °C. " + NOTE)
    b += lbl(210, 60, "càng xa ngọn lửa, nhiệt độ càng giảm", MUTE, 12, "middle", "400")
    for d in KC:
        b += lbl(pos[d], 98, "?", RED, 16, "middle", "700")
    return fig("d3-2", VB, "Bốn vị trí đo, nhiệt độ cần so với nhiệt độ phòng", b, "Dữ kiện: các vị trí đo theo đề. " + NOTE)

BUILD = [adapter, nhan, nhiet]

# ───────────── đề ─────────────
DANG = [
 dict(label="Dạng 1 · Dễ · Đọc nhãn thiết bị: DC, AC, Input, Output, cực + và −", topic=TOPIC,
      problem_html=(r"<p>Một bộ sạc có nhãn: <strong>Input: 100–240 V ~</strong>; <strong>Output: 5 V ⎓ 2 A</strong> (dấu $⎓$ là dòng một chiều). "
                    r"Một quạt mini ghi <strong>5 V, DC</strong>; dây đỏ của quạt cần nối với cực mang dấu $+$ của bộ sạc.</p>"
                    r"<p>a) Đầu Input nhận dòng điện loại nào, đầu Output cấp dòng điện loại nào?</p>"
                    r"<p>b) Quạt mini nên nối vào đầu nào của bộ sạc?</p>"
                    r"<p>c) Quạt có phù hợp với bộ sạc không? Dây xanh của quạt nối với cực nào?</p>")),
 dict(label="Dạng 2 · Trung bình · Đọc kí hiệu cảnh báo qua hình dạng và màu, rồi biết phải làm gì", topic=TOPIC,
      problem_html=(r"<p>Một thùng thu pin cũ trong phòng chuẩn bị dán bốn nhãn: <strong>(1)</strong> tam giác viền vàng, hình đầu lâu bên trong; "
                    r"<strong>(2)</strong> vòng tròn đỏ gạch chéo, hình thùng rác bên trong; <strong>(3)</strong> vòng tròn xanh, hình mặt nạ phòng độc bên trong; "
                    r"<strong>(4)</strong> hình chiếc cốc vỡ, không có khung bao quanh.</p>"
                    r"<p>a) Xếp mỗi nhãn vào nhóm: cảnh báo, cấm, bắt buộc hay bảo quản. Có bao nhiêu nhãn có khung (không tính nhãn bảo quản)?</p>"
                    r"<p>b) Một học sinh định vứt pin cũ vào thùng rác thường. Điều đó có được phép không? Vì sao?</p>"
                    r"<p>c) Học sinh cần làm gì trước khi mở thùng ra kiểm tra?</p>")),
 dict(label="Dạng 3 · Khó · Giữ khoảng cách an toàn: đọc số đo, so với sai số và áp dụng quy tắc", topic=TOPIC,
      problem_html=(r"<p>Giáo viên đặt nhiệt kế cạnh ngọn đèn cồn đang cháy, lần lượt cách $3$; $8$; $15$; $30\ \text{cm}$ và đọc số chỉ khi đã ổn định. "
                    r"Nhiệt độ phòng là $25\ ^\circ\text{C}$, sai số mỗi số đọc là $\pm 1\ ^\circ\text{C}$ (số liệu minh hoạ).</p>"
                    r"<div class=\"table-scroll\"><table class=\"tl-table\"><thead><tr><th>Khoảng cách (cm)</th><th>3</th><th>8</th><th>15</th><th>30</th></tr></thead><tbody>"
                    r"<tr><td>Nhiệt độ ($^\circ\text{C}$)</td><td>70</td><td>33</td><td>27</td><td>25,5</td></tr></tbody></table></div>"
                    r"<p>a) Ở $3\ \text{cm}$, nhiệt độ cao hơn nhiệt độ phòng bao nhiêu? b) Từ $3\ \text{cm}$ ra $8\ \text{cm}$, phần nóng hơn nhiệt độ phòng giảm bao nhiêu? "
                    r"c) Trong bốn vị trí đã đo, vị trí gần đèn nhất nào có nhiệt độ không còn khác nhiệt độ phòng quá sai số? "
                    r"d) Quy tắc an toàn nào được minh hoạ và nhóm nên đứng thế nào khi đèn cồn đang cháy?</p>")),
]

# ───────────── bảng phân tích đề ─────────────
ANALYSIS = [
 [("\"Input: 100–240 V ~\"", "Dấu ~ ở đầu vào", r"⚠ Dấu $\sim$ và dấu $⎓$ chỉ hai loại dòng điện khác nhau: loại nào là xoay chiều, loại nào một chiều?"),
  ("\"Output: 5 V ⎓ 2 A\"", "Dấu ⎓ ở đầu ra", r"Output là nơi thiết bị cấp điện cho mạch hay nơi nhận điện từ ổ cắm?"),
  ("\"quạt mini ghi 5 V, DC\"", "Cần 5 V một chiều", r"Quạt cần loại dòng nào và mấy vôn? Đối chiếu với nhãn bộ sạc."),
  ("\"dây đỏ nối cực mang dấu +\"", "Dây đỏ ↔ cực $+$", r"Cực dương ghi dấu hoặc màu gì, cực âm ghi dấu hoặc màu gì?")],
 [("\"tam giác viền vàng, hình đầu lâu\"", "Nhãn (1)", r"⚠ Nhìn hình dạng và màu trước: tam giác thuộc nhóm nào?"),
  ("\"vòng tròn đỏ gạch chéo, hình thùng rác\"", "Nhãn (2)", r"Vòng tròn đỏ gạch chéo cho biết điều gì được phép hay không được phép?"),
  ("\"vòng tròn xanh, hình mặt nạ phòng độc\"", "Nhãn (3)", r"Vòng tròn xanh là nhóm nào: cho biết phải làm hay không được làm?"),
  ("\"hình chiếc cốc vỡ, không có khung\"", "Nhãn (4)", r"Nhãn không có khung riêng thuộc nhóm nào, nhận ra qua điều gì?"),
  ("\"định vứt pin cũ vào thùng rác thường\"", "Cần xét cho phép hay cấm", r"Đối chiếu với nhãn nào trong bốn nhãn? Có cho phép không?")],
 [("\"cách 3; 8; 15; 30 cm ... nhiệt độ phòng 25 °C\"", "Bốn số chỉ và mốc so sánh", r"Phần nóng hơn phòng ở mỗi vị trí tính thế nào?"),
  ("\"sai số mỗi số đọc là ±1 °C\"", "Ngưỡng $1\\ ^\\circ\\text{C}$", r"⚠ Số đọc chênh nhiệt độ phòng bao nhiêu thì chưa coi là nóng hơn phòng thật?"),
  ("\"bảng: 70; 33; 27; 25,5\"", "Bốn số chỉ ở bốn khoảng cách", r"Vị trí nào đầu tiên có chênh lệch trong ngưỡng sai số?"),
  ("\"nhóm nên đứng thế nào khi đèn đang cháy\"", "Áp dụng quy tắc", r"Nhóm quy tắc nào về nhiệt và tia? Rút ra điều gì từ số đo?")],
]

# ───────────── lời giải ─────────────
R1 = [r"<strong>DC / AC:</strong> DC (hoặc dấu $⎓$): một chiều; AC (hoặc dấu $\sim$): xoay chiều.",
      r"<strong>Input / Output:</strong> Input là đầu vào, nhận điện; Output là đầu ra, cấp điện cho mạch.",
      r"<strong>Cực:</strong> cực dương ghi $+$ hoặc màu đỏ; cực âm ghi $-$ hoặc màu xanh.",
      r"⚠ <strong>Điều kiện:</strong> phải khớp cả loại dòng, vị trí nối và số vôn trên nhãn dụng cụ."]
R2 = [r"<strong>Nhóm kí hiệu:</strong> tam giác là cảnh báo; tròn đỏ gạch chéo là cấm; tròn xanh là bắt buộc phải làm.",
      r"<strong>Nhóm bảo quản:</strong> thường không có khung riêng, nhận ra qua hình bên trong.",
      r"<strong>Cách đọc:</strong> nhìn hình dạng và màu trước, rồi mới xem hình bên trong.",
      r"⚠ <strong>Điều kiện:</strong> kí hiệu cấm nghĩa là không được làm; kí hiệu bắt buộc nghĩa là phải làm trước khi tiếp xúc."]
R3 = [r"<strong>Phần nóng hơn phòng:</strong> $\Delta T = T - T_{\text{phòng}}$.",
      r"<strong>Sai số:</strong> chênh lệch trong $\pm 1\ ^\circ\text{C}$ thì chưa kết luận được là khác nhiệt độ phòng.",
      r"<strong>Quy tắc:</strong> giữ khoảng cách an toàn khi nung nóng; không chạm vật nóng khi chưa có dụng cụ hỗ trợ.",
      r"⚠ <strong>Điều kiện:</strong> chỉ kết luận trong các vị trí đã đo; số đo minh hoạ cho xu hướng, không phải con số cố định ở mọi đèn."]

SOLS = [
 sol(R1, [
  ("Loại dòng ở Input và Output", [P(r"Input ghi dấu $\sim$: xoay chiều (AC), nhận điện từ ổ cắm. Output ghi dấu $⎓$: một chiều (DC), cấp điện cho mạch."), A(r"T:Input: xoay chiều · Output: một chiều.")]),
  ("Chỗ nối quạt", [P(r"Quạt là dụng cụ nhận điện từ bộ sạc nên nối vào đầu ra:"), A(r"T:Nối vào <strong>Output</strong>.")]),
  ("Đối chiếu nhãn quạt và bộ sạc", [P(r"Quạt cần 5 V một chiều; Output cấp $5\ \text{V}$ một chiều: khớp loại dòng và số vôn."),
                                    A(r"T:Phù hợp. Dây đỏ nối cực $+$ (đỏ), dây xanh nối cực $-$ (xanh).")])],
  [r"a) Input: xoay chiều (AC) · Output: một chiều (DC)", r"b) Output", r"c) Phù hợp; dây xanh nối cực âm ($-$)"],
  r"Nhận dạng: đề cho <strong>nhãn thiết bị</strong> → đọc loại dòng, vị trí nối, số vôn, rồi đối chiếu hai nhãn."),
 sol(R2, [
  ("Nhãn (1) và (2)", [P(r"Nhãn (1): hình tam giác là nhóm cảnh báo, hình đầu lâu là nguy hiểm đến sức khoẻ (chất độc). Nhãn (2): vòng tròn đỏ gạch chéo là nhóm cấm; hình thùng rác là không được bỏ vào thùng rác."), A(r"T:Nhãn (1) cảnh báo; nhãn (2) cấm.")]),
  ("Nhãn (3): bắt buộc", [P(r"Vòng tròn xanh là nhóm bắt buộc; hình mặt nạ phòng độc là phải đeo mặt nạ. Nhãn (4) không có khung, nhận ra qua hình cốc vỡ: dụng cụ dễ vỡ, nhóm bảo quản."), A(r"T:Nhãn (3) bắt buộc; nhãn (4) bảo quản.")]),
  ("Đếm nhãn có khung", [P(r"Nhãn có khung (cảnh báo, cấm, bắt buộc):"), M(r"(1),\ (2),\ (3)"), A(r"3 \text{ nhãn}")]),
  ("Vứt pin vào thùng rác thường", [P(r"Nhãn (2) cấm bỏ vào thùng rác: học sinh không được vứt pin cũ vào thùng rác thường. Trước khi mở thùng, theo nhãn (1) và (3) cần cẩn thận chất độc và đeo mặt nạ phòng độc."), A(r"T:Không được phép.")])],
  [r"a) (1) cảnh báo · (2) cấm · (3) bắt buộc · (4) bảo quản; có $3$ nhãn có khung", r"b) Không được phép: nhãn (2) cấm bỏ vào thùng rác", r"c) Đeo mặt nạ phòng độc (nhãn 3) và cẩn thận chất độc (nhãn 1)"],
  r"Nhận dạng: đề cho <strong>nhiều kí hiệu</strong> → nhìn hình dạng và màu để xếp nhóm, rồi nêu việc phải làm theo từng nhóm."),
 sol(R3, [
  ("Phần nóng hơn phòng ở 3 cm", [P(r"Lấy nhiệt độ đo trừ nhiệt độ phòng:"), M(r"\Delta T_3 = 70 - 25"), A(r"45\ ^\circ\text{C}")]),
  ("Giảm khi ra từ 3 cm đến 8 cm", [P(r"Ở $8\ \text{cm}$:"), M(r"\Delta T_8 = 33 - 25 = 8\ ^\circ\text{C}"), P(r"Phần nóng hơn phòng đã giảm:"), M(r"45 - 8"), A(r"37\ ^\circ\text{C}")]),
  ("Vị trí không còn khác phòng quá sai số", [P(r"Tính $\Delta T$ ở $15\ \text{cm}$ và $30\ \text{cm}$:"), M(r"\Delta T_{15} = 27 - 25 = 2\ ^\circ\text{C} > 1\ ^\circ\text{C}"),
                                              M(r"\Delta T_{30} = 25{,}5 - 25 = 0{,}5\ ^\circ\text{C} \le 1\ ^\circ\text{C}"), A(r"T:Vị trí gần nhất: $30\ \text{cm}$.")]),
  ("Áp dụng quy tắc", [P(r"Gần ngọn lửa rất nóng và giảm mạnh khi ra xa, đúng quy tắc <strong>giữ khoảng cách an toàn</strong> khi nung nóng. Số đo chỉ ở bốn vị trí; càng xa ngọn lửa càng bớt nóng, nên phải giữ khoảng cách khi đèn đang cháy."),
                       A(r"T:Giữ khoảng cách an toàn khi nung nóng.")])],
  [r"a) $45\ ^\circ\text{C}$", r"b) $37\ ^\circ\text{C}$", r"c) $30\ \text{cm}$ (còn $15\ \text{cm}$ vẫn nóng hơn phòng $2\ ^\circ\text{C}$)", r"d) Giữ khoảng cách an toàn khi nung nóng; không chạm vật nóng khi chưa có dụng cụ hỗ trợ"],
  r"Nhận dạng: đề cho <strong>số đo kèm sai số</strong> → tính chênh lệch với nhiệt độ phòng, so với sai số, rồi nêu quy tắc áp dụng."),
]

# ───────────── tự giải từng bước ─────────────
STEPS = [
 dict(nhan_dang=r"Thấy <b>nhãn thiết bị</b> → đọc <b>loại dòng, đầu nối, số vôn</b> rồi đối chiếu",
      cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Loại dòng ở Output", "Dấu ⎓ ở đầu Output cho biết dòng điện loại nào?", loi=r"Đọc chữ V rồi cho rằng đầu nào cũng như nhau.",
       lua_chon=[(r"Một chiều (DC)", True), (r"Xoay chiều (AC)", r"Dấu $\sim$ mới là xoay chiều; dấu $⎓$ (hoặc chữ DC) là một chiều."),
                 (r"Xoay chiều (AC) vì có chữ V", r"Chữ V là vôn, không nói loại dòng; dấu $⎓$ mới cho biết dòng một chiều.")]),
  buoc("Chỗ nối quạt", "Quạt mini nên nối vào đầu nào của bộ sạc?", loi=r"Thấy Input ghi nhiều vôn hơn nên cho rằng nối vào đó \"cho mạnh\".",
       lua_chon=[(r"Output", True), (r"Input", r"Input là chỗ bộ sạc nhận điện từ ổ cắm; nối quạt vào đó là sai chỗ."),
                 (r"Input, vì ghi nhiều vôn hơn", r"Input nhận điện từ ổ cắm; nối quạt 5 V vào đó là sai chỗ và nguy hiểm.")]),
  buoc("Quạt có phù hợp không", "Đối chiếu nhãn quạt 5 V DC với Output: dây xanh của quạt nối cực nào và quạt có phù hợp không?", loi=r"Chỉ so số vôn mà bỏ qua loại dòng điện, hoặc nối dây xanh vào cực đỏ.",
       lua_chon=[(r"Phù hợp; dây xanh nối cực âm", True),
                 (r"Phù hợp; dây xanh nối cực dương", r"Cực dương là cực đỏ hoặc ghi $+$; dây xanh nối cực âm."),
                 (r"Không phù hợp vì bộ sạc ghi 2 A", r"Số ampe trên nhãn là dòng tối đa bộ sạc cung cấp được; quạt chỉ lấy phần nó cần. Cùng 5 V một chiều là phù hợp.")])]),
 dict(nhan_dang=r"Thấy <b>nhiều kí hiệu</b> → nhìn <b>hình dạng và màu</b> trước để xếp nhóm, rồi nêu việc phải làm",
      cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Nhãn (2) thuộc nhóm nào", "Vòng tròn đỏ gạch chéo thuộc nhóm nào?", loi=r"Nhìn hình thùng rác trước, bỏ qua hình dạng và màu.",
       lua_chon=[(r"Cấm", True), (r"Cảnh báo", r"Cảnh báo là hình tam giác; vòng tròn đỏ gạch chéo là cấm."),
                 (r"Bắt buộc", r"Bắt buộc là vòng tròn xanh, không gạch chéo.")]),
  buoc("Nhãn (3) yêu cầu gì", "Vòng tròn xanh có hình mặt nạ phòng độc yêu cầu làm gì?", loi=r"Cho rằng vòng tròn nào cũng là cấm vì có hình tròn.",
       lua_chon=[(r"Phải đeo mặt nạ phòng độc", True), (r"Không được đeo mặt nạ khi mở thùng", r"Vòng tròn xanh là bắt buộc phải làm, không phải cấm."),
                 (r"Chỉ cần đeo nếu thấy mùi lạ", r"Kí hiệu bắt buộc nghĩa là phải làm trước khi mở, không đợi có mùi.")]),
  buoc("Đếm nhãn có khung", "Trong bốn nhãn, có bao nhiêu nhãn có khung (cảnh báo, cấm, bắt buộc)?", dap_so=3, don_vi="", sai_so=0,
       loi=r"Đếm theo số hình bên trong nhãn thay vì theo khung bao quanh."),
  buoc("Vứt pin vào thùng rác thường", "Học sinh định vứt pin cũ vào thùng rác thường. Việc đó có được phép không?", loi=r"Thấy chỉ là pin cũ nên cho rằng vứt vào thùng rác nào cũng được.",
       lua_chon=[(r"Không, theo nhãn (2)", True), (r"Được, vì pin cũ đã hết điện", r"Nhãn (2) cấm bỏ vào thùng rác; pin cũ vẫn có chất độc theo nhãn (1)."),
                 (r"Được nếu đeo mặt nạ", r"Mặt nạ là yêu cầu khi mở thùng (nhãn 3), không thay được lệnh cấm vứt vào thùng rác.")],
       ke=[(r"Đối chiếu việc định làm với nhãn cấm trên thùng", True),
           (r"Hỏi ý kiến bạn cùng nhóm", r"Bạn cùng nhóm không phải người quyết định; phải theo nhãn cấm trên thùng."),
           (r"Chỉ nhìn hình bên trong của nhãn (3)", r"Nhãn (3) nói về việc phải làm khi mở thùng; việc vứt pin phải xét theo nhãn cấm.")])]),
 dict(nhan_dang=r"Thấy <b>số đo kèm sai số</b> → tính <b>chênh lệch với nhiệt độ phòng</b>, so với sai số, rồi nêu quy tắc",
      cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Phần nóng hơn phòng ở 3 cm", "Ở 3 cm, nhiệt độ cao hơn nhiệt độ phòng bao nhiêu độ?", dap_so=45, don_vi="°C", sai_so=1,
       loi=r"Đọc nhầm số chỉ làm phần nóng hơn phòng."),
  buoc("Giảm khi ra từ 3 cm đến 8 cm", "Từ 3 cm ra 8 cm, phần nóng hơn phòng giảm bao nhiêu độ?", dap_so=37, don_vi="°C", sai_so=1,
       loi=r"Trừ hai số chỉ nhiệt độ rồi so với nhiệt độ phòng một lần nữa, hoặc dùng nhầm khoảng 8 cm và 15 cm.",
       ke=[(r"Lấy phần nóng hơn phòng ở 3 cm trừ phần ở 8 cm", True),
           (r"Lấy 70 trừ 33 rồi trừ thêm 25", r"Trừ nhiệt độ phòng một lần nữa làm lệch kết quả: 70 − 33 − 25 = 12 °C, không phải độ giảm."),
           (r"Lấy nhiệt độ ở 8 cm trừ nhiệt độ phòng", r"Đây chỉ là phần nóng hơn phòng ở 8 cm, chưa phải độ giảm giữa hai vị trí.")]),
  buoc("Vị trí không còn khác phòng quá sai số", "Trong bốn vị trí, vị trí gần đèn nhất nào có nhiệt độ không còn khác nhiệt độ phòng quá sai số ±1 °C?",
       loi=r"Chọn vị trí xa nhất chỉ vì \"càng xa càng mát\", không so chênh lệch với sai số; hoặc coi 27 °C là bằng phòng.",
       lua_chon=[(r"30 cm", True), (r"15 cm", r"Ở 15 cm chênh lệch là 2 °C, lớn hơn sai số 1 °C: vẫn nóng hơn phòng thật."),
                 (r"8 cm", r"Ở 8 cm chênh lệch là 8 °C, còn nóng hơn phòng rõ rệt.")],
       ke=[(r"Tính chênh lệch với nhiệt độ phòng ở từng vị trí rồi so với sai số 1 °C", True),
           (r"Chọn vị trí có nhiệt độ thấp nhất", r"Nhiệt độ thấp nhất là câu trả lời cho \"xa nhất\", nhưng đề hỏi vị trí gần nhất mà vẫn trong sai số."),
           (r"Chọn vị trí có nhiệt độ bằng đúng 25 °C", r"Không có số chỉ nào đúng bằng 25 °C; cần so với sai số.")]),
  buoc("Áp dụng quy tắc", "Từ các số đo, nhóm nên làm gì khi đèn cồn đang cháy?", loi=r"Cho rằng chỉ nóng khi chạm vào ngọn lửa, đứng gần quan sát thì không sao.",
       lua_chon=[(r"Đứng xa ngọn lửa, không chạm vật nóng", True),
                 (r"Đứng cách 8 cm để vẫn nhìn rõ", r"Ở 8 cm vẫn nóng hơn phòng 8 °C: chưa đủ xa."),
                 (r"Đứng sát ngọn lửa rồi dùng kẹp là đủ an toàn", r"Kẹp giúp tay không chạm vật nóng nhưng không thay được việc giữ khoảng cách; ở 3 cm nóng hơn phòng 45 °C.")],
       ke=[(r"Áp dụng quy tắc giữ khoảng cách an toàn khi nung nóng", True),
           (r"Coi số đo là cố định ở mọi đèn cồn", r"Số đo chỉ cho xu hướng của thí nghiệm này; mỗi đèn có thể khác."),
           (r"Bỏ qua quy tắc vì chỉ cháy một lúc", r"Quy tắc áp dụng suốt thời gian nung nóng, dù chỉ ngắn.")])]),
]

write(J, 47, "Bài 2. Quy tắc an toàn trong phòng thực hành", DANG, BUILD, ANALYSIS, SOLS)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)

_t = open(J).read().replace('\\\\\\"', '\\"')
open(J, "w").write(_t)
