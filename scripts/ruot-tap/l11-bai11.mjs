// Ruột tập VL11 – Bài 11 · Sóng điện từ (lesson id 30). Quyển Chương 2 lớp 11 (Sóng): bài 8 = tr. 1–12 … bài 11 = tr. 37–48.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự giải vào vở · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l11-bai11.mjs (toàn bộ SVG tự vẽ). Nội dung theo bài web (book/cache/30.json, tải từ DB 13/11/2026):
// mục tiêu, dự đoán vệ tinh, II.1–II.5 (E ⊥ B, c và λ = c/f, đo c bằng lò vi sóng, thang sóng điện từ, truyền thông/ra-đa),
// ba bẫy, Trả bài 6 câu, bài toán mẫu nhà Minh, thử thách phân tầng, 4 dạng bài tập mẫu. Đáp số tính bằng Python 13/11/2026.
// Chạy: node scripts/ruot-tap/l11-bai11.mjs [file.pdf]     → scripts/ruot-tap/out/ruot-tap-vl11-bai11.pdf
//       node scripts/ruot-tap/l11-bai11.mjs --hinh         → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l11-bai11/
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL11b11 as H } from './hinh-l11-bai11.mjs';

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
  const out = resolve(HERE, 'out/hinh-l11-bai11'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 11, lid: 30, ten: 'SÓNG ĐIỆN TỪ', lop: 11, baiDau: 8, sub: 'Vật lí 11 · Chương 2: Sóng' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const E = m('\\vec E'), B = m('\\vec B'), la = m('\\lambda'), fq = m('f'), c = m('c');
const pw = (a, b) => m(`${a}\\cdot10^{${b}}`);
const ms = (s) => nw(`${s} m/s`);
const fq9 = '<span class="fill" style="min-width:16mm;height:9mm"></span>'; // ô phân số cao 9 mm (lỗi lặp HS ảo)

const css = '<style>.bt .ans .fill{height:9mm}.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:6mm}.tt:has(.nhap-t) .hd>span+span{display:none}.vung td{height:5.6mm}</style>';

const p1 = `${css}<section class="page">
${head('BÀI 11 · SÓNG ĐIỆN TỪ', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Nêu trong sóng điện từ cái gì dao động, ${E} và ${B} nằm theo phương nào`)}
${dong(`${ck}Tính ${la} từ ${fq} và ngược lại; đổi đúng kHz, MHz, GHz, nm`)}
${dong(`${ck}Xếp bảy vùng thang sóng điện từ, nêu một ứng dụng mỗi vùng`)}
${dong(`${ck}Giải thích wifi, 4G, vệ tinh, ra-đa gửi tin và đo khoảng cách thế nào`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Giữa vệ tinh và mặt đất là hàng chục nghìn km gần như chân không. Tín hiệu vẫn tới chảo thu vì:</p>
<div class="fig-side" style="${fs(42)}"><div>
${opt('A', 'Tín hiệu đi theo lớp khí loãng còn sót ngoài vũ trụ')}
${opt('B', 'Vệ tinh nối với mặt đất bằng một sợi cáp dài')}
${opt('C', 'Sóng mang tín hiệu không cần môi trường vật chất')}
${opt('D', 'Đó là sóng âm tần số rất cao, xuyên được chân không')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 2)}</div>
${H.veTinh()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f(12)} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Sóng điện từ là gì?', '1·4')}
<div class="card" style="padding:1.2mm 3mm">
<div><b>Faraday:</b> từ trường biến thiên (thay đổi theo thời gian) sinh ra ${f(30)} (gây dòng điện cảm ứng).</div>
<div><b>Maxwell:</b> điện trường biến thiên cũng sinh ra ${f(30)}.</div>
<div>Hai trường sinh ra nhau liên tiếp nên lan đi thành ${f(35)}.</div>
<div><b>Sóng điện từ:</b> điện từ trường biến thiên ${f(28)} (lặp lại sau những khoảng thời gian bằng nhau), lan truyền trong ${f(28)}.</div>
<div><b>Nguồn phát:</b> vật tạo ra điện trường hay từ trường ${f(25)}; ví dụ ${nw(`${f(25)},`)} ${f(25)}.</div>
<div><b>Ví dụ:</b> radio đang bắt đài AM, bật – tắt công tắc đèn cạnh đó thì loa kêu “rẹt”, vì tia lửa điện ở công tắc ${f(40)}.</div>
${wl('Nói lại bằng lời của em: vì sao điện trường và từ trường lan đi được thành sóng?', 2)}</div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('E VÀ B · TRUYỀN TRONG CHÂN KHÔNG · BƯỚC SÓNG')}
${h3(1, `II.1 · Hướng của ${E} và ${B}`, '2·1')}
<div class="card fig-side" style="${fs(44)};padding:1.2mm 3mm"><div>
<div>${E}: vectơ cường độ điện trường · ${B}: vectơ cảm ứng từ.</div>
<div>Tại mỗi điểm: ${E} ${f(25)} ${B}; cả hai ${f(25)} phương truyền ${m('\\Rightarrow')} sóng điện từ là sóng ${f(25)}.</div>
<div>${E} và ${B} dao động cùng ${f(25)}, cùng ${f(25)}. Sóng mang ${f(25)} (nắng làm da nóng).</div>
<div style="margin-top:.8mm"><b>Làm nhanh.</b> Sóng từ vệ tinh truyền thẳng đứng xuống mặt đất. Tại một điểm, ${E} nằm ngang theo hướng Đông – Tây. ${B} tại đó theo phương: ${f(30)}</div>
${wl('<span class="hint" style="font-weight:400">Vì sao (dùng đủ hai điều kiện)?</span>', 2)}</div>
${H.eb()}</div>
${h3(2, `II.2 · Truyền cả trong chân không; ${m('\\lambda=c/f')}`, '2·2')}
<div class="card" style="padding:1.2mm 3mm">
<div>Truyền trong rắn, lỏng, khí và cả ${f(25)}; sóng cơ thì ${f(25)}.</div>
<div>Trong chân không mọi sóng điện từ cùng tốc độ ${nw(`${m('c=')} ${f(22)} m/s`)}, bằng tốc độ ${f(25)} ${m('\\Rightarrow')} ánh sáng là ${f(25)}.</div>
<div>Trong nước, thuỷ tinh: tốc độ ${m('v')} ${f(25)} ${c}. Đổi môi trường: giữ nguyên ${f(25)}; đổi ${f(25)}.</div>
<div>Cũng truyền thẳng, phản xạ, ${f(25)}, nhiễu xạ, giao thoa như sóng cơ.</div>
<div style="margin-top:.6mm">Chân không: ${nw(`${m('\\lambda=')} ${fq9} ${m('=')} ${f(16)}`)} &nbsp;·&nbsp; môi trường tốc độ ${m('v')}: ${nw(`${m('\\lambda=')} ${fq9}`)} &nbsp;·&nbsp; ${la} (m), ${fq} (Hz), ${m('T')} (s)</div>
<div class="hint" style="margin:.4mm 0">Đổi: 1 kHz = ${m('10^{3}')} Hz · 1 MHz = ${m('10^{6}')} Hz · 1 GHz = ${m('10^{9}')} Hz · 1 nm = ${m('10^{-9}')} m</div>
<div><b>Ví dụ 1:</b> sóng 4G ${nw('900 MHz')}: ${nw(`${la} = ${f(16)} m`)} &nbsp;·&nbsp; <b>Ví dụ 2:</b> ăng ten thu sóng ${nw(`${m('\\lambda=3')} m`)}: ${nw(`${fq} = ${f(14)} MHz`)}</div>
<div><b>Ví dụ 3:</b> ánh sáng ${nw('600 nm')} (chân không) đi vào thuỷ tinh có ${nw(`${m('v=2\\cdot10^{8}')} m/s`)}: ${nw(`${fq} = ${f(22)} Hz`)} (giữ nguyên), ${nw(`${m("\\lambda'=")} ${f(14)} nm`)}</div></div>
${h3(3, 'Thí nghiệm: điện thoại trong hộp giấy và hộp sắt', '2·3')}
<div class="card" style="padding:1.2mm 3mm">
<div><b>Làm:</b> đặt máy A vào hộp giấy đậy nắp, dùng máy B gọi vào; chuyển A sang hộp bánh quy bằng sắt đậy kín, gọi lại.</div>
<div><b>Quan sát:</b> hộp giấy: ${f(30)} · hộp sắt: ${f(30)}</div>
<div><b>Rút ra:</b> vỏ kim loại kín (lồng Faraday) ${f(25)} gần hết sóng.</div>
${wl('Vì sao vào thang máy thì cuộc gọi video đứng hình?', 2)}</div>
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('ĐO TỐC ĐỘ SÓNG · THANG SÓNG ĐIỆN TỪ')}
${h3(1, 'II.3 · Thí nghiệm đo c bằng lò vi sóng', '3·1')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div><b>Làm:</b> nhấc đĩa xoay ra để thanh sô-cô-la không quay, bật lò ${nw('15–20 s')}, đo ${m('d')}; làm 5 lần. Lò phát ${nw(`${m('f=2{,}45')} GHz`)}.</div>
<table style="margin:.6mm 0"><tr><th>Lần</th><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><th>TB</th></tr>
<tr><th>${m('d')} (cm)</th><td>6,0</td><td>6,2</td><td>5,9</td><td>6,3</td><td>6,1</td><td style="width:13mm"></td></tr></table>
<div>Hai vệt chảy liền nhau cách nhau ${nw(`${m('d=')} ${f(12)}`)} (nửa bước sóng) ${m('\\Rightarrow')} ${nw(`${la} = ${f(18)} m`)}</div>
<div>${nw(`${m('c=\\lambda f=')} ${f(28)} m/s`)}; khớp tốc độ ánh sáng.</div>
<div>Sai số do: ${f(48)}</div>
<div class="hint"><b>An toàn:</b> không bật lò trống, không cho kim loại vào lò; sô-cô-la chảy rất nóng.</div></div>
${H.soCoLa()}</div>
${h3(2, 'II.4 · Thang sóng điện từ', '3·2')}
<div class="card fig-side" style="${fs(38)};padding:1.2mm 3mm"><div>
<div>Mọi vùng cùng bản chất, chỉ khác ${f(25)}, nên khác tính chất, công dụng. Xếp ${la} giảm dần:</div>
<div class="hint">1 ${m('\\mu')}m = ${m('10^{-6}')} m · 1 nm = ${m('10^{-9}')} m · 1 pm = ${m('10^{-12}')} m</div>
<table class="vung" style="margin:.6mm 0"><tr><th style="width:27mm">Vùng</th><th style="width:30mm">Bước sóng</th><th>Dùng làm gì</th></tr>
<tr><td>Sóng vô tuyến</td><td>1 m – 100 km</td><td></td></tr><tr><td>Vi sóng</td><td></td><td></td></tr><tr><td>Hồng ngoại</td><td></td><td></td></tr>
<tr><td>Nhìn thấy</td><td></td><td></td></tr><tr><td>Tử ngoại</td><td></td><td></td></tr><tr><td>Tia X</td><td></td><td></td></tr><tr><td>Tia gamma</td><td></td><td></td></tr></table>
<div>Trong ánh sáng nhìn thấy: ánh sáng ${f(25)} dài nhất ${nw('(760 nm)')}, ánh sáng ${f(25)} ngắn nhất ${nw('(380 nm)')}.</div>
<div><b>Thí nghiệm:</b> bấm giữ nút điều khiển ti vi, nhìn đầu điều khiển bằng mắt rồi qua camera điện thoại. Mắt thấy: ${f(25)} · camera thấy: ${f(25)}</div>
<div>Đó là ${f(25)} (${nw(`${m('\\lambda\\approx940')} nm`)}), dài hơn ánh sáng ${f(25)} nên mắt không thấy.</div>
<div><b>Làm nhanh:</b> bức xạ ${nw(`${m('f=1{,}0\\cdot10^{15}')} Hz`)} trong chân không: ${nw(`${la} = ${f(16)} nm`)}, thuộc vùng ${f(25)}</div></div>
${H.thang()}</div>
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('TRUYỀN THÔNG · BA CÁI BẪY · TRẢ BÀI')}
${h3(1, 'II.5 · Sóng điện từ trong truyền thông', '4·1')}
<div class="card fig-side" style="${fs(32)};padding:1.2mm 3mm"><div>
<div>Liên lạc dùng chủ yếu sóng ${f(25)} (gồm vi sóng): AM, FM, 4G, wifi, GPS, vệ tinh.</div>
<div><b>Phát:</b> sóng mang là sóng điện từ ${f(25)}; tín hiệu làm biên độ (AM) hay tần số (FM) của nó đổi theo: ${f(25)}.</div>
<div><b>Thu:</b> ${f(25)} nhận, máy tách tín hiệu. <b>Vệ tinh địa tĩnh</b> đứng yên với mặt đất, nhận rồi ${f(25)}.</div>
<div><b>Ra-đa:</b> đường đi – về bằng ${f(12)}; khoảng cách ${nw(`${m('d=')} ${fq9}`)}</div></div>
${H.raDa('Xung đi tới máy bay rồi về; t tính từ lúc phát đến lúc thu.')}</div>
${h3(2, 'III · Ba cái bẫy hay sập', '4·2')}
<div class="card" style="padding:.8mm 3mm">
<div class="trap">${ck}<span><b>“Cần không khí.”</b> Trên Mặt Trăng vẫn nói chuyện được qua ${f(25)}.</span></div>
<div class="trap">${ck}<span><b>“Tần số lớn thì nhanh.”</b> Chân không: mọi sóng cùng tốc độ ${c}; ${m('f')} lớn thì ${la} ${f(25)}.</span></div>
<div class="trap">${ck}<span><b>“Wifi là sóng âm.”</b> Máy ${m('\\to')} loa: sóng ${f(25)}; loa ${m('\\to')} tai: sóng ${f(25)}.</span></div></div>
${h3(3, 'IV · Trả bài 6 câu', '4·3')}
${box(`${tb('1. Sóng điện từ là gì? Nguồn phát là gì?')}${lines(1)}
${tb(`2. ${E}, ${B} và phương truyền nằm thế nào? Pha của ${E} và ${B}?`)}${lines(1)}
${tb('3. Tốc độ sóng điện từ trong chân không? Khác sóng cơ ở đâu?')}${lines(1)}
<div><b>4. Công thức bước sóng, kèm đơn vị:</b> ${f(45)}<span class="ck" style="float:right;margin:0"></span></div>
${tb('5. Kể bảy vùng thang sóng điện từ theo bước sóng giảm dần.')}${lines(2)}
<div><b>6. Đổi môi trường:</b> giữ nguyên ${f(30)} · đổi ${f(30)}<span class="ck" style="float:right;margin:0"></span></div>`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/6 câu · chưa thuộc: ${f(25)} ${nw(`${m('\\to')} đọc lại ô ${f(12)} Tập`)}</div>
${h3(4, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '4·4')}
${rkHai([1, 2, 3, 4], [5, 6, 7])}
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TOÁN MẪU · BÀI TẬP VỀ NHÀ · THỬ THÁCH')}
${h3(1, 'V · Bài toán mẫu: nhà Minh', '5·1')}
<div class="card soft" style="padding:1.2mm 3mm">Nhà Minh có radio bắt đài FM ${nw('100 MHz')}, bộ phát wifi hai băng ${nw('2,4 GHz')} và ${nw('5 GHz')}, xem truyền hình qua vệ tinh địa tĩnh cao ${nw('36 000 km')}. Lấy ${nw(`${m('c=3\\cdot10^{8}')} m/s`)}.
<div><b>a)</b> Tính bước sóng của đài FM. &nbsp;<b>b)</b> Tính bước sóng hai băng wifi. Băng nào ngắn hơn, mấy lần?</div>
<div><b>c)</b> Tín hiệu đi thẳng từ vệ tinh xuống chảo thu ngay bên dưới mất bao lâu?</div></div>
<div class="fig-side" style="${fs(40)};margin-top:.8mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl(`a) đổi ${m('f_1')} ra Hz, ${m('\\lambda_1=')}`, 2)}${wl(`b) ${m('\\lambda_2=')} &nbsp; ${m('\\lambda_3=')} &nbsp; tỉ số:`, 3)}${wl(`c) đổi km ra m, ${m('t=s/c=')}`, 2)}</div>${H.nhaMinh()}</div>
${h3(2, 'Điền bước còn thiếu: gọi điện qua vệ tinh', '5·2')}
<div class="fig-side" style="${fs(40)}"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:.6mm 3mm">
<div style="line-height:1.35">Tiếng nói đi từ trạm A lên vệ tinh rồi xuống trạm B, mỗi chặng ${nw('36 000 km')}.</div>
<div class="ln" style="height:7mm"><b>Bước 1:</b> ${nw(`${m('s=2\\times3{,}6\\cdot10^{7}=')} ${f(20)} m`)}</div>
<div class="ln" style="height:7mm"><b>Bước 2:</b> thời gian tiếng tới B: ${nw(`${m('t=s/c=')} ${f(14)} s`)}</div>
<div class="ln" style="height:7mm"><b>Bước 3:</b> B đáp ngay; A nghe câu trả lời sau ít nhất ${nw(`${f(14)} s`)}</div></div>${H.abVeTinh()}</div>
${K.btvn().replace('<i>1</i>', '<i>3</i>')}
${h3(4, 'Thử thách phân tầng', '5·4')}
${box(wl(`${m('\\bigstar')} Sóng 4G tần số ${nw('1 800 MHz')} có bước sóng bao nhiêu?`, 1)
 + wl(`${m('\\bigstar\\bigstar')} Mặt Trời cách Trái Đất ${nw(`${m('1{,}5\\cdot10^{8}')} km`)}. Ánh sáng đi tới mất bao lâu?`, 1)
 + wl(`${m('\\bigstar\\bigstar\\bigstar')} Thời gian sóng từ vệ tinh GPS tới máy thu đo lệch ${nw(`1 ${m('\\mu')}s`)} (${m('10^{-6}')} s) thì khoảng cách sai bao nhiêu? Vì sao GPS cần đồng hồ nguyên tử?`, 2))}
