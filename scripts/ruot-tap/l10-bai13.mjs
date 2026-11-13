// Ruột tập VL10 – Bài 13 · Tổng hợp và phân tích lực. Cân bằng lực (lesson id 58). Quyển Chương 3 lớp 10: bài 13 = tr. 1–12.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l10-bai13.mjs (SVG tự vẽ + 1 ảnh thật CC0 hai ngựa kéo cày từ book/assets/anh-that). Nội dung theo bài web
// (book/cache/58.json, tải từ DB 13/11/2026): mục tiêu, dự đoán hai dây kéo xe, II.1–II.6, hai thí nghiệm (vòng nhẫn, mặt nghiêng),
// ba bẫy, Trả bài 7 câu, hai bài toán mẫu (xe trượt, đèn treo), thử thách, 6 dạng bài tập mẫu.
// Đáp số Bài tương tự (tuongTu.dap) và các dạng tính bằng Python 13/11/2026 (math.cos/sin/acos theo radian), làm tròn 3 chữ số có nghĩa.
// Chạy: node scripts/ruot-tap/l10-bai13.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl10-bai13.pdf
//       node scripts/ruot-tap/l10-bai13.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l10-bai13/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL10b13 as H } from './hinh-l10-bai13.mjs';

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
  const out = resolve(HERE, 'out/hinh-l10-bai13'); mkdirSync(out, { recursive: true });
  const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true, args: ['--allow-file-access-from-files'] });
  const pg = await b.newPage();
  const katexCss = pathToFileURL(BOOK + 'node_modules/katex/dist/katex.min.css').href;
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

