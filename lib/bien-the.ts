/**
 * Biến thể đổi số (chặng 3A, 5/11/2026): một dạng bài tập mẫu mang khuôn đề `WorkedVariant`
 * (features/lessons/types.ts), trình duyệt tự sinh câu mới mỗi lần — không gọi API, đúng dạng chắc chắn.
 *
 * Thư viện thuần (không React, không DOM) để dùng chung cho component VariantPractice, script
 * scripts/kiem-bien-the.mts và test scripts/test-bien-the.mts.
 * Biểu thức đi qua bộ phân tích cú pháp riêng (đệ quy xuống), KHÔNG eval / new Function.
 */
import type { ExamQuestion } from "@/features/exams/types";
import type { WorkedVariant } from "@/features/lessons/types";

/* ───────────────────────────── Bộ đánh giá biểu thức ───────────────────────────── */

type Node =
  | { t: "num"; v: number }
  | { t: "var"; name: string }
  | { t: "un"; op: "-" | "!"; a: Node }
  | { t: "bin"; op: string; a: Node; b: Node }
  | { t: "call"; fn: string; args: Node[] };

type Tok = { k: "num"; v: number } | { k: "id"; v: string } | { k: "op"; v: string };

const OPS = ["<=", ">=", "==", "!=", "&&", "||", "+", "-", "*", "/", "^", "(", ")", ",", "<", ">", "!"];
const DEG = Math.PI / 180;

const FNS: Record<string, { n: number | [number, number]; f: (...a: number[]) => number }> = {
  sqrt: { n: 1, f: Math.sqrt },
  ln: { n: 1, f: Math.log },
  log10: { n: 1, f: Math.log10 },
  log2: { n: 1, f: Math.log2 },
  exp: { n: 1, f: Math.exp },
  abs: { n: 1, f: Math.abs },
  sin: { n: 1, f: (x) => Math.sin(x * DEG) },
  cos: { n: 1, f: (x) => Math.cos(x * DEG) },
  tan: { n: 1, f: (x) => Math.tan(x * DEG) },
  asin: { n: 1, f: (x) => Math.asin(x) / DEG },
  acos: { n: 1, f: (x) => Math.acos(x) / DEG },
  atan: { n: 1, f: (x) => Math.atan(x) / DEG },
  floor: { n: 1, f: Math.floor },
  ceil: { n: 1, f: Math.ceil },
  round: { n: [1, 2], f: (x, k = 0) => roundDec(x, k) },
  min: { n: [2, 9], f: Math.min },
  max: { n: [2, 9], f: Math.max },
};
const CONSTS: Record<string, number> = { pi: Math.PI };

function tokenize(src: string): Tok[] {
  const out: Tok[] = [];
  let i = 0;
  while (i < src.length) {
    const c = src[i];
    if (/\s/.test(c)) { i++; continue; }
    const num = /^(\d+\.?\d*|\.\d+)(e[+-]?\d+)?/i.exec(src.slice(i));
    if (num) { out.push({ k: "num", v: Number(num[0]) }); i += num[0].length; continue; }
    const id = /^[A-Za-z_]\w*/.exec(src.slice(i));
    if (id) { out.push({ k: "id", v: id[0] }); i += id[0].length; continue; }
    const op = OPS.find((o) => src.startsWith(o, i));
    if (!op) throw new Error(`ký tự lạ "${c}" ở vị trí ${i}`);
    out.push({ k: "op", v: op });
    i += op.length;
  }
  return out;
}

