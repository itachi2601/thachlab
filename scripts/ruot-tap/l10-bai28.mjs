// Ruột tập VL10 – Bài 28 · Động lượng (lesson id 73). Quyển L10 Chương 5 (bài 28–30): bài này là tr. 1–12.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự giải vào vở · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l10-bai28.mjs (toàn bộ SVG tự vẽ, không dùng ảnh Halliday). Nội dung theo bài web (book/cache/73.json, tải từ DB 12/11/2026):
// mục tiêu, dự đoán sân băng, II.1–II.4, hai thí nghiệm, ba bẫy, Trả bài 6 câu, bài toán mẫu bóng đập tường, thử thách, 5 dạng bài tập mẫu.
// Đáp số Bài tương tự (tuongTu.dap) và bài mẫu tính bằng Python 12/11/2026. Tránh sẵn 4 lỗi lặp HS ảo L11 Ch.3: hằng số (g, cos 60°)
// in sẵn trước khi hỏi · Mục tiêu/chú thích hình cạnh Dự đoán không lộ đáp án · ô đủ rộng cho phân số · dòng kẻ ≥ số ý.
// Chạy: node scripts/ruot-tap/l10-bai28.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl10-bai28.pdf
//       node scripts/ruot-tap/l10-bai28.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l10-bai28/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai, dapSo, TRANG_DAU } from './khung.mjs';
import { hinhL10b28 as H } from './hinh-l10-bai28.mjs';

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
  const out = resolve(HERE, 'out/hinh-l10-bai28'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 28, lid: 73, ten: 'ĐỘNG LƯỢNG', lop: 10, baiDau: 28, sub: 'Vật lí 10 · Chương 5: Động lượng' });
const { head, h3, foot } = K;
const tr = (n) => (28 - 28) * 12 + TRANG_DAU - 1 + n; // số trang tuyệt đối trong quyển
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const u = (s, d) => nw(m(`${s}\\ \\mathrm{${d}}`));
const KMS = '\\mathrm{kg\\cdot m/s}';
const kms = (s) => nw(m(`${s}\\ ${KMS}`));
const g98 = nw(m('g=9{,}8\\ \\mathrm{m/s^2}'));
const fn = f(12), fw = f(25), fl = f(34); // ô số ≥12 mm, ô chữ ≥25 mm (HS ảo 10/11), ô biểu thức dài 34 mm
const fp = (w, p) => nw(`${f(w)}${p}`); // ô + dấu câu dính nhau
const fu = (w = 16, d = KMS) => nw(`${f(w)}&nbsp;${m(d)}`); // ô số + đơn vị không gãy dòng
// Dòng viết cao 9 mm cho chỗ phải viết phân số/căn (HS ảo: phân số cần ô cao ≥ 9 mm)
const ph = (lab, tail = '') => `<div class="ln" style="height:9mm;display:flex;align-items:center;gap:1.5mm"><span>${lab}</span><span style="flex:1"></span>${tail}</div>`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const vp = m('\\vec p'), vv = m('\\vec v'), dp = m('\\Delta\\vec p'), al = m('\\alpha');

