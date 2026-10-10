# Phần B: Bài 4, 5, 6 của bộ 12 bài tự luận Cơ học HSG -> part-B.json (lesson 167)
import json, math, pathlib, re
SRC = pathlib.Path("/Users/MAC/Documents/THPT/Lop09/00_Dung_chung/HSG_KHTN9_Vat_li/01_Chuyen_de/Bai_tap_tu_luan_Co_hoc_VD-VDC/sinh-bai-tap.py")
HERE = pathlib.Path(__file__).parent

# --- lấy hàm hình từ nguồn, thay mũi tên marker bằng chữ V 30° ---
src = SRC.read_text().split("# ---------------- hình ----------------")
ns = {"math": math, "__file__": str(SRC)}
head = src[0].replace("from sach_mau import dung, tieu_de, muc", "")
exec(head, ns)
def L(x1, y1, x2, y2, w=1.5, d=None, m=False, ms=False):
    a = f' stroke-dasharray="{d}"' if d else ''
    out = f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke-width="{w}"{a}/>'
    def chev(tx, ty, fx, fy):
        ang = math.atan2(ty - fy, tx - fx); s = 8
        pts = []
        for da in (math.radians(150), math.radians(-150)):
            pts.append((tx + s * math.cos(ang + da), ty + s * math.sin(ang + da)))
        return "".join(f'<line x1="{tx:.1f}" y1="{ty:.1f}" x2="{px:.1f}" y2="{py:.1f}" stroke-width="{w}"/>' for px, py in pts)
    if m: out += chev(x2, y2, x1, y1)
    if ms: out += chev(x1, y1, x2, y2)
    return out
ns["L"] = L
exec("def _f():\n pass", ns)
body = "# ---------------- hình ----------------" + src[1]
body = body.split("g = 10")[0]   # chỉ phần hàm fig_*
exec(body, ns)
def fig(svg, cap):
    svg = re.sub(r'width="(\d+)" height="\d+"', r'width="\1" style="max-width:100%;height:auto"', svg, count=1)
    assert "marker-end" not in svg and "marker-start" not in svg
    return f'<figure class="fig">{svg}<figcaption>{cap}</figcaption></figure>'

def fm(x, nd=2):
    s = f"{x:.{nd}f}".rstrip("0").rstrip(".")
    return s.replace(".", "{,}")

# ---------------- số liệu ----------------
g = 10
# Bài 4
t1, t2, S, L2, v2 = 10, 50, 400, 150, 8
v4 = S / (t2 - t1); L4 = v4 * t1
vtd_n = v4 + v2; t_n = (L4 + L2) / vtd_n
vtd_c = v4 - v2; t_c = (L4 + L2) / vtd_c
assert (v4, L4, vtd_n, vtd_c, t_c) == (10, 100, 18, 2, 125) and abs(t_n - 13.8889) < 1e-3
# Bài 5
AB, m5, OA, PA = 1.2, 2, 0.4, 50
P5 = g * m5; OB = AB - OA; OG = AB / 2 - OA
F5 = (PA * OA - P5 * OG) / OB; N5 = PA + P5 + F5; OC = P5 * OG / PA
assert (P5, round(OG, 3), round(F5, 3), round(N5, 3), round(OC * 100, 3)) == (20, 0.2, 20, 90, 8)
# Bài 6
m6, l6, h6, H6 = 60, 4, 1, 0.8
P6 = g * m6; F0 = P6 * h6 / l6; F0r = F0 / 2; Fdoc = P6 * h6 / (H6 * l6); Fms = Fdoc - F0; Fr = Fdoc / 2
sday = 2 * l6; A6 = Fr * sday; Aich = P6 * h6; Hhe = Aich / A6
assert (P6, F0, F0r, Fdoc, Fms, Fr, sday, A6, Hhe) == (600, 150, 75, 187.5, 37.5, 93.75, 8, 750, 0.8)

# ---------------- helper HTML ----------------
def box(lines):
    li = "".join(f"<li>{x}</li>" for x in lines)
    return f'<div class="tl-box"><p class="tl-label">Kiến thức cần gọi lại</p><ol>{li}</ol></div>'
def step(n, title, parts, ans=None, tail=None):
    h = f'<div class="bt-step"><p class="bt-step-title"><span class="bt-step-n">{n}</span><span>{title}</span></p>'
    for p in parts:
        h += p if p.startswith("$$") else f"<p>{p}</p>"
    if ans: h += f'<div class="bt-ans">$${ans}$$</div>'
    if tail:
        for p in tail: h += p if p.startswith("$$") else f"<p>{p}</p>"
    return h + "</div>"
def final(lines):
    return '<div class="bt-final"><p><strong>Đáp số</strong></p>' + "".join(f"<p>{x}</p>" for x in lines) + "</div>"
def table(rows):
    h = '<div class="table-scroll"><table class="tl-table tl-table--data"><thead><tr><th>Câu trong đề</th><th>Dữ liệu</th><th>Kiến thức liên quan</th></tr></thead><tbody>'
    for a, b, c in rows: h += f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>"
    return h + "</tbody></table></div>"
def ch(text, ok, why=None):
    d = {"text": text, "dung": ok}
    if not ok: d["vi_sao"] = why
    return d
def buoc(tieu_de, hoi, loi, dap=None, sai=None, don_vi=None, lua=None, chon=None):
    b = {"tieu_de": tieu_de, "hoi": hoi}
    if lua: b["lua_chon"] = lua
    else: b.update({"dap_so": dap, "sai_so": sai, "don_vi": don_vi})
    b["loi_hay_gap"] = loi
    if chon: b["chon_buoc_ke"] = chon
    return b
def check_step(tieu_de, parts):  # bước không có câu hỏi
    return step(None, tieu_de, parts)

