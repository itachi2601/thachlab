#!/usr/bin/env python3
"""Dựng trang Flashcard tĩnh cho một chương AVCN từ data/bai.json.

    python3 .claude/skills/soan-bai-avcn/scripts/build_flashcard.py content/lesson-samples/avcn-chapter-8-chipping-machining

Ghi public/flashcard/avcn-chapter-<N>.html (đường dẫn = meta.flashcard trong bai.json, link trong bài trỏ tới đây).
Hai chế độ: Thẻ Leitner 3 hộp (lật thẻ, tự đánh giá) và Nhìn ảnh/định nghĩa đoán từ (4 phương án).
Không thư viện ngoài; tiến độ hộp lưu localStorage của trình duyệt (mất cũng không sao).
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]


def main() -> None:
    lesson_dir = Path(sys.argv[1]).resolve()
    data = json.loads((lesson_dir / "data" / "bai.json").read_text(encoding="utf-8"))
    meta = data["meta"]
    ch = meta.get("chapter") or meta.get("so") or int(lesson_dir.name.split("-")[2])
    href = meta.get("flashcard") or f"/flashcard/avcn-chapter-{ch}.html"
    terms = []
    for g in data["tu_vung"]:
        for t in g["tu"]:
            img = t.get("img")
            terms.append({
                "term": t["term"], "ipa": t.get("ipa", ""), "vi": t["vi"], "def": t.get("def", ""),
                "img": f"/assets/avcn/chapter-{ch}/{img}.webp" if img else "", "group": g["ten"],
            })
    for t in terms:
        if t["img"]:
            assert (ROOT / "public" / t["img"].lstrip("/")).exists(), f"thiếu ảnh {t['img']}"
    title = meta.get("title_en") or meta.get("title") or f"Chapter {ch}"
    html = TEMPLATE.replace("__CH__", str(ch)).replace("__TITLE__", title).replace(
        "__DATA__", json.dumps(terms, ensure_ascii=False).replace("</", "<\\/"))
    out = ROOT / "public" / href.lstrip("/")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"✓ {out.relative_to(ROOT)} — {len(terms)} thẻ")


TEMPLATE = r"""<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Flashcard Chapter __CH__ — Anh văn chuyên ngành Cơ khí | ThachLab</title>
<meta name="robots" content="noindex">
<style>
:root { --bg:#f7f8fb; --card:#fff; --ink:#0f172a; --muted:#475569; --line:#d6dbe4; --accent:#c2410c; --accent-soft:#fff1e6; --ok:#047857; --ok-soft:#e7f7ef; --bad:#b91c1c; --bad-soft:#fdecec; }
@media (prefers-color-scheme: dark) { :root { --bg:#0f172a; --card:#1e293b; --ink:#f1f5f9; --muted:#cbd5e1; --line:#334155; --accent:#fb923c; --accent-soft:#2a1d14; --ok:#34d399; --ok-soft:#10291f; --bad:#f87171; --bad-soft:#2d1515; } }
* { box-sizing:border-box; }
body { margin:0; background:var(--bg); color:var(--ink); font:17px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif; }
main { max-width:560px; margin:0 auto; padding:16px 16px 40px; }
a { color:var(--accent); }
.top { display:flex; align-items:center; justify-content:space-between; gap:8px; min-height:44px; }
.top a { display:inline-flex; align-items:center; min-height:44px; font-weight:600; text-decoration:none; }
h1 { font-size:1.35rem; line-height:1.3; margin:4px 0 2px; }
.sub { color:var(--muted); margin:0 0 14px; font-size:.95rem; }
.tabs { display:grid; grid-template-columns:1fr 1fr; gap:6px; background:var(--card); border:1px solid var(--line); border-radius:14px; padding:4px; margin-bottom:14px; }
.tabs button { min-height:44px; border:0; border-radius:10px; background:transparent; color:var(--ink); font:inherit; font-weight:600; cursor:pointer; }
.tabs button[aria-selected=true] { background:var(--accent); color:#fff; }
.boxes { display:grid; grid-template-columns:repeat(3,1fr); gap:6px; margin-bottom:12px; }
.boxes div { background:var(--card); border:1px solid var(--line); border-radius:12px; padding:6px; text-align:center; font-size:.85rem; color:var(--muted); }
.boxes b { display:block; font-size:1.3rem; color:var(--ink); }
.card { background:var(--card); border:1px solid var(--line); border-radius:18px; padding:16px; box-shadow:0 2px 10px rgba(15,23,42,.06); }
.pic { width:100%; aspect-ratio:4/3; object-fit:contain; background:#fff; border-radius:12px; display:block; }
.def { font-size:1.1rem; font-weight:600; margin:12px 0 0; }
.hint { color:var(--muted); font-size:.9rem; margin:8px 0 0; }
.back { border-top:1px dashed var(--line); margin-top:14px; padding-top:12px; }
.term { font-size:1.6rem; font-weight:800; margin:0; display:flex; align-items:center; gap:8px; flex-wrap:wrap; }
.ipa { color:var(--muted); font-size:1rem; font-weight:400; }
.vi { font-size:1.15rem; margin:4px 0 0; }
.btn { min-height:48px; padding:0 16px; border-radius:12px; border:1px solid var(--line); background:var(--card); color:var(--ink); font:inherit; font-weight:700; cursor:pointer; }
.btn-main { width:100%; margin-top:14px; background:var(--accent); border-color:var(--accent); color:#fff; }
.row { display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-top:14px; }
.btn-bad { background:var(--bad-soft); border-color:var(--bad); color:var(--bad); }
.btn-ok { background:var(--ok-soft); border-color:var(--ok); color:var(--ok); }
.speak { min-width:44px; min-height:44px; border-radius:50%; border:1px solid var(--line); background:var(--accent-soft); font-size:1.1rem; cursor:pointer; }
.opts { display:grid; gap:8px; margin-top:14px; }
.opts button { min-height:48px; text-align:left; padding:8px 14px; border-radius:12px; border:1px solid var(--line); background:var(--card); color:var(--ink); font:inherit; font-weight:600; cursor:pointer; }
.opts button.ok { background:var(--ok-soft); border-color:var(--ok); color:var(--ok); }
.opts button.bad { background:var(--bad-soft); border-color:var(--bad); color:var(--bad); }
.score { color:var(--muted); font-size:.95rem; margin:0 0 10px; }
.done { text-align:center; }
.credit { color:var(--muted); font-size:.8rem; margin-top:20px; }
</style>
</head>
<body>
<main>
  <div class="top"><a href="/lop-hoc/avcn/">← Về bài học</a><span class="sub" style="margin:0">Chapter __CH__</span></div>
  <h1>Flashcard: __TITLE__</h1>
  <p class="sub">20 từ ⭐ của chương. Chạm 🔊 để nghe phát âm.</p>
  <div class="tabs" role="tablist">
    <button role="tab" id="t-leitner" aria-selected="true">Thẻ 3 hộp</button>
    <button role="tab" id="t-quiz" aria-selected="false">Nhìn ảnh đoán từ</button>
  </div>
  <section id="view"></section>
  <p class="credit">Ảnh: Wikimedia Commons, giấy phép mở. Nguồn từng ảnh ghi trong bài học.</p>
</main>
<script>
const TERMS = __DATA__;
const KEY = "avcn-flashcard-ch__CH__";
TERMS.forEach((t, i) => { t.id = i; });
// Cặp từ đồng nghĩa trong chương: không cho làm phương án nhiễu của nhau (hai đáp án cùng đúng).
const SAME = [["coolant", "cutting fluid"]];
const clash = (a, b) => a.term === b.term || SAME.some((p) => p.includes(a.term) && p.includes(b.term));
const view = document.getElementById("view");
let box = {};
try { box = JSON.parse(localStorage.getItem(KEY) || "{}"); } catch (e) { box = {}; }
const boxOf = (t) => box[t.id] || 1;
function save() { try { localStorage.setItem(KEY, JSON.stringify(box)); } catch (e) {} }
function esc(s) { return String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]); }
function speak(text) {
  if (!("speechSynthesis" in window)) return;
  speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(text);
  u.lang = "en-US"; u.rate = 0.9;
  const score = (x) => {
    const l = x.lang.replace("_", "-").toLowerCase();
    if (!l.startsWith("en")) return -1;
    let s = l === "en-us" ? 10 : 5;
    if (/premium|enhanced|neural|natural|online/i.test(x.name)) s += 30;
    if (/\b(samantha|ava|allison|evan|nicky|zoe|aria|jenny|guy|google us english)\b/i.test(x.name)) s += 20;
    if (/\b(fred|albert|zarvox|bad news|bahh|bells|boing|bubbles|cellos|deranged|good news|hysterical|junior|kathy|organ|princess|ralph|trinoids|whisper|superstar)\b/i.test(x.name)) s -= 40;
    if (x.localService === false) s += 5;
    return s;
  };
  const v = speechSynthesis.getVoices().filter((x) => score(x) >= 0).sort((a, b) => score(b) - score(a))[0];
  if (v) u.voice = v;
  speechSynthesis.speak(u);
}
if ("speechSynthesis" in window) speechSynthesis.getVoices();
view.addEventListener("click", (e) => { const b = e.target.closest("[data-speak]"); if (b) speak(b.dataset.speak); });
function front(t) {
  return (t.img ? `<img class="pic" src="${t.img}" alt="">` : "") + `<p class="def">${esc(t.def)}</p>`;
}
function shuffle(a) { for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; }

// Thẻ Leitner 3 hộp: hộp 1 hiện nhiều nhất; "Nhớ rồi" đẩy lên một hộp, "Chưa nhớ" về hộp 1.
let current = null;
function pickCard() {
  const weights = { 1: 6, 2: 3, 3: 1 };
  const pool = TERMS.filter((t) => t !== current);
  const total = pool.reduce((s, t) => s + weights[boxOf(t)], 0);
  let r = Math.random() * total;
  for (const t of pool) { r -= weights[boxOf(t)]; if (r <= 0) return t; }
  return pool[0];
}
function boxesHtml() {
  const c = { 1: 0, 2: 0, 3: 0 };
  TERMS.forEach((t) => c[boxOf(t)]++);
  return `<div class="boxes"><div><b>${c[1]}</b>Hộp 1 · chưa nhớ</div><div><b>${c[2]}</b>Hộp 2 · đang nhớ</div><div><b>${c[3]}</b>Hộp 3 · đã thuộc</div></div>`;
}
function renderLeitner() {
  current = pickCard();
  const t = current;
  view.innerHTML = boxesHtml() + `<div class="card">${front(t)}<p class="hint">Nghĩ ra từ tiếng Anh trước, rồi mới lật thẻ.</p>
    <div id="back" class="back" hidden>
      <p class="term">${esc(t.term)} <span class="ipa">${esc(t.ipa)}</span> <button class="speak" data-speak="${esc(t.term)}" aria-label="Nghe">🔊</button></p>
      <p class="vi">${esc(t.vi)}</p>
      <div class="row"><button class="btn btn-bad" id="no">Chưa nhớ</button><button class="btn btn-ok" id="yes">Nhớ rồi</button></div>
    </div>
    <button class="btn btn-main" id="flip">Lật thẻ</button></div>`;
  document.getElementById("flip").onclick = (e) => { e.target.remove(); document.getElementById("back").hidden = false; speak(t.term); };
  view.querySelector("#no").onclick = () => { box[t.id] = 1; save(); renderLeitner(); };
  view.querySelector("#yes").onclick = () => { box[t.id] = Math.min(3, boxOf(t) + 1); save(); renderLeitner(); };
}

// Nhìn ảnh (hoặc đọc định nghĩa nếu từ không có ảnh) chọn 1 trong 4 từ — đúng dạng Part 1 của đề cuối kỳ.
let quiz = null;
function startQuiz() { quiz = { order: shuffle(TERMS.slice()), i: 0, right: 0 }; renderQuiz(); }
function renderQuiz() {
  if (quiz.i >= quiz.order.length) {
    view.innerHTML = `<div class="card done"><p class="term" style="justify-content:center">${quiz.right}/${quiz.order.length}</p><p class="vi">${quiz.right >= 16 ? "Rất tốt! Em đã sẵn sàng cho Part 1." : "Ôn lại các từ sai ở chế độ Thẻ 3 hộp rồi làm lại nhé."}</p><button class="btn btn-main" id="again">Làm lại</button></div>`;
    document.getElementById("again").onclick = startQuiz;
    return;
  }
  const t = quiz.order[quiz.i];
  const opts = shuffle([t, ...shuffle(TERMS.filter((x) => !clash(x, t)).filter((x, k, a) => a.findIndex((y) => y.term === x.term) === k)).slice(0, 3)]);
  view.innerHTML = `<p class="score">Câu ${quiz.i + 1}/${quiz.order.length} · đúng ${quiz.right}</p><div class="card">${front(t)}
    <div class="opts">${opts.map((o, k) => `<button data-k="${k}">${"abcd"[k]}. ${esc(o.term)}</button>`).join("")}</div><div id="after"></div></div>`;
  view.querySelectorAll(".opts button").forEach((b) => b.onclick = () => {
    const pick = opts[+b.dataset.k];
    const ok = pick === t;
    if (ok) quiz.right++; else box[t.id] = 1;
    save();
    view.querySelectorAll(".opts button").forEach((x) => { x.disabled = true; if (opts[+x.dataset.k] === t) x.classList.add("ok"); });
    if (!ok) b.classList.add("bad");
    document.getElementById("after").innerHTML = `<div class="back"><p class="term">${esc(t.term)} <span class="ipa">${esc(t.ipa)}</span> <button class="speak" data-speak="${esc(t.term)}" aria-label="Nghe">🔊</button></p><p class="vi">${esc(t.vi)}</p></div><button class="btn btn-main" id="next">Câu tiếp</button>`;
    document.getElementById("next").onclick = () => { quiz.i++; renderQuiz(); };
    speak(t.term);
  });
}

const tabs = { leitner: document.getElementById("t-leitner"), quiz: document.getElementById("t-quiz") };
function setMode(m) {
  tabs.leitner.setAttribute("aria-selected", m === "leitner");
  tabs.quiz.setAttribute("aria-selected", m === "quiz");
  m === "leitner" ? renderLeitner() : startQuiz();
}
tabs.leitner.onclick = () => setMode("leitner");
tabs.quiz.onclick = () => setMode("quiz");
setMode("leitner");
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
