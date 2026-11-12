// Ruột tập VL11 – Bài 20 · Điện thế (lesson id 39). Quyển Chương 3 lớp 11 (Điện trường): bài 20 = tr. 49–60.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l11-bai20.mjs (toàn bộ SVG tự vẽ, không dùng ảnh Halliday). Nội dung theo bài web (book/cache/39.json, tải từ DB 12/11/2026):
// mục tiêu, dự đoán chim trên dây 500 kV, II.1–II.4, thí nghiệm vôn kế + thí nghiệm nước muối, hai bẫy, Trả bài 6 câu,
// bài toán mẫu hai bản 2 cm – 120 V, thử thách 3 mức, mang về, 5 dạng bài tập mẫu.
// Đáp số Bài tương tự (tuongTu.dap) tính bằng Python 12/11/2026.
// Chạy: node scripts/ruot-tap/l11-bai20.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl11-bai20.pdf
//       node scripts/ruot-tap/l11-bai20.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l11-bai20/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL11b20 as H } from './hinh-l11-bai20.mjs';

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
  const katexCss = pathToFileURL(BOOK + 'node_modules/katex/dist/katex.min.css').href;
  const out = resolve(HERE, 'out/hinh-l11-bai20'); mkdirSync(out, { recursive: true });
  const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true, args: ['--allow-file-access-from-files'] });
  const pg = await b.newPage();
  for (const [name, fn] of Object.entries(H)) {
    writeFileSync(out + '/_tmp.html', `<!doctype html><meta charset="utf-8"><link rel="stylesheet" href="${katexCss}"><style>${css}</style>${fn()}`);
    await pg.goto(pathToFileURL(out + '/_tmp.html').href, { waitUntil: 'networkidle0' });
    await pg.evaluate('document.fonts.ready');
    await (await pg.$('.fig')).screenshot({ path: `${out}/${name}.png` });
    console.log(`${name}.png`);
  }
  await b.close();
  process.exit(0);
}

