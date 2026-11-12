// Ruột tập VL11 – Bài 25 · Năng lượng điện và công suất điện (lesson id 44). Quyển Chương 4 lớp 11: bài 22 = tr. 1–12, bài 25 = tr. 37–48.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l11-bai25.mjs (toàn bộ SVG tự vẽ). Nội dung theo bài web (book/cache/44.json, tải từ DB 12/11/2026): mục tiêu,
// dự đoán số điện của đèn 100 W, II.1–II.5, ví dụ công tơ + thí nghiệm đèn xe máy + hiệu suất hai pin AA, ba bẫy, Trả bài 6 câu,
// bài toán mẫu nguồn nuôi bộ sấy, thử thách ⭐–⭐⭐⭐, 5 dạng bài tập mẫu. Đáp số Bài tương tự (tuongTu.dap) tính bằng Python 12/11/2026.
// Chạy: node scripts/ruot-tap/l11-bai25.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl11-bai25.pdf
//       node scripts/ruot-tap/l11-bai25.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l11-bai25/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL11b25 as H } from './hinh-l11-bai25.mjs';

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
  const out = resolve(HERE, 'out/hinh-l11-bai25'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 25, lid: 44, ten: 'NĂNG LƯỢNG ĐIỆN · CÔNG SUẤT ĐIỆN', lop: 11, baiDau: 22, sub: 'Vật lí 11 · Chương 4: Dòng điện. Mạch điện' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const E = m('\\mathcal E'), Ir = m('I^2r'), Om = m('\\Omega');
const kWh = nw(m('1\\ \\mathrm{kWh}=3{,}6\\cdot10^6\\ \\mathrm J'));
const gia = nw(m('2500') + ' đồng/kWh');
const u = (s) => nw(m(s));   // số + đơn vị không gãy dòng
const V = (s) => u(`${s}\\ \\mathrm V`), W = (s) => u(`${s}\\ \\mathrm W`), A_ = (s) => u(`${s}\\ \\mathrm A`), O = (s) => u(`${s}\\ \\Omega`);
const nhan = (a, b) => nw(`${a} V – ${b} W`);

// Bài tương tự 1 cột, ô đáp số cuối dòng của ý (cùng cách l11-bai16).
const ttCss = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';

const p1 = `${ttCss}<section class="page">
${head('BÀI 25 · NĂNG LƯỢNG ĐIỆN VÀ CÔNG SUẤT ĐIỆN', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Tính <b>năng lượng điện</b> ${m('A=UIt')} và <b>công suất điện</b> ${m('P=UI')}; đổi jun sang kWh; đọc nhãn thiết bị`)}
${dong(`${ck}Phân biệt công suất <b>của nguồn</b> với công suất <b>mạch ngoài</b>; tính <b>hiệu suất</b> nguồn`)}
${dong(`${ck}Giải thích vì sao <b>đoản mạch</b> gây cháy; chọn <b>cầu chì</b>`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Hoá đơn tiền điện ghi “312 kWh”, mẹ gọi là “312 số điện”. Một bóng đèn ${W('100')} sáng liên tục 10 giờ “ăn” bao nhiêu số điện?</p>
<div class="fig-side" style="${fs(40)}"><div>
${opt('A', '100 số, vì công suất là 100 W')}
${opt('B', '1000 số, vì 100 nhân 10')}
${opt('C', '1 số')}
${opt('D', '10 số, vì sáng 10 giờ')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 1)}</div>
${H.congTo()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Năng lượng điện tiêu thụ', '1·4')}
<div class="card" style="padding:1.2mm 3mm">
<div>Dòng điện qua đoạn mạch: lực điện thực hiện công ${m('A=qU')}; mà ${m('q=')} ${f(12)} nên</div>
<div style="margin:.8mm 0;display:flex;align-items:flex-end;gap:3mm">${m('A=')} <span class="fill" style="min-width:26mm"></span> <span>đơn vị: ${m('U')} (V), ${m('I')} (A), ${m('t')} (${f(10)}) thì ${m('A')} ra ${f(14)}</span></div>
<div>Điện năng biến thành: nhiệt (bàn là), ${f(12)} (quạt), ${f(12)} (sạc pin), quang (đèn LED).</div>
<div>Chỉ toả nhiệt (định luật Jun–Len-xơ): ${m('Q=UIt=')} <span class="fill" style="min-width:16mm"></span> ${m('=')} <span class="fill" style="min-width:16mm;height:9mm"></span></div>
<div>Cho sẵn: ${kWh} (thiết bị 1 kW dùng trong 1 giờ). Công tơ điện đếm ${f(20)}, không đo ${f(20)}.</div>
</div>
${h3(5, 'Ví dụ: đọc công tơ khi đun ấm nước', '1·5')}
<div class="card" style="padding:1.2mm 3mm">
<div><b>Làm:</b> tắt mọi thiết bị, chỉ cắm ấm siêu tốc ${W('1800')} chạy liên tục đúng 10 phút. Chỉ số công tơ: ${u('1234{,}5\\ \\mathrm{kWh}')} lúc bật → ${u('1234{,}8\\ \\mathrm{kWh}')} lúc tắt.</div>
<div><b>Rút ra:</b> công tơ tăng ${f(14)} kWh. Tính: ${m('A=Pt=')} ${f(14)} kW · ${f(10)} h ${m('=')} ${f(12)} kWh ${m('=')} ${f(20)} J.</div>
</div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('CÔNG SUẤT ĐIỆN · NHÃN THIẾT BỊ')}
${h3(1, 'Làm nhanh', '2·1')}
${box(cau(`Bàn là mắc vào ${V('220')}, dòng ${A_('4{,}0')}, dùng 15 phút. Năng lượng điện tiêu thụ (kJ và kWh)?`, 2))}
${h3(2, 'II.2 · Công suất điện', '2·2')}
<div class="card fig-side" style="${fs(40)};padding:1.2mm 3mm"><div>
<div>Công suất điện là ${f(36)} tiêu thụ trong ${f(16)}.</div>
<div style="margin:1mm 0;display:flex;align-items:flex-end;gap:2mm">${m('P=\\tfrac{A}{t}=')} <span class="fill" style="min-width:12mm"></span> · chỉ toả nhiệt: ${m('P=')} <span class="fill" style="min-width:12mm"></span>${m('=')}<span class="fill" style="min-width:14mm;height:9mm"></span></div>
<div>Đơn vị: oát, ${m('1\\ \\mathrm W=1')} ${f(10)}.</div>
<div>Nhãn ${nhan(220, 100)}: ${nw(`${m('U')}<sub>đm</sub>${m('=')}`)} ${f(12)} là hiệu điện thế ${f(20)}; ${nw(`${m('P')}<sub>đm</sub>${m('=')}`)} ${f(12)} là công suất khi dùng đúng ${f(12)}.</div>
<div>Từ nhãn: ${nw(`${m('I')}<sub>đm</sub>${m('=')}`)} <span class="fill" style="min-width:14mm;height:9mm"></span> ; ${m('R=')} <span class="fill" style="min-width:14mm;height:9mm"></span> ${m('=')} ${f(16)}</div></div>
${H.nhan()}</div>
${h3(3, 'Thí nghiệm: kiểm nhãn đèn xe máy 12 V – 21 W', '2·3')}
<div class="card fig-side" style="${fs(42)};padding:1.2mm 3mm"><div>
<div><b>Làm:</b> đặt hiệu điện thế ${V('12{,}0')}, rồi ${V('9{,}0')} và ${V('6{,}0')}; đọc ampe kế.</div>
<table class="tbl-ct" style="margin:.8mm 0"><tr><th>${m('U')} (V)</th><th>12,0</th><th>9,0</th><th>6,0</th></tr>
<tr><td>${m('I')} (A)</td><td>1,75</td><td>1,55</td><td>1,30</td></tr>
<tr><td>${m('P=UI')} (W)</td><td></td><td></td><td></td></tr>
<tr><td>${m('R=U/I')} (${Om})</td><td></td><td></td><td></td></tr></table>
<div><b>Rút ra:</b> ở ${V('12{,}0')} công suất ${f(16)} nhãn. Đèn mờ thì ${m('R')} ${f(16)} vì dây tóc ${f(16)}. Bài tập ghi “coi ${m('R')} không đổi” là phép ${f(18)}.</div></div>
${H.denXe()}</div>
${h3(4, 'Làm nhanh', '2·4')}
${box(cau(`Đèn ${nhan(220, 100)} mắc vào ${V('110')}, coi ${m('R')} không đổi. Công suất thực? Vì sao không phải ${W('50')}?`, 2))}
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('CÔNG SUẤT NGUỒN · HIỆU SUẤT · ĐOẢN MẠCH')}
${h3(1, 'II.3 · Công và công suất của nguồn điện', '3·1')}
<div class="card fig-side" style="${fs(42)};padding:1.2mm 3mm"><div>
<div>Nguồn đẩy điện lượng ${m('q=It')} qua cả mạch kín: ${m('A_{ng}=')} ${f(16)} · ${m('P_{ng}=')} ${f(14)}</div>
<div>Bài 24: ${m('U=')} ${f(16)}. Nhân hai vế với ${m('I')}:</div>
<div style="margin:.6mm 0">${m('\\mathcal EI=')} ${f(14)} ${m('+')} ${f(14)} · mạch ngoài nhận ${f(10)} (có ích), nguồn tự nóng ${f(10)} (hao phí)</div>
<div>Ví dụ: sạc dự phòng ấm lên khi xả dòng lớn là do ${f(14)} toả ngay trong pin.</div></div>
${H.canBang()}</div>
${h3(2, 'II.4 · Hiệu suất của nguồn điện', '3·2')}
<div class="card fig-side" style="${fs(40)};padding:1.2mm 3mm"><div>
<div style="display:flex;align-items:flex-end;gap:2mm;margin-bottom:.6mm">${m('H=\\tfrac{A_{\\text{ci}}}{A_{\\text{tp}}}=')}<span class="fill" style="min-width:14mm;height:9mm"></span>${m('=')}<span class="fill" style="min-width:12mm;height:9mm"></span> · thuần điện trở: ${m('H=')}<span class="fill" style="min-width:14mm;height:9mm"></span></div>
<div>Mạch ngoài có quạt, động cơ, pin đang sạc: chỉ dùng ${m('H=')} ${f(12)}</div>
<div><b>Thí nghiệm:</b> hai pin AA nối tiếp (${m('\\mathcal E=3{,}0\\ \\mathrm V')}, ${m('r=1{,}0\\ \\Omega')}), đổi ${m('R')}, đọc ${m('U')}, ${m('I')}.</div>
<table class="tbl-ct" style="margin:.6mm 0"><tr><th>${m('R')} (${Om})</th><th>1,0</th><th>2,0</th><th>4,0</th><th>9,0</th></tr>
<tr><td>${m('I')} (A)</td><td>1,50</td><td>1,00</td><td>0,60</td><td>0,30</td></tr>
<tr><td>${m('U')} (V)</td><td>1,50</td><td>2,00</td><td>2,40</td><td>2,70</td></tr>
<tr><td>${m('H=U/\\mathcal E')}</td><td></td><td></td><td></td><td></td></tr></table>
<div><b>Rút ra:</b> ${m('R')} tăng thì ${m('H')} ${f(14)}; ${m('H')} có đạt 100 % không? ${f(30)}</div></div>
${H.haiPin()}</div>
${h3(3, 'II.5 · An toàn điện: đoản mạch và cầu chì', '3·3')}
<div class="card fig-side" style="${fs(36)};padding:1.2mm 3mm"><div>
<div>Đoản mạch: hai cực nguồn nối thẳng, ${m('R\\to0')}, dòng ${m('I=')} <span class="fill" style="min-width:10mm;height:9mm"></span> rất lớn vì ${m('r')} ${f(10)}.</div>
<div>Ắc quy ${V('12')}, ${m('r=0{,}02\\ \\Omega')} bị chìa khoá chạm hai cực: ${m('I\\approx')} ${f(12)} A, nhiệt trong ắc quy ${m('I^2r=')} ${f(14)} W.</div>
<div>Cầu chì / aptomat: tự ${f(16)} khi dòng vượt dòng định mức. Chọn cầu chì có dòng định mức ${f(26)} dòng làm việc.</div>
<div>Ấm ${nhan(220, 1800)}: ${m('I=')} ${f(12)} A ${m('\\to')} chọn cầu chì ${f(10)} A (có 5 A, 10 A, 30 A).</div></div>
${H.doanMach()}</div>
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('BA CÁI BẪY · TRẢ BÀI · TỰ KIỂM TRA')}
${h3(1, 'III · Ba cái bẫy hay sập', '4·1')}
<div class="card fig-side" style="${fs(40)};padding:1mm 3mm"><div>
<div class="trap">${ck}<span><b>“kW và kWh là một.”</b> kW là ${f(16)} (ghi trên nhãn); kWh là ${f(16)} (ghi trên hoá đơn). Điều hoà ${u('1{,}2\\ \\mathrm{kW}')} chạy 8 giờ mỗi đêm, 30 đêm: ${f(12)} kWh.</span></div>
<div class="trap">${ck}<span><b>“Công suất nguồn là công suất mạch ngoài.”</b> Nguồn phát ${m('\\mathcal EI')}, lớn hơn ${m('UI')} một phần ${f(10)}. Nguồn ${V('9{,}0')}, ${m('r=0{,}5\\ \\Omega')}, ${m('R=4{,}0\\ \\Omega')}: ${m('P_{ng}=')} ${f(10)} W, mạch ngoài ${f(10)} W.</span></div>
<div class="trap">${ck}<span><b>“Đèn công suất lớn luôn sáng hơn.”</b> Nối tiếp (cùng ${m('I')}) dùng ${m('P=')} ${f(10)}: ${m('R')} lớn nhận nhiều hơn. Song song (cùng ${m('U')}) dùng ${m('P=')} ${f(10)}. Đèn sáng hơn: ${f(10)}</span></div></div>
${H.noiTiep()}</div>
${h3(2, 'IV · Trả bài 6 câu', '4·2')}
${box(`${tb('1. Năng lượng điện tiêu thụ: công thức, đơn vị, đo bằng gì?')}${lines(2)}
${tb('2. Công suất điện là gì? Ba cách viết?')}${lines(1)}
${tb('3. Nhãn “220 V – 60 W” cho biết gì? Điện trở đèn?')}${lines(2)}
${tb('4. Công, công suất của nguồn; khác công suất mạch ngoài chỗ nào?')}${lines(2)}
${tb('5. Hiệu suất nguồn: hai cách viết, suy ra từ đâu?')}${lines(2)}
${tb('6. Vì sao đoản mạch gây cháy? Chọn cầu chì thế nào?')}${lines(2)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/6 câu · chưa thuộc: ${f(25)} ${nw(`→ đọc lại ô ${f(12)} Tập`)}</div>
${h3(3, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '4·3')}
${rkHai([1, 2, 3, 4], [5, 6, 7, 8])}
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TOÁN MẪU · BÀI TẬP VỀ NHÀ · THỬ THÁCH')}
${h3(1, 'V · Bài toán mẫu: nguồn nuôi bộ sấy', '5·1')}
<div class="card soft" style="padding:1.2mm 3mm">Nguồn có ${m('\\mathcal E=12\\ \\mathrm V')}, ${m('r=1{,}0\\ \\Omega')} nối với dây điện trở bộ sấy ${m('R=5{,}0\\ \\Omega')}.<br><b>a)</b> ${m('I')} và hiệu điện thế hai cực nguồn<br><b>b)</b> công suất của nguồn, mạch ngoài, toả nhiệt trong nguồn<br><b>c)</b> hiệu suất nguồn<br><b>d)</b> năng lượng bộ sấy nhận trong 10 phút</div>
<table><tr><th style="width:46mm">Câu trong đề</th><th>Dữ liệu ${m('\\to')} kiến thức</th></tr>
<tr><td>“12 V … 1,0 ${Om}”</td><td>${m('\\mathcal E')}, ${m('r')} ${m('\\to')} nguồn thật có ${m('r')}</td></tr>
<tr><td style="height:6.5mm">(ngầm) mạch kín</td><td></td></tr>
<tr><td style="height:6.5mm">“trong 10 phút”</td><td></td></tr>
</table>
<div class="fig-side" style="${fs(42)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl(`a) ${m('I=')} ${m('\\Rightarrow')} ${m('U=')}`, 1)}${wl(`b) ${m('P_{ng}=')} · ${m('P_R=')} · ${m('P_r=')}`, 2)}${wl(`c) ${m('H=')}`, 1)}${wl(`d) ${m('A_R=')}`, 1)}</div>${H.sayMau()}</div>
${h3(2, `Điền bước còn thiếu: cùng nguồn, đổi R = 11 ${Om}`, '5·2')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div class="ln"><b>Cho sẵn:</b> ${m('I=12/(11+1{,}0)=1{,}0\\ \\mathrm A')}; ${m('P_{ng}=\\mathcal EI=12\\ \\mathrm W')}</div>
${wl(`${m('U=')} &nbsp; ${m('P_R=')} &nbsp; ${m('H=')}`, 1)}${wl(`${m('R')} tăng thì ${m('H')} …… nhưng ${m('P_R')} ……`, 1)}</div>
${K.btvn().replace('<i>1</i>', '<i>3</i>')}
${h3(4, 'Thử thách phân tầng', '5·4')}
${box(cau(`${m('\\bigstar')} Tủ lạnh trung bình ${W('50')}, chạy cả ngày đêm: số kWh và tiền điện một ngày (giá ${gia})?`, 1)
 + cau(`${m('\\bigstar\\bigstar')} Ấm ${nhan(220, 1800)} đun ${u('1{,}0\\ \\mathrm{kg}')} nước ${u('25\\to100\\ ^\\circ\\mathrm C')} hết ${u('200\\ \\mathrm s')}, ${u('c=4200\\ \\mathrm{J/(kg{\\cdot}K)}')}. Hiệu suất ấm?`, 1)
 + cau(`${m('\\bigstar\\bigstar\\bigstar')} ${m('\\mathcal E=12\\ \\mathrm V')}, ${m('r=1{,}0\\ \\Omega')}, ${m('R')} đổi được: ${m('R')} bằng bao nhiêu thì ${m('P_R')} lớn nhất? ${m('H')} lúc đó?`, 1))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Điện năng tiêu thụ và đổi jun sang kWh',
    de: `Bình nóng lạnh ${nhan(220, 2000)} bật đúng định mức 45 phút mỗi tối (${kWh}).<br><b>a)</b> điện năng bình tiêu thụ mỗi tối, theo jun<br><b>b)</b> đổi điện năng đó ra kWh<br><b>c)</b> số điện (kWh) trong 30 ngày`,
    nd: `Ra jun: ${m('P')} theo ${f(8)}, ${m('t')} theo ${f(10)}; ra kWh: ${m('P')} theo ${f(8)}, ${m('t')} theo ${f(10)}`, a: ['a', 'b', 'c'], gi: 3 },
  { t: 'Dạng 2 · Dễ · Thiết bị dùng ở hiệu điện thế khác định mức',
    de: `Bàn là ghi ${nhan(220, 1100)}, cắm vào ổ chỉ có ${V('176')}. Coi điện trở bàn là không đổi.<br><b>a)</b> điện trở của bàn là<br><b>b)</b> cường độ dòng điện và công suất thực<br><b>c)</b> chạy liên tục 30 phút: điện năng tiêu thụ theo kWh`,
    nd: `${m('R=')} ${f(14)} từ nhãn; ${m('P')} tỉ lệ với ${f(10)}, không tỉ lệ với ${m('U')}`, a: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], gi: 3 },
  { t: 'Dạng 3 · Trung bình · Công suất nguồn và mạch ngoài',
    de: `Bộ pin ${m('\\mathcal E=6{,}0\\ \\mathrm V')}, ${m('r=0{,}40\\ \\Omega')} nối kín với điện trở sưởi ${m('R=2{,}6\\ \\Omega')}; bỏ qua dây nối.<br><b>a)</b> cường độ dòng điện<br><b>b)</b> công suất của nguồn, mạch ngoài nhận, toả nhiệt trong nguồn<br><b>c)</b> công của nguồn trong 5 phút`,
    nd: `Tìm ${m('I=')} ${f(14)} trước; kiểm ${m('P_{ng}=')} ${f(10)} ${m('+')} ${f(10)}`, a: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'b<sub>3</sub>', 'c'], cot: 5, gi: 5, fig: H.pinD3('Tìm I trước.') },
  { t: 'Dạng 4 · Khó · Hiệu suất nguồn, năng lượng có ích và hao phí',
    de: `Pin dự phòng ${m('\\mathcal E=12\\ \\mathrm V')}, ${m('r=0{,}75\\ \\Omega')} nối kín với biến trở ${m('R')} cấp điện cho thiết bị sưởi; chỉnh ${m('R')} để hiệu suất nguồn bằng 80 %; bỏ qua dây nối.<br><b>a)</b> giá trị ${m('R')}<br><b>b)</b> cường độ dòng điện; hiệu điện thế hai cực pin<br><b>c)</b> trong 10 phút: năng lượng mạch ngoài nhận; năng lượng toả ra trong pin`,
    nd: `Thuần điện trở: ${m('H=')} ${f(14)} ${m('\\to')} giải ngược ra ${m('R')}; ${nw(`${m('A')}<sub>ích</sub>${m('=')}`)} ${f(12)}, ${m('A_{\\text{hp}}=')} ${f(12)}`, a: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c<sub>1</sub>', 'c<sub>2</sub>'], cot: 5, gi: 7 },
  { t: 'Dạng 5 · Khó · Đoản mạch và chọn cầu chì',
    de: `Ắc quy xe máy ${m('\\mathcal E=12\\ \\mathrm V')}, ${m('r=0{,}030\\ \\Omega')}; bộ đèn điện trở ${O('2{,}37')} khi sáng, nối tiếp một cầu chì; có ba loại cầu chì ${A_('3')}, ${A_('7{,}5')}, ${A_('30')}; bỏ qua dây nối.<br><b>a)</b> dòng điện khi đèn sáng; chọn cầu chì nào<br><b>b)</b> dây chập nối tắt bộ đèn, điện trở mạch ngoài còn ${O('0{,}010')}: dòng điện và công suất toả nhiệt trong ắc quy<br><b>c)</b> dòng lúc chập gấp bao nhiêu lần dòng định mức cầu chì đã chọn; cầu chì có đứt không`,
    nd: `Lúc chập, ${m('r')} vẫn ${f(16)}: ${m('I=')} ${f(16)}; cầu chì định mức ${f(20)} dòng làm việc`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c<sub>1</sub>', 'c<sub>2</sub>'], cot: 6, gi: 7, fig: H.chapD5('Lúc chập, r vẫn trong mạch.') },
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
    { t: 'Dạng 1 · Bài 1', de: `Ấm siêu tốc ${nhan(220, 1500)}, mỗi ngày đun đúng hiệu điện thế định mức trong 20 phút (${kWh}).<br><b>a)</b> điện năng ấm tiêu thụ mỗi ngày, theo jun<br><b>b)</b> đổi điện năng đó ra kWh<br><b>c)</b> số điện (kWh) trong 30 ngày`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 1 · Bài 2', de: `Ti vi công suất ${W('120')} bật 5 giờ mỗi ngày (${kWh}; giá điện ${gia}).<br><b>a)</b> điện năng mỗi ngày, theo kWh<br><b>b)</b> điện năng đó theo jun<br><b>c)</b> tiền điện của ti vi trong 30 ngày`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 2 · Bài 1', de: `Đèn ${nhan(220, 60)} mắc vào ${V('110')}; coi điện trở đèn không đổi.<br><b>a)</b> điện trở của đèn<br><b>b)</b> cường độ dòng điện và công suất thực<br><b>c)</b> đèn sáng 4 giờ ở hiệu điện thế này: điện năng theo kWh`, o: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], ow: 20 },
    { t: 'Dạng 2 · Bài 2', de: `Bếp điện ${nhan(220, 1000)} cắm vào ổ chỉ có ${V('198')}; coi điện trở bếp không đổi.<br><b>a)</b> điện trở của bếp<br><b>b)</b> cường độ dòng điện và công suất thực<br><b>c)</b> bếp chạy liên tục 1 giờ: điện năng theo kWh`, o: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], ow: 20 },
    { t: 'Dạng 3 · Bài 1', de: `Nguồn ${m('\\mathcal E=12\\ \\mathrm V')}, ${m('r=0{,}50\\ \\Omega')} nối kín với ${m('R=5{,}5\\ \\Omega')}; bỏ qua dây nối.<br><b>a)</b> cường độ dòng điện<br><b>b)</b> công suất của nguồn, mạch ngoài nhận, toả nhiệt trong nguồn<br><b>c)</b> công của nguồn trong 10 phút`, o: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'b<sub>3</sub>', 'c'], ow: 16 },
    { t: 'Dạng 3 · Bài 2', de: `Nguồn ${m('\\mathcal E=9{,}0\\ \\mathrm V')}, ${m('r=1{,}0\\ \\Omega')} nối kín với ${m('R=2{,}0\\ \\Omega')}; bỏ qua dây nối.<br><b>a)</b> cường độ dòng điện; hiệu điện thế hai cực nguồn<br><b>b)</b> công suất của nguồn, mạch ngoài nhận, toả nhiệt trong nguồn<br><b>c)</b> nhiệt lượng toả ra trong nguồn trong 2 phút`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'b<sub>3</sub>', 'c'], ow: 16 },
  ], [
    { t: 'Dạng 4 · Bài 1', de: `Nguồn ${m('\\mathcal E=6{,}0\\ \\mathrm V')}, ${m('r=0{,}50\\ \\Omega')} nối kín với biến trở ${m('R')}; chỉnh ${m('R')} để hiệu suất nguồn bằng 75 %; bỏ qua dây nối.<br><b>a)</b> giá trị ${m('R')}<br><b>b)</b> cường độ dòng điện; hiệu điện thế hai cực nguồn<br><b>c)</b> trong 5 phút: năng lượng mạch ngoài nhận; năng lượng toả ra trong nguồn`, o: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c<sub>1</sub>', 'c<sub>2</sub>'], ow: 18 },
    { t: 'Dạng 4 · Bài 2', de: `Nguồn ${m('\\mathcal E=12\\ \\mathrm V')}, ${m('r=2{,}0\\ \\Omega')} nối kín với ${m('R=8{,}0\\ \\Omega')}; bỏ qua dây nối.<br><b>a)</b> hiệu suất nguồn<br><b>b)</b> cường độ dòng điện; hiệu điện thế hai cực nguồn<br><b>c)</b> muốn hiệu suất 90 % thì ${m('R')} bằng bao nhiêu; khi đó mạch ngoài nhận công suất bao nhiêu`, o: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c<sub>1</sub>', 'c<sub>2</sub>'], ow: 18 },
    { t: 'Dạng 5 · Bài 1', de: `Ắc quy ${m('\\mathcal E=12\\ \\mathrm V')}, ${m('r=0{,}040\\ \\Omega')}; bộ đèn điện trở ${O('2{,}36')} khi sáng, nối tiếp một cầu chì; có ba loại cầu chì ${A_('2')}, ${A_('6')}, ${A_('20')}; bỏ qua dây nối.<br><b>a)</b> dòng điện khi đèn sáng; chọn cầu chì nào<br><b>b)</b> dây chập, điện trở mạch ngoài còn ${O('0{,}020')}: dòng điện và công suất toả nhiệt trong ắc quy<br><b>c)</b> dòng lúc chập gấp bao nhiêu lần định mức cầu chì đã chọn; cầu chì có đứt không`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c<sub>1</sub>', 'c<sub>2</sub>'], ow: 16 },
    { t: 'Dạng 5 · Bài 2', de: `Bộ pin ${m('\\mathcal E=6{,}0\\ \\mathrm V')}, ${m('r=0{,}10\\ \\Omega')} nuôi quạt nhỏ coi như điện trở ${O('2{,}9')}, nối tiếp một cầu chì; có ba loại cầu chì ${A_('1')}, ${A_('3')}, ${A_('10')}; bỏ qua dây nối.<br><b>a)</b> dòng điện khi quạt chạy; chọn cầu chì nào<br><b>b)</b> một sợi dây kim loại chạm thẳng hai cực pin (${m('R\\approx0')}): dòng điện và công suất toả nhiệt trong pin<br><b>c)</b> dòng lúc chạm gấp bao nhiêu lần định mức cầu chì đã chọn`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], ow: 16 },
    nhap(5),
  ]],
  dap: [
    `D1·1: a) 1,8·10<sup>6</sup> J · b) 0,50 kWh · c) 15 kWh &nbsp;|&nbsp; D1·2: a) 0,60 kWh · b) 2,16·10<sup>6</sup> J · c) 45 000 đồng &nbsp;|&nbsp; D2·1: a) 807 ${Om} · b<sub>1</sub>) 0,136 A · b<sub>2</sub>) 15 W · c) 0,060 kWh &nbsp;|&nbsp; D2·2: a) 48,4 ${Om} · b<sub>1</sub>) 4,09 A · b<sub>2</sub>) 810 W · c) 0,81 kWh &nbsp;|&nbsp; D3·1: a) 2,0 A · b<sub>1</sub>) 24 W · b<sub>2</sub>) 22 W · b<sub>3</sub>) 2,0 W · c) 14 400 J &nbsp;|&nbsp; D3·2: a<sub>1</sub>) 3,0 A · a<sub>2</sub>) 6,0 V · b<sub>1</sub>) 27 W · b<sub>2</sub>) 18 W · b<sub>3</sub>) 9,0 W · c) 1080 J`,
    `D4·1: a) 1,5 ${Om} · b<sub>1</sub>) 3,0 A · b<sub>2</sub>) 4,5 V · c<sub>1</sub>) 4050 J · c<sub>2</sub>) 1350 J &nbsp;|&nbsp; D4·2: a) 80 % · b<sub>1</sub>) 1,2 A · b<sub>2</sub>) 9,6 V · c<sub>1</sub>) 18 ${Om} · c<sub>2</sub>) 6,48 W &nbsp;|&nbsp; D5·1: a<sub>1</sub>) 5,0 A · a<sub>2</sub>) 6 A · b<sub>1</sub>) 200 A · b<sub>2</sub>) 1600 W · c<sub>1</sub>) 33 lần · c<sub>2</sub>) đứt &nbsp;|&nbsp; D5·2: a<sub>1</sub>) 2,0 A · a<sub>2</sub>) 3 A · b<sub>1</sub>) 60 A · b<sub>2</sub>) 360 W · c) 20 lần`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 2], kq: [[1, 2, 3], [4, 5]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: `điện năng 1·4 · công suất, nhãn 2·2 · nguồn 3·1 · hiệu suất 3·2 · cầu chì 3·3 · bẫy 4·1 · bài mẫu 5·1 · dạng 1–3 ${m('\\to')} 6·1 · dạng 4–5 ${m('\\to')} 7·1`,
  out: process.argv[2],
});
