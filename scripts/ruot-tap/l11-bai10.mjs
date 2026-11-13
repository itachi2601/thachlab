// Ruột tập VL11 – Bài 10 · Thực hành: đo tần số của sóng âm (lesson id 29). Quyển Chương 2 lớp 11: bài 10 = tr. 25–36 (baiDau 8).
// Khung: khung.mjs (bố cục bài 14: 1–5 học · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Bài THỰC HÀNH: tr.1–5 = nhắc lại f–T · dụng cụ + sơ đồ + hai núm · các bước + ba bẫy · bảng 5 lần đo + sai số · xử lí, kết luận, câu hỏi báo cáo.
// Nội dung theo bài web (book/cache/29.json, tải 13/11/2026). Không có bài tập mẫu trên web → tr.6–9 là 3 dạng xử lí số liệu; đáp số tính bằng Python 13/11/2026.
// Chạy: node scripts/ruot-tap/l11-bai10.mjs [file.pdf]   → scripts/ruot-tap/out/ruot-tap-vl11-bai10.pdf
//       node scripts/ruot-tap/l11-bai10.mjs --hinh       → chụp từng hình ở cỡ in vào out/hinh-l11-bai10/
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL11b10 as H } from './hinh-l11-bai10.mjs';

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
  const out = resolve(HERE, 'out/hinh-l11-bai10'); mkdirSync(out, { recursive: true });
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