const K = khoiTao({ bai: 20, lid: 39, ten: 'ĐIỆN THẾ', lop: 11, baiDau: 16, sub: 'Vật lí 11 · Chương 3: Điện trường' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const e19 = nw(m('e=1{,}6\\cdot10^{-19}\\ \\mathrm C'));
const eV = nw(m('1\\ \\mathrm{eV}=1{,}6\\cdot10^{-19}\\ \\mathrm J'));
const uC = (s) => nw(m(`${s}\\ \\mu\\mathrm C`)), nC = (s) => nw(m(`${s}\\ \\mathrm{nC}`));
const V = (s) => nw(m(`${s}\\ \\mathrm V`)), Vm = (s) => nw(m(`${s}\\ \\mathrm{V/m}`)), cm = (s) => nw(m(`${s}\\ \\mathrm{cm}`)), J = (s) => nw(m(`${s}\\ \\mathrm J`));

// Bài tương tự (vở): ô đáp số cuối dòng ý (giống l10-bai23).
const ttCss = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';

const p1 = `${ttCss}<section class="page">
${head('BÀI 20 · ĐIỆN THẾ', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
<div>${ck}Viết và giải thích ${m('V_M=\\dfrac{W_M}{q}')} và ${m('U_{MN}=V_M-V_N=\\dfrac{A_{MN}}{q}')}</div>
<div>${ck}Phân biệt <b>điện thế</b> (của một điểm) với <b>thế năng</b> (của một điện tích)</div>
<div>${ck}Dùng ${m('U=Ed')} trong điện trường đều, biết ${m('d')} đo <b>dọc đường sức</b></div>
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Chim đậu trên dây 500 kV mà không bị điện giật, chủ yếu là vì:</p>
<div class="fig-side" style="${fs(46)}"><div>
${opt('A', 'Lông và chân chim cách điện hoàn toàn')}
${opt('B', 'Điện chỉ chạy trong lõi dây, không ra tới mặt dây ngoài')}
${opt('C', 'Hai chân gần như cùng điện thế, nên hầu như không có hiệu điện thế giữa chúng')}
${opt('D', 'Dây truyền tải có điện thế thấp hơn ổ cắm trong nhà')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 2)}</div>
${H.chimDay()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(2)}</div>
${h3(4, 'II.1 · Công của lực điện (nhắc lại Bài 19)', '1·4')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div>Công của lực điện không phụ thuộc ${f(25)}, chỉ phụ thuộc vị trí điểm ${f(14)} và điểm ${f(14)}.</div>
<div style="margin:.6mm 0">Điện trường đều: ${nw(`${m('A_{MN}=')} ${f(16)}`)}</div>
<div>${m('d')}: ${f(22)} của MN lên chiều ${f(22)}, có dấu: ${m('d\\gt0')} khi N lệch ${f(16)} chiều đường sức so với M.</div>
<div style="margin-top:.6mm">Công bằng độ ${f(14)} thế năng: ${nw(`${m('A_{MN}=')} ${f(12)} ${m('-')} ${f(12)}`)}</div></div>
${H.duongDi()}</div>
${box(wl('Lực điện giống trọng lực ở chỗ nào? (gợi ý: trượt dốc thẳng hay lượn vòng)', 2))}
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('ĐIỆN THẾ · HIỆU ĐIỆN THẾ')}
${h3(1, 'II.2 · Điện thế: thế năng của một culông', '2·1')}
<div class="card fig-side" style="${fs(42)};padding:1.2mm 3mm"><div>
<div>${nw(`${m('V_M=')} ${f(14)} ${m('=')} ${f(14)}`)} &nbsp;(${m('A_{M\\infty}')}: công đưa ${m('q')} từ M ra ${f(16)})</div>
<div>Điện thế là đại lượng của một ${f(16)}, không phụ thuộc ${f(22)} đặt vào.</div>
<div>Đơn vị: ${f(14)}; ${nw(`${m('1\\ \\mathrm V=1')} ${f(12)}`)}</div>
<div>Mốc ${m('V=0')}: thường chọn ${f(20)} hoặc ${f(20)}.</div>
<div>Mốc ở vô cực: nguồn ${m('Q\\gt0')} cho ${nw(`${m('V')} ${f(8)} 0`)}; nguồn ${m('Q\\lt0')} cho ${nw(`${m('V')} ${f(8)} 0`)}</div>
<div>Suy ra thế năng của ${m('q')} đặt tại M: ${nw(`${m('W_M=')} ${f(16)}`)}</div></div>
${H.bacThang()}</div>
${h3(2, 'Làm nhanh', '2·2')}
${box(`<div style="padding-top:.6mm;line-height:1.35"><b>Câu 1.</b> Đặt ${m('q_1=')}${uC('2')} tại M thì thế năng là ${nw(m('40\\ \\mu\\mathrm J'))}. Bỏ ${m('q_1')}, đặt ${m('q_2=')}${uC('-3')} vào đúng M.</div>
<div style="margin:.8mm 0 .4mm">${nw(`${m('V_M=')} ${f(18)}`)} &nbsp;&nbsp; ${nw(`thế năng của ${m('q_2')}: ${m('W=')} ${f(22)}`)}</div>`)}
${h3(3, 'II.3 · Hiệu điện thế', '2·3')}
<div class="card fig-side" style="${fs(42)};padding:1.2mm 3mm"><div>
<div>${nw(`${m('U_{MN}=')} ${f(12)} ${m('-')} ${f(12)} ${m('=')} ${f(14)}`)} &nbsp;⇒&nbsp; ${nw(`${m('A_{MN}=')} ${f(16)}`)}</div>
<div>Đổi thứ tự hai điểm thì đổi dấu: ${nw(`${m('U_{NM}=')} ${f(16)}`)}</div>
<div>Theo chiều đường sức, điện thế ${f(18)}.</div>
<div>Đổi mốc: mọi ${m('V')} ${f(14)}, còn ${m('U')} ${f(18)}.</div>
<div>${eV}: năng lượng electron nhận khi đi qua hiệu điện thế ${f(10)}&nbsp;V.</div>
<div>Electron: ${nw(`${m('q=')} ${f(18)}`)} — giữ đủ dấu của ${m('q')} và của ${m('U')}.</div></div>
${H.dangThe()}</div>
${h3(4, 'III · Bẫy 1: “Đặt electron vào thì điện thế âm”', '2·4')}
<table><tr><th style="width:24mm">Tiêu chí</th><th>Điện thế ${m('V')}</th><th>Thế năng ${m('W')}</th></tr>
<tr><td>Của ai</td><td>một điểm</td><td></td></tr>
<tr><td>Đổi ${m('q')} đặt vào</td><td></td><td>đổi theo ${m('W=qV')}</td></tr>
<tr><td>Đơn vị</td><td></td><td></td></tr>
<tr><td>Dấu do</td><td>điện trường + mốc</td><td></td></tr></table>
${box(wl(`Giải thích cho Nam vì sao đặt electron vào M không làm ${m('V_M')} thành âm:`, 2), 'margin-top:.8mm')}
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('VÔN KẾ ĐO GÌ · LIÊN HỆ U = Ed')}
${h3(1, 'Thí nghiệm: vôn kế chỉ đo được “hiệu”', '3·1')}
<div class="fig-side" style="${fs(42)}"><div>
<table class="tbl-ct"><tr><th style="width:9mm">Lần</th><th>Que đỏ · que đen chạm vào</th><th style="width:17mm">Số chỉ</th></tr>
<tr><td>1</td><td>cực (+) · cực (−) của pin 1,5 V</td><td></td></tr>
<tr><td>2</td><td>đổi hai que cho nhau</td><td></td></tr>
<tr><td>3</td><td>hai điểm trên cùng một dây đồng nối cực (+)</td><td></td></tr></table>
<div style="margin-top:.6mm"><b>Rút ra:</b> vôn kế số hiện ${nw(`V<sub>đỏ</sub> ${m('-')} ${f(14)}`)}; nó đo ${f(14)} giữa hai điểm, không đo ${f(14)} của một điểm. Lần 3 giống chuyện ${f(28)}.</div>
</div>
${H.vonKe()}</div>
${box(cau(`<b>Câu 2.</b> Electron đi từ M (${m('V_M=10\\ \\mathrm V')}) đến N (${m('V_N=60\\ \\mathrm V')}), ${e19}. ${nw(`${m('U_{MN}=')} ${f(14)}`)} &nbsp; ${nw(`${m('A_{MN}=')} ${f(22)} J ${m('=')} ${f(12)} eV`)}`, 1), 'margin-top:.8mm')}
${h3(2, 'II.4 · Liên hệ U = Ed trong điện trường đều', '3·2')}
<div class="card" style="padding:1.2mm 3mm">
<div>${nw(`${m('U=')} ${f(14)}`)} &nbsp;⇔&nbsp; ${nw(`${m('E=')} ${f(14)}`)} &nbsp; Đơn vị ${m('E')}: ${f(16)} (cùng nghĩa với N/C)</div>
<div>${m('d')}: hình chiếu ${f(14)} của MN lên chiều ${f(22)}; MN ${m('\\perp')} đường sức thì ${nw(`${m('U=')} ${f(10)}`)}</div></div>
${h3(3, 'Thí nghiệm đo: điện thế giữa hai lá đồng', '3·3')}
<div class="fig-side" style="${fs(44)}"><div>
<div style="line-height:1.35"><b>Làm:</b> hai lá đồng song song cách ${cm('10')} trong khay nước muối, nối nguồn ${V('6{,}0')}. Que đen chạm lá âm (0 V), que đỏ nhúng cách lá âm ${m('x')}.</div>
<table class="tbl-ct" style="margin-top:.6mm"><tr><th>${m('x')} (cm)</th><th>2</th><th>4</th><th>6</th><th>8</th></tr>
<tr><td>${m('V')} (V)</td><td>1,18</td><td>2,43</td><td>3,57</td><td>4,84</td></tr>
<tr><td>${m('V/x')} (V/m)</td><td></td><td></td><td></td><td></td></tr></table>
<div style="margin-top:.6mm"><b>Rút ra:</b> ${nw(`${m('V/x\\approx U/d=')} ${f(12)}&nbsp;V/m`)}: điện trường gần như ${f(14)}.</div>
<div>Di que đỏ song song lá đồng: số chỉ ${f(20)} ⇒ đường song song bản cực là đường ${f(18)}.</div>
</div>
${H.doThiVx()}</div>
${box(`<div style="padding:.4mm 0;line-height:1.35"><b>Câu 3.</b> Cũng thí nghiệm trên, đặt que đỏ ở ${nw(`${m('x=5')}&nbsp;cm`)}: vôn kế chỉ khoảng ${nw(`${f(14)}&nbsp;V`)}</div>`, 'margin-top:.8mm')}
${h3(4, 'VI · Điện thế trong đời sống', '3·4')}
<div class="card soft" style="padding:1mm 3mm">
<div>Thợ điện sửa đường dây đang mang điện phải làm “${f(20)}” với dây: cơ thể và dây cùng điện thế, ${nw(`${m('U\\approx')} ${f(10)}`)}</div>
<div>Bugi xe máy: hai điện cực cách ${nw(m('0{,}8\\ \\mathrm{mm}'))}, ${m('U')} cỡ ${nw(m('20\\,000\\ \\mathrm V'))} ⇒ ${nw(`${m('E=U/d\\approx')} ${f(18)}&nbsp;V/m`)}: đủ đánh thủng không khí thành tia lửa.</div></div>
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('BẪY 2 · TRẢ BÀI · TỰ KIỂM TRA')}
${h3(1, 'Bẫy 2: “U = E nhân độ dài MN”', '4·1')}
<div class="card fig-side" style="${fs(44)};padding:1.2mm 3mm"><div>
<div>Chỉ đúng khi MN nằm ${f(22)}. MN xiên góc ${m('\\alpha')} với đường sức: ${nw(`${m('d=MN\\cdot')} ${f(14)}`)}</div>
<div style="margin-top:.6mm"><b>Câu 5.</b> ${m('E=1000')}&nbsp;V/m, ${m('MN=5')}&nbsp;cm hợp với đường sức ${m('60^\\circ')}, N lệch theo chiều đường sức. ${nw(`${m('U_{MN}=')} ${f(16)}`)}</div></div>
${H.hinhChieu()}</div>
${h3(2, 'IV · Trả bài 6 câu', '4·2')}
${box(`${tb('1. Công lực điện phụ thuộc gì, không phụ thuộc gì?')}${lines(1)}
${tb('2. Định nghĩa điện thế, công thức, đơn vị, mốc?')}${lines(2)}
${tb('3. Hiệu điện thế và công của lực điện?')}${lines(1)}
${tb('4. Điện thế thay đổi thế nào dọc theo đường sức?')}${lines(1)}
${tb('5. Điện thế và thế năng khác nhau chỗ nào?')}${lines(1)}
${tb('6. Hệ thức giữa E và U, nghĩa của d?')}${lines(1)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/6 câu · chưa thuộc: ${f(25)} ${nw(`→ đọc lại ô ${f(12)} Tập`)}</div>
${h3(3, 'Kết quả tự kiểm tra (8 câu trên web)', '4·3')}
${rkHai([1, 2, 3, 4], [5, 6, 7, 8])}
${K.btvn().replace('<i>1</i>', '<i>4</i>')}
${foot(4)}</section>`;

const de = (txt, n) => `<div style="margin-top:.6mm;line-height:1.3"><b>${txt}</b></div>` + lines(n);
const p5 = `<section class="page">
${head('BÀI TOÁN MẪU · THỬ THÁCH · MANG VỀ')}
${h3(1, 'V · Bài toán mẫu: hai bản song song', '5·1')}
<div class="card soft" style="padding:1.2mm 3mm">Hai bản phẳng song song cách nhau ${cm('2')}, nối nguồn ${V('120')}; mốc điện thế ở bản âm.<br>
<b>a)</b> cường độ điện trường giữa hai bản<br><b>b)</b> điện thế tại M cách bản âm ${cm('0{,}5')}<br><b>c)</b> electron đi từ bản âm sang bản dương: công của lực điện (J và eV)</div>
<table><tr><th style="width:66mm">Câu trong đề</th><th>Dữ liệu → kiến thức</th></tr>
<tr><td>“hai bản phẳng song song”</td><td>điện trường đều → dùng được ${m('U=Ed')}</td></tr>
<tr><td style="height:5.5mm">“cách nhau 2 cm, nguồn 120 V”</td><td></td></tr>
<tr><td style="height:5.5mm">“mốc ở bản âm”</td><td></td></tr>
<tr><td style="height:5.5mm">“electron đi từ bản âm sang bản dương”</td><td></td></tr></table>
<div class="fig-side" style="${fs(40)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl(`a) ${m('E=')}`, 1)}${wl(`b) ${m('V_M=')}`, 1)}${wl(`c) U<sub>đầu–cuối</sub> ${m('=')}`, 1)}${wl(`${m('A=qU=')}`, 1)}${wl('Kiểm tra dấu, độ lớn có hợp lí?', 1)}</div>${H.banMau()}</div>
${h3(2, 'Điền bước còn thiếu (4 cm · 200 V · M cách bản âm 1 cm)', '5·2')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div class="ln"><b>Bước 1 (cho sẵn):</b> ${m('E=200/0{,}04=5000')}&nbsp;V/m</div>
${wl(`Bước 2: ${m('V_M=')}`, 1)}${wl('Bước 3: công lên electron từ bản âm sang bản dương (eV, J):', 1)}</div>
${h3(3, 'Thử thách phân tầng', '5·3')}
${box(de(`${m('\\bigstar')} MN vuông góc đường sức: ${m('U_{MN}')}, công đưa ${uC('2')} từ M đến N?`, 1)
 + de(`${m('\\bigstar\\bigstar')} Đề mẫu: electron rời bản âm, vận tốc đầu 0. Tốc độ tới bản dương? ${nw('('+m('m_e=9{,}1\\cdot10^{-31}\\ \\mathrm{kg}')+')')}`, 1)
 + de(`${m('\\bigstar\\bigstar\\bigstar')} Hai bản đề mẫu nằm ngang; hạt bụi âm ${nw(m('9{,}8\\cdot10^{-13}\\ \\mathrm{kg}'))} lơ lửng (${nw(m('g=9{,}8\\ \\mathrm{m/s^2}'))}). Bản nào ở trên? Hạt thừa bao nhiêu electron?`, 1))}
${h3(4, 'VI · Mang về: điều em dễ quên nhất', '5·4')}
${box(wl('1.', 1) + wl('2.', 1) + wl('3.', 1))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Công của lực điện và độ giảm thế năng',
    de: `${m('q=+')}${uC('2{,}0')} đi cong M → N, điện trường đều ${m('E=')}${Vm('3000')}; hình chiếu MN lên đường sức ${cm('4{,}0')}.<br><b>a)</b> công ${m('A_{MN}')}<br><b>b)</b> thế năng tăng hay giảm, bao nhiêu<br><b>c)</b> ${m('q')} đi thẳng từ N về M: ${m('A_{NM}')}`,
    nd: `Công không phụ thuộc ${f(30)}; N lệch theo chiều đường sức ⇒ ${nw(`${m('d')} ${f(8)} 0`)}`, a: ['a', 'b', 'c'], gi: 4, fig: H.duongD1(''), cot: 3 },
  { t: 'Dạng 2 · Dễ · Điện thế của một điểm, đổi điện tích, thế năng',
    de: `Mốc ở vô cực. ${m('q_1=+')}${nC('2{,}0')} tại M có thế năng ${nw(`${J('3{,}0\\cdot10^{-7}')};`)} ${nw(`${m('V_N=60\\ \\mathrm V')}.`)}<br><b>a)</b> ${m('V_M')}<br><b>b)</b> quả cầu (nguồn) tích điện dương hay âm<br><b>c)</b> bỏ ${m('q_1')}, đặt ${m('q_2=-')}${nC('4{,}0')} vào M: thế năng của ${m('q_2')}<br><b>d)</b> thế năng của ${m('q_2')} tại N`,
    nd: `${m('V')} là của ${f(16)}, không đổi khi đổi điện tích; ${nw(`${m('W=')} ${f(14)}`)} giữ dấu của ${m('q')}`, a: ['a', 'b', 'c', 'd'], gi: 4 },
  { t: 'Dạng 3 · Trung bình · Hiệu điện thế, công A = qU, đơn vị eV',
    de: `Mốc điện thế ở Trái Đất. ${m('V_A=+45\\ \\mathrm V')}, ${nw(`${m('V_B=+15\\ \\mathrm V')};`)} ${e19}, ${nw(`${eV}.`)}<br><b>a)</b> ${m('U_{AB}')}<br><b>b)</b> electron đi từ A đến B: công lực điện theo J và eV<br><b>c)</b> proton đi từ A đến B: công theo eV`,
    nd: `${nw(`${m('U_{AB}=')} V<sub>đầu</sub> ${m('-')} ${f(12)}`)}; electron ${nw(`${m('q=')} ${f(20)}`)}, proton ${nw(`${m('q=')} ${f(20)}`)}`, a: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], gi: 2 },
  { t: 'Dạng 4 · Trung bình · U = Ed: hình chiếu dọc đường sức, bài ngược',
    de: `Hai bản phẳng song song cách ${cm('6{,}0')}, hiệu điện thế ${V('240')}; điện trường giữa hai bản coi là đều. Tam giác MNP vuông tại P nằm giữa hai bản: MP dọc đường sức, cùng chiều đường sức khi đi từ M đến P; ${m('MN=5{,}0\\ \\mathrm{cm}')}, ${m('NP=4{,}0\\ \\mathrm{cm}')}.<br><b>a)</b> cường độ điện trường giữa hai bản<br><b>b)</b> hiệu điện thế ${m('U_{MN}')}<br><b>c)</b> khoảng cách từ M tới mặt đẳng thế phía bản âm có hiệu điện thế với M bằng ${V('60')}`,
    nd: `${m('d_{MN}')} là ${f(16)} (dọc đường sức), không phải ${f(12)}; ngược lại ${nw(`${m('d=')} ${f(12)}`)}`, a: ['a', 'b', 'c'], gi: 7, fig: H.tamD4(), cot: 3 },
  { t: 'Dạng 5 · Khó · Hai bản: điện thế, công lên electron, đổi mốc',
    de: `Hai bản phẳng song song cách ${cm('5{,}0')}, nối nguồn ${V('150')}: bản A nối cực dương, bản B nối cực âm. M cách bản B ${cm('1{,}5')}. Chọn mốc điện thế ở bản A. Lấy ${e19}.<br><b>a)</b> cường độ điện trường<br><b>b)</b> điện thế tại M<br><b>c)</b> electron đi từ bản B đến M: công của lực điện theo eV và J<br><b>d)</b> chọn lại mốc ở bản B: ${m('V_M')} bằng bao nhiêu? Công ở c) có đổi không?`,
    nd: `Khoảng cách tính từ M tới đúng bản ${f(16)}; đổi mốc thì ${m('V')} ${f(12)}, ${m('U')} ${f(14)}`, a: ['a', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>', 'd<sub>1</sub>', 'd<sub>2</sub>'], gi: 7, fig: H.banD5(), cot: 3 },
];

// Bài tương tự giải vào vở (thầy chốt 10/11): 1 cột; ô đáp số cuối đúng dòng của ý, nhãn khớp a) b) c)…;
// đáp số tính bằng Python 12/11/2026 (xem cuối file).
const oY = (s, o, w = 25) => s.split('<br>').map((p) => {
  const y = p.match(/^<b>([a-d])\)<\/b>/);
  if (!y) return `<div>${p}</div>`;
  const ls = o.map((l) => (Array.isArray(l) ? l : [l, w])).filter(([l]) => l[0] === y[1]);
  return `<div class="yo"><span>${p}</span><span class="oo">${ls.map(([l, lw]) => `<span class="nw"><b>${l})</b>${f(lw)}</span>`).join('')}</span></div>`;
}).join('');
const ttDe = (b) => b.fig ? `<div class="fig-side" style="grid-template-columns:1fr ${b.fw}mm">${`<div>${oY(b.de, b.o, b.ow)}</div>`}${b.fig}</div>` : oY(b.de, b.o, b.ow);
const vaoVo = (ds) => ds.map((b) => (b.o ? { t: b.t, de: ttDe(b), k: 0 } : b));
const nhap = (n) => ({ t: '<span class="nhap-t">Nháp / chỗ em còn vướng</span>', de: lines(n), k: 0 });
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–3', 'DẠNG 4–5'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `${m('q=+')}${uC('3{,}0')} đi gấp khúc M → N, ${nw(`${m('E=')}${Vm('2000')};`)} hình chiếu MN lên đường sức ${cm('5{,}0')} (cùng chiều).<br><b>a)</b> công ${m('A_{MN}')}<br><b>b)</b> thế năng tăng hay giảm, bao nhiêu<br><b>c)</b> công ${m('A_{NM}')} khi ${m('q')} đi thẳng từ N về M`, o: ['a', ['b', 36], 'c'] },
    { t: 'Dạng 1 · Bài 2', de: `${m('q=-')}${uC('4{,}0')} đi từ M đến N, ${nw(`${m('E=')}${Vm('5000')};`)} N lệch <b>ngược</b> chiều đường sức ${cm('2{,}0')}.<br><b>a)</b> công ${m('A_{MN}')}<br><b>b)</b> thế năng tăng/giảm, bao nhiêu<br><b>c)</b> N tới P (vuông góc đường sức): ${m('A_{NP}')}`, fig: H.duongTT(''), fw: 36, o: ['a', ['b', 32], 'c'] },
    { t: 'Dạng 2 · Bài 1', de: `Mốc điện thế ở vô cực. Điện tích thử ${m('q_1=+')}${nC('5{,}0')} đặt tại M có thế năng ${nw(`${J('1{,}0\\cdot10^{-6}')}.`)}<br><b>a)</b> điện thế ${m('V_M')}<br><b>b)</b> điện tích nguồn dương hay âm<br><b>c)</b> bỏ ${m('q_1')}, đặt ${m('q_2=-')}${nC('2{,}0')} vào M: thế năng của ${m('q_2')}`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 2 · Bài 2', de: `Mốc ở vô cực. Đặt ${m('q_1=-')}${nC('3{,}0')} tại M thì thế năng là ${nw(`${J('+6{,}0\\cdot10^{-7}')};`)} điện thế tại N là ${nw(`${V('-50')}.`)}<br><b>a)</b> điện thế ${m('V_M')}<br><b>b)</b> điện tích nguồn dương hay âm<br><b>c)</b> thế năng của ${m('q_2=+')}${nC('1{,}5')} đặt tại M<br><b>d)</b> thế năng của ${m('q_2')} đặt tại N`, o: ['a', 'b', 'c', 'd'] },
    { t: 'Dạng 3 · Bài 1', de: `${m('V_A=+80\\ \\mathrm V')}, ${nw(`${m('V_B=+20\\ \\mathrm V')};`)} ${e19}, ${nw(`${eV}.`)}<br><b>a)</b> ${m('U_{AB}')}<br><b>b)</b> electron đi từ A đến B: công (J và eV)<br><b>c)</b> proton đi từ A đến B: công (eV)`, o: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'] },
    { t: 'Dạng 3 · Bài 2', de: `${m('V_M=-20\\ \\mathrm V')}, ${nw(`${m('V_N=+30\\ \\mathrm V')};`)} ${e19}, ${nw(`${eV}.`)}<br><b>a)</b> ${m('U_{MN}')}<br><b>b)</b> electron đi từ M đến N: công (J và eV)<br><b>c)</b> electron đi từ N về M: công (eV)`, o: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'] },
  ], [
    { t: 'Dạng 4 · Bài 1', de: `Hai bản phẳng song song cách ${cm('4{,}0')}, hiệu điện thế ${nw(`${V('200')};`)} điện trường giữa hai bản coi là đều.<br><b>a)</b> cường độ điện trường ${m('E')}<br><b>b)</b> ${m('MN=5{,}0\\ \\mathrm{cm}')} hợp với đường sức ${nw(`${m('60^\\circ')},`)} N lệch theo chiều đường sức: ${m('U_{MN}')}<br><b>c)</b> khoảng cách dọc đường sức giữa hai mặt đẳng thế lệch nhau ${V('50')}`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 4 · Bài 2', de: `Điện trường đều ${nw(`${m('E=')}${Vm('2000')}.`)} Tam giác MNP vuông tại P: ${m('MP=6{,}0\\ \\mathrm{cm}')} dọc đường sức, cùng chiều đường sức khi đi từ M đến P; ${nw(`${m('NP=8{,}0\\ \\mathrm{cm}')}.`)}<br><b>a)</b> ${m('U_{MN}')}<br><b>b)</b> ${m('U_{NP}')}<br><b>c)</b> ${m('U_{PM}')}<br><b>d)</b> Nam tính ${m('U_{MN}=E\\cdot MN')}: ra bao nhiêu (sai)?`, fig: H.tamTT(), fw: 42, o: ['a', 'b', 'c', 'd'] },
    { t: 'Dạng 5 · Bài 1', de: `Hai bản song song cách ${cm('4{,}0')} nối nguồn ${nw(`${V('120')}:`)} bản A nối cực dương, bản B nối cực âm. M cách bản B ${nw(`${cm('1{,}0')}.`)} Chọn mốc ở bản B; ${nw(`${e19}.`)}<br><b>a)</b> cường độ điện trường<br><b>b)</b> điện thế tại M<br><b>c)</b> electron đi từ M đến bản A: công theo eV và J<br><b>d)</b> mốc ở bản A: ${m('V_M')}; công ở c) có đổi không`, o: ['a', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>', 'd<sub>1</sub>', 'd<sub>2</sub>'] },
    { t: 'Dạng 5 · Bài 2', de: `Hai bản song song cách ${cm('6{,}0')} nối nguồn ${nw(`${V('180')}:`)} A dương, B âm. M cách bản A ${nw(`${cm('2{,}0')}.`)} Mốc ở bản A; ${nw(`${e19}.`)}<br><b>a)</b> cường độ điện trường<br><b>b)</b> điện thế tại M<br><b>c)</b> electron đi từ M đến bản B: công theo eV và J<br><b>d)</b> mốc ở bản B: ${m('V_M')}`, fig: H.banTT(), fw: 42, o: ['a', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>', 'd'] },
    nhap(4),
  ]],
  // python3: q*E*d; V=W/q; W=qV; U=V1-V2; A=qU (q=-e electron); U=E*d*cos; E=U/d
  dap: [
    `D1·1: a) 3,0·10<sup>−4</sup> J · b) giảm 3,0·10<sup>−4</sup> J · c) −3,0·10<sup>−4</sup> J | D1·2: a) +4,0·10<sup>−4</sup> J · b) giảm 4,0·10<sup>−4</sup> J · c) 0 | D2·1: a) 200 V · b) dương · c) −4,0·10<sup>−7</sup> J | D2·2: a) −200 V · b) âm · c) −3,0·10<sup>−7</sup> J · d) −7,5·10<sup>−8</sup> J | D3·1: a) 60 V · b<sub>1</sub>) −9,6·10<sup>−18</sup> J · b<sub>2</sub>) −60 eV · c) +60 eV | D3·2: a) −50 V · b<sub>1</sub>) +8,0·10<sup>−18</sup> J · b<sub>2</sub>) +50 eV · c) −50 eV`,
    `D4·1: a) 5,0·10<sup>3</sup> V/m · b) 125 V · c) 1,0 cm | D4·2: a) 120 V · b) 0 · c) −120 V · d) 200 V | D5·1: a) 3,0·10<sup>3</sup> V/m · b) +30 V · c<sub>1</sub>) +90 eV · c<sub>2</sub>) 1,44·10<sup>−17</sup> J · d<sub>1</sub>) −90 V · d<sub>2</sub>) không đổi | D5·2: a) 3,0·10<sup>3</sup> V/m · b) −60 V · c<sub>1</sub>) −120 eV · c<sub>2</sub>) −1,92·10<sup>−17</sup> J · d) +120 V`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 2], kq: [[1, 2, 3], [4, 5]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'công lực điện 1·4 · điện thế 2·1 · hiệu điện thế 2·3 · vôn kế 3·1 · U = Ed 3·2 · bẫy 2·4, 4·1 · thí nghiệm nước muối 3·3 · bài toán mẫu 5·1 · dạng 1–3 → 6·1 · dạng 4–5 → 7·1',
  out: process.argv[2],
});
