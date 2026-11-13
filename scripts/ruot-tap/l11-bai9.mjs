// Ruột tập VL11 – Bài 9 · Sóng ngang, sóng dọc, sự truyền năng lượng của sóng cơ (lesson id 28).
// Quyển Chương 2 lớp 11 (Sóng): bài 8 = tr. 1–12, bài 9 = tr. 13–24.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự giải vào vở · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l11-bai9.mjs (toàn bộ SVG tự vẽ). Nội dung theo bài web (book/cache/28.json, tải từ DB 13/11/2026):
// mục tiêu, dự đoán phao câu, II.1 sóng ngang (dây nhảy), II.2 sóng dọc (slinky), II.3 đo tốc độ xung đi – về, II.4 môi trường + âm,
// II.5 năng lượng, cường độ sóng, ba bẫy, Trả bài 6 câu, bài toán mẫu loa 680 Hz, thử thách phân tầng, 6 dạng bài tập mẫu.
// Đáp số Bài tập mẫu + Bài tương tự tính bằng Python 13/11/2026.
// Chạy: node scripts/ruot-tap/l11-bai9.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl11-bai9.pdf
//       node scripts/ruot-tap/l11-bai9.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l11-bai9/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL11b9 as H } from './hinh-l11-bai9.mjs';

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
  const out = resolve(HERE, 'out/hinh-l11-bai9'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 9, lid: 28, ten: 'SÓNG NGANG · SÓNG DỌC · TRUYỀN NĂNG LƯỢNG', lop: 11, baiDau: 8, sub: 'Vật lí 11 · Chương 2: Sóng' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const L = m('\\lambda'), v = m('v'), fq = m('f'), A = m('A'), I = m('I'), P = m('P');
const u = (s, dv) => nw(m(`${s}\\ \\mathrm{${dv}}`));     // số + đơn vị trong KaTeX, không gãy dòng
const ms = (s) => u(s, 'm/s'), hz = (s) => u(s, 'Hz');
const vuong = m('\\perp'), song = m('\\parallel'), to = m('\\to'), xx = m('\\approx');

// Ô đáp số Bài tập mẫu cao 9,5 mm (phân số/đáp án chữ viết tay); ô chữ của Dạng 1 rộng (≥ 25 mm, checklist HS ảo).
const css = '<style>.bt>.gi{display:grid;grid-template-columns:1fr 1fr;column-gap:4mm}.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:5mm}.tt:has(.nhap-t) .hd>span+span{display:none}.bt .ans .fill{height:9.5mm}.bt:has(.d6x) .ans{grid-template-columns:2fr 1fr 1fr}</style>';

const p1 = `${css}<section class="page">
${head('BÀI 9 · SÓNG NGANG, SÓNG DỌC, NĂNG LƯỢNG SÓNG', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Phân biệt sóng ngang, sóng dọc và môi trường truyền; chỉ ra vùng nén, vùng dãn của sóng dọc`)}
${dong(`${ck}Nói được sóng truyền đi cái gì, cái gì ở lại; tính ${L}, khoảng cách các vùng nén, cường độ sóng`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Hòn sỏi rơi xuống hồ cách phao câu vài mét. Gợn tròn lan tới, phao nhấp nhô. Thứ gì đã đi từ chỗ sỏi rơi tới phao?</p>
<div class="fig-side" style="${fs(46)}"><div>
${opt('A', 'Nước ở chỗ sỏi rơi chảy dồn tới, nâng phao lên')}
${opt('B', 'Luồng không khí do sỏi rơi đẩy ra, thổi tới phao')}
${opt('C', 'Năng lượng dao động; nước ở chỗ phao chỉ lên xuống')}
${opt('D', 'Không có gì cả; phao tự nhấp nhô vì gió thổi')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 1)}</div>
${H.hoPhao('Sỏi rơi ở O; gợn tròn lan ra.')}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f(12)} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Sóng cơ · Sóng ngang', '1·4')}
<div class="card" style="padding:1.2mm 3mm">
<div><b>Sóng cơ</b> là ${f(40)} lan truyền trong ${f(32)}.</div>
<div><b>Sóng ngang:</b> phần tử dao động theo phương ${f(30)} với phương truyền sóng.</div>
<div><b>Ví dụ:</b> ${f(30)}, ${f(30)}. Sóng điện từ (ánh sáng) cũng ngang nhưng ${ck}là ${ck}không là sóng cơ.</div></div>
${h3(5, 'Thí nghiệm: dây nhảy và dải băng màu', '1·5')}
<div class="card fig-side" style="${fs(44)};padding:1.2mm 3mm"><div>
<div><b>Làm:</b> buộc đầu dây nhảy vào cột, kéo căng ngang, buộc dải băng màu ở giữa dây. Vẩy đầu dây lên xuống một cái thật nhanh.</div>
<div><b>Quan sát:</b> bướu chạy theo phương ${f(25)}; dải băng chuyển động theo phương ${f(25)}.</div>
<div><b>Rút ra:</b> hai phương ${f(25)} ${to} đây là sóng ${f(16)}.</div>
${wl('Dải băng có chạy theo bướu tới cột không? Vì sao?', 1)}</div>
${H.dayNhay('Băng (đỏ) dao động theo phương nào?')}</div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('SÓNG DỌC · ĐO TỐC ĐỘ XUNG TRÊN LÒ XO')}
${h3(1, 'II.2 · Sóng dọc', '2·1')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div><b>Sóng dọc:</b> phần tử dao động theo phương ${f(30)} với phương truyền sóng.</div>
<div>Sóng dọc lan đi thành chuỗi vùng nén (phần tử ${f(18)} lại) và vùng dãn (phần tử ${f(18)} ra) nối tiếp nhau.</div>
<div><b>Ví dụ:</b> lò xo bị đẩy – kéo dọc trục; ${f(32)}.</div>
<div><b>Thí nghiệm slinky:</b> hai bạn giữ hai đầu lò xo trên sàn, kéo dài ${nw('khoảng 4 m')}; một bạn đẩy – kéo đầu lò xo dọc trục.</div>
<div>Trên hình: chỗ A là vùng ${f(16)}, chỗ B là vùng ${f(16)}.</div>
<div>Vòng đỏ dán băng: ${ck}chạy theo chỗ A tới đầu kia &nbsp;${ck}chỉ tiến – lùi quanh chỗ cũ.</div></div>
${H.slinky()}</div>
${h3(2, 'Làm nhanh', '2·2')}
${box(cau(`<b>Câu 1.</b> Loa đầu sân trường phát nhạc, âm truyền nằm ngang tới tai em. Lớp không khí sát tai em dao động theo phương nào? Đó là sóng gì?`, 2)
 + cau(`<b>Câu 2.</b> Đặt điện thoại đang đổ chuông, màn hình sáng, vào bình kín rồi hút dần không khí ra. Tiếng chuông và ánh sáng màn hình thay đổi thế nào? Vì sao?`, 2))}
${h3(3, 'II.3 · Thí nghiệm đo: bấm giờ xung đi – về', '2·3')}
<div class="card" style="padding:1.2mm 3mm">
<div><b>Làm:</b> căng lò xo giữa tay bạn A và bạn B, cách nhau ${u('L=4{,}00', 'm')}. A đẩy mạnh một cái tạo xung nén, đồng thời bấm đồng hồ; xung tới tay B, dội lại, về tới tay A thì bấm dừng. Làm 5 lần (số minh hoạ).</div>
<table style="margin:.8mm 0"><tr><th>Lần</th><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><th>Trung bình</th></tr>
<tr><th>${m('t')} đi – về (s)</th><td>1,18</td><td>1,09</td><td>1,21</td><td>1,13</td><td>1,16</td><td style="height:6.5mm"></td></tr></table>
<div><b>Rút ra:</b> quãng xung đi được ${nw(`${m('2L=')} ${f(14)} m`)} &nbsp;·&nbsp; ${nw(`${m('v=\\dfrac{2L}{\\bar t}=')} ${f(16)} m/s`)}</div>
<div>Lần đo lệch xa trung bình nhất: lần ${f(10)}, lệch ${f(14)} s.</div>
${wl('Vì sao đo xung đi – về chính xác hơn đo một lượt?', 2)}
${wl('Muốn chính xác hơn nữa, em làm gì?', 1)}</div>
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('MÔI TRƯỜNG TRUYỀN · SÓNG ÂM · NĂNG LƯỢNG SÓNG')}
${h3(1, 'II.4 · Sóng cơ truyền được ở đâu?', '3·1')}
<div class="card" style="padding:1.2mm 3mm">
<div>Sóng cơ cần ${f(40)}; ${ck}có ${ck}không truyền qua chân không.</div>
<table style="margin:.8mm 0"><tr><th style="width:30mm">Tiêu chí</th><th>Sóng cơ ngang</th><th>Sóng cơ dọc</th></tr>
<tr><td>Phương dao động</td><td style="height:6.5mm"></td><td></td></tr>
<tr><td>Truyền trong</td><td style="height:6.5mm"></td><td></td></tr>
<tr><td>Ví dụ</td><td style="height:6.5mm"></td><td></td></tr></table>
<div><b>Sóng âm</b> trong không khí, chất lỏng là sóng ${f(16)}. Tai người nghe được: ${nw(`${f(14)} Hz`)} – ${nw(`${f(18)} Hz`)}; dưới là ${f(18)}, trên là ${f(18)}.</div>
<div>Âm to do ${f(25)} lớn; âm cao do ${f(25)} lớn.</div>
<div>Bước sóng: ${nw(`${m('\\lambda=')} ${f(16)}`)}. Sang môi trường khác: ${fq} ${ck}giữ nguyên ${ck}đổi; ${v} đổi nên ${L} đổi.</div></div>
${h3(2, 'II.5 · Sóng truyền năng lượng · Cường độ sóng', '3·2')}
<div class="card fig-side" style="${fs(42)};padding:1.2mm 3mm"><div>
<div>Sóng tới đâu, phần tử ở đó nhận ${f(25)} và dao động, ${ck}có ${ck}không đi theo sóng.</div>
<div>Trong cùng một môi trường, năng lượng sóng tỉ lệ với ${f(12)} và ${f(12)}.</div>
<div><b>Cường độ sóng</b> ${I}: năng lượng truyền qua một đơn vị diện tích ${f(25)} với phương truyền, trong một đơn vị thời gian.</div>
<div>${nw(`${m('I=')} ${f(16)}`)} &nbsp;(đơn vị ${f(14)}) &nbsp;·&nbsp; nguồn nhỏ phát đều mọi hướng: ${nw(`${m('I=')} ${f(18)}`)}</div>
<div>Xa gấp đôi thì ${I} còn ${f(14)} lần.</div></div>
${H.matCau()}</div>
${h3(3, 'III · Ba cái bẫy hay sập', '3·3')}
<div class="card fig-side" style="${fs(46)};padding:1mm 3mm"><div>
<div class="trap">${ck}<span><b>“Sóng chở nước và phao đi theo.”</b> ${nw(`${m('v=1')} m/s`)}, sau 10 s phao dời ${f(18)} m. Truyền đi: năng lượng, pha; ở lại: phần tử.</span></div>
<div class="trap">${ck}<span><b>“Vùng nén ở đỉnh đồ thị ${m('u')}–${m('x')}.”</b> Nén, dãn đều ở chỗ ${m('u=0')}: đi xuống là nén, đi lên là dãn. Trên hình: nén ở ${f(10)}, dãn ở ${f(10)}.</span></div>
<div class="trap">${ck}<span><b>“Ngang, dọc là so với mặt đất.”</b> So phương dao động với phương truyền. Dây treo đứng, lắc đầu dưới qua lại nằm ngang: sóng ${f(16)}.</span></div></div>
${H.uxDoc()}</div>
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('TRẢ BÀI · TỰ KIỂM TRA · BÀI TOÁN MẪU')}
${h3(1, 'IV · Trả bài 6 câu', '4·1')}
${box(`${tb('1. Sóng ngang là gì? Truyền trong môi trường nào? Ví dụ?')}${lines(2)}
${tb('2. Sóng dọc là gì? Truyền trong môi trường nào? Ví dụ?')}${lines(2)}
${tb(`3. Trên đồ thị ${m('u')}–${m('x')} của sóng dọc, vùng nén, vùng dãn ở đâu? Hai vùng nén liên tiếp cách bao xa?`)}${lines(1)}
${tb('4. Vì sao truyền sóng là truyền năng lượng? Phần tử môi trường làm gì?')}${lines(1)}
${tb(`5. Năng lượng sóng phụ thuộc ${A}, ${fq} thế nào? Cường độ sóng là gì?`)}${lines(2)}
${tb('6. Sóng âm trong không khí là sóng gì? Tai nghe dải tần nào? Âm to, âm cao do đâu?')}${lines(2)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/6 câu · chưa thuộc: ${f(25)} ${nw(`${to} đọc lại ô ${f(12)} Tập`)}</div>
${h3(2, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '4·2')}
${rkHai([1, 2, 3, 4], [5, 6, 7])}
${h3(3, 'V · Bài toán mẫu: loa của lớp', '4·3')}
<div class="card soft" style="padding:1.2mm 3mm">Loa của lớp phát âm tần số ${hz('680')}; tốc độ âm trong không khí ${ms('340')}.
<div><b>a)</b> Âm trong không khí là sóng ngang hay dọc? Phần tử khí dao động theo phương nào?</div><div><b>b)</b> Tính bước sóng.</div>
<div><b>c)</b> Khoảng cách hai vùng nén liên tiếp; từ một vùng nén tới vùng dãn gần nhất.</div>
<div><b>d)</b> Âm vào nước bể bơi, tốc độ ${ms('1500')}: tần số và bước sóng trong nước?</div></div>
<table><tr><th style="width:62mm">Câu trong đề</th><th>Dữ liệu ${to} kiến thức</th></tr>
<tr><td>“tần số 680 Hz”, “340 m/s”</td><td>${m('f=680')} Hz, ${m('v=340')} m/s ${to} ${m('\\lambda=v/f')}</td></tr>
<tr><td style="height:6.5mm">“hai vùng nén liên tiếp”, “nén … dãn gần nhất”</td><td></td></tr>
<tr><td style="height:6.5mm">“vào nước … 1500 m/s”</td><td></td></tr></table>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('GIẢI BÀI TOÁN MẪU · BÀI TẬP VỀ NHÀ · THỬ THÁCH')}
${h3(1, 'Giải bài toán mẫu', '5·1')}
<div class="fig-side" style="${fs(46)}"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl('a) Loại sóng, phương dao động:', 2)}${wl(`b) ${m('\\lambda=')}`, 1)}${wl('c) Nén – nén; nén – dãn gần nhất:', 2)}${wl(`d) ${m("f'=")} ; ${m("\\lambda'=")}`, 2)}${wl('Kiểm tra: tai nghe được không? Vào nước λ tăng hay giảm?'.replace('λ', L), 1)}</div>${H.ongLoa({ so: false })}</div>
${h3(2, `Điền bước còn thiếu: cùng đề, đổi tần số thành ${hz('425')}`, '5·2')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:.6mm 3mm">
<div class="ln" style="height:7mm"><b>Bước 1:</b> ${nw(`${m('\\lambda=\\dfrac{340}{425}=')} ${f(14)} m`)} &nbsp;·&nbsp; <b>Bước 2:</b> nén – dãn gần nhất: ${nw(`${f(14)} m`)}</div>
<div class="ln" style="height:7mm"><b>Bước 3:</b> trong nước ${nw(`${m("f'=")} ${f(14)} Hz`)} &nbsp;·&nbsp; ${nw(`${m("\\lambda'=")} ${f(14)} m`)}</div></div>
${K.btvn().replace('<i>1</i>', '<i>3</i>')}
${h3(4, 'Thử thách phân tầng', '5·4')}
<div class="fig-side" style="${fs(40)}">${box(wl(`${m('\\bigstar')} Âm ${hz('1000')} trong không khí (${ms('v=340')}). Hai vùng nén liên tiếp cách bao xa?`, 2)
 + wl(`${m('\\bigstar\\bigstar')} Loa nhỏ phát đều mọi hướng; cách ${u('2', 'm')}, ${u('I=0{,}08', 'W/m^2')}. Cách ${u('4', 'm')} thì ${I} bằng bao nhiêu?`, 3)
 + wl(`${m('\\bigstar\\bigstar\\bigstar')} Trạm nhận sóng P trước sóng S ${u('20', 's')}; ${u('v_P=8', 'km/s')}, ${u('v_S=4{,}5', 'km/s')}. Tâm động đất cách trạm bao xa?`, 4))}${H.dongDat('Hai sóng cùng xuất phát, cùng đường d.')}</div>
${h3(5, 'VI · Mang về: điều em dễ quên nhất', '5·5')}
${box(wl('1.', 1) + wl('2.', 1) + wl('3.', 1))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Phân biệt sóng ngang và sóng dọc',
    de: `<span class="d1x"></span>(1) Dây thép căng ngang, tay rung đầu A lên – xuống. (2) Ống chứa khí, pit-tông đẩy – kéo dọc trục ống. (3) Sỏi rơi xuống hồ, gợn tròn lan ra, phao nhấp nhô lên – xuống.<br><b>a)</b> mỗi trường hợp: hai phương vuông góc hay trùng nhau, sóng ngang hay dọc (a<sub>1</sub>, a<sub>2</sub>, a<sub>3</sub>)<br><b>b)</b> trong lòng một khối khí truyền được sóng ở (1) hay (2)? Lí do ghi ở phần giải<br><b>c)</b> rung đầu A nhanh gấp đôi: sóng (1) có thành sóng dọc không (có/không)?`,
    nd: `so hai phương: phương ${f(25)} và phương ${f(25)}; không dựa vào hướng dây, ống hay tần số`,
    a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'a<sub>3</sub>', 'b', 'c'], gi: 2, cot: 5 },
  { t: 'Dạng 2 · Trung bình · Sóng truyền đi cái gì, phần tử ở lại',
    de: `<div class="fig-side" style="grid-template-columns:1fr 40mm"><div>Sỏi rơi xuống mặt hồ yên lặng tại O, sóng tròn lan ra với ${ms('v=0{,}80')}. Phao câu cách O ${u('6{,}0', 'm')}, lá cách O ${u('9{,}6', 'm')}.<br><b>a)</b> kể từ lúc sỏi rơi, sau bao lâu phao (a<sub>1</sub>), lá (a<sub>2</sub>) bắt đầu nhấp nhô<br><b>b)</b> sau ${u('20', 's')} sóng lan tới cách O bao xa (b<sub>1</sub>); phao dời xa O thêm bao nhiêu (b<sub>2</sub>)<br><b>c)</b> từ O tới phao, sóng truyền đi nước ở O hay năng lượng dao động</div>${H.hoThang('')}</div>`,
    nd: `${m('s=vt')} là quãng của ${f(16)}; phao chỉ ${f(25)} quanh chỗ cũ`,
    a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], gi: 2, cot: 5 },
  { t: 'Dạng 3 · Trung bình · Sóng dọc: vùng nén, vùng dãn và bước sóng',
    de: `<div class="fig-side" style="grid-template-columns:1fr 44mm"><div>Loa phát âm ${hz('f=1700')} vào ống dài chứa khí, ${ms('v=340')}.<br><b>a)</b> sóng ngang hay dọc (a<sub>1</sub>); bước sóng (a<sub>2</sub>)<br><b>b)</b> khoảng cách hai vùng nén liên tiếp (b<sub>1</sub>); vùng nén – vùng dãn gần nhất (b<sub>2</sub>)<br><b>c)</b> từ vùng nén thứ nhất đến vùng nén thứ sáu<br><b>d)</b> lớp khí ở M có li độ ${m('u=+A')}: M thuộc vùng nén, vùng dãn hay không vùng nào</div>${H.ongLoa({ cap: '' })}</div>`,
    nd: `${m('\\lambda=v/f')}; nén – nén ${f(12)}, nén – dãn ${f(12)}; từ vùng 1 tới vùng 6 có ${f(10)} khoảng`,
    a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c', 'd'], gi: 2, cot: 6 },
  { t: `Dạng 4 · Trung bình · Năng lượng sóng tỉ lệ ${m('A^2')} và ${m('f^2')}`,
    de: `Vẩy đầu một sợi dây dài để tạo sóng ngang, ${ms('v=2{,}0')} không đổi. Năng lượng truyền qua một điểm mỗi giây tỉ lệ ${m('A^2')} và ${m('f^2')}. Lần 1: ${u('A_1=5{,}0', 'cm')}, ${hz('f_1=1{,}0')}. Năng lượng mỗi giây ở các lần sau gấp mấy lần lần 1?<br><b>a)</b> ${u('A_2=15', 'cm')}, ${hz('f_2=1{,}0')} &nbsp; <b>b)</b> ${u('A_3=5{,}0', 'cm')}, ${hz('f_3=0{,}50')} &nbsp; <b>c)</b> ${u('A_4=3{,}0', 'cm')}, ${hz('f_4=2{,}5')}<br><b>d)</b> giữ ${hz('f=1{,}0')}: biên độ bao nhiêu để năng lượng gấp 4 lần lần 1`,
    nd: `${nw(`${m('\\dfrac{E_n}{E_1}=')} ${f(30)}`)}; ${v} ${ck}có ${ck}không có mặt trong tỉ số`,
    a: ['a', 'b', 'c', 'd'], gi: 2 },
  { t: 'Dạng 5 · Khó · Cường độ sóng: nguồn điểm và tấm hứng',
    de: `<div class="fig-side" style="grid-template-columns:1fr 42mm"><div>Nguồn âm điểm phát đều mọi phương trong không khí, bỏ qua hấp thụ. Tại M cách nguồn ${u('r_1=3{,}0', 'm')}: ${u('I_1=0{,}020', 'W/m^2')}.<br><b>a)</b> công suất của nguồn<br><b>b)</b> cường độ âm tại N cách nguồn ${u('r_2=6{,}0', 'm')}<br><b>c)</b> tấm phẳng ${u('S=0{,}50', 'm^2')} đặt tại M, vuông góc phương truyền: năng lượng qua tấm trong ${nw('10 phút')}</div>${H.nguonMN('')}</div>`,
    nd: `${nw(`${m('P=I\\cdot')} ${f(16)}`)}; ${nw(`${m('E=')} ${f(16)}`)}, ${m('t')} đổi ra ${f(10)}`,
    a: ['a', 'b', 'c'], gi: 3 },
  { t: 'Dạng 6 · Nâng cao · Sóng P và sóng S từ cùng tâm chấn',
    de: `<span class="d6x"></span><div class="fig-side" style="grid-template-columns:1fr 42mm"><div>Động đất phát đồng thời sóng P (dọc), ${u('v_P=6{,}0', 'km/s')}, và sóng S (ngang), ${u('v_S=3{,}5', 'km/s')}, cùng đường trong vỏ Trái Đất. Trạm đo ghi sóng P tới trước sóng S ${u('\\Delta t=30', 's')} (số minh hoạ).<br><b>a)</b> lõi ngoài Trái Đất ở thể lỏng: sóng nào không qua được lõi ngoài? Vì sao<br><b>b)</b> tâm chấn cách trạm bao nhiêu kilômét<br><b>c)</b> kể từ lúc động đất, sóng P tới trạm sau bao lâu</div>${H.dongDat('')}</div>`,
    nd: `${nw(`${m('\\dfrac{d}{v_S}-\\dfrac{d}{v_P}=')} ${f(12)}`)}; sóng ngang ${ck}có ${ck}không truyền trong chất lỏng`,
    a: ['a', 'b', 'c'], gi: 2 },
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
const s1 = 'a<sub>1</sub>', s2 = 'a<sub>2</sub>', s3 = 'a<sub>3</sub>', b1 = 'b<sub>1</sub>', b2 = 'b<sub>2</sub>';
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–3', 'DẠNG 4–6'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `(1) Lò xo treo thẳng đứng, đẩy – kéo đầu dưới lên xuống dọc lò xo. (2) Gảy dây đàn ghi-ta căng ngang, dây rung vuông góc với dây. (3) Âm từ loa truyền trong nước bể bơi.<br><b>a)</b> sóng ngang hay sóng dọc ở (1), (2), (3)<br><b>b)</b> trường hợp nào truyền được trong chân không`, o: [s1, s2, s3, ['b', 30]], ow: 20 },
    { t: 'Dạng 1 · Bài 2', de: `(1) Sóng P động đất: lớp đất dao động dọc phương truyền. (2) Dây dài treo từ trần, lắc đầu dưới qua lại nằm ngang. (3) Gõ búa vào mặt bên thanh thép dài: thanh rung vuông góc trục, sóng lan dọc thanh.<br><b>a)</b> sóng ngang hay sóng dọc ở (1), (2), (3)<br><b>b)</b> sóng ở trường hợp nào truyền được trong lòng chất lỏng`, o: [s1, s2, s3, ['b', 30]], ow: 20 },
    { t: 'Dạng 2 · Bài 1', de: `Sóng trên mặt hồ lan từ O với ${ms('v=0{,}50')}. Phao cách O ${u('4{,}0', 'm')}, lá cách O ${u('7{,}0', 'm')}.<br><b>a)</b> sau bao lâu phao, lá bắt đầu nhấp nhô<br><b>b)</b> sau ${u('30', 's')} sóng cách O bao xa; phao dời thêm bao nhiêu`, o: [s1, s2, b1, b2], ow: 20 },
    { t: 'Dạng 2 · Bài 2', de: `Sóng ngang trên dây dài, ${ms('v=2{,}5')}; dải băng buộc cách đầu dây ${u('5{,}0', 'm')}. Vẩy đầu dây lúc ${m('t=0')}.<br><b>a)</b> sau bao lâu dải băng bắt đầu dao động<br><b>b)</b> trong ${u('6{,}0', 's')} sóng đi được bao xa; dải băng dời theo phương truyền bao nhiêu`, o: ['a', b1, b2], ow: 20 },
    { t: 'Dạng 3 · Bài 1', de: `Âm ${hz('850')} truyền trong không khí, ${ms('v=340')}.<br><b>a)</b> bước sóng<br><b>b)</b> nén – nén liên tiếp; nén – dãn gần nhất<br><b>c)</b> từ vùng nén thứ nhất đến vùng nén thứ tư`, o: ['a', b1, b2, 'c'], ow: 20 },
    { t: 'Dạng 3 · Bài 2', de: `Sóng dọc trên lò xo, tần số ${hz('5{,}0')}; từ vùng nén thứ nhất đến vùng nén thứ năm dài ${u('60', 'cm')}.<br><b>a)</b> bước sóng<br><b>b)</b> tốc độ truyền sóng<br><b>c)</b> vùng nén – vùng dãn gần nhất`, o: ['a', 'b', 'c'], ow: 20 },
  ], [
    { t: 'Dạng 4 · Bài 1', de: `Sóng trên dây, lần 1: ${u('A_1=4{,}0', 'cm')}, ${hz('f_1=2{,}0')}. Năng lượng mỗi giây gấp mấy lần lần 1?<br><b>a)</b> ${u('A=12', 'cm')}, ${hz('f=2{,}0')} &nbsp; <b>b)</b> ${u('A=4{,}0', 'cm')}, ${hz('f=6{,}0')} &nbsp; <b>c)</b> ${u('A=2{,}0', 'cm')}, ${hz('f=4{,}0')}<br><b>d)</b> giữ ${u('A=4{,}0', 'cm')}: tần số bao nhiêu để năng lượng gấp 16 lần`, o: ['a', 'b', 'c', 'd'], ow: 18 },
    { t: 'Dạng 4 · Bài 2', de: `Sóng trên dây, lần 1: ${u('A_1=6{,}0', 'cm')}, ${hz('f_1=1{,}5')}. Năng lượng mỗi giây gấp mấy lần lần 1?<br><b>a)</b> ${u('A=3{,}0', 'cm')}, ${hz('f=1{,}5')} &nbsp; <b>b)</b> ${u('A=6{,}0', 'cm')}, ${hz('f=4{,}5')} &nbsp; <b>c)</b> ${u('A=4{,}5', 'cm')}, ${hz('f=3{,}0')}<br><b>d)</b> giữ ${hz('f=1{,}5')}: biên độ bao nhiêu để năng lượng còn ${m('\\tfrac19')} lần 1`, o: ['a', 'b', 'c', 'd'], ow: 18 },
    { t: 'Dạng 5 · Bài 1', de: `Nguồn âm điểm phát đều, bỏ qua hấp thụ. Tại M cách nguồn ${u('2{,}0', 'm')}: ${u('I=0{,}050', 'W/m^2')}.<br><b>a)</b> công suất nguồn<br><b>b)</b> cường độ tại N cách nguồn ${u('10', 'm')}<br><b>c)</b> tấm ${u('0{,}20', 'm^2')} tại M, vuông góc phương truyền: năng lượng qua tấm trong ${nw('5 phút')}`, o: ['a', 'b', 'c'], ow: 22 },
    { t: 'Dạng 5 · Bài 2', de: `Nguồn âm điểm công suất ${u('P=4{,}0', 'W')} phát đều, bỏ qua hấp thụ.<br><b>a)</b> cường độ âm cách nguồn ${u('1{,}0', 'm')}<br><b>b)</b> khoảng cách tới nguồn tại đó ${u('I=0{,}010', 'W/m^2')}<br><b>c)</b> cửa sổ ${u('1{,}5', 'm^2')} cách nguồn ${u('5{,}0', 'm')}, vuông góc phương truyền: năng lượng qua cửa trong ${nw('1 phút')}`, o: ['a', 'b', 'c'], ow: 22 },
    { t: 'Dạng 6 · Bài 1', de: `Sóng P: ${u('v_P=8{,}0', 'km/s')}; sóng S: ${u('v_S=4{,}5', 'km/s')}, cùng đường. Trạm ghi P trước S ${u('21', 's')}.<br><b>a)</b> sóng nào tới trạm trước? Vì sao<br><b>b)</b> tâm chấn cách trạm bao xa<br><b>c)</b> sóng S tới trạm sau lúc động đất bao lâu`, o: [['a', 30], 'b', 'c'], ow: 20 },
    { t: 'Dạng 6 · Bài 2', de: `${u('v_P=6{,}0', 'km/s')}, ${u('v_S=4{,}0', 'km/s')}, cùng đường. Trạm X ghi sóng P sau động đất ${u('25', 's')}.<br><b>a)</b> tâm chấn cách trạm X bao xa<br><b>b)</b> sóng S tới X sau sóng P bao lâu<br><b>c)</b> trạm Y ghi S sau P ${u('20', 's')}: tâm chấn cách Y bao xa`, o: ['a', 'b', 'c'], ow: 20 },
  ]],
  dap: [
    `D1·1: a<sub>1</sub>) dọc · a<sub>2</sub>) ngang · a<sub>3</sub>) dọc · b) không trường hợp nào &nbsp;|&nbsp; D1·2: a<sub>1</sub>) dọc · a<sub>2</sub>) ngang · a<sub>3</sub>) ngang · b) chỉ (1) &nbsp;|&nbsp; D2·1: a<sub>1</sub>) 8,0 s · a<sub>2</sub>) 14 s · b<sub>1</sub>) 15 m · b<sub>2</sub>) gần như 0 &nbsp;|&nbsp; D2·2: a) 2,0 s · b<sub>1</sub>) 15 m · b<sub>2</sub>) gần như 0 &nbsp;|&nbsp; D3·1: a) 0,40 m · b<sub>1</sub>) 0,40 m · b<sub>2</sub>) 0,20 m · c) 1,2 m &nbsp;|&nbsp; D3·2: a) 15 cm · b) 0,75 m/s · c) 7,5 cm`,
    `D4·1: a) 9 · b) 9 · c) 1 (không đổi) · d) 8,0 Hz &nbsp;|&nbsp; D4·2: a) 0,25 · b) 9 · c) 2,25 · d) 2,0 cm &nbsp;|&nbsp; D5·1: a) ${xx} 2,51 W · b) 0,0020 W/m² · c) 3,0 J &nbsp;|&nbsp; D5·2: a) ${xx} 0,318 W/m² · b) ${xx} 5,64 m · c) ${xx} 1,15 J &nbsp;|&nbsp; D6·1: a) sóng P, vì ${m('v_P\\gt v_S')} · b) 216 km · c) 48 s &nbsp;|&nbsp; D6·2: a) 150 km · b) 12,5 s · c) 240 km`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 3], kq: [[1, 2, 3], [4, 5, 6]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'sóng ngang 1·4 · sóng dọc 2·1 · đo xung 2·3 · môi trường, âm, bước sóng 3·1 · năng lượng, cường độ 3·2 · bẫy 3·3 · bài mẫu 4·3 · dạng 1–3 ở 6·1 · dạng 4–6 ở 7·1',
  out: process.argv[2],
});
