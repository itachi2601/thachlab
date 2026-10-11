// Ghi bảng đã duyệt vào question_bank.question.question SAU KHI thầy duyệt trên scripts/data/bang-ngan-hang/duyet.html.
//   npx tsx scripts/ghi-bang-sau-duyet.mts            # dry-run: in việc sẽ làm
//   npx tsx scripts/ghi-bang-sau-duyet.mts --ghi      # ghi thật (sao lưu câu ra scripts/logs/ trước)
// Đọc quyet-dinh.json ({"<id>":{"quyet":"dung|sua|bo","bang":"hàng1\tô\tô\nhàng2…"}}). "dung"/"sua": thay cụm chữ dồn dòng bằng
// các dòng <br> có TAB (lib/question-table.ts dựng thành <table> lúc hiển thị). CHỈ ghi trường question.question của ngân hàng;
// bản sao trong exams.questions KHÔNG đổi (cần RPC riêng — xem báo cáo cuối phiên).
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const dir = path.dirname(fileURLToPath(import.meta.url));
const root = path.join(dir, "data", "bang-ngan-hang");
const ghi = process.argv.includes("--ghi");
const env = (k: string) => process.env[k] ?? fs.readFileSync(path.resolve(dir, "..", ".env.local"), "utf8").split("\n").find((l) => l.startsWith(`${k}=`))?.slice(k.length + 1).trim();
const fail = (m: string): never => { console.error(m); process.exit(1); };

const qdP = path.join(root, "quyet-dinh.json");
if (!fs.existsSync(qdP)) fail("Chưa có quyet-dinh.json (nút 'Xuất quyết định' trên duyet.html, dán vào file).");
const qd = JSON.parse(fs.readFileSync(qdP, "utf8")) as Record<string, { quyet: string; bang: string }>;
const cands = JSON.parse(fs.readFileSync(path.join(root, "ung-vien.json"), "utf8")) as { id: number; span: string }[];
const spanOf = new Map(cands.map((c) => [c.id, c.span]));
const todo = Object.entries(qd).filter(([, v]) => v.quyet === "dung" || v.quyet === "sua").map(([id, v]) => ({ id: Number(id), bang: v.bang }));
console.log(`dùng/sửa ${todo.length} · bỏ ${Object.keys(qd).length - todo.length}`);

const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL")!, env("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });
const { data: rows, error } = await sb.from("question_bank").select("id, question").in("id", todo.map((t) => t.id));
if (error) fail(error.message);
const plan: { id: number; q: any; next: string }[] = [];
for (const t of todo) {
  const row = rows!.find((r) => r.id === t.id);
  const span = spanOf.get(t.id);
  if (!row || !span) { console.error(`#${t.id}: không có trong ứng viên/ngân hàng — bỏ qua`); continue; }
  const raw: string = row.question.question ?? "";
  const lines = t.bang.split("\n").map((l) => l.trim()).filter(Boolean).map((l) => (l.includes("\t") ? l : l.split("|").map((x) => x.trim()).join("\t")));
  if (lines.length < 2 && !lines.some((l) => l.split("\t").length >= 3)) { console.error(`#${t.id}: bảng quá ngắn — bỏ qua`); continue; }
  if (!raw.includes(span)) { console.error(`#${t.id}: cụm chữ gốc không khớp nguyên văn (có thẻ HTML xen giữa?) — sửa tay`); continue; }
  plan.push({ id: t.id, q: row.question, next: raw.replace(span, "<br>" + lines.join("<br>") + "<br>") });
}
for (const p of plan) console.log(`#${p.id}: ${p.next.slice(0, 140).replace(/\t/g, " ⇥ ")}…`);
if (!ghi) { console.log(`DRY-RUN: sẽ ghi ${plan.length} câu. Thêm --ghi để ghi thật.`); process.exit(0); }
fs.mkdirSync(path.join(dir, "logs"), { recursive: true });
const bak = path.join(dir, "logs", `bang-sao-luu-${new Date().toISOString().replace(/[:.]/g, "-")}.json`);
fs.writeFileSync(bak, JSON.stringify(plan.map((p) => ({ id: p.id, question: p.q })), null, 1));
console.log(`đã sao lưu → ${path.relative(process.cwd(), bak)}`);
let ok = 0;
for (const p of plan) {
  const { error: e } = await sb.from("question_bank").update({ question: { ...p.q, question: p.next } }).eq("id", p.id);
  if (e) console.error(`#${p.id}: LỖI ${e.message}`); else ok++;
}
console.log(`xong ${ok}/${plan.length}.`);
