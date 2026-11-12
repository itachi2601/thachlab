// Ruột tập VL11 – Bài 24 · Nguồn điện (lesson id 43). Quyển Chương 4 lớp 11: bài 22 = tr. 1–12, bài 24 = tr. 25–36.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l11-bai24.mjs (toàn bộ SVG tự vẽ). Nội dung theo bài web (book/cache/43.json, tải từ DB 12/11/2026): mục tiêu,
// dự đoán đèn pha tối lúc đề, II.1–II.5, thí nghiệm siêu tụ/pin + đo U theo I, ba bẫy, Trả bài 6 câu, bài toán mẫu một nguồn
// một điện trở, thử thách ⭐–⭐⭐⭐, 4 dạng bài tập mẫu. Đáp số Bài tương tự (tuongTu.dap) tính bằng Python 12/11/2026.
// Chạy: node scripts/ruot-tap/l11-bai24.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl11-bai24.pdf
//       node scripts/ruot-tap/l11-bai24.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l11-bai24/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL11b24 as H } from './hinh-l11-bai24.mjs';

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
  const out = resolve(HERE, 'out/hinh-l11-bai24'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 24, lid: 43, ten: 'NGUỒN ĐIỆN', lop: 11, baiDau: 22, sub: 'Vật lí 11 · Chương 4: Dòng điện. Mạch điện' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const E = m('\\mathcal E'), r = m('r'), R = m('R'), U = m('U'), I = m('I');
const V = (s) => nw(m(`${s}\\ \\mathrm V`)), A = (s) => nw(m(`${s}\\ \\mathrm A`)), Om = (s) => nw(m(`${s}\\ \\Omega`));
const eC = nw(m('|e|=1{,}6\\cdot10^{-19}\\ \\mathrm C'));
const oF = (w, h = 10) => `<span class="fill" style="min-width:${w}mm;height:${h}mm"></span>`;

// Bài tương tự 1 cột, ô đáp số cuối dòng của ý (cùng cách l11-bai16).
const ttCss = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';

const p1 = `${ttCss}<section class="page">
${head('BÀI 24 · NGUỒN ĐIỆN', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Nêu vì sao cần <b>nguồn điện</b> và <b>lực lạ</b> làm gì bên trong nguồn`)}
${dong(`${ck}Định nghĩa và tính <b>suất điện động</b> của nguồn từ công của lực lạ`)}
${dong(`${ck}Giải mạch kín một nguồn; nhận ra <b>đoản mạch</b>; tính bộ nguồn <b>ghép</b>`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Bật khoá xe máy: đèn pha sáng rõ. Bấm nút đề: đèn tối hẳn một giây, máy nổ rồi đèn mới sáng lại. Vẫn bình đó, dây đó. Điều gì làm đèn tối đi lúc đề?</p>
<div class="fig-side" style="${fs(44)}"><div>
${opt('A', 'Nút đề cắt bớt điện của đèn, dồn cho mô tơ')}
${opt('B', 'Ắc quy hết điện trong tích tắc rồi tự nạp lại')}
${opt('C', 'Dòng đề rất lớn bị chính ắc quy cản bên trong, làm hai cực ắc quy tụt áp')}
${opt('D', 'Dây dẫn nóng lên lúc đề, điện trở dây tăng nên đèn nhận ít dòng')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 2)}</div>
${H.denPha()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(2)}</div>
${h3(4, 'II.1 · Nguồn điện duy trì hiệu điện thế', '1·4')}
<div class="card fig-side" style="${fs(42)};padding:1.2mm 3mm"><div>
<div>A tích điện ${m('+q')}, B tích điện ${m('-q')}: ${nw(`${m('V_A')} ${f(8)} ${m('V_B')}`)}.</div>
<div>Nối dây: electron đi ${nw(`${f(7)} → ${f(7)}`)}; dòng điện ${nw(`${f(7)} → ${f(7)}.`)}</div>
<div>Một lát sau hai quả ${f(16)}, ${nw(`${m('V_A')} ${f(7)} ${m('V_B')}`)}: ${nw(`dòng ${f(10)}.`)}</div>
<div>Muốn dòng chạy mãi phải giữ ${nw(`${m('U_{AB}=V_A-V_B')} ${f(8)} 0`)}.</div></div>
${H.haiQuaCau()}</div>
<div class="card soft" style="padding:1.2mm 3mm"><b>Nguồn điện:</b> thiết bị tạo ra và ${f(22)} hiệu điện thế giữa hai cực (+) và (−), nhờ đó duy trì ${f(30)} trong mạch kín.${wl('Ba nguồn điện em dùng hằng ngày:', 1)}</div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('THÍ NGHIỆM TỤ – PIN · LỰC LẠ · SUẤT ĐIỆN ĐỘNG')}
${h3(1, 'Thí nghiệm: tụ điện “giả làm” nguồn', '2·1')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div><b>Làm:</b> nạp siêu tụ ${nw(m('1{,}0\\ \\mathrm F'))} tới ${V('2{,}7')} rồi cho xả qua điện trở ${Om('100')}; bên cạnh, hai pin tiểu nối tiếp (${V('3{,}0')}) nuôi điện trở ${Om('100')} giống hệt. Vôn kế đo hai đầu mỗi điện trở.</div>
<table class="tbl-ct" style="margin:.6mm 0"><tr><th>${m('t')} (s)</th><th>0</th><th>20</th><th>40</th><th>60</th><th>300</th></tr>
<tr><td>Vôn kế, mạch tụ (V)</td><td>2,7</td><td>2,2</td><td>1,8</td><td>1,5</td><td>0,1</td></tr>
<tr><td>Vôn kế, mạch pin (V)</td><td>2,98</td><td>2,98</td><td>2,98</td><td>2,98</td><td>2,98</td></tr></table>
<div><b>Rút ra:</b> tụ chỉ chứa sẵn ${f(20)}, xả dần là ${f(12)}; pin ${f(22)} được hiệu điện thế, nên ${f(10)} mới là nguồn điện.</div></div>
${H.tuPin()}</div>
${h3(2, 'II.2 · Lực lạ và suất điện động', '2·2')}
<div class="card fig-side" style="${fs(42)};padding:1.2mm 3mm"><div>
<div>Mạch ngoài: dòng điện chạy từ cực ${f(8)} về cực ${f(8)}.</div>
<div>Trong nguồn: điện tích dương phải đi từ cực ${f(8)} sang cực ${f(8)}, ${f(14)} chiều điện trường; lực điện không làm nổi.</div>
<div>Cần <b>lực lạ</b>, khác bản chất lực điện: trong pin là lực ${f(16)}, trong máy phát điện là lực ${f(16)}.</div>
<div>Trong nguồn: công lực lạ ${m('A_{\\text{l}}')} ${f(8)} độ lớn công cản của lực điện ${m('A_{\\text{đ}}')}.</div>
<div>Mạch kín: dòng ra ở cực ${f(8)}, qua ${R}, vào cực ${f(8)}, rồi lực lạ đưa lên cực ${f(8)}.</div></div>
${H.lucLa()}</div>
<div class="card" style="padding:1.2mm 3mm">
<div>Suất điện động đặc trưng cho khả năng ${f(36)} của nguồn điện.</div>
<div style="margin:1mm 0;display:flex;align-items:flex-end;gap:3mm">${m('\\mathcal E=')} ${oF(24, 11)} <span>đơn vị ${f(10)} ${nw(`(1 V = 1 ${f(8)}/C)`)}</span></div>
<div>${m('A')}: công của ${f(20)} trong nguồn (J) · ${m('q')}: ${f(26)} (C)</div></div>
${h3(3, 'Làm nhanh', '2·3')}
${box(cau(`<b>Câu 1.</b> Vỏ pin ghi “1,5 V”. Con số này cho biết điều gì về công và điện tích?`, 2)
 + cau(`<b>Câu 2.</b> Pin có ${m('\\mathcal E=9{,}0\\ \\mathrm V')}. Lực lạ làm công bao nhiêu khi đưa ${nw(m('20\\ \\mathrm C'))} điện tích dương qua nguồn?`, 2))}
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('ĐIỆN TRỞ TRONG · ĐỊNH LUẬT OHM CHO TOÀN MẠCH')}
${h3(1, 'II.3 · Điện trở trong và hiệu điện thế hai cực', '3·1')}
<div class="card" style="padding:1.2mm 3mm">
<div>Điện tích đi trong nguồn bị ${f(16)} (va chạm với vật chất của nguồn): nguồn có <b>điện trở trong</b> ${r}.</div>
<div>Hở mạch (${nw(m('I=0'))}): ${nw(`${U} ${f(8)} ${E}`)} &nbsp;· mạch kín: ${nw(`${U} ${f(8)} ${E}`)}</div></div>
<div class="fig-side" style="${fs(46)}"><div>
<div style="line-height:1.35"><b>Thí nghiệm đo.</b> Pin tiểu đã dùng; hở mạch vôn kế ở hai cực chỉ ${V('1{,}50')}. Mắc hộp điện trở ${R}, ampe kế nối tiếp; đổi ${R}, đọc ${I}, ${U}.</div>
<table class="tbl-ct" style="margin-top:.6mm"><tr><th>${R} (Ω)</th><th>${I} (A)</th><th>${U} (V)</th><th>${m('\\mathcal E-U')} (V)</th><th>${m('\\dfrac{\\mathcal E-U}{I}')} (Ω)</th></tr>
<tr><td>14</td><td>0,10</td><td>1,40</td><td></td><td></td></tr>
<tr><td>9</td><td>0,15</td><td>1,35</td><td></td><td></td></tr>
<tr><td>4</td><td>0,30</td><td>1,20</td><td></td><td></td></tr>
<tr><td>2</td><td>0,50</td><td>1,00</td><td></td><td></td></tr>
<tr><td>1,5</td><td>0,60</td><td>0,90</td><td></td><td></td></tr></table>
<div style="margin-top:.6mm"><b>Rút ra:</b> ${m('\\mathcal E-U')} tỉ lệ thuận với ${f(8)}; hệ số là ${nw(`${r} = ${f(10)} Ω`)}</div></div>
${H.doThiUI()}</div>
<div class="card" style="padding:1.2mm 3mm">
<div style="display:flex;align-items:flex-end;gap:3mm">${m('U=')} ${oF(26, 9)} <span>${m('Ir')}: độ giảm thế trên ${f(10)}, mạch ngoài ${f(22)}.</span></div>
<div>Đồ thị ${m('U')} theo ${m('I')}: đường ${f(16)} đi xuống; cắt trục ${m('U')} tại ${f(8)}; độ dốc bằng ${f(10)}.</div></div>
${h3(2, 'II.4 · Định luật Ohm cho toàn mạch · đoản mạch', '3·2')}
<div class="card" style="padding:1.2mm 3mm">
<div>Bảo toàn năng lượng: công của nguồn ${nw(m('\\mathcal E It'))} = nhiệt ở ${R} + nhiệt ở ${r} = ${f(14)} + ${f(14)}</div>
<div style="margin:1mm 0;display:flex;align-items:flex-end;gap:3mm">⇒ ${m('I=')} ${oF(24, 11)} <span>Đoản mạch (${nw(m('R\\to0'))}): ${m('I_{\\text{đm}}=')}</span> ${oF(18, 11)}</div>
<div>Pin tiểu mới ${nw(`(${V('1{,}5')}, ${Om('0{,}3')})`)}: ${nw(`${m('I_{\\text{đm}}=')} ${f(10)} A`)}</div>
<div>Ắc quy xe máy ${nw(`(${V('12{,}6')}, ${Om('0{,}02')})`)}: ${nw(`${m('I_{\\text{đm}}=')} ${f(12)} A`)}</div>
<div><b>Thí nghiệm nối tắt pin tiểu mới</b> (dây đồng mảnh + ampe kế thang 10 A, đúng 3 giây, đeo kính; cấm làm với ắc quy, pin lithium): dây ${f(14)}; ampe kế chỉ cỡ ${f(10)} A.</div>
<div>${r} càng ${f(10)} thì đoản mạch càng nguy hiểm; cầu chì chặn dòng đoản mạch.</div></div>
${h3(3, 'Làm nhanh', '3·3')}
${box(cau(`Nguồn ${nw(m('\\mathcal E=6{,}0\\ \\mathrm V'))}, ${nw(m('r=0{,}50\\ \\Omega'))} nối ${nw(`${m('R=2{,}5\\ \\Omega')}.`)} Tính ${I} và ${U} hai cực nguồn (kiểm bằng hai cách).`, 2))}
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('GHÉP NGUỒN · BA CÁI BẪY · TRẢ BÀI')}
${h3(1, 'II.5 · Ghép nguồn thành bộ', '4·1')}
<div class="fig-side" style="${fs(46)}"><div>
<table><tr><th style="width:40mm">Cách ghép</th><th>${m('\\mathcal E_b')}</th><th>${m('r_b')}</th></tr>
<tr><td>Nối tiếp</td><td></td><td></td></tr>
<tr><td>Song song ${m('n')} nguồn giống nhau</td><td></td><td></td></tr>
<tr><td>Xung đối, ${m('\\mathcal E_1>\\mathcal E_2')}</td><td></td><td></td></tr>
<tr><td>${m('n')} dãy, mỗi dãy ${m('m')} nguồn</td><td></td><td></td></tr></table>
<div style="margin-top:.6mm">6 pin ${nw(`(${V('1{,}5')}; ${Om('0{,}6')})`)} như hình: ${nw(`${m('\\mathcal E_b=')} ${f(12)}`)} ${nw(`${m('r_b=')} ${f(12)}`)}</div></div>
${H.honHop('2 dãy, mỗi dãy 3 pin.', { n: 2, m: 3 })}</div>
${h3(2, 'III · Ba cái bẫy hay sập', '4·2')}
<div class="card" style="padding:1mm 3mm">
<div class="trap">${ck}<span><b>“Suất điện động là hiệu điện thế hai cực.”</b> ${E}: công lực lạ, không đổi; ${U}: công lực điện, ${nw(m('U<\\mathcal E'))} khi có dòng.</span></div>
<div class="trap">${ck}<span><b>“Trong nguồn dòng cũng chạy từ (+) sang (−).”</b> Trong nguồn dòng đi từ (−) lên (+) nhờ lực lạ, như máy bơm nước.</span></div>
<div class="trap">${ck}<span><b>“Vôn kế chỉ 1,5 V thì pin còn tốt.”</b> Hở mạch pin nào cũng ${V('1{,}5')}. Nối ${Om('3')}: pin mới ${nw(`(${Om('0{,}3')})`)} ${nw(`${m('U\\approx1{,}36\\ \\mathrm V')};`)} pin cũ ${nw(`(${Om('3')})`)} ${nw(`${m('U=')} ${f(10)} V`)}</span></div></div>
${h3(3, 'IV · Trả bài 6 câu', '4·3')}
${box(`${tb('1. Nguồn điện là gì? Vì sao hai quả cầu A, B không phải nguồn?')}${lines(1)}
${tb('2. Lực lạ là gì, làm việc ở đâu, theo chiều nào?')}${lines(1)}
${tb('3. Định nghĩa, công thức, đơn vị suất điện động.')}${lines(1)}
${tb(`4. Điện trở trong; ${m('U')} theo ${m('\\mathcal E')}, ${m('I')}, ${m('r')}; khi nào ${m('U=\\mathcal E')}?`)}${lines(1)}
${tb('5. Định luật Ohm cho toàn mạch suy ra từ đâu? Đoản mạch là gì?')}${lines(1)}
${tb(`6. So sánh ${m('\\mathcal E')} và ${m('U')}; ghép nối tiếp, song song.`)}${lines(1)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/6 câu · chưa thuộc: ${f(25)} ${nw(`→ đọc lại ô ${f(12)} Tập`)}</div>
${h3(4, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '4·4')}
${rkHai([1, 2, 3], [4, 5, 6])}
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TOÁN MẪU · BÀI TẬP VỀ NHÀ · THỬ THÁCH')}
${h3(1, 'V · Bài toán mẫu: nguồn nuôi một điện trở', '5·1')}
<div class="card soft fig-side" style="${fs(36)};padding:1.2mm 3mm"><div>Nguồn có suất điện động ${V('9{,}0')}, điện trở trong ${Om('1{,}0')}, nối với ${Om('R=8{,}0')} thành mạch kín.<br><b>a)</b> Tính cường độ dòng điện.<br><b>b)</b> Tính hiệu điện thế hai cực nguồn.<br><b>c)</b> Thay ${R} bằng ${Om("R'=2{,}0")}: ${U} còn bao nhiêu?<br><b>d)</b> Nối tắt hai cực nguồn: dòng điện bao nhiêu?</div>${H.mach('')}</div>
<table style="margin:0"><tr><th style="width:50mm">Câu trong đề</th><th>Dữ liệu → kiến thức</th></tr>
<tr><td>“suất điện động 9,0 V”</td><td>${m('\\mathcal E')} → không phải ${U} hai cực</td></tr>
<tr><td style="height:6.5mm">“điện trở trong 1,0 Ω”</td><td></td></tr>
<tr><td style="height:6.5mm">“nối tắt hai cực”</td><td></td></tr>
</table>
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm;margin-top:1mm">
${wl(`a) ${m('I=')}`, 1)}${wl(`b) ${m('U=')} (kiểm bằng cách thứ hai)`, 2)}${wl(`c) ${m("I'=")} … ⇒ ${m("U'=")}`, 1)}${wl(`d) ${m('I_{\\text{đm}}=')}`, 1)}</div>
${h3(2, 'Điền bước còn thiếu: cùng đề, chỉ đổi r = 2,0 Ω', '5·2')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div class="ln"><b>Bước 1 (cho sẵn):</b> ${m('R+r=8{,}0+2{,}0=10{,}0\\ \\Omega')}</div>
${wl(`Bước 2: ${m('I=')}`, 1)}${wl(`Bước 3: ${m('U=IR=')} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ${m('U=\\mathcal E-Ir=')}`, 1)}${wl(`Bước 4: ${r} tăng thì ${I} và ${U} tăng hay giảm?`, 1)}</div>
${K.btvn().replace('<i>1</i>', '<i>3</i>')}
${h3(4, 'Thử thách phân tầng', '5·4')}
${box(cau(`${m('\\bigstar')} Pin ${V('1{,}5')}, ${Om('r=0{,}5')} nối ${nw(`${m('R=2{,}5\\ \\Omega')}.`)} Tính ${I} và ${U}.`, 1)
 + cau(`${m('\\bigstar\\bigstar')} Nối ${Om('R_1=4')} thì ${A('I_1=1{,}0')}; nối ${Om('R_2=9')} thì ${nw(`${m('I_2=0{,}5\\ \\mathrm A')}.`)} Tìm ${E}, ${r}.`, 1)
 + cau(`${m('\\bigstar\\bigstar\\bigstar')} Ắc quy ${V('12{,}6')}, đề lấy ${A('60')}; đèn sáng rõ khi ${nw(`${m('U\\ge9{,}0\\ \\mathrm V')}.`)} Tìm ${r} tối đa.`, 1))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Suất điện động: công lực lạ, điện tích, thời gian',
    de: `Ắc quy có ${m('\\mathcal E=12\\ \\mathrm V')} cấp điện cho mạch kín. Trong thời gian dòng không đổi ${A('I=0{,}50')} chạy qua nguồn, lực lạ thực hiện công ${nw(m('A=1{,}8\\cdot10^{3}\\ \\mathrm J'))} đưa điện tích dương từ cực âm sang cực dương.<br><b>a)</b> điện tích đã dịch chuyển qua nguồn<br><b>b)</b> khoảng thời gian dòng điện chạy<br><b>c)</b> pin ${V('1{,}5')} đưa cùng lượng điện tích đó qua nguồn: công của lực lạ`,
    nd: `${nw(`${m('q=')} ${f(14)}`)} từ định nghĩa ${E}; ${nw(`${m('t=')} ${f(10)}`)}; ${m('A')} là công của ${f(16)}, không phải lực điện ở mạch ngoài`, a: ['a', 'b', 'c'], gi: 8 },
  { t: 'Dạng 2 · Trung bình · Hai số chỉ vôn kế: ℰ, I, r và dòng khi nối tắt',
    de: `Pin đã dùng lâu. Vôn kế lí tưởng ở hai cực pin chỉ ${V('9{,}0')} khi mạch hở. Nối hai cực pin với ${Om('R=30')} (bỏ qua điện trở dây nối), vôn kế chỉ ${V('7{,}5')}.<br><b>a)</b> suất điện động của pin<br><b>b)</b> cường độ dòng điện trong mạch kín<br><b>c)</b> điện trở trong của pin<br><b>d)</b> nối tắt hai cực pin: dòng qua pin`,
    nd: `Hở mạch ${nw(`${m('I=0')} ⇒ ${m('U=')} ${f(8)}`)}; có ${R}: ${nw(`${m('I=')} ${f(10)}`)}; ${nw(`${m('r=')} ${f(14)}`)}`, a: ['a', 'b', 'c', 'd'], gi: 8, fig: H.mach('K mở rồi K đóng.', { von: true, khoa: true }) },
  { t: 'Dạng 3 · Khó · Hai lần đo cùng một nguồn: lập hệ tìm r và ℰ',
    de: `Nối nguồn lần lượt với ${Om('R_1=3{,}0')} và ${Om('R_2=10')} (bỏ qua điện trở dây nối). Vôn kế lí tưởng ở hai cực nguồn chỉ ${V('U_1=3{,}6')} và ${V('U_2=5{,}0')} tương ứng.<br><b>a)</b> cường độ dòng điện mỗi lần đo<br><b>b)</b> điện trở trong ${r} và suất điện động ${E}<br><b>c)</b> nối tắt hai cực nguồn: dòng điện`,
    nd: `Mỗi lần: ${nw(`${m('I=')} ${f(8)}`)}, ${nw(`${m('U=')} ${f(14)}`)}; hai ẩn ⇒ hai phương trình, trừ vế khử ${f(8)}`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], gi: 6, cot: 3 },
  { t: 'Dạng 4 · Khó · Bộ nguồn hỗn hợp đối xứng: ℰ<sub>b</sub>, r<sub>b</sub>, I và dòng qua mỗi pin',
    de: `Đèn pin dùng 8 pin giống nhau, mỗi pin ${m('\\mathcal E_0=1{,}5\\ \\mathrm V')}, ${Om('r_0=0{,}50')}, ghép 2 dãy song song, mỗi dãy 4 pin nối tiếp. Bóng đèn coi như ${Om('R=3{,}0')} nối vào hai cực bộ nguồn; bỏ qua điện trở dây nối.<br><b>a)</b> suất điện động và điện trở trong của bộ<br><b>b)</b> cường độ dòng điện qua bóng đèn<br><b>c)</b> hiệu điện thế hai cực bộ nguồn<br><b>d)</b> cường độ dòng điện qua mỗi pin`,
    nd: `${nw(`${m('\\mathcal E_b=')} ${f(12)}`)}, ${nw(`${m('r_b=')} ${f(12)}`)}; hai dãy giống nhau ⇒ mỗi dãy mang ${f(10)} dòng tổng`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c', 'd'], gi: 5, fig: H.honHop('2 dãy, mỗi dãy 4 pin.', { n: 2, m: 4 }), cot: 3 },
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
  tieuDe: ['DẠNG 1–2', 'DẠNG 3–4'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Pin ${m('\\mathcal E=1{,}5\\ \\mathrm V')}, dòng không đổi ${A('I=0{,}20')} chạy qua nguồn; lực lạ thực hiện công ${nw(`${m('270\\ \\mathrm J')}.`)}<br><b>a)</b> điện tích đã dịch chuyển qua nguồn<br><b>b)</b> thời gian dòng điện chạy<br><b>c)</b> ắc quy ${V('12')} đưa cùng lượng điện tích đó qua nguồn: công của lực lạ`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 1 · Bài 2', de: `Ắc quy ${m('\\mathcal E=6{,}0\\ \\mathrm V')} cho dòng không đổi ${A('0{,}40')} chạy qua trong ${nw('10 phút')}; ${eC}.<br><b>a)</b> điện tích dịch chuyển qua nguồn<br><b>b)</b> công của lực lạ<br><b>c)</b> công của lực lạ khi đưa một electron qua nguồn (độ lớn)`, o: ['a', 'b', 'c'], ow: 30 },
    { t: 'Dạng 2 · Bài 1', de: `Vôn kế lí tưởng ở hai cực nguồn chỉ ${V('12')} khi mạch hở. Nối hai cực với ${Om('R=10')} (bỏ qua điện trở dây nối), vôn kế chỉ ${V('10')}.<br><b>a)</b> suất điện động<br><b>b)</b> cường độ dòng điện<br><b>c)</b> điện trở trong<br><b>d)</b> dòng khi nối tắt hai cực`, o: ['a', 'b', 'c', 'd'] },
    { t: 'Dạng 2 · Bài 2', de: `Vôn kế lí tưởng ở hai cực một bộ pin chỉ ${V('4{,}5')} khi mạch hở, chỉ ${V('4{,}0')} khi nối hai cực với ${Om('R=4{,}0')} (bỏ qua điện trở dây nối).<br><b>a)</b> suất điện động<br><b>b)</b> cường độ dòng điện<br><b>c)</b> điện trở trong<br><b>d)</b> dòng khi nối tắt hai cực`, o: ['a', 'b', 'c', 'd'] },
    nhap(10),
  ], [
    { t: 'Dạng 3 · Bài 1', de: `Nối nguồn lần lượt với ${Om('R_1=2{,}0')} và ${Om('R_2=5{,}0')} (bỏ qua điện trở dây nối); vôn kế lí tưởng ở hai cực chỉ ${V('U_1=4{,}0')} và ${V('U_2=5{,}0')}.<br><b>a)</b> dòng điện mỗi lần đo<br><b>b)</b> điện trở trong ${r} và suất điện động ${E}<br><b>c)</b> dòng khi nối tắt hai cực`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], ow: 18 },
    { t: 'Dạng 3 · Bài 2', de: `Nối nguồn với ${Om('R_1=1{,}0')} thì ampe kế chỉ ${A('I_1=2{,}0')}; nối với ${Om('R_2=4{,}0')} thì ${nw(`${m('I_2=0{,}80\\ \\mathrm A')}`)} (ampe kế lí tưởng, bỏ qua điện trở dây nối).<br><b>a)</b> hiệu điện thế hai cực mỗi lần<br><b>b)</b> điện trở trong ${r} và suất điện động ${E}<br><b>c)</b> dòng khi nối tắt hai cực`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], ow: 18 },
    { t: 'Dạng 4 · Bài 1', de: `6 pin giống nhau, mỗi pin ${m('\\mathcal E_0=2{,}0\\ \\mathrm V')}, ${Om('r_0=0{,}80')}, ghép 2 dãy song song, mỗi dãy 3 pin nối tiếp; mạch ngoài ${Om('R=4{,}8')}.<br><b>a)</b> ${m('\\mathcal E_b')} và ${m('r_b')} của bộ<br><b>b)</b> dòng điện qua ${R}<br><b>c)</b> hiệu điện thế hai cực bộ nguồn<br><b>d)</b> dòng điện qua mỗi pin`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c', 'd'], ow: 20 },
    { t: 'Dạng 4 · Bài 2', de: `4 pin giống nhau (${V('1{,}5')}; ${Om('0{,}50')}) mắc nối tiếp nhưng pin thứ ba bị lắp ngược; mạch ngoài ${Om('R=4{,}0')}.<br><b>a)</b> ${m('\\mathcal E_b')} và ${m('r_b')} của bộ<br><b>b)</b> dòng điện qua ${R}<br><b>c)</b> hiệu điện thế hai cực bộ nguồn<br><b>d)</b> lắp lại đúng pin thứ ba: dòng qua ${R}`, fig: H.nguoc(), fw: 44, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c', 'd'], ow: 18 },
    nhap(7),
  ]],
  dap: [
    `D1·1: a) 180 C · b) 900 s = 15 phút · c) 2,16·10<sup>3</sup> J &nbsp;|&nbsp; D1·2: a) 240 C · b) 1,44·10<sup>3</sup> J · c) 9,6·10<sup>−19</sup> J &nbsp;|&nbsp; D2·1: a) 12 V · b) 1,0 A · c) 2,0 Ω · d) 6,0 A &nbsp;|&nbsp; D2·2: a) 4,5 V · b) 1,0 A · c) 0,50 Ω · d) 9,0 A`,
    `D3·1: a<sub>1</sub>) 2,0 A · a<sub>2</sub>) 1,0 A · b<sub>1</sub>) 1,0 Ω · b<sub>2</sub>) 6,0 V · c) 6,0 A &nbsp;|&nbsp; D3·2: a<sub>1</sub>) 2,0 V · a<sub>2</sub>) 3,2 V · b<sub>1</sub>) 1,0 Ω · b<sub>2</sub>) 4,0 V · c) 4,0 A &nbsp;|&nbsp; D4·1: a<sub>1</sub>) 6,0 V · a<sub>2</sub>) 1,2 Ω · b) 1,0 A · c) 4,8 V · d) 0,50 A &nbsp;|&nbsp; D4·2: a<sub>1</sub>) 3,0 V · a<sub>2</sub>) 2,0 Ω · b) 0,50 A · c) 2,0 V · d) 1,0 A`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [2, 2], kq: [[1, 2], [3, 4]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'nguồn điện 1·4 · tụ – pin 2·1 · suất điện động 2·2 · điện trở trong 3·1 · Ohm toàn mạch 3·2 · ghép nguồn 4·1 · bẫy 4·2 · bài mẫu 5·1 · dạng 1–2 → 6·1 · dạng 3–4 → 7·1',
  out: process.argv[2],
});
