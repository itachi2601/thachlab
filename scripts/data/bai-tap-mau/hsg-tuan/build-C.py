"""Phần C của bài tập tuần HSG (lesson 167): Bài 7, 8, 9. Chạy: python3 build-C.py -> part-C.json
Số liệu tính ở đây rồi ghép vào chuỗi; hình lấy từ fig_* của sinh-bai-tap.py (đổi mũi tên marker -> chevron)."""
import json, math, pathlib, re
SRC = pathlib.Path("/Users/MAC/Documents/THPT/Lop09/00_Dung_chung/HSG_KHTN9_Vat_li/01_Chuyen_de/Bai_tap_tu_luan_Co_hoc_VD-VDC/sinh-bai-tap.py").read_text()
HERE = pathlib.Path(__file__).parent

# ---------- hình: nạp helper + 3 hàm fig_*, thay L() để vẽ chevron thay marker ----------
helpers = SRC[SRC.index("def S(w, h, b)"):SRC.index("def car(")]
ns = {"math": math}
exec(helpers, ns)
def chev(x, y, dx, dy, L=6, ang=30):
    n = math.hypot(dx, dy) or 1; ux, uy = dx / n, dy / n; t = math.radians(ang); pts = []
    for s in (1, -1):
        c, sn = math.cos(t), math.sin(s * t)
        pts.append((x - L * (ux * c - uy * sn), y - L * (ux * sn + uy * c)))
    (ax, ay), (bx, by) = pts
    return f'<path d="M{ax:.1f},{ay:.1f} L{x:.1f},{y:.1f} L{bx:.1f},{by:.1f}" fill="none" stroke-width="1.3" stroke-linejoin="miter" stroke-miterlimit="10" stroke-linecap="butt"/>'
def L2(x1, y1, x2, y2, w=1.5, d=None, m=False, ms=False):
    a = f' stroke-dasharray="{d}"' if d else ''
    s = f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke-width="{w}"{a}/>'
    n = math.hypot(x2 - x1, y2 - y1); Lc = max(3, min(6, 0.35 * n))
    if m: s += chev(x2, y2, x2 - x1, y2 - y1, Lc)
    if ms: s += chev(x1, y1, x1 - x2, y1 - y2, Lc)
    return s
ns["L"] = L2
def S2(w, h, b):
    return (f'<svg viewBox="0 0 {w} {h}" style="max-width:{w}px;width:100%;height:auto" xmlns="http://www.w3.org/2000/svg" '
            f'font-family="Arial,sans-serif" font-size="12" fill="#111" stroke="#111" stroke-width="1.5" '
            f'stroke-linecap="round" stroke-linejoin="round" role="img" aria-label="@@ARIA@@"><rect width="{w}" height="{h}" fill="#fff" stroke="none"/>{b}</svg>')
ns["S"] = S2
for name in ("fig_binh_thong", "fig_go", "fig_coc"):
    i = SRC.index(f"def {name}()"); j = SRC.index("\ndef ", i + 5) if "\ndef " in SRC[i + 5:i + 3000] else SRC.index("\n\n", i)
    exec(SRC[i:SRC.index("return S(", i) + SRC[SRC.index("return S(", i):].index("\n")], ns)
def fig(fn, aria, cap):
    svg = ns[fn]().replace("@@ARIA@@", aria)
    assert "marker-end" not in svg and "marker-start" not in svg
    return f'<figure class="fig">{svg}<figcaption>{cap}</figcaption></figure>'

# ---------- helpers HTML ----------
def v(x, nd=None):  # số kiểu Việt trong LaTeX
    s = (f"{x:.{nd}f}" if nd is not None else f"{x:g}")
    return s.replace(".", "{,}")
def p(t): return f"<p>{t}</p>"
def e(t): return f"$${t}$$"
def st(n, title, body, ans=None):
    a = f'<div class="bt-ans">$${ans}$$</div>' if ans else ""
    return f'<div class="bt-step"><p class="bt-step-title"><span class="bt-step-n">{n}</span><span>{title}</span></p>{body}{a}</div>'
def box(items):
    return '<div class="tl-box"><p class="tl-label">Kiến thức cần gọi lại</p><ol>' + "".join(f"<li>{i}</li>" for i in items) + "</ol></div>"
def final(lines, nd):
    return '<div class="bt-final"><p><strong>Đáp số</strong></p>' + "".join(p(l) for l in lines) + f'</div><p class="bt-note">Nhận dạng: {nd}</p>'
