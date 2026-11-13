// Ruột tập VL11 – Bài 4 · Bài tập về dao động điều hoà (lesson id 23). Quyển Chương 1 lớp 11: bài 1 = tr. 1–12 → bài 4 = tr. 37–48.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự giải vào vở · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l11-bai4.mjs (toàn bộ SVG tự vẽ; đồ thị x–t vẽ từ phương trình thật nên đọc được số). Nội dung theo bài web
// (book/cache/23.json, tải 13/11/2026): mục tiêu, dự đoán quả lắc, bốn họ bài tập, thí nghiệm chìa khoá + băng giấy + quay chậm,
// ba bẫy, Trả bài 6 câu, bài toán mẫu x = 8cos(2πt − π/3), câu 7 biến thể, thử thách, 5 dạng bài tập mẫu.
// Câu hỏi trắc nghiệm trên web (Câu 1–7) chuyển thành ô điền ngắn (giấy chỉ giữ việc phải viết tay).
// Đáp số Bài tương tự (tuongTu.dap) tính bằng Python 13/11/2026 (đếm số lần qua li độ bằng mô phỏng, quãng đường bằng tích phân số).
// Chạy: node scripts/ruot-tap/l11-bai4.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl11-bai4.pdf
//       node scripts/ruot-tap/l11-bai4.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l11-bai4/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL11b4 as H } from './hinh-l11-bai4.mjs';
const fc = (w = 16) => `<span class="fill" style="min-width:${w}mm;height:9mm"></span>`; // ô phân số cao 9 mm

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
  const out = resolve(HERE, 'out/hinh-l11-bai4'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 4, lid: 23, ten: 'BÀI TẬP VỀ DAO ĐỘNG ĐIỀU HOÀ', lop: 11, baiDau: 1, sub: 'Vật lí 11 · Chương 1: Dao động' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const cm = (s) => nw(`${s}&nbsp;cm`);
const pi = m('\\pi'), w_ = m('\\omega'), ph = m('\\varphi');
const x0 = m('x_0'), v0 = m('v_0');
const pt = (s) => m(`x=${s}`);

const p1 = `<section class="page">
${head('BÀI 4 · BÀI TẬP VỀ DAO ĐỘNG ĐIỀU HOÀ', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Nhìn đề, gọi đúng một trong <b>4 họ</b> bài tập dao động điều hoà`)}
${dong(`${ck}Đưa phương trình về <b>dạng chuẩn</b> rồi đọc biên độ, pha ban đầu, chu kì; đọc <b>đồ thị</b> ${m('x')}–${m('t')}`)}
${dong(`${ck}Dùng <b>hệ thức độc lập</b> giữa ${m('x')}, ${m('v')}, ${m('a')}; chọn đúng <b>dấu của pha ban đầu</b> ${ph}`)}
${dong(`${ck}Dùng <b>vòng tròn pha</b> tính thời gian, quãng đường, tốc độ trung bình`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Em bấm giờ quả lắc từ biên trái tới biên phải được ${nw('0,8 s')}. Chu kì dao động của quả lắc bằng bao nhiêu?</p>
<div class="fig-side" style="${fs(44)}"><div>
${opt('A', '0,8 s')}
${opt('B', '0,4 s')}
${opt('C', '1,6 s')}
${opt('D', '3,2 s')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 3)}</div>
${H.quaLac()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Một chu kì là vật đi từ đâu tới đâu?</span></div>${lines(2)}</div>
${h3(4, 'II.1 · Họ 1: đọc phương trình, đọc đồ thị', '1·4')}
<div class="card fig-side" style="${fs(44)};padding:1.2mm 3mm"><div>
<div>Dạng chuẩn: ${m('x=')} ${f(30)}, với ${nw(`${m('A')} ${f(10)} 0`)} và ${nw(`${ph} ${m('\\in(-\\pi;\\pi]')}`)}</div>
<div>${nw(`${m('T=')} ${fc()} s`)} · ${nw(`${m('f=')} ${fc()} Hz`)} (${w_}: rad/s)</div>
<div>Dấu trừ trước cos: ${nw(`${m('-\\cos\\alpha=\\cos(\\alpha')} ${f(12)} ${m('\\pi)')}`)} <span class="hint">(dấu nào giữ pha trong ${m('(-\\pi;\\pi]')}?)</span></div>
<div>Gặp sin: ${nw(`${m('\\sin\\alpha=\\cos\\big(\\alpha')} ${f(12)} ${m('\\tfrac{\\pi}{2}\\big)')}`)} <span class="hint">(+ hay −?)</span></div>
<div>Đồ thị bên, viết theo ${m('A')}, ${m('T')}:</div><div>khoảng 1 = ${f(12)} · 2 = ${f(12)} · 3 = ${f(12)}</div>
</div>${H.doThiBaKhoang()}</div>
<div class="card" style="margin-top:-1.5mm;border-top:0;border-radius:0 0 1.5mm 1.5mm;padding:0 3mm 1.2mm">
<div><b>Ví dụ.</b> ${pt('5\\sin(4\\pi t)')} cm đổi thành ${m('x=')} ${f(44)} cm</div>
<div>${nw(`${m('A=')} ${f(12)}`)} &nbsp;${nw(`${ph}${m('=')} ${f(12)}`)} &nbsp;${nw(`${m('T=')} ${f(12)}`)}</div></div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('HỌ 1 · HỌ 2: x, v, a · ĐO CHU KÌ')}
${h3(1, 'Làm nhanh Họ 1', '2·1')}
${box(`<div style="padding-top:.6mm"><b>Câu 1.</b> ${pt('-6\\cos(5\\pi t)')} cm. Dạng chuẩn: ${m('x=')} ${f(34)} cm</div>
<div>${nw(`${m('A=')} ${f(12)}`)} &nbsp;${nw(`${ph}${m('=')} ${f(12)}`)} &nbsp;· lúc ${m('t=0')} vật ở ${f(25)}</div>
<div style="margin-top:.6mm"><b>Câu 2.</b> Gắn bút vào quả nặng dao động, kéo đều băng giấy dưới bút ${nw('20 cm/s')}. Trên giấy: đỉnh cao nhất cách đáy thấp nhất ${cm('6,0')}; hai đỉnh liền kề cách nhau ${cm('16,0')}.</div>
<div>${nw(`${m('A=')} ${f(12)} cm`)} &nbsp; ${nw(`${m('T=')} ${f(12)} s`)} &nbsp;<span class="hint">(giấy chạy bao xa trong một chu kì?)</span></div>${lines(1)}`)}
${h3(2, 'II.2 · Họ 2: quan hệ x, v, a', '2·2')}
<div class="card fig-side" style="${fs(44)};padding:1.2mm 3mm"><div>
<div>${m('v=-A\\omega\\sin(\\omega t+\\varphi)')}; tốc độ cực đại ${nw(`${m('v_{\\max}=')} ${f(14)}`)} khi vật ở ${f(25)}</div>
<div>${m('a=')} ${f(16)}: ${m('a')} luôn ${f(25)} dấu với ${m('x')}</div>
<div>${nw(`${m('|a|_{\\max}=')} ${f(14)}`)} khi vật ở ${f(25)}</div>
</div>${H.trucXVA()}</div>
<div class="card" style="margin-top:-1.5mm;border-top:0;border-radius:0 0 1.5mm 1.5mm;padding:0 3mm 1.2mm">
<div>Hệ thức độc lập (không chứa ${m('t')}): ${m('v^2=')} ${f(34)}</div>
<div>Tại O: ${nw(`${m('|v|=')} ${f(14)}`)}, ${nw(`${m('a=')} ${f(12)}`)} &nbsp;· tại biên: ${nw(`${m('v=')} ${f(12)}`)}, ${nw(`${m('|a|=')} ${f(14)}`)}</div></div>
${box(`<div style="padding-top:.6mm"><b>Câu 3.</b> ${nw(`${m('A=5')} cm`)}, ${nw(`${w_}${m('=10')} rad/s`)}; vật ở ${nw(`${m('x=-3')} cm`)}.</div>
<div>Tốc độ ${nw(`${m('|v|=')} ${f(14)} cm/s`)} &nbsp; gia tốc ${nw(`${m('a=')} ${f(16)} ${m('\\mathrm{cm/s^2}')}`)}</div>${lines(1)}
<div style="padding-top:.6mm">Cùng vật, ở ${nw(`${m('x=+4')} cm`)}: ${nw(`${m('|v|=')} ${f(14)} cm/s`)} &nbsp; ${nw(`${m('a=')} ${f(16)} ${m('\\mathrm{cm/s^2}')}`)}</div>${lines(1)}`)}
${h3(3, 'Thí nghiệm: đo chu kì chùm chìa khoá', '2·3')}
<div class="card" style="padding:1.2mm 3mm">
<div><b>Làm:</b> buộc chùm chìa khoá vào dây dài ${cm('36')}, kéo lệch ${cm('5,0')} rồi thả; bấm điện thoại thời gian 10 dao động ${m('t_{10}')}, đo 5 lần.</div>
<table class="tbl-ct" style="margin:.8mm 0"><tr><th>Lần</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>Trung bình</th></tr>
<tr><td>${m('t_{10}')} (s)</td><td>12,12</td><td>11,93</td><td>12,18</td><td>11,89</td><td>12,03</td><td></td></tr></table>
<div>Sai số ${nw(`${m('\\Delta t_{10}=\\dfrac{t_{\\max}-t_{\\min}}{2}=')} ${f(14)} s`)} · ${nw(`${m('\\bar T=')} ${f(14)} s`)} · ${nw(`${m('\\Delta T=')} ${f(14)} s`)}</div>
<div>Kết quả <span class="hint">(${m('\\Delta T')} làm tròn lên, giữ 1 chữ số có nghĩa)</span>: ${nw(`${m('T=')} ${f(14)} ${m('\\pm')} ${f(12)} s`)}</div>
<div><b>Rút ra:</b> từ ${m('t_{10}')} sang ${m('T')}: chia cả ${f(25)} lẫn ${f(25)} cho 10.</div>
<div>Từ ${m('\\bar T')}: ${nw(`${w_}${m('=2\\pi/\\bar T=')} ${f(14)} rad/s`)} · ${nw(`${m('v_{\\max}=A\\omega=')} ${f(14)} cm/s`)}</div>
${wl('Vì sao bấm giờ 10 dao động rồi chia 10, mà không bấm 1 dao động?', 2)}</div>
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('HỌ 3: VIẾT PHƯƠNG TRÌNH · HỌ 4: VÒNG TRÒN PHA')}
${h3(1, 'II.3 · Họ 3: viết phương trình từ lúc t = 0', '3·1')}
<div class="card fig-side" style="${fs(36)};padding:1.2mm 3mm"><div>
<div><b>B1.</b> ${nw(`${w_}${m('=')} ${fc()}`)} (từ ${m('T')}) ${nw(`${m('=')} ${fc()}`)} (từ ${m('v_{\\max}, A')})</div>
<div><b>B2.</b> ${m('A')} đề cho, hoặc ${nw(`${m('A^2=x_0^2+')} ${fc(20)}`)}</div>
<div><b>B3.</b> ${nw(`${m('\\cos\\varphi=')} ${fc()}`)} → hai giá trị ${m('\\pm\\varphi')} (${m('M_1, M_2')})</div>
<div><b>B4.</b> ${nw(`${m('v_0>0')} ⇒ ${ph} ${f(10)} 0`)}; ${nw(`${m('v_0<0')} ⇒ ${ph} ${f(10)} 0`)}</div>
<div style="margin-top:.6mm"><b>Ví dụ.</b> ${nw(`${m('A=10')} cm`)}, ${nw(`${m('T=2')} s`)}, ${m('t=0')} ở ${nw(`${m('x=5')} cm`)}, đi chiều +</div>
<div>${nw(`${w_}${m('=')} ${f(14)}`)} &nbsp;${nw(`${m('\\cos\\varphi=')} ${fc()}`)} &nbsp;${nw(`${ph}${m('=')} ${fc()}`)}</div>
<div>${m('x=')} ${f(40)} cm &nbsp;<span class="hint">thử lại ở ${m('t=0')}</span></div>
</div>${H.haiDiemM()}</div>
${h3(2, 'Bẫy 1: dấu của pha ban đầu', '3·2')}
<table><tr><th style="width:52mm">Lúc ${m('t=0')}, vật</th><th style="width:30mm">M ở nửa (trên/dưới)</th><th>${ph}</th></tr>
<tr><td>đi theo chiều dương</td><td></td><td>${ph} ${f(10)} 0</td></tr>
<tr><td>đi theo chiều âm</td><td></td><td>${ph} ${f(10)} 0</td></tr>
<tr><td>ở biên dương · ở biên âm</td><td style="background:var(--soft)"></td><td>${ph}${m('=')} ${f(12)} · ${ph}${m('=')} ${f(12)}</td></tr>
<tr><td>qua O chiều dương · chiều âm</td><td style="background:var(--soft)"></td><td>${ph}${m('=')} ${f(12)} · ${ph}${m('=')} ${f(12)}</td></tr></table>
<div style="margin:.8mm 0"><b>Câu 4.</b> ${nw(`${m('A=4')} cm`)}; ${m('t=0')}: ${nw(`${m('x=-2')} cm`)}, về biên âm. ${nw(`${m('\\cos\\varphi=')} ${fc()}`)} &nbsp;${nw(`${ph}${m('=')} ${fc()}`)}</div>
${h3(3, 'II.4 · Họ 4: thời gian, quãng đường', '3·3')}
<div class="card fig-side" style="${fs(36)};padding:1.2mm 3mm"><div>
<div>M quay ${f(25)} chiều kim đồng hồ, chiếu xuống ${m('Ox')}: ${f(12)}</div>
<div>Góc quét ${m('2\\pi')} ứng với ${f(10)}: ${nw(`${m('\\Delta t=')} ${fc()}`)}</div>
<div>Quay chậm: ${m('T')} = 192 khung, ${nw(`${m('A=4')} cm`)}:</div>
<div>${nw(`O → 2 cm (16 khung): ${m('T/')}${f(12)}`)} · ${nw(`2 → 4 cm (32 khung): ${m('T/')}${f(12)}`)} · ${nw(`O → biên: ${m('T/')}${f(12)}`)}</div>
<div>${nw(`${m('T/2')} đi ${f(12)}`)} · ${nw(`${m('T')} đi ${f(12)}`)} · ${m('T/4')} đi đúng ${m('A')} chỉ khi bắt đầu ở ${f(25)}</div>
<div>Tốc độ TB ${m('=')} ${fc()} · vận tốc TB ${m('=')} ${fc(18)}</div>
</div>${H.mocThoiGian()}</div>
<div><b>Câu 5.</b> ${nw(`${m('T=1{,}2')} s`)}. Thời gian ngắn nhất đi từ ${m('x=-A/2')} đến ${m('x=+A/2')}: ${nw(`${m('\\Delta t=')} ${f(16)} s`)}</div>
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('BẪY 2–3 · TRẢ BÀI · TỰ KIỂM TRA')}
${h3(1, 'Bẫy 2: quãng đường khác độ dời', '4·1')}
<div class="card" style="padding:1mm 3mm">
<div>Quãng đường ${m('s')}: cộng ${f(25)}, luôn ${f(25)} · độ dời ${m('=')} ${f(25)}, có dấu</div>
<div><b>Câu 6.</b> ${nw(`${m('A=4')} cm`)}: vật đi từ biên ${m('+A')} sang biên ${m('-A')} rồi về O. ${nw(`${m('s=')} ${f(14)} cm`)} &nbsp;độ dời ${nw(`${m('=')} ${f(14)} cm`)}</div></div>
${h3(2, 'Bẫy 3: đồ thị và máy tính', '4·2')}
<div class="card" style="padding:1mm 3mm">
<div class="trap">${ck}<span><b>“Đỉnh–đáy là ${m('A')}.”</b> Đỉnh ở ${cm('+2')}, đáy ở ${cm('−2')} thì ${nw(`${m('A=2')} cm`)}, không phải ${cm('4')}.</span></div>
<div class="trap">${ck}<span><b>“Đỉnh–đáy cách nhau ${m('T')}.”</b> Đỉnh và đáy liền kề cách nhau ${m('T/2')}.</span></div>
<div class="trap">${ck}<span><b>“Bấm ${m('\\cos(\\pi/3)')} ra 0,9998.”</b> Máy đang ở chế độ độ (D); bài dao động dùng rad (R): ${m('\\cos\\pi')} phải ra ${m('-1')}.</span></div></div>
${h3(3, 'IV · Trả bài 6 câu', '4·3')}
${box(`${tb(`1. Từ ${m('x=A\\cos(\\omega t+\\varphi)')} lấy ${m('T')}, ${m('f')} thế nào? Gặp dấu trừ, gặp sin thì sao?`)}${lines(2)}
${tb(`2. Ba công thức chủ chốt về ${m('x')}, ${m('v')}, ${m('a')} của Họ 2?`)}${lines(2)}
${tb(`3. Biết ${x0} và chiều đi lúc ${m('t=0')}, chọn ${ph} thế nào?`)}${lines(2)}
${tb(`4. Thời gian đi giữa các mốc O, ${m('A/2')}, biên?`)}${lines(1)}
${tb(`5. Quãng đường trong ${m('T/2')}, trong ${m('T')}? Khi nào ${m('T/4')} cho đúng ${m('A')}?`)}${lines(2)}
${tb('6. Tốc độ trung bình khác vận tốc trung bình ở đâu?')}${lines(1)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/6 câu · chưa thuộc: ${f(25)} ${nw(`→ đọc lại ô ${f(12)} Tập`)}</div>
${h3(4, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '4·4')}
${rkHai([1, 2, 3], [4, 5, 6])}
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TOÁN MẪU · BÀI TẬP VỀ NHÀ · THỬ THÁCH')}
${h3(1, 'V · Bài toán mẫu', '5·1')}
<div class="card soft" style="padding:1.2mm 3mm">Vật dao động điều hoà theo ${pt('8\\cos\\left(2\\pi t-\\dfrac{\\pi}{3}\\right)')} cm, ${m('t')} tính bằng giây.
<b>a)</b> Tìm chu kì và tốc độ cực đại. <b>b)</b> Tìm thời điểm đầu tiên vật qua vị trí cân bằng. <b>c)</b> Tính quãng đường và tốc độ trung bình từ ${m('t=0')} đến thời điểm đó.</div>
<table style="margin-top:.6mm"><tr><th style="width:46mm">Câu trong đề</th><th>Dữ liệu → kiến thức → họ</th></tr>
<tr><td>“${m('8\\cos(2\\pi t-\\pi/3)')}”</td><td>${m('A=8')} cm, ${w_}${m('=2\\pi')} rad/s, ${ph}${m('=-\\pi/3')} → họ 1</td></tr>
<tr><td style="height:6mm">“chu kì, tốc độ cực đại”</td><td></td></tr>
<tr><td style="height:6mm">“lúc ${m('t=0')}” (ngầm)</td><td></td></tr>
<tr><td style="height:6mm">“đầu tiên qua VTCB”</td><td></td></tr>
<tr><td style="height:6mm">“quãng đường, tốc độ TB”</td><td></td></tr></table>
<div class="fig-side" style="${fs(46)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl(`a) ${m('T')}, ${m('v_{\\max}')}:`, 2)}${wl(`${x0} và chiều đi lúc ${m('t=0')}:`, 1)}${wl(`b) ${m('\\Delta\\varphi')}, ${m('\\Delta t')}:`, 2)}${wl(`c) ${m('s')}, tốc độ TB:`, 2)}</div>${H.mau()}</div>
${h3(2, 'Điền bước còn thiếu: lần đầu tới x = −4 cm', '5·2')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div class="ln"><b>Bước 1 (cho sẵn):</b> ${m('x=-4=-A/2')}, vật đi chiều âm nên M ở nửa trên, pha ${m('2\\pi/3')}</div>
${wl(`Bước 2: ${m('\\Delta\\varphi=')} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ${m('\\Delta t=')}`, 1)}${wl(`Bước 3: ${m('s=')} <span class="hint" style="font-weight:400">(đi ${m('4\\to8\\to-4')})</span>`, 1)}</div>
${K.btvn().replace('<h3><i>1</i>Đề BTVN</h3>', h3(3, 'Đề BTVN', '5·3')).replace(wl('Ghi chú của thầy về đề:', 2), wl('Ghi chú của thầy về đề:', 1))}
${h3(4, 'Thử thách phân tầng', '5·4')}
${box(wl(`${m('\\bigstar')} ${pt('10\\cos(4\\pi t+\\pi/6)')} cm. Chu kì và tốc độ cực đại?`, 2)
 + wl(`${m('\\bigstar\\bigstar')} ${nw(`${m('A=5')} cm`)}; tại ${nw(`${m('x=4')} cm`)} tốc độ ${nw(`${m('6\\pi')} cm/s`)}. Chu kì?`, 2)
 + wl(`${m('\\bigstar\\bigstar\\bigstar')} ${pt('8\\cos(2\\pi t+\\pi/3)')} cm. Thời điểm vật qua vị trí cân bằng lần thứ hai?`, 2))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Phương trình có sin và dấu trừ',
    de: `${pt('-4\\sin(5\\pi t)')} (${m('x')}: cm, ${m('t')}: s). <b>a)</b> dạng chuẩn; biên độ ${m('A')} và pha ban đầu ${ph}<br><b>b)</b> chu kì ${m('T')}, tần số ${m('f')} &nbsp;<b>c)</b> tốc độ cực đại, gia tốc cực đại<br><b>d)</b> lúc ${m('t=0')} vật ở đâu, đi theo chiều nào`,
    nd: `sin → cos: pha thêm ${fc(14)} · dấu trừ trước: pha thêm ${f(14)}`, a: ['a', 'b', 'c', 'd'], gi: 5 },
  { t: 'Dạng 2 · Trung bình · Hệ thức độc lập: hai cặp (x, |v|)',
    de: `Ở ${nw(`${m('x_1=3{,}0')} cm`)}: tốc độ ${nw(`${m('16\\pi')} cm/s`)}; ở ${nw(`${m('x_2=4{,}0')} cm`)}: tốc độ ${nw(`${m('12\\pi')} cm/s`)}. <b>a)</b> tần số góc ${w_} và chu kì<br><b>b)</b> biên độ ${m('A')} &nbsp;<b>c)</b> gia tốc cực đại`,
    nd: `viết ${m('v^2=\\omega^2(A^2-x^2)')} cho hai vị trí rồi trừ vế để mất ${f(12)}`, a: ['a', 'b', 'c'], gi: 4 },
  { t: 'Dạng 3 · Trung bình · Đọc đồ thị rồi viết phương trình',
    de: `Đồ thị ${m('x')}–${m('t')} ở hình bên (${m('x')}: cm, ${m('t')}: s). <b>a)</b> biên độ và chu kì<br><b>b)</b> tần số góc &nbsp;<b>c)</b> pha ban đầu và phương trình`,
    nd: `đáy và đỉnh liền kề cách ${f(12)} · lúc ${m('t=0')} đường cong đi xuống ⇒ ${ph} ${f(10)} 0`, a: ['a', 'b', 'c'], gi: 4, fig: H.doThiD3() },
  { t: 'Dạng 4 · Khó · Vòng tròn pha: qua một vị trí lần thứ n',
    de: `${pt('6\\cos\\left(4\\pi t+\\dfrac{\\pi}{3}\\right)')} cm, ${m('t')} tính bằng giây. Mỗi lần đi qua tính một lần, kể cả hai chiều.<br><b>a)</b> thời điểm vật qua vị trí cân bằng lần đầu<br><b>b)</b> thời điểm vật qua ${nw(`${m('x=-3')} cm`)} lần thứ 5`,
    nd: `mỗi vòng, M cắt đường ${m('x=-3')} ${f(12)} lần · ${nw(`${m('\\Delta t=\\Delta\\varphi/')}${f(12)}`)}`, a: ['a', 'b'], gi: 8, fig: H.d4() },
  { t: 'Dạng 5 · Khó · Quãng đường, tốc độ TB, vận tốc TB',
    de: `${nw(`${m('T=0{,}6')} s`)}, ${nw(`${m('A=4')} cm`)}; lúc ${m('t=0')} vật ở ${nw(`${m('x=2')} cm`)}, đi về biên âm. Xét từ ${m('t=0')} đến ${nw(`${m('t=1{,}4')} s`)}.<br><b>a)</b> quãng đường<br><b>b)</b> tốc độ trung bình<br><b>c)</b> vận tốc trung bình`,
    nd: `${nw(`${m('\\Delta t=')} ${f(12)}${m('T+')}${f(12)}`)}; phần dư theo dõi vị trí, không lấy ${m('T/4')} ứng với ${m('A')}`, a: ['a', 'b', 'c'], gi: 8, fig: H.d5() },
];

// Bài tương tự giải vào vở (thầy chốt 10/11): 1 cột; ô đáp số đặt cuối đúng dòng của ý, nhãn ô khớp a) b) c)…
// (a<sub>1</sub>, a<sub>2</sub> khi ý có 2 kết quả); o có thể là 'nhãn:rộng' để ô dài hơn (phương trình).
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
  tieuDe: ['DẠNG 1–3', 'DẠNG 3–5'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `${pt('-5\\cos(4\\pi t)')} (${m('x')}: cm, ${m('t')}: s).<br><b>a)</b> biên độ và pha ban đầu<br><b>b)</b> chu kì và tần số<br><b>c)</b> tốc độ cực đại, gia tốc cực đại`, o: [s1('a'), s2('a'), s1('b'), s2('b'), s1('c'), s2('c')] },
    { t: 'Dạng 1 · Bài 2', de: `${pt('3\\sin\\left(2\\pi t+\\dfrac{\\pi}{6}\\right)')} (${m('x')}: cm, ${m('t')}: s).<br><b>a)</b> dạng chuẩn: biên độ và pha ban đầu<br><b>b)</b> chu kì và tốc độ cực đại<br><b>c)</b> lúc ${m('t=0')}: li độ và chiều đi`, o: [s1('a'), s2('a'), s1('b'), s2('b'), s1('c'), s2('c')] },
    { t: 'Dạng 2 · Bài 1', de: `Ở ${nw(`${m('x=6')} cm`)} tốc độ ${nw(`${m('8\\pi')} cm/s`)}; ở ${nw(`${m('x=8')} cm`)} tốc độ ${nw(`${m('6\\pi')} cm/s`)}.<br><b>a)</b> tần số góc và chu kì<br><b>b)</b> biên độ<br><b>c)</b> gia tốc cực đại`, o: [s1('a'), s2('a'), 'b', 'c'] },
    { t: 'Dạng 2 · Bài 2', de: `Tốc độ cực đại ${nw(`${m('20\\pi')} cm/s`)}; ở ${nw(`${m('x=6')} cm`)} tốc độ ${nw(`${m('16\\pi')} cm/s`)}.<br><b>a)</b> tần số góc và chu kì<br><b>b)</b> biên độ<br><b>c)</b> gia tốc khi ${nw(`${m('x=6')} cm`)}`, o: [s1('a'), s2('a'), 'b', 'c'] },
    { t: 'Dạng 3 · Bài 1', de: `Đồ thị ${m('x')}–${m('t')} bên (${m('x')}: cm, ${m('t')}: s).<br><b>a)</b> biên độ và chu kì<br><b>b)</b> tần số góc<br><b>c)</b> pha ban đầu<br><b>d)</b> phương trình`, fig: H.ttD3a(), fw: 46, o: [s1('a'), s2('a'), 'b', 'c', 'd:44'] },
    nhap(3),
  ], [
    { t: 'Dạng 3 · Bài 2', de: `Đồ thị ${m('x')}–${m('t')} bên (${m('x')}: cm, ${m('t')}: s).<br><b>a)</b> biên độ và chu kì<br><b>b)</b> tần số góc<br><b>c)</b> pha ban đầu<br><b>d)</b> phương trình`, fig: H.ttD3b(), fw: 46, o: [s1('a'), s2('a'), 'b', 'c', 'd:44'] },
    { t: 'Dạng 4 · Bài 1', de: `${pt('10\\cos\\left(\\pi t+\\dfrac{\\pi}{6}\\right)')} cm, ${m('t')} tính bằng giây. Mỗi lần đi qua tính một lần.<br><b>a)</b> thời điểm qua vị trí cân bằng lần đầu<br><b>b)</b> thời điểm qua ${nw(`${m('x=5')} cm`)} lần thứ 3`, fig: H.ttD4(), fw: 44, o: ['a', 'b'] },
    { t: 'Dạng 4 · Bài 2', de: `${pt('6\\cos\\left(4\\pi t-\\dfrac{\\pi}{2}\\right)')} cm, ${m('t')} tính bằng giây. Mỗi lần đi qua tính một lần.<br><b>a)</b> thời điểm đầu tiên vật tới ${nw(`${m('x=3')} cm`)}<br><b>b)</b> thời điểm qua ${nw(`${m('x=-3')} cm`)} lần thứ 4`, o: ['a', 'b'] },
    { t: 'Dạng 5 · Bài 1', de: `${nw(`${m('T=2{,}0')} s`)}, ${nw(`${m('A=5')} cm`)}; lúc ${m('t=0')} vật ở biên dương. Xét từ ${m('t=0')} đến ${nw(`${m('t=4{,}5')} s`)}.<br><b>a)</b> quãng đường<br><b>b)</b> tốc độ trung bình<br><b>c)</b> vận tốc trung bình`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 5 · Bài 2', de: `${nw(`${m('T=1{,}2')} s`)}, ${nw(`${m('A=6')} cm`)}; lúc ${m('t=0')} vật ở ${nw(`${m('x=-3')} cm`)}, đi theo chiều dương. Xét từ ${m('t=0')} đến ${nw(`${m('t=2{,}8')} s`)}.<br><b>a)</b> quãng đường<br><b>b)</b> tốc độ trung bình<br><b>c)</b> vận tốc trung bình`, o: ['a', 'b', 'c'] },
    nhap(3),
  ]],
  dap: [
    `D1·1: a<sub>1</sub>) 5 cm · a<sub>2</sub>) π · b<sub>1</sub>) 0,5 s · b<sub>2</sub>) 2 Hz · c<sub>1</sub>) 20π ≈ 62,8 cm/s · c<sub>2</sub>) 80π² ≈ 790 cm/s² &nbsp;|&nbsp; D1·2: a<sub>1</sub>) 3 cm · a<sub>2</sub>) −π/3 · b<sub>1</sub>) 1 s · b<sub>2</sub>) 6π ≈ 18,8 cm/s · c<sub>1</sub>) 1,5 cm · c<sub>2</sub>) chiều dương &nbsp;|&nbsp; D2·1: a<sub>1</sub>) π ≈ 3,14 rad/s · a<sub>2</sub>) 2 s · b) 10 cm · c) 10π² ≈ 98,7 cm/s² &nbsp;|&nbsp; D2·2: a<sub>1</sub>) 2π ≈ 6,28 rad/s · a<sub>2</sub>) 1 s · b) 10 cm · c) −24π² ≈ −237 cm/s² &nbsp;|&nbsp; D3·1: a<sub>1</sub>) 6 cm · a<sub>2</sub>) 0,6 s · b) 10π/3 ≈ 10,5 rad/s · c) 2π/3 · d) x = 6cos(10πt/3 + 2π/3) cm`,
    `D3·2: a<sub>1</sub>) 3 cm · a<sub>2</sub>) 2,4 s · b) 5π/6 ≈ 2,62 rad/s · c) −π/3 · d) x = 3cos(5πt/6 − π/3) cm &nbsp;|&nbsp; D4·1: a) 1/3 s ≈ 0,333 s · b) 13/6 s ≈ 2,17 s &nbsp;|&nbsp; D4·2: a) 1/24 s ≈ 0,0417 s · b) 23/24 s ≈ 0,958 s &nbsp;|&nbsp; D5·1: a) 45 cm · b) 10 cm/s · c) −1,11 cm/s &nbsp;|&nbsp; D5·2: a) 57 cm · b) 20,4 cm/s · c) 3,21 cm/s`,
  ],
};

await K.dung({
  trang1to5: ttHaiCot + [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 2], kq: [[1, 2, 3], [4, 5]], khoNhat: true },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo), dap: tuongTu.dap.map((x) => x.replaceAll('π', m('\\pi'))) },
  tra: 'Họ 1 1·4 · Họ 2 2·2 · đo chu kì 2·3 · Họ 3 3·1 · dấu của pha 3·2 · Họ 4 3·3 · bẫy 4·1–4·2 · bài toán mẫu 5·1 · dạng 1–3 → 6·1 · dạng 4–5 → 7·1',
  out: process.argv[2],
});