/** Phân tích biểu thức thành cây. Ném lỗi (tiếng Việt) khi sai cú pháp hoặc gọi hàm lạ. */
export function parseExpr(src: string): Node {
  const toks = tokenize(src);
  let p = 0;
  const peek = () => toks[p];
  const isOp = (v: string) => peek()?.k === "op" && peek()!.v === v;
  const eat = (v: string) => {
    if (!isOp(v)) throw new Error(`thiếu "${v}" trong "${src}"`);
    p++;
  };
  const bin = (next: () => Node, ops: string[]) => () => {
    let a = next();
    while (peek()?.k === "op" && ops.includes(String(peek()!.v))) {
      const op = (toks[p++] as { v: string }).v;
      a = { t: "bin", op, a, b: next() };
    }
    return a;
  };
  const primary = (): Node => {
    const tk = toks[p++];
    if (!tk) throw new Error(`biểu thức "${src}" bị cụt`);
    if (tk.k === "num") return { t: "num", v: tk.v };
    if (tk.k === "id") {
      if (isOp("(")) {
        const fn = Object.hasOwn(FNS, tk.v) ? FNS[tk.v] : undefined;
        if (!fn) throw new Error(`hàm lạ "${tk.v}"`);
        p++;
        const args: Node[] = [];
        if (!isOp(")")) {
          args.push(or());
          while (isOp(",")) { p++; args.push(or()); }
        }
        eat(")");
        const [lo, hi] = Array.isArray(fn.n) ? fn.n : [fn.n, fn.n];
        if (args.length < lo || args.length > hi) throw new Error(`hàm ${tk.v} nhận ${lo === hi ? lo : `${lo}–${hi}`} đối số`);
        return { t: "call", fn: tk.v, args };
      }
      return { t: "var", name: tk.v };
    }
    if (tk.v === "(") { const e = or(); eat(")"); return e; }
    throw new Error(`không chờ "${tk.v}" trong "${src}"`);
  };
  // ^ kết hợp phải và chặt hơn dấu trừ một ngôi: -2^2 = -4, 2^-1 = 0,5
  const power = (): Node => {
    const a = primary();
    if (isOp("^")) { p++; return { t: "bin", op: "^", a, b: unary() }; }
    return a;
  };
  const unary = (): Node => {
    if (isOp("-") || isOp("!")) { const op = (toks[p++] as { v: "-" | "!" }).v; return { t: "un", op, a: unary() }; }
    if (isOp("+")) { p++; return unary(); }
    return power();
  };
  const mul = bin(unary, ["*", "/"]);
  const add = bin(mul, ["+", "-"]);
  const cmp = bin(add, ["<", "<=", ">", ">=", "==", "!="]);
  const and = bin(cmp, ["&&"]);
  const or = bin(and, ["||"]);
  const tree = or();
  if (p < toks.length) throw new Error(`thừa "${(toks[p] as { v: unknown }).v}" trong "${src}"`);
  return tree;
}

/** Các tên biến một biểu thức đọc (để kiểm khuôn trước khi sinh). */
export function exprNames(n: Node, acc = new Set<string>()): Set<string> {
  if (n.t === "var") acc.add(n.name);
  else if (n.t === "un") exprNames(n.a, acc);
  else if (n.t === "bin") { exprNames(n.a, acc); exprNames(n.b, acc); }
  else if (n.t === "call") n.args.forEach((a) => exprNames(a, acc));
  return acc;
}

export type Scope = Record<string, number>;

export function evalNode(n: Node, s: Scope): number {
  switch (n.t) {
    case "num": return n.v;
    case "var": {
      if (Object.hasOwn(s, n.name)) return s[n.name];
      if (Object.hasOwn(CONSTS, n.name)) return CONSTS[n.name];
      throw new Error(`biến chưa có "${n.name}"`);
    }
    case "un": { const a = evalNode(n.a, s); return n.op === "-" ? -a : a ? 0 : 1; }
    case "call": return FNS[n.fn].f(...n.args.map((a) => evalNode(a, s)));
    case "bin": {
      const a = evalNode(n.a, s), b = evalNode(n.b, s);
      switch (n.op) {
        case "+": return a + b;
        case "-": return a - b;
        case "*": return a * b;
        case "/": return a / b;
        case "^": return Math.pow(a, b);
        case "<": return a < b ? 1 : 0;
        case "<=": return a <= b ? 1 : 0;
        case ">": return a > b ? 1 : 0;
        case ">=": return a >= b ? 1 : 0;
        case "==": return Math.abs(a - b) <= 1e-9 * Math.max(1, Math.abs(a), Math.abs(b)) ? 1 : 0;
        case "!=": return Math.abs(a - b) <= 1e-9 * Math.max(1, Math.abs(a), Math.abs(b)) ? 0 : 1;
        case "&&": return a && b ? 1 : 0;
        case "||": return a || b ? 1 : 0;
      }
      throw new Error(`phép lạ "${n.op}"`);
    }
  }
}

