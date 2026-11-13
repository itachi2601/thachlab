// Ruột tập VL10 – Bài 17 · Trọng lực và lực căng (lesson id 62). Quyển Chương 3 lớp 10: bài 13 = tr. 1–12 → bài 17 = tr. 49–60.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l10-bai17.mjs (SVG tự vẽ + ảnh dây dọi thật book/assets/anh-that/day-doi.jpg, CC BY-SA 4.0).
// Nội dung theo bài web (book/cache/62.json, tải từ DB 13/11/2026): mục tiêu, dự đoán đĩa CD, II.1–II.5, ba thí nghiệm (dây dọi,
// lực kế – quả nặng, lực kế qua ròng rọc), ba bẫy, Trả bài 6 câu, bài toán mẫu A–B qua ròng rọc, thử thách, 5 dạng bài tập mẫu.
// Đáp số Bài tương tự (tuongTu.dap) tính bằng Python 13/11/2026.
// Chạy: node scripts/ruot-tap/l10-bai17.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl10-bai17.pdf
//       node scripts/ruot-tap/l10-bai17.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l10-bai17/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL10b17 as H } from './hinh-l10-bai17.mjs';

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
  const out = resolve(HERE, 'out/hinh-l10-bai17'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 17, lid: 62, ten: 'TRỌNG LỰC VÀ LỰC CĂNG', lop: 10, baiDau: 13, sub: 'Vật lí 10 · Chương 3: Động lực học' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const g10 = nw(m('g=10\\ \\mathrm{m/s^2}'));
const g98 = nw(m('g=9{,}8\\ \\mathrm{m/s^2}'));
const vP = m('\\vec P'), vT = m('\\vec T');
const kg = (s) => nw(m(`${s}\\ \\mathrm{kg}`)), N = (s) => nw(m(`${s}\\ \\mathrm{N}`)), ms2 = (s) => nw(m(`${s}\\ \\mathrm{m/s^2}`));

// Bài tương tự giải vào vở: 1 cột, ô đáp số cuối đúng dòng của ý (cùng cách l10-bai23.mjs)
const ttHaiCot = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm}.yo .oo{flex:none;display:flex;gap:3mm}.yo{line-height:1.35}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';

