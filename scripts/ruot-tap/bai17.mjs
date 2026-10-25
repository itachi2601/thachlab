// Ruột tập VL12 – Bài 17 · Hiện tượng phóng xạ (lesson id 18). Khung: khung.mjs; hình: hinh-ch4.mjs.
// Chạy: node scripts/ruot-tap/bai17.mjs [file.pdf] → scripts/ruot-tap/out/ruot-tap-vl12-bai17.pdf
import { khoiTao, m, lines, wl, fill as f, nw, exp, ck, box, opt, chon, rkHai, hinh } from './khung.mjs';
const K = khoiTao({ bai: 17, lid: 18, ten: 'HIỆN TƯỢNG PHÓNG XẠ' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;

const p1 = `<section class="page">
${head('BÀI 17 · HIỆN TƯỢNG PHÓNG XẠ', K.sub)}
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
<div>Hạt nhân không ${f(10)} tự ${f(10)}, phát tia và biến thành hạt nhân ${f(10)}: ${m('{}^{A}_{Z}\\mathrm{X}\\to')} ${f(10)} + ${m('{}^{A\'}_{Z\'}\\mathrm{Y}')}</div>
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
<div>${m('T')}: thời gian còn ${f(12)}. &nbsp;${m('N_t=N_0\\cdot')} ${f(14)}</div>
<div>${m('m_t=')} ${f(16)} &nbsp;·&nbsp; ${m('H_t=')} ${f(16)}</div>
<div>${m('\\Delta N=')} ${f(24)}</div>
<div>${m('\\lambda=')} ${f(10)} / ${f(6)} ≈ ${f(10)} / ${m('T')} &nbsp;·&nbsp; ${m('N_0=\\dfrac{m_0}{A}\\,')} ${f(10)}</div>
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
${h3(3, 'Kết quả tự kiểm tra câu 2–8', '3·3')}
${rkHai([2, 3, 4, 5], [6, 7, 8])}
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('BÀI TOÁN MẪU · MẪU NA-24 TRONG Y HỌC')}
${h3(1, 'V · Đề bài', '4')}
<div class="card soft" style="padding:1.2mm 3mm">Mẫu ${m('{}^{24}_{11}\\mathrm{Na}')}, ${m('T=15\\ \\mathrm{h}')}, ban đầu ${m('N_0=1{,}2\\cdot10^{15}')} hạt nhân.
<div><b>a)</b> Viết phương trình phân rã ${m('\\beta^-')}; hạt nhân con tiến hay lùi mấy ô?</div><div><b>b)</b> Tính ${m('\\lambda')} (${m('1/\\mathrm{s}')}).</div><div><b>c)</b> Sau 45 giờ còn bao nhiêu hạt nhân, đã rã bao nhiêu phần trăm?</div><div><b>d)</b> Tính ${m('H_0')} và độ phóng xạ còn lại sau 45 giờ.</div><div><b>e)</b> Đổi ${m('H_0')} ra curi.</div></div>
${h3(2, 'Phân tích đề')}
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
 + wl('★★★ Xương cổ còn 1/8 lượng C-14: tuổi? Một giả thiết dễ vỡ:', 4))}${hinh.chiaDoiMau('Chia mẫu làm hai: N và H giảm một nửa, còn T thì sao?')}</div>
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

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 2], kq: [[1, 2, 3], [4, 5]] },
  tra: 'phóng xạ 1·4 · đếm xung 1·5 · bốn loại tia 2·1 · dịch ô 2·2 · định luật phóng xạ 2·3 · độ phóng xạ 2·4 · bẫy 3·1 · dạng 1–3 → 6·1 · dạng 4–5 → 7·1',
  out: process.argv[2],
});
