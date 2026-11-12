// Ruột tập VL12 – Bài 6 · Định luật Boyle. Định luật Charles (lesson id 7). Quyển Chương 2 lớp 12 (bài 5–8): bài 6 = tr. 13–24.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l12-bai6.mjs (toàn bộ SVG tự vẽ). Nội dung theo bài web (book/cache/7.json, tải từ DB 12/11/2026): mục tiêu, dự đoán
// bơm xe, II.1 thông số + kenvin, thí nghiệm xilanh (Boyle) + cột khí trong ống (Charles), đơn vị/cột thuỷ ngân, ba bẫy, Trả bài 5 câu,
// bài toán mẫu xilanh y tế, thử thách ⭐–⭐⭐⭐, 5 dạng bài tập mẫu. Đáp số Bài tương tự (tuongTu.dap) tính bằng Python 12/11/2026.
// Chạy: node scripts/ruot-tap/l12-bai6.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl12-bai6.pdf
//       node scripts/ruot-tap/l12-bai6.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l12-bai6/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL12b6 as H } from './hinh-l12-bai6.mjs';

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
  const out = resolve(HERE, 'out/hinh-l12-bai6'); mkdirSync(out, { recursive: true });
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


const K = khoiTao({ bai: 6, lid: 7, ten: 'ĐỊNH LUẬT BOYLE · ĐỊNH LUẬT CHARLES', lop: 12, baiDau: 5, sub: 'Vật lí 12 · Chương 2: Khí lí tưởng' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const p1 = m('p_1'), p2 = m('p_2'), V1 = m('V_1'), V2 = m('V_2'), T1 = m('T_1'), T2 = m('T_2'), p0 = m('p_0');
const u = (s, d) => nw(m(`${s}\\ \\mathrm{${d}}`));
const dC = (s) => nw(m(`${s}\\ ^\\circ\\mathrm C`));
const lit = (s) => nw(`${m(s)} lít`);
// Đổi đơn vị in sẵn (HS ảo L11 Ch.3: hằng số/đơn vị phải có trong tập trước khi hỏi)
const doiDV = `<b>Cho sẵn:</b> ${nw(m('1\\ \\mathrm{atm}=760\\ \\mathrm{mmHg}=1{,}013\\cdot10^5\\ \\mathrm{Pa}'))} · ${nw(m('1\\ \\mathrm{bar}=10^5\\ \\mathrm{Pa}'))} · ${nw(`1 lít ${m('=1\\ \\mathrm{dm^3}=10^3\\ \\mathrm{cm^3}')}`)} · ${nw(`${m('1\\ \\mathrm{ml}=1\\ \\mathrm{cm^3}')}`)} · ${nw(m('1\\ \\mathrm{m^3}=10^3'))} lít`;

const ttCss = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';

const p1t = `${ttCss}<section class="page">
${head('BÀI 6 · ĐỊNH LUẬT BOYLE · ĐỊNH LUẬT CHARLES', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Nêu ba <b>thông số trạng thái</b> của một lượng khí; thế nào là <b>đẳng quá trình</b>`)}
${dong(`${ck}Phát biểu, viết hệ thức định luật <b>Boyle</b>, <b>Charles</b>; đọc đường đẳng nhiệt, đẳng áp`)}
${dong(`${ck}Đổi nhiệt độ ra <b>kenvin</b>; đổi đơn vị áp suất, thể tích; tính áp suất khí bị cột thuỷ ngân giam`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Bịt đầu ra của bơm xe đạp. Ấn cán bơm <b>thật chậm</b> (nhiệt độ khí coi như không đổi) cho thể tích khí trong thân bơm giảm còn một nửa. Áp suất khí:</p>
<div class="fig-side" style="${fs(40)}"><div>
${opt('A', 'Giảm còn một nửa, vì khí bị dồn vào chỗ chật')}
${opt('B', 'Không đổi, vì lượng khí vẫn thế')}
${opt('C', 'Tăng gấp đôi')}
${opt('D', 'Tăng gấp bốn')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 1)}</div>
${H.bomXe()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(2)}</div>
${h3(4, 'II.1 · Thông số trạng thái · Nhiệt độ tuyệt đối', '1·4')}
<div class="card" style="padding:1.2mm 3mm">
<div>Ba thông số trạng thái của một lượng khí: ${f(22)}, ${f(22)}, ${f(22)}.</div>
<div>Khí chuyển từ trạng thái này sang trạng thái khác: một ${f(56)}.</div>
<div>Đẳng quá trình: quá trình có một thông số ${f(22)}.</div>
<div>Đẳng nhiệt giữ ${f(24)} · đẳng áp giữ ${f(24)} · đẳng tích giữ ${f(24)}</div>
<div>Nhiệt độ tuyệt đối: ${m('T=')} ${f(22)}; ${m('T')} đo bằng ${f(14)}, ${m('t')} đo bằng ${f(10)}</div>
<div class="hint" style="margin-top:.6mm">${doiDV}</div>
</div>
${h3(5, 'Làm nhanh', '1·5')}
${box(`<div class="two"><div class="yo"><span><b>a)</b> ${dC('27')} = ? K</span><span class="oo">${f(20)}</span></div><div class="yo"><span><b>b)</b> ${u('200', 'K')} = ? °C</span><span class="oo">${f(20)}</span></div></div><div class="yo"><span><b>c)</b> ${u('2{,}0', 'atm')} bằng bao nhiêu pascal?</span><span class="oo">${f(30)}</span></div>`)}
${foot(1)}</section>`;

const p2t = `<section class="page">
${head('II.2 · ĐỊNH LUẬT BOYLE · QUÁ TRÌNH ĐẲNG NHIỆT')}
${h3(1, 'Thí nghiệm: nén khí trong xilanh kín, đọc áp kế', '2·1')}
<div class="card" style="padding:1.2mm 3mm">
<div><b>Làm:</b> nhốt khí trong xilanh có áp kế, ấn pittông thật chậm, mỗi lần dừng lại đọc ${m('V')} và ${m('p')}.</div>
<table class="tbl-ct" style="margin:.8mm 0"><tr><th>Lần đo</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th></tr>
<tr><td>${m('V')} (ml)</td><td>8,0</td><td>6,0</td><td>5,0</td><td>4,0</td><td>3,0</td></tr>
<tr><td>${m('p')} (kPa)</td><td>100</td><td>142</td><td>170</td><td>215</td><td>267</td></tr>
<tr><td>${m('pV')} (kPa·ml)</td><td>800</td><td>852</td><td>850</td><td>860</td><td></td></tr></table>
<div><b>Quan sát:</b> ${m('V')} giảm thì ${m('p')} ${f(22)}; tích ${m('pV')} ${f(46)}</div>
<div class="hint">Số liệu minh hoạ.</div><div><b>Vì sao lệch tới 7,5 %?</b> (nêu 2 nguyên nhân)</div>${lines(2)}
</div>
${h3(2, 'Định luật Boyle', '2·2')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div>Đẳng nhiệt: ${f(28)} của khí không đổi.</div>
<div>Khối lượng khí và nhiệt độ không đổi thì áp suất ${f(40)} với thể tích.</div>
<div style="margin:1mm 0;min-height:11mm;display:flex;align-items:flex-end;gap:2mm">${m('pV=')} ${f(16)} &nbsp;⇒ <span class="fill" style="min-width:30mm;height:9mm"></span></div>
<div>${p1}, ${p2} cùng ${f(16)}; ${V1}, ${V2} cùng ${f(16)} (không bắt buộc SI).</div>
<div>Đường đẳng nhiệt trên đồ thị ${m('p')}–${m('V')}: một nhánh ${f(24)}.</div>
<div>Nhiệt độ càng cao, đường càng ${f(16)} gốc toạ độ ⇒ ${nw(`${m('T_{(1)}')} ${f(8)} ${m('T_{(2)}')}`)}</div></div>
${H.doThiPV()}</div>
${h3(3, 'Làm nhanh', '2·3')}
${box(cau(`<b>Câu 1.</b> Khí ở ${u('2{,}0', 'atm')}, ${lit('3{,}0')}. Nén đẳng nhiệt còn ${lit('1{,}5')}. Tính ${p2}.`, 2)
 + cau(`<b>Câu 2.</b> Một lượng khí biến đổi sao cho ${m('pV')} luôn không đổi. Đó là quá trình gì? Thông số nào đứng yên?`, 1)
 + cau(`<b>Câu 3.</b> Kéo pittông thật chậm cho thể tích khí tăng 3 lần (nhiệt độ không đổi). Áp suất thay đổi thế nào?`, 1))}
${foot(2)}</section>`;

const p3t = `<section class="page">
${head('II.3 · ĐỊNH LUẬT CHARLES · BA CÁI BẪY')}
${h3(1, 'Thí nghiệm: cột khí trong ống, áp suất không đổi', '3·1')}
<div class="card fig-side" style="${fs(40)};padding:1.2mm 3mm"><div>
<div><b>Giả thuyết:</b> ${m('p')} không đổi thì ${m('V')} tỉ lệ thuận với nhiệt độ tuyệt đối. Ống đều nên ${m('V')} tỉ lệ với ${m('\\ell')}.</div>
<table class="tbl-ct" style="margin:.8mm 0"><tr><th>${m('t')} (°C)</th><th>0</th><th>25</th><th>50</th><th>75</th></tr>
<tr><td>${m('T')} (K)</td><td>273</td><td>298</td><td>323</td><td></td></tr>
<tr><td>${m('\\ell')} (cm)</td><td>10,0</td><td>10,9</td><td>11,9</td><td>12,9</td></tr>
<tr><td>${m('\\ell/T')} (cm/K)</td><td>0,0366</td><td>0,0366</td><td>0,0368</td><td></td></tr></table>
<div><b>Rút ra:</b> ${m('\\ell/T')} ${f(40)} ⇒ ${nw(`${m('\\dfrac{V_1}{T_1}')} ${f(8)} ${m('\\dfrac{V_2}{T_2}')}`)}</div>
<div><b>Giới hạn:</b> chỉ đo từ 273 K tới 348 K. “Thí nghiệm chứng minh ${m('V=0')} khi ${m('T=0')} K”: ${ck}đúng ${ck}sai</div></div>
${H.ongCharles()}</div>
${h3(2, 'Định luật Charles', '3·2')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div>Đẳng áp: ${f(28)} của khí không đổi.</div>
<div>Khối lượng khí và áp suất không đổi thì thể tích ${f(36)} với ${f(50)}.</div>
<div style="margin:1mm 0;min-height:11mm;display:flex;align-items:flex-end;gap:2mm">${m('\\dfrac{V}{T}=')} ${f(16)} &nbsp;⇒ <span class="fill" style="min-width:30mm;height:10mm"></span></div>
<div>${m('T')} bắt buộc tính bằng ${f(16)}, không dùng °C.</div>
<div>Đường đẳng áp trên đồ thị ${m('V')}–${m('T')}: đường ${f(20)}, kéo dài đi qua ${f(14)}.</div>
<div>Áp suất càng nhỏ, đường càng ${f(14)} ⇒ ${nw(`${m('p_{(1)}')} ${f(8)} ${m('p_{(2)}')}`)}</div></div>
${H.doThiVT()}</div>
${h3(3, 'Làm nhanh', '3·3')}
${box(cau(`<b>Câu 4.</b> Nung đẳng áp ${lit('1{,}0')} khí từ ${dC('27')} lên ${dC('87')}. Tính ${V2}. Vì sao lấy ${m('\\tfrac{87}{27}')} là sai?`, 2)
 + `<div class="yo" style="padding-top:1mm"><span><b>Câu 5.</b> Nung đẳng áp từ ${dC('20')} lên ${dC('40')}: thể tích tăng mấy lần?</span><span class="oo">${f(24)}</span></div>`)}
${h3(4, 'III · Ba cái bẫy hay sập', '3·4')}
<div class="card" style="padding:1mm 3mm">
<div class="trap">${ck}<span><b>“Đẳng nhiệt thì thể tích không đổi.”</b> Đẳng nhiệt giữ ${m('T')}; ${m('p')} và ${m('V')} đều đổi.</span></div>
<div class="trap">${ck}<span><b>“Lấy tỉ số hai nhiệt độ °C.”</b> Đổi ra K rồi mới lập tỉ số; nóng lên thì ${m('V')} tăng.</span></div>
<div class="trap">${ck}<span><b>“Đọc nhầm hai đồ thị.”</b> Đọc tên hai trục trước khi đọc dạng đường.</span></div>
</div>
${foot(3)}</section>`;

const p4t = `<section class="page">
${head('KHÍ BỊ CỘT THUỶ NGÂN GIAM · TRẢ BÀI · TỰ KIỂM TRA')}
${h3(1, 'Mở rộng: áp suất khí bị cột thuỷ ngân giam', '4·1')}
<div class="card fig-side" style="${fs(42)};padding:1.2mm 3mm"><div>
<div>Cột thuỷ ngân cao ${m('h')} (mm) gây thêm áp suất ${m('h')} (${f(16)}). Lấy ${nw(m('p_0=760\\ \\mathrm{mmHg}'))}; ${m('h')} và ${p0} cùng đơn vị.</div>
<div>(a) miệng hướng lên: ${nw(`${m('p=')} ${f(20)}`)} · (b) miệng hướng xuống: ${nw(`${m('p=')} ${f(20)}`)}</div>
<div>Ống nằm ngang: ${nw(`${m('p=')} ${f(14)}`)} · tiết diện đều nên ${m('V\\sim\\ell')}: ${nw(`Boyle viết thành ${f(26)}`)}</div>
<div><b>Ví dụ:</b> miệng hướng lên, ${m('h=50\\ \\mathrm{mm}')}: ${nw(`${m('p=')} ${f(18)}`)} (không phải 710 mmHg).</div>
<div><b>Làm nhanh:</b> miệng hướng xuống, cột Hg ${u('15', 'cm')}: ${nw(`${m('p=')} ${f(20)}`)} · nằm ngang: ${nw(`${m('p=')} ${f(20)}`)}</div></div>
${H.haiOng()}</div>
${h3(2, 'IV · Trả bài 5 câu', '4·2')}
${box(`${tb('1. Ba thông số trạng thái? Thế nào là đẳng quá trình?')}${lines(2)}
${tb('2. Phát biểu định luật Boyle; hệ thức cho hai trạng thái.')}${lines(2)}
${tb('3. Phát biểu định luật Charles; vì sao bắt buộc dùng kenvin?')}${lines(2)}
${tb('4. Dạng đường đẳng nhiệt, đường đẳng áp trên đồ thị?')}${lines(2)}
${tb(`5. ${m('1\\ \\mathrm{atm}')} = ? Pa = ? mmHg. Ống hở phía trên, cột Hg 200 mm: ${m('p')} khí?`)}${lines(2)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/5 câu · chưa thuộc: ${f(25)} ${nw(`→ đọc lại ô ${f(12)} Tập`)}</div>
${h3(3, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '4·3')}
${rkHai([1, 2, 3, 4], [5, 6, 7, 8])}
${foot(4)}</section>`;

const p5t = `<section class="page">
${head('BÀI TOÁN MẪU · BÀI TẬP VỀ NHÀ · THỬ THÁCH')}
${h3(1, 'V · Bài toán mẫu: nén và nung khí trong xilanh y tế', '5·1')}
<div class="card soft fig-side" style="${fs(40)};padding:1.2mm 3mm"><div>Xilanh y tế nhốt ${u('60', 'ml')} không khí ở ${u('1{,}0\\cdot10^5', 'Pa')} và ${dC('27')}.<br><b>a)</b> Bịt đầu xilanh, ấn pittông từ từ (nhiệt độ không đổi) cho thể tích còn ${u('25', 'ml')}. Tính áp suất khí.<br><b>b)</b> Đưa pittông về ${u('60', 'ml')}, nung khí tới ${dC('87')}, áp suất giữ không đổi. Thể tích tăng thêm bao nhiêu ml?</div>${H.xilanh()}</div>
<table><tr><th style="width:52mm">Câu trong đề</th><th>Dữ liệu → định luật</th></tr>
<tr><td>“nhốt 60 ml … 27 °C”</td><td>${m('V_1=60\\ \\mathrm{ml}')}; ${m('T_1=300\\ \\mathrm K')} (đổi ngay)</td></tr>
<tr><td style="height:6.5mm">“ấn từ từ … nhiệt độ không đổi”</td><td></td></tr>
<tr><td style="height:6.5mm">“nung tới 87 °C … áp suất không đổi”</td><td></td></tr>
</table>
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm;margin-top:1mm">
${wl(`a) ${m('p_2=')}`, 2)}${wl(`b) ${m('T_2=')} ………… ⇒ ${m('V_2=')} ………………… ⇒ ${m('\\Delta V=')}`, 3)}</div>
${h3(2, 'Điền bước còn thiếu: câu a nhưng nén từ 60 ml xuống 15 ml', '5·2')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div class="ln"><b>Bước 1 (cho sẵn):</b> ${m('p_1V_1=6{,}0\\cdot10^6\\ \\mathrm{Pa{\\cdot}ml}')}</div>
${wl(`Bước 2: ${m('p_2=')}`, 1)}${wl('Bước 3: thể tích giảm …… lần nên áp suất', 1)}</div>
${K.btvn().replace('<i>1</i>', '<i>3</i>')}
${h3(4, 'Thử thách phân tầng', '5·4')}
${box(`<div class="yo" style="padding-top:1mm"><span>${m('\\bigstar')} Khí ở ${u('1{,}0\\cdot10^5', 'Pa')}, ${lit('6{,}0')} nén đẳng nhiệt còn ${lit('2{,}0')}: áp suất?</span><span class="oo">${f(28)}</span></div>`
 + cau(`${m('\\bigstar\\bigstar')} Giữ áp suất đó, nung ${lit('2{,}0')} khí từ ${u('300', 'K')} lên ${u('360', 'K')}: thể tích?`, 1)
 + cau(`${m('\\bigstar\\bigstar\\bigstar')} Bơm xe bằng tay vài chục lần: thân bơm nóng lên, cán nặng tay hơn mức Boyle dự đoán. Vì sao?`, 1))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Nén khí ở nhiệt độ không đổi (Boyle)',
    de: `Bơm xe bịt kín: ${u('240', 'cm^3')} khí ở ${u('1{,}0\\cdot10^5', 'Pa')}; ấn thật chậm (nhiệt độ không đổi) tới ${u('80', 'cm^3')}.<br><b>a)</b> áp suất khí lúc này<br><b>b)</b> ấn tiếp tới ${u('4{,}8\\cdot10^5', 'Pa')}: thể tích khí`,
    nd: `Bịt kín + ấn thật chậm ⇒ đẳng ${f(14)} ⇒ hệ thức ${f(26)}`, a: ['a', 'b'], gi: 3 },
  { t: 'Dạng 2 · Trung bình · Nung đẳng áp, đổi sang kenvin (Charles)',
    de: `Xilanh đứng, pittông nhẹ trượt không ma sát, phía trên thông khí trời; khí chiếm ${u('450', 'cm^3')} ở ${dC('17')}.<br><b>a)</b> nung khí tới ${dC('75')}: thể tích khí và phần thể tích tăng thêm<br><b>b)</b> làm lạnh đẳng áp cho thể tích còn ${u('360', 'cm^3')}: nhiệt độ khí (°C)`,
    nd: `Pittông tự do ⇒ ${f(14)} không đổi; đổi ${m('t')} ra ${f(10)} trước khi lập tỉ số`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b'], gi: 4 },
  { t: 'Dạng 3 · Trung bình · Đọc đồ thị V–T của cùng một lượng khí',
    de: `Hình bên: (1), (2) kéo dài qua ${m('O')}; tại ${u('300', 'K')}, A trên (1) có ${lit('V=4')}, B trên (2) có ${lit('V=6')}.<br><b>a)</b> mỗi đường là quá trình gì; đường nào áp suất lớn hơn<br><b>b)</b> tỉ số ${m('p_{(1)}/p_{(2)}')}<br><b>c)</b> khí ở (2) nung đến ${u('450', 'K')}: thể tích`,
    nd: `A, B cùng ${m('T')} ⇒ dùng ${f(16)}; cùng một đường ⇒ dùng ${f(16)}`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'], gi: 5, fig: H.vtD3('') },
  { t: 'Dạng 4 · Khó · Hai giai đoạn nối tiếp: đẳng nhiệt rồi đẳng áp',
    de: `Xilanh kín có pittông chứa ${lit('3{,}0')} khí ở ${u('1{,}0', 'atm')}, ${dC('27')}. Giai đoạn 1: đẩy pittông thật chậm (nhiệt độ không đổi) đến ${u('2{,}5', 'atm')}. Giai đoạn 2: giữ ${u('2{,}5', 'atm')}, nung khí tới ${dC('127')}.<br><b>a)</b> thể tích sau giai đoạn 1<br><b>b)</b> thể tích sau giai đoạn 2<br><b>c)</b> so với lúc đầu, thể tích cuối giảm bao nhiêu lít`,
    nd: `GĐ 1: ${f(16)}; GĐ 2: ${f(16)}; thể tích ${f(14)} của giai đoạn trước là thể tích đầu của giai đoạn sau`, a: ['a', 'b', 'c'], gi: 7 },
  { t: 'Dạng 5 · Nâng cao · Khí bị cột thuỷ ngân giam trong ống, lật ống',
    de: `Ống thuỷ tinh dài ${u('80', 'cm')}, tiết diện đều, một đầu kín. Đặt thẳng đứng, miệng hướng lên: cột thuỷ ngân cao ${u('20', 'cm')} giam ở đáy cột khí dài ${u('28', 'cm')}; ${nw(m('p_0=760\\ \\mathrm{mmHg}'))}. Lật nhẹ ống ${m('180^\\circ')} (miệng hướng xuống), Hg không chảy ra, nhiệt độ không đổi.<br><b>a)</b> áp suất khí khi miệng hướng lên (mmHg)<br><b>b)</b> áp suất khí sau khi lật<br><b>c)</b> chiều dài cột khí sau khi lật`,
    nd: `Đổi ${m('h')} ra ${f(10)}; miệng lên ${nw(`${m('p=')} ${f(14)}`)}, miệng xuống ${nw(`${m('p=')} ${f(14)}`)}; Boyle với ${m('\\ell')}`, a: ['a', 'b', 'c'], gi: 6, fig: H.latD5() },
];

// Bài tương tự: mỗi dạng 2 bài, giải vào vở (thầy chốt 10/11), ô đáp số cuối dòng của ý; đáp số tính bằng Python 12/11/2026.
const oY = (s, o, w = {}) => s.split('<br>').map((p) => {
  const y = p.match(/^<b>([a-d])\)<\/b>/);
  if (!y) return `<div>${p}</div>`;
  const ls = o.filter((l) => l[0] === y[1]);
  return `<div class="yo"><span>${p}</span><span class="oo">${ls.map((l) => `<span class="nw"><b>${l})</b>${f(typeof w === 'object' ? (w[l] ?? 25) : w)}</span>`).join('')}</span></div>`;
}).join('');
const ttDe = (b) => b.fig ? `<div class="fig-side" style="grid-template-columns:1fr ${b.fw}mm">${`<div>${oY(b.de, b.o, b.ow)}</div>`}${b.fig}</div>` : oY(b.de, b.o, b.ow);
const vaoVo = (ds) => ds.map((b) => (b.o ? { t: b.t, de: ttDe(b), k: 0 } : b));
const nhap = (n) => ({ t: '<span class="nhap-t">Nháp / chỗ em còn vướng</span>', de: lines(n), k: 0 });
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–3', 'DẠNG 4–5'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Một lượng khí ${lit('6{,}0')} ở ${u('1{,}5\\cdot10^5', 'Pa')} được nén đẳng nhiệt.<br><b>a)</b> thể tích còn ${lit('2{,}5')}: áp suất khí<br><b>b)</b> áp suất đạt ${u('4{,}5\\cdot10^5', 'Pa')}: thể tích khí`, o: ['a', 'b'], ow: { a: 30 } },
    { t: 'Dạng 1 · Bài 2', de: `Xilanh bịt kín chứa ${u('50', 'cm^3')} khí ở ${u('1{,}0\\cdot10^5', 'Pa')}. Kéo pittông thật chậm (nhiệt độ không đổi) cho thể tích thành ${u('125', 'cm^3')}.<br><b>a)</b> áp suất khí lúc này<br><b>b)</b> áp suất đã giảm bao nhiêu pascal`, o: ['a', 'b'], ow: 30 },
    { t: 'Dạng 2 · Bài 1', de: `Khí ${lit('2{,}0')} ở ${dC('27')} được nung đẳng áp tới ${dC('177')} ${nw(`(${m('T=t+273')})`)}.<br><b>a)</b> thể tích khí; phần thể tích tăng thêm<br><b>b)</b> từ trạng thái đầu, làm lạnh đẳng áp cho thể tích còn ${lit('1{,}6')}: nhiệt độ khí theo °C`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b'], ow: 20 },
    { t: 'Dạng 2 · Bài 2', de: `Xilanh pittông tự do chứa ${u('600', 'cm^3')} khí ở ${dC('7{,}0')}; áp suất không đổi.<br><b>a)</b> nung tới ${dC('63')}: thể tích; phần tăng thêm<br><b>b)</b> nung tới nhiệt độ nào (°C) thì thể tích là ${u('750', 'cm^3')}`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b'], ow: 20 },
    { t: 'Dạng 3 · Bài 1', de: `Hai đường (1), (2) của cùng một lượng khí trên hệ trục ${m('V')}–${m('T')}, mỗi đường kéo dài qua ${m('O')}. Tại ${u('400', 'K')}: đường (1) có ${lit('V=3{,}0')}, đường (2) có ${lit('V=5{,}0')}.<br><b>a)</b> đường nào ứng với áp suất lớn hơn<br><b>b)</b> tỉ số ${m('p_{(1)}/p_{(2)}')}<br><b>c)</b> khí ở đường (1) làm lạnh tới ${u('200', 'K')}: thể tích`, o: ['a', 'b', 'c'], ow: 22 },
    { t: 'Dạng 3 · Bài 2', de: `Trên đồ thị ${m('p')}–${m('V')}, đường đẳng nhiệt của một lượng khí đi qua điểm ${lit('V=2{,}0')}, ${u('p=6{,}0', 'atm')}.<br><b>a)</b> đường có dạng gì<br><b>b)</b> trên đường đó: ${m('p')} tại ${lit('V=3{,}0')}; ${m('V')} tại ${u('p=1{,}5', 'atm')}<br><b>c)</b> đường đẳng nhiệt khác nằm xa gốc hơn: nhiệt độ cao hơn hay thấp hơn`, o: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], ow: { a: 26, 'b<sub>1</sub>': 18, 'b<sub>2</sub>': 18, c: 26 } },
    nhap(3),
  ], [
    { t: 'Dạng 4 · Bài 1', de: `Xilanh kín chứa ${lit('4{,}0')} khí ở ${u('1{,}0', 'atm')}, ${dC('27')}. Giai đoạn 1: nén thật chậm (nhiệt độ không đổi) đến ${u('2{,}0', 'atm')}. Giai đoạn 2: giữ ${u('2{,}0', 'atm')}, nung tới ${dC('177')}.<br><b>a)</b> thể tích sau giai đoạn 1<br><b>b)</b> thể tích sau giai đoạn 2<br><b>c)</b> thể tích cuối giảm bao nhiêu lít so với lúc đầu`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 4 · Bài 2', de: `Xilanh chứa ${lit('6{,}0')} khí ở ${u('1{,}5', 'atm')}, ${dC('27')}. Giai đoạn 1: giữ ${u('1{,}5', 'atm')}, làm lạnh tới ${dC('-73')}. Giai đoạn 2: nén đẳng nhiệt cho thể tích còn ${lit('2{,}0')}.<br><b>a)</b> thể tích sau giai đoạn 1<br><b>b)</b> áp suất sau giai đoạn 2<br><b>c)</b> nhiệt độ cuối (°C)`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 5 · Bài 1', de: `Ống tiết diện đều dài ${u('80', 'cm')}, một đầu kín, thẳng đứng miệng hướng lên: cột Hg cao ${u('10', 'cm')} giam cột khí dài ${u('33', 'cm')}; ${nw(m('p_0=760\\ \\mathrm{mmHg}'))}. Lật ống cho miệng hướng xuống, Hg không chảy ra, nhiệt độ không đổi.<br><b>a)</b> áp suất khí trước khi lật (mmHg)<br><b>b)</b> áp suất khí sau khi lật<br><b>c)</b> chiều dài cột khí sau khi lật`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 5 · Bài 2', de: `Ống tiết diện đều, một đầu kín, đặt <b>nằm ngang</b>: cột Hg dài ${u('19', 'cm')} giam cột khí dài ${u('40', 'cm')}; ${nw(m('p_0=760\\ \\mathrm{mmHg}'))}. Dựng ống thẳng đứng, miệng hướng lên; nhiệt độ không đổi.<br><b>a)</b> áp suất khí khi ống nằm ngang<br><b>b)</b> áp suất khí khi miệng hướng lên<br><b>c)</b> chiều dài cột khí lúc đó`, o: ['a', 'b', 'c'] },
    nhap(11),
  ]],
  dap: [
    `D1·1: a) 3,6·10<sup>5</sup> Pa · b) 2,0 lít &nbsp;|&nbsp; D1·2: a) 4,0·10<sup>4</sup> Pa · b) 6,0·10<sup>4</sup> Pa &nbsp;|&nbsp; D2·1: a<sub>1</sub>) 3,0 lít · a<sub>2</sub>) 1,0 lít · b) −33 °C &nbsp;|&nbsp; D2·2: a<sub>1</sub>) 720 cm³ · a<sub>2</sub>) 120 cm³ · b) 77 °C &nbsp;|&nbsp; D3·1: a) đường (1) · b) 5/3 ≈ 1,7 · c) 1,5 lít &nbsp;|&nbsp; D3·2: a) hypebol · b<sub>1</sub>) 4,0 atm · b<sub>2</sub>) 8,0 lít · c) cao hơn`,
    `D4·1: a) 2,0 lít · b) 3,0 lít · c) 1,0 lít &nbsp;|&nbsp; D4·2: a) 4,0 lít · b) 3,0 atm · c) −73 °C &nbsp;|&nbsp; D5·1: a) 860 mmHg · b) 660 mmHg · c) 43 cm &nbsp;|&nbsp; D5·2: a) 760 mmHg · b) 950 mmHg · c) 32 cm`,
  ],
};

await K.dung({
  trang1to5: [p1t, p2t, p3t, p4t, p5t].join('\n'),
  btm: { dang, tach: [3, 2], kq: [[1, 2, 3], [4, 5]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'thông số, kenvin, đổi đơn vị 1·4 · Boyle 2·2 · đồ thị p–V 2·2 · Charles 3·2 · đồ thị V–T 3·2 · cột thuỷ ngân 4·1 · bẫy 4·2 · bài toán mẫu 5·1 · dạng 1–3 → 6·1 · dạng 4–5 → 7·1',
  out: process.argv[2],
});
