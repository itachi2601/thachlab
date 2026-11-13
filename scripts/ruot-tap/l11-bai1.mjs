// Ruột tập VL11 – Bài 1 · Dao động điều hoà (lesson id 20). Quyển Chương 1 lớp 11: bài 1 = tr. 1–12.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l11-bai1.mjs (toàn bộ SVG tự vẽ). Nội dung theo bài web (book/cache/20.json, tải từ DB 13/11/2026):
// mở bài cái đu, II.1–II.5 (dao động cơ, tuần hoàn, đồ thị x–t, phương trình, chuyển động tròn đều), ba bẫy, Trả bài 5 câu,
// bài toán mẫu x = 6cos(5πt + π/2), thử sức, thử thách, 5 dạng bài tập mẫu.
// Đáp số Bài tương tự (tuongTu.dap) tính bằng Python 13/11/2026 (math.cos theo radian, làm tròn 3 chữ số có nghĩa).
// Chạy: node scripts/ruot-tap/l11-bai1.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl11-bai1.pdf
//       node scripts/ruot-tap/l11-bai1.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l11-bai1/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai, yn } from './khung.mjs';
import { hinhL11b1 as H } from './hinh-l11-bai1.mjs';

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
  const out = resolve(HERE, 'out/hinh-l11-bai1'); mkdirSync(out, { recursive: true });
  const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true, args: ['--allow-file-access-from-files'] });
  const pg = await b.newPage();
  const kx = `<link rel="stylesheet" href="${pathToFileURL(BOOK + 'node_modules/katex/dist/katex.min.css').href}">`;
  for (const [name, fn] of Object.entries(H)) {
    writeFileSync(out + '/_tmp.html', `<!doctype html><meta charset="utf-8">${kx}<style>${css}</style>${fn()}`);
    await pg.goto(pathToFileURL(out + '/_tmp.html').href, { waitUntil: 'networkidle0' });
    await pg.evaluate('document.fonts.ready');
    await (await pg.$('.fig')).screenshot({ path: `${out}/${name}.png` });
    console.log(`${name}.png`);
  }
  await b.close();
  process.exit(0);
}

