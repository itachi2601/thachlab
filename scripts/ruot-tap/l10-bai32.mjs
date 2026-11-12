// Ruột tập VL10 – Bài 32 · Lực hướng tâm và gia tốc hướng tâm (lesson id 77). Quyển Chương 6 lớp 10: bài 31 = tr. 1–12, bài 32 = tr. 13–24.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự (giải vào vở) · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l10-bai32.mjs (toàn bộ SVG tự vẽ, không dùng ảnh Halliday). Nội dung theo bài web (book/cache/77.json, tải từ DB 12/11/2026):
// mục tiêu, dự đoán khúc cua, II.1–II.3, thí nghiệm đồng xu + nút cao su, ba bẫy, Trả bài 6 câu, bài toán mẫu ô tô qua cua, thử thách, 5 dạng.
// Đáp số Bài tương tự (tuongTu.dap) và các số trong tập tính bằng Python 12/11/2026 (π ≈ 3,14 khi đề in sẵn π ≈ 3,14).
// Tránh 4 lỗi lặp HS ảo L11 Ch.3: g, π in sẵn ngay trong đề; Mục tiêu + hình khúc cua không vẽ/nêu hướng gia tốc; ô đáp án chữ 40 mm;
// dòng kẻ ≥ số ý ở Dạng 1–3.
// Chạy: node scripts/ruot-tap/l10-bai32.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl10-bai32.pdf
//       node scripts/ruot-tap/l10-bai32.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l10-bai32/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL10b32 as H } from './hinh-l10-bai32.mjs';

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
  const out = resolve(HERE, 'out/hinh-l10-bai32'); mkdirSync(out, { recursive: true });
  const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true, args: ['--allow-file-access-from-files'] });
  const pg = await b.newPage();
  const kx = pathToFileURL(BOOK + 'node_modules/katex/dist/katex.min.css').href;
  for (const [name, fn] of Object.entries(H)) {
    writeFileSync(out + '/_tmp.html', `<!doctype html><meta charset="utf-8"><link rel="stylesheet" href="${kx}"><style>${css}</style>${fn()}`);
    await pg.goto(pathToFileURL(out + '/_tmp.html').href, { waitUntil: 'networkidle0' });
    await pg.evaluate('document.fonts.ready');
    await (await pg.$('.fig')).screenshot({ path: `${out}/${name}.png` });
    console.log(`${name}.png`);
  }
  await b.close();
  process.exit(0);
}

