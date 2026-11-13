// Ruột tập VL11 – Bài 7 · Bài tập về sự chuyển hoá năng lượng trong dao động điều hoà (lesson id 26).
// Quyển Chương 1 Dao động lớp 11: bài 1 = tr. 1–12 … bài 7 = tr. 73–84.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l11-bai7.mjs (toàn bộ SVG tự vẽ; đồ thị đọc được số cho dạng 3, 5 và bài tương tự của chúng).
// Nội dung theo bài web (book/cache/26.json, tải từ DB 13/11/2026): mục tiêu, dự đoán xích đu, bốn họ bài tập, thí nghiệm đo
// W theo A, ví dụ xích đu, ba bẫy, Trả bài 6 câu, bài toán mẫu lò xo 100 g – 100 N/m, thử thách, 5 dạng bài tập mẫu.
// Đáp số Bài tương tự (tuongTu.dap) tính bằng Python 13/11/2026.
// Chạy: node scripts/ruot-tap/l11-bai7.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl11-bai7.pdf
//       node scripts/ruot-tap/l11-bai7.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l11-bai7/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL11b7 as H } from './hinh-l11-bai7.mjs';

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
  const out = resolve(HERE, 'out/hinh-l11-bai7'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 7, lid: 26, ten: 'BÀI TẬP VỀ SỰ CHUYỂN HOÁ NĂNG LƯỢNG TRONG DAO ĐỘNG ĐIỀU HOÀ', lop: 11, baiDau: 1, sub: 'Vật lí 11 · Chương 1: Dao động' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const W = m('W'), Wt = m('W_t'), Wd = m('W_{\\text{đ}}'), A = m('A'), x = m('x'), a0 = m('\\alpha_0'), al = m('\\alpha');
const vmax = m('v_{\\max}');
const g10 = nw(m('g=10\\ \\mathrm{m/s^2}')), g98 = nw(m('g=9{,}8\\ \\mathrm{m/s^2}')), pi10 = nw(m('\\pi^2=10'));
const u = (v, d) => nw(m(`${v}\\ \\mathrm{${d}}`));
// phân số cao: ô điền cạnh căn/phân số phải cao ≥ 9 mm (checklist HS ảo)
const fc = (w = 16) => `<span class="fill" style="min-width:${w}mm;height:9mm;vertical-align:-3mm"></span>`;

// Bài tương tự 1 cột, ô đáp số cuối dòng của ý (giống l10-bai23); chữ "đ" trong KaTeX \text lấy font của trang (không rơi về Times).
const ttHaiCot = '<style>.katex .text{font-family:BV,KaTeX_Main}.bt>.gi{display:grid;grid-template-columns:1fr 1fr;column-gap:4mm}.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm}.yo .oo{flex:none;display:flex;gap:3mm}.yo{line-height:1.35}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';

const p1 = `${ttHaiCot}<section class="page">
${head('BÀI 7 · NĂNG LƯỢNG TRONG DAO ĐỘNG ĐIỀU HOÀ: BÀI TẬP', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft" style="display:grid;grid-template-columns:1fr 1fr;column-gap:3mm;padding:1mm 3mm">
${dong(`${ck}Nhìn đề, gọi đúng một trong <b>4 họ</b> bài tập`)}
${dong(`${ck}Đọc <b>đồ thị năng lượng</b> theo ${x}, theo ${m('t')}`)}
${dong(`${ck}Tính ${W}, ${Wd}, ${Wt} tại li độ ${x}; tìm chỗ ${nw(m('W_{\\text{đ}}=nW_t'))}`)}
${dong(`${ck}Giải <b>con lắc đơn</b> bằng bảo toàn cơ năng`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<div class="fig-side" style="${fs(44)}"><div>
<p style="margin:0 0 1mm">Góc lệch lớn nhất của xích đu tăng từ ${m('5^\\circ')} lên ${m('10^\\circ')} (vẫn là góc nhỏ). Cơ năng của xích đu thay đổi thế nào?</p>
${opt('A', 'Tăng gấp đôi, đúng như góc')}
${opt('B', 'Tăng khoảng 4 lần')}
${opt('C', 'Không đổi, vẫn là xích đu đó')}
${opt('D', 'Tăng khoảng 1,4 lần')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 2)}</div>
${H.xichDu()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f(12)} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II · Bốn họ bài tập năng lượng', '1·4')}
<div style="margin-bottom:.8mm">Mốc thế năng luôn ở vị trí cân bằng (VTCB). Bài 5 ghi ${m('E_d')}, ${m('E_t')}; đề hay ghi ${Wd}, ${Wt}: cùng nghĩa.</div>
<table><tr><td>“tại li độ ${x}”, “khi vật cách VTCB…”</td><td style="width:19mm">Họ ${f(10)}</td><td>“động năng gấp ${m('n')} lần thế năng”</td><td style="width:19mm">Họ ${f(10)}</td></tr>
<tr><td>“đồ thị”, “tần số của động năng”</td><td>Họ ${f(10)}</td><td>“dây treo”, “góc lệch ${al}”</td><td>Họ ${f(10)}</td></tr></table>
${h3(5, 'Họ 1 · Tính W, W<sub>đ</sub>, W<sub>t</sub> tại li độ x', '1·5')}
<div class="card fig-side" style="${fs(42)};padding:1.2mm 3mm"><div>
<div>Cơ năng: ${m('W=\\tfrac12 k')}${f(12)} ${m('=\\tfrac12 m')}${f(14)} (không đổi)</div>
<div>Thế năng: ${m('W_t=')} ${f(16)} &nbsp;(dùng ${ck}${x} &nbsp;${ck}${A})</div>
<div>Động năng: ${m('W_{\\text{đ}}=W-')}${f(12)} ${m('=\\tfrac12 k\\,(')}${f(16)}${m(')')}</div>
<div>Tốc độ: ${m('|v|=\\omega')}${f(18)}; ${m('v_{\\max}=')} ${f(12)} ở ${f(12)}</div>
<div style="margin-top:.6mm"><b>Ví dụ:</b> ${nw(m('k=40\\ \\mathrm{N/m}'))}, ${u('A=10', 'cm')}, ${nw(`${m('x=6\\ \\mathrm{cm}')}:`)}</div>
<div>${m('W=')} ${f(12)}&nbsp;J · ${m('W_t=')} ${f(12)}&nbsp;J · ${m('W_{\\text{đ}}=')} ${f(12)}&nbsp;J</div>
<div><b>Bẫy:</b> thế ${A} vào chỗ ${x} thì ${m('W_t=')} ${f(12)}, ${m('W_{\\text{đ}}=')} ${f(12)}</div></div>
${H.loXo()}</div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('THÍ NGHIỆM ĐO · HỌ 2 · ĐỒ THỊ THEO LI ĐỘ')}
${h3(1, 'Thí nghiệm đo: cơ năng theo biên độ', '2·1')}
<div class="card" style="padding:1.2mm 3mm">
<div><b>Làm:</b> treo vật ${u('m=250', 'g')}, lò xo dãn thêm ${u('5{,}0', 'cm')}, ${g98} ⇒ ${m('k=\\dfrac{mg}{\\Delta\\ell}=')} ${f(12)}&nbsp;N/m. Kéo xuống ${A} (nhỏ hơn ${u('5', 'cm')}; thước ${u('\\pm1', 'mm')}) rồi thả; điện thoại quay 240 hình/giây đo tốc độ lúc qua VTCB.</div>
<table style="margin-top:.8mm"><tr><th style="width:36mm">${m('A\\ (\\mathrm{cm})')}</th><th>1</th><th>1,5</th><th>2</th><th>3</th><th>4</th></tr>
<tr><td>${m('v_{\\max}')} đo (cm/s)</td><td>13,5</td><td>20,5</td><td>27,5</td><td>41,5</td><td>55,0</td></tr>
<tr><td>${m('\\tfrac12 mv_{\\max}^2\\ (\\mathrm{mJ})')}</td><td>2,3</td><td>5,3</td><td>9,5</td><td>21,5</td><td>37,8</td></tr>
<tr><td style="height:7mm">${m('W/A^2\\ (\\mathrm{mJ/cm^2})')}</td><td></td><td></td><td></td><td></td><td></td></tr></table>
<div style="margin-top:.6mm"><b>Rút ra:</b> hàng cuối gần như ${f(25)} ⇒ ${W} tỉ lệ với ${f(14)}. Mô hình: ${m('\\tfrac12 k=')} ${f(12)}&nbsp;J/m² = ${f(12)}&nbsp;mJ/cm² ${nw(`(${m('1\\ \\mathrm{J/m^2}=0{,}1\\ \\mathrm{mJ/cm^2}')})`)}</div>
${wl('Hàng nào kém tin cậy nhất? Vì sao số đo luôn thấp hơn mô hình?', 3)}</div>
${h3(2, 'Họ 2 · Vị trí W<sub>đ</sub> = nW<sub>t</sub>', '2·2')}
<div class="card fig-side" style="${fs(44)};padding:1.2mm 3mm"><div>
<div>${m('W_{\\text{đ}}=nW_t')} ⇒ ${m('W=')} ${f(12)}${m('\\,W_t')} ⇒ ${m('x=\\pm')}${fc()}</div>
<div>${m('W_{\\text{đ}}=')}${fc(12)}${m('\\,W')} ⇒ ${m('|v|=v_{\\max}\\cdot')}${fc()}</div>
<div>Đảo lại, ${m('W_t=nW_{\\text{đ}}')}: ${m('x=\\pm')}${fc()} ; ${m('|v|=')}${fc()}</div>
<div><b>Ví dụ:</b> ${u('A=8', 'cm')}, ${m('W_{\\text{đ}}=15W_t')}: ${m('x=\\pm')} ${f(12)}&nbsp;cm</div>
<div><b>Bẫy:</b> chia cho ${m('n')} thay vì ${m('n+1')}, hoặc quên lấy căn.</div></div>
${H.phanN()}</div>
${h3(3, 'Họ 3 · Đồ thị theo li độ x', '2·3')}
<div class="card fig-side" style="${fs(44)};padding:1.2mm 3mm"><div>
<div>${Wt}: parabol ${ck}đáy ${ck}úp ở VTCB · ${Wd}: parabol ${ck}đáy ${ck}úp · ${W}: đường ${f(20)}</div>
<div>${m('W_{\\text{đ}}=W_t')} tại ${m('x=\\pm')}${fc(14)} ${m('\\approx\\pm')} ${f(12)}${m('\\,A')}</div>
<div><b>Ví dụ:</b> đồ thị ${Wd} theo ${x} có đỉnh ${u('40', 'mJ')} tại ${m('x=0')}, chạm trục tại ${nw(`${m('\\pm5\\ \\mathrm{cm}')}:`)}</div>
<div>${m('W=')} ${f(12)}&nbsp;J · ${m('A=')} ${f(12)}&nbsp;m · ${m('k=\\dfrac{2W}{A^2}=')} ${f(12)}&nbsp;N/m</div></div>
${H.doThiXLT()}</div>
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('ĐỒ THỊ THEO THỜI GIAN · CON LẮC ĐƠN · BA BẪY')}
${h3(1, 'Họ 3 · Đồ thị theo thời gian t', '3·1')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div>${Wt}, ${Wd} lên xuống quanh ${f(12)}, <b>ngược pha</b> (cái này cực đại thì cái kia ${f(16)})</div>
<div>Chu kì của ${Wd}, ${Wt}: ${m("T'=")} ${f(12)} · tần số ${m("f'=")} ${f(12)}</div>
<div>Li độ ${x} có chu kì ${f(12)}; ${W} theo ${m('t')} là đường ${f(16)}</div>
<div>Hai đỉnh ${Wt} liền nhau cách ${f(12)}</div>
<div>${m('W_{\\text{đ}}=W_t')}: ${f(10)} lần mỗi chu kì; hai lần liền nhau cách ${f(12)}</div></div>
${H.doThiTLT()}</div>
${h3(2, 'Họ 4 · Con lắc đơn', '3·2')}
<div class="card fig-side" style="${fs(42)};padding:1.2mm 3mm"><div>
<div>Độ cao so với đáy: ${m('h=l\\,(')}${f(16)}${m(')')}</div>
<div>Cơ năng: ${m('W=mgl\\,(')}${f(16)}${m(')')}, ${a0} là ${f(20)}</div>
<div>Ở góc ${al}: ${m('v=\\sqrt{2gl\\,(\\qquad\\qquad\\qquad)}')}</div>
<div>Qua đáy: ${m('v_{\\max}=')} ${fc(26)}</div>
<div>Góc nhỏ (khoảng ${m('10^\\circ')} trở xuống), ${a0} tính bằng ${f(12)}:</div>
<div>${m('W\\approx')} ${fc(18)} &nbsp; ${m('v_{\\max}\\approx')} ${fc(14)}</div>
<div><b>Bẫy:</b> viết ${m('\\cos\\alpha_0')} thay cho ${f(16)}</div></div>
${H.conLac()}</div>
${h3(3, 'Ví dụ: xích đu ở sân trường', '3·3')}
<div class="card soft" style="padding:1mm 3mm">Dây dài ${u('2{,}0', 'm')}, bạn ngồi ${u('40', 'kg')}, góc lệch lớn nhất ${m('30^\\circ')} ${nw(`(${m('\\cos30^\\circ\\approx0{,}866')})`)}, ${g98}, bỏ ma sát.
<div>${m('h=')} ${f(14)}&nbsp;m · ${m('W=mgh=')} ${f(14)}&nbsp;J · qua đáy ${m('v=\\sqrt{2gh}=')} ${f(14)}&nbsp;m/s</div></div>
${h3(4, 'III · Ba cái bẫy mất điểm', '3·4')}
<div class="card fig-side" style="${fs(34)};padding:1mm 3mm"><div>
<div class="trap">${ck}<span><b>cm, mJ và bình phương.</b> ${nw(m('k=200\\ \\mathrm{N/m}'))}, ${u('A=2', 'cm')}: ${m('W=')} ${f(12)}&nbsp;J = ${f(12)}&nbsp;mJ. Để nguyên cm thì kết quả lớn gấp ${f(12)} lần. ${m('0{,}0125\\ \\mathrm J=')} ${f(12)}&nbsp;mJ</span></div>
<div class="trap">${ck}<span><b>Chu kì năng lượng ${m('\\neq')} chu kì dao động.</b> Đồ thị ${Wt} lặp lại sau ${u('0{,}25', 's')} ⇒ ${m('T=')} ${f(12)}&nbsp;s</span></div>
<div class="trap">${ck}<span><b>Góc nhỏ phải đổi ra rad:</b> ${m('\\alpha(\\mathrm{rad})=\\alpha(^\\circ)\\cdot\\dfrac{\\pi}{180}')}; ${m('6^\\circ=')} ${f(14)}&nbsp;rad. Công thức có ${m('\\cos')}: máy để chế độ ${f(14)}</span></div></div>
${H.radian()}</div>
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('TỰ KIỂM TRA · BÀI TOÁN MẪU')}
${h3(1, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '4·1')}
${rkHai([1, 2, 3, 4], [5, 6, 7])}
${h3(2, 'V · Bài toán mẫu: lò xo nằm ngang', '4·2')}
<div class="card soft fig-side" style="${fs(44)};padding:1.2mm 3mm"><div>Con lắc lò xo nằm ngang: vật ${u('100', 'g')}, lò xo ${nw(m('100\\ \\mathrm{N/m}'))}. Kéo vật khỏi VTCB ${u('4', 'cm')} rồi thả nhẹ. Bỏ qua ma sát, lấy ${pi10}.
<div><b>a)</b> Tính cơ năng.</div><div><b>b)</b> Tìm li độ tại đó động năng bằng 3 lần thế năng, và tốc độ khi đó.</div><div><b>c)</b> Động năng biến thiên với tần số bao nhiêu?</div></div>
${H.loXoMau()}</div>
${h3(3, 'Phân tích đề')}
<table><tr><th style="width:52mm">Câu trong đề</th><th>Dữ liệu → kiến thức</th></tr>
<tr><td>“khối lượng 100 g”</td><td>${m('m=0{,}1\\ \\mathrm{kg}')} (đổi ra kg)</td></tr>
<tr><td style="height:6.5mm">“độ cứng 100 N/m”, “${m('\\pi^2=10')}”</td><td></td></tr>
<tr><td style="height:6.5mm">“kéo 4 cm rồi thả nhẹ”</td><td></td></tr>
<tr><td style="height:6.5mm">“động năng bằng 3 lần thế năng”</td><td></td></tr>
<tr><td style="height:6.5mm">“tần số … động năng”</td><td></td></tr></table>
${h3(4, 'Giải')}
<div class="two" style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm"><div>
${wl(`${m('\\omega')}, ${m('f')}:`, 3)}${wl('a) Cơ năng:', 3)}${wl('c) Tần số động năng:', 1)}</div><div>${wl(`b) ${x}, ${m('|v|')}:`, 4)}${wl(`Kiểm: ${m('W_t+W_{\\text{đ}}=W')}? ${m('|v|\\lt v_{\\max}')}?`, 3)}</div></div>
${h3(5, 'Điền bước còn thiếu: cùng đề, động năng bằng 8 lần thế năng', '4·5')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div class="ln"><b>Bước 1 (cho sẵn):</b> ${m('W=80\\ \\mathrm{mJ}')} như trên.</div>
${wl(`Bước 2: tổng mấy phần? ${m('x=')}`, 1)}${wl(`Bước 3: ${m('|v|=')}`, 1)}</div>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TẬP VỀ NHÀ · TRẢ BÀI · THỬ THÁCH')}
${K.btvn()}
${h3(2, 'IV · Trả bài 6 câu', '5·2')}
${box(`${tb('1. Cơ năng con lắc lò xo? Đơn vị nào phải đổi trước?')}${lines(1)}
${tb('2. Thế năng, động năng tại li độ x?')}${lines(1)}
${tb('3. W<sub>đ</sub> = nW<sub>t</sub> thì li độ và tốc độ bằng bao nhiêu?')}${lines(1)}
${tb('4. Đồ thị năng lượng theo x, theo t có dạng gì? Chu kì?')}${lines(2)}
${tb(`5. Con lắc đơn: cơ năng và tốc độ ở góc ${m('\\alpha')}?`)}${lines(1)}
${tb(`6. Khi nào dùng ${m('W\\approx\\tfrac12 mgl\\alpha_0^2')}? Góc tính bằng gì?`)}${lines(1)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/6 câu · chưa thuộc: ${f(25)} ${nw(`→ đọc lại ô ${f(12)} Tập`)}</div>
${h3(3, 'Thử thách phân tầng', '5·3')}
<div class="fig-side" style="${fs(40)}">${box(wl(`${m('\\bigstar')} Lò xo ${nw(m('k=20\\ \\mathrm{N/m}'))}, biên độ ${u('10', 'cm')}. Cơ năng?`, 1)
 + wl(`${m('\\bigstar\\bigstar')} Con lắc đơn ${u('l=1{,}0', 'm')}, thả từ ${m('60^\\circ')}, ${g98}. Tốc độ khi dây lệch ${nw(`${m('30^\\circ')}?`)}`, 2)
 + wl(`${m('\\bigstar\\bigstar\\bigstar')} Thế năng của con lắc lò xo ${u('m=100', 'g')} biến thiên với tần số ${u('6', 'Hz')}. Tìm ${m('k')} ${nw(`(${m('\\pi^2=10')}).`)}`, 2))}${H.conLacTT()}</div>
${h3(4, 'VI · Mang về: điều em dễ quên nhất', '5·4')}
${box(wl('1.', 1) + wl('2.', 1) + wl('3.', 1))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · W, W<sub>đ</sub>, W<sub>t</sub> và tốc độ tại li độ x',
    de: `Lò xo nằm ngang: vật ${u('400', 'g')}, ${nw(m('k=40\\ \\mathrm{N/m}'))}. Kéo vật khỏi VTCB ${u('15', 'cm')} rồi thả nhẹ, bỏ qua ma sát. Xét lúc ${nw(m('x=-9\\ \\mathrm{cm}'))}.<br><b>a)</b> cơ năng của con lắc<br><b>b)</b> thế năng và động năng tại li độ đó<br><b>c)</b> tốc độ của vật tại li độ đó`,
    nd: `${Wt} dùng ${f(12)}, không dùng ${A}; đổi cm → ${f(10)} trước khi bình phương`, a: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], gi: 4 },
  { t: 'Dạng 2 · Trung bình · W<sub>đ</sub> = nW<sub>t</sub>: tìm li độ và tốc độ',
    de: `Lò xo nằm ngang: vật ${u('500', 'g')}, ${nw(m('k=100\\ \\mathrm{N/m}'))}, biên độ ${u('10', 'cm')}, bỏ qua ma sát. Tại một thời điểm động năng bằng 24 lần thế năng.<br><b>a)</b> cơ năng<br><b>b)</b> li độ của vật lúc đó<br><b>c)</b> tốc độ của vật lúc đó`,
    nd: `${m('W_{\\text{đ}}=24W_t')} ⇒ ${m('W=')} ${f(10)}${m('\\,W_t')} ⇒ ${m('|x|=A\\,/')} ${f(12)}`, a: ['a', 'b', 'c'], gi: 4 },
  { t: 'Dạng 3 · Trung bình · Đọc đồ thị năng lượng theo li độ',
    de: `Con lắc lò xo nằm ngang, vật ${u('150', 'g')}, bỏ qua ma sát. Hình bên: ${Wt}, ${Wd} theo li độ ${x}; nét chấm gạch nằm ngang là cơ năng.<br><b>a)</b> độ cứng của lò xo<br><b>b)</b> động năng và tốc độ của vật khi ${nw(m('x=3\\ \\mathrm{cm}'))}`,
    nd: `Tại biên ${m('W_{\\text{đ}}=')} ${f(10)}; đọc ${W}, ${A} (đổi ra J, m) rồi ${m('k=2W/A^2')}`, a: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>'], gi: 4, hinh: H.d3 },
  { t: 'Dạng 4 · Khó · Con lắc đơn góc lớn',
    de: `Con lắc đơn: vật ${u('200', 'g')}, dây nhẹ không dãn dài ${u('0{,}9', 'm')}. Kéo lệch ${m('\\alpha_0=60^\\circ')} rồi thả nhẹ; bỏ qua lực cản, ${g10}, mốc thế năng ở vị trí thấp nhất ${nw(`(${m('\\cos60^\\circ=0{,}5')};`)} ${nw(`${m('\\cos30^\\circ\\approx0{,}866')})`)}.<br><b>a)</b> cơ năng<br><b>b)</b> tốc độ khi qua VTCB<br><b>c)</b> tốc độ khi dây lệch ${m('30^\\circ')}`,
    nd: `${m('60^\\circ')} không nhỏ ⇒ dùng công thức có ${f(12)}, không dùng ${m('\\tfrac12 mgl\\alpha_0^2')}`, a: ['a', 'b', 'c'], gi: 10, hinh: H.d4 },
  { t: 'Dạng 5 · Khó · Đọc đồ thị năng lượng theo thời gian',
    de: `Vật ${u('200', 'g')} dao động điều hoà trên lò xo nằm ngang, bỏ qua ma sát. Hình bên: ${Wt}, ${Wd} theo ${m('t')} (gốc thời gian lúc vật ở biên); hai đồ thị cắt nhau tại hai điểm liên tiếp như hình. Lấy ${pi10}.<br><b>a)</b> cơ năng và chu kì dao động<br><b>b)</b> độ cứng và biên độ<br><b>c)</b> tốc độ cực đại`,
    nd: `Giao điểm: ${m('W_{\\text{đ}}=W_t=')} ${f(12)}; hai giao điểm liên tiếp cách ${f(12)}`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], gi: 10, hinh: H.d5, cot: 5 },
];

