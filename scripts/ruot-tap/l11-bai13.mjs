// Ruột tập VL11 – Bài 13 · Sóng dừng (lesson id 32). Quyển Chương 2 lớp 11: bài 8 = tr. 1–12 … bài 13 = tr. 61–72.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự giải vào vở · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l11-bai13.mjs (toàn bộ SVG tự vẽ). Nội dung theo bài web (book/cache/32.json, tải từ DB 13/11/2026):
// mục tiêu, dự đoán bấm phím đàn, II.1–II.6, thí nghiệm dây thun + máy rung l = 0,80 m + đổi đầu tự do, ba bẫy, Trả bài 5 câu,
// bài toán mẫu dây 1,0 m, thử thách phân tầng, 6 dạng bài tập mẫu. Đáp số Bài tập mẫu + Bài tương tự tính bằng Python 13/11/2026.
// Chạy: node scripts/ruot-tap/l11-bai13.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl11-bai13.pdf
//       node scripts/ruot-tap/l11-bai13.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l11-bai13/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL11b13 as H } from './hinh-l11-bai13.mjs';

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
  const out = resolve(HERE, 'out/hinh-l11-bai13'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 13, lid: 32, ten: 'SÓNG DỪNG', lop: 11, baiDau: 8, sub: 'Vật lí 11 · Chương 2: Sóng' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const L = m('\\lambda'), l = m('l'), v = m('v'), k = m('k'), fz = m('f'), f0 = m('f_0');
const u = (s, dv) => nw(`${m(s)} ${dv}`); // số + đơn vị không gãy dòng

// Ô đáp số Bài tập mẫu cao 9,5 mm (phân số viết tay cần ≥ 9 mm — checklist HS ảo); Bài tương tự 1 cột, ô cuối dòng của ý.
const css = '<style>.bt .ans .fill{height:9.5mm}.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:5mm}.tt:has(.nhap-t) .hd>span+span{display:none}.tb2 td{height:6.5mm}</style>';

const p1 = `${css}<section class="page">
${head('BÀI 13 · SÓNG DỪNG', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Giải thích chỗ đứng yên trên dây; chỉ đúng nút, bụng và khoảng cách giữa chúng`)}
${dong(`${ck}Viết điều kiện có sóng dừng cho dây hai đầu cố định và dây một đầu tự do`)}
${dong(`${ck}Từ chiều dài dây, số nút, tần số: tính ${L} và ${v}`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Bấm phím cho đoạn dây đàn rung ngắn lại, giữ nguyên sức căng. Tần số âm phát ra sẽ:</p>
<div class="fig-side" style="${fs(42)}"><div>
${opt('A', 'Thấp hơn, vì dây ngắn dao động chậm hơn')}
${opt('B', 'Không đổi, vì vẫn là sợi dây đó')}
${opt('C', 'Cao hơn, vì đoạn dây ngắn thì tần số lớn hơn')}
${opt('D', 'Không đổi, vì tai không phân biệt được')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 1)}</div>
${H.danBam()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f(12)} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Sóng phản xạ', '1·4')}
<div class="card fig-side" style="${fs(44)};padding:1.2mm 3mm"><div>
<div>Đầu dây <b>cố định</b> (buộc chặt): sóng phản xạ ${f(14)} pha với sóng tới.</div>
<div>Đầu dây <b>tự do</b> (vòng nhẹ trượt trên cọc): sóng phản xạ ${f(14)} pha.</div>
<div>Sóng phản xạ cùng ${f(20)}, cùng ${f(20)} với sóng tới.</div>
<div><b>Sóng dừng</b>: sóng tổng hợp của hai sóng cùng biên độ, cùng bước sóng, truyền ${f(25)}.</div></div>
${H.phanXa()}</div>
${h3(5, 'II.2 · Nút sóng và bụng sóng', '1·5')}
<div class="card" style="padding:1.2mm 3mm">
<div>Nút: hai sóng thành phần ${f(25)} pha ${m('\\to')} không dao động, biên độ ${f(12)}.</div>
<div>Bụng: hai sóng thành phần ${f(25)} pha ${m('\\to')} dao động mạnh nhất, biên độ ${f(12)} (${m('A')}: biên độ sóng tới).</div>
<div>Đầu cố định luôn là ${f(25)}; đầu tự do luôn là ${f(25)}.</div>
<div>Hai nút (hai bụng) liên tiếp cách nhau ${f(12)}; một nút và một bụng liền kề cách nhau ${f(12)}.</div></div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('BÓ SÓNG · ĐIỀU KIỆN CÓ SÓNG DỪNG')}
${h3(1, 'Thí nghiệm: sợi dây thun rung bằng tay', '2·1')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div><b>Làm:</b> buộc một đầu dây thun vào chân ghế, tay trái giữ căng đầu kia, tay phải vung đầu dây lên xuống đều.</div>
<div><b>Quan sát:</b> dây chia thành những múi; có chỗ đứng yên hẳn. Vung nhanh hơn thì số múi ${ck}tăng ${ck}giảm.</div>
<div><b>Rút ra:</b> chỗ đứng yên là ${f(25)}, chỗ vồng mạnh nhất là ${f(25)}.</div>
<div>Mỗi múi giữa hai nút liên tiếp là một ${f(25)}, dài ${f(12)}.</div></div>
${H.dayThun()}</div>
${h3(2, 'II.3 · Điều kiện để có sóng dừng', '2·2')}
<div class="card fig-side" style="${fs(44)};padding:1.2mm 3mm"><div>
<table class="tb2"><tr><th style="width:20mm"></th><th>Hai đầu cố định</th><th>Một đầu cố định, một đầu tự do</th></tr>
<tr><th>${l} =</th><td></td><td></td></tr>
<tr><th>${k} chạy từ</th><td></td><td></td></tr>
<tr><th>${fz} =</th><td></td><td></td></tr>
<tr><th>${f0} =</th><td></td><td></td></tr>
<tr><th>Số bụng</th><td></td><td></td></tr>
<tr><th>Số nút</th><td></td><td></td></tr></table>
<div style="margin-top:.8mm"><b>Mẹo nhớ:</b> Cố Định: Nút – ${f(14)} – ${f(14)} · Tự Do: Bụng – ${f(14)} – ${f(14)}</div></div>
${H.haiTH()}</div>
${h3(3, 'Làm nhanh', '2·3')}
${box(cau(`<b>Câu 1.</b> Dây dài ${u('1{,}5', 'm')}, hai đầu cố định, có sóng dừng với 5 bó. Tính bước sóng.`, 2)
 + cau(`<b>Câu 2.</b> Dây dài ${u('0{,}4', 'm')}, một đầu cố định, một đầu tự do, ${u('v=8', 'm/s')}. Tần số nhỏ nhất để có sóng dừng?`, 3)
 + cau(`<b>Câu 3.</b> Dây hai đầu cố định có sóng dừng với 4 bó. Có bao nhiêu bụng, bao nhiêu nút (kể cả hai đầu)?`, 2))}
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('ĐO BƯỚC SÓNG · ĐẦU TỰ DO · BIÊN ĐỘ · BẪY')}
${h3(1, 'II.4 · Đo bước sóng và tốc độ truyền sóng', '3·1')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div>Hai đầu cố định, ${k} bó: ${nw(`${m('\\lambda=')} ${f(12)}`)} · ${nw(`${m('v=')} ${f(12)}`)}</div>
<div><b>Làm:</b> dây ${u('l=0{,}80', 'm')}; tăng dần ${fz} tới khi dây rung rõ nét, đếm ${k}.</div>
<table style="margin:.8mm 0"><tr><th>Số bó ${k}</th><td>2</td><td>3</td><td>4</td><td>5</td></tr>
<tr><th>${fz} (Hz)</th><td>24,9</td><td>37,4</td><td>50,2</td><td>62,3</td></tr>
<tr><th style="height:6.5mm">${L} (m)</th><td></td><td></td><td></td><td></td></tr>
<tr><th style="height:6.5mm">${v} (m/s)</th><td></td><td></td><td></td><td></td></tr></table>
<div><b>Rút ra:</b> đổi ${fz} thì ${v} ${ck}đổi ${ck}không đổi; ${v} do ${f(25)} quyết định.</div></div>
${H.mayRung()}</div>
${h3(2, `II.5 · Dây một đầu tự do: đo bằng ${m('\\lambda/4')}`, '3·2')}
<div class="card" style="padding:1.2mm 3mm">
<div>Đầu tự do là ${f(16)}, cách nút gần nhất ${f(12)}: ${nw(`${m('l=k\\tfrac{\\lambda}{2}+')} ${f(12)} ${m('=(2k+1)\\tfrac{\\lambda}{4}')}`)}</div>
<div><b>Làm:</b> cùng dây trên (${u('l=0{,}80', 'm')}, ${u('v\\approx20', 'm/s')}), tháo đầu B khỏi giá, gắn vào vòng nhẹ trượt trên cọc; quét tần số từ ${u('25', 'Hz')} xuống.</div>
<div><b>Quan sát:</b> ở ${u('25{,}0', 'Hz')} mất sóng dừng; ở ${u('18{,}75', 'Hz')} dây rung rõ trở lại, đầu B vung mạnh nhất.</div>
<div>Tần số nhỏ nhất: hai đầu cố định ${nw(`${f0} = ${f(14)} Hz`)} · một đầu tự do ${nw(`${f0} = ${f(14)} Hz`)}</div>
${wl(`Vì sao ở ${nw('25 Hz')} không có sóng dừng, ở ${nw('18,75 Hz')} lại có?`, 2)}</div>
${h3(3, 'II.6 · Biên độ dao động của một điểm trên dây', '3·3')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div>Cách nút gần nhất đoạn ${m('x')}: ${nw(`${m('A_M=')} ${f(30)}`)}</div>
<div>Bụng: biên độ ${f(12)}; bề rộng vùng dao động ${f(12)}.</div>
<div>Trong một bó: ${ck}cùng ${ck}ngược pha · hai bó kề nhau: ${ck}cùng ${ck}ngược pha.</div>
<div><b>Thay số:</b> ${nw(`${m('x=\\lambda/12')}: ${m('A_M=')} ${f(12)}`)} · ${nw(`${m('x=\\lambda/4')}: ${m('A_M=')} ${f(12)}`)}</div></div>
${H.bienDo()}</div>
${h3(4, 'III · Ba cái bẫy hay sập', '3·4')}
<div class="card" style="padding:1mm 3mm">
<div class="trap">${ck}<span><b>“Nút là chỗ sóng không truyền tới.”</b> Hai sóng đều tới; tại nút chúng ngược pha, cộng lại bằng 0.</span></div>
<div class="trap">${ck}<span><b>“Dây một đầu tự do vẫn dùng ${m('l=k\\lambda/2')}.”</b> Đếm số đầu cố định trước: một đầu tự do thì ${m('l=(2k+1)\\lambda/4')}.</span></div>
<div class="trap">${ck}<span><b>“Bao nhiêu bó thì bấy nhiêu nút.”</b> Hai đầu cố định: ${k} bó có ${m('k+1')} nút (kể cả hai đầu).</span></div></div>
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('TRẢ BÀI · TỰ KIỂM TRA · BÀI TOÁN MẪU')}
${h3(1, 'IV · Trả bài 5 câu', '4·1')}
${box(`${tb('1. Sóng dừng được tạo thành khi nào?')}${lines(2)}
${tb('2. Phản xạ ở đầu cố định và ở đầu tự do khác nhau thế nào?')}${lines(2)}
${tb('3. Nút sóng là gì, bụng sóng là gì? Biên độ mỗi loại?')}${lines(2)}
${tb('4. Viết điều kiện có sóng dừng cho hai trường hợp, kèm số nút, số bụng.')}${lines(2)}
${tb(`5. Từ sóng dừng tính ${L} và ${v} như thế nào?`)}${lines(2)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/5 câu · chưa thuộc: ${f(25)} ${nw(`${m('\\to')} đọc lại ô ${f(12)} Tập`)}</div>
${h3(2, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '4·2')}
${rkHai([1, 2, 3, 4], [5, 6, 7])}
${h3(3, 'V · Bài toán mẫu: đọc đề đến đâu, gọi kiến thức đến đó', '4·3')}
<div class="card soft" style="padding:1.2mm 3mm">Sợi dây AB dài ${u('l=1{,}0', 'm')}, hai đầu cố định; tốc độ truyền sóng trên dây ${u('v=20', 'm/s')}.
<div><b>a)</b> Tính tần số nhỏ nhất để trên dây có sóng dừng và bước sóng khi đó.</div>
<div><b>b)</b> Với ${u('f=40', 'Hz')}, trên dây có bao nhiêu bó sóng, bao nhiêu nút sóng?</div>
<div><b>c)</b> Giữ ${u('f=40', 'Hz')} rồi thả đầu B cho tự do. Trên dây có sóng dừng không? Vì sao?</div></div>
<table class="tb2"><tr><th style="width:50mm">Câu trong đề</th><th>Dữ liệu ${m('\\to')} kiến thức</th></tr>
<tr><td>“hai đầu cố định”</td><td>hai đầu là nút: ${m('l=k\\lambda/2')}; số nút ${m('=k+1')}</td></tr>
<tr><td>“tần số nhỏ nhất”</td><td></td></tr>
<tr><td>“${m('f=40')} Hz … bao nhiêu bó, nút”</td><td></td></tr>
<tr><td>“thả đầu B cho tự do”</td><td></td></tr></table>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('GIẢI BÀI TOÁN MẪU · BÀI TẬP VỀ NHÀ · THỬ THÁCH')}
${h3(1, 'Giải bài toán mẫu', '5·1')}
<div class="fig-side" style="${fs(46)}"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl(`a) ${L} khi ${k} nhỏ nhất; ${f0}:`, 3)}${wl(`b) ${L} ở 40 Hz; số bó ${k}; số nút:`, 3)}${wl(`c) ${m('l\\,/\\,(\\lambda/4)=')} … lẻ hay chẵn? Kết luận:`, 3)}${wl(`Kiểm tra: số bó × ${m('\\lambda/2')} có bằng ${l}?`, 1)}</div>${H.mauDay()}</div>
${h3(2, 'Điền bước còn thiếu: cùng cách làm, đổi số', '5·2')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:.6mm 3mm"><div>Dây ${u('l=1{,}2', 'm')}, hai đầu cố định, ${u('v=24', 'm/s')}, ${u('f=30', 'Hz')}.</div>
<div class="ln" style="height:7mm"><b>Bước 1:</b> ${nw(`${m('\\lambda=v/f=')} ${f(14)} m`)} &nbsp;·&nbsp; <b>Bước 2:</b> ${nw(`${m('k=2l/\\lambda=')} ${f(14)}`)}</div>
<div class="ln" style="height:7mm"><b>Bước 3:</b> có sóng dừng không? ${f(16)} &nbsp;·&nbsp; số nút: ${f(14)}</div></div>
${K.btvn().replace('<i>1</i>', '<i>3</i>')}
${h3(4, 'Thử thách phân tầng', '5·4')}
${box(wl(`${m('\\bigstar')} Dây ${u('1{,}2', 'm')}, hai đầu cố định, có sóng dừng với 3 bó. Tính bước sóng.`, 2)
 + wl(`${m('\\bigstar\\bigstar')} Cũng dây đó, ${u('v=24', 'm/s')}. Tính tần số.`, 2)
 + wl(`${m('\\bigstar\\bigstar\\bigstar')} Vẫn dây đó (${u('1{,}2', 'm')}, ${u('v=24', 'm/s')}) nhưng thả một đầu cho tự do, giữ ${u('f=30', 'Hz')}. Có sóng dừng không? Nếu không, hai tần số gần nhất cho sóng dừng là bao nhiêu?`, 3))}
${h3(5, 'VI · Mang về: điều em dễ quên nhất', '5·5')}
${box(wl('1.', 1) + wl('2.', 1) + wl('3.', 1))}
${foot(5)}</section>`;

