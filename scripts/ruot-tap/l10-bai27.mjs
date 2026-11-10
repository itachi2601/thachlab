// Ruột tập Vật lí 10 – Bài 27 · Hiệu suất (lesson id 72). Quyển L10 Chương 4 (bài 23–27): bài này là tr. 49–60.
// Khung: khung.mjs (bố cục bài 14 có trang Bài tương tự); hình: hinh-l10-bai27.mjs (SVG tự vẽ, không dùng ảnh Halliday).
// Nguồn nội dung: bài web lesson 72 (book/cache/72.json của worktree sach-in-tu-web-chuong-3): lý thuyết I–VI + 5 dạng bài tập mẫu.
// Đáp số bài tương tự tính bằng Python (xem báo cáo phiên 10/11/2026); số liệu bài toán mẫu, thí nghiệm, thử thách lấy đúng bài web.
// Chạy: node scripts/ruot-tap/l10-bai27.mjs [file.pdf] → scripts/ruot-tap/out/ruot-tap-vl10-bai27.pdf
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai, dapSo, TRANG_DAU } from './khung.mjs';
import { hinhBai27 as H } from './hinh-l10-bai27.mjs';
const K = khoiTao({ bai: 27, lid: 72, ten: 'HIỆU SUẤT', lop: 10, baiDau: 23, sub: 'Vật lí 10 · Chương 4: Năng lượng, công, công suất' });
const { head, h3, foot } = K;
const tr = (n) => (27 - 23) * 12 + TRANG_DAU - 1 + n; // số trang tuyệt đối trong quyển
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const W = (s) => m(`W_{\\mathrm{${s}}}`), P = (s) => m(`P_{\\mathrm{${s}}}`);
const pct = (s) => m(`${s}\\,\\%`);
const u = (s, d) => m(`${s}\\ \\mathrm{${d}}`);

const fn = f(12), fw = f(25); // ô số ≥12 mm, ô chữ ≥25 mm (HS ảo 10/11)
const fp = (w, p) => nw(`${f(w)}${p}`); // ô + dấu câu dính nhau, không để "." hay ";" mồ côi đầu dòng
const pc = (w = 12) => nw(`${f(w)}&nbsp;%`);
const g10 = nw(m('g=10\\ \\mathrm{m/s^2}'));
const Hp = (s) => nw(m(`H=${s}\\,\\%`));
// Dòng viết tự do cao 9 mm cho chỗ phải viết phân số
const ph = (lab, tail = '') => `<div class="ln" style="height:9mm;display:flex;align-items:center;gap:1.5mm"><span>${lab}</span><span style="flex:1"></span>${tail}</div>`;

