#!/usr/bin/env python3
"""Rút bộ thẻ "Ôn 5 phút" của MỘT bài từ theory.src.html (thử 25/11/2026, L11 bài 22–24).

Không soạn nội dung mới — chỉ lấy lại thứ bài đã có:
  - mỗi ô Chốt mục: câu 🎯 Cần nắm → thẻ lật (hỏi = <summary>, đáp = thân của nó);
  - hộp bẫy (mục có chữ "bẫy" trong <h3>): câu tự kiểm tra đầu tiên có .tl-quiz → thẻ chọn đáp án.
Mỗi thẻ mang `neo` = một đoạn chữ duy nhất của nó trong bài, để trang học sinh tìm đúng đoạn lý thuyết
cho nút "Ôn ngay" bằng chính splitTheorySections (không phụ thuộc trang đọc chia theo h3 hay h4).

Dùng:  python3 scripts/on-tap/rut-the-on.py <slug> [--toi-da 8]   → content/on-tap/<slug>.json
File ra là bản nháp: người soạn đọc lại, bỏ thẻ trùng ý, giữ ≤ 8 thẻ (N5), rồi mới commit.
"""
import argparse, json, pathlib, re

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


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--toi-da", type=int, default=8)
    a = ap.parse_args()

    src = ROOT / "content/lesson-samples" / a.slug / "theory.src.html"
    html = src.read_text(encoding="utf8")
    lesson_title = ""
    bundle = src.with_name("bundle.json")
    if bundle.exists():
        lesson_title = json.loads(bundle.read_text(encoding="utf8"))["target"].get("lesson_title", "")

    heads = list(re.finditer(r"<h3\b[^>]*>(.*?)</h3>", html, re.S))
    cards = []
    for i, h in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(html)
        sec = html[h.start() : end]
        muc = text(h.group(1))

        for m in re.finditer(r'<div class="tl-box tl-keep tl-chot">', sec):
            box = balanced_div(sec, m.start())
            q = re.search(r'tl-chot-h">.*?</p>\s*<details[^>]*>\s*<summary>(.*?)</summary>(.*?)</details>', box, re.S)
            if not q:
                continue
            # Chỉ lấy đáp 🎯 (đã gọn một dòng); dòng ✍️ Tập lặp lại ý đó nên bỏ (N4).
            dap = q.group(2).strip()
            # Tiểu mục <h4> đứng trước ô Chốt mục — "Ôn ngay" cuộn tới đúng ý đó, không chỉ đầu mục lớn.
            h4s = re.findall(r"<h4\b[^>]*>(.*?)</h4>", sec[: m.start()], re.S)
            card = {"kieu": "lat", "muc": muc, "neo": text(q.group(1))[:60], "hoi": q.group(1).strip(), "dap": dap}
            if h4s:
                card["tieu_muc"] = text(h4s[-1]).split("$")[0].strip()
            cards.append(card)

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
                cards.append({"kieu": "chon", "muc": muc, "neo": text(stem.group(1))[:60] if stem else "",
                              "hoi": stem.group(1).strip() if stem else "", "html": box})
                break

    out = ROOT / "content/on-tap" / f"{a.slug}.json"
    out.parent.mkdir(exist_ok=True)
    data = {
        "schema": "thachlab.on-tap/v1",
        "slug": a.slug,
        "lesson_title": lesson_title,
        "the": cards[: a.toi_da],
    }
    out.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
    print(f"{out.relative_to(ROOT)}: {len(cards)} thẻ rút được, giữ {len(data['the'])}")
    for c in data["the"]:
        print(f"  [{c['kieu']}] {c['muc'][:28]:28} | {c['neo']}")


if __name__ == "__main__":
    main()
