#!/usr/bin/env python3
"""Dựng gói bài học (thachlab.lesson-bundle/v1) cho lớp "Giải Vật lí trên máy tính cầm tay" từ
content/casio-vat-ly/wp-0X-*/ (ky-thuat.md hoặc so-tay.md, bai-luyen.md, mini-test.md).

  python3 scripts/build-casio-vat-ly.py          # ghi content/casio-vat-ly/_dung/<gói>/bundle.json + xem-thu.html
Chạy được trên cloud (cần pandoc). Không ghi DB: đăng bằng scripts/dang-casio-vat-ly.sh.
"""
import json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "content" / "casio-vat-ly"
OUT = ROOT / "_dung"
CLASS = "Giải Vật lí trên máy tính cầm tay"
CHAPTER = "Giải Vật lí bằng Casio fx-580VN X"

PACKS = [
    dict(dir="wp-01-so-tay-fx580vnx", lesson="Sổ tay máy Casio fx-580VN X", theory="so-tay.md", mini=None,
         exam_ids=["S1", "T1", "X1", "St2"], topic="Casio VL: Thao tác máy", exam_title="Luyện thao tác máy: 4 bài",
         sub="Sổ tay 8 mục · 20 bài luyện thao tác"),
    dict(dir="wp-03-dao-dong-co", lesson="Dao động cơ", theory="ky-thuat.md", mini="mini-test.md",
         topic="Casio VL: Dao động cơ", exam_title="Mini-test 30 phút: Dao động cơ", sub="3 trang kỹ thuật · 12 bài luyện"),
    dict(dir="wp-04-song-co", lesson="Sóng cơ", theory="ky-thuat.md", mini="mini-test.md",
         topic="Casio VL: Sóng cơ", exam_title="Mini-test 30 phút: Sóng cơ", sub="3 trang kỹ thuật · 12 bài luyện"),
    dict(dir="wp-05-dien-xoay-chieu", lesson="Điện xoay chiều", theory="ky-thuat.md", mini="mini-test.md",
         topic="Casio VL: Điện xoay chiều", exam_title="Mini-test 30 phút: Điện xoay chiều", sub="3 trang kỹ thuật · 12 bài luyện"),
    dict(dir="wp-06-dien-tu-anh-sang", lesson="Điện từ và sóng ánh sáng", theory="ky-thuat.md", mini="mini-test.md",
         topic="Casio VL: Điện từ và sóng ánh sáng", exam_title="Mini-test 30 phút: Điện từ và sóng ánh sáng",
         sub="3 trang kỹ thuật · 12 bài luyện"),
]

SOFT = [  # câu dành cho người soạn, không để lọt lên trang học sinh
    (re.compile(r"\s*\(bài học từ kiểm chéo WP-0\d\)"), ""),
    (re.compile(r" và thầy đã thử máy thật \(19/10/2026; xem `README\.md`\)"), " (cập nhật 19/10/2026)"),
    (re.compile(r"`?\.\./wp-01-so-tay-fx580vnx/so-tay\.md`?"), "bài **Sổ tay máy Casio fx-580VN X**"),
]


LIST_RX = re.compile(r"^\s*([-*]|\d+\.)\s")


def clean(md: str) -> str:
    for rx, rep in SOFT:
        md = rx.sub(rep, md)
    out, prev = [], ""
    for line in md.split("\n"):
        # Markdown của pandoc đòi dòng trống trước danh sách; file nguồn viết liền ngay sau dòng chữ.
        if LIST_RX.match(line) and prev.strip() and not LIST_RX.match(prev) and not prev.startswith((" ", "\t")):
            out.append("")
        elif LIST_RX.match(prev) and line.strip() and not LIST_RX.match(line) and not line.startswith((" ", "\t")):
            out.append("")  # dòng chữ ngay sau mục danh sách (Bẫy, Ghi chú…) là đoạn riêng, không nuốt vào mục
        out.append(line)
        prev = line
    return "\n".join(out)


def pandoc(md: str, shift: int = 0) -> str:
    html = subprocess.run(
        ["pandoc", "-f", "markdown+hard_line_breaks-smart", "-t", "html", "--mathjax", "--wrap=none", f"--shift-heading-level-by={shift}"],
        input=clean(md), capture_output=True, text=True, check=True).stdout
    html = re.sub(r'<span class="math inline">\\\((.*?)\\\)</span>', r"$\1$", html, flags=re.S)
    html = re.sub(r'<span class="math display">\\\[(.*?)\\\]</span>', r"$$\1$$", html, flags=re.S)
    return html.strip()


def problems(md: str):
    """[(id, tiêu đề đầy đủ, khối md)] theo tiêu đề dạng '## D1 ⭐ …' hoặc '### S1 ⭐⭐ …'."""
    parts = re.split(r"(?m)^#{2,3} (?=[A-Za-z]+\d+ )", md)
    out = []
    for p in parts[1:]:
        head, _, body = p.partition("\n")
        out.append((head.split()[0], head.strip(), body.strip().rstrip("-").strip()))
    return out


