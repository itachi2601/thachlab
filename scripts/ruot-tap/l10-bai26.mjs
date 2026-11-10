// Ruột tập VL10 – Bài 26 · Cơ năng và định luật bảo toàn cơ năng (lesson id 71); trang 37–48 của quyển Chương 4 (bài 23–27).
// Khung: khung.mjs (bố cục bài 14: 1–5 học bài mới · 6–7 Bài tập mẫu · 8–9 Bài tương tự · 10–11 sửa bài · 12 làm lại + QR); hình: hinh-l10-bai26.mjs.
// Nguồn nội dung: bài web lesson 71 (book/cache/71.json: theory + 5 dạng bài tập mẫu). Không dùng ảnh Halliday (toàn bộ hình SVG tự vẽ).
// Đáp số Bài tương tự tính lại bằng Python (10/11/2026), g = 10 m/s².
// Chạy: node scripts/ruot-tap/l10-bai26.mjs [file.pdf] → scripts/ruot-tap/out/ruot-tap-vl10-bai26.pdf
import { khoiTao, m, lines, wl, fill as f, nw, ck, box, opt, chon, rkHai } from './khung.mjs';
import { hinh26 as H } from './hinh-l10-bai26.mjs';
const K = khoiTao({ bai: 26, lid: 71, ten: 'CƠ NĂNG · BẢO TOÀN CƠ NĂNG', lop: 10, baiDau: 23, sub: 'Vật lí 10 · Chương 4: Năng lượng, công, công suất' });
const { head, h3, foot } = K;
const fs = (w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;
const tb = (s) => `<div><b>${s}</b><span class="ck" style="float:right;margin:0"></span></div>`;
const Wd = m('W_\\mathrm{d}'), Wt = m('W_\\mathrm{t}'), W = m('W'), z = m('z'), v = m('v');
const u = (x, d) => nw(`${x}&nbsp;${d}`); // số + đơn vị không tách dòng
const g10 = m('g=10\\ \\mathrm{m/s^2}');
const fu = (w, d) => nw(`${f(w)}&nbsp;${d}`);

const p1 = `<section class="page">
${head('BÀI 26 · CƠ NĂNG · BẢO TOÀN CƠ NĂNG', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
<div style="margin:.3mm 0">${ck}Tính <b>cơ năng</b> ${m('W=W_\\mathrm{d}+W_\\mathrm{t}')} theo mốc thế năng đã chọn</div>
<div style="margin:.3mm 0">${ck}Phát biểu <b>định luật bảo toàn cơ năng</b>, nêu đúng điều kiện; dùng nó tìm tốc độ, độ cao</div>
<div style="margin:.3mm 0">${ck}Tính độ giảm cơ năng khi có <b>ma sát, lực cản</b>: ${m('\\Delta W=A_\\mathrm{c}')}</div>
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Lan trượt ván trong lòng chảo: thả mình ở mép trái, không đạp, không nhún. Coi như không có ma sát và lực cản. Lượt đầu, Lan lên thành bên kia tới đâu?</p>
<div class="fig-side" style="${fs(50)}"><div>
${opt('A', 'Thấp hơn mép xuất phát')}
${opt('B', 'Đúng ngang mép xuất phát')}
${opt('C', 'Cao hơn mép xuất phát')}
${opt('D', 'Còn tuỳ thành bên kia dốc hay thoải')}
<div style="margin-top:1mm">${chon(10)}</div><div class="hint">Vì sao?</div>${lines(1)}</div>
${H.longChao('Lan thả mình ở mép trái. Lượt đầu, Lan lên tới đâu?')}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Cơ năng', '1·4')}
<div class="card" style="padding:1.2mm 3mm">
<div>Cơ năng = ${f(16)} + ${f(16)} &nbsp;(đơn vị ${f(8)})</div>
<div>${m('W=')} ${f(10)} + ${f(10)}; ${z} đo từ ${f(14)}, trục hướng ${f(8)}; dưới mốc thì ${nw(`${z} ${f(6)} 0`)}</div>
<div>Táo ${u('0,2', 'kg')} treo yên ở cành cao ${u('5', 'm')}, mốc mặt đất: ${Wd} = ${f(8)}; ${Wt} = ${fu(10, 'J')} ⇒ ${W} = ${fu(8, 'J')}</div>
<div>Táo rơi tới độ cao ${u('1,8', 'm')} với ${m('v=8\\ \\mathrm{m/s}')}: ${W} = ${f(10)} + ${f(10)} = ${fu(8, 'J')}</div>
<div>Đổi mốc thì ${W} ${f(10)}; mốc ở cành thì quả táo treo yên có ${W} = ${f(8)}</div>
<div class="hint"><b>Nhớ:</b> động năng là ${m('\\tfrac12 mv^2')}: đừng quên hệ số ${m('\\tfrac12')}.</div></div>
${h3(5, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '1·5')}
${rkHai([1, 2, 3, 4], [5, 6, 7])}
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('BẢO TOÀN CƠ NĂNG · KIỂM CHỨNG BẰNG CON LẮC')}
${h3(1, 'II.2 · Định luật bảo toàn cơ năng', '2·1')}
<div class="card fig-side" style="${fs(42)};padding:1.2mm 3mm"><div>
<div>Điều kiện: chỉ ${f(16)} (hay lực ${f(14)}) sinh công.</div>
<div>Khi đó ${W} ${f(12)}: &nbsp;${m('W_1=W_2')}</div>
<div>${m('\\tfrac12 mv_1^2+')} ${f(12)} = ${f(12)} ${m('+\\,mgz_2')}</div>
<div>Không sinh công: phản lực của máng ${f(10)}, lực căng ${f(10)}, vì luôn ${f(16)} với đường đi.</div>
<div>${Wd} tăng bao nhiêu thì ${Wt} ${f(12)} bấy nhiêu. Chỗ thấp nhất: ${Wd} ${f(12)}; chỗ cao nhất: ${Wt} ${f(12)}.</div>
<div>Rơi hoặc trượt máng nhẵn từ độ cao ${m('h')}, xuất phát nghỉ: ${m('v=')} ${f(14)}, không phụ thuộc ${f(6)}.</div>
<div>Táo ở hình, tại ${u('2,5', 'm')}: ${Wt} = ${fu(6, 'J')}, ${Wd} = ${fu(6, 'J')}, ${nw(`${m('v\\approx')} ${fu(8, 'm/s')}`)}</div></div>
${H.cotTao()}</div>
${h3(2, 'II.3 · Thí nghiệm: con lắc qua cổng quang', '2·2')}
<div class="card fig-side" style="${fs(40)};padding:1.2mm 3mm"><div>
<div>Đo thời gian chắn sáng ${m('t')}, bề rộng tấm chắn ${m('d')} ⇒ ${m('v=')} ${f(10)}</div>
<table class="tbl-ct" style="margin:1mm 0"><tr><th>${m('h\\ (\\mathrm{cm})')}</th><th>5</th><th>10</th><th>15</th><th>20</th></tr>
<tr><td>${m('v\\ (\\mathrm{m/s})')}</td><td>0,98</td><td>1,39</td><td>1,70</td><td>1,97</td></tr>
<tr><td>${m('\\dfrac{v^2}{2gh}')} (%)</td><td></td><td></td><td></td><td></td></tr></table>
<div>Kéo lên 20 cm (cao gấp 4 lần 5 cm): ${v} qua cổng gấp ${f(8)} lần.</div>
<div>Rút ra: ${Wt} lúc thả gần bằng ${f(14)} ở chỗ thấp nhất; lực căng dây ${f(14)}.</div></div>
${H.conLacCong()}</div>
<div class="card" style="padding:0 3mm .4mm">${wl('Vì sao cả 4 lần đều dưới 100 %? (2 nguyên nhân)', 3)}${wl('Vì sao lần h = 5 cm lệch nhiều nhất?', 1)}</div>
${h3(3, 'Tự kiểm tra: bi trên máng nhẵn', '2·3')}
<div class="card" style="padding:1mm 3mm"><div>Thả bi từ đỉnh máng nhẵn cao ${u('0,45', 'm')}; ${g10}:</div><div>${nw(`${m('v=\\sqrt{2gh}=')} ${f(16)}`)} ${nw(`= ${fu(8, 'm/s')}`)}</div>
<div>Đề không cho ${m('m')} vẫn tính được vì ${f(26)}. &nbsp;<b>Nhớ:</b> ra ${m('v^2')} rồi nhớ ${nw(`${f(10)}.`)}</div></div>
${h3(4, 'Xem thêm: cơ năng có lò xo', '2·4')}
<div class="card soft" style="padding:1mm 3mm">Lò xo ngang, không ma sát: ${m('W=\\tfrac12 mv^2+')} ${f(16)} &nbsp;(${m('k')}: ${f(12)}; ${nw(`${m('\\Delta l')}: ${f(12)})`)}</div>
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('KHI CÓ MA SÁT · BẪY · TRẢ BÀI')}
${h3(1, 'II.4 · Khi có ma sát, lực cản', '3·1')}
<div class="card fig-side" style="${fs(44)};padding:1.2mm 3mm"><div>
<div>Ma sát, lực cản sinh công ⇒ cơ năng ${f(18)}.</div>
<div>${m('\\Delta W=W_2-W_1=')} ${f(10)}; &nbsp;${m('A_\\mathrm{c}')} ${f(6)} 0 ⇒ ${W} ${f(10)}</div>
<div>Phần cơ năng mất thành ${f(14)}, âm thanh.</div>
<div>Lực kéo cùng chiều chuyển động: ${m('A')}<sub>khác</sub> ${f(6)} 0 ⇒ ${W} ${f(10)}</div>
<table class="tbl-ct" style="margin-top:.6mm"><tr><th>bóng bàn · lần nảy</th><th>0</th><th>1</th><th>2</th><th>3</th></tr>
<tr><td>độ cao đỉnh (m)</td><td>1,00</td><td>0,80</td><td>0,64</td><td>0,51</td></tr>
<tr><td>${m('h_n/h_{n-1}')}</td><td>–</td><td></td><td></td><td></td></tr></table>
<div>Ở đỉnh ${m('v=')} ${f(6)} nên ${W} tỉ lệ với ${f(12)}; mỗi lần chạm bàn mất ≈ ${fu(8, '%')} cơ năng.</div></div>
${H.dinhThapDan()}</div>
${h3(2, 'III · Ba cái bẫy hay sập', '3·2')}
<div class="card" style="padding:1mm 3mm">
<div class="trap">${ck}<span><b>“Cơ năng lúc nào cũng bảo toàn.”</b> Phải soát mọi lực: ô tô phanh xuống dốc đều có ${v} không đổi mà ${z} giảm ⇒ ${W} giảm.</span></div>
<div class="trap">${ck}<span><b>“Bảo toàn thì động năng không đổi.”</b> Giữ <b>tổng</b>, không giữ từng phần: ${Wd} và ${Wt} đổi qua lại.</span></div>
<div class="trap">${ck}<span><b>“Mỗi vị trí một mốc.”</b> Chọn mốc một lần, mọi ${z} đo từ đó; đổi mốc thì ${W} đổi, nhưng ${v} tính ra không đổi.</span></div></div>
${h3(3, 'IV · Trả bài 6 câu', '3·3')}
${box(`${tb('1. Cơ năng là gì? Công thức, đơn vị?')}${lines(1)}
${tb('2. Phát biểu định luật bảo toàn cơ năng và điều kiện.')}${lines(2)}
${tb('3. Lực căng dây, phản lực máng nhẵn có phá bảo toàn không? Vì sao?')}${lines(1)}
${tb('4. Khi bảo toàn, động năng cực đại ở đâu?')}${lines(1)}
${tb('5. Có ma sát, lực cản thì cơ năng thay đổi thế nào?')}${lines(1)}
${tb('6. Cơ năng bảo toàn có nghĩa tốc độ không đổi không?')}${lines(1)}`)}
<div class="card soft" style="margin-top:1.5mm;padding:1mm 3mm"><b>Bạn cùng bàn kiểm:</b> nói được ……/6 câu · câu chưa thuộc: ${f(26)} → đọc lại ô Tập ${f(14)}</div>
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('BÀI TOÁN MẪU · LAN TRONG LÒNG CHẢO')}
${h3(1, 'V · Đề bài', '4')}
<div class="card soft" style="padding:1.2mm 3mm">Lan cùng ván trượt nặng ${u('50', 'kg')}, xuất phát không vận tốc đầu từ mép ${m('A')} của lòng chảo, cao ${u('3,2', 'm')} so với đáy ${m('O')}. ${g10}, mốc thế năng ở đáy.
<div><b>a)</b> Bỏ qua ma sát, lực cản: tính cơ năng và tốc độ của Lan tại ${m('O')}.</div>
<div><b>b)</b> Vẫn bỏ qua ma sát: tính tốc độ tại ${m('M')} cao ${u('1,4', 'm')}.</div>
<div><b>c)</b> Thực tế Lan chỉ lên tới ${m('B')} cao ${u('2,8', 'm')} ở thành bên kia rồi dừng. Tính công của ma sát và lực cản từ ${m('A')} đến ${m('B')}.</div></div>
${h3(2, 'Phân tích đề (điền cùng thầy)')}
<table><tr><th style="width:50mm">Câu trong đề</th><th style="width:34mm">Dữ liệu</th><th>Kiến thức liên quan</th></tr>
<tr><td>“nặng 50 kg”</td><td>${m('m=50\\ \\mathrm{kg}')}</td><td>cả người và ván</td></tr>
<tr><td style="height:6.5mm">“không vận tốc đầu từ mép A”</td><td></td><td></td></tr>
<tr><td style="height:6.5mm">“cao 3,2 m so với đáy”, “mốc ở đáy”</td><td></td><td></td></tr>
<tr><td style="height:6.5mm">“bỏ qua ma sát và lực cản”</td><td></td><td></td></tr>
<tr><td style="height:6.5mm">“lên tới B cao 2,8 m rồi dừng”</td><td></td><td></td></tr></table>
${h3(3, 'Giải')}
<div class="fig-side" style="${fs(50)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl('a)', 3)}${wl('b)', 3)}${wl('c)', 3)}</div>${H.baiMau()}</div>
${h3(4, 'Mở rộng: Lan đẩy đà ở A với 2 m/s')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div class="ln" style="height:auto;padding-top:1mm"><b>Bước 1 (cho sẵn):</b> ${m('W_A=\\tfrac12\\cdot50\\cdot2^2+1600=1700\\ \\mathrm{J}')}.</div>
${wl(`Bước 2: ${m('v_O')} = …`, 2)}${wl('Bước 3: tới mép bên kia (cao 3,2 m), Lan còn tốc độ bao nhiêu?', 2)}</div>
<div class="card soft" style="margin-top:1.5mm;padding:1mm 3mm"><b>Em tự kiểm:</b> ${ck}một mốc cho cả bài &nbsp;${ck}khai căn ra ${v} &nbsp;${ck}${m('A_\\mathrm{c}')} mang dấu âm</div>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TẬP VỀ NHÀ · MANG VỀ · THỬ THÁCH')}
${K.btvn()}
${h3(2, 'VI · Mang về: điều em dễ quên nhất', '5')}
${box(wl('1.', 2) + wl('2.', 2) + wl('3.', 2))}
${h3(3, 'Đời sống: chọn 2 nơi dùng bài này')}
${box(wl('Thuỷ điện · búa máy đóng cọc · nhảy cao · tàu lượn: năng lượng đổi từ dạng nào sang dạng nào?', 3))}
${h3(4, 'Thử thách phân tầng')}
<div class="fig-side" style="grid-template-columns:1fr 40mm">${box(wl('★ Thả rơi tự do một vật từ 20 m. Tốc độ khi chạm đất?', 2)
 + wl('★★ Con lắc dây 0,8 m kéo lệch 60° rồi thả. Tốc độ ở vị trí thấp nhất?', 3)
 + wl('★★★ Toa tàu lượn 400 kg rời đỉnh cao 25 m (gần như đứng yên), qua đỉnh hai cao 20 m với 8 m/s. Công lực cản? Đỉnh hai cao 25 m thì toa lên được không?', 4))}${H.conLac60()}</div>
${h3(5, 'Câu 7 và mô phỏng PhET')}
${box(wl('Câu 7 (bài toán mẫu): ở độ cao nào động năng của Lan bằng thế năng?', 2)
 + wl('PhET, màn Ma sát · ma sát nhỏ nhất, thả từ cao · Dự đoán tổng cơ năng:', 1) + wl('Thấy:', 1)
 + wl('Tăng ma sát · phần năng lượng chuyển thành gì?', 1))}
${foot(5)}</section>`;

