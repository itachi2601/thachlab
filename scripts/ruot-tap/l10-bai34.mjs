// Ruột tập VL10 – Bài 34 · Khối lượng riêng. Áp suất chất lỏng (lesson id 79). Quyển Chương 7 lớp 10: bài 33 = tr. 1–12, bài 34 = tr. 13–24.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự giải vào vở · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l10-bai34.mjs (toàn bộ SVG tự vẽ, không dùng ảnh Halliday). Nội dung theo bài web (book/cache/79.json, tải từ DB 12/11/2026):
// mục tiêu, dự đoán lặn 2 m, II.1–II.6, ba thí nghiệm (khối nhôm, bút chì, chai đục lỗ), ba bẫy, Trả bài 6 câu, bài toán mẫu bể cá,
// thử thách, 5 dạng bài tập mẫu. Mọi đáp số (bài tập mẫu, Bài tương tự) tính lại bằng Python 12/11/2026.
// Tránh 4 lỗi lặp HS ảo L11 Ch.3: hằng số (g, ρ nước, pₐ, atm) in sẵn ở tr.1 trước mọi câu hỏi · Mục tiêu/chú thích hình không lộ đáp án
// Dự đoán (mục tiêu không nói "chỉ phụ thuộc độ sâu"; mũi tên M/N vẽ bằng nhau) · ô đáp số rộng (cot: 2 khi kép) · dòng kẻ ≥ số ý.
// Chạy: node scripts/ruot-tap/l10-bai34.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl10-bai34.pdf
//       node scripts/ruot-tap/l10-bai34.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l10-bai34/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL10b34 as H } from './hinh-l10-bai34.mjs';

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
  const out = resolve(HERE, 'out/hinh-l10-bai34'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 34, lid: 79, ten: 'KHỐI LƯỢNG RIÊNG · ÁP SUẤT CHẤT LỎNG', lop: 10, baiDau: 33, sub: 'Vật lí 10 · Chương 7: Biến dạng của vật rắn. Áp suất chất lỏng' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const g10 = nw(m('g=10\\ \\mathrm{m/s^2}'));
const rho = m('\\rho'), pa = m('p_a');
const u = (s) => nw(m(s));

const ttHaiCot = '<style>.bt>.gi{display:grid;grid-template-columns:1fr 1fr;column-gap:4mm}.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm}.yo .oo{flex:none;display:flex;gap:3mm}.yo{line-height:1.35}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';
const p1 = `${ttHaiCot}<section class="page">
${head('BÀI 34 · KHỐI LƯỢNG RIÊNG · ÁP SUẤT CHẤT LỎNG', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Tính <b>khối lượng riêng</b> ${m('\\rho')}; đổi g/cm³ ${m('\\leftrightarrow')} kg/m³`)}
${dong(`${ck}Phân biệt <b>áp lực</b> và <b>áp suất</b>; tính áp suất của vật rắn ép lên mặt`)}
${dong(`${ck}Tính <b>áp suất chất lỏng</b> tại một điểm; biết nó phụ thuộc những đại lượng nào`)}
${dong(`${ck}Vận dụng vào <b>bình thông nhau</b> và <b>lực đẩy Archimedes</b>`)}
</div>
<div class="card soft" style="padding:1mm 3mm"><b>Số liệu dùng trong cả tập</b> (đề không cho thì lấy): ${g10}; nước ${u('\\rho=1000\\ \\mathrm{kg/m^3}')}; áp suất khí quyển ${u('p_a=1{,}0\\cdot10^5\\ \\mathrm{Pa}')}; ${u('1\\ \\mathrm{atm}=1{,}013\\cdot10^5\\ \\mathrm{Pa}')}</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Lặn xuống đúng 2 m dưới mặt nước, tai em bị nước ép mạnh hơn ở đâu?</p>
<div class="fig-side" style="${fs(48)}"><div>
${opt('A', 'Ở hồ, vì phía trên có nhiều nước hơn')}
${opt('B', 'Ở bể bơi, vì thành bể dồn nước ép lại')}
${opt('C', 'Như nhau ở hai nơi')}
${opt('D', 'Ở hồ, vì mặt hồ rộng hứng nhiều không khí')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 2)}</div>
${H.beHo()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(2)}</div>
${h3(4, 'II.1 · Khối lượng riêng', '1·4')}
<div class="card" style="padding:1.2mm 3mm">
<div>Khối lượng riêng là khối lượng của một ${f(25)} chất: &nbsp;${m('\\rho=')} ${f(14)}, đơn vị ${f(14)}</div>
<div>Mỗi chất có một ${rho} riêng, nên dùng ${rho} để ${f(25)} chất. Cưa đôi một khối sắt: ${rho} mỗi nửa ${f(25)}</div>
<div>${u('1\\ \\mathrm{g/cm^3}=')} ${f(14)} kg/m³ · 1 lít ${m('=')} ${f(14)} m³ · ${u('1\\ \\mathrm{cm^3}=')} ${f(14)} m³</div>
<div>Trọng lượng của vật theo ${rho}, ${m('V')}, ${m('g')}: ${m('P=')} ${f(16)} · trọng lượng riêng ${m('d=')} ${f(14)}</div>
<div>Ví dụ: chai nước 1,5 lít có ${m('V=')} ${f(16)} m³, nên ${m('m=\\rho V=')} ${f(14)} kg</div>
<div class="hint" style="margin-top:.6mm">${rho} (kg/m³): dầu ăn ${m('\\approx')} 920 · nước 1000 · nhôm 2700 · sắt 7800 · thuỷ ngân 13 600</div></div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('ĐO KHỐI LƯỢNG RIÊNG · ÁP LỰC VÀ ÁP SUẤT')}
${h3(1, 'Thí nghiệm: bốn khối nhôm to nhỏ khác nhau', '2·1')}
<div class="fig-side" style="${fs(42)}"><div>
<div><b>Làm:</b> cân từng khối (độ chia 0,1 g); thả khối vào bình chia độ (độ chia 1 cm³): ${m('V=V_2-V_1=')} ${f(20)}</div>
<table class="tbl-ct" style="margin-top:.8mm"><tr><th>${m('m\\ (\\mathrm g)')}</th><th>${m('V\\ (\\mathrm{cm^3})')}</th><th>${m('\\rho\\ (\\mathrm{g/cm^3})')}</th></tr>
<tr><td>21,1</td><td>8</td><td></td></tr>
<tr><td>40,9</td><td>15</td><td></td></tr>
<tr><td>67,2</td><td>25</td><td></td></tr>
<tr><td>99,7</td><td>37</td><td></td></tr></table>
<div class="hint">Số liệu minh hoạ, chưa phải số đo thật. Nhôm theo bảng: 2,70 g/cm³.</div></div>
${H.binhChia()}</div>
<div class="card" style="margin-top:.6mm;padding:1mm 3mm">
<div><b>Rút ra:</b> khối to hay nhỏ thì ${rho} ${ck}khác nhau nhiều &nbsp;${ck}gần như nhau. Hàng lệch nhiều nhất: ${f(14)} vì:</div>${lines(1)}</div>
${h3(2, 'II.2 · Áp lực và áp suất', '2·2')}
<div class="card" style="padding:1.2mm 3mm">
<div><b>Áp lực:</b> lực ép có phương ${f(25)} với mặt bị ép.</div>
<div><b>Áp suất:</b> áp lực trên một ${f(25)} diện tích bị ép: ${m('p=')} ${f(16)}</div>
<div>Đơn vị: ${u('1\\ \\mathrm{Pa}=1')} ${f(14)} · ${u('1\\ \\mathrm{cm^2}=')} ${f(14)} m²</div>
<div>Cùng áp lực: ${m('S')} nhỏ thì ${m('p')} ${f(14)}; ${m('S')} lớn thì ${m('p')} ${f(14)}. Vật đặt trên sàn ngang: ${m('F=')} ${f(14)}</div></div>
${h3(3, 'Thí nghiệm: bút chì giữa hai ngón tay', '2·3')}
<div class="card fig-side" style="${fs(42)};padding:1.2mm 3mm"><div>
<div><b>Làm:</b> kẹp bút chì đã gọt giữa ngón cái (đầu bằng) và ngón trỏ (đầu nhọn), giữ bút nằm yên, ép nhẹ.</div>
<div><b>Quan sát:</b> ngón ${f(25)} đau hơn.</div>
<div><b>Rút ra:</b> bút đứng yên nên áp lực lên hai ngón ${f(25)}; đầu nhọn có ${m('S')} ${f(14)} nên áp suất ${f(14)}.</div></div>
${H.butChi()}</div>
${h3(4, 'Làm nhanh', '2·4')}
${box(cau(`<b>Câu 1.</b> Viên gạch ${u('2\\ \\mathrm{kg}')}, kích thước ${nw('20 cm × 10 cm × 5 cm')}, đặt đứng trên mặt ${nw('10 cm × 5 cm')}. Áp suất gạch ép lên sàn?`, 2)
 + cau(`<b>Câu 2.</b> Cùng viên gạch, đặt nằm trên mặt lớn nhất ${nw('20 cm × 10 cm')}: áp suất lên sàn tăng hay giảm, bao nhiêu lần?`, 1))}
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('ÁP SUẤT CHẤT LỎNG · BÌNH THÔNG NHAU · LỰC ĐẨY ARCHIMEDES')}
${h3(1, 'II.3 · Áp suất chất lỏng', '3·1')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div>Chất lỏng ép lên đáy, thành bình và mọi vật trong lòng nó theo ${f(25)} phương.</div>
<div style="margin:.5mm 0">Tại điểm sâu ${m('h')}: ${m('p=')} ${f(14)} ${m('+')} ${f(16)}</div>
<div>${pa}: áp suất ${f(25)} trên mặt thoáng</div>
<div>${m('\\rho g h')}: phần do ${f(25)} gây ra</div>
<div>${m('h')} đo từ ${f(25)} xuống điểm</div>
<div>Hai điểm chênh độ sâu: ${m('\\Delta p=')} ${f(16)}</div>
<div>Cùng chất lỏng đứng yên, cùng ${f(16)} ${m('\\to')} cùng áp suất.</div></div>
${H.doSau()}</div>
${h3(2, 'Thí nghiệm: chai nhựa đục lỗ', '3·2')}
<div class="card fig-side" style="${fs(30)};padding:1.2mm 3mm"><div>
<div><b>Làm:</b> chai 1 đục 3 lỗ ở ba độ cao; chai 2 (không vẽ) đục 4 lỗ quanh thân ở cùng một độ cao. Đổ đầy nước, mở lỗ.</div>
<div><b>Quan sát:</b> chai 1, lỗ số ${f(10)} phun mạnh nhất · chai 2, bốn tia ${f(25)}</div>
<div><b>Rút ra:</b> áp suất ${f(14)} theo độ sâu; cùng độ sâu, nước ép như nhau theo ${f(16)}.</div></div>
${H.chaiLo()}</div>
${h3(3, 'II.4 · Bình thông nhau', '3·3')}
<div class="card fig-side" style="${fs(40)};padding:1.2mm 3mm"><div>
<div>Một chất lỏng đứng yên: mực ở các nhánh ${f(25)}. Ví dụ: vòi ấm và thân ấm có mực nước ${f(20)}</div>
<div>Hai chất lỏng không hoà tan: A ở mặt phân cách, B cùng mức ngang ở nhánh kia, cùng nằm trong ${f(14)} nên ${m('p_A=p_B')}:</div>
<div style="margin:.5mm 0">${pa} ${m('+')} ${f(14)} ${m('=')} ${pa} ${m('+')} ${f(14)} &nbsp;${m('\\Rightarrow')}&nbsp; ${m('\\rho_1h_1=')} ${f(14)}</div>
<div>(1: dầu, 2: nước) ${m('h_1, h_2')} đo từ mức ${f(14)} lên tới ${f(25)} mỗi nhánh.</div></div>
${H.thongNhau()}</div>
${h3(4, 'II.5 · Lực đẩy Archimedes', '3·4')}
<div class="card fig-side" style="${fs(42)};padding:1.2mm 3mm"><div>
<div>Mặt dưới sâu hơn mặt trên nên bị ép ${f(14)}: chất lỏng đẩy vật hướng ${f(14)}.</div>
<div style="margin:.5mm 0">${m('F_A=')} ${f(25)} &nbsp;(${m('V')} là thể tích phần ${f(14)})</div>
<div>Vật đặc: ${m('\\rho_{\\text{vật}}\\lt\\rho_\\ell')} thì ${f(14)}; ${m('\\rho_{\\text{vật}}\\gt\\rho_\\ell')} thì ${f(14)}; bằng nhau thì ${f(14)}</div>
<div>Vật nổi, đứng yên: ${m('F_A=')} ${f(14)}</div></div>
${H.archimedes()}</div>
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('BA CÁI BẪY · TRẢ BÀI · TỰ KIỂM TRA')}
${h3(1, 'III · Ba cái bẫy hay sập', '4·1')}
<div class="card fig-side" style="${fs(44)};padding:1mm 3mm"><div>
<div class="trap">${ck}<span><b>“Nhiều nước thì đáy chịu áp suất lớn.”</b> Áp suất ở đáy chỉ theo ${m('\\rho')} và độ sâu ${m('h')}; lượng nước, diện tích đáy, hình dạng bình không có trong ${m('\\rho g h')}.</span></div>
<div class="trap">${ck}<span><b>“Quên ${pa}.”</b> Hỏi áp suất <b>tại</b> điểm (tuyệt đối): ${m('p_a+\\rho g h')}. Hỏi áp suất <b>do chất lỏng</b> hay số chỉ áp kế (áp suất dư): chỉ ${m('\\rho g h')}.</span></div>
<div class="trap">${ck}<span><b>“Thế số chưa đổi đơn vị.”</b> g/cm³ ${m('\\to')} kg/m³ (×1000), cm ${m('\\to')} m, cm² ${m('\\to')} m² (×10<sup>−4</sup>) trước khi thế.</span></div></div>
${H.baBinh()}</div>
${h3(2, 'IV · Trả bài 6 câu', '4·2')}
${box(`${tb('1. Khối lượng riêng: định nghĩa, công thức, đơn vị, đổi g/cm³ ra kg/m³.')}${lines(2)}
${tb('2. Áp lực khác áp suất ở đâu? Công thức áp suất.')}${lines(2)}
${tb('3. Công thức áp suất tại điểm ở độ sâu h; nghĩa từng số hạng.')}${lines(2)}
${tb('4. Vì sao áp suất ở đáy không phụ thuộc hình dạng bình, lượng chất lỏng?')}${lines(2)}
${tb('5. Bình thông nhau: một chất lỏng thì sao? Hai chất lỏng không hoà tan thì sao?')}${lines(2)}
${tb('6. Lực đẩy Archimedes: công thức, hướng; điều kiện vật nổi.')}${lines(2)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/6 câu · chưa thuộc: ${f(25)} ${nw(`${m('\\to')} đọc lại ô Tập ${f(12)}`)}</div>
${h3(3, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '4·3')}
${rkHai([1, 2, 3, 4], [5, 6, 7])}
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TOÁN MẪU · BÀI TẬP VỀ NHÀ · THỬ THÁCH')}
${h3(1, 'V · Bài toán mẫu: bể cá', '5·1')}
<div class="fig-side" style="${fs(40)}"><div>
<div class="card soft" style="padding:1.2mm 3mm;margin:0">Bể cá thành thẳng đứng, đáy ${nw('60 cm × 40 cm')}, chứa nước cao ${u('50\\ \\mathrm{cm}')}. Tính:
<div><b>a)</b> khối lượng nước</div><div><b>b)</b> áp suất do nước gây ra ở đáy và áp suất tại đáy</div><div><b>c)</b> áp lực của nước lên đáy</div><div><b>d)</b> áp suất do nước gây ra tại M cách đáy ${u('20\\ \\mathrm{cm}')}</div></div>
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm;margin-top:1mm">
${wl(`a) ${m('S=')} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ${m('V=')} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ${m('m=')}`, 1)}${wl(`b) ${m('\\rho g h=')} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ${m('p=p_a+\\rho g h=')}`, 1)}${wl('c) Áp lực của nước (dùng phần nào của p?):', 2)}${wl(`d) ${m('h_M=')} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ${m('p_M=')}`, 1)}${wl(`Kiểm tra: ${m('mg=')} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; khớp câu c) không? Vì sao?`, 1)}</div></div>
${H.beCa()}</div>
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm;margin-top:1mm">
<div class="ln"><b>Điền tiếp:</b> cùng bể, nước muối ${u('\\rho=1030\\ \\mathrm{kg/m^3}')} cao ${u('30\\ \\mathrm{cm}')}.</div>
${wl(`Bước 2: áp suất do nước muối ở đáy ${m('=')}`, 1)}${wl(`Bước 3: áp lực của nước muối lên đáy ${m('=')}`, 1)}</div>
${K.btvn().replace('<i>1</i>Đề BTVN', '<i>2</i>Đề BTVN')}
${h3(3, 'Thử thách phân tầng', '5·3')}
<div class="fig-side" style="${fs(36)}">${box(wl(`${m('\\bigstar')} Viên sỏi ${nw('54 g')} thả vào bình chia độ, nước dâng thêm ${nw('20 cm³')}. Khối lượng riêng của sỏi (kg/m³)?`, 2)
 + wl(`${m('\\bigstar\\bigstar')} Ống U chứa nước, rót vào một nhánh cột dầu ${u('\\rho=800\\ \\mathrm{kg/m^3}')} cao ${nw('15 cm')}. Mặt dầu cao hơn mặt nước bao nhiêu?`, 3)
 + wl(`${m('\\bigstar\\bigstar\\bigstar')} Theo hình bên: áp suất dư ở vòi tầng 1 và vòi tầng 6 khi khoá? Máy giặt tầng 6 cần áp suất dư ít nhất ${u('0{,}3\\cdot10^5\\ \\mathrm{Pa}')}: bồn có đủ cao không?`, 3))}${H.bonMai()}</div>
${h3(4, 'VI · Mang về: điều em dễ quên nhất', '5·4')}
${box(wl('1.', 1) + wl('2.', 1) + wl('3.', 1))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Khối lượng riêng và áp suất p = F/S (đổi đơn vị)',
    de: `Khối kim loại hình hộp ${nw('3,0 cm × 4,0 cm × 15 cm')}, khối lượng ${nw('1,26 kg')}.<br><b>a)</b> khối lượng riêng (kg/m³)<br><b>b)</b> áp suất lên mặt bàn khi đặt nằm trên mặt lớn nhất ${nw('4,0 cm × 15 cm')}<br><b>c)</b> áp suất khi dựng đứng trên mặt nhỏ nhất ${nw('3,0 cm × 4,0 cm')}`,
    nd: `${m('V')}: cm³ ${m('\\to')} m³ (×${f(12)}); ${m('S')}: cm² ${m('\\to')} m² (×${f(12)}); áp lực ${m('F=')} ${f(12)}`, a: ['a', 'b', 'c'], gi: 4 },
  { t: `Dạng 2 · Dễ · Áp suất chất lỏng theo độ sâu: ${m('p=\\rho gh')}`,
    de: `Bể dầu hoả ${rho} ${nw('= 0,80 g/cm³')}, mực dầu cao ${nw('2,5 m')}. Chỉ xét áp suất do dầu.<br><b>a)</b> áp suất do dầu ở đáy bể<br><b>b)</b> áp suất do dầu tại M cách mặt thoáng ${nw('1,0 m')}<br><b>c)</b> áp lực của dầu lên nắp van ở đáy, diện tích ${nw('20 cm²')}`,
    nd: `đổi ${rho} ra ${f(14)}; ${m('h')} đo từ ${f(25)}; áp lực ${m('F=')} ${f(12)}`, a: ['a', 'b', 'c'], gi: 3, fig: H.beDau('') },
  { t: 'Dạng 3 · Trung bình · Áp suất tuyệt đối và áp suất dư',
    de: `Thùng hình trụ cao ${nw('1,8 m')}, miệng hở, đầy nước; áp kế đo áp suất dư.<br><b>a)</b> tại đáy: áp suất do nước (a<sub>1</sub>), áp suất tuyệt đối (a<sub>2</sub>)<br><b>b)</b> tại A cách <b>đáy</b> ${nw('50 cm')}: áp suất tuyệt đối (b<sub>1</sub>), số chỉ áp kế (b<sub>2</sub>)<br><b>c)</b> B có áp suất tuyệt đối ${nw('1,12·10<sup>5</sup> Pa')}: B sâu bao nhiêu`,
    nd: `áp kế chỉ ${f(12)}; ${u('h_A=')} ${f(12)}; ngược lại ${m('h=(p-p_a)/\\rho g')}`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], gi: 5, fig: H.thungA(''), cot: 5 },
  { t: 'Dạng 4 · Khó · Bình thông nhau chứa hai chất lỏng không hoà tan',
    de: `Ống chữ U tiết diện đều, hai đầu hở, chứa thuỷ ngân ${u('\\rho_2=13\\,600\\ \\mathrm{kg/m^3}')}. Rót nước vào nhánh trái, cột nước cao ${u('20{,}4\\ \\mathrm{cm}')} tính từ mặt phân cách.<br><b>a)</b> mặt thuỷ ngân nhánh phải cao hơn mặt phân cách bao nhiêu cm<br><b>b)</b> mặt nước nhánh trái cao hơn mặt thuỷ ngân nhánh phải bao nhiêu cm<br><b>c)</b> muốn mặt thuỷ ngân nhánh phải cao hơn mặt phân cách ${u('3{,}0\\ \\mathrm{cm}')}: cột nước cao bao nhiêu cm`,
    nd: `A ở mặt phân cách, B cùng mức ngang nhánh phải, cùng trong ${f(16)}; nước ${u('\\rho_1=1000')} ${m('\\Rightarrow')} ${m('\\rho_1h_1=')} ${f(16)}`, a: ['a', 'b', 'c'], gi: 6, fig: H.uHg('') },
  { t: 'Dạng 5 · Khó · Lực đẩy Archimedes: khối nổi và điều kiện chìm hẳn',
    de: `Khối gỗ hình hộp đáy ${nw('20 cm × 20 cm')}, cao ${u('10\\ \\mathrm{cm}')}, khối lượng ${u('2{,}4\\ \\mathrm{kg}')}, thả vào nước, đáy nằm ngang.<br><b>a)</b> khối lượng riêng của gỗ (a<sub>1</sub>); khối nổi hay chìm (a<sub>2</sub>)<br><b>b)</b> lực đẩy Archimedes khi khối đứng yên trên mặt nước<br><b>c)</b> chiều cao phần chìm<br><b>d)</b> đặt lên mặt trên một vật nhỏ để khối vừa chìm hẳn (mực nước coi như không đổi): khối lượng tối thiểu của vật`,
    nd: `khối nổi đứng yên ${m('\\Rightarrow')} ${m('F_A=')} ${f(12)}; ${m('V')} trong ${m('F_A')} là thể tích ${f(16)}`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c', 'd'], gi: 7, fig: H.goNoi(''), cot: 3 },
];

// Bài tương tự giải vào vở (thầy chốt 10/11): 1 cột; ô đáp số 25 mm đặt cuối dòng của ý (oY), nhãn khớp a) b) c)…
// Đáp số tính bằng Python 12/11/2026 (g = 10, ρ nước 1000, pₐ = 1,0·10⁵ Pa, 1 atm = 1,013·10⁵ Pa).
const oY = (s, o, w = 25) => s.split('<br>').map((p) => {
  const y = p.match(/^<b>([a-d])\)<\/b>/);
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
    { t: 'Dạng 1 · Bài 1', de: `Khối sắt hình hộp ${nw('2,0 cm × 5,0 cm × 12 cm')}, khối lượng ${u('936\\ \\mathrm g')}.<br><b>a)</b> khối lượng riêng (kg/m³)<br><b>b)</b> áp suất lên bàn khi đặt trên mặt lớn nhất ${nw('5,0 cm × 12 cm')}<br><b>c)</b> áp suất khi dựng trên mặt nhỏ nhất ${nw('2,0 cm × 5,0 cm')}`, fig: H.khoiHop('', '12 cm'), fw: 38, o: ['a', 'b', 'c'] },
    { t: 'Dạng 1 · Bài 2', de: `Người ${u('60\\ \\mathrm{kg}')} đứng trên sàn ngang; mỗi bàn chân tiếp xúc sàn ${u('200\\ \\mathrm{cm^2}')}.<br><b>a)</b> áp suất lên sàn khi đứng hai chân<br><b>b)</b> áp suất khi đứng một chân<br><b>c)</b> đứng trên tấm ván diện tích ${u('0{,}40\\ \\mathrm{m^2}')} (bỏ qua khối lượng ván): áp suất lên sàn`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 2 · Bài 1', de: `Hồ nước sâu ${u('3{,}0\\ \\mathrm m')}. Chỉ xét áp suất do nước.<br><b>a)</b> áp suất do nước ở đáy hồ<br><b>b)</b> áp suất do nước tại M cách <b>đáy</b> ${u('1{,}2\\ \\mathrm m')}<br><b>c)</b> áp lực của nước lên ô kính ở đáy, diện tích ${u('400\\ \\mathrm{cm^2}')}`, fig: H.hoKinh(''), fw: 38, o: ['a', 'b', 'c'] },
    { t: 'Dạng 2 · Bài 2', de: `Thùng xăng ${u('\\rho=0{,}70\\ \\mathrm{g/cm^3}')}, mực xăng cao ${u('1{,}2\\ \\mathrm m')}. Chỉ xét áp suất do xăng.<br><b>a)</b> áp suất ở đáy thùng<br><b>b)</b> áp suất tại điểm sâu ${u('0{,}50\\ \\mathrm m')}<br><b>c)</b> chênh lệch áp suất giữa đáy và điểm đó`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 3 · Bài 1', de: `Thợ lặn ở độ sâu ${u('20\\ \\mathrm m')} trong nước biển ${u('\\rho=1030\\ \\mathrm{kg/m^3}')}.<br><b>a)</b> áp suất dư tại chỗ thợ lặn<br><b>b)</b> áp suất tuyệt đối tại đó<br><b>c)</b> áp suất tuyệt đối đổi ra atm`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 3 · Bài 2', de: `Áp kế ở đáy một bể nước hở chỉ áp suất dư ${u('1{,}5\\cdot10^4\\ \\mathrm{Pa}')}.<br><b>a)</b> độ sâu nước trong bể<br><b>b)</b> áp suất tuyệt đối ở đáy<br><b>c)</b> điểm có áp suất tuyệt đối ${u('1{,}08\\cdot10^5\\ \\mathrm{Pa}')} cách <b>đáy</b> bao nhiêu`, o: ['a', 'b', 'c'] },
    nhap(1),
  ], [
    { t: 'Dạng 4 · Bài 1', de: `Ống chữ U hai đầu hở chứa nước; rót dầu ${u('\\rho=800\\ \\mathrm{kg/m^3}')} vào nhánh trái, cột dầu cao ${u('10\\ \\mathrm{cm}')} tính từ mặt phân cách.<br><b>a)</b> mặt nước nhánh phải cao hơn mặt phân cách<br><b>b)</b> mặt dầu cao hơn mặt nước nhánh phải<br><b>c)</b> muốn hai mặt thoáng chênh nhau ${u('3{,}0\\ \\mathrm{cm}')}: cột dầu cao bao nhiêu`, fig: H.uDau(''), fw: 38, o: ['a', 'b', 'c'] },
    { t: 'Dạng 4 · Bài 2', de: `Ống chữ U hai đầu hở chứa thuỷ ngân ${u('13\\,600\\ \\mathrm{kg/m^3}')}; rót nước vào nhánh trái, cột nước cao ${u('27{,}2\\ \\mathrm{cm}')} tính từ mặt phân cách.<br><b>a)</b> mặt thuỷ ngân nhánh phải cao hơn mặt phân cách<br><b>b)</b> mặt nước cao hơn mặt thuỷ ngân nhánh phải<br><b>c)</b> thay nước bằng dầu ${u('800\\ \\mathrm{kg/m^3}')}, cột dầu cũng cao ${u('27{,}2\\ \\mathrm{cm}')}: làm lại câu a)`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 5 · Bài 1', de: `Khối gỗ lập phương cạnh ${u('10\\ \\mathrm{cm}')}, khối lượng ${u('0{,}70\\ \\mathrm{kg}')}, thả vào nước, đáy nằm ngang.<br><b>a)</b> khối lượng riêng của gỗ (a<sub>1</sub>); nổi hay chìm (a<sub>2</sub>)<br><b>b)</b> lực đẩy Archimedes khi khối đứng yên<br><b>c)</b> chiều cao phần chìm<br><b>d)</b> khối lượng vật nhỏ đặt lên để khối vừa chìm hẳn`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c', 'd'] },
    { t: 'Dạng 5 · Bài 2', de: `Vật nhôm đặc ${u('\\rho=2700\\ \\mathrm{kg/m^3}')}, thể tích ${u('200\\ \\mathrm{cm^3}')}, treo vào lực kế rồi nhúng chìm hẳn; vật đứng yên nên số chỉ lực kế ${m('=P-F_A')}.<br><b>a)</b> trọng lượng của vật<br><b>b)</b> lực đẩy Archimedes trong nước<br><b>c)</b> số chỉ lực kế khi vật chìm trong nước<br><b>d)</b> số chỉ lực kế khi vật chìm trong dầu ${u('800\\ \\mathrm{kg/m^3}')}`, o: ['a', 'b', 'c', 'd'] },
    nhap(7),
  ]],
  dap: [
    `D1·1: a) 7800 kg/m³ · b) 1560 Pa · c) 9360 Pa &nbsp;|&nbsp; D1·2: a) 15&nbsp;000 Pa · b) 30&nbsp;000 Pa · c) 1500 Pa &nbsp;|&nbsp; D2·1: a) 30&nbsp;000 Pa · b) 18&nbsp;000 Pa · c) 1200 N &nbsp;|&nbsp; D2·2: a) 8400 Pa · b) 3500 Pa · c) 4900 Pa &nbsp;|&nbsp; D3·1: a) 2,06·10<sup>5</sup> Pa · b) 3,06·10<sup>5</sup> Pa · c) ${m('\\approx')} 3,02 atm &nbsp;|&nbsp; D3·2: a) 1,5 m · b) 1,15·10<sup>5</sup> Pa · c) 0,70 m`,
    `D4·1: a) 8,0 cm · b) 2,0 cm · c) 15 cm &nbsp;|&nbsp; D4·2: a) 2,0 cm · b) 25,2 cm · c) 1,6 cm &nbsp;|&nbsp; D5·1: a<sub>1</sub>) 700 kg/m³ · a<sub>2</sub>) nổi · b) 7,0 N · c) 7,0 cm · d) 0,30 kg &nbsp;|&nbsp; D5·2: a) 5,4 N · b) 2,0 N · c) 3,4 N · d) 3,8 N`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 2], kq: [[1, 2, 3], [4, 5]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'khối lượng riêng 1·4 · đo khối lượng riêng 2·1 · áp suất 2·2 · áp suất chất lỏng 3·1 · bình thông nhau 3·3 · Archimedes 3·4 · bẫy 4·1 · bài toán mẫu 5·1 · dạng 1–3: 6·1 · dạng 4–5: 7·1',
  out: process.argv[2],
});
