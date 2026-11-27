// Ruột tập VL12 – Bài 17 · Hiện tượng phóng xạ (lesson id 18). Khung: khung.mjs; hình: hinh-ch4.mjs.
// Chạy: node scripts/ruot-tap/bai17.mjs [file.pdf] → scripts/ruot-tap/out/ruot-tap-vl12-bai17.pdf
import { khoiTao, m, lines, wl, fill as f, nw, exp, ck, box, opt, chon, rkHai, hinh } from './khung.mjs';
const K = khoiTao({ bai: 20, baiDau: 17, lid: 18, ten: 'HIỆN TƯỢNG PHÓNG XẠ' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;

// Bài tương tự giải vào vở (thầy chốt 10/11): ô đáp số đặt cuối dòng của từng ý (CSS .yo như l10-bai23.mjs).
const ttCss = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';
const p1 = `${ttCss}<section class="page">
${head('BÀI 20 · HIỆN TƯỢNG PHÓNG XẠ', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
<div style="margin:.3mm 0">${ck}Nêu được phóng xạ: <b>tự phát, ngẫu nhiên</b>, không phụ thuộc bên ngoài</div>
<div style="margin:.3mm 0">${ck}Phân biệt <b>${m('\\alpha,\\ \\beta^-,\\ \\beta^+,\\ \\gamma')}</b> và viết phương trình phân rã</div>
<div style="margin:.3mm 0">${ck}Dùng <b>chu kì bán rã</b> ${m('T')}, hằng số ${m('\\lambda')}, độ phóng xạ ${m('H')} (Bq, Ci)</div>
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Nhúng mẫu phóng xạ vào nitơ lỏng ${m('-196\\ ^\\circ\\mathrm{C}')} thì nhịp đếm của máy thay đổi thế nào?</p>
<div class="fig-side" style="${fs(52)}"><div>
${opt('A', 'Chậm đi hẳn, vì lạnh làm phản ứng chậm lại')}
${opt('B', 'Chậm đi, vì hạt nhân co lại khi lạnh')}
${opt('C', 'Không đổi')}
<div style="margin-top:1mm">${chon(10)}</div><div class="hint">Vì sao?</div>${lines(1)}</div>
${hinh.maDem('Nitơ lỏng bao quanh nguồn, ống đếm vẫn ghi xung.')}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Phóng xạ là gì', '1·4')}
<div class="card" style="padding:1.2mm 3mm">
<div>Hạt nhân không ${f(10)} tự ${f(10)}, phát ra ${f(10)} (tia) và biến thành hạt nhân ${f(10)}.</div>
<div>Hạt nhân mẹ ${m('{}^{A}_{Z}\\mathrm{X}')} → ${f(14)} + hạt nhân con ${m('{}^{A\'}_{Z\'}\\mathrm{Y}')}</div>
<div>Tự ${f(10)} (không cần kích thích) · ${f(12)} (không đoán được hạt nào) · không phụ thuộc ${f(24)}.</div>
<div>Đồng vị phóng xạ: tự nhiên ${f(16)}; nhân tạo ${f(16)}.</div></div>
${h3(5, 'Thí nghiệm: đếm xung của một nguồn', '1·5')}
<div class="card" style="padding:1.2mm 3mm">
<div>Năm lần đếm 1 phút: 512, 486, 531, 497, 505. Trung bình ${f(14)}; trừ phông nền 23 còn ${f(14)} xung/phút.</div>
<div>Từng phút thì ${f(14)}, nhưng nhịp trung bình thì ${f(14)}. Sai số cỡ ${nw(`±&nbsp;${f(8)}`)} xung/phút, vì thăng giáng ${f(14)}.</div></div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('BỐN LOẠI TIA · CHU KÌ BÁN RÃ · ĐỘ PHÓNG XẠ')}
${h3(1, 'II.2 · Bản chất bốn loại tia', '2·1')}
<div class="card fig-side" style="${fs(56)};padding:1.2mm 3mm"><div>
<div>${m('\\alpha')}: hạt nhân ${f(12)}; ion hoá ${f(10)}; xuyên ${f(10)}; lệch về bản ${f(8)}.</div>
<div>${m('\\beta^-')}: ${f(14)} ${m('{}^{0}_{-1}e')}; lệch về bản ${f(8)}.</div>
<div>${m('\\beta^+')}: ${f(14)} ${m('{}^{0}_{1}e')}; lệch về bản ${f(8)}.</div>
<div>${m('\\gamma')}: sóng ${f(16)}; xuyên ${f(10)}; ${f(8)} lệch.</div></div>
${hinh.batTia('Trong điện trường: α lệch về bản âm, β⁻ lệch về bản dương (nhiều hơn), γ không lệch.')}</div>
${h3(2, 'Phương trình và dịch chuyển ô', '2·2')}
<div class="card fig-side" style="${fs(56)};padding:1.2mm 3mm"><div>
<div>${m('\\alpha')} (${m('{}^{4}_{2}\\mathrm{He}')}): ${m('A_Y=')} ${f(8)}, ${m('Z_Y=')} ${f(8)} → con lùi ${f(5)} ô</div>
<div>${m('\\beta^-')} (${m('{}^{0}_{-1}e')}): ${m('A_Y=')} ${f(8)}, ${m('Z_Y=')} ${f(8)} → tiến ${f(5)} ô</div>
<div>${m('\\beta^+')} (${m('{}^{0}_{1}e')}): ${m('A_Y=')} ${f(8)}, ${m('Z_Y=')} ${f(8)} → lùi ${f(5)} ô</div>
<div>${m('\\gamma')}: hạt nhân con còn ở trạng thái ${f(14)}, ${m('Z,A')} ${f(10)}.</div></div>
${hinh.dichChuyenO('Hạt nhân con ở ô nào so với hạt nhân mẹ (ô Z)?')}</div>
${h3(3, 'II.3 · Định luật phóng xạ', '2·3')}
<div class="card fig-side" style="${fs(52)};padding:1.2mm 3mm"><div>
<div>${m('T')}: thời gian còn ${f(12)} số hạt.</div>
<div>${m('N_t=N_0\\cdot')} ${f(14)}</div>
<div>${m('m_t=')} ${f(16)}</div>
<div>${m('H_t=')} ${f(16)}</div>
<div>${m('\\Delta N=')} ${f(24)}</div>
<div>${m('\\lambda=')} ${f(10)} / ${m('T')} ≈ ${f(10)} / ${m('T')}</div>
<div>${m('N_0=\\dfrac{m_0}{A}\\cdot')} ${f(10)}</div>
<div>Sau ${m('T,\\,2T,\\,3T')}: còn ${f(8)}, ${f(8)}, ${f(8)}; đã rã ${f(8)}, ${f(8)}, ${f(8)}.</div></div>
${hinh.phanRaMu('Mỗi T còn một nửa. Điền tỉ lệ còn lại ở các mốc.')}</div>
${h3(4, 'II.4 · Độ phóng xạ', '2·4')}
<div class="card" style="padding:1.2mm 3mm">
<div>${m('H=')} ${f(10)} · ${f(8)} &nbsp;·&nbsp; số phân rã trong ${f(10)} &nbsp;·&nbsp; ${m('1\\ \\mathrm{Bq}=')} ${f(16)} &nbsp;·&nbsp; ${m('1\\ \\mathrm{Ci}=')} ${nw(`${f(14)}&nbsp;Bq`)}</div>
<div>Đổi Bq ra Ci thì con số phải ${f(10)} đi (Ci rất ${f(10)}). Đo mức mạnh hay yếu, <b>không</b> đo mức ${f(14)}.</div></div>
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('BẪY · TRẢ BÀI · KẾT QUẢ TỰ KIỂM TRA')}
${h3(1, 'III · Ba cái bẫy hay sập', '3·1')}
<div class="card" style="padding:1mm 3mm">
<div class="trap">${ck}<span><b>“Sau một chu kì là phân rã hết.”</b> “Bán rã” = một nửa; mẫu không bao giờ hết đúng.</span></div>
<div class="trap">${ck}<span><b>“Độ phóng xạ ${m('H')} và chu kì ${m('T')} là một.”</b> ${m('H')} phụ thuộc lượng chất; ${m('T')} thì không.</span></div>
<div class="trap">${ck}<span><b>“Nhầm chiều dịch ô.”</b> ${m('\\alpha')}: ${m('A-4,\\ Z-2')}; ${m('\\beta^-')}: ${m('A')} giữ, ${m('Z+1')}.</span></div></div>
${h3(2, 'IV · Trả bài 6 câu', '3·2')}
${box(`${tb('1. Phóng xạ là gì? Vì sao tự phát, ngẫu nhiên?')}${lines(2)}
${tb('2. Bản chất bốn loại tia và chỗ dịch chuyển của hạt nhân con?')}${lines(2)}
${tb('3. Phát biểu định luật phóng xạ, viết công thức N, m, H.')}${lines(2)}
${tb('4. Chu kì bán rã là gì? Hệ thức với hằng số phóng xạ λ?')}${lines(2)}
${tb('5. Độ phóng xạ là gì, đơn vị, liên hệ với số hạt nhân?')}${lines(2)}
${tb('6. Vì sao phóng xạ là ngẫu nhiên, và lộ ra thế nào khi đo?')}${lines(2)}`)}
<div class="card soft" style="margin-top:1.5mm;padding:1mm 3mm"><b>Bạn cùng bàn kiểm:</b> nói được ……/6 câu · câu chưa thuộc: ${f(30)} → đọc lại ô Tập ${f(14)}</div>
${h3(3, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '3·3')}
${rkHai([2, 3, 4, 5], [6, 7, 8])}
<div class="card soft" style="margin-top:1mm;padding:1mm 3mm"><b>Đề cuối tiết 1194:</b> điểm ……/20 &nbsp;· câu sai: <span class="fill" style="min-width:30mm"></span></div>
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('BÀI TOÁN MẪU · MẪU NA-24 TRONG Y HỌC')}
${h3(1, 'V · Đề bài', '4')}
<div class="card soft" style="padding:1.2mm 3mm">Mẫu ${m('{}^{24}_{11}\\mathrm{Na}')}, ${m('T=15\\ \\mathrm{h}')}, ban đầu ${m('N_0=1{,}2\\cdot10^{15}')} hạt nhân.
<div><b>a)</b> Viết phương trình phân rã ${m('\\beta^-')}; hạt nhân con tiến hay lùi mấy ô?</div><div><b>b)</b> Tính ${m('\\lambda')} (${m('1/\\mathrm{s}')}).</div><div><b>c)</b> Sau 45 giờ còn bao nhiêu hạt nhân, đã rã bao nhiêu phần trăm?</div><div><b>d)</b> Tính ${m('H_0')} và độ phóng xạ còn lại sau 45 giờ.</div><div><b>e)</b> Đổi ${m('H_0')} ra curi.</div></div>
${h3(2, 'Phân tích đề (điền cùng thầy)')}
<table><tr><th style="width:42mm">Câu trong đề</th><th style="width:40mm">Dữ liệu</th><th>Kiến thức liên quan</th></tr>
<tr><td>“${m('{}^{24}_{11}\\mathrm{Na}')}”</td><td>${m('A=24,\\ Z=11')}</td><td>${m('\\beta^-')}: ${m('Z+1')}</td></tr>
<tr><td style="height:6.5mm">“${m('T=15')} giờ”</td><td></td><td></td></tr>
<tr><td style="height:6.5mm">“sau 45 giờ”</td><td></td><td></td></tr>
<tr><td style="height:6.5mm">“độ phóng xạ… ra curi”</td><td></td><td></td></tr></table>
${h3(3, 'Giải')}
<div class="fig-side" style="${fs(52)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl('a)', 2)}${wl('b)', 2)}${wl('c)', 3)}${wl('d)', 3)}${wl('e)', 1)}</div>${hinh.na24('T = 15 giờ: sau 45 giờ là mấy chu kì? Còn lại bao nhiêu?')}</div>
${h3(4, 'Mở rộng: cũng mẫu đó, sau 60 giờ')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div class="ln" style="height:auto;padding-top:1mm"><b>Bước 1 (cho sẵn):</b> ${m('n=t/T=60/15=4')}, vậy ${m('N=N_0/16')}.</div>
${wl('Bước 2: N = …', 1)}${wl('Bước 3: H còn lại tính từ H₀ thế nào?', 2)}</div>
<div class="card soft" style="margin-top:1.5mm;padding:1mm 3mm"><b>Em tự kiểm:</b> ${ck}đổi giờ ra giây &nbsp;${ck}A, Z hai vế khớp &nbsp;${ck}có ghi đơn vị</div>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TẬP VỀ NHÀ · MANG VỀ · THỬ THÁCH')}
${K.btvn()}
${h3(2, 'VI · Mang về: điều em dễ quên nhất', '5')}
${box(wl('1.', 2) + wl('2.', 2) + wl('3.', 2))}
${h3(3, 'Thử thách phân tầng')}
<div class="fig-side" style="${fs(46)}">${box(wl('★ N₀ = 6·10²⁰ hạt, T = 5 năm. Sau 10 năm còn:', 2)
 + wl('★★ Vì sao nhiệt độ, axit không xử lí được chất thải phóng xạ?', 3)
 + wl('★★★ Xương cổ còn 1/8 lượng C-14: tuổi? Nêu một giả thiết về lượng C-14 ban đầu có thể sai:', 4))}<div style="display:grid;gap:2mm">${hinh.chiaDoiMau('Chia mẫu làm hai: N và H giảm một nửa, còn T thì sao?')}${hinh.anh('phong-xa-do-thi-ln-r.png', 'Đồ thị ln R theo t (R: số phân rã/giây) là đường thẳng, độ dốc = −λ (I-128: λ ≈ 0,0276/phút, T ≈ 25 phút). (Halliday 42.3.1)')}</div></div>
${h3(4, 'Câu 7, câu 8 (C-14)')}
${box(wl('Câu 7: I-131, T = 8 ngày, sau 16 ngày còn … %', 2) + wl('Câu 8: vì sao C-14 chỉ định tuổi được tới vài chục nghìn năm?', 2))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Chuỗi phân rã α rồi hai lần β⁻',
    de: `${m('{}^{238}_{92}\\mathrm{U}\\xrightarrow{\\alpha}\\mathrm{X}\\xrightarrow{\\beta^-}\\mathrm{Y}\\xrightarrow{\\beta^-}\\mathrm{W}')}.<br><b>a)</b> ${m('A,\\ Z')} của X, Y, W<br><b>b)</b> W đứng ô nào so với U; số khối đổi thế nào`,
    nd: `Mỗi tia: ${m('\\alpha')} lùi ${f(5)} ô, ${m('\\beta^-')} tiến ${f(5)} ô; số khối chỉ ${m('\\alpha')} làm đổi (giảm ${f(5)})`, a: ['a', 'b'], gi: 3, fig: 'chuoiU' },
  { t: 'Dạng 2 · Trung bình · Số hạt nhân còn lại sau n chu kì',
    de: `${m('N_0=6{,}4\\cdot10^{18}')} hạt ${m('{}^{210}_{84}\\mathrm{Po}')}, ${m('T=138')} ngày.<br><b>a)</b> còn bao nhiêu hạt sau 552 ngày<br><b>b)</b> bao nhiêu % đã phân rã<br><b>c)</b> sau 759 ngày còn bao nhiêu % số ban đầu`,
    nd: `Tìm ${m('n=t/T')} = ${f(8)}; còn lại ${m('N_0/2^n')}; đã rã = ${f(10)} − còn lại`, a: ['a', 'b', 'c'], gi: 0 },
  { t: 'Dạng 3 · Trung bình · Tìm T từ phần đã phân rã',
    de: `Iốt-131, ${m('m_0=64\\ \\mu\\mathrm{g}')}; sau 24 ngày đã rã ${m('56\\ \\mu\\mathrm{g}')}.<br><b>a)</b> chu kì ${m('T')}<br><b>b)</b> khối lượng còn sau 40 ngày<br><b>c)</b> sau ít nhất bao nhiêu ngày thì còn dưới ${m('0{,}1\\ \\mu\\mathrm{g}')} (gợi ý: ${m('\\log_2x=\\ln x/\\ln2')})`,
    nd: `Cho phần đã rã → phần còn ${m('m_0-')} ${f(8)}, ${m('m_t/m_0=2^{-n}')} ⇒ ${m('n=')} ${f(8)} ⇒ ${m('T=t/n')}`, a: ['a', 'b', 'c'], gi: 5 },
  { t: 'Dạng 4 · Khó · Độ phóng xạ nguồn xạ trị Co-60',
    de: `${m('4{,}0\\ \\mathrm{g}')} ${m('{}^{60}_{27}\\mathrm{Co}')}, ${m('T=5{,}27')} năm (1 năm = 365 ngày), ${m('N_A=6{,}022\\cdot10^{23}')}, ${m('M=60\\ \\mathrm{g/mol}')}.<br><b>a)</b> ${m('N_0')} và ${m('\\lambda')} (${m('1/\\mathrm{s}')})<br><b>b)</b> ${m('H_0')} theo Bq và Ci<br><b>c)</b> ${m('H')} sau 10,54 năm (Ci)`,
    nd: `${m('N_0=')} ${f(8)} ${m('\\cdot N_A')}; ${m('\\lambda=')} ${f(8)} / ${f(6)} (đổi ${f(6)} ra giây); ${m('H=')} ${f(8)}`, a: ['a', 'b', 'c'], gi: 6 },
  { t: 'Dạng 5 · Nâng cao · Định tuổi bằng carbon-14',
    de: `Cây sống ${m('0{,}226\\ \\mathrm{Bq/g}')} C; ${m('T=5730')} năm. Mẩu than ${m('5{,}0\\ \\mathrm{g}')} C đo được ${m('0{,}360\\ \\mathrm{Bq}')}.<br><b>a)</b> độ phóng xạ riêng ${m('h')} và ${m('h/h_0')}<br><b>b)</b> tuổi mẩu than<br><b>c)</b> lẫn carbon hiện đại: tuổi tính ra lớn hay nhỏ hơn thật?`,
    nd: `So hai mẫu cùng đơn vị Bq/g: ${m('h/h_0=2^{-n}')} ⇒ ${m('n=')} ${f(8)} ⇒ ${m('t=nT')}`, a: ['a', 'b', 'c'], gi: 5, fig: 'c14' },
];

// Bài tương tự: mỗi dạng 2 bài, đáp số tính bằng Python 16/11/2026 (ln2, N_A = 6,022·10²³, 1 năm = 365 ngày, 1 Ci = 3,7·10¹⁰ Bq).
const oY = (s, o, w = 25) => s.split('<br>').map((p) => {
  const y = p.match(/^<b>([a-d])\)<\/b>/);
  if (!y) return `<div>${p}</div>`;
  const ls = o.filter((l) => l[0] === y[1]);
  return `<div class="yo"><span>${p}</span><span class="oo">${ls.map((l) => `<span class="nw"><b>${l})</b>${f(w)}</span>`).join('')}</span></div>`;
}).join('');
const vaoVo = (ds) => ds.map((b) => (b.o ? { t: b.t, de: oY(b.de, b.o, b.ow), k: 0 } : b));
const nhap = (n) => ({ t: '<span class="nhap-t">Nháp / chỗ em còn vướng</span>', de: lines(n), k: 0 });
const s1 = '<sub>1</sub>', s2 = '<sub>2</sub>';
const ci = `${nw(m('1\\ \\mathrm{Ci}=3{,}7\\cdot10^{10}\\ \\mathrm{Bq}'))}`, na = nw(m('N_A=6{,}022\\cdot10^{23}\\ \\mathrm{mol^{-1}}'));
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–3', 'DẠNG 4–5'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `${m('{}^{232}_{90}\\mathrm{Th}\\xrightarrow{\\alpha}\\mathrm{X}\\xrightarrow{\\beta^-}\\mathrm{Y}\\xrightarrow{\\beta^-}\\mathrm{W}')}.<br><b>a)</b> ${m('A,\\ Z')} của X<br><b>b)</b> ${m('A,\\ Z')} của Y<br><b>c)</b> ${m('A,\\ Z')} của W<br><b>d)</b> W đứng ô nào so với Th; số khối đổi thế nào`, o: ['a', 'b', 'c', `d${s1}`, `d${s2}`] },
    { t: 'Dạng 1 · Bài 2', de: `Chuỗi phân rã biến ${m('{}^{226}_{88}\\mathrm{Ra}')} thành ${m('{}^{210}_{82}\\mathrm{Pb}')} chỉ gồm các phân rã ${m('\\alpha')} và ${m('\\beta^-')}.<br><b>a)</b> số lần phân rã ${m('\\alpha')}<br><b>b)</b> số lần phân rã ${m('\\beta^-')}`, o: ['a', 'b'], ow: 14 },
    { t: 'Dạng 2 · Bài 1', de: `${m('N_0=8{,}0\\cdot10^{16}')} hạt ${m('{}^{222}_{86}\\mathrm{Rn}')}, ${nw(`${m('T=3{,}8')} ngày`)}.<br><b>a)</b> còn bao nhiêu hạt sau 15,2 ngày<br><b>b)</b> bao nhiêu % đã phân rã<br><b>c)</b> sau 20,9 ngày còn bao nhiêu % số ban đầu`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 2 · Bài 2', de: `${m('N_0=4{,}8\\cdot10^{21}')} hạt ${m('{}^{137}_{55}\\mathrm{Cs}')}, ${nw(`${m('T=30')} năm`)}.<br><b>a)</b> còn bao nhiêu hạt sau 90 năm<br><b>b)</b> bao nhiêu % đã phân rã<br><b>c)</b> sau 45 năm còn bao nhiêu % số ban đầu`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 3 · Bài 1', de: `Phốt pho-32, ${nw(m('m_0=80\\ \\mu\\mathrm{g}'))}; sau 42,9 ngày đã rã ${nw(`${m('70\\ \\mu\\mathrm{g}')}.`)}<br><b>a)</b> chu kì ${m('T')}<br><b>b)</b> khối lượng còn sau 100 ngày<br><b>c)</b> sau ít nhất bao nhiêu ngày thì còn dưới ${m('0{,}5\\ \\mu\\mathrm{g}')} (gợi ý: ${nw(m('\\log_2x=\\ln x/\\ln2'))})`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 3 · Bài 2', de: `Radon-222, ${nw(m('m_0=48\\ \\mathrm{mg}'))}; sau 11,4 ngày đã rã ${nw(`${m('42\\ \\mathrm{mg}')}.`)}<br><b>a)</b> chu kì ${m('T')}<br><b>b)</b> khối lượng còn sau 19 ngày<br><b>c)</b> sau bao lâu thì chỉ còn ${m('1\\,\\%')} khối lượng ban đầu`, o: ['a', 'b', 'c'] },
    nhap(1),
  ], [
    { t: 'Dạng 4 · Bài 1', de: `${m('1{,}0\\ \\mathrm{g}')} ${m('{}^{226}_{88}\\mathrm{Ra}')}, ${nw(`${m('T=1600')} năm`)} (1 năm = 365 ngày), ${na}, ${nw(m('M=226\\ \\mathrm{g/mol}'))}, ${nw(`${ci}.`)}<br><b>a)</b> ${m('N_0')} và ${m('\\lambda')} (${m('1/\\mathrm{s}')})<br><b>b)</b> ${m('H_0')} theo Bq và Ci<br><b>c)</b> ${m('H')} sau 3200 năm (Ci)`, o: [`a${s1}`, `a${s2}`, `b${s1}`, `b${s2}`, 'c'] },
    { t: 'Dạng 4 · Bài 2', de: `${m('2{,}0\\ \\mathrm{mg}')} ${m('{}^{131}_{53}\\mathrm{I}')} dùng chẩn đoán tuyến giáp, ${nw(`${m('T=8{,}0')} ngày`)}, ${na}, ${nw(m('M=131\\ \\mathrm{g/mol}'))}, ${nw(`${ci}.`)}<br><b>a)</b> ${m('N_0')} và ${m('\\lambda')} (${m('1/\\mathrm{s}')})<br><b>b)</b> ${m('H_0')} theo Bq và Ci<br><b>c)</b> ${m('H')} sau 24 ngày (Ci)`, o: [`a${s1}`, `a${s2}`, `b${s1}`, `b${s2}`, 'c'] },
    { t: 'Dạng 5 · Bài 1', de: `Cây sống ${nw(m('0{,}226\\ \\mathrm{Bq/g}'))} C; ${nw(`${m('T=5730')} năm`)}. Mẩu gỗ cổ chứa ${m('10\\ \\mathrm{g}')} C đo được ${nw(`${m('0{,}565\\ \\mathrm{Bq}')}.`)}<br><b>a)</b> độ phóng xạ riêng ${m('h')} và ${m('h/h_0')}<br><b>b)</b> tuổi mẩu gỗ<br><b>c)</b> mẫu lẫn carbon từ than đá (không còn C-14): tuổi tính ra lớn hay nhỏ hơn thật?`, o: [`a${s1}`, `a${s2}`, 'b', 'c'] },
    { t: 'Dạng 5 · Bài 2', de: `Cây sống ${nw(m('0{,}226\\ \\mathrm{Bq/g}'))} C; ${nw(`${m('T=5730')} năm`)}. Mẩu xương chứa ${m('12\\ \\mathrm{g}')} C đo được ${nw(`${m('1{,}6\\ \\mathrm{Bq}')}.`)}<br><b>a)</b> độ phóng xạ riêng ${m('h')} và ${m('h/h_0')}<br><b>b)</b> tuổi mẩu xương<br><b>c)</b> quên trừ phông nền (số đếm dư): tuổi tính ra lớn hay nhỏ hơn thật?`, o: [`a${s1}`, `a${s2}`, 'b', 'c'] },
    nhap(9),
  ]],
  dap: [
    `D1·1: a) X: A = 228, Z = 88 · b) Y: 228, 89 · c) W: 228, 90 · d${s1}) cùng ô với Th (đồng vị) · d${s2}) giảm 4 &nbsp;|&nbsp; D1·2: a) 4 · b) 2 &nbsp;|&nbsp; D2·1: a) ${nw('5,0·10<sup>15</sup>')} · b) 93,75 % · c) 2,21 % &nbsp;|&nbsp; D2·2: a) ${nw('6,0·10<sup>20</sup>')} · b) 87,5 % · c) 35,4 % &nbsp;|&nbsp; D3·1: a) 14,3 ngày · b) 0,628 µg · c) 104,7 ngày (≈ 105 ngày) &nbsp;|&nbsp; D3·2: a) 3,8 ngày · b) 1,5 mg · c) 25,2 ngày`,
    `D4·1: a${s1}) ${nw('2,66·10<sup>21</sup>')} · a${s2}) ${nw('1,37·10<sup>−11</sup> s<sup>−1</sup>')} · b${s1}) ${nw('3,66·10<sup>10</sup> Bq')} · b${s2}) 0,989 Ci · c) 0,247 Ci &nbsp;|&nbsp; D4·2: a${s1}) ${nw('9,19·10<sup>18</sup>')} · a${s2}) ${nw('1,00·10<sup>−6</sup> s<sup>−1</sup>')} · b${s1}) ${nw('9,22·10<sup>12</sup> Bq')} · b${s2}) 249 Ci · c) 31,1 Ci &nbsp;|&nbsp; D5·1: a${s1}) 0,0565 Bq/g · a${s2}) 0,25 · b) 11 460 năm · c) lớn hơn &nbsp;|&nbsp; D5·2: a${s1}) 0,133 Bq/g · a${s2}) 0,590 · b) ≈ 4360 năm · c) nhỏ hơn`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 2], kq: [[1, 2, 3], [4, 5]] },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'phóng xạ 1·4 · đếm xung 1·5 · bốn loại tia 2·1 · dịch ô 2·2 · định luật phóng xạ 2·3 · độ phóng xạ 2·4 · bẫy 3·1 · dạng 1–3 → 6·1 · dạng 4–5 → 7·1',
  out: process.argv[2],
});
