// Ruột tập VL10 – Bài 15 · Định luật 2 Newton (lesson id 60). Quyển Chương 3 lớp 10: bài 13 = tr. 1–12, bài 15 = tr. 25–36.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l10-bai15.mjs (SVG tự vẽ + 1 ảnh thực tế xe trượt băng ở book/assets/anh-that). Nội dung theo bài web
// (book/cache/60.json, tải từ DB 13/11/2026): mục tiêu, dự đoán sân băng, hành trang, II.1–II.5 (hai thí nghiệm, định luật,
// khối lượng – quán tính, các bước giải), ba bẫy, Trả bài 6 câu, bài toán mẫu xe đẩy siêu thị, đổi chiều, thử thách, 6 dạng bài tập mẫu.
// Đáp số Bài tương tự (tuongTu.dap) và mọi số trong bảng tính bằng Python 13/11/2026.
// Chạy: node scripts/ruot-tap/l10-bai15.mjs [file.pdf]   → scripts/ruot-tap/out/ruot-tap-vl10-bai15.pdf
//       node scripts/ruot-tap/l10-bai15.mjs --hinh       → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l10-bai15/
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL10b15 as H } from './hinh-l10-bai15.mjs';
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
  const out = resolve(HERE, 'out/hinh-l10-bai15'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 15, lid: 60, ten: 'ĐỊNH LUẬT 2 NEWTON', lop: 10, baiDau: 13, sub: 'Vật lí 10 · Chương 3: Động lực học' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const u = (s, d) => nw(m(`${s}\\ \\mathrm{${d}}`));
const ms2 = '\\mathrm{m/s^2}';
const g10 = nw(m(`g=10\\ ${ms2}`));
const va = m('\\vec a'), vF = m('\\vec F'), Fhl = m('F_{\\mathrm{hl}}'), Fms = m('F_{\\mathrm{ms}}');
// ô điền kèm đơn vị in sẵn, không gãy dòng
const oDv = (w, dv) => nw(`${f(w)}&nbsp;${dv}`);

// Bài tương tự 1 cột, ô đáp số cuối dòng của ý (cùng cách l12-c3-bai10).
const ttCss = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}.tbl-c td,.tbl-c th{text-align:center;padding:.4mm 1.5mm}.tbl-c td{height:6mm}</style>';

