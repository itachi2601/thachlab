// Dựng ruột tập Vật lí 12 – Bài 14 (8 trang 165×240 mm, ô ly 5 mm; trang 6–7 là mẫu Sửa bài sau đề, trang 8 ghi chú tự do). Chạy: node scripts/ruot-tap/bai14.mjs [file.pdf]
// Mặc định ghi scripts/ruot-tap/out/ruot-tap-vl12-bai14.pdf. Cần book/node_modules (katex, qrcode-generator, puppeteer-core):
// worktree không có thì dùng book/ của bản chính ~/Projects/thachlab.
// Mã ô "Tập: trang · ô" (nhãn Web … trên giấy = tên mục trên web) trùng data-tap trong content/lesson-samples/l12-hat-nhan-mo-hinh-nguyen-tu/theory.src.html.
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
const lines = (n) => Array.from({ length: n }, () => '<div class="ln"></div>').join('');
// n dòng kẻ chấm, nhãn (a), b)…) nằm ngay đầu dòng đầu để không tốn thêm một dòng
const wl = (label, n) => `<div class="ln"><b>${label}</b></div>` + lines(n - 1);

// Nhãn góc phải: mã "trang·ô" trùng nhãn "✍ Tập: trang · ô" khi trình chiếu (data-tap trong theory.src.html).
const tag = (t) => `<span class="tag">Tập ${t}</span>`;
const foot = (n) => `<div class="foot"><span>Vật lí thầy Thạch · thachlab.id.vn</span><span>Bài 14 · trang ${n}/8</span></div>`;
// who=true chỉ ở trang 1 và trang Sửa bài (tập đóng sẵn, không lặp Ngày/Tên mỗi trang)
const head = (t, s, who = false) => `<div class="top"><div><b>${t}</b><small>${s}</small></div>${who ? '<div class="who">Ngày …../….. &nbsp;Tên: ………………</div>' : ''}</div>`;
const kw = (h) => `<div class="kw">🔑 ${h}</div>`;
const yn = `<td style="white-space:nowrap;padding:.2mm 1.8mm"><span class="ck"></span>Có &nbsp;<span class="ck"></span>Không</td>`;
const box = (inner, extra = '') => `<div style="background:#fff;border:.3mm solid var(--grid);border-radius:1.5mm;padding:1mm 3mm;${extra}">${inner}</div>`;
const rkRow = (i) => `<tr><td><b>${i}</b></td><td></td><td><span class="ck"></span></td><td><span class="ck"></span></td></tr>`;
const rkTable = (rows) => `<table class="rk"><tr><th style="width:9mm">Câu</th><th>Em chọn</th><th style="width:15mm">Chắc?</th><th style="width:15mm">Đúng?</th></tr>${rows}</table>`;

