// Ảnh đường dẫn tương đối (/lessons/<bài>/hinh/figNN.png) → URL đầy đủ https://thachlab.id.vn/lessons/… (chỉ khi tải được HTTP 200), ngân hàng + bản sao đề, một giao dịch/chunk như sua-so-mu-dong-bo.mts.
//   npx tsx scripts/sua-anh-src-dong-bo.mts → scripts/data/gon-ngan-hang/anh/chunk-NN.sql + backup-anh.json
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import { execSync } from "node:child_process";
const L0 = fs.readFileSync(".env.local", "utf8").split("\n");
const env = (k: string) => L0.find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const BASE = "https://thachlab.id.vn";
const ok = new Map<string, boolean>();
async function sống(p: string) { if (!ok.has(p)) { try { const r = await fetch(BASE + p, { method: "HEAD" }); ok.set(p, r.status === 200 && /image/.test(r.headers.get("content-type") ?? "")); } catch { ok.set(p, false); } } return ok.get(p)!; }
function mapStrings(v: any, f: (s: string) => string): any { if (typeof v === "string") return f(v); if (Array.isArray(v)) return v.map((x) => mapStrings(x, f)); if (v && typeof v === "object") return Object.fromEntries(Object.entries(v).map(([k, x]) => [k, mapStrings(x, f)])); return v; }
const RE = /(<img[^>]*?\bsrc=")(\/(?:lessons|images)\/[^"]+)(")/g;
async function chuanBi(q: any) { const ps = new Set<string>(); mapStrings(q, (s) => { for (const m of s.matchAll(RE)) ps.add(m[2]); return s; }); for (const p of ps) await sống(p); }
const fix = (s: string) => s.replace(RE, (m, a, p, c) => (ok.get(p) ? a + BASE + p + c : m));
// ---- Phần riêng: sửa mất ^ ở ngân hàng + MỌI bản sao trong exams.questions, trong một giao dịch có tắt trigger (xem sự cố hash/trigger 18/10).
//   npx tsx scripts/sua-so-mu-dong-bo.mts [--only=mu10] [--cap=cờ]   → dry-run: ghi scripts/data/gon-ngan-hang/mu/{mau.json,chunk-NN.sql,bao-cao.json}
//   chạy từng file: supabase db query --linked -f scripts/data/gon-ngan-hang/mu/chunk-NN.sql  (sao lưu trước đó ở backup-mu.json)
const OUT = "scripts/data/gon-ngan-hang/anh/"; fs.mkdirSync(OUT, { recursive: true });
const CAP = "anhSrcTuongDoi";
const flagged = new Set<number>(JSON.parse(fs.readFileSync("scripts/data/gon-ngan-hang/de-hu.json", "utf8")).filter((x: any) => x.flags.includes(CAP)).map((x: any) => x.id));
execSync("supabase db query --linked -f scripts/data/gon-ngan-hang/in-use.sql -o json > scripts/data/gon-ngan-hang/in-use.raw 2>/dev/null", { shell: "/bin/bash" });
const raw = fs.readFileSync("scripts/data/gon-ngan-hang/in-use.raw", "utf8"); const byHash = new Map<string, { exam: number; idx: number }[]>();
for (const r of JSON.parse(raw.slice(raw.indexOf("{"), raw.lastIndexOf("}") + 1)).rows) (byHash.get(r.h) ?? byHash.set(r.h, []).get(r.h)!).push({ exam: r.exam_id, idx: r.idx });
const need = new Set<number>(); const bank: any[] = [];
for (let f = 0; ; f += 500) { let d: any; for (let t = 0; t < 5; t++) { const r = await sb.from("question_bank").select("id,content_hash,question").eq("archived", false).in("id", [...flagged].slice(f, f + 500)); if (!r.error) { d = r.data; break; } await new Promise((s) => setTimeout(s, 2000)); } if (!d) throw new Error("timeout"); bank.push(...d); if (f + 500 >= flagged.size) break; }
const exCache = new Map<number, any[]>(); const exOf = async (id: number) => { if (!exCache.has(id)) { const { data, error } = await sb.from("exams").select("questions").eq("id", id).single(); if (error) throw error; exCache.set(id, data!.questions); } return exCache.get(id)!; };
const items: any[] = [], mau: any[] = [], bk: any[] = [], ambigAll: any[] = []; let katexBo = 0, khongDoi = 0, chuaKhop = 0;
for (const r of bank) {
  await chuanBi(r.question);
  const nq = mapStrings(r.question, fix);
  if (JSON.stringify(nq) === JSON.stringify(r.question)) { khongDoi++; continue; }
  const changes: any[] = [];
  const ex: any[] = [];
  for (const u of byHash.get(r.content_hash) ?? []) { const qs = await exOf(u.exam); const el = qs[u.idx]; if (!el) continue; ex.push({ exam: u.exam, idx: u.idx, el: mapStrings(el, fix) }); }
  if (!(byHash.get(r.content_hash) ?? []).length) chuaKhop++;
  items.push({ id: r.id, nq, ex }); bk.push({ id: r.id, question: r.question, ex: ex.map((e) => ({ exam: e.exam, idx: e.idx })) });
  mau.push({ id: r.id });
}
mau.sort(() => Math.random() - 0.5); fs.writeFileSync(OUT + "mau.json", JSON.stringify(mau.slice(0, 70), null, 1)); fs.writeFileSync(OUT + "bao-cao.json", JSON.stringify(ambigAll, null, 1)); fs.writeFileSync(OUT + "backup-mu.json", JSON.stringify(bk));
const eqTag = (s: string) => { let t = "j"; while (s.includes("$" + t + "$")) t += "x"; return "$" + t + "$"; };
for (let i = 0, n = 1; i < items.length; i += 120, n++) { const part = JSON.stringify(items.slice(i, i + 120)); const tg = eqTag(part);
  fs.writeFileSync(OUT + `chunk-${String(n).padStart(2, "0")}.sql`, `begin;\nalter table public.exams disable trigger trg_exams_sync_bank;\ndo $do$ declare r jsonb; e jsonb; h text; begin\n  for r in select * from jsonb_array_elements(${tg}${part}${tg}::jsonb) loop\n    h := public.question_content_hash(r->'nq');\n    if exists (select 1 from public.question_bank where content_hash = h and id <> (r->>'id')::bigint) then raise notice 'TRUNG %', r->>'id'; continue; end if;\n    update public.question_bank set question = r->'nq', content_hash = h, updated_at = now() where id = (r->>'id')::bigint;\n    for e in select * from jsonb_array_elements(r->'ex') loop\n      update public.exams set questions = jsonb_set(questions, array[e->>'idx'], e->'el') where id = (e->>'exam')::bigint;\n    end loop;\n  end loop;\nend $do$;\nalter table public.exams enable trigger trg_exams_sync_bank;\ncommit;\n`); }
console.log(`cờ ${CAP}: ${flagged.size} câu · sẽ sửa ${items.length} · bản sao đề ${items.reduce((s, x) => s + x.ex.length, 0)} · không đổi ${khongDoi} · bỏ vì KaTeX ${katexBo} · không thấy trong đề nào ${chuaKhop}`);