const a1 = 'a<sub>1</sub>', a2 = 'a<sub>2</sub>', b1 = 'b<sub>1</sub>', b2 = 'b<sub>2</sub>', b3 = 'b<sub>3</sub>', b4 = 'b<sub>4</sub>', c1 = 'c<sub>1</sub>', c2 = 'c<sub>2</sub>', c3 = 'c<sub>3</sub>';
const dang = [
  { t: 'Dạng 1 · Dễ · Dây hai đầu cố định: tần số nhỏ nhất, số bó, số nút',
    de: `Dây AB dài ${u('l=0{,}6', 'm')}, hai đầu A, B cố định; ${u('v=24', 'm/s')}.<br><b>a)</b> bước sóng dài nhất (a<sub>1</sub>) và tần số nhỏ nhất (a<sub>2</sub>) để có sóng dừng<br><b>b)</b> cho ${u('f=60', 'Hz')}: có sóng dừng không (b<sub>1</sub>); nếu có, số bó (b<sub>2</sub>), số bụng (b<sub>3</sub>), số nút kể cả hai đầu (b<sub>4</sub>)`,
    nd: `${L} dài nhất khi ${nw(`${m('k=')} ${f(10)}`)}; có sóng dừng khi ${nw(`${m('k=2l/\\lambda')} là số ${f(16)}`)}`,
    a: [a1, a2, b1, b2, b3, b4], gi: 2, cot: 6 },
  { t: 'Dạng 2 · Trung bình · Dây một đầu cố định, một đầu tự do',
    de: `<div class="fig-side" style="grid-template-columns:1fr 30mm"><div>Dây AB dài ${u('l=0{,}9', 'm')}, đầu A cố định, đầu B gắn vòng nhẹ trượt trên cọc (đầu tự do); ${u('v=18', 'm/s')}.<br><b>a)</b> tần số nhỏ nhất để có sóng dừng<br><b>b)</b> ${u('f=30', 'Hz')}: có sóng dừng không<br><b>c)</b> ${u('f=45', 'Hz')}: có sóng dừng không (c<sub>1</sub>); số bụng (c<sub>2</sub>), số nút kể cả A, B (c<sub>3</sub>)</div>${H.d2Vong()}</div>`,
    nd: `${nw(`${m('l\\,/\\,(\\lambda/4)')}`)} phải là số ${f(14)}; số bụng ${m('=')} số nút ${m('=')} ${f(12)}`,
    a: ['a', 'b', c1, c2, c3], gi: 3, cot: 5 },
  { t: 'Dạng 3 · Trung bình · Từ số điểm đứng yên tìm bước sóng và tốc độ',
    de: `Dây dài ${u('l=1{,}5', 'm')}, hai đầu cố định, có sóng dừng với ${u('f=40', 'Hz')}. Ngoài hai đầu dây còn 4 điểm khác luôn đứng yên.<br><b>a)</b> số bó sóng<br><b>b)</b> bước sóng<br><b>c)</b> tốc độ truyền sóng`,
    nd: `số nút kể cả hai đầu ${m('=')} ${f(10)} ${m('+2')}; ${nw(`${m('k=')} số nút ${f(10)}`)}; ${nw(`${m('\\lambda=2l/k')}`)}, ${nw(`${m('v=\\lambda f')}`)}`,
    a: ['a', 'b', 'c'], gi: 3 },
  { t: 'Dạng 4 · Khó · Đổi tần số trên cùng một sợi dây',
    de: `Dây AB dài ${u('l=1{,}5', 'm')}, hai đầu cố định, ${v} không đổi. Với ${u('f_1=42', 'Hz')} dây có 7 nút (kể cả hai đầu).<br><b>a)</b> tần số nhỏ nhất để có sóng dừng<br><b>b)</b> muốn có 5 nút (kể cả hai đầu) thì ${m('f_2')} bằng bao nhiêu<br><b>c)</b> tốc độ truyền sóng`,
    nd: `cùng dây: ${nw(`${m('f=k f_0')}`)} nên ${fz} tỉ lệ với số ${f(14)}; ${nw(`${m('v=')} ${f(16)}`)}`,
    a: ['a', 'b', 'c'], gi: 3 },
  { t: 'Dạng 5 · Khó · Biên độ của một điểm trên dây có sóng dừng',
    de: `Dây AB dài ${u('90', 'cm')}, hai đầu cố định, có 3 bó sóng; biên độ tại bụng ${u('4', 'cm')}; M cách A ${u('5', 'cm')}.<br><b>a)</b> bước sóng &nbsp;·&nbsp; <b>b)</b> biên độ dao động của M<br><b>c)</b> khoảng cách nhỏ nhất từ A tới điểm có biên độ ${u('2\\sqrt3', 'cm')}<br><b>d)</b> bề rộng vùng dao động của một bụng`,
    nd: `${nw(`${m('A_M=A_b\\left|\\sin\\dfrac{2\\pi d}{\\lambda}\\right|')}`)}, ${m('d')} đo từ ${f(16)}; bề rộng bụng ${m('=')} ${f(12)} ${m('A_b')}`,
    a: ['a', 'b', 'c', 'd'], gi: 4, fig: H.d5Day() },
  { t: 'Dạng 6 · Khó · Hai tần số liên tiếp cùng cho sóng dừng',
    de: `Dây AB dài ${u('l=0{,}75', 'm')}, hai đầu cố định. Hai tần số liên tiếp cho sóng dừng là ${u('150', 'Hz')} và ${u('200', 'Hz')}.<br><b>a)</b> tần số nhỏ nhất · <b>b)</b> tốc độ truyền sóng<br><b>c)</b> với ${u('f=200', 'Hz')}: số bó (c<sub>1</sub>), số nút kể cả hai đầu (c<sub>2</sub>)`,
    nd: `hai tần số liên tiếp ứng với ${k} và ${m('k+1')}: ${nw(`${f0} ${m('=')} ${f(20)}`)}; ${nw(`${m('v=2lf_0')}`)}`,
    a: ['a', 'b', c1, c2], gi: 3 },
];

