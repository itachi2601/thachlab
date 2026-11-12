// Ruột tập VL12 – Chương 3 · Bài 15 · Một số ứng dụng của cảm ứng điện từ (lesson id 126). Quyển Chương 3 lớp 12: bài 9 = tr. 1–12,
// nên bài 15 = tr. 73–84. KHÁC bai15.mjs (bài 15 Chương 4, năng lượng liên kết) — file này ghi ra out/ruot-tap-vl12-c3-bai15.pdf.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l12-c3-bai15.mjs (toàn bộ SVG tự vẽ). Nội dung theo bài web (book/cache/126.json, tải từ DB 12/11/2026): mục tiêu, dự đoán
// bếp từ, II.1 đàn ghi ta điện, II.2 sạc không dây (bảng d–U₂), II.3 dòng Foucault (con lắc tấm nhôm), II.4 bếp từ (đo hiệu suất), ba bẫy,
// Trả bài 6 câu, bài toán mẫu đế sạc, thử thách ⭐–⭐⭐⭐, 4 dạng bài tập mẫu. Đáp số (kể cả Bài tương tự) tính bằng Python 12/11/2026.
// Chạy: node scripts/ruot-tap/l12-c3-bai15.mjs [file.pdf]     → scripts/ruot-tap/out/ruot-tap-vl12-c3-bai15.pdf
//       node scripts/ruot-tap/l12-c3-bai15.mjs --hinh         → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l12-c3-bai15/
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL12c3b15 as H } from './hinh-l12-c3-bai15.mjs';
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
  const out = resolve(HERE, 'out/hinh-l12-c3-bai15'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 15, lid: 126, ten: 'MỘT SỐ ỨNG DỤNG CỦA CẢM ỨNG ĐIỆN TỪ', lop: 12, baiDau: 9, sub: 'Vật lí 12 · Chương 3: Từ trường' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const V = (s) => nw(m(`${s}\\ \\mathrm V`));
const ec = m('e_c'), N1 = m('N_1'), N2 = m('N_2'), U1 = m('U_1'), U2 = m('U_2'), dPhi = m('\\Delta\\Phi');
const cN = nw(m('c=4\\,200\\ \\mathrm{J/(kg{\\cdot}K)}')), DN = nw(m('D=1\\,000\\ \\mathrm{kg/m^3}'));
const muWb = nw(m('1\\ \\mu\\mathrm{Wb}=10^{-6}\\ \\mathrm{Wb}'));
const oF = (h = 10, w = 30) => `<span class="fill" style="min-width:${w}mm;height:${h}mm"></span>`;

// Bài tương tự 1 cột, ô đáp số cuối dòng của ý (cùng cách l11-bai16).
const ttCss = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';

const p1 = `${ttCss}<section class="page">
${head('BÀI 15 · MỘT SỐ ỨNG DỤNG CỦA CẢM ỨNG ĐIỆN TỪ', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Giải thích cách hoạt động của <b>đàn ghi ta điện</b>, <b>sạc không dây</b>, <b>bếp từ</b>, <b>phanh điện từ</b>`)}
${dong(`${ck}Nêu <b>dòng điện Foucault</b> là gì, khi nào có lợi, khi nào có hại và cách giảm`)}
${dong(`${ck}Dùng ${m('e_c=-N\\dfrac{\\Delta\\Phi}{\\Delta t}')} để giải thích, ${m('\\dfrac{U_2}{U_1}=\\dfrac{N_2}{N_1}')} để tính toán`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Bếp từ không lửa, không mâm nóng đỏ, vậy mà nồi gang chừng bốn phút đã sôi. Trong bếp từ, <b>cái gì nóng lên trước tiên</b>?</p>
<div class="fig-side" style="${fs(44)}"><div>
${opt('A', 'Mặt kính, rồi dẫn nhiệt sang đáy nồi')}
${opt('B', 'Đáy nồi, do dòng điện cảm ứng toả nhiệt')}
${opt('C', 'Đáy nồi, do cọ xát với mặt kính')}
${opt('D', 'Cuộn dây, rồi chiếu tia hồng ngoại vào nồi')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 2)}</div>
${H.bepTu()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Đàn ghi ta điện: dao động thành dòng điện', '1·4')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div>Dây thép nằm ngay trên nam châm có quấn cuộn dây (bộ cảm ứng). Dây bị nam châm ${f(20)}.</div>
<div>Dây dao động ⇒ ${f(18)} qua cuộn dây biến thiên ⇒ trong cuộn có ${f(40)}.</div>
<div style="margin:1mm 0;display:flex;align-items:flex-end;gap:2mm">${ec} = ${oF(11, 28)}</div>
<div class="hint">${ec} (V) · ${m('N')} số vòng · ${dPhi} biến thiên từ thông qua <b>một</b> vòng (Wb) · ${m('\\Delta t')} (s)</div>
<div>Dòng cảm ứng rất nhỏ, phải qua máy tăng âm rồi mới ra loa.</div></div>
${H.pickup()}</div>
${box(cau(`<b>Làm nhanh.</b> Gảy dây mạnh hơn: ${dPhi} mỗi nửa chu kì lớn hơn, tần số không đổi. ${ec} thay đổi thế nào? Tiếng to hơn hay cao hơn?`, 1))}
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('THÍ NGHIỆM DÂY THÉP RUNG · SẠC KHÔNG DÂY')}
${h3(1, 'Thí nghiệm: dây thép rung trên cuộn dây', '2·1')}
<div class="card" style="padding:1.2mm 3mm">
<div><b>Làm:</b> căng dây thép 60 cm trên giá gỗ, kẹp nam châm và cuộn dây 1 000 vòng sát dưới dây, nối điện kế nhạy; gảy dây, kéo căng thêm rồi gảy lại.</div>
<div><b>Quan sát:</b> kim điện kế ${f(36)}; ${nw(`dây căng hơn (rung nhanh hơn) thì kim ${f(30)}`)}</div>
<div>${nw(`dây tắt thì kim ${f(30)}`)}; ${nw(`gảy mạnh thì kim ${f(30)}`)}</div>
<div><b>Rút ra:</b> dao động cơ đã biến thành dòng cảm ứng cùng ${f(22)} với dao động của dây.</div>
</div>
${h3(2, 'II.2 · Sạc không dây: máy biến áp không lõi', '2·2')}
<div class="card fig-side" style="${fs(44)};padding:1.2mm 3mm"><div>
<div>Đế sạc: cuộn ${f(18)} nối dòng điện ${f(22)}. Sau lưng điện thoại: cuộn ${f(18)} nối pin. Hai cuộn ${f(24)} nhau.</div>
<div>Từ trường ${f(20)} của cuộn sơ cấp sinh suất điện động cảm ứng trong cuộn thứ cấp.</div>
<div style="margin:1mm 0;display:flex;align-items:flex-end;gap:2mm">Máy biến áp lí tưởng: ${oF(11, 30)}</div>
<div class="hint">${U1}, ${U2} điện áp hiệu dụng (V) · ${N1}, ${N2} số vòng · ${N2} là cuộn nối thiết bị cần nạp</div>
<div>Không có lõi sắt chung ⇒ nhiều từ thông ${f(14)} (không qua cuộn thứ cấp) ⇒ hiệu suất ${f(16)}.</div></div>
${H.sacKhongDay()}</div>
${h3(3, 'Thí nghiệm: điện áp thứ cấp theo khoảng cách', '2·3')}
<div class="fig-side" style="${fs(52)}"><div>
<div style="font-size:var(--fs-sm);line-height:1.35;margin-bottom:.6mm">Sơ cấp 200 vòng nối ${V('U_1=12')}, thứ cấp 150 vòng, hai ống nhựa đồng trục; chèn dần tấm bìa dày 1 cm vào giữa. ${nw(`Lí tưởng: ${m('U_2=')} ${f(16)}`)}</div>
<table class="tbl-ct"><tr><th>${m('d')} (cm)</th><th>0</th><th>1</th><th>2</th><th>3</th><th>4</th></tr>
<tr><td>${U2} đo (V)</td><td>8,4</td><td>7,1</td><td>5,9</td><td>4,8</td><td>3,9</td></tr>
<tr><td>So với lí tưởng (%)</td><td></td><td></td><td></td><td></td><td></td></tr></table>
<div class="hint" style="margin-top:.4mm">Số liệu minh hoạ, không phải số đo thật.</div></div>
<div><div><b>Rút ra:</b> khe hở càng lớn, từ thông ${f(10)} càng nhiều, ${U2} càng ${f(12)} ⇒ sạc không dây phải ${f(20)}.</div></div></div>
${h3(4, 'Làm nhanh', '2·4')}
${box(cau(`<b>Câu 1.</b> ${m('N_1=20')} vòng, ${m('N_2=15')} vòng, ${V('U_1=12')}; coi hai cuộn ghép lí tưởng. Tính ${U2}.`, 1)
 + cau(`<b>Câu 2.</b> Số đo áp sát ${V('8{,}4')} lệch bao nhiêu phần trăm so với lí tưởng ${V('9{,}0')}? Vì sao luôn đo được nhỏ hơn?`, 2))}
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('DÒNG ĐIỆN FOUCAULT · BẾP TỪ')}
${h3(1, 'II.3 · Dòng điện Foucault (dòng xoáy)', '3·1')}
<div class="card" style="padding:1.2mm 3mm">
<div>Là dòng điện cảm ứng sinh ra trong lòng ${f(26)} khi khối đó ${f(26)} trong từ trường hoặc nằm trong từ trường ${f(20)}.</div>
<div>Dòng khép kín trong khối, cường độ lớn vì ${f(34)}.</div>
<div>Hai tác dụng đi cùng nhau: <b>1)</b> ${f(30)} (Lenz: chống lại chuyển động) · <b>2)</b> ${f(30)}: ${m('Q=')} ${f(16)}</div>
<div>Giảm dòng Foucault có hại: lõi máy biến áp, lõi động cơ ghép từ ${f(50)}.</div>
</div>
${h3(2, 'Thí nghiệm: con lắc tấm nhôm giữa hai cực nam châm', '3·2')}
<div class="fig-side" style="${fs(42)}"><div>
<div style="font-size:var(--fs-sm);line-height:1.35;margin-bottom:.6mm">Tấm nhôm ${nw('100 × 60 × 3 mm')} treo bằng hai dây dài 40 cm. Đếm số lần tấm qua vị trí thấp nhất tới khi tắt hẳn, bấm giờ.</div>
<table class="tbl-ct"><tr><th style="width:30mm">Trường hợp</th><th>Số lần qua</th><th>Thời gian (s)</th><th>s / lần qua</th></tr>
<tr><td>Không nam châm</td><td>42</td><td>27</td><td></td></tr>
<tr><td>Tấm liền khối</td><td>6</td><td>3,8</td><td></td></tr>
<tr><td>Tấm xẻ rãnh</td><td>21</td><td>13,3</td><td></td></tr></table>
<div style="margin-top:.6mm"><b>Quan sát:</b> cột cuối ba hàng ${f(22)} (nửa chu kì gần như không đổi); tấm ${f(22)} tắt nhanh nhất.</div>
<div><b>Rút ra:</b> rãnh xẻ cắt đường dòng Foucault ⇒ điện trở ${f(12)} ⇒ dòng ${f(12)} ⇒ lực hãm ${f(14)}.</div></div>
${H.conLac()}</div>
${h3(3, 'II.4 · Bếp từ: đo hiệu suất khi đun 1 lít nước', '3·3')}
<div class="card fig-side" style="${fs(44)};padding:1.2mm 3mm"><div>
<div>Cuộn dây dưới mặt kính nuôi bằng dòng ${f(22)} tần số cao 20–30 kHz ⇒ từ thông qua đáy nồi ${f(18)} ⇒ dòng ${f(20)} trong đáy nồi toả nhiệt Joule.</div>
<div style="font-size:var(--fs-sm);line-height:1.35;margin:.6mm 0">Nước ${m('m=1{,}0')} kg, ${nw(m('c=4\\,180\\ \\mathrm{J/(kg{\\cdot}K)}'))}, đun ${m('\\tau=120')} s, cùng nồi thép có nắp; ${m('H=\\dfrac{mc\\Delta t}{P\\tau}')}.</div>
<table class="tbl-ct"><tr><th>Bếp</th><th>${m('P')} đo (W)</th><th>${m('t_1\\to t_2')} (°C)</th><th>Mặt bếp (°C)</th><th style="width:16mm">${m('H')}</th></tr>
<tr><td>Bếp từ</td><td>1 950</td><td>25,0 → 72,6</td><td>38</td><td></td></tr>
<tr><td>Điện trở</td><td>1 980</td><td>25,0 → 60,2</td><td>260</td><td>0,62</td></tr></table>
<div style="margin-top:.6mm"><b>Rút ra:</b> nhiệt sinh ngay trong ${f(22)}; mặt kính chỉ ${f(16)} nhờ nồi truyền xuống.</div></div>
${H.bepCat()}</div>
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('BA CÁI BẪY · TRẢ BÀI · TỰ KIỂM TRA')}
${h3(1, 'III · Ba cái bẫy hay sập', '4·1')}
<div class="card fig-side" style="${fs(40)};padding:1mm 3mm"><div>
<div class="trap">${ck}<span><b>“Bếp từ truyền nhiệt từ mặt bếp sang nồi.”</b> Bếp từ không có mâm nóng, mặt kính chỉ ấm nhờ nồi. Dùng nồi đáy nhiễm từ (gang, thép); nồi nhôm vẫn có dòng xoáy nhưng toả nhiệt rất ít.</span></div>
<div class="trap">${ck}<span><b>“Cứ ở trong từ trường là có dòng Foucault.”</b> Điều kiện là từ thông qua khối <b>biến thiên</b>: nam châm mạnh đứng yên cạnh tấm nhôm đứng yên không gây dòng.</span></div>
<div class="trap">${ck}<span><b>“Phanh điện từ dừng được xe ở mọi tốc độ.”</b> Suất điện động cảm ứng tỉ lệ với tốc độ biến thiên từ thông, nên lực hãm yếu dần khi xe chậm; dừng hẳn và giữ xe trên dốc là việc của phanh ma sát.</span></div></div>
${H.phanh()}</div>
${h3(2, 'IV · Trả bài 6 câu', '4·2')}
${box(`${tb('1. Dây đàn thép dao động thành dòng điện thế nào?')}${lines(2)}
${tb('2. Sạc không dây theo nguyên lí nào? Hai cuộn dây tên gì?')}${lines(1)}
${tb('3. Công thức suất điện động cảm ứng và máy biến áp lí tưởng.')}${lines(2)}
${tb('4. Dòng điện Foucault là gì? Hai tác dụng của nó?')}${lines(2)}
${tb('5. Vì sao tấm có rãnh xẻ dao động lâu hơn tấm liền khối?')}${lines(2)}
${tb('6. Vì sao lõi máy biến áp ghép từ lá thép mỏng cách điện?')}${lines(2)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/6 câu · chưa thuộc: ${f(25)} ${nw(`→ đọc lại ô ${f(12)} Tập`)}</div>
${h3(3, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '4·3')}
${rkHai([1, 2, 3, 4], [5, 6, 7])}
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TOÁN MẪU · BÀI TẬP VỀ NHÀ · THỬ THÁCH')}
${h3(1, 'V · Bài toán mẫu: đế sạc không dây', '5·1')}
<div class="card soft" style="padding:1.2mm 3mm">Đế sạc: cuộn sơ cấp ${m('N_1=20')} vòng nối nguồn xoay chiều ${V('U_1=12')}; cuộn sau lưng điện thoại ${m('N_2=15')} vòng. Áp sát, vôn kế (±0,1 V) chỉ ${V('8{,}4')}; kê bìa thì số đo như bảng ở Tập 74·3.
<b>a)</b> lí tưởng ${U2} bằng bao nhiêu; số đo lệch mấy % · <b>b)</b> vì sao ${U2} giảm nhanh khi tăng ${m('d')}; năng lượng mất thành gì · <b>c)</b> ở ${m('d=2')} cm, điện áp còn mấy % so với lí tưởng · <b>d)</b> pin cần nhận ${nw('36 000 J')}, công suất nạp 8 W: nạp đầy mất bao lâu</div>
<table><tr><th style="width:50mm">Câu trong đề</th><th>Dữ liệu → kiến thức</th></tr>
<tr><td>“sơ cấp 20 vòng; thứ cấp 15 vòng”</td><td>${m('N_2/N_1=0{,}75')} → ${m('U_2=U_1N_2/N_1')}</td></tr>
<tr><td style="height:6.5mm">“áp sát 8,4 V; kê bìa”</td><td></td></tr>
</table>
<div class="fig-side" style="${fs(46)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm 2mm">
${wl(`a) ${m('U_2=')}`, 3)}${wl('b)', 3)}${wl('c)', 1)}${wl(`d) ${m('t=')}`, 1)}</div>${H.uTheoD()}</div>
${h3(2, 'Điền bước còn thiếu: đế sạc khác', '5·2')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div class="ln" style="height:auto;min-height:5mm"><b>Đề:</b> ${m("N_1'=25")} vòng, ${V("U_1'=10")}, ${m("N_2'=10")} vòng; áp sát, vôn kế chỉ ${V('3{,}6')}.</div>
<div class="ln"><b>Bước 1 (cho sẵn):</b> ${m("N_2'/N_1'=10/25=0{,}4")}</div>
${wl(`Bước 2: lí tưởng ${m("U_2'=")}`, 1)}${wl('Bước 3: 3,6 V đạt bao nhiêu % giá trị lí tưởng?', 1)}</div>
${K.btvn().replace('<i>1</i>', '<i>3</i>')}
${h3(4, 'Thử thách phân tầng', '5·4')}
${box(wl(`${m('\\bigstar')} Sơ cấp 100 vòng nối ${V('24')}, thứ cấp 25 vòng. ${U2} bằng bao nhiêu?`, 1)
 + wl(`${m('\\bigstar\\bigstar')} Vì sao phanh điện từ yếu hẳn khi xe chậm?`, 1)
 + cau(`${m('\\bigstar\\bigstar\\bigstar')} Vì sao lõi máy biến áp ghép từ lá thép mỏng cách điện mà không đúc đặc?`, 1))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Đàn ghi ta điện: dòng cảm ứng, suất điện động trung bình',
    de: `Dây La của đàn ghi ta điện dao động với tần số ${nw(m('110\\ \\mathrm{Hz}'))} ngay trên bộ cảm ứng: nam châm quấn cuộn dây ${nw('6 000 vòng')} nối máy tăng âm; dây không chạm cuộn dây, cuộn dây đứng yên. Trong mỗi nửa chu kì, từ thông qua mỗi vòng biến thiên ${nw(m('|\\Delta\\Phi|=0{,}30\\ \\mu\\mathrm{Wb}'))} (${muWb}).<br><b>a)</b> trong cuộn dây có dòng cảm ứng không; nếu có, tần số bằng bao nhiêu<br><b>b)</b> độ lớn suất điện động cảm ứng trung bình trong nửa chu kì đó`,
    nd: `Có dòng khi từ thông ${f(18)}; ${nw(`${m('\\Delta t=')} ${f(14)}`)}; ${nw(`${m('|e_c|=')} ${f(20)}`)}`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b'], gi: 4, fig: H.pickup('Cuộn dây đứng yên, dây thép rung.') },
  { t: 'Dạng 2 · Trung bình · Sạc không dây: điện áp lí tưởng và số đo',
    de: `Đế sạc: cuộn sơ cấp ${m('N_1=24')} vòng nối nguồn xoay chiều ${V('U_1=12')}; cuộn thứ cấp sau lưng điện thoại ${m('N_2=16')} vòng; đồng trục, không lõi sắt chung. Áp sát, vôn kế (±0,1 V) chỉ ${V('7{,}2')}.<br><b>a)</b> coi ghép lí tưởng, tính ${U2}<br><b>b)</b> số đo 7,2 V bằng bao nhiêu % giá trị lí tưởng; vì sao nhỏ hơn<br><b>c)</b> kê hai tấm bìa dày 1 cm, vôn kế chỉ ${V('5{,}4')}: bằng bao nhiêu % lí tưởng`,
    nd: `${nw(`${m('U_2=')} ${f(20)}`)}; phần trăm = ${f(18)}; nhỏ hơn vì từ thông ${f(12)}`, a: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], cot: 2, gi: 5, fig: H.sacKhongDay('Kê hai tấm bìa: khe 2 cm.', { d: '2 cm', bia: true }) },
  { t: 'Dạng 3 · Khá · Dòng Foucault: điều kiện, lực hãm, toả nhiệt',
    de: `Tấm nhôm liền khối ${nw('100 × 60 × 3 mm')} (bỏ qua lực cản không khí): (1) nằm yên cạnh nam châm đứng yên; (2) rơi thẳng đứng qua khe giữa hai cực nam châm mạnh, mặt tấm vuông góc đường sức; (3) nằm yên giữa hai cực nam châm điện có dòng nuôi tăng dần; (4) nằm yên trong lò nướng nóng, không có nam châm.<br><b>a)</b> dòng Foucault xuất hiện ở những tình huống nào<br><b>b)</b> so với rơi tự do, tấm ở (2) rơi nhanh hơn, chậm hơn hay như nhau<br><b>c)</b> cơ năng mất đi ở (2) chuyển thành dạng năng lượng nào<br><b>d)</b> tấm cùng cỡ xẻ vài rãnh song song, ở (2) rơi nhanh hơn hay chậm hơn tấm liền khối`,
    nd: `Có dòng khi từ thông qua khối ${f(18)}; Lenz: lực từ ${f(18)} chuyển động; ${nw(`${m('I=|e_c|/R')}`)}`, a: ['a', 'b', 'c', 'd'], cot: 2, gi: 5, fig: H.tamRoi() },
  { t: 'Dạng 4 · Khó · Bếp từ: chọn nồi, nhiệt lượng, thời gian đun',
    de: `Bếp từ ghi ${nw('2 000 W')} (công suất điện tiêu thụ), hiệu suất 80 % (nhiệt nước nhận / điện năng tiêu thụ). Có hai nồi cùng cỡ: nồi nhôm và nồi gang. Đun ${nw('1,2 lít')} nước từ ${nw('25 °C')} đến sôi (${nw('100 °C')}); ${DN}, ${cN}.<br><b>a)</b> nên dùng nồi nào để đun nhanh hơn; vì sao<br><b>b)</b> nhiệt lượng nước nhận được<br><b>c)</b> thời gian đun sôi nước`,
    nd: `${nw(`${m('m=DV=')} ${f(14)}`)}; ${nw(`${m('Q=mc\\Delta t')}`)}; ${nw(`${m('P_{\\text{ích}}=')} ${f(12)}`)}; ${nw(`${m('t=')} ${f(14)}`)}`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'], cot: 2, gi: 5, fig: H.bepCat('Nồi đặt trên bếp từ.') },
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
  tieuDe: ['DẠNG 1–2', 'DẠNG 3–4'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Dây Mi của đàn ghi ta điện dao động với tần số ${nw(m('82\\ \\mathrm{Hz}'))} trên bộ cảm ứng có cuộn dây ${nw('5 000 vòng')} đứng yên. Trong mỗi nửa chu kì, từ thông qua mỗi vòng biến thiên ${nw(m('0{,}40\\ \\mu\\mathrm{Wb}'))} (${muWb}).<br><b>a)</b> tần số dòng cảm ứng trong cuộn dây<br><b>b)</b> thời gian nửa chu kì (ms)<br><b>c)</b> độ lớn suất điện động cảm ứng trung bình trong nửa chu kì`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 1 · Bài 2', de: `Một dây đàn dao động với tần số ${nw(m('196\\ \\mathrm{Hz}'))} trên bộ cảm ứng có cuộn dây ${nw('4 000 vòng')}; suất điện động cảm ứng trung bình trong mỗi nửa chu kì đo được ${V('0{,}50')} (${muWb}).<br><b>a)</b> thời gian nửa chu kì (ms)<br><b>b)</b> độ biến thiên từ thông qua một vòng trong nửa chu kì (${m('\\mu')}Wb)<br><b>c)</b> dây rung với tần số gấp đôi, ${dPhi} mỗi nửa chu kì như cũ: suất điện động trung bình`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 2 · Bài 1', de: `Đế sạc không dây: cuộn sơ cấp ${m('N_1=30')} vòng nối ${V('U_1=15')}, cuộn thứ cấp ${m('N_2=18')} vòng, không lõi sắt chung.<br><b>a)</b> coi ghép lí tưởng, tính ${U2}<br><b>b)</b> áp sát, vôn kế chỉ ${V('8{,}6')}: bằng bao nhiêu % lí tưởng<br><b>c)</b> kê bìa dày 1 cm, vôn kế chỉ ${V('6{,}3')}: bằng bao nhiêu % lí tưởng`, fig: H.sacKhongDay('Hai cuộn, khe d.'), fw: 34, o: ['a', 'b', 'c'] },
    { t: 'Dạng 2 · Bài 2', de: `Máy biến áp trong cục sạc: cuộn sơ cấp ${nw('1 100 vòng')} nối điện lưới ${V('U_1=220')}; coi gần đúng lí tưởng.<br><b>a)</b> muốn ${V('U_2=5{,}0')} thì cuộn thứ cấp phải có bao nhiêu vòng<br><b>b)</b> quấn nhầm thành 30 vòng: ${U2} khi đó<br><b>c)</b> đây là máy tăng áp hay hạ áp`, o: ['a', 'b', 'c'] },
    nhap(8),
  ], [
    { t: 'Dạng 3 · Bài 1', de: `Thả một nam châm nhỏ rơi theo phương thẳng đứng trong lòng một ống đồng dài dựng đứng (đồng không nhiễm từ, dẫn điện tốt; bỏ qua lực cản không khí, nam châm không chạm thành ống).<br><b>a)</b> trong thành ống có dòng Foucault không<br><b>b)</b> nam châm rơi nhanh hơn, chậm hơn hay như rơi tự do<br><b>c)</b> thay bằng ống nhựa cùng cỡ: nam châm rơi thế nào<br><b>d)</b> ống đồng xẻ một rãnh dọc suốt chiều dài: rơi nhanh hơn hay chậm hơn ống liền`, fig: H.ongDong(), fw: 22, o: ['a', 'b', 'c', 'd'], ow: { a: 18, b: 22, c: 30, d: 22 } },
    { t: 'Dạng 3 · Bài 2', de: `So sánh hai lõi cùng cỡ của một máy biến áp nối điện xoay chiều: lõi thép đúc đặc và lõi ghép từ nhiều lá thép mỏng sơn cách điện. Công tơ điện kiểu cũ có đĩa nhôm quay giữa hai cực một nam châm đứng yên.<br><b>a)</b> lõi nào nóng lên nhiều hơn khi máy chạy<br><b>b)</b> điện trở của mạch dòng xoáy trong lõi nào lớn hơn<br><b>c)</b> trong đĩa nhôm đang quay có dòng Foucault không<br><b>d)</b> lực từ lên dòng đó làm đĩa quay nhanh thêm hay bị hãm`, o: ['a', 'b', 'c', 'd'], ow: { a: 22, b: 26, c: 16, d: 22 } },
    { t: 'Dạng 4 · Bài 1', de: `Bếp từ ghi ${nw('1 800 W')} (điện tiêu thụ), hiệu suất 85 %. Đun ${nw('1,5 lít')} nước từ ${nw('20 °C')} đến ${nw('100 °C')}; ${DN}, ${cN}. Có ba nồi cùng cỡ: nhôm, thuỷ tinh chịu nhiệt, inox đáy nhiễm từ.<br><b>a)</b> dùng được nồi nào<br><b>b)</b> nhiệt lượng nước nhận được (kJ)<br><b>c)</b> thời gian đun (s)`, o: ['a', 'b', 'c'], ow: { a: 42 } },
    { t: 'Dạng 4 · Bài 2', de: `Bếp từ ghi ${nw('2 000 W')} (điện tiêu thụ) đun ${nw('2,0 lít')} nước từ ${nw('25 °C')} đến sôi (${nw('100 °C')}) hết ${nw('6,0 phút')}; ${DN}, ${cN}.<br><b>a)</b> nhiệt lượng nước nhận được (kJ)<br><b>b)</b> điện năng bếp tiêu thụ (kJ)<br><b>c)</b> hiệu suất của bếp`, o: ['a', 'b', 'c'] },
    nhap(4),
  ]],
  dap: [
    `D1·1: a) 82 Hz · b) 6,1 ms · c) 0,33 V &nbsp;|&nbsp; D1·2: a) 2,6 ms · b) 0,32 ${m('\\mu')}Wb · c) 1,0 V &nbsp;|&nbsp; D2·1: a) 9,0 V · b) 96 % · c) 70 % &nbsp;|&nbsp; D2·2: a) 25 vòng · b) 6,0 V · c) hạ áp`,
    `D3·1: a) có · b) chậm hơn · c) như rơi tự do · d) nhanh hơn &nbsp;|&nbsp; D3·2: a) lõi đặc · b) lõi lá thép mỏng · c) có · d) bị hãm &nbsp;|&nbsp; D4·1: a) nồi inox đáy nhiễm từ · b) 504 kJ · c) ≈ 329 s &nbsp;|&nbsp; D4·2: a) 630 kJ · b) 720 kJ · c) 87,5 %`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [2, 2], kq: [[1, 2], [3, 4]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'ghi ta điện 1·4 · dây rung 2·1 · sạc không dây 2·2 · khe hở 2·3 · Foucault 3·1 · tấm nhôm 3·2 · bếp từ 3·3 · bẫy 4·1 · bài mẫu 5·1 · dạng 1–2 → 6·1 · dạng 3–4 → 7·1',
  out: process.argv[2] ? resolve(process.argv[2]) : resolve(HERE, 'out/ruot-tap-vl12-c3-bai15.pdf'),
});
