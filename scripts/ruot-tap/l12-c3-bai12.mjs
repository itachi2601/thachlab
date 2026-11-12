// Ruột tập VL12 – Bài 12 · Hiện tượng cảm ứng điện từ (lesson id 13). Quyển Chương 3 lớp 12 (bài 9–16): bài 12 = tr. 37–48.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l12-c3-bai12.mjs (toàn bộ SVG tự vẽ). Nội dung theo bài web (book/cache/13.json, tải từ DB 12/11/2026):
// mục tiêu, dự đoán nam châm trong cuộn dây, II từ thông, III hiện tượng (bảng số đo), IV Lenz + ống nhôm, V Faraday + thanh trượt,
// Trả bài 6 câu, bài toán mẫu khung dây B tăng, thử thách ⭐–⭐⭐⭐, 5 dạng bài tập mẫu. Đáp số (tuongTu.dap) tính bằng Python 12/11/2026.
// Chạy: node scripts/ruot-tap/l12-c3-bai12.mjs [file.pdf]   → scripts/ruot-tap/out/ruot-tap-vl12-c3-bai12.pdf
//       node scripts/ruot-tap/l12-c3-bai12.mjs --hinh       → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l12-c3-bai12/
import { dirname as dn, resolve as rs } from 'node:path';
import { fileURLToPath as fu } from 'node:url';
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai, yn } from './khung.mjs';
import { hinhL12c3b12 as H } from './hinh-l12-c3-bai12.mjs';

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
  const out = resolve(HERE, 'out/hinh-l12-c3-bai12'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 12, lid: 13, ten: 'HIỆN TƯỢNG CẢM ỨNG ĐIỆN TỪ', lop: 12, baiDau: 9, sub: 'Vật lí 12 · Chương 3: Từ trường' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const tall = (w, h = 10) => `<span class="fill" style="min-width:${w}mm;height:${h}mm"></span>`;
const Phi = m('\\Phi'), al = m('\\alpha'), ec = m('e_c'), dPhi = m('\\Delta\\Phi'), dt = m('\\Delta t'), vB = m('\\vec B'), Bc = m('\\vec B_c');
const T_ = (s) => nw(m(`${s}\\ \\mathrm T`)), cm = (s) => nw(m(`${s}\\ \\mathrm{cm}`)), cm2 = (s) => nw(m(`${s}\\ \\mathrm{cm^2}`));
const s_ = (s) => nw(m(`${s}\\ \\mathrm s`)), Om = (s) => nw(m(`${s}\\ \\Omega`)), mWb = (s) => nw(m(`${s}\\ \\mathrm{mWb}`));
const doiCm2 = nw(m('1\\ \\mathrm{cm^2}=10^{-4}\\ \\mathrm{m^2}'));
const doiM = nw(m('1\\ \\mathrm{mWb}=10^{-3}\\ \\mathrm{Wb}')), doiMs = nw(m('1\\ \\mathrm{ms}=10^{-3}\\ \\mathrm s'));
const kdh = 'chiều kim đồng hồ';

// Bài tương tự 1 cột, ô đáp số cuối dòng của ý (cùng cách l11-bai16).
const ttCss = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';

const p1 = `${ttCss}<section class="page">
${head('BÀI 12 · HIỆN TƯỢNG CẢM ỨNG ĐIỆN TỪ', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Tính <b>từ thông</b> qua khung dây phẳng; lấy đúng góc ${al}`)}
${dong(`${ck}Nêu <b>điều kiện</b> để mạch xuất hiện dòng điện cảm ứng`)}
${dong(`${ck}Xác định <b>chiều</b> dòng điện cảm ứng bằng định luật Lenz`)}
${dong(`${ck}Tính <b>suất điện động cảm ứng</b> bằng định luật Faraday`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Đèn dynamo xe đạp sáng mà không cần pin. Thử: cầm nam châm đưa vào trong lòng cuộn dây nối điện kế rồi <b>giữ yên</b> ở đó. Kim điện kế sẽ ra sao?</p>
<div class="fig-side" style="${fs(44)}"><div>
${opt('A', 'Lệch liên tục suốt thời gian nam châm nằm trong cuộn dây')}
${opt('B', 'Không bao giờ lệch, vì mạch không có nguồn điện')}
${opt('C', 'Lệch trong lúc nam châm đang chuyển động, rồi về 0 khi nam châm đứng yên')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 1)}</div>
${H.duDoan()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II · Từ thông', '1·4')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div style="margin:.4mm 0;display:flex;align-items:flex-end;gap:2mm"><span>Khung phẳng ${m('S')} trong từ trường đều ${m('B')}:</span> ${m('\\Phi=')} ${tall(26)}</div>
<div>${al} là góc giữa ${f(26)} của mặt khung và ${vB}.</div>
<div>Đơn vị ${Phi}: ${f(14)} (đọc là ${f(16)}); ${doiCm2}</div>
<div>${nw(`${m('\\alpha=0^\\circ')}: ${m('\\Phi=')} ${f(14)}`)} (lớn nhất) · ${nw(`${m('\\alpha=90^\\circ')}: ${m('\\Phi=')} ${f(10)}`)}</div>
<div>Đề cho “mặt khung hợp với đường sức góc ${m('30^\\circ')}” thì ${nw(`${m('\\alpha=')} ${f(14)}`)}</div></div>
${H.tuThong()}</div>
${box(cau(`<b>Ví dụ.</b> Khung dây ${nw(m('S=0{,}05\\ \\mathrm{m^2}'))} trong từ trường đều ${T_('B=0{,}2')}, pháp tuyến hợp với ${vB} góc ${m('60^\\circ')}. Tính ${Phi}.`, 1))}
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('III · HIỆN TƯỢNG CẢM ỨNG ĐIỆN TỪ')}
${h3(1, 'Thí nghiệm: nam châm, cuộn dây, điện kế', '2·1')}
<div class="card fig-side" style="${fs(42)};padding:1.2mm 3mm"><div>
<div><b>Làm:</b> nối hai đầu cuộn dây với điện kế (không có pin). Đưa nam châm vào, giữ yên, rút ra; lặp lại nhanh hơn.</div>
<table style="margin-top:.8mm"><tr><th style="width:30mm">Thao tác</th><th>${Phi} qua cuộn dây</th><th style="width:24mm">Kim điện kế</th></tr>
<tr><td style="height:6.5mm">Đưa vào chậm</td><td></td><td></td></tr>
<tr><td style="height:6.5mm">Đưa vào nhanh</td><td></td><td></td></tr>
<tr><td style="height:6.5mm">Giữ yên trong cuộn</td><td></td><td></td></tr>
<tr><td style="height:6.5mm">Rút ra</td><td></td><td></td></tr></table></div>
${H.thiNghiem()}</div>
${h3(2, 'Bảng số đo: dòng cảm ứng theo tốc độ đưa vào', '2·2')}
<div class="card" style="padding:1.2mm 3mm">
<table class="tbl-ct"><tr><th style="width:30mm">${m('v')} (m/s)</th><th>0,1</th><th>0,2</th><th>0,4</th></tr>
<tr><td>${m('i')} (mA)</td><td>1,0</td><td>2,1</td><td>3,9</td></tr>
<tr><td>${m('i/v')} (mA·s/m)</td><td></td><td></td><td></td></tr></table>
<div style="margin-top:.6mm"><b>Rút ra:</b> ${m('i/v')} gần như ${f(20)} nên ${m('i')} tỉ lệ ${f(16)} với ${m('v')}.</div>
<div>Sai số đo ${nw(m('\\pm0{,}5\\ \\mathrm{mA}'))}: hàng kém tin cậy nhất là ${nw(`${m('v=')} ${f(12)}`)} vì sai số tương đối ${f(14)}</div>
<div class="hint">Số minh hoạ, không phải số đo thật.</div></div>
${h3(3, 'Hiện tượng cảm ứng điện từ', '2·3')}
<div class="card" style="padding:1.2mm 3mm">
<div>Khi từ thông qua một mạch ${f(14)} ${f(24)} thì trong mạch xuất hiện ${f(36)}.</div>
<div>Dòng này chỉ tồn tại trong lúc ${f(48)}.</div>
<div>Ba cách làm ${Phi} biến thiên: đổi ${f(14)} · đổi ${f(14)} · đổi ${f(14)}</div>
<div style="margin-top:.4mm">Ví dụ mỗi cách:</div>${lines(2)}</div>
${h3(4, 'Bẫy: “từ thông lớn thì có dòng điện”', '2·4')}
<table><tr><th>Tình huống (mạch kín)</th><th style="width:34mm">Có dòng cảm ứng?</th></tr>
<tr><td>Cuộn dây áp sát nam châm điện đang bật ổn định</td>${yn}</tr>
<tr><td>Cùng cuộn dây đó, lúc vừa ngắt công tắc nam châm điện</td>${yn}</tr>
<tr><td>Vòng dây đứng yên trong từ trường đều rất mạnh</td>${yn}</tr></table>
${box(cau('<b>Vì sao</b> tình huống đầu không có dòng dù từ thông rất lớn?', 1), 'margin-top:1mm')}
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('IV · CHIỀU DÒNG ĐIỆN CẢM ỨNG: ĐỊNH LUẬT LENZ')}
${h3(1, 'Định luật Lenz', '3·1')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div>Dòng điện cảm ứng có chiều sao cho từ trường mà nó sinh ra ${f(22)} sự ${f(22)} của từ thông đã sinh ra nó.</div>
<div style="margin-top:.6mm">Mặt vòng dây có đường sức cảm ứng đi ${f(10)} là mặt Bắc.</div>
<div>Chiều dòng: quy tắc ${f(26)} — ngón cái chỉ chiều ${f(20)}, các ngón khum chỉ chiều ${f(14)}.</div>
<div>Mẹo nhớ: tiến thì ${f(12)} · lùi thì ${f(12)}</div></div>
${H.lenz()}</div>
<table><tr><th style="width:44mm"></th><th>${Phi} tăng (nam châm lại gần)</th><th>${Phi} giảm (nam châm rút ra)</th></tr>
<tr><td>${Bc} so với ${vB} ngoài</td><td></td><td></td></tr>
<tr><td>Vòng dây đẩy hay kéo nam châm</td><td></td><td></td></tr>
<tr><td>Đầu vòng gần cực N là cực</td><td></td><td></td></tr></table>
${h3(2, 'Vì sao Lenz là bảo toàn năng lượng', '3·2')}
<div class="card" style="padding:1.2mm 3mm">
<div>Đẩy nam châm vào cuộn dây kín thấy nặng tay; đẩy càng nhanh càng ${f(14)}. Công của tay biến thành ${f(22)}.</div>
<div>Nếu cuộn dây <b>hút</b> nam châm đang tiến vào thì điều gì vô lí xảy ra?</div>${lines(1)}</div>
${h3(3, 'Thí nghiệm: nam châm rơi chậm trong ống nhôm', '3·3')}
<div class="card fig-side" style="${fs(24)};padding:1.2mm 3mm"><div>
<div><b>Làm:</b> thả cùng lúc từ miệng một ống nhôm thẳng đứng một cục nam châm và một cục nhôm cùng hình dạng.</div>
<div><b>Quan sát:</b> cục ${f(22)} ra đáy ống trước; cục kia rơi ${f(22)}.</div>
<div><b>Rút ra:</b> nam châm rơi làm từ thông qua thành ống ${f(18)}, sinh dòng ${f(14)} (dòng cảm ứng khép kín trong khối kim loại). Theo Lenz, dòng này ${f(16)} chuyển động: nguyên lí phanh ${f(12)}.</div></div>
${H.ongNhom()}</div>
${h3(4, 'Làm nhanh', '3·4')}
${box(`<div style="padding-top:1mm;line-height:1.6"><b>Câu 1.</b> Đưa cực Bắc của nam châm lại gần một vòng dây kín (theo trục vòng). Đầu vòng gần nam châm là cực ${f(12)}, vòng ${f(16)} nam châm.</div>
<div style="line-height:1.6"><b>Câu 2.</b> Kéo cực Nam của nam châm ra xa một vòng dây kín. Đầu vòng gần nam châm là cực ${f(12)}, vòng ${f(16)} nam châm.</div>
`)}
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('V · SUẤT ĐIỆN ĐỘNG CẢM ỨNG: ĐỊNH LUẬT FARADAY')}
${h3(1, 'Định luật Faraday', '4·1')}
<div class="card" style="padding:1.2mm 3mm">
<div>Độ lớn suất điện động cảm ứng ${ec} (đơn vị ${f(10)}) bằng ${f(26)} của từ thông qua mạch.</div>
<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:2mm;margin:.6mm 0">
<div style="display:flex;align-items:flex-end;gap:1mm">${m('|e_c|=')} ${tall(20)}</div>
<div style="display:flex;align-items:flex-end;gap:1mm"><span>${m('N')} vòng: ${m('|e_c|=')}</span> ${tall(16)}</div>
<div style="display:flex;align-items:flex-end;gap:1mm"><span>điện trở ${m('R')}: ${m('i=')}</span> ${tall(12)}</div></div>
<div>${Phi} trong công thức ${m('N')} vòng là từ thông qua ${f(18)}. Đổi: ${doiM} · ${doiMs}</div>
<div>Dấu trừ trong ${m('e_c=-\\dfrac{\\Delta\\Phi}{\\Delta t}')} thể hiện định luật ${f(16)}. Mạch hở: có ${ec}, ${f(16)} dòng.</div>
<div>Cùng ${dPhi}, đưa nam châm vào trong ${s_('0{,}1')} thay vì ${s_('1')}: ${ec} ${f(24)}</div></div>
${h3(2, 'Thanh kim loại trượt cắt đường sức', '4·2')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div>Thanh dài ${m('\\ell')} trượt đều với tốc độ ${m('v')}; ${vB}, thanh, ${m('\\vec v')} đôi một vuông góc.</div>
<div>Trong ${dt}: thanh đi được ${f(16)}; diện tích mạch tăng ${nw(`${m('\\Delta S=')} ${f(16)}`)}</div>
<div>${nw(`${m('\\Delta\\Phi=')} ${f(18)}`)} ⇒ ${nw(`${m('|e_c|=')} ${f(16)}`)}</div>
<div>Dòng ${nw(`${m('I=')} ${f(14)}`)} · công suất toả nhiệt ${nw(`${m('P=')} ${f(12)}`)}</div>
<div>Lực từ lên thanh ${nw(`${m('F=')} ${f(14)}`)}, chiều ${f(26)} chuyển động.</div>
<div>Trong hình, từ thông qua mạch ${f(14)}; dòng trong thanh chạy ${f(20)} (lên/xuống).</div>
<div>Muốn thanh trượt đều phải có lực kéo; công của lực kéo biến thành ${f(18)}.</div></div>
${H.thanhTruot()}</div>
${h3(3, 'Làm nhanh', '4·3')}
${box(cau(`<b>Câu 1.</b> Từ thông qua mạch kín giảm đều từ ${mWb('6')} về 0 trong ${s_('0{,}03')}. Tính ${m('|e_c|')}.`, 1)
 + cau(`<b>Câu 2.</b> Thanh dài ${cm('20')} trượt đều ${nw(m('50\\ \\mathrm{cm/s}'))} trên hai ray, vuông góc từ trường đều ${T_('B=0{,}4')}; điện trở toàn mạch ${Om('2')}. Tính ${m('I')}.`, 1))}
${h3(4, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '4·4')}
${rkHai([1, 2, 3, 4], [5, 6, 7])}
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('TRẢ BÀI · BÀI TOÁN MẪU · THỬ THÁCH')}
${h3(1, 'VI · Trả bài 6 câu', '5·1')}
${box(`${tb(`1. Từ thông: công thức, đơn vị; khi nào ${Phi} lớn nhất, bằng 0?`)}${lines(1)}
${tb('2. Điều kiện để có dòng điện cảm ứng?')}${lines(1)}
${tb('3. Định luật Lenz và mẹo nhớ?')}${lines(1)}
${tb('4. Định luật Faraday; dấu trừ nghĩa là gì?')}${lines(1)}
${tb('5. Vì sao nam châm rơi chậm trong ống nhôm?')}${lines(1)}
${tb(`6. Thanh trượt cắt đường sức: ${ec}, ${m('I')}, lực từ?`)}${lines(1)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/6 câu · chưa thuộc: ${f(25)} ${nw(`→ đọc lại ô ${f(12)} Tập`)}</div>
${h3(2, 'VII · Bài toán mẫu: khung dây, B tăng đều', '5·2')}
<div class="card soft" style="padding:1.2mm 3mm">Khung dây kín phẳng diện tích ${cm2('200')}, điện trở ${Om('0{,}5')}, mặt khung vuông góc với đường sức của từ trường đều. ${m('B')} tăng đều từ ${T_('0{,}1')} đến ${T_('0{,}5')} trong ${s_('0{,}2')}. Tính ${m('|e_c|')} và ${m('i')}.</div>
<div class="fig-side" style="${fs(30)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl(`${m('S=')} ${f(16)} &nbsp; ${m('\\alpha=')} ${f(10)} &nbsp; ${m('\\Delta\\Phi=(B_2-B_1)S=')}`, 2)}${wl(`${m('|e_c|=')} ${f(22)} &nbsp; ${m('i=')}`, 1)}${wl(`${Phi} tăng hay giảm? ${f(12)} &nbsp; ${Bc} so với ${vB}:`, 1)}</div>${H.khungMau('B vào giấy, tăng đều.')}</div>
${h3(3, `Điền bước: cùng khung, ${m('B')} giảm đều 0,5 T → 0,2 T trong 0,1 s`, '5·3')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl(`Bước 1: ${Phi} ${f(12)} ⇒ ${Bc} ${f(14)} chiều ${vB} ngoài`, 1)}${wl(`Bước 2: ${m('|\\Delta\\Phi|=')}`, 1)}${wl(`Bước 3: ${m('|e_c|=')} ${f(26)} &nbsp; ${m('i=')}`, 1)}</div>
${h3(4, 'Thử thách phân tầng', '5·4')}
${box(cau(`${m('\\bigstar')} Khung dây ${cm2('50')} vuông góc đường sức của từ trường đều ${T_('B=0{,}4')}. Tính ${Phi}.`, 1)
 + cau(`${m('\\bigstar\\bigstar')} Cuộn 100 vòng, ${Phi} mỗi vòng giảm đều từ ${mWb('4')} về 0 trong ${s_('0{,}02')}. ${m('|e_c|')} cả cuộn?`, 1)
 + cau(`${m('\\bigstar\\bigstar\\bigstar')} Khung một vòng ${nw(m('S=0{,}02\\ \\mathrm{m^2}'))}, ${Om('R=0{,}5')}, ${T_('B=0{,}5')}, quay đều trong ${s_('0{,}05')} từ pháp tuyến song song đến vuông góc ${vB}. Tính ${m('i')} trung bình; ${Bc} cùng hay ngược chiều ${vB}?`, 2))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Từ thông qua khung dây: góc của pháp tuyến',
    de: `Khung dây tròn bán kính ${cm('5{,}0')} trong từ trường đều ${T_('B=0{,}40')}; mặt khung hợp với đường sức góc ${m('30^\\circ')} (lấy ${nw(m('\\pi\\approx3{,}14'))}).<br><b>a)</b> từ thông qua khung<br><b>b)</b> quay khung tới vị trí nào thì từ thông lớn nhất; giá trị đó`,
    nd: `${al} là góc giữa ${f(16)} và ${vB} ⇒ ${nw(`${m('\\alpha=')} ${f(10)}`)}; ${nw(`${m('S=\\pi r^2=')} ${f(18)}`)}`, a: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>'], gi: 4, fig: H.khungD1() },
  { t: 'Dạng 2 · Trung bình · Chiều dòng điện cảm ứng theo định luật Lenz',
    de: `Vòng dây kín nằm trong mặt giấy; từ trường đều vuông góc mặt giấy, hướng vào trong (⊗). Nhìn từ phía người đọc.<br><b>a)</b> độ lớn ${vB} tăng đều: dòng cảm ứng cùng hay ngược ${kdh}<br><b>b)</b> độ lớn ${vB} giảm đều: chiều dòng cảm ứng`,
    nd: `${Phi} tăng ⇒ ${Bc} ${f(14)} chiều ${vB}; nắm tay phải: ngón cái theo ${f(14)}`, a: ['a', 'b'], cot: 2, gi: 3 },
  { t: 'Dạng 3 · Trung bình · Suất điện động cảm ứng khi B biến thiên',
    de: `Khung dây dẫn kín hình vuông cạnh ${cm('6{,}0')}, điện trở ${Om('0{,}30')}, mặt khung vuông góc với đường sức của từ trường đều. Cảm ứng từ giảm đều từ ${T_('0{,}50')} xuống ${T_('0{,}20')} trong ${nw(m('15\\ \\mathrm{ms}'))}.<br><b>a)</b> độ lớn suất điện động cảm ứng và cường độ dòng điện cảm ứng<br><b>b)</b> cùng độ giảm của ${m('B')} nhưng trong thời gian chỉ bằng một nửa: cường độ dòng điện cảm ứng`,
    nd: `Chỉ ${m('B')} đổi: ${nw(`${m('|\\Delta\\Phi|=')} ${f(16)}`)}; đổi ${m('S')} ra ${f(8)}, ${dt} ra ${f(8)}; ${m('i')} tỉ lệ nghịch với ${f(10)}`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b'], gi: 4 },
  { t: `Dạng 4 · Khó · Cuộn ${m('N')} vòng, quay khung đổi góc ${al}`,
    de: `Cuộn dây dẹt ${m('100')} vòng, diện tích mỗi vòng ${cm2('50')}, điện trở cả cuộn ${Om('4{,}0')}, trong từ trường đều ${T_('B=0{,}40')}. Ban đầu mặt cuộn dây vuông góc với đường sức. Quay đều cuộn dây quanh trục nằm trong mặt cuộn, vuông góc đường sức, trong ${s_('0{,}050')}, tới khi mặt cuộn hợp với đường sức góc ${m('30^\\circ')}.<br><b>a)</b> suất điện động cảm ứng trung bình và cường độ dòng điện trung bình<br><b>b)</b> trong lúc quay, từ trường cảm ứng cùng chiều hay ngược chiều từ trường ngoài`,
    nd: `${nw(`${m('\\alpha_1=')} ${f(10)}`)}, ${nw(`${m('\\alpha_2=')} ${f(10)}`)}; ${Phi} tính cho ${f(14)}; ${nw(`${m('|e_c|=')} ${f(18)}`)}`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b'], gi: 6 },
  { t: 'Dạng 5 · Khó · Đọc đồ thị từ thông theo thời gian',
    de: `Vòng dây kín điện trở ${Om('0{,}50')}; từ trường vuông góc mặt vòng, hướng vào trong tờ giấy (⊗); pháp tuyến chọn cùng chiều ${vB} nên ${Phi} ≥ 0. ${Phi} biến thiên như đồ thị.<br><b>a)</b> những đoạn nào có dòng điện cảm ứng<br><b>b)</b> cường độ dòng cảm ứng ở mỗi đoạn có dòng<br><b>c)</b> nhìn từ phía người đọc, dòng ở mỗi đoạn đó cùng hay ngược ${kdh}`,
    nd: `Độ dốc đoạn thẳng = ${f(26)}; đoạn nằm ngang: ${nw(`${m('e_c=')} ${f(8)}`)}`, a: ['a', 'b', 'c'], cot: 1, gi: 6, fig: H.doThiD5() },
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
const chieu = { a: 30, b: 30, c: 30 };
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–3', 'DẠNG 4–5'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Khung dây hình vuông cạnh ${cm('10')} trong từ trường đều ${T_('B=0{,}50')}; pháp tuyến của khung hợp với ${vB} góc ${m('60^\\circ')}.<br><b>a)</b> từ thông qua khung<br><b>b)</b> từ thông khi mặt khung song song với đường sức`, o: ['a', 'b'] },
    { t: 'Dạng 1 · Bài 2', de: `Khung dây chữ nhật ${nw(m('4{,}0\\ \\mathrm{cm}\\times5{,}0\\ \\mathrm{cm}'))} trong từ trường đều ${T_('B=0{,}060')}; mặt khung hợp với đường sức góc ${m('30^\\circ')}.<br><b>a)</b> góc ${al} dùng trong công thức từ thông<br><b>b)</b> từ thông qua khung<br><b>c)</b> từ thông lớn nhất khi quay khung`, o: ['a', 'b', 'c'], ow: { a: 16 } },
    { t: 'Dạng 2 · Bài 1', de: `Vòng dây kín nằm trong mặt giấy; từ trường đều vuông góc mặt giấy, hướng ra (⊙). Chiều kim đồng hồ xét khi nhìn từ phía người đọc.<br><b>a)</b> độ lớn ${vB} tăng đều: dòng cảm ứng cùng hay ngược ${kdh}<br><b>b)</b> độ lớn ${vB} giảm đều: chiều dòng cảm ứng`, o: ['a', 'b'], ow: chieu },
    { t: 'Dạng 2 · Bài 2', de: `Nam châm thẳng đứng, cực Bắc ở dưới, rơi theo trục xuyên qua vòng dây kín nằm ngang bên dưới. Nhìn từ trên xuống.<br><b>a)</b> lúc nam châm đang tới gần: mặt trên của vòng là cực gì<br><b>b)</b> lúc đó dòng cảm ứng cùng hay ngược ${kdh}<br><b>c)</b> lúc nam châm đã qua và rời xa phía dưới: mặt dưới của vòng là cực gì`, fig: H.roiTT(), fw: 22, o: ['a', 'b', 'c'], ow: { a: 16, b: 26, c: 16 } },
    { t: 'Dạng 3 · Bài 1', de: `Khung dây kín hình vuông cạnh ${cm('10')}, điện trở ${Om('0{,}20')}, mặt khung vuông góc đường sức. ${m('B')} tăng đều từ 0 đến ${T_('0{,}60')} trong ${s_('0{,}12')}.<br><b>a)</b> độ lớn suất điện động cảm ứng<br><b>b)</b> cường độ dòng điện cảm ứng<br><b>c)</b> rồi ${m('B')} giảm đều về 0 trong ${s_('0{,}040')}: cường độ dòng cảm ứng`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 3 · Bài 2', de: `Khung dây kín chữ nhật ${nw(m('5{,}0\\ \\mathrm{cm}\\times8{,}0\\ \\mathrm{cm}'))}, điện trở ${Om('0{,}40')}; pháp tuyến hợp với ${vB} góc ${m('60^\\circ')}. ${m('B')} giảm đều từ ${T_('0{,}80')} xuống ${T_('0{,}20')} trong ${nw(m('20\\ \\mathrm{ms}'))}.<br><b>a)</b> độ lớn độ biến thiên từ thông<br><b>b)</b> suất điện động cảm ứng; cường độ dòng điện cảm ứng`, o: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>'], ow: { 'b<sub>1</sub>': 20, 'b<sub>2</sub>': 20 } },
  ], [
    { t: 'Dạng 4 · Bài 1', de: `Cuộn dây dẹt ${m('200')} vòng, mỗi vòng ${cm2('40')}, điện trở cả cuộn ${Om('8{,}0')}, trong từ trường đều ${T_('B=0{,}50')}. Ban đầu mặt cuộn vuông góc đường sức; quay đều trong ${s_('0{,}040')} tới khi mặt cuộn song song đường sức.<br><b>a)</b> suất điện động cảm ứng trung bình<br><b>b)</b> cường độ dòng điện trung bình<br><b>c)</b> từ trường cảm ứng cùng hay ngược chiều từ trường ngoài`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 4 · Bài 2', de: `Cuộn dây dẹt ${m('50')} vòng, mỗi vòng ${cm2('100')}, điện trở cả cuộn ${Om('2{,}0')}, trong từ trường đều ${T_('B=0{,}20')}. Ban đầu mặt cuộn song song đường sức; quay đều trong ${s_('0{,}10')} tới khi mặt cuộn hợp với đường sức góc ${m('30^\\circ')}.<br><b>a)</b> độ biến thiên từ thông qua một vòng<br><b>b)</b> suất điện động cảm ứng trung bình; dòng điện trung bình<br><b>c)</b> từ trường cảm ứng cùng hay ngược chiều từ trường ngoài`, o: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], ow: { 'b<sub>1</sub>': 18, 'b<sub>2</sub>': 18 } },
    { t: 'Dạng 5 · Bài 1', de: `Vòng dây kín điện trở ${Om('0{,}30')}; từ thông qua vòng biến thiên theo thời gian như đồ thị bên.<br><b>a)</b> khoảng nào không có dòng cảm ứng<br><b>b)</b> cường độ dòng trong khoảng 0 – ${s_('0{,}040')}<br><b>c)</b> cường độ dòng trong khoảng ${s_('0{,}10')} – ${s_('0{,}16')}`, fig: H.doThiTT(), fw: 40, o: ['a', 'b', 'c'], ow: { a: 30, b: 20, c: 20 } },
    { t: 'Dạng 5 · Bài 2', de: `Vòng dây kín điện trở ${Om('0{,}50')}. Từ thông qua vòng giảm đều từ ${mWb('30')} về ${mWb('10')} trong khoảng 0 – ${s_('0{,}20')}, rồi giảm đều tiếp về 0 trong khoảng ${s_('0{,}20')} – ${s_('0{,}30')}.<br><b>a)</b> cường độ dòng cảm ứng trong khoảng đầu<br><b>b)</b> cường độ dòng cảm ứng trong khoảng sau<br><b>c)</b> chiều dòng ở hai khoảng giống hay khác nhau`, o: ['a', 'b', 'c'] },
    nhap(7),
  ]],
  dap: [
    `D1·1: a) 2,5·10<sup>−3</sup> Wb · b) 0 &nbsp;|&nbsp; D1·2: a) 60° · b) 6,0·10<sup>−5</sup> Wb · c) 1,2·10<sup>−4</sup> Wb &nbsp;|&nbsp; D2·1: a) cùng chiều KĐH · b) ngược chiều KĐH &nbsp;|&nbsp; D2·2: a) cực Bắc · b) ngược chiều KĐH · c) cực Bắc &nbsp;|&nbsp; D3·1: a) 0,050 V · b) 0,25 A · c) 0,75 A &nbsp;|&nbsp; D3·2: a) 1,2·10<sup>−3</sup> Wb · b<sub>1</sub>) 0,060 V · b<sub>2</sub>) 0,15 A`,
    `D4·1: a) 10 V · b) 1,25 A · c) cùng chiều &nbsp;|&nbsp; D4·2: a) 1,0·10<sup>−3</sup> Wb · b<sub>1</sub>) 0,50 V · b<sub>2</sub>) 0,25 A · c) ngược chiều &nbsp;|&nbsp; D5·1: a) 0,040 s – 0,10 s · b) 1,0 A · c) 0,67 A &nbsp;|&nbsp; D5·2: a) 0,20 A · b) 0,20 A · c) giống nhau`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 2], kq: [[1, 2, 3], [4, 5]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'từ thông 1·4 · thí nghiệm điện kế 2·1 · hiện tượng 2·3 · bẫy từ thông lớn 2·4 · Lenz 3·1 · ống nhôm 3·3 · Faraday 4·1 · thanh trượt 4·2 · bài toán mẫu 5·2 · dạng 1–3 → 6·1 · dạng 4–5 → 7·1',
  out: process.argv[2] ?? rs(dn(fu(import.meta.url)), 'out/ruot-tap-vl12-c3-bai12.pdf'),
});
