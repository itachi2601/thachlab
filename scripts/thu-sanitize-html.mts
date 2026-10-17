/**
 * Chạy THỬ (chỉ đọc) bộ sanitize HTML đề xuất trên toàn bộ nội dung đang có, in ra thứ bị gỡ.
 *   npx tsx scripts/thu-sanitize-html.mts            # content/**\/*.html + DB (cần .env.local)
 *   npx tsx scripts/thu-sanitize-html.mts --no-db    # chỉ file trong content/
 * Không ghi gì vào DB/file nguồn; báo cáo lưu ở scripts/logs/thu-sanitize-<giờ>.txt.
 * Cấu hình lấy từ lib/sanitize-html.ts (cùng cấu hình sẽ dùng cho ContentHtml).
 */
import fs from "node:fs";
import path from "node:path";
import { JSDOM } from "jsdom";
import createDOMPurify from "dompurify";
import katex from "katex";
import { createClient } from "@supabase/supabase-js";
import { PURIFY_CONFIG, installIframeHook, installSmilHook } from "../lib/sanitize-html";

const root = path.resolve(import.meta.dirname, "..");
const win = new JSDOM("").window;
const purify = createDOMPurify(win as unknown as Window & typeof globalThis);
installIframeHook(purify as never);
installSmilHook(purify as never);

function env(name: string): string | undefined {
  if (process.env[name]) return process.env[name];
  try {
    const m = fs.readFileSync(path.join(root, ".env.local"), "utf8").match(new RegExp(`^${name}=(.*)$`, "m"));
    return m?.[1]?.trim().replace(/^["']|["']$/g, "");
  } catch {
    return undefined;
  }
}

type Removed = { kind: "tag" | "attr"; name: string };
const tally = new Map<string, { count: number; sources: Set<string>; sample: string }>();
let scanned = 0;
let changedItems = 0;
const lines: string[] = [];

function check(html: string, source: string) {
  if (!html || !html.includes("<")) return;
  scanned++;
  const clean = purify.sanitize(html, PURIFY_CONFIG as never) as unknown as string;
  const removed = purify.removed as Array<{ element?: Element; attribute?: Attr; from?: Element }>;
  let any = false;
  for (const r of removed) {
    let rm: Removed | null = null;
    if (r.element) rm = { kind: "tag", name: r.element.nodeName.toLowerCase() };
    else if (r.attribute) rm = { kind: "attr", name: `${r.attribute.name} (trên <${r.from?.nodeName.toLowerCase() ?? "?"}>)` };
    if (!rm) continue;
    // thẻ rỗng #text bị gỡ khi cắt nội dung con của thẻ cấm: bỏ qua, chỉ đếm thẻ/thuộc tính thật
    if (rm.kind === "tag" && rm.name.startsWith("#")) continue;
    any = true;
    const key = `${rm.kind}:${rm.name}`;
    const e = tally.get(key) ?? { count: 0, sources: new Set<string>(), sample: "" };
    e.count++;
    e.sources.add(source);
    if (!e.sample) {
      const el = (r.element ?? r.attribute?.ownerElement ?? r.from) as Element | undefined;
      e.sample = (r.attribute ? `${r.attribute.name}="${String(r.attribute.value).slice(0, 120)}" ← ` : "") + (el?.outerHTML ?? "").slice(0, 120).replace(/\s+/g, " ");
    }
    tally.set(key, e);
  }
  if (any) changedItems++;
}

function walkStrings(v: unknown, fn: (s: string) => void) {
  if (typeof v === "string") fn(v);
  else if (Array.isArray(v)) v.forEach((x) => walkStrings(x, fn));
  else if (v && typeof v === "object") Object.values(v as Record<string, unknown>).forEach((x) => walkStrings(x, fn));
}

function listHtml(dir: string, out: string[] = []): string[] {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) listHtml(p, out);
    else if (e.name === "theory.html") out.push(p); // trang xem thử/lộ trình độc lập (có <script> riêng) KHÔNG đi qua ContentHtml
  }
  return out;
}

// ───────── 1. file trong content/ ─────────
const files = listHtml(path.join(root, "content"));
for (const f of files) check(fs.readFileSync(f, "utf8"), path.relative(root, f));
lines.push(`content/: ${files.length} file .html`);