${h3(5, 'VI · Mang về: điều em dễ quên nhất', '5·5')}
${box(wl('1.', 1) + wl('2.', 1))}
${foot(5)}</section>`;

const dang = [
  { t: `Dạng 1 · Dễ · Tính bước sóng hoặc tần số (${m('\\lambda=c/f')})`,
    de: `Bộ đàm của đội cứu hộ phát sóng ${nw('150 MHz')}. Một trạm 4G phát sóng có bước sóng ${nw('15 cm')}. Coi không khí như chân không, ${nw(`${m('c=3\\cdot10^{8}')} m/s`)}.<br><b>a)</b> bước sóng của sóng bộ đàm<br><b>b)</b> tần số của sóng trạm 4G<br><b>c)</b> sóng nào có bước sóng dài hơn (c<sub>1</sub>), dài gấp mấy lần (c<sub>2</sub>)`,
    nd: `cho ${fq} tìm ${nw(`${la} = ${fq9}`)}, cho ${la} tìm ${nw(`${fq} = ${fq9}`)}; đổi ${f(16)} ra Hz, cm ra ${f(12)}`,
    a: ['a', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'], gi: 8, cot: 4 },
  { t: 'Dạng 2 · Trung bình · Xác định vùng của bức xạ trên thang sóng điện từ',
    de: `Hai bức xạ trong chân không: ${nw(`${m('f_1=6{,}0\\cdot10^{14}')} Hz`)} và ${nw(`${m('f_2=3{,}0\\cdot10^{12}')} Hz`)}; ${nw(`${m('c=3\\cdot10^{8}')} m/s`)}. Mắt nhìn thấy ${nw('380 nm')} đến ${nw('760 nm')}; hồng ngoại ${nw('760 nm')} đến ${nw('1 mm')}.<br><b>a)</b> bước sóng ${m('\\lambda_1')} (a<sub>1</sub>), ${m('\\lambda_2')} (a<sub>2</sub>)<br><b>b)</b> vùng của bức xạ 1 (b<sub>1</sub>), bức xạ 2 (b<sub>2</sub>)`,
    nd: `tính ${la} ra mét rồi đổi sang ${f(16)} để so với ${f(25)} của thang`,
    a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>'], gi: 8, cot: 4, fig: H.mocThang() },
  { t: 'Dạng 3 · Trung bình · Nhận định đúng hay sai về sóng điện từ',
    de: `Một sóng điện từ truyền thẳng đứng từ vệ tinh xuống mặt đất. Ghi Đ hoặc S cho mỗi ý.<br><b>a)</b> Sóng này cần có không khí làm môi trường truyền.<br><b>b)</b> Tại mỗi điểm ${E} và ${B} vuông góc với nhau và cùng vuông góc với phương truyền.<br><b>c)</b> Khi đi từ không khí vào thuỷ tinh, tần số của sóng giảm còn tốc độ truyền không đổi.<br><b>d)</b> Trong chân không, ánh sáng đỏ và ánh sáng tím truyền với cùng một tốc độ.`,
    nd: `xét từng ý: môi trường truyền, hướng ${E}, ${B}; đổi môi trường thì ${f(16)} giữ nguyên, ${f(25)} đổi`,
    a: ['a', 'b', 'c', 'd'], gi: 5, cot: 4 },
  { t: 'Dạng 4 · Khó · Ra-đa đo khoảng cách và tốc độ',
    de: `Ra-đa phát xung về phía một drone đang bay thẳng ra xa. Xung phản xạ thu lại sau ${nw(`${m('t_1=160')} ${m('\\mu')}s`)} kể từ lúc phát. Sau ${nw('30 s')}, đo lần hai: ${nw(`${m('t_2=164')} ${m('\\mu')}s`)}. ${nw(`${m('c=3\\cdot10^{8}')} m/s`)}; ${nw(`1 ${m('\\mu')}s = ${m('10^{-6}')} s`)}.<br><b>a)</b> khoảng cách ra-đa – drone lần 1 (a<sub>1</sub>), lần 2 (a<sub>2</sub>)<br><b>b)</b> tốc độ trung bình của drone`,
    nd: `sóng đi rồi về nên ${nw(`${m('d=')} ${fq9}`)}; ${nw(`${m('v=')} ${fq9}`)}`,
    a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b'], gi: 9, fig: H.drone() },
];

// Bài tương tự giải vào vở (thầy chốt 10/11): ô đáp số cuối đúng dòng của ý. Đáp số tính bằng Python 13/11/2026.
const oY = (s, o, w = 25) => s.split('<br>').map((p) => {
  const y = p.match(/^<b>([a-d])\)<\/b>/);
  if (!y) return `<div>${p}</div>`;
  const ls = o.filter((l) => (Array.isArray(l) ? l[0] : l)[0] === y[1]);
  return `<div class="yo"><span>${p}</span><span class="oo">${ls.map((l) => { const [n, wd] = Array.isArray(l) ? l : [l, w]; return `<span class="nw"><b>${n})</b>${f(wd)}</span>`; }).join('')}</span></div>`;
}).join('');
const ttDe = (b) => b.fig ? `<div class="fig-side" style="grid-template-columns:1fr ${b.fw}mm"><div>${oY(b.de, b.o, b.ow)}</div>${b.fig}</div>` : oY(b.de, b.o, b.ow);
const vaoVo = (ds) => ds.map((b) => (b.o ? { t: b.t, de: ttDe(b), k: 0 } : b));
const nhap = (n) => ({ t: '<span class="nhap-t">Nháp / chỗ em còn vướng</span>', de: lines(n), k: 0 });
const C8 = `${nw(`${m('c=3\\cdot10^{8}')} m/s`)}`;
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–2', 'DẠNG 3–4'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Đài FM phát sóng ${nw('90 MHz')}; bộ phát wifi phát sóng có bước sóng ${nw('12,5 cm')}. Coi không khí như chân không, ${C8}.<br><b>a)</b> bước sóng của đài FM (m)<br><b>b)</b> tần số của sóng wifi (GHz)<br><b>c)</b> sóng nào dài hơn, dài gấp mấy lần`, o: ['a', 'b', ['c<sub>1</sub>', 25], ['c<sub>2</sub>', 16]] },
    { t: 'Dạng 1 · Bài 2', de: `Đài AM phát sóng ${nw('750 kHz')}; lò vi sóng phát sóng có bước sóng ${nw('12 cm')}. ${C8}.<br><b>a)</b> bước sóng của đài AM (m)<br><b>b)</b> tần số của lò (GHz)<br><b>c)</b> sóng nào dài hơn, dài gấp mấy lần`, o: ['a', 'b', ['c<sub>1</sub>', 25], ['c<sub>2</sub>', 16]] },
    { t: 'Dạng 2 · Bài 1', de: `<div class="fig-side" style="grid-template-columns:1fr 50mm"><div>Hai bức xạ trong chân không: ${nw(`${m('f_1=1{,}5\\cdot10^{15}')} Hz`)}, ${nw(`${m('f_2=5\\cdot10^{9}')} Hz`)}; ${C8}. Dùng mốc thang ở hình bên.${oY('<b>a)</b> bước sóng mỗi bức xạ<br><b>b)</b> vùng của mỗi bức xạ', ['a<sub>1</sub>', 'a<sub>2</sub>', ['b<sub>1</sub>', 25], ['b<sub>2</sub>', 25]], 17)}</div>${H.mocThang('Mốc một số vùng (bước sóng trong chân không), dùng cho cả hai bài dạng 2.')}</div>`, o: null },
    { t: 'Dạng 2 · Bài 2', de: `Hai bức xạ trong chân không: ${nw(`${m('f_1=5\\cdot10^{14}')} Hz`)}, ${nw(`${m('f_2=1{,}5\\cdot10^{18}')} Hz`)}; ${C8}; ${nw(`1 pm = ${m('10^{-12}')} m`)}.<br><b>a)</b> bước sóng mỗi bức xạ (nm hoặc pm)<br><b>b)</b> vùng của mỗi bức xạ`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', ['b<sub>1</sub>', 25], ['b<sub>2</sub>', 25]], ow: 17 },
    nhap(4),
  ], [
    { t: 'Dạng 3 · Bài 1 · Ánh sáng Mặt Trời tới Trái Đất. Ghi Đ hoặc S.', de: `<b>a)</b> Sóng điện từ truyền được trong chân không.<br><b>b)</b> ${E} và ${B} dao động lệch pha nhau ${m('\\pi/2')}.<br><b>c)</b> Ánh sáng đi từ không khí vào nước thì bước sóng giảm.<br><b>d)</b> Trong chân không, tia X truyền nhanh hơn sóng FM.`, o: [['a', 12], ['b', 12], ['c', 12], ['d', 12]] },
    { t: 'Dạng 3 · Bài 2 · Điện thoại phát nhạc qua loa bluetooth. Ghi Đ hoặc S.', de: `<b>a)</b> Sóng bluetooth từ điện thoại tới loa là sóng cơ.<br><b>b)</b> Tiếng từ loa tới tai em là sóng âm.<br><b>c)</b> Sóng điện từ là sóng dọc.<br><b>d)</b> Sóng wifi ${nw('5 GHz')} có bước sóng ngắn hơn sóng wifi ${nw('2,4 GHz')}.`, o: [['a', 12], ['b', 12], ['c', 12], ['d', 12]] },
    { t: 'Dạng 4 · Bài 1', de: `<div class="fig-side" style="grid-template-columns:1fr 44mm"><div>Ra-đa thu xung phản xạ từ một máy bay sau ${nw(`${m('200')} ${m('\\mu')}s`)}; ${nw('20 s')} sau, sau ${nw(`${m('180')} ${m('\\mu')}s`)}. ${C8}; ${nw(`1 ${m('\\mu')}s = ${m('10^{-6}')} s`)}.${oY('<b>a)</b> khoảng cách lần 1, lần 2 (km)<br><b>b)</b> tốc độ trung bình máy bay; bay lại gần hay ra xa', ['a<sub>1</sub>', 'a<sub>2</sub>', ['b<sub>1</sub>', 18], ['b<sub>2</sub>', 25]], 18)}</div>${H.raDa('Xung đi tới máy bay rồi phản xạ về ra-đa.')}</div>`, o: null },
    { t: 'Dạng 4 · Bài 2', de: `Xung ra-đa phát từ Trái Đất tới Mặt Trăng, phản xạ về sau ${nw('2,56 s')}. ${C8}; ${nw(`1 ns = ${m('10^{-9}')} s`)}.<br><b>a)</b> khoảng cách Trái Đất – Mặt Trăng (km)<br><b>b)</b> nếu đo thời gian lệch ${nw('1 ns')} thì khoảng cách sai bao nhiêu (cm)`, o: [['a', 30], 'b'] },
    nhap(5),
  ]],
  dap: [
    `D1·1: a) ${m('\\approx3{,}33')} m · b) 2,4 GHz · c<sub>1</sub>) sóng FM · c<sub>2</sub>) ${m('\\approx26{,}7')} lần &nbsp;|&nbsp; D1·2: a) 400 m · b) 2,5 GHz · c<sub>1</sub>) sóng AM · c<sub>2</sub>) ${m('\\approx3333')} lần &nbsp;|&nbsp; D2·1: a<sub>1</sub>) 200 nm · a<sub>2</sub>) 6 cm · b<sub>1</sub>) tử ngoại · b<sub>2</sub>) vi sóng &nbsp;|&nbsp; D2·2: a<sub>1</sub>) 600 nm · a<sub>2</sub>) 200 pm (0,2 nm) · b<sub>1</sub>) nhìn thấy · b<sub>2</sub>) tia X`,
    `D3·1: a) Đ · b) S · c) Đ · d) S &nbsp;|&nbsp; D3·2: a) S · b) Đ · c) S · d) Đ &nbsp;|&nbsp; D4·1: a<sub>1</sub>) 30 km · a<sub>2</sub>) 27 km · b<sub>1</sub>) 150 m/s · b<sub>2</sub>) bay lại gần &nbsp;|&nbsp; D4·2: a) 384 000 km · b) 15 cm`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [2, 2], kq: [[1, 2], [3, 4]], khoNhat: true },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'định nghĩa 1·4 · E, B 2·1 · c, bước sóng 2·2 · lò vi sóng 3·1 · thang 3·2 · ra-đa 4·1 · bẫy 4·2 · bài mẫu 5·1 · dạng 1–2 6·1 · dạng 3–4 7·1',
  out: process.argv[2],
});