const p1 = `<section class="page">
${head('BÀI 28 · ĐỘNG LƯỢNG', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Nêu được động lượng: công thức, hướng, đơn vị, hệ quy chiếu`)}
${dong(`${ck}Tính động lượng của <b>hệ hai vật</b> theo góc giữa hai chuyển động`)}
${dong(`${ck}Tính ${m('\\Delta p')} (cả khi <b>bật ngược lại</b>), lực trung bình; giải thích đệm hơi`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Trên sân băng (bỏ qua ma sát), bạn nhỏ ${u('30', 'kg')} lướt ${u('4', 'm/s')}, người lớn ${u('60', 'kg')} lướt ${u('2', 'm/s')} thẳng về phía em. Muốn mỗi người dừng hẳn trong cùng ${u('1', 's')}, em phải đẩy ai mạnh hơn?</p>
<div class="fig-side" style="${fs(44)}"><div>
${opt('A', 'Bạn nhỏ, vì lướt nhanh gấp đôi')}
${opt('B', 'Người lớn, vì nặng gấp đôi')}
${opt('C', 'Mạnh như nhau')}
${opt('D', 'Không so sánh được khi chưa biết lực')}
<div style="margin-top:1mm">${chon(12)}</div><div class="ln"><span class="hint">Vì sao?</span></div></div>
${H.sanBang()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${fn} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Động lượng của một vật', '1·4')}
<div class="card" style="padding:1.2mm 3mm">
<div class="two" style="display:grid;grid-template-columns:1fr 1fr;gap:0 4mm">
<div>Động lượng: ${vp} = ${fn}</div><div>Độ lớn: ${m('p=')} ${fn}</div>
<div>Vector cùng hướng với ${fn}</div><div>Đơn vị: ${fw}</div>
<div>${m('p')} phụ thuộc hệ quy chiếu vì</div><div>${fw} phụ thuộc hệ quy chiếu.</div></div>
<div>Đặc trưng cho khả năng ${fl} khi tương tác với vật khác.</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:0 4mm">
<div>Bóng ${u('0{,}45', 'kg')}, ${u('20', 'm/s')}: ${m('p=')} ${fn}</div><div>Xe ${nw(m('10')+' tấn')}, ${u('1', 'm/s')}: ${m('p=')} ${fw}</div></div>
<div>Khách ${u('60', 'kg')} ngồi yên trên tàu chạy ${u('15', 'm/s')}: so với toa ${m('p=')} ${fn}; so với ga ${m('p=')} ${fn}</div></div>
${h3(5, 'Thí nghiệm: bi lăn va khúc gỗ', '1·5')}
<div class="card fig-side" style="${fs(42)};padding:1.2mm 3mm"><div>
<div><b>Làm:</b> thả bi ${u('50', 'g')} từ độ cao ${u('10', 'cm')} rồi ${u('20', 'cm')}; lặp lại với bi ${u('100', 'g')}.</div>
<div><b>Quan sát:</b> thả cao hơn: bi tới ${fn}, ${m('d')} ${fp(12, '.')}</div>
<div>Bi nặng hơn: ${m('d')} ${fp(12, '.')}</div>
<div><b>Rút ra:</b> phụ thuộc cả ${fn} lẫn ${fp(12, ';')}</div>
<div>gộp lại thành ${fp(25, '.')}</div></div>
${H.biGo()}</div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('ĐỘNG LƯỢNG CỦA HỆ · XUNG LƯỢNG · ĐO BẰNG CẢM BIẾN')}
${h3(1, 'II.2 · Động lượng của hệ nhiều vật', '2·1')}
<div class="card fig-side" style="${fs(44)};padding:.8mm 3mm 1.2mm"><div>
<div>${m('\\vec p_{\\mathrm{he}}=')} ${fl} &nbsp;(cộng ${fp(25, ')')}</div>
<div>Cùng hướng (${m('\\alpha=0^\\circ')}): ${m('p=')} ${fl}</div>
<div>Ngược hướng (${m('\\alpha=180^\\circ')}): ${m('p=')} ${fl}</div>
${ph(`Vuông góc (${m('\\alpha=90^\\circ')}): ${m('p=')}`)}
${ph(`Góc ${al} bất kì: ${m('p^2=')}`)}
${ph(`Nếu ${m('p_1=p_2')}: ${m('p=')}`)}</div>
${H.binhHanh(`Hai vector chung gốc, hợp góc ${m('\\alpha')}.`)}</div>
${h3(2, 'II.3 · Xung lượng và độ biến thiên động lượng', '2·2')}
<div class="card" style="padding:.8mm 3mm 1.2mm">
<div>Xung lượng của lực trong ${m('\\Delta t')}: ${fp(25, ';')} đơn vị ${fw} = ${fp(25, '.')}</div>
<div>Độ biến thiên động lượng: ${dp} = ${fw} (sau trừ trước), cũng là ${fp(25, '.')}</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:5mm">${ph(`${dp} =`)}${ph(`Suy ra ${m('\\vec F=')}`)}</div>
<div>Dạng thứ hai chính là dạng tổng quát của ${fp(34, '.')}</div>
<div>Mẹo nhớ: “Lực nhỏ thì phải ${fp(25, '”')} — cùng ${m('\\Delta p')}, ${m('\\Delta t')} dài ra thì ${m('F')} ${fp(25, '.')}</div>
<div>Vật ${u('2', 'kg')} đứng yên, lực ngang ${u('50', 'N')} trong ${u('0{,}2', 's')}: ${m('\\Delta p=')} ${fn} ⇒ ${m('v=')} ${fn}</div></div>
${h3(3, 'Thí nghiệm: xe bật vào đệm lò xo', '2·3')}
<div class="card fig-side" style="${fs(44)};padding:1mm 3mm"><div>
<div><b>Làm:</b> xe ${u('0{,}250', 'kg')} trên ray đệm khí bật vào đệm lò xo gắn cảm biến lực; cổng quang đo ${m('v_1')} lúc tới, ${m('v_2')} lúc bật lại (chiều dương: chiều tới).</div>
<div><b>Quan sát:</b> ${m('v_2')} luôn mang dấu ${fp(12, ';')} cảm biến cho xung lượng ở hàng 3.</div></div>
${H.demLoXo()}</div>
<table class="tbl-ct"><tr><th>Lần</th><th>1</th><th>2</th><th>3</th><th>4</th></tr>
<tr><td>${m('v_1')} ; ${m('v_2')} (m/s)</td><td>0,40 ; −0,32</td><td>0,60 ; −0,49</td><td>0,80 ; −0,63</td><td>1,00 ; −0,81</td></tr>
<tr><td>Cảm biến (N·s)</td><td>0,176</td><td>0,268</td><td>0,352</td><td>0,445</td></tr>
<tr><td style="height:7mm">${m('|\\Delta p|=m|v_2-v_1|')}</td><td></td><td></td><td></td><td></td></tr></table>
<div style="margin:.8mm 0 0">Sai số cho phép = cổng quang ${m('\\pm 0{,}01\\ \\mathrm{m/s}')} (${m('\\Delta p')} sai cỡ ${m('\\pm 0{,}005')}) <b>cộng</b> cảm biến ${m('\\pm 2\\,\\%')}.</div>
<div><b>Rút ra:</b> chênh lệch ${fw} sai số cho phép ⇒ khớp với ${fp(34, '.')}</div>
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('BẪY · TRẢ BÀI · KẾT QUẢ TỰ KIỂM TRA')}
${h3(1, 'III · Ba cái bẫy hay sập', '3·1')}
<div class="card fig-side" style="${fs(42)};padding:1mm 3mm"><div>
<div class="trap">${ck}<span><b>Tính ${m('\\Delta p')} bằng hiệu hai độ lớn.</b> Bật ngược lại thì hai vận tốc trái dấu. Xe ${u('1', 'kg')} tới ${u('1', 'm/s')}, bật lại ${u('1', 'm/s')}: ${m('\\Delta p=')} ${fn}, không phải 0.</span></div>
<div class="trap">${ck}<span><b>Cộng động lượng như cộng số.</b> Hai xe giống nhau chạy ngược chiều cùng tốc độ: ${m('p_{\\mathrm{he}}=')} ${fn}, không phải ${m('2mv')}.</span></div>
<div class="trap">${ck}<span><b>“Đệm mềm làm giảm ${m('\\Delta p')}.”</b> Cùng vật, cùng tốc độ chạm, cùng dừng hẳn thì ${m('\\Delta p')} ${fp(25, ';')} đệm kéo dài ${m('\\Delta t')} nên ${m('F')} ${fp(25, '.')}</span></div></div>
${H.ftDoThi()}</div>
${h3(2, 'IV · Trả bài 6 câu', '3·2')}
${box(`${tb('1. Động lượng là gì? Công thức, đơn vị, hướng.')}${lines(2)}
${tb('2. Vì sao động lượng phụ thuộc hệ quy chiếu? Cho ví dụ.')}${lines(2)}
${tb('3. Động lượng của hệ hai vật tính thế nào? Các góc đặc biệt?')}${lines(2)}
${tb('4. Xung lượng của lực là gì, đơn vị gì?')}${lines(2)}
${tb('5. Liên hệ giữa Δp và lực; dạng tổng quát định luật II Newton.')}${lines(2)}
${tb('6. Đệm hơi cứu hộ giúp người nhảy xuống an toàn nhờ đâu?')}${lines(2)}`)}
<div class="card soft" style="margin-top:1.5mm;padding:1mm 3mm"><b>Bạn cùng bàn kiểm:</b> nói được ……/6 câu · câu chưa thuộc: ${fw} ${nw(`→ đọc lại ô Tập ${fn}`)}</div>
${h3(3, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '3·3')}
${rkHai([1, 2, 3], [4, 5, 6])}
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('BÀI TOÁN MẪU · BÓNG ĐẬP TƯỜNG')}
${h3(1, 'V · Đề bài', '4')}
<div class="card soft" style="padding:1.2mm 3mm">Quả bóng ${u('0{,}45', 'kg')} bay ngang với tốc độ ${u('12', 'm/s')}, đập vuông góc vào tường rồi bật ngược lại theo phương cũ với tốc độ ${u('8', 'm/s')}. Thời gian bóng chạm tường là ${u('0{,}05', 's')}.
<div><b>a)</b> Tìm độ biến thiên động lượng của bóng.</div><div><b>b)</b> Tìm lực trung bình do tường tác dụng lên bóng.</div></div>
${h3(2, 'Phân tích đề')}
<table><tr><th style="width:46mm">Câu trong đề</th><th style="width:34mm">Dữ liệu</th><th>Kiến thức liên quan</th></tr>
<tr><td>“khối lượng 0,45&nbsp;kg”</td><td>${m('m=0{,}45\\ \\mathrm{kg}')}</td><td>động lượng ${m('p=mv')}</td></tr>
<tr><td style="height:6.5mm">“bay … tốc độ 12&nbsp;m/s”</td><td></td><td></td></tr>
<tr><td style="height:6.5mm">“bật ngược lại … 8&nbsp;m/s”</td><td></td><td></td></tr>
<tr><td style="height:6.5mm">“chạm tường 0,05&nbsp;s”</td><td></td><td></td></tr>
<tr><td style="height:6.5mm">“lực trung bình do tường”</td><td></td><td></td></tr></table>
${h3(3, 'Giải')}
<div class="fig-side" style="${fs(42)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl('Chọn chiều dương:', 1)}${wl('a)', 4)}${wl('b)', 4)}${wl(`Kiểm tra (${g98}): ${m('mg\\approx')} …… N; so với lực tường: ……`, 1)}</div>${H.bongTuong()}</div>
${h3(4, 'Điền bước còn thiếu: lưới giữ bóng')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div class="ln" style="height:auto;padding-top:1mm"><b>Đề:</b> cùng quả bóng bay ${u('12', 'm/s')}, lưới khung thành giữ bóng lại, bóng dừng hẳn sau ${u('0{,}20', 's')}.</div>
<div class="ln"><b>Bước 1 (cho sẵn):</b> chiều dương là chiều bóng bay; ${m('v_1=12\\ \\mathrm{m/s}')}, ${m('v_2=0')}.</div>
${wl(`Bước 2: ${m('\\Delta p=')} …`, 2)}${wl(`Bước 3: lực trung bình của lưới ${m('F=')} …`, 2)}
${wl('So với tường ở câu b), vì sao nhỏ hơn?', 2)}</div>
<div class="card soft" style="margin-top:1.5mm;padding:1mm 3mm"><b>Em tự kiểm:</b> ${ck}chọn chiều dương trước &nbsp;${ck}${m('v_2')} có dấu &nbsp;${ck}${m('\\Delta p')} = sau − trước &nbsp;${ck}có đơn vị</div>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TẬP VỀ NHÀ · MANG VỀ · THỬ THÁCH')}
${K.btvn()}
${h3(2, 'VI · Mang về: điều em dễ quên nhất', '5')}
${box(wl('1.', 2) + wl('2.', 2) + wl('3.', 2))}
${h3(3, 'Thử thách phân tầng')}
<div class="fig-side" style="${fs(36)}">${box(wl(`★ So sánh động lượng viên đạn ${u('10', 'g')} bay ${u('800', 'm/s')} với bóng ${u('0{,}45', 'kg')} bay ${u('12', 'm/s')}.`, 2)
 + wl(`★★ Hai vật có động lượng cùng độ lớn ${kms('6')}, hợp nhau góc ${m('120^\\circ')} (${nw(m('\\cos 60^\\circ=0{,}5'))}). Động lượng của hệ?`, 2)
 + wl(`★★ Vật ${u('1', 'kg')} rơi tự do từ nghỉ, ${g98}. Độ biến thiên động lượng sau ${u('2', 's')}?`, 2)
 + wl(`★★★ Người ${u('60', 'kg')} rơi từ ${u('5', 'm')} xuống đệm hơi, dừng hẳn sau ${u('0{,}50', 's')}; tốc độ chạm đệm ${m('v')} với ${nw(m('v^2=2gh'))}, ${g98}. Độ lớn hợp lực trung bình lên người? Rơi xuống bê tông, dừng trong ${u('0{,}01', 's')} thì hợp lực gấp mấy lần?`, 4))}${H.demHoi()}</div>
${h3(4, 'Đời sống: nơi đang dùng bài này')}
<div class="card" style="padding:1.2mm 3mm">
<div>Túi khí, đai an toàn: kéo dài ${fw} người dừng lại, lực lên người ${fp(25, '.')}</div>
<div>Găng tay đấm bốc, võ sĩ lùi theo cú đấm: cùng ${m('\\Delta p')}, ${m('\\Delta t')} ${fp(25, '.')}</div>
<div>Ngã trên băng: lăn người theo đà thay vì ${fp(34, '.')}</div>
<div>Đóng đinh: mặt búa cứng, ${m('\\Delta t')} rất ${fw} nên lực lên đinh ${fp(25, '.')}</div></div>
${h3(5, 'Thử sức đổi chiều: biết lực, tìm tốc độ bật lại')}
${box(wl(`Bóng ở tr.&nbsp;${tr(4)} bay tới tường ${u('12', 'm/s')}, chạm ${u('0{,}05', 's')}, tường đẩy bóng lực trung bình ${u('150', 'N')}. Tìm tốc độ bóng bật lại.`, 3))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Động lượng một vật: đổi đơn vị, xét dấu',
    de: `Xe tải ${nw(m('1{,}5')+' tấn')} chạy ${u('54', 'km/h')}; ô tô con ${u('750', 'kg')} ngược chiều ${u('72', 'km/h')} (mốc: mặt đường).<br><b>a)</b> động lượng của xe tải &nbsp; <b>b)</b> động lượng của ô tô con (dấu theo chiều (+) ở hình)<br><b>c)</b> xe nào có động lượng với độ lớn lớn hơn`,
    nd: `Đổi tấn, km/h ra ${fp(25, ';')} ngược chiều dương thì ${m('v')} mang dấu ${fn}`, a: ['a', 'b', 'c'], gi: 5, fig: H.xeDuong(''), cot: 3 },
  { t: 'Dạng 2 · Dễ · Xung lượng của lực và tốc độ vật thu được',
    de: `Khí thuốc súng đẩy viên đạn ${u('10', 'g')} đang đứng yên bằng lực trung bình ${u('9000', 'N')} trong ${u('1{,}0', 'ms')}.<br><b>a)</b> xung lượng của lực đẩy &nbsp; <b>b)</b> tốc độ đạn khi ra khỏi nòng<br><b>c)</b> cùng lực, đẩy chỉ ${u('0{,}50', 'ms')}: tốc độ ra khỏi nòng`,
    nd: `Đổi g ra ${fw}, ms ra ${fp(25, ';')} ${m('F\\Delta t=mv_2-')} ${fn}`, a: ['a', 'b', 'c'], gi: 4 },
  { t: 'Dạng 3 · Trung bình · Động lượng của hệ hai vật theo góc',
    de: `Hai xe trên sàn nhẵn (vận tốc đo đối với sàn): xe 1 ${u('50', 'kg')}, ${u('6{,}0', 'm/s')}; xe 2 ${u('80', 'kg')}, ${u('5{,}0', 'm/s')}.<br>Độ lớn động lượng của hệ khi <b>a)</b> ngược chiều trên cùng đường thẳng<br><b>b)</b> trên hai đường vuông góc &nbsp; <b>c)</b> hai vận tốc hợp nhau góc ${m('60^\\circ')} (${nw(m('\\cos 60^\\circ=0{,}5'))})`,
    nd: `Tính ${m('p_1, p_2')} trước; cộng ${fw}, không cộng ${fp(25, '.')}`, a: ['a', 'b', 'c'], gi: 5 },
  { t: 'Dạng 4 · Trung bình · Độ biến thiên động lượng khi bật ngược lại',
    de: `Bóng cao su ${u('0{,}10', 'kg')} lăn trên sàn nhẵn, đập vuông góc vào vách cứng với tốc độ ${u('4{,}0', 'm/s')}.<br><b>a)</b> bật ngược lại cùng tốc độ ${u('4{,}0', 'm/s')}; chiều dương là chiều tới vách: ${m('\\Delta p')}<br><b>b)</b> tới ${u('4{,}0', 'm/s')}, bật lại ${u('3{,}0', 'm/s')} (chiều dương như a): ${m('\\Delta p')}<br><b>c)</b> ở ý a, chọn chiều dương là chiều bật ra: ${m('\\Delta p')}`,
    nd: `Bật ngược lại thì ${m('v_1, v_2')} ${fp(25, ';')} ${m('\\Delta p=m(')}${fw}${m(')')}`, a: ['a', 'b', 'c'], gi: 8, fig: H.bongTuong('4,0 m/s', '? m/s', '', 180), cot: 3 },
  { t: 'Dạng 5 · Khó · Lực trung bình từ độ biến thiên động lượng',
    de: `Thủ môn bắt bóng ${u('0{,}40', 'kg')} bay ngang ${u('20', 'm/s')}, giữ bóng dừng hẳn; lực của tay nằm ngang, bỏ qua trọng lượng bóng; chiều dương là chiều bay.<br><b>a)</b> tay giữ cứng, dừng sau ${u('0{,}010', 's')}: lực trung bình của tay<br><b>b)</b> tay co lại theo bóng, dừng sau ${u('0{,}050', 's')}: lực trung bình<br><b>c)</b> lực ở b bằng mấy lần lực ở a? Vì sao co tay thì đỡ đau?`,
    nd: `Hai ý cùng ${m('\\Delta p')} vì ${fp(34, ';')} chỉ ${m('\\Delta t')} đổi nên ${m('F=')} ${fw}`, a: ['a', 'b', 'c'], gi: 8, cot: 3 },
];

