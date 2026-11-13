// Ruột tập VL10 – Bài 7 · Đồ thị độ dịch chuyển – thời gian (lesson id 52). Quyển Chương 2 lớp 10: bài 4 = tr.1–12 → bài 7 = tr. 37–48.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l10-bai7.mjs (toàn bộ SVG tự vẽ; đồ thị có lưới đọc được số liệu). Nội dung theo bài web (book/cache/52.json, tải từ DB 13/11/2026):
// mục tiêu, dự đoán đồ thị xe đạp, II.1–II.5, hai thí nghiệm (bọt khí, đi bộ), ba bẫy, Trả bài 6 câu, 7 câu tự kiểm tra, bài toán mẫu xe đồ chơi,
// điền bước, thử sức đổi điểm, đổi chiều dương, thử thách, 4 dạng bài tập mẫu.
// Đáp số Bài tương tự (tuongTu.dap) tính bằng Python 13/11/2026 (bản tính ghi trong phiên; số nguyên/1 chữ số thập phân nên đối chiếu tay được).
// Chạy: node scripts/ruot-tap/l10-bai7.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl10-bai7.pdf
//       node scripts/ruot-tap/l10-bai7.mjs --hinh           → chụp từng hình ở cỡ in (50 mm) vào out/hinh-l10-bai7/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL10b7 as H } from './hinh-l10-bai7.mjs';

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
    + 'body{margin:0;font-family:BV,sans-serif;zoom:4}.fig{margin:0;width:50mm;border:.3mm solid #d3dbec;border-radius:1.5mm;padding:1mm 1.5mm .6mm;background:#fff}.fig svg{display:block;width:100%;height:auto}figcaption{font-size:2.95mm;color:#5f6a88;line-height:1.3;margin-top:.4mm}';
  const out = resolve(HERE, 'out/hinh-l10-bai7'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 7, lid: 52, ten: 'ĐỒ THỊ ĐỘ DỊCH CHUYỂN – THỜI GIAN', lop: 10, baiDau: 4, sub: 'Vật lí 10 · Chương 2: Động học' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const dt = m('d') + '–' + m('t');
const vv = (s) => nw(m(s));
const sp = (w) => `<span style="display:inline-block;width:${w}mm"></span>`;

const p1 = `<section class="page">
${head('BÀI 7 · ĐỒ THỊ ĐỘ DỊCH CHUYỂN – THỜI GIAN', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Vẽ được đồ thị ${dt} từ <b>bảng số liệu</b>`)}
${dong(`${ck}Tính <b>vận tốc</b> từ đồ thị, giữ đúng <b>dấu</b>`)}
${dong(`${ck}Đọc đồ thị để <b>kể lại</b> chuyển động của vật`)}
${dong(`${ck}Tách <b>quãng đường</b> và <b>độ dịch chuyển</b> khi vật quay đầu`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Trong đoạn 2 (nằm ngang) của đồ thị bên, bạn đi xe đạp đang làm gì?</p>
<div class="fig-side" style="${fs(50)}"><div>
${opt('A', 'Đi trên một đoạn đường nằm ngang, bằng phẳng')}
${opt('B', 'Chạy đều, tốc độ không đổi')}
${opt('C', 'Đứng yên một lúc')}
${opt('D', 'Đạp ngược về nhà')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 2)}</div>
${H.xeDap()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f(12)} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Quỹ đạo, độ dịch chuyển và quãng đường', '1·4')}
<div class="card" style="padding:1.2mm 3mm">
<div><b>Quỹ đạo:</b> đường vật ${f(25)} khi chuyển động. <b>Chuyển động thẳng:</b> quỹ đạo là ${f(25)}.</div>
<div><b>Chuyển động thẳng đều:</b> quỹ đạo thẳng, đi ${f(14)} chiều, tốc độ ${f(25)}.</div>
<div class="fig-side" style="${fs(50)};margin-top:.6mm"><div>
<div>Đi một chiều: ${m('\\lvert d\\rvert')} ${f(12)} ${m('s')}</div>
<div>Quay đầu: ${m('s')} vẫn ${f(25)}, ${m('d')} giảm, có thể ${f(14)}</div>
<div style="margin-top:.8mm">Tốc độ trung bình: ${m('v_{\\mathrm{tb}}=')} ${f(14)} (không âm)</div>
<div style="margin-top:.8mm">Vận tốc trung bình: ${m('\\vec v_{\\mathrm{tb}}=')} ${f(14)} (có dấu)</div>
<div style="margin-top:.8mm">Hình bên: ${nw(`${m('s=')} ${f(12)}&nbsp;m`)} · ${nw(`${m('d=')} ${f(12)}&nbsp;m`)}</div>
<div style="margin-top:.8mm"><b>Thử ngay:</b> trượt ${nw('25 m')} theo chiều dương rồi quay lại ${nw('15 m')}: ${nw(`${m('s=')} ${f(12)}&nbsp;m`)} · ${nw(`${m('d=')} ${f(12)}&nbsp;m`)}</div></div>
${H.truotBang()}</div></div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('PHƯƠNG TRÌNH · VẼ ĐỒ THỊ TỪ BẢNG SỐ LIỆU')}
${h3(1, 'II.2 · Phương trình chuyển động thẳng đều', '2·1')}
<div class="card" style="padding:1.2mm 3mm">
<div>${m('x=')} ${f(25)} &nbsp; với ${m('x_0')} là toạ độ lúc ${f(14)}, ${m('v')} là vận tốc (không đổi)</div>
<div>${m('v\\gt 0')}: đi ${f(25)} chiều dương · ${m('v\\lt 0')}: đi ${f(25)} chiều dương</div>
<div>Gốc toạ độ ở chỗ xuất phát (${m('x_0=0')}): ${m('x=d=')} ${f(14)}</div>
<div style="margin-top:.6mm"><b>Ví dụ:</b> xe đồ chơi xuất phát cách vạch mốc ${vv('2\\ \\mathrm m')}, chạy ra xa vạch mốc với ${vv('1{,}5\\ \\mathrm{m/s}')} (chiều dương từ vạch mốc ra).</div>
<div>${m('x=')} ${f(25)} (m) · lúc ${vv('t=4\\ \\mathrm s')}: ${nw(`${m('x=')} ${f(12)}&nbsp;m`)} · chạy về vạch mốc, cùng tốc độ: ${nw(`${m('v=')} ${f(14)}&nbsp;m/s`)}</div></div>
<div class="card soft" style="padding:1mm 3mm"><b>Làm nhanh.</b> Xe chạy theo ${vv('x=5-2t')} (${m('x')}: m, ${m('t')}: s): ${nw(`${m('x_0=')} ${f(12)}&nbsp;m`)} · ${nw(`${m('v=')} ${f(12)}&nbsp;m/s`)} · xe đi ${f(25)} chiều dương · qua gốc toạ độ lúc ${nw(`${m('t=')} ${f(12)}&nbsp;s`)}</div>
${h3(2, 'II.3 · Vẽ đồ thị từ bảng số liệu', '2·2')}
<div class="card" style="padding:1.2mm 3mm">
<div>Trục ngang: ${f(12)}; trục đứng: ${f(12)}; ghi ${f(25)} ở đầu mỗi trục.</div>
<div>Thẳng đều: ${m('d=vt')} có dạng ${m('y=ax')} ${m('\\to')} đồ thị là ${f(25)}, hệ số góc là ${f(12)}.</div>
<div>Điểm lệch nhẹ do sai số: kẻ ${f(25)} đi gần mọi điểm, không nối ${f(25)}.</div></div>
${h3(3, 'Thí nghiệm: bọt khí trong ống nước', '2·3')}
<div class="fig-side" style="${fs(62)}"><div>
<div><b>Làm:</b> ống nước dài ${vv('60\\ \\mathrm{cm}')} còn một bọt khí, vạch ${nw('0, 10, …, 50 cm')}; đặt ống nghiêng, bấm đồng hồ khi bọt qua vạch 0, đọc thời điểm qua từng vạch.</div>
<table class="tbl-ct" style="margin-top:.8mm"><tr><th>${m('d\\ (\\mathrm{cm})')}</th><th>${m('t\\ (\\mathrm s)')}</th><th>${m('d/t\\ (\\mathrm{cm/s})')}</th></tr>
<tr><td>10</td><td>2,1</td><td></td></tr>
<tr><td>20</td><td>3,9</td><td></td></tr>
<tr><td>30</td><td>6,1</td><td></td></tr>
<tr><td>40</td><td>7,9</td><td></td></tr>
<tr><td>50</td><td>10,0</td><td></td></tr></table>
<div class="hint">Số liệu minh hoạ; cột cuối làm tròn 2 chữ số thập phân.</div></div>
${H.luoiBotKhi()}</div>
<div class="card" style="margin-top:.8mm;padding:1mm 3mm">
<div><b>Rút ra:</b> các điểm gần như nằm trên ${f(25)} ${m('\\to')} bọt khí chuyển động ${f(25)}.</div>
<div>Độ dốc giữa hai điểm xa nhau trên đường: ${nw(`${m('v=')} ${f(14)}&nbsp;cm/s`)}</div>
${wl('Vì sao hàng 10 cm lệch nhiều nhất (bấm tay sai cỡ 0,1 s mỗi lần)?', 3)}</div>
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('ĐỘ DỐC LÀ VẬN TỐC · ĐỌC ĐỒ THỊ · BA CÁI BẪY')}
${h3(1, 'II.4 · Độ dốc là vận tốc', '3·1')}
<div class="fig-side" style="${fs(54)}"><div>
<div class="card" style="padding:1.2mm 3mm;margin-bottom:1mm">
<div>${m('v=')} ${f(25)} ${m('=')} ${f(25)}</div>
<div>Lấy hai điểm ${f(25)} trên đường, giữ đơn vị.</div>
<div>Nhanh hay chậm: so ${f(25)} độ dốc, bỏ ${f(12)}.</div></div>
<table><tr><th style="width:26mm">Dạng đường</th><th>Vật đang…</th></tr>
<tr><td>Đi lên, dốc nhiều</td><td></td></tr>
<tr><td>Đi lên, dốc ít</td><td></td></tr>
<tr><td>Nằm ngang</td><td></td></tr>
<tr><td>Đi xuống</td><td></td></tr></table></div>
${H.bonXe()}</div>
${box(`<div style="padding-top:.6mm"><b>Đọc hình bên.</b> Xe 4: ${nw(`${m('v_4=')} ${f(16)}&nbsp;m/s`)} &nbsp;· Xe 1: ${nw(`${m('v_1=')} ${f(16)}&nbsp;m/s`)}</div>
${wl('Chấm tròn (đường 1 cắt đường 4) cho biết gì về hai xe? Có cùng vận tốc không?', 2)}
<div class="hint" style="margin:.4mm 0">Đồ thị cong (nhanh, chậm dần): vận tốc tức thời = độ dốc của ${f(25)} tại điểm đó.</div>`)}
${h3(2, 'II.5 · Đọc đồ thị: kể lại chuyển động', '3·2')}
<div class="fig-side" style="${fs(50)}"><div class="card" style="padding:1.2mm 3mm;margin:0">
<div>Chia đồ thị theo các ${f(25)}.</div>
<div>Mỗi đoạn: dấu độ dốc cho ${f(25)};</div><div>độ lớn cho ${f(25)}; nằm ngang là ${f(14)}.</div>
<div>Đang đi lên chuyển sang đi xuống: vật ${f(25)}.</div>
<div style="margin-top:.6mm"><b>Thí nghiệm đi bộ:</b> thước dây 10 m dọc hành lang; một bạn đi chậm ra tới vạch 5 m, đứng 3 s, bước nhanh về vạch 0; bạn khác ghi vị trí mỗi giây.</div>
<div><b>Rút ra:</b> mỗi kiểu đi cho ${f(25)}.</div></div>
${H.diBo()}</div>
${h3(3, 'III · Ba cái bẫy hay sập', '3·3')}
<div class="card" style="padding:1mm 3mm">
<div class="trap">${ck}<span><b>“Đồ thị là con đường.”</b> Trục đứng là ${f(25)} của vật, không phải độ cao.</span></div>
<div class="trap">${ck}<span><b>“Đường nằm cao hơn là xe nhanh hơn.”</b> Cao là ${f(14)} · dốc là ${f(14)}; hai đường cắt nhau: hai vật ${f(14)}.</span></div>
<div class="trap">${ck}<span><b>“Đọc quãng đường ở điểm cuối.”</b> ${m('d=')} ${f(25)} · ${m('s=')} cộng ${f(14)} của từng đoạn.</span></div></div>
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('TRẢ BÀI · BÀI TOÁN MẪU')}
${h3(1, 'IV · Trả bài 6 câu', '4·1')}
${box(`${tb('1. Chuyển động thẳng đều là gì? Khi nào |d| = s?')}${lines(1)}
${tb('2. Phương trình chuyển động thẳng đều, nghĩa từng kí hiệu.')}${lines(2)}
${tb(`3. Đồ thị ${dt} của chuyển động thẳng đều có dạng gì? Vì sao?`)}${lines(1)}
${tb('4. Tính vận tốc từ đồ thị thế nào?')}${lines(1)}
${tb('5. Nhìn đồ thị, làm sao biết vật dừng, nhanh, chậm, đổi chiều?')}${lines(1)}
${tb('6. Hai đường cắt nhau nghĩa là gì? Quãng đường đọc ở đâu?')}${lines(1)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/6 câu · chưa thuộc: ${f(25)} ${nw(`${m('\\to')} đọc lại ô ${f(12)} Tập`)}</div>
${h3(2, 'V · Bài toán mẫu: xe đồ chơi trên sân trường', '4·2')}
<div class="fig-side" style="${fs(50)}"><div>
<div class="card soft" style="padding:1.2mm 3mm">Xe đồ chơi điều khiển từ xa chạy trên đường thẳng ở sân trường; đồ thị ${dt} ở hình bên, chiều dương từ vạch mốc ra cọc cờ.
<div><b>a)</b> Mô tả chuyển động trong từng đoạn ${m('OA')}, ${m('AB')}, ${m('BC')}.</div><div><b>b)</b> Tính vận tốc mỗi đoạn.</div><div><b>c)</b> Tính quãng đường, độ dịch chuyển, tốc độ trung bình và vận tốc trung bình trong ${vv('10\\ \\mathrm s')}.</div></div>
<table style="margin-top:.6mm"><tr><th style="width:30mm">Câu trong đề</th><th>Dữ liệu ${m('\\to')} kiến thức</th></tr>
<tr><td>đoạn OA, 0–4 s</td><td>${m('d')}: 0 ${m('\\to')} 8 m ${m('\\to')} tính độ dốc</td></tr>
<tr><td style="height:6.5mm">đoạn AB, 4–6 s</td><td></td></tr>
<tr><td style="height:6.5mm">đoạn BC, 6–10 s</td><td></td></tr>
<tr><td style="height:6.5mm">“quãng đường … độ dịch chuyển”</td><td></td></tr></table></div>
${H.xeDoChoi()}</div>
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm;margin-top:1mm">
${wl('a) Mô tả:', 2)}${wl(`b) ${m('v_{OA}=')}${sp(30)}${m('v_{AB}=')}${sp(30)}${m('v_{BC}=')}`, 1)}${wl(`c) ${m('s=')}${sp(30)}${m('d=')}`, 1)}${wl('Tốc độ trung bình, vận tốc trung bình; kiểm tra hợp lí:', 2)}</div>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('TỰ KIỂM TRA · BTVN · ĐIỀN BƯỚC · THỬ THÁCH')}
${h3(1, 'Kết quả tự kiểm tra (7 câu)', '5·1')}
${rkHai([1, 2, 3, 4], [5, 6, 7])}
${K.btvn().replace('<i>1</i>', '<i>2</i>')}
${h3(3, 'Điền bước còn thiếu: hôm sau, đồ thị đổi số', '5·3')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:.6mm 3mm">
<div><b>Đề:</b> ${m('OA')} từ 0 đến 3 s lên 9 m; ${m('AB')} đứng yên tới 5 s; ${m('BC')} từ 5 đến 8 s về ${m('d=0')}.</div>
<div class="ln"><b>Bước 1 (cho sẵn):</b> ${m('v_{OA}=\\dfrac{9}{3}=3\\ \\mathrm{m/s}')}</div>
${wl(`Bước 2: ${m('v_{BC}=')}`, 1)}${wl(`Bước 3: ${m('s=')}${sp(30)}tốc độ trung bình trong 8 s =`, 1)}</div>
${h3(4, 'Thử sức đổi điểm, đổi chiều (bài toán mẫu)', '5·4')}
${box(wl(`Xe ở đâu lúc ${vv('t=8\\ \\mathrm s')}? Đoạn BC bắt đầu lúc ${vv('t_0=6\\ \\mathrm s')}, ở ${vv('d_0=8\\ \\mathrm m')}: dùng ${m('d=d_0+v(t-t_0)')}.`, 2)
 + wl(`Chọn lại chiều dương từ cọc cờ về vạch mốc (gốc vẫn ở vạch mốc): ${m('v_{BC}')} và ${m('d')} lúc ${vv('t=4\\ \\mathrm s')} bằng bao nhiêu?`, 2))}
${h3(5, 'Thử thách phân tầng', '5·5')}
${box(wl(`${m('\\bigstar')} Đồ thị ${dt} của vận động viên trượt băng là đường thẳng qua ${m('(0;\\,0)')} và ${nw(`${m('(8\\ \\mathrm s;\\ 96\\ \\mathrm m)')}.`)} Vận tốc?`, 2)
 + wl(`${m('\\bigstar\\bigstar')} Xe 1: ${m('x=4t')}, xe 4: ${m('x=14-3t')} (${m('x')}: m, ${m('t')}: s; hai đường 1 và 4 ở tr.${3 + 36}). Hai xe gặp nhau lúc nào, ở đâu? So với hình.`, 2)
 + wl(`${m('\\bigstar\\bigstar\\bigstar')} Xe đồ chơi chạy ra ${nw('120 cm')} trong ${nw('4 s')}, dừng ${nw('2 s')}, chạy về ${nw('60 cm')} trong ${nw('3 s')}. Phác đồ thị; tính tốc độ trung bình và vận tốc trung bình trong ${nw('9 s')}.`, 3))}
${h3(6, 'VI · Mang về: điều em dễ quên nhất', '5·6')}
${box(wl('1.', 1) + wl('2.', 1) + wl('3.', 1))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Đọc đồ thị: mô tả, vị trí, quãng đường, độ dịch chuyển',
    de: `Xe ô tô đồ chơi chạy trên đường thẳng; chiều dương là chiều xe chạy lúc đầu; đồ thị ${dt} ở hình cạnh ô giải.<br><b>a)</b> mô tả chuyển động của xe trong từng khoảng thời gian<br><b>b)</b> vị trí của xe so với điểm xuất phát lúc ${nw('t = 2 s')} (b<sub>1</sub>), 4 s (b<sub>2</sub>), 8 s (b<sub>3</sub>), 10 s (b<sub>4</sub>)<br><b>c)</b> quãng đường (c<sub>1</sub>) và độ dịch chuyển (c<sub>2</sub>) sau 10 s; vì sao hai giá trị khác nhau?`,
    nd: `chia tại các ${f(20)}; ${m('d=d')}<sub>cuối</sub> ${f(12)} ${m('d')}<sub>đầu</sub>; ${m('s=')} cộng ${f(20)} từng đoạn`,
    a: ['b<sub>1</sub>', 'b<sub>2</sub>', 'b<sub>3</sub>', 'b<sub>4</sub>', 'c<sub>1</sub>', 'c<sub>2</sub>'], gi: 6, fig: H.d1(), cot: 3 },
  { t: 'Dạng 2 · Trung bình · Độ dốc: vận tốc từng đoạn và trung bình',
    de: `Người đi bộ trên đường thẳng; chiều dương ra xa cột mốc O, gốc thời gian lúc bắt đầu đi; đồ thị ${dt} (${m('d')} tính từ O) ở hình cạnh ô giải.<br><b>a)</b> vận tốc trên đoạn 1 (a<sub>1</sub>), đoạn 2 (a<sub>2</sub>), đoạn 3 (a<sub>3</sub>)<br><b>b)</b> những lúc người đó cách O ${nw('10 m')}<br><b>c)</b> vận tốc trung bình (c<sub>1</sub>) và tốc độ trung bình (c<sub>2</sub>) trong cả ${nw('50 s')}`,
    nd: `hai điểm trên ${f(14)} đoạn; trung bình: ${m('d/\\Delta t')} và ${m('s/\\Delta t')}, không lấy ${f(25)} các vận tốc`,
    a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'a<sub>3</sub>', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'], gi: 6, fig: H.d2(), cot: 3 },
  { t: 'Dạng 3 · Trung bình · Hai đồ thị thẳng: phương trình, chỗ gặp nhau',
    de: `Hai ô tô chạy trên đường thẳng nối bến A và B; xe I xuất phát từ A, xe II từ B. Gốc toạ độ tại A, chiều dương A ${m('\\to')} B, gốc thời gian lúc hai xe cùng xuất phát; đồ thị toạ độ – thời gian ở hình cạnh ô giải.<br><b>a)</b> vận tốc xe I (a<sub>1</sub>), xe II (a<sub>2</sub>)<br><b>b)</b> phương trình chuyển động xe I (b<sub>1</sub>), xe II (b<sub>2</sub>)<br><b>c)</b> hai xe gặp nhau lúc nào (c<sub>1</sub>), cách A bao nhiêu km (c<sub>2</sub>)`,
    nd: `${m('x=x_0+vt')}: ${m('x_0')} đọc tại ${f(14)}; hai xe gặp nhau khi ${f(25)}`,
    a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c<sub>1</sub>', 'c<sub>2</sub>'], gi: 6, fig: H.d3(), cot: 3 },
  { t: 'Dạng 4 · Khó · Xuất phát lệch giờ: gặp nhau, phương trình, đồ thị',
    de: `Hai người đi bộ ngược chiều từ hai đầu đoạn đường thẳng AB dài ${nw('10 km')}. Người ở A xuất phát trước người ở B ${nw('0,5 h')}; người ở B đi được ${nw('1 h')} thì hai người gặp nhau; hai người đi nhanh như nhau. Gốc toạ độ tại A, chiều dương A ${m('\\to')} B, gốc thời gian lúc người ở A xuất phát.<br><b>a)</b> vận tốc người ở A (a<sub>1</sub>), người ở B (a<sub>2</sub>)<br><b>b)</b> phương trình chuyển động người ở A (b<sub>1</sub>), người ở B (b<sub>2</sub>)<br><b>c)</b> vẽ đồ thị hai người vào hệ trục cạnh ô giải; thời điểm (c<sub>1</sub>) và vị trí (c<sub>2</sub>) gặp nhau`,
    nd: `xuất phát muộn: ${m('x=x_0+v(t-t_0)')}; ngược chiều gặp nhau: ${m('s_A+s_B=')} ${f(14)}`,
    a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c<sub>1</sub>', 'c<sub>2</sub>'], gi: 6, fig: H.d4(), cot: 3 },
];

// Bài tương tự giải vào vở (thầy chốt 10/11): mỗi dạng 2 bài, ô đáp số đặt cuối đúng dòng của ý; nhãn ô khớp a) b) c) (a<sub>1</sub>, a<sub>2</sub>… khi ý có nhiều kết quả).
// o: chuỗi nhãn hoặc [nhãn, rộng mm] khi ô cần rộng khác mặc định (ow).
const oY = (s, o, w = 25, hep = false) => s.split('<br>').map((p) => {
  const y = p.match(/^<b>([a-d])\)<\/b>/);
  if (!y) return `<div>${p}</div>`;
  const ls = o.map((l) => (Array.isArray(l) ? l : [l, w])).filter(([l]) => l[0] === y[1]);
  const oo = `<span class="oo">${ls.map(([l, lw]) => `<span class="nw"><b>${l})</b>${f(lw)}</span>`).join('')}</span>`;
  // ý có ≥ 2 ô: ô xuống dòng riêng, canh phải (để chữ đề không bị ép thành cột hẹp — xem ảnh tr.44 bản đầu)
  return hep && ls.length > 1 ? `<div>${p}</div><div class="yo" style="justify-content:flex-end">${oo}</div>` : `<div class="yo"><span>${p}</span>${oo}</div>`;
}).join('');
const ttDe = (b) => b.fig ? `<div class="fig-side" style="grid-template-columns:1fr ${b.fw}mm"><div>${oY(b.de, b.o, b.ow, true)}</div>${b.fig}</div>` : oY(b.de, b.o, b.ow);
const vaoVo = (ds) => ds.map((b) => (b.o ? { t: b.t, de: ttDe(b), k: 0 } : b));
const nhap = (n) => ({ t: '<span class="nhap-t">Nháp / chỗ em còn vướng</span>', de: lines(n), k: 0 });
const ttCss = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';
const s14 = (l) => [l, 14];
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–2', 'DẠNG 3–4'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Xe đồ chơi chạy trên đường thẳng; đồ thị ${dt} ở hình (${m('d')} tính từ điểm xuất phát).<br><b>a)</b> vị trí của xe lúc ${vv('t=7\\ \\mathrm s')}<br><b>b)</b> quãng đường đi được sau ${nw('10 s')}<br><b>c)</b> độ dịch chuyển sau ${nw('10 s')}`, fig: H.tt1a(), fw: 50, o: ['a', 'b', 'c'], ow: 16 },
    { t: 'Dạng 1 · Bài 2', de: `Một người đi dọc hành lang thẳng; đồ thị ${dt} ở hình (${m('d')} tính từ cửa lớp, chiều dương ra xa cửa).<br><b>a)</b> người đó đứng yên trong những khoảng thời gian nào<br><b>b)</b> độ dịch chuyển trong ${nw('12 s')}<br><b>c)</b> quãng đường trong ${nw('12 s')}`, fig: H.tt1b(), fw: 50, o: [['a', 28], 'b', 'c'], ow: 16 },
    { t: 'Dạng 2 · Bài 1', de: `Xe đạp đồ chơi chạy trên đường thẳng; chiều dương ra xa cột mốc O; đồ thị ${dt} ở hình (${m('d')} tính từ O).<br><b>a)</b> vận tốc trên ba đoạn<br><b>b)</b> những lúc xe cách O ${nw('6 m')}<br><b>c)</b> vận tốc trung bình, tốc độ trung bình trong ${nw('25 s')}`, fig: H.tt2a(), fw: 50, o: [s14('a<sub>1</sub>'), s14('a<sub>2</sub>'), s14('a<sub>3</sub>'), ['b', 28], s14('c<sub>1</sub>'), s14('c<sub>2</sub>')] },
    { t: 'Dạng 2 · Bài 2', de: `Một người chạy bộ trên đường thẳng; chiều dương ra xa cột mốc O; đồ thị ${dt} ở hình (${m('d')} tính từ O).<br><b>a)</b> vận tốc trên ba đoạn<br><b>b)</b> những lúc người đó cách O ${nw('40 m')}<br><b>c)</b> vận tốc trung bình, tốc độ trung bình trong ${nw('40 s')}`, fig: H.tt2b(), fw: 50, o: [s14('a<sub>1</sub>'), s14('a<sub>2</sub>'), s14('a<sub>3</sub>'), ['b', 28], s14('c<sub>1</sub>'), s14('c<sub>2</sub>')] },
  ], [
    { t: 'Dạng 3 · Bài 1', de: `Xe I xuất phát từ A, xe II từ B trên đường thẳng AB. Gốc toạ độ tại A, chiều dương A ${m('\\to')} B, gốc thời gian lúc hai xe cùng xuất phát; đồ thị toạ độ – thời gian ở hình.<br><b>a)</b> vận tốc mỗi xe<br><b>b)</b> phương trình chuyển động mỗi xe<br><b>c)</b> lúc gặp nhau; chỗ gặp cách A`, fig: H.tt3a(), fw: 47, o: [s14('a<sub>1</sub>'), s14('a<sub>2</sub>'), 'b<sub>1</sub>', 'b<sub>2</sub>', s14('c<sub>1</sub>'), s14('c<sub>2</sub>')] },
    { t: 'Dạng 3 · Bài 2', de: `Hai xe cùng chạy theo chiều từ A về B trên đường thẳng; lúc đầu xe I ở A, xe II ở chỗ cách A ${nw('60 km')}. Gốc toạ độ tại A, chiều dương A ${m('\\to')} B, gốc thời gian lúc hai xe cùng xuất phát; đồ thị ở hình.<br><b>a)</b> vận tốc mỗi xe<br><b>b)</b> phương trình chuyển động mỗi xe<br><b>c)</b> lúc xe I đuổi kịp xe II; chỗ đó cách A`, fig: H.tt3b(), fw: 47, o: [s14('a<sub>1</sub>'), s14('a<sub>2</sub>'), 'b<sub>1</sub>', 'b<sub>2</sub>', s14('c<sub>1</sub>'), s14('c<sub>2</sub>')] },
    { t: 'Dạng 4 · Bài 1', de: `Hai người đi bộ ngược chiều từ hai đầu đoạn đường thẳng AB dài ${nw('12 km')}. Người ở A xuất phát trước người ở B ${nw('1 h')}; người ở B đi được ${nw('1 h')} thì hai người gặp nhau; hai người đi nhanh như nhau. Gốc toạ độ tại A, chiều dương A ${m('\\to')} B, gốc thời gian lúc người ở A xuất phát.<br><b>a)</b> vận tốc mỗi người<br><b>b)</b> phương trình chuyển động mỗi người<br><b>c)</b> thời điểm và vị trí gặp nhau`, o: [s14('a<sub>1</sub>'), s14('a<sub>2</sub>'), 'b<sub>1</sub>', ['b<sub>2</sub>', 34], s14('c<sub>1</sub>'), s14('c<sub>2</sub>')] },
    { t: 'Dạng 4 · Bài 2', de: `Lúc 7 h một xe máy rời A chạy thẳng đều về B. Lúc 8 h một ô tô rời A đuổi theo với vận tốc ${nw('60 km/h')}; ô tô chạy được ${nw('2 h')} thì đuổi kịp xe máy. Gốc toạ độ tại A, chiều dương A ${m('\\to')} B, gốc thời gian lúc 7 h.<br><b>a)</b> vận tốc xe máy<br><b>b)</b> phương trình chuyển động xe máy, ô tô<br><b>c)</b> ô tô đuổi kịp lúc mấy giờ; chỗ đó cách A`, o: ['a', 'b<sub>1</sub>', ['b<sub>2</sub>', 34], s14('c<sub>1</sub>'), s14('c<sub>2</sub>')] },
  ]],
  dap: [
    `D1·1: a) 2 m · b) 14 m · c) ${m('-')}2 m &nbsp;|&nbsp; D1·2: a) 0–2 s và 6–8 s · b) 2 m · c) 14 m &nbsp;|&nbsp; D2·1: a<sub>1</sub>) 3 m/s · a<sub>2</sub>) 0 · a<sub>3</sub>) ${m('-')}1 m/s · b) 2 s và 19 s · c<sub>1</sub>) 0 · c<sub>2</sub>) 1,2 m/s &nbsp;|&nbsp; D2·2: a<sub>1</sub>) 0 · a<sub>2</sub>) 2 m/s · a<sub>3</sub>) ${m('-')}2 m/s · b) 25 s và 35 s · c<sub>1</sub>) 0,5 m/s · c<sub>2</sub>) 1,5 m/s`,
    `D3·1: a<sub>1</sub>) 60 km/h · a<sub>2</sub>) ${m('-')}90 km/h · b<sub>1</sub>) ${vv('x=60t')} · b<sub>2</sub>) ${vv('x=180-90t')} · c<sub>1</sub>) 1,2 h · c<sub>2</sub>) 72 km &nbsp;|&nbsp; D3·2: a<sub>1</sub>) 50 km/h · a<sub>2</sub>) 20 km/h · b<sub>1</sub>) ${vv('x=50t')} · b<sub>2</sub>) ${vv('x=60+20t')} · c<sub>1</sub>) 2 h · c<sub>2</sub>) 100 km &nbsp;|&nbsp; D4·1: a<sub>1</sub>) 4 km/h · a<sub>2</sub>) ${m('-')}4 km/h · b<sub>1</sub>) ${vv('x=4t')} · b<sub>2</sub>) ${vv('x=16-4t\\ (t\\ge 1\\ \\mathrm h)')} · c<sub>1</sub>) 2 h · c<sub>2</sub>) 8 km &nbsp;|&nbsp; D4·2: a) 40 km/h · b<sub>1</sub>) ${vv('x=40t')} · b<sub>2</sub>) ${vv('x=60(t-1)\\ (t\\ge 1\\ \\mathrm h)')} · c<sub>1</sub>) 10 h · c<sub>2</sub>) 120 km`,
  ],
};

await K.dung({
  trang1to5: ttCss + [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [2, 2], kq: [[1, 2], [3, 4]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: `quãng đường, độ dịch chuyển 1·4 · phương trình 2·1 · vẽ đồ thị 2·2 · độ dốc 3·1 · đọc đồ thị 3·2 · bẫy 3·3 · bài toán mẫu 4·2 · dạng 1–2 ${m('\\to')} 6·1 · dạng 3–4 ${m('\\to')} 7·1`,
  out: process.argv[2],
});
