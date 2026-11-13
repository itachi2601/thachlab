// Ruột tập VL11 – Bài 6 · Dao động tắt dần. Dao động cưỡng bức. Hiện tượng cộng hưởng (lesson id 25). Quyển Chương 1 lớp 11:
// bài 1 = tr. 1–12 → bài 6 = tr. 61–72.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự giải vào vở · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l11-bai6.mjs (toàn bộ SVG tự vẽ). Nội dung theo bài web (book/cache/25.json, tải từ DB 13/11/2026): mục tiêu, dự đoán xích đu,
// II.1–II.6 (tắt dần, thí nghiệm ba môi trường, duy trì, cưỡng bức, cộng hưởng, quét tần số), ba bẫy, Trả bài 7 câu, bài toán mẫu bệ máy,
// điền bước, thử thách, lợi – hại, mang về, 5 dạng bài tập mẫu. Đáp số Bài tương tự tính bằng Python 13/11/2026 (mô hình A(f) và e^(−βt) như bài web).
// Chạy: node scripts/ruot-tap/l11-bai6.mjs [file.pdf]   → scripts/ruot-tap/out/ruot-tap-vl11-bai6.pdf
//       node scripts/ruot-tap/l11-bai6.mjs --hinh       → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l11-bai6/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL11b6 as H } from './hinh-l11-bai6.mjs';

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
  const out = resolve(HERE, 'out/hinh-l11-bai6'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 6, lid: 25, ten: 'DAO ĐỘNG TẮT DẦN · CƯỠNG BỨC · CỘNG HƯỞNG', lop: 11, baiDau: 1, sub: 'Vật lí 11 · Chương 1: Dao động' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const f0 = m('f_0'), T0 = m('T_0'), w0 = m('\\omega_0');
const u = (s) => nw(m(s.replace(/ ([a-zA-Z/]+)$/, '\\ \\mathrm{$1}').replace(/ \\%$/, '\\,\\%')));   // số + đơn vị không gãy dòng: u('2,0 Hz')
const v = (s) => s.replace(/(\d),(\d)/g, '$1{,}$2').replace(/×/g, '\\times ').replace(/≤/g, '\\le ').replace(/ %$/, ' \\%');
const U = (s) => u(v(s));
// bảng quét tần số nằm ngang: hàng f, hàng A
const bangF = (fsr, As, dv = 'cm', pm = '') => `<table class="bf" style="margin:.5mm 0;font-size:var(--fs-sm)"><tr><th style="width:16mm">${m('f\\ (\\mathrm{Hz})')}</th>${fsr.map((x) => `<td style="text-align:center">${x}</td>`).join('')}</tr>
<tr><th>${m(`A\\ (\\mathrm{${dv}})`)}</th>${As.map((x) => `<td style="text-align:center">${x}${pm}</td>`).join('')}</tr></table>`;

const p1 = `<section class="page">
${head('BÀI 6 · DAO ĐỘNG TẮT DẦN · CƯỠNG BỨC · CỘNG HƯỞNG', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Phân biệt dao động <b>tắt dần</b>, <b>duy trì</b>, <b>cưỡng bức</b> theo nguyên nhân, chu kì, biên độ`)}
${dong(`${ck}Nêu điều kiện <b>cộng hưởng</b>; đọc đồ thị biên độ theo tần số với hai mức lực cản`)}
${dong(`${ck}Đọc <b>bảng quét tần số</b>, so hai số đọc với sai số`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Ngồi yên thì xích đu thấp dần rồi dừng; nhún đúng lúc đu đi xuống thì độ cao giữ gần như cũ. Vì sao?</p>
<div class="fig-side" style="${fs(40)}"><div>
${opt('A', 'Đu không có chu kì, nên ngồi yên là dừng ngay')}
${opt('B', 'Nhún đẩy liên tục; tần số nào cũng làm đu cao mãi')}
${opt('C', 'Ma sát lấy năng lượng; nhún chỉ bù trong một phần nhịp')}
${opt('D', 'Nhún đổi chu kì của đu, nhờ vậy đu giữ độ cao')}
<div style="margin-top:1mm">${chon(10)}</div></div>
${H.xichDu()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f(12)} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Dao động tắt dần', '1·4')}
<div class="card" style="padding:1.2mm 3mm">
<div>Biên độ và ${f(25)} giảm dần theo thời gian.</div>
<div>Nguyên nhân: ma sát, lực cản sinh công ${f(14)}; cơ năng chuyển thành ${f(25)}.</div>
<div>${ck}Có &nbsp;${ck}không có chu kì xác định, vì dao động ${f(28)} lặp lại y hệt. Ma sát quá lớn: vật ${f(45)}</div>
<div>Có lợi: ${f(28)} · có hại (cần dao động lâu) thì khắc phục: ${f(25)}</div></div>
${h3(5, 'Thí nghiệm: cùng một con lắc, ba môi trường', '1·5')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div><b>Làm:</b> thả lệch ${U('5,0 cm')} trong không khí, nước, dầu. Đọc biên độ còn lại sau ${U('2 s')}:</div>
<table style="margin:.6mm 0"><tr><th style="width:24mm">Môi trường</th><th>Không khí</th><th>Nước</th><th>Dầu nhớt</th></tr>
<tr><th>${m('A')} sau 2 s</th><td>${U('2,2 cm')}</td><td>${U('0,5 cm')}</td><td>${U('0,0 cm')}</td></tr>
<tr><th>Nét trên hình</th><td></td><td></td><td></td></tr></table>
<div><b>Rút ra:</b> môi trường càng ${f(20)}, biên độ giảm càng ${f(20)}.</div></div>
${H.baMoiTruong('Cùng lệch 5,0 cm, cùng lúc thả.')}</div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('DUY TRÌ · CƯỠNG BỨC · CỘNG HƯỞNG')}
${h3(1, 'II.2 · Dao động duy trì', '2·1')}
<div class="card fig-side" style="${fs(40)};padding:1.2mm 3mm"><div>
<div><span class="hint">Chu kì riêng ${T0}: chu kì hệ tự dao động khi không có ngoại lực, bỏ qua ma sát.</span></div>
<div>Dao động tắt dần được ${f(16)} đúng phần năng lượng đã mất sau mỗi chu kì.</div>
<div>Lực bù cùng chiều chuyển động, chỉ trong ${f(25)} chu kì, không đẩy suốt.</div>
<div>Biên độ ${f(20)}; chu kì bằng ${f(25)}.</div>
<div style="margin:.8mm 0">Tần số riêng ${nw(`${m('f_0=')} ${f(14)}`)} &nbsp;(Hz) &nbsp;· tần số góc riêng ${nw(`${m('\\omega_0=')} ${f(14)}`)} &nbsp;(rad/s)</div>
<div>Ví dụ: ${f(30)} · ${f(30)}</div></div>
${H.dongHo()}</div>
${h3(2, 'II.3 · Dao động cưỡng bức', '2·2')}
<div class="card" style="padding:1.2mm 3mm">
<div>Ngoại lực ${f(25)} tác dụng ${f(25)}: &nbsp;${m('F=F_0\\cos(\\omega t+\\varphi_0)')}</div>
<div>${m('F_0')} là ${f(30)} (N) · ${nw(`${m('\\omega=2\\pi f')}`)} là ${f(30)} (rad/s) · ${m('\\varphi_0')}: pha ban đầu (rad)</div>
<div>Khi ổn định: ${nw(`${'<i>f</i><sub>vật</sub> ='} ${f(18)}`)}, ${ck}luôn bằng &nbsp;${ck}có thể khác ${f0}.</div>
<div>Biên độ lớn khi: ${m('F_0')} ${f(14)} · lực cản ${f(14)} · ${m('|f-f_0|')} ${f(14)}</div></div>
${h3(3, 'II.4 · Cộng hưởng', '2·3')}
<div class="card fig-side" style="${fs(48)};padding:1.2mm 3mm"><div>
<div>Biên độ dao động cưỡng bức ${f(25)} khi tần số lực ${f(25)} tần số riêng.</div>
<div style="margin:.8mm 0">Điều kiện: ${nw(`${m('f=')} ${f(12)}`)} ${m('\\Leftrightarrow')} ${nw(`${m('\\omega=')} ${f(12)}`)} ${m('\\Leftrightarrow')} ${nw(`${m('T=')} ${f(12)}`)}</div>
<div>Cản nhỏ: đỉnh ${f(16)}, ${f(16)}</div>
<div>Cản lớn: đỉnh ${f(16)}, ${f(16)}</div></div>
${H.congHuong()}</div>
${h3(4, 'Làm nhanh', '2·4')}
${box(cau(`<b>Câu 1.</b> Con lắc có ${nw(`${m('T_0=0{,}50\\ \\mathrm s')},`)} chịu lực cưỡng bức ${nw(`${m('f=3{,}0\\ \\mathrm{Hz}')},`)} đã ổn định. Tần số dao động của con lắc? Có cộng hưởng không?`, 2)
 + cau(`<b>Câu 2.</b> Vì sao nhún xích đu đúng nhịp là dao động duy trì, không phải cưỡng bức, dù cả hai đều có ngoại lực?`, 2))}
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('THÍ NGHIỆM QUÉT TẦN SỐ · BA LOẠI · BẪY')}
${h3(1, 'II.5 · Thí nghiệm: quét tần số lực cưỡng bức', '3·1')}
<div class="fig-side" style="${fs(54)}"><div>
<div>Con lắc có ${nw(`${m('f_0')} chưa biết`)}. Chỉnh lực tới 5 tần số, chờ ổn định, đọc ${m('A')} một lần; sai số đọc ${U('±0,2 cm')}.</div>
<table class="tbl-ct" style="margin:.6mm 0"><tr><th>${m('f\\ (\\mathrm{Hz})')}</th><th>${m('A\\ (\\mathrm{cm})')}</th></tr>
<tr><td>1,0</td><td>2,7 ± 0,2</td></tr><tr><td>1,5</td><td>4,2 ± 0,2</td></tr><tr><td>2,0</td><td>6,0 ± 0,2</td></tr><tr><td>2,5</td><td>4,2 ± 0,2</td></tr><tr><td>3,0</td><td>2,7 ± 0,2</td></tr></table>
<div class="hint">Hai số đọc, mỗi số ±0,2 cm: chỉ chắc khác nhau khi hiệu vượt ${U('2 × 0,2 = 0,4 cm')}.</div>
</div>${H.luoiQuet()}</div>
<div class="card" style="margin-top:.6mm;padding:1mm 3mm">
<div>${m('A')} lớn nhất tại ${nw(`${m('f=')} ${f(12)}&nbsp;Hz`)} ⇒ ${nw(`${m('f_0=')} ${f(12)}&nbsp;Hz`)}</div>
<div>Đỉnh trừ hàng kề: ${nw(`${m('6{,}0-4{,}2=')} ${f(12)}&nbsp;cm`)} ${ck}vượt &nbsp;${ck}không vượt 0,4 cm ⇒ đỉnh ${ck}chắc &nbsp;${ck}chưa chắc</div>
<div>Hàng 1,5 Hz và 2,5 Hz: hiệu ${nw(`${f(12)}&nbsp;cm`)} ⇒ hai biên độ ${ck}khác nhau &nbsp;${ck}coi là bằng nhau</div></div>
${h3(2, 'II.6 · Ba loại, nhìn một lượt', '3·2')}
<table class="mo3"><tr><th style="width:21mm">Loại</th><th style="width:12mm">Mẹo</th><th>Nguyên nhân</th><th style="width:26mm">Chu kì</th><th style="width:26mm">Biên độ</th></tr>
<tr><td><b>Tắt dần</b></td><td>Mất</td><td></td><td></td><td></td></tr>
<tr><td><b>Duy trì</b></td><td>Bù</td><td></td><td></td><td></td></tr>
<tr><td><b>Cưỡng bức</b></td><td>Theo</td><td></td><td></td><td></td></tr></table>
<div style="margin:.4mm 0 0">Cưỡng bức có ${m('f=f_0')}: <b>Trùng</b> = ${f(25)}</div>
${h3(3, 'III · Ba cái bẫy hay sập', '3·3')}
<div class="card" style="padding:1mm 3mm">
<div class="trap">${ck}<span><b>“Có ngoại lực nên là cưỡng bức.”</b> Hỏi: lực đẩy suốt hay một phần nhịp; chu kì theo hệ hay theo lực? Nhún xích đu đúng nhịp là ${f(20)}.</span></div>
<div class="trap">${ck}<span><b>“Lực mạnh là cộng hưởng.”</b> ${nw(`${m('f_0=10\\ \\mathrm{Hz}')},`)} lực rất mạnh, ${nw(`${m('f=25\\ \\mathrm{Hz}')}:`)} ${m('A')} ${ck}cực đại ${ck}không cực đại; vật dao động với ${nw(`${f(12)}&nbsp;Hz`)}.</span></div>
<div class="trap">${ck}<span><b>“Tắt chậm vẫn là điều hoà.”</b> Biên độ đổi ⇒ không tuần hoàn ⇒ ${ck}có &nbsp;${ck}không có chu kì xác định.</span></div></div>
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('TRẢ BÀI · TỰ KIỂM TRA · BÀI TOÁN MẪU')}
${h3(1, 'IV · Trả bài 7 câu', '4·1')}
${box(`${tb('1. Tắt dần là gì? Năng lượng mất vì đâu?')}${lines(1)}
${tb('2. Vì sao tắt dần không có chu kì xác định? Ma sát quá lớn thì sao?')}${lines(1)}
${tb('3. Duy trì khác cưỡng bức chỗ nào? Chu kì, biên độ của duy trì?')}${lines(2)}
${tb('4. Viết dạng lực cưỡng bức. Khi ổn định, tần số vật bằng gì?')}${lines(1)}
${tb('5. Biên độ cưỡng bức phụ thuộc gì? Khi nào cộng hưởng?')}${lines(2)}
${tb('6. Một lợi, một hại của cộng hưởng? Tắt dần dùng vào việc gì?')}${lines(1)}
${tb('7. Mất – Bù – Theo – Trùng nghĩa là gì?')}${lines(1)}`)}
${h3(2, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '4·2')}
${rkHai([1, 2, 3, 4], [5, 6, 7, 8])}
${h3(3, 'V · Bài toán mẫu: tìm tần số riêng của bệ máy', '4·3')}
<div class="card soft fig-side" style="${fs(42)};padding:1.2mm 3mm"><div>Bệ máy chưa biết ${f0}. Lực ${m('F=20\\cos(2\\pi f t)')} N; ${m('F_0')} và lực cản không đổi; sai số đọc ${U('±0,2 cm')}.
${bangF(['8', '10', '12', '14', '16'], ['1,0', '2,4', '5,0', '2,4', '1,0'])}
<div><b>a)</b> Tìm ${f0}. Chỉnh lực tới tần số nào thì cộng hưởng?</div>
<div><b>b)</b> Ở ${U('f = 16 Hz')}, tần số dao động của bệ?</div>
<div><b>c)</b> ${m('A')} lúc 16 Hz so với lúc cộng hưởng? Hiệu có vượt sai số không?</div></div>${H.beMay()}</div>
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl('a) Đỉnh bảng, hiệu với hàng kề so với 0,4 cm:', 2)}${wl('b)', 1)}${wl('c)', 2)}</div>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('ĐIỀN BƯỚC · BÀI TẬP VỀ NHÀ · THỬ THÁCH · MANG VỀ')}
<h3><i>1</i>Điền bước còn thiếu: cùng bảng, động cơ ở ${U('f = 10 Hz')}</h3>
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div class="ln"><b>Bước 1 (cho sẵn):</b> ${nw(m('|10-12|=2\\ \\mathrm{Hz}'))}; bảng: ${U('A = 2,4 cm')}</div>
<div class="ln"><b>Bước 2:</b> tần số bệ lúc ổn định ${nw(`${f(14)}&nbsp;Hz`)} ${ck}bằng tần số lực &nbsp;${ck}bằng ${f0}</div>
<div class="ln"><b>Bước 3:</b> 2,4 cm so với 5,0 cm ${ck}lớn hơn ${ck}nhỏ hơn; hiệu ${nw(`${f(12)}&nbsp;cm`)} ${ck}vượt ${ck}không vượt 0,4 cm</div></div>
${K.btvn().replace('<i>1</i>', '<i>2</i>')}
${h3(3, 'Thử thách phân tầng', '5·3')}
<div class="fig-side" style="${fs(44)}">${box(wl(`${m('\\bigstar')} Con lắc có ${U('f_0 = 2 Hz')}, lực cưỡng bức có ${U('f = 2 Hz')}. Có cộng hưởng không? Vì sao?`, 2)
 + wl(`${m('\\bigstar\\bigstar')} ${U('f_0 = 5 Hz')}, cùng ${m('F_0')} và lực cản. Lần 1 lực có ${U('f = 5 Hz')}, lần 2 có ${U('f = 8 Hz')}. Tần số vật lần 2? Lần nào ${m('A')} lớn hơn?`, 3)
 + wl(`${m('\\bigstar\\bigstar\\bigstar')} Động cơ chạy ${U('25 Hz')}: chọn bệ có ${U('f_0 = 25 Hz')} hay ${U('8 Hz')}? Dầu trong ống nhớt nhiều hay ít? Vì sao?`, 4))}${H.dongCo()}</div>
