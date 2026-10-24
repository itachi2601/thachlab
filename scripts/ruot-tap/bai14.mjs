// Dựng ruột tập Vật lí 12 – Bài 14 (trang 165×240 mm, ô ly 5 mm). Chạy: node scripts/ruot-tap/bai14.mjs [file.pdf]
// Mặc định ghi scripts/ruot-tap/out/ruot-tap-vl12-bai14.pdf. Cần book/node_modules (katex, qrcode-generator, puppeteer-core):
// worktree không có thì dùng book/ của bản chính ~/Projects/thachlab.
// Mã ô "Tập: trang · ô" trùng data-tap trong content/lesson-samples/l12-hat-nhan-mo-hinh-nguyen-tu/theory.src.html.
import { createRequire } from 'node:module';
import { existsSync, mkdirSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
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
const F = BOOK + 'node_modules/@fontsource/be-vietnam-pro/files/be-vietnam-pro-';
const font = (w, sub) => `@font-face{font-family:BV;font-weight:${w};src:url("${pathToFileURL(F + sub + '-' + w + '-normal.woff2').href}")}`;
const lines = (n) => '<div class="ln">'.repeat(0) + Array.from({ length: n }, () => '<div class="ln"></div>').join('');
const tag = (t) => `<span class="tag">${t}</span>`;
const foot = (n) => `<div class="foot"><span>Vật lí thầy Thạch · thachlab.id.vn</span><span>Bài 14 · trang ${n}/4</span></div>`;
const head = (t, s) => `<div class="top"><div><b>${t}</b><small>${s}</small></div><div class="who">Ngày …../….. &nbsp;Tên: ………………</div></div>`;

const html = `<!doctype html><html lang="vi"><head><meta charset="utf-8"><title>Ruột tập Vật lí 12 – Bài 14</title>
<link rel="stylesheet" href="${pathToFileURL(BOOK + 'node_modules/katex/dist/katex.min.css').href}">
<style>
${font(400, 'vietnamese')}${font(600, 'vietnamese')}${font(800, 'vietnamese')}${font(400, 'latin')}${font(700, 'latin')}
@page{size:165mm 240mm;margin:0}
*{box-sizing:border-box}
:root{--ink:#1c2540;--navy:#1d3a78;--grid:#d3dbec;--soft:#eef2fa;--hint:#6b7694}
body{margin:0;font:400 3.5mm/1.45 BV,'Be Vietnam Pro',sans-serif;color:var(--ink)}
.page{width:165mm;height:240mm;padding:11mm 12mm 14mm 14mm;position:relative;overflow:hidden;page-break-after:always;
 background-image:linear-gradient(var(--grid) .15mm,transparent .15mm),linear-gradient(90deg,var(--grid) .15mm,transparent .15mm);background-size:5mm 5mm;background-position:14mm 11mm}
.page>*{position:relative}
.top{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:.5mm solid var(--navy);padding-bottom:1.5mm;margin-bottom:3mm;background:#fff}
.top b{display:block;font-weight:800;font-size:4.6mm;color:var(--navy)}.top small{color:var(--hint);font-size:2.9mm}
.who{font-size:3mm;color:var(--hint);white-space:nowrap}
h3{margin:3mm 0 1.5mm;font-weight:800;font-size:3.9mm;color:var(--navy);background:#fff;display:inline-block;padding-right:2mm}
h3 i{font-style:normal;background:var(--navy);color:#fff;border-radius:1mm;padding:.2mm 1.6mm;margin-right:1.5mm;font-size:3.2mm}
.card{background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:2.2mm 3mm;margin-bottom:2mm}
.card.soft{background:var(--soft);border-color:var(--grid)}
.hint{color:var(--hint);font-size:2.9mm}
.opt{display:flex;gap:2mm;margin:.8mm 0}.opt .b{width:4.6mm;height:4.6mm;border:.3mm solid var(--navy);border-radius:50%;flex:none;text-align:center;font-size:2.8mm;line-height:4.2mm;font-weight:700;color:var(--navy)}
.ln{height:5mm;border-bottom:.2mm dotted var(--hint);background:#fff}
.two{display:grid;grid-template-columns:1fr 1fr;gap:3mm}
.box{border:.3mm solid var(--navy);background:#fff;border-radius:1.5mm}
.fill{display:inline-block;min-width:11mm;border-bottom:.3mm solid var(--navy);height:4mm;vertical-align:baseline}
table{border-collapse:collapse;width:100%;background:#fff;font-size:3.3mm}
th,td{border:.3mm solid var(--navy);padding:1.2mm 1.8mm;vertical-align:top}
th{background:var(--soft);font-weight:700;text-align:left}
.ck{display:inline-block;width:3.8mm;height:3.8mm;border:.3mm solid var(--navy);border-radius:.6mm;vertical-align:-.7mm;margin-right:1mm}
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:2mm;margin:2mm 0}
.steps div{background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:1.5mm 2mm;font-size:3.1mm}
.steps b{color:var(--navy)}
.foot{position:absolute;left:14mm;right:12mm;bottom:5mm;display:flex;justify-content:space-between;font-size:2.7mm;color:var(--hint);background:#fff;padding:0 1mm}
.big{font-size:8mm;text-align:center;padding:1mm 0}
.qr{width:19mm;height:19mm;flex:none}.qr svg{width:100%;height:100%}
.tag{position:absolute;right:12mm;margin:.4mm 0 0;border:.3mm solid var(--navy);border-radius:1mm;padding:0 1.4mm;background:#fff;color:var(--navy);font-size:2.6mm;font-weight:700;line-height:3.6mm}
.kw{margin:1.1mm 0;font-size:3.4mm}
.trap{display:flex;gap:2mm;align-items:flex-start;margin:1mm 0}
</style></head><body>

<!-- TRANG 1 -->
<section class="page">
${head('BÀI 14 · HẠT NHÂN VÀ NGUYÊN TỬ', 'Vật lí 12 · Chương 4: Vật lí hạt nhân')}
<h3><i>1</i>Hôm nay em làm được gì?</h3>${tag('ô 1')}
<div class="card soft">
<div><span class="ck"></span>Nêu được hạt nhân gồm <b>prôtôn, nơtron</b> và lực giữ chúng lại</div>
<div><span class="ck"></span>Đọc và viết đúng kí hiệu ${m('{}^{A}_{Z}\\mathrm{X}')}, tính số nơtron</div>
<div><span class="ck"></span>Nói được <b>đồng vị</b> là gì; phân biệt 3 mô hình nguyên tử</div>
</div>
<h3><i>2</i>Dự đoán trước khi học <span class="hint">(đoán sai cũng không sao)</span></h3>${tag('ô 2–3')}
<div class="card">
<p style="margin:0 0 1.5mm">Năm 1909, Rutherford bắn chùm hạt alpha vào lá vàng mỏng. Phần lớn hạt bay thẳng qua; một phần tám nghìn hạt lệch mạnh, vài hạt <b>bật ngược lại</b>. Theo em, nguyên tử:</p>
<div class="opt"><span class="b">A</span><span>Là khối cầu đặc, các hạt phân bố đều</span></div>
<div class="opt"><span class="b">B</span><span>Không có hạt nhân, chỉ có các êlectron</span></div>
<div class="opt"><span class="b">C</span><span>Gần như trống rỗng, điện dương tập trung ở một vùng rất nhỏ</span></div>
<div style="margin-top:2mm">Em chọn: <span class="fill"></span> &nbsp; Em <span class="ck"></span>chắc &nbsp;<span class="ck"></span>không chắc</div>
<div class="hint" style="margin-top:1.5mm">Vì sao em nghĩ vậy? (1 dòng)</div>${lines(2)}
</div>
<h3><i>3</i>Học xong, em sửa lại <span class="hint">(bút khác màu)</span></h3>
<div class="card soft"><div>Đáp án đúng là: <span class="fill"></span> &nbsp; Em đoán <span class="ck"></span>đúng &nbsp;<span class="ck"></span>sai</div>
<div class="hint" style="margin-top:1mm">Điều em hiểu sai hoặc mới biết:</div>${lines(3)}</div>
<h3><i>4</i>Năm cụm từ khoá <span class="hint">(điền chữ còn thiếu)</span></h3>${tag('ô 4')}
<div class="card" style="padding:1.2mm 3mm">
<div class="kw">🔑 Prôtôn · Nơtron · Nuclôn · Lực hạt nhân rất <span class="fill"></span></div>
<div class="kw">🔑 ${m('A')} trên · ${m('Z')} <span class="fill"></span> · ${m('N=A-Z')}</div>
<div class="kw">🔑 Cùng ${m('Z')} · Khác <span class="fill" style="min-width:8mm"></span> · Cùng tính chất hoá học</div>
<div class="kw">🔑 Vỏ êlectron · Hạt nhân nhỏ <span class="fill"></span> · Quỹ đạo lượng tử hoá</div>
<div class="kw">🔑 Đo bằng <span class="fill" style="min-width:8mm"></span> · ${m('R')} theo căn bậc <span class="fill" style="min-width:8mm"></span> ${m('A')}</div>
</div>
${foot(1)}</section>

<!-- TRANG 2 -->
<section class="page">
${head('GHI BÀI · HẠT NHÂN, ĐỒNG VỊ, MÔ HÌNH', 'Điền vào chỗ trống khi nghe giảng, đừng chép lại cả câu')}
<h3><i>1</i>II.1 · Đọc nhãn hạt nhân: trên là tổng, dưới là prôtôn</h3>${tag('ô 1')}
<div class="card" style="display:grid;grid-template-columns:30mm 1fr;gap:3mm;align-items:center;padding:1.5mm 3mm">
<div class="big">${m('{}^{A}_{Z}\\mathrm{X}')}</div>
<div>
<div>${m('A')} (trên) = số <span class="fill" style="min-width:20mm"></span> &nbsp;<span class="hint">(prôtôn + nơtron)</span></div>
<div>${m('Z')} (dưới) = số <span class="fill" style="min-width:20mm"></span> &nbsp; ${m('N')} = <span class="fill" style="min-width:8mm"></span> − <span class="fill" style="min-width:8mm"></span></div>
</div></div>
<div class="card" style="padding:1.5mm 3mm"><b>Tự kiểm tra 1.</b> ${m('{}^{65}_{29}\\mathrm{Cu}')} có:<div class="two" style="margin:.8mm 0"><div><b>A.</b> 65 prôtôn, 29 nơtron</div><div><b>B.</b> 29 nuclôn, 36 nơtron</div><div><b>C.</b> 29 prôtôn, 36 nơtron</div><div><b>D.</b> 29 prôtôn, 65 nơtron</div></div>
Em chọn: <span class="fill"></span> &nbsp; Vì ${m('N=A-Z=')} <span class="fill" style="min-width:25mm"></span></div>

<h3><i>2</i>II.2 · Đồng vị: cùng …… khác ……</h3>${tag('ô 2')}
<div class="card" style="margin-bottom:1.5mm;padding:1.5mm 3mm">Đồng vị: cùng số <span class="fill" style="min-width:14mm"></span>, khác số <span class="fill" style="min-width:14mm"></span>; tính chất <span class="fill" style="min-width:20mm"></span> giống nhau.</div>
<table><tr><th>Cặp hạt nhân</th><th style="width:15mm">${m('Z')}</th><th style="width:15mm">${m('N')}</th><th style="width:36mm">Đồng vị?</th></tr>
<tr><td>${m('{}^{16}_{8}\\mathrm{O}')} và ${m('{}^{17}_{8}\\mathrm{O}')}</td><td></td><td></td><td style="white-space:nowrap"><span class="ck"></span>Có &nbsp;<span class="ck"></span>Không</td></tr>
<tr><td>${m('{}^{14}_{6}\\mathrm{C}')} và ${m('{}^{14}_{7}\\mathrm{N}')}</td><td></td><td></td><td style="white-space:nowrap"><span class="ck"></span>Có &nbsp;<span class="ck"></span>Không</td></tr>
<tr><td>${m('{}^{3}_{1}\\mathrm{H}')} và ${m('{}^{3}_{2}\\mathrm{He}')}</td><td></td><td></td><td style="white-space:nowrap"><span class="ck"></span>Có &nbsp;<span class="ck"></span>Không</td></tr></table>

<h3><i>3</i>II.3 · Ba mô hình nguyên tử</h3>${tag('ô 3')}
<table><tr><th>Thomson</th><th>Rutherford</th><th>Bohr</th></tr>
<tr><td style="height:15mm"></td><td></td><td></td></tr></table>

<h3><i>4</i>II.4 · Kích thước hạt nhân và đơn vị u</h3>${tag('ô 4')}
<div class="card" style="padding:1.5mm 3mm">${m('R=')} <span class="fill" style="min-width:9mm"></span> · 10<sup><span class="fill" style="min-width:8mm"></span></sup> · ${m('A^{1/3}')} (m)<br>
${m('1\\ \\mathrm{u}\\approx')} <span class="fill" style="min-width:16mm"></span> kg ≈ <span class="fill" style="min-width:12mm"></span> ${m('\\mathrm{MeV}/c^2')} &nbsp;&nbsp; ${m('1\\ \\mathrm{MeV}=')} <span class="fill" style="min-width:16mm"></span> J</div>
<h3 style="margin-top:2mm"><i>5</i>Ghi chú thêm của em</h3>
<div style="background:#fff;border:.3mm solid var(--grid);border-radius:1.5mm;padding:0 2mm">${lines(3)}</div>
${foot(2)}</section>

<!-- TRANG 3 -->
<section class="page">
${head('BÀI TOÁN MẪU · ĐỌC NHÃN KIM LOẠI', 'Phân tích đề trước, tính sau')}
<h3><i>1</i>Đề bài</h3>${tag('trang 3')}
<div class="card soft">Mẫu kim loại ghi ${m('{}^{27}_{13}\\mathrm{Al}')}. Khối lượng mol nguyên tử nhôm là ${m('26{,}98')} g/mol; ${m('N_A=6{,}022\\cdot10^{23}\\ \\mathrm{mol}^{-1}')}.<br>
<b>a)</b> Xác định số prôtôn, số nơtron của hạt nhân nhôm. &nbsp;<b>b)</b> Tính bán kính hạt nhân nhôm. &nbsp;<b>c)</b> Tính khối lượng một nguyên tử nhôm ra u và ra kg. &nbsp;<b>d)</b> Hai đồng vị của đồng (${m('{}^{63}_{29}\\mathrm{Cu}')}, ${m('{}^{65}_{29}\\mathrm{Cu}')}) khác nhau ở đại lượng nào?</div>
<h3><i>2</i>Bảng phân tích đề <span class="hint">(dòng đầu đã làm mẫu)</span></h3>
<table><tr><th style="width:42mm">Câu trong đề</th><th style="width:36mm">Dữ liệu</th><th>Kiến thức liên quan</th></tr>
<tr><td>“${m('{}^{27}_{13}\\mathrm{Al}')}”</td><td>${m('A=27;\\ Z=13')}</td><td>${m('N=A-Z')}</td></tr>
<tr><td style="height:9mm">“bán kính hạt nhân”</td><td></td><td></td></tr>
<tr><td style="height:9mm">“khối lượng mol”</td><td></td><td></td></tr>
<tr><td style="height:9mm">“hai đồng vị của đồng”</td><td></td><td></td></tr></table>
<h3><i>3</i>Giải theo ba bước</h3>
<div class="steps">
<div><b>① Lấy dữ liệu</b><br>Gạch chân số liệu, đổi đơn vị nếu cần.</div>
<div><b>② Chọn công thức</b><br>Chữ trước, số sau.</div>
<div><b>③ Tính và kiểm</b><br>Đơn vị đúng chưa? Số hợp lí chưa?</div></div>
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:1mm 3mm;margin-top:1mm">
<b>a)</b>${lines(1)}<b>b)</b>${lines(2)}<b>c)</b>${lines(3)}<b>d)</b>${lines(1)}</div>
<div class="card soft" style="margin-top:2.5mm"><b>Em tự kiểm:</b> <span class="ck"></span>${m('N')} là số nguyên &nbsp;<span class="ck"></span>${m('R')} cỡ ${m('10^{-15}')} m &nbsp;<span class="ck"></span>có ghi đơn vị</div>
${foot(3)}</section>

<!-- TRANG 4 -->
<section class="page">
${head('BẪY VÀ TRẢ BÀI', 'Cuối bài: nói bằng lời của em trước, rồi mới mở sách đối chiếu')}
<h3><i>1</i>III · Ba cái bẫy hay sập <span class="hint">(đánh dấu bẫy em từng sập)</span></h3>${tag('ô 1')}
<div class="card">
<div class="trap"><span class="ck"></span><span><b>Lấy số khối làm khối lượng.</b> ${m('A')} là số đếm nuclôn, còn khối lượng nguyên tử tính bằng u là số thực (nhôm: ${m('26{,}98')} u).</span></div>
<div class="trap"><span class="ck"></span><span><b>“Đồng vị khác số prôtôn”.</b> Sai: đồng vị phải <b>cùng</b> ${m('Z')}.</span></div>
<div class="trap"><span class="ck"></span><span><b>Êlectron quay ở khoảng cách nào cũng được.</b> Bohr: chỉ ở quỹ đạo có năng lượng xác định.</span></div></div>
<h3><i>2</i>IV · Trả bài: 5 câu</h3>${tag('ô 2')}
<div style="background:#fff;border:.3mm solid var(--grid);border-radius:1.5mm;padding:1mm 3mm">
<div><b>1.</b> Hạt nhân gồm những hạt nào? Vì sao không vỡ ra?</div>${lines(2)}
<div><b>2.</b> Viết kí hiệu ${m('{}^{A}_{Z}\\mathrm{X}')}, nói rõ từng chữ.</div>${lines(2)}
<div><b>3.</b> Đồng vị là gì? Kể tên ba đồng vị của hiđrô, chúng giống và khác nhau ở đâu?</div>${lines(2)}
<div><b>4.</b> Thomson, Rutherford, Bohr khác nhau ở đâu?</div>${lines(2)}
<div><b>5.</b> Đơn vị u là gì? Viết công thức bán kính hạt nhân.</div>${lines(2)}</div>
<div style="display:flex;gap:3mm;align-items:center;margin-top:3mm" class="card soft">
<div class="qr">${qrSvg}</div>
<div><b>Học lại trên thachlab</b><br><span class="hint">Quét mã để mở thẳng phần Kiểm tra của bài 14 (cần đăng nhập thachlab).</span><br>
<span style="font-size:3mm">Em còn chưa chắc ở: ………………………………</span></div></div>
${foot(4)}</section>
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