const p1 = `<section class="page">
${head('BÀI 27 · HIỆU SUẤT', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
<div style="margin:.3mm 0">${ck}Phân biệt năng lượng <b>có ích</b> và <b>hao phí</b> của một máy</div>
<div style="margin:.3mm 0">${ck}Tính <b>hiệu suất</b> theo năng lượng và theo công suất</div>
<div style="margin:.3mm 0">${ck}Giải thích vì sao ${m('H')} luôn nhỏ hơn 100&nbsp;%; biết cách giảm hao phí</div>
<div style="margin:.3mm 0">${ck}Tính hiệu suất khi <b>ghép nhiều máy nối tiếp</b></div>
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Bóng sợi đốt ${nw('60 W')} và bóng LED ${nw('9 W')} sáng ngang nhau. Sau mười phút, bóng sợi đốt nóng hơn hẳn. Điện năng bóng sợi đốt nhận vào đã đi đâu?</p>
<div class="fig-side" style="${fs(42)}"><div>
${opt('A', 'Phần không thành ánh sáng thì biến mất')}
${opt('B', 'Một phần thành ánh sáng, phần còn lại thành nhiệt')}
${opt('C', 'Bóng tự tạo thêm năng lượng cho mình')}
${opt('D', 'Toàn bộ thành ánh sáng, chỉ dây dẫn nóng')}
<div style="margin-top:1mm">${chon(12)}</div><div class="ln"><span class="hint">Vì sao?</span></div></div>
${H.haiBong()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${fn} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Năng lượng có ích và hao phí', '1·4')}
<div class="card fig-side" style="${fs(44)};padding:1.2mm 3mm"><div>
<div>${m('W_{\\mathrm{tp}}=')} ${fw} + ${fw}</div>
<div>Toàn phần ${W('tp')}: năng lượng máy ${fp(25, '.')}</div>
<div>Có ích ${W('ci')}: phần thành dạng ${fp(25, '.')}</div>
<div>Hao phí ${W('hp')}: thành ${fw}, ${fp(25, '.')}</div>
<div>Hao phí không ${fp(25, ';')}</div>
<div>năng lượng vẫn ${fp(25, '.')}</div></div>
${H.baLoai('Bề dày dải tỉ lệ năng lượng.')}</div>
${h3(5, 'Thí nghiệm: sờ vỏ quạt bàn', '1·5')}
<div class="card fig-side" style="${fs(33)};padding:1.2mm 3mm"><div>
<div><b>Làm:</b> bật quạt ${nw('10 phút')}; áp tay lên vỏ động cơ (1), rồi chân đế (2); không chạm cánh.</div>
<div><b>Quan sát:</b> chỗ ${fn} ấm hơn rõ; nghe tiếng ${fp(25, '.')}</div>
<div><b>Rút ra:</b> điện năng không thành hết ${fp(25, ';')}</div>
<div>một phần thành ${fw}, ${fp(25, ':')} ${W('hp')}.</div></div>
${H.quat('')}</div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('HIỆU SUẤT · VÁN NGHIÊNG · GHÉP NỐI TIẾP')}
${h3(1, 'II.2 · Hiệu suất', '2·1')}
<div class="card" style="padding:.6mm 3mm 1.2mm">
<div style="display:grid;grid-template-columns:1fr 1fr;gap:5mm">${ph(`<b>Theo năng lượng:</b> ${m('H=')}`)}${ph(`<b>Theo công suất:</b> ${m('H=')}`)}</div>
<div>${m('H')} cho biết bao nhiêu % năng lượng nhận vào thành ${fp(25, '.')}</div>
<div>${m('H')} không có ${fp(25, '.')}</div>
<div>Máy thật: ${m('H')} ${fn} 100&nbsp;%. Dạng theo công suất có được vì ${m('P=')} ${fp(25, '.')}</div>
${ph(`Bóng sợi đốt ${nw('60 W')} cho ${nw('3,6 W')} ánh sáng: ${m('H=')}`, `= ${pc()}`)}
${ph(`Bóng LED ${nw('9 W')} cho cùng ${nw('3,6 W')} ánh sáng: ${m('H=')}`, `= ${pc()}`)}</div>
${h3(2, 'Thí nghiệm: hiệu suất của ván nghiêng', '2·2')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div><b>Làm:</b> kéo đều xe gỗ ${nw('0,40 kg')} lên ván bằng lực kế tới độ cao ${nw(m('h=20\\ \\mathrm{cm}'))}, ở bốn góc ${m('\\alpha')} (${g10}).</div>
<div>Có ích luôn là ${m('W_{\\mathrm{ci}}=mgh=')} ${nw(`${fn}&nbsp;J`)}</div>
<div>Toàn phần là công ta bỏ ra: ${m('W_{\\mathrm{tp}}=')} ${fw}</div></div>
${H.vanNghieng('')}</div>
<table class="tbl-ct"><tr><th>Góc ${m('\\alpha')}</th><th>15°</th><th>25°</th><th>35°</th><th>45°</th></tr>
<tr><td>${m('W_{\\mathrm{tp}}=Fs')} (J)</td><td>1,55</td><td>1,22</td><td>1,09</td><td>1,00</td></tr>
<tr><td>${m('W_{\\mathrm{hp}}')} (J)</td><td></td><td></td><td></td><td></td></tr>
<tr><td>${m('H')} (%)</td><td></td><td></td><td></td><td></td></tr></table>
<div style="margin:.8mm 0 0">Cả bốn lần ${m('H')} ${fn} 100&nbsp;% vì có ${fp(25, '.')} Ván ${fw} cho ${m('H')} cao nhất.</div>
<div>Ván thoải: quãng đường ${m('s')} ${fw}, công ma sát ${fp(25, ',')}</div>
<div>nên hao phí ${fp(25, '.')}</div>
${wl('Sai số đến từ đâu?', 2)}
${h3(3, 'II.3 · Vì sao H < 100 %; ghép nhiều máy', '2·3')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div>Ma sát, dây dẫn nóng, rung, kêu ⇒ ${m('W_{\\mathrm{hp}}')} ${nw(`${fn}&nbsp;0.`)}</div>
<div>Ròng rọc, ván nghiêng: không lợi về ${fp(25, '.')}</div>
<div>Nối tiếp: ${m('H=')} ${fp(25, ';')}</div>
<div>đổi mỗi ${m('H')} ra ${fw} rồi nhân.</div>
<div>Ví dụ hình bên: ${m('H=')} ${fn} · ${fn} = ${pc()}</div>
<div>Giảm hao phí: ${fw}, ${fp(25, '.')}</div></div>
${H.noiTiep('Số minh hoạ: khâu sau nhận phần ra của khâu trước.')}</div>
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('BẪY · TRẢ BÀI · KẾT QUẢ TỰ KIỂM TRA')}
${h3(1, 'III · Ba cái bẫy hay sập', '3·1')}
<div class="card fig-side" style="${fs(40)};padding:1mm 3mm"><div>
<div class="trap">${ck}<span><b>“Hiệu suất cao thì máy mạnh.”</b> Máy mạnh là ${P('ci')} lớn; ${m('H')} chỉ là tỉ lệ: ${m('P_{\\mathrm{ci}}=H\\cdot P_{\\mathrm{tp}}')}.</span></div>
<div class="trap">${ck}<span><b>Lấy nhầm tử và mẫu.</b> Tử là có ích, mẫu là toàn phần; ${m('H')} không đơn vị, “120 %” là vô lí. Đề cho hao phí thì trừ ra ${W('ci')} trước.</span></div>
<div class="trap">${ck}<span><b>“Ghép hai máy thì cộng hiệu suất.”</b> Nối tiếp thì nhân: ${m('H=H_1H_2')}, nhỏ hơn từng khâu.</span></div></div>
${H.haiMay()}</div>
${h3(2, 'IV · Trả bài 6 câu', '3·2')}
${box(`${tb('1. Hiệu suất là gì? Viết hai công thức.')}${lines(2)}
${tb('2. Năng lượng toàn phần, có ích, hao phí liên hệ thế nào?')}${lines(2)}
${tb('3. Vì sao H luôn nhỏ hơn 100 %?')}${lines(2)}
${tb('4. Hiệu suất khác công suất ở chỗ nào?')}${lines(2)}
${tb('5. Ghép hai máy nối tiếp thì hiệu suất cả hệ tính thế nào?')}${lines(2)}
${tb('6. Đọc đề, nhận ra phần có ích và phần toàn phần bằng cách nào?')}${lines(2)}`)}
<div class="card soft" style="margin-top:1.5mm;padding:1mm 3mm"><b>Bạn cùng bàn kiểm:</b> nói được ……/6 câu · câu chưa thuộc: ${fw} ${nw(`→ đọc lại ô Tập ${fn}`)}</div>
${h3(3, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '3·3')}
${rkHai([1, 2, 3], [4, 5, 6])}
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('BÀI TOÁN MẪU · THANG MÁY CHUNG CƯ')}
${h3(1, 'V · Đề bài', '4')}
<div class="card soft" style="padding:1.2mm 3mm">Thang máy nâng đều cabin cùng người ${u('300', 'kg')} lên cao ${u('5', 'm')} trong ${u('20', 's')}. Động cơ tiêu thụ công suất điện ${u('1{,}25', 'kW')}. Lấy ${g10}.
<div><b>a)</b> Tính công suất có ích.</div><div><b>b)</b> Tính hiệu suất của thang máy.</div><div><b>c)</b> Tính nhiệt hao phí toả ra trong 20 s.</div></div>
${h3(2, 'Phân tích đề')}
<table><tr><th style="width:44mm">Câu trong đề</th><th style="width:34mm">Dữ liệu</th><th>Kiến thức liên quan</th></tr>
<tr><td>“cabin cùng người 300&nbsp;kg”</td><td>${m('m=300\\ \\mathrm{kg}')}</td><td>trọng lượng ${m('mg')}</td></tr>
<tr><td style="height:6.5mm">“nâng đều, cao 5&nbsp;m”</td><td></td><td></td></tr>
<tr><td style="height:6.5mm">“trong 20&nbsp;s”</td><td></td><td></td></tr>
<tr><td style="height:6.5mm">“điện tiêu thụ 1,25&nbsp;kW”</td><td></td><td></td></tr>
<tr><td style="height:6.5mm">“nhiệt hao phí”</td><td></td><td></td></tr></table>
${h3(3, 'Giải')}
<div class="fig-side" style="${fs(38)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl('a)', 3)}${wl('b)', 3)}${wl('c)', 4)}${wl(`Kiểm tra: ${m('P_{\\mathrm{ci}}/P_{\\mathrm{tp}}=')} …… ${nw('&lt; 100&nbsp;%?')}`, 1)}</div>${H.thangMay()}</div>
${h3(4, 'Điền bước còn thiếu: tải 200&nbsp;kg')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div class="ln" style="height:auto;padding-top:1mm"><b>Đề:</b> cùng thang máy, nâng tải ${nw('200 kg')} lên ${nw('6 m')} trong ${nw('12 s')}, điện tiêu thụ ${nw('2,0 kW')}.</div>
${wl(`Bước 1: ${m('W_{\\mathrm{ci}}=')} …`, 2)}${wl(`Bước 2: ${m('P_{\\mathrm{ci}}=')} …`, 2)}
<div class="ln"><b>Bước 3 (cho sẵn):</b> ${m('H=P_{\\mathrm{ci}}/P_{\\mathrm{tp}}=')} …… ; so với câu b): ……</div></div>
<div class="card soft" style="margin-top:1.5mm;padding:1mm 3mm"><b>Em tự kiểm:</b> ${ck}đổi kW ra W &nbsp;${ck}${m('H')} &lt; 100&nbsp;% &nbsp;${ck}có ghi đơn vị</div>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TẬP VỀ NHÀ · MANG VỀ · THỬ THÁCH')}
${K.btvn()}
${h3(2, 'VI · Mang về: điều em dễ quên nhất', '5')}
${box(wl('1.', 2) + wl('2.', 2) + wl('3.', 2))}
${h3(3, 'Thử thách phân tầng')}
<div class="fig-side" style="${fs(40)}">${box(wl(`★ Máy có ${nw(m('P_{\\mathrm{ci}}=800\\ \\mathrm{W}'))}, ${Hp('80')}. Công suất toàn phần?`, 2)
 + wl(`★★ Tấm pin ${u('1{,}6', 'm^2')} nhận ${u('1000', 'W/m^2')}, ${Hp('20')}. Công suất điện?`, 3)
 + wl(`★★★ Động cơ ${pct('90')}, hộp giảm tốc ${pct('80')}, vít me ${pct('75')} nối tiếp. Cần ${u('2{,}7', 'kW')} ở cuối thì điện vào bao nhiêu?`, 4))}${H.pinMT()}</div>
${h3(4, 'Đời sống: nơi đang dùng bài này')}
<div class="card" style="padding:1.2mm 3mm">
<div>Động cơ xăng của xe máy: ${m('H')} chỉ cỡ ${nw('25–30&nbsp;%')}; bảo dưỡng xích, nhớt để bớt ${fp(25, '.')}</div>
<div>Pin mặt trời: chỉ ${nw('15–20&nbsp;%')} ánh sáng thành điện, còn lại thành ${fp(25, '.')}</div>
<div>Quạt, máy giặt: ổ trục, dầu bôi trơn giảm ${fp(25, ';')}</div>
<div>thay bóng sợi đốt bằng ${fw} để tiết kiệm điện.</div></div>
${h3(5, 'Thử sức đổi chiều: biết hiệu suất, tìm điện năng')}
${box(wl(`Thang máy ở tr.&nbsp;${tr(4)} thay động cơ ${Hp('75')}, vẫn nâng ${nw('300 kg')} lên ${nw('5 m')} trong ${nw('20 s')}. Tìm ${P('tp')} và số oát tiết kiệm được.`, 3))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Năng lượng toàn phần, có ích, hao phí',
    de: `Mỗi lần khoan, máy khoan nhận ${u('150', 'kJ')} điện năng, ${u('105', 'kJ')} thành cơ năng; còn lại làm nóng vỏ, ồn, rung.<br><b>a)</b> năng lượng hao phí mỗi lần khoan<br><b>b)</b> phần hao phí mất đi hay chuyển sang dạng nào<br><b>c)</b> tra dầu xong hao phí còn ${u('25', 'kJ')}, có ích vẫn ${u('105', 'kJ')}: điện năng mỗi lần khoan`,
    nd: `${m('W_{\\mathrm{tp}}=')} ${fw} + ${fp(25, ':')} biết hai, suy ra cái thứ ba`, a: ['a', 'b', 'c'], gi: 4, fig: H.khoan('') },
  { t: 'Dạng 2 · Dễ · Hiệu suất theo năng lượng và theo công suất',
    de: `Máy bơm nước chạy ${nw('5 phút')}, nhận điện năng ${u('540', 'kJ')}, truyền cho nước cơ năng ${u('405', 'kJ')}.<br><b>a)</b> hiệu suất máy bơm<br><b>b)</b> công suất toàn phần và có ích<br><b>c)</b> dùng hai công suất tính lại ${m('H')}, so với câu a`,
    nd: `${m('H')} = phần ${fw} chia phần ${fp(25, ';')} ${m('t')} đổi ra ${fp(12, '.')}`, a: ['a', 'b', 'c'], gi: 3 },
  { t: 'Dạng 3 · Trung bình · Cho hiệu suất, tìm công suất hoặc năng lượng',
    de: `Động cơ xe đạp điện có ${Hp('80')}.<br><b>a)</b> nhận ${u('250', 'W')} điện: công suất cơ có ích<br><b>b)</b> cần công có ích ${u('144', 'kJ')}: điện năng phải nhận<br><b>c)</b> năng lượng hao phí ở câu b`,
    nd: `Đổi ${m('H')} ra ${fp(25, ';')} ${nw(m('P_{\\mathrm{ci}}=H\\cdot P_{\\mathrm{tp}}'))}; ${m('W_{\\mathrm{tp}}=W_{\\mathrm{ci}}')} ${fw} ${m('H')}`, a: ['a', 'b', 'c'], gi: 3 },
  { t: 'Dạng 4 · Trung bình · Hiệu suất của tời kéo vật lên cao',
    de: `Tời điện kéo đều thùng vữa ${u('350', 'kg')} lên cao ${u('12', 'm')} trong ${u('24', 's')} qua ròng rọc cố định; công suất điện ${u('2{,}5', 'kW')}; ${g10}.<br><b>a)</b> công có ích<br><b>b)</b> công suất có ích và hiệu suất<br><b>c)</b> năng lượng hao phí trong thời gian kéo`,
    nd: `Kéo đều ⇒ ${m('W_{\\mathrm{ci}}=')} ${fp(25, ';')} ${m('W_{\\mathrm{tp}}=')} ${fp(25, ';')} hao phí = hiệu hai số`, a: ['a', 'b', 'c'], gi: 6, fig: H.toi(''), cot: 2 },
  { t: 'Dạng 5 · Khó · Ghép nhiều khâu nối tiếp và giảm hao phí',
    de: `Xe điện nhỏ: pin → bộ điều khiển (${pct('95')}) → động cơ (${pct('80')}) → hộp số (${pct('75')}) → bánh xe.<br><b>a)</b> hiệu suất cả hệ<br><b>b)</b> bánh xe nhận ${u('5{,}7', 'kJ')} có ích: pin phải cấp bao nhiêu<br><b>c)</b> thay MỘT khâu bằng khâu ${pct('90')}: thay khâu nào để ${m('H')} lớn nhất, ${m('H')} khi đó`,
    nd: `Nối tiếp ⇒ ${m('H=')} ${fp(25, ';')} thay khâu có ${m('H')} ${fw} thì lợi nhất`, a: ['a', 'b', 'c'], gi: 6, fig: H.baKhau(''), cot: 2 },
];

// Bài tương tự: mỗi dạng 2 bài đặt cạnh nhau (2 cột) để mỗi ý có dòng câu hỏi + ≥1 dòng kẻ riêng (HS ảo 10/11: tr.56 chỉ 1 dòng/ý).
// Đáp số tính bằng Python, in lật ngược. Khung chưa có bố cục 2 cột nên chèn CSS ngay trong de của bài đầu.
const ttCss2 = `<style>.tt:has(.tt2)>.hd>span:last-child{display:none}.tt2{display:grid;grid-template-columns:1fr 1fr;gap:0 4mm}.tt2>div{min-width:0}
.tt2 .h2{display:flex;justify-content:space-between;align-items:center;font-weight:700;color:var(--navy);border-bottom:.2mm solid var(--grid);margin-bottom:.3mm}
.tt2 .h2>span:last-child{font-weight:400;color:var(--ink);white-space:nowrap}.tt2 .q{margin-top:.5mm}</style>`;
const okS = '<span><span class="ck"></span>đúng &nbsp;<span class="ck"></span>sai, đã sửa</span>';
// Giải vào vở (thầy chốt 10/11): mỗi ý một dòng câu hỏi, cuối bài một hàng ô đáp số (dapSo); o mặc định = nhãn các ý, ý 2 kết quả tách b<sub>1</sub>/b<sub>2</sub>.
const bai = (stmt, ys, o = ys.map((y) => y[0])) => `<div>${stmt}</div>` + ys.map(([lab, q]) => `<div class="q"><b>${lab})</b> ${q}</div>`).join('') + dapSo(o);
const NHAP = [1, 6]; // số dòng nháp cuối tr.8, tr.9 — đổ cho dư 0–15 mm
const nhap = (n) => `<div style="margin-top:2mm;border-top:.3mm solid var(--grid);padding-top:.8mm"><b>Nháp / chỗ em còn vướng</b>${lines(n)}</div>`;
const hai = (a, b, css = '') => `${css}<div class="tt2">${[a, b].map((x, i) => `<div><div class="h2"><span>Bài ${i + 1}</span>${okS}</div>${x}</div>`).join('')}</div>`;
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–3', 'DẠNG 4–5'],
  trang: [[
    { t: 'Dạng 1 · Toàn phần, có ích, hao phí', k: 0, de: hai(
      bai(`Máy xay sinh tố nhận ${u('60', 'kJ')} điện năng, ${u('42', 'kJ')} thành cơ năng quay lưỡi dao.`, [['a', 'Năng lượng hao phí?'], ['b', 'Hao phí chuyển sang những dạng nào?']]),
      bai(`Động cơ ô tô nhận ${u('800', 'kJ')} từ xăng, hao phí ${u('560', 'kJ')}.`, [['a', 'Công có ích?'], ['b', `Bảo dưỡng xong hao phí còn ${u('500', 'kJ')}, có ích giữ nguyên: năng lượng toàn phần mới?`]]), ttCss2) },
    { t: 'Dạng 2 · Hiệu suất theo năng lượng và công suất', k: 0, de: hai(
      bai(`Quạt điện chạy ${nw('10 phút')}, nhận ${u('36', 'kJ')} điện năng, cho ${u('28{,}8', 'kJ')} cơ năng có ích.`, [['a', 'Hiệu suất?'], ['b', 'Công suất toàn phần (b<sub>1</sub>) và có ích (b<sub>2</sub>)?']], ['a', 'b<sub>1</sub>', 'b<sub>2</sub>']),
      bai(`Máy nâng hàng trong ${nw('2 phút')} nhận ${u('96', 'kJ')} điện năng, sinh công có ích ${u('60', 'kJ')}.`, [['a', 'Hiệu suất?'], ['b', 'Công suất toàn phần (b<sub>1</sub>) và có ích (b<sub>2</sub>)?'], ['c', 'Công suất hao phí?']], ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c'])) },
    { t: 'Dạng 3 · Cho hiệu suất, tìm công suất hoặc năng lượng', k: 0, de: hai(
      bai(`Máy bơm có ${Hp('70')}.`, [['a', `Nhận ${u('1{,}5', 'kW')} điện: công suất có ích?`], ['b', `Cần cơ năng có ích ${u('210', 'kJ')}: điện năng phải nhận?`], ['c', 'Năng lượng hao phí ở câu b?']]),
      bai(`Động cơ có ${Hp('85')}, công suất có ích ${u('1{,}7', 'kW')}.`, [['a', 'Công suất toàn phần?'], ['b', `Điện năng tiêu thụ trong ${nw('10 phút')}?`], ['c', `Nhiệt hao phí trong ${nw('10 phút')}?`]])) + nhap(NHAP[0]) },
  ], [
    { t: 'Dạng 4 · Hiệu suất của máy kéo vật lên cao', k: 0, de: hai(
      bai(`Cần cẩu nâng đều kiện hàng ${u('500', 'kg')} lên cao ${u('18', 'm')} trong ${u('30', 's')}; công suất điện ${u('4{,}0', 'kW')}; ${g10}.`, [['a', 'Công có ích?'], ['b', 'Công suất có ích (b<sub>1</sub>) và hiệu suất (b<sub>2</sub>)?'], ['c', `Năng lượng hao phí trong ${nw('30 s')}?`]], ['a', 'b<sub>1</sub>', 'b<sub>2</sub>', 'c']),
      bai(`Kéo đều thùng hàng ${u('50', 'kg')} lên ván nghiêng dài ${u('3{,}0', 'm')}, cao ${u('1{,}2', 'm')}, lực kéo ${u('250', 'N')} dọc ván; ${g10}.<div class="hint">Gợi ý: đề không cho ma sát. Công toàn phần = lực kéo × chiều dài ván; hao phí = toàn phần − có ích.</div>`, [['a', 'Công có ích?'], ['b', 'Công toàn phần?'], ['c', 'Hiệu suất?'], ['d', 'Công hao phí?']])) },
    { t: 'Dạng 5 · Ghép nhiều khâu nối tiếp', k: 0, de: hai(
      bai(`Động cơ (${pct('90')}) nối với hộp giảm tốc (${pct('70')}).`, [['a', 'Hiệu suất cả hệ?'], ['b', `Đầu ra cần ${u('3{,}15', 'kJ')}: điện năng vào?`], ['c', 'Tổng năng lượng hao phí?']]),
      bai(`Sạc xe điện: bộ sạc (${pct('90')}) → pin (${pct('80')}) → động cơ (${pct('85')}).`, [['a', 'Hiệu suất cả chuỗi?'], ['b', `Thay MỘT khâu bằng khâu ${pct('95')}: thay khâu nào (b<sub>1</sub>) để hiệu suất lớn nhất? Hiệu suất khi đó (b<sub>2</sub>)?<div class="hint">Gợi ý: thử thay lần lượt cả 3 khâu, mỗi lần tính lại ${m('H')} cả chuỗi rồi so.</div>`]], ['a', 'b<sub>1</sub>', 'b<sub>2</sub>'])) + nhap(NHAP[1]) },
  ]],
  dap: [
    'D1·1: a) 18 kJ · b) nhiệt, âm, rung &nbsp;|&nbsp; D1·2: a) 240 kJ · b) 740 kJ &nbsp;|&nbsp; D2·1: a) 80 % · b<sub>1</sub>) 60 W · b<sub>2</sub>) 48 W &nbsp;|&nbsp; D2·2: a) 62,5 % · b<sub>1</sub>) 800 W · b<sub>2</sub>) 500 W · c) 300 W &nbsp;|&nbsp; D3·1: a) 1050 W · b) 300 kJ · c) 90 kJ &nbsp;|&nbsp; D3·2: a) 2000 W · b) 1200 kJ · c) 180 kJ',
    'D4·1: a) 90 000 J · b<sub>1</sub>) 3000 W · b<sub>2</sub>) 75 % · c) 30 000 J &nbsp;|&nbsp; D4·2: a) 600 J · b) 750 J · c) 80 % · d) 150 J &nbsp;|&nbsp; D5·1: a) 63 % · b) 5,0 kJ · c) 1,85 kJ &nbsp;|&nbsp; D5·2: a) 61,2 % · b<sub>1</sub>) thay pin · b<sub>2</sub>) 72,7 %',
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 2], kq: [[1, 2, 3], [4, 5]] },
  tuongTu,
  tra: 'có ích – hao phí 1·4 · thí nghiệm quạt 1·5 · hiệu suất 2·1 · ván nghiêng 2·2 · nối tiếp 2·3 · bẫy 3·1 · dạng 1–3 → 6·1 · dạng 4–5 → 7·1',
  out: process.argv[2],
});
