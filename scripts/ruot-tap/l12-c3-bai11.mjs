// Ruột tập VL12 – Chương 3 · Bài 11 · Thực hành: đo độ lớn cảm ứng từ (lesson id 12). Quyển Chương 3 lớp 12: bài 11 = tr. 25–36 (baiDau 9).
// Khung: khung.mjs (bố cục bài 14: 1–5 học · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR).
// Bài THỰC HÀNH (web không có bài tập mẫu): tr.1–5 = nguyên lý · dụng cụ + bố trí · các bước + bẫy · bảng số liệu + sai số · đồ thị Δm–I + suy ra B + báo cáo.
// Nội dung theo bài web (book/cache/12.json, tải 12/11/2026). Đáp số mọi bài (BTM, tương tự) tính bằng Python 12/11/2026.
// Chạy: node scripts/ruot-tap/l12-c3-bai11.mjs   → scripts/ruot-tap/out/ruot-tap-vl12-c3-bai11.pdf
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL12c3b11 as H } from './hinh-l12-c3-bai11.mjs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const OFF = (11 - 9) * 12;
const K = khoiTao({ bai: 11, lid: 12, lop: 12, baiDau: 9, ten: 'THỰC HÀNH: ĐO ĐỘ LỚN CẢM ỨNG TỪ', sub: 'Vật lí 12 · Chương 3: Từ trường' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const cau = (s, k) => `<div style="padding-top:1mm;line-height:1.35">${s}</div>${lines(k)}`;
const dong = (s) => `<div style="margin:.3mm 0">${s}</div>`;
const Bm = m('B'), I = m('I'), l = m('l'), dm = m('\\Delta m'), F = m('F'), g = m('g');
const T_ = (s) => nw(m(`${s}\\ \\mathrm T`)), A = (s) => nw(m(`${s}\\ \\mathrm A`)), G = (s) => nw(m(`${s}\\ \\mathrm g`));
const dv = nw(`${dm}: kg · ${I}: A · ${l}: m · ${F}: N · ${Bm}: T`);
const gg = nw(m('g=9{,}81\\ \\mathrm{m/s^2}'));
const hang = nw(`${g} = ${m('9{,}81\\ \\mathrm{m/s^2}')} · 1 g = ${m('10^{-3}\\ \\mathrm{kg}')} · 1 cm = ${m('10^{-2}\\ \\mathrm m')}`);

const ttCss = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';

const p1 = `${ttCss}<section class="page">
${head('BÀI 11 · THỰC HÀNH: ĐO ĐỘ LỚN CẢM ỨNG TỪ', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${dong(`${ck}Lắp bộ cân dòng điện, đọc số cân, ghi bảng số liệu ${m('(I,\\ \\Delta m)')}`)}
${dong(`${ck}Tính ${Bm} từ từng lần đo và từ độ dốc đồ thị ${m('\\Delta m')}–${m('I')}`)}
${dong(`${ck}Ghi kết quả kèm sai số; nêu hai lỗi hay gặp và cách tránh`)}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Nhóm đặt nam châm chữ U lên đĩa cân, bấm TARE cho cân về 0,00 g. Khung dây treo trên giá riêng, cạnh dưới nằm trong khe nam châm nhưng không chạm cân hay nam châm. Đóng công tắc cho dòng điện chạy qua. Số chỉ của cân sẽ thế nào?</p>
<div class="fig-side" style="${fs(52)}"><div>
${opt('A', 'Không đổi, vì dây không chạm cân hay nam châm')}
${opt('B', 'Đổi đi một lượng nhỏ; đảo chiều dòng thì số chỉ đổi theo chiều ngược lại')}
${opt('C', 'Tăng thêm đúng bằng khối lượng của dây')}
${opt('D', 'Nhảy lung tung, vì từ trường làm cân hiển thị sai')}
<div style="margin-top:1mm">${chon(10)}</div>${wl('<span class="hint" style="font-weight:400">Vì sao?</span>', 2)}</div>
${H.soDo('Bố trí cân dòng điện. Số chỉ cân đã TARE về 0,00 g.')}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Nhắc lại: cân đo phản lực lên nam châm', '1·4')}
<div class="card" style="padding:1.2mm 3mm">
<div class="hint" style="margin-bottom:.4mm">Hằng số và đổi đơn vị: ${hang}</div>
<div>Dây dài ${l}, vuông góc đường sức, dòng ${I}: lực từ ${nw(`${F} = ${f(22)}`)}. Nam châm chịu ${f(18)} của lực này nên cân đọc ${nw(`${F} = ${f(22)}`)}.</div>
<div class="hint" style="margin:.3mm 0">Đơn vị: ${dv}</div>
<div>Từ hai biểu thức: ${nw(`${Bm} = ${f(30)}`)}</div></div>
${h3(5, 'Làm nhanh', '1·5')}
${box(cau(`Cạnh khung dài ${nw(m('l=5{,}0\\ \\mathrm{cm}'))}, dòng ${A('3{,}0')}; cân tăng ${G('1{,}84')}. Tính ${Bm}.`, 1))}
${foot(1)}</section>`;

const bangDc = (rows) => `<table><tr><th style="width:36mm">Dụng cụ</th><th>Đặt ở đâu · để làm gì</th></tr>${rows.map((x) => `<tr><td style="height:9.5mm">${x}</td><td></td></tr>`).join('')}</table>`;
const p2 = `<section class="page">
${head('DỤNG CỤ · BỐ TRÍ · GIÁ ĐỠ RIÊNG · ĐẢO CHIỀU DÒNG')}
${h3(1, 'II.2 · Dụng cụ và bố trí', '2·1')}
<div class="fig-side" style="${fs(60)}"><div>
${bangDc(['Cân điện tử, chia 0,01 g', 'Nam châm chữ U', 'Khung dây + giá đứng', 'Nguồn một chiều, biến trở', 'Ampe kế', 'Thước kẹp (đo l)'])}
</div>${H.soDo('Hình 1. Cân dòng điện: dây không đặt trên cân.')}</div>
${h3(2, 'Vì sao giá đỡ khung phải đứng riêng?', '2·2')}
<div class="card" style="padding:1.2mm 3mm">
<div>Một nhóm lỡ để chân giá đỡ khung tựa lên chính đĩa cân (cùng nam châm). Khi đóng mạch, số trên cân sẽ:</div>
${opt('A', 'tăng gấp đôi, vì cân đo cả lực lên dây lẫn lên nam châm')}
${opt('B', 'báo quá tải vì có thêm giá đỡ')}
${opt('C', 'vẫn chỉ đúng như trước, giá đỡ không ảnh hưởng')}
${opt('D', 'gần như vẫn 0,00 g, vì hai lực từ triệt tiêu trên cân')}
<div style="margin-top:.8mm">${chon(10)} &nbsp; Cân đo ${f(22)} lên mọi vật tựa trên bệ.</div></div>
${h3(3, 'Đảo chiều dòng điện', '2·3')}
<div class="card" style="padding:1.2mm 3mm">
<div>Dòng ${A('3{,}0')} thì cân chỉ ${G('+1{,}45')}. Giữ độ lớn, đảo hai đầu nguồn: cân chỉ ${nw(`${f(14)} g`)}. Ngắt mạch: cân chỉ ${nw(`${f(14)} g`)}.</div>
<div style="margin-top:.6mm">Khi tính ${Bm}, ta lấy ${nw(m('|\\Delta m|'))} vì ${f(40)}</div>${lines(2)}</div>
${h3(4, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '2·4')}
${rkHai([1, 2, 3, 4], [5, 6, 7, 8])}
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('CÁC BƯỚC ĐO · AN TOÀN · HAI CÁI BẪY SỐ LIỆU')}
${h3(1, 'II.3 · Các bước đo', '3·1')}
<div class="card" style="padding:1.2mm 3mm">
<div class="trap"><b>1.</b><span>Lắp theo Hình 1; đo ${l} bằng thước kẹp. Chưa có dòng thì bấm ${f(14)}, cân về 0,00 g.</span></div>
<div class="trap"><b>2.</b><span>Chỉnh biến trở tới ${nw(m('I=1{,}0\\ \\mathrm A'))}, đóng K, đợi số ổn định, đọc ${dm} (lần 1) rồi <b>ngắt K</b>; kiểm cân về 0,00 g.</span></div>
<div class="trap"><b>3.</b><span>Đóng lại, đọc lần 2. Đảo hai đầu nguồn, đóng K, đọc ${dm} đảo chiều, ngắt K.</span></div>
<div class="trap"><b>4.</b><span>Lặp ở 2,0; 3,0; 4,0; 5,0 A. Ghi vào bảng (tr. ${4 + OFF}). Tổng cộng ${f(8)} lần đóng K.</span></div>
<div class="trap"><b>5.</b><span>Tính ${Bm} từng hàng; vẽ đồ thị (tr. ${5 + OFF}); ước lượng sai số.</span></div>
<div style="margin-top:.6mm"><b>An toàn:</b> chỉ đóng K lúc đọc số, đọc xong ngắt ngay vì ${f(26)}</div></div>
${h3(2, 'III · Bẫy 1: “cân đo lực lên dây”', '3·2')}
<div class="card" style="padding:1.2mm 3mm">
<table><tr><th style="width:30mm">Vật</th><th style="width:30mm">Nằm trên cân?</th><th>Chịu lực nào?</th></tr>
<tr><td style="height:8mm"><b>Dây (khung)</b></td><td></td><td></td></tr>
<tr><td style="height:8mm"><b>Nam châm</b></td><td></td><td></td></tr></table>
<div style="margin-top:.8mm">Đóng mạch, cân tăng ${G('1{,}45')}. Lực từ lên dây hướng ${ck}lên &nbsp;${ck}xuống &nbsp;${ck}nằm ngang. Vì ${f(40)}</div>${lines(1)}</div>
${h3(3, 'III · Bẫy 2: dây không vuông góc đường sức', '3·3')}
<div class="fig-side" style="${fs(52)}"><div>
<div>Khi dây hợp đường sức góc ${m('\\theta')}: ${nw(`${F} = ${f(26)}`)}. Với ${nw(m('\\theta=90^\\circ'))}: ${f(8)} ${m('BIl')}; với ${nw(m('\\theta=60^\\circ'))}: ${f(10)} ${m('BIl')}.</div>
<div style="margin-top:.6mm">Nhóm để dây lệch ${nw(m('60^\\circ'))} nhưng vẫn dùng ${nw(m('B=\\dfrac{\\Delta m\\,g}{Il}'))}. ${Bm} tính ra ${ck}lớn hơn &nbsp;${ck}nhỏ hơn &nbsp;${ck}bằng ${Bm} thật, khoảng ${f(10)} %.</div></div>
${H.goc()}</div>
${K.btvn().replace('<i>1</i>', '<i>4</i>')}
${foot(3)}</section>`;

const bangSo = () => `<table class="tbl-ct" style="text-align:center">
<tr><th style="width:15mm;padding:.7mm .8mm">${I} (A)</th><th>${dm} thuận lần 1 (g)</th><th>${dm} thuận lần 2 (g)</th><th>${dm} đảo chiều (g)</th><th>${nw(m('|\\Delta m|'))} TB (g)</th><th>${Bm} (T)</th></tr>
${[0, 1, 2, 3, 4, 5].map((x) => `<tr><td style="height:8.5mm"><b>${x},0</b></td><td></td><td></td><td></td><td></td><td></td></tr>`).join('')}</table>`;
const nguyenNhan = ['Quên TARE: cân lệch +0,02 g', 'Chân giá đỡ tựa lên đĩa cân', `Dây lệch đường sức (${m('\\theta\\ne90^\\circ')})`, 'Đọc khi cân chưa ổn định, dây nóng', 'Quên đổi g sang kg, cm sang m'];
const p4 = `<section class="page">
${head('BẢNG SỐ LIỆU · SAI SỐ')}
${h3(1, 'II.4 · Số liệu nhóm em', '4·1')}
<div class="hint" style="margin-bottom:.8mm">${l} = ${f(14)} cm (thước kẹp) · ${hang}</div>
${bangSo()}
<div class="hint" style="margin:.8mm 0">Sai số dụng cụ: cân ${nw(m('\\pm0{,}01\\ \\mathrm g'))}; ampe kế ${nw(m('\\pm0{,}05\\ \\mathrm A'))}; thước kẹp ${nw(m('\\pm0{,}5\\ \\mathrm{mm}'))}. Công thức: ${nw(m('B=\\dfrac{\\Delta m\\,g}{Il}'))}.</div>
<div class="card soft" style="padding:1.2mm 3mm"><div><b>Quan sát:</b> ${I} tăng thì ${nw(`${m('|\\Delta m|')} ${f(14)}`)}; tỉ số ${nw(m('\\Delta m/I'))} ${ck}gần không đổi &nbsp;${ck}thay đổi nhiều.</div></div>
${h3(2, 'Sai số đến từ đâu, khắc phục thế nào?', '4·2')}
<div class="fig-side" style="${fs(52)}"><div>
<table><tr><th>Nguyên nhân</th><th style="width:40mm">Khắc phục</th></tr>${nguyenNhan.map((x) => `<tr><td style="height:8.5mm;font-size:var(--fs-sm)">${x}</td><td></td></tr>`).join('')}</table></div>
${H.soDo('Một nhóm bố trí như hình.', true)}</div>
${h3(3, 'Làm nhanh: sai số của một lần đo', '4·3')}
<div class="card" style="padding:1.2mm 3mm">
<div>${nw(m('l=4{,}0\\ \\mathrm{cm}=40\\ \\mathrm{mm}'))}, ${A('2{,}0')}, ${nw(m('\\Delta m=0{,}97\\ \\mathrm g'))}, ${nw(m('B=0{,}119\\ \\mathrm T'))}. Sai số: cân ${nw(m('0{,}01\\ \\mathrm g'))}; ampe kế ${nw(m('0{,}05\\ \\mathrm A'))}; thước kẹp ${nw(m('0{,}5\\ \\mathrm{mm}'))}.</div>
<div style="margin-top:.6mm">${nw(`${m('\\dfrac{\\Delta(\\Delta m)}{\\Delta m}=')} ${f(12)} %`)} · ${nw(`${m('\\dfrac{\\Delta I}{I}=')} ${f(12)} %`)} · ${nw(`${m('\\dfrac{\\Delta l}{l}=')} ${f(12)} %`)}</div>
<div style="margin-top:.6mm">${nw(`${m('\\dfrac{\\Delta B}{B}=')} ${f(14)} %`)} · ${nw(`${m('\\Delta B=')} ${f(14)} T`)}</div></div>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head(`ĐỒ THỊ ${m('\\Delta m')}–${m('I')} · SUY RA ${Bm} · BÁO CÁO`)}
${h3(1, `II.5 · Đồ thị ${m('\\Delta m')} theo ${m('I')} của nhóm em`, '5·1')}
<div style="width:106mm">${H.luoi()}</div>
${h3(2, `Suy ra ${Bm} từ độ dốc`, '5·2')}
<table style="text-align:center"><tr><th>Điểm A ${m('(I;\\Delta m)')}</th><th>Điểm B ${m('(I;\\Delta m)')}</th><th>Độ dốc ${m('k')} (g/A)</th><th>${Bm} = ${nw(m('\\dfrac{k\\,g}{l}'))} (T)</th></tr>
<tr><td style="height:9mm"></td><td></td><td></td><td></td></tr></table>
<div class="hint" style="margin:.5mm 0">Độ dốc ${nw(m('k=\\dfrac{\\Delta m_B-\\Delta m_A}{I_B-I_A}'))} (g/A) ứng với ${nw(m('k=\\dfrac{Bl}{g}'))}; đổi g sang kg, cm sang m trước khi thế.</div>
<div class="card soft" style="padding:1mm 3mm"><b>Kết quả:</b> ${nw(`${Bm} từ độ dốc = ${f(16)} T`)} · ${nw(`${Bm} trung bình từng hàng = ${f(16)} T`)} · ${nw(`${Bm} = (${f(12)} ± ${f(12)}) T`)}</div>
${h3(3, 'Câu hỏi báo cáo', '5·3')}
${box(`<div style="padding-top:.6mm"><b>1.</b> Cân đang đo lực nào, vì sao dây không đặt trên cân?</div>${lines(2)}
<div style="padding-top:.6mm"><b>2.</b> Đường thẳng có đi qua gốc không? Nếu cắt trục ${dm} ở +0,02 g thì nhóm đã quên bước nào?</div>${lines(2)}
<div style="padding-top:.6mm"><b>3.</b> Vì sao nên đo ở dòng lớn? Nêu một lỗi nhóm có thể mắc và cách tránh.</div>${lines(2)}`)}
${foot(5)}</section>`;

const tbDe = (Is, Ds) => `<table style="text-align:center;margin:.6mm 0"><tr><th style="width:21mm;text-align:left">Lần</th>${Is.map((_, i) => `<th>${i + 1}</th>`).join('')}</tr>`
  + `<tr><td style="text-align:left">${I} (A)</td>${Is.map((x) => `<td>${x}</td>`).join('')}</tr><tr><td style="text-align:left">${dm} (g)</td>${Ds.map((x) => `<td>${x}</td>`).join('')}</tr></table>`;
const dang = [
  { t: 'Dạng 1 · Dễ · Từ một lần đo: lực từ, cảm ứng từ và dấu số cân',
    de: `Cạnh khung dài ${nw(m('l=6{,}0\\ \\mathrm{cm}'))} nằm trong khe nam châm. Với ${A('2{,}5')}, cân tăng ${G('1{,}78')}. Lấy ${nw(m('g=9{,}81\\ \\mathrm{m/s^2}'))}.<br><b>a)</b> lực từ ${F}<br><b>b)</b> cảm ứng từ ${Bm}<br><b>c)</b> số chỉ cân khi đảo chiều dòng, giữ ${A('2{,}5')}`,
    nd: `${nw(`${F} = ${m('\\Delta m')} · ${f(10)}`)} (đổi g sang kg); ${nw(`${Bm} = ${f(20)}`)}; đảo chiều thì ${f(14)}`, a: ['a', 'b', 'c'], gi: 5, fig: H.soDo('Bố trí đo của đề.') },
  { t: 'Dạng 2 · Trung bình · Hai lỗi hệ thống: quên TARE, dây lệch đường sức',
    de: `Nhóm không bấm TARE, cân chỉ ban đầu ${G('+0{,}20')}. Với ${A('4{,}0')}, ${nw(m('l=4{,}0\\ \\mathrm{cm}'))}: đóng mạch cân chỉ ${G('+2{,}17')}; đảo chiều dòng cân chỉ ${G('-1{,}77')}. Lấy ${gg}.<br><b>a)</b> ${Bm} nếu nhóm dùng thẳng số chỉ ${G('2{,}17')}<br><b>b)</b> ${dm} đúng, tính bằng nửa hiệu hai số đọc<br><b>c)</b> ${Bm} đúng<br><b>d)</b> số a) lệch so với c) bao nhiêu phần trăm`,
    nd: `Nửa hiệu hai số đọc triệt ${f(14)}; ${nw(`${dm} = ${f(14)}`)}; lệch % = ${nw(`(${f(8)} − ${f(8)}) / ${f(8)}`)}`, a: ['a', 'b', 'c', 'd'], gi: 8 },
  { t: `Dạng 3 · Khó · Xử lí bảng số liệu: độ dốc đồ thị và ${Bm}`,
    de: `${nw(m('l=5{,}0\\ \\mathrm{cm}'))}, lấy ${gg}. Bảng số liệu (đã lấy trung bình hai chiều dòng):
${tbDe(['1,0', '2,0', '3,0', '4,0', '5,0'], ['0,61', '1,21', '1,84', '2,42', '3,07'])}Đường thẳng qua gốc có độ dốc ${nw(m('k=\\dfrac{\\sum I\\,\\Delta m}{\\sum I^2}'))}.<br><b>a)</b> ${nw(m('\\sum I\\,\\Delta m'))} và ${nw(m('\\sum I^2'))}<br><b>b)</b> độ dốc ${m('k')} (g/A)<br><b>c)</b> ${Bm} từ độ dốc`,
    nd: `${nw(`${m('k=')} ${f(14)}`)}; ${nw(`${Bm} = ${f(8)} · ${g} / ${f(8)}`)} (đổi g sang kg, cm sang m)`, a: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'], cot: 4, gi: 21 },
];

const oY = (s, o, w = {}) => s.split('<br>').map((p) => {
  const y = p.match(/^<b>([a-d])\)<\/b>/);
  if (!y) return `<div>${p}</div>`;
  const ls = o.filter((x) => x[0] === y[1]);
  return `<div class="yo"><span>${p}</span><span class="oo">${ls.map((x) => `<span class="nw"><b>${x})</b>${f(typeof w === 'object' ? (w[x] ?? 25) : w)}</span>`).join('')}</span></div>`;
}).join('');
const ttDe = (b) => b.fig ? `<div class="fig-side" style="grid-template-columns:1fr ${b.fw}mm">${`<div>${oY(b.de, b.o, b.ow)}</div>`}${b.fig}</div>` : oY(b.de, b.o, b.ow);
const vaoVo = (ds) => ds.map((b) => (b.o ? { t: b.t, de: ttDe(b), k: 0 } : b));
const nhap = (n) => ({ t: '<span class="nhap-t">Nháp / chỗ em còn vướng</span>', de: lines(n), k: 0 });
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–3', 'DẠNG 3 · ĐỌC ĐỒ THỊ'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Cạnh khung dài ${nw(m('l=5{,}0\\ \\mathrm{cm}'))}; với ${A('2{,}0')} cân tăng ${G('0{,}98')}. Lấy ${gg}.<br><b>a)</b> lực từ ${F}<br><b>b)</b> cảm ứng từ ${Bm}<br><b>c)</b> số chỉ cân khi đảo chiều dòng`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 1 · Bài 2', de: `Một nam châm khác: ${nw(m('l=3{,}0\\ \\mathrm{cm}'))}, ${A('4{,}0')}, cân tăng ${G('1{,}42')}. Lấy ${gg}.<br><b>a)</b> lực từ ${F}<br><b>b)</b> cảm ứng từ ${Bm}<br><b>c)</b> số chỉ cân khi đảo chiều dòng`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 2 · Bài 1 (quên TARE)', de: `Không bấm TARE, cân chỉ ban đầu ${G('+0{,}30')}. ${A('3{,}0')}, ${nw(m('l=5{,}0\\ \\mathrm{cm}'))}: đóng mạch cân chỉ ${G('+2{,}14')}; đảo chiều cân chỉ ${G('-1{,}54')}. Lấy ${gg}.<br><b>a)</b> ${dm} đúng (nửa hiệu hai số đọc)<br><b>b)</b> ${Bm} đúng<br><b>c)</b> ${Bm} nếu dùng thẳng ${G('2{,}14')}, lệch bao nhiêu %`, o: ['a', 'b', 'c<sub>1</sub>', 'c<sub>2</sub>'], ow: { 'c<sub>2</sub>': 18 } },
    { t: 'Dạng 2 · Bài 2 (dây lệch)', de: `Dây hợp đường sức góc ${nw(m('30^\\circ'))}; ${A('2{,}0')}, ${nw(m('l=4{,}0\\ \\mathrm{cm}'))}, cân tăng ${G('0{,}61')}. Lực từ ${nw(m('F=BIl\\sin\\theta'))}; lấy ${gg}.<br><b>a)</b> ${Bm} nếu nhóm dùng công thức vuông góc<br><b>b)</b> ${Bm} thật<br><b>c)</b> ${Bm} ở a) nhỏ hơn thật bao nhiêu %`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 3 · Bài 1', de: `${nw(m('l=4{,}0\\ \\mathrm{cm}'))}, lấy ${gg}; bảng số liệu một nam châm:${tbDe(['1,0', '2,0', '3,0', '4,0', '5,0'], ['0,52', '0,98', '1,49', '1,95', '2,47'])}<br><b>a)</b> ${nw(m('\\sum I\\,\\Delta m'))}; ${nw(m('\\sum I^2'))}<br><b>b)</b> độ dốc ${nw(m('k=\\dfrac{\\sum I\\,\\Delta m}{\\sum I^2}'))} (g/A)<br><b>c)</b> ${Bm} từ độ dốc`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'], ow: { 'a<sub>1</sub>': 18, 'a<sub>2</sub>': 18 } },
  ], [
    { t: 'Dạng 3 · Bài 2', de: `${nw(m('l=6{,}0\\ \\mathrm{cm}'))}, lấy ${gg}; bảng số liệu một nam châm khác:${tbDe(['1,0', '2,0', '3,0', '4,0', '5,0'], ['0,51', '1,03', '1,52', '2,06', '2,55'])}<br><b>a)</b> ${nw(m('\\sum I\\,\\Delta m'))}; ${nw(m('\\sum I^2'))}<br><b>b)</b> độ dốc ${nw(m('k=\\dfrac{\\sum I\\,\\Delta m}{\\sum I^2}'))} (g/A)<br><b>c)</b> ${Bm} từ độ dốc`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b', 'c'], ow: { 'a<sub>1</sub>': 18, 'a<sub>2</sub>': 18 } },
    { t: 'Đọc đồ thị', de: `<div class="fig-side" style="grid-template-columns:1fr 44mm"><div>Hai nam châm dùng chung một khung dây; đường (1) và (2) là đồ thị ${dm}–${I}. Nam châm nào có ${Bm} lớn hơn? Vì sao?${lines(3)}</div>${H.haiDuong()}</div>`, k: 0 },
    nhap(16),
  ]],
  dap: [
    `D1·1: a) 9,61·10<sup>−3</sup> N · b) 0,096 T · c) −0,98 g &nbsp;|&nbsp; D1·2: a) 1,39·10<sup>−2</sup> N · b) 0,116 T · c) −1,42 g &nbsp;|&nbsp; D2·1: a) 1,84 g · b) 0,120 T · c<sub>1</sub>) 0,140 T · c<sub>2</sub>) 16 % &nbsp;|&nbsp; D2·2: a) 0,075 T · b) 0,150 T · c) 50 % &nbsp;|&nbsp; D3·1: a<sub>1</sub>) 27,1 g·A · a<sub>2</sub>) 55 A² · b) 0,493 g/A · c) 0,121 T`,
    `D3·2: a<sub>1</sub>) 28,12 g·A · a<sub>2</sub>) 55 A² · b) 0,511 g/A · c) 0,084 T &nbsp;|&nbsp; Đọc đồ thị: nam châm (1), đường dốc hơn (k = Bl/g)`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [2, 1], kq: [[1, 2], [3]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'nguyên lý 1·4 · dụng cụ 2·1 · giá đỡ 2·2 · các bước 3·1 · bẫy 3·2–3·3 · bảng số liệu 4·1 · sai số 4·2 · đồ thị 5·1 · dạng 1–2: 6·1 · dạng 3: 7·1',
  out: resolve(dirname(fileURLToPath(import.meta.url)), 'out/ruot-tap-vl12-c3-bai11.pdf'),
});
