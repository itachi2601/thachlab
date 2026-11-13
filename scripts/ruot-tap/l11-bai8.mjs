// Ruột tập VL11 – Bài 8 · Mô tả sóng (lesson id 27). Quyển Chương 2 lớp 11 (bài 8–15): bài 8 = tr. 1–12.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự giải vào vở · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l11-bai8.mjs (toàn bộ SVG tự vẽ). Nội dung theo bài web (book/cache/27.json, tải từ DB 13/11/2026):
// mục tiêu, dự đoán làn sóng người, II.1–II.4, thí nghiệm khay nước + lò xo 240 fps, ba bẫy + bẫy phụ, Trả bài 6 câu,
// bài toán mẫu u_O = 2cos(40πt), thử thách phân tầng, 5 dạng bài tập mẫu. Đáp số Bài tập mẫu + Bài tương tự tính bằng Python 13/11/2026 (math, radian).
// Chạy: node scripts/ruot-tap/l11-bai8.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl11-bai8.pdf
//       node scripts/ruot-tap/l11-bai8.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l11-bai8/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL11b8 as H } from './hinh-l11-bai8.mjs';

if (process.argv[2] === '--hinh') {
  const { createRequire } = await import('node:module');
  const { existsSync, mkdirSync, writeFileSync } = await import('node:fs');
  const { dirname, resolve } = await import('node:path');
  const { fileURLToPath, pathToFileURL } = await import('node:url');
  const HERE = dirname(fileURLToPath(import.meta.url));
  const BOOK = [resolve(HERE, '../../book/'), '/Users/MAC/Projects/thachlab/book'].find((d) => existsSync(d + '/node_modules')) + '/';
  const puppeteer = createRequire(BOOK + 'package.json')('puppeteer-core');
  const F = resolve(HERE, 'fonts') + '/source-sans-3-';
  const css = ['latin', 'latin-ext', 'vietnamese'].flatMap((s) => [400, 700].map((w) => `@font-face{font-family:BV;font-weight:${w};src:url("${pathToFileURL(`${F}${s}-${w}-normal.woff2`).href}")}`)).join('')
    + 'body{margin:0;font-family:BV,sans-serif;zoom:4}.fig{margin:0;width:46mm;border:.3mm solid #d3dbec;border-radius:1.5mm;padding:1mm 1.5mm .6mm;background:#fff}.fig svg{display:block;width:100%;height:auto}figcaption{font-size:2.95mm;color:#5f6a88;line-height:1.3;margin-top:.4mm}';
  const out = resolve(HERE, 'out/hinh-l11-bai8'); mkdirSync(out, { recursive: true });
  const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true, args: ['--allow-file-access-from-files'] });
  const pg = await b.newPage();
  for (const [name, fn] of Object.entries(H)) {
    writeFileSync(out + '/_tmp.html', `<!doctype html><meta charset="utf-8"><link rel="stylesheet" href="${pathToFileURL(BOOK + 'node_modules/katex/dist/katex.min.css').href}"><style>${css}</style>${fn()}`);
    await pg.goto(pathToFileURL(out + '/_tmp.html').href, { waitUntil: 'networkidle0' });
    await pg.evaluate('document.fonts.ready');
    await (await pg.$('.fig')).screenshot({ path: `${out}/${name}.png` });
    console.log(`${name}.png`);
  }
  await b.close();
  process.exit(0);
}

