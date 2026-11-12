// Ruột tập VL11 – Bài 21 · Tụ điện (lesson id 40). Quyển Chương 3 lớp 11 (Điện trường): bài 21 = tr. 61–72.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l11-bai21.mjs (toàn bộ SVG tự vẽ, không dùng ảnh Halliday). Nội dung theo bài web (book/cache/40.json, tải từ DB 12/11/2026):
// mục tiêu, dự đoán đèn flash, II.1–II.5, ba thí nghiệm (LED nạp/phóng, đo Q theo U, tấm nhôm), ba bẫy, Trả bài 6 câu,
// bài toán mẫu hai tụ nối tiếp + điền bước song song + thử sức đổi số, thử thách 3 tầng, 5 dạng bài tập mẫu.
// Đáp số Bài tương tự (tuongTu.dap) tính bằng Python 12/11/2026; Bài tương tự giải vào vở (vo: true), xếp 2 cột bằng <style> riêng (ttHaiCot).
// Chạy: node scripts/ruot-tap/l11-bai21.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl11-bai21.pdf
//       node scripts/ruot-tap/l11-bai21.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l11-bai21/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL11b21 as H } from './hinh-l11-bai21.mjs';

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
  const out = resolve(HERE, 'out/hinh-l11-bai21'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 21, lid: 40, ten: 'TỤ ĐIỆN', lop: 11, baiDau: 16, sub: 'Vật lí 11 · Chương 3: Điện trường' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const u = (s) => nw(m(s));            // số + đơn vị KaTeX không gãy dòng
const uF = (v) => u(`${v}\\ \\mu\\mathrm F`), uC = (v) => u(`${v}\\ \\mu\\mathrm C`), V = (v) => u(`${v}\\ \\mathrm V`);
const C1 = m('C_1'), C2 = m('C_2'), C3 = m('C_3'), eps = m('\\varepsilon');

const ttHaiCot = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm}.yo .oo{flex:none;display:flex;gap:3mm}.yo{line-height:1.35}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';