# ================= BÀI 4 =================
p4 = ('<p>Một đoàn tàu chuyển động thẳng đều. Tàu chạy qua một cột điện (từ lúc đầu tàu tới cột đến lúc đuôi tàu rời cột) hết $10\\ \\text{s}$; '
      'chạy qua một cây cầu dài $400\\ \\text{m}$ (từ lúc đầu tàu lên cầu đến lúc đuôi tàu rời cầu) hết $50\\ \\text{s}$.</p>'
      '<ol type="a"><li>Tính chiều dài $L$ và tốc độ $v$ của đoàn tàu.</li>'
      '<li>Tàu gặp một đoàn tàu khác dài $150\\ \\text{m}$ chạy ngược chiều với tốc độ $8\\ \\text{m/s}$. Hai tàu lướt qua nhau (từ lúc hai đầu tàu gặp nhau đến lúc hai đuôi tàu rời nhau) trong bao lâu?</li>'
      '<li>Nếu tàu thứ hai chạy cùng chiều với tốc độ $8\\ \\text{m/s}$, tàu thứ nhất vượt qua nó mất bao lâu?</li></ol>'
      + fig(ns["fig_tau"](), "Đoàn tàu, cầu dài $400\\ \\text{m}$ và cột điện"))
a4 = table([
  ("\"chạy qua một cột điện … hết $10$ s\"", "$t_1=10$ s", "⚠ Cột điện coi là một điểm : đầu tàu chỉ đi đúng chiều dài tàu, $L=v\\,t_1$"),
  ("\"cầu dài $400$ m … từ lúc đầu tàu lên cầu đến lúc đuôi tàu rời cầu hết $50$ s\"", "$S=400$ m ; $t_2=50$ s", "⚠ Đầu tàu đi thêm cả chiều dài tàu : $L+S=v\\,t_2$"),
  ("\"Tính chiều dài $L$ và tốc độ $v$\"", "Cần tìm $L$, $v$", "Hai phương trình hai ẩn, trừ vế với vế : $S=v\\,(t_2-t_1)$"),
  ("\"đoàn tàu khác dài $150$ m ngược chiều $8$ m/s\"", "$L_2=150$ m ; $v_2=8$ m/s", "Ngược chiều : $v_{\\text{tđ}}=v+v_2$ ; quãng đường tương đối $s_{\\text{tđ}}=L+L_2$"),
  ("\"từ lúc hai đầu tàu gặp nhau đến lúc hai đuôi tàu rời nhau\"", "Cần tìm $t$", "$t=\\dfrac{L+L_2}{v_{\\text{tđ}}}$"),
  ("\"cùng chiều … tàu thứ nhất vượt qua\"", "Cùng chiều, $v\\gt v_2$", "⚠ Cùng chiều : $v_{\\text{tđ}}=v-v_2$ (chỉ vượt được khi $v\\gt v_2$) ; $s_{\\text{tđ}}=L+L_2$"),
])
s4 = box([
  "<strong>Điểm chuẩn :</strong> theo dõi đầu tàu ; quãng đường đầu tàu đi được là quãng đường của cả sự kiện.",
  "<strong>Qua cột điện :</strong> $s=L$ ; <strong>qua cầu :</strong> $s=L+S$ ; <strong>qua tàu khác :</strong> $s_{\\text{tđ}}=L+L_2$.",
  "Ngược chiều : $v_{\\text{tđ}}=v+v_2$ ; cùng chiều : $v_{\\text{tđ}}=v-v_2$.",
  "⚠ <strong>Điều kiện :</strong> mốc đầu và mốc cuối phải là hai đầu tàu gặp nhau và hai đuôi tàu rời nhau.",
])
s4 += step(1, "Tốc độ của đoàn tàu", [
  "Qua cột : đầu tàu đi đúng $L$ trong $10\\ \\text{s}$, nên $L=v\\cdot10$.",
  "Qua cầu : đầu tàu đi $L+400$ trong $50\\ \\text{s}$, nên $L+400=v\\cdot50$.",
  "Trừ vế với vế để khử $L$ :", "$$400=v\\,(50-10)$$", "$$v=\\dfrac{400}{50-10}$$"], f"v={fm(v4)}\\ \\text{{m/s}}")
s4 += step(2, "Chiều dài đoàn tàu", [
  "Dùng phương trình qua cột điện :", "$$L=v\\,t_1$$", f"$$L={fm(v4)}\\times10$$"], f"L={fm(L4)}\\ \\text{{m}}")
s4 += step(3, "Tốc độ tương đối khi ngược chiều", [
  "Hai tàu chạy ngược chiều nên khoảng cách giữa chúng rút ngắn bằng tổng hai tốc độ :", "$$v_{\\text{tđ}}=v+v_2$$", f"$$v_{{\\text{{tđ}}}}={fm(v4)}+8$$"], f"v_{{\\text{{tđ}}}}={fm(vtd_n)}\\ \\text{{m/s}}")
s4 += step(4, "Thời gian lướt qua nhau (ngược chiều)", [
  "Từ lúc hai đầu tàu gặp nhau đến lúc hai đuôi tàu rời nhau, phần đã lướt qua nhau là tổng hai chiều dài :", "$$s_{\\text{tđ}}=L+L_2$$", f"$$s_{{\\text{{tđ}}}}={fm(L4)}+150={fm(L4+L2)}\\ \\text{{m}}$$",
  "$$t=\\dfrac{s_{\\text{tđ}}}{v_{\\text{tđ}}}$$", f"$$t=\\dfrac{{{fm(L4+L2)}}}{{{fm(vtd_n)}}}$$"], f"t\\approx{fm(t_n,1)}\\ \\text{{s}}")
s4 += step(5, "Tốc độ tương đối khi cùng chiều", [
  "Cùng chiều thì tàu sau chỉ đuổi kịp bằng phần tốc độ hơn :", "$$v_{\\text{tđ}}=v-v_2$$", f"$$v_{{\\text{{tđ}}}}={fm(v4)}-8$$"], f"v_{{\\text{{tđ}}}}={fm(vtd_c)}\\ \\text{{m/s}}")
s4 += step(6, "Thời gian vượt (cùng chiều)", [
  "Từ lúc đầu tàu thứ nhất ngang đuôi tàu thứ hai đến lúc đuôi tàu thứ nhất ngang đầu tàu thứ hai, quãng đường tương đối vẫn là $L+L_2$ :", "$$t=\\dfrac{L+L_2}{v-v_2}$$", f"$$t=\\dfrac{{{fm(L4+L2)}}}{{{fm(vtd_c)}}}$$"], f"t={fm(t_c)}\\ \\text{{s}}")
