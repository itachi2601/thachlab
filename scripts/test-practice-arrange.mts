import { arrangeForMotivation, pickByMix, pickAndArrange, tierCounts } from "../features/lessons/practice-arrange";
type Q = { question: { difficulty: "" | "de" | "trung-binh" | "kho" } };
const mk = (de: number, tb: number, kho: number, none = 0): Q[] => [
  ...Array(de).fill(0).map(() => ({ question: { difficulty: "de" as const } })),
  ...Array(tb).fill(0).map(() => ({ question: { difficulty: "trung-binh" as const } })),
  ...Array(kho).fill(0).map(() => ({ question: { difficulty: "kho" as const } })),
  ...Array(none).fill(0).map(() => ({ question: { difficulty: "" as const } })),
];
const r = (q: Q) => (q.question.difficulty === "de" ? 0 : q.question.difficulty === "kho" ? 2 : 1);
let fail = 0;
const ok = (c: boolean, m: string) => { if (!c) { fail++; console.log("FAIL", m); } };
for (let t = 0; t < 300; t++) {
  for (const [de, tb, kho] of [[20, 20, 20], [3, 10, 15], [0, 5, 20], [2, 2, 2], [10, 0, 0]] as const) {
    const pool = mk(de, tb, kho);
    for (const band of ["weak", "mid", "strong"] as const) {
      const got = pickAndArrange(pool, 10, band);
      ok(got.length === Math.min(10, pool.length), `len ${de},${tb},${kho},${band}`);
      ok(new Set(got).size === got.length, "dup");
      if (got.length >= 6) {
        ok(r(got[got.length - 1]) <= 1 || got.every((x) => r(x) === 2), `end not hard ${de},${tb},${kho},${band}`);
        let run = 0;
        for (const x of got) { run = r(x) === 2 ? run + 1 : 0; ok(run <= 2 || (tb + de) * 2 < got.length,`run3 hard ${de},${tb},${kho}`); }
        if (de >= 2) ok(r(got[0]) === 0 && r(got[1]) === 0 || tierCounts(got)[0] < 2, `opener ${de},${tb},${kho},${band}`);
      }
    }
  }
}
const w = tierCounts(pickByMix(mk(20, 20, 20), 10, "weak"));
ok(w[0] === 5 && w[1] === 4 && w[2] === 1, `weak mix ${w}`);
const s = tierCounts(pickByMix(mk(20, 20, 20), 10, "strong"));
ok(s[0] === 2 && s[1] === 5 && s[2] === 3, `strong mix ${s}`);
const unl = pickByMix(mk(0, 0, 0, 12), 10, "weak");
ok(unl.length === 10, "unlabelled");
const sample = arrangeForMotivation(pickByMix(mk(20, 20, 20), 10, "weak")).map(r).join("");
console.log("mẫu 10 câu em yếu (0=dễ 1=TB 2=khó):", sample, fail ? `\n${fail} LỖI` : "\nOK");
process.exit(fail ? 1 : 0);
