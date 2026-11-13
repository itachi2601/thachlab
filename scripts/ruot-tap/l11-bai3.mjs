// Ruột tập VL11 – Bài 3 · Vận tốc, gia tốc trong dao động điều hoà (lesson id 22). Quyển Chương 1 lớp 11: bài 3 = tr. 25–36.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự giải vào vở · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l11-bai3.mjs (toàn bộ SVG tự vẽ). Nội dung theo bài web (book/cache/22.json, tải từ DB 13/11/2026):
// mục tiêu, dự đoán xích đu, II.1–II.5, thí nghiệm con lắc lò xo, ba bẫy, Trả bài 6 câu, bài toán mẫu, thử thách, 5 dạng bài tập mẫu.
// Đáp số Bài tương tự (tuongTu.dap) tính bằng Python 13/11/2026 (math, radian), làm tròn 3 chữ số có nghĩa.
// Chạy: node scripts/ruot-tap/l11-bai3.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl11-bai3.pdf
//       node scripts/ruot-tap/l11-bai3.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l11-bai3/
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL11b3 as H } from './hinh-l11-bai3.mjs';
const fc = (w = 16) => `<span class="fill" style="min-width:${w}mm;height:9mm;vertical-align:-3mm"></span>`;

if (process.argv[2] === '--hinh') {
  const { createRequire } = await import('node:module');
  const { existsSync, mkdirSync, writeFileSync } = await import('node:fs');
  const { dirname, resolve } = await import('node:path');
  const { fileURLToPath, pathToFileURL } = await import('node:url');
  const HERE = dirname(fileURLToPath(import.meta.url));
  const BOOK = [resolve(HERE, '../../book/'), '/Users/MAC/Projects/thachlab/book'].find((d) => existsSync(d + '/node_modules')) + '/';
  const puppeteer = createRequire(BOOK + 'package.json')('puppeteer-core');
  const F = resolve(HERE, 'fonts') + '/source-sans-3-';
  const kx = pathToFileURL(BOOK + 'node_modules/katex/dist/katex.min.css').href;
  const css = ['latin', 'latin-ext', 'vietnamese'].flatMap((s) => [400, 700].map((w) => `@font-face{font-family:BV;font-weight:${w};src:url("${pathToFileURL(`${F}${s}-${w}-normal.woff2`).href}")}`)).join('')
    + 'body{margin:0;font-family:BV,sans-serif;zoom:4}.fig{margin:0;width:46mm;border:.3mm solid #d3dbec;border-radius:1.5mm;padding:1mm 1.5mm .6mm;background:#fff}.fig svg{display:block;width:100%;height:auto}figcaption{font-size:2.95mm;color:#5f6a88;line-height:1.3;margin-top:.4mm}';
  const out = resolve(HERE, 'out/hinh-l11-bai3'); mkdirSync(out, { recursive: true });
  const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true, args: ['--allow-file-access-from-files'] });
  const pg = await b.newPage();
  for (const [name, fn] of Object.entries(H)) {
    writeFileSync(out + '/_tmp.html', `<!doctype html><meta charset="utf-8"><link rel="stylesheet" href="${kx}"><style>${css}</style>${fn()}`);
    await pg.goto(pathToFileURL(out + '/_tmp.html').href, { waitUntil: 'networkidle0' });
    await pg.evaluate('document.fonts.ready');
    await (await pg.$('.fig')).screenshot({ path: `${out}/${name}.png` });
    console.log(`${name}.png`);
  }
  await b.close();
  process.exit(0);
}

