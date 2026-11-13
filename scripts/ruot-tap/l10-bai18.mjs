// Ruột tập VL10 – Bài 18 · Lực ma sát (lesson id 63). Quyển Chương 3 lớp 10 (Động lực học): bài 13 = tr. 1–12 → bài 18 = tr. 61–72.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự giải vào vở · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l10-bai18.mjs (SVG tự vẽ + ảnh thật gai lốp xe của hồ sơ sách). Nội dung theo bài web (book/cache/63.json, tải từ DB 13/11/2026):
// mục tiêu, dự đoán thùng nước, II.1–II.5, ba thí nghiệm, ba bẫy, Trả bài 6 câu, bài toán mẫu cầu trượt, thử thách, 5 dạng bài tập mẫu.
// Đáp số Bài tương tự (tuongTu.dap) và các ô điền tính bằng Python 13/11/2026 (math.sin/cos theo radian, làm tròn 2–3 chữ số có nghĩa).
// Chạy: node scripts/ruot-tap/l10-bai18.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl10-bai18.pdf
//       node scripts/ruot-tap/l10-bai18.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l10-bai18/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL10b18 as H } from './hinh-l10-bai18.mjs';

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
  const out = resolve(HERE, 'out/hinh-l10-bai18'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 18, lid: 63, ten: 'LỰC MA SÁT', lop: 10, baiDau: 13, sub: 'Vật lí 10 · Chương 3: Động lực học' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const g10 = nw(m('g=10\\ \\mathrm{m/s^2}'));
const g98 = nw(m('g=9{,}8\\ \\mathrm{m/s^2}'));
const al = m('\\alpha'), mu = m('\\mu');
const Fms = m('F_{\\mathrm{ms}}'), Fmsn = m('F_{\\mathrm{msn}}'), Fmst = m('F_{\\mathrm{mst}}'), Fmax = m('F_{\\mathrm{msn\\,max}}');

const ttHaiCot = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm}.yo .oo{flex:none;display:flex;gap:3mm}.yo{line-height:1.35}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';
const p1 = `${ttHaiCot}<section class="page">
${head('BÀI 18 · LỰC MA SÁT', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Phân biệt ma sát <b>nghỉ</b>, ma sát <b>trượt</b>, ma sát <b>lăn</b>: khi nào có, hướng ra sao, lớn bao nhiêu`)}
${dong(`${ck}Dùng ${m('F_{\\mathrm{mst}}=\\mu N')}; tính đúng áp lực ${m('N')} trên mặt ngang, khi kéo chếch, trên mặt nghiêng`)}
${dong(`${ck}Đọc bảng số liệu để tìm hệ số ma sát và nhận xét sai số`)}
${dong(`${ck}Giải bài toán động lực học có ma sát, kể cả vật trên mặt phẳng nghiêng`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">An đẩy ngang thùng nước khoáng ${nw('50 N')}, thùng chưa nhúc nhích. Lúc đó sàn tác dụng lên thùng lực ma sát bao nhiêu?</p>
<div class="fig-side" style="${fs(46)}"><div>
${opt('A', 'Bằng 0, vì thùng chưa chuyển động')}
${opt('B', `Đúng ${nw('50 N')}, ngược chiều lực đẩy`)}
${opt('C', 'Một giá trị cố định của sàn, không phụ thuộc lực đẩy')}
${opt('D', `Lớn hơn ${nw('50 N')}, nên thùng mới đứng yên`)}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 1)}</div>
${H.anDay()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Ma sát nghỉ', '1·4')}
<div class="card" style="padding:1.2mm 3mm">
<div>Xuất hiện khi có lực kéo/đẩy mà vật vẫn ${f(25)} trên mặt tiếp xúc.</div>
<div>Phương: ${f(25)} mặt tiếp xúc. Chiều: ngược ${f(25)} chuyển động của vật.</div>
<div>Độ lớn: ${Fmsn} ${m('=')} ${f(25)} lực gây xu hướng trượt. Giới hạn: ${nw(`${m('0\\le F_{\\mathrm{msn}}\\le')} ${f(14)}`)}</div>
<div class="fig-side" style="${fs(48)};margin-top:.6mm"><div>
<div><b>Đọc đồ thị:</b></div>
<div>Đoạn OA: hộp ${f(25)}</div>
<div>Tại A: hộp ${f(25)}</div>
<div>Đoạn BC: ma sát ${ck}tăng ${ck}không đổi, nhỏ hơn ở A khoảng ${nw(`${f(12)}&nbsp;N`)}</div>
<div style="margin-top:1mm">Tủ cần lực ngang ít nhất ${nw('300 N')} mới dịch. Hai bạn đẩy ${nw('260 N')} và kéo ${nw('35 N')} cùng chiều: tủ ${ck}đứng yên ${ck}trượt; ma sát ${nw(`${f(12)}&nbsp;N`)}</div></div>
${H.doThi()}</div></div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('MA SÁT TRƯỢT · ĐO HỆ SỐ MA SÁT · ÁP LỰC')}
${h3(1, 'II.2 · Ma sát trượt', '2·1')}
<div class="card" style="padding:1.2mm 3mm">
<div>Xuất hiện khi vật ${f(25)} trên bề mặt; chiều ngược chiều ${f(25)} tương đối.</div>
<div style="margin:.6mm 0">${nw(`${Fmst}${m('=')} ${f(12)}`)} &nbsp;· ${mu}: hệ số ma sát trượt, đơn vị ${f(25)} · ${m('N')}: ${f(25)} (N)</div>
<div>Phụ thuộc: ${f(25)}, ${f(25)}, ${f(25)}.</div>
<div>Không phụ thuộc: ${f(25)}, ${f(25)}. Thường ${ck}lớn hơn ${ck}nhỏ hơn ma sát nghỉ cực đại.</div></div>
${h3(2, 'Thí nghiệm: đổi mặt tiếp xúc, đổi tốc độ, cho lăn', '2·2')}
<div class="card fig-side" style="${fs(40)};padding:1.2mm 3mm"><div>
<div><b>Làm:</b> hộp ${nw('0,40 kg')} kéo trượt đều khi nằm (mặt rộng), dựng đứng (mặt hẹp), rồi kéo nhanh hơn; cuối cùng kê lên hai bút chì cho lăn.</div>
<div><b>Quan sát:</b> ba lần trượt lực kế đều chỉ khoảng ${nw('1,2 N')}; khi lăn chỉ dưới ${nw('0,1 N')}.</div>
<div><b>Rút ra:</b> ma sát trượt ${f(25)} theo diện tích, tốc độ; ma sát lăn ${f(25)} ma sát trượt rất nhiều.</div></div>
${H.butChi()}</div>
${h3(3, 'II.3 · Đo hệ số ma sát bằng lực kế', '2·3')}
<div class="fig-side" style="${fs(58)}"><table class="tbl-ct" style="font-size:var(--fs-sm)">
<tr><th>${m('N')} (N)</th><th>Nghỉ cực đại (N)</th><th>Trượt (N)</th><th>F<sub>trượt</sub>/<i>N</i></th></tr>
<tr><td>1,96</td><td>0,7</td><td>0,6</td><td></td></tr>
<tr><td>3,92</td><td>1,5</td><td>1,2</td><td></td></tr>
<tr><td>5,88</td><td>2,1</td><td>1,7</td><td></td></tr>
<tr><td>7,84</td><td>2,9</td><td>2,4</td><td></td></tr></table>
<div style="font-size:var(--fs-sm);line-height:1.4"><b>Làm:</b> hộp gỗ trên bàn gỗ, thêm gia trọng; ${m('N=mg')}, ${g98}. Lực kế chia độ ${nw('0,1 N')}, đọc sai cỡ ${nw('±0,05 N')}.<br>Tính tỉ số ở cột cuối (2 chữ số sau dấu phẩy).</div></div>
<div class="card" style="margin-top:.8mm;padding:1mm 3mm">
<div>Trung bình ${nw(`${mu} ${m('\\approx')} ${f(14)}`)} · Lần đo kém tin cậy nhất: lần ${f(12)}, vì</div>${lines(1)}</div>
${h3(4, 'II.4 · Áp lực N: không phải lúc nào cũng bằng mg', '2·4')}
<div class="card fig-side" style="${fs(48)};padding:1.2mm 3mm"><div>
<div>Lấy ${m('N')} theo phương ${f(25)} mặt tiếp xúc.</div>
<div style="margin:.8mm 0">Mặt ngang, kéo ngang: ${nw(`${m('N=')} ${f(16)}`)}</div>
<div style="margin:.8mm 0">Mặt ngang, kéo chếch lên góc ${al}: ${nw(`${m('N=')} ${f(22)}`)}</div>
<div style="margin:.8mm 0">Mặt nghiêng góc ${al}: ${nw(`${m('N=')} ${f(16)}`)}</div>
<div class="hint">Trên dốc, ${m('P')} tách thành ${m('P_x=mg\\sin\\alpha')} (dọc dốc) và ${m('P_y=mg\\cos\\alpha')} (ép vào dốc).</div></div>
${H.keoCheo()}</div>
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('THÍ NGHIỆM TẤM VÁN · MA SÁT LĂN · TRẢ BÀI')}
${h3(1, 'Thí nghiệm: nâng dần tấm ván', '3·1')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div><b>Quan sát:</b> hộp bắt đầu trượt khi ${nw('h ≈ 0,34 m')}; búng nhẹ thì hộp trượt đều khi ${nw('h ≈ 0,29 m')}. ${nw(m('\\sin\\alpha=h/L'))}.</div>
<div style="margin-top:.6mm">Sắp trượt: ${nw(`${m('mg\\sin\\alpha=\\mu_n\\,mg\\cos\\alpha')}`)} ⇒ ${nw(`${m('\\mu_n=')} ${f(14)}`)} ${nw(`${m('\\approx')} ${f(12)}`)}</div>
<div style="margin-top:.6mm">Trượt đều: ${nw(`${m('\\mu=\\tan\\alpha\\approx')} ${f(12)}`)}; so với bảng ở Tập 62·3: ${ck}khớp ${ck}lệch</div></div>
${H.nangVan()}</div>
${h3(2, 'II.5 · Ma sát lăn · có lợi, có hại', '3·2')}
<div class="card fig-side" style="${fs(36)};padding:1.2mm 3mm"><div>
<div>Ma sát lăn có khi vật ${f(25)} trên bề mặt; ${ck}lớn hơn ${ck}nhỏ hơn ma sát trượt rất nhiều.</div>
<div>Có lợi (2 ví dụ): ${f(25)} · ${f(25)}</div>
<div>Có hại (2 ví dụ): ${f(25)} · ${f(25)}</div>
<table style="margin-top:1mm;font-size:var(--fs-sm)"><tr><th style="width:17mm"></th><th>Nghỉ</th><th>Trượt</th><th>Lăn</th></tr>
<tr><td>Khi nào</td><td></td><td></td><td></td></tr><tr><td>Độ lớn</td><td></td><td></td><td></td></tr></table></div>
${H.gaiLop()}</div>
${h3(3, 'IV · Trả bài 6 câu', '3·3')}
${box(`${tb('1. Ma sát nghỉ xuất hiện khi nào? Chiều, độ lớn?')}${lines(2)}
${tb('2. Công thức ma sát trượt, tên và đơn vị từng kí hiệu.')}${lines(1)}
${tb('3. Ma sát trượt phụ thuộc và không phụ thuộc vào gì?')}${lines(2)}
${tb('4. Áp lực N trong ba trường hợp?')}${lines(2)}
${tb('5. So sánh ma sát nghỉ cực đại, ma sát trượt, ma sát lăn.')}${lines(1)}
${tb('6. Ma sát luôn ngược chiều chuyển động: đúng hay sai? Ví dụ.')}${lines(1)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/6 câu · chưa thuộc: ${f(25)} ${nw(`→ đọc lại ô ${f(12)} Tập`)}</div>
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('BẪY · TỰ KIỂM TRA · BÀI TOÁN MẪU')}
${h3(1, 'III · Ba cái bẫy hay sập', '4·1')}
<div class="card" style="padding:1mm 3mm">
<div class="trap">${ck}<span><b>“Ma sát lúc nào cũng bằng ${m('\\mu N')}.”</b> Đứng yên: ma sát nghỉ, tính bằng cân bằng lực.</span></div>
<div class="trap">${ck}<span><b>“Áp lực luôn bằng ${m('mg')}.”</b> Kéo chếch lên: ${m('mg-F\\sin\\alpha')}; mặt nghiêng: ${m('mg\\cos\\alpha')}.</span></div>
<div class="trap">${ck}<span><b>“Ma sát luôn cản chuyển động.”</b> Bước đi: ma sát nghỉ đẩy bàn chân tới trước.</span></div></div>
${h3(2, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '4·2')}
${rkHai([1, 2, 3], [4, 5, 6])}
${h3(3, 'V · Bài toán mẫu: cầu trượt ở công viên', '4·3')}
<div class="card soft" style="padding:1.2mm 3mm">Một bạn nhỏ được thả không vận tốc đầu từ đỉnh cầu trượt dài ${m('2{,}0\\ \\mathrm m')}, nghiêng ${m('30^\\circ')} so với phương ngang. Hệ số ma sát trượt giữa bạn và mặt trượt là ${m('0{,}20')}. Lấy ${g98}.
<div>Tìm gia tốc của bạn và tốc độ ở chân cầu trượt.</div></div>
${h3(4, 'Phân tích đề')}
<table><tr><th style="width:56mm">Câu trong đề</th><th>Dữ liệu → kiến thức</th></tr>
<tr><td>“thả không vận tốc đầu”</td><td>${m('v_0=0')} (dữ kiện ngầm)</td></tr>
<tr><td style="height:6.5mm">“cầu trượt dài 2,0 m”</td><td></td></tr>
<tr><td style="height:6.5mm">“nghiêng 30°”</td><td></td></tr>
<tr><td style="height:6.5mm">“hệ số ma sát trượt 0,20”</td><td></td></tr>
<tr><td style="height:6.5mm">“gia tốc, tốc độ ở chân cầu trượt”</td><td></td></tr></table>
${h3(5, 'Giải')}
<div class="fig-side" style="${fs(52)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl(`Chiếu lên ${m('Oy')}: ${m('N=')}`, 1)}${wl(`Chiếu lên ${m('Ox')}, tìm ${m('a')}:`, 3)}${wl(`Tốc độ ${m('v')} ở chân cầu:`, 2)}${wl(`Kiểm tra: ${m('a')} so với ${m('g\\sin\\alpha')}?`, 1)}</div>${H.cauTruot()}</div>
${h3(6, `Điền bước còn thiếu: cầu trượt cũ nhám, ${m('\\mu=0{,}40')}`)}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div class="ln"><b>Bước 1 (cho sẵn):</b> ${m('N=mg\\cos 30^\\circ')}, phương trình trên ${m('Ox')} như cũ.</div>
${wl(`Bước 2: ${m('a=')}`, 1)}${wl(`Bước 3: ${m('v=')}`, 1)}</div>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TẬP VỀ NHÀ · THỬ THÁCH · MANG VỀ')}
${K.btvn()}
${h3(2, 'Thử thách phân tầng', '5·2')}
<div class="fig-side" style="${fs(44)}">${box(wl(`${m('\\bigstar')} Kéo thùng ${nw('20 kg')} trượt đều trên sàn ngang bằng lực ngang ${nw('60 N')}; ${g10}. Tìm ${mu}.`, 3)
 + wl(`${m('\\bigstar\\bigstar')} Kéo thùng ${nw('10 kg')} trượt đều trên sàn ngang bằng dây chếch lên ${nw('45°')}; ${nw(m('\\mu=0{,}20'))}; ${g98}. Tìm lực kéo.`, 4)
 + wl(`${m('\\bigstar\\bigstar\\bigstar')} Xe tải phanh gấp, khoá bánh, để lại vết trượt dài ${nw('45 m')} trên đường nhựa khô; ${nw(m('\\mu=0{,}70'))}; ${g98}. Lúc bắt đầu trượt xe chạy bao nhiêu km/h?`, 4))}${H.vetPhanh()}</div>
${h3(3, 'Câu đổi chiều: biết chuyển động, tìm hệ số ma sát', '5·3')}
${box(wl(`Xe đạp và người ${nw('86 kg')} đang chạy ${nw('4 m/s')} thì bóp phanh khoá bánh, xe trượt ${nw('2 m')} rồi dừng trên đường ngang; ${g10}. Tìm gia tốc, lực ma sát và ${mu} giữa lốp và đường.`, 5))}
${h3(4, 'VI · Mang về: điều em dễ quên nhất', '5·4')}
${box(wl('1.', 3) + wl('2.', 3) + wl('3.', 3))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Ma sát nghỉ hay ma sát trượt: tủ đứng yên hay trượt',
    de: `Tủ lạnh ${m('50\\ \\mathrm{kg}')}: kéo ngang tăng dần thì bắt đầu trượt ở ${nw(`${m('160\\ \\mathrm N')};`)} giữ trượt đều cần ${nw(`${m('120\\ \\mathrm N')}.`)}<br><b>a)</b> kéo ngang ${m('140\\ \\mathrm N')}: tủ đứng yên hay trượt, lực ma sát bao nhiêu<br><b>b)</b> kéo ngang ${m('200\\ \\mathrm N')}: tủ đứng yên hay trượt, lực ma sát và gia tốc`,
    nd: `${nw(`${Fmax} ${m('=')} ${f(12)}`)}; đã trượt: ${nw(`${Fmst} ${m('=')} ${f(12)}`)}`, a: ['a', 'b'], gi: 3, cot: 2 },
  { t: `Dạng 2 · Trung bình · Mặt ngang: ${mu}, gia tốc, đoạn trượt thêm`,
    de: `Thùng gỗ ${m('40\\ \\mathrm{kg}')} trên sàn ngang; kéo ngang ${m('98\\ \\mathrm N')} thì thùng trượt đều; ${nw(`${g98}.`)}<br><b>a)</b> hệ số ma sát trượt<br><b>b)</b> kéo từ nghỉ bằng lực ngang ${m('150\\ \\mathrm N')}: gia tốc<br><b>c)</b> sau ${m('4{,}0\\ \\mathrm s')} kéo thì buông dây: thùng trượt thêm bao xa`,
    nd: `trượt đều ⇒ ${nw(`${Fmst} ${m('=')} ${f(12)}`)}; buông dây: ${nw(`${m('a=-')} ${f(12)}`)}`, a: ['a', 'b', 'c'], gi: 4 },
  { t: 'Dạng 3 · Khá · Kéo chếch lên: áp lực thay đổi',
    de: `Thùng ${m('6{,}0\\ \\mathrm{kg}')} trên sàn ngang, ${nw(m('\\mu=0{,}30'))}, ${nw(`${g98}.`)} Kéo bằng dây chếch lên ${m('30^\\circ')}, lực ${m('30\\ \\mathrm N')}, thùng trượt từ nghỉ.<br><b>a)</b> áp lực của thùng lên sàn<br><b>b)</b> lực ma sát trượt<br><b>c)</b> gia tốc của thùng`,
    nd: `${nw(`${m('N=mg-')} ${f(14)}`)}; phương ngang: ${nw(`${f(14)} − ${Fmst} ${m('=ma')}`)}`, a: ['a', 'b', 'c'], gi: 4, fig: H.d3 },
  { t: 'Dạng 4 · Khá · Trượt xuống mặt phẳng nghiêng',
    de: `Bao hàng ${m('12\\ \\mathrm{kg}')} thả không vận tốc đầu ở đỉnh tấm ván dốc dài ${nw(`${m('5{,}0\\ \\mathrm m')},`)} nghiêng ${nw(`${m('35^\\circ')};`)} ${nw(`${m('\\mu=0{,}30')};`)} ${nw(`${g98}.`)}<br><b>a)</b> áp lực lên ván và lực ma sát trượt<br><b>b)</b> gia tốc của bao hàng<br><b>c)</b> tốc độ khi tới chân ván`,
    nd: `${nw(`${m('N=')} ${f(16)}`)}; ${nw(`${m('a=g(')} ${f(22)} ${m(')')}`)}, khối lượng ${ck}triệt tiêu ${ck}cần biết`, a: ['a', 'b', 'c'], gi: 5, fig: H.d4, cot: 2 },
  { t: 'Dạng 5 · Khó · Lên dốc rồi có tụt xuống không',
    de: `Vật ${m('3{,}0\\ \\mathrm{kg}')} ở chân dốc nghiêng ${nw(`${m('25^\\circ')},`)} được truyền vận tốc đầu ${m('6{,}0\\ \\mathrm{m/s}')} dọc dốc, hướng lên; ${nw(m('\\mu=0{,}20'))} (coi ma sát nghỉ cực đại bằng ma sát trượt); ${nw(`${g98}.`)}<br><b>a)</b> gia tốc lúc đi lên và quãng đường đi lên được<br><b>b)</b> tới điểm cao nhất, vật nằm yên hay trượt xuống<br><b>c)</b> nếu vật về tới chân dốc: tốc độ khi đó`,
    nd: `lên dốc: ma sát hướng ${f(14)}; ở đỉnh so ${m('\\tan\\alpha')} với ${f(12)}; xuống dốc ma sát ${ck}đổi chiều ${ck}giữ chiều`, a: ['a', 'b', 'c'], gi: 7, fig: H.d5, cot: 2 },
];

// Bài tương tự giải vào vở (thầy chốt 10/11): 1 cột; ô đáp số 25 mm (40 mm khi ý dài) đặt cuối đúng dòng của ý, nhãn ô khớp a) b) c)…
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
    { t: 'Dạng 1 · Bài 1', de: `Bàn học ${m('20\\ \\mathrm{kg}')} trên sàn. Kéo ngang tăng dần: bàn bắt đầu trượt khi lực ${nw(`${m('80\\ \\mathrm N')};`)} giữ trượt đều cần lực ngang ${nw(`${m('60\\ \\mathrm N')}.`)}<br><b>a)</b> kéo ngang ${m('50\\ \\mathrm N')}: đứng yên hay trượt; lực ma sát<br><b>b)</b> kéo ngang ${m('100\\ \\mathrm N')}: lực ma sát; gia tốc`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>'] },
    { t: 'Dạng 1 · Bài 2', de: `Thùng ${m('30\\ \\mathrm{kg}')} trên sàn ngang, ${nw(`${m('\\mu_n=0{,}50')}`)} (${nw(m('F_{\\mathrm{msn\\,max}}=\\mu_n N'))}), ${nw(`${m('\\mu=0{,}40')};`)} ${nw(`${g10}.`)}<br><b>a)</b> ma sát nghỉ cực đại; ma sát trượt<br><b>b)</b> đẩy ngang ${m('100\\ \\mathrm N')}: lực ma sát<br><b>c)</b> đẩy ngang ${m('210\\ \\mathrm N')}: gia tốc`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'] },
    { t: 'Dạng 2 · Bài 1', de: `Thùng ${m('50\\ \\mathrm{kg}')} trên sàn ngang; kéo ngang ${m('150\\ \\mathrm N')} thì trượt đều; ${nw(`${g10}.`)}<br><b>a)</b> hệ số ma sát trượt<br><b>b)</b> kéo từ nghỉ bằng lực ngang ${m('250\\ \\mathrm N')}: gia tốc<br><b>c)</b> kéo ${m('3{,}0\\ \\mathrm s')} rồi buông dây: thùng trượt thêm bao xa`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 2 · Bài 2', de: `Đẩy hộp ${m('2{,}0\\ \\mathrm{kg}')} trên mặt bàn ngang; hộp rời tay với tốc độ ${m('3{,}0\\ \\mathrm{m/s}')}, trượt ${m('1{,}5\\ \\mathrm m')} rồi dừng; ${nw(`${g10}.`)}<br><b>a)</b> độ lớn gia tốc<br><b>b)</b> lực ma sát<br><b>c)</b> hệ số ma sát trượt`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 3 · Bài 1', de: `Thùng ${m('10\\ \\mathrm{kg}')} trên sàn ngang, ${nw(`${m('\\mu=0{,}25')};`)} kéo bằng dây chếch lên ${nw(`${m('30^\\circ')},`)} lực ${nw(`${m('40\\ \\mathrm N')};`)} ${nw(`${g10}.`)}<br><b>a)</b> áp lực lên sàn<br><b>b)</b> lực ma sát trượt<br><b>c)</b> gia tốc`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 3 · Bài 2', de: `Đẩy thùng ${m('20\\ \\mathrm{kg}')} từ phía sau bằng lực ${m('100\\ \\mathrm N')} chếch <b>xuống</b> ${m('30^\\circ')} so với phương ngang; ${nw(`${m('\\mu=0{,}30')};`)} ${nw(`${g10}.`)}<br><b>a)</b> áp lực lên sàn<br><b>b)</b> lực ma sát trượt<br><b>c)</b> gia tốc`, o: ['a', 'b', 'c'] },
  ], [
    { t: 'Dạng 4 · Bài 1', de: `Hộp ${m('4{,}0\\ \\mathrm{kg}')} thả không vận tốc đầu, trượt xuống hết dốc dài ${nw(`${m('3{,}0\\ \\mathrm m')},`)} nghiêng ${nw(`${m('30^\\circ')};`)} ${nw(`${m('\\mu=0{,}25')};`)} ${nw(`${g98}.`)}<br><b>a)</b> áp lực lên dốc; lực ma sát<br><b>b)</b> gia tốc<br><b>c)</b> tốc độ ở chân dốc`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'] },
    { t: 'Dạng 4 · Bài 2', de: `Một vật trượt <b>đều</b> xuống tấm ván nghiêng ${nw(`${m('20^\\circ')}.`)} Nâng ván lên nghiêng ${m('30^\\circ')}, thả vật không vận tốc đầu (cùng ${mu}); ${nw(`${g98}.`)}<br><b>a)</b> hệ số ma sát trượt<br><b>b)</b> gia tốc khi ván nghiêng ${m('30^\\circ')}<br><b>c)</b> tốc độ sau ${m('2{,}0\\ \\mathrm s')}`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 5 · Bài 1', de: `Vật ${m('2{,}0\\ \\mathrm{kg}')} ở chân dốc nghiêng ${nw(`${m('30^\\circ')},`)} được truyền vận tốc ${m('5{,}0\\ \\mathrm{m/s}')} lên dốc; ${nw(m('\\mu=0{,}20'))} (ma sát nghỉ cực đại = ma sát trượt); ${nw(`${g98}.`)}<br><b>a)</b> độ lớn gia tốc lúc lên; quãng đường lên<br><b>b)</b> ở điểm cao nhất: nằm yên hay trượt xuống<br><b>c)</b> tốc độ khi về chân dốc`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'] },
    { t: 'Dạng 5 · Bài 2', de: `Vật ${m('1{,}0\\ \\mathrm{kg}')} ở chân dốc nghiêng ${nw(`${m('15^\\circ')},`)} được truyền vận tốc ${m('4{,}0\\ \\mathrm{m/s}')} lên dốc; ${nw(m('\\mu=0{,}40'))} (ma sát nghỉ cực đại = ma sát trượt); ${nw(`${g98}.`)}<br><b>a)</b> độ lớn gia tốc lúc lên; quãng đường lên<br><b>b)</b> ở điểm cao nhất: nằm yên hay trượt xuống<br><b>c)</b> lực ma sát lúc đó: loại gì, bao nhiêu`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'] },
    nhap(8),
  ]],
  dap: [
    `D1·1: a<sub>1</sub>) đứng yên · a<sub>2</sub>) 50 N · b<sub>1</sub>) 60 N · b<sub>2</sub>) 2,0 m/s² &nbsp;|&nbsp; D1·2: a<sub>1</sub>) 150 N · a<sub>2</sub>) 120 N · b) 100 N · c) 3,0 m/s² &nbsp;|&nbsp; D2·1: a) 0,30 · b) 2,0 m/s² · c) 6,0 m &nbsp;|&nbsp; D2·2: a) 3,0 m/s² · b) 6,0 N · c) 0,30 &nbsp;|&nbsp; D3·1: a) 80 N · b) 20 N · c) 1,46 m/s² &nbsp;|&nbsp; D3·2: a) 250 N · b) 75 N · c) 0,58 m/s²`,
    `D4·1: a<sub>1</sub>) 33,9 N · a<sub>2</sub>) 8,49 N · b) 2,78 m/s² · c) 4,08 m/s &nbsp;|&nbsp; D4·2: a) 0,36 · b) 1,81 m/s² · c) 3,62 m/s &nbsp;|&nbsp; D5·1: a<sub>1</sub>) 6,60 m/s² · a<sub>2</sub>) 1,89 m · b) trượt xuống · c) 3,48 m/s &nbsp;|&nbsp; D5·2: a<sub>1</sub>) 6,32 m/s² · a<sub>2</sub>) 1,27 m · b) nằm yên · c<sub>1</sub>) ma sát nghỉ · c<sub>2</sub>) 2,54 N`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 2], kq: [[1, 2, 3], [4, 5]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'ma sát nghỉ 1·4 · ma sát trượt 2·1 · đo hệ số ma sát 2·3 · áp lực N 2·4 · tấm ván 3·1 · ma sát lăn 3·2 · bẫy 4·1 · bài toán mẫu 4·3 · dạng 1–3 → 6·1 · dạng 4–5 → 7·1',
  out: process.argv[2],
});
