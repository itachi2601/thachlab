// Ruột tập VL10 – Bài 14 · Định luật 1 Newton (lesson id 59). Quyển Chương 3 lớp 10: bài 13 = tr. 1–12, bài 14 = tr. 13–24.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l10-bai14.mjs (SVG tự vẽ + 1 ảnh thật Wikimedia CC BY 3.0 ở book/assets/anh-that). Nội dung theo bài web
// (book/cache/59.json, tải từ DB 13/11/2026): mục tiêu, dự đoán bánh khúc côn cầu, hành trang, II.1 Galilei, II.2 định luật 1,
// II.3 quán tính + thí nghiệm đồng xu, ba bẫy, Trả bài 6 câu, bài toán mẫu xe tải + điền bước + biến thể, đời sống, thử thách, 3 dạng.
// Đáp số Bài tương tự (tuongTu.dap) tính bằng Python 13/11/2026.
// Chạy: node scripts/ruot-tap/l10-bai14.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl10-bai14.pdf
//       node scripts/ruot-tap/l10-bai14.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l10-bai14/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL10b14 as H } from './hinh-l10-bai14.mjs';

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
  const out = resolve(HERE, 'out/hinh-l10-bai14'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 14, lid: 59, ten: 'ĐỊNH LUẬT 1 NEWTON', lop: 10, baiDau: 13, sub: 'Vật lí 10 · Chương 3: Động lực học' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const g10 = nw(m('g=10\\ \\mathrm{m/s^2}'));
const Fhl = m('\\vec F_{\\mathrm{hl}}'), vv = m('\\vec v');
const Fk = m('F_k'), Fc = m('F_c'), Fms = m('F_{\\mathrm{ms}}');

const p1 = `<section class="page">
${head('BÀI 14 · ĐỊNH LUẬT 1 NEWTON', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Phát biểu được <b>định luật 1 Newton</b> và điều kiện áp dụng`)}
${dong(`${ck}Nêu đúng <b>vai trò của lực</b> đối với vận tốc của vật`)}
${dong(`${ck}Giải thích hiện tượng <b>quán tính</b>: phanh gấp, rẽ gấp, giũ áo`)}
${dong(`${ck}Tìm lực chưa biết khi vật <b>đứng yên</b> hoặc <b>chuyển động thẳng đều</b>`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Bánh khúc côn cầu rời gậy, trượt trên mặt băng <b>hoàn toàn không ma sát</b>, không có không khí. Sau khi rời gậy, bánh sẽ:</p>
<div class="fig-side" style="${fs(46)}"><div>
${opt('A', 'Dừng ngay, vì không còn lực đẩy của gậy')}
${opt('B', 'Chậm dần rồi dừng, vì “lực đẩy” của gậy hao dần')}
${opt('C', 'Chuyển động thẳng đều mãi mãi')}
${opt('D', 'Nhanh dần lên, vì không còn gì cản')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 2)}</div>
${H.banh()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(2)}</div>
${h3(4, 'Mở bài: cú đẩy trên sân băng', '1·4')}
<div class="card" style="padding:1.2mm 3mm">
<div>Trên sân băng, đẩy nhẹ vào thành sân là em lướt gần hết sân. Cùng cú đẩy ấy trên sàn xi măng với giày thường, em chỉ trượt nửa bước.</div>
${wl('Cái gì làm em dừng lại: “hết lực đẩy” hay một lực khác?', 3)}</div>
${h3(5, 'Kiểm tra hành trang', '1·5')}
${box(`<div>Gia tốc ${m('a=\\dfrac{\\Delta v}{\\Delta t}')} &nbsp;· Xe chạy thẳng đều ${nw(m('15\\ \\mathrm{m/s}'))} trong ${nw(m('10\\ \\mathrm s'))}: ${nw(`${m('a=')} ${f(16)}`)}</div>
<div style="margin-top:.6mm">Hai lực cân bằng: cùng đặt lên ${f(25)}, cùng ${f(25)}, cùng ${f(25)}, ${f(25)} chiều.</div>`)}
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('THÍ NGHIỆM GALILEI · ĐỊNH LUẬT 1 NEWTON')}
${h3(1, 'II.1 · Thí nghiệm của Galilei: bi trên hai máng nghiêng', '2·1')}
<div class="fig-side" style="${fs(50)}"><div>
<div><b>Làm:</b> thả bi từ độ cao ${nw(m('h_0=20\\ \\mathrm{cm}'))} trên máng (1) nghiêng ${m('30^\\circ')}; bi lăn lên máng (2). Hạ dần máng (2), đo quãng đường ${m('d')} và độ cao ${m('h')} bi lên được (thước chia ${nw('0,5 cm')}).</div>
<table class="tbl-ct" style="margin-top:.8mm"><tr><th>Góc máng (2)</th><th>${m('d\\ (\\mathrm{cm})')}</th><th>${m('h\\ (\\mathrm{cm})')}</th><th>${m('h_0-h\\ (\\mathrm{cm})')}</th></tr>
<tr><td>${m('30^\\circ')}</td><td>37,3</td><td>18,7</td><td></td></tr>
<tr><td>${m('15^\\circ')}</td><td>69,4</td><td>18,0</td><td></td></tr>
<tr><td>${m('5^\\circ')}</td><td>180,3</td><td>15,7</td><td></td></tr></table>
<div class="hint" style="margin-top:.3mm">Số liệu minh hoạ, không phải số đo gốc của Galilei.</div></div>
${H.haiMang()}</div>
<div class="card" style="margin-top:.6mm;padding:1mm 3mm">
<div>Máng (2) càng thoải: ${m('d')} ${f(25)}, ${m('h')} ${f(25)}. Bi lên thấp hơn ${m('h_0')} vì có ${f(25)}.</div>
<div><b>Rút ra:</b> không ma sát, máng (2) nằm ngang thì bi</div>${lines(2)}
${cau('Hai hàng đầu chỉ chênh 0,7 cm. Cột nào cho kết luận chắc hơn? Vì sao?', 2)}</div>
${h3(2, 'II.2 · Định luật 1 Newton', '2·2')}
<div class="card" style="padding:1.2mm 3mm">
<div>Nếu vật không chịu tác dụng của ${f(25)}, hoặc chịu các lực có hợp lực ${f(25)}, thì:</div>
<div>· vật đang đứng yên sẽ ${f(40)}</div>
<div>· vật đang chuyển động sẽ ${f(52)}</div>
<div style="margin:.6mm 0">${Fhl} ${m('=')} ${f(12)} &nbsp;${m('\\Rightarrow')}&nbsp; ${vv} ${m('=')} ${f(16)} &nbsp;(cả ${f(25)} lẫn ${f(25)})</div>
<div>Đứng yên hoặc thẳng đều gọi chung là trạng thái ${f(30)}.</div></div>
<div class="card fig-side" style="${fs(48)};padding:1.2mm 3mm"><div>
<div><b>Lực</b> là nguyên nhân làm ${f(40)}</div>
<div>(đổi độ lớn, đổi hướng, hoặc cả hai), không phải để ${f(40)}.</div>
<div style="margin-top:.8mm">Xe chạy thẳng đều trên đường ngang (điền =, &gt; hoặc &lt;):</div>
<div>${nw(`${Fk} ${f(12)} ${Fc}`)} &nbsp;·&nbsp; ${nw(`${m('N')} ${f(12)} ${m('P')}`)} &nbsp;·&nbsp; hợp lực ${nw(`${m('=')} ${f(16)}`)}</div>
${cau('Xe chạy tới mà hợp lực như vậy. Có mâu thuẫn không? (Voyager 1 tắt máy vẫn bay ≈ 17 km/s.)', 2)}</div>
${H.oTo()}</div>
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('QUÁN TÍNH · BA CÁI BẪY · TỰ KIỂM TRA')}
${h3(1, 'II.3 · Quán tính', '3·1')}
<div class="card" style="padding:1.2mm 3mm">
<div><b>Quán tính:</b> tính chất của mọi vật có xu hướng bảo toàn ${f(25)}, cả về ${f(25)} lẫn ${f(25)}.</div>
<div>Vì có quán tính, vận tốc không thể thay đổi ${f(25)}; lực phải tác dụng trong một khoảng thời gian.</div>
<div>Định luật 1 còn gọi là định luật ${f(25)}. Khối lượng càng lớn, quán tính càng ${f(16)}.</div></div>
<table class="tbl-ct"><tr><th style="width:62mm">Tình huống</th><th>Người (hoặc vật) bị làm sao, vì sao</th></tr>
<tr><td>Xe đang chạy, phanh gấp</td><td></td></tr>
<tr><td>Xe đứng yên, tăng tốc đột ngột</td><td></td></tr>
<tr><td>Xe rẽ gấp sang trái</td><td></td></tr>
<tr><td>Giũ mạnh chiếc áo bám bụi</td><td></td></tr>
<tr><td>Gõ đuôi cán búa xuống nền</td><td></td></tr></table>
${h3(2, 'Thí nghiệm: đồng xu, tấm bìa và chiếc cốc', '3·2')}
<div class="card fig-side" style="${fs(42)};padding:1.2mm 3mm"><div>
<div><b>Làm:</b> đặt bìa cứng lên miệng cốc, đồng xu giữa bìa. Búng thật nhanh vào mép bìa theo phương ngang. Lặp lại nhưng kéo bìa thật chậm.</div>
<div style="margin-top:.6mm"><b>Thấy:</b> búng nhanh: xu ${f(36)}</div>
<div>kéo chậm: xu ${f(36)}</div>
${cau('<b>Rút ra:</b> vì sao búng nhanh thì xu không đi theo bìa?', 1)}</div>
${H.dongXu()}</div>
${h3(3, 'III · Ba cái bẫy hay sập', '3·3')}
<div class="card fig-side" style="${fs(40)};padding:1mm 3mm"><div>
<div class="trap">${ck}<span><b>“Đang chạy thì phải có lực đẩy theo chiều chạy.”</b> Không lực, vật vẫn thẳng đều; hết lực đẩy, vật dừng vì có lực cản.</span></div>
<div class="trap">${ck}<span><b>“Đứng yên nghĩa là không có lực nào.”</b> Sách trên bàn chịu ${m('P')} và ${m('N')}: có lực, nhưng hợp lực bằng ${m('\\vec 0')}.</span></div>
<div class="trap">${ck}<span><b>“Quán tính là lực đẩy em về phía trước.”</b> Quán tính là tính chất, không phải lực: không có vật nào đẩy em.</span></div></div>
${H.phanhGap()}</div>
${h3(4, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '3·4')}
${rkHai([1, 2, 3], [4, 5, 6])}
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('TRẢ BÀI · BÀI TOÁN MẪU')}
${h3(1, 'IV · Trả bài 6 câu', '4·1')}
${box(`${tb('1. Phát biểu định luật 1 Newton.')}${lines(2)}
${tb('2. Trạng thái cân bằng gồm những trạng thái nào? Điều kiện?')}${lines(1)}
${tb('3. Thí nghiệm Galilei: làm gì, thấy gì, suy ra gì?')}${lines(2)}
${tb('4. Lực là nguyên nhân của cái gì?')}${lines(1)}
${tb('5. Quán tính là gì? Nêu hai ví dụ.')}${lines(2)}
${tb('6. “Không chịu lực” khác “chịu các lực cân bằng” thế nào?')}${lines(1)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/6 câu · chưa thuộc: ${f(25)} ${nw(`→ đọc lại ô ${f(12)} Tập`)}</div>
${h3(2, 'V · Bài toán mẫu: xe tải chạy thẳng đều', '4·2')}
<div class="card soft" style="padding:1.2mm 3mm">Xe tải khối lượng ${nw('5 tấn')} chạy thẳng đều trên đường nằm ngang với tốc độ ${nw(m('54\\ \\mathrm{km/h}'))}. Lực cản tác dụng lên xe bằng ${nw('0,04')} trọng lượng xe. Lấy ${g10}. Tính lực kéo của động cơ và lực đỡ của mặt đường lên xe.</div>
<table><tr><th style="width:52mm">Câu trong đề</th><th>Dữ liệu → kiến thức</th></tr>
<tr><td>“khối lượng 5 tấn”</td><td>${m('m=5000\\ \\mathrm{kg}')}, ${m('P=mg')}</td></tr>
<tr><td style="height:6.5mm">“chạy thẳng đều”</td><td></td></tr>
<tr><td style="height:6.5mm">“đường nằm ngang”</td><td></td></tr>
<tr><td style="height:6.5mm">“tốc độ 54 km/h”</td><td></td></tr>
<tr><td style="height:6.5mm">“bằng 0,04 trọng lượng”</td><td></td></tr></table>
<div class="fig-side" style="${fs(50)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl(`Trọng lượng ${m('P')}:`, 1)}${wl(`Lực cản ${Fc}:`, 1)}${wl(`Phương ngang → ${Fk}:`, 2)}${wl(`Phương đứng → ${m('N')}:`, 2)}</div>${H.xeTai()}</div>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('ĐIỀN BƯỚC · BIẾN THỂ · BÀI TẬP VỀ NHÀ · THỬ THÁCH')}
${h3(1, 'Điền bước và biến thể của bài toán mẫu', '5·1')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:.4mm 3mm 0">
<div>Cùng đề, xe chở thêm hàng thành ${nw('8 tấn')}, lực cản bằng <b>${nw('0,05')}</b> trọng lượng.</div>
<div class="ln"><b>Bước 1 (cho sẵn):</b> ${m('P=8000\\cdot 10=80\\,000\\ \\mathrm N')}</div>
${wl(`Bước 2: ${Fc}=`, 1)}${wl(`Bước 3: ${Fk}= &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; vì`, 1)}
${cau(`<b>Đổi vai.</b> Lực kéo ${nw('3000 N')}, xe chạy thẳng đều, lực cản bằng ${nw('0,05')} trọng lượng, ${g10}. Khối lượng xe?`, 1)}
${cau(`<b>Tắt máy.</b> Xe ${nw('5 tấn')} của đề tắt máy (${nw(`${Fk}=0`)}). Hợp lực lúc đó bằng bao nhiêu, hướng nào? Xe dừng ngay hay lăn thêm?`, 1)}</div>
${K.btvn().replace('<i>1</i>', '<i>2</i>')}
${h3(3, 'Thử thách phân tầng', '5·3')}
${box(cau(`${m('\\bigstar')} Vật đang chạy ${nw('3 m/s')} thì chịu hai lực cùng ${nw('10 N')}, cùng phương, ngược chiều. Vận tốc của vật sau ${nw('5 s')}?`, 1)
 + cau(`${m('\\bigstar\\bigstar')} Người ${nw('60 kg')} đứng trên cân trong thang máy đang đi lên đều, ${g10}. Lực đỡ của sàn lên người?`, 1)
 + cau(`${m('\\bigstar\\bigstar\\bigstar')} Quả cầu treo bằng dây trên trần toa tàu. <b>a)</b> Tàu chạy thẳng đều: dây thẳng đứng hay lệch?`, 1)
 + wl('<b>b)</b> Tàu phanh: dây lệch về phía đầu tàu hay đuôi tàu? Vì sao?', 1))}
${h3(4, 'VI · Đời sống và mang về', '5·4')}
<div class="fig-side" style="${fs(34)}">${box(wl('Vì sao ô tô phải có dây an toàn và tựa đầu ghế?', 2) + wl('Mang về: điều em dễ quên nhất', 2))}${H.anhVaCham()}</div>
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Vật trượt đều trên sàn ngang: ma sát và phản lực',
    de: `Chiếc tủ ${m('60\\ \\mathrm{kg}')} được đẩy trượt <b>thẳng đều</b> trên sàn nằm ngang bằng lực nằm ngang ${m('150\\ \\mathrm N')}; ${g10}.<br><b>a)</b> độ lớn lực ma sát<br><b>b)</b> độ lớn phản lực của sàn lên tủ`,
    nd: `Thẳng đều ⇒ hợp lực ${f(12)}; phương ngang ${nw(`${m('F')} ${f(12)} ${Fms}`)}; phương đứng ${nw(`${m('N')} ${f(12)} ${m('P')}`)}`, a: ['a', 'b'], gi: 9, fig: H.tuTruot() },
  { t: 'Dạng 2 · Trung bình · Nâng đều: lực căng của cáp',
    de: `Cần cẩu nâng kiện hàng ${m('450\\ \\mathrm{kg}')} bằng cáp thẳng đứng; kiện hàng đi lên với tốc độ <b>không đổi</b> ${m('0{,}5\\ \\mathrm{m/s}')}. Bỏ qua khối lượng cáp; ${g10}.<br><b>a)</b> lực căng của cáp<br><b>b)</b> lực căng lớn hơn, nhỏ hơn hay bằng trọng lực kiện hàng`,
    nd: `Vận tốc không đổi ⇒ ${nw(`${m('T')} ${f(12)} ${m('P')}`)}; dữ kiện thừa là ${f(28)}`, a: ['a', 'b'], gi: 9, fig: H.canCau(), cot: 2 },
  { t: 'Dạng 3 · Khá · Dây kéo chếch lên: ma sát và phản lực',
    de: `Kéo thùng ${m('20\\ \\mathrm{kg}')} trượt thẳng đều trên sàn ngang bằng dây chếch lên, hợp với phương ngang góc ${m('\\alpha')} có ${nw(m('\\cos\\alpha=0{,}8'))}, ${nw(m('\\sin\\alpha=0{,}6'))}. Lực căng dây ${m('50\\ \\mathrm N')}; ${g10}.<br><b>a)</b> hai thành phần ${m('T_x')} (ngang) và ${m('T_y')} (đứng) của lực căng<br><b>b)</b> độ lớn lực ma sát<br><b>c)</b> độ lớn phản lực của sàn`,
    nd: `${nw(`${m('T_x=T\\cdot')} ${f(16)}`)}, ${nw(`${m('T_y=T\\cdot')} ${f(16)}`)}; phương đứng: ${nw(`${m('N=P')} ${f(12)} ${m('T_y')}`)} (dây kéo lên hay đè xuống?)`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'], gi: 15, fig: H.thungD3(), cot: 2,
    bang: `<table style="margin:.6mm 0"><tr><th style="width:60mm">Câu trong đề</th><th>Dữ liệu → kiến thức</th></tr><tr><td>“trượt thẳng đều”</td><td></td></tr><tr><td>“dây chếch lên … cos, sin”</td><td></td></tr><tr><td>“lực căng dây 50 N”</td><td></td></tr></table>` },
];

// Bài tương tự giải vào vở (thầy chốt 10/11): 1 cột; ô đáp số đặt cuối đúng dòng của ý, nhãn khớp a) b) c)… (a<sub>1</sub>, a<sub>2</sub> khi ý có 2 kết quả).
const ttHaiCot = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm}.yo .oo{flex:none;display:flex;gap:3mm}.yo{line-height:1.35}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';
const oY = (s, o, w = 25) => s.split('<br>').map((p) => {
  const y = p.match(/^<b>([a-d])\)<\/b>/);
  if (!y) return `<div>${p}</div>`;
  const ls = o.filter((l) => l[0] === y[1]);
  return `<div class="yo"><span>${p}</span><span class="oo">${ls.map((l) => `<span class="nw"><b>${l})</b>${f(w)}</span>`).join('')}</span></div>`;
}).join('');
const ttDe = (b) => b.fig ? `<div class="fig-side" style="grid-template-columns:1fr ${b.fw}mm">${`<div>${oY(b.de, b.o, b.ow)}</div>`}${b.fig}</div>` : oY(b.de, b.o, b.ow);
const vaoVo = (ds) => ds.map((b) => (b.o ? { t: b.t, de: ttDe(b), k: 0 } : b));
const nhap = (n) => ({ t: '<span class="nhap-t">Nháp / chỗ em còn vướng</span>', de: lines(n), k: 0 });
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–2', 'DẠNG 3'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Thùng hàng ${m('40\\ \\mathrm{kg}')} được đẩy trượt thẳng đều trên sàn ngang bằng lực nằm ngang ${nw(`${m('120\\ \\mathrm N')};`)} ${nw(`${g10}.`)}<br><b>a)</b> độ lớn lực ma sát<br><b>b)</b> độ lớn phản lực của sàn`, o: ['a', 'b'] },
    { t: 'Dạng 1 · Bài 2', de: `Xe đạp và người, tổng khối lượng ${m('70\\ \\mathrm{kg}')}, chạy thẳng đều trên đường ngang; lực cản tổng cộng bằng ${nw('0,03')} trọng lượng; ${nw(`${g10}.`)}<br><b>a)</b> độ lớn lực cản<br><b>b)</b> lực phát động (theo phương ngang) mà mặt đường tác dụng lên xe<br><b>c)</b> phản lực của mặt đường`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 2 · Bài 1', de: `Buồng thang máy ${m('600\\ \\mathrm{kg}')} đi <b>xuống</b> với tốc độ không đổi ${nw(`${m('2\\ \\mathrm{m/s}')};`)} ${nw(`${g10}.`)}<br><b>a)</b> lực căng của cáp<br><b>b)</b> lực căng lớn hơn, nhỏ hơn hay bằng trọng lực buồng thang`, o: ['a', 'b'], ow: 30 },
    { t: 'Dạng 2 · Bài 2', de: `Người nhảy dù cùng dù, tổng khối lượng ${m('80\\ \\mathrm{kg}')}, đang rơi thẳng đứng với tốc độ không đổi; ${nw(`${g10}.`)}<br><b>a)</b> hợp lực tác dụng lên người và dù<br><b>b)</b> độ lớn lực cản của không khí<br><b>c)</b> lực cản bỗng giảm còn ${m('600\\ \\mathrm N')}: tốc độ rơi tăng, giảm hay không đổi`, o: ['a', 'b', 'c'], ow: 30 },
    nhap(13),
  ], [
    { t: 'Dạng 3 · Bài 1', de: `Kéo thùng ${m('30\\ \\mathrm{kg}')} trượt thẳng đều trên sàn ngang bằng dây chếch lên góc ${m('\\alpha')}, ${nw(m('\\cos\\alpha=0{,}8'))}, ${nw(`${m('\\sin\\alpha=0{,}6')};`)} lực căng dây ${nw(`${m('100\\ \\mathrm N')};`)} ${nw(`${g10}.`)}<br><b>a)</b> ${m('T_x')} và ${m('T_y')}<br><b>b)</b> độ lớn lực ma sát<br><b>c)</b> độ lớn phản lực của sàn`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'] },
    { t: 'Dạng 3 · Bài 2', de: `Đẩy xe ${m('25\\ \\mathrm{kg}')} trượt thẳng đều trên sàn ngang từ phía sau, lực đẩy ${m('50\\ \\mathrm N')} chếch <b>xuống</b> góc ${m('\\alpha')} so với phương ngang, ${nw(m('\\cos\\alpha=0{,}8'))}, ${nw(`${m('\\sin\\alpha=0{,}6')};`)} ${nw(`${g10}.`)}<br><b>a)</b> ${m('F_x')} và ${m('F_y')}<br><b>b)</b> độ lớn lực ma sát<br><b>c)</b> độ lớn phản lực của sàn`, fig: H.thungTT(), fw: 46, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'] },
    nhap(20),
  ]],
};
tuongTu.dap = [
  `D1·1: a) F<sub>ms</sub> = 120 N · b) N = 400 N &nbsp;|&nbsp; D1·2: a) F<sub>c</sub> = 21 N · b) 21 N · c) N = 700 N &nbsp;|&nbsp; D2·1: a) T = 6000 N · b) bằng &nbsp;|&nbsp; D2·2: a) ${m('\\vec 0')} · b) 800 N · c) tăng (hợp lực hướng xuống)`,
  `D3·1: a<sub>1</sub>) T<sub>x</sub> = 80 N · a<sub>2</sub>) T<sub>y</sub> = 60 N · b) F<sub>ms</sub> = 80 N · c) N = 240 N &nbsp;|&nbsp; D3·2: a<sub>1</sub>) F<sub>x</sub> = 40 N · a<sub>2</sub>) F<sub>y</sub> = 30 N · b) F<sub>ms</sub> = 40 N · c) N = 280 N`,
];

await K.dung({
  trang1to5: ttHaiCot + [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [2, 1], kq: [[1, 2], [3]], khoNhat: true },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'dự đoán 1·2 · Galilei 2·1 · định luật 1 2·2 · quán tính 3·1 · đồng xu 3·2 · bẫy 3·3 · bài toán mẫu 4·2 · điền bước, biến thể 5·1 · dạng 1–2 → 6·1 · dạng 3 → 7·1',
  out: process.argv[2],
});
