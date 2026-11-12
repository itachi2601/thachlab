// Ruột tập VL10 – Bài 30 · Thực hành: xác định động lượng của vật trước và sau va chạm (lesson id 75). Quyển Chương 5 lớp 10: bài 30 = tr. 25–36.
// Khung: khung.mjs (bố cục bài 14: 1–5 học · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Bài THỰC HÀNH: tr.1 dụng cụ + dự đoán · tr.2 sơ đồ bố trí + các bước · tr.3 bảng số liệu TN1 + xử lí sai số · tr.4 TN2 · tr.5 báo cáo, bẫy, trả bài, BTVN.
// Nội dung theo bài web (book/cache/75.json, tải 12/11/2026); 4 dạng bài tập mẫu của web; đáp số Bài tương tự tính bằng Python 12/11/2026.
// Hình: hinh-l10-bai30.mjs (SVG tự vẽ). Không dùng ảnh Halliday.
// Chạy: node scripts/ruot-tap/l10-bai30.mjs [file.pdf]       → scripts/ruot-tap/out/ruot-tap-vl10-bai30.pdf
//       node scripts/ruot-tap/l10-bai30.mjs --hinh           → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l10-bai30/ để soát chữ/nét
import { khoiTao, m, lines, wl as wl0, fill as f, nw, ck, box, opt, chon } from './khung.mjs';
import { hinhL10b30 as H } from './hinh-l10-bai30.mjs';

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
  const out = resolve(HERE, 'out/hinh-l10-bai30'); mkdirSync(out, { recursive: true });
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

const K = khoiTao({ bai: 30, lid: 75, lop: 10, baiDau: 28, ten: 'THỰC HÀNH: ĐỘNG LƯỢNG TRƯỚC VÀ SAU VA CHẠM', sub: 'Vật lí 10 · Chương 5: Động lượng' });
const { head, foot } = K;
// Chữ Hi Lạp và dấu ′ trong văn bản thường rơi về Helvetica (Source Sans chỉ nạp latin/vietnamese) → đổi sang KaTeX.
const G = (s) => s.replace(/Δp′/g, m('\\Delta p\\prime')).replace(/p₁′/g, m('p_1\\prime')).replace(/p₂′/g, m('p_2\\prime'))
  .replace(/p′/g, m('p\\prime')).replace(/δ/g, m('\\delta')).replace(/ε/g, m('\\varepsilon'));
