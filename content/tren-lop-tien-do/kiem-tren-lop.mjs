// Bước 5 skill ban-chieu-tren-lop: kiểm máy một bản chiếu.
// node content/tren-lop-tien-do/kiem-tren-lop.mjs <slug> [--chup]
// Phục vụ worktree qua http (đường /fonts → public/fonts), mở content/lesson-samples/<slug>/tren-lop.html.
// 1280×720 + 1920×1080: mở hết .an[hidden], .an-o, từng .buoc của clip → báo màn tràn; đo hình (cao % màn, chữ nhỏ nhất / chữ thường);
// .katex-error; 375px cuộn ngang. --chup: chụp mỗi màn 1280×720 (đáp án mở) vào content/lesson-samples/<slug>/thu-lop-ao/chup/ (không commit).
import { createRequire } from 'node:module';
import http from 'node:http';
import { readFileSync, existsSync, mkdirSync, statSync } from 'node:fs';
import { join, extname } from 'node:path';
const ROOT = process.cwd(); // chạy từ gốc repo/worktree
const slug = process.argv[2]; const chup = process.argv.includes('--chup');
const puppeteer = createRequire('/Users/MAC/Projects/thachlab/book/package.json')('puppeteer-core');
const MIME = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.woff2': 'font/woff2', '.svg': 'image/svg+xml', '.webp': 'image/webp', '.js': 'text/javascript' };
const srv = http.createServer((q, r) => {
  const p = decodeURIComponent(q.url.split('?')[0]);
  for (const f of [join(ROOT, p), join(ROOT, 'public', p)]) if (existsSync(f) && statSync(f).isFile()) { r.writeHead(200, { 'content-type': MIME[extname(f)] || 'application/octet-stream' }); return r.end(readFileSync(f)); }
  r.writeHead(404); r.end();
}).listen(0);
const url = `http://127.0.0.1:${srv.address().port}/content/lesson-samples/${slug}/tren-lop.html`;
const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true });
const pg = await b.newPage();
let loi = 0;
for (const [w, h] of [[1280, 720], [1920, 1080]]) {
  await pg.setViewport({ width: w, height: h });
  await pg.goto(url, { waitUntil: 'networkidle0' });
  await pg.evaluate('document.fonts.ready');
  await new Promise((r) => setTimeout(r, 400));
  const kq = await pg.evaluate(() => {
    document.documentElement.style.scrollBehavior = 'auto';
    document.querySelectorAll('.an[hidden]').forEach((a) => (a.hidden = false));
    document.querySelectorAll('.an-o').forEach((s) => (s.style.visibility = 'visible'));
    document.querySelectorAll('ol.opt li[data-dung]').forEach((li) => li.classList.add('dung'));
    const body = parseFloat(getComputedStyle(document.body).fontSize), vh = innerHeight, out = [];
    const tran = (m) => m.scrollHeight - m.clientHeight;
    for (const m of document.querySelectorAll('.man')) {
      let t = tran(m), ghi = '';
      const bs = [...m.querySelectorAll('.buoc')];
      for (const x of bs) { bs.forEach((y) => y.classList.toggle('hien', y === x)); const tx = tran(m); if (tx > t) { t = tx; ghi = ' (bước t=' + x.dataset.t + ')'; } }
      const figs = [...m.querySelectorAll('.fig svg, .qr svg')].map((s) => {
        const r = s.getBoundingClientRect(), vb = s.viewBox.baseVal, k = vb && vb.width ? r.width / vb.width : 1;
        let mn = 1e9; s.querySelectorAll('text').forEach((tx) => { const fs = parseFloat(getComputedStyle(tx).fontSize) * k; if (fs < mn) mn = fs; });
        return { cao: Math.round((r.height / vh) * 100), chu: mn < 1e9 ? +(mn / body).toFixed(2) : null };
      });
      // chữ thường bị co (phần tử chữ nhỏ hơn 0,6 chữ thường, ngoài .top/.nho/.tap)
      out.push({ id: m.id, tran: t > 1 ? t + ghi : 0, figs });
    }
    return { body, out, katex: document.querySelectorAll('.katex-error').length, nMan: document.querySelectorAll('.man').length };
  });
  console.log(`== ${w}×${h} · chữ thường ${kq.body}px · ${kq.nMan} màn · katex-error ${kq.katex}`);
  loi += kq.katex;
  for (const m of kq.out) {
    const f = m.figs.map((x) => `hình cao ${x.cao}% chữ ${x.chu ?? '-'}`).join('; ');
    const xau = m.tran || m.figs.some((x) => x.chu !== null && x.chu < 0.7);
    if (xau) loi++;
    console.log(`${xau ? '✗' : ' '} ${m.id.padEnd(8)} ${m.tran ? 'TRÀN ' + m.tran + 'px ' : ''}${f}`);
  }
  if (chup && w === 1280) {
    const dir = join(ROOT, 'content/lesson-samples', slug, 'thu-lop-ao/chup'); mkdirSync(dir, { recursive: true });
    const ids = kq.out.map((m) => m.id);
    for (const id of ids) {
      await pg.evaluate((id) => { const m = document.getElementById(id); window.scrollTo(0, m.offsetTop); const bs = [...m.querySelectorAll('.buoc')]; if (bs.length) bs.forEach((y, i) => y.classList.toggle('hien', i === bs.length - 1)); }, id);
      await pg.screenshot({ path: join(dir, id + '.png') });
    }
    console.log('chụp:', dir);
  }
}
await pg.setViewport({ width: 375, height: 812, isMobile: true });
await pg.goto(url, { waitUntil: 'networkidle0' });
const ngang = await pg.evaluate(() => document.documentElement.scrollWidth);
console.log(`375px: scrollWidth ${ngang} ${ngang > 376 ? '✗ CUỘN NGANG' : 'ok'}`);
if (ngang > 376) loi++;
console.log(loi ? `LỖI: ${loi}` : 'ĐẠT');
await b.close(); srv.close();
