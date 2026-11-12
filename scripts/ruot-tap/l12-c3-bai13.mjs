// Ruột tập VL12 – Chương 3 · Bài 13 · Đại cương về dòng điện xoay chiều (lesson id 14). Quyển Chương 3 lớp 12: bài 9 = tr. 1–12 → bài 13 = tr. 49–60.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Tên file có '-c3-' vì Chương 4 L12 đã có bai14–18.mjs. Hình: hinh-l12-c3-bai13.mjs (toàn bộ SVG tự vẽ).
// Nội dung theo bài web (book/cache/14.json, tải từ DB 12/11/2026): mục tiêu, dự đoán đỉnh ổ điện, II.1 khung quay, máy phát mini,
// II.2 biểu thức u/i + T, f, ω, hai LED ngược chiều, II.3 hiệu dụng, hai bẫy, Trả bài 5 câu, bài toán mẫu viết biểu thức i,
// thử thách ⭐–⭐⭐⭐, 5 dạng bài tập mẫu. Đáp số Bài tương tự (tuongTu.dap) tính bằng Python 12/11/2026.
// Chạy: node scripts/ruot-tap/l12-c3-bai13.mjs [file.pdf]   → scripts/ruot-tap/out/ruot-tap-vl12-c3-bai13.pdf
//       node scripts/ruot-tap/l12-c3-bai13.mjs --hinh       → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l12-c3-bai13/ để soát chữ/nét
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL12c3b13 as H } from './hinh-l12-c3-bai13.mjs';
const HERE = dirname(fileURLToPath(import.meta.url));

