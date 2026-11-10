// Đo chỗ viết của Bài tương tự (khối .tt) trong ruột tập: số ý, số ô đáp số, số dòng kẻ và độ rộng dòng.
// Chạy sau khi dựng: node scripts/ruot-tap/do-cho-viet.mjs out/ruot-tap-vl10-bai23.pdf.html [file khác…]
// Quy đổi "dòng-130/ý" = (tổng chiều dài dòng kẻ / 130 mm) / số ý. Giải trên giấy cần ≥ 2; dưới mức đó thì cho giải vào vở (tuongTu.vo + o:[…]).
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';
import { resolve } from 'node:path';
// puppeteer-core nằm ở book/node_modules (worktree có thể chỉ symlink về checkout chính)
let puppeteer;
try { puppeteer = createRequire(new URL('../../book/package.json', import.meta.url))('puppeteer-core'); }
catch { puppeteer = createRequire('/Users/MAC/Projects/thachlab/book/package.json')('puppeteer-core'); }
const files = process.argv.slice(2);
if (!files.length) { console.error('Cần ít nhất một file .pdf.html'); process.exit(1); }
const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true, args: ['--no-sandbox', '--allow-file-access-from-files'] });
for (const f of files) {
  const p = await b.newPage();
  await p.goto(pathToFileURL(resolve(f)).href, { waitUntil: 'networkidle0' });
  const rows = await p.evaluate(() => {
    const mm = 96 / 25.4;
    return [...document.querySelectorAll('.tt')].map((t) => {
      const parts = (t.innerText.match(/(^|\n)\s*[a-e]\)/g) || []).length || 1;
      const len = [...t.querySelectorAll('.ln')].reduce((s, e) => s + e.getBoundingClientRect().width / mm, 0);
      const o = t.querySelectorAll('.dso .fill').length;
      return [t.querySelector('.hd span')?.innerText.slice(0, 18) || '?', parts, o, +(len / 130 / parts).toFixed(1)];
    });
  });
  console.log('== ' + f);
  rows.forEach(([t, y, o, d]) => console.log(`${t.padEnd(19)} ý ${y} · ô đáp số ${o} · dòng-130/ý ${d}${!o && d < 2 ? '  ← thiếu chỗ viết' : ''}`));
  await p.close();
}
await b.close();
