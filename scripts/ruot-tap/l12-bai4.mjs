// Ruột tập VL12 – Bài 4 · Thực hành: đo nhiệt dung riêng, nhiệt nóng chảy riêng, nhiệt hoá hơi riêng (lesson id 5). Quyển Chương 1 lớp 12: bài 4 = tr. 37–48 (baiDau 1).
// Khung: khung.mjs (bố cục bài 14: 1–5 học · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Bài THỰC HÀNH: tr.1–5 = nhắc lại · dụng cụ + sơ đồ + đọc đồ thị · các bước + bẫy · bảng số liệu (đo lặp) + sai số · đồ thị t(τ) + xử lí + câu hỏi báo cáo.
// Nội dung theo bài web (book/cache/5.json, tải 12/11/2026). Đáp số mọi bài (BTM, tương tự) tính bằng Python 12/11/2026.
// Chạy: node scripts/ruot-tap/l12-bai4.mjs [file.pdf]   → scripts/ruot-tap/out/ruot-tap-vl12-bai4.pdf
//       node scripts/ruot-tap/l12-bai4.mjs --hinh       → chụp từng hình ở cỡ in vào out/hinh-l12-bai4/
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL12b4 as H } from './hinh-l12-bai4.mjs';

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
  const out = resolve(HERE, 'out/hinh-l12-bai4'); mkdirSync(out, { recursive: true });
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