s4 += step(7, "Kiểm tra", [
  f"Cùng chiều lâu hơn ngược chiều (${fm(t_c)}\\ \\text{{s}}\\gt{fm(t_n,1)}\\ \\text{{s}}$) vì hai tàu lại gần nhau chậm hơn nhiều.",
  f"Đổi lại : ${fm(t_n,1)}\\ \\text{{s}}\\times{fm(vtd_n)}\\ \\text{{m/s}}\\approx{fm(L4+L2)}\\ \\text{{m}}=L+L_2$ ✓.",
  "Nếu lấy quãng đường qua cầu chỉ là $400\\ \\text{m}$ sẽ ra $v=8\\ \\text{m/s}$, ngắn hơn thực tế vì quên chiều dài tàu."])
s4 = '<div class="bt-sol">' + s4 + final([f"a) $v={fm(v4)}\\ \\text{{m/s}}$ ; $L={fm(L4)}\\ \\text{{m}}$", f"b) $t\\approx{fm(t_n,1)}\\ \\text{{s}}$", f"c) $t={fm(t_c)}\\ \\text{{s}}$"]) + \
      '<p class="bt-note">Nhận dạng: thấy <strong>tàu có chiều dài qua cột, cầu, tàu khác</strong> → quãng đường cộng thêm chiều dài cần vượt ; <strong>ngược chiều</strong> cộng tốc độ, <strong>cùng chiều</strong> trừ tốc độ.</p></div>'
b4 = [
 buoc("Tốc độ của đoàn tàu", "Tốc độ $v$ của đoàn tàu bằng bao nhiêu?", "Lấy $v=\\dfrac{400}{50}$ vì coi tàu đi đúng chiều dài cầu, quên rằng đầu tàu còn phải đi thêm chiều dài tàu.", v4, 0.1, "m/s"),
 buoc("Chiều dài đoàn tàu", "Chiều dài $L$ của đoàn tàu bằng bao nhiêu?", "Lấy $L=400\\ \\text{m}$ (nhầm với chiều dài cầu) hoặc dùng $t_2$ thay cho $t_1$.", L4, 1, "m",
      chon=[ch("Qua cột điện đầu tàu đi đúng chiều dài tàu : $L=v\\,t_1$", True),
            ch("$L=v\\,t_2$ (dùng thời gian qua cầu)", False, "Trong thời gian qua cầu, đầu tàu đi $L+S$ chứ không chỉ $L$."),
            ch("$L$ bằng chiều dài cầu", False, "Chiều dài cầu và chiều dài tàu là hai đại lượng độc lập ; đề không nói chúng bằng nhau.")]),
 buoc("Tốc độ tương đối khi ngược chiều", "Hai tàu ngược chiều lại gần nhau với tốc độ (so với nhau) bằng bao nhiêu?", "Trừ hai tốc độ như khi cùng chiều, hoặc lấy trung bình cộng của hai tốc độ.", vtd_n, 0.1, "m/s",
      chon=[ch("Ngược chiều thì cộng : $v_{\\text{tđ}}=v+v_2$", True),
            ch("Ngược chiều thì trừ : $v_{\\text{tđ}}=v-v_2$", False, "Trừ tốc độ là trường hợp cùng chiều ; ngược chiều thì hai tàu cùng góp vào việc rút ngắn khoảng cách."),
            ch("Lấy trung bình : $v_{\\text{tđ}}=\\dfrac{v+v_2}{2}$", False, "Không có lí do chia đôi ; khoảng cách giảm bằng tổng hai tốc độ mỗi giây.")]),
 buoc("Thời gian lướt qua nhau (ngược chiều)", "Hai tàu lướt qua nhau (hai đầu gặp nhau đến hai đuôi rời nhau) mất bao lâu ?", "Chỉ tính chiều dài tàu thứ hai, hoặc chia tổng chiều dài cho tốc độ riêng của tàu mình.", round(t_n, 1), 0.1, "s",
      chon=[ch("Chia tổng chiều dài hai tàu cho tốc độ tương đối : $t=\\dfrac{L+L_2}{v_{\\text{tđ}}}$", True),
            ch("$t=\\dfrac{L_2}{v_{\\text{tđ}}}$", False, "Hai đuôi chỉ rời nhau khi cả hai đoàn tàu đã lướt qua nhau, phải tính cả $L$ lẫn $L_2$."),
            ch("$t=\\dfrac{L+L_2}{v}$ (dùng tốc độ tàu mình)", False, "Tàu kia cũng chuyển động nên tốc độ lướt qua nhau phải là tốc độ tương đối.")]),
 buoc("Tốc độ tương đối khi cùng chiều", "Cùng chiều, tàu thứ nhất đuổi tàu thứ hai với tốc độ (so với nhau) bằng bao nhiêu?", "Cộng hai tốc độ như câu ngược chiều.", vtd_c, 0.1, "m/s",
      chon=[ch("Cùng chiều thì trừ : $v_{\\text{tđ}}=v-v_2$", True),
            ch("Cùng chiều thì cộng : $v_{\\text{tđ}}=v+v_2$", False, "Cộng là trường hợp ngược chiều ; cùng chiều tàu sau chỉ đuổi kịp bằng phần tốc độ hơn."),
            ch("$v_{\\text{tđ}}=v_2-v$", False, "Tàu thứ nhất nhanh hơn nên phải lấy tốc độ lớn trừ tốc độ nhỏ, nếu không ra tốc độ âm.")]),
 buoc("Thời gian vượt (cùng chiều)", "Tàu thứ nhất vượt hết tàu thứ hai mất bao lâu?", "Dùng lại tốc độ tương đối của câu ngược chiều, hoặc chỉ tính chiều dài tàu mình.", t_c, 1, "s",
      chon=[ch("$t=\\dfrac{L+L_2}{v-v_2}$", True),
            ch("$t=\\dfrac{L+L_2}{v+v_2}$ (dùng lại kết quả câu trước)", False, "Cùng chiều tốc độ tương đối là hiệu, không phải tổng."),
            ch("$t=\\dfrac{L}{v-v_2}$", False, "Đuôi tàu thứ nhất phải qua đầu tàu thứ hai, nên quãng đường tương đối gồm cả $L_2$.")]),
 {"tieu_de": "Kiểm tra", "chon_buoc_ke": [
    ch("So sánh hai thời gian và đổi lại : thời gian × tốc độ tương đối = tổng chiều dài", True),
    ch("Không cần kiểm tra vì phép tính đơn giản", False, "Kiểm tra đổi lại bắt được lỗi cộng trừ tốc độ và quên chiều dài tàu."),
    ch("Chỉ kiểm tra đơn vị giây", False, "Đúng đơn vị chưa chắc đúng số ; phải đối chiếu với tổng chiều dài.")]} ,
]
b4[-1].pop("chon_buoc_ke")  # bước kiểm tra không hỏi, không cần chọn bước kế

