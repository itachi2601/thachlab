#!/usr/bin/env python3
"""Dựng trang XEM THỬ cho một bài lý thuyết (không cần Playwright — chỉ cần Google Chrome).

Dùng (chạy từ gốc repo thachlab):
  python3 build_preview.py <theory.html> [thư-mục-ra] [--tieu-de "…"] [--phu-de "…"]

Sinh ra (mặc định trong <thư-mục-bài>/xem-thu/):
  xem-thu.html    — trang rời, mở bằng Chrome là bấm thử được ngay (radio + <details>), có nút mở hết đáp án
  kiem-quiz.html  — tự bấm mọi đáp án khi mở bằng trình duyệt (bản kiểm nhanh bằng mắt;
                    bản kiểm tự động không cần trình duyệt là check_quizzes.py)
  sec-<n>.html    — từng mục <h3> ở bề ngang 375px, mở sẵn <details> + đặt sẵn "checked" vào đáp án ĐÚNG
  sec-sai.html    — quiz đầu tiên với đáp án SAI được chọn (để chụp phản hồi đỏ)
  fig-<n>.html    — từng hình SVG

CSS lấy đúng từ app/globals.css (khối hình vẽ + khối .tl-*), KaTeX lấy từ node_modules.
Sau bước này chụp ảnh bằng: python3 chup_anh.py <thư-mục-ra>
"""
import pathlib, re, sys

SKILL_SCRIPTS = pathlib.Path(__file__).resolve().parent
CSS_MARK_A = "/* Hình vẽ SVG nội tuyến"
CSS_MARK_B = "/* ---------- Nội dung bài viết blog"
CSS_MARK_C = "/* Bài lý thuyết tương tác"


def repo_root(start: pathlib.Path) -> pathlib.Path:
    p = start.resolve()
    for cand in [p, *p.parents]:
        if (cand / "app" / "globals.css").exists() and (cand / "node_modules" / "katex").exists():
            return cand
    raise SystemExit("Không tìm thấy gốc repo thachlab (cần app/globals.css và node_modules/katex)")


CSS_EXTRA = """
.exam-content figure.fig{max-width:min(100%,420px);margin:.9rem auto}
.exam-content figure.fig svg{display:block;width:100%;height:auto}
.exam-content figure.fig figcaption{margin-top:.35rem;font-size:.85em;color:#94a3b8;text-align:center}
"""

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

BAR = """
const bar=document.createElement('div');
bar.style.cssText='position:sticky;top:0;z-index:9;background:#0b1220;border-bottom:1px solid #1e293b;padding:8px 16px;margin:-20px -16px 16px;display:flex;gap:8px;align-items:center;font-size:12px;color:#94a3b8';
const b1=document.createElement('button');b1.textContent='Mở tất cả đáp án';
const b2=document.createElement('button');b2.textContent='Đóng lại';
for(const b of [b1,b2]) b.style.cssText='background:#1e293b;color:#e2e8f0;border:0;border-radius:8px;padding:6px 10px;font-size:12px;cursor:pointer';
b1.onclick=()=>document.querySelectorAll('details').forEach(d=>d.open=true);
b2.onclick=()=>document.querySelectorAll('details').forEach(d=>d.open=false);
bar.append(b1,b2);document.body.prepend(bar);
"""

CHECK = """
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


def open_all(h):
    return h.replace('<details class="tl-details">', '<details class="tl-details" open>')


def check_ok(h):
    return re.sub(r'<input type="radio" name="([^"]+)" id="([^"]+)">(<label for="\2" class="tl-opt tl-ok">)',
                  r'<input type="radio" name="\1" id="\2" checked>\3', h)


def check_no(h, limit=1):
    n = [0]

    def rep(m):
        n[0] += 1
        return (f'<input type="radio" name="{m.group(1)}" id="{m.group(2)}" checked>'
                f'<label for="{m.group(2)}" class="tl-opt tl-no">') if n[0] <= limit else m.group(0)

    return re.sub(r'<input type="radio" name="([^"]+)" id="([^"]+)">(<label for="\2" class="tl-opt tl-no">)', rep, h)


def main(argv):
    flags = {"--tieu-de": "Bài lý thuyết (bản xem thử)", "--phu-de": "BẢN XEM THỬ — chưa đăng lên web."}
    rest = []
    i = 0
    while i < len(argv):
        if argv[i] in flags:
            flags[argv[i]] = argv[i + 1]
            i += 2
        else:
            rest.append(argv[i])
            i += 1
    if not rest:
        print(__doc__)
        return 1

    theory_path = pathlib.Path(rest[0]).resolve()
    out = pathlib.Path(rest[1]).resolve() if len(rest) > 1 else theory_path.parent / "xem-thu"
    out.mkdir(parents=True, exist_ok=True)

    ROOT = repo_root(theory_path.parent)
    g = (ROOT / "app" / "globals.css").read_text(encoding="utf8")
    css = (g[g.index(CSS_MARK_A):g.index(CSS_MARK_B)] + g[g.index(CSS_MARK_C):] + CSS_EXTRA)
    katex = (ROOT / "node_modules" / "katex" / "dist").as_uri()
    theory = theory_path.read_text(encoding="utf8")
    title, sub = flags["--tieu-de"], flags["--phu-de"]

    def page(body, script=""):
        head = (f'<h1>{title}</h1><p class="sub">{sub}</p>' if title else "") + f'<span class="exam-content">{body}</span>'
        html = BASE.format(katex=katex, css=css, body=f'<div class="wrap">{head}</div>')
        return html.replace("</html>", f"<script>{script}</script></html>") if script else html

    (out / "xem-thu.html").write_text(page(theory, BAR), encoding="utf8")
    (out / "kiem-quiz.html").write_text(page(theory, CHECK), encoding="utf8")

    parts = re.split(r"(?=<h3>)", theory)
    for i, body in enumerate(parts):
        (out / f"sec-{i}.html").write_text(page(check_ok(open_all(body))), encoding="utf8")

    first_quiz = re.search(r'<div class="tl-quiz">.*?</div>\n</div>', theory, re.S)
    if first_quiz:
        wrong = theory[:first_quiz.start()] + check_no(first_quiz.group(0)) + theory[first_quiz.end():]
        (out / "sec-sai.html").write_text(page(open_all(wrong)), encoding="utf8")

    figs = re.findall(r'<figure class="fig".*?</figure>', theory, re.S)
    for i, f in enumerate(figs, 1):
        (out / f"fig-{i}.html").write_text(page(f), encoding="utf8")

    print(f"{out}: xem-thu.html · kiem-quiz.html · {len(parts)} mục · {len(figs)} hình")
    print(f"chụp ảnh: python3 {SKILL_SCRIPTS / 'chup_anh.py'} {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