const OFF = (10 - 8) * 12;
const K = khoiTao({ bai: 10, lid: 29, lop: 11, baiDau: 8, ten: 'THỰC HÀNH: ĐO TẦN SỐ CỦA SÓNG ÂM', sub: 'Vật lí 11 · Chương 2: Sóng' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const fq = m('f'), Tq = m('T'), Nq = m('N'), Lq = m('L'), kq = m('k'), fb = m('\\bar f'), df = m('\\Delta f');
const Hz = (s) => nw(m(`${s}\\ \\mathrm{Hz}`)), ms = (s) => nw(m(`${s}\\ \\mathrm{ms}`)), mso = (s) => nw(m(`${s}\\ \\text{ms/ô}`)), o = (s) => nw(m(`${s}\\ \\text{ô}`));
const dv = nw(`${fq}: Hz · ${Tq}: s · 1 ms = 10<sup>−3</sup> s · 1 µs = 10<sup>−3</sup> ms`);

const ttCss = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';

const p1 = `${ttCss}<section class="page">
${head('BÀI 10 · THỰC HÀNH: ĐO TẦN SỐ CỦA SÓNG ÂM', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Nêu dụng cụ và các bước đo tần số của một nguồn âm đơn`)}
${dong(`${ck}Từ màn dao động kí, tính chu kì ${Tq} và tần số ${fq}`)}
${dong(`${ck}Xử lí 5 lần đo, ghi kết quả ${nw(m('f=\\bar f\\pm\\Delta f'))}, nêu nguồn sai số`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Mai đặt điện thoại cạnh đàn ukulele rồi gảy dây A. Ứng dụng lên dây báo một con số tính bằng héc (Hz). Theo em, nó xác định con số đó bằng cách nào?</p>
<div class="fig-side" style="${fs(48)}"><div>
${opt('A', 'Đo độ to của tiếng đàn rồi đổi ra Hz')}
${opt('B', 'Đo thời gian âm đi từ dây đàn tới micro')}
${opt('C', 'Đếm màng micro dao động bao nhiêu lần mỗi giây')}
${opt('D', 'Đo bước sóng của âm bằng cảm biến khoảng cách')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 2)}</div>
${H.dienThoai()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(2)}</div>
${h3(4, `II.1 · Nhắc lại: tần số ${fq} và chu kì ${Tq}`, '1·4')}
<div class="card fig-side" style="${fs(48)};padding:1.2mm 3mm"><div>
<div>${fq} là số dao động toàn phần trong ${nw('1 s')}; ${Tq} là thời gian một dao động toàn phần.</div>
<div class="hint" style="margin:.3mm 0">Đơn vị: ${dv}</div>
<div>Liên hệ: ${nw(`${m('f=')} ${f(20)}`)}</div>
<div>Đếm ${Nq} dao động trong thời gian ${m('t')}: ${nw(`${m('f=')} ${f(20)}`)}</div>
<div style="margin-top:.6mm">Trên hình, hai đỉnh liên tiếp (chấm đỏ) cách nhau ${f(20)}.</div></div>
${H.sinSong()}</div>
${h3(5, 'Làm nhanh', '1·5')}
${box(cau(`Một âm đơn có chu kì ${Tq} = ${ms('4')}. Tần số của âm là bao nhiêu?`, 2))}
${foot(1)}</section>`;

const bangDc = (rows) => `<table><tr><th style="width:24mm">Dụng cụ</th><th>Làm gì</th><th style="width:26mm">Nối vào</th></tr>${rows.map((x) => `<tr><td style="height:14.5mm">${x}</td><td></td><td></td></tr>`).join('')}</table>`;
const p2 = `<section class="page">
${head('DỤNG CỤ · SƠ ĐỒ NỐI · HAI NÚM CỦA DAO ĐỘNG KÍ')}
${h3(1, 'II.2 · Dụng cụ và sơ đồ nối', '2·1')}
<div class="fig-side" style="${fs(58)}"><div>
<div class="hint" style="margin-bottom:.8mm">Nguồn âm đơn: âm thoa 440 Hz, hoặc loa + máy phát tần số.</div>
${bangDc(['Nguồn âm đơn', 'Micro', 'Dao động kí', 'Dây tín hiệu'])}
</div>${H.soDo()}</div>
${h3(2, 'II.3 · Hai núm dễ nhầm: TIME/DIV và VOLT/DIV', '2·2')}
<div class="card" style="padding:1.2mm 3mm">
<div class="hint">Đơn vị: TIME/DIV đo bằng ms/ô hay µs/ô · VOLT/DIV đo bằng V/ô · ${nw('1 ms = 10<sup>−3</sup> s')} · ${nw('1 µs = 10<sup>−3</sup> ms')}</div>
<table style="margin-top:.8mm"><tr><th style="width:36mm"></th><th>TIME/DIV</th><th>VOLT/DIV</th></tr>
<tr><td style="height:11mm">Chỉnh trục nào (ngang, dọc)?</td><td></td><td></td></tr>
<tr><td style="height:11mm">Dùng để tính ${fq}? ${ck}có &nbsp;${ck}không</td><td></td><td></td></tr></table>
<div style="margin-top:.8mm">Núm ghi ${nw(m('200\\ \\mu\\text{s/ô}'))} thì ${kq} = ${f(14)} ms/ô.</div></div>
${h3(3, 'II.4 · Không có dao động kí vẫn đo được', '2·3')}
<div class="card" style="padding:1.2mm 3mm">
<div>Ghi âm nguồn âm đơn, phóng to dạng sóng, đếm ${Nq} chu kì liên tiếp trong thời gian ${m('t')}: ${nw(`${m('f=')} ${f(20)}`)}</div>
<div style="margin-top:.6mm">Ứng dụng phân tích phổ: tần số của âm đọc ở ${ck}đỉnh cao nhất của phổ &nbsp;${ck}đỉnh cao nhất của dạng sóng theo thời gian</div></div>
${h3(4, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '2·4')}
${rkHai([1, 2, 3, 4], [5, 6, 7, 8])}
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('CÁC BƯỚC ĐO · HAI CÁI BẪY SỐ LIỆU')}
${h3(1, 'II.5 · Các bước đo', '3·1')}
<div class="card" style="padding:1.2mm 3mm">
<div class="trap"><b>1.</b><span>Nối micro vào kênh ${f(10)} của dao động kí. Gõ âm thoa ${nw('440 Hz')} sát micro.</span></div>
<div class="trap"><b>2.</b><span>Chỉnh VOLT/DIV và TRIGGER cho hình sóng rõ và ${f(14)}. Đặt TIME/DIV ${nw(m('k=1\\ \\text{ms/ô}'))}.</span></div>
<div class="trap"><b>3.</b><span>Đo bề rộng ${Lq} của ${nw(m('N=4'))} chu kì liên tiếp, đọc tới ${nw(m('0{,}1\\ \\text{ô}'))}; gõ lại, đo đủ ${f(8)} lần (bảng tr. ${4 + OFF}).</span></div>
<div class="trap"><b>4.</b><span>Tính ${fq} từng lần, ${fb}, sai số (tr. ${4 + OFF}); ghi kết quả (tr. ${5 + OFF}).</span></div>
<div style="margin-top:.6mm"><b>Nhân – Chia – Đổi – Lật:</b> ${nw(`${Lq}·${kq} = ${f(12)} ms`)} → ${nw(`chia ${Nq}: ${Tq} = ${f(12)} ms`)} → ${nw(`đổi: ${f(12)} s`)} → ${nw(`lật: ${fq} = ${f(14)} Hz`)}</div>
<div style="margin-top:.6mm"><b>Vì sao</b> đo ${Nq} chu kì liên tiếp thay vì một chu kì?</div>${lines(3)}</div>
${h3(2, 'III · Bẫy 1: đếm đỉnh thay vì đếm chu kì', '3·2')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<table style="text-align:center"><tr><th style="width:32mm">Đếm được</th><th>2 đỉnh</th><th>4 đỉnh</th><th>${m('n')} đỉnh</th></tr>
<tr><td style="height:10mm">Số chu kì ${Nq}</td><td></td><td></td><td></td></tr></table>
<div style="margin-top:.8mm;line-height:1.35">TIME/DIV ${mso('0{,}5')}. Em đếm 5 đỉnh liên tiếp (hình), đỉnh đầu tới đỉnh cuối cách nhau ${o('6{,}0')}. ${nw(`${Nq} = ${f(8)}`)} · ${nw(`${Tq} = ${f(12)} ms`)} · ${nw(`${fq} = ${f(14)} Hz`)}</div></div>
${H.man({ start: 1.5, per: 1.5, n: 4 })}</div>
${h3(3, 'III · Bẫy 2: nhầm đơn vị của độ chia', '3·3')}
<div class="card" style="padding:1.2mm 3mm">
<div>Núm TIME/DIV ghi ${nw(m('50\\ \\mu\\text{s/ô}'))}; ba chu kì liên tiếp chiếm ${o('6{,}0')}.</div>
<div style="margin-top:.6mm">${nw(`${kq} = ${f(14)} ms/ô`)} · ${nw(`${Tq} = ${f(14)} ms`)} · ${nw(`${fq} = ${f(16)} Hz`)}</div></div>
${K.btvn().replace('<i>1</i>', '<i>4</i>')}
${foot(3)}</section>`;

const nguyenNhan = ['Đọc ô: nhìn xiên, vạch ngắm dày', 'Sóng nhỏ dần sau mỗi lần gõ', 'Núm TIME/DIV chưa về vị trí CAL', 'Nhãn 440 Hz của âm thoa có dung sai'];
const p4 = `<section class="page">
${head('BẢNG SỐ LIỆU · SAI SỐ')}
${h3(1, 'IV · Số liệu nhóm em (5 lần đo)', '4·1')}
<div class="hint" style="margin-bottom:.8mm">Đặt sẵn: ${nw(m('N=4'))} · ${nw(m('k=1\\ \\text{ms/ô}'))} · ${nw(`${kq} = 10<sup>−3</sup> s/ô`)} · sai số đọc ${nw(m('\\Delta L=0{,}1\\ \\text{ô}'))}</div>
<table class="tbl-ct" style="text-align:center"><tr><th style="width:11mm">Lần</th><th>${Lq} (ô)</th><th>${m('f_i=\\dfrac{N}{L\\,k}')} (Hz)</th><th>${m('\\Delta f_i=|f_i-\\bar f|')} (Hz)</th></tr>
${[1, 2, 3, 4, 5].map((i) => `<tr><td style="height:9mm"><b>${i}</b></td><td></td><td></td><td></td></tr>`).join('')}
<tr><td style="height:9mm"><b>TB</b></td><td>${m('\\bar L=')}</td><td>${m('\\bar f=')}</td><td>${m('\\Delta\\bar f=')}</td></tr></table>
<div class="card soft" style="margin-top:1.2mm;padding:1.2mm 3mm"><div>Sai số dụng cụ: ${nw(`${m('\\Delta f_{dc}=\\bar f\\cdot\\dfrac{\\Delta L}{\\bar L}=')} <span class="fill" style="min-width:26mm;height:10mm"></span>`)} Hz</div></div>
${h3(2, 'Sai số đến từ đâu, khắc phục thế nào?', '4·2')}
<div class="fig-side" style="${fs(46)}"><div>
<table><tr><th>Nguồn sai số</th><th style="width:44mm">Khắc phục</th></tr>${nguyenNhan.map((x) => `<tr><td style="height:9mm;font-size:var(--fs-sm)">${x}</td><td></td></tr>`).join('')}</table>
<div style="margin-top:1mm;line-height:1.35">Cùng một sóng, đo theo (1) hay (2) cho sai số tỉ đối ${m('\\dfrac{\\Delta L}{L}')} nhỏ hơn? ${ck}(1) &nbsp;${ck}(2) &nbsp;Vì ${f(20)}</div></div>
${H.haiCach()}</div>
${h3(3, 'Làm nhanh: sai số tỉ đối theo bề rộng L', '4·3')}
<div class="card" style="padding:1.2mm 3mm">
<div>Đọc lệch ${nw(m('\\Delta L=0{,}1\\ \\text{ô}'))}. Đo 1 chu kì: ${nw(m('L=2{,}3\\ \\text{ô}'))}, ${nw(`${m('\\dfrac{\\Delta L}{L}=')} ${f(14)} %`)}. Đo 4 chu kì: ${nw(m('L=9{,}1\\ \\text{ô}'))}, ${nw(`${m('\\dfrac{\\Delta L}{L}=')} ${f(14)} %`)}</div></div>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head(`KẾT QUẢ ${nw(m('f=\\bar f\\pm\\Delta f'))} · BẪY 3 · BÁO CÁO`)}
${h3(1, 'V · Kết quả đo của nhóm', '5·1')}
<table style="text-align:center"><tr><th>${fb} (Hz)</th><th>${m('\\Delta\\bar f')} (Hz)</th><th>${m('\\Delta f_{dc}')} (Hz)</th><th>${df} = ${m('\\Delta\\bar f+\\Delta f_{dc}')} (Hz)</th></tr>
<tr><td style="height:9mm"></td><td></td><td></td><td></td></tr></table>
<div class="card soft" style="margin-top:1.2mm;padding:1.2mm 3mm"><div>${nw(`${m('f=')}(${f(14)} ± ${f(14)}) Hz`)} &nbsp;· Làm tròn ${df} tới 1–2 chữ số có nghĩa, ${fb} cùng hàng.</div>
<div style="margin-top:.8mm">Giá trị ghi trên nguồn: ${f(14)} Hz. Khoảng ${nw(m('\\bar f\\pm\\Delta f'))} ${ck}có &nbsp;${ck}không chứa giá trị đó.</div></div>
${h3(2, 'III · Bẫy 3: lấy biên độ làm tần số', '5·2')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div style="line-height:1.35">Hai âm đơn có cùng biên độ (hình), vẽ cùng thang thời gian. Âm ${f(8)} cao hơn, vì trong cùng số ô nó có ${f(20)} chu kì.</div>${H.haiAm()}</div>
${h3(3, 'V · Vẽ lại màn của nhóm', '5·3')}
<div style="width:64mm">${H.manTrong()}</div>
${h3(4, 'Câu hỏi báo cáo', '5·4')}
${box(`<div style="padding-top:.6mm"><b>1.</b> Một nguồn sai số <b>ngẫu nhiên</b> và một nguồn sai số <b>hệ thống</b> của nhóm em là gì? Cách giảm từng loại?</div>${lines(2)}
<div style="padding-top:.6mm"><b>2.</b> Nếu khoảng ${nw(m('\\bar f\\pm\\Delta f'))} không chứa giá trị ghi trên nguồn, em nghi ngờ điều gì trước?</div>${lines(2)}`)}
${foot(5)}</section>`;

const tbL = (Ls) => `<table style="text-align:center;margin:.6mm 0"><tr><th style="width:21mm;text-align:left">Lần</th>${Ls.map((_, i) => `<th>${i + 1}</th>`).join('')}</tr><tr><td style="text-align:left">${Lq} (ô)</td>${Ls.map((x) => `<td>${x}</td>`).join('')}</tr></table>`;
const dang = [
  { t: 'Dạng 1 · Dễ · Đọc màn dao động kí: số chu kì, chu kì, tần số',
    de: `TIME/DIV ở ${mso('0{,}5')}. Trên màn đếm 5 đỉnh liên tiếp (chấm đỏ), đỉnh đầu tới đỉnh cuối cách nhau ${o('8{,}0')}.<br><b>a)</b> số chu kì ${Nq} của đoạn đó<br><b>b)</b> chu kì ${Tq}<br><b>c)</b> tần số ${fq}`,
    nd: `${m('n')} đỉnh liên tiếp có ${f(8)} chu kì; ${nw(`${Tq} = ${f(14)} ms`)}; đổi ms ra ${f(6)} rồi lật ngược`, a: ['a', 'b', 'c'], gi: 6, fig: H.man({ start: 1, per: 2, n: 4 }) },
  { t: 'Dạng 2 · Trung bình · Chọn thang đo: một chu kì chiếm mấy ô',
    de: `Loa phát âm đơn ${Hz('800')}. TIME/DIV ở ${mso('0{,}5')}; màn rộng ${o('10')}.<br><b>a)</b> chu kì ${Tq} (ms)<br><b>b)</b> một chu kì chiếm bao nhiêu ô<br><b>c)</b> ${m('N=3')} chu kì liên tiếp chiếm ${Lq} bằng bao nhiêu ô<br><b>d)</b> màn chứa trọn tối đa mấy chu kì liên tiếp`,
    nd: `ô mỗi chu kì = ${nw(`${Tq} : ${kq}`)}; ${nw(`${Lq} = ${f(12)}`)}; ${nw(`${m('N_{max}=')} ${f(10)}`)} (số nguyên)`, a: ['a', 'b', 'c', 'd'], gi: 9 },
  { t: `Dạng 3 · Khó · 5 lần đo: ${fb}, sai số và kết quả ${nw(m('f=\\bar f\\pm\\Delta f'))}`,
    de: `Đo âm thoa bằng dao động kí: ${nw(m('N=4'))}, ${nw(m('k=1\\ \\text{ms/ô}'))}, đọc lệch ${nw(m('\\Delta L=0{,}1\\ \\text{ô}'))}.