const cache = new Map<string, Node>();
/** Tính một biểu thức (có cache cây). */
export function evaluate(src: string, s: Scope): number {
  let n = cache.get(src);
  if (!n) { n = parseExpr(src); cache.set(src, n); }
  return evalNode(n, s);
}

/* ───────────────────────────── Số ngẫu nhiên có seed ───────────────────────────── */

/** mulberry32: cùng seed → cùng dãy số (để tái hiện câu khi cần, kiểm 200 bộ số cố định). */
export function mulberry32(seed: number): () => number {
  // trộn seed trước (seed liền nhau 1, 2, 3… không cho số đầu na ná nhau)
  let a = Math.imul((seed >>> 0) ^ 0x9e3779b9, 0x85ebca6b);
  a = Math.imul(a ^ (a >>> 13), 0xc2b2ae35);
  a = (a ^ (a >>> 16)) >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/* ───────────────────────────── Làm tròn & in số ───────────────────────────── */

export function roundDec(x: number, k: number): number {
  const f = Math.pow(10, k);
  return Math.round((x + Math.sign(x) * Number.EPSILON * Math.abs(x)) * f) / f;
}

function decimalsOf(step: number): number {
  const s = String(step);
  if (s.includes("e-")) return Number(s.split("e-")[1]);
  return s.includes(".") ? s.split(".")[1].length : 0;
}

export type RoundSpec = { cs: number } | { tp: number };

/** Làm tròn theo chữ số có nghĩa / chữ số thập phân. */
export function roundSpec(x: number, spec: RoundSpec): number {
  if (!Number.isFinite(x) || x === 0) return x;
  if ("tp" in spec) return roundDec(x, spec.tp);
  const e = Math.floor(Math.log10(Math.abs(x)));
  const k = spec.cs - 1 - e;
  return k >= 0 ? roundDec(x, k) : Math.round(x / Math.pow(10, -k)) * Math.pow(10, -k);
}

/** Nửa đơn vị của chữ số cuối khi làm tròn (sai số làm tròn cho phép). */
export function halfUnit(x: number, spec: RoundSpec): number {
  if ("tp" in spec) return 0.5 * Math.pow(10, -spec.tp);
  if (x === 0) return 0;
  const e = Math.floor(Math.log10(Math.abs(x)));
  return 0.5 * Math.pow(10, e - spec.cs + 1);
}

const stripZeros = (s: string) => (s.includes(".") ? s.replace(/\.?0+$/, "") : s);

/**
 * In số kiểu đề Việt Nam. `latex`: dấu phẩy `{,}` và lũy thừa `6{,}4.10^{18}` (dùng trong $…$);
 * không latex: "2,2" (đáp án ô Phần III). Số |x| ≥ 1e5 hoặc < 1e-3 in dạng a.10^n (chỉ khi latex).
 */
export function formatNum(x: number, spec: RoundSpec, latex = true): string {
  if (!Number.isFinite(x)) return String(x);
  const comma = latex ? "{,}" : ",";
  const ax = Math.abs(x);
  if (latex && "cs" in spec && x !== 0 && (ax >= 1e5 || ax < 1e-3)) {
    let e = Math.floor(Math.log10(ax));
    let m = roundDec(x / Math.pow(10, e), spec.cs - 1);
    if (Math.abs(m) >= 10) { m /= 10; e += 1; }
    if (Math.abs(m) === 1) return `${m < 0 ? "-" : ""}10^{${e}}`; // "1.10^{5}" dễ đọc nhầm thành 1,10
    return `${stripZeros(m.toFixed(spec.cs - 1)).replace(".", comma)}.10^{${e}}`;
  }
  const r = roundSpec(x, spec);
  let dec: number;
  if ("tp" in spec) dec = spec.tp;
  else dec = r === 0 ? 0 : Math.max(0, spec.cs - 1 - Math.floor(Math.log10(Math.abs(r))));
  const s = stripZeros(r.toFixed(dec));
  return (s === "-0" ? "0" : s).replace(".", comma);
}

/* ───────────────────────────── Sinh câu ───────────────────────────── */

const PH = /\{\{\s*([A-Za-z_]\w*)\s*(?:\|\s*(\.?\d+))?\s*\}\}/g;
const DEFAULT_SPEC: RoundSpec = { cs: 3 };
const LETTERS = ["A", "B", "C", "D"];

export interface VariantQuestion {
  seed: number;
  /** Câu dựng sẵn cho QuestionCard (đủ đáp án, lời giải, distractorNotes) — nhãn A. B. C. D. / ô đáp số do QuestionCard sinh (E1–E3). */
  question: ExamQuestion;
  /** Đáp số chưa làm tròn (chấm sai số). */
  exact: number;
  /** abcd: bước gỡ rối gợi ý theo phương án (undefined ở đáp án đúng hoặc nhiễu không gắn bước). */
  stepByOption?: (number | undefined)[];
  scope: Scope;
}

export type TryResult = { ok: true; q: VariantQuestion } | { ok: false; loi: string };

function specOf(v: WorkedVariant): RoundSpec {
  return v.lam_tron ?? DEFAULT_SPEC;
}

/** Thay chỗ trống `{{ten|…}}`. Số của biến ngẫu nhiên in theo số lẻ của bước, đại lượng tính in 3 chữ số có nghĩa. */
export function fillTemplate(html: string, v: WorkedVariant, scope: Scope, texts: Record<string, string>): string {
  return html.replace(PH, (_m, name: string, fmt?: string) => {
    if (Object.hasOwn(texts, name)) return texts[name];
    if (!Object.hasOwn(scope, name)) throw new Error(`chỗ trống lạ {{${name}}}`);
    const x = scope[name];
    let spec: RoundSpec;
    if (fmt) spec = fmt.startsWith(".") ? { tp: Number(fmt.slice(1)) } : { cs: Number(fmt) };
    else if (name === "dap_so") spec = specOf(v);
    else if (Object.hasOwn(v.bien, name)) {
      const ax = Math.abs(x);
      spec = ax >= 1e5 || (ax < 1e-3 && x !== 0) ? { cs: 3 } : { tp: decimalsOf(v.bien[name].buoc) };
    } else spec = DEFAULT_SPEC;
    return formatNum(x, spec, true);
  });
}

function relDiff(a: number, b: number): number {
  const m = Math.max(Math.abs(a), Math.abs(b));
  return m === 0 ? 0 : Math.abs(a - b) / m;
}

function shuffle<T>(arr: T[], rng: () => number): T[] {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(rng() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

/** MỘT lần bốc số (không thử lại) — script kiểm dùng để đếm từng loại vi phạm. */
export function tryOnce(v: WorkedVariant, seed: number): TryResult {
  const rng = mulberry32(seed);
  const scope: Scope = {};
  const texts: Record<string, string> = {};
  if (v.bo?.length) {
    const pick = v.bo[Math.floor(rng() * v.bo.length)];
    for (const [k, x] of Object.entries(pick)) {
      if (typeof x === "number") scope[k] = x;
      else texts[k] = x;
    }
  }
  for (const [k, b] of Object.entries(v.bien)) {
    const n = Math.round((b.max - b.min) / b.buoc);
    const i = Math.floor(rng() * (n + 1));
    scope[k] = roundDec(b.min + i * b.buoc, decimalsOf(b.buoc));
  }
  try {
    for (const [k, e] of Object.entries(v.tinh ?? {})) scope[k] = evaluate(e, scope);
    scope.dap_so = evaluate(v.dap_so, scope);
  } catch (e) {
    return { ok: false, loi: `lỗi biểu thức: ${(e as Error).message}` };
  }
  for (const [k, x] of Object.entries(scope)) if (!Number.isFinite(x)) return { ok: false, loi: `NaN/vô cực ở "${k}"` };
  for (const r of v.rang_buoc ?? []) {
    let ok: number;
    try { ok = evaluate(r, scope); } catch (e) { return { ok: false, loi: `lỗi ràng buộc: ${(e as Error).message}` }; }
    if (!Number.isFinite(ok) || !ok) return { ok: false, loi: `vi phạm ràng buộc "${r}"` };
  }
  const exact = scope.dap_so;
  const spec = specOf(v);
  const minDiff = v.khac_nhau ?? 0.05;
  let html: string, sol: string;
  try {
    html = fillTemplate(v.de, v, scope, texts);
    sol = v.loi_giai ? fillTemplate(v.loi_giai, v, scope, texts) : "";
  } catch (e) {
    return { ok: false, loi: (e as Error).message };
  }

  if (v.kieu === "so") {
    const answer = formatNum(exact, spec, false);
    if (answer.length > 4) return { ok: false, loi: `đáp số "${answer}" dài hơn 4 ký tự (ô Phần III)` };
    return { ok: true, q: { seed, exact, scope, question: { type: "short_answer", question: html, answer, explanation: sol } } };
  }

  // abcd: đáp án đúng + 3 nhiễu đầu tiên hợp lệ
  const picks: { x: number; loi: string; buoc?: number }[] = [];
  let lastWhy = "không đủ 3 phương án nhiễu";
  for (const d of v.nhieu ?? []) {
    if (picks.length === 3) break;
    let x: number;
    try { x = evaluate(d.bieu_thuc, scope); } catch (e) { return { ok: false, loi: `lỗi biểu thức nhiễu: ${(e as Error).message}` }; }
    if (!Number.isFinite(x)) { lastWhy = `phương án nhiễu NaN/vô cực "${d.bieu_thuc}"`; continue; }
    if (exact > 0 && x <= 0) { lastWhy = `phương án nhiễu âm/không "${d.bieu_thuc}"`; continue; }
    const all = [exact, ...picks.map((p) => p.x)];
    if (all.some((y) => relDiff(x, y) < minDiff)) { lastWhy = `phương án trùng/gần nhau (< ${minDiff * 100} %) "${d.bieu_thuc}"`; continue; }
    picks.push({ x, loi: d.loi, buoc: d.buoc });
  }
  if (picks.length < 3) return { ok: false, loi: lastWhy };
  const opts = shuffle([{ x: exact, loi: "", buoc: undefined as number | undefined, right: true }, ...picks.map((p) => ({ ...p, right: false }))], rng);
  const unit = v.don_vi ? ` ${v.don_vi}` : "";
  const options = opts.map((o) => `$${formatNum(o.x, spec, true)}$${unit}`);
  if (new Set(options).size < 4) return { ok: false, loi: "hai phương án in ra giống nhau sau làm tròn" };
  const notes: Record<string, string> = {};
  opts.forEach((o, i) => { if (!o.right && o.loi) notes[LETTERS[i]] = o.loi; });
  return {
    ok: true,
    q: {
      seed,
      exact,
      scope,
      stepByOption: opts.map((o) => o.buoc),
      question: {
        type: "multiple_choice",
        question: html,
        options,
        answer: opts.findIndex((o) => o.right),
        explanation: sol,
        distractorNotes: notes,
      },
    },
  };
}

/** Sinh một câu: thử tối đa `tries` bộ số (seed liên tiếp) tới khi qua mọi ràng buộc. null = khuôn hỏng. */
export function generate(v: WorkedVariant, seed: number, tries = 200): VariantQuestion | null {
  for (let i = 0; i < tries; i++) {
    const r = tryOnce(v, (seed + i * 0x9e3779b1) >>> 0);
    if (r.ok) return r.q;
  }
  return null;
}

/** Chấm ô đáp số: khớp chuỗi đáp án, hoặc lệch ≤ sai_so tương đối + nửa đơn vị làm tròn. */
export function gradeNumeric(input: string, q: VariantQuestion, v: WorkedVariant): { dung: boolean; khopChuoi: boolean } {
  const norm = input.trim().replace(/[−–]/g, "-").replace(",", ".");
  const ans = q.question.type === "short_answer" ? q.question.answer.replace(",", ".") : "";
  if (norm !== "" && norm === ans) return { dung: true, khopChuoi: true };
  const x = Number(norm);
  if (!/^-?\d+(\.\d+)?$/.test(norm) || !Number.isFinite(x)) return { dung: false, khopChuoi: false };
  const tol = (v.sai_so ?? 0) * Math.abs(q.exact) + halfUnit(q.exact, specOf(v)) * (1 + 1e-9);
  return { dung: Math.abs(x - q.exact) <= tol, khopChuoi: false };
}

/* ───────────────────────────── Kiểm khuôn (tĩnh) ───────────────────────────── */

/** Lỗi soạn khuôn thấy được không cần sinh số: cú pháp biểu thức, tên lạ, chỗ trống số nằm ngoài $…$. */
export function checkTemplate(v: WorkedVariant): string[] {
  const errs: string[] = [];
  const textNames = new Set<string>();
  const numNames = new Set<string>(Object.keys(CONSTS));
  if (v.bo?.length) {
    const keys = Object.keys(v.bo[0]).sort().join(",");
    v.bo.forEach((b, i) => { if (Object.keys(b).sort().join(",") !== keys) errs.push(`bo[${i}] khác trường với bo[0]`); });
    for (const [k, x] of Object.entries(v.bo[0])) (typeof x === "number" ? numNames : textNames).add(k);
  }
  for (const [k, b] of Object.entries(v.bien ?? {})) {
    if (!(b.buoc > 0) || !(b.max >= b.min)) errs.push(`bien.${k}: cần buoc > 0 và max ≥ min`);
    else if (Math.abs((b.max - b.min) / b.buoc - Math.round((b.max - b.min) / b.buoc)) > 1e-6) errs.push(`bien.${k}: (max − min) không chia hết cho buoc`);
    numNames.add(k);
  }
  const need = (label: string, src: string) => {
    try {
      for (const n of exprNames(parseExpr(src))) if (!numNames.has(n)) errs.push(`${label}: biến chưa khai báo "${n}"`);
    } catch (e) {
      errs.push(`${label}: ${(e as Error).message}`);
    }
  };
  for (const [k, e] of Object.entries(v.tinh ?? {})) { need(`tinh.${k}`, e); numNames.add(k); }
  need("dap_so", v.dap_so);
  numNames.add("dap_so");
  (v.rang_buoc ?? []).forEach((r, i) => need(`rang_buoc[${i}]`, r));
  if (v.kieu === "abcd") {
    if ((v.nhieu?.length ?? 0) < 3) errs.push("kieu abcd cần ≥ 3 phương án nhiễu");
    (v.nhieu ?? []).forEach((d, i) => {
      need(`nhieu[${i}]`, d.bieu_thuc);
      if (!d.loi?.trim()) errs.push(`nhieu[${i}]: thiếu "loi" (vì sao em chọn sai)`);
    });
  } else if (v.kieu !== "so") errs.push(`kieu phải là "so" hoặc "abcd"`);
  for (const [label, html] of [["de", v.de], ["loi_giai", v.loi_giai ?? ""]] as const) {
    if (((html.replace(/\\\$/g, "").match(/\$/g) ?? []).length) % 2) errs.push(`${label}: số dấu $ lẻ`);
    for (const m of html.matchAll(PH)) {
      const name = m[1];
      if (textNames.has(name)) continue;
      if (!numNames.has(name)) { errs.push(`${label}: chỗ trống lạ {{${name}}}`); continue; }
      const before = html.slice(0, m.index).replace(/\\\$/g, "");
      if (((before.match(/\$/g) ?? []).length) % 2 === 0) errs.push(`${label}: {{${name}}} nằm ngoài $…$`);
    }
  }
  return errs;
}
