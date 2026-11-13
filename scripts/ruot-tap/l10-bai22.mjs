// Ruột tập VL10 – Bài 22 · Thực hành: Tổng hợp lực (lesson id 67). Quyển Chương 3 lớp 10: bài 22 = tr. 109–120 (baiDau 13).
// Khung: khung.mjs (bố cục bài 14: 1–5 học · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Bài THỰC HÀNH (web không có Bài tập mẫu): tr.1 nhắc lại · tr.2 dụng cụ + ý tưởng lực cân bằng · tr.3 các bước + hai bẫy · tr.4 bảng số liệu + sai số
// · tr.5 vẽ hình bình hành + kết luận + báo cáo · tr.6–7 bốn dạng xử lí số liệu thay Dạng.
// Nội dung theo bài web (book/cache/67.json, tải 13/11/2026). Đáp số mọi bài (dạng, tương tự) tính bằng Python 13/11/2026.
// Chạy: node scripts/ruot-tap/l10-bai22.mjs [file.pdf]   → scripts/ruot-tap/out/ruot-tap-vl10-bai22.pdf
//       node scripts/ruot-tap/l10-bai22.mjs --hinh       → chụp từng hình ở cỡ in vào out/hinh-l10-bai22/
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL10b22 as H } from './hinh-l10-bai22.mjs';

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
  const out = resolve(HERE, 'out/hinh-l10-bai22'); mkdirSync(out, { recursive: true });
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

