// Dựng ruột tập Vật lí 12 – Bài 14 (12 trang 165×240 mm, ô ly 5 mm; đóng lò xo: lề gáy 20 mm đổi bên theo trang chẵn/lẻ). Theo nhịp buổi L12 (2 h): buổi N dạy hết bài web trên lớp 60′ (trang 1–5) + cuối giờ giao ĐỀ BTVN (ô trang 5);
// buổi N+1: 10′ ôn (trang 3) → 20′ kiểm tra → 30′ sửa bài trên lớp (trang 8); trang 9 sửa bài kiểm tra chương, trang 10 làm lại câu sai sau 1 tuần; trang 6–7 Bài tập mẫu 5 dạng bán cấu trúc (module bai14-btm.mjs); trang 11–12 ghi chú tự do (đúng 2 trang/bài, không ô hỏi trợ giảng). Hình minh hoạ: module hinh.mjs. Chạy: node scripts/ruot-tap/bai14.mjs [file.pdf]
// Mặc định ghi scripts/ruot-tap/out/ruot-tap-vl12-bai14.pdf. Cần book/node_modules (katex, qrcode-generator, puppeteer-core):
// worktree không có thì dùng book/ của bản chính ~/Projects/thachlab.
// Mã ô "Tập: trang · ô" (nhãn Web … trên giấy = tên mục trên web) trùng data-tap trong content/lesson-samples/l12-hat-nhan-mo-hinh-nguyen-tu/theory.src.html.
import { createRequire } from 'node:module';
import { existsSync, mkdirSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { btmCss, btmPages } from './bai14-btm.mjs';
import { hinh } from './hinh.mjs';
const HERE = dirname(fileURLToPath(import.meta.url));
const BOOK = [resolve(HERE, '../../book/'), '/Users/MAC/Projects/thachlab/book'].find((d) => existsSync(d + '/node_modules')) + '/';
const LINK = 'https://thachlab.id.vn/lop-hoc/bai/?id=15#muc=kiem-tra';
const require = createRequire(BOOK + 'package.json');
const katex = require('katex');
const qrcode = require('qrcode-generator');
const puppeteer = require('puppeteer-core');
const m = (s) => katex.renderToString(s, { throwOnError: true, output: 'html' });
const qr = qrcode(0, 'M'); qr.addData(LINK); qr.make();
const qrSvg = qr.createSvgTag({ cellSize: 3, margin: 0, scalable: true });
const qr2 = qrcode(0, 'M'); qr2.addData('https://thachlab.id.vn/'); qr2.make();
const qrHome = qr2.createSvgTag({ cellSize: 3, margin: 0, scalable: true });
// Góc giới thiệu cuối tập (thầy chốt 25/10): bạn mượn tập thấy tò mò muốn biết thầy/web này là gì. Giọng kể, không rao bán;
// nói đúng thứ HS 14–18 quan tâm (SDT: tự chủ, làm được, có bạn cùng học; Dahl–Steinberg: địa vị bạn cùng lứa → bảng xếp hạng).
const gioiThieu = `<div class="gt"><div class="gtq"><div class="qr">${qrSvg}</div><small>Bài học này</small></div><div class="gtq"><div class="qr">${qrHome}</div><small>Trang chủ</small></div><div>
<b>Vật lí thầy Thạch · thachlab.id.vn.</b> Tập này đi cùng bài học trên web: lý thuyết kèm thí nghiệm và mô phỏng, tự kiểm tra chấm
ngay, bài tập mẫu giải từng bước, đề luyện bám đề thi tốt nghiệp, bảng xếp hạng theo mùa. Mượn tập của bạn thì quét mã trang chủ để xem thử.</div></div>`;
// Source Sans 3 (OFL, thầy chốt 25/10 để tiết kiệm trang): hẹp hơn Noto Sans ~10%, x-height cao nên hạ cỡ chữ xuống 3,3 mm vẫn dễ đọc;
// có dấu tiếng Việt. Mỗi tệp con PHẢI có unicode-range, nếu không tệp sau đè tệp trước và chữ in đậm rơi về Helvetica.
const F = resolve(HERE, 'fonts') + '/source-sans-3-';
const UR = {
  latin: 'U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD',
  'latin-ext': 'U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF',
  vietnamese: 'U+0102-0103,U+0110-0111,U+0128-0129,U+0168-0169,U+01A0-01A1,U+01AF-01B0,U+0300-0301,U+0303-0304,U+0308-0309,U+0323,U+0329,U+1EA0-1EF9,U+20AB',
};
const fonts = [400, 700].flatMap((w) => Object.keys(UR).map((sub) =>
  `@font-face{font-family:BV;font-weight:${w};src:url("${pathToFileURL(F + sub + '-' + w + '-normal.woff2').href}");unicode-range:${UR[sub]}}`)).join('');
const lines = (n) => Array.from({ length: n }, () => '<div class="ln"></div>').join('');
// n dòng kẻ chấm, nhãn (a), b)…) nằm ngay đầu dòng đầu để không tốn thêm một dòng
const wl = (label, n) => `<div class="ln"><b>${label}</b></div>` + lines(n - 1);

// Nhãn góc phải: mã "trang·ô" trùng nhãn "✍ Tập: trang · ô" khi trình chiếu (data-tap trong theory.src.html).
const tag = (t) => `<span class="tag">Tập ${t}</span>`;
const foot = (n) => `<div class="foot"><span></span><span>Bài 14 · ${n}/12</span></div>`;
// Không Ngày/Tên (các tờ đóng thành sách — thầy chốt 25/10); phụ đề chỉ khi thật cần, thầy tự điều phối nhịp buổi.
const head = (t, s = '') => `<div class="top"><div><b>${t}</b>${s ? `<small>${s}</small>` : ''}</div></div>`;
const yn = `<td style="white-space:nowrap;padding:.2mm 1.8mm"><span class="ck"></span>Có &nbsp;<span class="ck"></span>Không</td>`;
const box = (inner, extra = '') => `<div style="background:#fff;border:.3mm solid var(--grid);border-radius:1.5mm;padding:1mm 3mm;${extra}">${inner}</div>`;
const rkRow = (i) => `<tr><td><b>${i}</b></td><td></td><td><span class="ck"></span></td><td><span class="ck"></span></td></tr>`;
const rkTable = (rows) => `<table class="rk"><tr><th style="width:9mm">Câu</th><th>Em chọn</th><th style="width:15mm">Chắc?</th><th style="width:15mm">Đúng?</th></tr>${rows}</table>`;

// Trang "Sửa bài" (thầy chốt 25/10, góc nhìn HS trung bình theo kịp 30′ chữa bài): đề làm trên web nên KHÔNG chép lại lưới đáp án
// (web đã hiện em–đúng từng câu; thầy chốt 25/10 bỏ lưới) — chỉ ghi số câu sai ở dòng đầu, rồi 5 ô "Thầy chữa" rộng, mỗi ô một câu,
// 4 tick lí do + ☐ làm lại; hai dòng ghi nhớ; dưới cùng dòng tra ô Tập để xem lại.
const traNhanh = `<div class="tra"><b>Xem lại ở Tập:</b> kí hiệu, lực hạt nhân 1·4 · đồng vị 2·1 · mô hình 2·2 · R, u, khối lượng 2·3 · bẫy 3·1 · dạng 1–3 → 6·1 · dạng 4–5 → 7·1</div>`;
const chua = (k) => `<div class="chb"><div class="chh"><b>Câu ……</b> <span>sai vì: <span class="ck"></span>đọc đề <span class="ck"></span>công thức <span class="ck"></span>tính <span class="ck"></span>đơn vị</span><span><span class="ck"></span>làm lại (tr.10)</span></div>${lines(k)}</div>`;
const fixPage = (n, { title, sub = '', lap = false, ks = [5, 5, 5, 4, 4] }) => `<section class="page">
${head(title, sub)}
<div class="card soft" style="padding:1mm 3mm"><div style="display:flex;gap:4mm;flex-wrap:wrap"><span>Đề: ……………………………</span><span>Điểm: ……/……</span>${lap ? '<span>Lần trước: ……/……</span>' : '<span>Làm trên: <span class="ck"></span>thachlab <span class="ck"></span>Azota</span>'}</div>
<div style="margin-top:.6mm"><b>Câu sai:</b> P.I <span class="fill" style="min-width:24mm"></span> · P.II <span class="fill" style="min-width:20mm"></span> · P.III <span class="fill" style="min-width:12mm"></span></div></div>
<h3><i>1</i>Thầy chữa</h3>
${ks.map(chua).join('')}
<h3><i>2</i>Ghi nhớ sau buổi sửa</h3>
${box(lines(2))}
${traNhanh}
${foot(n)}</section>`;

const html = `<!doctype html><html lang="vi"><head><meta charset="utf-8"><title>Ruột tập Vật lí 12 – Bài 14</title>
<link rel="stylesheet" href="${pathToFileURL(BOOK + 'node_modules/katex/dist/katex.min.css').href}">
<style>
${fonts}
@page{size:165mm 240mm;margin:0}
*{box-sizing:border-box}
/* Thang cỡ chữ 4 mức (C3): --fs-h1 tiêu đề trang · --fs-h3 tiêu đề mục · --fs-body thân (3,3 mm ≈ 9,4 pt với Source Sans 3) · --fs-sm chữ phụ
   (2,95 mm ≈ 8,4 pt, không nhỏ hơn — C1). Dòng kẻ 5 mm = 1,43 thân chữ; đoạn chữ liền line-height 1.45 (= 5,1 mm, khớp ô ly) để dấu tiếng Việt không chạm dòng trên. */
:root{--ink:#1c2540;--navy:#1d3a78;--grid:#d3dbec;--soft:#eef2fa;--hint:#5f6a88;--fs-h1:4.4mm;--fs-h3:3.7mm;--fs-body:3.3mm;--fs-sm:2.95mm;
 --pl:20mm;--pr:10mm}
body{margin:0;font:400 var(--fs-body)/1.45 BV,KaTeX_Main,KaTeX_AMS,sans-serif;text-rendering:optimizeLegibility;font-kerning:normal;color:var(--ink)}
/* Lề đóng lò xo: mép gáy 20 mm (lỗ xoắn ăn ~8 mm + ngón tay giữ), mép ngoài 10 mm. Trang lẻ gáy bên trái, trang chẵn gáy bên phải (in hai mặt). */
.page{width:165mm;height:240mm;padding:11mm var(--pr) 14mm var(--pl);position:relative;overflow:hidden;page-break-after:always;
 background-image:linear-gradient(var(--grid) .15mm,transparent .15mm),linear-gradient(90deg,var(--grid) .15mm,transparent .15mm);background-size:5mm 5mm;background-position:var(--pl) 11mm}
.page:nth-of-type(even){--pl:10mm;--pr:20mm}
.page>*{position:relative}
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
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:2mm;margin:2mm 0}
.steps div{background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:1.5mm 2mm;font-size:var(--fs-sm)}
.steps b{color:var(--navy)}
.foot{position:absolute;left:var(--pl);right:var(--pr);bottom:5mm;display:flex;justify-content:space-between;font-size:var(--fs-sm);color:var(--hint);background:#fff;padding:0 1mm}
.big{font-size:7mm;text-align:center;padding:0}
.qr{width:29mm;height:29mm;padding:2mm;background:#fff;border:.3mm solid var(--grid);flex:none}.qr svg{width:25mm;height:25mm;display:block}
.tag{position:absolute;right:var(--pr);margin:1.6mm 0 0;border-radius:1mm;padding:.2mm 2mm;background:var(--navy);color:#fff;font-size:var(--fs-sm);font-weight:700;line-height:4.6mm}
/* Hình minh hoạ: SVG nét, chữ trong hình = chữ trang (H3, H4); đặt ngay cạnh câu nó minh hoạ (N8). .fig-side = hình đứng bên phải một khối chữ. */
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
.nhip{background:var(--soft);border:.3mm solid var(--grid);border-radius:1.2mm;padding:.8mm 2.5mm;font-size:var(--fs-sm);line-height:1.4;margin-bottom:1.5mm}
.nhip b{color:var(--navy)}
${btmCss}
</style></head><body>

<!-- TRANG 1: mục tiêu, dự đoán, II.1 -->
<section class="page">
${head('BÀI 14 · HẠT NHÂN VÀ NGUYÊN TỬ', 'Vật lí 12 · Chương 4: Vật lí hạt nhân')}
<h3><i>1</i>Mục tiêu</h3>${tag('1·1')}
<div class="card soft">
<div style="margin:.3mm 0"><span class="ck"></span>Nêu được hạt nhân gồm <b>prôtôn, nơtron</b> và lực giữ chúng lại</div>
<div style="margin:.3mm 0"><span class="ck"></span>Đọc và viết đúng kí hiệu ${m('{}^{A}_{Z}\\mathrm{X}')}, tính số nơtron</div>
<div style="margin:.3mm 0"><span class="ck"></span>Nói được <b>đồng vị</b> là gì; phân biệt 3 mô hình nguyên tử</div>
</div>
<h3><i>2</i>Dự đoán trước khi học</h3>${tag('1·2')}
<div class="card">
<p style="margin:0 0 1mm">Năm 1909, Rutherford bắn hạt alpha vào lá vàng mỏng và thấy như hình bên. Theo em, nguyên tử:</p>
<div class="fig-side" style="grid-template-columns:1fr 30mm"><div>
<div class="opt"><span class="b">A</span><span>Là khối cầu đặc, các hạt phân bố đều</span></div>
<div class="opt"><span class="b">B</span><span>Không có hạt nhân, chỉ có các êlectron</span></div>
<div class="opt"><span class="b">C</span><span>Gần như trống rỗng, điện dương tập trung ở một vùng rất nhỏ</span></div>
<div style="margin-top:1.5mm">Em chọn: <span class="fill" style="min-width:10mm"></span> &nbsp;<span class="ck"></span>chắc &nbsp;<span class="ck"></span>không chắc &nbsp;· <span class="hint">Vì sao?</span></div>${lines(1)}</div>
${hinh.anh('rutherford-bo-thi-nghiem.png', 'Máy dò quay quanh lá vàng, đếm hạt ở góc φ.')}</div>
</div>
<h3><i>3</i>Học xong, em sửa lại</h3>${tag('1·3')}
<div class="card soft"><div>Đáp án đúng là: <span class="fill"></span> &nbsp; Em đoán <span class="ck"></span>đúng &nbsp;<span class="ck"></span>sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
<h3><i>4</i>II.1 · Hạt nhân, lực hạt nhân, kí hiệu</h3>${tag('1·4')}
<div class="card" style="padding:1.2mm 3mm">
<div>Hạt nhân gồm <span class="fill" style="min-width:16mm"></span> và <span class="fill" style="min-width:16mm"></span>, gọi chung là <span class="fill" style="min-width:16mm"></span>.</div>
<div>Lực hạt nhân: rất <span class="fill" style="min-width:12mm"></span>, thắng lực <span class="fill" style="min-width:16mm"></span>, tầm tác dụng cỡ <span class="nw">10<span class="exp"></span>&nbsp;m</span>.</div>
<div style="display:grid;grid-template-columns:26mm 1fr;gap:3mm;align-items:center;margin-top:1mm">
<div class="big">${m('{}^{A}_{Z}\\mathrm{X}')}</div>
<div>
<div>${m('A')} (trên) = số <span class="fill" style="min-width:14mm"></span> = <span class="fill" style="min-width:14mm"></span> + <span class="fill" style="min-width:14mm"></span></div>
<div>${m('Z')} (dưới) = số <span class="fill" style="min-width:20mm"></span> &nbsp; ${m('N')} = <span class="fill" style="min-width:8mm"></span> − <span class="fill" style="min-width:8mm"></span></div>
</div></div></div>
<div class="card" style="padding:1mm 3mm"><b>Tự kiểm tra 1.</b> ${m('{}^{65}_{29}\\mathrm{Cu}')} có:<div><b>A.</b> 65 prôtôn, 29 nơtron</div><div><b>B.</b> 29 nuclôn, 36 nơtron</div><div><b>C.</b> 29 prôtôn, 36 nơtron</div><div><b>D.</b> 29 prôtôn, 65 nơtron</div>
Em chọn: <span class="fill"></span> <span class="ck"></span>chắc &nbsp; Vì ${m('N=A-Z=')} <span class="fill" style="min-width:25mm"></span></div>
${foot(1)}</section>

<!-- TRANG 2: II.2–II.4, kết quả tự kiểm tra -->
<section class="page">
${head('ĐỒNG VỊ · MÔ HÌNH · KÍCH THƯỚC')}
<h3><i>1</i>II.2 · Đồng vị</h3>${tag('2·1')}
<div class="card fig-side" style="grid-template-columns:1fr 40mm;margin-bottom:1.5mm;padding:1.2mm 3mm"><div><div>Đồng vị: cùng số <span class="fill" style="min-width:14mm"></span>, khác số <span class="fill" style="min-width:14mm"></span>; tính chất <span class="fill" style="min-width:20mm"></span> giống nhau.</div>
<div style="margin-top:1mm">Ba đồng vị của hiđrô: ${m('{}^{1}_{1}\\mathrm{H}')}, ${m('{}^{2}_{1}\\mathrm{H}')} (<span class="fill" style="min-width:12mm"></span>), ${m('{}^{3}_{1}\\mathrm{H}')} (<span class="fill" style="min-width:12mm"></span>): cùng <span class="fill" style="min-width:6mm"></span> prôtôn, nơtron <span class="fill" style="min-width:6mm"></span> / <span class="fill" style="min-width:6mm"></span> / <span class="fill" style="min-width:6mm"></span></div></div>
${hinh.dongViH('Cùng 1 prôtôn (đặc, +), khác số nơtron (rỗng).')}</div>
<table><tr><th>Cặp hạt nhân</th><th style="width:15mm">${m('Z')}</th><th style="width:15mm">${m('N')}</th><th style="width:36mm">Đồng vị?</th></tr>
<tr><td>${m('{}^{12}_{6}\\mathrm{C}')} và ${m('{}^{14}_{6}\\mathrm{C}')}</td><td></td><td></td>${yn}</tr>
<tr><td>${m('{}^{40}_{18}\\mathrm{Ar}')} và ${m('{}^{40}_{20}\\mathrm{Ca}')}</td><td></td><td></td>${yn}</tr>
<tr><td>${m('{}^{35}_{17}\\mathrm{Cl}')} và ${m('{}^{37}_{17}\\mathrm{Cl}')}</td><td></td><td></td>${yn}</tr></table>

<h3><i>2</i>II.3 · Ba mô hình nguyên tử</h3>${tag('2·2')}
<div class="card" style="padding:1.2mm 3mm;margin-bottom:1mm">Rutherford: nguyên tử có hạt nhân rất nhỏ mang điện <span class="fill" style="min-width:14mm"></span>, êlectron ở vỏ. Bohr thêm: êlectron chỉ ở những quỹ đạo có <span class="fill" style="min-width:30mm"></span>.</div>
<table class="mo"><tr><th>Thomson 1904</th><th>Rutherford 1911</th><th>Bohr 1913</th></tr>
<tr><td><div>Hình:</div><div>Điểm mới:</div><div>Bị bác bỏ / còn thiếu:</div></td><td><div>Hình:</div><div>Điểm mới:</div><div>Bị bác bỏ / còn thiếu:</div></td><td><div>Hình:</div><div>Điểm mới:</div><div>Bị bác bỏ / còn thiếu:</div></td></tr></table>

<h3><i>3</i>II.4 · Kích thước hạt nhân và đơn vị u</h3>${tag('2·3')}
<div class="card" style="padding:1.2mm 3mm"><div>${m('R=')} <span class="fill" style="min-width:9mm"></span> · 10<span class="exp"></span> · ${m('A^{1/3}')} (m) &nbsp;<span class="hint">${m('A')} là số khối, số nguyên</span></div>
<div>Nguyên tử cỡ <span class="nw">10<span class="exp"></span>&nbsp;m</span> · hạt nhân cỡ <span class="nw">10<span class="exp"></span>&nbsp;m</span> → nhỏ hơn <span class="nw"><span class="fill" style="min-width:12mm"></span>&nbsp;lần</span></div>
<div>${m('1\\ \\mathrm{u}')} = <span class="fill" style="min-width:7mm"></span> khối lượng nguyên tử <span class="fill" style="min-width:9mm"></span> ≈ <span class="nw"><span class="fill" style="min-width:18mm"></span>&nbsp;kg</span> ≈ <span class="fill" style="min-width:12mm"></span> ${m('\\mathrm{MeV}/c^2')}</div>
<div>${m('1\\ \\mathrm{MeV}=')} <span class="nw"><span class="fill" style="min-width:22mm"></span>&nbsp;J</span></div>
<div>Một nguyên tử: ${m('m\\approx')} <span class="fill" style="min-width:8mm"></span> · u &nbsp;·&nbsp; một mol: ${m('M\\approx')} <span class="nw"><span class="fill" style="min-width:8mm"></span>&nbsp;g/mol</span></div></div>
<h3><i>4</i>Kết quả tự kiểm tra câu 2–7</h3>${tag('2·4')}
<div class="two">${rkTable(rkRow(2) + rkRow(3) + rkRow(4))}${rkTable(rkRow(5) + rkRow(6) + rkRow(7))}</div>
${foot(2)}</section>

<!-- TRANG 3: bẫy, trả bài -->
<section class="page">
${head('BẪY · TRẢ BÀI')}
<h3><i>1</i>III · Ba cái bẫy hay sập</h3>${tag('3·1')}
<div class="card">
<div class="trap"><span class="ck"></span><span><b>Lấy số khối làm khối lượng.</b> ${m('A')} là số đếm nuclôn, còn khối lượng nguyên tử tính bằng u là số thực (nhôm: ${m('26{,}98\\ \\mathrm{u}')}).</span></div>
<div class="trap"><span class="ck"></span><span><b>“Đồng vị khác số prôtôn”.</b> Sai: đồng vị phải <b>cùng</b> ${m('Z')}.</span></div>
<div class="trap"><span class="ck"></span><span><b>Êlectron quay ở khoảng cách nào cũng được.</b> Bohr: chỉ ở quỹ đạo có năng lượng xác định.</span></div></div>
<h3><i>2</i>IV · Trả bài 5 câu</h3>${tag('3·2')}
${box(`<div><b>1.</b> Hạt nhân gồm những hạt nào? Vì sao không vỡ ra?<span class="ck" style="float:right;margin:0"></span></div>${lines(2)}
<div><b>2.</b> Viết kí hiệu ${m('{}^{A}_{Z}\\mathrm{X}')}, nói rõ từng chữ.<span class="ck" style="float:right;margin:0"></span></div>${lines(2)}
<div><b>3.</b> Đồng vị là gì? Kể tên ba đồng vị của hiđrô, chúng giống và khác nhau ở đâu?<span class="ck" style="float:right;margin:0"></span></div>${lines(3)}
<div><b>4.</b> Thomson, Rutherford, Bohr khác nhau ở đâu?<span class="ck" style="float:right;margin:0"></span></div>${lines(3)}
<div><b>5.</b> Đơn vị u là gì? Viết công thức bán kính hạt nhân.<span class="ck" style="float:right;margin:0"></span></div>${lines(2)}`)}
<div class="card soft" style="margin-top:1.5mm;padding:1mm 3mm"><b>Bạn cùng bàn kiểm:</b> nói được ……/5 câu · câu chưa thuộc: <span class="fill" style="min-width:30mm"></span> → đọc lại ô Tập <span class="fill" style="min-width:14mm"></span></div>
<div class="card" style="padding:1mm 3mm"><b>Ghi chú</b>${lines(8)}</div>
${foot(3)}</section>

<!-- TRANG 4: bài toán mẫu -->
<section class="page">
${head('BÀI TOÁN MẪU · ĐỌC NHÃN KIM LOẠI')}
<h3><i>1</i>V · Đề bài</h3>${tag('4')}
<div class="card soft fig-side" style="grid-template-columns:1fr 34mm;padding:1.2mm 3mm"><div>Mẫu kim loại ghi ${m('{}^{27}_{13}\\mathrm{Al}')}. Khối lượng mol nguyên tử nhôm là ${m('26{,}98\\ \\mathrm{g/mol}')}; ${m('N_A=6{,}022\\cdot10^{23}\\ \\mathrm{mol}^{-1}')}.<br>
<div><b>a)</b> Xác định số prôtôn, số nơtron của hạt nhân nhôm.</div><div><b>b)</b> Tính bán kính hạt nhân nhôm.</div><div><b>c)</b> Tính khối lượng một nguyên tử nhôm ra u và ra kg.</div><div><b>d)</b> Hai đồng vị của đồng (${m('{}^{63}_{29}\\mathrm{Cu}')}, ${m('{}^{65}_{29}\\mathrm{Cu}')}) khác nhau ở đại lượng nào?</div></div>${hinh.nhanKimLoai()}</div>
<h3><i>2</i>Phân tích đề</h3>
<table><tr><th style="width:42mm">Câu trong đề</th><th style="width:36mm">Dữ liệu</th><th>Kiến thức liên quan</th></tr>
<tr><td>“${m('{}^{27}_{13}\\mathrm{Al}')}”</td><td>${m('A=27;\\ Z=13')}</td><td>${m('N=A-Z')}</td></tr>
<tr><td style="height:6.5mm">“bán kính hạt nhân”</td><td></td><td></td></tr>
<tr><td style="height:6.5mm">“khối lượng mol”</td><td></td><td></td></tr>
<tr><td style="height:6.5mm">“ra đơn vị u”</td><td></td><td></td></tr>
<tr><td style="height:6.5mm">“hai đồng vị của đồng”</td><td></td><td></td></tr></table>
<h3><i>3</i>Giải</h3>
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm;margin-top:1mm">
${wl('a)', 3)}${wl('b)', 3)}${wl('c)', 3)}${wl('d)', 2)}
</div>
<h3><i>4</i>Mở rộng: khối lượng trung bình của đồng</h3>
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div class="ln" style="height:auto;padding-top:1mm"><b>Bước 1 (cho sẵn):</b> đồng tự nhiên = hai đồng vị ở câu d), ${m('M=63{,}54\\ \\mathrm{g/mol}')}.</div>
${wl(`Bước 2: m(Cu) = 63,54 / ${m('N_A')} = …&nbsp;g = …&nbsp;kg`, 2)}${wl('Bước 3: đổi sang u = … ; so với 63 và 65:', 2)}</div>
<div class="card soft" style="margin-top:1.5mm;padding:1mm 3mm"><b>Em tự kiểm:</b> <span class="ck"></span>${m('N')} là số nguyên &nbsp;<span class="ck"></span>${m('R')} cỡ ${m('10^{-15}')} m &nbsp;<span class="ck"></span>có ghi đơn vị</div>
${foot(4)}</section>

<!-- TRANG 5: mang về, thử thách, mô phỏng -->
<section class="page">
${head('BÀI TẬP VỀ NHÀ · MANG VỀ · THỬ THÁCH')}
<h3><i>1</i>Đề BTVN</h3>
<div class="card" style="padding:1.2mm 3mm">
<div>
<div><b>Đề:</b> <span class="fill" style="min-width:52mm"></span> &nbsp;<b>Số câu:</b> <span class="fill" style="min-width:10mm"></span></div>
<div style="margin-top:.8mm"><b>Làm ở:</b> <span class="ck"></span>thachlab &nbsp;<span class="ck"></span>Azota &nbsp;<span class="ck"></span>giấy &nbsp;· <b>Hạn:</b> ……/……</div>
${wl('Ghi chú của thầy về đề:', 2)}
<div style="margin-top:.8mm"><span class="ck"></span><b>Đã nộp</b> &nbsp;· <b>Điểm:</b> ……/…… &nbsp;· <b>Câu sai:</b> <span class="fill" style="min-width:34mm"></span></div>
</div>
</div>
<h3><i>2</i>VI · Mang về: điều em dễ quên nhất</h3>${tag('5')}
${box(wl('1.', 2) + wl('2.', 2) + wl('3.', 2))}
<h3><i>3</i>Thử thách phân tầng</h3>
<div class="fig-side" style="grid-template-columns:1fr 42mm">${box(`<div class="ln"><b>★ ${m('{}^{4}_{2}\\mathrm{He}')}:</b> số prôtôn <span class="fill" style="min-width:10mm"></span> · số nơtron <span class="fill" style="min-width:10mm"></span> · vì <span class="fill" style="min-width:20mm"></span></div>` + wl('★★ Vì sao nơtron làm hạt nhân bền hơn?', 2) + wl('★★★ Hạt nhân vàng chiếm bao nhiêu phần thể tích nguyên tử? (kích thước ở Tập 2·3)', 4))}${hinh.kichThuoc()}</div>
<h3><i>4</i>Câu 7 (urani) và mô phỏng PhET</h3>
<div class="fig-side" style="grid-template-columns:1fr 36mm">${box(wl(`Câu 7 (${m('{}^{238}_{92}\\mathrm{U}')}): A, Z, N = …`, 2)
 + wl('Bắn hạt alpha (Rutherford) · Dự đoán:', 1) + wl('Thấy:', 2)
 + wl('Đồng vị neon · Dự đoán:', 1) + wl('Thấy / vì sao 20,18:', 2))}${hinh.anh('rutherford-alpha-qua-la-vang.png', 'Chỉ hạt alpha đi sát hạt nhân (chấm đỏ) mới lệch mạnh.')}</div>
${foot(5)}</section>

${btmPages(6, { m, head, foot, tag, lines, wl, hinh })}
${fixPage(8, { title: 'SỬA BÀI TRÊN LỚP' })}
${fixPage(9, { title: 'SỬA BÀI KIỂM TRA CHƯƠNG', lap: true, ks: [5, 5, 4, 4, 4] })}
<!-- TRANG 10: làm lại câu sai sau 1 tuần (retrieval cách quãng) -->
<section class="page">
${head('LÀM LẠI CÂU SAI · SAU 1 TUẦN')}
<div class="card soft" style="padding:1mm 3mm"><b>Câu lấy từ:</b> trang 8 (câu ……………) · trang 9 (câu ……………)</div>
${[1, 2, 3, 4].map((i) => `<h3><i>${i}</i>Câu …… <span class="hint">(từ trang ……)</span> &nbsp;<span class="ck"></span>lần này đúng</h3>${box(lines(6))}`).join('')}
<div class="card soft" style="margin-top:1.5mm;padding:1mm 3mm"><b>Kết quả:</b> đúng ……/…… &nbsp;<span class="ck"></span>đã hỏi thầy câu còn sai</div>
${foot(10)}</section>

<!-- TRANG 11–12: ghi chú tự do -->
${[11, 12].map((n) => `<section class="page dots">
${head('GHI CHÚ')}
${n === 12 ? gioiThieu : ''}
${foot(n)}</section>`).join('')}
</body></html>`;

const out = process.argv[2] ?? resolve(HERE, 'out/ruot-tap-vl12-bai14.pdf');
mkdirSync(dirname(out), { recursive: true });
writeFileSync(out + '.html', html);
const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true, args: ['--no-sandbox', '--allow-file-access-from-files'] });
const p = await b.newPage();
await p.goto(pathToFileURL(out + '.html').href, { waitUntil: 'networkidle0' });
await p.evaluate('document.fonts.ready');
const diag = await p.evaluate(() => [...document.querySelectorAll('.page')].map((pg, i) => {
  const lim = pg.getBoundingClientRect().bottom - 14 * 3.7795; // chừa chân trang
  let max = 0; pg.querySelectorAll('.page>*:not(.foot)').forEach(e => { max = Math.max(max, e.getBoundingClientRect().bottom); });
  return `trang ${i + 1}: dư ${Math.round((lim - max) / 3.7795)} mm; katexErr=${pg.querySelectorAll('.katex-error').length}`;
}));
console.log(diag.join('\n'));
await p.pdf({ path: out, preferCSSPageSize: true, printBackground: true });
await b.close();