${tbL(['8,0', '8,1', '7,9', '8,0', '8,2'])}<b>a)</b> tần số trung bình ${fb}<br><b>b)</b> sai số ngẫu nhiên ${m('\\Delta\\bar f')} (trung bình các ${m('|f_i-\\bar f|')})<br><b>c)</b> sai số dụng cụ ${m('\\Delta f_{dc}')}<br><b>d)</b> sai số tổng ${df}; ghi ${m('f=\\ldots\\pm\\ldots')}`,
    nd: `${nw(`${m('f_i=')} ${f(16)}`)} (đổi ${kq} ra s); ${nw(`${m('\\Delta f_{dc}=\\bar f\\dfrac{\\Delta L}{\\bar L}')}`)}; ${nw(`${df} = ${f(10)} + ${f(10)}`)}`, a: ['a', 'b', 'c', 'd<sub>1</sub>', 'd<sub>2</sub>'], cot: 3, gi: 21 },
];

const oY = (s, ol, w = {}) => s.split('<br>').map((p) => {
  const y = p.match(/^<b>([a-d])\)<\/b>/);
  if (!y) return `<div>${p}</div>`;
  const ls = ol.filter((l) => l[0] === y[1]);
  return `<div class="yo"><span>${p}</span><span class="oo">${ls.map((l) => `<span class="nw"><b>${l})</b>${f(typeof w === 'object' ? (w[l] ?? 25) : w)}</span>`).join('')}</span></div>`;
}).join('');
const ttDe = (b) => b.fig ? `<div class="fig-side" style="grid-template-columns:1fr ${b.fw}mm"><div>${oY(b.de, b.o, b.ow)}</div>${b.fig}</div>` : oY(b.de, b.o, b.ow);
const vaoVo = (ds) => ds.map((b) => (b.o ? { t: b.t, de: ttDe(b), k: 0 } : b));
const nhap = (n) => ({ t: '<span class="nhap-t">Nháp / chỗ em còn vướng</span>', de: lines(n), k: 0 });
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–3', 'DẠNG 3 · GHI ÂM ĐẾM CHU KÌ'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `TIME/DIV ở ${mso('0{,}2')}. Trên màn, 4 đỉnh liên tiếp: đỉnh đầu tới đỉnh cuối cách nhau ${o('6{,}0')}.<br><b>a)</b> số chu kì ${Nq}<br><b>b)</b> chu kì ${Tq}<br><b>c)</b> tần số ${fq}`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 1 · Bài 2', de: `TIME/DIV ở ${mso('1')}. Trên màn, 6 đỉnh liên tiếp: đỉnh đầu tới đỉnh cuối cách nhau ${o('7{,}5')}.<br><b>a)</b> số chu kì ${Nq}<br><b>b)</b> chu kì ${Tq}<br><b>c)</b> tần số ${fq}`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 2 · Bài 1', de: `Âm đơn ${Hz('1\\,250')}. TIME/DIV ở ${mso('0{,}2')}; màn rộng ${o('10')}.<br><b>a)</b> chu kì ${Tq} (ms)<br><b>b)</b> một chu kì chiếm bao nhiêu ô<br><b>c)</b> ${m('N=2')} chu kì liên tiếp chiếm ${Lq} bao nhiêu ô<br><b>d)</b> màn chứa trọn tối đa mấy chu kì`, o: ['a', 'b', 'c', 'd'], ow: { a: 22, b: 22, c: 22, d: 22 } },
    { t: 'Dạng 2 · Bài 2', de: `Âm đơn ${Hz('250')}. TIME/DIV ở ${mso('2')}; màn rộng ${o('10')}.<br><b>a)</b> chu kì ${Tq} (ms)<br><b>b)</b> một chu kì chiếm bao nhiêu ô<br><b>c)</b> ${m('N=4')} chu kì liên tiếp chiếm ${Lq} bao nhiêu ô<br><b>d)</b> màn chứa trọn tối đa mấy chu kì`, o: ['a', 'b', 'c', 'd'], ow: { a: 22, b: 22, c: 22, d: 22 } },
    { t: 'Dạng 3 · Bài 1', de: `Đo một nguồn âm: ${nw(m('N=3'))}, ${nw(m('k=0{,}5\\ \\text{ms/ô}'))}, đọc lệch ${nw(m('\\Delta L=0{,}1\\ \\text{ô}'))}:${tbL(['6,0', '6,2', '5,9', '6,1', '6,0'])}<b>a)</b> tần số trung bình ${fb}<br><b>b)</b> sai số ngẫu nhiên ${m('\\Delta\\bar f')}<br><b>c)</b> sai số dụng cụ ${m('\\Delta f_{dc}')}<br><b>d)</b> sai số tổng ${df}; ghi ${m('f=\\ldots\\pm\\ldots')}`, o: ['a', 'b', 'c', 'd<sub>1</sub>', 'd<sub>2</sub>'], ow: { 'd<sub>2</sub>': 34 } },
    nhap(3),
  ], [
    { t: 'Dạng 3 · Bài 2', de: `Đo nguồn âm khác: ${nw(m('N=4'))}, ${nw(m('k=0{,}5\\ \\text{ms/ô}'))}, cùng sai số đọc ${nw(m('0{,}1\\ \\text{ô}'))}:${tbL(['8,4', '8,2', '8,3', '8,5', '8,3'])}<b>a)</b> tần số trung bình ${fb}<br><b>b)</b> sai số ngẫu nhiên ${m('\\Delta\\bar f')}<br><b>c)</b> sai số dụng cụ ${m('\\Delta f_{dc}')}<br><b>d)</b> sai số tổng ${df}; ghi ${m('f=\\ldots\\pm\\ldots')}`, o: ['a', 'b', 'c', 'd<sub>1</sub>', 'd<sub>2</sub>'], ow: { 'd<sub>2</sub>': 34 } },
    { t: 'Ghi âm rồi đếm chu kì', de: `Ghi âm một nốt, phóng to dạng sóng: 12 chu kì liên tiếp mất ${ms('27{,}3')}, đọc thời gian có thể lệch ${ms('0{,}1')}.<br><b>a)</b> tần số ${nw(m('f=\\dfrac{N}{t}'))}<br><b>b)</b> sai số tỉ đối ${m('\\dfrac{\\Delta t}{t}')} (%)<br><b>c)</b> sai số ${df}; ghi ${m('f=\\ldots\\pm\\ldots')}`, o: ['a', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'], ow: { 'c<sub>2</sub>': 34 } },
    nhap(19),
  ]],
  dap: [
    `D1·1: a) 3 · b) 0,4 ms · c) 2 500 Hz &nbsp;|&nbsp; D1·2: a) 5 · b) 1,5 ms · c) 667 Hz &nbsp;|&nbsp; D2·1: a) 0,8 ms · b) 4,0 ô · c) 8,0 ô · d) 2 chu kì &nbsp;|&nbsp; D2·2: a) 4 ms · b) 2,0 ô · c) 8,0 ô · d) 5 chu kì &nbsp;|&nbsp; D3·1: a) 994 Hz · b) 14,4 Hz · c) 16,5 Hz · d<sub>1</sub>) 31 Hz · d<sub>2</sub>) (994 ± 31) Hz`,
    `D3·2: a) 959 Hz · b) 10,1 Hz · c) 11,5 Hz · d<sub>1</sub>) 22 Hz · d<sub>2</sub>) (959 ± 22) Hz &nbsp;|&nbsp; Ghi âm: a) 440 Hz · b) 0,37 % · c<sub>1</sub>) 2 Hz · c<sub>2</sub>) (440 ± 2) Hz`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [2, 1], kq: [[1, 2], [3]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'nhắc lại 1·4 · dụng cụ 2·1 · hai núm 2·2 · các bước 3·1 · bẫy đếm đỉnh 3·2 · bảng số liệu 4·1 · sai số 4·2 · kết quả 5·1 · bẫy 3 5·2 · dạng 1–2 → 6·1 · dạng 3 → 7·1',
  out: process.argv[2],
});