// ---- Bài tập mẫu: 5 dạng theo web (lesson 71). Dạng 1–2 giải nhẩm (chỉ đáp số, hình cạnh đề); ô giải từ dạng 3 ----
const deFig = (txt, fig, w = 40) => `<div class="fig-side" style="grid-template-columns:1fr ${w}mm;gap:2mm"><div>${txt}</div>${fig}</div>`;
const dang = [
  { t: 'Dạng 1 · Dễ · Cơ năng theo mốc thế năng',
    de: deFig(`Hòn đá ${u('0,20', 'kg')} ném thẳng đứng lên từ cửa sổ cao ${u('6,0', 'm')}; đang lên, qua ${m('P')} cao ${u('8,0', 'm')} với ${u('3,0', 'm/s')}. Mái cao ${u('10', 'm')}; ${g10}.<br><b>a)</b> ${Wd} tại ${m('P')}<br><b>b)</b> ${W} tại ${m('P')}, mốc ở mặt đất<br><b>c)</b> ${W}, mốc ở cửa sổ<br><b>d)</b> ${W}, mốc ở mái`, H.baMoc('')),
    nd: `${Wd} ${f(14)} mốc; ${m('W_\\mathrm{t}=mgz')} với ${z} đo từ ${f(10)}; dưới mốc thì ${nw(`${z} ${f(5)} 0`)}`, a: ['a', 'b', 'c', 'd'], gi: 0 },
  { t: 'Dạng 2 · Dễ · Bảo toàn cơ năng: tìm tốc độ, độ cao',
    de: deFig(`Bi ${u('50', 'g')} thả không vận tốc đầu từ đỉnh ${m('A')} của máng cong nhẵn, ${m('A')} cao ${u('2,45', 'm')} so với chân máng ${m('O')}; bỏ qua lực cản, ${g10}.<br><b>a)</b> tốc độ tại ${m('O')}<br><b>b)</b> tốc độ tại ${m('M')} cao ${u('1,2', 'm')}<br><b>c)</b> độ cao của ${m('N')}, nơi bi có ${u('3,0', 'm/s')}`, H.mangCong('')),
    nd: `Máng nhẵn → chỉ ${f(14)} sinh công → ${m('W_A=W_O')}; ${m('m')} ở hai vế nên ${f(14)}`, a: ['a', 'b', 'c'], gi: 0 },
  { t: 'Dạng 3 · Trung bình · Vị trí động năng bằng thế năng',
    de: `Hòn đá ${u('0,40', 'kg')} ném thẳng đứng lên từ mặt đất với ${u('12', 'm/s')}; bỏ qua sức cản, ${g10}, mốc ở mặt đất.<br><b>a)</b> lúc đi lên, cơ năng thay đổi thế nào?<br><b>b)</b> cơ năng của hòn đá<br><b>c)</b> độ cao nơi ${m('W_\\mathrm{d}=W_\\mathrm{t}')}<br><b>d)</b> ${Wd} ở độ cao ${u('5,0', 'm')}`,
    nd: `${m('W_\\mathrm{d}=W_\\mathrm{t}')} ⇒ ${m('W=')} ${f(6)} ${Wt}; tốc độ đổi không có nghĩa ${W} đổi`, a: ['a', 'b', 'c', 'd'], gi: 6 },
  { t: 'Dạng 4 · Khó · Ném lên từ sân thượng, đổi mốc',
    de: `Từ sân thượng cao ${u('3,0', 'm')}, ném thẳng đứng lên hòn sỏi ${u('0,20', 'kg')}; sỏi lên tới ${u('8,0', 'm')} so với mặt đất rồi rơi. Bỏ qua cản, ${g10}, mốc ở mặt đất.<br><b>a)</b> cơ năng của sỏi<br><b>b)</b> tốc độ lúc ném<br><b>c)</b> độ cao nơi ${m('W_\\mathrm{d}=3W_\\mathrm{t}')}<br><b>d)</b> mốc ở sân thượng: cơ năng và độ cao cực đại so với mốc mới`,
    nd: `Điểm cao nhất ${m('v=')} ${f(6)} ⇒ ${m('W=')} ${f(10)}; ${m('W_\\mathrm{d}=nW_\\mathrm{t}')} ⇒ ${m('W=')} ${f(10)} ${Wt}`, a: ['a', 'b', 'c', 'd'], gi: 6, fig: H.sanThuong('') },
  { t: 'Dạng 5 · Khó · Có lực cản: công của lực cản',
    de: `Vận động viên trượt tuyết ${u('50', 'kg')} (kể cả dụng cụ) xuất phát từ nghỉ ở đỉnh dốc ${m('A')} cao ${u('10', 'm')} so với chân dốc ${m('B')}, tới ${m('B')} với ${u('12', 'm/s')}; ${g10}, mốc ở chân dốc.<br><b>a)</b> cơ năng tại ${m('A')} và tại ${m('B')}<br><b>b)</b> công của lực cản trên dốc<br><b>c)</b> lực cản lấy đi bao nhiêu % cơ năng ban đầu<br><b>d)</b> lượt khác qua ${m('A')} với ${u('5,0', 'm/s')}, công lực cản như cũ: tốc độ ở ${m('B')}`,
    nd: `Có lực cản → không dùng ${m('W_1=W_2')}: ${m('A_\\mathrm{c}=')} ${f(10)} − ${f(10)}, ${m('A_\\mathrm{c}')} ${f(5)} 0`, a: ['a', 'b', 'c', 'd'], gi: 6, fig: H.docTruot('') },
];