// Bài tương tự giải vào vở (thầy chốt 10/11): 1 cột; ô đáp số cuối đúng dòng của ý. Đáp số tính bằng Python 13/11/2026.
// Một dòng có thể gom nhiều ý ("<b>a)</b> … · <b>b)</b> …"): ô đáp số của mọi ý trong dòng xếp cuối dòng đó.
const oY = (s, o, w = 22) => s.split('<br>').map((p) => {
  const ys = [...p.matchAll(/<b>([a-d])\)<\/b>/g)].map((x) => x[1]);
  if (!ys.length) return `<div>${p}</div>`;
  const ls = o.filter((x) => ys.includes((Array.isArray(x) ? x[0] : x)[0]));
  return `<div class="yo"><span>${p}</span><span class="oo">${ls.map((x) => { const [n, wd] = Array.isArray(x) ? x : [x, w]; return `<span class="nw"><b>${n})</b>${f(wd)}</span>`; }).join('')}</span></div>`;
}).join('');
const ttDe = (b) => b.fig ? `<div class="fig-side" style="grid-template-columns:1fr ${b.fw}mm"><div>${oY(b.de, b.o, b.ow)}</div>${b.fig}</div>` : oY(b.de, b.o, b.ow);
const vaoVo = (ds) => ds.map((b) => (b.o ? { t: b.t, de: ttDe(b), k: 0 } : b));
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–3', 'DẠNG 4–6'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Dây dài ${u('0{,}8', 'm')}, hai đầu cố định, ${u('v=32', 'm/s')}.<br><b>a)</b> bước sóng dài nhất, tần số nhỏ nhất<br><b>b)</b> cho ${u('f=80', 'Hz')}: số bó, số nút (kể cả hai đầu)`, o: [a1, a2, b1, b2], ow: 18 },
    { t: 'Dạng 1 · Bài 2', de: `Dây dài ${u('1{,}2', 'm')}, hai đầu cố định, ${u('v=36', 'm/s')}.<br><b>a)</b> ${u('f=40', 'Hz')}: có sóng dừng không<br><b>b)</b> ${u('f=45', 'Hz')}: số bó, số nút (kể cả hai đầu)`, o: ['a', b1, b2], ow: 18 },
    { t: 'Dạng 2 · Bài 1', de: `Dây dài ${u('0{,}5', 'm')}, một đầu cố định, một đầu tự do, ${u('v=10', 'm/s')}.<br><b>a)</b> tần số nhỏ nhất để có sóng dừng<br><b>b)</b> ${u('f=20', 'Hz')}: có sóng dừng không<br><b>c)</b> ${u('f=25', 'Hz')}: số bụng, số nút (kể cả hai đầu)`, o: ['a', 'b', c1, c2], ow: 18 },
    { t: 'Dạng 2 · Bài 2', de: `Dây dài ${u('1{,}2', 'm')}, một đầu cố định, một đầu tự do, ${u('v=24', 'm/s')}.<br><b>a)</b> tần số nhỏ nhất để có sóng dừng<br><b>b)</b> ${u('f=35', 'Hz')}: số bụng, số nút (kể cả hai đầu)<br><b>c)</b> tần số lớn nhất nhỏ hơn ${u('30', 'Hz')} cho sóng dừng`, o: ['a', b1, b2, 'c'], ow: 18 },
    { t: 'Dạng 3 · Bài 1', de: `Dây dài ${u('0{,}9', 'm')}, hai đầu cố định, ${u('f=50', 'Hz')}; ngoài hai đầu còn 2 điểm khác luôn đứng yên.<br><b>a)</b> số bó · <b>b)</b> bước sóng · <b>c)</b> tốc độ truyền sóng`, o: ['a', 'b', 'c'], ow: 18 },
    { t: 'Dạng 3 · Bài 2', de: `Dây hai đầu cố định đặt cạnh thước như hình bên, ${u('f=25', 'Hz')}.<br><b>a)</b> số bó, số nút (kể cả hai đầu)<br><b>b)</b> bước sóng · <b>c)</b> tốc độ`, fig: H.tt3Hinh(), fw: 42, o: [a1, a2, 'b', 'c'], ow: 16 },
  ], [
    { t: 'Dạng 4 · Bài 1', de: `Dây dài ${u('1{,}2', 'm')}, hai đầu cố định, ${v} không đổi. Với ${u('f_1=60', 'Hz')} dây có 5 nút (kể cả hai đầu).<br><b>a)</b> tần số nhỏ nhất · <b>b)</b> tần số để dây có 3 nút<br><b>c)</b> tốc độ truyền sóng`, o: ['a', 'b', 'c'], ow: 18 },
    { t: 'Dạng 4 · Bài 2', de: `Dây dài ${u('0{,}8', 'm')}, hai đầu cố định, ${v} không đổi. Với ${u('f_1=30', 'Hz')} dây có 4 bụng.<br><b>a)</b> tần số nhỏ nhất · <b>b)</b> tần số để dây có 6 nút<br><b>c)</b> tốc độ truyền sóng`, o: ['a', 'b', 'c'], ow: 18 },
    { t: 'Dạng 5 · Bài 1', de: `Dây dài ${u('120', 'cm')}, hai đầu cố định, có 4 bó; biên độ bụng ${u('6', 'cm')}; M cách đầu A ${u('5', 'cm')}.<br><b>a)</b> bước sóng · <b>b)</b> biên độ của M<br><b>c)</b> khoảng cách nhỏ nhất từ A tới điểm có biên độ ${u('3\\sqrt2', 'cm')}<br><b>d)</b> bề rộng vùng dao động của bụng`, o: ['a', 'b', 'c', 'd'], ow: 18 },
    { t: 'Dạng 5 · Bài 2', de: `Dây dài ${u('60', 'cm')}, hai đầu cố định, có 2 bó; <b>sóng tới</b> có biên độ ${u('1{,}5', 'cm')}; N cách đầu A ${u('10', 'cm')}.<br><b>a)</b> bước sóng, biên độ bụng<br><b>b)</b> biên độ của N<br><b>c)</b> khoảng cách nhỏ nhất từ A tới điểm có biên độ ${u('1{,}5', 'cm')}<br><b>d)</b> bề rộng vùng dao động của bụng`, o: [a1, a2, 'b', 'c', 'd'], ow: 16 },
    { t: 'Dạng 6 · Bài 1', de: `Dây dài ${u('1{,}0', 'm')}, hai đầu cố định; hai tần số liên tiếp cho sóng dừng là ${u('120', 'Hz')} và ${u('150', 'Hz')}.<br><b>a)</b> tần số nhỏ nhất · <b>b)</b> tốc độ truyền sóng<br><b>c)</b> với ${u('150', 'Hz')}: số bó, số nút (kể cả hai đầu)`, o: ['a', 'b', c1, c2], ow: 18 },
    { t: 'Dạng 6 · Bài 2', de: `Dây dài ${u('0{,}6', 'm')}, hai đầu cố định; hai tần số liên tiếp cho sóng dừng là ${u('84', 'Hz')} và ${u('105', 'Hz')}.<br><b>a)</b> tần số nhỏ nhất · <b>b)</b> tốc độ truyền sóng<br><b>c)</b> với ${u('84', 'Hz')}: số bó, số nút (kể cả hai đầu)`, o: ['a', 'b', c1, c2], ow: 18 },
  ]],
  dap: [
    `D1·1: ${a1}) 1,6 m · ${a2}) 20 Hz · ${b1}) 4 bó · ${b2}) 5 nút &nbsp;|&nbsp; D1·2: a) không (${m('k\\approx2{,}67')}) · ${b1}) 3 bó · ${b2}) 4 nút &nbsp;|&nbsp; D2·1: a) 5 Hz · b) không (${m('l/(\\lambda/4)=4')}, chẵn) · ${c1}) 3 bụng · ${c2}) 3 nút &nbsp;|&nbsp; D2·2: a) 5 Hz · ${b1}) 4 bụng · ${b2}) 4 nút · c) 25 Hz &nbsp;|&nbsp; D3·1: a) 3 bó · b) 0,6 m · c) 30 m/s &nbsp;|&nbsp; D3·2: ${a1}) 4 bó · ${a2}) 5 nút · b) 0,6 m · c) 15 m/s`,
    `D4·1: a) 15 Hz · b) 30 Hz · c) 36 m/s &nbsp;|&nbsp; D4·2: a) 7,5 Hz · b) 37,5 Hz · c) 12 m/s &nbsp;|&nbsp; D5·1: a) 60 cm · b) 3 cm · c) 7,5 cm · d) 12 cm &nbsp;|&nbsp; D5·2: ${a1}) 60 cm · ${a2}) 3 cm · b) ${m('1{,}5\\sqrt3\\approx2{,}60')} cm · c) 5 cm · d) 6 cm &nbsp;|&nbsp; D6·1: a) 30 Hz · b) 60 m/s · ${c1}) 5 bó · ${c2}) 6 nút &nbsp;|&nbsp; D6·2: a) 21 Hz · b) 25,2 m/s · ${c1}) 4 bó · ${c2}) 5 nút`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 3], kq: [[1, 2, 3], [4, 5, 6]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'sóng phản xạ 1·4 · nút, bụng 1·5 · bó sóng 2·1 · điều kiện 2·2 · đo bước sóng, tốc độ 3·1 · đầu tự do 3·2 · biên độ 3·3 · bẫy 3·4 · bài toán mẫu 4·3 · dạng 1–3 ở 6·1 · dạng 4–6 ở 7·1',
  out: process.argv[2],
});
