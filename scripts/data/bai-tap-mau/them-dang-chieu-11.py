"""Thêm vào bài tập mẫu lesson 11 (Lực từ. Cảm ứng từ) một dạng BÀI NGƯỢC bàn tay trái:
biết chiều lực từ → tìm chiều đường sức hoặc chiều dòng điện (3 trường hợp: B ⊥ hình, nam châm N–S, lực ⊗).
Vá 11.json TẠI CHỖ (không chạy lại build-hinh-11.py vì sẽ mất tom_de/cong_cu): chèn làm Dạng 2, đánh lại số các dạng sau.
Idempotent: xoá dạng có data-bt="dn-*" cũ trước khi chèn.
Chạy: python3 scripts/data/bai-tap-mau/them-dang-chieu-11.py"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from hinh_11 import *

J = os.path.join(HERE, "11.json")
T215 = "Quy tắc bàn tay trái, xác định phương chiều lực từ"
F = 16  # cỡ chữ nhãn chính (≥ 13 px ở 375 px, H4)


def dn(kk):
    b = ""
    # nhãn câu
    for x, t in ((70, "a)"), (210, "b)"), (350, "c)")):
        b += lbl(x, 24, t, "currentColor", F, "middle", "700")
    for x in (139, 281):
        b += seg(x, 36, x, 212, "currentColor", 1, "3 4", .4)
    # ── a) dây thẳng đứng, I lên, F sang phải, B ⊥ hình chưa biết
    ga = seg(62, 52, 62, 172, "currentColor", 6, "", .35) + arrow("dn", "o", 62, 160, 62, 70, 3)
    ga += lbl(52, 120, "I", ORG, F, "end", "700")
    ga += arrow("dn", "r", 66, 112, 116, 112, 3) + lbl(118, 104, "F", RED, F, "start", "700")
    if kk == 0:
        ga = (f'<g>{ga}<animateTransform attributeName="transform" type="translate" values="0 0;7 0" '
              f'dur="1.2s" begin="indefinite" fill="freeze"/></g>')
    b += ga + lbl(70, 206, "B: ⊙ hay ⊗?", BLUE, F, "middle", "700")
    # ── b) hai cực N (trái) – S (phải), dây ⊥ hình, F xuống, I chưa biết
    b += f'<rect x="146" y="58" width="16" height="118" rx="3" fill="#f87171" opacity=".55"/>'
    b += f'<rect x="258" y="58" width="16" height="118" rx="3" fill="#60a5fa" opacity=".55"/>'
    b += lbl(154, 50, "N", "currentColor", F, "middle", "700") + lbl(266, 50, "S", "currentColor", F, "middle", "700")
    gb = f'<circle cx="210" cy="104" r="12" fill="none" stroke="currentColor" stroke-width="2.2"/>'
    gb += lbl(210, 110, "?", ORG, F, "middle", "700")
    gb += arrow("dn", "r", 210, 118, 210, 166, 3) + lbl(223, 164, "F", RED, F, "start", "700")
    if kk == 0:
        gb = (f'<g>{gb}<animateTransform attributeName="transform" type="translate" values="0 0;0 7" '
              f'dur="1.2s" begin="indefinite" fill="freeze"/></g>')
    b += gb + lbl(210, 206, "I: ⊙ hay ⊗?", ORG, F, "middle", "700")
    # ── c) dây MN nằm ngang, B hướng xuống, F ⊗, I chưa biết
    for x in (314, 386):
        b += field_line(x, 48, x, 176, BLUE, 1.5, "6 4", 10)
    b += seg(306, 132, 394, 132, "currentColor", 6, "", .35)
    b += lbl(300, 138, "M", "currentColor", F, "end", "700") + lbl(400, 138, "N", "currentColor", F, "start", "700")
    b += sym_in(350, 98, 9, RED) + lbl(364, 104, "F", RED, F, "start", "700")
    b += lbl(350, 206, "I: M→N hay N→M?", ORG, 15, "middle", "700")
    cap_end = " Lực F: đỏ; dòng điện I: cam; đường sức: xanh, nét đứt. ⊙ hướng ra phía người nhìn, ⊗ hướng vào mặt phẳng hình. " + NOTE
    if kk == 0:
        return fig("dn-0", "0 0 420 218", "Ba trường hợp: dây thẳng đứng chịu lực sang phải; dây vuông góc hình giữa hai cực N và S chịu lực xuống; dây MN nằm ngang trong đường sức hướng xuống chịu lực hướng vào hình", b,
                   "Mô phỏng: dây ở a và b bị đẩy nhẹ theo chiều lực từ đã cho (ở c lực hướng vào hình nên không thấy dịch); dấu ? là chiều cần tìm." + cap_end)
    return fig("dn-2", "0 0 420 218", "Dữ kiện ba trường hợp, dấu hỏi ở chiều cần tìm", b, "Dữ kiện: mỗi câu biết hai chiều, tìm chiều còn lại." + cap_end)


PROBLEM = r"""<p>Trong mỗi trường hợp dưới đây, đoạn dây dẫn thẳng mang dòng điện đặt trong từ trường đều và chịu lực từ có chiều như đề cho. Các hướng "lên", "xuống", "sang trái", "sang phải" là hướng trong mặt phẳng hình vẽ; ⊙ là hướng ra phía người nhìn, ⊗ là hướng vào mặt phẳng hình.</p><ol type="a"><li>Dây thẳng đứng nằm trong mặt phẳng hình, dòng điện chạy từ dưới lên. Đường sức từ vuông góc với mặt phẳng hình. Lực từ tác dụng lên dây hướng sang phải. Đường sức từ hướng ra hay hướng vào mặt phẳng hình?</li><li>Dây đặt vuông góc với mặt phẳng hình, nằm giữa hai cực của một nam châm: cực N ở bên trái, cực S ở bên phải. Lực từ tác dụng lên dây hướng xuống. Dòng điện trong dây chạy ra hay chạy vào mặt phẳng hình?</li><li>Đoạn dây MN nằm ngang trong mặt phẳng hình (M bên trái, N bên phải), đường sức từ thẳng đứng hướng xuống. Lực từ tác dụng lên dây hướng vào mặt phẳng hình (⊗). Dòng điện chạy từ M đến N hay từ N đến M?</li></ol>"""

ANALYSIS = [
 ("\"Dây thẳng đứng … dòng điện chạy từ dưới lên\"", r"$I$ hướng lên", "Chiều từ cổ tay đến ngón tay là chiều dòng điện"),
 ("\"Lực từ … hướng sang phải\"", r"$\vec F$ sang phải", r"Ngón cái choãi $90^\circ$ chỉ chiều lực từ"),
 ("\"Đường sức từ vuông góc với mặt phẳng hình\"", r"$\vec B$ là ⊙ hoặc ⊗", r"⚠ Bàn tay trái chỉ dùng khi dây không song song đường sức; lực từ luôn vuông góc với cả dây và đường sức"),
 ("\"cực N ở bên trái, cực S ở bên phải\"", "Đường sức nằm ngang giữa hai cực", "Bên ngoài nam châm, đường sức đi ra từ cực nào, đi vào cực nào?"),
 ("\"Dây đặt vuông góc với mặt phẳng hình … lực từ hướng xuống\"", r"$\vec F$ hướng xuống; $I$ là ⊙ hoặc ⊗", "Lòng bàn tay đón đường sức, ngón cái theo chiều lực"),
 ("\"đường sức từ thẳng đứng hướng xuống … lực từ hướng vào mặt phẳng hình\"", r"$\vec B$ hướng xuống; $\vec F$ ⊗", "Muốn đón đường sức đi xuống, lòng bàn tay phải quay về phía nào? Ngón cái chỉ vào trang giấy thì bốn ngón tay nằm theo phương nào?"),
 ("\"hướng ra hay hướng vào … chạy từ M đến N hay từ N đến M?\"", r"Cần chiều $\vec B$ (a), chiều $I$ (b, c)", r"Biết hai trong ba chiều ($\vec B$, $I$, $\vec F$) thì suy ra chiều còn lại bằng bàn tay trái"),
]

RC = [r"<strong>Quy tắc bàn tay trái:</strong> đường sức xuyên vào lòng bàn tay, chiều từ cổ tay đến ngón tay là chiều $I$, ngón cái choãi $90^\circ$ chỉ chiều $\vec F$.",
      r"<strong>Dùng ngược:</strong> biết hai trong ba chiều thì đặt tay theo hai chiều đó, đọc ra chiều thứ ba.",
      r"<strong>Nam châm:</strong> bên ngoài nam châm, đường sức đi ra từ cực N, đi vào cực S.",
      r"⚠ <strong>Điều kiện:</strong> dây không song song đường sức; lực từ vuông góc với cả dây và đường sức."]

SOL = sol(RC, [
 ("Cách tìm chiều chưa biết", [P("Quy tắc bàn tay trái nối ba chiều: đường sức, dòng điện, lực từ. Biết hai chiều thì đặt tay theo hai chiều ấy."), A("T:Đặt tay theo hai chiều đã biết, đọc ra chiều thứ ba.")]),
 ("Chiều đường sức (câu a)", [P("Bàn tay trái: bốn ngón tay chỉ lên (chiều $I$), ngón cái chỉ sang phải (chiều $\\vec F$)."),
                              P("Khi đó lòng bàn tay quay vào trong trang giấy, ra xa người nhìn. Đường sức xuyên vào lòng bàn tay nên đi từ sau trang giấy ra phía người nhìn."),
                              A("T:Đường sức hướng ra khỏi mặt phẳng hình (⊙).")]),
 ("Chiều dòng điện (câu b)", [P("Giữa hai cực, đường sức đi từ N sang S, tức hướng sang phải."),
                              P("Lòng bàn tay trái quay sang trái để đón đường sức, ngón cái chỉ xuống. Khi đó bốn ngón tay chỉ vào trong trang giấy."),
                              A("T:Dòng điện chạy vào mặt phẳng hình (⊗).")]),
 ("Chiều dòng điện (câu c)", [P("Đường sức đi xuống nên lòng bàn tay trái ngửa lên để đón đường sức."),
                              P("Ngón cái chỉ vào trong trang giấy (chiều $\\vec F$). Khi đó bốn ngón tay chỉ sang phải."),
                              A("T:Dòng điện chạy từ M đến N.")]),
 ("Kiểm tra", [P("Đảo chiều vừa tìm ở mỗi câu thì bàn tay trái cho lực ngược với chiều đề cho, nên mỗi câu chỉ có một đáp án."),
               P("Ở cả ba câu, chiều đường sức, chiều dòng điện và chiều lực từ vuông góc nhau từng đôi một.")])],
 ["a) Đường sức hướng ra khỏi mặt phẳng hình (⊙)", "b) Dòng điện chạy vào mặt phẳng hình (⊗)", "c) Dòng điện chạy từ M đến N"],
 r"Nhận dạng: đề <strong>cho sẵn chiều lực từ</strong>, hỏi chiều dòng điện hoặc đường sức → <strong>dùng ngược bàn tay trái</strong>: đặt tay theo hai chiều đã biết, đọc chiều thứ ba.")

STEP = dict(
 nhan_dang=r"Thấy <b>cho chiều lực từ</b>, hỏi chiều <b>dòng điện</b> hoặc <b>đường sức</b> → bàn tay trái đặt theo hai chiều đã biết.",
 cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 3},
 buoc=[
  buoc("Cách tìm chiều chưa biết", "Đề cho chiều lực từ và chiều dòng điện, chưa biết chiều đường sức. Làm thế nào?",
       lua_chon=[("Đặt bàn tay trái theo chiều dòng điện và chiều lực, xem đường sức phải xuyên vào lòng bàn tay từ phía nào", True),
                 ("Dùng quy tắc nắm tay phải quanh dây để tìm đường sức", "Nắm tay phải cho đường sức do chính dòng điện trong dây sinh ra, không phải từ trường ngoài gây lực lên dây."),
                 ("Lấy chiều đường sức trùng chiều lực từ", "Lực từ luôn vuông góc với đường sức, không cùng chiều với nó.")],
       loi="Dùng nắm tay phải thay cho bàn tay trái, hoặc cho đường sức cùng chiều lực."),
  buoc("Chiều đường sức ở câu a", "Ở câu a, đường sức có chiều nào?",
       lua_chon=[("⊙ — hướng ra phía người nhìn", True),
                 ("⊗ — hướng vào mặt phẳng hình", r"Với đường sức ⊗ và dòng điện hướng lên, bàn tay trái cho lực sang trái, ngược với đề."),
                 ("Hướng lên, dọc theo dây", "Đường sức song song với dây thì lực từ bằng 0, không thể có lực sang phải.")],
       loi="Để đường sức đi vào mu bàn tay thay vì lòng bàn tay nên ra chiều ngược.",
       ke=[(r"Đặt bốn ngón tay theo chiều $I$, ngón cái theo chiều $\vec F$, xem lòng bàn tay quay về phía nào", True),
           (r"Dùng bàn tay phải: ngón cái theo $I$, bốn ngón khum lại", "Đó là quy tắc nắm tay phải, cho đường sức của chính dòng điện, không dùng cho lực từ."),
           (r"Đặt ngón cái theo chiều $I$, bốn ngón tay theo chiều $\vec F$", "Đổi vai hai ngón: bốn ngón tay chỉ chiều dòng điện, ngón cái chỉ chiều lực.")]),
  buoc("Chiều dòng điện ở câu b", "Ở câu b, dòng điện trong dây có chiều nào?",
       lua_chon=[("⊗ — chạy vào mặt phẳng hình", True),
                 ("⊙ — chạy ra phía người nhìn", "Với dòng điện ⊙ và đường sức đi từ N sang S, bàn tay trái cho lực hướng lên, ngược với đề."),
                 ("Sang phải, theo chiều đường sức", "Dây vuông góc mặt phẳng hình nên dòng điện chỉ có thể ⊙ hoặc ⊗; dòng điện dọc đường sức thì không có lực.")],
       loi="Cho đường sức giữa hai cực đi từ S sang N, nên lòng bàn tay quay ngược và ra chiều ngược.",
       ke=[(r"Xác định chiều đường sức giữa hai cực, rồi đặt lòng bàn tay đón đường sức, ngón cái theo $\vec F$", True),
           ("Lấy đường sức đi từ S sang N giữa hai cực", "Bên ngoài nam châm, đường sức đi ra từ cực N và đi vào cực S."),
           ("Đặt bốn ngón tay theo chiều lực từ", "Bốn ngón tay chỉ chiều dòng điện; chiều lực là ngón cái.")]),
  buoc("Chiều dòng điện ở câu c", "Ở câu c, dòng điện chạy theo chiều nào?",
       lua_chon=[("Từ M đến N", True),
                 ("Từ N đến M", "Với dòng điện từ N đến M và đường sức hướng xuống, bàn tay trái cho lực hướng ra phía người nhìn, ngược với đề."),
                 ("Không xác định được vì lực từ không nằm trong mặt phẳng hình", "Bàn tay trái vẫn dùng được khi ngón cái chỉ vào trang giấy.")],
       loi="Lúng túng khi ngón cái phải chỉ vào trang giấy, đặt tay lệch nên đọc ngược chiều bốn ngón tay.",
       ke=[("Lòng bàn tay đón đường sức đi xuống, ngón cái chỉ vào mặt phẳng hình, rồi đọc chiều bốn ngón tay", True),
           ("Ngón cái chỉ xuống theo đường sức, bốn ngón tay theo chiều lực", "Đường sức xuyên vào lòng bàn tay chứ không theo ngón cái; ngón cái là chiều lực."),
           ("Kết luận không có lực vì lực không nằm trong mặt phẳng hình", "Dây vuông góc đường sức nên có lực; lực vuông góc với cả dây và đường sức nên hướng ra hoặc vào mặt phẳng hình.")]),
  buoc("Kiểm tra"),
 ])

TOM_DE = {"cho": [r"a) dây thẳng đứng, $I$ hướng lên, $\vec F$ sang phải, $\vec B$ ⊥ mặt phẳng hình",
                  r"b) dây ⊥ mặt phẳng hình, giữa cực N (trái) và S (phải), $\vec F$ hướng xuống",
                  r"c) dây MN nằm ngang, $\vec B$ hướng xuống, $\vec F$ ⊗"],
          "tim": [r"a) chiều $\vec B$ (⊙ hay ⊗)", r"b) chiều $I$ (⊙ hay ⊗)", r"c) chiều $I$ (M → N hay N → M)"]}

NEW = dict(form="bai_tap", label="Dạng 2 · Trung bình · Bài ngược bàn tay trái: tìm chiều dòng điện hoặc chiều đường sức", topic=T215,
           problem_html=PROBLEM + dn(0), solution_html=SOL, analysis_html=dn(2) + tbl(ANALYSIS), tom_de=TOM_DE, **STEP)

d = json.load(open(J))
ds = [q for q in d["dang_bai"] if 'data-bt="dn-' not in q.get("problem_html", "")]
ds.insert(1, NEW)
k = 0
for q in ds:
    if re.match(r"Dạng \d+", q["label"]):
        k += 1
        q["label"] = re.sub(r"^Dạng \d+", f"Dạng {k}", q["label"])
d["dang_bai"] = ds
d["generated_at"] = "2026-11-05"
d["review"] = {"checked": True, "notes": "thêm Dạng 2 bài ngược bàn tay trái (them-dang-chieu-11.py); kiem-code tự giải 3/3 khớp, lựa chọn sai đều sai thật, không lộ đáp án; đã tô màu cực N/S, thêm vạch ngăn ô, dời nhãn F câu b"}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
print("ok", [q["label"][:40] for q in ds])