const K = khoiTao({ bai: 1, lid: 20, ten: 'DAO ĐỘNG ĐIỀU HOÀ', lop: 11, baiDau: 1, sub: 'Vật lí 11 · Chương 1: Dao động' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const pt = (s) => nw(m(s));
const PT = m('x=A\\cos(\\omega t+\\varphi)');
// chữ Hi Lạp trong chữ thường (đáp số, tiêu đề): Source Sans 3 không có π ω φ → rơi về Helvetica; đổi sang KaTeX
const gr = (str) => str.replace(/[πωφα]/g, (c) => m({ 'π': '\\pi', 'ω': '\\omega', 'φ': '\\varphi', 'α': '\\alpha' }[c]));
const w = m('\\omega'), ph = m('\\varphi');

// Bài tương tự xếp 1 cột, ô đáp số cuối dòng của ý (giống l10-bai23).
const ttCot = '<style>.bt:has(.d3k) .ans{grid-template-columns:1fr 1fr 1fr 1.9fr}.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}.cosb td,.cosb th{padding:.3mm 1.2mm;text-align:center;font-size:var(--fs-sm)}</style>';

const p1 = `${ttCot}<section class="page">
${head('BÀI 1 · DAO ĐỘNG ĐIỀU HOÀ', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Nêu được <b>dao động cơ</b>, <b>dao động tuần hoàn</b>, <b>dao động điều hoà</b>`)}
${dong(`${ck}Đọc ${m('A')}, ${w}, ${ph} từ phương trình; tính ${m('T')}, ${m('f')}, pha và li độ`)}
${dong(`${ck}Đọc ${m('A')}, ${m('T')}, li độ lúc ${m('t=0')} trên <b>đồ thị li độ – thời gian</b>`)}
${dong(`${ck}Dùng <b>chuyển động tròn đều</b> để viết phương trình dao động`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<div class="fig-side" style="${fs(46)}"><div>
<p style="margin:0 0 1mm">Em ngồi trên đu, bạn đẩy nhẹ một cái. Đu đi tới, dừng lại, quay về, sang phía bên kia… Em bấm đồng hồ: cứ <b>3 s</b> đu lại về đúng chỗ cũ và đi theo hướng cũ. Chuyển động của đu thuộc loại nào?</p>
${opt('A', 'Tuần hoàn, vì sau những khoảng thời gian bằng nhau đu trở lại như cũ')}
${opt('B', 'Không tuần hoàn, vì đu lúc nhanh lúc chậm')}
${opt('C', 'Chỉ tuần hoàn khi đu đi thật nhanh')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 1)}</div>
${H.du()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Dao động cơ', '1·4')}
<div class="card" style="padding:1.2mm 3mm">
<div><b>Dao động cơ</b> là chuyển động ${f(25)} quanh một ${f(30)} (viết tắt VTCB).</div></div>
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div><b>Thí nghiệm · Làm:</b> vật gắn lò xo đang đứng yên; kéo vật lệch ra rồi thả tay.</div>
<div><b>Quan sát:</b> vật đi ${f(25)} hai bên chỗ đứng yên ban đầu.</div>
<div><b>Rút ra:</b> chỗ đứng yên ban đầu là ${f(30)}; vật dao động quanh nó, giữa hai ${f(14)} ${m('-A')} và ${m('+A')}.</div>
${wl('Kể một vật quanh em cũng dao động cơ:', 2)}</div>
${H.conLac()}</div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('DAO ĐỘNG TUẦN HOÀN · ĐỒ THỊ LI ĐỘ – THỜI GIAN')}
${h3(1, 'II.2 · Dao động tuần hoàn', '2·1')}
<div class="card" style="padding:1.2mm 3mm">
<div><b>Tuần hoàn:</b> sau những khoảng thời gian ${f(25)}, vật trở lại vị trí ${f(14)} theo ${f(25)} cũ.</div></div>
<table><tr><th>Chuyển động</th><th style="width:33mm">Tuần hoàn?</th></tr>
<tr><td>Con lắc đồng hồ đung đưa</td>${yn}</tr>
<tr><td>Cành cây đu đưa khi gió thổi lúc mạnh lúc yếu</td>${yn}</tr>
<tr><td>Cái đu được đẩy mạnh dần rồi yếu dần</td>${yn}</tr>
<tr><td>Cái đu ở Dự đoán: lúc nhanh lúc chậm trong mỗi lần đi về, cứ 3 s lại như cũ</td>${yn}</tr></table>
<div style="margin-top:1mm">Đu qua chỗ cũ nhưng đi <b>ngược chiều</b>: đã lặp lại chưa? ${ck}rồi &nbsp;${ck}chưa</div>
<div class="card soft" style="margin-top:1mm;padding:1mm 3mm"><b>Dao động điều hoà</b> là dao động tuần hoàn đơn giản nhất: li độ biến thiên theo hàm ${f(16)} của thời gian.
<div class="hint">Hàm côsin nhận giá trị từ −1 đến 1 và lặp lại sau mỗi góc ${m('2\\pi')} rad.</div></div>
${h3(2, 'II.3 · Đồ thị li độ – thời gian', '2·2')}
<div class="card fig-side" style="${fs(48)};padding:1.2mm 3mm"><div>
<div><b>Thí nghiệm · Làm:</b> gắn bút lên vật dao động, kéo tờ giấy chạy đều qua đầu bút.</div>
<div><b>Rút ra:</b> đồ thị li độ theo thời gian là đường ${f(25)}.</div>
<div style="margin-top:.8mm">${m('x')} (<b>li độ</b>): vị trí của vật so với ${f(16)}; ${m('x')} ${ck}luôn dương ${ck}có thể âm</div>
<div>${m('A')} (<b>biên độ</b>): giá trị ${f(25)} của li độ</div>
<div>${m('T')} (<b>chu kì</b>): thời gian ${f(16)} để vật về chỗ cũ theo hướng cũ. Cái đu ở Dự đoán: ${nw(`${m('T=')} ${f(12)}&nbsp;s`)}</div>
<div>${m('f=\\dfrac{1}{T}')} (<b>tần số</b>): số dao động trong 1 s, đơn vị ${f(12)}</div>
${wl('Đồ thị là hình sin, sao phương trình lại dùng côsin?', 2)}</div>
${H.butVe()}</div>
${h3(3, 'Làm nhanh: đọc đồ thị', '2·3')}
<div class="fig-side" style="${fs(48)}">${box(`<div>Đồ thị li độ – thời gian của một vật ở hình bên.</div>
<div style="margin-top:1mm">${nw(`${m('A=')} ${f(14)}&nbsp;cm`)} &nbsp;&nbsp; ${nw(`${m('T=')} ${f(14)}&nbsp;s`)} &nbsp;&nbsp; ${nw(`${m('f=')} ${f(14)}&nbsp;Hz`)}</div>
<div style="margin-top:1.5mm">Lúc ${m('t=0')}: ${nw(`${m('x=')} ${f(14)}&nbsp;cm`)} &nbsp;&nbsp; lúc ${m('t=0{,}4')} s: ${nw(`${m('x=')} ${f(14)}&nbsp;cm`)}</div>`)}${H.doThiP2()}</div>
${foot(2)}</section>`;

const cosBang = `<table class="cosb" style="width:auto;margin-top:1mm"><tr><th>góc (rad)</th><td>0</td><td>${m('\\frac{\\pi}{6}')}</td><td>${m('\\frac{\\pi}{3}')}</td><td>${m('\\frac{\\pi}{2}')}</td><td>${m('\\frac{2\\pi}{3}')}</td><td>${m('\\pi')}</td><td>${m('\\frac{3\\pi}{2}')}</td><td>${m('2\\pi')}</td></tr>
<tr><th>côsin</th><td>1</td><td>${m('\\frac{\\sqrt3}{2}')}</td><td>${m('\\frac12')}</td><td>0</td><td>${m('-\\frac12')}</td><td>−1</td><td>0</td><td>1</td></tr></table>`;

const p3 = `<section class="page">
${head('PHƯƠNG TRÌNH DAO ĐỘNG · CHUYỂN ĐỘNG TRÒN ĐỀU')}
${h3(1, 'II.4 · Phương trình dao động điều hoà', '3·1')}
<div class="card" style="padding:1.2mm 3mm">
<div style="font-size:var(--fs-h3)">${PT} &nbsp;&nbsp; ${m('\\omega=')} ${f(16)} &nbsp;&nbsp; ${m('f=\\dfrac1T')}</div>
<table style="margin-top:1mm"><tr><th style="width:18mm">Kí hiệu</th><th style="width:30mm">Tên</th><th style="width:20mm">Đơn vị</th><th>Ghi nhớ</th></tr>
<tr><td>${m('x')}</td><td></td><td>cm hoặc m</td><td>có thể âm</td></tr>
<tr><td>${m('A')}</td><td></td><td></td><td>${m('A')} ${ck}${m('\\gt 0')} &nbsp;${ck}có thể âm</td></tr>
<tr><td>${w}</td><td></td><td></td><td>${m('\\omega=2\\pi f')}</td></tr>
<tr><td>${m('\\omega t+\\varphi')}</td><td></td><td>rad</td><td>cho biết vị trí và chiều chuyển động lúc ${m('t')}</td></tr>
<tr><td>${ph}</td><td></td><td></td><td>là pha lúc ${m('t=')} ${f(10)}</td></tr></table>
<div class="hint" style="margin-top:.6mm">${m('\\pi\\approx3{,}14')} · ${m('\\pi\\ \\mathrm{rad}=180^\\circ')} · bấm côsin của pha thì để máy tính ở chế độ <b>R</b> (radian).</div>
${cosBang}</div>
<div class="card soft" style="padding:1.2mm 3mm"><div><b>Ví dụ:</b> ${m('x=5\\cos\\left(2\\pi t+\\frac{\\pi}{3}\\right)')} cm: &nbsp;${nw(`${m('A=')} ${f(14)}`)} &nbsp; ${nw(`${m('\\omega=')} ${f(16)}`)} &nbsp; ${nw(`${m('\\varphi=')} ${f(14)}`)}</div>
<div>Lúc ${m('t=0')}: ${nw(`${m('x=')} ${f(16)}`)} &nbsp; · Đổi ${ph}: đồ thị chỉ ${f(25)}; tăng ${ph} thì dịch sang ${f(25)}</div></div>
${h3(2, 'II.5 · Liên hệ với chuyển động tròn đều', '3·2')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div><b>Bóng van xe đạp:</b> bánh xe quay đều, van chạy vòng tròn; chiếu đèn song song mặt bánh xe thì bóng van trên tường chạy ${f(25)} theo một đường thẳng.</div>
<div style="margin-top:.6mm">${m('M')} quay đều với tốc độ góc ${w}, bán kính ${nw(`${m('OM=')} ${f(10)}`)}.</div>
<div>Lúc ${m('t=0')}, ${m('OM')} hợp với ${m('Ox')} góc ${f(12)}.</div>
<div>Hình chiếu ${m('Q')} của ${m('M')} lên ${m('Ox')}: ${nw(`${m('x=')} ${f(30)}`)}</div>
<div>${m('Q')} ở biên khi ${m('M')} ở ${f(40)}</div>
<div>Từ biên này sang biên kia: ${m('M')} quay ${f(16)} vòng, mất ${nw(`${m('t=')} ${f(12)}`)} (theo ${m('T')})</div></div>
${H.tronDeu()}</div>
${h3(3, 'Thử với mô phỏng: vật nặng treo lò xo', '3·3')}
${box(`<div>PhET <i>Masses and Springs</i> (CC BY 4.0): treo quả cân, kéo xuống một đoạn rồi thả.</div>
<div><b>Dự đoán:</b> vật nặng hơn thì dao động ${ck}nhanh hơn &nbsp;${ck}chậm hơn &nbsp;${ck}như cũ</div>
<table style="margin:.8mm 0"><tr><th>Quả cân (g)</th><th>50</th><th>100</th><th>250</th></tr>
<tr><td>${m('T')} (s) = thời gian 5 dao động : 5</td><td></td><td></td><td></td></tr></table>
<div><b>Rút ra:</b> vật nặng hơn thì ${m('T')} ${f(25)}; lò xo cứng hơn thì ${m('T')} ${f(25)}.</div>`)}
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('BẪY · TRẢ BÀI · TỰ KIỂM TRA')}
${h3(1, 'III · Ba cái bẫy hay sập', '4·1')}
<div class="card" style="padding:1mm 3mm">
<div class="trap">${ck}<span><b>“Li độ là quãng đường đã đi.”</b> ${m('x')} là vị trí so với VTCB, có thể âm.</span></div>
<div class="trap">${ck}<span><b>“Biên độ có thể âm.”</b> ${m('A\\gt0')}; dấu trừ nằm ở pha: ${m('-\\cos\\alpha=\\cos(\\alpha+\\pi)')}.</span></div>
<div class="trap">${ck}<span><b>“Hết một chu kì thì ${m('x=0')}.”</b> Hết một chu kì vật về đúng vị trí cũ, theo chiều cũ.</span></div></div>
${h3(2, 'IV · Trả bài 5 câu', '4·2')}
${box(`${tb('1. Dao động cơ là gì?')}${lines(1)}
${tb('2. Dao động tuần hoàn là gì?')}${lines(2)}
${tb('3. Viết phương trình dao động điều hoà, nêu tên từng kí hiệu (Biên – Tần – Pha).')}${lines(3)}
${tb('4. Đồ thị li độ – thời gian có dạng gì? Đọc A và T ở đâu trên đồ thị?')}${lines(2)}
${tb(`5. Dao động điều hoà liên hệ thế nào với chuyển động tròn đều? A và ${w} ứng với gì?`)}${lines(2)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/5 câu · chưa thuộc: ${f(25)} ${nw(`→ đọc lại ô ${f(12)} Tập`)}</div>
${h3(3, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '4·3')}
${rkHai([1, 2, 3], [4, 5, 6])}
${h3(4, 'Câu nhanh', '4·4')}
${box(`<div><b>a)</b> Vật dao động theo ${m('x=4\\cos(\\pi t)')} cm. Khi vật ở biên phía âm, ${nw(`${m('x=')} ${f(14)}`)}</div>
<div><b>b)</b> Biên độ của ${m('x=-3\\cos(2t)')} cm: ${nw(`${m('A=')} ${f(14)}`)}; viết lại ${nw(`${m('x=')} ${f(36)}`)}</div>
<div><b>c)</b> Vật dao động theo ${m('x=10\\cos(2\\pi t)')} cm. Lúc ${m('t=0{,}25')} s: pha ${f(14)}, ${nw(`${m('x=')} ${f(14)}`)}</div>`)}
${h3(5, 'VI · Mang về: điều em dễ quên nhất', '4·5')}
${box(wl('1.', 1) + wl('2.', 1) + wl('3.', 1))}
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TẬP VỀ NHÀ · BÀI TOÁN MẪU · THỬ THÁCH')}
${K.btvn()}
${h3(2, 'V · Bài toán mẫu: đọc phương trình, tính li độ', '5·2')}
<div class="card soft" style="padding:1.2mm 3mm">Một vật dao động điều hoà theo phương trình ${m('x=6\\cos\\left(5\\pi t+\\frac{\\pi}{2}\\right)')} cm (${m('t')} tính bằng s). Xác định biên độ, tần số góc, pha ban đầu và li độ của vật lúc ${m('t=0')} và lúc ${m('t=0{,}1')} s.</div>
<table><tr><th style="width:46mm">Câu trong đề</th><th>Dữ liệu → kiến thức</th></tr>
<tr><td>“theo phương trình …”</td><td>đối chiếu với ${PT}</td></tr>
<tr><td style="height:6.5mm">“li độ lúc ${m('t=0')}”</td><td></td></tr>
<tr><td style="height:6.5mm">“li độ lúc ${m('t=0{,}1')} s”</td><td></td></tr>
<tr><td>Dữ kiện ngầm: góc tính bằng rad</td><td>máy tính để chế độ R</td></tr></table>
<div class="fig-side" style="${fs(40)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl(`Đối chiếu: ${m('A=')} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ${m('\\omega=')} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ${m('\\varphi=')}`, 1)}${wl(`Lúc ${m('t=0')}: ${m('x=')}`, 1)}${wl(`Lúc ${m('t=0{,}1')} s: pha ${m('=')}`, 2)}${wl('Kiểm tra: |x| có vượt A không?', 1)}${wl(`Trên hình: đánh dấu ${m('M')}, ${m('Q')} lúc ${m('t=0')} và lúc pha bằng ${m('\\pi')}.`, 1)}</div>${H.tronMau('')}</div>
${h3(3, 'Câu đổi chiều', '5·3')}
${box(wl(`Cùng đề, nhưng ${m('x=-6\\cos\\left(5\\pi t+\\frac{\\pi}{2}\\right)')} cm: tìm ${m('A')}, ${ph} (với ${m('-\\pi\\lt\\varphi\\le\\pi')}) và li độ lúc ${m('t=0{,}1')} s.`, 3))}
${h3(4, 'Thử thách phân tầng', '5·4')}
<div class="fig-side" style="${fs(40)}">${box(wl(`${m('\\bigstar')} ${m('M')} quay đều một vòng hết ${nw('2 s')}, bán kính ${nw('10 cm')}. Hình chiếu ${m('Q')} đi từ biên này sang biên kia mất bao lâu?`, 2)
 + wl(`${m('\\bigstar\\bigstar')} ${m('x=8\\cos\\left(2\\pi t+\\frac{\\pi}{3}\\right)')} cm: li độ lúc ${m('t=0')} và lúc ${m('t=\\frac16')} s; trong thời gian đó ${m('M')} quay góc bao nhiêu?`, 3)
 + wl(`${m('\\bigstar\\bigstar\\bigstar')} Pít-tông động cơ chạy lên xuống nhờ trục khuỷu quay đều. Vì sao chỉ <b>gần</b> dao động điều hoà?`, 2))}${H.tronTT()}</div>
${foot(5)}</section>`;

