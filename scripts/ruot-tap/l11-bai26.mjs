// Ruột tập VL11 – Bài 26 · Thực hành: đo suất điện động và điện trở trong của pin điện hoá (lesson id 45). Quyển Chương 4 lớp 11: bài 26 = tr. 49–60 (baiDau 22).
// Khung: khung.mjs (bố cục bài 14: 1–5 học · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Bài THỰC HÀNH: tr.1–5 = nhắc lại · dụng cụ + sơ đồ · các bước + bẫy · bảng số liệu + sai số · đồ thị U(I) + suy ra ℰ, r + câu hỏi báo cáo.
// Nội dung theo bài web (book/cache/45.json, tải 12/11/2026). Đáp số mọi bài (BTM, tương tự) tính bằng Python 12/11/2026.
// Chạy: node scripts/ruot-tap/l11-bai26.mjs [file.pdf]   → scripts/ruot-tap/out/ruot-tap-vl11-bai26.pdf
//       node scripts/ruot-tap/l11-bai26.mjs --hinh       → chụp từng hình ở cỡ in vào out/hinh-l11-bai26/
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL11b26 as H } from './hinh-l11-bai26.mjs';

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
  const out = resolve(HERE, 'out/hinh-l11-bai26'); mkdirSync(out, { recursive: true });
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


