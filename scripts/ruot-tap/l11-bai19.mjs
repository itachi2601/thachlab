// Ruột tập VL11 – Bài 19 · Thế năng điện (lesson id 38). Quyển Chương 3 lớp 11 (bài 16–21): bài 19 = tr. 37–48.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự giải vào vở · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l11-bai19.mjs (toàn bộ SVG tự vẽ, không dùng ảnh Halliday). Nội dung theo bài web (book/cache/38.json, tải từ DB 12/11/2026):
// mục tiêu, dự đoán hạt bụi máy lọc, II.1–II.6, ví dụ ba đường, thí nghiệm khay nước muối, ba bẫy, Trả bài 6 câu,
// bài toán mẫu electron giữa hai bản, thử thách 3 mức, mang về, 4 dạng bài tập mẫu.
// Đáp số Bài tương tự (tuongTu.dap) tính bằng Python 12/11/2026.
// Chạy: node scripts/ruot-tap/l11-bai19.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl11-bai19.pdf
//       node scripts/ruot-tap/l11-bai19.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l11-bai19/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL11b19 as H } from './hinh-l11-bai19.mjs';

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
  const out = resolve(HERE, 'out/hinh-l11-bai19'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 19, lid: 38, ten: 'THẾ NĂNG ĐIỆN', lop: 11, baiDau: 16, sub: 'Vật lí 11 · Chương 3: Điện trường' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const sci = (a, n) => m(`${a}\\cdot10^{${n}}`);
const qe = nw(m('q_e=-1{,}6\\cdot10^{-19}\\ \\mathrm C'));
const vE = m('\\vec E');
const qeP = nw(`(${m('q_e=-1{,}6\\cdot10^{-19}\\ \\mathrm C')})`), qeP1 = nw(`(${m('q_e=-1{,}6\\cdot10^{-19}\\ \\mathrm C')},`) + ' ';

// Bài tương tự giải vào vở: ô đáp số đặt cuối đúng dòng của ý (giống l10-bai23).
const ttCss = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';

const p1 = `${ttCss}<section class="page">
${head('BÀI 19 · THẾ NĂNG ĐIỆN', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Tính công của lực điện ${m('A=qEd')}, đặt đúng <b>dấu</b> của ${m('q')} và ${m('d')}`)}
${dong(`${ck}Giải thích vì sao công của lực điện <b>không phụ thuộc đường đi</b>`)}
${dong(`${ck}Nêu ý nghĩa <b>thế năng điện</b>, biết chọn mốc và tính ${m('W_M')}`)}
${dong(`${ck}Dùng ${m('A_{MN}=W_M-W_N')} nối công, thế năng và động năng`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Máy lọc không khí: hạt bụi mang điện âm bị tấm thu hút về. Hai hạt bụi giống hệt cùng rời đầu kim, cùng bám vào N: một bay thẳng, một lượn cong. Chỉ xét lực điện, công của lực điện làm mỗi hạt đi từ đầu kim tới N thì:</p>
<div class="fig-side" style="${fs(46)}"><div>
${opt('A', 'Hạt bay đường cong lớn hơn, vì đi quãng dài hơn')}
${opt('B', 'Hạt bay thẳng lớn hơn, vì luôn đi đúng hướng lực hút')}
${opt('C', 'Bằng nhau, vì cùng đầu, cùng cuối')}
${opt('D', 'Hạt bay cong bằng 0, vì không đi theo hướng lực')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 1)}</div>
${H.hatBui()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(2)}</div>
${h3(4, 'II.1 · Công của lực điện trong điện trường đều', '1·4')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div>Điện trường đều: lực ${m('\\vec F=q\\vec E')} không đổi về ${f(16)} và ${f(16)}.</div>
<div style="margin:.6mm 0">${m('A_{MN}=')} ${f(12)} · ${f(12)} · ${f(12)}</div>
<div>${m('q')} lấy cả ${f(14)}. ${m('d')} là độ dài đại số ${f(25)} của MN lên ${f(25)}.</div>
<div>${m('d>0')}: hình chiếu ${f(18)} chiều đường sức; ${m('d<0')}: ${f(18)} chiều.</div>
<div>MN vuông góc đường sức: ${nw(`${m('d=')} ${f(10)}`)}, ${nw(`${m('A=')} ${f(10)}`)}.</div>
<div>${nw(`Proton ${m('q=+1{,}6\\cdot10^{-19}\\ \\mathrm C')}`)} · ${nw(`electron ${qe}`)}</div></div>
${H.hinhChieu()}</div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('DẤU CỦA d · CÔNG KHÔNG PHỤ THUỘC ĐƯỜNG ĐI · THẾ NĂNG')}
${h3(1, 'Hình chiếu d có dấu', '2·1')}
<div style="display:grid;grid-template-columns:1fr 1fr;gap:3mm;align-items:start"><table>
<tr><th>Đoạn đi trong điện trường đều</th><th style="width:15mm">${m('d')}</th></tr>
<tr><td>MN 5 cm, chiếu được 3 cm cùng chiều</td><td></td></tr>
<tr><td>MN dài ${m('s')}, hợp chiều đường sức góc ${m('\\alpha')}</td><td></td></tr>
<tr><td>4 cm vuông góc đường sức</td><td></td></tr>
<tr><td>2 cm ngược chiều đường sức</td><td></td></tr></table>
<table>
<tr><th>Đi xuôi đường sức</th><th style="width:17mm">Proton</th><th style="width:17mm">Electron</th></tr>
<tr><td style="height:7mm">Lực so với ${vE}</td><td>cùng chiều</td><td></td></tr>
<tr><td style="height:7mm">Dấu của ${m('A')}</td><td></td><td></td></tr>
<tr><td style="height:7mm">Thế năng tăng/giảm</td><td></td><td></td></tr></table></div>
${box(cau(`<b>Câu 1.</b> Electron đi ${nw('2 cm')} ngược chiều đường sức, ${nw(m('E=1000\\ \\mathrm{V/m}'))}. Công của lực điện? Dấu?`, 4), 'margin-top:1mm')}
${h3(2, 'II.2 · Công không phụ thuộc đường đi · lực thế', '2·2')}
<div class="card fig-side" style="${fs(44)};padding:1.2mm 3mm"><div>
<div>Đi gấp khúc M → P → N: ${nw(`${m('A_{MP}=')} ${f(10)}`)} vì MP ${f(25)} đường sức;</div>
<div>${nw(`${m('A_{PN}=')} ${f(16)}`)}. Tổng ${f(12)} công đi thẳng MN.</div>
<div>Công của lực điện chỉ phụ thuộc ${f(22)} và ${f(22)}, không phụ thuộc ${f(22)}.</div>
<div>Đi một vòng kín về chỗ cũ: ${nw(`${m('A=')} ${f(10)}`)}.</div>
<div><b>Lực thế:</b> ${f(18)}, ${f(18)}, ${f(18)}. Lực ${f(18)} không phải lực thế.</div></div>
${H.baDuong()}</div>
${h3(3, 'II.3 · Thế năng điện', '2·3')}
<div class="card fig-side" style="${fs(44)};padding:1.2mm 3mm"><div>
<div>${m('W_M')} đặc trưng cho ${f(40)} của điện trường khi đặt ${m('q')} tại M.</div>
<div>Số đo: công của lực điện khi ${m('q')} đi từ M tới ${f(25)}.</div>
<div>Điện trường đều, mốc ở bản âm: ${nw(`${m('W_M=')} ${f(16)}`)}, ${m('d')} = khoảng cách từ M tới ${f(16)}.</div>
<div>Điện tích điểm ${m('Q')}, mốc ở vô cực: ${nw(`${m('W=')} ${f(16)}`)}</div>
<div class="hint">(${nw(m('k=9\\cdot10^9\\ \\mathrm{N\\,m^2/C^2}'))}; ${m('q')}, ${m('Q')} lấy cả dấu)</div>
<div><b>“${m('qEd')} như ${m('mgh')}”:</b> ${m('q')} ↔ ${f(10)}, ${m('E')} ↔ ${f(10)}, ${m('d')} ↔ ${f(10)}</div>
<div>Với ${m('q<0')}: càng xa mốc, ${m('W')} càng ${f(16)}.</div></div>
${H.haiBan()}</div>
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('CÔNG VÀ THẾ NĂNG · ĐIỆN THẾ · THÍ NGHIỆM · BẪY')}
${h3(1, 'II.4 · Đo thử: khay nước muối, hai lá đồng cách 10,0 cm, nguồn 6,0 V', '3·1')}
<div class="fig-side" style="${fs(46)}"><div>
<div style="margin-bottom:.6mm"><b>Làm:</b> cực âm vôn kế nối lá âm; que đo đặt cách lá âm ${m('x')}.</div>
<table class="tbl-ct"><tr><th>${m('x\\ (\\mathrm{cm})')}</th><th>${m('V')} đo ${m('(\\mathrm V)')}</th><th>${m('V/x')} (V/m, đổi ${m('x')} ra m)</th></tr>
<tr><td>2,0</td><td>1,18</td><td></td></tr>
<tr><td>4,0</td><td>2,43</td><td></td></tr>
<tr><td>6,0</td><td>3,57</td><td></td></tr>
<tr><td>8,0</td><td>4,84</td><td></td></tr></table>
<div style="margin-top:.6mm"><b>Rút ra:</b> ${m('V')} tỉ lệ ${f(10)} với ${m('x')}; ${nw(`${m('E\\approx')} ${f(12)} V/m`)}. Thế năng của 1 C tại đó ${m('W=Ex')}.</div></div>
${H.doThi()}</div>
${box(wl('Lí thuyết 0,60 V/cm, sao bảng lệch tới 2 %? Nêu 2 nguyên nhân:', 2), 'margin-top:1mm')}
${h3(2, 'II.5 · Công bằng độ giảm thế năng', '3·2')}
<div class="card" style="padding:1.2mm 3mm">
<div>${m('A_{MN}=')} ${f(14)} − ${f(14)} ${m('=-\\Delta W')}</div>
<div>${m('A>0')}: thế năng ${f(16)}; &nbsp;${m('A<0')}: thế năng ${f(16)}.</div>
<div>Chỉ có lực điện: thế năng giảm bao nhiêu thì ${f(25)} tăng bấy nhiêu.</div>
<div>Từ nghỉ: ${nw(`${m('A=')} ${f(16)}`)} ⇒ ${nw(`${m('v=')} ${f(25)}`)}</div>
<div>Đổi mốc thì từng ${m('W')} ${f(14)}; hiệu ${m('W_M-W_N')} ${f(16)}. Điền bảng:</div>
<table style="margin-top:.6mm"><tr><th>Mốc đặt ở</th><th>${m('W_M')}</th><th>${m('W_N')}</th><th>${m('W_M-W_N')}</th></tr>
<tr><td>Điểm O</td><td>6 mJ</td><td>2 mJ</td><td></td></tr>
<tr><td>Điểm N</td><td></td><td>0</td><td></td></tr></table></div>
${box(cau(`<b>Câu 2.</b> Mốc ở bản âm. Electron đặt cách bản âm ${nw('2 cm')}: thế năng dương, âm hay bằng 0? Vì sao?`, 2), 'margin-top:1mm')}
${h3(3, 'II.6 · Nối sang Bài 20: điện thế', '3·3')}
<div class="card soft" style="padding:1mm 3mm"><div>${m('V_M=W_M/q')} (đơn vị ${f(10)}) &nbsp;·&nbsp; ${m('U_{MN}=V_M-V_N')} ⇒ ${nw(`${m('A_{MN}=')} ${f(14)}`)}</div><div>Đi xuôi đường sức thì ${m('V')} ${f(16)}</div></div>
${h3(4, 'III · Ba cái bẫy hay sập', '3·4')}
<div class="card" style="padding:1mm 3mm">
<div class="trap">${ck}<span><b>“${m('d')} là độ dài đường đi.”</b> ${m('d')} là hình chiếu, có dấu; đi vuông góc thì ${m('d=0')}.</span></div>
<div class="trap">${ck}<span><b>“Bỏ dấu của điện tích.”</b> Viết ${m('q')} kèm dấu trước; dấu của ${m('A')} là tích hai dấu.</span></div>
<div class="trap">${ck}<span><b>“Thế năng có giá trị tuyệt đối.”</b> ${m('W')} đổi theo mốc, hiệu ${m('W_M-W_N')} thì không.</span></div></div>
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('TRẢ BÀI · TỰ KIỂM TRA · BÀI TOÁN MẪU')}
${h3(1, 'IV · Trả bài 6 câu', '4·1')}
${box(`${tb('1. Công thức công của lực điện? d là gì?')}${lines(1)}
${tb('2. Công của lực điện phụ thuộc gì, không phụ thuộc gì?')}${lines(1)}
${tb('3. Thế năng điện đặc trưng cho gì? Số đo bằng gì?')}${lines(1)}
${tb('4. Viết W<sub>M</sub> trong điện trường đều và quanh điện tích điểm.')}${lines(1)}
${tb('5. Công liên hệ với thế năng thế nào? A > 0 thì thế năng ra sao?')}${lines(1)}
${tb('6. Hai trường hợp điện tích di chuyển mà lực điện không sinh công?')}${lines(1)}`)}
${h3(2, 'Kết quả tự kiểm tra (7 câu trên web)', '4·2')}
${rkHai([1, 2, 3, 4], [5, 6, 7])}
${h3(3, 'V · Bài toán mẫu: electron giữa hai bản', '4·3')}
<div class="card soft fig-side" style="${fs(44)};padding:1.2mm 3mm"><div>Hai bản phẳng nằm ngang cách nhau ${nw('4 cm')}, bản trên dương, bản dưới âm; ${nw(m('E=2000\\ \\mathrm{V/m}'))}. Electron ${qeP1}${nw(m('m=9{,}1\\cdot10^{-31}\\ \\mathrm{kg}'))}) đi từ M (cách bản âm ${nw('1 cm')}) sang ngang ${nw('3 cm')} tới P, rồi thẳng lên ${nw('2 cm')} tới N.
<div><b>a)</b> Công của lực điện trên đường M → P → N.</div>
<div><b>b)</b> Mốc thế năng ở bản âm: tính ${m('W_M')}, ${m('W_N')}, kiểm lại câu a.</div>
<div><b>c)</b> Electron khác rời M từ nghỉ, chỉ chịu lực điện: tốc độ khi cách bản âm ${nw('3 cm')}.</div></div>
${H.mau()}</div>
<table><tr><th style="width:52mm">Câu trong đề</th><th>Dữ liệu → kiến thức</th></tr>
<tr><td>“bản trên dương, bản dưới âm”</td><td>${vE} hướng xuống</td></tr>
<tr><td style="height:5.5mm">“sang ngang 3 cm tới P”</td><td></td></tr>
<tr><td style="height:5.5mm">“thẳng lên 2 cm tới N”</td><td></td></tr>
<tr><td style="height:5.5mm">“mốc ở bản âm”, M cách 1 cm</td><td></td></tr>
<tr><td style="height:5.5mm">“rời M từ nghỉ”</td><td></td></tr></table>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('GIẢI BÀI MẪU · BÀI TẬP VỀ NHÀ · THỬ THÁCH')}
${h3(1, 'Giải bài toán mẫu', '5·1')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl(`a) ${m('A_{MP}')}, ${m('A_{PN}')}, ${m('A_{MPN}')}:`, 3)}${wl(`b) ${m('W_M')}, ${m('W_N')}, kiểm lại:`, 3)}${wl(`c) Công, rồi ${m('v')}:`, 3)}</div>
${h3(2, 'Điền bước còn thiếu: thay electron bằng proton, đi M → P → N')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div class="ln"><b>Bước 1 (cho sẵn):</b> ${m('A_{MP}=0')} vì MP vuông góc đường sức.</div>
${wl(`Bước 2: ${m('d=')}`, 1)}${wl(`${m('A_{PN}=')}`, 1)}${wl('Bước 3: thế năng proton tăng hay giảm, bao nhiêu?', 2)}</div>
${K.btvn().replace('<i>1</i>', '<i>3</i>')}
${h3(4, 'Thử thách phân tầng', '5·4')}
<div class="fig-side" style="${fs(38)}">${box(wl(`${m('\\bigstar')} Điện tích ${nw(m('5\\ \\mu\\mathrm C'))} đi một vòng kín. Công của lực điện?`, 1)
 + wl(`${m('\\bigstar\\bigstar')} Tam giác đều ABC cạnh ${nw('10 cm')}, ${nw(m('E=3000\\ \\mathrm{V/m}'))} song song BC, chiều B → C, ${nw(m('q=+2\\ \\mu\\mathrm C'))}: tính ${m('A_{AB}')}, ${m('A_{BC}')}, ${m('A_{CA}')}.`, 3)
 + wl(`${m('\\bigstar\\bigstar\\bigstar')} Nếu công lực điện phụ thuộc đường đi thì có chế được “máy chạy mãi” không? Vì sao?`, 2))}${H.tamGiac()}</div>
${h3(5, 'VI · Mang về: điều em dễ quên nhất', '5·5')}
${box(wl('1.', 2) + wl('2.', 1) + wl('3.', 1))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Công A = qEd: hình chiếu có dấu và dấu của điện tích',
    de: `Điện trường đều ${m('E=5000\\ \\mathrm{V/m}')}, đường sức nằm ngang hướng sang phải. Electron ${qeP} đi thẳng từ M đến N, ${nw(m('MN=8{,}0\\ \\mathrm{cm}'))} hợp với chiều đường sức góc ${nw(`${m('120^\\circ')}.`)} Chỉ xét lực điện.<br><b>a)</b> độ dài đại số ${m('d')} của hình chiếu MN lên đường sức<br><b>b)</b> công ${m('A_{MN}')}<br><b>c)</b> electron đi thẳng từ N về M: ${m('A_{NM}')}`,
    nd: `${nw(`${m('d=MN\\cos\\alpha')}`)}, góc tù ⇒ ${m('d')} ${f(12)}; dấu của ${m('A')} = dấu ${m('q')} × dấu ${m('d')} ⇒ ${m('A')} ${f(12)}`, a: ['a', 'b', 'c'], gi: 6, fig: H.d1(''), cot: 3 },
  { t: 'Dạng 2 · Trung bình · Công không phụ thuộc đường đi: gấp khúc, đường cong, vòng kín',
    de: `${nw(m('E=3000\\ \\mathrm{V/m}'))}, đường sức hướng từ A sang B. Hạt ${nw(m('q=-2{,}0\\ \\mu\\mathrm C'))} đi từ A đến B (${nw(m('AB=6{,}0\\ \\mathrm{cm}'))} dọc đường sức), rồi B đến C (${nw(m('BC=10\\ \\mathrm{cm}'))}, hợp với chiều đường sức ${nw(`${m('60^\\circ')})`)}.<br><b>a)</b> công trên đường A → B → C<br><b>b)</b> từ A tới D theo đường cong dài ${nw('25 cm')}; D ngay dưới C, ${nw(m('CD=4{,}0\\ \\mathrm{cm}'))} vuông góc đường sức: công<br><b>c)</b> đi A → B → C rồi về A theo CA: công cả vòng`,
    nd: `Đổi ${nw(`${m('\\mu\\mathrm C')} → C`)}; độ dài ${nw('25 cm')} ${ck}có ${ck}không đi vào công thức; ${m('d_{AD}=d_{AC}')} vì<br>${f(60)}`, a: ['a', 'b', 'c'], gi: 7, fig: H.d2(''), cot: 3 },
  { t: 'Dạng 3 · Trung bình · Thế năng có mốc: từ W<sub>M</sub> và công tìm E, vị trí N, rồi đổi mốc',
    de: `Hai bản phẳng nằm ngang cách nhau ${nw('5,0 cm')}; bản trên âm, bản dưới dương; điện trường đều. Hạt bụi ${nw(m('q=-5{,}0\\ \\mathrm{nC}'))}. Mốc thế năng ở bản trên. Tại M cách bản trên ${nw('1,0 cm')}: ${nw(`${m('W_M=-2{,}0\\cdot10^{-7}\\ \\mathrm J')}.`)} Hạt đi tới N nằm dưới M, lực điện sinh công ${nw(`${m('A_{MN}=+6{,}0\\cdot10^{-7}\\ \\mathrm J')}.`)} Bỏ qua trọng lực.<br><b>a)</b> cường độ điện trường<br><b>b)</b> thế năng ${m('W_N')}<br><b>c)</b> khoảng cách từ N tới bản trên<br><b>d)</b> đổi mốc sang bản dưới: thế năng tại N`,
    nd: `${vE} hướng ${f(12)}; từ M lên mốc là ${ck}xuôi ${ck}ngược ${vE}; ${nw(`${m('W_N=W_M-')} ${f(12)}`)}`, a: ['a', 'b', 'c', 'd'], gi: 5, fig: H.d3(''), cot: 2 },
  { t: 'Dạng 4 · Khó · Từ nghỉ, chỉ có lực điện: công = độ tăng động năng, tìm ngược E',
    de: `Hạt bụi ${nw(m('q=+4{,}0\\ \\mathrm{nC}'))}, ${nw(m('m=2{,}0\\cdot10^{-8}\\ \\mathrm{kg}'))}, thả nghỉ tại M giữa hai bản phẳng nằm ngang (bản trên dương, bản dưới âm), M cách bản âm ${nw('5,0 cm')}. Hạt đi thẳng xuống theo đường sức, tới bản âm với tốc độ ${nw('10 m/s')}. Chỉ có lực điện.<br><b>a)</b> công của lực điện từ M tới bản âm<br><b>b)</b> cường độ điện trường<br><b>c)</b> tốc độ khi qua P, cách bản âm ${nw('2,0 cm')}`,
    nd: `Từ nghỉ: ${nw(`${m('A=')} ${f(14)}`)}; ${nw(`${m('d_{MP}=')} ${f(12)}`)}, không phải 2,0 cm`, a: ['a', 'b', 'c'], gi: 6, fig: H.d4(''), cot: 3 },
];

