// Dựng PDF từ một file HTML: KaTeX → QR → Paged.js → Chrome in PDF.
// Dùng: node render.mjs <vào.html> <ra.pdf>
import puppeteer from 'puppeteer-core';
import { pathToFileURL } from 'node:url';
import { resolve } from 'node:path';

const [,, inp, out] = process.argv;
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const browser = await puppeteer.launch({ executablePath: CHROME, headless: true, args: ['--no-sandbox', '--allow-file-access-from-files'] });
const page = await browser.newPage();
page.on('console', m => { const t = m.text(); if (/error|warn|PAGES/i.test(t)) console.log('[page]', t.slice(0, 300)); });
page.on('pageerror', e => console.log('[pageerror]', String(e).slice(0, 300)));
await page.goto(pathToFileURL(resolve(inp)).href, { waitUntil: 'load', timeout: 120000 });
await page.waitForFunction('window.__bookDone === true || window.__bookError', { timeout: 600000 });
const err = await page.evaluate('window.__bookError || null');
if (err) { console.log('LỖI:', err); }
const pages = await page.evaluate('document.querySelectorAll(".pagedjs_page").length');
console.log('PAGES', pages);
const diag = await page.evaluate(() => {
  const out = { katexErr: document.querySelectorAll('.katex-error').length, overflow: [], dollars: 0 };
  document.querySelectorAll('.pagedjs_page').forEach((pg, i) => {
    const area = pg.querySelector('.pagedjs_page_content > div') || pg.querySelector('.pagedjs_page_content');
    if (!area) return;
    const ar = area.getBoundingClientRect();
    area.querySelectorAll('*').forEach(el => {
      if (el.closest('svg') && el.tagName !== 'svg') return;
      const r = el.getBoundingClientRect();
      if (r.width > 0 && (r.right > ar.right + 3 || r.left < ar.left - 3) && !el.closest('.lopen,.sec-band,.cover,.chapter-open,.tiet')) {
        if (out.overflow.length < 12) out.overflow.push(`p${i+1} <${el.tagName.toLowerCase()} class="${(el.className&&el.className.baseVal!==undefined)?el.className.baseVal:el.className}"> +${Math.round(r.right-ar.right)}px`);
      }
    });
    if (/\$/.test(pg.innerText || '')) out.dollars++;
  });
  return out;
});
if (diag.katexErr || diag.overflow.length || diag.dollars) console.log('CHẨN ĐOÁN', JSON.stringify(diag));
await page.pdf({ path: resolve(out), preferCSSPageSize: true, printBackground: true });
await browser.close();