# ================= BÀI 5 =================
p5 = ('<p>Thanh $AB$ đồng chất, tiết diện đều, dài $1{,}2\\ \\text{m}$, khối lượng $2\\ \\text{kg}$, đặt trên điểm tựa $O$ với $OA=0{,}4\\ \\text{m}$. '
      'Treo tại đầu $A$ một vật có trọng lượng $50\\ \\text{N}$. Lấy $g=10\\ \\text{N/kg}$.</p>'
      '<ol type="a"><li>Để thanh cân bằng nằm ngang, phải tác dụng vào đầu $B$ một lực $F$ theo phương thẳng đứng. $F$ hướng lên hay hướng xuống ? Tính $F$.</li>'
      '<li>Tính lực mà điểm tựa $O$ tác dụng lên thanh khi đó.</li>'
      '<li>Bỏ lực $F$. Phải dời vật $50\\ \\text{N}$ tới điểm $C$ nào trên thanh để thanh tự cân bằng nằm ngang ? Tính $OC$ và cho biết $C$ nằm về phía $A$ hay phía $B$.</li></ol>'
      + fig(ns["fig_thanh"](), "Thanh $AB$ tựa trên $O$, vật $50\\ \\text{N}$ ở $A$, lực $F$ ở $B$"))
a5 = table([
  ("\"Thanh $AB$ đồng chất, dài $1{,}2$ m, khối lượng $2$ kg\"", "$AB=1{,}2$ m ; $m=2$ kg", "⚠ Thanh có khối lượng nên có trọng lượng $P=10m$ đặt tại trung điểm $G$ (mở rộng ngoài chuẩn KHTN 9 : mômen của thanh có khối lượng)"),
  ("\"đặt trên điểm tựa $O$ với $OA=0{,}4$ m\"", "$OA=0{,}4$ m", "Cánh tay đòn luôn tính từ $O$ : $OB=AB-OA$ ; $OG=\\dfrac{AB}{2}-OA$"),
  ("\"Treo tại đầu $A$ một vật $50$ N\"", "$P_A=50$ N", "Mômen $P_A\\cdot OA$ làm thanh quay về phía $A$"),
  ("\"tác dụng vào đầu $B$ một lực $F$ … hướng lên hay hướng xuống\"", "$F$ ở $B$, cánh tay đòn $OB$", "⚠ Chiều của $F$ chọn sao cho mômen hai phía bằng nhau ; quy tắc mômen : tổng mômen quay thuận = tổng mômen quay ngược"),
  ("\"lực mà điểm tựa $O$ tác dụng lên thanh\"", "Lực đỡ $N$ hướng lên", "Cân bằng lực thẳng đứng : $N$ bằng tổng các lực kéo xuống"),
  ("\"Bỏ lực $F$ … dời vật $50$ N tới $C$\"", "Cần tìm $OC$ và phía của $C$", "Chỉ còn hai mômen : $P_A\\cdot OC=P\\cdot OG$"),
])
s5 = box([
  "<strong>Quy tắc mômen :</strong> thanh cân bằng khi tổng mômen làm quay thuận chiều kim đồng hồ bằng tổng mômen làm quay ngược chiều, đều lấy đối với $O$.",
  "<strong>Mômen :</strong> $M=F\\cdot d$, với $d$ là cánh tay đòn tính từ $O$ tới giá của lực.",
  "⚠ <strong>Thanh đồng chất :</strong> trọng lượng $P=10m$ đặt tại trung điểm $G$ của thanh, không bỏ qua.",
  "<strong>Cân bằng lực :</strong> thanh đứng yên theo phương thẳng đứng nên lực đỡ của $O$ cân bằng các lực kéo xuống.",
])
s5 += step(1, "Trọng lượng của thanh", ["Thanh đồng chất nên trọng lượng đặt tại trung điểm $G$ :", "$$P=10\\,m$$", f"$$P=10\\times2$$"], f"P={fm(P5)}\\ \\text{{N}}")
s5 += step(2, "Cánh tay đòn của trọng lượng thanh", [
  "$G$ cách $A$ nửa chiều dài thanh, mà $O$ cách $A$ là $OA$, nên $G$ nằm về phía $B$ so với $O$ :", "$$OG=\\dfrac{AB}{2}-OA$$", f"$$OG=0{{,}}6-0{{,}}4$$"], f"OG={fm(OG)}\\ \\text{{m}}")
s5 += step(3, "Chiều của lực $F$", [
  f"Mômen của vật ở $A$ (quay về phía $A$) : $P_A\\cdot OA={fm(PA*OA)}\\ \\text{{N·m}}$.",
  f"Mômen của trọng lượng thanh (quay về phía $B$) : $P\\cdot OG={fm(P5*OG)}\\ \\text{{N·m}}$.",
  "Phía $A$ thắng, nên $F$ tại $B$ phải thêm mômen quay về phía $B$ : $F$ hướng <strong>xuống</strong>."], None)
s5 += step(4, "Độ lớn của lực $F$", [
  "Cân bằng mômen đối với $O$ :", "$$P_A\\cdot OA=P\\cdot OG+F\\cdot OB$$", f"$$50\\times0{{,}}4={fm(P5)}\\times{fm(OG)}+F\\times{fm(OB)}$$",
  "$$F=\\dfrac{P_A\\cdot OA-P\\cdot OG}{OB}$$", f"$$F=\\dfrac{{{fm(PA*OA)}-{fm(P5*OG)}}}{{{fm(OB)}}}$$"], f"F={fm(F5)}\\ \\text{{N}}")
s5 += step(5, "Lực của điểm tựa", [
  "Thanh không chuyển động lên xuống, nên lực đỡ $N$ cân bằng ba lực kéo xuống :", "$$N=P_A+P+F$$", f"$$N=50+{fm(P5)}+{fm(F5)}$$"], f"N={fm(N5)}\\ \\text{{N}}")
