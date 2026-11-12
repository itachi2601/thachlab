// Ruột tập VL11 – Bài 23 · Điện trở. Định luật Ohm (lesson id 42). Quyển Chương 4 lớp 11: bài 22 = tr. 1–12, bài 23 = tr. 13–24.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l11-bai23.mjs (toàn bộ SVG tự vẽ). Nội dung theo bài web (book/cache/42.json, tải từ DB 12/11/2026): mục tiêu, dự đoán
// bóng đèn "chết" lúc bật, II.1–II.6, thí nghiệm R 10 Ω / đèn 6 V – 3 W / NTC trong nước, sai số, ba bẫy, Trả bài 6 câu, bài toán mẫu
// dây tóc vonfram, thử thách ⭐–⭐⭐⭐, 5 dạng bài tập mẫu. Đáp số Bài tương tự (tuongTu.dap) tính bằng Python 12/11/2026.
// Tránh sẵn 4 lỗi lặp HS ảo L11 Ch.3: hằng số α in sẵn trước khi hỏi · Mục tiêu/chú thích hình cạnh Dự đoán không lộ đáp án (đồ thị đèn
// để trống cho HS chấm) · ô rộng cho phân số/đáp án dài · số dòng kẻ ≥ số ý ở Dạng 1–3.
// Chạy: node scripts/ruot-tap/l11-bai23.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl11-bai23.pdf
//       node scripts/ruot-tap/l11-bai23.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l11-bai23/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL11b23 as H } from './hinh-l11-bai23.mjs';

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
  const out = resolve(HERE, 'out/hinh-l11-bai23'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 23, lid: 42, ten: 'ĐIỆN TRỞ · ĐỊNH LUẬT OHM', lop: 11, baiDau: 22, sub: 'Vật lí 11 · Chương 4: Dòng điện. Mạch điện' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const Om = (s) => nw(m(`${s}\\ \\Omega`)), kOm = (s) => nw(m(`${s}\\ \\mathrm{k}\\Omega`));
const V = (s) => nw(m(`${s}\\ \\mathrm V`)), A = (s) => nw(m(`${s}\\ \\mathrm A`)), mA = (s) => nw(m(`${s}\\ \\mathrm{mA}`));
const oC = (s) => nw(m(`${s}\\ ^\\circ\\mathrm C`));
const R0 = m('R_0'), t0 = m('t_0'), al = m('\\alpha'), rho = m('\\rho');
const aW = nw(m('\\alpha_{\\mathrm W}=4{,}5\\cdot10^{-3}\\ \\mathrm{K^{-1}}'));
const aCu = nw(m('\\alpha_{\\mathrm{Cu}}=3{,}9\\cdot10^{-3}\\ \\mathrm{K^{-1}}'));
const o = (w = 12, h = 0) => `<span class="fill" style="min-width:${w}mm${h ? `;height:${h}mm` : ''}"></span>`;

// Bài tương tự 1 cột, ô đáp số cuối dòng của ý (cùng cách l11-bai16).
const ttCss = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}.bng td,.bng th{padding:.2mm 1.5mm;text-align:center}.bt .ans .fill{height:6.5mm}</style>';

