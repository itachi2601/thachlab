// Ruột tập Vật lí 10 – Bài 24 · Công suất (lesson id 69), tr. 13–24 của quyển Chương 4. Khung: khung.mjs (bố cục bài 14 có Bài tương tự);
// hình: hinh-l10-bai24.mjs (SVG tự vẽ, không dùng ảnh Halliday). Nội dung theo bài web (book/cache/69.json): khung ghi bài theo mục I–VI,
// 3 bẫy, Trả bài 6 câu, bài toán mẫu thang máy 800 kg, 5 dạng bài tập mẫu. Bài tương tự: 2 bài/dạng, đáp số tính bằng Python (lật ngược).
// Chạy: node scripts/ruot-tap/l10-bai24.mjs [file.pdf] → scripts/ruot-tap/out/ruot-tap-vl10-bai24.pdf
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhL10b24 as H } from './hinh-l10-bai24.mjs';
const K = khoiTao({ bai: 24, lid: 69, ten: 'CÔNG SUẤT', lop: 10, baiDau: 23, sub: 'Vật lí 10 · Chương 4: Năng lượng, công, công suất' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const dd = (de, k) => `<div style="padding-top:.8mm">${de}</div>` + lines(k);   // đề trên, k dòng kẻ dưới (nhãn dài trong .ln bị tràn đè dòng)
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const u = (s) => nw(m(`\\mathrm{${s}}`));
const g10 = nw(m('g=10\\ \\mathrm{m/s^2}'));
const sao = (k) => m('\\bigstar'.repeat(k).replace(/\\bigstar\\bigstar/g, '\\bigstar\\,\\bigstar'));

const p1 = `<section class="page">
${head('BÀI 24 · CÔNG SUẤT', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
<div style="margin:.3mm 0">${ck}Hiểu công suất ${nw(m('P=A/t') + ':')} sinh công <b>nhanh hay chậm</b></div>
<div style="margin:.3mm 0">${ck}Đổi W, kW, MW, mã lực; nhớ <b>kWh là đơn vị của công</b></div>
<div style="margin:.3mm 0">${ck}Dùng ${m('P=Fv')} cho công suất tức thời; giải thích vì sao xe lên dốc phải giảm số</div>
<div style="margin:.3mm 0">${ck}Không nhầm <b>công suất lớn</b> với <b>công lớn</b></div>
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<div class="fig-side" style="${fs(50)}"><div>
<p style="margin:0 0 1mm">Điều gì khác nhau giữa hai thang máy?</p>
${opt('A', 'Công của thang A lớn hơn, vì nó nâng nhanh hơn')}
${opt('B', 'Công bằng nhau, thang A sinh công nhanh hơn')}
${opt('C', 'Công của thang B lớn hơn, vì nó làm việc lâu hơn')}
${opt('D', 'Hai thang giống hệt nhau, vì cùng nâng một thùng')}
<div style="margin-top:1mm">${chon(10)}</div><div class="hint">Vì sao?</div>${lines(1)}</div>
${H.haiThangMay()}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Công suất trung bình', '1·4')}
<div class="card" style="padding:1.2mm 3mm">
<div>Công suất đặc trưng cho ${f(28)} sinh công: bằng ${f(25)} sinh ra trong một ${f(25)} thời gian.</div>
<div>${m('P=')} ${f(12)} / ${f(12)} &nbsp;· ${nw(m('P') + ':')} ${f(25)} (W) · ${nw(m('A') + ':')} ${f(25)} (J) · ${nw(m('t') + ':')} ${f(25)} (s)</div>
<div>Mở bài (${g10}): cả hai thang ${m('A=mgh=')} ${nw(`${f(16)}&nbsp;J`)}</div>
<div>Thang A: ${m('P=')} ${nw(`${f(14)}&nbsp;W`)}; &nbsp;thang B: ${m('P=')} ${nw(`${f(14)}&nbsp;W`)}</div>
<div>Đèn ${u('10\\ W')} tiêu thụ ${nw(`${f(12)}&nbsp;J`)} điện mỗi ${f(25)}.</div></div>
${h3(5, 'II.2 · Đơn vị công suất', '1·5')}
<table style="text-align:center"><tr><th>${u('1\\ W')}</th><th>${u('1\\ kW')}</th><th>${u('1\\ MW')}</th><th>1 CV (Pháp)</th><th>1 HP (Anh)</th></tr>
<tr><td style="height:6.5mm">${f(12)} J/s</td><td>${f(14)} W</td><td>${f(14)} W</td><td>736 W</td><td>746 W</td></tr></table>
<div class="card" style="padding:1mm 3mm;margin-top:1.2mm">
<div>${u('1\\ kWh')} là đơn vị của ${f(25)}, không phải công suất: ${u('1\\ kWh=')} ${nw(`${f(18)}&nbsp;J`)}</div>
<div>Thang A ${u('10\\ kW')} ${m('\\approx')} ${nw(`${f(12)}&nbsp;CV`)}; &nbsp;máy ${u('1\\ kW')} chạy 1 giờ tiêu thụ ${nw(`${f(12)}&nbsp;kWh`)}</div></div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('THÍ NGHIỆM LEO CẦU THANG · P = F·v')}
${h3(1, 'Thí nghiệm: leo cầu thang', '2·1')}
<div class="card fig-side" style="${fs(46)};padding:1.2mm 3mm"><div>
<div><b>Làm:</b> bạn ${u('50\\ kg')} leo cầu thang cao ${u('3{,}0\\ m')} bốn lần, mỗi lần nhanh hơn; bạn khác bấm giờ.</div>
<div><b>Quan sát:</b> thời gian giảm dần; leo nhanh thì mệt hơn.</div>
<table class="tbl-ct" style="margin:.8mm 0;text-align:center"><tr><th>Lần</th><th>1</th><th>2</th><th>3</th><th>4</th></tr>
<tr><td>${m('t')} (s)</td><td>12,0</td><td>8,5</td><td>6,0</td><td>4,0</td></tr>
<tr><td>${m('P')} (W)</td><td></td><td></td><td></td><td></td></tr></table>
<div>Mỗi lần ${m('A=mgh=')} ${nw(`${f(14)}&nbsp;J`)} (${g10})</div></div>
${H.cauThang()}</div>
<div class="card" style="padding:1mm 3mm">
<div><b>Rút ra:</b> công nâng người ${f(25)}; leo nhanh hơn thì công suất ${f(25)}.</div>
<div>Đồng hồ bấm tay sai ${nw(u('0{,}3\\ s') + ':')} lần ${f(12)} bị ảnh hưởng nhiều nhất, vì</div>${lines(1)}</div>
${h3(2, 'II.3 · Công suất, lực và vận tốc', '2·2')}
<div class="card" style="padding:1.2mm 3mm">
<div>Lực ${m('F')} không đổi, cùng hướng độ dịch chuyển: ${m('A=F\\,d=F\\,v_{tb}\\,t')} ${nw(`${m('\\Rightarrow')} ${m('P=\\dfrac{A}{t}=')} ${f(12)} · ${f(12)}`)}</div>
<div>Khoảng thời gian rất nhỏ: ${m('v_{tb}')} thành vận tốc ${f(25)}; ${m('P=Fv')} là công suất ${f(25)}, đúng cả khi ${m('F')} thay đổi (miễn ${m('F')} ${f(25)} ${nw(m('v') + ').')}</div>
<div>Xe đạp điện ${nw(u('250\\ W') + ':')} ${u('18\\ km/h=')} ${nw(`${f(12)}&nbsp;m/s`)} ${m('\\Rightarrow')} lực kéo tối đa ${m('F=P/v=')} ${nw(`${f(12)}&nbsp;N`)}; tốc độ gấp đôi thì còn ${nw(`${f(12)}&nbsp;N`)}</div>
<div>Lên dốc: trọng lực có thêm thành phần kéo xe xuống dốc ${m('\\Rightarrow')} cần ${m('F')} ${f(25)}; ${m('P_{\\max}')} gần như cố định ${m('\\Rightarrow')} ${m('v=P/F')} ${f(25)}</div>
</div>
${h3(3, 'Thí nghiệm: đạp xe lên dốc cầu', '2·3')}
<div class="card fig-side" style="${fs(48)};padding:1.2mm 3mm"><div>
<div><b>Làm:</b> lên dốc giữ nguyên số, rồi giảm số (số nhẹ) và lên lại.</div>
<div><b>Quan sát:</b> giữ số cũ thì chân ấn hết sức mà xe chậm dần; số nhẹ thì lên hết dốc dù chậm.</div>
<div><b>Rút ra:</b> công suất người đạp có ${f(25)} nên ${m('P=Fv')} gần như ${f(25)}; số nhẹ cho ${m('F')} ${f(25)}, đổi lại ${m('v')} ${f(25)}.</div>
<div style="margin-top:.6mm">Xe máy ${nw(u('6\\ kW') + ':')} lực kéo lớn nhất ${m('F=P/v')}</div>
<table class="tbl-ct" style="text-align:center"><tr><th>${m('v')} (m/s)</th><th>20</th><th>10</th><th>5</th><th>2</th></tr>
<tr><td>${m('F')} (N)</td><td></td><td></td><td></td><td></td></tr></table>
<div style="margin-top:.6mm">${m('v')} giảm 10 lần (20 ${m('\\to')} 2 m/s) thì ${m('F')} ${f(25)}</div></div>
${H.duongFv()}</div>
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('BẪY · TRẢ BÀI · KẾT QUẢ TỰ KIỂM TRA')}
${h3(1, 'III · Ba cái bẫy hay sập', '3·1')}
<div class="card fig-side" style="${fs(44)};padding:1mm 3mm"><div>
<div class="trap">${ck}<span><b>“Công suất lớn là công lớn.”</b> ${m('A=P\\,t')} còn phụ thuộc thời gian: máy ${u('5\\ kW')} chạy ${u('10\\ s')} sinh công ${f(25)} máy ${u('1\\ kW')} chạy ${nw(u('100\\ s') + '.')}</span></div>
<div class="trap">${ck}<span><b>“kWh là đơn vị công suất.”</b> kWh trên hoá đơn điện là ${f(25)}. Đèn ${u('40\\ W')} bật ${nw(u('5\\ h') + ':')} ${nw(`${f(14)}&nbsp;kWh`)}</span></div>
<div class="trap">${ck}<span><b>“Xe lên dốc chậm vì động cơ yếu đi.”</b> ${m('P_{\\max}')} vẫn như cũ; lên dốc cần ${m('F')} lớn hơn nên ${m('v=P/F')} ${f(25)}.</span></div></div>
${H.cotPt()}</div>
${h3(2, 'IV · Trả bài 6 câu', '3·2')}
${box(`${tb('1. Công suất là gì? Viết công thức.')}${lines(2)}
${tb('2. 1 W bằng gì? Nêu kW, MW, mã lực.')}${lines(2)}
${tb('3. kWh là đơn vị của đại lượng nào? Bằng bao nhiêu jun?')}${lines(2)}
${tb('4. Công suất liên hệ thế nào với lực và vận tốc? Điều kiện?')}${lines(2)}
${tb('5. Công suất tức thời khác công suất trung bình ở đâu?')}${lines(2)}
${tb('6. Vì sao xe lên dốc phải giảm số?')}${lines(2)}`)}
<div class="card soft" style="margin-top:1.5mm;padding:1mm 3mm"><b>Bạn cùng bàn kiểm:</b> nói được ……/6 câu · câu chưa thuộc: ${f(30)} ${nw(`${m('\\to')} đọc lại ô Tập ${f(14)}`)}</div>
${h3(3, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '3·3')}
${rkHai([1, 2, 3, 4], [5, 6, 7])}
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('BÀI TOÁN MẪU · THANG MÁY 800 kg LÊN 15 m')}
${h3(1, 'V · Đề bài', '4')}
<div class="card soft" style="padding:1.2mm 3mm">Cabin cùng người và đồ nặng ${nw(u('800\\ kg') + ',')} nâng đều lên cao ${u('15\\ m')} trong ${nw(u('30\\ s') + '.')} Bỏ qua ma sát và đối trọng, ${g10}.
<div><b>a)</b> Công của lực kéo?</div><div><b>b)</b> Công suất trung bình (W và mã lực Pháp, ${nw(u('1\\ CV=736\\ W') + ')')}?</div><div><b>c)</b> Kiểm lại bằng ${nw(m('P=Fv') + '.')}</div></div>
${h3(2, 'Phân tích đề')}
<table><tr><th style="width:44mm">Câu trong đề</th><th style="width:36mm">Dữ liệu</th><th>Kiến thức liên quan</th></tr>
<tr><td>“nặng 800 kg”</td><td>${m('m=800\\ \\mathrm{kg}')}</td><td>trọng lượng ${m('mg=8\\,000\\ \\mathrm N')}</td></tr>
<tr><td style="height:6.5mm">“nâng đều”</td><td></td><td></td></tr>
<tr><td style="height:6.5mm">“cao 15 m”</td><td></td><td></td></tr>
<tr><td style="height:6.5mm">“trong 30 s”</td><td></td><td></td></tr>
<tr><td style="height:6.5mm">“bỏ qua ma sát, đối trọng”</td><td></td><td></td></tr></table>
${h3(3, 'Giải')}
<div class="fig-side" style="${fs(42)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl('Lực kéo:', 2)}${wl('a)', 3)}${wl('b)', 4)}${wl('c)', 4)}</div>${H.cabin()}</div>
${h3(4, 'Mở rộng: cùng thang, chạy chậm hơn, hết 40 s')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl(`Bước 1: ${m('A=')} ${f(25)} J`, 2)}${wl(`Bước 2: ${m('P=A/t=')} ${f(25)} W`, 1)}${wl(`Kiểm tra: ${m('v=d/t=')} ${f(18)} m/s; ${m('F\\cdot v=')} ${f(18)} W`, 2)}</div>
<div class="card soft" style="margin-top:1.5mm;padding:1mm 3mm"><b>Em tự kiểm:</b> ${ck}gạch “nâng đều” ${m('\\Rightarrow')} ${m('F=mg')} &nbsp;${ck}đổi kW ra W &nbsp;${ck}có ghi đơn vị</div>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TẬP VỀ NHÀ · MANG VỀ · THỬ THÁCH')}
${K.btvn()}
${h3(2, 'VI · Mang về: điều em dễ quên nhất', '5')}
${box(wl('1.', 3) + wl('2.', 3) + wl('3.', 2))}
${h3(3, 'Thử thách phân tầng')}
<div class="fig-side" style="grid-template-columns:1fr 42mm">${box(dd(`${sao(1)} Lực ${u('200\\ N')} kéo vật đều ${u('5\\ m')} trong ${nw(u('10\\ s') + '.')} Công suất?`, 2)
 + dd(`${sao(2)} Ô tô ${u('60\\ kW')} chạy đều ${u('15\\ m/s')} trên đường bằng. Lực cản? Cùng ${nw(m('P') + ',')} chạy ${u('30\\ m/s')} thì lực kéo lớn nhất?`, 3)
 + dd(`${sao(3)} Ô tô ${u('60\\ kW')} chạy đều ${u('20\\ m/s')} trên đường bằng. Lên dốc, lực cản tổng cộng gấp 3, công suất giữ nguyên. Vận tốc lên dốc?`, 3))}${H.xeDoc('Lên dốc: lực kéo, lực cản, trọng lực.', 'dài', 'cao')}</div>
${h3(4, 'Câu 7 (đổi số)')}
${box(dd(`Thang máy ở bài toán mẫu (${u('800\\ kg')} lên ${nw(u('15\\ m') + '),')} động cơ tối đa ${nw(u('5\\ kW') + ',')} nâng đều: thời gian ngắn nhất ${nw(`${f(14)} s`)}; khi đó ${m('v=')} ${nw(`${f(14)} m/s`)}`, 2))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Công suất, công và đổi đơn vị (kWh, mã lực)',
    de: `Máy bơm nước ${u('2{,}0\\ kW')} chạy liên tục ${u('3{,}0')} giờ; ${nw(u('1\\ CV=736\\ W') + '.')}<br><b>a)</b> công máy bơm sinh ra, theo kWh&emsp;&emsp;<b>b)</b> công đó theo J&emsp;&emsp;<b>c)</b> công suất theo CV<br><b>d)</b> máy bơm ${u('0{,}50\\ kW')} phải chạy bao lâu để sinh cùng công đó`,
    nd: `${m('A=')} ${f(12)} · ${f(12)} (kW nhân h ra kWh); ${u('1\\ kWh=')} ${nw(`${f(18)}&nbsp;J`)}`, a: ['a', 'b', 'c', 'd'], gi: 4 },
  { t: 'Dạng 2 · Dễ · Công suất trung bình khi kéo và khi nâng',
    de: `Kéo đều thùng trên sàn ngang bằng lực ${u('120\\ N')} cùng hướng đi, đi ${u('15\\ m')} trong ${nw(u('20\\ s') + '.')} Nâng đều thùng ${u('24\\ kg')} lên cao ${u('1{,}5\\ m')} trong ${nw(u('3{,}0\\ s') + ',')} ${g10}.<br><b>a)</b> công của lực kéo<br><b>b)</b> công suất trung bình khi kéo<br><b>c)</b> công suất trung bình của lực nâng`,
    nd: `${m('A=Fd')} rồi ${nw(m('P=A/t') + ';')} nâng đều thì lực nâng ${m('F=')} ${f(14)}`, a: ['a', 'b', 'c'], gi: 3, fig: () => H.keoNang('') },
  { t: 'Dạng 3 · Trung bình · Công suất tức thời P = F·v, đổi km/h ra m/s',
    de: `Xe máy điện trên đường ngang, lực kéo luôn cùng hướng chuyển động.<br><b>a)</b> chạy đều ${nw(u('36\\ km/h') + ',')} lực kéo ${nw(u('150\\ N') + ':')} công suất tức thời<br><b>b)</b> giữ chạy đều như vậy ${u('5{,}0')} phút: công động cơ sinh ra<br><b>c)</b> tăng tốc, lúc ${u('54\\ km/h')} lực kéo ${nw(u('120\\ N') + ':')} công suất tức thời lúc đó`,
    nd: `${m('v')} (m/s) ${m('=')} km/h : ${f(12)}; ${m('P=')} ${f(12)} · ${f(12)}, lấy ở cùng một lúc`, a: ['a', 'b', 'c'], gi: 3 },
  { t: 'Dạng 4 · Khó · Động cơ nâng vật: lực nâng, vận tốc lớn nhất, thời gian ngắn nhất',
    de: `Cần cẩu tháp, động cơ ${nw(u('22{,}5\\ kW') + ',')} nâng đều kiện vật liệu ${u('750\\ kg')} lên cao ${nw(u('30\\ m') + '.')} Coi toàn bộ công suất dùng để nâng, ${g10}.<br><b>a)</b> lực nâng của cáp<br><b>b)</b> vận tốc nâng đều lớn nhất<br><b>c)</b> thời gian ngắn nhất để nâng lên ${u('30\\ m')}`,
    nd: `${m('F=mg')} ${m('\\to')} ${m('v_{\\max}=')} ${f(12)} / ${f(12)} (${m('P')} đổi ra W) ${m('\\to')} ${m('t_{\\min}=')} ${f(12)} / ${f(12)}`, a: ['a', 'b', 'c'], gi: 7, fig: () => H.canCau('') },
  { t: 'Dạng 5 · Khó · Xe lên dốc với công suất tối đa',
    de: `Ô tô tải ${u('4{,}5')} tấn, công suất tối đa ${nw(u('36\\ kW') + ',')} tổng lực cản ${u('1\\,800\\ N')} không đổi cả trên đường ngang lẫn khi lên dốc, ${g10}. Dốc ${nw(m('6\\,\\%') + ':')} đi ${u('100\\ m')} theo mặt dốc thì lên cao ${nw(u('6\\ m') + '.')}<br><b>a)</b> chạy đều trên đường ngang với công suất tối đa: vận tốc<br><b>b)</b> lực kéo khi lên dốc đều<br><b>c)</b> lên dốc đều với công suất tối đa: vận tốc<br><b>d)</b> dốc dài ${nw(u('500\\ m') + ':')} thời gian đi hết dốc`,
    nd: `Lên dốc đều: ${m('F_k=F_c+')} ${f(20)}, với ${m('\\sin\\alpha=')} ${f(12)}; rồi ${m('v=P/F_k')}`, a: ['a', 'b', 'c', 'd'], gi: 9, fig: () => H.xeDoc() },
];

// Bài tương tự: mỗi dạng 2 bài, đề ghi đủ hằng số; đáp số tính bằng Python (xem báo cáo phiên 10/11/2026).
const tuongTu = {
  tieuDe: ['DẠNG 1–3', 'DẠNG 4–5'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Máy bơm ${u('1{,}2\\ kW')} chạy liên tục ${u('2{,}5')} giờ; ${nw(u('1\\ kWh=3{,}6\\cdot10^{6}\\ J') + ',')} ${nw(u('1\\ CV=736\\ W') + '.')}<div class="ln"><b>a)</b> công theo kWh</div><div class="ln"><b>b)</b> công theo J</div><div class="ln"><b>c)</b> công suất theo CV</div>`, k: 1 },
    { t: 'Dạng 1 · Bài 2', de: `Động cơ ${u('10\\ CV')} (${nw(u('1\\ CV=736\\ W') + ')')} chạy ${u('30')} phút.<div class="ln"><b>a)</b> công suất theo kW</div><div class="ln"><b>b)</b> công theo kWh</div><div class="ln"><b>c)</b> công theo J (${nw(u('1\\ kWh=3{,}6\\cdot10^{6}\\ J') + ')')}</div><div class="ln"><b>d)</b> máy ${u('2{,}0\\ kW')} chạy bao lâu để sinh cùng công</div>`, k: 1 },
    { t: 'Dạng 2 · Bài 1', de: `Kéo đều thùng trên sàn ngang bằng lực ${u('80\\ N')} cùng hướng chuyển động, đi ${u('12\\ m')} trong ${nw(u('16\\ s') + '.')}<div class="ln"><b>a)</b> công của lực kéo</div><div class="ln"><b>b)</b> công suất trung bình</div>`, k: 0 },
    { t: 'Dạng 2 · Bài 2', de: `Nâng đều bao xi măng ${u('50\\ kg')} lên cao ${u('2{,}4\\ m')} trong ${nw(u('4{,}0\\ s') + ',')} ${g10}.<div class="ln"><b>a)</b> lực nâng</div><div class="ln"><b>b)</b> công của lực nâng</div><div class="ln"><b>c)</b> công suất trung bình</div>`, k: 1 },
    { t: 'Dạng 3 · Bài 1', de: `Ô tô chạy đều ${nw(u('54\\ km/h') + ',')} lực kéo ${u('2\\,000\\ N')} cùng hướng chuyển động.<div class="ln"><b>a)</b> công suất tức thời (kW)</div><div class="ln"><b>b)</b> công động cơ sinh ra trong ${u('10')} phút</div>`, k: 1 },
    { t: 'Dạng 3 · Bài 2', de: `Xe máy chạy đều ${u('72\\ km/h')} với công suất ${nw(u('4{,}0\\ kW') + ',')} lực kéo cùng hướng chuyển động.<div class="ln"><b>a)</b> lực kéo</div><div class="ln"><b>b)</b> tăng tốc, lúc ${u('90\\ km/h')} lực kéo ${nw(u('150\\ N') + ':')} công suất tức thời</div>`, k: 1 },
  ], [
    { t: 'Dạng 4 · Bài 1', de: `Động cơ ${u('12\\ kW')} nâng đều kiện hàng ${u('600\\ kg')} lên cao ${nw(u('24\\ m') + ';')} toàn bộ công suất dùng để nâng, ${g10}.<div class="ln"><b>a)</b> lực nâng</div><div class="ln"><b>b)</b> vận tốc nâng lớn nhất</div><div class="ln"><b>c)</b> thời gian ngắn nhất</div>`, k: 2 },
    { t: 'Dạng 4 · Bài 2', de: `Thang máy (cabin và người) ${u('1\\,200\\ kg')} cần nâng đều lên cao ${u('36\\ m')} trong ${nw(u('24\\ s') + ';')} bỏ qua mất mát, ${g10}.<div class="ln"><b>a)</b> vận tốc nâng</div><div class="ln"><b>b)</b> lực kéo của cáp</div><div class="ln"><b>c)</b> công suất tối thiểu của động cơ (kW)</div>`, k: 2 },
    { t: 'Dạng 5 · Bài 1', de: `Ô tô ${u('2{,}0')} tấn, công suất tối đa ${nw(u('30\\ kW') + ',')} lực cản ${u('1\\,500\\ N')} không đổi, ${g10}. Dốc ${nw(m('5\\,\\%') + ':')} đi ${u('100\\ m')} theo mặt dốc thì lên cao ${nw(u('5\\ m') + ',')} tức ${nw(m('\\sin\\alpha=0{,}05') + '.')}<div class="ln"><b>a)</b> vận tốc khi chạy đều trên đường ngang với công suất tối đa</div><div class="ln"><b>b)</b> lực kéo khi lên dốc đều</div><div class="ln"><b>c)</b> vận tốc lên dốc với công suất tối đa</div><div class="ln"><b>d)</b> thời gian đi hết dốc dài ${u('600\\ m')}</div>`, k: 2 },
    { t: 'Dạng 5 · Bài 2', de: `Xe tải ${u('6{,}0')} tấn, công suất tối đa ${nw(u('48\\ kW') + ',')} lực cản ${u('2\\,400\\ N')} không đổi, ${g10}. Dốc ${nw(m('4\\,\\%') + ':')} đi ${u('100\\ m')} theo mặt dốc thì lên cao ${nw(u('4\\ m') + ',')} tức ${nw(m('\\sin\\alpha=0{,}04') + '.')}<div class="ln"><b>a)</b> vận tốc trên đường ngang với công suất tối đa</div><div class="ln"><b>b)</b> lực kéo khi lên dốc đều</div><div class="ln"><b>c)</b> vận tốc lên dốc với công suất tối đa</div><div class="ln"><b>d)</b> lực kéo lên dốc gấp mấy lần trên đường ngang</div>`, k: 2 },
  ]],
  dap: [
    `D1·1: a) 3,0 kWh · b) ${m('1{,}08\\cdot10^{7}')} J · c) ${m('\\approx')} 1,63 CV &nbsp;|&nbsp; D1·2: a) 7,36 kW · b) 3,68 kWh · c) ${m('1{,}32\\cdot10^{7}')} J · d) 1,84 h &nbsp;|&nbsp; D2·1: a) 960 J · b) 60 W &nbsp;|&nbsp; D2·2: a) 500 N · b) 1 200 J · c) 300 W &nbsp;|&nbsp; D3·1: a) 30 kW · b) ${m('1{,}8\\cdot10^{7}')} J &nbsp;|&nbsp; D3·2: a) 200 N · b) 3,75 kW`,
    `D4·1: a) 6 000 N · b) 2,0 m/s · c) 12 s &nbsp;|&nbsp; D4·2: a) 1,5 m/s · b) 12 000 N · c) 18 kW &nbsp;|&nbsp; D5·1: a) 20 m/s · b) 2 500 N · c) 12 m/s · d) 50 s &nbsp;|&nbsp; D5·2: a) 20 m/s · b) 4 800 N · c) 10 m/s · d) 2 lần`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 2], kq: [[1, 2, 3], [4, 5]], khoNhat: false },
  tuongTu,
  tra: `công suất 1·4 · đơn vị 1·5 · leo cầu thang 2·1 · P = Fv 2·2 · dốc cầu 2·3 · bẫy 3·1 · dạng 1–3 ${m('\\to')} 6·1 · dạng 4–5 ${m('\\to')} 7·1`,
  out: process.argv[2],
});
