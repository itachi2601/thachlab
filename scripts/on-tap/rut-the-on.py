#!/usr/bin/env python3
"""Rút bộ thẻ "Ôn 5 phút" của MỘT bài từ theory.html (đã nhúng hình SVG) (thử 25/11/2026, L11 bài 22–24).

Không soạn nội dung mới — chỉ lấy lại thứ bài đã có:
  - mỗi ô Chốt mục: câu 🎯 Cần nắm → thẻ lật (hỏi = <summary>, đáp = thân của nó);
  - hộp bẫy (mục có chữ "bẫy" trong <h3>): câu tự kiểm tra đầu tiên có .tl-quiz → thẻ chọn đáp án.
Mỗi thẻ mang `neo` = một đoạn chữ duy nhất của nó trong bài, để trang học sinh tìm đúng đoạn lý thuyết
cho nút "Ôn ngay" bằng chính splitTheorySections (không phụ thuộc trang đọc chia theo h3 hay h4).
Mỗi thẻ có `id` = 8 ký tự đầu sha1(neo) — khoá lịch ôn trong bảng on_tap_the; sửa chữ câu hỏi là thành thẻ mới.

Dùng:  python3 scripts/on-tap/rut-the-on.py <slug> [<slug> …] [--toi-da 8]   → content/on-tap/<slug>.json
       python3 scripts/on-tap/rut-the-on.py --tat-ca      (mọi bài có ô Chốt mục)
       python3 scripts/on-tap/rut-the-on.py --chi-index   (chỉ sinh lại content/on-tap/index.ts)
lesson_id lấy từ content/on-tap/_lesson-ids.json (sinh bằng `npx tsx scripts/on-tap/anh-xa-lesson-id.mts`).
Mỗi lần chạy đều SINH LẠI content/on-tap/index.ts từ các JSON trong thư mục (không sửa tay file đó).
File ra là bản nháp: người soạn đọc lại, bỏ thẻ trùng ý, giữ ≤ 8 thẻ (N5), rồi mới commit.
"""
import argparse, hashlib, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parents[2]