const OFF = (4 - 1) * 12;
const K = khoiTao({ bai: 4, lid: 5, lop: 12, baiDau: 1, ten: 'THỰC HÀNH: ĐO NHIỆT DUNG RIÊNG, NHIỆT NÓNG CHẢY RIÊNG, NHIỆT HOÁ HƠI RIÊNG', sub: 'Vật lí 12 · Chương 1: Vật lí nhiệt' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const Pm = m('P'), tau = m('\\tau'), Q = m('Q'), c = m('c'), lam = m('\\lambda'), L = m('L'), dt = m('\\Delta t'), k = m('k');
const dv = nw(`${Pm}: W · ${tau}: s · m: kg · ${dt}: K`);
const frac = (w = 26) => `<span class="fill" style="min-width:${w}mm;height:10mm"></span>`;
const hangSo = `<div class="card soft" style="padding:1mm 3mm;margin-bottom:1mm"><b>Hằng số cho sẵn:</b> ${nw(`${c}<sub>nước</sub> = ${m('4200\\ \\mathrm{J/(kg\\cdot K)}')}`)} · ${nw(`${lam}<sub>đá</sub> = ${m('3{,}34\\times10^{5}\\ \\mathrm{J/kg}')}`)} · ${nw(`${L}<sub>nước</sub> = ${m('2{,}26\\times10^{6}\\ \\mathrm{J/kg}')}`)} · ${nw(m('1\\ \\mathrm K=1\\ ^\\circ\\mathrm C'))}</div>`;

const ttCss = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';

const p1 = `${ttCss}<section class="page">
${head(`BÀI 4 · THỰC HÀNH: ĐO ${c}, ${lam}, ${L}`, K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Nêu đại lượng cần đo, dụng cụ của từng phép đo ${c}, ${lam}, ${L}`)}
${dong(`${ck}Đọc đồ thị ${m('t')} theo ${tau}, chỉ ra mỗi đoạn ứng với quá trình nào`)}
${dong(`${ck}Tính ${c}, ${lam}, ${L} từ số đo; ghi kết quả kèm nguồn sai số`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Đun một cốc nước đá, khuấy đều. Trong lúc <b>đá còn đang tan</b>, nhiệt kế chỉ thế nào?</p>
<div class="fig-side" style="${fs(44)}"><div>
${opt('A', 'Tăng đều, như khi đun nước lỏng')}
${opt('B', 'Đứng yên cho tới khi đá tan hết')}
${opt('C', 'Giảm dần, vì đá hút bớt nhiệt')}
${opt('D', 'Tăng nhanh lúc đầu rồi chậm dần')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 1)}</div>
${H.cocDa()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Nhắc lại: không dụng cụ nào đọc thẳng nhiệt lượng', '1·4')}
${hangSo}
<div class="card" style="padding:1.2mm 3mm">
<div>Bếp công suất ${Pm} chạy trong thời gian ${tau}: nhiệt lượng truyền cho chất ${nw(`${Q} = ${f(22)}`)}</div>
<div class="hint">Đơn vị: ${dv}</div>
<div style="display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;margin-top:.6mm"><span>Đoạn <b>nghiêng</b> (nhiệt độ đổi): ${nw(`${c} = ${frac(24)}`)}</span><span>Đoạn <b>ngang</b> lúc tan: ${nw(`${lam} = ${frac(20)}`)}</span></div>
<div style="margin-top:.6mm">Đoạn <b>ngang</b> lúc sôi: ${nw(`${L} = ${frac(20)}`)} &nbsp; <span class="hint">(${tau} là thời gian của <i>đoạn ngang</i>)</span></div></div>
${h3(5, 'Làm nhanh', '1·5')}
${box(cau(`Bếp ${nw(m('500\\ \\mathrm W'))} chạy ${nw(`${m('2{,}0')} phút`)}. Nhiệt lượng truyền cho chất là bao nhiêu jun? Ghi kèm đổi đơn vị.`, 1))}
${foot(1)}</section>`;

const dc = (rows) => `<table><tr><th style="width:38mm">Dụng cụ</th><th>Đo đại lượng nào · đơn vị</th></tr>${rows.map((x) => `<tr><td style="height:9mm">${x}</td><td></td></tr>`).join('')}</table>`;
const p2 = `<section class="page">
${head(`DỤNG CỤ · SƠ ĐỒ BỐ TRÍ · ĐỌC ĐỒ THỊ ${m('t(\\tau)')}`)}
${h3(1, 'II.2 · Dụng cụ và sơ đồ bố trí', '2·1')}
<div class="fig-side" style="${fs(62)}"><div>
${dc(['Oát kế (có đo thời gian)', 'Cân điện tử', 'Nhiệt kế chia 0,1 °C', 'Bình xốp có nắp, que khuấy'])}
</div>${H.soDo()}</div>
${h3(2, 'II.3 · Đọc đồ thị khi đun đá liên tục', '2·2')}
<div class="fig-side" style="${fs(52)}"><div>
<table><tr><th style="width:11mm">Đoạn</th><th>Dáng</th><th>Quá trình</th><th style="width:15mm">Cho ta</th></tr>
${[1, 2, 3].map((i) => `<tr><td style="height:13mm"><b>(${i})</b></td><td style="white-space:nowrap;font-size:var(--fs-sm)">${ck}ngang<br>${ck}nghiêng</td><td></td><td style="font-size:var(--fs-sm)">${ck}${c}<br>${ck}${lam}<br>${ck}${L}</td></tr>`).join('')}</table>
<div style="margin-top:.8mm;line-height:1.35">Hai đoạn ngang cùng ${Pm}, cùng ${m('m')}: đoạn nào dài hơn thì nhiệt chuyển thể ${f(12)} hơn.</div></div>
${H.doThi()}</div>
${h3(3, 'Đổi đơn vị trước khi thay số — bẫy 3', '2·3')}
<div class="card" style="padding:1.2mm 3mm"><div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:1mm 3mm">
<span>${nw(`250 g = ${f(14)} kg`)}</span><span>${nw(`4,0 phút = ${f(14)} s`)}</span><span>${nw(`1,5 kW = ${f(14)} W`)}</span><span>${nw(`40 K = ${f(10)} °C`)}</span></div>
<div style="margin-top:.8mm">Bạn A tính ${nw(m('c=\\dfrac{500\\times120}{500\\times40}=3{,}0'))} (${nw(m('P'))} W, ${tau} s, ${nw('m = 500 g')}, ${dt} K). Lỗi ở: ${f(30)}. Kết quả đúng: ${nw(`${f(18)} J/(kg·K)`)}</div>
</div>
${h3(4, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '2·4')}
${rkHai([1, 2, 3], [4, 5])}
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('CÁC BƯỚC ĐO · AN TOÀN · BA CÁI BẪY SỐ LIỆU')}
${h3(1, 'II.4 · Các bước đo', '3·1')}
<div class="card" style="padding:1.2mm 3mm">
<div class="trap"><b>1.</b><span>Cân ${m('m')} nước vào bình xốp (ghi bảng tr. ${4 + OFF}). Cắm nhiệt kế (chia ${f(10)} °C), que khuấy, đậy nắp; ghi ${Pm} ở oát kế.</span></div>
<div class="trap"><b>2.</b><span>Bật nguồn và bấm giờ cùng lúc, <b>khuấy đều</b>. Đọc ${m('t')} mỗi 60 s tới 300 s.</span></div>
<div class="trap"><b>3.</b><span>Để nguội, đo lại cùng ${m('m')}, cùng ${Pm}: có <b>hai lần đo</b>, lấy trung bình.</span></div>
<div class="trap"><b>4.</b><span>Phễu đá: ${nw(`giai đoạn 1 (chưa điện, ${tau} = 300 s)`)}: cân ${m('m_1')}; giai đoạn 2 (có điện, cùng ${tau}): cân ${m('m_2')}.</span></div>
<div class="trap"><b>5.</b><span>Hoá hơi: nước đang sôi, cân khối lượng đầu và cuối sau ${tau} đun.</span></div>
<div style="margin-top:.6mm"><b>An toàn:</b> không để dây điện trở ngoài nước khi bật nguồn (cháy dây); hơi và nước sôi gây bỏng.</div>
<div style="margin-top:.6mm"><b>Vì sao</b> phải khuấy đều trước khi đọc nhiệt kế?</div>${lines(2)}</div>
${h3(2, 'III · Bẫy 1: “nhiệt kế đứng yên nghĩa là hết truyền nhiệt”', '3·2')}
<div class="card" style="padding:1.2mm 3mm">
<table><tr><th style="width:36mm"></th><th>Đoạn nghiêng</th><th>Đoạn ngang</th></tr>
<tr><td style="height:8mm">Nhiệt dùng để</td><td></td><td></td></tr>
<tr><td style="height:8mm">Tính được</td><td></td><td></td></tr></table>
<div style="margin-top:.8mm">Nước sôi ${nw(m('100\\ ^\\circ\\mathrm C'))} trên bếp ${nw(m('400\\ \\mathrm W'))}, nhiệt kế đứng yên. Mỗi giây vẫn có ${nw(`${f(14)} J`)} đi vào nước.</div></div>
${h3(4, 'Thử: c của nước có phụ thuộc khối lượng nước?', '3·3')}
<div class="card" style="padding:1.2mm 3mm">
<div class="hint" style="margin-bottom:.4mm">Bếp ${nw(m('150\\ \\mathrm W'))}, ${nw(m('\\tau=300\\ \\mathrm s'))}, ${nw(m('t_1=28{,}0\\ ^\\circ\\mathrm C'))}</div>
<table class="tbl-ct" style="text-align:center"><tr><th style="width:26mm">${m('m')} (kg)</th><th>0,200</th><th>0,300</th><th>0,400</th></tr>
<tr><td style="text-align:left">${m('t_2')} (°C)</td><td>81,3</td><td>63,7</td><td>54,8</td></tr>
<tr><td style="text-align:left">${c}</td><td>4221</td><td>4202</td><td></td></tr></table>
<div style="margin-top:.6mm">${m('m')} gấp đôi mà ${c} ${ck}đổi nhiều &nbsp;${ck}gần như không đổi. Giả thuyết “${c} phụ thuộc ${m('m')}” ${ck}đúng &nbsp;${ck}bị bác bỏ.</div></div>
${K.btvn().replace('<i>1</i>', '<i>5</i>')}
${foot(3)}</section>`;

const bangA = `<table class="tbl-ct" style="text-align:center">
<tr><th style="width:12mm;padding:.7mm .8mm">${tau} (s)</th><th style="padding:.7mm .8mm">${m('t')} lần 1 (°C)</th><th style="padding:.7mm .8mm">${m('t')} lần 2 (°C)</th><th style="padding:.7mm .8mm">${m('\\bar t')} (°C)</th><th style="padding:.7mm .8mm">${dt} (K)</th><th style="padding:.7mm .8mm">${m('c=\\dfrac{P\\tau}{m\\Delta t}')}</th></tr>
${[0, 60, 120, 180, 240, 300].map((x) => `<tr><td style="height:6.5mm"><b>${x}</b></td><td></td><td></td><td></td>${x === 0 ? '<td>0</td><td>—</td>' : '<td></td><td></td>'}</tr>`).join('')}</table>`;
const p4 = `<section class="page">
${head('BẢNG SỐ LIỆU (ĐO LẶP) · SAI SỐ')}
${h3(1, 'II.5 · Bảng A: nhiệt dung riêng của nước', '4·1')}
<div style="margin-bottom:.8mm">${nw(`${m('m=')} ${f(16)} kg`)} &nbsp; ${nw(`${Pm} = ${f(16)} W`)} &nbsp; ${nw(`${m('t_0=')} ${f(14)} °C`)} <span class="hint">(${dt} tính từ ${m('\\bar t')} lúc ${nw(`${tau} = 0`)})</span></div>
${bangA}
${h3(2, 'Bảng B: nhiệt nóng chảy riêng (phễu đá)', '4·2')}
<div style="margin-bottom:.8mm">${nw(`${m('U=')} ${f(12)} V`)} &nbsp; ${nw(`${m('I=')} ${f(12)} A`)} &nbsp; ${nw(`${tau} = ${f(12)} s`)} &nbsp; ${nw(`${m('UI\\tau=')} ${f(16)} J`)}</div>
<table class="tbl-ct" style="text-align:center"><tr><th style="width:44mm"></th><th>Lần 1</th><th>Lần 2</th><th>Trung bình</th></tr>
<tr><td style="text-align:left">${m('m_1')} (g), chưa cấp điện</td><td></td><td></td><td></td></tr>
<tr><td style="text-align:left">${m('m_2')} (g), có điện</td><td></td><td></td><td></td></tr></table>
<div style="margin-top:.6mm">${nw(`${m('m_2-m_1=')} ${f(14)} g = ${f(14)} kg`)} &nbsp; ${nw(`${lam} = ${m('\\dfrac{UI\\tau}{m_2-m_1}')} = ${f(24)} J/kg`)}</div>
${h3(3, 'Bảng C: nhiệt hoá hơi riêng', '4·3')}
<table class="tbl-ct" style="text-align:center"><tr><th style="width:16mm"></th><th style="padding:.7mm .8mm">${m('m_1')} đầu (kg)</th><th style="padding:.7mm .8mm">${m('m_2')} cuối (kg)</th><th style="padding:.7mm .8mm">${Pm} (W)</th><th style="padding:.7mm .8mm">${tau} (s)</th><th style="padding:.7mm .8mm">${L} (J/kg)</th></tr>
<tr><td style="height:7mm"><b>Lần 1</b></td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td style="height:7mm"><b>Lần 2</b></td><td></td><td></td><td></td><td></td><td></td></tr></table>
${h3(4, 'Sai số: nguồn nào lớn nhất?', '4·4')}
<div class="card" style="padding:1.2mm 3mm">
<div class="hint" style="margin-bottom:.4mm">Sai số dụng cụ: nhiệt kế ${nw(m('\\pm0{,}1\\ ^\\circ\\mathrm C'))}; cân ${nw(m('\\pm0{,}001\\ \\mathrm{kg}'))}; sai số của ${dt} là tổng sai số hai lần đọc.</div>
<div>Lần ${nw(m('m=0{,}200\\ \\mathrm{kg}'))}, ${nw(m('\\Delta t=53{,}3\\pm0{,}2\\ \\mathrm K'))}: sai số tỉ đối của ${dt} ${f(10)} %; của ${m('m')} ${f(10)} %. Sai số tỉ đối của ${c}: ${f(10)} %. Nhiệt mất ra môi trường làm ${c} ${ck}lớn hơn &nbsp;${ck}nhỏ hơn thật.</div></div>
${h3(5, 'III · Bẫy 2: hai cách tính c cho hai số khác nhau', '4·5')}
<div class="card" style="padding:1.2mm 3mm">
<div>Nhóm khác đo ${nw(m('m=0{,}200\\ \\mathrm{kg}'))}, ${nw(m('P=150\\ \\mathrm W'))}: từng mốc ${nw(m('\\tau=300\\ \\mathrm s'))} cho ${nw(m('c=4221\\ \\mathrm{J/(kg\\cdot K)}'))}; đồ thị có độ dốc ${nw(m('k=0{,}178\\ \\mathrm{K/s}'))}: ${nw(`${c} = ${frac(26)}`)} &nbsp; Hai cách chênh nhau ${nw(`${f(10)} %`)}</div>
<div style="margin-top:.6mm">Một mốc lẻ lệch khỏi đường thẳng: ${ck}đọc nhiệt độ sai &nbsp;${ck}mất nhiệt. Mọi mốc lệch cùng phía: ${ck}đọc sai &nbsp;${ck}mất nhiệt.</div></div>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head(`ĐỒ THỊ ${m('t(\\tau)')} · XỬ LÍ SỐ LIỆU · BÁO CÁO`)}
${h3(1, `II.6 · Đồ thị ${m('t')} theo ${tau} của nhóm em (từ bảng A)`, '5·1')}
<div style="width:112mm">${H.luoi()}</div>
${h3(2, `Suy ra ${c} từ độ dốc`, '5·2')}
<table style="text-align:center"><tr><th style="width:15mm"></th><th>Điểm A ${m('(\\tau;t)')}</th><th>Điểm B ${m('(\\tau;t)')}</th><th>${k} (K/s)</th><th>${c} (J/(kg·K))</th></tr>
<tr><td style="height:9mm"><b>Độ dốc</b></td><td></td><td></td><td></td><td></td></tr></table>
<div class="hint" style="margin:.5mm 0">A, B chọn trên <b>đường thẳng</b>, xa nhau; ${nw(m('k=\\dfrac{t_B-t_A}{\\tau_B-\\tau_A}'))}; ${nw(m('c=\\dfrac{P}{mk}'))}.</div>
<div class="card soft" style="padding:1mm 3mm"><div>Cách từng mốc (${nw(`${tau} = 300 s`)} ở bảng A): ${nw(`${c} = ${f(20)}`)} &nbsp; Chênh hai cách: ${nw(`${f(10)} %`)} &nbsp; Kết quả: ${nw(`${c} = (${f(14)} ± ${f(12)})`)} J/(kg·K)</div></div>
${h3(3, 'Câu hỏi báo cáo', '5·3')}
${box(`<div style="padding-top:.6mm"><b>1.</b> Đoạn nằm ngang cho biết gì? Dùng số liệu bảng B hoặc C của nhóm em để chứng minh nhiệt vào đoạn ngang không hề nhỏ.</div>${lines(2)}
<div style="padding-top:.6mm"><b>2.</b> Nêu hai nguồn sai số của nhóm em và hướng lệch của kết quả.</div>${lines(2)}`)}
${foot(5)}</section>`;

const tb5 = (hang, tops, ts, w1 = `${m('\\tau')} (s)`, w2 = `${m('t')} (°C)`) => `<table style="text-align:center;margin:.6mm 0"><tr><th style="width:21mm;text-align:left">${w1}</th>${tops.map((x) => `<td><b>${x}</b></td>`).join('')}</tr><tr><td style="text-align:left;font-weight:700;background:var(--soft)">${w2}</td>${ts.map((x) => `<td>${x}</td>`).join('')}</tr></table>`;
const dang = [
  { t: `Dạng 1 · Dễ · Tính nhiệt dung riêng từ số đo ${m('P')}, ${tau}, ${m('m')}, ${m('t')}`,
    de: `Đo ${c} của dầu ăn bằng nhiệt lượng kế vỏ xốp: ${nw(m('m=250\\ \\mathrm g'))}; ${nw(m('P=75\\ \\mathrm W'))}; đun ${nw(`${m('\\tau=4{,}0')} phút`)} (khuấy đều), nhiệt độ tăng từ ${nw(m('22{,}0\\ ^\\circ\\mathrm C'))} lên ${nw(m('56{,}0\\ ^\\circ\\mathrm C'))}; coi ${nw(m('P\\tau'))} đều làm nóng dầu.<br><b>a)</b> nhiệt lượng bếp truyền<br><b>b)</b> nhiệt dung riêng ${c} của dầu<br><b>c)</b> thật ra còn mất nhiệt: ${c} vừa tính ${ck}lớn hơn &nbsp;${ck}nhỏ hơn giá trị thật`,
    nd: `đổi về SI trước: ${nw(`${tau} = ${f(10)} s`)}, ${nw(`m = ${f(10)} kg`)}; ${nw(`${Q} = ${f(18)}`)}; ${nw(`${c} = ${m('\\dfrac{Q}{m\\Delta t}')}`)}`, a: ['a', 'b', 'c'], gi: 8 },
  { t: `Dạng 2 · Trung bình · Đọc đồ thị ${m('t')}–${tau} có hai đoạn nằm ngang`,
    de: `Đun ${nw(m('0{,}200\\ \\mathrm{kg}'))} nước đá đang tan (từ ${nw(m('0\\ ^\\circ\\mathrm C'))}) bằng bếp ${nw(m('P=400\\ \\mathrm W'))} không đổi; đồ thị dừng khi nước vừa hoá hơi hết; coi nhiệt bếp truyền hết cho chất. Các mốc đọc trên trục ${tau}.<br><b>a)</b> dùng đoạn nghiêng, tính ${c}<br><b>b)</b> dùng đoạn ngang thứ nhất, tính ${lam}<br><b>c)</b> dùng đoạn ngang thứ hai, tính ${L}`,
    nd: `${tau}<sub>1</sub>, ${tau}<sub>2</sub> là <b>độ dài</b> đoạn ngang: ${nw(`${tau}<sub>2</sub> = ${f(10)} − ${f(10)}`)}; ${nw(`${k} = ${m('\\dfrac{\\Delta t}{\\Delta\\tau}')}`)}`, a: ['a', 'b', 'c'], gi: 4, fig: H.doThi('Đồ thị của đề; các mốc đọc: 170 s, 385 s, 1535 s.', ['170', '385', '1535']) },
  { t: 'Dạng 3 · Khó · Phễu nước đá hai giai đoạn: tìm cường độ dòng điện',
    de: `Phễu nước đá hai giai đoạn: dây điện trở nối nguồn ${nw(m('U=12\\ \\mathrm V'))}, dòng ${m('I')} chưa biết; mỗi giai đoạn ${nw(m('\\tau=240\\ \\mathrm s'))}. Giai đoạn 1 (chưa điện) hứng được ${nw(m('m_1=4{,}2\\ \\mathrm g'))}; giai đoạn 2 (có điện) hứng được ${nw(m('m_2=12{,}8\\ \\mathrm g'))}. Môi trường làm tan lượng đá như nhau ở hai giai đoạn; nhiệt dây toả ra đều làm tan đá; ${nw(m('\\lambda=3{,}34\\times10^{5}\\ \\mathrm{J/kg}'))}.<br><b>a)</b> khối lượng đá tan do dây điện trở<br><b>b)</b> nhiệt lượng dây truyền cho đá<br><b>c)</b> cường độ dòng điện ${m('I')}<br><b>d)</b> bỏ giai đoạn 1, coi cả ${m('m_2')} do dây: ${m('I\\,\'')}`,
    nd: `phần do dây = ${nw(`${m('m_2')} − ${f(10)}`)}; ${nw(`${Q} = ${f(10)} · ${m('m_d')}`)}; ${nw(`${Q} = ${f(10)}`)} (dây điện trở)`, a: ['a', 'b', 'c', 'd'], gi: 4, fig: H.pheu('Phễu nước đá của đề.') },
  { t: 'Dạng 4 · Khó · So hai cách tính c và nhận xét hướng lệch',
    de: `Đo ${c} khối nhôm ${nw(m('m=0{,}500\\ \\mathrm{kg}'))} khoan lỗ đặt dây điện trở và nhiệt kế; ${nw(m('P=60\\ \\mathrm W'))}. Số đo theo thời gian từ lúc cấp điện; coi toàn bộ nhiệt dây toả làm nóng nhôm; tra bảng ${nw(m('c=880\\ \\mathrm{J/(kg\\cdot K)}'))}.<br><b>a)</b> ${c} theo từng mốc ${nw(m('\\tau=200\\ \\mathrm s'))} và ${nw(m('\\tau=300\\ \\mathrm s'))}<br><b>b)</b> ${c} theo độ dốc, dùng hai mốc đầu và cuối<br><b>c)</b> hai cách khác nhau ở mốc nào? Kết quả độ dốc lớn hơn hay nhỏ hơn tra bảng, vì sao`,
    bang: tb5(0, [0, 100, 200, 300, 400], ['25,0', '37,9', '50,8', '66,7', '76,6']),
    nd: `${nw(`${dt} = ${m('t')} − ${m('t_0')}`)} (so với lúc ${nw(`${tau} = 0`)}); ${nw(`${c} = ${m('\\dfrac{P}{mk}')}`)}`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'], cot: 3, gi: 3 },
];

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
  tieuDe: ['DẠNG 1–2', 'DẠNG 3–4'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Đo ${c} của một loại dầu: ${nw(m('m=300\\ \\mathrm g'))}; ${nw(m('P=90\\ \\mathrm W'))}; đun ${nw(`${m('\\tau=3{,}0')} phút`)}, nhiệt độ tăng từ ${nw(m('20{,}0\\ ^\\circ\\mathrm C'))} lên ${nw(m('46{,}0\\ ^\\circ\\mathrm C'))}; coi ${nw(m('P\\tau'))} đều làm nóng dầu.<br><b>a)</b> nhiệt lượng bếp truyền<br><b>b)</b> nhiệt dung riêng ${c}<br><b>c)</b> có mất nhiệt thì ${c} tính ra lớn hơn hay nhỏ hơn thật`, o: ['a', 'b', 'c'], ow: { c: 18 } },
    { t: 'Dạng 1 · Bài 2', de: `Một nhóm đun nước: ${nw(m('m=0{,}400\\ \\mathrm{kg}'))}; ${nw(m('P=200\\ \\mathrm W'))}; đun ${nw(`${m('\\tau=5{,}0')} phút`)}, nhiệt độ tăng từ ${nw(m('24{,}0\\ ^\\circ\\mathrm C'))} lên ${nw(m('58{,}0\\ ^\\circ\\mathrm C'))}.<br><b>a)</b> nhiệt lượng bếp truyền<br><b>b)</b> nhiệt dung riêng ${c}<br><b>c)</b> so với ${nw(m('4200\\ \\mathrm{J/(kg\\cdot K)}'))}: lớn hơn hay nhỏ hơn`, o: ['a', 'b', 'c'], ow: { c: 18 } },
    { t: 'Dạng 2 · Bài 1', de: `Đun ${nw(m('0{,}250\\ \\mathrm{kg}'))} nước đá từ ${nw(m('0\\ ^\\circ\\mathrm C'))} bằng bếp ${nw(m('500\\ \\mathrm W'))}. Đoạn ngang thứ nhất kết thúc ở ${nw(m('\\tau=170\\ \\mathrm s'))}; đoạn nghiêng (${nw(m('0\\to100\\ ^\\circ\\mathrm C'))}) kết thúc ở ${nw(m('380\\ \\mathrm s'))}; đoạn ngang thứ hai kết thúc ở ${nw(m('1510\\ \\mathrm s'))}.<br><b>a)</b> nhiệt dung riêng ${c}<br><b>b)</b> nhiệt nóng chảy riêng ${lam}<br><b>c)</b> nhiệt hoá hơi riêng ${L}`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 2 · Bài 2', de: `Đun ${nw(m('0{,}150\\ \\mathrm{kg}'))} nước đá từ ${nw(m('0\\ ^\\circ\\mathrm C'))} bằng bếp ${nw(m('300\\ \\mathrm W'))}. Các mốc gãy: ${nw(m('175\\ \\mathrm s'))} (hết đoạn ngang thứ nhất), ${nw(m('387\\ \\mathrm s'))} (hết đoạn nghiêng ${nw(m('0\\to100\\ ^\\circ\\mathrm C'))}), ${nw(m('1580\\ \\mathrm s'))} (hết đoạn ngang thứ hai).<br><b>a)</b> nhiệt dung riêng ${c}<br><b>b)</b> nhiệt nóng chảy riêng ${lam}<br><b>c)</b> nhiệt hoá hơi riêng ${L}`, o: ['a', 'b', 'c'] },
    nhap(8),
  ], [
    { t: 'Dạng 3 · Bài 1', de: `Phễu nước đá hai giai đoạn: ${nw(m('U=12\\ \\mathrm V'))}, ${nw(m('I=2{,}5\\ \\mathrm A'))}, mỗi giai đoạn ${nw(m('\\tau=300\\ \\mathrm s'))}; hứng được ${nw(m('m_1=3{,}6\\ \\mathrm g'))} (chưa điện) và ${nw(m('m_2=30{,}0\\ \\mathrm g'))} (có điện). Môi trường làm tan đá như nhau ở hai giai đoạn; nhiệt dây đều làm tan đá.<br><b>a)</b> khối lượng đá tan do dây<br><b>b)</b> nhiệt nóng chảy riêng ${lam}<br><b>c)</b> bỏ giai đoạn 1, chia cho cả ${m('m_2')}: ${m('\\lambda\\,\'')}<br><b>d)</b> ${m('\\lambda\\,\'')} lớn hơn hay nhỏ hơn ${lam} ở câu b`, o: ['a', 'b', 'c', 'd'], ow: { d: 16 } },
    { t: 'Dạng 3 · Bài 2', de: `Kiểm tra dây điện trở bằng phễu đá: ${nw(m('U=9\\ \\mathrm V'))}, mỗi giai đoạn ${nw(m('\\tau=300\\ \\mathrm s'))}; ${nw(m('m_1=5{,}0\\ \\mathrm g'))} (chưa điện), ${nw(m('m_2=14{,}2\\ \\mathrm g'))} (có điện); ${nw(m('\\lambda=3{,}34\\times10^{5}\\ \\mathrm{J/kg}'))}.<br><b>a)</b> khối lượng đá tan do dây<br><b>b)</b> nhiệt lượng dây truyền cho đá<br><b>c)</b> cường độ dòng điện ${m('I')}<br><b>d)</b> bỏ giai đoạn 1, coi cả ${m('m_2')} do dây: ${m('I\\,\'')}`, o: ['a', 'b', 'c', 'd'] },
    { t: 'Dạng 4 · Bài 1', de: `Khối nhôm ${nw(m('m=0{,}400\\ \\mathrm{kg}'))}, ${nw(m('P=50\\ \\mathrm W'))}; tra bảng ${nw(m('c=880\\ \\mathrm{J/(kg\\cdot K)}'))}:${tb5(0, [0, 100, 200, 300, 400], ['24,0', '37,4', '50,9', '62,0', '77,8'])}<br><b>a)</b> ${c} tại ${nw(m('\\tau=200\\ \\mathrm s'))}<br><b>b)</b> ${c} tại ${nw(m('\\tau=300\\ \\mathrm s'))}<br><b>c)</b> ${c} theo độ dốc, hai mốc đầu và cuối<br><b>d)</b> mốc lệch khỏi đường: ${m('\\tau=')}`, o: ['a', 'b', 'c', 'd'], ow: { d: 14 } },
    { t: 'Dạng 4 · Bài 2', de: `Khối đồng ${nw(m('m=0{,}500\\ \\mathrm{kg}'))}, ${nw(m('P=20\\ \\mathrm W'))}; tra bảng ${nw(m('c=385\\ \\mathrm{J/(kg\\cdot K)}'))}:${tb5(0, [0, 200, 400, 600, 800], ['22,0', '41,5', '61,1', '80,4', '100,0'])}<br><b>a)</b> độ dốc ${k}<br><b>b)</b> nhiệt dung riêng ${c}<br><b>c)</b> chênh so với tra bảng (%)<br><b>d)</b> ${c} lớn hơn hay nhỏ hơn bảng`, o: ['a', 'b', 'c', 'd'], ow: { d: 16 } },
    nhap(1),
  ]],
  dap: [
    `D1·1: a) 16 200 J · b) 2,08×10<sup>3</sup> J/(kg·K) · c) lớn hơn &nbsp;|&nbsp; D1·2: a) 60 000 J · b) 4,41×10<sup>3</sup> J/(kg·K) · c) lớn hơn &nbsp;|&nbsp; D2·1: a) 4,20×10<sup>3</sup> J/(kg·K) · b) 3,40×10<sup>5</sup> J/kg · c) 2,26×10<sup>6</sup> J/kg &nbsp;|&nbsp; D2·2: a) 4,24×10<sup>3</sup> J/(kg·K) · b) 3,50×10<sup>5</sup> J/kg · c) 2,39×10<sup>6</sup> J/kg`,
    `D3·1: a) 26,4 g · b) 3,41×10<sup>5</sup> J/kg · c) 3,00×10<sup>5</sup> J/kg · d) nhỏ hơn &nbsp;|&nbsp; D3·2: a) 9,2 g · b) 3,07×10<sup>3</sup> J · c) 1,14 A · d) 1,76 A &nbsp;|&nbsp; D4·1: a) 929 · b) 987 · c) 929 (J/(kg·K)) · d) 300 s &nbsp;|&nbsp; D4·2: a) 0,0975 K/s · b) 410 J/(kg·K) · c) 6,6 % · d) lớn hơn`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [2, 2], kq: [[1, 2], [3, 4]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'dụng cụ 2·1 · đọc đồ thị 2·2 · các bước 3·1 · bẫy 3·2 · thử 3·3 · bảng số liệu 4·1 · sai số 4·4 · bẫy 4·5 · đồ thị 5·1 · dạng 1–2 → 6·1 · dạng 3–4 → 7·1',
  out: process.argv[2],
});
