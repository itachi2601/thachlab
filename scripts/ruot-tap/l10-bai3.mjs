// Ruột tập VL10 – Bài 3 · Thực hành tính sai số trong phép đo. Ghi kết quả đo (lesson id 48). Quyển Chương 1 lớp 10: bài 3 = tr. 25–36.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Nội dung theo bài web (book/cache/48.json, tải 13/11/2026): mục tiêu, dự đoán cục tẩy, SI + tiếp đầu ngữ, thứ nguyên, hệ thống/ngẫu nhiên,
// thí nghiệm con lắc 5 lần đo, tỉ đối, gián tiếp, CSCN, ba bẫy, bài toán mẫu g, 3 dạng bài tập mẫu. Bài có BTM → dùng bố cục l10-bai23 (tr.6–7 Dạng, tr.8–9 Bài tương tự).
// Đáp số mọi bài (BTM, tương tự) tính bằng Python 13/11/2026. Không dùng ảnh Halliday (SVG tự vẽ trong hinh-l10-bai3.mjs).
// Chạy: node scripts/ruot-tap/l10-bai3.mjs [file.pdf]   → scripts/ruot-tap/out/ruot-tap-vl10-bai3.pdf
//       node scripts/ruot-tap/l10-bai3.mjs --hinh       → chụp từng hình ở cỡ in vào out/hinh-l10-bai3/
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai, yn } from './khung.mjs';
import { hinhL10b3 as H } from './hinh-l10-bai3.mjs';

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
  const out = resolve(HERE, 'out/hinh-l10-bai3'); mkdirSync(out, { recursive: true });
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

