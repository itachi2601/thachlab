// Ruột tập VL12 – Bài 5 · Thuyết động học phân tử chất khí (lesson id 6). Quyển Chương 2 lớp 12: bài 5 = tr. 1–12.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l12-bai5.mjs (toàn bộ SVG tự vẽ). Nội dung theo bài web (book/cache/6.json, tải từ DB 12/11/2026): mục tiêu, dự đoán
// hạt khói trong hộp kín, II.1–II.5, thí nghiệm Brown + ống khói trắng NH₃/HCl, ba bẫy, Trả bài 6 câu, bài toán mẫu túi khí,
// thử thách ⭐–⭐⭐⭐, 5 dạng bài tập mẫu. Đáp số Bài tương tự (tuongTu.dap) tính bằng Python 12/11/2026.
// Chạy: node scripts/ruot-tap/l12-bai5.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl12-bai5.pdf
//       node scripts/ruot-tap/l12-bai5.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l12-bai5/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL12b5 as H } from './hinh-l12-bai5.mjs';

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
  const out = resolve(HERE, 'out/hinh-l12-bai5'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 5, lid: 6, ten: 'THUYẾT ĐỘNG HỌC PHÂN TỬ CHẤT KHÍ', lop: 12, baiDau: 5, sub: 'Vật lí 12 · Chương 2: Khí lí tưởng' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const NA = nw(m('N_A=6{,}02\\cdot10^{23}\\ \\mathrm{mol^{-1}}'));
const dktc = 'đktc (0 °C, 1 atm)';
const ch = (s) => m(`\\mathrm{${s}}`);
const N2 = ch('N_2'), O2 = ch('O_2'), CO2 = ch('CO_2'), H2 = ch('H_2'), NH3 = ch('NH_3');
const g = (s) => nw(m(`${s}\\ \\mathrm g`)), L = (s) => nw(`${m(s)} lít`), gmol = (s) => nw(m(`M=${s}\\ \\mathrm{g/mol}`));
const pt = (a, b) => nw(m(`${a}\\cdot10^{${b}}`));

// Bài tương tự 1 cột, ô đáp số cuối dòng của ý (cùng cách l10-bai23).
const ttCss = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';

const p1 = `${ttCss}<section class="page">
${head('BÀI 5 · THUYẾT ĐỘNG HỌC PHÂN TỬ CHẤT KHÍ', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Nêu ba nội dung của <b>thuyết động học phân tử chất khí</b>; giải thích thí nghiệm của Brown`)}
${dong(`${ck}Giải thích <b>áp suất khí</b>; nêu bốn nội dung của <b>mô hình khí lí tưởng</b>`)}
${dong(`${ck}Tính số mol, số phân tử, khối lượng, thể tích khí ở đktc bằng ${m('n=\\dfrac{N}{N_A}=\\dfrac{m}{M}')}`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Hộp kính đậy kín chứa khói hương, không có gió. Rọi đèn ngang qua, nhìn qua kính lúp: mỗi hạt khói là một chấm sáng. Các chấm sáng sẽ thế nào?</p>
<div class="fig-side" style="${fs(42)}"><div>
${opt('A', 'Đứng yên lơ lửng một chỗ')}
${opt('B', 'Rơi đều xuống đáy theo đường thẳng')}
${opt('C', 'Cùng trôi chậm về một phía')}
${opt('D', 'Mỗi chấm nhảy hỗn loạn theo kiểu riêng, không dừng')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 1)}</div>
${H.hopKhoi()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Thí nghiệm Brown: hạt khói trong hộp kín', '1·4')}
<div class="card fig-side" style="${fs(40)};padding:1.2mm 3mm"><div>
<div><b>Giả thuyết cần kiểm:</b> chất khí gồm rất nhiều phân tử nhỏ mà mắt không thấy được.</div>
<div><b>Làm:</b> đậy kín hộp, chờ 30 s; rọi đèn ngang, theo dõi vài chấm sáng; làm lại khi hộp ấm hơn.</div>
<div><b>Quan sát:</b> chấm sáng đi theo đường ${f(24)}; hai chấm cạnh nhau đi giống hay khác kiểu? ${f(16)}; hộp ấm hơn thì chấm sáng ${f(32)}</div>
<div><b>Rút ra:</b> phân tử khí chuyển động ${f(30)}</div>
<div><b>Cơ chế:</b> phân tử khí va đập hạt khói từ ${f(18)}; hai phía không bao giờ ${f(18)} nên hạt bị đẩy lệch liên tục.</div>
<div><b>Chưa nói được gì:</b> không thấy phân tử; đường gấp khúc là của ${f(20)}, không phải của phân tử.</div></div>
${H.vaDap()}</div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('THUYẾT ĐỘNG HỌC PHÂN TỬ · PHÂN TỬ NHANH, MÙI LAN CHẬM')}
${h3(1, 'II.2 · Ba nội dung của thuyết: Nhỏ – Loạn – Đập', '2·1')}
<div class="card fig-side" style="${fs(42)};padding:1.2mm 3mm"><div>
<div><b>Nhỏ:</b> chất khí gồm rất nhiều phân tử, kích thước rất ${f(12)} so với ${f(24)} giữa chúng ⇒ lực tương tác (hút và đẩy) ${f(16)}, yếu hơn hẳn thể lỏng, rắn.</div>
<div><b>Loạn:</b> chuyển động ${f(20)}, không ngừng; nhiệt độ càng cao thì tốc độ ${f(16)}. Ở đktc, tốc độ trung bình cỡ vài trăm m/s (${N2} ở 0 °C: khoảng 455 m/s).</div>
<div><b>Đập:</b> phân tử va vào thành bình, tác dụng lên thành một ${f(12)} ⇒ gây ra ${f(20)} của khí.</div>
<div style="margin-top:.6mm"><b>Ví dụ:</b> bóng bay buộc kín nhúng nước nóng thì căng, nhúng nước đá thì xẹp. Giải thích theo nội dung Loạn và Đập:</div>${lines(2)}</div>
${H.baNoiDung()}</div>
${h3(2, 'II.3 · Thí nghiệm đo: ống khói trắng', '2·2')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div><b>Làm:</b> ống thuỷ tinh dài 40 cm nằm ngang; tẩm bông đầu A bằng ${NH3}, đầu B bằng HCl, bịt kín, bấm đồng hồ. Hai khí gặp nhau tạo vòng khói trắng ${ch('NH_4Cl')}.</div>
<table class="tbl-ct" style="margin-top:.6mm"><tr><th>Lần đo (số minh hoạ)</th><th>1</th><th>2</th><th>3</th></tr>
<tr><td>${m('x')} (cm)</td><td>23,5</td><td>24,0</td><td>24,2</td></tr>
<tr><td>${m('t')} (s)</td><td>180</td><td>177</td><td>188</td></tr>
<tr><td>Tốc độ lan ${m('x/t')} (cm/s)</td><td>0,13</td><td></td><td></td></tr></table></div>
${H.ongKhoi()}</div>
<div class="card" style="padding:1.2mm 3mm">
<div><b>Rút ra:</b> tốc độ lan cỡ ${f(12)} cm/s. Một phân tử bay cỡ 455 m/s = 45 500 cm/s, nhanh hơn (lấy tốc độ lan 0,13 cm/s) cỡ ${f(24)} lần.</div>
<div>Mùi lan chậm vì:</div>${lines(1)}
<div>Vòng khói luôn gần đầu ${f(12)} vì ở cùng nhiệt độ phân tử ${f(14)} hơn chuyển động chậm hơn (${NH3}: ${gmol('17')}; HCl: ${gmol('36{,}5')}).</div>
<div><b>Sai số:</b> ba lần đo lệch nhau tới 0,7 cm. Nêu hai nguyên nhân:</div>${lines(2)}</div>
${h3(3, 'Làm nhanh', '2·3')}
${box(cau(`Giữa các phân tử khí có lực tương tác không? Mạnh hay yếu, vì sao?`, 1))}
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('MÔ HÌNH KHÍ LÍ TƯỞNG · LƯỢNG CHẤT VÀ MOL')}
${h3(1, 'II.4 · Mô hình khí lí tưởng: Chấm – Không lực – Thẳng – Nảy', '3·1')}
<div class="card fig-side" style="${fs(36)};padding:1.2mm 3mm"><div>
<div><b>Chấm:</b> coi mỗi phân tử là một ${f(22)} vì khoảng cách giữa chúng lớn.</div>
<div><b>Không lực:</b> bỏ qua ${f(30)} khi chưa va chạm.</div>
<div><b>Thẳng:</b> giữa hai va chạm, phân tử chuyển động ${f(22)}</div>
<div><b>Nảy:</b> va chạm ${f(42)} với nhau và với thành bình.</div>
<div>Đập vào thành: ${m('v_x')} ${f(24)}, ${m('v_y')} ${f(24)}</div>
<div>Khí thực ở nhiệt độ, áp suất bình thường gần giống khí lí tưởng; nén mạnh hay làm lạnh sâu thì mô hình sai rõ.</div>
</div>
${H.vaThanh()}</div>
${h3(2, 'II.5 · Lượng chất, mol, số Avogadro', '3·2')}
<div class="card fig-side" style="${fs(40)};padding:1.2mm 3mm"><div>
<div>Mol là lượng chất chứa ${f(14)} phân tử; số Avogadro ${NA} (cho sẵn).</div>
<div>Khối lượng mol ${m('M')}: khối lượng của ${f(12)}, đơn vị ${f(12)}</div>
<div>Ở ${dktc}, 1 mol khí nào cũng chiếm ${f(16)}</div>
<div style="display:flex;gap:6mm;align-items:flex-end;margin:1mm 0;min-height:11mm"><span>${m('n=')} <span class="fill" style="min-width:16mm;height:10mm"></span> ${m('=')} <span class="fill" style="min-width:16mm;height:10mm"></span></span><span>Khí ở đktc: ${m('n=')} <span class="fill" style="min-width:16mm;height:10mm"></span></span></div>
<table class="tbl-ct"><tr><th>Kí hiệu</th><th>${m('n')}</th><th>${m('m')}</th><th>${m('M')}</th><th>${m('V')} (đktc)</th></tr>
<tr><td>Đơn vị</td><td></td><td></td><td></td><td></td></tr></table><div style="font-size:var(--fs-sm)">${m('N')}: số phân tử, không có đơn vị.</div></div>
${H.thung1mol()}</div>
${h3(3, 'Làm nhanh', '3·3')}
${box(cau(`<b>a)</b> Ở đktc, ${L('44{,}8')} khí ${CO2} chứa bao nhiêu phân tử?`, 2)
 + cau(`<b>b)</b> Bình chứa 2 mol khí helium (He, ${gmol('4')}) ở đktc. Khối lượng và thể tích lượng khí đó?`, 2)
 + cau(`<b>c)</b> Bình A chứa 1 mol ${N2} (${gmol('28')}), bình B chứa 1 mol ${CO2} (${gmol('44')}), cùng ở đktc. So sánh thể tích và khối lượng khí hai bình.`, 2))}
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('BA CÁI BẪY · TRẢ BÀI · TỰ KIỂM TRA')}
${h3(1, 'III · Ba cái bẫy hay sập', '4·1')}
<div class="card fig-side" style="${fs(40)};padding:1mm 3mm"><div>
<div class="trap">${ck}<span><b>“Phân tử bay vài trăm m/s thì mùi phải lan tức thì.”</b> Lẫn tốc độ một phân tử với tốc độ lan của cả đám: phân tử bay nhanh nhưng va chạm liên tục, đường đi gấp khúc; cả đám chỉ lan cỡ 0,1 cm/s trong ống kín.</span></div>
<div class="trap">${ck}<span><b>“Khí lí tưởng: phân tử không có kích thước, không có lực.”</b> Mô hình <i>bỏ qua</i> hai thứ đó vì chúng không đáng kể khi khí loãng, chứ phân tử thật vẫn có cả hai.</span></div>
<div class="trap">${ck}<span><b>“1 mol khí nào cũng nặng 22,4 g.”</b> 22,4 lít là thể tích mol ở đktc, giống nhau cho mọi khí; khối lượng mol khác nhau: ${N2} 28 · ${O2} 32 · ${CO2} 44 g/mol.</span></div></div>
${H.gapKhuc()}</div>
${h3(2, 'IV · Trả bài 6 câu', '4·2')}
${box(`${tb('1. Chuyển động Brown là gì? Nó chứng tỏ điều gì?')}${lines(2)}
${tb('2. Ba nội dung của thuyết động học phân tử chất khí?')}${lines(2)}
${tb('3. Vì sao lực liên kết giữa các phân tử khí rất yếu?')}${lines(1)}
${tb('4. Áp suất khí lên thành bình sinh ra từ đâu?')}${lines(1)}
${tb('5. Mô hình khí lí tưởng gồm gì? Khi nào dùng được?')}${lines(2)}
${tb('6. Mol là gì? Hệ thức lượng chất, tên và đơn vị từng kí hiệu? Thể tích mol ở đktc?')}${lines(4)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/6 câu · chưa thuộc: ${f(25)} ${nw(`→ đọc lại ô ${f(12)} Tập`)}</div>
${h3(3, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '4·3')}
${rkHai([1, 2, 3, 4], [5, 6, 7])}
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TOÁN MẪU · BÀI TẬP VỀ NHÀ · THỬ THÁCH')}
${h3(1, 'V · Bài toán mẫu: túi khí an toàn trên ô tô', '5·1')}
<div class="card soft" style="padding:1.2mm 3mm">Túi khí ô tô ở ${dktc} chứa ${g('84')} ${N2} (${gmol('28')}); ${NA}.<br><b>a)</b> số mol khí trong túi<br><b>b)</b> số phân tử ${N2}<br><b>c)</b> thể tích túi<br><b>d)</b> túi ${CO2} (${gmol('44')}) cùng thể tích, điều kiện: khối lượng khí? Vì sao khác?</div>
<table><tr><th style="width:44mm">Câu trong đề</th><th style="width:40mm">Dữ liệu</th><th>Kiến thức liên quan</th></tr>
<tr><td>“ở đktc”</td><td>0 °C · 1 atm</td><td>thể tích mol 22,4 lít</td></tr>
<tr><td style="height:6.5mm">“84 g ${N2}, M = 28 g/mol”</td><td></td><td><span class="hint">ghi dạng ${m('n=m:M')}</span></td></tr>
<tr><td style="height:6.5mm">“túi ${CO2} cùng thể tích”</td><td></td><td></td></tr>
</table>
<div class="fig-side" style="${fs(34)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl(`a) ${m('n=')}`, 1)}${wl(`b) ${m('N=')}`, 1)}${wl(`c) ${m('V=')}`, 1)}${wl(`d) ${m("n'=")}, ${m("m'=")}`, 1)}${wl('Vì sao khác:', 1)}</div>${H.tuiKhi()}</div>
${h3(2, 'Điền bước còn thiếu: túi oxygen y tế', '5·2')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div style="padding-top:.8mm;line-height:1.35">Túi ${nw(m('0{,}32\\ \\mathrm{kg}'))} ${O2} (${gmol('32')}), đktc. <b>Bước 1 (cho sẵn):</b> ${nw(m('m=320\\ \\mathrm g'))}, ${nw(m('n=320:32=10'))} mol</div>
${wl(`Bước 2: số phân tử ${m('N=')}`, 1)}${wl(`Bước 3: thể tích túi ${m('V=')}`, 1)}</div>
${K.btvn().replace('<i>1</i>', '<i>3</i>')}
${h3(4, 'Thử thách phân tầng', '5·4')}
${box(`<div style="padding-top:.4mm">${m('\\bigstar')} Bình chứa 0,5 mol khí. Số phân tử trong bình? ${f(34)}</div>`
 + cau(`${m('\\bigstar\\bigstar')} Vì sao vòng khói trắng trong ống khuếch tán (ô 2·2) luôn hiện gần đầu HCl hơn?`, 1)
 + cau(`${m('\\bigstar\\bigstar\\bigstar')} ${nw(m('1\\ \\mathrm{cm^3}'))} khí ở đktc chứa bao nhiêu phân tử? Vì sao hạt khói nhỏ “nhảy múa” dữ dội?`, 2))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Đối chiếu phát biểu với thuyết động học phân tử',
    de: `Nhìn qua kính lúp, hạt khói trong hộp kín đi theo đường gấp khúc, không dừng. Bốn phát biểu:<br>(1) Hạt khói bị phân tử khí va đập không cân bằng từ mọi phía nên bị đẩy lệch liên tục.<br>(2) Chuyển động của hạt khói chứng tỏ phân tử khí chuyển động hỗn loạn, không ngừng.<br>(3) Áp suất khí lên thành hộp là do trọng lượng của khí đè xuống đáy hộp.<br>(4) Nhiệt độ khí càng cao thì phân tử khí chuyển động càng chậm.<br><b>a)</b> có bao nhiêu phát biểu đúng &nbsp;<b>b)</b> số các phát biểu sai; sửa lại ở phần giải`,
    nd: `Xét cả lí do nêu trong từng phát biểu; áp suất khí do ${f(24)} của phân tử vào thành`, a: ['a', 'b'], gi: 2, cot: 2 },
  { t: 'Dạng 2 · Dễ · Từ khối lượng khí tính số mol và số phân tử',
    de: `Bình kín chứa ${nw(m('0{,}16\\ \\mathrm{kg}'))} khí oxygen ${O2}, ${gmol('32')}; ${NA}.<br><b>a)</b> số mol khí trong bình &nbsp;<b>b)</b> số phân tử oxygen trong bình`,
    nd: `${m('M')} tính bằng g/mol nên đổi ${m('m')} ra ${f(10)} trước; ${nw(`${m('N=')} ${f(14)}`)}`, a: ['a', 'b'], gi: 2, cot: 2 },
  { t: 'Dạng 3 · Trung bình · Từ số phân tử tính khối lượng, thể tích ở đktc',
    de: `Bình kín chứa ${pt('1{,}505', '23')} nguyên tử helium ở ${dktc}; ${gmol('4')}; ${NA}.<br><b>a)</b> số mol helium &nbsp;<b>b)</b> khối lượng helium &nbsp;<b>c)</b> thể tích bình, theo lít<br><b>d)</b> bình cùng thể tích, cùng điều kiện đựng ${H2} (${gmol('2')}): khối lượng ${m("m'")}, số phân tử ${m("N'")}`,
    nd: `Mọi đại lượng đi qua ${f(14)}; cùng ${m('V')}, cùng điều kiện ⇒ cùng ${f(14)}`, a: ['a', 'b', 'c', 'd<sub>1</sub>', 'd<sub>2</sub>'], gi: 6, cot: 5, fig: H.haiBinhD3() },
];
const dang2 = [
  { t: 'Dạng 4 · Khó · Chuỗi nhiều khâu: thể tích, khối lượng riêng, khối lượng, số mol, số phân tử',
    de: `Giọt nước hình cầu đường kính ${nw(m('4{,}0\\ \\mathrm{mm}'))}. Nước có ${nw(m('\\rho=1{,}0\\ \\mathrm{g/cm^3}'))}, ${gmol('18')}; ${NA}; thể tích hình cầu ${nw(m('V=\\dfrac{\\pi d^3}{6}'))}.<br><b>a)</b> thể tích giọt nước, theo ${m('\\mathrm{cm^3}')} &nbsp;<b>b)</b> khối lượng giọt &nbsp;<b>c)</b> số mol nước &nbsp;<b>d)</b> số phân tử nước`,
    nd: `Đổi ${m('d')} ra ${f(10)} trước; nước là chất lỏng nên ${f(30)} dùng 22,4 lít`, a: ['a', 'b', 'c', 'd'], gi: 6, cot: 2, fig: H.giotD4() },
  { t: 'Dạng 5 · Nâng cao · Khoảng cách giữa các phân tử khí so với kích thước phân tử',
    de: `Khí nitrogen ở đktc, thể tích mol ${nw(m('22{,}4\\ \\mathrm L'))}; ${NA}. Coi mỗi phân tử ở tâm một hình lập phương nhỏ; các hình xếp khít, lấp đầy thể tích khí. Đường kính phân tử ${N2} cỡ ${nw(m('D=3{,}0\\cdot10^{-10}\\ \\mathrm m'))}.<br><b>a)</b> thể tích mỗi hình lập phương, theo ${m('\\mathrm{m^3}')}<br><b>b)</b> cạnh ${m('d')} của hình lập phương (coi là khoảng cách giữa hai phân tử kề nhau)<br><b>c)</b> ${m('d')} gấp bao nhiêu lần ${m('D')}; khớp với nội dung nào của thuyết`,
    nd: `Đổi ${nw(m('1\\ \\mathrm L='))} ${f(14)}; ${nw(`${m('V_1=')} ${f(16)}`)}; ${nw(`${m('d=')} ${f(14)}`)}`, a: ['a', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'], gi: 6, cot: 2, fig: H.lapPhuongD5() },
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
    { t: 'Dạng 1 · Bài 1', de: `Quả bóng bay buộc kín, nhúng vào chậu nước nóng thì căng lên. Bốn phát biểu:<br>(1) Phân tử khí trong bóng chuyển động nhanh hơn.<br>(2) Phân tử va vào vỏ bóng mạnh hơn nên áp suất tăng.<br>(3) Từng phân tử nở to ra nên bóng căng.<br>(4) Số phân tử khí trong bóng tăng lên.<br><b>a)</b> có bao nhiêu phát biểu đúng<br><b>b)</b> số các phát biểu sai (sửa trong vở)`, fig: H.bongTT(), fw: 28, o: ['a', 'b'], ow: { a: 14, b: 22 } },
    { t: 'Dạng 1 · Bài 2', de: `Bốn phát biểu về mô hình khí lí tưởng. (1) Coi mỗi phân tử là một chất điểm.<br>(2) Khí thực bị nén rất mạnh vẫn giống hệt khí lí tưởng.<br>(3) Khi chưa va chạm, các phân tử hút nhau mạnh.<br>(4) Va chạm với thành bình làm phân tử mất bớt động năng.<br><b>a)</b> có bao nhiêu phát biểu đúng<br><b>b)</b> số các phát biểu sai (sửa trong vở)`, o: ['a', 'b'], ow: { a: 14, b: 26 } },
    { t: 'Dạng 2 · Bài 1', de: `Bình chứa ${nw(m('0{,}56\\ \\mathrm{kg}'))} khí ${N2}, ${gmol('28')}; ${NA}.<br><b>a)</b> số mol khí trong bình<br><b>b)</b> số phân tử ${N2} trong bình`, o: ['a', 'b'] },
    { t: 'Dạng 2 · Bài 2', de: `Bình chứa ${g('8{,}8')} khí ${CO2}, ${gmol('44')}; ${NA}.<br><b>a)</b> số mol khí trong bình<br><b>b)</b> số phân tử ${CO2} trong bình`, o: ['a', 'b'] },
    { t: 'Dạng 3 · Bài 1', de: `Bình kín chứa ${pt('3{,}01', '23')} phân tử ${O2} ở đktc; ${gmol('32')}; ${NA}.<br><b>a)</b> số mol khí<br><b>b)</b> khối lượng khí<br><b>c)</b> thể tích bình, theo lít<br><b>d)</b> bình ${N2} (${gmol('28')}) cùng ${m('V')}, điều kiện: ${m('m')}, ${m('N')}`, o: ['a', 'b', 'c', 'd<sub>1</sub>', 'd<sub>2</sub>'], ow: { 'd<sub>1</sub>': 16, 'd<sub>2</sub>': 24 } },
    { t: 'Dạng 3 · Bài 2', de: `Bình kín chứa ${pt('9{,}03', '22')} phân tử ${CO2} ở đktc; ${gmol('44')}; ${NA}.<br><b>a)</b> số mol khí<br><b>b)</b> khối lượng khí<br><b>c)</b> thể tích bình, theo lít<br><b>d)</b> bình helium (${gmol('4')}) cùng thể tích, điều kiện: khối lượng`, o: ['a', 'b', 'c', 'd'] },
  ], [
    { t: 'Dạng 4 · Bài 1', de: `Giọt nước hình cầu đường kính ${nw(m('2{,}0\\ \\mathrm{mm}'))}; ${nw(m('\\rho=1{,}0\\ \\mathrm{g/cm^3}'))}, ${gmol('18')}; ${NA}; ${nw(m('V=\\dfrac{\\pi d^3}{6}'))}.<br><b>a)</b> thể tích giọt, theo ${m('\\mathrm{cm^3}')}<br><b>b)</b> khối lượng giọt<br><b>c)</b> số mol nước<br><b>d)</b> số phân tử nước`, o: ['a', 'b', 'c', 'd'], ow: 30 },
    { t: 'Dạng 4 · Bài 2', de: `Khối nhôm lập phương cạnh ${nw(m('1{,}0\\ \\mathrm{cm}'))}; nhôm có ${nw(m('\\rho=2{,}7\\ \\mathrm{g/cm^3}'))}, ${gmol('27')}; ${NA}.<br><b>a)</b> thể tích khối, theo ${m('\\mathrm{cm^3}')}<br><b>b)</b> khối lượng khối<br><b>c)</b> số mol nhôm<br><b>d)</b> số nguyên tử nhôm`, fig: H.khoiNhomTT(), fw: 30, o: ['a', 'b', 'c', 'd'], ow: 30 },
    { t: 'Dạng 5 · Bài 1', de: `Nước lỏng: 1 mol nước chiếm ${nw(m('18\\ \\mathrm{cm^3}'))}; ${NA}. Coi mỗi phân tử nước ở tâm một hình lập phương nhỏ xếp khít; đường kính phân tử nước cỡ ${nw(m('3{,}0\\cdot10^{-10}\\ \\mathrm m'))}.<br><b>a)</b> thể tích mỗi hình lập phương, theo ${m('\\mathrm{m^3}')}<br><b>b)</b> cạnh ${m('d')} của hình lập phương<br><b>c)</b> ${m('d')} gấp bao nhiêu lần đường kính phân tử (so với khí ở Dạng 5, Tập 7·1)`, o: ['a', 'b', 'c'], ow: 30 },
    { t: 'Dạng 5 · Bài 2', de: `Khí nitrogen ở 0 °C nhưng áp suất chỉ 0,10 atm: thể tích mol là ${nw(m('224\\ \\mathrm L'))} (cho sẵn); ${NA}; đường kính phân tử ${nw(m('D=3{,}0\\cdot10^{-10}\\ \\mathrm m'))}. Coi mỗi phân tử ở tâm một hình lập phương xếp khít.<br><b>a)</b> thể tích mỗi hình lập phương, theo ${m('\\mathrm{m^3}')}<br><b>b)</b> cạnh ${m('d')}<br><b>c)</b> ${m('d')} gấp bao nhiêu lần ${m('D')}`, o: ['a', 'b', 'c'], ow: 30 },
    nhap(3),
  ]],
  dap: [
    `D1·1: a) 2 · b) (3), (4) &nbsp;|&nbsp; D1·2: a) 1 · b) (2), (3), (4) &nbsp;|&nbsp; D2·1: a) 20 mol · b) 1,204·10<sup>25</sup> &nbsp;|&nbsp; D2·2: a) 0,20 mol · b) 1,204·10<sup>23</sup> &nbsp;|&nbsp; D3·1: a) 0,50 mol · b) 16 g · c) 11,2 lít · d<sub>1</sub>) 14 g · d<sub>2</sub>) 3,01·10<sup>23</sup> &nbsp;|&nbsp; D3·2: a) 0,15 mol · b) 6,6 g · c) 3,36 lít · d) 0,60 g`,
    `D4·1: a) 4,19·10<sup>−3</sup> cm³ · b) 4,19·10<sup>−3</sup> g · c) 2,33·10<sup>−4</sup> mol · d) 1,40·10<sup>20</sup> &nbsp;|&nbsp; D4·2: a) 1,0 cm³ · b) 2,7 g · c) 0,10 mol · d) 6,02·10<sup>22</sup> &nbsp;|&nbsp; D5·1: a) 2,99·10<sup>−29</sup> m³ · b) 3,1·10<sup>−10</sup> m · c) ≈ 1 lần (nước lỏng: phân tử xếp sát nhau; khí ở đktc: cách nhau cỡ 11 lần) &nbsp;|&nbsp; D5·2: a) 3,72·10<sup>−25</sup> m³ · b) 7,19·10<sup>−9</sup> m · c) ≈ 24 lần`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang: [...dang, ...dang2], tach: [3, 2], kq: [[1, 2, 3], [4, 5]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'Brown 1·4 · Nhỏ – Loạn – Đập 2·1 · ống khói trắng 2·2 · khí lí tưởng 3·1 · mol, N<sub>A</sub>, 22,4 lít 3·2 · bẫy 4·1 · bài toán mẫu 5·1 · dạng 1–3 → 6·1 · dạng 4–5 → 7·1',
  out: process.argv[2],
});
