// Ruột tập VL10 – Bài 19 · Lực cản và lực nâng (lesson id 64). Quyển Chương 3 lớp 10 (bài 13–22): bài 19 = tr. 73–84.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l10-bai19.mjs (SVG tự vẽ + 1 ảnh thật nhảy dù trong book/assets/anh-that/, CC BY 2.0). Nội dung theo bài web
// (book/cache/64.json, tải 13/11/2026): mục tiêu, dự đoán hai tờ giấy, hành trang, II.1–II.6, thí nghiệm phễu giấy và bình tràn,
// ba bẫy, Trả bài 6 câu, bài toán mẫu khối nhôm, thử thách, 3 dạng bài tập mẫu (quả cầu, bung dù, lực kế tìm ρ chất lỏng).
// Đáp số Bài tương tự (tuongTu.dap) tính bằng Python 13/11/2026.
// Chạy: node scripts/ruot-tap/l10-bai19.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl10-bai19.pdf
//       node scripts/ruot-tap/l10-bai19.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l10-bai19/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL10b19 as H } from './hinh-l10-bai19.mjs';

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
  const out = resolve(HERE, 'out/hinh-l10-bai19'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 19, lid: 64, ten: 'LỰC CẢN VÀ LỰC NÂNG', lop: 10, baiDau: 13, sub: 'Vật lí 10 · Chương 3: Động lực học' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const g10 = nw(m('g=10\\ \\mathrm{m/s^2}'));
const rn = nw(`${m('\\rho')}<sub>nước</sub>${m('=1000\\ \\mathrm{kg/m^3}')}`);
const FA = m('F_A'), P = m('P'), V = m('V'), rho = m('\\rho');

// Bài tương tự xếp 1 cột, ô đáp số cuối dòng ý (như bài 23).
const ttCss = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';
const p1 = `${ttCss}<section class="page">
${head('BÀI 19 · LỰC CẢN VÀ LỰC NÂNG', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Nêu đặc điểm <b>lực cản</b> của chất lưu (chất lỏng, chất khí)`)}
${dong(`${ck}Mô tả <b>ba giai đoạn</b> của vật rơi trong không khí, hiểu <b>tốc độ giới hạn</b>`)}
${dong(`${ck}Viết và dùng công thức <b>lực đẩy Archimedes</b>; giải thích bằng chênh lệch áp suất`)}
${dong(`${ck}So trọng lượng với lực đẩy để biết vật <b>nổi, lơ lửng hay chìm</b>`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Viên giấy vo chạm sàn trước, tờ phẳng chao lượn mãi mới rơi. Vì sao tờ phẳng rơi chậm hơn hẳn?</p>
<div class="fig-side" style="${fs(46)}"><div>
${opt('A', 'Viên giấy vo tròn nặng hơn tờ phẳng')}
${opt('B', 'Không khí cản tờ phẳng mạnh hơn nhiều, vì nó hứng gió trên diện tích lớn')}
${opt('C', 'Trái Đất hút tờ phẳng yếu hơn, vì nó trải rộng ra')}
${opt('D', 'Lực đẩy Archimedes của không khí lên tờ phẳng lớn hơn, vì nó to hơn')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 1)}</div>
${H.haiTo('Hai tờ A4 giống hệt nhau lúc vừa thả.')}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f(12)} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'Hành trang (KHTN 8)', '1·4')}
<div class="card" style="padding:1.2mm 3mm">
<div>${nw(`${m('1')} lít ${m('=1\\ \\mathrm{dm^3}=')} ${f(16)}&nbsp;${m('\\mathrm{m^3}')}`)} &nbsp;·&nbsp; ${nw(`${m('1\\ \\mathrm{cm^3}=1\\ \\mathrm{ml}=')} ${f(16)}&nbsp;${m('\\mathrm{m^3}')}`)}</div>
<div>Khối lượng riêng ${nw(`${rho} = <span class="fill" style="min-width:16mm;height:9mm"></span>`)} &nbsp;·&nbsp; áp suất chất lỏng ở độ sâu ${m('h')}: ${nw(`${m('p=')} ${f(14)}`)}</div>
<div>Nước ${rn}, sâu ${m('2\\ \\mathrm m')}, ${g10}: ${nw(`${m('p=')} ${f(16)}&nbsp;Pa`)}</div></div>
${h3(5, 'II.1 · Lực cản của chất lưu', '1·5')}
<div class="card" style="padding:1.2mm 3mm">
<div><b>Chất lưu</b> = chất ${f(16)} và chất ${f(16)} (nước, dầu, không khí…).</div>
<div>Vật chuyển động trong chất lưu luôn chịu lực cản. <b>Điểm đặt:</b> vẽ tại ${f(25)} của vật.</div>
<div><b>Phương, chiều:</b> cùng phương, ${f(25)} chiều chuyển động.</div>
<div><b>Độ lớn</b> phụ thuộc hai yếu tố của vật: ${f(25)} và ${f(25)}</div></div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('PHỄU GIẤY RƠI · BA GIAI ĐOẠN · LỰC NÂNG')}
${h3(1, 'Thí nghiệm: phễu giấy rơi', '2·1')}
<div class="card" style="padding:1.2mm 3mm">
<div><b>Làm:</b> thả phễu giấy (khuôn giấy nướng bánh) từ cao ${nw('2,5 m')}; quay chậm đoạn ${nw('1,50 m')} cuối để đo ${m('t')}. Chồng 1, 2, 3, 4 phễu lồng khít (trọng lượng gấp 1, 2, 3, 4). Qua ${nw('1 m')} đầu, phễu đã rơi đều.</div>
<div class="fig-side" style="${fs(62, 'margin-top:.8mm')}">
<table class="tbl-ct"><tr><th>Số phễu ${m('n')}</th><th>${m('t\\ (\\mathrm s)')}</th><th>${m('v=\\dfrac{1{,}50}{t}\\ (\\mathrm{m/s})')}</th><th>${m('v^2/n')}</th></tr>
<tr><td>1</td><td>1,38</td><td>1,09</td><td>1,19</td></tr>
<tr><td>2</td><td>0,95</td><td></td><td></td></tr>
<tr><td>3</td><td>0,80</td><td>1,88</td><td>1,18</td></tr>
<tr><td>4</td><td>0,67</td><td></td><td></td></tr></table>
<div>
<div>Rơi đều ⇒ lực cản ${f(12)} trọng lượng.</div>
<div>Trọng lượng gấp 4, tốc độ chỉ gấp khoảng ${f(12)} lần.</div>
<div>Cột ${m('v^2/n')} gần như ${f(25)} ⇒ lực cản tăng gần theo ${f(12)}.</div></div></div></div>
${h3(2, 'II.2 · Vật rơi trong không khí: ba giai đoạn', '2·2')}
<div class="fig-side" style="${fs(44)}"><div class="card" style="padding:1.2mm 3mm;margin:0">
<div><b>GĐ 1</b> (rất ngắn): ${m('v')} nhỏ, lực cản gần bằng ${f(12)}; gần như nhanh dần đều, ${nw(`${m('a\\approx')} ${f(12)}&nbsp;${m('\\mathrm{m/s^2}')}`)}</div>
<div><b>GĐ 2:</b> ${m('v')} tăng, lực cản ${f(16)}, hợp lực ${f(16)} ⇒ vẫn nhanh dần nhưng gia tốc ${f(16)}</div>
<div><b>GĐ 3:</b> lực cản ${f(12)} trọng lượng, hợp lực ${f(12)}: rơi ${f(16)} với <b>tốc độ giới hạn</b> ${m('v_{gh}')}</div>
<div style="margin-top:.6mm">Ghi số 1, 2, 3 vào ba ô dưới đồ thị.</div></div>
${H.vt('Đường đặc: tốc độ của vật. Đường đứt: rơi tự do.')}</div>
<div class="fig-side" style="${fs(34, 'margin-top:1.2mm')}"><div class="card" style="padding:1.2mm 3mm;margin:0">
<div><b>Nhảy dù</b> (số liệu minh hoạ): chưa mở dù, sau khoảng ${nw('12 s')} tốc độ đạt cỡ ${nw('50 m/s')} rồi không tăng nữa.</div>
<div>Mở dù: lực cản tăng vọt, ${ck}lớn hơn ${ck}nhỏ hơn trọng lượng ⇒ người ${f(25)} dần, tới khi cân bằng thì rơi đều với tốc độ ${ck}lớn hơn ${ck}nhỏ hơn ${nw('50 m/s')}</div>
<div>Dù càng rộng thì tốc độ giới hạn càng ${f(16)}</div></div>
${H.nhayDu('Chưa mở dù. Ảnh: Tony Danbury, Wikimedia Commons, CC BY 2.0.')}</div>
${h3(3, 'II.3 · Lực nâng của chất lưu', '2·3')}
<div class="card" style="padding:1.2mm 3mm">
<div><b>Khinh khí cầu:</b> lực đẩy Archimedes của ${f(25)} lớn hơn trọng lượng cả khí cầu nên bay lên. Khí nóng ${f(16)} hơn khí lạnh bên ngoài.</div>
<div><b>Máy bay:</b> lực nâng do không khí ${f(25)} qua cánh, nên phải chạy đủ nhanh mới cất cánh.</div></div>
${h3(4, 'Làm nhanh', '2·4')}
${box(cau(`<b>Câu 1.</b> Đã mở dù, rơi đều ${nw('5 m/s')}: còn trọng lực không? Lực cản so với trọng lượng, hợp lực?`, 2))}
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('LỰC ĐẨY ARCHIMEDES · CHÊNH LỆCH ÁP SUẤT · NỔI, CHÌM')}
${h3(1, 'II.4 · Lực đẩy Archimedes', '3·1')}
<div class="card" style="padding:1.2mm 3mm">
<div><b>Điểm đặt:</b> trọng tâm phần ${f(25)} bị vật chiếm chỗ. <b>Phương</b> ${f(16)}, <b>chiều</b> từ ${f(16)}</div>
<div><b>Độ lớn</b> bằng trọng lượng phần ${f(25)} bị chiếm chỗ: &nbsp;${nw(`${FA} = ${f(14)} = ${f(12)}`)} (dùng ${m('d=\\rho g')})</div>
<div>${rho}: khối lượng riêng của ${f(25)} (kg/m³) · ${V}: thể tích ${f(25)} (m³)</div></div>
${h3(2, 'Thí nghiệm: lực kế và bình tràn', '3·2')}
<div class="fig-side" style="${fs(48)}"><div class="card" style="padding:1.2mm 3mm;margin:0">
<div><b>Làm:</b> treo khối nhôm ${nw('100 cm³')} vào lực kế, nhúng dần vào bình nước đầy tới miệng, hứng nước tràn ra ${nw(`(${m('g=9{,}8\\ \\mathrm{m/s^2}')}).`)}</div>
<div><b>Quan sát:</b> chìm hẳn: lực kế chỉ ${nw('1,67 N')}; hạ sâu thêm vẫn ${nw('1,67 N')}. Nước tràn ra ${nw('100 cm³')}.</div>
<div>Lực kế giảm: ${nw(`${m('2{,}65-1{,}67=')} ${f(12)}&nbsp;N`)}</div>
<div>Trọng lượng nước tràn: ${nw(`${m('1000\\cdot 9{,}8\\cdot')} ${f(16)} ${m('=')} ${f(12)}&nbsp;N`)}</div>
<div><b>Rút ra:</b> lực đẩy tăng theo phần ${f(16)}, không tăng theo ${f(16)}</div></div>
${H.binhTran('Lực kế ở ba lần đo.')}</div>
${h3(3, 'II.5 · Vì sao có lực đẩy: chênh lệch áp suất', '3·3')}
<div class="fig-side" style="${fs(44)}"><div class="card" style="padding:1.2mm 3mm;margin:0">
<div>Áp suất ở độ sâu ${m('h')}: ${nw(`${m('p=p_0+')} ${f(14)}`)} &nbsp;(${m('p_0')}: áp suất khí quyển)</div>
<div>Chênh nhau ${m('\\Delta h')}: ${nw(`${m('\\Delta p=')} ${f(14)}`)}, ${ck}có ${ck}không phụ thuộc ${m('p_0')}</div>
<div>Mặt dưới sâu hơn ⇒ ${m('F_2')} ${f(10)} ${m('F_1')}; các mặt bên ${f(25)}</div>
<div>${nw(`${m('F_2-F_1=\\Delta p\\cdot S=')} ${f(16)} ${m('=\\rho g V')}`)}</div></div>
${H.hopApSuat('Hộp đáy S, cao Δh chìm hẳn.')}</div>
${h3(4, 'II.6 · Nổi, lơ lửng hay chìm', '3·4')}
<table><tr><th style="width:42mm">Khi vật chìm hẳn</th><th>Vật sẽ</th></tr>
<tr><td>${m('P\\gt F_A')}</td><td></td></tr>
<tr><td>${m('P=F_A')}</td><td></td></tr>
<tr><td>${m('P\\lt F_A')}</td><td></td></tr>
<tr><td>Đã nổi yên trên mặt</td><td>${FA} của phần chìm ${ck}lớn hơn ${ck}bằng ${ck}nhỏ hơn ${P}</td></tr></table>
${box(wl(`Thép có khối lượng riêng gấp gần 8 lần nước. Vì sao tàu thép vẫn nổi?`, 2), 'margin-top:1.2mm')}
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('BẪY · TRẢ BÀI · TỰ KIỂM TRA')}
${h3(1, 'III · Ba cái bẫy hay sập', '4·1')}
<div class="card" style="padding:1mm 3mm">
<div class="trap">${ck}<span><b>“Rơi đều là hết lực.”</b> Trọng lực vẫn còn nguyên; lực cản bằng trọng lượng, ${nw('hợp lực bằng 0.')}</span></div>
<div class="trap">${ck}<span><b>“Lấy ${rho} của vật, ${V} cả vật.”</b> Lấy ${rho} của <b>chất lỏng</b>, ${V} <b>phần chìm</b>, đổi ra m³.</span></div>
<div class="trap">${ck}<span><b>“Càng sâu, lực đẩy càng lớn.”</b> Áp suất tăng theo độ sâu, nhưng ${m('F_A=\\rho gV')} không có ${m('h')}. Chìm hẳn rồi thì sâu mấy cũng thế.</span></div></div>
${h3(2, 'IV · Trả bài 6 câu', '4·2')}
${box(`${tb('1. Nêu đặc điểm lực cản của chất lưu.')}${lines(2)}
${tb('2. Vật rơi trong không khí qua mấy giai đoạn? Kể tên.')}${lines(3)}
${tb('3. Công thức lực đẩy Archimedes, tên và đơn vị từng kí hiệu.')}${lines(2)}
${tb('4. Lực đẩy Archimedes đặt ở đâu, hướng nào?')}${lines(1)}
${tb('5. Độ chênh áp suất giữa hai điểm trong chất lỏng phụ thuộc gì?')}${lines(1)}
${tb('6. Khi nào vật nổi, lơ lửng, chìm?')}${lines(2)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/6 câu · chưa thuộc: ${f(25)} ${nw(`→ đọc lại ô ${f(12)} Tập`)}</div>
${h3(3, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '4·3')}
${rkHai([1, 2, 3], [4, 5, 6])}
${h3(4, 'Làm nhanh', '4·4')}
${box(cau(`<b>Câu 1.</b> Khối gỗ ${nw('2,0 dm³')} nổi trên nước, phần chìm ${nw('1,2 dm³')}; ${rn}, ${g10}. Lực đẩy Archimedes? Trọng lượng khối gỗ?`, 2))}
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TOÁN MẪU: KHỐI NHÔM TREO LỰC KẾ')}
${h3(1, 'V · Đề bài', '5·1')}
<div class="fig-side" style="${fs(44)}"><div class="card soft" style="padding:1.2mm 3mm;margin:0">Một khối nhôm đặc treo vào lực kế, ngoài không khí lực kế chỉ ${nw('5,4 N')}. Nhúng khối nhôm chìm hoàn toàn trong nước. Khối lượng riêng của nhôm ${nw(m('2700\\ \\mathrm{kg/m^3}'))}, của nước ${nw(m('1000\\ \\mathrm{kg/m^3}'))}, ${g10}.
<div>Tìm thể tích khối nhôm, lực đẩy Archimedes và số chỉ lực kế.</div></div>
${H.nhomLucKe('Cùng một khối nhôm.')}</div>
${h3(2, 'Phân tích đề')}
<table><tr><th style="width:48mm">Câu trong đề</th><th>Dữ liệu → kiến thức</th></tr>
<tr><td>“ngoài không khí lực kế chỉ ${nw('5,4 N')}”</td><td>${m('P=5{,}4\\ \\mathrm N')} → tìm khối lượng ${m('m=P/g')}</td></tr>
<tr><td style="height:6.5mm">“nhôm 2700 kg/m³”</td><td></td></tr>
<tr><td style="height:6.5mm">“chìm hoàn toàn” (dữ kiện ngầm)</td><td></td></tr>
<tr><td style="height:6.5mm">“nước 1000 kg/m³”</td><td></td></tr>
<tr><td style="height:6.5mm">“số chỉ lực kế khi nhúng”, vật đứng yên</td><td></td></tr></table>
${h3(3, 'Giải')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm;margin-top:1mm">
${wl(`Khối lượng ${m('m')}:`, 1)}${wl(`Thể tích ${m('V')}:`, 2)}${wl(`Lực đẩy ${FA}:`, 2)}${wl(`Số chỉ lực kế ${m('T')} (vật đứng yên: ${m('T+F_A=P')}):`, 2)}${wl(`Kiểm tra: ${m('P/F_A')} có bằng tỉ số khối lượng riêng nhôm/nước?`, 1)}</div>
${h3(4, 'Điền bước còn thiếu: nhúng chìm hẳn trong dầu', '5·4')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div class="ln"><b>Bước 1 (cho sẵn):</b> dầu ${nw(m('\\rho=800\\ \\mathrm{kg/m^3}'))}; ${m('V')} như bài trên (không đổi)</div>
${wl(`Bước 2: ${m('F_A=')}`, 1)}${wl(`Bước 3: ${m('T=')}`, 1)}</div>
${h3(5, 'Thử sức đổi chiều', '5·5')}
${box(wl(`Vật nặng ${nw('5,4 N')} ngoài không khí, chìm hẳn trong nước lực kế chỉ ${nw('3,4 N')}. Tìm khối lượng riêng của vật, vật làm bằng gì?`, 3))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Quả cầu chìm hoàn toàn: tính lực đẩy Archimedes',
    de: `Quả cầu thể tích ${m('400\\ \\mathrm{cm^3}')} nhúng chìm hoàn toàn trong nước biển ${nw(m('\\rho=1030\\ \\mathrm{kg/m^3}'))}; ${g10}.<br><b>a)</b> đổi thể tích ra ${m('\\mathrm{m^3}')}<br><b>b)</b> độ lớn lực đẩy Archimedes`,
    nd: `${rho} của ${f(25)}; chìm hoàn toàn ⇒ ${nw(`${m('V')}<sub>chìm</sub> ${m('=')} ${f(12)}`)}; ${nw(`${m('1\\ \\mathrm{cm^3}=')} ${f(16)}&nbsp;${m('\\mathrm{m^3}')}`)}`, a: ['a', 'b'], gi: 4, fig: H.cauBien('Hình không vẽ lực đẩy.') },
  { t: 'Dạng 2 · Trung bình · Vừa bung dù: lực cản lớn hơn trọng lực, tìm gia tốc',
    de: `Người nhảy dù cùng dù tổng ${m('75\\ \\mathrm{kg}')} đang rơi xuống. Ngay sau khi bung dù, lực cản không khí hướng lên, độ lớn ${nw(m('2250\\ \\mathrm N'))}. Bỏ qua lực đẩy Archimedes của không khí; ${g10}.<br><b>a)</b> trọng lượng ${P}<br><b>b)</b> độ lớn và hướng của hợp lực<br><b>c)</b> độ lớn gia tốc; người rơi nhanh dần hay chậm dần`,
    nd: `Hai lực ngược chiều ⇒ ${nw(`${m('F_{hl}=')} ${f(16)}`)}; gia tốc cùng hướng ${f(16)}; ngược chiều ${m('\\vec v')} ⇒ ${f(16)}`, a: ['a', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'], gi: 5, fig: H.bungDu('Hình không vẽ trọng lực.'), cot: 2 },
  { t: 'Dạng 3 · Khá · Lực kế khi nhúng vật vào chất lỏng: tìm khối lượng riêng chất lỏng',
    de: `Khối đồng đặc treo vào lực kế; ngoài không khí lực kế chỉ ${nw(m('8{,}9\\ \\mathrm N'))}. Nhúng chìm hoàn toàn vào một chất lỏng thì lực kế chỉ ${nw(m('8{,}1\\ \\mathrm N'))}. Khối lượng riêng của đồng ${nw(m('8900\\ \\mathrm{kg/m^3}'))}; ${g10}; bỏ qua lực đẩy của không khí.<br><b>a)</b> thể tích khối đồng<br><b>b)</b> lực đẩy Archimedes<br><b>c)</b> khối lượng riêng của chất lỏng; chất lỏng nặng hay nhẹ hơn nước (${rn})`,
    nd: `${nw(`${m('V=')} <span class="fill" style="min-width:16mm;height:9mm"></span>`)} (qua ${m('m=P/g')}); vật đứng yên ⇒ ${nw(`${m('T+F_A=')} ${f(12)}`)}; ${nw(`${m('\\rho=')} <span class="fill" style="min-width:16mm;height:9mm"></span>`)}`, a: ['a', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'], gi: 21, fig: H.dongLong('Hình không ghi khối lượng riêng chất lỏng.'), cot: 2 },
];

// Bài tương tự giải vào vở (thầy chốt 10/11): 1 cột, ô đáp số cuối đúng dòng ý; mỗi dạng 2 bài; đáp số Python 13/11/2026.
const oY = (s, o, w = 25) => s.split('<br>').map((p) => {
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
  tieuDe: ['DẠNG 1–2', 'DẠNG 3'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Viên bi sắt thể tích ${m('250\\ \\mathrm{cm^3}')} chìm hoàn toàn trong nước; ${rn}, ${g10}.<br><b>a)</b> thể tích viên bi theo ${m('\\mathrm{m^3}')}<br><b>b)</b> lực đẩy Archimedes`, o: ['a', 'b'], ow: { a: 30 } },
    { t: 'Dạng 1 · Bài 2', de: `Khúc gỗ thể tích ${m('3{,}0\\ \\mathrm{dm^3}')} nổi yên trên nước, phần chìm ${nw(`${m('1{,}8\\ \\mathrm{dm^3}')};`)} ${rn}, ${g10}.<br><b>a)</b> thể tích phần chìm theo ${m('\\mathrm{m^3}')}<br><b>b)</b> lực đẩy Archimedes<br><b>c)</b> trọng lượng khúc gỗ`, o: ['a', 'b', 'c'], ow: { a: 30 } },
    { t: 'Dạng 2 · Bài 1', de: `Vận động viên cùng dù tổng ${m('80\\ \\mathrm{kg}')} đang rơi; ngay sau khi bung dù, lực cản không khí hướng lên, độ lớn ${nw(`${m('2000\\ \\mathrm N')}.`)} Bỏ qua lực đẩy của không khí; ${g10}.<br><b>a)</b> trọng lượng<br><b>b)</b> độ lớn và hướng của hợp lực<br><b>c)</b> gia tốc; nhanh dần hay chậm dần`, fig: H.bungDu(''), fw: 34, o: ['a', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'], ow: { b: 34, 'c<sub>1</sub>': 18, 'c<sub>2</sub>': 22 } },
    { t: 'Dạng 2 · Bài 2', de: `Người cùng dù tổng ${m('90\\ \\mathrm{kg}')} rơi, chưa mở dù; lúc tốc độ còn nhỏ, lực cản không khí là ${nw(`${m('540\\ \\mathrm N')}.`)} Bỏ qua lực đẩy của không khí; ${g10}.<br><b>a)</b> độ lớn và hướng của hợp lực lúc đó<br><b>b)</b> độ lớn gia tốc lúc đó<br><b>c)</b> khi đạt tốc độ giới hạn, lực cản bằng bao nhiêu`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'], ow: { 'a<sub>2</sub>': 16 } },
    nhap(9),
  ], [
    { t: 'Dạng 3 · Bài 1', de: `Khối nhôm đặc treo vào lực kế, ngoài không khí lực kế chỉ ${nw(`${m('2{,}7\\ \\mathrm N')};`)} nhúng chìm hoàn toàn trong một chất lỏng, lực kế chỉ ${nw(`${m('1{,}9\\ \\mathrm N')}.`)} Nhôm ${nw(`${m('2700\\ \\mathrm{kg/m^3}')};`)} ${g10}; bỏ qua lực đẩy của không khí.<br><b>a)</b> thể tích khối nhôm<br><b>b)</b> lực đẩy Archimedes<br><b>c)</b> khối lượng riêng chất lỏng`, fig: H.dongLong('', '1,9 N'), fw: 34, o: ['a', 'b', 'c'], ow: { a: 30 } },
    { t: 'Dạng 3 · Bài 2 (đổi chiều)', de: `Một vật treo vào lực kế, ngoài không khí lực kế chỉ ${nw(`${m('6{,}0\\ \\mathrm N')};`)} nhúng chìm hoàn toàn trong nước lực kế chỉ ${nw(`${m('4{,}0\\ \\mathrm N')}.`)} ${rn}; ${g10}; bỏ qua lực đẩy của không khí.<br><b>a)</b> lực đẩy Archimedes<br><b>b)</b> thể tích vật<br><b>c)</b> khối lượng riêng của vật`, o: ['a', 'b', 'c'], ow: { b: 30 } },
    nhap(22),
  ]],
  dap: [
    `D1·1: a) 2,5·10<sup>−4</sup> m³ · b) 2,5 N &nbsp;|&nbsp; D1·2: a) 1,8·10<sup>−3</sup> m³ · b) 18 N · c) 18 N &nbsp;|&nbsp; D2·1: a) 800 N · b) 1200 N, hướng lên · c<sub>1</sub>) 15 m/s² · c<sub>2</sub>) chậm dần &nbsp;|&nbsp; D2·2: a<sub>1</sub>) 360 N · a<sub>2</sub>) hướng xuống · b) 4,0 m/s² · c) 900 N`,
    `D3·1: a) 1,0·10<sup>−4</sup> m³ · b) 0,80 N · c) 800 kg/m³ &nbsp;|&nbsp; D3·2: a) 2,0 N · b) 2,0·10<sup>−4</sup> m³ · c) 3000 kg/m³`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [2, 1], kq: [[1, 2], [3]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'lực cản 1·5 · phễu giấy 2·1 · ba giai đoạn 2·2 · Archimedes 3·1 · bình tràn 3·2 · chênh áp suất 3·3 · nổi, chìm 3·4 · bẫy 4·1 · bài toán mẫu 5·1 · dạng 1–2 → 6·1 · dạng 3 → 7·1',
  out: process.argv[2],
});
