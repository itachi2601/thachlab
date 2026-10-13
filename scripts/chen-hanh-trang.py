#!/usr/bin/env python3
"""Chèn khối "🧰 Kiểm tra hành trang" (2–3 câu tự chấm về kiến thức nền Toán/Vật lí + phần nhắc nhanh)
vào bài lý thuyết tương tác, ngay TRƯỚC mục lý thuyết đầu tiên (<h3>II.), tức là sau Mở bài + Dự đoán.

Dữ liệu: content/hanh-trang/<slug>.json (khoá: lesson_id, dung_lai, cau[{hoi, pa[], dung, ok, no[]}], nhac[], xem_lai).
Ghi vào content/lesson-samples/<slug>/: theory.src.html, theory.html, bundle.json (theory_html = theory.html).
Chạy lại được: khối nằm giữa <!--hanh-trang--> … <!--/hanh-trang--> nên chạy lần nữa là thay, không nhân đôi.

  python3 scripts/chen-hanh-trang.py                        # dry-run mọi bài có dữ liệu
  python3 scripts/chen-hanh-trang.py --bai l10-luc-ma-sat --apply
  python3 scripts/chen-hanh-trang.py --apply --nen <thư-mục>  # lấy <thư-mục>/<lesson_id>.html (bản body_html
                                                              # kéo từ DB) làm nền cho theory.html thay bản trong repo
Đăng: bash scripts/cap-nhat-ly-thuyet.sh content/lesson-samples/<slug>/theory.html <lesson_id>
Lý do sư phạm: docs/PHUONG-PHAP-NOI-DUNG-LY-THUYET.md mục "Kiểm tra hành trang".
"""
import argparse, html, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "content/hanh-trang"
LESSONS = ROOT / "content/lesson-samples"
MO, DONG = "<!--hanh-trang-->", "<!--/hanh-trang-->"
MOC = re.compile(r"^<h3>II\.", re.M)
NHAN = "ABCD"


def render(slug: str, d: dict) -> str:
    lid = d["lesson_id"]
    out = [MO, '<div class="tl-box tl-box--think tl-hanh-trang">',
           '<p class="tl-label">🧰 Kiểm tra hành trang</p>',
           f'<p>Bài này dùng lại {d["dung_lai"]}.<br>Sai câu nào thì mở <strong>Nhắc nhanh</strong> ngay dưới.</p>']
    for i, c in enumerate(d["cau"], 1):
        if not 0 <= c["dung"] < len(c["pa"]) or len(c["pa"]) != 4:
            sys.exit(f"✗ {slug} câu {i}: cần 4 phương án và chỉ số đáp án hợp lệ")
        name = f"ht{lid}-q{i}"
        out.append(f'<p><strong>Câu {i}.</strong> {c["hoi"]}</p>')
        out.append('<div class="tl-quiz">')
        for j, pa in enumerate(c["pa"]):
            cls = "tl-ok" if j == c["dung"] else "tl-no"
            out.append(f'<input type="radio" name="{name}" id="{name}{"abcd"[j]}">'
                       f'<label for="{name}{"abcd"[j]}" class="tl-opt {cls}">{NHAN[j]}. {pa}</label>')
        out.append(f'<div class="tl-fb tl-fb--ok"><p><strong>Chính xác.</strong> {c["ok"]}</p></div>')
        out.append('<div class="tl-fb tl-fb--no"><p><strong>Chưa đúng.</strong><br>' + "<br>".join(c["no"])
                   + '</p></div>')
        out.append('</div>')
    out.append('<details class="tl-details">')
    out.append('<summary>📌 Nhắc nhanh kiến thức cần dùng</summary>')
    out.append("<ul>" + "".join(f"<li>{x}</li>" for x in d["nhac"]) + "</ul>")
    out.append(f'<p>Xem lại: {html.escape(d["xem_lai"], quote=False)}</p>')
    out.append('</details>')
    out.append('</div>')
    out.append(DONG)
    return "\n".join(out) + "\n\n"