const h3 = (i, t, tg) => K.h3(i, G(t), tg);
const wl = (l, n) => wl0(G(l), n);
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const tb = (s) => `<div><b>${G(s)}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const g98 = nw(m('g=9{,}8\\ \\mathrm{m/s^2}'));
const v1 = (s = '') => m(`v_1${s}`), p_ = (s) => m(s);
// Bảng ghi số liệu: cols = tiêu đề; rows = [nhãn dòng, [giá trị cho sẵn hoặc '']…]; hàng 'Mẫu' in nghiêng xám. Ô trống cao h mm.
const bang = (cols, mau, nRow = 3, h = 7.5, w0 = 13) => {
  const th = cols.map((c, i) => `<th${i === 0 ? ` style="width:${w0}mm"` : ''} style="text-align:center">${c}</th>`).join('');
  const rowMau = `<tr style="color:var(--hint);font-style:italic"><td style="text-align:center;height:${h}mm">Mẫu</td>${mau.map((c) => `<td style="text-align:center">${c}</td>`).join('')}</tr>`;
  const rows = Array.from({ length: nRow }, (_, i) => `<tr><td style="text-align:center;height:${h}mm"><b>${i + 1}</b></td>${mau.map(() => '<td></td>').join('')}</tr>`).join('');
  return `<table class="bsl"><tr>${th}</tr>${rowMau}${rows}</table>`;
};
const bslCss = '<style>.bsl th{text-align:center;padding:.5mm .8mm;font-size:var(--fs-sm);line-height:1.25;vertical-align:middle}.bsl td{padding:.3mm .8mm;font-size:var(--fs-sm)}</style>';

const p1 = `${bslCss}<section class="page">
${head('BÀI 30 · THỰC HÀNH · ĐỘNG LƯỢNG TRƯỚC VÀ SAU VA CHẠM', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Đo tốc độ xe bằng <b>cổng quang</b>: ${m('v=\\dfrac{s}{t}')}, rồi tính động lượng ${m('p=mv')} <b>có dấu</b>`)}
${dong(`${ck}Làm hai phép đo: <b>va chạm mềm</b> (hai xe dính nhau) và <b>hai xe đẩy nhau</b> (lò xo ở giữa)`)}
${dong(`${ck}So tổng động lượng <b>trước và sau</b>, kết luận có xét <b>sai số</b>`)}
${dong(`${ck}Giải thích vì sao ${m('p\\prime')} lệch ${m('p')} vài phần trăm khi hệ <b>không kín hoàn toàn</b>`)}
</div>
${h3(2, 'Dự đoán trước khi làm', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Cắt dây. Điều gì xảy ra với hai xe? <span class="hint">(xe 2 nặng gấp đôi xe 1)</span></p>
<div class="fig-side" style="${fs(52)}"><div>
${opt('A', 'Hai xe chạy nhanh bằng nhau, vì lực lò xo lên hai xe bằng nhau')}
${opt('B', 'Xe 2 nặng hơn nên chạy nhanh hơn, vì có nhiều “đà” hơn')}
${opt('C', 'Xe 1 chạy nhanh gấp đôi xe 2, hai xe đi ngược chiều')}
${opt('D', 'Hai xe vẫn đứng yên, vì hai lực triệt tiêu nhau')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 1)}</div>
${H.dudoan()}</div>
</div>
${h3(3, 'Làm xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'Dụng cụ và số cho sẵn', '1·4')}
<table><tr><th style="width:42mm">Dụng cụ</th><th>Dùng để</th><th style="width:44mm">Số cho sẵn</th></tr>
<tr><td>Băng đệm khí + bơm</td><td>xe lướt trên lớp khí, ma sát rất nhỏ</td><td>—</td></tr>
<tr><td>Cổng quang + đồng hồ</td><td>đo thời gian ${m('t')} chắn tia sáng</td><td>${m('\\Delta t=0{,}001\\ \\mathrm s')}</td></tr>
<tr><td>Tấm cản quang</td><td>bề rộng ${m('s')} (đo bằng thước kẹp)</td><td>${nw(m('s=5{,}00\\ \\mathrm{cm}=0{,}0500\\ \\mathrm m'))}</td></tr>
<tr><td>Cân điện tử</td><td>đo khối lượng ${m('m')} từng xe</td><td>${m('\\Delta m=0{,}001\\ \\mathrm{kg}')} mỗi lần cân</td></tr>
<tr><td>Chốt ghim + sáp · lò xo</td><td>hai xe dính nhau · hai xe đẩy nhau</td><td>—</td></tr></table>
<div class="hint" style="margin-top:.8mm">Cân hai xe là hai lần cân, nên với ${m('p\\prime')} sau va chạm mềm thì ${m('\\Delta m=0{,}002\\ \\mathrm{kg}')}. Mọi tính toán trong tập dùng đúng các số này.</div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('Ý TƯỞNG ĐO · THÍ NGHIỆM 1: VA CHẠM MỀM')}
${h3(1, 'Đo t, tính v, tính p', '2·1')}
<div class="card" style="padding:1.2mm 3mm">
<div>Bề rộng ${m('s')}, thời gian chắn ${m('t')}: ${nw(`${m('v=')} ${f(12)} ${m('/')} ${f(12)}`)} &nbsp;· ${nw(`đổi ${m('5{,}00\\ \\mathrm{cm}=')} ${f(14)}&nbsp;m`)}</div>
<div>Động lượng: ${nw(`${m('p=')} ${f(12)} ${m('\\cdot')} ${f(12)}`)}; xe ngược chiều dương thì ${m('p')} mang dấu ${f(12)}</div>
<div>Đồng hồ chỉ ${m('t\\gt0')} nên ${m('v\\gt0')}: dấu của ${m('p')} do em ${f(25)} sau khi chọn chiều dương.</div></div>
${h3(2, 'Thí nghiệm 1 · bố trí', '2·2')}
<div class="fig-side" style="${fs(62)}"><div style="padding-top:1mm">
<div class="trap" style="margin:.3mm 0">${ck}<span>Băng nằm ngang: xe đặt đứng yên giữa băng không trôi</span></div>
<div class="trap" style="margin:.3mm 0">${ck}<span>Tấm cản quang song song với băng</span></div>
<div class="trap" style="margin:.3mm 0">${ck}<span>Bơm khí chạy; đồng hồ ở chế độ “vật chắn cổng”, nhấn reset về ${m('0{,}000')}</span></div>
<div class="trap" style="margin:.3mm 0">${ck}<span>Cân ${m('m_1')}, ${m('m_2')}, ghi vào Bảng 1 (tr. ${3 + 24})</span></div>
<div class="trap" style="margin:.3mm 0">${ck}<span>Xe 2 đứng yên giữa hai cổng; xe 1 ở ngoài cổng 1</span></div></div>
${H.boTri1()}</div>
${h3(3, 'Cách đo', '2·3')}
<div class="card" style="padding:1.2mm 3mm">
<div><b>1.</b> Đẩy xe 1 tới va vào xe 2; hai xe dính nhau (chốt ghim + sáp) rồi chạy qua cổng 2.</div>
<div><b>2.</b> Đọc ${m('t_1')} (xe 1 qua cổng 1) và ${m('t_1\\prime')} (cặp xe qua cổng 2): lấy số đo lần xe chắn cổng <b>đầu tiên</b>.</div>
<div><b>3.</b> Làm 3 lần; mỗi lần gắn thêm gia trọng lên xe 1 hoặc xe 2.</div>
<div style="margin-top:1mm">Trước va chạm xe 2 đứng yên: ${m('p=')} ${f(12)} ${m('\\cdot v_1')}. Sau va chạm hai xe dính nhau: ${nw(`${m('p\\prime=(')} ${f(14)} ${m(')\\,v\\prime')}`)}.</div>
${wl('Vì sao chỉ lấy số đo lần xe chắn cổng đầu tiên?', 2)}</div>
${h3(4, 'Làm nhanh', '2·4')}
${box(cau(`<b>Câu 1.</b> Lần 3: ${m('m_1=0{,}405\\ \\mathrm{kg}')}, ${m('t_1=0{,}105\\ \\mathrm s')} (tấm cản quang ${m('5{,}00\\ \\mathrm{cm}')}). Động lượng ${m('p')} trước va chạm?`, 2)
 + cau(`<b>Câu 2.</b> Va chạm mềm: ${m('m_1=0{,}205\\ \\mathrm{kg}')}, ${m('m_2=0{,}398\\ \\mathrm{kg}')}; sau va chạm hai xe dính nhau qua cổng 2 với ${m('v\\prime=0{,}170\\ \\mathrm{m/s}')}. Động lượng ${m('p\\prime')}?`, 1)
 + cau(`<b>Câu 3.</b> Hai xe đẩy nhau: xe 1 (${m('0{,}250\\ \\mathrm{kg}')}) sang trái ${m('0{,}400\\ \\mathrm{m/s}')}, xe 2 (${m('0{,}500\\ \\mathrm{kg}')}) sang phải ${m('0{,}205\\ \\mathrm{m/s}')}. Chọn chiều dương sang trái: tổng động lượng sau?`, 2))}
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('THÍ NGHIỆM 1 · SỐ LIỆU VÀ XỬ LÍ SAI SỐ')}
${h3(1, 'Bảng 1 · số đo (ghi ngay khi đo)', '3·1')}
${bang(['Lần', `${m('m_1')} (kg)`, `${m('m_2')} (kg)`, `${m('t_1')} (s)`, `${m('t_1\\prime')} (s)`], ['0,205', '0,198', '0,099', '0,199'], 3, 9)}
${h3(2, 'Bảng 2 · tính p, p′, δ và ε', '3·2')}
${bang(['Lần', `${m('v_1')} (m/s)`, `${m('p')} (kg·m/s)`, `${m('v\\prime')} (m/s)`, `${m('p\\prime')} (kg·m/s)`, `${m('\\delta')} (%)`, `${m('\\varepsilon')} (%)`], ['0,505', '0,1035', '0,251', '0,1013', '2,2', '2,5'], 3, 11)}
<div class="hint" style="margin-top:.6mm">Dòng Mẫu: số liệu minh hoạ lần làm trước, để đối chiếu cách tính.</div>
${h3(3, 'Công thức xử lí (cho sẵn)', '3·3')}
<div class="card soft" style="padding:1.2mm 3mm">
<div>Độ lệch: ${m('\\delta=\\dfrac{|p\\prime-p|}{p}')} &nbsp;·&nbsp; sai số một động lượng: ${m('\\dfrac{\\Delta p}{p}=\\dfrac{\\Delta m}{m}+\\dfrac{\\Delta t}{t}')}</div>
<div>Sai số gộp: ${m('\\varepsilon=\\dfrac{\\Delta p}{p}+\\dfrac{\\Delta p\\prime}{p\\prime}')} &nbsp;·&nbsp; <b>Kết luận:</b> ${m('\\delta\\le\\varepsilon')} thì bảo toàn trong sai số</div>
<div class="hint">${m('\\Delta m=0{,}001\\ \\mathrm{kg}')} cho ${m('p')} (cân xe 1), ${m('0{,}002\\ \\mathrm{kg}')} cho ${m('p\\prime')} (cân hai xe); ${m('\\Delta t=0{,}001\\ \\mathrm s')}; không cộng sai số của ${m('s')} vì cùng một tấm cản quang cho ${m('p')} và ${m('p\\prime')}.</div></div>
${h3(4, 'Tính chi tiết ε (lần 1) và kết luận', '3·4')}
<div class="card" style="padding:1.2mm 3mm">
<div>${m('\\dfrac{\\Delta p}{p}=')} ${f(16)} &nbsp;·&nbsp; ${m('\\dfrac{\\Delta p\\prime}{p\\prime}=')} ${f(16)} &nbsp;·&nbsp; ${m('\\varepsilon=')} ${f(16)}</div>
<div style="margin-top:1mm">Số lần có ${m('\\delta\\le\\varepsilon')}: ${f(10)} / 3 &nbsp;· Động lượng bảo toàn trong sai số? ${ck}có &nbsp;${ck}không</div>
${wl('Một lần có δ > ε thì em làm gì trước tiên, vì sao chưa kết luận “định luật sai”?', 2)}
${wl('Giá trị trung bình của δ ba lần:', 1)}</div>
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('THÍ NGHIỆM 2: HAI XE ĐẨY NHAU')}
${h3(1, 'Bố trí và cách đo', '4·1')}
<div class="fig-side" style="${fs(62)}"><div style="padding-top:1mm">
<div><b>Làm:</b> gắn lò xo vào một xe, nén lại, buộc hai xe bằng dây. Cắt dây.</div>
<div>Đọc ${m('t_1\\prime')} (xe 1 qua cổng 1) và ${m('t_2\\prime')} (xe 2 qua cổng 2). Đổi gia trọng, làm 3 lần.</div>
<div style="margin-top:1mm">Trước khi cắt dây hai xe đứng yên: ${m('p=')} ${f(12)}</div>
<div>Chiều dương sang phải <span class="hint">(ghi + hoặc −)</span>:</div>
<div>${nw(`${m('p_1\\prime=')} ${f(8)} ${m('m_1v_1\\prime')}`)} &nbsp;·&nbsp; ${nw(`${m('p_2\\prime=')} ${f(8)} ${m('m_2v_2\\prime')}`)}</div></div>
${H.boTri2()}</div>
${h3(2, 'Bảng 3 · số đo', '4·2')}
${bang(['Lần', `${m('m_1')} (kg)`, `${m('m_2')} (kg)`, `${m('t_1\\prime')} (s)`, `${m('t_2\\prime')} (s)`], ['0,205', '0,198', '0,205', '0,195'])}
${h3(3, 'Bảng 4 · tính p₁′, p₂′, p′ và Δp′', '4·3')}
${bang(['Lần', `${m('p_1\\prime')} (kg·m/s)`, `${m('p_2\\prime')} (kg·m/s)`, `${m('p\\prime=p_1\\prime+p_2\\prime')}`, `${m('\\Delta p\\prime')} (kg·m/s)`, `${m('|p\\prime|\\le\\Delta p\\prime')}?`], ['−0,0500', '+0,0508', '+0,0008', '0,0010', 'có'], 3, 9)}
<div class="hint" style="margin-top:.6mm">Dòng Mẫu: số liệu minh hoạ, ${m('v')} lấy từ ${m('s=0{,}0500\\ \\mathrm m')}.</div>
${h3(4, 'Công thức và kết luận', '4·4')}
<div class="card soft" style="padding:1.2mm 3mm">
<div>${m('\\Delta p_i\\prime=|p_i\\prime|\\left(\\dfrac{\\Delta m}{m_i}+\\dfrac{\\Delta t}{t_i\\prime}\\right)')} &nbsp;·&nbsp; ${m('\\Delta p\\prime=\\Delta p_1\\prime+\\Delta p_2\\prime')} &nbsp;(${nw(`${m('\\Delta m=0{,}001\\ \\mathrm{kg}')},`)} ${m('\\Delta t=0{,}001\\ \\mathrm s')})</div></div>
<div class="card" style="padding:1.2mm 3mm">
<div>Trước đó ${m('p=0')} nên không chia được cho ${f(12)} để tính ${m('\\delta')}; ta so ${m('|p\\prime|')} với ${f(14)}.</div>
<div>Số lần có ${m('|p\\prime|\\le\\Delta p\\prime')}: ${f(10)} / 3 &nbsp;· Bảo toàn trong sai số? ${ck}có &nbsp;${ck}không</div>
${wl('Hai xe cùng khối lượng thì hai động lượng sau có độ lớn thế nào, hai tốc độ ra sao?', 2)}</div>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÁO CÁO · BẪY · TRẢ BÀI')}
${h3(1, 'Vẽ kết quả thí nghiệm 1', '5·1')}
<div class="fig-side" style="${fs(62)}"><div style="padding-top:1mm">
<div>Chấm ${m('p\\prime/p')} ba lần, vẽ thanh ± ${m('\\varepsilon')} (lấy ${m('\\varepsilon')} ở Bảng 2).</div>
<div style="margin-top:1mm">Ba độ lệch: ${nw(`${ck}cùng phía`)} ${nw(`${ck}xen kẽ`)}</div>
<div>Cùng phía gợi ý sai số: ${nw(`${ck}hệ thống`)} ${nw(`${ck}ngẫu nhiên`)}</div>
${wl('Nguyên nhân có thể:', 2)}</div>
${H.luoiSS()}</div>
${h3(2, 'Ba cái bẫy', '5·2')}
<div class="card" style="padding:1mm 3mm">
<div class="trap">${ck}<span><b>“Quên dấu.”</b> Đồng hồ cho ${m('t\\gt0')}: chọn chiều dương trước, xe đi ngược chiều dương thì ${m('p\\lt0')}.</span></div>
<div class="trap">${ck}<span><b>“Sau va chạm mềm chỉ tính một xe.”</b> Hai xe dính nhau: cộng khối lượng ${m('m_1+m_2')}.</span></div>
<div class="trap">${ck}<span><b>“${m('p\\prime')} khác ${m('p')} là thí nghiệm hỏng.”</b> So ${m('\\delta')} với ${m('\\varepsilon')}; ma sát khí, băng nghiêng làm lệch vài %.</span></div></div>
${h3(3, 'Trả bài 6 câu', '5·3')}
${box(`${tb('1. Đo tốc độ xe bằng cổng quang thế nào?')}${lines(1)}
${tb('2. Động lượng của xe tính thế nào, dấu ra sao?')}${lines(1)}
${tb('3. Va chạm mềm: đo gì, tính p và p′ thế nào?')}${lines(2)}
${tb('4. Hai xe đẩy nhau: p trước bằng bao nhiêu, kiểm điều gì?')}${lines(1)}
${tb('5. Khi nào kết luận “bảo toàn trong sai số”?')}${lines(1)}
${tb('6. Vì sao p′ lệch p vài %, giảm bằng cách nào?')}${lines(1)}`)}
${K.btvn()}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Tốc độ và động lượng từ số đo cổng quang',
    de: `Xe ${m('0{,}320\\ \\mathrm{kg}')} gắn tấm cản quang rộng ${m('2{,}50\\ \\mathrm{cm}')} chạy trên băng đệm khí, chắn cổng quang ${m('0{,}040\\ \\mathrm s')}. Chiều dương là chiều chuyển động của xe.<br><b>a)</b> tốc độ của xe lúc qua cổng<br><b>b)</b> động lượng của xe<br><b>c)</b> nếu chọn chiều dương ngược lại: động lượng của xe`,
    nd: `đổi ${nw(`${m('s')} sang ${f(10)}&nbsp;m`)} trước khi tính; ${nw(`${m('v=')} ${f(12)} ${m('/')} ${f(12)}`)}`, a: ['a', 'b', 'c'], gi: 6, fig: H.congQuang() },
  { t: G('Dạng 2 · Trung bình · Va chạm mềm: p, p′, δ rồi so với ε'),
    de: `Xe 1 (${m('0{,}350\\ \\mathrm{kg}')}) va vào xe 2 (${m('0{,}250\\ \\mathrm{kg}')}) đang đứng yên, hai xe dính nhau. Tấm cản quang ${m('4{,}00\\ \\mathrm{cm}')}; ${m('t_1=0{,}080\\ \\mathrm s')}; ${m('t_1\\prime=0{,}140\\ \\mathrm s')}; sai số gộp ${m('\\varepsilon\\approx2{,}6\\,\\%')}.<br><b>a)</b> động lượng ${m('p')} trước va chạm<br><b>b)</b> động lượng ${m('p\\prime')} sau va chạm<br><b>c)</b> độ lệch ${m('\\delta')}<br><b>d)</b> bảo toàn trong sai số không? (ghi Có hay Không)`,
    nd: `xe 2 đứng yên ⇒ ${nw(`${m('p=')} ${f(12)} ${m('\\cdot v_1')}`)}; sau dính nhau khối lượng chuyển động là ${f(14)}`, a: ['a', 'b', 'c', 'd'], gi: 9, fig: H.boTri1('Va chạm mềm: xe 1 tới, xe 2 đứng yên.') },
  { t: G('Dạng 3 · Khó · Hai xe đẩy nhau: dấu và sai số của p′'),
    de: `Hai xe đứng yên, lò xo nén giữa chúng; xe 1 ${m('0{,}300\\ \\mathrm{kg}')}, xe 2 ${m('0{,}500\\ \\mathrm{kg}')}, tấm cản quang cùng ${m('4{,}00\\ \\mathrm{cm}')}. Cắt dây: xe 1 sang trái, ${m('t_1\\prime=0{,}160\\ \\mathrm s')}; xe 2 sang phải, ${m('t_2\\prime=0{,}265\\ \\mathrm s')}. Chọn chiều dương sang phải; ${nw(`${m('\\Delta m=0{,}001\\ \\mathrm{kg}')},`)} ${m('\\Delta t=0{,}001\\ \\mathrm s')}.<br><b>a)</b> động lượng ${m('p_1\\prime')} (có dấu)<br><b>b)</b> động lượng ${m('p_2\\prime')} (có dấu)<br><b>c)</b> tổng ${m('p\\prime')}<br><b>d)</b> sai số ${m('\\Delta p\\prime')}<br><b>e)</b> ${m('|p\\prime|\\le\\Delta p\\prime')}? (ghi Có hay Không)`,
    nd: `trước: ${nw(`${m('p=')} ${f(10)}`)}; xe đi ngược chiều dương thì ${m('p')} mang dấu ${f(10)}; ${nw(`${m('p=0')} nên so ${m('|p\\prime|')} với ${f(12)}`)}`, a: ['a', 'b', 'c', 'd', 'e'], gi: 6, cot: 5 },
  { t: 'Dạng 4 · Khó · Băng nghiêng: tìm h từ độ lệch',
    de: `Băng đệm khí dài ${m('L=1{,}50\\ \\mathrm m')} kê nghiêng xuống phía xe 2, bỏ qua ma sát: ${m('a\\approx gh/L')}, ${g98}. Tốc độ xe 1 đọc ở cổng 1 là ${m('0{,}400\\ \\mathrm{m/s}')}; xe 2 đứng yên cách cổng 1 đoạn ${m('x=0{,}250\\ \\mathrm m')}. Ba lần đo đều cho ${m('p\\prime\\gt p')} (${m('\\delta\\approx3{,}0\\,\\%\\gt\\varepsilon\\approx2{,}0\\,\\%')}), coi tốc độ thật ở chỗ va chạm lớn hơn số đọc đúng ${m('3{,}0\\,\\%')}.<br><b>a)</b> tốc độ thật ${m('v_t')} ở chỗ va chạm<br><b>b)</b> gia tốc ${m('a')} dọc băng<br><b>c)</b> độ cao ${m('h')} kê thêm (đổi ra mm)<br><b>d)</b> lệch cùng phía nhiều lần: sai số ${ck}hệ thống ${ck}ngẫu nhiên`,
    nd: `${nw(`${m('v_t^2=')} ${f(10)} ${m('+2ax')}`)}; ${nw(`${m('h=')} ${f(10)} ${m('\\cdot L/g')}`)}`, a: ['a', 'b', 'c', 'd'], gi: 6, fig: H.bangNghieng() },
];

const oY = (s, o, w = 25, u = {}) => s.split('<br>').map((p) => {
  const y = p.match(/^<b>([a-d])\)<\/b>/);
  if (!y) return `<div>${p}</div>`;
  const ls = o.filter((l) => l[0] === y[1]);
  return `<div class="yo"><span>${p}</span><span class="oo">${ls.map((l) => `<span class="nw"><b>${l})</b>${f(w)}</span>`).join('')}${u[y[1]] ? `<span class="un">${u[y[1]]}</span>` : ''}</span></div>`;
}).join('');
const ttDe = (b) => b.fig ? `<div class="fig-side" style="grid-template-columns:1fr ${b.fw}mm">${`<div>${oY(b.de, b.o, b.ow, b.u)}</div>`}${b.fig}</div>` : oY(b.de, b.o, b.ow, b.u);
const vaoVo = (ds) => ds.map((b) => (b.o ? { t: b.t, de: ttDe(b), k: 0 } : b));
const nhap = (n) => ({ t: '<span class="nhap-t">Nháp / chỗ em còn vướng</span>', de: lines(n), k: 0 });
const ttHaiCot = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .un{align-self:flex-end;font-size:.9em;margin-left:-1.5mm;white-space:nowrap}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–2', 'DẠNG 3–4'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Xe ${m('0{,}250\\ \\mathrm{kg}')} gắn tấm cản quang rộng ${m('3{,}00\\ \\mathrm{cm}')} chắn cổng quang ${m('0{,}050\\ \\mathrm s')}; chiều dương là chiều chuyển động của xe.<br><b>a)</b> tốc độ của xe<br><b>b)</b> động lượng của xe`, o: ['a', 'b'], u: {a:m('\\mathrm{m/s}'),b:m('\\mathrm{kg\\cdot m/s}')} },
    { t: 'Dạng 1 · Bài 2', de: `Xe ${m('0{,}415\\ \\mathrm{kg}')} gắn tấm cản quang rộng ${m('5{,}00\\ \\mathrm{cm}')}, chắn cổng ${m('0{,}125\\ \\mathrm s')}.<br><b>a)</b> tốc độ của xe<br><b>b)</b> động lượng, nếu chiều dương cùng chiều xe<br><b>c)</b> động lượng, nếu chiều dương ngược chiều xe`, o: ['a', 'b', 'c'], u: {a:m('\\mathrm{m/s}'),b:m('\\mathrm{kg\\cdot m/s}'),c:m('\\mathrm{kg\\cdot m/s}')} },
    { t: 'Dạng 2 · Bài 1', de: `Va chạm mềm: xe 1 (${m('0{,}300\\ \\mathrm{kg}')}) va xe 2 (${m('0{,}200\\ \\mathrm{kg}')}) đứng yên, hai xe dính nhau; tấm cản quang ${m('5{,}00\\ \\mathrm{cm}')}; ${m('t_1=0{,}100\\ \\mathrm s')}; ${m('t_1\\prime=0{,}170\\ \\mathrm s')}; ${m('\\varepsilon\\approx2{,}3\\,\\%')}.<br><b>a)</b> ${m('p')} trước va chạm<br><b>b)</b> ${m('p\\prime')} sau va chạm<br><b>c)</b> độ lệch ${m('\\delta')}<br><b>d)</b> bảo toàn trong sai số? (Có hay Không)`, o: ['a', 'b', 'c', 'd'], u: {a:m('\\mathrm{kg\\cdot m/s}'),b:m('\\mathrm{kg\\cdot m/s}'),c:m('\\mathrm{\\%}')} },
    { t: 'Dạng 2 · Bài 2', de: `Va chạm mềm: xe 1 (${m('0{,}400\\ \\mathrm{kg}')}) va xe 2 (${m('0{,}300\\ \\mathrm{kg}')}) đứng yên; tấm cản quang ${m('4{,}00\\ \\mathrm{cm}')}; ${m('t_1=0{,}100\\ \\mathrm s')}; ${m('t_1\\prime=0{,}170\\ \\mathrm s')}; ${m('\\varepsilon\\approx2{,}1\\,\\%')}.<br><b>a)</b> ${m('p')} trước<br><b>b)</b> ${m('p\\prime')} sau<br><b>c)</b> độ lệch ${m('\\delta')}<br><b>d)</b> bảo toàn trong sai số? (Có hay Không)`, o: ['a', 'b', 'c', 'd'], u: {a:m('\\mathrm{kg\\cdot m/s}'),b:m('\\mathrm{kg\\cdot m/s}'),c:m('\\mathrm{\\%}')} },
    nhap(8),
  ], [
    { t: 'Dạng 3 · Bài 1', de: `Hai xe đứng yên, lò xo nén giữa chúng: xe 1 ${m('0{,}400\\ \\mathrm{kg}')}, xe 2 ${m('0{,}200\\ \\mathrm{kg}')}, tấm cản quang ${m('4{,}00\\ \\mathrm{cm}')}. Cắt dây: xe 1 sang trái, ${m('t_1\\prime=0{,}200\\ \\mathrm s')}; xe 2 sang phải, ${m('t_2\\prime=0{,}098\\ \\mathrm s')}. Chiều dương sang phải; ${nw(`${m('\\Delta m=0{,}001\\ \\mathrm{kg}')},`)} ${m('\\Delta t=0{,}001\\ \\mathrm s')}.<br><b>a)</b> ${m('p_1\\prime')} và ${m('p_2\\prime')} (có dấu)<br><b>b)</b> tổng ${m('p\\prime')}<br><b>c)</b> sai số ${m('\\Delta p\\prime')}<br><b>d)</b> ${m('|p\\prime|\\le\\Delta p\\prime')}? (Có hay Không)`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c', 'd'], u: {a:m('\\mathrm{kg\\cdot m/s}'),b:m('\\mathrm{kg\\cdot m/s}'),c:m('\\mathrm{kg\\cdot m/s}')} },
    { t: 'Dạng 3 · Bài 2', de: `Cùng thí nghiệm hai xe đẩy nhau: xe 1 ${m('0{,}250\\ \\mathrm{kg}')} sang trái, ${m('t_1\\prime=0{,}125\\ \\mathrm s')}; xe 2 ${m('0{,}500\\ \\mathrm{kg}')} sang phải, ${m('t_2\\prime=0{,}255\\ \\mathrm s')}; tấm cản quang ${m('4{,}00\\ \\mathrm{cm}')}; <b>chiều dương sang trái</b>; ${nw(`${m('\\Delta m=0{,}001\\ \\mathrm{kg}')},`)} ${m('\\Delta t=0{,}001\\ \\mathrm s')}.<br><b>a)</b> ${m('p_1\\prime')} và ${m('p_2\\prime')} (có dấu)<br><b>b)</b> tổng ${m('p\\prime')}<br><b>c)</b> sai số ${m('\\Delta p\\prime')}<br><b>d)</b> ${m('|p\\prime|\\le\\Delta p\\prime')}? (Có hay Không)`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c', 'd'], u: {a:m('\\mathrm{kg\\cdot m/s}'),b:m('\\mathrm{kg\\cdot m/s}'),c:m('\\mathrm{kg\\cdot m/s}')} },
    { t: 'Dạng 4 · Bài 1', de: `Băng dài ${m('L=1{,}20\\ \\mathrm m')} kê nghiêng xuống phía xe 2; ${g98}; ${m('v=0{,}500\\ \\mathrm{m/s}')} ở cổng 1; ${m('x=0{,}300\\ \\mathrm m')}; tốc độ thật ở chỗ va chạm lớn hơn số đọc ${m('2{,}0\\,\\%')}; ${m('a\\approx g\\dfrac{h}{L}')}.<br><b>a)</b> ${m('v_t')}<br><b>b)</b> gia tốc ${m('a')}<br><b>c)</b> độ cao ${m('h')} (mm)`, o: ['a', 'b', 'c'], u: {a:m('\\mathrm{m/s}'),b:m('\\mathrm{m/s^2}'),c:m('\\mathrm{mm}')} },
    { t: 'Dạng 4 · Bài 2', de: `Băng dài ${m('L=1{,}50\\ \\mathrm m')} kê nghiêng xuống phía xe 2; ${g98}; ${m('v=0{,}600\\ \\mathrm{m/s}')} ở cổng 1; ${m('x=0{,}200\\ \\mathrm m')}; tốc độ thật lớn hơn số đọc ${m('4{,}0\\,\\%')}; ${m('a\\approx g\\dfrac{h}{L}')}.<br><b>a)</b> ${m('v_t')}<br><b>b)</b> gia tốc ${m('a')}<br><b>c)</b> độ cao ${m('h')} (mm)`, o: ['a', 'b', 'c'], u: {a:m('\\mathrm{m/s}'),b:m('\\mathrm{m/s^2}'),c:m('\\mathrm{mm}')} },
    nhap(3),
  ]],
  dap: [
    G(`D1·1: a) 0,600 m/s · b) 0,150 kg·m/s &nbsp;|&nbsp; D1·2: a) 0,400 m/s · b) +0,166 kg·m/s · c) −0,166 kg·m/s &nbsp;|&nbsp; D2·1: a) 0,150 kg·m/s · b) 0,1471 kg·m/s · c) 1,96 % ≈ 2,0 % · d) Có (δ ≤ ε) &nbsp;|&nbsp; D2·2: a) 0,160 kg·m/s · b) 0,1647 kg·m/s · c) 2,9 % · d) Không (δ &gt; ε)`),
    G(`D3·1: a<sub>1</sub>) −0,0800 · a<sub>2</sub>) +0,0816 · b) +0,0016 · c) 0,0018 · d) Có (|p′| ≤ Δp′) &nbsp;|&nbsp; D3·2: a<sub>1</sub>) +0,0800 · a<sub>2</sub>) −0,0784 · b) +0,0016 · c) 0,0014 · d) Không (|p′| &gt; Δp′) &nbsp;|&nbsp; D4·1: a) 0,510 m/s · b) 0,0168 m/s² · c) 2,1 mm &nbsp;|&nbsp; D4·2: a) 0,624 m/s · b) 0,0734 m/s² · c) 11 mm`),
  ],
};

await K.dung({
  trang1to5: [ttHaiCot, p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [2, 2], kq: [[1, 2], [3, 4]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'dụng cụ 1·4 · ý tưởng đo 2·1 · bố trí 2·2 · bảng thí nghiệm 1 3·1 · công thức sai số 3·3 · thí nghiệm 2 4·1 · bảng 4 4·3 · bẫy 5·2 · dạng 1–2 → 6·1 · dạng 3–4 → 7·1',
  out: process.argv[2],
});
