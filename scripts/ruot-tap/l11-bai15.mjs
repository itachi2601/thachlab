// Ruột tập VL11 – Bài 15 · Thực hành: đo tốc độ truyền âm bằng ống cộng hưởng (lesson id 34). Quyển Chương 2 lớp 11: bài 15 = tr. 85–96 (baiDau 8).
// Khung: khung.mjs (bố cục bài 14: 1–5 học · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Bài THỰC HÀNH: tr.1–5 = nhắc lại · cột khí cộng hưởng + dụng cụ · các bước + bẫy · số liệu + sai số nguồn · tính λ, v, Δv + báo cáo.
// Nội dung theo bài web (book/cache/34.json, tải 13/11/2026). Đáp số mọi bài (BTM, tương tự) tính bằng Python 13/11/2026.
// Chạy: node scripts/ruot-tap/l11-bai15.mjs [file.pdf]   → scripts/ruot-tap/out/ruot-tap-vl11-bai15.pdf
//       node scripts/ruot-tap/l11-bai15.mjs --hinh       → chụp từng hình ở cỡ in vào out/hinh-l11-bai15/
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL11b15 as H } from './hinh-l11-bai15.mjs';

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
  const out = resolve(HERE, 'out/hinh-l11-bai15'); mkdirSync(out, { recursive: true });
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