def chen(text: str, block: str, slug: str, ten: str) -> str:
    if MO in text:
        a, b = text.index(MO), text.index(DONG) + len(DONG)
        rest = text[b:].lstrip("\n")
        return text[:a] + block + rest
    m = MOC.search(text)
    if not m:
        sys.exit(f"✗ {slug}/{ten}: không thấy mốc <h3>II.")
    return text[:m.start()] + block + text[m.start():]


LINT = ROOT / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/lint_do_dai.py"
PHUT = re.compile(r"([Đđ]ọc khoảng (?:<strong>)?)(\d+)( phút)")


def cap_nhat_phut(th: pathlib.Path) -> str:
    """Số phút ở khung 🎯 Mục tiêu = số lint_do_dai đo, làm tròn LÊN (skill, Nhật ký 2026-10-06)."""
    import math, subprocess
    out = subprocess.run([sys.executable, str(LINT), str(th)], capture_output=True, text=True).stdout
    m = re.search(r"~([\d.]+) phút", out)
    if not m:
        return ""
    ph = math.ceil(float(m.group(1)))
    t = th.read_text(encoding="utf8")
    th.write_text(PHUT.sub(lambda x: f"{x.group(1)}{ph}{x.group(3)}", t, count=1), encoding="utf8")
    return f" · {ph} phút"


def ghi_json_giu_dinh_dang(p: pathlib.Path, obj: dict) -> None:
    raw = p.read_text(encoding="utf8")
    m = re.search(r"\n( +)\"", raw)
    s = json.dumps(obj, ensure_ascii=False, indent=len(m.group(1)) if m else 1)
    p.write_text(s + ("\n" if raw.endswith("\n") else ""), encoding="utf8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bai")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--nen", help="thư mục chứa <lesson_id>.html (body_html từ DB) làm nền cho theory.html")
    a = ap.parse_args()
    files = sorted(DATA.glob("*.json"))
    if a.bai:
        files = [f for f in files if f.stem == a.bai]
        if not files:
            sys.exit(f"✗ không có dữ liệu content/hanh-trang/{a.bai}.json")
    for f in files:
        slug, d = f.stem, json.loads(f.read_text(encoding="utf8"))
        block = render(slug, d)
        dir_ = LESSONS / slug
        src, th, bp = dir_ / "theory.src.html", dir_ / "theory.html", dir_ / "bundle.json"
        nen = th.read_text(encoding="utf8")
        if a.nen:
            pdb = pathlib.Path(a.nen) / f"{d['lesson_id']}.html"
            if pdb.exists():
                nen = pdb.read_text(encoding="utf8")
        new_th = chen(nen, block, slug, "theory.html")
        new_src = chen(src.read_text(encoding="utf8"), block, slug, "theory.src.html") if src.exists() else None
        print(f"{slug} (bài {d['lesson_id']}): {len(d['cau'])} câu, khối {len(block)} ký tự"
              f"{' — nền DB' if a.nen and (pathlib.Path(a.nen) / (str(d['lesson_id']) + '.html')).exists() else ''}")
        if not a.apply:
            continue
        th.write_text(new_th, encoding="utf8")
        print("   số phút" + (cap_nhat_phut(th) or ": không đo được"))
        new_th = th.read_text(encoding="utf8")
        if new_src is not None:
            ph = PHUT.search(new_th)
            if ph and "__PHUT__" not in new_src:
                new_src = PHUT.sub(lambda x: x.group(1) + ph.group(2) + x.group(3), new_src, count=1)
            src.write_text(new_src, encoding="utf8")
        if bp.exists():
            b = json.loads(bp.read_text(encoding="utf8"))
            b["theory_html"] = new_th
            ghi_json_giu_dinh_dang(bp, b)
    if not a.apply:
        print("(dry-run — thêm --apply để ghi)")


if __name__ == "__main__":
    main()