const OFF = (26 - 22) * 12;
const K = khoiTao({ bai: 26, lid: 45, lop: 11, baiDau: 22, ten: 'THỰC HÀNH: ĐO SUẤT ĐIỆN ĐỘNG VÀ ĐIỆN TRỞ TRONG', sub: 'Vật lí 11 · Chương 4: Dòng điện. Mạch điện' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const E = m('\\mathcal{E}'), U = m('U'), I = m('I'), r = m('r'), R0 = m('R_0'), Rx = m('R_x');
const V = (s) => nw(m(`${s}\\ \\mathrm V`)), A = (s) => nw(m(`${s}\\ \\mathrm A`)), Om = (s) => nw(m(`${s}\\ \\Omega`));
const dv = nw(`${E}, ${U}: V · ${I}: A · ${r}: Ω`);

const ttCss = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';

const p1 = `${ttCss}<section class="page">
${head('BÀI 26 · THỰC HÀNH: ĐO SUẤT ĐIỆN ĐỘNG VÀ ĐIỆN TRỞ TRONG', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Lắp mạch đo, đọc đúng ampe kế và vôn kế, ghi bảng số liệu ${m('(I,U)')}`)}
${dong(`${ck}Vẽ đồ thị ${m('U')} theo ${m('I')}, từ đường thẳng đọc các đại lượng đặc trưng của pin`)}
${dong(`${ck}Ghi kết quả kèm sai số; nêu được nguyên nhân sai số`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Xe đồ chơi chạy pin AA đứng ì. Vôn kế đo hai đầu viên pin lúc chưa lắp vào xe chỉ 1,50 V; lúc động cơ đang rên ư ử chỉ còn 1,06 V. Vì sao số đo tụt đi?</p>
<div class="fig-side" style="${fs(48)}"><div>
${opt('A', 'Đồng hồ đo sai mỗi khi có dòng chạy trong mạch')}
${opt('B', 'Động cơ “hút” bớt suất điện động của viên pin')}
${opt('C', 'Có dòng thì pin sụt áp bên trong, pin cũ sụt nhiều')}
${opt('D', 'Pin hết năng lượng nên chỉ còn “điện áp ảo” ở hai cực')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 1)}</div>
${H.xeDoChoi()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, `II.1 · Nhắc lại: ${m('U=\\mathcal{E}-Ir')} là một đường thẳng`, '1·4')}
<div class="card fig-side" style="${fs(48)};padding:1.2mm 3mm"><div>
<div>Pin có suất điện động ${E}, điện trở trong ${r}. Có dòng ${I} chạy qua: ${m('U=')} ${f(30)}.</div>
<div class="hint" style="margin:.3mm 0">Đơn vị: ${dv}</div>
<div>Đồ thị ${m('U')} theo ${m('I')}: đường ${f(22)}; cắt trục ${m('U')} tại ${f(8)} ${nw(`(lúc ${m('I=')} ${f(8)})`)}; hệ số góc bằng ${f(10)}.</div>
<div style="margin-top:.6mm">Hai điểm (1), (2) trên đường: ${nw(`${m('r=')} <span class="fill" style="min-width:34mm;height:10mm"></span>`)}</div></div>
${H.duongThang()}</div>
${h3(5, 'Làm nhanh', '1·5')}
${box(cau(`Đường ${m('U')}–${m('I')} của một pin cắt trục ${m('U')} tại ${V('1{,}50')} và đi qua điểm ${nw(m('(0{,}50\\ \\mathrm A;\\ 1{,}10\\ \\mathrm V)'))}. Điện trở trong ${r} của pin là bao nhiêu?`, 1))}
${foot(1)}</section>`;

const bangDc = (rows) => `<table><tr><th style="width:36mm">Dụng cụ</th><th>Mắc thế nào · để làm gì</th></tr>${rows.map((x) => `<tr><td style="height:11mm">${x}</td><td></td></tr>`).join('')}</table>`;
const p2 = `<section class="page">
${head('DỤNG CỤ · SƠ ĐỒ MẠCH ĐO · ĐIỆN TRỞ BẢO VỆ')}
${h3(1, 'II.2 · Dụng cụ và sơ đồ mạch', '2·1')}
<div class="fig-side" style="${fs(58)}"><div>
${bangDc(['Pin cần đo: pin AA đã dùng + pin mới cùng loại', `Biến trở ${Rx}: ${nw(m('0\\text{–}100\\ \\Omega'))}`, `Điện trở ${R0} ${nw(m('=2{,}0\\ \\Omega'))}`, 'Ampe kế, thang 2 A', 'Vôn kế, thang 2 V', 'Khoá K'])}
</div>${H.soDo()}</div>
${h3(2, `Vì sao phải mắc điện trở bảo vệ ${m('R_0')}?`, '2·2')}
<div class="card" style="padding:1.2mm 3mm">
<div>Định luật Ohm toàn mạch: ${nw(m('I=\\dfrac{\\mathcal{E}}{R_{\\text{ngoài}}+r}'))}. Pin mới có ${nw(m('\\mathcal{E}=1{,}50\\ \\mathrm V'))}, ${nw(m('r=0{,}30\\ \\Omega'))} (cho sẵn).</div>
<div style="margin-top:.6mm">Bỏ ${R0}, vặn ${nw(`${Rx} = 0`)}: ${nw(`${m('I=')} ${f(22)}`)} &nbsp;· Có ${R0} ${nw(m('=2{,}0\\ \\Omega'))}, ${nw(`${Rx} = 0`)}: ${nw(`${m('I=')} ${f(22)}`)}</div>
<div style="margin-top:.6mm">Ampe kế thang ${nw(m('2\\ \\mathrm A'))}. Cách nào dòng lớn nhất còn trong thang? ${ck}bỏ ${R0} &nbsp;${ck}có ${R0}</div></div>
${h3(3, 'Ampe kế và vôn kế: mắc nhầm là hỏng', '2·3')}
<div class="fig-side" style="${fs(44)}"><div>
<table><tr><th style="width:32mm"></th><th>Ampe kế</th><th>Vôn kế</th></tr>
<tr><td style="height:9mm">Điện trở</td><td></td><td></td></tr>
<tr><td style="height:9mm">Mắc với pin</td><td></td><td></td></tr></table>
<div style="margin-top:1mm;line-height:1.35">Một bạn mắc ampe kế như hình. Em chọn: ${ck}ampe kế chỉ 0 &nbsp;${ck}ampe kế nối tắt hai cực: dòng rất lớn, pin nóng &nbsp;${ck}ampe kế vẫn đọc đúng dòng qua biến trở</div></div>
${H.ampeSongSong()}</div>
${h3(4, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '2·4')}
${rkHai([1, 2, 3, 4], [5, 6, 7, 8])}
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('CÁC BƯỚC ĐO · AN TOÀN · HAI CÁI BẪY SỐ LIỆU')}
${h3(1, 'II.3 · Các bước đo', '3·1')}
<div class="card" style="padding:1.2mm 3mm">
<div class="trap"><b>1.</b><span>Lắp mạch theo sơ đồ. Kiểm cực đồng hồ, chọn thang: vôn kế ${f(10)} V, ampe kế ${f(10)} A. Khoá K ${f(12)}.</span></div>
<div class="trap"><b>2.</b><span>Vặn ${nw(`${Rx} = 100 Ω`)}. Đóng K, đọc nhanh ${m('U')} và ${m('I')}, ghi bảng (tr. ${4 + OFF}), <b>ngắt K ngay</b>.</span></div>
<div class="trap"><b>3.</b><span>Giảm ${Rx} lần lượt: 20; 10; 5; 2; 0 Ω; mỗi lần lặp bước 2. Tổng cộng ${f(8)} lần đo.</span></div>
<div class="trap"><b>4.</b><span>Thay pin mới, giữ nguyên mạch và các giá trị ${Rx}, đo lại.</span></div>
<div class="trap"><b>5.</b><span>Vẽ đồ thị (tr. ${5 + OFF}); đọc ${E}, ${r}; ước lượng sai số; ghi kết quả.</span></div>
<div style="margin-top:.6mm"><b>An toàn:</b> không nối thẳng hai cực pin bằng dây hay ampe kế (đoản mạch: pin nóng, hỏng đồng hồ); không đóng K lâu vì ${E}, ${r} trôi.</div>
<div style="margin-top:.6mm"><b>Vì sao</b> chỉ đóng K lúc đọc số, đọc xong ngắt ngay?</div>${lines(2)}</div>
${h3(2, 'III · Bẫy 1: “vôn kế 1,5 V nên pin cấp 1,5 V”', '3·2')}
<div class="card" style="padding:1.2mm 3mm">
<table><tr><th style="width:36mm"></th><th>Mạch hở (${m('I=0')})</th><th>Có tải (${m('I>0')})</th></tr>
<tr><td style="height:8mm">Vôn kế đọc</td><td></td><td></td></tr></table>
<div style="margin-top:.8mm">Pin ${nw(m('\\mathcal{E}=1{,}50\\ \\mathrm V'))}, ${nw(m('r=0{,}8\\ \\Omega'))} nối động cơ kéo dòng ${A('0{,}50')}. Hiệu điện thế hai đầu động cơ: ${nw(`${m('U=')} ${f(22)}`)}</div></div>
${h3(3, 'III · Bẫy 2: lấy một cặp số rồi tính r = U/I', '3·3')}
<div class="card" style="padding:1.2mm 3mm">
<div>Lần đo 5 (${nw(`${Rx} = 2 Ω`)}, ${nw(m('R_0=2{,}0\\ \\Omega'))}): ${nw(m('I=0{,}311\\ \\mathrm A'))}, ${nw(m('U=1{,}25\\ \\mathrm V'))}. Bạn A tính ${nw(m('r=U/I=4{,}0\\ \\Omega'))}.</div>
<div style="margin-top:.6mm">${m('U/I')} là điện trở của ${f(22)}, bằng ${nw(`${R0} + ${Rx} = ${f(10)}`)}. Với ${nw(m('\\mathcal{E}=1{,}50\\ \\mathrm V'))}: ${nw(`${m('r=\\dfrac{\\mathcal{E}-U}{I}=')} <span class="fill" style="min-width:26mm;height:10mm"></span>`)}</div></div>
${K.btvn().replace('<i>1</i>', '<i>4</i>')}
${foot(3)}</section>`;

const nguyenNhan = ['Chuôi cắm, khoá K lỏng: số nhảy', 'Thang đo quá lớn: mất chữ số lẻ', `Đóng K lâu: pin nóng, ${E} và ${r} trôi`, 'Dây nối giữa pin và vôn kế có điện trở', 'Đọc – ghi nhầm mA với A, nhầm cột'];
const bangSo = (ten) => `<div><div style="font-weight:700;color:var(--navy);margin-bottom:.4mm">${ten}</div><table class="tbl-ct" style="text-align:center">
<tr><th style="width:9mm;padding:.7mm .8mm">Lần</th><th style="width:15mm;padding:.7mm .8mm">${Rx} (Ω)</th><th>${I} (A)</th><th>${U} (V)</th></tr>
${[100, 20, 10, 5, 2, 0].map((x, i) => `<tr><td style="height:8.5mm"><b>${i + 1}</b></td><td>${x}</td><td></td><td></td></tr>`).join('')}</table></div>`;
const p4 = `<section class="page">
${head('BẢNG SỐ LIỆU · SAI SỐ')}
${h3(1, 'II.4 · Số liệu nhóm em', '4·1')}
<div class="two">${bangSo('Pin cũ')}${bangSo('Pin mới')}</div>
<div class="hint" style="margin:.8mm 0">Sai số dụng cụ: vôn kế ${nw(m('\\pm0{,}01\\ \\mathrm V'))}; ampe kế ${nw(m('\\pm0{,}002\\ \\mathrm A'))} (theo cấp chính xác của máy, lớn hơn chữ số cuối hiện ${nw(m('0{,}001\\ \\mathrm A'))}).</div>
<div class="card soft" style="padding:1.2mm 3mm"><div><b>Quan sát:</b> ${Rx} càng nhỏ thì ${I} ${f(14)}, ${U} ${f(14)}. Pin cũ: ${U} từ ${f(10)} V xuống ${f(10)} V; pin mới: từ ${f(10)} V xuống ${f(10)} V.</div></div>
${h3(2, 'Sai số đến từ đâu, khắc phục thế nào?', '4·2')}
<div class="fig-side" style="${fs(44)}"><div>
<table><tr><th>Nguyên nhân</th><th style="width:44mm">Khắc phục</th></tr>${nguyenNhan.map((x) => `<tr><td style="height:8mm;font-size:var(--fs-sm)">${x}</td><td></td></tr>`).join('')}</table></div>
${H.kepVon()}</div>
<div class="card soft" style="margin-top:1.2mm;padding:1.2mm 3mm">Ampe kế đặt ${ck}trong ${ck}ngoài đoạn M–N (hai điểm vôn kế kẹp). Vì vậy điện trở ampe kế ${ck}có ${ck}không cộng vào ${r} đo được.</div>
${h3(3, 'Làm nhanh: chọn hai điểm để tính r', '4·3')}
<div class="card" style="padding:1.2mm 3mm">
<div>Pin cũ mẫu: lần 1 ${nw(m('(0{,}014\\ \\mathrm A;\\ 1{,}48\\ \\mathrm V)'))}, lần 2 ${nw(m('(0{,}066\\ \\mathrm A;\\ 1{,}44\\ \\mathrm V)'))}, lần 3 ${nw(m('(0{,}117\\ \\mathrm A;\\ 1{,}40\\ \\mathrm V)'))}, lần 6 ${nw(m('(0{,}534\\ \\mathrm A;\\ 1{,}06\\ \\mathrm V)'))}. Sai số của hiệu hai số ${m('U')} là ${V('0{,}02')}.</div>
<div style="margin-top:.6mm">Hiệu ${m('U')} lần 1–6: ${f(10)} V, sai số chiếm ${f(8)} % · lần 2–3: ${f(10)} V, chiếm ${f(8)} %. Dùng cặp lần ${f(8)} và lần ${f(8)} cho ${r} đáng tin hơn.</div></div>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head(`ĐỒ THỊ ${m('U(I)')} · SUY RA ${E}, ${r} · BÁO CÁO`)}
${h3(1, 'II.5 · Đồ thị U theo I của nhóm em', '5·1')}
<div style="width:116mm">${H.luoi()}</div>
${h3(2, `Suy ra ${E} và ${r} từ đường thẳng`, '5·2')}
<table style="text-align:center"><tr><th style="width:15mm"></th><th>${E} (V)</th><th>Điểm A ${m('(I;U)')}</th><th>Điểm B ${m('(I;U)')}</th><th>${r} (Ω)</th></tr>
<tr><td style="height:8.5mm"><b>Pin cũ</b></td><td></td><td></td><td></td><td></td></tr>
<tr><td style="height:8.5mm"><b>Pin mới</b></td><td></td><td></td><td></td><td></td></tr></table>
<div class="hint" style="margin:.5mm 0">A, B chọn trên <b>đường thẳng</b>, xa nhau; ${nw(m('r=\\dfrac{U_A-U_B}{I_B-I_A}'))}; ${E} đọc ở giao trục ${m('U')}.</div>
<div class="card soft" style="padding:1mm 3mm"><b>Sai số của ${r} (pin cũ):</b> ${nw(m('\\dfrac{\\Delta r}{r}=\\dfrac{\\Delta(U_A-U_B)}{U_A-U_B}+\\dfrac{\\Delta(I_B-I_A)}{I_B-I_A}'))}. Sai số của hiệu = tổng hai sai số. ${nw(`${m('\\Delta r=')} ${f(14)}`)} · ${nw(`${m('r=')}(${f(12)} ± ${f(12)}) Ω`)}</div>
${h3(3, 'Câu hỏi báo cáo', '5·3')}
${box(`<div style="padding-top:.6mm"><b>1.</b> Pin nào có ${r} lớn hơn? Giải thích vì sao xe đồ chơi chạy yếu với pin cũ.</div>${lines(2)}
<div style="padding-top:.6mm"><b>2.</b> Nguồn sai số lớn nhất của nhóm em là gì, cách giảm?</div>${lines(1)}`)}
${foot(5)}</section>`;

const kk = nw(`(thang ampe kế ${m('2\\ \\mathrm A')})`);
const tbDe = (Rxs, Is, Us) => `<table style="text-align:center;margin:.6mm 0"><tr><th style="width:21mm;text-align:left">Lần</th>${Rxs.map((_, i) => `<th>${i + 1}</th>`).join('')}</tr>`
  + `<tr><td style="text-align:left">${Rx} (Ω)</td>${Rxs.map((x) => `<td>${x}</td>`).join('')}</tr><tr><td style="text-align:left">${I} (A)</td>${Is.map((x) => `<td>${x}</td>`).join('')}</tr><tr><td style="text-align:left">${U} (V)</td>${Us.map((x) => `<td>${x}</td>`).join('')}</tr></table>`;
const dang = [
  { t: 'Dạng 1 · Dễ · Hai cặp (I, U) của pin: tìm điện trở trong và suất điện động',
    de: `Nhóm đo một viên pin (ampe kế nối tiếp, vôn kế song song hai cực pin). Vặn biến trở hai lần:<br>Lần 1: ${nw(m('I_1=0{,}20\\ \\mathrm A'))}, ${nw(m('U_1=1{,}36\\ \\mathrm V'))}; lần 2: ${nw(m('I_2=0{,}60\\ \\mathrm A'))}, ${nw(m('U_2=1{,}00\\ \\mathrm V'))}. ${U} là số chỉ vôn kế (hiệu điện thế hai cực pin).<br><b>a)</b> điện trở trong ${r} của pin<br><b>b)</b> suất điện động ${E} của pin`,
    nd: `Hai cặp cùng thoả ${nw(`${m('U=')} ${f(22)}`)}; trừ vế thì mất ${f(10)}; ${nw(`${E} = ${m('U')} + ${f(10)}`)}`, a: ['a', 'b'], gi: 4, fig: H.duongThang() },
  { t: 'Dạng 2 · Trung bình · Dự đoán số chỉ ampe kế, vôn kế và vai trò điện trở bảo vệ',
    de: `Pin cũ ${nw(m('\\mathcal{E}=1{,}55\\ \\mathrm V'))}, ${nw(m('r=0{,}60\\ \\Omega'))}; ${nw(m('R_0=2{,}0\\ \\Omega'))} nối tiếp biến trở đang ở ${nw(m('R_x=3{,}0\\ \\Omega'))}. Ampe kế điện trở không đáng kể, vôn kế điện trở rất lớn, khoá K đóng.<br><b>a)</b> số chỉ ampe kế<br><b>b)</b> số chỉ vôn kế<br><b>c)</b> bạn học sinh bỏ ${R0} rồi vặn ${nw(`${Rx} = 0`)}: dòng qua pin; ampe kế ${nw(`thang ${m('2\\ \\mathrm A')}`)} có chịu được không`,
    nd: `${nw(`${m('I=')} ${f(24)}`)}; ${nw(`${U} = ${E} − ${f(10)}`)}; bỏ ${R0}, ${nw(`${Rx} = 0`)}: ${nw(`${m('I=')} ${f(14)}`)}`, a: ['a', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'], gi: 5, fig: H.soDo('Mạch đo của đề: M, N là hai cực pin.') },
  { t: `Dạng 3 · Khó · Xử lí bảng số liệu: chọn cặp điểm, tính ${r}, ${E} và sai số`,
    de: `Bảng số liệu một viên pin AA, ${nw(m('R_0=2{,}0\\ \\Omega'))}; vôn kế ${nw(m('\\pm0{,}01\\ \\mathrm V'))}, ampe kế ${nw(m('\\pm0{,}002\\ \\mathrm A'))}:
