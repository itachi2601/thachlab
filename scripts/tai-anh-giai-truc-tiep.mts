// Tải ảnh trong các lô truc-tiep-anh về scripts/data/giai-lai/truc-tiep-anh/img/ và thêm trường "anh" (đường dẫn local, theo thứ tự xuất hiện) vào từng câu của lô.
import fs from "node:fs";
import crypto from "node:crypto";
const DIR = "scripts/data/giai-lai/truc-tiep-anh/", IMG = DIR + "img/";
fs.mkdirSync(IMG, { recursive: true });
const cache = new Map<string, string>(); let loi = 0;
async function tai(url: string): Promise<string | null> {
  if (cache.has(url)) return cache.get(url)!;
  const ext = (url.match(/\.(png|jpe?g|webp|gif)(\?|$)/i)?.[1] ?? "jpg").toLowerCase();
  const f = IMG + crypto.createHash("md5").update(url).digest("hex").slice(0, 12) + "." + ext;
  if (!fs.existsSync(f)) {
    for (let t = 0; t < 3; t++) { try { const r = await fetch(url); if (r.ok) { fs.writeFileSync(f, Buffer.from(await r.arrayBuffer())); break; } } catch {} if (t === 2) { loi++; return null; } }
  }
  cache.set(url, f); return f;
}
for (const lo of fs.readdirSync(DIR).filter((f) => /^lo-\d+\.json$/.test(f))) {
  const rows: any[] = JSON.parse(fs.readFileSync(DIR + lo, "utf8"));
  for (const r of rows) {
    const urls = [...JSON.stringify(r).matchAll(/<img[^>]*?src=\\"([^"\\]+)\\"/g)].map((m) => m[1]);
    r.anh = (await Promise.all(urls.map(tai))).filter(Boolean).map((p) => "/Users/MAC/Projects/thachlab/" + p);
    r.co_svg = /<svg/.test(JSON.stringify(r)) || undefined;
  }
  fs.writeFileSync(DIR + lo, JSON.stringify(rows));
}
console.log("ảnh:", cache.size, "lỗi:", loi);
