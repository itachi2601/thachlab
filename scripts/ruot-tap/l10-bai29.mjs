// Ruột tập Vật lí 10 – Bài 29 · Định luật bảo toàn động lượng (lesson id 74). Quyển L10 Chương 5 (bài 28–29…): bài này là tr. 13–24.
// Khung: khung.mjs (bố cục bài 14 có trang Bài tương tự, giải vào vở); hình: hinh-l10-bai29.mjs (SVG tự vẽ, không dùng ảnh Halliday).
// Nguồn nội dung: bài web lesson 74 (book/cache/74.json): lý thuyết I–VI + 5 dạng bài tập mẫu; số liệu bài mẫu, thí nghiệm, thử thách
// lấy đúng bài web. Đáp số bài tương tự tính bằng Python (phiên 12/11/2026).
// Chạy: node scripts/ruot-tap/l10-bai29.mjs [file.pdf] → scripts/ruot-tap/out/ruot-tap-vl10-bai29.pdf
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai, dapSo, TRANG_DAU } from './khung.mjs';
import { hinhBai29 as H } from './hinh-l10-bai29.mjs';
const K = khoiTao({ bai: 29, lid: 74, ten: 'ĐỊNH LUẬT BẢO TOÀN ĐỘNG LƯỢNG', lop: 10, baiDau: 28, sub: 'Vật lí 10 · Chương 5: Động lượng' });
const { head, h3, foot } = K;
const tr = (n) => (29 - 28) * 12 + TRANG_DAU - 1 + n; // số trang tuyệt đối trong quyển
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const u = (s, d) => nw(m(`${s}\\ \\mathrm{${d}}`));
const kgms = '\\mathrm{kg\\cdot m/s}';

const fn = f(12), fw = f(25), fl = f(34); // ô số ≥12 mm, ô chữ ≥25 mm, ô "số + chiều" 34 mm (HS ảo 10/11)
const fp = (w, p) => nw(`${f(w)}${p}`); // ô + dấu câu dính nhau
// Dòng viết tự do cao 9 mm cho chỗ phải viết công thức có phân số
const ph = (lab, tail = '') => `<div class="ln" style="height:9mm;display:flex;align-items:center;gap:1.5mm"><span>${lab}</span><span style="flex:1"></span>${tail}</div>`;
const pT = `${m('p')}<sub>trước</sub>`, pS = `${m('p')}<sub>sau</sub>`;
// Câu hỏi dài (nhiều dòng chữ) rồi n dòng kẻ — wl() chỉ hợp nhãn một dòng
const q = (s, n) => `<div style="padding-top:.6mm;border-bottom:.2mm dotted var(--hint);background:#fff">${s}</div>` + lines(n);
const mot = (s) => `<div style="margin:.3mm 0">${ck}${s}</div>`;

