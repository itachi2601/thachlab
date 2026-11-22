#!/usr/bin/env python3
"""Dựng 10 đề thi thử AVCN (khung đề cuối kỳ 5 Part) -> exams.json. Chạy: python3 build.py
Part 1: 10 câu định nghĩa, mỗi chương 1 từ ⭐ (mỗi từ ⭐ dùng đúng 1 lần qua 10 đề)
Part 2: Article chép nguyên văn giáo trình, 6 câu điền từ (3 phương án) + 1 nhóm Đúng/Sai 4 ý
Part 3: đoạn điền từ 8 chỗ có hộp từ · Part 4–5: chọn bản dịch Anh→Việt, Việt→Anh (thay cho viết tay)."""
import json, pathlib, random, re, sys, importlib.util
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
from data import EXAMS, DENY, P1_DEF, P1_SWAP
spec = importlib.util.spec_from_file_location("kt", ROOT / ".claude/skills/soan-bai-avcn/scripts/build_kiem_tra_tu_vung.py")
kt = importlib.util.module_from_spec(spec); spec.loader.exec_module(kt)

TOPIC = "AVCN: Đề thi thử cuối kỳ"
chap = {}
for c in range(1, 11):
    d = next(ROOT.glob(f"content/lesson-samples/avcn-chapter-{c}-*"))
    chap[c] = json.load(open(d / "data" / "bai.json"))

def plain(s): return re.sub(r"<[^>]+>", "", s)
def article(c, a, end):
    txt = " ".join(plain(x[0]) for x in chap[c]["bai_doc"][a - 1]["cau"])
    if end:
        i = txt.index(end); txt = txt[: i + len(end)]
    return txt
LAB = "abcd"
_pool = {}
def _pos(rng, m):
    if not _pool.get(m):
        p = list(range(m)) * 4; rng.shuffle(p); _pool[m] = p
    return _pool[m].pop()
def mk_mc(qs, q, right, wrong, why, rng):
    opts = list(wrong); k = _pos(rng, len(opts) + 1); opts.insert(k, right)
    qs.append({"type": "multiple_choice", "question": q, "options": opts, "answer": k, "explanation": why,
               "topic": TOPIC, "form": "ly_thuyet", "difficulty": "trung-binh"})

def build(n):
    _pool.clear(); E = EXAMS[n - 1]; rng = random.Random(900 + n); qs = []
    # ---- Part 1
    for c in range(1, 11):
        kt._cam.clear()
        kt._cam.update(frozenset((a.lower(), b.lower())) for a, b in kt.CAM_CAP.get(c, []))
        clusters = chap[c]["tu_vung"]
        words = [t for cl in clusters for t in cl["tu"]]
        idx = 2 * (n - 1) + ((n + c) % 2)
        t = words[idx]
        ci = next(i for i, cl in enumerate(clusters) if t in cl["tu"])
        d = re.sub(r"\s*Noun: [^.]*\.?$", "", kt.DEF_SUA.get(c, {}).get(t["def"], t["def"]))
        d = P1_DEF.get((n, c), d)
        wrong = kt.pick(rng, t, [clusters[ci]["tu"], words], key=lambda x: x["term"])
        wr_terms = [w["term"] for w in wrong]
        if (n, c) in P1_SWAP:
            a_, b_ = P1_SWAP[(n, c)]; wr_terms = [b_ if x == a_ else x for x in wr_terms]
        vi = kt.clean_vi(t["vi"])
        mk_mc(qs, f"<strong>Part 1 · Câu {c}.</strong> {d}", t["term"], wr_terms,
              f"<strong>{t['term']}</strong> = {vi}.", rng)
    # ---- Part 2
    ac, aa, end = E["art"]
    art = article(ac, aa, end)
    blk = f'<blockquote><strong>Part 2 · Article</strong><br>{art}</blockquote>'
    for i, (s, ans, wr) in enumerate(E["cloze"], 1):
        stem = f'{blk}<p><strong>Part 2.1 · Câu {i}.</strong> Điền từ vào chỗ trống: {s.replace("____", "<strong>______</strong>")}</p>'
        full = s.replace("____", ans)
        mk_mc(qs, stem, ans, wr, f"Trong Article: <em>{full}</em>", rng)
    stem = f'{blk}<p><strong>Part 2.2.</strong> Đúng hay Sai theo bài đọc?</p>'
    qs.append({"type": "true_false", "question": stem,
               "statements": [{"text": t, "answer": a} for t, a in E["tf"]],
               "explanation": "Đối chiếu từng ý với Article ở trên.", "topic": TOPIC, "form": "ly_thuyet", "difficulty": "trung-binh"})
    # ---- Part 3
    box, text, dap = E["p3"]
    boxh = " · ".join(f"<strong>{w}</strong>" for w in sorted(box, key=str.lower))
    for i in range(1, 9):
        body = re.sub(r"\{(\d)\}", lambda m: f"<strong>({m.group(1)}) ______</strong>" if int(m.group(1)) == i
                      else f"({m.group(1)}) ______", text)
        stem = (f'<strong>Part 3 · Chỗ trống ({i}).</strong> Chọn từ trong hộp để điền vào chỗ trống ({i}).'
                f'<blockquote>{boxh}</blockquote><p>{body}</p>')
        right = dap[i - 1]
        wrong = rng.sample([w for w in box if w != right and w not in DENY.get(n, {}).get(i, [])], 3)
        mk_mc(qs, stem, right, wrong, f"({i}) = <strong>{right}</strong>. " + re.sub(r"\{(\d)\}", lambda m: f"<u>{dap[int(m.group(1))-1]}</u>", text), rng)
    # ---- Part 4–5
    en, vi, wr = E["p4"]
    mk_mc(qs, f"<strong>Part 4 · Dịch sang tiếng Việt.</strong> Chọn bản dịch đúng nhất:<br><em>{en}</em>", vi, wr, f"Bản dịch đúng: {vi}", rng)
    vi, en, wr = E["p5"]
    mk_mc(qs, f"<strong>Part 5 · Dịch sang tiếng Anh.</strong> Chọn câu tiếng Anh đúng nhất:<br><em>{vi}</em>", en, wr, f"Câu đúng: {en}", rng)
    return qs

out = []
for n in range(1, 11):
    qs = build(n)
    out.append({"title": f"Đề thi thử cuối kỳ AVCN – Đề {n}", "topic": TOPIC, "difficulty": "trung-binh",
                "duration_minutes": 45, "subject_code": "avcn", "questions": qs})
    print(n, len(qs), "câu", [q["answer"] for q in qs if q["type"] == "multiple_choice"].count(0), "đáp án a")
json.dump(out, open(HERE / "exams.json", "w"), ensure_ascii=False, indent=1)
