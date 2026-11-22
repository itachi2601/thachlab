#!/usr/bin/env python3
"""Dựng đề KIỂM TRA TỪ VỰNG (25 câu, 15 phút) cho một chương AVCN từ data/bai.json.

Mục đích: thầy xem em nào đã thật sự học 20 từ ⭐ của chương (đề nằm ở mục Kiểm tra, có điểm, có bảng điểm).
  - 10 câu: định nghĩa tiếng Anh (kiểu Part 1) → chọn từ
  - 10 câu: nghĩa tiếng Việt → chọn từ tiếng Anh
  - 5 câu : từ ⭐⭐ → chọn nghĩa tiếng Việt
Mỗi từ ⭐ xuất hiện đúng một lần; trong mỗi cụm từ xen kẽ hai chiều hỏi. Phương án nhiễu lấy trong cùng cụm trước
(dễ nhầm thật), loại từ chứa nhau (screwdriver / phillips screwdriver) để không có hai đáp án đúng.

Chạy: python3 .claude/skills/soan-bai-avcn/scripts/build_kiem_tra_tu_vung.py <thư mục bài>  [--all]
Ghi:  <thư mục bài>/kiem-tra-tu-vung/bundle.json
"""
import json, pathlib, random, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[4]

# Sửa sau khi soát (kiem-code): cặp từ KHÔNG được làm phương án nhiễu cho nhau (gần nghĩa → hai đáp án đúng),
# và từ ⭐⭐ không đưa vào đề (nghĩa mơ hồ). Khoá = số chương.
_F5 = ["nail", "screw", "bolt", "pin", "nut", "washer", "anchor", "clamp", "rivet", "blind rivet"]
CAM_CAP: dict[int, list[tuple[str, str]]] = {
    2: [("general safety sign", "fire safety sign")],
    3: [("pliers", "diagonal cutters"), ("hand tool", "hardware")],
    4: [("micrometer", "vernier caliper"), ("outside micrometer", "vernier caliper"), ("inside micrometer", "vernier caliper"),
        ("depth micrometer", "vernier caliper"), ("variation", "deviation"), ("deviation", "tolerance"), ("tolerance", "variation"), ("tolerance", "permissible"), ("variation", "permissible")],
    5: [("fastener", x) for x in _F5] + [("spanner", "hex key / Allen key"), ("pin", "nail"),
                                          ("wood screw", "sheet metal screw"), ("screw", "bolt")],
    6: [("weld pool", "molten"), ("heat-affected zone", "weld zone")],
    7: [("forging", "rolling"), ("metal-forming", "cold-working"), ("metal-forming", "hot-working"),
        ("metal-forming", "forging"), ("metal-forming", "rolling"), ("forging", "cold-working"), ("forging", "hot-working"), ("cold-working", "rolling")],
    8: [("cutting fluid", "coolant"), ("turn", "bore"), ("swarf / chips", "workpiece")],
    9: [("manufacturing", "mass production"), ("CNC", "CAM"), ("software", "CAM"), ("software", "CAD"), ("software", "CNC"), ("CNC", "automation")],
    10: [("spare part", "replacement"), ("mechanical maintenance", "preventive maintenance"), ("mechanical maintenance", "corrective maintenance"), ("failure", "downtime")],
}
BO_THEM: dict[int, list[str]] = {}
# Sửa chữ câu hỏi để không lộ đáp án (khoá = định nghĩa / nghĩa gốc trong bai.json)
DEF_SUA: dict[int, dict[str, str]] = {
    6: {"An electrode which does not melt and is not consumed during welding.":
        "A rod which does not melt and is not consumed during welding."},
    8: {"A machine fitted with a drill bit to cut circular holes.":
        "A machine fitted with a rotating cutting tool to cut circular holes.",
        "A liquid that keeps the workpiece cool. Cutting fluid acts as a coolant.":
        "A liquid that keeps the workpiece cool."},
}
VI_SUA: dict[int, dict[str, str]] = {
    4: {"pound": "cân Anh (khoảng 0,45 kg)", "imperial": "hệ đo lường Anh–Mỹ",
        "cubic inch": "đơn vị thể tích nhỏ của hệ Anh"},
    8: {"swarf / chips": "phoi (mảnh kim loại bị cắt bỏ)", "workpiece": "phôi (vật đang gia công)"},
}
_cam: set = set()


def clean_vi(s: str) -> str:
    """Bỏ ngoặc gợi ý (đời thường…, tiếng Anh) để nghĩa tiếng Việt không lộ/không lan man."""
    def keep(m):
        inner = m.group(1)
        if re.search(r"đời thường|cùng nghĩa|còn gọi|tiếng Mỹ|[=:]|\bis\b|\blà\b", inner):
            return ""
        if not re.search(r"[à-ỹđ]", inner, re.I):  # toàn chữ không dấu → tiếng Anh
            return ""
        return m.group(0)
    s = re.sub(r"\s*\(([^()]*)\)", keep, s)
    return re.sub(r"\s+", " ", s).strip(" ,;")


def overlap(a: str, b: str) -> bool:
    a, b = a.lower(), b.lower()
    return a in b or b in a or frozenset((a, b)) in _cam


