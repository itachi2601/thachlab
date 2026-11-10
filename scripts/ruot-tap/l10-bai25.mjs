// Ruột tập Vật lí 10 – Bài 25 · Động năng, thế năng (lesson id 70), tr. 25–36 của quyển Chương 4 (bài 23 = tr. 1–12).
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR); hình: hinh-l10-bai25.mjs.
// Nguồn nội dung: bài trên web (book/cache/70.json, tải từ DB 10/11/2026): khung ghi bài, bẫy, trả bài, bài toán mẫu, 5 dạng bài tập mẫu.
// Không dùng ảnh Halliday: toàn bộ 11 hình là SVG tự vẽ. Đáp số bài tương tự tính lại bằng Python (g = 10 m/s²), xem `dap` cuối file.
// Kiểm hình ở cỡ in: xem-hinh.mjs chỉ nạp hinh.mjs + hinh-ch4.mjs, nên chụp bằng bản sao tạm đổi import sang hinh-l10-bai25.mjs (export hinhB25).
// Chạy: node scripts/ruot-tap/l10-bai25.mjs [file.pdf] → scripts/ruot-tap/out/ruot-tap-vl10-bai25.pdf
import { khoiTao, m as m0, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinhB25 as H } from './hinh-l10-bai25.mjs';
const m = (s) => nw(m0(s)); // số + đơn vị, "g = 10 m/s²" không gãy dòng
const ft = (w) => `<span class="fill" style="min-width:${w}mm;height:9mm"></span>`; // ô viết phân số
const K = khoiTao({ bai: 25, lid: 70, ten: 'ĐỘNG NĂNG · THẾ NĂNG', lop: 10, baiDau: 23, sub: 'Vật lí 10 · Chương 4: Năng lượng, công, công suất' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const Wd = m('W_\\mathrm{d}'), Wt = m('W_\\mathrm{t}');
const u = (s) => m(s); // số + đơn vị viết trong KaTeX để không tách dòng

// Trang 8 có 6 bài: Dạng 1–2 xếp hai cột (bài 1 | bài 2 cùng dạng), Dạng 3 một cột (có hình) để vừa một trang; khung chưa có tuỳ chọn này nên đặt CSS riêng ở đây.
const css2cot = `<style>section.page:nth-of-type(8)>.tt:nth-child(-n+5){float:left;width:calc(50% - 1.2mm)}section.page:nth-of-type(8)>.tt:nth-child(even):nth-child(-n+5){clear:left;margin-right:2.4mm}section.page:nth-of-type(8)>.tt:nth-child(n+6){clear:both}</style>`;
const p1 = `${css2cot}<section class="page">
${head('BÀI 25 · ĐỘNG NĂNG · THẾ NĂNG', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
<div style="margin:.3mm 0">${ck}Tính <b>động năng</b> ${m('W_\\mathrm{d}=\\tfrac12mv^2')} và dùng <b>định lí động năng</b></div>
<div style="margin:.3mm 0">${ck}Tính <b>thế năng trọng trường</b> ${m('W_\\mathrm{t}=mgz')} theo mốc đã chọn</div>
<div style="margin:.3mm 0">${ck}Tính <b>công của trọng lực</b> từ hiệu thế năng, không cần biết đường đi</div>
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Minh đạp xe ${u('10\\ \\mathrm{km/h}')}, bóp chặt phanh: bánh xe lết ${u('2\\ \\mathrm m')} mới dừng. Hôm sau, cùng đường, xe chạy ${u('20\\ \\mathrm{km/h}')}, bóp phanh y như cũ. Lần này bánh xe lết khoảng:</p>
<div class="fig-side" style="${fs(38)}"><div>
<div style="display:grid;grid-template-columns:1fr 1fr">${opt('A', u('2\\ \\mathrm m'))}${opt('B', u('4\\ \\mathrm m'))}${opt('C', u('8\\ \\mathrm m'))}${opt('D', u('16\\ \\mathrm m'))}</div>
<div style="margin-top:1mm">${chon(12)}</div><div class="hint">Vì sao?</div>${lines(1)}</div>
${H.xeDap('Mũi tên vận tốc theo tỉ lệ; vạch lết hôm sau vẽ ngắt, không theo tỉ lệ.')}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Động năng', '1·4')}
<div class="card" style="padding:1.2mm 3mm">
<div>Là năng lượng vật có do ${f(26)}. &nbsp;${m('W_\\mathrm{d}=')} ${ft(18)} &nbsp;(đơn vị ${f(12)})</div>
<div>Với một vật: phụ thuộc ${f(25)} của vận tốc, không phụ thuộc ${f(25)} của vận tốc.</div>
<div>Đại lượng ${f(25)}, không âm: ${Wd} ${f(12)} 0.</div>
<div>Tính tương đối: vali nằm yên trên tàu có ${Wd} đối với toa = ${f(12)}, đối với đất ${f(12)} 0.</div>
<div>Lan ${u('50\\ \\mathrm{kg}')} lướt ${u('6\\ \\mathrm{m/s}')}: ${m('W_\\mathrm{d}=')} ${nw(`${f(16)}&nbsp;J`)}, dù lướt sang trái hay sang phải.</div></div>
${h3(5, 'II.2 · Định lí động năng', '1·5')}
<div class="card" style="padding:1.2mm 3mm">
<div>${m('\\tfrac12mv^2-\\tfrac12mv_0^2=')} ${f(28)} &nbsp;(tổng công mọi ${f(25)} lực)</div>
<div>Tổng công dương: ${Wd} ${f(25)}; tổng công âm: ${Wd} ${f(25)}.</div>
<div>Phanh với lực hãm ${m('F_\\mathrm{h}')}: ${m('0-\\tfrac12mv_0^2=')} ${f(16)} ${m('\\Rightarrow s=')} ${ft(20)}; ${nw(`${m('s')} tỉ lệ với ${f(12)}.`)}</div></div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('THÍ NGHIỆM · THẾ NĂNG · CÔNG CỦA TRỌNG LỰC')}
${h3(1, 'Thí nghiệm: khúc gỗ trượt sau cổng quang', '2·1')}
<div class="card fig-side" style="${fs(48)};padding:1.2mm 3mm"><div>
<table class="tbl-ct" style="font-size:var(--fs-sm)"><tr><th>${m('v\\ (\\mathrm{m/s})')}</th><th>1,00</th><th>1,50</th><th>2,00</th><th>2,50</th></tr>
<tr><td>${m('s\\ (\\mathrm m)')}</td><td>0,21</td><td>0,44</td><td>0,82</td><td>1,22</td></tr>
<tr><td>${m('s/v^2')}</td><td></td><td></td><td></td><td></td></tr></table>
<div style="margin-top:.6mm">${m('v')} từ 1,00 lên 2,00: ${m('s')} gấp ${f(12)} lần.</div>
<div>Hàng cuối gần như ${f(25)} ${nw(`⇒ ${m('s')} tỉ lệ với ${f(12)}.`)}</div>
<div>Ma sát sinh công ${f(25)}, đúng bằng phần ${f(25)} mất đi.</div>
<div>Lần ${m('s/v^2')} lệch nhất so với trung bình 0,20: ${nw(`${m('v=')} ${f(12)}`)}, vì ${f(34)}.</div></div>
${H.congQuang('Cổng quang đo v; thước đo quãng trượt s.')}</div>
${h3(2, 'II.3 · Thế năng trọng trường', '2·2')}
<div class="card fig-side" style="${fs(38)};padding:1.2mm 3mm"><div>
<div>Năng lượng ${f(25)} giữa Trái Đất và vật; phụ thuộc ${f(25)} của vật.</div>
<div>Mốc: vị trí chọn để ${f(25)}.</div>
<div>${m('W_\\mathrm{t}=')} ${f(14)}; ${m('z')}: toạ độ trên trục thẳng đứng hướng ${f(25)}, gốc ở mốc.</div>
<div>Mốc ở mặt đất: ${m('W_\\mathrm{t}=')} ${f(14)}, ${m('h')} là ${f(26)}.</div>
<div style="margin-top:.6mm">Sách ${u('0{,}5\\ \\mathrm{kg}')} trên giá cao ${u('2{,}0\\ \\mathrm m')}; bàn cao ${u('0{,}8\\ \\mathrm m')}; trần ${u('3{,}0\\ \\mathrm m')}; ${m('g=10\\ \\mathrm{m/s^2}')}.</div>
<table style="font-size:var(--fs-sm);margin-top:.5mm"><tr><th>Mốc</th><th>sàn</th><th>mặt bàn</th><th>trần</th></tr>
<tr><td>${m('z\\ (\\mathrm m)')}</td><td></td><td></td><td></td></tr><tr><td>${m('W_\\mathrm{t}\\ (\\mathrm J)')}</td><td></td><td></td><td></td></tr></table></div>
${H.trucZ('Điền dấu của W<sub>t</sub> ở ba vị trí.')}</div>
${h3(3, 'II.4 · Công của trọng lực · lực thế', '2·3')}
<div class="card fig-side" style="${fs(44)};padding:1.2mm 3mm"><div>
<div>Rơi từ độ cao ${m('h')}: ${m('A=')} ${f(14)}. Trượt dốc dài ${m('s')}, góc ${m('\\alpha')}: ${m('A=mgs\\sin\\alpha=')} ${f(12)}.</div>
<div>Lực thế: công chỉ phụ thuộc ${f(30)}.</div>
<div>${m('A_{MN}=')} ${f(12)} ${m('-')} ${f(12)}; không phụ thuộc đường đi.</div>
<div>Đi xuống: ${m('A_P')} ${f(12)} 0, thế năng ${f(25)}.</div>
<div>Đi lên: ${m('A_P')} ${f(12)} 0, thế năng ${f(25)}.</div>
<div>Lực thế: trọng lực, lực ${f(25)}, lực tĩnh điện.</div>
<div>Ma sát ${f(25)} lực thế, vì ${f(34)}.</div></div>
${H.haiDuong('Hai đường từ A lên B, cùng độ cao h: công của trọng lực có khác nhau?')}</div>
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('THÍ NGHIỆM · BẪY · TRẢ BÀI · TỰ KIỂM TRA')}
${h3(1, 'Thí nghiệm: con lắc vướng đinh', '3·1')}
<div class="card fig-side" style="${fs(42)};padding:1.2mm 3mm"><div>
<div><b>Quan sát:</b> có đinh, quả nặng bên kia lên tới ${f(30)}.</div>
<div><b>Rút ra:</b> lực căng dây luôn ${f(25)} đường đi nên công ${f(12)}.</div>
<div>Hai điểm cao nhất đều có ${m('v=')} ${f(12)}: công trọng lực lúc xuống và lúc lên ${f(25)}; công ấy chỉ phụ thuộc ${f(25)}.</div></div>
${H.conLac('Dây vướng đinh: bên kia quả nặng lên tới đâu?')}</div>
${h3(2, 'III · Ba cái bẫy hay sập', '3·2')}
<div class="card" style="padding:1mm 3mm">
<div class="trap">${ck}<span><b>“Tốc độ gấp đôi thì động năng gấp đôi.”</b> ${Wd} theo ${m('v^2')}: lập tỉ số tốc độ rồi bình phương.</span></div>
<div class="trap">${ck}<span><b>“Thế năng là con số cố định của vật.”</b> ${Wt} đổi theo mốc, ghi rõ mốc; hiệu thế năng thì không đổi.</span></div>
<div class="trap">${ck}<span><b>“Định lí động năng chỉ tính công lực kéo.”</b> Cộng công mọi ngoại lực, kể cả công âm của ma sát.</span></div></div>
${h3(3, 'IV · Trả bài 6 câu', '3·3')}
${box(`${tb('1. Động năng là gì? Công thức, đơn vị?')}${lines(2)}
${tb('2. Ba tính chất của động năng?')}${lines(2)}
${tb('3. Phát biểu định lí động năng.')}${lines(2)}
${tb('4. Thế năng trọng trường: công thức; khi nào âm?')}${lines(2)}
${tb('5. Công của trọng lực từ M đến N tính thế nào?')}${lines(2)}
${tb('6. Ma sát có phải lực thế không, vì sao?')}${lines(2)}`)}
<div class="card soft" style="margin-top:1.5mm;padding:1mm 3mm"><b>Bạn cùng bàn kiểm:</b> nói được ……/6 câu · câu chưa thuộc: ${f(20)} ${nw(`→ đọc lại ô Tập ${f(14)}`)}</div>
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('BÀI TOÁN MẪU · TOA TÀU LƯỢN TỪ A XUỐNG B')}
${h3(1, 'V · Đề bài', '4')}
<div class="card soft" style="padding:1.2mm 3mm">Toa tàu lượn cùng hành khách nặng ${u('400\\ \\mathrm{kg}')} qua điểm ${m('A')} cao ${u('18\\ \\mathrm m')} so với mặt đất với tốc độ ${u('10\\ \\mathrm{m/s}')}, rồi lao xuống điểm ${m('B')} cao ${u('3\\ \\mathrm m')}. Bỏ qua ma sát và lực cản, ${m('g=10\\ \\mathrm{m/s^2}')}.
<div><b>a)</b> Chọn mốc thế năng ở mặt đất, tính thế năng của toa tại ${m('A')} và ${m('B')}.</div><div><b>b)</b> Tính công của trọng lực từ ${m('A')} đến ${m('B')}.</div><div><b>c)</b> Tính tốc độ của toa tại ${m('B')}.</div></div>
${h3(2, 'Phân tích đề')}
<table><tr><th style="width:46mm">Câu trong đề</th><th style="width:36mm">Dữ liệu</th><th>Kiến thức liên quan</th></tr>
<tr><td>“nặng 400 kg”</td><td>${m('m=400\\ \\mathrm{kg}')}</td><td>cả toa và người</td></tr>
<tr><td style="height:6.5mm">“${m('A')} cao 18 m … 10 m/s”</td><td></td><td></td></tr>
<tr><td style="height:6.5mm">“${m('B')} cao 3 m”</td><td></td><td></td></tr>
<tr><td style="height:6.5mm">“bỏ qua ma sát và lực cản”</td><td></td><td></td></tr>
<tr><td style="height:6.5mm">“mốc ở mặt đất”</td><td></td><td></td></tr></table>
${h3(3, 'Giải')}
<div class="fig-side" style="${fs(52)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl('a)', 3)}${wl('b)', 2)}${wl('c)', 4)}</div>${H.tauLuon()}</div>
${h3(4, 'Điền bước còn thiếu: có lực cản')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div class="ln" style="height:auto;padding-top:1mm"><b>Đề:</b> cùng đề, nhưng lực cản không khí và ma sát sinh công tổng cộng ${u('-30\\,000\\ \\mathrm J')} ${nw(`từ ${m('A')} đến ${m('B')}.`)}</div>
${wl('Bước 1: tổng công các ngoại lực = …', 2)}${wl('Bước 2: W<sub>dB</sub> = …', 2)}
<div class="ln" style="height:auto;padding-top:1mm"><b>Bước 3 (cho sẵn):</b> ${m('v_B=\\sqrt{2W_{\\mathrm dB}/m}=')} ${nw(`${f(14)}&nbsp;m/s`)}</div></div>
<div class="card soft" style="margin-top:1.5mm;padding:1mm 3mm"><b>Em tự kiểm:</b> ${ck}nói rõ mốc &nbsp;${ck}thế năng đầu trừ cuối &nbsp;${ck}cộng công mọi lực</div>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TẬP VỀ NHÀ · MANG VỀ · THỬ THÁCH')}
${K.btvn()}
${h3(2, 'VI · Mang về: điều em dễ quên nhất', '5·1')}
${box(wl('1.', 2) + wl('2.', 2) + wl('3.', 2))}
${h3(3, 'Thử thách phân tầng')}
<div class="fig-side" style="grid-template-columns:1fr 44mm">${box(wl(`★ Viên đạn ${u('10\\ \\mathrm g')} bay ${u('400\\ \\mathrm{m/s}')}. Động năng?`, 2)
 + wl('★★ Quả bóng chạm sàn và bẹp lại: động năng chuyển thành dạng nào? Vì sao bóng không nảy lại tới độ cao cũ?', 3)
 + wl(`★★★ Ném hòn đá ${u('2\\ \\mathrm{kg}')} từ mép vực với ${u('10\\ \\mathrm{m/s}')}, hướng tuỳ ý; lòng suối thấp hơn mép vực ${u('20\\ \\mathrm m')}; mốc ở mép vực, bỏ qua cản. Thế năng ở lòng suối? Tốc độ chạm nước có phụ thuộc hướng ném?`, 5))}${H.vuc()}</div>
${h3(4, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '5·2')}
${rkHai([1, 2, 3, 4], [5, 6, 7])}
${h3(5, 'Đổi chiều (đổi số)')}
${box(wl(`Toa rời ${m('B')} (cao ${u('3\\ \\mathrm m')}) với ${u('16\\ \\mathrm{m/s}')}, bỏ qua ma sát, leo dốc tới khi dừng. Toa lên tới độ cao … m so với mặt đất`, 4))}
${foot(5)}</section>`;

const dang = [
  { t: 'Dạng 1 · Dễ · Tính và so sánh động năng',
    de: `Xe tải ${u('4{,}0')} tấn chạy ${u('36\\ \\mathrm{km/h}')}. <b>a)</b> động năng xe tải (kJ)<br><b>b)</b> ô tô con ${u('1{,}0')} tấn có cùng động năng: tốc độ (m/s)<br><b>c)</b> xe tải tăng tốc lên ${u('90\\ \\mathrm{km/h}')}: động năng gấp mấy lần lúc đầu`,
    nd: `km/h → m/s: ${f(12)}; cùng vật: tỉ số ${Wd} = ${nw(`(tỉ số ${f(12)})²`)}`, a: ['a', 'b', 'c'], gi: 3 },
  { t: 'Dạng 2 · Dễ · Thế năng khi mốc ở mặt đất',
    de: `Mốc ở nền kho, ${m('g=10\\ \\mathrm{m/s^2}')}. Thùng A ${u('12\\ \\mathrm{kg}')} ở độ cao ${u('1{,}5\\ \\mathrm m')}; thùng B ${u('5{,}0\\ \\mathrm{kg}')} ở ${u('3{,}6\\ \\mathrm m')}.<br><b>a)</b> thế năng của mỗi thùng &nbsp; <b>b)</b> so sánh hai thế năng<br><b>c)</b> thùng C ${u('8{,}0\\ \\mathrm{kg}')} có thế năng ${u('240\\ \\mathrm J')}: độ cao của C`,
    nd: `Mốc ở nền → ${m('z')} = ${f(25)}; ${m('W_\\mathrm{t}=')} ${f(12)}; tìm độ cao: chia ${Wt} cho ${f(12)}`, a: ['a', 'b', 'c'], gi: 3 },
  { t: 'Dạng 3 · Trung bình · Đổi mốc, xét dấu thế năng',
    de: `<div class="fig-side" style="grid-template-columns:1fr 46mm"><div>Chậu cây ${u('2{,}0\\ \\mathrm{kg}')} trên sàn tầng 3; độ cao các sàn so với mặt đường ghi trên hình, ${m('g=10\\ \\mathrm{m/s^2}')}. Thế năng của chậu khi mốc tại:<br><b>a)</b> mặt đường<br><b>b)</b> sàn tầng hầm<br><b>c)</b> sàn tầng 6</div>${H.toaNha('')}</div>`,
    nd: `Đổi mốc → ${m('z')} = độ cao vật ${f(25)} độ cao mốc; ${nw(`dưới mốc: ${Wt} ${f(12)}`)}`, a: ['a', 'b', 'c'], gi: 3 },
  { t: 'Dạng 4 · Trung bình · Công của trọng lực từ hiệu thế năng',
    de: `Người đi xe đạp, tổng ${u('60\\ \\mathrm{kg}')}: từ đỉnh dốc A cao ${u('40\\ \\mathrm m')} xuống chân dốc B cao ${u('12\\ \\mathrm m')}, rồi lên đồi C cao ${u('25\\ \\mathrm m')} (cùng một mức chuẩn), ${m('g=10\\ \\mathrm{m/s^2}')}.<br><b>a)</b> công của trọng lực từ A đến B<br><b>b)</b> từ B đến C<br><b>c)</b> từ A đến C; có phụ thuộc đường đi quanh co không`,
    nd: `${m('A_{MN}=')} ${Wt} ${f(12)} − ${Wt} ${f(12)} = ${m('mg(')}${f(18)}${m(')')}; đi xuống công ${f(25)}, đi lên công ${f(25)}`, a: ['a', 'b', 'c'], gi: 5, fig: H.doi('') },
  { t: 'Dạng 5 · Khó · Định lí động năng với nhiều ngoại lực',
    de: `Kéo thùng ${u('20\\ \\mathrm{kg}')} từ nghỉ ở chân dốc lên đỉnh bằng dây song song mặt dốc; dốc dài ${u('10\\ \\mathrm m')}, nghiêng ${m('30^\\circ')}; lực kéo ${u('150\\ \\mathrm N')}, ma sát ${u('25\\ \\mathrm N')}, ${m('g=10\\ \\mathrm{m/s^2}')}.<br><b>a)</b> tốc độ của thùng ở đỉnh dốc<br><b>b)</b> lần khác, tốc độ đầu ở chân dốc ${u('2{,}0\\ \\mathrm{m/s}')}, ma sát vẫn ${u('25\\ \\mathrm N')}: lực kéo bao nhiêu để thùng vừa tới đỉnh thì dừng`,
    nd: `Kể đủ lực: ${m('\\vec F,\\ \\vec F_\\mathrm{ms},\\ \\vec P,\\ \\vec N')}; ${m('N')} có công ${f(12)}; lên dốc ${m('A_P=-mgh')} với ${m('h=')} ${f(14)}`, a: ['a', 'b'], gi: 6, fig: H.doc('') },
];

// Bài tương tự: mỗi dạng 2 bài, đáp số tính bằng Python (g = 10 m/s²)
const sideFig = (de, fig, w = 40) => `<div class="fig-side" style="grid-template-columns:1fr ${w}mm">${`<div>${de}</div>`}${fig}</div>`;
const tuongTu = {
  tieuDe: ['DẠNG 1–3', 'DẠNG 4–5'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Xe máy (kể cả người) ${u('150\\ \\mathrm{kg}')} chạy ${u('54\\ \\mathrm{km/h}')}.<br><b>a)</b> động năng (kJ)<br><b>b)</b> xe đạp ${u('75\\ \\mathrm{kg}')} cùng động năng: tốc độ (m/s)<br><b>c)</b> xe máy giảm còn ${u('18\\ \\mathrm{km/h}')}: động năng giảm mấy lần`, k: 3 },
    { t: 'Dạng 1 · Bài 2', de: `Quả bóng đá ${u('0{,}45\\ \\mathrm{kg}')} bay ${u('72\\ \\mathrm{km/h}')}.<br><b>a)</b> động năng (J)<br><b>b)</b> bóng tennis ${u('0{,}060\\ \\mathrm{kg}')} cùng động năng: tốc độ<br><b>c)</b> còn ${u('36\\ \\mathrm{km/h}')}: động năng còn mấy phần`, k: 3 },
    { t: 'Dạng 2 · Bài 1', de: `Mốc ở sàn, ${m('g=10\\ \\mathrm{m/s^2}')}. Đèn ${u('2{,}0\\ \\mathrm{kg}')} treo cao ${u('3{,}2\\ \\mathrm m')}; quạt ${u('4{,}0\\ \\mathrm{kg}')} treo cao ${u('2{,}8\\ \\mathrm m')}.<br><b>a)</b> thế năng của mỗi vật<br><b>b)</b> vật nào có thế năng lớn hơn<br><b>c)</b> vật ${u('5{,}0\\ \\mathrm{kg}')} có thế năng ${u('150\\ \\mathrm J')}: độ cao`, k: 3 },
    { t: 'Dạng 2 · Bài 2', de: `Mốc ở chân núi, ${m('g=10\\ \\mathrm{m/s^2}')}. Người ${u('60\\ \\mathrm{kg}')} đeo ba lô ${u('15\\ \\mathrm{kg}')} ở độ cao ${u('1200\\ \\mathrm m')}.<br><b>a)</b> thế năng của người (kJ)<br><b>b)</b> thế năng của ba lô (kJ)<br><b>c)</b> độ cao để người có thế năng ${u('900\\ \\mathrm{kJ}')}`, k: 3 },
    { t: 'Dạng 3 · Bài 1', de: sideFig(`Mặt nước giếng sâu ${u('5{,}0\\ \\mathrm m')} dưới mặt đất. Gàu nước ${u('3{,}0\\ \\mathrm{kg}')} treo cao ${u('1{,}2\\ \\mathrm m')} trên mặt đất, ${m('g=10\\ \\mathrm{m/s^2}')}.<br><b>a)</b> thế năng của gàu, mốc ở mặt đất<br><b>b)</b> thế năng của gàu, mốc ở mặt nước<br><b>c)</b> gàu thả xuống chạm mặt nước: thế năng, mốc ở mặt đất${lines(3)}`, H.gieng(''), 44), k: 0 },
    { t: 'Dạng 3 · Bài 2', de: `Sàn hầm sâu ${u('3{,}0\\ \\mathrm m')} dưới mặt đường; sàn tầng 5 cao ${u('12\\ \\mathrm m')}. Người ${u('50\\ \\mathrm{kg}')} đứng trên sàn hầm, ${m('g=10\\ \\mathrm{m/s^2}')}. Thế năng của người khi mốc tại:<br><b>a)</b> mặt đường<br><b>b)</b> sàn tầng 5<br><b>c)</b> sàn hầm`, k: 3 },
  ], [
    { t: 'Dạng 4 · Bài 1', de: `Người trượt tuyết ${u('70\\ \\mathrm{kg}')} từ A cao ${u('80\\ \\mathrm m')} xuống B cao ${u('30\\ \\mathrm m')} rồi lên C cao ${u('45\\ \\mathrm m')} (cùng mức chuẩn), ${m('g=10\\ \\mathrm{m/s^2}')}.<br><b>a)</b> công của trọng lực từ A đến B<br><b>b)</b> từ B đến C<br><b>c)</b> từ A đến C`, k: 3 },
    { t: 'Dạng 4 · Bài 2', de: `Cần cẩu nâng thùng ${u('25\\ \\mathrm{kg}')} từ mặt đất lên sàn tầng 4 cao ${u('12\\ \\mathrm m')}, rồi hạ xuống sàn tầng 2 cao ${u('6{,}0\\ \\mathrm m')}, ${m('g=10\\ \\mathrm{m/s^2}')}.<br><b>a)</b> công của trọng lực lúc nâng<br><b>b)</b> lúc hạ<br><b>c)</b> cả quá trình; thế năng tăng hay giảm bao nhiêu`, k: 3 },
    { t: 'Dạng 5 · Bài 1', de: sideFig(`Kéo xe trượt ${u('30\\ \\mathrm{kg}')} từ nghỉ ở chân dốc lên đỉnh bằng dây song song mặt dốc; dốc dài ${u('8{,}0\\ \\mathrm m')}, nghiêng ${m('30^\\circ')}; lực kéo ${u('250\\ \\mathrm N')}, ma sát ${u('40\\ \\mathrm N')}, ${m('g=10\\ \\mathrm{m/s^2}')}.<br><b>a)</b> công của từng lực (lực kéo, ma sát, trọng lực, phản lực)<br><b>b)</b> tốc độ của xe ở đỉnh dốc`, H.doc('', 's = 8,0 m'), 40), k: 4 },
    { t: 'Dạng 5 · Bài 2', de: `Thùng ${u('10\\ \\mathrm{kg}')} trượt từ nghỉ ở đỉnh dốc dài ${u('5{,}0\\ \\mathrm m')}, nghiêng ${m('30^\\circ')}; ma sát trên dốc ${u('15\\ \\mathrm N')}, ${m('g=10\\ \\mathrm{m/s^2}')}.<br><b>a)</b> tổng công các ngoại lực trên dốc (trọng lực, ma sát, phản lực)<br><b>b)</b> tốc độ ở chân dốc<br><b>c)</b> thùng trượt tiếp trên sàn ngang, ma sát ${u('20\\ \\mathrm N')}: đi thêm bao xa thì dừng`, k: 3 },
  ]],
  dap: [
    `D1·1: a) 16,9 kJ · b) 21,2 m/s · c) 9 lần &nbsp;|&nbsp; D1·2: a) 90 J · b) 54,8 m/s · c) 1/4 &nbsp;|&nbsp; D2·1: a) đèn 64 J; quạt 112 J · b) quạt · c) 3,0 m &nbsp;|&nbsp; D2·2: a) 720 kJ · b) 180 kJ · c) 1500 m &nbsp;|&nbsp; D3·1: a) 36 J · b) 186 J · c) −150 J &nbsp;|&nbsp; D3·2: a) −1500 J · b) −7500 J · c) 0`,
    `D4·1: a) 35 kJ · b) −10,5 kJ · c) 24,5 kJ &nbsp;|&nbsp; D4·2: a) −3000 J · b) +1500 J · c) −1500 J; thế năng tăng 1500 J &nbsp;|&nbsp; D5·1: a) ${m('A_F')} = 2000 J; ${m('A_\\mathrm{ms}')} = −320 J; ${m('A_P')} = −1200 J; ${m('A_N')} = 0 · b) 5,66 m/s &nbsp;|&nbsp; D5·2: a) 175 J · b) 5,92 m/s · c) 8,75 m`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 2], kq: [[1, 2, 3], [4, 5]] },
  tuongTu,
  tra: 'động năng 1·4 · định lí động năng 1·5 · gỗ trượt 2·1 · thế năng 2·2 · công trọng lực 2·3 · con lắc 3·1 · bẫy 3·2 · dạng 1–3 → 6·1 · dạng 4–5 → 7·1',
  out: process.argv[2],
});
