// Ruột tập VL10 – Bài 31 · Động học của chuyển động tròn đều (lesson id 76). Quyển Chương 6 lớp 10: bài 31 = tr. 1–12.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l10-bai31.mjs (toàn bộ SVG tự vẽ, không dùng ảnh Halliday). Nội dung theo bài web (book/cache/76.json, tải từ DB 12/11/2026):
// mục tiêu, dự đoán sân băng, II.1–II.4, ba thí nghiệm (1 rad, đĩa lò vi sóng, giọt nước), ba bẫy, Trả bài 6 câu, bài toán mẫu bánh xe đạp,
// thử thách, 5 dạng bài tập mẫu. Đáp số Bài tương tự (tuongTu.dap) và các số in sẵn tính bằng Python 12/11/2026.
// Tránh sẵn 4 lỗi lặp HS ảo (L11 Ch.3): π, rad, 1 m/s = 3,6 km/h, cos 21° in sẵn trước khi hỏi · Mục tiêu/hình Dự đoán không nói
// "điểm xa tâm nhanh hơn" và không vẽ quỹ đạo từng người · ô 25 mm cho đáp số chữ/phân số, 40 mm cho đáp số dài · dòng kẻ ≥ số ý ở Dạng 1–3.
// Chạy: node scripts/ruot-tap/l10-bai31.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl10-bai31.pdf
//       node scripts/ruot-tap/l10-bai31.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l10-bai31/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL10b31 as H } from './hinh-l10-bai31.mjs';

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
  const out = resolve(HERE, 'out/hinh-l10-bai31'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 31, lid: 76, ten: 'ĐỘNG HỌC CỦA CHUYỂN ĐỘNG TRÒN ĐỀU', lop: 10, baiDau: 31, sub: 'Vật lí 10 · Chương 6: Chuyển động tròn' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const w = m('\\omega'), th = m('\\theta'), pi = m('\\pi'), vv = m('\\vec v');
const ap = m('\\approx');
const u = (s) => nw(m(s)); // số + đơn vị không gãy dòng
const vph = 'vòng/phút';

// Bài tương tự giải vào vở: ô đáp số cuối dòng từng ý (cùng helper bài 23).
const ttHaiCot = '<style>.bt>.gi{display:grid;grid-template-columns:1fr 1fr;column-gap:4mm}.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm}.yo .oo{flex:none;display:flex;gap:3mm}.yo{line-height:1.35}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}.dd td{text-align:center;padding:.3mm 1mm}</style>';
const p1 = `${ttHaiCot}<section class="page">
${head('BÀI 31 · ĐỘNG HỌC CỦA CHUYỂN ĐỘNG TRÒN ĐỀU', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Đo góc bằng <b>radian</b>; tính <b>độ dịch chuyển góc</b> từ cung và bán kính`)}
${dong(`${ck}Dùng <b>tốc độ góc</b> ${w}, <b>chu kì</b> ${m('T')}, <b>tần số</b> ${m('f')}; đổi ${vph} sang rad/s`)}
${dong(`${ck}Tính <b>tốc độ</b> của một điểm trên vật quay từ ${w}`)}
${dong(`${ck}Vẽ đúng <b>vectơ vận tốc</b> của vật chuyển động tròn đều`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Cả hàng nắm tay, luôn thẳng, xoay quanh người trụ O. So người thứ hai (gần O) với người ngoài cùng, nhận xét nào đúng?</p>
<div class="fig-side" style="${fs(46)}"><div>
${opt('A', 'Hai người như nhau về mọi mặt, vì nắm tay nhau')}
${opt('B', 'Cùng quay hết một vòng trong cùng thời gian, nhưng người ngoài chạy nhanh hơn')}
${opt('C', 'Người ngoài cùng quay hết một vòng mất ít thời gian hơn')}
${opt('D', 'Người gần tâm chạy nhanh hơn, vì ở gần trục quay')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 2)}</div>
${H.hangXoay()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(2)}</div>
${h3(4, 'II.1 · Chuyển động tròn đều và radian', '1·4')}
<div class="card" style="padding:1.2mm 3mm">
<div><b>Chuyển động tròn đều:</b> quỹ đạo là ${f(25)}, ${f(25)} không đổi.</div>
<div>Vị trí của vật: cung ${m('s')} tính từ mốc, hoặc <b>độ dịch chuyển góc</b> ${th}: góc ở ${f(14)} mà bán kính quét được.</div>
<div><b>1 rad</b> là góc chắn cung dài bằng ${f(25)}. &nbsp; ${m('\\theta=')} ${f(14)} &nbsp;(${th} tính bằng ${f(12)})</div>
<div>Cho sẵn: ${m('180^\\circ=\\pi\\ \\text{rad}')}, ${u('\\pi\\approx3{,}14')}. Độ → rad: nhân ${m('\\dfrac{\\pi}{180}')}. Điền bằng ${pi}:</div>
<table class="dd" style="margin-top:.6mm"><tr><th>Góc</th><th>${m('30^\\circ')}</th><th>${m('45^\\circ')}</th><th>${m('60^\\circ')}</th><th>${m('90^\\circ')}</th><th>${m('360^\\circ')} (1 vòng)</th></tr>
<tr><th>rad</th><td style="height:8mm"></td><td></td><td></td><td></td><td></td></tr></table></div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('MỘT RADIAN · TỐC ĐỘ GÓC · CHU KÌ · TẦN SỐ · TỐC ĐỘ')}
${h3(1, 'Thí nghiệm: một radian dài bao nhiêu?', '2·1')}
<div class="card fig-side" style="${fs(40)};padding:1.2mm 3mm"><div>
<div><b>Làm:</b> cắt sợi chỉ dài đúng bằng bán kính nắp nồi, quấn sát vành từ A, đánh dấu điểm cuối B, nối A, B với tâm O.</div>
<div><b>Quan sát:</b> thước đo độ cho ${nw(`${m('\\widehat{AOB}\\approx')} ${f(12)}${m('^\\circ')}`)}; nắp to hay nhỏ ${ck}vẫn vậy ${ck}khác đi.</div>
<div><b>Rút ra:</b> 1 rad không phụ thuộc ${f(25)}; cả vòng dài ${m('2\\pi r')} nên ứng với ${f(14)} rad.</div></div>
${H.radian()}</div>
${h3(2, 'II.2 · Tốc độ góc, chu kì, tần số', '2·2')}
<div class="card" style="padding:1.2mm 3mm">
<div>${w}: góc bán kính quét được trong mỗi ${f(14)}, đơn vị ${f(14)}. &nbsp;Một vòng là ${f(12)} rad.</div>
<div>${m('T')}: thời gian đi hết ${f(25)}, đơn vị ${f(12)}. &nbsp;${m('f')}: số vòng trong ${f(14)}, đơn vị ${f(12)}.</div>
<div style="margin:.6mm 0">${m('\\omega=\\dfrac{\\Delta\\theta}{\\phantom{xx}}')}${f(12)} &nbsp;&nbsp; ${m('T=\\dfrac{\\Delta t}{\\phantom{x}}')}${f(12)} (${m('n')} vòng) &nbsp;&nbsp; ${m('f=\\dfrac{1}{\\phantom{x}}')}${f(12)}</div>
<div>${m('\\omega=\\dfrac{2\\pi}{\\phantom{x}}')}${f(12)} ${m('=2\\pi\\,\\cdot')} ${f(12)} &nbsp;&nbsp; Kim giây: ${u('T=60\\ \\mathrm s')} ⇒ ${m('\\omega=')} ${f(25)} rad/s</div></div>
${h3(3, 'Thí nghiệm đo: chu kì đĩa xoay lò vi sóng', '2·3')}
<div class="fig-side" style="${fs(40)}"><div>
<div><b>Làm:</b> dán băng dính lên mép đĩa, bấm giờ đĩa quay <b>3 vòng</b>; làm 5 lần (số liệu minh hoạ).</div>
<table class="tbl-ct" style="margin-top:.6mm"><tr><th>Lần</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>TB</th></tr>
<tr><th>${m('\\Delta t')} (s)</th><td>30,2</td><td>29,8</td><td>30,1</td><td>30,4</td><td>29,9</td><td></td></tr></table>
<div style="margin-top:.6mm">${m('T=')} ${f(14)} s · ${m('f=')} ${f(14)} Hz · ${m('\\omega=')} ${f(14)} rad/s</div>
${wl(`Vì sao tính ${w} không cần ${u('r=14{,}0\\ \\mathrm{cm}')}?`, 1)}
<div>Lần đo lệch xa trung bình nhất: lần ${f(10)}</div></div>
${H.diaLoVi()}</div>
${h3(4, 'II.3 · Tốc độ và tốc độ góc', '2·4')}
<div class="card fig-side" style="${fs(42)};padding:1.2mm 3mm"><div>
<div>${m('v=\\dfrac{\\Delta s}{\\Delta t}')}, cung ${m('\\Delta s=\\Delta\\theta\\,\\cdot')} ${f(12)}</div><div>⇒ ${m('v=')} ${f(14)} ${m('=\\dfrac{2\\pi r}{\\phantom{x}}')}${f(12)}</div>
<div>Mọi điểm trên cùng một vật quay có chung ${f(12)}, ${f(12)}, ${f(12)}; điểm xa tâm hơn có ${m('v')} ${f(25)}.</div>
<div style="margin-top:.6mm"><b>Quay lại hàng người:</b> người ngoài cùng cách O ${u('6\\ \\mathrm m')}, cả hàng quay 1 vòng hết ${u('5\\ \\mathrm s')}. Cho sẵn ${u('1\\ \\mathrm{m/s}=3{,}6\\ \\mathrm{km/h}')}.</div>
<div>${m('v=')} ${f(14)} m/s ${m('\\approx')} ${f(14)} km/h</div></div>
${H.haiDiem()}</div>
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('VECTƠ VẬN TỐC · BẪY · TRẢ BÀI')}
${h3(1, 'II.4 · Vectơ vận tốc: luôn tiếp tuyến', '3·1')}
<div class="card fig-side" style="${fs(42)};padding:1.2mm 3mm"><div>
<div><b>Phương:</b> ${f(25)} với đường tròn, ${f(25)} với bán kính tại điểm đó.</div>
<div><b>Chiều:</b> theo ${f(25)}. &nbsp;<b>Độ lớn:</b> bằng ${f(12)}, không đổi.</div>
<div>Phương đổi theo vị trí ⇒ ${vv} luôn đổi ${f(25)}.</div>
<div style="margin-top:.8mm"><b>Thí nghiệm giọt nước:</b> quay bánh xe đạp dựng ngược có nước trên lốp. Vệt nước rời vành theo ${nw(`${ck}bán kính`)} ${nw(`${ck}tiếp tuyến`)} ${nw(`${ck}cong theo vành`)}.</div>
<div><b>Rút ra:</b> rời bánh, giọt nước giữ ${f(25)} ở chỗ rời.</div></div>
${H.veVanToc()}</div>
${h3(2, 'III · Ba cái bẫy hay sập', '3·2')}
<div class="card" style="padding:1mm 3mm">
<div class="trap">${ck}<span><b>“Tốc độ không đổi thì vận tốc không đổi.”</b> Tốc độ là một con số; ${vv} có hướng, đổi hướng là vận tốc đổi (Bài 32 tìm gia tốc).</span></div>
<div class="trap">${ck}<span><b>“Cùng quay theo một vật thì cùng tốc độ.”</b> Chung ${w}, ${m('T')}, ${m('f')}; còn ${m('v=\\omega r')} khác theo ${m('r')}.</span></div>
<div class="trap">${ck}<span><b>“Vòng/phút là rad/s.”</b> Chia 60 được ${m('f')}, rồi nhân ${m('2\\pi')}: ${m('\\omega=\\dfrac{2\\pi n}{60}')}.</span></div></div>
${h3(3, 'IV · Trả bài 6 câu', '3·3')}
${box(`${tb('1. Chuyển động tròn đều là gì? Vị trí vật cho bằng gì?')}${lines(2)}
${tb('2. 1 rad là gì? Công thức góc theo cung; đổi độ sang rad.')}${lines(2)}
${tb(`3. Định nghĩa ${w}, T, f kèm đơn vị.`)}${lines(2)}
${tb(`4. Viết các hệ thức nối ${w}, T, f, v.`)}${lines(2)}
${tb('5. Vectơ vận tốc: phương, chiều, độ lớn?')}${lines(2)}
${tb('6. Đổi n vòng/phút sang rad/s thế nào?')}${lines(1)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/6 câu · chưa thuộc: ${f(25)} ${nw(`→ đọc lại ô ${f(12)} Tập`)}</div>
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('TỰ KIỂM TRA · BÀI TOÁN MẪU')}
${h3(1, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '4·1')}
${rkHai([1, 2, 3, 4], [5, 6, 7])}
${h3(2, 'V · Bài toán mẫu: tốc độ điểm trên vành bánh xe đạp', '4·2')}
<div class="card soft" style="padding:1.2mm 3mm">Bánh xe đạp đường kính ${u('60\\ \\mathrm{cm}')} quay đều ${nw(`120 ${vph}`)} quanh trục. Cho sẵn ${u('1\\ \\mathrm{m/s}=3{,}6\\ \\mathrm{km/h}')}.
<div><b>a)</b> Tính tần số và chu kì quay của bánh xe.</div><div><b>b)</b> Tính tốc độ góc của bánh xe.</div>
<div><b>c)</b> Tính tốc độ của một điểm trên vành (so với trục), theo m/s và km/h.</div></div>
${h3(3, 'Phân tích đề')}
<table><tr><th style="width:50mm">Câu trong đề</th><th>Dữ liệu → kiến thức</th></tr>
<tr><td>“đường kính 60 cm”</td><td>${m('r=0{,}3\\ \\mathrm m')} (nửa đường kính, đổi ra mét)</td></tr>
<tr><td style="height:6.5mm">“quay đều 120 ${vph}”</td><td></td></tr>
<tr><td style="height:6.5mm">“chu kì”</td><td></td></tr>
<tr><td style="height:6.5mm">“tốc độ góc”</td><td></td></tr>
<tr><td style="height:6.5mm">“điểm trên vành bánh xe”</td><td></td></tr></table>
${h3(4, 'Giải')}
<div class="fig-side" style="${fs(46)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl(`a) ${m('f')}, ${m('T')}:`, 2)}${wl(`b) ${w}:`, 2)}${wl(`c) ${m('v')} (m/s rồi km/h):`, 3)}${wl(`Kiểm bằng cách khác: mỗi vòng điểm vành đi ${m('\\pi d')} ⇒`, 2)}</div>${H.banhXe()}</div>
${h3(5, `Điền bước còn thiếu: bánh xe trẻ em đường kính 40 cm, ${nw(`150 ${vph}`)}`)}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div class="ln"><b>Bước 1 (cho sẵn):</b> ${m('f=150/60=2{,}5\\ \\mathrm{Hz}')}; ${m('T=0{,}4\\ \\mathrm s')}</div>
${wl(`Bước 2: ${m('\\omega=')}`, 1)}${wl(`Bước 3: ${m('r=')} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; m &nbsp;&nbsp;⇒ ${m('v=')}`, 1)}</div>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TẬP VỀ NHÀ · THỬ THÁCH · MANG VỀ')}
${K.btvn()}
${h3(2, 'Thử thách phân tầng', '5·2')}
<div class="fig-side" style="${fs(44)}">${box(wl(`${m('\\bigstar')} Động cơ quay ${nw(`3000 ${vph}`)}. Tính ${w}.`, 3)
 + wl(`${m('\\bigstar\\bigstar')} Kim phút dài ${u('10\\ \\mathrm{cm}')}, kim giờ dài ${u('6\\ \\mathrm{cm}')}. Tốc độ đầu kim phút gấp mấy lần đầu kim giờ?`, 4)
 + wl(`${m('\\bigstar\\bigstar\\bigstar')} Hà Nội ở vĩ độ ${m('21^\\circ')}; ${u('R=6370\\ \\mathrm{km}')}, Trái Đất tự quay ${u('T=24\\ \\mathrm h=86\\,400\\ \\mathrm s')}, ${u('\\cos21^\\circ\\approx0{,}934')}. Tốc độ của người đứng yên ở Hà Nội? Vì sao không dùng thẳng ${m('R')}?`, 5))}${H.traiDat()}</div>
${h3(3, 'Câu đổi chiều (bài toán mẫu)', '5·3')}
${box(wl(`Bánh xe nhỏ đường kính ${u('40\\ \\mathrm{cm}')}. Muốn điểm trên vành có đúng tốc độ như bài mẫu (${u('3{,}77\\ \\mathrm{m/s}')}), bánh phải quay bao nhiêu ${vph}? Viết ${m('v=\\omega r')} trước khi đoán tăng hay giảm.`, 5))}
${h3(4, 'VI · Mang về: điều em dễ quên nhất', '5·4')}
${box(wl('1.', 3) + wl('2.', 3) + wl('3.', 3))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Nhận biết tròn đều, vận tốc, độ dịch chuyển góc',
    de: `Xe đồ chơi chạy ngược chiều kim đồng hồ trên ray tròn tâm O, ${u('r=0{,}50\\ \\mathrm m')}; đồng hồ tốc độ luôn chỉ ${u('0{,}40\\ \\mathrm{m/s}')}. Xe đang qua A, điểm xa nhất bên phải O.<br><b>a)</b> có phải tròn đều; vận tốc có đổi không<br><b>b)</b> tại A, ${vv} có phương, chiều thế nào<br><b>c)</b> sau ${u('5{,}0\\ \\mathrm s')}: cung đi được, độ dịch chuyển góc (rad)`,
    nd: `Tròn đều: quỹ đạo tròn, ${f(25)} không đổi; ${vv} ${f(25)} bán kính`, a: ['a', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'], gi: 5, fig: H.ray() },
  { t: 'Dạng 2 · Dễ · Chu kì, tần số, tốc độ góc từ số vòng đếm được',
    de: `Vòng đu quay quay đều, hết ${nw('5 vòng')} trong ${u('2{,}0')} phút.<br><b>a)</b> chu kì và tần số &nbsp; <b>b)</b> tốc độ góc<br><b>c)</b> sau ${u('10\\ \\mathrm s')}, bán kính nối một cabin với trục quét góc bao nhiêu độ`,
    nd: `Đổi phút ra ${f(12)}; ${m('T=\\Delta t/n')}; góc quét ${m('\\theta=')} ${f(14)}, nhân ${m('180^\\circ/\\pi')} ra độ`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'], gi: 5 },
  { t: 'Dạng 3 · Trung bình · Đổi vòng/phút ra rad/s; góc quay rất ngắn',
    de: `Đĩa ổ cứng máy tính quay đều ${nw(`7200 ${vph}`)}.<br><b>a)</b> tần số và chu kì (chu kì ra mili giây) &nbsp; <b>b)</b> tốc độ góc (rad/s)<br><b>c)</b> trong ${u('1{,}0\\ \\mathrm{ms}')} đĩa quay góc bao nhiêu độ`,
    nd: `${vph}: chia ${f(12)} ra ${m('f')}, nhân ${f(12)} ra ${w}; ${u('1\\ \\mathrm{ms}=')} ${f(14)} s`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'], gi: 5 },
  { t: 'Dạng 4 · Trung bình · Các điểm cùng quay, khác bán kính',
    de: `Đĩa than đường kính ${u('30\\ \\mathrm{cm}')} quay đều ${nw(`45 ${vph}`)} quanh trục qua tâm. M ở mép đĩa, N cách tâm ${u('5{,}0\\ \\mathrm{cm}')}.<br><b>a)</b> tốc độ góc của đĩa<br><b>b)</b> tốc độ của M<br><b>c)</b> tốc độ của N`,
    nd: `Cùng một đĩa ⇒ chung ${f(14)}; ${nw(`${m('r_M=')} ${f(14)} m`)} (nửa đường kính)`, a: ['a', 'b', 'c'], gi: 7, fig: H.diaThan() },
  { t: 'Dạng 5 · Khó · Từ vòng/phút ra tốc độ đầu cánh; bài ngược tìm chiều dài cánh',
    de: `Cánh quạt máy làm mát dài ${u('0{,}40\\ \\mathrm m')} (từ trục tới đầu cánh), quay đều ${nw(`480 ${vph}`)}.<br><b>a)</b> tốc độ của đầu cánh<br><b>b)</b> thay cánh khác, quạt quay chậm lại còn ${nw(`320 ${vph}`)} mà đầu cánh vẫn giữ tốc độ như trước: cánh mới dài bao nhiêu`,
    nd: `Giữ ${m('v')} ⇒ ${m('\\omega_1 r_1=')} ${f(14)}; ${w} giảm thì ${m('r')} phải ${f(14)}`, a: ['a', 'b'], gi: 9, fig: H.canhQuat() },
];

// Bài tương tự: mỗi dạng 2 bài, đáp số tính bằng Python 12/11/2026 (math.pi, degrees), làm tròn 3 chữ số có nghĩa.
const oY = (s, o, w = 25) => s.split('<br>').map((p) => {
  const y = p.match(/^<b>([a-d])\)<\/b>/);
  if (!y) return `<div>${p}</div>`;
  const ls = o.filter((l) => l[0] === y[1]);
  return `<div class="yo"><span>${p}</span><span class="oo">${ls.map((l) => `<span class="nw"><b>${l})</b>${f(w)}</span>`).join('')}</span></div>`;
}).join('');
const ttDe = (b) => b.fig ? `<div class="fig-side" style="grid-template-columns:1fr ${b.fw}mm">${`<div>${oY(b.de, b.o, b.ow)}</div>`}${b.fig}</div>` : oY(b.de, b.o, b.ow);
const vaoVo = (ds) => ds.map((b) => (b.o ? { t: b.t, de: ttDe(b), k: 0 } : b));
const nhap = (n) => ({ t: '<span class="nhap-t">Nháp / chỗ em còn vướng</span>', de: lines(n), k: 0 });
const s1 = '<sub>1</sub>', s2 = '<sub>2</sub>';
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–3', 'DẠNG 4–5'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Vận động viên chạy trên đường tròn bán kính ${u('50\\ \\mathrm m')}, đồng hồ tốc độ luôn chỉ ${u('5{,}0\\ \\mathrm{m/s}')}.<br><b>a)</b> có phải chuyển động tròn đều; vận tốc có đổi không<br><b>b)</b> cung chạy được sau ${u('20\\ \\mathrm s')}<br><b>c)</b> độ dịch chuyển góc sau ${u('20\\ \\mathrm s')} (rad)`, o: [`a${s1}`, `a${s2}`, 'b', 'c'] },
    { t: 'Dạng 1 · Bài 2', de: `Ô tô chạy vòng xuyến bán kính ${u('20\\ \\mathrm m')}, tốc độ không đổi ${u('10\\ \\mathrm{m/s}')}, đang qua D (hình).<br><b>a)</b> ${vv} tại D: phương, chiều<br><b>b)</b> cung đi được sau ${u('3{,}0\\ \\mathrm s')}<br><b>c)</b> độ dịch chuyển góc đó (rad và độ)`, fig: H.vongXuyen(), fw: 40, o: ['a', 'b', `c${s1}`, `c${s2}`] },
    { t: 'Dạng 2 · Bài 1', de: `Con quay đồ chơi quay đều, được ${nw('12 vòng')} trong ${u('3{,}0\\ \\mathrm s')}.<br><b>a)</b> chu kì và tần số<br><b>b)</b> tốc độ góc<br><b>c)</b> góc quét được trong ${u('0{,}10\\ \\mathrm s')} (độ)`, o: [`a${s1}`, `a${s2}`, 'b', 'c'] },
    { t: 'Dạng 2 · Bài 2', de: `Vòng đu quay quay đều ${nw('3 vòng')} trong ${u('1{,}5')} phút.<br><b>a)</b> chu kì và tần số<br><b>b)</b> tốc độ góc<br><b>c)</b> góc quét được trong ${u('5{,}0\\ \\mathrm s')} (độ)`, o: [`a${s1}`, `a${s2}`, 'b', 'c'] },
    { t: 'Dạng 3 · Bài 1', de: `Mũi máy khoan quay đều ${nw(`3000 ${vph}`)}.<br><b>a)</b> tần số và chu kì (ms)<br><b>b)</b> tốc độ góc (rad/s)<br><b>c)</b> góc quay trong ${u('2{,}0\\ \\mathrm{ms}')} (độ)`, o: [`a${s1}`, `a${s2}`, 'b', 'c'] },
    { t: 'Dạng 3 · Bài 2', de: `Cánh quạt bàn quay đều ${nw(`1200 ${vph}`)}.<br><b>a)</b> tần số và chu kì (ms)<br><b>b)</b> tốc độ góc (rad/s)<br><b>c)</b> góc quay trong ${u('10\\ \\mathrm{ms}')} (độ)`, o: [`a${s1}`, `a${s2}`, 'b', 'c'] },
  ], [
    { t: 'Dạng 4 · Bài 1', de: `Đĩa CD đường kính ${u('12\\ \\mathrm{cm}')} quay đều ${nw(`300 ${vph}`)}. M ở mép, N cách tâm ${u('2{,}0\\ \\mathrm{cm}')}.<br><b>a)</b> tốc độ góc<br><b>b)</b> tốc độ của M<br><b>c)</b> tốc độ của N`, fig: H.diaCD(), fw: 40, o: ['a', 'b', 'c'] },
    { t: 'Dạng 4 · Bài 2', de: `Cánh quạt trần dài ${u('60\\ \\mathrm{cm}')} (từ trục), quay đều ${nw(`180 ${vph}`)}.<br><b>a)</b> tốc độ góc<br><b>b)</b> tốc độ đầu cánh<br><b>c)</b> tốc độ điểm giữa cánh<br><b>d)</b> tốc độ đầu cánh gấp mấy lần điểm giữa`, o: ['a', 'b', 'c', 'd'] },
    { t: 'Dạng 5 · Bài 1', de: `Tua-bin gió có cánh dài ${u('20\\ \\mathrm m')} (từ trục), quay đều ${nw(`15 ${vph}`)}.<br><b>a)</b> tốc độ đầu cánh<br><b>b)</b> gió yếu, tua-bin chỉ quay ${nw(`12 ${vph}`)}; muốn đầu cánh giữ tốc độ cũ thì cánh phải dài bao nhiêu`, o: ['a', 'b'] },
    { t: 'Dạng 5 · Bài 2', de: `Lưỡi máy cắt cỏ dài ${u('0{,}25\\ \\mathrm m')} (từ trục), quay đều ${nw(`3000 ${vph}`)}.<br><b>a)</b> tốc độ đầu lưỡi<br><b>b)</b> thay lưỡi dài ${u('0{,}30\\ \\mathrm m')}, giữ tốc độ đầu lưỡi: máy phải quay bao nhiêu ${vph}`, o: ['a', 'b'] },
    nhap(10),
  ]],
  dap: [
    `D1·1: a${s1}) có · a${s2}) có, đổi hướng · b) 100 m · c) 2,0 rad &nbsp;|&nbsp; D1·2: a) nằm ngang, sang phải · b) 30 m · c${s1}) 1,5 rad · c${s2}) ${ap} 85,9° &nbsp;|&nbsp; D2·1: a${s1}) 0,25 s · a${s2}) 4,0 Hz · b) 8${pi} ${ap} 25,1 rad/s · c) 144° &nbsp;|&nbsp; D2·2: a${s1}) 30 s · a${s2}) ${ap} 0,0333 Hz · b) ${pi}/15 ${ap} 0,209 rad/s · c) 60° &nbsp;|&nbsp; D3·1: a${s1}) 50 Hz · a${s2}) 20 ms · b) 100${pi} ${ap} 314 rad/s · c) 36° &nbsp;|&nbsp; D3·2: a${s1}) 20 Hz · a${s2}) 50 ms · b) 40${pi} ${ap} 126 rad/s · c) 72°`,
    `D4·1: a) 10${pi} ${ap} 31,4 rad/s · b) ${ap} 1,88 m/s · c) ${ap} 0,628 m/s &nbsp;|&nbsp; D4·2: a) 6${pi} ${ap} 18,8 rad/s · b) ${ap} 11,3 m/s · c) ${ap} 5,65 m/s · d) 2 &nbsp;|&nbsp; D5·1: a) ${ap} 31,4 m/s · b) 25 m &nbsp;|&nbsp; D5·2: a) ${ap} 78,5 m/s · b) 2500 ${vph}`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 2], kq: [[1, 2, 3], [4, 5]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: `radian 1·4 · 1 rad 2·1 · ${w}, T, f 2·2 · đĩa lò vi sóng 2·3 · ${m('v=\\omega r')} 2·4 · vectơ vận tốc 3·1 · bẫy 3·2 · bài toán mẫu 4·2 · dạng 1–3 → 6·1 · dạng 4–5 → 7·1`,
  out: process.argv[2],
});
