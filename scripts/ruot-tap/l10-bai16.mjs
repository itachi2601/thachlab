// Ruột tập VL10 – Bài 16 · Định luật 3 Newton (lesson id 61). Quyển Chương 3 lớp 10: bài 13 = tr. 1–12 → bài 16 = tr. 37–48.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l10-bai16.mjs (SVG tự vẽ + 1 ảnh thực tế tên lửa từ book/assets/anh-that, public domain).
// Nội dung theo bài web (book/cache/61.json, tải từ DB 13/11/2026): mục tiêu, dự đoán thành sân, II.1–II.3 (lực–phản lực, 4 đặc điểm,
// hai lực kế), ba bẫy, Trả bài 6 câu, bài toán mẫu hai bạn trượt băng, đời sống, thử thách, 3 dạng bài tập mẫu.
// Đáp số Bài tương tự (tuongTu.dap) và mọi số trong ô điền tính bằng Python 13/11/2026.
// Chạy: node scripts/ruot-tap/l10-bai16.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl10-bai16.pdf
//       node scripts/ruot-tap/l10-bai16.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l10-bai16/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL10b16 as H } from './hinh-l10-bai16.mjs';

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
  const out = resolve(HERE, 'out/hinh-l10-bai16'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 16, lid: 61, ten: 'ĐỊNH LUẬT 3 NEWTON', lop: 10, baiDau: 13, sub: 'Vật lí 10 · Chương 3: Động lực học' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const FAB = m('\\vec F_{AB}'), FBA = m('\\vec F_{BA}');
const ms2 = (s) => nw(m(`${s}\\ \\mathrm{m/s^2}`));

const p1 = `<section class="page">
${head('BÀI 16 · ĐỊNH LUẬT 3 NEWTON', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Phát biểu <b>định luật 3 Newton</b> và viết được biểu thức của nó`)}
${dong(`${ck}Nêu <b>4 đặc điểm</b> của cặp lực – phản lực; phân biệt với <b>hai lực cân bằng</b>`)}
${dong(`${ck}Dùng định luật 2 cho <b>từng vật</b> để tính gia tốc của hai vật tương tác`)}
${dong(`${ck}Đọc bảng số đo hai lực kế, nhận ra <b>sai số đọc</b>`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Em đi giày trượt, hai tay đẩy mạnh vào thành sân băng (thành gắn chặt với mặt đất). Em sẽ chuyển động thế nào?</p>
<div class="fig-side" style="${fs(46)}"><div>
${opt('A', 'Đứng yên, vì thành sân không nhúc nhích')}
${opt('B', 'Trượt tiến về phía thành sân')}
${opt('C', 'Trượt lùi ra xa thành sân')}
${opt('D', 'Trượt sang bên, dọc theo thành sân')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 1)}</div>
${H.thanhSan()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f(12)} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Lực và phản lực', '1·4')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div>A tác dụng lên B một lực thì B cũng ${f(25)} lên A một lực.</div>
<div>Hai lực này gọi là ${f(25)} và ${f(25)}.</div>
<div>Chúng có cùng ${f(25)}, ngược ${f(25)}, cùng ${f(25)}.</div>
<div style="margin:1mm 0"><b>Định luật 3 Newton:</b> ${nw(`${m('\\vec F_{AB}=')} ${f(16)}`)}</div>
<div>${FAB}: lực ${f(12)} tác dụng lên ${f(12)}</div>
<div>${FBA}: lực ${f(12)} tác dụng lên ${f(12)}</div></div>
${H.boiBe()}</div>
<div class="card" style="margin-top:1.2mm;padding:1mm 3mm">${cau('<b>Thành sân cũng chịu lực đẩy của em. Vì sao thành sân không nhúc nhích mà em lại chuyển động?</b>', 2)}</div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('BỐN ĐẶC ĐIỂM · HAI LỰC KẾ · BẪY 1')}
${h3(1, 'II.2 · Ba Cùng – Một Ngược – Một Khác', '2·1')}
<table><tr><th style="width:30mm">Đặc điểm</th><th>Nghĩa là</th><th style="width:44mm">Ví dụ</th></tr>
<tr><td>Cùng ${f(18)}</td><td>cùng xuất hiện, cùng mất đi</td><td>hai kim lực kế đi cùng nhau</td></tr>
<tr><td>Cùng ${f(18)}</td><td>cùng bản chất (cùng hấp dẫn, cùng đàn hồi…)</td><td>Trái Đất hút táo, táo hút ${f(14)}</td></tr>
<tr><td>Cùng ${f(18)}</td><td>${m('F_{AB}=F_{BA}')} dù hai vật nặng nhẹ khác nhau</td><td>xe tải đâm xe con</td></tr>
<tr><td>Ngược ${f(18)}</td><td>cùng phương, chiều ngược nhau</td><td>em đẩy thành, thành đẩy em</td></tr>
<tr><td>Khác ${f(18)}</td><td>mỗi lực đặt lên một vật</td><td>lực em đẩy đặt lên ${f(14)}</td></tr></table>
${h3(2, 'II.3 · Thí nghiệm: hai lực kế kéo nhau', '2·2')}
<div class="card fig-side" style="${fs(52)};padding:1.2mm 3mm"><div>
<div><b>Làm:</b> móc hai lực kế ${nw('5 N')} (đã chỉnh số 0) vào nhau, đặt nằm ngang. Giữ đầu lực kế 1, kéo đầu lực kế 2 chậm, tăng dần qua 5 lần; mỗi lần đọc cả hai số chỉ.</div>
<div style="margin-top:.6mm"><b>Đọc được tới</b> ${nw(m('\\pm 0{,}1\\ \\mathrm N'))}.</div></div>
${H.lucKe()}</div>
<div class="fig-side" style="${fs(62)}">
<table class="tbl-ct"><tr><th>Lần</th><th>Lực kế 1 (N)</th><th>Lực kế 2 (N)</th></tr>
<tr><td>1</td><td>1,0</td><td>1,0</td></tr><tr><td>2</td><td>2,0</td><td>2,0</td></tr><tr><td>3</td><td>3,0</td><td>3,1</td></tr>
<tr><td>4</td><td>4,1</td><td>4,0</td></tr><tr><td>5</td><td>5,0</td><td>5,0</td></tr></table>
${box(`<div style="line-height:1.35">Lần 3 lực kế 2 chỉ lớn hơn ${nw('0,1 N')}, lần 4 lại nhỏ hơn ${nw('0,1 N')}. Có phải hai lực khác nhau không? Vì sao?</div>${lines(4)}`)}</div>
<div class="card" style="margin-top:1.2mm;padding:1mm 3mm"><b>Rút ra:</b> lực và phản lực có độ lớn ${f(25)}, xuất hiện ${f(25)}; mỗi lực kế chỉ đo lực đặt lên ${f(25)}.</div>
${h3(3, 'III · Bẫy 1 · “Bằng nhau, ngược chiều thì triệt tiêu”', '2·3')}
<div class="fig-side" style="${fs(44)}"><div>
<table><tr><th></th><th>Hai lực cân bằng</th><th>Lực – phản lực</th></tr>
<tr><td>Đặt lên</td><td>${f(25)}</td><td>${f(25)}</td></tr>
<tr><td>Triệt tiêu?</td><td>${f(25)}</td><td>${f(25)}</td></tr>
<tr><td>Loại lực</td><td>${f(25)}</td><td>${f(25)}</td></tr></table>
<div style="margin-top:1mm">Hai lực cân bằng: ${f(12)} và ${f(12)} · Lực – phản lực: ${f(12)} và ${f(12)}</div></div>
${H.sachBan()}</div>
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('NHẮC NHANH · HAI CÁI BẪY · TRẢ BÀI')}
${h3(1, 'Nhắc nhanh kiến thức cần dùng', '3·1')}
<div class="card soft" style="padding:1mm 3mm">
<div>Định luật 2: ${m('\\vec a=\\dfrac{\\vec F}{m}')}, ${m('\\vec a')} cùng hướng hợp lực, hợp lực chỉ gồm các lực <b>đặt lên chính vật đó</b>.</div>
<div>Vectơ đối ${m('-\\vec F')}: cùng độ lớn, cùng phương, ngược chiều với ${m('\\vec F')}. &nbsp;Từ nghỉ, gia tốc không đổi: ${nw(m('v=at'))}; ${nw(m('a=\\Delta v/\\Delta t'))}.</div></div>
${h3(2, 'Bẫy 2 · “Xe nặng đâm xe nhẹ thì lực lớn hơn”', '3·2')}
<table><tr><th style="width:44mm"></th><th>Xe tải ${nw('8000 kg')}</th><th>Xe con ${nw('1000 kg')}</th></tr>
<tr><td>Lực xe kia tác dụng lên nó</td><td>${f(25)}</td><td>${nw('40 000 N')}</td></tr>
<tr><td>Gia tốc ${m('a=F/m')}</td><td>${f(25)}</td><td>${f(25)}</td></tr></table>
<div style="margin-top:.6mm">Xe con hỏng nặng hơn vì ${f(25)} của nó lớn hơn, không phải vì ${f(25)} lớn hơn. Khi lực tương tác là hợp lực lên mỗi vật: ${nw(`${m('m_Aa_A=')} ${f(16)}`)}</div>
${h3(3, 'Bẫy 3 · “Phải có thứ gì bên ngoài để đẩy”', '3·3')}
<div class="fig-side" style="${fs(36)}"><div>
${cau('<b>Trong chân không, tên lửa đẩy vào cái gì? Cái gì đẩy tên lửa đi lên?</b>', 2)}
${cau('<b>Phi hành gia đứng yên ngoài không gian ném búa về phía trước. Người sẽ thế nào? Vì sao?</b>', 2)}</div>
${H.tenLua()}</div>
${h3(4, 'IV · Trả bài 6 câu', '3·4')}
${box(`${tb('1. Phát biểu định luật 3 Newton.')}${lines(1)}
${tb('2. Viết biểu thức, nói rõ từng kí hiệu.')}${lines(1)}
${tb('3. Bốn đặc điểm của cặp lực – phản lực.')}${lines(1)}
${tb('4. Hai lực cân bằng khác lực – phản lực ở đâu?')}${lines(1)}
${tb('5. Lực hai bên bằng nhau, sao gia tốc hai vật khác nhau?')}${lines(1)}
${tb('6. Hệ thức m<sub>A</sub>a<sub>A</sub> = m<sub>B</sub>a<sub>B</sub> suy ra từ đâu?')}${lines(1)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/6 câu · chưa thuộc: ${f(25)} ${nw(`→ đọc lại ô ${f(12)} Tập`)}</div>
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('TỰ KIỂM TRA · BÀI TOÁN MẪU')}
${h3(1, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '4·1')}
${rkHai([1, 2, 3], [4, 5, 6])}
${h3(2, 'V · Bài toán mẫu: hai bạn trượt băng đẩy nhau', '4·2')}
<div class="card soft" style="padding:1.2mm 3mm">Hai bạn A (${nw('40 kg')}) và B (${nw('60 kg')}) đứng đối diện nhau trên giày trượt, hai tay chạm nhau. Bạn A đẩy bạn B bằng lực ${nw('120 N')}. Bỏ qua ma sát. Tính gia tốc của mỗi bạn.</div>
${h3(3, 'Phân tích đề')}
<table><tr><th style="width:52mm">Câu trong đề</th><th>Dữ liệu → kiến thức</th></tr>
<tr><td>“A (40 kg) và B (60 kg)”</td><td>${m('m_A=40\\ \\mathrm{kg}')}, ${m('m_B=60\\ \\mathrm{kg}')}</td></tr>
<tr><td style="height:6.5mm">“giày trượt … bỏ qua ma sát”</td><td></td></tr>
<tr><td style="height:6.5mm">“A đẩy B bằng lực 120 N”</td><td></td></tr>
<tr><td style="height:6.5mm">“tính gia tốc của mỗi bạn”</td><td></td></tr></table>
${h3(4, 'Giải')}
<div class="fig-side" style="${fs(52)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl(`Lực lên B, lực lên A (định luật mấy?):`, 2)}${wl(`Gia tốc bạn A:`, 3)}${wl(`Gia tốc bạn B:`, 2)}${wl(`Kiểm tra ${m('m_Aa_A')} và ${m('m_Ba_B')}; hai bạn đi về đâu?`, 2)}</div>${H.haiBan()}</div>
${h3(5, 'Điền bước còn thiếu: B nặng 80 kg')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div class="ln">Cùng đề, A vẫn ${nw('40 kg')}, lực vẫn ${nw('120 N')}, B nặng ${nw('80 kg')}.</div>
<div class="ln"><b>Bước 1 (cho sẵn):</b> ${m('a_A=120/40=3\\ \\mathrm{m/s^2}')}</div>
${wl(`Bước 2: ${m('a_B=')}`, 1)}${wl(`Bước 3: so ${m('m_Aa_A')} với ${m('m_Ba_B')}:`, 1)}</div>
${h3(6, 'Câu đổi chiều: biết gia tốc, tìm lực', '4·3')}
${box(cau(`Cùng hai bạn A (${nw('40 kg')}) và B (${nw('60 kg')}) đẩy nhau, đo được ${nw(m('a_B=1\\ \\mathrm{m/s^2}'))}. Tìm lực đẩy và ${m('a_A')}.`, 3))}
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TẬP VỀ NHÀ · THỬ THÁCH · MANG VỀ')}
${K.btvn()}
${h3(2, 'Thử thách phân tầng', '5·2')}
${box(cau(`${m('\\bigstar')} A đẩy B bằng lực ${nw('30 N')}. Lực B đẩy A bằng bao nhiêu, hướng nào?`, 1)
 + cau(`${m('\\bigstar\\bigstar')} Hai bạn ${nw('50 kg')} và ${nw('40 kg')} đứng trên giày trượt, đẩy nhau bằng lực ${nw('100 N')}. Gia tốc mỗi bạn?`, 2))}
<div class="fig-side" style="${fs(50)};margin-top:1mm">${box(cau(`${m('\\bigstar\\bigstar\\bigstar')} Ngựa ${nw('400 kg')} kéo xe ${nw('200 kg')} bằng dây. Đất đẩy chân ngựa về trước ${nw('900 N')}, ma sát cản xe ${nw('300 N')}; ngựa và xe cùng gia tốc. Tính gia tốc và lực căng dây ${m('T')}.`, 0)
 + wl(`Phương trình của xe:`, 1) + wl(`Phương trình của ngựa:`, 1) + wl(`${m('a=')} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ${m('T=')}`, 1))}${H.nguaXeTT()}</div>
${h3(3, 'VI · Đời sống: ai đẩy lại ta?', '5·3')}
<table><tr><th style="width:40mm">Việc làm</th><th>Ta đẩy cái gì, về đâu?</th><th>Cái gì đẩy lại ta, về đâu?</th></tr>
<tr><td>Bơi</td><td>tay đẩy nước ra sau</td><td></td></tr>
<tr><td>Đi bộ</td><td></td><td>đất đẩy chân lên trước</td></tr>
<tr><td>Bắn súng</td><td>súng đẩy đạn về trước</td><td></td></tr>
<tr><td>Đá bóng</td><td>chân đẩy bóng về trước</td><td></td></tr></table>
${h3(4, 'Mang về: điều em dễ quên nhất', '5·4')}
${box(wl('1.', 2) + wl('2.', 2) + wl('3.', 2))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Đẩy tường trên giày trượt: lực của tường và gia tốc người',
    de: `Người ${m('60\\ \\mathrm{kg}')} đi giày trượt patin, đặt hai tay vào tường thẳng đứng rồi đẩy tường bằng lực nằm ngang ${m('90\\ \\mathrm N')}. Bỏ qua ma sát giữa giày và sàn.<br><b>a)</b> độ lớn lực tường tác dụng lên người<br><b>b)</b> gia tốc của người lúc đang đẩy`,
    nd: `Lực người đẩy tường đặt lên ${f(25)}; gia tốc của người chỉ tính bằng lực đặt lên ${f(25)}`, a: ['a', 'b'], gi: 8, fig: H.d1(), cot: 2 },
  { t: 'Dạng 2 · Trung bình · Ngựa kéo xe: lực xe kéo ngựa và gia tốc xe',
    de: `Ngựa kéo xe ${m('300\\ \\mathrm{kg}')} trên đường nằm ngang bằng lực ${m('800\\ \\mathrm N')} dọc dây kéo. Mặt đường tác dụng lên xe lực ma sát ${m('200\\ \\mathrm N')}.<br><b>a)</b> độ lớn lực xe kéo ngựa<br><b>b)</b> hợp lực lên xe<br><b>c)</b> gia tốc của xe`,
    nd: `Lực xe kéo ngựa đặt lên ${f(25)} nên ${ck}có ${ck}không cộng vào hợp lực lên xe`, a: ['a', 'b', 'c'], gi: 6, fig: H.d2() },
  { t: 'Dạng 3 · Khá · Hai xe va nhau: lực tương tác và độ giảm vận tốc',
    de: `Trên đường ray nhẵn nằm ngang, xe A ${m('1{,}5\\ \\mathrm{kg}')} chạy tới va vào xe B ${m('0{,}5\\ \\mathrm{kg}')} đang đứng yên. Trong ${m('0{,}2\\ \\mathrm s')} hai xe tương tác, xe B tăng tốc từ nghỉ đến ${m('2{,}4\\ \\mathrm{m/s}')}. Coi lực tương tác không đổi.<br><b>a)</b> gia tốc của xe B<br><b>b)</b> độ lớn lực tương tác<br><b>c)</b> gia tốc của xe A<br><b>d)</b> độ giảm vận tốc của xe A`,
    nd: `Biết ${m('\\Delta v')} của xe ${f(12)} → ${nw(`${m('a=')} ${f(14)}`)} → ${nw(`${m('F=')} ${f(14)}`)}; lực lên xe kia ${f(25)} nên ${nw(`${m('a_A=')} ${f(14)}`)}`, a: ['a', 'b', 'c', 'd'], gi: 14, fig: H.d3(),
    bang: `<table style="margin:.6mm 0"><tr><th style="width:56mm">Câu trong đề</th><th>Dữ liệu → kiến thức</th></tr>