const K = khoiTao({ bai: 3, lid: 22, ten: 'VẬN TỐC, GIA TỐC TRONG DAO ĐỘNG ĐIỀU HOÀ', lop: 11, baiDau: 1, sub: 'Vật lí 11 · Chương 1: Dao động' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const u = (s) => nw(m(s));                       // số + đơn vị không gãy dòng
const om = m('\\omega'), ph = m('\\varphi'), pi = m('\\pi');
const rad = `<span class="hint">Máy tính để chế độ <b>rad</b>; ${m('\\pi\\approx 3{,}14')}, ${m('\\sqrt2\\approx1{,}41')}, ${m('\\sqrt3\\approx1{,}73')}.</span>`;
const vmx = m('v_{\\max}'), amx = m('a_{\\max}');

const p1 = `<section class="page">
${head('BÀI 3 · VẬN TỐC, GIA TỐC TRONG DAO ĐỘNG ĐIỀU HOÀ', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Viết <b>${m('v')} và ${m('a')}</b> khi biết ${m('x=A\\cos(\\omega t+\\varphi)')}`)}
${dong(`${ck}Chỉ chỗ <b>tốc độ</b> và <b>độ lớn gia tốc</b> lớn nhất, nhỏ nhất; đọc chiều ${m('\\vec v')}, ${m('\\vec a')}`)}
${dong(`${ck}Dùng ba <b>hệ thức không chứa ${m('t')}</b>`)}
${dong(`${ck}Tính <b>thời gian</b> đi giữa các mốc li độ đặc biệt`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Trên quỹ đạo ghế xích đu, chỗ nào tốc độ lớn nhất?</p>
<div class="fig-side" style="${fs(46)}"><div>
${opt('A', 'Hai điểm cao nhất, vì ghế vừa tích được đà')}
${opt('B', 'Chỗ thấp nhất, khi qua vị trí cân bằng')}
${opt('C', 'Mọi chỗ như nhau, vì chu kì không đổi')}
${opt('D', 'Ngay sau khi rời điểm cao, vì lúc đó mới bắt đầu nhanh')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 1)}</div>
${H.xichDu()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Vận tốc', '1·4')}
<div class="card" style="padding:1.2mm 3mm">
<div>${m('v')} là đạo hàm của ${m('x')} theo ${m('t')}. Với ${m('x=A\\cos(\\omega t+\\varphi)')}:</div>
<div style="margin:.6mm 0">${m('v=')} ${f(30)} &nbsp;&nbsp;hay&nbsp;&nbsp; ${m('v=A\\omega\\cos(\\omega t+\\varphi\\,+')} ${f(12)}${m(')')}</div>
<div>${m('v')} sớm pha ${f(12)} so với ${m('x')} (gọi là ${f(25)} pha). Đơn vị: ${m('x')} theo cm thì ${m('v')} theo ${f(14)}</div>
<div class="fig-side" style="${fs(52)};margin-top:.8mm"><div>
<div>Tốc độ lớn nhất ${m('|v|_{\\max}=')} ${f(14)}, khi vật qua ${f(25)}</div>
<div>Tốc độ ${m('|v|=0')} tại ${f(25)}; ở đó vật đổi chiều.</div>
<div>${m('v_{\\max}=+A\\omega')} khi qua O theo chiều ${f(14)}</div>
<div>${m('v_{\\min}=')} ${f(14)} khi qua O theo chiều âm.</div>
<div>Từ O ra biên: ${f(25)} dần. Từ biên về O: ${f(25)} dần.</div></div>
${H.trucV()}</div></div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('GIA TỐC · ĐỒ THỊ x, v, a · QUAN HỆ PHA')}
${h3(1, 'II.2 · Gia tốc', '2·1')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div>${m('a')} là đạo hàm của ${m('v')}:</div>
<div style="margin:.6mm 0">${m('a=')} ${f(30)}</div>
<div>Gọn: ${m('a=')} ${f(16)} &nbsp;(trái dấu ${m('x')})</div>
<div>${m('|a|_{\\max}=')} ${f(14)} tại ${f(25)}; ${m('a=0')} tại ${f(12)}</div>
<div>${m('\\vec a')} luôn hướng về ${f(12)}</div>
<div>${m('a_{\\max}=+A\\omega^2')} tại biên ${f(14)}</div>
<div>Ra biên: ${m('\\vec v')}, ${m('\\vec a')} ${f(25)} chiều. Về O: ${f(25)} chiều.</div>
<div>Dao động điều hoà ${ck}có &nbsp;${ck}không có đoạn nhanh dần <b>đều</b>, vì ${m('|a|')} đổi theo ${f(12)}</div></div>
${H.trucA()}</div>
${h3(2, `Đọc đồ thị x, v, a (${m('\\varphi=0')})`, '2·2')}
<div class="fig-side" style="${fs(50)}"><div>
<table class="tbl-ct"><tr><th style="width:21mm">Mốc</th><th>${m('x')}</th><th>${m('v')}</th><th>${m('a')}</th></tr>
<tr><td>${m('t=0')}</td><td>${m('+A')}</td><td>${m('0')}</td><td>${m('-A\\omega^2')}</td></tr>
<tr><td>${m('t=T/4')}</td><td></td><td></td><td></td></tr>
<tr><td>${m('t=T/2')}</td><td></td><td></td><td></td></tr>
<tr><td>${m('t=3T/4')}</td><td></td><td></td><td></td></tr></table>
<div style="margin-top:1mm">Trong một chu kì, ${m('v')} và ${m('a')} cùng dấu trong khoảng thời gian ${nw(`${m('\\Delta t=')} ${f(12)}`)}</div>
<div>Đó là lúc vật đi từ ${f(25)} về ${f(12)}</div></div>
${H.xva(`${m('\\varphi=0')}. Nét liền: x · nét đứt: v · nét chấm: a. Vạch đứt dọc: T/4, T/2, 3T/4, T.`)}</div>
${h3(3, 'II.3 · Quan hệ pha và vị trí đặc biệt', '2·3')}
<div class="two"><table><tr><th>Cặp</th><th>Lệch pha</th></tr>
<tr><td>${m('v')} so với ${m('x')}</td><td>sớm ${f(10)}</td></tr>
<tr><td>${m('a')} so với ${m('v')}</td><td>sớm ${f(10)}</td></tr>
<tr><td>${m('a')} so với ${m('x')}</td><td>sớm ${f(10)}: ${f(14)} pha</td></tr></table>
<table><tr><th>Vị trí</th><th>${m('|v|')}</th><th>${m('|a|')}</th></tr>
<tr><td>O</td><td>${vmx}</td><td>0</td></tr>
<tr><td>${m('\\pm A/2')}</td><td style="height:7mm"></td><td></td></tr>
<tr><td>${m('\\pm A\\sqrt2/2')}</td><td style="height:7mm"></td><td></td></tr>
<tr><td>${m('\\pm A\\sqrt3/2')}</td><td style="height:7mm"></td><td></td></tr>
<tr><td>${m('\\pm A')}</td><td></td><td></td></tr></table></div>
<div class="hint" style="margin-top:.6mm">Bảng phải: ghi theo ${vmx} và ${amx} (vd ${m('v_{\\max}/2')}). ${vmx} ở đây là tốc độ cực đại ${m('A\\omega')}.</div>
<div class="card soft" style="margin-top:.8mm;padding:1mm 3mm"><b>Áp dụng:</b> ${u('A=4\\ \\mathrm{cm}')}, ${u('\\omega=10\\ \\mathrm{rad/s}')}. Tại ${u('x=-2\\ \\mathrm{cm}')} (tức ${m('-A/2')}): ${m('|v|=')} ${f(16)} cm/s · ${m('a=')} ${f(16)} cm/s² (ghi dấu)</div>
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('THÍ NGHIỆM · HỆ THỨC BỎ t · THỜI GIAN TỚI MỐC')}
${h3(1, 'Thí nghiệm: đo A, T rồi tính v và a', '3·1')}
<div class="fig-side" style="${fs(44)}"><div>
<div>Kéo lệch ${u('A=4{,}0\\ \\mathrm{cm}')} rồi thả, bấm giờ 10 dao động (${m('t_{10}')}), năm lần:</div>
<table class="tbl-ct" style="margin-top:.6mm"><tr><th>${m('t_{10}')} (s)</th><td>8,02</td><td>7,96</td><td>8,08</td><td>7,94</td><td>8,00</td></tr></table>
<div style="margin-top:.6mm">${m('T')} trung bình ${f(14)} s · ${m('\\omega=2\\pi/T=')} ${f(14)} rad/s</div>
<div>${m('v_{\\max}=A\\omega=')} ${f(14)} cm/s</div>
<div>Tại ${u('x=2{,}0\\ \\mathrm{cm}')}: ${m('|v|=\\omega\\sqrt{A^2-x^2}=')} ${f(14)} cm/s; ${m('a=-\\omega^2x=')} ${f(16)} cm/s²</div>
<div><b>Rút ra:</b> càng xa O, tốc độ càng ${f(14)}, ${m('|a|')} càng ${f(14)}</div></div>
${H.conLac()}</div>
${h3(2, 'II.4 · Hệ thức độc lập với thời gian', '3·2')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div>Hai đại lượng cùng tần số, biên độ ${m('M')}, ${m('N')}:</div>
<div>cùng pha: ${m('\\dfrac mM=')} ${f(14)} · ngược pha: ${m('\\dfrac mM=')} ${f(14)}</div>
<div>vuông pha: ${m('\\left(\\dfrac mM\\right)^2+\\left(\\dfrac nN\\right)^2=')} ${f(12)}</div>
<div style="margin-top:.6mm">${m('x')}–${m('v')}: ${m('A^2=x^2+')} ${fc(16)}<br>${m('\\to')} đồ thị là ${f(25)}</div>
<div>${m('v')}–${m('a')}: ${m('A^2=')}${fc(16)}${m('+')}${fc(16)}</div>
<div>${m('x')}–${m('a')}: ${m('a=')} ${f(14)} ${m('\\to')} đồ thị là đoạn ${f(25)}</div></div>
${H.elip()}</div>
${h3(3, 'II.5 · Thời gian ngắn nhất từ O tới các mốc', '3·3')}
<div class="fig-side" style="${fs(48)}"><div>
<table><tr><th>Từ O tới</th><th>Góc quét</th><th>Thời gian</th></tr>
<tr><td>${m('\\pm A/2')}</td><td>${m('\\pi/6')}</td><td></td></tr>
<tr><td>${m('\\pm A\\sqrt2/2')}</td><td></td><td></td></tr>
<tr><td>${m('\\pm A\\sqrt3/2')}</td><td></td><td></td></tr>
<tr><td>${m('\\pm A')}</td><td></td><td></td></tr></table>
<div style="margin-top:.8mm">Quy đổi: ${m('T\\leftrightarrow 2\\pi')}, nên ${m('\\Delta t=\\dfrac{\\text{góc quét}}{2\\pi}\\,T')}</div>
<div>Từ ${m('A/2')} ra biên ${m('A')}: ${m('\\Delta t=')} ${f(14)} · từ ${m('-A/2')} tới ${m('A/2')} qua O: ${f(14)}</div>
<div>${m('T=0{,}800')} s thì ${m('T/12=')} ${f(14)} s</div></div>
${H.vongTron('Điểm chạy đều trên vòng, bóng của nó trên trục x là vật. Một vòng mất T.')}</div>
${h3(4, 'Làm nhanh', '3·4')}
${box(`<div><b>Câu 1.</b> ${u('T=0{,}8\\ \\mathrm s')}. Thời gian ngắn nhất từ O tới ${m('x=A\\sqrt2/2')}? ${f(14)} s</div><div><b>Câu 2.</b> Cùng ${m('T')}, thời gian ngắn nhất từ ${m('x=-A/2')} tới ${m('x=A\\sqrt3/2')}? ${f(14)} s</div>`)}
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('BẪY · TRẢ BÀI · TỰ KIỂM TRA')}
${h3(1, 'III · Ba cái bẫy hay sập', '4·1')}
<div class="card" style="padding:1mm 3mm">
<div class="trap">${ck}<span><b>“Tốc độ cực đại có dấu.”</b> ${m('v')} có dấu (đi từ ${m('-A\\omega')} tới ${m('+A\\omega')}); tốc độ ${m('|v|')} không âm. Qua O theo chiều âm: ${m('v=-A\\omega')} nhưng ${m('|v|=A\\omega')}.</span></div>
<div class="trap">${ck}<span><b>“Ra biên thì ${m('\\vec a')} cùng chiều ${m('\\vec v')}, nhanh dần đều.”</b> Ra biên: ngược chiều, chậm dần, không đều.</span></div>
<div class="trap">${ck}<span><b>“Đề cho ${m('f')} thì ${m('v_{\\max}=Af')}.”</b> Đổi ${m('\\omega=2\\pi f')} trước. ${u('A=2\\ \\mathrm{cm}')}, ${u('f=5\\ \\mathrm{Hz}')}: ${m('v_{\\max}=')} ${f(16)}</span></div></div>
${h3(2, 'IV · Trả bài 6 câu', '4·2')}
${box(`${tb(`1. Viết ${m('v')} khi ${m('x=A\\cos(\\omega t+\\varphi)')}. ${m('v')} lệch pha bao nhiêu so với ${m('x')}?`)}${lines(3)}
${tb(`2. ${m('|v|')} và ${m('v')} lớn nhất, nhỏ nhất ở đâu?`)}${lines(3)}
${tb(`3. Viết ${m('a')}; ${m('a_{\\max}')}, ${m('a_{\\min}')} ở đâu?`)}${lines(3)}
${tb(`4. Pha giữa ${m('x')}, ${m('v')}, ${m('a')}.`)}${lines(2)}
${tb(`5. Ba hệ thức bỏ ${m('t')}.`)}${lines(2)}
${tb(`6. Thời gian từ O tới ${m('A/2')}, ${m('A\\sqrt2/2')}, ${m('A\\sqrt3/2')}, ${m('A')}.`)}${lines(2)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/6 câu · chưa thuộc: ${f(25)} ${nw(`${m('\\to')} đọc lại ô ${f(12)} Tập`)}</div>
${h3(3, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '4·3')}
${rkHai([1, 2, 3], [4, 5, 6])}
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TOÁN MẪU · THỬ THÁCH · MANG VỀ')}
${h3(1, 'V · Bài toán mẫu', '5·1')}
<div class="card soft" style="padding:1.2mm 3mm">Vật dao động điều hoà trên trục Ox, ${u('A=4\\ \\mathrm{cm}')}, ${u('\\omega=10\\ \\mathrm{rad/s}')}. Lúc ${m('t=0')} vật ở biên dương.
<div><b>a)</b> Viết ${m('v(t)')} và ${m('a(t)')}.</div><div><b>b)</b> Khi qua ${u('x=2\\ \\mathrm{cm}')} theo chiều âm, tính ${m('v')} và ${m('a')}.</div><div><b>c)</b> Thời gian ngắn nhất từ biên dương tới ${u('x=2\\ \\mathrm{cm}')}.</div></div>
<table style="margin-top:.6mm"><tr><th style="width:44mm">Câu trong đề</th><th style="width:30mm">Dữ liệu</th><th>Kiến thức</th></tr>
<tr><td>“lúc ${m('t=0')} ở biên dương”</td><td></td><td></td></tr>
<tr><td>“qua ${m('x=2')} cm theo chiều âm”</td><td></td><td></td></tr>
<tr><td>“từ biên dương tới ${m('x=2')} cm”</td><td></td><td></td></tr></table>
<div class="fig-side" style="${fs(46)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl(`a) ${m('\\varphi=')} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ${m('v(t)=')}`, 2)}${wl(`b) ${m('|v|=')}`, 2)}${wl(`&nbsp;&nbsp;&nbsp;&nbsp; ${m('a=')}`, 1)}${wl('c)', 2)}</div>${H.btm()}</div>
${h3(2, 'Điền bước còn thiếu', '5·2')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div class="ln">Cùng đề, lúc ${m('x=A\\sqrt2/2=2\\sqrt2')} cm, vật đang đi về O. <b>Bước 1 (cho sẵn):</b> ${m('(x/A)^2=1/2')}</div>
${wl(`Bước 2: ${m('|v|=')} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; dấu của ${m('v')}:`, 1)}${wl('Bước 3: thời gian từ biên dương =', 1)}</div>
${h3(3, 'Thử thách phân tầng', '5·3')}
${box(wl(`${m('\\bigstar')} ${u('A=3\\ \\mathrm{cm}')}, ${u('T=0{,}5\\ \\mathrm s')}. Tính ${vmx}.`, 2)
 + wl(`${m('\\bigstar\\bigstar')} ${m('x=-A\\sqrt3/2')}, ${u('A=4\\ \\mathrm{cm}')}, ${u('\\omega=10\\ \\mathrm{rad/s}')}, đang ra biên âm. Tính ${m('v')}, ${m('a')}; nhanh hay chậm dần?`, 3)
 + wl(`${m('\\bigstar\\bigstar\\bigstar')} Chứng minh: trong một chu kì, ${m('v')} và ${m('a')} cùng dấu đúng ${m('T/2')}.`, 2))}
${h3(4, 'VI · Mang về: điều em dễ quên nhất', '5·4')}
${box(wl('1.', 1) + wl('2.', 1) + wl('3.', 1))}
${foot(5)}</section>`;

// ---- Bài tập mẫu (tr. 6–7): 5 dạng theo bài web ----
const dang = [
  { t: 'Dạng 1 · Dễ · Viết v(t), a(t); v<sub>max</sub>, a<sub>max</sub>; v và a tại một thời điểm',
    de: `${m('x=5\\cos(4\\pi t+\\pi/3)')} (${m('x')}: cm, ${m('t')}: s; máy tính chế độ rad).<br><b>a)</b> tốc độ cực đại và độ lớn gia tốc cực đại<br><b>b)</b> phương trình ${m('v(t)')} và ${m('a(t)')} &nbsp;&nbsp; <b>c)</b> ${m('v')} và ${m('a')} tại ${u('t=\\tfrac1{12}\\ \\mathrm s')}; vật đang ${ck}về VTCB ${ck}ra biên`,
    nd: `${m('v')}, ${m('a')} cùng dấu: ${f(25)} dần; ngược dấu: ${f(25)} dần`,
    a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'c<sub>1</sub>', 'c<sub>2</sub>'], gi: 4 },
  { t: 'Dạng 2 · Trung bình · Biết li độ tìm v, a; biết tốc độ tìm li độ',
    de: `${u('A=10\\ \\mathrm{cm}')}, ${u('\\omega=4\\ \\mathrm{rad/s}')}; vật qua ${u('x=+6\\ \\mathrm{cm}')} theo chiều dương.<br><b>a)</b> độ lớn vận tốc tại đó &nbsp;&nbsp; <b>b)</b> gia tốc tại đó (kể cả dấu); nhanh dần hay chậm dần?<br><b>c)</b> lúc khác tốc độ ${u('24\\ \\mathrm{cm/s}')}: độ lớn li độ khi đó`,
    nd: `${m('|v|=\\omega\\sqrt{\\ \\ }')} ${fc(22)}; dấu ${m('v')} lấy từ ${f(25)}`, a: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], gi: 4 },
  { t: `Dạng 3 · Trung bình · Đọc đồ thị x–t: A, T, ${m('\\varphi')}; suy ra v và a`,
    de: `Hình bên là đồ thị li độ theo thời gian (${m('x')}: cm, ${m('t')}: s).<br><b>a)</b> chu kì ${m('T')} và pha ban đầu ${ph} (đọc ${m('A')}, tính ${om} trong khung giải)<br><b>b)</b> ${m('v(t)')}, ${m('a(t)')}; pha của ${m('v')}, ${m('a')} so với ${m('x')} &nbsp;&nbsp; <b>c)</b> ${m('v')} và ${m('a')} tại ${m('t=0')}`,
    nd: `${m('\\cos\\varphi=x(0)/A')} cho hai góc; chọn theo ${f(25)} của đồ thị lúc ${m('t=0')}`,
    a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'c<sub>1</sub>', 'c<sub>2</sub>'], gi: 5, fig: H.d3('') },
  { t: 'Dạng 4 · Khó · Tốc độ bằng nửa cực đại: li độ, thời gian, gia tốc',
    de: `${u('A=8\\ \\mathrm{cm}')}, ${u('T=1{,}2\\ \\mathrm s')}; ${m('t=0')} vật ở biên dương.<br><b>a)</b> tốc độ cực đại<br><b>b)</b> khi tốc độ bằng nửa tốc độ cực đại: độ lớn li độ<br><b>c)</b> thời gian ngắn nhất từ ${m('t=0')} tới lúc đó<br><b>d)</b> độ lớn gia tốc lúc đó`,
    nd: `${m('(x/A)^2+(v/v_{\\max})^2=1')} ${m('\\to')} ${m('|x|=')} ${f(16)}; từ biên tới mốc đó mất ${f(14)}`, a: ['a', 'b', 'c', 'd'], gi: 8, fig: H.d4() },
  { t: `Dạng 5 · Khó · Bài ngược: hai cặp (li độ, tốc độ) ${m('\\to\\omega')}, A, T, a<sub>max</sub>`,
    de: `Qua ${u('x_1=3\\ \\mathrm{cm}')} tốc độ ${u('40\\ \\mathrm{cm/s}')}; qua ${u('x_2=4\\ \\mathrm{cm}')} tốc độ ${u('30\\ \\mathrm{cm/s}')}.<br><b>a)</b> tần số góc ${om} và chu kì ${m('T')}<br><b>b)</b> biên độ ${m('A')}<br><b>c)</b> tốc độ cực đại và độ lớn gia tốc cực đại`,
    nd: `Viết ${m('A^2=x^2+v^2/\\omega^2')} cho hai điểm rồi ${f(25)} để khử ${m('A^2')}; tìm ${om} trước`,
    a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'], gi: 7, cot: 3 },
];