const p1 = `${ttCss}<section class="page">
${head('BÀI 15 · ĐỊNH LUẬT 2 NEWTON', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Đọc số liệu thí nghiệm để tìm mối liên hệ giữa <b>gia tốc, lực và khối lượng</b>`)}
${dong(`${ck}Phát biểu <b>định luật 2 Newton</b>, viết công thức; hiểu ${m('F')} trong công thức là lực nào`)}
${dong(`${ck}Hiểu <b>khối lượng</b> là mức quán tính; đổi đúng đơn vị newton`)}
${dong(`${ck}Giải hai kiểu bài: <b>biết lực → tìm chuyển động</b>, <b>biết chuyển động → tìm lực</b>`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Trên sân băng, em đẩy vào lưng một bạn nhỏ ${u('40', 'kg')} bằng lực ${u('80', 'N')}. Sau đó em đẩy y hệt, cũng ${u('80', 'N')}, vào lưng chú huấn luyện viên ${u('80', 'kg')}. Lúc đẩy, gia tốc hai người so với nhau thế nào?</p>
<div class="fig-side" style="${fs(48)}"><div>
${opt('A', `Bằng nhau, vì cùng một lực đẩy ${u('80', 'N')}`)}
${opt('B', 'Bạn nhỏ có gia tốc gấp đôi chú huấn luyện viên')}
${opt('C', 'Chú huấn luyện viên tăng tốc nhanh hơn, vì nặng nên “đà” lớn')}
${opt('D', `Chú huấn luyện viên đứng yên, vì ${u('80', 'kg')} không nhỏ hơn ${u('80', 'N')}`)}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 2)}</div>
${H.sanBang()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(2)}</div>
${h3(4, 'Kiểm tra hành trang: gia tốc', '1·4')}
<div class="card" style="padding:1.2mm 3mm"><div>
<div>Định nghĩa: ${m('a=')} ${f(25)} &nbsp;· công thức không có ${m('t')}: ${nw(`${m('v^2-v_0^2=')} ${f(16)}`)}</div>
<div style="margin-top:1mm"><b>1.</b> Xe máy tăng tốc đều từ đứng yên lên ${u('10', 'm/s')} trong ${u('5', 's')}.</div>
${lines(1)}<div>Gia tốc ${m('a=')} ${oDv(16, m(ms2))}</div>
<div style="margin-top:1mm"><b>2.</b> Xe đang chạy ${u('10', 'm/s')} thì hãm phanh đều, đi thêm ${u('25', 'm')} thì dừng.</div>
${lines(1)}<div>${m('a=')} ${oDv(16, m(ms2))}; dấu của ${m('a')} cho biết xe ${f(25)}</div>
<div class="hint" style="margin-top:1mm">Đổi đơn vị: ${m('1\\ \\mathrm{g}=10^{-3}\\ \\mathrm{kg}')} · ${m('1')} tấn ${m('=1000\\ \\mathrm{kg}')} · ${m('1\\ \\mathrm{m/s}=3{,}6\\ \\mathrm{km/h}')}</div></div></div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('II · LỰC, KHỐI LƯỢNG VÀ GIA TỐC')}
${h3(1, 'II.1 · Thí nghiệm: giữ khối lượng, đổi lực', '2·1')}
<div class="card fig-side" style="${fs(50)};padding:1.2mm 3mm"><div>
<div><b>Làm:</b> xe ${u('m=0{,}50', 'kg')} trên máng đệm khí (ma sát gần như bằng 0). Quả nặng kéo xe qua ròng rọc; cảm biến đo ${m('F')} (sai số ${u('\\pm0{,}01', 'N')}). Thả xe từ nghỉ ở cổng 1, đo ${m('t')} tới cổng 2 (sai số ${u('\\pm0{,}01', 's')}).</div>
<div style="margin-top:.6mm">Từ ${m('s=\\tfrac12at^2')} (vì ${m('v_0=0')}): ${m('a=')} ${f(16)}</div></div>
${H.mangDemKhi('Cảm biến đo F; hai cổng quang đo t.')}</div>
<div class="fig-side" style="${fs(48)}"><div>
<table class="tbl-c"><tr><th>${m('F\\ (\\mathrm N)')}</th><th>${m('t\\ (\\mathrm s)')}</th><th>${m(`a\\ (${ms2})`)}</th><th>${m('F/a\\ (\\mathrm{kg})')}</th></tr>
<tr><td>0,10</td><td>2,29</td><td>0,19</td><td></td></tr>
<tr><td>0,20</td><td>1,56</td><td>0,41</td><td></td></tr>
<tr><td>0,30</td><td>1,31</td><td>0,58</td><td></td></tr>
<tr><td>0,40</td><td>1,11</td><td>0,81</td><td></td></tr></table>
<div style="margin-top:1mm">${m('F/a')} trung bình ≈ ${oDv(12, 'kg')}, gần bằng ${f(25)} của xe.</div>
<div><b>Rút ra:</b> giữ ${m('m')}, ${m('a')} ${f(25)} với ${m('F')}.</div>
<div>Lần đo kém tin cậy nhất: ${nw(`${m('F=')} ${f(12)}&nbsp;N`)}, vì</div>${lines(1)}</div>
${H.doThiAF()}</div>
${h3(2, 'II.2 · Thí nghiệm: giữ lực, đổi khối lượng', '2·2')}
<div class="card" style="padding:1.2mm 3mm">
<div><b>Làm:</b> chỉnh quả treo để cảm biến luôn đọc ${u('F=0{,}40', 'N')}; chất gia trọng (khối nặng đặt thêm lên xe) để đổi tổng khối lượng xe.</div>
<table class="tbl-c" style="margin:.8mm 0"><tr><th style="width:30mm">${m('m\\ (\\mathrm{kg})')}</th><td>0,50</td><td>0,75</td><td>1,00</td><td>1,50</td></tr>
<tr><th>${m(`a\\ (${ms2})`)}</th><td>0,80</td><td>0,53</td><td>0,40</td><td>0,27</td></tr>
<tr><th>${m('m\\cdot a\\ (\\mathrm N)')}</th><td></td><td></td><td></td><td></td></tr></table>
<div><b>Rút ra:</b> tích ${m('m\\cdot a')} luôn gần bằng ${oDv(12, 'N')}; giữ ${m('F')}, ${m('a')} ${f(25)} với ${m('m')}.</div>
<div>Khối lượng gấp đôi thì gia tốc ${f(25)}.</div></div>
${h3(3, 'II.3 · Định luật 2 Newton', '2·3')}
<div class="card" style="padding:1.2mm 3mm">
<div>Gia tốc của vật cùng hướng với ${f(25)} tác dụng lên vật.</div>
<div>Độ lớn gia tốc tỉ lệ thuận với ${f(25)}, tỉ lệ nghịch với ${f(25)}.</div>
<div style="margin:.8mm 0;font-size:var(--fs-h3)">${va} ${m('=')} ${f(20)} &nbsp;&nbsp; hay &nbsp;&nbsp; ${vF} ${m('=')} ${f(20)}</div>
<div>${vF}: ${f(25)} , tức tổng vectơ mọi lực tác dụng lên vật, đơn vị ${f(12)}</div>
<div>${m('m')}: khối lượng (${f(12)}) &nbsp;· ${va}: gia tốc (${f(14)})</div>
<div><b>Đơn vị lực:</b> ${nw(`${m('1\\ \\mathrm N=')} ${f(25)}`)}, là lực truyền cho vật ${u('1', 'kg')} gia tốc ${f(16)}</div></div>
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('KHỐI LƯỢNG · CÁC BƯỚC GIẢI · BẪY · TỰ KIỂM TRA')}
${h3(1, 'II.4 · Khối lượng là mức quán tính', '3·1')}
<div class="card" style="padding:1.2mm 3mm">
<div>Khối lượng càng lớn, vận tốc càng ${f(25)} thay đổi. Khối lượng là đại lượng ${f(25)}, luôn ${f(16)}, không đổi với mỗi vật.</div>
<div>Khối lượng cộng được: xe ${u('500', 'kg')} chở ${u('300', 'kg')} hàng, cả hệ ${oDv(14, 'kg')}</div>
<div style="margin-top:.6mm"><b>Ví dụ:</b> xe con ${nw('1,5 tấn')} và xe tải ${nw('15 tấn')} cùng chạy ${u('20', 'm/s')}, cùng lực hãm ${u('15\\,000', 'N')}. Quãng dừng ${m('s=\\dfrac{v_0^2}{2|a|}')}.</div>
<table class="tbl-c" style="margin-top:.6mm"><tr><th></th><th>${m('m\\ (\\mathrm{kg})')}</th><th>${m(`|a|\\ (${ms2})`)}</th><th>${m('s\\ (\\mathrm m)')}</th></tr>
<tr><th style="text-align:left">Xe con</th><td></td><td></td><td></td></tr>
<tr><th style="text-align:left">Xe tải</th><td></td><td></td><td></td></tr></table>
<div><b>Rút ra:</b> cùng lực hãm, xe càng nặng càng ${f(25)}.</div></div>
${h3(2, 'II.5 · Bài toán động lực học: các bước', '3·2')}
<div class="card" style="padding:1.2mm 3mm">
<div><b>Vẽ</b> hình, chọn vật, chọn ${f(25)} &nbsp;→ <b>Kể</b> mọi ${f(16)} &nbsp;→ <b>Viết</b> ${nw(`${m('\\Sigma\\vec F=')} ${f(14)}`)}</div>
<div>→ <b>Chiếu</b>: lực cùng chiều dương mang dấu ${f(10)}, ngược chiều mang dấu ${f(10)}; ra ${m('a\\lt 0')} nghĩa là ${f(25)}</div>
<div style="margin-top:.6mm">Nối ${m('a')} với động học: ${m('v=')} ${f(20)} · ${m('s=')} ${f(25)} · ${m('v^2-v_0^2=')} ${f(16)}</div></div>
${h3(3, 'III · Ba cái bẫy hay sập', '3·3')}
<div class="card" style="padding:1mm 3mm">
<div class="trap">${ck}<span><b>“F là lực kéo.”</b> ${m('F')} là hợp lực. Kéo thùng ${u('20', 'kg')} bằng lực ngang ${u('100', 'N')}, ma sát ${u('60', 'N')}: ${nw(`${Fhl}${m('=')} ${f(12)}&nbsp;N`)}, ${nw(`${m('a=')} ${f(12)}&nbsp;${m(ms2)}`)}</span></div>
<div class="fig-side" style="${fs(52)};margin:0"><div class="trap">${ck}<span><b>“Lực hướng đâu, vật chạy hướng đó.”</b> Định luật nói <b>gia tốc</b> cùng hướng hợp lực, không nói vận tốc. Xe đang phanh: ${va} hướng ${f(25)}, ${m('\\vec v')} hướng ${f(25)}. Lực đổi thì ${f(16)} đổi ngay; vận tốc đổi ${f(16)}.</span></div>
${H.xePhanh()}</div>
<div class="trap">${ck}<span><b>“Lấy trọng lượng làm khối lượng, quên đổi gam.”</b> ${m('P=mg')} là lực (N), ${m('m')} đo bằng kg. Vật ${u('P=20', 'N')} chịu hợp lực ${u('5', 'N')}, ${g10}: ${nw(`${m('m=')} ${f(12)}&nbsp;kg`)}, ${nw(`${m('a=')} ${f(12)}&nbsp;${m(ms2)}`)}. Xe ${u('200', 'g')}: ${nw(`${m('m=')} ${f(12)}&nbsp;kg`)}</span></div></div>
${h3(4, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '3·4')}
${rkHai([1, 2, 3], [4, 5, 6])}
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('TRẢ BÀI · BÀI TOÁN MẪU')}
${h3(1, 'IV · Trả bài 6 câu', '4·1')}
${box(`${tb('1. Phát biểu định luật 2 Newton.')}${lines(2)}
${tb('2. Viết công thức, nói tên và đơn vị từng kí hiệu.')}${lines(1)}
${tb('3. 1 N là gì?')}${lines(1)}
${tb('4. Khối lượng có những tính chất gì? Liên quan quán tính thế nào?')}${lines(2)}
${tb('5. F trong công thức là lực nào? Gia tốc cùng hướng với gì?')}${lines(1)}
${tb('6. Nêu các bước giải bài toán động lực học.')}${lines(2)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/6 câu · chưa thuộc: ${f(25)} ${nw(`→ đọc lại ô ${f(12)} Tập`)}</div>
${h3(2, 'V · Bài toán mẫu: xe đẩy siêu thị', '4·2')}
<div class="card soft" style="padding:1.2mm 3mm">Xe đẩy chở đầy hàng, tổng khối lượng ${u('60', 'kg')}, đang đứng yên. Một người đẩy xe bằng lực nằm ngang ${u('90', 'N')}; lực ma sát cản xe là ${u('30', 'N')}. Tìm gia tốc của xe, vận tốc và quãng đường xe đi được sau ${u('4', 's')}.</div>
<table><tr><th style="width:44mm">Câu trong đề</th><th>Dữ liệu → kiến thức</th></tr>
<tr><td>“tổng khối lượng 60 kg”</td><td>${m('m=60\\ \\mathrm{kg}')} (khối lượng cộng được)</td></tr>
<tr><td style="height:6.5mm">“đang đứng yên”</td><td></td></tr>
<tr><td style="height:6.5mm">“lực nằm ngang 90 N”, “ma sát 30 N”</td><td></td></tr>
<tr><td style="height:6.5mm">“sau 4 s”</td><td></td></tr></table>
<div class="fig-side" style="${fs(52)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl('Chiều dương; lực theo phương đứng:', 2)}${wl(`Hợp lực ${Fhl}:`, 1)}${wl(`Gia tốc ${m('a')}:`, 1)}${wl(`${m('v')} và ${m('s')} sau 4 s:`, 2)}${wl('Kiểm tra dấu, đơn vị:', 1)}</div>${H.xeDay()}</div>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TẬP VỀ NHÀ · ĐỔI CHIỀU · THỬ THÁCH · MANG VỀ')}
${K.btvn()}
${h3(2, 'Điền bước còn thiếu: sàn bẩn, ma sát 42 N', '5·2')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div class="ln">Bước 1: ${Fhl}${m('=')}</div><div class="ln">Bước 2: ${m('a=')}</div>
<div class="ln"><b>Bước 3 (cho sẵn):</b> ${m('s=\\tfrac12at^2=')} ${oDv(16, 'm')}</div></div>
${h3(3, 'Đổi chiều: biết chuyển động, tìm lực', '5·3')}
${box(wl(`Ô tô ${nw('1,2 tấn')} đang chạy ${u('15', 'm/s')} thì phanh, dừng sau ${u('25', 'm')}. Tìm gia tốc và lực hãm (độ lớn, hướng so với chiều chuyển động).`, 4))}
${h3(4, 'Thử thách phân tầng', '5·4')}
${box(wl(`${m('\\bigstar')} Lực ${u('12', 'N')} truyền cho vật gia tốc ${u('3', 'm/s^2')}. Khối lượng vật?`, 2)
 + wl(`${m('\\bigstar\\bigstar')} Lực ${m('F')} truyền cho vật ${m('m_1')} gia tốc ${u('2', 'm/s^2')}, cho vật ${m('m_2')} gia tốc ${u('3', 'm/s^2')}. Ghép hai vật, cùng lực ấy cho gia tốc bao nhiêu?`, 3)
 + wl(`${m('\\bigstar\\bigstar\\bigstar')} Ô tô ${nw('1 tấn')} chạy ${nw('36 km/h')} thì thấy vật cản cách ${u('30', 'm')}, phanh với lực hãm ${u('2000', 'N')}. Xe có dừng kịp không?`, 4))}
${h3(5, 'VI · Mang về: điều em dễ quên nhất', '5·5')}
<div class="fig-side" style="${fs(46)}">${box(wl('1.', 2) + wl('2.', 2) + wl('3.', 2))}${H.xeTruotBang()}</div>
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Tìm gia tốc từ lực và khối lượng',
    de: `Xe điều khiển từ xa ${u('250', 'g')} đứng yên trên mặt bàn nhẵn; động cơ kéo xe bằng lực nằm ngang ${u('0{,}8', 'N')}; bỏ qua ma sát và lực cản không khí.<br><b>a)</b> khối lượng xe theo kg<br><b>b)</b> gia tốc của xe`,
    nd: `đổi ${m('m')} ra ${f(12)} trước; không ma sát ⇒ lực kéo chính là ${f(25)}`, a: ['a', 'b'], gi: 2, cot: 2 },
  { t: 'Dạng 2 · Trung bình · Có ma sát: hợp lực và hướng gia tốc',
    de: `Công nhân kéo thùng hàng ${u('35', 'kg')} trên sàn kho bằng dây nằm ngang, lực ${u('120', 'N')}; sàn tác dụng lực ma sát ${u('50', 'N')}; thùng trượt về phía người kéo.<br><b>a)</b> hợp lực lên thùng<br><b>b)</b> độ lớn gia tốc<br><b>c)</b> hướng gia tốc`,
    nd: `hai lực ngược chiều ⇒ ${Fhl}${m('=')} ${f(22)}; ${va} cùng hướng ${f(22)}`, a: ['a', 'b', 'c'], gi: 3, cot: 3, fig: `<div style="width:40mm;margin-left:auto">${H.thungKeo('')}</div>` },
  { t: 'Dạng 3 · Trung bình · Chất thêm hàng, đổi lực đẩy',
    de: `Xe đẩy siêu thị rỗng được đẩy bằng lực ngang ${u('15', 'N')} thì có gia tốc ${u('0{,}5', 'm/s^2')}. Chất lên xe kiện hàng ${u('40', 'kg')}, đẩy bằng lực ngang ${u('28', 'N')}. Bỏ qua ma sát.<br><b>a)</b> khối lượng xe rỗng<br><b>b)</b> khối lượng xe khi chở hàng<br><b>c)</b> gia tốc của xe khi chở hàng`,
    nd: `lần 1 biết ${m('F')}, ${m('a')} ⇒ ${nw(`${m('m=')} ${f(16)}`)}; khối lượng ${f(25)} được`, a: ['a', 'b', 'c'], gi: 3 },
  { t: 'Dạng 4 · Khá · Từ nghỉ: gia tốc, vận tốc, quãng đường',
    de: `Thùng ${u('12', 'kg')} đứng yên trên sàn ngang, được kéo bằng lực ngang ${u('54', 'N')}; ma sát ${u('18', 'N')}. Sau ${u('6', 's')}:<br><b>a)</b> gia tốc của thùng<br><b>b)</b> vận tốc<br><b>c)</b> quãng đường đi được`,
    nd: `“đứng yên” ⇒ ${nw(`${m('v_0=')} ${f(12)}`)}; dùng ${nw(`${m('v=')} ${f(16)}`)}, ${nw(`${m('s=')} ${f(20)}`)}`, a: ['a', 'b', 'c'], gi: 3 },
  { t: 'Dạng 5 · Khá · Từ quãng đường phanh tìm lực hãm',
    de: `Ô tô ${nw('1,4 tấn')} chạy ${nw('108 km/h')} thì phanh gấp, vết phanh dài ${u('90', 'm')} rồi dừng; lực hãm không đổi.<br><b>a)</b> gia tốc (có dấu; chiều dương là chiều chuyển động)<br><b>b)</b> độ lớn lực hãm<br><b>c)</b> hướng lực hãm so với chiều chuyển động`,
    nd: `không có ${m('t')} ⇒ ${nw(`${m('v^2-v_0^2=')} ${f(14)}`)}; ${nw(`${m('F\\lt 0')} nghĩa là ${f(22)}`)}`, a: ['a', 'b', 'c'], gi: 3, cot: 3, fig: `<div style="width:40mm;margin-left:auto">${H.otoPhanh('')}</div>` },
  { t: 'Dạng 6 · Khó · Tắt máy khi đang chạy đều',
    de: `Ô tô ${nw('1,8 tấn')} chạy thẳng đều ${nw('90 km/h')}, lực kéo ${u('900', 'N')}. Tại O tắt máy; lực cản không đổi.<br><b>a)</b> lực cản lúc chạy đều<br><b>b)</b> gia tốc sau khi tắt máy (có dấu)<br><b>c)</b> thời gian từ O đến khi dừng<br><b>d)</b> quãng đường từ O đến khi dừng`,
    nd: `chạy đều ⇒ ${nw(`${m('a=')} ${f(10)}`)} ⇒ ${nw(`${m('F_{\\mathrm c}=')} ${f(14)}`)}; tắt máy ⇒ hợp lực là ${f(22)}`, a: ['a', 'b', 'c', 'd'], gi: 3, fig: `<div style="width:40mm;margin-left:auto">${H.tatMay('')}</div>` },
];

// Bài tương tự giải vào vở (thầy chốt 10/11): 1 cột; ô đáp số cuối đúng dòng của ý, nhãn ô khớp a) b) c)…
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
  tieuDe: ['DẠNG 1–3', 'DẠNG 4–6'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Xe đồ chơi ${u('400', 'g')} trên sàn nhẵn, kéo bằng lực nằm ngang ${u('1{,}2', 'N')}; bỏ qua ma sát.<br><b>a)</b> khối lượng xe theo kg<br><b>b)</b> gia tốc của xe`, o: ['a', 'b'] },
    { t: 'Dạng 1 · Bài 2', de: `Vật ${u('600', 'g')} trên mặt bàn nhẵn chịu lực nằm ngang ${u('1{,}5', 'N')}; bỏ qua ma sát.<br><b>a)</b> gia tốc của vật<br><b>b)</b> lực tăng gấp đôi: gia tốc khi đó`, o: ['a', 'b'] },
    { t: 'Dạng 2 · Bài 1', de: `Đẩy tủ ${u('50', 'kg')} trên sàn bằng lực nằm ngang ${u('160', 'N')}; lực ma sát ${u('110', 'N')}.<br><b>a)</b> hợp lực lên tủ<br><b>b)</b> độ lớn gia tốc<br><b>c)</b> hướng gia tốc so với lực đẩy`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 2 · Bài 2', de: `Thùng ${u('40', 'kg')} đang trượt sang phải; người kéo bằng dây nằm ngang lực ${u('90', 'N')} hướng sang phải; ma sát ${u('150', 'N')}.<br><b>a)</b> hợp lực (độ lớn, hướng)<br><b>b)</b> độ lớn gia tốc<br><b>c)</b> thùng nhanh dần hay chậm dần`, fig: H.thungKeo('Thùng đang trượt sang phải.', { F: '90 N', ms: '150 N', m: '40 kg' }), fw: 46, o: ['a', 'b', 'c'] },
    { t: 'Dạng 3 · Bài 1', de: `Xe rỗng đẩy bằng lực ngang ${u('20', 'N')} có gia tốc ${u('0{,}8', 'm/s^2')}. Chất thêm ${u('15', 'kg')} hàng, đẩy bằng lực ngang ${u('30', 'N')}; bỏ qua ma sát.<br><b>a)</b> khối lượng xe rỗng<br><b>b)</b> khối lượng khi chở hàng<br><b>c)</b> gia tốc khi chở hàng`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 3 · Bài 2', de: `Cùng lực ${m('F')} (là hợp lực) truyền cho vật ${m('m_1')} gia tốc ${u('6', 'm/s^2')}, cho vật ${m('m_2')} gia tốc ${u('3', 'm/s^2')}.<br><b>a)</b> tỉ số ${m('m_2/m_1')}<br><b>b)</b> ghép hai vật thành một, cùng lực ${m('F')}: gia tốc`, o: ['a', 'b'] },
    nhap(2),
  ], [
    { t: 'Dạng 4 · Bài 1', de: `Xe ${u('20', 'kg')} đứng yên trên sàn ngang, kéo bằng lực ngang ${u('70', 'N')}; ma sát ${u('30', 'N')}. Sau ${u('5', 's')}:<br><b>a)</b> gia tốc<br><b>b)</b> vận tốc<br><b>c)</b> quãng đường`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 4 · Bài 2', de: `Thùng ${u('15', 'kg')} đứng yên trên sàn ngang, kéo bằng lực ngang ${u('45', 'N')}; ma sát ${u('15', 'N')}.<br><b>a)</b> gia tốc<br><b>b)</b> thời gian để thùng đi được ${u('16', 'm')}<br><b>c)</b> vận tốc lúc đó`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 5 · Bài 1', de: `Xe máy chở người, tổng ${u('120', 'kg')}, chạy ${nw('54 km/h')} thì phanh, trượt thêm ${u('15', 'm')} rồi dừng. Lực hãm không đổi; chiều dương là chiều chuyển động.<br><b>a)</b> ${m('v_0')} theo m/s<br><b>b)</b> gia tốc (có dấu)<br><b>c)</b> độ lớn lực hãm; hướng so với chiều chuyển động`, o: ['a', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'] },
    { t: 'Dạng 5 · Bài 2', de: `Ô tô ${nw('2 tấn')} chạy ${nw('72 km/h')} thì phanh, dừng sau ${u('4{,}0', 's')}. Lực hãm không đổi; chiều dương là chiều chuyển động.<br><b>a)</b> gia tốc (có dấu)<br><b>b)</b> độ lớn lực hãm<br><b>c)</b> quãng đường phanh`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 6 · Bài 1', de: `Ô tô ${nw('1,2 tấn')} chạy thẳng đều ${nw('72 km/h')} trên đường ngang, lực kéo động cơ ${u('600', 'N')}; rồi tắt máy, lực cản không đổi.<br><b>a)</b> lực cản<br><b>b)</b> gia tốc sau khi tắt máy (có dấu)<br><b>c)</b> thời gian đến khi dừng<br><b>d)</b> quãng đường đến khi dừng`, o: ['a', 'b', 'c', 'd'] },
    { t: 'Dạng 6 · Bài 2', de: `Ô tô ${nw('1,5 tấn')} chạy thẳng đều ${nw('36 km/h')}, lực kéo động cơ ${u('1500', 'N')}; rồi tắt máy, lực cản không đổi.<br><b>a)</b> gia tốc sau khi tắt máy (có dấu)<br><b>b)</b> quãng đường đến khi dừng<br><b>c)</b> để dừng trong ${u('20', 'm')} sau khi tắt máy: lực hãm cần thêm`, fig: H.tatMay('', { v: '36 km/h', Fk: '1500 N' }), fw: 46, o: ['a', 'b', 'c'] },
  ]],
  dap: [
    `D1·1: a) 0,40 kg · b) 3,0 m/s² &nbsp;|&nbsp; D1·2: a) 2,5 m/s² · b) 5,0 m/s² &nbsp;|&nbsp; D2·1: a) 50 N · b) 1,0 m/s² · c) cùng hướng lực đẩy &nbsp;|&nbsp; D2·2: a) 60 N, sang trái · b) 1,5 m/s² · c) chậm dần &nbsp;|&nbsp; D3·1: a) 25 kg · b) 40 kg · c) 0,75 m/s² &nbsp;|&nbsp; D3·2: a) 2 · b) 2,0 m/s²`,
    `D4·1: a) 2,0 m/s² · b) 10 m/s · c) 25 m &nbsp;|&nbsp; D4·2: a) 2,0 m/s² · b) 4,0 s · c) 8,0 m/s &nbsp;|&nbsp; D5·1: a) 15 m/s · b) −7,5 m/s² · c<sub>1</sub>) 900 N · c<sub>2</sub>) ngược chiều &nbsp;|&nbsp; D5·2: a) −5,0 m/s² · b) 10 000 N · c) 40 m &nbsp;|&nbsp; D6·1: a) 600 N · b) −0,50 m/s² · c) 40 s · d) 400 m &nbsp;|&nbsp; D6·2: a) −1,0 m/s² · b) 50 m · c) 2250 N`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 3], kq: [[1, 2, 3], [4, 5, 6]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'hành trang 1·4 · thí nghiệm a–F 2·1 · a–m 2·2 · định luật 2·3 · khối lượng 3·1 · các bước giải 3·2 · bẫy 3·3 · trả bài 4·1 · bài toán mẫu 4·2 · đổi chiều 5·3 · dạng 1–3 → 6·1 · dạng 4–6 → 7·1',
  out: process.argv[2],
});
