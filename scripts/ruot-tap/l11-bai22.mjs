// Ruột tập VL11 – Bài 22 · Cường độ dòng điện (lesson id 41). Quyển Chương 4 lớp 11: bài 22 = tr. 1–12.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l11-bai22.mjs (toàn bộ SVG tự vẽ). Nội dung theo bài web (book/cache/41.json, tải từ DB 12/11/2026): mục tiêu,
// dự đoán tốc độ trôi, II.1–II.4, thí nghiệm ampe kế ba vị trí + đồng hồ USB, ví dụ tính v trong dây 1,5 mm², ba bẫy, Trả bài 6 câu,
// bài toán mẫu cáp kích bình, thử thách ⭐–⭐⭐⭐, 5 dạng bài tập mẫu. Đáp số Bài tương tự (tuongTu.dap) tính bằng Python 12/11/2026.
// Chạy: node scripts/ruot-tap/l11-bai22.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl11-bai22.pdf
//       node scripts/ruot-tap/l11-bai22.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l11-bai22/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL11b22 as H } from './hinh-l11-bai22.mjs';

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
  const out = resolve(HERE, 'out/hinh-l11-bai22'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 22, lid: 41, ten: 'CƯỜNG ĐỘ DÒNG ĐIỆN', lop: 11, baiDau: 22, sub: 'Vật lí 11 · Chương 4: Dòng điện. Mạch điện' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const u = (s) => nw(m(s));   // số + đơn vị KaTeX không gãy dòng
const eC = u('e=1{,}6\\cdot10^{-19}\\ \\mathrm C');
const nCu = u('n=8{,}5\\cdot10^{28}\\ \\mathrm{m^{-3}}');
const mAh = u('1\\ \\mathrm{mAh}=3{,}6\\ \\mathrm C');
const I = m('I'), dq = m('\\Delta q'), dt = m('\\Delta t');
const cao = (w, h = 10) => `<span class="fill" style="min-width:${w}mm;height:${h}mm"></span>`;

// Bài tương tự 1 cột, ô đáp số cuối dòng của ý (cùng cách l11-bai16).
const ttCss = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';

const p1 = `${ttCss}<section class="page">
${head('BÀI 22 · CƯỜNG ĐỘ DÒNG ĐIỆN', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Nêu định nghĩa, đơn vị của <b>cường độ dòng điện</b> và cách đo nó`)}
${dong(`${ck}Phân biệt chiều dòng điện với chiều electron; dòng <b>không đổi</b> với dòng <b>một chiều</b>`)}
${dong(`${ck}Nối cường độ dòng điện với số hạt tải và <b>tốc độ trôi</b> của chúng trong dây`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Bật công tắc, đèn sáng gần như tức thì dù dây tới đèn dài 5 m. Mỗi electron trong dây đồng trôi dọc dây (dịch chuyển có hướng) nhanh cỡ nào?</p>
<div class="fig-side" style="${fs(44)}"><div>
${opt('A', `Gần bằng tốc độ ánh sáng, ${u('3\\cdot10^8\\ \\mathrm{m/s}')}`)}
${opt('B', 'Cỡ vài km/s, như âm thanh trong kim loại')}
${opt('C', 'Dưới 1 mm/s, chậm hơn kiến bò')}
${opt('D', 'Đứng yên, chỉ có điện trường chạy trong dây')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 1)}</div>
${H.congTac()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Cường độ dòng điện là gì?', '1·4')}
<div class="card" style="padding:1.2mm 3mm">
<div>Dòng điện: dòng chuyển dời ${f(20)} của các ${f(22)}. Trong kim loại, hạt tải là ${f(25)}</div>
<div>Cường độ dòng điện ${I} đặc trưng cho tác dụng ${f(25)} của dòng điện.</div>
<div style="margin:1mm 0;min-height:12mm;display:flex;align-items:flex-end;gap:2mm;flex-wrap:wrap">${m('I=')} ${cao(24, 11)} <span>${dq}: điện lượng qua ${f(30)} của dây trong thời gian ${dt}</span></div>
<div>Đơn vị: ${dq} (C), ${dt} (s), ${I} (A, ampe) · ${nw(`${m('1\\ \\mathrm A=1')} ${f(12)}`)}</div>
<div style="margin-top:.6mm"><b>Ví dụ:</b> kim ampe kế bộ sạc ắc quy chỉ ${u('9\\ \\mathrm A')}. Mỗi giây có bao nhiêu cu-lông và bao nhiêu electron qua tiết diện dây? (${eC})</div>${lines(2)}
<div>Lúc kim chỉ ${u('4\\ \\mathrm A')}, “9” nhiều hơn “4” ở chỗ: ${f(70)}</div></div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('ĐO CƯỜNG ĐỘ DÒNG ĐIỆN · ĐIỆN LƯỢNG SẠC VÀO ĐIỆN THOẠI')}
${h3(1, 'Ampe kế: đặt ở đâu trong mạch?', '2·1')}
<div class="card fig-side" style="${fs(44)};padding:1.2mm 3mm"><div>
<div>Đo ${I} bằng ${f(22)}, mắc ${f(20)} với đoạn mạch cần đo: dòng phải chạy ${f(25)} ampe kế.</div>
<div><b>Thí nghiệm · Làm:</b> mắc pin 3 V, bóng đèn nhỏ và ampe kế số (thang 1 A) thành mạch kín. Đặt ampe kế lần lượt trước đèn, sau đèn, sát cực âm pin. Rồi đảo hai cực pin.</div>
<div><b>Quan sát:</b> ba vị trí đều đọc ${f(16)} A; đảo pin, đồng hồ hiện ${f(16)} A.</div>
<div><b>Rút ra:</b> trong mạch nối tiếp ${I} ${f(30)} tại mọi tiết diện. Dấu “−” chỉ báo ${f(32)}, độ lớn không đổi.</div></div>
${H.mach('Mạch pin – đèn – ampe kế.')}</div>
${h3(2, 'Làm nhanh', '2·2')}
${box(cau(`Cục sạc nhanh ghi ${u('5\\ \\mathrm V')}, ${u('3\\ \\mathrm A')}. Trong 2 phút sạc, điện lượng qua dây sạc là bao nhiêu? Số ${u('5\\ \\mathrm V')} có dùng không?`, 2))}
${h3(3, 'II.2 · Thí nghiệm đo: đồng hồ USB và điện thoại', '2·3')}
<div class="card" style="padding:1.2mm 3mm">
<div><b>Làm:</b> cắm đồng hồ đo USB (hiện ${I} và điện lượng theo mAh) giữa cục sạc và điện thoại cạn pin. Sạc chậm, dòng giữ ổn định ${u('I=1{,}50\\ \\mathrm A')}. Cứ 10 phút ghi số mAh, 5 lần.</div>
<div>Đổi đơn vị: ${m('1\\ \\mathrm{mAh}=10^{-3}\\ \\mathrm A\\cdot')} ${f(14)} ${m('\\mathrm s=')} ${f(16)} C</div></div>
<div class="fig-side" style="${fs(48)}"><div>
<table class="tbl-ct"><tr><th>${dt} (phút)</th><th>Đồng hồ (mAh)</th><th>${m('\\Delta q=I\\Delta t')} (C)</th></tr>
<tr><td>10</td><td>250</td><td>900</td></tr><tr><td>20</td><td>500</td><td></td></tr><tr><td>30</td><td>750</td><td></td></tr><tr><td>40</td><td>1000</td><td></td></tr><tr><td>50</td><td>1250</td><td></td></tr></table>
<div style="margin-top:.8mm"><b>Rút ra:</b> dòng không đổi thì ${dq} tỉ lệ ${f(20)} với ${dt}; độ dốc đồ thị là ${f(14)}.</div>
<div style="margin-top:.6mm">Dòng dao động ${u('\\pm0{,}02\\ \\mathrm A')}: ở hàng 10 phút, ${dq} lệch ${nw(`${m('\\pm')} ${f(14)} C`)}</div>${lines(2)}</div>
${H.khungDoThi()}</div>
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('CHIỀU DÒNG ĐIỆN · HẠT TẢI ĐIỆN')}
${h3(1, 'II.3 · Chiều dòng điện. Dòng không đổi, dòng một chiều', '3·1')}
<div class="card" style="padding:1.2mm 3mm">
<div>Chiều dòng điện quy ước: chiều chuyển động của hạt mang điện ${f(18)}. Trong mạch: từ cực ${f(8)} của nguồn qua mạch ngoài về cực ${f(8)}.</div>
<div>Trong kim loại, ion dương chỉ dao động quanh nút mạng; electron trôi ${f(20)} chiều dòng điện (ngược chiều điện trường).</div></div>
<div class="fig-side" style="${fs(46)}"><div>
<table><tr><th style="width:21mm"></th><th>Dòng không đổi</th><th>Dòng một chiều</th></tr>
<tr><td>Chiều</td><td style="height:6.5mm"></td><td></td></tr>
<tr><td>Cường độ</td><td style="height:6.5mm"></td><td></td></tr>
<tr><td>Đồ thị</td><td style="height:6.5mm"></td><td></td></tr></table>
<div style="margin-top:.6mm">Dòng không đổi ${ck}luôn ${ck}không luôn là dòng một chiều. Dòng một chiều ${ck}luôn ${ck}không luôn là dòng không đổi.</div></div>
${H.haiDong()}</div>
${h3(2, 'II.4 · Cường độ dòng điện và hạt tải điện', '3·2')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div>Dây tiết diện ${m('S')}, mật độ hạt tải ${m('n')} (hạt/m³), mỗi hạt mang điện ${m('e')}, trôi với tốc độ ${m('v')}. Trong ${dt} mỗi hạt đi được ${m('v\\Delta t')}.</div>
<div>Số hạt trong trụ: ${nw(`${m('N=')} ${f(28)}`)} · điện lượng qua ${m('S')}: ${nw(`${m('\\Delta q=')} ${f(26)}`)}</div>
<div style="margin:1mm 0;min-height:11mm;display:flex;align-items:flex-end;gap:2mm">Chia cho ${dt}: ${m('I=')} ${cao(26, 9)}</div>
<div>Mật độ dòng điện ${nw(`${m('j=\\dfrac{I}{S}=')} ${f(14)}`)}, đơn vị ${f(14)}</div>
<div>Đồng: ${nCu} (do vật liệu, cho sẵn). Tăng ${I} trong cùng một dây là tăng ${f(10)}, không phải tăng ${f(10)}.</div></div>
${H.hinhTru()}</div>
${h3(3, 'Ví dụ tính: electron trôi nhanh cỡ nào?', '3·3')}
<div class="card" style="padding:1.2mm 3mm">
<div>Dây đồng dân dụng ${u('S=1{,}5\\ \\mathrm{mm^2}=')} ${f(22)} ${m('\\mathrm{m^2}')}; ${nCu}; ${eC}.</div>
<div>${nw(`${m('Sne=')} ${f(22)} C/m`)} · ${nw(`${m('v=\\dfrac{I}{Sne}')}`)}</div>
<table class="tbl-ct" style="margin-top:.6mm"><tr><th>${I} (A)</th><th>1</th><th>5</th><th>10</th><th>16</th></tr>
<tr><td>${m('v')} (mm/s)</td><td>0,049</td><td></td><td></td><td></td></tr></table>
<div style="margin-top:.6mm"><b>Rút ra:</b> ngay ở 16 A, electron trôi chưa tới ${f(16)}. Đèn sáng ngay vì ${f(70)}</div>${lines(1)}</div>
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('BA CÁI BẪY · TRẢ BÀI · TỰ KIỂM TRA')}
${h3(1, 'III · Ba cái bẫy hay sập', '4·1')}
<div class="card fig-side" style="${fs(44)};padding:1mm 3mm"><div>
<div class="trap">${ck}<span><b>“Dòng mạnh là electron chạy như ánh sáng.”</b> Tốc độ trôi của từng electron chỉ cỡ mm/s; gần ${u('3\\cdot10^8\\ \\mathrm{m/s}')} là tốc độ điện trường lan dọc dây. Dòng 1 A lên 2 A trong cùng dây: ${m('n')} giữ nguyên, ${m('v')} gấp đôi.</span></div>
<div class="trap">${ck}<span><b>“Một chiều thì là không đổi.”</b> Dòng sau chỉnh lưu đi một chiều nhưng cường độ nhấp nhô nên không phải dòng không đổi. Xoay chiều là chiều đổi qua lại.</span></div>
<div class="trap">${ck}<span><b>“Mắc ampe kế song song, để nguyên đơn vị.”</b> Ampe kế mắc nối tiếp, không nối thẳng vào hai cực pin. ${u('300\\ \\mathrm{mC}')} trong 2 phút: ${u('I=0{,}300/120=2{,}5\\ \\mathrm{mA}')}, không phải ${u('150\\ \\mathrm{mA}')}.</span></div></div>
${H.ampeSai()}</div>
${h3(2, 'IV · Trả bài 6 câu', '4·2')}
${box(`${tb('1. Cường độ dòng điện đặc trưng cho gì? Công thức, đơn vị?')}${lines(2)}
${tb('2. Đo cường độ dòng điện bằng gì, mắc thế nào?')}${lines(1)}
${tb('3. Chiều dòng điện quy ước? Electron đi chiều nào?')}${lines(1)}
${tb('4. Dòng không đổi khác dòng một chiều ở chỗ nào?')}${lines(2)}
${tb(`5. Viết ${m('I=Snve')}, nêu nghĩa và đơn vị từng kí hiệu.`)}${lines(2)}
${tb('6. Mật độ dòng điện là gì? Vì sao electron chậm mà đèn sáng ngay?')}${lines(2)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/6 câu · chưa thuộc: ${f(25)} ${nw(`→ đọc lại ô ${f(12)} Tập`)}</div>
${h3(3, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '4·3')}
${rkHai([1, 2, 3, 4], [5, 6, 7, 8])}
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TOÁN MẪU · BÀI TẬP VỀ NHÀ · THỬ THÁCH')}
${h3(1, 'V · Bài toán mẫu: cáp kích bình ô tô', '5·1')}
<div class="card soft fig-side" style="${fs(42)};padding:1.2mm 3mm"><div>Bộ kích bình cấp dòng không đổi ${u('I=120\\ \\mathrm A')} qua cáp đồng tiết diện ${u('S=25\\ \\mathrm{mm^2}')}; ${nCu}; ${eC}.
<div><b>a)</b> Điện lượng qua tiết diện cáp trong 1 phút.</div><div><b>b)</b> Số electron qua tiết diện đó.</div><div><b>c)</b> Tốc độ trôi của electron.</div><div><b>d)</b> Mật độ dòng điện trong cáp.</div></div>${H.capKich()}</div>
<table><tr><th style="width:46mm">Câu trong đề</th><th>Dữ liệu → kiến thức</th></tr>
<tr><td>“dòng không đổi 120 A”</td><td>${I} không đổi → dùng được ${m('\\Delta q=I\\Delta t')}</td></tr>
<tr><td style="height:6mm">“tiết diện 25 mm²”</td><td></td></tr>
<tr><td style="height:6mm">“trong 1 phút”</td><td></td></tr>
<tr><td style="height:6mm">“tốc độ trôi”</td><td></td></tr></table>
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm;margin-top:1mm">
${wl(`a) ${m('\\Delta q=')}`, 1)}${wl(`b) ${m('N=')}`, 1)}${wl(`c) ${m('Sne=')} …… ${m('\\Rightarrow v=')}`, 2)}${wl(`d) ${m('j=')}`, 1)}</div>
${h3(2, 'Điền bước còn thiếu: cùng cáp, giảm dòng còn 60 A', '5·2')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div class="ln"><b>Bước 1 (cho sẵn):</b> ${m('Sne=3{,}4\\cdot10^{5}\\ \\mathrm{C/m}')} (như trên, không đổi)</div>
${wl(`Bước 2: ${m('\\Delta q')} trong 1 phút ${m('=')}`, 1)}${wl(`Bước 3: ${m('v=')}`, 1)}</div>
${K.btvn().replace('<i>1</i>', '<i>3</i>')}
${h3(4, 'Thử thách phân tầng', '5·4')}
${box(wl(`${m('\\bigstar')} Đèn pin chạy dòng ${u('0{,}25\\ \\mathrm A')} trong 10 phút. Điện lượng qua đèn?`, 1)
 + wl(`${m('\\bigstar\\bigstar')} Pin dự phòng ${u('10\\,000\\ \\mathrm{mAh}')} phóng dòng không đổi ${u('2{,}0\\ \\mathrm A')} được bao lâu? ${nw(`(${mAh})`)}`, 2)
 + wl(`${m('\\bigstar\\bigstar\\bigstar')} Cáp kích bài mẫu dài ${u('2{,}0\\ \\mathrm m')}. Electron đi hết cáp mất bao lâu? Vì sao bật bộ kích là có dòng ngay?`, 2))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Ampe kế, chiều electron, loại dòng',
    de: 'Nạp ắc quy xe máy qua dây đồng: kim ampe kế dao động từ 2 A đến 6 A, luôn ở một phía vạch 0.<br><b>a)</b> ampe kế mắc thế nào với ắc quy<br><b>b)</b> electron trong dây trôi theo chiều nào so với chiều dòng điện quy ước<br><b>c)</b> dòng nạp là dòng không đổi, dòng một chiều hay cả hai',
    nd: `Không đổi: chiều và ${f(20)} đều không đổi; một chiều: chỉ ${f(16)} không đổi`, a: ['a', 'b', 'c'], gi: 4, fig: H.sacD1() },
  { t: 'Dạng 2 · Dễ · Điện lượng, số electron, thời gian',
    de: `Quạt mini USB đang chạy; ampe kế mắc nối tiếp chỉ ${u('0{,}40\\ \\mathrm A')}, không đổi; ${eC}.<br><b>a)</b> điện lượng qua tiết diện dây trong ${u('50\\ \\mathrm s')}<br><b>b)</b> số electron qua tiết diện trong thời gian đó<br><b>c)</b> thời gian để có ${u('32\\ \\mathrm C')} qua tiết diện`,
    nd: `Nối ba đại lượng: ${nw(`${m('\\Delta q=')} ${f(14)}`)} và ${nw(`${m('\\Delta q=')} ${f(14)}`)}`, a: ['a', 'b', 'c'], gi: 3 },
  { t: 'Dạng 3 · Trung bình · Đổi mA, phút, mAh',
    de: `Sạc đồng hồ (đầu ra ${u('5\\ \\mathrm V')}): dòng không đổi ${u('150\\ \\mathrm{mA}')} trong 36 phút; pin ${u('300\\ \\mathrm{mAh}')}; ${mAh}.<br><b>a)</b> điện lượng qua dây sạc, theo C<br><b>b)</b> đổi điện lượng đó ra mAh<br><b>c)</b> pin được nạp thêm bao nhiêu phần trăm dung lượng`,
    nd: `Đổi ${f(12)} ra A, ${f(12)} ra s trước khi nhân; số ${u('5\\ \\mathrm V')} ${f(16)}`, a: ['a', 'b', 'c'], gi: 3 },
  { t: 'Dạng 4 · Trung bình · Tốc độ trôi khi đổi tiết diện',
    de: `Dây nối bình nước nóng có lõi đồng tiết diện ${u('2{,}5\\ \\mathrm{mm^2}')}, mang dòng không đổi ${u('10\\ \\mathrm A')}; ${nCu}; ${eC}.<br><b>a)</b> tốc độ trôi của electron trong lõi, theo mm/s<br><b>b)</b> nối tiếp thêm đoạn lõi đồng ${u('1{,}0\\ \\mathrm{mm^2}')}, dòng vẫn ${u('10\\ \\mathrm A')}: tốc độ trôi trong đoạn này, theo mm/s`,
    nd: `${nw(`${m('v=')} ${f(22)}`)}; đổi ${u('1\\ \\mathrm{mm^2}=')} ${f(14)} ${m('\\mathrm{m^2}')}; nối tiếp thì ${f(10)} như nhau, ${m('v')} tỉ lệ ${f(14)} với ${m('S')}`, a: ['a', 'b'], gi: 7, fig: H.dayD4() },
  { t: 'Dạng 5 · Khó · Cường độ, số electron, tốc độ trôi, mật độ dòng',
    de: `Dây đồng cấp điện cho bếp từ có tiết diện ${u('6{,}0\\ \\mathrm{mm^2}')}. Dòng không đổi: trong 1,5 phút có ${u('2700\\ \\mathrm C')} qua tiết diện thẳng của dây; ${nCu}; ${eC}.<br><b>a)</b> cường độ dòng điện<br><b>b)</b> số electron qua tiết diện trong thời gian đó<br><b>c)</b> tốc độ trôi của electron, theo mm/s<br><b>d)</b> mật độ dòng điện, theo A/mm²`,
    nd: `Phút → s, mm² → m²; ${nw(`${m('j=\\dfrac{I}{S}=')} ${f(12)}`)} (kiểm lại hai cách)`, a: ['a', 'b', 'c', 'd'], cot: 2, gi: 6, fig: H.dayD5() },
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
const nAl = u('n=1{,}8\\cdot10^{29}\\ \\mathrm{m^{-3}}');
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–3', 'DẠNG 4–5'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: 'Đèn LED xe đạp chạy bằng đinamô qua bộ chỉnh lưu. Ampe kế trong mạch chỉ nhấp nhô từ 0 đến 0,3 A, kim không bao giờ lùi về phía âm.<br><b>a)</b> ampe kế mắc thế nào với đèn<br><b>b)</b> electron trong dây trôi theo chiều nào so với chiều dòng điện quy ước<br><b>c)</b> dòng qua đèn là dòng không đổi, dòng một chiều hay cả hai', o: ['a', 'b', 'c'], ow: 30 },
    { t: 'Dạng 1 · Bài 2', de: `Pin ${u('1{,}5\\ \\mathrm V')} nuôi đồng hồ treo tường; ampe kế số mắc đúng cách chỉ ${u('0{,}20\\ \\mathrm{mA}')}, giữ nguyên nhiều giờ.<br><b>a)</b> dòng này là dòng không đổi, dòng một chiều hay cả hai<br><b>b)</b> ở mạch ngoài, electron đi từ cực nào của pin về cực nào<br><b>c)</b> đảo hai cực pin (ampe kế để nguyên): ampe kế chỉ bao nhiêu`, o: ['a', 'b', 'c'], ow: 30 },
    { t: 'Dạng 2 · Bài 1', de: `Bóng đèn pin có dòng không đổi ${u('0{,}32\\ \\mathrm A')}; ${eC}.<br><b>a)</b> điện lượng qua tiết diện dây trong ${u('25\\ \\mathrm s')}<br><b>b)</b> số electron qua tiết diện trong thời gian đó<br><b>c)</b> thời gian để có ${u('48\\ \\mathrm C')} qua tiết diện`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 2 · Bài 2', de: `Dòng không đổi: trong ${u('20\\ \\mathrm s')} có ${u('2{,}5\\cdot10^{19}')} electron qua tiết diện thẳng của dây; ${eC}.<br><b>a)</b> điện lượng qua tiết diện trong 20 s<br><b>b)</b> cường độ dòng điện<br><b>c)</b> thời gian để ${u('1{,}0\\cdot10^{20}')} electron qua tiết diện`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 3 · Bài 1', de: `Tai nghe bluetooth sạc bằng dòng không đổi ${u('250\\ \\mathrm{mA}')} trong 48 phút; pin tai nghe ${u('400\\ \\mathrm{mAh}')}; ${mAh}.<br><b>a)</b> điện lượng qua dây sạc, theo cu-lông<br><b>b)</b> đổi điện lượng đó ra mAh<br><b>c)</b> pin được nạp thêm bao nhiêu phần trăm dung lượng`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 3 · Bài 2', de: `Pin dự phòng ${u('5000\\ \\mathrm{mAh}')} đang đầy, sạc cho điện thoại bằng dòng không đổi ${u('1{,}2\\ \\mathrm A')} trong 90 phút; ${mAh}.<br><b>a)</b> điện lượng pin dự phòng đã cấp, theo cu-lông<br><b>b)</b> đổi điện lượng đó ra mAh<br><b>c)</b> pin dự phòng còn bao nhiêu phần trăm dung lượng`, o: ['a', 'b', 'c'] },
  ], [
    { t: 'Dạng 4 · Bài 1', de: `Dây lõi đồng tiết diện ${u('1{,}5\\ \\mathrm{mm^2}')} mang dòng không đổi ${u('6{,}0\\ \\mathrm A')}; ${nCu}; ${eC}.<br><b>a)</b> tốc độ trôi của electron trong lõi, theo mm/s<br><b>b)</b> nối tiếp đoạn lõi đồng ${u('0{,}75\\ \\mathrm{mm^2}')}: tốc độ trôi trong đoạn này, theo mm/s<br><b>c)</b> tốc độ trôi ở đoạn nhỏ gấp mấy lần ở đoạn lớn`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 4 · Bài 2', de: `Dây nhôm tiết diện ${u('4{,}0\\ \\mathrm{mm^2}')} (nhôm: ${nAl}) nối tiếp dây đồng ${u('2{,}5\\ \\mathrm{mm^2}')} (đồng: ${nCu}), dòng không đổi ${u('20\\ \\mathrm A')}; ${eC}.<br><b>a)</b> tốc độ trôi trong dây nhôm, theo mm/s<br><b>b)</b> tốc độ trôi trong dây đồng, theo mm/s<br><b>c)</b> dây nào electron trôi nhanh hơn, gấp mấy lần`, o: ['a', 'b', 'c'], ow: { c: 30 } },
    { t: 'Dạng 5 · Bài 1', de: `Dây đồng tiết diện ${u('4{,}0\\ \\mathrm{mm^2}')}; dòng không đổi: trong 2,0 phút có ${u('4800\\ \\mathrm C')} qua tiết diện; ${nCu}; ${eC}.<br><b>a)</b> cường độ dòng điện<br><b>b)</b> số electron qua tiết diện trong thời gian đó<br><b>c)</b> tốc độ trôi của electron, theo mm/s<br><b>d)</b> mật độ dòng điện, theo A/mm²`, o: ['a', 'b', 'c', 'd'] },
    { t: 'Dạng 5 · Bài 2', de: `Trong dây đồng tiết diện ${u('2{,}5\\ \\mathrm{mm^2}')}, electron trôi với tốc độ ${u('0{,}40\\ \\mathrm{mm/s}')}; ${nCu}; ${eC}.<br><b>a)</b> cường độ dòng điện<br><b>b)</b> mật độ dòng điện, theo A/mm²<br><b>c)</b> điện lượng qua tiết diện trong 5,0 phút<br><b>d)</b> số electron qua tiết diện trong thời gian đó`, o: ['a', 'b', 'c', 'd'] },
    nhap(6),
  ]],
  dap: [
    `D1·1: a) nối tiếp · b) ngược chiều · c) một chiều, không phải dòng không đổi &nbsp;|&nbsp; D1·2: a) cả hai · b) từ cực − về cực + · c) −0,20 mA (độ lớn vẫn 0,20 mA) &nbsp;|&nbsp; D2·1: a) 8,0 C · b) 5,0·10<sup>19</sup> · c) 150 s &nbsp;|&nbsp; D2·2: a) 4,0 C · b) 0,20 A · c) 80 s &nbsp;|&nbsp; D3·1: a) 720 C · b) 200 mAh · c) 50 % &nbsp;|&nbsp; D3·2: a) 6480 C · b) 1800 mAh · c) 64 %`,
    `D4·1: a) 0,29 mm/s · b) 0,59 mm/s · c) 2 lần &nbsp;|&nbsp; D4·2: a) 0,17 mm/s · b) 0,59 mm/s · c) dây đồng, gấp 3,4 lần &nbsp;|&nbsp; D5·1: a) 40 A · b) 3,0·10<sup>22</sup> · c) 0,74 mm/s · d) 10 A/mm² &nbsp;|&nbsp; D5·2: a) 13,6 A · b) 5,4 A/mm² · c) 4080 C · d) 2,55·10<sup>22</sup>`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 2], kq: [[1, 2, 3], [4, 5]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'định nghĩa I 1·4 · ampe kế 2·1 · đồng hồ USB, mAh 2·3 · chiều dòng, không đổi/một chiều 3·1 · I = Snve 3·2 · tốc độ trôi 3·3 · bẫy 4·1 · bài toán mẫu 5·1 · dạng 1–3 → 6·1 · dạng 4–5 → 7·1',
  out: process.argv[2],
});