const p1 = `${ttCss}<section class="page">
${head('BÀI 23 · ĐIỆN TRỞ. ĐỊNH LUẬT OHM', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Định nghĩa <b>điện trở</b> ${m('R=U/I')}, đơn vị ôm; đổi đúng kΩ, mA`)}
${dong(`${ck}Phát biểu <b>định luật Ohm</b>; đọc <b>đường đặc trưng vôn – ampe</b>`)}
${dong(`${ck}Giải thích vì sao kim loại có điện trở; ${m('R')} của kim loại, NTC, PTC phụ thuộc <b>nhiệt độ</b> ra sao`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Bóng đèn sợi đốt hay đứt đúng lúc bật công tắc, hiếm khi đứt lúc đang sáng. Cùng ổ 220 V: dòng qua dây tóc lớn nhất vào lúc nào?</p>
<div class="fig-side" style="${fs(42)}"><div>
${opt('A', 'Lúc vừa bật, dây tóc còn nguội')}
${opt('B', 'Lúc đã sáng ổn định, dây tóc nóng nhất')}
${opt('C', 'Như nhau, vì hiệu điện thế không đổi')}
${opt('D', 'Lúc vừa tắt, dây tóc còn nóng')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 1)}</div>
${H.denBat()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Điện trở là gì', '1·4')}
<div class="card fig-side" style="${fs(40)};padding:1.2mm 3mm"><div>
<div>Cùng ${V('12')}: dây A cho ${A('2')}, dây B chỉ ${A('0{,}5')}. Dây ${f(8)} cản dòng mạnh hơn.</div>
<div>Điện trở đo mức ${f(30)} của vật dẫn.</div>
<div style="margin:1mm 0;min-height:11mm;display:flex;align-items:flex-end;gap:2mm">${m('R=')} <span class="fill" style="min-width:16mm;height:10mm"></span> <span>đơn vị: ${f(14)} (kí hiệu ${f(8)})</span></div>
<div>${m('1\\ \\Omega=1')} ${f(12)} · dây A: ${m('R=')} ${f(12)} · dây B: ${m('R=')} ${f(12)}</div>
<div>${m('1\\ \\mathrm{k}\\Omega=')} ${f(14)} ${m('\\Omega')} · ${m('1\\ \\mathrm{M}\\Omega=')} ${f(14)} ${m('\\Omega')} · ${m('1\\ \\mathrm{mA}=')} ${f(14)} ${m('\\mathrm A')}</div></div>
${H.dayAB()}</div>
${h3(5, 'Làm nhanh', '1·5')}
${box(cau(`Điện trở ${kOm('2{,}2')} mắc vào ${V('11')}. Dòng điện qua nó bằng bao nhiêu mA? &nbsp;${m('I=')} ${o(16)} mA`, 1))}
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('ĐƯỜNG ĐẶC TRƯNG VÔN – AMPE · ĐỊNH LUẬT OHM')}
${h3(1, 'II.2 · Thí nghiệm đo: U và I của điện trở 10 Ω', '2·1')}
<div class="card fig-side" style="${fs(40)};padding:1.2mm 3mm"><div>
<div><b>Làm:</b> mắc điện trở ${Om('10')} (loại ít nóng) vào nguồn điều chỉnh được; ampe kế (sai số ${A('\\pm0{,}01')}) mắc ${f(16)}, vôn kế (${V('\\pm0{,}1')}) mắc ${f(16)} với R. Tăng ${m('U')} từ 1,0 V tới 5,0 V, ghi ${m('I')}.</div>
<table class="tbl-ct bng" style="margin-top:.8mm"><tr><th>${m('U')} (V)</th><th>1,0</th><th>2,0</th><th>3,0</th><th>4,0</th><th>5,0</th></tr>
<tr><td>${m('I')} (A)</td><td>0,10</td><td>0,20</td><td>0,30</td><td>0,40</td><td>0,50</td></tr>
<tr><td>${m('U/I')} (Ω)</td><td></td><td></td><td></td><td></td><td></td></tr></table>
<div style="margin-top:.6mm"><b>Rút ra:</b> ${m('U')} gấp đôi thì ${m('I')} ${f(16)}; ${m('I')} ${f(25)} với ${m('U')}.</div></div>
${H.machDo()}</div>
<div class="fig-side" style="${fs(46)}"><div>
<div><b>Đường đặc trưng vôn – ampe:</b> đồ thị ${f(10)} theo ${f(10)} của một linh kiện.</div>
<div>Điện trở (nhiệt độ ổn định): đường ${f(30)}.</div>
<div>Độ dốc ${m('\\dfrac{I}{U}=')} <span class="fill" style="min-width:12mm;height:9mm"></span> &nbsp;⇒ đường dốc hơn thì ${m('R')} ${f(14)}.</div>
<div style="margin-top:.3mm"><b>Sai số:</b> sai số tương đối của ${m('R')} ≈ ${m('\\dfrac{\\Delta U}{U}+\\dfrac{\\Delta I}{I}')}</div>
<div>Hàng 1,0 V: ${o(14)} % &nbsp;· hàng 5,0 V: ${o(14)} %</div>
<div>Tính ${m('R')} từ một hàng thì chọn hàng ${f(12)} V, vì ${f(30)}</div>
<div>Tốt nhất: chấm cả 5 điểm rồi lấy ${f(30)}</div></div>
${H.luoiR()}</div>
${h3(2, 'II.3 · Định luật Ohm', '2·2')}
<div class="card" style="padding:1.2mm 3mm">
<div>Cường độ dòng điện qua vật dẫn tỉ lệ ${f(16)} với ${f(30)}, tỉ lệ ${f(16)} với ${f(25)}.</div>
<div style="margin:.4mm 0;min-height:11mm;display:flex;align-items:flex-end;gap:2mm">${m('I=')} <span class="fill" style="min-width:16mm;height:10mm"></span> <span>&nbsp;“${m('I')} tỉ lệ thuận ${m('U')}” chỉ đúng khi ${m('R')} ${f(22)}</span></div>
<div><b>Ví dụ:</b> LED cần ${mA('20')}; hai đầu điện trở nối tiếp với LED là ${V('3')}. ${m('R=')} ${o(26)}</div>
</div>
${h3(3, 'Nhắc lại từ lớp 9', '2·3')}
<table class="bng"><tr><th style="width:24mm"></th><th>Điện trở tương đương</th><th style="width:28mm">${m('I')}</th><th style="width:28mm">${m('U')}</th></tr>
<tr><td style="height:10mm">Nối tiếp</td><td></td><td></td><td></td></tr><tr><td style="height:10mm">Song song</td><td></td><td></td><td></td></tr></table>
<div style="margin-top:1mm">Dây đồng chất, tiết diện đều: ${m('R=')} <span class="fill" style="min-width:16mm;height:9mm"></span> ; ${rho} là ${f(25)} (đơn vị ${f(14)})</div>
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('VÌ SAO CÓ ĐIỆN TRỞ · ĐIỆN TRỞ THEO NHIỆT ĐỘ')}
${h3(1, 'II.4 · Vì sao kim loại có điện trở', '3·1')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div>Ion ${f(14)} xếp đều ở ${f(25)} tinh thể; electron ${f(14)} trôi giữa chúng khi có điện trường.</div>
<div>Ion dao động ${f(14)}; electron trôi qua ${f(20)} vào ion, bị cản: đó là điện trở.</div>
<div style="margin-top:.6mm">Nóng hơn → ion rung ${f(14)} → va chạm ${f(14)} → electron trôi ${f(14)} → cùng ${m('U')} thì ${m('I')} ${f(12)} → ${m('R')} ${f(12)}.</div></div>
${H.mangIon()}</div>
${h3(2, 'II.5 · Thí nghiệm đo: bóng đèn 6 V – 3 W', '3·2')}
<div class="fig-side" style="${fs(46)}"><div>
<div><b>Làm:</b> thay điện trở 10 Ω bằng đèn 6 V – 3 W; tăng ${m('U')} từ 1,0 V tới 6,0 V, chờ ổn định rồi ghi ${m('I')}. Chấm 6 điểm lên hình bên.</div>
<table class="tbl-ct bng" style="margin-top:.8mm"><tr><th>${m('U')} (V)</th><th>1,0</th><th>2,0</th><th>3,0</th><th>4,0</th><th>5,0</th><th>6,0</th></tr>
<tr><td>${m('I')} (A)</td><td>0,17</td><td>0,26</td><td>0,33</td><td>0,39</td><td>0,45</td><td>0,50</td></tr>
<tr><td>${m('U/I')} (Ω)</td><td>5,9</td><td></td><td>9,1</td><td></td><td>11,1</td><td></td></tr></table>
<div style="margin-top:.6mm"><b>Quan sát:</b> ${m('U')} tăng 6 lần, ${m('I')} tăng ${f(25)}; ${m('U/I')} ${f(20)}.</div>
<div><b>Rút ra:</b> ${m('R')} dây tóc ${f(16)} khi nóng lên; đường đặc trưng của đèn ${f(25)}.</div>
<div>Điốt: chỉ dẫn điện theo ${f(16)} (chiều thuận); đường đặc trưng ${f(16)}.</div></div>
${H.luoiDen()}</div>
${h3(3, 'Công thức điện trở kim loại theo nhiệt độ', '3·3')}
<div class="card" style="padding:1.2mm 3mm">
<div style="margin:.4mm 0 1mm;min-height:10mm;display:flex;align-items:flex-end;gap:2mm">${m('R=')} <span class="fill" style="min-width:42mm;height:9mm"></span> <span>${R0}: điện trở ở ${t0} (thường 20 °C)</span></div>
<div>${al}: hệ số ${f(30)} (đơn vị ${f(10)}); kim loại có ${nw(`${al} ${f(8)} 0`)}</div>
<div>Tra cứu (gần đúng, cho sẵn): đồng ${aCu} · vonfram ${aW}</div>
<div>${m('t-t_0')} tính bằng °C hay K đều ra ${f(20)}. Điện trở suất cũng vậy: ${m('\\rho=')} ${f(34)}</div>
</div>
${h3(4, 'Điền bước còn thiếu', '3·4')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div style="padding:.6mm 0;line-height:1.35;border-bottom:.2mm dotted var(--hint)"><b>Đề:</b> dây tóc vonfram ${nw(`${m('R_0=4{,}0\\ \\Omega')} ở ${oC('20')}`)}; khi sáng dây tóc ${oC('1\\,020')}, dòng ${A('0{,}20')}.</div>
<div class="ln"><b>Bước 1 (cho sẵn):</b> ${m('t-t_0=1020-20=1000')} °C</div>
${wl(`Bước 2: ${m('R=4{,}0\\,[1+4{,}5\\cdot10^{-3}\\cdot1000]=')}`, 1)}${wl(`Bước 3: ${m('U=IR=')}`, 1)}</div>
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('ĐIỆN TRỞ NHIỆT · BA CÁI BẪY · TRẢ BÀI')}
${h3(1, 'II.6 · Điện trở nhiệt NTC và PTC', '4·1')}
<div class="card fig-side" style="${fs(34)};padding:1.2mm 3mm"><div>
<div>Điện trở nhiệt: ${m('R')} đổi rất mạnh theo nhiệt độ, dùng làm ${f(22)}. <b>Đo:</b> NTC ${kOm('10')} trong nước ấm.</div>
<table class="tbl-ct bng" style="margin-top:.6mm"><tr><th>${m('t')} (°C)</th><th>25</th><th>35</th><th>45</th><th>55</th></tr>
<tr><td>${m('R')} (kΩ)</td><td>10,0</td><td>6,5</td><td>4,3</td><td>3,0</td></tr></table>
<div style="margin-top:.6mm">NTC (hệ số ${f(10)}): nóng thì ${m('R')} ${f(22)}.</div><div>PTC (hệ số ${f(10)}): nóng thì ${m('R')} ${f(22)}, làm cầu chì tự phục hồi.</div></div>
${H.ntcCoc()}</div>
${h3(2, 'III · Ba cái bẫy hay sập', '4·2')}
<div class="card fig-side" style="${fs(38)};padding:1mm 3mm"><div>
<div class="trap">${ck}<span><b>“${m('U')} tăng thì ${m('R')} tăng, vì ${m('R=U/I')}.”</b> Điện trở 10 Ω (nhiệt độ ổn định) từ ${V('2{,}0')} lên ${V('4{,}0')}: ${m('R')} = ${o(10)} Ω, ${m('I')} từ ${o(12)} A lên ${o(12)} A.</span></div>
<div class="trap">${ck}<span><b>“Cái gì nóng lên cũng tăng điện trở.”</b> Sai với ${f(12)}: pin sạc nóng từ 25 °C lên 45 °C thì NTC ${kOm('10')} còn khoảng ${o(10)} kΩ.</span></div>
<div class="trap">${ck}<span><b>“Đường dốc hơn là điện trở lớn hơn.”</b> Đồ thị ${m('I')} theo ${m('U')}: độ dốc ${o(8)}; đồ thị ${m('U')} theo ${m('I')}: độ dốc ${o(8)}. Hình bên: ${m('R_1=')} ${o(10)} Ω, ${m('R_2=')} ${o(10)} Ω.</span></div></div>
${H.haiDuong()}</div>
${h3(3, 'IV · Trả bài 6 câu', '4·3')}
${box(`${tb('1. Điện trở là gì? Công thức, đơn vị, bội số?')}${lines(1)}
${tb('2. Phát biểu định luật Ohm. Khi nào I tỉ lệ thuận U?')}${lines(1)}
${tb('3. Đường đặc trưng V–A của điện trở, của đèn khác nhau thế nào?')}${lines(1)}
${tb('4. Vì sao kim loại có điện trở?')}${lines(1)}
${tb('5. Công thức R theo nhiệt độ; ý nghĩa từng kí hiệu?')}${lines(1)}
${tb('6. NTC, PTC khác kim loại ở chỗ nào?')}${lines(1)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/6 câu · chưa thuộc: ${f(25)} ${nw(`→ đọc lại ô ${f(12)} Tập`)}</div>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('TỰ KIỂM TRA · BÀI TOÁN MẪU · THỬ THÁCH')}
${h3(1, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '5·1')}
${rkHai([1, 2, 3], [4, 5, 6])}
${h3(2, 'V · Bài toán mẫu: dây tóc lúc nguội và lúc sáng', '5·2')}
<div class="card soft" style="padding:1.2mm 3mm">Dây tóc vonfram ${m('R_0=4{,}0\\ \\Omega')} ở ${oC('20')}, ${aW}; sáng bình thường: ${V('12')}, ${A('0{,}25')}.<br><b>a)</b> ${m('R')} khi sáng bình thường<br><b>b)</b> nhiệt độ dây tóc lúc đó<br><b>c)</b> lúc vừa bật (dây tóc ${oC('20')}): dòng điện; gấp mấy lần lúc sáng</div>
<table><tr><th style="width:50mm">Câu trong đề</th><th>Dữ liệu → kiến thức</th></tr>
<tr><td>“${m('R_0=4{,}0\\ \\Omega')} ở 20 °C”</td><td>${R0}, ${m('t_0=20')} °C → mốc của ${m('R(t)')}</td></tr>
<tr><td style="height:6.5mm">“12 V, dòng 0,25 A”</td><td></td></tr>
</table>
<div class="fig-side" style="${fs(36)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl(`a) ${m('R=')}`, 1)}${wl(`b) ${m('R/R_0=1+\\alpha(t-t_0)')} ⇒`, 2)}${wl(`c) ${m('I_0=')}`, 2)}</div>${H.dayToc('')}</div>
${K.btvn().replace('<i>1</i>', '<i>3</i>')}
${h3(4, 'Thử thách phân tầng', '5·4')}
${box(cau(`${m('\\bigstar')} Điện trở ${Om('470')} mắc vào ${V('9{,}4')}. Tính ${m('I')} ra mA.`, 1)
 + cau(`${m('\\bigstar\\bigstar')} Ở hình mục II.5, điểm đo 2,0 V của đèn nằm trên hay dưới đường đứt 12 Ω? Vì sao?`, 1)
 + cau(`${m('\\bigstar\\bigstar\\bigstar')} Cuộn dây đồng động cơ: ${Om('1{,}50')} ở ${oC('20')}; chạy một giờ, tắt máy đo ngay: ${Om('1{,}80')} (${aCu}). Nhiệt độ cuộn dây? Vì sao phải đo “ngay”?`, 2))}
${foot(5)}</section>`;

