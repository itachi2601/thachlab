// Ruột tập VL10 – Bài 21 · Moment lực. Cân bằng của vật rắn (lesson id 66). Quyển Chương 3 lớp 10: bài 13 = tr. 1–12 → bài 21 = tr. 97–108.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự giải vào vở · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l10-bai21.mjs (SVG tự vẽ + ảnh thật búa nhổ đinh từ book/assets/anh-that). Nội dung theo bài web (book/cache/66.json, tải 13/11/2026):
// mục tiêu, dự đoán búa nhổ đinh, nhắc nhanh, II.1–II.4, ba thí nghiệm (mở cửa, thước có trục, thước trên bàn), ba bẫy, Trả bài 6 câu,
// bài toán mẫu thanh gỗ + túi gạo, thử sức đổi chiều, thử thách ⭐–⭐⭐⭐, 5 dạng bài tập mẫu. Đáp số Bài tương tự tính bằng Python 13/11/2026.
// Chạy: node scripts/ruot-tap/l10-bai21.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl10-bai21.pdf
//       node scripts/ruot-tap/l10-bai21.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l10-bai21/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL10b21 as H } from './hinh-l10-bai21.mjs';

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
  const out = resolve(HERE, 'out/hinh-l10-bai21'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 21, lid: 66, ten: 'MOMENT LỰC · CÂN BẰNG CỦA VẬT RẮN', lop: 10, baiDau: 13, sub: 'Vật lí 10 · Chương 3: Động lực học' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const Nm = '\\ \\mathrm{N\\cdot m}';
const u = (v, d) => nw(m(`${v}\\ \\mathrm{${d}}`));      // số + đơn vị không gãy dòng
const al = m('\\alpha');
const fx = (w = 12) => f(w);

const p1 = `<section class="page">
${head('BÀI 21 · MOMENT LỰC · CÂN BẰNG CỦA VẬT RẮN', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Tính được <b>tác dụng làm quay</b> của một lực đối với một trục`)}
${dong(`${ck}Dùng <b>quy tắc moment</b> cho vật có trục quay cố định`)}
${dong(`${ck}Nêu <b>hai điều kiện cân bằng</b> của vật rắn`)}
${dong(`${ck}Nhận ra <b>ngẫu lực</b> và tính moment của nó`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Minh ấn ${u('300', 'N')} mà đinh không nhúc nhích; anh Tuấn chỉ ấn ${u('150', 'N')} lại nhổ được đinh. Cả hai ấn vuông góc với cán. Điều gì quyết định tác dụng làm quay của lực?</p>
<div class="fig-side" style="${fs(50)}"><div>
${opt('A', 'Chỉ độ lớn của lực')}
${opt('B', 'Độ lớn của lực và khoảng cách từ trục quay tới giá của lực (đường thẳng chứa lực)')}
${opt('C', 'Khối lượng của cái búa')}
${opt('D', 'Tay ấn nhanh hay chậm')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 2)}</div>
${H.buaNhoDinh()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'Nhắc nhanh kiến thức cần dùng', '1·4')}
<div class="card soft" style="padding:1.2mm 3mm">
<div>Khoảng cách từ điểm ${m('O')} tới đường thẳng ${m('\\Delta')} = độ dài đoạn ${f(25)} kẻ từ ${m('O')} xuống ${m('\\Delta')}.</div>
<div>Tam giác vuông: cạnh đối = huyền × ${fx()} · cạnh kề = huyền × ${fx()}</div>
<div>Thử: ${nw(m('OA=0{,}4\\ \\mathrm m'))}, ${m('\\Delta')} qua ${m('A')} hợp với ${m('OA')} góc ${m('30^\\circ')}: khoảng cách từ ${m('O')} tới ${m('\\Delta')} = ${fx()} m</div></div>
${h3(5, 'II.1 · Moment lực', '1·5')}
<div class="card" style="padding:1.2mm 3mm">
<div>Moment lực đặc trưng cho tác dụng ${f(25)} của lực quanh một trục.</div>
<div style="margin:.6mm 0">${m('M=')} ${fx()} · ${fx()} &nbsp;&nbsp; đơn vị của ${m('M')}: ${f(16)}</div>
<div><b>Cánh tay đòn</b> ${m('d')} = khoảng cách từ ${f(25)} tới ${f(25)} của lực, đo ${f(25)}.</div>
<div>Mở bài: Minh ${nw(`${m('M=')} ${fx()} N·m`)}; anh Tuấn ${nw(`${m('M=')} ${fx()} N·m`)}. Nhổ đinh cần khoảng ${u('40', 'N\\cdot m')}: người nhổ được là ${f(25)}</div></div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('CÁNH TAY ĐÒN · QUY TẮC MOMENT')}
${h3(1, 'Lực xiên: tìm cánh tay đòn', '2·1')}
<div class="card fig-side" style="${fs(50)};padding:1.2mm 3mm"><div>
<div>Lực ${m('F')} đặt tại ${m('A')}, ${m('OA=r')}, giá của ${m('F')} hợp với ${m('OA')} góc ${al}:</div>
<div style="margin:.6mm 0">${m('d=')} ${fx(14)} &nbsp;nên ${m('d')} ${ck}${m('\\lt r')} &nbsp;${ck}${m('=r')} &nbsp;${ck}${m('\\gt r')}</div>
<div>Lực vuông góc với ${m('OA')}: ${m('d=')} ${fx()}</div>
<div>Giá của lực đi qua trục: ${m('d=')} ${fx()} nên ${m('M=')} ${fx()}</div>
<div>Đề cho góc giữa lực và ${m('OA')} → dùng ${fx()}; góc giữa lực và phương vuông góc ${m('OA')} → dùng ${fx()}</div></div>
${H.lucXien()}</div>
${h3(2, 'Thí nghiệm: mở cửa lớp', '2·2')}
<div class="card" style="padding:1.2mm 3mm">
<div><b>Làm:</b> một ngón tay đẩy cửa vuông góc mặt cửa ở mép ngoài, ở giữa, sát bản lề; cuối cùng đẩy ở mép ngoài, hướng thẳng vào bản lề.</div>
<div><b>Quan sát:</b> cửa mở nhẹ nhất khi đẩy ở ${f(25)}; đẩy hướng vào bản lề thì cửa ${f(25)}</div>
<div><b>Rút ra:</b> tác dụng làm quay tăng theo ${f(25)}; giá lực qua trục thì ${nw(`${m('M=')} ${fx()}`)}</div></div>
${h3(3, 'II.2 · Quy tắc moment', '2·3')}
<div class="card" style="padding:1.2mm 3mm">
<div>Áp dụng cho vật có ${f(30)}.</div>
<div>Vật cân bằng khi tổng moment làm quay ${f(25)} chiều kim đồng hồ bằng tổng moment làm quay ${f(25)} chiều kim đồng hồ:</div>
<div style="margin:.6mm 0">${m("M_1+M_2+\\dots=")} ${f(30)}</div></div>
${h3(4, 'Thí nghiệm: thước có trục quay ở giữa', '2·4')}
<div class="fig-side" style="${fs(48)}"><div>
<table class="tbl-ct"><tr><th>${m('d_2\\ (\\mathrm{cm})')}</th><th>${m('F_2\\ (\\mathrm N)')}</th><th>${m('F_2 d_2\\ (\\mathrm{N\\cdot cm})')}</th></tr>
<tr><td>10</td><td>3,10</td><td></td></tr>
<tr><td>15</td><td>2,00</td><td></td></tr>
<tr><td>20</td><td>1,52</td><td></td></tr>
<tr><td>30</td><td>0,99</td><td></td></tr></table>
<div style="margin-top:.6mm">${m('P_1 d_1=')} ${fx()} N·cm = ${fx()} N·m</div>
</div>
${H.thuocTN()}</div>
<div class="card" style="margin-top:.8mm;padding:1mm 3mm">
<div>So cột cuối với ${m('P_1d_1')}. Lệch nhiều nhất ở ${nw(`${m('d_2=')} ${fx()} cm`)}, vì:</div>${lines(1)}
<div><b>Rút ra:</b> lực kế càng xa trục, số chỉ càng ${f(25)}; moment hai bên ${f(25)}</div></div>
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('CÂN BẰNG CỦA VẬT RẮN · NGẪU LỰC · BA CÁI BẪY')}
${h3(1, 'II.3 · Điều kiện cân bằng của vật rắn', '3·1')}
<div class="card" style="padding:1.2mm 3mm">
<div>Không tịnh tiến: ${f(25)} ${m('=\\vec 0')} &nbsp;·&nbsp; Không quay: ${f(25)} ${m('=0')} đối với điểm ${f(25)}</div>
<div>Chiều quay chọn làm dương: moment mang dấu ${fx(8)}; chiều kia mang dấu ${fx(8)}</div>
<div><b>Mẹo chọn trục:</b> đặt trục ở chỗ có lực ${f(25)}, vì lực đó có ${nw(`${m('d=')} ${fx(8)}`)} nên biến khỏi phương trình moment.</div>
<div style="margin-top:.6mm"><b>Thử:</b> ván đồng chất dài ${u('2', 'm')}, ${nw(m('P=200\\ \\mathrm N'))}, hai đầu gác lên hai bờ mương. Trục qua bờ trái: lực bờ phải ${nw(`${m('N_2=')} ${fx()} N`)}; tổng lực: lực bờ trái ${nw(`${m('N_1=')} ${fx()} N`)}</div></div>
${h3(2, 'II.4 · Ngẫu lực', '3·2')}
<div class="card fig-side" style="${fs(44)};padding:1.2mm 3mm"><div>
<div><b>Ngẫu lực:</b> hai lực ${f(25)}, ${f(25)} chiều, cùng ${f(25)}, cùng đặt vào ${f(25)}</div>
<div>Tổng hai lực = ${fx()} nên ngẫu lực chỉ làm vật ${f(25)}</div>
<div>Vật tự do quay quanh trục qua ${f(25)}; vật có trục cố định quay quanh ${f(25)}</div>
<div style="margin:.6mm 0">${m('M=')} ${fx()} · ${fx()} &nbsp;với ${m('d')} là khoảng cách giữa ${f(25)}</div>
<div>Moment ngẫu lực ${ck}có &nbsp;${ck}không phụ thuộc vị trí trục quay.</div>
<div><b>Thí nghiệm:</b> đẩy hai đầu thước 30 cm trên mặt bàn nhẵn, ngược chiều, mạnh như nhau, vuông góc thước. Thước ${ck}trượt đi &nbsp;${ck}quay tại chỗ, quanh vạch ${fx()} cm.</div>
<div><b>Thử:</b> vô lăng, mỗi lực ${u('20', 'N')}, hai giá cách nhau ${u('0{,}36', 'm')}: hợp lực = ${fx()} N; ${nw(`${m('M=')} ${fx()} N·m`)}</div></div>
${H.voLang()}</div>
${h3(3, 'III · Ba cái bẫy hay sập', '3·3')}
<div class="fig-side" style="${fs(30)}"><div class="card" style="padding:1mm 3mm;margin:0">
<div class="trap">${ck}<span><b>“Cánh tay đòn là khoảng cách tới điểm đặt lực.”</b> Đo vuông góc từ trục tới <b>giá</b> lực: ${m('d=r\\sin\\alpha')}.</span></div>
<div class="trap">${ck}<span><b>“Lực càng lớn, vật càng dễ quay.”</b> Đẩy cửa hướng vào bản lề: ${m('d=0')}, ${m('M=0')}. So moment, không so lực.</span></div>
<div class="trap">${ck}<span><b>“Tổng lực bằng 0 là vật cân bằng.”</b> Ngẫu lực trên vô lăng: tổng lực bằng 0 mà vẫn quay. Cần thêm tổng moment bằng 0.</span></div></div>${H.anhBua()}</div>
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('TỰ KIỂM TRA · BÀI TOÁN MẪU')}
${h3(1, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '4·1')}
${rkHai([1, 2, 3], [4, 5, 6])}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm Trả bài:</b> ……/6 câu · chưa thuộc: ${f(25)} ${nw(`→ đọc lại ô ${fx()} Tập`)}</div>
${h3(2, 'V · Bài toán mẫu: thanh gỗ và túi gạo', '4·2')}
<div class="card soft" style="padding:1.2mm 3mm">Thanh gỗ đồng chất ${m('AB')} dài ${u('1{,}2', 'm')}, trọng lượng ${u('40', 'N')}, kê trên giá đỡ nhọn tại ${m('O')} cách đầu ${m('A')} một đoạn ${u('0{,}4', 'm')}. Treo túi gạo ở ${m('A')} thì thanh nằm ngang cân bằng.
<div>Tìm trọng lượng túi gạo và lực giá đỡ tác dụng lên thanh.</div></div>
${h3(3, 'Phân tích đề')}
<table><tr><th style="width:50mm">Câu trong đề</th><th>Dữ liệu → kiến thức</th></tr>
<tr><td>“đồng chất, dài 1,2 m”</td><td>Trọng tâm ${m('G')} ở giữa: ${m('AG=0{,}6\\ \\mathrm m')}</td></tr>
<tr><td style="height:6.5mm">“trọng lượng 40 N”</td><td></td></tr>
<tr><td style="height:6.5mm">“cách đầu A 0,4 m”</td><td></td></tr>
<tr><td style="height:6.5mm">“treo túi gạo ở A”</td><td></td></tr>
<tr><td style="height:6.5mm">Dữ kiện ngầm: “nằm ngang cân bằng”</td><td></td></tr></table>
${h3(4, 'Giải')}
<div class="fig-side" style="${fs(52)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl('Chọn trục qua điểm nào, vì sao?', 2)}${wl('Quy tắc moment, tìm <i>P</i><sub>1</sub>:', 3)}${wl('Tổng lực, tìm <i>N</i>:', 2)}${wl('Kiểm tra: moment quanh <i>A</i>', 2)}</div>${H.thanhMau()}</div>
${h3(5, 'Điền bước còn thiếu: giá đỡ dời tới cách A đúng 0,3 m')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl(`Bước 1: ${m('OG=')}`, 1)}${wl(`Bước 2: ${m('P_1=')}`, 1)}
<div class="ln"><b>Bước 3:</b> ${m('N=P_1+P=')} ${f(16)}</div></div>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TẬP VỀ NHÀ · THỬ THÁCH · TRẢ BÀI')}
${K.btvn()}
${h3(2, 'Thử thách phân tầng', '5·2')}
<div class="fig-side" style="${fs(44)}">${box(wl(`${m('\\bigstar')} Lực ${u('15', 'N')} vuông góc tay quay, cách trục ${u('0{,}2', 'm')}. Moment?`, 2)
 + wl(`${m('\\bigstar\\bigstar')} Lực ${u('40', 'N')} đặt ở mép cửa cách bản lề ${u('0{,}9', 'm')}, hợp với mặt cửa góc ${m('60^\\circ')}. Moment?`, 2)
 + wl(`${m('\\bigstar\\bigstar\\bigstar')} Thanh nhẹ dài ${u('1', 'm')} kê trên hai giá ở hai đầu ${m('A')}, ${m('B')}; treo vật ${u('300', 'N')} cách ${m('A')} ${u('0{,}4', 'm')}. Lực mỗi giá?`, 3))}${H.haiGia()}</div>