s5 += step(6, "Phía của điểm $C$", [
  "Bỏ $F$, chỉ còn mômen của trọng lượng thanh quay về phía $B$.",
  "Vật $50\\ \\text{N}$ phải tạo mômen bằng như thế quay về phía $A$ : cánh tay đòn $OC$ phải nhỏ hơn $OA$, tức $C$ nằm giữa $O$ và $A$ (về phía $A$)."], None)
s5 += step(7, "Vị trí điểm $C$", [
  "Cân bằng mômen đối với $O$ khi không còn $F$ :", "$$P_A\\cdot OC=P\\cdot OG$$", "$$OC=\\dfrac{P\\cdot OG}{P_A}$$", f"$$OC=\\dfrac{{{fm(P5)}\\times{fm(OG)}}}{{50}}={fm(OC,3)}\\ \\text{{m}}$$"], f"OC={fm(OC*100)}\\ \\text{{cm}}")
s5 += step(8, "Kiểm tra", [
  f"Thử lại câu a : $F\\cdot OB+P\\cdot OG={fm(F5)}\\times{fm(OB)}+{fm(P5*OG)}={fm(PA*OA)}\\ \\text{{N·m}}=P_A\\cdot OA$ ✓.",
  f"Thử lại câu c : $50\\times{fm(OC,3)}={fm(PA*OC)}\\ \\text{{N·m}}={fm(P5*OG)}\\ \\text{{N·m}}=P\\cdot OG$ ✓.",
  "Nếu bỏ qua trọng lượng thanh sẽ ra $F=25\\ \\text{N}$, sai vì thanh không nhẹ."])
s5 = '<div class="bt-sol">' + s5 + final(["a) $F$ hướng xuống ; $F=20\\ \\text{N}$", "b) $N=90\\ \\text{N}$", "c) $OC=8\\ \\text{cm}$, $C$ nằm về phía $A$"]) + \
      '<p class="bt-note">Nhận dạng: thấy <strong>thanh đồng chất có khối lượng</strong> trên điểm tựa → thêm <strong>trọng lượng thanh tại trung điểm</strong> vào phương trình mômen.</p></div>'
b5 = [
 buoc("Trọng lượng của thanh", "Trọng lượng $P$ của thanh $AB$ bằng bao nhiêu ?", "Lấy $P=2\\ \\text{N}$ (nhầm khối lượng với trọng lượng) hoặc bỏ qua trọng lượng thanh.", P5, 0.5, "N"),
 buoc("Cánh tay đòn của trọng lượng thanh", "Khoảng cách $OG$ từ điểm tựa tới trọng tâm thanh bằng bao nhiêu mét ?", "Lấy $OG=0{,}6\\ \\text{m}$ vì đo từ $A$ thay vì đo từ $O$.", round(OG, 3), 0.01, "m",
      chon=[ch("$G$ là trung điểm : $OG=\\dfrac{AB}{2}-OA$", True),
            ch("$OG=\\dfrac{AB}{2}$ (đo từ $A$)", False, "Cánh tay đòn phải tính từ điểm tựa $O$, không phải từ đầu $A$."),
            ch("$OG=\\dfrac{OB}{2}$", False, "Trọng tâm nằm ở giữa cả thanh $AB$, không phải ở giữa đoạn $OB$.")]),
 buoc("Chiều của lực $F$", "Mômen nào lớn hơn, và $F$ tại $B$ phải hướng thế nào để thanh nằm ngang ?", "Chọn $F$ hướng lên theo cảm tính vì $B$ ở \"đầu kia\", không so mômen hai phía.",
      lua=[ch("Mômen của vật ở $A$ lớn hơn mômen của trọng lượng thanh, nên $F$ hướng xuống", True),
           ch("Mômen của vật ở $A$ lớn hơn, nên $F$ hướng lên", False, "Hướng lên làm $B$ quay lên, giống chiều quay của vật ở $A$, càng mất cân bằng."),
           ch("Thanh đồng chất nên tự cân bằng, không cần $F$", False, "Thanh đồng chất chỉ cân bằng khi $O$ ở trung điểm ; ở đây $O$ lệch về phía $A$ và còn vật treo ở $A$.")],
      chon=[ch("So mômen của vật ở $A$ với mômen của trọng lượng thanh đối với $O$", True),
            ch("So trọng lượng vật ở $A$ với trọng lượng thanh", False, "Phải so mômen $F\\cdot d$, vì cánh tay đòn hai lực khác nhau."),
            ch("Cho luôn $F=P_A$", False, "Không có cơ sở : cánh tay đòn của $F$ và của vật ở $A$ khác nhau.")]),
 buoc("Độ lớn của lực $F$", "Lực $F$ tại $B$ có độ lớn bằng bao nhiêu ?", "Bỏ qua mômen của trọng lượng thanh nên ra $F$ lớn hơn thực tế, hoặc để mômen của thanh cùng vế với mômen của vật ở $A$.", F5, 0.5, "N",
      chon=[ch("$P_A\\cdot OA=P\\cdot OG+F\\cdot OB$", True),
            ch("$P_A\\cdot OA=F\\cdot OB$ (coi thanh nhẹ)", False, "Thanh có khối lượng $2\\ \\text{kg}$ nên trọng lượng của nó có mômen cùng phía $B$ với $F$."),
            ch("$P_A\\cdot OA+P\\cdot OG=F\\cdot OB$", False, "Trọng lượng thanh nằm về phía $B$, cùng phía với $F$ ; phải đặt ở cùng vế với $F\\cdot OB$.")]),
 buoc("Lực của điểm tựa", "Lực $N$ mà điểm tựa $O$ tác dụng lên thanh bằng bao nhiêu ?", "Quên cộng $F$ vì chỉ nghĩ tới hai trọng lượng, hoặc trừ $F$ vì tưởng $F$ nâng thanh.", N5, 0.5, "N",
      chon=[ch("Cân bằng lực thẳng đứng : $N=P_A+P+F$", True),
            ch("$N=P_A+P$ (không kể $F$)", False, "$F$ hướng xuống cũng đè lên thanh nên $O$ phải đỡ cả phần đó."),
            ch("$N=P_A+P-F$", False, "$F$ hướng xuống, cùng chiều hai trọng lượng, nên phải cộng chứ không trừ.")]),
 buoc("Phía của điểm $C$", "Bỏ $F$, vật $50\\ \\text{N}$ phải dời tới $C$ nằm về phía nào của thanh ?", "Dời vật sang phía $B$ vì tưởng \"dời ra xa\" thì cân bằng.",
      lua=[ch("Về phía $A$, gần $O$ hơn $A$ (cánh tay đòn nhỏ lại)", True),
           ch("Về phía $B$, cùng phía với trọng lượng thanh", False, "Khi đó hai mômen cùng quay về phía $B$, không thể cân bằng."),
           ch("Giữ nguyên tại $A$", False, "Tại $A$ mômen của vật lớn hơn mômen của trọng lượng thanh nên thanh vẫn quay về phía $A$.")],
      chon=[ch("Vật chỉ cần cân bằng với mômen của trọng lượng thanh, nên cánh tay đòn phải ngắn đi", True),
            ch("Dời vật tới trung điểm $G$ của thanh", False, "Tại $G$ vật tạo mômen cùng chiều với trọng lượng thanh, không đối trọng."),
            ch("Dời vật tới đầu $B$", False, "Ở $B$ vật làm thanh quay về phía $B$ rất mạnh, càng mất cân bằng.")]),
 buoc("Vị trí điểm $C$", "Khoảng cách $OC$ bằng bao nhiêu xentimét ?", "Dùng cánh tay đòn $OA$ cho trọng lượng thanh, hoặc vẫn giữ số hạng $F\\cdot OB$ dù đã bỏ $F$.", round(OC * 100, 3), 0.2, "cm",
      chon=[ch("$P_A\\cdot OC=P\\cdot OG$", True),
            ch("$P_A\\cdot OC=P\\cdot OG+F\\cdot OB$", False, "Đã bỏ lực $F$ nên không còn số hạng $F\\cdot OB$."),
            ch("$P_A\\cdot OC=P\\cdot OA$", False, "Cánh tay đòn của trọng lượng thanh là $OG$ (tới trung điểm), không phải $OA$.")]),
 {"tieu_de": "Kiểm tra", "loi_hay_gap": None},
]
b5[-1].pop("loi_hay_gap")

