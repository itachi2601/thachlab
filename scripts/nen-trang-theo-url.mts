// Làm nền trắng các ảnh (theo URL Storage lesson-media) mà thầy ghi "làm trắng nền" khi kiểm mắt, ghi đè tại chỗ.
//   npx tsx scripts/nen-trang-theo-url.mts ghi-chu-anh.json duyet-cong-thuc.json        # tải + làm + trang xem thử (KHÔNG ghi)
//   npx tsx scripts/nen-trang-theo-url.mts ghi-chu-anh.json duyet-cong-thuc.json --ghi  # ghi đè Storage (ảnh gốc lưu ở goc/)
//   thêm --khoi-phuc để trả ảnh gốc.  Kết quả: scripts/data/gemini-hinh/nen-trang-url/
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { lamTrangNen } from "./lib-nen-trang";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const out = path.join(scriptDir, "data", "gemini-hinh", "nen-trang-url");
const goc = path.join(out, "goc");
fs.mkdirSync(goc, { recursive: true });
const args = process.argv.slice(2);
const ghi = args.includes("--ghi");
const khoiPhuc = args.includes("--khoi-phuc");
const files = args.filter((a) => a.endsWith(".json")).map((f) => (fs.existsSync(f) ? f : path.join(os.homedir(), "Downloads", f)));
const srcs = new Set<string>();
for (const f of files) for (const x of JSON.parse(fs.readFileSync(f, "utf8")) as { src: string; ghi_chu?: string; latex?: string; loai?: string }[])
  if (/trắng/i.test(x.ghi_chu ?? "") || (x.loai === "hinh" && /trắng/i.test(x.latex ?? ""))) srcs.add(x.src);
const name = (s: string) => s.split("/lesson-media/")[1].replace(/\//g, "_");
console.log(`${srcs.size} ảnh cần nền trắng`);
const rows: string[] = [];
const jobs: { storagePath: string; file: string }[] = [];
for (const s of srcs) {
  const n = name(s);
  const g = path.join(goc, n);
  if (!fs.existsSync(g)) fs.writeFileSync(g, Buffer.from(await (await fetch(s)).arrayBuffer()));
  const { png, bg } = await lamTrangNen(g);
  const o = path.join(out, n.replace(/\.\w+$/, ".png"));
  fs.writeFileSync(o, png);
  jobs.push({ storagePath: s.split("/lesson-media/")[1], file: khoiPhuc ? g : o });
  rows.push(`<tr><td>${n}<br><small>nền ${bg}</small></td><td><img src="goc/${n}" height="110"></td><td><img src="${path.basename(o)}" height="110"></td></tr>`);
}
fs.writeFileSync(path.join(out, "xem-thu.html"), `<!doctype html><meta charset="utf-8"><title>Nền trắng (URL)</title><body style="font-family:system-ui"><table border="1" cellpadding="6">${rows.join("")}</table>`);
console.log(`→ ${path.relative(process.cwd(), path.join(out, "xem-thu.html"))}`);
if (!ghi) { console.log("DRY-RUN. Thêm --ghi để ghi đè lên Storage."); process.exit(0); }
const readEnv = (k: string) => process.env[k] ?? fs.readFileSync(path.resolve(scriptDir, "..", ".env.local"), "utf8").split("\n").find((l) => l.startsWith(`${k}=`))?.slice(k.length + 1).trim();
const supabase = createClient(readEnv("NEXT_PUBLIC_SUPABASE_URL")!, readEnv("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });
let ok = 0;
for (const j of jobs) {
  const ext = j.file.toLowerCase();
  const { error } = await supabase.storage.from("lesson-media").upload(j.storagePath, fs.readFileSync(j.file), { upsert: true, contentType: ext.endsWith(".png") ? "image/png" : "image/jpeg", cacheControl: "300" });
  if (error) console.error(`${j.storagePath}: LỖI ${error.message}`); else { ok++; console.log(`✓ ${j.storagePath}`); }
}
console.log(`xong ${ok}/${jobs.length}`);