const OFF = (22 - 13) * 12;
const K = khoiTao({ bai: 22, lid: 67, lop: 10, baiDau: 13, ten: 'THỰC HÀNH: TỔNG HỢP LỰC', sub: 'Vật lí 10 · Chương 3: Động lực học' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const Ft = m('F');
const F = (s = '') => m(`F${s ? `_${s}` : ''}`), F1 = F('1'), F2 = F('2'), F3 = F('3'), Fv = m('F_{\\text{vẽ}}'), al = m('\\alpha');
const dl = m('\\delta'), Dl = m('\\Delta');
const N = (s) => nw(m(`${s}\\ \\mathrm N`)), deg = (s) => nw(m(`${s}^\\circ`)), cm = (s) => nw(m(`${s}\\ \\mathrm{cm}`));
const cs = nw(`${m('\\Delta F=0{,}1\\ \\mathrm N')} mỗi lực kế · tỉ lệ xích ${cm('1')} ứng ${N('0{,}5')}`);

const ttCss = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';

const p1 = `${ttCss}<section class="page">
${head('BÀI 22 · THỰC HÀNH: TỔNG HỢP LỰC', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Bố trí ba lực kế và nút O để tổng hợp hai lực đồng quy: đọc ${F1}, ${F2}, ${F3}, đo góc ${al}`)}
${dong(`${ck}Vẽ hình bình hành theo tỉ lệ xích, đo đường chéo, so với số chỉ lực kế`)}
${dong(`${ck}Kết luận bằng độ lệch ${dl} và sai số ${Dl}, không bằng cảm giác “gần bằng”`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Khung ảnh nặng ${N('2{,}0')} treo bằng hai dây giống hệt nhau, đối xứng. Em dời hai đinh ra xa để góc giữa hai dây tăng từ ${deg('60')} lên ${deg('120')}. Lực căng của mỗi dây thay đổi thế nào?</p>
<div class="fig-side" style="${fs(48)}"><div>
${opt('A', `Không đổi, vì trọng lượng khung vẫn là ${N('2{,}0')}`)}
${opt('B', 'Giảm đi, vì dây xoạc ra thì mỗi dây gánh nhẹ hơn')}
${opt('C', `Tăng lên, vì hai lực nghiêng vẫn phải đỡ ${N('2{,}0')}`)}
${opt('D', 'Bằng một nửa trọng lượng, vì hai dây giống hệt nhau')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 1)}</div>
${H.khungAnh()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, `II.1 · Nhắc lại: hợp lực của hai lực đồng quy`, '1·4')}
<div class="card fig-side" style="${fs(48)};padding:1.2mm 3mm"><div>
<div>Hai lực ${F1}, ${F2} chung gốc O, hợp góc ${al}. Quy tắc hình bình hành: ${Ft} là đường ${f(18)} qua O.</div>
<div style="margin-top:.6mm">${m('F=')} ${nw(`${m('\\sqrt{\\ \\ }')} <span class="fill" style="min-width:38mm;height:9mm"></span>`)}</div>
<div class="hint" style="margin:.3mm 0">Đơn vị: ${m('F_1,F_2,F')}: N · ${al}: độ · ${cs}</div>
<div style="margin-top:.6mm">${nw(`${m('\\alpha=0^\\circ:\\ F=')} ${f(20)}`)} &nbsp;${nw(`${m('\\alpha=90^\\circ:\\ F=')} ${f(20)}`)}</div>
<div style="margin-top:.6mm">${nw(`${m('\\alpha=180^\\circ:\\ F=')} ${f(20)}`)}</div></div>
${H.hbh()}</div>
${h3(5, 'Làm nhanh', '1·5')}
${box(cau(`${m('F_1=1{,}5')} N và ${m('F_2=2{,}0')} N đồng quy, hai dây vuông góc. Hợp lực ${Ft} có độ lớn bao nhiêu?`, 1))}
${foot(1)}</section>`;

const bangDc = (rows) => `<table><tr><th style="width:38mm">Dụng cụ</th><th>Để làm gì · độ chia</th></tr>${rows.map((x) => `<tr><td style="height:14mm">${x}</td><td></td></tr>`).join('')}</table>`;
const p2 = `<section class="page">
${head('DỤNG CỤ · BỐ TRÍ · LỰC CÂN BẰNG')}
${h3(1, 'II.1 · Dụng cụ và bố trí', '2·1')}
<div class="fig-side" style="${fs(62)}"><div>
${bangDc(['Giá đỡ, bảng giấy', `Ba lực kế ${N('5')}`, 'Dây mảnh, nút O', 'Vật nặng', 'Thước, thước đo độ'])}
</div>${H.boTri()}</div>
${h3(2, 'Vì sao lực kế 3 đo được lực tổng hợp?', '2·2')}
<div class="card" style="padding:1.2mm 3mm">
<div>Nút O đứng yên nên hợp lực lên O bằng ${f(10)}. Vậy ${m('\\vec F+\\vec F_3=')} ${f(10)}.</div>
<div style="margin-top:.6mm">${F3} so với ${Ft}: cùng ${f(18)}, cùng ${f(18)}, ${f(18)} chiều.</div>
<div style="margin-top:.6mm">${Fv}: ${f(22)} từ hình bình hành; ${F3}: số chỉ lực kế ${f(8)}.</div></div>
${h3(3, 'Độ chia và cách đọc', '2·3')}
<div class="fig-side" style="${fs(62)}"><div>
<div>Mặt lực kế ${N('5')} chia thành các vạch. Mỗi độ chia ứng ${f(10)} N. Nhìn thẳng mặt chỉ để tránh sai số do nhìn lệch.</div>
<div style="margin-top:1.2mm">Kim chỉ trên hình: ${nw(`${m('F=')} ${f(16)} N`)}</div></div>${H.doChia()}</div>
${h3(4, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '2·4')}
${rkHai([1, 2, 3, 4], [5, 6, 7, 8])}
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('CÁC BƯỚC ĐO · HAI CÁI BẪY SỐ LIỆU')}
${h3(1, 'II.2 · Các bước đo', '3·1')}
<div class="card" style="padding:1.2mm 3mm">
<div class="trap"><b>1.</b><span>Chỉnh số ${f(8)} từng lực kế ở đúng tư thế dùng. Buộc ba dây vào nút O, chờ O ${f(22)}.</span></div>
<div class="trap"><b>2.</b><span>Chấm hai điểm trên mỗi dây để đánh dấu phương; đọc ${F1}, ${F2}, ${F3} (ghi bảng tr. ${4 + OFF}).</span></div>
<div class="trap"><b>3.</b><span>Lấy giấy ra, nối các chấm qua O, đo góc ${al} giữa hai dây. Làm ${f(14)} lần, đổi vị trí hai chốt hoặc đổi vật.</span></div>
<div class="trap"><b>4.</b><span>Vẽ hình bình hành (tr. ${5 + OFF}), đo đường chéo, tính ${Fv}; so với ${F3}.</span></div>
<div style="margin-top:.6mm"><b>Vì sao</b> phải đợi O đứng yên rồi mới đọc số?</div>${lines(1)}</div>
${h3(2, 'III · Bẫy 1: số 0 của lực kế', '3·2')}
<div class="fig-side" style="${fs(44)}"><div>
<table><tr><th>Tình huống</th><th style="width:50mm">Em làm</th></tr>
<tr><td style="height:9mm">Treo thẳng đứng</td><td></td></tr>
<tr><td style="height:9mm">Kéo nghiêng hoặc nằm ngang</td><td></td></tr>
<tr><td style="height:9mm">Chưa móc gì, kim chỉ ${N('0{,}3')}</td><td></td></tr></table>
<div style="margin-top:1mm;line-height:1.35">Lực kế 1 và 2 chưa chỉnh số 0, mỗi cái chỉ ${N('+0{,}1')} khi chưa móc gì. Hình bình hành vẽ từ số đọc: ${Ft} vẽ ${ck}lớn hơn ${ck}nhỏ hơn ${ck}bằng ${Ft} thật.</div></div>${H.soKhong()}</div>
${h3(3, `III · Bẫy 2: góc ${al} ở nút O`, '3·3')}
<div class="fig-side" style="${fs(52)}"><div>
<div>Cho ${nw(m('F_1=2{,}0\\ \\mathrm N'))}, ${nw(m('F_2=3{,}0\\ \\mathrm N'))}, ${nw(m('\\alpha=120^\\circ'))} (đo ở nút O giữa hai dây).</div>
<div style="margin-top:.8mm">Công thức dùng ${m('\\alpha')} = ${f(12)}°: ${nw(`${m('F=')} ${f(26)} N`)}</div>
<div style="margin-top:.8mm">Vẽ nối đuôi: góc ở đỉnh (dấu ?) là ${f(14)}°. Khi dùng công thức vẫn thay góc ${f(8)}.</div></div>${H.gocAlpha()}</div>
${K.btvn().replace('<i>1</i>', '<i>4</i>')}
${foot(3)}</section>`;

const bangDo = `<table class="tbl-ct" style="text-align:center">
<tr><th style="width:11mm">Lần</th><th>${F1} (N)</th><th>${F2} (N)</th><th>${al} (độ)</th><th>${F3} đọc (N)</th><th>Số 0 lệch (N)</th><th>${F3} đúng (N)</th></tr>
${[1, 2, 3].map((i) => `<tr><td style="height:9mm"><b>${i}</b></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>`).join('')}</table>`;
const bangVe = `<table class="tbl-ct" style="text-align:center">
<tr><th style="width:11mm">Lần</th><th>Cạnh ${F1} (cm)</th><th>Cạnh ${F2} (cm)</th><th>Chéo (cm)</th><th>${Fv} (N)</th><th>${dl} (N)</th><th>${dl} ${m('\\le')} ${Dl}?</th></tr>
${[1, 2, 3].map((i) => `<tr><td style="height:9mm"><b>${i}</b></td><td></td><td></td><td></td><td></td><td></td><td>${ck}</td></tr>`).join('')}</table>`;
const p4 = `<section class="page">
${head('BẢNG SỐ LIỆU · SAI SỐ')}
${h3(1, 'II.3 · Số liệu đo của nhóm em', '4·1')}
${bangDo}
<div class="hint" style="margin:.8mm 0">Số 0 lệch: số chỉ khi chưa móc gì (không lệch thì ghi 0). ${F3} đúng = ${F3} đọc − số 0 lệch.</div>
${h3(2, 'II.4 · Vẽ hình bình hành rồi so với lực đo', '4·2')}
<div class="card soft" style="padding:1.2mm 3mm">Tỉ lệ xích ${cm('1')} ứng ${N('0{,}5')}: cạnh vẽ ${m('=\\dfrac{F}{0{,}5}')} cm; ${nw(`${Fv} = chéo ${m('\\times 0{,}5')}`)}. Độ lệch ${nw(`${dl} = |${Fv} − ${F3}|`)}.</div>
${bangVe}
${h3(3, `Sai số ${Dl} của bài này`, '4·3')}
<div class="card" style="padding:1.2mm 3mm">
<div>Mỗi lực kế sai ${nw(m('\\Delta F=0{,}1\\ \\mathrm N'))}. ${Fv} dựng từ ${F1}, ${F2}, rồi so với ${F3} nên ${nw(`${Dl} = ${m('\\Delta F_1+\\Delta F_2+\\Delta F_3')} = ${f(14)} N`)}</div>
<div style="margin-top:.6mm">${nw(`${dl} ${m('\\le')} ${Dl}`)}: ${f(40)}. ${nw(`${dl} > ${Dl}`)}: ${f(40)}</div></div>
${h3(4, 'Quan sát và so sánh', '4·4')}
<div class="card soft" style="padding:1.2mm 3mm"><div>Lần có ${dl} lớn nhất: lần ${f(14)}, ${nw(`${dl} = ${f(14)} N`)}. Cả ba lần ${Ft} vẽ cùng lớn hơn hoặc cùng nhỏ hơn ${F3}? ${f(26)}</div>${lines(1)}</div>
${h3(5, 'Làm nhanh: ba lần đo của một nhóm', '4·5')}
<div class="card" style="padding:1.2mm 3mm">
<table class="tbl-ct" style="text-align:center"><tr><th style="width:14mm">Lần</th><th>${dl} (N)</th><th>${dl} ${m('\\le')} ${Dl} = ${N('0{,}3')}?</th></tr>
${[['1', '0{,}10'], ['2', '0{,}25'], ['3', '0{,}35']].map(([i, d]) => `<tr><td style="height:7mm"><b>${i}</b></td><td>${m(d)}</td><td>${ck}hợp &nbsp;${ck}chưa hợp</td></tr>`).join('')}</table>
<div style="margin-top:.8mm">Lần chưa hợp: việc đầu tiên em kiểm là ${f(40)}</div></div>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('VẼ HÌNH BÌNH HÀNH · KẾT LUẬN · BÁO CÁO')}
${h3(1, 'II.5 · Hình bình hành của nhóm em (một lần đo)', '5·1')}
<div style="width:123.6mm">${H.luoi()}</div>
<div style="margin:.5mm 0">${nw(`${m('F_1=')} ${f(14)} N`)} · ${nw(`${m('F_2=')} ${f(14)} N`)} · ${nw(`${m('\\alpha=')} ${f(14)}°`)} · chéo ${f(12)} cm · ${nw(`${Fv} = ${f(12)} N`)}</div>
${h3(2, 'Kết luận', '5·2')}
<div class="card soft" style="padding:1.2mm 3mm"><div>${nw(`${dl} = ${f(12)} N`)}, ${nw(`${Dl} = ${f(10)} N`)}: ${ck}hợp quy tắc hình bình hành trong sai số &nbsp;${ck}chưa hợp, cần kiểm lại</div></div>
${h3(3, 'Câu hỏi báo cáo', '5·3')}
${box(`<div style="padding-top:.6mm"><b>1.</b> Nguồn sai số lớn nhất của nhóm em là gì? Cách giảm?</div>${lines(2)}
<div style="padding-top:.6mm"><b>2.</b> Một lần ${dl} vượt ${Dl} thì kiểm gì trước khi nghi ngờ quy tắc?</div>${lines(1)}
<div style="padding-top:.6mm"><b>3.</b> Cả ba lần ${Fv} đều lớn hơn ${F3} khoảng ${N('0{,}2')} và đều có ${dl} ${m('\\le')} ${Dl}. Có kết luận được quy tắc đúng không? Nguyên nhân có thể và cách kiểm?</div>${lines(2)}`)}
${foot(5)}</section>`;

// ---- Bốn dạng xử lí số liệu (thay Bài tập mẫu): 1 dễ · 2 TB · 3 hiệu chỉnh số 0 · 4 khó (hai dây treo vật)
const dang = [
  { t: `Dạng 1 · Dễ · Hai lực vuông góc: dựng hình, tính ${Fv}, so với ${F3}`,
    de: `Ba lực kế: ${nw(m('F_1=0{,}9\\ \\mathrm N'))}, ${nw(m('F_2=1{,}2\\ \\mathrm N'))}, hai dây vuông góc; lực kế 3 chỉ ${nw(m('F_3=1{,}6\\ \\mathrm N'))}. Tỉ lệ xích ${cm('1')} ứng ${N('0{,}5')}, mỗi lực kế sai ${N('0{,}1')}.<br><b>a)</b> độ dài hai cạnh vẽ<br><b>b)</b> đường chéo và ${Fv}<br><b>c)</b> độ lệch ${dl}<br><b>d)</b> sai số ${Dl}; kết luận`,
    nd: `Cạnh ${nw(`= ${m('F/0{,}5')}`)}; hình ${f(14)} nên chéo ${nw(m('=\\sqrt{a^2+b^2}'))}; ${nw(`${dl} = |${Fv} − ${F3}|`)}; ${nw(`${Dl} = ${m('3\\Delta F')}`)} so với ${dl}`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c', 'd<sub>1</sub>', 'd<sub>2</sub>'], gi: 6, fig: H.hbh('Hai cạnh vẽ chung gốc O, nét đứt hoàn thành hình.') },
  { t: `Dạng 2 · Trung bình · Góc ${al} bất kì: công thức, chéo đo được, độ lệch`,
    de: `${nw(m('F_1=2{,}0\\ \\mathrm N'))}, ${nw(m('F_2=3{,}0\\ \\mathrm N'))}, góc giữa hai dây ở nút O là ${nw(m('\\alpha=60^\\circ'))}. Đường chéo vẽ đo được ${cm('8{,}7')} (tỉ lệ ${cm('1')} ứng ${N('0{,}5')}); lực kế 3 chỉ ${nw(m('F_3=4{,}5\\ \\mathrm N'))}; ${nw(m('\\Delta F=0{,}1\\ \\mathrm N'))} mỗi lực kế.<br><b>a)</b> ${Ft} tính bằng công thức<br><b>b)</b> ${Fv} từ đường chéo<br><b>c)</b> độ lệch ${dl}<br><b>d)</b> kết luận so với ${Dl}`,
    nd: `${nw(`${m('F^2=F_1^2+F_2^2+')} ${f(18)}`)}; ${nw(`${Fv} = chéo ${m('\\times 0{,}5')}`)}; ${nw(`${dl} = |${Fv} − ${F3}|`)}`, a: ['a', 'b', 'c', 'd'], gi: 5 },
  { t: 'Dạng 3 · Khó hơn · Hiệu chỉnh số 0 của lực kế rồi kết luận',
    de: `${nw(m('F_1=2{,}4\\ \\mathrm N'))}, ${nw(m('F_2=3{,}2\\ \\mathrm N'))}, hai dây vuông góc. Nhóm thay một lực kế 3 khác mà chưa chỉnh số 0: lực kế đọc ${nw(m('4{,}4\\ \\mathrm N'))}; treo thẳng, chưa móc vật thì nó chỉ ${nw(m('0{,}3\\ \\mathrm N'))}. Tỉ lệ xích ${cm('1')} ứng ${N('0{,}5')}; ${nw(m('\\Delta F=0{,}1\\ \\mathrm N'))} mỗi lực kế.<br><b>a)</b> ${Fv} (qua đường chéo)<br><b>b)</b> ${dl} khi dùng số đọc ${N('4{,}4')}; so với ${Dl}<br><b>c)</b> ${F3} sau khi trừ số 0 lệch<br><b>d)</b> ${dl} mới; kết luận`,
    nd: `Số 0 lệch ${nw('+0,3')} cộng vào ${f(14)} lần đọc; ${nw(`${F3} đúng = đọc − ${f(10)}`)}`, a: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c', 'd<sub>1</sub>', 'd<sub>2</sub>'], gi: 6 },
  { t: `Dạng 4 · Khó · Hai dây treo vật: lực căng phụ thuộc góc ${al}`,
    de: `Vật nặng ${N('3{,}0')} treo bằng hai dây giống hệt nhau, đối xứng, góc giữa hai dây là ${al}. Mỗi dây có lực căng ${m('T')}, hợp lực của hai dây cân bằng với ${m('P')}.<br><b>a)</b> ${m('T')} khi ${nw(m('\\alpha=60^\\circ'))}<br><b>b)</b> ${m('T')} khi ${nw(m('\\alpha=120^\\circ'))}<br><b>c)</b> dây chịu được tối đa ${N('4{,}0')}: góc ${al} lớn nhất không làm dây đứt`,
    nd: `Mỗi dây lệch ${nw(m('\\alpha/2'))} so với phương đứng: ${nw(`${m('2T\\cos\\dfrac{\\alpha}{2}=')} ${f(10)}`)}; ${al} tăng thì ${m('T')} ${f(14)}`, a: ['a', 'b', 'c'], cot: 3, gi: 5, fig: H.khungAnh(`Hai dây treo vật; ${al} là góc giữa hai dây.`, 'vật') },
];

const oY = (s, o, w = {}) => s.split('<br>').map((p) => {
  const y = p.match(/^<b>([a-d])\)<\/b>/);
  if (!y) return `<div>${p}</div>`;
  const ls = o.filter((l) => l[0] === y[1]);
  return `<div class="yo"><span>${p}</span><span class="oo">${ls.map((l) => `<span class="nw"><b>${l})</b>${f(typeof w === 'object' ? (w[l] ?? 25) : w)}</span>`).join('')}</span></div>`;
}).join('');
const ttDe = (b) => b.fig ? `<div class="fig-side" style="grid-template-columns:1fr ${b.fw}mm">${`<div>${oY(b.de, b.o, b.ow)}</div>`}${b.fig}</div>` : oY(b.de, b.o, b.ow);
const vaoVo = (ds) => ds.map((b) => (b.o ? { t: b.t, de: ttDe(b), k: 0 } : b));
const nhap = (n) => ({ t: '<span class="nhap-t">Nháp / chỗ em còn vướng</span>', de: lines(n), k: 0 });
const kc = `Tỉ lệ xích ${cm('1')} ứng ${N('0{,}5')}; ${nw(m('\\Delta F=0{,}1\\ \\mathrm N'))} mỗi lực kế`;
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–3', 'DẠNG 3–4'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `${nw(m('F_1=0{,}6\\ \\mathrm N'))}, ${nw(m('F_2=0{,}8\\ \\mathrm N'))}, hai dây vuông góc; ${nw(m('F_3=1{,}2\\ \\mathrm N'))}. ${kc}.<br><b>a)</b> độ dài hai cạnh vẽ; đường chéo<br><b>b)</b> ${Fv} và ${dl}<br><b>c)</b> ${Dl}; kết luận`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], ow: { c: 40 } },
    { t: 'Dạng 1 · Bài 2', de: `${nw(m('F_1=1{,}5\\ \\mathrm N'))}, ${nw(m('F_2=3{,}6\\ \\mathrm N'))}, hai dây vuông góc; ${nw(m('F_3=3{,}5\\ \\mathrm N'))}. ${kc}.<br><b>a)</b> độ dài hai cạnh vẽ; đường chéo<br><b>b)</b> ${Fv} và ${dl}<br><b>c)</b> ${Dl}; kết luận`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], ow: { c: 40 } },
    { t: 'Dạng 2 · Bài 1', de: `${nw(m('F_1=1{,}0\\ \\mathrm N'))}, ${nw(m('F_2=2{,}0\\ \\mathrm N'))}, góc giữa hai dây ${nw(m('\\alpha=60^\\circ'))}; chéo đo được ${cm('5{,}3')}; ${nw(m('F_3=2{,}5\\ \\mathrm N'))}. ${kc}.<br><b>a)</b> ${Ft} bằng công thức<br><b>b)</b> ${Fv} từ đường chéo<br><b>c)</b> ${dl}<br><b>d)</b> kết luận so với ${Dl}`, o: ['a', 'b', 'c', 'd'], ow: { d: 36 } },
    { t: 'Dạng 2 · Bài 2', de: `${nw(m('F_1=2{,}0\\ \\mathrm N'))}, ${nw(m('F_2=1{,}5\\ \\mathrm N'))}, ${nw(m('\\alpha=120^\\circ'))}; chéo đo được ${cm('3{,}6')}; ${nw(m('F_3=2{,}2\\ \\mathrm N'))}. ${kc}.<br><b>a)</b> ${Ft} bằng công thức<br><b>b)</b> ${Fv} từ đường chéo<br><b>c)</b> ${dl}<br><b>d)</b> kết luận so với ${Dl}`, o: ['a', 'b', 'c', 'd'], ow: { d: 36 } },
    { t: 'Dạng 3 · Bài 1', de: `${nw(m('F_1=1{,}2\\ \\mathrm N'))}, ${nw(m('F_2=1{,}6\\ \\mathrm N'))}, hai dây vuông góc. Lực kế 3 đọc ${nw(m('2{,}5\\ \\mathrm N'))}; chưa móc vật nó chỉ ${nw(m('0{,}3\\ \\mathrm N'))}. ${kc}.<br><b>a)</b> ${Fv}<br><b>b)</b> ${dl} khi chưa hiệu chỉnh; kết luận<br><b>c)</b> ${F3} sau hiệu chỉnh<br><b>d)</b> ${dl} mới; kết luận`, o: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c', 'd<sub>1</sub>', 'd<sub>2</sub>'], ow: { 'b<sub>2</sub>': 26, 'd<sub>2</sub>': 26 } },
  ], [
    { t: 'Dạng 3 · Bài 2', de: `${nw(m('F_1=1{,}0\\ \\mathrm N'))}, ${nw(m('F_2=2{,}4\\ \\mathrm N'))}, hai dây vuông góc. Lực kế 3 đọc ${nw(m('3{,}1\\ \\mathrm N'))}; chưa móc vật nó chỉ ${nw(m('0{,}4\\ \\mathrm N'))}. ${kc}.<br><b>a)</b> ${Fv}<br><b>b)</b> ${dl} khi chưa hiệu chỉnh; kết luận<br><b>c)</b> ${F3} sau hiệu chỉnh<br><b>d)</b> ${dl} mới; kết luận`, o: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c', 'd<sub>1</sub>', 'd<sub>2</sub>'], ow: { 'b<sub>2</sub>': 26, 'd<sub>2</sub>': 26 } },
    { t: 'Dạng 4 · Bài 1', de: `Vật ${N('2{,}4')} treo bằng hai dây giống nhau, đối xứng, góc giữa hai dây ${al}; mỗi dây lực căng ${m('T')}.<br><b>a)</b> ${m('T')} khi ${nw(m('\\alpha=90^\\circ'))}<br><b>b)</b> ${m('T')} khi ${nw(m('\\alpha=120^\\circ'))}<br><b>c)</b> dây chịu tối đa ${N('3{,}0')}: góc ${al} lớn nhất`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 4 · Bài 2', de: `Vật ${N('4{,}0')} treo bằng hai dây giống nhau, đối xứng, góc giữa hai dây ${al}.<br><b>a)</b> ${m('T')} khi ${nw(m('\\alpha=60^\\circ'))}<br><b>b)</b> ${m('T')} khi ${nw(m('\\alpha=90^\\circ'))}<br><b>c)</b> dây chịu tối đa ${N('6{,}0')}: góc ${al} lớn nhất`, o: ['a', 'b', 'c'] },
    nhap(18),
  ]],
  dap: [
    `D1·1: a) 1,2 cm; 1,6 cm · b) chéo 2,0 cm; F vẽ 1,0 N; ${dl} 0,2 N · c) ${Dl} = 0,3 N: hợp &nbsp;|&nbsp; D1·2: a) 3,0 cm; 7,2 cm · b) chéo 7,8 cm; F vẽ 3,9 N; ${dl} 0,4 N · c) ${Dl} = 0,3 N: chưa hợp &nbsp;|&nbsp; D2·1: a) 2,65 N · b) 2,65 N · c) 0,15 N · d) hợp &nbsp;|&nbsp; D2·2: a) 1,80 N · b) 1,80 N · c) 0,40 N · d) chưa hợp &nbsp;|&nbsp; D3·1: a) 2,0 N · b) ${dl} 0,5 N, chưa hợp · c) 2,2 N · d) ${dl} 0,2 N, hợp`,
    `D3·2: a) 2,6 N · b) ${dl} 0,5 N, chưa hợp · c) 2,7 N · d) ${dl} 0,1 N, hợp &nbsp;|&nbsp; D4·1: a) 1,70 N · b) 2,4 N · c) 133° &nbsp;|&nbsp; D4·2: a) 2,31 N · b) 2,83 N · c) 141°`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [2, 2], kq: [[1, 2], [3, 4]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'nhắc lại 1·4 · lực cân bằng 2·2 · các bước 3·1 · bẫy 3·2–3·3 · bảng số liệu 4·1 · sai số 4·3 · hình bình hành 5·1 · dạng 1–2: 6·1 · dạng 3–4: 7·1',
  out: process.argv[2],
});