const K = khoiTao({ bai: 8, lid: 27, ten: 'MÔ TẢ SÓNG', lop: 11, baiDau: 8, sub: 'Vật lí 11 · Chương 2: Sóng' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const L = m('\\lambda'), v = m('v'), T = m('T'), fq = m('f'), A = m('A'), w = m('\\omega'), d = m('d'), dp = m('\\Delta\\varphi');
const uM = m('u_M'), uO = m('u_O');

// Bài tương tự 1 cột, ô đáp số cuối dòng của ý (như l11-bai2); ô đáp số Bài tập mẫu cao 8 mm.
const css = '<style>.bt>.gi{display:grid;grid-template-columns:1fr 1fr;column-gap:4mm}.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo{line-height:1.2}.yo .fill{height:6mm}.tt:has(.nhap-t) .hd>span+span{display:none}.bt .ans .fill{height:9mm}.bt:has(.d4x) .ans>div:nth-child(3){grid-column:span 2}.bt:has(.d5x) .ans>div:nth-child(n+5){grid-column:span 2}.bt:has(.d5x) .ans{grid-template-columns:repeat(4,1fr)}</style>';

const p1 = `${css}<section class="page">
${head('BÀI 8 · MÔ TẢ SÓNG', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Chỉ ra khi có sóng, thứ gì truyền đi`)}
${dong(`${ck}Dùng ${m('\\lambda=vT=\\frac{v}{f}')}; viết ${uM} cách nguồn đoạn ${d}; tính độ lệch pha ${dp}`)}
${dong(`${ck}Phân biệt đồ thị ${m('u')}–${m('t')} (một điểm) với đồ thị ${m('u')}–${m('x')} (một lúc)`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Làn sóng người chạy hết khán đài. Thứ gì đã “đi” từ đầu này sang đầu kia?</p>
<div class="fig-side" style="${fs(44)}"><div>
${opt('A', 'Mọi khán giả đi sang đầu kia rồi quay về')}
${opt('B', 'Chỉ trạng thái đứng lên – ngồi xuống truyền đi')}
${opt('C', 'Không khí trong sân chảy thành một dòng')}
${opt('D', 'Cả khán đài rung lên rồi dừng lại')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 1)}</div>
${H.khanDai()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f(12)} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Sóng cơ và sự truyền sóng', '1·4')}
<div class="card" style="padding:1.2mm 3mm">
<div>Sóng cơ là ${f(30)} lan truyền trong một ${f(25)}.</div>
<div>Muốn có sóng cơ cần đủ hai thứ: ${f(30)} và ${f(40)}.</div>
<div>Sóng cơ không truyền được trong ${f(25)}, vì ở đó ${f(40)}.</div>
<div>Phần tử môi trường chỉ ${f(30)} quanh ${f(30)};</div>
<div>thứ lan ra xa là ${f(25)} và ${f(25)}.</div></div>
${h3(5, 'Thí nghiệm: khay nước và miếng xốp', '1·5')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div><b>Làm:</b> thả miếng xốp nhỏ C lên mặt nước trong khay; chấm đầu vật nhọn O xuống nước theo nhịp đều tay.</div>
<div><b>Quan sát:</b> gợn tròn lan ra từ O; miếng xốp C ${f(45)}; ngừng chấm, gợn ${ck}dừng ngay ${ck}lan tiếp rồi yếu dần.</div>
<div><b>Rút ra:</b> thứ lan ra xa là ${f(30)}, không phải ${f(25)}.</div>
${wl('Gõ nhẹ một đầu thước kẻ: mẩu tẩy trên thước có chạy ra xa không?', 1)}</div>
${H.khayNuoc()}</div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('NĂM ĐẠI LƯỢNG ĐẶC TRƯNG CỦA SÓNG')}
${h3(1, 'II.2 · Bảng tra nhanh', '2·1')}
<table style="margin-bottom:1mm"><tr><th style="width:37mm">Đại lượng, đơn vị</th><th>Nghĩa</th></tr>
<tr><td>Biên độ ${A} (m, cm)</td><td>độ lệch lớn nhất khỏi ${f(30)}</td></tr>
<tr><td>Chu kì ${T} (${f(12)})</td><td>thời gian một phần tử làm xong ${f(35)}</td></tr>
<tr><td>Tần số ${fq} (${f(12)})</td><td>số dao động toàn phần trong ${f(14)}; ${nw(`${m('f=')} ${f(12)}`)}</td></tr>
<tr><td>Bước sóng ${L} (m, cm)</td><td>(1) quãng đường sóng truyền được trong ${f(25)}<br>(2) khoảng cách gần nhất giữa hai điểm cùng phương truyền dao động ${f(25)}</td></tr>
<tr><td>Tốc độ truyền ${v} (m/s)</td><td>lan truyền ${f(25)}; phụ thuộc ${f(25)}</td></tr></table>
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div><b>Công thức:</b> ${nw(`${m('\\lambda=')} ${f(14)} ${m('=')} ${f(14)}`)} &nbsp;·&nbsp; ${nw(`${m('v=')} ${f(14)}`)}</div>
<div>Trên hình: đoạn (1) là ${f(25)}, đoạn (2) là ${f(25)}</div>
<div><b>Ví dụ:</b> sóng biển vỗ bờ mỗi 5 s, hai đỉnh liên tiếp cách 12 m: ${nw(`${T} = ${f(12)} s`)} · ${nw(`${L} = ${f(12)} m`)} · ${nw(`${v} = ${f(14)} m/s`)}</div></div>
${H.dayChup()}</div>
${h3(2, 'Hai điểm cùng phương truyền · Đổi môi trường', '2·2')}
<div class="card" style="padding:1.2mm 3mm">
<table style="margin-bottom:.8mm"><tr><th>Hai điểm gần nhau nhất (${m('k')} nguyên)</th><th style="width:26mm">Cách nhau</th></tr>
<tr><td>cùng pha: ${m('\\Delta\\varphi=2k\\pi')}</td><td></td></tr>
<tr><td>ngược pha: ${m('\\Delta\\varphi=(2k+1)\\pi')}</td><td></td></tr>
<tr><td>vuông pha: ${m('\\Delta\\varphi=(2k+1)\\frac{\\pi}{2}')}</td><td></td></tr>
<tr><td>đỉnh thứ nhất đến đỉnh thứ ${m('n')} (liên tiếp)</td><td></td></tr></table>
<div>Sang môi trường khác: giữ nguyên ${f(12)}; thay đổi ${f(12)} và ${f(12)} <span class="hint">(ghi kí hiệu)</span>.</div>
<div>Sóng cơ truyền nhanh nhất trong chất ${f(25)}, chậm nhất trong chất ${f(25)}.</div>
<div><b>Lò xo, quay 240 khung/s:</b> một điểm lên đỉnh lặp lại sau ${nw('48 khung')}; hai đỉnh liên tiếp cách ${nw('0,8 m')}: ${nw(`${T} = ${f(12)} s`)} · ${nw(`${v} = ${f(14)} m/s`)}</div></div>
${h3(3, 'Làm nhanh', '2·3')}
${box(cau(`<b>Câu 1.</b> Sóng có ${nw(`${m('T=0{,}4')} s`)}, truyền với ${nw(`${m('v=2{,}5')} m/s`)}. Tính bước sóng.`, 1)
 + `<div style="padding:1mm 0 .6mm"><b>Câu 2.</b> Sóng âm từ nước ra không khí: ${nw(`${fq} ${f(25)}`)} · ${nw(`${v} ${f(25)}`)} · ${nw(`${L} ${f(25)}`)} <span class="hint">(tăng / giảm / giữ nguyên)</span></div>`)}
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('PHƯƠNG TRÌNH SÓNG · ĐỒ THỊ SÓNG')}
${h3(1, 'II.3 · Độ trễ pha và phương trình sóng', '3·1')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div>Nguồn ${nw(`${m('u_O=A\\cos(\\omega t)')}`)}; sóng truyền theo chiều dương với tốc độ ${v}; M cách O đoạn ${d}.</div>
<div>Sóng mất ${nw(`${m('t_0=')} ${f(14)}`)} mới tới M; trước lúc đó M ${f(25)}.</div>
<div>${nw(`${m('u_M=A\\cos\\left[\\omega\\left(t-\\frac{d}{v}\\right)\\right]')}`)} ${m('\\Rightarrow')} ${nw(`${m('u_M=')} ${f(42)}`)}</div>
<div>M trễ pha so với O: ${nw(`${dp} ${m('=')} ${f(16)}`)}; điểm nào sóng tới sau thì ${ck}cộng ${ck}trừ pha.</div>
<div>Đi thêm ${L}: trễ thêm ${f(12)} · đi thêm ${m('\\frac{\\lambda}{2}')}: trễ ${f(12)}, hai điểm ${f(25)} pha.</div>
<div>Nguồn có pha ban đầu ${m('\\varphi_0')}: ${nw(`${m('u_M=A\\cos\\left(\\omega t+\\varphi_0-\\frac{2\\pi d}{\\lambda}\\right)')}`)}</div>
<div class="hint">${m('\\omega')}: tần số góc của nguồn (rad/s) · ${d}, ${L} cùng đơn vị (cm)</div></div>
${H.truyenOM()}</div>
${h3(2, 'II.4 · Hai loại đồ thị, đừng lẫn', '3·2')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<table style="margin-bottom:.8mm"><tr><th style="width:26mm">Đồ thị</th><th>Hai đỉnh liên tiếp cách nhau · đọc được gì</th></tr>
<tr><td>${m('u')}–${m('t')} (tại MỘT điểm)</td><td style="height:11mm"></td></tr>
<tr><td>${m('u')}–${m('x')} (tại MỘT lúc)</td><td style="height:11mm"></td></tr></table>
<div>Gặp đồ thị sóng, việc đầu tiên: đọc ${f(35)}</div>
<div>Trên ${m('u')}–${m('x')}, muốn biết chiều truyền: biết một điểm đang lên hay xuống, rồi thử ${f(45)}</div></div>
${H.haiTruc()}</div>
${h3(3, 'III · Ba cái bẫy hay sập', '3·3')}
<div class="card" style="padding:1mm 3mm">
<div class="trap">${ck}<span><b>“Sóng đến thì vật trôi theo sóng.”</b> Chiếc lá trên mặt hồ chỉ nhấp nhô tại chỗ; sóng mang pha và năng lượng đi.</span></div>
<div class="trap">${ck}<span><b>Lẫn hai chữ ${v}.</b> Tốc độ truyền ${v} do môi trường; tốc độ dao động cực đại ${nw(`${m('v_{max}=\\omega A')}`)} do nguồn. Không có “cái nào luôn lớn hơn”.</span></div>
<div class="trap">${ck}<span><b>Nhìn đồ thị, quên nhãn trục hoành.</b> Trục ${m('t')}: hai đỉnh cách ${T}; trục ${m('x')}: hai đỉnh cách ${L}.</span></div>
<div class="trap">${ck}<span><b>“Đổi môi trường thì tần số đổi.”</b> ${fq}, ${T} khoá theo nguồn; chỉ ${v} và ${L} đổi.</span></div></div>
<div style="margin-top:.4mm">${wl(`Sóng có ${nw('A = 2 cm')}, ${nw('f = 50 Hz')}, ${nw('v = 2 m/s')}: ${nw(`${m('v_{max}=')} ${f(16)} m/s`)}; so với ${v}:`, 1)}</div>
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('TRẢ BÀI · TỰ KIỂM TRA · BÀI TOÁN MẪU')}
${h3(1, 'IV · Trả bài 6 câu', '4·1')}
${box(`${tb('1. Sóng cơ là gì? Cần điều kiện nào? Vì sao không truyền trong chân không?')}${lines(1)}
${tb(`2. Viết các công thức liên hệ ${L}, ${T}, ${fq}, ${v} và đơn vị.`)}${lines(1)}
${tb('3. Phát biểu hai định nghĩa của bước sóng.')}${lines(1)}
${tb(`4. M cách nguồn O đoạn ${d} theo chiều truyền: trễ pha bao nhiêu? Viết ${uM}.`)}${lines(2)}
${tb('5. Sóng sang môi trường khác: đại lượng nào đổi, đại lượng nào không? Vì sao?')}${lines(1)}
${tb(`6. Đồ thị ${m('u')}–${m('t')} và ${m('u')}–${m('x')} khác nhau ở đâu? Mỗi loại cho biết gì?`)}${lines(1)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/6 câu · chưa thuộc: ${f(25)} ${nw(`${m('\\to')} đọc lại ô ${f(12)} Tập`)}</div>
${h3(2, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '4·2')}
${rkHai([1, 2, 3], [4, 5, 6])}
${h3(3, 'V · Bài toán mẫu: đọc đề đến đâu, gọi kiến thức đến đó', '4·3')}
<div class="card soft fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>Sóng truyền trên mặt nước từ nguồn O theo chiều dương trục Ox với tốc độ ${nw(`${m('v=60')} cm/s`)}. Nguồn O dao động theo ${nw(`${m('u_O=2\\cos(40\\pi t)')} cm`)}.
<div><b>a)</b> Tính chu kì, tần số và bước sóng.</div><div><b>b)</b> Viết phương trình dao động của điểm M cách O ${nw('9 cm')}.</div>
<div><b>c)</b> Tại ${nw(`${m('t=0{,}1625')} s`)}, M có li độ bao nhiêu và đang đi theo chiều nào?</div>
<div><b>d)</b> So sánh tốc độ truyền sóng với tốc độ dao động cực đại của phần tử nước.</div></div>${H.mauOM()}</div>
<table><tr><th style="width:44mm">Câu trong đề</th><th>Dữ liệu ${m('\\to')} kiến thức</th></tr>
<tr><td>“theo chiều dương trục Ox”</td><td>sóng tới sau thì trừ pha: dùng dấu ${m('-')}</td></tr>
<tr><td style="height:6.5mm">“${m('u_O=2\\cos(40\\pi t)')} cm”</td><td></td></tr>
<tr><td style="height:6.5mm">“M cách O 9 cm”</td><td></td></tr>
<tr><td style="height:6.5mm">“tại ${m('t=0{,}1625')} s”</td><td></td></tr>
</table>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('GIẢI BÀI TOÁN MẪU · BÀI TẬP VỀ NHÀ · THỬ THÁCH')}
${h3(1, 'Giải bài toán mẫu', '5·1')}
${box(`${wl(`a) ${fq}, ${T}, ${L}:`, 2)}${wl(`b) ${dp} và ${uM}:`, 2)}${wl(`c) sóng đã tới M chưa? ${uM} và dấu vận tốc ${m('v_M=-\\omega A\\sin(\\text{pha})')}:`, 3)}${wl(`d) ${m('v_{max}=\\omega A=')} &nbsp; so với ${v}:`, 2)}${wl(`Kiểm tra: 9 cm gấp mấy lần ${L}? có khớp câu b không?`, 1)}`, 'padding:0 3mm')}
${h3(2, `Điền bước còn thiếu: ${nw(`${m('v=80')} cm/s`)}, ${nw(`${m('f=20')} Hz`)}, N cách O ${nw('9 cm')}`, '5·2')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:.6mm 3mm">
<div class="ln" style="height:7mm"><b>Bước 1:</b> ${nw(`${m('\\lambda=\\frac{v}{f}=')} ${f(14)} cm`)} &nbsp;·&nbsp; ${nw(`${m('\\frac{d}{\\lambda}=')} ${f(14)}`)}</div>
<div class="ln" style="height:7mm"><b>Bước 2:</b> ${nw(`${m('\\Delta\\varphi=\\frac{2\\pi d}{\\lambda}=')} ${f(16)}`)} &nbsp;·&nbsp; bỏ vòng ${m('2\\pi')} trọn còn ${f(14)} ${m('\\to')} N và O ${f(25)}</div></div>
${K.btvn().replace('<i>1</i>', '<i>3</i>')}
${h3(4, 'Thử thách phân tầng', '5·4')}
<div class="fig-side" style="${fs(44)}">${box(wl(`${m('\\bigstar')} ${nw(`${m('T=0{,}4')} s`)}, ${nw(`${m('\\lambda=2')} m`)}. Tính ${v}.`, 2)
 + wl(`${m('\\bigstar\\bigstar')} M, N cùng phương truyền cách nhau ${m('\\frac{3\\lambda}{4}')}. Lệch pha bao nhiêu?`, 2)
 + wl(`${m('\\bigstar\\bigstar\\bigstar')} Hình bên: ngay sau đó P đi lên hay đi xuống? Q thì sao? Vì sao?`, 3))}${H.suon()}</div>
${h3(5, 'VI · Mang về: điều em dễ quên nhất', '5·5')}
${box(wl('1.', 1) + wl('2.', 1) + wl('3.', 1))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Đếm ngọn sóng: chu kì, tần số, tốc độ truyền',
    de: `Phao trên mặt hồ nhô lên ${nw('9 lần')} (tính từ lần đầu đến lần thứ chín) trong ${nw('20 s')}; khoảng cách giữa hai ngọn sóng liên tiếp là ${nw('4,5 m')}.<br><b>a)</b> chu kì ${T} (a<sub>1</sub>) và tần số ${fq} (a<sub>2</sub>)<br><b>b)</b> tốc độ truyền sóng ${v}`,
    nd: `${m('n')} lần nhô lên có ${f(14)} chu kì; hai ngọn liên tiếp cách ${f(12)}; ${nw(`${m('v=')} ${f(12)}`)}`,
    a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b'], gi: 4 },
  { t: 'Dạng 2 · Trung bình · Hai điểm: lệch pha, khoảng cách',
    de: `Sóng truyền trên dây từ M tới N, ${nw(`${m('v=1{,}2')} m/s`)}, ${nw(`${m('f=20')} Hz`)}; ${nw('MN = 10,5 cm')}.<br><b>a)</b> bước sóng<br><b>b)</b> độ lệch pha giữa M và N (b<sub>1</sub>); cùng, ngược hay vuông pha (b<sub>2</sub>)<br><b>c)</b> điểm P gần M nhất, dao động ngược pha với M, cách M bao nhiêu`,
    nd: `đổi ${v} ra ${f(12)}; lập tỉ số ${nw(`${m('\\frac{d}{\\lambda}=')} ${f(12)}`)}; ngược pha gần nhất: ${nw(`${m('d=')} ${f(12)}`)}`,
    a: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], gi: 4, fig: H.dayMN() },
  { t: 'Dạng 3 · Trung bình · Đọc phương trình sóng',
    de: `${nw(`${m('u=5\\cos(8\\pi t-0{,}2\\pi x)')} (cm)`)}, ${m('x')} tính bằng cm, ${m('t')} tính bằng s.<br><b>a)</b> biên độ (a<sub>1</sub>), chu kì (a<sub>2</sub>), tần số (a<sub>3</sub>)<br><b>b)</b> bước sóng (b<sub>1</sub>), tốc độ truyền sóng theo m/s (b<sub>2</sub>)<br><b>c)</b> tốc độ dao động cực đại của phần tử dây (c<sub>1</sub>); lớn hơn hay nhỏ hơn ${v} (c<sub>2</sub>)`,
    nd: `so với ${nw(`${m('u=A\\cos\\left(\\omega t-\\frac{2\\pi x}{\\lambda}\\right)')}`)}: hệ số của ${m('x')} là ${f(12)}; ${L} cùng đơn vị ${f(12)}`,
    a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'a<sub>3</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c<sub>1</sub>', 'c<sub>2</sub>'], gi: 4 },
  { t: 'Dạng 4 · Khó · Phương trình tại M, li độ và chiều chuyển động',
    de: `<span class="d4x"></span>Nguồn O: ${nw(`${m('u_O=4\\cos\\left(20\\pi t-\\frac{\\pi}{2}\\right)')} (cm)`)}, bắt đầu dao động lúc ${m('t=0')}; sóng truyền theo chiều dương Ox với ${nw('1,5 m/s')}, biên độ không đổi. M cách O ${nw('20 cm')}.<br><b>a)</b> chu kì (a<sub>1</sub>) và bước sóng (a<sub>2</sub>)<br><b>b)</b> phương trình dao động của M<br><b>c)</b> tại ${nw(`${m('t=0{,}15')} s`)}: li độ của M (c<sub>1</sub>), chiều chuyển động (c<sub>2</sub>)`,
    nd: `kiểm sóng đã tới M: ${nw(`${m('t\\ge\\frac{d}{v}=')} ${f(14)} s`)}; chiều theo dấu ${nw(`${m('v_M=-\\omega A\\sin(\\text{pha})')}`)}`,
    a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'], gi: 6 },
  { t: 'Dạng 5 · Khó · Đọc hai đồ thị u–x và u–t, viết phương trình',
    de: `<span class="d5x"></span>Sóng hình sin truyền theo chiều dương Ox. Hình (a): li độ theo toạ độ ${m('x')} lúc ${m('t=0')}; hình (b): li độ theo thời gian của điểm M có ${nw(`${m('x_M=6')} cm`)}.<br><b>a)</b> biên độ (a<sub>1</sub>), bước sóng (a<sub>2</sub>), chu kì (a<sub>3</sub>)<br><b>b)</b> tốc độ truyền sóng<br><b>c)</b> phương trình dao động của M<br><b>d)</b> phương trình của N cách M ${nw('9 cm')} theo chiều truyền sóng`,
    nd: `đọc nhãn trục hoành trước: hình (a) cho ${f(12)}, hình (b) cho ${f(12)}; lúc ${m('t=0')} M ở đâu cho ${m('\\varphi_0')}; N tới sau nên ${f(25)}`,
    a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'a<sub>3</sub>', 'b', 'c', 'd'], gi: 7, fig: H.d5() },
];

// Bài tương tự giải vào vở (thầy chốt 10/11): 1 cột; ô đáp số cuối đúng dòng của ý, nhãn ô khớp a) b) c)…
const oY = (s, o, w = 25) => s.split('<br>').map((p) => {
  const ys = [...p.matchAll(/<b>([a-d])\)<\/b>/g)].map((x) => x[1]);
  if (!p.startsWith('<b>') || !ys.length) return `<div>${p}</div>`;
  const ls = o.filter((l) => ys.includes((Array.isArray(l) ? l[0] : l)[0]));
  return `<div class="yo"><span>${p}</span><span class="oo">${ls.map((l) => { const [n, wd, h] = Array.isArray(l) ? l : [l, w]; return `<span class="nw"><b>${n})</b>${h ? f(wd).replace('style="', `style="height:${h}mm;`) : f(wd)}</span>`; }).join('')}</span></div>`;
}).join('');
const ttDe = (b) => b.fig ? `<div class="fig-side" style="grid-template-columns:1fr ${b.fw}mm"><div>${oY(b.de, b.o, b.ow)}</div>${b.fig}</div>` : oY(b.de, b.o, b.ow);
const vaoVo = (ds) => ds.map((b) => (b.o ? { t: b.t, de: ttDe(b), k: 0 } : b));
const nhap = (n) => ({ t: '<span class="nhap-t">Nháp / chỗ em còn vướng</span>', de: lines(n), k: 0 });
const s = (c, i) => `${c}<sub>${i}</sub>`;
const PT = 46; // ô phương trình (mm)
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–3', 'DẠNG 4–5'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Phao nhô lên ${nw('11 lần')} (từ lần đầu đến lần cuối) trong ${nw('20 s')}; khoảng cách giữa ${nw('3 ngọn sóng')} liên tiếp là ${nw('6 m')}.<br><b>a)</b> chu kì, tần số, bước sóng; <b>b)</b> tốc độ truyền`, o: [s('a', 1), s('a', 2), s('a', 3), 'b'], ow: 18 },
    { t: 'Dạng 1 · Bài 2', de: `Thuyền nhô lên ${nw('5 lần')} (từ lần đầu đến lần cuối) trong ${nw('16 s')}; khoảng cách giữa ${nw('5 ngọn sóng')} liên tiếp là ${nw('12 m')}.<br><b>a)</b> chu kì, tần số, bước sóng; <b>b)</b> tốc độ truyền`, o: [s('a', 1), s('a', 2), s('a', 3), 'b'], ow: 18 },
    { t: 'Dạng 2 · Bài 1', de: `Sóng truyền trên dây từ M tới N, ${nw(`${m('v=0{,}8')} m/s`)}, ${nw(`${m('f=10')} Hz`)}; ${nw('MN = 22 cm')}.<br><b>a)</b> bước sóng<br><b>b)</b> độ lệch pha giữa M, N; cùng, ngược hay vuông pha<br><b>c)</b> điểm gần M nhất dao động cùng pha với M cách M bao nhiêu`, o: ['a', s('b', 1), [s('b', 2), 25], 'c'], ow: 20 },
    { t: 'Dạng 2 · Bài 2', de: `Sóng truyền trên dây từ M tới N, ${nw(`${m('v=2')} m/s`)}, ${nw(`${m('f=50')} Hz`)}; ${nw('MN = 10 cm')}.<br><b>a)</b> bước sóng<br><b>b)</b> độ lệch pha giữa M, N; cùng, ngược hay vuông pha<br><b>c)</b> điểm gần M nhất dao động vuông pha với M cách M bao nhiêu`, o: ['a', s('b', 1), [s('b', 2), 25], 'c'], ow: 20 },
    { t: `Dạng 3 · Bài 1 · ${nw(`${m('u=4\\cos(10\\pi t-0{,}5\\pi x)')} (cm)`)}, ${m('x')}: cm, ${m('t')}: s`, de: `<b>a)</b> biên độ, chu kì, tần số<br><b>b)</b> bước sóng; tốc độ truyền sóng (m/s)<br><b>c)</b> ${m('v_{max}')} của phần tử (cm/s); lớn hơn hay nhỏ hơn ${v}`, o: [s('a', 1), s('a', 2), s('a', 3), s('b', 1), s('b', 2), [s('c', 1), 26], [s('c', 2), 25]], ow: 16 },
    { t: `Dạng 3 · Bài 2 · ${nw(`${m('u=2\\cos\\left(20\\pi t-\\frac{\\pi x}{15}\\right)')} (cm)`)}, ${m('x')}: cm, ${m('t')}: s`, de: `<b>a)</b> biên độ, chu kì, tần số<br><b>b)</b> bước sóng; tốc độ truyền sóng (m/s)<br><b>c)</b> ${m('v_{max}')} của phần tử (cm/s); lớn hơn hay nhỏ hơn ${v}`, o: [s('a', 1), s('a', 2), s('a', 3), s('b', 1), s('b', 2), [s('c', 1), 26], [s('c', 2), 25]], ow: 16 },
  ], [
    { t: 'Dạng 4 · Bài 1', de: `Nguồn O: ${nw(`${m('u_O=5\\cos(10\\pi t)')} (cm)`)}, từ ${m('t=0')}; sóng truyền theo +Ox, ${nw('v = 40 cm/s')}, biên độ không đổi. M cách O ${nw('6 cm')}.<br><b>a)</b> chu kì, bước sóng; <b>b)</b> phương trình của M<br><b>c)</b> tại ${nw(`${m('t=0{,}2')} s`)}: li độ của M, chiều chuyển động`, o: [[s('a', 1), 14], [s('a', 2), 16], ['b', PT, 9], [s('c', 1), 20], [s('c', 2), 25]], ow: 20 },
    { t: 'Dạng 4 · Bài 2', de: `Nguồn O: ${nw(`${m('u_O=6\\cos\\left(4\\pi t+\\frac{\\pi}{3}\\right)')} (cm)`)}, từ ${m('t=0')}; sóng truyền theo +Ox, ${nw('v = 0,6 m/s')}, biên độ không đổi. M cách O ${nw('10 cm')}.<br><b>a)</b> chu kì, bước sóng; <b>b)</b> phương trình của M<br><b>c)</b> tại ${nw(`${m('t=0{,}5')} s`)}: li độ của M, chiều chuyển động`, o: [[s('a', 1), 14], [s('a', 2), 16], ['b', PT, 9], [s('c', 1), 20], [s('c', 2), 25]], ow: 20 },
    { t: 'Dạng 5 · Bài 1', de: `Sóng truyền theo chiều dương Ox. (a): ${m('u')}–${m('x')} lúc ${m('t=0')}; (b): ${m('u')}–${m('t')} của M (${nw(`${m('x_M=5')} cm`)}).<br><b>a)</b> biên độ, bước sóng, chu kì<br><b>b)</b> tốc độ truyền sóng<br><b>c)</b> phương trình của M<br><b>d)</b> phương trình của N (sau M ${nw('5 cm')})`, fig: H.tt51(), fw: 44, o: [s('a', 1), s('a', 2), s('a', 3), 'b', ['c', PT, 9], ['d', PT, 9]], ow: 14 },
    { t: 'Dạng 5 · Bài 2', de: `Sóng truyền theo chiều dương Ox. (a): ${m('u')}–${m('x')} lúc ${m('t=0')}; (b): ${m('u')}–${m('t')} của M (${nw(`${m('x_M=10')} cm`)}).<br><b>a)</b> biên độ, bước sóng, chu kì<br><b>b)</b> tốc độ truyền sóng<br><b>c)</b> phương trình của M<br><b>d)</b> phương trình của N (sau M ${nw('10 cm')})`, fig: H.tt52(), fw: 44, o: [s('a', 1), s('a', 2), s('a', 3), 'b', ['c', PT, 9], ['d', PT, 9]], ow: 14 },
  ]],
  dap: [
    `D1·1: a<sub>1</sub>) 2 s · a<sub>2</sub>) 0,5 Hz · a<sub>3</sub>) 3 m · b) 1,5 m/s &nbsp;|&nbsp; D1·2: a<sub>1</sub>) 4 s · a<sub>2</sub>) 0,25 Hz · a<sub>3</sub>) 3 m · b) 0,75 m/s &nbsp;|&nbsp; D2·1: a) 8 cm · b<sub>1</sub>) ${m('5{,}5\\pi')} rad · b<sub>2</sub>) vuông pha · c) 8 cm &nbsp;|&nbsp; D2·2: a) 4 cm · b<sub>1</sub>) ${m('5\\pi')} rad · b<sub>2</sub>) ngược pha · c) 1 cm &nbsp;|&nbsp; D3·1: a) 4 cm; 0,2 s; 5 Hz · b) 4 cm; 0,2 m/s · c<sub>1</sub>) ${m('40\\pi\\approx125{,}7')} cm/s · c<sub>2</sub>) lớn hơn &nbsp;|&nbsp; D3·2: a) 2 cm; 0,1 s; 10 Hz · b) 30 cm; 3 m/s · c<sub>1</sub>) ${m('40\\pi\\approx125{,}7')} cm/s · c<sub>2</sub>) nhỏ hơn`,
    `D4·1: a) 0,2 s; 8 cm · b) ${nw(`${m('u_M=5\\cos\\left(10\\pi t-\\frac{3\\pi}{2}\\right)')} cm`)} ${m('=5\\cos\\left(10\\pi t+\\frac{\\pi}{2}\\right)')} · c<sub>1</sub>) 0 (vị trí cân bằng) · c<sub>2</sub>) chiều âm &nbsp;|&nbsp; D4·2: a) 0,5 s; 30 cm · b) ${nw(`${m('u_M=6\\cos\\left(4\\pi t-\\frac{\\pi}{3}\\right)')} cm`)} · c<sub>1</sub>) 3 cm · c<sub>2</sub>) chiều dương &nbsp;|&nbsp; D5·1: a) 4 cm; 20 cm; 0,5 s · b) 40 cm/s · c) ${nw(`${m('u_M=4\\cos(4\\pi t)')} cm`)} · d) ${nw(`${m('u_N=4\\cos\\left(4\\pi t-\\frac{\\pi}{2}\\right)')} cm`)} &nbsp;|&nbsp; D5·2: a) 2 cm; 40 cm; 0,2 s · b) 2 m/s · c) ${nw(`${m('u_M=2\\cos\\left(10\\pi t-\\frac{\\pi}{2}\\right)')} cm`)} · d) ${nw(`${m('u_N=2\\cos(10\\pi t-\\pi)')} cm`)}`,
  ],
};


// Số + đơn vị không gãy dòng (lỗi HS ảo 13/11): thay dấu cách bằng &nbsp; trong phần chữ (ngoài thẻ).
const U = /(\d) (s|m|Hz|cm|mm|m\/s|cm\/s|rad|lần|ngọn|khung|fps)(?![\p{L}\/])/gu;
const nbU = (x) => typeof x === 'string' ? x.split(/(<[^>]*>)/).map((t) => (t.startsWith('<') ? t : t.replace(U, '$1&nbsp;$2'))).join('')
  : Array.isArray(x) ? x.map(nbU) : x && typeof x === 'object' ? Object.fromEntries(Object.entries(x).map(([k, v]) => [k, nbU(v)])) : x;

await K.dung(nbU({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 2], kq: [[1, 2, 3], [4, 5]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'sóng cơ 1·4 · khay nước 1·5 · năm đại lượng 2·1 · lệch pha, đổi môi trường 2·2 · phương trình sóng 3·1 · đồ thị u–t, u–x 3·2 · bẫy 3·3 · bài toán mẫu 4·3 · dạng 1–3 ở 6·1 · dạng 4–5 ở 7·1',
  out: process.argv[2],
}));
