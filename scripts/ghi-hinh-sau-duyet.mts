// Ghi hình SVG (Gemini đọc thông số → code vẽ) vào câu ngân hàng SAU KHI thầy duyệt trên so-sanh.html.
//   npx tsx scripts/ghi-hinh-sau-duyet.mts            # dry-run: chỉ in việc sẽ làm
//   npx tsx scripts/ghi-hinh-sau-duyet.mts --ghi      # ghi thật (sao lưu câu ra scripts/logs/ trước)
// Đọc scripts/data/gemini-hinh/quyet-dinh.json ({"<id>":"dung|sua|bo", "_ghi_chu":{"<id>":"..."}}) và svg/<id>.svg.
//  - "dung": sao lưu question_bank.question, gọi RPC bank_set_question_figure_svc (cần migration
//    20261011130000; RPC tự chèn vào mọi exams.questions dùng câu đó và xoá ai_figure).
//  - "sua":  gom ghi chú của thầy vào scripts/data/gemini-hinh/can-ve-lai.md để xuất lại cho Gemini.
//  - "bo":   không làm gì.
// Chạy trên Mac qua tab terminal (cần SUPABASE_SERVICE_ROLE_KEY trong env/.env.local).
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const root = path.join(scriptDir, "data", "gemini-hinh");
const ghi = process.argv.includes("--ghi");
function readEnvLocal(key: string): string | undefined {
  const p = path.resolve(scriptDir, "..", ".env.local");
  if (!fs.existsSync(p)) return undefined;
  const line = fs.readFileSync(p, "utf8").split("\n").find((l) => l.startsWith(`${key}=`));
  return line ? line.slice(key.length + 1).trim() : undefined;
}
const fail = (m: string): never => { console.error(m); process.exit(1); };

const qdPath = path.join(root, "quyet-dinh.json");
if (!fs.existsSync(qdPath)) fail("Chưa có quyet-dinh.json (nút 'Xuất quyết định' trên so-sanh.html, dán vào file).");
const qd = JSON.parse(fs.readFileSync(qdPath, "utf8")) as Record<string, unknown>;
const notes = (qd._ghi_chu ?? {}) as Record<string, string>;
const entries = Object.entries(qd).filter(([k]) => /^\d+$/.test(k)) as [string, string][];
const dung = entries.filter(([, v]) => v === "dung").map(([k]) => Number(k));
const sua = entries.filter(([, v]) => v === "sua").map(([k]) => Number(k));
console.log(`dùng ${dung.length} · vẽ lại ${sua.length} · bỏ ${entries.length - dung.length - sua.length}`);

if (sua.length) {
  const md = `# Câu cần Gemini vẽ lại — ${new Date().toISOString().slice(0, 10)}\n\n` +
    sua.map((id) => `- #${id}: ${notes[String(id)] ?? "(thầy không ghi chú)"}`).join("\n") + "\n";
  fs.writeFileSync(path.join(root, "can-ve-lai.md"), md);
  console.log(`→ can-ve-lai.md (${sua.length} câu): gắn vào prompt lượt sau, xoá out/<id>.json cũ trước khi Gemini chạy lại`);
}

const svgs = new Map<number, string>();
for (const id of dung) {
  const p = path.join(root, "svg", `${id}.svg`);
  if (!fs.existsSync(p)) { console.error(`#${id}: thiếu svg/${id}.svg — bỏ qua`); continue; }
  const s = fs.readFileSync(p, "utf8").trim();
  if (!/^<svg[\s>]/i.test(s)) { console.error(`#${id}: file không bắt đầu bằng <svg — bỏ qua`); continue; }
  svgs.set(id, s);
}
if (!ghi) { console.log(`DRY-RUN: sẽ ghi ${svgs.size} câu: ${[...svgs.keys()].join(", ")}. Thêm --ghi để ghi thật.`); process.exit(0); }
if (!svgs.size) process.exit(0);

const url = process.env.NEXT_PUBLIC_SUPABASE_URL ?? readEnvLocal("NEXT_PUBLIC_SUPABASE_URL");
const key = process.env.SUPABASE_SERVICE_ROLE_KEY ?? readEnvLocal("SUPABASE_SERVICE_ROLE_KEY");
if (!url || !key) fail("thiếu NEXT_PUBLIC_SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY");
const supabase = createClient(url!, key!, { auth: { autoRefreshToken: false, persistSession: false } });

// Sao lưu TRƯỚC khi ghi (chỉ các câu sắp ghi, lọc server theo id).
const { data: rows, error: e0 } = await supabase.from("question_bank").select("id, content_hash, question, ai_figure").in("id", [...svgs.keys()]);
if (e0) fail(`đọc ngân hàng lỗi: ${e0.message}`);
const logDir = path.join(scriptDir, "logs");
fs.mkdirSync(logDir, { recursive: true });
const bak = path.join(logDir, `hinh-gemini-sao-luu-${new Date().toISOString().replace(/[:.]/g, "-")}.json`);
fs.writeFileSync(bak, JSON.stringify(rows, null, 1));
console.log(`đã sao lưu ${rows?.length} câu → ${path.relative(process.cwd(), bak)}`);

let ok = 0;
for (const [id, svg] of svgs) {
  const { error } = await supabase.rpc("bank_set_question_figure_svc", { p_bank_id: id, p_img_html: svg });
  if (error) { console.error(`#${id}: LỖI ${error.message}`); continue; }
  ok++; console.log(`#${id}: đã ghi`);
}
console.log(`xong ${ok}/${svgs.size}. Hoàn tác: khôi phục trường question từ file sao lưu (bank) — bản trong exams.questions đổi theo RPC, cần đặt lại cùng cách.`);