const OFF = (15 - 8) * 12;
const K = khoiTao({ bai: 15, lid: 34, lop: 11, baiDau: 8, ten: 'THỰC HÀNH: ĐO TỐC ĐỘ TRUYỀN ÂM', sub: 'Vật lí 11 · Chương 2: Sóng' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const lam = m('\\lambda'), v = m('v'), fr = m('f'), l1 = m('l_1'), l2 = m('l_2'), e = m('e'), I0 = m('I_0');
const cm = (s) => nw(m(`${s}\\ \\mathrm{cm}`)), ms = (s) => nw(m(`${s}\\ \\mathrm{m/s}`)), Hz = (s) => nw(m(`${s}\\ \\mathrm{Hz}`));
const dv = nw(`${lam}, ${e}, ${m('l')}: cm · ${v}: m/s · ${fr}: Hz`);
const tall = (w) => `<span class="fill" style="min-width:${w}mm;height:10mm"></span>`;
const tk = nw(`${m('v_{tk}\\approx331+0{,}6\\,t')} (${m('t')}: °C)`);

const ttCss = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';

const p1 = `${ttCss}<section class="page">
${head('BÀI 15 · THỰC HÀNH: ĐO TỐC ĐỘ TRUYỀN ÂM', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Giải thích vì sao mực nước khác nhau thì tiếng thổi qua miệng chai khác nhau`)}
${dong(`${ck}Nêu phương án đo ${v} bằng ống cộng hưởng và chỗ dễ sai`)}
${dong(`${ck}Từ bảng số đo tính ${lam}, ${v}; viết kết quả kèm sai số`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Chai A nhiều nước nhất, chai C ít nước nhất. Thổi ngang miệng cả ba chai, tiếng kêu của chai A so với chai C:</p>
<div class="fig-side" style="${fs(48)}"><div>
${opt('A', 'Thấp hơn, vì chai A chứa nhiều nước nên nặng hơn')}
${opt('B', 'Như nhau, vì ba chai cùng một loại')}
${opt('C', 'Cao hơn, vì cột không khí trong chai A ngắn hơn')}
${opt('D', 'Cao hơn, vì nước sóng sánh làm tiếng to hơn')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 1)}</div>
${H.chai()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Nhắc lại: âm của tai và âm của máy đo', '1·4')}
<div class="card" style="padding:1.2mm 3mm">
<div>Ghép cảm giác với đại lượng vật lí: độ cao ↔ ${f(24)} · độ to ↔ ${f(30)} · âm sắc ↔ ${f(30)}</div>
<div style="margin-top:.6mm">${nw(`${m('L=10\\lg\\dfrac{I}{I_0}')}`)} (dB), ${nw(m('I_0=10^{-12}\\ \\mathrm{W/m^2}'))} (ngưỡng nghe; ${m('\\lg')} là logarit thập phân). ${m('I')} gấp 10 lần thì ${m('L')} tăng ${f(12)} dB.</div>
<div style="margin-top:.6mm">Trong một chu kì sóng đi được một ${f(18)}, nên ${nw(`${v} = ${f(18)}`)}. ${tk}; ${nw(`ở 20 °C: ${v} ≈ 343 m/s`)}. ${nw(`Đổi ${fr} thì ${lam} ${f(25)}, ${v} ${f(25)}`)} (điền: đổi / giữ nguyên).</div>
<div class="hint" style="margin:.3mm 0">Đơn vị: ${dv}</div></div>
${h3(5, 'Làm nhanh', '1·5')}
${box(cau(`Máy phát ${Hz('686')}, không khí ở ${nw(m('20\\ ^\\circ\\mathrm C'))} (${ms('343')}). Bước sóng ${lam} của âm là bao nhiêu mét?`, 1))}
${foot(1)}</section>`;

const bangDc = (rows) => `<table><tr><th style="width:38mm">Dụng cụ</th><th>Để làm gì</th></tr>${rows.map((x) => `<tr><td style="height:8.5mm">${x}</td><td></td></tr>`).join('')}</table>`;
const p2 = `<section class="page">
${head('CỘT KHÍ CỘNG HƯỞNG · DỤNG CỤ · CÁCH ĐO')}
${h3(1, 'II.2 · Cột khí một đầu kín: nút và bụng ở đâu?', '2·1')}
<div class="fig-side" style="${fs(58)}"><div>
<div class="card" style="padding:1.2mm 3mm">
<div>Ống thẳng đứng, đáy có nước, loa phát âm đơn sắc ${fr} trên miệng. Âm xuống mặt nước rồi phản xạ, tạo <b>sóng dừng</b> (như bài 13). Mặt nước chặn không khí dao động: đó là ${f(14)}. Miệng ống thông ra ngoài: không khí dao động mạnh nhất, đó là ${f(14)}, nằm cao hơn miệng một đoạn ${e} (${nw(`${e} ≈ 0,6 lần bán kính ống`)}).</div>
<div style="margin-top:.8mm">${m('l')} đo từ miệng ống xuống mặt nước. Từ nút tới bụng liền kề bằng ${tall(12)}·${lam}.</div>
<div style="margin-top:.8mm;display:grid;grid-template-columns:1fr 1fr;gap:3mm;align-items:center"><div>Lần 1: ${nw(`${l1} + ${e} = ${tall(16)}`)}</div><div>Lần 2: ${nw(`${l2} + ${e} = ${tall(16)}`)}</div></div>
<div style="margin-top:.4mm">Trừ vế với vế: ${nw(`${l2} − ${l1} = ${tall(16)}`)} ⇒ ${nw(`${lam} = ${f(24)}`)} (${e} mất đi).</div></div>
</div>${H.ong()}</div>
${h3(2, 'II.3 · Dụng cụ và cách đo', '2·2')}
<div class="fig-side" style="${fs(40)}"><div>
${bangDc(['Máy phát tần số + loa', `Ống trong suốt, ⌀ 16 mm, dài 670 mm`, 'Bình nước nối ống bằng ống mềm', 'Thước gắn bên ống', 'Nhiệt kế phòng'])}
<div class="hint" style="margin:.5mm 0">Ống ⌀ 16 mm: bán kính 8 mm, nên ${nw(`${e} ≈ ${f(12)} cm`)}.</div>
</div>${H.boOng()}</div>
${h3(3, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '2·3')}
${rkHai([1, 2, 3, 4], [5, 6, 7, 8])}
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('CÁC BƯỚC ĐO · AN TOÀN · BA CÁI BẪY')}
${h3(1, 'II.4 · Các bước đo', '3·1')}
<div class="card" style="padding:1.2mm 3mm">
<div class="trap"><b>1.</b><span>Lắp bộ ống; ghi nhiệt độ phòng ${m('t')} = ${f(12)} °C. Máy phát ${nw(`${fr} = ${f(12)} Hz`)} (gợi ý 500), âm vừa đủ nghe.</span></div>
<div class="trap"><b>2.</b><span>Đưa mực nước sát miệng ống; ${f(25)} (hạ / nâng) bình thật chậm đến chỗ nghe <b>to nhất lần đầu</b>; đọc ${l1} ngay tại mặt nước, mắt ngang mặt nước (tr. ${4 + OFF}).</span></div>
<div class="trap"><b>3.</b><span>Hạ tiếp tới lần to nhất thứ hai, đọc ${l2}.</span></div>
<div class="trap"><b>4.</b><span>Đưa nước về sát miệng ống, làm đủ ${f(12)} lần; ghi bảng (tr. ${4 + OFF}).</span></div>
<div class="trap"><b>5.</b><span>Tính ${lam}, ${v}, sai số, viết kết quả (tr. ${5 + OFF}).</span></div>
<div style="margin-top:.6mm"><b>Lưu ý:</b> thổi/gõ vào ống không phải cách làm cột khí rung; chỉ dùng máy phát và loa. Phòng yên lặng khi nghe.</div></div>
${h3(2, `III · Bẫy 1: “lần to đầu tiên là ${m('\\lambda/4')} nên ${m('\\lambda=4l_1')}”`, '3·2')}
<div class="card" style="padding:1.2mm 3mm">
<div>${Hz('400')}: ${nw(m('l_1=20{,}9\\ \\mathrm{cm}'))}, ${nw(m('l_2=63{,}8\\ \\mathrm{cm}'))}. An: ${nw(`${v} = 4${l1}${fr} = ${f(14)}`)} m/s. Bình: ${nw(`${v} = 2(${l2} − ${l1})${fr} = ${f(14)}`)} m/s. Giá trị tham khảo ${ms('343')}: bạn ${f(25)} đúng, vì ${l1} nhỏ hơn ${nw(`${lam}/4`)} đúng đoạn ${f(12)}.</div></div>
${h3(3, 'III · Bẫy 2: “hai lần to liên tiếp cách nhau một bước sóng”', '3·3')}
<div class="card" style="padding:1.2mm 3mm">
<div>${Hz('1000')}: các vị trí nghe to liên tiếp ở 8,1 · 25,2 · 42,4 · 59,5 cm. Hai vị trí kề nhau cách ${f(12)} cm, bằng ${tall(12)}·${lam}. Vậy ${nw(`${lam} = ${f(14)} cm`)}, ${nw(`${v} = ${f(14)} m/s`)}.</div></div>
${h3(4, 'III · Bẫy 3: “âm cao thì truyền nhanh hơn”', '3·4')}
<div class="card" style="padding:1.2mm 3mm">
<table style="text-align:center"><tr><th style="width:36mm"></th><th>${fr} = 500 Hz</th><th>${fr} = 800 Hz</th></tr>
<tr><td style="height:8mm">${lam} (cm)</td><td></td><td></td></tr>
<tr><td style="height:8mm">${v} (m/s)</td><td></td><td></td></tr></table>
<div class="hint" style="margin:.5mm 0">Cùng ống, cùng phòng ${nw(m('20\\ ^\\circ\\mathrm C'))}. Nguồn quyết định ${f(25)}, môi trường quyết định ${f(25)}.</div></div>
${K.btvn().replace('<i>1</i>', '<i>5</i>')}
${foot(3)}</section>`;

const nguyenNhan = ['Phòng ồn, gió, người nói', 'Máy phát trôi tần số, pít-tông hở khe', 'Hạ nước quá nhanh, bỏ qua chỗ to nhất', 'Đọc thước lệch mắt; đọc mép bình thay vì mặt nước', 'Phòng nóng hơn 20 °C mà vẫn so với 343 m/s'];
const bangSo = `<table class="tbl-ct" style="text-align:center"><tr><th style="width:12mm">Lần</th><th>${l1} (cm)</th><th>${l2} (cm)</th><th>${m('l_2-l_1')} (cm)</th></tr>
${[1, 2, 3, 4, 5].map((i) => `<tr><td style="height:9mm"><b>${i}</b></td><td></td><td></td><td></td></tr>`).join('')}
<tr><td style="height:9mm"><b>TB</b></td><td></td><td></td><td></td></tr></table>`;
const p4 = `<section class="page">
${head('BẢNG SỐ LIỆU · SAI SỐ ĐẾN TỪ ĐÂU')}
${h3(1, 'II.5 · Số liệu nhóm em', '4·1')}
<div class="fig-side" style="${fs(46)}"><div>${bangSo}
<div class="hint" style="margin:.8mm 0">Máy phát ${nw(`${fr} = …… ± 1 Hz`)}; thước chia tới 1 mm. ${nw(`${m('t')} = …… °C`)}.</div></div>${H.docThuoc()}</div>
<div class="card soft" style="padding:1.2mm 3mm"><div><b>Quan sát:</b> trong ống có ${f(12)} chỗ nghe to nhất; ${m('l_2-l_1')} qua các lần đo ${ck}gần như không đổi ${ck}đổi nhiều.</div></div>
${h3(2, 'Sai số đến từ đâu, khắc phục thế nào?', '4·2')}
<table><tr><th>Nguyên nhân</th><th style="width:70mm">Khắc phục</th></tr>${nguyenNhan.map((x) => `<tr><td style="height:8mm;font-size:var(--fs-sm)">${x}</td><td></td></tr>`).join('')}</table>
${h3(3, 'Làm nhanh: sai số ngẫu nhiên của một cột', '4·3')}
<div class="card" style="padding:1.2mm 3mm">
<div>Năm lần đo ${l1}: 16,8 · 16,7 · 16,8 · 16,6 · 16,7 (cm). Trung bình ${nw(`${m('\\bar l_1')} = ${f(12)} cm`)}; độ lệch từng lần: ${f(60)}; ${nw(`${m('\\overline{\\Delta l_1}')} = ${f(12)} cm`)} (trung bình các độ lệch, lấy giá trị dương).</div>
<div class="hint" style="margin:.5mm 0">Tính tới 2 chữ số sau dấu phẩy. Sai số của ${m('l')} còn cộng sai số dụng cụ ${m('\\Delta l_{dc}')} (đề cho).</div></div>
${h3(4, 'Làm nhanh: phòng nóng hơn thì sao?', '4·4')}
${box(cau(`Cùng ống, ${Hz('500')}, nhưng phòng ${nw(m('30\\ ^\\circ\\mathrm C'))}. ${tk} ⇒ ${v} = ${f(12)} m/s. Hiệu ${m('l_2-l_1')} dự kiến bao nhiêu cm (so với phòng 20 °C: ${cm('34{,}3')})?`, 1))}
${foot(4)}</section>`;

const p5 = `<section class="page">
${head(`TÍNH ${m('\\lambda')}, ${m('v')} · SAI SỐ · BÁO CÁO`)}
${h3(1, 'II.6 · Từ bảng số liệu ra kết quả', '5·1')}
<div class="fig-side" style="${fs(46)}"><div class="card" style="padding:1.2mm 3mm">
<div>${nw(`${m('\\bar\\lambda=2(\\bar l_2-\\bar l_1)=')} ${f(20)} cm`)} &nbsp;= ${f(14)} m</div>
<div style="margin-top:.6mm">${nw(`${m('\\bar v=\\bar\\lambda f=')} ${f(20)} m/s`)}</div>
<div style="margin-top:.6mm">Tổng hoặc hiệu: <b>cộng sai số tuyệt đối</b>. ${nw(`${m('\\Delta\\lambda=2(\\Delta l_1+\\Delta l_2)=')} ${f(16)} cm`)}</div>
<div style="margin-top:.6mm">Tích hoặc thương: <b>cộng sai số tỉ đối</b>. ${nw(`${m('\\dfrac{\\Delta v}{\\bar v}=\\dfrac{\\Delta\\lambda}{\\bar\\lambda}+\\dfrac{\\Delta f}{f}=')} ${f(16)} %`)}</div>
<div style="margin-top:.6mm">${nw(`${m('\\Delta v=')} ${f(14)} m/s`)} &nbsp; · &nbsp; ${nw(`${v} = (${f(14)} ± ${f(12)}) m/s`)}</div></div>${H.khoangDo()}</div>
<table class="tbl-ct" style="text-align:center;margin-top:1mm"><tr><th style="width:12mm">Lần</th><th>${m('l_2-l_1')} (cm)</th><th>${lam} (cm)</th><th>${v} (m/s)</th></tr>
${[1, 2, 3, 4, 5].map((i) => `<tr><td style="height:9mm"><b>${i}</b></td><td></td><td></td><td></td></tr>`).join('')}</table>
${h3(2, 'So với giá trị tham khảo', '5·2')}
<div class="card" style="padding:1.2mm 3mm">
<div>Nhiệt độ phòng ${nw(`${m('t')} = ${f(12)} °C`)}; ${nw(`${m('v_{tk}=331+0{,}6t=')} ${f(14)} m/s`)}. Khoảng đo từ ${f(12)} đến ${f(12)} m/s. ${m('v_{tk}')} nằm ${ck}trong ${ck}ngoài khoảng này ⇒ phép đo ${ck}phù hợp ${ck}chưa phù hợp.</div></div>
${h3(3, 'Câu hỏi báo cáo', '5·3')}
${box(`<div style="padding-top:.6mm"><b>1.</b> Vì sao đo ${l1} và ${l2} rồi lấy hiệu, không đo ${l1} rồi nhân 4?</div>${lines(2)}
<div style="padding-top:.6mm"><b>2.</b> Nguồn sai số lớn nhất của nhóm em là gì, cách giảm?</div>${lines(2)}
<div style="padding-top:.6mm"><b>3.</b> Ống cao ${nw('67 cm')}, đổi máy phát từ ${Hz('500')} xuống ${Hz('200')} thì nhóm gặp khó gì?</div>${lines(2)}`)}
${foot(5)}</section>`;

const tbDe = (ls1, ls2) => `<table style="text-align:center;margin:.6mm 0"><tr><th style="width:21mm;text-align:left">Lần</th>${ls1.map((_, i) => `<th>${i + 1}</th>`).join('')}</tr>`
  + `<tr><td style="text-align:left">${l1} (cm)</td>${ls1.map((x) => `<td>${x}</td>`).join('')}</tr><tr><td style="text-align:left">${l2} (cm)</td>${ls2.map((x) => `<td>${x}</td>`).join('')}</tr></table>`;
const dang = [
  { t: 'Dạng 1 · Dễ · Mức cường độ âm: từ cường độ ra dB và từ dB ra cường độ',
    de: `Loa phát âm ${Hz('800')}; máy đo ghi ${nw(m('I=4{,}0\\cdot10^{-7}\\ \\mathrm{W/m^2}'))}. Lấy ${nw(m('I_0=10^{-12}\\ \\mathrm{W/m^2}'))}.<br><b>a)</b> mức cường độ âm ${m('L')}<br><b>b)</b> ${m('I')} tăng 100 lần: ${m('L')} lúc này<br><b>c)</b> bàn khác máy đo ${nw(m('L=85\\ \\mathrm{dB}'))}: cường độ âm ${m('I')}`,
    nd: `${nw(`${m('L=10\\lg')} ${f(20)}`)}; ${m('I')} gấp 100 lần thì ${m('L')} tăng ${f(12)} dB; ${nw(`${m('I=I_0\\cdot10^{L/10}')}`)}`, a: ['a', 'b', 'c'], gi: 3 },
  { t: 'Dạng 2 · Trung bình · Ống một đầu kín: dự đoán các vị trí cộng hưởng',
    de: `Ống thẳng đứng dài ${cm('67')}, loa ở miệng ống phát ${Hz('600')}; phòng ${nw(m('15\\ ^\\circ\\mathrm C'))}; ${nw(m('e=0{,}5\\ \\mathrm{cm}'))}. Mặt nước hạ dần từ miệng ống xuống.<br><b>a)</b> ${v} và ${lam}<br><b>b)</b> ${l1} và ${l2} của hai lần to nhất đầu<br><b>c)</b> có nghe được lần to nhất thứ ba không (so với chiều dài ống)`,
    nd: `${nw(`${v} = 331 + 0,6${m('t')}`)}; ${nw(`${l1} + ${e} = ${f(12)}`)}; lần ba ${nw(`${m('l_3+e=')} ${f(14)}`)} so với 67 cm`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], cot: 3, gi: 4, fig: H.ong() },
  { t: `Dạng 3 · Trung bình · Từ hai lần cộng hưởng tính ${m('\\lambda')}, ${m('v')}, ${m('e')}`,
    de: `Âm thoa ${Hz('640')} (coi chính xác), phòng ${nw(m('28\\ ^\\circ\\mathrm C'))}. Nghe to nhất lần một khi ${nw(m('l_1=13{,}0\\ \\mathrm{cm}'))}, lần hai khi ${nw(m('l_2=39{,}9\\ \\mathrm{cm}'))}.<br><b>a)</b> ${lam} và ${v} nhóm đo được<br><b>b)</b> đoạn ${e}<br><b>c)</b> ${v} theo nhiệt độ phòng; kết quả đo lệch bao nhiêu phần trăm so với giá trị đó`,
    nd: `${nw(`${lam} = 2(${l2} − ${l1})`)}; ${nw(`${e} = ${lam}/4 − ${l1}`)}; lệch ${nw(`= |${v} − ${m('v_{tk}')}| / ${m('v_{tk}')}`)}`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'], cot: 3, gi: 3 },
  { t: 'Dạng 4 · Khó · Xử lí bảng số liệu: sai số và so với giá trị tham khảo',
    de: `Ống dài ${cm('70')}, phòng ${nw(m('30\\ ^\\circ\\mathrm C'))}, máy phát ${nw(m('f=400\\pm1\\ \\mathrm{Hz}'))}. Sai số dụng cụ ${nw(m('\\Delta l_{dc}=0{,}1\\ \\mathrm{cm}'))}; sai số của mỗi ${m('\\bar l')} = độ lệch trung bình + ${m('\\Delta l_{dc}')}.${tbDe(['21,5', '21,7', '21,6', '21,8', '21,4'], ['65,2', '65,1', '65,3', '65,2', '65,2'])}<b>a)</b> ${m('\\bar\\lambda')} và ${m('\\bar v')}<br><b>b)</b> ${m('\\Delta\\lambda')}, ${m('\\Delta v')}; viết ${m('v=\\bar v\\pm\\Delta v')}<br><b>c)</b> so với giá trị tham khảo theo nhiệt độ phòng: có phù hợp không`,
    nd: `${nw(`${m('\\bar l_1')}, ${m('\\bar l_2')}`)} rồi ${nw(`${m('\\bar\\lambda=2(\\bar l_2-\\bar l_1)')}`)}; ${nw(`${m('\\Delta\\lambda')} = 2(${f(12)} + ${f(12)})`)}; ${nw(`${m('\\dfrac{\\Delta v}{\\bar v}=\\dfrac{\\Delta\\lambda}{\\bar\\lambda}+\\dfrac{\\Delta f}{f}')}`)}`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], cot: 3, gi: 6 },
];

const oY = (s, o, w = {}) => s.split('<br>').map((p) => {
  const y = p.match(/^<b>([a-d])\)<\/b>/);
  if (!y) return `<div>${p}</div>`;
  const ls = o.filter((l) => l[0] === y[1]);
  return `<div class="yo"><span>${p}</span><span class="oo">${ls.map((l) => `<span class="nw"><b>${l})</b>${f(typeof w === 'object' ? (w[l] ?? 25) : w)}</span>`).join('')}</span></div>`;
}).join('');
const ttDe = (b) => oY(b.de, b.o, b.ow);
const vaoVo = (ds) => ds.map((b) => (b.o ? { t: b.t, de: ttDe(b), k: 0 } : b));
const nhap = (n) => ({ t: '<span class="nhap-t">Nháp / chỗ em còn vướng</span>', de: lines(n), k: 0 });
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–3', 'DẠNG 3 · DẠNG 4'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Máy đo ghi ${nw(m('I=2{,}5\\cdot10^{-6}\\ \\mathrm{W/m^2}'))} (${nw(m('I_0=10^{-12}\\ \\mathrm{W/m^2}'))}).<br><b>a)</b> mức cường độ âm ${m('L')}<br><b>b)</b> ${m('I')} tăng 100 lần: ${m('L')} lúc này<br><b>c)</b> bàn khác ${nw(m('L=72\\ \\mathrm{dB}'))}: cường độ âm ${m('I')}`, o: ['a', 'b', 'c'], ow: { c: 30 } },
    { t: 'Dạng 1 · Bài 2', de: `Một âm có ${nw(m('I=3{,}2\\cdot10^{-5}\\ \\mathrm{W/m^2}'))}.<br><b>a)</b> mức cường độ âm ${m('L')}<br><b>b)</b> ${m('I')} giảm còn 1/10: ${m('L')} lúc này<br><b>c)</b> ${nw(m('L=90\\ \\mathrm{dB}'))}: cường độ âm ${m('I')}`, o: ['a', 'b', 'c'], ow: { c: 30 } },
    { t: 'Dạng 2 · Bài 1', de: `Ống dài ${cm('67')}, loa ${Hz('500')}, phòng ${nw(m('25\\ ^\\circ\\mathrm C'))}, ${nw(m('e=0{,}5\\ \\mathrm{cm}'))}.<br><b>a)</b> ${v} và ${lam}<br><b>b)</b> ${l1} và ${l2} của hai lần to nhất đầu<br><b>c)</b> lần to thứ ba có nghe được trong ống không`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], ow: { 'a<sub>1</sub>': 18, 'a<sub>2</sub>': 18, 'b<sub>1</sub>': 18, 'b<sub>2</sub>': 18, c: 20 } },
    { t: 'Dạng 2 · Bài 2', de: `Ống dài ${cm('50')}, loa ${Hz('800')}, phòng ${nw(m('20\\ ^\\circ\\mathrm C'))}, ${nw(m('e=0{,}4\\ \\mathrm{cm}'))}.<br><b>a)</b> ${v} và ${lam}<br><b>b)</b> ${l1} và ${l2}<br><b>c)</b> lần to thứ ba có nghe được trong ống không`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], ow: { 'a<sub>1</sub>': 18, 'a<sub>2</sub>': 18, 'b<sub>1</sub>': 18, 'b<sub>2</sub>': 18, c: 20 } },
    { t: 'Dạng 3 · Bài 1', de: `Âm thoa ${Hz('512')} (chính xác), phòng ${nw(m('20\\ ^\\circ\\mathrm C'))}: ${nw(m('l_1=16{,}6\\ \\mathrm{cm}'))}, ${nw(m('l_2=49{,}9\\ \\mathrm{cm}'))}.<br><b>a)</b> ${lam} và ${v} đo được<br><b>b)</b> đoạn ${e}<br><b>c)</b> ${v} theo nhiệt độ phòng; độ lệch phần trăm của kết quả đo`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'], ow: { 'a<sub>1</sub>': 18, 'a<sub>2</sub>': 18, b: 18, 'c<sub>1</sub>': 18, 'c<sub>2</sub>': 18 } },
    nhap(6),
  ], [
    { t: 'Dạng 3 · Bài 2', de: `Máy phát ${Hz('1000')} (chính xác), phòng ${nw(m('25\\ ^\\circ\\mathrm C'))}: ${nw(m('l_1=8{,}3\\ \\mathrm{cm}'))}, ${nw(m('l_2=25{,}2\\ \\mathrm{cm}'))}.<br><b>a)</b> ${lam} và ${v} đo được<br><b>b)</b> đoạn ${e}<br><b>c)</b> ${v} theo nhiệt độ phòng; độ lệch phần trăm của kết quả đo`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'], ow: { 'a<sub>1</sub>': 18, 'a<sub>2</sub>': 18, b: 18, 'c<sub>1</sub>': 18, 'c<sub>2</sub>': 18 } },
    { t: 'Dạng 4 · Bài 1', de: `Phòng ${nw(m('20\\ ^\\circ\\mathrm C'))}, ${nw(m('f=500\\pm1\\ \\mathrm{Hz}'))}, ${nw(m('\\Delta l_{dc}=0{,}1\\ \\mathrm{cm}'))} (sai số của ${m('\\bar l')} = độ lệch trung bình + ${m('\\Delta l_{dc}')}):${tbDe(['16,7', '16,9', '16,8', '16,6', '16,7'], ['50,8', '51,0', '50,9', '50,7', '51,0'])}<b>a)</b> ${m('\\bar\\lambda')} và ${m('\\bar v')}<br><b>b)</b> ${m('\\Delta\\lambda')}, ${m('\\Delta v')}; ghi ${m('v=\\bar v\\pm\\Delta v')}<br><b>c)</b> so với giá trị tham khảo: phù hợp không`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], ow: { 'a<sub>1</sub>': 18, 'a<sub>2</sub>': 18, 'b<sub>1</sub>': 18, 'b<sub>2</sub>': 30, c: 34 } },
    { t: 'Dạng 4 · Bài 2', de: `Phòng ${nw(m('25\\ ^\\circ\\mathrm C'))}, ${nw(m('f=1000\\pm1\\ \\mathrm{Hz}'))}, cùng cách tính sai số:${tbDe(['8,2', '8,4', '8,3', '8,1', '8,5'], ['25,6', '25,5', '25,7', '25,5', '25,7'])}<b>a)</b> ${m('\\bar\\lambda')} và ${m('\\bar v')}<br><b>b)</b> ${m('\\Delta\\lambda')}, ${m('\\Delta v')}; ghi ${m('v=\\bar v\\pm\\Delta v')}<br><b>c)</b> so với giá trị tham khảo: phù hợp không`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], ow: { 'a<sub>1</sub>': 18, 'a<sub>2</sub>': 18, 'b<sub>1</sub>': 18, 'b<sub>2</sub>': 30, c: 34 } },
    nhap(7),
  ]],
  dap: [
    `D1·1: a) 64,0 dB · b) 84,0 dB · c) 1,58·10<sup>−5</sup> W/m² &nbsp;|&nbsp; D1·2: a) 75,1 dB · b) 65,1 dB · c) 1,0·10<sup>−3</sup> W/m² &nbsp;|&nbsp; D2·1: a<sub>1</sub>) 346 m/s · a<sub>2</sub>) 69,2 cm · b<sub>1</sub>) 16,8 cm · b<sub>2</sub>) 51,4 cm · c) không (l<sub>3</sub> ≈ 86,0 cm &gt; 67 cm) &nbsp;|&nbsp; D2·2: a<sub>1</sub>) 343 m/s · a<sub>2</sub>) 42,9 cm · b<sub>1</sub>) 10,3 cm · b<sub>2</sub>) 31,8 cm · c) không (l<sub>3</sub> ≈ 53,2 cm &gt; 50 cm) &nbsp;|&nbsp; D3·1: a<sub>1</sub>) 66,6 cm · a<sub>2</sub>) 341,0 m/s · b) 0,05 cm · c<sub>1</sub>) 343 m/s · c<sub>2</sub>) 0,6 %`,
    `D3·2: a<sub>1</sub>) 33,8 cm · a<sub>2</sub>) 338,0 m/s · b) 0,15 cm · c<sub>1</sub>) 346 m/s · c<sub>2</sub>) 2,3 % &nbsp;|&nbsp; D4·1: a<sub>1</sub>) 68,28 cm · a<sub>2</sub>) 341,4 m/s · b<sub>1</sub>) 0,78 cm · b<sub>2</sub>) v = 341,4 ± 4,6 m/s · c) 343 nằm trong [336,8; 346,0], phù hợp &nbsp;|&nbsp; D4·2: a<sub>1</sub>) 34,6 cm · a<sub>2</sub>) 346,0 m/s · b<sub>1</sub>) 0,80 cm · b<sub>2</sub>) v = 346,0 ± 8,3 m/s · c) 346 nằm trong khoảng, phù hợp`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [2, 2], kq: [[1, 2], [3, 4]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'nhắc lại 1·4 · cột khí 2·1 · dụng cụ 2·2 · các bước 3·1 · bẫy 3·2–3·4 · số liệu 4·1 · sai số 4·2 · tính v 5·1 · dạng 1–2 → 6·1 · dạng 3–4 → 7·1',
  out: process.argv[2],
});
