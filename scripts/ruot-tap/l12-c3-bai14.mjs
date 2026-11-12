// Ruột tập VL12 Chương 3 – Bài 14 · Máy phát điện xoay chiều. Máy biến áp (lesson id 125). Quyển Chương 3 lớp 12: bài 9 = tr. 1–12,
// bài 14 = tr. 61–72. KHÁC bai14.mjs (bài 14 Chương 4 hạt nhân) — file và PDF có '-c3-' để không ghi đè nhau.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l12-c3-bai14.mjs (toàn bộ SVG tự vẽ). Nội dung theo bài web (book/cache/125.json, tải từ DB 12/11/2026): mục tiêu,
// dự đoán đường dây 500 kV, II.1–II.5, thí nghiệm máy phát mini / ba cuộn dây / quấn cuộn thứ cấp / đèn 12 V dây dài, ba bẫy,
// Trả bài 6 câu, bài toán mẫu tổ máy 20 kW, thử thách ⭐–⭐⭐⭐, 5 dạng bài tập mẫu. Đáp số (mẫu + tương tự) tính bằng Python 12/11/2026.
// Chạy: node scripts/ruot-tap/l12-c3-bai14.mjs            → scripts/ruot-tap/out/ruot-tap-vl12-c3-bai14.pdf
//       node scripts/ruot-tap/l12-c3-bai14.mjs --hinh     → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l12-c3-bai14/ để soát chữ/nét
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL12c3b14 as H } from './hinh-l12-c3-bai14.mjs';
const HERE = dirname(fileURLToPath(import.meta.url));

