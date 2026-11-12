// Ruột tập VL10 – Bài 6 · Thực hành: đo tốc độ của vật chuyển động (lesson id 51). Quyển Chương 2 lớp 10: bài 6 = tr. 25–36 (baiDau 4).
// Khung: khung.mjs (bố cục bài 14: 1–5 học · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Bài THỰC HÀNH có 4 dạng bài tập mẫu: tr.1–5 = mục tiêu/dự đoán/cổng quang · phương án 1 (hai cổng) · phương án 2 (một cổng, lệch tâm)
// · từ bảng số tới báo cáo + bẫy sai số · Trả bài + bài toán mẫu. Nội dung theo bài web (book/cache/51.json, tải 13/11/2026).
// Đáp số mọi bài (BTM, tương tự) tính bằng Python 13/11/2026 (làm tròn theo quy ước bài: Δ một chữ số có nghĩa).
// Chạy: node scripts/ruot-tap/l10-bai6.mjs [file.pdf]   → scripts/ruot-tap/out/ruot-tap-vl10-bai6.pdf
//       node scripts/ruot-tap/l10-bai6.mjs --hinh       → chụp từng hình ở cỡ in vào out/hinh-l10-bai6/
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai, dapSo } from './khung.mjs';
import { hinhL10b6 as H } from './hinh-l10-bai6.mjs';

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
  const out = resolve(HERE, 'out/hinh-l10-bai6'); mkdirSync(out, { recursive: true });
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

