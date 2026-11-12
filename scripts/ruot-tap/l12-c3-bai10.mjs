// Ruột tập VL12 – Chương 3 · Bài 10 · Lực từ. Cảm ứng từ (lesson id 11). Quyển Chương 3 lớp 12: bài 9 = tr. 1–12, bài 10 = tr. 13–24.
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Hình: hinh-l12-c3-bai10.mjs (toàn bộ SVG tự vẽ). Nội dung theo bài web (book/cache/11.json, tải từ DB 12/11/2026):
// mục tiêu, dự đoán dây song song đường sức, II.1–II.6 (bàn tay trái, F = BIl sinα, cân dòng điện, cảm ứng từ, ngẫu lực từ,
// nắm tay phải, lực Lorentz), ba bẫy, Trả bài 7 câu, bài toán mẫu, thử thách ⭐–⭐⭐⭐, 6 dạng bài tập mẫu.
// Đáp số Bài tương tự (tuongTu.dap) tính bằng Python 12/11/2026. Tên file có '-c3-' vì bài 14–16 Chương 3 trùng số Chương 4.
// Chạy: node scripts/ruot-tap/l12-c3-bai10.mjs [file.pdf]   → scripts/ruot-tap/out/ruot-tap-vl12-c3-bai10.pdf
//       node scripts/ruot-tap/l12-c3-bai10.mjs --hinh       → chụp từng hình ở cỡ in (46 mm) vào out/hinh-l12-c3-bai10/
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL12c3b10 as H } from './hinh-l12-c3-bai10.mjs';
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
  const out = resolve(HERE, 'out/hinh-l12-c3-bai10'); mkdirSync(out, { recursive: true });
  const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true, args: ['--allow-file-access-from-files'] });
  const pg = await b.newPage();
  for (const [name, fn] of Object.entries(H)) {
    writeFileSync(out + '/_tmp.html', `<!doctype html><meta charset="utf-8"><link rel="stylesheet" href="${pathToFileURL(BOOK + 'node_modules/katex/dist/katex.min.css').href}"><style>${css}</style>${fn()}`);
    await pg.goto(pathToFileURL(out + '/_tmp.html').href, { waitUntil: 'networkidle0' });
    await pg.evaluate('document.fonts.ready');
    await (await pg.$('.fig')).screenshot({ path: `${out}/${name}.png` });
    console.log(`${name}.png`);
  }
  await b.close();
  process.exit(0);
}

