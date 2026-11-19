// Ruột tập VL12 Chương 3 – Bài 16 · Điện từ trường. Mô hình sóng điện từ (lesson id 127). Quyển Chương 3 lớp 12: bài 9 = tr. 1–12,
// bài 16 = tr. 85–96. KHÁC bai16.mjs (bài 16 Chương 4 hạt nhân) — file và PDF đặt tên có '-c3-' để không ghi đè.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l12-c3-bai16.mjs (toàn bộ SVG tự vẽ). Nội dung theo bài web (book/cache/127.json, tải từ DB 12/11/2026): mục tiêu,
// dự đoán bếp từ – radio, II.1–II.5, thí nghiệm nam châm rơi qua ống dây + bảng I theo f của mạch có tụ, ba bẫy, Trả bài 5 câu,
// bài toán mẫu đài FM qua vệ tinh địa tĩnh, thử thách ⭐–⭐⭐⭐, 6 dạng bài tập mẫu. Đáp số Bài tương tự tính bằng Python 12/11/2026.
// Chạy: node scripts/ruot-tap/l12-c3-bai16.mjs            → scripts/ruot-tap/out/ruot-tap-vl12-c3-bai16.pdf
//       node scripts/ruot-tap/l12-c3-bai16.mjs --hinh     → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l12-c3-bai16/ để soát chữ/nét
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL12c3b16 as H } from './hinh-l12-c3-bai16.mjs';
const HERE = dirname(fileURLToPath(import.meta.url));

if (process.argv[2] === '--hinh') {
  const { createRequire } = await import('node:module');
  const { existsSync, mkdirSync, writeFileSync } = await import('node:fs');
  const { pathToFileURL } = await import('node:url');
  const BOOK = [resolve(HERE, '../../book/'), '/Users/MAC/Projects/thachlab/book'].find((d) => existsSync(d + '/node_modules')) + '/';
  const puppeteer = createRequire(BOOK + 'package.json')('puppeteer-core');
  const F = resolve(HERE, 'fonts') + '/source-sans-3-';
  const css = ['latin', 'latin-ext', 'vietnamese'].flatMap((s) => [400, 700].map((w) => `@font-face{font-family:BV;font-weight:${w};src:url("${pathToFileURL(`${F}${s}-${w}-normal.woff2`).href}")}`)).join('')
    + 'body{margin:0;font-family:BV,sans-serif;zoom:4}.fig{margin:0;width:46mm;border:.3mm solid #d3dbec;border-radius:1.5mm;padding:1mm 1.5mm .6mm;background:#fff}.fig svg{display:block;width:100%;height:auto}figcaption{font-size:2.95mm;color:#5f6a88;line-height:1.3;margin-top:.4mm}';
  const out = resolve(HERE, 'out/hinh-l12-c3-bai16'); mkdirSync(out, { recursive: true });
  const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true, args: ['--allow-file-access-from-files'] });
  const pg = await b.newPage();
  const kcss = pathToFileURL(BOOK + 'node_modules/katex/dist/katex.min.css').href;
  for (const [name, fn] of Object.entries(H)) {
    writeFileSync(out + '/_tmp.html', `<!doctype html><meta charset="utf-8"><link rel="stylesheet" href="${kcss}"><style>${css}</style><span class="katex" style="position:absolute;opacity:0">x</span>${fn()}`);
    await pg.goto(pathToFileURL(out + '/_tmp.html').href, { waitUntil: 'networkidle0' });
    await pg.evaluate('document.fonts.ready');
    await (await pg.$('.fig')).screenshot({ path: `${out}/${name}.png` });
    console.log(`${name}.png`);
  }
  await b.close();
  process.exit(0);
}