# ================= BÀI 6 =================
p6 = ('<p>Kéo một vật khối lượng $60\\ \\text{kg}$ lên theo mặt phẳng nghiêng dài $4\\ \\text{m}$, cao $1\\ \\text{m}$ bằng hệ gồm một ròng rọc động gắn vào vật và một ròng rọc cố định ở đỉnh dốc (hình) ; '
      'các đoạn dây đều song song với mặt nghiêng. Hiệu suất của riêng mặt phẳng nghiêng (tỉ số giữa công nâng vật và công của lực kéo vật dọc mặt nghiêng) là $80\\ \\%$ ; '
      'ròng rọc nhẹ, trục không ma sát ; dây nhẹ, không giãn. Lấy $g=10\\ \\text{N/kg}$.</p>'
      '<ol type="a"><li>Nếu mặt nghiêng không có ma sát, lực kéo ở đầu dây là bao nhiêu ?</li>'
      '<li>Với hiệu suất $80\\ \\%$, tính lực ma sát giữa vật và mặt nghiêng và lực kéo thực tế ở đầu dây.</li>'
      '<li>Để đưa vật từ chân lên đỉnh dốc, người kéo phải kéo dây đi một đoạn bao nhiêu và thực hiện công bao nhiêu ? Tính hiệu suất của cả hệ.</li></ol>'
      + fig(ns["fig_nghieng_rr"](), "Mặt nghiêng, ròng rọc động gắn vào vật, ròng rọc cố định ở đỉnh dốc"))
a6 = table([
  ("\"vật khối lượng $60$ kg … mặt phẳng nghiêng dài $4$ m, cao $1$ m\"", "$m=60$ kg ; $l=4$ m ; $h=1$ m", "$P=10m$ ; không ma sát thì lực dọc mặt nghiêng $F_0=\\dfrac{P\\,h}{l}$"),
  ("\"ròng rọc động gắn vào vật và ròng rọc cố định ở đỉnh dốc\"", "Hai đoạn dây cùng nâng vật", "⚠ Vật treo trên hai đoạn dây song song mặt nghiêng, mỗi đoạn có lực căng $F$ nên $2F=F_{\\text{dọc}}$ ; ròng rọc cố định chỉ đổi hướng"),
  ("\"Hiệu suất của riêng mặt phẳng nghiêng … $80\\ \\%$\"", "$H=0{,}8$", "⚠ $H=\\dfrac{P\\,h}{F_{\\text{dọc}}\\,l}$ với $F_{\\text{dọc}}$ là lực kéo vật dọc mặt nghiêng, không phải lực ở đầu dây"),
  ("\"hai máy cơ nối tiếp (mặt nghiêng rồi ròng rọc)\"", "Công truyền từ máy này sang máy kia", "Mở rộng ngoài chuẩn KHTN 9 : hiệu suất của máy nối tiếp ; ròng rọc không ma sát nên công không hao phí qua nó"),
  ("\"tính lực ma sát\"", "Cần tìm $F_{\\text{ms}}$", "$F_{\\text{ms}}=F_{\\text{dọc}}-F_0$"),
  ("\"kéo dây đi một đoạn … công … hiệu suất của cả hệ\"", "Cần tìm $s$, $A$, $H_{\\text{hệ}}$", "$s=2l$ ; $A=F\\,s$ ; $H_{\\text{hệ}}=\\dfrac{P\\,h}{A}$"),
])
s6 = box([
  "<strong>Mặt phẳng nghiêng :</strong> không ma sát thì lực kéo dọc $F_0=\\dfrac{P\\,h}{l}$ ; hiệu suất $H=\\dfrac{A_{\\text{ích}}}{A_{\\text{tp}}}=\\dfrac{P\\,h}{F_{\\text{dọc}}\\,l}$.",
  "<strong>Ròng rọc động :</strong> lợi hai lần về lực, thiệt hai lần về đường đi ($s=2l$).",
  "⚠ <strong>Điều kiện :</strong> hiệu suất $80\\ \\%$ chỉ áp cho mặt nghiêng, nên dùng với lực dọc mặt nghiêng, không dùng với lực ở đầu dây.",
  "Ròng rọc và dây lí tưởng : công ở đầu dây bằng công của lực kéo vật dọc mặt nghiêng.",
])
s6 += step(1, "Lực dọc mặt nghiêng khi không ma sát", ["Trọng lượng vật $P=10m=600\\ \\text{N}$.", "$$F_0=\\dfrac{P\\,h}{l}$$", f"$$F_0=\\dfrac{{{fm(P6)}\\times1}}{{4}}$$"], f"F_0={fm(F0)}\\ \\text{{N}}")
s6 += step(2, "Lực kéo ở đầu dây khi không ma sát", ["Vật treo trên hai đoạn dây song song mặt nghiêng, mỗi đoạn căng $F$ :", "$$2F=F_0$$", f"$$F=\\dfrac{{{fm(F0)}}}{{2}}$$"], f"F={fm(F0r)}\\ \\text{{N}}")
s6 += step(3, "Lực dọc mặt nghiêng khi có ma sát", [
  "Hiệu suất của mặt nghiêng :", "$$H=\\dfrac{P\\,h}{F_{\\text{dọc}}\\,l}$$", "$$F_{\\text{dọc}}=\\dfrac{P\\,h}{H\\,l}$$", f"$$F_{{\\text{{dọc}}}}=\\dfrac{{{fm(Aich)}}}{{0{{,}}8\\times4}}$$"], f"F_{{\\text{{dọc}}}}={fm(Fdoc)}\\ \\text{{N}}")
