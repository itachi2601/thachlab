// Ruột tập VL10 – Bài 11 · Thực hành: đo gia tốc rơi tự do (lesson id 56). Quyển Chương 2 lớp 10 (baiDau 4): bài 11 = tr. 85–96.
// Khung: khung.mjs (bố cục bài 14: 1–5 học · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Bài THỰC HÀNH, web không có dạng bài tập mẫu: tr.1 dự đoán + nhắc lại · tr.2 dụng cụ + thứ tự thao tác · tr.3 các bước + bẫy · tr.4 bảng số liệu + sai số · tr.5 đồ thị s–t² + báo cáo;
// tr.6–7 thay Dạng bằng 3 dạng xử lí số liệu (g từ một lần đo; trung bình + sai số; đồ thị s–t²), tr.8–9 Bài tương tự.
// Nội dung theo bài web (book/cache/56.json, tải 13/11/2026). Mọi đáp số tính bằng Python 13/11/2026.
// Chạy: node scripts/ruot-tap/l10-bai11.mjs [file.pdf]   → scripts/ruot-tap/out/ruot-tap-vl10-bai11.pdf
//       node scripts/ruot-tap/l10-bai11.mjs --hinh       → chụp từng hình ở cỡ in vào out/hinh-l10-bai11/
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL10b11 as H } from './hinh-l10-bai11.mjs';

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
  const out = resolve(HERE, 'out/hinh-l10-bai11'); mkdirSync(out, { recursive: true });
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