const OFF = (6 - 4) * 12;
const K = khoiTao({ bai: 6, lid: 51, lop: 10, baiDau: 4, ten: 'THỰC HÀNH: ĐO TỐC ĐỘ', sub: 'Vật lí 10 · Chương 2: Động học' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b></div>`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const AB = nw(m('A\\leftrightarrow B'));
const s_ = m('s'), t_ = m('t'), v_ = m('v'), d_ = m('d'), tbar = m('\\bar t'), Dt = m('\\Delta t');
const ttCss = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';
const dv = nw(`${s_}, ${d_}: m · ${t_}: s · ${v_}: m/s`);

const p1 = `${ttCss}<section class="page">
${head('BÀI 6 · THỰC HÀNH: ĐO TỐC ĐỘ CỦA VẬT CHUYỂN ĐỘNG', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Dùng đồng hồ hiện số và cổng quang điện, chọn đúng <b>MODE</b> cho từng phép đo`)}
${dong(`${ck}Đo <b>tốc độ trung bình</b> và <b>tốc độ tức thời</b> của viên bi trên máng nghiêng`)}
${dong(`${ck}Xử lí bảng số liệu, viết kết quả <b>có sai số</b> vào báo cáo`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Bi thép lăn qua đoạn ${nw(m('0{,}500\\ \\mathrm m'))} hết chưa đầy ${nw(m('1\\ \\mathrm s'))}. Đồng hồ bấm tay hiện tới ${nw(m('0{,}01\\ \\mathrm s'))}; tay người bấm thường lệch cỡ ${nw(m('0{,}1\\text{–}0{,}2\\ \\mathrm s'))} mỗi lần. Kết quả đo đoạn này bằng cách bấm tay tin được tới đâu?</p>
<div class="fig-side" style="${fs(48)}"><div>
${opt('A', 'Tin được tới phần trăm giây, vì đồng hồ hiện tới 0,01 s')}
${opt('B', 'Tin được nếu bấm thật tập trung, quen tay thì hết lệch')}
${opt('C', 'Khó tin: lệch 0,2 s trên chưa đầy 1 s là sai số lớn')}
${opt('D', 'Không đo được: bi lăn nhanh dần nên không có tốc độ')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 1)}</div>
${H.mayBam()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Cổng quang điện và đồng hồ hiện số', '1·4')}
<div class="card fig-side" style="${fs(48)};padding:1.2mm 3mm"><div>
<div>Cổng quang: một bên phát tia hồng ngoại, một bên thu. Vật ${f(12)} tia thì cổng báo cho đồng hồ, như một ${f(22)} không cần tay.</div>
<div>Hai ổ cắm A, B nối hai cổng; thang ${nw(m('9{,}999\\ \\mathrm s'))}, chia tới ${nw(`${f(12)}&nbsp;s`)}. Nút ${f(20)} đưa số chỉ về ${nw(m('0{,}000'))}.</div>
<div class="hint" style="margin:.3mm 0">Từ gợi ý: chắn · công tắc · RESET · 0,001</div></div>
${H.congQuang()}</div>
<table><tr><th style="width:30mm">MODE</th><th>Đồng hồ đếm khoảng thời gian nào</th></tr>
<tr><td style="height:8mm">${AB}</td><td></td></tr>
<tr><td style="height:8mm">A hoặc B</td><td></td></tr>
</table>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('PHƯƠNG ÁN 1 · ĐO TỐC ĐỘ TRUNG BÌNH')}
${h3(1, 'II.2 · Phương án 1: hai cổng quang', '2·1')}
<div class="card fig-side" style="${fs(52)};padding:1.2mm 3mm"><div>
<div>Cổng E nối ổ ${f(8)}, cổng F nối ổ ${f(8)}; núm MODE ở vị trí ${nw(f(14))}.</div>
<div style="margin:.4mm 0">${s_}${nw(m('=EF'))} đọc trên ${f(25)} của máng (chia tới mm). ${nw(`${m('v_{\\mathrm{tb}}=')} ${f(14)}`)}</div>
<div>Nam châm điện giữ bi: lần nào bi cũng rời nam châm từ ${f(25)} chỗ, tốc độ đầu bằng ${f(8)}.</div>
<div class="hint" style="margin:.4mm 0">Đơn vị: ${dv}</div></div>
${H.boTri()}</div>
${h3(2, 'Thí nghiệm 1: bi qua hai cổng (số liệu minh hoạ)', '2·2')}
<div class="card" style="padding:1.2mm 3mm">
<div>Cho ${nw(m('s=0{,}500\\ \\mathrm m'))}; thả bi ba lần từ cùng một chỗ, MODE ${AB}.</div>
<table class="tbl-ct" style="text-align:center;margin:.8mm 0"><tr><th style="width:26mm">Lần</th><th>${t_} (s)</th><th>${nw(m('|t-\\bar t|\\ (\\mathrm s)'))}</th></tr>
<tr><td>1</td><td>0,835</td><td></td></tr><tr><td>2</td><td>0,838</td><td></td></tr><tr><td>3</td><td>0,837</td><td></td></tr>
<tr><td><b>Trung bình</b></td><td></td><td></td></tr></table>
<div>Số lớn nhất trừ số nhỏ nhất: ${nw(`${f(14)}&nbsp;s`)} (chỉ vài phần nghìn giây, nhỏ hơn nhiều độ lệch của tay bấm).</div>
<div style="margin-top:.6mm">Tốc độ trung bình: ${nw(`${m('v_{\\mathrm{tb}}=\\dfrac{0{,}500}{\\bar t}=')} <span class="fill" style="min-width:26mm;height:10mm"></span>`)}</div></div>
${h3(3, 'Làm nhanh', '2·3')}
${box(`<div style="padding-top:1mm;line-height:1.35"><b>Câu 1.</b> Hai cổng cách nhau ${nw(m('0{,}400\\ \\mathrm m'))}, MODE ${AB} hiện ${nw(m('0{,}500\\ \\mathrm s'))}. Tốc độ trung bình của bi?</div>${lines(1)}
<div style="padding-top:1mm;line-height:1.35"><b>Câu 2.</b> ${nw(m('s/t'))} có phải tốc độ của bi đúng lúc qua F không? Vì sao?</div>${lines(2)}`)}
${h3(4, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '2·4')}
${rkHai([1, 2, 3], [4, 5, 6])}
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('PHƯƠNG ÁN 2 · TỐC ĐỘ TỨC THỜI · HAI CÁI BẪY')}
${h3(1, 'II.3 · Phương án 2: một cổng quang', '3·1')}
<div class="card" style="padding:1.2mm 3mm">
<div>Từ lúc mép trước chạm tia tới lúc mép sau rời tia, bi đi được đúng ${f(25)}; ${d_} đo bằng ${f(22)}.</div>
<div style="margin:.4mm 0">${nw(`${v_} = ${f(14)}`)}; ${t_} là thời gian chắn tia, MODE ${f(14)}. ${d_} chỉ cỡ ${nw('2 cm')} nên tốc độ chưa kịp đổi: coi là tốc độ ${f(20)} tại cổng.</div>
<div class="hint">Từ gợi ý: tức thời · đường kính · thước kẹp · A hoặc B</div></div>
${h3(2, 'Thí nghiệm 2: bi chắn một cổng (số liệu minh hoạ)', '3·2')}
<div class="card" style="padding:1.2mm 3mm">
<div>${nw(`${m('d=20{,}0\\ \\mathrm{mm}=')} ${f(14)}&nbsp;m`)}; cổng F, MODE B, tia qua tâm bi. Ba lần đo ${t_}: ${nw('0,024 s')}; ${nw('0,023 s')}; ${nw('0,024 s')}.</div>
<div style="margin-top:.6mm">${nw(`${tbar} = ${f(14)}&nbsp;s`)} &nbsp;· ${nw(`${m('v_F=\\dfrac{d}{\\bar t}=')} <span class="fill" style="min-width:26mm;height:10mm"></span>`)}</div>
<div>So với ${nw(m('v_{\\mathrm{tb}}=0{,}597\\ \\mathrm{m/s}'))} trên EF: ${nw(`${m('v_F')} ${ck}lớn hơn &nbsp;${ck}nhỏ hơn`)}; vì bi lăn ${f(25)}.</div></div>
${h3(3, 'III · Bẫy 1: “s/t và d/t cùng là tốc độ của bi, như nhau”', '3·3')}
<div class="card" style="padding:1.2mm 3mm">
<table><tr><th style="width:34mm"></th><th>Tốc độ trung bình</th><th>Tốc độ tức thời</th></tr>
<tr><td style="height:8.5mm">Lấy gì chia gì</td><td></td><td></td></tr>
<tr><td style="height:8.5mm">Số cổng · MODE</td><td></td><td></td></tr></table>
<div style="margin-top:.6mm">Muốn biết bi nhanh bao nhiêu <b>đúng lúc tới chân máng</b>: một cổng ở ${f(25)} máng, lấy ${f(25)} chia ${t_}.</div></div>
${h3(4, 'III · Bẫy 2: tia sáng qua chỗ nào của bi cũng được', '3·4')}
<div class="card fig-side" style="${fs(48)};padding:1.2mm 3mm"><div>
<div>Bi ${nw(m('d=20\\ \\mathrm{mm}'))}, bán kính ${nw(m('R=10\\ \\mathrm{mm}'))}. Tia cách tâm ${nw(m('h=6\\ \\mathrm{mm}'))}: dây cung ${nw(m('c=2\\sqrt{R^2-h^2}'))}.</div>
<table style="margin:.6mm 0"><tr><th style="width:27mm"></th><th>Tia qua tâm</th><th>Tia lệch tâm</th></tr>
<tr><td style="height:8mm;font-size:var(--fs-sm)">Bi đi được khi chắn tia (mm)</td><td></td><td></td></tr>
<tr><td style="height:8mm;font-size:var(--fs-sm)">${nw(m('d/t'))} so với tốc độ thật</td><td></td><td></td></tr></table>
<div>Lần nào cũng lệch cùng một phía: lấy trung bình ${ck}có ${ck}không sửa được; phải chỉnh lại ${f(25)} cổng quang.</div></div>
${H.tiaLech()}</div>
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('TỪ BẢNG SỐ TỚI BÁO CÁO · SAI SỐ')}
${h3(1, 'II.4 · Cách tính sai số', '4·1')}
<div class="card" style="padding:1.2mm 3mm">
<div>Sai số dụng cụ: đồng hồ hiện số lấy ${f(12)} độ chia = ${nw(`${f(12)}&nbsp;s`)}; thước có vạch lấy ${f(12)} độ chia (thước mm: ${nw(`${f(12)}&nbsp;mm`)}).</div>
<div style="margin:.4mm 0">${nw(`${Dt} = ${f(25)} + ${f(25)}`)} &nbsp;(lệch trung bình + dụng cụ)</div>
<div>Chia thì cộng phần trăm: ${nw(`${m('\\delta v=')} ${f(12)} + ${f(12)}`)}; ${nw(`${m('\\Delta v=')} ${f(12)} · ${f(12)}`)}</div>
<div style="margin-top:.4mm">Ghi: ${nw(`${m('v=')} ${f(12)} ± ${f(12)}`)} (${m('\\Delta v')} giữ một chữ số khác 0).</div></div>
${h3(2, `Bảng Thí nghiệm 1 (tr. ${2 + OFF}) → kết quả`, '4·2')}
<div class="card" style="padding:1.2mm 3mm">
<div>${nw(`${tbar} = ${f(14)}&nbsp;s`)}; ${nw(`${Dt} = ${f(12)} + 0,001 = ${f(12)}&nbsp;s`)}; ${nw(`${m('\\delta t=')} ${f(12)}&nbsp;%`)}</div>
<div style="margin:.5mm 0">${nw(`${m('\\Delta s=0{,}0005\\ \\mathrm m')}`)}: ${nw(`${m('\\delta s=')} ${f(12)}&nbsp;%`)}; ${nw(`${m('\\delta v=')} ${f(12)}&nbsp;%`)}</div>
<div>${nw(`${m('\\Delta v=')} ${f(14)}&nbsp;m/s`)} &nbsp;· Kết quả: ${nw(`${m('v_{\\mathrm{tb}}=(')} ${f(14)} ± ${f(14)}) m/s`)}</div></div>
${h3(3, `Bảng Thí nghiệm 2 (tr. ${3 + OFF}) → kết quả`, '4·3')}
<div class="card" style="padding:1.2mm 3mm">
<div>${nw(`${Dt} = 0,000 + 0,001 = 0,001&nbsp;s`)}; ${nw(`${m('\\delta t=')} ${f(12)}&nbsp;%`)}; thước kẹp chia ${nw('0,1 mm')}: ${nw(`${m('\\delta d=\\dfrac{0{,}05}{20{,}0}=')} <span class="fill" style="min-width:12mm;height:10mm"></span>&nbsp;%`)}</div>
<div style="margin:.5mm 0">${nw(`${m('\\delta v=')} ${f(12)}&nbsp;%`)}; ${nw(`${m('\\Delta v=')} ${f(12)}&nbsp;m/s`)}; kết quả ${nw(`${m('v_F=(')} ${f(12)} ± ${f(12)}) m/s`)}</div>
<div>Kết quả nào kém chính xác hơn, tức ${m('\\delta v')} lớn hơn: ${ck}phương án 1 &nbsp;${ck}phương án 2</div></div>
${h3(4, 'III · Bẫy 3: “sai số tuyệt đối nhỏ hơn là đo tốt hơn”', '4·4')}
<div class="card fig-side" style="${fs(52)};padding:1.2mm 3mm"><div>
<div>(I) ${nw(m('t=0{,}800\\ \\mathrm s'))}, sai số ${nw(m('0{,}004\\ \\mathrm s'))}. (II) ${nw(m('t=0{,}020\\ \\mathrm s'))}, sai số ${nw(m('0{,}001\\ \\mathrm s'))}.</div>
<div style="margin:.5mm 0">${nw(`${m('\\delta t_{(\\mathrm I)}=')} ${f(12)}&nbsp;%`)}; ${nw(`${m('\\delta t_{(\\mathrm{II})}=')} ${f(12)}&nbsp;%`)}</div>
<div>Phép đo chính xác hơn: ${f(14)}; vì phải so sai số với ${f(25)}.</div></div>
${H.soSai()}</div>
${K.btvn()}
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('TRẢ BÀI · BÀI TOÁN MẪU · BÀI TẬP VỀ NHÀ')}
${h3(1, 'IV · Trả bài 5 câu', '5·1')}
${box(`${tb('1. Cổng quang làm việc gì? MODE A↔B và MODE B đếm khoảng thời gian nào?')}${lines(2)}
${tb('2. Đo tốc độ trung bình: cần đo gì, bằng dụng cụ nào?')}${lines(1)}
${tb('3. Đo tốc độ tức thời: cần đo gì, bằng dụng cụ nào? Tia sáng phải ở đâu?')}${lines(2)}
${tb('4. Công thức sai số của t và của v; cách viết kết quả.')}${lines(2)}
${tb('5. Vì sao dùng nam châm điện thả bi? Vì sao tia phải qua tâm bi?')}${lines(2)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/5 câu · chưa thuộc: ${f(25)} ${nw(`→ đọc lại ô ${f(12)} Tập`)}</div>
${h3(2, 'V · Bài toán mẫu: bi qua hai cổng quang', '5·2')}
<div class="card soft" style="padding:1.2mm 3mm">Hai cổng quang cách nhau ${m('0{,}600\\ \\mathrm m')} (thước máng chia mm). MODE ${AB}, ba lần thả bi hiện ${nw(m('0{,}776\\ \\mathrm s'))}; ${nw(m('0{,}780\\ \\mathrm s'))}; ${nw(m('0{,}778\\ \\mathrm s'))}. Viết kết quả đo tốc độ trung bình kèm sai số.</div>
${h3(3, 'Phân tích đề')}
<table><tr><th style="width:50mm">Câu trong đề</th><th>Dữ liệu → kiến thức</th></tr>
<tr><td>“cách nhau 0,600 m”</td><td>${m('s=0{,}600\\ \\mathrm m')}, đo một lần</td></tr>
<tr><td style="height:6.5mm">“thước máng chia mm”</td><td></td></tr>
<tr><td style="height:6.5mm">“MODE ${AB}”</td><td></td></tr>
<tr><td style="height:6.5mm">“ba lần … hiện …”</td><td></td></tr>
<tr><td style="height:6.5mm">Đồng hồ hiện số</td><td></td></tr></table>
${h3(4, 'Giải')}
<div class="fig-side" style="${fs(46)}"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl(`${tbar} và ${Dt}:`, 2)}${wl(`${m('\\bar v')}:`, 1)}${wl(`${m('\\delta s,\\ \\delta t,\\ \\delta v')}:`, 2)}${wl('Kết quả:', 1)}</div>${H.boTri('Bố trí của đề: E, F là hai cổng.')}</div>
${foot(5)}</section>`;

// ---- Bài tập mẫu: 4 dạng (tr.6–7) ----
const dang = [
  { t: 'Dạng 1 · Dễ · Chọn MODE đo và tính tốc độ từ số hiển thị',
    de: `Bi thép lăn qua hai cổng quang E, F nối đồng hồ hiện số. Thước máng: ${nw(m('EF=0{,}400\\ \\mathrm m'))}; thước kẹp: ${nw(m('d=20{,}0\\ \\mathrm{mm}'))}; tia của cổng F qua tâm bi. Lần 1: MODE ${AB} hiện ${nw(m('0{,}712\\ \\mathrm s'))}; lần 2: MODE B (cổng F) hiện ${nw(m('0{,}022\\ \\mathrm s'))}.<br><b>a)</b> mỗi số hiển thị là thời gian của việc gì<br><b>b)</b> tốc độ trung bình của bi trên đoạn EF<br><b>c)</b> tốc độ tức thời của bi khi qua cổng F`,
    nd: `${nw(`MODE ${AB} đi với ${f(14)}`)}; một cổng đi với ${f(25)} của bi; đổi ${nw('mm → m')} trước khi chia`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'], cot: 2, gi: 4, fig: H.boTri('Bố trí của đề: E, F là hai cổng.') },
  { t: 'Dạng 2 · Trung bình · Bảng số liệu tốc độ trung bình và kết quả có sai số',
    de: `Đo tốc độ trung bình của bi trên đoạn EF. Thước máng chia nhỏ nhất ${nw(m('1\\ \\mathrm{mm}'))}, ${nw(m('s=EF=0{,}650\\ \\mathrm m'))}. Đồng hồ hiện số (chia ${nw(m('0{,}001\\ \\mathrm s'))}), MODE ${AB}, thả bi ba lần từ cùng một chỗ: ${nw(m('0{,}899\\ \\mathrm s'))}; ${nw(m('0{,}903\\ \\mathrm s'))}; ${nw(m('0{,}904\\ \\mathrm s'))}.<br><b>a)</b> tính ${tbar} và ${Dt}<br><b>b)</b> tính tốc độ trung bình ${m('\\bar v')}<br><b>c)</b> viết kết quả ${m('v=\\bar v\\pm\\Delta v')}`,
    nd: `Chuỗi ${nw(m('\\bar t\\to\\Delta t\\to\\bar v\\to\\delta v\\to\\Delta v'))}; ${nw(`${Dt} = ${f(14)} + ${f(14)}`)}`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'], cot: 2, gi: 4 },
  { t: 'Dạng 3 · Trung bình · Tốc độ tức thời từ thời gian chắn tia',
    de: `Đo tốc độ tức thời của bi tại cổng F. Thước kẹp chia ${nw(m('0{,}1\\ \\mathrm{mm}'))} cho ${nw(m('d=16{,}0\\ \\mathrm{mm}'))}. Đồng hồ hiện số chia ${nw(m('0{,}001\\ \\mathrm s'))}, MODE B; cả ba lần thả đều hiện ${nw(m('t=0{,}020\\ \\mathrm s'))}; tia qua tâm bi.<br><b>a)</b> tốc độ tức thời ${m('\\bar v')} tại F<br><b>b)</b> ${m('\\delta v')} và kết quả ${m('v=\\bar v\\pm\\Delta v')}<br><b>c)</b> muốn chính xác hơn thì cải thiện phép đo đại lượng nào trước`,
    nd: `Ba lần trùng nhau vẫn còn sai số ${f(14)}; ${nw(`${m('\\delta v=')} ${f(12)} + ${f(12)}`)}`, a: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], cot: 2, gi: 6 },
  { t: 'Dạng 4 · Khó · Tia sáng lệch tâm bi: độ lệch của phép đo d/t',
    de: `Bi đường kính ${nw(m('d=20{,}0\\ \\mathrm{mm}'))} qua cổng F lắp thấp: tia cắt bi theo dây cung cách tâm ${nw(m('h=8{,}0\\ \\mathrm{mm}'))}. MODE B hiện ${nw(m('t=0{,}015\\ \\mathrm s'))}; một nhóm vẫn tính bằng ${m('d/t')}.<br><b>a)</b> quãng đường bi thật sự đi được khi chắn tia<br><b>b)</b> tốc độ đúng của bi tại F<br><b>c)</b> ${m('d/t')} của nhóm lớn hơn tốc độ đúng bao nhiêu phần trăm<br><b>d)</b> thả nhiều lần rồi lấy trung bình có hết độ lệch không`,
    nd: `Tia lệch tâm: quãng đường chắn tia là ${f(25)}, ${nw(m('c=2\\sqrt{R^2-h^2}'))}; lệch cùng một phía thì lấy trung bình ${ck}có ${ck}không sửa được`, a: ['a', 'b', 'c', 'd'], cot: 2, gi: 6, fig: H.tiaLech('Tia lệch tâm cắt bi theo dây cung.') },
];

// ---- Bài tương tự: 2 bài/dạng, giải vào vở, đáp số in ngược (Python 13/11/2026) ----
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
    { t: 'Dạng 1 · Bài 1', de: `Hai cổng E, F cách nhau ${nw(m('0{,}500\\ \\mathrm m'))}; đường kính bi ${nw(m('d=16{,}0\\ \\mathrm{mm}'))}, tia qua tâm. Lần 1: MODE ${AB} hiện ${nw(m('0{,}640\\ \\mathrm s'))}; lần 2: MODE B (cổng F) hiện ${nw(m('0{,}018\\ \\mathrm s'))}.<br><b>a)</b> số ${nw(m('0{,}640\\ \\mathrm s'))} là thời gian của việc gì<br><b>b)</b> tốc độ trung bình trên EF<br><b>c)</b> tốc độ tức thời tại F`, o: ['a', 'b', 'c'], ow: { a: 40 }, fig: H.boTri('Cùng bố trí; F là cổng thứ hai.'), fw: 44 },
    { t: 'Dạng 1 · Bài 2', de: `Hai cổng cách nhau ${nw(m('0{,}300\\ \\mathrm m'))}; ${nw(m('d=12{,}0\\ \\mathrm{mm}'))}, tia qua tâm. Lần 1: MODE ${AB} hiện ${nw(m('0{,}520\\ \\mathrm s'))}; lần 2: MODE B (cổng F) hiện ${nw(m('0{,}016\\ \\mathrm s'))}.<br><b>a)</b> số ${nw(m('0{,}016\\ \\mathrm s'))} là thời gian của việc gì<br><b>b)</b> tốc độ trung bình trên EF<br><b>c)</b> tốc độ tức thời tại F`, o: ['a', 'b', 'c'], ow: { a: 40 } },
    { t: 'Dạng 2 · Bài 1', de: `Thước máng chia ${nw(m('1\\ \\mathrm{mm}'))}, ${nw(m('s=0{,}800\\ \\mathrm m'))}; đồng hồ hiện số chia ${nw(m('0{,}001\\ \\mathrm s'))}, MODE ${AB}; ba lần đo ${nw(m('1{,}052\\ \\mathrm s'))}; ${nw(m('1{,}056\\ \\mathrm s'))}; ${nw(m('1{,}057\\ \\mathrm s'))}.<br><b>a)</b> ${tbar} và ${Dt}<br><b>b)</b> tốc độ trung bình ${m('\\bar v')}<br><b>c)</b> viết kết quả ${m('v=\\bar v\\pm\\Delta v')}`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'] },
    { t: 'Dạng 2 · Bài 2', de: `Thước máng chia ${nw(m('1\\ \\mathrm{mm}'))}, ${nw(m('s=0{,}450\\ \\mathrm m'))}; đồng hồ hiện số chia ${nw(m('0{,}001\\ \\mathrm s'))}, MODE ${AB}; ba lần đo ${nw(m('0{,}655\\ \\mathrm s'))}; ${nw(m('0{,}652\\ \\mathrm s'))}; ${nw(m('0{,}656\\ \\mathrm s'))}.<br><b>a)</b> ${tbar} và ${Dt}<br><b>b)</b> tốc độ trung bình ${m('\\bar v')}<br><b>c)</b> viết kết quả ${m('v=\\bar v\\pm\\Delta v')}`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'] },
    nhap(5),
  ], [
    { t: 'Dạng 3 · Bài 1', de: `Thước kẹp chia ${nw(m('0{,}1\\ \\mathrm{mm}'))}: ${nw(m('d=20{,}0\\ \\mathrm{mm}'))}. Đồng hồ chia ${nw(m('0{,}001\\ \\mathrm s'))}, MODE B; cả ba lần đều hiện ${nw(m('0{,}025\\ \\mathrm s'))}; tia qua tâm bi.<br><b>a)</b> tốc độ tức thời ${m('\\bar v')}<br><b>b)</b> ${m('\\delta v')} và kết quả ${m('v=\\bar v\\pm\\Delta v')}<br><b>c)</b> cải thiện phép đo đại lượng nào trước`, o: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], ow: { 'b<sub>2</sub>': 34 } },
    { t: 'Dạng 3 · Bài 2', de: `Thước kẹp chia ${nw(m('0{,}1\\ \\mathrm{mm}'))}: ${nw(m('d=16{,}0\\ \\mathrm{mm}'))}. Đồng hồ chia ${nw(m('0{,}001\\ \\mathrm s'))}, MODE B; cả ba lần đều hiện ${nw(m('0{,}032\\ \\mathrm s'))}; tia qua tâm bi.<br><b>a)</b> tốc độ tức thời ${m('\\bar v')}<br><b>b)</b> ${m('\\delta v')} và kết quả ${m('v=\\bar v\\pm\\Delta v')}<br><b>c)</b> cải thiện phép đo đại lượng nào trước`, o: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], ow: { 'b<sub>2</sub>': 34 } },
    { t: 'Dạng 4 · Bài 1', de: `Bi ${nw(m('d=20{,}0\\ \\mathrm{mm}'))}; tia cắt bi theo dây cung cách tâm ${nw(m('h=6{,}0\\ \\mathrm{mm}'))}; MODE B hiện ${nw(m('t=0{,}020\\ \\mathrm s'))}; nhóm vẫn tính ${m('d/t')}.<br><b>a)</b> quãng đường bi đi được khi chắn tia<br><b>b)</b> tốc độ đúng<br><b>c)</b> ${m('d/t')} lớn hơn tốc độ đúng bao nhiêu phần trăm<br><b>d)</b> lấy trung bình nhiều lần có hết lệch không`, o: ['a', 'b', 'c', 'd'], fig: H.tiaLech('Tia lệch tâm cắt bi theo dây cung.'), fw: 44 },
    { t: 'Dạng 4 · Bài 2', de: `Bi ${nw(m('d=26{,}0\\ \\mathrm{mm}'))}; tia cắt bi theo dây cung cách tâm ${nw(m('h=5{,}0\\ \\mathrm{mm}'))}; MODE B hiện ${nw(m('t=0{,}030\\ \\mathrm s'))}; nhóm vẫn tính ${m('d/t')}.<br><b>a)</b> quãng đường bi đi được khi chắn tia<br><b>b)</b> tốc độ đúng<br><b>c)</b> ${m('d/t')} lớn hơn tốc độ đúng bao nhiêu phần trăm<br><b>d)</b> lấy trung bình nhiều lần có hết lệch không`, o: ['a', 'b', 'c', 'd'] },
    nhap(6),
  ]],
  dap: [
    `D1·1: a) thời gian đi E → F · b) 0,781 m/s · c) 0,889 m/s &nbsp;|&nbsp; D1·2: a) thời gian chắn tia ở F · b) 0,577 m/s · c) 0,750 m/s &nbsp;|&nbsp; D2·1: a<sub>1</sub>) 1,055 s · a<sub>2</sub>) 0,003 s · b) 0,758 m/s · c<sub>1</sub>) 0,758 · c<sub>2</sub>) 0,003 (m/s) &nbsp;|&nbsp; D2·2: a<sub>1</sub>) 0,654 s · a<sub>2</sub>) 0,003 s · b) 0,688 m/s · c<sub>1</sub>) 0,688 · c<sub>2</sub>) 0,004 (m/s)`,
    `D3·1: a) 0,80 m/s · b<sub>1</sub>) 4,3 % · b<sub>2</sub>) (0,80 ± 0,03) m/s · c) thời gian &nbsp;|&nbsp; D3·2: a) 0,50 m/s · b<sub>1</sub>) 3,4 % · b<sub>2</sub>) (0,50 ± 0,02) m/s · c) thời gian &nbsp;|&nbsp; D4·1: a) 16,0 mm · b) 0,80 m/s · c) 25 % · d) không &nbsp;|&nbsp; D4·2: a) 24,0 mm · b) 0,80 m/s · c) 8,3 % · d) không`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [2, 2], kq: [[1, 2], [3, 4]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'cổng quang 1·4 · phương án 1 2·1 · thí nghiệm 1 2·2 · phương án 2 3·1 · thí nghiệm 2 3·2 · bẫy 3·3 3·4 · sai số 4·1 · bài toán mẫu 5·2 · dạng 1–2 → 6·1 · dạng 3–4 → 7·1',
  out: process.argv[2],
});
