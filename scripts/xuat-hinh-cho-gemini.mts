// Xuất thư mục thí điểm cho Gemini Spark đọc ảnh đồ thị xấu — CHỈ ĐỌC DB, ghi file cục bộ.
// Đầu vào: scripts/data/kiem-ke-anh-ngan-hang/rows.json (từ kiem-ke-anh-ngan-hang.mts).
//   npx tsx scripts/xuat-hinh-cho-gemini.mts [--n 20] [--loai do_thi] [--ids 1,2,3]
// Kết quả: scripts/data/gemini-hinh/cau/<id>/{anh-1.png, de-bai.md} + danh-sach.md
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
function readEnvLocal(key: string): string | undefined {
  const p = path.resolve(scriptDir, "..", ".env.local");
  if (!fs.existsSync(p)) return undefined;
  const line = fs.readFileSync(p, "utf8").split("\n").find((l) => l.startsWith(`${key}=`));
  return line ? line.slice(key.length + 1).trim() : undefined;
}
const url = process.env.NEXT_PUBLIC_SUPABASE_URL ?? readEnvLocal("NEXT_PUBLIC_SUPABASE_URL");
const key = process.env.SUPABASE_SERVICE_ROLE_KEY ?? readEnvLocal("SUPABASE_SERVICE_ROLE_KEY");
if (!url || !key) { console.error("thiếu NEXT_PUBLIC_SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY"); process.exit(1); }
const supabase = createClient(url, key, { auth: { autoRefreshToken: false, persistSession: false } });

const arg = (name: string, def: string) => { const i = process.argv.indexOf(name); return i > 0 ? process.argv[i + 1] : def; };
const N = Number(arg("--n", "20"));
const LOAI = arg("--loai", "do_thi");
const IDS = arg("--ids", "").split(",").map(Number).filter(Boolean);

type Row = { id: number; grade: string | null; topic: string | null; loai: string; srcs: string[]; muc: string;
  anh?: { src: string; w: number | null; h: number | null; bytes: number | null }[] };
const rows: Row[] = JSON.parse(fs.readFileSync(path.join(scriptDir, "data", "kiem-ke-anh-ngan-hang", "rows.json"), "utf8"));
const rank: Record<string, number> = { rat_xau: 0, xau: 1, mo: 2, "nho_<8KB": 3, ok: 4 };
let pick = IDS.length
  ? rows.filter((r) => IDS.includes(r.id))
  : rows.filter((r) => r.loai === LOAI && r.srcs.every((s) => s.startsWith("http"))
        && !(r.anh ?? []).some((a) => (a.w ?? 99) < 40 || (a.h ?? 99) < 30)) // bỏ câu có ảnh công thức (glyph nhỏ)
      .sort((a, b) => (rank[a.muc] ?? 9) - (rank[b.muc] ?? 9) || (a.anh?.[0]?.w ?? 0) - (b.anh?.[0]?.w ?? 0))
      .slice(0, N);
if (!pick.length) { console.error("không có câu nào để xuất"); process.exit(1); }

const { data, error } = await supabase.from("question_bank").select("id, grade, topic_name, question").in("id", pick.map((r) => r.id));
if (error) { console.error(error.message); process.exit(1); }

const strip = (s: string) => s.replace(/<img[^>]*>/gi, "[ẢNH]").replace(/<br\s*\/?>/gi, "\n").replace(/<[^>]+>/g, "").replace(/&nbsp;/g, " ").trim();
const outRoot = path.join(scriptDir, "data", "gemini-hinh");
const cauDir = path.join(outRoot, "cau");
fs.mkdirSync(path.join(outRoot, "out"), { recursive: true });
const list: string[] = [];
for (const r of data ?? []) {
  const q = r.question as Record<string, unknown>;
  const dir = path.join(cauDir, String(r.id));
  fs.mkdirSync(dir, { recursive: true });
  const meta = pick.find((p) => p.id === r.id)!;
  let i = 0;
  for (const src of meta.srcs) {
    i++;
    try {
      const res = await fetch(src);
      const ext = (res.headers.get("content-type") ?? "image/png").split("/")[1].replace("jpeg", "jpg");
      fs.writeFileSync(path.join(dir, `anh-${i}.${ext}`), Buffer.from(await res.arrayBuffer()));
    } catch (e) { console.error(`#${r.id} ảnh ${i}: ${(e as Error).message}`); }
  }
  let md = `# Câu #${r.id} — Lớp ${r.grade ?? "?"} — ${r.topic_name ?? ""}\n\n## Đề bài\n\n${strip(String(q.question ?? ""))}\n`;
  if (Array.isArray(q.options)) md += `\n## Phương án\n\n${(q.options as string[]).map((o, k) => `${"ABCD"[k]}. ${strip(o)}`).join("\n")}\n`;
  if (Array.isArray(q.statements)) md += `\n## Mệnh đề\n\n${(q.statements as { text?: string }[]).map((s, k) => `${"abcd"[k]}) ${strip(s.text ?? "")}`).join("\n")}\n`;
  if (typeof q.explanation === "string" && q.explanation) md += `\n## Lời giải (tham khảo số liệu)\n\n${strip(q.explanation)}\n`;
  fs.writeFileSync(path.join(dir, "de-bai.md"), md);
  list.push(`- ${r.id} · L${r.grade} · ${r.topic_name ?? ""} · ${meta.muc} · ${meta.anh?.map((a) => `${a.w}×${a.h}`).join(", ")}`);
}
fs.writeFileSync(path.join(outRoot, "danh-sach.md"), `# Câu đã xuất (${list.length})\n\n${list.join("\n")}\n`);
console.log(`Đã xuất ${list.length} câu → ${path.relative(process.cwd(), cauDir)}/\nĐưa cho Gemini: đọc PROMPT.md + schema.json, ghi out/<id>.json`);
