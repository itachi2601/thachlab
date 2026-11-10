// Ruột tập VL10 – Bài 23 · Năng lượng. Công cơ học (lesson id 68). Quyển Chương 4 lớp 10: bài 23 = tr. 1–12.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l10-bai23.mjs (toàn bộ SVG tự vẽ, không dùng ảnh Halliday). Nội dung theo bài web (book/cache/68.json, tải từ DB 10/11/2026):
// mục tiêu, dự đoán sân băng, II.1–II.3, hai thí nghiệm, ba bẫy, Trả bài 6 câu, bài toán mẫu ván trượt, thử thách, 5 dạng bài tập mẫu.
// Đáp số Bài tương tự (tuongTu.dap) tính bằng Python 10/11/2026; Bài tương tự xếp 2 cột bằng <style> riêng (ttHaiCot) vì khung xếp dọc.
// Không dùng ảnh Halliday.
// Chạy: node scripts/ruot-tap/l10-bai23.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl10-bai23.pdf
//       node scripts/ruot-tap/l10-bai23.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l10-bai23/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL10b23 as H } from './hinh-l10-bai23.mjs';

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
  const out = resolve(HERE, 'out/hinh-l10-bai23'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 23, lid: 68, ten: 'NĂNG LƯỢNG · CÔNG CƠ HỌC', lop: 10, baiDau: 23, sub: 'Vật lí 10 · Chương 4: Năng lượng, công, công suất' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const g10 = m('g=10\\ \\mathrm{m/s^2}');
const vF = m('\\vec F'), vd = m('\\vec d'), al = m('\\alpha');

// Bài tương tự xếp 2 cột (khung xếp .tt dọc, 10 bài không vừa 2 trang khi mỗi ý một dòng) — đề xuất đưa vào khung.
const ttHaiCot = '<style>.page:has(>.tt){display:flex;flex-wrap:wrap;column-gap:2mm;align-content:flex-start}.page:has(>.tt)>*{flex:1 1 100%}.page:has(>.tt)>.tt{flex:0 0 calc(50% - 1mm);min-width:0;display:flex;flex-direction:column}.tt .de{flex:1}</style>';
const p1 = `${ttHaiCot}<section class="page">
${head('BÀI 23 · NĂNG LƯỢNG · CÔNG CƠ HỌC', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Kể được các <b>dạng năng lượng</b>; nêu sự chuyển hoá và <b>bảo toàn</b> năng lượng`)}
${dong(`${ck}Dùng ${m('A=Fs\\cos\\alpha')} và xét <b>dấu của công</b> theo góc ${al}`)}
${dong(`${ck}Tính công của <b>trọng lực</b> và của <b>lực ma sát</b>`)}
${dong(`${ck}Nhận ra khi nào một lực <b>không sinh công</b>`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Theo vật lí, ai đã thực hiện công lên vật mình tác dụng lực?</p>
<div class="fig-side" style="${fs(50)}"><div>
${opt('A', 'Chỉ Minh, vì giữ ba lô lâu và mỏi tay hơn')}
${opt('B', 'Chỉ Lan, vì Hà dịch chuyển theo hướng lực')}
${opt('C', 'Cả hai như nhau, vì cả hai đều dùng lực tay')}
${opt('D', 'Không ai, vì không có vật nào nóng lên')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 1)}</div>
${H.sanBang()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Năng lượng: nhiều dạng, không tự mất', '1·4')}
<div class="card" style="padding:1.2mm 3mm">
<div>Năng lượng tồn tại ở nhiều ${f(12)}; ${f(16)} từ dạng này sang dạng khác hoặc ${f(14)} từ vật này sang vật khác.</div>
<div><b>Bảo toàn:</b> năng lượng không tự ${f(14)}, không tự ${f(14)}.</div>
<div>Đại lượng ${f(10)} hướng, đơn vị ${f(10)}; ${m('1\\ \\mathrm{cal}=')} ${nw(`${f(12)}&nbsp;J`)}</div>
<div>Hai nhóm lớn: ${f(12)} năng (do chuyển động) · ${f(12)} năng (do vị trí, trạng thái).</div>
<div>Tên dạng: dây cung căng ${f(12)} · than đỏ ${f(12)} · dòng điện sạc ${f(12)} · nắng chiếu pin ${f(12)}</div></div>
${h3(5, 'Thí nghiệm: quả bóng nảy thấp dần', '1·5')}
<div class="card fig-side" style="${fs(37)};padding:1.2mm 3mm"><div>
<div><b>Làm:</b> thả bóng tennis từ cao 1 m xuống sàn gạch, nhìn độ cao mỗi lần nảy.</div>
<div><b>Rút ra:</b> thế năng ${m('\\leftrightarrow')} ${f(14)} năng; mỗi lần chạm sàn, một phần thành ${f(12)} năng và ${f(12)}.</div>
${wl('Bóng nằm yên. Năng lượng lúc thả đi đâu?', 2)}</div>
${H.bongNay()}</div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('CÔNG CƠ HỌC · DẤU CỦA CÔNG · TRỌNG LỰC, MA SÁT')}
${h3(1, 'II.2 · Công cơ học', '2·1')}
<div class="card fig-side" style="${fs(50)};padding:1.2mm 3mm"><div>
<div>Lực làm vật ${f(16)} thì lực thực hiện công, tức là ${f(14)} năng lượng cho vật.</div>
<div style="margin:.6mm 0">${m('A=')} ${f(8)} · ${f(8)} · ${f(12)} &nbsp;(vật đi thẳng một chiều: ${m('d=s')})</div>
<div>${al} là góc giữa ${f(8)} và ${f(8)}. &nbsp;${m('1\\ \\mathrm{J}=1')} ${nw(f(12))}</div>
<div>Chỉ phần lực dọc đường đi, ${f(14)}, mới sinh công.</div></div>
${H.phanTichLuc()}</div>
${h3(2, 'Dấu của công', '2·2')}
<div class="fig-side" style="${fs(56)}"><table>
<tr><th style="width:37mm">Góc ${al}</th><th style="width:16mm">Dấu ${m('A')}</th><th>Tên gọi</th></tr>
<tr><td>${m('0^\\circ\\le\\alpha\\lt 90^\\circ')}</td><td></td><td></td></tr>
<tr><td>${m('\\alpha=90^\\circ')}</td><td></td><td></td></tr>
<tr><td>${m('90^\\circ\\lt\\alpha\\le 180^\\circ')}</td><td></td><td></td></tr></table>
${H.dauCong()}</div>
<div style="margin-top:1mm">${vF} cùng hướng ${vd}: ${m('A=')} ${f(14)} &nbsp;·&nbsp; ${vF} ngược hướng ${vd}: ${m('A=')} ${f(14)}</div>
<div>Chuyển động đều vẫn có dịch chuyển, nên từng lực ${f(16)} sinh công.</div>
${h3(3, 'II.3 · Trọng lực và ma sát trượt', '2·3')}
<div class="card fig-side" style="${fs(50)};padding:1.2mm 3mm"><div>
<div>Vật đi xuống, độ cao giảm ${m('h')}: ${m('A_P=')} ${f(14)}</div>
<div>Vật đi lên, độ cao tăng ${m('h')}: ${m('A_P=')} ${f(14)}</div>
<div>Vật đi ngang: ${m('A_P=')} ${f(10)}</div>
<div>Lên dốc dài ${m('s')}, nghiêng ${m('\\theta')}: ${m('h=')} ${f(14)}</div>
<div>Ma sát trượt, quãng đường ${m('s')}: ${m('A_{\\mathrm{ms}}=')} ${f(14)} &nbsp;(góc ${al} = ${nw(f(10))}, công luôn ${f(10)})</div></div>
${H.docTrongLuc()}</div>
${h3(4, 'Làm nhanh', '2·4')}
${box(cau(`<b>Câu 1.</b> Kéo vali bằng lực 50 N, dây hợp với phương ngang ${m('60^\\circ')}, vali đi thẳng 20 m trên sàn ngang. Công của lực kéo?`, 2)
 + cau(`<b>Câu 2.</b> Thang máy hạ cabin thẳng đứng xuống, chậm đều. Công của lực căng cáp dương, âm hay bằng 0? Vì sao?`, 2))}
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('THÍ NGHIỆM MẶT NGHIÊNG · BẪY · TRẢ BÀI')}
${h3(1, 'Thí nghiệm: đưa xe lên cùng độ cao bằng nhiều đường', '3·1')}
<div class="fig-side" style="${fs(42)}"><div>
<table class="tbl-ct"><tr><th>${m('s\\ (\\mathrm m)')}</th><th>${m('F\\ (\\mathrm N)')}</th><th>${m('A=Fs\\ (\\mathrm J)')}</th></tr>
<tr><td>0,20 (kéo thẳng đứng)</td><td>2,00</td><td></td></tr>
<tr><td>0,40</td><td>1,06</td><td></td></tr>
<tr><td>0,80</td><td>0,56</td><td></td></tr>
<tr><td>1,00</td><td>0,46</td><td></td></tr></table>
</div>
${H.keoXe()}</div>
<div class="card" style="margin-top:.6mm;padding:1mm 3mm">
<div>So cột cuối với ${m('Ph=')} ${nw(`${f(10)}&nbsp;J`)}. Lệch nhiều nhất ở ${m('s=')} ${nw(`${f(10)}&nbsp;m`)}; phần dôi ra đi đâu?</div>${lines(1)}
<div><b>Rút ra:</b> mặt nghiêng lợi về ${f(12)}, thiệt về ${f(14)}, không lợi về ${f(10)}.</div></div>
${h3(2, 'III · Ba cái bẫy hay sập', '3·2')}
<div class="card fig-side" style="${fs(34)};padding:1mm 3mm"><div>
<div class="trap">${ck}<span><b>“Mỏi tay là có công.”</b> Cầm vật đứng yên: ${m('d=0')}. Xách xô đi ngang: lực tay vuông góc đường đi. Cả hai ${m('A=0')}.</span></div>
<div class="trap">${ck}<span><b>“Lấy quãng đường của người đẩy.”</b> Lấy ${m('s')} của vật nhận lực: đẩy xe tải đứng yên thì ${m('A=0')}.</span></div>
<div class="trap">${ck}<span><b>“${al} là góc dốc.”</b> ${al} là góc giữa ${vF} và ${vd}: kéo song song dốc thì ${m('\\alpha=0^\\circ')}.</span></div></div>
${H.xachXo()}</div>
${h3(3, 'IV · Trả bài 6 câu', '3·3')}
${box(`${tb('1. Kể 5 dạng năng lượng, mỗi dạng một ví dụ.')}${lines(2)}
${tb('2. Phát biểu định luật bảo toàn năng lượng.')}${lines(1)}
${tb('3. Công thức công, ý nghĩa từng kí hiệu, đơn vị.')}${lines(2)}
${tb('4. Khi nào công dương, âm, bằng 0? Gọi tên.')}${lines(2)}
${tb('5. Công của trọng lực và của ma sát trượt tính thế nào?')}${lines(2)}
${tb('6. Hai trường hợp mỏi tay mà công bằng 0?')}${lines(1)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/6 câu · chưa thuộc: ${f(24)} → đọc lại Tập ${f(12)}</div>
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('TỰ KIỂM TRA · BÀI TOÁN MẪU')}
${h3(1, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '4·1')}
${rkHai([1, 2, 3], [4, 5, 6])}
${h3(2, 'V · Bài toán mẫu: kéo ván trượt trên sân băng', '4·2')}
<div class="card soft" style="padding:1.2mm 3mm">Trên sân băng nằm ngang, Lan kéo ván trượt chở em nhỏ, tổng khối lượng ${m('30\\ \\mathrm{kg}')}, bằng dây chếch lên hợp với phương ngang ${m('30^\\circ')}, lực kéo ${m('40\\ \\mathrm N')}. Ván đi thẳng ${m('15\\ \\mathrm m')}. Hệ số ma sát trượt ${m('0{,}05')}, lấy ${m('g=10\\ \\mathrm{m/s^2}')}.
<div>Tính công của lực kéo, trọng lực, phản lực và lực ma sát.</div></div>
${h3(3, 'Phân tích đề')}
<table><tr><th style="width:50mm">Câu trong đề</th><th>Dữ liệu → kiến thức</th></tr>
<tr><td>“tổng khối lượng 30 kg”</td><td>${m('P=mg=300\\ \\mathrm N')}</td></tr>
<tr><td style="height:6.5mm">“chếch lên … 30°, lực kéo 40 N”</td><td></td></tr>
<tr><td style="height:6.5mm">“nằm ngang … đi thẳng 15 m”</td><td></td></tr>
<tr><td style="height:6.5mm">“hệ số ma sát trượt 0,05”</td><td></td></tr>
<tr><td style="height:6.5mm">Dữ kiện ngầm: ván không chuyển động theo phương thẳng đứng</td><td></td></tr></table>
${h3(4, 'Giải')}
<div class="fig-side" style="${fs(52)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl(`Công lực kéo ${m('A_F')}:`, 2)}${wl(`Công của ${m('P')}, ${m('N')}:`, 1)}${wl(`Phản lực ${m('N')} và ${m('F_{\\mathrm{ms}}')}:`, 3)}${wl(`Công ma sát ${m('A_{\\mathrm{ms}}')}:`, 2)}${wl('Tổng công, dấu có hợp lí?', 2)}</div>${H.vanTruot()}</div>
${h3(5, 'Điền bước còn thiếu: Lan kéo dây nằm ngang')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl(`Bước 1: ${m('A_F=')}`, 1)}${wl(`Bước 2: ${m('N=')} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ${m('F_{\\mathrm{ms}}=')}`, 1)}
<div class="ln"><b>Bước 3 (cho sẵn):</b> ${m('A_{\\mathrm{ms}}=-F_{\\mathrm{ms}}\\,s=')} ${f(16)}</div></div>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TẬP VỀ NHÀ · THỬ THÁCH · MANG VỀ')}
${K.btvn()}
${h3(2, 'Thử thách phân tầng', '5·2')}
<div class="fig-side" style="${fs(44)}">${box(wl(`${m('\\bigstar')} Nâng đều hộp 2 kg lên kệ cao 1,5 m (${g10}). Công của lực nâng?`, 3)
 + wl(`${m('\\bigstar\\bigstar')} Sô-cô-la ghi 200 kcal (1 kcal = 1000 cal): bao nhiêu J? Đủ nâng người 50 kg lên cao bao nhiêu?`, 3)
 + wl(`${m('\\bigstar\\bigstar\\bigstar')} Vật 2 kg trượt xuống hết dốc dài 4 m nghiêng 30°, ${m('\\mu=0{,}1')}: công của trọng lực, phản lực, ma sát?`, 5))}${H.docTruot()}</div>
${h3(3, 'Câu đổi chiều (bài toán mẫu)', '5·3')}
${box(wl('Cùng đề, Lan đẩy ván từ phía sau, lực 40 N chếch <b>xuống</b> 30°. Tính N, F<sub>ms</sub>, công ma sát. Đẩy chếch xuống có lợi không?', 5))}
${h3(4, 'VI · Mang về: điều em dễ quên nhất', '5·4')}
${box(wl('1.', 3) + wl('2.', 3) + wl('3.', 3))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Chuyển hoá và bảo toàn năng lượng',
    de: `Máy xay sinh tố nhận ${m('300\\ \\mathrm J')} điện năng mỗi giây; lưỡi dao và hoa quả nhận ${m('240\\ \\mathrm J')} động năng mỗi giây, phần còn lại làm nóng động cơ và thành tiếng ồn.<br><b>a)</b> điện năng chuyển thành những dạng nào<br><b>b)</b> phần thành nhiệt và âm mỗi giây<br><b>c)</b> phần đó trong ${m('20\\ \\mathrm s')}<br><b>d)</b> An nói “tắt máy thì phần ấy mất hẳn”: đúng hay sai`,
    nd: `Năng lượng vào bằng ${f(14)} các phần năng lượng ra; phần nhiệt, âm tản vào ${f(14)}`, a: ['a', 'b', 'c', 'd'], gi: 0 },
  { t: 'Dạng 2 · Dễ · Lực cùng phương với dịch chuyển',
    de: `Nam đẩy xe siêu thị đi thẳng <b>đều</b> ${m('12\\ \\mathrm m')} trên sàn ngang, lực đẩy ${m('25\\ \\mathrm N')} theo chiều chuyển động; sàn tác dụng lực cản dọc đường đi.<br><b>a)</b> công của lực đẩy<br><b>b)</b> công của lực cản<br><b>c)</b> tổng công của hai lực`,
    nd: `Đi đều ⇒ hợp lực ${f(8)} ⇒ ${m('F_c=')} ${f(8)}; cùng hướng: ${m('A=+Fs')}, ngược hướng: ${nw(`${m('A=')} ${f(10)}`)}`, a: ['a', 'b', 'c'], gi: 0 },
  { t: 'Dạng 3 · Trung bình · Lực xiên góc và dấu của công',
    de: `Thùng trượt thẳng ${m('8{,}0\\ \\mathrm m')} trên sàn ngang; lực ${m('F=70\\ \\mathrm N')} trong ba tình huống:<br><b>a)</b> ${vF} hợp với hướng chuyển động ${m('60^\\circ')}<br><b>b)</b> ${vF} thẳng đứng, hướng lên<br><b>c)</b> ${vF} hợp với hướng chuyển động ${m('120^\\circ')}<br>Tính công và gọi tên: phát động, cản hay không sinh công.`,
    nd: `${m('A=Fs\\cos\\alpha')}; dấu của ${f(12)} quyết định loại công; lực thẳng đứng, đường ngang ⇒ ${nw(`${m('\\alpha=')} ${f(8)}`)}`, a: ['a', 'b', 'c'], gi: 3, fig: H.baGoc3() },
  { t: 'Dạng 4 · Trung bình · Trọng lực lên, xuống dốc và ma sát',
    de: `Kéo đều thùng ${m('40\\ \\mathrm{kg}')} lên dốc nghiêng ${m('30^\\circ')}, đi ${m('6{,}0\\ \\mathrm m')} dọc dốc; ma sát trượt ${m('40\\ \\mathrm N')}; ${m('g=10\\ \\mathrm{m/s^2}')}.<br><b>a)</b> độ cao nâng lên ${m('h')} và công của trọng lực<br><b>b)</b> công của ma sát lúc kéo lên<br><b>c)</b> thùng trượt xuống đúng ${m('6{,}0\\ \\mathrm m')} về chỗ cũ: công của trọng lực và của ma sát`,
    nd: `Trọng lực tính theo ${f(10)} (${m('h=s\\sin\\theta')}), dấu theo lên/xuống; ma sát tính theo ${f(10)}, luôn ${f(8)}`, a: ['a', 'b', 'c'], gi: 4, fig: H.docD4() },
  { t: 'Dạng 5 · Khó · Nhiều lực: tìm N, lực ma sát rồi công từng lực',
    de: `Kéo thùng ${m('25\\ \\mathrm{kg}')} trên nền ngang bằng dây chếch lên ${m('30^\\circ')}, lực ${m('100\\ \\mathrm N')}; thùng đi thẳng ${m('12\\ \\mathrm m')}; hệ số ma sát trượt ${m('0{,}20')}; ${m('g=10\\ \\mathrm{m/s^2}')}.<br><b>a)</b> công của lực kéo<br><b>b)</b> công của trọng lực và phản lực<br><b>c)</b> công của lực ma sát<br><b>d)</b> tổng công`,
    nd: `Lực kéo chếch lên nâng bớt thùng: ${m('N=P-')} ${f(14)}, không lấy ${m('N=mg')}; ${nw(m('F_{\\mathrm{ms}}=\\mu N'))}`, a: ['a', 'b', 'c', 'd'], gi: 5, fig: H.thungKeo() },
];

// Bài tương tự: mỗi dạng 2 bài, đáp số tính bằng Python (python3, math.cos/sin theo radian), làm tròn 3 chữ số có nghĩa.
const de = (s, fig, w = 44) => `${s}<div style="max-width:${w}mm;margin:.8mm auto 0">${fig}</div>`;
const tuongTu = {
  tieuDe: ['DẠNG 1–3', 'DẠNG 4–5'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Bóng đèn LED nhận ${m('10\\ \\mathrm J')} điện năng mỗi giây, phát ra ${m('4{,}0\\ \\mathrm J')} quang năng mỗi giây, phần còn lại thành nhiệt.<br><b>a)</b> điện năng chuyển thành những dạng nào<br><b>b)</b> nhiệt năng toả ra mỗi giây<br><b>c)</b> nhiệt năng toả ra trong ${m('60\\ \\mathrm s')}`, k: 3 },
    { t: 'Dạng 1 · Bài 2', de: `Thả quả bóng có thế năng ${m('12\\ \\mathrm J')} (so với sàn). Sau lần nảy đầu, ở điểm cao nhất bóng còn thế năng ${m('9{,}0\\ \\mathrm J')}.<br><b>a)</b> năng lượng đã thành nhiệt và âm ở lần chạm sàn đầu<br><b>b)</b> lần nảy sau cũng mất ${m('25\\,\\%')} năng lượng đang có: thế năng ở đỉnh lần nảy thứ hai<br><b>c)</b> bóng nằm yên: tổng nhiệt và âm đã sinh ra`, k: 3 },
    { t: 'Dạng 2 · Bài 1', de: `Kéo vali đi thẳng <b>đều</b> ${m('15\\ \\mathrm m')} trên sàn ngang, lực kéo ${m('40\\ \\mathrm N')} theo chiều chuyển động; sàn cản dọc đường đi.<br><b>a)</b> công lực kéo<br><b>b)</b> công lực cản<br><b>c)</b> tổng công`, k: 3 },
    { t: 'Dạng 2 · Bài 2', de: `Đẩy xe hàng ${m('20\\ \\mathrm m')} trên sàn ngang, lực đẩy ${m('50\\ \\mathrm N')} theo chiều chuyển động, lực cản ${m('35\\ \\mathrm N')} ngược chiều.<br><b>a)</b> công lực đẩy<br><b>b)</b> công lực cản<br><b>c)</b> tổng công; xe đi đều hay nhanh dần?`, k: 3 },
    { t: 'Dạng 3 · Bài 1', de: de(`Vật đi thẳng ${m('10\\ \\mathrm m')} trên sàn ngang; lực ${m('F=50\\ \\mathrm N')} hợp với hướng đi:<br><b>a)</b> ${m('30^\\circ')}<br><b>b)</b> ${m('90^\\circ')}<br><b>c)</b> ${m('150^\\circ')}<br>Tính công, gọi tên loại công.`, H.baGocTT('Cùng F, cùng s, đổi góc.'), 48), k: 3 },
    { t: 'Dạng 3 · Bài 2', de: `Kéo xe trượt tuyết đi ${m('25\\ \\mathrm m')} trên mặt ngang bằng dây hợp với phương ngang ${m('45^\\circ')}, lực ${m('60\\ \\mathrm N')}.<br><b>a)</b> công lực kéo<br><b>b)</b> công nếu dây nằm ngang<br><b>c)</b> dây hợp góc bao nhiêu thì công còn ${m('750\\ \\mathrm J')}`, k: 3 },
  ], [
    { t: 'Dạng 4 · Bài 1', de: de(`Vật ${m('5{,}0\\ \\mathrm{kg}')} trượt xuống hết dốc dài ${m('8{,}0\\ \\mathrm m')} nghiêng ${m('30^\\circ')}; ma sát trượt ${m('6{,}0\\ \\mathrm N')}; ${g10}.<br><b>a)</b> độ cao ${m('h')} của dốc<br><b>b)</b> công của trọng lực<br><b>c)</b> công của lực ma sát`, H.docTT('Trượt xuống: dấu của từng công?'), 48), k: 5 },
    { t: 'Dạng 4 · Bài 2', de: `Kéo đều thùng ${m('20\\ \\mathrm{kg}')} lên hết dốc dài ${m('10\\ \\mathrm m')}, đỉnh dốc cao ${m('2{,}0\\ \\mathrm m')}; ma sát trượt ${m('30\\ \\mathrm N')}; ${g10}.<br><b>a)</b> công của trọng lực khi lên<br><b>b)</b> công của ma sát khi lên<br><b>c)</b> thùng trượt xuống về chỗ cũ (ma sát vẫn ${m('30\\ \\mathrm N')}): công của trọng lực, của ma sát<br><b>d)</b> tổng công trọng lực cả đi lẫn về`, k: 7 },
    { t: 'Dạng 5 · Bài 1', de: `Kéo thùng ${m('20\\ \\mathrm{kg}')} trên nền ngang bằng dây chếch lên ${m('30^\\circ')}, lực ${m('80\\ \\mathrm N')}; thùng đi ${m('10\\ \\mathrm m')}; ${m('\\mu=0{,}25')}; ${g10}.<br><b>a)</b> phản lực ${m('N')} và lực ma sát<br><b>b)</b> công lực kéo<br><b>c)</b> công của ${m('P')}, ${m('N')}, ma sát<br><b>d)</b> tổng công`, k: 8 },
    { t: 'Dạng 5 · Bài 2', de: `Đẩy xe ${m('30\\ \\mathrm{kg}')} trên nền ngang từ phía sau, lực ${m('100\\ \\mathrm N')} chếch <b>xuống</b> ${m('30^\\circ')} so với phương ngang; xe đi ${m('8{,}0\\ \\mathrm m')}; ${m('\\mu=0{,}10')}; ${g10}.<br><b>a)</b> phản lực ${m('N')} và lực ma sát<br><b>b)</b> công lực đẩy<br><b>c)</b> công lực ma sát<br><b>d)</b> tổng công`, k: 8 },
  ]],
  dap: [
    `D1·1: a) quang năng và nhiệt năng · b) 6,0 J · c) 360 J &nbsp;|&nbsp; D1·2: a) 3,0 J · b) 6,75 J · c) 12 J &nbsp;|&nbsp; D2·1: a) 600 J · b) −600 J · c) 0 &nbsp;|&nbsp; D2·2: a) 1000 J · b) −700 J · c) 300 J, nhanh dần &nbsp;|&nbsp; D3·1: a) 433 J, phát động · b) 0, không sinh công · c) −433 J, công cản &nbsp;|&nbsp; D3·2: a) 1061 J · b) 1500 J · c) 60°`,
    `D4·1: a) 4,0 m · b) +200 J · c) −48 J &nbsp;|&nbsp; D4·2: a) −400 J · b) −300 J · c) +400 J; −300 J · d) 0 &nbsp;|&nbsp; D5·1: a) N = 160 N; ${nw('F<sub>ms</sub> = 40 N')} · b) 693 J · c) 0; 0; −400 J · d) 293 J &nbsp;|&nbsp; D5·2: a) N = 350 N; ${nw('F<sub>ms</sub> = 35 N')} · b) 693 J · c) −280 J · d) 413 J`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 2], kq: [[1, 2, 3], [4, 5]], khoNhat: false },
  tuongTu,
  tra: 'năng lượng 1·4 · bóng nảy 2·1 · công 2·2 · dấu của công 2·3 · trọng lực, ma sát 3·1 · mặt nghiêng 3·2 · bẫy 3·3 · bài toán mẫu 5·1 · dạng 1–3 → 6·1 · dạng 4–5 → 7·1',
  out: process.argv[2],
});