const bangD2 = `<table class="bng" style="font-size:var(--fs-sm);margin:.4mm 0 .8mm;line-height:1.15"><tr><th style="font-weight:400">đo khi ổn định</th><th colspan="3">X</th><th colspan="3">Y</th></tr>
<tr><td>(${m('U')} V; ${m('I')} mA)</td><td>(2,0; 2,0)</td><td>(4,0; 4,0)</td><td>(6,0; 6,0)</td><td>(1,0; 0,50)</td><td>(3,0; 2,0)</td><td>(6,0; 6,6)</td></tr>
<tr><td>${m('U/I')} (kΩ)</td><td></td><td></td><td></td><td></td><td></td><td></td></tr></table>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Tính R và I, đổi mA sang A',
    de: `Điện trở có nhiệt độ ổn định: hiệu điện thế hai đầu ${V('6{,}0')} thì ampe kế chỉ ${mA('24')}.<br><b>a)</b> điện trở ${m('R')} (Ω)<br><b>b)</b> tăng hiệu điện thế lên ${V('15')}: cường độ dòng điện (mA)`,
    nd: `Đổi ${f(10)} ra A trước khi thế số; nhiệt độ ổn định ⇒ ${m('R')} ${f(14)}`, a: ['a', 'b'], cot: 2, gi: 3 },
  { t: 'Dạng 2 · Dễ · X, Y: một điện trở thuần, một NTC',
    de: `<b>a)</b> điền ${m('U/I')} (kΩ) vào bảng<br><b>b)</b> đường đặc trưng nào thẳng qua gốc: ${f(10)}<br><b>c)</b> vì sao đường còn lại không thẳng`,
    bang: bangD2,
    nd: `V/mA = ${f(10)}; ${m('I')} tăng theo ${m('U')} chưa đủ, phải xét ${m('U/I')} ${f(16)}`, a: [], gi: 4 },
  { t: 'Dạng 3 · Trung bình · Hai đường đặc trưng, I tính bằng mA',
    de: `<div class="fig-side" style="grid-template-columns:1fr 28mm"><div>(1) của ${m('R_1')} qua ${nw('(6,0 V; 3,0 mA)')}, (2) của ${m('R_2')} qua ${nw('(6,0 V; 1,2 mA)')}.<br><b>a)</b> ${m('R_1')}, ${m('R_2')} (kΩ)<br><b>b)</b> đường nào dốc hơn; ${m('R')} của nó lớn hay nhỏ hơn<br><b>c)</b> đặt ${V('9{,}0')} vào ${m('R_2')}: dòng điện (mA)</div>${H.haiDuongD3('')}</div>`,
    nd: `Trục đứng là ${m('I')} ⇒ độ dốc ${nw(`${m('=')} ${f(12)}`)}; V/kΩ = ${f(10)}`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'], gi: 5 },
  { t: 'Dạng 4 · Trung bình · Từ U, I tìm nhiệt độ dây kim loại',
    de: `Nhiệt kế điện trở dây platin: ${m('R_0=100\\ \\Omega')} ở ${m('t_0=0\\ ^\\circ\\mathrm C')}; ${nw(m('\\alpha=3{,}9\\cdot10^{-3}\\ \\mathrm{K^{-1}}'))}. Đưa dây vào lò, đặt ${V('0{,}89')} vào hai đầu dây thì ampe kế chỉ ${mA('5{,}0')}.<br><b>a)</b> điện trở của dây trong lò<br><b>b)</b> nhiệt độ của lò<br><b>c)</b> thay dây platin bằng NTC: nhiệt độ tăng thì ${m('R')} tăng hay giảm`,
    nd: `${t0} đọc từ đề, không mặc định 20 °C; ${nw(`${m('R/R_0-1=')} ${f(16)}`)}`, a: ['a', 'b', 'c'], gi: 6, fig: H.loPt() },
  { t: 'Dạng 5 · Khó · Dây nung nicrom của bàn là',
    de: `Ở ${oC('20')}, dây nung nicrom có ${m('R_0=40{,}0\\ \\Omega')}, ${nw(m('\\rho_0=1{,}10\\cdot10^{-6}\\ \\Omega{\\cdot}\\mathrm m'))}; ${nw(m('\\alpha=0{,}40\\cdot10^{-3}\\ \\mathrm{K^{-1}}'))}. Bàn là cắm vào ${V('220')}; khi nóng ổn định dây ở ${oC('270')}.<br><b>a)</b> điện trở khi nóng ổn định<br><b>b)</b> cường độ dòng điện khi đó<br><b>c)</b> lúc vừa cắm (dây ${oC('20')}): dòng điện; gấp mấy lần dòng khi nóng<br><b>d)</b> điện trở suất khi nóng ổn định`,
    nd: `Mỗi trạng thái dùng ${m('R')} của ${f(25)}; ${m('\\rho')} theo cùng hệ số ${m('[1+\\alpha(t-t_0)]')}`, a: ['a', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>', 'd'], cot: 3, gi: 7, fig: H.rTheoT() },
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
const aPt = nw(m('\\alpha=3{,}9\\cdot10^{-3}\\ \\mathrm{K^{-1}}'));
const aNi = nw(m('\\alpha=0{,}40\\cdot10^{-3}\\ \\mathrm{K^{-1}}'));
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–3', 'DẠNG 4–5'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Điện trở có nhiệt độ ổn định. Hiệu điện thế hai đầu ${V('4{,}5')} thì dòng điện ${mA('15')}.<br><b>a)</b> điện trở ${m('R')} (Ω)<br><b>b)</b> tăng hiệu điện thế lên ${V('12')}: cường độ dòng điện (mA)`, o: ['a', 'b'] },
    { t: 'Dạng 1 · Bài 2', de: `Điện trở ${kOm('1{,}5')}, nhiệt độ ổn định, mắc vào ${V('9{,}0')}.<br><b>a)</b> cường độ dòng điện (mA)<br><b>b)</b> muốn dòng điện bằng ${mA('2{,}0')} thì hiệu điện thế bằng bao nhiêu`, o: ['a', 'b'] },
    { t: 'Dạng 2 · Bài 1', de: `Hai linh kiện: một điện trở thuần, một bóng đèn sợi đốt. X: ${nw('(2,0 V; 0,40 A)')}, ${nw('(4,0 V; 0,62 A)')}, ${nw('(6,0 V; 0,75 A)')}. Y: ${nw('(1,0 V; 0,25 A)')}, ${nw('(3,0 V; 0,75 A)')}, ${nw('(5,0 V; 1,25 A)')}.<br><b>a)</b> ${m('U/I')} (Ω) mỗi lần đo của X; của Y<br><b>b)</b> đường đặc trưng nào thẳng qua gốc<br><b>c)</b> linh kiện nào là đèn; vì sao ${m('U/I')} của nó đổi`, o: ['a<sub>X</sub>', 'a<sub>Y</sub>', 'b', 'c'], ow: { 'a<sub>X</sub>': 26, 'a<sub>Y</sub>': 22, b: 16, c: 64 } },
    { t: 'Dạng 2 · Bài 2', de: `Hai linh kiện: một điện trở thuần, một NTC. X: ${nw('(2,0 V; 1,0 mA)')}, ${nw('(4,0 V; 2,5 mA)')}, ${nw('(6,0 V; 4,8 mA)')}. Y: ${nw('(1,5 V; 0,50 mA)')}, ${nw('(3,0 V; 1,0 mA)')}, ${nw('(6,0 V; 2,0 mA)')}.<br><b>a)</b> ${m('U/I')} (kΩ) mỗi lần đo của X; của Y<br><b>b)</b> linh kiện nào là NTC; điện trở của nó tăng hay giảm khi dòng lớn dần`, o: ['a<sub>X</sub>', 'a<sub>Y</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>'], ow: { 'a<sub>X</sub>': 26, 'a<sub>Y</sub>': 22, 'b<sub>1</sub>': 14, 'b<sub>2</sub>': 20 } },
    { t: 'Dạng 3 · Bài 1', de: `Trục ngang ${m('U')} (V), trục đứng ${m('I')} (mA); hai đường thẳng qua gốc: (1) qua ${nw('(4,0 V; 2,0 mA)')}, (2) qua ${nw('(4,0 V; 0,50 mA)')}.<br><b>a)</b> ${m('R_1')}, ${m('R_2')} (kΩ)<br><b>b)</b> đường dốc hơn ứng với điện trở lớn hơn hay nhỏ hơn<br><b>c)</b> đặt ${V('10')} vào ${m('R_1')}: dòng điện (mA)`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'], ow: { 'a<sub>1</sub>': 16, 'a<sub>2</sub>': 16, b: 25, c: 16 } },
    { t: 'Dạng 3 · Bài 2', de: `<b>Chú ý trục:</b> trục ngang ${m('I')} (mA), trục đứng ${m('U')} (V); (1) qua ${nw('(2,0 mA; 6,0 V)')}, (2) qua ${nw('(2,0 mA; 3,0 V)')}.<br><b>a)</b> ${m('R_1')}, ${m('R_2')} (kΩ)<br><b>b)</b> đường dốc hơn ứng với điện trở lớn hơn hay nhỏ hơn<br><b>c)</b> đặt ${V('4{,}5')} vào ${m('R_2')}: dòng điện (mA)`, fig: H.uTheoI(), fw: 34, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'], ow: { 'a<sub>1</sub>': 14, 'a<sub>2</sub>': 14, b: 20, c: 14 } },
  ], [
    { t: 'Dạng 4 · Bài 1', de: `Nhiệt kế điện trở dây platin: ${m('R_0=100\\ \\Omega')} ở ${m('t_0=0\\ ^\\circ\\mathrm C')}; ${aPt}. Đặt ${V('0{,}278')} vào hai đầu dây trong nồi nước thì dòng điện ${mA('2{,}0')}.<br><b>a)</b> điện trở của dây<br><b>b)</b> nhiệt độ nước<br><b>c)</b> nước nóng thêm, giữ nguyên hiệu điện thế: số chỉ ampe kế tăng hay giảm`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 4 · Bài 2', de: `Cuộn dây đồng của động cơ: ${m('R_0=16\\ \\Omega')} ở ${oC('20')}; ${aCu}. Khi chạy, đặt ${V('12')} thì dòng điện ${A('0{,}60')}.<br><b>a)</b> điện trở cuộn dây khi chạy<br><b>b)</b> nhiệt độ cuộn dây<br><b>c)</b> đợi động cơ nguội hẳn rồi mới đo: ${m('R')} đo được lớn hơn hay nhỏ hơn câu a`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 5 · Bài 1', de: `Dây tóc vonfram: ở ${oC('20')} có ${m('R_0=10\\ \\Omega')}, ${nw(m('\\rho_0=5{,}5\\cdot10^{-8}\\ \\Omega{\\cdot}\\mathrm m'))}; ${aW}. Đèn cắm vào ${V('220')}, khi sáng dây tóc ở ${oC('2\\,020')}.<br><b>a)</b> điện trở khi sáng<br><b>b)</b> cường độ dòng điện khi sáng<br><b>c)</b> lúc vừa bật (dây ${oC('20')}): dòng điện; gấp mấy lần lúc sáng<br><b>d)</b> điện trở suất khi sáng`, o: ['a', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>', 'd'], ow: { 'c<sub>1</sub>': 16, 'c<sub>2</sub>': 14, d: 30 } },
    { t: 'Dạng 5 · Bài 2', de: `Dây nung bếp điện bằng nicrom: ở ${oC('20')} có ${m('R_0=50{,}0\\ \\Omega')}, ${nw(m('\\rho_0=1{,}10\\cdot10^{-6}\\ \\Omega{\\cdot}\\mathrm m'))}; ${aNi}. Cắm vào ${V('220')}; nóng ổn định ở ${oC('520')}.<br><b>a)</b> điện trở khi nóng<br><b>b)</b> cường độ dòng điện khi nóng<br><b>c)</b> lúc vừa cắm: dòng điện; gấp mấy lần dòng khi nóng<br><b>d)</b> điện trở suất khi nóng`, o: ['a', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>', 'd'], ow: { 'c<sub>1</sub>': 16, 'c<sub>2</sub>': 14, d: 30 } },
    nhap(7),
  ]],
  dap: [
    `D1·1: a) 300 Ω · b) 40 mA &nbsp;|&nbsp; D1·2: a) 6,0 mA · b) 3,0 V &nbsp;|&nbsp; D2·1: a<sub>X</sub>) 5,0; 6,5; 8,0 Ω · a<sub>Y</sub>) 4,0 Ω cả ba lần · b) Y · c) X, dây tóc nóng lên nên R tăng &nbsp;|&nbsp; D2·2: a<sub>X</sub>) 2,0; 1,6; 1,3 kΩ · a<sub>Y</sub>) 3,0 kΩ cả ba lần · b<sub>1</sub>) X · b<sub>2</sub>) giảm &nbsp;|&nbsp; D3·1: a<sub>1</sub>) 2,0 kΩ · a<sub>2</sub>) 8,0 kΩ · b) nhỏ hơn · c) 5,0 mA &nbsp;|&nbsp; D3·2: a<sub>1</sub>) 3,0 kΩ · a<sub>2</sub>) 1,5 kΩ · b) lớn hơn (trục đứng là U) · c) 3,0 mA`,
    `D4·1: a) 139 Ω · b) 100 °C · c) giảm &nbsp;|&nbsp; D4·2: a) 20 Ω · b) ≈ 84 °C · c) nhỏ hơn &nbsp;|&nbsp; D5·1: a) 100 Ω · b) 2,2 A · c<sub>1</sub>) 22 A · c<sub>2</sub>) 10 lần · d) 5,5·10<sup>−7</sup> Ω·m &nbsp;|&nbsp; D5·2: a) 60,0 Ω · b) 3,7 A · c<sub>1</sub>) 4,4 A · c<sub>2</sub>) 1,2 lần · d) 1,32·10<sup>−6</sup> Ω·m`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 2], kq: [[1, 2, 3], [4, 5]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'R, đổi đơn vị 1·4 · đo R 2·1 · Ohm 2·2 · ion 3·1 · đèn 3·2 · R(t) 3·3 · NTC 4·1 · bẫy 4·2 · mẫu 5·2 · dạng 1–3 6·1 · dạng 4–5 7·1',
  out: process.argv[2],
});