const oY = (s, o, w = 25) => s.split('<br>').map((p) => {
  const y = p.match(/^<b>([a-d])\)<\/b>/);
  if (!y) return `<div>${p}</div>`;
  const ls = o.filter((l) => l[0] === y[1]);
  return `<div class="yo"><span>${p}</span><span class="oo">${ls.map((l) => `<span class="nw"><b>${l})</b>${f(w)}</span>`).join('')}</span></div>`;
}).join('');
const ttDe = (b) => b.fig ? `<div class="fig-side" style="grid-template-columns:1fr ${b.fw}mm">${`<div>${oY(b.de, b.o, b.ow)}</div>`}${b.fig}</div>` : oY(b.de, b.o, b.ow);
const vaoVo = (ds) => ds.map((b) => (b.o ? { t: b.t, de: ttDe(b), k: 0 } : b));
const nhap = (n) => ({ t: '<span class="nhap-t">Nháp / chỗ em còn vướng</span>', de: lines(n), k: 0 });
const J = (s) => nw(`${s} J`);
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–2', 'DẠNG 3–4'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Proton (${nw(m('q=+1{,}6\\cdot10^{-19}\\ \\mathrm C'))}) đi thẳng từ M đến N trong điện trường đều ${nw(`${m('E=4000\\ \\mathrm{V/m}')};`)} ${nw(m('MN=6{,}0\\ \\mathrm{cm}'))} hợp với chiều đường sức ${nw(`${m('60^\\circ')}.`)}<br><b>a)</b> hình chiếu ${m('d')} (cm)<br><b>b)</b> công ${m('A_{MN}')}<br><b>c)</b> công ${m('A_{NM}')} khi đi ngược lại`, o: ['a', 'b', 'c'], ow: 30 },
    { t: 'Dạng 1 · Bài 2', de: `Electron ${qeP} trong điện trường đều ${nw(`${m('E=2500\\ \\mathrm{V/m}')}.`)} Tính công của lực điện khi nó đi đoạn thẳng dài ${nw('4,0 cm')}:<br><b>a)</b> vuông góc đường sức<br><b>b)</b> ngược chiều đường sức<br><b>c)</b> hợp với chiều đường sức góc ${m('150^\\circ')}`, o: ['a', 'b', 'c'], ow: 30 },
    { t: 'Dạng 2 · Bài 1', de: `${nw(m('E=2000\\ \\mathrm{V/m}'))}. Điện tích ${nw(m('q=+3{,}0\\ \\mu\\mathrm C'))} đi từ A đến B (${nw('5,0 cm')} dọc đường sức, cùng chiều), rồi từ B đến C (${nw('8,0 cm')} vuông góc đường sức).<br><b>a)</b> công ${m('A_{AB}')}<br><b>b)</b> công trên đường A → B → C<br><b>c)</b> từ A tới C theo một đường cong dài ${nw('20 cm')}: công<br><b>d)</b> đi A → B → C rồi về A: công cả vòng`, fig: H.tt21(''), fw: 40, o: ['a', 'b', 'c', 'd'], ow: 30 },
    { t: 'Dạng 2 · Bài 2', de: `${nw(m('E=5000\\ \\mathrm{V/m}'))}. Điện tích ${nw(m('q=-4{,}0\\ \\mu\\mathrm C'))} đi từ A đến B (${nw('4,0 cm')} ngược chiều đường sức), rồi từ B đến C (${nw('6,0 cm')}, hợp với chiều đường sức ${nw(`${m('60^\\circ')})`)}.<br><b>a)</b> công ${m('A_{AB}')}<br><b>b)</b> công ${m('A_{BC}')}<br><b>c)</b> công trên đường A → B → C<br><b>d)</b> công ${m('A_{CA}')} khi đi thẳng từ C về A`, o: ['a', 'b', 'c', 'd'], ow: 30 },
    nhap(5),
  ], [
    { t: 'Dạng 3 · Bài 1', de: `Hai bản phẳng nằm ngang cách nhau ${nw('6,0 cm')}, bản trên dương, bản dưới âm. Điện tích ${nw(m('q=+2{,}0\\ \\mathrm{nC}'))}; mốc thế năng ở bản dưới. Tại M cách bản dưới ${nw('4,0 cm')}: ${nw(`${m('W_M=+4{,}0\\cdot10^{-7}\\ \\mathrm J')}.`)} Hạt đi từ M tới N (N nằm giữa hai bản), lực điện sinh công ${nw(`${m('+3{,}0\\cdot10^{-7}\\ \\mathrm J')}.`)}<br><b>a)</b> cường độ điện trường<br><b>b)</b> thế năng ${m('W_N')}<br><b>c)</b> khoảng cách từ N tới bản dưới<br><b>d)</b> đổi mốc sang bản trên: thế năng tại N`, o: ['a', 'b', 'c', 'd'], ow: 30 },
    { t: 'Dạng 3 · Bài 2', de: `Hai bản phẳng thẳng đứng cách nhau ${nw('5,0 cm')}, bản trái dương, bản phải âm, ${nw(`${m('E=4000\\ \\mathrm{V/m}')}.`)} Electron ${qeP}; mốc ở bản âm. M cách bản âm ${nw('3,0 cm')}, N cách bản âm ${nw('1,0 cm')}.<br><b>a)</b> ${m('W_M')}<br><b>b)</b> ${m('W_N')}<br><b>c)</b> công ${m('A_{MN}')}<br><b>d)</b> đổi mốc sang bản dương: ${m('W_M')}`, fig: H.tt32('M, N trên cùng một đường sức.'), fw: 42, o: ['a', 'b', 'c', 'd'], ow: 30 },
    { t: 'Dạng 4 · Bài 1', de: `Hai bản phẳng song song cách nhau ${nw('2,0 cm')}, ${nw(`${m('E=1000\\ \\mathrm{V/m}')}.`)} Electron ${qeP1}${nw(m('m=9{,}1\\cdot10^{-31}\\ \\mathrm{kg}'))}) rời bản âm từ nghỉ, chỉ chịu lực điện.<br><b>a)</b> công của lực điện tới bản dương<br><b>b)</b> tốc độ khi chạm bản dương<br><b>c)</b> tốc độ khi đi được nửa đường`, o: ['a', 'b', 'c'], ow: 30 },
    { t: 'Dạng 4 · Bài 2', de: `Hạt bụi ${nw(m('q=+2{,}0\\ \\mathrm{nC}'))}, ${nw(m('m=1{,}0\\cdot10^{-8}\\ \\mathrm{kg}'))}, thả nghỉ tại M cách bản âm ${nw('4,0 cm')}, đi thẳng theo đường sức tới bản âm với tốc độ ${nw('8,0 m/s')}. Chỉ có lực điện.<br><b>a)</b> công của lực điện<br><b>b)</b> cường độ điện trường<br><b>c)</b> tốc độ khi qua P, cách bản âm ${nw('3,0 cm')}`, o: ['a', 'b', 'c'], ow: 30 },
    nhap(4),
  ]],
  dap: [
    `D1·1: a) 3,0 cm · b) ${J(sci('1{,}92', -17))} · c) ${J(sci('-1{,}92', -17))}<br>D1·2: a) 0 · b) ${J(sci('+1{,}6', -17))} · c) ${J(sci('+1{,}39', -17))}<br>D2·1: a) ${J(sci('3{,}0', -4))} · b) ${J(sci('3{,}0', -4))} · c) ${J(sci('3{,}0', -4))} · d) 0<br>D2·2: a) ${J(sci('+8{,}0', -4))} · b) ${J(sci('-6{,}0', -4))} · c) ${J(sci('+2{,}0', -4))} · d) ${J(sci('-2{,}0', -4))}`,
    `D3·1: a) 5000 V/m · b) ${J(sci('+1{,}0', -7))} · c) 1,0 cm · d) ${J(sci('-5{,}0', -7))}<br>D3·2: a) ${J(sci('-1{,}92', -17))} · b) ${J(sci('-6{,}4', -18))} · c) ${J(sci('-1{,}28', -17))} · d) ${J(sci('+1{,}28', -17))}<br>D4·1: a) ${J(sci('3{,}2', -18))} · b) ${nw(`${sci('2{,}65', 6)} m/s`)} · c) ${nw(`${sci('1{,}88', 6)} m/s`)}<br>D4·2: a) ${J(sci('3{,}2', -7))} · b) 4000 V/m · c) 4,0 m/s`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [2, 2], kq: [[1, 2], [3, 4]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'công A = qEd 1·4 · dấu của d 2·1 · không phụ thuộc đường đi 2·2 · thế năng 2·3 · thí nghiệm 3·1 · công và thế năng 3·2 · bẫy 3·4 · bài toán mẫu 4·3 · dạng 1–2 → 6·1 · dạng 3–4 → 7·1',
  out: process.argv[2],
});
