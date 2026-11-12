// Ruột tập VL12 – Bài 2 · Thang nhiệt độ (lesson id 3). Quyển Chương 1 lớp 12 (Vật lí nhiệt): bài 2 = tr. 13–24.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l12-bai2.mjs (toàn bộ SVG tự vẽ). Nội dung theo bài web (book/cache/3.json, tải từ DB 12/11/2026): mục tiêu, dự đoán
// cơn sốt 38,5 °C trên thang Kelvin, II.1–II.5 (cân bằng nhiệt + trộn nước, Celsius + kiểm hai mốc, Kelvin + kéo dài đồ thị p–t,
// Fahrenheit + bảng đổi, nhiệt kế), ba bẫy, Trả bài 6 câu, bài toán mẫu lò nướng 392 °F, thử thách ⭐–⭐⭐⭐, 6 dạng bài tập mẫu.
// Đáp số Bài tương tự (tuongTu.dap) và các ô "em tự tính" tính bằng Python 12/11/2026.
// Chạy: node scripts/ruot-tap/l12-bai2.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl12-bai2.pdf
//       node scripts/ruot-tap/l12-bai2.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l12-bai2/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL12b2 as H } from './hinh-l12-bai2.mjs';

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
  const out = resolve(HERE, 'out/hinh-l12-bai2'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 2, lid: 3, ten: 'THANG NHIỆT ĐỘ', lop: 12, baiDau: 1, sub: 'Vật lí 12 · Chương 1: Vật lí nhiệt' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const dC = (s) => nw(m(`${s}\\ ^\\circ\\mathrm C`)), dF = (s) => nw(m(`${s}\\ ^\\circ\\mathrm F`)), dK = (s) => nw(m(`${s}\\ \\mathrm K`));
const oC = m('^\\circ\\mathrm C'), oF = m('^\\circ\\mathrm F'), oK = m('\\mathrm K');
const cK = nw(m('T=t+273')), cF = nw(m('t_F=1{,}8\\,t+32'));
const dung2 = `Dùng ${cK} và ${cF}.`;
const dung3 = `(dùng ${cK}, ${cF})`;
const tall = (w) => `<span class="fill" style="min-width:${w}mm;height:10mm"></span>`;

// Bài tương tự 1 cột, ô đáp số cuối dòng của ý (cùng cách l11-bai16).
const ttCss = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';

const p1 = `${ttCss}<section class="page">
${head('BÀI 2 · THANG NHIỆT ĐỘ', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Nêu ý nghĩa của nhiệt độ: <b>cân bằng nhiệt</b>, <b>chiều truyền nhiệt năng</b>`)}
${dong(`${ck}Đọc ba thang Celsius – Kelvin – Fahrenheit; đổi <b>một giá trị</b>, <b>một khoảng chênh</b>`)}
${dong(`${ck}Kể được nguyên lí các loại <b>nhiệt kế</b>`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Đêm qua em sốt: nhiệt kế ở nhà hiện ${dC('38{,}5')}, bác sĩ bên Mỹ đọc ${dF('101{,}3')}. Đo cùng cơn sốt bằng nhiệt kế thang Kelvin thì được:</p>
<div class="fig-side" style="${fs(36)}"><div>
<div class="two" style="gap:0 3mm">${opt('A', dK('38{,}5'))}${opt('B', dK('311{,}5'))}${opt('C', dK('234{,}5'))}${opt('D', dK('273'))}</div>
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 1)}</div>
${H.baThang()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Nhiệt độ và cân bằng nhiệt', '1·4')}
<div class="card fig-side" style="${fs(34)};padding:1.2mm 3mm"><div>
<div>Tiếp xúc, chênh nhiệt độ: nhiệt năng truyền từ vật ${f(14)} sang vật ${f(14)}.</div>
<div>Phần nhiệt năng truyền đi gọi là ${f(25)}.</div>
<div>Nhiệt độ bằng nhau thì ${f(25)}: hai vật ở trạng thái ${f(25)}.</div>
<div>Nhiệt độ cho biết trạng thái ${f(25)} và ${f(16)} truyền nhiệt năng.</div></div>
${H.tiepXuc('a) Trước khi tiếp xúc. b) Sau một lúc.')}</div>
<div class="card" style="padding:1.2mm 3mm">
<div><b>Thí nghiệm: trộn nước nóng với nước lạnh.</b> Mô hình (bỏ qua ca): ${m('t_{cb}=\\dfrac{m_1t_1+m_2t_2}{m_1+m_2}')}</div>
<table class="tbl-ct" style="margin:.6mm 0"><tr><th>${m('m_1')} (g)</th><th>${m('t_1')} (${oC})</th><th>${m('m_2')} (g)</th><th>${m('t_2')} (${oC})</th><th>${m('t_{cb}')} mô hình</th><th>${m('t_{cb}')} đo</th></tr>
<tr><td>100</td><td>60</td><td>100</td><td>20</td><td>40,0</td><td>39,1</td></tr>
<tr><td>100</td><td>80</td><td>300</td><td>20</td><td></td><td>34,6</td></tr></table>
<div><b>Rút ra:</b> ${m('t_{cb}')} nằm ${f(20)} hai nhiệt độ đầu, lệch về phía phần nước ${f(18)}. Số đo ${f(16)} mô hình vì ${f(30)}</div>
</div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('THANG CELSIUS · KIỂM TRA HAI MỐC')}
${h3(1, 'II.2 · Thang Celsius', '2·1')}
<div class="card" style="padding:1.2mm 3mm">
<div>Mốc 1: nhiệt độ ${f(25)} của nước đá tinh khiết, quy ước ${nw(`${f(10)} ${oC}`)}</div>
<div>Mốc 2: nhiệt độ ${f(20)} của nước tinh khiết ở áp suất tiêu chuẩn, quy ước ${nw(`${f(10)} ${oC}`)}</div>
<div>Khoảng giữa chia thành ${f(12)} phần bằng nhau; kí hiệu ${m('t')}, đơn vị ${oC}; dưới 0 là số ${f(14)}.</div>
</div>
${h3(2, 'Thí nghiệm: kiểm tra hai mốc 0 °C và 100 °C', '2·2')}
<div class="card fig-side" style="${fs(42)};padding:1.2mm 3mm"><div>
<div><b>Giả thuyết:</b> nhiệt kế (sai số ${nw(m('\\pm0{,}5\\ ^\\circ\\mathrm C'))}) chia độ đúng ở hai mốc ${dC('0')} và ${dC('100')}.</div>
<div><b>Làm:</b> (1) cắm bầu nhiệt kế vào giữa nước đá đập nhỏ trộn nước cất, không chạm đáy; khuấy, đọc ba lần cách nhau 1 phút. (2) Đun nước cất sôi đều, giữ bầu trong hơi nước ngay trên mặt nước, đọc ba lần. (3) Ghi áp suất khí quyển; coi đúng 1 atm.</div></div>
${H.haiMoc()}</div>
<table><tr><th style="width:40mm">Trường hợp</th><th>Ba lần đọc (${oC})</th><th style="width:34mm">Trung bình (${oC})</th></tr>
<tr><td>Nước đá đang tan</td><td>0,2 · 0,1 · 0,3</td><td>0,2</td></tr>
<tr><td>Hơi nước đang sôi</td><td>99,6 · 99,7 · 100,1</td><td></td></tr></table>
<div class="card" style="margin-top:1mm;padding:1.2mm 3mm">
<div><b>Rút ra:</b> cả hai số trung bình lệch mốc ${f(14)} ${dC('0{,}5')} nên ${f(25)} giả thuyết.</div>
<div><b>Chưa nói được:</b> nhiệt kế có chia ${f(16)} ở khoảng giữa hai mốc không.</div>
</div>
${h3(3, 'Chiều sai số: số đọc cao hơn hay thấp hơn mốc?', '2·3')}
<table><tr><th>Nguyên nhân</th><th style="width:24mm">Mốc nào</th><th style="width:30mm">Đọc cao / thấp hơn</th></tr>
<tr><td>Áp suất khí quyển dưới 1 atm</td><td></td><td></td></tr>
<tr><td>Nước đá lẫn muối, tạp chất</td><td></td><td></td></tr>
<tr><td>Bầu nhiệt kế chạm đáy bình đang đun</td><td></td><td></td></tr>
<tr><td>Đọc khi số chưa đứng yên (mốc dưới; mốc trên)</td><td>cả hai</td><td></td></tr></table>
${h3(4, 'Làm nhanh', '2·4')}
${box(cau('Bạn nói: “Nước đang sôi đứng nhiệt độ vì không nhận thêm nhiệt lượng.” Đúng hay sai? Vì sao hai trạng thái này làm được mốc?', 2))}
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('THANG KELVIN · THANG FAHRENHEIT')}
${h3(1, 'II.3 · Thang Kelvin: mốc 0 tuyệt đối', '3·1')}
<div class="card" style="padding:1.2mm 3mm">
<div>Gốc ${dK('0')}: độ không ${f(18)}, nhiệt độ ${f(18)} mà vật có thể có.</div>
<div>Mốc còn lại: nhiệt độ ${f(18)} của nước (cùng lúc ở cả ba thể), quy ước ${nw(`${f(14)} K`)} (tương đương ${dC('0{,}01')}).</div>
<div>Kí hiệu ${m('T')}, đơn vị K: viết ${dK('300')}, không viết ${f(14)}; ${m('T')} không bao giờ ${f(12)}.</div>
<div>Khoảng chênh ${dK('1')} ${f(16)} khoảng chênh ${dC('1')}.</div>
<div style="display:flex;align-items:flex-end;gap:3mm;flex-wrap:wrap">${m('T=')} ${tall(30)} <span>bài tập thường làm tròn: ${m('T=')} ${f(24)}</span></div>
</div>
<div class="fig-side" style="${fs(46)}"><div>
<div><b>Thí nghiệm: kéo dài đồ thị để tìm 0 K.</b> Giữ thể tích một lượng khí không đổi, ngâm bình lần lượt vào nước đá đang tan, nước phòng, nước ấm, nước sôi; đọc áp suất.</div>
<table class="tbl-ct" style="margin:.6mm 0"><tr><th>${m('t')} (${oC})</th><td>0</td><td>25</td><td>50</td><td>75</td><td>100</td></tr>
<tr><th>${m('p')} (kPa)</th><td>100,0</td><td>109,2</td><td>118,3</td><td>127,5</td><td>136,6</td></tr></table>
<div>Tăng 1 độ, ${m('p')} tăng ${nw(`≈ ${f(14)} kPa`)}. Từ ${dC('0')} phải hạ thêm ${nw(`≈ ${f(12)} độ`)} để ${nw(m('p=0'))}: đường thẳng cắt trục ${m('t')} ở ${nw(`≈ ${f(14)} ${oC}`)}.</div>
<div>Mọi chất khí cho cùng điểm cắt: đó là gốc ${f(14)}.</div></div>
${H.doThiP()}</div>
${h3(2, 'II.4 · Thang Fahrenheit', '3·2')}
<div class="card" style="padding:1.2mm 3mm">
<div>Hai mốc nước: nước đá đang tan ${nw(`${f(12)} ${oF}`)}, hơi nước đang sôi ${nw(`${f(12)} ${oF}`)}; khoảng giữa chia ${f(12)} khoảng.</div>
<div>Một độ chia ${oC} ứng với ${nw(`${f(12)} : 100 = ${f(10)}`)} độ chia ${oF}.</div>
<div style="display:flex;align-items:flex-end;gap:6mm;flex-wrap:wrap;margin-top:.6mm"><span>${m('t_F=')} ${tall(30)}</span><span>${m('t_C=')} ${tall(30)}</span></div>
</div>
${h3(3, 'Bảng đổi giữa ba thang', '3·3')}
<table><tr><th style="width:36mm">Muốn đổi</th><th>Làm gì</th></tr>
<tr><td>${oC} → K</td><td></td></tr><tr><td>K → ${oC}</td><td></td></tr><tr><td>${oC} → ${oF}</td><td></td></tr><tr><td>${oF} → ${oC}</td><td></td></tr>
<tr><td>K ↔ ${oF}</td><td></td></tr>
<tr><td style="height:9mm">Khoảng chênh</td><td>${m('\\Delta T')} (K) = ${f(18)} &nbsp; ${m('\\Delta t_F')} (${oF}) = ${f(22)}</td></tr></table>
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('NHIỆT KẾ · BA CÁI BẪY · TRẢ BÀI')}
${h3(1, 'Làm nhanh', '4·1')}
${box(cau(`<b>Câu 1.</b> ${dung2} Nhiệt độ phòng ${dC('25')} bằng bao nhiêu ${oF}? Bao nhiêu K?`, 1)
 + cau(`<b>Câu 2.</b> Khay bánh nguội từ ${dC('180')} xuống ${dC('25')}. Nhiệt độ giảm bao nhiêu ${oC}, bao nhiêu K, bao nhiêu ${oF}?`, 1))}