const K = khoiTao({ bai: 13, lid: 58, ten: 'TỔNG HỢP VÀ PHÂN TÍCH LỰC · CÂN BẰNG LỰC', lop: 10, baiDau: 13, sub: 'Vật lí 10 · Chương 3: Động lực học' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const g10 = nw(m('g=10\\ \\mathrm{m/s^2}'));
const vF = (i = '') => m(`\\vec F${i ? `_${i}` : ''}`), al = m('\\alpha');

// Bài tương tự giải vào vở (thầy chốt 10/11): ô đáp số đặt cuối đúng dòng của ý (như bài 23); ttHaiCot giữ kiểu dòng ý–ô của bài 23.
const ttHaiCot = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';
const p1 = `${ttHaiCot}<section class="page">
${head('BÀI 13 · TỔNG HỢP VÀ PHÂN TÍCH LỰC · CÂN BẰNG LỰC', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Tổng hợp hai lực đồng quy bằng <b>quy tắc hình bình hành</b>`)}
${dong(`${ck}Tìm hợp lực của hai lực <b>song song cùng chiều</b>: độ lớn và vị trí giá`)}
${dong(`${ck}<b>Phân tích</b> một lực thành hai thành phần vuông góc`)}
${dong(`${ck}Dùng <b>điều kiện cân bằng</b> để tìm lực căng dây`)}
${dong(`${ck}Phân biệt hai lực cân bằng với cặp lực – phản lực`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Hai bạn kéo xe trên sân băng bằng hai dây. Hợp lực lên xe là bao nhiêu?</p>
<div class="fig-side" style="${fs(46)}"><div>
${opt('A', 'Luôn bằng 200 N, vì 100 + 100')}
${opt('B', 'Luôn bằng 100 N, vì xe chỉ có một chiều chạy')}
${opt('C', 'Từ 0 đến 200 N, tuỳ góc giữa hai dây')}
${opt('D', 'Luôn bằng 0, vì hai lực kéo triệt tiêu nhau')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 1)}</div>
${H.haiDay(`Nhìn từ trên xuống. Mỗi bạn kéo 100 N; hai dây hợp góc ${al}.`)}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Tổng hợp lực', '1·4')}
<div class="card" style="padding:1.2mm 3mm">
<div><b>Tổng hợp lực:</b> thay các lực tác dụng ${f(25)} lên một vật bằng ${f(14)} lực có tác dụng ${f(25)}.</div>
<div>Lực thay thế gọi là ${f(25)}; các lực bị thay gọi là ${f(30)}.</div>
<div>Hệ thức: ${m('\\vec F=')} ${f(30)} &nbsp;(cộng ${f(25)}, không cộng số).</div></div>
${h3(5, 'Thí nghiệm: ba lực kế và vòng nhẫn', '1·5')}
<div class="card fig-side" style="${fs(40)};padding:1.2mm 3mm"><div>
<div><b>Làm:</b> ba dây buộc vào vòng nhẫn, mỗi dây móc một lực kế. Kéo lực kế 1, 2 hợp góc ${al}, kéo lực kế 3 cho vòng nằm yên; đọc ba số, vạch ba hướng dây.</div>
<div style="margin-top:.6mm"><b>Quan sát:</b> vẽ ${vF(1)}, ${vF(2)} chung gốc theo tỉ lệ, dựng hình có hai cạnh kề là hai vectơ ấy: đường chéo từ gốc có độ lớn bằng số chỉ lực kế ${f(12)} và hướng ${f(25)} với dây thứ ba.</div>
<div style="margin-top:.6mm"><b>Rút ra:</b> quy tắc ${f(30)} đúng với lực.</div></div>
${H.vongNhan()}</div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('HAI LỰC CÙNG PHƯƠNG · QUY TẮC HÌNH BÌNH HÀNH')}
${h3(1, 'II.2 · Hai lực cùng phương', '2·1')}
<div class="card fig-side" style="${fs(44)};padding:1.2mm 3mm"><div>
<div><b>Cùng chiều:</b> ${m('F=')} ${f(25)}; hợp lực ${f(25)} chiều hai lực.</div>
<div style="margin-top:.6mm"><b>Ngược chiều:</b> ${m('F=')} ${f(25)}; hợp lực cùng chiều lực ${f(25)}.</div>
<div style="margin-top:1mm"><b>Kéo co:</b> đội trái kéo ${nw('800 N')}, đội phải kéo ${nw('750 N')}. Hợp lực lên dây ${nw(`${f(14)}&nbsp;N`)}, hướng về đội ${f(14)}.</div></div>
${H.ngua()}</div>
${h3(2, 'II.3 · Hai lực đồng quy: quy tắc hình bình hành', '2·2')}
<div class="card fig-side" style="${fs(44)};padding:1.2mm 3mm"><div>
<div>Hai lực đồng quy có ${f(14)} cắt nhau tại một điểm. Trượt về điểm đó, vẽ ${vF(1)}, ${vF(2)} chung gốc.</div>
<div style="margin-top:.6mm">Dựng hình bình hành nhận hai vectơ làm cạnh: ${f(25)} xuất phát từ gốc là hợp lực ${vF()}.</div>
<div style="margin-top:1mm">${m('F^2=')} ${f(48)}</div>
<div style="margin-top:.6mm">${al} là góc giữa ${f(45)}.</div>
<div style="margin-top:.6mm"><b>Nhắc:</b> ${m('\\cos 0^\\circ=')} ${f(12)} ${m('\\cos 60^\\circ=')} ${f(12)} ${m('\\cos 90^\\circ=')} ${f(12)}</div>
<div>${m('\\cos 120^\\circ=')} ${f(12)} ${m('\\cos 180^\\circ=')} ${f(12)}</div></div>
${H.hbh()}</div>
<table style="margin-top:.6mm"><tr><th style="width:52mm">Trường hợp đặc biệt</th><th>Hợp lực ${m('F')}</th></tr>
<tr><td>${m('\\alpha=0^\\circ')} (cùng chiều)</td><td></td></tr>
<tr><td>${m('\\alpha=180^\\circ')} (ngược chiều)</td><td></td></tr>
<tr><td>${m('\\alpha=90^\\circ')} (vuông góc)</td><td></td></tr>
<tr><td>${m('F_1=F_2')}, góc ${al} bất kì</td><td></td></tr></table>
<div style="margin-top:.6mm">Góc ${al} càng mở thì hợp lực càng ${f(25)}.</div>
${h3(3, `Bảng số liệu: vòng nhẫn với ${m('F_1=3{,}0\\ \\mathrm N')}, ${m('F_2=4{,}0\\ \\mathrm N')}`, '2·3')}
<div class="card" style="padding:1mm 3mm">
<table class="tbl-ct"><tr><th>Góc ${al}</th><th>${m('0^\\circ')}</th><th>${m('60^\\circ')}</th><th>${m('90^\\circ')}</th><th>${m('120^\\circ')}</th><th>${m('180^\\circ')}</th></tr>
<tr><td>${m('F')} tính (N)</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>${m('F_3')} đọc (N)</td><td>6,9</td><td>6,1</td><td>5,1</td><td>3,7</td><td>1,1</td></tr></table>
<div style="margin-top:.6mm">Sai số lực kế ${nw('± 0,1 N')}; lệch lớn nhất ${nw(`${f(12)}&nbsp;N`)}. Quy tắc có sai không? Vì sao?</div>${lines(1)}</div>
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('LỰC SONG SONG · PHÂN TÍCH LỰC · CÂN BẰNG')}
${h3(1, 'II.4 · Hai lực song song cùng chiều', '3·1')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div>${m('F=')} ${f(25)}, hợp lực ${f(20)} chiều hai lực; giá hợp lực nằm ${f(20)} hai giá, gần lực ${f(20)} hơn.</div>
<div style="margin-top:.6mm">${m('\\dfrac{F_1}{F_2}=')} <span class="fill" style="min-width:16mm;height:9mm"></span> &nbsp;(tỉ lệ ${f(25)})</div>
<div style="margin-top:.6mm"><b>Đòn gánh:</b> vai đỡ ${nw(`${f(12)}&nbsp;N`)}; ${nw(`${m('d_1=')} ${f(12)}&nbsp;m`)} (từ thùng 30 N), ${nw(`${m('d_2=')} ${f(12)}&nbsp;m`)}</div>
${wl('Cách tính:', 1)}</div>
${H.donGanh()}</div>
${h3(2, 'II.5 · Phân tích lực', '3·2')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div>Phân tích lực là việc ${f(25)} với tổng hợp lực: thay một lực bằng ${f(14)} lực thành phần có tác dụng giống hệt.</div>
<div style="margin-top:.6mm">Chọn hai trục vuông góc ${m('Ox')}, ${m('Oy')}: ${nw(`${m('F_x=')} ${f(20)}`)} &nbsp; ${nw(`${m('F_y=')} ${f(20)}`)}</div>
<div style="margin-top:.6mm">${al} là góc giữa ${f(25)} và ${f(25)}.</div>
<div style="margin-top:.6mm">Thành phần <b>kề</b> góc dùng ${f(16)}; thành phần <b>đối</b> góc dùng ${f(16)}.</div></div>
${H.keo()}</div>
${h3(3, 'Thí nghiệm: vật trên mặt phẳng nghiêng', '3·3')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div><b>Làm:</b> quả nặng ${nw(`${m('P=2{,}0\\ \\mathrm N')}`)} trên ván trơn nghiêng góc ${al}; lực kế song song ván giữ vật đứng yên.</div>
<table class="tbl-ct" style="margin-top:.6mm"><tr><th>${al}</th><th>${m('15^\\circ')}</th><th>${m('30^\\circ')}</th><th>${m('45^\\circ')}</th></tr>
<tr><td>Lực kế (N)</td><td>0,5</td><td>1,0</td><td>1,4</td></tr>
<tr><td>${m('P\\sin\\alpha')} (N)</td><td></td><td></td><td></td></tr></table>
<div style="margin-top:.6mm"><b>Rút ra:</b> lực kế ${m('=P_x=P')} ${f(16)}; thành phần ép vào ván ${m('P_y=P')} ${f(16)}.</div></div>
${H.docTN()}</div>
${h3(4, 'II.6 · Cân bằng lực', '3·4')}
<div class="card" style="padding:1.2mm 3mm">
<div>Chất điểm cân bằng (${f(25)} hoặc ${f(30)}) khi tổng các lực ${m('\\vec F_1+\\vec F_2+\\dots=')} ${f(12)}.</div>
<div style="margin-top:.6mm"><b>Ba lực:</b> hợp của hai lực ${f(25)} và ${f(25)} lực thứ ba; nối đuôi nhau thì tạo thành ${f(25)} khép kín.</div>
</div>
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('BA CÁI BẪY · TRẢ BÀI · TỰ KIỂM TRA')}
${h3(1, 'III · Ba cái bẫy hay sập', '4·1')}
<div class="card" style="padding:1mm 3mm">
<div class="trap">${ck}<span><b>“Hợp lực luôn bằng tổng hai lực.”</b> Phải cộng vectơ: ${nw(`${f(16)} ${m('\\le F\\le')} ${f(16)}`)}; hợp lực có thể nhỏ hơn cả hai lực thành phần.</span></div>
<div class="trap">${ck}<span><b>“Hai lực bằng nhau, ngược chiều là lực – phản lực.”</b> Sách nằm yên trên bàn: ${m('\\vec P')} và ${m('\\vec N')} cùng đặt lên ${f(20)} nên là hai lực ${f(25)}.</span></div>
<table style="margin:.4mm 0 .8mm"><tr><th style="width:30mm"></th><th>Hai lực cân bằng</th><th>Lực – phản lực</th></tr>
<tr><td>Đặt lên</td><td></td><td></td></tr><tr><td>Triệt tiêu nhau?</td><td></td><td></td></tr></table>
<div class="trap">${ck}<span><b>“Thành phần dọc dốc là ${m('P\\cos\\alpha')}.”</b> Trên dốc nghiêng ${al}: ${nw(`${m('P_x=')} ${f(16)}`)} (dọc dốc), ${nw(`${m('P_y=')} ${f(16)}`)} (ép vào dốc). Mẹo kiểm: dốc gần nằm ngang (${m('\\alpha\\to 0')}) thì ${m('P_x\\to')} ${f(12)}.</span></div></div>
${h3(2, 'IV · Trả bài 7 câu', '4·2')}
${box(`${tb('1. Tổng hợp lực là gì? Hợp lực, lực thành phần là gì?')}${lines(1)}
${tb('2. Công thức hợp lực hai lực đồng quy và bốn trường hợp đặc biệt.')}${lines(3)}
${tb(`3. Hợp lực của hai lực ${m('F_1')}, ${m('F_2')} nằm trong khoảng nào?`)}${lines(1)}
${tb(`4. Phân tích lực là gì? Viết ${m('F_x')}, ${m('F_y')}; ${al} là góc nào?`)}${lines(2)}
${tb('5. Điều kiện cân bằng của chất điểm? Với ba lực thì sao?')}${lines(1)}
${tb('6. Hai lực cân bằng khác cặp lực – phản lực ở đâu?')}${lines(1)}
${tb('7. Hợp lực hai lực song song cùng chiều: độ lớn, vị trí giá?')}${lines(1)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/7 câu · chưa thuộc: ${f(25)} ${nw(`→ đọc lại ô ${f(12)} Tập`)}</div>
${h3(3, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '4·3')}
${rkHai([1, 2, 3], [4, 5, 6])}
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TẬP VỀ NHÀ · BÀI TOÁN MẪU · THỬ THÁCH')}
${K.btvn()}
${h3(2, 'V · Bài toán mẫu 1: hai bạn kéo xe trượt', '5·2')}
<div class="card soft" style="padding:1.2mm 3mm">Trên sân băng, dây bạn A kéo xe ${nw('30 N')} về phía đông, dây bạn B kéo ${nw('40 N')} về phía bắc. Bỏ qua ma sát. Tìm độ lớn và hướng của hợp lực lên xe.</div>
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl(`Góc giữa hai lực, độ lớn ${m('F')}:`, 2)}${wl(`Hướng: góc ${m('\\theta')} giữa ${vF()} và hướng đông (${m('\\cos\\theta=F_1/F')}):`, 2)}${wl(`Kiểm tra: ${m('F')} có nằm giữa ${m('\\lvert F_1-F_2\\rvert')} và ${m('F_1+F_2')}?`, 1)}
<div class="ln"><b>Điền bước:</b> mỗi bạn kéo ${nw('50 N')}, hai dây hợp ${nw(`${m('120^\\circ')}.`)}</div><div class="ln">${nw(`${m('\\alpha/2=')} ${f(12)}`)} &nbsp; ${nw(`${m('\\cos(\\alpha/2)=')} ${f(12)}`)} &nbsp; ${nw(`${m('F=')} ${f(14)}&nbsp;N`)}</div></div>
${h3(3, 'Bài toán mẫu 2: chiếc đèn treo bằng hai dây', '5·3')}
<div class="card soft" style="padding:1.2mm 3mm">Đèn ${nw('2,0 kg')} treo trần bằng hai dây đối xứng, hai dây hợp nhau góc ${m('60^\\circ')}; ${g10}. Tính lực căng mỗi dây.</div>
<div class="fig-side" style="${fs(40)}"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl(`Dữ kiện ngầm “đèn đứng yên” cho biết:`, 2)}${wl(`Hợp lực của ${m('T_1')}, ${m('T_2')} (dùng ${m('F=2T\\cos(\\alpha/2)')}):`, 1)}${wl(`Lực căng ${m('T')}:`, 3)}${wl(`Mở rộng góc giữa hai dây thành ${m('120^\\circ')}: ${m('T=')}`, 2)}</div>
${H.den()}</div>
${h3(4, 'Thử thách phân tầng', '5·4')}
${box(wl(`${m('\\bigstar')} Hai lực ${nw('6 N')} và ${nw('8 N')} vuông góc. Hợp lực?`, 2)
 + wl(`${m('\\bigstar\\bigstar')} Hai lực ${nw(m('F_1=F_2=12\\ \\mathrm N'))} có hợp lực ${nw('12 N')}. Góc giữa chúng?`, 2)
 + wl(`${m('\\bigstar\\bigstar\\bigstar')} Thùng ${nw('10 kg')} nằm yên trên dốc ${nw(m('37^\\circ'))} (${nw(m('\\sin 37^\\circ=0{,}6'))}, ${nw(m('\\cos 37^\\circ=0{,}8'))}, ${g10}). Lực ma sát giữ thùng và phản lực của dốc?`, 3))}
${foot(5)}</section>`;

// hình đặt cạnh đề (ý ngắn nằm bên trái) thay vì cạnh ô giải → mỗi dạng thấp hơn ~15 mm
const deH = (txt, fig, w = 38) => `<div class="fig-side" style="${fs(w)}"><div>${txt}</div>${fig('')}</div>`;
const dang = [
  { t: 'Dạng 1 · Dễ · Độ lớn hợp lực của hai lực đồng quy theo góc',
    de: `Hai lực đồng quy ${m('F_1=5{,}0\\ \\mathrm N')}, ${m('F_2=12\\ \\mathrm N')}. Hợp lực khi góc giữa chúng là:<br><b>a)</b> ${m('180^\\circ')}<br><b>b)</b> ${m('90^\\circ')}<br><b>c)</b> ${m('60^\\circ')}`,
    nd: `${m('F^2=')} ${f(45)} &nbsp;(${m('180^\\circ')}: trừ thẳng; ${m('90^\\circ')}: Pythagore)`, a: ['a', 'b', 'c'], gi: 3 },
  { t: 'Dạng 2 · Trung bình · Khoảng giá trị của hợp lực, tìm góc',
    de: `Hai lực đồng quy ${m('F_1=7{,}0\\ \\mathrm N')}, ${m('F_2=15\\ \\mathrm N')} tác dụng lên một chất điểm.<br><b>a)</b> hợp lực nhỏ nhất (a<sub>1</sub>), lớn nhất (a<sub>2</sub>) khi đổi góc<br><b>b)</b> hợp lực có thể bằng ${m('5{,}0\\ \\mathrm N')} (b<sub>1</sub>)? bằng ${m('12\\ \\mathrm N')} (b<sub>2</sub>)?<br><b>c)</b> hợp lực bằng ${m('20\\ \\mathrm N')}: góc giữa hai lực`,
    nd: `${f(16)} ${m('\\le F\\le')} ${f(16)}; biết ${m('F')} tìm góc: ${nw(`${m('\\cos\\alpha=')} ${f(36)}`)}`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], gi: 3, cot: 5 },
  { t: 'Dạng 3 · Trung bình · Phân tích lực kéo xiên',
    de: deH(`Dây kéo thùng trên sàn, hợp với phương ngang ${m('40^\\circ')}, ${m('F=45\\ \\mathrm N')}.<br><b>a)</b> ${m('F_x')} nằm ngang (a<sub>1</sub>), ${m('F_y')} thẳng đứng (a<sub>2</sub>)<br><b>b)</b> thành phần làm thùng tiến (b<sub>1</sub>), làm thùng bớt ép sàn (b<sub>2</sub>)<br><b>c)</b> dây chếch ${m('60^\\circ')}: ${m('F_x')}`, H.keoD3, 36),
    nd: `${al} đo từ phương ngang ⇒ ${nw(`${m('F_x=F')} ${f(14)}`)}, ${nw(`${m('F_y=F')} ${f(14)}`)}`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], gi: 3, cot: 5 },
  { t: 'Dạng 4 · Trung bình · Phân tích trọng lực trên mặt dốc',
    de: deH(`Thùng ${m('8{,}0\\ \\mathrm{kg}')} trên dốc nghiêng ${m('40^\\circ')}; ${g10}.<br><b>a)</b> trọng lượng ${m('P')}<br><b>b)</b> ${m('P_x')} dọc dốc (b<sub>1</sub>), ${m('P_y')} vuông góc dốc (b<sub>2</sub>)<br><b>c)</b> dốc còn nghiêng ${m('20^\\circ')}: ${m('P_x')}`, H.docD4, 32),
    nd: `góc giữa ${m('\\vec P')} và ${m('\\vec P_y')} bằng góc nghiêng ⇒ ${nw(`${m('P_x=P')} ${f(14)}`)}, ${nw(`${m('P_y=P')} ${f(14)}`)}`, a: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], gi: 3 },
  { t: 'Dạng 5 · Khó · Vật treo bằng hai dây: lực căng khi cân bằng',
    de: deH(`Vật ${m('3{,}0\\ \\mathrm{kg}')} treo vào vòng ${m('O')}; dây ${m('OA')} nằm ngang buộc tường, dây ${m('OB')} lệch ${m('30^\\circ')} so với phương thẳng đứng buộc trần; ${g10}.<br><b>a)</b> lực căng dây ${m('OB')}<br><b>b)</b> lực căng dây ${m('OA')}`, (c) => H.oab(c, 1.3), 32),
    nd: `chiếu lên ${m('Oy')}: ${nw(`${m('T_{OB}')} ${f(14)} ${m('=P')}`)}; chiếu lên ${m('Ox')}: ${nw(`${m('T_{OA}=T_{OB}')} ${f(14)}`)}`, a: ['a', 'b'], gi: 3, cot: 2 },
  { t: 'Dạng 6 · Khó · Dây võng: lực căng mỗi nhánh',
    de: deH(`Hai cột cùng độ cao cách nhau ${m('AB=6{,}0\\ \\mathrm m')}; treo đèn ${m('4{,}0\\ \\mathrm{kg}')} giữa dây thì dây võng ${m('h=0{,}50\\ \\mathrm m')}; ${g10}.<br><b>a)</b> góc ${m('\\theta')} giữa mỗi nhánh và phương ngang<br><b>b)</b> lực căng mỗi nhánh<br><b>c)</b> lực căng gấp mấy lần trọng lượng đèn`, (c) => H.vong(c, 1.3), 34),
    nd: `${nw(`${m('\\tan\\theta=')} ${f(16)}`)}; hai thành phần đứng đỡ đèn: ${nw(`${m('2T')} ${f(14)} ${m('=P')}`)}`, a: ['a', 'b', 'c'], gi: 3 },
];

// Bài tương tự: mỗi dạng 2 bài, giải vào vở; đáp số tính bằng Python 13/11/2026, 3 chữ số có nghĩa.
const oY = (s, o, w = 25) => s.split('<br>').map((p) => {
  const y = p.match(/^<b>([a-d])\)<\/b>/);
  if (!y) return `<div>${p}</div>`;
  const ls = o.filter((l) => l[0] === y[1]);
  return `<div class="yo"><span>${p}</span><span class="oo">${ls.map((l) => `<span class="nw"><b>${l})</b>${f(w)}</span>`).join('')}</span></div>`;
}).join('');
const ttDe = (b) => b.fig ? `<div class="fig-side" style="grid-template-columns:1fr ${b.fw}mm">${`<div>${oY(b.de, b.o, b.ow)}</div>`}${b.fig}</div>` : oY(b.de, b.o, b.ow);
const vaoVo = (ds) => ds.map((b) => (b.o ? { t: b.t, de: ttDe(b), k: 0 } : b));
const nhap = (n) => ({ t: '<span class="nhap-t">Nháp / chỗ em còn vướng</span>', de: lines(n), k: 0 });
const a1 = 'a<sub>1</sub>', a2 = 'a<sub>2</sub>';
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–3', 'DẠNG 4–6'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Hai lực đồng quy ${m('6{,}0\\ \\mathrm N')} và ${m('8{,}0\\ \\mathrm N')}. Hợp lực khi góc giữa hai lực là:<br><b>a)</b> ${m('0^\\circ')}<br><b>b)</b> ${m('180^\\circ')}<br><b>c)</b> ${m('90^\\circ')}<br><b>d)</b> ${m('120^\\circ')}`, o: ['a', 'b', 'c', 'd'] },
    { t: 'Dạng 1 · Bài 2', de: `Hai lực đồng quy cùng độ lớn ${m('20\\ \\mathrm N')}. Hợp lực khi góc giữa hai lực là:<br><b>a)</b> ${m('60^\\circ')}<br><b>b)</b> ${m('90^\\circ')}<br><b>c)</b> ${m('120^\\circ')}`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 2 · Bài 1', de: `Hai lực đồng quy ${m('F_1=9{,}0\\ \\mathrm N')}, ${m('F_2=12\\ \\mathrm N')}.<br><b>a)</b> hợp lực nhỏ nhất, lớn nhất<br><b>b)</b> hợp lực có thể bằng ${m('25\\ \\mathrm N')} không<br><b>c)</b> hợp lực bằng ${m('15\\ \\mathrm N')}: góc giữa hai lực`, o: [a1, a2, 'b', 'c'] },
    { t: 'Dạng 2 · Bài 2', de: `Hai lực đồng quy cùng độ lớn ${m('10\\ \\mathrm N')}.<br><b>a)</b> hợp lực nhỏ nhất, lớn nhất<br><b>b)</b> hợp lực bằng ${m('10\\ \\mathrm N')}: góc giữa hai lực<br><b>c)</b> hợp lực bằng ${m('17{,}3\\ \\mathrm N')}: góc giữa hai lực`, o: [a1, a2, 'b', 'c'] },
    { t: 'Dạng 3 · Bài 1', de: `Kéo xe bằng dây chếch lên ${m('30^\\circ')} so với phương ngang, lực ${m('F=60\\ \\mathrm N')}.<br><b>a)</b> ${m('F_x')} (a<sub>1</sub>), ${m('F_y')} (a<sub>2</sub>)<br><b>b)</b> dây chếch ${m('45^\\circ')}: ${m('F_x')}`, fig: H.keo(`Dây chếch góc ${al} so với phương ngang.`), fw: 40, o: [a1, a2, 'b'] },
    { t: 'Dạng 3 · Bài 2', de: `Kéo vali bằng lực ${m('50\\ \\mathrm N')} dọc theo quai, quai hợp với phương ngang ${m('50^\\circ')}.<br><b>a)</b> thành phần ngang ${m('F_x')}, thẳng đứng ${m('F_y')}<br><b>b)</b> vẫn kéo ${m('50\\ \\mathrm N')}, muốn ${m('F_x=40\\ \\mathrm N')} thì quai hợp với phương ngang góc bao nhiêu`, o: [a1, a2, 'b'] },
  ], [
    { t: 'Dạng 4 · Bài 1', de: `Vật ${m('10\\ \\mathrm{kg}')} trên dốc nghiêng ${m('30^\\circ')}; ${g10}.<br><b>a)</b> thành phần trọng lực dọc dốc ${m('P_x')}, vuông góc dốc ${m('P_y')}<br><b>b)</b> dốc nghiêng ${m('45^\\circ')}: ${m('P_x')}`, o: [a1, a2, 'b'] },
    { t: 'Dạng 4 · Bài 2', de: `Thùng ${m('6{,}0\\ \\mathrm{kg}')} trên dốc nghiêng ${m('25^\\circ')}; ${g10}.<br><b>a)</b> ${m('P_x')} (dọc dốc) và ${m('P_y')} (vuông góc dốc)<br><b>b)</b> dốc nghiêng bao nhiêu độ thì ${m('P_x=P_y')}`, o: [a1, a2, 'b'] },
    { t: 'Dạng 5 · Bài 1', de: `Vật ${m('2{,}0\\ \\mathrm{kg}')} treo vào vòng ${m('O')}; dây ${m('OA')} nằm ngang, dây ${m('OB')} hợp với phương thẳng đứng ${m('45^\\circ')}; ${g10}.<br><b>a)</b> lực căng dây ${m('OB')}<br><b>b)</b> lực căng dây ${m('OA')}`, o: ['a', 'b'] },
    { t: 'Dạng 5 · Bài 2', de: `Vật ${m('5{,}0\\ \\mathrm{kg}')} treo vào vòng ${m('O')}; dây ${m('OA')} nằm ngang, dây ${m('OB')} hợp với <b>trần nằm ngang</b> góc ${m('60^\\circ')}; ${g10}.<br><b>a)</b> góc giữa ${m('OB')} và phương thẳng đứng<br><b>b)</b> lực căng dây ${m('OB')}<br><b>c)</b> lực căng dây ${m('OA')}`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 6 · Bài 1', de: `Hai cột cách nhau ${m('8{,}0\\ \\mathrm m')}, dây võng ${m('0{,}40\\ \\mathrm m')} khi treo đèn ${m('3{,}0\\ \\mathrm{kg}')} ở chính giữa; ${g10}.<br><b>a)</b> góc ${m('\\theta')} giữa mỗi nhánh và phương ngang<br><b>b)</b> lực căng mỗi nhánh<br><b>c)</b> lực căng gấp mấy lần trọng lượng đèn`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 6 · Bài 2', de: `Đèn ${m('2{,}0\\ \\mathrm{kg}')} treo chính giữa một dây, mỗi nhánh hợp với phương ngang ${m('10^\\circ')}; ${g10}.<br><b>a)</b> lực căng mỗi nhánh<br><b>b)</b> dây chùng hơn, mỗi nhánh hợp với phương ngang ${m('30^\\circ')}: lực căng<br><b>c)</b> lực căng ở câu a gấp mấy lần trọng lượng đèn`, o: ['a', 'b', 'c'] },
    nhap(2),
  ]],
  dap: [
    `D1·1: a) 14 N · b) 2,0 N · c) 10 N · d) 7,21 N &nbsp;|&nbsp; D1·2: a) 34,6 N · b) 28,3 N · c) 20 N &nbsp;|&nbsp; D2·1: ${a1}) 3,0 N · ${a2}) 21 N · b) không · c) 90° &nbsp;|&nbsp; D2·2: ${a1}) 0 · ${a2}) 20 N · b) 120° · c) 60° &nbsp;|&nbsp; D3·1: ${a1}) 52,0 N · ${a2}) 30,0 N · b) 42,4 N &nbsp;|&nbsp; D3·2: ${a1}) 32,1 N · ${a2}) 38,3 N · b) 36,9°`,
    `D4·1: ${a1}) 50 N · ${a2}) 86,6 N · b) 70,7 N &nbsp;|&nbsp; D4·2: ${a1}) 25,4 N · ${a2}) 54,4 N · b) 45° &nbsp;|&nbsp; D5·1: a) 28,3 N · b) 20 N &nbsp;|&nbsp; D5·2: a) 30° · b) 57,7 N · c) 28,9 N &nbsp;|&nbsp; D6·1: a) 5,71° · b) 151 N · c) 5,02 lần &nbsp;|&nbsp; D6·2: a) 57,6 N · b) 20 N · c) 2,88 lần`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 3], kq: [[1, 2, 3], [4, 5, 6]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'tổng hợp 1·4 · cùng phương 2·1 · hình bình hành 2·2 · song song 3·1 · phân tích 3·2 · dốc 3·3 · cân bằng 3·4 · bẫy 4·1 · mẫu 5·2, 5·3 · dạng 1–3 → 6·1 · 4–6 → 7·1',
  out: process.argv[2],
});
