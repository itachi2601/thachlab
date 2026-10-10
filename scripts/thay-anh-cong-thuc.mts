// Thay ảnh công thức (MathType → PNG nhỏ) bằng chữ LaTeX `$…$` trong câu ngân hàng + mọi đề đang dùng câu đó.
// Đầu vào: ~/Downloads/duyet-cong-thuc.json (xuất từ scripts/data/kiem-ke-anh-ngan-hang/duyet-cong-thuc.html sau khi thầy duyệt).
//   npx tsx scripts/thay-anh-cong-thuc.mts [file.json]           # dry-run: kiểm LaTeX bằng KaTeX, in kế hoạch
//   npx tsx scripts/thay-anh-cong-thuc.mts [file.json] --ghi     # ghi thật (sao lưu các câu ra scripts/logs/ trước)
//   thêm --thu 3  để chỉ làm 3 câu đầu
// Cần migration 20261011140000_bank_replace_question_imgs.sql đã chạy. Chạy trên Mac qua tab terminal.
import { createClient } from "@supabase/supabase-js";
import katex from "katex";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const ghi = args.includes("--ghi");
const thuIdx = args.indexOf("--thu");
const thu = thuIdx >= 0 ? Number(args[thuIdx + 1]) : Infinity;
const file = args.find((a) => a.endsWith(".json")) ?? path.join(os.homedir(), "Downloads", "duyet-cong-thuc.json");
function readEnvLocal(key: string): string | undefined {
  const p = path.resolve(scriptDir, "..", ".env.local");
  if (!fs.existsSync(p)) return undefined;
  const line = fs.readFileSync(p, "utf8").split("\n").find((l) => l.startsWith(`${key}=`));
  return line ? line.slice(key.length + 1).trim() : undefined;
}
type It = { id: number; i: number; src: string; loai: string; latex: string };
const items: It[] = JSON.parse(fs.readFileSync(file, "utf8")).filter((x: It) => x.loai === "cong_thuc" && x.latex.trim());

const bad: string[] = [];
const byQ = new Map<number, Map<string, string>>(); // id → src → text (cùng một ảnh chỉ một công thức: lấy cái đầu)
for (const x of items) {
  const lx = x.latex.trim();
  const plain = /^[.,;:!?]$/.test(lx); // dấu câu: chèn chữ thường, không bọc $
  if (!plain) {
    try { katex.renderToString(lx, { throwOnError: true }); } catch (e) { bad.push(`#${x.id}.${x.i} "${lx}" → ${(e as Error).message.slice(0, 80)}`); continue; }
    if (/[<>&]/.test(lx)) { bad.push(`#${x.id}.${x.i} "${lx}" có < > & (đổi \\lt \\gt)`); continue; }
  }
  const m = byQ.get(x.id) ?? new Map();
  if (!m.has(x.src)) m.set(x.src, plain ? lx : `$${lx}$`);
  byQ.set(x.id, m);
}
console.log(`${items.length} ảnh công thức → ${byQ.size} câu · LaTeX lỗi ${bad.length}`);
for (const b of bad) console.log("  LỖI " + b);
const ids = [...byQ.keys()].slice(0, thu);
for (const id of ids.slice(0, 8)) console.log(`  #${id}: ` + [...byQ.get(id)!.values()].join("  "));
if (!ghi) { console.log("DRY-RUN. Thêm --ghi để ghi thật."); process.exit(0); }

const url = process.env.NEXT_PUBLIC_SUPABASE_URL ?? readEnvLocal("NEXT_PUBLIC_SUPABASE_URL");
const key = process.env.SUPABASE_SERVICE_ROLE_KEY ?? readEnvLocal("SUPABASE_SERVICE_ROLE_KEY");
if (!url || !key) { console.error("thiếu NEXT_PUBLIC_SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY"); process.exit(1); }
const supabase = createClient(url, key, { auth: { autoRefreshToken: false, persistSession: false } });
const { data: rows, error: e0 } = await supabase.from("question_bank").select("id, content_hash, question").in("id", ids);
if (e0) { console.error("đọc ngân hàng lỗi: " + e0.message); process.exit(1); }
fs.mkdirSync(path.join(scriptDir, "logs"), { recursive: true });
const bak = path.join(scriptDir, "logs", `cong-thuc-sao-luu-${new Date().toISOString().replace(/[:.]/g, "-")}.json`);
fs.writeFileSync(bak, JSON.stringify(rows, null, 1));
console.log(`sao lưu ${rows?.length}/${ids.length} câu → ${path.relative(process.cwd(), bak)}`);
let ok = 0;
for (const id of ids) {
  const map = [...byQ.get(id)!].map(([src, text]) => ({ src, text }));
  const { data, error } = await supabase.rpc("bank_replace_question_imgs", { p_bank_id: id, p_map: map });
  if (error) console.error(`#${id}: LỖI ${error.message}`);
  else { ok++; console.log(`#${id}: ✓ ${map.length} ảnh · ${(data as { exams_updated: number }).exams_updated} đề`); }
}
console.log(`xong ${ok}/${ids.length}. Hoàn tác: khôi phục trường question từ file sao lưu.`);
