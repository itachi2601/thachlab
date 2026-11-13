// Ruột tập VL10 – Bài 5 · Tốc độ và vận tốc (lesson id 50). Quyển Chương 2 lớp 10 (bài 4–12): bài 5 = tr. 13–24.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự giải vào vở · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l10-bai5.mjs (toàn bộ SVG tự vẽ). Nội dung theo bài web (book/cache/50.json, tải 13/11/2026): mục tiêu, dự đoán đường
// đua trượt băng, II.1–II.4, hai thí nghiệm (đo tốc độ đi bộ, bút trên giấy bị kéo), ba bẫy, Trả bài 6 câu, bài toán mẫu ca nô qua
// sông, thử thách, 6 dạng bài tập mẫu. Đáp số Bài tương tự (tuongTu.dap) tính bằng Python 13/11/2026.
// Chạy: node scripts/ruot-tap/l10-bai5.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl10-bai5.pdf
//       node scripts/ruot-tap/l10-bai5.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l10-bai5/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL10b5 as H } from './hinh-l10-bai5.mjs';

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
  const out = resolve(HERE, 'out/hinh-l10-bai5'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 5, lid: 50, ten: 'TỐC ĐỘ VÀ VẬN TỐC', lop: 10, baiDau: 4, sub: 'Vật lí 10 · Chương 2: Động học' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const vv = (s) => m(`\\vec v_{${s}}`);
const v = (s) => m(`v_{${s}}`);
const vtb = m('v_{\\mathrm{tb}}'), vvtb = m('\\vec v_{\\mathrm{tb}}'), vd = m('\\vec d');
const kmh = m('\\mathrm{km/h}'), ms = m('\\mathrm{m/s}');

const ttHaiCot = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm}.yo .oo{flex:none;display:flex;gap:3mm}.yo{line-height:1.35}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';
const p1 = `${ttHaiCot}<section class="page">
${head('BÀI 5 · TỐC ĐỘ VÀ VẬN TỐC', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Tính được <b>tốc độ trung bình</b>; đổi được km/h ↔ m/s`)}
${dong(`${ck}Hiểu <b>tốc độ tức thời</b> là số chỉ trên tốc kế`)}
${dong(`${ck}Phân biệt <b>tốc độ</b> với <b>vận tốc</b>`)}
${dong(`${ck}Dùng <b>công thức cộng vận tốc</b> khi hai vận tốc cùng chiều, ngược chiều, vuông góc`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Đường đua trượt băng dài ${nw('111 m')} một vòng. Vận động viên trượt đúng một vòng trong khoảng ${nw('9 s')} rồi dừng ở đúng vạch xuất phát. Bảng điện tử báo tốc độ trung bình khoảng ${nw('12,3 m/s')}. <b>Vận tốc trung bình</b> sau cả vòng là bao nhiêu?</p>
<div class="fig-side" style="${fs(46)}"><div>
${opt('A', `Khoảng ${nw('12,3 m/s')}, vì lấy ${nw('111 m')} chia ${nw('9 s')}`)}
${opt('B', 'Bằng 0')}
${opt('C', `Khoảng ${nw('6,2 m/s')}, trung bình của 0 (lúc đứng ở vạch) và ${nw('12,3 m/s')}`)}
${opt('D', 'Không tính được, vì đường đua cong')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 2)}</div>
${H.duongDua()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(2)}</div>
${h3(4, 'II.1 · Tốc độ trung bình', '1·4')}
<div class="card" style="padding:1.2mm 3mm">
<div>Tốc độ cho biết chuyển động ${f(25)} hay ${f(25)}; là đại lượng ${f(25)} hướng.</div>
<div style="margin:.6mm 0">${vtb} = <span class="fill" style="min-width:16mm;height:9mm"></span> &nbsp;với ${m('s')} là ${f(25)}, ${m('t')} là ${f(25)}</div>
<div>Đơn vị SI: ${f(14)}. ${nw(`1 km/h = 1000 m : ${f(12)}&nbsp;s`)}</div>
<div>km/h → m/s: ${f(25)} cho 3,6 &nbsp;·&nbsp; m/s → km/h: ${f(25)} với 3,6</div>
<div>Đổi: ${nw(`54 km/h = ${f(12)}&nbsp;m/s`)} · ${nw(`15 m/s = ${f(12)}&nbsp;km/h`)}</div>
<div style="margin-top:.6mm"><b>Vòng đua ở trên:</b> ${nw(`${m('v_{\\mathrm{tb}}=111:9\\approx')} ${f(14)}&nbsp;m/s`)} ${nw(`≈ ${f(14)}&nbsp;km/h`)}</div>
<div style="margin-top:.6mm">Vì sao số ${nw('12,3 m/s')} này là <b>tốc độ</b> chứ không phải vận tốc trung bình của cả vòng?</div>${lines(1)}</div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('ĐO TỐC ĐỘ · TỐC ĐỘ TỨC THỜI · VẬN TỐC')}
${h3(1, 'Thí nghiệm: đo tốc độ đi bộ của một bạn', '2·1')}
<div class="fig-side" style="${fs(42)}"><div>
<div><b>Làm:</b> dán hai vạch cách nhau ${nw(`${m('s=10{,}0\\ \\mathrm m')}`)}. Một bạn đi bộ đều qua hai vạch, bạn khác bấm đồng hồ lúc chân chạm mỗi vạch. Đo 5 lần.</div>
<table class="tbl-ct" style="margin-top:.8mm"><tr><th>Lần</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>TB</th></tr>
<tr><td>${m('t\\ (\\mathrm s)')}</td><td>7,9</td><td>8,3</td><td>8,1</td><td>7,7</td><td>8,0</td><td></td></tr>
<tr><td>${m('v_{\\mathrm{tb}}\\ (\\mathrm{m/s})')}</td><td></td><td></td><td></td><td></td><td></td><td></td></tr></table></div>
${H.diBo()}</div>
<div class="card" style="margin-top:.8mm;padding:1mm 3mm">
<div>Lệch nhiều nhất: lần ${f(12)} và lần ${f(12)}. Sai số lớn nhất đến từ:</div>${lines(1)}
<div>Muốn giảm sai số, em sẽ:</div>${lines(1)}</div>
${h3(2, 'II.2 · Tốc độ tức thời', '2·2')}
<div class="card fig-side" style="${fs(34)};padding:1.2mm 3mm"><div>
<div>Tốc độ tức thời: tốc độ tại một ${f(25)}, tức tốc độ trung bình trong khoảng thời gian rất ${f(25)}.</div>
<div>Tốc kế xe máy chỉ tốc độ ${f(25)}. Tốc độ tức thời không đổi ⇒ chuyển động ${f(25)}.</div>
<div style="margin-top:.6mm"><b>Làm nhanh.</b> Xe máy đi ${nw('6 km')} từ nhà tới trường hết ${nw('15 phút')}; lúc qua cổng, tốc kế chỉ ${nw('20 km/h')}.</div>
<div>${nw(`${vtb} = ${f(14)}&nbsp;km/h`)}; số ${nw('20 km/h')} là tốc độ ${f(25)}.</div></div>
${H.tocKe()}</div>
${h3(3, 'II.3 · Vận tốc', '2·3')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div>${m('s')}: độ dài đường đi thật. ${vd}: mũi tên nối thẳng điểm ${f(25)} → điểm ${f(25)}.</div>
<div style="margin:.4mm 0">${nw(`${vvtb} =`)} ${f(14)} ${m(':\\ t')}, là đại lượng ${f(25)}.</div>
<div>Vectơ ${vvtb}: gốc đặt ở ${f(25)}; hướng theo ${f(25)}; độ dài tỉ lệ ${f(25)}.</div>
<div>Vận tốc tức thời tại một điểm trên đường cong: hướng ${f(25)} với quỹ đạo, theo chiều vật đi.</div>
<div>Đi thẳng, không đổi chiều: ${nw(`${m('d')} ${f(12)} ${m('s')}`)}.</div>
<div style="margin-top:.6mm"><b>Ví dụ.</b> Xe đồ chơi chạy nửa vòng tròn ${nw(`${m('R=20\\ \\mathrm{cm}')}`)} từ A tới B hết ${nw('4 s')}; quãng đường nửa vòng ${nw(`${m('s=\\pi R')}`)}.</div>
<div>${nw(`${m('s\\approx')} ${f(12)}&nbsp;cm`)} · ${nw(`${m('d=')} ${f(12)}&nbsp;cm`)} · tốc độ TB ${nw(`≈ ${f(12)}&nbsp;cm/s`)}</div>
<div>độ lớn vận tốc TB ${nw(`= ${f(12)}&nbsp;cm/s`)}, hướng từ ${f(12)} sang ${f(12)}</div></div>
${H.nuaVong()}</div>
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('TÍNH TƯƠNG ĐỐI · CÔNG THỨC CỘNG VẬN TỐC')}
${h3(1, 'II.4 · Tính tương đối của chuyển động', '3·1')}
<div class="card" style="padding:1.2mm 3mm">
<div>Vật đứng yên so với hệ quy chiếu này vẫn có thể ${f(25)} so với hệ quy chiếu khác: vận tốc phụ thuộc ${f(25)}.</div>
<div style="margin:.4mm 0">Đánh số: (1) vật đang xét · (2) hệ ${f(25)} · (3) hệ ${f(25)}</div>
<table style="margin:.6mm 0"><tr><th style="width:14mm">Kí hiệu</th><th>Vận tốc của … so với …</th><th style="width:30mm">Tên gọi</th></tr>
<tr><td>${vv('13')}</td><td style="height:6mm"></td><td></td></tr>
<tr><td>${vv('12')}</td><td style="height:6mm"></td><td></td></tr>
<tr><td>${vv('23')}</td><td style="height:6mm"></td><td></td></tr></table>
<div><b>Công thức cộng vận tốc:</b> ${nw(`${vv('13')} =`)} ${f(14)} + ${f(14)} &nbsp;· mẹo “khử số 2”: nối 1 → 2 với 2 → 3 được ${f(14)}</div></div>
${h3(2, 'Ba trường hợp đặc biệt', '3·2')}
<div class="fig-side" style="${fs(42)}"><table>
<tr><th style="width:24mm">${vv('12')} và ${vv('23')}</th><th>Độ lớn ${v('13')}</th></tr>
<tr><td>Cùng chiều</td><td style="height:7.5mm"></td></tr>
<tr><td>Ngược chiều</td><td style="height:8mm;vertical-align:bottom"><span class="hint">chiều theo vận tốc</span> ${f(25)}</td></tr>
<tr><td>Vuông góc</td><td style="height:9.5mm"></td></tr></table>
${H.baTH()}</div>
${h3(3, 'Thí nghiệm: vẽ trên tờ giấy đang bị kéo', '3·3')}
<div class="card fig-side" style="${fs(40)};padding:1.2mm 3mm"><div>
<div><b>Làm:</b> A kéo đều dải giấy dọc mép bàn; B đưa bút dạ đều theo thước đặt vuông góc mép bàn.</div>
<div><b>Quan sát:</b> so với bàn, ngòi bút đi ${f(25)}; vệt mực trên giấy ${f(25)}.</div>
<div><b>Rút ra</b> (đánh số như mục 1): bút là (1), giấy là (${f(12)}), bàn là (${f(12)}). Vệt trên giấy ứng với ${nw(`${m('\\vec v')} số ${f(12)}`)}; đường dọc thước ứng với ${nw(`${m('\\vec v')} số ${f(12)}`)}.</div></div>
${H.giayKeo()}</div>
${h3(4, 'Làm nhanh', '3·4')}
${box(cau(`<b>Câu 1.</b> Em đi về phía đầu tàu ${nw('1 m/s')} so với toa; tàu chạy ${nw('10 m/s')} so với đường ray. Vận tốc kéo theo là bao nhiêu, của cái gì so với cái gì? Tính ${v('13')}.`, 2)
 + cau(`<b>Câu 2.</b> Người bơi ngược dòng ${nw('1,5 m/s')} so với nước; nước chảy ${nw('2 m/s')} so với bờ. So với bờ: ${nw(`${v('13')} = ${f(14)}&nbsp;m/s`)}, theo chiều ${f(25)}.`, 1))}
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('TỰ KIỂM TRA · BẪY · TRẢ BÀI · THỬ THÁCH')}
${h3(1, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '4·1')}
${rkHai([1, 2, 3, 4], [5, 6, 7])}
${h3(2, 'III · Ba cái bẫy hay sập', '4·2')}
<div class="card" style="padding:1mm 3mm"><div>
<div class="trap">${ck}<span><b>“Tốc độ TB = độ lớn vận tốc TB.”</b> Chỉ đúng khi đi thẳng, không quay đầu; đi vòng, quay lại thì ${m('d\\lt s')}.</span></div>
<div class="trap">${ck}<span><b>“Tốc độ TB = trung bình cộng các tốc độ.”</b> Phải lấy tổng ${m('s')} chia tổng ${m('t')}.</span></div>
<div class="trap">${ck}<span><b>“Cộng vận tốc như cộng hai số.”</b> Vẽ vectơ trước: ngược chiều thì trừ, vuông góc dùng Pythagore.</span></div></div></div>
${h3(3, 'IV · Trả bài 6 câu', '4·3')}
${box(`${tb('1. Công thức tốc độ trung bình, ý nghĩa kí hiệu; đổi km/h sang m/s?')}${lines(1)}
${tb('2. Tốc độ tức thời là gì? Thế nào là chuyển động đều?')}${lines(1)}
${tb('3. Vận tốc trung bình tính thế nào? Vectơ của nó có ba đặc điểm gì?')}${lines(1)}
${tb('4. Khi nào độ lớn vận tốc trung bình bằng tốc độ trung bình?')}${lines(1)}
${tb('5. Vận tốc tuyệt đối, tương đối, kéo theo: của cái gì so với cái gì?')}${lines(1)}
${tb('6. Công thức cộng vận tốc và ba trường hợp đặc biệt?')}${lines(2)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/6 câu · chưa thuộc: ${f(25)} ${nw(`→ đọc lại ô ${f(12)} Tập`)}</div>
${h3(4, 'Thử thách phân tầng', '4·4')}
<div class="fig-side" style="${fs(40)}">${box(cau(`${m('\\bigstar')} Đổi ${nw('72 km/h')} sang m/s: ${f(20)}`, 0)
 + cau(`${m('\\bigstar\\bigstar')} Nửa đầu <b>thời gian</b> ${nw('40 km/h')}, nửa sau ${nw('60 km/h')}: ${m('v_{\\mathrm{tb}}=')} ${f(16)}`, 0)
 + cau(`${m('\\bigstar\\bigstar\\bigstar')} Ca nô ${nw('5 m/s')} so với nước, nước ${nw('3 m/s')}, sông ${nw('120 m')}. Cập đúng B đối diện: góc ${m('\\alpha')}? thời gian?`, 2))}${H.caNoLech()}</div>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TOÁN MẪU · CA NÔ QUA SÔNG · VỀ NHÀ')}
${h3(1, 'V · Bài toán mẫu: ca nô qua sông', '5·1')}
<div class="card soft" style="padding:1.2mm 3mm">Ca nô chạy ${nw('4 m/s')} so với nước, mũi luôn vuông góc với bờ. Sông rộng ${nw('120 m')}, nước chảy đều ${nw('3 m/s')} so với bờ. Tính: <b>a)</b> độ lớn vận tốc của ca nô so với bờ; <b>b)</b> thời gian sang sông; <b>c)</b> khoảng cách BC từ điểm cập bến C tới điểm B đối diện chỗ xuất phát A.</div>
<table><tr><th style="width:52mm">Câu trong đề</th><th>Dữ liệu → kiến thức</th></tr>
<tr><td>“ca nô … 4 m/s so với nước”</td><td>${m('v_{12}=4\\ \\mathrm{m/s}')} → vận tốc tương đối</td></tr>
<tr><td style="height:6.5mm">“nước chảy … 3 m/s so với bờ”</td><td></td></tr>
<tr><td style="height:6.5mm">“mũi … vuông góc với bờ”</td><td></td></tr>
<tr><td style="height:6.5mm">“sông rộng 120 m”</td><td></td></tr>
<tr><td style="height:6.5mm">Ngầm: “chạy đều”</td><td></td></tr></table>
<div class="fig-side" style="${fs(46)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl('Đánh số (1), (2), (3):', 1)}${wl(`a) ${v('13')}:`, 2)}${wl('b) Thời gian sang sông:', 2)}${wl('c) BC:', 2)}${wl(`Kiểm tra: ${m('AC')} và ${m('v_{13}\\,t')} có bằng nhau?`, 1)}</div>${H.caNo()}</div>
${h3(2, 'Điền bước còn thiếu', '5·2')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div class="ln"><b>Đổi số:</b> ${nw('8 m/s')} so với nước, nước ${nw('6 m/s')}, sông rộng ${nw('200 m')}, mũi vẫn vuông góc bờ.</div>
<div class="ln"><b>Bước 1 (cho sẵn):</b> ${m('v_{13}=\\sqrt{8^2+6^2}=10\\ \\mathrm{m/s}')}</div>
${wl(`Bước 2: ${m('t=')}`, 1)}${wl(`Bước 3: ${m('BC=')}`, 1)}</div>
${K.btvn().replace('<i>1</i>', '<i>3</i>')}
${h3(4, 'VI · Mang về: điều em dễ quên nhất', '5·4')}
${box(wl('1.', 2) + wl('2.', 2))}
${foot(5)}</section>`;

// Hình bài tập mẫu thu còn 38 mm, không chú thích (cột hình của khung rộng 46 mm) để hình không cao hơn ô "Phân tích và giải".
const sm = (fig, w = 38) => fig.replace('<figure class="fig"', `<figure class="fig" style="width:${w}mm;justify-self:end"`);
const dang = [
  { t: 'Dạng 1 · Dễ · Tốc độ trung bình khi đi nhiều đoạn',
    de: `Chạy bộ trên đường thẳng, không đổi chiều: ${nw('4 phút')} đầu với ${nw('4 m/s')}, ${nw('6 phút')} sau với ${nw('3 m/s')}.<br><b>a)</b> quãng đường ${m('s')}<br><b>b)</b> tốc độ trung bình (m/s)<br><b>c)</b> lấy ${m('(4+3):2')} làm tốc độ trung bình được không?`,
    nd: `Đổi phút ra ${f(25)}; lấy tổng ${m('s')} chia tổng ${f(14)}`, a: ['a', 'b', 'c'], gi: 3, fig: sm(H.chayBo(), 36) },
  { t: 'Dạng 2 · Dễ · Lộ trình gấp khúc',
    de: `Từ nhà A đến trường C: ${nw('AB = 480 m')} hướng đông hết ${nw('6 phút')}, rồi ${nw('BC = 360 m')} hướng bắc hết ${nw('4 phút')}.<br><b>a)</b> độ lớn độ dịch chuyển AC<br><b>b)</b> tốc độ trung bình<br><b>c)</b> độ lớn vận tốc trung bình`,
    nd: `${m('d=AC')} tính bằng định lí ${f(25)}; ${vvtb} hướng từ ${f(12)} tới ${f(12)}`, a: ['a', 'b', 'c'], gi: 3, fig: sm(H.loTrinh(), 36) },
  { t: 'Dạng 3 · Trung bình · Đi rồi quay lại: dấu của vận tốc',
    de: `Bể dài ${nw('50 m')}: bơi đầu → cuối ${nw('40 s')}, rồi về ${nw('50 s')}; chiều dương đầu → cuối.<br><b>a)</b> vận tốc trung bình lúc bơi về (cuối → đầu)<br><b>b)</b> tốc độ trung bình cả đi lẫn về<br><b>c)</b> vận tốc trung bình cả đi lẫn về`,
    nd: `Tốc độ luôn ${f(25)}; vận tốc mang dấu; về chỗ cũ ⇒ ${nw(`${m('d=')} ${f(12)}`)}`, a: ['a', 'b', 'c'], gi: 3, fig: sm(H.beBoi(), 36) },
  { t: 'Dạng 4 · Trung bình · Cộng vận tốc cùng chiều: đuổi kịp',
    de: `Mô tô quay phim chạy cùng chiều đoàn đua xe đạp, giữ ${nw('60 km/h')} so với mặt đường; vận động viên (VĐV) dẫn đầu cách mô tô ${nw('10 km')}, sau ${nw('30 phút')} mô tô bắt kịp. Các xe chạy thẳng đều.<br><b>a)</b> vận tốc của mô tô so với VĐV dẫn đầu<br><b>b)</b> tốc độ của VĐV so với mặt đường<br><b>c)</b> quãng đường VĐV đi được trong ${nw('30 phút')}`,
    nd: `(1) mô tô · (2) ${f(25)} · (3) ${f(25)}; ${nw(`${v('13')} =`)} ${f(18)}`, a: ['a', 'b', 'c'], gi: 3, fig: sm(H.moTo(), 36) },
  { t: 'Dạng 5 · Trung bình · Cộng vận tốc vuông góc',
    de: `Ca nô chạy ${nw('14,4 km/h')} so với nước, mũi luôn hướng đông, vuông góc bờ; sông rộng ${nw('200 m')}; nước chảy về phía nam ${nw('3 m/s')} so với bờ.<br><b>a)</b> độ lớn vận tốc của ca nô so với bờ<br><b>b)</b> thời gian qua sông<br><b>c)</b> điểm cập bến cách điểm đối diện bao xa`,
    nd: `${nw(`${m('14{,}4\\ \\mathrm{km/h}=')} ${f(12)}&nbsp;m/s`)}; chỉ ${f(14)} đưa ca nô sang bờ bên kia`, a: ['a', 'b', 'c'], gi: 3, fig: sm(H.caNoD5(), 36) },
  { t: 'Dạng 6 · Khó · Chọn hướng mũi để tới đúng điểm đối diện',
    de: `Ca nô ${nw('4 m/s')} so với nước (không đổi) đi từ A sang B đối diện. Lần 1 mũi hướng thẳng tới B: sau ${nw('100 s')} cập bờ ở C, cách B ${nw('200 m')} về hạ lưu. Lần 2 mũi theo AD lệch về thượng lưu, cập đúng B.<br><b>a)</b> từ lần 1: vận tốc của nước<br><b>b)</b> góc giữa AD và AB<br><b>c)</b> thời gian qua sông lần 2`,
    nd: `Lần 2: ${vv('13')} ⊥ bờ ⇒ ${vv('12')} là cạnh ${f(25)}`, a: ['a', 'b', 'c'], gi: 3, fig: sm(H.caNoD6(), 36) },
];

// Bài tương tự giải vào vở (thầy chốt 10/11): 1 cột; ô đáp số 25 mm đặt cuối đúng dòng của ý, nhãn ô khớp a) b) c)…
// (a<sub>1</sub>, a<sub>2</sub> khi ý có 2 kết quả). Mỗi dạng 2 bài; đáp số tính bằng Python 13/11/2026, in lật ngược cuối trang.
const oY = (s, o, w = 25) => s.split('<br>').map((p) => {
  const y = p.match(/^<b>([a-d])\)<\/b>/);
  if (!y) return `<div>${p}</div>`;
  const ls = o.filter((l) => l[0] === y[1]);
  return `<div class="yo"><span>${p}</span><span class="oo">${ls.map((l) => `<span class="nw"><b>${l})</b>${f(w)}</span>`).join('')}</span></div>`;
}).join('');
const ttDe = (b) => b.fig ? `<div class="fig-side" style="grid-template-columns:1fr ${b.fw}mm">${`<div>${oY(b.de, b.o, b.ow)}</div>`}${b.fig}</div>` : oY(b.de, b.o, b.ow);
const nhap = (n) => ({ t: '<span class="nhap-t">Nháp / chỗ em còn vướng</span>', de: lines(n), k: 0 });
const vaoVo = (ds) => ds.map((b) => (b.o ? { t: b.t, de: ttDe(b), k: 0 } : b));
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–3', 'DẠNG 4–6'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Xe đạp đi trên đường thẳng, không đổi chiều: ${nw('20 phút')} đầu với ${nw('18 km/h')}, ${nw('10 phút')} sau với ${nw('12 km/h')}.<br><b>a)</b> quãng đường cả chuyến (km)<br><b>b)</b> tốc độ trung bình (km/h)<br><b>c)</b> tốc độ trung bình (m/s)`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 1 · Bài 2', de: `Ô tô đi quãng đường thẳng ${nw('60 km')}: nửa đầu quãng đường với ${nw('30 km/h')}, nửa sau với ${nw('60 km/h')}.<br><b>a)</b> thời gian đi nửa đầu (ô 1), nửa sau (ô 2)<br><b>b)</b> tốc độ trung bình cả quãng<br><b>c)</b> ${m('(30+60):2')} có bằng kết quả b) không?`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'] },
    { t: 'Dạng 2 · Bài 1', de: `Từ cổng trường, An đi ${nw('300 m')} về hướng bắc rồi rẽ vuông góc đi ${nw('400 m')} về hướng đông, hết tất cả ${nw('250 s')}.<br><b>a)</b> quãng đường<br><b>b)</b> độ lớn độ dịch chuyển<br><b>c)</b> tốc độ trung bình<br><b>d)</b> độ lớn vận tốc trung bình`, o: ['a', 'b', 'c', 'd'] },
    { t: 'Dạng 2 · Bài 2', de: `Xe chạy nửa vòng tròn bán kính ${nw('50 m')} từ A tới B (AB là đường kính) hết ${nw('20 s')}; lấy ${nw(m('\\pi=3{,}14'))}.<br><b>a)</b> quãng đường<br><b>b)</b> độ lớn độ dịch chuyển<br><b>c)</b> tốc độ trung bình<br><b>d)</b> độ lớn vận tốc trung bình`, o: ['a', 'b', 'c', 'd'] },
    { t: 'Dạng 3 · Bài 1', de: `Trên đường thẳng, Bình chạy từ A tới B cách ${nw('600 m')} hết ${nw('200 s')}, rồi quay lại tới C là trung điểm AB hết ${nw('100 s')}. Chiều dương từ A tới B.<br><b>a)</b> quãng đường (ô 1) và độ dịch chuyển (ô 2) cả quá trình<br><b>b)</b> tốc độ trung bình<br><b>c)</b> vận tốc trung bình`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'] },
    { t: 'Dạng 3 · Bài 2', de: `Bể bơi dài ${nw('25 m')}: bơi đầu → cuối hết ${nw('20 s')}, cuối → đầu hết ${nw('25 s')}. Chiều dương: đầu → cuối.<br><b>a)</b> vận tốc trung bình lượt về<br><b>b)</b> tốc độ trung bình cả đi lẫn về<br><b>c)</b> vận tốc trung bình cả đi lẫn về`, o: ['a', 'b', 'c'] },
  ], [
    { t: 'Dạng 4 · Bài 1', de: `Tàu chạy ${nw('12 m/s')} so với đường ray; Minh đi trong toa ${nw('1,5 m/s')} so với toa. Vận tốc của Minh so với đường ray khi Minh đi:<br><b>a)</b> về phía đầu tàu<br><b>b)</b> về phía cuối tàu`, o: ['a', 'b'] },
    { t: 'Dạng 4 · Bài 2', de: `Ô tô chạy ${nw('54 km/h')} đuổi theo xe tải chạy cùng chiều ${nw('36 km/h')}, lúc đầu cách nhau ${nw('2 km')}; hai xe chạy thẳng đều.<br><b>a)</b> vận tốc của ô tô so với xe tải<br><b>b)</b> thời gian đuổi kịp (phút)<br><b>c)</b> quãng đường ô tô đi đến lúc đuổi kịp`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 5 · Bài 1', de: `Thuyền chạy ${nw('1,2 m/s')} so với nước, mũi luôn vuông góc bờ; nước chảy ${nw('0,5 m/s')}; sông rộng ${nw('60 m')}.<br><b>a)</b> độ lớn vận tốc của thuyền so với bờ<br><b>b)</b> thời gian qua sông<br><b>c)</b> điểm cập bến cách điểm đối diện bao xa`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 5 · Bài 2', de: `Máy bay bay ${nw('240 km/h')} so với không khí, mũi hướng bắc; gió thổi về phía đông ${nw('70 km/h')} so với mặt đất.<br><b>a)</b> độ lớn vận tốc máy bay so với mặt đất<br><b>b)</b> góc lệch của đường bay khỏi hướng bắc<br><b>c)</b> sau ${nw('2 h')}, máy bay lệch về phía đông bao xa`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 6 · Bài 1', de: `Ca nô chạy ${nw('2,6 m/s')} so với nước, nước chảy ${nw('1,0 m/s')}, sông rộng ${nw('120 m')}. Muốn cập bến đúng điểm đối diện:<br><b>a)</b> độ lớn vận tốc ca nô so với bờ<br><b>b)</b> góc lệch của mũi về thượng lưu (so với phương vuông góc bờ)<br><b>c)</b> thời gian qua sông`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 6 · Bài 2', de: `Thuyền chạy ${nw('2,0 m/s')} so với nước. Lần 1, mũi vuông góc bờ: sau ${nw('50 s')} cập bờ cách điểm đối diện ${nw('60 m')} về hạ lưu. Lần 2, mũi lệch lên thượng lưu để cập đúng điểm đối diện.<br><b>a)</b> vận tốc của nước<br><b>b)</b> chiều rộng sông<br><b>c)</b> góc lệch của mũi ở lần 2<br><b>d)</b> thời gian qua sông lần 2`, o: ['a', 'b', 'c', 'd'] },
    nhap(1),
  ]],
  dap: [
    `D1·1: a) 8 km · b) 16 km/h · c) 4,44 m/s &nbsp;|&nbsp; D1·2: a<sub>1</sub>) 1 h · a<sub>2</sub>) 0,5 h · b) 40 km/h · c) không (${m('45\\neq 40')}) &nbsp;|&nbsp; D2·1: a) 700 m · b) 500 m · c) 2,8 m/s · d) 2,0 m/s &nbsp;|&nbsp; D2·2: a) 157 m · b) 100 m · c) 7,85 m/s · d) 5,0 m/s &nbsp;|&nbsp; D3·1: a<sub>1</sub>) 900 m · a<sub>2</sub>) +300 m · b) 3,0 m/s · c) +1,0 m/s &nbsp;|&nbsp; D3·2: a) ${m('-1{,}0')} m/s · b) 1,11 m/s · c) 0`,
    `D4·1: a) 13,5 m/s · b) 10,5 m/s, theo chiều tàu &nbsp;|&nbsp; D4·2: a) 18 km/h · b) ≈ 6,7 phút (400 s) · c) 6 km &nbsp;|&nbsp; D5·1: a) 1,3 m/s · b) 50 s · c) 25 m &nbsp;|&nbsp; D5·2: a) 250 km/h · b) ≈ 16,3° về phía đông · c) 140 km &nbsp;|&nbsp; D6·1: a) 2,4 m/s · b) ≈ 22,6° · c) 50 s &nbsp;|&nbsp; D6·2: a) 1,2 m/s · b) 100 m · c) ≈ 36,9° · d) 62,5 s`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 3], kq: [[1, 2, 3], [4, 5, 6]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'tốc độ TB 1·4 · đo tốc độ 2·1 · tức thời 2·2 · vận tốc 2·3 · tương đối 3·1 · cộng vận tốc 3·2 · bẫy 4·2 · bài toán mẫu 5·1 · dạng 1–3 → 6·1 · dạng 4–6 → 7·1',
  out: process.argv[2],
});
