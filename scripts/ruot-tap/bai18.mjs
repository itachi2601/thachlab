// Ruột tập VL12 – Bài 18 · An toàn phóng xạ (lesson id 19). Khung: khung.mjs; hình: hinh-ch4.mjs.
// Chạy: node scripts/ruot-tap/bai18.mjs [file.pdf] → scripts/ruot-tap/out/ruot-tap-vl12-bai18.pdf
import { khoiTao, m, lines, wl, fill as f, nw, exp, ck, box, opt, chon, rkHai, hinh } from './khung.mjs';
const K = khoiTao({ bai: 21, baiDau: 17, lid: 19, ten: 'AN TOÀN PHÓNG XẠ' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const hd = m('\\dot H');

const p1 = `<section class="page">
${head('BÀI 21 · AN TOÀN PHÓNG XẠ', K.sub + ' · web: Bài 18')}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
<div style="margin:.3mm 0">${ck}Nêu được <b>tác hại</b> của tia phóng xạ và bốn yếu tố quyết định</div>
<div style="margin:.3mm 0">${ck}Phân biệt <b>liều hấp thụ</b> (Gy) với <b>liều tương đương</b> (Sv)</div>
<div style="margin:.3mm 0">${ck}Vận dụng <b>thời gian – khoảng cách – che chắn</b> để tính liều</div>
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Kỹ thuật viên lùi từ 1 m ra 3 m. Suất liều ở chỗ mới sẽ:</p>
<div class="fig-side" style="${fs(52)}"><div>
${opt('A', 'Còn một nửa')}
${opt('B', 'Còn một phần ba')}
${opt('C', 'Còn một phần chín')}
${opt('D', 'Không đổi')}
<div style="margin-top:1mm">${chon(10)}</div><div class="hint">Vì sao?</div>${lines(1)}</div>
${hinh.nguoiSauChi('Lùi từ 1 m ra 3 m: suất liều đổi bao nhiêu lần?')}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Tia phóng xạ gây hại thế nào', '1·4')}
<div class="card" style="padding:1.2mm 3mm">
<div>Không nhìn ${f(10)}; ${f(10)} hoá môi trường, phá huỷ phân tử sinh học, hỏng ${f(10)}; nặng nhất ở tế bào phân chia ${f(10)}.</div>
<div>Bốn yếu tố: ${f(22)}, khả năng ${f(12)}, khả năng ${f(14)}, ${f(14)} chiếu.</div></div>
${h3(5, 'II.2 · Liều hấp thụ và liều tương đương', '1·5')}
<div class="card" style="padding:1.2mm 3mm">
<div>${m('D=')} ${f(8)} / ${f(8)} (đơn vị ${f(8)}); ${m('1\\ \\mathrm{Gy}=')} ${nw(`${f(10)}&nbsp;J/kg`)}</div>
<div>${m('H=')} ${f(8)} · ${f(8)} (đơn vị ${f(8)}); ${m('w_R')}: X, γ, β = ${f(6)}; α = ${f(6)}; nơtron ${f(10)}</div>
<div>Suất liều ${hd} (${nw('µSv/h')}): ${m('H=')} ${f(8)} · ${f(8)} &nbsp;<span class="hint">đổi phút ra giờ trước</span></div></div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('MỐC LIỀU · BA NGUYÊN TẮC · ỨNG DỤNG · CHẤT THẢI')}
${h3(1, 'Mốc liều nên nhớ (mSv)', '2·1')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div>Phông tự nhiên: ${nw(`${f(8)}&nbsp;mSv/năm`)}</div>
<div>X-quang ngực: ${nw(`${f(8)}&nbsp;mSv`)} &nbsp;·&nbsp; chụp CT: ${nw(`${f(8)}&nbsp;mSv`)}</div>
<div>Giới hạn nghề nghiệp: ${nw(`${f(8)}&nbsp;mSv/năm`)}; dân thường ${nw(`${f(8)}&nbsp;mSv/năm`)}</div>
<div>Toàn thân ${nw(`${f(10)}&nbsp;mSv`)}: chết ${f(8)} số người.</div></div>
${hinh.bacLieu('Thang logarit, đơn vị mSv.')}</div>
${h3(2, 'II.3 · Thời gian – khoảng cách – che chắn', '2·2')}
<div class="card fig-side" style="${fs(56)};padding:1.2mm 3mm"><div>
<div>Thời gian: liều tỉ lệ ${f(10)} với ${m('t')}. &nbsp;${m('H=')} ${f(8)} · ${f(8)}</div>
<div>Khoảng cách: ${m('\\dot H\\sim')} ${f(8)}; ${m('\\dfrac{\\dot H_2}{\\dot H_1}=')} ${f(16)}</div>
<div>Che chắn: α ${f(10)}; β ${f(10)}; γ, X ${f(18)}.</div></div>
${hinh.xuyen('Mỗi tia dừng ở một tấm chắn khác nhau.')}</div>
${h3(3, 'Thí nghiệm: suất liều theo khoảng cách', '2·3')}
<table class="tbl-ct"><tr><th>${m('d\\ (\\mathrm m)')}</th><th>0,5</th><th>1,0</th><th>1,5</th><th>2,0</th><th>3,0</th></tr>
<tr><td>${hd} (µSv/h)</td><td>360</td><td>90</td><td>40</td><td>22,5</td><td>10</td></tr>
<tr><td>${hd}${m('\\cdot d^2')}</td><td></td><td></td><td></td><td></td><td></td></tr></table>
<div class="hint" style="margin:.5mm 0 0">Hàng cuối gần như không đổi ⇒ ${hd} tỉ lệ nghịch với ${f(8)}. Lùi xa là cách giảm liều ${f(10)} nhất.</div>
${h3(4, 'II.4 – II.6 · Biển, liều kế, y tế, chất thải', '2·4')}
<div class="card" style="padding:1.2mm 3mm">
<div>Biển ba cánh: đặt ở nơi ${f(18)}; liều kế đeo ở ${f(10)}, đọc định kì.</div>
<div>Y tế: liều ${f(8)} để xem (chẩn đoán), liều ${f(8)} để diệt (điều trị ung thư).</div>
<div>Chất thải: phân loại theo ${f(18)} → giảm thể tích → ${f(10)} → ${f(10)}; không ${f(10)} loãng.</div></div>
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('BẪY · TRẢ BÀI · KẾT QUẢ TỰ KIỂM TRA')}
${h3(1, 'III · Ba cái bẫy hay sập', '3·1')}
<div class="card" style="padding:1mm 3mm">
<div class="trap">${ck}<span><b>“Gy và Sv là một.”</b> Gy đo năng lượng mô nhận; Sv đo mức nguy hiểm: ${m('H=w_R D')}.</span></div>
<div class="trap">${ck}<span><b>“Xa gấp đôi thì liều giảm một nửa.”</b> Tỉ lệ nghịch ${m('r^2')}: xa gấp 2 ⇒ còn ${m('1/4')}.</span></div>
<div class="trap">${ck}<span><b>“Alpha bị giấy chắn nên vô hại.”</b> Chỉ đúng khi nguồn ở ${f(10)}; ${f(14)} vào thì nguy hiểm nhất.</span></div></div>
${h3(2, 'IV · Trả bài 6 câu', '3·2')}
${box(`${tb('1. Tia phóng xạ gây hại cho cơ thể thế nào?')}${lines(2)}
${tb('2. Liều hấp thụ và liều tương đương khác nhau thế nào?')}${lines(2)}
${tb('3. Phát biểu ba nguyên tắc an toàn phóng xạ.')}${lines(2)}
${tb('4. Vì sao lùi xa gấp đôi thì liều còn một phần tư?')}${lines(2)}
${tb('5. Biển cảnh báo phóng xạ đặt ở đâu, để làm gì?')}${lines(2)}
${tb('6. Xử lí chất thải phóng xạ theo bước nào, vì sao tách theo chu kì?')}${lines(2)}`)}
<div class="card soft" style="margin-top:1.5mm;padding:1mm 3mm"><b>Bạn cùng bàn kiểm:</b> nói được ……/6 câu · câu chưa thuộc: ${f(30)} → đọc lại ô Tập ${f(14)}</div>
${h3(3, 'Kết quả tự kiểm tra (câu chiếu trên lớp)', '3·3')}
${rkHai([2, 3, 4], [5, 6, 7])}
${h3(4, 'Đề 1195 cuối tiết (web: Bài 18)', '3·4')}
<div class="card soft" style="padding:1mm 3mm">Điểm ……/20 &nbsp;· câu sai: ${f(40)}</div>
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('BÀI TOÁN MẪU · SUẤT LIỀU 90 µSv/h TẠI 1 m')}
${h3(1, 'V · Đề bài', '4·1')}
<div class="card soft" style="padding:1.2mm 3mm">Nguồn ${m('{}^{192}_{77}\\mathrm{Ir}')}: máy đo cho ${m('90\\ \\mu\\mathrm{Sv/h}')} tại 1 m. Kỹ thuật viên đứng ở 3 m, mỗi ca 30 phút, cả năm 2 000 giờ; giới hạn nghề nghiệp 20 mSv/năm.
<div><b>a)</b> Suất liều ở 3 m?</div><div><b>b)</b> Liều trong 30 phút ở 3 m?</div><div><b>c)</b> Ở 1 m trong 30 phút, liều gấp mấy lần?</div><div><b>d)</b> 2 000 giờ/năm ở 3 m có vượt giới hạn?</div></div>
${h3(2, 'Phân tích đề (điền ở nhà)', '4·2')}
<table><tr><th style="width:46mm">Câu trong đề</th><th style="width:36mm">Dữ liệu</th><th>Kiến thức liên quan</th></tr>
<tr><td>“90 µSv/h tại 1 m”</td><td>${m('\\dot H_1=90')}</td><td>suất liều gốc</td></tr>
<tr><td style="height:6.5mm">“đứng cách nguồn 3 m”</td><td></td><td></td></tr>
<tr><td style="height:6.5mm">“30 phút mỗi ca”</td><td></td><td></td></tr>
<tr><td style="height:6.5mm">“cả năm 2 000 giờ”</td><td></td><td></td></tr></table>
${h3(3, 'Giải', '4·3')}
<div class="fig-side" style="${fs(52)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl('a)', 2)}${wl('b)', 2)}${wl('c)', 2)}${wl('d)', 3)}</div>${hinh.nguoiSauChi('Ở 1 m và 3 m.', '90 µSv/h', '?')}</div>
${h3(4, 'Mở rộng: 160 µSv/h tại 1 m', '4·4')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div class="ln" style="height:auto;padding-top:1mm"><b>Đề:</b> đứng cách 2 m trong 15 phút, mỗi ca không quá 0,01 mSv. <b>Bước 1 (cho sẵn):</b> xa gấp 2 ⇒ ${hd}${m('_2=160/4=40\\ \\mu\\mathrm{Sv/h}')}.</div>
${wl('Bước 2: liều trong 15 phút = …', 2)}${wl('Bước 3: muốn liều ≤ 5 µSv thì đứng tối đa mấy phút?', 2)}</div>
<div class="card soft" style="margin-top:1.5mm;padding:1mm 3mm"><b>Em tự kiểm:</b> ${ck}đổi phút ra giờ &nbsp;${ck}chia theo tỉ số khoảng cách &nbsp;${ck}có ghi đơn vị</div>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TẬP VỀ NHÀ · MANG VỀ · THỬ THÁCH', 'Tập bài 21 = Bài 18 trên web')}
${K.btvn().replace('</h3>', `</h3>${K.tag('5·1')}`).replace('<b>Điểm:</b>', '<b>Điểm BTVN:</b>')}
${h3(2, 'VI · Mang về: điều em dễ quên nhất', '5·2')}
${box(wl('1.', 2) + wl('2.', 2) + wl('3.', 2))}
${h3(3, 'Thử thách phân tầng', '5·3')}
<div class="fig-side" style="grid-template-columns:1fr 30mm">${box(wl('★ Đổi 0,1 mSv ra µSv; X-quang ngực gấp mấy lần 5 µSv một ca?', 2)
 + wl('★★ Vì sao cùng 1 Gy, alpha gây hại gấp 20 lần tia X?', 3)
 + wl('★★★ Vì sao I-131 (T = 8 ngày) lưu vài tháng được còn nhiên liệu phải cách li hàng nghìn năm?', 4))}${hinh.bienCanhBao('Biển cảnh báo.')}</div>
${h3(4, 'Câu 7 (đổi số)', '5·4')}
${box(wl('120 µSv/h tại 2 m; liều ≤ 20 µSv, ở 4 m đứng tối đa … phút', 3))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Liều hấp thụ và liều tương đương',
    de: `X-quang ngực: khối mô ${m('12\\ \\mathrm{kg}')} hấp thụ ${m('1{,}2\\ \\mathrm{mJ}')} tia X (${m('w_R=1')}).<br><b>a)</b> liều hấp thụ ${m('D')} (Gy)<br><b>b)</b> liều tương đương ${m('H')} (mSv)`,
    nd: `Cho năng lượng hấp thụ và khối lượng mô → ${m('D=')} ${f(8)} / ${f(8)}, rồi ${m('H=')} ${f(8)} · ${m('D')}`, a: ['a', 'b'], gi: 0 },
  { t: 'Dạng 2 · Trung bình · Cùng liều hấp thụ, khác loại tia',
    de: `Hai mẫu mô ${m('0{,}50\\ \\mathrm{kg}')}, mỗi mẫu hấp thụ ${m('2{,}0\\ \\mathrm{mJ}')}: A chiếu γ, B chiếu α.<br><b>a)</b> ${m('D')} mỗi mẫu (mGy)<br><b>b)</b> ${m('H')} mỗi mẫu (mSv)<br><b>c)</b> mẫu nào hại hơn, gấp mấy lần`,
    nd: `Cùng năng lượng hấp thụ → cùng ${m('D')}; so tác hại bằng ${m('H=w_R\\,D')} với ${m('w_R')} = ${f(6)} và ${f(6)}`, a: ['a', 'b', 'c'], gi: 0 },
  { t: 'Dạng 3 · Trung bình · Suất liều theo khoảng cách',
    de: `Nguồn điểm: ${m('72\\ \\mu\\mathrm{Sv/h}')} tại 0,50 m.<br><b>a)</b> suất liều tại 1,5 m<br><b>b)</b> đặt máy cách nguồn bao nhiêu m để chỉ còn ${m('2{,}0\\ \\mu\\mathrm{Sv/h}')}`,
    nd: `Đổi khoảng cách → ${m('\\dot H_2/\\dot H_1=')} (${m('r_1/r_2')})<sup>${f(4)}</sup>: chia theo ${f(14)} khoảng cách`, a: ['a', 'b'], gi: 4, fig: 'nghichBinhPhuong' },
  { t: 'Dạng 4 · Khó · Thời gian đứng tối đa mỗi ca',
    de: `Nguồn ${m('250\\ \\mu\\mathrm{Sv/h}')} tại 1,0 m; kỹ thuật viên đứng cách 2,5 m.<br><b>a)</b> suất liều tại chỗ đứng<br><b>b)</b> liều khi đứng 12 phút<br><b>c)</b> liều mỗi ca ≤ ${m('20\\ \\mu\\mathrm{Sv}')}: đứng tối đa mấy phút`,
    nd: `Cho suất liều, thời gian, liều cho phép → ${m('H=')} ${f(8)} · ${m('t')} (đổi phút ra ${f(6)})`, a: ['a', 'b', 'c'], gi: 3 },
  { t: 'Dạng 5 · Khó · So sánh bốn biện pháp giảm liều',
    de: `Đứng 1,0 m, 40 phút/ca, máy đo 360 xung/phút. A: lùi 3,0 m; B: còn 10 phút; C: chì 5 mm (154 xung/phút); D: nhôm 3 mm (335 xung/phút).<br><b>a)</b> % liều còn lại của từng biện pháp<br><b>b)</b> biện pháp nào giảm nhiều nhất`,
    nd: `Quy mỗi biện pháp về % liều còn lại rồi tô vào thanh: A ${f(8)}, B ${f(8)}, C ${f(8)}, D ${f(8)}`, a: ['a', 'b'], gi: 4, fig: 'baBienPhap' },
  { t: 'Dạng 6 · Nâng cao · Liều cả năm và khoảng cách tối thiểu',
    de: `Nguồn ${m('160\\ \\mu\\mathrm{Sv/h}')} tại 1,0 m; nhân viên làm 2 000 giờ/năm ở 2,0 m; giới hạn 20 mSv/năm.<br><b>a)</b> liều cả năm; gấp mấy lần giới hạn<br><b>b)</b> phải đứng cách tối thiểu bao nhiêu m`,
    nd: `Đổi mSv ra µSv, quy ngược về suất liều cho phép ${m('=')} ${f(10)}, rồi về khoảng cách`, a: ['a', 'b'], gi: 2 },
];

// Bài tương tự (bố cục bài 14, thầy chốt 10/11): bài về nhà, GIẢI VÀO VỞ; giấy in đề + ô đáp số theo ý, đáp số lật ngược cuối trang.
// Đáp số tính bằng Python (python3) 16/11/2026; w_R: X, γ, β = 1; α = 20 (như bài học).
const ttCss = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';
const oY = (s, o, w = 25) => s.split('<br>').map((p) => {
  const y = p.match(/^<b>([a-d])\)<\/b>/);
  if (!y) return `<div>${p}</div>`;
  const ls = o.filter((l) => l[0] === y[1]);
  return `<div class="yo"><span>${p}</span><span class="oo">${ls.map((l) => `<span class="nw"><b>${l})</b>${f(w)}</span>`).join('')}</span></div>`;
}).join('');
const ttDe = (b) => oY(b.de, b.o, b.ow);
const vaoVo = (ds) => ds.map((b) => (b.o ? { t: b.t, de: ttDe(b), k: 0 } : b));
const nhap = (n) => ({ t: '<span class="nhap-t">Nháp / chỗ em còn vướng</span>', de: lines(n), k: 0 });
const wr = m('w_R:\\ \\mathrm X,\\ \\gamma,\\ \\beta=1;\\ \\alpha=20');
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–3', 'DẠNG 4–6'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Chụp CT bụng: khối mô ${m('20\\ \\mathrm{kg}')} hấp thụ ${m('0{,}16\\ \\mathrm J')} tia X (${m('w_R=1')}).<br><b>a)</b> liều hấp thụ ${m('D')} (mGy)<br><b>b)</b> liều tương đương ${m('H')} (mSv)`, o: ['a', 'b'] },
    { t: 'Dạng 1 · Bài 2', de: `Xạ trị: khối u ${m('0{,}25\\ \\mathrm{kg}')} nhận ${m('0{,}50\\ \\mathrm J')} tia ${m('\\gamma')} mỗi buổi (${m('w_R=1')}).<br><b>a)</b> liều hấp thụ mỗi buổi (Gy)<br><b>b)</b> liều tương đương mỗi buổi (Sv)<br><b>c)</b> cả đợt cần ${m('60\\ \\mathrm{Gy}')}: số buổi`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 2 · Bài 1', de: `Hai mẫu mô ${m('0{,}40\\ \\mathrm{kg}')}, mỗi mẫu hấp thụ ${m('1{,}2\\ \\mathrm{mJ}')}: A chiếu ${m('\\beta')}, B chiếu ${m('\\alpha')} (${wr}).<br><b>a)</b> ${m('D')} mỗi mẫu (mGy)<br><b>b)</b> ${m('H')} của A, của B (mSv)<br><b>c)</b> mẫu nào hại hơn, gấp mấy lần`, o: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'] },
    { t: 'Dạng 2 · Bài 2', de: `Khối mô ${m('2{,}0\\ \\mathrm{kg}')} bị chiếu ${m('\\alpha')}, nhận liều tương đương ${m('4{,}0\\ \\mathrm{mSv}')} (${wr}).<br><b>a)</b> liều hấp thụ ${m('D')} (mGy)<br><b>b)</b> năng lượng mô đã hấp thụ (mJ)<br><b>c)</b> muốn cùng ${m('H')} bằng tia ${m('\\gamma')}, mô phải hấp thụ bao nhiêu mJ`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 3 · Bài 1', de: `Nguồn điểm: ${m('48\\ \\mu\\mathrm{Sv/h}')} tại 2,0 m.<br><b>a)</b> suất liều tại 4,0 m (µSv/h)<br><b>b)</b> cách nguồn bao nhiêu m thì còn ${m('3{,}0\\ \\mu\\mathrm{Sv/h}')}`, o: ['a', 'b'] },
    { t: 'Dạng 3 · Bài 2', de: `Nguồn điểm: ${m('200\\ \\mu\\mathrm{Sv/h}')} tại 0,40 m.<br><b>a)</b> suất liều tại 1,0 m (µSv/h)<br><b>b)</b> cách nguồn bao nhiêu m thì còn ${m('2{,}0\\ \\mu\\mathrm{Sv/h}')}`, o: ['a', 'b'] },
    nhap(4),
  ], [
    { t: 'Dạng 4 · Bài 1', de: `Nguồn ${m('180\\ \\mu\\mathrm{Sv/h}')} tại 1,0 m; kỹ thuật viên đứng cách 3,0 m.<br><b>a)</b> suất liều tại chỗ đứng (µSv/h)<br><b>b)</b> liều khi đứng 15 phút (µSv)<br><b>c)</b> liều mỗi ca ≤ ${m('10\\ \\mu\\mathrm{Sv}')}: đứng tối đa mấy phút`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 4 · Bài 2', de: `Nguồn ${m('400\\ \\mu\\mathrm{Sv/h}')} tại 0,50 m; kỹ thuật viên đứng cách 2,0 m.<br><b>a)</b> suất liều tại chỗ đứng (µSv/h)<br><b>b)</b> liều khi đứng 6 phút (µSv)<br><b>c)</b> liều mỗi ca ≤ ${m('15\\ \\mu\\mathrm{Sv}')}: đứng tối đa mấy phút`, o: ['a', 'b', 'c'] },
    { t: 'Dạng 5 · Bài 1', de: `Đứng 1,0 m, 30 phút/ca, máy đo 400 xung/phút. Tính % liều còn lại khi:<br><b>a)</b> lùi ra 2,0 m<br><b>b)</b> chỉ đứng 6 phút<br><b>c)</b> đặt tấm chì (máy còn 120 xung/phút)<br><b>d)</b> biện pháp nào giảm liều nhiều nhất`, o: ['a', 'b', 'c', 'd'] },
    { t: 'Dạng 5 · Bài 2', de: `Đứng 0,50 m, 20 phút/ca, máy đo 500 xung/phút. Tính % liều còn lại khi:<br><b>a)</b> lùi ra 1,5 m<br><b>b)</b> chỉ đứng 5 phút<br><b>c)</b> đặt tấm chì (máy còn 250 xung/phút)<br><b>d)</b> vừa lùi ra 1,5 m vừa đặt tấm chì đó`, o: ['a', 'b', 'c', 'd'] },
    { t: 'Dạng 6 · Bài 1', de: `Nguồn ${m('90\\ \\mu\\mathrm{Sv/h}')} tại 1,0 m; nhân viên làm 1 500 giờ/năm ở 1,5 m; giới hạn 20 mSv/năm.<br><b>a)</b> liều cả năm (mSv); gấp mấy lần giới hạn<br><b>b)</b> phải đứng cách tối thiểu bao nhiêu m`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b'] },
    { t: 'Dạng 6 · Bài 2', de: `Nguồn ${m('250\\ \\mu\\mathrm{Sv/h}')} tại 1,0 m; nhân viên làm 2 000 giờ/năm ở 2,5 m; giới hạn 20 mSv/năm.<br><b>a)</b> liều cả năm (mSv); gấp mấy lần giới hạn<br><b>b)</b> phải đứng cách tối thiểu bao nhiêu m`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b'] },
    nhap(2),
  ]],
  dap: [
    `D1·1: ${nw('a) 8,0 mGy')} · ${nw('b) 8,0 mSv')} &nbsp;|&nbsp; D1·2: ${nw('a) 2,0 Gy')} · ${nw('b) 2,0 Sv')} · ${nw('c) 30 buổi')} &nbsp;|&nbsp; D2·1: ${nw('a) 3,0 mGy')} · ${nw('b<sub>1</sub>) 3,0 mSv')} · ${nw('b<sub>2</sub>) 60 mSv')} · c) B, gấp 20 lần &nbsp;|&nbsp; D2·2: ${nw('a) 0,20 mGy')} · ${nw('b) 0,40 mJ')} · ${nw('c) 8,0 mJ')} &nbsp;|&nbsp; D3·1: ${nw('a) 12 µSv/h')} · ${nw('b) 8,0 m')} &nbsp;|&nbsp; D3·2: ${nw('a) 32 µSv/h')} · ${nw('b) 4,0 m')}`,
    `D4·1: ${nw('a) 20 µSv/h')} · ${nw('b) 5,0 µSv')} · ${nw('c) 30 phút')} &nbsp;|&nbsp; D4·2: ${nw('a) 25 µSv/h')} · ${nw('b) 2,5 µSv')} · ${nw('c) 36 phút')} &nbsp;|&nbsp; D5·1: ${nw('a) 25 %')} · ${nw('b) 20 %')} · ${nw('c) 30 %')} · d) chỉ đứng 6 phút &nbsp;|&nbsp; D5·2: ${nw('a) 11 %')} · ${nw('b) 25 %')} · ${nw('c) 50 %')} · ${nw('d) 5,6 %')} &nbsp;|&nbsp; D6·1: ${nw('a<sub>1</sub>) 60 mSv')} · ${nw('a<sub>2</sub>) gấp 3 lần')} · ${nw('b) 2,6 m')} &nbsp;|&nbsp; D6·2: ${nw('a<sub>1</sub>) 80 mSv')} · ${nw('a<sub>2</sub>) gấp 4 lần')} · ${nw('b) 5,0 m')}`,
  ],
};

await K.dung({
  trang1to5: ttCss + [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 3], kq: [[1, 2, 3], [4, 5, 6]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'tác hại 1·4 · liều Gy–Sv 1·5 · mốc liều 2·1 · ba nguyên tắc 2·2 · bảng đo 2·3 · biển, y tế, chất thải 2·4 · bẫy 3·1 · dạng 1–3 → 6·1 · dạng 4–6 → 7·1',
  out: process.argv[2],
});
