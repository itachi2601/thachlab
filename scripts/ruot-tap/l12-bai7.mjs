// Ruột tập VL12 – Bài 7 · Phương trình trạng thái của khí lí tưởng (lesson id 8). Quyển Chương 2 lớp 12: bài 5 = tr. 1–12 → bài 7 = tr. 25–36.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l12-bai7.mjs (toàn bộ SVG tự vẽ). Nội dung theo bài web (book/cache/8.json, tải từ DB 12/11/2026): mục tiêu, dự đoán bình khí
// nén ngoài nắng, II.1–II.4 (ba thông số + phương trình trạng thái, đẳng tích, ba định luật, Clapeyron – Mendeleev), thí nghiệm bóng bàn,
// ba bẫy, Trả bài 6 câu, bài toán mẫu thân bơm xe đạp, thử thách ⭐–⭐⭐⭐, 5 dạng bài tập mẫu. Đáp số Bài tương tự tính bằng Python 12/11/2026.
// Chạy: node scripts/ruot-tap/l12-bai7.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl12-bai7.pdf
//       node scripts/ruot-tap/l12-bai7.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l12-bai7/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL12b7 as H } from './hinh-l12-bai7.mjs';

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
  const out = resolve(HERE, 'out/hinh-l12-bai7'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 7, lid: 8, ten: 'PHƯƠNG TRÌNH TRẠNG THÁI CỦA KHÍ LÍ TƯỞNG', lop: 12, baiDau: 5, sub: 'Vật lí 12 · Chương 2: Khí lí tưởng' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const RC = nw(m('R=8{,}31\\ \\mathrm{J/(mol{\\cdot}K)}'));
const TK = nw(m('T\\,(\\mathrm K)=t\\,(^\\circ\\mathrm C)+273'));
const atm = nw(m('1\\ \\mathrm{atm}\\approx1{,}013\\cdot10^5\\ \\mathrm{Pa}'));
const p1 = m('p_1'), p2 = m('p_2'), V1 = m('V_1'), V2 = m('V_2'), T1 = m('T_1'), T2 = m('T_2');
const oC = (s) => nw(m(`${s}\\ ^\\circ\\mathrm C`)), Pa = (s) => nw(m(`${s}\\ \\mathrm{Pa}`)), K_ = (s) => nw(m(`${s}\\ \\mathrm K`));
const lit = (s) => nw(`${m(s)} lít`);
const pt = m('\\dfrac{p_1V_1}{T_1}=\\dfrac{p_2V_2}{T_2}');

const ttCss = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';

const p1_ = `${ttCss}<section class="page">
${head('BÀI 7 · PHƯƠNG TRÌNH TRẠNG THÁI CỦA KHÍ LÍ TƯỞNG', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Nêu ba <b>thông số trạng thái</b>; viết <b>phương trình trạng thái</b> của một lượng khí`)}
${dong(`${ck}Phát biểu định luật của quá trình <b>đẳng tích</b> và hệ thức giữa ${m('p')} và ${m('T')}`)}
${dong(`${ck}Từ phương trình trạng thái suy ra ba định luật Boyle – Charles – Gay-Lussac`)}
${dong(`${ck}Dùng phương trình <b>Clapeyron – Mendeleev</b> tính số mol, khối lượng, thể tích khí`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Bình khí nén mini kín (lượng khí và thể tích không đổi). Sáng kim chỉ ${nw('5,0 bar')}, khí ở ${oC('27')}; trưa khí lên ${oC('47')}. Áp suất thay đổi thế nào?</p>
<div class="fig-side" style="${fs(38)}"><div>
${opt('A', 'Tăng khoảng 1,74 lần')}
${opt('B', 'Tăng khoảng 1,07 lần')}
${opt('C', 'Không đổi, vì thể tích bình không đổi')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 2)}</div>
${H.binhNang()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Ba thông số trạng thái — một hằng số', '1·4')}
<div class="card" style="padding:1.2mm 3mm">
<div>Một lượng khí xác định được mô tả bằng ba thông số trạng thái: ${f(22)}, ${f(22)}, ${f(30)}.</div>
<div style="margin:1mm 0;min-height:12mm;display:flex;align-items:flex-end;gap:3mm"><span>Phương trình trạng thái (lượng khí không đổi):</span> <span class="fill" style="min-width:42mm;height:11mm"></span></div>
<div>Hằng số ${m('pV/T')} chỉ phụ thuộc ${f(30)}, không phụ thuộc cách biến đổi.</div>
<div>Lập tỉ số hai trạng thái: ${m('p')} và ${m('V')} chỉ cần ${f(40)} ở hai vế; còn ${m('T')} thì ${f(40)}.</div>
</div>
${h3(5, 'Làm nhanh', '1·5')}
${box(cau(`<b>Câu 1.</b> Đề không nói giữ thông số nào: hệ thức nào luôn đúng cho một lượng khí xác định, vì sao?`, 1))}
${foot(1)}</section>`;

const p2_ = `<section class="page">
${head('VÌ SAO CÓ PHƯƠNG TRÌNH TRẠNG THÁI · THÍ NGHIỆM')}
${h3(1, 'Suy ra phương trình qua trạng thái trung gian', '2·1')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div>Đi từ (1) sang (2) qua trạng thái (1’) có áp suất ${p2}, nhiệt độ ${T1}, thể tích ${m("V'")}.</div>
<div style="margin-top:.6mm">(1) → (1’) giữ ${m('T')}, định luật ${f(20)}:</div><div style="text-align:right"><span class="fill" style="min-width:40mm"></span></div>
<div style="margin-top:.6mm">(1’) → (2) giữ ${m('p')}, định luật ${f(20)}:</div><div style="text-align:right"><span class="fill" style="min-width:40mm;height:9mm"></span></div>
${wl(`Rút ${m("V'")} rồi thay vào, được:`, 3)}</div>
${H.trungGian()}</div>
${h3(2, 'Thí nghiệm: quả bóng bàn bẹp phồng trở lại', '2·2')}
<div class="card fig-side" style="${fs(42)};padding:1.2mm 3mm"><div>
<div><b>Làm:</b> thả quả bóng bàn bị bẹp (chưa nứt) vào cốc nước nóng khoảng ${oC('80')}.</div>
${wl('Quan sát: <span style="font-weight:400">vỏ bóng</span>', 1)}
<div><b>Rút ra:</b> nước nóng làm ${m('T')} của khí trong bóng ${f(14)} → áp suất khí ${f(14)}, đẩy vỏ bóng về dạng cũ, thể tích ${f(14)}.</div>
<div>Cả ${f(10)} thông số cùng đổi, nên cần một ${f(44)} chung cho cả ba.</div></div>
${H.bongBan()}</div>
${h3(3, 'Làm nhanh', '2·3')}
${box(`<div style="line-height:6mm"><b>Đổi nhiệt độ</b> (cho sẵn ${TK}): ${nw(`${oC('27')} = ${f(14)} K`)} &nbsp; ${nw(`${oC('-33')} = ${f(14)} K`)} &nbsp; ${nw(`${K_('450')} = ${f(14)} °C`)} &nbsp; ${nw(`${oC('0')} = ${f(14)} K`)}</div>` + cau(`<b>Câu 2.</b> Một lượng khí: ${lit('V_1=3{,}0')}, ${p1} ${m('=2{,}0')} atm, ${oC('27')} → ${lit('V_2=2{,}0')}, ${oC('127')}. Tính ${p2}.`, 3))}
${h3(4, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '2·4')}
${rkHai([1, 2, 3, 4], [5, 6, 7])}
${foot(2)}</section>`;

const p3_ = `<section class="page">
${head('QUÁ TRÌNH ĐẲNG TÍCH · BA ĐỊNH LUẬT TRONG MỘT PHƯƠNG TRÌNH')}
${h3(1, 'II.2 · Thí nghiệm: bình kín ngâm nước ở năm nhiệt độ', '3·1')}
<div class="card" style="padding:1.2mm 3mm">
<div style="font-size:var(--fs-sm);line-height:1.35;margin-bottom:.6mm">Bình kín (thể tích không đổi) nối áp kế, ngâm lần lượt vào nước ở năm nhiệt độ; đợi kim áp kế đứng yên rồi đọc ${m('p')}.</div>
<table class="tbl-ct"><tr><th>${m('t')} (°C)</th><th>0</th><th>25</th><th>50</th><th>75</th><th>100</th></tr>
<tr><td>${m('T')} (K)</td><td>273</td><td>298</td><td>323</td><td>348</td><td></td></tr>
<tr><td>${m('p')} (kPa)</td><td>100,0</td><td>108,9</td><td>118,4</td><td>126,9</td><td>136,3</td></tr>
<tr><td>${m('p/T')} (kPa/K)</td><td>0,366</td><td>0,365</td><td>0,367</td><td>0,365</td><td></td></tr></table>
<div style="margin-top:.6mm"><b>Rút ra:</b> ${m('p/T')} ${f(40)} nên ${m('p')} ${f(40)} với ${m('T')}.</div>
<div>Chia ${m('p')} cho ${m('t')} (°C) thì tỉ số ${f(46)} (lỗi khái niệm, không phải sai số).</div></div>
${h3(2, 'Định luật của quá trình đẳng tích', '3·2')}
<div class="card fig-side" style="${fs(44)};padding:1.2mm 3mm"><div>
<div>Quá trình đẳng tích: ${f(30)} không đổi.</div>
<div>Áp suất ${f(28)} với ${nw(`nhiệt độ ${f(24)}.`)}</div>
<div style="margin:1mm 0;min-height:12mm;display:flex;align-items:flex-end;gap:3mm"><span>Hệ thức:</span><span class="fill" style="min-width:34mm;height:11mm"></span></div>
<div>Hằng số ${m('p/T')} phụ thuộc lượng khí và ${nw(`${f(22)}.`)}</div>
<div>Đồ thị ${m('p')}–${m('T')}: đường thẳng kéo dài đi qua ${nw(`${f(22)}.`)}</div>
<div>Cùng ${m('T')}, đường nằm trên có:</div><div>${m('p')} ${f(20)} ⇒ ${m('V')} ${f(20)}.</div></div>
${H.dangTich()}</div>
${h3(3, 'II.3 · Ba định luật cũ nằm gọn trong một phương trình', '3·3')}
<table><tr><th style="width:30mm">Giữ không đổi</th><th>Hệ thức còn lại</th><th style="width:44mm">Tên định luật (Boyle / Charles / Gay-Lussac)</th></tr>
<tr><td style="height:9mm">Nhiệt độ ${m('T')}</td><td></td><td></td></tr>
<tr><td style="height:9mm">Áp suất ${m('p')}</td><td></td><td></td></tr>
<tr><td style="height:9mm">Thể tích ${m('V')}</td><td></td><td></td></tr></table>
${h3(4, 'Làm nhanh', '3·4')}
${box(cau(`<b>Câu 3.</b> Khí trong bình kín ở ${oC('27')}, ${Pa('3{,}0\\cdot10^5')}. Hạ xuống ${oC('0')} thì áp suất bằng bao nhiêu?`, 3))}
${foot(3)}</section>`;

const p4_ = `<section class="page">
${head('CLAPEYRON – MENDELEEV · BA CÁI BẪY · THỬ THÁCH')}
${h3(1, 'II.4 · Phương trình Clapeyron – Mendeleev', '4·1')}
<div class="card fig-side" style="${fs(34)};padding:1.2mm 3mm"><div>
<div>Cho sẵn: ${RC}; ${atm}.</div>
<div>Hằng số ${m('pV/T')} của một lượng khí bằng ${f(14)}, với ${m('n')} là ${f(22)}.</div>
<div style="margin:1mm 0;min-height:11mm;display:flex;align-items:flex-end;gap:3mm"><span>Phương trình:</span><span class="fill" style="min-width:26mm;height:5mm"></span><span>số mol ${m('n=')}</span><span class="fill" style="min-width:14mm;height:10mm"></span></div>
<div>Dùng ${m('R=8{,}31')} thì ${m('p')} tính bằng ${f(12)}, ${m('V')} bằng ${f(12)}, ${m('T')} bằng ${f(10)}.</div>
<div>${m('m')} và ${m('M')} cùng đơn vị (cùng g hoặc cùng kg).</div>
<div>Điều kiện tiêu chuẩn (${oC('0')}, 1 atm): 1 mol khí chiếm 22,4 lít.</div></div>
${H.molKhi()}</div>
${box(cau(`<b>Ví dụ.</b> ${nw('32 g')} khí oxygen (${nw(m('M=32\\ \\mathrm{g/mol}'))}) chiếm bao nhiêu lít ở ${oC('27')}, ${Pa('1{,}0\\cdot10^5')}?`, 2))}
${h3(2, 'III · Ba cái bẫy hay sập', '4·2')}
<div class="card fig-side" style="${fs(34)};padding:1mm 3mm"><div>
<div class="trap"><span class="ck" style="flex:none"></span><span><b>“Lấy tỉ số hai nhiệt độ Celsius.”</b> ${oC('27')} lên ${oC('47')} nghe như gần gấp đôi, nhưng thật ra ${K_('300')} → ${K_('320')}, chỉ tăng 6,7 %. Tỉ số chỉ lấy trên thang Kelvin.</span></div>
<div class="trap"><span class="ck" style="flex:none"></span><span><b>“Bình vẫn kín thì dùng phương trình trạng thái được.”</b> Đã xả bớt hoặc bơm thêm khí thì lượng khí đổi, hằng số ${m('pV/T=nR')} đổi: tính ${m('n')} riêng cho từng trạng thái.</span></div>
<div class="trap"><span class="ck" style="flex:none"></span><span><b>“Đường dốc hơn là thể tích lớn hơn.”</b> Kẻ đường thẳng đứng tại một ${m('T')}: đường nằm trên có ${m('p')} lớn hơn, cùng lượng khí thì ${m('V')} nhỏ hơn.</span></div></div>
${H.haiThang()}</div>
${h3(3, 'Thử thách phân tầng', '4·3')}
${box(cau(`${m('\\bigstar')} Xilanh pittông tự do (áp suất không đổi): ${lit('3{,}0')} khí ở ${oC('27')} nung lên ${oC('127')}. Thể tích?`, 1)
 + cau(`${m('\\bigstar\\bigstar')} Bình ${lit('4')} có van an toàn mở ở ${Pa('8{,}0\\cdot10^5')}. Sáng ${oC('27')}, ${Pa('6{,}0\\cdot10^5')}. Khí nóng tới bao nhiêu °C thì van mở?`, 2)
 + cau(`${m('\\bigstar\\bigstar\\bigstar')} Cùng lượng khí ở hai bình ${m('V_1\\lt V_2')}: trên đồ thị ${m('p')}–${m('T')}, đường đẳng tích nào nằm trên, vì sao?`, 2))}
${foot(4)}</section>`;

const p5_ = `<section class="page">
${head('TRẢ BÀI · BÀI TOÁN MẪU · BÀI TẬP VỀ NHÀ')}
${h3(1, 'IV · Trả bài 6 câu', '5·1')}
${box(`${tb('1. Ba thông số trạng thái; phương trình trạng thái.')}${lines(2)}
${tb(`2. Vì sao phải dùng ${m('T')} (K), không dùng ${m('t')} (°C)?`)}${lines(1)}
${tb('3. Quá trình đẳng tích: định nghĩa, định luật, hệ thức.')}${lines(2)}
${tb(`4. Hằng số ${m('p/T')} và ${m('pV/T')} phụ thuộc những gì?`)}${lines(1)}
${tb('5. Từ phương trình trạng thái suy ra ba định luật thế nào?')}${lines(2)}
${tb(`6. Clapeyron – Mendeleev; ${m('R')}; 1 mol ở điều kiện tiêu chuẩn?`)}${lines(2)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/6 câu · chưa thuộc: ${f(25)} ${nw(`→ đọc lại ô ${f(12)} Tập`)}</div>
${h3(2, 'V · Bài toán mẫu: nén khí trong thân bơm xe đạp', '5·2')}
<div class="card soft" style="padding:1.2mm 3mm">Thân bơm (bịt kín đầu vòi) chứa ${nw(m('200\\ \\mathrm{cm^3}'))} không khí ở ${oC('27')}, ${Pa('1{,}0\\cdot10^5')}.
<b>a)</b> Nén nhanh còn ${nw(m('40\\ \\mathrm{cm^3}'))}, khí lên ${oC('87')}: tính áp suất.
<b>b)</b> Nén thật chậm, nhiệt độ giữ ${oC('27')}: áp suất bao nhiêu?
<b>c)</b> Số mol khí trong thân bơm sau khi nén nhanh (cho sẵn ${RC}, ${nw(m('1\\ \\mathrm{cm^3}=10^{-6}\\ \\mathrm{m^3}'))}).</div>
<div class="fig-side" style="${fs(35)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl(`a) Đổi K: ${T1} = ${f(14)} ; ${p2} =`, 2)}${wl(`b) Định luật: ${f(16)} ⇒ ${m("p'_2=")}`, 1)}${wl(`c) Đổi ${V2} ra m³; ${m('n=')}`, 2)}</div>${H.bom()}</div>
${K.btvn().replace('<i>1</i>', '<i>3</i>').replace(wl('Ghi chú của thầy về đề:', 2), wl('Ghi chú của thầy về đề:', 1))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Quá trình đẳng tích: nung nóng bình kín',
    de: `Bình thép kín (thể tích không đổi) chứa khí ở ${oC('27')}, ${Pa('2{,}4\\cdot10^5')}; để gần lò nung, khí lên ${oC('117')}.<br><b>a)</b> áp suất khí trong bình lúc đó<br><b>b)</b> van an toàn mở khi áp suất đạt ${Pa('3{,}6\\cdot10^5')}: khí nóng tới bao nhiêu °C thì van mở`,
    nd: `Bình kín, ${m('V')} không đổi ⇒ ${nw(`${m('p_1/T_1=')} ${f(14)}`)}; đổi ${m('t')} ra ${f(12)} trước khi chia`, a: ['a', 'b'], gi: 2 },
  { t: 'Dạng 2 · Trung bình · Cả p, V, T cùng đổi',
    de: `Xi lanh động cơ chứa ${nw(m('2{,}4\\ \\mathrm{dm^3}'))} hỗn hợp khí ở ${nw('1,0 atm')}, ${oC('27')}. Pit-tông nén xuống ${nw(m('0{,}20\\ \\mathrm{dm^3}'))} thì áp suất tăng lên ${nw('18 atm')}; lượng khí không đổi.<br><b>a)</b> nhiệt độ khí cuối quá trình nén: a<sub>1</sub> theo K, a<sub>2</sub> theo °C<br><b>b)</b> nếu nén thật chậm để nhiệt độ vẫn ${oC('27')}: áp suất cuối (atm); so với ${nw('18 atm')}`,
    nd: `${nw(`${m('T_2=T_1\\cdot')} ${f(18)}`)}; ${m('p')}, ${m('V')} giữ atm, dm³ (chỉ lấy tỉ số); giữ ${m('T')} ⇒ định luật ${f(16)}`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b'], gi: 4 },
  { t: 'Dạng 3 · Trung bình · Đọc đồ thị p–T của hai đường đẳng tích',
    de: `Cùng một lượng khí: nung trong bình kín ${lit('V_1=4{,}0')} là đoạn MN trên đường (1); trong bình kín khác là đường (2) qua Q. Hai đường kéo dài qua O.<br><b>a)</b> áp suất tại N<br><b>b)</b> thể tích bình ứng với đường (2)<br><b>c)</b> đường nào ứng với thể tích lớn hơn`,
    nd: `Cùng một đường: ${nw(`${m('p/T')} ${f(16)}`)}; M, Q cùng ${m('T')} nên ${nw(`${m('p_MV_1=')} ${f(14)}`)}`, a: ['a', 'b', 'c'], gi: 5, fig: H.doThiD3() },
  { t: 'Dạng 4 · Khá · Clapeyron – Mendeleev: số mol, khối lượng, thể tích',
    de: `Bình thép dung tích ${lit('12')} chứa khí nitrogen (${nw(m('M=28\\ \\mathrm{g/mol}'))}) ở ${oC('27')}, ${Pa('2{,}0\\cdot10^6')}. Cho sẵn ${RC}; ở điều kiện tiêu chuẩn (${oC('0')}, 1 atm) 1 mol khí chiếm 22,4 lít.<br><b>a)</b> số mol khí trong bình<br><b>b)</b> khối lượng nitrogen<br><b>c)</b> đưa lượng khí này về điều kiện tiêu chuẩn thì chiếm bao nhiêu lít`,
    nd: `Đổi ${m('V')} ra ${f(16)}, ${m('T')} ra K; ${nw(`${m('n=')} ${f(18)}`)}, ${nw(`${m('m=')} ${f(12)}`)}`, a: ['a', 'b', 'c'], gi: 6 },
  { t: 'Dạng 5 · Khó · Lượng khí thay đổi: khối lượng khí đã dùng',
    de: `Bình thép ${lit('8{,}0')} chứa oxygen (${nw(m('M=32\\ \\mathrm{g/mol}'))}). Mới nạp: ${oC('27')}, ${Pa('4{,}5\\cdot10^6')}. Sau một thời gian dùng để hàn, đóng van, để trong kho ở ${oC('17')}, áp suất còn ${Pa('1{,}5\\cdot10^6')}. Cho sẵn ${RC}.<br><b>a)</b> khối lượng oxygen lúc mới nạp và lúc còn lại<br><b>b)</b> khối lượng oxygen đã dùng`,
    nd: `Lượng khí đã đổi ⇒ ${f(16)} dùng ${pt}; viết ${m('pV=nRT')} riêng cho từng trạng thái, ${nw(`${m('m=')} ${f(14)}`)}`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b'], gi: 6, fig: H.haiLanD5() },
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
    { t: 'Dạng 1 · Bài 1', de: `Bình kín chứa khí ở ${oC('27')}, ${Pa('1{,}5\\cdot10^5')}; thể tích bình không đổi.<br><b>a)</b> phơi nắng, khí nóng tới ${oC('57')}: áp suất khí<br><b>b)</b> làm lạnh để áp suất còn ${Pa('1{,}2\\cdot10^5')}: nhiệt độ khí (°C)`, o: ['a', 'b'], ow: 30 },
    { t: 'Dạng 1 · Bài 2', de: `Bóng đèn sợi đốt chứa khí trơ ở ${oC('27')}, áp suất ${nw('0,50 atm')}; thể tích bóng không đổi.<br><b>a)</b> đèn sáng, khí nóng tới ${oC('327')}: áp suất khí<br><b>b)</b> bóng chịu được tối đa ${nw('1,2 atm')}: khí nóng tới bao nhiêu °C thì bóng vỡ`, o: ['a', 'b'], ow: 30 },
    { t: 'Dạng 2 · Bài 1', de: `Xi lanh chứa ${lit('3{,}0')} khí ở ${nw('1,0 atm')}, ${oC('7')}. Nén còn ${lit('0{,}50')} thì áp suất ${nw('7,5 atm')}; lượng khí không đổi.<br><b>a)</b> nhiệt độ khí sau khi nén, theo K và theo °C<br><b>b)</b> nếu nén thật chậm, nhiệt độ giữ ${oC('7')}: áp suất cuối (atm)`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b'], ow: 22 },
    { t: 'Dạng 2 · Bài 2', de: `Bóng thám không chứa ${nw(m('6{,}0\\ \\mathrm{m^3}'))} khí ở mặt đất: ${Pa('1{,}0\\cdot10^5')}, ${oC('27')}. Lên cao, áp suất ${Pa('0{,}50\\cdot10^5')}, nhiệt độ ${oC('-33')}; lượng khí không đổi.<br><b>a)</b> thể tích bóng trên cao<br><b>b)</b> nếu nhiệt độ trên cao vẫn là ${oC('27')}: thể tích bóng`, o: ['a', 'b'], ow: 30 },
    { t: 'Dạng 3 · Bài 1', de: `Đồ thị ${m('p')}–${m('T')} của một lượng khí: đường (1) qua O và M (${K_('300')}, ${Pa('2{,}0\\cdot10^5')}), ứng với bình kín ${lit('6{,}0')}; đường (2) của cùng lượng khí qua O và Q (${K_('300')}, ${Pa('3{,}0\\cdot10^5')}).<br><b>a)</b> điểm N trên (1) có ${Pa('3{,}0\\cdot10^5')}: nhiệt độ tại N<br><b>b)</b> thể tích bình ứng với đường (2)<br><b>c)</b> đường nào ứng với thể tích lớn hơn`, o: ['a', 'b', 'c'], ow: 22 },
    { t: 'Dạng 3 · Bài 2', de: `Cùng một lượng khí: đường đẳng tích (1) ứng với ${lit('V_1=2{,}0')}, qua A (${K_('250')}, ${Pa('1{,}0\\cdot10^5')}); đường đẳng tích (2) ứng với ${lit('V_2=5{,}0')}.<br><b>a)</b> hằng số ${m('p/T')} của đường (1) (Pa/K)<br><b>b)</b> áp suất trên đường (2) tại ${K_('500')}<br><b>c)</b> đường nào nằm trên`, o: ['a', 'b', 'c'], ow: 22 },
    nhap(4),
  ], [
    { t: 'Dạng 4 · Bài 1', de: `Bình ${lit('10')} chứa khí oxygen (${nw(m('M=32\\ \\mathrm{g/mol}'))}) ở ${oC('27')}, ${Pa('1{,}5\\cdot10^6')}. Cho sẵn ${RC}; 1 mol khí ở điều kiện tiêu chuẩn chiếm 22,4 lít.<br><b>a)</b> số mol khí<br><b>b)</b> khối lượng oxygen<br><b>c)</b> thể tích lượng khí này ở điều kiện tiêu chuẩn`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 4 · Bài 2', de: `Nạp ${nw('0,56 kg')} khí nitrogen (${nw(m('M=28\\ \\mathrm{g/mol}'))}) vào bình ${lit('50')} ở ${oC('27')}. Cho sẵn ${RC}; 1 mol khí ở điều kiện tiêu chuẩn chiếm 22,4 lít.<br><b>a)</b> số mol khí<br><b>b)</b> áp suất khí trong bình<br><b>c)</b> thể tích lượng khí này ở điều kiện tiêu chuẩn`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 5 · Bài 1', de: `Bình ${lit('20')} chứa nitrogen (${nw(m('M=28\\ \\mathrm{g/mol}'))}). Lúc đầu ${oC('27')}, ${Pa('5{,}0\\cdot10^6')}; sau khi dùng bớt, ở ${oC('7')}, áp suất còn ${Pa('2{,}0\\cdot10^6')}. Cho sẵn ${RC}.<br><b>a)</b> khối lượng khí lúc đầu và lúc sau<br><b>b)</b> khối lượng khí đã dùng`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b'], ow: 22 },
    { t: 'Dạng 5 · Bài 2', de: `Bình ${lit('10')} chứa oxygen (${nw(m('M=32\\ \\mathrm{g/mol}'))}) ở ${oC('17')}, ${Pa('1{,}2\\cdot10^6')}. Bơm thêm oxygen, sau đó bình ở ${oC('27')}, ${Pa('2{,}5\\cdot10^6')}. Cho sẵn ${RC}.<br><b>a)</b> khối lượng khí trước và sau khi bơm<br><b>b)</b> khối lượng khí đã bơm thêm<br><b>c)</b> có dùng được ${pt} cho hai trạng thái này không`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'], ow: 20 },
    nhap(10),
  ]],
  dap: [
    `D1·1: a) 1,65·10<sup>5</sup> Pa · b) −33 °C &nbsp;|&nbsp; D1·2: a) 1,0 atm · b) 447 °C &nbsp;|&nbsp; D2·1: a<sub>1</sub>) 350 K · a<sub>2</sub>) 77 °C · b) 6,0 atm &nbsp;|&nbsp; D2·2: a) 9,6 m³ · b) 12 m³ &nbsp;|&nbsp; D3·1: a) 450 K · b) 4,0 lít · c) đường (1) &nbsp;|&nbsp; D3·2: a) 400 Pa/K · b) 0,80·10<sup>5</sup> Pa · c) đường (1)`,
    `D4·1: a) 6,02 mol · b) 193 g · c) 135 lít &nbsp;|&nbsp; D4·2: a) 20 mol · b) 1,0·10<sup>6</sup> Pa · c) 448 lít &nbsp;|&nbsp; D5·1: a<sub>1</sub>) 1,12 kg · a<sub>2</sub>) 481 g · b) 642 g &nbsp;|&nbsp; D5·2: a<sub>1</sub>) 159 g · a<sub>2</sub>) 321 g · b) 162 g · c) không (lượng khí đổi)`,
  ],
};

await K.dung({
  trang1to5: [p1_, p2_, p3_, p4_, p5_].join('\n'),
  btm: { dang, tach: [3, 2], kq: [[1, 2, 3], [4, 5]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'ba thông số 1·4 · đổi K 2·3 · suy ra 2·1 · bóng bàn 2·2 · đẳng tích 3·1 · ba định luật 3·3 · Clapeyron 4·1 · bẫy 4·2 · trả bài 5·1 · bài mẫu 5·2 · dạng 1–3 → 6·1 · dạng 4–5 → 7·1',
  out: process.argv[2],
});
