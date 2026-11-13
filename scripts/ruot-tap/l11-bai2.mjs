// Ruột tập VL11 – Bài 2 · Mô tả dao động điều hoà (lesson id 21). Quyển Chương 1 lớp 11: bài 1 = tr. 1–12, bài 2 = tr. 13–24.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự giải vào vở · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l11-bai2.mjs (toàn bộ SVG tự vẽ). Nội dung theo bài web (book/cache/21.json, tải từ DB 13/11/2026):
// mục tiêu, dự đoán quả lắc, II.1–II.5, thí nghiệm lò xo + năm lần đọc li độ, ba bẫy, Trả bài 6 câu, bài toán mẫu x = 6cos(πt + π/3),
// thử thách phân tầng, 5 dạng bài tập mẫu. Đáp số Bài tập mẫu + Bài tương tự tính bằng Python 13/11/2026 (math, radian).
// Chạy: node scripts/ruot-tap/l11-bai2.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl11-bai2.pdf
//       node scripts/ruot-tap/l11-bai2.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l11-bai2/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL11b2 as H } from './hinh-l11-bai2.mjs';

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
  const out = resolve(HERE, 'out/hinh-l11-bai2'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 2, lid: 21, ten: 'MÔ TẢ DAO ĐỘNG ĐIỀU HOÀ', lop: 11, baiDau: 1, sub: 'Vật lí 11 · Chương 1: Dao động' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const x = m('x'), A = m('A'), T = m('T'), w = m('\\omega'), ph = m('\\varphi'), t0 = m('t=0');
const pt = m('x=A\\cos(\\omega t+\\varphi)');

// Bài tương tự 1 cột, ô đáp số cuối dòng của ý (như l10-bai23); ô cao 6 mm để viết phân số có π.
// Ô đáp số Bài tập mẫu cao 9,5 mm (phân số 2π/3 viết tay cần ≥ 9 mm — checklist HS ảo).
const css = '<style>.bt>.gi{display:grid;grid-template-columns:1fr 1fr;column-gap:4mm}.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:5mm}.tt:has(.nhap-t) .hd>span+span{display:none}.bt .ans .fill{height:9.5mm}.bt:has(.d3x) .ans{grid-template-columns:1fr 1fr 1fr 2.3fr}.bt:has(.d4x) .ans>div:last-child{grid-column:span 2}.bt:has(.d5x) .ans{grid-template-columns:2fr 1fr 1fr}</style>';

const p1 = `${css}<section class="page">
${head('BÀI 2 · MÔ TẢ DAO ĐỘNG ĐIỀU HOÀ', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Viết ${pt}, gọi tên ${x}, ${A}, pha, ${ph}`)}
${dong(`${ck}Tính ${T}, ${m('f')}, ${w}; đọc ${ph}: lúc ${t0} vật ở đâu, sắp đi đâu`)}
${dong(`${ck}So sớm, trễ, đồng, ngược pha; đọc ${A}, ${T} trên đồ thị ${m('x')}–${m('t')}`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Hai bạn bấm giờ cùng một quả lắc ở hai lúc khác nhau. Đại lượng nào đổi?</p>
<div class="fig-side" style="${fs(40)}"><div>
${opt('A', 'Biên độ và chu kì đều đổi')}
${opt('B', `Chỉ pha ban đầu đổi; ${A}, ${T}, ${m('f')}, ${w} không đổi`)}
${opt('C', 'Tần số đổi vì người sau đếm ít nhịp hơn')}
${opt('D', 'Mọi đại lượng trong phương trình đều đổi')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 1)}</div>
${H.conLac()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f(12)} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Li độ và biên độ', '1·4')}
<div class="card" style="padding:1.2mm 3mm">
<div>Phương trình dao động điều hoà: ${nw(`${m('x=')} ${f(42)}`)}</div>
<div>${x}: ${f(25)}, độ lệch khỏi ${f(30)} (cm, m); có dấu.</div>
<div>${A}: ${f(25)}, là giá trị ${f(25)} của li độ, luôn dương.</div>
<div>Vật luôn nằm trong đoạn ${f(25)}; ${A} phụ thuộc ${f(30)}.</div>
<div>${m('\\omega t+\\varphi')}: ${f(25)} (rad) · ${ph}: ${f(25)} (rad) · ${w}: tần số góc (rad/s)</div></div>
${h3(5, 'Thí nghiệm: vật không ra khỏi đoạn [−A; A]', '1·5')}
<div class="card fig-side" style="${fs(40)};padding:1.2mm 3mm"><div>
<div><b>Làm:</b> kéo vật lệch ${nw('4 cm')} rồi thả; ${nw(`${m('T=2')} s`)}, ${nw(`${m('x=4\\cos(\\pi t)')} cm`)} (máy tính chế độ <b>rad</b>).</div>
<table class="tbl-ct" style="margin:.8mm 0"><tr><th>${m('t')} (s)</th><td>0</td><td>0,5</td><td>1,0</td><td>1,5</td></tr><tr><th>${m('x')} (cm)</th><td></td><td></td><td></td><td></td></tr></table>
<div><b>Rút ra:</b> ${x} trong đoạn ${f(25)} cm; ${nw(`${A} = ${f(12)} cm`)}</div>
${wl('Hai lần x = 0 trong bảng có giống nhau không? Vì sao?', 2)}</div>
${H.loXo()}</div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('CHU KÌ · TẦN SỐ · PHA BAN ĐẦU')}
${h3(1, 'II.2 · Chu kì, tần số, tần số góc', '2·1')}
<div class="card" style="padding:1.2mm 3mm">
<div>${T}: thời gian ${f(30)} (s), tức trở lại vị trí cũ theo ${f(25)}.</div>
<div>${m('f')}: số dao động trong ${f(14)} (Hz). &nbsp; ${nw(`${m('f=')} ${f(14)}`)} &nbsp;·&nbsp; ${nw(`${m('\\omega=')} ${f(14)} ${m('=')} ${f(14)}`)} &nbsp;(rad/s, luôn dương)</div>
<div>${T}, ${m('f')}, ${w} do ${f(25)}; ${A} do ${f(25)}. Với một vật, bốn đại lượng này ${ck}đổi ${ck}không đổi theo lúc nhìn.</div>
<div><b>Ví dụ:</b> đếm 20 dao động hết 16 s: ${nw(`${T} = ${f(12)} s`)} · ${nw(`${m('f')} = ${f(12)} Hz`)} · ${nw(`${w} = ${f(14)} rad/s`)}</div>
<div><b>Chú ý:</b> lấy ${m('\\omega/(2\\pi)')} được ${f(12)}, chưa phải ${T}.</div></div>
${h3(2, 'II.3 · Pha ban đầu', '2·2')}
<div class="card fig-side" style="${fs(44)};padding:1.2mm 3mm"><div>
<div>Pha ${m('\\omega t+\\varphi')} cho biết ${f(25)} của vật lúc ${m('t')}.</div>
<div>${ph} là pha lúc ${f(12)}; ${nw(`${ph} nằm trong ${f(16)}`)}; phụ thuộc cách kích thích và cách chọn ${f(25)}.</div>
<div>Trên vòng tròn: ${ph} là góc có hướng từ trục Ox tới ${f(25)} lúc ${t0}; dương nếu quay ${f(30)}.</div>
<div><b>Mẹo chiều:</b> tăng ${m('t')} một chút; ${x} giảm thì đi về phía âm, ${x} tăng thì đi về phía dương.</div>
<table style="margin-top:.8mm"><tr><th>Lúc ${t0}</th><th style="width:22mm">${ph}</th></tr>
<tr><td>ở biên dương, sắp về O</td><td></td></tr><tr><td>ở O, sắp sang phía dương</td><td></td></tr>
<tr><td>ở biên âm, sắp về O</td><td></td></tr><tr><td>ở O, sắp sang phía âm</td><td></td></tr></table></div>
${H.vongPha()}</div>
${h3(3, 'Làm nhanh', '2·3')}
${box(cau(`<b>Câu 1.</b> Vật thực hiện 30 dao động trong 12 s. Tính ${T}, ${m('f')}, ${w}.`, 3)
 + cau(`<b>Câu 2.</b> ${nw(`${m('x=5\\cos(4\\pi t+\\pi)')} cm`)}. Lúc ${t0} vật ở đâu, sắp đi về phía nào?`, 2)
 + cau(`<b>Câu 3.</b> Kéo vật lệch xa gấp đôi rồi thả: trong ${A}, ${T}, ${m('f')}, ${w}, ${ph}, đại lượng nào đổi? Vì sao?`, 2))}
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('ĐỘ LỆCH PHA · ĐỒ THỊ LI ĐỘ – THỜI GIAN')}
${h3(1, 'II.4 · Độ lệch pha', '3·1')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div>Hai dao động cùng ${w}: ${nw(`${m('\\Delta\\varphi=')} ${f(25)}`)} &nbsp;·&nbsp; ${nw(`${m('\\Delta t=')} ${f(16)}`)}</div>
<div>${m('x_1=A\\cos(\\omega t)')} và ${m('x_2=A\\cos(\\omega t-\\frac{\\pi}{2})')}: đỉnh của dao động ${f(12)} đến trước ${f(12)}.</div>
<table style="margin:.8mm 0"><tr><th style="width:31mm">Khi</th><th>Dao động 1 so với 2</th></tr>
<tr><td>${m('\\varphi_1\\gt\\varphi_2')}</td><td></td></tr><tr><td>${m('\\varphi_1\\lt\\varphi_2')}</td><td></td></tr>
<tr><td>${m('\\varphi_1=\\varphi_2')}</td><td></td></tr><tr><td>${m('\\varphi_1=\\varphi_2\\pm\\pi')}</td><td></td></tr></table>
<div>Hiệu lớn hơn ${m('\\pi')}: cộng hoặc trừ ${f(12)} rồi mới so.</div>
<div>Đổi lúc bắt đầu nhìn: độ lệch pha ${ck}đổi ${ck}không đổi.</div></div>
${H.lechPha()}</div>
${h3(2, 'II.5 · Đọc đồ thị x–t và thí nghiệm năm lần đọc', '3·2')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div>Độ cao đỉnh dương là ${f(12)}; hai đỉnh dương liên tiếp cách nhau ${f(12)}; trục hoành là ${f(25)}.</div>
<div><b>Làm:</b> ${nw('A = 5,0 cm')}, ${nw('T = 1,00 s')}, ${nw(`${m('\\varphi=0')}`)}; đọc thước (độ chia ${nw('0,1 cm')}) mỗi ${nw('0,10 s')}.</div>
<table style="margin:.8mm 0"><tr><th>${m('t')} (s)</th><td>0</td><td>0,10</td><td>0,20</td><td>0,30</td><td>0,40</td></tr>
<tr><th>${m('x')} tính (cm)</th><td>5,000</td><td>4,045</td><td>1,545</td><td>−1,545</td><td>−4,045</td></tr>
<tr><th style="height:6.5mm">${m('x')} đọc (cm)</th><td></td><td></td><td></td><td></td><td></td></tr></table>
<div>Sai số tuyệt đối ở ${nw('t = 0,10 s')}: ${nw(`${f(14)} cm`)}; do ${f(30)}.</div>
<div>Từ đồ thị bên: ${nw(`${A} = ${f(12)} cm`)} · ${nw(`${T} = ${f(12)} s`)}</div>
${wl('Mỗi 0,10 s, li độ đổi nhiều ở gần biên hay gần O?', 2)}</div>
${H.namCham()}</div>
${h3(3, 'III · Ba cái bẫy hay sập', '3·3')}
<div class="card" style="padding:1mm 3mm">
<div class="trap">${ck}<span><b>“Về giữa rồi nên li độ bằng 0, quãng đường cũng 0.”</b> Li độ có dấu, trong ${m('[-A;A]')}; quãng đường luôn dương, cộng dồn.</span></div>
<div class="trap">${ck}<span><b>“Thấy ${m('x=2')} cm thì ${m('A=2')} cm.”</b> Li độ đổi từng lúc; biên độ là cực đại của cả dao động.</span></div>
<div class="trap">${ck}<span><b>“Đổi mốc ${m('t=0')} thì độ lệch pha đổi.”</b> Mỗi pha cộng thêm cùng ${m('\\omega\\tau')}; hiệu giữ nguyên.</span></div></div>
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('TRẢ BÀI · TỰ KIỂM TRA · BÀI TOÁN MẪU')}
${h3(1, 'IV · Trả bài 6 câu', '4·1')}
${box(`${tb('1. Thế nào là dao động điều hoà? Viết phương trình.')}${lines(2)}
${tb(`2. ${x} và ${A} khác nhau thế nào? Vật nằm trong đoạn nào?`)}${lines(2)}
${tb(`3. Viết ${m('f')}, ${w} theo ${T}. Cái nào theo cấu tạo, cái nào theo cách kích thích?`)}${lines(2)}
${tb(`4. ${ph} cho biết gì? Nằm trong khoảng nào? Trên vòng tròn là góc nào?`)}${lines(2)}
${tb(`5. ${m('x_1=A\\cos(\\omega t)')}, ${m('x_2=A\\cos(\\omega t-\\pi/2)')}: ai sớm pha, lệch bao nhiêu?`)}${lines(1)}
${tb(`6. Khi nào sớm, trễ, đồng, ngược pha? Đọc ${A}, ${T} trên đồ thị thế nào?`)}${lines(2)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/6 câu · chưa thuộc: ${f(25)} ${nw(`${m('\\to')} đọc lại ô ${f(12)} Tập`)}</div>
${h3(2, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '4·2')}
${rkHai([1, 2, 3, 4], [5, 6, 7])}
${h3(3, 'V · Bài toán mẫu: đọc phương trình, viết dao động trễ pha', '4·3')}
<div class="card soft" style="padding:1.2mm 3mm">Một vật dao động điều hoà trên trục Ox: ${nw(`${m('x=6\\cos\\left(\\pi t+\\frac{\\pi}{3}\\right)')} cm`)}, ${m('t')} tính bằng giây.
<div><b>a)</b> Xác định ${A}, ${w}, ${ph}, rồi tính ${T} và ${m('f')}.</div><div><b>b)</b> Lúc ${t0}, vật ở đâu và sắp đi chiều nào?</div>
<div><b>c)</b> Viết phương trình dao động cùng ${A}, cùng ${w}, trễ pha ${m('\\pi/2')} so với dao động này.</div></div>
<table><tr><th style="width:50mm">Câu trong đề</th><th>Dữ liệu ${m('\\to')} kiến thức</th></tr>
<tr><td>“${m('x=6\\cos(\\pi t+\\pi/3)')} cm”</td><td>${A} = 6 cm; ${m('\\omega=\\pi')} rad/s; ${m('\\varphi=\\pi/3')} rad</td></tr>
<tr><td style="height:6.5mm">“tính ${T} và ${m('f')}”</td><td></td></tr>
<tr><td style="height:6.5mm">“lúc ${t0}”</td><td></td></tr>
<tr><td style="height:6.5mm">“trễ pha ${m('\\pi/2')}”</td><td></td></tr></table>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('GIẢI BÀI TOÁN MẪU · BÀI TẬP VỀ NHÀ · THỬ THÁCH')}
${h3(1, 'Giải bài toán mẫu', '5·1')}
<div class="fig-side" style="${fs(46)}"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl(`a) ${A}, ${w}, ${ph}; ${T}, ${m('f')}:`, 2)}${wl(`b) ${m('x_0=')} và chiều:`, 2)}${wl(`c) ${m("\\varphi'=")} và phương trình:`, 3)}${wl(`Kiểm tra: ${m('x_0')} trong ${m('[-6;6]')}? ${m("\\varphi'")} trong ${m('(-\\pi;\\pi]')}?`, 1)}</div>${H.mauVong()}</div>
${h3(2, `Điền bước còn thiếu: ${m('x=6\\cos(\\pi t)')} cm`, '5·2')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:.6mm 3mm">
<div class="ln" style="height:7mm"><b>Bước 1:</b> ${nw(`${m('T=2\\pi/\\omega=')} ${f(14)} s`)} &nbsp;·&nbsp; lúc ${t0} vật ở ${f(30)}</div>
<div class="ln" style="height:7mm"><b>Bước 2:</b> dao động trễ pha ${m('\\pi/2')} có ${nw(`${m("\\varphi'=")} ${f(14)}`)} &nbsp;${m('\\to')} ${nw(`${m("x'=")} ${f(40)}`)}</div></div>
${K.btvn().replace('<i>1</i>', '<i>3</i>')}
${h3(4, 'Thử thách phân tầng', '5·4')}
${box(wl(`${m('\\bigstar')} ${nw('A = 5 cm')}, ${nw('T = 2 s')}, ${m('\\varphi=0')}. Tính ${m('f')} và ${w}.`, 2)
 + wl(`${m('\\bigstar\\bigstar')} ${nw(`${m('x=3\\cos(4\\pi t+\\pi/6)')} cm`)}. Lúc ${t0}: li độ và chiều chuyển động?`, 3)
 + wl(`${m('\\bigstar\\bigstar\\bigstar')} ${m('\\varphi_1=\\pi/3')}, ${m('\\varphi_2=-\\pi/6')}, ${nw('T = 2 s')}. Ai sớm pha, lệch bao nhiêu (${m('\\Delta\\varphi')}, ${m('\\Delta t')})? Đổi mốc sang ${nw('t = 0,5 s')} thì độ lệch pha còn như cũ không?`, 4))}
${h3(5, 'VI · Mang về: điều em dễ quên nhất', '5·5')}
${box(wl('1.', 1) + wl('2.', 1) + wl('3.', 1))}
${foot(5)}</section>`;