${h3(2, 'II.5 · Nhiệt kế: mỗi loại dựa trên tính chất gì?', '4·2')}
<div class="fig-side" style="${fs(36)}">
<table><tr><th style="width:28mm">Loại nhiệt kế</th><th>Dựa trên tính chất thay đổi theo nhiệt độ</th></tr>
<tr><td>Chất lỏng</td><td></td></tr><tr><td>Kim loại</td><td></td></tr><tr><td>Khí</td><td></td></tr>
<tr><td>Điện trở</td><td></td></tr><tr><td>Cặp nhiệt điện</td><td></td></tr><tr><td>Hồng ngoại</td><td></td></tr></table>
${H.hongNgoai()}</div>
${h3(3, 'III · Ba cái bẫy hay sập', '4·3')}
<div class="card" style="padding:.6mm 3mm">
<div class="trap">${ck}<span><b>“Nhiệt truyền từ vật nhiều nhiệt năng hơn.”</b> Chiều truyền do <b>nhiệt độ</b> quyết định.</span></div>
<div class="trap">${ck}<span><b>“${dC('0')} là ${dK('0')}.”</b> Hai thang khác gốc; “${dC('20')} gấp đôi ${dC('10')}” vô nghĩa, so tỉ số phải đổi ra K.</span></div>
<div class="trap">${ck}<span><b>“Đổi thang chỉ cần cộng trừ.”</b> 100 độ chia Celsius ứng 180 độ chia Fahrenheit; khoảng chênh không cộng 273, không cộng 32.</span></div>
</div>
${h3(4, 'IV · Trả bài 6 câu', '4·4')}
${box(`${tb('1. Nhiệt độ cho biết gì? Nhiệt năng truyền theo chiều nào?')}${lines(1)}
${tb('2. Hai mốc của thang Celsius? Khoảng giữa chia thế nào?')}${lines(1)}
${tb('3. Độ không tuyệt đối bằng bao nhiêu °C? Nhiệt độ điểm ba của nước?')}${lines(1)}
${tb('4. Công thức đổi °C ↔ K và °C ↔ °F. Vì sao không viết “°K”?')}${lines(1)}
${tb('5. Khoảng chênh 10 °C bằng bao nhiêu K, bao nhiêu °F? Vì sao khác nhau?')}${lines(1)}
${tb('6. Kể tên các loại nhiệt kế và tính chất mỗi loại dựa vào.')}${lines(1)}`)}
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('TỰ KIỂM TRA · BÀI TOÁN MẪU · THỬ THÁCH')}
${h3(1, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '5·1')}
${rkHai([1, 2, 3, 4], [5, 6, 7, 8])}
${h3(2, 'V · Bài toán mẫu: lò nướng bánh ghi 392 °F', '5·2')}
<div class="fig-side" style="${fs(34)}"><div class="card soft" style="padding:1.2mm 3mm;margin:0">Lò nướng đặt ở ${dC('200')}; mặt số chia theo thang Fahrenheit hiện ${dF('392')}. Nhiệt độ nướng hợp lí ${dC('180')} đến ${dC('220')}. Nướng xong, khay bánh nguội trong bếp ở ${dC('30')}. ${dung2}<br>
<b>a)</b> ${dF('392')} có đúng bằng ${dC('200')} không?<br><b>b)</b> đổi khoảng nhiệt độ nướng ra ${oF}<br>
<b>c)</b> khay nguội từ ${dC('200')} xuống ${dC('30')}: độ giảm bao nhiêu ${oC}, K, ${oF}?<br><b>d)</b> ${dC('30')} là bao nhiêu K?</div>
${H.loNuong()}</div>
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm;margin-top:1mm">
${wl('a)', 1)}${wl('b)', 2)}${wl(`c) giá trị hay khoảng chênh? ${m('\\Delta t=')}`, 2)}${wl('d)', 1)}</div>
${K.btvn().replace('<i>1</i>', '<i>3</i>')}
${h3(4, 'Thử thách phân tầng', '5·4')}
${box(wl(`${m('\\bigstar')} Nước đá đang tan ở ${dC('0')}. Đổi sang K và ${oF}.`, 1)
 + cau(`${m('\\bigstar\\bigstar')} Vì sao công thức chất khí dùng kelvin mà không dùng độ C?`, 1)
 + cau(`${m('\\bigstar\\bigstar\\bigstar')} Nhiệt kế hồng ngoại đo trán được ${dC('36{,}5')}, nhưng bắn vào mảnh giấy bạc dán trên trán chỉ được ${dC('30')}. Vì sao?`, 1))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Chiều truyền nhiệt năng và cân bằng nhiệt',
    de: `Bi thép nhỏ ở ${dC('120')} thả vào bể nước rất lớn ở ${dC('25')} (bể có nhiều nhiệt năng hơn bi).<br><b>a)</b> viên bi nóng hơn nước bao nhiêu độ<br><b>b)</b> nhiệt năng truyền theo chiều nào<br><b>c)</b> truyền nhiệt dừng khi nào; lúc đó hai vật ở trạng thái gì`,
    nd: `Chiều truyền do ${f(20)} quyết định, không do lượng nhiệt năng hay khối lượng`, a: ['a', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'], gi: 3, fig: H.trongBe('Bể lớn, cách nhiệt.') },
  { t: 'Dạng 2 · Dễ · Đổi giữa thang Celsius và thang Kelvin',
    de: `Dùng ${cK} (${m('T')} tính bằng K, ${m('t')} bằng ${oC}).<br><b>a)</b> thân nhiệt ${dC('37')} theo K; <b>b)</b> heli sôi ở ${dK('4{,}22')} theo ${oC}<br><b>c)</b> thuỷ ngân đông đặc ở ${dC('-39')} theo K<br><b>d)</b> bạn báo đo được ${dC('-300')}: có đáng tin không, vì sao`,
    nd: `${oC} → K: ${f(16)}; K → ${oC}: ${f(16)}; kelvin không bao giờ ${f(12)}`, a: ['a', 'b', 'c', 'd'], gi: 4 },
  { t: 'Dạng 3 · Trung bình · Đổi giữa ba thang Celsius, Kelvin, Fahrenheit',
    de: `${dung2}<br><b>a)</b> công thức bánh của Mỹ ghi nướng ở ${dF('374')}: tính theo ${oC}<br><b>b)</b> nhiệt kế y tế hiện ${dF('98{,}6')}: thân nhiệt theo ${oC}, rồi theo K<br><b>c)</b> phòng thí nghiệm ghi nhiệt độ phòng ${dK('293')}: tính theo ${oF}`,
    nd: `${oF} → ${oC}: trừ ${f(10)} rồi chia ${f(10)}; K ↔ ${oF} phải đi qua ${f(10)}`, a: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], gi: 3 },
  { t: 'Dạng 4 · Trung bình · Khoảng chênh nhiệt độ trên ba thang',
    de: `Hà Nội một ngày: thấp nhất ${dC('17')}, cao nhất ${dC('29')}. ${dung2}<br><b>a)</b> chênh lệch cao nhất – thấp nhất theo ${oC}<br><b>b)</b> chênh lệch đó theo K và theo ${oF}<br><b>c)</b> bạn An lấy kết quả câu a cộng thêm 273 để ra kelvin: chỉ ra chỗ sai`,
    nd: `${nw(`${m('\\Delta T=')} ${f(12)}`)}; ${nw(`${m('\\Delta t_F=')} ${f(14)}`)}; không cộng ${f(10)}, ${f(10)}`, a: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], gi: 3 },
  { t: 'Dạng 5 · Khó · So sánh nhiệt độ khác thang, chiều truyền nhiệt',
    de: `Ba vật tiếp xúc nhau, cách nhiệt với bên ngoài: A chỉ ${dF('68')}, B chỉ ${dK('293')}, C chỉ ${dC('25')}.<br><b>a)</b> đổi nhiệt độ vật A và vật B về ${oC} ${dung3}<br><b>b)</b> xếp ba vật theo nhiệt độ tăng dần<br><b>c)</b> cặp vật nào không trao đổi nhiệt với nhau ngay từ đầu<br><b>d)</b> nhiệt năng truyền từ vật nào sang vật nào`,
    nd: `Đổi về cùng ${f(12)}; bằng nhau thì ${f(18)}; khác: từ ${f(10)} sang ${f(10)}`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c', 'd'], cot: 5, gi: 4, fig: H.baVat() },
  { t: 'Dạng 6 · Nâng cao · Lập phương trình giữa hai thang',
    de: `Dùng ${cF} (${m('t')}: số đọc ${oC}) và ${cK}.<br><b>a)</b> ở nhiệt độ nào số đọc ${oF} gấp đôi số đọc ${oC}<br><b>b)</b> ở nhiệt độ nào hai thang ${oF} và ${oC} cho cùng một số đọc<br><b>c)</b> ở nhiệt độ nào (tính theo K) số đọc ${oC} bằng một nửa số đọc K`,
    nd: `Viết cả hai số đọc theo cùng một ẩn: “${oF} gấp đôi ${oC}” ⇒ ${nw(`${f(22)} = 2t`)}`, a: ['a', 'b', 'c'], gi: 3 },
];