// ---- Bài tương tự: mỗi dạng 2 bài (2–3 ý), đáp số tính bằng Python. Ý bên trái, dòng kẻ bên phải (mỗi ý đối diện dòng của nó) ----
const yk = (ys, k) => `<div style="display:grid;grid-template-columns:62mm 1fr;gap:2mm;align-items:start"><div>${ys.map((y, i) => `<div style="line-height:5mm"><b>${'abcd'[i]})</b> ${y}</div>`).join('')}</div><div>${lines(k)}</div></div>`;
const tt = (t, stem, ys, k, fig, w) => fig ? { t, de: deFig(`${stem}<br>${ys.map((y, i) => `<b>${'abcd'[i]})</b> ${y}`).join('<br>')}`, fig, w), k }
  : { t, de: stem + yk(ys, k), k: 0 };
const tuongTu = {
  tieuDe: ['DẠNG 1–3', 'DẠNG 4–5'],
  trang: [[
    tt('Dạng 1 · Bài 1', `Bóng ${u('0,50', 'kg')} qua ${m('P')} cao ${u('4,0', 'm')} so với sàn với ${u('4,0', 'm/s')}; trần cao ${u('6,0', 'm')}; ${g10}.`, [`${Wd} tại ${m('P')}`, `${W}, mốc ở sàn`, `${W}, mốc ở trần`], 4),
    tt('Dạng 1 · Bài 2', `Táo ${u('0,15', 'kg')} rơi qua độ cao ${u('2,0', 'm')} với ${u('6,0', 'm/s')}; cành cao ${u('3,8', 'm')}; ${g10}.`, [`${W}, mốc ở mặt đất`, `${W}, mốc ở cành`], 2),
    tt('Dạng 2 · Bài 1', `Thả vật từ đỉnh máng nhẵn cao ${u('1,8', 'm')}, không vận tốc đầu; ${g10}.`, [`tốc độ ở chân máng`, `độ cao nơi vật có ${u('5,0', 'm/s')}`], 2, H.mangCong('', { hA: '1,8 m', hM: '' }), 28),
    tt('Dạng 2 · Bài 2', `Thả rơi bi từ độ cao ${u('7,2', 'm')}, bỏ qua lực cản; ${g10}.`, [`tốc độ khi chạm đất`, `tốc độ ở độ cao ${u('4,0', 'm')}`], 3),
    tt('Dạng 3 · Bài 1', `Ném thẳng lên từ mặt đất bóng ${u('0,50', 'kg')} với ${u('8,0', 'm/s')}; bỏ qua cản; ${g10}; mốc mặt đất.`, [`cơ năng`, `độ cao nơi ${m('W_\\mathrm{d}=W_\\mathrm{t}')}`, `${Wd} ở độ cao ${u('1,2', 'm')}`], 4),
    tt('Dạng 3 · Bài 2', `Thả rơi vật ${u('0,20', 'kg')} từ độ cao ${u('15', 'm')}; bỏ qua cản; ${g10}; mốc mặt đất.`, [`độ cao nơi ${m('W_\\mathrm{d}=W_\\mathrm{t}')}`, `tốc độ của vật khi đó`], 3),
  ], [
    tt('Dạng 4 · Bài 1', `Từ ban công cao ${u('5,0', 'm')} ném thẳng đứng lên vật ${u('0,10', 'kg')}; vật lên tới ${u('10', 'm')} so với mặt đất. Bỏ qua cản, ${g10}, mốc ở mặt đất.`, [`tốc độ lúc ném`, `độ cao nơi ${m('W_\\mathrm{d}=4W_\\mathrm{t}')}`, `mốc ở ban công: cơ năng và độ cao cực đại so với mốc mới`], 5, H.sanThuong('', { top: '10 m', base: '5,0 m', ten: 'ban công' }), 34),
    tt('Dạng 4 · Bài 2', `Từ độ cao ${u('4,0', 'm')} ném thẳng đứng lên hòn sỏi ${u('0,20', 'kg')} với ${u('6,0', 'm/s')}; bỏ qua cản, ${g10}, mốc ở mặt đất.`, [`độ cao cực đại so với mặt đất`, `tốc độ khi chạm đất`], 4),
    tt('Dạng 5 · Bài 1', `Xe trượt ${u('40', 'kg')} (kể cả người) xuất phát từ nghỉ ở đỉnh dốc cao ${u('8,0', 'm')}, tới chân dốc với ${u('10', 'm/s')}; ${g10}, mốc ở chân dốc.`, [`công của lực cản`, `phần trăm cơ năng bị mất`, `lượt khác qua đỉnh với ${u('3,0', 'm/s')}, công lực cản như cũ: tốc độ ở chân dốc`], 5, H.docTruot('', { h: '8,0 m', v: '10 m/s' }), 34),
    tt('Dạng 5 · Bài 2', `Thả quả bóng ${u('0,40', 'kg')} từ độ cao ${u('5,0', 'm')}, chạm đất với ${u('9,0', 'm/s')}; ${g10}, mốc ở mặt đất.`, [`công của lực cản không khí`, `phần trăm cơ năng bị mất`], 4),
  ]],
  dap: [
    `D1·1: a) 4,0 J · b) 24 J · c) −6,0 J &nbsp;|&nbsp; D1·2: a) 5,7 J · b) 0 J &nbsp;|&nbsp; D2·1: a) 6,0 m/s · b) 0,55 m &nbsp;|&nbsp; D2·2: a) 12 m/s · b) 8,0 m/s &nbsp;|&nbsp; D3·1: a) 16 J · b) 1,6 m · c) 10 J &nbsp;|&nbsp; D3·2: a) 7,5 m · b) ≈ 12,2 m/s`,
    `D4·1: a) 10 m/s · b) 2,0 m · c) 5,0 J; 5,0 m &nbsp;|&nbsp; D4·2: a) 5,8 m · b) ≈ 10,8 m/s &nbsp;|&nbsp; D5·1: a) −1 200 J · b) 37,5 % · c) ≈ 10,4 m/s &nbsp;|&nbsp; D5·2: a) −3,8 J · b) 19 %`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 2], kq: [[1, 2, 3], [4, 5]] },
  tuongTu,
  tra: 'cơ năng 1·4 · bảo toàn 2·1 · con lắc 2·2 · bi trên máng 2·3 · ma sát, bóng nảy 3·1 · bẫy 3·2 · trả bài 3·3 · dạng 1–3 → 6·1 · dạng 4–5 → 7·1',
  out: process.argv[2],
});
