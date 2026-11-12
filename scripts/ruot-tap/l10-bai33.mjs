// Ruột tập VL10 – Bài 33 · Biến dạng của vật rắn (lesson id 78). Quyển Chương 7 lớp 10: bài 33 = tr. 1–12.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự (giải vào vở) · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l10-bai33.mjs (toàn bộ SVG tự vẽ, không dùng ảnh Halliday). Nội dung theo bài web (book/cache/78.json, tải từ DB 12/11/2026):
// mục tiêu, dự đoán cân treo, II.1–II.3, ba thí nghiệm (bút bi, đo k, hai lò xo), ba bẫy, Trả bài 6 câu, bài toán mẫu, thử thách, 5 dạng BTM.
// Đáp số Bài tương tự (tuongTu.dap) và bài toán mẫu tính bằng Python 12/11/2026. g = 10 m/s² in sẵn ở mọi đề cần trọng lượng.
// Chạy: node scripts/ruot-tap/l10-bai33.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl10-bai33.pdf
//       node scripts/ruot-tap/l10-bai33.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l10-bai33/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL10b33 as H } from './hinh-l10-bai33.mjs';

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
  const out = resolve(HERE, 'out/hinh-l10-bai33'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 33, lid: 78, ten: 'BIẾN DẠNG CỦA VẬT RẮN', lop: 10, baiDau: 33, sub: 'Vật lí 10 · Chương 7: Biến dạng của vật rắn. Áp suất chất lỏng' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const g10 = nw(m('g=10\\ \\mathrm{m/s^2}'));
const dl = m('|\\Delta l|'), Fdh = m('F_{\\text{đh}}'), l0 = m('l_0');
const u = (s) => nw(m(`\\mathrm{${s}}`));

const ttHaiCot = '<style>.bt>.gi{display:grid;grid-template-columns:1fr 1fr;column-gap:4mm}.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm}.yo .oo{flex:none;display:flex;gap:3mm}.yo{line-height:1.35}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}.bng td,.bng th{padding:0 1.5mm;line-height:1.18;text-align:center}</style>';
const p1 = `${ttHaiCot}<section class="page">
${head('BÀI 33 · BIẾN DẠNG CỦA VẬT RẮN', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Phân biệt biến dạng <b>kéo</b> – <b>nén</b>; biến dạng <b>đàn hồi</b> – <b>dẻo</b>`)}
${dong(`${ck}Nêu điểm đặt, phương, chiều của <b>lực đàn hồi</b> của lò xo`)}
${dong(`${ck}Phát biểu và dùng <b>định luật Hooke</b>; biết khi nào định luật hết đúng`)}
${dong(`${ck}Tránh ba lỗi hay gặp khi tính với lò xo`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<div class="fig-side" style="${fs(46)}"><div>
<p style="margin:0 0 1mm">Lò xo dài ${u('20\\ cm')}. Treo 1 túi cam ${u('200\\ g')}, lò xo dài ${u('22\\ cm')}. Treo 2 túi như thế, lò xo dài bao nhiêu?</p>
${opt('A', `${u('44\\ cm')}, vì treo gấp đôi`)}
${opt('B', `${u('24\\ cm')}, vì phần dài thêm gấp đôi`)}
${opt('C', `${u('22\\ cm')}, lò xo đã dãn hết cỡ`)}
${opt('D', `${u('40\\ cm')}, gấp đôi chiều dài ban đầu`)}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 1)}</div>
${H.canTreo()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Biến dạng kéo, nén — đàn hồi, dẻo', '1·4')}
<div class="card fig-side" style="${fs(44)};padding:1.2mm 3mm"><div>
<div>Cặp lực ngược chiều, vuông góc bề mặt vật:</div>
<div><b>Kéo:</b> lực hướng ${f(18)} vật → vật ${f(18)}</div>
<div><b>Nén:</b> lực hướng ${f(18)} vật → vật ${f(18)}</div>
<div><b>Đàn hồi:</b> thôi lực, vật ${f(42)}</div>
<div><b>Dẻo:</b> thôi lực, vật ${f(42)}</div>
<div><b>Giới hạn đàn hồi:</b> mức lực ${f(20)} mà vật còn đàn hồi</div></div>
${H.keoNen()}</div>
${h3(5, 'Thí nghiệm: chiếc lò xo bút bi', '1·5')}
<div class="card fig-side" style="${fs(42)};padding:1.2mm 3mm"><div>
<div><b>Làm:</b> kéo nhẹ hai đầu lò xo bút bi rồi thả; sau đó kéo thật mạnh rồi thả.</div>
<div><b>Rút ra:</b> kéo nhẹ → biến dạng ${f(22)}; kéo mạnh, vượt ${f(32)} → biến dạng ${f(18)}.</div>
</div>
${H.butBi()}</div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('LỰC ĐÀN HỒI CỦA LÒ XO · ĐỊNH LUẬT HOOKE')}
${h3(1, 'II.2 · Lực đàn hồi của lò xo', '2·1')}
<div class="card fig-side" style="${fs(48)};padding:1.2mm 3mm"><div>
<div>Xuất hiện khi lò xo ${f(25)}, có xu hướng đưa lò xo về ${f(30)}.</div>
<div><b>Điểm đặt:</b> lên ${f(40)}</div>
<div><b>Phương:</b> ${f(36)}</div>
<div><b>Chiều:</b> ${f(36)}</div>
<div>Lò xo dãn → ${f(14)} vật về phía lò xo.</div>
<div>Lò xo nén → ${f(14)} vật ra xa lò xo.</div>
<div style="margin-top:.6mm">Ngồi lên yên xe đạp: lò xo yên bị ${f(14)}, lực đàn hồi hướng ${f(14)}.</div></div>
${H.lucDH()}</div>
${h3(2, 'II.3 · Định luật Hooke', '2·2')}
<div class="card" style="padding:1.2mm 3mm">
<div>Trong ${f(32)}, độ lớn lực đàn hồi của lò xo ${f(30)} với độ biến dạng.</div>
<div style="margin:.8mm 0;text-align:center">${Fdh} ${m('=')} ${f(22)} &nbsp;&nbsp;&nbsp; ${dl} ${m('=')} ${f(22)}</div>
<table><tr><th style="width:16mm">Kí hiệu</th><th>Tên gọi</th><th style="width:18mm">Đơn vị</th></tr>
<tr><td>${Fdh}</td><td></td><td></td></tr>
<tr><td>${m('k')}</td><td></td><td></td></tr>
<tr><td>${m('\\Delta l')}</td><td></td><td></td></tr>
<tr><td>${m('l')}</td><td></td><td></td></tr>
<tr><td>${l0}</td><td></td><td></td></tr></table>
<div style="margin-top:.8mm">${m('k')} là của riêng từng lò xo, phụ thuộc: ${f(56)}</div></div>
${h3(3, 'Làm nhanh', '2·3')}
${box(cau(`<b>Câu 1.</b> Chân ghế khi em ngồi lên, dây chun buộc tóc đang căng, dây cáp treo thang máy: vật nào bị nén? Vì sao?`, 2)
 + cau(`<b>Câu 2.</b> Kéo móc lực kế bằng lực ${u('3\\ N')} thì lò xo bên trong dãn ${u('6\\ cm')}. Tính độ cứng của lò xo.`, 2)
 + cau(`<b>Câu 3.</b> Lò xo dài tự nhiên ${u('30\\ cm')}, ${nw(`${m('k=100')}&nbsp;N/m`)}, bị ép hai đầu còn dài ${u('26\\ cm')}. Độ lớn lực đàn hồi?`, 2))}
