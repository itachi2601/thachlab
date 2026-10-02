#!/usr/bin/env python3
"""Dựng trang XEM THỬ cho bài lý thuyết (không cần Playwright — dùng Google Chrome headless).

Sinh trong xem-thu/:
  xem-thu.html        — trang rời, mở bằng Chrome là bấm thử được ngay (radio + <details>)
  kiem-quiz.html      — trang tự bấm mọi đáp án rồi ghi kết quả vào #ket-qua (đọc bằng --dump-dom)
  sec-<n>.html        — từng mục <h3> ở bề ngang 375px, đã mở hết <details> + chọn sẵn đáp án đúng (để chụp ảnh)
  fig-<n>.html        — từng hình SVG (để chụp ảnh kiểm nhãn/chồng chữ)

Dùng: python3 build_preview.py   (chạy tại thư mục bài, gốc repo thachlab)
"""
import os, re, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = HERE / "xem-thu"
OUT.mkdir(exist_ok=True)

theory = (HERE / "theory.html").read_text(encoding="utf8")
g = (ROOT / "app/globals.css").read_text(encoding="utf8")
css = (g[g.index("/* Hình vẽ SVG nội tuyến"):g.index("/* ---------- Nội dung bài viết blog")]
       + g[g.index("/* Bài lý thuyết tương tác"):])
katex = (ROOT / "node_modules/katex/dist").as_uri()

BASE = """<!doctype html><html lang="vi"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="stylesheet" href="{katex}/katex.min.css">
<style>
:root{{color-scheme:dark}}
body{{margin:0;background:#0f172a;color:#e2e8f0;font:16px/1.75 system-ui,-apple-system,"Segoe UI",sans-serif}}
.wrap{{max-width:720px;margin:0 auto;padding:20px 16px 64px}}
.exam-content{{display:block}}
h1{{font-size:20px;margin:0 0 4px}} .sub{{color:#94a3b8;font-size:13px;margin:0 0 16px}}
{css}
</style>
{body}
<script src="{katex}/katex.min.js"></script>
<script src="{katex}/contrib/auto-render.min.js"></script>
<script>
renderMathInElement(document.body,{{delimiters:[{{left:"$$",right:"$$",display:true}},{{left:"$",right:"$",display:false}}]}});
</script>
</html>"""

def page(title, subtitle, body, extra_script=""):
    head = ((f'<h1>{title}</h1><p class="sub">{subtitle}</p>' if title else "")
            + f'<span class="exam-content">{body}</span>')
    html = BASE.format(katex=katex, css=css, body=f'<div class="wrap">{head}</div>')
    if extra_script:
        html = html.replace("</html>", f"<script>{extra_script}</script></html>")
    return html

TITLE = "Bài 8. Mô tả sóng (Vật lí 11 — Chương 2: Sóng)"
SUB = "BẢN XEM THỬ — chưa đăng lên web. Bấm được đáp án và mở được ô “bấm xem”."

# 1. Trang xem thử đầy đủ (giữ nguyên trạng thái thu gọn, có nút mở hết đáp án)
open_script = """
const bar=document.createElement('div');
bar.style.cssText='position:sticky;top:0;z-index:9;background:#0b1220;border-bottom:1px solid #1e293b;padding:8px 16px;margin:-20px -16px 16px;display:flex;gap:8px;align-items:center;font-size:12px;color:#94a3b8';
const b1=document.createElement('button');b1.textContent='Mở tất cả đáp án';
const b2=document.createElement('button');b2.textContent='Đóng lại';
for(const b of [b1,b2]) b.style.cssText='background:#1e293b;color:#e2e8f0;border:0;border-radius:8px;padding:6px 10px;font-size:12px;cursor:pointer';
b1.onclick=()=>document.querySelectorAll('details').forEach(d=>d.open=true);
b2.onclick=()=>document.querySelectorAll('details').forEach(d=>d.open=false);
bar.append(b1,b2);document.body.prepend(bar);
"""
(OUT / "xem-thu.html").write_text(page(TITLE, SUB, theory, open_script), encoding="utf8")

# 2. Trang tự kiểm quiz (chọn từng đáp án, đối chiếu phản hồi hiện ra)
check_script = """
const out=[];
document.querySelectorAll('.tl-quiz').forEach((q,i)=>{
  const res=[];
  q.querySelectorAll('label.tl-opt').forEach(l=>{
    l.click();
    const fb=[...q.querySelectorAll('.tl-fb')].map(x=>getComputedStyle(x).display==='block');
    const ok=l.classList.contains('tl-ok');
    res.push(ok ? (fb[0]&&!fb[1]?'✓':'✗LỖI') : (!fb[0]&&fb[1]?'✓':'✗LỖI'));
  });
  out.push('quiz '+(i+1)+' ('+q.querySelectorAll('label.tl-opt').length+' đáp án): '+res.join(' '));
});
document.title='XONG';
const p=document.createElement('pre');p.id='ket-qua';p.textContent=out.join('\\n');
document.body.append(p);
"""
(OUT / "kiem-quiz.html").write_text(page("", "", theory, check_script), encoding="utf8")

# 3. Từng mục <h3> cho ảnh chụp: mở sẵn <details> + đặt sẵn "checked" vào đáp án đúng
#    (không cần JS: CSS :has(input:checked + .tl-ok) tự hiện phản hồi xanh khi chụp)
def open_all(h):
    return h.replace('<details class="tl-details">', '<details class="tl-details" open>')


def check_ok(h):
    return re.sub(r'<input type="radio" name="([^"]+)" id="([^"]+)">(<label for="\2" class="tl-opt tl-ok">)',
                  r'<input type="radio" name="\1" id="\2" checked>\3', h)


def check_no(h, limit=1):
    """Chọn đáp án SAI đầu tiên (để chụp thử phản hồi đỏ)."""
    n = [0]

    def rep(m):
        n[0] += 1
        return (f'<input type="radio" name="{m.group(1)}" id="{m.group(2)}" checked>'
                f'<label for="{m.group(2)}" class="tl-opt tl-no">') if n[0] <= limit else m.group(0)

    return re.sub(r'<input type="radio" name="([^"]+)" id="([^"]+)">(<label for="\2" class="tl-opt tl-no">)', rep, h)


parts = re.split(r"(?=<h3>)", theory)
for i, body in enumerate(parts):
    body = check_ok(open_all(body))
    (OUT / f"sec-{i}.html").write_text(
        page("", "", body) if i else page(TITLE, SUB, body), encoding="utf8")

# 3b. Trang chụp thử phản hồi ĐỎ: chọn đáp án sai ở quiz đầu tiên
first_quiz = re.search(r'<div class="tl-quiz">.*?</div>\n</div>', theory, re.S)
if first_quiz:
    wrong = theory[:first_quiz.start()] + check_no(first_quiz.group(0)) + theory[first_quiz.end():]
    (OUT / "sec-sai.html").write_text(page(TITLE, SUB, open_all(wrong)), encoding="utf8")

# 4. Từng hình SVG
figs = re.findall(r'<figure class="fig".*?</figure>', theory, re.S)
for i, f in enumerate(figs, 1):
    (OUT / f"fig-{i}.html").write_text(page("", "", f), encoding="utf8")

print(f"xem-thu.html · kiem-quiz.html · {len(parts)} mục · {len(figs)} hình  ->  {OUT}")