def text(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


def balanced_div(html: str, start: int) -> str:
    """Trả về khối <div …>…</div> bắt đầu tại `start` (đếm lồng nhau)."""
    depth = 0
    for m in re.finditer(r"<div\b|</div>", html[start:]):
        depth += 1 if m.group(0) == "<div" else -1
        if depth == 0:
            return html[start : start + m.end()]
    raise ValueError("div không đóng")

FIG_RE = re.compile(r'<figure class="fig[^"]*"[^>]*>.*?</figure>', re.S)


def usable(fig: str) -> bool:
    """Chỉ dùng hình SVG tự vẽ, ≤ 20 KB (ảnh chụp/ảnh sách thì không: bản quyền + nặng)."""
    return "<svg" in fig and "<img" not in fig and len(fig) <= 20_000


def no_caption(fig: str) -> str:
    return re.sub(r"<figcaption>.*?</figcaption>", "", fig, flags=re.S)


INLINE = ("strong", "em", "b", "i", "span", "u", "sub", "sup", "mark")


def can_the(parts: list) -> list:
    """Tách câu có thể cắt ngang <strong>…</strong>: mỗi gạch tự đóng thẻ còn mở và mở lại ở gạch sau."""
    out, mo = [], []  # mo: các thẻ mở (nguyên văn) mang sang gạch sau
    for p in parts:
        q = "".join(mo) + p
        mo = []
        for m in re.finditer(r"<(/?)(\w+)\b[^>]*>", q):
            ten = m.group(2).lower()
            if ten not in INLINE:
                continue
            if m.group(1):
                for k in range(len(mo) - 1, -1, -1):
                    if re.match(rf"<{ten}\b", mo[k], re.I):
                        del mo[k]
                        break
            else:
                mo.append(m.group(0))
        q += "".join(f"</{re.match(r'<(\w+)', t).group(1)}>" for t in reversed(mo))
        out.append(re.sub(r"<(\w+)\b[^>]*>\s*</\1>", "", q))
    return out


def bullets(html: str, sentences: bool = False) -> str:
    """Mỗi ý một dòng (thầy chốt 25/11): tách theo " · ", <br>, và câu (". " + chữ hoa) → <ul><li>…</li></ul>."""
    inner = html.strip()
    if inner.count("<p>") > 1:  # nhiều đoạn: tách từng đoạn
        return "".join(bullets(m.group(0)) for m in re.finditer(r"<p>.*?</p>", inner, re.S))
    inner = re.sub(r"^\s*<p>(.*)</p>\s*$", r"\1", inner, flags=re.S)
    parts = []
    for x in re.split(r"\s*(?:<br\s*/?>| · )\s*", inner):
        # Tách câu, nhưng không cắt trong công thức $…$ (đếm số dấu $ phía trước chẵn).
        start = 0
        for m in re.finditer(r"[.;]\s+(?=[A-ZĐÂĂÊÔƠƯÁÀẢÃẠÉÈẺẼẸÍÌỈĨỊÓÒỎÕỌÚÙỦŨỤÝ<$])", x):
            if x[: m.start()].count("$") % 2 == 0:
                parts.append(x[start : m.start()])
                start = m.end()
        parts.append(x[start:])
    parts = can_the(parts)
    parts = [p.strip().rstrip(".").strip() for p in parts]
    # Câu hướng dẫn thao tác trên hình động ("Bấm ▶ Chạy…") vô nghĩa trên thẻ; "(số liệu minh hoạ)" là ghi chú cho hình.
    parts = [re.sub(r"\s*\(số liệu minh hoạ\)", "", p) for p in parts if not text(p).startswith(("Bấm ", "Nhấn "))]
    # Gạch chỉ còn đơn vị (ví dụ "J" tách ra từ "… · J · …") → nói rõ là đơn vị.
    parts = [f"Đơn vị: {p}" if re.fullmatch(r"[A-Za-zΩ°/·]{1,3}", p.strip()) else p for p in parts if text(p)]
    parts = [p[0].upper() + p[1:] if p[:1].isalpha() else p for p in parts if p]
    if len(parts) < 2:
        return f"<p>{inner}</p>"
    return "<ul>" + "".join(f"<li>{x}</li>" for x in parts) + "</ul>"


def sinh_index() -> None:
    """content/on-tap/index.ts: import tường minh từng JSON (bundler tách đúng từng chunk), khoá theo slug và lesson_id."""
    d = ROOT / "content/on-tap"
    rows, ids = [], []
    for f in sorted(d.glob("*.json")):
        if f.name.startswith("_"):
            continue
        j = json.loads(f.read_text(encoding="utf8"))
        rows.append(f'  "{f.stem}": () => import("./{f.name}").then((m) => m.default as BoOnTap),')
        if j.get("lesson_id"):
            ids.append((int(j["lesson_id"]), f.stem, len(j.get("the", []))))
    ids.sort()
    out = [
        "// FILE SINH TỰ ĐỘNG bởi scripts/on-tap/rut-the-on.py — KHÔNG SỬA TAY (chạy lại script với --chi-index).",
        'import type { BoOnTap } from "@/components/lessons/OnNamPhut";',
        "",
        "/** Bộ thẻ \"Ôn 5 phút\" theo slug bài; mỗi bộ một chunk riêng, chỉ nạp khi mở. */",
        "export const BO_ON_TAP: Record<string, () => Promise<BoOnTap>> = {",
        *rows,
        "};",
        "",
        "/** lesson_id → slug + số thẻ (để trang bài biết có bộ thẻ và hiện \"N thẻ\" mà chưa phải nạp JSON). */",
        "export const ON_TAP_THEO_BAI: Record<number, { slug: string; so_the: number }> = {",
        *[f'  {i}: {{ slug: "{s}", so_the: {n} }},' for i, s, n in ids],
        "};",
        "",
    ]
    (d / "index.ts").write_text("\n".join(out), encoding="utf8")
    print(f"index.ts: {len(rows)} bộ, {len(ids)} có lesson_id")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("slugs", nargs="*")
    ap.add_argument("--toi-da", type=int, default=8)
    ap.add_argument("--tat-ca", action="store_true")
    ap.add_argument("--chi-index", action="store_true")
    a = ap.parse_args()
    if not a.chi_index:
        slugs = a.slugs
        if a.tat_ca:
            slugs = sorted(p.parent.name for p in (ROOT / "content/lesson-samples").glob("*/theory.html")
                           if "tl-chot" in p.read_text(encoding="utf8"))
        ids_f = ROOT / "content/on-tap/_lesson-ids.json"
        ids = json.loads(ids_f.read_text(encoding="utf8")) if ids_f.exists() else {}
        for slug in slugs:
            rut(slug, a.toi_da, ids.get(slug))
    sinh_index()


def rut(slug: str, toi_da: int, lesson_id) -> None:
    class A: pass
    a = A(); a.slug = slug; a.toi_da = toi_da
    src = ROOT / "content/lesson-samples" / a.slug / "theory.html"
    html = src.read_text(encoding="utf8")
    lesson_title = ""
    bundle = src.with_name("bundle.json")
    if bundle.exists():
        lesson_title = json.loads(bundle.read_text(encoding="utf8"))["target"].get("lesson_title", "")

    heads = list(re.finditer(r"<h3\b[^>]*>(.*?)</h3>", html, re.S))
    cards = []  # (vị trí trong bài, thẻ) — sắp theo thứ tự bài
    used_figs = set()
    for i, h in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(html)
        sec = html[h.start() : end]
        muc = text(h.group(1))
        h4_at = [m.start() for m in re.finditer(r"<h4\b", sec)]

        for m in re.finditer(r'<div class="tl-box tl-keep tl-chot">', sec):
            box = balanced_div(sec, m.start())
            q = re.search(r'tl-chot-h">.*?</p>\s*<details[^>]*>\s*<summary>(.*?)</summary>(.*?)</details>', box, re.S)
            if not q:
                continue
            # Chỉ lấy đáp 🎯 (đã gọn một dòng); dòng ✍️ Tập lặp lại ý đó nên bỏ (N4). Ý nối bằng "·" → gạch đầu dòng.
            card = {"kieu": "lat", "muc": muc, "neo": text(q.group(1))[:60], "hoi": q.group(1).strip(),
                    "dap": bullets(q.group(2))}
            # Tiểu mục <h4> đứng trước ô Chốt mục — "Ôn ngay" cuộn tới đúng ý đó, không chỉ đầu mục lớn.
            h4s = re.findall(r"<h4\b[^>]*>(.*?)</h4>", sec[: m.start()], re.S)
            if h4s:
                card["tieu_muc"] = text(h4s[-1]).split("$")[0].strip()
            # Hình trong cùng tiểu mục → mặt trước làm gợi ý nhớ (bỏ chú thích), chú thích sang mặt sau.
            lo = max([x for x in h4_at if x < m.start()], default=0)
            for f in FIG_RE.finditer(sec[lo : m.start()]):
                if usable(f.group(0)):
                    card["hinh"] = no_caption(f.group(0))
                    used_figs.add(h.start() + lo + f.start())
                    break
            cards.append((h.start() + m.start(), card))

        if "bẫy" in muc.lower():
            for m in re.finditer(r'<div class="tl-box tl-box--think tl-check">', sec):
                box = balanced_div(sec, m.start())
                if "tl-quiz" not in box:
                    continue
                stem = re.search(r"<p>(.*?)</p>", box, re.S)
                # Bỏ dòng gợi ý ⚠ đặt trước phương án: trong bài nó dẫn dắt, khi ôn nó làm lộ đáp án.
                box = re.sub(r"<p>\s*⚠.*?</p>\s*", "", box, flags=re.S)
                # Đổi id/name để không đụng câu gốc khi cùng trang với bài lý thuyết.
                box = re.sub(r'\b(id|for|name)="(tl[\w-]+)"', r'\1="on-\2"', box)
                cards.append((h.start() + m.start(), {"kieu": "chon", "muc": muc,
                              "neo": text(stem.group(1))[:60] if stem else "",
                              "hoi": stem.group(1).strip() if stem else "", "html": box}))
                break

    # Hình chưa gắn thẻ nào mà có chú thích đủ ý → thẻ "nhìn hình, nói lại" (tối đa 2, ưu tiên mục II).
    hinh = []
    for i, h in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(html)
        muc = text(h.group(1))
        if not muc.startswith("II."):
            continue
        sec = html[h.start() : end]
        h4s = [(m.start(), text(m.group(1))) for m in re.finditer(r"<h4\b[^>]*>(.*?)</h4>", sec, re.S)]
        for f in FIG_RE.finditer(sec):
            at = h.start() + f.start()
            cap = re.search(r"<figcaption>(.*?)</figcaption>", f.group(0), re.S)
            cap_t = re.sub(r"^Hình\s*\d+\.\s*", "", text(cap.group(1))) if cap else ""
            if at in used_figs or not usable(f.group(0)) or len(cap_t) < 40:
                continue
            tm = [t for x, t in h4s if x < f.start()]
            card = {"kieu": "lat", "muc": muc, "neo": cap_t[:40], "hoi": "Nhìn hình: hình này cho thấy điều gì?",
                    "hinh": no_caption(f.group(0)), "dap": bullets(cap_t)}
            if tm:
                card["tieu_muc"] = tm[-1].split("$")[0].strip()
            hinh.append((at, card))
    cards += hinh[:2]
    cards = [{"id": hashlib.sha1(c["neo"].encode()).hexdigest()[:8], **c} for _, c in sorted(cards, key=lambda x: x[0])]

    out = ROOT / "content/on-tap" / f"{a.slug}.json"
    out.parent.mkdir(exist_ok=True)
    data = {
        "schema": "thachlab.on-tap/v1",
        "slug": a.slug,
        "lesson_id": lesson_id,
        "lesson_title": lesson_title,
        "the": cards[: a.toi_da],
    }
    out.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
    print(f"{out.relative_to(ROOT)}: {len(cards)} thẻ rút được, giữ {len(data['the'])}, lesson_id={lesson_id}")


if __name__ == "__main__":
    main()
