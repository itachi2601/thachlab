// Ruột tập VL11 – Bài 17 · Khái niệm điện trường (lesson id 36). Quyển Chương 3 lớp 11: bài 17 = tr. 13–24.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự (giải vào vở) · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l11-bai17.mjs (toàn bộ SVG tự vẽ, không dùng ảnh Halliday). Nội dung theo bài web (book/cache/36.json, tải từ DB 12/11/2026):
// mục tiêu, dự đoán thước nhựa, II.1–II.5, thí nghiệm cân điện tử + điện phổ, ba bẫy, Trả bài 5 câu, bài toán mẫu 3–4–5, thử thách, 5 dạng.
// Đáp số Bài tương tự (tuongTu.dap) và bảng thí nghiệm tính bằng Python 12/11/2026.
// Chạy: node scripts/ruot-tap/l11-bai17.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl11-bai17.pdf
//       node scripts/ruot-tap/l11-bai17.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l11-bai17/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai, dapSo } from './khung.mjs';
import { hinhL11b17 as H } from './hinh-l11-bai17.mjs';

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
  const out = resolve(HERE, 'out/hinh-l11-bai17'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 17, lid: 36, ten: 'KHÁI NIỆM ĐIỆN TRƯỜNG', lop: 11, baiDau: 16, sub: 'Vật lí 11 · Chương 3: Điện trường' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const vE = m('\\vec E'), vF = m('\\vec F'), eps = m('\\varepsilon');
const nC = (s) => nw(m(`${s}\\ \\mathrm{nC}`));
const cm = (s) => nw(m(`${s}\\ \\mathrm{cm}`));
const Vm = (s) => nw(m(`${s}\\ \\mathrm{V/m}`));
const kk = nw(m('k=9\\cdot10^{9}\\ \\mathrm{N\\cdot m^2/C^2}'));
const fh = (w) => `<span class="fill" style="min-width:${w}mm;height:10mm;vertical-align:-5mm"></span>`; // ô cao cho phân số (HS ảo: ≥9 mm)
const cung = (s) => ({ t: '<span class="nhap-t">Dùng cho cả trang</span>', de: s, k: 0 });
const ee = nw(m('e=1{,}6\\cdot10^{-19}\\ \\mathrm C'));

const p1 = `<section class="page">
${head('BÀI 17 · KHÁI NIỆM ĐIỆN TRƯỜNG', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Nêu được <b>điện trường</b> là gì · ${ck}Dùng ${m('\\vec E=\\vec F/q')}, ${m('E=k|Q|/(\\varepsilon r^2)')}, vẽ đúng chiều ${vE}`)}
${dong(`${ck}Nêu đặc điểm của <b>đường sức điện</b> · ${ck}Cộng vectơ ${vE} theo <b>nguyên lí chồng chất</b>`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Thước nhựa nhiễm điện hút được mẩu giấy ở cách vài centimét vì:</p>
<div class="fig-side" style="${fs(36)}"><div>
${opt('A', 'Thước làm không khí chuyển động, gió hút giấy lên')}
${opt('B', 'Lực hút chỉ có khi hai vật chạm nhau; giấy tự bay lên trước')}
${opt('C', 'Quanh thước có một “môi trường” đặc biệt, nó tác dụng lực lên giấy')}
${opt('D', 'Lực hấp dẫn giữa thước và giấy tăng lên khi cọ')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 1)}</div>
${H.thuocGiay()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Điện trường', '1·4')}
<div class="card" style="padding:1.2mm 3mm">
<div>Điện trường là dạng ${f(25)} tồn tại quanh ${f(25)}, do điện tích tạo ra và gắn liền với nó.</div>
<div>Nó truyền tương tác: ${m('Q')} không đẩy ${m('q')} trực tiếp, mà ${f(25)} của ${m('Q')} tác dụng lên ${m('q')}.</div>
<div><b>Tính chất cơ bản:</b> tác dụng ${f(25)} lên điện tích khác đặt trong nó.</div>
<div>Điện trường tĩnh: do các điện tích ${f(25)} gây ra. Dò điện trường: đặt vào đó một ${f(25)} (đủ nhỏ).</div></div>
${h3(5, 'II.2 · Cường độ điện trường', '1·5')}
<div class="card fig-side" style="${fs(40)};padding:1.2mm 3mm"><div>
<div>${vE} đặc trưng cho điện trường về phương diện ${f(20)} tại một điểm.</div>
<div style="margin:.6mm 0">${nw(`${m('\\vec E=')} ${fh(14)} &nbsp;⇒&nbsp; ${m('\\vec F=')} ${f(14)} &nbsp;·&nbsp; ${m('F=')} ${f(14)}`)}</div>
<div>Đơn vị: ${f(14)} = ${f(14)}</div>
<div>${nw(`${m('q>0')}: ${vF} ${f(16)} chiều ${vE}`)} · ${nw(`${m('q<0')}: ${vF} ${f(16)} chiều ${vE}`)}</div>
<div>${m('E')} ${ck}có &nbsp;${ck}không phụ thuộc điện tích thử ${m('q')}.</div></div>
${H.efDau()}</div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('ĐIỆN TÍCH ĐIỂM · ĐO E BẰNG CÂN · ĐƯỜNG SỨC')}
${h3(1, 'II.3 · Điện trường của một điện tích điểm', '2·1')}
<div class="card fig-side" style="${fs(44)};padding:1.2mm 3mm"><div>
<div><b>Điểm đặt:</b> ${f(30)}</div>
<div><b>Phương:</b> đường thẳng nối ${f(30)}</div>
<div><b>Chiều:</b> ${nw(`${m('Q>0')} ${f(25)}`)} · ${nw(`${m('Q<0')} ${f(25)}`)}</div>
<div style="margin:.6mm 0"><b>Độ lớn:</b> ${m('E=')} ${fh(26)} &nbsp; với ${kk} (cho sẵn)</div>
<div>${eps}: hằng số ${f(22)}; chân không, không khí ${nw(`${m('\\varepsilon\\approx')} ${f(10)}`)}; dầu, nước ${m('\\varepsilon>1')} nên ${m('E')} ${f(18)}</div>
<div><b>Mẹo:</b> ${m('r')} gấp đôi thì ${m('E')} ${f(25)}</div></div>
${H.quanhQ()}</div>
${h3(2, 'Thí nghiệm: cân điện tử “cân” lực điện', '2·2')}
<div class="fig-side" style="${fs(40)}"><div>
<div style="margin-bottom:.6mm">${m('Q=40\\ \\mathrm{nC}')} giữ phía trên ${m('q')}; ${nw(m('F=\\Delta m\\cdot g'))} (${m('\\Delta m')} đổi ra kg, ${nw(m('g\\approx9{,}8\\ \\mathrm{m/s^2}'))}), ${m('E=F/q')}.</div>
<table class="tbl-ct"><tr><th>Lần đo</th><th>${m('\\Delta m')} (g)</th><th>${m('E=F/q')} (V/m)</th></tr>
<tr><td>${m('r=3')} cm, ${m('q=10')} nC</td><td>0,41</td><td>${m('4{,}0\\cdot10^{5}')}</td></tr>
<tr><td>${m('r=4')} cm, ${m('q=10')} nC</td><td>0,23</td><td></td></tr>
<tr><td>${m('r=6')} cm, ${m('q=10')} nC</td><td>0,10</td><td></td></tr>
<tr><td>${m('r=4')} cm, ${m('q=5')} nC</td><td>0,12</td><td></td></tr></table>
</div>${H.canDien()}</div>
<div class="card" style="margin-top:.6mm;padding:1mm 3mm">
<div><b>Rút ra:</b> ${m('r')} gấp đôi (3 → 6 cm), ${m('E')} giảm khoảng ${f(12)} lần. Ở 4 cm, ${m('q')} giảm một nửa thì ${m('F')} ${f(30)}, ${m('E')} ${f(30)}.</div></div>
${h3(3, 'II.4 · Đường sức điện', '2·3')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div><b>Tiếp:</b> tiếp tuyến tại mỗi điểm là ${f(16)} của ${vE}; hướng đường sức là hướng của vectơ ${f(12)}.</div>
<div>Qua mỗi điểm vẽ được ${f(16)} đường sức; các đường sức ${f(16)} cắt nhau.</div>
<div><b>Ra – Vào:</b> đi ra từ điện tích ${f(16)}, kết thúc ở điện tích ${f(16)} (hoặc vô cực), nên ${ck}có &nbsp;${ck}không khép kín.</div>
<div><b>Độ lớn E:</b> chỗ ${m('E')} lớn đường sức ${f(16)}, chỗ ${m('E')} nhỏ đường sức ${f(16)}.</div>
<div><b>Điện phổ:</b> bột hạt cách điện rắc trong dầu, đặt trong điện trường, xếp thành ${f(22)} dọc theo đường sức.</div></div>
${H.duongSuc()}</div>
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('CHỒNG CHẤT ĐIỆN TRƯỜNG · BẪY · TRẢ BÀI')}
${h3(1, 'II.5 · Nguyên lí chồng chất điện trường', '3·1')}
<div class="card fig-side" style="${fs(42)};padding:1.2mm 3mm"><div>
<div>Các điện tích ${m('q_1,q_2,\\dots')} gây ra tại M các vectơ ${m('\\vec E_1,\\vec E_2,\\dots')}: ${nw(`${m('\\vec E=')} ${f(28)}`)}</div>
<div>Hai vectơ: cộng theo quy tắc ${f(28)}.</div>
<table style="margin-top:.6mm"><tr><th>Hai vectơ</th><th style="width:12mm">Góc</th><th>Độ lớn ${m('E')}</th></tr>
<tr><td>Cùng chiều</td><td>${m('0^\\circ')}</td><td></td></tr>
<tr><td>Ngược chiều</td><td>${m('180^\\circ')}</td><td></td></tr>
<tr><td>Vuông góc</td><td>${m('90^\\circ')}</td><td></td></tr>
<tr><td>Góc bất kì</td><td>${m('\\alpha')}</td><td>${m('E^2=')}</td></tr>
<tr><td style="height:9mm">${m('E_1=E_2')}</td><td>${m('\\alpha')}</td><td>${m('E=')}</td></tr></table></div>
${H.hbh()}</div>
${h3(2, 'III · Ba cái bẫy hay sập', '3·2')}
<div class="card" style="padding:1mm 3mm">
<div class="trap">${ck}<span><b>“${m('E=F/q')} nên ${m('q')} càng lớn thì ${m('E')} càng nhỏ.”</b> ${m('E=F/q')} là cách <i>đo</i>; ${m('E')} do ${m('Q')} nguồn và vị trí quyết định, có sẵn cả khi chưa đặt ${m('q')}.</span></div>
<div class="trap">${ck}<span><b>“Cộng độ lớn, lấy dấu ${m('Q')} để cộng trừ.”</b> Dấu của ${m('Q')} chỉ để chọn chiều ${vE}; cộng <b>vectơ</b>, vẽ trước tính sau.</span></div>
<div class="trap">${ck}<span><b>“Đường sức là đường điện tích chạy theo.”</b> Đường sức chỉ cho hướng lực; có vận tốc ban đầu thì quỹ đạo thường lệch khỏi đường sức.</span></div></div>
${h3(3, 'IV · Trả bài 5 câu', '3·3')}
${box(`${tb('1. Điện trường là gì? Tính chất cơ bản của nó?')}${lines(2)}
${tb(`2. Công thức định nghĩa ${m('\\vec E')}, đơn vị. Khi nào ${m('\\vec F')} ngược chiều ${m('\\vec E')}?`)}${lines(2)}
${tb(`3. Điểm đặt, phương, chiều, độ lớn của ${m('\\vec E')} do điện tích điểm ${m('Q')} gây ra.`)}${lines(2)}
${tb('4. Kể bốn đặc điểm của đường sức điện.')}${lines(2)}
${tb('5. Nguyên lí chồng chất. Hai vectơ vuông góc thì tính E thế nào?')}${lines(1)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/5 câu · chưa thuộc: ${f(25)} ${nw(`→ đọc lại ô ${f(12)} Tập`)}</div>
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('TỰ KIỂM TRA · BÀI TOÁN MẪU')}
${h3(1, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '4·1')}
${rkHai([1, 2, 3], [4, 5, 6])}
${h3(2, 'V · Bài toán mẫu: hai điện tích và một góc vuông ẩn', '4·2')}
<div class="card soft" style="padding:1.2mm 3mm">Trong không khí, đặt ${m('q_1=+12\\ \\mathrm{nC}')} tại A và ${m('q_2=-16\\ \\mathrm{nC}')} tại B, ${m('AB=5\\ \\mathrm{cm}')}. Điểm M cách A ${cm(3)}, cách B ${cm(4)}. Cho ${kk}, ${ee}.
<div><b>a)</b> ${m('E_1')}, ${m('E_2')} do mỗi điện tích gây ra tại M &nbsp;<b>b)</b> ${m('E')} tổng hợp tại M &nbsp;<b>c)</b> lực lên electron đặt tại M, hướng</div></div>
${h3(3, 'Phân tích đề')}
<table><tr><th style="width:44mm">Câu trong đề</th><th>Dữ liệu → kiến thức</th></tr>
<tr><td>“Trong không khí”</td><td>${m('\\varepsilon=1')} → ${m('E=k|Q|/r^2')}</td></tr>
<tr><td style="height:6.5mm">“${m('q_1=+12')} nC tại A”</td><td></td></tr>
<tr><td style="height:6.5mm">“${m('q_2=-16')} nC tại B”</td><td></td></tr>
<tr><td style="height:6.5mm">“AB = 5 cm”, “3 cm”, “4 cm”</td><td></td></tr>
<tr><td style="height:6.5mm">“electron tại M”</td><td></td></tr></table>
${h3(4, 'Giải')}
<div class="fig-side" style="${fs(48)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl(`a) ${m('E_1')}, chiều:`, 2)}${wl(`${m('E_2')}, chiều:`, 2)}${wl(`b) Góc giữa ${m('\\vec E_1')}, ${m('\\vec E_2')}; ${m('E')}:`, 3)}${wl('c) F, hướng:', 2)}${wl('Kiểm tra: E nằm giữa hai số nào?', 2)}</div>${H.tamGiac345()}</div>
${h3(5, 'Điền bước còn thiếu: cùng đề, đổi dấu ${q2}'.replace('${q2}', m('q_2=+16\\ \\mathrm{nC}')))}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div class="ln"><b>Bước 1 (cho sẵn):</b> ${nw(m('E_1=1{,}2\\cdot10^5\\ \\mathrm{V/m}'))} ra xa A; ${nw(m('E_2=9\\cdot10^4\\ \\mathrm{V/m}'))}</div>
${wl(`Bước 2: chiều mới của ${m('\\vec E_2')}; góc với ${m('\\vec E_1')} còn ${m('90^\\circ')}?`, 1)}${wl(`Bước 3: ${m('E=')}`, 1)}</div>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TẬP VỀ NHÀ · THỬ THÁCH · MANG VỀ')}
${K.btvn()}
${h3(2, 'Thử thách phân tầng', '5·2')}
<div class="fig-side" style="${fs(38)}">${box(wl(`${m('\\bigstar')} ${m('Q=+2\\ \\mathrm{nC}')} trong không khí, ${kk}. Tính ${m('E')} tại điểm cách nó ${cm(3)} và lực lên ${m('q=-1\\ \\mathrm{nC}')} đặt ở đó (độ lớn, hướng).`, 4)
 + wl(`${m('\\bigstar\\bigstar')} ${m('q_1=+4\\ \\mathrm{nC}')} tại A, ${m('q_2=+1\\ \\mathrm{nC}')} tại B, ${m('AB=9\\ \\mathrm{cm}')}. Tìm điểm có điện trường tổng hợp bằng 0.`, 4)
 + wl(`${m('\\bigstar\\bigstar\\bigstar')} Ba điện tích ${m('+q')} bằng nhau ở ba đỉnh tam giác đều. ${m('E')} ở tâm bằng bao nhiêu? Lập luận, không cần tính số.`, 4))}${H.tamGiacDeu()}</div>
${h3(3, 'Câu đổi vị trí (bài toán mẫu)', '5·3')}
${box(wl(`Vẫn ${m('q_1=+12\\ \\mathrm{nC}')} tại A, ${m('q_2=-16\\ \\mathrm{nC}')} tại B, nhưng ${m('AB=6\\ \\mathrm{cm}')} và M là trung điểm AB. Vẽ hai vectơ tại M rồi tính ${m('E')} (${m('k')} như trên). Vì sao không dùng ${m('\\sqrt{E_1^2+E_2^2}')} như bài mẫu?`, 4))}
${h3(4, 'VI · Mang về: điều em dễ quên nhất', '5·4')}
${box(wl('1.', 3) + wl('2.', 3) + wl('3.', 3))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Từ lực trên điện tích thử tìm E, rồi đổi điện tích thử',
    de: `Tại M, điện tích thử ${m('q_1=-4\\ \\mathrm{nC}')} chịu lực điện ${m('6\\cdot10^{-4}\\ \\mathrm N')} hướng về phía bắc.<br><b>a)</b> độ lớn và hướng của ${vE} tại M<br><b>b)</b> bỏ ${m('q_1')}, đặt vào M ${m('q_2=+2\\ \\mathrm{nC}')}: lực lên ${m('q_2')} và hướng`,
    nd: `${m('E=F/|q|')}; ${m('q<0')} thì ${vF} ${f(14)} chiều ${vE}; đổi điện tích thử thì ${vE} tại M ${f(16)}`, a: ['a', 'b'], gi: 3, cot: 2, fig: H.d1() },
  { t: 'Dạng 2 · Dễ · E của điện tích điểm, lực lên điện tích thử',
    de: `Điện tích điểm ${m('Q=-6\\ \\mathrm{nC}')} đặt cố định trong không khí; M cách Q ${cm(3)}; ${kk}.<br><b>a)</b> ${m('E')} tại M và hướng<br><b>b)</b> đặt tại M ${m('q=+2\\ \\mathrm{nC}')}: lực lên ${m('q')} và hướng`,
    nd: `thế ${m('|Q|')}, ${m('r')} đổi ra ${f(10)}; dấu của ${m('Q')} chỉ để chọn ${f(16)}`, a: ['a', 'b'], gi: 4, cot: 2, fig: H.d2() },
  { t: 'Dạng 3 · Trung bình · Điện môi, tỉ lệ theo khoảng cách',
    de: `${m('Q=+8\\ \\mathrm{nC}')} đặt trong dầu ${m('\\varepsilon=2')}. M cách Q ${cm(4)}; N trên tia QM, cách Q ${cm(12)}; ${m('k')} như Dạng 2.<br><b>a)</b> ${m('E_M')} &nbsp;<b>b)</b> ${m('E_N')} &nbsp;<b>c)</b> P trên tia QM có ${m('E_P=900\\ \\mathrm{V/m}')}: khoảng cách PQ`,
    nd: `cùng ${m('Q')}, cùng môi trường: ${m('r')} gấp ${m('n')} lần thì ${m('E')} giảm ${f(12)} lần`, a: ['a', 'b', 'c'], gi: 5, fig: H.d3() },
  { t: 'Dạng 4 · Trung bình · Chồng chất hai vectơ cùng phương',
    de: `Trong không khí, ${m('q_1=+9\\ \\mathrm{nC}')} tại A, ${m('q_2=-4\\ \\mathrm{nC}')} tại B, ${m('AB=4\\ \\mathrm{cm}')}; ${kk}.<br><b>a)</b> M trên đường AB, ngoài đoạn AB, phía B, cách B ${cm(2)}: ${m('E')} tổng hợp tại M và hướng<br><b>b)</b> ${m('E')} tổng hợp tại trung điểm I của AB`,
    nd: `${m('r_i')} đo từ chính điện tích đó; cùng chiều thì ${m('E=')} ${f(16)}, ngược chiều thì ${m('E=')} ${f(16)}`, a: ['a', 'b'], gi: 7, fig: H.d4(), cot: 2 },
  { t: 'Dạng 5 · Khó · Hai điện tích bằng nhau, điểm trên trung trực',
    de: `Trong không khí, hai quả cầu nhỏ cùng điện tích ${m('Q=+5\\ \\mathrm{nC}')} giữ cố định tại A và B, ${m('AB=8\\ \\mathrm{cm}')}. M trên trung trực của AB, cách trung điểm H một đoạn ${cm(3)}; ${m('k')} như Dạng 4.<br><b>a)</b> ${m('E')} tổng hợp tại M và hướng<br><b>b)</b> đặt tại M quả cầu ${m('q=-2\\ \\mathrm{nC}')}: lực lên nó và hướng<br><b>c)</b> nếu ${m('q')} nằm đúng ở H: lực điện tổng hợp`,
    nd: `${m('MA=')} ${f(14)}, không phải ${m('MH')} hay ${m('AB')}; ${nw(m('E=2E_1\\cos\\dfrac{\\alpha}{2}'))} với ${nw(`${m('\\cos\\dfrac{\\alpha}{2}=')} ${fh(12)}`)}`, a: ['a', 'b', 'c'], gi: 9, fig: H.d5(), cot: 3 },
];

// Bài tương tự: mỗi dạng 2 bài, đáp số tính bằng Python 12/11/2026 (k = 9e9, e = 1,6e-19 C), làm tròn 3 chữ số có nghĩa.
// Giải vào vở (thầy chốt 10/11): 1 cột; ô đáp số 25 mm (40 mm khi ý có độ lớn + hướng) đặt cuối đúng dòng của ý.
const ttHaiCot = '<style>.bt>.gi{display:grid;grid-template-columns:1fr 1fr;column-gap:4mm}.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm}.yo .oo{flex:none;display:flex;gap:3mm}.yo{line-height:1.35}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';
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
    cung(`${kk}; ${ee}; không khí ${m('\\varepsilon\\approx1')}.`),
    { t: 'Dạng 1 · Bài 1', de: `Tại M, điện tích thử ${m('q_1=+5\\ \\mathrm{nC}')} chịu lực điện ${m('1{,}0\\cdot10^{-3}\\ \\mathrm N')} hướng về phía đông.<br><b>a)</b> ${m('E')} tại M (độ lớn, hướng)<br><b>b)</b> thay bằng ${m('q_2=-3\\ \\mathrm{nC}')} tại M: lực lên ${m('q_2')} (độ lớn, hướng)`, o: ['a', 'b'], ow: 60 },
    { t: 'Dạng 1 · Bài 2', de: `Electron (${ee}) đặt tại M chịu lực điện ${m('3{,}2\\cdot10^{-15}\\ \\mathrm N')} hướng thẳng lên.<br><b>a)</b> ${m('E')} tại M (độ lớn, hướng)<br><b>b)</b> thay bằng proton (${m('q=+e')}) tại M: lực lên proton (độ lớn, hướng)`, o: ['a', 'b'], ow: 60 },
    { t: 'Dạng 2 · Bài 1', de: `${m('Q=+4\\ \\mathrm{nC}')} đặt trong không khí; M cách Q ${cm(6)}; ${kk}.<br><b>a)</b> ${m('E')} tại M (độ lớn, hướng)<br><b>b)</b> lực lên ${m('q=-3\\ \\mathrm{nC}')} đặt tại M (độ lớn, hướng)`, o: ['a', 'b'], ow: 60 },
    { t: 'Dạng 2 · Bài 2', de: `${m('Q=-2{,}5\\ \\mathrm{nC}')} đặt trong không khí; M cách Q ${cm(5)}.<br><b>a)</b> ${m('E')} tại M (độ lớn, hướng)<br><b>b)</b> lực lên electron đặt tại M (độ lớn, hướng)`, o: ['a', 'b'], ow: 60 },
    { t: 'Dạng 3 · Bài 1', de: `${m('Q=+6\\ \\mathrm{nC}')} đặt trong dầu ${m('\\varepsilon=3')}; M cách Q ${cm(3)}, N trên tia QM cách Q ${cm(6)}.<br><b>a)</b> ${m('E_M')}<br><b>b)</b> ${m('E_N')}<br><b>c)</b> P trên tia QM có ${m('E_P=800\\ \\mathrm{V/m}')}: khoảng cách PQ`, fig: H.ttD3(), fw: 44, o: ['a', 'b', 'c'] },
    { t: 'Dạng 3 · Bài 2', de: `${m('Q=+10\\ \\mathrm{nC}')} đặt trong dầu ${m('\\varepsilon=2{,}5')}; M cách Q ${cm(6)}.<br><b>a)</b> ${m('E_M')} trong dầu<br><b>b)</b> ${m('E')} tại M nếu bỏ dầu (không khí)<br><b>c)</b> trong dầu, ${m('E')} tại N cách Q ${cm(2)}`, o: ['a', 'b', 'c'] },
  ], [
    cung(`${kk}; không khí ${m('\\varepsilon\\approx1')}; electron ${m('q=-1{,}6\\cdot10^{-19}\\ \\mathrm C')}.`),
    { t: 'Dạng 4 · Bài 1', de: `Trong không khí, ${m('q_1=+4\\ \\mathrm{nC}')} tại A, ${m('q_2=-4\\ \\mathrm{nC}')} tại B, ${m('AB=6\\ \\mathrm{cm}')}.<br><b>a)</b> ${m('E')} tổng hợp tại trung điểm I (độ lớn, hướng)<br><b>b)</b> M trên đường AB, ngoài đoạn AB, phía B, cách B ${cm(3)}: ${m('E')} tổng hợp (độ lớn, hướng)`, o: ['a', 'b'], ow: 60 },
    { t: 'Dạng 4 · Bài 2', de: `Trong không khí, ${m('q_1=+16\\ \\mathrm{nC}')} tại A, ${m('q_2=+4\\ \\mathrm{nC}')} tại B, ${m('AB=6\\ \\mathrm{cm}')}.<br><b>a)</b> ${m('E')} tổng hợp tại trung điểm I (độ lớn, hướng)<br><b>b)</b> điểm có ${m('E=0')}: cách A bao nhiêu, cách B bao nhiêu`, o: ['a', 'b'], ow: 60 },
    { t: 'Dạng 5 · Bài 1', de: `Trong không khí, hai điện tích ${m('Q=+4\\ \\mathrm{nC}')} tại A và B, ${m('AB=6\\ \\mathrm{cm}')}; M trên trung trực của AB, cách trung điểm H ${cm(4)}.<br><b>a)</b> ${m('E')} tổng hợp tại M (độ lớn, hướng)<br><b>b)</b> lực lên ${m('q=+3\\ \\mathrm{nC}')} đặt tại M<br><b>c)</b> ${m('E')} tại H`, o: ['a', 'b', 'c'], ow: 60 },
    { t: 'Dạng 5 · Bài 2', de: `Trong không khí, ${m('q_1=+6\\ \\mathrm{nC}')} tại A, ${m('q_2=-6\\ \\mathrm{nC}')} tại B, ${m('AB=6\\ \\mathrm{cm}')}; M trên trung trực của AB, cách trung điểm H ${cm(4)}.<br><b>a)</b> ${m('E')} tổng hợp tại M (độ lớn, hướng)<br><b>b)</b> lực lên electron đặt tại M (độ lớn, hướng)<br><b>c)</b> ${m('E')} tại H (độ lớn, hướng)`, fig: H.ttD5(), fw: 40, o: ['a', 'b', 'c'], ow: 60 },
    nhap(5),
  ]],
  dap: [
    `D1·1: a) 2,0·10<sup>5</sup> V/m, hướng đông · b) 6,0·10<sup>−4</sup> N, hướng tây &nbsp;|&nbsp; D1·2: a) 2,0·10<sup>4</sup> V/m, hướng xuống · b) 3,2·10<sup>−15</sup> N, hướng xuống &nbsp;|&nbsp; D2·1: a) 1,0·10<sup>4</sup> V/m, ra xa Q · b) 3,0·10<sup>−5</sup> N, về phía Q &nbsp;|&nbsp; D2·2: a) 9,0·10<sup>3</sup> V/m, về phía Q · b) 1,4·10<sup>−15</sup> N, ra xa Q &nbsp;|&nbsp; D3·1: a) 2,0·10<sup>4</sup> V/m · b) 5,0·10<sup>3</sup> V/m · c) 15 cm &nbsp;|&nbsp; D3·2: a) 1,0·10<sup>4</sup> V/m · b) 2,5·10<sup>4</sup> V/m · c) 9,0·10<sup>4</sup> V/m`,
    `D4·1: a) 8,0·10<sup>4</sup> V/m, hướng về B · b) 3,6·10<sup>4</sup> V/m, hướng về B &nbsp;|&nbsp; D4·2: a) 1,2·10<sup>5</sup> V/m, hướng về B · b) giữa A và B, cách A 4 cm, cách B 2 cm &nbsp;|&nbsp; D5·1: a) 2,3·10<sup>4</sup> V/m, theo HM ra xa AB · b) 6,9·10<sup>−5</sup> N, cùng hướng E · c) 0 &nbsp;|&nbsp; D5·2: a) 2,6·10<sup>4</sup> V/m, song song AB, chiều A → B · b) 4,1·10<sup>−15</sup> N, chiều B → A · c) 1,2·10<sup>5</sup> V/m, hướng về B`,
  ],
};

await K.dung({
  trang1to5: ttHaiCot + [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 2], kq: [[1, 2, 3], [4, 5]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'điện trường 1·4 · cường độ 1·5 · điện tích điểm 2·1 · cân điện tử 2·2 · đường sức 2·3 · chồng chất 3·1 · bẫy 3·2 · bài toán mẫu 4·2 · dạng 1–3 → 6·1 · dạng 4–5 → 7·1',
  out: process.argv[2],
});
