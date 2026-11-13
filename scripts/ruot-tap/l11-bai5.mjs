// Ruột tập VL11 – Bài 5 · Động năng. Thế năng. Sự chuyển hoá năng lượng trong dao động điều hoà (lesson id 24).
// Quyển Chương 1 lớp 11 (Dao động): bài 1 = tr. 1–12 → bài 5 = tr. 49–60.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự giải vào vở · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l11-bai5.mjs (toàn bộ SVG tự vẽ). Nội dung theo bài web (book/cache/24.json, tải từ DB 13/11/2026):
// mục tiêu, dự đoán xích đu, II.1–II.6, thí nghiệm đo k rồi tính năm vạch, ba bẫy, Trả bài 6 câu, bài toán mẫu,
// điền bước, thử sức đổi biên độ, thử thách 3 mức, 5 dạng bài tập mẫu (D5 đọc đồ thị E_d(x)).
// Đáp số Bài tương tự (tuongTu.dap) tính bằng Python 13/11/2026.
// Chạy: node scripts/ruot-tap/l11-bai5.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl11-bai5.pdf
//       node scripts/ruot-tap/l11-bai5.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l11-bai5/
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL11b5 as H } from './hinh-l11-bai5.mjs';

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
  const out = resolve(HERE, 'out/hinh-l11-bai5'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 5, lid: 24, ten: 'ĐỘNG NĂNG · THẾ NĂNG TRONG DAO ĐỘNG ĐIỀU HOÀ', lop: 11, baiDau: 1, sub: 'Vật lí 11 · Chương 1: Dao động' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const Et = m('E_t'), Ed = m('E_d'), W = m('W');
const fr = (s) => m(`\\tfrac{1}{2}${s}`);

const ttHaiCot = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm}.yo .oo{flex:none;display:flex;gap:3mm}.yo{line-height:1.35}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';
const p1 = `${ttHaiCot}<section class="page">
${head('BÀI 5 · ĐỘNG NĂNG · THẾ NĂNG TRONG DAO ĐỘNG ĐIỀU HOÀ', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Viết ${Et}, ${Ed}, ${W}; chỉ đúng chỗ <b>cực đại</b>, <b>cực tiểu</b> của từng đại lượng`)}
${dong(`${ck}So <b>chu kì</b> và <b>pha</b> của ${Et}, ${Ed} với chu kì của li độ`)}
${dong(`${ck}Biết khi nào ${W} không đổi; ${W} của con lắc lò xo có phụ thuộc ${m('m')} không`)}
${dong(`${ck}Tìm li độ, tốc độ khi ${m('E_d=nE_t')}; đọc đồ thị năng lượng`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Năng lượng lúc đu dừng ở trên cao đã đi đâu?</p>
<div class="fig-side" style="${fs(44)}"><div>
${opt('A', 'Mất hẳn, vì vận tốc bằng không')}
${opt('B', 'Hoá nhiệt ngay, nên đu không tự quay xuống được')}
${opt('C', 'Thành thế năng; khi đu xuống thì trả lại thành động năng')}
${opt('D', 'Thành điện năng trong trụ của xích đu')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 1)}</div>
${H.xichDu()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Thế năng: mốc ở VTCB', '1·4')}
<div class="card" style="padding:1.2mm 3mm">
<div>Li độ ${m('x=A\\cos(\\omega t+\\varphi)')} tính từ vị trí cân bằng (VTCB); ${m('\\omega')}: tần số góc (rad/s), ${m('\\varphi')}: pha ban đầu (rad).</div>
<div>Mốc thế năng đặt tại ${f(25)}; ở đó ${m('x=0')} và ${m('E_t=')} ${f(12)}</div>
<div>${m('E_t=\\tfrac{1}{2}k')} ${f(14)} ${m('=\\tfrac{1}{2}m\\omega^2')} ${f(14)} &nbsp;· ${Et} chỉ phụ thuộc ${f(25)}</div>
<div>${Et} lớn nhất tại ${f(25)}: ${m('E_{t,\\max}=')} ${f(16)}</div></div>
${h3(5, 'II.2 · Động năng: lớn ở giữa', '1·5')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div>${m('E_d=\\tfrac{1}{2}m')} ${f(14)} &nbsp;(${m('v')}: vận tốc)</div>
<div>Theo li độ: ${m('E_d=\\tfrac{1}{2}k\\big(')} ${f(16)} ${m('\\big)')}</div>
<div>${Ed} lớn nhất tại ${f(25)}: ${m('E_{d,\\max}=\\tfrac{1}{2}m')} ${f(14)}, với ${m('v_{\\max}=\\omega A')}</div>
<div>${Ed} bằng 0 tại ${f(25)}, vì ở đó ${m('v=')} ${f(12)}</div>
<div>Vì ${m('k=m\\omega^2')} nên ${m('\\tfrac{1}{2}m\\omega^2A^2=\\tfrac{1}{2}k')} ${f(14)}</div></div>
${H.conLacTrang1()}</div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('HAI NĂNG LƯỢNG ĐỔI CHỖ · CƠ NĂNG')}
${h3(1, 'II.3 · Theo li độ: một tăng, cái kia giảm', '2·1')}
<div class="fig-side" style="${fs(48)}"><div><table>
<tr><th style="width:34mm"></th><th>${Et}</th><th>${Ed}</th></tr>
<tr><td>Lớn nhất ở</td><td></td><td></td></tr>
<tr><td>Bằng 0 ở</td><td></td><td></td></tr>
<tr><td>Đi từ VTCB ra biên</td><td>${ck}tăng ${ck}giảm</td><td>${ck}tăng ${ck}giảm</td></tr>
<tr><td>Đồ thị theo ${m('x')}</td><td>${ck}nét liền ${ck}nét đứt</td><td>${ck}nét liền ${ck}nét đứt</td></tr></table>
<div style="margin-top:1mm">Cắt nhau khi ${m('E_t=E_d')}, tức ${m('x^2=A^2-x^2')}: ${m('x=\\pm')} ${f(16)}</div></div>
${H.haiParabol()}</div>
${h3(2, 'Theo thời gian: năng lượng đổi nhanh gấp đôi', '2·2')}
<div class="card fig-side" style="${fs(48)};padding:1.2mm 3mm"><div>
<table><tr><th></th><th>Li độ ${m('x')}</th><th>${Et}, ${Ed}</th></tr>
<tr><td>Chu kì</td><td>${m('T')}</td><td></td></tr>
<tr><td>Tần số</td><td>${m('f')}</td><td></td></tr>
<tr><td>Tần số góc</td><td>${m('\\omega')}</td><td></td></tr></table>
<div style="margin-top:1mm">${Et} và ${Ed} dao động ${ck}cùng pha ${ck}ngược pha (lệch nhau ${m('\\pi')} rad): cái này cực đại thì cái kia ${f(25)}</div>
<div class="hint">Vì sao: ${m('\\cos^2\\alpha=\\tfrac{1+\\cos2\\alpha}{2}')}, ${m('\\sin^2\\alpha=\\tfrac{1-\\cos2\\alpha}{2}')}.</div></div>
${H.theoT()}</div>
${h3(3, 'II.4 · Cơ năng: tổng không đổi', '2·3')}
<div class="card" style="padding:1.2mm 3mm">
<div>Bỏ qua ma sát: ${m('W=E_t+E_d=\\tfrac{1}{2}k')} ${f(14)} ${m('=\\tfrac{1}{2}m\\omega^2')} ${f(14)} ${m('=E_{t,\\max}=E_{d,\\max}')}</div>
<div>Đồ thị ${m('W(t)')} là đường ${f(25)}; ${W} tỉ lệ với ${f(25)} của biên độ.</div>
<div>Con lắc lò xo: thay ${m('\\omega^2=k/m')} thì ${m('m')} bị triệt. Giữ ${m('k')}, ${m('A')}, đổi ${m('m')}: ${W} ${ck}đổi ${ck}không đổi; ${m('T')} ${ck}đổi ${ck}không đổi</div></div>
${h3(4, 'Làm nhanh', '2·4')}
${box(`<div style="padding-top:1mm"><b>Câu 1.</b> Con lắc lò xo dao động với chu kì ${nw(m('T=0{,}50\\ \\mathrm s'))}. Thế năng biến thiên với chu kì bao nhiêu? ${f(16)}</div>
<div style="padding-top:1mm"><b>Câu 2.</b> Biên độ tăng gấp đôi, giữ ${m('k')}: cơ năng tăng mấy lần? ${f(12)}</div>
<div style="padding-top:1mm"><b>Câu 3.</b> Giữ ${m('k')}, ${m('A')}, thay vật nặng gấp 4 lần: chu kì ${m('T')} đổi thế nào? Cơ năng đổi thế nào? Vì sao?</div>${lines(2)}`)}
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('NĂM CHỖ TRÊN MỘT CHU KÌ · CON LẮC LÒ XO · THÍ NGHIỆM')}
${h3(1, 'II.5 · Năm chỗ trên một chu kì', '3·1')}
<table><tr><th style="width:30mm">Chỗ</th><th>Li độ ${m('x')}</th><th>Tốc độ ${m('|v|')} theo ${m('v_{\\max}')}</th><th style="width:22mm">Số lần / chu kì</th></tr>
<tr><td>${m('E_d')} cực đại</td><td>${m('0')}</td><td>${m('v_{\\max}')}</td><td>2</td></tr>
<tr><td>${m('E_d=3E_t')}</td><td style="height:7mm"></td><td></td><td></td></tr>
<tr><td>${m('E_d=E_t')}</td><td style="height:7mm"></td><td></td><td></td></tr>
<tr><td>${m('E_d=E_t/3')}</td><td style="height:7mm"></td><td></td><td></td></tr>
<tr><td>${m('E_t')} cực đại</td><td style="height:7mm"></td><td></td><td></td></tr></table>
<div class="card soft" style="margin-top:1mm;padding:1mm 3mm">Tổng quát ${m('E_d=nE_t')} (${m('n\\gt 0')}): ${m('W=(n+1)E_t')} ${m('\\Rightarrow')} ${m('x=\\pm')} ${f(18)} &nbsp;· mỗi li độ ${m('\\pm x')} vật đi qua ${f(12)} lần mỗi chu kì (đi ra, quay về).</div>
${h3(2, 'II.6 · Con lắc lò xo nằm ngang', '3·2')}
<div class="card" style="padding:1.2mm 3mm">
<div>Lò xo nhẹ (coi như không có khối lượng), độ cứng ${m('k')}, vật ${m('m')}, bỏ ma sát:</div>
<div>${m('\\omega=')} ${f(16)} &nbsp; ${m('T=')} ${f(16)} &nbsp; ${m('f=')} ${f(16)}</div>
<div>Chỉ phụ thuộc ${f(25)}; không phụ thuộc ${f(25)} hay cách kích thích.</div></div>
${h3(3, 'Thí nghiệm: đo k, rồi tính năng lượng tại năm vạch', '3·3')}
<div class="card" style="padding:1.2mm 3mm">
<div><b>Làm:</b> treo quả ${nw(m('m=200\\ \\mathrm g'))}, đo độ dãn ${nw(m('\\Delta\\ell=4{,}9\\ \\mathrm{cm}'))}, lấy ${nw(m('g=9{,}8\\ \\mathrm{m/s^2}'))}: ${m('k=\\dfrac{mg}{\\Delta\\ell}=')} ${f(14)} N/m. Đặt lò xo nằm ngang, kéo tới ${nw(m('A=8{,}0\\ \\mathrm{cm}'))} rồi thả.</div></div>
<div class="fig-side" style="${fs(46)}"><table class="tbl-ct"><tr><th>Vạch ${m('x')}</th><th>${m('E_t')} (J)</th><th>${m('E_d')} (J)</th><th>${m('W')} (J)</th></tr>
<tr><td>${m('0')}</td><td></td><td></td><td></td></tr>
<tr><td>${m('A/2=4{,}0')} cm</td><td></td><td></td><td></td></tr>
<tr><td>${m('A/\\sqrt2\\approx5{,}66')} cm</td><td></td><td></td><td></td></tr>
<tr><td>${m('A\\sqrt3/2\\approx6{,}93')} cm</td><td></td><td></td><td></td></tr>
<tr><td>${m('A=8{,}0')} cm</td><td></td><td></td><td></td></tr></table>
${H.namVach()}</div>
<div class="card soft" style="margin-top:.8mm;padding:1mm 3mm">
<div>Tính ${m('E_t=\\tfrac{1}{2}kx^2')}, ${m('E_d=\\tfrac{1}{2}k(A^2-x^2)')} theo đúng ${m('A/\\sqrt2')}, ${m('A\\sqrt3/2')} (không theo số làm tròn).</div>
<div><b>Rút ra:</b> bỏ ma sát thì ${W} ${f(25)}; ${Et} và ${Ed} chỉ ${f(25)} cho nhau.</div>
${wl('Bảng này đã kiểm được định luật chưa? Muốn kiểm thật phải đo thêm gì?', 2)}</div>
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('BA CÁI BẪY · TRẢ BÀI · TỰ KIỂM TRA · MANG VỀ')}
${h3(1, 'III · Ba cái bẫy hay sập', '4·1')}
<div class="card" style="padding:1mm 3mm">
<div class="trap">${ck}<span><b>“${W} lên xuống theo thời gian, ${W} phụ thuộc ${m('m')}.”</b> ${Et} và ${Ed} đổi chỗ; ${W} nằm ngang. ${m('\\omega^2=k/m')} nên ${m('W=\\tfrac{1}{2}kA^2')}, không còn ${m('m')}.</span></div>
<div class="trap">${ck}<span><b>“${Et}, ${Ed} cùng chu kì với li độ.”</b> ${Et} lên đỉnh ở cả hai biên: năng lượng có chu kì ${m('T/2')}, tần số ${m('2f')}.</span></div>
<div class="trap">${ck}<span><b>“${m('E_d=E_t')} khi ${m('x=\\pm A/2')}.”</b> Bằng nhau thì chia căn hai: ${m('x=\\pm A/\\sqrt2')}. Tại ${m('x=\\pm A/2')}: ${m('E_t=W/4')}, ${m('E_d=3W/4')}.</span></div></div>
${h3(2, 'IV · Trả bài 6 câu', '4·2')}
${box(`${tb(`1. Mốc thế năng đặt ở đâu? Viết ${Et} theo ${m('x')} và theo ${m('t')}.`)}${lines(2)}
${tb(`2. ${Et} và ${Ed} cực đại, cực tiểu ở đâu? Giá trị cực đại?`)}${lines(2)}
${tb(`3. ${W} bằng gì? Con lắc lò xo có phụ thuộc ${m('m')} không?`)}${lines(2)}
${tb(`4. ${Et}, ${Ed} biến thiên với chu kì nào? Cùng pha hay ngược pha?`)}${lines(1)}
${tb(`5. Khi ${m('E_d=E_t')} và khi ${m('E_d=3E_t')}: ${m('x')}, ${m('|v|')} bằng bao nhiêu? Mấy lần mỗi chu kì?`)}${lines(2)}
${tb(`6. ${m('\\omega')}, ${m('T')}, ${m('f')} của con lắc lò xo? Có phụ thuộc ${m('A')} không?`)}${lines(2)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/6 câu · chưa thuộc: ${f(25)} ${nw(`${m('\\to')} đọc lại ô ${f(12)} Tập`)}</div>
${h3(3, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '4·3')}
${rkHai([1, 2, 3], [4, 5, 6])}
${h3(4, 'Mang về: điều em dễ quên nhất', '4·4')}
${box(wl('1.', 1) + wl('2.', 1) + wl('3.', 1))}
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TOÁN MẪU · THỬ THÁCH')}
${h3(1, 'V · Bài toán mẫu', '5·1')}
<div class="card soft fig-side" style="${fs(44)};padding:1.2mm 3mm"><div>Con lắc lò xo nằm ngang, ${nw(m('k=40\\ \\mathrm{N/m}'))}, vật ${nw(m('m=200\\ \\mathrm g'))}. Kéo vật lệch khỏi VTCB ${nw(m('8{,}0\\ \\mathrm{cm}'))} rồi thả nhẹ; bỏ qua ma sát.
<div><b>a)</b> cơ năng ${W}</div><div><b>b)</b> ${Et} và ${Ed} khi ${nw(m('x=4{,}0\\ \\mathrm{cm}'))}</div><div><b>c)</b> li độ khi động năng bằng thế năng</div></div>${H.mau()}</div>
<table><tr><th style="width:44mm">Câu trong đề</th><th>Dữ liệu ${m('\\to')} kiến thức</th></tr>
<tr><td>“nằm ngang, bỏ qua ma sát”</td><td>${W} không đổi; mốc ${Et} tại VTCB</td></tr>
<tr><td>“${m('m=200')} g … lệch ${m('8{,}0')} cm rồi thả nhẹ”</td><td style="height:6.5mm"></td></tr>
<tr><td>“khi ${m('x=4{,}0')} cm”</td><td style="height:6.5mm"></td></tr>
<tr><td>“động năng bằng thế năng”</td><td style="height:6.5mm"></td></tr></table>
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm;margin-top:1mm">
${wl('a)', 2)}${wl('b)', 3)}${wl('c)', 3)}</div>
${h3(2, 'Điền bước còn thiếu: cùng con lắc, A = 6,0 cm, hỏi tại x = 3,0 cm', '5·2')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div class="ln"><b>Bước 1 (cho sẵn):</b> ${m('A=0{,}060\\ \\mathrm m')}, ${m('x=0{,}030\\ \\mathrm m')}</div>
${wl(`Bước 2: ${m('W=\\tfrac{1}{2}kA^2=')}`, 1)}${wl(`Bước 3: ${m('E_t=')} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ${m('E_d=W-E_t=')}`, 1)}${wl(`Kiểm tra: ${m('E_d/E_t=')} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; vì ${m('x=')}`, 1)}</div>
${h3(3, 'Thử thách phân tầng', '5·3')}
<div class="fig-side" style="${fs(44)}">${box(wl(`${m('\\bigstar')} ${Et} cực đại ở đâu? Bằng bao nhiêu? Lúc đó ${m('v=')}?`, 2)
 + wl(`${m('\\bigstar\\bigstar')} ${nw(m('A=8{,}0\\ \\mathrm{cm}'))}, ${m('E_d=3E_t')} thì ${m('|x|=')}? Mấy lần mỗi chu kì?`, 2)
 + wl(`${m('\\bigstar\\bigstar\\bigstar')} Biên độ giảm từ 8,0 cm còn 6,0 cm (giữ ${m('k')}, ${m('m')}): ${m('v_{\\max}')} mới bằng ${m('v_{\\max}')} cũ nhân mấy? ${W} mới?`, 3))}${H.doiA()}</div>
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Cơ năng, thế năng, động năng và tốc độ tại một li độ',
    de: `Con lắc lò xo nằm ngang, bỏ qua ma sát, ${m('k=50\\ \\mathrm{N/m}')}, ${m('m=500\\ \\mathrm g')}; kéo vật lệch ${m('10\\ \\mathrm{cm}')} rồi thả nhẹ.<br><b>a)</b> cơ năng ${W}<br><b>b)</b> tại ${m('x=6{,}0\\ \\mathrm{cm}')}: thế năng ${m('(b_1)')} và động năng ${m('(b_2)')}<br><b>c)</b> tốc độ của vật ở li độ đó`,
    nd: `thả nhẹ ${m('\\Rightarrow')} ${m('A=')} ${f(16)}; ${m('E_d=W-')} ${f(12)}; đổi g ${m('\\to')} kg, cm ${m('\\to')} m`, a: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], gi: 3 },
  { t: 'Dạng 2 · Trung bình · Động năng bằng n lần thế năng',
    de: `Con lắc lò xo nằm ngang, bỏ qua ma sát, ${m('m=250\\ \\mathrm g')}, ${m('k=25\\ \\mathrm{N/m}')}, ${m('A=12\\ \\mathrm{cm}')}. Lúc động năng gấp 8 lần thế năng:<br><b>a)</b> độ lớn li độ<br><b>b)</b> tốc độ<br><b>c)</b> trong một chu kì có mấy lần như vậy`,
    nd: `${m('E_d=8E_t')} ${m('\\Rightarrow')} ${m('W=')} ${f(14)} ${m('E_t')}; không phải trường hợp ${m('x=\\pm A/\\sqrt2')}`, a: ['a', 'b', 'c'], gi: 3, fig: H.d2() },
  { t: 'Dạng 3 · Trung bình · Biết li độ và tốc độ cùng lúc: tìm W, A',
    de: `Con lắc lò xo nằm ngang, bỏ qua ma sát, ${m('m=250\\ \\mathrm g')}, ${m('k=25\\ \\mathrm{N/m}')}. Khi vật ở ${m('x=3{,}0\\ \\mathrm{cm}')} thì tốc độ ${m('40\\ \\mathrm{cm/s}')}.<br><b>a)</b> cơ năng<br><b>b)</b> biên độ<br><b>c)</b> tốc độ cực đại`,
    nd: `chưa biết ${m('A')} ${m('\\Rightarrow')} ${m('W=\\tfrac{1}{2}kx^2+')} ${f(16)}; rồi ${m('A')} từ ${m('W=\\tfrac{1}{2}kA^2')}`, a: ['a', 'b', 'c'], gi: 3 },
  { t: 'Dạng 4 · Khó · Chu kì của năng lượng; động năng theo thời gian',
    de: `Con lắc lò xo nằm ngang, ${m('m=100\\ \\mathrm g')}, ${m('k=40\\ \\mathrm{N/m}')}. Kéo vật tới ${m('A=5{,}0\\ \\mathrm{cm}')} rồi thả nhẹ lúc ${m('t=0')}; bỏ qua ma sát; lấy ${m('\\pi=3{,}14')}.<br><b>a)</b> chu kì dao động ${m('T')}<br><b>b)</b> chu kì ${m("T'")} của thế năng, động năng<br><b>c)</b> thời gian ngắn nhất giữa hai lần liên tiếp ${m('E_d=E_t')}<br><b>d)</b> động năng tại ${m('t=T/6')}`,
    nd: `thả từ biên: ${m('x=A\\cos\\omega t')} ${m('\\Rightarrow')} ${m('E_d=W\\sin^2')} ${f(14)}; ${m("T'=")} ${f(12)}`, a: ['a', 'b', 'c', 'd'], gi: 5, fig: H.d4() },
  { t: 'Dạng 5 · Khó · Đọc đồ thị động năng theo li độ',
    de: `Con lắc lò xo nằm ngang, ${m('m=500\\ \\mathrm g')}, bỏ qua ma sát. Đồ thị bên là động năng ${Ed} (J) theo li độ ${m('x')} (cm).<br><b>a)</b> cơ năng ${m('(a_1)')} và biên độ ${m('(a_2)')}<br><b>b)</b> độ cứng ${m('k')}<br><b>c)</b> tốc độ cực đại<br><b>d)</b> li độ khi động năng bằng ${m('0{,}030\\ \\mathrm J')}`,
    nd: `đỉnh đồ thị (${m('x=0')}): ${m('E_{d,\\max}=')} ${f(12)}; ${m('E_d=0')} tại ${m('x=\\pm')} ${f(12)}`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c', 'd'], gi: 5, fig: H.d5(), cot: 3 },
];

// Bài tương tự giải vào vở (thầy chốt 10/11): 1 cột; ô đáp số 25 mm đặt cuối đúng dòng của ý; nhãn khớp a) b) c)…
// Đáp số tính bằng Python 13/11/2026 (π = 3,14 ở Dạng 4 theo đề).
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
  tieuDe: ['DẠNG 1–3', 'DẠNG 4–5'],
  trang: [[
    { t: 'Dạng 1 · Bài 1 <span class="hint" style="font-weight:400">(mọi bài: con lắc lò xo nằm ngang, bỏ qua ma sát)</span>', de: `${m('k=80\\ \\mathrm{N/m}')}, ${m('m=200\\ \\mathrm g')}, biên độ ${m('5{,}0\\ \\mathrm{cm}')}. Xét lúc ${m('x=3{,}0\\ \\mathrm{cm}')}.<br><b>a)</b> cơ năng<br><b>b)</b> thế năng ${m('(b_1)')} và động năng ${m('(b_2)')} lúc đó<br><b>c)</b> tốc độ lúc đó`, o: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'] },
    { t: 'Dạng 1 · Bài 2', de: `${m('k=100\\ \\mathrm{N/m}')}, ${m('m=1{,}0\\ \\mathrm{kg}')}, kéo vật lệch ${m('4{,}0\\ \\mathrm{cm}')} rồi thả nhẹ. Xét lúc ${m('x=-2{,}0\\ \\mathrm{cm}')}.<br><b>a)</b> cơ năng<br><b>b)</b> thế năng ${m('(b_1)')} và động năng ${m('(b_2)')} lúc đó<br><b>c)</b> tốc độ lúc đó`, o: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'] },
    { t: 'Dạng 2 · Bài 1', de: `${m('k=100\\ \\mathrm{N/m}')}, ${m('m=400\\ \\mathrm g')}, ${m('A=10\\ \\mathrm{cm}')}. Lúc động năng gấp 3 lần thế năng:<br><b>a)</b> độ lớn li độ<br><b>b)</b> tốc độ<br><b>c)</b> trong một chu kì có mấy lần như vậy`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 2 · Bài 2', de: `${m('k=40\\ \\mathrm{N/m}')}, ${m('m=100\\ \\mathrm g')}, ${m('A=8{,}0\\ \\mathrm{cm}')}. Lúc <b>thế năng</b> gấp 3 lần động năng:<br><b>a)</b> độ lớn li độ<br><b>b)</b> tốc độ<br><b>c)</b> trong một chu kì có mấy lần như vậy`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 3 · Bài 1', de: `${m('m=200\\ \\mathrm g')}, ${m('k=20\\ \\mathrm{N/m}')}. Khi ${m('x=4{,}0\\ \\mathrm{cm}')} thì tốc độ ${m('30\\ \\mathrm{cm/s}')}.<br><b>a)</b> cơ năng<br><b>b)</b> biên độ<br><b>c)</b> tốc độ cực đại`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 3 · Bài 2', de: `${m('m=400\\ \\mathrm g')}, ${m('k=40\\ \\mathrm{N/m}')}. Khi ${m('x=-6{,}0\\ \\mathrm{cm}')} thì tốc độ ${m('80\\ \\mathrm{cm/s}')}.<br><b>a)</b> cơ năng<br><b>b)</b> biên độ<br><b>c)</b> tốc độ cực đại`, o: ['a', 'b', 'c'] },
    nhap(3),
  ], [
    { t: 'Dạng 4 · Bài 1', de: `${m('m=400\\ \\mathrm g')}, ${m('k=100\\ \\mathrm{N/m}')}, kéo tới ${m('A=4{,}0\\ \\mathrm{cm}')} rồi thả nhẹ lúc ${m('t=0')}; ${m('\\pi=3{,}14')}.<br><b>a)</b> chu kì ${m('T')}<br><b>b)</b> chu kì ${m("T'")} của thế năng<br><b>c)</b> thời gian ngắn nhất giữa hai lần liên tiếp ${m('E_d=E_t')}<br><b>d)</b> động năng tại ${m('t=T/12')}`, o: ['a', 'b', 'c', 'd'] },
    { t: 'Dạng 4 · Bài 2', de: `${m('m=400\\ \\mathrm g')}, ${m('k=160\\ \\mathrm{N/m}')}, kéo tới ${m('A=5{,}0\\ \\mathrm{cm}')} rồi thả nhẹ lúc ${m('t=0')}; ${m('\\pi=3{,}14')}.<br><b>a)</b> tần số dao động ${m('f')}<br><b>b)</b> tần số biến thiên của động năng<br><b>c)</b> động năng tại ${m('t=T/8')}<br><b>d)</b> thời gian ngắn nhất từ lúc thả tới lúc ${m('E_d=3E_t')}`, o: ['a', 'b', 'c', 'd'] },
    { t: 'Dạng 5 · Bài 1', de: `${m('m=200\\ \\mathrm g')}. Đồ thị bên: động năng ${Ed} (J) theo ${m('x')} (cm).<br><b>a)</b> cơ năng ${m('(a_1)')}, biên độ ${m('(a_2)')}<br><b>b)</b> độ cứng ${m('k')}<br><b>c)</b> tốc độ cực đại<br><b>d)</b> li độ khi ${m('E_d=0{,}050\\ \\mathrm J')}`, fig: H.t5a(), fw: 46, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c', 'd'], ow: 18 },
    { t: 'Dạng 5 · Bài 2', de: `${m('m=500\\ \\mathrm g')}. Đồ thị bên: <b>thế năng</b> ${Et} (J) theo ${m('x')} (cm).<br><b>a)</b> cơ năng ${m('(a_1)')}, biên độ ${m('(a_2)')}<br><b>b)</b> độ cứng ${m('k')}<br><b>c)</b> tốc độ cực đại<br><b>d)</b> động năng tại ${m('x=3{,}0\\ \\mathrm{cm}')}`, fig: H.t5b(), fw: 46, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c', 'd'], ow: 18 },
    nhap(4),
  ]],
  dap: [
    `D1·1: a) 0,10 J · b<sub>1</sub>) 0,036 J · b<sub>2</sub>) 0,064 J · c) 0,80 m/s &nbsp;|&nbsp; D1·2: a) 0,080 J · b<sub>1</sub>) 0,020 J · b<sub>2</sub>) 0,060 J · c) 0,35 m/s &nbsp;|&nbsp; D2·1: a) 5,0 cm · b) 1,37 m/s · c) 4 lần &nbsp;|&nbsp; D2·2: a) 6,93 cm · b) 0,80 m/s · c) 4 lần &nbsp;|&nbsp; D3·1: a) 0,025 J · b) 5,0 cm · c) 0,50 m/s &nbsp;|&nbsp; D3·2: a) 0,20 J · b) 10 cm · c) 1,0 m/s`,
    `D4·1: a) 0,397 s · b) 0,199 s · c) 0,0993 s · d) 0,020 J &nbsp;|&nbsp; D4·2: a) 3,18 Hz · b) 6,37 Hz · c) 0,10 J · d) 0,0523 s &nbsp;|&nbsp; D5·1: a<sub>1</sub>) 0,090 J · a<sub>2</sub>) 6,0 cm · b) 50 N/m · c) 0,95 m/s · d) ±4,0 cm &nbsp;|&nbsp; D5·2: a<sub>1</sub>) 0,125 J · a<sub>2</sub>) 5,0 cm · b) 100 N/m · c) 0,71 m/s · d) 0,080 J`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 2], kq: [[1, 2, 3], [4, 5]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'E<sub>t</sub> 1·4 · E<sub>d</sub> 1·5 · theo x 2·1 · theo t 2·2 · W 2·3 · năm chỗ 3·1 · chu kì 3·2 · bẫy 4·1 · bài mẫu 5·1 · D1–3 6·1 · D4–5 7·1',
  out: process.argv[2],
});
