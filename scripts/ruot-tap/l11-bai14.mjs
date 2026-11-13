// Ruột tập VL11 – Bài 14 · Bài tập về sóng (lesson id 33). Quyển Chương 2 lớp 11: bài 8 = tr. 1–12 → bài 14 = tr. 73–84.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự giải vào vở · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l11-bai14.mjs (toàn bộ SVG tự vẽ; hình dạng sóng và sóng dừng vẽ từ hàm thật nên đọc được số). Nội dung theo bài web
// (book/cache/33.json, tải 13/11/2026): mục tiêu, dự đoán 5 ngọn sóng, bốn họ A–D (15 dạng), thí nghiệm chậu nước, hai loa,
// khe Young đo laser, ống một đầu kín, ba bẫy, Trả bài 5 câu, bài toán mẫu đếm cực đại/cực tiểu, biến thể, thử thách, 6 dạng bài tập mẫu.
// Câu trắc nghiệm trên web (Câu 1–6) chuyển thành ô điền ngắn (giấy chỉ giữ việc phải viết tay).
// Đáp số Bài tương tự (tuongTu.dap) tính bằng Python 13/11/2026.
// Chạy: node scripts/ruot-tap/l11-bai14.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl11-bai14.pdf
//       node scripts/ruot-tap/l11-bai14.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l11-bai14/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL11b14 as H } from './hinh-l11-bai14.mjs';

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
  const out = resolve(HERE, 'out/hinh-l11-bai14'); mkdirSync(out, { recursive: true });
  const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true, args: ['--allow-file-access-from-files'] });
  const pg = await b.newPage();
  const kx = pathToFileURL(BOOK + 'node_modules/katex/dist/katex.min.css').href;
  for (const [name, fn] of Object.entries(H)) {
    writeFileSync(out + '/_tmp.html', `<!doctype html><meta charset="utf-8"><link rel="stylesheet" href="${kx}"><style>${css}</style>${fn()}`);
    await pg.goto(pathToFileURL(out + '/_tmp.html').href, { waitUntil: 'networkidle0' });
    await pg.evaluate('document.fonts.ready');
    await (await pg.$('.fig')).screenshot({ path: `${out}/${name}.png` });
    console.log(`${name}.png`);
  }
  await b.close();
  process.exit(0);
}