${h3(4, 'VI · Lợi, hại', '5·4')}
<div class="card" style="padding:1mm 3mm">
<div>Tắt dần có lợi: ${f(30)} · ${f(30)}</div>
<div>Cộng hưởng có hại: nhà, cầu, bệ máy phải có ${f0} ${f(30)} tần số lực <span class="hint">(cầu Tacoma 1940: SGK coi là cộng hưởng)</span></div>
<div>Cộng hưởng có lợi: hộp đàn · ${f(25)} · ${f(25)}</div></div>
${h3(5, 'Mang về: điều em dễ quên nhất', '5·5')}
${box(wl('1.', 2) + wl('2.', 2) + wl('3.', 2))}
${foot(5)}</section>`;

const deH = (txt, fig, w = 46) => `<div class="fig-side" style="grid-template-columns:1fr ${w}mm"><div>${txt}</div>${fig}</div>`;
const bangDoc = (fsr, As) => `<table class="bf" style="font-size:var(--fs-sm);text-align:center"><tr><th>${m('f')} (Hz)</th><th>${m('A')} (cm)</th></tr>${fsr.map((x, i) => `<tr><td>${x}</td><td>${As[i]}</td></tr>`).join('')}</table>`;
const dang = [
  { t: 'Dạng 1 · Dễ · Phân loại dao động',
    de: `Ba con lắc lò xo giống nhau, ${U('T_0 = 1,0 s')}, đồ thị bên. (1) Kéo lệch rồi thả trong không khí. (2) Như (1), có cơ cấu bù đúng phần năng lượng mất mỗi chu kì. (3) Trên bệ rung ${U('1,5 Hz')} (lực liên tục), đã ổn định.<br><b>a)</b> mỗi con lắc dao động loại gì<br><b>b)</b> chu kì dao động của con lắc (3)`,
    nd: `Xét cách ${f(25)} được cấp; cưỡng bức ổn định: ${nw(`${'<i>f</i><sub>vật</sub> ='} ${f(16)}`)}`, a: ['a<sub>(1)</sub>', 'a<sub>(2)</sub>', 'a<sub>(3)</sub>', 'b'], gi: 2, fig: H.d1(''), fw: 30 },
  { t: 'Dạng 2 · Trung bình · Bảng quét tần số',
    de: `Cột biển quảng cáo trên bàn rung, cùng lực; đọc ${m('A')} đỉnh cột lúc ổn định, sai số ${U('±0,2 cm')} (chắc khác nhau khi hiệu vượt ${U('0,4 cm')}).`
      + `<br><b>a)</b> tần số riêng ${f0} của cột<br><b>b)</b> xe tải làm đất rung đều ${U('5,0 Hz')}: tần số dao động của cột<br><b>c)</b> đất rung ${U('4,0 Hz')}: ${m('A')} tăng/giảm bao nhiêu so với 5,0 Hz; vượt sai số?`, fw: 30, fig: bangDoc(['2,0', '3,0', '3,5', '4,0', '5,0', '6,0'], ['3,3', '5,4', '6,0', '5,4', '3,3', '2,2']),
    nd: `${f0} ở chỗ ${m('A')} ${f(18)}; ${nw(`${'<i>f</i><sub>vật</sub> ='} ${f(14)}`)}; ${m('A')} lớn khi ${m('|f-f_0|')} ${f(14)}`, a: ['a', 'b', 'c'], gi: 3 },
  { t: 'Dạng 3 · Trung bình · Biên độ tắt dần, cơ năng còn lại',
    de: `Biên độ con lắc: ${m('A=A_0e^{-\\beta t}')}, ${U('A_0 = 5,0 cm')}, ${nw(`${m('\\beta=0{,}20\\ \\mathrm{s^{-1}}')};`)} ${nw(m('\\ln 2\\approx0{,}693'))}; cơ năng tỉ lệ ${m('A^2')}.<br><b>a)</b> biên độ sau ${U('5,0 s')}<br><b>b)</b> sau bao lâu biên độ còn một nửa ${m('A_0')}<br><b>c)</b> lúc đó cơ năng còn bao nhiêu phần trăm`,
    nd: `${m('e^{-\\beta t}=1/2')} ⇒ ${nw(`${m('t=')} ${f(16)}`)}; ${nw(`${m('W/W_0=(')}${f(16)}${m(')^2')}`)}`, a: ['a', 'b', 'c'], gi: 3, fig: H.d3(''), fw: 30 },
  { t: 'Dạng 4 · Khó · Xe qua gờ giảm tốc',
    de: `Gờ giảm tốc cách đều ${U('L = 6,0 m')}; thân xe trên lò xo có ${U('T_0 = 0,80 s')}; mỗi gờ đẩy xe một lần. Cho ${nw(m('1\\ \\mathrm{m/s}=3{,}6\\ \\mathrm{km/h}'))}.<br><b>a)</b> xe chạy ${U('36 km/h')}: chu kì của ngoại lực<br><b>b)</b> vận tốc (km/h) để thân xe rung mạnh nhất<br><b>c)</b> ${U('36 km/h')} hay ${U('54 km/h')} (lực, lực cản như nhau) rung mạnh hơn; vì sao`,
    nd: `${nw(`${'<i>T</i><sub>lực</sub> ='} ${f(14)}`)}; cộng hưởng khi ${nw(`${f(14)}${m('=T_0')}`)}; so ${m('|f-f_0|')}, không so độ nhanh`, a: ['a', 'b', 'c'], gi: 5, fig: H.d4('') },
  { t: 'Dạng 5 · Nâng cao · Chọn đệm chống rung',
    de: `Máy bơm trên bệ có đệm; chạy ổn định thì lực có tần số ${U('20 Hz')}; khởi động thì tần số lực tăng từ 0 lên 20 Hz. Biên độ bệ: ${m('A(f)=\\dfrac{A_r\\,b}{\\sqrt{(f-f_0)^2+b^2}}')}. Hai đệm cùng ${U('f_0 = 5,0 Hz')}: X có ${U('A_r = 7,5 cm')}, ${U('b = 0,40 Hz')}; Y có ${U('A_r = 2,0 cm')}, ${U('b = 1,5 Hz')}. Yêu cầu: chạy ổn định ${U('A ≤ 0,30 cm')}; khởi động ${U('A ≤ 3,0 cm')}.<br><b>a)</b> biên độ lúc chạy ổn định của X, Y<br><b>b)</b> biên độ lớn nhất lúc khởi động của X, Y<br><b>c)</b> chọn đệm nào; vì sao`,
    nd: `Khởi động: ${m('f')} quét qua ${f(12)} ⇒ ${nw(`${m('A_{\\max}=')} ${f(12)}`)}; chạy ổn định: thế ${nw(`${m('f=')} ${f(12)}`)}`, a: ['a<sub>X</sub>', 'a<sub>Y</sub>', 'b<sub>X</sub>', 'b<sub>Y</sub>', 'c'], gi: 6, fig: H.d5(''), cot: 5 },
];

// Bài tương tự giải vào vở (thầy chốt 10/11): 1 cột, ô đáp số 25 mm cuối đúng dòng của ý (nhãn khớp a) b) c)…; a<sub>1</sub>, a<sub>2</sub> khi ý có 2 kết quả).
const ttCss = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.6mm}.tt:has(.nhap-t) .hd>span+span{display:none}.mo3 td{height:12.5mm}.bf th,.bf td{padding:0 1.5mm;line-height:1.12}.bt .ans .fill{height:7.5mm}</style>';
const oY = (s, o, w = 25) => s.split('<br>').map((p) => {
  const y = p.match(/^<b>([a-d])\)<\/b>/);
  if (!y) return `<div>${p}</div>`;
  const ls = o.filter((l) => l[0] === y[1]);
  return `<div class="yo"><span>${p}</span><span class="oo">${ls.map((l) => `<span class="nw"><b>${l})</b>${f(w)}</span>`).join('')}</span></div>`;
}).join('');
const ttDe = (b) => b.fig ? `<div class="fig-side" style="grid-template-columns:1fr ${b.fw}mm">${`<div>${oY(b.de, b.o, b.ow)}</div>`}${b.fig}</div>` : oY(b.de, b.o, b.ow);
const vaoVo = (ds) => ds.map((b) => (b.o ? { t: b.t, de: ttDe(b), k: 0 } : b));
const nhap = (n) => ({ t: '<span class="nhap-t">Nháp / chỗ em còn vướng</span>', de: lines(n), k: 0 });
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–2', 'DẠNG 3–5'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Gọi tên loại dao động và chu kì (nếu có):<br><b>a)</b> quả lắc đồng hồ, dây cót bù năng lượng mỗi nhịp, ${U('T_0 = 2,0 s')}<br><b>b)</b> màng loa rung theo dòng điện xoay chiều ${U('50 Hz')}, đã ổn định<br><b>c)</b> thân xe máy nảy lên sau ổ gà rồi giảm xóc làm êm ngay`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], ow: 22 },
    { t: 'Dạng 1 · Bài 2', de: `Con lắc lò xo có ${U('T_0 = 0,50 s')} đặt trên bệ rung ${U('3,0 Hz')}, đã ổn định.<br><b>a)</b> loại dao động<br><b>b)</b> tần số và chu kì dao động của con lắc<br><b>c)</b> tắt bệ rung, con lắc dao động tiếp trong không khí: loại gì; có chu kì xác định không`, o: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c<sub>1</sub>', 'c<sub>2</sub>'], ow: 22, fig: H.beRung(''), fw: 30 },
    { t: 'Dạng 2 · Bài 1', de: `Quét tần số lực lên một giá đỡ, cùng lực, đọc ${m('A')} lúc ổn định (sai số ${U('±0,1 cm')}; chắc khác nhau khi hiệu vượt ${U('0,2 cm')}):`
      + bangF(['4,0', '5,0', '6,0', '7,0', '8,0'], ['2,0', '3,2', '4,5', '3,2', '2,0'])
      + `<b>a)</b> tần số riêng ${f0}<br><b>b)</b> lực có tần số ${U('8,0 Hz')}: tần số dao động của giá<br><b>c)</b> giảm tần số lực từ 8,0 Hz xuống 7,0 Hz: ${m('A')} tăng hay giảm bao nhiêu; có vượt sai số không`, o: ['a', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'] },
    { t: 'Dạng 2 · Bài 2', de: `Ghế xe buýt trên bàn rung, cùng lực, đọc ${m('A')} lúc ổn định (sai số ${U('±0,2 mm')}; chắc khác nhau khi hiệu vượt ${U('0,4 mm')}):`
      + bangF(['1,0', '2,0', '3,0', '4,0', '5,0'], ['0,9', '1,5', '2,4', '1,5', '0,9'], 'mm')
      + `<b>a)</b> tần số riêng ${f0} của ghế<br><b>b)</b> động cơ làm sàn rung ${U('4,0 Hz')}: tần số và chu kì dao động của ghế<br><b>c)</b> ở 1,0 Hz và 5,0 Hz: hiệu hai biên độ; hai biên độ có khác nhau thật không`, o: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c<sub>1</sub>', 'c<sub>2</sub>'], ow: 20 },
    nhap(1),
  ], [
    { t: 'Dạng 3 · Bài 1', de: `${U('A_0 = 6,0 cm')}, ${m('A=A_0e^{-\\beta t}')}, ${nw(`${m('\\beta=0{,}10\\ \\mathrm{s^{-1}}')};`)} ${nw(m('\\ln2\\approx0{,}693'))}; cơ năng tỉ lệ ${m('A^2')}.<br><b>a)</b> biên độ sau ${U('10 s')}<br><b>b)</b> thời điểm biên độ còn một nửa<br><b>c)</b> cơ năng còn bao nhiêu phần trăm lúc ${U('t = 10 s')}`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 3 · Bài 2', de: `Con lắc trong nước: ${U('A_0 = 4,0 cm')}, ${nw(`${m('\\beta=0{,}50\\ \\mathrm{s^{-1}}')}.`)}<br><b>a)</b> biên độ sau ${U('2,0 s')}<br><b>b)</b> cơ năng còn bao nhiêu phần trăm sau ${U('2,0 s')}<br><b>c)</b> sau bao lâu cơ năng còn ${U('25 %')}`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 4 · Bài 1', de: `Gờ giảm tốc cách đều ${U('5,0 m')}; thân xe có ${nw(`${U('T_0 = 0,50 s')}.`)}<br><b>a)</b> xe chạy ${U('54 km/h')}: chu kì của ngoại lực<br><b>b)</b> vận tốc (km/h) gây cộng hưởng<br><b>c)</b> ${U('30 km/h')} hay ${U('54 km/h')} rung mạnh hơn`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 4 · Bài 2', de: `Người gánh nước, mỗi bước dài ${U('0,60 m')}; nước trong thùng có chu kì riêng ${nw(`${U('T_0 = 0,60 s')}.`)}<br><b>a)</b> đi với vận tốc nào (m/s) thì nước sóng sánh mạnh nhất<br><b>b)</b> đi ${U('1,5 m/s')}: chu kì của lực<br><b>c)</b> ${U('0,80 m/s')} hay ${U('1,5 m/s')} nước sóng sánh mạnh hơn`, fig: H.ganhNuoc(''), fw: 28, o: ['a', 'b', 'c'] },
    { t: 'Dạng 5 · Bài 1', de: `Máy giặt vắt ${U('15 Hz')}, khởi động từ 0; bệ ${nw(`${U('f_0 = 3,0 Hz')};`)} ${m('A(f)=\\frac{A_r b}{\\sqrt{(f-f_0)^2+b^2}}')}. Đệm P: ${U('A_r = 6,0 cm')}, ${U('b = 0,30 Hz')}; đệm Q: ${U('A_r = 1,5 cm')}, ${U('b = 1,2 Hz')}. Cần: khởi động ${U('A ≤ 2,0 cm')}, vắt ${U('A ≤ 0,20 cm')}.<br><b>a)</b> biên độ lúc vắt ổn định của P, Q<br><b>b)</b> biên độ lớn nhất lúc khởi động của P, Q<br><b>c)</b> chọn đệm nào`, o: ['a<sub>P</sub>', 'a<sub>Q</sub>', 'b<sub>P</sub>', 'b<sub>Q</sub>', 'c'], ow: 18 },
    { t: 'Dạng 5 · Bài 2', de: `Bệ có ${U('f_0 = 4,0 Hz')}, ${U('A_r = 3,0 cm')}, ${U('b = 0,50 Hz')} (công thức như bài 1). Biên độ khi tần số lực:<br><b>a)</b> ${U('4,0 Hz')}<br><b>b)</b> ${U('4,5 Hz')}<br><b>c)</b> ${U('10 Hz')}<br><b>d)</b> máy chạy trên ${f0}: tần số nhỏ nhất để ${U('A ≤ 0,10 cm')}`, o: ['a', 'b', 'c', 'd'] },
  ]],
  dap: [
    `D1·1: a<sub>1</sub>) duy trì · a<sub>2</sub>) 2,0 s · b<sub>1</sub>) cưỡng bức · b<sub>2</sub>) 0,020 s · c) tắt dần &nbsp;|&nbsp; D1·2: a) cưỡng bức · b<sub>1</sub>) 3,0 Hz · b<sub>2</sub>) 0,33 s · c<sub>1</sub>) tắt dần · c<sub>2</sub>) không &nbsp;|&nbsp; D2·1: a) 6,0 Hz · b) 8,0 Hz · c<sub>1</sub>) tăng 1,2 cm · c<sub>2</sub>) có &nbsp;|&nbsp; D2·2: a) 3,0 Hz · b<sub>1</sub>) 4,0 Hz · b<sub>2</sub>) 0,25 s · c<sub>1</sub>) 0 · c<sub>2</sub>) không`,
    `D3·1: a) 2,2 cm · b) 6,9 s · c) 14 % &nbsp;|&nbsp; D3·2: a) 1,5 cm · b) 14 % · c) 1,4 s &nbsp;|&nbsp; D4·1: a) 0,33 s · b) 36 km/h · c) 30 km/h &nbsp;|&nbsp; D4·2: a) 1,0 m/s · b) 0,40 s · c) 0,80 m/s &nbsp;|&nbsp; D5·1: a<sub>P</sub>) 0,15 cm · a<sub>Q</sub>) 0,15 cm · b<sub>P</sub>) 6,0 cm · b<sub>Q</sub>) 1,5 cm · c) Q &nbsp;|&nbsp; D5·2: a) 3,0 cm · b) 2,1 cm · c) 0,25 cm · d) 19 Hz`,
  ],
};

await K.dung({
  trang1to5: ttCss + [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang: dang.map((d) => (d.fig ? { ...d, de: deH(d.de, d.fig, d.fw), fig: null } : d)), tach: [3, 2], kq: [[1, 2, 3], [4, 5]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'tắt dần 1·4 · ba môi trường 1·5 · duy trì 2·1 · cưỡng bức 2·2 · cộng hưởng 2·3 · quét tần số 3·1 · ba loại 3·2 · bẫy 3·3 · bài toán mẫu 4·3 · dạng 1–3 → 6·1 · dạng 4–5 → 7·1',
  out: process.argv[2],
});