const p1 = `<section class="page">
${head('BÀI 29 · ĐỊNH LUẬT BẢO TOÀN ĐỘNG LƯỢNG', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
${mot('Nhận ra <b>hệ kín</b>; phát biểu định luật bảo toàn động lượng')}
${mot('Viết phương trình động lượng <b>có dấu</b> theo chiều dương đã chọn')}
${mot('Phân biệt va chạm <b>mềm</b> và va chạm <b>đàn hồi</b>')}
${mot('Giải thích chuyển động bằng <b>phản lực</b>: súng giật, tên lửa')}
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Trên sân băng, An trượt thẳng tới với tốc độ ${u('4', 'm/s')} rồi ôm chầm lấy Bình đang đứng yên. Hai bạn đều nặng ${u('50', 'kg')}. Ngay sau cú ôm, hai bạn cùng lướt với tốc độ bao nhiêu?</p>
<div class="fig-side" style="${fs(44)}"><div>
${opt('A', `${u('4', 'm/s')}: An kéo Bình theo đúng tốc độ cũ`)}
${opt('B', u('2', 'm/s'))}
${opt('C', `${m('0')}: ôm nhau thì đứng lại`)}
${opt('D', `Khoảng ${u('2{,}8', 'm/s')}, để động năng giữ nguyên`)}
<div style="margin-top:1mm">${chon(12)}</div><div class="ln"><span class="hint">Vì sao?</span></div></div>
${H.omNhau()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${fn} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Hệ kín', '1·4')}
<div class="card fig-side" style="${fs(44)};padding:1.2mm 3mm"><div>
<div><b>Nội lực:</b> lực giữa ${fp(25, '.')}</div>
<div><b>Ngoại lực:</b> lực do ${fw} gây ra.</div>
<div><b>Hệ kín:</b> không có ${fw},</div>
<div>hoặc các ngoại lực ${fp(25, '.')}</div>
<div>Coi gần đúng là kín: va chạm, ${fp(25, ',')}</div>
<div>${fw} (nội lực rất ${fp(25, ',')}</div>
<div>xảy ra rất ${fp(25, ').')}</div>
<div>Ngoại lực chỉ theo phương đứng ⇒</div><div>động lượng bảo toàn theo phương ${fp(25, '.')}</div></div>
${H.heKin()}</div>
<div class="card soft" style="padding:1mm 3mm"><b>Hệ nào coi được là hệ kín?</b>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:0 3mm">
<div>${ck}A. Quả táo đang rơi tự do</div><div>${ck}B. Người + xe đạp đang phanh</div>
<div>${ck}C. Thuyền buồm được gió đẩy</div><div>${ck}D. Hai xe va chạm trên ray đệm khí</div></div></div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('ĐỊNH LUẬT · THÍ NGHIỆM · HAI KIỂU VA CHẠM')}
${h3(1, 'II.2 · Phát biểu định luật', '2·1')}
<div class="card" style="padding:.6mm 3mm 1.2mm">
<div>Hệ kín thì tổng ${fw} động lượng ${fp(25, '.')}</div>
${ph('<b>Hệ hai vật:</b>')}
<div>Từng vật có thể ${fw} động lượng; ${fw} thì không đổi.</div>
<div><b>Vì sao?</b> Hai vật đẩy nhau: ${m('\\vec F_{12}=-\\vec F_{21}')} (định luật ${fn} Newton), cùng thời gian ${m('\\Delta t')}.</div>
<div>Theo Bài 28: ${m('\\Delta\\vec p_1=\\vec F_{21}\\Delta t')}, ${m('\\Delta\\vec p_2=\\vec F_{12}\\Delta t')} ⇒ ${m('\\Delta\\vec p_1+\\Delta\\vec p_2=')} ${fp(12, '.')}</div></div>
${h3(2, 'Thí nghiệm: va chạm mềm trên ray đệm khí', '2·2')}
<div class="card fig-side" style="${fs(48)};padding:1.2mm 3mm"><div>
<div><b>Làm:</b> xe 1 có ${nw(m('m_1=0{,}20\\ \\mathrm{kg}'))}; xe 2 đứng yên. Đẩy xe 1, đo ${m('v_1')} rồi ${m('v')}; đổi ${m('m_2')}, đo 4 lần.</div>
<div><b>Quan sát:</b> hai xe dính nhau đi ${fw} xe 1 lúc đầu.</div></div>
${H.rayDem()}</div>
<table class="tbl-ct"><tr><th>${m('m_2')} (kg)</th><th>0,20</th><th>0,30</th><th>0,40</th><th>0,60</th></tr>
<tr><td>${m('v_1')} ; ${m('v')} (m/s)</td><td>0,52 ; 0,25</td><td>0,60 ; 0,24</td><td>0,57 ; 0,19</td><td>0,66 ; 0,16</td></tr>
<tr><td>${pT}${m('=m_1v_1')} (${m(kgms)})</td><td></td><td></td><td></td><td></td></tr>
<tr><td>${pS}${m('=(m_1+m_2)v')} (${m(kgms)})</td><td></td><td></td><td></td><td></td></tr></table>
<div style="margin:.8mm 0 0"><b>Rút ra:</b> ${pT} ${fw} ${pS}; lệch vài % vì ${ck}ma sát còn sót ${ck}sai số đo thời gian ${ck}cả hai.</div>
<div>Động năng lần 1 (${nw(m('W_{\\text{đ}}=\\tfrac12mv^2'))}): ${m('W')}<sub>sau</sub> : ${m('W')}<sub>trước</sub> = ${nw(`${fn}&nbsp;%`)} ⇒ động năng ${fp(25, '.')}</div>
${h3(3, 'II.3 · Va chạm mềm và va chạm đàn hồi', '2·3')}
<div class="card fig-side" style="${fs(44)};padding:1.2mm 3mm"><div>
<table style="margin:0"><tr><th style="width:24mm"></th><th>Va chạm mềm</th><th>Va chạm đàn hồi</th></tr>
<tr><td>Sau va chạm</td><td style="height:6.5mm"></td><td></td></tr>
<tr><td>Động lượng</td><td style="height:6.5mm"></td><td></td></tr>
<tr><td>Động năng</td><td style="height:6.5mm"></td><td></td></tr></table>
${ph('Vận tốc chung sau va chạm mềm: ' + m('v='))}
<div>${m('v_1, v_2, v')} là giá trị ${fp(25, ':')} ngược chiều dương thì ${fp(12, '.')}</div></div>
${H.haiVaCham()}</div>
<div><b>Thí nghiệm đệm lò xo</b> (hai xe bằng nhau, xe 2 đứng yên):</div><div>sau va chạm xe 1 ${fw}, xe 2 ${fp(25, '.')}</div>
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('PHẢN LỰC · BẪY · TRẢ BÀI')}
${h3(1, 'II.4 · Chuyển động bằng phản lực', '3·1')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div>Tách ra một hướng ⇒ phần còn lại ${fp(25, '.')}</div>
${ph('Hệ đứng yên rồi tách: ' + m('m\\vec v+M\\vec V='), m('\\Rightarrow\\ \\vec V='))}
<div>Dấu “−”: phần còn lại đi ${fp(25, '.')}</div>
<div><b>Bóng bay trên sợi cước:</b> khí phụt ${fp(25, ',')}</div><div>bóng lao ${fp(25, '.')}</div>
<div>Đổi khối lượng: ${nw(m('1\\ \\mathrm{g}=0{,}001\\ \\mathrm{kg}'))}; ${nw('1 tấn = 1000 kg')}.</div></div>
${H.tenLua()}</div>
${ph(`Súng ${u('4', 'kg')} bắn đạn ${u('20', 'g')} bay ${u('500', 'm/s')}: ${m('V=')}`, `= ${nw(`${fn}&nbsp;m/s`)}; chiều: ${fl}`)}
${h3(2, 'III · Ba cái bẫy hay sập', '3·2')}
<div class="card fig-side" style="${fs(40)};padding:1mm 3mm"><div>
<div class="trap">${ck}<span><b>Quên dấu của vận tốc.</b> Chọn chiều dương trước; vật chạy ngược chiều dương thế ${m('v<0')} dù đề chỉ cho tốc độ. Dấu kết quả cho biết chiều.</span></div>
<div class="trap">${ck}<span><b>“Động lượng giữ nguyên thì động năng cũng giữ.”</b> Va chạm mềm (dính, cắm vào) làm động năng giảm; động lượng vẫn bảo toàn.</span></div>
<div class="trap">${ck}<span><b>Dùng bảo toàn cho cả quãng trượt dài.</b> Chỉ dùng từ ngay trước đến ngay sau va chạm; trượt lâu thì ma sát làm động lượng giảm.</span></div></div>
${H.chieuDuong()}</div>
${h3(3, 'IV · Trả bài 6 câu', '3·3')}
${box(`${tb('1. Hệ kín là gì? Kể hai trường hợp coi gần đúng là kín.')}${lines(1)}
${tb('2. Phát biểu định luật bảo toàn động lượng, viết cho hệ hai vật.')}${lines(1)}
${tb('3. Trước khi thế số vào phương trình động lượng phải làm gì?')}${lines(1)}
${tb('4. Va chạm mềm khác va chạm đàn hồi ở đâu? Cái gì bảo toàn trong cả hai?')}${lines(1)}
${tb('5. Công thức vận tốc chung sau va chạm mềm suy ra từ đâu?')}${lines(1)}
${tb('6. Chuyển động bằng phản lực là gì? Dấu “−” trong công thức nói gì?')}${lines(1)}`)}
<div class="card soft" style="margin-top:1.5mm;padding:1mm 3mm"><b>Bạn cùng bàn kiểm:</b> nói được ……/6 câu · câu chưa thuộc: ${fw} ${nw(`→ đọc lại ô Tập ${fn}`)}</div>
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('BÀI TOÁN MẪU · HAI CẦU THỦ ÔM DÍNH')}
${h3(1, 'V · Đề bài', '4')}
<div class="card soft" style="padding:1.2mm 3mm">Trên sân băng, hai cầu thủ khúc côn cầu lao vào nhau trên cùng một đường thẳng: A nặng ${u('80', 'kg')} chạy ${u('6', 'm/s')}, B nặng ${u('100', 'kg')} chạy ${u('3', 'm/s')} theo chiều ngược lại. Va chạm xong, hai người ôm dính lấy nhau. Bỏ qua ma sát trong lúc va chạm.
<div><b>a)</b> Tìm vận tốc (độ lớn và chiều) của hai người ngay sau va chạm.</div><div><b>b)</b> Tìm phần động năng đã mất ${nw(`(${m('W_{\\text{đ}}=\\tfrac12mv^2')})`)}.</div></div>
${h3(2, 'Phân tích đề')}
<table><tr><th style="width:46mm">Câu trong đề</th><th style="width:34mm">Dữ liệu</th><th>Kiến thức liên quan</th></tr>
<tr><td>“trên cùng một đường thẳng”</td><td>một phương</td><td>chọn chiều dương</td></tr>
<tr><td style="height:6.5mm">“A nặng 80&nbsp;kg chạy 6&nbsp;m/s”</td><td></td><td></td></tr>
<tr><td style="height:6.5mm">“B … 3&nbsp;m/s theo chiều ngược lại”</td><td></td><td></td></tr>
<tr><td style="height:6.5mm">“ôm dính lấy nhau”</td><td></td><td></td></tr>
<tr><td style="height:6.5mm">“bỏ qua ma sát trong lúc va chạm”</td><td></td><td></td></tr></table>
${h3(3, 'Giải')}
<div class="fig-side" style="${fs(42)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl('Chọn chiều dương:', 1)}${wl('a)', 4)}${wl('b)', 3)}${wl('Kiểm tra: dấu của v khớp với vật có động lượng lớn hơn?', 1)}</div>${H.cauThu()}</div>
${h3(4, 'Điền bước còn thiếu: B chạy 4,8&nbsp;m/s')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div class="ln" style="height:auto;padding-top:1mm"><b>Đề:</b> như trên, nhưng B chạy ${u('4{,}8', 'm/s')} (vẫn ngược chiều A).</div>
<div class="ln"><b>Bước 1 (cho sẵn):</b> chiều dương theo A: ${m('v_A=+6\\ \\mathrm{m/s}')}, ${m('v_B=-4{,}8\\ \\mathrm{m/s}')}</div>
${wl('Bước 2: tổng động lượng trước =', 2)}${wl(`Bước 3: ${m('v=')} … ; hai người chuyển động thế nào?`, 2)}</div>
<div class="card soft" style="margin-top:1.5mm;padding:1mm 3mm"><b>Em tự kiểm:</b> ${ck}chọn chiều dương &nbsp;${ck}thế dấu “−” cho B &nbsp;${ck}đọc chiều từ dấu của ${m('v')}</div>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TẬP VỀ NHÀ · MANG VỀ · THỬ THÁCH')}
${K.btvn()}
${h3(2, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '5·1')}
${rkHai([1, 2, 3], [4, 5, 6])}
${h3(3, 'VI · Mang về: điều em dễ quên nhất', '5·2')}
${box(wl('1.', 1) + wl('2.', 1))}
${h3(4, 'Thử thách phân tầng')}
<div class="fig-side" style="${fs(42)}">${box(q(`★ Người ${u('60', 'kg')} (không kể tạ) đứng yên trên ván trượt nhẹ (bỏ qua khối lượng ván và ma sát) ném quả tạ ${u('3', 'kg')} về trước với ${u('4', 'm/s')} so với đất. Người trượt lùi nhanh bao nhiêu?`, 1)
 + q(`★★ Đạn ${u('10', 'g')} bay ngang ${u('400', 'm/s')} cắm vào bao cát ${u('3{,}99', 'kg')} treo đứng yên. Vận tốc bao cát ngay sau va chạm? Còn bao nhiêu % động năng?`, 2)
 + q(`★★★ Xe cát ${u('50', 'kg')} chạy ${u('2', 'm/s')} trên ray ngang. Hòn đá ${u('10', 'kg')} rơi chéo cắm vào cát: lúc chạm vận tốc ${u('6', 'm/s')}, chếch xuống ${m('60^\\circ')} so với phương ngang, thành phần ngang ngược chiều xe. Vận tốc xe sau đó?`, 2))}${H.xeCat()}</div>
${h3(5, 'Thử sức đổi chiều: B chạy cùng chiều A')}
${box(q(`Bài toán mẫu ở tr.&nbsp;${tr(4)}: A đuổi theo B (B chạy ${u('3', 'm/s')} cùng chiều) rồi ôm dính. Tìm ${m('v')}, rồi so với số em sẽ ra nếu ở bài mẫu quên dấu “−” của B: vì sao trùng nhau?`, 2))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Hệ kín và bảo toàn động lượng',
    de: `Trên ray đệm khí nằm ngang (ma sát coi như bằng 0), xe 1 ${u('0{,}30', 'kg')} chạy ${u('0{,}60', 'm/s')} tới đẩy xe 2 ${u('0{,}20', 'kg')} đang đứng yên. Ngay sau va chạm, xe 2 chạy cùng chiều xe 1 với ${u('0{,}45', 'm/s')}.<br><b>a)</b> hệ hai xe có kín trong lúc va chạm không, vì sao; &nbsp;<b>b)</b> vận tốc xe 1 ngay sau va chạm (độ lớn, chiều)`,
    nd: `ngoại lực ${fw} ⇒ hệ kín; tổng động lượng trước = ${fp(25, '.')}`, a: ['a', 'b'], gi: 2, fig: H.d1(''), cot: 2 },
  { t: 'Dạng 2 · Dễ · Va chạm mềm: tính vận tốc chung',
    de: `Trong kho hàng, xe đẩy A ${u('150', 'kg')} chạy ${u('2{,}0', 'm/s')} trên nền nhẵn tới va vào xe đẩy B ${u('250', 'kg')}; sau va chạm hai xe móc dính. Bỏ qua ma sát. Tốc độ hai xe ngay sau va chạm khi:<br><b>a)</b> xe B đang đứng yên; &nbsp;<b>b)</b> xe B đang chạy cùng chiều xe A với ${u('0{,}40', 'm/s')}`,
    nd: `“móc dính” ⇒ va chạm ${fp(20, ';')} ${m('v=')} tổng động lượng : ${fp(20, '.')}`, a: ['a', 'b'], gi: 3 },
  { t: 'Dạng 3 · Trung bình · Mềm hay đàn hồi?',
    de: `Trên ray đệm khí, xe 1 ${u('0{,}30', 'kg')} chạy ${u('0{,}80', 'm/s')} va vào xe 2 ${u('0{,}10', 'kg')} đứng yên. Sau va chạm hai xe tách nhau, chạy theo chiều cũ: xe 1 ${u('0{,}40', 'm/s')}, xe 2 ${u('1{,}2', 'm/s')}. Dùng ${nw(m('W_{\\text{đ}}=\\tfrac12mv^2'))}.<br><b>a)</b> tổng động lượng có bảo toàn không (ghi giá trị)<br><b>b)</b> tổng động năng có bảo toàn không; va chạm mềm hay đàn hồi<br><b>c)</b> nếu hai xe dính nhau: tổng động năng ngay sau va chạm`,
    nd: `phân loại phải kiểm cả ${fw} lẫn ${fp(25, '.')}`, a: ['a', 'b', 'c'], gi: 5 },
  { t: 'Dạng 4 · Trung bình · Bảo toàn động lượng với vận tốc ngược chiều',
    de: `Hai goòng chạy ngược chiều trên ray thẳng nằm ngang, đâm vào nhau rồi móc dính: goòng A ${u('900', 'kg')}, ${u('2{,}0', 'm/s')}; goòng B ${u('600', 'kg')}, ${u('1{,}0', 'm/s')}. Bỏ qua ma sát.<br><b>a)</b> vận tốc hai goòng ngay sau va chạm (độ lớn và chiều)<br><b>b)</b> A giữ nguyên số liệu: B phải chạy ngược chiều A với tốc độ bao nhiêu để sau va chạm hai goòng đứng yên`,
    nd: `chiều dương theo ${fp(25, ';')} ${m('v_B=')} ${fp(12, ';')} đứng yên ⇒ tổng ${m('p=')} ${fp(12, '.')}`, a: ['a', 'b'], gi: 7, fig: H.goong(''), cot: 2 },
  { t: 'Dạng 5 · Khó · Chuyển động bằng phản lực: súng giật, tên lửa',
    de: `Cả hai hệ ban đầu đứng yên.<br><b>a)</b> Súng ${u('2{,}5', 'kg')} (không kể đạn) đặt tự do trên mặt nhẵn, bắn đạn ${u('10', 'g')} theo phương ngang với ${u('400', 'm/s')} so với đất: tốc độ giật lùi của súng<br><b>b)</b> Tên lửa mô hình ${u('0{,}60', 'kg')} (kể cả khí) trên ray đệm khí phụt tức thời ${u('0{,}10', 'kg')} khí về sau với ${u('30', 'm/s')} so với đất: tốc độ tên lửa ngay sau khi phụt`,
    nd: `đổi ${m('m')} ra ${fp(12, ';')} ${m('M')} là khối lượng ${fw} sau khi tách; ${nw(m('V=-\\dfrac{m}{M}v'))}`, a: ['a', 'b'], gi: 6, fig: H.sung(''), cot: 2 },
];

// Bài tương tự: mỗi dạng 2 bài đặt cạnh nhau (2 cột), GIẢI VÀO VỞ (thầy chốt 10/11): giấy chỉ in đề + ô đáp số.
// Đáp số tính bằng Python, in lật ngược. CSS 2 cột chèn trong de của bài đầu (như bài 27).
const ttCss2 = `<style>.tt:has(.tt2)>.hd>span:last-child{display:none}.tt2{display:grid;grid-template-columns:1fr 1fr;gap:0 4mm}.tt2>div{min-width:0}
.tt2 .h2{display:flex;justify-content:space-between;align-items:center;font-weight:700;color:var(--navy);border-bottom:.2mm solid var(--grid);margin-bottom:.3mm}
.tt2 .h2>span:last-child{font-weight:400;color:var(--ink);white-space:nowrap}.tt2 .q{margin-top:.5mm}.tt2 .dso{gap:.5mm 2mm}</style>`;
const okS = '<span><span class="ck"></span>đúng &nbsp;<span class="ck"></span>sai, đã sửa</span>';
const bai = (stmt, ys, o = ys.map((y) => y[0]), w = 20) => `<div>${stmt}</div>` + ys.map(([lab, q]) => `<div class="q"><b>${lab})</b> ${q}</div>`).join('') + (typeof o === 'string' ? o : dapSo(o, w));
const NHAP = [0, 8]; // số dòng nháp cuối tr.8, tr.9 — đổ cho dư 0–15 mm
const nhap = (n) => !n ? '' : `<div style="margin-top:2mm;border-top:.3mm solid var(--grid);padding-top:.8mm"><b>Nháp / chỗ em còn vướng</b>${lines(n)}</div>`;
const hai = (a, b, css = '') => `${css}<div class="tt2">${[a, b].map((x, i) => `<div><div class="h2"><span>Bài ${i + 1}</span>${okS}</div>${x}</div>`).join('')}</div>`;
const chieu = '(độ lớn và chiều)';
// Ô đáp số tách: số vào ô, chiều/kết luận chọn bằng ô tích (HS ảo 12/11: chữ dài không vừa ô 25–34 mm)
const oS = (l, w = 20) => `<span class="nw"><b>${l})</b>${f(w)}</span>`;
const oC = (...c) => `<span class="nw">${c.map((x) => `${ck}${x}`).join(' &nbsp;')}</span>`;
const ds = (...p) => `<div class="dso"><b>Đáp số:</b>${p.join(' ')}</div>`;
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–3', 'DẠNG 4–5'],
  trang: [[
    { t: 'Dạng 1 · Hệ kín và bảo toàn động lượng', k: 0, de: hai(
      bai(`Ray đệm khí nằm ngang: xe 1 ${u('0{,}40', 'kg')} chạy ${u('0{,}50', 'm/s')} đẩy xe 2 ${u('0{,}10', 'kg')} đứng yên; ngay sau va chạm xe 2 chạy ${u('1{,}2', 'm/s')} cùng chiều xe 1.`, [['a', 'Hệ hai xe có kín không? Vì sao?'], ['b', `Vận tốc xe 1 ngay sau va chạm ${chieu}?`]], ds(`<span class="nw"><b>a)</b> ${ck}kín ${ck}không kín</span>`, oS('b'), oC('cùng chiều cũ', 'bật ngược'))),
      bai(`Trên mặt bàn nhẵn, bi A ${u('0{,}20', 'kg')} lăn ${u('3{,}0', 'm/s')} va thẳng vào bi B ${u('0{,}30', 'kg')} đứng yên; ngay sau đó B lăn ${u('2{,}4', 'm/s')} theo chiều cũ của A.`, [['a', 'Tổng động lượng trước va chạm?'], ['b', `Vận tốc bi A ngay sau va chạm ${chieu}?`]], ds(oS('a', 26), oS('b'), oC('theo chiều cũ', 'bật ngược'))), ttCss2) },
    { t: 'Dạng 2 · Va chạm mềm: vận tốc chung', k: 0, de: hai(
      bai(`Toa tàu ${nw('20 tấn')} chạy ${u('1{,}5', 'm/s')} va vào toa ${nw('10 tấn')} rồi móc dính. Bỏ qua ma sát. Vận tốc hai toa ngay sau va chạm khi:`, [['a', 'toa 10 tấn đứng yên?'], ['b', `toa 10 tấn đang chạy cùng chiều với ${u('0{,}60', 'm/s')}?`]]),
      bai(`Đạn ${u('10', 'g')} bay ngang ${u('300', 'm/s')} cắm vào khối gỗ ${u('1{,}49', 'kg')} đứng yên trên mặt nhẵn.<br>Cho ${nw(m('1\\ \\mathrm{g}=0{,}001\\ \\mathrm{kg}'))}; ${nw(m('W_{\\text{đ}}=\\tfrac12mv^2'))}.`, [['a', 'Vận tốc gỗ và đạn ngay sau va chạm?'], ['b', 'Động năng mất đi bao nhiêu jun?']])) },
    { t: 'Dạng 3 · Mềm hay đàn hồi', k: 0, de: hai(
      bai(`Ray đệm khí: xe 1 ${u('0{,}20', 'kg')} chạy ${u('0{,}90', 'm/s')} va vào xe 2 ${u('0{,}40', 'kg')} đứng yên. Sau va chạm xe 1 bật ngược ${u('0{,}30', 'm/s')}, xe 2 chạy ${u('0{,}60', 'm/s')} theo chiều cũ của xe 1.`, [['a', 'Tổng động lượng trước (a<sub>1</sub>) và sau (a<sub>2</sub>)?'], ['b', 'Tổng động năng trước (b<sub>1</sub>) và sau (b<sub>2</sub>)?'], ['c', 'Va chạm mềm hay đàn hồi?']], ds(oS('a<sub>1</sub>', 26), oS('a<sub>2</sub>', 26), oS('b<sub>1</sub>'), oS('b<sub>2</sub>'), `<span class="nw"><b>c)</b> ${ck}mềm ${ck}đàn hồi</span>`)),
      bai(`Xe ${u('0{,}50', 'kg')} chạy ${u('0{,}60', 'm/s')} va vào xe ${u('0{,}25', 'kg')} đứng yên, hai xe dính nhau.`, [['a', 'Vận tốc chung?'], ['b', 'Tổng động năng trước (b<sub>1</sub>) và sau (b<sub>2</sub>)?'], ['c', 'Mất bao nhiêu phần trăm động năng?']], ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'])) },
  ], [
    { t: 'Dạng 4 · Vận tốc ngược chiều', k: 0, de: hai(
      bai(`Xe A ${u('2{,}0', 'kg')} chạy ${u('3{,}0', 'm/s')} và xe B ${u('4{,}0', 'kg')} chạy ${u('2{,}0', 'm/s')} ngược chiều nhau trên ray ngang, va chạm rồi dính lại. Bỏ qua ma sát.`, [['a', `Vận tốc hai xe ngay sau va chạm ${chieu}?`], ['b', 'A giữ nguyên: B phải chạy ngược chiều A nhanh bao nhiêu để sau va chạm hai xe đứng yên?']], ds(oS('a'), oC('theo chiều A', 'theo chiều B'), oS('b'))),
      bai(`Người ${u('60', 'kg')} chạy ${u('4{,}0', 'm/s')} nhảy lên xe goòng ${u('140', 'kg')} trên ray ngang. Bỏ qua ma sát.`, [['a', `Goòng đang chạy ngược chiều người với ${u('1{,}0', 'm/s')}: vận tốc người và goòng ngay sau đó ${chieu}?`], ['b', `Goòng chạy cùng chiều người với ${u('1{,}0', 'm/s')}: vận tốc ngay sau đó?`]], ds(oS('a'), oC('theo chiều người', 'theo chiều goòng'), oS('b')))) },
    { t: 'Dạng 5 · Chuyển động bằng phản lực', k: 0, de: hai(
      bai(`Súng ${u('3{,}0', 'kg')} (không kể đạn) đặt tự do, bắn đạn ${u('15', 'g')} theo phương ngang với ${u('600', 'm/s')} so với đất.<br>Cho ${nw(m('1\\ \\mathrm{g}=0{,}001\\ \\mathrm{kg}'))}.`, [['a', `Vận tốc giật của súng ${chieu}?`], ['b', `Người tì chặt súng vào vai, súng + người nặng ${u('63', 'kg')}: tốc độ giật lúc này?`]], ds(oS('a'), oC('cùng chiều đạn', 'ngược chiều đạn'), oS('b'))),
      bai(`Tên lửa mô hình ${u('1{,}2', 'kg')} (kể cả khí) đứng yên trên ray đệm khí, phụt tức thời ${u('0{,}20', 'kg')} khí về sau với ${u('40', 'm/s')} so với đất.`, [['a', 'Khối lượng phần tên lửa còn lại?'], ['b', `Vận tốc tên lửa ngay sau khi phụt ${chieu}?`]], ds(oS('a'), oS('b'), oC('cùng chiều khí', 'ngược chiều khí')))) + nhap(NHAP[1]) },
  ]],
  dap: [
    'D1·1: a) kín (trọng lực cân bằng phản lực, ma sát ≈ 0) · b) 0,20 m/s; cùng chiều cũ &nbsp;|&nbsp; D1·2: a) 0,60 kg·m/s · b) 0,60 m/s; bật ngược &nbsp;|&nbsp; D2·1: a) 1,0 m/s · b) 1,2 m/s &nbsp;|&nbsp; D2·2: a) 2,0 m/s · b) 447 J &nbsp;|&nbsp; D3·1: a<sub>1</sub>) 0,18 kg·m/s · a<sub>2</sub>) 0,18 kg·m/s · b<sub>1</sub>) 0,081 J · b<sub>2</sub>) 0,081 J · c) đàn hồi &nbsp;|&nbsp; D3·2: a) 0,40 m/s · b<sub>1</sub>) 0,090 J · b<sub>2</sub>) 0,060 J · c) 33 %',
    'D4·1: a) 0,33 m/s; theo chiều B · b) 1,5 m/s &nbsp;|&nbsp; D4·2: a) 0,50 m/s; theo chiều người · b) 1,9 m/s &nbsp;|&nbsp; D5·1: a) 3,0 m/s; ngược chiều đạn · b) 0,14 m/s &nbsp;|&nbsp; D5·2: a) 1,0 kg · b) 8,0 m/s; ngược chiều khí',
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 2], kq: [[1, 2, 3], [4, 5]] },
  tuongTu,
  tra: 'hệ kín 1·4 · định luật 2·1 · thí nghiệm ray đệm khí 2·2 · mềm/đàn hồi 2·3 · phản lực 3·1 · bẫy 3·2 · dạng 1–3 → 6·1 · dạng 4–5 → 7·1',
  out: process.argv[2],
});
