// Kiểm máy bản chiếu "trên lớp" (skill ban-chieu-tren-lop bước 5) — chạy trên bản web public/dev/tren-lop/<slug>.html
// (phục vụ public/ qua http để nạp font tự host). Dùng: node scripts/tren-lop/kiem.mjs <slug> [--anh <thư mục>]
// In: màn tràn (mở hết .an, từng .buoc của clip) ở 1280×720 và 1920×1080; hình: cao (% màn) + chữ nhỏ nhất trong hình / chữ thường
// khi đáp án mở; .katex-error; còn "$" chưa dựng; 375px cuộn ngang. --anh: chụp từng màn 1280×720 (đáp án mở) vào thư mục.
import { createRequire } from 'node:module';
import { createServer } from 'node:http';
import { existsSync, readFileSync, mkdirSync } from 'node:fs';
import { resolve, dirname, extname } from 'node:path';
import { fileURLToPath } from 'node:url';
const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(HERE, '../..');
const BOOK = [resolve(ROOT, 'book'), '/Users/MAC/Projects/thachlab/book'].find((d) => existsSync(d + '/node_modules/puppeteer-core'));
const puppeteer = createRequire(BOOK + '/package.json')('puppeteer-core');
const slug = process.argv[2];
const anhDir = process.argv.includes('--anh') ? process.argv[process.argv.indexOf('--anh') + 1] : null;
const PUB = resolve(ROOT, 'public');
if (!existsSync(`${PUB}/dev/tren-lop/${slug}.html`)) { console.error('chưa build', slug); process.exit(1); }
const MIME = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.woff2': 'font/woff2', '.js': 'text/javascript', '.svg': 'image/svg+xml' };
const srv = createServer((q, r) => {
  const p = resolve(PUB, '.' + decodeURIComponent(q.url.split('?')[0]));
  if (!p.startsWith(PUB) || !existsSync(p)) { r.writeHead(404); r.end(); return; }
  r.writeHead(200, { 'content-type': MIME[extname(p)] ?? 'application/octet-stream' }); r.end(readFileSync(p));
}).listen(0);
const url = `http://127.0.0.1:${srv.address().port}/dev/tren-lop/${slug}.html`;
const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true });
const pg = await b.newPage();
const mo = () => pg.evaluate(() => {
  document.querySelectorAll('.an').forEach((e) => { e.hidden = false; });
  document.querySelectorAll('.an-o').forEach((e) => { e.style.visibility = 'visible'; });
});
const do_ = () => pg.evaluate(() => {
  const out = [];
  const body = parseFloat(getComputedStyle(document.body).fontSize);
  const tran = (s) => s.scrollHeight - s.clientHeight;
  document.querySelectorAll('.man').forEach((s) => {
    const vg = s.querySelector('.vg');
    let t = 0;
    if (vg) { const bs = [...vg.querySelectorAll('.buoc')]; bs.forEach((x) => { bs.forEach((y) => y.classList.toggle('hien', y === x)); t = Math.max(t, tran(s)); }); bs.forEach((y, i) => y.classList.toggle('hien', i === 0)); }
    else t = tran(s);
    const figs = [...s.querySelectorAll('.fig svg')].map((g) => {
      const vb = g.viewBox.baseVal, k = vb && vb.height ? g.getBoundingClientRect().height / vb.height : 1;
      const fs = [...g.querySelectorAll('text')].map((x) => parseFloat(getComputedStyle(x).fontSize) * k).filter((x) => x > 0);
      return { cao: Math.round(g.getBoundingClientRect().height / innerHeight * 100), chu: fs.length ? +(Math.min(...fs) / body).toFixed(2) : null };
    });
    out.push({ id: s.id, tran: t, figs });
  });
  const txt = document.body.innerText;
  return { out, katexErr: document.querySelectorAll('.katex-error').length, dola: (txt.match(/\$/g) || []).length, so: out.length };
});
for (const [w, h] of [[1280, 720], [1920, 1080]]) {
  await pg.setViewport({ width: w, height: h });
  await pg.goto(url, { waitUntil: 'networkidle0' });
  await pg.evaluate('document.fonts.ready');
  await mo();
  const r = await do_();
  const tran = r.out.filter((x) => x.tran > 1).map((x) => `${x.id}(+${x.tran}px)`);
  console.log(`${w}×${h}: ${r.so} màn · tràn: ${tran.join(' ') || 'không'} · katex-error ${r.katexErr} · "$" còn ${r.dola}`);
  if (w === 1280) {
    const f = r.out.filter((x) => x.figs.length).map((x) => `${x.id}: ` + x.figs.map((g) => `cao ${g.cao}% chữ ${g.chu ?? '—'}`).join(' | '));
    console.log('  hình (đáp án mở): ' + (f.join(' · ') || 'không có'));
    const nho = r.out.flatMap((x) => x.figs.filter((g) => g.chu !== null && g.chu < 0.7).map(() => x.id));
    if (nho.length) console.log('  ⚠ chữ hình < 0,7 chữ thường: ' + [...new Set(nho)].join(' '));
    if (anhDir) {
      mkdirSync(anhDir, { recursive: true });
      const ids = r.out.map((x) => x.id);
      for (const id of ids) { await pg.evaluate((i) => document.getElementById(i).scrollIntoView(), id); await new Promise((z) => setTimeout(z, 150)); await pg.screenshot({ path: `${anhDir}/${id}.png` }); }
      console.log('  ảnh:', anhDir);
    }
  }
}
await pg.setViewport({ width: 375, height: 812 });
await pg.goto(url, { waitUntil: 'networkidle0' });
await mo();
const sw = await pg.evaluate(() => document.documentElement.scrollWidth);
console.log(`375px: scrollWidth ${sw}${sw > 375 ? ' ⚠ cuộn ngang' : ' (không cuộn ngang)'}`);
await b.close(); srv.close();