// ───────── 2. KaTeX: công thức thật đi qua sanitize có nguyên vẹn không ─────────
const formulas = new Set<string>();
for (const f of files.slice(0, 400)) {
  const t = fs.readFileSync(f, "utf8");
  for (const m of t.matchAll(/\$([^$\n]{2,120})\$/g)) {
    formulas.add(m[1]);
    if (formulas.size >= 1500) break;
  }
  if (formulas.size >= 1500) break;
}
const scratch = win.document.createElement("div");
const norm = (h: string) => {
  scratch.innerHTML = h;
  return scratch.innerHTML;
};
let katexBroken = 0;
let katexTried = 0;
for (const fm of formulas) {
  let rendered: string;
  try {
    rendered = katex.renderToString(fm, { throwOnError: true, displayMode: false, strict: "ignore" });
  } catch {
    continue;
  }
  katexTried++;
  const before = norm(rendered);
  const after = purify.sanitize(rendered, PURIFY_CONFIG as never) as unknown as string;
  const afterNorm = norm(after);
  if (before !== afterNorm) {
    katexBroken++;
    if (katexBroken <= 2) {
      let i = 0;
      while (i < before.length && before[i] === afterNorm[i]) i++;
      lines.push(`  KaTeX khác sau sanitize: $${fm}$ — lệch tại ${i}: trước «${before.slice(Math.max(0, i - 40), i + 80)}» sau «${afterNorm.slice(Math.max(0, i - 40), i + 80)}»`);
    }
  }
}
lines.push(`KaTeX: thử ${katexTried} công thức, ${katexBroken} cái bị đổi sau sanitize`);

// ───────── 3. DB (chỉ đọc) ─────────
if (!process.argv.includes("--no-db")) {
  const url = env("NEXT_PUBLIC_SUPABASE_URL");
  const key = env("SUPABASE_SERVICE_ROLE_KEY") ?? env("NEXT_PUBLIC_SUPABASE_ANON_KEY");
  if (!url || !key) throw new Error("thiếu URL/khoá Supabase trong .env.local");
  const sb = createClient(url, key, { auth: { persistSession: false, autoRefreshToken: false } });

  async function pageAll(table: string, cols: string, idCol: string, each: (row: Record<string, unknown>) => void) {
    let from = 0;
    let n = 0;
    for (;;) {
      const { data, error } = await sb.from(table).select(cols).order(idCol).range(from, from + 999);
      if (error) throw new Error(`${table}: ${error.message}`);
      if (!data?.length) break;
      (data as unknown as Record<string, unknown>[]).forEach(each);
      n += data.length;
      if (data.length < 1000) break;
      from += 1000;
    }
    lines.push(`DB ${table}: ${n} dòng`);
  }

  await pageAll("lesson_items", "id,body_html,questions", "id", (r) => {
    check(String(r.body_html ?? ""), `lesson_items#${r.id}.body_html`);
    walkStrings(r.questions, (s) => check(s, `lesson_items#${r.id}.questions`));
  });
  await pageAll("cnc_lessons", "id,body_html", "id", (r) => check(String(r.body_html ?? ""), `cnc_lessons#${r.id}`));
  await pageAll("question_bank", "id,question", "id", (r) => walkStrings(r.question, (s) => check(s, `question_bank#${r.id}`)));
}

// ───────── báo cáo ─────────
lines.push(`\nĐã quét ${scanned} chuỗi có HTML; ${changedItems} chuỗi bị sanitize gỡ ít nhất một thứ.`);
if (tally.size === 0) lines.push("KHÔNG có thẻ/thuộc tính nào bị gỡ.");
for (const [k, v] of [...tally.entries()].sort((a, b) => b[1].count - a[1].count)) {
  lines.push(`\n• ${k}  ×${v.count}  (${v.sources.size} nguồn, vd ${[...v.sources].slice(0, 3).join(", ")})`);
  lines.push(`    mẫu: ${v.sample}`);
}
const out = lines.join("\n");
console.log(out);
fs.mkdirSync(path.join(root, "scripts/logs"), { recursive: true });
fs.writeFileSync(path.join(root, `scripts/logs/thu-sanitize-${new Date().toISOString().replace(/[:.]/g, "-")}.txt`), out);