${foot(2)}</section>`;

const row = (F, l) => `<tr><td>${F}</td><td>${l}</td><td></td><td></td></tr>`;
const p3 = `<section class="page">
${head('THÍ NGHIỆM ĐO ĐỘ CỨNG · BA CÁI BẪY')}
${h3(1, 'Thí nghiệm: tìm độ cứng k', '3·1')}
<div class="fig-side" style="${fs(44)}"><div>
<div style="margin-bottom:.6mm">${nw(`${m('l_0=10{,}0')}&nbsp;cm`)}; treo 1…5 quả ${u('50\\ g')}, mỗi quả nặng ${nw(`${m('0{,}49')}&nbsp;N`)}.</div>
<table class="tbl-ct bng"><tr><th>${m('F')} (N)</th><th>${m('l')} (cm)</th><th style="width:14mm">${m('\\Delta l')} (cm)</th><th style="width:20mm">${m('F/|\\Delta l|')} (N/m)</th></tr>
${row('0,49', '11,9')}${row('0,98', '13,9')}${row('1,47', '15,9')}${row('1,96', '17,9')}${row('2,45', '19,8')}</table>
</div>
${H.doThi()}</div>
<div class="card" style="margin-top:.6mm;padding:1mm 3mm">
<div>Trung bình ${nw(`${m('k\\approx')} ${f(14)}&nbsp;N/m`)}. Hàng lệch nhiều nhất: ${f(14)}; vì sao?</div>${lines(1)}
<div><b>Rút ra:</b> các điểm nằm trên ${f(22)} qua gốc ⇒ ${m('F')} ${f(22)} với ${m('\\Delta l')}.</div>
<div>Cùng quả ${u('100\\ g')}: lò xo dây to dãn ${f(12)}, dây mảnh dãn ${f(12)} ⇒ ${m('k')} do ${f(16)} quyết định.</div></div>
${h3(2, 'III · Ba cái bẫy hay sập', '3·2')}
<div class="card" style="padding:1mm 3mm">
<div class="trap">${ck}<span><b>“Lấy chiều dài ${m('l')}.”</b> Lực tỉ lệ với phần dài thêm/ngắn đi ${nw(`${m('|\\Delta l|=|l-l_0|')},`)} không với cả ${m('l')}.</span></div>
<div class="trap">${ck}<span><b>“Kéo mạnh thì ${m('k')} lớn hơn.”</b> ${m('F')} tăng thì ${m('\\Delta l')} tăng đúng tỉ lệ; ${m('k')} thuộc về lò xo.</span></div>
<div class="trap">${ck}<span><b>“Hooke dùng cho mọi lực.”</b> Chỉ trong giới hạn đàn hồi; quá giới hạn, đồ thị cong, lò xo hỏng.</span></div></div>
${h3(3, 'IV · Trả bài 6 câu', '3·3')}
${box(`${tb('1. Kéo và nén khác nhau ở chiều cặp lực thế nào?')}${lines(1)}
${tb('2. Biến dạng đàn hồi, dẻo, giới hạn đàn hồi là gì?')}${lines(1)}
${tb('3. Lực đàn hồi của lò xo: điểm đặt, phương, chiều?')}${lines(2)}
${tb('4. Định luật Hooke: phát biểu, công thức, đơn vị.')}${lines(1)}
${tb('5. Độ biến dạng khác chiều dài thế nào?')}${lines(1)}
${tb('6. k phụ thuộc vào gì? Kéo mạnh hơn k có đổi?')}${lines(1)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/6 câu · chưa thuộc: ${f(25)} ${nw(`→ đọc lại ô ${f(12)} Tập`)}</div>
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('TỰ KIỂM TRA · BÀI TOÁN MẪU')}
${h3(1, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '4·1')}
${rkHai([1, 2, 3], [4, 5, 6])}
${h3(2, 'V · Bài toán mẫu: lò xo treo thẳng đứng', '4·2')}
<div class="card soft" style="padding:1.2mm 3mm">Một lò xo nhẹ treo thẳng đứng, chiều dài tự nhiên ${u('25\\ cm')}. Treo vật ${u('200\\ g')}, khi vật đứng yên lò xo dài ${u('29\\ cm')}. Lấy ${g10}, lò xo luôn trong giới hạn đàn hồi.
<div><b>a)</b> Tính độ cứng.</div><div><b>b)</b> Treo thêm vật ${u('300\\ g')} nữa thì lò xo dài bao nhiêu?</div><div><b>c)</b> Muốn lò xo dài ${u('32\\ cm')} phải treo tổng cộng bao nhiêu gam?</div></div>
${h3(3, 'Phân tích đề')}
<table><tr><th style="width:50mm">Câu trong đề</th><th>Dữ liệu → kiến thức</th></tr>
<tr><td>“lò xo nhẹ treo thẳng đứng”</td><td>bỏ qua khối lượng lò xo; lực đàn hồi hướng lên</td></tr>
<tr><td style="height:6.5mm">“vật 200 g … đứng yên”</td><td></td></tr>
<tr><td style="height:6.5mm">“tự nhiên 25 cm … dài 29 cm”</td><td></td></tr>
<tr><td style="height:6.5mm">“treo thêm 300 g nữa”</td><td></td></tr>
<tr><td style="height:6.5mm">“trong giới hạn đàn hồi”</td><td></td></tr></table>
${h3(4, 'Giải')}
<div class="fig-side" style="${fs(42)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl(`a) ${Fdh} và ${dl}:`, 2)}${wl(`&nbsp;&nbsp;&nbsp; độ cứng ${m('k')}:`, 1)}${wl('b) Tổng khối lượng, lực, độ dãn:', 2)}${wl(`&nbsp;&nbsp;&nbsp; chiều dài ${m('l')}:`, 1)}${wl(`c) ${dl}, lực, khối lượng:`, 2)}${wl('Kiểm tra: cứ 50 g dãn thêm bao nhiêu cm?', 1)}</div>${H.treo({ l0: '25 cm', l: '29 cm', m: '200 g', h0: 100, h: 116, cap: 'Bên trái (nét đứt): lò xo chưa treo.' })}</div>
${h3(5, 'Điền bước còn thiếu: lò xo bị nén')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div style="padding-top:.8mm;line-height:1.35">Cùng lò xo (${nw(`${m('k=50')}&nbsp;N/m`)}, ${nw(`${m('l_0=25')}&nbsp;cm`)}), dựng đứng trên bàn, đặt vật ${u('300\\ g')} lên đầu trên (${g10}).</div>
<div class="ln"><b>Bước 1 (cho sẵn):</b> vật đứng yên, ${nw(`${m('F_{\\text{đh}}=mg=3')}&nbsp;N`)}, hướng lên.</div>
${wl(`Bước 2: ${dl} ${m('=')}`, 1)}${wl(`Bước 3: ${m('l=')} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span style="font-weight:400">(cộng hay trừ? vì sao)</span>`, 1)}</div>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TẬP VỀ NHÀ · THỬ THÁCH · MANG VỀ')}
${K.btvn()}
${h3(2, 'Thử thách phân tầng', '5·2')}
<div class="fig-side" style="${fs(38)}">${box(wl(`${m('\\bigstar')} Lò xo ${nw(`${m('k=200')}&nbsp;N/m`)} bị kéo dãn ${u('3\\ cm')}. Lực đàn hồi?`, 3)
 + wl(`${m('\\bigstar\\bigstar')} Lò xo ${nw(`${m('k=100')}&nbsp;N/m`)} cắt đôi thành hai nửa giống nhau. Treo ${u('1\\ N')} vào một nửa thì nửa đó dãn bao nhiêu? Độ cứng một nửa?`, 4)
 + wl(`${m('\\bigstar\\bigstar\\bigstar')} Treo vật ${u('200\\ g')} vào lò xo ${nw(`${m('k=50')}&nbsp;N/m`)} trong thang máy đi lên nhanh dần, ${nw(m('a=2\\ \\mathrm{m/s^2}'))}; ${g10}. Lò xo dãn bao nhiêu? So với lúc thang đứng yên?`, 4))}${H.thangMay()}</div>
${h3(3, 'Câu đổi chiều: biết hai chiều dài, tìm l<sub>0</sub> và k', '5·3')}
${box(wl(`Treo ${u('100\\ g')}, lò xo dài ${u('22\\ cm')}; treo ${u('300\\ g')}, dài ${u('26\\ cm')} (${g10}). Tìm ${m('k')} và ${l0}. Gợi ý: phần lực chênh gây ra phần dài chênh.`, 5))}
${h3(4, 'VI · Mang về: điều em dễ quên nhất', '5·4')}
${box(wl('1.', 3) + wl('2.', 3) + wl('3.', 3))}
${foot(5)}</section>`;

