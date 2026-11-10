// Chụp từng hình trong hinh.mjs ở đúng cỡ in (mặc định rộng 46 mm, phóng 4×) để kiểm cỡ chữ/nét trước khi dựng cả tập.
// Chạy: node scripts/ruot-tap/xem-hinh.mjs [rộng_mm] → scripts/ruot-tap/out/hinh/<tên>.png
import { createRequire } from 'node:module';
import { existsSync, mkdirSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { hinh as hinh14 } from './hinh.mjs';
import { hinhCh4 } from './hinh-ch4.mjs';
const hinh = { ...hinh14, ...hinhCh4 };
const HERE = dirname(fileURLToPath(import.meta.url));
const BOOK = [resolve(HERE, '../../book/'), '/Users/MAC/Projects/thachlab/book'].find((d) => existsSync(d + '/node_modules')) + '/';
const puppeteer = createRequire(BOOK + 'package.json')('puppeteer-core');
const W = Number(process.argv[2] ?? 46);
const F = resolve(HERE, 'fonts') + '/noto-sans-';
const css = ['latin', 'latin-ext', 'vietnamese'].map((s) => `@font-face{font-family:BV;src:url("${pathToFileURL(F + s + '-400-normal.woff2').href}")}`).join('')
  + ['latin', 'latin-ext', 'vietnamese'].map((s) => `@font-face{font-family:BV;font-weight:700;src:url("${pathToFileURL(F + s + '-700-normal.woff2').href}")}`).join('')
  + `body{margin:0;font-family:BV,sans-serif;zoom:4}.fig{margin:0;width:${W}mm;border:.3mm solid #d3dbec;border-radius:1.5mm;padding:1mm 1.5mm .6mm;background:#fff}.fig svg{display:block;width:100%;height:auto}figcaption{font-size:3.1mm;color:#5f6a88;line-height:1.3;margin-top:.4mm}`;
const out = resolve(HERE, 'out/hinh'); mkdirSync(out, { recursive: true });
const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true, args: ['--no-sandbox', '--allow-file-access-from-files'] });
const pg = await b.newPage();
for (const [name, fn] of Object.entries(hinh)) {
  if (name === 'anh') continue; // ảnh raster cần tên tệp, kiểm bằng mắt khi chèn
  const html = `<!doctype html><html><head><meta charset="utf-8"><style>${css}</style></head><body>${fn()}</body></html>`;
  writeFileSync(out + '/_tmp.html', html);
  await pg.goto(pathToFileURL(out + '/_tmp.html').href, { waitUntil: 'networkidle0' });
  await pg.evaluate('document.fonts.ready');
  const el = await pg.$('.fig');
  await el.screenshot({ path: `${out}/${name}.png` });
  console.log(`${name}.png`);
}
await b.close();