// Bài tương tự: mỗi dạng 2 bài, giải vào vở; ô đáp số 25 mm cuối đúng dòng của ý (c<sub>1</sub>, c<sub>2</sub> khi ý có 2 kết quả).
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
    { t: 'Dạng 1 · Bài 1', de: `Lò xo nằm ngang: vật ${u('200', 'g')}, ${nw(m('k=50\\ \\mathrm{N/m}'))}, biên độ ${u('8', 'cm')}, bỏ qua ma sát. Xét lúc ${nw(m('x=4\\ \\mathrm{cm}'))}.<br><b>a)</b> cơ năng<br><b>b)</b> thế năng, động năng lúc đó<br><b>c)</b> tốc độ lúc đó`, o: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'] },
    { t: 'Dạng 1 · Bài 2', de: `Lò xo nằm ngang: vật ${u('1{,}0', 'kg')}, ${nw(m('k=100\\ \\mathrm{N/m}'))}, biên độ ${u('10', 'cm')}, bỏ qua ma sát. Xét lúc ${nw(m('x=-6\\ \\mathrm{cm}'))}.<br><b>a)</b> cơ năng<br><b>b)</b> thế năng, động năng lúc đó<br><b>c)</b> tốc độ lúc đó`, o: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'] },
    { t: 'Dạng 2 · Bài 1', de: `Vật ${u('100', 'g')}, lò xo ${nw(m('40\\ \\mathrm{N/m}'))}, biên độ ${u('6', 'cm')}, bỏ qua ma sát. Lúc động năng bằng 3 lần thế năng:<br><b>a)</b> cơ năng<br><b>b)</b> li độ<br><b>c)</b> tốc độ`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 2 · Bài 2', de: `Vật ${u('400', 'g')}, lò xo ${nw(m('100\\ \\mathrm{N/m}'))}, biên độ ${u('8', 'cm')}, bỏ qua ma sát. Lúc <b>thế năng</b> bằng 3 lần động năng:<br><b>a)</b> cơ năng<br><b>b)</b> li độ<br><b>c)</b> tốc độ`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 3 · Bài 1', de: `Vật ${u('200', 'g')} trên lò xo nằm ngang, bỏ qua ma sát; hình bên là ${Wt}, ${Wd} theo ${x}.<br><b>a)</b> độ cứng lò xo<br><b>b)</b> động năng khi ${nw(m('x=4\\ \\mathrm{cm}'))}<br><b>c)</b> tốc độ khi đó`, fig: H.tt3a(), fw: 40, o: ['a', 'b', 'c'] },
    { t: 'Dạng 3 · Bài 2', de: `Vật ${u('100', 'g')} trên lò xo nằm ngang, bỏ qua ma sát; hình bên là động năng theo ${x}.<br><b>a)</b> độ cứng lò xo<br><b>b)</b> tốc độ cực đại<br><b>c)</b> li độ tại đó ${m('W_{\\text{đ}}=W_t')}`, fig: H.tt3b(), fw: 40, o: ['a', 'b', 'c'] },
  ], [
    { t: 'Dạng 4 · Bài 1', de: `Con lắc đơn: vật ${u('500', 'g')}, dây ${u('1{,}0', 'm')}, thả nhẹ từ ${m('\\alpha_0=60^\\circ')}; bỏ qua lực cản, ${nw(`${g10};`)} ${nw(`${m('\\cos45^\\circ\\approx0{,}707')}.`)}<br><b>a)</b> cơ năng (mốc ở đáy)<br><b>b)</b> tốc độ khi qua VTCB<br><b>c)</b> tốc độ khi dây lệch ${m('45^\\circ')}`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 4 · Bài 2', de: `Con lắc đơn: vật ${u('200', 'g')}, dây ${u('0{,}45', 'm')}. Kéo dây tới nằm ngang ${nw(`(${m('\\alpha_0=90^\\circ')})`)} rồi thả nhẹ; bỏ qua lực cản, ${nw(`${g10}.`)}<br><b>a)</b> cơ năng (mốc ở đáy)<br><b>b)</b> tốc độ khi qua VTCB<br><b>c)</b> tốc độ khi dây lệch ${m('60^\\circ')}`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 5 · Bài 1', de: `Vật ${u('100', 'g')} trên lò xo nằm ngang, bỏ qua ma sát; hình bên là ${Wt}, ${Wd} theo ${m('t')}, gốc thời gian ở biên. Lấy ${nw(`${pi10}.`)}<br><b>a)</b> cơ năng<br><b>b)</b> chu kì dao động<br><b>c)</b> độ cứng lò xo<br><b>d)</b> biên độ`, fig: H.tt5a(), fw: 44, o: ['a', 'b', 'c', 'd'] },
    { t: 'Dạng 5 · Bài 2', de: `Vật ${u('300', 'g')} trên lò xo nằm ngang, bỏ qua ma sát; hình bên là động năng theo ${m('t')}, gốc thời gian lúc qua VTCB. Lấy ${nw(`${pi10}.`)}<br><b>a)</b> chu kì dao động<br><b>b)</b> tần số biến thiên của động năng<br><b>c)</b> độ cứng lò xo<br><b>d)</b> biên độ`, fig: H.tt5b(), fw: 44, o: ['a', 'b', 'c', 'd'] },
    nhap(5),
  ]],
  dap: [
    `D1·1: a) 0,16 J · b<sub>1</sub>) 0,04 J · b<sub>2</sub>) 0,12 J · c) 1,10 m/s &nbsp;|&nbsp; D1·2: a) 0,50 J · b<sub>1</sub>) 0,18 J · b<sub>2</sub>) 0,32 J · c) 0,80 m/s &nbsp;|&nbsp; D2·1: a) 0,072 J · b) ±3 cm · c) 1,04 m/s &nbsp;|&nbsp; D2·2: a) 0,32 J · b) ±6,93 cm · c) 0,63 m/s &nbsp;|&nbsp; D3·1: a) 40 N/m · b) 18 mJ · c) 0,42 m/s &nbsp;|&nbsp; D3·2: a) 100 N/m · b) 1,26 m/s · c) ±2,83 cm`,
    `D4·1: a) 2,5 J · b) 3,16 m/s · c) 2,04 m/s &nbsp;|&nbsp; D4·2: a) 0,90 J · b) 3,0 m/s · c) 2,12 m/s &nbsp;|&nbsp; D5·1: a) 20 mJ · b) 0,2 s · c) 100 N/m · d) 2 cm &nbsp;|&nbsp; D5·2: a) 0,4 s · b) 5 Hz · c) 75 N/m · d) 4 cm`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang: dang.map((d) => (d.hinh ? { ...d, de: `<div class="fig-side" style="grid-template-columns:1fr 46mm"><div>${d.de}</div>${d.hinh()}</div>` } : d)), tach: [3, 2], kq: [[1, 2, 3], [4, 5]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'bốn họ 1·4 · họ 1 1·5 · đo W theo A 2·1 · họ 2 2·2 · đồ thị theo x 2·3 · theo t 3·1 · con lắc đơn 3·2 · bẫy 3·4 · bài toán mẫu 4·2 · dạng 1–3 → 6·1 · dạng 4–5 → 7·1',
  out: process.argv[2],
});
