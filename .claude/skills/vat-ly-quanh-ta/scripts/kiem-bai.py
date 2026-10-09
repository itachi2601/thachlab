#!/usr/bin/env python3
"""Kiểm bài "Vật lý quanh ta" trước khi commit + tra bài học thachlab.

  python3 kiem-bai.py content/blog/<slug>.md   # kiểm một bài (exit 1 nếu có ✗)
  python3 kiem-bai.py --tim "áp suất"          # tìm bài học trong public/data/catalog.json, in link
  python3 kiem-bai.py --da-viet                # liệt kê các bài category "Vật lý quanh ta" đã có
"""
import json
import re
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import yaml

ROOT = Path(__file__).resolve().parents[4]
CATALOG = ROOT / "public/data/catalog.json"
BLOG = ROOT / "content/blog"
CATEGORY = "Vật lý quanh ta"
MUC_BAT_BUOC = ["Đoán thử", "Thử ước lượng", "Tự thử ở nhà|Quan sát ở nhà", "Hiểu lầm hay gặp",
                "Em đã học ở đâu", "Nghĩ tiếp", "Nguồn"]


def catalog():
    c = json.loads(CATALOG.read_text())
    classes = {x["id"]: x["name"] for x in c["classes"]}
    chapters = {x["id"]: x for x in c["chapters"]}
    return classes, chapters, c["lessons"]


def doc_bai(path: Path):
    raw = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
    if not m:
        return None, raw
    return yaml.safe_load(m.group(1)) or {}, m.group(2)


def tim(tu: str):
    classes, chapters, lessons = catalog()
    tu = tu.lower()
    for l in lessons:
        ch = chapters.get(l["chapter_id"], {})
        text = f'{l["title"]} {l.get("description") or ""} {ch.get("title", "")}'.lower()
        if tu in text and not l["title"].startswith(("Kiểm tra", "Đề ")):
            lop = ", ".join(classes.get(i, "?") for i in ch.get("classIds", []))
            lop = lop if lop.startswith("KHTN") else f"Lớp {lop}"
            sub = ch.get("subjectCode", "vat-ly")
            pub = "" if l.get("published") else "  (CHƯA hiện)"
            print(f'[{lop} · {l["title"]}](/lop-hoc/bai?id={l["id"]}&subject={sub}&chapter={l["chapter_id"]}){pub}')


def da_viet():
    for p in sorted(BLOG.glob("*.md")):
        fm, _ = doc_bai(p)
        if fm and fm.get("category") == CATEGORY:
            print(f'{fm.get("date")}  {p.stem}  — {fm.get("title")}')


def kiem(path: Path) -> int:
    loi, canh = [], []
    fm, body = doc_bai(path)
    if fm is None:
        print("✗ thiếu frontmatter ---")
        return 1
    for k in ["title", "description", "date", "category", "tags", "keywords"]:
        if not fm.get(k):
            loi.append(f"frontmatter thiếu `{k}`")
    if fm.get("category") != CATEGORY:
        loi.append(f'category phải là "{CATEGORY}"')
    if len(str(fm.get("title", ""))) > 70:
        canh.append("title > 70 ký tự")
    d = len(str(fm.get("description", "")))
    if d and not 100 <= d <= 200:
        canh.append(f"description {d} ký tự (nên 120–180)")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(fm.get("date", ""))):
        loi.append("date phải dạng yyyy-mm-dd")
    if path.stem != re.sub(r"[^a-z0-9-]", "", path.stem):
        loi.append("tên file chỉ gồm a-z, 0-9, gạch nối")

    so_chu = len(body.split())
    if so_chu < 600:
        loi.append(f"thân bài {so_chu} chữ (< 600)")
    elif not 700 <= so_chu <= 1300:
        canh.append(f"thân bài {so_chu} chữ (nên 700–1200)")

    if re.search(r"(?<!\\)\$[^$\n]+\$", body):
        loi.append("có $…$ — blog không render KaTeX, viết công thức Unicode")
    if re.search(r"\b[Tt]hầy\s+(sẽ|đã|muốn|nghĩ|thấy|hỏi|kể)|\b(cho|với|như) thầy\b", body):
        loi.append("thân bài tự xưng 'thầy' — dùng em/chúng ta")
    if "<script" in body.lower() or "base64," in body:
        loi.append("có <script> hoặc base64")

    heads = re.findall(r"^##\s+(.+)$", body, re.M)
    for muc in MUC_BAT_BUOC:
        if not any(re.search(muc, h) for h in heads):
            loi.append(f"thiếu mục ## {muc}")

    nguon = body.split("## Nguồn", 1)[1] if "## Nguồn" in body else ""
    if not re.search(r"\]\(https://", nguon):
        loi.append("mục Nguồn chưa có link https")

    _, _, lessons = catalog()
    ids = {l["id"] for l in lessons}
    links = re.findall(r"\]\((/lop-hoc/bai\?[^)\s]+)\)", body)
    if not links:
        canh.append("chưa link bài học thachlab nào (mục Em đã học ở đâu)")
    for u in links:
        q = parse_qs(urlparse(u).query)
        try:
            if int(q["id"][0]) not in ids:
                loi.append(f"link bài không có trong catalog: {u}")
        except (KeyError, ValueError):
            loi.append(f"link bài sai dạng: {u}")

    imgs = re.findall(r"!\[[^\]]*\]\(([^)\s]+)\)", body)
    if fm.get("cover"):
        imgs.append(fm["cover"])
    for src in imgs:
        if src.startswith("http"):
            loi.append(f"ảnh ngoài site (bản quyền/tốc độ): {src}")
            continue
        f = ROOT / "public" / src.lstrip("/")
        if not f.exists():
            loi.append(f"thiếu file ảnh {src}")
            continue
        kb = f.stat().st_size / 1024
        if kb > 150:
            loi.append(f"ảnh {src} {kb:.0f} KB > 150 KB")
        if f.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
            from PIL import Image
            w = Image.open(f).size[0]
            if w > 1200:
                loi.append(f"ảnh {src} rộng {w}px > 1200")
    if len(re.findall(r"!\[", body)) > 3:
        canh.append("hơn 3 hình trong bài")

    for c in canh:
        print("⚠", c)
    for l in loi:
        print("✗", l)
    print(f"{'✓ đạt' if not loi else '✗ chưa đạt'} — {so_chu} chữ, {len(links)} link bài, {len(imgs)} ảnh")
    return 1 if loi else 0


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        sys.exit(2)
    if a[0] == "--tim":
        tim(" ".join(a[1:]))
    elif a[0] == "--da-viet":
        da_viet()
    else:
        sys.exit(kiem(Path(a[0])))