const OFF = (11 - 4) * 12;
const K = khoiTao({ bai: 11, lid: 56, lop: 10, baiDau: 4, ten: 'THỰC HÀNH: ĐO GIA TỐC RƠI TỰ DO', sub: 'Vật lí 10 · Chương 2: Động học' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const g = m('g'), s_ = m('s'), t_ = m('t'), tb = m('\\bar t'), gb = m('\\bar g'), dl = m('\\delta'), dg = m('\\Delta g'), dt = m('\\Delta t');
const S = (x) => nw(m(`${x}\\ \\mathrm m`)), Ts = (x) => nw(m(`${x}\\ \\mathrm s`)), G = (x) => nw(m(`${x}\\ \\mathrm{m/s^2}`));
const dv = nw(`${s_}: m · ${t_}: s · ${g}: m/s²`);
const dcs = nw(`${m('\\Delta s=0{,}001\\ \\mathrm m')}; ${m('\\Delta t_{\\mathrm{dc}}=0{,}001\\ \\mathrm s')}`);
const ttCss = '<style>.yo{padding-top:.5mm;display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';

const p1 = `${ttCss}<section class="page">
${head('BÀI 11 · THỰC HÀNH: ĐO GIA TỐC RƠI TỰ DO', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Nêu phương án đo ${g}, đọc đúng thước và đồng hồ, ghi bảng số liệu ${m('(s,t)')}`)}
${dong(`${ck}Xử lí số liệu: trung bình, sai số, viết ${m('g=\\bar g\\pm\\Delta g')}`)}
${dong(`${ck}Vẽ đồ thị ${m('s')} theo ${m('t^2')}, suy ra ${g} từ độ dốc; phân biệt sai số ngẫu nhiên và hệ thống`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Hai bạn thả cùng một viên bi từ độ cao ${nw(m('0{,}500\\ \\mathrm m'))}. Lan bấm đồng hồ bấm giây bằng tay; Minh dùng đồng hồ hiện số nối cổng quang (cảm biến ghi thời điểm vật chắn tia sáng đi qua). Vì sao phòng thí nghiệm dùng cổng quang chứ không bấm tay?</p>
<div class="fig-side" style="${fs(58)}"><div>
${opt('A', 'Cổng quang làm bi rơi nhanh hơn nên số đo nhỏ hơn')}
${opt('B', 'Người bấm tay chậm hơn lúc bi chạm, độ trễ so với cả lần rơi là đáng kể')}
${opt('C', 'Đồng hồ hiện số hiện nhiều chữ số nên không có sai số')}
${opt('D', 'Bấm tay luôn đúng hơn, cổng quang bị ánh sáng làm lệch')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 1)}</div>
${H.tayCong()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, `II.1 · Nhắc lại: bi thả từ nghỉ, ${m('s=\\tfrac12 gt^2')}`, '1·4')}
<div class="card fig-side" style="${fs(48)};padding:1.2mm 3mm"><div>
<div>Rơi tự do từ nghỉ: ${m('v_0=')} ${f(8)}, ${m('a=')} ${f(8)}. Suy ra ${nw(`${g} = `)} ${f(24)}</div>
<div class="hint" style="margin:.3mm 0">Đơn vị: ${dv}</div>
<div>Đồ thị ${s_} theo ${m('t^2')}: đường ${f(22)}, đi qua ${f(14)}; độ dốc ${m('k=')} ${f(10)}, nên ${nw(`${g} = `)} ${f(14)}</div>
<div style="margin-top:.6mm">Hai điểm (1), (2) trên đường: ${nw(`${m('k=')} <span class="fill" style="min-width:34mm;height:10mm"></span>`)}</div></div>
${H.duongS()}</div>
${foot(1)}</section>`;

const buoc = ['Bi rơi, đồng hồ bắt đầu đếm', 'Bi che tia sáng của cổng quang: đồng hồ dừng, hiện ' + t_, 'Nam châm điện giữ bi thép, đồng hồ ở 0', 'Ngắt công tắc nam châm'];
const p2 = `<section class="page">
${head('DỤNG CỤ · BỐ TRÍ · THỨ TỰ THAO TÁC')}
${h3(1, 'II.2 · Dụng cụ và bố trí', '2·1')}
<div class="fig-side" style="${fs(58)}"><div>
<table><tr><th style="width:38mm">Dụng cụ</th><th>Dùng để</th><th style="width:20mm">Độ chia</th></tr>
<tr><td style="height:9mm">Giá đỡ thẳng đứng</td><td></td><td>—</td></tr>
<tr><td style="height:9mm">Nam châm điện + công tắc</td><td></td><td>—</td></tr>
<tr><td style="height:9mm">Thước</td><td>đo ${s_}</td><td>1 mm</td></tr>
<tr><td style="height:9mm">Cổng quang + đồng hồ hiện số</td><td>đo ${t_}</td><td>0,001 s</td></tr></table>
<div class="hint" style="margin-top:.6mm">Cổng quang: cảm biến ghi thời điểm vật chắn tia sáng. Sai số dụng cụ lấy bằng một độ chia.</div>
<div style="margin-top:.6mm">${nw(`${m('\\Delta s=')} ${f(14)} m`)} &nbsp;${nw(`${m('\\Delta t_{\\mathrm{dc}}=')} ${f(18)} s`)}</div></div>
${H.boTri('Bố trí thí nghiệm.')}</div>
${h3(2, 'Thứ tự thao tác: điền số 1–4', '2·2')}
<div class="card" style="padding:1.2mm 3mm">
${buoc.map((x) => `<div class="trap"><b>${f(6)}</b><span>${x}</span></div>`).join('')}
<div style="margin-top:.8mm">Giá đỡ phải thẳng đứng; kiểm bằng ${f(26)}. Mép dưới bi ở ngay ${f(24)} thì ${t_} mới là thời gian rơi hết ${s_}.</div></div>
${h3(3, 'Vì sao không bấm tay?', '2·3')}
<div class="card" style="padding:1.2mm 3mm">Người bấm trễ cỡ ${nw(m('0{,}1\\ \\mathrm s'))}. Cả lần rơi từ ${S('0{,}500')} chỉ khoảng ${Ts('0{,}32')}: độ trễ chiếm ${nw(`${f(10)} %`)}. Nếu vật rơi ${Ts('3')} thì chiếm ${nw(`${f(10)} %`)}.</div>
${h3(4, 'Làm nhanh', '2·4')}
${box(cau(`Thả bi từ ${S('0{,}350')}; đồng hồ ghi ${Ts('0{,}267')} (một lần đo). Gia tốc rơi tự do tính được là bao nhiêu?`, 1))}
${h3(5, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '2·5')}
${rkHai([1, 2, 3], [4, 5, 6])}
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('CÁC BƯỚC ĐO · HAI CÁI BẪY SỐ LIỆU')}
${h3(1, 'II.3 · Các bước đo', '3·1')}
<div class="card" style="padding:1.2mm 3mm">
<div class="trap"><b>1.</b><span>Dựng giá thẳng đứng, đặt cổng quang cách mép dưới bi ${S('0{,}500')}. Đo ${s_} bằng ${f(14)}.</span></div>
<div class="trap"><b>2.</b><span>Thả bi: ngắt công tắc, đọc ${t_} trên đồng hồ, ghi bảng (tr. ${4 + OFF}). Thả ${f(8)} lần ở cùng độ cao.</span></div>
<div class="trap"><b>3.</b><span>Tính ${tb}, ${dt}, ${gb}, ${dl}, ${dg}; viết ${nw(m('g=\\bar g\\pm\\Delta g'))}.</span></div>
<div class="trap"><b>4.</b><span>Đổi độ cao ${nw(m('s=0{,}200;\\ 0{,}300;\\ \\dots;\\ 0{,}600\\ \\mathrm m'))}, thả 5 lần mỗi độ cao, lấy ${tb}; vẽ đồ thị (tr. ${5 + OFF}).</span></div></div>
${h3(2, 'III · Bẫy 1: đo s từ mặt nam châm', '3·2')}
<div class="card fig-side" style="${fs(40)};padding:1.2mm 3mm"><div>
<div>Bi thật sự rơi ${S('0{,}400')}, đồng hồ đúng ${Ts('0{,}286')}. Nhóm đo ${s_} từ mặt nam châm (dài hơn đoạn rơi ${nw(m('0{,}010\\ \\mathrm m'))}) nên ghi ${S('0{,}410')}.</div>
<div style="margin-top:.6mm">${nw(`${g} đúng ${m('=')} ${f(16)}`)} &nbsp;${nw(`${g} nhóm tính ${m('=')} ${f(16)}`)}</div>
<div style="margin-top:.6mm">Lệch ${f(8)} %, ${ck}lớn hơn ${ck}nhỏ hơn giá trị đúng. Thả 100 lần rồi lấy trung bình: lệch này ${ck}giảm ${ck}không giảm.</div></div>
${H.saiGoc()}</div>
${h3(3, 'III · Bẫy 2: lấy trung bình là hết sai số?', '3·3')}
<div class="card" style="padding:1.2mm 3mm">
<table><tr><th>Nguyên nhân</th><th style="width:56mm">Loại sai số</th><th style="width:34mm">Trung bình giảm?</th></tr>
${[`Tay run, ${t_} mỗi lần lên xuống vài phần nghìn giây`, 'Nam châm còn từ dư: bi rời muộn 0,002 s ở mọi lần', `Thước đặt sai gốc, ${s_} dài hơn thật mọi lần`].map((x) => `<tr><td style="height:10mm;font-size:var(--fs-sm)">${x}</td><td style="white-space:nowrap"><span class="ck"></span>ngẫu nhiên &nbsp;<span class="ck"></span>hệ thống</td><td style="white-space:nowrap"><span class="ck"></span>Có &nbsp;<span class="ck"></span>Không</td></tr>`).join('')}</table></div>
${h3(4, 'III · Bẫy 3: khác 9,8 là thí nghiệm hỏng?', '3·4')}
<div class="card" style="padding:1.2mm 3mm">Nhóm báo cáo ${nw(m('g=9{,}50\\pm0{,}05\\ \\mathrm{m/s^2}'))}: khoảng từ ${f(12)} đến ${f(12)}. Có chứa ${nw(m('9{,}8'))}? ${ck}có &nbsp;${ck}không. Kết luận: ${ck}thí nghiệm hỏng &nbsp;${ck}nghi sai số hệ thống.</div>
${K.btvn().replace('<i>1</i>', '<i>5</i>')}
${foot(3)}</section>`;

const bangT = `<table class="tbl-ct" style="text-align:center"><tr><th style="width:12mm">Lần</th><th>${t_} (s)</th><th>${m('\\Delta t_i=|t_i-\\bar t|')} (s)</th></tr>
${[1, 2, 3, 4, 5].map((i) => `<tr><td style="height:8mm"><b>${i}</b></td><td></td><td></td></tr>`).join('')}</table>`;
const p4 = `<section class="page">
${head('BẢNG SỐ LIỆU · XỬ LÍ SAI SỐ')}
${h3(1, `II.4 · Số liệu nhóm em: ${nw(m('s=0{,}500\\ \\mathrm m'))}, 5 lần thả`, '4·1')}
<div class="two"><div>${bangT}</div><div>
<div class="card soft" style="padding:1.2mm 3mm">
<div>${tb} ${nw(m('='))} ${f(24)} s</div>
<div style="margin-top:.8mm">${nw(`${m('\\overline{\\Delta t}=')} ${f(20)} s`)}</div>
<div style="margin-top:.8mm">${nw(`${dt} ${m('=\\overline{\\Delta t}+\\Delta t_{\\mathrm{dc}}=')} ${f(18)} s`)}</div></div>
<div class="hint" style="margin-top:.8mm">${dcs}</div></div></div>
${h3(2, 'Tính g và sai số', '4·2')}
<div class="card" style="padding:1.2mm 3mm">
<div>${nw(`${gb} ${m('=\\dfrac{2s}{\\bar t^2}=')} <span class="fill" style="min-width:26mm;height:10mm"></span> m/s²`)}</div>
<div style="margin-top:.6mm">${nw(`${dl} ${m('=\\dfrac{\\Delta s}{s}+2\\dfrac{\\Delta t}{\\bar t}=')} <span class="fill" style="min-width:34mm;height:10mm"></span>`)}</div>
<div style="margin-top:.6mm">${nw(`${dg} ${m('=\\delta\\cdot\\bar g=')} ${f(16)} m/s²`)} &nbsp;· ${nw(`${m('g=(')}${f(14)} ± ${f(14)}${m(')\\ \\mathrm{m/s^2}')}`)}</div></div>
${h3(3, 'Phần nào của sai số lớn hơn?', '4·3')}
<div class="card soft" style="padding:1.2mm 3mm">
<div>${nw(`${m('\\dfrac{\\Delta s}{s}=')} ${f(14)} %`)} &nbsp;${nw(`${m('2\\dfrac{\\Delta t}{\\bar t}=')} ${f(14)} %`)}. Phần lớn hơn do ${ck}${s_} &nbsp;${ck}${t_}.</div>
<div style="margin-top:.6mm">Muốn giảm sai số tương đối của ${g}, em ${ck}thả cao hơn &nbsp;${ck}đo ${s_} bằng thước chia ${nw(m('0{,}1\\ \\mathrm{mm}'))}. Vì ${t_} cỡ ${nw(m('0{,}3\\ \\mathrm s'))} thì ${m('\\Delta t/\\bar t')} ${f(14)}.</div></div>
${h3(4, 'Vì sao có hệ số 2?', '4·4')}
<div class="card soft" style="padding:1.2mm 3mm">${g} chứa ${m('t^2=t\\cdot t')}: ${t_} lệch ${nw(m('1\\,\\%'))} thì ${m('t^2')} lệch khoảng ${f(8)} %. Tích, thương thì ${ck}cộng ${ck}trừ sai số tương đối.</div>
${h3(5, 'Dụng cụ kém: điện thoại quay 240 khung/s', '4·5')}
<div class="card soft" style="padding:1.2mm 3mm">Lệch một khung hình là ${nw(`${m('\\Delta t_{\\mathrm{dc}}=\\dfrac{1}{240}=')} <span class="fill" style="min-width:20mm;height:10mm"></span> s`)}, lớn hơn đồng hồ hiện số ${f(10)} lần.</div>
${h3(6, 'Khoảng kết quả và 9,8', '4·6')}
<div class="card" style="padding:1.2mm 3mm">
<div>Khoảng ${nw(m('\\bar g\\pm\\Delta g'))} của nhóm em từ ${f(12)} đến ${f(12)} ${nw(m('\\mathrm{m/s^2}'))}. Có chứa ${nw(m('9{,}8'))}? ${ck}có &nbsp;${ck}không. Nếu không chứa, nghi ${ck}sai số hệ thống &nbsp;${ck}đo ít lần.</div></div>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head(`ĐỒ THỊ ${m('s')} THEO ${m('t^2')} · BÁO CÁO`)}
${h3(1, 'II.5 · Năm độ cao, một đồ thị', '5·1')}
<table style="text-align:center"><tr><th style="width:22mm"></th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th></tr>
<tr><td style="height:8mm;text-align:left">${s_} (m)</td>${['0,200', '0,300', '0,400', '0,500', '0,600'].map((x) => `<td>${x}</td>`).join('')}</tr>
<tr><td style="height:8mm;text-align:left">${tb} (s)</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td style="height:8mm;text-align:left">${m('\\bar t^2')} (s²)</td><td></td><td></td><td></td><td></td><td></td></tr></table>
<div style="width:112mm;margin-top:.8mm">${H.luoi()}</div>
${h3(2, `Suy ra ${g} từ độ dốc`, '5·2')}
<div class="card soft" style="padding:1mm 3mm"><div>Hai điểm trên <b>đường thẳng</b>, xa nhau: A ${nw(`(${f(10)}; ${f(10)})`)}, B ${nw(`(${f(10)}; ${f(10)})`)}. ${nw(`${m('k=\\dfrac{s_B-s_A}{t_B^2-t_A^2}=')} <span class="fill" style="min-width:20mm;height:10mm"></span>`)} ${nw(`${g}${m('=2k=')} ${f(14)}`)}</div></div>
${h3(3, 'Câu hỏi báo cáo', '5·3')}
${box(`<div style="padding-top:.6mm"><b>1.</b> Hai cách (tr. ${4 + OFF} và tr. ${5 + OFF}), cách nào dùng cả năm độ cao? Điểm lệch khỏi đường thẳng thấy ngay ở cách nào?</div>${lines(2)}
<div style="padding-top:.6mm"><b>2.</b> Nguồn sai số lớn nhất của nhóm em là gì, cách giảm?</div>${lines(1)}`)}
${foot(5)}</section>`;

const tbDe = (ts, ss) => `<table style="text-align:center;margin:.6mm 0"><tr><th style="width:21mm;text-align:left">Lần</th>${ts.map((_, i) => `<th>${i + 1}</th>`).join('')}</tr>`
  + `<tr><td style="text-align:left">${m('t^2')} (s²)</td>${ts.map((x) => `<td>${x}</td>`).join('')}</tr><tr><td style="text-align:left">${s_} (m)</td>${ss.map((x) => `<td>${x}</td>`).join('')}</tr></table>`;
const t4 = (a) => nw(`${m('t=')} ${a.join('; ')} s`);
const dang = [
  { t: 'Dạng 1 · Dễ · Tính g từ một lần đo; ghi nhầm gốc của s',
    de: `Thả bi từ nghỉ: quãng đường ${S('0{,}450')}, đồng hồ ghi ${Ts('0{,}303')}.<br><b>a)</b> gia tốc rơi tự do ${g}<br><b>b)</b> nhóm đo ${s_} từ mặt nam châm (dài hơn thật ${nw(m('0{,}010\\ \\mathrm m'))}) nên ghi ${S('0{,}460')}: ${g} nhóm tính<br><b>c)</b> ${g} ở câu b) lớn hơn ${g} ở câu a) bao nhiêu phần trăm`,
    nd: `${nw(`${g} = `)} ${f(22)}; ${s_} ở tử số, ${s_} lớn hơn thì ${g} ${f(10)}`, a: ['a', 'b', 'c'], gi: 3, fig: H.boTri('Bố trí đo của đề.', false), fw: 46 },
  { t: 'Dạng 2 · Trung bình · Bốn lần đo: trung bình, sai số, kết quả có sai số',
    de: `Thả bi từ ${S('0{,}600')} (${dcs}). Bốn lần đo ${t4(['0,350', '0,352', '0,351', '0,351'])}.<br><b>a)</b> ${tb} và ${dt}<br><b>b)</b> ${gb}<br><b>c)</b> sai số tương đối ${dl}<br><b>d)</b> ${dg} và kết quả ${nw(m('g=\\bar g\\pm\\Delta g'))}<br><b>e)</b> khoảng ${nw(m('\\bar g\\pm\\Delta g'))} có chứa ${nw(m('9{,}8\\ \\mathrm{m/s^2}'))} không`,
    nd: `${nw(`${m('\\Delta t_i')}: ${f(10)}; ${f(10)}; ${f(10)}; ${f(10)}`)}; ${nw(`${dt} = ${m('\\overline{\\Delta t}')} + ${f(10)}`)}; ${nw(`${dl} = ${f(14)} + 2·${f(14)}`)}`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c', 'd<sub>1</sub>', 'd<sub>2</sub>', 'e'], cot: 4, gi: 6 },
  { t: `Dạng 3 · Khó · Đồ thị ${s_} theo ${m('t^2')}: độ dốc và điểm cắt trục`,
    de: `Nhóm đo năm độ cao (bi đường kính ${nw(m('1{,}0\\ \\mathrm{cm}'))}, mỗi độ cao đã lấy ${tb}). Vẽ ${s_} theo ${m('t^2')} thì các điểm thẳng hàng nhưng <b>không qua gốc</b>:
