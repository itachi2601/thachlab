// Ruột tập VL12 – Bài 8 · Áp suất – động năng của phân tử khí (lesson id 9). Quyển Chương 2 lớp 12: bài 5–8, bài 8 = tr. 37–48.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l12-bai8.mjs (toàn bộ SVG tự vẽ). Nội dung theo bài web (book/cache/9.json, tải từ DB 12/11/2026): mục tiêu, dự đoán
// bóng bàn bẹp, II.1–II.5 (Nhỏ–Loạn–Đập–Nảy, một phân tử, N phân tử, Ed = 3/2 kT, bình kín p/T), hai bẫy, Trả bài 6 câu, bài toán mẫu
// bình N2, thử thách ⭐–⭐⭐⭐, 5 dạng bài tập mẫu. Đáp số Bài tương tự (tuongTu.dap) tính bằng Python 12/11/2026.
// Chạy: node scripts/ruot-tap/l12-bai8.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl12-bai8.pdf
//       node scripts/ruot-tap/l12-bai8.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l12-bai8/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL12b8 as H } from './hinh-l12-bai8.mjs';

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
  const out = resolve(HERE, 'out/hinh-l12-bai8'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 8, lid: 9, ten: 'ÁP SUẤT · ĐỘNG NĂNG CỦA PHÂN TỬ KHÍ', lop: 12, baiDau: 5, sub: 'Vật lí 12 · Chương 2: Khí lí tưởng' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const cao = (w = 26) => `<span class="fill" style="min-width:${w}mm;height:10mm"></span>`;   // ô cao cho phân số
const kB = nw(m('k=1{,}38\\cdot10^{-23}\\ \\mathrm{J/K}'));
const NA = nw(m('N_A=6{,}02\\cdot10^{23}\\ \\mathrm{mol^{-1}}'));
const RR = nw(m('R=8{,}31\\ \\mathrm{J/(mol{\\cdot}K)}'));
const Ed = m('\\overline{E_d}'), v2 = m('\\overline{v^2}'), mu = m('\\mu'), vr = m('v_{rms}');
const oC = (s) => nw(m(`${s}\\ ^\\circ\\mathrm C`));
const hs = `<div class="card soft" style="padding:.8mm 3mm;font-size:var(--fs-sm)"><b>Hằng số dùng trong bài:</b> ${kB} · ${NA} · ${RR} · ${nw(m('T=t+273'))}</div>`;

const ttCss = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';

const p1 = `${ttCss}<section class="page">
${head('BÀI 8 · ÁP SUẤT · ĐỘNG NĂNG CỦA PHÂN TỬ KHÍ', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Nêu mô hình động học phân tử; giải thích vì sao khí gây <b>áp suất</b> lên thành bình`)}
${dong(`${ck}Lập công thức áp suất do <b>một</b> và do <b>N</b> phân tử; dùng hằng số Boltzmann ${m('k')}`)}
${dong(`${ck}Tìm xem động năng phân tử phụ thuộc nhiệt độ thế nào; kiểm bằng thí nghiệm bình kín`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Quả bóng bàn bị giẫm bẹp, nhúng vào nước ${oC('80')} thì vỏ phồng lại. Khi khí trong bóng nóng lên, các phân tử khí đập vào mặt trong vỏ bóng thay đổi thế nào?</p>
<div class="fig-side" style="${fs(44)}"><div>
${opt('A', 'Đập mạnh hơn vì phân tử nóng lên thì nặng thêm')}
${opt('B', 'Bay nhanh hơn: mỗi cú đập truyền động lượng lớn hơn, lại đập dày hơn')}
${opt('C', 'Không đổi; hơi nước thấm qua vỏ làm số phân tử tăng')}
${opt('D', 'Không đổi; vỏ bóng gặp nóng mềm ra và tự phồng lại')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 2)}</div>
${H.bongBan()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(2)}</div>
${h3(4, 'II.1 · Mô hình khí lí tưởng nhìn từ thành bình', '1·4')}
<div class="card fig-side" style="${fs(42)};padding:1.2mm 3mm"><div>
<div><b>Nhỏ:</b> phân tử có kích thước ${f(22)} so với khoảng cách giữa chúng; bỏ qua lực ${f(22)} khi chưa va chạm.</div>
<div><b>Loạn:</b> chuyển động ${f(22)} không ngừng; giữa hai va chạm bay ${f(22)}.</div>
<div><b>Đập:</b> va vào thành, truyền ${f(22)} cho thành; vô số va chạm mỗi giây thành lực đẩy đều: ${f(22)} của khí.</div>
<div><b>Nảy:</b> va chạm hoàn toàn ${f(20)}: phân tử bật ngược, tốc độ ${f(20)}.</div>
<div style="margin-top:.6mm"><b>Hộp gạo lắc:</b> thêm hạt thì tiếng đập vào thành ${f(22)}; lắc nhanh hơn thì ${f(22)}.</div></div>
${H.hopKhi()}</div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('MỘT PHÂN TỬ · N PHÂN TỬ: CÔNG THỨC ÁP SUẤT')}
${h3(1, 'II.2 · Một phân tử va chạm vào thành bình', '2·1')}
<div class="card" style="padding:1.2mm 3mm"><div class="fig-side" style="${fs(42)}"><div>
<div>Bình lập phương cạnh ${m('l')}, ${nw(m('V=l^3'))}, ${nw(m('S=l^2'))}. Phân tử khối lượng ${m('m')} bay dọc ${m('Ox')} với tốc độ ${m('v')}, đập vuông góc vào thành rồi bật ngược.</div>
<div style="margin-top:.6mm">Động lượng trước: ${m('+mv')} · sau: ${f(16)}</div>
<div style="margin-top:.6mm">Độ lớn độ biến thiên: ${nw(`${m('|\\Delta p|=')} ${f(16)}`)}</div></div>
${H.vaCham()}</div>
<div style="margin-top:.6mm">Một vòng đi – về: ${m('\\Delta t=')} ${cao(18)} ⇒ mỗi giây có ${cao(18)} va chạm</div>
<div style="margin-top:.6mm">Lực trung bình ${m('F')} = (động lượng mỗi va chạm) × (số va chạm mỗi giây) ${m('=')} ${cao(24)}</div>
<div style="margin-top:.6mm">Áp suất do một phân tử: ${m('p_m=\\tfrac{F}{S}=')} ${cao(30)}</div></div>
${h3(2, 'II.3 · N phân tử: công thức áp suất của khí', '2·2')}
<div class="card" style="padding:1.2mm 3mm">
<div>Chỉ thành phần ${m('v_x')} ${f(22)} với thành mới gây áp suất lên thành đó. Ba phương ${f(18)} nên ${nw(`${m('\\overline{v_x^2}=')} ${f(12)} ${v2}`)}</div>
<div style="margin-top:.6mm">Trung bình của các bình phương tốc độ: ${m('\\overline{v^2}=')} ${cao(46)}</div>
<div style="margin-top:.6mm">${m('p=')} ${cao(30)} ${m('=\\dfrac13\\rho\\,\\overline{v^2}=')} ${cao(24)}</div>
<table style="margin-top:1mm"><tr><th style="width:20mm">Kí hiệu</th><th>Tên gọi</th><th style="width:30mm">Công thức / đơn vị</th></tr>
<tr><td>${mu}</td><td></td><td></td></tr><tr><td>${m('\\rho')}</td><td></td><td></td></tr><tr><td>${Ed}</td><td></td><td></td></tr></table>
</div>
${h3(3, 'Làm nhanh', '2·3')}
${box(cau(`<b>Câu 1.</b> Phân tử ${nw(m('m=4{,}65\\cdot10^{-26}\\ \\mathrm{kg}'))} bay vuông góc tới thành với ${nw(m('v=500\\ \\mathrm{m/s}'))}, bật ngược đàn hồi. Độ lớn độ biến thiên động lượng?`, 1)
 + cau(`<b>Câu 2.</b> Bình ${nw(m('2{,}0'))} lít chứa ${nw(m('6{,}02\\cdot10^{22}'))} phân tử ${nw(`N${m('_2')}`)}, mỗi phân tử ${nw(m('4{,}65\\cdot10^{-26}\\ \\mathrm{kg}'))}; ${nw(m('\\overline{v^2}=2{,}5\\cdot10^5\\ \\mathrm{m^2/s^2}'))}. Tính ${m('\\rho')} và ${m('p')}.`, 2))}
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('ĐỘNG NĂNG TỊNH TIẾN TRUNG BÌNH · NHIỆT ĐỘ TUYỆT ĐỐI')}
${hs}
${h3(1, 'II.4 · Động năng tịnh tiến trung bình và nhiệt độ', '3·1')}
<div class="card fig-side" style="${fs(42)};padding:1.2mm 3mm"><div>
<div>Ô 38·2: ${m('p=\\tfrac23\\mu\\overline{E_d}')}. Phương trình trạng thái: ${m('p=\\tfrac{nRT}{V}=\\tfrac{N}{V}\\cdot\\tfrac{R}{N_A}T=\\mu kT')}, với ${nw(`${m('k=')} ${f(14)}`)}</div>
<div style="margin-top:.6mm">So hai biểu thức: ${m('\\overline{E_d}=\\dfrac{m\\overline{v^2}}{2}=')} ${cao(24)}</div>
<div>Hệ số ${m('\\tfrac32')}: ba phương tịnh tiến, mỗi phương góp ${f(16)}</div>
<div>${Ed} chỉ phụ thuộc ${f(16)}; mọi khí cùng nhiệt độ có ${Ed} ${f(16)}</div>
<div style="margin-top:.6mm">${m('v_{rms}=\\sqrt{\\overline{v^2}}=')} ${cao(24)}</div>
<div>Cùng ${m('T')}: khí ${f(14)} hơn thì bay nhanh hơn.</div>
<div style="margin-top:.4mm">Hình bên: đường ứng nhiệt độ cao hơn là ${f(10)}, vì ${f(32)}</div></div>
${H.phanBo()}</div>
${h3(2, 'II.5 · Thí nghiệm: áp suất khí trong bình kín theo nhiệt độ', '3·2')}
<div class="fig-side" style="${fs(40)}"><div>
<table class="tbl-ct"><tr><th>${m('t')} (°C)</th><th>10</th><th>30</th><th>50</th><th>70</th><th>90</th></tr>
<tr><td>${m('T')} (K)</td><td>283</td><td>303</td><td>323</td><td>343</td><td></td></tr>
<tr><td>${m('p')} (kPa)</td><td>96,0</td><td>102,8</td><td>109,5</td><td>116,4</td><td>123,0</td></tr>
<tr><td>${m('p/T')} (kPa/K)</td><td>0,3392</td><td>0,3393</td><td>0,3390</td><td>0,3394</td><td></td></tr></table>
<div style="font-size:var(--fs-sm);color:var(--hint)">Số liệu minh hoạ, ${m('V')} và lượng khí không đổi.</div>
<div style="margin-top:.6mm"><b>Hiện tượng:</b> nước càng nóng, áp kế chỉ ${f(20)}</div>
<div><b>Kết luận:</b> ${m('p/T')} ${f(20)} ⇒ ${m('p')} tỉ lệ thuận với ${f(22)}</div>
<div><b>Cơ chế:</b> phân tử bay ${f(16)}, va chạm ${f(16)} và ${f(16)}</div>
<div><b>Giới hạn:</b> dụng cụ chỉ đo ${f(30)}; tốc độ, động năng phân tử là suy ra từ mô hình.</div>
<div><b>Sai số:</b> đọc ${m('p')} khi khí chưa kịp nóng bằng nước thì ${m('p/T')} đo được ${f(16)} giá trị thật.</div></div>
${H.binhKin()}</div>
${h3(3, 'Làm nhanh', '3·3')}
${box(cau(`Đồ thị ${Ed} theo ${m('T')} (kelvin) có dạng ${f(30)}. Ở nhiệt độ nào (°C) thì ${nw(m('\\overline{E_d}=4{,}14\\cdot10^{-21}\\ \\mathrm J'))}?`, 1))}
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('HAI CÁI BẪY · TRẢ BÀI · TỰ KIỂM TRA')}
${h3(1, 'III · Hai cái bẫy hay sập', '4·1')}
<div class="card fig-side" style="${fs(38)};padding:1mm 3mm"><div>
<div class="trap">${ck}<span><b>“Nhiệt độ gấp đôi thì động năng gấp đôi.”</b> Trong ${m('\\overline{E_d}=\\tfrac32kT')}, ${m('T')} là nhiệt độ tuyệt đối. ${oC('20')} lên ${oC('40')}: ${nw(`${m('T_1=')} ${f(12)}`)}, ${nw(`${m('T_2=')} ${f(12)}`)} ⇒ ${Ed} tăng ${f(12)} lần.</span></div>
<div class="trap">${ck}<span><b>“Phân tử nặng hơn thì động năng trung bình lớn hơn.”</b> Cùng ${nw(m('300\\ \\mathrm K'))}: ${Ed} của ${nw(`H${m('_2')}`)} ${f(14)} của ${nw(`O${m('_2')}`)}. ${nw(`O${m('_2')}`)} nặng gấp 16 lần ${nw(`H${m('_2')}`)} nên ${vr} của ${nw(`H${m('_2')}`)} gấp ${f(10)} lần của ${nw(`O${m('_2')}`)}.</span></div></div>
${H.thang()}</div>
${h3(2, 'IV · Trả bài 6 câu', '4·2')}
${box(`${tb('1. Mô hình động học phân tử nói gì; vì sao khí có áp suất?')}${lines(2)}
${tb(`2. Vì sao va chạm vuông góc với thành cho ${m('|\\Delta p|=2mv')}?`)}${lines(2)}
${tb('3. Công thức áp suất do một và do N phân tử; tên, đơn vị kí hiệu.')}${lines(3)}
${tb('4. Động năng tịnh tiến trung bình liên hệ nhiệt độ thế nào? k = ?')}${lines(2)}
${tb(`5. Cùng nhiệt độ, ${nw(`H${m('_2')}`)} và ${nw(`O${m('_2')}`)} khác nhau thế nào về động năng, tốc độ?`)}${lines(2)}
${tb('6. Vì sao công thức động năng bắt buộc dùng kelvin?')}${lines(2)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/6 câu · chưa thuộc: ${f(25)} ${nw(`→ đọc lại ô ${f(12)} Tập`)}</div>
${h3(3, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '4·3')}
${rkHai([1, 2, 3, 4], [5, 6, 7, 8])}
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TOÁN MẪU · BÀI TẬP VỀ NHÀ · THỬ THÁCH')}
${h3(1, 'V · Bài toán mẫu: bình khí nitơ', '5·1')}
<div class="card soft" style="padding:1.2mm 3mm">Bình kín ${nw(m('V=3{,}0'))} lít chứa ${nw(m('n=0{,}20'))} mol khí nitơ ở ${oC('27')}; ${nw(m('M=28\\ \\mathrm{g/mol}'))}. Dùng ${m('k')}, ${m('N_A')}, ${m('R')} in sẵn ở đầu trang 39.
<b>a)</b> ${mu} và ${Ed} &nbsp;<b>b)</b> ${vr} &nbsp;<b>c)</b> ${m('p')} theo hai cách &nbsp;<b>d)</b> nung lên ${oC('87')} (${m('V')} không đổi): ${m('p')} và ${Ed} tăng mấy lần?</div>
<table><tr><th style="width:40mm">Câu trong đề</th><th style="width:40mm">Dữ liệu</th><th>Kiến thức</th></tr>
<tr><td>“3,0 lít”</td><td>${m('V=3{,}0\\cdot10^{-3}\\ \\mathrm{m^3}')}</td><td>đổi lít ra m³</td></tr>
<tr><td style="height:6.5mm">“0,20 mol”</td><td></td><td></td></tr>
<tr><td style="height:6.5mm">“27 °C”, “M = 28 g/mol”</td><td></td><td></td></tr>
</table>
<div class="fig-side" style="${fs(40)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl(`a) ${m('\\mu=')}`, 2)}${wl(`b) ${m('m=M/N_A=')}`, 2)}${wl(`c) ${m('p=\\tfrac23\\mu\\overline{E_d}=')}`, 1)}${wl(`&nbsp;&nbsp;&nbsp; ${m('p=nRT/V=')}`, 1)}${wl('d)', 1)}</div>${H.binhN2()}</div>
${h3(2, 'Điền bước còn thiếu: thay nitơ bằng 0,20 mol heli (M = 4 g/mol), 27 °C', '5·2')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div class="ln"><b>Bước 1 (cho sẵn):</b> ${nw(m('\\overline{E_d}\\approx6{,}2\\cdot10^{-21}\\ \\mathrm J'))} như nitơ, vì chỉ phụ thuộc nhiệt độ.</div>
${wl(`Bước 2: ${m('m_{He}=')}`, 1)}${wl(`Bước 3: ${m('v_{rms}=')} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;; so với ${nw(`N${m('_2')}`)}:`, 1)}</div>
${K.btvn().replace('<i>1</i>', '<i>3</i>')}
${h3(4, 'Thử thách phân tầng', '5·4')}
${box(wl(`${m('\\bigstar')} ${Ed} ở ${oC('0')} và ở ${oC('27')}; tăng mấy lần?`, 1)
 + cau(`${m('\\bigstar\\bigstar')} Cùng nhiệt độ, ${nw(`H${m('_2')}`)} nhanh hơn ${nw(`O${m('_2')}`)} 4 lần mà áp suất hai bình (cùng ${m('N')}, ${m('V')}) vẫn bằng nhau. Vì sao?`, 1)
 + cau(`${m('\\bigstar\\bigstar\\bigstar')} Bình kín giữ nguyên nhiệt độ, hút bớt một nửa số phân tử. Áp suất đổi thế nào? Giải bằng hai cách.`, 1))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Động năng tịnh tiến trung bình ở một nhiệt độ',
    de: `Trong phòng sấy, khí ${nw(`H${m('_2')}`)} và khí ${nw(`O${m('_2')}`)} trộn lẫn trong một bình kín, cùng ở ${oC('47')} (${kB}).<br><b>a)</b> động năng tịnh tiến trung bình của một phân tử ${nw(`H${m('_2')}`)}<br><b>b)</b> ${Ed} của phân tử ${nw(`O${m('_2')}`)} lớn hơn, nhỏ hơn hay bằng của ${nw(`H${m('_2')}`)}; vì sao`,
    nd: `Đổi sang ${f(12)} trước; ${nw(`${m('\\overline{E_d}=')} ${f(14)}`)} không chứa ${f(18)} phân tử`, a: ['a', 'b'], cot: 2, gi: 4, fig: H.honHop() },
  { t: 'Dạng 2 · Trung bình · Đổi nhiệt độ: E<sub>d</sub>, v<sub>rms</sub>, p tăng mấy lần',
    de: `Khí heli trong bình kín (thể tích, lượng khí không đổi) được hơ nóng từ ${oC('27')} lên ${oC('147')}. Làm tròn tỉ số đến hai chữ số thập phân.<br><b>a)</b> ${Ed} tăng bao nhiêu lần<br><b>b)</b> ${vr} tăng bao nhiêu lần<br><b>c)</b> áp suất tăng bao nhiêu lần`,
    nd: `Lấy tỉ số ${f(12)} (kelvin); ${Ed} và ${m('p')} tỉ lệ ${f(10)}; ${vr} tỉ lệ ${f(12)}`, a: ['a', 'b', 'c'], gi: 3 },
  { t: 'Dạng 3 · Trung bình · Áp suất từ khối lượng riêng và v<sub>rms</sub>',
    de: `Bình kín chứa khí neon có khối lượng riêng ${nw(m('0{,}90\\ \\mathrm{kg/m^3}'))}; ${nw(m('v_{rms}=600\\ \\mathrm{m/s}'))}.<br><b>a)</b> áp suất khí trong bình<br><b>b)</b> nung nóng (thể tích, lượng khí không đổi) đến khi ${nw(m('v_{rms}=900\\ \\mathrm{m/s}'))}: áp suất khi đó`,
    nd: `${nw(`${m('p=')} ${f(16)}`)}; phải ${f(18)} ${vr} trước khi thay; ${m('\\rho')} ${f(14)} vì ${m('V')} và lượng khí giữ nguyên`, a: ['a', 'b'], cot: 2, gi: 3 },
  { t: 'Dạng 4 · Khá · Tốc độ căn quân phương từ nhiệt độ và khối lượng mol',
    de: `Bình kín chứa khí argon (${nw(m('M=40\\ \\mathrm{g/mol}'))}) ở ${oC('77')}; ${NA}, ${kB}.<br><b>a)</b> khối lượng một phân tử argon<br><b>b)</b> ${Ed} và ${vr} của phân tử argon<br><b>c)</b> thay bằng heli (${nw(m('M=4\\ \\mathrm{g/mol}'))}) cùng nhiệt độ: ${vr} của heli gấp mấy lần của argon`,
    nd: `${nw(`${m('m=')} ${f(14)}`)} (đổi ${m('M')} ra ${f(14)}); ${nw(`${m('v_{rms}=')} ${f(20)}`)}; cùng ${m('T')} thì ${m('\\dfrac{v_1}{v_2}=')} ${f(16)}`, a: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], cot: 2, gi: 6 },
  { t: 'Dạng 5 · Khó · Bài ngược: từ áp suất và mật độ tìm nhiệt độ, rồi đổi trạng thái',
    de: `Bình kín chứa khí heli có mật độ phân tử ${nw(m('\\mu=2{,}4\\cdot10^{25}\\ \\mathrm{m^{-3}}'))}, áp suất ${nw(m('1{,}0\\cdot10^{5}\\ \\mathrm{Pa}'))}; ${kB}.<br><b>a)</b> ${Ed} của một phân tử heli<br><b>b)</b> nhiệt độ tuyệt đối của khí<br><b>c)</b> hút bớt khí cho số phân tử còn một nửa, rồi nung đến ${oC('117')} (vẫn bình đó): áp suất lúc này`,
    nd: `Chưa có ${m('T')} ⇒ đi từ ${nw(`${m('p=')} ${f(16)}`)} tìm ${Ed} trước; sau đó ${nw(`${m('p=')} ${f(12)}`)} với ${mu} và ${m('T')} mới`, a: ['a', 'b', 'c'], gi: 6, fig: H.truocSau() },
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
const W = 32;   // ô đáp số có số mũ: 32 mm
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–3', 'DẠNG 4–5'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Khí ${nw(`CO${m('_2')}`)} và khí ${nw(`N${m('_2')}`)} trộn trong một bình kín ở ${oC('127')}; ${kB}.<br><b>a)</b> ${Ed} của một phân tử ${nw(`CO${m('_2')}`)}<br><b>b)</b> ${Ed} của phân tử ${nw(`N${m('_2')}`)} so với ${nw(`CO${m('_2')}`)}<br><b>c)</b> ở bao nhiêu °C thì ${Ed} của khí bằng ${nw(m('6{,}21\\cdot10^{-21}\\ \\mathrm J'))}`, o: ['a', 'b', 'c'], ow: { a: W, b: 22, c: 18 } },
    { t: 'Dạng 1 · Bài 2', de: `Không khí trong kho lạnh ở ${oC('-23')}; ${kB}.<br><b>a)</b> ${Ed} của một phân tử khí<br><b>b)</b> phải tăng lên bao nhiêu °C thì ${Ed} gấp đôi`, o: ['a', 'b'], ow: { a: W, b: 18 } },
    { t: 'Dạng 2 · Bài 1', de: `Khí oxygen trong bình kín (thể tích, lượng khí không đổi) được nung từ ${oC('7')} lên ${oC('287')}. Làm tròn tỉ số đến hai chữ số thập phân.<br><b>a)</b> ${Ed} tăng bao nhiêu lần<br><b>b)</b> ${vr} tăng bao nhiêu lần<br><b>c)</b> áp suất tăng bao nhiêu lần`, o: ['a', 'b', 'c'], ow: 16 },
    { t: 'Dạng 2 · Bài 2', de: `Khí trong bình kín (thể tích, lượng khí không đổi) được làm lạnh từ ${oC('127')} xuống ${oC('-73')}. Làm tròn tỉ số đến hai chữ số thập phân.<br><b>a)</b> ${Ed} mới bằng bao nhiêu lần ${Ed} cũ<br><b>b)</b> ${vr} mới bằng bao nhiêu lần ${vr} cũ<br><b>c)</b> áp suất mới bằng bao nhiêu lần áp suất cũ`, o: ['a', 'b', 'c'], ow: 16 },
    { t: 'Dạng 3 · Bài 1', de: `Khí nitơ trong bình kín có khối lượng riêng ${nw(m('1{,}2\\ \\mathrm{kg/m^3}'))}, ${nw(m('v_{rms}=500\\ \\mathrm{m/s}'))}.<br><b>a)</b> áp suất khí<br><b>b)</b> nung nóng (thể tích, lượng khí không đổi) đến ${nw(m('v_{rms}=600\\ \\mathrm{m/s}'))}: áp suất khi đó`, o: ['a', 'b'], ow: W },
    { t: 'Dạng 3 · Bài 2', de: `Một khối khí có áp suất ${nw(m('1{,}5\\cdot10^5\\ \\mathrm{Pa}'))}, ${nw(m('v_{rms}=700\\ \\mathrm{m/s}'))}.<br><b>a)</b> khối lượng riêng của khí<br><b>b)</b> giữ thể tích, lượng khí; nung đến khi áp suất gấp 4 lần: ${vr} khi đó`, o: ['a', 'b'], ow: W },
    nhap(3),
  ], [
    { t: 'Dạng 4 · Bài 1', de: `Bình kín chứa khí nitơ (${nw(m('M=28\\ \\mathrm{g/mol}'))}) ở ${oC('27')}; ${NA}, ${kB}.<br><b>a)</b> khối lượng một phân tử nitơ<br><b>b)</b> ${Ed} và ${vr} của phân tử nitơ<br><b>c)</b> thay bằng hydrogen (${nw(m('M=2\\ \\mathrm{g/mol}'))}) cùng nhiệt độ: ${vr} của ${nw(`H${m('_2')}`)} gấp mấy lần của ${nw(`N${m('_2')}`)}`, o: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], ow: { a: W, 'b<sub>1</sub>': W, 'b<sub>2</sub>': 22, c: 16 } },
    { t: 'Dạng 4 · Bài 2', de: `Bình kín chứa khí oxygen (${nw(m('M=32\\ \\mathrm{g/mol}'))}) ở ${oC('127')}; ${NA}, ${kB}.<br><b>a)</b> khối lượng một phân tử oxygen<br><b>b)</b> ${Ed} và ${vr} của phân tử oxygen<br><b>c)</b> nung đến bao nhiêu °C thì ${vr} gấp đôi`, o: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], ow: { a: W, 'b<sub>1</sub>': W, 'b<sub>2</sub>': 22, c: 18 } },
    { t: 'Dạng 5 · Bài 1', de: `Bình kín chứa khí heli có mật độ phân tử ${nw(m('3{,}0\\cdot10^{25}\\ \\mathrm{m^{-3}}'))}, áp suất ${nw(m('1{,}2\\cdot10^{5}\\ \\mathrm{Pa}'))}; ${kB}.<br><b>a)</b> ${Ed} của một phân tử heli<br><b>b)</b> nhiệt độ tuyệt đối của khí<br><b>c)</b> bơm thêm heli cho số phân tử tăng 1,5 lần, rồi nung đến ${oC('87')} (vẫn bình đó): áp suất lúc này`, o: ['a', 'b', 'c'], ow: { a: W, b: 18, c: W } },
    { t: 'Dạng 5 · Bài 2', de: `Bình kín chứa khí neon có mật độ phân tử ${nw(m('2{,}0\\cdot10^{25}\\ \\mathrm{m^{-3}}'))}, áp suất ${nw(m('9{,}0\\cdot10^{4}\\ \\mathrm{Pa}'))}; ${kB}.<br><b>a)</b> ${Ed} của một phân tử neon<br><b>b)</b> nhiệt độ tuyệt đối của khí<br><b>c)</b> hút bớt khí cho số phân tử còn một phần ba, rồi làm nguội đến ${oC('7')}: áp suất lúc này`, o: ['a', 'b', 'c'], ow: { a: W, b: 18, c: W } },
    nhap(6),
  ]],
  dap: [
    `D1·1: a) 8,28·10<sup>−21</sup> J · b) bằng · c) 27 °C &nbsp;|&nbsp; D1·2: a) 5,18·10<sup>−21</sup> J · b) 227 °C &nbsp;|&nbsp; D2·1: a) 2,00 · b) 1,41 · c) 2,00 &nbsp;|&nbsp; D2·2: a) 0,50 · b) 0,71 · c) 0,50 &nbsp;|&nbsp; D3·1: a) 1,0·10<sup>5</sup> Pa · b) 1,44·10<sup>5</sup> Pa &nbsp;|&nbsp; D3·2: a) 0,92 kg/m³ · b) 1400 m/s`,
    `D4·1: a) 4,65·10<sup>−26</sup> kg · b<sub>1</sub>) 6,21·10<sup>−21</sup> J · b<sub>2</sub>) 517 m/s · c) 3,74 &nbsp;|&nbsp; D4·2: a) 5,32·10<sup>−26</sup> kg · b<sub>1</sub>) 8,28·10<sup>−21</sup> J · b<sub>2</sub>) 558 m/s · c) 1327 °C &nbsp;|&nbsp; D5·1: a) 6,0·10<sup>−21</sup> J · b) 290 K · c) 2,24·10<sup>5</sup> Pa &nbsp;|&nbsp; D5·2: a) 6,75·10<sup>−21</sup> J · b) 326 K · c) 2,58·10<sup>4</sup> Pa`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 2], kq: [[1, 2, 3], [4, 5]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'mô hình 1·4 · một phân tử 2·1 · N phân tử 2·2 · động năng – nhiệt độ 3·1 · bình kín 3·2 · bẫy 4·1 · bài toán mẫu 5·1 · dạng 1–3 → 6·1 · dạng 4–5 → 7·1',
  out: process.argv[2],
});
