// Ruột tập VL10 – Bài 8 · Chuyển động biến đổi. Gia tốc (lesson id 53). Quyển Chương 2 lớp 10 (bài 4–12): bài 8 = tr. 49–60.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l10-bai8.mjs (toàn bộ SVG tự vẽ). Nội dung theo bài web (book/cache/53.json, tải từ DB 13/11/2026):
// mục tiêu, dự đoán đèn xanh, II.1–II.4, hai thí nghiệm (vết bi, xe lăn), ba bẫy, Trả bài 6 câu, bài toán mẫu ô tô hãm phanh,
// thử thách phân tầng, 5 dạng bài tập mẫu. Đáp số bài mẫu, Bài tương tự (tuongTu.dap) tính bằng Python 13/11/2026.
// Chạy: node scripts/ruot-tap/l10-bai8.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl10-bai8.pdf
//       node scripts/ruot-tap/l10-bai8.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l10-bai8/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL10b8 as H, vongH as V } from './hinh-l10-bai8.mjs';

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
  const out = resolve(HERE, 'out/hinh-l10-bai8'); mkdirSync(out, { recursive: true });
  const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true, args: ['--allow-file-access-from-files'] });
  const pg = await b.newPage();
  for (const [name, fn] of Object.entries(H)) {
    writeFileSync(out + '/_tmp.html', `<!doctype html><meta charset="utf-8"><style>${css}</style>${fn()}`);
    await pg.goto(pathToFileURL(out + '/_tmp.html').href, { waitUntil: 'networkidle0' });
    await pg.evaluate('document.fonts.ready');
    await (await pg.$('.fig')).screenshot({ path: `${out}/${name}.png` });
    console.log(`${name}.png`);
  }
  await b.close();
  process.exit(0);
}

