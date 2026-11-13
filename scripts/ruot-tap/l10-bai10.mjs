// Ruột tập VL10 – Bài 10 · Sự rơi tự do (lesson id 55). Quyển Chương 2 lớp 10 (Động học, bài 4–12): bài 10 = tr. 73–84.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l10-bai10.mjs (toàn bộ SVG tự vẽ, không dùng ảnh Halliday). Nội dung theo bài web (book/cache/55.json, tải từ DB 13/11/2026):
// mục tiêu, dự đoán viên giấy – hòn bi, II.1–II.4, ba thí nghiệm (ba lần thả + ống Newton, dây dọi, cổng quang), ba bẫy,
// Trả bài 6 câu, bài toán mẫu chậu hoa 20 m, thử thách phân tầng, 5 dạng bài tập mẫu.
// Mọi đề ghi rõ g (9,8 hay 10 m/s²) ngay trong đề. Đáp số Bài tương tự (tuongTu.dap) tính bằng Python 13/11/2026.
// Chạy: node scripts/ruot-tap/l10-bai10.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl10-bai10.pdf
//       node scripts/ruot-tap/l10-bai10.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l10-bai10/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL10b10 as H } from './hinh-l10-bai10.mjs';

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
  const out = resolve(HERE, 'out/hinh-l10-bai10'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 10, lid: 55, ten: 'SỰ RƠI TỰ DO', lop: 10, baiDau: 4, sub: 'Vật lí 10 · Chương 2: Động học' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
// ô điền cho biểu thức có phân số / căn: cao 9 mm (checklist HS ảo)
const fp = (w = 22) => `<span class="fill" style="min-width:${w}mm;height:9mm"></span>`;
const g10 = nw(m('g=10\\ \\mathrm{m/s^2}')), g98 = nw(m('g=9{,}8\\ \\mathrm{m/s^2}'));
const kc = '<i>(bỏ qua lực cản của không khí)</i>';

const p1 = `<section class="page">
${head('BÀI 10 · SỰ RƠI TỰ DO', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Giải thích vì sao trong không khí các vật rơi <b>nhanh, chậm khác nhau</b>; nêu thế nào là <b>rơi tự do</b>`)}
${dong(`${ck}Nêu <b>phương, chiều, tính chất</b> của chuyển động rơi tự do`)}
${dong(`${ck}Dùng <b>ba công thức rơi tự do</b> tính thời gian rơi, quãng đường, vận tốc`)}
${dong(`${ck}Nêu <b>gia tốc rơi tự do</b> ${m('g')} và những gì làm ${m('g')} thay đổi`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Vo chặt tờ giấy A4 thành một viên tròn, thả cùng lúc với hòn bi thép từ độ cao ${nw('1,5 m')}. Điều gì xảy ra?</p>
<div class="fig-side" style="${fs(40)}"><div>
${opt('A', 'Hòn bi chạm sàn trước rõ rệt, vì nó nặng hơn nhiều lần')}
${opt('B', 'Viên giấy vẫn rơi chậm như tờ giấy phẳng, vì khối lượng giấy không đổi')}
${opt('C', 'Hai vật chạm sàn gần như cùng lúc')}
${opt('D', 'Viên giấy chạm sàn trước, vì nó nhẹ hơn')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 2)}</div>
${H.giayBi()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f(12)} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(2)}</div>
${h3(4, 'II.1 · Rơi trong không khí và rơi tự do', '1·4')}
<div class="card" style="padding:1.2mm 3mm">
<div>Trong không khí, các vật rơi nhanh, chậm khác nhau là do ${f(30)} của không khí.</div>
<div>Lực cản càng ${f(25)} so với trọng lượng thì vật rơi càng nhanh.</div>
<div>Loại bỏ hết không khí: mọi vật rơi ${f(30)}.</div>
<div><b>Rơi tự do</b> là sự rơi chỉ dưới tác dụng của ${f(30)}.</div>
<div>Rơi trong không khí mà lực cản ${f(30)} so với trọng lượng cũng coi là rơi tự do.</div></div>
${h3(5, 'III · Bẫy 1', '1·5')}
<div class="card" style="padding:1mm 3mm"><div class="trap">${ck}<span><b>“Vật nặng rơi nhanh hơn.”</b> Câu này sai. Em viết lại cho đúng:</span></div>${lines(1)}
</div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('THÍ NGHIỆM · ĐẶC ĐIỂM · CÔNG THỨC RƠI TỰ DO')}
${h3(1, 'Thí nghiệm: ba lần thả và ống Newton', '2·1')}
<div class="card fig-side" style="${fs(40)};padding:1.2mm 3mm"><div>
<div><b>Làm:</b> (1) thả cùng lúc tờ giấy phẳng và quyển sách; (2) đặt tờ giấy (nhỏ hơn bìa) nằm phẳng trên sách rồi thả; (3) vo tròn tờ giấy, thả cùng hòn bi.</div>
<div><b>Quan sát</b> (vật chạm sàn trước, hoặc “cùng lúc”):</div>
<div>(1) ${f(25)} &nbsp;(2) ${f(25)} &nbsp;(3) ${f(25)}</div>
${wl('Ở (2), vì sao tờ giấy nhẹ vẫn rơi kịp quyển sách?', 2)}
<div>Ống Newton đã hút hết không khí: lông chim và hòn bi rơi ${f(25)}.</div></div>
${H.ongNewton()}</div>
${h3(2, 'II.2 · Đặc điểm của chuyển động rơi tự do', '2·2')}
<div class="fig-side" style="${fs(34)}"><div>
<div class="card" style="padding:1.2mm 3mm">
<div><b>Phương:</b> ${f(30)} (phương của dây dọi)</div>
<div><b>Chiều:</b> ${f(30)}</div>
<div><b>Tính chất:</b> chuyển động thẳng ${f(30)}</div></div>
<div style="margin:.6mm 0 .4mm"><b>Thí nghiệm dây dọi.</b> Thả bi sát dây dọi cạnh thước, quay video chậm, dừng hình mỗi ${nw('0,1 s')} (số liệu minh hoạ, ${g98}):</div>
<table class="tbl-ct" style="text-align:center"><tr><th>${m('t\\ (\\mathrm s)')}</th><th>0</th><th>0,1</th><th>0,2</th><th>0,3</th><th>0,4</th><th>0,5</th></tr>
<tr><td>Vị trí (cm)</td><td>0</td><td>4,9</td><td>19,6</td><td>44,1</td><td>78,4</td><td>122,5</td></tr>
<tr><td>Khoảng (cm)</td><td>–</td><td>4,9</td><td></td><td></td><td></td><td></td></tr></table>
</div>
${H.dayDoi()}</div>
<div class="card" style="margin-top:1mm;padding:1.2mm 3mm">
<div>Mỗi khoảng dài hơn khoảng trước ${nw(`${f(14)}&nbsp;cm`)} ⇒ vận tốc tăng ${f(25)} ⇒ nhanh dần đều.</div>
<div>Tỉ lệ các khoảng liên tiếp: ${nw(`1 : ${f(12)} : ${f(12)} : ${f(12)} : ${f(12)}`)}</div></div>
${h3(3, 'II.3 · Công thức rơi tự do', '2·3')}
<div class="card" style="padding:1.2mm 3mm">
<div>Gốc tại điểm thả, chiều dương hướng xuống, gốc thời gian lúc thả: thay ${nw(`${m('v_0=')} ${f(12)}`)}, ${nw(`${m('a=')} ${f(12)}`)} vào công thức Bài 9.</div>
<div style="display:flex;gap:4mm;flex-wrap:wrap;align-items:flex-end;margin-top:.6mm"><span>Vận tốc: ${m('v=')} ${fp(18)}</span><span>Quãng đường: ${m('s=')} ${fp(22)}</span><span>Không có thời gian: ${m('v^2=')} ${fp(18)}</span></div>
<div style="display:flex;gap:4mm;flex-wrap:wrap;align-items:flex-end;margin-top:.6mm"><span>Chạm đất (${m('s=h')}): &nbsp;${m('t=')} ${fp(22)}</span><span>${m('v=')} ${fp(22)}</span></div>
<div style="margin-top:.6mm">Mẹo với ${g10}: rơi 1, 2, 3, 4 giây được ${nw(`${f(12)} – ${f(12)} – ${f(12)} – ${f(12)}&nbsp;m`)}</div></div>
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('GIA TỐC RƠI TỰ DO · BA CÁI BẪY')}
${h3(1, 'II.4 · Gia tốc rơi tự do', '3·1')}
<div class="card" style="padding:1.2mm 3mm">
<div>Tại cùng một nơi, mọi vật rơi tự do với ${f(30)} gia tốc ${m('g')} (đơn vị ${f(14)}).</div>
<div>Đo ngang mặt biển: xích đạo ${m('\\approx 9{,}78')} · vĩ độ 45° ${m('\\approx 9{,}81')} · địa cực ${nw(`${m('\\approx 9{,}83\\ \\mathrm{m/s^2}')}.`)}</div>
<div>Càng gần địa cực, ${m('g')} càng ${f(25)}; càng lên cao, ${m('g')} càng ${f(25)}.</div>
<div>Gần mặt đất thường lấy ${nw(`${m('g=')} ${f(14)}&nbsp;m/s²`)}; bài tập hay làm tròn ${nw(`${f(14)}&nbsp;m/s²`)}.</div></div>
${h3(2, 'Thí nghiệm: đo g bằng cổng quang', '3·2')}
<div class="fig-side" style="${fs(44)}"><div>
<table class="tbl-ct" style="text-align:center"><tr><th>${m('s\\ (\\mathrm m)')}</th><th>${m('t\\ (\\mathrm s)')}</th><th>${m('g=2s/t^2\\ (\\mathrm{m/s^2})')}</th></tr>
<tr><td>0,20</td><td>0,205</td><td></td></tr>
<tr><td>0,40</td><td>0,289</td><td></td></tr>
<tr><td>0,60</td><td>0,353</td><td></td></tr>
<tr><td>0,80</td><td>0,407</td><td></td></tr>
<tr><td>1,00</td><td>0,455</td><td></td></tr></table>
<div style="margin-top:.6mm">Lệch xa 9,8 nhất ở hàng ${nw(`${m('s=')} ${f(14)}&nbsp;m`)}.</div>
${wl('Mọi giá trị đều nhỏ hơn 9,8. Vì sao?', 2)}</div>
${H.congQuang()}</div>
${h3(3, 'III · Bẫy 2 và bẫy 3', '3·3')}
<div class="card" style="padding:1mm 3mm">
<div class="fig-side" style="${fs(44)}"><div>
<div class="trap">${ck}<span><b>“Giây thứ ${m('n')}” lẫn với “${m('n')} giây đầu”.</b> Giây thứ ${m('n')} chỉ là đoạn từ ${m('t=n-1')} đến ${m('t=n')}: ${nw(m('\\Delta s=s_n-s_{n-1}'))}.</span></div>
<div style="margin:0 0 .6mm 7mm">Hình bên: 3 giây đầu rơi ${nw(`${f(14)}&nbsp;m`)}; giây thứ 3 rơi ${nw(`${f(14)}&nbsp;m`)}.</div>
<div class="trap">${ck}<span><b>“Độ cao gấp đôi thì thời gian gấp đôi.”</b> ${m('s')} tỉ lệ với ${m('t^2')}, nên:</span></div>
<div style="margin-left:7mm">${m('t')} gấp 2 ⇒ ${m('s')} gấp ${f(12)}</div>
<div style="margin-left:7mm">${m('h')} gấp 4 ⇒ ${m('t')} gấp ${f(12)}</div>
<div style="margin-left:7mm">${m('h')} gấp 2 ⇒ ${m('t')} gấp ${f(14)}</div></div>
${H.giayThu()}</div></div>
${h3(4, 'Làm nhanh', '3·4')}
${box(cau(`<b>Câu 1.</b> Thả hòn đá rơi tự do, ${g98}. Sau ${nw('3 s')}, vận tốc và quãng đường đã rơi là bao nhiêu?`, 2)
 + cau(`<b>Câu 2.</b> Vật rơi tự do chạm đất với vận tốc ${nw('25 m/s')}, ${g10}. Vật được thả từ độ cao bao nhiêu?`, 1))}
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('TỰ KIỂM TRA · BÀI TOÁN MẪU')}
${h3(1, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '4·1')}
${rkHai([1, 2, 3], [4, 5, 6])}
${h3(2, 'V · Bài toán mẫu: chậu hoa rơi từ ban công', '4·2')}
<div class="card soft" style="padding:1.2mm 3mm">Một chậu hoa tuột khỏi móc ở ban công tầng 7, độ cao ${nw('20 m')} so với mặt đất, rơi thẳng xuống. Bỏ qua sức cản không khí, lấy ${g10}. Tính:
<div><b>a)</b> thời gian chậu rơi tới mặt đất</div><div><b>b)</b> vận tốc lúc chạm đất</div><div><b>c)</b> quãng đường chậu rơi trong giây cuối cùng</div></div>
${h3(3, 'Phân tích đề')}
<table><tr><th style="width:50mm">Câu trong đề</th><th>Dữ liệu → kiến thức</th></tr>
<tr><td>“tuột khỏi móc”</td><td>${m('v_0=0')}, mốc thời gian lúc tuột</td></tr>
<tr><td style="height:6.5mm">“độ cao 20 m so với mặt đất”</td><td></td></tr>
<tr><td style="height:6.5mm">“bỏ qua sức cản không khí”</td><td></td></tr>
<tr><td style="height:6.5mm">“trong giây cuối cùng”</td><td></td></tr></table>
${h3(4, 'Giải')}
<div class="fig-side" style="${fs(44)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl('a) Thời gian rơi:', 3)}${wl('b) Vận tốc chạm đất:', 2)}${wl('c) Quãng đường giây cuối:', 4)}${wl('Kiểm tra bằng cách khác:', 2)}</div>${H.chauHoa()}</div>
${h3(5, 'Điền bước còn thiếu: chậu rơi từ độ cao 45 m (cùng nơi, g = 10 m/s²)')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div class="ln" style="height:9mm;display:flex;align-items:center"><b>Bước 1 (cho sẵn):</b>&nbsp;${m('t=\\sqrt{\\dfrac{2\\cdot 45}{10}}=3\\ \\mathrm s')}</div>
${wl(`Bước 2: ${m('v=')}`, 1)}${wl('Bước 3: quãng đường giây cuối =', 2)}</div>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TẬP VỀ NHÀ · TRẢ BÀI · THỬ THÁCH')}
${K.btvn()}
${h3(2, 'IV · Trả bài 6 câu', '5·2')}
${box(`${tb('1. Vì sao trong không khí các vật rơi nhanh, chậm khác nhau?')}${lines(2)}
${tb('2. Rơi tự do là gì? Khi nào rơi trong không khí cũng coi là rơi tự do?')}${lines(2)}
${tb('3. Ba đặc điểm của chuyển động rơi tự do?')}${lines(1)}
${tb('4. Công thức vận tốc, quãng đường, hệ thức không có thời gian?')}${lines(1)}
${tb(`5. Thời gian rơi và vận tốc chạm đất khi thả từ độ cao ${m('h')}?`)}${lines(1)}
${tb(`6. Gia tốc ${m('g')}: như nhau khi nào, phụ thuộc gì, thường lấy bao nhiêu?`)}${lines(1)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/6 câu · chưa thuộc: ${f(25)} ${nw(`→ đọc lại ô ${f(12)} Tập`)}</div>
${h3(3, 'Thử thách phân tầng', '5·3')}
<div class="fig-side" style="${fs(32)}">${box(wl(`${m('\\bigstar')} Quả táo rơi từ cành cao ${nw('3,2 m')}, ${g10}. Thời gian rơi và vận tốc chạm đất?`, 2)
 + wl(`${m('\\bigstar\\bigstar')} Thước đo phản xạ rơi ${nw('20 cm')} rồi em mới bắt được, ${g98}. Thời gian phản xạ của em?`, 2)
 + wl(`${m('\\bigstar\\bigstar\\bigstar')} Thả bi 1, đúng ${nw('1 s')} sau thả bi 2 từ cùng chỗ, ${g10}. Khi bi 2 đã rơi ${m('t')} giây, hai bi cách nhau bao xa? Khoảng cách đó thay đổi thế nào?`, 3))}${H.thuoc()}</div>
${h3(4, 'VI · Mang về: điều em dễ quên nhất', '5·4')}
${box(wl('1.', 1) + wl('2.', 1) + wl('3.', 1))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Biết thời gian rơi: tìm độ cao và vận tốc lúc chạm',
    de: `Thả nhẹ hòn đá từ mép một cây cầu xuống mặt sông, đo được thời gian rơi ${nw(m('t=4{,}0\\ \\mathrm s'))}. ${kc}, ${g98}.<br><b>a)</b> mặt cầu cao bao nhiêu so với mặt sông<br><b>b)</b> vận tốc của hòn đá lúc chạm mặt sông`,
    nd: `“Thả nhẹ” ⇒ ${nw(`${m('v_0=')} ${f(12)}`)}; chạm sông khi ${nw(`${m('s=')} ${f(12)}`)}`, a: ['a', 'b'], gi: 2, cot: 2 },
  { t: 'Dạng 2 · Trung bình · Quãng đường trong n giây đầu và trong giây thứ n',
    de: `Thả rơi tự do một vật từ đỉnh cột cao ${nw('125 m')}, ${g10}.<br><b>a)</b> sau bao lâu vật chạm đất<br><b>b)</b> quãng đường vật rơi trong ${nw('3 s')} đầu tiên<br><b>c)</b> quãng đường vật rơi trong giây thứ 3`,
    nd: `“3 s đầu”: ${m('t')} từ 0 đến ${nw(`${f(12)}&nbsp;s`)}; “giây thứ 3”: ${m('t')} từ ${nw(`${f(12)}&nbsp;s`)} đến 3 s`, a: ['a', 'b', 'c'], gi: 3 },
  { t: 'Dạng 3 · Trung bình · Biết quãng đường giây cuối: tìm thời gian rơi, độ cao',
    de: `Thả rơi tự do viên sỏi từ cửa sổ toà nhà; trong giây cuối trước khi chạm sân, sỏi rơi được ${nw('24,5 m')}, ${g98}.<br><b>a)</b> viên sỏi rơi trong bao lâu<br><b>b)</b> cửa sổ cao bao nhiêu so với mặt sân<br><b>c)</b> vận tốc của viên sỏi lúc chạm sân`,
    nd: `Gọi ${m('t')} là thời gian rơi: giây cuối là từ ${f(14)} đến ${m('t')}, nên ${nw(m('\\Delta s=s(t)-s(t-1)'))}`, a: ['a', 'b', 'c'], gi: 3, fig: H.toaNha('') },
  { t: 'Dạng 4 · Khó · Rơi tự do kết hợp truyền âm: tìm độ sâu của hang',
    de: `Thả hòn đá rơi tự do vào một cái hang sâu. Sau ${nw('4,25 s')} kể từ lúc thả, người thả nghe thấy tiếng đá chạm đáy. Vận tốc truyền âm trong không khí lấy ${nw('320 m/s')}; ${g10}.<br><b>a)</b> tính chiều sâu của hang<br><b>b)</b> nếu bỏ qua thời gian truyền âm thì độ sâu tính ra là bao nhiêu, sai lệch bao nhiêu so với câu a`,
    nd: `${nw('4,25 s')} = thời gian đá rơi ${m('t_1')} + ${f(25)}; âm đi lên đều: ${nw(`${m('t_2=')} ${fp(16)}`)}`, a: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>'], gi: 5, fig: H.hang() },
  { t: 'Dạng 5 · Khó · Hai vật thả cách nhau một khoảng thời gian',
    de: `Từ đỉnh cột cao ${nw('125 m')} thả rơi tự do bi A. Đúng ${nw('1 s')} sau, thả bi B từ cùng điểm, không vận tốc đầu. ${g10}. Mốc ${m('t=0')} lúc thả A; xét lúc cả hai bi còn đang rơi.<br><b>a)</b> khi A đã rơi ${nw('3 s')}, hai bi cách nhau bao nhiêu<br><b>b)</b> sau lúc thả A bao lâu thì hai bi cách nhau ${nw('35 m')}<br><b>c)</b> hiệu vận tốc ${m('v_A-v_B')}; khoảng cách tăng thêm bao nhiêu mét mỗi giây`,
    nd: `B rơi trễ 1 s: lúc ${m('t')}, B đã rơi được ${f(16)} giây; ${nw(m('d=s_A-s_B'))}`, a: ['a', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'], gi: 5, fig: H.haiBi() },
];

// Bài tương tự giải vào vở (thầy chốt 10/11): 1 cột; ô đáp số 25 mm đặt cuối đúng dòng của ý, nhãn ô khớp a) b) c)…;
// cuối trang là vùng nháp. Đáp số tính bằng Python 13/11/2026 (g ghi trong từng đề).
const ttHaiCot = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';
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
    { t: 'Dạng 1 · Bài 1', de: `Thả nhẹ viên bi từ mép cầu, bi chạm mặt sông sau ${nw('3,0 s')}. ${kc}, ${g98}.<br><b>a)</b> mặt cầu cao bao nhiêu so với mặt sông<br><b>b)</b> vận tốc lúc chạm mặt sông`, fig: H.cauSong('Thả nhẹ từ mép cầu.'), fw: 40, o: ['a', 'b'] },
    { t: 'Dạng 1 · Bài 2', de: `Quả táo rơi tự do từ cành cây, chạm đất sau ${nw('0,6 s')}. ${g10}.<br><b>a)</b> cành cây cao bao nhiêu<br><b>b)</b> vận tốc lúc chạm đất`, o: ['a', 'b'] },
    { t: 'Dạng 2 · Bài 1', de: `Thả rơi tự do một vật từ độ cao ${nw('80 m')}. ${g10}.<br><b>a)</b> thời gian rơi tới đất<br><b>b)</b> quãng đường rơi trong ${nw('2 s')} đầu<br><b>c)</b> quãng đường rơi trong giây thứ 2<br><b>d)</b> quãng đường rơi trong giây cuối cùng`, o: ['a', 'b', 'c', 'd'] },
    { t: 'Dạng 2 · Bài 2', de: `Thả rơi tự do một vật từ độ cao ${nw('122,5 m')}. ${g98}.<br><b>a)</b> thời gian rơi tới đất<br><b>b)</b> quãng đường rơi trong ${nw('4 s')} đầu<br><b>c)</b> quãng đường rơi trong giây thứ 4`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 3 · Bài 1', de: `Vật rơi tự do, trong giây cuối cùng trước khi chạm đất rơi được ${nw('35 m')}. ${g10}.<br><b>a)</b> thời gian rơi<br><b>b)</b> độ cao lúc thả<br><b>c)</b> vận tốc lúc chạm đất`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 3 · Bài 2', de: `Vật rơi tự do, trong giây cuối cùng trước khi chạm đất rơi được ${nw('14,7 m')}. ${g98}.<br><b>a)</b> thời gian rơi<br><b>b)</b> độ cao lúc thả<br><b>c)</b> vận tốc lúc chạm đất`, o: ['a', 'b', 'c'] },
  ], [
    { t: 'Dạng 4 · Bài 1', de: `Thả hòn đá rơi tự do xuống giếng cạn. Sau ${nw('3,15 s')} kể từ lúc thả thì nghe tiếng đá chạm đáy. Vận tốc âm lấy ${nw('300 m/s')}; ${g10}.<br><b>a)</b> độ sâu của giếng<br><b>b)</b> độ sâu tính ra nếu bỏ qua thời gian truyền âm, và sai lệch so với câu a`, fig: H.hang('Đá rơi xuống, rồi tiếng động đi lên.', { tong: 'tổng: 3,15 s' }), fw: 40, o: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>'], ow: 20 },
    { t: 'Dạng 4 · Bài 2', de: `Hòn đá rơi tự do ${nw('3,0 s')} thì chạm đáy giếng. Vận tốc âm lấy ${nw('340 m/s')}; ${g10}.<br><b>a)</b> độ sâu của giếng<br><b>b)</b> sau bao lâu kể từ lúc thả thì nghe tiếng đá chạm đáy`, o: ['a', 'b'] },
    { t: 'Dạng 5 · Bài 1', de: `Từ đỉnh tháp cao ${nw('245 m')} thả rơi tự do bi A; đúng ${nw('2 s')} sau thả bi B từ cùng điểm. ${g10}. Mốc ${m('t=0')} lúc thả A; xét lúc cả hai còn đang rơi.<br><b>a)</b> khi A đã rơi ${nw('4 s')}, hai bi cách nhau bao nhiêu<br><b>b)</b> hiệu vận tốc ${m('v_A-v_B')}<br><b>c)</b> sau lúc thả A bao lâu thì hai bi cách nhau ${nw('100 m')}`, fig: H.haiBi('Bi A thả trước 2 s.', { tre: '2 s' }), fw: 40, o: ['a', 'b', 'c'], ow: 20 },
    { t: 'Dạng 5 · Bài 2', de: `Từ mái nhà cao ${nw('20 m')}, hai giọt nước nhỏ xuống cách nhau ${nw('0,5 s')}, rơi tự do. ${g10}. Mốc ${m('t=0')} lúc giọt 1 rời mái.<br><b>a)</b> khi giọt 1 đã rơi ${nw('1,5 s')}, hai giọt cách nhau bao nhiêu<br><b>b)</b> hiệu vận tốc của hai giọt<br><b>c)</b> khoảng cách tăng thêm bao nhiêu mét mỗi giây`, o: ['a', 'b', 'c'] },
    nhap(7),
  ]],
  dap: [
    `D1·1: a) 44,1 m · b) 29,4 m/s &nbsp;|&nbsp; D1·2: a) 1,8 m · b) 6,0 m/s &nbsp;|&nbsp; D2·1: a) 4 s · b) 20 m · c) 15 m · d) 35 m &nbsp;|&nbsp; D2·2: a) 5 s · b) 78,4 m · c) 34,3 m &nbsp;|&nbsp; D3·1: a) 4 s · b) 80 m · c) 40 m/s &nbsp;|&nbsp; D3·2: a) 2 s · b) 19,6 m · c) 19,6 m/s`,
    `D4·1: a) 45 m · b<sub>1</sub>) 49,6 m · b<sub>2</sub>) 4,6 m &nbsp;|&nbsp; D4·2: a) 45 m · b) 3,13 s &nbsp;|&nbsp; D5·1: a) 60 m · b) 20 m/s · c) 6 s &nbsp;|&nbsp; D5·2: a) 6,25 m · b) 5 m/s · c) 5 m`,
  ],
};

await K.dung({
  trang1to5: ttHaiCot + [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 2], kq: [[1, 2, 3], [4, 5]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'rơi tự do 1·4 · ba lần thả 2·1 · đặc điểm, dây dọi 2·2 · công thức 2·3 · gia tốc g 3·1 · cổng quang 3·2 · bẫy 1·5, 3·3 · bài toán mẫu 4·2 · dạng 1–3 → 6·1 · dạng 4–5 → 7·1',
  out: process.argv[2],
});