if (process.argv[2] === '--hinh') {
  const { createRequire } = await import('node:module');
  const { existsSync, mkdirSync, writeFileSync } = await import('node:fs');
  const { pathToFileURL } = await import('node:url');
  const BOOK = [resolve(HERE, '../../book/'), '/Users/MAC/Projects/thachlab/book'].find((d) => existsSync(d + '/node_modules')) + '/';
  const puppeteer = createRequire(BOOK + 'package.json')('puppeteer-core');
  const F = resolve(HERE, 'fonts') + '/source-sans-3-';
  const css = ['latin', 'latin-ext', 'vietnamese'].flatMap((s) => [400, 700].map((w) => `@font-face{font-family:BV;font-weight:${w};src:url("${pathToFileURL(`${F}${s}-${w}-normal.woff2`).href}")}`)).join('')
    + 'body{margin:0;font-family:BV,sans-serif;zoom:4}.fig{margin:0;width:46mm;border:.3mm solid #d3dbec;border-radius:1.5mm;padding:1mm 1.5mm .6mm;background:#fff}.fig svg{display:block;width:100%;height:auto}figcaption{font-size:2.95mm;color:#5f6a88;line-height:1.3;margin-top:.4mm}';
  const out = resolve(HERE, 'out/hinh-l12-c3-bai14'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 14, lid: 125, ten: 'MÁY PHÁT ĐIỆN XOAY CHIỀU · MÁY BIẾN ÁP', lop: 12, baiDau: 9, sub: 'Vật lí 12 · Chương 3: Từ trường' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const big = (w, h = 10) => `<span class="fill" style="min-width:${w}mm;height:${h}mm"></span>`;
const V = (s) => nw(m(`${s}\\ \\mathrm V`)), kV = (s) => nw(m(`${s}\\ \\mathrm{kV}`)), W = (s) => nw(m(`${s}\\ \\mathrm W`)), kW = (s) => nw(m(`${s}\\ \\mathrm{kW}`));
const Hz = (s) => nw(m(`${s}\\ \\mathrm{Hz}`)), Om = (s) => nw(m(`${s}\\ \\Omega`)), A = (s) => nw(m(`${s}\\ \\mathrm A`));
const vp = (s) => nw(`${s} vòng/phút`), vs = (s) => nw(`${s} vòng/s`);
const N1 = m('N_1'), N2 = m('N_2'), U1 = m('U_1'), U2 = m('U_2'), I1 = m('I_1'), I2 = m('I_2'), dP = m('\\Delta P'), om = m('\\omega'), E0 = m('E_0');
const can2 = nw(`(${m('E=E_0/\\sqrt2')})`);
const doiN = nw(`(1 vòng/s = 60 vòng/phút)`);

// Bài tương tự 1 cột, ô đáp số cuối dòng của ý (cùng cách l11-bai16).
const ttCss = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';

const p1 = `${ttCss}<section class="page">
${head('BÀI 14 · MÁY PHÁT ĐIỆN XOAY CHIỀU · MÁY BIẾN ÁP', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Nêu nguyên tắc tạo dòng xoay chiều, cấu tạo máy phát và tính tần số ${m('f')}`)}
${dong(`${ck}Nắm cấu tạo, công thức <b>máy biến áp</b>; phân biệt tăng áp với hạ áp`)}
${dong(`${ck}Giải thích vì sao đường dây truyền tải đi xa dùng điện áp rất cao`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Ổ cắm nhà em ghi 220 V – 50 Hz, nhưng trên đường từ nhà máy về, điện được đẩy lên ${kV('500')}. Đẩy lên ${kV('500')} để làm gì?</p>
<div class="fig-side" style="${fs(46)}"><div>
${opt('A', 'Sinh thêm điện năng vì điện áp cao')}
${opt('B', 'Giảm điện năng toả nhiệt trên dây dẫn')}
${opt('C', 'Giữ cho dòng trên dây không đổi chiều')}
${opt('D', 'Tăng tần số để động cơ quay nhanh hơn')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 1)}</div>
${H.duongDay()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Nguyên tắc tạo dòng điện xoay chiều', '1·4')}
<div class="card fig-side" style="${fs(44)};padding:1.2mm 3mm"><div>
<div>Ba từ khoá: quay khung → ${f(24)} biến thiên → sinh ${f(28)}</div>
<div>Pháp tuyến hợp với ${m('\\vec B')} góc ${nw(m('\\alpha=\\omega t+\\varphi'))} nên ${m('\\Phi=')} ${f(22)} biến thiên tuần hoàn.</div>
<div style="margin:1mm 0;display:flex;align-items:flex-end;gap:2mm;flex-wrap:wrap">${m('e=')} ${big(30, 6)} &nbsp; với ${m('E_0=')} ${big(22, 6)}</div>
<div>${E0}: suất điện động ${f(18)} (V) · ${om}: ${f(22)} (rad/s)</div>
<div>Khung quay một vòng thì ${m('e')} lặp lại ${f(22)}.</div>
<div style="margin-top:.6mm"><b>Câu 1.</b> Suất điện động trong khung quay do đại lượng nào quyết định: độ lớn từ thông hay tốc độ biến thiên từ thông? Vì sao?</div>${lines(2)}</div>
${H.khungQuay()}</div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('MÁY PHÁT MỘT PHA · TẦN SỐ f = np')}
${h3(1, 'II.2 · Máy phát điện xoay chiều một pha', '2·1')}
<div class="card fig-side" style="${fs(42)};padding:1.2mm 3mm"><div>
<div><b>Phần cảm:</b> ${f(22)} — tạo ra ${f(24)}</div>
<div><b>Phần ứng:</b> ${f(22)} — sinh ${f(30)}</div>
<div>Bộ phận đứng yên: ${f(16)} · bộ phận quay: ${f(16)}</div>
<div>Phần ứng quay thì dòng ra mạch ngoài nhờ ${f(20)} và ${f(20)}.</div>
<div style="margin:1.2mm 0;display:flex;align-items:flex-end;gap:3mm;flex-wrap:wrap">${m('f=')} ${big(16, 6)} <span>(${m('n')}: vòng/s)</span> &nbsp; ${m('f=')} ${big(20, 10)} <span>(${m('n')}: vòng/phút)</span></div>
<div>${m('p')} là số ${f(20)}, không phải số cực. Hình bên: ${nw(`${m('p=')} ${f(10)}`)}</div></div>
${H.roTo4()}</div>
${h3(2, 'Thí nghiệm: máy phát mini quay ở nhiều tốc độ', '2·2')}
<div class="card" style="padding:1.2mm 3mm">
<div><b>Làm:</b> quay máy phát mini ở 5 tốc độ, tần số kế đo ${m('f')}. Tính ${m('f/n')} (lấy 2 chữ số sau dấu phẩy).</div>
<table class="tbl-ct" style="margin:.8mm 0"><tr><th>${m('n')} (vòng/s)</th><th>5</th><th>10</th><th>15</th><th>20</th><th>25</th></tr>
<tr><td>${m('f')} đo (Hz)</td><td>9,8</td><td>20,1</td><td>30,2</td><td>39,6</td><td>50,3</td></tr>
<tr><td>${m('f/n')}</td><td>1,96</td><td></td><td></td><td></td><td></td></tr></table>
<div><b>Rút ra:</b> ${m('f/n')} luôn xấp xỉ ${f(10)}, đúng bằng ${f(30)} của máy.</div>
<div><b>Sai số:</b> ${m('f/n')} lệch cả hai phía nên là sai số ${f(20)}; giảm bằng cách ${f(48)}</div>
</div>
${h3(3, 'Làm nhanh', '2·3')}
${box(cau(`<b>Câu 2.</b> Rô-to 2 cặp cực quay ${vp('1500')}. Tần số dòng điện là bao nhiêu? ${doiN}`, 2)
 + cau(`<b>Câu 3.</b> Máy phát tua-bin nước quay ${vp('125')} phải phát ${Hz('50')}. Rô-to cần khoảng bao nhiêu cặp cực?`, 2))}
${h3(4, 'Điền bước còn thiếu: rô-to 8 cặp cực quay 375 vòng/phút', '2·4')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div class="ln"><b>Bước 1 (cho sẵn):</b> ${m('n=375/60=6{,}25')} vòng/s</div>
${wl(`Bước 2: ${m('f=np=')}`, 1)}${wl('Bước 3: máy đã phát đúng tần số lưới điện 50 Hz chưa?', 1)}</div>
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('MÁY PHÁT BA PHA · MÁY BIẾN ÁP')}
${h3(1, 'II.3 · Máy phát điện xoay chiều ba pha', '3·1')}
<div class="card fig-side" style="${fs(38)};padding:1.2mm 3mm"><div>
<div>Stato: ba cuộn dây giống nhau đặt lệch nhau ${f(14)}; rô-to quay đều.</div>
<div>Ba suất điện động: cùng ${f(18)}, cùng ${f(18)}, lệch pha ${f(14)}.</div>
<div><b>Thí nghiệm:</b> nối mỗi cuộn với một đèn LED, quay nam châm chậm. Ba đèn sáng ${f(40)}</div>
<div>Hệ ba pha: máy phát, đường dây, ${f(26)}; lợi: tiết kiệm ${f(12)}, tạo ${f(26)}.</div>
<div>Mắc hình sao: ${nw(m('U_d=\\sqrt3\\,U_p'))}. Với ${nw(m('U_p=220\\ \\mathrm V'))}: ${nw(`${m('U_d\\approx')} ${f(12)}`)}</div></div>
${H.baPha()}</div>
${h3(2, 'II.4 · Máy biến áp', '3·2')}
<div class="card fig-side" style="${fs(44)};padding:1.2mm 3mm"><div>
<div>Hai cuộn dây ${nw(m('N_1\\ne N_2'))} quấn trên một ${f(20)} bằng lá thép silic.</div>
<div>Sơ cấp ${N1} nối ${f(24)}; thứ cấp ${N2} nối ${f(12)}.</div>
<div style="margin:1mm 0;display:flex;align-items:flex-end;gap:2mm">Máy lí tưởng: ${m('\\dfrac{U_1}{U_2}=')} ${big(14)} ${m('=')} ${big(14)}</div>
<div>${nw(`${m('k=N_1/N_2')}:`)} ${nw(`${m('k>1')} máy ${f(14)}`)} · ${nw(`${m('k<1')} máy ${f(14)}`)}</div>
<div>Lõi ghép lá mỏng sơn cách điện để giảm dòng ${f(16)}. Nối nguồn một chiều không đổi: thứ cấp ${f(30)}, vì ${f(40)}</div></div>
${H.bienAp()}</div>
${h3(3, 'Thí nghiệm: quấn thêm vòng ở cuộn thứ cấp', '3·3')}
<div class="card" style="padding:1.2mm 3mm">
<div>${nw(m('N_1=200'))} vòng, ${nw(m('U_1=12{,}0\\ \\mathrm V'))}, đo khi chưa nối tải. Tính ô trống (3 chữ số).</div>
<table class="tbl-ct" style="margin:.8mm 0"><tr><th>${N2} (vòng)</th><th>100</th><th>200</th><th>400</th><th>600</th></tr>
<tr><td>${m('N_1/N_2')}</td><td>2,00</td><td>1,00</td><td>0,500</td><td></td></tr>
<tr><td>${U2} đo (V)</td><td>5,9</td><td>11,6</td><td>23,5</td><td>35,1</td></tr>
<tr><td>${m('U_1/U_2')}</td><td>2,03</td><td>1,03</td><td>0,511</td><td></td></tr></table>
<div><b>Câu 4.</b> Phát biểu nào <b>sai</b>? Khoanh và sửa lại cho đúng.</div>
<div>A. Gấp đôi số vòng thứ cấp thì vôn kế chỉ gần gấp đôi.</div>
<div>B. Kết quả ủng hộ giả thuyết điện áp tỉ lệ số vòng.</div>
<div>C. Cuộn nhiều vòng có điện áp lớn vì từ thông qua mỗi vòng của nó lớn hơn.</div>
<div>D. Không đo dòng nên chưa kiểm được tỉ số dòng điện.</div>${lines(1)}
</div>
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('TRUYỀN TẢI ĐIỆN · BA CÁI BẪY · TRẢ BÀI')}
${h3(1, 'II.5 · Truyền tải điện năng đi xa', '4·1')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div>Phát công suất ${m('P')} ở điện áp ${m('U')} nơi phát: dòng trên dây ${nw(`${m('I=')} ${f(12)}`)}</div>
<div style="margin:.6mm 0;display:flex;align-items:flex-end;gap:2mm">Hao phí toả nhiệt: ${m('\\Delta P=')} ${big(12, 6)} ${m('=')} ${big(16)}</div>
<div>Tăng ${m('U')} lên ${m('k')} lần thì ${dP} ${f(12)} ${f(12)} lần.</div>
<div>Hiệu suất truyền tải: ${nw(`${m('H=')} ${f(20)}`)}</div></div>
${H.truyenTai()}</div>
<table class="tbl-ct" style="margin-bottom:1mm"><tr><th>Tổ máy ${kW('20')}, dây ${Om('2')}: ${m('U')} (V)</th><th>250</th><th>500</th><th>1 000</th><th>5 000</th></tr>
<tr><td>${dP} (W)</td><td>12 800</td><td>3 200</td><td></td><td></td></tr></table>
${h3(2, 'III · Ba cái bẫy hay sập', '4·2')}
<div class="card fig-side" style="${fs(38)};padding:1mm 3mm"><div>
<div class="trap">${ck}<span><b>“Máy biến áp sinh thêm điện năng.”</b> Lí tưởng: ${nw(m('P_1=P_2'))}; điện áp tăng bao nhiêu lần thì cường độ giảm bấy nhiêu lần. Tần số giữ nguyên.</span></div>
<div class="trap">${ck}<span><b>“${m('f=n')}, khỏi để ý số cặp cực.”</b> Đúng là ${m('f=np')}: cùng ${vs('25')}, rô-to 1 cặp cực cho ${Hz('25')}, 2 cặp cực cho ${Hz('50')}.</span></div>
<div class="trap">${ck}<span><b>“Phần cảm là cuộn dây.”</b> Gọi theo nhiệm vụ: phần cảm tạo từ trường (nam châm), phần ứng sinh suất điện động (cuộn dây); cái nào quay cũng được.</span></div></div>
${H.capCuc()}</div>
${h3(3, 'IV · Trả bài 6 câu', '4·3')}
${box(`${tb('1. Nguyên tắc tạo dòng xoay chiều? Biểu thức suất điện động.')}${lines(1)}
${tb('2. Máy phát một pha gồm bộ phận nào? Vành khuyên để làm gì?')}${lines(1)}
${tb(`3. ${m('f=np')}: ${m('n')}, ${m('p')} là gì? Rô-to 6 cặp cực quay ${vp('600')}: ${m('f=')}?`)}${lines(1)}
${tb('4. Ba suất điện động của máy phát ba pha có đặc điểm gì?')}${lines(1)}
${tb('5. Máy biến áp: cấu tạo, công thức; khi nào là máy tăng áp?')}${lines(1)}
${tb(`6. Công thức hao phí; vì sao tăng ${m('U')} thì hao phí giảm ${m('k^2')} lần?`)}${lines(1)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/6 câu · chưa thuộc: ${f(25)} ${nw(`→ đọc lại ô ${f(12)} Tập`)}</div>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TOÁN MẪU · BÀI TẬP VỀ NHÀ · THỬ THÁCH')}
${h3(1, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '5·1')}
${rkHai([1, 2, 3], [4, 5, 6])}
${h3(2, 'V · Bài toán mẫu: tổ máy 20 kW và đường dây 2 Ω', '5·2')}
<div class="card soft" style="padding:1.2mm 3mm">Tổ máy phát một pha có rô-to hai cặp cực, quay ${vp('1500')}, phát ra ${V('500')}, công suất ${kW('20')}.<br><b>a)</b> Tính tần số dòng điện.<br><b>b)</b> Nối máy phát vào cuộn sơ cấp (500 vòng) của máy biến áp lí tưởng; đường dây nối cuộn thứ cấp (5000 vòng). Tăng áp hay hạ áp? Tính ${U2}.<br><b>c)</b> Đường dây có điện trở tổng ${Om('2')}. Tính hao phí khi chưa dùng và khi đã dùng máy biến áp.</div>
<div class="fig-side" style="${fs(46)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl(`a) ${m('n=')} … vòng/s ⇒ ${m('f=')}`, 1)}${wl(`b) ${m('k=')} … ⇒ máy … · ${m('U_2=')}`, 2)}${wl(`c) Chưa dùng: ${m('I=')} … ⇒ ${m('\\Delta P=')}`, 2)}${wl(`Đã dùng: ${m('I=')} … ⇒ ${m('\\Delta P=')}`, 2)}</div>${H.mau()}</div>
${K.btvn().replace('<i>1</i>', '<i>3</i>')}
${h3(4, 'Thử thách phân tầng', '5·4')}
${box(cau(`${m('\\bigstar')} ${nw(m('N_1=1000'))} vòng, ${nw(m('N_2=200'))} vòng, ${nw(m('U_1=220\\ \\mathrm V'))}. Tăng áp hay hạ áp? Tính ${U2}.`, 1)
 + cau(`${m('\\bigstar\\bigstar')} Vì sao máy biến áp không dùng được với dòng một chiều không đổi?`, 1)
 + cau(`${m('\\bigstar\\bigstar\\bigstar')} ${nw(m('R=5\\ \\Omega'))}, ${nw(m('P=100\\ \\mathrm{kW}'))}, ${nw(m('U=5\\ \\mathrm{kV}'))}. Tính hiệu suất; muốn ${nw(m('H\\ge99\\%'))} thì ${m('U')} ít nhất bao nhiêu?`, 2))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Tần số dòng điện của máy phát: f = np',
    de: `Rô-to máy phát một pha là nam châm có 4 cặp cực, quay đều ${vp('750')}.<br><b>a)</b> tần số ${m('f')} của dòng điện<br><b>b)</b> tần số góc ${om} của suất điện động<br><b>c)</b> máy khác quay ${vp('300')}, muốn phát ${Hz('50')}: số cặp cực`,
    nd: `Đổi ${m('n')} ra ${f(14)} trước; ${nw(`${m('f=')} ${f(10)}`)}; ${nw(`${m('\\omega=')} ${f(12)}`)}`, a: ['a', 'b', 'c'], gi: 3 },
  { t: 'Dạng 2 · Trung bình · Suất điện động của khung quay',
    de: `Khung 400 vòng, mỗi vòng ${nw(m('50\\ \\mathrm{cm^2}'))}, quay ${vp('1200')}, trục vuông góc với từ trường đều ${nw(m('0{,}030\\ \\mathrm T'))}.<br><b>a)</b> tần số góc ${om}<br><b>b)</b> suất điện động cực đại ${E0}<br><b>c)</b> suất điện động hiệu dụng ${m('E')} ${can2}`,
    nd: `Đổi ${m('S')} ra ${f(10)}, ${m('n')} ra vòng/s; ${nw(`${m('E_0=')} ${f(18)}`)}`, a: ['a', 'b', 'c'], gi: 3 },
  { t: 'Dạng 3 · Trung bình · Máy biến áp lí tưởng: U, I, P hai cuộn',
    de: `Máy biến áp lí tưởng ${nw(m('N_1=1100'))}, ${nw(m('N_2=60'))} vòng; ${nw(m('U_1=220\\ \\mathrm V'))}; thứ cấp nối đèn, ${nw(m('I_2=2{,}5\\ \\mathrm A'))}.<br><b>a)</b> tăng áp hay hạ áp; ${U2}<br><b>b)</b> cường độ ${I1} ở cuộn sơ cấp<br><b>c)</b> công suất mạch sơ cấp lấy từ mạng điện`,
    nd: `${m('U')} tỉ lệ ${f(12)} với số vòng, ${m('I')} tỉ lệ ${f(12)}; ${nw(`${m('P_1=')} ${f(12)}`)}`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'], gi: 4 },
  { t: 'Dạng 4 · Khá · Hao phí và hiệu suất truyền tải điện năng',
    de: `Nhà máy truyền ${nw(m('P=1{,}2\\ \\mathrm{MW}'))} trên đường dây điện trở tổng ${Om('5')}; điện áp hiệu dụng nơi phát ${kV('20')}, coi ${nw(m('\\cos\\varphi=1'))}.<br><b>a)</b> cường độ hiệu dụng ${m('I')} trên dây<br><b>b)</b> công suất hao phí ${dP}; hiệu suất ${m('H')}<br><b>c)</b> giữ ${m('P')}, ${m('R')}, tăng điện áp nơi phát lên ${kV('60')}: hao phí khi đó`,
    nd: `Đổi MW, kV ra W, V; ${nw(`${m('I=')} ${f(10)}`)}; ${nw(`${m('\\Delta P=')} ${f(12)}`)}; ${m('U')} tăng ${m('k')} lần thì ${dP} giảm ${f(10)} lần`, a: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], gi: 5, fig: H.truyenTai('Dây R toả nhiệt; U là điện áp nơi phát.') },
  { t: 'Dạng 5 · Khó · Máy tăng áp trước đường dây: điện áp tối thiểu',
    de: `Máy phát ${nw(m('P=400\\ \\mathrm{kW}'))}, điện áp hai cực ${nw(m('U_1=2\\ \\mathrm{kV}'))}, qua máy biến áp lí tưởng ${nw(m('N_1=1000'))}, ${nw(m('N_2=5000'))} vòng rồi lên đường dây ${Om('10')}; coi ${nw(m('\\cos\\varphi=1'))}, điện áp đầu dây là điện áp thứ cấp.<br><b>a)</b> điện áp hiệu dụng ở đầu đường dây<br><b>b)</b> cường độ trên dây; công suất hao phí<br><b>c)</b> muốn ${nw(m('H\\ge99\\%'))} (cùng ${m('P, R, U_1, N_1')}): điện áp đầu dây tối thiểu; ${N2} tối thiểu`,
    nd: `${nw(`${m('H\\ge99\\%\\Rightarrow\\Delta P\\le')} ${f(16)}`)}; ${nw(`${m('U^2\\ge')} ${big(18, 9)}`)}; ${nw(`${m('N_2=N_1\\cdot')} ${f(14)}`)}`, a: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c<sub>1</sub>', 'c<sub>2</sub>'], gi: 6, cot: 3, fig: H.soDoD5() },
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
    { t: 'Dạng 1 · Bài 1', de: `Rô-to máy phát một pha có 6 cặp cực, quay đều ${vp('500')} ${doiN}.<br><b>a)</b> tần số ${m('f')} của dòng điện<br><b>b)</b> tần số góc ${om}<br><b>c)</b> máy tua-bin khí quay ${vp('3000')}, muốn phát ${Hz('50')}: số cặp cực`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 1 · Bài 2', de: `Rô-to máy phát thuỷ điện có 24 cặp cực, phát dòng ${Hz('50')}.<br><b>a)</b> tốc độ quay của rô-to (vòng/phút)<br><b>b)</b> rô-to quay nhanh lên ${vp('150')}: tần số khi đó<br><b>c)</b> tần số góc ở câu b`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 2 · Bài 1', de: `Khung ${nw(m('N=200'))} vòng, mỗi vòng ${nw(m('S=100\\ \\mathrm{cm^2}'))}, quay đều ${vp('3000')} quanh trục vuông góc với ${m('\\vec B')}, ${nw(m('B=0{,}050\\ \\mathrm T'))} ${can2}.<br><b>a)</b> tần số góc ${om}<br><b>b)</b> suất điện động cực đại ${E0}<br><b>c)</b> suất điện động hiệu dụng ${m('E')}<br><b>d)</b> quấn gấp đôi số vòng, giữ các đại lượng khác: ${E0}`, o: ['a', 'b', 'c', 'd'], ow: 20 },
    { t: 'Dạng 2 · Bài 2', de: `Khung ${nw(m('N=500'))} vòng, mỗi vòng ${nw(m('S=200\\ \\mathrm{cm^2}'))}, quay đều trong từ trường ${nw(m('B=0{,}10\\ \\mathrm T'))}, trục vuông góc với ${m('\\vec B')} ${can2}.<br><b>a)</b> muốn ${nw(m('E_0=100\\pi\\ \\mathrm V\\approx314\\ \\mathrm V'))}: tần số góc ${om}<br><b>b)</b> tốc độ quay của khung (vòng/phút)<br><b>c)</b> suất điện động hiệu dụng ${m('E')}`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 3 · Bài 1', de: `Máy biến áp lí tưởng ${nw(m('N_1=500'))} vòng, ${nw(m('N_2=2000'))} vòng; ${nw(m('U_1=110\\ \\mathrm V'))}; thứ cấp có ${nw(m('I_2=0{,}50\\ \\mathrm A'))}.<br><b>a)</b> tăng áp hay hạ áp; ${U2}<br><b>b)</b> cường độ ${I1}<br><b>c)</b> công suất sơ cấp`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'], ow: 20 },
    { t: 'Dạng 3 · Bài 2', de: `Bộ sạc có máy biến áp lí tưởng hạ ${V('220')} xuống ${V('11')}, cuộn sơ cấp ${nw(m('N_1=2200'))} vòng.<br><b>a)</b> số vòng ${N2}<br><b>b)</b> thứ cấp cấp ${A('2{,}0')}: cường độ ${I1}<br><b>c)</b> công suất sơ cấp`, o: ['a', 'b', 'c'] },
  ], [
    { t: 'Dạng 4 · Bài 1', de: `Truyền ${nw(m('P=500\\ \\mathrm{kW}'))} trên đường dây ${Om('8')}, điện áp nơi phát ${kV('10')}, ${nw(m('\\cos\\varphi=1'))}.<br><b>a)</b> cường độ ${m('I')} trên dây<br><b>b)</b> hao phí ${dP}; hiệu suất ${m('H')}<br><b>c)</b> tăng điện áp nơi phát lên ${kV('40')}: hao phí`, o: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], ow: 22 },
    { t: 'Dạng 4 · Bài 2', de: `Truyền ${nw(m('P=2{,}0\\ \\mathrm{MW}'))} trên đường dây ${Om('10')}, điện áp nơi phát ${kV('50')}, ${nw(m('\\cos\\varphi=1'))}.<br><b>a)</b> cường độ ${m('I')} trên dây<br><b>b)</b> hao phí ${dP}; hiệu suất ${m('H')}<br><b>c)</b> muốn hao phí giảm 16 lần: điện áp nơi phát`, o: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], ow: 22 },
    { t: 'Dạng 5 · Bài 1', de: `Máy phát ${nw(m('P=200\\ \\mathrm{kW}'))}, ${nw(m('U_1=1{,}0\\ \\mathrm{kV}'))}, qua máy biến áp lí tưởng ${nw(m('N_1=500'))}, ${nw(m('N_2=5000'))} vòng rồi lên đường dây ${Om('20')}, ${nw(m('\\cos\\varphi=1'))}.<br><b>a)</b> điện áp đầu đường dây<br><b>b)</b> cường độ trên dây; hao phí<br><b>c)</b> muốn ${nw(m('H\\ge99\\%'))}: điện áp đầu dây tối thiểu; ${N2} tối thiểu`, o: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c<sub>1</sub>', 'c<sub>2</sub>'], ow: 18 },
    { t: 'Dạng 5 · Bài 2', de: `Máy phát ${nw(m('P=100\\ \\mathrm{kW}'))}, ${nw(m('U_1=500\\ \\mathrm V'))}, qua máy tăng áp lí tưởng có ${nw(m('N_1=200'))} vòng rồi lên đường dây ${Om('5')}, ${nw(m('\\cos\\varphi=1'))}.<br><b>a)</b> muốn ${nw(m('H\\ge98\\%'))}: điện áp đầu dây tối thiểu<br><b>b)</b> ${N2} tối thiểu<br><b>c)</b> dùng ${nw(m('N_2=4000'))} vòng: hao phí; hiệu suất`, fig: H.soDoD5('Tìm điện áp đầu dây trước, rồi N<sub>2</sub>.'), fw: 44, o: ['a', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'], ow: 18 },
    nhap(9),
  ]],
  dap: [
    `D1·1: a) 50 Hz · b) ${m('100\\pi\\approx314')} rad/s · c) 1 cặp cực &nbsp;|&nbsp; D1·2: a) 125 vòng/phút · b) 60 Hz · c) ${m('120\\pi\\approx377')} rad/s &nbsp;|&nbsp; D2·1: a) ${m('100\\pi\\approx314')} rad/s · b) 31,4 V · c) 22,2 V · d) 62,8 V &nbsp;|&nbsp; D2·2: a) ${m('100\\pi\\approx314')} rad/s · b) 3000 vòng/phút · c) 222 V &nbsp;|&nbsp; D3·1: a<sub>1</sub>) tăng áp · a<sub>2</sub>) 440 V · b) 2,0 A · c) 220 W &nbsp;|&nbsp; D3·2: a) 110 vòng · b) 0,10 A · c) 22 W`,
    `D4·1: a) 50 A · b<sub>1</sub>) 20 kW · b<sub>2</sub>) 96 % · c) 1,25 kW &nbsp;|&nbsp; D4·2: a) 40 A · b<sub>1</sub>) 16 kW · b<sub>2</sub>) 99,2 % · c) 200 kV &nbsp;|&nbsp; D5·1: a) 10 kV · b<sub>1</sub>) 20 A · b<sub>2</sub>) 8,0 kW · c<sub>1</sub>) 20 kV · c<sub>2</sub>) 10 000 vòng &nbsp;|&nbsp; D5·2: a) 5,0 kV · b) 2000 vòng · c<sub>1</sub>) 500 W · c<sub>2</sub>) 99,5 %`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 2], kq: [[1, 2, 3], [4, 5]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'nguyên tắc 1·4 · máy phát 2·1 · f = np 2·2 · ba pha 3·1 · máy biến áp 3·2 · quấn cuộn 3·3 · truyền tải 4·1 · bẫy 4·2 · bài mẫu 5·2 · D1–3 6·1 · D4–5 7·1',
  out: resolve(HERE, 'out/ruot-tap-vl12-c3-bai14.pdf'),
});
