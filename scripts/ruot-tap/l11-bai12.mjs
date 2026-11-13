// Ruột tập VL11 – Bài 12 · Giao thoa sóng (lesson id 31). Quyển Chương 2 lớp 11: bài 8 = tr. 1–12 … bài 12 = tr. 49–60.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự giải vào vở · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l11-bai12.mjs (toàn bộ SVG tự vẽ). Nội dung theo bài web (book/cache/31.json, tải từ DB 13/11/2026):
// mục tiêu, dự đoán hai loa, II.1–II.4 (nguồn kết hợp, cực đại/cực tiểu, trên đoạn AB, khe Young + hai bức xạ), thí nghiệm khay sóng,
// laser, bịt một loa, bẫy, Trả bài 6 câu, bài toán mẫu f = 20 Hz, AB = 10 cm, 5 dạng bài tập mẫu. Đáp số tính bằng Python 13/11/2026.
// Chạy: node scripts/ruot-tap/l11-bai12.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl11-bai12.pdf
//       node scripts/ruot-tap/l11-bai12.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l11-bai12/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL11b12 as H } from './hinh-l11-bai12.mjs';

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
  const out = resolve(HERE, 'out/hinh-l11-bai12'); mkdirSync(out, { recursive: true });
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


const K = khoiTao({ bai: 12, lid: 31, ten: 'GIAO THOA SÓNG', lop: 11, baiDau: 8, sub: 'Vật lí 11 · Chương 2: Sóng' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const fT = (w) => `<span class="fill" style="min-width:${w}mm;height:9mm"></span>`; // ô cao cho phân số viết tay (≥ 9 mm)
const L = m('\\lambda'), d21 = m('d_2-d_1'), k0 = m('k');
const um = (s) => nw(`${s} ${m('\\mu\\text{m}')}`);

const css = '<style>.bt>.gi{display:grid;grid-template-columns:1fr 1fr;column-gap:4mm}.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:5mm}.tt:has(.nhap-t) .hd>span+span{display:none}.bt .ans .fill{height:8.5mm}.tbl-cc td{height:6.5mm}.tbl-dem td{height:9.5mm}</style>';

const p1 = `${css}<section class="page">
${head('BÀI 12 · GIAO THOA SÓNG', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Nêu ba điều kiện để hai nguồn là hai nguồn kết hợp`)}
${dong(`${ck}Dùng hiệu đường đi ${d21} để xét cực đại, cực tiểu; đếm số điểm trên đoạn AB`)}
${dong(`${ck}Dùng ${m('i=\\lambda D/a')}: tính khoảng vân, bước sóng; xét vân sáng hay vân tối`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Hai loa cùng phát một bản nhạc. Em đi chậm dọc hàng ghế đầu. Em nghe thấy gì?</p>
<div class="fig-side" style="${fs(42)}"><div>
${opt('A', 'Chỗ nào cũng to hơn khi chỉ bật một loa')}
${opt('B', 'Chỗ to, chỗ nhỏ, xen kẽ nhau')}
${opt('C', 'Chỗ nào cũng nghe như khi chỉ bật một loa')}
${opt('D', 'Càng gần loa càng to, xa ra nhỏ dần')}
<div style="margin-top:1mm">${chon(12)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 1)}</div>
${H.haiLoa()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f(12)} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Giao thoa và hai nguồn kết hợp', '1·4')}
<div class="card" style="padding:1.2mm 3mm">
<div><b>Giao thoa:</b> hai sóng gặp nhau, tạo ra ${f(70)}</div>
<div><b>Vân giao thoa:</b> ${f(95)}</div>
<div><b>Hai nguồn kết hợp</b> (Phương – Tần – Pha): cùng ${f(25)} · cùng ${f(25)}</div>
<div>· độ lệch pha ${f(40)}</div>
<div>Thiếu một điều kiện thì ${f(60)}</div>
<div>Ví dụ hai nguồn kết hợp: hai loa ${f(50)}</div></div>
${h3(5, 'Thí nghiệm: khay sóng hai mũi nhọn', '1·5')}
<div class="card fig-side" style="${fs(42)};padding:1.2mm 3mm"><div>
<div><b>Làm:</b> gắn hai mũi nhọn vào cùng một cần rung, cho chạm mặt nước, bật rung. Sau đó nhấc một mũi lên.</div>
${wl('Quan sát (hai mũi cùng rung):', 2)}${wl('Quan sát (nhấc một mũi):', 1)}${wl('Rút ra: chỉ có vân giao thoa khi', 2)}</div>
${H.khay()}</div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('CỰC ĐẠI · CỰC TIỂU · HIỆU ĐƯỜNG ĐI')}
${h3(1, 'II.2 · Cực đại và cực tiểu (hai nguồn cùng pha)', '2·1')}
<div class="card fig-side" style="${fs(34)};padding:1.2mm 3mm"><div>
<div>Hiệu đường đi: ${d21}; ${m('d_1')}, ${m('d_2')}: từ M tới ${f(25)}</div>
<div>Hiệu ${m('k\\lambda')}: tới M trễ ${f(12)} chu kì ${m('\\to')} hai sóng ${f(25)}</div>
<div>Hiệu ${m('(k+\\tfrac12)\\lambda')}: trễ ${f(12)} chu kì ${m('\\to')} hai sóng ${f(25)}</div>
<div><b>Nhắc (Bài 8):</b> ${nw(m('\\lambda=v/f'))} · ${m('k=0,\\pm1,\\pm2,\\dots')} · ${m('a')}: biên độ mỗi sóng tới M</div></div>
${H.diemM()}</div>
<div class="fig-side" style="${fs(46)}"><div>
<table class="tbl-cc"><tr><th style="width:27mm"></th><th>Cực đại</th><th>Cực tiểu</th></tr>
<tr><th>${d21}</th><td></td><td></td></tr><tr><th>Hai sóng tới M</th><td></td><td></td></tr>
<tr><th>Biên độ</th><td></td><td></td></tr><tr><th>Hình ảnh</th><td></td><td></td></tr></table>
<div style="margin-top:.8mm"><b>Mẹo</b> (hai nguồn cùng pha): tính ${m('(d_2-d_1)/\\lambda')}</div>
<div>nguyên ${m('\\to')} ${f(25)} · nguyên + ½ ${m('\\to')} ${f(25)}</div></div>
${H.congSong()}</div>
${h3(2, 'Đường cực đại, cực tiểu quanh hai nguồn', '2·2')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div>Trên hình: ${f(12)} cực đại · ${f(12)} cực tiểu</div>
<div>Trên trung trực: ${nw(`${d21} = ${f(12)}`)}</div>
<div>${m('\\to')} trung trực là đường ${f(25)}, ${nw(`${m('k=')} ${f(12)}`)}</div>
<div>Ra phía A, các cực đại ứng với ${nw(`${m('k=')} ${f(20)}`)}</div>
${wl('Điểm nằm trên nét đứt có đứng yên không, dù cả hai sóng đều tới?', 2)}</div>
${H.vanAB()}</div>
${h3(3, 'Làm nhanh', '2·3')}
${box(cau(`<b>Câu 1.</b> Hai nguồn cùng pha, ${nw(`${L} = 4 cm`)}. Điểm M có ${nw(`${m('d_1=9')} cm`)}, ${nw(`${m('d_2=17')} cm`)}. M là cực đại hay cực tiểu? Bậc ${k0}?`, 3)
 + cau(`<b>Câu 2.</b> Cùng pha, ${nw('f = 10 Hz')}, ${nw('v = 30 cm/s')}; N có ${nw(`${m('d_1=14')} cm`)}, ${nw(`${m('d_2=18{,}5')} cm`)}. N là cực đại hay cực tiểu?`, 2))}
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('TRÊN ĐOẠN AB · KHE YOUNG · CÁI BẪY')}
${h3(1, 'II.3 · Trên đoạn nối hai nguồn AB (hai nguồn cùng pha)', '3·1')}
<div class="card fig-side" style="${fs(50)};padding:1.2mm 3mm"><div>
<div>Khoảng cách giữa:</div><table class="tbl-dem" style="margin:.4mm 0"><tr><th>hai cực đại liên tiếp</th><td style="width:18mm"></td></tr><tr><th>cực đại – cực tiểu liền kề</th><td></td></tr></table>
<div>Trung điểm O của AB: ${f(25)}, ${nw(`${m('k=')} ${f(12)}`)}</div></div>
${H.doanAB()}</div>
<div class="card" style="padding:1.2mm 3mm">
<div><b>Đếm số điểm trên AB</b> (${k0} nguyên, không lấy hai đầu A, B):</div>
<table class="tbl-dem" style="margin:.6mm 0"><tr><th style="width:22mm">Cực đại</th><td></td><th style="width:22mm">Cực tiểu</th><td></td></tr></table>
<div>Vì sao: M giữa A và B thì ${m('d_1+d_2=AB')} nên ${m('|d_2-d_1|')} ${f(12)} ${m('AB')}; thay ${m('d_2-d_1=k\\lambda')}, chia cho ${L}.</div></div>
${h3(2, 'II.4 · Giao thoa ánh sáng: khe Young', '3·2')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div>Hai khe ${m('S_1, S_2')} là hai nguồn ${f(25)}</div>
<div>Vân sáng: ${f(25)} · vân tối: ${f(25)}</div>
<table class="tbl-dem" style="margin:.6mm 0"><tr><th>Khoảng vân ${m('i')}</th><th>Vân sáng ${m('x_s')}</th><th>Vân tối ${m('x_t')}</th><th>Sáng – tối liền kề</th></tr><tr><td></td><td></td><td></td><td></td></tr></table>
<div>${m('x')} đo từ ${f(34)}</div></div>
${H.young()}</div>
<div class="card" style="padding:1mm 3mm"><b>Thí nghiệm:</b> laser đỏ (${nw(`${m('\\lambda\\approx0{,}65')} ${m('\\mu\\text{m}')}`)}) qua hai khe ${nw(`${m('a=0{,}2')} mm`)}, màn cách ${nw(`${m('D=2')} m`)} (không rọi laser vào mắt người).
<div>Dự tính ${nw(`${m('i=')} ${f(14)} mm`)} · Đặt màn xa hơn thì vân ${ck}giãn ra ${ck}sít lại · <b>Rút ra:</b> ánh sáng có ${f(26)}</div></div>
<div class="card soft" style="padding:1mm 3mm"><b>Hai bức xạ cùng lúc:</b> vân sáng trùng khi ${m('k_1\\lambda_1=k_2\\lambda_2')}, tức ${nw(`${m('k_1/k_2=')} ${fT(16)} ${m('=p/q')}`)} (tối giản) ${m('\\to')} khoảng vân trùng ${nw(`${m('i_{tr}=')} ${f(22)}`)}</div>
${h3(3, 'III · Cái bẫy: “cực tiểu là chỗ không có sóng tới”', '3·3')}
<div class="card" style="padding:1mm 3mm">
<div>Sửa lại cho đúng: cực tiểu đứng yên vì ${f(76)}</div>
<div><b>Thí nghiệm bịt một loa:</b> hai loa nối cùng một máy phát âm; đứng ở chỗ nghe “nhỏ xíu”, nhờ bạn bịt kín một loa. Tiếng ${ck}to lên ${ck}nhỏ đi ${ck}không đổi</div>
<div>M đang là cực tiểu, tắt một nguồn: M dao động với biên độ ${f(14)} (${m('a')}: biên độ một sóng)</div></div>
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('TRẢ BÀI · TỰ KIỂM TRA · BÀI TOÁN MẪU')}
${h3(1, 'IV · Trả bài 6 câu', '4·1')}
${box(`${tb('1. Hai nguồn kết hợp cần những điều kiện nào?')}${lines(2)}
${tb('2. Viết điều kiện cực đại, cực tiểu (hai nguồn cùng pha); giải thích từng kí hiệu.')}${lines(2)}
${tb('3. Tại cực đại, cực tiểu, hai sóng tới thế nào? Biên độ bao nhiêu?')}${lines(2)}
${tb('4. Trên AB, hai cực đại liên tiếp cách nhau bao nhiêu? Trung điểm AB là gì?')}${lines(1)}
${tb('5. Viết công thức đếm số cực đại, cực tiểu trên AB.')}${lines(2)}
${tb('6. Công thức khoảng vân của khe Young, vị trí vân sáng, vân tối?')}${lines(2)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/6 câu · chưa thuộc: ${f(25)} ${nw(`${m('\\to')} đọc lại ô ${f(12)} Tập`)}</div>
${h3(2, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '4·2')}
${rkHai([1, 2], [3, 4])}
${h3(3, 'V · Bài toán mẫu: xét một điểm, đếm trên AB', '4·3')}
<div class="card soft" style="padding:1.2mm 3mm">Trên mặt nước có hai nguồn A, B dao động cùng pha, cùng tần số ${nw('f = 20 Hz')}, ${nw('AB = 10 cm')}. Tốc độ truyền sóng là ${nw('30 cm/s')}.
<div><b>a)</b> Điểm M cách A là ${nw('12 cm')}, cách B là ${nw('15 cm')}. M là cực đại hay cực tiểu?</div>
<div><b>b)</b> Trên đoạn AB có bao nhiêu điểm cực đại, bao nhiêu điểm cực tiểu?</div></div>
<table><tr><th style="width:52mm">Câu trong đề</th><th>Dữ liệu ${m('\\to')} kiến thức</th></tr>
<tr><td>“hai nguồn A, B dao động cùng pha”</td><td>dùng cực đại ${m('k\\lambda')}, cực tiểu ${m('(k+\\tfrac12)\\lambda')}</td></tr>
<tr><td style="height:6.5mm">“${nw('f = 20 Hz')} … ${nw('30 cm/s')}”</td><td></td></tr>
<tr><td style="height:6.5mm">“M cách A ${nw('12 cm')}, cách B ${nw('15 cm')}”</td><td></td></tr>
<tr><td style="height:6.5mm">“cực đại hay cực tiểu?”</td><td></td></tr>
<tr><td style="height:6.5mm">“bao nhiêu điểm trên đoạn AB”</td><td></td></tr></table>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('GIẢI BÀI TOÁN MẪU · BÀI TẬP VỀ NHÀ · THỬ THÁCH')}
${h3(1, 'Giải bài toán mẫu', '5·1')}
<div class="fig-side" style="${fs(48)}"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl(`Bước sóng ${m('\\lambda=')}`, 1)}${wl(`a) ${d21} và ${m('(d_2-d_1)/\\lambda')}; kết luận:`, 2)}${wl(`b) ${m('AB/\\lambda')}; số cực đại:`, 2)}${wl('Số cực tiểu:', 2)}${wl('Kiểm tra bằng thước bên: số cực đại có khớp không?', 2)}</div>${H.thuocAB()}</div>
${h3(2, 'Điền bước còn thiếu: khe Young', '5·2')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:.6mm 3mm">
<div>${nw(`${m('a=1')} mm`)}, ${nw(`${m('D=2')} m`)}, ${nw(`${m('\\lambda=0{,}5')} ${m('\\mu\\text{m}')}`)}. Điểm P trên màn cách vân trung tâm ${nw('2,5 mm')}.</div>
<div class="ln" style="height:7mm"><b>Bước 1:</b> ${nw(`${m('i=\\lambda D/a=')} ${f(16)} mm`)}</div>
<div class="ln" style="height:7mm"><b>Bước 2:</b> ${nw(`${m('x/i=')} ${f(14)}`)} ${m('\\to')} P là ${f(30)}</div></div>
${K.btvn().replace('<i>1</i>', '<i>3</i>')}
${h3(4, 'Thử thách phân tầng', '5·4')}
${box(wl(`${m('\\bigstar')} Hai nguồn cùng pha, ${nw(`${L} = 2 cm`)}; ${nw(`${m('MA=12')} cm`)}, ${nw(`${m('MB=15')} cm`)}. M là cực đại hay cực tiểu?`, 2)
 + wl(`${m('\\bigstar\\bigstar')} Hai nguồn cùng pha, ${nw(`${L} = 2 cm`)}, ${nw('AB = 9 cm')}. Đếm số cực đại, số cực tiểu trên đoạn AB.`, 3)
 + wl(`${m('\\bigstar\\bigstar\\bigstar')} Hai nguồn dao động <b>ngược pha</b>. Trung điểm của AB là cực đại hay cực tiểu? Vì sao?`, 3))}
${h3(5, 'VI · Mang về: điều em dễ quên nhất', '5·5')}
${box(wl('1.', 1) + wl('2.', 1) + wl('3.', 1))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Xét một điểm là cực đại hay cực tiểu',
    de: `Hai nguồn A, B cùng pha, ${nw('f = 25 Hz')}, ${nw('AB = 20 cm')}, tốc độ sóng ${nw('v = 50 cm/s')}. M cách A ${nw('16 cm')}, cách B ${nw('21 cm')}; N cách A ${nw('18 cm')}, cách B ${nw('24 cm')}.<br><b>a)</b> M là cực đại hay cực tiểu? Ghi kèm ${k0}<br><b>b)</b> N là cực đại hay cực tiểu? Ghi kèm ${k0}`,
    nd: `chia ${d21} cho ${f(12)} (không xét số cm); nguyên ${m('\\to')} ${f(25)}, nguyên + ½ ${m('\\to')} ${f(25)}`,
    a: ['a', 'b'], gi: 3, cot: 2 },
  { t: 'Dạng 2 · Trung bình · Đếm số cực đại, cực tiểu trên đoạn AB',
    de: `Hai nguồn kết hợp A, B cùng pha, ${nw('f = 20 Hz')}, ${nw('AB = 12 cm')}, ${nw('v = 40 cm/s')}. Trên đoạn AB có bao nhiêu điểm<br><b>a)</b> dao động với biên độ cực đại?<br><b>b)</b> đứng yên (cực tiểu)?`,
    nd: `tính ${m('AB/\\lambda')}, đếm ${k0} nguyên; ${k0} làm điểm trùng đúng nguồn A, B thì ${f(25)}`,
    a: ['a', 'b'], gi: 4, cot: 2 },
  { t: 'Dạng 3 · Trung bình · Biết số dãy cực đại giữa M và trung trực',
    de: `Hai nguồn A, B cùng pha, ${nw('f = 10 Hz')}, ${nw('AB = 24 cm')}. Điểm M cách A ${nw('14 cm')}, cách B ${nw('26 cm')} dao động với biên độ cực đại. Giữa M và trung trực của AB còn ${nw('3 dãy')} cực đại khác (không kể trung trực).<br><b>a)</b> M thuộc dãy cực đại bậc mấy?<br><b>b)</b> Tính bước sóng.<br><b>c)</b> Tính tốc độ truyền sóng.`,
    nd: `trung trực ${nw(`${m('k=')} ${f(12)}`)}; dãy qua M kế sau ${f(12)} dãy; ${nw(`${L} = ${f(14)}`)}, ${nw(`${m('v=')} ${f(14)}`)}`,
    a: ['a', 'b', 'c'], gi: 5, fig: H.dayM() },
];
const dang2 = [
  { t: 'Dạng 4 · Trung bình · Khe Young: khoảng vân, bước sóng, loại vân',
    de: `Thí nghiệm Young, ánh sáng đơn sắc: ${nw(`${m('a=0{,}8')} mm`)}, ${nw(`${m('D=1{,}6')} m`)}. Khoảng cách giữa ${nw('7 vân sáng')} liên tiếp là ${nw('6,0 mm')} (hình). M và N ở cùng một phía vân trung tâm, cách vân trung tâm ${nw('4,5 mm')} và ${nw('7,0 mm')}.<br><b>a)</b> khoảng vân ${m('i')} (a<sub>1</sub>), bước sóng ${L} (a<sub>2</sub>)<br><b>b)</b> M (b<sub>1</sub>), N (b<sub>2</sub>) là vân sáng hay vân tối? Vân sáng thì ghi bậc`,
    nd: `${f(12)} vân sáng liên tiếp có ${f(12)} khoảng vân; ${nw(`${L} = ${fT(16)}`)}, đổi ${m('i')}, ${m('a')} ra mét; xét ${m('x/i')}`,
    a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>'], gi: 7, fig: H.vanD4() },
  { t: 'Dạng 5 · Khó · Khe Young với hai bức xạ: vân sáng trùng nhau',
    de: `Thí nghiệm Young: ${nw(`${m('a=1{,}2')} mm`)}, ${nw(`${m('D=2')} m`)}; chiếu cùng lúc ${nw(`${m('\\lambda_1=0{,}60')} ${m('\\mu\\text{m}')}`)} và ${nw(`${m('\\lambda_2=0{,}45')} ${m('\\mu\\text{m}')}`)}. Vân sáng trung tâm của hai bức xạ trùng nhau.<br><b>a)</b> khoảng vân ${m('i_1')} (a<sub>1</sub>), ${m('i_2')} (a<sub>2</sub>)<br><b>b)</b> khoảng cách từ vân trung tâm tới vân sáng gần nhất cùng màu với nó (vân trùng)<br><b>c)</b> giữa hai vân trùng liên tiếp có bao nhiêu vân sáng của riêng ${m('\\lambda_2')}?`,
    nd: `${nw(`${m('\\dfrac{k_1}{k_2}=')} ${fT(16)}`)} tối giản ${m('=\\dfrac pq')}; ${nw(`${m('i_{tr}=')} ${f(14)}`)}; không đếm hai vân trùng ở hai đầu`,
    a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'], gi: 8, fig: H.thangD5() },
];

// Bài tương tự giải vào vở (thầy chốt 10/11): 1 cột; ô đáp số cuối đúng dòng của ý, nhãn ô khớp a) b) c)…
// Đáp số tính bằng Python 13/11/2026.
const oY = (s, o, w = 25) => s.split('<br>').map((p) => {
  const y = p.match(/^<b>([a-d])\)<\/b>/);
  if (!y) return `<div>${p}</div>`;
  const ls = o.filter((l) => (Array.isArray(l) ? l[0] : l)[0] === y[1]);
  return `<div class="yo"><span>${p}</span><span class="oo">${ls.map((l) => { const [n, wd] = Array.isArray(l) ? l : [l, w]; return `<span class="nw"><b>${n})</b>${f(wd)}</span>`; }).join('')}</span></div>`;
}).join('');
const ttDe = (b) => b.fig ? `<div class="fig-side" style="grid-template-columns:1fr ${b.fw}mm"><div>${oY(b.de, b.o, b.ow)}</div>${b.fig}</div>` : oY(b.de, b.o, b.ow);
const vaoVo = (ds) => ds.map((b) => (b.o ? { t: b.t, de: ttDe(b), k: 0 } : b));
const nhap = (n) => ({ t: '<span class="nhap-t">Nháp / chỗ em còn vướng</span>', de: lines(n), k: 0 });
const s1 = 'a<sub>1</sub>', s2 = 'a<sub>2</sub>', b1 = 'b<sub>1</sub>', b2 = 'b<sub>2</sub>';
const CD = 34; // ô chữ "cực đại/cực tiểu, k = …" (mm)
const cungPha = (fq, v) => `Hai nguồn A, B cùng pha, ${nw(`f = ${fq} Hz`)}, tốc độ sóng ${nw(`v = ${v}`)}.`;
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–3', 'DẠNG 4–5'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `${cungPha(20, '40 cm/s')} M cách A ${nw('10 cm')}, cách B ${nw('17 cm')}; N cách A ${nw('14 cm')}, cách B ${nw('20 cm')}.<br><b>a)</b> M: cực đại hay cực tiểu, ${k0} = ?<br><b>b)</b> N: cực đại hay cực tiểu, ${k0} = ?`, o: [['a', CD], ['b', CD]] },
    { t: 'Dạng 1 · Bài 2', de: `${cungPha(15, '60 cm/s')} M cách A ${nw('20 cm')}, cách B ${nw('26 cm')}; N cách A ${nw('9 cm')}, cách B ${nw('17 cm')}.<br><b>a)</b> M: cực đại hay cực tiểu, ${k0} = ?<br><b>b)</b> N: cực đại hay cực tiểu, ${k0} = ?`, o: [['a', CD], ['b', CD]] },
    { t: 'Dạng 2 · Bài 1', de: `${cungPha(25, '50 cm/s')} ${nw('AB = 11 cm')}. Trên đoạn AB có bao nhiêu điểm<br><b>a)</b> cực đại?<br><b>b)</b> cực tiểu?`, o: [['a', 14], ['b', 14]] },
    { t: 'Dạng 2 · Bài 2', de: `${cungPha(50, '1,5 m/s')} ${nw('AB = 14 cm')}. Trên đoạn AB có bao nhiêu điểm<br><b>a)</b> cực đại?<br><b>b)</b> cực tiểu?`, o: [['a', 14], ['b', 14]] },
    { t: 'Dạng 3 · Bài 1', de: `Hai nguồn A, B cùng pha, ${nw('f = 20 Hz')}, ${nw('AB = 20 cm')}. M cách A ${nw('10 cm')}, cách B ${nw('19 cm')} là cực đại; giữa M và trung trực còn ${nw('2 dãy')} cực đại khác.<br><b>a)</b> bậc ${k0} của dãy qua M<br><b>b)</b> bước sóng<br><b>c)</b> tốc độ truyền sóng`, o: [['a', 16], ['b', 18], ['c', 22]] },
    { t: 'Dạng 3 · Bài 2', de: `Hai nguồn A, B cùng pha, ${nw('f = 15 Hz')}, ${nw('AB = 18 cm')}. M cách A ${nw('16 cm')}, cách B ${nw('26 cm')} là cực đại; giữa M và trung trực còn ${nw('4 dãy')} cực đại khác.<br><b>a)</b> bậc ${k0} của dãy qua M<br><b>b)</b> bước sóng<br><b>c)</b> tốc độ truyền sóng`, o: [['a', 16], ['b', 18], ['c', 22]] },
  ], [
    { t: 'Dạng 4 · Bài 1', de: `Young: ${nw(`${m('a=1')} mm`)}, ${nw(`${m('D=2')} m`)}; ${nw('9 vân sáng')} liên tiếp cách nhau ${nw('9,6 mm')}. M, N cùng phía vân trung tâm, cách nó ${nw('4,2 mm')} và ${nw('6,0 mm')}.<br><b>a)</b> ${m('i')}, ${L}<br><b>b)</b> M, N là vân gì? (vân sáng: ghi bậc)`, o: [[s1, 18], [s2, 18], [b1, 28], [b2, 28]] },
    { t: 'Dạng 4 · Bài 2', de: `Young: ${nw(`${m('a=0{,}5')} mm`)}, ${nw(`${m('D=1{,}6')} m`)}; đoạn màn ở hình bên. M, N cùng phía vân trung tâm, cách nó ${nw('5,0 mm')} và ${nw('8,0 mm')}.<br><b>a)</b> ${m('i')}, ${L}<br><b>b)</b> M, N là vân gì?`, fig: H.vanTT(), fw: 40, o: [[s1, 14], [s2, 14], [b1, 24], [b2, 24]] },
    { t: 'Dạng 5 · Bài 1', de: `Young: ${nw(`${m('a=1')} mm`)}, ${nw(`${m('D=2')} m`)}; chiếu cùng lúc ${um(`${m('\\lambda_1=0{,}50')}`)} và ${um(`${m('\\lambda_2=0{,}75')}`)}.<br><b>a)</b> ${m('i_1')}, ${m('i_2')}<br><b>b)</b> từ vân trung tâm tới vân trùng gần nhất<br><b>c)</b> giữa hai vân trùng liên tiếp: số vân sáng riêng ${m('\\lambda_1')}`, o: [[s1, 18], [s2, 18], ['b', 20], ['c', 16]] },
    { t: 'Dạng 5 · Bài 2', de: `Young: ${nw(`${m('a=0{,}8')} mm`)}, ${nw(`${m('D=1{,}2')} m`)}; chiếu cùng lúc ${um(`${m('\\lambda_1=0{,}64')}`)} và ${um(`${m('\\lambda_2=0{,}48')}`)}.<br><b>a)</b> ${m('i_1')}, ${m('i_2')}<br><b>b)</b> từ vân trung tâm tới vân trùng gần nhất<br><b>c)</b> giữa hai vân trùng liên tiếp: số vân sáng riêng ${m('\\lambda_2')}`, o: [[s1, 18], [s2, 18], ['b', 20], ['c', 16]] },
    nhap(9),
  ]],
  dap: [
    `D1·1: a) cực tiểu, ${m('k=3')} · b) cực đại, ${m('k=3')} &nbsp;|&nbsp; D1·2: a) cực tiểu, ${m('k=1')} · b) cực đại, ${m('k=2')} &nbsp;|&nbsp; D2·1: a) 11 · b) 10 &nbsp;|&nbsp; D2·2: a) 9 · b) 10 &nbsp;|&nbsp; D3·1: a) ${m('k=3')} · b) ${nw('3 cm')} · c) ${nw('60 cm/s')} &nbsp;|&nbsp; D3·2: a) ${m('k=5')} · b) ${nw('2 cm')} · c) ${nw('30 cm/s')}`,
    `D4·1: a<sub>1</sub>) ${nw('1,2 mm')} · a<sub>2</sub>) ${um('0,6')} · b<sub>1</sub>) M vân tối (${m('k=3')}) · b<sub>2</sub>) N vân sáng ${nw('bậc 5')} &nbsp;|&nbsp; D4·2: a<sub>1</sub>) ${nw('2,0 mm')} · a<sub>2</sub>) ${um('0,625')} · b<sub>1</sub>) M vân tối (${m('k=2')}) · b<sub>2</sub>) N vân sáng ${nw('bậc 4')} &nbsp;|&nbsp; D5·1: a<sub>1</sub>) ${nw('1,0 mm')} · a<sub>2</sub>) ${nw('1,5 mm')} · b) ${nw('3,0 mm')} · c) ${nw('2 vân')} &nbsp;|&nbsp; D5·2: a<sub>1</sub>) ${nw('0,96 mm')} · a<sub>2</sub>) ${nw('0,72 mm')} · b) ${nw('2,88 mm')} · c) ${nw('3 vân')}`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang: [...dang, ...dang2], tach: [3, 2], kq: [[1, 2, 3], [4, 5]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'nguồn kết hợp 1·4 · khay sóng 1·5 · cực đại, cực tiểu 2·1 · đường vân quanh AB 2·2 · trên đoạn AB 3·1 · khe Young, hai bức xạ 3·2 · bẫy 3·3 · bài toán mẫu 4·3 · dạng 1–3 ở 6·1 · dạng 4–5 ở 7·1',
  out: process.argv[2],
});
