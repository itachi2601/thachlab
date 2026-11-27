// Ruột tập VL12 – Bài 16 · Phản ứng phân hạch, phản ứng nhiệt hạch và ứng dụng (lesson id 17). Khung: khung.mjs; hình: hinh-ch4.mjs.
// Chạy: node scripts/ruot-tap/bai16.mjs [file.pdf] → scripts/ruot-tap/out/ruot-tap-vl12-bai16.pdf
import { khoiTao, m, lines, wl, fill as f, nw, exp, ck, box, opt, chon, rkHai, hinh } from './khung.mjs';
const K = khoiTao({ bai: 19, baiDau: 17, lid: 17, ten: 'PHÂN HẠCH · NHIỆT HẠCH' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;

// Bài tương tự giải vào vở: ô đáp số đặt cuối dòng của từng ý (như l10-bai23).
const ttCss = '<style>.yo{display:flex;justify-content:space-between;align-items:flex-end;gap:2mm;line-height:1.35}.yo .oo{flex:none;display:flex;gap:3mm}.yo .fill{height:3.4mm}.tt:has(.nhap-t) .hd>span+span{display:none}</style>';
const p1 = `${ttCss}<section class="page">
${head('BÀI 19 · PHÂN HẠCH · NHIỆT HẠCH', K.sub)}
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
${hinh.phanHach(`Một nơtron chậm làm vỡ U-235: hai mảnh, thêm 2–3 nơtron, tia ${m('\\gamma')}.`)}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Phản ứng hạt nhân và các định luật bảo toàn', '1·4')}
<div class="card" style="padding:1.2mm 3mm">
<div>Biến hạt nhân này thành hạt nhân khác: tự ${f(12)} hoặc do ${f(14)}.</div>
<div>Bảo toàn 4 đại lượng: 1) ${f(14)} 2) số ${f(12)} 3) ${f(18)} toàn phần 4) ${f(14)}. <b>Không</b> bảo toàn ${f(24)}.</div>
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
${hinh.anh('lo-phan-ung-nuoc-ap-luc.png', 'Lò nước áp lực: lõi lò (tím) đun nước vòng sơ cấp → bình sinh hơi → tua bin + máy phát; bình ngưng làm lạnh hơi (vòng thứ cấp). Thanh điều khiển cắm từ trên xuống lõi. (Halliday 43.2.2)')}</div>
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
${h3(3, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '3·3')}
${rkHai([2, 3, 4], [5, 6, 7])}
<div class="card soft" style="margin-top:1mm;padding:1mm 3mm"><b>Đề cuối tiết 1193:</b> điểm ……/19</div>
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('BÀI TOÁN MẪU · MỘT GAM URANI BẰNG MẤY TẤN THAN?')}
${h3(1, 'V · Đề bài', '4')}
<div class="card soft" style="padding:1.2mm 3mm">${m('{}^{235}_{92}\\mathrm{U}+{}^{1}_{0}\\mathrm{n}\\to{}^{144}_{56}\\mathrm{Ba}+{}^{89}_{36}\\mathrm{Kr}+x\\,{}^{1}_{0}\\mathrm{n}')}. ${m('m_{\\mathrm{U}}=235{,}0439')}, ${m('m_{\\mathrm{n}}=1{,}0087')}, ${m('m_{\\mathrm{Ba}}=143{,}9230')}, ${m('m_{\\mathrm{Kr}}=88{,}9176')} (u); ${m('1\\ \\mathrm{MeV}=1{,}6\\cdot10^{-13}\\ \\mathrm{J}')}; ${m('N_A=6{,}02\\cdot10^{23}')}; ${m('M=235\\ \\mathrm{g/mol}')}; than ${m('2{,}7\\cdot10^{7}\\ \\mathrm{J/kg}')}.
<div><b>a)</b> Tìm ${m('x')}, kiểm tra bảo toàn.</div><div><b>b)</b> Độ hụt khối và năng lượng của một phân hạch (MeV).</div><div><b>c)</b> Một gam U-235 phân hạch hết toả bao nhiêu jun?</div><div><b>d)</b> Bằng đốt bao nhiêu kg than?</div></div>
${h3(2, 'Phân tích đề (điền cùng thầy)')}
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
<div class="ln" style="height:auto;padding-top:1mm"><b>Bước 1 (cho sẵn):</b> ${m('200\\ \\mathrm{MeV}=3{,}2\\cdot10^{-11}\\ \\mathrm{J}')} (đề trên là một cặp mảnh cụ thể Ba + Kr nên ra 173 MeV; trung bình mọi cặp mảnh ≈ 200 MeV).</div>
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
 + wl('★★★ (HS giỏi) Mặt trời chỉ 1,5·10⁷ K, thấp hơn 10⁸ K; vì sao vẫn cháy?', 3)
 + wl('Câu 7 (đã chọn ở ô 27·3): 200 MeV/phân hạch; số phân hạch để toả 1 J = …', 1))}
${h3(4, 'Xem hình: Mặt trời là lò nhiệt hạch')}
<div class="fig-side" style="grid-template-columns:90mm 1fr">${hinh.anh('chu-trinh-proton-proton.png', 'Chu trình p–p: 4 prôtôn → He-4 + 2 nơtrinô + 6γ, toả 26,7 MeV. e⁺ pôzitron, ν nơtrinô, γ phôtôn, Q năng lượng toả ra của từng bước. (Halliday 43.5.1)')}<div class="hint">Lõi Mặt trời chỉ cỡ 1,5·10⁷ K; vì sao vẫn cháy? (thử thách ★★★)</div></div>
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
    nd: `Cho khối lượng hai vế → ${m('\\Delta m=\\sum m_{\\mathrm{truoc}}-')} ${f(12)}, xét dấu, nhân ${f(10)}`, a: ['a', 'b'], gi: 5 },
  { t: 'Dạng 4 · Khó · Đốt cả gam nhiên liệu nhiệt hạch',
    de: `D + T toả 17,6 MeV. Lò đốt hết ${m('1{,}0\\ \\mathrm{g}')} đơteri (${m('M=2{,}0\\ \\mathrm{g/mol}')}), triti dư; ${m('1\\ \\mathrm{MeV}=1{,}6\\cdot10^{-13}\\ \\mathrm{J}')}; than ${m('2{,}7\\cdot10^{7}\\ \\mathrm{J/kg}')}.<br><b>a)</b> số phản ứng<br><b>b)</b> năng lượng (J)<br><b>c)</b> bằng đốt bao nhiêu kg than`,
    nd: `Cho khối lượng nhiên liệu → ${m('N=')} ${f(8)} ${m('\\cdot N_A')}, nhân năng lượng ${f(10)}`, a: ['a', 'b', 'c'], gi: 5 },
  { t: 'Dạng 5 · Nâng cao · Lò 900 MW chạy 30 ngày',
    de: `Công suất nhiệt ${m('900\\ \\mathrm{MW}')}, 30 ngày liên tục, toàn bộ từ phân hạch U-235, mỗi phân hạch ${m('200\\ \\mathrm{MeV}')}; ${m('M=235\\ \\mathrm{g/mol}')}.<br><b>a)</b> năng lượng lò toả ra (J)<br><b>b)</b> khối lượng U-235 đã phân hạch<br><b>c)</b> bằng đốt bao nhiêu tấn than`,
    nd: `Cho công suất và thời gian → ${m('E=')} ${f(8)}·${f(8)}, chia cho năng lượng ${f(10)} để đếm hạt nhân`, a: ['a', 'b', 'c'], gi: 4, fig: 'congSuat' },
];

// Bài tương tự (thầy chốt 10/11): bài về nhà, giải vào vở; mỗi dạng 2 bài; đáp số tính bằng Python 16/11/2026
// (1 u = 931,5 MeV/c², 1 MeV = 1,6·10⁻¹³ J, N_A = 6,02·10²³; khối lượng HẠT NHÂN, cùng bộ số với Dạng 3).
const oY = (s, o, w = 25) => s.split('<br>').map((p) => {
  const y = p.match(/^<b>([a-d])\)<\/b>/);
  if (!y) return `<div>${p}</div>`;
  const ls = o.filter((l) => l[0] === y[1]);
  return `<div class="yo"><span>${p}</span><span class="oo">${ls.map((l) => `<span class="nw"><b>${l})</b>${f(w)}</span>`).join('')}</span></div>`;
}).join('');
const vaoVo = (ds) => ds.map((b) => (b.o ? { t: b.t, de: oY(b.de, b.o, b.ow), k: 0 } : b));
const nhap = (n) => ({ t: '<span class="nhap-t">Nháp / chỗ em còn vướng</span>', de: lines(n), k: 0 });
const n0 = '{}^{1}_{0}\\mathrm{n}';
const MeVJ = nw(`${m('1\\ \\mathrm{MeV}=1{,}6\\cdot10^{-13}\\ \\mathrm{J}')}`);
const NA = nw(m('N_A=6{,}02\\cdot10^{23}\\ \\mathrm{mol^{-1}}'));
const u = `${m('1\\ \\mathrm{u}=931{,}5\\ \\mathrm{MeV}/c^2')}`;
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–3', 'DẠNG 4–5'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `(1) ${m('{}^{2}_{1}\\mathrm{H}+{}^{2}_{1}\\mathrm{H}\\to{}^{3}_{2}\\mathrm{He}+' + n0)}; (2) ${m(n0 + '+{}^{239}_{94}\\mathrm{Pu}\\to{}^{134}_{54}\\mathrm{Xe}+{}^{103}_{40}\\mathrm{Zr}+3\\,' + n0)}. Nơtron ba thế hệ trong lò: ${nw('40 000')}; ${nw('39 600')}; ${nw('39 204')}.<br><b>a)</b> loại phản ứng (1), (2)<br><b>b)</b> hệ số ${m('k')}; công suất lò đổi thế nào<br><b>c)</b> chỉnh thanh điều khiển ra sao`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'] },
    { t: 'Dạng 1 · Bài 2', de: `(1) ${m(n0 + '+{}^{235}_{92}\\mathrm{U}\\to{}^{140}_{55}\\mathrm{Cs}+{}^{93}_{37}\\mathrm{Rb}+3\\,' + n0)}; (2) ${m('{}^{2}_{1}\\mathrm{H}+{}^{3}_{2}\\mathrm{He}\\to{}^{4}_{2}\\mathrm{He}+{}^{1}_{1}\\mathrm{H}')}. Nơtron ba thế hệ: ${nw('12 000')}; ${nw('12 000')}; ${nw('12 000')}.<br><b>a)</b> loại phản ứng (1), (2)<br><b>b)</b> hệ số ${m('k')}; công suất lò đổi thế nào<br><b>c)</b> chỉnh thanh điều khiển ra sao`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'] },
    { t: 'Dạng 2 · Bài 1', de: `(1) ${m(n0 + '+{}^{235}_{92}\\mathrm{U}\\to{}^{140}_{54}\\mathrm{Xe}+{}^{94}_{38}\\mathrm{Sr}+x\\,' + n0)}; (2) ${m('{}^{7}_{3}\\mathrm{Li}+{}^{1}_{1}\\mathrm{H}\\to{}^{4}_{2}\\mathrm{He}+{}^{A}_{Z}\\mathrm{X}')}<br><b>a)</b> ${m('x')}; điện tích hai vế có bằng nhau?<br><b>b)</b> hạt X`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b'] },
    { t: 'Dạng 2 · Bài 2', de: `(1) ${m(n0 + '+{}^{235}_{92}\\mathrm{U}\\to{}^{141}_{56}\\mathrm{Ba}+{}^{92}_{36}\\mathrm{Kr}+x\\,' + n0)}; (2) ${m('{}^{2}_{1}\\mathrm{H}+{}^{2}_{1}\\mathrm{H}\\to{}^{3}_{1}\\mathrm{H}+{}^{A}_{Z}\\mathrm{X}')}<br><b>a)</b> ${m('x')}; điện tích hai vế có bằng nhau?<br><b>b)</b> hạt X`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b'] },
    { t: 'Dạng 3 · Bài 1', de: `(1) ${m('{}^{2}_{1}\\mathrm{H}+{}^{2}_{1}\\mathrm{H}\\to{}^{3}_{2}\\mathrm{He}+' + n0)}; (2) ${m('{}^{27}_{13}\\mathrm{Al}+{}^{4}_{2}\\mathrm{He}\\to{}^{30}_{15}\\mathrm{P}+' + n0)}. ${m('m_D=2{,}013553')}, ${m('m_{He3}=3{,}014932')}, ${m('m_n=1{,}008665')}, ${m('m_{Al}=26{,}974406')}, ${m('m_{He4}=4{,}001506')}, ${m('m_P=29{,}970085')} (u); ${u}; ${nw(`${MeVJ}.`)}<br><b>a)</b> ${m('W')} của (1) theo MeV và J<br><b>b)</b> (2) toả hay thu? bao nhiêu MeV`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>'] },
    { t: 'Dạng 3 · Bài 2', de: `(1) ${m('{}^{7}_{3}\\mathrm{Li}+{}^{1}_{1}\\mathrm{p}\\to2\\,{}^{4}_{2}\\mathrm{He}')}; (2) ${m('{}^{7}_{3}\\mathrm{Li}+{}^{1}_{1}\\mathrm{p}\\to{}^{7}_{4}\\mathrm{Be}+' + n0)}. ${m('m_{Li}=7{,}014357')}, ${m('m_p=1{,}007276')}, ${m('m_{He}=4{,}001506')}, ${m('m_{Be}=7{,}014733')}, ${m('m_n=1{,}008665')} (u); ${u}; ${nw(`${MeVJ}.`)}<br><b>a)</b> ${m('W')} của (1) theo MeV và J<br><b>b)</b> (2) toả hay thu? bao nhiêu MeV`, o: ['a<sub>1</sub>', 'a<sub>2</sub>', 'b<sub>1</sub>', 'b<sub>2</sub>'] },
  ], [
    { t: 'Dạng 4 · Bài 1', de: `D + T → He + n toả ${nw(m('17{,}6\\ \\mathrm{MeV}'))}. Lò đốt hết ${m('0{,}30\\ \\mathrm g')} triti (${m('M=3{,}0\\ \\mathrm{g/mol}')}), đơteri dư; ${NA}; ${MeVJ}; than ${nw(`${m('2{,}7\\cdot10^{7}\\ \\mathrm{J/kg}')}.`)}<br><b>a)</b> số phản ứng<br><b>b)</b> năng lượng toả ra (J)<br><b>c)</b> bằng đốt bao nhiêu kg than`, o: ['a', 'b', 'c'], ow: 30 },
    { t: 'Dạng 4 · Bài 2', de: `${m('{}^{7}_{3}\\mathrm{Li}+{}^{1}_{1}\\mathrm{p}\\to2\\,{}^{4}_{2}\\mathrm{He}')} toả ${nw(m('17{,}3\\ \\mathrm{MeV}'))}. Đốt hết ${m('1{,}4\\ \\mathrm g')} liti-7 (${m('M=7{,}0\\ \\mathrm{g/mol}')}), prôtôn dư; ${NA}; ${MeVJ}; xăng ${nw(`${m('4{,}6\\cdot10^{7}\\ \\mathrm{J/kg}')}.`)}<br><b>a)</b> số phản ứng<br><b>b)</b> năng lượng toả ra (J)<br><b>c)</b> bằng đốt bao nhiêu kg xăng`, o: ['a', 'b', 'c'], ow: 30 },
    { t: 'Dạng 5 · Bài 1', de: `Lò công suất nhiệt ${m('500\\ \\mathrm{MW}')} chạy liên tục 365 ngày, toàn bộ từ phân hạch U-235, mỗi phân hạch ${nw(m('200\\ \\mathrm{MeV}'))}; ${m('M=235\\ \\mathrm{g/mol}')}; ${NA}; ${MeVJ}; than ${nw(`${m('2{,}7\\cdot10^{7}\\ \\mathrm{J/kg}')}.`)}<br><b>a)</b> năng lượng lò toả ra (J)<br><b>b)</b> khối lượng U-235 đã phân hạch<br><b>c)</b> bằng đốt bao nhiêu tấn than`, o: ['a', 'b', 'c'], ow: 30 },
    { t: 'Dạng 5 · Bài 2', de: `Nhà máy điện hạt nhân công suất <b>điện</b> ${m('1200\\ \\mathrm{MW}')}, hiệu suất ${m('30\\,\\%')}, chạy 24 giờ; U-235, mỗi phân hạch ${nw(m('200\\ \\mathrm{MeV}'))}; ${m('M=235\\ \\mathrm{g/mol}')}; ${NA}; ${MeVJ}; than ${nw(`${m('2{,}7\\cdot10^{7}\\ \\mathrm{J/kg}')}.`)}<br><b>a)</b> năng lượng nhiệt lò toả ra (J)<br><b>b)</b> khối lượng U-235 đã phân hạch<br><b>c)</b> bằng đốt bao nhiêu tấn than`, o: ['a', 'b', 'c'], ow: 30 },
    nhap(7),
  ]],
  dap: [
    `D1·1: a<sub>1</sub>) nhiệt hạch · a<sub>2</sub>) phân hạch · b<sub>1</sub>) k = 0,99 · b<sub>2</sub>) giảm dần · c) kéo bớt ra &nbsp;|&nbsp; D1·2: a<sub>1</sub>) phân hạch · a<sub>2</sub>) nhiệt hạch · b<sub>1</sub>) k = 1 · b<sub>2</sub>) không đổi · c) giữ nguyên &nbsp;|&nbsp; D2·1: a<sub>1</sub>) x = 2 · a<sub>2</sub>) có (92 = 54 + 38) · b) ${nw(`<sup>4</sup><sub>2</sub>He (hạt ${m('\\alpha')})`)} &nbsp;|&nbsp; D2·2: a<sub>1</sub>) x = 3 · a<sub>2</sub>) có (92 = 56 + 36) · b) ${nw('<sup>1</sup><sub>1</sub>H (prôtôn)')} &nbsp;|&nbsp; D3·1: a<sub>1</sub>) 3,27 MeV · a<sub>2</sub>) ${nw('5,23·10<sup>−13</sup> J')} · b<sub>1</sub>) thu · b<sub>2</sub>) 2,64 MeV &nbsp;|&nbsp; D3·2: a<sub>1</sub>) 17,3 MeV · a<sub>2</sub>) ${nw('2,78·10<sup>−12</sup> J')} · b<sub>1</sub>) thu · b<sub>2</sub>) 1,64 MeV`,
    `D4·1: a) ${nw('6,02·10<sup>22</sup>')} · b) ${nw('1,70·10<sup>11</sup> J')} · c) ${nw('6,28·10<sup>3</sup> kg')} &nbsp;|&nbsp; D4·2: a) ${nw('1,20·10<sup>23</sup>')} · b) ${nw('3,33·10<sup>11</sup> J')} · c) ${nw('7,24·10<sup>3</sup> kg')} &nbsp;|&nbsp; D5·1: a) ${nw('1,58·10<sup>16</sup> J')} · b) ${nw('192 kg')} · c) ${nw('5,84·10<sup>5</sup> tấn')} &nbsp;|&nbsp; D5·2: a) ${nw('3,46·10<sup>14</sup> J')} · b) ${nw('4,22 kg')} · c) ${nw('1,28·10<sup>4</sup> tấn')}`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 2], kq: [[1, 2, 3], [4, 5]] },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'bảo toàn 1·4 · năng lượng toả ra 1·5 · phân hạch 2·1 · hệ số k 2·2 · lò phản ứng 2·3 · nhiệt hạch 2·4 · bẫy 3·1 · dạng 1–3 → 6·1 · dạng 4–5 → 7·1',
  out: process.argv[2],
});
