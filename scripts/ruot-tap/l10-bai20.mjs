// Ruột tập VL10 – Bài 20 · Một số ví dụ về cách giải các bài toán thuộc phần động lực học (lesson id 65).
// Quyển Chương 3 lớp 10 (bài đầu = bài 13) → bài 20 = tr. 85–96.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l10-bai20.mjs (SVG tự vẽ + 1 ảnh thật cầu trượt trong book/assets/anh-that). Nội dung theo bài web (book/cache/65.json, tải 13/11/2026):
// mục tiêu, dự đoán cầu trượt, hành trang, II.1 bốn bước, cầu nối a, ba tình huống (mặt ngang/kéo xiên, mặt nghiêng, hai vật nối dây),
// thí nghiệm hai hộp, đo thử xe lăn, bốn bẫy, Trả bài 6 câu, thử thách. Bài web KHÔNG có mục bài tập mẫu riêng → 4 Dạng ở tr.6–7 lấy từ
// các ví dụ giải mẫu trong lý thuyết: D1 mặt ngang kéo ngang/kéo xiên · D2 mặt nghiêng · D3 bài toán ngược (thử thách ★★) · D4 hệ nối dây = bài toán mẫu V.
// Đáp số Dạng + Bài tương tự tính bằng Python 13/11/2026 (g = 10 m/s², sin/cos ghi trong từng đề).
// Chạy: node scripts/ruot-tap/l10-bai20.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl10-bai20.pdf
//       node scripts/ruot-tap/l10-bai20.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l10-bai20/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL10b20 as H } from './hinh-l10-bai20.mjs';

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
  const out = resolve(HERE, 'out/hinh-l10-bai20'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 20, lid: 65, ten: 'GIẢI BÀI TOÁN ĐỘNG LỰC HỌC', lop: 10, baiDau: 13, sub: 'Vật lí 10 · Chương 3: Động lực học' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const u = (s) => nw(m(s));
const ps = (w) => `<span class="fill" style="min-width:${w}mm;height:9mm"></span>`;   // ô phân số cao 9 mm
const g10 = u('g=10\\ \\mathrm{m/s^2}');
const al = m('\\alpha'), mu = m('\\mu');
const Fms = m('F_{\\mathrm{ms}}');

// Bài tương tự 1 cột, ô đáp số cuối dòng của ý (giống bài 23).
const ttCss = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';

const p1 = `${ttCss}<section class="page">
${head('BÀI 20 · GIẢI BÀI TOÁN ĐỘNG LỰC HỌC', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Thuộc quy trình <b>4 bước</b> giải một bài toán động lực học`)}
${dong(`${ck}Áp quy trình vào: <b>mặt ngang</b> có ma sát, <b>mặt phẳng nghiêng</b>, <b>hai vật nối dây</b> qua ròng rọc`)}
${dong(`${ck}Tránh 4 bẫy: thiếu/thừa lực · ${m('N=mg')} mọi lúc · đổi chiều dương · ma sát nghỉ tính ${m('\\mu N')}`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<div class="fig-side" style="${fs(44)}"><div>
<p style="margin:0 0 .6mm">Cầu trượt đôi: hai làn giống hệt, cùng độ dốc. Em và một bạn nặng gấp đôi em mặc quần cùng loại vải, cùng buông tay ở đỉnh (bỏ qua sức cản không khí). Ai tới chân cầu trước?</p>
${opt('A', 'Bạn nặng gấp đôi, xuống nhanh gấp đôi')}
${opt('B', 'Bạn nặng hơn, xuống nhanh hơn một chút')}
${opt('C', 'Hai người tới gần như cùng lúc')}
${opt('D', 'Em nhẹ hơn nên xuống nhanh hơn')}
<div style="margin-top:.6mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 1)}</div>
${H.cauTruot()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f(12)} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'Kiểm tra hành trang', '1·4')}
<div class="card" style="padding:1.2mm 3mm">
<div>Mặt nghiêng góc ${al}: thành phần của ${m('P')} <b>dọc</b> dốc ${f(25)} · <b>vuông góc</b> dốc ${f(25)}</div>
<div>Ma sát trượt: ${u('F_{\\mathrm{ms}}=')} ${f(16)} · với ${u('N=50\\ \\mathrm N')}, ${u('\\mu=0{,}2')}: ${u('F_{\\mathrm{ms}}=')} ${f(12)}&nbsp;N</div>
<div>Định luật II: ${nw(`${m('a=')} ${ps(16)}`)} (${m('F')} là ${f(25)}) · không chứa ${m('t')}: ${f(30)}</div></div>
${h3(5, 'II.1 · Bốn bước, một cầu nối', '1·5')}
<div class="card" style="padding:1.2mm 3mm">
<div><b>Bốn bước:</b> Vẽ – ${f(25)} – ${f(25)} – ${f(25)}</div>
<div><b>Bước 1</b> (Vẽ): chọn ${f(25)} khảo sát; Ox theo chiều ${f(30)}, giữ đến hết.</div>
<div><b>Bước 2:</b> mỗi lực phải chỉ ra được ${f(30)}</div>
<div><b>Bước 3:</b> ${f(40)} (dạng vectơ)</div>
<div><b>Bước 4:</b> theo Ox, Oy tìm ${m('a')}; kiểm dấu: ${m('a<0')} nghĩa là ${f(36)}</div></div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('CẦU NỐI GIA TỐC · TÌNH HUỐNG 1: MẶT NGANG')}
${h3(1, 'Lực và chuyển động nối với nhau qua đâu?', '2·1')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div>Đại lượng cầu nối: ${f(25)}</div>
<div><b>Bài toán thuận:</b> biết ${f(20)} → tìm ${m('a')} → tìm ${f(20)}</div>
<div><b>Bài toán ngược:</b> biết ${m('v,\\ s,\\ t')} → tìm ${f(12)} → tìm ${f(20)}</div>
<div style="margin-top:.6mm"><b>Ba công thức hay ghép</b> (chuyển động thẳng biến đổi đều):</div>
<div>${m('v=')} ${f(25)} &nbsp; ${m('s=')} ${f(30)}</div>
<div>${m('v^2-v_0^2=')} ${f(20)}</div></div>
${H.cauNoi()}</div>
${h3(2, 'II.2 · Tình huống 1: mặt ngang có ma sát', '2·2')}
<div class="card" style="padding:1.2mm 3mm">
<div><b>Ví dụ:</b> kéo thùng sách ${u('20\\ \\mathrm{kg}')} trên sàn ngang bằng lực <b>nằm ngang</b> ${u('80\\ \\mathrm N')}, hệ số ma sát trượt ${u('0{,}3')}, ${g10}.</div>
<div><b>Vẽ:</b> Ox theo chiều kéo, Oy hướng lên.</div>
<div><b>Kể lực</b> (ghi vật gây ra): ${m('\\vec P')} (${f(25)}) · ${m('\\vec N')} (${f(16)}) · ${m('\\vec F')} (dây) · ${m('\\vec F_{\\mathrm{ms}}')} (${f(16)})</div>
<div><b>Chiếu Oy:</b> ${f(30)} ⇒ ${u('N=')} ${f(12)}&nbsp;N</div>
<div><b>Chiếu Ox:</b> ${f(36)} ⇒ ${u('a=')} ${f(12)}&nbsp;${u('\\mathrm{m/s^2}')}</div>
<div><b>Kiểm:</b> ${m('a')} ${ck}dương ${ck}âm ⇒ thùng đi ${f(25)} chiều kéo.</div></div>
<div class="card fig-side" style="${fs(44)};padding:1.2mm 3mm"><div>
<div><b>Kéo xiên lên góc ${al}:</b> dây nhấc bớt thùng nên áp lực thay đổi.</div>
<div style="margin-top:.6mm">Chiếu Oy: ${f(36)} = 0</div>
<div>⇒ ${m('N=')} ${f(30)}</div>
<div style="margin-top:.6mm">Chiếu Ox: ${f(36)} ${m('=ma')}</div>
<div style="margin-top:.6mm">So với kéo ngang, ${m('N')} ${ck}lớn hơn ${ck}nhỏ hơn ⇒ ma sát ${f(16)}</div>
<div>Chỉ lợi khi góc nhỏ: xiên quá thì phần kéo ngang ${f(20)} giảm nhiều.</div></div>
${H.keoXien()}</div>
${h3(3, 'Làm nhanh', '2·3')}
${box(cau(`<b>Câu 1.</b> Kéo thùng ${u('20\\ \\mathrm{kg}')} bằng lực ${u('100\\ \\mathrm N')}, dây xiên lên ${u('30^\\circ')} so với sàn (${u('\\sin 30^\\circ=0{,}5')}), ${u('\\mu=0{,}2')}, ${g10}. Tính ${m('N')} và lực ma sát trượt. So với kéo nằm ngang cùng ${u('100\\ \\mathrm N')}, ma sát giảm bao nhiêu?`, 4))}
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('TÌNH HUỐNG 2: MẶT NGHIÊNG · TÌNH HUỐNG 3: HAI VẬT NỐI DÂY')}
${h3(1, 'II.3 · Tình huống 2: mặt phẳng nghiêng', '3·1')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div>Chọn Ox <b>dọc mặt nghiêng, chiều xuống dốc</b>; Oy vuông góc mặt nghiêng.</div>
<div>Chỉ một lực phải tách là ${f(12)}</div>
<div>dọc dốc: ${f(20)} · vuông góc: ${f(20)}</div>
<div style="margin-top:.6mm"><b>Oy:</b> ${f(30)} ${m('=0')}</div>
<div>⇒ ${m('N=')} ${f(20)}, ${ck}lớn hơn ${ck}nhỏ hơn ${m('mg')}</div>
<div style="margin-top:.6mm"><b>Ox</b> (trượt xuống): ${f(36)} ${m('=ma')}</div>
<div>⇒ ${m('a=')} ${f(36)}</div>
<div>Trong ${m('a')} không còn ${f(12)}. Bỏ ma sát: ${m('a=')} ${f(16)}</div></div>
${H.docTach()}</div>
${h3(2, 'Thí nghiệm: hai hộp, một nhẹ một nặng', '3·2')}
<div class="card" style="padding:1.2mm 3mm">
<div><b>Làm:</b> hai hộp bút giống nhau, một rỗng, một nhét đầy đồ; đặt cạnh nhau ở đầu tấm ván nghiêng khoảng ${u('30^\\circ')}, thả cùng lúc.</div>
<div><b>Quan sát:</b> ${f(60)}</div>
<div><b>Rút ra:</b> gia tốc trượt ${f(50)} khối lượng.</div>
<div><b>Vật nằm yên trên dốc</b> khi ${m('\\tan\\alpha\\le')} ${f(12)}; lúc đó ma sát nghỉ bằng ${f(20)} (không phải ${m('\\mu_n mg\\cos\\alpha')}).</div></div>
${h3(3, 'Làm nhanh', '3·3')}
${box(cau(`<b>Câu 2.</b> Hộp trượt xuống dốc nghiêng ${u('30^\\circ')} (${u('\\sin 30^\\circ=0{,}5')}; ${u('\\cos 30^\\circ\\approx 0{,}866')}), ${u('\\mu=0{,}2')}, ${g10}. Gia tốc của hộp?`, 2))}
${h3(4, 'II.4 · Tình huống 3: hai vật nối dây qua ròng rọc', '3·4')}
<div class="card fig-side" style="${fs(44)};padding:1.2mm 3mm"><div>
<div>Dây không dãn ⇒ hai vật cùng độ lớn ${f(25)}</div>
<div>Dây, ròng rọc nhẹ, không ma sát ⇒ cùng ${f(25)}</div>
<div>Chiều dương: ${f(50)}</div>
<div style="margin-top:.6mm">${m('m_1')} (bàn có ma sát): ${f(30)} ${m('=m_1a')}</div>
<div>${m('m_2')} (treo): ${f(30)} ${m('=m_2a')}</div>
<div>Cộng hai phương trình: ${f(12)} triệt tiêu.</div></div>
${H.rongRoc()}</div>
${box(cau(`<b>Câu 3.</b> Hình trên với ${u('m_1=4\\ \\mathrm{kg}')}, ${u('m_2=1\\ \\mathrm{kg}')}, ${u('\\mu=0{,}1')}, ${g10}. Hệ có chạy không? Nếu có, tính gia tốc.`, 2))}
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('ĐO THỬ · BỐN CÁI BẪY · TRẢ BÀI')}
${h3(1, 'II.5 · Đo thử: xe lăn kéo bởi quả nặng', '4·1')}
<div class="fig-side" style="${fs(38)}"><div>
<div style="margin-bottom:.6mm">Xe ${u('m_1=0{,}40\\ \\mathrm{kg}')} trên máng ngang, quả nặng ${u('m_2=0{,}10\\ \\mathrm{kg}')}. Thả từ nghỉ, đo ${m('t')} xe đi ${u('s=0{,}80\\ \\mathrm m')}; ${u('a=2s/t^2')}; ${g10}.</div>
<table class="tbl-ct" style="font-size:var(--fs-sm)"><tr><th>Lần</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th></tr>
<tr><td>${m('t\\ (\\mathrm s)')}</td><td>0,93</td><td>0,95</td><td>0,92</td><td>0,94</td><td>0,93</td></tr>
<tr><td>${m('a\\ (\\mathrm{m/s^2})')}</td><td></td><td></td><td></td><td></td><td></td></tr></table>
</div>${H.xeLan()}</div>
<div class="card" style="margin-top:.6mm;padding:1mm 3mm">
<div>Dự đoán (bỏ ma sát): ${m('a=m_2g/(m_1+m_2)=')} ${f(12)}&nbsp;${u('\\mathrm{m/s^2}')} · ${m('a')} đo trung bình ${f(12)}&nbsp;${u('\\mathrm{m/s^2}')}</div>
<div>Cả 5 lần lệch một phía ⇒ sai số ${f(25)}; do ${f(40)}</div></div>
${h3(2, 'III · Bốn cái bẫy', '4·2')}
<div class="card fig-side" style="${fs(33)};padding:1mm 3mm"><div>
<div class="trap">${ck}<span><b>Thiếu/thừa lực.</b> Không có “lực đà”: mỗi lực do một vật gây ra. Hộp trượt lên, tay đã buông, chịu các lực ${f(30)}</span></div>
<div class="trap">${ck}<span><b>${m('N=mg')} mọi lúc.</b> Mặt ngang kéo xiên: ${m('N=')} ${f(25)} · mặt nghiêng: ${m('N=')} ${f(20)}</span></div>
<div class="trap">${ck}<span><b>Đổi chiều dương giữa chừng.</b> Vật quay đầu: ${f(12)} đổi dấu, ${f(12)} không đổi dấu.</span></div>
<div class="trap">${ck}<span><b>Ma sát nghỉ cũng tính ${m('\\mu N')}.</b> Tủ ${u('50\\ \\mathrm{kg}')} bị đẩy ngang ${u('120\\ \\mathrm N')} vẫn đứng yên, ${u('\\mu_n=0{,}4')}, ${g10}: ${u('F_{\\mathrm{ms}}=')} ${f(12)}&nbsp;N, mức trần ${f(12)}&nbsp;N</span></div></div>
${H.hopLen()}</div>
${h3(3, 'IV · Trả bài 6 câu', '4·3')}
${box(`${tb('1. Bốn bước giải bài toán động lực học là gì?')}${lines(1)}
${tb('2. Đại lượng nào nối lực với chuyển động? Hai loại bài toán?')}${lines(1)}
${tb(`3. Mặt nghiêng góc ${al}: chọn trục thế nào, ${m('N')} bằng bao nhiêu, ${m('a')} khi trượt xuống?`)}${lines(1)}
${tb(`4. Kéo xiên lên góc ${al} trên mặt ngang: áp lực bằng bao nhiêu?`)}${lines(1)}
${tb('5. Hai vật nối dây qua ròng rọc: chung những gì, chiều dương chọn ra sao?')}${lines(1)}
${tb(`6. Khi nào được dùng ${m('F_{\\mathrm{ms}}=\\mu N')}?`)}${lines(1)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/6 câu · chưa thuộc: ${f(25)} ${nw(`→ đọc lại ô ${f(12)} Tập`)}</div>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TẬP VỀ NHÀ · THỬ THÁCH · MANG VỀ')}
${K.btvn()}
${h3(2, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '5·2')}
${rkHai([1, 2, 3], [4, 5, 6])}
${h3(3, 'Thử thách phân tầng', '5·3')}
<div class="fig-side" style="${fs(44)}">${box(cau(`${m('\\bigstar')} Vật trượt không ma sát, từ nghỉ, trên dốc ${u('30^\\circ')} (${u('\\sin 30^\\circ=0{,}5')}), ${g10}. Gia tốc? Tốc độ sau ${u('2\\ \\mathrm s')}?`, 2)
 + cau(`${m('\\bigstar\\bigstar')} <b>Bài toán ngược.</b> Ô tô ${u('1000\\ \\mathrm{kg}')} đang chạy ${u('20\\ \\mathrm{m/s}')} thì phanh gấp, trượt ${u('40\\ \\mathrm m')} rồi dừng (đường ngang, ${g10}). Lực hãm? Hệ số ma sát trượt?`, 2)
 + cau(`${m('\\bigstar\\bigstar\\bigstar')} <b>Vật chồng.</b> Ván ${u('2\\ \\mathrm{kg}')} trên sàn nhẵn, khối ${u('1\\ \\mathrm{kg}')} đặt trên ván, hệ số ma sát khối–ván ${u('0{,}3')} (nghỉ và trượt như nhau), ${g10}. Kéo ván ngang ${u('6\\ \\mathrm N')}: khối có trượt trên ván không? Kéo ${u('12\\ \\mathrm N')} thì sao?`, 4))}${H.vatChong()}</div>
${h3(4, 'VI · Mang về: điều em dễ quên nhất', '5·4')}
${box(wl('1.', 2) + wl('2.', 2) + wl('3.', 2))}
${foot(5)}</section>`;

// Hình đặt cạnh đề (không cạnh ô giải) để dòng giải chạy hết bề ngang — thầy chốt "Giải cần ≥ 2 dòng rộng 130 mm mỗi ý".
const deH = (s, fig, w = 42) => `<div class="fig-side" style="grid-template-columns:1fr ${w}mm"><div>${s}</div>${fig()}</div>`;
const dang = [
  { t: 'Dạng 1 · Dễ → Trung bình · Mặt ngang: kéo ngang rồi kéo xiên',
    de: deH(`Thùng ${u('30\\ \\mathrm{kg}')} đứng yên trên sàn ngang; hệ số ma sát trượt ${u('0{,}25')}; ${g10}. Kéo bằng lực ${u('120\\ \\mathrm N')}.<br><b>a)</b> kéo <b>nằm ngang</b>: phản lực ${m('N')}<br><b>b)</b> kéo nằm ngang: gia tốc<br><b>c)</b> kéo bằng dây chếch lên ${u('37^\\circ')} (${u('\\sin 37^\\circ=0{,}6')}; ${u('\\cos 37^\\circ=0{,}8')}): phản lực ${m('N')}<br><b>d)</b> kéo chếch ${u('37^\\circ')}: gia tốc`, H.d2),
    nd: `Oy cho ${m('N')}: kéo xiên thì ${m('N=mg-')} ${f(16)}; Ox chỉ lấy ${f(16)}`, a: ['a', 'b', 'c', 'd'], gi: 7 },
  { t: 'Dạng 2 · Trung bình · Vật trượt xuống mặt phẳng nghiêng',
    de: deH(`Vật ${u('2{,}0\\ \\mathrm{kg}')} trượt từ nghỉ ở đỉnh dốc dài ${u('10\\ \\mathrm m')}, nghiêng ${u('30^\\circ')} (${u('\\sin 30^\\circ=0{,}5')}; ${u('\\cos 30^\\circ\\approx 0{,}866')}); ${u('\\mu=0{,}1')}; ${g10}.<br><b>a)</b> phản lực ${m('N')}<br><b>b)</b> gia tốc<br><b>c)</b> tốc độ ở chân dốc<br><b>d)</b> thời gian trượt hết dốc`, H.d3),
    nd: `Ox dọc dốc: ${m('a=g(')} ${f(16)} ${m('-')} ${f(16)}${m(')')}`, a: ['a', 'b', 'c', 'd'], gi: 6 },
  { t: 'Dạng 3 · Khó · Bài toán ngược: từ chuyển động tìm lực',
    de: deH(`Ô tô ${u('1200\\ \\mathrm{kg}')} đang chạy ${u('15\\ \\mathrm{m/s}')} trên đường ngang thì phanh gấp, bánh trượt ${u('22{,}5\\ \\mathrm m')} rồi dừng; ${g10}.<br><b>a)</b> gia tốc (chiều dương là chiều chạy)<br><b>b)</b> độ lớn lực hãm<br><b>c)</b> hệ số ma sát trượt lốp–đường`, H.d4),
    nd: `tìm ${m('a')} trước từ ${m('v^2-v_0^2=')} ${f(16)}; rồi ${m('F_{\\text{hãm}}=')} ${f(16)}; ${m('\\mu=')} ${f(16)}`, a: ['a', 'b', 'c'], gi: 4 },
  { t: 'Dạng 4 · Khó · Hai vật nối dây qua ròng rọc (bài toán mẫu)',
    de: deH(`Khối gỗ ${u('m_1=2\\ \\mathrm{kg}')} trên bàn ngang, nối dây nhẹ không dãn vắt qua ròng rọc ở mép bàn với quả nặng ${u('m_2=1\\ \\mathrm{kg}')} treo thẳng đứng. Hệ số ma sát gỗ–bàn ${u('0{,}2')} (nghỉ và trượt như nhau). Thả hệ từ nghỉ; bỏ qua khối lượng, ma sát ròng rọc; ${g10}.<br><b>a)</b> giả sử hệ đứng yên: ma sát nghỉ cần có, mức trần ${m('\\mu m_1g')}; hệ có chạy không<br><b>b)</b> gia tốc của hệ<br><b>c)</b> lực căng dây<br><b>d)</b> quãng đường quả nặng đi được sau ${u('1\\ \\mathrm s')}`, H.d5, 40),
    nd: `cùng ${m('a')}, cùng ${m('T')}; cộng hai phương trình: ${nw(`${m('a=')} ${ps(40)}`)}; kiểm ${m('T')} ${ck}${m('\\lt P_2')} ${ck}${m('\\gt P_2')}`, a: ['a', 'b', 'c', 'd'], gi: 6, cot: 2 },
];

// Bài tương tự giải vào vở (thầy chốt 10/11): ô đáp số 25 mm cuối đúng dòng của ý; nhãn a₁, a₂ khi ý có 2 kết quả. Đáp số tính bằng Python 13/11/2026.
const oY = (s, o, w = 25) => s.split('<br>').map((p) => {
  const y = p.match(/^<b>([a-d])\)<\/b>/);
  if (!y) return `<div>${p}</div>`;
  const ls = o.filter((l) => l[0] === y[1]);
  return `<div class="yo"><span>${p}</span><span class="oo">${ls.map((l) => `<span class="nw"><b>${l})</b>${f(w)}</span>`).join('')}</span></div>`;
}).join('');
const ttDe = (b) => b.fig ? `<div class="fig-side" style="grid-template-columns:1fr ${b.fw}mm"><div>${oY(b.de, b.o, b.ow)}</div>${b.fig}</div>` : oY(b.de, b.o, b.ow);
const vaoVo = (ds) => ds.map((b) => (b.o ? { t: b.t, de: ttDe(b), k: 0 } : b));
const nhap = (n) => ({ t: '<span class="nhap-t">Nháp / chỗ em còn vướng</span>', de: lines(n), k: 0 });
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–2', 'DẠNG 3–4'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Kéo hộp ${u('10\\ \\mathrm{kg}')} trên sàn ngang bằng lực <b>nằm ngang</b> ${u('40\\ \\mathrm N')}; ${u('\\mu=0{,}3')}; ${g10}; từ nghỉ.<br><b>a)</b> lực ma sát trượt<br><b>b)</b> gia tốc<br><b>c)</b> quãng đường sau ${u('2\\ \\mathrm s')}`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 1 · Bài 2', de: `Kéo vali ${u('12\\ \\mathrm{kg}')} trên sàn ngang bằng dây chếch lên ${u('60^\\circ')} (${u('\\sin 60^\\circ\\approx 0{,}866')}; ${u('\\cos 60^\\circ=0{,}5')}), lực ${u('40\\ \\mathrm N')}; ${u('\\mu=0{,}1')}; ${g10}.<br><b>a)</b> phản lực ${m('N')}<br><b>b)</b> gia tốc<br><b>c)</b> gia tốc nếu kéo nằm ngang cùng ${u('40\\ \\mathrm N')}`, fig: H.t22(), fw: 40, o: ['a', 'b', 'c'] },
    { t: 'Dạng 2 · Bài 1', de: `Vật trượt từ nghỉ xuống hết dốc dài ${u('8{,}0\\ \\mathrm m')} nghiêng ${u('37^\\circ')} (${u('\\sin 37^\\circ=0{,}6')}; ${u('\\cos 37^\\circ=0{,}8')}); ${u('\\mu=0{,}25')}; ${g10}.<br><b>a)</b> gia tốc<br><b>b)</b> tốc độ ở chân dốc<br><b>c)</b> thời gian trượt`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 2 · Bài 2', de: `Đẩy viên đá lên dốc băng nghiêng ${u('30^\\circ')} (${u('\\sin 30^\\circ=0{,}5')}; bỏ ma sát) với tốc độ đầu ${u('10\\ \\mathrm{m/s}')}; chiều dương hướng lên dốc; ${g10}.<br><b>a)</b> gia tốc (có dấu)<br><b>b)</b> quãng đường lên tới điểm cao nhất<br><b>c)</b> thời gian đi lên`, fig: H.t32(), fw: 40, o: ['a', 'b', 'c'] },
    nhap(6),
  ], [
    { t: 'Dạng 3 · Bài 1', de: `Ô tô ${u('1000\\ \\mathrm{kg}')} đang chạy ${u('10\\ \\mathrm{m/s}')} trên đường ngang thì hãm phanh, dừng sau ${u('5{,}0\\ \\mathrm s')}.<br><b>a)</b> gia tốc (chiều dương là chiều chạy)<br><b>b)</b> độ lớn lực hãm<br><b>c)</b> quãng đường từ lúc hãm tới lúc dừng`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 3 · Bài 2', de: `Ô tô ${u('800\\ \\mathrm{kg}')} khởi hành từ nghỉ trên đường ngang, sau ${u('10\\ \\mathrm s')} đạt ${u('20\\ \\mathrm{m/s}')}; lực cản tổng cộng ${u('400\\ \\mathrm N')}.<br><b>a)</b> gia tốc<br><b>b)</b> lực kéo của động cơ<br><b>c)</b> quãng đường trong ${u('10\\ \\mathrm s')} đó`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 4 · Bài 1', de: `Khối ${u('m_1=3{,}0\\ \\mathrm{kg}')} trên bàn ngang nối dây nhẹ không dãn qua ròng rọc nhẹ ở mép bàn với quả nặng ${u('m_2=2{,}0\\ \\mathrm{kg}')} treo; ${u('\\mu=0{,}2')} (nghỉ và trượt như nhau); thả từ nghỉ; ${g10}.<br><b>a)</b> gia tốc của hệ<br><b>b)</b> lực căng dây<br><b>c)</b> quãng đường sau ${u('2\\ \\mathrm s')}`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 4 · Bài 2', de: `Khối ${u('m_1=4{,}0\\ \\mathrm{kg}')} trên bàn ngang nối dây nhẹ không dãn qua ròng rọc nhẹ ở mép bàn với quả nặng ${u('m_2=1{,}0\\ \\mathrm{kg}')} treo; ${u('\\mu=0{,}3')} (nghỉ và trượt như nhau); thả từ nghỉ; ${g10}.<br><b>a)</b> giả sử đứng yên: ma sát nghỉ cần có; mức trần ${m('\\mu m_1g')}<br><b>b)</b> hệ có chuyển động không; gia tốc<br><b>c)</b> lực ma sát lúc đó`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'] },
    nhap(9),
  ]],
  dap: [
    `D1·1: a) 30 N · b) 1,0 m/s² · c) 2,0 m &nbsp;|&nbsp; D1·2: a) 85,4 N · b) 0,955 m/s² · c) 2,33 m/s² &nbsp;|&nbsp; D2·1: a) 4,0 m/s² · b) 8,0 m/s · c) 2,0 s &nbsp;|&nbsp; D2·2: a) −5,0 m/s² · b) 10 m · c) 2,0 s`,
    `D3·1: a) −2,0 m/s² · b) 2000 N · c) 25 m &nbsp;|&nbsp; D3·2: a) 2,0 m/s² · b) 2000 N · c) 100 m &nbsp;|&nbsp; D4·1: a) 2,8 m/s² · b) 14,4 N · c) 5,6 m &nbsp;|&nbsp; D4·2: a<sub>1</sub>) 10 N · a<sub>2</sub>) 12 N · b<sub>1</sub>) không (đứng yên) · b<sub>2</sub>) a = 0 · c) 10 N (ma sát nghỉ)`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [2, 2], kq: [[1, 2], [3, 4]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'bốn bước 1·5 · cầu nối a 2·1 · mặt ngang, kéo xiên 2·2 · mặt nghiêng 3·1 · hai vật nối dây 3·4 · đo thử 4·1 · bẫy 4·2 · dạng 1–2 → 6·1 · dạng 3–4 → 7·1',
  out: process.argv[2],
});