${tbDe(['0,040', '0,060', '0,080', '0,100', '0,120'], ['0,204', '0,301', '0,398', '0,495', '0,592'])}<b>a)</b> độ dốc ${m('k')} từ điểm 1 và điểm 5<br><b>b)</b> ${g}<br><b>c)</b> đường thẳng cắt trục ${s_} tại ${m('s_0')}`,
    nd: `${nw(`${m('k=\\dfrac{\\Delta s}{\\Delta(t^2)}=')} ${f(16)}`)}; ${g} = ${f(10)}·${m('k')}; ${m('t^2=0')}: ${s_} = ${f(10)}`, a: ['a', 'b', 'c'], gi: 21, fig: H.truc },
];

const oY = (s, o, w = {}) => s.split('<br>').map((p) => {
  const y = p.match(/^<b>([a-e])\)<\/b>/);
  if (!y) return `<div>${p}</div>`;
  const ls = o.filter((l) => l[0] === y[1]);
  return `<div class="yo"><span>${p}</span><span class="oo">${ls.map((l) => `<span class="nw"><b>${l})</b>${f(typeof w === 'object' ? (w[l] ?? 25) : w)}</span>`).join('')}</span></div>`;
}).join('');
const vaoVo = (ds) => ds.map((b) => (b.o ? { t: b.t, de: oY(b.de, b.o, b.ow), k: 0 } : b));
const nhap = (n) => ({ t: '<span class="nhap-t">Nháp / chỗ em còn vướng</span>', de: lines(n), k: 0 });
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–2', 'DẠNG 3 · ĐỌC KẾT QUẢ'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Thả bi từ nghỉ: quãng đường ${S('0{,}700')}, đồng hồ ghi ${Ts('0{,}378')}.<br><b>a)</b> ${g}<br><b>b)</b> ghi nhầm ${nw(m('s=0{,}710\\ \\mathrm m'))} (đo từ mặt nam châm): ${g} nhóm tính<br><b>c)</b> ${g} ở b) lớn hơn ${g} ở a) bao nhiêu phần trăm`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 1 · Bài 2', de: `Thả bi từ nghỉ: quãng đường ${S('0{,}250')}, đồng hồ ghi ${Ts('0{,}226')}.<br><b>a)</b> ${g}<br><b>b)</b> ghi nhầm ${nw(m('s=0{,}260\\ \\mathrm m'))}: ${g} nhóm tính<br><b>c)</b> ${g} ở b) lớn hơn ${g} ở a) bao nhiêu phần trăm`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 2 · Bài 1', de: `Thả bi từ ${S('0{,}400')} (${dcs}). Bốn lần đo ${t4(['0,285', '0,287', '0,286', '0,286'])}.<br><b>a)</b> ${tb} và ${dt}<br><b>b)</b> ${gb}<br><b>c)</b> ${dl}<br><b>d)</b> ${dg} và kết quả ${nw(m('g=\\bar g\\pm\\Delta g'))}`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c', 'd<sub>1</sub>', 'd<sub>2</sub>'], ow: { 'a<sub>1</sub>': 18, 'a<sub>2</sub>': 22, c: 22 } },
    { t: 'Dạng 2 · Bài 2', de: `Thả bi từ ${S('0{,}300')} (${dcs}). Bốn lần đo ${t4(['0,248', '0,247', '0,249', '0,248'])}.<br><b>a)</b> ${tb} và ${dt}<br><b>b)</b> ${gb}<br><b>c)</b> ${dl}<br><b>d)</b> ${dg} và kết quả ${nw(m('g=\\bar g\\pm\\Delta g'))}`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c', 'd<sub>1</sub>', 'd<sub>2</sub>'], ow: { 'a<sub>1</sub>': 18, 'a<sub>2</sub>': 22, c: 22 } },
    { t: 'Dạng 3 · Bài 1', de: `Các điểm ${m('(t^2;\\ s)')} thẳng hàng nhưng không qua gốc:${tbDe(['0,040', '0,080', '0,120', '0,160', '0,200'], ['0,207', '0,399', '0,591', '0,783', '0,975'])}<b>a)</b> độ dốc ${m('k')} từ điểm 1 và điểm 5<br><b>b)</b> ${g}<br><b>c)</b> ${m('s_0')} (điểm cắt trục ${s_})`, o: ['a', 'b', 'c'] },
  ], [
    { t: 'Dạng 3 · Bài 2', de: `Bảng khác, cùng cách xử lí:${tbDe(['0,040', '0,060', '0,080', '0,100', '0,120'], ['0,203', '0,302', '0,401', '0,500', '0,599'])}<b>a)</b> độ dốc ${m('k')} từ điểm 1 và điểm 5<br><b>b)</b> ${g}<br><b>c)</b> ${m('s_0')} (điểm cắt trục ${s_})`, o: ['a', 'b', 'c'] },
    { t: 'Đọc kết quả', de: `Ba nhóm báo cáo ${nw(m('g\\ (\\mathrm{m/s^2})'))}: nhóm 1: ${nw(m('9{,}60\\pm0{,}15'))}; nhóm 2: ${nw(m('9{,}92\\pm0{,}06'))}; nhóm 3: ${nw(m('9{,}75\\pm0{,}10'))}.<br><b>a)</b> nhóm nào có khoảng ${nw(m('\\bar g\\pm\\Delta g'))} chứa ${nw(m('9{,}8'))}<br><b>b)</b> khoảng của nhóm 2 từ … đến …`, o: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>'], ow: { a: 14 } },
    nhap(21),
  ]],
  dap: [
    `D1·1: a) 9,80 · b) 9,94 · c) 1,4 % &nbsp;|&nbsp; D1·2: a) 9,79 · b) 10,18 · c) 4,0 % &nbsp;|&nbsp; D2·1: a<sub>1</sub>) 0,286 s · a<sub>2</sub>) 0,0015 s · b) 9,78 · c) 0,0130 · d<sub>1</sub>) 0,13 · d<sub>2</sub>) (9,78 ± 0,13) m/s² &nbsp;|&nbsp; D2·2: a<sub>1</sub>) 0,248 s · a<sub>2</sub>) 0,0015 s · b) 9,76 · c) 0,0154 · d<sub>1</sub>) 0,15 · d<sub>2</sub>) (9,76 ± 0,15) m/s² &nbsp;|&nbsp; D3·1: a) 4,80 · b) 9,60 m/s² · c) 0,015 m`,
    `D3·2: a) 4,95 · b) 9,90 m/s² · c) 0,005 m &nbsp;|&nbsp; Đọc kết quả: a) nhóm 3 · b<sub>1</sub>) 9,86 · b<sub>2</sub>) 9,98`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [2, 1], kq: [[1, 2], [3]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'nhắc lại 1·4 · dụng cụ 2·1 · thao tác 2·2 · các bước 3·1 · bẫy 3·2 · bảng số liệu 4·1 · sai số 4·3 · đồ thị 5·1 · dạng 1–2 → 6·1 · dạng 3 → 7·1',
  out: process.argv[2],
});
