// Xáo thứ tự bốn ý a)–d) của câu Đúng–sai trong scripts/data/theory-quiz/*.json để học sinh không đoán được
// theo vị trí (đợt 27/10/2026: ý a Đúng 83%, ý d Đúng 23%). Đi kèm: đánh lại nhãn trong lời giải, hoán vị distractorNotes.
// Ổn định (hạt giống theo bài + số thứ tự câu) nên chạy lại ra cùng kết quả; câu đã xáo xong chạy lại sẽ xáo tiếp,
// nên chỉ chạy --apply MỘT lần. Mặc định dry-run.
//
//   node scripts/xao-y-dung-sai.mjs            # dry-run, in báo cáo
//   node scripts/xao-y-dung-sai.mjs --apply    # ghi vào file
//   node scripts/xao-y-dung-sai.mjs --apply 190.json 191.json   # chỉ các file sinh mới (đừng xáo lại bộ cũ)
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const dir = path.join(path.dirname(fileURLToPath(import.meta.url)), "data", "theory-quiz");
const apply = process.argv.includes("--apply");
const only = process.argv.slice(2).filter((a) => !a.startsWith("--"));
const L = ["a", "b", "c", "d"];

function rng(seed) {
  let s = seed >>> 0;
  return () => {
    s = (s + 0x6d2b79f5) >>> 0;
    let t = s;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function shuffled(seed) {
  const r = rng(seed);
  const p = [0, 1, 2, 3];
  for (let i = 3; i > 0; i--) {
    const j = Math.floor(r() * (i + 1));
    [p[i], p[j]] = [p[j], p[i]];
  }
  return p; // vị trí mới i giữ ý cũ p[i]
}

const REF = /(?<![\wÀ-ỹ$])ý\s+([a-d])(?![\wÀ-ỹ])/g;
const hasLabel = (s) => /(?<![\w$])[a-d]\)/.test(s);

// Trả về lời giải đã đổi nhãn, hoặc null nếu không xử lý tự động được.
function relabel(expl, p) {
  const newOf = {};
  p.forEach((old, i) => (newOf[L[old]] = L[i]));
  const swapRefs = (t) => t.replace(REF, (_, x) => `ý ${newOf[x]}`);
  if (!hasLabel(expl)) return swapRefs(expl);
  const m = expl.match(/^(\s*)a\) ([\s\S]*?)\s+b\) ([\s\S]*?)\s+c\) ([\s\S]*?)\s+d\) ([\s\S]*)$/);
  if (!m) return null;
  const seg = { a: m[2], b: m[3], c: m[4], d: m[5] };
  if (Object.values(seg).some(hasLabel)) return null;
  return m[1] + p.map((old, i) => `${L[i]}) ${swapRefs(seg[L[old]])}`).join(" ");
}

const stat = { files: 0, tf: 0, shuffled: 0, skipped: [], pos: [0, 0, 0, 0], pat: {} };
for (const f of fs.readdirSync(dir).filter((n) => n.endsWith(".json") && (!only.length || only.includes(n))).sort()) {
  const file = path.join(dir, f);
  const raw = fs.readFileSync(file, "utf8");
  const j = JSON.parse(raw);
  let changed = false;
  const style = [[1, "\n"], [1, ""], [2, "\n"], [2, ""], [4, "\n"], [0, "\n"]].find(([n, nl]) => JSON.stringify(j, null, n) + nl === raw);
  if (!style) { stat.skipped.push(`${f}(định dạng lạ, bỏ cả file)`); continue; }
  j.questions.forEach((q, qi) => {
    if (q.type !== "true_false" || q.statements?.length !== 4) return;
    stat.tf++;
    const p = shuffled((Number(j.lesson_id) || 0) * 1000 + qi + 7);
    const ctx = [q.question, ...q.statements.map((s) => s.text)].join(" ");
    const expl = relabel(q.explanation ?? "", p);
    if (REF.test(ctx) || /(?<![\w$])[a-d]\)/.test(ctx) || expl === null) {
      REF.lastIndex = 0;
      stat.skipped.push(`${f}#${qi}`);
      q.statements.forEach((s, i) => s.answer && stat.pos[i]++);
      return;
    }
    REF.lastIndex = 0;
    q.statements = p.map((old) => q.statements[old]);
    q.explanation = expl;
    if (q.distractorNotes) {
      const n = {};
      p.forEach((old, i) => { if (q.distractorNotes[old] !== undefined) n[i] = q.distractorNotes[old]; });
      q.distractorNotes = n;
    }
    q.statements.forEach((s, i) => s.answer && stat.pos[i]++);
    const key = q.statements.map((s) => (s.answer ? "T" : "F")).join("");
    stat.pat[key] = (stat.pat[key] || 0) + 1;
    stat.shuffled++;
    changed = true;
  });
  stat.files++;
  if (changed && apply) fs.writeFileSync(file, JSON.stringify(j, null, style[0]) + style[1]);
}
const pct = stat.pos.map((n) => Math.round((n / stat.tf) * 100));
console.log(apply ? "ĐÃ GHI" : "DRY-RUN", `· ${stat.files} file · ${stat.tf} câu đúng–sai · xáo ${stat.shuffled} · bỏ qua ${stat.skipped.length}`);
console.log(`Sau xáo: % Đúng ở a b c d = ${pct.join(" ")}`);
console.log("Mẫu:", Object.entries(stat.pat).sort((x, y) => y[1] - x[1]).slice(0, 6).map(([k, v]) => `${k} ${v}`).join(" · "));
if (stat.skipped.length) console.log("Bỏ qua (cần tay):", stat.skipped.join(" "));