// ---- Bài tương tự (tr. 8–9): giải vào vở, mỗi dạng 2 bài; ô đáp số cuối dòng của ý (như l10-bai23) ----
const ttHaiCot = '<style>.bt{margin-bottom:1mm}.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';
const oY = (s, o, w = 25) => s.split('<br>').map((p) => {
  const y = p.match(/^<b>([a-d])\)<\/b>/);
  if (!y) return `<div>${p}</div>`;
  const ls = o.map((l) => (Array.isArray(l) ? l : [l, w])).filter(([l]) => l[0] === y[1]);
  return `<div class="yo"><span>${p}</span><span class="oo">${ls.map(([l, ww]) => `<span class="nw"><b>${l})</b>${f(ww)}</span>`).join('')}</span></div>`;
}).join('');
const ttDe = (b) => b.fig ? `<div class="fig-side" style="grid-template-columns:1fr ${b.fw}mm"><div>${oY(b.de, b.o, b.ow)}</div>${b.fig}</div>` : oY(b.de, b.o, b.ow);
const vaoVo = (ds) => ds.map((b) => (b.o ? { t: b.t, de: ttDe(b), k: 0 } : b));
const nhap = (n) => ({ t: '<span class="nhap-t">Nháp / chỗ em còn vướng</span>', de: lines(n), k: 0 });
const s1 = `<span class="hint">(${m('x')}: cm, ${m('t')}: s; máy tính chế độ rad)</span>`;
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–3', 'DẠNG 3–5'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `${m('x=4\\cos\\left(2\\pi t-\\dfrac{\\pi}{6}\\right)')} ${s1}<br><b>a)</b> tốc độ cực đại<br><b>b)</b> độ lớn gia tốc cực đại<br><b>c)</b> ${m('v')} và ${m('a')} tại ${u('t=0{,}25\\ \\mathrm s')}<br><b>d)</b> lúc đó vật về VTCB hay ra biên?`, o: ['a', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>', 'd'], ow: 20 },
    { t: 'Dạng 1 · Bài 2', de: `${m('x=6\\cos\\left(5\\pi t+\\dfrac{\\pi}{6}\\right)')} ${s1}<br><b>a)</b> phương trình ${m('v(t)')}<br><b>b)</b> phương trình ${m('a(t)')}<br><b>c)</b> ${m('v')} và ${m('a')} tại ${u('t=0{,}1\\ \\mathrm s')}; vật ${ck}nhanh dần ${ck}chậm dần`, o: [['a', 46], ['b', 46], 'c<sub>1</sub>', 'c<sub>2</sub>'], ow: 20 },
    { t: 'Dạng 2 · Bài 1', de: `${u('A=10\\ \\mathrm{cm}')}, ${u('\\omega=5\\ \\mathrm{rad/s}')}; vật qua ${u('x=-8\\ \\mathrm{cm}')} theo chiều dương.<br><b>a)</b> vận tốc tại đó (kể cả dấu)<br><b>b)</b> gia tốc tại đó; nhanh dần hay chậm dần?<br><b>c)</b> lúc tốc độ ${u('40\\ \\mathrm{cm/s}')}: độ lớn li độ`, o: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'] },
    { t: 'Dạng 2 · Bài 2', de: `${u('A=13\\ \\mathrm{cm}')}, ${u('\\omega=2\\ \\mathrm{rad/s}')}; vật qua ${u('x=5\\ \\mathrm{cm}')} theo chiều âm.<br><b>a)</b> vận tốc tại đó (kể cả dấu)<br><b>b)</b> gia tốc tại đó; nhanh dần hay chậm dần?<br><b>c)</b> lúc gia tốc có độ lớn ${u('24\\ \\mathrm{cm/s^2}')}: độ lớn li độ và tốc độ`, o: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c<sub>1</sub>', 'c<sub>2</sub>'], ow: 20 },
    { t: 'Dạng 3 · Bài 1', de: `Đồ thị x–t bên (${m('x')}: cm, ${m('t')}: s).<br><b>a)</b> biên độ ${m('A')} và chu kì ${m('T')}<br><b>b)</b> ${om} và pha ban đầu ${ph}<br><b>c)</b> ${m('v')} và ${m('a')} tại ${m('t=0')}`, fig: H.tt31('Vạch t cách nhau 0,4 s.'), fw: 52, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c<sub>1</sub>', 'c<sub>2</sub>'], ow: 14 },
  ], [
    { t: 'Dạng 3 · Bài 2', de: `Đồ thị x–t bên (${m('x')}: cm, ${m('t')}: s).<br><b>a)</b> biên độ ${m('A')} và chu kì ${m('T')}<br><b>b)</b> ${om} và pha ban đầu ${ph}<br><b>c)</b> ${m('v')} tại ${m('t=0')}<br><b>d)</b> lần đầu ${m('v=+v_{\\max}')}`, fig: H.tt32('Vạch t cách nhau 0,1 s.'), fw: 52, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c', 'd'], ow: 14 },
    { t: 'Dạng 4 · Bài 1', de: `${u('A=4\\ \\mathrm{cm}')}, ${u('T=0{,}8\\ \\mathrm s')}; ${m('t=0')} ở biên dương. Xét lúc tốc độ bằng ${m('\\tfrac{\\sqrt2}{2}v_{\\max}')} lần đầu.<br><b>a)</b> tốc độ cực đại<br><b>b)</b> độ lớn li độ lúc đó<br><b>c)</b> thời gian từ ${m('t=0')} tới lúc đó<br><b>d)</b> độ lớn gia tốc lúc đó`, o: ['a', 'b', 'c', 'd'] },
    { t: 'Dạng 4 · Bài 2', de: `${u('A=10\\ \\mathrm{cm}')}, ${u('T=2\\ \\mathrm s')}; ${m('t=0')} ở biên âm. Xét lúc tốc độ bằng ${m('\\tfrac{\\sqrt3}{2}v_{\\max}')} lần đầu.<br><b>a)</b> tốc độ cực đại<br><b>b)</b> độ lớn li độ lúc đó<br><b>c)</b> thời gian từ ${m('t=0')} tới lúc đó<br><b>d)</b> độ lớn gia tốc lúc đó`, o: ['a', 'b', 'c', 'd'] },
    { t: 'Dạng 5 · Bài 1', de: `Qua ${u('x_1=6\\ \\mathrm{cm}')} tốc độ ${u('16\\ \\mathrm{cm/s}')}; qua ${u('x_2=8\\ \\mathrm{cm}')} tốc độ ${u('12\\ \\mathrm{cm/s}')}.<br><b>a)</b> ${om} và ${m('T')}<br><b>b)</b> biên độ ${m('A')}<br><b>c)</b> tốc độ cực đại và độ lớn gia tốc cực đại`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'], ow: 18 },
    { t: 'Dạng 5 · Bài 2', de: `Qua ${u('x_1=5\\ \\mathrm{cm}')} tốc độ ${u('60\\ \\mathrm{cm/s}')}; qua ${u('x_2=12\\ \\mathrm{cm}')} tốc độ ${u('25\\ \\mathrm{cm/s}')}.<br><b>a)</b> ${om} và ${m('T')}<br><b>b)</b> biên độ ${m('A')}<br><b>c)</b> tốc độ cực đại và độ lớn gia tốc cực đại`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'], ow: 18 },
  ]],
  dap: [
    `D1·1: a) 25,1 cm/s · b) 158 cm/s² · c<sub>1</sub>) −21,8 cm/s · c<sub>2</sub>) −79,0 cm/s² · d) về VTCB &nbsp;|&nbsp; D1·2: a) ${m('v=-30\\pi\\sin(5\\pi t+\\pi/6)')} cm/s · b) ${m('a=-150\\pi^2\\cos(5\\pi t+\\pi/6)')} cm/s² · c<sub>1</sub>) −81,6 cm/s · c<sub>2</sub>) +740 cm/s², chậm dần &nbsp;|&nbsp; D2·1: a) +30 cm/s · b<sub>1</sub>) +200 cm/s² · b<sub>2</sub>) nhanh dần · c) 6 cm &nbsp;|&nbsp; D2·2: a) −24 cm/s · b<sub>1</sub>) −20 cm/s² · b<sub>2</sub>) nhanh dần · c<sub>1</sub>) 6 cm · c<sub>2</sub>) 23,1 cm/s &nbsp;|&nbsp; D3·1: a<sub>1</sub>) 4 cm · a<sub>2</sub>) 2,4 s · b<sub>1</sub>) ${m('5\\pi/6\\approx 2{,}62')} rad/s · b<sub>2</sub>) ${m('-2\\pi/3')} · c<sub>1</sub>) +9,07 cm/s · c<sub>2</sub>) +13,7 cm/s²`,
    `D3·2: a<sub>1</sub>) 5 cm · a<sub>2</sub>) 0,8 s · b<sub>1</sub>) ${m('2{,}5\\pi\\approx 7{,}85')} rad/s · b<sub>2</sub>) ${m('\\pi/2')} · c) −39,3 cm/s · d) 0,4 s &nbsp;|&nbsp; D4·1: a) 31,4 cm/s · b) 2,83 cm · c) 0,1 s · d) 174 cm/s² &nbsp;|&nbsp; D4·2: a) 31,4 cm/s · b) 5 cm · c) 0,333 s · d) 49,3 cm/s² &nbsp;|&nbsp; D5·1: a<sub>1</sub>) 2 rad/s · a<sub>2</sub>) 3,14 s · b) 10 cm · c<sub>1</sub>) 20 cm/s · c<sub>2</sub>) 40 cm/s² &nbsp;|&nbsp; D5·2: a<sub>1</sub>) 5 rad/s · a<sub>2</sub>) 1,26 s · b) 13 cm · c<sub>1</sub>) 65 cm/s · c<sub>2</sub>) 325 cm/s²`,
  ],
};

await K.dung({
  trang1to5: ttHaiCot + [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 2], kq: [[1, 2, 3], [4, 5]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'vận tốc 1·4 · gia tốc 2·1 · đồ thị x, v, a 2·2 · pha, vị trí đặc biệt 2·3 · thí nghiệm 3·1 · hệ thức 3·2 · thời gian tới mốc 3·3 · bẫy 4·1 · bài toán mẫu 5·1 · dạng 1–3: 6·1 · dạng 4–5: 7·1',
  out: process.argv[2],
});