const dang = [
  { t: `Dạng 1 · Dễ · Đọc phương trình: ${A}, ${w}, ${ph}, ${T}, ${m('f')} và li độ`,
    de: `${nw(`${m('x=8\\cos\\left(5\\pi t-\\frac{\\pi}{3}\\right)')} cm`)}, ${m('t')} tính bằng giây.<br><b>a)</b> biên độ ${A} (a<sub>1</sub>), tần số góc ${w} (a<sub>2</sub>), pha ban đầu ${ph} (a<sub>3</sub>)<br><b>b)</b> chu kì ${T} (b<sub>1</sub>), tần số ${m('f')} (b<sub>2</sub>)<br><b>c)</b> li độ lúc ${nw('t = 0,1 s')}`,
    nd: `So với ${pt}: dấu trừ trong ngoặc thuộc về ${f(12)}; thế ${m('t')} vào cả pha, máy tính để chế độ ${f(14)}`,
    a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'a<sub>3</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], gi: 2, cot: 6 },
  { t: 'Dạng 2 · Trung bình · Viết phương trình từ li độ và chiều lúc t = 0',
    de: `Vật dao động điều hoà với ${nw('A = 6 cm')}, ${nw('T = 0,5 s')}. Chọn ${t0} lúc vật ở ${nw(`${m('x=-3')} cm`)} và đang đi theo chiều dương.<br><b>a)</b> viết phương trình dao động<br><b>b)</b> kể từ ${t0}, sau bao lâu vật lần đầu tới biên dương`,
    nd: `${m('\\cos\\varphi=x_0/A')} cho ${f(12)} góc đối nhau; chọn dấu của ${ph} theo ${f(30)}`,
    a: ['a', 'b'], gi: 4, cot: 2 },
  { t: 'Dạng 3 · Trung bình · Độ lệch pha: sớm hay trễ, lệch bao lâu',
    de: `<div class="fig-side d3x" style="grid-template-columns:1fr 34mm"><div>${nw(`${m('x_1=3\\cos\\left(4\\pi t+\\frac{\\pi}{6}\\right)')} cm`)} và ${nw(`${m('x_2=5\\cos\\left(4\\pi t-\\frac{\\pi}{3}\\right)')} cm`)}.<br><b>a)</b> dao động nào sớm pha (a<sub>1</sub>), lệch pha bao nhiêu (a<sub>2</sub>)<br><b>b)</b> đỉnh dương của dao động sớm pha đến trước bao lâu<br><b>c)</b> viết ${m('x_3')} cùng biên độ với ${m('x_1')}, ngược pha với ${m('x_1')}</div>${H.haiBanKinh()}</div>`,
    nd: `${ph} lớn hơn thì ${f(16)} pha; ${nw(`${m('\\Delta t=')} ${f(14)}`)}; ngược pha: ${nw(`${m('\\varphi_3=\\varphi_1\\pm')} ${f(12)}`)}, ghi trong ${m('(-\\pi;\\pi]')}`,
    a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'], gi: 4 },
  { t: 'Dạng 4 · Khó · Đọc đồ thị li độ – thời gian rồi viết phương trình',
    de: `<span class="d4x"></span>Đồ thị ${m('x')}–${m('t')} của một vật dao động điều hoà ở hình bên.<br><b>a)</b> đọc biên độ ${A} (a<sub>1</sub>) và chu kì ${T} (a<sub>2</sub>)<br><b>b)</b> tính tần số góc ${w}<br><b>c)</b> xác định ${ph} (c<sub>1</sub>) và viết phương trình (c<sub>2</sub>)`,
    nd: `đỉnh cho ${f(12)}, hai đỉnh dương liên tiếp cho ${f(12)}; điểm lúc ${t0} cùng ${f(25)} cho ${ph}`,
    a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'], gi: 6, fig: H.doThiD4('') },
  { t: 'Dạng 5 · Khó · Đổi mốc thời gian: pha ban đầu đổi, nhịp giữ nguyên',
    de: `<span class="d5x"></span>Theo đồng hồ của An: ${nw(`${m('x=8\\cos\\left(2\\pi t-\\frac{5\\pi}{6}\\right)')} cm`)}. Bình bấm đồng hồ muộn hơn An ${nw('0,25 s')}: khi Bình chỉ ${m("t'=0")} thì An chỉ ${nw('t = 0,25 s')}.<br><b>a)</b> phương trình li độ theo đồng hồ của Bình<br><b>b)</b> lúc Bình bắt đầu bấm giờ: li độ (b<sub>1</sub>), chiều chuyển động (b<sub>2</sub>)<br><b>c)</b> so hai phương trình: đại lượng nào đổi (c<sub>1</sub>), đại lượng nào giữ nguyên (c<sub>2</sub>)`,
    nd: `bấm muộn ${m('\\tau')}: ${nw(`${m('t=t\'+')} ${f(12)}`)}, ${nw(`${m("\\varphi'=\\varphi+")} ${f(14)}`)}, rồi đưa ${m("\\varphi'")} về ${f(16)}`,
    a: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c<sub>1</sub>', 'c<sub>2</sub>'], gi: 5, fig: H.haiDongHo() },
];

// Bài tương tự giải vào vở (thầy chốt 10/11): 1 cột; ô đáp số cuối đúng dòng của ý, nhãn ô khớp a) b) c)…
// (a<sub>1</sub>, a<sub>2</sub> khi ý có nhiều kết quả). Đáp số tính bằng Python 13/11/2026.
const oY = (s, o, w = 25) => s.split('<br>').map((p) => {
  const y = p.match(/^<b>([a-d])\)<\/b>/);
  if (!y) return `<div>${p}</div>`;
  const ls = o.filter((l) => (Array.isArray(l) ? l[0] : l)[0] === y[1]);
  return `<div class="yo"><span>${p}</span><span class="oo">${ls.map((l) => { const [n, wd] = Array.isArray(l) ? l : [l, w]; return `<span class="nw"><b>${n})</b>${f(wd)}</span>`; }).join('')}</span></div>`;
}).join('');
const ttDe = (b) => b.fig ? `<div class="fig-side" style="grid-template-columns:1fr ${b.fw}mm"><div>${oY(b.de, b.o, b.ow)}</div>${b.fig}</div>` : oY(b.de, b.o, b.ow);
const vaoVo = (ds) => ds.map((b) => (b.o ? { t: b.t, de: ttDe(b), k: 0 } : b));
const nhap = (n) => ({ t: '<span class="nhap-t">Nháp / chỗ em còn vướng</span>', de: lines(n), k: 0 });
const s1 = 'a<sub>1</sub>', s2 = 'a<sub>2</sub>', s3 = 'a<sub>3</sub>';
const PT = 48; // ô phương trình (mm)
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–3', 'DẠNG 4–5'],
  trang: [[
    { t: `Dạng 1 · Bài 1 · ${nw(`${m('x=10\\cos\\left(4\\pi t+\\frac{\\pi}{6}\\right)')} cm`)}`, de: `<b>a)</b> ${A}, ${w}, ${ph}<br><b>b)</b> ${T}, ${m('f')}<br><b>c)</b> li độ lúc ${nw('t = 0,25 s')}`, o: [s1, s2, s3, 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], ow: 18 },
    { t: `Dạng 1 · Bài 2 · ${nw(`${m('x=5\\cos\\left(10\\pi t-\\frac{\\pi}{2}\\right)')} cm`)}`, de: `<b>a)</b> ${A}, ${w}, ${ph}<br><b>b)</b> ${T}, ${m('f')}<br><b>c)</b> li độ lúc ${nw('t = 0,05 s')}`, o: [s1, s2, s3, 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], ow: 18 },
    { t: 'Dạng 2 · Bài 1', de: `${nw('A = 4 cm')}, ${nw('T = 1 s')}. Chọn ${t0} lúc vật ở ${nw(`${m('x=2')} cm`)}, đang đi theo chiều âm.<br><b>a)</b> phương trình dao động<br><b>b)</b> kể từ ${t0}, sau bao lâu vật lần đầu tới biên âm`, o: [['a', PT], 'b'] },
    { t: 'Dạng 2 · Bài 2', de: `${nw('A = 10 cm')}, ${nw('T = 2 s')}. Chọn ${t0} lúc vật ở ${nw(`${m('x=-5')} cm`)}, đang đi theo chiều âm.<br><b>a)</b> phương trình dao động<br><b>b)</b> kể từ ${t0}, sau bao lâu vật lần đầu qua vị trí cân bằng O`, o: [['a', PT], 'b'] },
    { t: 'Dạng 3 · Bài 1', de: `${nw(`${m('x_1=4\\cos\\left(2\\pi t+\\frac{\\pi}{3}\\right)')} cm`)} và ${nw(`${m('x_2=6\\cos\\left(2\\pi t-\\frac{\\pi}{6}\\right)')} cm`)}.<br><b>a)</b> dao động nào sớm pha, lệch pha bao nhiêu<br><b>b)</b> đỉnh dương của dao động sớm pha đến trước bao lâu<br><b>c)</b> ${m('x_3')} cùng biên độ với ${m('x_2')}, ngược pha với ${m('x_2')}`, o: [s1, s2, 'b', ['c', PT]] },
    { t: 'Dạng 3 · Bài 2', de: `${nw(`${m('x_1=5\\cos\\left(\\pi t+\\frac{5\\pi}{6}\\right)')} cm`)} và ${nw(`${m('x_2=5\\cos\\left(\\pi t-\\frac{5\\pi}{6}\\right)')} cm`)}.<br><b>a)</b> hiệu ${m('\\varphi_1-\\varphi_2')} đưa về ${m('[-\\pi;\\pi]')}<br><b>b)</b> dao động nào sớm pha; sớm bao lâu<br><b>c)</b> ${m('x_3')} biên độ ${nw('2 cm')}, đồng pha với ${m('x_2')}`, fig: H.haiBanKinhTT(''), fw: 36, o: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', ['c', 40]], ow: 18 },
  ], [
    { t: 'Dạng 4 · Bài 1', de: `Đồ thị ${m('x')}–${m('t')} ở hình bên.<br><b>a)</b> ${A}, ${T}<br><b>b)</b> ${w}<br><b>c)</b> ${ph}<br><b>d)</b> phương trình`, fig: H.doThiTT1(''), fw: 50, o: [s1, s2, 'b', 'c', ['d', 44]], ow: 20 },
    { t: 'Dạng 4 · Bài 2', de: `Đồ thị ${m('x')}–${m('t')} ở hình bên.<br><b>a)</b> ${A}, ${T}<br><b>b)</b> ${w}<br><b>c)</b> ${ph}<br><b>d)</b> phương trình`, fig: H.doThiTT2(''), fw: 50, o: [s1, s2, 'b', 'c', ['d', 44]], ow: 20 },
    { t: 'Dạng 5 · Bài 1', de: `Theo đồng hồ An: ${nw(`${m('x=6\\cos\\left(4\\pi t+\\frac{\\pi}{3}\\right)')} cm`)}. Bình bấm giờ muộn hơn An ${nw('0,125 s')}.<br><b>a)</b> phương trình theo đồng hồ Bình<br><b>b)</b> lúc Bình bắt đầu bấm: li độ, chiều chuyển động<br><b>c)</b> đại lượng nào đã đổi`, o: [['a', PT], 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'] },
    { t: 'Dạng 5 · Bài 2', de: `Theo đồng hồ An: ${nw(`${m('x=4\\cos\\left(2\\pi t+\\frac{2\\pi}{3}\\right)')} cm`)}. Bình bấm giờ muộn hơn An ${nw('0,75 s')}.<br><b>a)</b> phương trình theo đồng hồ Bình (${m("\\varphi'")} trong ${m('(-\\pi;\\pi]')})<br><b>b)</b> li độ lúc ${m("t'=0")}<br><b>c)</b> theo đồng hồ Bình, lần đầu vật tới biên dương lúc nào`, o: [['a', PT], 'b', 'c'] },
    nhap(2),
  ]],
  dap: [
    `D1·1: a<sub>1</sub>) 10 cm · a<sub>2</sub>) ${m('4\\pi')} rad/s · a<sub>3</sub>) ${m('\\pi/6')} rad · b<sub>1</sub>) 0,5 s · b<sub>2</sub>) 2 Hz · c) ${m('-5\\sqrt3\\approx-8{,}66')} cm &nbsp;|&nbsp; D1·2: a<sub>1</sub>) 5 cm · a<sub>2</sub>) ${m('10\\pi')} rad/s · a<sub>3</sub>) ${m('-\\pi/2')} rad · b<sub>1</sub>) 0,2 s · b<sub>2</sub>) 5 Hz · c) 5 cm &nbsp;|&nbsp; D2·1: a) ${nw(`${m('x=4\\cos(2\\pi t+\\pi/3)')} cm`)} · b) ${m('1/3')} s ${m('\\approx')} 0,33 s &nbsp;|&nbsp; D2·2: a) ${nw(`${m('x=10\\cos(\\pi t+2\\pi/3)')} cm`)} · b) ${m('5/6')} s ${m('\\approx')} 0,83 s &nbsp;|&nbsp; D3·1: a<sub>1</sub>) ${m('x_1')} sớm pha · a<sub>2</sub>) ${m('\\pi/2')} rad · b) 0,25 s · c) ${nw(`${m('x_3=6\\cos(2\\pi t+5\\pi/6)')} cm`)} &nbsp;|&nbsp; D3·2: a) ${m('-\\pi/3')} rad · b<sub>1</sub>) ${m('x_2')} sớm pha · b<sub>2</sub>) ${m('1/3')} s ${m('\\approx')} 0,33 s · c) ${nw(`${m('x_3=2\\cos(\\pi t-5\\pi/6)')} cm`)}`,
    `D4·1: a<sub>1</sub>) 6 cm · a<sub>2</sub>) 1,2 s · b) ${m('5\\pi/3')} rad/s · c) ${m('-2\\pi/3')} rad · d) ${nw(`${m('x=6\\cos(5\\pi t/3-2\\pi/3)')} cm`)} &nbsp;|&nbsp; D4·2: a<sub>1</sub>) 5 cm · a<sub>2</sub>) 0,8 s · b) ${m('5\\pi/2')} rad/s · c) ${m('\\pi/2')} rad · d) ${nw(`${m('x=5\\cos(5\\pi t/2+\\pi/2)')} cm`)} &nbsp;|&nbsp; D5·1: a) ${nw(`${m("x=6\\cos(4\\pi t'+5\\pi/6)")} cm`)} · b<sub>1</sub>) ${m('-3\\sqrt3\\approx-5{,}20')} cm · b<sub>2</sub>) chiều âm · c) chỉ ${m('\\varphi')} đổi &nbsp;|&nbsp; D5·2: a) ${nw(`${m("x=4\\cos(2\\pi t'+\\pi/6)")} cm`)} · b) ${m('2\\sqrt3\\approx3{,}46')} cm · c) ${m("t'=11/12")} s ${m('\\approx')} 0,92 s`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 2], kq: [[1, 2, 3], [4, 5]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'li độ, biên độ 1·4 · thí nghiệm lò xo 1·5 · chu kì, tần số 2·1 · pha ban đầu 2·2 · lệch pha 3·1 · đồ thị x–t 3·2 · bẫy 3·3 · bài toán mẫu 4·3 · dạng 1–3 ở 6·1 · dạng 4–5 ở 7·1',
  out: process.argv[2],
});