const K = khoiTao({ bai: 10, lid: 11, ten: 'LỰC TỪ · CẢM ỨNG TỪ', lop: 12, baiDau: 9, sub: 'Vật lí 12 · Chương 3: Từ trường' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const al = m('\\alpha'), vB = m('\\vec B'), vF = m('\\vec F');
const RA = m('\\odot'), VAO = m('\\otimes');
const u = (s, d) => nw(m(`${s}\\ \\mathrm{${d}}`));
const g10 = nw(m('g=10\\ \\mathrm{m/s^2}'));
const aDef = `${al}: góc giữa dây và ${vB}`;

// Bài tương tự 1 cột, ô đáp số cuối dòng của ý (cùng cách l11-bai16).
const ttCss = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';

const p1 = `${ttCss}<section class="page">
${head('BÀI 10 · LỰC TỪ · CẢM ỨNG TỪ', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Nêu <b>điểm đặt, phương, chiều</b> của lực từ lên đoạn dây; dùng quy tắc <b>bàn tay trái</b>`)}
${dong(`${ck}Tính độ lớn lực từ lên đoạn dây; tìm <b>cảm ứng từ</b> ${m('B')} (đơn vị tesla)`)}
${dong(`${ck}Giải thích vì sao khung dây <b>quay</b>; xác định chiều đường sức bằng quy tắc <b>nắm tay phải</b>`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Loa bluetooth hát được nhờ cuộn dây mang dòng điện đặt sát nam châm. Nếu đặt đoạn dây mang dòng điện <b>song song</b> với đường sức từ thì lực từ lên dây:</p>
<div class="fig-side" style="${fs(38)}"><div>
${opt('A', 'Lớn nhất')}
${opt('B', 'Bằng 0')}
${opt('C', 'Khác 0 nhưng nhỏ nhất')}
${opt('D', 'Chỉ bằng 0 khi dây vuông góc đường sức')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 1)}</div>
${H.kheDuDoan()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Lực từ lên đoạn dây mang dòng điện', '1·4')}
<div class="card" style="padding:1.2mm 3mm">
<div><b>Điểm đặt:</b> ${f(30)} của đoạn dây. <b>Phương:</b> vuông góc với mặt phẳng chứa ${f(14)} và ${f(14)}.</div>
<div>Kí hiệu hướng: ${RA} hướng ${f(30)} mặt phẳng hình · ${VAO} hướng ${f(30)} mặt phẳng hình.</div>
<div><b>Quy tắc bàn tay trái:</b> đặt bàn tay trái duỗi thẳng sao cho đường sức từ xuyên vào ${f(24)}; chiều từ cổ tay đến ngón tay trùng chiều ${f(24)}; ngón cái choãi ${m('90^\\circ')} chỉ chiều ${f(24)}.</div>
</div>
<div class="card fig-side" style="${fs(42)};padding:1.2mm 3mm"><div>
<div><b>Thí nghiệm · Làm:</b> treo dây nhôm nằm ngang giữa hai cực nam châm, nối nguồn một chiều 3–6 V, đóng khoá K.</div>
<div><b>Quan sát:</b> đóng mạch, dây ${f(36)}; đảo chiều dòng, dây ${f(36)}; xoay cho dây song song đường sức, dây ${f(30)}.</div>
<div><b>Rút ra:</b> lực từ có khi dây ${f(40)} đường sức; chiều lực đổi theo chiều ${f(20)}.</div></div>
${H.dayTreo()}</div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('ĐỘ LỚN LỰC TỪ · CÂN DÒNG ĐIỆN · CẢM ỨNG TỪ')}
${h3(1, 'II.2 · Độ lớn lực từ (định luật Ampe)', '2·1')}
<div class="card" style="padding:1.2mm 3mm">
<div style="margin:.4mm 0;min-height:12mm;display:flex;align-items:flex-end;gap:3mm">${m('F=')} <span class="fill" style="min-width:34mm;height:10mm"></span>
<span>Vuông góc: ${nw(`${m('F_{\\max}=')} ${f(16)}`)} · song song: ${nw(`${m('F=')} ${f(10)}`)}</span></div>
<div class="hint">Ghi tên đại lượng và đơn vị:</div><table class="tbl-ct"><tr><td style="width:8mm">${m('F')}</td><td></td><td></td><td style="width:8mm">${m('I')}</td><td></td><td style="width:14mm"></td></tr>
<tr><td>${m('B')}</td><td></td><td style="width:14mm"></td><td style="width:8mm">${m('l')}</td><td></td><td></td></tr>
<tr><td>${al}</td><td colspan="5">góc giữa ${f(30)} và ${f(30)}</td></tr></table>
</div>
${h3(2, 'Thí nghiệm: cân dòng điện đo lực từ', '2·2')}
<div class="fig-side" style="${fs(44)}"><div>
<div style="font-size:var(--fs-sm);line-height:1.35;margin-bottom:.6mm">Nam châm chữ U đặt trên cân (khe có từ trường đều, hướng N sang S); dây MN kẹp trên giá riêng, phần trong khe dài ${u('l=5{,}0', 'cm')}, ${u('I=2{,}0', 'A')}. Số chỉ cân tăng ${m('\\Delta m')}; ${nw(m('F=\\Delta m\\cdot g'))}, ${nw(m('g=9{,}8\\ \\mathrm{m/s^2}'))}.</div>
<table class="tbl-ct"><tr><th>Góc ${al}</th><th>${m('90^\\circ')}</th><th>${m('60^\\circ')}</th><th>${m('30^\\circ')}</th><th>${m('0^\\circ')}</th></tr>
<tr><td>${m('\\Delta m')} (g)</td><td>1,03</td><td>0,87</td><td>0,52</td><td>0,00</td></tr>
<tr><td>${m('\\sin\\alpha')}</td><td>1</td><td>0,866</td><td>0,500</td><td>0</td></tr>
<tr><td>${m('\\Delta m/\\sin\\alpha')} (g)</td><td>1,03</td><td>1,00</td><td></td><td>—</td></tr></table>
<div style="margin-top:.6mm"><b>Rút ra:</b> tỉ số ${m('\\Delta m/\\sin\\alpha')} gần như ${f(24)} ⇒ ${m('F')} tỉ lệ với ${f(16)}.</div>
<div>Dây bị đẩy ${f(14)} nên nam châm bị đẩy ${f(14)} (lực – phản lực), cân chỉ ${f(14)}.</div>
<div>Ở ${m('90^\\circ')}: ${m('F=')} ${f(20)} N ⇒ ${m('B=F/(Il)=')} ${f(16)} T</div></div>
${H.canDong()}</div>
${h3(3, 'II.3 · Cảm ứng từ', '2·3')}
<div class="card" style="padding:1.2mm 3mm">
<div>${vB} là vectơ đặc trưng cho từ trường về mặt ${f(30)}.</div>
<div><b>Phương:</b> phương của ${f(40)} nằm cân bằng tại điểm đó. <b>Chiều:</b> từ cực ${f(12)} sang cực ${f(12)} của nó.</div>
<div style="display:flex;align-items:flex-end;gap:2mm;min-height:11mm"><b>Độ lớn:</b> ${m('B=')} <span class="fill" style="min-width:24mm;height:10mm"></span> · đơn vị ${f(14)} (T), ${nw(`${m('1\\ \\mathrm T=1')} ${f(16)}`)}</div>
<div>Mốc so: Trái Đất cỡ ${u('5\\cdot10^{-5}', 'T')}; khe nam châm chữ U cỡ ${u('0{,}1', 'T')}; máy MRI 1,5–3 T.</div>
</div>
${h3(4, 'Làm nhanh', '2·4')}
${box(cau(`<b>Câu 1.</b> Dây dài ${u('5', 'cm')}, ${u('I=2', 'A')}, vuông góc đường sức, lực từ ${u('0{,}01', 'N')}. Tính ${m('B')}. Tăng dòng lên ${u('4', 'A')} thì ${m('B')} và ${m('F')} bằng bao nhiêu?`, 2))}
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('NGẪU LỰC TỪ · NẮM TAY PHẢI · LỰC LORENTZ')}
${h3(1, 'II.4 · Lực từ lên khung dây: ngẫu lực từ', '3·1')}
<div class="card fig-side" style="${fs(42)};padding:1.2mm 3mm"><div>
<div>Hai cạnh đối diện chịu hai lực cùng ${f(16)}, ngược ${f(14)}, không cùng ${f(12)} ⇒ <b>ngẫu lực từ</b>: hợp lực ${f(12)}, khung ${f(16)}.</div>
<div style="display:flex;align-items:flex-end;gap:2mm;min-height:8mm">${m('M=')} ${f(30)} · ${nw(`${m('M_{\\max}=')} ${f(20)}`)}</div>
<div>${al} ở đây là góc giữa ${vB} và ${f(30)} của khung (khác ${al} trong ${m('F')}).</div>
<div>${m('M')} lớn nhất khi mặt khung ${f(24)} đường sức; ${m('M=0')} khi mặt khung ${f(24)} đường sức: khung dừng ở đó.</div></div>
${H.nguLuc()}</div>
${h3(2, 'II.5 · Từ trường của dòng điện: quy tắc nắm tay phải', '3·2')}
<div class="card fig-side" style="${fs(34)};padding:1.2mm 3mm"><div>
<div><b>Dây thẳng:</b> đường sức là đường ${f(16)} đồng tâm, tâm trên dây, nằm trong mặt phẳng ${f(24)} với dây. Ngón cái theo ${f(10)}, bốn ngón khum theo ${f(16)}.</div>
<div><b>Vòng dây, ống dây:</b> bốn ngón khum theo ${f(10)}, ngón cái chỉ ${f(14)} trong lòng. Trong lòng ống dây: từ trường ${f(14)}, đường sức ${f(24)} trục ống.</div>
<div><b>Hai dòng điện song song:</b> cùng chiều thì ${f(14)}; ngược chiều thì ${f(14)}.</div>
<div class="hint">Phân biệt: tay trái tìm chiều ${f(10)}; tay phải tìm chiều ${f(10)}.</div></div>
${H.dayThang()}</div>
${h3(3, 'II.6 · Lực từ lên hạt mang điện chuyển động (lực Lorentz)', '3·3')}
<div class="card fig-side" style="${fs(42)};padding:1.2mm 3mm"><div>
<div>${m('f=')} ${f(26)}, ${al}: góc giữa ${m('\\vec v')} và ${vB}. Phương vuông góc với cả ${m('\\vec v')} và ${vB}.</div>
<div>Chiều: bàn tay trái, cổ tay → ngón tay theo ${m('\\vec v')}; ngón cái chỉ ${m('\\vec f')} nếu ${m('q>0')}; electron thì ${f(20)}.</div>
<div>${m('\\vec f\\perp\\vec v')} nên lực từ ${f(20)} công: tốc độ ${f(20)}.</div>
<div style="display:flex;align-items:flex-end;gap:2mm;min-height:10mm">${m('\\vec v\\perp\\vec B')}: tròn đều, ${m('r=')} <span class="fill" style="min-width:18mm;height:9mm"></span> ${m('T=')} <span class="fill" style="min-width:18mm;height:9mm"></span></div></div>
${H.lorentz()}</div>
${box(cau(`<b>Làm nhanh.</b> Electron bay vuông góc từ trường đều, ${u('v=2\\cdot10^7', 'm/s')}, ${u('B=2\\cdot10^{-3}', 'T')}; cho ${u('m=9{,}1\\cdot10^{-31}', 'kg')}, ${u('|q|=1{,}6\\cdot10^{-19}', 'C')}. Tính ${m('f')}, ${m('r')}, ${m('T')}.`, 3))}
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('BA CÁI BẪY · TRẢ BÀI · TỰ KIỂM TRA')}
${h3(1, 'III · Ba cái bẫy hay sập', '4·1')}
<div class="card fig-side" style="${fs(40)};padding:1mm 3mm"><div>
<div class="trap">${ck}<span><b>“Có từ trường là có lực.”</b> Dây song song đường sức (${nw(m('\\alpha=0^\\circ'))} hoặc ${nw(m('180^\\circ'))}) thì ${nw(m('F=0'))}, khỏi đặt tay trái (hình b).</span></div>
<div class="trap">${ck}<span><b>“Tay nào cũng được.”</b> Tay <b>trái</b>: chiều lực ${vF}. Tay <b>phải</b> (nắm tay): chiều ${vB} do dòng điện sinh ra.</span></div>
<div class="trap">${ck}<span><b>“Tăng dòng thử thì ${m('B')} tăng.”</b> ${m('B')} có sẵn ở chỗ đặt dây; tăng ${m('I')} thì ${m('F')} tăng, ${m('B')} không đổi.</span></div></div>
${H.vuongSong()}</div>
${h3(2, 'IV · Trả bài 7 câu', '4·2')}
${box(`${tb('1. Lực từ lên đoạn dây: điểm đặt, phương, chiều?')}${lines(1)}
${tb('2. Phát biểu quy tắc bàn tay trái.')}${lines(2)}
${tb(`3. Công thức ${m('F')}, kí hiệu, đơn vị; khi nào ${m('F=0')}?`)}${lines(2)}
${tb('4. Cảm ứng từ: phương, chiều, độ lớn, đơn vị.')}${lines(2)}
${tb(`5. Vì sao khung dây quay trong từ trường? Viết ${m('M')}.`)}${lines(2)}
${tb('6. Chiều đường sức của dây thẳng, vòng dây, ống dây?')}${lines(2)}
${tb('7. Hạt mang điện bay vuông góc đường sức chuyển động thế nào?')}${lines(2)}`)}
<div class="card soft" style="margin-top:.8mm;padding:.8mm 3mm"><b>Bạn cùng bàn kiểm:</b> ……/7 câu · chưa thuộc: ${f(25)} ${nw(`→ đọc lại ô ${f(12)} Tập`)}</div>
${h3(3, 'Kết quả tự kiểm tra (9 câu trên web, chiếu trên lớp)', '4·3')}
${rkHai([1, 2, 3, 4, 5], [6, 7, 8, 9])}
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TOÁN MẪU · BÀI TẬP VỀ NHÀ · THỬ THÁCH')}
${h3(1, 'V · Bài toán mẫu: đoạn dây trong từ trường nam châm', '5·1')}
<div class="card soft fig-side" style="${fs(40)};padding:1.2mm 3mm"><div>Dây dài ${u('l=20', 'cm')} mang dòng ${u('I=2{,}5', 'A')} trong từ trường đều ${u('B=0{,}08', 'T')}; dây hợp đường sức góc ${m('30^\\circ')}.<br>
<b>a)</b> lực từ lên đoạn dây<br><b>b)</b> xoay dây vuông góc đường sức: ${m('F')} bằng bao nhiêu<br><b>c)</b> thay bằng khung ${nw(m('4\\times5\\ \\mathrm{cm}'))}, ${m('N=50')} vòng, cùng dòng: ${m('M_{\\max}')}</div>
${H.dayXien()}</div>
<table><tr><th style="width:44mm">Câu trong đề</th><th style="width:30mm">Dữ liệu</th><th>Kiến thức</th></tr>
<tr><td>“dài 20 cm”</td><td>${m('l=0{,}20\\ \\mathrm m')}</td><td>đổi ra mét</td></tr>
<tr><td style="height:6.5mm">“góc 30° với đường sức”</td><td></td><td></td></tr>
<tr><td style="height:6.5mm">“khung 4×5 cm, 50 vòng”</td><td></td><td></td></tr>
</table>
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm;margin-top:1mm">
${wl(`a) ${m('F=')}`, 1)}${wl(`b) ${m('F=')}`, 1)}${wl(`c) ${m('S=')} … ⇒ ${m('M_{\\max}=')}`, 1)}</div>
${h3(2, 'Điền bước còn thiếu', '5·2')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div class="ln"><b>Đề:</b> dây ${u('25', 'cm')}, ${u('I=4', 'A')}, vuông góc đường sức, lực kế đo ${u('F=0{,}05', 'N')}. Tìm ${m('B')}.</div>
<div class="ln"><b>Bước 1 (cho sẵn):</b> dây vuông góc nên ${m('B=F/(Il)')}.</div>
${wl('Bước 2: thay số (đổi cm ra m):', 1)}${wl(`Bước 3: ${m('B=')} ………… T; có hợp lí không?`, 1)}</div>
${K.btvn().replace('<i>1</i>', '<i>3</i>')}
${h3(4, 'Thử thách phân tầng', '5·4')}
${box(cau(`${m('\\bigstar')} Dây ${u('10', 'cm')} mang dòng ${u('2', 'A')} vuông góc đường sức, ${u('B=0{,}5', 'T')}. Tính lực từ.`, 1)
 + cau(`${m('\\bigstar\\bigstar')} Cũng dây đó, hợp đường sức ${m('30^\\circ')}, lực từ đo được ${u('0{,}1', 'N')}. ${m('B')} bằng bao nhiêu?`, 1)
 + cau(`${m('\\bigstar\\bigstar\\bigstar')} Khung 20 vòng, ${nw(m('S=25\\ \\mathrm{cm^2}'))}, dòng ${u('2', 'A')}, ${u('B=0{,}4', 'T')}: ${m('M_{\\max}')}? Vì sao khung quay mà tâm khung không bị đẩy đi?`, 2))}
${foot(5)}</section>`;

// Hình đặt cạnh đề (cột 40 mm) để không tốn chiều cao; dạng 6 hình đặt cạnh ô giải (khung: 46 mm).
const deH = (txt, fig, w = 40) => `<div class="fig-side" style="grid-template-columns:1fr ${w}mm;gap:2mm"><div>${txt}</div>${fig}</div>`;
const dang = [
  { t: 'Dạng 1 · Dễ · Bàn tay trái: chiều lực từ',
    de: `Dây MN nằm ngang (M trái, N phải), đường sức vuông góc mặt phẳng hình, hướng ra (${RA}).<br><b>a)</b> dòng từ M đến N: lực từ hướng lên, xuống, trái hay phải<br><b>b)</b> đảo chiều dòng, giữ từ trường: chiều lực<br><b>c)</b> từ câu a, đảo cả dòng và từ trường (${VAO}): chiều lực`,
    nd: `tay trái: đường sức vào ${f(16)}, cổ tay → ngón tay theo ${f(6)}, ngón cái chỉ ${f(6)}`, a: ['a', 'b', 'c'], gi: 3 },
  { t: 'Dạng 2 · Trung bình · Dùng ngược bàn tay trái',
    de: deH(`<b>a)</b> dây thẳng đứng, dòng chạy lên, lực sang phải; đường sức vuông góc hình: ra hay vào<br><b>b)</b> dây vuông góc hình, N trái, S phải, lực hướng xuống: dòng ra hay vào<br><b>c)</b> MN ngang, đường sức hướng xuống, lực hướng vào: dòng M → N hay N → M`, H.d2(''), 44),
    nd: `biết hai chiều thì đặt tay trái theo chúng; giữa hai cực, đường sức đi từ ${f(6)} sang ${f(6)}`, a: ['a', 'b', 'c'], gi: 3 },
  { t: `Dạng 3 · Trung bình · Tính ${m('F=BIl\\sin\\alpha')}`,
    de: `Dây thẳng dài ${u('15', 'cm')}, dòng ${u('4{,}0', 'A')}, từ trường đều ${u('B=0{,}25', 'T')} (${aDef}). Độ lớn lực từ khi dây:<br><b>a)</b> vuông góc đường sức<br><b>b)</b> hợp đường sức ${m('30^\\circ')}<br><b>c)</b> hợp đường sức ${m('150^\\circ')}`,
    nd: `đổi ${m('l')} ra ${f(10)}; ${nw(`${m('\\sin150^\\circ=')} ${f(10)}`)}; dọc đường sức thì ${nw(`${m('\\sin\\alpha=')} ${f(8)}`)}`, a: ['a', 'b', 'c'], gi: 3 },
  { t: 'Dạng 4 · Trung bình · Tìm B từ lực từ đo được',
    de: `Dây thẳng dài ${u('12', 'cm')}, dòng ${u('2{,}5', 'A')}, hợp đường sức từ trường đều góc ${m('30^\\circ')}; lực từ đo được ${u('15', 'mN')}.<br><b>a)</b> cảm ứng từ ${m('B')}<br><b>b)</b> tăng dòng lên ${u('5{,}0', 'A')}, giữ nguyên dây, vị trí, từ trường: ${m('B')} khi đó; lực từ (mN)`,
    nd: `${nw(`${m('B=')} ${f(20)}`)}; đổi mN ra N; tăng dòng thử thì ${m('B')} ${f(16)}`, a: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>'], gi: 3 },
  { t: 'Dạng 5 · Khó · Dây cân bằng: chiều I, cường độ, lực căng',
    de: deH(`Dây MN dài ${u('20', 'cm')}, nặng ${u('8{,}0', 'g')}, treo ngang bằng hai sợi chỉ nhẹ trong từ trường đều ${u('B=0{,}10', 'T')} hướng ra (${RA}); ${g10}.<br><b>a)</b> chiều, cường độ dòng để lực căng hai sợi chỉ bằng 0<br><b>b)</b> giảm dòng còn ${u('2{,}4', 'A')}, giữ chiều: tổng lực căng (mN)`, H.d5(), 34),
    nd: `lực căng bằng 0 ⇒ lực từ hướng ${f(10)}, ${nw(`${m('F=')} ${f(8)}`)}; còn lực căng: ${nw(`${m('T+F=')} ${f(8)}`)}`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b'], gi: 3 },
  { t: 'Dạng 6 · Khó · Khung dây: lực từng cạnh, mômen ngẫu lực',
    de: deH(`Khung ABCD: ${u('AB=6{,}0', 'cm')}, ${u('BC=4{,}0', 'cm')}, 50 vòng, ${u('I=2{,}0', 'A')}, ${u('B=0{,}20', 'T')}; mặt khung song song đường sức, AB vuông góc đường sức (${al} trong ${m('M')}: góc giữa ${vB} và pháp tuyến).<br><b>a)</b> lực lên mỗi cạnh chịu lực từ<br><b>b)</b> mômen ngẫu lực từ<br><b>c)</b> mômen khi pháp tuyến hợp đường sức ${m('30^\\circ')}`, H.d6()),
    nd: `cạnh dọc đường sức: ${nw(`${m('F=')} ${f(6)}`)}; hợp lực lên khung ${f(8)}; ${nw(`${m('M=')} ${f(20)}`)}`, a: ['a', 'b', 'c'], gi: 3 },
];

// Bài tương tự: mỗi dạng 2 bài, giải vào vở (thầy chốt 10/11), ô đáp số cuối dòng của ý; đáp số tính bằng Python 12/11/2026.
const oY = (s, o, w = {}) => s.split('<br>').map((p) => {
  const y = p.match(/^<b>([a-d])\)<\/b>/);
  if (!y) return `<div>${p}</div>`;
  const ls = o.filter((l) => l[0] === y[1]);
  return `<div class="yo"><span>${p}</span><span class="oo">${ls.map((l) => `<span class="nw"><b>${l})</b>${f(typeof w === 'object' ? (w[l] ?? 22) : w)}</span>`).join('')}</span></div>`;
}).join('');
const ttDe = (b) => b.fig ? `<div class="fig-side" style="grid-template-columns:1fr ${b.fw}mm">${`<div>${oY(b.de, b.o, b.ow)}</div>`}${b.fig}</div>` : oY(b.de, b.o, b.ow);
const vaoVo = (ds) => ds.map((b) => (b.o ? { t: b.t, de: ttDe(b), k: 0 } : b));
const nhap = (n) => ({ t: '<span class="nhap-t">Nháp / chỗ em còn vướng</span>', de: lines(n), k: 0 });
const huong = 'Ghi hướng: lên, xuống, trái, phải, ra hoặc vào mặt phẳng hình.';
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–3', 'DẠNG 4–6'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Dây MN thẳng đứng (M trên, N dưới), đường sức vuông góc mặt phẳng hình, hướng vào (${VAO}); dòng từ M đến N. ${huong}<br><b>a)</b> chiều lực từ<br><b>b)</b> đảo chiều từ trường (${RA}), giữ dòng: chiều lực<br><b>c)</b> từ câu a, đảo cả dòng và từ trường: chiều lực`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 1 · Bài 2', de: `Dây MN nằm ngang (M trái, N phải), đường sức trong mặt phẳng hình, hướng lên; dòng từ M đến N.<br><b>a)</b> chiều lực từ<br><b>b)</b> xoay dây thẳng đứng (dọc đường sức): lực từ bằng bao nhiêu<br><b>c)</b> như câu a nhưng dòng từ N đến M: chiều lực`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 2 · Bài 1', de: `Biết hai chiều, tìm chiều thứ ba.<br><b>a)</b> dây ngang, dòng sang phải, lực hướng lên; đường sức vuông góc hình: ra hay vào<br><b>b)</b> dây vuông góc hình, N trên, S dưới, lực sang trái: dòng ra hay vào<br><b>c)</b> dây thẳng đứng, đường sức sang phải, lực hướng ra: dòng chạy lên hay xuống`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 2 · Bài 2', de: `Biết hai chiều, tìm chiều thứ ba.<br><b>a)</b> dây thẳng đứng, dòng chạy xuống, lực sang trái; đường sức vuông góc hình: ra hay vào<br><b>b)</b> dây vuông góc hình, S trái, N phải, lực hướng xuống: dòng ra hay vào<br><b>c)</b> MN ngang (M trái), đường sức hướng vào, lực hướng xuống: M → N hay N → M`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 3 · Bài 1', de: `Dây dài ${u('25', 'cm')}, ${u('I=3{,}0', 'A')}, từ trường đều ${u('B=0{,}40', 'T')} (${aDef}). Lực từ khi dây:<br><b>a)</b> vuông góc đường sức<br><b>b)</b> hợp đường sức ${m('30^\\circ')}<br><b>c)</b> hợp đường sức ${m('120^\\circ')}<br><b>d)</b> song song đường sức`, o: ['a', 'b', 'c', 'd'], ow: 18 },
    { t: 'Dạng 3 · Bài 2', de: `Dây dài ${u('8{,}0', 'cm')}, ${u('I=5{,}0', 'A')}, từ trường đều ${u('B=0{,}050', 'T')} (${aDef}).<br><b>a)</b> lực từ khi dây vuông góc đường sức (mN)<br><b>b)</b> lực từ khi dây hợp đường sức ${m('45^\\circ')} (mN)<br><b>c)</b> góc nhọn ${al} để lực từ bằng ${u('10', 'mN')}`, o: ['a', 'b', 'c'] },
  ], [
    { t: 'Dạng 4 · Bài 1', de: `Dây dài ${u('10', 'cm')}, ${u('I=4{,}0', 'A')}, vuông góc đường sức từ trường đều, lực từ ${u('0{,}060', 'N')}.<br><b>a)</b> cảm ứng từ ${m('B')}<br><b>b)</b> giảm dòng còn ${u('2{,}0', 'A')}, giữ nguyên dây và từ trường: ${m('B')} khi đó; lực từ (mN)`, o: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>'] },
    { t: 'Dạng 4 · Bài 2', de: `Dây dài ${u('5{,}0', 'cm')}, ${u('I=3{,}0', 'A')}, hợp đường sức từ trường đều góc ${m('30^\\circ')}, lực từ ${u('4{,}5', 'mN')}.<br><b>a)</b> cảm ứng từ ${m('B')}<br><b>b)</b> xoay dây vuông góc đường sức, giữ dòng: lực từ (mN)`, o: ['a', 'b'] },
    { t: 'Dạng 5 · Bài 1', de: `Dây MN dài ${u('25', 'cm')}, khối lượng ${u('10', 'g')}, treo ngang bằng hai sợi chỉ nhẹ (M trái, N phải), từ trường đều ${u('B=0{,}20', 'T')} hướng vào (${VAO}); ${g10}.<br><b>a)</b> chiều và cường độ dòng điện để lực căng bằng 0<br><b>b)</b> dòng ${u('1{,}2', 'A')} cùng chiều câu a: tổng lực căng (mN)<br><b>c)</b> dòng ${u('1{,}2', 'A')} ngược chiều câu a: tổng lực căng (mN)`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'], ow: 16 },
    { t: 'Dạng 5 · Bài 2', de: `Thanh kim loại MN dài ${u('20', 'cm')}, khối lượng ${u('6{,}0', 'g')}, treo ngang bằng hai sợi chỉ nhẹ (M trái, N phải), từ trường đều ${u('B=0{,}15', 'T')} hướng ra (${RA}); dòng ${u('3{,}0', 'A')} từ M đến N; ${g10}.<br><b>a)</b> độ lớn (mN) và chiều lực từ<br><b>b)</b> tổng lực căng hai sợi chỉ (mN)`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b'] },
    { t: 'Dạng 6 · Bài 1', de: `Khung vuông cạnh ${u('5{,}0', 'cm')}, ${m('N=100')} vòng, ${u('I=2{,}0', 'A')}, từ trường đều ${u('B=0{,}10', 'T')}; mặt khung song song đường sức, hai cạnh vuông góc đường sức (${al} trong ${m('M')}: góc giữa ${vB} và pháp tuyến).<br><b>a)</b> lực từ lên mỗi cạnh vuông góc đường sức<br><b>b)</b> mômen ngẫu lực lúc đầu<br><b>c)</b> mômen khi pháp tuyến hợp đường sức ${m('60^\\circ')}`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 6 · Bài 2', de: `Khung chữ nhật ${nw(m('8{,}0\\times5{,}0\\ \\mathrm{cm}'))}, ${m('N=40')} vòng, trong từ trường đều ${u('B=0{,}25', 'T')}; mômen cực đại đo được ${nw(m('0{,}060\\ \\mathrm{N{\\cdot}m}'))}.<br><b>a)</b> cường độ dòng điện<br><b>b)</b> mômen khi mặt khung vuông góc đường sức<br><b>c)</b> mômen khi pháp tuyến hợp đường sức ${m('30^\\circ')}`, o: ['a', 'b', 'c'] },
  ]],
  dap: [
    `D1·1: a) sang phải · b) sang trái · c) sang phải &nbsp;|&nbsp; D1·2: a) ra (${RA}) · b) 0 · c) vào (${VAO}) &nbsp;|&nbsp; D2·1: a) vào · b) vào · c) chạy xuống &nbsp;|&nbsp; D2·2: a) ra · b) ra · c) N → M &nbsp;|&nbsp; D3·1: a) 0,30 N · b) 0,15 N · c) 0,26 N · d) 0 &nbsp;|&nbsp; D3·2: a) 20 mN · b) 14 mN · c) 30°`,
    `D4·1: a) 0,15 T · b<sub>1</sub>) 0,15 T · b<sub>2</sub>) 30 mN &nbsp;|&nbsp; D4·2: a) 0,060 T · b) 9,0 mN &nbsp;|&nbsp; D5·1: a<sub>1</sub>) M → N · a<sub>2</sub>) 2,0 A · b) 40 mN · c) 160 mN &nbsp;|&nbsp; D5·2: a<sub>1</sub>) 90 mN · a<sub>2</sub>) xuống · b) 150 mN &nbsp;|&nbsp; D6·1: a) 1,0 N · b) 0,050 N·m · c) 0,043 N·m &nbsp;|&nbsp; D6·2: a) 1,5 A · b) 0 · c) 0,030 N·m`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 3], kq: [[1, 2, 3], [4, 5, 6]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'bàn tay trái 1·4 · độ lớn F 2·1 · cân dòng điện 2·2 · cảm ứng từ 2·3 · ngẫu lực 3·1 · nắm tay phải 3·2 · Lorentz 3·3 · bẫy 4·1 · bài toán mẫu 5·1 · dạng 1–3 → 6·1 · dạng 4–6 → 7·1',
  out: process.argv[2] ?? resolve(HERE, 'out/ruot-tap-vl12-c3-bai10.pdf'),
});