const dang = [
  { t: gr('Dạng 1 · Dễ · Đọc phương trình: A, ω, φ, T, f, li độ'),
    de: `Vật dao động điều hoà theo ${m('x=10\\cos\\left(4\\pi t+\\frac{2\\pi}{3}\\right)')} (${m('x')}: cm, ${m('t')}: s).<br><b>a)</b> biên độ, tần số góc, pha ban đầu;&ensp;<b>b)</b> chu kì và tần số;&ensp;<b>c)</b> pha và li độ lúc ${m('t=0{,}25')} s`,
    nd: `${nw(`${m('T=')} ${f(14)}`)}; ${nw(`${m('f=')} ${f(14)}`)}; pha ${m('=')} ${f(16)} (rad); ${m('x=A\\cos(\\text{pha})')}`, a: ['a', 'b', 'c'], gi: 4 },
  { t: 'Dạng 2 · Trung bình · Dấu trừ trước côsin: đưa về A > 0',
    de: `Vật dao động điều hoà theo ${m('x=-6\\cos\\left(5\\pi t-\\frac{\\pi}{3}\\right)')} (${m('x')}: cm, ${m('t')}: s).&ensp;<b>a)</b> biên độ<br><b>b)</b> viết lại với ${m('A\\gt0')}, ${m('-\\pi\\lt\\varphi\\le\\pi')}, nêu ${ph};&ensp;<b>c)</b> li độ lúc ${m('t=0')} và ${m('t=0{,}2')} s`,
    nd: `${m('-\\cos\\alpha=\\cos(\\alpha')} ${f(12)} ${m('\\pi)')}; ${m('A')} luôn ${f(25)}`, a: ['a', 'b', 'c'], gi: 4 },
  { t: 'Dạng 3 · Trung bình · Đọc đồ thị li độ – thời gian',
    de: `<div class="fig-side d3k" style="grid-template-columns:1fr 46mm"><div>Hình bên là đồ thị li độ – thời gian của một vật dao động điều hoà.<br><b>a)</b> đọc biên độ ${m('A')} và chu kì ${m('T')}<br><b>b)</b> tính tần số góc ${w}<br><b>c)</b> tìm ${ph} (với ${m('0\\le\\varphi\\le\\pi')})<br><b>d)</b> viết phương trình dao động</div>${H.doThiD3('')}</div>`,
    nd: `${m('T')} = khoảng thời gian giữa hai ${f(25)} liên tiếp; ${m('x(0)=A\\cos\\varphi')}`, a: ['a', 'b', 'c', 'd'], gi: 5 },
  { t: 'Dạng 4 · Khó · Viết phương trình từ quỹ đạo và gốc thời gian',
    de: `Vật dao động điều hoà trên đoạn thẳng dài ${m('16\\ \\mathrm{cm}')}; trong ${m('20\\ \\mathrm s')} thực hiện ${m('30')} dao động toàn phần. Gốc toạ độ O ở VTCB, chiều dương sang phải, gốc thời gian lúc vật ở biên âm.<br><b>a)</b> biên độ và chu kì<br><b>b)</b> tần số góc và phương trình dao động<br><b>c)</b> li độ lúc ${m('t=\\frac13')} s`,
    nd: `${nw(`${m('L=2\\,\\cdot')} ${f(12)}`)}; ${m('T=\\frac{t}{N}')}; biên âm ⇒ ${nw(`${m('\\cos\\varphi=')} ${f(12)}`)}`, a: ['a', 'b', 'c'], gi: 6, fig: H.quyDao(), cot: 2 },
  { t: 'Dạng 5 · Khó · Hình chiếu của chuyển động tròn đều',
    de: `Đĩa tròn bán kính ${m('R=12\\ \\mathrm{cm}')} quay đều quanh tâm O, ${m('150')} vòng/phút, ngược chiều kim đồng hồ. Q là hình chiếu của điểm M ở mép đĩa lên trục Ox nằm ngang qua O (chiều dương sang phải). Lúc ${m('t=0')}, M ở điểm cao nhất.<br><b>a)</b> tốc độ góc (rad/s); biên độ và tần số góc của Q<br><b>b)</b> pha ban đầu và phương trình dao động của Q<br><b>c)</b> li độ của Q lúc ${m('t=\\frac{1}{30}')} s`,
    nd: `1 vòng ${m('=')} ${f(12)} rad; ${nw(`${m('A=')} ${f(12)}`)}; ${ph}: góc từ ${m('Ox')} tới ${m('OM')} lúc ${m('t=0')}`, a: ['a', 'b', 'c'], gi: 7, fig: H.diaD5(), cot: 2 },
];