${h3(3, 'IV · Trả bài 6 câu', '5·3')}
${box(`${tb('1. Moment lực là gì? Công thức, đơn vị.')}${lines(2)}
${tb('2. Cánh tay đòn đo từ đâu tới đâu?')}${lines(1)}
${tb('3. Phát biểu quy tắc moment. Áp dụng cho vật nào?')}${lines(1)}
${tb('4. Hai điều kiện cân bằng của vật rắn?')}${lines(1)}
${tb('5. Ngẫu lực là gì? Gây ra chuyển động gì?')}${lines(1)}
${tb('6. Moment ngẫu lực tính thế nào? Có phụ thuộc trục không?')}${lines(1)}`)}
${h3(4, 'VI · Mang về: điều em dễ quên nhất', '5·4')}
${box(wl('1.', 2) + wl('2.', 2) + wl('3.', 2))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Moment của lực: tính M, tìm lực khi đổi chỗ đặt',
    de: `Cửa rộng ${u('0{,}90', 'm')} quay quanh bản lề. Đẩy lực ${nw(m('F=20\\ \\mathrm N'))} vuông góc mặt cửa, cách bản lề ${u('75', 'cm')}.<br><b>a)</b> moment của lực đối với trục bản lề<br><b>b)</b> đẩy cách bản lề ${u('15', 'cm')}, cùng moment: lực bao nhiêu`,
    nd: `${m('d')} = khoảng từ bản lề tới ${f(25)}; đổi cm → ${fx()}`, a: ['a', 'b'], gi: 2 },
  { t: 'Dạng 2 · Trung bình · Lực xiên: tìm cánh tay đòn rồi tính moment',
    de: `Đẩy núm cối xay đá (cách tâm ${nw(m('r=0{,}30\\ \\mathrm m'))}) bằng lực ${nw(m('F=80\\ \\mathrm N'))} nằm ngang, giá lực hợp với đường nối núm – tâm góc ${m('40^\\circ')}.<br><b>a)</b> cánh tay đòn ${m('d')} của lực<br><b>b)</b> moment của lực đối với trục quay<br><b>c)</b> đẩy vuông góc đường nối núm – tâm: lực bao nhiêu để cùng moment`,
    nd: `Góc ${m('40^\\circ')} nằm giữa giá của ${m('F')} và ${f(25)} nên ${nw(`${m('d=r\\cdot')} ${f(14)}`)}`, a: ['a', 'b', 'c'], gi: 3, fig: H.coiXay() },
  { t: 'Dạng 3 · Trung bình · Ngẫu lực: hợp lực và moment',
    de: `Hai tay nắm hai đầu đường kính bánh lái, cách nhau ${u('0{,}90', 'm')}; mỗi tay đẩy ${u('30', 'N')} tiếp tuyến với vành, hai lực ngược chiều.<br><b>a)</b> hợp lực của hai lực<br><b>b)</b> moment của cặp lực đối với trục quay<br><b>c)</b> muốn moment ${u('36', 'N\\cdot m')}: mỗi tay đẩy bao nhiêu`,
    nd: `Hợp lực của ngẫu lực = ${fx()}; ${m('d')} = khoảng cách giữa ${f(25)}`, a: ['a', 'b', 'c'], gi: 3 },
  { t: 'Dạng 4 · Khá · Thanh trên giá đỡ: vị trí và lực giá đỡ',
    de: `Thanh đồng chất ${m('AB')} dài ${u('1{,}0', 'm')}, trọng lượng ${u('20', 'N')}; gắn chặt khối ${u('40', 'N')} ở ${m('A')}, khối ${u('20', 'N')} ở ${m('B')} (kích thước bỏ qua). Thanh đặt trên giá đỡ nhọn ${m('O')}, nằm ngang cân bằng.<br><b>a)</b> khoảng cách ${m('OA')}<br><b>b)</b> lực giá đỡ tác dụng lên thanh`,
    nd: `Trục qua ${fx()} để ${m('N')} biến mất; đặt ${m('OA=x')} thì ${nw(`${m('OG=')} ${f(14)}`)}, ${nw(`${m('OB=')} ${f(14)}`)}`, a: ['a', 'b'], gi: 5, fig: H.thanhHaiKhoi() },
  { t: 'Dạng 5 · Khó · Thanh gắn bản lề, giữ bằng dây xiên',
    de: `Thanh đồng chất ${m('AB')} dài ${u('1{,}5', 'm')}, trọng lượng ${u('40', 'N')}, nằm ngang; đầu ${m('A')} gắn bản lề vào tường, đầu ${m('B')} treo biển ${u('16', 'N')}. Dây buộc ở ${m('C')} (${nw(m('AC=1{,}2\\ \\mathrm m'))}) lên tường phía trên bản lề, hợp với thanh góc ${m('30^\\circ')}.<br><b>a)</b> lực căng dây<br><b>b)</b> thành phần thẳng đứng của lực bản lề: độ lớn, hướng lên hay xuống`,
    nd: `Trục qua ${fx()}; ${nw(`${m('d_T=AC\\cdot')} ${f(14)}`)}; phương đứng: ${nw(`${m('T\\sin 30^\\circ+N_y=')} ${f(16)}`)}`, a: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>'], gi: 7, fig: H.banLe(), cot: 3 },
];