const bangD1 = `<table class="bng" style="margin:.2mm 0"><tr><th style="text-align:left">${m('F')} (N)</th><td>2</td><td>4</td><td>6</td><td>8</td><td>10</td></tr>
<tr><th style="text-align:left">${m('l')} (cm), khi có lực</th><td>22</td><td>24</td><td>26</td><td>28</td><td>33</td></tr>
<tr><th style="text-align:left">${m("l'")} (cm), sau khi thôi lực</th><td>20</td><td>20</td><td>20</td><td>20</td><td>22</td></tr></table>`;
const dang = [
  { t: 'Dạng 1 · Dễ · Nhận biết kéo, nén, đàn hồi, dẻo, giới hạn đàn hồi',
    de: `Lò xo dài tự nhiên ${u('20\\ cm')}, một đầu gắn tường, bị kéo ra xa tường bằng lực ${m('F')} tăng dần qua 5 lần thử:`,
    bang: `${bangD1}<div><b>a)</b> lò xo bị biến dạng kéo hay nén</div><div><b>b)</b> lần thử nào lò xo bị biến dạng dẻo</div><div><b>c)</b> lực lớn nhất còn đàn hồi (c<sub>1</sub>); giới hạn đàn hồi nằm trong khoảng nào (c<sub>2</sub>)</div>`,
    nd: `Đàn hồi hay dẻo: so ${m("l'")} với ${f(14)} sau khi ${f(18)}`, a: ['a', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'], gi: 4 },
  { t: 'Dạng 2 · Dễ · Định luật Hooke: tìm k, độ dãn, lực',
    de: `Lò xo nhẹ, một đầu cố định, bị kéo bằng lực ${u('6{,}0\\ N')} thì dãn thêm ${u('4{,}0\\ cm')}; luôn trong giới hạn đàn hồi.<br><b>a)</b> độ cứng ${m('k')}<br><b>b)</b> kéo bằng ${u('9{,}0\\ N')}: dãn thêm bao nhiêu cm<br><b>c)</b> muốn dãn thêm ${u('2{,}0\\ cm')}: lực bao nhiêu`,
    nd: `đổi ${f(10)} ra ${f(10)} trước khi thế; ${m('k')} ${f(22)} khi lực đổi`, a: ['a', 'b', 'c'], gi: 4 },
  { t: 'Dạng 3 · Trung bình · Chiều dài lò xo khi bị kéo hoặc bị nén',
    de: `Lò xo nhẹ nằm ngang gắn tường, ${nw(`${m('l_0=24')}&nbsp;cm`)}, ${nw(`${m('k=120')}&nbsp;N/m`)}; luôn trong giới hạn đàn hồi.<br><b>a)</b> chiều dài khi kéo đầu tự do bằng ${u('3{,}6\\ N')}<br><b>b)</b> chiều dài khi đẩy đầu tự do về phía tường bằng ${u('4{,}8\\ N')}<br><b>c)</b> muốn lò xo dài ${u('30\\ cm')}: lực kéo bao nhiêu`,
    nd: `kéo: ${m('l=l_0')} ${f(8)} ${dl} · nén: ${m('l=l_0')} ${f(8)} ${dl}`, a: ['a', 'b', 'c'], gi: 3, fig: H.ngang() },
];
const dang45 = [
  { t: 'Dạng 4 · Khó · Lò xo treo vật đứng yên: k, chiều dài, khối lượng',
    de: `Lò xo nhẹ ${nw(`${m('l_0=20')}&nbsp;cm`)}, treo thẳng đứng, đầu trên cố định. Treo vật ${u('120\\ g')}; khi vật đứng yên lò xo dài ${u('23\\ cm')}. ${g10}, luôn trong giới hạn đàn hồi.<br><b>a)</b> độ cứng ${m('k')}<br><b>b)</b> treo thêm vật ${u('80\\ g')} nữa: lò xo dài bao nhiêu<br><b>c)</b> phải treo thêm bao nhiêu gam nữa (so với vật ${u('120\\ g')}) để lò xo dài ${u('32\\ cm')}`,
    nd: `vật đứng yên ⇒ ${Fdh} ${m('=')} ${f(14)}; “treo thêm” là ${f(18)} khối lượng`, a: ['a', 'b', 'c'], gi: 8, fig: H.treo({ l0: '20 cm', l: '23 cm', m: '120 g', h0: 100, h: 115 }) },
  { t: 'Dạng 5 · Khó · Bài ngược: biết hai chiều dài, tìm l<sub>0</sub> và k',
    de: `Lò xo nhẹ treo thẳng đứng. Treo vật ${u('160\\ g')}, lò xo dài ${u('24\\ cm')}; treo thêm để tổng là ${u('480\\ g')}, lò xo dài ${u('28\\ cm')}. ${g10}, luôn trong giới hạn đàn hồi; chưa biết ${l0} và ${m('k')}.<br><b>a)</b> độ cứng ${m('k')}<br><b>b)</b> chiều dài tự nhiên ${l0}<br><b>c)</b> chỉ treo vật ${u('400\\ g')}: lò xo dài bao nhiêu`,
    nd: `trừ hai phương trình Hooke ⇒ ${l0} ${f(18)}: ${m('k=\\Delta F/')} ${f(16)}`, a: ['a', 'b', 'c'], gi: 8, fig: H.haiLan() },
];

// Bài tương tự (giải vào vở, thầy chốt 10/11): 1 cột; ô đáp số đặt cuối dòng của ý, nhãn khớp a) b) c)…; đáp số in ngược cuối trang.
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
    { t: 'Dạng 1 · Bài 1', de: `Dây chun dài tự nhiên ${u('10\\ cm')}. Kéo hai đầu bằng lực ${nw(`${m('F=1;\\ 2;\\ 3;\\ 4')}&nbsp;N`)}; sau mỗi lần thôi lực, dây dài lần lượt ${nw(`${m('10;\\ 10;\\ 10;\\ 11{,}5')}&nbsp;cm`)}.<br><b>a)</b> dây bị biến dạng kéo hay nén<br><b>b)</b> lần thử nào dây bị biến dạng dẻo<br><b>c)</b> lực lớn nhất còn đàn hồi; giới hạn đàn hồi trong khoảng nào`, o: ['a', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'], ow: 25 },
    { t: 'Dạng 1 · Bài 2', de: `Ghi kéo/nén hoặc đàn hồi/dẻo:<br><b>a)</b> dây cáp cần cẩu đang nâng hàng<br><b>b)</b> cột nhà đỡ mái<br><b>c)</b> lò xo giảm xóc khi xe qua ổ gà<br><b>d)</b> kẹp giấy bị bẻ cong, thả ra không thẳng lại`, o: ['a', 'b', 'c', 'd'] },
    { t: 'Dạng 2 · Bài 1', de: `Lò xo dãn ${u('2{,}5\\ cm')} khi chịu lực kéo ${u('4{,}0\\ N')}; luôn trong giới hạn đàn hồi.<br><b>a)</b> độ cứng ${m('k')}<br><b>b)</b> kéo bằng ${u('10\\ N')}: dãn bao nhiêu cm<br><b>c)</b> dãn ${u('1{,}5\\ cm')}: lực kéo bao nhiêu`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 2 · Bài 2', de: `Lò xo trong một lực kế có ${nw(`${m('k=200')}&nbsp;N/m`)}.<br><b>a)</b> kéo móc bằng ${u('5{,}0\\ N')}: lò xo dãn bao nhiêu cm<br><b>b)</b> lò xo dãn ${u('4{,}0\\ cm')}: lực kéo bao nhiêu<br><b>c)</b> các vạch chia cách nhau ${u('1\\ cm')}: mỗi vạch ứng với bao nhiêu N`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 3 · Bài 1', de: `Lò xo nằm ngang, một đầu gắn tường, ${nw(`${m('l_0=30')}&nbsp;cm`)}, ${nw(`${m('k=80')}&nbsp;N/m`)}.<br><b>a)</b> kéo đầu tự do bằng ${u('2{,}4\\ N')}: chiều dài<br><b>b)</b> đẩy về phía tường bằng ${u('4{,}0\\ N')}: chiều dài<br><b>c)</b> muốn lò xo dài ${u('27\\ cm')}: kéo hay đẩy, lực bao nhiêu`, fig: H.ngang({ l0: 30 }), fw: 40, o: ['a', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'], ow: 16 },
    { t: 'Dạng 3 · Bài 2', de: `Lò xo ${nw(`${m('l_0=15')}&nbsp;cm`)}, ${nw(`${m('k=50')}&nbsp;N/m`)}, luôn trong giới hạn đàn hồi.<br><b>a)</b> lò xo bị kéo dài thành ${u('18\\ cm')}: lực đàn hồi<br><b>b)</b> lò xo bị nén còn ${u('12\\ cm')}: lực đàn hồi<br><b>c)</b> ép hai đầu bằng lực ${u('3{,}0\\ N')}: chiều dài lò xo`, o: ['a', 'b', 'c'] },
  ], [
    { t: 'Dạng 4 · Bài 1', de: `Lò xo nhẹ ${nw(`${m('l_0=30')}&nbsp;cm`)} treo thẳng đứng. Treo vật ${u('250\\ g')}, khi đứng yên lò xo dài ${nw(`${m('35')}&nbsp;cm;`)} ${nw(`${g10}.`)}<br><b>a)</b> độ cứng ${m('k')}<br><b>b)</b> treo thêm vật ${u('150\\ g')} nữa: chiều dài<br><b>c)</b> muốn lò xo dài ${u('40\\ cm')}: treo tổng cộng bao nhiêu gam`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 4 · Bài 2', de: `Lò xo nhẹ ${nw(`${m('k=100')}&nbsp;N/m`)}, ${nw(`${m('l_0=20')}&nbsp;cm`)}, dựng đứng trên bàn; đặt vật ${u('500\\ g')} lên đầu trên; ${nw(`${g10}.`)}<br><b>a)</b> độ biến dạng ${dl}<br><b>b)</b> chiều dài lò xo khi vật đứng yên<br><b>c)</b> treo ngược: đầu trên cố định, treo vật đó ở đầu dưới: chiều dài`, fig: H.nenBan(), fw: 36, o: ['a', 'b', 'c'] },
    { t: 'Dạng 5 · Bài 1', de: `Lò xo nhẹ treo thẳng đứng. Treo ${u('200\\ g')}: dài ${u('32\\ cm')}; treo tổng ${u('500\\ g')}: dài ${nw(`${m('38')}&nbsp;cm;`)} ${nw(`${g10}.`)}<br><b>a)</b> độ cứng ${m('k')}<br><b>b)</b> chiều dài tự nhiên ${l0}<br><b>c)</b> chỉ treo ${u('300\\ g')}: chiều dài`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 5 · Bài 2', de: `Lò xo nhẹ treo thẳng đứng. Treo ${u('120\\ g')}: dài ${u('22\\ cm')}; treo ${u('300\\ g')}: dài ${nw(`${m('25')}&nbsp;cm;`)} ${nw(`${g10}.`)}<br><b>a)</b> độ cứng ${m('k')}<br><b>b)</b> chiều dài tự nhiên ${l0}<br><b>c)</b> muốn lò xo dài ${u('26\\ cm')}: treo bao nhiêu gam`, o: ['a', 'b', 'c'] },
    nhap(13),
  ]],
  dap: [
    `D1·1: a) kéo · b) 4 N · c<sub>1</sub>) 3 N · c<sub>2</sub>) 3 N ${m("\\le")} gh &lt; 4 N &nbsp;|&nbsp; D1·2: a) kéo · b) nén · c) nén · d) dẻo &nbsp;|&nbsp; D2·1: a) 160 N/m · b) 6,25 cm · c) 2,4 N &nbsp;|&nbsp; D2·2: a) 2,5 cm · b) 8,0 N · c) 2,0 N &nbsp;|&nbsp; D3·1: a) 33 cm · b) 25 cm · c<sub>1</sub>) đẩy · c<sub>2</sub>) 2,4 N &nbsp;|&nbsp; D3·2: a) 1,5 N · b) 1,5 N · c) 9,0 cm`,
    `D4·1: a) 50 N/m · b) 38 cm · c) 500 g &nbsp;|&nbsp; D4·2: a) 5,0 cm · b) 15 cm · c) 25 cm &nbsp;|&nbsp; D5·1: a) 50 N/m · b) 28 cm · c) 34 cm &nbsp;|&nbsp; D5·2: a) 60 N/m · b) 20 cm · c) 360 g`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang: [...dang, ...dang45], tach: [3, 2], kq: [[1, 2, 3], [4, 5]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'biến dạng 1·4 · bút bi 1·5 · lực đàn hồi 2·1 · định luật Hooke 2·2 · đo k 3·1 · bẫy 3·2 · bài toán mẫu 4·2 · dạng 1–3 → 6·1 · dạng 4–5 → 7·1',
  out: process.argv[2],
});