// Bài tương tự giải vào vở (thầy chốt 10/11): 1 cột; ô đáp số 25 mm (40–48 mm khi đáp số là phương trình) cuối dòng của ý.
const oY = (s, o, wd = 25) => s.split('<br>').map((p) => {
  const y = p.match(/^<b>([a-d])\)<\/b>/);
  if (!y) return `<div>${p}</div>`;
  const ls = o.filter((l) => (Array.isArray(l) ? l[0] : l)[0] === y[1]);
  return `<div class="yo"><span>${p}</span><span class="oo">${ls.map((l) => { const [nh, rr] = Array.isArray(l) ? l : [l, wd]; return `<span class="nw"><b>${nh})</b>${f(rr)}</span>`; }).join('')}</span></div>`;
}).join('');
// o: nhãn hoặc [nhãn, rộng mm]; nhãn đầu là chữ a–d của ý
const oo = (s) => s.map((l) => (Array.isArray(l) ? l : [l, 25]));
const ttDe = (b) => b.fig ? `<div class="fig-side" style="grid-template-columns:1fr ${b.fw}mm">${`<div>${oY(b.de, oo(b.o))}</div>`}${b.fig}</div>` : oY(b.de, oo(b.o));
const vaoVo = (ds) => ds.map((b) => (b.o ? { t: b.t, de: ttDe(b), k: 0 } : b));
const nhap = (n) => ({ t: '<span class="nhap-t">Nháp / chỗ em còn vướng</span>', de: lines(n), k: 0 });
const s1 = (l) => `${l[0]}<sub>${l[1]}</sub>`;
const PTo = (l) => [l, 46];
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–3', 'DẠNG 4–5'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `${m('x=8\\cos\\left(2\\pi t+\\frac{\\pi}{6}\\right)')} (${m('x')}: cm, ${m('t')}: s). Máy tính để chế độ R.<br><b>a)</b> biên độ; pha ban đầu<br><b>b)</b> chu kì; tần số<br><b>c)</b> li độ lúc ${m('t=0{,}5')} s`, o: [s1('a1'), s1('a2'), s1('b1'), s1('b2'), 'c'] },
    { t: 'Dạng 1 · Bài 2', de: `${m('x=5\\cos\\left(\\pi t-\\frac{\\pi}{4}\\right)')} (${m('x')}: cm, ${m('t')}: s).<br><b>a)</b> tần số góc; chu kì<br><b>b)</b> li độ lúc ${m('t=0')}<br><b>c)</b> li độ lúc ${m('t=1')} s`, o: [s1('a1'), s1('a2'), 'b', 'c'] },
    { t: 'Dạng 2 · Bài 1', de: `${m('x=-4\\cos(2\\pi t)')} (${m('x')}: cm, ${m('t')}: s).<br><b>a)</b> biên độ<br><b>b)</b> pha ban đầu khi viết lại với ${m('A\\gt0')}, ${m('-\\pi\\lt\\varphi\\le\\pi')}<br><b>c)</b> li độ lúc ${m('t=0{,}25')} s`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 2 · Bài 2', de: `${m('x=-10\\cos\\left(4\\pi t+\\frac{\\pi}{6}\\right)')} (${m('x')}: cm, ${m('t')}: s).<br><b>a)</b> viết lại với ${m('A\\gt0')}, ${m('-\\pi\\lt\\varphi\\le\\pi')}<br><b>b)</b> li độ lúc ${m('t=0')}<br><b>c)</b> li độ lúc ${m('t=0{,}125')} s`, o: [PTo('a'), 'b', 'c'] },
    { t: 'Dạng 3 · Bài 1', de: `Đồ thị li độ – thời gian bên cạnh.<br><b>a)</b> biên độ; chu kì<br><b>b)</b> tần số góc<br><b>c)</b> ${ph} (với ${m('0\\le\\varphi\\le\\pi')})<br><b>d)</b> phương trình`, fig: H.doThiTT1(), fw: 44, o: [[s1('a1'), 18], [s1('a2'), 18], ['b', 18], [s1('c'), 0], ['c', 18], ['d', 40]].filter((l) => l[1]) },
    { t: 'Dạng 3 · Bài 2', de: `Đồ thị li độ – thời gian bên cạnh.<br><b>a)</b> biên độ; chu kì<br><b>b)</b> tần số góc<br><b>c)</b> ${ph} (với ${m('0\\le\\varphi\\le\\pi')})<br><b>d)</b> phương trình`, fig: H.doThiTT2(), fw: 44, o: [[s1('a1'), 18], [s1('a2'), 18], ['b', 18], [s1('c'), 0], ['c', 18], ['d', 40]].filter((l) => l[1]) },
  ], [
    { t: 'Dạng 4 · Bài 1', de: `Vật dao động điều hoà trên đoạn thẳng dài ${m('10\\ \\mathrm{cm}')}; ${m('20')} dao động toàn phần trong ${m('10\\ \\mathrm s')}. Gốc O ở VTCB, gốc thời gian lúc vật ở biên dương.<br><b>a)</b> biên độ; chu kì<br><b>b)</b> phương trình dao động<br><b>c)</b> li độ lúc ${m('t=\\frac16')} s`, o: [s1('a1'), s1('a2'), PTo('b'), 'c'] },
    { t: 'Dạng 4 · Bài 2', de: `Vật dao động điều hoà, quỹ đạo dài ${m('12\\ \\mathrm{cm}')}; ${m('15')} dao động toàn phần trong ${m('30\\ \\mathrm s')}. Gốc O ở VTCB, gốc thời gian lúc vật ở biên âm.<br><b>a)</b> biên độ; tần số góc<br><b>b)</b> phương trình dao động<br><b>c)</b> li độ lúc ${m('t=\\frac23')} s`, o: [s1('a1'), s1('a2'), PTo('b'), 'c'] },
    { t: 'Dạng 5 · Bài 1', de: `Đĩa bán kính ${m('10\\ \\mathrm{cm}')} quay đều ${m('120')} vòng/phút, ngược chiều kim đồng hồ; Q là hình chiếu của điểm M ở mép đĩa lên trục Ox qua tâm (chiều dương sang phải). Lúc ${m('t=0')}, M nằm trên Ox, phía dương.<br><b>a)</b> tần số góc của Q<br><b>b)</b> phương trình dao động của Q<br><b>c)</b> li độ của Q lúc ${m('t=\\frac{1}{12}')} s`, o: ['a', PTo('b'), 'c'] },
    { t: 'Dạng 5 · Bài 2', de: `Đĩa bán kính ${m('8\\ \\mathrm{cm}')} quay đều ${m('30')} vòng/phút, ngược chiều kim đồng hồ; Q là hình chiếu của M (mép đĩa) lên Ox nằm ngang qua tâm (chiều dương sang phải). Lúc ${m('t=0')}, M ở điểm <b>thấp nhất</b>.<br><b>a)</b> tần số góc; ${ph} (với ${m('-\\pi\\lt\\varphi\\le\\pi')})<br><b>b)</b> phương trình dao động của Q<br><b>c)</b> li độ của Q lúc ${m('t=\\frac13')} s`, o: [s1('a1'), s1('a2'), PTo('b'), 'c'] },
    nhap(9),
  ]],
  dap: [
    gr(`D1·1: a<sub>1</sub>) 8 cm · a<sub>2</sub>) π/6 rad · b<sub>1</sub>) 1 s · b<sub>2</sub>) 1 Hz · c) −6,93 cm &nbsp;|&nbsp; D1·2: a<sub>1</sub>) π rad/s · a<sub>2</sub>) 2 s · b) 3,54 cm · c) −3,54 cm &nbsp;|&nbsp; D2·1: a) 4 cm · b) π rad · c) 0 &nbsp;|&nbsp; D2·2: a) ${nw('x = 10cos(4πt − 5π/6) cm')} · b) −8,66 cm · c) 5 cm &nbsp;|&nbsp; D3·1: a<sub>1</sub>) 5 cm · a<sub>2</sub>) 2 s · b) π rad/s · c) 0 · d) ${nw('x = 5cos(πt) cm')} &nbsp;|&nbsp; D3·2: a<sub>1</sub>) 3 cm · a<sub>2</sub>) 0,4 s · b) 5π rad/s · c) π/2 · d) ${nw('x = 3cos(5πt + π/2) cm')}`),
    gr(`D4·1: a<sub>1</sub>) 5 cm · a<sub>2</sub>) 0,5 s · b) ${nw('x = 5cos(4πt) cm')} · c) −2,5 cm &nbsp;|&nbsp; D4·2: a<sub>1</sub>) 6 cm · a<sub>2</sub>) π rad/s · b) ${nw('x = 6cos(πt + π) cm')} · c) 3 cm &nbsp;|&nbsp; D5·1: a) 4π rad/s · b) ${nw('x = 10cos(4πt) cm')} · c) 5 cm &nbsp;|&nbsp; D5·2: a<sub>1</sub>) π rad/s · a<sub>2</sub>) −π/2 · b) ${nw('x = 8cos(πt − π/2) cm')} · c) 6,93 cm`),
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 2], kq: [[1, 2, 3], [4, 5]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'dao động cơ 1·4 · tuần hoàn 2·1 · đồ thị x–t 2·2 · phương trình 3·1 · chuyển động tròn đều 3·2 · bẫy 4·1 · bài toán mẫu 5·2 · dạng 1–3 → 6·1 · dạng 4–5 → 7·1',
  out: process.argv[2],
});