${tbDe([100, 20, 10, 5, 2, 0], ['0,015', '0,069', '0,124', '0,208', '0,348', '0,633'], ['1,54', '1,52', '1,49', '1,46', '1,39', '1,27'])}<b>a)</b> chọn hai lần đo cho ${r} đáng tin nhất (không vẽ đồ thị); tính ${r}<br><b>b)</b> tính ${E}<br><b>c)</b> coi ${r} là thương của hai hiệu, ước lượng ${m('\\Delta r')} bằng cách cộng sai số tỉ đối của tử và mẫu; ghi ${m('r=\\ldots\\pm\\ldots')}`,
    nd: `Chọn hai lần ${f(12)} nhau vì hiệu ${f(8)} lớn so với sai số; ${nw(`${m('\\dfrac{\\Delta r}{r}=')} ${f(14)} + ${f(14)}`)}`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'], cot: 3, gi: 18 },
];

const oY = (s, o, w = {}) => s.split('<br>').map((p) => {
  const y = p.match(/^<b>([a-d])\)<\/b>/);
  if (!y) return `<div>${p}</div>`;
  const ls = o.filter((l) => l[0] === y[1]);
  return `<div class="yo"><span>${p}</span><span class="oo">${ls.map((l) => `<span class="nw"><b>${l})</b>${f(typeof w === 'object' ? (w[l] ?? 25) : w)}</span>`).join('')}</span></div>`;
}).join('');
const ttDe = (b) => b.fig ? `<div class="fig-side" style="grid-template-columns:1fr ${b.fw}mm">${`<div>${oY(b.de, b.o, b.ow)}</div>`}${b.fig}</div>` : oY(b.de, b.o, b.ow);
const vaoVo = (ds) => ds.map((b) => (b.o ? { t: b.t, de: ttDe(b), k: 0 } : b));
const nhap = (n) => ({ t: '<span class="nhap-t">Nháp / chỗ em còn vướng</span>', de: lines(n), k: 0 });
const k2 = nw(`(${A('2')} là thang ampe kế)`);
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–3', 'DẠNG 3 · ĐỌC ĐỒ THỊ'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Một viên pin cho hai cặp số khi đổi biến trở: lần 1 ${nw(m('I_1=0{,}10\\ \\mathrm A'))}, ${nw(m('U_1=1{,}45\\ \\mathrm V'))}; lần 2 ${nw(m('I_2=0{,}50\\ \\mathrm A'))}, ${nw(m('U_2=1{,}13\\ \\mathrm V'))} (${U}: số chỉ vôn kế hai cực pin).<br><b>a)</b> điện trở trong ${r}<br><b>b)</b> suất điện động ${E}`, o: ['a', 'b'] },
    { t: 'Dạng 1 · Bài 2', de: `Một viên pin khác: lần 1 ${nw(m('I_1=0{,}30\\ \\mathrm A'))}, ${nw(m('U_1=1{,}40\\ \\mathrm V'))}; lần 2 ${nw(m('I_2=0{,}90\\ \\mathrm A'))}, ${nw(m('U_2=1{,}04\\ \\mathrm V'))}.<br><b>a)</b> điện trở trong ${r}<br><b>b)</b> suất điện động ${E}`, o: ['a', 'b'] },
    { t: 'Dạng 2 · Bài 1', de: `Pin ${nw(m('\\mathcal{E}=1{,}50\\ \\mathrm V'))}, ${nw(m('r=0{,}50\\ \\Omega'))}; ${nw(m('R_0=1{,}0\\ \\Omega'))} nối tiếp biến trở ${nw(m('R_x=4{,}0\\ \\Omega'))}; ampe kế lí tưởng thang ${nw(m('2\\ \\mathrm A'))}, vôn kế song song hai cực pin.<br><b>a)</b> số chỉ ampe kế<br><b>b)</b> số chỉ vôn kế<br><b>c)</b> bỏ ${R0}, vặn ${nw(`${Rx} = 0`)}: dòng qua pin; ampe kế có chịu được không`, o: ['a', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'], ow: { 'c<sub>2</sub>': 18 } },
    { t: 'Dạng 2 · Bài 2', de: `Pin ${nw(m('\\mathcal{E}=1{,}60\\ \\mathrm V'))}, ${nw(m('r=0{,}40\\ \\Omega'))}; ${nw(m('R_0=2{,}0\\ \\Omega'))} nối tiếp biến trở ${nw(m('R_x=1{,}0\\ \\Omega'))}; ampe kế lí tưởng thang ${nw(m('2\\ \\mathrm A'))}.<br><b>a)</b> số chỉ ampe kế<br><b>b)</b> số chỉ vôn kế<br><b>c)</b> bỏ ${R0}, vặn ${nw(`${Rx} = 0`)}: dòng qua pin; ampe kế có chịu được không`, o: ['a', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'], ow: { 'c<sub>2</sub>': 18 } },
    { t: 'Dạng 3 · Bài 1', de: `Bảng số liệu một viên pin, ${nw(m('R_0=2{,}0\\ \\Omega'))}; vôn kế ${nw(m('\\pm0{,}01\\ \\mathrm V'))}, ampe kế ${nw(m('\\pm0{,}002\\ \\mathrm A'))}:${tbDe([50, 10, 5, 2, 0], ['0,030', '0,124', '0,207', '0,343', '0,612'], ['1,54', '1,49', '1,45', '1,37', '1,22'])}<br><b>a)</b> chọn hai lần đo xa nhau; tính ${r}<br><b>b)</b> tính ${E}<br><b>c)</b> ước lượng ${m('\\Delta r')} (cộng sai số tỉ đối của tử và mẫu); ghi ${m('r=\\ldots\\pm\\ldots')}`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'], ow: { 'a<sub>1</sub>': 18, 'c<sub>2</sub>': 34 } },
  ], [
    { t: 'Dạng 3 · Bài 2', de: `Bảng số liệu một viên pin khác, ${nw(m('R_0=2{,}0\\ \\Omega'))}; cùng sai số dụng cụ:${tbDe([50, 10, 5, 2, 0], ['0,028', '0,116', '0,189', '0,304', '0,514'], ['1,46', '1,39', '1,32', '1,22', '1,03'])}<br><b>a)</b> chọn hai lần đo xa nhau; tính ${r}<br><b>b)</b> tính ${E}<br><b>c)</b> ước lượng ${m('\\Delta r')}; ghi ${m('r=\\ldots\\pm\\ldots')}`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'], ow: { 'a<sub>1</sub>': 18, 'c<sub>2</sub>': 34 } },
    { t: 'Đọc đồ thị', de: `<div class="fig-side" style="grid-template-columns:1fr 44mm"><div>Hai pin cùng ${E}, đường (1) và (2) như hình. <div class="yo"><span>Pin nào có ${r} lớn hơn? Đường số</span><span class="oo"><span class="nw">${f(14)}</span></span></div><div class="yo" style="margin-top:1.5mm"><span>Vì đường đó</span><span class="oo"><span class="nw">${f(32)}</span></span></div></div>${H.haiPin()}</div>`, k: 0 },
    nhap(16),
  ]],
  dap: [
    `D1·1: a) 0,80 Ω · b) 1,53 V &nbsp;|&nbsp; D1·2: a) 0,60 Ω · b) 1,58 V &nbsp;|&nbsp; D2·1: a) 0,27 A · b) 1,36 V · c<sub>1</sub>) 3,0 A · c<sub>2</sub>) không &nbsp;|&nbsp; D2·2: a) 0,47 A · b) 1,41 V · c<sub>1</sub>) 4,0 A · c<sub>2</sub>) không &nbsp;|&nbsp; D3·1: a<sub>1</sub>) lần 1 và 5 · a<sub>2</sub>) 0,55 Ω · b) 1,56 V · c<sub>1</sub>) 0,04 Ω · c<sub>2</sub>) (0,55 ± 0,04) Ω`,
    `D3·2: a<sub>1</sub>) lần 1 và 5 · a<sub>2</sub>) 0,88 Ω · b) 1,48 V · c<sub>1</sub>) 0,05 Ω · c<sub>2</sub>) (0,88 ± 0,05) Ω &nbsp;|&nbsp; Đọc đồ thị: đường (2), dốc hơn`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [2, 1], kq: [[1, 2], [3]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'nhắc lại 1·4 · dụng cụ 2·1 · điện trở bảo vệ 2·2 · các bước 3·1 · bẫy 3·2 · bảng số liệu 4·1 · sai số 4·2 · đồ thị 5·1 · dạng 1–2 → 6·1 · dạng 3 → 7·1',
  out: process.argv[2],
});