const K = khoiTao({ bai: 16, lid: 127, ten: 'ĐIỆN TỪ TRƯỜNG · MÔ HÌNH SÓNG ĐIỆN TỪ', lop: 12, baiDau: 9, sub: 'Vật lí 12 · Chương 3: Từ trường' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const cC = nw(m('c=3\\cdot10^8\\ \\mathrm{m/s}'));
const vE = m('\\vec E'), vB = m('\\vec B'), lam = m('\\lambda');
const u = (s, d) => nw(m(`${s}\\ \\mathrm{${d}}`));

const ttCss = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';

const p1 = `${ttCss}<section class="page">
${head('BÀI 16 · ĐIỆN TỪ TRƯỜNG · MÔ HÌNH SÓNG ĐIỆN TỪ', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Nêu được cái gì sinh ra <b>điện trường xoáy</b>, thế nào là <b>dòng điện dịch</b>`)}
${dong(`${ck}Nói được <b>điện từ trường</b> là gì và quan hệ giữa ${vE}, ${vB} tại một điểm`)}
${dong(`${ck}Mô tả sự tạo thành, tính chất <b>sóng điện từ</b>; tính bước sóng, tần số, chu kì`)}
${dong(`${ck}Đọc <b>thang sóng điện từ</b>: sáu vùng sóng và ứng dụng chính`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Mỗi lần bếp từ bật lên nấu, chiếc radio chạy pin cách đó hai mét lại rè, dù không có dây nào nối chúng. Vì sao?</p>
<div class="fig-side" style="${fs(42)}"><div>
${opt('A', 'Nhiệt từ mặt bếp truyền trong không khí làm radio rè')}
${opt('B', 'Dòng nhiễu theo dây điện chung sang radio')}
${opt('C', 'Dòng biến thiên trong bếp sinh ra thứ gì đó lan tới ăng ten')}
${opt('D', 'Sóng âm của bếp biến thành sóng điện từ ở ăng ten')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 1)}</div>
${H.bepTu()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Từ trường biến thiên sinh điện trường xoáy', '1·4')}
<div class="card fig-side" style="${fs(40)};padding:1.2mm 3mm"><div>
<div>Vùng có từ trường ${f(22)} theo thời gian thì xuất hiện ${f(30)}.</div>
<div>Đường sức của nó là đường ${f(18)}, bao quanh các ${f(30)}.</div>
<div style="margin-top:.6mm"><b>Thí nghiệm.</b> Thả nam châm rơi qua ống dây, lần chậm rồi lần nhanh; sau đó giữ yên nam châm trong lòng ống.</div>
<div><b>Quan sát:</b> nam châm chuyển động: kim ${f(16)}; thả nhanh: kim lệch ${f(14)}; giữ yên: kim chỉ ${f(10)}</div>
<div><b>Rút ra:</b> thứ gây ra điện trường trong dây là ${f(30)}, không phải ${f(28)}.</div>
<div><b>Chưa nói được:</b> kim không cho biết ${f(40)}</div></div>
${H.namCham()}</div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('DÒNG ĐIỆN DỊCH · ĐIỆN TỪ TRƯỜNG')}
${h3(1, 'II.2 · Điện trường biến thiên sinh từ trường', '2·1')}
<div class="card fig-side" style="${fs(42)};padding:1.2mm 3mm"><div>
<div>Tụ tích hoặc phóng điện: điện tích hai bản ${f(16)} nên giữa hai bản có điện trường ${f(20)}.</div>
<div>Điện trường đó tương đương một dòng điện chạy qua tụ, gọi là ${f(30)}.</div>
<div>Dòng điện dịch gây ra ${f(22)} có đường sức ${f(16)}, bao quanh các đường sức điện.</div></div>
${H.tuXoayChieu()}</div>
${h3(2, 'Thí nghiệm: dòng xoay chiều qua mạch có tụ', '2·2')}
<div class="card" style="padding:1.2mm 3mm">
<div style="margin-bottom:.6mm">Giữ ${u('U=12', 'V')}, ${u('C=1', '\\mu F')}, đổi tần số ${m('f')} của nguồn, đọc ampe kế. Tính cột ${m('I/f')} (lấy 3 chữ số sau dấu phẩy).</div>
<table class="tbl-ct"><tr><th>${m('f')} (Hz)</th><th>50</th><th>100</th><th>200</th><th>400</th><th>800</th></tr>
<tr><td>${m('I')} (mA)</td><td>3,6</td><td>7,4</td><td>14,8</td><td>29,5</td><td>58,0</td></tr>
<tr><td>${m('I/f')} (mA/Hz)</td><td>0,072</td><td></td><td></td><td></td><td></td></tr></table>
<div style="margin-top:.6mm"><b>Rút ra:</b> ${m('I/f')} gần như ${f(22)} ⇒ dòng qua tụ tỉ lệ ${f(16)} với ${m('f')}.</div>
<div>Giữa hai bản là chất cách điện, mạch vẫn có dòng vì giữa hai bản có ${f(46)}.</div>
<div><b>Đối chiếu</b> (công thức cho sẵn, không cần nhớ): ${m('I=U\\cdot2\\pi fC')} ⇒ ${nw(`${m('I/f=U\\cdot2\\pi C\\approx')} ${f(20)} mA/Hz`)}; số đo thấp hơn vì ${f(36)}</div>
</div>
${h3(3, 'II.3 · Điện từ trường', '2·3')}
<div class="card" style="padding:1.2mm 3mm">
<div>Maxwell: từ trường biến thiên sinh ${f(28)} và ngược lại; hai trường là hai mặt của một trường thống nhất gọi là ${f(28)}.</div>
<div>Hai trường không tách riêng được: chúng cùng tồn tại và ${f(30)} qua lại.</div>
<div>Điện trường tĩnh, từ trường của nam châm đứng yên ${f(16)} phải điện từ trường, vì ${f(40)}</div>
</div>
${h3(4, 'Làm nhanh', '2·4')}
${box(`<div style="padding-top:1mm"><b>Câu 1.</b> Về thí nghiệm mạch có tụ ở trên, phát biểu nào <b>sai</b>?</div>
${opt('A', `Tần số càng lớn, dòng càng mạnh; ${m('I/f')} gần như không đổi`)}
${opt('B', 'Mạch vẫn có dòng dù giữa hai bản tụ là chất cách điện')}
${opt('C', 'Mạch có dòng vì điện tích chạy xuyên qua lớp cách điện')}
${opt('D', 'Thí nghiệm không cho biết hình dạng từ trường của dòng điện dịch')}
<div>${chon(10)}</div>`)}
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('SÓNG ĐIỆN TỪ · THANG SÓNG ĐIỆN TỪ')}
${h3(1, 'II.4 · Sự tạo thành và lan truyền sóng điện từ', '3·1')}
<div class="card fig-side" style="${fs(44)};padding:1.2mm 3mm"><div>
<div>Tại O có điện trường biến thiên ${m('E_1')}: ${m('E_1')} sinh ra ${f(12)}; ${m('B_1')} biến thiên lại sinh ra ${f(12)}; cứ thế lan ra xa thành ${f(26)}.</div>
<div>Sóng điện từ là sóng ${f(14)}: ${vE} ${f(16)} ${vB}, cả hai ${f(16)} phương truyền.</div>
<div>${vE} và ${vB} biến thiên điều hoà, luôn ${f(18)}.</div>
<div>Chân không ${cC}; môi trường khác: ${nw(`${m('v')} ${f(8)} ${m('c')}`)}.</div>
<div style="display:flex;gap:4mm;align-items:flex-end;margin:.6mm 0">${nw(`Chân không: ${m('\\lambda=')}<span class="fill" style="min-width:22mm;height:10mm"></span>`)} ${nw(`Môi trường: ${m('\\lambda=')}<span class="fill" style="min-width:14mm;height:10mm"></span>`)}</div>
<div>Mang ${f(18)}: tần số càng cao, ${f(24)}.</div>
<div>Tuân theo: truyền thẳng, phản xạ, ${f(14)}, ${f(14)}, nhiễu xạ.</div></div>
${H.songEB()}</div>
${h3(2, 'II.5 · Thang sóng điện từ', '3·2')}
<div class="fig-side" style="${fs(46)}"><div>
<table class="tsong" style="font-size:var(--fs-sm)"><style>.tsong td{height:5.6mm}</style><tr><th style="width:7mm">Số</th><th style="width:22mm">Tên vùng</th><th style="width:27mm">Bước sóng</th><th>Gặp ở đâu</th></tr>
<tr><td>(1)</td><td></td><td>1 mm – hàng km</td><td></td></tr>
<tr><td>(2)</td><td></td><td>0,76 µm – 1 mm</td><td></td></tr>
<tr><td>(3)</td><td></td><td>0,38 – 0,76 µm</td><td></td></tr>
<tr><td>(4)</td><td></td><td>10 nm – 0,38 µm</td><td></td></tr>
<tr><td>(5)</td><td></td><td>0,01 – 10 nm</td><td></td></tr>
<tr><td>(6)</td><td></td><td>dưới 0,01 nm</td><td></td></tr></table>
<div style="font-size:var(--fs-sm);margin-top:.4mm"><b>Chọn tên:</b> tia X · vô tuyến · gamma · tử ngoại · hồng ngoại · ánh sáng nhìn thấy. <b>Chỗ gặp:</b> đèn diệt khuẩn · wifi, điện thoại · chụp xương · mắt thấy · điều khiển TV · xạ trị</div>
<div style="font-size:var(--fs-sm);margin-top:.4mm">Đổi: ${nw(m('1\\ \\mathrm{mm}=10^{-3}\\ \\mathrm m'))} · ${nw(m('1\\ \\mu\\mathrm m=10^{-6}\\ \\mathrm m'))} · ${nw(m('1\\ \\mathrm{nm}=10^{-9}\\ \\mathrm m'))}</div>
<div>Mọi vùng cùng bản chất, trong chân không cùng tốc độ ${f(8)}; bước sóng càng nhỏ, năng lượng càng ${f(12)}.</div>
<div>Mẹo nhớ sáu vùng (bước sóng giảm dần): ${f(50)}</div></div>
${H.thangSong()}</div>
${h3(3, 'Làm nhanh', '3·3')}
${box(cau(`<b>Câu 1.</b> Lò vi sóng phát sóng ${u('2{,}45', 'GHz')} ${nw(`(${cC})`)}. Bước sóng bằng bao nhiêu xentimét? Thuộc vùng nào?`, 1)
 + cau(`<b>Câu 2.</b> Tại một điểm có sóng điện từ, lúc ${m('E')} đạt cực đại thì ${m('B')} thế nào? Vì sao?`, 1))}
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('BA CÁI BẪY · TRẢ BÀI · TỰ KIỂM TRA')}
${h3(1, 'III · Ba cái bẫy hay sập', '4·1')}
<div class="card fig-side" style="${fs(42)};padding:1mm 3mm"><div>
<div class="trap">${ck}<span><b>“Điện trường xoáy cũng như điện trường tĩnh.”</b> Hình (1): điện trường ${f(14)}, do ${f(42)}; hình (2): điện trường ${f(14)}, do ${f(42)}</span></div>
<div class="trap">${ck}<span><b>“Sóng điện từ cần môi trường để truyền.”</b> Ánh sáng Mặt Trời đi ${nw(m('1{,}5\\cdot10^{11}\\ \\mathrm m'))} gần như chân không tới Trái Đất ${nw(`(${cC})`)} mất ${nw(`${m('t=s/c=')} ${f(14)} s`)}.</span></div>
<div class="trap">${ck}<span><b>“${vE}, ${vB} lệch pha như ${m('u')}, ${m('i')} của tụ.”</b> Trong sóng điện từ, khi ${nw(m('E=0'))} thì ${nw(`${m('B=')} ${f(12)}`)}.</span></div></div>
${H.duongSuc()}</div>
${h3(2, 'IV · Trả bài 5 câu', '4·2')}
${box(`${tb('1. Từ trường biến thiên sinh ra gì? Đường sức của nó dạng nào?')}${lines(2)}
${tb('2. Điện trường biến thiên sinh ra gì? Dòng điện dịch là gì?')}${lines(3)}
${tb('3. Điện từ trường là gì? Có tách riêng hai trường được không?')}${lines(2)}
${tb('4. Sóng điện từ tạo thành thế nào? Tính chất và công thức bước sóng.')}${lines(3)}
${tb('5. Sáu vùng của thang sóng điện từ theo bước sóng giảm dần.')}${lines(2)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/5 câu · chưa thuộc: ${f(25)} ${nw(`→ đọc lại ô ${f(12)} Tập`)}</div>
${h3(3, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '4·3')}
${rkHai([1, 2, 3, 4], [5, 6, 7, 8])}
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TOÁN MẪU · BÀI TẬP VỀ NHÀ · THỬ THÁCH')}
${h3(1, 'V · Bài toán mẫu: đài FM 100 MHz và vệ tinh địa tĩnh', '5·1')}
<div class="card soft" style="padding:1.2mm 3mm">Đài FM phát ở ${u('100', 'MHz')}, máy thu cách đài ${u('30', 'km')}. Tín hiệu lên vệ tinh địa tĩnh ở độ cao ${u('35\\,786', 'km')} rồi phát thẳng xuống máy thu. Coi như chân không, ${cC}, bỏ qua thời gian xử lí ở vệ tinh. <b>a)</b> Tính bước sóng. <b>b)</b> Tín hiệu đi qua vệ tinh mất bao lâu? <b>c)</b> Bước sóng thuộc vùng nào? Tia X dài hơn hay ngắn hơn?</div>
<table><tr><th style="width:46mm">Câu trong đề</th><th>Dữ liệu → kiến thức</th></tr>
<tr><td>“phát ở 100 MHz”</td><td>${m('f=10^8\\ \\mathrm{Hz}')} → ${m('\\lambda=c/f')}</td></tr>
<tr><td style="height:6.5mm">“cách đài 30 km”</td><td></td></tr>
<tr><td style="height:6.5mm">“độ cao 35 786 km”</td><td></td></tr>
</table>
<div class="fig-side" style="${fs(40)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl(`a) ${m('\\lambda=')}`, 1)}${wl('b) Quãng đường, thời gian:', 3)}${wl('c) Vùng; so với tia X:', 1)}</div>${H.veTinh()}</div>
${h3(2, 'Điền bước còn thiếu: vẫn vệ tinh đó, đài phát ở 120 MHz', '5·2')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div class="ln"><b>Bước 1 (cho sẵn):</b> ${m('f=1{,}2\\cdot10^8\\ \\mathrm{Hz}')}</div>
${wl(`Bước 2: ${m('\\lambda=c/f=')}`, 1)}${wl('Bước 3: thời gian qua vệ tinh có đổi so với câu b? Vì sao?', 1)}${lines(1)}</div>
${K.btvn().replace('<i>1</i>', '<i>3</i>')}
${h3(4, 'Thử thách phân tầng', '5·4')}
${box(cau(`${m('\\bigstar')} Sóng wifi ${u('2{,}4', 'GHz')} có bước sóng bao nhiêu xentimét?`, 1)
 + cau(`${m('\\bigstar\\bigstar')} Ánh sáng đỏ ${u('0{,}75', '\\mu m')} (chân không) vào thuỷ tinh ${nw(m('n=1{,}5'))}: ${m('f')}, ${m('v')}, ${lam} đổi thế nào?`, 2)
 + cau(`${m('\\bigstar\\bigstar\\bigstar')} Gọi nhau qua vệ tinh địa tĩnh: vì sao hai người hay nói chồng lên nhau?`, 1))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Điện trường xoáy: nguồn gây ra và dạng đường sức',
    de: 'Nam châm thẳng rơi vào lòng ống dây nối kín với điện kế nhạy: khi nam châm chuyển động trong lòng ống, kim lệch; khi giữ yên nam châm trong lòng ống, kim chỉ vạch 0.<br><b>a)</b> điện trường trong dây dẫn do nguyên nhân nào gây ra<br><b>b)</b> đường sức của điện trường đó có dạng nào',
    nd: `Hai lúc khác nhau ở ${f(20)}; không do điện tích sinh ra ⇒ đường sức ${f(15)}`, a: ['a', 'b'], cot: 2, gi: 3 },
  { t: 'Dạng 2 · Dễ · Bước sóng, chu kì và tần số của sóng điện từ',
    de: `Kênh FM phát sóng tần số ${u('91', 'MHz')}; điều khiển quạt trần dùng LED hồng ngoại bước sóng ${u('940', 'nm')}. Coi không khí như chân không, ${cC}.<br><b>a)</b> bước sóng của sóng FM; <b>b)</b> chu kì của sóng FM<br><b>c)</b> tần số của sóng hồng ngoại`,
    nd: `Đổi MHz → Hz, nm → m trước; ${nw(`${m('\\lambda=')} ${f(24)}`)}; ${nw(`${m('T=')} ${f(20)}`)}`, a: ['a', 'b', 'c'], gi: 4 },
  { t: 'Dạng 3 · Trung bình · E và B cùng pha: tìm giá trị tức thời',
    de: `Tại M có sóng điện từ truyền qua; giá trị cực đại ${nw(m('E_0=18\\ \\mathrm{V/m}'))}, ${nw(m('B_0=60\\ \\mathrm{nT}'))}.<br><b>a)</b> khi ${nw(m('E=6{,}0\\ \\mathrm{V/m}'))}: độ lớn ${m('B')}<br><b>b)</b> khi ${nw(m('B=45\\ \\mathrm{nT}'))}: độ lớn ${m('E')}; <b>c)</b> khi ${nw(m('E=0'))}: ${m('B')} bằng bao nhiêu`,
    nd: `${vE}, ${vB} luôn ${f(16)} ⇒ ${nw(`${m('E/E_0=')} ${f(20)}`)} ở mọi thời điểm`, a: ['a', 'b', 'c'], gi: 5, fig: H.dongPha() },
  { t: 'Dạng 4 · Trung bình · Đổi môi trường: tần số, tốc độ, bước sóng',
    de: `Ánh sáng lục bước sóng ${u('540', 'nm')} trong chân không đi vào nước chiết suất ${nw(m('n=\\tfrac43'))}; ${cC}.<br><b>a)</b> tần số của ánh sáng; <b>b)</b> tốc độ truyền trong nước<br><b>c)</b> bước sóng trong nước`,
    nd: `Đổi môi trường: ${f(18)} giữ nguyên; ${nw(`${m('v=')} ${f(20)}`)}; ${nw(`${m("\\lambda'=")} ${f(24)}`)}`, a: ['a', 'b', 'c'], gi: 4 },
  { t: 'Dạng 5 · Khó · Thời gian truyền xung vô tuyến: ra-đa – Mặt Trăng',
    de: `Ra-đa phát xung vô tuyến tới Mặt Trăng rồi thu xung phản xạ; chân không, ${cC}.<br><b>a)</b> lần 1, ${nw(m('d=3{,}84\\cdot10^8\\ \\mathrm m'))}: thời gian xung đi tới Mặt Trăng<br><b>b)</b> lần 1: thời gian từ lúc phát đến lúc thu xung phản xạ<br><b>c)</b> lần 2 thu xung phản xạ sau ${u('2{,}50', 's')}: khoảng cách lúc đó`,
    nd: `Từ lúc phát đến lúc thu: xung đi ${f(16)} quãng đường; ${nw(`${m('d=')} ${f(22)}`)}`, a: ['a', 'b', 'c'], gi: 4, fig: H.raDa() },
  { t: 'Dạng 6 · Khó · Thời điểm đầu tiên E bằng 0 hoặc cực đại',
    de: `Tại một điểm có sóng điện từ, ${nw(m('B=B_0\\cos\\left(2\\pi\\cdot10^8t+\\tfrac{\\pi}{3}\\right)'))}, ${nw(m('B_0>0'))}, ${m('t')} (s). <b>a)</b> chu kì của sóng<br><b>b)</b> kể từ ${nw(m('t=0'))}, thời điểm đầu tiên ${m('E')} tại điểm đó bằng 0<br><b>c)</b> kể từ ${nw(m('t=0'))}, thời điểm đầu tiên ${m('E')} đạt cực đại`,
    nd: `${m('E')}, ${m('B')} ${f(20)}; ${m('E=0')} khi pha ${f(20)}; ${m('E=E_0')} khi pha ${f(20)}`, a: ['a', 'b', 'c'], gi: 4, fig: H.vongPha() },
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
const kc = nw(`(${cC})`);
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–3', 'DẠNG 4–6'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: 'Cuộn dây quấn quanh lõi sắt nối nguồn xoay chiều; vòng dây kín bao quanh lõi, không chạm cuộn dây.<br><b>a)</b> vòng dây có điện trường không; do đâu<br><b>b)</b> đường sức điện trường đó dạng nào<br><b>c)</b> đổi sang nguồn một chiều, dòng đã ổn định: còn điện trường không', o: ['a', 'b', 'c'], ow: { a: 45, b: 50, c: 16 } },
    { t: 'Dạng 1 · Bài 2', de: 'Tụ điện phẳng, giữa hai bản là không khí, nối với nguồn xoay chiều.<br><b>a)</b> giữa hai bản có điện trường biến thiên không<br><b>b)</b> điện trường đó sinh ra gì; tên “dòng” tương đương chạy qua tụ<br><b>c)</b> nối tụ vào nguồn một chiều, tụ đã tích đầy: giữa hai bản còn từ trường không', o: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], ow: { a: 16, 'b<sub>1</sub>': 26, 'b<sub>2</sub>': 34, c: 16 } },
    { t: 'Dạng 2 · Bài 1', de: `Đài phát thanh AM phát sóng tần số ${u('600', 'kHz')}; lò vi sóng dùng sóng bước sóng ${u('12{,}2', 'cm')}. Coi không khí như chân không ${kc}.<br><b>a)</b> bước sóng của sóng AM<br><b>b)</b> chu kì của sóng AM<br><b>c)</b> tần số sóng của lò vi sóng`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 2 · Bài 2', de: `Wifi phát sóng tần số ${u('5{,}0', 'GHz')}; đèn diệt khuẩn phát tia tử ngoại bước sóng ${u('254', 'nm')}. Coi không khí như chân không ${kc}.<br><b>a)</b> bước sóng của sóng wifi<br><b>b)</b> chu kì của sóng wifi<br><b>c)</b> tần số của tia tử ngoại`, o: ['a', 'b', 'c'], ow: { c: 32 } },
    { t: 'Dạng 3 · Bài 1', de: `Tại M có sóng điện từ truyền qua, ${nw(m('E_0=12\\ \\mathrm{V/m}'))}, ${nw(m('B_0=40\\ \\mathrm{nT}'))}.<br><b>a)</b> khi ${nw(m('E=3{,}0\\ \\mathrm{V/m}'))}: độ lớn ${m('B')}<br><b>b)</b> khi ${nw(m('B=30\\ \\mathrm{nT}'))}: độ lớn ${m('E')}<br><b>c)</b> khi ${m('B')} đạt cực đại: ${m('E')} bằng bao nhiêu`, fig: H.dongPha('Vạch dọc: lúc E = 3,0 V/m.', '3,0', 1 / 4), fw: 36, o: ['a', 'b', 'c'] },
    { t: 'Dạng 3 · Bài 2', de: `Tại N có sóng điện từ truyền qua, ${nw(m('E_0=150\\ \\mathrm{V/m}'))}, ${nw(m('B_0=0{,}50\\ \\mu\\mathrm T'))}.<br><b>a)</b> khi ${nw(m('E=60\\ \\mathrm{V/m}'))}: độ lớn ${m('B')}<br><b>b)</b> khi ${nw(m('B=0{,}35\\ \\mu\\mathrm T'))}: độ lớn ${m('E')}<br><b>c)</b> khi ${nw(m('B=0'))}: ${m('E')} bằng bao nhiêu`, o: ['a', 'b', 'c'] },
  ], [
    { t: 'Dạng 4 · Bài 1', de: `Ánh sáng đỏ bước sóng ${u('600', 'nm')} trong chân không đi vào thuỷ tinh chiết suất ${nw(m('n=1{,}5'))} ${kc}.<br><b>a)</b> tần số của ánh sáng<br><b>b)</b> tốc độ truyền trong thuỷ tinh<br><b>c)</b> bước sóng trong thuỷ tinh`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 4 · Bài 2', de: `Sóng vô tuyến tần số ${u('150', 'MHz')} truyền trong một sợi cáp với tốc độ ${nw(m('2{,}4\\cdot10^8\\ \\mathrm{m/s}'))} ${kc}.<br><b>a)</b> bước sóng của sóng này trong chân không<br><b>b)</b> bước sóng trong cáp<br><b>c)</b> sóng trong cáp chậm hơn trong chân không bao nhiêu lần`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 5 · Bài 1', de: `Ra-đa phát xung vô tuyến tới một máy bay, thu xung phản xạ sau ${u('120', '\\mu s')} kể từ lúc phát ${kc}.<br><b>a)</b> quãng đường xung đã đi (cả đi lẫn về)<br><b>b)</b> khoảng cách từ ra-đa tới máy bay<br><b>c)</b> máy bay cách ra-đa ${u('30', 'km')}: thu xung phản xạ sau bao lâu`, fig: H.mayBay(), fw: 36, o: ['a', 'b', 'c'] },
    { t: 'Dạng 5 · Bài 2', de: `Vệ tinh địa tĩnh ở độ cao ${u('36\\,000', 'km')}; trạm phát và trạm thu coi như ngay dưới vệ tinh ${kc}.<br><b>a)</b> thời gian tín hiệu đi từ trạm phát lên vệ tinh<br><b>b)</b> thời gian tín hiệu đi trạm phát → vệ tinh → trạm thu<br><b>c)</b> ánh sáng Mặt Trời tới Trái Đất mất ${u('500', 's')}: khoảng cách Mặt Trời – Trái Đất`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 6 · Bài 1', de: `Tại một điểm có sóng điện từ, ${nw(m('E=E_0\\cos\\left(2\\pi\\cdot10^7t+\\dfrac{\\pi}{4}\\right)'))}, ${nw(m('E_0>0'))}, ${m('t')} tính bằng giây.<br><b>a)</b> chu kì của sóng<br><b>b)</b> kể từ ${nw(m('t=0'))}, thời điểm đầu tiên ${m('B')} bằng 0<br><b>c)</b> kể từ ${nw(m('t=0'))}, thời điểm đầu tiên ${m('B')} đạt cực đại`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 6 · Bài 2', de: `Tại một điểm có sóng điện từ, ${nw(m('B=B_0\\cos\\left(2\\pi\\cdot10^8t-\\dfrac{\\pi}{3}\\right)'))}, ${nw(m('B_0>0'))}, ${m('t')} tính bằng giây.<br><b>a)</b> chu kì của sóng<br><b>b)</b> kể từ ${nw(m('t=0'))}, thời điểm đầu tiên ${m('E')} bằng 0<br><b>c)</b> kể từ ${nw(m('t=0'))}, thời điểm đầu tiên ${m('E')} đạt cực đại`, o: ['a', 'b', 'c'] },
  ]],
  dap: [
    `D1·1: a) có, do từ trường biến thiên · b) đường cong kín, bao quanh đường cảm ứng từ · c) không &nbsp;|&nbsp; D1·2: a) có · b<sub>1</sub>) từ trường · b<sub>2</sub>) dòng điện dịch · c) không &nbsp;|&nbsp; D2·1: a) 500 m · b) 1,67 ${m('\\mu')}s · c) 2,46 GHz &nbsp;|&nbsp; D2·2: a) 6,0 cm · b) 0,20 ns · c) 1,18·10<sup>15</sup> Hz &nbsp;|&nbsp; D3·1: a) 10 nT · b) 9,0 V/m · c) 12 V/m &nbsp;|&nbsp; D3·2: a) 0,20 ${m('\\mu')}T · b) 105 V/m · c) 0`,
    `D4·1: a) 5,0·10<sup>14</sup> Hz · b) 2,0·10<sup>8</sup> m/s · c) 400 nm &nbsp;|&nbsp; D4·2: a) 2,0 m · b) 1,6 m · c) 1,25 lần &nbsp;|&nbsp; D5·1: a) 3,6·10<sup>4</sup> m · b) 18 km · c) 200 ${m('\\mu')}s &nbsp;|&nbsp; D5·2: a) 0,12 s · b) 0,24 s · c) 1,5·10<sup>11</sup> m &nbsp;|&nbsp; D6·1: a) 100 ns · b) 12,5 ns · c) 87,5 ns &nbsp;|&nbsp; D6·2: a) 10 ns · b) 4,17 ns · c) 1,67 ns`,
  ],
};

const nbsp = (s) => s.replace(/: /g, ':&nbsp;').replace(/\) /g, ')&nbsp;').replace(/(\d|<\/sup>) (?=[A-Za-zµ<])/g, '$1&nbsp;');
await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 3], kq: [[1, 2, 3], [4, 5, 6]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo), dap: tuongTu.dap.map(nbsp) },
  tra: 'điện trường xoáy 1·4 · dòng điện dịch 2·1 · mạch có tụ 2·2 · điện từ trường 2·3 · sóng điện từ 3·1 · thang sóng 3·2 · bẫy 4·1 · bài toán mẫu 5·1 · dạng 1–3 → 6·1 · dạng 4–6 → 7·1',
  out: process.argv[2] ?? resolve(HERE, 'out/ruot-tap-vl12-c3-bai16.pdf'),
});
