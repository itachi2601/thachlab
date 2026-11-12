// Ruột tập VL10 – Bài 2 · Các quy tắc an toàn trong phòng thực hành Vật lí (lesson id 47). Quyển Chương 1 lớp 10: bài 2 = tr. 13–24 (baiDau 1).
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l10-bai2.mjs (toàn bộ SVG tự vẽ). Nội dung theo bài web (book/cache/47.json, tải từ DB 13/11/2026): mục tiêu, dự đoán dây chưa nối,
// II.1 nhãn thiết bị + thí nghiệm núm bộ nguồn, II.2 kí hiệu, II.3 mười quy tắc, thí nghiệm khoảng cách đèn cồn, ba bẫy, Trả bài 6 câu,
// bài toán mẫu (bàn thực hành lỗi), thử thách, 3 dạng bài tập mẫu. Web có 3 dạng; thêm Dạng 4 (sự cố bất ngờ, từ ô "Thử sức đổi tình huống") để đủ chỗ 2 trang. Bài tương tự 6 bài (mỗi dạng 1–3 hai bài): tr.20 Dạng 1–2, tr.21 Dạng 3.
// Đáp số Bài tương tự tính bằng Python 13/11/2026. Không dùng ảnh Halliday.
// Chạy: node scripts/ruot-tap/l10-bai2.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl10-bai2.pdf
//       node scripts/ruot-tap/l10-bai2.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l10-bai2/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai, dapSo } from './khung.mjs';
import { hinhL10b2 as H } from './hinh-l10-bai2.mjs';

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
  const out = resolve(HERE, 'out/hinh-l10-bai2'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 2, lid: 47, ten: 'AN TOÀN PHÒNG THỰC HÀNH', lop: 10, baiDau: 1, sub: 'Vật lí 10 · Chương 1: Mở đầu' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const dT = m('\\Delta T'), dTdinh = nw(m('\\Delta T=T-T_{\\text{phòng}}'));
const dg = (s) => nw(`${s}&nbsp;°C`);

const ttHaiCot = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm}.yo .oo{flex:none;display:flex;gap:3mm}.yo{line-height:1.35}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';

