// Ruột tập VL12 – Bài 1 · Sự chuyển thể (lesson id 2). Quyển Chương 1 lớp 12: bài 1 = tr. 1–12.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l12-bai1.mjs (toàn bộ SVG tự vẽ). Nội dung theo bài web (book/cache/2.json, tải từ DB 12/11/2026): mục tiêu, dự đoán
// li đá đang tan, II.1–II.5, thí nghiệm rượu + nước, đun nước đá mỗi phút, ba bẫy, Trả bài 6 câu, bài toán mẫu băng phiến,
// thử thách ⭐–⭐⭐⭐, 5 dạng bài tập mẫu. Đáp số Bài tương tự (tuongTu.dap) tính bằng Python 12/11/2026.
// Chạy: node scripts/ruot-tap/l12-bai1.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl12-bai1.pdf
//       node scripts/ruot-tap/l12-bai1.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l12-bai1/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL12b1 as H } from './hinh-l12-bai1.mjs';

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
  const out = resolve(HERE, 'out/hinh-l12-bai1'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 1, lid: 2, ten: 'SỰ CHUYỂN THỂ', lop: 12, baiDau: 1, sub: 'Vật lí 12 · Chương 1: Vật lí nhiệt' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const dC = (s) => nw(m(`${s}\\ ^\\circ\\mathrm C`));
const ph = (s) => nw(`${s} phút`);
const to = m('\\to');
// Bảng tra nhiệt độ nóng chảy in sẵn trong đề (dạng 3, 5 và bài tương tự)
const traNC = (ds) => `<b>Nhiệt độ nóng chảy:</b> ${ds.map(([c, v]) => nw(`${c} ${dC(v)}`)).join(' · ')}`;
// bảng t – T nằm ngang, một hoặc hai hàng
const bangTT = (ts, Ts) => `<table style="margin:.6mm 0;text-align:center;font-size:var(--fs-sm);line-height:1.3"><tr><th style="width:17mm;white-space:nowrap;padding:.2mm 1mm">${m('t')} (phút)</th>${ts.map((v) => `<td style="padding:.2mm .4mm">${v}</td>`).join('')}</tr>
<tr><th style="white-space:nowrap;padding:.2mm 1mm">${m('T')} (°C)</th>${Ts.map((v) => `<td style="padding:.2mm .4mm">${String(v).replace('-', '−')}</td>`).join('')}</tr></table>`;

// Bài tương tự 1 cột, ô đáp số cuối dòng của ý (cùng cách l11-bai16).
const ttCss = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';

const p1 = `${ttCss}<section class="page">
${head('BÀI 1 · SỰ CHUYỂN THỂ', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Mô tả cấu trúc rắn, lỏng, khí bằng <b>mô hình động học phân tử</b>`)}
${dong(`${ck}Gọi tên các <b>quá trình chuyển thể</b> và chiều của chúng`)}
${dong(`${ck}Giải thích nhiệt độ trong lúc chất đang nóng chảy, đang sôi`)}
${dong(`${ck}Đọc <b>đồ thị nhiệt độ – thời gian</b>; trả lời 6 câu ở mục Trả bài`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Trưa nắng, li nước có ba viên đá để quên trên bàn. Li vẫn nhận nhiệt từ không khí nóng. Trong lúc đá <b>đang tan</b>, nhiệt độ của li:</p>
<div class="fig-side" style="${fs(40)}"><div>
${opt('A', 'Tăng đều theo thời gian')}
${opt('B', `Giữ nguyên ở ${dC('0')} cho tới khi đá tan hết`)}
${opt('C', 'Giảm rồi mới tăng trở lại')}
${opt('D', 'Tăng nhanh lúc đầu rồi chậm dần')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 2)}</div>
${H.liDa()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(2)}</div>
${h3(4, 'II.1 · Mô hình động học phân tử', '1·4')}
<div class="card" style="padding:1.2mm 3mm">
<div><b>Rời:</b> chất cấu tạo từ những hạt ${f(22)}, giữa chúng có ${f(25)}.</div>
<div><b>Loạn:</b> các hạt chuyển động ${f(30)}; nhiệt độ càng cao thì tốc độ trung bình càng ${f(14)}.</div>
<div><b>Hút – Đẩy:</b> giữa các hạt có lực liên kết; gần nhau thì lực ${f(14)} chiếm ưu thế, xa nhau thì lực ${f(14)} chiếm ưu thế.</div>
<div style="margin-top:.6mm"><b>Thí nghiệm:</b> rót ${nw('50 ml')} rượu vào ống đong đã có ${nw('50 ml')} nước.</div>
<div><b>Quan sát:</b> mực chất lỏng ở vạch ${f(20)} ml (so với ${nw('100 ml')}: ${f(16)}).</div>
<div><b>Rút ra:</b> nội dung nào của mô hình? Vì sao?</div>${lines(2)}</div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('CẤU TRÚC BA THỂ · SỰ CHUYỂN THỂ')}
${h3(1, 'II.2 · Cấu trúc chất rắn, chất lỏng, chất khí', '2·1')}
<div class="fig-side" style="${fs(44)}"><div>
<table style="font-size:var(--fs-sm)"><tr><th style="width:9mm">Thể</th><th>Khoảng cách, sắp xếp</th><th>Chuyển động của hạt</th><th>Thể tích, hình dạng</th></tr>
<tr><td style="height:13mm">Rắn</td><td></td><td></td><td></td></tr>
<tr><td style="height:13mm">Lỏng</td><td></td><td></td><td></td></tr>
<tr><td style="height:13mm">Khí</td><td></td><td></td><td></td></tr></table></div>
${H.baThe()}</div>
<div style="margin-top:.6mm">Khoảng cách giữa các hạt càng nhỏ thì lực liên kết càng ${f(16)}, các hạt sắp xếp càng ${f(18)}.</div>
${h3(2, 'II.3 · Sự chuyển thể: bốn quá trình chính và hai quá trình ít gặp', '2·2')}
<div class="card fig-side" style="${fs(52)};padding:1.2mm 3mm"><div>
<div style="line-height:5.2mm">(1) ${f(30)}<br>(2) ${f(30)}<br>(3) ${f(30)}<br>(4) ${f(30)}<br>(5) ${f(30)}<br>(6) ${f(30)}</div>
<div style="margin-top:.6mm">Hoá hơi gồm hai cách: ${f(18)} và ${f(18)}.</div>
<div>Cùng một chất: nhiệt độ nóng chảy ${f(18)} nhiệt độ đông đặc.</div></div>
${H.vong()}</div>
${h3(3, 'Làm nhanh', '2·3')}
${box(cau(`<b>Câu 1.</b> Băng phiến (long não) trong tủ quần áo nhỏ dần, không thấy chất lỏng nào. Đó là quá trình gì, chiều nào?`, 1)
 + cau(`<b>Câu 2.</b> Thuỷ ngân nóng chảy ở ${dC('-39')}. Thuỷ ngân lỏng đông đặc ở nhiệt độ nào?`, 1)
 + cau(`<b>Câu 3.</b> Nến cháy: sáp ở đỉnh chảy xuống rồi cứng lại ở chân nến. Kể hai quá trình theo đúng thứ tự.`, 1)
 + cau(`<b>Câu 4.</b> Vì sao bơm xe đạp nén được không khí trong ống bơm, còn nước trong xi lanh kín thì gần như không nén được?`, 2))}
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('NÓNG CHẢY · BAY HƠI · SÔI · CHẤT RẮN')}
${h3(1, 'II.4 · Thí nghiệm: đun nước đá, mỗi phút ghi nhiệt độ', '3·1')}
${bangTT([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 20, 35], ['−6,0', '0,2', '0,2', '0,2', '0,3', '17,8', '38,0', '58,1', '78,0', '98,1', '100,2', '100,3', '100,3', '100,2'])}
<div class="fig-side" style="${fs(46)}"><div>
<div>Nhiệt độ đứng yên ở khoảng ${f(14)} °C từ phút ${f(8)} đến phút ${f(8)}: đá đang ${f(20)}.</div>
<div>Nhiệt độ đứng yên ở khoảng ${f(14)} °C từ phút ${f(8)}: nước đang ${f(20)}.</div>
<div>Từ phút 5 đến phút 9, nhiệt độ tăng ${f(14)} °C mỗi phút.</div>
<div style="margin-top:.6mm"><b>Vì sao</b> bếp vẫn cấp nhiệt mà nhiệt độ không tăng? Nhiệt nhận vào dùng để làm gì?</div>${lines(2)}
<div class="hint" style="margin-top:.4mm">Nhiệt kế chỉ 0,2 °C chứ không đúng 0 °C: nhiệt kế có sai số ±0,5 °C.</div></div>
${H.nuocDa()}</div>
${h3(2, 'Bay hơi và sôi', '3·2')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<table><tr><th style="width:22mm"></th><th>Bay hơi</th><th>Sôi</th></tr>
<tr><td>Xảy ra ở đâu</td><td style="height:8mm"></td><td></td></tr>
<tr><td>Nhiệt độ</td><td style="height:8mm"></td><td></td></tr></table>
<div style="margin-top:.6mm">Hình (a) là ${f(18)}, hình (b) là ${f(18)}.</div>
<div>Nhiệt độ sôi phụ thuộc ${f(22)}.</div></div>
${H.bayHoiSoi()}</div>
${h3(3, 'II.5 · Chất rắn kết tinh và chất rắn vô định hình', '3·3')}
<table><tr><th style="width:24mm">Tiêu chí</th><th>Kết tinh</th><th>Vô định hình</th></tr>
<tr><td>Cấu trúc</td><td style="height:7mm"></td><td></td></tr>
<tr><td>Nóng chảy</td><td style="height:7mm"></td><td></td></tr>
<tr><td>Ví dụ</td><td style="height:7mm"></td><td></td></tr></table>
${h3(4, 'Làm nhanh', '3·4')}
${box(cau(`<b>Câu 3.</b> Đun nóng đều một chất rắn kết tinh: đồ thị nhiệt độ – thời gian có hai đoạn nằm ngang ở ${dC('80')} và ${dC('250')}. Mỗi đoạn ứng với quá trình nào?`, 1)
 + cau(`<b>Câu 4.</b> Làm nguội hơi của chính chất đó từ ${dC('300')} xuống nhiệt độ phòng: gặp đoạn nằm ngang nào trước, đó là quá trình gì?`, 1))}
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('BA CÁI BẪY · TRẢ BÀI · TỰ KIỂM TRA')}
${h3(1, 'III · Ba cái bẫy hay sập', '4·1')}
<div class="card fig-side" style="${fs(42)};padding:1mm 3mm"><div>
<div class="trap">${ck}<span><b>“Đang nóng chảy thì nhiệt độ vẫn tăng.”</b> Lẫn nhiệt độ với nhiệt lượng: đang chuyển thể thì nhiệt độ ${f(16)}, nhiệt lượng vẫn ${f(16)}.</span></div>
<div class="trap">${ck}<span><b>“Nước chỉ bay hơi khi đã sôi.”</b> Quần áo phơi vẫn khô dù chưa tới ${dC('100')}: bay hơi xảy ra ở ${f(22)}.</span></div>
<div class="trap">${ck}<span><b>“Khí không có thể tích.”</b> Bơm thêm khí vào bình 20 lít đầy oxygen: thể tích khí ${f(14)} lít; thứ tăng là ${f(30)}. Nói đúng: khí không có ${f(25)}.</span></div></div>
${H.binhKhi()}</div>
${h3(2, 'IV · Trả bài 6 câu', '4·2')}
${box(`${tb('1. Ba nội dung của mô hình động học phân tử?')}${lines(2)}
${tb('2. Bốn quá trình chuyển thể và chiều của chúng?')}${lines(2)}
${tb('3. Vì sao chất lỏng có thể tích xác định mà hình dạng không xác định?')}${lines(2)}
${tb('4. Vì sao nhiệt độ không đổi suốt thời gian nóng chảy?')}${lines(2)}
${tb('5. Bay hơi khác sôi ở đâu? Nhiệt độ sôi phụ thuộc gì?')}${lines(2)}
${tb('6. Chất rắn kết tinh khác vô định hình ở đâu? Mỗi loại một ví dụ.')}${lines(2)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/6 câu · chưa thuộc: ${f(25)} ${nw(`→ đọc lại ô ${f(12)} Tập`)}</div>
${h3(3, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '4·3')}
${rkHai([1, 2, 3], [4, 5, 6])}
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TOÁN MẪU · BÀI TẬP VỀ NHÀ · THỬ THÁCH')}
${h3(1, 'V · Bài toán mẫu: đọc bảng nhiệt độ – thời gian', '5·1')}
<div class="card soft" style="padding:1.2mm 3mm">Đun nóng đều một chất rắn kết tinh, ghi nhiệt độ sau mỗi phút:
${bangTT([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], [20, 35, 50, 65, 80, 80, 80, 80, 80, 95, 110, 125, 140])}
${traNC([['nước đá', '0'], ['băng phiến', '80'], ['nhôm', '660']])}.<br>
<b>a)</b> Nhiệt độ nóng chảy? Chất này là gì? &nbsp;<b>b)</b> Nóng chảy kéo dài bao lâu? &nbsp;<b>c)</b> Từ phút 8 đến phút 12, nhiệt độ tăng bao nhiêu độ mỗi phút?</div>
<div class="fig-side" style="${fs(48)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl('a) Đoạn nằm ngang ở … ⇒ chất là', 2)}${wl('b) Đếm khoảng giữa hai mốc, không đếm số dòng:', 2)}${wl(`c) ${m('\\dfrac{\\Delta T}{\\Delta t}=')}`, 2)}</div>${H.truc()}</div>
${h3(2, 'Điền bước còn thiếu: làm nguội chính chất đó từ 140 °C', '5·2')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div class="ln"><b>Bước 1 (cho sẵn):</b> mỗi phút toả nhiệt đúng bằng lúc đun ⇒ thể lỏng nguội ${nw('15 °C')} mỗi phút.</div>
${wl(`Bước 2: từ ${dC('140')} xuống ${dC('80')} mất`, 1)}${wl('Bước 3: đông đặc ở nhiệt độ nào, trong bao lâu?', 1)}${wl('Bước 4: tổng thời gian đến khi đông đặc hoàn toàn:', 1)}</div>
${K.btvn().replace('<i>1</i>', '<i>3</i>')}
${h3(4, 'Thử thách phân tầng', '5·4')}
${box(wl(`${m('\\bigstar')} Kể tên bốn quá trình chuyển thể chính và chiều của mỗi quá trình.`, 2)
 + cau(`${m('\\bigstar\\bigstar')} Vì sao trời nồm, nền nhà và gương lại “đổ mồ hôi”?`, 1)
 + cau(`${m('\\bigstar\\bigstar\\bigstar')} Trên núi cao 3000 m, nước sôi ở khoảng ${dC('90')}. Vì sao nấu cơm ở đó lâu chín hơn?`, 1))}
${foot(5)}</section>`;

const tra3 = `Nhiệt độ nóng chảy: ${['thiếc 232', 'chì 327', 'nhôm 660'].map((x) => nw(x + ' °C')).join(' · ')}`;
const hep = (fig, w = 36) => `<div style="width:${w}mm;justify-self:end">${fig}</div>`;
const dang = [
  { t: 'Dạng 1 · Dễ · Gọi tên quá trình chuyển thể trong đời sống',
    de: `Cốc nước đá trong phòng nóng ẩm, cạnh đĩa có ít nước. Sau 30 phút: (1) đá nhỏ dần, nước trong cốc nhiều lên; (2) thành ngoài cốc phủ giọt nước; (3) nước trong đĩa cạn bớt, không sủi bọt.<br><b>a)</b> tên quá trình và chiều chuyển thể ở (1), (2), (3)<br><b>b)</b> có mấy hiện tượng mà chất toả nhiệt`,
    nd: `Gọi tên theo thể đầu ${to} thể cuối; không sủi bọt thì là ${f(18)}`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'a<sub>3</sub>', 'b'], gi: 2, fig: hep(H.cocD1(''), 21) },
  { t: 'Dạng 2 · Dễ · Thể tích và hình dạng của rắn, lỏng, khí trong bình',
    de: `Sáp nến (khối đặc), dầu ăn, khí helium, mỗi chất ${nw('0,30 lít')}, lần lượt cho vào ba bình rỗng ${nw('1,5 lít')} rồi đậy kín (bình 3 đã hút hết không khí trước khi bơm helium). Nhiệt độ không đổi.<br><b>a)</b> thể tích và hình dạng trong bình của sáp (a<sub>1</sub>), dầu (a<sub>2</sub>), helium (a<sub>3</sub>)<br><b>b)</b> giải thích kết quả của helium bằng mô hình động học phân tử`,
    nd: `Rắn, lỏng giữ ${f(22)}; khí ${f(28)}`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'a<sub>3</sub>', 'b'], gi: 2 },
  { t: 'Dạng 3 · Trung bình · Đọc bảng nhiệt độ – thời gian',
    de: `Đun nóng đều chất rắn kết tinh ${m('X')}. ${tra3}.${bangTT([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], [52, 82, 112, 142, 172, 202, 232, 232, 232, 232, 232, 232, 257, 282, 307])}<b>a)</b> nhiệt độ nóng chảy của ${m('X')}; ${m('X')} là chất nào<br><b>b)</b> chất nóng chảy trong bao lâu<br><b>c)</b> ở phút thứ 9, chất ở thể nào<br><b>d)</b> sau khi nóng chảy hết, nhiệt độ tăng bao nhiêu độ mỗi phút`,
    nd: `Dòng nhiệt độ không đổi là ${f(25)}; thời gian = ${f(22)} hai mốc`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c', 'd'], cot: 5, gi: 4 },
  { t: 'Dạng 4 · Khó · Đọc đồ thị nhiệt độ – thời gian nhiều giai đoạn',
    de: `Chất ${m('X')} lúc đầu ở thể rắn, ${dC('20')}, được đun nóng đều. Đồ thị nhiệt độ theo thời gian như hình; ${m('BC')} và ${m('DE')} là hai đoạn nằm ngang.<br><b>a)</b> nhiệt độ nóng chảy và nhiệt độ sôi của ${m('X')}<br><b>b)</b> ở phút thứ 16, ${m('X')} ở thể nào<br><b>c)</b> quá trình sôi kéo dài bao lâu<br><b>d)</b> ở đoạn ${m('CD')}, nhiệt độ tăng bao nhiêu độ mỗi phút`,
    nd: `Đoạn ngang ${f(12)} là nóng chảy, đoạn ngang ${f(12)} là sôi (không xét độ dài)`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c', 'd'], cot: 3, gi: 6, fig: H.doThiD4() },
  { t: 'Dạng 5 · Nâng cao · Làm nguội kim loại đúc: dữ kiện ẩn',
    de: `Rót chì lỏng ở ${dC('397')} vào khuôn; khi còn lỏng, chì nguội đều ${nw('14 °C')} mỗi phút. Lúc đun, thanh chì ấy nóng chảy hết trong 4 phút; coi tốc độ toả nhiệt khi nguội bằng tốc độ nhận nhiệt lúc đun. ${tra3}.<br><b>a)</b> chì đông đặc ở nhiệt độ nào<br><b>b)</b> sau bao nhiêu phút kể từ lúc rót thì chì bắt đầu đông đặc<br><b>c)</b> chì đông đặc hoàn toàn vào phút thứ mấy<br><b>d)</b> nhiệt độ chì ở phút thứ 7<br><b>e)</b> thuỷ tinh nguội đều mà nhiệt kế không lúc nào đứng yên: thuỷ tinh là chất rắn loại nào`,
    nd: `Đông đặc ở ${f(16)} nhiệt độ nóng chảy; thời gian đông đặc ${f(18)}`, a: ['a', 'b', 'c', 'd', 'e'], cot: 3, gi: 5 },
];

// Bài tương tự: mỗi dạng 2 bài, giải vào vở (thầy chốt 10/11), ô đáp số cuối dòng của ý; đáp số tính bằng Python 12/11/2026.
const oY = (s, o, w = {}) => s.split('<br>').map((p) => {
  const y = p.match(/^<b>([a-e])\)<\/b>/);
  if (!y) return `<div>${p}</div>`;
  const ls = o.filter((l) => l[0] === y[1]);
  return `<div class="yo"><span>${p}</span><span class="oo">${ls.map((l) => `<span class="nw"><b>${l})</b>${f(typeof w === 'object' ? (w[l] ?? 25) : w)}</span>`).join('')}</span></div>`;
}).join('');
const ttDe = (b) => b.fig ? `<div class="fig-side" style="grid-template-columns:1fr ${b.fw}mm">${`<div>${oY(b.de, b.o, b.ow)}</div>`}${b.fig}</div>` : oY(b.de, b.o, b.ow);
const vaoVo = (ds) => ds.map((b) => (b.o ? { t: b.t, de: ttDe(b), k: 0 } : b));
const nhap = (n) => ({ t: '<span class="nhap-t">Nháp / chỗ em còn vướng</span>', de: lines(n), k: 0 });
const traCB = traNC([['nước đá', '0'], ['băng phiến', '80'], ['thiếc', '232'], ['chì', '327'], ['nhôm', '660']]);
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–3', 'DẠNG 4–5'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `(1) Sương đọng trên lá lúc sớm; (2) trưa nắng, sương biến mất; (3) nước trong ngăn đá thành đá viên.<br><b>a)</b> tên quá trình ở (1), (2), (3)<br><b>b)</b> số hiện tượng chất toả nhiệt`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'a<sub>3</sub>', 'b'], ow: { b: 10, 'a<sub>1</sub>': 20, 'a<sub>2</sub>': 20, 'a<sub>3</sub>': 20 } },
    { t: 'Dạng 1 · Bài 2', de: `(1) Sô-cô-la trong túi chảy mềm; (2) đá khô nhỏ dần, không có chất lỏng; (3) nước sủi bọt ở ${nw('100 °C')}.<br><b>a)</b> tên quá trình ở (1), (2), (3)<br><b>b)</b> số hiện tượng chất nhận nhiệt`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'a<sub>3</sub>', 'b'], ow: { b: 10, 'a<sub>1</sub>': 20, 'a<sub>2</sub>': 20, 'a<sub>3</sub>': 20 } },
    { t: 'Dạng 2 · Bài 1', de: `Bình kín ${nw('2,0 lít')}: (1) ${nw('0,10 lít')} đá cuội; (2) ${nw('0,40 lít')} nước; (3) ${nw('0,40 lít')} nitrogen bơm vào bình rỗng.<br><b>a)</b> thể tích đá cuội, nước, nitrogen trong bình<br><b>b)</b> chất nào có hình dạng theo bình chứa`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'a<sub>3</sub>', 'b'], ow: { 'a<sub>1</sub>': 16, 'a<sub>2</sub>': 16, 'a<sub>3</sub>': 16, b: 30 } },
    { t: 'Dạng 2 · Bài 2', de: `Xi lanh kín chứa ${nw('50 cm³')} khí. Đẩy pit-tông cho phần chứa khí còn ${nw('30 cm³')}, nhiệt độ không đổi.<br><b>a)</b> thể tích khí khi đó<br><b>b)</b> số phân tử khí trong xi lanh tăng, giảm hay không đổi<br><b>c)</b> thay khí bằng ${nw('50 cm³')} nước: có đẩy được còn ${nw('30 cm³')} không`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 3 · Bài 1', de: `Đun nóng đều chất rắn kết tinh ${m('Y')}. ${traNC([['thiếc', '232'], ['chì', '327'], ['nhôm', '660']])}.${bangTT([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [87, 147, 207, 267, 327, 327, 327, 327, 327, 347, 367])}<br><b>a)</b> nhiệt độ nóng chảy; ${m('Y')} là chất nào<br><b>b)</b> thời gian nóng chảy<br><b>c)</b> ở phút thứ 6, chất ở thể nào; sau khi nóng chảy hết, nhiệt độ tăng bao nhiêu độ mỗi phút`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'], ow: { 'a<sub>1</sub>': 16, 'a<sub>2</sub>': 16, b: 16, 'c<sub>1</sub>': 26, 'c<sub>2</sub>': 14 } },
    { t: 'Dạng 3 · Bài 2', de: `Đun nóng đều một chất rắn kết tinh. ${traNC([['nước đá', '0'], ['thiếc', '232'], ['chì', '327']])}.${bangTT([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [-12, -6, 0, 0, 0, 0, 0, 0, 3, 6])}<br><b>a)</b> nhiệt độ nóng chảy; chất là gì<br><b>b)</b> thời gian nóng chảy<br><b>c)</b> ở phút thứ 1, chất ở thể nào; sau khi nóng chảy hết, nhiệt độ tăng bao nhiêu độ mỗi phút`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'], ow: { 'a<sub>1</sub>': 16, 'a<sub>2</sub>': 20, b: 16, 'c<sub>1</sub>': 14, 'c<sub>2</sub>': 14 } },
  ], [
    { t: 'Dạng 4 · Bài 1', de: `Đun nóng đều chất rắn ${m('X')}; ${m('BC')}, ${m('DE')} nằm ngang.<br><b>a)</b> nhiệt độ nóng chảy, nhiệt độ sôi<br><b>b)</b> ở phút thứ 9, ${m('X')} ở thể nào<br><b>c)</b> thời gian nóng chảy, thời gian sôi<br><b>d)</b> đoạn ${m('CD')}: tăng mấy °C mỗi phút`, fig: H.doThiT1(''), fw: 46, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>', 'd'], ow: { 'a<sub>1</sub>': 14, 'a<sub>2</sub>': 14, b: 22, 'c<sub>1</sub>': 14, 'c<sub>2</sub>': 14, d: 22 } },
    { t: 'Dạng 4 · Bài 2', de: `Làm nguội đều hơi chất ${m('Z')} tới khi thành rắn; ${m('BC')}, ${m('DE')} nằm ngang.<br><b>a)</b> nhiệt độ sôi, nhiệt độ nóng chảy<br><b>b)</b> ở phút thứ 4, ${m('Z')} ở thể nào<br><b>c)</b> đông đặc kéo dài bao lâu<br><b>d)</b> đoạn ${m('CD')}: giảm mấy °C mỗi phút`, fig: H.doThiT2(''), fw: 46, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c', 'd'], ow: { 'a<sub>1</sub>': 14, 'a<sub>2</sub>': 14, b: 26, c: 16, d: 22 } },
    { t: 'Dạng 5 · Bài 1', de: `Rót thiếc lỏng ở ${dC('292')} vào khuôn. Khi còn lỏng, thiếc nguội đều ${nw('12 °C')} mỗi phút. Lúc đun, thỏi thiếc ấy nóng chảy hoàn toàn mất 3 phút; coi tốc độ toả nhiệt khi nguội bằng tốc độ nhận nhiệt lúc đun. ${traCB}.<br><b>a)</b> thiếc đông đặc ở nhiệt độ nào<br><b>b)</b> sau bao nhiêu phút kể từ lúc rót thì thiếc bắt đầu đông đặc<br><b>c)</b> thiếc đông đặc hoàn toàn vào phút thứ mấy<br><b>d)</b> nhiệt độ thiếc ở phút thứ 6`, o: ['a', 'b', 'c', 'd'], ow: 18 },
    { t: 'Dạng 5 · Bài 2', de: `Rót nhôm lỏng ở ${dC('720')} vào khuôn. Khi còn lỏng, nhôm nguội đều ${nw('15 °C')} mỗi phút. Lúc đun, khối nhôm ấy nóng chảy hoàn toàn mất 6 phút; coi tốc độ toả nhiệt khi nguội bằng tốc độ nhận nhiệt lúc đun. ${traCB}.<br><b>a)</b> nhôm bắt đầu đông đặc vào phút thứ mấy<br><b>b)</b> nhôm đông đặc hoàn toàn vào phút thứ mấy<br><b>c)</b> nhiệt độ nhôm ở phút thứ 3; ở phút thứ 8<br><b>d)</b> nhựa nóng nguội đều, nhiệt kế không lúc nào đứng yên: nhựa là chất rắn loại nào`, o: ['a', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>', 'd'], ow: { a: 14, b: 14, 'c<sub>1</sub>': 16, 'c<sub>2</sub>': 16, d: 26 } },
    nhap(2),
  ]],
  dap: [
    'D1·1: a<sub>1</sub>) ngưng tụ · a<sub>2</sub>) bay hơi · a<sub>3</sub>) đông đặc · b) 2 | D1·2: a<sub>1</sub>) nóng chảy · a<sub>2</sub>) thăng hoa · a<sub>3</sub>) sôi · b) 3 | D2·1: a<sub>1</sub>) 0,10 lít · a<sub>2</sub>) 0,40 lít · a<sub>3</sub>) 2,0 lít · b) nước, nitrogen | D2·2: a) 30 cm³ · b) không đổi · c) không | D3·1: a<sub>1</sub>) 327 °C · a<sub>2</sub>) chì · b) 4 phút · c<sub>1</sub>) rắn và lỏng · c<sub>2</sub>) 20 °C | D3·2: a<sub>1</sub>) 0 °C · a<sub>2</sub>) nước đá · b) 5 phút · c<sub>1</sub>) rắn · c<sub>2</sub>) 3 °C',
    'D4·1: a<sub>1</sub>) 80 °C · a<sub>2</sub>) 230 °C · b) lỏng · c<sub>1</sub>) 4 phút · c<sub>2</sub>) 7 phút · d) 30 °C | D4·2: a<sub>1</sub>) 110 °C · a<sub>2</sub>) 30 °C · b) hơi và lỏng · c) 6 phút · d) 20 °C | D5·1: a) 232 °C · b) 5 phút · c) phút 8 · d) 232 °C | D5·2: a) phút 4 · b) phút 10 · c<sub>1</sub>) 675 °C · c<sub>2</sub>) 660 °C · d) vô định hình',
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 2], kq: [[1, 2, 3], [4, 5]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'động học phân tử 1·4 · ba thể 2·1 · chuyển thể 2·2 · đun nước đá 3·1 · bay hơi, sôi 3·2 · kết tinh 3·3 · bẫy 4·1 · bài toán mẫu 5·1 · dạng 1–3 → 6·1 · dạng 4–5 → 7·1',
  out: process.argv[2],
});
