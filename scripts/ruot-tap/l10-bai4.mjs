// Ruột tập VL10 – Bài 4 · Độ dịch chuyển và quãng đường đi được (lesson id 49). Quyển Chương 2 lớp 10: bài 4 = tr. 1–12.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự (giải vào vở) · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l10-bai4.mjs (toàn bộ SVG tự vẽ). Nội dung theo bài web (book/cache/49.json, tải từ DB 13/11/2026):
// mục tiêu, dự đoán sân băng, II.1–II.5, ví dụ xe tới–lùi, thí nghiệm ray uốn, ba bẫy, Trả bài 6 câu, bài toán mẫu đạp xe,
// thử thách phân tầng, 5 dạng bài tập mẫu. Đáp số Bài tương tự (tuongTu.dap) tính bằng Python 13/11/2026.
// Chạy: node scripts/ruot-tap/l10-bai4.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl10-bai4.pdf
//       node scripts/ruot-tap/l10-bai4.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l10-bai4/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL10b4 as H } from './hinh-l10-bai4.mjs';

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
  const out = resolve(HERE, 'out/hinh-l10-bai4'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 4, lid: 49, ten: 'ĐỘ DỊCH CHUYỂN VÀ QUÃNG ĐƯỜNG ĐI ĐƯỢC', lop: 10, baiDau: 4, sub: 'Vật lí 10 · Chương 2: Động học' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const vd = m('\\vec d'), vtb = m('v_{\\mathrm{tb}}');
const so = (s) => nw(m(s)); // số + đơn vị không gãy dòng

// Bài tương tự xếp 2 cột như bài 23 (khung xếp .tt dọc); ô đáp số đặt cuối đúng dòng của ý.
const ttHaiCot = '<style>.bt>.gi{display:grid;grid-template-columns:1fr 1fr;column-gap:4mm}.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm}.yo .oo{flex:none;display:flex;gap:3mm}.yo{line-height:1.35}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';

const p1 = `${ttHaiCot}<section class="page">
${head('BÀI 4 · ĐỘ DỊCH CHUYỂN VÀ QUÃNG ĐƯỜNG ĐI ĐƯỢC', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Nêu được <b>chất điểm</b>, <b>quỹ đạo</b>, <b>hệ quy chiếu</b>; xác định vị trí bằng <b>toạ độ</b>`)}
${dong(`${ck}Định nghĩa <b>độ dịch chuyển</b> ${vd} và tính nó trên một đường thẳng`)}
${dong(`${ck}So sánh <b>quãng đường đi được</b> với độ dịch chuyển; tính <b>tốc độ trung bình</b>`)}
${dong(`${ck}Tìm độ dịch chuyển khi vật đi theo <b>hai hướng vuông góc</b>`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Em trượt đúng một vòng sát rào rồi dừng ở cửa vào sân. Đồng hồ thể thao báo “đã đi ${so('60\\ \\mathrm m')}”. Bạn đứng ở cửa nói: “Cậu có dịch chuyển tí nào đâu!” Ai đúng?</p>
<div class="fig-side" style="${fs(48)}"><div>
${opt('A', `Chỉ đồng hồ đúng: đi ${so('60\\ \\mathrm m')} tức là dịch chuyển ${so('60\\ \\mathrm m')}`)}
${opt('B', 'Cả hai đúng: đồng hồ đo độ dài đường đi, bạn nói về sự thay đổi vị trí')}
${opt('C', 'Chỉ bạn đúng: em về chỗ cũ nên đồng hồ đo sai')}
${opt('D', `Cả hai sai: dịch chuyển phải là nửa vòng, ${so('30\\ \\mathrm m')}`)}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 2)}</div>
${H.sanBang()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f(12)} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(2)}</div>
${h3(4, 'II.1 · Chuyển động, chất điểm, quỹ đạo', '1·4')}
<div class="card" style="padding:1.2mm 3mm">
<div><b>Chuyển động cơ:</b> vị trí của vật ${f(25)} so với vật khác theo ${f(25)}.</div>
<div><b>Tính tương đối:</b> ngồi trên xe buýt, em đứng yên so với ${f(25)} nhưng chuyển động so với ${f(25)}.</div>
<div><b>Chất điểm:</b> vật có kích thước rất ${f(25)} so với ${f(25)}; khối lượng ${f(25)} khối lượng của vật.</div>
<div><b>Quỹ đạo:</b> ${f(25)} mà chất điểm vạch ra khi chuyển động.</div>
<div style="margin-top:.6mm">Xe khách dài khoảng ${so('10\\ \\mathrm m')} chạy Hà Nội – Huế (khoảng ${so('650\\ \\mathrm{km}')}): ${ck}là &nbsp;${ck}không là chất điểm.</div>
<div>Cũng xe đó lùi vào chỗ đỗ hẹp: ${ck}là &nbsp;${ck}không là chất điểm.</div></div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('HỆ QUY CHIẾU · ĐỘ DỊCH CHUYỂN · QUÃNG ĐƯỜNG')}
${h3(1, 'II.2 · Hệ quy chiếu: Mốc – Trục – Giờ', '2·1')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div>Hệ quy chiếu = ${f(25)} gắn với vật mốc + ${f(25)} và đồng hồ.</div>
<div>Toạ độ ${m('x=\\overline{OM}')}: M ở phía dương của O thì ${nw(`${m('x=')} ${f(12)}`)}; ở phía âm thì ${nw(`${m('x=')} ${f(12)}`)}.</div>
<div>Trong hình: ${nw(`${m('x_M=')} ${f(12)}&nbsp;m`)} ; ${nw(`${m('x_N=')} ${f(12)}&nbsp;m`)}</div>
<div>“Lúc 7 giờ” là ${f(25)}; “từ 7 giờ đến 7 giờ 45 phút” là ${f(25)}, ${nw(`${m('\\Delta t=')} ${f(12)}&nbsp;phút`)}.</div>
<div>Đổi gốc thời gian: ${f(25)} đổi, ${f(25)} giữ nguyên.</div></div>
${H.trucToaDo()}</div>
${h3(2, 'II.3 · Độ dịch chuyển', '2·2')}
<div class="card fig-side" style="${fs(50)};padding:1.2mm 3mm"><div>
<div>Độ dịch chuyển ${vd} là đại lượng ${f(25)}, cho biết ${f(25)} và ${f(25)} của sự thay đổi vị trí.</div>
<div>Vẽ: mũi tên nối ${f(25)} tới ${f(25)}.</div>
<div style="margin:.6mm 0">Trên trục ${m('Ox')}: ${nw(`${m('d=\\Delta x=')} ${f(25)}`)}; dấu của ${m('d')} cho biết ${f(25)}.</div>
<div><b>Ví dụ (hình bên):</b> xe đi từ ${so('20\\ \\mathrm{cm}')} tới ${so('80\\ \\mathrm{cm}')} rồi lùi về ${so('50\\ \\mathrm{cm}')}.</div>
<div>Đoạn đã chạy ${nw(`${f(12)}&nbsp;cm`)}; ${nw(`${m('d=')} ${f(12)}&nbsp;cm`)}. Nếu lùi về ${so('10\\ \\mathrm{cm}')}: ${nw(`${m('d=')} ${f(12)}&nbsp;cm`)}.</div></div>
${H.xeToiLui()}</div>
${h3(3, 'II.4 · Quãng đường đi được', '2·3')}
<div class="card" style="padding:1.2mm 3mm">
<div>Quãng đường ${m('s')}: ${f(25)} vật đi được trong suốt quá trình; đại lượng ${f(25)}, không ${f(25)}.</div>
<div>Thẳng, không đổi chiều: ${nw(`${m('|d|')} ${f(12)} ${m('s')}`)} · Đổi chiều hoặc đi đường cong: ${nw(`${m('|d|')} ${f(12)} ${m('s')}`)} · Quay về chỗ cũ: ${nw(`${m('d=')} ${f(12)}`)}</div></div>
${h3(4, 'Làm nhanh', '2·4')}
${box(`<div style="padding-top:1mm;line-height:1.35"><b>Câu 1.</b> Cùng trục như hình II.3: xe đi từ ${so('70\\ \\mathrm{cm}')} tới ${so('90\\ \\mathrm{cm}')} rồi lùi về ${so('40\\ \\mathrm{cm}')}.</div>
${wl(`Độ dịch chuyển ${m('d=')}`, 1)}${wl(`Quãng đường ${m('s=')}`, 1)}${wl(`Vì sao ${m('|d|\\lt s')}?`, 1)}`)}
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('THÍ NGHIỆM RAY UỐN · TỐC ĐỘ TRUNG BÌNH · BẪY · TỰ KIỂM TRA')}
${h3(1, 'Thí nghiệm: xe đồ chơi trên ray uốn', '3·1')}
<div class="fig-side" style="${fs(52)}"><div>
<table class="tbl-ct"><tr><th>Hình ray</th><th>${m('s')} đo (cm)</th><th>${m('d')} đo (cm)</th></tr>
<tr><td>thẳng ${so('30\\ \\mathrm{cm}')}</td><td>30,2</td><td>30,0</td></tr>
<tr><td>nửa vòng, ${so('r=10\\ \\mathrm{cm}')}</td><td>31,9</td><td>20,1</td></tr>
<tr><td>chữ L ${nw('30 cm + 40 cm')}</td><td>70,6</td><td>49,9</td></tr>
<tr><td>trọn vòng, ${so('r=10\\ \\mathrm{cm}')}</td><td>63,5</td><td>0,0</td></tr></table>
<div class="hint" style="margin-top:.4mm">Đo ${m('s')} bằng sợi chỉ đặt dọc ray, đo ${m('d')} bằng thước nối thẳng hai dấu (số liệu minh hoạ).</div>
</div>
${H.rayUon()}</div>
<div class="card" style="margin-top:.6mm;padding:1mm 3mm">
<div>Tính theo hình: nửa vòng ${nw(`${m('s=\\pi r\\approx')} ${f(12)}&nbsp;cm`)}, ${nw(`${m('d=')} ${f(12)}&nbsp;cm`)}; chữ L ${nw(`${m('d=')} ${f(12)}&nbsp;cm`)}; trọn vòng ${nw(`${m('s=2\\pi r\\approx')} ${f(12)}&nbsp;cm`)}.</div>
<div><b>Rút ra:</b> chỉ ray ${f(25)} cho ${m('d\\approx s')}; vòng kín cho ${nw(`${m('d=')} ${f(12)}`)}. Vì sao cột ${m('s')} lệch nhiều hơn cột ${m('d')}?</div>${lines(1)}</div>
${h3(2, 'II.5 · Tốc độ trung bình', '3·2')}
<div class="card" style="padding:1.2mm 3mm">
<div>${nw(`${vtb}${m('=')}`)} <span class="fill" style="min-width:16mm;height:9mm"></span> &nbsp;(${m('s')}: ${f(25)}, ${m('t')}: thời gian đi hết quãng đường đó)</div>
<div>Đơn vị ${m('\\mathrm{m/s}')} hoặc ${m('\\mathrm{km/h}')}: ${nw(`${m('1\\ \\mathrm{m/s}=')} ${f(12)}&nbsp;km/h`)}, vì ${nw(`${m('1\\ \\mathrm h=')} ${f(12)}&nbsp;s`)}. Cho biết nhanh hay chậm, ${ck}có &nbsp;${ck}không cho biết hướng.</div>
<div><b>Sân băng:</b> một vòng ${so('60\\ \\mathrm m')} hết ${so('20\\ \\mathrm s')}: ${nw(`${m('d=')} ${f(12)}`)}; ${nw(`${vtb}${m('=')} ${f(12)}&nbsp;m/s`)} ${nw(`${m('=')} ${f(12)}&nbsp;km/h`)}.</div></div>
${h3(3, 'III · Ba cái bẫy hay sập', '3·3')}
<div class="card fig-side" style="${fs(40)};padding:1mm 3mm"><div>
<div class="trap">${ck}<span><b>“Đi bao nhiêu thì dịch chuyển bấy nhiêu.”</b> Chỉ đúng khi chuyển động ${f(25)}, không ${f(25)}.</span></div>
<div class="trap">${ck}<span><b>“Dấu âm là sai, gạch bỏ.”</b> ${m('d\\lt 0')}: vật dịch chuyển ${f(25)} chiều dương; còn ${m('s')} luôn ${f(25)}.</span></div>
<div class="trap">${ck}<span><b>“Cộng độ dịch chuyển như cộng số.”</b> Hai đoạn vuông góc: ${nw(`${m('d=')} ${f(25)}`)}; cùng phương, ngược chiều: ${nw(`${m('d=')} ${f(25)}`)}.</span></div></div>
${H.vuongGoc()}</div>
${h3(4, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '3·4')}
${rkHai([1, 2, 3], [4, 5, 6])}
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('TRẢ BÀI · BÀI TOÁN MẪU')}
${h3(1, 'IV · Trả bài 6 câu', '4·1')}
${box(`${tb('1. Chuyển động cơ là gì? Vì sao nói chuyển động có tính tương đối?')}${lines(2)}
${tb('2. Khi nào coi vật là chất điểm? Quỹ đạo là gì?')}${lines(1)}
${tb('3. Hệ quy chiếu gồm những gì?')}${lines(2)}
${tb('4. Độ dịch chuyển là gì, vẽ thế nào, tính thế nào trên một trục?')}${lines(2)}
${tb(`5. Ba điểm khác nhau giữa ${m('d')} và ${m('s')}. Khi nào độ lớn bằng nhau?`)}${lines(2)}
${tb(`6. Tính tốc độ trung bình thế nào? Đi một vòng kín thì ${m('d')} và ${vtb} ra sao?`)}${lines(1)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/6 câu · chưa thuộc: ${f(25)} ${nw(`${m("\\to")} đọc lại ô ${f(12)} Tập`)}</div>
${h3(2, 'V · Bài toán mẫu: đạp xe tới trường', '4·2')}
<div class="card soft" style="padding:1.2mm 3mm">Một bạn đạp xe từ nhà, đi thẳng ${so('1{,}2\\ \\mathrm{km}')} về phía Đông tới ngã tư, rồi rẽ trái đi thẳng ${so('0{,}5\\ \\mathrm{km}')} về phía Bắc thì tới trường. Cả quãng hết ${nw('6 phút')}. Tính quãng đường đi được, độ dịch chuyển (độ lớn và hướng) và tốc độ trung bình.</div>
<table><tr><th style="width:52mm">Câu trong đề</th><th>Dữ liệu ${m("\\to")} kiến thức</th></tr>
<tr><td>“đi thẳng 1,2 km về phía Đông”</td><td>${m('d_1=1{,}2\\ \\mathrm{km}')}, đoạn thẳng, không đổi chiều</td></tr>
<tr><td style="height:6.5mm">“rẽ trái … 0,5 km về phía Bắc”</td><td></td></tr>
<tr><td style="height:6.5mm">“từ nhà … tới trường”</td><td></td></tr>
<tr><td style="height:6.5mm">“hết 6 phút”</td><td></td></tr></table>
<div class="fig-side" style="${fs(52)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl(`Quãng đường ${m('s')}:`, 1)}${wl(`Độ lớn ${m('d')}:`, 2)}${wl(`Hướng ${m('\\alpha')} (máy tính chế độ D, SHIFT tan):`, 2)}${wl(`Tốc độ trung bình ${vtb}:`, 2)}${wl(`Kiểm tra: ${m('d')} so với ${m('s')}?`, 1)}</div>${H.dapXe()}</div>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TẬP VỀ NHÀ · THỬ THÁCH · MANG VỀ')}
${K.btvn()}
${h3(2, 'Điền bước còn thiếu: cùng hình, đổi số', '5·2')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div style="padding-top:1mm;line-height:1.4"><b>Đề:</b> ${so('0{,}8\\ \\mathrm{km}')} về Đông, ${so('0{,}6\\ \\mathrm{km}')} về Bắc, hết ${nw('6 phút')}. <b>Bước 1 (cho sẵn):</b> ${m('s=0{,}8+0{,}6=1{,}4\\ \\mathrm{km}')}</div>
${wl(`Bước 2: ${m('d=')}`, 1)}${wl(`Bước 3: ${vtb}${m('=')}`, 1)}</div>
${h3(3, 'Thử thách phân tầng', '5·3')}
<div class="fig-side" style="${fs(40)}">${box(wl(`${m('\\bigstar')} Xe đi trên trục ${m('Ox')} từ ${so('x_1=15\\ \\mathrm{km}')} đến ${so('x_2=5\\ \\mathrm{km}')}, không đổi chiều. Tìm ${m('d')} và ${m('s')}.`, 2)
 + wl(`${m('\\bigstar\\bigstar')} Chạy ${nw('1,5 vòng')} quanh sân tròn bán kính ${so('50\\ \\mathrm m')} (lấy ${so('\\pi\\approx 3{,}14')}). Tìm ${m('s')} và độ lớn ${m('d')}.`, 3)
 + wl(`${m('\\bigstar\\bigstar\\bigstar')} Có khi nào độ lớn độ dịch chuyển lớn hơn quãng đường không? Lập luận.`, 3))}${H.vongRuoi()}</div>
${h3(4, 'Câu đổi chiều (bài toán mẫu)', '5·4')}
${box(wl(`Hôm sau bạn đó đi ${so('1{,}2\\ \\mathrm{km}')} về Đông rồi quay lại ${so('0{,}5\\ \\mathrm{km}')} về Tây trên cùng đường, hết ${nw('6 phút')}. Tính độ lớn, hướng của ${m('d')} và ${vtb}. So với bài toán mẫu, ${vtb} có đổi không? Vì sao?`, 4))}
${h3(5, 'VI · Mang về: điều em dễ quên nhất', '5·5')}
${box(wl('1.', 3) + wl('2.', 3) + wl('3.', 3))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Đi rồi quay lại trên một đường thẳng: tìm d và s',
    de: `Nhà A, tiệm C, bưu điện B trên một đường thẳng như hình. Gốc ${m('O')} ở A, chiều dương A ${m("\\to")} B.<br><b>a)</b> A ${m("\\to")} B ${m("\\to")} C: độ dịch chuyển (a<sub>1</sub>), quãng đường (a<sub>2</sub>)<br><b>b)</b> đi tiếp về A, cả hành trình: độ dịch chuyển (b<sub>1</sub>), quãng đường (b<sub>2</sub>)`,
    nd: `${m('s')} cộng ${f(25)} các đoạn; ${nw(`${m('d=')} ${f(25)}`)}`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>'], gi: 4, fig: H.d1Truc('') },
  { t: 'Dạng 2 · Dễ · Dùng toạ độ có dấu: d âm nghĩa là gì',
    de: `Gốc ${m('O')} ở trạm xăng, ${m('Ox')} hướng Đông. Xe tải đi từ ${so('x_1=12\\ \\mathrm{km}')} về phía Tây tới ${so('x_2=-3\\ \\mathrm{km}')}, rồi quay đầu tới ${so('x_3=2\\ \\mathrm{km}')}.<br><b>a)</b> đoạn ${m('x_1\\to x_2')}: ${m('d')} (a<sub>1</sub>), ${m('s')} (a<sub>2</sub>) &nbsp;<b>b)</b> cả hành trình: ${m('d')} (b<sub>1</sub>), ${m('s')} (b<sub>2</sub>)<br><b>c)</b> điểm dừng ở phía nào của điểm xuất phát?`,
    nd: `dấu của ${m('d')} cho biết ${f(25)}; đổi chiều thì ${f(25)} rồi cộng ${m('s')}`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], gi: 5, fig: H.d2Truc(''), cot: 5 },
  { t: 'Dạng 3 · Trung bình · Hai đoạn vuông góc: độ lớn và hướng của d',
    de: `Đi bộ từ nhà tới trường: thẳng ${so('900\\ \\mathrm m')} về phía Đông, rồi rẽ trái thẳng ${so('1200\\ \\mathrm m')} về phía Bắc. Tìm <b>a)</b> quãng đường; <b>b)</b> độ lớn độ dịch chuyển; <b>c)</b> góc giữa độ dịch chuyển và hướng Đông.`,
    nd: `hai đoạn vuông góc: ${nw(`${m('d=')} ${f(25)}`)}; ${nw(`${m('\\tan\\alpha=')} <span class="fill" style="min-width:16mm;height:9mm"></span>`)}`, a: ['a', 'b', 'c'], gi: 3, fig: H.d3VuongGoc('') },
  { t: 'Dạng 4 · Trung bình · Tốc độ trung bình khi có đoạn nghỉ',
    de: `Một bạn đạp xe trên đường thẳng, không đổi chiều: đạp ${so('4\\ \\mathrm{km}')} từ nhà tới công viên hết ${nw('20 phút')}, nghỉ ${nw('10 phút')}, rồi đạp tiếp ${so('2\\ \\mathrm{km}')} tới sân bóng hết ${nw('20 phút')}. Biết ${so('1\\ \\mathrm{m/s}=3{,}6\\ \\mathrm{km/h}')}.<br><b>a)</b> tốc độ trung bình đoạn đầu (a<sub>1</sub>) và đoạn sau (a<sub>2</sub>), theo km/h<br><b>b)</b> tốc độ trung bình cả hành trình theo km/h (b<sub>1</sub>) và m/s (b<sub>2</sub>)<br><b>c)</b> kết quả b<sub>1</sub> có bằng trung bình cộng của a<sub>1</sub> và a<sub>2</sub> không`,
    nd: `${m('t')} của cả hành trình ${ck}có &nbsp;${ck}không tính thời gian nghỉ; ${nw(`${vtb}${m('=')} ${f(25)}`)}, không phải trung bình cộng`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], gi: 5, fig: H.d4ThoiGian(), cot: 3 },
  { t: 'Dạng 5 · Khó · Quay đầu rồi rẽ vuông góc: d, s và tốc độ trung bình',
    de: `Xe mô hình chạy trên sàn với tốc độ không đổi. Từ điểm ${m('O')}, xe đi thẳng ${so('7\\ \\mathrm m')} về phía Đông, quay đầu đi ${so('3\\ \\mathrm m')} về phía Tây trên cùng đường, rồi rẽ đi thẳng ${so('3\\ \\mathrm m')} về phía Bắc thì dừng. Cả hành trình mất ${so('26\\ \\mathrm s')}.<br><b>a)</b> quãng đường đi được<br><b>b)</b> độ lớn (b<sub>1</sub>) và hướng (b<sub>2</sub>) của độ dịch chuyển<br><b>c)</b> tốc độ trung bình`,
    nd: `gộp hai đoạn ${f(25)} trước (ngược chiều lấy ${f(25)}), rồi mới dùng Pi-ta-go; ${vtb} dùng ${f(25)}`, a: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], gi: 7, fig: H.d5QuayRe(), cot: 2 },
];

// Bài tương tự giải vào vở (thầy chốt 10/11): 1 cột; ô đáp số 25 mm (40 mm khi ý dài) đặt cuối đúng dòng của ý, nhãn khớp a) b) c)…
// Đáp số tính bằng Python 13/11/2026 (math.hypot, math.atan, đổi phút → giờ), làm tròn như đề.
const oY = (s, o, w = 25) => s.split('<br>').map((p) => {
  const y = p.match(/^<b>([a-e])\)<\/b>/);
  if (!y) return `<div>${p}</div>`;
  const ls = o.filter((l) => l[0] === y[1]);
  return `<div class="yo"><span>${p}</span><span class="oo">${ls.map((l) => `<span class="nw"><b>${l})</b>${f(w)}</span>`).join('')}</span></div>`;
}).join('');
const ttDe = (b) => b.fig ? `<div class="fig-side" style="grid-template-columns:1fr ${b.fw}mm">${`<div>${oY(b.de, b.o, b.ow)}</div>`}${b.fig}</div>` : oY(b.de, b.o, b.ow);
const vaoVo = (ds) => ds.map((b) => (b.o ? { t: b.t, de: ttDe(b), k: 0 } : b));
const nhap = (n) => ({ t: '<span class="nhap-t">Nháp / chỗ em còn vướng</span>', de: lines(n), k: 0 });
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–3', 'DẠNG 4–5'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Nhà A cách trường B ${so('1200\\ \\mathrm m')} trên một đường thẳng; hiệu sách C nằm giữa, cách A ${so('500\\ \\mathrm m')}. Gốc ${m('O')} ở A, chiều dương A ${m("\\to")} B. Đi A ${m("\\to")} B rồi quay về C.<br><b>a)</b> tới C: ${m('d')} (a<sub>1</sub>), ${m('s')} (a<sub>2</sub>)<br><b>b)</b> đi tiếp về A, cả hành trình: ${m('d')} (b<sub>1</sub>), ${m('s')} (b<sub>2</sub>)`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>'] },
    { t: 'Dạng 1 · Bài 2', de: `Thang máy: gốc ${m('O')} ở sàn tầng 1, chiều dương hướng lên, mỗi tầng cao ${so('3{,}0\\ \\mathrm m')} (sàn tầng 2 ở ${so('x=3{,}0\\ \\mathrm m')}). Thang đi từ tầng 3 lên tầng 9 rồi xuống tầng 5.<br><b>a)</b> ${m('d')} (a<sub>1</sub>), ${m('s')} (a<sub>2</sub>)<br><b>b)</b> sau đó về tầng 3, cả hành trình: ${m('d')} (b<sub>1</sub>), ${m('s')} (b<sub>2</sub>)`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>'] },
    { t: 'Dạng 2 · Bài 1', de: `${m('Ox')} hướng Bắc, gốc ${m('O')} ở cổng trường. Xe đạp đi từ ${so('x_1=4\\ \\mathrm{km}')} về phía Nam tới ${so('x_2=-2\\ \\mathrm{km}')}, rồi quay đầu về phía Bắc tới ${so('x_3=1\\ \\mathrm{km}')}.<br><b>a)</b> độ dịch chuyển đoạn ${m('x_1\\to x_2')}<br><b>b)</b> cả hành trình: ${m('d')} (b<sub>1</sub>), ${m('s')} (b<sub>2</sub>)<br><b>c)</b> điểm dừng ở phía nào của điểm xuất phát`, o: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'] },
    { t: 'Dạng 2 · Bài 2', de: `Trục ${m('Ox')} hướng Đông, gốc ${m('O')} ở ngã ba. Người chạy bộ đi từ ${so('x_1=-300\\ \\mathrm m')} tới ${so('x_2=500\\ \\mathrm m')} rồi quay về ${so('x_3=200\\ \\mathrm m')}.<br><b>a)</b> cả hành trình: ${m('d')} (a<sub>1</sub>), ${m('s')} (a<sub>2</sub>)<br><b>b)</b> điểm dừng ở phía nào của điểm xuất phát`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b'] },
    { t: 'Dạng 3 · Bài 1', de: `Đi thẳng ${so('400\\ \\mathrm m')} về phía Bắc, rồi rẽ đi thẳng ${so('300\\ \\mathrm m')} về phía Đông.<br><b>a)</b> quãng đường<br><b>b)</b> độ lớn độ dịch chuyển<br><b>c)</b> góc giữa độ dịch chuyển và hướng Bắc`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 3 · Bài 2', de: `Thiết bị bay không người lái bay thẳng ${so('5{,}0\\ \\mathrm{km}')} về phía Tây, rồi bay thẳng ${so('12\\ \\mathrm{km}')} về phía Nam (cùng độ cao).<br><b>a)</b> quãng đường<br><b>b)</b> độ lớn độ dịch chuyển<br><b>c)</b> góc giữa độ dịch chuyển và hướng Tây`, o: ['a', 'b', 'c'] },
  ], [
    { t: 'Dạng 4 · Bài 1', de: `Chạy bộ trên đường thẳng, không đổi chiều: ${so('3{,}0\\ \\mathrm{km}')} hết ${nw('15 phút')}, nghỉ ${nw('5 phút')}, chạy tiếp ${so('2{,}0\\ \\mathrm{km}')} hết ${nw('20 phút')}. Biết ${so('1\\ \\mathrm{m/s}=3{,}6\\ \\mathrm{km/h}')}.<br><b>a)</b> tốc độ trung bình đoạn đầu (a<sub>1</sub>), đoạn sau (a<sub>2</sub>), theo km/h<br><b>b)</b> tốc độ trung bình cả hành trình, theo km/h<br><b>c)</b> kết quả b) đổi ra m/s`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'] },
    { t: 'Dạng 4 · Bài 2', de: `Xe buýt chạy trên đường thẳng, không đổi chiều: ${so('12\\ \\mathrm{km}')} hết ${nw('15 phút')}, dừng đón khách ${nw('6 phút')}, chạy tiếp ${so('9\\ \\mathrm{km}')} hết ${nw('15 phút')}. Biết ${so('1\\ \\mathrm{m/s}=3{,}6\\ \\mathrm{km/h}')}.<br><b>a)</b> tốc độ trung bình cả hành trình, theo km/h<br><b>b)</b> kết quả a) đổi ra m/s<br><b>c)</b> tốc độ trung bình nếu xe không dừng đón khách, theo km/h`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 5 · Bài 1', de: `Robot hút bụi chạy với tốc độ không đổi: từ ${m('O')} đi thẳng ${so('9\\ \\mathrm m')} về phía Đông, quay đầu đi ${so('3\\ \\mathrm m')} về phía Tây trên cùng đường, rồi rẽ đi thẳng ${so('8\\ \\mathrm m')} về phía Bắc; hết ${so('40\\ \\mathrm s')}.<br><b>a)</b> quãng đường<br><b>b)</b> độ lớn độ dịch chuyển<br><b>c)</b> góc giữa độ dịch chuyển và hướng Đông<br><b>d)</b> tốc độ trung bình`, o: ['a', 'b', 'c', 'd'] },
    { t: 'Dạng 5 · Bài 2', de: `Thuyền đi thẳng ${so('7\\ \\mathrm{km}')} về phía Bắc, quay lại ${so('3\\ \\mathrm{km}')} về phía Nam trên cùng đường, rồi rẽ đi thẳng ${so('3\\ \\mathrm{km}')} về phía Đông; hết ${nw('30 phút')}.<br><b>a)</b> quãng đường<br><b>b)</b> độ lớn độ dịch chuyển<br><b>c)</b> góc giữa độ dịch chuyển và hướng Bắc<br><b>d)</b> tốc độ trung bình, theo km/h`, o: ['a', 'b', 'c', 'd'] },
    nhap(7),
  ]],
  dap: [
    `D1·1: a<sub>1</sub>) +500 m · a<sub>2</sub>) 1900 m · b<sub>1</sub>) 0 · b<sub>2</sub>) 2400 m &nbsp;|&nbsp; D1·2: a<sub>1</sub>) +6 m · a<sub>2</sub>) 30 m · b<sub>1</sub>) 0 · b<sub>2</sub>) 36 m &nbsp;|&nbsp; D2·1: a) ${m("-")}6 km · b<sub>1</sub>) ${m("-")}3 km · b<sub>2</sub>) 9 km · c) phía Nam &nbsp;|&nbsp; D2·2: a<sub>1</sub>) +500 m · a<sub>2</sub>) 1100 m · b) phía Đông &nbsp;|&nbsp; D3·1: a) 700 m · b) 500 m · c) ${m("\\approx")} 37° &nbsp;|&nbsp; D3·2: a) 17 km · b) 13 km · c) ${m("\\approx")} 67°`,
    `D4·1: a<sub>1</sub>) 12 km/h · a<sub>2</sub>) 6 km/h · b) 7,5 km/h · c) ${m("\\approx")} 2,08 m/s &nbsp;|&nbsp; D4·2: a) 35 km/h · b) ${m("\\approx")} 9,72 m/s · c) 42 km/h &nbsp;|&nbsp; D5·1: a) 20 m · b) 10 m · c) ${m("\\approx")} 53° (về phía Bắc) · d) 0,5 m/s &nbsp;|&nbsp; D5·2: a) 13 km · b) 5 km · c) ${m("\\approx")} 37° (về phía Đông) · d) 26 km/h`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 2], kq: [[1, 2, 3], [4, 5]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: `chất điểm 1·4 · hệ quy chiếu 2·1 · độ dịch chuyển 2·2 · quãng đường 2·3 · ray uốn 3·1 · tốc độ trung bình 3·2 · bẫy 3·3 · bài toán mẫu 4·2 · dạng 1–3 ${m("\\to")} 6·1 · dạng 4–5 ${m("\\to")} 7·1`,
  out: process.argv[2],
});
