// Ruột tập VL10 – Bài 9 · Chuyển động thẳng biến đổi đều (lesson id 54). Quyển Chương 2 lớp 10: bài 4 = tr. 1–12 → bài 9 = tr. 61–72.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l10-bai9.mjs (toàn bộ SVG tự vẽ). Nội dung theo bài web (book/cache/54.json, tải từ DB 13/11/2026):
// mục tiêu, dự đoán quãng phanh, II.1–II.4, thí nghiệm máng nghiêng, bảng quãng phanh, ba bẫy, Trả bài 6 câu,
// bài toán mẫu ô tô đuổi xe máy + điền bước phanh gấp, thử thách, 6 dạng bài tập mẫu.
// Đáp số Bài tương tự (tuongTu.dap) và mọi số điền tính bằng Python 13/11/2026.
// Chạy: node scripts/ruot-tap/l10-bai9.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl10-bai9.pdf
//       node scripts/ruot-tap/l10-bai9.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l10-bai9/ để soát chữ/nét
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai, dapSo } from './khung.mjs';
import { hinhL10b9 as H } from './hinh-l10-bai9.mjs';

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
  const out = resolve(HERE, 'out/hinh-l10-bai9'); mkdirSync(out, { recursive: true });
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


const K = khoiTao({ bai: 9, lid: 54, ten: 'CHUYỂN ĐỘNG THẲNG BIẾN ĐỔI ĐỀU', lop: 10, baiDau: 4, sub: 'Vật lí 10 · Chương 2: Động học' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const u = (s) => nw(m(s)); // số + đơn vị không gãy dòng
const v0 = m('v_0'), aa = m('a'), vv = m('v'), tt = m('t'), dd = m('d');

// Ô đáp số cuối dòng ý (yo/oo) và dòng giải 2 cột trong Bài tập mẫu — giữ như l10-bai23.mjs.
const ttHaiCot = '<style>.bt>.gi{display:grid;grid-template-columns:1fr 1fr;column-gap:4mm}.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm}.yo .oo{flex:none;display:flex;gap:3mm}.yo{line-height:1.35}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';
const p1 = `${ttHaiCot}<section class="page">
${head('BÀI 9 · CHUYỂN ĐỘNG THẲNG BIẾN ĐỔI ĐỀU', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Nhận ra <b>nhanh dần đều</b>, <b>chậm dần đều</b> qua dấu của ${aa} và ${vv}`)}
${dong(`${ck}Đọc <b>đồ thị ${vv}–${tt}</b>: độ dốc cho gia tốc, diện tích cho độ dịch chuyển`)}
${dong(`${ck}Dùng đúng ba công thức: vận tốc, độ dịch chuyển, công thức <b>không có thời gian</b>`)}
${dong(`${ck}Giải bài <b>hai xe gặp nhau</b> và bài <b>phanh gấp</b>`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Xe máy chạy ${u('36\\ \\mathrm{km/h}')}, phanh thì trượt thêm ${u('10\\ \\mathrm m')} rồi dừng. Hôm sau, cũng xe đó, cũng đường đó, chạy ${u('72\\ \\mathrm{km/h}')} và phanh y như cũ (cùng gia tốc). Xe trượt bao xa thì dừng?</p>
<div class="fig-side" style="${fs(50)}"><div>
${opt('A', `${u('20\\ \\mathrm m')}, vì tốc độ gấp đôi thì quãng phanh gấp đôi`)}
${opt('B', `${u('40\\ \\mathrm m')}, gấp bốn lần`)}
${opt('C', `${u('10\\ \\mathrm m')}, vì phanh như cũ`)}
${opt('D', `${u('30\\ \\mathrm m')}, vì xe nặng đà hơn một chút`)}
<div style="margin-top:1mm">${chon(12)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 2)}</div>
${H.phanh()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f(12)} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Gia tốc không đổi: nhanh dần đều, chậm dần đều', '1·4')}
<div class="card" style="padding:1.2mm 3mm">
<div><b>Chuyển động thẳng biến đổi đều:</b> quỹ đạo ${f(25)}, gia tốc ${f(25)} (cả độ lớn lẫn hướng).</div>
<div style="margin:.6mm 0">${m('a=\\dfrac{\\Delta v}{\\Delta t}=')} ${f(30)} &nbsp; đơn vị của ${aa}: ${f(14)}</div>
<div><b>Nhanh dần đều:</b> ${aa} ${f(25)} dấu ${vv}, tức ${m('a\\cdot v')} ${f(12)} 0</div>
<div><b>Chậm dần đều:</b> ${aa} ${f(25)} dấu ${vv}, tức ${m('a\\cdot v')} ${f(12)} 0</div>
<div style="margin-top:.8mm"><b>Ví dụ.</b> Người trượt băng thả trôi với ${u('6\\ \\mathrm{m/s}')}, mỗi giây chậm đi ${u('0{,}5\\ \\mathrm{m/s}')}. Chiều dương theo chiều trượt:</div>
<div>${nw(`${m('a=')} ${f(16)}`)} · nhanh hay chậm dần: ${f(25)} · dừng hẳn sau ${nw(`${m('t=')} ${f(12)} s`)}</div>
${lines(1)}</div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('CÔNG THỨC VẬN TỐC · ĐỒ THỊ v–t · ĐỘ DỊCH CHUYỂN')}
${h3(1, 'II.2 · Công thức vận tốc và đồ thị v–t', '2·1')}
<div class="card fig-side" style="${fs(52)};padding:1.2mm 3mm"><div>
<div>Gốc thời gian lúc bắt đầu xét (${m('t_0=0')}):</div>
<div style="margin:.6mm 0">${m('v=')} ${f(30)} &nbsp; từ nghỉ: ${m('v=')} ${f(14)}</div>
<div>Đồ thị ${vv}–${tt} là đoạn ${f(25)}, cắt trục ${vv} tại ${f(12)}.</div>
<div>Độ dốc ${m('=\\dfrac{\\Delta v}{\\Delta t}=')} ${f(12)}</div>
<div>Dốc lên: ${m('a')} ${f(12)} 0 · dốc xuống: ${m('a')} ${f(12)} 0</div>
<div>Nằm ngang: ${f(25)}</div>
<div style="margin-top:.6mm">Đọc tam giác trên đường A: ${nw(`${m('a_A=')} ${f(14)} m/s²`)}</div></div>
${H.vt3()}</div>
${h3(2, 'Thí nghiệm: đo vận tốc xe lăn trên máng nghiêng', '2·2')}
<div class="fig-side" style="${fs(46)}"><div>
<div class="hint" style="margin-bottom:.6mm">Tấm chắn rộng ${u('b=2{,}00\\ \\mathrm{cm}')}; đồng hồ chia ${u('0{,}001\\ \\mathrm s')}; ${m('v=b/\\tau')} (${m('\\tau')}: thời gian tấm chắn qua cổng).</div>
<table class="tbl-ct"><tr><th>${m('t\\ (\\mathrm s)')}</th><th>${m('v\\ (\\mathrm{m/s})')}</th><th>${m('v/t\\ (\\mathrm{m/s^2})')}</th></tr>
<tr><td>0,635</td><td>0,31</td><td></td></tr>
<tr><td>0,892</td><td>0,44</td><td></td></tr>
<tr><td>1,262</td><td>0,63</td><td></td></tr>
<tr><td>1,551</td><td>0,77</td><td></td></tr></table></div>
${H.mang()}</div>
<div class="card" style="margin-top:.6mm;padding:1mm 3mm">
<div><b>Rút ra:</b> ${m('v/t')} gần như ${f(25)} ⇒ ${m('v=')} ${f(12)}; ${nw(`${m('a\\approx')} ${f(14)} m/s²`)}</div>
${wl(`Hàng nào có ${vv} kém tin cậy nhất? Vì sao? <span class="hint" style="font-weight:400">(gợi ý: ${m('\\tau=b/v')})</span>`, 3)}</div>
${h3(3, 'II.3 · Độ dịch chuyển: diện tích dưới đồ thị v–t', '2·3')}
<div class="card fig-side" style="${fs(48)};padding:1.2mm 3mm"><div>
<div>Độ dịch chuyển = diện tích giữa ${f(25)} và trục ${tt}.</div>
<div style="margin:.5mm 0">Hình thang: ${m('d=')} ${f(25)} ${m('\\cdot\\, t')}</div>
<div style="margin:.5mm 0">${m('d=')} ${f(30)}</div>
<div>Hình bên: ${nw(`${m('d=')} ${f(12)} + ${f(12)} = ${f(12)} m`)}</div>
<div style="margin:.5mm 0"><b>Phương trình chuyển động:</b> ${m('x=')} ${f(30)}</div>
<div>Trước khi viết, chọn: gốc ${f(25)}, chiều ${f(25)}, gốc ${f(25)}</div>
<div>Không đổi chiều: quãng đường ${nw(`${m('s=')} ${f(12)}`)}</div></div>
${H.thang()}</div>
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('CÔNG THỨC KHÔNG CÓ THỜI GIAN · BẪY · TRẢ BÀI')}
${h3(1, 'II.4 · Công thức không có thời gian', '3·1')}
<div class="card" style="padding:1.2mm 3mm">
<div>Khử ${tt} giữa ${m('v=v_0+at')} và ${m('d=\\dfrac{v_0+v}{2}\\,t')}: &nbsp; ${f(40)} &nbsp; Dùng khi đề ${f(25)}</div>
<div style="margin-top:.6mm">Phanh tới dừng (${m('v=0')}): ${m('d=')} ${f(25)} &nbsp; ⇒ ${v0} gấp đôi thì ${dd} gấp ${f(12)}</div></div>
<div class="fig-side" style="${fs(58)}"><table class="tbl-ct">
<tr><th>Tốc độ lúc phanh</th><th style="width:26mm">Quãng phanh</th></tr>
<tr><td>${m('36\\ \\mathrm{km/h}=10\\ \\mathrm{m/s}')}</td><td>${m('10\\ \\mathrm m')}</td></tr>
<tr><td>${m('54\\ \\mathrm{km/h}=')} ${f(12)} m/s</td><td></td></tr>
<tr><td>${m('72\\ \\mathrm{km/h}=')} ${f(12)} m/s</td><td></td></tr>
<tr><td>${m('90\\ \\mathrm{km/h}=')} ${f(12)} m/s</td><td></td></tr></table>
<div class="card soft" style="padding:1mm 2.5mm;margin:0">Cùng gia tốc phanh ${u('5\\ \\mathrm{m/s^2}')} (đường khô, chưa tính lúc phản xạ). Đổi đơn vị: ${u('1\\ \\mathrm{m/s}=3{,}6\\ \\mathrm{km/h}')}, tức km/h chia 3,6 được m/s.</div></div>
${h3(2, 'III · Ba cái bẫy hay sập', '3·2')}
<div class="card fig-side" style="${fs(46)};padding:1mm 3mm"><div>
<div class="trap">${ck}<span><b>“${m('a')} âm là chậm dần.”</b> Dấu ${aa} chỉ cho biết ${m('\\vec a')} cùng hay ngược chiều dương. Nhanh hay chậm: xét dấu ${m('a\\cdot v')}.</span></div>
<div class="trap">${ck}<span><b>“Thay ngay ${tt} của đề.”</b> Xe phanh: tính lúc dừng ${nw(m('t_d=v_0/|a|'))} trước; ${m('t\\gt t_d')} thì ${nw(m('d=\\dfrac{v_0^2}{2|a|}'))}.</span></div>
<div class="trap">${ck}<span><b>“Hai đường ${vv}–${tt} cắt nhau là gặp nhau.”</b> Cắt nhau chỉ là cùng vận tốc; gặp nhau khi ${m('x_1=x_2')}.</span></div></div>
${H.bayDung()}</div>
${h3(3, 'IV · Trả bài 6 câu', '3·3')}
${box(`${tb('1. Biến đổi đều là gì? Nhận ra nhanh dần, chậm dần bằng cách nào?')}${lines(1)}
${tb('2. Công thức vận tốc? Khi nào chỉ còn v = at?')}${lines(1)}
${tb('3. Đồ thị v–t có dạng gì? Đọc a và d ở đâu?')}${lines(2)}
${tb('4. Công thức độ dịch chuyển, phương trình chuyển động? Khi nào s = d?')}${lines(1)}
${tb('5. Công thức không có t? Vì sao quãng phanh tăng nhanh theo tốc độ?')}${lines(2)}
${tb('6. Bài hai xe gặp nhau: lập phương trình thế nào, gặp nhau khi nào?')}${lines(1)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/6 câu · chưa thuộc: ${f(25)} ${nw(`→ đọc lại ô ${f(12)} Tập`)}</div>
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('TỰ KIỂM TRA · BÀI TOÁN MẪU')}
${h3(1, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '4·1')}
${rkHai([1, 2, 3], [4, 5, 6])}
${h3(2, 'V · Bài toán mẫu: ô tô đuổi xe máy', '4·2')}
<div class="card soft fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>Ô tô đang dừng ở vạch đèn đỏ. Đèn chuyển xanh, ô tô khởi hành nhanh dần đều với gia tốc ${u('2\\ \\mathrm{m/s^2}')}. Đúng lúc đó, một xe máy chạy thẳng đều ${u('10\\ \\mathrm{m/s}')} đi qua vạch dừng, cùng chiều với ô tô.
<div style="margin-top:.6mm">Sau bao lâu ô tô đuổi kịp xe máy, ở đâu, và lúc đó ô tô có vận tốc bao nhiêu?</div></div>${H.haiXe()}</div>
${h3(3, 'Phân tích đề')}
<table><tr><th style="width:52mm">Câu trong đề</th><th>Dữ liệu → kiến thức</th></tr>
<tr><td>“đang dừng … khởi hành”</td><td>${m('v_{01}=0')} → ${m('x_1=x_{01}+\\tfrac12 a_1t^2')}</td></tr>
<tr><td style="height:6.5mm">“đúng lúc đó … đi qua vạch dừng”</td><td></td></tr>
<tr><td style="height:6.5mm">“thẳng đều 10 m/s”</td><td></td></tr>
<tr><td style="height:6.5mm">“đuổi kịp, ở đâu”</td><td></td></tr>
<tr><td style="height:6.5mm">“vận tốc lúc đó”</td><td></td></tr></table>
${h3(4, 'Giải')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm;margin-top:1mm">
${wl('Chọn gốc toạ độ, chiều dương, gốc thời gian:', 1)}${wl(`Phương trình: ${m('x_1=')} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ${m('x_2=')}`, 1)}${wl(`Gặp nhau ${m('x_1=x_2')}:`, 2)}${wl('Vị trí và vận tốc ô tô:', 2)}${wl('Kiểm tra bằng vận tốc trung bình:', 1)}</div>
${h3(5, 'Điền bước còn thiếu: phanh gấp')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div style="padding-top:.8mm;line-height:1.35">Ô tô chạy ${u('72\\ \\mathrm{km/h}')} thấy vật cản cách ${u('50\\ \\mathrm m')}, phanh ngay, chậm dần đều với gia tốc độ lớn ${u('5\\ \\mathrm{m/s^2}')}. Xe có đâm vào vật cản không?</div>
<div class="ln"><b>Bước 1 (cho sẵn):</b> ${m('v_0=72\\ \\mathrm{km/h}=20\\ \\mathrm{m/s}')}</div>
${wl(`Bước 2: quãng phanh ${m('d=')}`, 1)}${wl('Bước 3: so với 50 m, kết luận:', 1)}</div>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TẬP VỀ NHÀ · THỬ THÁCH · MANG VỀ')}
${K.btvn()}
${h3(2, 'Thử thách phân tầng', '5·2')}
<div class="fig-side" style="${fs(44)}">${box(wl(`${m('\\bigstar')} Xe khởi hành từ nghỉ, ${u('a=2\\ \\mathrm{m/s^2}')}. Sau ${u('5\\ \\mathrm s')}: vận tốc và quãng đường?`, 3)
 + wl(`${m('\\bigstar\\bigstar')} Vật nhanh dần đều từ nghỉ, đi được ${u('5\\ \\mathrm m')} trong giây thứ ba (từ ${nw(m('t=2\\ \\mathrm s'))} đến ${nw(m('t=3\\ \\mathrm s'))}). Tìm ${aa}.`, 4)
 + wl(`${m('\\bigstar\\bigstar\\bigstar')} Ô tô chạy ${u('15\\ \\mathrm{m/s}')}; người lái mất ${u('0{,}8\\ \\mathrm s')} mới đạp phanh, rồi xe chậm dần đều với gia tốc độ lớn ${u('6\\ \\mathrm{m/s^2}')}. Tổng quãng đường từ lúc thấy vật cản tới lúc dừng?`, 5))}${H.phanXa()}</div>
${h3(3, 'Câu đổi chiều (bài toán mẫu)', '5·3')}
${box(wl(`Cùng lúc đèn xanh, xe máy ở cách vạch dừng ${u('75\\ \\mathrm m')} phía trước, chạy đều ${u('10\\ \\mathrm{m/s}')} <b>về phía</b> ô tô. Giữ chiều dương như cũ: viết ${m('x_2')}, tìm lúc và chỗ hai xe gặp nhau.`, 5))}
${h3(4, 'VI · Mang về: điều em dễ quên nhất', '5·4')}
${box(wl('1.', 3) + wl('2.', 3) + wl('3.', 3))}
${foot(5)}</section>`;

// Hình cạnh đề (không cạnh ô giải) để ô giải dùng 2 cột dòng kẻ — tiết kiệm chiều cao trang 7.
const deH = (txt, fig, w = 38) => `<div class="fig-side" style="grid-template-columns:1fr ${w}mm;margin:0"><div>${txt}</div>${fig()}</div>`;
const dang = [
  { t: 'Dạng 1 · Dễ · Tăng tốc đều: tìm vận tốc và quãng đường',
    de: `Đoàn tàu đang chạy ${u('20\\ \\mathrm{m/s}')} thì tăng tốc đều với gia tốc ${u('0{,}5\\ \\mathrm{m/s^2}')} trong ${nw(`${m('30\\ \\mathrm s')}.`)}<br><b>a)</b> vận tốc của tàu sau ${m('30\\ \\mathrm s')}<br><b>b)</b> quãng đường tàu đi được trong thời gian đó`,
    nd: `chiều dương theo chiều chạy ⇒ ${aa} ${f(12)} 0; tàu không đổi chiều ⇒ ${nw(`${m('s=')} ${f(12)}`)}`, a: ['a', 'b'], gi: 3 },
  { t: 'Dạng 2 · Dễ · Đọc đồ thị v–t: gia tốc và quãng đường',
    de: `Xe chạy thẳng một chiều, đồ thị ${vv}–${tt} như hình bên.<br><b>a)</b> gia tốc ở từng giai đoạn ${m('a_1, a_2, a_3')}; xe nhanh dần, chậm dần hay đều<br><b>b)</b> quãng đường xe đi được trong ${m('14\\ \\mathrm s')}`,
    nd: `${aa} = độ ${f(25)}; quãng đường = ${f(25)} dưới đồ thị`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'a<sub>3</sub>', 'b'], gi: 5, fig: H.d2, cot: 2 },
  { t: 'Dạng 3 · Trung bình · Phanh tới dừng',
    de: `Xe máy chạy ${u('54\\ \\mathrm{km/h}')} thì phanh gấp, dừng lại sau vết phanh dài ${nw(`${m('37{,}5\\ \\mathrm m')}.`)} Coi là chậm dần đều.<br><b>a)</b> gia tốc và thời gian phanh<br><b>b)</b> vận tốc sau ${m('2\\ \\mathrm s')} kể từ lúc phanh<br><b>c)</b> quãng đường đi được trong ${m('7\\ \\mathrm s')} kể từ lúc phanh`,
    nd: `không cho, không hỏi ${tt} ⇒ dùng ${f(30)}; ${m('7\\ \\mathrm s')} so với lúc dừng ${m('t_d')} trước`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'], gi: 4 },
  { t: 'Dạng 4 · Trung bình · Quãng đường trong giây thứ n',
    de: `Vật nhanh dần đều, vận tốc ban đầu ${nw(`${m('3\\ \\mathrm{m/s}')}.`)} Trong giây thứ 5 (tính từ lúc bắt đầu) vật đi được ${nw(`${m('12\\ \\mathrm m')}.`)}<br><b>a)</b> gia tốc của vật<br><b>b)</b> quãng đường vật đi được trong giây thứ 8`,
    nd: `giây thứ ${m('n')} là từ ${nw(`${m('t=')} ${f(14)}`)} đến ${nw(`${m('t=')} ${f(12)}`)}; ${m('\\Delta s_n=s_n-')} ${f(12)}`, a: ['a', 'b'], gi: 4 },
  { t: 'Dạng 5 · Khó · Hai giai đoạn: dốc rồi mặt ngang',
    de: deH(`Quả cầu lăn từ nghỉ ở đỉnh A của dốc dài ${m('64\\ \\mathrm m')}, tới chân dốc B sau ${nw(`${m('8\\ \\mathrm s')}.`)} Sau đó lăn tiếp trên mặt ngang thêm ${m('32\\ \\mathrm m')} (B → C) thì dừng. Mỗi giai đoạn biến đổi đều.<br><b>a)</b> gia tốc trên dốc và vận tốc tại B<br><b>b)</b> gia tốc và thời gian lăn trên BC<br><b>c)</b> vận tốc trung bình trên cả hành trình AC`, H.d5),
    nd: `${m('v_B')}: vận tốc ${f(25)} của giai đoạn 1, vận tốc ${f(25)} của giai đoạn 2; ${m('v_{tb}=')} tổng đường : ${f(25)}`, a: ['a', 'b', 'c'], gi: 4 },
  { t: 'Dạng 6 · Khó · Hai xe ngược chiều trên dốc: lúc và nơi gặp nhau',
    de: deH(`Ô tô qua chân dốc với ${u('20\\ \\mathrm{m/s}')}, lên dốc chậm dần đều, ${nw(`${m('|a_1|=0{,}4\\ \\mathrm{m/s^2}')}.`)} Cùng lúc, xe đạp ở đỉnh dốc có ${u('2\\ \\mathrm{m/s}')}, xuống dốc nhanh dần đều, ${nw(`${m('|a_2|=0{,}2\\ \\mathrm{m/s^2}')}.`)} Dốc dài ${nw(`${m('570\\ \\mathrm m')}.`)} Gốc toạ độ ở chân dốc, <b>chiều dương từ chân lên đỉnh dốc</b> (chiều chuyển động của ô tô).<br><b>a)</b> sau bao lâu hai xe gặp nhau; chỗ gặp cách chân dốc bao xa<br><b>b)</b> vận tốc của mỗi xe lúc gặp nhau`, H.d6, 40),
    nd: `cả hai xe cùng hệ quy chiếu đã chọn; xe đạp: ${nw(`${m('v_{02}=')} ${f(12)}`)}, ${nw(`${m('a_2=')} ${f(12)}`)}; loại nghiệm khi ô tô đã ${f(25)}`, a: ['a', 'b'], gi: 4, cot: 2 },
];

// Bài tương tự giải vào vở (thầy chốt 10/11): 1 cột; ô đáp số 25 mm đặt cuối đúng dòng của ý, nhãn ô khớp a) b) c)…
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
  tieuDe: ['DẠNG 1–3', 'DẠNG 4–6'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Ô tô đang chạy ${u('10\\ \\mathrm{m/s}')} thì tăng tốc đều với gia tốc ${u('1{,}5\\ \\mathrm{m/s^2}')} trong ${nw(`${m('8\\ \\mathrm s')}.`)}<br><b>a)</b> vận tốc sau ${m('8\\ \\mathrm s')}<br><b>b)</b> quãng đường đi được trong ${m('8\\ \\mathrm s')} đó`, o: ['a', 'b'] },
    { t: 'Dạng 1 · Bài 2', de: `Xe máy khởi hành từ nghỉ, nhanh dần đều, sau ${m('10\\ \\mathrm s')} đạt ${u('54\\ \\mathrm{km/h}')} (${u('1\\ \\mathrm{m/s}=3{,}6\\ \\mathrm{km/h}')}).<br><b>a)</b> gia tốc của xe<br><b>b)</b> quãng đường đi được trong ${m('10\\ \\mathrm s')}<br><b>c)</b> vận tốc sau ${m('4\\ \\mathrm s')}`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 2 · Bài 1', de: `Thang máy đi lên: từ nghỉ tăng đều tới ${u('3\\ \\mathrm{m/s}')} trong ${nw(`${m('2\\ \\mathrm s')},`)} giữ ${u('3\\ \\mathrm{m/s}')} tới ${nw(`${m('t=10\\ \\mathrm s')},`)} rồi giảm đều, dừng lúc ${nw(`${m('t=13\\ \\mathrm s')}.`)}<br><b>a)</b> gia tốc ba giai đoạn ${m('a_1, a_2, a_3')}<br><b>b)</b> thang đi lên được bao cao`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'a<sub>3</sub>', 'b'], ow: 18 },
    { t: 'Dạng 2 · Bài 2', de: `Xe chạy thẳng một chiều: lúc ${m('t=0')} có ${nw(`${m('v=10\\ \\mathrm{m/s}')},`)} giảm đều tới ${u('4\\ \\mathrm{m/s}')} lúc ${nw(`${m('t=3\\ \\mathrm s')},`)} rồi tăng đều tới ${u('12\\ \\mathrm{m/s}')} lúc ${nw(`${m('t=7\\ \\mathrm s')}.`)}<br><b>a)</b> gia tốc hai giai đoạn ${m('a_1, a_2')}; mỗi giai đoạn nhanh hay chậm dần<br><b>b)</b> quãng đường trong ${m('7\\ \\mathrm s')}`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b'] },
    { t: 'Dạng 3 · Bài 1', de: `Ô tô chạy ${u('72\\ \\mathrm{km/h}')} thì phanh, chậm dần đều, đi thêm ${u('50\\ \\mathrm m')} thì dừng.<br><b>a)</b> gia tốc của xe<br><b>b)</b> thời gian phanh<br><b>c)</b> quãng đường đi được trong ${m('6\\ \\mathrm s')} kể từ lúc phanh`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 3 · Bài 2', de: `Tàu chạy ${u('36\\ \\mathrm{km/h}')} thì hãm phanh, chậm dần đều với gia tốc độ lớn ${nw(`${m('0{,}5\\ \\mathrm{m/s^2}')}.`)}<br><b>a)</b> thời gian và quãng đường từ lúc hãm tới lúc dừng<br><b>b)</b> vận tốc sau ${m('10\\ \\mathrm s')}<br><b>c)</b> quãng đường đi được trong ${m('30\\ \\mathrm s')} kể từ lúc hãm`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'], ow: 18 },
    nhap(3),
  ], [
    { t: 'Dạng 4 · Bài 1', de: `Vật nhanh dần đều từ nghỉ với gia tốc ${nw(`${m('4\\ \\mathrm{m/s^2}')}.`)}<br><b>a)</b> quãng đường đi được trong ${m('3\\ \\mathrm s')} đầu<br><b>b)</b> quãng đường đi được trong giây thứ 3`, o: ['a', 'b'] },
    { t: 'Dạng 4 · Bài 2', de: `Vật nhanh dần đều, vận tốc ban đầu ${nw(`${m('2\\ \\mathrm{m/s}')}.`)} Trong giây thứ 4 vật đi được ${nw(`${m('9\\ \\mathrm m')}.`)}<br><b>a)</b> gia tốc của vật<br><b>b)</b> quãng đường đi được trong giây thứ 6`, o: ['a', 'b'] },
    { t: 'Dạng 5 · Bài 1', de: `Xe khởi hành từ nghỉ, nhanh dần đều, sau ${m('20\\ \\mathrm s')} đạt ${nw(`${m('10\\ \\mathrm{m/s}')};`)} rồi phanh, chậm dần đều thêm ${m('25\\ \\mathrm m')} thì dừng.<br><b>a)</b> gia tốc và quãng đường giai đoạn đầu<br><b>b)</b> gia tốc và thời gian phanh<br><b>c)</b> tốc độ trung bình cả hành trình`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'], ow: 18 },
    { t: 'Dạng 5 · Bài 2', de: `Quả cầu lăn từ nghỉ xuống dốc dài ${m('25\\ \\mathrm m')} với gia tốc ${nw(`${m('2\\ \\mathrm{m/s^2}')},`)} rồi lăn trên mặt ngang chậm dần đều, sau ${m('4\\ \\mathrm s')} thì dừng.<br><b>a)</b> vận tốc ở chân dốc và thời gian xuống dốc<br><b>b)</b> gia tốc và quãng đường trên mặt ngang`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>'], ow: 18 },
    { t: 'Dạng 6 · Bài 1', de: `Hai xe ở A và B cách nhau ${nw(`${m('200\\ \\mathrm m')},`)} cùng lúc chạy về phía nhau: xe từ A khởi hành từ nghỉ, nhanh dần đều ${nw(`${m('2\\ \\mathrm{m/s^2}')};`)} xe từ B chạy đều ${nw(`${m('10\\ \\mathrm{m/s}')}.`)}<br><b>a)</b> thời điểm gặp nhau<br><b>b)</b> chỗ gặp cách A bao xa<br><b>c)</b> vận tốc xe từ A lúc gặp`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 6 · Bài 2', de: `Ô tô qua chân dốc với ${nw(`${m('12\\ \\mathrm{m/s}')},`)} lên dốc chậm dần đều, gia tốc độ lớn ${nw(`${m('0{,}2\\ \\mathrm{m/s^2}')}.`)} Cùng lúc, xe đạp ở đỉnh dốc có ${u('1\\ \\mathrm{m/s}')} xuống dốc nhanh dần đều, gia tốc độ lớn ${nw(`${m('0{,}2\\ \\mathrm{m/s^2}')}.`)} Dốc dài ${nw(`${m('390\\ \\mathrm m')}.`)}<br><b>a)</b> thời điểm gặp nhau<br><b>b)</b> chỗ gặp cách chân dốc<br><b>c)</b> tốc độ ô tô, tốc độ xe đạp lúc gặp`, o: ['a', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'], ow: 18 },
    nhap(2),
  ]],
  dap: [
    `D1·1: a) 22 m/s · b) 128 m &nbsp;|&nbsp; D1·2: a) 1,5 m/s² · b) 75 m · c) 6 m/s &nbsp;|&nbsp; D2·1: a<sub>1</sub>) 1,5 m/s² · a<sub>2</sub>) 0 · a<sub>3</sub>) −1 m/s² · b) 31,5 m &nbsp;|&nbsp; D2·2: a<sub>1</sub>) −2 m/s², chậm dần · a<sub>2</sub>) +2 m/s², nhanh dần · b) 53 m &nbsp;|&nbsp; D3·1: a) −4 m/s² · b) 5 s · c) 50 m (xe dừng lúc 5 s) &nbsp;|&nbsp; D3·2: a<sub>1</sub>) 20 s · a<sub>2</sub>) 100 m · b) 5 m/s · c) 100 m`,
    `D4·1: a) 18 m · b) 10 m &nbsp;|&nbsp; D4·2: a) 2 m/s² · b) 13 m &nbsp;|&nbsp; D5·1: a<sub>1</sub>) 0,5 m/s² · a<sub>2</sub>) 100 m · b<sub>1</sub>) −2 m/s² · b<sub>2</sub>) 5 s · c) 5 m/s &nbsp;|&nbsp; D5·2: a<sub>1</sub>) 10 m/s · a<sub>2</sub>) 5 s · b<sub>1</sub>) −2,5 m/s² · b<sub>2</sub>) 20 m &nbsp;|&nbsp; D6·1: a) 10 s · b) 100 m · c) 20 m/s &nbsp;|&nbsp; D6·2: a) 30 s · b) 270 m · c<sub>1</sub>) 6 m/s · c<sub>2</sub>) 7 m/s`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 3], kq: [[1, 2, 3], [4, 5, 6]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'nhanh/chậm dần 1·4 · công thức v, đồ thị v–t 2·1 · thí nghiệm 2·2 · độ dịch chuyển 2·3 · không có t 3·1 · bẫy 3·2 · bài toán mẫu 4·2 · dạng 1–3 → 6·1 · dạng 4–6 → 7·1',
  out: process.argv[2],
});