const p1 = `${ttHaiCot}<section class="page">
${head('BÀI 17 · TRỌNG LỰC VÀ LỰC CĂNG', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Nêu đủ bốn đặc điểm của <b>trọng lực</b>; tìm <b>trọng tâm</b> của vật phẳng`)}
${dong(`${ck}Phân biệt <b>khối lượng</b> với <b>trọng lượng</b>`)}
${dong(`${ck}Vẽ đúng <b>lực căng</b> ${vT} của dây: điểm đặt, phương, chiều`)}
${dong(`${ck}Giải bài <b>hệ vật nối dây qua ròng rọc</b>: tìm gia tốc và lực căng`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Đĩa CD (khoét lỗ giữa) treo trên đinh bằng dây buộc ở mép. Đĩa lắc vài cái rồi đứng yên; dây kéo dài xuống luôn đi qua tâm lỗ, chỗ không có nhựa. <b>Trọng lực tác dụng lên đĩa đặt ở đâu?</b></p>
<div class="fig-side" style="${fs(30)}"><div>
${opt('A', 'Ở điểm buộc dây trên mép đĩa, vì dây giữ đĩa ở đó')}
${opt('B', 'Ở tâm lỗ, dù chỗ đó không có nhựa')}
${opt('C', 'Rải đều trên vành, nên không có một điểm đặt nào')}
${opt('D', 'Ở điểm thấp nhất của mép đĩa, vì gần đất nhất')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 2)}</div>
${H.diaCD('Đĩa treo đứng yên trên đinh.')}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(2)}</div>
${h3(4, 'II.1 · Trọng lực', '1·4')}
<div class="card fig-side" style="${fs(28)};padding:1.2mm 3mm"><div>
<div>Trọng lực là lực ${f(25)} giữa Trái Đất và vật, kí hiệu ${vP}.</div>
<div>Điểm đặt: ${f(25)} &nbsp;${m('G')} của vật.</div>
<div>Phương: ${f(25)} · Chiều: ${f(25)}</div>
<div style="margin:.6mm 0">Độ lớn: ${m('P=')} ${f(14)} &nbsp; (${m('P')}: ${f(12)}; ${m('m')}: ${f(12)}; ${m('g')}: ${f(14)})</div>
<div>Dây dọi của thợ xây chỉ phương ${f(25)}.</div>
${wl('Ở hai phía Trái Đất, hai dây dọi có song song không? Vì sao?', 2)}</div>
${H.dayDoi()}</div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('TRỌNG TÂM · TRỌNG LƯỢNG')}
${h3(1, 'II.2 · Trọng tâm', '2·1')}
<div class="card" style="padding:1.2mm 3mm">
<div>Trọng tâm là ${f(25)} của trọng lực.</div>
<div>Vật phẳng, mỏng, đồng chất, đối xứng: trọng tâm ở ${f(25)} (thước thẳng: ${f(18)}; đĩa tròn: ${f(18)}).</div>
<div>Vị trí trọng tâm phụ thuộc ${f(25)}; trọng tâm có thể nằm ${f(25)} vật.</div></div>
${h3(2, 'Thí nghiệm: tìm trọng tâm tấm bìa bằng dây dọi', '2·2')}
<div class="card fig-side" style="${fs(42)};padding:1.2mm 3mm"><div>
<div><b>Làm:</b> đục lỗ ${m('A')}, ${m('B')}, ${m('C')} gần mép bìa. Treo bìa ở ${m('A')} lên đinh, buộc dây dọi cùng đinh, kẻ theo dây. Làm lại với ${m('B')}, rồi với ${m('C')} để kiểm tra.</div>
<div><b>Quan sát:</b> ba đường kẻ ${f(25)}; đặt điểm đó lên đầu bút chì, bìa ${f(25)}.</div>
<div><b>Rút ra:</b> vật treo đứng yên khi trọng tâm nằm ${f(25)} điểm treo.</div>
${wl('Cần ít nhất mấy lần treo để tìm G? Lần thứ ba để làm gì?', 2)}</div>
${H.biaDayDoi()}</div>
${h3(3, 'II.3 · Trọng lượng', '2·3')}
<table><tr><th style="width:30mm"></th><th>Khối lượng ${m('m')}</th><th>Trọng lượng ${m('P')}</th></tr>
<tr><td>Đơn vị · đo bằng</td><td></td><td></td></tr>
<tr><td>Đổi chỗ đặt vật</td><td></td><td></td></tr>
<tr><td>Vô hướng hay vectơ</td><td></td><td></td></tr></table>
<div style="margin-top:.6mm">Gần mặt đất ${m('g\\approx')} ${f(14)}&nbsp;${m('\\mathrm{m/s^2}')}; ${m('g')} hơi khác theo ${f(18)} và ${f(18)}. ${nw(`${m('1\\ \\mathrm{N/kg}=1')} ${f(14)}`)}</div>
${h3(4, 'Thí nghiệm: treo các quả nặng 50 g vào lực kế', '2·4')}
<div class="fig-side" style="${fs(36)}"><div>
<table class="tbl-ct"><tr><th>${m('m\\ (\\mathrm{kg})')}</th><th>${m('P')} đọc ${m('(\\mathrm N)')}</th><th>${m('P/m\\ (\\mathrm{N/kg})')}</th></tr>
<tr><td>0,050</td><td>0,50</td><td></td></tr>
<tr><td>0,100</td><td>0,95</td><td></td></tr>
<tr><td>0,150</td><td>1,45</td><td></td></tr>
<tr><td>0,200</td><td>1,95</td><td></td></tr></table>
<div style="margin-top:.6mm"><b>Rút ra:</b> ${m('P')} ${f(25)} với ${m('m')}; ${m('P/m')} gần bằng ${f(12)}.</div>
${wl('Hàng nào kém tin cậy nhất? Vì sao? (mỗi số đọc sai tới ± 0,05 N)', 2)}</div>
${H.lucKe()}</div>
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('LỰC CĂNG DÂY · HỆ VẬT NỐI DÂY QUA RÒNG RỌC')}
${h3(1, 'II.4 · Lực căng dây', '3·1')}
<div class="card fig-side" style="${fs(30)};padding:1.2mm 3mm"><div>
<div>Dây bị kéo thì tại mọi điểm trên dây xuất hiện lực căng ${vT}.</div>
<div>Điểm đặt: ${f(25)}</div>
<div>Phương: ${f(25)} · Chiều: ${f(25)}</div>
<div>Dây chỉ ${f(14)}, không ${f(14)}.</div>
<div>Dây nhẹ (khối lượng không đáng kể): ${m('T')} ${f(25)} ở mọi điểm, kể cả khi vắt qua ròng rọc nhẹ, nhẵn.</div>
<div>Đèn đứng yên: ${m('T')} ${f(12)} ${m('P')} của đèn.</div></div>
${H.denTreo()}</div>
${h3(2, 'II.5 · Hệ vật nối dây qua ròng rọc', '3·2')}
<div class="card fig-side" style="${fs(40)};padding:1.2mm 3mm"><div>
<div>Dây không dãn: các vật có cùng ${f(25)}.</div>
<div>Dây nhẹ, ròng rọc nhẹ nhẵn: ${nw(`${m('T_1')} ${f(10)} ${m('T_2')}`)}.</div>
<div>Cách giải: viết ${m('\\vec F=m\\vec a')} ${f(25)} cho từng vật, chiều dương theo ${f(25)} của vật đó; ${f(14)} các phương trình để khử ${m('T')}.</div></div>
${H.heLyThuyet()}</div>
${h3(3, 'Thí nghiệm: lực kế kéo dây vắt qua ròng rọc', '3·3')}
<div class="card fig-side" style="${fs(40)};padding:1.2mm 3mm"><div>
<div><b>Làm:</b> treo quả nặng ${N('1{,}0')} vào một đầu dây vắt qua ròng rọc cố định; đầu kia móc lực kế, giữ quả nặng đứng yên. Kéo lực kế theo ba hướng 1, 2, 3.</div>
<div><b>Quan sát:</b> cả ba lần lực kế chỉ khoảng ${f(12)} N.</div>
<div><b>Rút ra:</b> ròng rọc đổi ${f(25)} của dây nhưng lực căng hai bên ${f(25)}.</div></div>
${H.rongRocLucKe()}</div>
${h3(4, 'III · Ba cái bẫy hay sập', '3·4')}
<div class="card" style="padding:1mm 3mm">
<div class="trap">${ck}<span><b>“Em nặng 50 kg.”</b> kg là đơn vị của ${f(25)}; trọng lượng tính bằng ${f(10)}.</span></div>
<div class="trap">${ck}<span><b>“Lực căng luôn bằng trọng lượng vật treo.”</b> ${m('T=P')} chỉ khi vật ${f(25)}.</span></div>
<table style="margin:.4mm 0 .8mm"><tr><th style="width:62mm">Gia tốc của vật treo</th><th>Chiều dương theo ${m('\\vec a')}, định luật 2</th><th style="width:16mm">So ${m('T')}, ${m('P')}</th></tr>
<tr><td>${m('\\vec a')} hướng lên (lên nhanh dần, xuống chậm dần)</td><td>${m('T=m(g')}${f(8)}${m('a)')}</td><td></td></tr>
<tr><td>${m('\\vec a')} hướng xuống (xuống nhanh dần, lên chậm dần)</td><td>${m('T=m(g')}${f(8)}${m('a)')}</td><td></td></tr></table>
<div class="fig-side" style="${fs(24)};gap:2mm"><div class="trap" style="margin:0">${ck}<span><b>“Vẽ ${vT} chĩa vào vật.”</b> Gốc ${vT} ở ${f(25)}, mũi chĩa ${f(25)}. Con lắc lệch: vẽ ${vT} lên quả cầu ở hình bên.</span></div>${H.conLac('')}</div></div>
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('TRẢ BÀI · TỰ KIỂM TRA · BÀI TOÁN MẪU')}
${h3(1, 'IV · Trả bài 6 câu', '4·1')}
${box(`${tb('1. Trọng lực là gì? Nêu bốn đặc điểm.')}${lines(1)}
${tb('2. Trọng tâm vật phẳng đối xứng ở đâu? Có luôn nằm trên vật không?')}${lines(1)}
${tb('3. Cách tìm trọng tâm tấm bìa bằng dây dọi?')}${lines(1)}
${tb('4. Trọng lượng khác khối lượng ở những điểm nào?')}${lines(1)}
${tb('5. Lực căng dây: điểm đặt, phương, chiều?')}${lines(1)}
${tb('6. Hệ vật nối dây nhẹ không dãn qua ròng rọc: hai vật giống nhau ở điều gì?')}${lines(1)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/6 câu · chưa thuộc: ${f(25)} ${nw(`→ đọc lại ô ${f(12)} Tập`)}</div>
${h3(2, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '4·2')}
${rkHai([1, 2, 3], [4, 5, 6])}
${h3(3, 'V · Bài toán mẫu: khối trên bàn nối vật treo', '4·3')}
<div class="card soft" style="padding:1.2mm 3mm">Khối ${m('A')} khối lượng ${kg('2')} nằm trên bàn ngang nhẵn, nối bằng dây nhẹ, không dãn vắt qua ròng rọc nhẹ ở mép bàn với vật ${m('B')} khối lượng ${kg('0{,}5')} treo thẳng đứng. Thả hệ từ nghỉ, bỏ qua mọi ma sát, lấy ${g10}. Tính gia tốc của hệ và lực căng dây.</div>
<table><tr><th style="width:50mm">Câu trong đề</th><th>Dữ liệu → kiến thức</th></tr>
<tr><td>“vật ${m('B')} … ${kg('0{,}5')} treo”</td><td>${m('P_B=m_Bg=5\\ \\mathrm N')}</td></tr>
<tr><td style="height:6.5mm">“bàn ngang nhẵn”</td><td></td></tr>
<tr><td style="height:6.5mm">“dây nhẹ, không dãn … ròng rọc nhẹ”</td><td></td></tr>
<tr><td style="height:6.5mm">“gia tốc … lực căng”</td><td></td></tr></table>
<div class="fig-side" style="${fs(48)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl(`Vật ${m('A')} (chiều dương về phía ròng rọc):`, 1)}${wl(`Vật ${m('B')} (chiều dương hướng xuống):`, 1)}${wl(`Cộng hai phương trình, tìm ${m('a')}:`, 2)}${wl(`Lực căng ${m('T')}; so ${m('T')} với ${m('P_B')}:`, 2)}</div>${H.vdMau()}</div>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TẬP VỀ NHÀ · THỬ THÁCH · MANG VỀ')}
${K.btvn()}
${h3(2, 'Điền bước còn thiếu: cùng hình, đổi số', '5·2')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div class="ln">${m('m_A=3\\ \\mathrm{kg}')}, ${m('m_B=1\\ \\mathrm{kg}')}, ${g10}. <b>Bước 1 (cho sẵn):</b> ${m('P_B=m_Bg=10\\ \\mathrm N')}</div>
${wl(`Bước 2: ${m('a=P_B/(m_A+m_B)=')}`, 1)}${wl(`Bước 3: ${m('T=')}`, 1)}</div>
${h3(3, 'Thử thách phân tầng', '5·3')}
<div class="fig-side" style="${fs(38)}">${box(wl(`${m('\\bigstar')} Vật ${kg('5')} ở nơi ${g98}: trọng lượng bao nhiêu?`, 2)
 + wl(`${m('\\bigstar\\bigstar')} Thang máy kéo thùng hàng ${kg('50')} đi <b>xuống, chậm dần</b> với ${m('a=1\\ \\mathrm{m/s^2}')} (${g10}). Lực căng cáp?`, 3)
 + wl(`${m('\\bigstar\\bigstar\\bigstar')} Hai vật ${kg('3')} và ${kg('2')} treo hai đầu dây vắt qua ròng rọc cố định nhẹ (${g10}). Tìm ${m('a')} và ${m('T')}.`, 4))}${H.atwoodTT()}</div>
${h3(4, 'Câu đổi chiều (bài toán mẫu)', '5·4')}
${box(wl(`Đề gốc (${kg('2')}, ${kg('0{,}5')}, ${g10}), tay giữ chặt khối ${m('A')}: lực căng bằng bao nhiêu? Lớn hơn hay nhỏ hơn ${N('4')} lúc thả tay?`, 2)
 + wl(`Thay ${m('A')} bằng khối ngày càng nặng: ${m('T')} tăng hay giảm, có vượt ${N('5')} không? Gợi ý: xét phương trình của vật ${m('B')}.`, 2))}
${h3(5, 'VI · Mang về: điều em dễ quên nhất', '5·5')}
${box(wl('1.', 3) + wl('2.', 3) + wl('3.', 3))}
${foot(5)}</section>`;

// Ô đáp số đặt cuối đúng dòng của ý (như trang Bài tương tự) thay hàng ô đáp số của khung → mỗi dạng bớt 8,5 mm, trang 6 vừa 3 dạng.
const oY = (s, o, w = 25) => s.split('<br>').map((p) => {
  const y = p.match(/^<b>([a-d])\)<\/b>/);
  if (!y) return `<div>${p}</div>`;
  const ls = o.filter((l) => l[0] === y[1]);
  return `<div class="yo"><span>${p}</span><span class="oo">${ls.map((l) => `<span class="nw"><b>${l})</b>${f(w)}</span>`).join('')}</span></div>`;
}).join('');
const bt = (d) => ({ ...d, de: oY(d.de, d.a, d.ow ?? 25), a: [] });
const dang = [
  { t: 'Dạng 1 · Dễ · Khối lượng, trọng lượng ở từng nơi',
    de: `Xe tự hành ${kg('90')} treo đứng yên vào lực kế trên Trái Đất ${nw(`(${g98})`)} rồi trên Sao Hoả ${nw(`(${ms2('g\'=3{,}7')})`)}.<br><b>a)</b> trọng lượng của xe trên Trái Đất<br><b>b)</b> khối lượng của xe trên Sao Hoả<br><b>c)</b> trọng lượng của xe trên Sao Hoả`,
    nd: `${m('m')} ${f(18)} khi đổi nơi; ${m('P=mg')} với ${m('g')} của ${f(25)}`, a: ['a', 'b', 'c'], gi: 3 },
  { t: 'Dạng 2 · Trung bình · Vật treo có gia tốc: lực căng',
    de: `Tời nâng thùng hàng ${kg('800')} bằng cáp thép nhẹ, thẳng đứng; ${g10}. Lực căng cáp khi thùng:<br><b>a)</b> đi lên thẳng đều<br><b>b)</b> khởi động, đi lên nhanh dần với ${m('a=1{,}5\\ \\mathrm{m/s^2}')}<br><b>c)</b> sắp tới nơi, đi lên chậm dần với ${m('a=1{,}2\\ \\mathrm{m/s^2}')}<br><b>d)</b> cáp chịu tối đa ${N('9\\,000')}: cáp đứt không, ở giai đoạn nào?`,
    nd: `Lên nhanh dần ⇒ ${m('\\vec a')} hướng ${f(12)}; lên chậm dần ⇒ ${m('\\vec a')} hướng ${f(12)}`, a: ['a', 'b', 'c', 'd'], gi: 4 },
  { t: 'Dạng 3 · Trung bình · Vật trên bàn nhẵn nối vật treo qua ròng rọc',
    de: `Khối ${m('A')} (${kg('1{,}5')}) trên bàn ngang nhẵn nối với vật ${m('B')} (${kg('1{,}0')}) treo qua ròng rọc ở mép bàn; dây nhẹ không dãn, ròng rọc nhẹ; thả từ nghỉ; ${g10}.<br><b>a)</b> gia tốc của hệ<br><b>b)</b> lực căng của dây<br><b>c)</b> so sánh lực căng với trọng lượng của ${m('B')}`,
    nd: `${m('A')}: ${nw(`${m('T=')} ${f(14)}`)}; ${m('B')}: ${nw(`${m('P_B-T=')} ${f(14)}`)}; cộng để khử ${m('T')}`, a: ['a', 'b', 'c'], gi: 4, fig: H.heD3() },
];
const dang2 = [
  { t: 'Dạng 4 · Khó · Hai vật treo hai bên ròng rọc cố định',
    de: `Hai vật ${m('m_1=5{,}0\\ \\mathrm{kg}')} và ${m('m_2=3{,}0\\ \\mathrm{kg}')} buộc hai đầu dây nhẹ, không dãn, vắt qua ròng rọc cố định nhẹ, không ma sát. Giữ hai vật cùng độ cao rồi thả nhẹ; ${g10}.<br><b>a)</b> độ lớn gia tốc của mỗi vật<br><b>b)</b> lực căng của dây<br><b>c)</b> lực căng lớn hơn, nhỏ hơn hay nằm giữa trọng lượng của hai vật`,
    nd: `Vật ${f(18)} đi xuống; cộng hai phương trình: ${nw(`${m('P_1-P_2=')} ${f(25)}`)}`, a: ['a', 'b', 'c'], gi: 11, fig: H.atwoodD4(), cot: 3 },
  { t: 'Dạng 5 · Khó · Bài ngược: dây chỉ chịu lực căng tối đa',
    de: `Khối ${m('A')} (${kg('2{,}0')}) trên bàn ngang nhẵn, nối bằng dây nhẹ không dãn vắt qua ròng rọc nhẹ ở mép bàn với vật ${m('B')} treo thẳng đứng. Dây chịu tối đa ${N('12')}. Thả từ nghỉ, bỏ qua ma sát, ${g10}.<br><b>a)</b> gia tốc lớn nhất của hệ để dây không đứt<br><b>b)</b> khối lượng lớn nhất của ${m('B')} để dây không đứt`,
    nd: `${m('A')} chỉ chịu ${m('T')} ⇒ ${nw(`${m('a_{max}=')} ${f(16)}`)}; rồi xét vật ${f(10)} với ${m('T_{max}')}, ${m('a_{max}')}`, a: ['a', 'b'], gi: 10, fig: H.heD5(), cot: 2 },
];

