// Ruột tập VL10 – Bài 12 · Chuyển động ném (lesson id 57). Quyển Chương 2 lớp 10 (Động học): bài 4 = tr. 1–12, bài 12 = tr. 97–108.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l10-bai12.mjs (toàn bộ SVG tự vẽ, quỹ đạo vẽ theo số liệu đề). Nội dung theo bài web (book/cache/57.json, tải từ DB 13/11/2026):
// mục tiêu, dự đoán hai gói hàng, II.1–II.4 ném ngang, hai thí nghiệm, ba bẫy, bài toán mẫu bờ kè, VI ném xiên (+ bài mẫu cú sút),
// Trả bài 6 câu, tự kiểm tra 6 câu, thử thách 4 mức, 6 dạng bài tập mẫu.
// Đáp số Bài tương tự (tuongTu.dap) tính bằng Python 13/11/2026; Bài tương tự giải vào vở (vo: true), mỗi dạng 2 bài.
// Chạy: node scripts/ruot-tap/l10-bai12.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl10-bai12.pdf
//       node scripts/ruot-tap/l10-bai12.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l10-bai12/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL10b12 as H } from './hinh-l10-bai12.mjs';

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
  const out = resolve(HERE, 'out/hinh-l10-bai12'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 12, lid: 57, ten: 'CHUYỂN ĐỘNG NÉM', lop: 10, baiDau: 4, sub: 'Vật lí 10 · Chương 2: Động học' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
// ô cho công thức có phân số/căn: cao 9 mm (checklist HS ảo: phân số cao ≥ 9 mm)
const ob = (w = 18) => `<span style="display:inline-block;width:${w}mm;height:9mm;border:.3mm solid var(--navy);border-radius:.6mm;background:#fff;vertical-align:middle;margin:.3mm .5mm"></span>`;
const g98 = nw(m('g=9{,}8\\ \\mathrm{m/s^2}')), g10 = nw(m('g=10\\ \\mathrm{m/s^2}'));
const v0 = m('v_0'), al = m('\\alpha'), vv0 = m('\\vec v_0');
const ms = (s) => nw(m(`${s}\\ \\mathrm{m/s}`)), mm = (s) => nw(m(`${s}\\ \\mathrm{m}`)), deg = (s) => nw(m(`${s}^\\circ`));

// Bài tương tự (khung xếp .tt dọc): ô đáp số đặt cuối dòng của ý (giống l10-bai23), xếp 1 cột.
const ttCss = '<style>.bt .ans .fill{height:6.5mm}.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';

const p1 = `${ttCss}<section class="page">
${head('BÀI 12 · CHUYỂN ĐỘNG NÉM', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft two" style="row-gap:0;padding:1.2mm 3mm">
${dong(`${ck}Tách <b>ném ngang</b> thành hai chuyển động`)}
${dong(`${ck}Viết <b>quỹ đạo</b>, gọi tên dạng đường đi`)}
${dong(`${ck}Tính <b>thời gian bay, tầm xa, vận tốc</b>`)}
${dong(`${ck}<b>Ném xiên</b>: tầm cao, thời gian bay, tầm xa`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card" style="padding:1.2mm 3mm">
<p style="margin:0 0 .6mm">Cùng độ cao, cùng lúc: gói 1 thả từ máy bay đang bay ngang, gói 2 thả từ trực thăng đứng yên (bỏ qua lực cản). Gói nào chạm đất trước?</p>
<div class="fig-side" style="${fs(48)}"><div>
${opt('A', 'Hai gói chạm đất cùng lúc')}
${opt('B', 'Gói 2, vì nó rơi thẳng đứng')}
${opt('C', 'Gói 1, vì nó đang bay nhanh')}
${opt('D', 'Máy bay càng nhanh, gói 1 càng lâu chạm đất')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 1)}</div>
${H.thaGoi()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f(12)} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Ném ngang: hai chuyển động thành phần', '1·4')}
<div class="card" style="padding:1.2mm 3mm">
<div>Ném ngang: ${vv0} theo phương ${f(25)}; sau đó vật chỉ chịu ${f(25)} (bỏ qua lực cản).</div>
<div>Gốc O tại điểm ném · Ox theo ${vv0} · Oy thẳng đứng hướng ${f(25)} &nbsp;<span class="hint">${m('g\\approx 9{,}8\\ \\mathrm{m/s^2}')}</span></div>
<table style="margin:.8mm 0"><tr><th style="width:24mm"></th><th style="width:17mm">Gia tốc</th><th style="width:30mm">Chuyển động</th><th>Vận tốc</th><th>Toạ độ</th></tr>
<tr><td>Ox (ngang)</td><td style="height:6.5mm">${m('a_x=')}</td><td></td><td>${m('v_x=')}</td><td>${m('x=')}</td></tr>
<tr><td>Oy (xuống)</td><td style="height:8.5mm">${m('a_y=')}</td><td></td><td>${m('v_y=')}</td><td>${m('y=')}</td></tr></table>
<div>Hai chuyển động thành phần ${f(25)} với nhau, chỉ chung thời gian ${m('t')}.</div></div>
${h3(5, 'Thí nghiệm: một bi bắn ngang, một bi thả rơi', '1·5')}
<div class="card fig-side" style="${fs(44)};padding:1.2mm 3mm"><div>
<div><b>Làm:</b> bắn ngang bi 1, cùng lúc thả bi 2; quay chậm.</div>
<div><b>Quan sát:</b> mỗi nhịp, hai bi luôn cùng ${f(25)}; chạm sàn ${f(25)}.</div>
<div><b>Rút ra:</b> phần ngang ${ck}có ${ck}không đổi phần rơi.</div>
<div>Bắn mạnh hơn: ${f(25)} đổi, ${f(25)} không.</div></div>
${H.haiBi()}</div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('QUỸ ĐẠO · THỜI GIAN BAY · TẦM XA · VẬN TỐC')}
${h3(1, 'II.2 · Quỹ đạo: khử t', '2·1')}
<div class="card fig-side" style="${fs(48)};padding:1.2mm 3mm"><div>
<div>Từ ${m('x=v_0t')} rút ${m('t=')}${ob(16)}, thế vào ${m('y=\\tfrac12 gt^2')}:</div>
<div style="margin:.4mm 0">${m('y=')}${ob(20)}${m('\\cdot x^2')}</div>
<div>${m('y')} tỉ lệ với ${f(12)} nên quỹ đạo là một phần ${f(25)}, đỉnh tại ${f(25)}.</div>
<div><b>Đọc hình:</b> sau những khoảng thời gian bằng nhau, các đoạn ngang ${f(25)}; các đoạn rơi tăng theo tỉ lệ ${nw(`1 : ${f(8)} : ${f(8)} : ${f(8)}`)}</div></div>
${H.quyDao()}</div>
${h3(2, 'II.3 · Thời gian bay và tầm xa', '2·2')}
<div class="card" style="padding:1.2mm 3mm">
<div>Vật chạm đất khi ${m('y=')} ${f(12)}: &nbsp; ${m('t=')}${ob(20)} &nbsp; ${m('L=v_0t=')}${ob(24)}</div>
<div>Thời gian bay chỉ phụ thuộc ${f(25)} và ${m('g')}; <b>không</b> phụ thuộc ${f(25)}. Tầm xa ${m('L')} phụ thuộc cả ${f(12)} lẫn ${f(12)}.</div></div>
${h3(3, 'Thí nghiệm đo: bắn bi ngang ở ba độ cao', '2·3')}
<table class="tbl-ct"><tr><th>${m('h\\ (\\mathrm m)')}</th><th>${m('L')} đo ${m('(\\mathrm m)')}</th><th>${m('t=\\sqrt{2h/g}\\ (\\mathrm s)')}</th><th>${m('v_0=L/t\\ (\\mathrm{m/s})')}</th></tr>
<tr><td>0,45</td><td>0,451</td><td></td><td></td></tr>
<tr><td>0,80</td><td>0,611</td><td>0,404</td><td></td></tr>
<tr><td>1,25</td><td>0,757</td><td></td><td></td></tr></table>
<div style="margin:.6mm 0 0">Lấy ${g98}. <b>Rút ra:</b> cùng súng, ${v0} ${f(25)} ở mọi độ cao; độ cao chỉ đổi ${f(25)} và ${f(25)}.</div>
${h3(4, 'II.4 · Vận tốc tại một điểm', '2·4')}
<div class="card fig-side" style="${fs(48)};padding:1.2mm 3mm"><div>
<div>${m('v_x=')} ${f(14)} (không đổi) &nbsp;·&nbsp; ${m('v_y=')} ${f(14)} (tăng đều)</div>
<div style="margin:.4mm 0">${m('v=')}${ob(30)}</div>
<div>Chạm đất: ${m('v_y=')}${ob(18)} ${m('\\Rightarrow v_{\\mathrm{cd}}=')}${ob(22)}</div>
<div>${m('\\tan\\alpha=')}${ob(14)}${m('=')}${ob(14)} &nbsp;(${al}: góc giữa ${m('\\vec v')} và phương ${f(14)})</div></div>
${H.vanToc()}</div>
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('BA CÁI BẪY · BÀI TOÁN MẪU NÉM NGANG')}
${h3(1, 'III · Ba cái bẫy hay sập', '3·1')}
<div class="card" style="padding:1mm 3mm">
<div class="trap">${ck}<span><b>“Ném nhanh hơn thì rơi lâu hơn.”</b> ${m('t=\\sqrt{2h/g}')} không chứa ${v0}: ${v0} chỉ đổi tầm xa.</span></div>
<div class="trap">${ck}<span><b>“Bay xa dần nên phương ngang nhanh dần.”</b> Ox không có lực: ${m('v_x=v_0')} suốt chuyển động.</span></div>
<div class="trap">${ck}<span><b>“Ném ngang là nhanh dần đều.”</b> Chỉ ${m('v_y=gt')} tăng đều; tốc độ ${m('v')} tăng không đều.</span></div></div>
${h3(2, 'V · Bài toán mẫu: hòn sỏi ném từ bờ kè', '3·2')}
<div class="card soft" style="padding:1.2mm 3mm">Từ bờ kè cao ${mm('h=20')} so với mặt nước, một người ném ngang hòn sỏi với ${ms('v_0=15')}. Bỏ qua sức cản không khí, lấy ${g98}.
<div><b>a)</b> Sau bao lâu sỏi chạm nước?</div><div><b>b)</b> Điểm chạm nước cách chân bờ kè bao xa theo phương ngang?</div><div><b>c)</b> Độ lớn vận tốc lúc vừa chạm nước và góc của vận tốc đó với phương ngang.</div></div>
${h3(3, 'Phân tích đề')}
<table><tr><th style="width:52mm">Câu trong đề</th><th>Dữ liệu → kiến thức</th></tr>
<tr><td>“ném ngang một hòn sỏi”</td><td>Tách hai phương: Ox thẳng đều, Oy rơi tự do</td></tr>
<tr><td style="height:5.5mm">“bờ kè cao 20 m”</td><td></td></tr>
<tr><td style="height:5.5mm">“${v0} = 15 m/s”</td><td></td></tr>
<tr><td style="height:5.5mm">“cách chân bờ kè bao xa”</td><td></td></tr>
<tr><td style="height:5.5mm">“góc của vận tốc với phương ngang”</td><td></td></tr></table>
${h3(4, 'Giải')}
<div class="fig-side" style="${fs(50)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl(`a) Thời gian rơi ${m('t')}:`, 2)}${wl(`b) Tầm xa ${m('L')}:`, 1)}${wl(`c) ${m('v_y')} lúc chạm nước:`, 1)}${wl(`Độ lớn ${m('v')}:`, 2)}${wl(`${m('\\tan\\alpha')} và ${al}:`, 2)}${wl(`Kiểm tra bằng ${m('v_{\\mathrm{cd}}')}:`, 1)}</div>${H.boKe()}</div>
${h3(5, 'Điền bước còn thiếu: bờ kè cao 45 m, ném ngang 20 m/s, g = 10 m/s²')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div class="ln"><b>Bước 1 (cho sẵn):</b> ${m('t=\\sqrt{2h/g}=3\\ \\mathrm s')}</div>
${wl(`Bước 2: ${m('L=')}`, 1)}${wl(`Bước 3: ${m('v_y=')} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ${m('v=')} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ${m('\\tan\\alpha=')} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ${m('\\alpha\\approx')}`, 1)}</div>
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('NÉM XIÊN: VẪN LÀ TÁCH HAI PHƯƠNG')}
${h3(1, 'VI.1 · Phân tích vận tốc ban đầu', '4·1')}
<div class="card fig-side" style="${fs(48)};padding:1.2mm 3mm"><div>
<div>Ném xiên: ${vv0} hợp với phương ngang góc ${al} (<b>góc ném</b>). Chọn Oy hướng <b>lên</b> ⇒ ${m('a_y=')} ${f(12)}</div>
<div style="margin:.4mm 0">${m('v_{0x}=')} ${f(22)} &nbsp; ${m('v_{0y}=')} ${f(22)}</div>
<div>Ox: ${m('v_x=')} ${f(20)} &nbsp; ${m('x=')} ${f(22)}</div>
<div>Oy: ${m('v_y=')} ${f(20)} &nbsp; ${m('y=')}${ob(26)}</div>
<div>Oy: lên ${f(25)} dần, tới đỉnh, rồi xuống ${f(25)} dần.</div></div>
${H.nemXien()}</div>
${h3(2, 'VI.2 · Tầm cao, thời gian bay, tầm xa (ném từ mặt đất)', '4·2')}
<div class="card" style="padding:1.2mm 3mm">
<div>Đỉnh: ${f(12)} ${m('=0')} ⇒ ${m('t_{\\text{lên}}=')}${ob(18)} ${m('H=')}${ob(22)}</div>
<div>Chạm đất: ${m('y=')} ${f(10)} ⇒ ${m('t=')}${ob(16)}${m('=')} ${f(10)}${m('\\,t_{\\text{lên}}')} · ${m('L=v_{0x}t=')}${ob(24)}</div>
<div class="fig-side" style="grid-template-columns:1fr 58mm;margin-top:.8mm;align-items:center"><table class="tbl-ct"><tr><th>Góc ${al}</th><th>${m('H\\ (\\mathrm m)')}</th><th>${m('L\\ (\\mathrm m)')}</th></tr>
<tr><td style="height:5.6mm">${deg(30)}</td><td></td><td></td></tr><tr><td style="height:5.6mm">${deg(45)}</td><td></td><td></td></tr><tr><td style="height:5.6mm">${deg(60)}</td><td></td><td></td></tr></table>
<div>Cùng ${ms('v_0=10')}, ${g10}. <span class="hint">(${m('2\\sin\\alpha\\cos\\alpha=\\sin2\\alpha')}, Toán 11)</span><br><b>Rút ra:</b> ${m('L')} lớn nhất khi ${nw(`${al} = ${f(12)}`)}; hai góc ${f(25)} nhau cho cùng ${m('L')}.</div></div></div>
${h3(3, 'Bẫy: “lên tới đỉnh thì vật dừng lại”', '4·3')}
<div class="card" style="padding:1mm 3mm"><div class="trap">${ck}<span>Ở đỉnh ${m('v_y=0')} nhưng ${m('v=')} ${f(20)}, hướng ${f(22)}; gia tốc vẫn là ${f(12)}.</span></div></div>
${h3(4, 'Bài toán mẫu ném xiên: cú sút bóng', '4·4')}
<div class="card soft" style="padding:1.2mm 3mm">Cầu thủ sút bóng từ mặt sân với ${ms('v_0=20')}, hợp với phương ngang ${deg(30)}. Bỏ qua sức cản, lấy ${g10}.
<div><b>a)</b> bóng lên cao nhất bao nhiêu</div><div><b>b)</b> bóng bay trong bao lâu</div><div><b>c)</b> bóng rơi cách chỗ sút bao xa</div><div><b>d)</b> vận tốc ở điểm cao nhất</div></div>
<div class="fig-side" style="${fs(48)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl(`Tách: ${m('v_{0x}=')} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ${m('v_{0y}=')}`, 1)}${wl(`a) ${m('H')}:`, 1)}${wl(`b) ${m('t_{\\text{lên}}')}, ${m('t')}:`, 1)}${wl(`c) ${m('L')}:`, 1)}${wl(`d) ${m('v')} ở đỉnh:`, 1)}</div>${H.sutBong()}</div>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('TRẢ BÀI · TỰ KIỂM TRA · BÀI TẬP VỀ NHÀ · THỬ THÁCH')}
${h3(1, 'IV · Trả bài 6 câu', '5·1')}
${box(`${wl('1. Ném ngang là gì? Vật chịu lực nào?', 1)}${wl('2. Mỗi phương chuyển động thế nào? Công thức vận tốc, toạ độ.', 2)}${wl('3. Phương trình quỹ đạo; vì sao chỉ vẽ một phần parabol?', 2)}${wl('4. Thời gian bay, tầm xa. Thời gian bay phụ thuộc gì?', 2)}${wl('5. Vận tốc tại thời điểm t, vận tốc chạm đất, góc lệch.', 2)}${wl('6. Ném xiên khác ném ngang ở đâu? Viết H, t, L.', 2)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/6 câu · chưa thuộc: ${f(25)} ${nw(`→ đọc lại ô ${f(12)} Tập`)}</div>
${h3(2, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '5·2')}
${rkHai([1, 2, 3], [4, 5, 6])}
${K.btvn().replace('<i>1</i>', '<i>3</i>')}
${h3(4, 'Thử thách phân tầng', '5·4')}
<div class="fig-side" style="${fs(42)}">${box(wl(`${m('\\bigstar')} Ném ngang từ ${mm('h=80')}, ${g10}. Thời gian rơi?`, 1)
 + wl(`${m('\\bigstar\\bigstar')} Cũng bài đó với ${ms('v_0=25')}: tầm xa và vận tốc chạm đất?`, 2)
 + wl(`${m('\\bigstar\\bigstar')} Ném xiên từ mặt đất, ${ms('v_0=20')}, ${nw(`${al} = ${deg(45)}`)}, ${g10}: tính ${m('H')} và ${m('L')}.`, 2)
 + wl(`${m('\\bigstar\\bigstar\\bigstar')} Máy bay cứu trợ bay ngang ở ${mm('500')} với ${ms('100')}, ${g10}. Thả hàng khi còn cách đích bao xa theo phương ngang? Vì sao không thả ngay trên đích?`, 3))}${H.thaHang()}</div>
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Ném ngang: thời gian bay và tầm xa',
    de: `Máy bay cứu hộ bay ngang ở độ cao ${mm('490')}, vận tốc ${ms('60')}, thả gói hàng. Bỏ qua lực cản, ${g98}.<br><b>a)</b> sau bao lâu gói hàng chạm đất<br><b>b)</b> thả gói khi máy bay còn cách điểm cần rơi trúng bao xa (theo phương ngang)`,
    nd: `Tìm ${m('t')} từ phương ${f(25)} trước; ${m('t')} không phụ thuộc ${f(12)}`, a: ['a', 'b'], gi: 2, cot: 2 },
  { t: 'Dạng 2 · Dễ · Ném ngang: vận tốc chạm đất và góc',
    de: `Từ mép vách đá cao ${mm('78{,}4')}, ném ngang hòn đá với ${ms('v_0=30')}. Bỏ qua lực cản, ${g98}. Lúc chạm đất:<br><b>a)</b> độ lớn vận tốc<br><b>b)</b> góc giữa vectơ vận tốc và phương ngang`,
    nd: `${m('v_x=')} ${f(12)} không đổi · ${m('v_y=')} ${f(12)} lúc chạm · hai vectơ ${f(25)}`, a: ['a', 'b'], gi: 3, cot: 2 },
  { t: 'Dạng 3 · Trung bình · Bài ngược: biết tầm xa, tìm v<sub>0</sub>; vật cản',
    de: `Từ mép mái nhà cao ${mm('19{,}6')}, ném ngang hòn đá; đá chạm đất cách chân nhà ${mm('15')}. Bỏ qua lực cản, ${g98}.<br><b>a)</b> vận tốc ném ${v0}<br><b>b)</b> cây cao ${mm('10')} cách chân nhà ${mm('10')}: đá có bay qua ngọn cây không, cao hơn ngọn bao nhiêu`,
    nd: `${m('v_0=L/t')}; ở cây: ${m('t_1=x/v_0')}, độ cao còn lại ${m('h-\\tfrac12gt_1^2')}`, a: ['a', 'b'], gi: 4, fig: H.nhaCay(), cot: 2 },
  { t: 'Dạng 4 · Trung bình · Ném xiên từ mặt đất: H, t, L',
    de: `Nhảy xa: bật với ${ms('v_0=9{,}8')}, góc ${deg(30)}, tiếp đất cùng độ cao; bỏ qua lực cản, ${g98}.<br><b>a)</b> ${m('v_{0x}')} và ${m('v_{0y}')}<br><b>b)</b> thời gian lên tới đỉnh và tầm cao ${m('H')}<br><b>c)</b> thời gian bay và tầm xa ${m('L')}`,
    nd: `Đỉnh: ${f(12)} ${m('=0')} · cùng độ cao nên ${m('t=')} ${f(10)}${m('\\,t_{\\text{lên}}')}`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c<sub>1</sub>', 'c<sub>2</sub>'], gi: 3, cot: 6 },
  { t: 'Dạng 5 · Khó · Ném xiên từ độ cao: rơi thấp hơn chỗ ném',
    de: `Từ vách đá cao ${mm('22{,}05')} ném đá lên với ${ms('v_0=14{,}7')}, góc ${deg(30)}; bỏ qua lực cản, ${g98}.<br><b>a)</b> thời gian từ lúc ném đến lúc chạm đất<br><b>b)</b> tầm xa tính từ chân vách<br><b>c)</b> độ cao lớn nhất so với mặt đất<br><b>d)</b> độ lớn vận tốc khi chạm đất`,
    nd: `Oy lên, gốc ở chỗ ném: chạm đất khi ${m('y=')} ${f(14)}; bỏ nghiệm âm`, a: ['a', 'b', 'c', 'd'], gi: 4, fig: H.vachXien() },
  { t: 'Dạng 6 · Khó · Bài ngược: biết tầm xa, tìm góc ném',
    de: `Pháo bắn với ${ms('v_0=14')}, nòng nghiêng ${al}, đạn rơi về độ cao nòng; bỏ qua lực cản, ${g98}.<br><b>a)</b> góc nghiêng nòng để đạn rơi cách pháo ${mm('15')}<br><b>b)</b> thời gian bay ứng với từng góc<br><b>c)</b> tầm xa lớn nhất và góc đạt được`,
    nd: `${m('\\sin2\\alpha=gL/v_0^2')} cho hai góc ${f(25)} nhau`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c<sub>1</sub>', 'c<sub>2</sub>'], gi: 3, cot: 6 },
];

// Bài tương tự: mỗi dạng 2 bài, đáp số tính bằng Python (math, radian), làm tròn 3 chữ số có nghĩa. Giải vào vở (thầy chốt 10/11):
// 1 cột; ô đáp số 25 mm đặt cuối đúng dòng của ý, nhãn khớp a) b) c)… (a<sub>1</sub>, a<sub>2</sub> khi ý có 2 kết quả).
const oY = (s, o, w = 25) => s.split('<br>').map((p) => {
  const y = p.match(/^<b>([a-d])\)<\/b>/);
  if (!y) return `<div>${p}</div>`;
  const ls = o.filter((l) => l[0] === y[1]);
  return `<div class="yo"><span>${p}</span><span class="oo">${ls.map((l) => `<span class="nw"><b>${l})</b>${f(w)}</span>`).join('')}</span></div>`;
}).join('');
const ttDe = (b) => b.fig ? `<div class="fig-side" style="grid-template-columns:1fr ${b.fw}mm">${`<div>${oY(b.de, b.o, b.ow)}</div>`}${b.fig}</div>` : oY(b.de, b.o, b.ow);
const vaoVo = (ds) => ds.map((b) => (b.o ? { t: b.t, de: ttDe(b), k: 0 } : b));
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–3 · NÉM NGANG', 'DẠNG 4–6 · NÉM XIÊN'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Từ đỉnh tháp cao ${mm('45')}, ném ngang một vật với ${ms('12')}. Bỏ qua lực cản, ${g10}.<br><b>a)</b> thời gian rơi<br><b>b)</b> tầm xa<br><b>c)</b> ném với ${ms('24')} thì thời gian rơi bằng bao nhiêu`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 1 · Bài 2', de: `Máy bay bay ngang ở độ cao ${mm('720')} với ${ms('50')} thả một thùng hàng. Bỏ qua lực cản, ${g10}.<br><b>a)</b> thời gian thùng rơi<br><b>b)</b> thả khi máy bay còn cách đích bao xa theo phương ngang`, o: ['a', 'b'] },
    { t: 'Dạng 2 · Bài 1', de: `Ném ngang hòn bi từ độ cao ${mm('20')} với ${ms('15')}. Bỏ qua lực cản, ${g10}. Lúc chạm đất:<br><b>a)</b> thành phần ${m('v_y')}<br><b>b)</b> độ lớn vận tốc<br><b>c)</b> góc giữa vận tốc và phương ngang`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 2 · Bài 2', de: `Viên bi lăn ra khỏi mép bàn cao ${mm('1{,}25')} với vận tốc ngang ${ms('2{,}0')}. Bỏ qua lực cản, ${g10}.<br><b>a)</b> thời gian rơi<br><b>b)</b> độ lớn vận tốc lúc chạm sàn<br><b>c)</b> góc giữa vận tốc lúc chạm sàn và phương ngang`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 3 · Bài 1', de: `Ném ngang một quả bóng từ độ cao ${mm('5{,}0')}; bóng chạm đất cách điểm ném ${mm('8{,}0')} theo phương ngang. Bỏ qua lực cản, ${g10}.<br><b>a)</b> thời gian bay<br><b>b)</b> vận tốc ném<br><b>c)</b> vận tốc ném để bóng rơi cách ${mm('12')}`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 3 · Bài 2', de: `Từ ban công cao ${mm('11{,}25')}, ném ngang quả bóng; bóng chạm đất cách chân nhà ${mm('9{,}0')}. Cách chân nhà ${mm('6{,}0')} có bức tường cao ${mm('5{,}0')}. Bỏ qua lực cản, ${g10}.<br><b>a)</b> vận tốc ném<br><b>b)</b> độ cao của bóng khi tới chỗ tường; bóng có bay qua tường không`, fig: H.ttTuong(), fw: 44, o: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>'] },
  ], [
    { t: 'Dạng 4 · Bài 1', de: `Ném xiên từ mặt đất với ${ms('10')}, góc ${deg(60)}, vật rơi về cùng độ cao; bỏ qua lực cản, ${g10}.<br><b>a)</b> ${m('v_{0x}')} và ${m('v_{0y}')}<br><b>b)</b> tầm cao ${m('H')}<br><b>c)</b> thời gian bay và tầm xa`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'] },
    { t: 'Dạng 4 · Bài 2', de: `Phát bóng từ mặt sân với ${ms('24')}, góc ${deg(30)}, bóng rơi xuống mặt sân; bỏ qua lực cản, ${g10}.<br><b>a)</b> thời gian lên tới đỉnh và tầm cao<br><b>b)</b> thời gian bay và tầm xa<br><b>c)</b> tốc độ của bóng ở điểm cao nhất`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'] },
    { t: 'Dạng 5 · Bài 1', de: `Từ độ cao ${mm('15')} ném vật lên với ${ms('10')}, góc ${deg(30)}; bỏ qua lực cản, ${g10}.<br><b>a)</b> thời gian bay · <b>b)</b> tầm xa theo phương ngang<br><b>c)</b> độ cao lớn nhất so với mặt đất<br><b>d)</b> tốc độ khi chạm đất`, o: ['a', 'b', 'c', 'd'] },
    { t: 'Dạng 5 · Bài 2', de: `Từ mái nhà cao ${mm('25')} ném bóng lên với ${ms('20')}, góc ${deg(30)}; bỏ qua lực cản, ${g10}.<br><b>a)</b> thời gian bay · <b>b)</b> tầm xa tính từ chân nhà<br><b>c)</b> độ cao lớn nhất so với mặt đất<br><b>d)</b> tốc độ khi chạm đất`, fig: H.ttMai(), fw: 44, o: ['a', 'b', 'c', 'd'] },
    { t: 'Dạng 6 · Bài 1', de: `Vòi nước ở mặt đất phun với ${ms('20')}, nước rơi về cùng độ cao vòi; bỏ qua lực cản, ${g10}.<br><b>a)</b> góc nghiêng vòi để nước rơi cách vòi ${mm('20')}<br><b>b)</b> thời gian bay ứng với từng góc<br><b>c)</b> tầm xa lớn nhất của vòi`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'] },
    { t: 'Dạng 6 · Bài 2', de: `Đá bóng từ mặt sân với ${ms('10')}, bóng rơi cách chỗ đá ${nw(`${m('5\\sqrt3\\ \\mathrm m')} (≈ 8,66 m)`)}; bỏ qua lực cản, ${g10}.<br><b>a)</b> các góc đá có thể · <b>b)</b> tầm cao ứng với từng góc<br><b>c)</b> có đá được tới ${mm('12')} với tốc độ này không`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'] },
  ]],
  dap: [
    `D1·1: a) 3,0 s · b) 36 m · c) 3,0 s &nbsp;|&nbsp; D1·2: a) 12 s · b) 600 m &nbsp;|&nbsp; D2·1: a) 20 m/s · b) 25 m/s · c) 53,1° &nbsp;|&nbsp; D2·2: a) 0,50 s · b) 5,39 m/s · c) 68,2° &nbsp;|&nbsp; D3·1: a) 1,0 s · b) 8,0 m/s · c) 12 m/s &nbsp;|&nbsp; D3·2: a) 6,0 m/s · b<sub>1</sub>) 6,25 m · b<sub>2</sub>) có, cao hơn tường 1,25 m`,
    `D4·1: a<sub>1</sub>) 5,0 m/s · a<sub>2</sub>) 8,66 m/s · b) 3,75 m · c<sub>1</sub>) 1,73 s · c<sub>2</sub>) 8,66 m &nbsp;|&nbsp; D4·2: a<sub>1</sub>) 1,2 s · a<sub>2</sub>) 7,2 m · b<sub>1</sub>) 2,4 s · b<sub>2</sub>) 49,9 m · c) 20,8 m/s &nbsp;|&nbsp; D5·1: a) 2,30 s · b) 19,9 m · c) 16,25 m · d) 20 m/s &nbsp;|&nbsp; D5·2: a) 3,45 s · b) 59,7 m · c) 30 m · d) 30 m/s &nbsp;|&nbsp; D6·1: a<sub>1</sub>) 15° · a<sub>2</sub>) 75° · b<sub>1</sub>) 1,04 s · b<sub>2</sub>) 3,86 s · c) 40 m &nbsp;|&nbsp; D6·2: a<sub>1</sub>) 30° · a<sub>2</sub>) 60° · b<sub>1</sub>) 1,25 m · b<sub>2</sub>) 3,75 m · c) không (tối đa 10 m)`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 3], kq: [[1, 2, 3], [4, 5, 6]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'ném ngang 1·4 · quỹ đạo 2·1 · t, L 2·2 · vận tốc 2·4 · bẫy 3·1 · bờ kè 3·2 · ném xiên 4·1 · H, t, L 4·2 · cú sút 4·4 · dạng 1–3 → 6·1 · dạng 4–6 → 7·1',
  out: process.argv[2],
});