s6 += step(4, "Lực ma sát", ["Phần lực thừa so với trường hợp lí tưởng dùng để thắng ma sát :", "$$F_{\\text{ms}}=F_{\\text{dọc}}-F_0$$", f"$$F_{{\\text{{ms}}}}={fm(Fdoc)}-{fm(F0)}$$"], f"F_{{\\text{{ms}}}}={fm(Fms)}\\ \\text{{N}}")
s6 += step(5, "Lực kéo thực tế ở đầu dây", ["Vẫn hai đoạn dây chia đều lực dọc :", "$$F=\\dfrac{F_{\\text{dọc}}}{2}$$", f"$$F=\\dfrac{{{fm(Fdoc)}}}{{2}}$$"], f"F={fm(Fr)}\\ \\text{{N}}")
s6 += step(6, "Đoạn dây phải kéo", ["Vật đi hết $l=4\\ \\text{m}$ dọc dốc ; ròng rọc động thiệt hai lần về đường đi :", "$$s=2l$$", "$$s=2\\times4$$"], f"s={fm(sday)}\\ \\text{{m}}")
s6 += step(7, "Công của người kéo", ["Lực kéo thực tế nhân với quãng đường dây :", "$$A=F\\,s$$", f"$$A={fm(Fr)}\\times{fm(sday)}$$"], f"A={fm(A6)}\\ \\text{{J}}")
s6 += step(8, "Hiệu suất của cả hệ", ["Công có ích là công nâng vật lên cao $h$ :", "$$A_{\\text{ích}}=P\\,h=600\\ \\text{J}$$", "$$H_{\\text{hệ}}=\\dfrac{A_{\\text{ích}}}{A}$$", f"$$H_{{\\text{{hệ}}}}=\\dfrac{{{fm(Aich)}}}{{{fm(A6)}}}$$"], f"H_{{\\text{{hệ}}}}={fm(Hhe*100)}\\ \\%")
s6 += step(9, "Kiểm tra", [
  f"Công qua ròng rọc không đổi : $F_{{\\text{{dọc}}}}\\,l={fm(Fdoc)}\\times4={fm(Fdoc*4)}\\ \\text{{J}}=A$ ✓.",
  "Ròng rọc không ma sát nên hiệu suất cả hệ bằng hiệu suất của mặt nghiêng ✓."])
s6 = '<div class="bt-sol">' + s6 + final([f"a) $F={fm(F0r)}\\ \\text{{N}}$", f"b) $F_{{\\text{{ms}}}}={fm(Fms)}\\ \\text{{N}}$ ; $F={fm(Fr)}\\ \\text{{N}}$", f"c) $s={fm(sday)}\\ \\text{{m}}$ ; $A={fm(A6)}\\ \\text{{J}}$ ; $H_{{\\text{{hệ}}}}={fm(Hhe*100)}\\ \\%$"]) + \
      '<p class="bt-note">Nhận dạng: thấy <strong>hai máy cơ nối tiếp, cho hiệu suất</strong> → tách từng máy : lực nào đi vào máy nào ; <strong>công không đổi qua ròng rọc không ma sát</strong>.</p></div>'
