// Ruột tập VL12 – Bài 3 · Nội năng. Định luật 1 của nhiệt động lực học (lesson id 4). Quyển Chương 1 lớp 12: bài 3 = tr. 25–36.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l12-bai3.mjs (toàn bộ SVG tự vẽ). Nội dung theo bài web (book/cache/4.json, tải từ DB 12/11/2026): mục tiêu, dự đoán
// hai ấm 60 °C, II.1–II.5, thí nghiệm bơm xe + Joule, bếp điện đo c, ba bẫy, Trả bài 7 câu, bài toán mẫu bơm xe, thử thách ⭐–⭐⭐⭐,
// 5 dạng bài tập mẫu. Đáp số Bài tương tự (tuongTu.dap) và các ô "em tự tính" tính bằng Python 12/11/2026.
// Chạy: node scripts/ruot-tap/l12-bai3.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl12-bai3.pdf
//       node scripts/ruot-tap/l12-bai3.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l12-bai3/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL12b3 as H } from './hinh-l12-bai3.mjs';

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
  const out = resolve(HERE, 'out/hinh-l12-bai3'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 3, lid: 4, ten: 'NỘI NĂNG · ĐỊNH LUẬT 1 NHIỆT ĐỘNG LỰC HỌC', lop: 12, baiDau: 1, sub: 'Vật lí 12 · Chương 1: Vật lí nhiệt' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const J = (s) => nw(m(`${s}\\ \\mathrm J`));
const cs = (s) => `${m('c')}<sub>${s}</sub>`;
const cN = nw(`${cs('nước')} ${m('=4200\\ \\mathrm{J/(kg{\\cdot}K)}')}`);
const cDv = m('\\mathrm{J/(kg{\\cdot}K)}');
const dU = m('\\Delta U'), A = m('A'), Q = m('Q'), dt = m('\\Delta t');
const oC = (s) => nw(m(`${s}\\ ^\\circ\\mathrm C`)), kg = (s) => nw(m(`${s}\\ \\mathrm{kg}`));
const hai = (a, b) => `${ck}${a} &nbsp;${ck}${b}`;

// Bài tương tự 1 cột, ô đáp số cuối dòng của ý (cùng cách l10-bai23).
const ttCss = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';

const p1 = `${ttCss}<section class="page">
${head('BÀI 3 · NỘI NĂNG · ĐỊNH LUẬT 1 NHIỆT ĐỘNG LỰC HỌC', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Nêu được <b>nội năng</b> là gì, đơn vị, nội năng phụ thuộc vào những gì`)}
${dong(`${ck}Kể được hai cách làm biến đổi nội năng; tính nhiệt lượng ${m('Q=mc\\Delta t')}`)}
${dong(`${ck}Vận dụng <b>định luật 1</b> ${m('\\Delta U=A+Q')} với đúng quy ước dấu`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Hai ấm nước đều ở ${oC('60')}: ấm A chứa 200 g, ấm B chứa 2 kg. So với ấm A, ấm B có nội năng</p>
<div class="fig-side" style="${fs(40)}"><div>
${opt('A', 'Bằng nhau, vì nội năng chỉ do nhiệt độ quyết định')}
${opt('B', 'Lớn hơn, vì cùng nhiệt độ nhưng nhiều phân tử hơn')}
${opt('C', 'Nhỏ hơn, vì nhiều nước thì phân tử chậm hơn')}
${opt('D', 'Không so sánh được')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 1)}</div>
${H.haiAm()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Nội năng', '1·4')}
<div class="card" style="padding:1.2mm 3mm">
<div>Nội năng là tổng ${f(22)} và ${f(22)} của các phân tử cấu tạo nên vật.</div>
<div>Kí hiệu ${f(10)}, đơn vị ${f(14)}. Nội năng phụ thuộc ${f(20)} và ${f(20)} của vật.</div>
<div>Cùng chất, cùng nhiệt độ: khối lượng càng lớn thì nội năng ${f(18)}.</div>
<div>Không đo trực tiếp được nội năng, chỉ đo được ${f(36)} của nó.</div>
<div style="margin-top:.6mm">Sáng sớm, thanh chắn kim loại và ghế gỗ cùng ở ${oC('5')} mà kim loại buốt tay hơn, vì kim loại ${f(40)}.</div></div>
${h3(5, 'Làm nhanh', '1·5')}
${box(cau(`Hai miếng sắt cùng khối lượng: miếng ngoài nắng ${oC('45')}, miếng trong bóng râm ${oC('30')}. Miếng nào có nội năng lớn hơn? Vì sao?`, 1) + cau(`Cốc nước ${oC('80')} và nồi nước ${oC('40')}: có chắc nồi nước có nội năng nhỏ hơn cốc không? Vì sao?`, 1))}
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('HAI CÁCH LÀM BIẾN ĐỔI NỘI NĂNG')}
${h3(1, 'II.2 · Thực hiện công và truyền nhiệt', '2·1')}
<div class="card fig-side" style="${fs(42)};padding:1.2mm 3mm"><div>
<div>Cách (a) gọi là ${f(30)}: có ${f(14)} làm vật dịch chuyển hoặc đổi thể tích.</div>
<div>Vật nhận công thì nội năng ${f(12)}; vật sinh công thì nội năng ${f(12)}.</div>
<div>Cách (b) gọi là ${f(30)}: xảy ra khi hai vật có ${f(30)}.</div>
<div>Vật thu nhiệt thì nội năng ${f(12)}; vật toả nhiệt thì nội năng ${f(12)}.</div></div>
${H.haiCach()}</div>
${h3(2, 'Thí nghiệm: bơm xe bằng tay, nóng ở đâu?', '2·2')}
<div class="card fig-side" style="${fs(38)};padding:1.2mm 3mm"><div>
<div><b>Làm:</b> bơm nhanh khoảng 30 giây (40–50 lần ấn), sờ thân ống ở 1, 2, 3; nghỉ cho nguội rồi bơm cùng số lần nhưng thật chậm. Coi mỗi lần ấn nhanh khí không kịp trao đổi nhiệt.</div>
<div><b>Quan sát:</b> chỗ nóng nhất ở vị trí ${f(10)}; bơm chậm thì nóng ${f(14)}.</div>
<div><b>Rút ra:</b> khí bị nén ${f(22)} nên nội năng ${f(12)}, khí nóng lên rồi truyền nhiệt ra thân bơm.</div>
<div>Ma sát pit-tông xảy ra dọc cả ống nên ${f(30)} được vì sao chỗ đó nóng nhất.</div></div>
${H.bomXe()}</div>
${h3(3, 'Thí nghiệm Joule: quả nặng quay cánh khuấy', '2·3')}
<div class="fig-side" style="${fs(44)}"><div>
<div style="font-size:var(--fs-sm);line-height:1.35;margin-bottom:.6mm">Thả quả nặng ${m('M=20')} kg rơi ${m('h=2{,}00')} m, lặp ${m('n')} lần; công ${m('A=nMgh')} (${nw(m('g=9{,}8\\ \\mathrm{m/s^2}'))}) làm ${kg('0{,}400')} nước nóng thêm ${dt}. Số liệu minh hoạ, không phải số đo của Joule.</div>
<table class="tbl-ct"><tr><th>${m('n')}</th><th>${m('A')} (J)</th><th>${dt} (K)</th><th>${m('\\dfrac{A}{m\\Delta t}')} ${m('\\left(\\mathrm{\\tfrac{J}{kg\\cdot K}}\\right)')}</th></tr>
<tr><td>5</td><td>1 960</td><td>1,13</td><td>4 336</td></tr>
<tr><td>10</td><td>3 920</td><td>2,25</td><td>4 356</td></tr>
<tr><td>15</td><td>5 880</td><td>3,38</td><td>4 349</td></tr>
<tr><td>20</td><td>7 840</td><td>4,50</td><td style="height:7mm"></td></tr></table>
<div style="margin-top:.6mm"><b>Rút ra:</b> không đun mà nước vẫn nóng; tỉ số ${m('\\dfrac{A}{m\\Delta t}')} gần như ${f(20)} và gần nhiệt dung riêng của nước. Vậy công và nhiệt lượng ${f(22)}, cộng được với nhau.</div></div>
${H.joule()}</div>
<div class="card soft" style="padding:.8mm 3mm;margin-top:1mm">Tỉ số lớn hơn 4 180 một chút vì ${f(60)}</div>
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('NHIỆT LƯỢNG · ĐỊNH LUẬT 1 · ĐO NHIỆT LƯỢNG')}
${h3(1, 'II.3 · Nhiệt lượng, nhiệt dung riêng', '3·1')}
<div class="card" style="padding:1.2mm 3mm">
<div>Nhiệt dung riêng ${m('c')} của một chất: nhiệt lượng cần để ${f(14)} chất đó tăng thêm ${f(10)}.</div>
<table class="tbl-ct" style="margin:.6mm 0"><tr><th>Chất (cho sẵn)</th><th>nước</th><th>nhôm</th><th>sắt</th><th>đồng</th><th>chì</th></tr>
<tr><td>${m('c')} (${cDv})</td><td>4 200 <span class="hint">(tra: 4 180)</span></td><td>880</td><td>460</td><td>380</td><td>130</td></tr></table>
<div style="display:flex;align-items:flex-end;gap:3mm;min-height:7mm">${m('Q=')} <span class="fill" style="min-width:34mm"></span> <span>với ${dt} = ${f(26)}</span></div>
<div>Hiệu nhiệt độ đo theo °C hay K ${f(26)}. Mẹo: ${m('c')} lớn thì ${f(36)}.</div>
<div><b>Làm nhanh.</b> Tính nhiệt lượng cần để đun ${kg('0{,}50')} nhôm từ ${oC('20')} lên ${oC('120')}.</div>${lines(1)}</div>
${h3(2, 'II.4 · Định luật 1 nhiệt động lực học', '3·2')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div>Độ biến thiên nội năng của hệ bằng ${f(14)} công và nhiệt lượng mà hệ ${f(20)}.</div>
<div style="margin:1mm 0;display:flex;align-items:flex-end;gap:3mm">${dU} = <span class="fill" style="min-width:28mm"></span></div>
<div><b>Quy ước dấu:</b> ${m('A>0')} hệ nhận công, ${m('A<0')} hệ sinh công; ${m('Q>0')} hệ thu nhiệt, ${m('Q<0')} hệ toả nhiệt.</div>
<div>${m('\\Delta U>0')}: nội năng ${f(14)} · ${m('\\Delta U<0')}: nội năng ${f(14)}</div></div>
${H.dauAQ()}</div>
<table><tr><th style="width:62mm">Quá trình của khí</th><th style="width:14mm">${A}</th><th style="width:14mm">${Q}</th><th>${dU}; nóng hay lạnh đi</th></tr>
<tr><td>Nén nhanh, không kịp trao đổi nhiệt</td><td></td><td></td><td></td></tr>
<tr><td>Giãn nở, không trao đổi nhiệt</td><td></td><td></td><td></td></tr>
<tr><td>Đun trong bình kín, thể tích không đổi</td><td></td><td></td><td></td></tr></table>
${h3(3, 'Làm nhanh', '3·3')}
${box(cau(`Khí trong xilanh giãn nở, sinh công ${J('40')}, đồng thời thu nhiệt ${J('25')}. Đặt dấu ${A}, ${Q}; tính ${dU}. Khí nóng lên hay lạnh đi?`, 1))}
${h3(4, 'II.5 · Số liệu: đo c của nước bằng bếp điện', '3·4')}
<div class="card" style="padding:1.2mm 3mm">
<div style="font-size:var(--fs-sm);line-height:1.35">Đun ${kg('0{,}500')} nước, bếp ${nw(m('P=500\\ \\mathrm W'))} nên sau ${m('\\tau')} giây bếp đưa vào ${m('Q=P\\tau')}. ${dt} tính so với ${oC('25{,}0')}. Số liệu minh hoạ.</div>
<table class="tbl-ct" style="margin:.5mm 0"><tr><th>${m('\\tau')} (s)</th><th>20</th><th>40</th><th>60</th><th>80</th></tr>
<tr><td>${m('t')} (°C)</td><td>29,6</td><td>34,1</td><td>38,6</td><td>43,1</td></tr>
<tr><td>${m('c=\\dfrac{Q}{m\\Delta t}')} (${cDv})</td><td>4 348</td><td>4 396</td><td>4 412</td><td></td></tr></table>
<div><b>Rút ra:</b> ${m('c')} đo được lớn hơn 4 180 vì ${f(70)}</div></div>
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('BA CÁI BẪY · TRẢ BÀI · TỰ KIỂM TRA')}
${h3(1, 'III · Ba cái bẫy hay sập', '4·1')}
<div class="card fig-side" style="${fs(38)};padding:1mm 3mm"><div>
<div class="trap">${ck}<span><b>“Vật nhiều nội năng hơn thì nóng hơn.”</b> Điền bảng dưới rồi trả lời câu hỏi ở hình.</span></div>
<div class="trap">${ck}<span><b>“Vật có nhiệt lượng 500 J.”</b> Vật có <b>nội năng</b>; nhiệt lượng chỉ có trong lúc truyền.</span></div>
<div class="trap">${ck}<span><b>Dấu của ${A}.</b> “Khí sinh công 80 J” là ${m('A=-80')} J, không phải ${m('+80')} J.</span></div></div>
${H.satVaBe()}</div>
<table>
<tr><th style="width:52mm"></th><th>Nhiệt độ</th><th>Nội năng</th></tr>
<tr><td>Cho biết gì</td><td style="height:7mm"></td><td></td></tr>
<tr><td>Phụ thuộc khối lượng?</td><td style="height:6mm"></td><td></td></tr>
<tr><td>Quyết định chiều truyền nhiệt?</td><td style="height:6mm"></td><td></td></tr></table>
${h3(2, 'IV · Trả bài 7 câu', '4·2')}
${box(`${tb('1. Nội năng là gì, đơn vị, phụ thuộc những gì?')}${lines(1)}
${tb('2. Hai cách làm biến đổi nội năng; dấu hiệu phân biệt?')}${lines(1)}
${tb(`3. Công thức nhiệt lượng; kí hiệu, đơn vị?`)}${lines(1)}
${tb('4. Nhiệt dung riêng cho biết gì? Vì sao nước dùng làm mát?')}${lines(2)}
${tb('5. Phát biểu định luật 1, viết hệ thức.')}${lines(2)}
${tb('6. Vì sao khí bị nén nhanh lại nóng lên?')}${lines(2)}
${tb(`7. Nhiệt kế đo °C thì ${dt} có phải đổi sang K không?`)}${lines(1)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/7 câu · chưa thuộc: ${f(25)} ${nw(`→ đọc lại ô ${f(12)} Tập`)}</div>
${h3(3, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '4·3')}
${rkHai([1, 2, 3], [4, 5])}
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TOÁN MẪU · BÀI TẬP VỀ NHÀ · THỬ THÁCH')}
${h3(1, 'V · Bài toán mẫu: bơm xe đạp', '5·1')}
<div class="card soft" style="padding:1.2mm 3mm">Trong một lần ấn pit-tông, người bơm thực hiện công ${J('60')} lên khối khí trong bơm; cùng lúc khối khí truyền ra ngoài ${J('15')} nhiệt lượng qua thành ống bơm. <b>a)</b> Tính độ biến thiên nội năng của khối khí. <b>b)</b> Khí nóng lên hay lạnh đi? Vì sao?</div>
<table><tr><th style="width:50mm">Câu trong đề</th><th>Dữ liệu → kiến thức</th></tr>
<tr><td>“công 60 J lên khối khí”</td><td>khí nhận công → ${m('A=+60')} J</td></tr>
<tr><td style="height:6mm">“truyền ra ngoài 15 J nhiệt lượng”</td><td></td></tr>
<tr><td style="height:6mm">“độ biến thiên nội năng”</td><td></td></tr>
</table>
<div class="fig-side" style="${fs(42)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl(`Hệ: ……………… · Đặt dấu: ${A} = …… ; ${Q} = ……`, 1)}${wl(`a) ${dU} =`, 1)}${wl('b)', 1)}</div>${H.bomMau()}</div>
${h3(2, 'Điền bước còn thiếu: lần ấn này công 75 J, nhiệt truyền ra ngoài 25 J', '5·2')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div class="ln"><b>Bước 1 (cho sẵn):</b> khí nhận công ${m('A=+75')} J; khí toả nhiệt ${m('Q=-25')} J</div>
${wl(`Bước 2: ${dU} =`, 1)}${wl('Bước 3: khí nóng lên hay lạnh đi, vì sao?', 1)}</div>
${K.btvn().replace('<i>1</i>', '<i>3</i>')}
${h3(4, 'Thử thách phân tầng', '5·4')}
${box(cau(`${m('\\bigstar')} Đun ${kg('1{,}5')} nước từ ${oC('20')} lên ${oC('80')}, ${cN}. Tính nhiệt lượng cần.`, 1)
 + cau(`${m('\\bigstar\\bigstar')} Khối nhôm 400 g ở ${oC('250')} thả vào ${kg('0{,}80')} nước ở ${oC('25')}; ${nw(`${cs('nhôm')} ${m('=880')}`)}, ${nw(`${cs('nước')} ${m('=4200')}`)} ${cDv}. Bỏ qua mất mát, tìm nhiệt độ cân bằng.`, 1)
 + cau(`${m('\\bigstar\\bigstar\\bigstar')} ${kg('0{,}500')} nước đá ở ${oC('0')}, bếp 500 W: tan hết sau 334 s, suốt lúc đó nhiệt độ đứng yên ở ${oC('0')}. Vì sao? Tính nhiệt lượng làm tan 1 kg nước đá.`, 1))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Nhận ra cách biến đổi nội năng',
    de: `Đĩa phanh nhôm ${kg('0{,}25')} ở ${oC('25{,}0')}, ${nw(m('c=880'))} ${cDv}. Phanh gấp: má phanh thực hiện công ${J('4400')} lên đĩa (chưa kịp truyền nhiệt); rồi đĩa từ ${oC('45{,}0')} nguội về ${oC('25{,}0')}.<br><b>a)</b> lúc phanh: ${hai('thực hiện công', 'truyền nhiệt')}; ${m('\\Delta U_1')}<br><b>b)</b> lúc nguội: ${hai('thực hiện công', 'truyền nhiệt')}; nhiệt lượng ${Q} và ${m('\\Delta U_2')}<br><b>c)</b> ${dU} cả hai giai đoạn`,
    nd: `Nhận công thì ${A} ${f(8)}; toả nhiệt thì ${Q} ${f(8)}; ${nw(`${dt} = ${f(22)}`)}`, a: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], gi: 4, fig: H.phanhD1('') },
  { t: 'Dạng 2 · Trung bình · Đặt dấu A, Q cho từng giai đoạn',
    de: `Giai đoạn 1: nén nhanh, pit-tông thực hiện công ${J('180')} lên khí, khí toả ra ngoài ${J('70')}. Giai đoạn 2: khí giãn nở, thu ${J('130')} từ không khí xung quanh và sinh công ${J('150')}.<br><b>a)</b> ${m('\\Delta U_1')} ở giai đoạn 1<br><b>b)</b> ${m('\\Delta U_2')} ở giai đoạn 2<br><b>c)</b> sau hai giai đoạn, nội năng ${hai('tăng', 'giảm')} bao nhiêu`,
    nd: `Mỗi giai đoạn đặt dấu riêng, rồi cộng ${f(16)} ${m('\\Delta U_1+\\Delta U_2')}`, a: ['a', 'b', 'c'], gi: 3 },
  { t: 'Dạng 3 · Trung bình · Bài ngược: biết ΔU, tìm A hoặc Q',
    de: `(1) nén khí: nhận công ${J('25')}, nội năng giảm ${J('35')}; (2) hơ nóng: nhận nhiệt ${J('100')}, nội năng tăng ${J('20')}.<br><b>a)</b> quá trình 1: khí ${hai('toả', 'thu')} nhiệt; ${m('Q_1')}<br><b>b)</b> quá trình 2: khí ${hai('nhận', 'sinh')} công; ${m('A_2')}`,
    nd: `Nội năng giảm thì ${dU} ${f(8)}; rút ${nw(`${m('Q=')} ${f(16)}`)}, ${nw(`${m('A=')} ${f(16)}`)}`, a: ['a', 'b'], gi: 2 },
  { t: 'Dạng 4 · Khó · Công làm nóng vật rồi nhiệt truyền sang nước',
    de: `Khoan lỗ trên khối đồng ${kg('0{,}300')} đặt trong cốc cách nhiệt chứa ${kg('0{,}250')} nước ở ${oC('24{,}0')}. Một lượt khoan, mũi khoan thực hiện công ${J('5400')} lên khối đồng; cuối lượt nước ở ${oC('27{,}0')}. Nước chỉ nhận nhiệt từ khối đồng và không nhận công; ${cN}.<br><b>a)</b> nhiệt lượng nước nhận được<br><b>b)</b> khối đồng ${hai('toả', 'thu')} nhiệt; nhiệt lượng ${Q} của khối đồng<br><b>c)</b> ${dU} của khối đồng; nội năng đồng ${hai('tăng', 'giảm')}`,
    nd: `Nước thu bao nhiêu thì đồng ${f(12)} bấy nhiêu; đồng: ${nw(`${A} = ${f(12)}`)}, ${nw(`${Q} = ${f(12)}`)}`, a: ['a', 'b', 'c'], gi: 6, fig: H.khoanD4() },
  { t: 'Dạng 5 · Nâng cao · Cả chu trình: ΔU = 0 trong tủ lạnh',
    de: `Gas trong tủ lạnh tuần hoàn qua máy nén, dàn nóng, van tiết lưu, dàn lạnh rồi trở về đúng trạng thái đầu. Mỗi chu trình máy nén thực hiện công ${J('150')} lên gas; ở dàn nóng gas toả ra ${J('450')}. Van không có công, không trao đổi nhiệt; gas chỉ thu nhiệt ở dàn lạnh.<br><b>a)</b> nhiệt lượng gas thu ở dàn lạnh mỗi chu trình<br><b>b)</b> cần lấy ${nw(m('54\\ \\mathrm{kJ}'))} nhiệt từ ngăn lạnh: số chu trình<br><b>c)</b> tổng công máy nén trong số chu trình đó`,
    nd: `Hết chu trình về trạng thái đầu nên ${nw(`${dU} = ${f(10)}`)}; ${nw(`${m('0=A+Q_{\\text{nóng}}+')} ${f(14)}`)}`, a: ['a', 'b', 'c'], gi: 6, fig: H.tuLanhD5() },
];

// Bài tương tự: mỗi dạng 2 bài, giải vào vở (thầy chốt 10/11), ô đáp số cuối dòng của ý; đáp số tính bằng Python 12/11/2026.
const oY = (s, o, w = {}) => s.split('<br>').map((p) => {
  const y = p.match(/^<b>([a-d])\)<\/b>/);
  if (!y) return `<div>${p}</div>`;
  const ls = o.filter((l) => l[0] === y[1]);
  return `<div class="yo"><span>${p}</span><span class="oo">${ls.map((l) => `<span class="nw"><b>${l})</b>${f(typeof w === 'object' ? (w[l] ?? 25) : w)}</span>`).join('')}</span></div>`;
}).join('');
const ttDe = (b) => b.fig ? `<div class="fig-side" style="grid-template-columns:1fr ${b.fw}mm">${`<div>${oY(b.de, b.o, b.ow)}</div>`}${b.fig}</div>` : oY(b.de, b.o, b.ow);
const vaoVo = (ds) => ds.map((b) => (b.o ? { t: b.t, de: ttDe(b), k: 0 } : b));
const nhap = (n) => ({ t: '<span class="nhap-t">Nháp / chỗ em còn vướng</span>', de: lines(n), k: 0 });
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–3', 'DẠNG 4–5'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Đĩa phanh thép ${kg('0{,}40')}, ${nw(m('c=460'))} ${cDv}, ở ${oC('30{,}0')}. Phanh gấp: ma sát thực hiện công ${J('3680')} lên đĩa, chưa kịp truyền nhiệt; đĩa lên ${oC('50{,}0')} rồi nguội về ${oC('35{,}0')}.<br><b>a)</b> ${m('\\Delta U_1')} lúc phanh<br><b>b)</b> nhiệt lượng ${Q} của đĩa lúc nguội<br><b>c)</b> ${dU} của đĩa cả hai giai đoạn`, fig: H.phanhTT(''), fw: 44, o: ['a', 'b', 'c'] },
    { t: 'Dạng 1 · Bài 2', de: `Búa đập lên miếng chì ${kg('0{,}20')} (${nw(m('c=130'))} ${cDv}), tổng công ${J('520')}; chì chưa kịp truyền nhiệt.<br><b>a)</b> nội năng chì đổi bằng cách nào; ${dU} của chì<br><b>b)</b> độ tăng nhiệt độ của chì<br><b>c)</b> sau đó chì nguội về nhiệt độ ban đầu: nhiệt lượng ${Q} của chì`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'], ow: { 'a<sub>1</sub>': 30, 'a<sub>2</sub>': 20, b: 20, c: 22 } },
    { t: 'Dạng 2 · Bài 1', de: `(1) khí bị nén, nhận công ${J('250')}, toả nhiệt ${J('90')}; (2) khí giãn nở, sinh công ${J('200')}, thu nhiệt ${J('60')}.<br><b>a)</b> ${m('\\Delta U_1')} ở giai đoạn (1)<br><b>b)</b> ${m('\\Delta U_2')} ở giai đoạn (2)<br><b>c)</b> ${dU} sau hai giai đoạn; nội năng tăng hay giảm`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 2 · Bài 2', de: `(1) khí thu nhiệt ${J('300')}, giãn nở sinh công ${J('120')}; (2) khí bị nén, nhận công ${J('80')}, toả nhiệt ${J('260')}.<br><b>a)</b> ${m('\\Delta U_1')} ở giai đoạn (1)<br><b>b)</b> ${m('\\Delta U_2')} ở giai đoạn (2)<br><b>c)</b> ${dU} sau hai giai đoạn`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 3 · Bài 1', de: `(1) nén khí: nhận công ${J('40')}, nội năng tăng ${J('15')}; (2) hơ nóng: nhận nhiệt ${J('70')}, nội năng giảm ${J('10')}.<br><b>a)</b> ${m('Q_1')} (có dấu); khí toả hay thu nhiệt<br><b>b)</b> ${m('A_2')} (có dấu); khí nhận hay sinh công`, o: ['a', 'b'] },
    { t: 'Dạng 3 · Bài 2', de: `(1) khí giãn nở sinh công ${J('50')}, nội năng giảm ${J('20')}; (2) khí toả nhiệt ${J('45')}, nội năng tăng ${J('15')}.<br><b>a)</b> ${m('Q_1')} (có dấu); khí toả hay thu nhiệt<br><b>b)</b> ${m('A_2')} (có dấu); khí nhận hay sinh công`, o: ['a', 'b'] },
    nhap(3),
  ], [
    { t: 'Dạng 4 · Bài 1', de: `Khoan khối nhôm ${kg('0{,}200')} đặt trong cốc cách nhiệt chứa ${kg('0{,}300')} nước ở ${oC('20{,}0')}. Mũi khoan thực hiện công ${J('6000')} lên khối nhôm; cuối lượt nước ở ${oC('23{,}0')}. Nước chỉ nhận nhiệt từ nhôm, không nhận công; ${cN}.<br><b>a)</b> nhiệt lượng nước nhận được<br><b>b)</b> nhiệt lượng ${Q} của khối nhôm (có dấu)<br><b>c)</b> ${dU} của khối nhôm`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 4 · Bài 2', de: `Mài một khối sắt đặt trong chậu cách nhiệt chứa ${kg('0{,}500')} nước; đá mài thực hiện công ${J('4000')} lên khối sắt, nước nóng từ ${oC('25{,}0')} lên ${oC('26{,}5')}. Nước chỉ nhận nhiệt từ sắt, không nhận công; ${cN}.<br><b>a)</b> nhiệt lượng nước nhận được<br><b>b)</b> nhiệt lượng ${Q} của khối sắt (có dấu)<br><b>c)</b> ${dU} của khối sắt`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 5 · Bài 1', de: `Tủ lạnh: mỗi chu trình máy nén thực hiện công ${J('200')} lên gas, gas toả ra ở dàn nóng ${J('700')}, chỉ thu nhiệt ở dàn lạnh; hết chu trình gas về đúng trạng thái đầu.<br><b>a)</b> nhiệt gas thu ở dàn lạnh mỗi chu trình<br><b>b)</b> lấy ${nw(m('60\\ \\mathrm{kJ}'))} từ ngăn lạnh: số chu trình<br><b>c)</b> tổng công máy nén khi đó`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 5 · Bài 2', de: `Điều hoà: mỗi chu trình gas thu ${J('600')} ở dàn lạnh trong phòng, máy nén thực hiện công ${J('200')} lên gas; gas toả nhiệt ở dàn nóng ngoài trời và về đúng trạng thái đầu (${nw(m('1\\ \\mathrm{MJ}=10^6\\ \\mathrm J'))}).<br><b>a)</b> nhiệt gas toả ở dàn nóng mỗi chu trình<br><b>b)</b> lấy ${nw(m('1{,}2\\ \\mathrm{MJ}'))} khỏi phòng: số chu trình<br><b>c)</b> tổng nhiệt toả ra ngoài trời khi đó`, fig: H.dieuHoaTT(), fw: 46, o: ['a', 'b', 'c'], ow: 20 },
    nhap(5),
  ]],
  dap: [
    `D1·1: a) +3 680 J · b) −2 760 J · c) +920 J &nbsp;|&nbsp; D1·2: a<sub>1</sub>) thực hiện công · a<sub>2</sub>) +520 J · b) 20 K · c) −520 J &nbsp;|&nbsp; D2·1: a) +160 J · b) −140 J · c) +20 J, tăng &nbsp;|&nbsp; D2·2: a) +180 J · b) −180 J · c) 0 J &nbsp;|&nbsp; D3·1: a) −25 J, toả · b) −80 J, sinh công &nbsp;|&nbsp; D3·2: a) +30 J, thu · b) +60 J, nhận công`,
    `D4·1: a) 3 780 J · b) −3 780 J · c) +2 220 J &nbsp;|&nbsp; D4·2: a) 3 150 J · b) −3 150 J · c) +850 J &nbsp;|&nbsp; D5·1: a) 500 J · b) 120 · c) 24 000 J &nbsp;|&nbsp; D5·2: a) 800 J · b) 2 000 · c) 1,6·10<sup>6</sup> J`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 2], kq: [[1, 2, 3], [4, 5]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'nội năng 1·4 · hai cách 2·1 · bơm xe 2·2 · Joule 2·3 · nhiệt lượng 3·1 · định luật 1 3·2 · bếp điện 3·4 · bẫy 4·1 · bài toán mẫu 5·1 · dạng 1–3 → 6·1 · dạng 4–5 → 7·1',
  out: process.argv[2],
});