// Bài tương tự: mỗi dạng 2 bài đặt cạnh nhau (2 cột), GIẢI VÀO VỞ (thầy chốt 10/11): giấy chỉ in đề + ô đáp số; đáp số Python in lật ngược.
const ttCss2 = `<style>.tt:has(.tt2)>.hd>span:last-child{display:none}.tt2{display:grid;grid-template-columns:1fr 1fr;gap:0 4mm}.tt2>div{min-width:0}
.tt2 .h2{display:flex;justify-content:space-between;align-items:center;font-weight:700;color:var(--navy);border-bottom:.2mm solid var(--grid);margin-bottom:.3mm}
.tt2 .h2>span:last-child{font-weight:400;color:var(--ink);white-space:nowrap}.tt2 .q{margin-top:.5mm}</style>`;
const okS = '<span><span class="ck"></span>đúng &nbsp;<span class="ck"></span>sai, đã sửa</span>';
const bai = (stmt, ys, o = ys.map((y) => y[0])) => `<div>${stmt}</div>` + ys.map(([lab, q]) => `<div class="q"><b>${lab})</b> ${q}</div>`).join('') + dapSo(o);
const NHAP = [2, 8]; // số dòng nháp cuối tr.8, tr.9 — đổ cho dư 0–15 mm
const nhap = (n) => `<div style="margin-top:2mm;border-top:.3mm solid var(--grid);padding-top:.8mm"><b>Nháp / chỗ em còn vướng</b>${lines(n)}</div>`;
const hai = (a, b, css = '') => `${css}<div class="tt2">${[a, b].map((x, i) => `<div><div class="h2"><span>Bài ${i + 1}</span>${okS}</div>${x}</div>`).join('')}</div>`;
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–3', 'DẠNG 4–5'],
  trang: [[
    { t: 'Dạng 1 · Động lượng một vật, xét dấu', k: 0, de: hai(
      bai(`Xe máy cùng người ${u('120', 'kg')} chạy ${u('36', 'km/h')}; xe đạp cùng người ${u('60', 'kg')} chạy ngược chiều ${u('18', 'km/h')}. Chiều dương là chiều xe máy.`, [['a', 'Động lượng xe máy?'], ['b', 'Động lượng xe đạp (kể cả dấu)?']]),
      bai(`Bi ${u('20', 'g')} lăn ${u('0{,}5', 'm/s')}; bóng bàn ${u('2{,}7', 'g')} bay ${u('15', 'm/s')} ngược chiều bi. Chiều dương là chiều bi.`, [['a', 'Động lượng của bi?'], ['b', 'Động lượng bóng bàn (kể cả dấu)?'], ['c', 'Vật nào có động lượng lớn hơn về độ lớn?']]), ttCss2) },
    { t: 'Dạng 2 · Xung lượng và tốc độ thu được', k: 0, de: hai(
      bai(`Gậy golf đánh quả bóng ${u('46', 'g')} đang đứng yên bằng lực trung bình ${u('2300', 'N')} trong ${u('1{,}0', 'ms')}.`, [['a', 'Xung lượng của lực?'], ['b', 'Tốc độ bóng ngay sau cú đánh?']]),
      bai(`Xe đồ chơi ${u('0{,}50', 'kg')} đứng yên trên sàn nhẵn, được đẩy ngang bằng lực ${u('4{,}0', 'N')} trong ${u('0{,}25', 's')}.`, [['a', 'Xung lượng của lực?'], ['b', 'Tốc độ xe sau đó?'], ['c', `Cùng lực, muốn xe đạt ${u('3{,}0', 'm/s')} thì đẩy bao lâu?`]])) },
    { t: 'Dạng 3 · Động lượng của hệ hai vật', k: 0, de: hai(
      bai(`Xe 1: ${u('2{,}0', 'kg')}, ${u('3{,}0', 'm/s')}; xe 2: ${u('3{,}0', 'kg')}, ${u('2{,}0', 'm/s')}. Độ lớn động lượng của hệ khi hai xe chạy`, [['a', 'cùng chiều?'], ['b', 'ngược chiều?'], ['c', 'vuông góc?']]),
      bai(`Bi 1: ${u('1{,}0', 'kg')}, ${u('4{,}0', 'm/s')}; bi 2: ${u('1{,}5', 'kg')}, ${u('2{,}0', 'm/s')}. Độ lớn động lượng của hệ khi hai vận tốc hợp nhau góc (${nw(m('\\cos 60^\\circ=0{,}5'))}, ${nw(m('\\cos 120^\\circ=-0{,}5'))})`, [['a', `${m('90^\\circ')}?`], ['b', `${m('60^\\circ')}?`], ['c', `${m('120^\\circ')}?`]])) + nhap(NHAP[0]) },
  ], [
    { t: 'Dạng 4 · Độ biến thiên động lượng khi bật ngược lại', k: 0, de: hai(
      bai(`Bóng ${u('0{,}20', 'kg')} đập vuông góc vào tường với tốc độ ${u('5{,}0', 'm/s')}. Chiều dương là chiều tới tường.`, [['a', `Bật ngược lại cùng tốc độ ${u('5{,}0', 'm/s')}: ${m('\\Delta p')}?`], ['b', `Bật lại với ${u('2{,}0', 'm/s')}: ${m('\\Delta p')}?`]]),
      bai(`Bóng rổ ${u('0{,}60', 'kg')} rơi chạm sàn với tốc độ ${u('6{,}0', 'm/s')}, nảy thẳng lên với ${u('4{,}0', 'm/s')}. Chiều dương hướng lên.`, [['a', `Vận tốc trước (a<sub>1</sub>) và sau (a<sub>2</sub>) va chạm, kể cả dấu?`], ['b', `${m('\\Delta p')}?`], ['c', `Bóng không nảy (dính sàn): ${m('\\Delta p')}?`]], ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'])) },
    { t: 'Dạng 5 · Lực trung bình', k: 0, de: hai(
      bai(`Ô tô ${u('1000', 'kg')} đang chạy ${u('20', 'm/s')} thì phanh, dừng hẳn sau ${u('4{,}0', 's')}. Chiều dương là chiều chạy.`, [['a', `${m('\\Delta p')} của ô tô?`], ['b', 'Lực hãm trung bình (kể cả dấu)?']]),
      bai(`Người ${u('60', 'kg')} nhảy xuống, chạm đất với tốc độ ${u('6{,}0', 'm/s')} rồi dừng hẳn. Tính độ lớn hợp lực trung bình lên người khi`, [['a', `chân thẳng, dừng sau ${u('0{,}05', 's')}?`], ['b', `gập gối, dừng sau ${u('0{,}30', 's')}?`], ['c', 'Lực ở a gấp mấy lần lực ở b?']])) + nhap(NHAP[1]) },
  ]],
  dap: [
    'D1·1: a) 1200 kg·m/s · b) −300 kg·m/s &nbsp;|&nbsp; D1·2: a) 0,010 kg·m/s · b) −0,0405 kg·m/s · c) bóng bàn &nbsp;|&nbsp; D2·1: a) 2,3 N·s · b) 50 m/s &nbsp;|&nbsp; D2·2: a) 1,0 N·s · b) 2,0 m/s · c) 0,375 s &nbsp;|&nbsp; D3·1: a) 12 · b) 0 · c) ≈ 8,5 kg·m/s &nbsp;|&nbsp; D3·2: a) 5,0 · b) ≈ 6,1 · c) ≈ 3,6 kg·m/s',
    'D4·1: a) −2,0 kg·m/s · b) −1,4 kg·m/s &nbsp;|&nbsp; D4·2: a<sub>1</sub>) −6,0 m/s · a<sub>2</sub>) +4,0 m/s · b) 6,0 kg·m/s · c) 3,6 kg·m/s &nbsp;|&nbsp; D5·1: a) −20 000 kg·m/s · b) −5000 N &nbsp;|&nbsp; D5·2: a) 7200 N · b) 1200 N · c) 6 lần',
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 2], kq: [[1, 2, 3], [4, 5]] },
  tuongTu,
  tra: 'động lượng 1·4 · thí nghiệm bi 1·5 · hệ nhiều vật 2·1 · xung lượng 2·2 · đệm lò xo 2·3 · bẫy 3·1 · dạng 1–3 → 6·1 · dạng 4–5 → 7·1',
  out: process.argv[2],
});