const K = khoiTao({ bai: 8, lid: 53, ten: 'CHUYỂN ĐỘNG BIẾN ĐỔI · GIA TỐC', lop: 10, baiDau: 4, sub: 'Vật lí 10 · Chương 2: Động học' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const u = (s) => nw(m(s)); // số + đơn vị không gãy dòng
const ms = (x) => u(`${x}\\ \\mathrm{m/s}`), kmh = (x) => u(`${x}\\ \\mathrm{km/h}`), sec = (x) => u(`${x}\\ \\mathrm s`), ms2 = (x) => u(`${x}\\ \\mathrm{m/s^2}`);
const va = m('\\vec a'), vv = m('\\vec v');

const p1 = `<section class="page">
${head('BÀI 8 · CHUYỂN ĐỘNG BIẾN ĐỔI · GIA TỐC', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Nhận ra <b>chuyển động biến đổi</b> và <b>thẳng biến đổi đều</b>`)}
${dong(`${ck}Nêu định nghĩa, công thức, đơn vị, ý nghĩa của <b>gia tốc</b>`)}
${dong(`${ck}Phân biệt <b>nhanh dần</b> và <b>chậm dần</b> qua chiều của ${va} so với ${vv}`)}
${dong(`${ck}Đọc <b>đồ thị v–t</b>: tính gia tốc và độ dịch chuyển từ đồ thị`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Đèn vừa chuyển xanh. Xe nào “tăng tốc” mạnh hơn?</p>
<div class="fig-side" style="${fs(48)}"><div>
${opt('A', `Ô tô, vì đạt vận tốc cuối lớn hơn, ${ms(20)}`)}
${opt('B', `Xe máy, vì tăng ${ms(10)} chỉ trong ${sec(5)}`)}
${opt('C', `Như nhau, vì cả hai cùng tăng ${ms(10)}`)}
${opt('D', 'Ô tô, vì tăng tốc lâu hơn')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 1)}</div>
${H.denXanh()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Chuyển động biến đổi', '1·4')}
<div class="card" style="padding:1.2mm 3mm">
<div><b>Chuyển động biến đổi:</b> chuyển động có ${f(25)} thay đổi.</div>
<div>Vận tốc là vectơ nên “thay đổi” gồm đổi ${f(25)} hoặc đổi ${f(25)}.</div>
<div><b>Thẳng biến đổi đều:</b> chuyển động thẳng, độ lớn vận tốc ${f(25)} hoặc ${f(25)} theo thời gian.</div>
<div>“Đều” nghĩa là: cứ mỗi giây, vận tốc tăng (hoặc giảm) ${f(25)}.</div></div>
${h3(5, 'Thí nghiệm: dấu vết viên bi qua video', '1·5')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div><b>Làm:</b> quay video bi lăn trên bàn ngang, xuống máng nghiêng, rồi lên máng nghiêng; dừng hình mỗi ${sec('0{,}2')}, chấm vị trí.</div>
<div><b>Quan sát:</b> trên bàn các khoảng ${f(25)}; xuống dốc ${f(25)}; lên dốc ${f(25)}.</div>
<div><b>Rút ra:</b> khoảng đi được mỗi ${sec('0{,}2')} thay đổi, tức ${f(25)} thay đổi.</div>
${wl('Đoạn nào là chuyển động đều? Vì sao?', 1)}</div>
${H.vetBi()}</div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('GIA TỐC · THÍ NGHIỆM XE LĂN · NHANH DẦN, CHẬM DẦN')}
${h3(1, 'II.2 · Gia tốc', '2·1')}
<div class="card" style="padding:1.2mm 3mm">
<div>Gia tốc đặc trưng cho độ ${f(25)} của vận tốc theo thời gian: vận tốc đổi ${f(25)} hay chậm.</div>
<div style="margin:.8mm 0">Vectơ: ${m('\\vec a=\\dfrac{\\Delta\\vec v}{\\Delta t}')} &nbsp;· &nbsp;Thẳng, đã chọn chiều dương: ${m('a=\\dfrac{\\Delta v}{\\Delta t}=')} ${f(25)}</div>
<div>Gia tốc là đại lượng ${f(25)}; đơn vị ${f(14)}. Đổi ${m('\\mathrm{km/h}\\to\\mathrm{m/s}')}: ${f(16)} cho ${m('3{,}6')}.</div>
<div><b>Đọc đơn vị:</b> ${ms2(2)} nghĩa là mỗi ${f(14)}, vận tốc thay đổi ${f(16)}.</div>
<div>Xe máy ở mục Dự đoán: ${m('a=')} ${f(25)} ${m('=')} ${f(12)} ${m('\\mathrm{m/s^2}')}; ô tô: ${m('a=')} ${f(12)} ${m('\\mathrm{m/s^2}')}</div></div>
${h3(2, 'Thí nghiệm: đo gia tốc xe lăn xuống máng nghiêng', '2·2')}
<div class="fig-side" style="${fs(46)}"><div>
<table class="tbl-ct"><tr><th>${m('t\\ (\\mathrm s)')}</th><th>${m('v\\ (\\mathrm{m/s})')}</th><th>${m('\\Delta v/\\Delta t\\ (\\mathrm{m/s^2})')}</th></tr>
<tr><td>0,0</td><td>0,20</td><td>—</td></tr>
<tr><td>0,2</td><td>0,30</td><td></td></tr>
<tr><td>0,4</td><td>0,40</td><td></td></tr>
<tr><td>0,6</td><td>0,49</td><td></td></tr>
<tr><td>0,8</td><td>0,59</td><td></td></tr></table></div>
${H.xeMang()}</div>
<div class="card" style="margin-top:.8mm;padding:1mm 3mm">
<div>Lấy cả khoảng ${m('0\\to0{,}8\\ \\mathrm s')}: ${m('a\\approx')} ${f(25)} ${m('\\mathrm{m/s^2}')}. Xe chuyển động ${f(25)}</div>
${wl(`Vì sao bốn khoảng cho ${m('\\Delta v/\\Delta t')} hơi khác nhau? Khoảng nào tin cậy hơn?`, 2)}</div>
${h3(3, 'II.3 · Nhanh dần đều và chậm dần đều', '2·3')}
<div class="fig-side" style="${fs(50)}"><table>
<tr><th></th><th>Nhanh dần đều</th><th>Chậm dần đều</th></tr>
<tr><td>Độ lớn ${m('v')}</td><td></td><td></td></tr>
<tr><td>${va} so với ${vv}</td><td></td><td></td></tr>
<tr><td>Dấu ${m('a\\cdot v')}</td><td></td><td></td></tr>
<tr><td>Ví dụ</td><td></td><td></td></tr></table>
${H.bonChieu()}</div>
${box(cau(`Bi lăn lên dốc tới khi dừng rồi lăn ngược xuống. Lúc lăn xuống, bi nhanh dần hay chậm dần? ${va} hướng lên hay xuống dốc?`, 2))}
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('ĐỒ THỊ VẬN TỐC – THỜI GIAN · BA CÁI BẪY · TỰ KIỂM TRA')}
${h3(1, 'II.4 · Đồ thị v–t (thẳng, không đổi chiều)', '3·1')}
<div class="card fig-side" style="${fs(48)};padding:1.2mm 3mm"><div>
<div>Thẳng đều: ${f(25)} trục ${m('Ot')}, ${nw(`${m('a=')} ${f(12)}`)}</div>
<div>Thẳng biến đổi đều: đường thẳng ${f(25)}.</div>
<div style="margin:.6mm 0"><b>Độ dốc</b> ${m('=a=\\tan\\alpha=')} ${f(25)}</div>
<div><b>Diện tích</b> dưới đồ thị từ ${m('t_1')} đến ${m('t_2')} ${m('=')} ${f(25)}</div>
<div>Khi ${m('v>0')}: đồ thị đi lên là ${f(25)}, đi xuống là ${f(25)}</div>
<div class="hint">${m('\\tan\\alpha')} tính bằng số đọc trên hai trục, không đo góc bằng thước đo độ.</div></div>
${H.baDoThi()}</div>
${box(cau(`<b>Làm nhanh.</b> Đồ thị ${m('v')}–${m('t')} của xe là đoạn thẳng từ ${ms(4)} lúc ${m('t=0')} lên ${ms(10)} lúc ${sec(3)}. Gia tốc? Nhanh hay chậm dần?`, 2))}
${h3(2, 'III · Ba cái bẫy hay sập', '3·2')}
<div class="card" style="padding:1mm 3mm">
<div class="trap">${ck}<span><b>“Nhanh thì gia tốc lớn.”</b> Máy bay bay thẳng đều ${ms(250)} có ${m('a=')} ${f(12)}; xe máy vừa rời vạch dừng (${m('v=0')}) vẫn có ${m('a')} ${f(12)} ${m('0')}.</span></div>
<div class="trap">${ck}<span><b>“Gia tốc âm là chậm dần.”</b> Dấu của ${m('a')} phụ thuộc chiều dương em chọn; nhanh hay chậm dần xét dấu của ${f(16)}.</span></div>
<div class="trap">${ck}<span><b>“Tốc độ không đổi thì không có gia tốc.”</b> Xe vào cua, đồng hồ đứng yên ${kmh(40)}, nhưng ${f(25)} vận tốc đổi nên vẫn có gia tốc.</span></div></div>
<table><tr><th style="width:40mm">Dấu của ${m('v')} và ${m('a')}</th><th>Kết luận</th></tr>
<tr><td>Cùng dấu</td><td></td></tr><tr><td>Trái dấu</td><td></td></tr><tr><td>Chỉ biết ${m('a<0')}</td><td></td></tr></table>
${box(cau(`<b>Làm nhanh.</b> Xe chạy chậm dần đều; chọn chiều dương <b>ngược</b> chiều chuyển động. Dấu của ${m('v')}: ${f(12)} · dấu của ${m('a')}: ${f(12)}. Vì sao?`, 1), 'margin-top:1mm')}
${h3(3, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '3·3')}
${rkHai([1, 2, 3], [4, 5, 6])}
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('TRẢ BÀI · BÀI TOÁN MẪU')}
${h3(1, 'IV · Trả bài 6 câu', '4·1')}
${box(`${tb('1. Chuyển động biến đổi là gì? Thẳng biến đổi đều là gì?')}${lines(2)}
${tb('2. Gia tốc: định nghĩa, công thức, đơn vị.')}${lines(2)}
${tb(`3. ${m('a=3\\ \\mathrm{m/s^2}')} nghĩa là gì?`)}${lines(1)}
${tb('4. Khi nào nhanh dần, khi nào chậm dần?')}${lines(1)}
${tb('5. Đồ thị v–t: dạng của thẳng đều, biến đổi đều? Độ dốc, diện tích cho biết gì?')}${lines(2)}
${tb('6. Tốc độ không đổi thì có thể có gia tốc không? Ví dụ.')}${lines(1)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/6 câu · chưa thuộc: ${f(25)} ${nw(`→ đọc lại ô ${f(12)} Tập`)}</div>
${h3(2, 'V · Bài toán mẫu: ô tô hãm phanh', '4·2')}
<div class="card soft" style="padding:1.2mm 3mm">Ô tô đang chạy thẳng ${kmh(54)} thì hãm phanh, chậm dần đều và dừng lại sau ${sec(5)}. Chọn chiều dương là chiều chuyển động. Tính gia tốc, cho biết chiều của gia tốc, và dùng đồ thị ${m('v')}–${m('t')} tính quãng đường ô tô đi được khi hãm phanh.</div>
<table><tr><th style="width:52mm">Câu trong đề</th><th>Dữ liệu → kiến thức</th></tr>
<tr><td>“đang chạy … 54 km/h”</td><td>${m('v_1=54:3{,}6=15\\ \\mathrm{m/s}')}</td></tr>
<tr><td style="height:6.5mm">“dừng lại sau 5 s”</td><td></td></tr>
<tr><td style="height:6.5mm">“chiều dương là chiều chuyển động”</td><td></td></tr>
<tr><td style="height:6.5mm">“quãng đường … đồ thị v–t”</td><td></td></tr></table>
<div class="fig-side" style="${fs(50)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl(`Gia tốc ${m('a')}:`, 2)}${wl(`Chiều của ${va}:`, 1)}${wl('Quãng đường (diện tích):', 2)}${wl('Kiểm tra lại:', 1)}</div>${H.phanh()}</div>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('ĐIỀN BƯỚC · BÀI TẬP VỀ NHÀ · THỬ THÁCH · MANG VỀ')}
${h3(1, `Điền bước còn thiếu: dừng sau ${sec(4)}, lúc hãm ${kmh(72)}`, '5·1')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div class="ln"><b>Bước 1 (cho sẵn):</b> ${m('v_1=72:3{,}6=20\\ \\mathrm{m/s}')}; &nbsp;${m('v_2=0')}</div>
${wl(`Bước 2: ${m('a=')}`, 1)}${wl(`Bước 3: ${m('s=')}`, 1)}
<div class="ln"><b>Đổi chiều:</b> chiều dương <b>ngược</b> chiều xe chạy (đề gốc ${kmh(54)}, ${sec(5)})</div>
<div class="ln">${m('a=')} ${f(16)} ${m('\\mathrm{m/s^2}')}; &nbsp;xe ${ck}nhanh dần ${ck}chậm dần, vì</div>${lines(1)}</div>
${K.btvn().replace('<i>1</i>', '<i>2</i>')}
${h3(3, 'Thử thách phân tầng', '5·3')}
<div class="fig-side" style="${fs(46)}">${box(wl(`${m('\\bigstar')} Tàu hoả tăng đều từ ${kmh(36)} lên ${kmh(54)} trong ${sec(10)}. Gia tốc?`, 3)
 + wl(`${m('\\bigstar\\bigstar')} VĐV trượt băng đang lướt ${ms(8)} thì hãm, chậm dần đều, gia tốc có độ lớn ${ms2(2)}. Sau bao lâu dừng? Đi thêm bao xa?`, 4)
 + wl(`${m('\\bigstar\\bigstar\\bigstar')} Vật có ${m('a=-2\\ \\mathrm{m/s^2}')} không đổi, lúc ${m('t=0')} có ${ms(4)}. Lúc ${sec(3)}, vật nhanh dần hay chậm dần?`, 5))}${H.doiChieu()}</div>
${h3(4, 'VI · Mang về: điều em dễ quên nhất', '5·4')}
${box(wl('1.', 3) + wl('2.', 3) + wl('3.', 3))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Tính gia tốc từ hai vận tốc, đổi km/h',
    de: `Ô tô tải đang chạy thẳng ${kmh(18)} thì tăng ga, vận tốc tăng đều; ${sec(20)} sau đạt ${kmh(36)}.<br><b>a)</b> gia tốc của xe<br><b>b)</b> vận tốc sau ${sec(40)} kể từ lúc tăng ga<br><b>c)</b> sau bao lâu (từ lúc tăng ga) xe đạt ${kmh(72)}`,
    nd: `đổi ${m('\\mathrm{km/h}\\to\\mathrm{m/s}')}: ${f(16)} cho 3,6; rút ra ${m('v_2=v_1+')} ${f(16)}`, a: ['a', 'b', 'c'], gi: 3 },
  { t: 'Dạng 2 · Trung bình · Xe phanh: dấu của gia tốc và chiều dương',
    de: `Xe máy đang chạy thẳng ${kmh(36)} thì phanh gấp, chậm dần đều, dừng sau ${sec(4)}.<br><b>a)</b> chiều dương theo chiều chuyển động: ${m('a')}; dấu ${m('v')}, ${m('a')}<br><b>b)</b> chiều dương ngược chiều chuyển động: ${m('a')}; dấu ${m('v')}, ${m('a')}; còn chậm dần không<br><b>c)</b> vận tốc sau ${sec(2)} kể từ lúc phanh (chiều dương như a)`,
    nd: `chậm dần ${m('\\Leftrightarrow a\\cdot v')} ${f(12)} 0 (không xét riêng dấu ${m('a')})`, a: ['a', 'b', 'c'], gi: 4 },
  { t: 'Dạng 3 · Trung bình · Đọc đồ thị v–t: gia tốc từng giai đoạn',
    de: `Đồ thị ${m('v')}–${m('t')} của tàu điện chạy thẳng (hình); chiều dương là chiều chuyển động.<br><b>a)</b> gia tốc ${m('a_1')}, ${m('a_2')}, ${m('a_3')}; tính chất chuyển động từng giai đoạn<br><b>b)</b> lúc ${sec(18)}: nhanh dần hay chậm dần`,
    nd: `mỗi đoạn thẳng một giai đoạn; ${m('a=')} độ ${f(16)} của đoạn đó`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'a<sub>3</sub>', 'b'], gi: 5, fig: H.tauDien('') },
  { t: 'Dạng 4 · Trung bình · Quãng đường từ diện tích dưới đồ thị v–t',
    de: `Vận tốc xe máy trên đường thẳng: ${nw(`${m('t=0')}: ${m('v=0')}`)}; ${nw(`${m('t=8\\ \\mathrm s')}: ${ms(12)}`)}; ${nw(`${m('t=20\\ \\mathrm s')}: ${ms(12)}`)}; ${nw(`${m('t=30\\ \\mathrm s')}: ${m('v=0')}`)}; giữa hai mốc liền nhau ${m('v')} đổi đều.<br><b>a)</b> tính chất chuyển động từng giai đoạn<br><b>b)</b> gia tốc trong ${sec(8)} đầu và ${sec(10)} cuối<br><b>c)</b> quãng đường trong ${sec(30)} (diện tích)<br><b>d)</b> tốc độ trung bình trong ${sec(30)}`,
    nd: `diện tích = ${f(25)}; xe không đổi chiều nên bằng quãng đường`, a: ['a', 'b', 'c', 'd'], gi: 6, fig: H.luoiTrong(), cot: 2 },
  { t: 'Dạng 5 · Khó · Vật đổi hướng: độ biến thiên vận tốc và gia tốc',
    de: `Bóng tennis bay ngang ${ms(25)} hướng đông, đập vuông góc vào tường, bật lại ${ms(15)} hướng tây; va chạm kéo dài ${sec('0{,}05')}.<br><b>a)</b> độ biến thiên <b>tốc độ</b><br><b>b)</b> chiều dương hướng đông: độ biến thiên <b>vận tốc</b> ${m('\\Delta v')}<br><b>c)</b> gia tốc trung bình và hướng của gia tốc`,
    nd: `bật ngược lại thì ${m('v_1')}, ${m('v_2')} ${f(25)} dấu; ${m('\\Delta v')} khác hiệu hai tốc độ`, a: ['a', 'b', 'c'], gi: 6, fig: H.bongTuong(), cot: 3 },
];

// Bài tương tự: giải vào vở (thầy chốt 10/11); mỗi dạng 2 bài; ô đáp số cuối đúng dòng của ý (mẫu l10-bai23).
const oY = (s, o, w = 25) => s.split('<br>').map((p) => {
  const y = p.match(/^<b>([a-d])\)<\/b>/);
  if (!y) return `<div>${p}</div>`;
  const ls = o.filter((l) => l[0] === y[1]);
  return `<div class="yo"><span>${p}</span><span class="oo">${ls.map((l) => `<span class="nw"><b>${l})</b>${f(w)}</span>`).join('')}</span></div>`;
}).join('');
const ttDe = (b) => b.fig ? `<div class="fig-side" style="grid-template-columns:1fr ${b.fw}mm"><div>${oY(b.de, b.o, b.ow)}</div>${b.fig}</div>` : oY(b.de, b.o, b.ow);
const vaoVo = (ds) => ds.map((b) => (b.o ? { t: b.t, de: ttDe(b), k: 0 } : b));
const nhap = (n) => ({ t: '<span class="nhap-t">Nháp / chỗ em còn vướng</span>', de: lines(n), k: 0 });
const ttCot = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–3', 'DẠNG 4–5'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Xe buýt đang chạy thẳng ${kmh(36)} thì tăng tốc đều; sau ${sec(10)} đạt ${kmh(54)}.<br><b>a)</b> gia tốc<br><b>b)</b> vận tốc sau ${sec(16)} kể từ lúc tăng tốc (m/s)<br><b>c)</b> sau bao lâu (từ lúc tăng tốc) xe đạt ${kmh(72)}`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 1 · Bài 2', de: `Tàu hoả rời ga, chuyển động thẳng nhanh dần đều; sau ${sec(75)} đạt ${kmh(54)}.<br><b>a)</b> gia tốc<br><b>b)</b> vận tốc sau ${sec(50)} kể từ lúc rời ga (m/s)<br><b>c)</b> sau bao lâu tàu đạt ${kmh(72)}`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 2 · Bài 1', de: `Ô tô đang chạy thẳng ${kmh(72)} thì hãm phanh, chậm dần đều, dừng lại sau ${sec(5)}.<br><b>a)</b> chiều dương là chiều chuyển động: gia tốc ${m('a')}<br><b>b)</b> chiều dương ngược chiều chuyển động: gia tốc ${m('a')}<br><b>c)</b> vận tốc sau ${sec(3)} kể từ lúc phanh (chiều dương như câu a)`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 2 · Bài 2', de: `Bạn An đang đạp xe thẳng ${kmh(18)} thì ngừng đạp; xe chậm dần đều, sau ${sec(10)} còn ${kmh(9)}.<br><b>a)</b> chiều dương là chiều chuyển động: gia tốc<br><b>b)</b> kể từ lúc còn ${kmh(9)}, thêm bao lâu thì xe dừng<br><b>c)</b> chiều dương ngược chiều chuyển động: gia tốc`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 3 · Bài 1', de: `Đồ thị ${m('v')}–${m('t')} của thang máy đi lên (hình); chiều dương hướng lên.<br><b>a)</b> gia tốc ${m('a_1')}, ${m('a_2')}<br><b>b)</b> gia tốc ${m('a_3')}<br><b>c)</b> giai đoạn có gia tốc độ lớn lớn nhất<br><b>d)</b> lúc ${sec(9)}: nhanh dần hay chậm dần`, fig: H.thangMay(''), fw: 46, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c', 'd'], ow: 14 },
    { t: 'Dạng 3 · Bài 2', de: `Đồ thị ${m('v')}–${m('t')} của một xe (hình); chiều dương là chiều chuyển động.<br><b>a)</b> gia tốc ${m('a_1')} trong giai đoạn ${V(1)}<br><b>b)</b> gia tốc ${m('a_3')} trong giai đoạn ${V(3)}<br><b>c)</b> lúc ${sec(2)}: nhanh dần hay chậm dần`, fig: H.xeBon(''), fw: 46, o: ['a', 'b', 'c'] },
  ], [
    { t: 'Dạng 4 · Bài 1', de: `Vận tốc xe trên đường thẳng: ${nw(`${m('t=0')}: ${m('v=0')}`)}; ${nw(`${m('t=10\\ \\mathrm s')}: ${ms(8)}`)}; ${nw(`${m('t=25\\ \\mathrm s')}: ${ms(8)}`)}; ${nw(`${m('t=30\\ \\mathrm s')}: ${m('v=0')}`)}; giữa hai mốc liền nhau ${m('v')} đổi đều. Vẽ đồ thị ${m('v')}–${m('t')} vào vở.<br><b>a)</b> gia tốc trong ${sec(10)} đầu và ${sec(5)} cuối<br><b>b)</b> quãng đường trong ${sec(30)}<br><b>c)</b> tốc độ trung bình trong ${sec(30)}`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'], ow: 20 },
    { t: 'Dạng 4 · Bài 2', de: `Tàu điện: ${nw(`${m('t=0')}: ${m('v=0')}`)}; ${nw(`${m('t=20\\ \\mathrm s')}: ${ms(15)}`)}; ${nw(`${m('t=80\\ \\mathrm s')}: ${ms(15)}`)}; ${nw(`${m('t=110\\ \\mathrm s')}: ${m('v=0')}`)}; giữa hai mốc liền nhau ${m('v')} đổi đều.<br><b>a)</b> gia tốc lúc tăng tốc và lúc hãm<br><b>b)</b> quãng đường từ ga này tới ga kia<br><b>c)</b> tốc độ trung bình (làm tròn 0,1 m/s)`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'], ow: 20 },
    { t: 'Dạng 5 · Bài 1', de: `Quả bóng đá bay ngang ${ms(20)} hướng đông, đập vuông góc vào tường, bật lại ${ms(12)} hướng tây; va chạm kéo dài ${sec('0{,}02')}. Chiều dương hướng đông.<br><b>a)</b> độ biến thiên tốc độ<br><b>b)</b> độ biến thiên vận tốc ${m('\\Delta v')}<br><b>c)</b> gia tốc trung bình và hướng của gia tốc`, o: ['a', 'b', 'c'], ow: 30 },
    { t: 'Dạng 5 · Bài 2', de: `Quả bóng rơi chạm sàn với vận tốc ${ms(6)} hướng xuống, nảy lên ${ms(4)} hướng lên; va chạm kéo dài ${sec('0{,}1')}. Chiều dương hướng lên.<br><b>a)</b> vận tốc ${m('v_1')} (trước) và ${m('v_2')} (sau), có dấu<br><b>b)</b> độ biến thiên vận tốc ${m('\\Delta v')}<br><b>c)</b> gia tốc trung bình và hướng của gia tốc`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'], ow: 20 },
    nhap(9),
  ]],
  dap: [
    `D1·1: a) 0,5 m/s² · b) 18 m/s · c) 20 s &nbsp;|&nbsp; D1·2: a) 0,2 m/s² · b) 10 m/s · c) 100 s &nbsp;|&nbsp; D2·1: a) −4 m/s² · b) +4 m/s² · c) 8 m/s &nbsp;|&nbsp; D2·2: a) −0,25 m/s² · b) 10 s · c) +0,25 m/s² &nbsp;|&nbsp; D3·1: a<sub>1</sub>) 1,5 m/s² · a<sub>2</sub>) 0 · b) −1 m/s² · c) ${V(1)} · d) chậm dần &nbsp;|&nbsp; D3·2: a) 2 m/s² · b) −2 m/s² · c) nhanh dần`,
    `D4·1: a<sub>1</sub>) 0,8 m/s² · a<sub>2</sub>) −1,6 m/s² · b) 180 m · c) 6,0 m/s &nbsp;|&nbsp; D4·2: a<sub>1</sub>) 0,75 m/s² · a<sub>2</sub>) −0,5 m/s² · b) 1275 m · c) 11,6 m/s &nbsp;|&nbsp; D5·1: a) −8 m/s (giảm 8 m/s) · b) −32 m/s · c) −1600 m/s², hướng tây &nbsp;|&nbsp; D5·2: a<sub>1</sub>) −6 m/s · a<sub>2</sub>) +4 m/s · b) +10 m/s · c) 100 m/s², hướng lên`,
  ],
};

await K.dung({
  trang1to5: ttCot + [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 2], kq: [[1, 2, 3], [4, 5]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'chuyển động biến đổi 1·4 · vết bi 1·5 · gia tốc 2·1 · xe lăn 2·2 · nhanh/chậm dần 2·3 · đồ thị v–t 3·1 · bẫy 3·2 · bài toán mẫu 4·2 · dạng 1–3 → 6·1 · dạng 4–5 → 7·1',
  out: process.argv[2],
});