def split_answer(body: str):
    m = re.search(r"(?m)^\*\*Đáp số[^*]*\*\*", body)
    if not m:
        return body, ""
    return body[: m.start()].strip(), body[m.start():].strip()


def strip_lead(de: str) -> str:
    return re.sub(r"^\*\*Đề\.\*\*\s*", "", de)


def worked(md: str):
    items = []
    for pid, head, body in problems(md):
        de, ans = split_answer(body)
        if not ans:
            sys.exit(f"{pid}: không thấy '**Đáp số.**'")
        html = pandoc(strip_lead(de)) + '\n<details class="casio-ans"><summary>Xem đáp số và cách bấm máy</summary>\n' + pandoc(ans) + "\n</details>"
        items.append(dict(label=head, body_html=html))
    return items


def essay(q_md: str, ans_md: str, topic: str, level: str = "trung-binh"):
    return dict(type="essay", question=q_md.strip(), suggestedAnswer=ans_md.strip(),
                gradingGuide="Đúng đáp số (sai khác chỉ ở chữ số làm tròn thứ 4) và nêu được thao tác máy chính; thiếu đơn vị hoặc đổi đơn vị sai trừ điểm.",
                explanation=ans_md.strip(), topic=topic, form="ly_thuyet", difficulty=level)


def mini_questions(md: str, topic: str):
    de_part, _, ans_part = md.partition("## Đáp án")
    def by_m(text):
        d = {}
        for m in re.finditer(r"(?ms)^\*\*(M\d+)\.\*\*\s*(.*?)(?=^\*\*M\d+\.\*\*|\Z)", text):
            d[m.group(1)] = m.group(2).strip().rstrip("-").strip()
        return d
    qs, ans = by_m(de_part), by_m(ans_part)
    if not qs or set(qs) != set(ans):
        sys.exit(f"mini-test: đề {sorted(qs)} khác đáp án {sorted(ans)}")
    return [essay(qs[k], ans[k], topic, "kho" if False else "trung-binh") for k in sorted(qs)]


def build(p):
    d = ROOT / p["dir"]
    tmd = (d / p["theory"]).read_text(encoding="utf-8")
    tmd = re.sub(r"(?m)^# .*\n", "", tmd, count=1)  # bỏ H1
    theory = pandoc(tmd, shift=1)
    bl = (d / "bai-luyen.md").read_text(encoding="utf-8")
    we = worked(bl)
    if p["mini"]:
        qs = mini_questions((d / p["mini"]).read_text(encoding="utf-8"), p["topic"])
    else:
        probs = {pid: (head, body) for pid, head, body in problems(bl)}
        qs = []
        for pid in p["exam_ids"]:
            de, ans = split_answer(probs[pid][1])
            qs.append(essay(strip_lead(de), ans, p["topic"]))
    bundle = dict(
        schema="thachlab.lesson-bundle/v1",
        target=dict(class_name=CLASS, chapter_title=CHAPTER, lesson_title=p["lesson"]),
        theory_title="Kỹ thuật bấm máy" if p["mini"] else "Sổ tay máy",
        theory_subtitle=p["sub"],
        theory_html=theory,
        worked_examples=we,
        exam=dict(title=p["exam_title"], topic=p["topic"], difficulty="trung-binh", duration_minutes=30,
                  subject_code="casio-vat-ly", questions=qs, new_topics=[p["topic"]]),
        raster_images=[],
    )
    return bundle


def preview(b, title):
    parts = [f"<h1>{title}</h1>", b["theory_html"]]
    parts += [f"<h3>{w['label']}</h3>{w['body_html']}" for w in b["worked_examples"]]
    parts += [f"<h3>Câu {i+1}</h3><p>{q['question']}</p><details><summary>Đáp án</summary><pre>{q['suggestedAnswer']}</pre></details>" for i, q in enumerate(b["exam"]["questions"])]
    return ('<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">'
            '<style>body{font:16px/1.6 system-ui;max-width:720px;margin:0 auto;padding:16px}code{background:#eee;padding:1px 4px;border-radius:4px}</style>'
            + "".join(parts) +
            '<script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>'
            '<script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>'
            '<script>renderMathInElement(document.body,{delimiters:[{left:"$$",right:"$$",display:true},{left:"$",right:"$",display:false}]})</script>')


if __name__ == "__main__":
    for p in PACKS:
        b = build(p)
        o = OUT / p["dir"]
        o.mkdir(parents=True, exist_ok=True)
        (o / "bundle.json").write_text(json.dumps(b, ensure_ascii=False, indent=1), encoding="utf-8")
        (o / "xem-thu.html").write_text(preview(b, p["lesson"]), encoding="utf-8")
        print(f"{p['lesson']}: lý thuyết {len(b['theory_html'])//1024} KB · {len(b['worked_examples'])} bài luyện · {len(b['exam']['questions'])} câu mini-test")
