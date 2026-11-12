// Ruột tập VL11 – Bài 16 · Lực tương tác giữa hai điện tích (lesson id 35). Quyển Chương 3 lớp 11: bài 16 = tr. 1–12.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l11-bai16.mjs (toàn bộ SVG tự vẽ, không dùng ảnh Halliday). Nội dung theo bài web (book/cache/35.json, tải từ DB 12/11/2026):
// mục tiêu, dự đoán tia lửa ở siêu thị, II.1–II.5, thí nghiệm thước nhựa + cân điện tử, ba bẫy, Trả bài 6 câu, bài toán mẫu hai quả
// cầu treo, thử thách ⭐–⭐⭐⭐, 5 dạng bài tập mẫu. Đáp số Bài tương tự (tuongTu.dap) tính bằng Python 12/11/2026.
// Chạy: node scripts/ruot-tap/l11-bai16.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl11-bai16.pdf
//       node scripts/ruot-tap/l11-bai16.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l11-bai16/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL11b16 as H } from './hinh-l11-bai16.mjs';

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
  const out = resolve(HERE, 'out/hinh-l11-bai16'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 16, lid: 35, ten: 'LỰC TƯƠNG TÁC GIỮA HAI ĐIỆN TÍCH', lop: 11, baiDau: 16, sub: 'Vật lí 11 · Chương 3: Điện trường' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const kC = nw(m('k=9\\cdot10^9\\ \\mathrm{N{\\cdot}m^2/C^2}'));
const eC = nw(m('|e|=1{,}6\\cdot10^{-19}\\ \\mathrm C'));
const g10 = nw(m('g=10\\ \\mathrm{m/s^2}'));
const q1 = m('q_1'), q2 = m('q_2'), q0 = m('q_0'), r1 = m('r_1'), r2 = m('r_2'), eps = m('\\varepsilon'), al = m('\\alpha');
const nC = (s) => nw(m(`${s}\\ \\mathrm{nC}`)), uC = (s) => nw(m(`${s}\\ \\mu\\mathrm C`)), cm = (s) => nw(m(`${s}\\ \\mathrm{cm}`));

// Bài tương tự 1 cột, ô đáp số cuối dòng của ý (cùng cách l10-bai23).
const ttCss = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';

const p1 = `${ttCss}<section class="page">
${head('BÀI 16 · LỰC TƯƠNG TÁC GIỮA HAI ĐIỆN TÍCH', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Giải thích ba cách nhiễm điện bằng <b>thuyết electron</b>; dùng <b>bảo toàn điện tích</b>`)}
${dong(`${ck}Phát biểu và tính ${m('F=k\\dfrac{|q_1q_2|}{\\varepsilon r^2}')}, đổi đúng đơn vị SI`)}
${dong(`${ck}Tổng hợp lực điện lên một điện tích; tìm vị trí để điện tích <b>cân bằng</b>`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Đẩy xe qua sàn nhựa ở siêu thị, chạm tay vào kệ sắt: tách! Điện làm em bị giật đến từ đâu?</p>
<div class="fig-side" style="${fs(42)}"><div>
${opt('A', 'Có sẵn trong sàn nhà, truyền qua đế giày vào người')}
${opt('B', 'Đế giày, quần áo cọ xát làm electron dời từ vật này sang vật kia')}
${opt('C', 'Cơ thể tự sinh ra điện tích mới mỗi khi bước đi')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 1)}</div>
${H.sieuThi()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Nhiễm điện và thuyết electron', '1·4')}
<div class="card" style="padding:1.2mm 3mm">
<div>Vật nhiễm điện: ${f(25)} hoặc đẩy vật khác, hoặc phóng ${f(25)}.</div>
<div>Nguyên tử bình thường trung hoà: tổng điện tích ${f(14)}. Electron nhẹ, linh động, dễ ${f(25)}.</div>
<div>Thừa electron: vật ${f(16)} · thiếu electron: vật ${f(16)} · ${nw(`${m('|q|=')} ${f(12)}`)}</div>
<div>Điện tích luôn là bội của ${nw(`${m('|e|=')} ${f(22)}&nbsp;C`)}</div>
<div style="margin-top:.6mm"><b>Ví dụ:</b> thanh thuỷ tinh cọ lụa tích điện ${nC('+13')}. Bao nhiêu electron đã rời thanh? Lụa nhiễm điện gì?</div>${lines(2)}</div>
<table>
<tr><th style="width:30mm">Cách nhiễm điện</th><th>Kết quả</th><th>Electron đi đâu</th></tr>
<tr><td style="height:7mm">Cọ xát</td><td></td><td></td></tr>
<tr><td style="height:7mm">Tiếp xúc</td><td></td><td></td></tr>
<tr><td style="height:7mm">Hưởng ứng</td><td></td><td></td></tr></table>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('BẢO TOÀN ĐIỆN TÍCH · ĐỊNH LUẬT COULOMB')}
${h3(1, 'Bảo toàn điện tích', '2·1')}
<div class="card" style="padding:1.2mm 3mm">
<div>Hệ cô lập: hệ không ${f(40)} với bên ngoài.</div>
<div>Trong hệ cô lập, tổng ${f(16)} điện tích ${f(20)} (cộng giữ nguyên dấu + và −).</div>
<div>${m('n')} quả cầu giống hệt chạm nhau rồi tách ra: ${m("q'=")} <span class="fill" style="min-width:30mm;height:10mm"></span></div>
</div>
${h3(2, 'Thí nghiệm: thước nhựa, giấy vụn, lon nhôm', '2·2')}
<div class="card fig-side" style="${fs(42)};padding:1.2mm 3mm"><div>
<div><b>Làm:</b> cọ thước nhựa vào tóc khô, đưa lại gần giấy vụn; rồi đưa lại gần (không chạm) lon nhôm rỗng nằm ngang.</div>
<div><b>Quan sát:</b> giấy vụn ${f(32)}; lon nhôm ${f(32)}</div>
<div><b>Rút ra:</b> thước nhiễm điện do ${f(18)}; lon nhiễm điện do ${f(18)}: đầu gần thước mang điện ${f(14)} dấu, ở gần hơn nên bị hút mạnh hơn đầu xa bị đẩy.</div></div>
${H.lonNhom()}</div>
${h3(3, 'II.2 · Định luật Coulomb', '2·3')}
<div class="card fig-side" style="${fs(44)};padding:1.2mm 3mm"><div>
<div>Điện tích điểm: vật tích điện rất ${f(14)} so với khoảng cách đang xét.</div>
<div>Cùng dấu thì ${f(14)}, trái dấu thì ${f(14)}.</div>
<div>Lực có phương ${f(40)}; độ lớn tỉ lệ thuận với ${f(16)}, tỉ lệ nghịch với ${f(16)}.</div>
<div style="margin:.8mm 0">${m('F=')} <span class="fill" style="min-width:24mm;height:10mm"></span> &nbsp; ${m('k=')} ${f(22)}</div>
<div>${eps}: hằng số ${f(18)}, ${nw(`${m('\\varepsilon\\ge')} ${f(8)}`)}; chân không ${nw(`${m('\\varepsilon=')} ${f(8)}`)}, không khí ${nw(`${m('\\varepsilon\\approx')} ${f(8)}`)}</div>
<div>Trong điện môi (dầu, thuỷ tinh, nước nguyên chất) lực ${f(14)} ${eps} lần.</div>
<div>Chỉ đúng cho điện tích điểm hoặc quả cầu tích điện đều (coi điện tích đặt ở ${f(12)}).</div></div>
${H.haiDienTich()}</div>
${h3(4, 'Làm nhanh', '2·4')}
${box(cau(`<b>Câu 1.</b> ${m('r')} tăng 2 lần, ${m('|q_1|')} giảm 2 lần thì ${m('F')} tăng hay giảm bao nhiêu lần?`, 1)
 + cau(`<b>Câu 2.</b> Hai điện tích trong không khí hút nhau lực ${nw(m('8\\ \\mathrm N'))}. Đặt vào dầu ${nw(m('\\varepsilon=2'))} và giảm khoảng cách còn một nửa: lực bằng bao nhiêu?`, 1))}
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('LỰC GIẢM THEO r² · TỔNG HỢP LỰC · CÂN BẰNG')}
${h3(1, 'II.3 · Thí nghiệm đo: cân điện tử “cân” lực điện', '3·1')}
<div class="fig-side" style="${fs(36)}"><div>
<div style="font-size:var(--fs-sm);line-height:1.35;margin-bottom:.6mm">Quả cầu A ${nC('+20')} đặt trên cân (đã trừ bì); hạ quả B ${nC('+20')} thẳng phía trên A. ${nw(`${m('F=')}(số cân, kg)${m('\\cdot g')},`)} ${nw(m('g=9{,}8\\ \\mathrm{m/s^2}'))}. Hàng đầu: ${m('0{,}92\\cdot10^{-3}\\cdot9{,}8\\cdot0{,}02^2\\approx3{,}61\\cdot10^{-6}')}</div>
<table class="tbl-ct"><tr><th>${m('r')} (cm)</th><th>2</th><th>3</th><th>4</th><th>5</th><th>6</th></tr>
<tr><td>Số cân (g)</td><td>0,92</td><td>0,41</td><td>0,23</td><td>0,15</td><td>0,10</td></tr>
<tr><td>${m('Fr^2')} (${m('10^{-6}')} N·m²)</td><td>3,61</td><td></td><td></td><td></td><td></td></tr></table>
<div style="margin-top:.6mm"><b>Rút ra:</b> tích ${m('Fr^2')} ${f(25)} nên ${m('F')} tỉ lệ nghịch với ${f(12)}.</div></div>
${H.canDien()}</div>
${h3(2, 'II.4 · Tổng hợp lực điện', '3·2')}
<div class="fig-side" style="${fs(44)}"><div>
<div>${q0} chịu lực của nhiều điện tích: ${m('\\vec F=')} ${f(30)}. Tính từng lực bằng Coulomb, vẽ đúng chiều hút/đẩy.</div>
<table style="margin-top:.6mm"><tr><th style="width:44mm">Hai lực</th><th>Hợp lực</th></tr>
<tr><td>Cùng chiều</td><td></td></tr><tr><td>Ngược chiều</td><td></td></tr><tr><td>Vuông góc</td><td></td></tr>
<tr><td>Góc ${al} bất kì (chung gốc tại ${q0})</td><td></td></tr><tr><td>${m('F_1=F_2')}, góc ${al}</td><td></td></tr></table>
<div style="margin-top:.6mm">Cùng hút/cùng đẩy: ${nw(`${al} = ${f(16)}`)} · một hút, một đẩy: ${nw(`${al} = ${f(24)}`)}</div></div>
${H.tongHop()}</div>
${h3(3, 'II.5 · Cân bằng của điện tích chịu nhiều lực', '3·3')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div>${q0} đứng yên khi ${m('\\vec F_{10}+\\vec F_{20}=')} ${f(10)}: hai lực cùng ${f(14)}, ngược ${f(14)}, bằng ${f(14)}.</div>
<div>C nằm trên ${f(25)}, gần điện tích có độ lớn ${f(14)}.</div>
<div>Cùng dấu: C ở ${f(18)} đoạn AB, ${nw(`${m('r_1+r_2=')} ${f(10)}`)}</div>
<div>Trái dấu: C ở ${f(18)} đoạn AB, ${nw(`${m('|r_1-r_2|=')} ${f(10)}`)}</div>
<div>${m('\\dfrac{r_1}{r_2}=')} <span class="fill" style="min-width:20mm;height:10mm"></span>; kết quả ${f(16)} phụ thuộc dấu và độ lớn của ${q0}.</div></div>
${H.canBang()}</div>
${h3(4, 'Làm nhanh', '3·4')}
${box(cau(`${m('AB=8')} cm, ${m('q_1=+9\\ \\mu\\mathrm C')} tại A, ${m('q_2=+1\\ \\mu\\mathrm C')} tại B. Tìm ${m('CA')}, ${m('CB')} để ${q0} cân bằng.`, 1))}
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('BA CÁI BẪY · TRẢ BÀI · TỰ KIỂM TRA')}
${h3(1, 'III · Ba cái bẫy hay sập', '4·1')}
<div class="card fig-side" style="${fs(40)};padding:1mm 3mm"><div>
<div class="trap">${ck}<span><b>“Quên đổi đơn vị, quên bình phương.”</b> Đổi SI trước ${nw('('+m('\\mu\\mathrm C\\to10^{-6}\\ \\mathrm C')+'')}, ${nw(m('\\mathrm{nC}\\to10^{-9}\\ \\mathrm C'))}, ${nw(m('\\mathrm{cm}\\to\\mathrm m'))}), bình phương ${m('r')} sau: ${nw(m('r=5\\ \\mathrm{cm}=0{,}05\\ \\mathrm m'))}, ${nw(m('r^2=2{,}5\\cdot10^{-3}\\ \\mathrm{m^2}'))}.</span></div>
<div class="trap">${ck}<span><b>“Chạm nhau rồi tách: cộng độ lớn.”</b> Cộng có dấu: ${uC('+8')} và ${uC('-4')} chạm rồi tách thì mỗi quả ${uC('+2')}, không phải ${uC('6')}.</span></div>
<div class="trap">${ck}<span><b>“Điện tích lớn hơn đẩy mạnh hơn.”</b> Lực ${q1} lên ${q2} và lực ${q2} lên ${q1} bằng độ lớn, ngược chiều, đặt lên hai vật khác nhau (định luật III Newton).</span></div></div>
${H.capLuc()}</div>
${h3(2, 'IV · Trả bài 6 câu', '4·2')}
${box(`${tb('1. Ba cách nhiễm điện, mỗi cách cho kết quả gì?')}${lines(2)}
${tb('2. Vật nhiễm điện âm, dương theo thuyết electron?')}${lines(1)}
${tb('3. Định luật bảo toàn điện tích; quả cầu giống nhau chạm rồi tách?')}${lines(2)}
${tb('4. Định luật Coulomb: phát biểu, công thức, đơn vị.')}${lines(3)}
${tb(`5. Hai lực vuông góc; hai lực bằng nhau hợp góc ${al}: hợp lực?`)}${lines(2)}
${tb(`6. Đặt ${q0} ở đâu để cân bằng giữa ${q1}, ${q2}?`)}${lines(2)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/6 câu · chưa thuộc: ${f(25)} ${nw(`→ đọc lại ô ${f(12)} Tập`)}</div>
${h3(3, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '4·3')}
${rkHai([1, 2, 3], [4, 5, 6])}
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TOÁN MẪU · BÀI TẬP VỀ NHÀ · THỬ THÁCH')}
${h3(1, 'V · Bài toán mẫu: hai quả cầu treo', '5·1')}
<div class="card soft" style="padding:1.2mm 3mm">Hai quả cầu nhỏ giống nhau, mỗi quả ${nw(m('0{,}1\\ \\mathrm g'))}, treo vào cùng một điểm bằng hai dây mảnh cách điện dài bằng nhau. Tích điện bằng nhau, chúng đẩy nhau; khi cân bằng hai dây hợp nhau ${m('90^\\circ')}, hai quả cách nhau ${cm('6')}. Lấy ${g10}. Tìm độ lớn điện tích mỗi quả.</div>
<table><tr><th style="width:50mm">Câu trong đề</th><th>Dữ liệu → kiến thức</th></tr>
<tr><td>“khối lượng 0,1 g … g = 10”</td><td>${m('m=10^{-4}\\ \\mathrm{kg}')} → ${m('P=mg')}</td></tr>
<tr><td style="height:6.5mm">“dây mảnh cách điện”</td><td></td></tr>
<tr><td style="height:6.5mm">“đẩy nhau … cân bằng”</td><td></td></tr>
</table>
<div class="fig-side" style="${fs(46)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl('Các lực lên một quả; điều kiện cân bằng:', 2)}${wl(`${m('\\tan\\alpha=')} … ⇒ ${m('F=')}`, 2)}${wl(`Coulomb ⇒ ${m('|q|=')}`, 2)}</div>${H.quaCauTreo('Lực lên quả bên phải.')}</div>
${h3(2, 'Điền bước còn thiếu: hai dây hợp nhau 60°, hai quả cách 3 cm', '5·2')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div class="ln"><b>Bước 1 (cho sẵn):</b> mỗi dây lệch ${m('\\alpha=30^\\circ')}; ${m('P=10^{-3}\\ \\mathrm N')}; ${m('\\tan30^\\circ\\approx0{,}577')}</div>
${wl(`Bước 2: ${m('F=')}`, 1)}${wl(`Bước 3: ${m('|q|=0{,}03\\sqrt{F/k}=')}`, 1)}</div>
${K.btvn().replace('<i>1</i>', '<i>3</i>')}
${h3(4, 'Thử thách phân tầng', '5·4')}
${box(wl(`${m('\\bigstar')} Quả cầu tích điện ${nw(m('+3{,}2\\cdot10^{-9}\\ \\mathrm C'))}: thừa hay thiếu bao nhiêu electron?`, 2)
 + cau(`${m('\\bigstar\\bigstar')} Tam giác ABC vuông tại C, ${m('CA=3')} cm, ${m('CB=4')} cm; ${m('q_A=-9\\cdot10^{-8}')} C, ${m('q_B=+1{,}2\\cdot10^{-7}')} C, ${m('q_0=+10^{-8}')} C tại C. Hợp lực lên ${q0}?`, 1)
 + cau(`${m('\\bigstar\\bigstar\\bigstar')} ${m('q_1=-2\\ \\mu\\mathrm C')} tại A, ${m('q_2=+8\\ \\mu\\mathrm C')} tại B, ${m('AB=12')} cm. Đặt ${q0} ở đâu để cân bằng? Đổi dấu ${q0} có khác?`, 1))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Hai quả cầu giống nhau chạm rồi tách',
    de: `Hai quả cầu kim loại nhỏ giống hệt nhau, đặt trên bàn cách điện, mang ${m('q_1=-8{,}0')} nC và ${m('q_2=+2{,}0')} nC, chạm nhau rồi tách ra (bỏ qua điện tích mất vào không khí; ${eC}).<br><b>a)</b> điện tích mỗi quả sau khi tách<br><b>b)</b> êlectron chuyển từ quả nào sang quả nào; số êlectron chuyển`,
    nd: `Hệ cô lập: tổng ${f(14)} không đổi; cộng ${f(10)} dấu, chia đều; ${nw(`${m('n=')} ${f(12)}`)}`, a: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>'], gi: 3, fig: H.chamD1() },
  { t: 'Dạng 2 · Dễ · Định luật Coulomb: lực, hút hay đẩy, điện tích từ lực',
    de: `Trong không khí, ${m('q_1=+3{,}0\\ \\mu\\mathrm C')} và ${m('q_2=-5{,}0\\ \\mu\\mathrm C')} cách nhau ${cm('30')} ${nw(`(${kC})`)}.<br><b>a)</b> độ lớn lực tương tác; hút hay đẩy<br><b>b)</b> cặp điện tích khác bằng độ lớn, cách nhau ${cm('10')} trong không khí, đẩy nhau lực ${nw(m('0{,}90\\ \\mathrm N'))}: độ lớn mỗi điện tích`,
    nd: `Đổi ${f(12)} trước, bình phương ${m('r')} sau; dấu chỉ để biết ${f(16)}; ${nw(`${m('|q|=')} ${f(16)}`)}`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b'], gi: 3 },
  { t: 'Dạng 3 · Trung bình · Đổi môi trường, khoảng cách, điện tích',
    de: `Hai điện tích điểm trong không khí cách nhau ${cm('6{,}0')}, hút nhau lực ${m('F_0=4{,}0')} mN.<br><b>a)</b> nhúng cả hai vào dầu ${nw(m('\\varepsilon=4{,}0'))}, giữ khoảng cách: lực khi đó<br><b>b)</b> vẫn trong dầu, đặt cách nhau bao nhiêu để lực lại bằng ${nw(m('4{,}0'))} mN<br><b>c)</b> về không khí, tăng ${m('|q_1|')} lên 3 lần và giảm khoảng cách còn ${cm('3{,}0')}: lực khi đó`,
    nd: `Lập tỉ số với tình huống mốc: ${m('F')} tỉ lệ thuận với ${f(14)}, nghịch với ${f(10)} và ${f(10)}`, a: ['a', 'b', 'c'], gi: 3 },
  { t: 'Dạng 4 · Trung bình · Vị trí cân bằng trên đường nối hai điện tích',
    de: `Trên thanh nhựa thẳng nằm ngang, đủ dài, trong không khí, gắn cố định ${m('q_1=+36')} nC tại A và ${m('q_2=-4{,}0')} nC tại B, ${m('AB=9{,}0')} cm. Hạt ${m('q_0=+2{,}0')} nC xâu vào thanh, trượt không ma sát ${nw(`(${kC})`)}.<br><b>a)</b> đặt ${q0} ở C nào để hợp lực điện lên nó bằng 0: ${m('CA')}, ${m('CB')}<br><b>b)</b> lực do ${q1} và lực do ${q2} lên ${q0} tại C (để kiểm tra)<br><b>c)</b> thay ${q0} bằng hạt ${nC('-2{,}0')}: vị trí cân bằng có đổi không`,
    nd: `Trái dấu ⇒ C ở ${f(18)} đoạn AB, gần điện tích ${f(14)}; ${nw(`${m('\\dfrac{r_1}{r_2}=')} ${f(14)}`)}`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'], gi: 7, fig: H.mienD4() },
  { t: 'Dạng 5 · Khó · Hợp lực của hai điện tích lên một điện tích',
    de: `Trong không khí, ${m('q_1=+4{,}0')} nC tại A, ${m('q_2=-12')} nC tại B, ${m('q_0=+2{,}0')} nC tại C; ${m('CA=3{,}0')} cm, ${m('CB=6{,}0')} cm, CA vuông góc CB ${nw(`(${kC})`)}.<br><b>a)</b> độ lớn lực ${m('F_1')} do ${q1} và ${m('F_2')} do ${q2} lên ${q0}<br><b>b)</b> độ lớn hợp lực lên ${q0}<br><b>c)</b> góc giữa hợp lực và ${m('\\vec F_1')}`,
    nd: `Hai lực vuông góc: ${nw(`${m('F=')} ${f(22)}`)}; ${nw(`${m('\\tan\\varphi=')} ${f(14)}`)}`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'], gi: 7, fig: H.tamGiacD5() },
];

// Bài tương tự: mỗi dạng 2 bài, giải vào vở (thầy chốt 10/11), ô đáp số cuối dòng của ý; đáp số tính bằng Python 12/11/2026.
const oY = (s, o, w = 25) => s.split('<br>').map((p) => {
  const y = p.match(/^<b>([a-d])\)<\/b>/);
  if (!y) return `<div>${p}</div>`;
  const ls = o.filter((l) => l[0] === y[1]);
  return `<div class="yo"><span>${p}</span><span class="oo">${ls.map((l) => `<span class="nw"><b>${l})</b>${f(w)}</span>`).join('')}</span></div>`;
}).join('');
const ttDe = (b) => b.fig ? `<div class="fig-side" style="grid-template-columns:1fr ${b.fw}mm">${`<div>${oY(b.de, b.o, b.ow)}</div>`}${b.fig}</div>` : oY(b.de, b.o, b.ow);
const vaoVo = (ds) => ds.map((b) => (b.o ? { t: b.t, de: ttDe(b), k: 0 } : b));
const nhap = (n) => ({ t: '<span class="nhap-t">Nháp / chỗ em còn vướng</span>', de: lines(n), k: 0 });
const kk = nw(`(${kC})`);
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–3', 'DẠNG 4–5'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Hai quả cầu kim loại nhỏ giống hệt nhau mang ${m('q_1=+5{,}0')} nC và ${m('q_2=-9{,}0')} nC, chạm nhau rồi tách ra; hệ cô lập; ${eC}.<br><b>a)</b> điện tích mỗi quả sau khi tách<br><b>b)</b> êlectron chuyển từ quả nào sang quả nào; số êlectron chuyển`, o: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>'] },
    { t: 'Dạng 1 · Bài 2', de: `Ba quả cầu kim loại giống hệt nhau mang ${nC('+6{,}0')}, ${nC('-3{,}0')}, ${nC('+9{,}0')}, cùng chạm nhau rồi tách ra; hệ cô lập; ${eC}.<br><b>a)</b> điện tích mỗi quả sau khi tách<br><b>b)</b> sau khi tách, mỗi quả thừa hay thiếu bao nhiêu êlectron`, fig: H.baQuaTT(), fw: 54, o: ['a', 'b'], ow: 22 },
    { t: 'Dạng 2 · Bài 1', de: `Trong không khí, ${m('q_1=-2{,}0\\ \\mu\\mathrm C')} và ${m('q_2=-4{,}0\\ \\mu\\mathrm C')} cách nhau ${cm('20')} ${kk}.<br><b>a)</b> độ lớn lực tương tác; hút hay đẩy<br><b>b)</b> hai điện tích bằng độ lớn, cách nhau ${cm('5{,}0')} trong không khí, đẩy nhau lực ${nw(m('3{,}6\\ \\mathrm N'))}: độ lớn mỗi điện tích`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b'] },
    { t: 'Dạng 2 · Bài 2', de: `Trong không khí, ${m('q_1=+2{,}0')} nC và ${m('q_2=-8{,}0')} nC cách nhau ${cm('3{,}0')} ${kk}.<br><b>a)</b> độ lớn lực tương tác; hút hay đẩy<br><b>b)</b> hai điện tích bằng độ lớn, cách nhau ${cm('3{,}0')} trong không khí, đẩy nhau lực ${nw(m('0{,}40\\ \\mathrm N'))}: độ lớn mỗi điện tích`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b'] },
    { t: 'Dạng 3 · Bài 1', de: `Hai điện tích điểm trong không khí cách nhau ${cm('6{,}0')}, hút nhau lực ${m('F_0=9{,}0')} mN.<br><b>a)</b> nhúng vào chất lỏng ${nw(m('\\varepsilon=2{,}25'))}, giữ khoảng cách: lực khi đó<br><b>b)</b> trong chất lỏng đó, cách nhau bao nhiêu để lực lại bằng ${nw(m('9{,}0'))} mN<br><b>c)</b> về không khí, giảm ${m('|q_1|')} 2 lần, tăng khoảng cách lên ${cm('12')}: lực khi đó`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 3 · Bài 2', de: `Hai điện tích điểm trong không khí đẩy nhau lực ${m('F_0=2{,}0')} mN.<br><b>a)</b> tăng độ lớn mỗi điện tích 2 lần và tăng khoảng cách 2 lần: lực khi đó<br><b>b)</b> giữ điện tích ban đầu, đặt vào dầu ${nw(m('\\varepsilon=2{,}0'))}, khoảng cách còn một nửa: lực khi đó<br><b>c)</b> khoảng cách còn một nửa, môi trường có ${eps} bằng bao nhiêu thì lực vẫn bằng ${nw(m('F_0'))}`, o: ['a', 'b', 'c'] },
  ], [
    { t: 'Dạng 4 · Bài 1', de: `Trong không khí, gắn cố định ${m('q_1=+4{,}0')} nC tại A và ${m('q_2=+9{,}0')} nC tại B, ${m('AB=10')} cm ${kk}. Hạt ${m('q_0=+1{,}0')} nC trượt không ma sát trên thanh thẳng qua A, B.<br><b>a)</b> vị trí C để ${q0} cân bằng: ${m('CA')}, ${m('CB')}<br><b>b)</b> độ lớn lực do ${q1} lên ${q0} tại C<br><b>c)</b> thay ${q0} bằng ${nC('-3{,}0')}: vị trí cân bằng có đổi không`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'] },
    { t: 'Dạng 4 · Bài 2', de: `Trong không khí, gắn cố định ${m('q_1=-1{,}0')} nC tại A và ${m('q_2=+4{,}0')} nC tại B, ${m('AB=6{,}0')} cm ${kk}. Hạt ${m('q_0=+2{,}0')} nC trượt không ma sát trên thanh thẳng qua A, B.<br><b>a)</b> C ở trong hay ngoài đoạn AB, phía nào; ${m('CA')}, ${m('CB')}<br><b>b)</b> độ lớn lực do ${q1} lên ${q0} tại C<br><b>c)</b> nếu ${q2} đổi thành ${nC('+1{,}0')}: còn vị trí cân bằng không`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'a<sub>3</sub>', 'b', 'c'], ow: 22 },
    { t: 'Dạng 5 · Bài 1', de: `Trong không khí, ${m('q_1=+6{,}0')} nC tại A, ${m('q_2=+16')} nC tại B, ${m('q_0=+1{,}0')} nC tại C; ${m('CA=3{,}0')} cm, ${m('CB=4{,}0')} cm, CA vuông góc CB ${kk}.<br><b>a)</b> độ lớn ${m('F_1')} do ${q1}, ${m('F_2')} do ${q2} lên ${q0}<br><b>b)</b> độ lớn hợp lực lên ${q0}<br><b>c)</b> góc giữa hợp lực và ${m('\\vec F_1')}`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'] },
    { t: 'Dạng 5 · Bài 2', de: `Trong không khí, ba điện tích ở ba đỉnh tam giác đều cạnh ${cm('6{,}0')}: ${m('q_A=q_B=+4{,}0')} nC, ${m('q_0=+1{,}0')} nC tại C ${kk}.<br><b>a)</b> độ lớn lực do mỗi điện tích A, B lên ${q0}<br><b>b)</b> góc giữa hai lực; độ lớn hợp lực<br><b>c)</b> thay ${m('q_B=-4{,}0')} nC: góc giữa hai lực; hợp lực`, fig: H.deuTT(), fw: 38, o: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c<sub>1</sub>', 'c<sub>2</sub>'], ow: 20 },
    nhap(5),
  ]],
  dap: [
    `D1·1: a) −2,0 nC · b<sub>1</sub>) quả 2 → quả 1 · b<sub>2</sub>) 4,4·10<sup>10</sup> &nbsp;|&nbsp; D1·2: a) +4,0 nC · b) thiếu 2,5·10<sup>10</sup> êlectron &nbsp;|&nbsp; D2·1: a<sub>1</sub>) 1,8 N · a<sub>2</sub>) đẩy · b) 1,0 ${m('\\mu')}C &nbsp;|&nbsp; D2·2: a<sub>1</sub>) 1,6·10<sup>−4</sup> N · a<sub>2</sub>) hút · b) 0,20 ${m('\\mu')}C &nbsp;|&nbsp; D3·1: a) 4,0 mN · b) 4,0 cm · c) 1,1 mN &nbsp;|&nbsp; D3·2: a) 2,0 mN · b) 4,0 mN · c) ${m('\\varepsilon')} = 4,0`,
    `D4·1: a<sub>1</sub>) CA = 4,0 cm · a<sub>2</sub>) CB = 6,0 cm · b) 2,3·10<sup>−5</sup> N · c) không đổi &nbsp;|&nbsp; D4·2: a<sub>1</sub>) ngoài, phía A · a<sub>2</sub>) CA = 6,0 cm · a<sub>3</sub>) CB = 12 cm · b) 5,0·10<sup>−6</sup> N · c) không &nbsp;|&nbsp; D5·1: a<sub>1</sub>) 6,0·10<sup>−5</sup> N · a<sub>2</sub>) 9,0·10<sup>−5</sup> N · b) 1,1·10<sup>−4</sup> N · c) 56° &nbsp;|&nbsp; D5·2: a) 1,0·10<sup>−5</sup> N · b<sub>1</sub>) 60° · b<sub>2</sub>) 1,7·10<sup>−5</sup> N · c<sub>1</sub>) 120° · c<sub>2</sub>) 1,0·10<sup>−5</sup> N`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 2], kq: [[1, 2, 3], [4, 5]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'nhiễm điện 1·4 · bảo toàn điện tích 2·1 · thước nhựa 2·2 · Coulomb 2·3 · cân điện tử 3·1 · tổng hợp lực 3·2 · cân bằng 3·3 · bẫy 4·1 · bài toán mẫu 5·1 · dạng 1–3 → 6·1 · dạng 4–5 → 7·1',
  out: process.argv[2],
});