const K = khoiTao({ bai: 14, lid: 33, ten: 'BÀI TẬP VỀ SÓNG', lop: 11, baiDau: 8, sub: 'Vật lí 11 · Chương 2: Sóng' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const u = (s, d) => nw(`${s}&nbsp;${d}`);
const L_ = m('\\lambda'), dp = m('\\Delta\\varphi');
const k12 = m('(k+\\tfrac12)');

const p1 = `<section class="page">
${head('BÀI 14 · BÀI TẬP VỀ SÓNG', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Nhìn đề, gọi đúng một trong <b>4 họ</b> bài tập sóng (15 dạng gộp lại)`)}
${dong(`${ck}Thuộc <b>công thức chủ chốt</b> của từng họ, kèm cái <b>bẫy</b> hay mất điểm`)}
${dong(`${ck}Đọc đề: gạch dữ kiện → gọi kiến thức → tính → kiểm tra kết quả`)}
${dong(`${ck}Tự trả lời 5 câu Trả bài mà không mở sách`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Đề cho: “khoảng cách giữa 5 ngọn sóng liên tiếp là ${u('2', 'm')}”. Bước sóng bằng bao nhiêu?</p>
<div class="fig-side" style="${fs(46)}"><div>
${opt('A', '0,4 m')}
${opt('B', '0,5 m')}
${opt('C', '1 m')}
${opt('D', '2 m')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 2)}</div>
${H.namNgon()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Đếm số chấm hay đếm số khoảng?</span></div>${lines(1)}</div>
${h3(4, 'Bốn họ: nhìn từ khoá, gọi họ', '1·4')}
<table><tr><th style="width:62mm">Từ khoá trong đề</th><th style="width:14mm">Họ</th><th>Đại lượng “thước đo”</th></tr>
<tr><td>ngọn sóng, tần số, lệch pha, sóng điện từ</td><td>A</td><td>${L_}${m('=vT')} · Dạng 1–5</td></tr>
<tr><td>hai nguồn A, B; cực đại, cực tiểu</td><td>${f(8)}</td><td>hiệu đường đi ${f(20)} · Dạng 6–8</td></tr>
<tr><td>khe Young, vân sáng, vân tối</td><td>${f(8)}</td><td>khoảng vân ${f(16)} · Dạng 9–12</td></tr>
<tr><td>dây hai đầu cố định, ống sáo, nút, bụng</td><td>${f(8)}</td><td>${m('L=')} ${f(16)} · Dạng 13–15</td></tr></table>
${h3(5, 'Thí nghiệm: đo tốc độ sóng nước trong chậu', '1·5')}
<div class="card" style="padding:1.2mm 3mm">
<div><b>Làm:</b> thả nút chai vào chậu nước rộng, gõ nhịp đều đầu thước xuống mặt nước. Bấm giờ 10 dao động của nút chai; đo khoảng cách 5 ngọn sóng liên tiếp.</div>
<div><b>Quan sát:</b> 10 dao động mất ${u('5,0', 's')}; 5 ngọn liên tiếp cách nhau ${u('0,60', 'm')}.</div>
<div><b>Rút ra:</b> ${nw(`${m('T=')} ${f(14)} s`)} &nbsp;${nw(`${L_}${m('=')} ${f(14)} m`)} &nbsp;${nw(`${m('v=\\lambda/T=')} ${f(14)} m/s`)}</div>
${wl('Vì sao bấm giờ 10 dao động rồi chia 10, đo 5 ngọn rồi chia 4?', 2)}</div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('HỌ A: SÓNG CƠ, SÓNG ĐIỆN TỪ · HỌ B: GIAO THOA')}
${h3(1, 'II.1 · Công thức chủ chốt họ A', '2·1')}
<div class="card fig-side" style="${fs(42)};padding:1.2mm 3mm"><div>
<div><b>D1.</b> ${nw(`${m('f=')} ${f(12)}`)} &nbsp;${nw(`${L_}${m('=vT=')} ${f(12)}`)} &nbsp;· đi một chu kì, sóng đi ${f(20)}</div>
<div><b>D2.</b> Cường độ ${nw(`${m('I=P/S')}`)}, sóng cầu ${nw(`${m('S=')} ${f(14)}`)}: ${nw(`${m('I\\sim')} ${f(14)}`)}</div>
<div>Xa nguồn gấp đôi thì ${m('I')} ${f(25)}</div>
<div><b>D3.</b> Hai điểm cách ${m('d')} trên phương truyền: ${nw(`${dp}${m('=')} ${f(16)}`)}</div>
<div>Cùng pha ${nw(`${m('d=')} ${f(14)}`)} · ngược pha ${nw(`${m('d=')} ${f(16)}`)} · vuông pha ${nw(`${m('d=(2k+1)\\lambda/4')}`)}</div>
</div>${H.songCau()}</div>
<div class="card" style="margin-top:-1.5mm;border-top:0;border-radius:0 0 1.5mm 1.5mm;padding:0 3mm 1.2mm">
<div><b>D4.</b> Nguồn ${m('u_0=A\\cos\\omega t')}, điểm M cách nguồn ${m('x')}: ${nw(`${m('u_M=A\\cos\\big(')} ${f(26)} ${m('\\big)')}`)}; M ${f(16)} pha hơn nguồn</div>
<div><b>D5.</b> Sóng điện từ: ${nw(`${m('f=')} ${f(12)}`)}, ${nw(`${m('c=3\\cdot10^8')} m/s`)}. Đài FM ${u('100', 'MHz')}: ${nw(`${L_}${m('=')} ${f(12)} m`)}</div>
<div>Thang sóng, ${L_} giảm dần: vô tuyến → ${f(20)} → ánh sáng nhìn thấy (${nw(`${m('0{,}38')}–${m('0{,}76\\ \\mu\\text{m}')}`)}) → tử ngoại → ${f(14)} → tia ${m('\\gamma')}</div></div>
${box(`<div style="padding-top:.6mm"><b>Câu 1.</b> Hai điểm trên cùng phương truyền sóng cách nhau ${m('1{,}5\\lambda')}.</div>
<div>${nw(`${dp}${m('=')} ${f(16)}`)} &nbsp;bỏ một vòng ${m('2\\pi')} còn ${f(14)} ${m('\\Rightarrow')} hai điểm dao động ${f(25)}</div>`)}
${h3(2, 'II.2 · Họ B: giao thoa sóng cơ (Dạng 6–8)', '2·2')}
<div class="card" style="padding:1.2mm 3mm">
<div><b>D6.</b> Hai nguồn <b>cùng pha</b>: cực đại ${nw(`${m('d_2-d_1=')} ${f(14)}`)} · cực tiểu ${nw(`${m('d_2-d_1=')} ${f(18)}`)}</div>
<div><b>D7.</b> Biên độ tại M (nguồn cùng pha, cùng biên độ ${m('A')}): ${nw(`${m('A_M=2A\\left|\\cos\\left[\\pi\\dfrac{d_2-d_1}{\\lambda}\\right]\\right|')}`)}; nguồn ngược pha đổi ${m('\\cos')} thành ${f(12)}</div>
<div><b>D8.</b> Đếm trên đoạn nối hai nguồn (cùng pha): cực đại ${nw(`${m('-\\dfrac{S_1S_2}{\\lambda}<k<\\dfrac{S_1S_2}{\\lambda}')}`)}; cực tiểu thay ${m('k')} bằng ${f(16)}</div>
<div>Dấu ${m('<')} chứ không phải ${m('\\le')} vì ${f(40)}</div>
<div style="margin-top:.6mm"><b>Ví dụ hai loa:</b> hai loa cùng phát ${u('340', 'Hz')}, cùng pha, ${nw(`${m('v=340')} m/s`)} ${m('\\Rightarrow')} ${nw(`${L_}${m('=')} ${f(12)} m`)}. Điểm cách loa 1 là ${u('4,0', 'm')}, cách loa 2 là ${u('4,5', 'm')}: hiệu đường ${f(12)} ${m('=')} ${f(12)}${L_} ${m('\\Rightarrow')} âm ${f(20)}</div>
</div>
<div class="fig-side" style="${fs(64)};margin-top:1mm"><div>
${box(`<div style="padding-top:.6mm"><b>Câu 2.</b> Với ${nw(`${m('AB=4\\lambda')}`)}, nguồn cùng pha:</div>
<div>${nw(`${m('-4<k<4')}`)} ${m('\\Rightarrow')} ${f(12)} cực đại</div><div>${nw(`${m('-4<k+\\tfrac12<4')}`)} ${m('\\Rightarrow')} ${f(12)} cực tiểu</div>
<div>Hai cực đại liền kề cách ${f(14)}</div><div class="hint">Đếm trên hình bên để kiểm lại.</div>`)}</div>
${H.giaoThoaAB()}</div>
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('HỌ C: KHE YOUNG · HỌ D: SÓNG DỪNG')}
${h3(1, 'II.3 · Họ C: khe Young (Dạng 9–10)', '3·1')}
<div class="card fig-side" style="${fs(48)};padding:1.2mm 3mm"><div>
<div><b>D9.</b> Khoảng vân ${nw(`${m('i=')} ${f(14)}`)}; vân sáng ${nw(`${m('x_s=')} ${f(12)}`)}; vân tối ${nw(`${m('x_t=')} ${f(16)}`)}</div>
<div>${m('a')}: khoảng cách ${f(25)} · ${m('D')}: khoảng cách ${f(30)}</div>
<div><b>D10.</b> Trường rộng ${m('L')}, đối xứng qua vân trung tâm (${m('[\\ ]')}: phần nguyên):</div>
<div>${nw(`${m('N_s=2\\left[\\dfrac{L}{2i}\\right]+1')}`)}, luôn ${f(12)} &nbsp;${nw(`${m('N_t=2\\left[\\dfrac{L}{2i}+0{,}5\\right]')}`)}, luôn ${f(12)}</div>
</div>${H.vanYoung()}</div>
${h3(2, 'Họ C: trùng vân, ánh sáng trắng (Dạng 11–12)', '3·2')}
<div class="card" style="padding:1.2mm 3mm">
<div><b>D11.</b> Trùng vân: ${nw(`${m('k_1\\lambda_1=')} ${f(16)}`)} ${m('\\Rightarrow')} ${nw(`${m('\\dfrac{k_1}{k_2}=')} ${f(14)}`)}, rút gọn về phân số tối giản</div>
<div><b>D12.</b> Ánh sáng trắng: ${nw(`${m('0{,}38\\le\\lambda\\le0{,}76\\ \\mu\\text{m}')}`)}; vân sáng tại ${m('x')}: ${nw(`${L_}${m('=')} ${f(16)}`)}, tìm các ${m('k')} nguyên thoả</div>
<div style="margin-top:.6mm"><b>Thí nghiệm đo bước sóng laser:</b> ${nw(`${m('a=0{,}50')} mm`)}, ${nw(`${m('D=1{,}50')} m`)}; đo khoảng cách ${m('\\ell')} của 6 vân sáng liên tiếp, 5 lần.</div>
<table class="tbl-ct" style="margin:.8mm 0"><tr><th>Lần</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>Trung bình</th></tr>
<tr><td>${m('\\ell')} (mm)</td><td>9,6</td><td>9,8</td><td>9,7</td><td>9,9</td><td>9,7</td><td></td></tr></table>
<div>6 vân sáng liên tiếp = ${f(10)} khoảng vân · ${nw(`${m('i=')} ${f(14)} mm`)} · ${nw(`${L_}${m('=ia/D=')} ${f(14)} ${m('\\mu\\text{m}')}`)}, vùng màu ${f(16)}</div>
${wl('Vì sao đo cả đoạn nhiều khoảng vân rồi chia, không đo thẳng một khoảng vân?', 2)}</div>
${h3(3, 'II.4 · Họ D: sóng dừng (Dạng 13–15)', '3·3')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div><b>D13.</b> Hai đầu cố định: ${nw(`${m('L=')} ${f(14)}`)}, có ${m('n')} bụng và ${f(12)} nút</div>
<div>Một đầu cố định, một đầu tự do: ${nw(`${m('L=')} ${f(16)}`)}, có ${f(12)} bụng và ${m('n+1')} nút</div>
<div><b>D14.</b> Dây hai đầu nút: ${nw(`${m('f_1=')} ${f(12)}`)}, ${m('f_n=nf_1')} · ống một đầu kín: ${nw(`${m('f_1=')} ${f(12)}`)}, chỉ có hoạ âm bậc ${f(10)}</div>
<div>Đầu cố định, đầu kín là ${f(12)} · đầu tự do, đầu hở là ${f(12)}</div>
<div><b>D15.</b> M cách nút gần nhất ${m('x')}: ${nw(`${m('A_M=2A\\left|\\sin\\dfrac{2\\pi x}{\\lambda}\\right|')}`)}</div>
</div>${H.motDauTuDo()}</div>
${foot(3)}</section>`;

const p4 = () => `<section class="page">
${head('HỌ D: LUYỆN NHANH · BA BẪY · TRẢ BÀI')}
${bay}
${foot(4)}</section>`;

const bay = `${h3(1, 'Họ D: luyện nhanh', '4·1')}
<div class="card" style="padding:1.2mm 3mm">
<div><b>Thử ống nhựa:</b> bịt kín một đầu ống dài ${u('0,17', 'm')}, thổi ngang miệng; ${nw(`${m('v=340')} m/s`)}. ${nw(`${m('f_1=')} ${f(12)} Hz`)}; nối dài ống thì nốt ${f(16)}</div></div>
${box(`<div style="padding-top:.6mm"><b>Câu 3.</b> Dây dài ${u('0,9', 'm')}, một đầu cố định, một đầu tự do, ${nw(`${L_}${m('=1{,}2')} m`)}. ${nw(`${m('L=')} ${f(10)}${m('\\cdot\\dfrac{\\lambda}{4}')}`)} ${m('\\Rightarrow')} ${nw(`${m('n=')} ${f(10)}`)} ${m('\\Rightarrow')} ${f(10)} bụng</div>`)}
${h3(2, 'III · Ba cái bẫy mất điểm', '4·2')}
<table><tr><th style="width:44mm">Bẫy</th><th>Em ghi lại cách đúng</th></tr>
<tr><td><b>1.</b> ${m('n')} ngọn, ${m('n')} vân sáng liên tiếp</td><td>${m('n')} ngọn cách ${f(18)}${L_} · 9 vân sáng cách ${f(12)}${m('i')}</td></tr>
<tr><td><b>2.</b> Hai nguồn ngược pha</td><td>cực đại khi ${nw(`${m('d_2-d_1=')} ${f(18)}`)}: cực đại, cực tiểu ${f(18)}</td></tr>
<tr><td><b>3.</b> Đếm nút, bụng</td><td>${m('n')} bó có ${f(14)} nút; đừng quên ${f(30)}</td></tr></table>
${box(`<div style="padding-top:.6mm"><b>Câu 4.</b> ${nw(`${m('i=2')} mm`)}, trường đối xứng rộng ${u('15', 'mm')}: ${nw(`${m('\\dfrac{L}{2i}=')} ${f(12)}`)} ${m('\\Rightarrow')} ${nw(`${m('N_s=')} ${f(12)}`)} vân sáng</div>
<div><b>Câu 5.</b> Dây hai đầu cố định có 5 nút (kể cả hai đầu): ${f(10)} bụng</div>
<div><b>Câu 6.</b> ${nw(`${m('AB=20')} cm`)}, ${nw(`${L_}${m('=2')} cm`)}, hai nguồn ngược pha: ${f(10)} cực đại, ${f(10)} cực tiểu</div>`, 'margin-top:1mm')}
${h3(3, 'IV · Trả bài 5 câu', '4·3')}
${box(`${tb(`1. ${m('T')}, ${m('f')}, ${L_}, ${m('v')} nối với nhau thế nào? ${m('n')} ngọn liên tiếp cách nhau bao nhiêu?`)}${lines(2)}
${tb(`2. Hai điểm cách ${m('d')} trên phương truyền lệch pha bao nhiêu? Khi nào cùng, ngược, vuông pha?`)}${lines(2)}
${tb('3. Hai nguồn cùng pha: điều kiện cực đại, cực tiểu? Đếm trên đoạn nối hai nguồn thế nào?')}${lines(2)}
${tb('4. Khoảng vân, vị trí vân sáng, vân tối? Khi nào hai bức xạ trùng vân?')}${lines(2)}
${tb('5. Điều kiện sóng dừng cho hai loại dây? Số nút, số bụng?')}${lines(2)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/5 câu · chưa thuộc: ${f(25)} ${nw(`→ đọc lại ô ${f(12)} Tập`)}</div>`;

const p5 = `<section class="page">
${head('BÀI TOÁN MẪU · BÀI TẬP VỀ NHÀ · THỬ THÁCH')}
${h3(1, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '5·1')}
${rkHai([1, 2, 3], [4, 5, 6])}
${h3(2, 'V · Bài toán mẫu', '5·2')}
<div class="card soft" style="padding:1.2mm 3mm">Hai nguồn sóng nước A, B cùng pha, cách nhau ${u('20', 'cm')}, tần số ${u('50', 'Hz')}, tốc độ truyền sóng ${u('1,0', 'm/s')}. Tìm số điểm dao động với biên độ cực đại và cực tiểu trên đoạn AB.</div>
<table style="margin-top:.6mm"><tr><th style="width:44mm">Câu trong đề</th><th>Dữ liệu → kiến thức</th></tr>
<tr><td>“cùng pha”</td><td>cực đại khi ${m('d_2-d_1=k\\lambda')} · Dạng 6</td></tr>
<tr><td style="height:6mm">“50 Hz”, “1,0 m/s”</td><td></td></tr>
<tr><td style="height:6mm">“cách nhau 20 cm”</td><td></td></tr>
<tr><td style="height:6mm">“cực đại, cực tiểu trên AB”</td><td></td></tr></table>
<div class="fig-side" style="${fs(44)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl(`${L_} (cùng đơn vị cm), ${m('AB/\\lambda')}:`, 2)}${wl('Cực đại: miền k, đếm:', 1)}${wl('Cực tiểu: miền k, đếm:', 1)}${wl('Kiểm tra (xen kẽ, chênh 1):', 1)}</div>${H.haiNguon()}</div>
<div style="margin-top:.8mm"><b>Đổi ${nw(`${m('AB=21')} cm`)}:</b> ${nw(`${m('AB/\\lambda=')} ${f(12)}`)} ${m('\\Rightarrow')} ${f(10)} cực đại, ${f(10)} cực tiểu &nbsp;<span class="hint">(hai điểm ${m('k+\\tfrac12=\\pm10{,}5')} rơi vào đâu?)</span></div>
${K.btvn().replace('<h3><i>1</i>Đề BTVN</h3>', h3(3, 'Đề BTVN', '5·3')).replace(wl('Ghi chú của thầy về đề:', 2), wl('Ghi chú của thầy về đề:', 2))}
${h3(4, 'Thử thách phân tầng', '5·4')}
${box(wl(`${m('\\bigstar')} Sóng mặt hồ ${nw(`${m('f=2')} Hz`)}, ${nw(`${L_}${m('=0{,}5')} m`)}. Tốc độ truyền sóng?`, 2)
 + wl(`${m('\\bigstar\\bigstar')} Dây ${u('1,2', 'm')}, hai đầu cố định, ${nw(`${m('f=50')} Hz`)}, có 4 bụng. Tốc độ truyền sóng?`, 2)
 + wl(`${m('\\bigstar\\bigstar\\bigstar')} Young ${nw(`${m('D=2')} m`)}, ${nw(`${m('a=1')} mm`)}, hai bức xạ ${nw(`${m('0{,}48')}`)} và ${nw(`${m('0{,}60\\ \\mu\\text{m}')}`)}. Vân sáng trùng gần vân trung tâm nhất cách bao xa?`, 2))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Đọc hình dạng sóng: bước sóng, chu kì, tốc độ',
    de: `Sóng hình sin truyền trên dây, ${nw(`${m('f=4')} Hz`)}. Hình bên: hình dạng dây tại một thời điểm, có bốn đỉnh sóng liên tiếp.<br><b>a)</b> bước sóng ${L_}<br><b>b)</b> chu kì ${m('T')}<br><b>c)</b> tốc độ truyền sóng ${m('v')} (m/s)`,
    nd: `bốn đỉnh liên tiếp có ${f(10)} khoảng; đổi ${L_} sang ${f(10)} trước khi nhân ${m('f')}`, a: ['a', 'b', 'c'], gi: 3, fig: H.d1() },
  { t: 'Dạng 2 · Trung bình · Độ lệch pha hai điểm trên phương truyền',
    de: `Sóng trên dây: ${nw(`${m('f=20')} Hz`)}, ${nw(`${m('v=4{,}0')} m/s`)}; M, N cách nhau ${nw(`${m('MN=0{,}45')} m`)} theo phương truyền sóng.<br><b>a)</b> bước sóng ${L_}<br><b>b)</b> độ lệch pha giữa M và N<br><b>c)</b> M, N dao động cùng pha, ngược pha, vuông pha hay không đặc biệt?`,
    nd: `${nw(`${dp}${m('=2\\pi d/\\lambda')}`)}; bỏ các bội của ${m('2\\pi')} rồi so phần dư với ${f(10)}, ${m('\\pi')}, ${m('\\pi/2')}`, a: ['a', 'b', 'c'], gi: 2, cot: 3 },
  { t: 'Dạng 3 · Khó · Giao thoa cùng pha: loại điểm M, đếm trên AB',
    de: `Hai nguồn kết hợp A, B cùng pha, ${nw(`${m('f=25')} Hz`)}, ${nw(`${m('AB=12')} cm`)}, ${nw(`${m('v=0{,}50')} m/s`)}. Điểm M cách A ${u('15', 'cm')}, cách B ${u('8', 'cm')}.<br><b>a)</b> bước sóng ${L_}<br><b>b)</b> M nằm trên cực đại hay cực tiểu?<br><b>c)</b> trên đoạn AB có bao nhiêu cực đại, bao nhiêu cực tiểu?`,
    nd: `${nw(`${m('|d_1-d_2|/\\lambda')}`)} nguyên → ${f(16)}, bán nguyên → ${f(16)}; A, B không tính`, a: ['a', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'], gi: 3 },
];
const dang2 = [
  { t: 'Dạng 4 · Khó · Khe Young: khoảng vân, đếm vân sáng, vân tối',
    de: `Young: ${nw(`${m('a=0{,}50')} mm`)}, ${nw(`${m('D=1{,}5')} m`)}, ${nw(`${L_}${m('=0{,}60\\ \\mu\\text{m}')}`)}; trường đối xứng rộng ${nw(`${m('L=17')} mm`)}.<br><b>a)</b> khoảng vân ${m('i')}<br><b>b)</b> số vân sáng, số vân tối trên trường<br><b>c)</b> điểm P cách vân trung tâm ${u('6,3', 'mm')} là vân sáng hay vân tối?`,
    nd: `đổi ${L_}, ${m('a')}, ${m('D')} về mét trước · ${m('[\\ ]')} là phần nguyên: bỏ phần lẻ, ${f(20)} · xét ${nw(`${m('x_P/i')}`)}`, a: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], gi: 3 },
  { t: 'Dạng 5 · Khó · Sóng dừng trên dây hai đầu cố định',
    de: `Dây AB dài ${nw(`${m('L=0{,}60')} m`)}, hai đầu cố định, ${nw(`${m('f=150')} Hz`)}: sóng dừng như hình.<br><b>a)</b> bước sóng và tốc độ truyền sóng<br><b>b)</b> số nút (kể cả A, B)<br><b>c)</b> giữ nguyên dây, lực căng: tần số để có 4 bụng?`,
    nd: `mỗi bó dài ${f(12)}; đổi ${m('f')} thì ${m('v')} ${f(16)}, ${L_} đổi`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'], gi: 3, fig: H.d5() },
  { t: 'Dạng 6 · Khó · Ống một đầu kín: hai tần số cộng hưởng liên tiếp',
    de: `Ống một đầu kín cộng hưởng ở hai tần số liên tiếp ${u('1020', 'Hz')}, ${u('1700', 'Hz')}; tốc độ âm ${u('340', 'm/s')}.<br><b>a)</b> tần số âm cơ bản<br><b>b)</b> chiều dài ống<br><b>c)</b> ở ${u('1700', 'Hz')} trong ống có mấy bụng sóng (kể cả đầu hở)?`,
    nd: `ống một đầu kín chỉ có hoạ âm bậc lẻ: hai tần số liên tiếp hơn kém ${f(12)}`, a: ['a', 'b', 'c'], gi: 2 },
];

// Bài tương tự giải vào vở (thầy chốt 10/11): 1 cột; ô đáp số đặt cuối đúng dòng của ý, nhãn ô khớp a) b) c)…
// (a<sub>1</sub>, a<sub>2</sub> khi ý có 2 kết quả); o có thể là 'nhãn:rộng' để ô dài hơn.
const ttHaiCot = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';
const oY = (s, o, w = 22) => s.split('<br>').map((p) => {
  const y = p.match(/^<b>([a-d])\)<\/b>/);
  if (!y) return `<div>${p}</div>`;
  const ls = o.filter((l) => l[0] === y[1]).map((l) => { const [n, ww] = l.split(':'); return [n, ww ? +ww : w]; });
  return `<div class="yo"><span>${p}</span><span class="oo">${ls.map(([l, ww]) => `<span class="nw"><b>${l})</b>${f(ww)}</span>`).join('')}</span></div>`;
}).join('');
const ttDe = (b) => b.fig ? `<div class="fig-side" style="grid-template-columns:1fr ${b.fw}mm">${`<div>${oY(b.de, b.o, b.ow)}</div>`}${b.fig}</div>` : oY(b.de, b.o, b.ow);
const vaoVo = (ds) => ds.map((b) => (b.o ? { t: b.t, de: ttDe(b), k: 0 } : b));
const nhap = (n) => ({ t: '<span class="nhap-t">Nháp / chỗ em còn vướng</span>', de: lines(n), k: 0 });
const s1 = (s) => `${s}<sub>1</sub>`, s2 = (s) => `${s}<sub>2</sub>`;
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–3', 'DẠNG 4–6'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Sóng hình sin trên dây, ${nw(`${m('f=5')} Hz`)}. Hình bên: hình dạng dây có năm đỉnh liên tiếp.<br><b>a)</b> bước sóng (cm)<br><b>b)</b> chu kì<br><b>c)</b> tốc độ truyền sóng (m/s)`, fig: H.tt1(), fw: 46, o: ['a', 'b', 'c'] },
    { t: 'Dạng 1 · Bài 2', de: `Phao trên mặt hồ nhô lên cao nhất 6 lần, từ lần 1 tới lần 6 mất ${u('10', 's')}. Khoảng cách giữa 4 ngọn sóng liên tiếp là ${u('1,8', 'm')}.<br><b>a)</b> chu kì<br><b>b)</b> bước sóng<br><b>c)</b> tốc độ truyền sóng`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 2 · Bài 1', de: `Sóng trên dây: ${nw(`${m('f=50')} Hz`)}, ${nw(`${m('v=2{,}0')} m/s`)}; M, N trên cùng phương truyền, cách nhau ${u('10', 'cm')}.<br><b>a)</b> bước sóng (cm)<br><b>b)</b> độ lệch pha giữa M và N<br><b>c)</b> cùng, ngược, vuông pha hay không đặc biệt?`, o: ['a', 'b', 'c:26'] },
    { t: 'Dạng 2 · Bài 2', de: `Sóng trên mặt nước: ${nw(`${m('f=10')} Hz`)}, ${nw(`${m('v=0{,}60')} m/s`)}; hai điểm trên cùng phương truyền cách nhau ${u('4,5', 'cm')}.<br><b>a)</b> bước sóng (cm)<br><b>b)</b> độ lệch pha<br><b>c)</b> cùng, ngược, vuông pha hay không đặc biệt?`, o: ['a', 'b', 'c:26'] },
    { t: 'Dạng 3 · Bài 1', de: `Hai nguồn A, B cùng pha, ${nw(`${m('f=20')} Hz`)}, ${nw(`${m('v=0{,}40')} m/s`)}, ${nw(`${m('AB=9')} cm`)}. M cách A ${u('13', 'cm')}, cách B ${u('7', 'cm')}.<br><b>a)</b> bước sóng (cm)<br><b>b)</b> M là cực đại hay cực tiểu?<br><b>c)</b> số cực đại, số cực tiểu trên AB`, o: ['a', 'b:26', s1('c'), s2('c')] },
    { t: 'Dạng 3 · Bài 2', de: `Hai nguồn A, B cùng pha, ${nw(`${m('f=40')} Hz`)}, ${nw(`${m('v=0{,}80')} m/s`)}, ${nw(`${m('AB=15')} cm`)}. M cách A ${u('10', 'cm')}, cách B ${u('15', 'cm')}.<br><b>a)</b> bước sóng (cm)<br><b>b)</b> M là cực đại hay cực tiểu?<br><b>c)</b> số cực đại, số cực tiểu trên AB`, o: ['a', 'b:26', s1('c'), s2('c')] },
  ], [
    { t: 'Dạng 4 · Bài 1', de: `Young: ${nw(`${m('a=1{,}0')} mm`)}, ${nw(`${m('D=2{,}0')} m`)}, ${nw(`${L_}${m('=0{,}50\\ \\mu\\text{m}')}`)}; trường đối xứng rộng ${u('12,5', 'mm')}.<br><b>a)</b> khoảng vân (mm)<br><b>b)</b> số vân sáng, số vân tối<br><b>c)</b> điểm cách vân trung tâm ${u('4,5', 'mm')}: vân sáng hay tối?`, o: ['a', s1('b'), s2('b'), 'c'] },
    { t: 'Dạng 4 · Bài 2', de: `Young: ${nw(`${m('a=0{,}80')} mm`)}, ${nw(`${m('D=1{,}6')} m`)}, ${nw(`${L_}${m('=0{,}45\\ \\mu\\text{m}')}`)}; trường đối xứng rộng ${u('10', 'mm')}.<br><b>a)</b> khoảng vân (mm)<br><b>b)</b> số vân sáng, số vân tối<br><b>c)</b> điểm cách vân trung tâm ${u('3,6', 'mm')}: vân gì, bậc mấy?`, o: ['a', s1('b'), s2('b'), 'c:26'] },
    { t: 'Dạng 5 · Bài 1', de: `Dây dài ${u('1,2', 'm')}, hai đầu cố định, ${nw(`${m('f=100')} Hz`)}, sóng dừng như hình bên.<br><b>a)</b> bước sóng, tốc độ truyền sóng<br><b>b)</b> số nút (kể cả hai đầu)<br><b>c)</b> giữ nguyên dây và lực căng, tần số để có 6 bụng`, fig: H.tt5(), fw: 44, o: [s1('a'), s2('a'), 'b', 'c'], ow: 16 },
    { t: 'Dạng 5 · Bài 2', de: `Dây dài ${u('0,90', 'm')}, hai đầu cố định, ${nw(`${m('f=60')} Hz`)}, trên dây có 3 bụng sóng.<br><b>a)</b> bước sóng, tốc độ truyền sóng<br><b>b)</b> số nút (kể cả hai đầu)<br><b>c)</b> giữ nguyên dây và lực căng, tần số để có 5 bụng`, o: [s1('a'), s2('a'), 'b', 'c'] },
    { t: 'Dạng 6 · Bài 1', de: `Ống một đầu kín, một đầu hở cộng hưởng ở hai tần số liên tiếp ${u('750', 'Hz')} và ${u('1250', 'Hz')}; tốc độ âm ${u('340', 'm/s')}.<br><b>a)</b> tần số âm cơ bản<br><b>b)</b> chiều dài ống<br><b>c)</b> số bụng ở ${u('1250', 'Hz')} (kể cả đầu hở)`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 6 · Bài 2', de: `Ống một đầu kín, một đầu hở cộng hưởng ở hai tần số liên tiếp ${u('1050', 'Hz')} và ${u('1470', 'Hz')}; tốc độ âm ${u('336', 'm/s')}.<br><b>a)</b> tần số âm cơ bản<br><b>b)</b> chiều dài ống<br><b>c)</b> số bụng ở ${u('1470', 'Hz')} (kể cả đầu hở)`, o: ['a', 'b', 'c'] },
    nhap(1),
  ]],
  dap: [
    `D1·1: a) 8 cm · b) 0,2 s · c) 0,4 m/s &nbsp;|&nbsp; D1·2: a) 2 s · b) 0,6 m · c) 0,3 m/s &nbsp;|&nbsp; D2·1: a) 4 cm · b) 5π rad · c) ngược pha &nbsp;|&nbsp; D2·2: a) 6 cm · b) 1,5π rad · c) vuông pha &nbsp;|&nbsp; D3·1: a) 2 cm · b) cực đại (bậc 3) · c<sub>1</sub>) 9 · c<sub>2</sub>) 8 &nbsp;|&nbsp; D3·2: a) 2 cm · b) cực tiểu · c<sub>1</sub>) 15 · c<sub>2</sub>) 14`,
    `D4·1: a) 1,0 mm · b<sub>1</sub>) 13 · b<sub>2</sub>) 12 · c) vân tối &nbsp;|&nbsp; D4·2: a) 0,90 mm · b<sub>1</sub>) 11 · b<sub>2</sub>) 12 · c) vân sáng bậc 4 &nbsp;|&nbsp; D5·1: a<sub>1</sub>) 0,6 m · a<sub>2</sub>) 60 m/s · b) 5 nút · c) 150 Hz &nbsp;|&nbsp; D5·2: a<sub>1</sub>) 0,6 m · a<sub>2</sub>) 36 m/s · b) 4 nút · c) 100 Hz &nbsp;|&nbsp; D6·1: a) 250 Hz · b) 0,34 m · c) 3 bụng &nbsp;|&nbsp; D6·2: a) 210 Hz · b) 0,40 m · c) 4 bụng`,
  ],
};

await K.dung({
  trang1to5: ttHaiCot + [p1, p2, p3, p4(), p5].join('\n'),
  btm: { dang: [...dang, ...dang2], tach: [3, 3], kq: [[1, 2, 3], [4, 5, 6]], khoNhat: true },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo), dap: tuongTu.dap.map((x) => x.replaceAll('π', m('\\pi'))) },
  tra: 'bốn họ 1·4 · họ A 2·1 · chậu nước 1·5 · họ B 2·2 · khe Young 3·1–3·2 · sóng dừng 3·3, 4·1 · bẫy 4·2 · trả bài 4·3 · bài toán mẫu 5·2 · dạng 1–3 → 6·1 · dạng 4–6 → 7·1',
  out: process.argv[2],
});
