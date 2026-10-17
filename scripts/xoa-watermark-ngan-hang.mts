// Xoá dòng quảng cáo "Tài liệu ôn thi ... Website: thukhoadaihoc.vn" (chữ VNI vỡ: "Taøi lieäu ...") lẫn trong question_bank.
//   npx tsx scripts/xoa-watermark-ngan-hang.mts            # DRY-RUN: in mẫu + ghi báo cáo vào scripts/logs/
//   npx tsx scripts/xoa-watermark-ngan-hang.mts --apply    # ghi thật (sao lưu nguyên văn các câu đổi ra scripts/logs/ trước)
// Quét cả câu đã ẩn (archived). Sau khi sửa, chuỗi nào còn chứa "thukhoadaihoc" được liệt kê là "con-sot" để xử lý tay.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
function env(key: string): string | undefined {
  const line = fs.readFileSync(path.resolve(scriptDir, "..", ".env.local"), "utf8").split("\n").find((l) => l.startsWith(`${key}=`));
  return line ? line.slice(key.length + 1).trim() : undefined;
}
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL")!, env("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });
const APPLY = process.argv.includes("--apply");
// --ids=<file.json> : chỉ xử lý các id trong file (mảng số, lấy bằng scripts/sql/watermark-ids.sql) — nhanh hơn quét cả bảng
const IDS_FILE = process.argv.find((a) => a.startsWith("--ids="))?.slice(6);
const IDS: number[] | null = IDS_FILE ? JSON.parse(fs.readFileSync(IDS_FILE, "utf8")) : null;

// Khoảng trắng/xuống dòng/thẻ HTML có thể chen giữa từng ký tự (chép từ PDF) → cho phép "rác" giữa các chữ của tên miền.
const G = String.raw`(?:\s|<[^>]*>|&nbsp;)*`;
const DOMAIN = ["thukhoadaihoc", "vn"].map((w) => w.split("").join(G)).join(G + String.raw`\.` + G);
const WEBSITE = "Website".split("").join(G) + G + ":";
// Từ "T" của "Taøi" tới hết tên miền, tối đa 400 ký tự, không vượt qua "$" (không ăn vào công thức).
// Thường nằm gọn trong một cặp $…$ riêng sau <br> → xoá luôn cặp $ và <br> đứng trước, để không còn "$$".
const RE = new RegExp(String.raw`(?:<br\s*/?>\s*)?\$?\s*T${G}a${G}[øo][^$]{0,400}?${WEBSITE}${G}${DOMAIN}\s*\$?`, "g");
const RE_FALLBACK = new RegExp(`(?:${WEBSITE}${G})?${DOMAIN}`, "g"); // chỉ còn "Website: thukhoadaihoc.vn"
const SOT = new RegExp(DOMAIN, "i");

function clean(s: string): string {
  if (!/ø|website|thukhoa/i.test(s)) return s;
  let t = s.replace(RE, "").replace(RE_FALLBACK, "");
  // dọn dòng trống/khoảng trắng thừa để lại
  t = t.replace(/(<br\s*\/?>\s*){2,}/gi, "<br>").replace(/\n{3,}/g, "\n\n").replace(/[ \t]+\n/g, "\n");
  return t === s ? s : t.trim();
}
function mapStrings(v: any, f: (s: string) => string): any {
  if (typeof v === "string") return f(v);
  if (Array.isArray(v)) return v.map((x) => mapStrings(x, f));
  if (v && typeof v === "object") return Object.fromEntries(Object.entries(v).map(([k, x]) => [k, mapStrings(x, f)]));
  return v;
}
const strs = (v: any): string[] => (typeof v === "string" ? [v] : v && typeof v === "object" ? Object.values(v).flatMap(strs) : []);

const report: any[] = [], backup: any[] = [], conSot: any[] = [];
let lastId = 0, scanned = 0, shown = 0;
for (;;) {
  const q = sb.from("question_bank").select("id, question, archived").gt("id", lastId).order("id").limit(300);
  const { data, error } = IDS ? await q.in("id", IDS.filter((i) => i > lastId).slice(0, 300)) : await q;
  if (error) { console.error(error.message); process.exit(1); }
  if (!data?.length || (IDS && !IDS.some((i) => i > lastId))) break;
  const toWrite: { id: number; nq: any }[] = [];
  for (const r of data) {
    scanned++;
    const nq = mapStrings(r.question, clean);
    const before = JSON.stringify(r.question), after = JSON.stringify(nq);
    if (before !== after) {
      backup.push({ id: r.id, question: r.question });
      toWrite.push({ id: r.id, nq });
      const i = before.search(/T(?:\\n|\s)*a(?:\\n|\s)*[øo]/);
      report.push({ id: r.id, archived: r.archived, mau: before.slice(Math.max(0, i - 40), i + 200) });
      if (shown++ < 8) console.log(`#${r.id}\n  TRƯỚC: ${before.slice(Math.max(0, i - 60), i + 160)}\n  SAU  : ${after.slice(Math.max(0, i - 60), i + 60)}\n`);
    }
    if (strs(nq).some((s) => /vn/.test(s) && SOT.test(s))) conSot.push({ id: r.id, mau: strs(nq).find((s) => SOT.test(s))!.slice(0, 300) });
  }
  if (APPLY && toWrite.length) {
    fs.writeFileSync(path.join(scriptDir, "logs", `backup-watermark-${runId()}.json`), JSON.stringify(backup));
    for (const w of toWrite) {
      const { error: e2 } = await sb.from("question_bank").update({ question: w.nq }).eq("id", w.id);
      if (e2) { console.error("LỖI id", w.id, e2.message); process.exit(1); }
    }
  }
  lastId = data[data.length - 1].id;
}
function runId() { return (globalThis as any).__rid ??= Date.now(); }
const out = path.join(scriptDir, "logs", `xoa-watermark-${APPLY ? "apply" : "dry"}-${Date.now()}.json`);
fs.writeFileSync(out, JSON.stringify({ report, conSot }, null, 2));
console.log(APPLY ? "ĐÃ GHI" : "DRY-RUN", `· quét ${scanned} · câu đổi ${backup.length} · còn sót ${conSot.length} →`, path.relative(process.cwd(), out));
for (const c of conSot.slice(0, 5)) console.log("  SÓT #" + c.id, JSON.stringify(c.mau));
