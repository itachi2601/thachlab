// Ruột tập VL11 – Bài 18 · Điện trường đều (lesson id 37). Quyển Chương 3 lớp 11: bài 18 = tr. 25–36.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l11-bai18.mjs (toàn bộ SVG tự vẽ, không dùng ảnh Halliday). Nội dung theo bài web (book/cache/37.json, tải từ DB 12/11/2026):
// mục tiêu, dự đoán máy in phun, II.1–II.3, ba thí nghiệm (hạt bột, giấy dẫn điện, ống lệch tia), ba bẫy, Trả bài 6 câu,
// bài toán mẫu electron qua hai bản, thử thách phân tầng, 5 dạng bài tập mẫu.
// Đáp số Bài tương tự (tuongTu.dap) tính bằng Python 12/11/2026 (|e| = 1,6·10⁻¹⁹ C, mₑ = 9,1·10⁻³¹ kg).
// Chạy: node scripts/ruot-tap/l11-bai18.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl11-bai18.pdf
//       node scripts/ruot-tap/l11-bai18.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l11-bai18/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL11b18 as H } from './hinh-l11-bai18.mjs';

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
  const out = resolve(HERE, 'out/hinh-l11-bai18'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 18, lid: 37, ten: 'ĐIỆN TRƯỜNG ĐỀU', lop: 11, baiDau: 16, sub: 'Vật lí 11 · Chương 3: Điện trường' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const vE = m('\\vec E'), v0 = m('\\vec v_0');
const eM = nw(`${m('|e|=1{,}6\\cdot10^{-19}\\ \\mathrm C')}`), meM = nw(`${m('m_e=9{,}1\\cdot10^{-31}\\ \\mathrm{kg}')}`);
const hs = `Cho ${eM}, ${meM}.`;

// Bài tương tự xếp 1 cột, ô đáp số cuối dòng của ý (giống l10-bai23).
const ttCss = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm}.yo .oo{flex:none;display:flex;gap:3mm}.yo{line-height:1.35}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}.dap sup{line-height:0;font-size:.75em}</style>';
const p1 = `${ttCss}<section class="page">
${head('BÀI 18 · ĐIỆN TRƯỜNG ĐỀU', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Nêu đặc điểm <b>điện trường đều</b> giữa hai bản phẳng song song tích điện trái dấu`)}
${dong(`${ck}Dùng ${m('E=\\dfrac{U}{d}')}, đổi đúng đơn vị ${nw('V/m = N/C')}`)}
${dong(`${ck}Giải bài điện tích bay vào <b>vuông góc</b> đường sức: ngang đều, dọc nhanh dần đều, quỹ đạo parabol`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Giọt mực tích điện <b>âm</b> bay ngang vào khe. Bản trên dương, bản dưới âm. Giọt mực đi đường nào?</p>
<div class="fig-side" style="${fs(48)}"><div>
${opt('A', 'Đi thẳng, không lệch, vì bay vuông góc với đường sức')}
${opt('B', 'Cong dần lên phía bản dương, theo một đường parabol')}
${opt('C', 'Lệch lên theo một đường thẳng xiên')}
${opt('D', 'Cong dần xuống phía bản âm')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 2)}</div>
${H.mayIn()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(2)}</div>
${h3(4, 'II.1 · Điện trường đều giữa hai bản song song', '1·4')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div>Điện trường đều: ${vE} tại mọi điểm bằng nhau, cùng ${f(14)}, cùng ${f(14)}, cùng ${f(14)}.</div>
<div><b>Cách tạo:</b> hai bản kim loại phẳng ${f(22)}, rộng hơn nhiều so với ${m('d')}, tích điện ${f(18)}.</div>
<div><b>Đường sức:</b> thẳng, ${f(20)}, ${f(20)}.</div>
<div>Phương ${f(20)} với hai bản; chiều từ bản ${f(12)} sang bản ${f(12)}.</div>
<div>Gần mép bản, đường sức ${f(16)}: ở đó ${f(22)}.</div></div>
${H.veDuongSuc()}</div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('HẠT BỘT · E = U/d · HẠT BAY VUÔNG GÓC ĐƯỜNG SỨC')}
${h3(1, 'Thí nghiệm: hạt bột xếp hàng trong dầu', '2·1')}
<div class="card fig-side" style="${fs(40)};padding:1.2mm 3mm"><div>
<div><b>Làm:</b> rắc bột semolina vào khay dầu, nhúng hai lá đồng song song cách 4 cm, nối máy phát tĩnh điện rồi quay.</div>
<div><b>Quan sát:</b> giữa hai lá, hạt bột xếp thành ${f(40)}</div>
<div>Gần mép lá: ${f(40)}</div>
<div><b>Rút ra:</b> giữa hai bản (xa mép) là ${f(30)}</div></div>
${H.hatBot()}</div>
${h3(2, 'II.2 · Cường độ điện trường giữa hai bản', '2·2')}
<div class="card" style="padding:1.2mm 3mm">
<div style="display:flex;gap:6mm;align-items:center"><div style="font-size:1.15em">${m('E=')} ${f(16)}</div><div>Đơn vị: ${m('E')} ${f(12)} · ${m('U')} ${f(10)} · ${m('d')} (khoảng cách hai bản) ${f(10)}</div></div>
<div>${m('1\\ \\mathrm{V/m}=1')} ${f(12)}, vì ${nw(`${m('1\\ \\mathrm V=1')} ${f(12)}`)} ${nw(`${m('=1')} ${f(14)}`)}</div>
<div><b>Mẹo nhớ:</b> “Vôn trên mét”: đọc tên đơn vị là ra công thức.</div></div>
${h3(3, 'Thí nghiệm đo: dò điện thế trên giấy dẫn điện', '2·3')}
<div class="fig-side" style="${fs(44)}"><div>
<table class="tbl-ct"><tr><th>${m('x\\ (\\mathrm{cm})')}</th><th>${m('V\\ (\\mathrm V)')}</th><th>${m('V/x\\ (\\mathrm{V/m})')}</th></tr>
<tr><td>1,0</td><td>1,5</td><td></td></tr>
<tr><td>2,0</td><td>3,0</td><td></td></tr>
<tr><td>3,0</td><td>4,5</td><td></td></tr>
<tr><td>4,0</td><td>6,0</td><td></td></tr>
<tr><td>5,0</td><td>7,5</td><td></td></tr></table>
<div>Nhớ đổi ${m('x')} ra mét. So với ${nw(`${m('U/d=')} ${f(16)}&nbsp;V/m`)}</div></div>
${H.giayDan()}</div>
<div class="card" style="margin-top:0;padding:.8mm 3mm">
<div>Vôn kế sai số ${nw(m('\\pm 0{,}1\\ \\mathrm V'))}. Tính ${m('E')} từ hàng ${nw(`${m('x=')} ${f(12)}&nbsp;cm`)} là chính xác nhất, vì:</div>${lines(1)}</div>
${h3(4, 'II.3 · Điện tích bay vào vuông góc đường sức', '2·4')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div>Chân không, bỏ qua trọng lực (khi ${m('mg')} rất nhỏ so với ${m('|q|E')}). Gốc ${m('O')} tại điểm vào; ${m('Oy')} cùng chiều lực điện.</div>
<div>Lực điện: ${nw(`${m('F=')} ${f(14)}`)}, không đổi, ${f(16)} ${v0}</div>
<div>Gia tốc: ${nw(`${m('a=')} ${f(24)}`)}</div>
<div>Theo ${m('Ox')}: ${f(20)} &nbsp;${nw(`${m('x=')} ${f(12)}`)}</div>
<div>Theo ${m('Oy')}: ${f(26)} &nbsp;${nw(`${m('y=')} ${f(12)}`)}</div>
<div>Quỹ đạo (parabol): ${m('y=')} ${f(32)} ${m('\\cdot x^2')}</div>
<div>${m('q\\gt 0')} lệch về bản ${f(12)} · ${m('q\\lt 0')} (electron) lệch về bản ${f(12)}</div>
<div><b>Mẹo:</b> “Ném ngang, đổi ${m('g')} thành ${m('a')}”.</div></div>
${H.hatBay()}</div>
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('ỐNG LỆCH TIA · BẪY · TRẢ BÀI')}
${h3(1, 'Thí nghiệm: ống lệch tia điện tử', '3·1')}
<div class="fig-side" style="${fs(46)}"><div>
<table class="tbl-ct"><tr><th style="width:24mm">Làm</th><th>Tia electron đi thế nào?</th></tr>
<tr><td>${m('U=0')}</td><td></td></tr>
<tr><td>Có ${m('U')}</td><td></td></tr>
<tr><td>${m('U')} gấp đôi</td><td></td></tr>
<tr><td>Đảo cực</td><td></td></tr></table>
<div style="margin-top:.6mm"><b>Rút ra:</b> electron lệch về bản ${f(14)} theo ${f(18)}; độ lệch ${f(25)}</div></div>
${H.ongLech()}</div>
<div class="card soft" style="margin-top:.8mm;padding:1mm 3mm">Bay vào <b>song song</b> với đường sức: hạt đi ${f(18)}; lực cùng chiều vận tốc thì ${f(22)}, ngược chiều thì ${f(22)}.</div>
${h3(2, 'III · Ba cái bẫy hay sập', '3·2')}
<div class="card" style="padding:1mm 3mm">
<div class="trap">${ck}<span><b>“Lực điện luôn cùng chiều đường sức.”</b> Chỉ đúng với ${m('q\\gt 0')}; electron chịu lực ngược chiều ${vE}.</span></div>
<div class="trap">${ck}<span><b>“Ra khỏi hai bản vẫn cong tiếp.”</b> Hết trường là hết lực: hạt đi thẳng theo vận tốc lúc ra.</span></div>
<div class="trap">${ck}<span><b>“Để ${m('d')} bằng cm.”</b> ${nw('100 V')}, ${nw('2 cm')}: ${m('E=100/0{,}02=5000\\ \\mathrm{V/m}')}, không phải 50. ${m('E=U/d')} chỉ dùng cho trường đều.</span></div></div>
${h3(3, 'IV · Trả bài 6 câu', '3·3')}
${box(`${tb('1. Điện trường đều là gì? Tạo ra bằng cách nào?')}${lines(2)}
${tb('2. Đường sức giữa hai bản có đặc điểm gì?')}${lines(1)}
${tb('3. Công thức E theo U và d, đơn vị. Vì sao V/m = N/C?')}${lines(2)}
${tb('4. Bay vuông góc đường sức: hai chuyển động thành phần?')}${lines(2)}
${tb('5. Phương trình quỹ đạo? Lệch về bản nào?')}${lines(1)}
${tb('6. Ra khỏi hai bản thì đi thế nào? Khi nào bỏ qua trọng lực?')}${lines(1)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/6 câu · chưa thuộc: ${f(25)} ${nw(`→ đọc lại ô ${f(12)} Tập`)}</div>
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('LÀM NHANH · BÀI TOÁN MẪU')}
${h3(1, 'Làm nhanh', '4·1')}
${box(cau(`<b>Câu 1.</b> Hai bản cách nhau ${nw('4 mm')}, ${nw(m('U=12\\ \\mathrm V'))}. Tính ${m('E')}.`, 1)
 + cau(`<b>Câu 2.</b> Proton bay ngang vào giữa hai bản nằm ngang; bản trên âm, bản dưới dương. Proton lệch về đâu, theo đường gì?`, 1))}
${h3(2, 'V · Bài toán mẫu: electron bay qua hai bản', '4·2')}
<div class="card soft" style="padding:1.2mm 3mm">Electron bay vào chính giữa hai bản kim loại phẳng nằm ngang, song song với hai bản, tốc độ ${nw(m('v_0=2{,}0\\cdot10^{7}\\ \\mathrm{m/s}'))}. Hai bản dài ${nw(m('L=5{,}0\\ \\mathrm{cm}'))}, cách nhau ${nw(m('d=2{,}0\\ \\mathrm{cm}'))}, ${nw(m('U=91\\ \\mathrm V'))}, bản trên dương. ${hs}
<div><b>a)</b> Tính ${m('E')} giữa hai bản.</div><div><b>b)</b> Tính gia tốc electron. Nó lệch về bản nào?</div><div><b>c)</b> Tính độ lệch khi ra khỏi hai bản. Electron có chạm bản không?</div></div>
${h3(3, 'Phân tích đề')}
<table><tr><th style="width:50mm">Câu trong đề</th><th>Dữ liệu → kiến thức</th></tr>
<tr><td>“song song với hai bản”</td><td>${m('\\vec v_0\\perp\\vec E')} → ném ngang: ${m('Ox')} đều, ${m('Oy')} nhanh dần đều</td></tr>
<tr><td style="height:6mm">“chính giữa hai bản”</td><td></td></tr>
<tr><td style="height:6mm">“dài 5,0 cm”, ${m('v_0')}</td><td></td></tr>
<tr><td style="height:6mm">“cách nhau 2,0 cm, U = 91 V”</td><td></td></tr>
<tr><td style="height:6mm">“bản trên tích điện dương”</td><td></td></tr>
<tr><td style="height:6mm">Dữ kiện ngầm: “electron”</td><td></td></tr></table>
${h3(4, 'Giải')}
<div class="fig-side" style="${fs(52)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl(`a) ${m('E')}:`, 1)}${wl(`b) ${m('F')}, ${m('a')}, chiều lệch:`, 2)}${wl(`c) ${m('t=L/v_0')}, ${m('y=\\tfrac12at^2')}:`, 2)}${wl('So với khoảng tới bản, kết luận:', 1)}</div>${H.baiMau()}</div>
${h3(5, 'Điền bước còn thiếu: cùng đề, U = 182 V')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div class="ln"><b>Bước 1 (cho sẵn):</b> ${m('E=182/0{,}020=9100\\ \\mathrm{V/m}')}</div>
${wl(`Bước 2: ${m('a=')}`, 1)}
<div class="ln"><b>Bước 3 (cho sẵn):</b> ${m('t=2{,}5\\cdot10^{-9}\\ \\mathrm s')}, không đổi vì ${m('L')}, ${m('v_0')} giữ nguyên</div>
${wl(`Bước 4: ${m('y=')} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Có chạm bản không?`, 1)}</div>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TẬP VỀ NHÀ · TỰ KIỂM TRA · THỬ THÁCH · MANG VỀ')}
${K.btvn()}
${h3(2, 'Kết quả tự kiểm tra (8 câu, đề chiếu trên lớp)', '5·2')}
${rkHai([1, 2, 3, 4], [5, 6, 7, 8])}
${h3(3, 'Thử thách phân tầng', '5·3')}
<div class="fig-side" style="${fs(46)}">${box(wl(`${m('\\bigstar')} Hai bản cách nhau ${nw('5,0 mm')}, ${nw(m('U=50\\ \\mathrm V'))}. Tính ${m('E')}.`, 2)
 + wl(`${m('\\bigstar\\bigstar')} Trong bài mẫu, tính ${m('v_y')} lúc electron ra khỏi bản và góc lệch ${m('\\alpha')} so với ${v0}.`, 3)
 + wl(`${m('\\bigstar\\bigstar\\bigstar')} Đặt màn cách mép ra của hai bản ${nw(m('D=20\\ \\mathrm{cm}'))}. Vệt sáng lệch khỏi điểm giữa màn bao nhiêu?`, 4))}${H.manHinh()}</div>
${h3(4, 'Thử sức đổi số, đổi chiều (bài toán mẫu)', '5·4')}
${box(wl(`Giữ ${nw('U = 91 V')}, ${m('L')}, ${m('d')}, nhưng ${nw(m('v_0=4{,}0\\cdot10^{7}\\ \\mathrm{m/s}'))}. Độ lệch khi ra khỏi bản? Vì sao bay nhanh lại lệch ít?`, 3)
 + wl('Đảo cực hai bản (bản dưới dương): E, a, t, độ lệch và phía lệch thay đổi thế nào?', 2))}
${h3(5, 'VI · Mang về: điều em dễ quên nhất', '5·5')}
${box(wl('1.', 2) + wl('2.', 2) + wl('3.', 2))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Hai bản song song: E, lực điện và chiều của lực',
    de: `Hai bản phẳng song song nằm ngang cách nhau ${nw(m('d=8{,}0\\ \\mathrm{mm}'))}, ${nw(m('U=240\\ \\mathrm V'))}; bản trên dương. Hạt bụi ${nw(m('q=-2{,}5\\ \\mathrm{nC}'))} ở giữa, xa mép; bỏ qua trọng lực.<br><b>a)</b> cường độ điện trường<br><b>b)</b> độ lớn lực điện lên hạt bụi; lực hướng lên hay xuống<br><b>c)</b> giữ ${m('U')}, giảm ${m('d')} còn một nửa: lực điện thay đổi thế nào`,
    nd: `đổi ${m('d')} ra ${f(12)}; ${m('q\\lt 0')} nên lực ${f(25)} chiều ${vE}`, a: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], gi: 3 },
  { t: 'Dạng 2 · Trung bình · Bay dọc đường sức: dừng rồi quay lại',
    de: `Electron bay vào điện trường đều ${nw(m('E=1820\\ \\mathrm{V/m}'))} dọc đường sức, cùng chiều ${vE}, ${nw(m('v_0=8{,}0\\cdot10^{6}\\ \\mathrm{m/s}'))}. Trường đủ rộng, bỏ qua trọng lực; ${m('|e|')}, ${m('m_e')} như bài toán mẫu.<br><b>a)</b> lực cùng hay ngược chiều vận tốc; độ lớn gia tốc<br><b>b)</b> quãng đường tới khi dừng<br><b>c)</b> sau đó electron đi thế nào; thời gian từ lúc vào tới khi trở lại điểm vào`,
    nd: `lực ngược chiều ${v0} ⇒ chuyển động ${f(25)}; dùng ${nw(m('v^2-v_0^2=2as'))}`, a: ['a', 'b', 'c'], gi: 3 },
  { t: 'Dạng 3 · Trung bình · Bay vuông góc đường sức: có chạm bản?',
    de: `Electron bay vào chính giữa hai bản nằm ngang, song song với bản, ${nw(m('v_0=1{,}0\\cdot10^{7}\\ \\mathrm{m/s}'))}. Bản dài ${nw(m('L=4{,}5\\ \\mathrm{cm}'))}, cách nhau ${nw(m('d=1{,}0\\ \\mathrm{cm}'))}, ${nw(m('U=36{,}4\\ \\mathrm V'))}; bản <b>dưới</b> dương; ${m('|e|')}, ${m('m_e')} như bài toán mẫu.<br><b>a)</b> ${m('E')}, gia tốc; lệch về bản nào<br><b>b)</b> electron có ra khỏi hai bản không; nếu không, chạm bản ở điểm cách mép vào bao nhiêu cm`,
    nd: `tính độ lệch nếu bay hết ${m('L')}, so với ${f(14)}; chạm thì giải ${nw(`${m('\\tfrac12at^2=')} ${f(12)}`)}`, a: ['a', 'b'], gi: 3, fig: H.d3Cham(''), cot: 2 },
  { t: 'Dạng 4 · Khó · Ra khỏi hai bản: góc lệch và vệt trên giấy',
    de: `Giọt mực máy in phun ${nw(m('m=1{,}0\\cdot10^{-10}\\ \\mathrm{kg}'))}, ${nw(m('q=-2{,}0\\cdot10^{-12}\\ \\mathrm C'))} bay ngang vào chính giữa hai bản với ${nw(m('v_0=20\\ \\mathrm{m/s}'))}. Bản dài ${nw(m('L=1{,}0\\ \\mathrm{cm}'))}, cách nhau ${nw(m('d=4{,}0\\ \\mathrm{mm}'))}, ${nw(m('U=1600\\ \\mathrm V'))}, bản trên dương. Ra khỏi bản, giọt bay thêm ${nw(m('D=2{,}0\\ \\mathrm{cm}'))} theo phương ngang rồi chạm giấy. Bỏ qua trọng lực, lực cản.<br><b>a)</b> gia tốc giọt mực giữa hai bản<br><b>b)</b> ${m('v_y')} và góc lệch ${m('\\alpha')} lúc ra khỏi bản<br><b>c)</b> khoảng cách ${m('Y')} từ điểm chạm giấy tới đường bay ban đầu`,
    nd: `${nw(m('\\tan\\alpha=v_y/v_0'))}; ngoài bản hết lực ⇒ đi ${f(16)}; ${nw(`${m('Y=y+')} ${f(18)}`)}`, a: ['a', 'b', 'c'], gi: 6, fig: H.d4Giay(), cot: 3 },
  { t: 'Dạng 5 · Khó · Bài ngược: U lớn nhất để electron còn ra khỏi hai bản',
    de: `Electron bay vào chính giữa hai bản nằm ngang, song song với bản, ${nw(m('v_0=1{,}6\\cdot10^{7}\\ \\mathrm{m/s}'))}. Bản dài ${nw(m('L=4{,}0\\ \\mathrm{cm}'))}, cách nhau ${nw(m('d=2{,}0\\ \\mathrm{cm}'))}; bản trên dương. Bỏ qua trọng lực; ${eM}, ${meM}.<br><b>a)</b> hiệu điện thế lớn nhất để electron còn bay ra<br><b>b)</b> đặt ${nw(m('U=546\\ \\mathrm V'))}: có ra không; nếu không, chạm bản nào, cách mép vào bao nhiêu cm`,
    nd: `giới hạn: sượt mép bản khi ${nw(`${m('x=L')}: ${m('y=')} ${f(12)}`)}; ${m('t=L/v_0')} không phụ thuộc ${m('U')}`, a: ['a', 'b'], gi: 7, fig: H.d5SuotMep(), cot: 2 },
];

// Bài tương tự: mỗi dạng 2 bài, đáp số tính bằng Python 12/11/2026, làm tròn 2–3 chữ số có nghĩa. Giải vào vở (vo: true).
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
    { t: 'Dạng 1 · Bài 1', de: `Hai bản nằm ngang cách nhau ${nw(m('5{,}0\\ \\mathrm{mm}'))}, ${nw(`${m('U=150\\ \\mathrm V')};`)} bản <b>dưới</b> dương. Hạt bụi ${nw(m('q=+4{,}0\\ \\mathrm{nC}'))} ở giữa; bỏ qua trọng lực.<br><b>a)</b> cường độ điện trường<br><b>b)</b> độ lớn lực điện; lực hướng lên hay xuống<br><b>c)</b> giữ ${m('d')}, tăng ${m('U')} gấp 3: độ lớn lực điện`, o: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'] },
    { t: 'Dạng 1 · Bài 2', de: `Hạt bụi ${nw(m('q=-1{,}6\\ \\mathrm{nC}'))} ở giữa hai bản nằm ngang cách nhau ${nw(m('1{,}2\\ \\mathrm{cm}'))}, chịu lực ${nw(`${m('4{,}8\\cdot10^{-5}\\ \\mathrm N')}.`)} Bản trên dương.<br><b>a)</b> cường độ điện trường<br><b>b)</b> hiệu điện thế giữa hai bản`, o: ['a', 'b'] },
    { t: 'Dạng 2 · Bài 1', de: `Electron bay vào trường đều ${nw(m('E=910\\ \\mathrm{V/m}'))} dọc đường sức, cùng chiều ${vE}, ${nw(`${m('v_0=4{,}0\\cdot10^{6}\\ \\mathrm{m/s}')}.`)} ${hs}<br><b>a)</b> chiều lực so với vận tốc; độ lớn gia tốc<br><b>b)</b> quãng đường tới khi dừng<br><b>c)</b> thời gian từ lúc vào tới khi trở lại điểm vào`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'] },
    { t: 'Dạng 2 · Bài 2', de: `Electron rời bản âm (vận tốc đầu bằng 0), bay thẳng tới bản dương. Hai bản cách nhau ${nw(m('2{,}0\\ \\mathrm{cm}'))}, ${nw(`${m('U=182\\ \\mathrm V')}.`)} (${m('|e|')}, ${m('m_e')} như bài 1.)<br><b>a)</b> cường độ điện trường; gia tốc<br><b>b)</b> thời gian bay tới bản dương<br><b>c)</b> tốc độ khi chạm bản dương`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'] },
    { t: 'Dạng 3 · Bài 1', de: `Electron bay vào chính giữa hai bản nằm ngang, song song với bản, ${nw(`${m('v_0=2{,}0\\cdot10^{7}\\ \\mathrm{m/s}')}.`)} Bản dài ${nw(m('6{,}0\\ \\mathrm{cm}'))}, cách nhau ${nw(m('2{,}0\\ \\mathrm{cm}'))}, ${nw(`${m('U=45{,}5\\ \\mathrm V')};`)} bản trên dương. (${m('|e|')}, ${m('m_e')} như D2·1.)<br><b>a)</b> gia tốc; lệch về bản nào<br><b>b)</b> độ lệch khi ra khỏi bản; có chạm bản không`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>'], ow: 22 },
    { t: 'Dạng 3 · Bài 2', de: `Electron bay vào chính giữa, song song với hai bản dài ${nw(m('5{,}0\\ \\mathrm{cm}'))}, cách nhau ${nw(m('1{,}0\\ \\mathrm{cm}'))}, ${nw(`${m('U=45{,}5\\ \\mathrm V')};`)} bản <b>dưới</b> dương; ${nw(`${m('v_0=1{,}0\\cdot10^{7}\\ \\mathrm{m/s}')}.`)} (${m('|e|')}, ${m('m_e')} như D2·1.)<br><b>a)</b> gia tốc; độ lệch nếu bay hết chiều dài bản<br><b>b)</b> có ra khỏi bản không? Chạm thì chạm bản nào, cách mép vào bao xa`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b'], ow: 28 },
  ], [
    { t: 'Dạng 4 · Bài 1', de: `Giọt mực ${nw(m('m=2{,}0\\cdot10^{-10}\\ \\mathrm{kg}'))}, ${nw(m('q=-4{,}0\\cdot10^{-12}\\ \\mathrm C'))} bay ngang vào chính giữa hai bản, ${nw(`${m('v_0=25\\ \\mathrm{m/s}')}.`)} Bản dài ${nw(m('1{,}0\\ \\mathrm{cm}'))}, cách nhau ${nw(m('5{,}0\\ \\mathrm{mm}'))}, ${nw(`${m('U=1250\\ \\mathrm V')};`)} ra khỏi bản bay thêm ${nw(m('D=2{,}0\\ \\mathrm{cm}'))} tới giấy.<br><b>a)</b> gia tốc<br><b>b)</b> ${m('v_y')}, góc lệch ${m('\\alpha')} lúc ra khỏi bản<br><b>c)</b> khoảng cách ${m('Y')} trên giấy`, fig: H.d4Giay('L = 1,0 cm, D = 2,0 cm. Y = ?'), fw: 44, o: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], ow: 18 },
    { t: 'Dạng 4 · Bài 2', de: `Electron bay vào chính giữa hai bản dài ${nw(m('4{,}0\\ \\mathrm{cm}'))}, cách nhau ${nw(m('2{,}0\\ \\mathrm{cm}'))}, ${nw(`${m('U=91\\ \\mathrm V')},`)} với ${nw(`${m('v_0=2{,}0\\cdot10^{7}\\ \\mathrm{m/s}')}.`)} Màn đặt cách mép ra ${nw(`${m('D=16\\ \\mathrm{cm}')}.`)} ${hs}<br><b>a)</b> độ lệch khi ra khỏi bản<br><b>b)</b> ${m('\\tan\\alpha')} lúc ra khỏi bản<br><b>c)</b> độ lệch ${m('Y')} của vệt sáng trên màn`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 5 · Bài 1', de: `Electron bay vào chính giữa hai bản dài ${nw(m('5{,}0\\ \\mathrm{cm}'))}, cách nhau ${nw(m('1{,}0\\ \\mathrm{cm}'))}, song song với bản, ${nw(`${m('v_0=2{,}0\\cdot10^{7}\\ \\mathrm{m/s}')};`)} bản trên dương. ${hs}<br><b>a)</b> hiệu điện thế lớn nhất để electron còn ra khỏi bản<br><b>b)</b> đặt ${nw(m('U=182\\ \\mathrm V'))}: chạm bản nào, cách mép vào bao nhiêu cm`, o: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>'], ow: 22 },
    { t: 'Dạng 5 · Bài 2', de: `Hai bản dài ${nw(m('4{,}0\\ \\mathrm{cm}'))}, cách nhau ${nw(m('1{,}0\\ \\mathrm{cm}'))}, ${nw(`${m('U=36{,}4\\ \\mathrm V')}.`)} Electron bay vào chính giữa, song song với bản. (${m('|e|')}, ${m('m_e')} như bài 1.)<br><b>a)</b> gia tốc của electron<br><b>b)</b> tốc độ ${m('v_0')} nhỏ nhất để electron còn ra khỏi hai bản`, o: ['a', 'b'], ow: 30 },
    nhap(6),
  ]],
  dap: [
    `D1·1: a) 3,0·10<sup>4</sup> V/m · b<sub>1</sub>) 1,2·10<sup>−4</sup> N · b<sub>2</sub>) lên · c) 3,6·10<sup>−4</sup> N &nbsp;|&nbsp; D1·2: a) 3,0·10<sup>4</sup> V/m · b) 360 V &nbsp;|&nbsp; D2·1: a<sub>1</sub>) ngược chiều · a<sub>2</sub>) 1,6·10<sup>14</sup> m/s<sup>2</sup> · b) 5,0 cm · c) 50 ns &nbsp;|&nbsp; D2·2: a<sub>1</sub>) 9100 V/m · a<sub>2</sub>) 1,6·10<sup>15</sup> m/s<sup>2</sup> · b) 5,0 ns · c) 8,0·10<sup>6</sup> m/s &nbsp;|&nbsp; D3·1: a<sub>1</sub>) 4,0·10<sup>14</sup> m/s<sup>2</sup> · a<sub>2</sub>) bản trên · b<sub>1</sub>) 1,8 mm · b<sub>2</sub>) không chạm &nbsp;|&nbsp; D3·2: a<sub>1</sub>) 8,0·10<sup>14</sup> m/s<sup>2</sup> · a<sub>2</sub>) 10 mm · b) bản dưới, 3,5 cm`,
    `D4·1: a) 5,0·10<sup>3</sup> m/s<sup>2</sup> · b<sub>1</sub>) 2,0 m/s · b<sub>2</sub>) 4,6° · c) 2,0 mm &nbsp;|&nbsp; D4·2: a) 1,6 mm · b) 0,080 · c) 14,4 mm &nbsp;|&nbsp; D5·1: a) 91 V · b<sub>1</sub>) bản trên · b<sub>2</sub>) 3,5 cm &nbsp;|&nbsp; D5·2: a) 6,4·10<sup>14</sup> m/s<sup>2</sup> · b) ≈ 1,01·10<sup>7</sup> m/s`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 2], kq: [[1, 2, 3], [4, 5]], khoNhat: true },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'điện trường đều 1·4 · hạt bột 2·1 · E = U/d 2·2 · giấy dẫn điện 2·3 · bay vuông góc 2·4 · ống lệch tia 3·1 · bẫy 3·2 · bài toán mẫu 4·2 · dạng 1–3 → 6·1 · dạng 4–5 → 7·1',
  out: process.argv[2],
});