// Trang "Sửa bài sau đề trên lớp": một đề một trang, 8 hàng câu sai, giải lại câu sai nhất, hẹn làm lại (retrieval cách quãng).
const errRow = () => `<tr><td></td><td></td><td><span class="ck"></span>đọc đề <span class="ck"></span>nhớ sai<br><span class="ck"></span>tính <span class="ck"></span>chưa học</td><td></td></tr>`;
const fixPage = (n, lan) => `<section class="page">
${head(`SỬA BÀI SAU ĐỀ TRÊN LỚP · ${lan}`, 'Sửa trong 24 giờ: ghi vì sao sai, không chỉ chép đáp án', true)}
<div class="card soft" style="display:flex;gap:4mm;flex-wrap:wrap"><span>Đề: ……………………………</span><span>Điểm: ……/……</span><span>Sai: P.I …… · P.II …… · P.III ……</span></div>
<h3><i>1</i>Câu sai và lí do <span class="hint">(mỗi câu một hàng)</span></h3>
<table class="er"><tr><th style="width:12mm">Câu</th><th style="width:22mm">Chọn → Đúng</th><th style="width:40mm">Loại lỗi</th><th>Cần xem lại (Tập ô …)</th></tr>${errRow().repeat(8)}</table>
<h3><i>2</i>Giải lại câu sai nhất <span class="hint">(chữ trước, số sau)</span></h3>
${box(wl('Câu …:', 6))}
<h3><i>3</i>Bẫy mới em phát hiện · câu hỏi cho thầy/trợ giảng</h3>
${box(wl('Bẫy:', 2) + wl('Hỏi:', 2))}
<div class="card soft" style="margin-top:2mm"><b>Làm lại các câu sai (không nhìn lời giải):</b> <span style="white-space:nowrap"><span class="ck"></span>sau 2 ngày</span> &nbsp;<span style="white-space:nowrap"><span class="ck"></span>sau 1 tuần</span> &nbsp;<span style="white-space:nowrap"><span class="ck"></span>trước kiểm tra chương</span> · lần cuối đúng ……/……</div>
${foot(n)}</section>`;

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
.top{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:.5mm solid var(--navy);padding-bottom:1mm;margin-bottom:2mm;background:#fff}
.top b{display:block;font-weight:800;font-size:4.6mm;color:var(--navy)}.top small{color:var(--hint);font-size:2.9mm}
.who{font-size:3mm;color:var(--hint);white-space:nowrap}
h3{margin:1.8mm 0 1mm;line-height:1.25;font-weight:800;font-size:3.9mm;color:var(--navy);background:#fff;display:inline-block;padding-right:2mm}
h3 i{font-style:normal;background:var(--navy);color:#fff;border-radius:1mm;padding:.2mm 1.6mm;margin-right:1.5mm;font-size:3.2mm}
.card{background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:1.6mm 3mm;margin-bottom:1.5mm}
.card.soft{background:var(--soft);border-color:var(--grid)}
.hint{color:var(--hint);font-size:2.9mm}
.opt{display:flex;gap:2mm;margin:.8mm 0}.opt .b{width:4.6mm;height:4.6mm;border:.3mm solid var(--navy);border-radius:50%;flex:none;text-align:center;font-size:2.8mm;line-height:4.2mm;font-weight:700;color:var(--navy)}
.ln{height:5mm;border-bottom:.2mm dotted var(--hint);background:#fff}
.two{display:grid;grid-template-columns:1fr 1fr;gap:3mm}
.box{border:.3mm solid var(--navy);background:#fff;border-radius:1.5mm}
.fill{display:inline-block;min-width:18mm;border-bottom:.3mm solid var(--navy);height:4mm;vertical-align:baseline}
table{border-collapse:collapse;width:100%;background:#fff;font-size:3.3mm}
th,td{border:.3mm solid var(--navy);padding:.7mm 1.8mm;vertical-align:top}
th{background:var(--soft);font-weight:700;text-align:left}
.ck{display:inline-block;width:4.8mm;height:4.8mm;border:.3mm solid var(--navy);border-radius:.7mm;vertical-align:-1.1mm;margin-right:1mm}
.mo td{height:35mm;vertical-align:top;font-size:2.8mm;color:var(--hint)}.mo td div{border-bottom:.2mm dotted var(--grid);margin-top:7mm}.mo td div:first-child{margin-top:0;padding-bottom:11mm}
.er td,.er th{padding:.6mm 1.2mm;height:11mm;font-size:2.9mm;vertical-align:middle;line-height:4.2mm}.er th{height:auto;text-align:center}.er .ck{margin:0 .6mm 0 0;vertical-align:middle}
.rk td,.rk th{padding:0 1mm;height:5mm;line-height:3.6mm;font-size:3mm;text-align:center;vertical-align:middle}.rk .ck{margin:0;vertical-align:middle}
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:2mm;margin:2mm 0}
.steps div{background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:1.5mm 2mm;font-size:3.1mm}
.steps b{color:var(--navy)}
.foot{position:absolute;left:14mm;right:12mm;bottom:5mm;display:flex;justify-content:space-between;font-size:2.7mm;color:var(--hint);background:#fff;padding:0 1mm}
.big{font-size:7mm;text-align:center;padding:0}
.qr{width:29mm;height:29mm;padding:2mm;background:#fff;border:.3mm solid var(--grid);flex:none}.qr svg{width:25mm;height:25mm;display:block}
.tag{position:absolute;right:12mm;margin:1.6mm 0 0;border-radius:1mm;padding:.2mm 2mm;background:var(--navy);color:#fff;font-size:3.2mm;font-weight:700;line-height:4.6mm}
.kw{margin:1.1mm 0;font-size:3.4mm}
.trap{display:flex;gap:2mm;align-items:flex-start;margin:1mm 0}
</style></head><body>

<!-- TRANG 1: mục tiêu, dự đoán, II.1 -->
<section class="page">
${head('BÀI 14 · HẠT NHÂN VÀ NGUYÊN TỬ', 'Vật lí 12 · Chương 4: Vật lí hạt nhân', true)}
<h3><i>1</i>Hôm nay em làm được gì?</h3>${tag('1·1')}
<div class="card soft">
<div style="margin:.3mm 0"><span class="ck"></span>Nêu được hạt nhân gồm <b>prôtôn, nơtron</b> và lực giữ chúng lại</div>
<div style="margin:.3mm 0"><span class="ck"></span>Đọc và viết đúng kí hiệu ${m('{}^{A}_{Z}\\mathrm{X}')}, tính số nơtron</div>
<div style="margin:.3mm 0"><span class="ck"></span>Nói được <b>đồng vị</b> là gì; phân biệt 3 mô hình nguyên tử</div>
</div>
<h3><i>2</i>Dự đoán trước khi học <span class="hint">(đoán sai cũng không sao)</span></h3>${tag('1·2')}
<div class="card">
<p style="margin:0 0 1.5mm">Năm 1909, Rutherford bắn chùm hạt alpha vào lá vàng mỏng. Phần lớn hạt bay thẳng qua; một phần tám nghìn hạt lệch mạnh, vài hạt <b>bật ngược lại</b>. Theo em, nguyên tử:</p>
<div class="opt"><span class="b">A</span><span>Là khối cầu đặc, các hạt phân bố đều</span></div>
<div class="opt"><span class="b">B</span><span>Không có hạt nhân, chỉ có các êlectron</span></div>
<div class="opt"><span class="b">C</span><span>Gần như trống rỗng, điện dương tập trung ở một vùng rất nhỏ</span></div>
<div style="margin-top:1.5mm">Em chọn: <span class="fill" style="min-width:10mm"></span> &nbsp;<span class="ck"></span>chắc &nbsp;<span class="ck"></span>không chắc &nbsp;· <span class="hint">Vì sao em nghĩ vậy?</span></div>${lines(1)}
</div>
<h3><i>3</i>Học xong, em sửa lại <span class="hint">(bút khác màu)</span></h3>${tag('1·3')}
<div class="card soft"><div>Đáp án đúng là: <span class="fill"></span> &nbsp; Em đoán <span class="ck"></span>đúng &nbsp;<span class="ck"></span>sai</div>
<div class="hint" style="margin-top:1mm">Điều em hiểu sai hoặc mới biết:</div>${lines(2)}</div>
<h3><i>4</i>II.1 · Hạt nhân, lực hạt nhân, kí hiệu</h3>${tag('1·4')}
<div class="card" style="padding:1.2mm 3mm">
${kw(`Prôtôn · Nơtron · Nuclôn · Lực hạt nhân rất <span class="fill"></span>`)}
<div>Lực hạt nhân: rất <span class="fill" style="min-width:14mm"></span>, thắng lực <span class="fill" style="min-width:20mm"></span>, chỉ trong phạm vi <span style="white-space:nowrap"><span class="fill" style="min-width:16mm"></span> m.</span></div>
${kw(`${m('A')} trên · ${m('Z')} <span class="fill"></span> · ${m('N=A-Z')}`)}
<div style="display:grid;grid-template-columns:26mm 1fr;gap:3mm;align-items:center;margin-top:1mm">
<div class="big">${m('{}^{A}_{Z}\\mathrm{X}')}</div>
<div>
<div>${m('A')} (trên) = số <span class="fill" style="min-width:14mm"></span> = <span class="fill" style="min-width:14mm"></span> + <span class="fill" style="min-width:14mm"></span></div>
<div>${m('Z')} (dưới) = số <span class="fill" style="min-width:20mm"></span> &nbsp; ${m('N')} = <span class="fill" style="min-width:8mm"></span> − <span class="fill" style="min-width:8mm"></span></div>
</div></div></div>
<div class="card" style="padding:1mm 3mm"><b>Tự kiểm tra 1.</b> ${m('{}^{65}_{29}\\mathrm{Cu}')} có:<div class="two" style="margin:0"><div><b>A.</b> 65 prôtôn, 29 nơtron</div><div><b>B.</b> 29 nuclôn, 36 nơtron</div><div><b>C.</b> 29 prôtôn, 36 nơtron</div><div><b>D.</b> 29 prôtôn, 65 nơtron</div></div>
Em chọn: <span class="fill"></span> <span class="ck"></span>chắc &nbsp; Vì ${m('N=A-Z=')} <span class="fill" style="min-width:25mm"></span></div>
${foot(1)}</section>

<!-- TRANG 2: II.2–II.4, kết quả tự kiểm tra -->
<section class="page">
${head('GHI BÀI · ĐỒNG VỊ, MÔ HÌNH, KÍCH THƯỚC', 'Điền vào chỗ trống khi nghe giảng, đừng chép lại cả câu')}
<h3><i>1</i>II.2 · Đồng vị</h3>${tag('2·1')}
<div class="card" style="margin-bottom:1.5mm;padding:1.2mm 3mm">${kw(`Cùng ${m('Z')} · Khác <span class="fill"></span> · Cùng tính chất hoá học`)}
<div>Đồng vị: cùng số <span class="fill" style="min-width:14mm"></span>, khác số <span class="fill" style="min-width:14mm"></span>; tính chất <span class="fill" style="min-width:20mm"></span> giống nhau.</div>
<div style="margin-top:1mm">Ba đồng vị của hiđrô: ${m('{}^{1}_{1}\\mathrm{H}')}, ${m('{}^{2}_{1}\\mathrm{H}')} (<span class="fill" style="min-width:14mm"></span>), ${m('{}^{3}_{1}\\mathrm{H}')} (<span class="fill" style="min-width:14mm"></span>): cùng <span class="fill" style="min-width:8mm"></span> prôtôn, số nơtron <span class="fill" style="min-width:6mm"></span> / <span class="fill" style="min-width:6mm"></span> / <span class="fill" style="min-width:6mm"></span></div></div>
<table><tr><th>Cặp hạt nhân</th><th style="width:15mm">${m('Z')}</th><th style="width:15mm">${m('N')}</th><th style="width:36mm">Đồng vị?</th></tr>
<tr><td>${m('{}^{12}_{6}\\mathrm{C}')} và ${m('{}^{14}_{6}\\mathrm{C}')}</td><td></td><td></td>${yn}</tr>
<tr><td>${m('{}^{40}_{18}\\mathrm{Ar}')} và ${m('{}^{40}_{20}\\mathrm{Ca}')}</td><td></td><td></td>${yn}</tr>
<tr><td>${m('{}^{35}_{17}\\mathrm{Cl}')} và ${m('{}^{37}_{17}\\mathrm{Cl}')}</td><td></td><td></td>${yn}</tr></table>

<h3><i>2</i>II.3 · Ba mô hình nguyên tử</h3>${tag('2·2')}
<div class="card" style="padding:1.2mm 3mm;margin-bottom:1mm">${kw(`Vỏ êlectron · Hạt nhân nhỏ <span class="fill"></span> · Quỹ đạo lượng tử hoá`)}</div>
<table class="mo"><tr><th>Thomson 1904</th><th>Rutherford 1911</th><th>Bohr 1913</th></tr>
<tr><td><div>Hình:</div><div>Điểm mới:</div><div>Bị bác bỏ / còn thiếu:</div></td><td><div>Hình:</div><div>Điểm mới:</div><div>Bị bác bỏ / còn thiếu:</div></td><td><div>Hình:</div><div>Điểm mới:</div><div>Bị bác bỏ / còn thiếu:</div></td></tr></table>

<h3><i>3</i>II.4 · Kích thước hạt nhân và đơn vị u</h3>${tag('2·3')}
<div class="card" style="padding:1.2mm 3mm">${kw(`Đo bằng <span class="fill"></span> · ${m('R')} theo căn bậc <span class="fill"></span> ${m('A')}`)}
<div>${m('R=')} <span class="fill" style="min-width:9mm"></span> · 10<sup><span class="fill" style="min-width:11mm;height:3.6mm"></span></sup> · ${m('A^{1/3}')} (m)</div>
<div>${m('1\\ \\mathrm{u}')} = <span class="fill" style="min-width:8mm"></span> khối lượng nguyên tử <span class="fill" style="min-width:12mm"></span> ≈ <span class="fill" style="min-width:22mm"></span> kg ≈ <span class="fill" style="min-width:16mm"></span> ${m('\\mathrm{MeV}/c^2')}</div>
<div>${m('1\\ \\mathrm{MeV}=')} <span class="fill" style="min-width:22mm"></span> J</div></div>
<h3><i>4</i>Kết quả tự kiểm tra <span class="hint">(câu 2–7 trên web; câu 1 đã ghi ở Tập 1·4)</span></h3>${tag('2·4')}
<div class="two">${rkTable(rkRow(2) + rkRow(3) + rkRow(4))}${rkTable(rkRow(5) + rkRow(6) + rkRow(7))}</div>
<div class="hint" style="margin-top:1mm">Chắc mà vẫn sai → chỗ cần xem lại nhất.</div>
${foot(2)}</section>

<!-- TRANG 3: bẫy, trả bài -->
<section class="page">
${head('BẪY VÀ TRẢ BÀI', 'Nói bằng lời của em trước, rồi mới bấm xem đáp án trên web')}
<h3><i>1</i>III · Ba cái bẫy hay sập <span class="hint">(đánh dấu bẫy em từng sập)</span></h3>${tag('3·1')}
<div class="card">
<div class="trap"><span class="ck"></span><span><b>Lấy số khối làm khối lượng.</b> ${m('A')} là số đếm nuclôn, còn khối lượng nguyên tử tính bằng u là số thực (nhôm: ${m('26{,}98')} u).</span></div>
<div class="trap"><span class="ck"></span><span><b>“Đồng vị khác số prôtôn”.</b> Sai: đồng vị phải <b>cùng</b> ${m('Z')}.</span></div>
<div class="trap"><span class="ck"></span><span><b>Êlectron quay ở khoảng cách nào cũng được.</b> Bohr: chỉ ở quỹ đạo có năng lượng xác định.</span></div></div>
<h3><i>2</i>IV · Trả bài: 5 câu</h3>${tag('3·2')}
${box(`<div><b>1.</b> Hạt nhân gồm những hạt nào? Vì sao không vỡ ra?</div>${lines(2)}
<div><b>2.</b> Viết kí hiệu ${m('{}^{A}_{Z}\\mathrm{X}')}, nói rõ từng chữ.</div>${lines(2)}
<div><b>3.</b> Đồng vị là gì? Kể tên ba đồng vị của hiđrô, chúng giống và khác nhau ở đâu?</div>${lines(3)}
<div><b>4.</b> Thomson, Rutherford, Bohr khác nhau ở đâu?</div>${lines(3)}
<div><b>5.</b> Đơn vị u là gì? Viết công thức bán kính hạt nhân.</div>${lines(2)}`)}
<div class="card soft" style="display:flex;gap:3mm;align-items:flex-start;margin-top:2mm">
<div style="width:34mm;flex:none"><div class="qr">${qrSvg}</div>
<div class="hint" style="margin-top:1mm">Quét mã: phần Kiểm tra của bài 14 trên thachlab (cần đăng nhập).</div></div>
<div style="flex:1"><b>Ghi chú thêm của em</b> <span class="hint">(điều thầy nhấn mạnh, chỗ còn lấn cấn)</span>${lines(8)}</div></div>
${foot(3)}</section>

<!-- TRANG 4: bài toán mẫu -->
<section class="page">
${head('BÀI TOÁN MẪU · ĐỌC NHÃN KIM LOẠI', 'Phân tích đề trước, tính sau')}
<h3><i>1</i>V · Đề bài</h3>${tag('4')}
<div class="card soft" style="padding:1.2mm 3mm">Mẫu kim loại ghi ${m('{}^{27}_{13}\\mathrm{Al}')}. Khối lượng mol nguyên tử nhôm là ${m('26{,}98')} g/mol; ${m('N_A=6{,}022\\cdot10^{23}\\ \\mathrm{mol}^{-1}')}.<br>
<b>a)</b> Xác định số prôtôn, số nơtron của hạt nhân nhôm. &nbsp;<b>b)</b> Tính bán kính hạt nhân nhôm. &nbsp;<b>c)</b> Tính khối lượng một nguyên tử nhôm ra u và ra kg. &nbsp;<b>d)</b> Hai đồng vị của đồng (${m('{}^{63}_{29}\\mathrm{Cu}')}, ${m('{}^{65}_{29}\\mathrm{Cu}')}) khác nhau ở đại lượng nào?</div>
<h3><i>2</i>Bảng phân tích đề <span class="hint">(dòng đầu đã làm mẫu)</span></h3>
<table><tr><th style="width:42mm">Câu trong đề</th><th style="width:36mm">Dữ liệu</th><th>Kiến thức liên quan</th></tr>
<tr><td>“${m('{}^{27}_{13}\\mathrm{Al}')}”</td><td>${m('A=27;\\ Z=13')}</td><td>${m('N=A-Z')}</td></tr>
<tr><td style="height:6.5mm">“bán kính hạt nhân”</td><td></td><td></td></tr>
<tr><td style="height:6.5mm">“khối lượng mol”</td><td></td><td></td></tr>
<tr><td style="height:6.5mm">“ra đơn vị u”</td><td></td><td></td></tr>
<tr><td style="height:6.5mm">“hai đồng vị của đồng”</td><td></td><td></td></tr></table>
<h3><i>3</i>Giải <span class="hint">① lấy dữ liệu, đổi đơn vị → ② chữ trước, số sau → ③ kiểm đơn vị, số hợp lí</span></h3>
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm;margin-top:1mm">
${wl('a)', 3)}${wl('b)', 3)}${wl('c)', 4)}${wl('d)', 2)}
<div class="ln" style="height:auto;padding-top:1mm;font-size:3.1mm"><b>Điền bước còn thiếu</b> · Bước 1 (cho sẵn): đồng có khối lượng mol ${m('63{,}54')} g/mol; ${m('R_{\\mathrm{Cu}}=1{,}2\\cdot10^{-15}\\cdot63^{1/3}\\approx4{,}8\\cdot10^{-15}')} m.</div>
${wl(`Bước 2: m(Cu) = 63,54 / ${m('N_A')} = … g = … kg`, 2)}${wl('Bước 3: đổi sang u = … ; so với 63 và 65:', 3)}</div>
<div class="card soft" style="margin-top:1.5mm;padding:1mm 3mm"><b>Em tự kiểm:</b> <span class="ck"></span>${m('N')} là số nguyên &nbsp;<span class="ck"></span>${m('R')} cỡ ${m('10^{-15}')} m &nbsp;<span class="ck"></span>có ghi đơn vị</div>
${foot(4)}</section>

<!-- TRANG 5: mang về, thử thách, mô phỏng -->
<section class="page">
${head('MANG VỀ · THỬ THÁCH · MÔ PHỎNG', 'Viết không nhìn web, rồi mới đối chiếu')}
<h3><i>1</i>VI · Mang về <span class="hint">(mỗi dòng một ý, bằng lời của em)</span></h3>${tag('5')}
${box(wl('Hạt nhân:', 2) + wl('Lực hạt nhân:', 2) + wl('Kí hiệu:', 2) + wl('Đồng vị:', 2) + wl('Mô hình:', 2) + wl('Kích thước:', 2) + wl('Khối lượng:', 2) + wl('Đọc đề:', 1))}
<h3><i>2</i>Thử thách phân tầng <span class="hint">(tính ra giấy rồi mới bấm xem)</span></h3>
${box(wl('⭐ He-4: prôtôn, nơtron?', 1) + wl('⭐⭐ Vì sao nơtron làm hạt nhân bền hơn?', 3) + wl('⭐⭐⭐ Hạt nhân vàng chiếm bao nhiêu phần thể tích nguyên tử?', 6))}
<h3><i>3</i>Câu 7 (urani) và mô phỏng PhET</h3>
${box(wl(`Câu 7 (${m('{}^{238}_{92}\\mathrm{U}')}): em chọn … · A, Z, N =`, 2)
 + wl('Bắn hạt alpha (Rutherford) · Dự đoán:', 1) + wl('Thấy:', 2)
 + wl('Đồng vị neon · Dự đoán trung bình gần đồng vị nào:', 1) + wl('Thấy / vì sao 20,18:', 2))}
${foot(5)}</section>

${fixPage(6, 'Lần 1')}${fixPage(7, 'Lần 2')}

<!-- TRANG 8: ghi chú tự do -->
<section class="page">
${head('GHI CHÚ TỰ DO', 'Sơ đồ, công thức thầy viết thêm, điều muốn hỏi')}
<div class="card soft"><b>Câu hỏi còn lại cho thầy / trợ giảng:</b>${lines(3)}</div>
${foot(8)}</section>
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