// Bài tương tự: mỗi dạng 2 bài, giải vào vở, đáp số tính bằng Python (13/11/2026). Ô đáp số cuối đúng dòng của ý.
const ttDe = (b) => b.fig ? `<div class="fig-side" style="grid-template-columns:1fr ${b.fw}mm">${`<div>${oY(b.de, b.o, b.ow)}</div>`}${b.fig}</div>` : oY(b.de, b.o, b.ow);
const vaoVo = (ds) => ds.map((b) => (b.o ? { t: b.t, de: ttDe(b), k: 0 } : b));
const nhap = (n) => ({ t: '<span class="nhap-t">Nháp / chỗ em còn vướng</span>', de: lines(n), k: 0 });
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–3', 'DẠNG 4–5'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Nhà du hành khối lượng ${kg('60')} trên Trái Đất (${g98}) rồi lên Mặt Trăng (${ms2('g\'=1{,}6')}).<br><b>a)</b> trọng lượng trên Trái Đất<br><b>b)</b> khối lượng trên Mặt Trăng<br><b>c)</b> trọng lượng trên Mặt Trăng`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 1 · Bài 2', de: `Ở nơi ${ms2('g=9{,}78')}, treo vật đứng yên vào lực kế, lực kế chỉ ${N('19{,}56')}.<br><b>a)</b> khối lượng của vật<br><b>b)</b> trọng lượng của vật ở nơi ${ms2('g=9{,}83')}<br><b>c)</b> trọng lượng của vật trên Sao Mộc (${ms2('g=24{,}8')})`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 2 · Bài 1', de: `Thang máy cùng người tổng khối lượng ${kg('600')}, ${g10}. Lực căng cáp khi thang:<br><b>a)</b> đi lên thẳng đều<br><b>b)</b> đi xuống nhanh dần với ${m('a=0{,}8\\ \\mathrm{m/s^2}')}<br><b>c)</b> đi xuống chậm dần với ${m('a=0{,}8\\ \\mathrm{m/s^2}')}`, fig: H.toiCap('Thang đi xuống: a hướng nào?', '600 kg', true), fw: 34, o: ['a', 'b', 'c'] },
    { t: 'Dạng 2 · Bài 2', de: `Cần cẩu nâng kiện hàng ${kg('1\\,200')} bằng cáp thẳng đứng, cáp chịu tối đa ${N('14\\,000')}; ${g10}.<br><b>a)</b> lực căng khi kiện treo đứng yên<br><b>b)</b> gia tốc hướng lên lớn nhất để cáp không đứt<br><b>c)</b> lực căng khi kiện đi lên chậm dần với ${m('a=2{,}0\\ \\mathrm{m/s^2}')}`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 3 · Bài 1', de: `Khối ${m('A')} (${kg('4{,}0')}) trên bàn ngang nhẵn nối qua ròng rọc ở mép bàn với vật ${m('B')} (${kg('1{,}0')}) treo; dây nhẹ không dãn, ròng rọc nhẹ; thả từ nghỉ; ${g10}.<br><b>a)</b> gia tốc của hệ<br><b>b)</b> lực căng dây<br><b>c)</b> lực căng lớn hơn hay nhỏ hơn trọng lượng ${m('B')}`, fig: H.heTT(), fw: 40, o: ['a', 'b', 'c'] },
    { t: 'Dạng 3 · Bài 2', de: `Như bài 1 nhưng ${m('m_A=3{,}0\\ \\mathrm{kg}')}, ${m('m_B=2{,}0\\ \\mathrm{kg}')}; ${g10}.<br><b>a)</b> gia tốc của hệ<br><b>b)</b> lực căng dây<br><b>c)</b> quãng đường ${m('B')} đi được sau ${nw(m('0{,}50\\ \\mathrm s'))} kể từ lúc thả`, o: ['a', 'b', 'c'] },
  ], [
    { t: 'Dạng 4 · Bài 1', de: `Hai vật ${m('m_1=4{,}0\\ \\mathrm{kg}')} và ${m('m_2=1{,}0\\ \\mathrm{kg}')} treo hai đầu dây nhẹ không dãn vắt qua ròng rọc cố định nhẹ, nhẵn; thả từ nghỉ; ${g10}.<br><b>a)</b> độ lớn gia tốc<br><b>b)</b> lực căng dây<br><b>c)</b> so ${m('T')} với ${m('P_1')} và ${m('P_2')}`, fig: H.atwoodTT2(), fw: 34, o: ['a', 'b', 'c'], ow: 30 },
    { t: 'Dạng 4 · Bài 2', de: `Như bài 1 nhưng ${m('m_1=2{,}5\\ \\mathrm{kg}')}, ${m('m_2=1{,}5\\ \\mathrm{kg}')}; ${g10}.<br><b>a)</b> độ lớn gia tốc<br><b>b)</b> lực căng dây<br><b>c)</b> quãng đường mỗi vật đi được sau ${nw(m('1{,}0\\ \\mathrm s'))} kể từ lúc thả`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 5 · Bài 1', de: `Khối ${m('A')} (${kg('3{,}0')}) trên bàn ngang nhẵn nối qua ròng rọc ở mép bàn với vật ${m('B')} treo; dây nhẹ không dãn chịu tối đa ${N('15')}; thả từ nghỉ; ${g10}.<br><b>a)</b> gia tốc lớn nhất để dây không đứt<br><b>b)</b> khối lượng lớn nhất của ${m('B')}`, o: ['a', 'b'] },
    { t: 'Dạng 5 · Bài 2', de: `Như bài 1 nhưng ${m('m_A=4{,}0\\ \\mathrm{kg}')}, dây chịu tối đa ${N('10')}; ${g10}.<br><b>a)</b> gia tốc lớn nhất để dây không đứt<br><b>b)</b> khối lượng lớn nhất của ${m('B')}<br><b>c)</b> treo ${m('B')} ${kg('1{,}0')}: lực căng dây`, o: ['a', 'b', 'c'] },
    nhap(11),
  ]],
  dap: [
    `D1·1: a) 588 N · b) 60 kg · c) 96 N &nbsp;|&nbsp; D1·2: a) 2,0 kg · b) 19,66 N · c) 49,6 N &nbsp;|&nbsp; D2·1: a) 6000 N · b) 5520 N · c) 6480 N &nbsp;|&nbsp; D2·2: a) 12 000 N · b) 1,67 m/s² · c) 9600 N &nbsp;|&nbsp; D3·1: a) 2,0 m/s² · b) 8,0 N · c) nhỏ hơn (8 N &lt; 10 N) &nbsp;|&nbsp; D3·2: a) 4,0 m/s² · b) 12 N · c) 0,50 m`,
    `D4·1: a) 6,0 m/s² · b) 16 N · c) P<sub>2</sub> &lt; T &lt; P<sub>1</sub> (10 N &lt; 16 N &lt; 40 N) &nbsp;|&nbsp; D4·2: a) 2,5 m/s² · b) 18,75 N · c) 1,25 m &nbsp;|&nbsp; D5·1: a) 5,0 m/s² · b) 3,0 kg &nbsp;|&nbsp; D5·2: a) 2,5 m/s² · b) 1,33 kg · c) 8,0 N`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang: [...dang, ...dang2].map(bt), tach: [3, 2], kq: [[1, 2, 3], [4, 5]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo), dap: tuongTu.dap.map((d) => d.replace(/(\d) (N|kg|m\/s²|m)(?=[ )·&,]|$)/g, '$1&nbsp;$2')) },
  tra: 'trọng lực 1·4 · trọng tâm 2·1 · dây dọi 2·2 · trọng lượng 2·3 · lực kế 2·4 · lực căng 3·1 · hệ nối dây 3·2 · bẫy 3·4 · bài toán mẫu 4·3 · dạng 1–3 → 6·1 · dạng 4–5 → 7·1',
  out: process.argv[2],
});