const K = khoiTao({ bai: 32, lid: 77, ten: 'LỰC HƯỚNG TÂM VÀ GIA TỐC HƯỚNG TÂM', lop: 10, baiDau: 31, sub: 'Vật lí 10 · Chương 6: Chuyển động tròn' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const g10 = nw(m('g=10\\ \\mathrm{m/s^2}'));
const g98 = nw(m('g=9{,}8\\ \\mathrm{m/s^2}'));
const pi = nw(m('\\pi\\approx 3{,}14'));
const aht = m('a_{\\mathrm{ht}}'), Fht = m('F_{\\mathrm{ht}}'), om = m('\\omega'), Fms = m('F_{\\mathrm{ms}}'), Fmax = m('F_{\\max}');

// Bài tương tự: cùng CSS 2 cột/ô cuối dòng như l10-bai23.mjs (khung xếp .tt dọc).
const ttHaiCot = '<style>.bt>.gi{display:grid;grid-template-columns:1fr 1fr;column-gap:4mm}.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm}.yo .oo{flex:none;display:flex;gap:3mm}.yo{line-height:1.35}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';
const p1 = `${ttHaiCot}<section class="page">
${head('BÀI 32 · LỰC HƯỚNG TÂM VÀ GIA TỐC HƯỚNG TÂM', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Phân biệt <b>tốc độ</b> và <b>vận tốc</b> của vật chuyển động tròn đều`)}
${dong(`${ck}Nêu gốc, phương, chiều và tính độ lớn của <b>gia tốc</b> trong chuyển động tròn đều`)}
${dong(`${ck}Chỉ ra lực nào đóng vai <b>lực hướng tâm</b>; tính ${Fht}`)}
${dong(`${ck}Gỡ ba hiểu lầm: “lực mới”, “lực li tâm”, ${aht} phụ thuộc ${m('r')} thế nào`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Trong lúc qua khúc cua, xe có gia tốc không? Nếu có, gia tốc hướng về đâu?</p>
<div class="fig-side" style="${fs(46)}"><div>
${opt('A', 'Không có, vì kim tốc độ đứng yên')}
${opt('B', 'Có, hướng theo chiều xe đang chạy')}
${opt('C', 'Có, hướng vào phía trong khúc cua')}
${opt('D', 'Có, hướng ra phía ngoài khúc cua')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 2)}</div>
${H.khucCua()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Vận tốc trong chuyển động tròn đều', '1·4')}
<div class="card fig-side" style="${fs(48)};padding:1.2mm 3mm"><div>
<div>Gia tốc đo độ biến đổi của vectơ vận tốc, cả ${f(20)} lẫn ${f(20)}.</div>
<div>Tròn đều: độ lớn vận tốc ${f(20)}, hướng ${f(20)} ⇒ ${ck}có &nbsp;${ck}không có gia tốc.</div>
<div>${m('\\Delta\\vec v')} em vẽ ở hình chĩa về ${f(25)}.</div>
<div style="margin-top:.6mm"><b>Gia tốc hướng tâm:</b> gốc ${f(20)}</div>
<div>phương ${f(30)} · chiều ${f(20)}</div>
<div style="margin:.6mm 0">${aht}${m('\\,=')} ${f(14)} ${m('=')} ${f(14)} &nbsp;đơn vị ${f(12)}</div>
<div class="hint">Đổi được hai dạng nhờ ${m('v=\\omega r')} (Bài 31).</div></div>
${H.deltaV()}</div>
${h3(5, 'Làm nhanh', '1·5')}
${box(cau(`<b>Câu 1.</b> Kim giây đồng hồ quay đều. Đầu kim có gia tốc không? Nếu có, hướng về đâu?`, 2))}
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('TÍNH GIA TỐC HƯỚNG TÂM · LỰC HƯỚNG TÂM')}
${h3(1, 'Tính thử · cho sẵn 1 m/s = 3,6 km/h', '2·1')}
<div class="card" style="padding:1.2mm 3mm">
<div>Xe ${nw('36 km/h')} = ${f(12)} m/s qua cua ${nw(m('r=50\\ \\mathrm m'))}: ${aht}${m('\\,=')} ${f(16)} ${m('\\mathrm{m/s^2}')}</div>
<div style="margin-top:.6mm">Lồng vắt máy giặt quay ${nw('600 vòng/phút')}, thành lồng cách trục ${nw('20 cm')} (${pi}, ${g98}):</div>
<div>${m('f=')} ${f(12)} vòng/s · ${m('\\omega=2\\pi f=')} ${f(16)} rad/s · ${aht}${m('\\,=')} ${f(16)} ${m('\\mathrm{m/s^2}')} ≈ ${f(12)} lần ${m('g')}</div></div>
${h3(2, 'II.2 · Lực hướng tâm: tên một vai, không phải lực mới', '2·2')}
<div class="card" style="padding:1.2mm 3mm">
<div>Lực hướng tâm là lực (hay ${f(20)}) tác dụng lên vật chuyển động tròn đều, hướng ${f(20)}.</div>
<div>Nó ${ck}là &nbsp;${ck}không phải một loại lực mới: luôn là một lực ${f(20)} hoặc hợp lực của chúng.</div>
<div style="margin:.6mm 0">${Fht}${m('\\,=m\\,a_{\\mathrm{ht}}=')} ${f(16)} ${m('=')} ${f(16)} &nbsp;(N)</div></div>
<table><tr><th style="width:62mm">Tình huống</th><th>Lực đóng vai lực hướng tâm</th></tr>
<tr><td>Vệ tinh bay tròn quanh Trái Đất</td><td></td></tr>
<tr><td>Ô tô qua cua trên đường phẳng</td><td></td></tr>
<tr><td>Vật buộc dây quay trên bàn nhẵn</td><td></td></tr>
<tr><td>Người trượt băng nghiêng người vào cua</td><td>thành phần nằm ngang của <span class="hint" style="font-size:.85em">(lực mặt băng đỡ người)</span></td></tr></table>
${h3(3, 'Thí nghiệm: đồng xu trên bàn xoay', '2·3')}
<div class="card fig-side" style="${fs(42)};padding:1.2mm 3mm"><div>
<div><b>Làm:</b> đặt đồng xu trên đĩa bàn xoay, cách tâm khoảng ${nw('10 cm')}. Quay chậm rồi nhanh dần.</div>
<div><b>Quan sát:</b> quay chậm, xu ${f(25)}; quay đủ nhanh, xu ${f(25)}.</div>
<div><b>Rút ra:</b> lực giữ xu đi vòng là ${f(25)}. Xu trượt khi lực cần có ${m('m\\omega^2 r')} ${f(14)} ma sát nghỉ lớn nhất.</div>
${wl('Quay càng nhanh thì xu càng dễ trượt. Vì sao?', 1)}</div>
${H.dongXu()}</div>
${h3(4, 'Làm nhanh', '2·4')}
${box(cau(`<b>Câu 2.</b> Xe đạp ${nw('15 m/s')} qua cua bán kính ${nw('75 m')}: gia tốc hướng tâm? Nhanh gấp 3 thì gia tốc gấp mấy lần?`, 2)
 + cau(`<b>Câu 3.</b> Tạ xích quay tròn: lực nào đóng vai lực hướng tâm? Buông tay, tạ bay theo hướng nào?`, 2))}
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('ĐO THỬ F = mv²/r · BẪY · TRẢ BÀI')}
${h3(1, 'Thí nghiệm: nút cao su quay trên đầu ống', '3·1')}
<div class="fig-side" style="${fs(46)}"><div>
<div><b>Làm:</b> nút ${nw(m('m=0{,}050\\ \\mathrm{kg}'))} buộc đầu dây luồn qua ống, đầu dưới treo quả nặng ${m('M')}. Quay nút thành vòng tròn ngang ${nw(m('r=0{,}50\\ \\mathrm m'))}, bấm giờ 10 vòng ${m('t_{10}')}.</div>
<div><b>Rút ra:</b> quả nặng đứng yên ⇒ lực căng ${m('T=')} ${f(14)}; lực căng đóng vai ${f(25)}.</div>
<div class="hint">Tính: ${m('T_{\\mathrm q}=t_{10}/10')} (chu kì quay), ${m('v=2\\pi r/T_{\\mathrm q}')}; ${pi}, ${g98}.</div>
</div>${H.nutCaoSu('Quả nặng đứng yên: T = ?')}</div>
<table class="tbl-ct" style="margin-top:.6mm"><style>.tbl-ct td{height:5mm;padding-top:.3mm;padding-bottom:.3mm}</style><tr><th>${m('Mg')} (N)</th><th>${m('t_{10}')} (s)</th><th>${m('T_{\\mathrm q}')} (s)</th><th>${m('v')} (m/s)</th><th>${m('mv^2/r')} (N)</th></tr>
<tr><td>0,98</td><td>10,2</td><td>1,02</td><td>3,08</td><td>0,95</td></tr>
<tr><td>1,96</td><td>7,1</td><td></td><td></td><td></td></tr>
<tr><td>2,94</td><td>6,0</td><td></td><td></td><td></td></tr></table>
<div>So hai cột lực: hàng nào lệch nhiều nhất? Thử nêu một nguyên nhân gây lệch.</div>${lines(2)}
${h3(2, 'III · Ba cái bẫy hay sập', '3·2')}
<div class="card fig-side" style="${fs(35)};padding:1mm 3mm"><div>
<div class="trap">${ck}<span><b>“Vẽ thêm lực hướng tâm.”</b> Nó chỉ là vai của một lực đã có.</span></div>
<div class="trap">${ck}<span><b>“Lực li tâm đẩy vật ra.”</b> Không vật nào gây ra nó. Mất lực hướng tâm, vật bay theo ${f(20)} (đường ${f(8)}).</span></div>
<div class="trap">${ck}<span><b>“${m('r')} lớn thì ${aht} nhỏ.”</b> Cùng ${m('v')}: ${m('a=v^2/r')}, ${m('r')} lớn → ${m('a')} ${f(10)} · cùng ${om}: ${m('a=\\omega^2 r')}, ${m('r')} lớn → ${m('a')} ${f(10)}</span></div></div>
${H.viBi()}</div>
${h3(3, 'IV · Trả bài 6 câu', '3·3')}
${box(`${tb('1. Vì sao tròn đều có gia tốc dù tốc độ không đổi?')}${lines(1)}
${tb('2. Gốc, phương, chiều, độ lớn, đơn vị của gia tốc hướng tâm.')}${lines(2)}
${tb('3. Lực hướng tâm là gì? Có phải một loại lực mới?')}${lines(1)}
${tb('4. Ba tình huống và lực đóng vai lực hướng tâm.')}${lines(2)}
${tb('5. Dây đứt, vật bay theo hướng nào? Có “lực li tâm” không?')}${lines(1)}
${tb('6. r tăng thì gia tốc hướng tâm tăng hay giảm?')}${lines(1)}`)}
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('TỰ KIỂM TRA · BÀI TOÁN MẪU')}
${h3(1, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '4·1')}
${rkHai([1, 2, 3], [4, 5, 6])}
${h3(2, 'V · Bài toán mẫu: ô tô qua khúc cua', '4·2')}
<div class="card soft" style="padding:1.2mm 3mm">Ô tô ${m('1200\\ \\mathrm{kg}')} chạy đều ${m('36\\ \\mathrm{km/h}')} qua khúc cua tròn bán kính ${m('50\\ \\mathrm m')} trên đường nằm ngang. Lực ma sát nghỉ lớn nhất mặt đường tác dụng lên xe bằng ${m('0{,}5')} lần trọng lượng xe. Lấy ${g10}; ${nw('1 m/s = 3,6 km/h')}.
<div>Tính lực hướng tâm. Xe có bị trượt không? Tốc độ lớn nhất để qua cua an toàn?</div></div>
${h3(3, 'Phân tích đề')}
<table><tr><th style="width:50mm">Câu trong đề</th><th>Dữ liệu → kiến thức</th></tr>
<tr><td>“ô tô 1200 kg”</td><td>${m('m=1200\\ \\mathrm{kg}')}</td></tr>
<tr><td style="height:6.5mm">“chạy đều 36 km/h”</td><td></td></tr>
<tr><td style="height:6.5mm">“bán kính 50 m”</td><td></td></tr>
<tr><td style="height:6.5mm">“đường nằm ngang”</td><td></td></tr>
<tr><td style="height:6.5mm">“0,5 lần trọng lượng”</td><td></td></tr></table>
${h3(4, 'Giải')}
<div class="fig-side" style="${fs(48)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl(`Gia tốc ${aht}:`, 2)}${wl(`Lực hướng tâm cần có, do lực nào cung cấp:`, 2)}${wl(`${Fmax} và kết luận trượt hay không:`, 2)}${wl(`Tốc độ lớn nhất ${m('v_{\\max}')} (m/s và km/h):`, 3)}${wl(`${m('v_{\\max}')} có phụ thuộc ${m('m')} không?`, 1)}</div>${H.xeSau()}</div>
${h3(5, 'Điền bước còn thiếu: trời mưa, ma sát nghỉ lớn nhất chỉ còn 0,16 lần trọng lượng')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div class="ln"><b>Bước 1 (cho sẵn):</b> lực hướng tâm cần có vẫn là ${m('2400\\ \\mathrm N')}.</div>
${wl(`Bước 2: ${Fmax}${m('\\,=')} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; so với 2400 N, xe`, 1)}${wl(`Bước 3: ${m('v_{\\max}=')}`, 1)}</div>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TẬP VỀ NHÀ · THỬ THÁCH · MANG VỀ')}
${K.btvn()}
${h3(2, 'Thử thách phân tầng', '5·2')}
<div class="fig-side" style="${fs(42)}">${box(wl(`${m('\\bigstar')} Xe chạy ${nw('20 m/s')} qua cua bán kính ${nw('100 m')}. Gia tốc hướng tâm?`, 3)
 + wl(`${m('\\bigstar\\bigstar')} Đồng xu cách tâm bàn xoay ${nw('10 cm')}, bàn quay ${nw('30 vòng/phút')}; ma sát nghỉ lớn nhất bằng 0,3 lần trọng lượng xu; ${g10}, ${pi}. Xu có trượt không? Đặt xa tâm nhất bao nhiêu thì còn đứng yên?`, 5)
 + wl(`${m('\\bigstar\\bigstar\\bigstar')} Trạm vũ trụ bay tròn ở độ cao ${nw('400 km')} (bán kính Trái Đất ${nw('6400 km')}), tốc độ ${nw('7,7 km/s')}. Tính ${aht}. Phi hành gia “lơ lửng” có phải vì hết trọng lực?`, 5))}${H.traiDat()}</div>
${h3(3, 'Câu đổi chiều: biết lực giới hạn, tìm tốc độ', '5·3')}
${box(wl(`Vật ${nw('0,25 kg')} buộc dây quay tròn trên mặt bàn nằm ngang nhẵn, ${nw(m('r=0{,}50\\ \\mathrm m'))}. Dây chịu lực căng tối đa ${nw('18 N')}. Tốc độ lớn nhất để dây chưa đứt? Quay với ${nw('5,0 m/s')} thì lực căng bao nhiêu?`, 4))}
${h3(4, 'VI · Mang về: điều em dễ quên nhất', '5·4')}
${box(wl('1.', 3) + wl('2.', 3) + wl('3.', 3))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Vận tốc đổi hướng nên có gia tốc hướng tâm',
    de: `Hòn bi buộc dây (đầu kia cố định tại ${m('O')}) chạy tròn đều trên bàn nhẵn nằm ngang, ${nw(`${m('v=2{,}0\\ \\mathrm{m/s}')},`)} ${nw(`${m('r=0{,}50\\ \\mathrm m')};`)} ${m('A')}, ${m('B')} ở hai đầu một đường kính.<br><b>a)</b> vận tốc tại ${m('A')} và tại ${m('B')} có giống nhau không<br><b>b)</b> hòn bi có gia tốc không<br><b>c)</b> gia tốc của bi tại ${m('A')} hướng thế nào &nbsp; <b>d)</b> độ lớn gia tốc`,
    nd: `vận tốc là ${f(20)}; tốc độ không đổi nhưng ${f(20)} đổi ⇒ có gia tốc`, a: ['a', 'b', 'c', 'd'], gi: 5 },
  { t: 'Dạng 2 · Dễ · Gia tốc hướng tâm từ chu kì và bán kính',
    de: `Vòng quay công viên bán kính ${m('15\\ \\mathrm m')} quay đều, mỗi vòng hết ${m('40\\ \\mathrm s')}; khách ngồi ở mép vòng; ${pi}.<br><b>a)</b> tốc độ góc của vòng quay &nbsp; <b>b)</b> tốc độ dài của khách<br><b>c)</b> gia tốc hướng tâm của khách`,
    nd: `${nw(`${m('\\omega=')} ${f(12)}`)}, ${nw(`${m('v=')} ${f(12)}`)}, rồi ${nw(`${aht}${m('\\,=')} ${f(12)}`)}`, a: ['a', 'b', 'c'], gi: 4 },
  { t: `Dạng 3 · Trung bình · Giữ nguyên ${om} hay giữ nguyên ${m('v')}`,
    de: `Quạt trần quay đều ${m('\\omega=20\\ \\mathrm{rad/s}')}; điểm ${m('A')} cách trục ${m('10\\ \\mathrm{cm}')}, điểm ${m('B')} ở đầu cánh cách trục ${m('30\\ \\mathrm{cm}')}.<br><b>a)</b> gia tốc hướng tâm của ${m('A')} và của ${m('B')}<br><b>b)</b> hai xe máy cùng ${m('10\\ \\mathrm{m/s}')} qua hai khúc cua ${m('r_1=20\\ \\mathrm m')}, ${m('r_2=40\\ \\mathrm m')}: gia tốc hướng tâm mỗi xe<br><b>c)</b> xe 1 tăng lên ${m('12\\ \\mathrm{m/s}')} trên cua ${m('r_1')}: gia tốc gấp mấy lần lúc trước`,
    nd: `${m('A')}, ${m('B')} chung ${f(10)}; hai xe chung ${f(10)} → chọn công thức theo đại lượng chung`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], gi: 6, fig: H.quat(''), cot: 5 },
  { t: 'Dạng 4 · Trung bình · Lực nào đóng vai lực hướng tâm',
    de: `Vật nhỏ ${m('50\\ \\mathrm g')} đặt trên đĩa nằm ngang, cách trục ${m('20\\ \\mathrm{cm}')}. Đĩa quay đều ${m('60')} vòng/phút, vật không trượt; ${pi}.<br><b>a)</b> lực nào đóng vai lực hướng tâm của vật<br><b>b)</b> độ lớn lực hướng tâm<br><b>c)</b> lực đóng vai lực hướng tâm của (i) ô tô chạy đều qua cua nằm ngang; (ii) vệ tinh bay tròn quanh Trái Đất`,
    nd: `${m('\\vec P')}, ${m('\\vec N')} ${f(20)}; lực nằm ngang còn lại hướng vào tâm là ${f(25)}; ${nw(`${m('\\omega=2\\pi f')}, ${m('f=')} ${f(12)}`)}`, a: ['a', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'], gi: 5, fig: H.diaVat(''), cot: 2 },
  { t: 'Dạng 5 · Khó · Lực hướng tâm so với ma sát nghỉ cực đại',
    de: `Mô tô cùng người lái ${m('200\\ \\mathrm{kg}')} chạy đều ${m('54\\ \\mathrm{km/h}')} vào đường vòng nằm ngang. Ma sát nghỉ cực đại bằng ${m('0{,}60')} lần trọng lượng khi đường khô, ${m('0{,}30')} lần khi đường ướt; ${g10}.<br><b>a)</b> bán kính ${m('50\\ \\mathrm m')}: lực hướng tâm cần có; xe có trượt trên đường khô, đường ướt không<br><b>b)</b> bán kính cong nhỏ nhất để xe không trượt khi đường khô, khi đường ướt`,
    nd: `không trượt khi ${Fht} ${f(10)} ${Fmax}; giới hạn ứng với ${nw(`${Fht} ${f(10)} ${Fmax}`)}; đổi km/h ra m/s trước (${nw('1 m/s = 3,6 km/h')})`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'a<sub>3</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>'], gi: 7, fig: H.moTo(''), cot: 3 },
];

