// Sửa src ảnh bị dính tiền tố "/lessons/<slug>/" trước https://… trong question_bank.
//   npx tsx scripts/sua-link-anh-hong.mts [--apply] [id id …]   (mặc định dry-run, không ghi)
//   npx tsx scripts/sua-link-anh-hong.mts --rollback <file sao lưu>
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
const dir = path.dirname(fileURLToPath(import.meta.url));
const env = fs.readFileSync(path.resolve(dir, "..", ".env.local"), "utf8");
const g = (k: string) => env.split("\n").find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const sb = createClient(g("NEXT_PUBLIC_SUPABASE_URL"), g("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const args = process.argv.slice(2);
const APPLY = args.includes("--apply");
const rb = args.indexOf("--rollback");
if (rb >= 0) {
  const bk = JSON.parse(fs.readFileSync(args[rb + 1], "utf8")) as { id: number; question: unknown }[];
  for (const r of bk) { const { error } = await sb.from("question_bank").update({ question: r.question }).eq("id", r.id); console.log(r.id, error?.message ?? "đã trả"); }
  process.exit(0);
}
const ids = args.filter((a) => /^\d+$/.test(a)).map(Number);
const BAD = /(?:\/lessons\/[a-z0-9-]+\/)+(https:\/\/[^"'\s)\\]+)/g;
const backup: { id: number; question: unknown }[] = [];
const bkFile = path.join(dir, "logs", `sua-link-anh-hong-${new Date().toISOString().replace(/[:.]/g, "-")}.backup.json`);
fs.mkdirSync(path.join(dir, "logs"), { recursive: true });
let problems = 0;
for (const id of ids) {
  const { data, error } = await sb.from("question_bank").select("id, question").eq("id", id).single();
  if (error || !data) { console.log(id, "KHÔNG đọc được", error?.message); problems++; continue; }
  const s = JSON.stringify(data.question);
  const fixes = [...s.matchAll(BAD)].map((m) => [m[0], m[1]] as const);
  const imgs = [...s.matchAll(/<img\b[^>]*?src=\\"([^"\\]+)\\"/g)].map((m) => m[1]);
  console.log(`\n#${id}: ${imgs.length} ảnh, ${fixes.length} link hỏng`);
  for (const [o, n] of fixes) { const r = await fetch(n, { method: "HEAD" }); console.log("  ", o.slice(0, 60) + "…", "→", n.slice(-45), r.status); if (!r.ok) problems++; }
  const rest = imgs.filter((u) => !/^https:\/\//.test(u) && !u.startsWith("data:")).filter((u) => !fixes.some(([o]) => o === u));
  if (rest.length) { console.log("   ảnh src lạ còn lại:", rest); problems++; }
  if (!fixes.length) continue;
  if (APPLY) {
    backup.push({ id, question: data.question });
    fs.writeFileSync(bkFile, JSON.stringify(backup));
    const out = JSON.parse(s.replace(BAD, "$1"));
    const u = await sb.from("question_bank").update({ question: out }).eq("id", id);
    console.log("   ", u.error ? "LỖI " + u.error.message : "đã ghi");
  }
}
if (APPLY && backup.length) console.log("\nSao lưu:", bkFile);
console.log(APPLY ? "" : "\nDRY-RUN: chưa ghi gì.", problems ? `${problems} vấn đề` : "không vấn đề");