def pick(rng, answer, pools, key=lambda x: x, n=3):
    """Lấy n phương án nhiễu: ưu tiên pool đầu (cùng cụm), không chứa nhau với đáp án, không trùng."""
    out = []
    for pool in pools:
        cand = [x for x in pool if key(x) != key(answer) and not overlap(key(x), key(answer))
                and all(key(x) != key(y) for y in out)]
        rng.shuffle(cand)
        out += cand[: n - len(out)]
        if len(out) == n:
            break
    if len(out) < n:
        raise SystemExit(f"không đủ phương án nhiễu cho {key(answer)!r}")
    return out


def build(d: pathlib.Path) -> dict:
    bai = json.load(open(d / "data" / "bai.json"))
    base = json.load(open(d / "bundle.json"))
    ch = bai["meta"]["chapter"]
    title_en = bai["meta"]["title_en"]
    topic = base["exam"].get("topic") or f"AVCN C{ch}: {title_en}"
    rng = random.Random(1000 + ch)
    _cam.clear()
    _cam.update(frozenset((a.lower(), b.lower())) for a, b in CAM_CAP.get(ch, []))

    clusters = bai["tu_vung"]
    for c in clusters:
        for t in c["tu"]:
            t["def"] = re.sub(r"\s*Noun: [^.]*\.?$", "", DEF_SUA.get(ch, {}).get(t["def"], t["def"]))
            if t["term"] in VI_SUA.get(ch, {}):
                t["vi"] = VI_SUA[ch][t["term"]]
    all_words = [t for c in clusters for t in c["tu"]]
    defs, vis = [], []
    for ci, c in enumerate(clusters):
        for wi, t in enumerate(c["tu"]):
            # xen kẽ chiều hỏi; cụm lẻ đảo pha để mỗi chiều đủ 10 câu
            (defs if (wi + ci) % 2 == 0 else vis).append((ci, t))
    # cân bằng 10/10 nếu cụm không đủ 5 từ
    while len(defs) > len(vis) + 1:
        vis.append(defs.pop())
    while len(vis) > len(defs) + 1:
        defs.append(vis.pop())

    qs = []
    vi_tri = [i % 4 for i in range(28)]  # đáp án rải đều a–d (không để một chữ cái chiếm nửa đề)
    random.Random(2000 + ch).shuffle(vi_tri)

    def mc(q, right, wrong, why):
        k = vi_tri[len(qs)]
        opts = list(wrong)
        opts.insert(k, right)
        qs.append({"type": "multiple_choice", "question": q, "options": opts, "answer": k, "explanation": why,
                   "topic": topic, "form": "ly_thuyet", "difficulty": "de"})

    term = lambda t: t["term"]
    for ci, t in defs:
        same = [x for x in clusters[ci]["tu"]]
        wrong = pick(rng, t, [same, all_words], key=term)
        mc(f"Which word matches this definition?<br><em>{t['def']}</em>", t["term"], [w["term"] for w in wrong],
           f"<strong>{t['term']}</strong> = {clean_vi(t['vi'])}.")
    for ci, t in vis:
        same = [x for x in clusters[ci]["tu"]]
        wrong = pick(rng, t, [same, all_words], key=term)
        mc(f"Which English word means <strong>“{clean_vi(t['vi'])}”</strong>?", t["term"], [w["term"] for w in wrong],
           f"{t['term']}: {t['def']}")

    bo = {t.lower() for t in BO_THEM.get(ch, [])} | {w["term"].lower() for w in all_words}
    them = [x for x in bai["tu_vung_them"] if x["term"].lower() not in bo]
    rng.shuffle(them)
    vkey = lambda x: clean_vi(x["vi"])
    for t in them[:5]:
        _cam.update(frozenset((vkey(x).lower(), vkey(y).lower())) for a, b in CAM_CAP.get(ch, [])
                    for x in bai["tu_vung_them"] if x["term"].lower() == a.lower()
                    for y in bai["tu_vung_them"] if y["term"].lower() == b.lower())
        wrong = pick(rng, t, [bai["tu_vung_them"]], key=vkey)
        mc(f"What does <strong>{t['term']}</strong> mean?", clean_vi(t["vi"]), [vkey(w) for w in wrong],
           f"<strong>{t['term']}</strong> = {t['vi']}.")

    # trộn thứ tự câu (giữ cố định theo chương) để hai chiều hỏi không dồn khối
    rng.shuffle(qs)
    short = re.sub(r"\s*[—-]\s.*$", "", title_en)
    base.update({"theory_html": "", "theory_title": "", "theory_subtitle": "", "worked_examples": [],
                 "raster_images": []})
    base["exam"] = {"title": f"Kiểm tra từ vựng Chapter {ch}: {short}", "topic": topic, "difficulty": "de",
                    "duration_minutes": 15, "subject_code": "avcn", "questions": qs}
    out = d / "kiem-tra-tu-vung"
    out.mkdir(exist_ok=True)
    json.dump(base, open(out / "bundle.json", "w"), ensure_ascii=False, indent=1)
    return base


if __name__ == "__main__":
    dirs = (sorted(ROOT.glob("content/lesson-samples/avcn-chapter-*")) if "--all" in sys.argv
            else [pathlib.Path(a).resolve() for a in sys.argv[1:] if not a.startswith("--")])
    for d in dirs:
        b = build(d)
        print(f"{d.name}: {len(b['exam']['questions'])} câu · {b['exam']['title']}")