b6 = [
 buoc("Lực dọc mặt nghiêng khi không ma sát", "Lực kéo vật dọc mặt nghiêng (tại vật) khi không ma sát bằng bao nhiêu ?", "Lấy lực bằng cả trọng lượng (quên lợi về lực của mặt nghiêng) hoặc dùng $\\dfrac{P\\,l}{h}$.", F0, 0.5, "N"),
 buoc("Lực kéo ở đầu dây khi không ma sát", "Lực kéo ở đầu dây khi không ma sát bằng bao nhiêu ?", "Nhân đôi thay vì chia đôi, hoặc quên ròng rọc động.", F0r, 0.5, "N",
      chon=[ch("Vật treo trên hai đoạn dây nên $2F=F_0$", True),
            ch("$F=F_0$ vì ròng rọc chỉ đổi hướng lực", False, "Chỉ ròng rọc cố định mới chỉ đổi hướng ; ròng rọc động gắn vào vật cho lợi hai lần về lực."),
            ch("$F=2F_0$", False, "Lợi về lực nghĩa là kéo nhẹ hơn, không phải nặng hơn.")]),
 buoc("Lực dọc mặt nghiêng khi có ma sát", "Lực kéo vật dọc mặt nghiêng khi có ma sát bằng bao nhiêu ?", "Dùng $H=\\dfrac{P\\,h}{F\\,l}$ với $F$ là lực ở đầu dây thay vì lực dọc mặt nghiêng.", Fdoc, 0.5, "N",
      chon=[ch("Dùng $H=\\dfrac{P\\,h}{F_{\\text{dọc}}\\,l}$ với lực dọc mặt nghiêng", True),
            ch("Dùng $H=\\dfrac{P\\,h}{F\\,l}$ với $F$ là lực ở đầu dây", False, "Hiệu suất này chỉ của mặt nghiêng, ứng với lực dọc trên quãng đường $l$ ; lực ở đầu dây ứng với quãng đường dây $2l$."),
            ch("$F_{\\text{dọc}}=F_0\\cdot H$", False, "Có ma sát thì lực phải lớn hơn trường hợp lí tưởng, nhân với $H\\lt1$ làm lực nhỏ đi.")]),
 buoc("Lực ma sát", "Lực ma sát giữa vật và mặt nghiêng bằng bao nhiêu ?", "Lấy $(1-H)P$ (nhân hao phí với trọng lượng) hoặc lấy luôn $F_{\\text{dọc}}$.", Fms, 0.2, "N",
      chon=[ch("$F_{\\text{ms}}=F_{\\text{dọc}}-F_0$ (phần lực thừa)", True),
            ch("$F_{\\text{ms}}=(1-H)\\,P$", False, "Hiệu suất tính trên công dọc mặt nghiêng, không nhân thẳng với trọng lượng."),
            ch("$F_{\\text{ms}}=F_{\\text{dọc}}$", False, "Lực dọc còn phải cân bằng thành phần trọng lực dọc mặt nghiêng $F_0$, không chỉ thắng ma sát.")]),
 buoc("Lực kéo thực tế ở đầu dây", "Lực kéo thực tế ở đầu dây bằng bao nhiêu ?", "Nhân thêm hiệu suất một lần nữa (tính hai lần) hoặc quên chia đôi.", Fr, 0.2, "N",
      chon=[ch("$F=\\dfrac{F_{\\text{dọc}}}{2}$", True),
            ch("$F=F_{\\text{dọc}}-F_{\\text{ms}}$", False, "Hiệu này chính là $F_0$, lực dọc lí tưởng chưa chia đôi."),
            ch("$F=\\dfrac{F_{\\text{dọc}}\\cdot H}{2}$", False, "$F_{\\text{dọc}}$ đã gồm ma sát, nhân thêm $H$ là tính hiệu suất hai lần.")]),
 buoc("Đoạn dây phải kéo", "Người kéo phải kéo dây đi một đoạn bao nhiêu mét để vật lên hết dốc ?", "Lấy đoạn dây bằng đúng quãng đường vật đi (quên ròng rọc động thiệt đường).", sday, 0.1, "m",
      chon=[ch("Dây đi gấp đôi quãng đường vật : $s=2l$", True),
            ch("$s=l$", False, "Ròng rọc động lợi lực thì thiệt đường đi, dây phải đi dài hơn vật."),
            ch("$s=\\dfrac{l}{2}$", False, "Ngược lại : lợi hai lần về lực thì phải kéo dài gấp đôi, không ngắn đi.")]),
 buoc("Công của người kéo", "Công của người kéo thực hiện bằng bao nhiêu ?", "Nhân lực ở đầu dây với quãng đường vật thay vì quãng đường dây.", A6, 2, "J",
      chon=[ch("$A=F\\,s$ với $F$ và $s$ đều ở đầu dây", True),
            ch("$A=F\\,l$", False, "Lực $F$ ở đầu dây đi quãng $s=2l$, không phải $l$ ; làm vậy thiếu một nửa công."),
            ch("$A=P\\,h$", False, "Đó là công có ích nâng vật lên, chưa gồm công thắng ma sát.")]),
 buoc("Hiệu suất của cả hệ", "Hiệu suất của cả hệ (mặt nghiêng và ròng rọc) bằng bao nhiêu phần trăm ?", "Nhân $80\\ \\%$ với lợi lực $0{,}5$ của ròng rọc (lẫn lợi về lực với hiệu suất).", Hhe * 100, 0.5, "%",
      chon=[ch("$H_{\\text{hệ}}=\\dfrac{P\\,h}{A}$ (công có ích chia công người kéo)", True),
            ch("$H_{\\text{hệ}}=0{,}8\\times0{,}5$", False, "$0{,}5$ là lợi về lực của ròng rọc, không phải hiệu suất ; ròng rọc không ma sát không hao phí."),
            ch("$H_{\\text{hệ}}=\\dfrac{P\\,h}{F\\,l}$", False, "Mẫu số dùng $l$ trong khi lực ở đầu dây ứng với đường $2l$, sẽ ra kết quả vượt $100\\ \\%$, vô lí.")]),
 {"tieu_de": "Kiểm tra"},
]

def dang(label, topic, prob, ana, sol, nd, bu, hay):
    return {"label": label, "topic": topic, "form": "bai_tap", "problem_html": prob, "analysis_html": ana, "solution_html": sol,
            "cap_do": 3, "fading": "giau_het", "nhan_dang": nd, "buoc": bu, "go_roi": {"buoc_hay_sai": hay}}
dang_bai = [
 dang("Bài 4 · Vận dụng · Đoàn tàu qua cột điện, qua cầu, qua tàu khác · Thứ Hai 12/10", "Tổng hợp vận tốc, tính tương đối của chuyển động", p4, a4, s4,
      "Thấy <b>tàu có chiều dài qua cột, cầu, tàu khác</b> → quãng đường cộng chiều dài ; <b>ngược chiều</b> cộng, <b>cùng chiều</b> trừ tốc độ.", b4, 0),
 dang("Bài 5 · Vận dụng · Thanh đồng chất trên điểm tựa · Thứ Ba 13/10", "Moment lực và quy tắc moment", p5, a5, s5,
      "Thấy <b>thanh đồng chất có khối lượng</b> trên điểm tựa → thêm <b>trọng lượng thanh tại trung điểm</b> vào phương trình mômen.", b5, 1),
 dang("Bài 6 · Vận dụng cao · Mặt phẳng nghiêng kết hợp ròng rọc động · Thứ Ba 13/10", "Tính hiệu suất của máy và động cơ", p6, a6, s6,
      "Thấy <b>hai máy cơ nối tiếp, cho hiệu suất</b> → tách từng máy ; <b>công không đổi qua ròng rọc không ma sát</b>.", b6, 2),
]
out = {"lesson_id": 167, "lesson_title": "Bài tập tuần này: 12 bài tự luận Cơ học", "review": {"checked": True, "notes": "tạm, chờ kiểm chéo"}, "dang_bai": dang_bai}
(HERE / "part-B.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
print("ok", [len(d["buoc"]) for d in dang_bai], [d["solution_html"].count('class="bt-step"') for d in dang_bai])