// Bài tương tự giải vào vở (thầy chốt 10/11): 1 cột; ô đáp số 25 mm đặt cuối đúng dòng của ý (oY, như l10-bai23), đáp số in ngược.
// Đáp số tính bằng Python 13/11/2026 (math.sin theo radian), làm tròn 3 chữ số có nghĩa.
const ttCss = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';
const oY = (s, o, w = 25) => s.split('<br>').map((p) => {
  const y = p.match(/^<b>([a-d])\)<\/b>/);
  if (!y) return `<div>${p}</div>`;
  const ls = o.filter((l) => l[0] === y[1]);
  return `<div class="yo"><span>${p}</span><span class="oo">${ls.map((l) => `<span class="nw"><b>${l})</b>${f(w)}</span>`).join('')}</span></div>`;
}).join('');
const ttDe = (b) => b.fig ? `<div class="fig-side" style="grid-template-columns:1fr ${b.fw}mm"><div>${oY(b.de, b.o, b.ow)}</div>${b.fig}</div>` : oY(b.de, b.o, b.ow);
const vaoVo = (ds) => ds.map((b) => (b.o ? { t: b.t, de: ttDe(b), k: 0 } : b));
const nhap = (n) => ({ t: '<span class="nhap-t">Nháp / chỗ em còn vướng</span>', de: lines(n), k: 0 });
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–3', 'DẠNG 4–5'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Vặn bu-lông bằng cờ lê: lực ${u('40', 'N')} vuông góc cán, đặt cách tâm bu-lông ${u('25', 'cm')}.<br><b>a)</b> moment của lực đối với tâm bu-lông<br><b>b)</b> cầm cách tâm ${u('20', 'cm')}: lực bao nhiêu để có cùng moment`, o: ['a', 'b'] },
    { t: 'Dạng 1 · Bài 2', de: `Dùng xà beng bẩy tảng đá cần moment ${u('120', 'N\\cdot m')} quanh điểm tì; tay ấn vuông góc xà beng.<br><b>a)</b> tay đặt cách điểm tì ${u('1{,}2', 'm')}: lực tay bao nhiêu<br><b>b)</b> tay ấn được tối đa ${u('80', 'N')}: phải đặt tay cách điểm tì ít nhất bao xa`, o: ['a', 'b'] },
    { t: 'Dạng 2 · Bài 1', de: `Lực ${u('50', 'N')} đặt ở mép cửa cách bản lề ${u('0{,}80', 'm')}, hợp với mặt cửa góc ${m('30^\\circ')}.<br><b>a)</b> cánh tay đòn ${m('d')}<br><b>b)</b> moment của lực đối với bản lề<br><b>c)</b> đẩy vuông góc mặt cửa tại cùng điểm: lực bao nhiêu để có cùng moment`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 2 · Bài 2', de: `Cờ lê: lực ${u('60', 'N')} đặt ở đầu cán cách tâm bu-lông ${u('0{,}30', 'm')}, hợp với cán góc ${m('60^\\circ')}.<br><b>a)</b> cánh tay đòn ${m('d')}<br><b>b)</b> moment của lực<br><b>c)</b> giữ nguyên góc, muốn moment ${u('18', 'N\\cdot m')}: lực bao nhiêu`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 3 · Bài 1', de: `Hai ngón tay vặn tay nắm vòi nước bằng ngẫu lực, mỗi lực ${u('5{,}0', 'N')}, hai giá cách nhau ${u('4{,}0', 'cm')}.<br><b>a)</b> hợp lực của hai lực<br><b>b)</b> moment của ngẫu lực<br><b>c)</b> vòi cần moment ${u('0{,}30', 'N\\cdot m')}: mỗi ngón đẩy bao nhiêu`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 3 · Bài 2', de: `Tháo bánh xe bằng cần chữ thập: hai tay đẩy hai đầu cần, mỗi tay ${u('60', 'N')}, ngược chiều, hai tay cách nhau ${u('0{,}50', 'm')}.<br><b>a)</b> hợp lực của hai lực<br><b>b)</b> moment của ngẫu lực<br><b>c)</b> chỉ một tay đẩy ở đầu cần cách trục ${u('0{,}25', 'm')}: lực bao nhiêu để có cùng moment`, o: ['a', 'b', 'c'] },
    nhap(4),
  ], [
    { t: 'Dạng 4 · Bài 1', de: `Thanh đồng chất ${m('AB')} dài ${u('2{,}0', 'm')}, trọng lượng ${u('60', 'N')}; treo vật ${u('90', 'N')} ở đầu ${m('A')}. Thanh nằm ngang trên giá đỡ nhọn ${m('O')}.<br><b>a)</b> khoảng cách ${m('OA')}<br><b>b)</b> lực giá đỡ tác dụng lên thanh`, o: ['a', 'b'] },
    { t: 'Dạng 4 · Bài 2', de: `Đòn gánh nhẹ dài ${u('1{,}5', 'm')}; đầu ${m('A')} treo thúng ${u('300', 'N')}, đầu ${m('B')} treo thúng ${u('200', 'N')}. Đòn gánh nằm ngang trên vai.<br><b>a)</b> vai đặt cách ${m('A')} bao nhiêu<br><b>b)</b> lực vai đỡ đòn gánh`, o: ['a', 'b'] },
    { t: 'Dạng 5 · Bài 1', de: `Thanh đồng chất ${m('AB')} dài ${u('1{,}0', 'm')}, trọng lượng ${u('30', 'N')}, nằm ngang; đầu ${m('A')} gắn bản lề vào tường, dây buộc ở đầu ${m('B')} lên tường phía trên, hợp với thanh góc ${m('30^\\circ')}.<br><b>a)</b> cánh tay đòn của lực căng đối với ${m('A')}<br><b>b)</b> lực căng dây<br><b>c)</b> thành phần thẳng đứng của lực bản lề: độ lớn, hướng`, o: ['a', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'] },
    { t: 'Dạng 5 · Bài 2', de: `Thanh đồng chất ${m('AB')} dài ${u('1{,}2', 'm')}, trọng lượng ${u('20', 'N')}, nằm ngang, đầu ${m('A')} gắn bản lề; đầu ${m('B')} treo đèn ${u('40', 'N')} và buộc dây lên tường, dây hợp với thanh góc ${m('45^\\circ')}.<br><b>a)</b> cánh tay đòn của lực căng đối với ${m('A')}<br><b>b)</b> lực căng dây<br><b>c)</b> thành phần thẳng đứng của lực bản lề: độ lớn, hướng`, o: ['a', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'] },
    nhap(10),
  ]],
  dap: [
    `D1·1: a) 10 N·m · b) 50 N &nbsp;|&nbsp; D1·2: a) 100 N · b) 1,5 m &nbsp;|&nbsp; D2·1: a) 0,40 m · b) 20 N·m · c) 25 N &nbsp;|&nbsp; D2·2: a) 0,260 m · b) 15,6 N·m · c) 69,3 N &nbsp;|&nbsp; D3·1: a) 0 · b) 0,20 N·m · c) 7,5 N &nbsp;|&nbsp; D3·2: a) 0 · b) 30 N·m · c) 120 N`,
    `D4·1: a) 0,40 m · b) 150 N &nbsp;|&nbsp; D4·2: a) 0,60 m · b) 500 N &nbsp;|&nbsp; D5·1: a) 0,50 m · b) 30 N · c<sub>1</sub>) 15 N · c<sub>2</sub>) hướng lên &nbsp;|&nbsp; D5·2: a) 0,849 m · b) 70,7 N · c<sub>1</sub>) 10 N · c<sub>2</sub>) hướng lên`,
  ],
};

await K.dung({
  trang1to5: ttCss + [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 2], kq: [[1, 2, 3], [4, 5]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'moment 1·5 · lực xiên 2·1 · quy tắc moment 2·3 · cân bằng 3·1 · ngẫu lực 3·2 · bẫy 3·3 · bài mẫu 4·2 · dạng 1–3 → 6·1 · dạng 4–5 → 7·1',
  out: process.argv[2],
});