const p1 = `${ttHaiCot}<section class="page">
${head('BÀI 21 · TỤ ĐIỆN', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Nói được <b>tụ điện</b> là gì, cách tích điện, vì sao nó chặn dòng một chiều`)}
${dong(`${ck}Dùng ${m('C=Q/U')}, đổi µF, nF, pF; biết ${m('C')} chỉ do <b>cấu tạo</b> quyết định`)}
${dong(`${ck}Tính <b>năng lượng</b> của tụ; giải bài ghép <b>nối tiếp</b>, <b>song song</b>`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Năng lượng cho cú loé chói trong tích tắc đến từ đâu?</p>
<div class="fig-side" style="${fs(42)}"><div>
${opt('A', 'Pin đẩy thẳng điện vào bóng đúng lúc bấm chụp')}
${opt('B', 'Một linh kiện gom điện tích từ pin trong vài giây, rồi xả hết một lần')}
${opt('C', 'Bóng đèn tự sinh năng lượng khi có ánh sáng chiếu vào')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 1)}</div>
${H.flash()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Tụ điện là gì', '1·4')}
<div class="card fig-side" style="${fs(40)};padding:1.2mm 3mm"><div>
<div><b>Cấu tạo:</b> hai ${f(16)} gần nhau, ngăn cách bằng ${f(16)}.</div>
<div><b>Tác dụng:</b> (động từ) ${f(14)} điện tích; xoay chiều: tích, ${f(12)} liên tục.</div>
<div><b>Tích điện:</b> nối hai bản với nguồn: bản nối cực + tích ${f(12)}, bản kia ${f(12)}.</div>
<div><b>Điện tích của tụ:</b> điện tích trên ${f(14)} bản (không cộng).</div>
</div>
${H.tuPhang()}</div>
${h3(5, 'Thí nghiệm: tụ nạp rồi tự xả qua đèn LED', '1·5')}
<div class="card fig-side" style="${fs(42)};padding:1.2mm 3mm"><div>
<div><b>Làm:</b> nối tiếp pin ${V(9)}, tụ ${uF(1000)}, LED. Tháo pin, nối tụ với LED đảo chiều.</div>
<div><b>Quan sát:</b> vừa nối pin, LED ${f(16)} rồi ${f(16)} dù pin còn nối. Nối tụ với LED: LED lại ${f(20)}.</div>
<div><b>Vì sao LED tắt hẳn dù pin còn nối?</b> Tụ đã ${f(16)}. Dòng một chiều ${ck}đi qua &nbsp;${ck}không đi qua tụ, vì giữa hai bản là chất ${f(16)}.</div></div>
${H.ledMach()}</div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('ĐIỆN DUNG · ĐO Q THEO U · C DO CẤU TẠO')}
${h3(1, 'II.2 · Điện dung', '2·1')}
<div class="card fig-side" style="${fs(52)};padding:1.2mm 3mm"><div>
<div>Điện dung đặc trưng cho khả năng ${f(25)} của tụ:</div>
<div style="margin:.6mm 0;font-size:3.7mm">${m('C=')} ${f(14)} &nbsp;&nbsp; ${m('\\Rightarrow\\ Q=')} ${f(14)}</div>
<div>Đơn vị: ${f(18)} (F). 1 F là điện dung của tụ tích được ${f(10)} khi đặt vào ${f(10)}.</div>
<div><b>Tụ xoay:</b> điện dung đổi được khi xoay ${f(18)} (dò đài radio).</div>
<div style="margin-top:.6mm"><b>Vỏ ghi</b> “${uF(1000)} – ${V(10)}”: ${f(35)} và ${f(50)}; vượt: tụ bị ${f(16)}.</div></div>
<table><tr><th>Ước số</th><th>Quy đổi</th></tr>
<tr><td>1 mF</td><td>${m('10^{-3}')} F</td></tr>
<tr><td>1 µF</td><td style="height:6mm"></td></tr>
<tr><td>1 nF</td><td></td></tr>
<tr><td>1 pF</td><td></td></tr></table></div>
${h3(2, 'Thí nghiệm đo: Q theo U của tụ ghi “470 µF – 16 V”', '2·2')}
<div class="fig-side" style="${fs(52)}"><div>
<table class="tbl-ct"><tr><th>${m('U\\ (\\mathrm V)')}</th><th>${m('Q\\ (\\mu\\mathrm C)')}</th><th>${m('Q/U\\ (\\mu\\mathrm F)')}</th></tr>
<tr><td>2</td><td>980</td><td></td></tr>
<tr><td>4</td><td>1900</td><td></td></tr>
<tr><td>6</td><td>2890</td><td></td></tr>
<tr><td>8</td><td>3820</td><td></td></tr>
<tr><td>10</td><td>4800</td><td></td></tr></table>
<div style="margin-top:.8mm">Trung bình ${m('Q/U\\approx')} ${f(14)} µF. Vỏ ghi 470 µF; lệch vì sai số ${f(25)}.</div>
<div><b>Rút ra:</b> ${m('Q')} tỉ lệ ${f(16)} với ${m('U')}; tỉ số ${m('Q/U')} gần như ${f(16)}, đó là ${f(8)}.</div></div>
${H.doThiQU()}</div>
${h3(3, 'II.3 · C do cấu tạo quyết định', '2·3')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div>${m('C')} chỉ phụ thuộc ${f(30)}, <b>không</b> phụ thuộc ${f(10)} hay ${f(10)}.</div>
<div style="margin:.6mm 0"><b>Tụ phẳng:</b> ${m('C=\\dfrac{\\varepsilon S}{9\\cdot10^{9}\\cdot4\\pi d}')} &nbsp;(${m('S')}: diện tích phần ${f(14)} của hai bản, đơn vị ${f(8)}; ${m('d')} đổi ra ${f(8)})</div>
<div>Điện trường giữa hai bản là đều: ${m('E=')} ${f(12)}. Điện môi chịu tối đa ${m('E_{\\max}')} nên ${m('U_{\\max}=')} ${f(14)}</div>
<div><b>Tấm nhôm:</b> gốc ${nw('≈ 350 pF')}. Tăng ${m('d')} gấp đôi: ≈ ${f(10)} pF; trượt lệch nửa tấm: ≈ ${f(10)} pF; chèn nhựa: ${m('C')} ${f(14)} vài lần.</div>
<div><b>Rút ra:</b> ${m('S')} lớn, ${m('d')} ${f(10)}, ${eps} ${f(10)} thì ${m('C')} lớn.</div></div>
${H.tamNhom()}</div>
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('NĂNG LƯỢNG CỦA TỤ · GHÉP TỤ · BA CÁI BẪY')}
${h3(1, 'II.4 · Năng lượng của tụ', '3·1')}
<div class="card fig-side" style="${fs(44)};padding:1.2mm 3mm"><div>
<div>Tụ tích điện thì giữa hai bản có ${f(25)}; nó dự trữ năng lượng điện trường.</div>
<div style="margin:.8mm 0;font-size:3.7mm">${m('W=\\tfrac12')}${f(12)} ${m('=\\tfrac12')}${f(12)} ${m('=')} ${f(14)} <span class="hint">(theo ${m('Q,U')} · ${m('C,U')} · ${m('Q,C')})</span></div>
<div>Còn nối nguồn (${m('U')} giữ): dùng ${f(16)} · đã ngắt nguồn (${m('Q')} giữ): dùng ${f(16)}</div>
<div>Vì sao có ½? Lúc nạp, ${m('U')} tăng dần từ ${f(8)}; ${m('W')} là diện tích ${f(20)} dưới đường ${m('Q')}–${m('U')}.</div>
<div>Cùng một tụ, nạp ở ${m('U')} gấp đôi thì ${m('W')} gấp ${f(8)} lần.</div>
<div><b>Ví dụ:</b> tụ flash ${uF(150)} nạp tới ${V(300)}: ${m('W=')} ${f(20)} J.</div></div>
${H.tamGiac()}</div>
${h3(2, 'II.5 · Ghép tụ', '3·2')}
<div class="fig-side" style="${fs(42)}"><div><table>
<tr><th style="width:12mm">Ghép</th><th>Nối tiếp</th><th>Song song</th></tr>
<tr><td>${m('Q')}</td><td style="height:6mm"></td><td></td></tr>
<tr><td>${m('U')}</td><td style="height:6mm"></td><td></td></tr>
<tr><td>${m('C')} bộ</td><td style="height:8mm"></td><td></td></tr>
<tr><td>So với</td><td>${ck}lớn hơn ${ck}nhỏ hơn tụ nhỏ nhất</td><td>${ck}lớn hơn ${ck}nhỏ hơn tụ lớn nhất</td></tr></table>
<div style="margin-top:.6mm">Hai tụ nối tiếp: ${m('C=')} ${f(20)} · Công thức ghép chỉ đúng khi các tụ ${f(25)} trước lúc ghép.</div>
<div><b>Tụ đã tích sẵn:</b> ${uF(2)} đã tích ${uC(20)} nối song song (+ với +) với ${uF(3)} chưa tích. Bảo toàn điện tích: ${m('U=')} ${f(10)} V; ${m('Q_1=')} ${f(10)} µC; ${m('Q_2=')} ${f(10)} µC.</div></div>
${H.ghep()}</div>
${h3(3, 'III · Ba cái bẫy hay sập', '3·3')}
<div class="card fig-side" style="${fs(42)};padding:1mm 3mm"><div>
<div class="trap">${ck}<span><b>“${m('C=Q/U')} nên tăng ${m('U')} thì ${m('C')} giảm.”</b> Sai: tụ nối 6 V đổi sang 12 V: ${m('C')} ${f(20)}, chỉ ${m('Q')} ${f(20)}.</span></div>
<div class="trap">${ck}<span><b>“Nối tiếp thì ${m('U')} chia đều.”</b> Sai: ${m('Q')} bằng nhau nên ${m('U_i=Q/C_i')}, tụ ${f(12)} gánh ${m('U')} lớn. ${uF(4)} nối tiếp ${uF(12)}: ${m('C=')} ${f(12)} µF.</span></div>
<div class="trap">${ck}<span><b>Nối nguồn hay ngắt nguồn?</b> Còn nối: ${f(8)} giữ · đã ngắt: ${f(8)} giữ. Ngắt nguồn, kéo hai bản xa gấp đôi: ${m('C')} ${f(16)}, ${m('U')} ${f(16)}.</span></div></div>
${H.nguon()}</div>
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('TRẢ BÀI · BÀI TOÁN MẪU')}
${h3(1, 'IV · Trả bài 6 câu', '4·1')}
${box(`${tb('1. Tụ điện là gì? Tích điện cho tụ thế nào?')}${lines(1)}
${tb('2. Định nghĩa điện dung, đơn vị, ước số?')}${lines(1)}
${tb('3. C phụ thuộc vào gì? Công thức tụ phẳng?')}${lines(1)}
${tb('4. Ba dạng công thức năng lượng của tụ?')}${lines(1)}
${tb('5. Nối tiếp, song song: cái gì chung, C bộ tính sao?')}${lines(2)}
${tb(`6. Vỏ tụ ghi “${nw('1000 µF – 10 V')}” nghĩa là gì? Quá 10 V thì sao?`)}${lines(1)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/6 câu · chưa thuộc: ${f(25)} ${nw(`→ đọc lại ô ${f(12)} Tập`)}</div>
${h3(2, 'V · Bài toán mẫu: hai tụ nối tiếp', '4·2')}
<div class="card soft fig-side" style="${fs(40)};padding:1.2mm 3mm"><div>Hai tụ chưa tích điện, ${m('C_1=3\\ \\mu\\mathrm F')} và ${m('C_2=6\\ \\mu\\mathrm F')}, ghép nối tiếp rồi nối vào nguồn ${m('U=12\\ \\mathrm V')}.
<div><b>a)</b> Tính điện dung của bộ và điện tích của mỗi tụ.</div><div><b>b)</b> Tính hiệu điện thế trên mỗi tụ và năng lượng của bộ.</div></div>${H.baiMau()}</div>
<table><tr><th style="width:44mm">Câu trong đề</th><th>Dữ liệu → kiến thức</th></tr>
<tr><td>“chưa tích điện”</td><td>Ban đầu ${m('Q=0')} → dùng được công thức ghép</td></tr>
<tr><td style="height:6mm">“ghép nối tiếp”</td><td></td></tr>
<tr><td style="height:6mm">“nối vào nguồn 12 V”</td><td></td></tr>
<tr><td style="height:6mm">“năng lượng của bộ”</td><td></td></tr></table>
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm;margin-top:1mm">
${wl(`Điện dung bộ ${m('C')}:`, 2)}${wl(`Điện tích ${m('Q_1, Q_2')}:`, 2)}${wl(`Hiệu điện thế ${m('U_1, U_2')}:`, 2)}${wl(`Năng lượng ${m('W')} (ra J và µJ):`, 2)}${wl(`Kiểm tra: ${m('U_1+U_2=')} ? Tụ nào gánh ${m('U')} lớn hơn?`, 1)}</div>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('TỰ KIỂM TRA · ĐIỀN BƯỚC · BTVN · THỬ THÁCH')}
${h3(1, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '5·1')}
${rkHai([1, 2, 3], [4, 5, 6])}
${h3(2, 'Điền bước còn thiếu: cùng hai tụ, ghép song song vào 12 V', '5·2')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div class="ln"><b>Bước 1 (cho sẵn):</b> ${m('C=C_1+C_2=9\\ \\mu\\mathrm F')}; ${m('U_1=U_2=12\\ \\mathrm V')}; ${m('Q_1=C_1U=36\\ \\mu\\mathrm C')}</div>
${wl(`Bước 2: ${m('Q_2=')} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; kiểm: ${m('Q_1+Q_2=CU')}?`, 1)}${wl(`Bước 3: ${m('W')} của bộ ${m('=')}`, 1)}</div>
<div class="card soft" style="margin-top:1mm;padding:1mm 3mm"><b>Thử sức đổi số:</b> ${uF(2)} và ${uF(6)} nối tiếp vào ${V(16)}. Hiệu điện thế trên tụ ${uF(2)}: ${f(14)} V${lines(1)}</div>
${K.btvn().replace('<i>1</i>', '<i>3</i>')}
${h3(4, 'Thử thách phân tầng', '5·4')}
<div class="fig-side" style="${fs(44)}">${box(wl(`${m('\\bigstar')} Tụ ${uF(20)} nối vào nguồn ${V(10)}. Tính ${m('Q')} và ${m('W')}.`, 3)
 + wl(`${m('\\bigstar\\bigstar')} Tụ ${uF(2)} và tụ ${uF(4)}, mỗi tụ chịu tối đa ${V(50)}, ghép nối tiếp. Bộ chịu được tối đa bao nhiêu vôn?`, 3)
 + wl(`${m('\\bigstar\\bigstar\\bigstar')} Tụ phẳng nạp xong rồi ngắt nguồn, kéo hai bản ra xa gấp đôi. Năng lượng tăng hay giảm? Phần chênh đến từ đâu?`, 3))}${H.thuThach()}</div>
${h3(5, 'VI · Mang về: điều em dễ quên nhất', '5·5')}
${box(wl('1.', 2) + wl('2.', 2) + wl('3.', 2))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Điện dung C = Q/U và đổi đơn vị',
    de: `Nối tụ A vào nguồn ${V('9{,}0')}; nạp đầy, tụ A tích ${uC(63)}. Tụ B có ghi “${u('4{,}7\\ \\mathrm{nF}')} – ${V(25)}”.<br><b>a)</b> điện dung tụ A, theo µF<br><b>b)</b> nối tụ A vào nguồn ${V(30)}: điện tích, theo µC<br><b>c)</b> điện tích lớn nhất tụ B tích được, theo nC`,
    nd: `${m('C=Q/U')}; µC/V = ${f(10)}; nF·V = ${f(10)}; số vôn trên vỏ là ${f(25)}`, a: ['a', 'b', 'c'], gi: 3 },
  { t: 'Dạng 2 · Dễ · Năng lượng của tụ điện',
    de: `Tụ ${uF(50)} được nạp tới ${V(40)}.<br><b>a)</b> điện tích và năng lượng của tụ<br><b>b)</b> nạp tới ${V(80)}: năng lượng gấp bao nhiêu lần lúc đầu<br><b>c)</b> nạp tới bao nhiêu vôn để năng lượng là ${u('0{,}25\\ \\mathrm J')}`,
    nd: `đổi µF ra ${f(8)} thì ${m('W')} ra J; cùng tụ thì ${m('W')} tỉ lệ với ${f(12)}`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'], gi: 3 },
  { t: 'Dạng 3 · Trung bình · Tụ phẳng: C theo cấu tạo, U tối đa',
    de: `Tụ phẳng: hai bản vuông cạnh ${u('30\\ \\mathrm{cm}')}, cách nhau ${u('2{,}0\\ \\mathrm{mm}')} trong không khí (${m('\\varepsilon=1')}); không khí chịu tối đa ${u('E_{\\max}=3\\cdot10^{6}\\ \\mathrm{V/m}')}.<br><b>a)</b> điện dung của tụ<br><b>b)</b> lấp đầy điện môi ${m('\\varepsilon=4')}: điện dung lúc này<br><b>c)</b> hiệu điện thế lớn nhất đặt vào tụ không khí mà không bị đánh thủng`,
    nd: `${m('S=a^2')} đổi ra ${f(8)}, ${m('d')} ra ${f(8)}; ${m('U_{\\max}=')} ${f(14)}`, a: ['a', 'b', 'c'], gi: 4, fig: H.tuVuong('30 cm', '2 mm', '') },
  { t: 'Dạng 4 · Trung bình · Ghép tụ hỗn hợp',
    de: `Ba tụ chưa tích điện ${m('C_1=5{,}0\\ \\mu\\mathrm F')}, ${m('C_2=20\\ \\mu\\mathrm F')}, ${m('C_3=6{,}0\\ \\mu\\mathrm F')}: ${C1} nối tiếp ${C2}, nhánh đó song song với ${C3}. Nối bộ vào nguồn ${V(60)}.<br><b>a)</b> điện dung của bộ<br><b>b)</b> điện tích của tụ ${C3}<br><b>c)</b> điện tích và hiệu điện thế của tụ ${C1}`,
    nd: `gộp nhánh ${f(14)} thành một tụ, rồi ${f(14)}; mỗi nhánh đều chịu ${f(10)} V`, a: ['a', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'], gi: 7, fig: H.honHop('') },
  { t: 'Dạng 5 · Khó · Ngắt nguồn, kéo hai bản ra xa: năng lượng và công',
    de: `Tụ phẳng không khí ${m('C_0=40\\ \\mathrm{nF}')} nạp tới ${V(150)} rồi ngắt khỏi nguồn. Kéo hai bản ra xa đến khi khoảng cách tăng gấp ba.<br><b>a)</b> điện tích và năng lượng trước khi kéo<br><b>b)</b> hiệu điện thế và năng lượng sau khi kéo<br><b>c)</b> công cần thực hiện để kéo hai bản ra xa`,
    nd: `ngắt nguồn ⇒ ${f(8)} giữ; ${m('d')} gấp ba ⇒ ${m('C')} ${f(18)}; ${m('A=')} ${f(16)}`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], gi: 8, fig: H.keoBan(''), cot: 3 },
];

// Bài tương tự giải vào vở (thầy chốt 10/11): 1 cột; ô đáp số cuối đúng dòng của ý (nhãn khớp a) b) c)…; a<sub>1</sub>, a<sub>2</sub> khi ý có 2 kết quả).
// Đáp số tính bằng Python 12/11/2026 (k = 9·10⁹, làm tròn 3 chữ số có nghĩa).
const oY = (s, o, w = 25) => s.split('<br>').map((p) => {
  const y = p.match(/^<b>([a-d])\)<\/b>/);
  if (!y) return `<div>${p}</div>`;
  const ls = o.filter((l) => l[0] === y[1]);
  return `<div class="yo"><span>${p}</span><span class="oo">${ls.map((l) => `<span class="nw"><b>${l})</b>${f(w)}</span>`).join('')}</span></div>`;
}).join('');
const ttDe = (b) => b.fig ? `<div class="fig-side" style="grid-template-columns:1fr ${b.fw}mm">${`<div>${oY(b.de, b.o, b.ow)}</div>`}${b.fig}</div>` : oY(b.de, b.o, b.ow);
const vaoVo = (ds) => ds.map((b) => (b.o ? { t: b.t, de: ttDe(b), k: 0 } : b));
const nhap = (n) => ({ t: '<span class="nhap-t">Nháp / chỗ em còn vướng</span>', de: lines(n), k: 0 });
const kk = '\\ (k=9\\cdot10^{9}\\ \\mathrm{N\\cdot m^2/C^2})';
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–3', 'DẠNG 4–5'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Nối tụ vào nguồn ${V(12)}, nạp đầy tụ tích ${uC(36)}.<br><b>a)</b> điện dung của tụ, theo µF<br><b>b)</b> nối tụ đó vào nguồn ${V('5{,}0')}: điện tích, theo µC<br><b>c)</b> tụ khác ghi “${uF(220)} – ${V(16)}”: điện tích lớn nhất, theo mC`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 1 · Bài 2', de: `Tụ có ghi “${u('470\\ \\mathrm{pF}')} – ${V(50)}”.<br><b>a)</b> điện dung theo F (viết dạng ${m('a\\cdot10^{n}')})<br><b>b)</b> nối tụ vào nguồn ${V(20)}: điện tích, theo nC<br><b>c)</b> điện tích lớn nhất tụ tích được, theo nC`, o: ['a', 'b', 'c'], ow: 30 },
    { t: 'Dạng 2 · Bài 1', de: `Tụ ${uF(20)} được nạp tới ${V(100)}.<br><b>a)</b> điện tích và năng lượng của tụ<br><b>b)</b> nạp tới ${V(50)}: năng lượng bằng mấy phần lúc đầu<br><b>c)</b> nạp tới bao nhiêu vôn để năng lượng là ${u('0{,}90\\ \\mathrm J')}`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'], ow: 20 },
    { t: 'Dạng 2 · Bài 2', de: `Máy khử rung tim dùng tụ ${uF(100)} nạp tới ${V(2000)}.<br><b>a)</b> điện tích của tụ<br><b>b)</b> năng lượng của tụ<br><b>c)</b> muốn xả ${u('50\\ \\mathrm J')} thì nạp tụ tới bao nhiêu vôn`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 3 · Bài 1', de: `Tụ phẳng: hai bản vuông cạnh ${u('10\\ \\mathrm{cm}')}, cách nhau ${u('0{,}50\\ \\mathrm{mm}')} trong không khí ${m(kk)}; không khí chịu tối đa ${u('3\\cdot10^{6}\\ \\mathrm{V/m}')}.<br><b>a)</b> điện dung, theo pF<br><b>b)</b> lấp đầy điện môi ${m('\\varepsilon=2')}: điện dung, theo pF<br><b>c)</b> hiệu điện thế lớn nhất cho tụ không khí`, fig: H.tuVuong('10 cm', '0,5 mm', ''), fw: 40, o: ['a', 'b', 'c'] },
    { t: 'Dạng 3 · Bài 2', de: `Tụ phẳng không khí, diện tích đối diện ${u('0{,}040\\ \\mathrm{m^2}')}, hai bản cách ${u('2{,}0\\ \\mathrm{mm}')} ${m(kk)}, nối vào nguồn ${V(120)}.<br><b>a)</b> điện dung, theo pF<br><b>b)</b> cường độ điện trường giữa hai bản<br><b>c)</b> điện tích của tụ, theo nC`, o: ['a', 'b', 'c'], ow: 30 },
  ], [
    { t: 'Dạng 4 · Bài 1', de: `Ba tụ chưa tích điện: ${m('C_1=3\\ \\mu\\mathrm F')} nối tiếp ${m('C_2=6\\ \\mu\\mathrm F')}, nhánh đó song song với ${m('C_3=4\\ \\mu\\mathrm F')}; nguồn ${V(30)}.<br><b>a)</b> điện dung của bộ<br><b>b)</b> điện tích của ${C3}<br><b>c)</b> điện tích và hiệu điện thế của ${C1}`, o: ['a', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'], ow: 20 },
    { t: 'Dạng 4 · Bài 2', de: `Ba tụ chưa tích điện: ${m('C_1=2\\ \\mu\\mathrm F')} song song ${m('C_2=4\\ \\mu\\mathrm F')}, cụm đó nối tiếp ${m('C_3=3\\ \\mu\\mathrm F')}; nguồn ${V(18)}.<br><b>a)</b> điện dung của bộ<br><b>b)</b> điện tích của ${C3}<br><b>c)</b> hiệu điện thế của ${C3}<br><b>d)</b> điện tích của ${C1}`, fig: H.honHop2(''), fw: 42, o: ['a', 'b', 'c', 'd'] },
    { t: 'Dạng 5 · Bài 1', de: `Tụ phẳng không khí ${u('20\\ \\mathrm{nF}')} nạp tới ${V(100)} rồi ngắt khỏi nguồn; kéo hai bản ra xa đến khi khoảng cách tăng gấp đôi.<br><b>a)</b> điện tích và năng lượng trước khi kéo<br><b>b)</b> hiệu điện thế và năng lượng sau khi kéo<br><b>c)</b> công cần thực hiện`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], ow: 20 },
    { t: 'Dạng 5 · Bài 2', de: `Tụ phẳng có điện môi ${m('\\varepsilon=2')} lấp đầy, ${u('C=30\\ \\mathrm{nF}')} (đã có điện môi), nạp tới ${V(200)} rồi ngắt khỏi nguồn; rút tấm điện môi ra (còn không khí).<br><b>a)</b> điện tích và năng lượng lúc đầu<br><b>b)</b> hiệu điện thế và năng lượng sau khi rút<br><b>c)</b> công cần thực hiện để rút tấm điện môi`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], ow: 20 },
    nhap(6),
  ]],
  dap: [
    `D1·1: a) 3,0 µF · b) 15 µC · c) 3,52 mC &nbsp;|&nbsp; D1·2: a) ${nw('4,7·10<sup>−10</sup> F')} · b) 9,4 nC · c) 23,5 nC &nbsp;|&nbsp; D2·1: a<sub>1</sub>) 2,0 mC · a<sub>2</sub>) 0,10 J · b) ¼ (giảm 4 lần) · c) 300 V &nbsp;|&nbsp; D2·2: a) 0,20 C · b) 200 J · c) 1000 V &nbsp;|&nbsp; D3·1: a) 177 pF · b) 354 pF · c) 1500 V &nbsp;|&nbsp; D3·2: a) 177 pF · b) ${nw('6,0·10<sup>4</sup> V/m')} · c) 21,2 nC`,
    `D4·1: a) 6,0 µF · b) 120 µC · c<sub>1</sub>) 60 µC · c<sub>2</sub>) 20 V &nbsp;|&nbsp; D4·2: a) 2,0 µF · b) 36 µC · c) 12 V · d) 12 µC &nbsp;|&nbsp; D5·1: a<sub>1</sub>) 2,0 µC · a<sub>2</sub>) 100 µJ · b<sub>1</sub>) 200 V · b<sub>2</sub>) 200 µJ · c) 100 µJ &nbsp;|&nbsp; D5·2: a<sub>1</sub>) 6,0 µC · a<sub>2</sub>) 600 µJ · b<sub>1</sub>) 400 V · b<sub>2</sub>) 1200 µJ · c) 600 µJ`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 2], kq: [[1, 2, 3], [4, 5]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'tụ điện 1·4 · LED 1·5 · điện dung 2·1 · đo Q–U 2·2 · cấu tạo 2·3 · năng lượng 3·1 · ghép tụ 3·2 · bẫy 3·3 · bài toán mẫu 4·2 · dạng 1–3 → 6·1 · dạng 4–5 → 7·1',
  out: process.argv[2],
});