// Bài tương tự: mỗi dạng 2 bài, giải vào vở (thầy chốt 10/11), ô đáp số cuối dòng của ý; đáp số tính bằng Python 12/11/2026.
const oY = (s, o, w = {}) => s.split('<br>').map((p) => {
  const ys = [...p.matchAll(/<b>([a-d])\)<\/b>/g)].map((x) => x[1]);
  if (!/^<b>[a-d]\)<\/b>/.test(p)) return `<div>${p}</div>`;
  const ls = o.filter((l) => ys.includes(l[0]));
  return `<div class="yo"><span>${p}</span><span class="oo">${ls.map((l) => `<span class="nw"><b>${l})</b>${f(typeof w === 'object' ? (w[l] ?? 25) : w)}</span>`).join('')}</span></div>`;
}).join('');
const ttDe = (b) => b.fig ? `<div class="fig-side" style="grid-template-columns:1fr ${b.fw}mm">${`<div>${oY(b.de, b.o, b.ow)}</div>`}${b.fig}</div>` : oY(b.de, b.o, b.ow);
const vaoVo = (ds) => ds.map((b) => (b.o ? { t: b.t, de: ttDe(b), k: 0 } : b));
const nhap = (n) => ({ t: '<span class="nhap-t">Nháp / chỗ em còn vướng</span>', de: lines(n), k: 0 });
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–3', 'DẠNG 4–6'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Thả cục nước đá ở ${dC('-10')} vào cốc nước ${dC('30')}; cốc cách nhiệt với bên ngoài.<br><b>a)</b> nước nóng hơn nước đá bao nhiêu độ<br><b>b)</b> nhiệt năng truyền theo chiều nào<br><b>c)</b> truyền nhiệt dừng khi nào; lúc đó hai vật ở trạng thái gì`, o: ['a', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'], ow: { a: 16, b: 32, 'c<sub>1</sub>': 30, 'c<sub>2</sub>': 28 } },
    { t: 'Dạng 1 · Bài 2', de: `Viên sỏi ${dC('15')} đặt lên tảng băng lớn ${dC('-5')} trong thùng cách nhiệt. Bình nói: “Băng nhiều nhiệt năng hơn nên nhiệt truyền từ băng sang sỏi.”<br><b>a)</b> sỏi và băng chênh nhau bao nhiêu độ<br><b>b)</b> nhiệt năng thật sự truyền theo chiều nào<br><b>c)</b> Bình sai ở đâu`, fig: H.trongBe('Thùng cách nhiệt.', 'sỏi 15 °C', 'băng −5 °C'), fw: 32, o: ['a', 'b', 'c'], ow: { a: 16, b: 34, c: 40 } },
    { t: 'Dạng 2 · Bài 1', de: `Dùng ${cK}.<br><b>a)</b> nước sôi ở ${dC('100')} theo K<br><b>b)</b> nitơ lỏng sôi ở ${dK('77')} theo ${oC}<br><b>c)</b> nhiệt độ thấp nhất đo được ở Nam Cực ${dC('-89')} theo K<br><b>d)</b> bạn báo đo được ${dC('-280')}: có đáng tin không`, o: ['a', 'b', 'c', 'd'], ow: { d: 34 } },
    { t: 'Dạng 2 · Bài 2', de: `Dùng ${cK}.<br><b>a)</b> bề mặt Mặt Trời khoảng ${dK('5800')} theo ${oC}<br><b>b)</b> phòng học ${dC('27')} theo K<br><b>c)</b> ôxi lỏng sôi ở ${dC('-183')} theo K<br><b>d)</b> nhiệt độ thấp nhất có thể có, tính theo ${oC} (làm tròn)`, o: ['a', 'b', 'c', 'd'] },
    { t: 'Dạng 3 · Bài 1', de: `${dung2}<br><b>a)</b> lò nướng đặt ${dF('356')}: tính theo ${oC}<br><b>b)</b> nhiệt kế y tế hiện ${dF('100{,}4')}: thân nhiệt theo ${oC}, rồi theo K<br><b>c)</b> ngăn đá tủ lạnh ${dK('263')}: tính theo ${oF}`, o: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], ow: 20 },
    { t: 'Dạng 3 · Bài 2', de: `${dung2}<br><b>a)</b> nước hồ bơi ${dF('86')}: tính theo ${oC}<br><b>b)</b> một đêm mùa đông ở Canada ${dF('-4')}: tính theo ${oC}, rồi theo K<br><b>c)</b> nước ấm pha trà ${dK('353')}: tính theo ${oF}`, o: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], ow: 20 },
  ], [
    { t: 'Dạng 4 · Bài 1', de: `Sa mạc: ngày ${dC('45')}, đêm ${dC('5')}. ${dung2}<br><b>a)</b> chênh lệch theo ${oC}; <b>b)</b> theo K; <b>c)</b> ${nw(`theo ${oF}`)}<br><b>d)</b> bạn Hoa tính ${m('1{,}8\\cdot40+32=104')} ${oF} cho câu c: sai ở đâu`, o: ['a', 'b', 'c', 'd'], ow: { a: 16, b: 16, c: 16, d: 40 } },
    { t: 'Dạng 4 · Bài 2', de: `Đun ấm nước từ ${dC('25')} đến ${dC('100')}. ${dung2}<br><b>a)</b> nhiệt độ tăng bao nhiêu ${oC}<br><b>b)</b> tăng bao nhiêu K<br><b>c)</b> tăng bao nhiêu ${oF}<br><b>d)</b> đổi riêng ${dC('25')} và ${dC('100')} ra ${oF} để kiểm câu c`, o: ['a', 'b', 'c', 'd<sub>1</sub>', 'd<sub>2</sub>'], ow: 18 },
    { t: 'Dạng 5 · Bài 1', de: `Ba vật tiếp xúc, cách nhiệt: A chỉ ${dF('50')}, B chỉ ${dK('283')}, C chỉ ${dC('5')}.<br><b>a)</b> đổi A, B về ${oC} ${dung3}<br><b>b)</b> xếp ba vật theo nhiệt độ tăng dần<br><b>c)</b> cặp nào không trao đổi nhiệt ngay từ đầu<br><b>d)</b> nhiệt năng truyền từ vật nào sang vật nào`, fig: H.baVat('Ba nhiệt kế khác thang.', ['50 °F', '283 K', '5 °C']), fw: 30, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c', 'd'], ow: { 'a<sub>1</sub>': 14, 'a<sub>2</sub>': 14, b: 28, c: 22, d: 36 } },
    { t: 'Dạng 5 · Bài 2', de: `Ba vật tiếp xúc, cách nhiệt: A chỉ ${dF('77')}, B chỉ ${dK('300')}, C chỉ ${dC('26')}.<br><b>a)</b> đổi A, B về ${oC} ${dung3}<br><b>b)</b> xếp ba vật theo nhiệt độ tăng dần<br><b>c)</b> có cặp nào cân bằng nhiệt không<br><b>d)</b> vật nào nhận nhiệt năng từ cả hai vật kia`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c', 'd'], ow: { 'a<sub>1</sub>': 14, 'a<sub>2</sub>': 14, b: 28, c: 18, d: 14 } },
    { t: 'Dạng 6 · Bài 1', de: `Dùng ${cF} và ${cK}.<br><b>a)</b> ở nhiệt độ nào số đọc ${oF} gấp ba số đọc ${oC} (tính theo ${oC})<br><b>b)</b> ở nhiệt độ nào số đọc ${oF} lớn hơn số đọc ${oC} đúng 40<br><b>c)</b> ở nhiệt độ nào (theo K) số đọc K gấp ba số đọc ${oC}`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 6 · Bài 2', de: `Dùng ${cF} và ${cK}.<br><b>a)</b> ở nhiệt độ nào số đọc ${oF} bằng một nửa số đọc ${oC} (tính theo ${oC})<br><b>b)</b> ở nhiệt độ nào số đọc ${oF} gấp năm số đọc ${oC}<br><b>c)</b> ở nhiệt độ nào (theo K) số đọc K gấp đôi số đọc ${oF}`, o: ['a', 'b', 'c'] },
  ]],
  dap: [
    `D1·1: a) 40 °C · b) từ nước sang nước đá · c<sub>1</sub>) khi hai nhiệt độ bằng nhau · c<sub>2</sub>) cân bằng nhiệt &nbsp;|&nbsp; D1·2: a) 20 °C · b) từ sỏi sang băng · c) chiều truyền do nhiệt độ, không do nhiệt năng &nbsp;|&nbsp; D2·1: a) 373 K · b) −196 °C · c) 184 K · d) không (ra −7 K) &nbsp;|&nbsp; D2·2: a) 5527 °C · b) 300 K · c) 90 K · d) −273 °C &nbsp;|&nbsp; D3·1: a) 180 °C · b<sub>1</sub>) 38 °C · b<sub>2</sub>) 311 K · c) 14 °F &nbsp;|&nbsp; D3·2: a) 30 °C · b<sub>1</sub>) −20 °C · b<sub>2</sub>) 253 K · c) 176 °F`,
    `D4·1: a) 40 °C · b) 40 K · c) 72 °F · d) cộng 32 vào khoảng chênh &nbsp;|&nbsp; D4·2: a) 75 °C · b) 75 K · c) 135 °F · d<sub>1</sub>) 77 °F · d<sub>2</sub>) 212 °F &nbsp;|&nbsp; D5·1: a<sub>1</sub>) 10 °C · a<sub>2</sub>) 10 °C · b) C &lt; A = B · c) A và B · d) từ A và B sang C &nbsp;|&nbsp; D5·2: a<sub>1</sub>) 25 °C · a<sub>2</sub>) 27 °C · b) A &lt; C &lt; B · c) không · d) A &nbsp;|&nbsp; D6·1: a) ≈ 26,7 °C · b) 10 °C · c) 409,5 K &nbsp;|&nbsp; D6·2: a) ≈ −24,6 °C · b) 10 °C · c) ≈ 353,4 K`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 3], kq: [[1, 2, 3], [4, 5, 6]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'cân bằng nhiệt 1·4 · Celsius 2·1 · hai mốc 2·2 · Kelvin 3·1 · Fahrenheit 3·2 · bảng đổi 3·3 · nhiệt kế 4·2 · bẫy 4·3 · bài toán mẫu 5·2 · dạng 1–3 → 6·1 · dạng 4–6 → 7·1',
  out: process.argv[2],
});