<tr><td>“đường ray nhẵn”</td><td style="height:6.5mm"></td></tr>
<tr><td>“B tăng tốc từ nghỉ đến 2,4 m/s trong 0,2 s”</td><td style="height:6.5mm"></td></tr>
<tr><td>“lực tương tác không đổi”</td><td style="height:6.5mm"></td></tr>
<tr><td>“độ giảm vận tốc của xe A”</td><td style="height:6.5mm"></td></tr></table>` },
];

// Bài tương tự: mỗi dạng 2 bài, giải vào vở (thầy chốt 10/11): 1 cột, ô đáp số 25 mm đặt cuối đúng dòng của ý, nhãn khớp a) b) c)…
// Đáp số tính bằng Python 13/11/2026 (xem ghi chú đầu file).
const ttCss = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';
const oY = (s, o, w = 25) => s.split('<br>').map((p) => {
  const y = p.match(/^<b>([a-d])\)<\/b>/);
  if (!y) return `<div>${p}</div>`;
  const ls = o.filter((l) => l[0] === y[1]);
  return `<div class="yo"><span>${p}</span><span class="oo">${ls.map((l) => `<span class="nw"><b>${l})</b>${f(w)}</span>`).join('')}</span></div>`;
}).join('');
const vaoVo = (ds) => ds.map((b) => (b.o ? { t: b.t, de: oY(b.de, b.o, b.ow), k: 0 } : b));
const nhap = (n) => ({ t: '<span class="nhap-t">Nháp / chỗ em còn vướng</span>', de: lines(n), k: 0 });
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–2', 'DẠNG 3'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Bạn ${m('50\\ \\mathrm{kg}')} đi giày trượt đẩy tường bằng lực nằm ngang ${m('75\\ \\mathrm N')}; bỏ qua ma sát.<br><b>a)</b> độ lớn lực tường tác dụng lên bạn<br><b>b)</b> gia tốc của bạn lúc đang đẩy<br><b>c)</b> đẩy trong ${m('0{,}4\\ \\mathrm s')} từ nghỉ: tốc độ lúc rời tường`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 1 · Bài 2', de: `Phi hành gia ${m('80\\ \\mathrm{kg}')} (kể cả bộ đồ) lơ lửng đứng yên cạnh trạm vũ trụ, đẩy vào thành trạm bằng lực ${m('40\\ \\mathrm N')} trong ${m('0{,}5\\ \\mathrm s')}.<br><b>a)</b> độ lớn lực thành trạm tác dụng lên người<br><b>b)</b> gia tốc của người lúc đang đẩy<br><b>c)</b> tốc độ của người lúc rời thành trạm`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 2 · Bài 1', de: `Đầu máy kéo toa xe ${m('2000\\ \\mathrm{kg}')} trên đường ray nằm ngang bằng lực ${m('5000\\ \\mathrm N')}; lực cản lên toa ${m('1000\\ \\mathrm N')}.<br><b>a)</b> độ lớn lực toa kéo đầu máy<br><b>b)</b> hợp lực lên toa<br><b>c)</b> gia tốc của toa`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 2 · Bài 2', de: `Nam kéo thùng ${m('40\\ \\mathrm{kg}')} trên sàn ngang bằng dây nằm ngang, lực ${m('120\\ \\mathrm N')}; ma sát lên thùng ${m('80\\ \\mathrm N')}.<br><b>a)</b> độ lớn lực thùng kéo Nam<br><b>b)</b> gia tốc của thùng<br><b>c)</b> Hà nói: “Nam kéo thùng ${nw('120 N')}, thùng kéo Nam ${nw('120 N')}, triệt tiêu nên thùng đứng yên.” Đúng hay sai?`, o: ['a', 'b', 'c'] },
    nhap(12),
  ], [
    { t: 'Dạng 3 · Bài 1', de: `Trên đường ray nhẵn, xe A ${m('2{,}0\\ \\mathrm{kg}')} chạy tới va vào xe B ${m('1{,}0\\ \\mathrm{kg}')} đang đứng yên. Trong ${m('0{,}1\\ \\mathrm s')} tương tác, xe B tăng tốc từ nghỉ đến ${m('3{,}0\\ \\mathrm{m/s}')}. Coi lực tương tác không đổi.<br><b>a)</b> gia tốc của xe B<br><b>b)</b> độ lớn lực tương tác<br><b>c)</b> gia tốc của xe A<br><b>d)</b> độ giảm vận tốc của xe A`, o: ['a', 'b', 'c', 'd'] },
    { t: 'Dạng 3 · Bài 2', de: `Hai bạn A ${m('45\\ \\mathrm{kg}')} và B ${m('60\\ \\mathrm{kg}')} đứng yên trên giày trượt, đẩy tay nhau trong ${m('0{,}5\\ \\mathrm s')}; bỏ qua ma sát. Lúc buông tay, A đạt tốc độ ${m('2{,}0\\ \\mathrm{m/s}')}. Coi lực đẩy không đổi.<br><b>a)</b> gia tốc của A<br><b>b)</b> độ lớn lực đẩy<br><b>c)</b> gia tốc của B<br><b>d)</b> tốc độ của B lúc buông tay`, o: ['a', 'b', 'c', 'd'] },
    nhap(21),
  ]],
  dap: [
    `D1·1: a) 75 N · b) 1,5 m/s² · c) 0,6 m/s &nbsp;|&nbsp; D1·2: a) 40 N · b) 0,5 m/s² · c) 0,25 m/s &nbsp;|&nbsp; D2·1: a) 5000 N · b) 4000 N · c) 2,0 m/s² &nbsp;|&nbsp; D2·2: a) 120 N · b) 1,0 m/s² · c) sai (hai lực đặt lên hai vật khác nhau)`,
    `D3·1: a) 30 m/s² · b) 30 N · c) 15 m/s² · d) 1,5 m/s &nbsp;|&nbsp; D3·2: a) 4,0 m/s² · b) 180 N · c) 3,0 m/s² · d) 1,5 m/s`,
  ],
};

await K.dung({
  trang1to5: ttCss + [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [2, 1], kq: [[1, 2], [3]], khoNhat: true },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'lực – phản lực 1·4 · bốn đặc điểm 2·1 · hai lực kế 2·2 · bẫy 1 2·3 · nhắc nhanh 3·1 · bẫy 2–3 3·2–3·3 · bài toán mẫu 4·2 · dạng 1–2 → 6·1 · dạng 3 → 7·1',
  out: process.argv[2],
});
