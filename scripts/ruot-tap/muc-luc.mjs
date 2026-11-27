// Trang MỤC LỤC cho quyển ruột tập theo học kì (dung-hoc-ki.sh gọi). 17/11/2026.
//   node scripts/ruot-tap/muc-luc.mjs <ruột.pdf> <mục-lục.pdf> "<tên quyển>"
// Đọc ruột đã ghép (PyMuPDF): mỗi trang mở bài có dòng 1 "BÀI N · TÊN", dòng 2 "Vật lí X · Chương k: …".
// Xuất 2 trang 165×240 không đánh số: tr. i = mục lục (mặt phải, gáy trái), tr. ii = để trống → trang 1 của ruột vẫn là mặt phải.
import { execFileSync } from 'node:child_process';
import { createRequire } from 'node:module';
import { existsSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { fonts } from './khung.mjs';
import { chuanHoa } from './ky-tu-in.mjs';

const [src, out, tenQuyen] = process.argv.slice(2);
const HERE = dirname(fileURLToPath(import.meta.url));
const BOOK = [resolve(HERE, '../../book/'), '/Users/MAC/Projects/thachlab/book'].find((d) => existsSync(d + '/node_modules')) + '/';
const puppeteer = createRequire(BOOK + 'package.json')('puppeteer-core');

const py = `
import fitz, json, re, sys
d = fitz.open(sys.argv[1]); r = []
for i, pg in enumerate(d):
    L = [s.strip() for s in pg.get_text().split('\\n') if s.strip()]
    if len(L) > 1 and re.match(r'(BÀI|Bài) \\d+( · |\\. )', L[0]) and L[1].startswith('Vật lí'):
        r.append({'p': i + 1, 'bai': L[0], 'ch': L[1]})
print(json.dumps({'n': len(d), 'r': r}, ensure_ascii=False))`;
const { n, r } = JSON.parse(execFileSync('/usr/bin/python3', ['-c', py, src], { encoding: 'utf8' }));
if (!r.length) throw new Error('không thấy trang mở bài nào trong ' + src);

const tenQ = tenQuyen || r[0].ch;   // quyển một chương: lấy "Vật lí X · Chương k: …" ở trang mở bài đầu
const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
const nhom = [];
for (const [i, e] of r.entries()) {
  const het = (r[i + 1]?.p ?? n + 1) - 1;
  const ch = e.ch.replace(/^Vật lí \d+ · /, '');
  if (nhom.at(-1)?.ch !== ch) nhom.push({ ch, p: e.p, bai: [] });
  // kiểu mộc (RUOT_TAP_KIEU=moc) in 'Bài 1. Sự chuyển thể' thay 'BÀI 1 · SỰ CHUYỂN THỂ'
  const [so, ...ten] = /^Bài \d+\. /.test(e.bai) ? [e.bai.match(/^Bài \d+/)[0], e.bai.replace(/^Bài \d+\. /, '')] : e.bai.split(' · ');
  nhom.at(-1).bai.push({ so: so.replace('BÀI', 'Bài'), ten: ten.join(' · '), p: e.p, het });
  nhom.at(-1).het = het;
}
const dong = nhom.map((g) => `<div class="ch"><span>${esc(g.ch)}</span><i></i><b>${g.p}–${g.het}</b></div>`
  + g.bai.map((b) => `<div class="bai"><span><em>${b.so}</em>${esc(b.ten)}</span><i></i><b>${b.p}</b></div>`).join('')).join('');

const html = `<!doctype html><html lang="vi"><head><meta charset="utf-8"><style>${fonts}
@page{size:165mm 240mm;margin:0}*{box-sizing:border-box}
body{margin:0;font-family:BV,sans-serif;color:#1c2540;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:165mm;height:240mm;padding:16mm 12mm 14mm 22mm;page-break-after:always;overflow:hidden}
h1{margin:0;font-size:7mm;color:#1d3a78;letter-spacing:.4mm}.q{font-size:4mm;color:#5f6a88;margin:1mm 0 6mm;border-bottom:.5mm solid #1d3a78;padding-bottom:2mm}
.ch,.bai{display:flex;align-items:baseline;gap:1.5mm;line-height:1.45}
.ch{margin:4mm 0 1.2mm;font-weight:700;font-size:3.9mm;color:#1d3a78}.ch:first-of-type{margin-top:0}
.bai{font-size:3.4mm;padding-left:4mm;margin:.3mm 0}.bai em{font-style:normal;font-weight:700;color:#1d3a78;display:inline-block;min-width:13mm}
.ch span,.bai span{flex:0 1 auto}.ch i,.bai i{flex:1 1 auto;border-bottom:.35mm dotted #8a94b0;min-width:6mm}.ch b,.bai b{flex:none;font-weight:700}
.note{margin-top:7mm;font-size:3mm;color:#5f6a88;line-height:1.5;border-top:.25mm solid #d3dbec;padding-top:2mm}
</style></head><body>
<section class="page"><h1>MỤC LỤC</h1><div class="q">${esc(tenQ)}</div>${dong}
<div class="note">Mỗi bài 12 trang: học bài mới · bài tập mẫu · bài tương tự · sửa bài · làm lại câu sai. Số trang ghi ở chân mỗi trang.</div></section>
<section class="page"></section>
</body></html>`;
writeFileSync(out + '.html', html);
const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true, args: ['--no-sandbox', '--allow-file-access-from-files'] });
const p = await b.newPage();
await p.goto(pathToFileURL(out + '.html').href, { waitUntil: 'networkidle0' });
await p.evaluate(chuanHoa);
await p.evaluate('document.fonts.ready');
const du = await p.evaluate(() => { const pg = document.querySelector('.page'); const last = pg.lastElementChild.getBoundingClientRect().bottom; return Math.round((pg.getBoundingClientRect().bottom - 14 * 3.7795 - last) / 3.7795); });
await p.pdf({ path: out, preferCSSPageSize: true, printBackground: true });
await b.close();
console.log(`  mục lục: ${nhom.length} chương, ${r.length} bài; dư ${du} mm${du < 0 ? ' ! TRÀN' : ''}`);