// Bài tương tự giải vào vở (thầy chốt 10/11): ô đáp số cuối đúng dòng của ý (như l10-bai23.mjs); ô 25 mm, 40 mm khi đáp án là chữ.
const oY = (s, o, w = 25) => s.split('<br>').map((p) => {
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
    { t: 'Dạng 1 · Bài 1', de: `Xe đồ chơi chạy tròn đều trên ray, ${m('r=0{,}80\\ \\mathrm m')}, ${m('v=0{,}40\\ \\mathrm{m/s}')}; ${m('M')}, ${m('N')} ở hai đầu một đường kính.<br><b>a)</b> vận tốc tại ${m('M')} và ${m('N')} giống hay khác nhau<br><b>b)</b> xe có gia tốc không<br><b>c)</b> gia tốc tại ${m('M')} hướng về đâu<br><b>d)</b> độ lớn gia tốc`, o: ['a', 'b', 'c', 'd'], ow: { a: 40, c: 40 } },
    { t: 'Dạng 1 · Bài 2', de: `Vận động viên chạy đều ${m('5{,}0\\ \\mathrm{m/s}')} trên đoạn đường cong tròn bán kính ${m('25\\ \\mathrm m')}.<br><b>a)</b> tốc độ có thay đổi không<br><b>b)</b> sau nửa vòng: góc giữa hai vectơ vận tốc<br><b>c)</b> gia tốc của người hướng về đâu<br><b>d)</b> độ lớn gia tốc`, o: ['a', 'b', 'c', 'd'], ow: { c: 40 } },
    { t: 'Dạng 2 · Bài 1', de: `Đu quay bán kính ${m('6{,}0\\ \\mathrm m')} quay đều, mỗi vòng hết ${m('12\\ \\mathrm s')}; ${nw(`${pi}.`)}<br><b>a)</b> tốc độ góc<br><b>b)</b> tốc độ dài của ghế ở mép<br><b>c)</b> gia tốc hướng tâm của ghế`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 2 · Bài 2', de: `Máy li tâm quay ${m('3000')} vòng/phút, ống nghiệm cách trục ${m('10\\ \\mathrm{cm}')}; ${pi}; ${nw(`${g98}.`)}<br><b>a)</b> tần số (vòng/s)<br><b>b)</b> tốc độ góc<br><b>c)</b> gia tốc hướng tâm của ống; gấp mấy lần ${m('g')}`, o: ['a', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'] },
    { t: 'Dạng 3 · Bài 1', de: `Đĩa quay đều ${nw(`${m('\\omega=3{,}5\\ \\mathrm{rad/s}')};`)} ${m('M')} cách tâm ${m('5{,}0\\ \\mathrm{cm}')}, ${m('N')} cách tâm ${nw(`${m('15\\ \\mathrm{cm}')}.`)}<br><b>a)</b> gia tốc hướng tâm của ${m('M')}, của ${m('N')}<br><b>b)</b> tỉ số ${m('a_N/a_M')}<br><b>c)</b> tỉ số ${m('v_N/v_M')}`, fig: H.diaMN(), fw: 40, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'], ow: 20 },
    { t: 'Dạng 3 · Bài 2', de: `Hai ô tô cùng chạy ${m('20\\ \\mathrm{m/s}')} qua hai khúc cua ${m('r_1=80\\ \\mathrm m')} và ${nw(`${m('r_2=160\\ \\mathrm m')}.`)}<br><b>a)</b> gia tốc hướng tâm của mỗi xe<br><b>b)</b> xe 2 phải chạy bao nhiêu m/s để gia tốc bằng xe 1`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b'] },
  ], [
    { t: 'Dạng 4 · Bài 1', de: `Vật ${m('100\\ \\mathrm g')} đặt trên đĩa nằm ngang cách trục ${nw(`${m('15\\ \\mathrm{cm}')};`)} đĩa quay đều ${m('30')} vòng/phút, vật không trượt; ${nw(`${pi}.`)}<br><b>a)</b> lực đóng vai lực hướng tâm<br><b>b)</b> tốc độ góc<br><b>c)</b> độ lớn lực hướng tâm`, o: ['a', 'b', 'c'], ow: { a: 40 } },
    { t: 'Dạng 4 · Bài 2', de: `Quả cầu ${m('200\\ \\mathrm g')} buộc dây quay tròn đều trên mặt bàn nằm ngang nhẵn, ${nw(`${m('r=0{,}50\\ \\mathrm m')},`)} tốc độ ${nw(`${m('3{,}0\\ \\mathrm{m/s}')}.`)}<br><b>a)</b> lực đóng vai lực hướng tâm<br><b>b)</b> độ lớn lực đó<br><b>c)</b> Mặt Trăng quay quanh Trái Đất: lực nào đóng vai lực hướng tâm`, o: ['a', 'b', 'c'], ow: { a: 40, c: 40 } },
    { t: 'Dạng 5 · Bài 1', de: `Ô tô ${m('1000\\ \\mathrm{kg}')} qua khúc cua phẳng bán kính ${nw(`${m('40\\ \\mathrm m')};`)} ma sát nghỉ cực đại bằng ${m('0{,}50')} lần trọng lượng; ${g10}; ${nw('1 m/s = 3,6 km/h.')}<br><b>a)</b> xe chạy ${m('54\\ \\mathrm{km/h}')}: lực hướng tâm cần có; xe có trượt không<br><b>b)</b> tốc độ lớn nhất qua cua an toàn (m/s; km/h)`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>'], ow: 22 },
    { t: 'Dạng 5 · Bài 2', de: `Đồng xu trên bàn xoay cách tâm ${nw(`${m('12\\ \\mathrm{cm}')};`)} ma sát nghỉ cực đại bằng ${m('0{,}40')} lần trọng lượng xu; ${g10}; ${nw(`${pi}.`)}<br><b>a)</b> bàn quay ${m('45')} vòng/phút: gia tốc hướng tâm của xu; xu có trượt không<br><b>b)</b> tốc độ góc lớn nhất để xu không trượt<br><b>c)</b> vẫn ${m('45')} vòng/phút: đặt xu xa tâm nhất bao nhiêu`, fig: H.xuTT(), fw: 40, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'], ow: 20 },
    nhap(8),
  ]],
  dap: [
    `D1·1: a) khác (ngược hướng) · b) có · c) từ M vào tâm · d) 0,20 m/s² &nbsp;|&nbsp; D1·2: a) không · b) 180° · c) vào tâm đường cong · d) 1,0 m/s² &nbsp;|&nbsp; D2·1: a) 0,523 rad/s · b) 3,14 m/s · c) 1,64 m/s² &nbsp;|&nbsp; D2·2: a) 50 vòng/s · b) 314 rad/s · c<sub>1</sub>) ≈ 9,86·10³ m/s² · c<sub>2</sub>) ≈ 1,0·10³ lần &nbsp;|&nbsp; D3·1: a<sub>1</sub>) 0,61 m/s² · a<sub>2</sub>) 1,84 m/s² · b) 3 · c) 3 &nbsp;|&nbsp; D3·2: a<sub>1</sub>) 5,0 m/s² · a<sub>2</sub>) 2,5 m/s² · b) 28 m/s`,
    `D4·1: a) ma sát nghỉ của đĩa · b) 3,14 rad/s · c) 0,148 N &nbsp;|&nbsp; D4·2: a) lực căng dây · b) 3,6 N · c) lực hấp dẫn của Trái Đất &nbsp;|&nbsp; D5·1: a<sub>1</sub>) 5625 N · a<sub>2</sub>) trượt (5625 N &gt; 5000 N) · b<sub>1</sub>) 14,1 m/s · b<sub>2</sub>) 51 km/h &nbsp;|&nbsp; D5·2: a<sub>1</sub>) 2,66 m/s² · a<sub>2</sub>) không trượt (2,66 &lt; 4) · b) 5,77 rad/s · c) 18 cm`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 2], kq: [[1, 2, 3], [4, 5]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'gia tốc hướng tâm 1·4 · tính thử 2·1 · lực hướng tâm 2·2 · đồng xu 2·3 · nút cao su 3·1 · bẫy 3·2 · bài toán mẫu 4·2 · dạng 1–3 → 6·1 · dạng 4–5 → 7·1',
  out: process.argv[2],
});
