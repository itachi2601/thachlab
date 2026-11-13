// Ruột tập VL10 – Bài 1 · Làm quen với Vật lí (lesson id 46). Quyển Chương 1 lớp 10: bài 1 = tr. 1–12.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l10-bai1.mjs (SVG tự vẽ). Nội dung theo bài web (book/cache/46.json, tải từ DB 13/11/2026): mục tiêu, dự đoán ấm nước, II.1–II.5,
// hai thí nghiệm (giọt mực, sách–giấy rơi), ba bẫy, Trả bài 6 câu, bài toán mẫu ly nước đá, 3 dạng bài tập mẫu.
// Đáp số Bài tương tự tính bằng Python 13/11/2026. Chạy: node scripts/ruot-tap/l10-bai1.mjs [file.pdf] | --hinh
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai, dapSo } from './khung.mjs';
import { hinhL10b1 as H } from './hinh-l10-bai1.mjs';

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
  const out = resolve(HERE, 'out/hinh-l10-bai1'); mkdirSync(out, { recursive: true });
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


const K = khoiTao({ bai: 1, lid: 46, ten: 'LÀM QUEN VỚI VẬT LÍ', lop: 10, baiDau: 1, sub: 'Vật lí 10 · Chương 1: Mở đầu' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const pm = (x) => nw(m(`\\pm ${x}`));

const p1 = `<section class="page">
${head('BÀI 1 · LÀM QUEN VỚI VẬT LÍ', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Nêu <b>đối tượng</b> nghiên cứu của vật lí; phân biệt <b>vi mô</b> và <b>vĩ mô</b>`)}
${dong(`${ck}Kể được <b>mục tiêu</b> môn Vật lí và ảnh hưởng của nó tới <b>năm lĩnh vực</b>`)}
${dong(`${ck}Phân biệt <b>thực nghiệm</b> với <b>lí thuyết</b>; nhớ quy trình <b>5 bước</b>`)}
${dong(`${ck}So <b>chênh lệch với sai số</b> trước khi nói hai số là khác nhau`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Phần nào của cảnh ấm nước sắp sôi thuộc phạm vi nghiên cứu của vật lí?</p>
<div class="fig-side" style="${fs(48)}"><div>
${opt('A', 'Chỉ nắp ấm rung, vì ta nhìn thấy nó')}
${opt('B', 'Chỉ chuyển động của phân tử, vì đó mới là gốc')}
${opt('C', 'Cả hai, và mối liên hệ giữa chúng')}
${opt('D', 'Không phần nào, đây là việc của hoá học')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 1)}</div>
${H.amNuoc('Ấm nước trên bếp sắp sôi.')}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Vật lí nghiên cứu gì', '1·4')}
<div class="card" style="padding:1.2mm 3mm">
<div>Vật lí nghiên cứu ${f(25)} của vật chất và ${f(25)} ở mọi cấp độ.</div>
<div><b>Vi mô:</b> mắt thường ${f(25)} thấy (nguyên tử, phân tử).</div>
<div><b>Vĩ mô:</b> mắt thường ${f(25)} thấy (Trái Đất, vũ trụ).</div></div>
${h3(5, 'Thí nghiệm: giọt mực trong nước nóng và lạnh', '1·5')}
<div class="card fig-side" style="${fs(40)};padding:1.2mm 3mm"><div>
<div><b>Làm:</b> nhỏ một giọt mực vào hai cốc nước, không khuấy: một cốc lạnh, một cốc nóng khoảng ${nw(m('60^\\circ\\mathrm{C}'))} (cẩn thận bỏng).</div>
<div><b>Quan sát:</b> mực loang đều nhanh hơn ở cốc ${f(25)}.</div>
<div><b>Rút ra:</b> mực loang là hiện tượng ${f(14)} mô; nguyên nhân là ${f(25)} nước (cấp độ ${f(14)} mô): nước càng nóng, chúng chuyển động càng ${f(14)}.</div></div>
${H.giotMuc('Hai cốc, nhìn cùng một lúc sau khi nhỏ mực.')}</div>
<div class="card soft" style="margin-top:1mm;padding:.8mm 3mm"><b>Làm nhanh:</b> xếp vi mô hay vĩ mô: nguyên tử, phân tử nước, hạt cát, người, Trái Đất.${lines(2)}</div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('MỤC TIÊU · ẢNH HƯỞNG · HAI PHƯƠNG PHÁP')}
${h3(1, 'II.2 · Mục tiêu của môn Vật lí', '2·1')}
<div class="card fig-side" style="${fs(40)};padding:1.2mm 3mm"><div>
<div>Khám phá quy luật ${f(25)} nhất của vận động và tương tác của vật chất, năng lượng, ở cả vi mô lẫn vĩ mô.</div>
<div>Ở phổ thông: nắm kiến thức, kĩ năng và ${f(25)} vào học tập, đời sống.</div>
<div>Vật lí là cơ sở của khoa học ${f(25)}.</div>
<div style="margin-top:.6mm"><b>Ví dụ “tổng quát”:</b> một định luật bảo toàn năng lượng cho cả hai cảnh: xe đạp xuống dốc, thế năng thành ${f(25)} năng; pin hết dần, hoá năng thành ${f(25)} năng.</div></div>
${H.thang('Năm đối tượng từ nhỏ đến lớn (không theo tỉ lệ).')}</div>
${h3(2, 'II.3 · Vật lí ảnh hưởng tới năm lĩnh vực', '2·2')}
<div class="hint" style="margin-bottom:.6mm">Ngân hàng ví dụ: internet · chụp MRI · robot tự động hoá · đèn LED trồng cây · kính hiển vi điện tử</div>
<table><tr><th style="width:42mm">Lĩnh vực</th><th>Ví dụ từ vật lí (chọn trong ngân hàng, hoặc tự thêm)</th></tr>
<tr><td style="height:6mm">Thông tin liên lạc</td><td></td></tr>
<tr><td style="height:6mm">Y tế</td><td></td></tr>
<tr><td style="height:6mm">Công nghiệp</td><td></td></tr>
<tr><td style="height:6mm">Nông nghiệp</td><td></td></tr>
<tr><td style="height:6mm">Nghiên cứu</td><td></td></tr></table>
${h3(3, 'II.4 · Hai phương pháp nghiên cứu', '2·3')}
<table><tr><th style="width:24mm"></th><th>Thực nghiệm</th><th>Lí thuyết</th></tr>
<tr><td><b>Làm gì</b></td><td style="height:11mm"></td><td></td></tr>
<tr><td><b>Kết quả cần</b></td><td style="height:11mm"></td><td></td></tr></table>
<div class="card soft" style="margin-top:1mm;padding:1.2mm 3mm">
<div><b>Ví dụ:</b> thả sách rơi từ độ cao ${nw(m('h'))} (m); ${nw(m('g\\approx 9{,}8\\ \\mathrm{m/s^2}'))} là gia tốc rơi tự do (học kĩ ở bài Sự rơi tự do).</div>
<div>Đo thời gian rơi bằng video: phương pháp ${f(25)}. Tính trước ${nw(m('t=\\sqrt{\\dfrac{2h}{g}}'))}: phương pháp ${f(25)}.</div></div>
${h3(4, 'Làm nhanh (tiếp)', '2·4')}
${box(cau(`<b>Câu 2.</b> Máy chụp MRI, đèn LED chiếu cây, kính hiển vi điện tử: mỗi thiết bị thuộc lĩnh vực nào?`, 1))}
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('QUY TRÌNH 5 BƯỚC · THÍ NGHIỆM SÁCH VÀ GIẤY RƠI')}
${h3(1, 'II.5 · Quy trình nghiên cứu: 5 bước', '3·1')}
<div class="card fig-side" style="${fs(40)};padding:1.2mm 3mm"><div>
<div><b>Thấy:</b> ${f(25)}, suy luận &nbsp;·&nbsp; <b>Hỏi:</b> đề xuất ${f(25)}</div>
<div><b>Đoán:</b> hình thành ${f(25)} (lời đoán nguyên nhân, chưa được kiểm tra)</div>
<div><b>Thử:</b> ${f(25)} giả thuyết &nbsp;·&nbsp; <b>Chốt:</b> rút ra ${f(25)}</div>
<div>Kiểm tra không khớp: ${f(25)} hoặc ${f(25)} giả thuyết, rồi quay lại bước ${f(8)}.</div>
<div style="margin-top:.6mm"><b>Lưu ý:</b> suy luận ở bước 1 chỉ dẫn tới câu ${f(25)}; lời đoán nguyên nhân để đem đi kiểm tra mới là giả thuyết.</div></div>
${H.nam('Năm bước nghiên cứu; có đường quay lại.')}</div>
${h3(2, 'Làm nhanh', '3·2')}
${box(cau(`<b>Câu 1.</b> Lan thấy sách rơi nhanh hơn tờ giấy và nói: “Chắc do không khí cản tờ giấy nhiều hơn.” Câu này thuộc bước nào? Vì sao?`, 2))}
${h3(3, 'Thí nghiệm: sách và giấy rơi', '3·3')}
<div class="fig-side" style="${fs(44)}"><div>
<div><b>Làm:</b> thả cùng lúc từ ${nw('2 m')}: sách với giấy phẳng; giấy đặt trên sách; giấy vo tròn thả cùng sách. Quay video ${nw('60 hình/giây')} (1 khung = ${nw(m('\\tfrac1{60}\\ \\mathrm s'))}); thả mỗi kiểu 3 lần, đếm số khung hình từ lúc buông tới lúc chạm sàn.</div>
<table class="tbl-ct" style="margin-top:.8mm;text-align:center"><tr><th style="text-align:left">Vật</th><th>Số khung 3 lần</th><th>Trung bình</th><th>${m('t\\ (\\mathrm s)')}</th><th>${m('g=\\dfrac{2h}{t^2}')}</th></tr>
<tr><td style="text-align:left">Sách</td><td>38 · 38 · 39</td><td></td><td></td><td></td></tr>
<tr><td style="text-align:left">Giấy vo</td><td>41 · 41 · 41</td><td></td><td></td><td></td></tr></table></div>
${H.roi('Thả cùng lúc từ cùng độ cao; ảnh chụp cùng một thời điểm (minh hoạ).')}</div>
<div class="card" style="margin-top:.6mm;padding:1mm 3mm">
<div><b>Quan sát:</b> giấy phẳng rơi ${f(25)} hẳn; giấy đặt trên sách rơi ${f(25)} sách.</div>
<div>Mỗi lần đếm lệch ${pm('1')} khung ${nw(`= ${m('\\pm')} ${f(14)} s`)}. Chênh giữa hai vật ${nw(m('\\approx 2{,}7'))} khung: ${ck}vượt ${ck}không vượt sai số.</div>
<div><b>Rút ra:</b> giấy phẳng chậm vì ${f(25)} cản, không phải vì ${f(25)}.</div></div>
${h3(4, 'Điền bước còn thiếu: giả thuyết của Hà', '3·4')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div style="padding-top:1mm;line-height:1.35"><b>Hà đoán (cho sẵn):</b> ly càng lạnh thì càng đọng nhiều giọt ở thành ngoài.</div>${wl('Cách kiểm tra (hai ly giống nhau, chỉ đổi một điều):', 1)}${wl('Dự đoán nếu giả thuyết đúng:', 1)}</div>
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('BA CÁI BẪY · TRẢ BÀI · TỰ KIỂM TRA')}
${h3(1, 'III · Ba cái bẫy hay sập', '4·1')}
<div class="card fig-side" style="${fs(40)};padding:1mm 3mm"><div>
<div class="trap">${ck}<span><b>“Đã có lí thuyết thì khỏi cần đo.”</b> Robot đi ${nw('6 m')} với ${nw('0,2 m/s')}: lí thuyết ${nw(`${m('6:0{,}2=')} ${f(12)} s`)}, đo được ${nw('33 s')}. Lệch ⇒ tìm ${f(25)}, không bỏ bên nào.</span></div>
<div class="trap">${ck}<span><b>“Giả thuyết bị bác bỏ là thí nghiệm hỏng.”</b> Bác bỏ cũng là kết quả: loại một hướng ${f(14)}, cho biết điều ${f(14)}.</span></div>
<div class="trap">${ck}<span><b>“Hai số khác nhau là khác thật.”</b> Chênh lệch ${f(25)} sai số thì chưa kết luận được.</span></div></div>
${H.robot('Robot hút bụi đi dọc bốn cạnh ô vuông cạnh 1,5 m.')}</div>
${h3(2, 'IV · Trả bài 6 câu', '4·2')}
${box(`${tb('1. Vật lí nghiên cứu gì? Vi mô và vĩ mô khác nhau thế nào?')}${lines(2)}
${tb('2. Mục tiêu của môn Vật lí là gì?')}${lines(2)}
${tb('3. Kể năm lĩnh vực chịu ảnh hưởng của vật lí, mỗi lĩnh vực một ví dụ.')}${lines(2)}
${tb('4. Hai phương pháp nghiên cứu là gì, quan hệ với nhau thế nào?')}${lines(2)}
${tb('5. Năm bước của quy trình (chữ Đoán là bước nào)? Không khớp thì làm gì?')}${lines(2)}
${tb('6. Vì sao giả thuyết bị bác bỏ vẫn có giá trị?')}${lines(2)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/6 câu · chưa thuộc: ${f(25)} ${nw(`→ đọc lại ô ${f(12)} Tập`)}</div>
${h3(3, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '4·3')}
${rkHai([1, 2, 3, 4], [5, 6, 7])}
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TOÁN MẪU · BÀI TẬP VỀ NHÀ · MANG VỀ')}
${h3(1, 'V · Bài toán mẫu: ly nước đá', '5·1')}
<div class="card soft fig-side" style="${fs(36)};padding:1.2mm 3mm"><div>Ly nước đá để ngoài trời nóng. Sau vài phút, mặt ngoài ly đọng đầy giọt nước. Minh nói: “Nước từ trong ly thấm qua thành ra ngoài.”
<div>Vận dụng quy trình nghiên cứu: nêu vấn đề, giả thuyết, một cách kiểm tra có dự đoán rõ ràng, rồi kết luận.</div></div>
${H.lyNuoc('Ly nước đá để ngoài trời nóng vài phút.')}</div>
${h3(2, 'Giải')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl('Vấn đề:', 1)}${wl(`Giả thuyết G1 (của Minh) và G2 (em đoán):`, 2)}${wl('Kiểm tra G1; dự đoán nếu G1 đúng:', 2)}${wl('Kiểm tra G2; dự đoán nếu G2 đúng:', 2)}</div>
<div class="card soft" style="margin:1mm 0;padding:1mm 3mm"><b>Kết quả đo (cho sẵn):</b> giọt ngoài ly trong suốt, không màu; ly rỗng ướp lạnh mang ra vẫn đọng giọt.</div>
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">${wl('Kết luận (G1, G2 thế nào):', 2)}</div>
${K.btvn()}
${h3(4, 'VI · Mang về: điều em dễ quên nhất', '5·2')}
${box(wl('1.', 1) + wl('2.', 1))}
${foot(5)}</section>`;

const tbl3 = (hang, cot = 'Cốc') => `<table style="text-align:center;margin:.6mm 0"><tr><th style="text-align:left;width:22mm">${cot}</th><th>Lần 1</th><th>Lần 2</th><th>Lần 3</th></tr>${hang.map(([n, a, b, c]) => `<tr><td style="text-align:left">${n}</td><td>${a}</td><td>${b}</td><td>${c}</td></tr>`).join('')}</table>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Phân loại vi mô – vĩ mô và lĩnh vực ứng dụng',
    de: `Bốn đối tượng: <b>(1)</b> một nguyên tử đồng trong dây điện; <b>(2)</b> máy tính bảng trên bàn; <b>(3)</b> Mặt Trăng; <b>(4)</b> một phân tử nước trong cốc. Ba ứng dụng: <b>(I)</b> máy siêu âm khám thai; <b>(II)</b> đèn LED chiếu cho rau trong nhà kính; <b>(III)</b> kính hiển vi điện tử nghiên cứu tế bào.<br><b>a)</b> đối tượng nào vi mô, đối tượng nào vĩ mô<br><b>b)</b> lĩnh vực của (I), (II), (III) trong năm lĩnh vực: thông tin liên lạc, y tế, công nghiệp, nông nghiệp, nghiên cứu`,
    nd: `Vi mô: mắt thường ${f(25)} thấy; thiết bị phục vụ việc gì thì thuộc lĩnh vực ${f(25)}`, a: ['a', 'b'], gi: 3, cot: 1 },
  { t: 'Dạng 2 · Trung bình · So kết quả lí thuyết với số đo',
    de: `Nam và Hà muốn biết xe đồ chơi chạy hết đường dài ${m('2{,}4\\ \\mathrm m')} mất bao lâu. Nam coi xe chạy đều với tốc độ ${m('0{,}30\\ \\mathrm{m/s}')} và tính ${m('t=\\dfrac{s}{v}')}. Hà bấm đồng hồ ba lần: ${m('8{,}6\\ \\mathrm s')}; ${m('8{,}7\\ \\mathrm s')}; ${m('8{,}5\\ \\mathrm s')}; sai số mỗi lần ${pm('0{,}2\\ \\mathrm s')}.<br><b>a)</b> cách làm của Nam, của Hà thuộc phương pháp nào<br><b>b)</b> trung bình của Hà lệch bao nhiêu so với Nam tính<br><b>c)</b> độ lệch có vượt sai số không; nhóm nên làm gì tiếp`,
    nd: `Dự đoán bằng công thức: ${f(25)}; đo bằng đồng hồ: ${f(25)}; so độ lệch với ${f(25)}`, a: ['a', 'b', 'c'], gi: 4, fig: H.xeDuong('', '2,4 m'), cot: 1 },
  { t: 'Dạng 3 · Khó · Quy trình 5 bước: giả thuyết, số liệu, kết luận',
    de: `Hoa thấy đá trong cốc kim loại tan nhanh hơn trong cốc xốp. Hoa hỏi: “Vì sao đá trong cốc kim loại tan nhanh hơn?” rồi nói: “Chắc do kim loại truyền nhiệt từ không khí vào đá nhanh hơn.” Hai cốc cùng dung tích, cùng lượng đá, đặt cùng chỗ; thời gian đá tan hết (phút), sai số mỗi lần ${pm('0{,}5')} phút:${tbl3([['Kim loại', '14,2', '13,8', '14,0'], ['Xốp', '22,5', '23,1', '22,8']])}<b>a)</b> câu nào của Hoa là giả thuyết<br><b>b)</b> thời gian tan trung bình hai cốc chênh nhau<br><b>c)</b> chênh lệch so với sai số<br><b>d)</b> kết luận phù hợp`,
    nd: `Lời đoán nguyên nhân chưa kiểm tra là ${f(25)}; so chênh lệch trung bình với ${f(14)}; kết luận chỉ cho điều kiện đã ${f(14)}`, a: ['a', 'b', 'c', 'd'], gi: 9, fig: H.haiCoc('', 'kim loại', 'xốp'), cot: 2 },
];

// Bài tương tự giải vào vở (thầy chốt 10/11): xếp 1 cột; ô đáp số theo nhãn ý; MỖI DẠNG 2 bài; đáp số tính bằng Python (13/11/2026).
const ttHaiCot = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm}.yo .oo{flex:none;display:flex;gap:3mm}.yo{line-height:1.35}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';
const oY = (s, o, w = 25) => s.split('<br>').map((p) => {
  const y = p.match(/^<b>([a-d])\)<\/b>/);
  if (!y) return `<div>${p}</div>`;
  const ls = o.filter((l) => l[0] === y[1]);
  return `<div class="yo"><span>${p}</span><span class="oo">${ls.map((l) => `<span class="nw"><b>${l})</b>${f(w)}</span>`).join('')}</span></div>`;
}).join('');
const ttDe = (b) => b.fig ? `<div class="fig-side" style="grid-template-columns:1fr ${b.fw}mm"><div>${oY(b.de, b.o, b.ow)}</div>${b.fig}</div>` : oY(b.de, b.o, b.ow);
const vaoVo = (ds, i) => ds.map((b) => (b.o ? { t: b.t, de: (i === 0 && b === ds[0] ? ttHaiCot : '') + ttDe(b), k: 0 } : b));
const nhap = (n) => ({ t: '<span class="nhap-t">Nháp / chỗ em còn vướng</span>', de: lines(n), k: 0 });
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–2', 'DẠNG 3'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Bốn đối tượng: <b>(1)</b> một phân tử oxi trong không khí; <b>(2)</b> quả bóng đá; <b>(3)</b> ngôi sao Mặt Trời; <b>(4)</b> hạt nhân của một nguyên tử. Ba ứng dụng: <b>(I)</b> máy chụp cộng hưởng từ (MRI); <b>(II)</b> cáp quang truyền internet; <b>(III)</b> robot hàn ở nhà máy.<br><b>a)</b> các đối tượng vi mô; các đối tượng vĩ mô<br><b>b)</b> lĩnh vực của (I), (II), (III)`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'b<sub>3</sub>'], ow: 22 },
    { t: 'Dạng 1 · Bài 2', de: `Bốn đối tượng: <b>(1)</b> một hạt cát trên bãi biển; <b>(2)</b> một nguyên tử hiđrô; <b>(3)</b> Trái Đất; <b>(4)</b> một phân tử nước trong giọt sương. Ba ứng dụng: <b>(I)</b> đèn LED chiếu cho cây trong nhà kính; <b>(II)</b> máy quang phổ phân tích mẫu; <b>(III)</b> máy xạ trị chữa ung thư.<br><b>a)</b> các đối tượng vi mô; các đối tượng vĩ mô<br><b>b)</b> lĩnh vực của (I), (II), (III)`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'b<sub>3</sub>'], ow: 22 },
    { t: 'Dạng 2 · Bài 1', de: `Xe đồ chơi chạy hết đường dài ${m('3{,}6\\ \\mathrm m')}. Nam coi xe chạy đều với tốc độ ${m('0{,}40\\ \\mathrm{m/s}')} và tính ${m('t=\\dfrac{s}{v}')}. Hà bấm đồng hồ ba lần: ${m('9{,}8\\ \\mathrm s')}; ${m('10{,}0\\ \\mathrm s')}; ${m('10{,}2\\ \\mathrm s')}; sai số mỗi lần ${pm('0{,}2\\ \\mathrm s')}.<br><b>a)</b> thời gian Nam tính<br><b>b)</b> thời gian trung bình Hà đo<br><b>c)</b> độ lệch giữa hai kết quả<br><b>d)</b> độ lệch lớn hơn hay không lớn hơn sai số`, o: ['a', 'b', 'c', 'd'], fig: H.xeDuong('', '3,6 m'), fw: 44, ow: 30 },
    { t: 'Dạng 2 · Bài 2', de: `Xe đồ chơi chạy hết đường dài ${m('1{,}8\\ \\mathrm m')}. Nam coi xe chạy đều với tốc độ ${m('0{,}30\\ \\mathrm{m/s}')} và tính ${m('t=\\dfrac{s}{v}')}. Hà bấm đồng hồ ba lần: ${m('6{,}2\\ \\mathrm s')}; ${m('5{,}9\\ \\mathrm s')}; ${m('6{,}2\\ \\mathrm s')}; sai số mỗi lần ${pm('0{,}3\\ \\mathrm s')}.<br><b>a)</b> thời gian Nam tính<br><b>b)</b> thời gian trung bình Hà đo<br><b>c)</b> độ lệch giữa hai kết quả<br><b>d)</b> độ lệch lớn hơn hay không lớn hơn sai số`, o: ['a', 'b', 'c', 'd'], ow: 30 },
  ], [
    { t: 'Dạng 3 · Bài 1', de: `Minh thấy bột ca cao tan trong sữa nóng nhanh hơn trong sữa lạnh. Minh hỏi: “Vì sao bột tan nhanh hơn trong sữa nóng?” rồi nói: “Chắc do phân tử sữa nóng chuyển động nhanh hơn.” Thời gian bột tan hết (giây), sai số mỗi lần ${pm('5')} s:${tbl3([['Sữa nóng', '40', '38', '42'], ['Sữa lạnh', '95', '90', '100']])}<br><b>a)</b> giả thuyết là câu hỏi hay lời đoán<br><b>b)</b> thời gian tan trung bình hai cốc chênh nhau<br><b>c)</b> chênh lệch so với sai số<br><b>d)</b> kết luận phù hợp`, o: ['a', 'b', 'c', 'd'], fig: H.haiCoc('', 'nóng', 'lạnh'), fw: 44 },
    { t: 'Dạng 3 · Bài 2', de: `Nam thấy ống thép mát tay hơn ống nhựa. Nam hỏi: “Vì sao ống thép mát hơn?” rồi nói: “Chắc do thép dẫn nhiệt khỏi tay nhanh hơn.” Nhiệt độ mặt ống sau khi cầm ${nw('30 s')} (°C), sai số mỗi lần ${pm('0{,}5')} °C:${tbl3([['Ống thép', '25,1', '24,9', '25,0'], ['Ống nhựa', '25,3', '25,2', '25,4']], 'Ống')}<br><b>a)</b> giả thuyết là câu hỏi hay lời đoán<br><b>b)</b> nhiệt độ trung bình hai ống chênh nhau<br><b>c)</b> chênh lệch so với sai số<br><b>d)</b> kết luận phù hợp`, o: ['a', 'b', 'c', 'd'] },
    nhap(8),
  ]],
  dap: [
    `D1·1: a<sub>1</sub>) (1), (4) · a<sub>2</sub>) (2), (3) · b<sub>1</sub>) y tế · b<sub>2</sub>) liên lạc · b<sub>3</sub>) công nghiệp &nbsp;|&nbsp; D1·2: a<sub>1</sub>) (2), (4) · a<sub>2</sub>) (1), (3) · b<sub>1</sub>) nông nghiệp · b<sub>2</sub>) nghiên cứu · b<sub>3</sub>) y tế &nbsp;|&nbsp; D2·1: a) 9,0 s · b) 10,0 s · c) 1,0 s · d) lớn hơn sai số, khác thật &nbsp;|&nbsp; D2·2: a) 6,0 s · b) 6,1 s · c) 0,1 s · d) không lớn hơn sai số, chưa kết luận được là khác`,
    `D3·1: a) lời đoán · b) 55 s · c) lớn hơn nhiều sai số 5 s · d) giả thuyết được ủng hộ trong điều kiện đã thử &nbsp;|&nbsp; D3·2: a) lời đoán · b) 0,3 °C · c) không vượt sai số 0,5 °C · d) chưa kết luận được là khác; chưa đủ để ủng hộ giả thuyết`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [2, 1], kq: [[1, 2], [3]], khoNhat: true },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'đối tượng 1·4 · giọt mực 1·5 · lĩnh vực 2·2 · hai phương pháp 2·3 · năm bước 3·1 · sách–giấy rơi 3·3 · ba bẫy 4·1 · bài toán mẫu 5·1 · dạng 1–2 → 6·1 · dạng 3 → 7·1',
  out: process.argv[2],
});