def table(rows):
    return ('<p>Mỗi câu của đề: <strong>cho dữ liệu gì, gọi kiến thức nào?</strong> Hàng có ⚠ là <strong>điều kiện áp dụng</strong> — kiểm tra trước khi dùng công thức.</p>'
            '<div class="table-scroll"><table class="tl-table tl-table--data"><thead><tr><th>Câu trong đề</th><th>Dữ liệu</th><th>Kiến thức liên quan</th></tr></thead><tbody>'
            + "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in rows) + "</tbody></table></div>")
def ch(*items):  # items: (text, dung, vi_sao)
    return [({"text": t, "dung": True} if d else {"text": t, "dung": False, "vi_sao": w}) for t, d, w in items]
def bu(tieu_de, hoi, dap, don_vi, sai, loi, ck=None):
    b = {"tieu_de": tieu_de, "hoi": hoi, "dap_so": dap, "sai_so": sai, "don_vi": don_vi, "loi_hay_gap": loi}
    if ck: b["chon_buoc_ke"] = ch(*ck)
    return b
def bc(tieu_de, hoi, lua, loi, ck=None):
    b = {"tieu_de": tieu_de, "hoi": hoi, "lua_chon": ch(*lua), "loi_hay_gap": loi}
    if ck: b["chon_buoc_ke"] = ch(*ck)
    return b

g = 10
# ================= BÀI 7 =================
S1, S2_, m, dn, dd = 100e-4, 50e-4, 1, 10000, 8000
p7 = g * m / S1; h7 = p7 / dn; m2 = p7 * S2_ / g; hd = p7 / dd
assert (round(p7), round(h7 * 100, 6), round(m2, 6), round(hd * 100, 6)) == (1000, 10, 0.5, 12.5)

prob7 = ('<p>Bình thông nhau gồm hai nhánh hình trụ tiết diện $S_1=100\\ \\text{cm}^2$ và $S_2=50\\ \\text{cm}^2$, chứa nước (trọng lượng riêng $10\\,000\\ \\text{N/m}^3$). '
         'Đặt lên mặt nước nhánh lớn một pittông mỏng, nhẹ, khít rồi đặt lên pittông một quả cân $1\\ \\text{kg}$. Lấy $g=10\\ \\text{N/kg}$.</p>'
         '<ol type="a"><li>Mực nước hai nhánh chênh lệch bao nhiêu? Nhánh nào cao hơn?</li>'
         '<li>Đặt lên mặt nước nhánh nhỏ một pittông nhẹ, khít. Phải đặt lên pittông này quả cân khối lượng bao nhiêu để mực nước hai nhánh ngang nhau?</li>'
         '<li>Bỏ pittông ở nhánh nhỏ (nhánh lớn vẫn còn pittông và quả cân $1\\ \\text{kg}$). Đổ dầu (trọng lượng riêng $8\\,000\\ \\text{N/m}^3$, không tan trong nước) vào nhánh nhỏ cho đến khi mặt nước hai nhánh ngang nhau. Tính chiều cao cột dầu.</li></ol>'
         + fig("fig_binh_thong", "Bình thông nhau hai nhánh, nhánh lớn có pittông và quả cân 1 kg", "Bình thông nhau: nhánh lớn có pittông và quả cân, nhánh nhỏ để hở."))
ana7 = table([
    ('"hai nhánh hình trụ $S_1=100$ cm² và $S_2=50$ cm², chứa nước ($10\\,000$ N/m³)"', '$S_1=0{,}01$ m² ; $S_2=0{,}005$ m² ; $d_n=10\\,000$ N/m³',
     '⚠ Đổi cm² ra m² trước khi tính áp suất ; hai điểm cùng độ cao trong cùng một chất lỏng đứng yên thì cùng áp suất'),
    ('"pittông mỏng, nhẹ, khít … quả cân $1$ kg"', '$m=1$ kg ; bỏ qua trọng lượng pittông', 'Pittông truyền áp suất lên mặt nước : $p=\\dfrac{F}{S_1}$ với $F=10m$'),
    ('"mực nước hai nhánh chênh lệch bao nhiêu"', 'Cần tìm $h$', 'Cột nước chênh gây áp suất bằng áp suất của quả cân : $d_n\\,h=p$'),
    ('"pittông ở nhánh nhỏ … mực nước hai nhánh ngang nhau"', 'Cần tìm $m_2$', '⚠ Mực ngang nhau nên áp suất dưới hai pittông bằng nhau : $\\dfrac{F_1}{S_1}=\\dfrac{F_2}{S_2}$'),
    ('"đổ dầu ($8\\,000$ N/m³) … mặt nước hai nhánh ngang nhau"', '$d_d=8\\,000$ N/m³ ; cần tìm $h_d$', '⚠ Cột dầu phải gây áp suất bằng $p$ (không còn cột nước nào chênh) : $d_d\\,h_d=p$'),
    ('"bình thông nhau có pittông"', 'Chất lỏng truyền áp suất', 'Mở rộng ngoài chuẩn KHTN 9 : nguyên lí Pascal (chất lỏng truyền nguyên vẹn áp suất đặt lên nó)'),
])
sol7 = '<div class="bt-sol">' + box([
    '<strong>Khái niệm:</strong> áp suất $p=\\dfrac{F}{S}$ ; cột chất lỏng cao $h$ gây áp suất $p=d\\,h$ ; chất lỏng đứng yên truyền nguyên vẹn áp suất.',
    '<strong>Công thức:</strong> $p=\\dfrac{F}{S}$ ; $p=d\\,h$ ; $P=10m$.',
    'Hai điểm <strong>cùng độ cao</strong> trong <strong>cùng một chất lỏng</strong> đứng yên thì có cùng áp suất (mặt đẳng áp).',
    '⚠ <strong>Điều kiện:</strong> đổi cm² ra m² ; chỉ so sánh áp suất ở hai điểm cùng độ cao, cùng chất lỏng liên tục ; áp suất khí quyển hai nhánh như nhau nên triệt tiêu.']) + \
  st(1, "Áp suất do quả cân gây ra", p("Pittông nhẹ nên chỉ quả cân đè lên mặt nước nhánh lớn :") + e("F=10m=10\\cdot1=10\\ \\text{N}") + e(f"p=\\dfrac{{F}}{{S_1}}=\\dfrac{{10}}{{0{{,}}01}}"), f"p={v(p7,0)}\\ \\text{{Pa}}".replace("1000", "1\\,000")) + \
  st(2, "Độ chênh mực nước", p("Chọn mặt đẳng áp là mặt phẳng ngang đi qua mặt dưới pittông. Nước nhánh nhỏ ở cùng độ cao đó chịu thêm cột nước chênh $h$ :") +
     e("d_n\\,h=p") + e(f"h=\\dfrac{{p}}{{d_n}}=\\dfrac{{1\\,000}}{{10\\,000}}=0{{,}}1\\ \\text{{m}}"), "h=10\\ \\text{cm}") + \
  st(3, "Nhánh nào cao hơn", p("Nhánh lớn bị pittông và quả cân ép nên mặt nước nhánh lớn thấp xuống ; nước bị đẩy sang nhánh nhỏ để cân bằng áp suất."), "\\text{Nhánh nhỏ cao hơn}") + \
  st(4, "Quả cân ở nhánh nhỏ", p("Mực nước hai nhánh ngang nhau thì áp suất dưới hai pittông bằng nhau :") + e("\\dfrac{F_1}{S_1}=\\dfrac{F_2}{S_2}") +
     e("F_2=F_1\\cdot\\dfrac{S_2}{S_1}=10\\cdot\\dfrac{50}{100}=5\\ \\text{N}") + e("m_2=\\dfrac{F_2}{10}"), "m_2=0{,}5\\ \\text{kg}") + \
  st(5, "Cột dầu", p("Mặt nước hai nhánh ngang nhau nên cột dầu phải gây đúng áp suất $p$ của quả cân :") + e("d_d\\,h_d=p") + e("h_d=\\dfrac{p}{d_d}=\\dfrac{1\\,000}{8\\,000}=0{,}125\\ \\text{m}"), "h_d=12{,}5\\ \\text{cm}") + \
  st(6, "Kiểm tra", p("Dầu nhẹ hơn nước ($8\\,000\\lt10\\,000$) nên cột dầu phải cao hơn cột nước chênh : $12{,}5\\ \\text{cm}\\gt10\\ \\text{cm}$ ✓.") +
     p("Tỉ số $\\dfrac{h_d}{h}=\\dfrac{d_n}{d_d}=\\dfrac{10\\,000}{8\\,000}=1{,}25$ ✓.") + p("Nhánh nhỏ ở câu b : $\\dfrac{5}{0{,}005}=1\\,000\\ \\text{Pa}$, bằng $p$ ✓.")) + \
  final(["a) $10\\ \\text{cm}$ ; nhánh nhỏ cao hơn", "b) $0{,}5\\ \\text{kg}$", "c) $12{,}5\\ \\text{cm}$"],
        "thấy <strong>bình thông nhau có pittông hoặc hai chất lỏng</strong> → chọn <strong>mặt đẳng áp</strong> trong cùng một chất lỏng rồi viết áp suất hai bên bằng nhau.") + "</div>"
b7 = [
 bu("Áp suất do quả cân gây ra", "Quả cân (pittông nhẹ) gây áp suất $p$ lên nước nhánh lớn bằng bao nhiêu pascal?", 1000, "Pa", 10,
    "Chia lực cho $S_2$ thay vì $S_1$ (pittông đặt ở nhánh lớn), hoặc quên đổi cm² ra m² nên ra áp suất nhỏ hơn thực tế rất nhiều."),
 bu("Độ chênh mực nước", "Cột nước chênh giữa hai nhánh cao bao nhiêu xentimét?", 10, "cm", 0.2,
    "Lấy $h=\\dfrac{F}{d}$ không chia cho tiết diện, hoặc quên đổi mét ra xentimét.",
    [("Cột nước chênh gây áp suất đúng bằng $p$ của quả cân : $d_n\\,h=p$", True, ""),
     ("Hai nhánh thông nhau nên mực nước luôn bằng nhau : $h=0$", False, "Pittông và quả cân tạo thêm áp suất lên mặt nước nhánh lớn, nên mực nước nhánh nhỏ phải cao lên mới cân bằng."),
     ("$h=\\dfrac{F}{d_n}$ với $F$ là trọng lượng quả cân", False, "Áp suất mới so sánh được với $d\\,h$ ; lực $F$ chưa chia cho tiết diện thì đơn vị là $\\text{m}^2$, không phải độ cao.")]),
 bc("Nhánh nào cao hơn", "Nhánh nào có mặt nước cao hơn ?",
    [("Nhánh nhỏ (không pittông)", True, ""),
     ("Nhánh lớn (có pittông và quả cân)", False, "Nhánh lớn bị ép bởi pittông và quả cân nên mặt nước ở đó thấp xuống, nước dồn sang nhánh nhỏ."),
     ("Hai nhánh ngang nhau", False, "Ngang nhau chỉ khi áp suất hai bên bằng nhau ; ở đây nhánh lớn chịu thêm áp suất của quả cân.")],
    "Cho rằng nhánh tiết diện lớn chứa nhiều nước hơn nên mực nước cao hơn — mực nước do áp suất quyết định, không do lượng nước.",
    [("Nhánh bị ép thêm áp suất thì mực nước thấp xuống, nước dồn sang nhánh kia", True, ""),
     ("Nhánh nào chứa nhiều nước hơn thì mực nước cao hơn", False, "Mực nước quyết định bởi áp suất, không phải lượng nước ; nhánh rộng chứa nhiều nước vẫn có thể thấp hơn."),
     ("Quả cân đặt ở nhánh nào thì nhánh đó nâng mực nước lên", False, "Quả cân đè xuống chứ không nâng : nước bị ép dồn sang nhánh còn lại.")]),
 bu("Quả cân ở nhánh nhỏ", "Phải đặt lên pittông nhánh nhỏ quả cân khối lượng bao nhiêu kilôgam để mực nước hai nhánh ngang nhau?", 0.5, "kg", 0.01,
    "Lấy $m_2=m_1$ vì cho rằng \"mực ngang nhau thì hai quả cân bằng nhau\" (quên tiết diện hai nhánh khác nhau), hoặc nhân nhầm $S_1/S_2$.",
    [("Áp suất dưới hai pittông bằng nhau : $\\dfrac{F_1}{S_1}=\\dfrac{F_2}{S_2}$", True, ""),
     ("Hai quả cân phải bằng nhau : $m_2=m_1$", False, "Ngang mực nghĩa là áp suất bằng nhau, không phải lực bằng nhau ; tiết diện khác nhau thì lực khác nhau."),
     ("$F_2=F_1\\cdot\\dfrac{S_1}{S_2}$", False, "Ngược tỉ lệ : tiết diện nhánh nhỏ bé hơn nên lực cần để cùng áp suất cũng nhỏ hơn, phải nhân $\\dfrac{S_2}{S_1}$.")]),
 bu("Cột dầu", "Cột dầu ở nhánh nhỏ cao bao nhiêu xentimét để mặt nước hai nhánh ngang nhau?", 12.5, "cm", 0.2,
    "Dùng trọng lượng riêng của nước thay vì của dầu, hoặc cộng thêm một cột nước nào đó dù mặt nước hai nhánh đã ngang nhau.",
    [("Cột dầu gây áp suất đúng bằng $p$ : $d_d\\,h_d=p$", True, ""),
     ("$d_n\\,h_d=p$ (dùng trọng lượng riêng của nước)", False, "Cột đang xét là dầu nên phải dùng trọng lượng riêng của dầu, nhỏ hơn của nước."),
     ("$d_d\\,h_d=p+d_n\\,h$", False, "Mặt nước hai nhánh ngang nhau nên không có cột nước chênh nào cần cộng thêm.")]),
 {"tieu_de": "Kiểm tra"},
]
d7 = dict(form="bai_tap", label="Bài 7 · Vận dụng · Bình thông nhau có pittông · Thứ Tư 14/10", topic="Khối lượng riêng và áp suất chất lỏng theo độ sâu",
          problem_html=prob7, analysis_html=ana7, solution_html=sol7, cap_do=3, fading="giau_het",
          nhan_dang="Thấy <b>bình thông nhau có pittông / hai chất lỏng</b> → nghĩ tới <b>mặt đẳng áp</b>, viết áp suất hai bên bằng nhau.",
          buoc=b7, go_roi={"buoc_hay_sai": 3})

# ================= BÀI 8 =================
S8, h8, Dg, Dn, Ds = 100e-4, 0.10, 600, 1000, 7800
V8 = S8 * h8; Pg = g * Dg * V8; x8 = Dg / Dn * h8; FA = g * Dn * V8; mb = (FA - Pg) / g
Vs = (FA - Pg) / (g * (Ds - Dn)); ms = Ds * Vs; T8 = FA - Pg
assert (round(Pg, 6), round(x8 * 100, 6), round(FA, 6), round(mb, 6), round(Vs * 1e6, 1), round(ms, 3), round(T8, 6)) == (6, 6, 10, 0.4, 58.8, 0.459, 4)
assert abs((ms * g - g * Dn * Vs) - T8) < 1e-9
prob8 = ('<p>Khối gỗ hình hộp chữ nhật, diện tích đáy $100\\ \\text{cm}^2$, cao $10\\ \\text{cm}$, khối lượng riêng $600\\ \\text{kg/m}^3$, thả nổi trong nước (khối lượng riêng $1\\,000\\ \\text{kg/m}^3$). Lấy $g=10\\ \\text{N/kg}$.</p>'
         '<ol type="a"><li>Tính chiều cao phần gỗ chìm trong nước.</li>'
         '<li>Đặt lên mặt gỗ một vật nhỏ khối lượng $m$. Tính $m$ để mặt trên của gỗ vừa ngang mặt nước.</li>'
         '<li>Bỏ vật ở câu b. Dùng dây mảnh, không giãn treo dưới đáy gỗ một quả cầu bằng sắt (khối lượng riêng $7\\,800\\ \\text{kg/m}^3$, ngập hoàn toàn trong nước) thì gỗ cũng vừa chìm hết. Bỏ qua thể tích dây. Tính thể tích và khối lượng quả cầu.</li>'
         '<li>Trong trường hợp c, dây chịu lực căng bao nhiêu?</li></ol>'
         + fig("fig_go", "Khối gỗ nổi trong nước, quả cầu sắt treo dưới đáy", "Khối gỗ nổi ; ở câu c có quả cầu sắt treo dưới đáy."))
ana8 = table([
    ('"hình hộp chữ nhật, đáy $100$ cm², cao $10$ cm, $600$ kg/m³"', '$S=100$ cm² ; $h=10$ cm ; $D_g=600$ kg/m³', '⚠ Gỗ nổi được vì $D_g\\lt D_n$ ; đổi cm³ ra m³ khi dùng $D$ theo kg/m³ : $V=S\\,h$'),
    ('"thả nổi trong nước ($1\\,000$ kg/m³)"', '$D_n=1\\,000$ kg/m³', 'Nổi cân bằng : $F_A=P_{g}$ với $F_A=10D_n\\,S\\,x$'),
    ('"Tính chiều cao phần gỗ chìm"', 'Cần tìm $x$', '$x=h\\cdot\\dfrac{D_g}{D_n}$'),
    ('"vật nhỏ khối lượng $m$ … mặt trên vừa ngang mặt nước"', 'Gỗ chìm hết : $V_{chìm}=V$', '⚠ Lúc này $F_{A,max}=10D_n\\,V$ ; cân bằng : $F_{A,max}=P_g+10m$'),
    ('"treo dưới đáy gỗ quả cầu sắt ($7\\,800$ kg/m³, ngập hoàn toàn) … gỗ vừa chìm hết"', '$D_s=7\\,800$ kg/m³ ; cả hai vật chìm hết', '⚠ Quả cầu ngập trong nước cũng chịu lực đẩy : cân bằng cả hệ $F_{A,g}+F_{A,s}=P_g+P_s$'),
    ('"dây chịu lực căng bao nhiêu"', 'Cần tìm $T$', 'Tách riêng một vật : với gỗ, $F_{A,g}=P_g+T$'),
])
sol8 = '<div class="bt-sol">' + box([
    '<strong>Khái niệm:</strong> vật nằm cân bằng trong chất lỏng thì lực đẩy Archimedes cân bằng với trọng lượng của những gì nó phải đỡ.',
    '<strong>Công thức:</strong> $F_A=d_n\\,V_{chìm}=10D_n\\,V_{chìm}$ ; $P=10m=10D\\,V$.',
    'Có nhiều vật gắn với nhau thì viết cân bằng cho <strong>cả hệ</strong> : tổng lực đẩy bằng tổng trọng lượng. Cần lực căng dây thì tách riêng một vật.',
    '⚠ <strong>Điều kiện:</strong> $V_{chìm}$ là thể tích phần ngập trong nước ; vật ngập hoàn toàn thì $V_{chìm}=V$ ; đổi cm³ ra m³ trước khi tính.']) + \
  st(1, "Chiều cao phần gỗ chìm", p("Thể tích gỗ và trọng lượng gỗ :") + e("V=S\\,h=100\\cdot10=1\\,000\\ \\text{cm}^3=10^{-3}\\ \\text{m}^3") + e("P_g=10D_g\\,V=10\\cdot600\\cdot10^{-3}=6\\ \\text{N}") +
     p("Nổi cân bằng $F_A=P_g$ :") + e("10D_n\\,S\\,x=10D_g\\,S\\,h") + e("x=h\\cdot\\dfrac{D_g}{D_n}=10\\cdot\\dfrac{600}{1\\,000}"), "x=6\\ \\text{cm}") + \
  st(2, "Lực đẩy khi gỗ vừa chìm hết", p("Gỗ chìm hết thì $V_{chìm}=V$ :") + e("F_{A,max}=10D_n\\,V=10\\cdot1\\,000\\cdot10^{-3}"), "F_{A,max}=10\\ \\text{N}") + \
  st(3, "Vật đặt trên mặt gỗ", p("Gỗ phải đỡ trọng lượng của chính nó và của vật :") + e("F_{A,max}=P_g+10m") + e("m=\\dfrac{F_{A,max}-P_g}{10}=\\dfrac{10-6}{10}"), "m=0{,}4\\ \\text{kg}") + \
  st(4, "Thể tích quả cầu sắt", p("Cả gỗ và sắt đều chìm hết nên mỗi vật chịu một lực đẩy. Cân bằng của cả hệ :") + e("F_{A,g}+F_{A,s}=P_g+P_s") +
     e("F_{A,max}+10D_n\\,V_s=P_g+10D_s\\,V_s") + e("V_s=\\dfrac{F_{A,max}-P_g}{10\\,(D_s-D_n)}=\\dfrac{10-6}{10\\cdot6\\,800}\\approx5{,}88\\cdot10^{-5}\\ \\text{m}^3"), "V_s\\approx58{,}8\\ \\text{cm}^3") + \
  st(5, "Khối lượng quả cầu sắt", e("m_s=D_s\\,V_s=7\\,800\\cdot5{,}88\\cdot10^{-5}"), "m_s\\approx0{,}459\\ \\text{kg}") + \
  st(6, "Lực căng dây", p("Xét riêng khối gỗ : lực đẩy hướng lên, trọng lượng và lực căng dây cùng hướng xuống :") + e("F_{A,g}=P_g+T") + e("T=F_{A,max}-P_g=10-6"), "T=4\\ \\text{N}") + \
  st(7, "Kiểm tra", p("Xét riêng quả cầu : $T=P_s-F_{A,s}$.") + e("P_s=10\\cdot0{,}459\\approx4{,}59\\ \\text{N}\\ ;\\ F_{A,s}=10\\cdot1\\,000\\cdot5{,}88\\cdot10^{-5}\\approx0{,}59\\ \\text{N}") +
     p("$T=4{,}59-0{,}59=4{,}0\\ \\text{N}$, khớp với bước 6 ✓.") + p("Quả cầu nặng hơn vật ở câu b ($0{,}459\\gt0{,}4\\ \\text{kg}$) vì nước còn đẩy quả cầu lên ✓.")) + \
  final(["a) $6\\ \\text{cm}$", "b) $0{,}4\\ \\text{kg}$", "c) $V_s\\approx58{,}8\\ \\text{cm}^3$ ; $m_s\\approx0{,}459\\ \\text{kg}$", "d) $4\\ \\text{N}$"],
        "thấy <strong>vật nổi + vật đặt trên hoặc treo dưới</strong> → viết <strong>cân bằng cho cả hệ</strong> (tổng $F_A$ = tổng $P$) ; cần lực dây thì tách riêng một vật.") + "</div>"
b8 = [
 bu("Chiều cao phần gỗ chìm", "Khối gỗ nổi chìm sâu bao nhiêu xentimét?", 6, "cm", 0.1,
    "Lấy $x=h\\cdot\\dfrac{D_n}{D_g}$ (ngược tỉ số), hoặc cho rằng gỗ chìm hết nên $x=h$."),
 bu("Lực đẩy khi gỗ vừa chìm hết", "Khi gỗ vừa chìm hết, lực đẩy Archimedes lên gỗ bằng bao nhiêu niutơn?", 10, "N", 0.1,
    "Dùng khối lượng riêng của gỗ thay vì của nước, hoặc quên nhân $10$ để đổi khối lượng ra trọng lượng.",
    [("Chìm hết nên $V_{chìm}=V$ : $F_{A,max}=d_n\\,V$", True, ""),
     ("Lực đẩy vẫn bằng trọng lượng gỗ : $F_A=P_g$", False, "Đó là lúc gỗ nổi tự do ; khi gỗ bị đè chìm hết, phần thể tích chìm tăng lên nên lực đẩy lớn hơn trọng lượng gỗ."),
     ("$F_{A,max}=d_g\\,V$ (dùng trọng lượng riêng của gỗ)", False, "Lực đẩy do nước tác dụng nên phải dùng trọng lượng riêng của nước.")]),
 bu("Vật đặt trên mặt gỗ", "Vật đặt lên gỗ phải có khối lượng bao nhiêu kilôgam để gỗ vừa chìm hết?", 0.4, "kg", 0.01,
    "Viết $F_A=P_{vật}$ mà quên trọng lượng của chính khối gỗ, hoặc quên chia cho $10$ để đổi niutơn ra kilôgam.",
    [("Gỗ đỡ cả chính nó và vật : $F_{A,max}=P_g+P_{vật}$", True, ""),
     ("$F_{A,max}=P_{vật}$", False, "Gỗ cũng có trọng lượng riêng của nó, lực đẩy phải đỡ cả gỗ lẫn vật."),
     ("Phần chìm vẫn là phần chìm ở câu a, chỉ cộng thêm khối lượng vật", False, "Thêm vật thì gỗ chìm sâu hơn ; đề cho gỗ vừa chìm hết nên $V_{chìm}=V$.")]),
 bu("Thể tích quả cầu sắt", "Thể tích $V_s$ của quả cầu sắt bằng bao nhiêu xentimét khối?", 58.8, "cm³", 0.5,
    "Bỏ lực đẩy lên quả cầu (coi sắt chỉ thêm trọng lượng) nên được $V_s$ sai, hoặc đổi m³ ra cm³ sai $10^3$ lần.",
    [("Viết cân bằng cả hệ gỗ + sắt, mỗi vật chìm hết đều có lực đẩy", True, ""),
     ("$F_{A,g}=P_g+P_s$ (bỏ lực đẩy lên quả cầu)", False, "Quả cầu ngập hoàn toàn trong nước cũng chịu lực đẩy, không thể bỏ qua."),
     ("Lấy khối lượng quả cầu bằng khối lượng vật ở câu b", False, "Vật ở câu b chỉ chịu trọng lượng ; quả cầu bị nước đẩy lên nên khối lượng khác, phải tìm qua thể tích.")]),
 bu("Khối lượng quả cầu sắt", "Khối lượng $m_s$ của quả cầu sắt bằng bao nhiêu kilôgam?", 0.459, "kg", 0.005,
    "Nhân thể tích với khối lượng riêng của nước, hoặc nhân với thể tích chưa đổi sang m³.",
    [("$m_s=D_s\\,V_s$", True, ""),
     ("$m_s=D_n\\,V_s$", False, "Đó là khối lượng của nước có cùng thể tích với quả cầu, không phải của sắt."),
     ("$m_s=\\dfrac{F_{A,s}}{10}$", False, "Lực đẩy chia $10$ chỉ cho khối lượng nước bị chiếm chỗ, không phải khối lượng quả cầu.")]),
 bu("Lực căng dây", "Dây chịu lực căng bao nhiêu niutơn?", 4, "N", 0.1,
    "Cho $T=P_s$ (bỏ lực đẩy lên quả cầu), hoặc cộng $F_A$ với $P$ của gỗ thay vì lấy hiệu.",
    [("Xét riêng gỗ : $F_{A,g}=P_g+T$", True, ""),
     ("$T=P_s$", False, "Nước đẩy quả cầu lên nên dây chỉ chịu trọng lượng trừ lực đẩy, không phải toàn bộ trọng lượng."),
     ("$T=F_{A,g}+P_g$", False, "Lực căng dây và trọng lượng gỗ cùng hướng xuống, cùng cân bằng với lực đẩy : phải lấy $F_A-P_g$.")]),
 {"tieu_de": "Kiểm tra"},
]
d8 = dict(form="bai_tap", label="Bài 8 · Vận dụng cao · Khối gỗ nổi, vật đặt trên và vật treo dưới · Thứ Tư 14/10", topic="Lực đẩy Archimedes và điều kiện nổi",
          problem_html=prob8, analysis_html=ana8, solution_html=sol8, cap_do=3, fading="giau_het",
          nhan_dang="Thấy <b>vật nổi + vật đặt trên / treo dưới</b> → nghĩ tới <b>cân bằng cả hệ</b>: tổng F<sub>A</sub> = tổng P.",
          buoc=b8, go_roi={"buoc_hay_sai": 3})

# ================= BÀI 9 =================
S9, S9c, hc, mc, mn, ms9, Dsoi = 200, 50, 12, 200, 100, 100, 2.5
xa = mc / S9c; dha = mc / S9; xb = (mc + mn) / S9c; dhb = mn / S9; dc1 = ms9 / S9; Vso = ms9 / Dsoi; dc2 = Vso / S9; mmax = S9c * hc - mc
assert (xa, dha, xb, dhb, dc1, dc2, round(dc1 - dc2, 6), mmax) == (4, 1, 6, 0.5, 0.5, 0.2, 0.3, 400)
prob9 = ('<p>Bình hình trụ đủ cao, tiết diện $S=200\\ \\text{cm}^2$, đựng nước, mực nước cao $20\\ \\text{cm}$. Thả vào bình một cốc hình trụ thành mỏng (bỏ qua thể tích thành cốc), khối lượng $200\\ \\text{g}$, tiết diện $50\\ \\text{cm}^2$, cao $12\\ \\text{cm}$ ; cốc nổi thẳng đứng, miệng hướng lên, đáy không chạm đáy bình. Khối lượng riêng của nước $1\\ \\text{g/cm}^3$.</p>'
         '<ol type="a"><li>Cốc chìm sâu bao nhiêu? Mực nước trong bình dâng thêm bao nhiêu?</li>'
         '<li>Rót vào cốc $100\\ \\text{g}$ nước. Cốc chìm sâu bao nhiêu? Mực nước trong bình dâng thêm bao nhiêu so với câu a?</li>'
         '<li>Thay vì rót nước, bỏ vào cốc một hòn sỏi $100\\ \\text{g}$ (khối lượng riêng $2{,}5\\ \\text{g/cm}^3$). Tính độ dâng thêm của mực nước trong bình (so với câu a) trong hai trường hợp : sỏi nằm trong cốc, và sỏi được thả thẳng xuống đáy bình (cốc rỗng vẫn nổi). Trường hợp nào mực nước cao hơn, cao hơn bao nhiêu?</li>'
         '<li>Rót nước vào cốc tối đa bao nhiêu gam thì cốc vẫn chưa bị ngập (miệng cốc vừa chạm mặt nước)?</li></ol>'
         + fig("fig_coc", "Bình trụ đựng nước, cốc hình trụ nổi thẳng đứng", "Bình trụ và cốc nổi."))
ana9 = table([
    ('"Bình hình trụ … $S=200$ cm², mực nước cao $20$ cm"', '$S=200$ cm² ; $D_n=1$ g/cm³', '⚠ Độ dâng của mực nước bình tính bằng thể tích chiếm chỗ chia cho tiết diện <strong>bình</strong> $S$, không phải tiết diện cốc'),
    ('"cốc hình trụ thành mỏng, $200$ g, tiết diện $50$ cm², cao $12$ cm … nổi thẳng đứng"', '$m_c=200$ g ; $S_c=50$ cm² ; $h_c=12$ cm', 'Nổi : $F_A=P$ nên khối lượng nước bị chiếm chỗ bằng khối lượng vật : $V_{chìm}=\\dfrac{m}{D_n}$ ; độ chìm $x=\\dfrac{V_{chìm}}{S_c}$'),
    ('"Cốc chìm sâu bao nhiêu? Mực nước dâng thêm"', 'Cần tìm $x$ và $\\Delta h$', '$x=\\dfrac{V_{chìm}}{S_c}$ ; $\\Delta h=\\dfrac{V_{chìm}}{S}$'),
    ('"Rót vào cốc $100$ g nước"', '$m_n=100$ g', 'Khối lượng tổng của cốc và nước trong cốc quyết định $V_{chìm}$ ; so với câu a chỉ tăng thêm phần nước rót'),
    ('"hòn sỏi $100$ g ($2{,}5$ g/cm³) … trong cốc, và thả thẳng xuống đáy bình"', '$m_s=100$ g ; $D_s=2{,}5$ g/cm³', '⚠ Sỏi trong cốc : vật nổi chiếm chỗ theo <strong>khối lượng</strong> ; sỏi dưới đáy : vật chìm chiếm chỗ theo <strong>thể tích thật</strong> $V=\\dfrac{m}{D}$'),
    ('"Rót nước tối đa … miệng cốc vừa chạm mặt nước"', 'Chìm tối đa $x=h_c=12$ cm', '$V_{chìm,max}=S_c\\,h_c$ ; khối lượng tối đa đỡ được $=D_n\\,V_{chìm,max}$ rồi trừ khối lượng cốc'),
])
sol9 = '<div class="bt-sol">' + box([
    '<strong>Khái niệm:</strong> vật nổi cân bằng nên lực đẩy bằng trọng lượng ; nước bị chiếm chỗ có khối lượng đúng bằng khối lượng vật.',
    '<strong>Công thức:</strong> $V_{chìm}=\\dfrac{m}{D_n}$ ; độ chìm $x=\\dfrac{V_{chìm}}{S_c}$ ; mực nước bình dâng $\\Delta h=\\dfrac{V_{chiếm}}{S}$.',
    'Vật nổi chiếm chỗ theo <strong>khối lượng</strong> ; vật chìm hẳn chiếm chỗ theo <strong>thể tích thật</strong> $V=\\dfrac{m}{D}$.',
    '⚠ <strong>Điều kiện:</strong> chia thể tích cho tiết diện <strong>bình</strong> khi tính độ dâng mực nước ; cốc phải còn nổi, miệng chưa chìm dưới mặt nước.']) + \
  st(1, "Cốc rỗng chìm sâu bao nhiêu", p("Nổi cân bằng nên nước bị chiếm chỗ nặng bằng cốc :") + e("V_{chìm}=\\dfrac{m_c}{D_n}=\\dfrac{200}{1}=200\\ \\text{cm}^3") + e("x=\\dfrac{V_{chìm}}{S_c}=\\dfrac{200}{50}"), "x=4\\ \\text{cm}") + \
  st(2, "Mực nước trong bình dâng", p("Phần chìm của cốc chiếm chỗ $200\\ \\text{cm}^3$ trong bình tiết diện $S$ :") + e("\\Delta h=\\dfrac{V_{chìm}}{S}=\\dfrac{200}{200}"), "\\Delta h=1\\ \\text{cm}") + \
  st(3, "Cốc chìm sâu khi có nước rót vào", p("Khối lượng cốc và nước trong cốc là $200+100=300\\ \\text{g}$ :") + e("V_{chìm}=\\dfrac{300}{1}=300\\ \\text{cm}^3") + e("x=\\dfrac{V_{chìm}}{S_c}=\\dfrac{300}{50}"), "x=6\\ \\text{cm}") + \
  st(4, "Mực nước dâng thêm so với câu a", p("Thể tích phần chìm tăng thêm $300-200=100\\ \\text{cm}^3$ :") + e("\\Delta h'=\\dfrac{100}{S}=\\dfrac{100}{200}"), "\\Delta h'=0{,}5\\ \\text{cm}") + \
  st(5, "Sỏi nằm trong cốc", p("Cốc vẫn nổi, nước bị chiếm chỗ thêm có khối lượng bằng khối lượng sỏi :") + e("\\Delta V=\\dfrac{m_s}{D_n}=\\dfrac{100}{1}=100\\ \\text{cm}^3") + e("\\Delta h_1=\\dfrac{\\Delta V}{S}=\\dfrac{100}{200}"), "\\Delta h_1=0{,}5\\ \\text{cm}") + \
  st(6, "Sỏi thả xuống đáy bình", p("Cốc rỗng vẫn như câu a. Sỏi chìm hẳn chiếm đúng thể tích thật của nó :") + e("V_s=\\dfrac{m_s}{D_s}=\\dfrac{100}{2{,}5}=40\\ \\text{cm}^3") + e("\\Delta h_2=\\dfrac{V_s}{S}=\\dfrac{40}{200}"), "\\Delta h_2=0{,}2\\ \\text{cm}") + \
  st(7, "Trường hợp nào mực nước cao hơn", p("So hai độ dâng : $\\Delta h_1\\gt\\Delta h_2$. Sỏi nằm trong cốc làm mực nước cao hơn vì sỏi nổi nhờ cốc nên chiếm chỗ theo khối lượng ($100\\ \\text{cm}^3$ nước), lớn hơn thể tích thật ($40\\ \\text{cm}^3$) do sỏi nặng hơn nước."), "\\text{Sỏi nằm trong cốc}") + \
  st(8, "Chênh lệch giữa hai trường hợp", e("\\Delta h_1-\\Delta h_2=0{,}5-0{,}2"), "\\Delta h_1-\\Delta h_2=0{,}3\\ \\text{cm}") + \
  st(9, "Lượng nước tối đa rót vào cốc", p("Cốc chìm tối đa $12\\ \\text{cm}$ :") + e("V_{chìm,max}=S_c\\,h_c=50\\cdot12=600\\ \\text{cm}^3") +
     p("Cốc và nước trong cốc nặng tối đa $600\\ \\text{g}$ :") + e("m_{n,max}=600-m_c=600-200"), "m_{n,max}=400\\ \\text{g}") + \
  st(10, "Kiểm tra", p("Khi đó cốc và nước nặng $200+400=600\\ \\text{g}$, cần chiếm chỗ $600\\ \\text{cm}^3$ ✓.") + p("Mực nước bình lúc đó cao $20+\\dfrac{600}{200}=23\\ \\text{cm}$, cốc chìm $12\\ \\text{cm}$ nên đáy cốc còn cách đáy bình $11\\ \\text{cm}$ ✓ (cốc không chạm đáy).") +
     p("Câu b : $\\Delta h'=0{,}5\\ \\text{cm}$ đúng bằng khi rót thẳng $100\\ \\text{g}$ nước vào bình ✓.")) + \
  final(["a) chìm $4\\ \\text{cm}$ ; dâng $1\\ \\text{cm}$", "b) chìm $6\\ \\text{cm}$ ; dâng thêm $0{,}5\\ \\text{cm}$", "c) sỏi trong cốc : $+0{,}5\\ \\text{cm}$ ; sỏi dưới đáy : $+0{,}2\\ \\text{cm}$ ; trong cốc cao hơn $0{,}3\\ \\text{cm}$", "d) $400\\ \\text{g}$"],
        "thấy <strong>vật nổi trong bình, hỏi mực nước</strong> → vật nổi chiếm chỗ theo <strong>khối lượng</strong>, vật chìm chiếm chỗ theo <strong>thể tích</strong>.") + "</div>"
b9 = [
 bu("Cốc rỗng chìm sâu bao nhiêu", "Cốc rỗng nổi thì chìm sâu bao nhiêu xentimét?", 4, "cm", 0.1,
    "Chia thể tích chìm cho tiết diện bình $S$ thay vì tiết diện cốc $S_c$, hoặc cho rằng cốc chìm hết chiều cao $12\\ \\text{cm}$."),
 bu("Mực nước trong bình dâng", "Mực nước trong bình dâng thêm bao nhiêu xentimét?", 1, "cm", 0.05,
    "Lấy độ dâng bằng độ chìm của cốc ($\\Delta h=x$), hoặc chia cho tiết diện cốc thay vì tiết diện bình.",
    [("Thể tích chiếm chỗ chia cho tiết diện bình : $\\Delta h=\\dfrac{V_{chìm}}{S}$", True, ""),
     ("Mực nước dâng đúng bằng độ chìm của cốc : $\\Delta h=x$", False, "Nước dâng lên trên cả tiết diện bình rộng, không dồn vào chỗ cốc nên $\\Delta h$ nhỏ hơn $x$."),
     ("$\\Delta h=\\dfrac{V_{chìm}}{S_c}$", False, "$S_c$ là tiết diện cốc ; nước dâng trong toàn bình nên phải chia cho tiết diện bình $S$.")]),
 bu("Cốc chìm sâu khi có nước rót vào", "Sau khi rót nước vào cốc, cốc chìm sâu bao nhiêu xentimét?", 6, "cm", 0.1,
    "Chỉ tính khối lượng nước rót vào mà quên khối lượng cốc, hoặc giữ nguyên độ chìm của câu a.",
    [("Nổi cân bằng với tổng khối lượng cốc và nước : $V_{chìm}=\\dfrac{m_c+m_n}{D_n}$", True, ""),
     ("Độ chìm không đổi vì cốc vẫn là cốc đó", False, "Cốc nặng thêm thì lực đẩy phải tăng, cốc phải chìm sâu hơn."),
     ("$V_{chìm}=\\dfrac{m_n}{D_n}$ (chỉ tính nước rót)", False, "Cốc vẫn nặng $200\\ \\text{g}$ ; lực đẩy phải đỡ cả cốc và nước.")]),
 bu("Mực nước dâng thêm so với câu a", "Mực nước trong bình dâng thêm bao nhiêu xentimét so với câu a?", 0.5, "cm", 0.02,
    "Chia phần thể tích tăng thêm cho tiết diện cốc, hoặc tính lại từ đầu rồi quên trừ độ dâng ở câu a.",
    [("Thể tích phần chìm tăng thêm chia cho tiết diện bình", True, ""),
     ("Thể tích nước rót chia cho tiết diện cốc", False, "Nước dâng trong cả bình rộng hơn, không chỉ trong cốc ; phải chia cho $S$."),
     ("Lấy luôn độ dâng sau khi rót nước, không trừ độ dâng ở câu a", False, "Đề hỏi dâng thêm so với câu a nên chỉ lấy phần tăng thêm.")]),
 bu("Sỏi nằm trong cốc", "Với sỏi nằm trong cốc, mực nước bình dâng thêm bao nhiêu xentimét so với câu a?", 0.5, "cm", 0.02,
    "Dùng thể tích thật của sỏi để tính phần nước bị chiếm chỗ, trong khi sỏi nổi nhờ cốc.",
    [("Cốc vẫn nổi : nước bị chiếm chỗ thêm có khối lượng bằng khối lượng sỏi", True, ""),
     ("Nước bị chiếm chỗ thêm có thể tích bằng thể tích thật của sỏi", False, "Đó là khi sỏi chìm hẳn xuống đáy ; sỏi trong cốc đang nổi cùng cốc nên chiếm chỗ theo khối lượng."),
     ("Cốc nổi nên mực nước bình không đổi", False, "Cốc chìm sâu thêm để đỡ sỏi nên nước vẫn bị chiếm chỗ thêm và mực nước dâng.")]),
 bu("Sỏi thả xuống đáy bình", "Với sỏi thả xuống đáy bình, mực nước bình dâng thêm bao nhiêu xentimét so với câu a?", 0.2, "cm", 0.02,
    "Coi sỏi chiếm chỗ theo khối lượng như khi nổi, hoặc quên đổi khối lượng riêng nên tính sai thể tích sỏi.",
    [("Sỏi chìm hẳn : nước bị chiếm chỗ bằng thể tích thật $V=\\dfrac{m}{D}$", True, ""),
     ("Sỏi vẫn chiếm chỗ theo khối lượng như khi nổi", False, "Sỏi nằm dưới đáy được đáy bình đỡ, không còn nổi nên chỉ chiếm chỗ đúng thể tích thật."),
     ("Sỏi nằm dưới đáy nên không làm mực nước thay đổi", False, "Sỏi vẫn chiếm một thể tích trong nước nên mực nước vẫn dâng.")]),
 bc("Trường hợp nào mực nước cao hơn", "Trường hợp nào làm mực nước bình cao hơn?",
    [("Sỏi nằm trong cốc", True, ""),
     ("Sỏi thả xuống đáy bình", False, "Sỏi dưới đáy chỉ chiếm chỗ thể tích thật nhỏ hơn nên mực nước thấp hơn."),
     ("Hai trường hợp như nhau vì cùng một hòn sỏi", False, "Sỏi trong cốc chiếm chỗ theo khối lượng, sỏi dưới đáy chiếm chỗ theo thể tích thật ; hai giá trị này khác nhau vì sỏi nặng hơn nước.")],
    "Cho rằng hai trường hợp như nhau vì \"cùng hòn sỏi\" — quên một bên chiếm chỗ theo khối lượng, một bên theo thể tích.",
    [("So hai độ dâng vừa tìm được", True, ""),
     ("Kết luận ngay là như nhau vì khối lượng sỏi không đổi", False, "Khối lượng giống nhau nhưng cách chiếm chỗ khác nhau nên độ dâng khác nhau."),
     ("Tính lại lực đẩy lên cốc rỗng", False, "Lực đẩy lên cốc rỗng không đổi giữa hai trường hợp, không giúp so sánh.")]),
 bu("Chênh lệch giữa hai trường hợp", "Mực nước ở hai trường hợp chênh nhau bao nhiêu xentimét (lấy số lớn trừ số nhỏ)?", 0.3, "cm", 0.02,
    "Cộng hai độ dâng thay vì lấy hiệu.",
    [("Lấy hiệu hai độ dâng đã tìm", True, ""),
     ("Cộng hai độ dâng", False, "Hai trường hợp là hai tình huống tách rời, không xảy ra cùng lúc ; so sánh phải lấy hiệu."),
     ("Lấy hiệu của hai thể tích chiếm chỗ rồi chia cho tiết diện cốc", False, "Độ dâng của mực nước bình phải chia cho tiết diện bình.")]),
 bu("Lượng nước tối đa rót vào cốc", "Rót nước vào cốc tối đa bao nhiêu gam thì miệng cốc vừa chạm mặt nước?", 400, "g", 5,
    "Lấy $S$ của bình thay vì $S_c$ khi tính thể tích chìm tối đa, hoặc quên trừ khối lượng cốc.",
    [("Chìm tối đa $12\\ \\text{cm}$ : $V_{chìm,max}=S_c\\,h_c$, rồi trừ khối lượng cốc", True, ""),
     ("Đổ đầy cốc : $m=D_n\\,S_c\\,h_c$ (không trừ khối lượng cốc)", False, "Khi miệng cốc chạm mặt nước, khối lượng cốc và nước cộng lại mới bằng khối lượng nước chiếm chỗ ; phải trừ khối lượng cốc."),
     ("$V_{chìm,max}=S\\,h_c$ (tiết diện bình)", False, "Phần chìm của cốc là hình trụ tiết diện $S_c$, không phải tiết diện bình.")]),
 {"tieu_de": "Kiểm tra"},
]
d9 = dict(form="bai_tap", label="Bài 9 · Vận dụng cao · Cốc nổi trong bình — mực nước thay đổi thế nào? · Thứ Năm 15/10", topic="Lực đẩy Archimedes và điều kiện nổi",
          problem_html=prob9, analysis_html=ana9, solution_html=sol9, cap_do=3, fading="giau_het",
          nhan_dang="Thấy <b>vật nổi trong bình, hỏi mực nước</b> → vật nổi chiếm chỗ theo <b>khối lượng</b>, vật chìm chiếm chỗ theo <b>thể tích</b>.",
          buoc=b9, go_roi={"buoc_hay_sai": 5})

out = {"lesson_id": 167, "lesson_title": "Bài tập tuần này: 12 bài tự luận Cơ học", "review": {"checked": True, "notes": "tạm, chờ kiểm chéo"}, "dang_bai": [d7, d8, d9]}
(HERE / "part-C.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
print("ok", [len(d["buoc"]) for d in out["dang_bai"]])
