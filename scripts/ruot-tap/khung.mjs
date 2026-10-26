// Khung dùng chung cho ruột tập VL12 từ Bài 15 trở đi (bai15.mjs … bai18.mjs): cùng bố cục 12 trang, cùng quy ước thầy chốt 25/10/2026
// (xem skill sach-in-tu-web, mục "Ruột tập theo bài"). bai14.mjs giữ nguyên bản riêng (đã in thử), khung này chép CSS/trang cố định từ đó.
// Dùng: const K = khoiTao({ bai: 15, lid: 16, ten: 'NĂNG LƯỢNG LIÊN KẾT' }); rồi ghép trang 1–5 bằng các helper K.*, gọi
// `await K.dung({ p15: '<section>…', btm: { dang, tach: [3, 3], kq: [[1,2,3],[4,5,6]], khoNhat: true }, tra: 'chuỗi tra nhanh' })`.
// Trang 8–12 (sửa bài, làm lại, ghi chú) sinh tự động; trang 6–7 từ btm.dang (module bai14-btm.mjs chỉ lấy btmCss).
import { createRequire } from 'node:module';
import { existsSync, mkdirSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { btmCss } from './bai14-btm.mjs';
import { hinh as hinh14 } from './hinh.mjs';
import { hinhCh4 } from './hinh-ch4.mjs';
const HERE = dirname(fileURLToPath(import.meta.url));
const BOOK = [resolve(HERE, '../../book/'), '/Users/MAC/Projects/thachlab/book'].find((d) => existsSync(d + '/node_modules')) + '/';
const require = createRequire(BOOK + 'package.json');
const katex = require('katex');
const qrcode = require('qrcode-generator');
const puppeteer = require('puppeteer-core');

export const hinh = { ...hinh14, ...hinhCh4 };
export const m = (s) => katex.renderToString(s, { throwOnError: true, output: 'html' });
const qrSvgOf = (url) => { const q = qrcode(0, 'M'); q.addData(url); q.make(); return q.createSvgTag({ cellSize: 3, margin: 0, scalable: true }); };

const F = resolve(HERE, 'fonts') + '/source-sans-3-';
const UR = {
  latin: 'U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD',
  'latin-ext': 'U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF',
  vietnamese: 'U+0102-0103,U+0110-0111,U+0128-0129,U+0168-0169,U+01A0-01A1,U+01AF-01B0,U+0300-0301,U+0303-0304,U+0308-0309,U+0323,U+0329,U+1EA0-1EF9,U+20AB',
};
const fonts = [400, 700].flatMap((w) => Object.keys(UR).map((sub) =>
  `@font-face{font-family:BV;font-weight:${w};src:url("${pathToFileURL(F + sub + '-' + w + '-normal.woff2').href}");unicode-range:${UR[sub]}}`)).join('');

export const lines = (n) => Array.from({ length: n }, () => '<div class="ln"></div>').join('');
export const wl = (label, n) => `<div class="ln"><b>${label}</b></div>` + lines(n - 1);
export const fill = (w = 18) => `<span class="fill" style="min-width:${w}mm"></span>`;
export const nw = (s) => `<span class="nw">${s}</span>`;
export const exp = '<span class="exp"></span>';
export const ck = '<span class="ck"></span>';
export const yn = `<td style="white-space:nowrap;padding:.2mm 1.8mm"><span class="ck"></span>Có &nbsp;<span class="ck"></span>Không</td>`;
export const box = (inner, extra = '') => `<div style="background:#fff;border:.3mm solid var(--grid);border-radius:1.5mm;padding:1mm 3mm;${extra}">${inner}</div>`;
export const rkRow = (i) => `<tr><td><b>${i}</b></td><td></td><td><span class="ck"></span></td><td><span class="ck"></span></td></tr>`;
export const rkTable = (rows) => `<table class="rk"><tr><th style="width:9mm">Câu</th><th>Em chọn</th><th style="width:15mm">Chắc?</th><th style="width:15mm">Đúng?</th></tr>${rows}</table>`;
export const rkHai = (a, b) => `<div class="two">${rkTable(a.map(rkRow).join(''))}${rkTable(b.map(rkRow).join(''))}</div>`;
export const opt = (c, s) => `<div class="opt"><span class="b">${c}</span><span>${s}</span></div>`;
export const abcd = (a) => a.map((s, i) => `<div><b>${'ABCD'[i]}.</b> ${s}</div>`).join('');
// Một dòng chọn đáp án + chắc + (tuỳ) lí do
export const chon = (n = 10) => `Em chọn: ${fill(n)} <span class="ck"></span>chắc &nbsp;<span class="ck"></span>không chắc`;

// Đánh số trang liền mạch cả quyển (một quyển = một chương, năm bài × 12 trang): bài 14 = tr.1–12, bài 15 = tr.13–24 … bài 18 = tr.49–60.
// BOOK_PAGE_START (mặc định 1) = số trang của trang đầu bài 14, để quyển nối tiếp chương liền kề (vd 61 nếu chương trước dài 60 trang);
// số bắt đầu chẵn thì lề gáy đổi bên (class .flip). Nhãn "Tập t·ô" trên giấy dùng số trang tuyệt đối này.
export const BAI_DAU = 14, TRANG_MOI_BAI = 12;
export const TRANG_DAU = Number(process.env.BOOK_PAGE_START ?? 1);
export function khoiTao({ bai, lid, ten, sub = 'Vật lí 12 · Chương 4: Vật lí hạt nhân' }) {
  const off = (bai - BAI_DAU) * TRANG_MOI_BAI + TRANG_DAU - 1;   // + off = số trang trong quyển
  const abs = (t) => String(t).replace(/^(\d+)/, (_, a) => Number(a) + off);
  const absAll = (s) => s.replace(/(\d+)(·\d+)/g, (_, a, k) => Number(a) + off + k);
  const LINK = `https://thachlab.id.vn/lop-hoc/bai/?id=${lid}#muc=kiem-tra`;
  const qrSvg = qrSvgOf(LINK), qrHome = qrSvgOf('https://thachlab.id.vn/');
  const tag = (t) => `<span class="tag">Tập ${abs(t)}</span>`;
  const foot = (n) => `<div class="foot"><span></span><span>Bài ${bai} · tr. ${n + off}</span></div>`;
  const head = (t, s = '') => `<div class="top"><div><b>${t}</b>${s ? `<small>${s}</small>` : ''}</div></div>`;
  const h3 = (i, t, tg = '') => `<h3><i>${i}</i>${t}</h3>${tg ? tag(tg) : ''}`;
  const card = (inner, extra = '', cls = '') => `<div class="card ${cls}" style="${extra}">${inner}</div>`;
  const gioiThieu = `<div class="gt"><div class="gtq"><div class="qr">${qrSvg}</div><small>Bài học này</small></div><div class="gtq"><div class="qr">${qrHome}</div><small>Trang chủ</small></div><div>
<b>Xem lại bài này trên thachlab.id.vn:</b> quét mã <b>Bài học này</b> để mở lý thuyết, thí nghiệm, mô phỏng, tự kiểm tra và bài tập mẫu
đúng bài ${bai}; mã <b>Trang chủ</b> để vào các bài khác.</div></div>`;

  const chua = (k) => `<div class="chb"><div class="chh"><b>Câu ……</b> <span>sai vì: <span class="ck"></span>đọc đề <span class="ck"></span>công thức <span class="ck"></span>tính <span class="ck"></span>đơn vị</span><span><span class="ck"></span>làm lại (tr.${10 + off})</span></div>${lines(k)}</div>`;
  const fixPage = (n, tra, { title, lap = false, ks = [5, 5, 5, 4, 4] }) => `<section class="page">
${head(title)}
<div class="card soft" style="padding:1mm 3mm"><div style="display:flex;gap:4mm;flex-wrap:wrap"><span>Đề: ……………………………</span><span>Điểm: ……/……</span>${lap ? '<span>Lần trước: ……/……</span>' : '<span>Làm trên: <span class="ck"></span>thachlab <span class="ck"></span>Azota</span>'}</div>
<div style="margin-top:.6mm"><b>Câu sai:</b> P.I <span class="fill" style="min-width:24mm"></span> · P.II <span class="fill" style="min-width:20mm"></span> · P.III <span class="fill" style="min-width:12mm"></span></div></div>
<h3><i>1</i>Thầy chữa</h3>
${ks.map(chua).join('')}
<h3><i>2</i>Ghi nhớ sau buổi sửa</h3>
${box(lines(2))}
<div class="tra"><b>Xem lại ở Tập:</b> ${absAll(tra)}</div>
${foot(n)}</section>`;

  const btvn = () => `<h3><i>1</i>Đề BTVN</h3>
<div class="card" style="padding:1.2mm 3mm">
<div>
<div><b>Đề:</b> <span class="fill" style="min-width:52mm"></span> &nbsp;<b>Số câu:</b> <span class="fill" style="min-width:10mm"></span></div>
<div style="margin-top:.8mm"><b>Làm ở:</b> <span class="ck"></span>thachlab &nbsp;<span class="ck"></span>Azota &nbsp;<span class="ck"></span>giấy &nbsp;· <b>Hạn:</b> ……/……</div>
${wl('Ghi chú của thầy về đề:', 2)}
<div style="margin-top:.8mm"><span class="ck"></span><b>Đã nộp</b> &nbsp;· <b>Điểm:</b> ……/…… &nbsp;· <b>Câu sai:</b> <span class="fill" style="min-width:34mm"></span></div>
</div>
</div>`;

  // ---- Bài tập mẫu (trang 6–7) ----
  const f = (w) => fill(w);
  const ansRow = (labels) => `<div class="ans${labels.length === 3 ? ' c3' : ''}">${labels.map((l) => `<div><b>${l})</b>${f(10)}</div>`).join('')}</div>`;
  const tu = '<span><span class="ck"></span>tự làm &nbsp;<span class="ck"></span>cần gợi ý</span>';
  const gi = (k, fig) => !k ? '' : fig ? `<div class="fig-side" style="grid-template-columns:1fr 46mm;margin-bottom:.8mm"><div class="gi" style="margin:0">${wl('Phân tích và giải:', k)}</div>${hinh[fig]()}</div>` : `<div class="gi">${wl('Phân tích và giải:', k)}</div>`;
  const block = (d) => `<div class="bt"><div class="hd"><span>${d.t}</span>${tu}</div><div class="de">${d.de}</div>${d.bang ?? ''}<div class="nd"><b>Mấu chốt:</b> ${d.nd}</div>${gi(d.gi, d.fig)}${ansRow(d.a)}</div>`;
  const kq = (ds) => `<div class="card soft" style="padding:1.2mm 3mm"><b>Ba bài tương tự:</b> đúng ${ds.map((i) => `D${i} ……/3`).join(' · ')}</div>`;
  const btmTrang = (n, btm) => {
    const [a, b] = btm.tach, cuoi = btm.dang.length;
    return `<section class="page">
${head(`BÀI TẬP MẪU · DẠNG 1–${a}`)}
${h3(1, 'Nhận dạng và đáp số', `${n}·1`)}
${btm.dang.slice(0, a).map(block).join('\n')}
${kq(btm.kq[0])}
${foot(n)}</section>
<section class="page">
${head(`BÀI TẬP MẪU · DẠNG ${a + 1}–${cuoi}`)}
${h3(1, 'Giải', `${n + 1}·1`)}
${btm.dang.slice(a).map(block).join('\n')}
${kq(btm.kq[1])}
${btm.khoNhat === false ? '' : `<div class="card soft" style="padding:1.2mm 3mm">Dạng em thấy khó nhất: D……, vì:${lines(1)}</div>`}
${foot(n + 1)}</section>`;
  };

  const css = `${fonts}
@page{size:165mm 240mm;margin:0}
*{box-sizing:border-box}
:root{--ink:#1c2540;--navy:#1d3a78;--grid:#d3dbec;--soft:#eef2fa;--hint:#5f6a88;--fs-h1:4.4mm;--fs-h3:3.7mm;--fs-body:3.3mm;--fs-sm:2.95mm;--pl:20mm;--pr:10mm}
body{margin:0;font:400 var(--fs-body)/1.45 BV,KaTeX_Main,KaTeX_AMS,sans-serif;text-rendering:optimizeLegibility;font-kerning:normal;color:var(--ink)}
.page{width:165mm;height:240mm;padding:11mm var(--pr) 14mm var(--pl);position:relative;overflow:hidden;page-break-after:always;
 background-image:linear-gradient(var(--grid) .15mm,transparent .15mm),linear-gradient(90deg,var(--grid) .15mm,transparent .15mm);background-size:5mm 5mm;background-position:var(--pl) 11mm}
.page:nth-of-type(even){--pl:10mm;--pr:20mm}
.page>*{position:relative}
body.flip .page:nth-of-type(odd){--pl:10mm;--pr:20mm}body.flip .page:nth-of-type(even){--pl:20mm;--pr:10mm}
.top{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:.5mm solid var(--navy);padding-bottom:1mm;margin-bottom:2mm;background:#fff}
.top b{display:block;font-weight:700;font-size:var(--fs-h1);color:var(--navy)}.top small{color:var(--hint);font-size:var(--fs-sm)}
h3{margin:1.8mm 0 1mm;line-height:1.25;font-weight:700;font-size:var(--fs-h3);color:var(--navy);background:#fff;display:inline-block;padding-right:2mm}
h3 i{font-style:normal;background:var(--navy);color:#fff;border-radius:1mm;padding:.2mm 1.6mm;margin-right:1.5mm;font-size:var(--fs-sm)}
.card{background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:1.6mm 3mm;margin-bottom:1.5mm}
.card.soft{background:var(--soft);border-color:var(--grid)}
.hint{color:var(--hint);font-size:var(--fs-sm)}
.opt{display:flex;gap:2mm;margin:.8mm 0}.opt .b{width:4.6mm;height:4.6mm;border:.3mm solid var(--navy);border-radius:50%;flex:none;text-align:center;font-size:var(--fs-sm);line-height:4.2mm;font-weight:700;color:var(--navy)}
.ln{height:5mm;border-bottom:.2mm dotted var(--hint);background:#fff}
.two{display:grid;grid-template-columns:1fr 1fr;gap:3mm}
.box{border:.3mm solid var(--navy);background:#fff;border-radius:1.5mm}
.fill{display:inline-block;min-width:18mm;border-bottom:.3mm solid var(--navy);height:4mm;vertical-align:baseline}
table{border-collapse:collapse;width:100%;background:#fff;font-size:var(--fs-body)}
th,td{border:.3mm solid var(--navy);padding:.7mm 1.8mm;vertical-align:top}
th{background:var(--soft);font-weight:700;text-align:left}
.ck{display:inline-block;width:4.8mm;height:4.8mm;border:.3mm solid var(--navy);border-radius:.7mm;vertical-align:-1.1mm;margin-right:1mm}
.mo td{height:27mm;vertical-align:top;font-size:var(--fs-sm);color:var(--hint)}.mo td div{border-bottom:.2mm dotted var(--grid);margin-top:5mm}.mo td div:first-child{margin-top:0;padding-bottom:8.5mm}
.rk td,.rk th{padding:0 1mm;height:5mm;line-height:3.6mm;font-size:var(--fs-sm);text-align:center;vertical-align:middle}.rk .ck{margin:0;vertical-align:middle}
.foot{position:absolute;left:var(--pl);right:var(--pr);bottom:5mm;display:flex;justify-content:space-between;font-size:var(--fs-sm);color:var(--hint);background:#fff;padding:0 1mm}
.big{font-size:7mm;text-align:center;padding:0}
.qr{width:29mm;height:29mm;padding:2mm;background:#fff;border:.3mm solid var(--grid);flex:none}.qr svg{width:25mm;height:25mm;display:block}
.tag{position:absolute;right:var(--pr);margin:1.6mm 0 0;border-radius:1mm;padding:.2mm 2mm;background:var(--navy);color:#fff;font-size:var(--fs-sm);font-weight:700;line-height:4.6mm}
.fig{margin:0;background:#fff;border:.3mm solid var(--grid);border-radius:1.5mm;padding:1mm 1.5mm .6mm;min-width:0}.fig svg{display:block;width:100%;height:auto;font-family:BV,sans-serif}
.fig figcaption,.fig .cap{font-size:var(--fs-sm);color:var(--hint);line-height:1.3;margin-top:.4mm}
.fig-side{display:grid;gap:2.5mm;align-items:start}
.page.dots{background-image:radial-gradient(circle,#aab4cc .3mm,transparent .35mm);background-size:5mm 5mm;background-position:0 0;background-origin:content-box;background-clip:content-box}
.nw{white-space:nowrap}
.gt{position:absolute;left:var(--pl);right:var(--pr);bottom:13mm;display:flex;gap:3mm;align-items:center;background:#fff;border:.25mm solid var(--grid);border-radius:1.5mm;padding:1.6mm 2.5mm;font-size:var(--fs-sm);line-height:1.4;color:var(--hint)}.gt b{color:var(--navy)}
.gtq{text-align:center;flex:none}.gtq .qr{width:22mm;height:22mm;padding:1.5mm;border:0}.gtq .qr svg{width:19mm;height:19mm}.gtq small{display:block;font-size:var(--fs-sm)}
.tra{background:#fff;border:.3mm dashed var(--navy);border-radius:1.2mm;padding:.6mm 2mm;font-size:var(--fs-sm);line-height:1.4;margin-bottom:.5mm}
.chb{background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm .4mm;margin-bottom:1.4mm}
.chh{display:flex;justify-content:space-between;gap:2mm;align-items:center;font-size:var(--fs-sm);line-height:5mm;white-space:nowrap}.chh .ck{width:3.6mm;height:3.6mm;border-radius:.5mm;vertical-align:-.7mm;margin:0 .4mm 0 1mm}
.exp{display:inline-block;width:9mm;height:3.8mm;border:.3mm solid var(--navy);border-radius:.6mm;background:#fff;vertical-align:1.3mm;margin:0 .5mm}
.trap{display:flex;gap:2mm;align-items:flex-start;margin:1mm 0}
.tbl-ct td{height:6.5mm}
${btmCss}`;

  async function dung({ trang1to5, btm, tra, out = resolve(HERE, `out/ruot-tap-vl12-bai${bai}.pdf`), fix2 = {} }) {
    const html = `<!doctype html><html lang="vi"><head><meta charset="utf-8"><title>Ruột tập Vật lí 12 – Bài ${bai}</title>
<link rel="stylesheet" href="${pathToFileURL(BOOK + 'node_modules/katex/dist/katex.min.css').href}">
<style>${css}</style></head><body${TRANG_DAU % 2 === 0 ? ' class="flip"' : ''}>
${trang1to5}
${btmTrang(6, btm)}
${fixPage(8, tra, { title: 'SỬA BÀI TRÊN LỚP' })}
${fixPage(9, tra, { title: 'SỬA BÀI KIỂM TRA CHƯƠNG', lap: true, ks: [5, 5, 4, 4, 4], ...fix2 })}
<section class="page">
${head('LÀM LẠI CÂU SAI · SAU 1 TUẦN')}
<div class="card soft" style="padding:1mm 3mm"><b>Câu lấy từ:</b> trang ${8 + off} (câu ……………) · trang ${9 + off} (câu ……………)</div>
${[1, 2, 3, 4].map((i) => `<h3><i>${i}</i>Câu …… <span class="hint">(từ trang ……)</span> &nbsp;<span class="ck"></span>lần này đúng</h3>${box(lines(6))}`).join('')}
<div class="card soft" style="margin-top:1.5mm;padding:1mm 3mm"><b>Kết quả:</b> đúng ……/…… &nbsp;<span class="ck"></span>đã hỏi thầy câu còn sai</div>
${foot(10)}</section>
${[11, 12].map((n) => `<section class="page dots">
${head('GHI CHÚ')}
${n === 12 ? gioiThieu : ''}
${foot(n)}</section>`).join('')}
</body></html>`;
    mkdirSync(dirname(out), { recursive: true });
    writeFileSync(out + '.html', html);
    const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true, args: ['--no-sandbox', '--allow-file-access-from-files'] });
    const p = await b.newPage();
    await p.goto(pathToFileURL(out + '.html').href, { waitUntil: 'networkidle0' });
    await p.evaluate('document.fonts.ready');
    const diag = await p.evaluate(() => [...document.querySelectorAll('.page')].map((pg, i) => {
      const lim = pg.getBoundingClientRect().bottom - 14 * 3.7795;
      let max = 0; pg.querySelectorAll('.page>*:not(.foot)').forEach((e) => { max = Math.max(max, e.getBoundingClientRect().bottom); });
      return `trang ${i + 1}: dư ${Math.round((lim - max) / 3.7795)} mm; katexErr=${pg.querySelectorAll('.katex-error').length}`;
    }));
    console.log(diag.join('\n'));
    await p.pdf({ path: out, preferCSSPageSize: true, printBackground: true });
    await b.close();
    console.log('→', out);
  }
  return { bai, lid, tag, foot, head, h3, card, btvn, gi, dung, gioiThieu, ten, sub, hinh };
}
