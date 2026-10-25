// Ruột tập VL12 – Bài 16 · Phản ứng phân hạch, phản ứng nhiệt hạch và ứng dụng (lesson id 17). Khung: khung.mjs; hình: hinh-ch4.mjs.
// Chạy: node scripts/ruot-tap/bai16.mjs [file.pdf] → scripts/ruot-tap/out/ruot-tap-vl12-bai16.pdf
import { khoiTao, m, lines, wl, fill as f, nw, exp, ck, box, opt, chon, rkHai, hinh } from './khung.mjs';
const K = khoiTao({ bai: 16, lid: 17, ten: 'PHÂN HẠCH · NHIỆT HẠCH' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;

const p1 = `<section class="page">
${head('BÀI 16 · PHÂN HẠCH · NHIỆT HẠCH', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
<div style="margin:.3mm 0">${ck}Nêu được <b>phản ứng hạt nhân</b> và các đại lượng <b>bảo toàn</b></div>
<div style="margin:.3mm 0">${ck}Tính <b>năng lượng toả ra</b> ${m('W')} từ độ hụt khối của phản ứng</div>
<div style="margin:.3mm 0">${ck}Mô tả <b>phân hạch, dây chuyền</b> (hệ số ${m('k')}), lò phản ứng và <b>nhiệt hạch</b></div>
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Nhà máy điện hạt nhân không có ngọn lửa. Năng lượng khổng lồ ấy đến từ đâu?</p>
<div class="fig-side" style="${fs(52)}"><div>
${opt('A', 'Phản ứng hoá học giữa urani với nước')}
${opt('B', 'Hạt nhân urani vỡ ra, khối lượng nghỉ thành năng lượng')}
${opt('C', 'Nhiệt còn lại trong lòng đất')}
${opt('D', 'Ma sát giữa nước và thanh nhiên liệu')}
<div style="margin-top:1mm">${chon(10)}</div><div class="hint">Vì sao?</div>${lines(1)}</div>
${hinh.phanHach('Một nơtron chậm làm vỡ U-235: hai mảnh, thêm 2–3 nơtron, tia γ.')}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Phản ứng hạt nhân và các định luật bảo toàn', '1·4')}
<div class="card" style="padding:1.2mm 3mm">
<div>Biến hạt nhân này thành hạt nhân khác: tự ${f(12)} hoặc do ${f(14)}.</div>
<div>Bảo toàn: ${f(14)}, số ${f(12)}, ${f(18)} toàn phần, ${f(14)}. <b>Không</b> bảo toàn ${f(24)}.</div>
<div>${m('A_1+A_2=')} ${f(16)} &nbsp;·&nbsp; ${m('Z_1+Z_2=')} ${f(16)}</div>
<div style="margin-top:.6mm"><b>Tự kiểm tra 1.</b> ${m('{}^{235}_{92}\\mathrm{U}+{}^{1}_{0}\\mathrm{n}\\to{}^{144}_{56}\\mathrm{Ba}+{}^{89}_{36}\\mathrm{Kr}+x\\,{}^{1}_{0}\\mathrm{n}')}</div>
<div>Cộng ${m('A')} hai vế: ${f(34)} ⇒ ${m('x=')} ${f(8)} &nbsp;${ck}chắc</div></div>
${h3(5, 'II.2 · Năng lượng toả ra của phản ứng', '1·5')}
<div class="card" style="padding:1.2mm 3mm">
<div>${m('W=(')} ${f(22)} ${m(')\\,c^2')} &nbsp;·&nbsp; ${m('1\\ \\mathrm{u}=')} ${nw(`${f(12)}&nbsp;MeV/${m('c^2')}`)} &nbsp;·&nbsp; ${m('1\\ \\mathrm{MeV}=')} ${nw(`${f(18)}&nbsp;J`)}</div>
<div>Khối lượng nghỉ <b>giảm</b> ⇒ ${m('W')} ${f(8)} 0: phản ứng ${f(10)}. &nbsp;Khối lượng nghỉ <b>tăng</b> ⇒ ${m('W')} ${f(8)} 0: ${f(10)}.</div></div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('PHÂN HẠCH · DÂY CHUYỀN · LÒ PHẢN ỨNG · NHIỆT HẠCH')}
${h3(1, 'II.3 · Phân hạch', '2·1')}
<div class="card" style="padding:1.2mm 3mm"><div>Hạt nhân rất ${f(10)} hấp thụ ${f(12)} chậm rồi vỡ thành ${f(8)} mảnh; mỗi lần thêm ${f(8)}–${f(8)} nơtron và tia ${f(8)}.</div>
<div>Toả vì hai mảnh bền hơn: ${m('E_{lkr}')} ${f(10)}, tổng khối lượng nghỉ ${f(10)}. Một phân hạch cỡ ${nw(`${f(10)}&nbsp;MeV`)}.</div></div>
${h3(2, 'II.4 · Phản ứng dây chuyền, hệ số nhân k', '2·2')}
<div class="card fig-side" style="${fs(52)};padding:1.2mm 3mm"><div>
<div>${m('k=')} ${f(12)} / ${f(12)}</div>
<div>${m('k\\lt1')}: ${f(16)} &nbsp;·&nbsp; ${m('k=1')}: ${f(16)}</div>
<div>${m('k\\gt1')}: ${f(20)}</div>
<div>Khối lượng tới hạn: lượng nhiên liệu ${f(14)} để giữ ${m('k\\ge1')}.</div></div>
${hinh.chuoiNotron('Ba thế hệ nơtron: k = số nơtron thế hệ sau chia thế hệ trước.')}</div>
${h3(3, 'II.5 · Lò phản ứng', '2·3')}
<div class="card fig-side" style="${fs(56)};padding:1.2mm 3mm"><div>
<div>Thanh điều khiển (bo, cađimi) ${f(14)} nơtron: đẩy vào ⇒ ${m('k')} ${f(10)}; kéo ra ⇒ ${m('k')} ${f(10)}.</div>
<div>Giữ ${m('k=')} ${f(6)} để công suất không đổi. Chất tải nhiệt đưa nhiệt tới ${f(16)} rồi ${f(14)}.</div></div>
${hinh.loPhanUng('Thanh điều khiển hấp thụ nơtron: đẩy vào sâu thì k giảm.')}</div>
${h3(4, 'II.6 · Nhiệt hạch', '2·4')}
<div class="card fig-side" style="${fs(54)};padding:1.2mm 3mm"><div>
<div>Hạt nhân rất ${f(10)} kết hợp thành hạt nhân ${f(12)}.</div>
<div>Điều kiện: ${nw(`${f(12)}&nbsp;K`)}, mật độ ${f(12)}, duy trì ${f(12)}.</div>
<div>Nơi có nhiệt hạch tự nhiên: ${f(24)}.</div></div>
${hinh.nhietHach('D + T → He-4 + n, toả cỡ 17,6 MeV.')}</div>
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('BẪY · TRẢ BÀI · KẾT QUẢ TỰ KIỂM TRA')}
${h3(1, 'III · Ba cái bẫy hay sập', '3·1')}
<div class="card" style="padding:1mm 3mm">
<div class="trap">${ck}<span><b>“U-235 tự vỡ như chất phóng xạ.”</b> Phân hạch cần <b>nơtron</b> bắn vào, điều khiển được bằng ${m('k')}.</span></div>
<div class="trap">${ck}<span><b>“Khối lượng được bảo toàn.”</b> Khối lượng nghỉ <b>không</b> bảo toàn: phần hụt là năng lượng.</span></div>
<div class="trap">${ck}<span><b>“Phân hạch và nhiệt hạch là một.”</b> Ngược chiều: nặng vỡ ra – nhẹ ghép lại.</span></div></div>
${h3(2, 'IV · Trả bài 6 câu', '3·2')}
${box(`${tb('1. Phản ứng hạt nhân là gì? Bốn đại lượng nào bảo toàn?')}${lines(2)}
${tb('2. Viết hệ thức năng lượng phản ứng. Khi nào toả, khi nào thu?')}${lines(2)}
${tb('3. Phân hạch là gì? Vì sao phân hạch U-235 toả năng lượng?')}${lines(2)}
${tb('4. Hệ số nhân nơtron k là gì? Ý nghĩa ba trường hợp?')}${lines(2)}
${tb('5. Nhà máy điện hạt nhân gồm bộ phận nào? Thanh điều khiển để làm gì?')}${lines(2)}
${tb('6. Nhiệt hạch là gì? Điều kiện và một nơi có nhiệt hạch tự nhiên?')}${lines(2)}`)}
<div class="card soft" style="margin-top:1.5mm;padding:1mm 3mm"><b>Bạn cùng bàn kiểm:</b> nói được ……/6 câu · câu chưa thuộc: ${f(30)} → đọc lại ô Tập ${f(14)}</div>
${h3(3, 'Kết quả tự kiểm tra câu 2–7', '3·3')}
${rkHai([2, 3, 4], [5, 6, 7])}
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('BÀI TOÁN MẪU · MỘT GAM URANI BẰNG MẤY TẤN THAN?')}
${h3(1, 'V · Đề bài', '4')}
<div class="card soft" style="padding:1.2mm 3mm">${m('{}^{235}_{92}\\mathrm{U}+{}^{1}_{0}\\mathrm{n}\\to{}^{144}_{56}\\mathrm{Ba}+{}^{89}_{36}\\mathrm{Kr}+x\\,{}^{1}_{0}\\mathrm{n}')}. ${m('m_{\\mathrm{U}}=235{,}0439')}, ${m('m_{\\mathrm{n}}=1{,}0087')}, ${m('m_{\\mathrm{Ba}}=143{,}9230')}, ${m('m_{\\mathrm{Kr}}=88{,}9176')} (u); ${m('1\\ \\mathrm{MeV}=1{,}6\\cdot10^{-13}\\ \\mathrm{J}')}; ${m('N_A=6{,}02\\cdot10^{23}')}; than ${m('2{,}7\\cdot10^{7}\\ \\mathrm{J/kg}')}.
<div><b>a)</b> Tìm ${m('x')}, kiểm tra bảo toàn.</div><div><b>b)</b> Độ hụt khối và năng lượng của một phân hạch (MeV).</div><div><b>c)</b> Một gam U-235 phân hạch hết toả bao nhiêu jun?</div><div><b>d)</b> Bằng đốt bao nhiêu kg than?</div></div>
${h3(2, 'Phân tích đề')}
<table><tr><th style="width:46mm">Câu trong đề</th><th style="width:36mm">Dữ liệu</th><th>Kiến thức liên quan</th></tr>
<tr><td>“U-235 hấp thụ nơtron chậm”</td><td>${m('A=235,\\ Z=92')}</td><td>bảo toàn ${m('A,\\ Z')}</td></tr>
<tr><td style="height:6.5mm">“khối lượng các hạt”</td><td></td><td></td></tr>
<tr><td style="height:6.5mm">“một gam U-235”</td><td></td><td></td></tr>
<tr><td style="height:6.5mm">“than toả ${m('2{,}7\\cdot10^{7}')} J/kg”</td><td></td><td></td></tr></table>
${h3(3, 'Giải')}
<div class="fig-side" style="${fs(56)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl('a)', 2)}${wl('b)', 4)}${wl('c)', 3)}${wl('d)', 2)}</div>${hinh.canPhanUng('Khối lượng nghỉ sau nhỏ hơn trước: phần hụt thành W.')}</div>
${h3(4, 'Mở rộng: trung bình 200 MeV một phân hạch')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div class="ln" style="height:auto;padding-top:1mm"><b>Bước 1 (cho sẵn):</b> ${m('200\\ \\mathrm{MeV}=3{,}2\\cdot10^{-11}\\ \\mathrm{J}')}.</div>
${wl('Bước 2: muốn có đúng 1 J cần … phân hạch', 2)}${wl('Bước 3: con số đó nói lên điều gì về nhiên liệu hạt nhân?', 2)}</div>
<div class="card soft" style="margin-top:1.5mm;padding:1mm 3mm"><b>Em tự kiểm:</b> ${ck}cộng đủ nơtron cả hai vế &nbsp;${ck}đổi MeV ra J &nbsp;${ck}có ghi đơn vị</div>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TẬP VỀ NHÀ · MANG VỀ · THỬ THÁCH')}
${K.btvn()}
${h3(2, 'VI · Mang về: điều em dễ quên nhất', '5')}
${box(wl('1.', 2) + wl('2.', 2) + wl('3.', 2))}
${h3(3, 'Thử thách phân tầng')}
${box(wl('★ Bốn bộ phận chính của nhà máy điện hạt nhân và vai trò thanh điều khiển:', 3)
 + wl('★★ Vì sao trong lò phải giữ k = 1 mà không để k lớn hơn một chút?', 3)
 + wl('★★★ Mặt trời chỉ 1,5·10⁷ K, thấp hơn 10⁸ K; vì sao vẫn cháy?', 4))}
${h3(4, 'Câu 7 (đổi số)')}
${box(wl('Số phân hạch cần để toả 1 J (200 MeV/phân hạch) = …', 2))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Phân loại phản ứng, hệ số nhân k',
    de: `(1) ${m('{}^{1}_{0}\\mathrm{n}+{}^{235}_{92}\\mathrm{U}\\to{}^{95}_{39}\\mathrm{Y}+{}^{138}_{53}\\mathrm{I}+3\\,{}^{1}_{0}\\mathrm{n}')} (lò); (2) ${m('{}^{2}_{1}\\mathrm{H}+{}^{3}_{1}\\mathrm{H}\\to{}^{4}_{2}\\mathrm{He}+{}^{1}_{0}\\mathrm{n}')}. Nơtron ba thế hệ: 50 000; 50 200; 50 400.<br><b>a)</b> loại của (1), (2)<br><b>b)</b> hệ số ${m('k')}, công suất đổi thế nào<br><b>c)</b> chỉnh thanh điều khiển ra sao`,
    nd: `Nặng vỡ → ${f(10)}; nhẹ ghép → ${f(10)}; ${m('k=')} ${f(10)} / ${f(10)} rồi so với ${f(4)}`, a: ['a', 'b', 'c'], gi: 3, fig: 'baTheHe' },
  { t: 'Dạng 2 · Dễ · Tìm hạt chưa biết bằng bảo toàn',
    de: `(1) ${m('{}^{1}_{0}\\mathrm{n}+{}^{235}_{92}\\mathrm{U}\\to{}^{139}_{54}\\mathrm{Xe}+{}^{95}_{38}\\mathrm{Sr}+x\\,{}^{1}_{0}\\mathrm{n}')}; (2) ${m('{}^{2}_{1}\\mathrm{H}+{}^{2}_{1}\\mathrm{H}\\to{}^{3}_{2}\\mathrm{He}+{}^{A}_{Z}\\mathrm{X}')}<br><b>a)</b> ${m('x')}; điện tích hai vế có bằng nhau?<br><b>b)</b> hạt X`,
    nd: `Hạt chưa biết → viết ${m('\\sum A')} và ${m('\\sum Z')} hai vế, nhớ cộng cả hạt ${f(14)}`, a: ['a', 'b'], gi: 0 },
  { t: 'Dạng 3 · Trung bình · Toả hay thu năng lượng',
    de: `(1) D + T → He + n; (2) ${m('{}^{14}_{7}\\mathrm{N}+{}^{4}_{2}\\mathrm{He}\\to{}^{17}_{8}\\mathrm{O}+{}^{1}_{1}\\mathrm{p}')}. ${m('m_D=2{,}013553')}, ${m('m_T=3{,}015501')}, ${m('m_{He}=4{,}001506')}, ${m('m_n=1{,}008665')}, ${m('m_N=13{,}999231')}, ${m('m_O=16{,}994740')}, ${m('m_p=1{,}007276')} (u).<br><b>a)</b> ${m('W')} của (1) theo MeV và J<br><b>b)</b> (2) toả hay thu? bao nhiêu MeV`,
    nd: `Cho khối lượng hai vế → ${m('\\Delta m=\\sum m_{trước}-')} ${f(12)}, xét dấu, nhân ${f(10)}`, a: ['a', 'b'], gi: 5 },
  { t: 'Dạng 4 · Khó · Đốt cả gam nhiên liệu nhiệt hạch',
    de: `D + T toả 17,6 MeV. Lò đốt hết ${m('1{,}0\\ \\mathrm{g}')} đơteri (${m('M=2{,}0\\ \\mathrm{g/mol}')}), triti dư; ${m('1\\ \\mathrm{MeV}=1{,}6\\cdot10^{-13}\\ \\mathrm{J}')}; than ${m('2{,}7\\cdot10^{7}\\ \\mathrm{J/kg}')}.<br><b>a)</b> số phản ứng<br><b>b)</b> năng lượng (J)<br><b>c)</b> bằng đốt bao nhiêu kg than`,
    nd: `Cho khối lượng nhiên liệu → ${m('N=')} ${f(8)} ${m('\\cdot N_A')}, nhân năng lượng ${f(10)}`, a: ['a', 'b', 'c'], gi: 5 },
  { t: 'Dạng 5 · Nâng cao · Lò 900 MW chạy 30 ngày',
    de: `Công suất nhiệt ${m('900\\ \\mathrm{MW}')}, 30 ngày liên tục, toàn bộ từ phân hạch U-235, mỗi phân hạch ${m('200\\ \\mathrm{MeV}')}; ${m('M=235\\ \\mathrm{g/mol}')}.<br><b>a)</b> năng lượng lò toả ra (J)<br><b>b)</b> khối lượng U-235 đã phân hạch<br><b>c)</b> bằng đốt bao nhiêu tấn than`,
    nd: `Cho công suất và thời gian → ${m('E=')} ${f(8)}·${f(8)}, chia cho năng lượng ${f(10)} để đếm hạt nhân`, a: ['a', 'b', 'c'], gi: 4, fig: 'congSuat' },
];

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 2], kq: [[1, 2, 3], [4, 5]] },
  tra: 'bảo toàn 1·4 · năng lượng toả ra 1·5 · phân hạch 2·1 · hệ số k 2·2 · lò phản ứng 2·3 · nhiệt hạch 2·4 · bẫy 3·1 · dạng 1–3 → 6·1 · dạng 4–5 → 7·1',
  out: process.argv[2],
});