const p1 = `${ttHaiCot}<section class="page">
${head('BÀI 2 · AN TOÀN PHÒNG THỰC HÀNH', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Đọc đúng nhãn trên thiết bị: <b>DC, AC, cực +/−, Input, Output</b>`)}
${dong(`${ck}Nhận nhóm <b>kí hiệu</b> qua hình dạng và màu, biết việc phải làm`)}
${dong(`${ck}Nêu và vận dụng <b>10 quy tắc an toàn</b> khi thực hành`)}
${dong(`${ck}Chỉ ra lỗi nào vi phạm quy tắc nào, việc đầu tiên khi có <b>sự cố</b>`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Bộ nguồn đã bật. Bạn trong nhóm giục: “Nối nhanh đi, chỉ một giây thôi!” Việc đầu tiên cần làm trước khi cầm đầu dây hở?</p>
<div class="fig-side" style="${fs(48)}"><div>
${opt('A', 'Nối ngay cho kịp giờ, vì vỏ nhựa nên chạm là an toàn')}
${opt('B', 'Tắt công tắc nguồn, rồi mới nối dây')}
${opt('C', 'Đeo găng cao su, nối luôn khi nguồn còn bật')}
${opt('D', 'Nối bằng một tay, tay kia giấu ra sau lưng')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 1)}</div>
${H.banDay()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Đọc nhãn trên thiết bị', '1·4')}
<div class="card fig-side" style="${fs(48)};padding:1.2mm 3mm"><div>
<div><b>DC</b> là dòng điện ${f(25)} chiều (pin, đầu ra bộ nguồn); <b>AC</b> là dòng điện ${f(25)} chiều (ổ cắm nhà).</div>
<div>Cực dương: dấu ${f(12)} hoặc màu ${f(25)}; cực âm: dấu ${f(12)} hoặc màu ${f(25)}.</div>
<div><b>Input</b> là đầu ${f(25)} (điện đi vào thiết bị); <b>Output</b> là đầu ${f(25)} (thiết bị cấp điện cho mạch).</div>
<div><b>Định mức</b> là số ${f(25)} ghi trên nhãn dụng cụ: mức dụng cụ được thiết kế để hoạt động bình thường.</div></div>
${H.nhanNguon()}</div>
<div class="card soft" style="padding:1.2mm 3mm"><b>Đo thử:</b> núm ở vạch 3; 6; 9; 12 V, vôn kế chỉ 3,1; 6,2; 9,3; 12,4 V. Bóng ghi 6 V mà núm ở vạch 12 V thì nhận ${f(12)} V, gấp ${f(12)} lần định mức. Vạch chỉ là giá trị gần ${f(25)}.</div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('KÍ HIỆU · MƯỜI QUY TẮC')}
${h3(1, 'II.2 · Kí hiệu: nhìn hình dạng và màu trước, hình bên trong sau', '2·1')}
<div class="fig-side" style="${fs(48)}"><div>
<table><tr><th style="width:36mm">Hình dạng, màu</th><th style="width:25mm">Nhóm</th><th>Ý nghĩa</th></tr>
<tr><td>(1) Tam giác, viền vàng</td><td></td><td>cẩn thận, có nguy hiểm</td></tr>
<tr><td>(2) Tròn, đỏ, gạch chéo</td><td></td><td>không được làm</td></tr>
<tr><td>(3) Tròn, xanh</td><td></td><td>phải làm</td></tr>
<tr><td>(4), (5) Không có khung</td><td></td><td>nhận ra qua hình bên trong</td></tr></table>
<div style="margin-top:1mm">Hình trong tam giác hay gặp: nhiệt độ cao · ${f(25)} · ${f(25)} · ${f(25)}</div>
<div>Hình trong vòng cấm: ${f(25)} · hình trong vòng xanh: đeo ${f(25)}</div></div>
${H.kiHieu()}</div>
${h3(2, 'Làm nhanh', '2·2')}
${box(cau(`<b>Câu 1.</b> Lọ cồn có hai nhãn: chất dễ cháy và cấm lửa. Trên bàn đang đốt đèn cồn và có bộ nguồn. Nên đặt lọ cồn ở đâu, nắp thế nào?`, 2)
 + cau(`<b>Câu 2.</b> Dụng cụ ghi ${nw('6 V, DC')}. Bộ nguồn có Input ${nw('220 V ~')}, Output ${nw('3–12 V')} gồm cổng DC và cổng AC. Nối vào cổng nào, núm ở vạch nào?`, 2))}
${h3(3, 'II.3 · Mười quy tắc, bốn nhóm', '2·3')}
<div class="card" style="padding:1.2mm 3mm">
<div><b>Trước khi làm:</b> đọc kĩ hướng dẫn và ${f(25)} hiệu; ${f(25)} tra thiết bị, dụng cụ; chỉ làm khi giáo viên cho ${f(25)}.</div>
<div style="margin-top:1mm"><b>Với điện:</b> ${f(25)} công tắc nguồn trước khi cầm hoặc tháo; chỉ cắm khi số ${f(25)} khớp với dụng cụ; dây điện ${f(25)} gọn, không vướng; nước, dung dịch dẫn điện hoặc dễ cháy để ${f(25)} thiết bị điện.</div>
<div style="margin-top:1mm"><b>Nhiệt và tia:</b> không chạm vật ${f(25)} khi chưa có dụng cụ hỗ trợ (dùng ${f(25)} hoặc găng chịu nhiệt); giữ ${f(25)} cách an toàn khi nung nóng, có vật bắn ra, có tia ${f(25)}.</div>
<div style="margin-top:1mm"><b>Sau khi làm:</b> ${f(25)} sinh, sắp gọn thiết bị; bỏ chất thải vào đúng ${f(25)} quy định.</div></div>
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('THÍ NGHIỆM KHOẢNG CÁCH · BẪY · TRẢ BÀI')}
${h3(1, 'Thí nghiệm: càng xa ngọn lửa, càng bớt nóng', '3·1')}
<div class="fig-side" style="${fs(48)}"><div>
<div>Nhiệt độ phòng ${nw('25 °C')}, sai số mỗi số đọc ${nw('±1 °C')}; phần nóng hơn phòng ${dTdinh}.</div>
<table class="tbl-ct"><tr><th style="width:34mm">Cách đèn (cm)</th><th>2</th><th>5</th><th>10</th><th>20</th></tr>
<tr><td>Nhiệt kế chỉ (°C)</td><td>125</td><td>41</td><td>29</td><td>26</td></tr>
<tr><td>${dT} (°C)</td><td></td><td></td><td></td><td></td></tr></table></div>
${H.khoangCach()}</div>
<div class="card" style="margin-top:.6mm;padding:1mm 3mm">
<div><b>Rút ra:</b> từ 5 ra 10 cm, ${dT} giảm từ ${f(12)} °C xuống ${f(12)} °C. Ở 20 cm, ${dT} = ${f(12)} °C ${nw(`${m('\\le')} ${f(12)} °C`)} nên chưa kết luận được là khác phòng.</div>
<div>Vì vậy khi đèn đang cháy phải giữ ${f(25)} an toàn.</div></div>
${h3(2, 'III · Ba cái bẫy hay sập', '3·2')}
<div class="card" style="padding:1mm 3mm">
<div class="trap">${ck}<span><b>“Phích vừa khít ổ là dùng được.”</b> Thiết bị ghi ${nw('110 V ~')} mà cắm ổ ${nw('220 V')}: quá áp, dễ cháy. Vừa chân ${m('\\neq')} vừa ${f(25)}.</span></div>
<div class="trap">${ck}<span><b>“Hết lửa, hết khói là hết nóng.”</b> Cốc vừa đun sôi vẫn gây bỏng; mắt không ${f(25)} được nhiệt độ ${m('\\to')} dùng kẹp hoặc găng chịu nhiệt.</span></div>
<div class="trap">${ck}<span><b>“Mạch lắp đúng rồi, bật thử một giây.”</b> Chỉ bật khi ${f(25)} cho phép.</span></div></div>
${h3(3, 'IV · Trả bài 6 câu', '3·3')}
${box(`${tb('1. DC, AC, “+”, “−”, Input, Output nghĩa là gì?')}${lines(2)}
${tb('2. Hình dạng và màu của kí hiệu cho biết gì?')}${lines(2)}
${tb('3. Ba việc phải làm trước khi bắt đầu thí nghiệm?')}${lines(1)}
${tb('4. Bốn quy tắc khi làm việc với điện?')}${lines(2)}
${tb('5. Với vật nóng và tia laser phải làm gì, vì sao?')}${lines(2)}
${tb('6. Làm xong thí nghiệm phải làm gì?')}${lines(1)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/6 câu · chưa thuộc: ${f(25)} ${nw(`${m('\\to')} đọc lại ô ${f(12)} Tập`)}</div>
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('TỰ KIỂM TRA · BÀI TOÁN MẪU')}
${h3(1, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '4·1')}
${rkHai([1, 2, 3, 4], [5, 6, 7])}
${h3(2, 'V · Bài toán mẫu: xử lí tình huống ở bàn thực hành', '4·2')}
<div class="fig-side" style="${fs(52)}"><div class="card soft" style="padding:1.2mm 3mm;margin:0">Nhóm mắc bóng đèn ghi ${nw('6 V, DC')} vào bộ nguồn (Input ${nw('220 V ~')}; Output DC, núm vạch 3; 6; 9; 12 V). Núm đang ở vạch ${nw('12 V')}. Cốc nước đặt sát ổ cắm, dây nguồn vắt ngang lối đi. Nam định tháo bóng ra gắn lại khi nguồn còn bật; giáo viên chưa cho phép bắt đầu.
<div>Chỉ ra các lỗi, rồi xếp các việc cần làm trước khi bật nguồn.</div></div>${H.banLoi()}</div>
${h3(3, 'Phân tích đề')}
<table><tr><th style="width:62mm">Câu trong đề</th><th>Vi phạm quy tắc nào</th></tr>
<tr><td>“núm đang ở vạch 12 V”</td><td>Quá áp: gấp đôi định mức 6 V</td></tr>
<tr><td style="height:6.5mm">“cốc nước đặt sát ổ cắm”</td><td></td></tr>
<tr><td style="height:6.5mm">“dây nguồn vắt ngang lối đi”</td><td></td></tr>
<tr><td style="height:6.5mm">“tháo bóng khi nguồn còn bật”</td><td></td></tr>
<tr><td style="height:6.5mm">“giáo viên chưa cho phép”</td><td></td></tr></table>
${h3(4, 'Giải: các việc theo thứ tự')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl('Việc 1:', 2)}${wl('Việc 2:', 2)}${wl('Việc 3:', 2)}${wl('Việc 4:', 2)}${wl('Kiểm lại: mỗi lỗi đã có việc sửa chưa?', 1)}</div>
${h3(5, 'Điền bước còn thiếu: bóng ghi 3 V, DC')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div class="ln"><b>Bước 1 (cho sẵn):</b> tắt công tắc nguồn rồi mới tháo, gắn bóng.</div>
${wl('Bước 2: núm đặt ở vạch', 1)}${wl('Bước 3: trước khi bật nguồn cần', 1)}</div>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TẬP VỀ NHÀ · THỬ THÁCH · MANG VỀ')}
${K.btvn()}
${h3(2, 'Thử thách phân tầng', '5·2')}
<div class="fig-side" style="${fs(48)}">${box(wl(`${m('\\bigstar')} Kí hiệu “cấm lửa” thuộc nhóm nào, ý nghĩa gì?`, 2)
 + wl(`${m('\\bigstar\\bigstar')} Dụng cụ ghi ${nw('9 V, DC')}. Bộ nguồn đo được: vạch 3; 6; 9; 12 V cho 3,1; 6,2; 9,3; 12,4 V. Núm ở vạch nào, vôn kế dự kiến chỉ bao nhiêu?`, 3)
 + wl(`${m('\\bigstar\\bigstar\\bigstar')} Cần đun nước bằng đèn cồn trên bàn đang có bộ nguồn. Nêu ba điều chỉnh cách bố trí để an toàn.`, 5))}${H.banDen()}</div>
${h3(3, 'Câu vận dụng ở nhà', '5·3')}
${box(wl(`Nêu hai việc ở nhà em cần áp dụng quy tắc an toàn (ví dụ nước xa thiết bị điện, dùng kẹp khi cầm vật nóng); mỗi việc ghi rõ quy tắc nào.`, 6))}
${h3(4, 'VI · Mang về: điều em dễ quên nhất', '5·4')}
${box(wl('1.', 3) + wl('2.', 3) + wl('3.', 3))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Đọc nhãn thiết bị: DC, AC, Input, Output, cực + và −',
    de: `Bộ sạc có nhãn <b>Input: 100–240 V ~</b> và <b>Output: DC 5 V, 2 A</b>. Quạt mini ghi <b>5 V, DC</b>; dây đỏ của quạt nối cực mang dấu ${m('+')}.<br><b>a)</b> loại dòng điện ở Input và ở Output<br><b>b)</b> nối quạt vào đầu nào của bộ sạc<br><b>c)</b> quạt có phù hợp không; dây xanh nối cực nào`,
    nd: `khớp loại ${f(25)}, chỗ nối (Input/${f(25)}), số ${f(25)}`, a: ['a', 'b', 'c'], gi: 4, fig: H.sac(), cot: 2 },
  { t: 'Dạng 2 · Trung bình · Đọc kí hiệu qua hình dạng, màu rồi biết phải làm gì',
    de: `Thùng thu pin cũ dán bốn nhãn: <b>(1)</b> tam giác viền vàng, hình đầu lâu; <b>(2)</b> tròn đỏ gạch chéo, hình thùng rác; <b>(3)</b> tròn xanh, hình mặt nạ phòng độc; <b>(4)</b> hình cốc vỡ, không có khung.<br><b>a)</b> nhóm của mỗi nhãn; số nhãn có khung<br><b>b)</b> vứt pin vào thùng rác thường có được không, vì sao<br><b>c)</b> việc cần làm trước khi mở thùng`,
    nd: `nhìn ${f(25)} và ${f(25)} trước; tròn đỏ gạch chéo là nhóm ${f(25)}`, a: ['a', 'b', 'c'], gi: 4, fig: H.nhanThung(), cot: 2 },
  { t: 'Dạng 3 · Khó · Giữ khoảng cách: đọc số đo, so với sai số, áp dụng quy tắc',
    de: `Nhiệt kế đặt cạnh ngọn đèn cồn đang cháy, lần lượt cách ${m('3;\\ 8;\\ 15;\\ 30\\ \\mathrm{cm}')}, chỉ ${m('70;\\ 33;\\ 27;\\ 25{,}5\\ ^\\circ\\mathrm{C}')}. Nhiệt độ phòng ${m('25\\ ^\\circ\\mathrm{C}')}, sai số mỗi số đọc ${m('\\pm1\\ ^\\circ\\mathrm{C}')}.<br><b>a)</b> ${dT} ở 3 cm<br><b>b)</b> ${dT} giảm bao nhiêu từ 3 cm ra 8 cm<br><b>c)</b> vị trí gần đèn nhất mà ${m('\\Delta T\\le1\\ ^\\circ\\mathrm{C}')}<br><b>d)</b> quy tắc nào được minh hoạ; khi đèn đang cháy nên đứng thế nào`,
    nd: `${dTdinh} = ${f(12)} − ${f(12)}; ${m('\\Delta T\\le')} ${f(12)} °C thì chưa kết luận được là khác nhiệt độ phòng`, a: ['a', 'b', 'c', 'd'], gi: 5, fig: H.khoangCach('Cách đèn 3; 8; 15; 30 cm.', [3, 8, 15, 30]), cot: 2 },
  { t: 'Dạng 4 · Khó · Xử lí sự cố bất ngờ ở bàn thực hành',
    de: `Đèn cồn trên bàn thực hành bị đổ, cồn cháy lan trên mặt bàn, gần bộ nguồn đang bật.<br><b>a)</b> việc đầu tiên của mọi bạn trong nhóm<br><b>b)</b> việc của bạn ngồi gần công tắc nguồn<br><b>c)</b> việc của bạn khác cùng lúc<br><b>d)</b> vì sao không tạt nước vội vào chỗ cháy`,
    nd: `${f(25)} tay, lùi ra ${m('\\to')} ngắt ${f(25)} nếu an toàn ${m('\\to')} báo ${f(25)} ${m('\\to')} làm theo hướng dẫn`, a: ['a', 'b', 'c', 'd'], gi: 4, cot: 2 },
];

// Bài tương tự: mỗi dạng 2 bài, đáp số tính bằng Python 13/11/2026. Giải vào vở (thầy chốt 10/11): ô đáp số theo nhãn ý, in lật ngược ở cuối trang.
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
  tieuDe: ['DẠNG 1–2', 'DẠNG 3–4'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Đèn pin nhỏ ghi <b>3 V, DC</b>, dây đỏ nối cực mang dấu ${m('+')}. Bộ nguồn: <b>Input 220 V ~</b>; Output có cổng DC (cực đỏ ${m('+')}, cực xanh ${m('-')}) và cổng AC; núm vạch 3; 6; 9; 12 V.<br><b>a)</b> loại dòng điện ở Input<br><b>b)</b> nối đèn vào cổng nào, núm ở vạch mấy vôn<br><b>c)</b> dây đỏ của đèn nối cực màu gì`, o: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], ow: 28 },
    { t: 'Dạng 1 · Bài 2', de: `Đèn bàn LED ghi <b>12 V, DC</b>. Hai bộ đổi nguồn: bộ A ghi <b>Input 220 V ~, Output 12 V, DC</b>; bộ B ghi <b>Input 220 V ~, Output 12 V, AC</b>.<br><b>a)</b> bộ nào dùng được với đèn<br><b>b)</b> đèn nối vào Input hay Output<br><b>c)</b> đầu nào của bộ đổi nguồn cắm vào ổ cắm điện`, o: ['a', 'b', 'c'], ow: 28 },
    { t: 'Dạng 2 · Bài 1', de: `Tủ hoá chất dán ba nhãn: <b>(1)</b> tam giác viền vàng, hình tia chớp; <b>(2)</b> tròn đỏ gạch chéo, hình ngọn lửa; <b>(3)</b> tròn xanh, hình mặt nạ phòng độc.<br><b>a)</b> nhóm của nhãn (1)<br><b>b)</b> nhóm của nhãn (2)<br><b>c)</b> nhóm của nhãn (3)<br><b>d)</b> có được châm lửa thử cạnh tủ không`, fig: H.nhanTu('Ba nhãn trên tủ.'), fw: 40, o: ['a', 'b', 'c', 'd'], ow: 28 },
    { t: 'Dạng 2 · Bài 2', de: `Một tủ dán sáu nhãn: ba tam giác (chất dễ cháy, chất độc, tia laser), một tròn đỏ gạch chéo (cấm lửa), một tròn xanh (đeo mặt nạ phòng độc), một hình cốc vỡ không có khung.<br><b>a)</b> số nhãn có khung<br><b>b)</b> số nhãn thuộc nhóm cảnh báo<br><b>c)</b> nhãn nào cho biết việc không được làm<br><b>d)</b> nhóm của nhãn cốc vỡ`, o: ['a', 'b', 'c', 'd'], ow: 28 },
    nhap(8),
  ], [
    { t: 'Dạng 3 · Bài 1', de: `Nhiệt kế đặt cạnh ngọn đèn cồn cháy, lần lượt cách ${m('4;\\ 10;\\ 20;\\ 40\\ \\mathrm{cm}')}, chỉ ${m('62;\\ 31;\\ 26{,}8;\\ 25{,}4\\ ^\\circ\\mathrm{C}')}. Nhiệt độ phòng ${m('25\\ ^\\circ\\mathrm{C}')}, sai số mỗi số đọc ${m('\\pm1\\ ^\\circ\\mathrm{C}')}; ${dTdinh}.<br><b>a)</b> ${dT} ở 4 cm<br><b>b)</b> ${dT} giảm bao nhiêu từ 4 cm ra 10 cm<br><b>c)</b> vị trí gần đèn nhất mà ${m('\\Delta T\\le1\\ ^\\circ\\mathrm{C}')}<br><b>d)</b> có kết luận được “ở 30 cm bằng nhiệt độ phòng” không`, fig: H.khoangCach('Cách đèn 4; 10; 20; 40 cm.', [4, 10, 20, 40]), fw: 44, o: ['a', 'b', 'c', 'd'], ow: 28 },
    { t: 'Dạng 3 · Bài 2', de: `Tấm kim loại nung nóng; nhiệt kế đặt lần lượt cách ${m('5;\\ 12;\\ 25;\\ 50\\ \\mathrm{cm}')}, chỉ ${m('80;\\ 40;\\ 28{,}5;\\ 26{,}5\\ ^\\circ\\mathrm{C}')}. Nhiệt độ phòng ${m('26\\ ^\\circ\\mathrm{C}')}, sai số ${m('\\pm1\\ ^\\circ\\mathrm{C}')}; ${dTdinh}.<br><b>a)</b> ${dT} ở 5 cm<br><b>b)</b> ${dT} giảm bao nhiêu từ 5 cm ra 12 cm<br><b>c)</b> vị trí gần nhất mà ${m('\\Delta T\\le1\\ ^\\circ\\mathrm{C}')}<br><b>d)</b> ${dT} ở 12 cm bằng bao nhiêu phần trăm ${dT} ở 5 cm (làm tròn đến 1 %)`, o: ['a', 'b', 'c', 'd'], ow: 28 },
    { t: 'Dạng 4 · Bài 1', de: `Đang làm thí nghiệm, dây nguồn của bộ nguồn bốc khói và có mùi khét.<br><b>a)</b> việc đầu tiên của cả nhóm<br><b>b)</b> việc của bạn ngồi gần công tắc, nếu không phải đi qua chỗ có khói<br><b>c)</b> báo cho ai<br><b>d)</b> có nên rút phích bằng tay ướt cho nhanh không`, o: ['a', 'b', 'c', 'd'], ow: 30 },
    { t: 'Dạng 4 · Bài 2', de: `Ổ cắm gắn với bộ nguồn bật ra tia lửa điện, một góc bàn có khói.<br><b>a)</b> việc đầu tiên của mọi bạn<br><b>b)</b> việc của bạn ngồi gần công tắc nguồn (nếu an toàn)<br><b>c)</b> ai quyết định cách xử lí tiếp theo<br><b>d)</b> tạt nước vào bộ nguồn có đúng không`, o: ['a', 'b', 'c', 'd'], ow: 30 },
    nhap(7),
  ]],
  dap: [
    `D1·1: a) xoay chiều · b<sub>1</sub>) DC · b<sub>2</sub>) 3 V · c) đỏ &nbsp;|&nbsp; D1·2: a) bộ A · b) Output · c) Input &nbsp;|&nbsp; D2·1: a) cảnh báo · b) cấm · c) bắt buộc · d) không &nbsp;|&nbsp; D2·2: a) 5 · b) 3 · c) cấm lửa · d) bảo quản`,
    `D3·1: a) 37 °C · b) 31 °C · c) 40 cm · d) không (30 cm chưa đo) &nbsp;|&nbsp; D3·2: a) 54 °C · b) 40 °C · c) 50 cm · d) 26 % &nbsp;|&nbsp; D4·1: a) dừng tay, lùi ra · b) tắt công tắc nguồn · c) giáo viên · d) không &nbsp;|&nbsp; D4·2: a) dừng tay, lùi ra · b) tắt công tắc nguồn · c) giáo viên · d) không`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [2, 2], kq: [[1, 2], [3, 4]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'nhãn thiết bị 1·4 · kí hiệu 2·1 · mười quy tắc 2·3 · khoảng cách 3·1 · ba bẫy 3·2 · bài toán mẫu 4·2 · dạng 1–2 → 6·1 · dạng 3–4 → 7·1',
  out: process.argv[2],
});