if (process.argv[2] === '--hinh') {
  const { createRequire } = await import('node:module');
  const { existsSync, mkdirSync, writeFileSync } = await import('node:fs');
  const { pathToFileURL } = await import('node:url');
  const BOOK = [resolve(HERE, '../../book/'), '/Users/MAC/Projects/thachlab/book'].find((d) => existsSync(d + '/node_modules')) + '/';
  const puppeteer = createRequire(BOOK + 'package.json')('puppeteer-core');
  const F = resolve(HERE, 'fonts') + '/source-sans-3-';
  const css = ['latin', 'latin-ext', 'vietnamese'].flatMap((s) => [400, 700].map((w) => `@font-face{font-family:BV;font-weight:${w};src:url("${pathToFileURL(`${F}${s}-${w}-normal.woff2`).href}")}`)).join('')
    + 'body{margin:0;font-family:BV,sans-serif;zoom:4}.fig{margin:0;width:46mm;border:.3mm solid #d3dbec;border-radius:1.5mm;padding:1mm 1.5mm .6mm;background:#fff}.fig svg{display:block;width:100%;height:auto}figcaption{font-size:2.95mm;color:#5f6a88;line-height:1.3;margin-top:.4mm}';
  const out = resolve(HERE, 'out/hinh-l12-c3-bai13'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 13, lid: 14, lop: 12, baiDau: 9, ten: 'ĐẠI CƯƠNG VỀ DÒNG ĐIỆN XOAY CHIỀU', sub: 'Vật lí 12 · Chương 3: Từ trường' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const tall = (w, h = 9) => `<span class="fill" style="min-width:${w}mm;height:${h}mm"></span>`;
const PI = '<span style="font-family:KaTeX_Math;font-style:italic">π</span>';
const om = m('\\omega'), ph = m('\\varphi'), Phi = m('\\Phi'), r2 = m('\\sqrt2');
const V = (s) => nw(m(`${s}\\ \\mathrm V`)), A = (s) => nw(m(`${s}\\ \\mathrm A`)), Om = (s) => nw(m(`${s}\\ \\Omega`)), Hz = (s) => nw(m(`${s}\\ \\mathrm{Hz}`));

// Bài tương tự 1 cột, ô đáp số cuối dòng của ý (cùng cách l11-bai16).
const ttCss = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';

const p1 = `${ttCss}<section class="page">
${head('BÀI 13 · ĐẠI CƯƠNG VỀ DÒNG ĐIỆN XOAY CHIỀU', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Giải thích vì sao <b>khung dây quay</b> trong từ trường sinh ra điện xoay chiều`)}
${dong(`${ck}Đọc và viết biểu thức ${m('u')}, ${m('i')} theo thời gian; tính ${m('T')}, ${m('f')}, ${om}`)}
${dong(`${ck}Hiểu <b>giá trị hiệu dụng</b>; đổi qua lại giữa giá trị hiệu dụng và cực đại`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Ổ điện nhà em ghi 220 V – 50 Hz. Nối dao động ký vào hai lỗ ổ cắm. Đỉnh cao nhất của sóng điện áp khoảng:</p>
<div class="fig-side" style="${fs(44)}"><div>
${opt('A', 'Đúng 220 V')}
${opt('B', 'Khoảng 311 V')}
${opt('C', 'Khoảng 156 V')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 1)}</div>
${H.oDien()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Khung dây quay trong từ trường', '1·4')}
<div class="card fig-side" style="${fs(44)};padding:1.2mm 3mm"><div>
<div>Khung ${m('N')} vòng, diện tích ${m('S')}, quay đều ${m('n')} vòng/s quanh trục vuông góc ${m('\\vec B')}: ${nw(`${om} = ${f(16)}`)}</div>
<div>Góc giữa pháp tuyến ${m('\\vec n')} và ${m('\\vec B')}: ${nw(`${m('\\alpha=')} ${f(18)}`)}; ${ph} là góc lúc ${f(14)}</div>
<div>Từ thông: ${nw(`${m('\\Phi=')} ${f(28)}`)}, với ${nw(`${m('\\Phi_0=')} ${f(14)}`)}</div>
<div>Faraday: ${nw(`${m("e=-\\Phi'=")} ${f(24)}`)}${m('\\sin(\\omega t+\\varphi)')}</div>
<div style="margin:1mm 0;display:flex;align-items:flex-end;gap:2mm;flex-wrap:wrap">${m('e=')} ${tall(36)} <span>với ${nw(`${m('E_0=')} ${f(16)}`)}</span></div>
<div>${m('e')} ${f(10)} pha ${f(10)} so với ${Phi}.</div></div>
${H.khungQuay()}</div>
${h3(5, 'Làm nhanh', '1·5')}
${box(`<div class="yo" style="padding-top:1mm"><span>Khung ${m('N=50')} vòng, ${nw(m('S=100\\ \\mathrm{cm^2}'))}, quay 10 vòng/s trong ${nw(m('B=0{,}2\\ \\mathrm T'))} (trục vuông góc ${m('\\vec B')}). Tìm ${m('E_0')}.</span><span class="oo"><span class="nw"><b>${m('E_0=')}</b>${f(20)}</span></span></div>${lines(1)}`)}
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('MÁY PHÁT MINI · BIỂU THỨC u, i')}
${h3(1, 'Thí nghiệm đo: máy phát mini quay tay', '2·1')}
<div class="card fig-side" style="${fs(42)};padding:1.2mm 3mm"><div>
<div><b>Làm:</b> nối máy phát mini (một cặp cực) với dao động ký; quay đều ${m('n=2, 4, 6, 8, 10')} vòng/s, đọc biên độ ${m('U_0')}.</div>
<table class="tbl-ct" style="margin:.6mm 0"><tr><th>${m('n')} (vòng/s)</th><th>2</th><th>4</th><th>6</th><th>8</th><th>10</th></tr>
<tr><td>${m('U_0')} (V)</td><td>0,95</td><td>1,82</td><td>2,84</td><td>3,67</td><td>4,70</td></tr>
<tr><td>${m('U_0/n')} (V·s)</td><td>0,475</td><td></td><td></td><td></td><td></td></tr></table>
<div><b>Quan sát:</b> quay càng nhanh, sóng càng ${f(14)} và càng ${f(14)}</div>
<div><b>Rút ra:</b> ${m('U_0/n')} ${f(20)} nên ${m('U_0')} tỉ lệ ${f(14)} với ${m('n')}, khớp ${nw(`${m('E_0=')} ${f(14)}`)}. Mỗi vòng quay cho một chu kì: ${nw(`${m('f=')} ${f(10)}`)}</div>
<div><b>Sai số:</b> đếm vòng trong 1 s lệch ±1 vòng. Cách giảm:</div>${lines(1)}</div>
${H.mayPhat()}</div>
${h3(2, 'II.2 · Biểu thức dòng điện và điện áp xoay chiều', '2·2')}
<div class="card" style="padding:1.2mm 3mm">
<div style="display:flex;gap:6mm;align-items:flex-end;margin-bottom:.8mm"><span>${m('u=')} ${tall(36)}</span><span>${m('i=')} ${tall(36)}</span></div>
<table><tr><th style="width:32mm">Đại lượng</th><th>Nghĩa</th></tr>
<tr><td>${m('u')}, ${m('i')}</td><td></td></tr><tr><td>${m('U_0')}, ${m('I_0')} (luôn ${m('>0')})</td><td></td></tr>
<tr><td>${m('\\omega t+\\varphi')}; ${ph}</td><td></td></tr></table>
</div>
${h3(3, 'Tần số góc · chu kì · tần số', '2·3')}
<div class="card" style="padding:1.2mm 3mm">
<div style="display:flex;gap:6mm;align-items:flex-end;flex-wrap:wrap"><span>${m('\\omega=')} ${f(16)}</span><span>${m('T=')} ${tall(16)} ${m('=')} ${tall(16)}</span></div>
<div>Điện lưới Việt Nam ${Hz('f=50')}: ${nw(`${om} = ${f(16)}`)} rad/s · ${nw(`${m('T=')} ${f(14)}`)} s</div>
<div>Mỗi chu kì dòng điện đổi chiều ${f(8)} lần ⇒ 1 s đổi chiều ${f(10)} lần; ổ điện nhà em: ${f(12)} lần/s.</div>
</div>
${h3(4, 'Làm nhanh', '2·4')}
${box(`<div style="padding-top:1mm;line-height:1.35"><b>Câu 1.</b> ${nw(m('i=4\\cos\\left(100\\pi t-\\dfrac{\\pi}{3}\\right)\\ \\mathrm A'))}. Tìm:</div>
<div class="yo"><span><b>a)</b> tần số ${m('f')} và chu kì ${m('T')}</span><span class="oo"><span class="nw"><b>f =</b>${f(16)}</span><span class="nw"><b>T =</b>${f(16)}</span></span></div>
<div class="yo"><span><b>b)</b> pha ban đầu; số lần đổi chiều trong 1 s (từ giây thứ hai)</span><span class="oo"><span class="nw"><b>${ph} =</b>${f(14)}</span><span class="nw"><b>số lần</b>${f(12)}</span></span></div>${lines(1)}`)}
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('HAI LED NGƯỢC CHIỀU · GIÁ TRỊ HIỆU DỤNG')}
${h3(1, 'Thí nghiệm: hai đèn LED mắc ngược chiều', '3·1')}
<div class="card fig-side" style="${fs(42)};padding:1.2mm 3mm"><div>
<div><b>Làm:</b> máy phát tín hiệu nối hai LED mắc song song, ngược chiều, qua điện trở bảo vệ. Chỉnh ${Hz('f=1')}, rồi tăng dần lên ${Hz('50')}. Mỗi LED chỉ cho dòng đi qua theo một chiều.</div>
<div><b>Quan sát:</b> ở 1 Hz: ${f(44)}</div>
<div>ở 50 Hz: ${f(52)}</div>
<div><b>Rút ra:</b> mỗi chu kì, mỗi LED sáng ${f(8)} lần ⇒ dòng đổi chiều ${f(8)} lần. Mắt không theo kịp ${f(10)} lần đổi chiều mỗi giây nên thấy đèn sáng đều.</div>
<div><b>Lưu ý:</b> nếu lúc ${m('t=0')} có ${m('i=0')} (${nw(m('\\varphi=\\pm\\dfrac{\\pi}{2}'))}) thì giây đầu tiên chỉ đổi chiều ${f(14)} lần, vì điểm ${m('t=0')} không tính.</div></div>
${H.haiLed()}</div>
${h3(2, 'II.3 · Giá trị hiệu dụng', '3·2')}
<div class="card fig-side" style="${fs(44)};padding:1.2mm 3mm"><div>
<div>Trung bình của ${m('i')} trong một chu kì bằng ${f(8)}, nhưng dây vẫn nóng: nhiệt tỉ lệ với ${f(12)}.</div>
<div><b>Cường độ hiệu dụng ${m('I')}</b>: cường độ của dòng ${f(20)} khi qua cùng điện trở, trong cùng thời gian thì toả ${f(24)} dòng xoay chiều.</div>
<div style="display:flex;gap:4mm;align-items:flex-end;margin:1mm 0;flex-wrap:wrap"><span>${m('I=')} ${tall(14, 10)}</span><span>${m('U=')} ${tall(14, 10)}</span><span>${m('E=')} ${tall(14, 10)}</span></div>
<div>Ampe kế, vôn kế xoay chiều và số ghi trên thiết bị đều là giá trị ${f(18)}.</div>
<div><b>Vì sao ${r2}:</b> trung bình của ${m('\\cos^2')} trong một chu kì là ${m('\\tfrac12')} ⇒ ${nw(`${m('P=R\\,\\overline{i^2}=')} ${f(16)}`)}; đặt bằng ${m('RI^2')} ⇒ ${nw(`${m('I^2=')} ${f(12)}`)}</div></div>
${H.dienAp()}</div>
${h3(3, 'Làm nhanh', '3·3')}
${box(cau(`<b>Câu 2.</b> Dòng xoay chiều hiệu dụng ${A('2')} và dòng không đổi ${A('2')} cùng chạy qua một điện trở trong cùng thời gian. Dòng nào toả nhiệt nhiều hơn? Vì sao?`, 1)
 + `<div style="padding-top:1mm;line-height:1.35"><b>Câu 3.</b> Dòng ${nw(m('i=2\\cos(100\\pi t)\\ \\mathrm A'))} chạy qua ${Om('R=10')}.</div>
<div class="yo"><span>Cường độ hiệu dụng ${m('I')} và công suất toả nhiệt ${m('P')} của ${m('R')}</span><span class="oo"><span class="nw"><b>I =</b>${f(16)}</span><span class="nw"><b>P =</b>${f(14)}</span></span></div>${lines(1)}
<div class="yo" style="padding-top:1mm"><span><b>Câu 4.</b> Vôn kế xoay chiều đo ổ điện chỉ ${V('220')}. Điện áp cực đại ${m('U_0')} bằng bao nhiêu?</span><span class="oo"><span class="nw"><b>${m('U_0=')}</b>${f(20)}</span></span></div>`)}
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('HAI CÁI BẪY · TRẢ BÀI · TỰ KIỂM TRA')}
${h3(1, 'III · Bẫy 1: lẫn tức thời, cực đại, hiệu dụng', '4·1')}
<table><tr><th style="width:30mm">Giá trị</th><th>Là gì · dùng khi nào</th></tr>
<tr><td>Tức thời ${m('u, i')}</td><td></td></tr><tr><td>Cực đại ${m('U_0, I_0')}</td><td></td></tr>
<tr><td style="height:9mm">Hiệu dụng ${m('U, I')}</td><td></td></tr><tr><td>Trung bình</td><td></td></tr></table>
${h3(2, 'Bẫy 2: “từ thông cực đại thì suất điện động cực đại”', '4·2')}
<div class="fig-side" style="${fs(44)}"><div>
<table><tr><th>Khung ở vị trí</th><th style="width:15mm">${Phi}</th><th style="width:15mm">${m('e')}</th></tr>
<tr><td>mặt khung vuông góc ${m('\\vec B')} (${m('\\vec n\\parallel\\vec B')})</td><td></td><td></td></tr>
<tr><td>mặt khung song song ${m('\\vec B')} (${m('\\vec n\\perp\\vec B')})</td><td></td><td></td></tr></table>
<div style="margin-top:.6mm">Vì ${m("e=-\\Phi'")}: lúc ${Phi} đạt đỉnh, đồ thị ${Phi} nằm ngang, độ dốc ${f(10)} nên ${nw(`${m('e=')} ${f(10)}`)}</div></div>
${H.phiE()}</div>
${h3(3, 'IV · Trả bài 5 câu', '4·3')}
${box(`${tb('1. Vì sao khung quay trong từ trường sinh ra điện xoay chiều?')}${lines(2)}
${tb(`2. Viết biểu thức ${m('i')}, nêu tên từng đại lượng.`)}${lines(2)}
${tb(`3. Liên hệ ${m('T')}, ${m('f')}, ${om}? Lưới 50 Hz đổi chiều mấy lần mỗi giây?`)}${lines(1)}
${tb('4. Cường độ hiệu dụng là gì? Vì sao không dùng giá trị trung bình?')}${lines(2)}
${tb(`5. ${Phi} và ${m('e')} lệch pha bao nhiêu? Khi ${m('e')} cực đại, khung nằm ở đâu?`)}${lines(1)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/5 câu · chưa thuộc: ${f(25)} ${nw(`→ đọc lại ô ${f(12)} Tập`)}</div>
${h3(4, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '4·4')}
${rkHai([1, 2, 3, 4], [5, 6, 7])}
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TOÁN MẪU · BÀI TẬP VỀ NHÀ · THỬ THÁCH')}
${h3(1, 'V · Bài toán mẫu: viết biểu thức dòng điện', '5·1')}
<div class="card soft" style="padding:1.2mm 3mm">Dòng điện xoay chiều có tần số ${Hz('50')} và cường độ hiệu dụng ${A('2')}. Tại ${m('t=0')}, cường độ tức thời là ${A('2')} và đang giảm.<br><b>a)</b> Viết biểu thức ${m('i')}.<br><b>b)</b> Cho dòng này chạy qua ${Om('R=25')} trong 1 phút: nhiệt lượng toả ra?</div>
<table><tr><th style="width:42mm">Câu trong đề</th><th>Dữ liệu → kiến thức</th></tr>
<tr><td>“tần số 50 Hz”</td><td>${Hz('f=50')} → ${m('\\omega=2\\pi f')}</td></tr>
<tr><td style="height:6.5mm">“hiệu dụng 2 A”</td><td></td></tr>
<tr><td style="height:6.5mm">“${m('t=0')}, ${m('i=2')} A”</td><td></td></tr>
<tr><td style="height:6.5mm">“đang giảm”</td><td></td></tr>
</table>
<div class="fig-side" style="${fs(44)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl(`${om} = ……, ${m('I_0=')} …… ; thế ${m('t=0')}: ${m('\\cos\\varphi=')}`, 1)}${wl(`Đang giảm ⇒ ${m("i'(0)")} …… 0 ⇒ ${m('\\sin\\varphi')} …… 0 ⇒ ${m('\\varphi=')}`, 1)}${wl(`a) ${m('i=')}`, 1)}${wl(`b) ${m('Q=')}`, 1)}</div>${H.iMau()}</div>
${h3(2, 'Điền bước còn thiếu: cùng đề, chỉ đổi thành “đang tăng”', '5·2')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div class="ln"><b>Bước 1 (cho sẵn):</b> ${m('\\omega=100\\pi')} rad/s, ${m('I_0=2\\sqrt2')} A, ${m('\\cos\\varphi=\\tfrac{1}{\\sqrt2}')}</div>
${wl(`Bước 2: đang tăng ⇒ ${m('\\sin\\varphi')} …… 0 ⇒ ${m('\\varphi=')}`, 1)}${wl(`Bước 3: ${m('i=')}`, 1)}</div>
${K.btvn().replace('<i>1</i>', '<i>3</i>')}
${h3(4, 'Thử thách phân tầng', '5·4')}
${box(`<div class="yo" style="padding-top:1mm"><span>${m('\\bigstar')} ${nw(m('u=100\\sqrt2\\cos(100\\pi t)\\ \\mathrm V'))}. Tìm ${m('U')}, ${m('f')}, ${m('T')}.</span><span class="oo"><span class="nw"><b>U =</b>${f(12)}</span><span class="nw"><b>f =</b>${f(12)}</span><span class="nw"><b>T =</b>${f(12)}</span></span></div>
 ${cau(`${m('\\bigstar\\bigstar')} Khung ${m('N=100')} vòng, ${nw(m('S=200\\ \\mathrm{cm^2}'))}, quay 50 vòng/s trong từ trường đều ${nw(m('B=0{,}1\\ \\mathrm T'))} (trục vuông góc ${m('\\vec B')}). Tìm ${m('E_0')} và ${m('E')}.`, 1)}
 ${cau(`${m('\\bigstar\\bigstar\\bigstar')} Đèn chỉ sáng khi ${nw(m('|u|\\ge110\\sqrt2\\ \\mathrm V'))}, mắc vào ${nw(m('u=220\\sqrt2\\cos(100\\pi t)\\ \\mathrm V'))}. Mỗi giây đèn sáng bao lâu?`, 1)}`)}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Đọc các đại lượng từ biểu thức của điện áp',
    de: `Điện áp tức thời giữa hai đầu một thiết bị là ${nw(m('u=20\\sqrt2\\cos(40\\pi t+\\tfrac{\\pi}{3})\\ \\mathrm V'))} (${m('t')} tính bằng s).<br><b>a)</b> điện áp hiệu dụng ${m('U')} và pha ban đầu ${m('\\varphi_u')}<br><b>b)</b> tần số góc ${om}, tần số ${m('f')}, chu kì ${m('T')}<br><b>c)</b> điện áp tức thời tại ${m('t=0')}`,
    nd: `${nw(`${m('U_0=')} ${f(16)}`)}; ${nw(`${m('U=')} ${f(16)}`)}; ${nw(`${m('f=')} ${f(16)}`)}`,
    a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'b<sub>3</sub>', 'c'], cot: 6, gi: 3 },
  { t: 'Dạng 2 · Trung bình · Công suất và nhiệt lượng toả ra trên điện trở',
    de: `Dòng điện ${nw(m('i=4\\cos(100\\pi t-\\tfrac{\\pi}{6})\\ \\mathrm A'))} chạy qua điện trở ${Om('R=25')}.<br><b>a)</b> công suất toả nhiệt trung bình của ${m('R')}<br><b>b)</b> nhiệt lượng toả ra trong 2 phút<br><b>c)</b> cường độ dòng không đổi toả cùng nhiệt lượng trên ${m('R')} trong cùng thời gian`,
    nd: `${m('P=I^2R')} với ${m('I')} là giá trị ${f(18)}; 2 phút = ${f(10)} s`,
    a: ['a', 'b', 'c'], gi: 3 },
  { t: 'Dạng 3 · Khá · Viết biểu thức i từ f, I và giá trị lúc t = 0',
    de: `Dòng điện xoay chiều có tần số ${Hz('50')}, cường độ hiệu dụng ${A('2')}. Tại ${m('t=0')}, cường độ tức thời là ${nw(m('-\\sqrt2\\ \\mathrm A'))} và đang tăng.<br><b>a)</b> biểu thức của ${m('i')} (dạng hàm cos, ${m('t')} tính bằng s)<br><b>b)</b> cường độ tức thời tại ${nw(m('t=\\tfrac{1}{200}\\ \\mathrm s'))}`,
    nd: `${nw(`${m('\\cos\\varphi=')} ${f(16)}`)} ⇒ hai nghiệm ${m('\\pm')}; đang tăng ⇒ ${m("i'(0)>0")} ⇒ ${nw(`${m('\\sin\\varphi')} ${f(10)} 0`)}`,
    a: ['a', 'b'], cot: 2, gi: 3, fig: H.d3 },
  { t: 'Dạng 4 · Khá · Khung dây quay: từ thông và suất điện động',
    de: `Khung dây ${m('N=200')} vòng, diện tích mỗi vòng ${nw(m('S=100\\ \\mathrm{cm^2}'))}, quay đều 1500 vòng/phút quanh trục vuông góc với đường sức của từ trường đều ${nw(m('B=0{,}04\\ \\mathrm T'))}. Lúc ${m('t=0')}, pháp tuyến của khung cùng hướng ${m('\\vec B')}.<br><b>a)</b> tần số góc ${om} và từ thông cực đại ${m('\\Phi_0')}<br><b>b)</b> suất điện động cực đại ${m('E_0')} và hiệu dụng ${m('E')}<br><b>c)</b> biểu thức suất điện động ${m('e')} (V, s)`,
    nd: `Đổi ${nw(`${m('n=')} ${f(12)} vòng/s`)}, ${nw(`${m('S=')} ${f(14)} ${m('\\mathrm{m^2}')}`)}; ${m('e')} chậm pha ${f(10)} so với ${Phi}`,
    a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], cot: 2, gi: 4, fig: H.d4 },
  { t: 'Dạng 5 · Khó · Thời gian đèn sáng và thời điểm đèn tắt',
    de: `Bóng đèn chỉ sáng khi ${nw(m('|u|\\ge100\\sqrt3\\ \\mathrm V'))}. Đặt vào đèn ${nw(m('u=200\\cos(100\\pi t)\\ \\mathrm V'))}.<br><b>a)</b> trong một chu kì, đèn sáng tổng cộng bao nhiêu ms<br><b>b)</b> trong 1 s, đèn sáng tổng cộng bao lâu<br><b>c)</b> kể từ ${m('t=0')} (đèn đang sáng), đèn tắt lần đầu lúc nào (ms)`,
    nd: `${nw(`${m('|\\cos\\alpha|\\ge')} ${f(12)}`)}; mỗi chu kì đèn sáng ${f(8)} lần; ${m('\\Delta t=\\dfrac{\\Delta\\alpha}{\\omega}')}`,
    a: ['a', 'b', 'c'], gi: 5, fig: H.d5 },
];

// Bài tương tự: mỗi dạng 2 bài, giải vào vở (thầy chốt 10/11), ô đáp số cuối dòng của ý; đáp số tính bằng Python 12/11/2026.
const oY = (s, o, w = {}) => s.split('<br>').map((p) => {
  const y = p.match(/^<b>([a-d])\)<\/b>/);
  if (!y) return `<div>${p}</div>`;
  const ls = o.filter((l) => l[0] === y[1]);
  return `<div class="yo"><span>${p}</span><span class="oo">${ls.map((l) => `<span class="nw"><b>${l})</b>${f(typeof w === 'object' ? (w[l] ?? 22) : w)}</span>`).join('')}</span></div>`;
}).join('');
const ttDe = (b) => b.fig ? `<div class="fig-side" style="grid-template-columns:1fr ${b.fw}mm">${`<div>${oY(b.de, b.o, b.ow)}</div>`}${b.fig}</div>` : oY(b.de, b.o, b.ow);
const vaoVo = (ds) => ds.map((b) => (b.o ? { t: b.t, de: ttDe(b), k: 0 } : b));
const nhap = (n) => ({ t: '<span class="nhap-t">Nháp / chỗ em còn vướng</span>', de: lines(n), k: 0 });
const s1 = (k) => `<b>${k})</b>`;
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–3', 'DẠNG 4–5'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `${nw(m('u=110\\sqrt2\\cos\\left(100\\pi t-\\dfrac{\\pi}{6}\\right)\\ \\mathrm V'))} (${m('t')} tính bằng s).<br>${s1('a')} ${m('U')} và ${m('\\varphi_u')}<br>${s1('b')} ${om}, ${m('f')}, ${m('T')}<br>${s1('c')} ${m('u')} tại ${m('t=0')}`,
      o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'b<sub>3</sub>', 'c'], ow: 18 },
    { t: 'Dạng 1 · Bài 2', de: `${nw(m('i=6\\cos\\left(80\\pi t-\\dfrac{2\\pi}{3}\\right)\\ \\mathrm A'))} (${m('t')} tính bằng s).<br>${s1('a')} ${m('I')} và ${m('\\varphi_i')}<br>${s1('b')} ${om}, ${m('f')}, ${m('T')}<br>${s1('c')} ${m('i')} tại ${m('t=0')}`,
      o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'b<sub>3</sub>', 'c'], ow: 18 },
    { t: 'Dạng 2 · Bài 1', de: `Dòng ${nw(m('i=2\\sqrt2\\cos\\left(100\\pi t+\\dfrac{\\pi}{4}\\right)\\ \\mathrm A'))} chạy qua ${Om('R=50')}.<br>${s1('a')} công suất toả nhiệt trung bình của ${m('R')}<br>${s1('b')} nhiệt lượng toả ra trong 5 phút<br>${s1('c')} cường độ dòng không đổi toả cùng nhiệt lượng trên ${m('R')} trong cùng thời gian`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 2 · Bài 2', de: `Dòng ${nw(m('i=6\\cos(100\\pi t)\\ \\mathrm A'))} chạy qua ${Om('R=10')}.<br>${s1('a')} công suất toả nhiệt trung bình của ${m('R')}<br>${s1('b')} nhiệt lượng toả ra trong 30 s<br>${s1('c')} cường độ dòng không đổi toả cùng nhiệt lượng trên ${m('R')} trong cùng thời gian`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 3 · Bài 1', de: `Dòng điện xoay chiều tần số ${Hz('50')}, cường độ hiệu dụng ${nw(m('\\sqrt2\\ \\mathrm A'))}. Tại ${m('t=0')}, ${A('i=1')} và đang giảm.<br>${s1('a')} biểu thức ${m('i')} (dạng hàm cos, ${m('t')} tính bằng s)<br>${s1('b')} ${m('i')} tại ${nw(m('t=\\dfrac{1}{300}\\ \\mathrm s'))}`,
      o: ['a', 'b'], ow: { a: 58, b: 18 } },
    { t: 'Dạng 3 · Bài 2', de: `Dòng điện xoay chiều tần số ${Hz('25')}, cường độ hiệu dụng ${A('3')}. Tại ${m('t=0')}, ${A('i=3')} và đang tăng.<br>${s1('a')} biểu thức ${m('i')} (dạng hàm cos, ${m('t')} tính bằng s)<br>${s1('b')} ${m('i')} tại ${nw(m('t=\\dfrac{1}{200}\\ \\mathrm s'))}`,
      o: ['a', 'b'], ow: { a: 58, b: 18 } },
  ], [
    { t: 'Dạng 4 · Bài 1', de: `Khung ${m('N=100')} vòng, mỗi vòng ${nw(m('S=200\\ \\mathrm{cm^2}'))}, quay đều 3000 vòng/phút quanh trục vuông góc với từ trường đều ${nw(m('B=0{,}05\\ \\mathrm T'))}. Lúc ${m('t=0')}, pháp tuyến cùng hướng ${m('\\vec B')}.<br>${s1('a')} ${om} và ${m('\\Phi_0')}<br>${s1('b')} ${m('E_0')} và ${m('E')}<br>${s1('c')} biểu thức ${m('e')} (V, s)`,
      o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], ow: { 'a<sub>1</sub>': 20, 'a<sub>2</sub>': 20, 'b<sub>1</sub>': 20, 'b<sub>2</sub>': 20, c: 58 } },
    { t: 'Dạng 4 · Bài 2', de: `Khung ${m('N=500')} vòng, mỗi vòng ${nw(m('S=50\\ \\mathrm{cm^2}'))}, quay đều 600 vòng/phút quanh trục vuông góc với từ trường đều ${nw(m('B=0{,}1\\ \\mathrm T'))}. Lúc ${m('t=0')}, góc giữa ${m('\\vec n')} và ${m('\\vec B')} là ${nw(m('\\varphi=\\dfrac{\\pi}{3}'))}, tức ${nw(m('\\Phi=\\Phi_0\\cos\\left(\\omega t+\\dfrac{\\pi}{3}\\right)'))}.<br>${s1('a')} ${om} và ${m('\\Phi_0')}<br>${s1('b')} ${m('E_0')} và ${m('E')}<br>${s1('c')} biểu thức ${m('e')} (V, s)`,
      o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], ow: { 'a<sub>1</sub>': 20, 'a<sub>2</sub>': 20, 'b<sub>1</sub>': 20, 'b<sub>2</sub>': 20, c: 58 } },
    { t: 'Dạng 5 · Bài 1', de: `Đèn chỉ sáng khi ${nw(m('|u|\\ge100\\sqrt2\\ \\mathrm V'))}; đặt vào đèn ${nw(m('u=200\\cos(100\\pi t)\\ \\mathrm V'))}.<br>${s1('a')} thời gian đèn sáng trong một chu kì (ms)<br>${s1('b')} thời gian đèn sáng trong 1 s<br>${s1('c')} kể từ ${m('t=0')}, đèn tắt lần đầu lúc nào (ms)`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 5 · Bài 2', de: `Đèn chỉ sáng khi ${nw(m('|u|\\ge90\\ \\mathrm V'))}; đặt vào đèn ${nw(m('u=180\\cos(120\\pi t)\\ \\mathrm V'))}.<br>${s1('a')} thời gian đèn sáng trong một chu kì (ms)<br>${s1('b')} thời gian đèn sáng trong 1 s<br>${s1('c')} kể từ ${m('t=0')}, đèn tắt lần đầu lúc nào (ms)`, o: ['a', 'b', 'c'] },
    nhap(9),
  ]],
  dap: [
    `D1·1: a<sub>1</sub>) 110 V · a<sub>2</sub>) −${PI}/6 · b<sub>1</sub>) 100${PI} ≈ 314 rad/s · b<sub>2</sub>) 50 Hz · b<sub>3</sub>) 0,02 s · c) 55√6 ≈ 135 V &nbsp;|&nbsp; D1·2: a<sub>1</sub>) 3√2 ≈ 4,24 A · a<sub>2</sub>) −2${PI}/3 · b<sub>1</sub>) 80${PI} ≈ 251 rad/s · b<sub>2</sub>) 40 Hz · b<sub>3</sub>) 0,025 s · c) −3 A &nbsp;|&nbsp; D2·1: a) 200 W · b) 60 000 J · c) 2 A &nbsp;|&nbsp; D2·2: a) 180 W · b) 5400 J · c) 3√2 ≈ 4,24 A &nbsp;|&nbsp; D3·1: a) i = 2cos(100${PI}t + ${PI}/3) A · b) −1 A &nbsp;|&nbsp; D3·2: a) i = 3√2 cos(50${PI}t − ${PI}/4) A · b) 3√2 ≈ 4,24 A`,
    `D4·1: a<sub>1</sub>) 100${PI} ≈ 314 rad/s · a<sub>2</sub>) 0,1 Wb · b<sub>1</sub>) 10${PI} ≈ 31,4 V · b<sub>2</sub>) ≈ 22,2 V · c) e = 10${PI} cos(100${PI}t − ${PI}/2) V &nbsp;|&nbsp; D4·2: a<sub>1</sub>) 20${PI} ≈ 62,8 rad/s · a<sub>2</sub>) 0,25 Wb · b<sub>1</sub>) 5${PI} ≈ 15,7 V · b<sub>2</sub>) ≈ 11,1 V · c) e = 5${PI} cos(20${PI}t − ${PI}/6) V &nbsp;|&nbsp; D5·1: a) 10 ms · b) 0,5 s · c) 2,5 ms &nbsp;|&nbsp; D5·2: a) ≈ 11,1 ms · b) 2/3 s ≈ 0,67 s · c) ≈ 2,78 ms`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 2], kq: [[1, 2, 3], [4, 5]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: `khung quay 1·4 · máy phát mini 2·1 · biểu thức u, i 2·2 · T, f, ${om} 2·3 · hai LED 3·1 · hiệu dụng 3·2 · bẫy 4·1 · bài toán mẫu 5·1 · dạng 1–3 → 6·1 · dạng 4–5 → 7·1`,
  out: process.argv[2] ?? resolve(HERE, 'out/ruot-tap-vl12-c3-bai13.pdf'),
});