const OFF = (3 - 1) * 12;
const K = khoiTao({ bai: 3, lid: 48, lop: 10, baiDau: 1, ten: 'THỰC HÀNH TÍNH SAI SỐ · GHI KẾT QUẢ ĐO', sub: 'Vật lí 10 · Chương 1: Mở đầu' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const A = m('A'), dA = m('\\Delta A'), Ab = m('\\overline{A}'), dl = m('\\delta A');
const ttCss = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';

// ---------- Trang 1: mục tiêu · dự đoán · đơn vị SI · tiếp đầu ngữ ----------
const kyHieu = ['Chiều dài', 'Khối lượng', 'Thời gian', 'Nhiệt độ', 'Cường độ dòng điện', 'Lượng chất', 'Cường độ ánh sáng'];
const p1 = `${ttCss}<section class="page">
${head('BÀI 3 · TÍNH SAI SỐ · GHI KẾT QUẢ ĐO', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Đổi đơn vị theo hệ <b>SI</b>, kiểm công thức bằng <b>thứ nguyên</b>`)}
${dong(`${ck}Phân biệt sai số <b>hệ thống</b> và <b>ngẫu nhiên</b>`)}
${dong(`${ck}Tính sai số <b>tuyệt đối</b>, <b>tỉ đối</b> của phép đo trực tiếp và gián tiếp`)}
${dong(`${ck}Ghi ${m('A=\\overline{A}\\pm\\Delta A')} đúng <b>chữ số có nghĩa</b>`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Hai bạn cùng đo một cục tẩy: A dùng thước kẻ vạch 1 mm đọc “12 mm”; B dùng thước điện tử đọc “12,05 mm”. Hai con số khác nhau. Điều nào hợp lí nhất?</p>
<div class="fig-side" style="${fs(46)}"><div>
${opt('A', 'Một bạn chắc chắn đọc sai, vì kích thước thật chỉ có một con số')}
${opt('B', 'Cả hai có thể đúng: dụng cụ chia nhỏ hơn thì sát giá trị thật hơn')}
${opt('C', 'Bạn A ghi thành 12,00 mm là chính xác ngang bạn B')}
${opt('D', 'Thước kẻ bị hỏng vì không đọc được phần lẻ')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 1)}</div>
${H.haiThuoc()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Bảy đơn vị cơ bản của hệ SI', '1·4')}
<table><tr><th>Đại lượng</th><th style="width:34mm">Đơn vị</th><th style="width:22mm">Kí hiệu</th></tr>
${kyHieu.map((x) => `<tr><td style="height:6mm">${x}</td><td></td><td></td></tr>`).join('')}</table>
${foot(1)}</section>`;

// ---------- Trang 2: thứ nguyên · loại sai số · sai số dụng cụ ----------
const p2 = `<section class="page">
${head('TIẾP ĐẦU NGỮ · THỨ NGUYÊN · PHÉP ĐO · HAI LOẠI SAI SỐ')}
${h3(1, 'Tiếp đầu ngữ và đổi đơn vị', '2·1')}
<table style="text-align:center"><tr><th style="text-align:center">giga (G)</th><th style="text-align:center">mega (M)</th><th style="text-align:center">kilo (k)</th><th style="text-align:center">mili (m)</th><th style="text-align:center">micro (${m('\\mu')})</th><th style="text-align:center">nano (n)</th></tr>
<tr><td>${m('10^{9}')}</td><td>${m('10^{6}')}</td><td>${m('10^{3}')}</td><td>${m('10^{-3}')}</td><td>${m('10^{-6}')}</td><td>${m('10^{-9}')}</td></tr></table>
<div style="margin-top:1mm">${nw(`${m('12\\ \\mathrm{mm}=12\\cdot 10^{-3}\\ \\mathrm m')}`)} · ${nw(`${m('36\\ \\mathrm{km/h}=')} ${f(22)} ${m('\\mathrm{m/s}')}`)} · ${nw(`${m('250\\ \\mathrm{mg}=')} ${f(22)} ${m('\\mathrm{kg}')}`)}</div>
${h3(2, 'II.2 · Thứ nguyên: kiểm công thức', '2·2')}
<div class="card" style="padding:1.2mm 3mm">
<div>Thứ nguyên ${m('[X]')} cho biết đơn vị của ${m('X')} dựng từ đơn vị cơ bản thế nào. Kí hiệu: ${m('\\mathrm L')} chiều dài · ${m('\\mathrm M')} khối lượng · ${m('\\mathrm T')} thời gian.</div>
<div class="hint" style="margin:.4mm 0">Cho sẵn: ${nw(`${m('[v]=\\mathrm{L\\,T^{-1}}')}`)} · ${nw(`${m('[a]=\\mathrm{L\\,T^{-2}}')}`)} · hệ số như ${m('\\tfrac12')}, ${m('2')} không có thứ nguyên.</div>
<div>Hai vế của công thức phải ${f(22)} thứ nguyên; các số hạng cộng, trừ nhau cũng phải ${f(22)} thứ nguyên.</div></div>
<table><tr><th style="width:44mm">Công thức</th><th>[vế trái]</th><th>[vế phải]</th><th style="width:30mm">Cùng thứ nguyên?</th></tr>
<tr><td style="height:9mm">${m('v=a\\,t^{2}')}</td><td></td><td></td>${yn}</tr>
<tr><td style="height:9mm">${m('s=\\tfrac12\\,a\\,t^{2}')}</td><td></td><td></td>${yn}</tr>
<tr><td style="height:9mm">${m('v^{2}=v_0^{2}+a\\,s')}</td><td></td><td></td>${yn}</tr></table>
<div style="margin-top:1mm">Công thức thứ ba cùng thứ nguyên mà vẫn sai (còn thiếu một hệ số): hệ số cần thêm là ${f(14)}. Kiểm thứ nguyên chỉ bắt được lỗi ${f(25)}, không bắt được thiếu ${f(25)}.</div>
${h3(3, 'II.3 · Phép đo và hai loại sai số', '2·3')}
<div class="fig-side" style="${fs(44)}"><div>
<div>Đo ${f(25)}: đọc ngay trên dụng cụ (cân khối lượng, bình chia độ). Đo ${f(25)}: qua công thức với các đại lượng đo trực tiếp (tốc độ, khối lượng riêng).</div>
<div class="hint" style="margin:.4mm 0">ĐCNN: độ chia nhỏ nhất của dụng cụ. Sai số dụng cụ ${nw(m('\\Delta A_{\\mathrm{dc}}'))}: dụng cụ có vạch chia lấy ${f(14)} ĐCNN; dụng cụ hiện số lấy ${f(14)} ĐCNN.</div>
<div>Mép cục tẩy nằm đúng vạch 12: ${nw(`${m('A=(12{,}0\\pm')} ${f(10)}${m(')\\ \\mathrm{mm}')}`)}, vì ĐCNN của thước là ${f(10)} mm.</div></div>
${H.thuocDoc()}</div>
<table style="margin-top:1mm"><tr><th style="width:34mm"></th><th>Sai số hệ thống</th><th>Sai số ngẫu nhiên</th></tr>
<tr><td style="height:9mm">Lệch thế nào?</td><td></td><td></td></tr>
<tr><td style="height:9mm">Do đâu?</td><td></td><td></td></tr>
<tr><td style="height:9mm">Đo nhiều lần có giảm?</td><td></td><td></td></tr></table>
<div style="margin-top:1mm">Thước mòn đầu luôn đo thiếu: ${f(25)}. &nbsp;Bấm đồng hồ lúc sớm lúc muộn: ${f(25)}.</div>
${foot(2)}</section>`;

// ---------- Trang 3: sai số tuyệt đối trực tiếp (thí nghiệm con lắc) · tỉ đối ----------
const tdo = [20.19, 19.85, 20.14, 19.94, 20.23];
const p3 = `<section class="page">
${head('ĐO NHIỀU LẦN · SAI SỐ TUYỆT ĐỐI · SAI SỐ TỈ ĐỐI')}
${h3(1, 'II.4 · Sai số tuyệt đối của phép đo trực tiếp', '3·1')}
<div class="card" style="padding:1.2mm 3mm">
<div>${m('\\overline{A}=\\dfrac{A_1+A_2+\\dots+A_n}{n}')} · ${m('\\Delta A_i=|\\overline{A}-A_i|')} · ${m('\\Delta A=\\overline{\\Delta A}+\\Delta A_{\\mathrm{dc}}')}</div>
<div>Chỉ đo 1 lần thì ${nw(`${m('\\Delta A=')} ${f(14)}`)}. Ở đây ${m('\\overline{\\Delta A}')} là trung bình của các ${m('\\Delta A_i')}.</div></div>
${h3(2, 'Thí nghiệm: 10 dao động của con lắc đơn, đo 5 lần', '3·2')}
<div class="fig-side" style="${fs(46)}"><div>
<div><b>Làm:</b> con lắc dài ${nw('1,000 m')}, lệch ${nw(m('5^\\circ'))} rồi thả; đồng hồ số (ĐCNN ${nw('0,01 s')}) bấm thời gian ${m('t')} của 10 dao động, 5 lần.</div>
<div><b>Quan sát:</b> 5 số không trùng nhau (bảng). Tổng 5 lần ${m('t_i')}: ${f(18)} s.</div></div>
${H.diemDo()}</div>
<table class="tbl-ct" style="text-align:center;margin-top:1mm"><tr><th style="width:18mm;text-align:center">Lần</th>${tdo.map((_, i) => `<th style="text-align:center">${i + 1}</th>`).join('')}</tr>
<tr><td style="height:7mm"><b>${m('t_i')} (s)</b></td>${tdo.map((v) => `<td>${String(v.toFixed(2)).replace('.', ',')}</td>`).join('')}</tr>
<tr><td style="height:8.5mm"><b>${m('\\Delta t_i')} (s)</b></td>${tdo.map(() => '<td></td>').join('')}</tr></table>
<div class="card soft" style="margin-top:1mm;padding:1.2mm 3mm">
<div>${nw(`${m('\\overline{t}=')} ${f(16)} s`)} · ${nw(`${m('\\overline{\\Delta t}=')} ${f(16)} s`)} · ${nw(`${m('\\Delta t_{\\mathrm{dc}}=')} ${f(12)} s`)}</div>
<div>${nw(`${m('\\Delta t=')} ${f(16)} s`)} · ghi kết quả: ${nw(`${m('t=(')} ${f(16)} ± ${f(12)}${m(')\\ \\mathrm s')}`)}</div></div>
${h3(3, 'II.5 · Sai số tỉ đối: mức độ chính xác', '3·3')}
<div class="card" style="padding:1.2mm 3mm">
<div>${m('\\delta A=\\dfrac{\\Delta A}{\\overline{A}}\\cdot 100\\,\\%')}. Cùng ${dA}, đại lượng đo càng ${f(14)} thì ${dl} càng lớn.</div>
<div style="margin-top:.6mm">Con lắc: ${nw(`${m('\\delta t=')} ${f(16)} %`)}. Nghĩa là cứ ${nw('100 s')} đo thì sai chừng ${f(12)} s.</div>
<div style="margin-top:.6mm">Đo ${nw('2 s')} mà sai ${nw('0,15 s')}: ${nw(`${m('\\delta=')} ${f(14)} %`)}</div></div>
${h3(5, 'IV · Trả bài 6 câu', '3·4')}
${box(`${tb('1. Bảy đơn vị cơ bản SI; thứ nguyên và hai quy tắc kiểm công thức?')}${lines(1)}
${tb('2. Hệ thống khác ngẫu nhiên thế nào? Đo nhiều lần giảm loại nào?')}${lines(1)}
${tb('3. Sai số tuyệt đối của phép đo trực tiếp tính ra sao?')}${lines(1)}
${tb('4. Sai số tỉ đối: công thức và ý nghĩa?')}${lines(1)}
${tb('5. Sai số gián tiếp: tổng/hiệu, tích/thương, luỹ thừa?')}${lines(1)}
${tb('6. Ghi kết quả đo và đếm chữ số có nghĩa?')}${lines(1)}`)}
${foot(3)}</section>`;

// ---------- Trang 4: gián tiếp · chữ số có nghĩa · ba bẫy ----------
const p4 = `<section class="page">
${head('PHÉP ĐO GIÁN TIẾP · CHỮ SỐ CÓ NGHĨA · BA CÁI BẪY')}
${h3(1, 'II.6 · Sai số của phép đo gián tiếp', '4·1')}
<table><tr><th style="width:46mm">Phép tính</th><th>Sai số tìm được</th></tr>
<tr><td style="height:11mm">${m('F=X\\pm Y\\pm Z')} (trừ cũng vậy)</td><td>${m('\\Delta F=')} ${f(40)}</td></tr>
<tr><td style="height:11mm">${m('A=X\\,\\dfrac{Y}{Z}')}</td><td>${m('\\delta A=')} ${f(40)}</td></tr>
<tr><td style="height:11mm">${m('A=X^{n}\\dfrac{Y^{m}}{Z^{k}}')}</td><td>${m('\\delta A=')} ${f(40)}</td></tr></table>
<div style="margin-top:1mm">Hình lập phương ${m('V=a^{3}')}, đo được ${nw(`${m('\\delta a=0{,}5\\,\\%')}`)}: ${nw(`${m('\\delta V=')} ${f(16)} %`)}</div>
${h3(2, 'II.7 · Ghi kết quả và chữ số có nghĩa', '4·2')}
<div class="card" style="padding:1.2mm 3mm">
<div>${m('A=\\overline{A}\\pm\\Delta A')}. ${dA} giữ 1–2 chữ số có nghĩa: chữ số đầu là ${f(8)} hoặc ${f(8)} thì giữ ${f(8)} chữ số, còn lại giữ ${f(8)}.</div>
<div>${Ab} viết đến cùng ${f(25)} với ${dA}. &nbsp;Số 0 đứng đầu ${ck}có ${ck}không có nghĩa; số 0 cuối phần thập phân ${ck}có ${ck}không có nghĩa.</div></div>
<table style="text-align:center;margin-top:1mm"><tr><th style="text-align:center">Số</th><th style="text-align:center">${nw(m('0{,}0620'))}</th><th style="text-align:center">${m('1007')}</th><th style="text-align:center">${m('0{,}00040')}</th><th style="text-align:center">${m('2{,}50')}</th></tr>
<tr><td style="height:7mm"><b>Số CSCN</b></td><td></td><td></td><td></td><td></td></tr></table>
<div style="margin-top:1mm">Đo quãng đường nhiều lần được ${nw(m('\\overline{s}=2{,}3856\\ \\mathrm m'))}, ${nw(m('\\Delta s=0{,}013\\ \\mathrm m'))}. Ghi: ${nw(`${m('s=(')} ${f(16)} ± ${f(14)}${m(')\\ \\mathrm m')}`)}</div>
${h3(3, 'III · Ba cái bẫy hay sập', '4·3')}
<div class="fig-side" style="${fs(46)}"><div class="card" style="padding:1mm 3mm;margin:0">
<div class="trap">${ck}<span><b>“Đo nhiều lần thì sai số nào cũng nhỏ đi.”</b> Chỉ giảm sai số ${f(22)}; cân luôn chỉ thừa ${nw('0,3 g')} thì trung bình 5 lần vẫn thừa ${f(10)} g.</span></div>
<div class="trap">${ck}<span><b>“Sai số tuyệt đối nhỏ là đo chính xác.”</b> So ${f(8)}, không so ${f(8)}: tấm bìa ${nw(m('(250{,}0\\pm0{,}5)\\ \\mathrm{mm}'))} có ${nw(`${m('\\delta=')} ${f(10)} %`)}, cục tẩy ${nw(m('(12{,}0\\pm0{,}5)\\ \\mathrm{mm}'))} có ${nw(`${m('\\delta=')} ${f(10)} %`)}.</span></div>
<div class="trap">${ck}<span><b>“Ghi thêm số 0 cho đẹp.”</b> ${nw(m('1{,}5\\ \\mathrm m'))} và ${nw(m('1{,}500\\ \\mathrm m'))} khác nhau: dụng cụ đo tới ${f(10)} và tới ${f(10)}.</span></div></div>
${H.haiHang('Dãy 1 và dãy 2: năm lần đo cùng một vật; nét đứt là giá trị thật.')}</div>
${h3(4, 'Làm nhanh', '4·4')}
<div class="card" style="padding:1.2mm 3mm"><div>Cân điện tử có ĐCNN ${nw('0,1 g')} chỉ ${nw('25,3 g')}. Đo một lần: ghi ${nw(`${m('m=(')} ${f(14)} ± ${f(10)}${m(')\\ \\mathrm g')}`)}</div></div>
${foot(4)}</section>`;

// ---------- Trang 5: tự kiểm tra · bài toán mẫu · BTVN ----------
const p5 = `<section class="page">
${head('TỰ KIỂM TRA · BÀI TOÁN MẪU · BÀI TẬP VỀ NHÀ')}
${h3(1, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '5·1')}
${rkHai([1, 2, 3, 4], [5, 6, 7])}
${h3(2, 'V · Bài toán mẫu: đo g bằng con lắc đơn', '5·2')}
<div class="card soft" style="padding:1.2mm 3mm">${m('g=\\dfrac{4\\pi^{2}l}{T^{2}}')}. Dây dài ${nw(m('l=1{,}000\\ \\mathrm m'))}, thước ĐCNN ${nw('1 mm')} (sai số dụng cụ lấy một ĐCNN). Thời gian ${m('t')} của 10 dao động đo 5 lần ở bảng tr. ${3 + OFF}; ${m('T=t/10')}. Bỏ qua sai số của ${m('\\pi')}. Tính ${m('g')} và ghi kết quả.</div>
<table style="margin-top:1mm"><tr><th style="width:50mm">Câu trong đề</th><th>Dữ liệu → kiến thức</th></tr>
<tr><td>“${m('g=4\\pi^2l/T^2')}”</td><td>Gián tiếp: tích, thương, ${f(8)} ở ${m('T')}</td></tr>
<tr><td style="height:6.5mm">“ĐCNN 1 mm, một ĐCNN”</td><td></td></tr>
<tr><td style="height:6.5mm">“10 dao động, 5 lần”</td><td></td></tr>
<tr><td style="height:6.5mm">“bỏ qua sai số của ${m('\\pi')}”</td><td></td></tr></table>
${h3(3, 'Giải')}
<div class="fig-side" style="${fs(40)}"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl(`${m('T')}, ${m('\\delta T')}:`, 2)}${wl(`${m('\\overline{g}')}:`, 1)}${wl(`${m('\\delta l')}, ${m('\\delta g')}:`, 2)}${wl(`${m('\\Delta g')}, ghi kết quả:`, 2)}</div>${H.cungDoDai()}</div>
<div style="margin-top:1mm">${nw('Đổi thước đo dây thành loại kém hơn:')} ${nw(m('\\Delta l=0{,}003\\ \\mathrm m'))}: ${nw(`${m('\\delta g=')} ${f(14)} %`)}; ${nw(`${m('g=(')} ${f(14)} ± ${f(12)}${m(')\\ \\mathrm{m/s^2}')}`)}</div>
${K.btvn().replace('<i>1</i>', '<i>4</i>')}
${foot(5)}</section>`;

// ---------- Bài tập mẫu: 3 dạng ----------
const dang = [
  { t: 'Dạng 1 · Dễ · Đo trực tiếp nhiều lần: trung bình, sai số tuyệt đối, tỉ đối, ghi kết quả',
    de: `Viên bi thép cân bốn lần bằng cân điện tử ĐCNN ${nw(m('0{,}01\\ \\mathrm g'))} (sai số dụng cụ lấy một ĐCNN): ${nw(m('5{,}38'))}; ${nw(m('5{,}42'))}; ${nw(m('5{,}38'))}; ${nw(m('5{,}42'))} (g).<br><b>a)</b> giá trị trung bình ${m('\\overline{m}')}<br><b>b)</b> sai số tuyệt đối ${m('\\Delta m')}<br><b>c)</b> sai số tỉ đối ${m('\\delta m')}<br><b>d)</b> ghi kết quả đo`,
    nd: `${nw(m('\\Delta m=\\overline{\\Delta m}+\\Delta m_{\\mathrm{dc}}'))}: ${nw(`${m('\\overline{\\Delta m}=')} ${f(14)}`)}; ${nw(`${m('\\delta m=')} ${f(14)}`)}; ${m('\\Delta m')} có ${f(8)} CSCN nên ${m('\\overline{m}')} lấy ${f(8)} chữ số thập phân`, a: ['a', 'b', 'c', 'd'], gi: 4, fig: H.can(), cot: 2 },
  { t: 'Dạng 2 · Trung bình · Đo gián tiếp nhân, chia: cộng sai số tỉ đối',
    de: `Xe lăn chạy hết đường ray: ${nw(m('s=(2{,}50\\pm0{,}01)\\ \\mathrm m'))}, ${nw(m('t=(4{,}2\\pm0{,}1)\\ \\mathrm s'))}. Tốc độ trung bình ${m('v=s/t')}.<br><b>a)</b> ${m('\\delta s')} và ${m('\\delta t')}<br><b>b)</b> sai số tỉ đối ${m('\\delta v')}<br><b>c)</b> ${m('\\overline{v}')}, ${m('\\Delta v')} rồi ghi ${m('v=\\overline{v}\\pm\\Delta v')} đúng CSCN`,
    nd: `Chia cũng ${f(25)} sai số ${f(14)}: ${nw(`${m('\\delta v=')} ${f(10)} + ${f(10)}`)}; ${nw(`${m('\\Delta v=\\overline{v}\\,\\delta v')}`)}`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>', 'c<sub>3</sub>'], gi: 5, fig: H.rayXe(), cot: 3 },
  { t: 'Dạng 3 · Khó · Gián tiếp có số mũ: gộp phép đo nhiều lần và một lần, tìm nguồn sai số lớn nhất',
    de: `Vật trượt không vận tốc đầu trên mặt nghiêng dài ${nw(m('s=(1{,}20\\pm0{,}01)\\ \\mathrm m'))}. Thời gian trượt đo 5 lần bằng đồng hồ số (ĐCNN ${nw(m('0{,}01\\ \\mathrm s'))}, sai số dụng cụ lấy một ĐCNN): ${nw(m('1{,}54'))}; ${nw(m('1{,}48'))}; ${nw(m('1{,}48'))}; ${nw(m('1{,}51'))}; ${nw(m('1{,}49'))} (s). Gia tốc ${m('a=\\dfrac{2s}{t^{2}}')}.<br><b>a)</b> ${m('\\overline{t}')} và ${m('\\Delta t')}<br><b>b)</b> ${m('\\delta s')}, ${m('\\delta t')} rồi ${m('\\delta a')}<br><b>c)</b> ${m('\\overline{a}')}, ${m('\\Delta a')}; ghi ${m('a=\\overline{a}\\pm\\Delta a')}<br><b>d)</b> đại lượng nào đóng góp nhiều nhất vào ${m('\\delta a')}`,
    nd: `Số mũ nhân với ${f(14)} của chính nó: ${nw(`${m('\\delta a=\\delta s+')} ${f(8)} ${m('\\delta t')}`)}; hệ số ${m('2')} ${ck}có ${ck}không đóng góp vào sai số`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'b<sub>3</sub>', 'c<sub>1</sub>', 'c<sub>2</sub>', 'c<sub>3</sub>', 'd'], cot: 3, gi: 18, fig: H.mpn() },
];

// ---------- Bài tương tự (giải vào vở) ----------
const oY = (s, o, w = {}) => s.split('<br>').map((p) => {
  const y = p.match(/^<b>([a-d])\)<\/b>/);
  if (!y) return `<div>${p}</div>`;
  const ls = o.filter((l) => l[0] === y[1]);
  return `<div class="yo"><span>${p}</span><span class="oo">${ls.map((l) => `<span class="nw"><b>${l})</b>${f(typeof w === 'object' ? (w[l] ?? 25) : w)}</span>`).join('')}</span></div>`;
}).join('');
const ttDe = (b) => b.fig ? `<div class="fig-side" style="grid-template-columns:1fr ${b.fw}mm">${`<div>${oY(b.de, b.o, b.ow)}</div>`}${b.fig}</div>` : oY(b.de, b.o, b.ow);
const vaoVo = (ds) => ds.map((b) => (b.o ? { t: b.t, de: ttDe(b), k: 0 } : b));
const nhap = (n) => ({ t: '<span class="nhap-t">Nháp / chỗ em còn vướng</span>', de: lines(n), k: 0 });
const nm = (s) => nw(m(s));
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–3', 'DẠNG 3 · NGOÀI DẠNG'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Đường kính quả cầu thép đo bốn lần bằng thước kẹp ĐCNN ${nm('0{,}02\\ \\mathrm{mm}')} (sai số dụng cụ lấy một ĐCNN): ${nm('12{,}30')}; ${nm('12{,}34')}; ${nm('12{,}30')}; ${nm('12{,}34')} (mm).<br><b>a)</b> ${m('\\overline{d}')}<br><b>b)</b> ${m('\\Delta d')}<br><b>c)</b> ${m('\\delta d')}<br><b>d)</b> ghi kết quả ${m('d=\\overline{d}\\pm\\Delta d')}`, o: ['a', 'b', 'c', 'd'], ow: { d: 44 } },
    { t: 'Dạng 1 · Bài 2', de: `Chu kì con lắc đo bốn lần bằng đồng hồ số ĐCNN ${nm('0{,}01\\ \\mathrm s')} (sai số dụng cụ lấy một ĐCNN): ${nm('1{,}42')}; ${nm('1{,}38')}; ${nm('1{,}40')}; ${nm('1{,}40')} (s).<br><b>a)</b> ${m('\\overline{T}')}<br><b>b)</b> ${m('\\Delta T')}<br><b>c)</b> ${m('\\delta T')}<br><b>d)</b> ghi kết quả ${m('T=\\overline{T}\\pm\\Delta T')}`, o: ['a', 'b', 'c', 'd'], ow: { d: 44 } },
    { t: 'Dạng 2 · Bài 1', de: `Vật đi hết quãng đường ${nm('s=(1{,}80\\pm0{,}02)\\ \\mathrm m')} trong ${nm('t=(3{,}6\\pm0{,}1)\\ \\mathrm s')}; ${m('v=s/t')}.<br><b>a)</b> ${m('\\delta s')} và ${m('\\delta t')}<br><b>b)</b> ${m('\\delta v')}<br><b>c)</b> ${m('\\overline{v}')}, ${m('\\Delta v')}; ghi ${m('v=\\overline{v}\\pm\\Delta v')}`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>', 'c<sub>3</sub>'], ow: { 'c<sub>3</sub>': 40, 'a<sub>1</sub>': 18, 'a<sub>2</sub>': 18, 'c<sub>1</sub>': 18, 'c<sub>2</sub>': 18 } },
    { t: 'Dạng 2 · Bài 2', de: `Xe đi hết đường ray ${nm('s=(4{,}00\\pm0{,}02)\\ \\mathrm m')} trong ${nm('t=(2{,}5\\pm0{,}1)\\ \\mathrm s')}; ${m('v=s/t')}.<br><b>a)</b> ${m('\\delta s')} và ${m('\\delta t')}<br><b>b)</b> ${m('\\delta v')}<br><b>c)</b> ${m('\\overline{v}')}, ${m('\\Delta v')}; ghi ${m('v=\\overline{v}\\pm\\Delta v')}`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>', 'c<sub>3</sub>'], ow: { 'c<sub>3</sub>': 40, 'a<sub>1</sub>': 18, 'a<sub>2</sub>': 18, 'c<sub>1</sub>': 18, 'c<sub>2</sub>': 18 } },
    { t: 'Dạng 3 · Bài 1', de: `Vật trượt không vận tốc đầu trên mặt nghiêng dài ${nm('s=(1{,}50\\pm0{,}01)\\ \\mathrm m')}; ${m('t')} đo bốn lần bằng đồng hồ số ĐCNN ${nm('0{,}01\\ \\mathrm s')}: ${nm('1{,}20')}; ${nm('1{,}18')}; ${nm('1{,}22')}; ${nm('1{,}20')} (s). ${m('a=2s/t^{2}')}.<br><b>a)</b> ${m('\\overline{t}')} và ${m('\\Delta t')}<br><b>b)</b> ${m('\\delta s')}, ${m('\\delta t')}, ${m('\\delta a')}<br><b>c)</b> ${m('\\overline{a}')}, ${m('\\Delta a')}; ghi ${m('a=\\overline{a}\\pm\\Delta a')}`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'b<sub>3</sub>', 'c<sub>1</sub>', 'c<sub>2</sub>', 'c<sub>3</sub>'], ow: { 'c<sub>3</sub>': 40, 'a<sub>1</sub>': 14, 'a<sub>2</sub>': 14, 'b<sub>1</sub>': 14, 'b<sub>2</sub>': 14, 'b<sub>3</sub>': 14, 'c<sub>1</sub>': 14, 'c<sub>2</sub>': 14 } },
  ], [
    { t: 'Dạng 3 · Bài 2', de: `Khối kim loại hình lập phương, cạnh ${m('a')} đo bốn lần bằng thước kẹp ĐCNN ${nm('0{,}02\\ \\mathrm{cm}')}: ${nm('2{,}00')}; ${nm('2{,}02')}; ${nm('2{,}00')}; ${nm('1{,}98')} (cm); khối lượng ${nm('m=(21{,}6\\pm0{,}1)\\ \\mathrm g')}. ${m('\\rho=m/a^{3}')}.<br><b>a)</b> ${m('\\overline{a}')} và ${m('\\Delta a')}<br><b>b)</b> ${m('\\delta m')}, ${m('\\delta a')}, ${m('\\delta\\rho')}<br><b>c)</b> ${m('\\overline{\\rho}')}, ${m('\\Delta\\rho')}; ghi ${m('\\rho=\\overline{\\rho}\\pm\\Delta\\rho')}`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'b<sub>3</sub>', 'c<sub>1</sub>', 'c<sub>2</sub>', 'c<sub>3</sub>'], ow: { 'c<sub>3</sub>': 40, 'a<sub>1</sub>': 14, 'a<sub>2</sub>': 14, 'b<sub>1</sub>': 14, 'b<sub>2</sub>': 14, 'b<sub>3</sub>': 14, 'c<sub>1</sub>': 14, 'c<sub>2</sub>': 14 } },
    { t: 'Ngoài dạng · Đơn vị, thứ nguyên, chữ số có nghĩa', de: `Cho sẵn: ${nm('[F]=\\mathrm{M\\,L\\,T^{-2}}')}, ${nm('[v]=\\mathrm{L\\,T^{-1}}')}.<br><b>a)</b> đổi ${nm('72\\ \\mathrm{km/h}')} sang ${nm('\\mathrm{m/s}')}<br><b>b)</b> đổi ${nm('0{,}25\\ \\mathrm{mm}')} sang ${nm('\\mathrm m')} (dạng ${m('x\\cdot10^{n}')})<br><b>c)</b> kiểm ${m('F=\\dfrac{mv^{2}}{r}')}: vế phải có thứ nguyên ${nm('\\mathrm{M\\,L\\,T^{-2}}')} không<br><b>d)</b> số chữ số có nghĩa của ${nm('0{,}0620')}; ${nm('1007')}; ${nm('0{,}00040')}`, o: ['a', 'b', 'c', 'd<sub>1</sub>', 'd<sub>2</sub>', 'd<sub>3</sub>'], ow: { b: 30, 'd<sub>1</sub>': 10, 'd<sub>2</sub>': 10, 'd<sub>3</sub>': 10, c: 14 } },
    { t: 'Ngoài dạng · Loại sai số', de: `Cân điện tử chưa chỉnh về số 0 nên luôn chỉ thừa ${nm('0{,}2\\ \\mathrm g')}. Một vật cân sáu lần, lấy trung bình.<br><b>a)</b> loại sai số này<br><b>b)</b> trung bình sáu lần có hết lệch ${nm('0{,}2\\ \\mathrm g')} không<br><b>c)</b> cách khắc phục`, o: ['a', 'b', 'c'], ow: { a: 28, b: 14, c: 50 } },
    nhap(14),
  ]],
  dap: [
    `D1·1: a) 12,32 mm · b) 0,04 mm · c) 0,32 % · d) (12,32 ± 0,04) mm &nbsp;|&nbsp; D1·2: a) 1,40 s · b) 0,02 s · c) 1,43 % · d) (1,40 ± 0,02) s &nbsp;|&nbsp; D2·1: a<sub>1</sub>) 1,11 % · a<sub>2</sub>) 2,78 % · b) 3,89 % · c<sub>1</sub>) 0,500 m/s · c<sub>2</sub>) 0,019 m/s · c<sub>3</sub>) (0,500 ± 0,019) m/s &nbsp;|&nbsp; D2·2: a<sub>1</sub>) 0,5 % · a<sub>2</sub>) 4,0 % · b) 4,5 % · c<sub>1</sub>) 1,60 m/s · c<sub>2</sub>) 0,07 m/s · c<sub>3</sub>) (1,60 ± 0,07) m/s &nbsp;|&nbsp; D3·1: a<sub>1</sub>) 1,20 s · a<sub>2</sub>) 0,02 s · b<sub>1</sub>) 0,67 % · b<sub>2</sub>) 1,67 % · b<sub>3</sub>) 4,0 % · c<sub>1</sub>) 2,08 m/s² · c<sub>2</sub>) 0,08 m/s² · c<sub>3</sub>) (2,08 ± 0,08) m/s²`,
    `D3·2: a<sub>1</sub>) 2,00 cm · a<sub>2</sub>) 0,03 cm · b<sub>1</sub>) 0,46 % · b<sub>2</sub>) 1,5 % · b<sub>3</sub>) 5,0 % · c<sub>1</sub>) 2,70 g/cm³ · c<sub>2</sub>) 0,13 g/cm³ · c<sub>3</sub>) (2,70 ± 0,13) g/cm³ &nbsp;|&nbsp; Ngoài dạng 1: a) 20 m/s · b) 2,5·10<sup>−4</sup> m · c) có · d<sub>1</sub>) 3 · d<sub>2</sub>) 4 · d<sub>3</sub>) 2 &nbsp;|&nbsp; Ngoài dạng 2: a) hệ thống · b) không · c) chỉnh cân về số 0`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [2, 1], kq: [[1, 2], [3]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'đơn vị SI 1·4 · thứ nguyên 2·2 · hai loại sai số 2·3 · con lắc 3·2 · tỉ đối 3·3 · gián tiếp 4·1 · CSCN 4·2 · bẫy 4·3 · bài toán mẫu 5·2 · dạng 1–2 → 6·1 · dạng 3 → 7·1',
  out: process.argv[2],
});
