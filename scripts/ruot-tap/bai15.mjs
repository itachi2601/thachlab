// Ruột tập VL12 – Bài 15 · Năng lượng liên kết hạt nhân (lesson id 16). Khung chung: khung.mjs; hình: hinh-ch4.mjs.
// Chạy: node scripts/ruot-tap/bai15.mjs [file.pdf] → scripts/ruot-tap/out/ruot-tap-vl12-bai15.pdf
import { khoiTao, m, lines, wl, fill as f, nw, exp, ck, box, opt, chon, rkHai, hinh } from './khung.mjs';
const K = khoiTao({ bai: 18, baiDau: 17, lid: 16, ten: 'NĂNG LƯỢNG LIÊN KẾT HẠT NHÂN' });
const { head, h3, card, foot } = K;
const fs = (fig, w, extra = '') => `grid-template-columns:1fr ${w}mm;${extra}`;

const p1 = `<section class="page">
${head('BÀI 18 · NĂNG LƯỢNG LIÊN KẾT HẠT NHÂN', K.sub)}
${h3(1, 'Mục tiêu', '1·1')}
<div class="card soft">
<div style="margin:.3mm 0">${ck}Nêu được <b>lực hạt nhân</b> giữ các nuclôn và vì sao hạt nhân không bung ra</div>
<div style="margin:.3mm 0">${ck}Tính <b>độ hụt khối</b> và <b>năng lượng liên kết</b> ${m('E_{lk}')}</div>
<div style="margin:.3mm 0">${ck}Tính ${m('E_{lkr}')} và dùng nó để <b>so độ bền</b> các hạt nhân</div>
</div>
${h3(2, 'Dự đoán trước khi học', '1·2')}
<div class="card">
<p style="margin:0 0 1mm">Các prôtôn trong hạt nhân đẩy nhau. Vì sao hạt nhân vẫn đứng vững?</p>
<div class="fig-side" style="${fs('', 52)}"><div>
${opt('A', 'Lực hạt nhân hút các nuclôn mạnh hơn hẳn lực đẩy tĩnh điện')}
${opt('B', 'Lực đẩy tĩnh điện giữa các prôtôn rất yếu')}
${opt('C', 'Êlectron ở vỏ hút ngược các prôtôn vào trong')}
<div style="margin-top:1.5mm">${chon(10)}</div><div class="hint">Vì sao?</div>${lines(1)}</div>
${hinh.lucHatNhan('Hai prôtôn cách ~10<sup>−15</sup> m: đẩy (nét đặc) bị lực hạt nhân (nét đứt) thắng.')}</div>
</div>
${h3(3, 'Học xong, em sửa lại', '1·3')}
<div class="card soft"><div>Đáp án đúng là: ${f()} &nbsp; Em đoán ${ck}đúng &nbsp;${ck}sai &nbsp;· <span class="hint">Điều em hiểu sai hoặc mới biết:</span></div>${lines(1)}</div>
${h3(4, 'II.1 · Lực hạt nhân', '1·4')}
<div class="card" style="padding:1.2mm 3mm">
<div>Lực hạt nhân là lực ${f(14)} giữa các ${f(16)}; ${f(12)} phụ thuộc điện tích (p–p, p–n, n–n hút ${f(12)}).</div>
<div>Rất ${f(12)} nhưng tầm rất ngắn, cỡ ${nw(`10${exp}&nbsp;m`)}; không phải lực ${f(16)} hay lực ${f(16)}.</div></div>
${h3(5, 'II.2 · Đo khối lượng hạt nhân', '1·5')}
<div class="card" style="padding:1.2mm 3mm">
<div>Không cân được hạt nhân: đo khối lượng ${f(18)} (gồm cả ${f(14)}) rồi suy ra, chính xác tới phần ${f(12)}.</div>
<div>${m('1\\ \\mathrm{u}=')} ${nw(`${f(20)}&nbsp;kg`)} ≈ ${nw(`${f(12)}&nbsp;${m('\\mathrm{MeV}/c^2')}`)}</div>
<div>${m('m_p=')} ${f(20)} u &nbsp;·&nbsp; ${m('m_n=')} ${f(20)} u &nbsp;·&nbsp; ${m('m_e=')} ${f(16)} u</div></div>
${foot(1)}</section>`;

const p2 = `<section class="page">
${head('KHỐI LƯỢNG – NĂNG LƯỢNG · ĐỘ HỤT KHỐI')}
${h3(1, 'II.3 · Hệ thức Einstein', '2·1')}
<div class="card" style="padding:1.2mm 3mm">
<div>${m('E=')} ${f(10)} · ${f(10)}<span class="nw"><sup>2</sup></span> &nbsp;→&nbsp; ${m('1\\ \\mathrm{u}\\cdot c^2=')} ${nw(`${f(14)}&nbsp;MeV`)}</div>
<div>Năng lượng nghỉ một prôtôn: ${m('1{,}007276\\times931{,}5=')} ${nw(`${f(16)}&nbsp;MeV`)}</div></div>
${h3(2, 'II.4 · Độ hụt khối, năng lượng liên kết', '2·2')}
<div class="card fig-side" style="${fs('', 52)};padding:1.2mm 3mm"><div>
<div>${m('\\Delta m=Z\\cdot')} ${f(8)} ${m('+(A-Z)\\cdot')} ${f(8)} ${m('-')} ${f(8)}</div>
<div>Đề cho khối lượng <b>nguyên tử</b> → cộng thêm ${f(8)}·${m('m_e')} vào tổng hạt rời.</div>
<div>${m('E_{lk}=')} ${f(10)} ${m('\\cdot c^2=\\Delta m(\\mathrm{u})\\times')} ${f(12)} MeV</div>
<div>${m('E_{lkr}=')} ${f(10)} / ${f(10)} (MeV/nuclôn); càng ${f(10)} càng bền.</div>
<div>Tách hạt nhân thành nuclôn rời: ${f(12)} năng lượng; tạo thành: ${f(12)}.</div></div>
${hinh.doHutKhoi('Vẽ phóng đại: hiệu chỉ 0,76 %. Nguyên tử nhẹ hơn tổng hạt rời.')}</div>
${h3(3, 'Tính cho bốn hạt nhân (Δm đã cho)', '2·3')}
<table class="tbl-ct"><tr><th style="width:24mm">Hạt nhân</th><th style="width:33mm">${m('\\Delta m\\ (\\mathrm{u})')}</th><th>${m('E_{lk}\\ (\\mathrm{MeV})')}</th><th>${m('E_{lkr}\\ (\\text{MeV/nuclôn})')}</th></tr>
<tr><td>${m('{}^{4}_{2}\\mathrm{He}')}</td><td>0,030377</td><td></td><td></td></tr>
<tr><td>${m('{}^{16}_{\\ 8}\\mathrm{O}')}</td><td>0,137005</td><td></td><td></td></tr>
<tr><td>${m('{}^{56}_{26}\\mathrm{Fe}')}</td><td>0,528462</td><td></td><td></td></tr>
<tr><td>${m('{}^{235}_{\\ 92}\\mathrm{U}')}</td><td>1,915057</td><td></td><td></td></tr></table>
${h3(4, 'II.5 · Đọc đường cong ' + m('E_{lkr}'), '2·4')}
<div class="card fig-side" style="${fs('', 56)};padding:1.2mm 3mm"><div>
<div>${m('E_{lkr}')} lớn nhất quanh ${f(12)}, cỡ ${nw(`${f(8)}&nbsp;MeV/nuclôn`)}.</div>
<div>Hạt nhân nhẹ hợp lại: ${m('E_{lkr}')} ${f(10)} → ${f(10)} năng lượng.</div>
<div>Hạt nhân nặng vỡ ra: ${m('E_{lkr}')} ${f(10)} → ${f(10)} năng lượng.</div>
<div>Mẹo nhớ: “bền nhất ở ${f(10)}, hai đầu đều ${f(8)}”.</div></div>
${hinh.duongCongLkr('Đỉnh ở giữa (sắt-56): hạt nhân nhẹ hợp lại và nặng vỡ ra đều tiến về đỉnh.')}</div>
${foot(2)}</section>`;

const p3 = `<section class="page">
${head('BẪY · TRẢ BÀI · KẾT QUẢ TỰ KIỂM TRA')}
${h3(1, 'II.6 · Hoá học và hạt nhân', '3·1')}
<div class="card" style="padding:1.2mm 3mm">Đốt một phân tử: vài ${nw(`${f(8)}&nbsp;eV`)}; tạo một hạt nhân He-4: ${nw(`${f(8)}&nbsp;MeV`)} → hơn nhau cỡ ${nw(`10${exp}&nbsp;lần`)}.</div>
${h3(2, 'III · Ba cái bẫy hay sập', '3·2')}
<div class="card" style="padding:1mm 3mm">
<div class="trap">${ck}<span><b>“Khối lượng đã mất đi.”</b> Không mất: chuyển thành năng lượng ${m('E=\\Delta m\\,c^2')}.</span></div>
<div class="trap">${ck}<span><b>“${m('E_{lk}')} lớn là bền.”</b> Phải chia cho ${m('A')}, so bằng ${m('E_{lkr}')}.</span></div>
<div class="trap">${ck}<span><b>“Hạt nhân càng lớn càng bền.”</b> Qua vùng sắt thì ngược lại.</span></div></div>
${h3(3, 'IV · Trả bài 6 câu', '3·3')}
${box(`<div><b>1.</b> Lực hạt nhân là gì? Ba đặc điểm?<span class="ck" style="float:right;margin:0"></span></div>${lines(2)}
<div><b>2.</b> Độ hụt khối là gì? Khi nào phải cộng ${m('Zm_e')}?<span class="ck" style="float:right;margin:0"></span></div>${lines(2)}
<div><b>3.</b> Năng lượng liên kết là gì? Tạo thành hạt nhân thì toả hay thu?<span class="ck" style="float:right;margin:0"></span></div>${lines(2)}
<div><b>4.</b> ${m('E_{lkr}')} là gì? Vì sao dùng nó để so độ bền?<span class="ck" style="float:right;margin:0"></span></div>${lines(2)}
<div><b>5.</b> Xu hướng ${m('E_{lkr}')} hai bên đỉnh sắt?<span class="ck" style="float:right;margin:0"></span></div>${lines(2)}
<div><b>6.</b> Vì sao tính ${m('E_{lk}')} bằng 931,5 MeV/u không nhân ${m('c^2')} nữa?<span class="ck" style="float:right;margin:0"></span></div>${lines(2)}`)}
<div class="card soft" style="margin-top:1.5mm;padding:1mm 3mm"><b>Bạn cùng bàn kiểm:</b> nói được ……/6 câu · câu chưa thuộc: ${f(30)} → đọc lại ô Tập ${f(14)}</div>
${h3(4, 'Kết quả tự kiểm tra (đề chiếu trên lớp)', '3·4')}
${rkHai([2, 3, 4, 5], [6, 7, 8])}
${foot(3)}</section>`;

const p4 = `<section class="page">
${head('BÀI TOÁN MẪU · NĂNG LƯỢNG LIÊN KẾT CỦA HELI-4')}
${h3(1, 'V · Đề bài', '4')}
<div class="card soft" style="padding:1.2mm 3mm">Nguyên tử ${m('{}^{4}_{2}\\mathrm{He}')} có ${m('m_{\\mathrm{He}}=4{,}002603\\ \\mathrm{u}')}; ${m('m_p=1{,}007276\\ \\mathrm{u}')}, ${m('m_n=1{,}008665\\ \\mathrm{u}')}, ${m('m_e=0{,}000549\\ \\mathrm{u}')}; ${m('1\\ \\mathrm{u}=931{,}5\\ \\mathrm{MeV}/c^2')}.
<div><b>a)</b> Tính độ hụt khối của hạt nhân.</div><div><b>b)</b> Tính ${m('E_{lk}')} và ${m('E_{lkr}')}.</div><div><b>c)</b> Tách hạt nhân thành nuclôn rời thì cấp vào hay thu về bao nhiêu năng lượng?</div></div>
${h3(2, 'Phân tích đề (điền cùng thầy)')}
<table><tr><th style="width:46mm">Câu trong đề</th><th style="width:36mm">Dữ liệu</th><th>Kiến thức liên quan</th></tr>
<tr><td>“khối lượng nguyên tử ${m('m_{\\mathrm{He}}')}”</td><td>đã gồm 2 êlectron</td><td>cộng ${m('Zm_e')}</td></tr>
<tr><td style="height:6.5mm">“${m('m_p,\\ m_n,\\ m_e')}”</td><td></td><td></td></tr>
<tr><td style="height:6.5mm">“${m('{}^{4}_{2}\\mathrm{He}')}”</td><td></td><td></td></tr>
<tr><td style="height:6.5mm">“${m('1\\ \\mathrm{u}=931{,}5')}”</td><td></td><td></td></tr>
<tr><td style="height:6.5mm">“tách thành nuclôn rời”</td><td></td><td></td></tr></table>
${h3(3, 'Giải')}
<div class="fig-side" style="${fs('', 56)};margin-top:1mm"><div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
${wl('a)', 4)}${wl('b)', 3)}${wl('c)', 2)}</div>${hinh.bacThangNL('Tạo thành: toả; tách ra: cấp vào cùng một lượng.')}</div>
${h3(4, 'Mở rộng: đơteri')}
<div style="background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:0 3mm">
<div class="ln" style="height:auto;padding-top:1mm"><b>Bước 1 (cho sẵn):</b> ${m('{}^{2}_{1}\\mathrm{H}')}, ${m('m_{\\mathrm{H}}=2{,}014102\\ \\mathrm{u}')}; tổng hạt rời ${m('m_p+m_n+m_e=2{,}016490\\ \\mathrm{u}')}.</div>
${wl('Bước 2: Δm = …', 2)}${wl('Bước 3: E<sub>lk</sub> = …  ·  E<sub>lkr</sub> = …', 2)}${wl('Bước 4: so với 7,07 MeV của He-4 → bền hơn hay kém?', 2)}</div>
<div class="card soft" style="margin-top:1.5mm;padding:1mm 3mm"><b>Em tự kiểm:</b> ${ck}có cộng ${m('Zm_e')} &nbsp;${ck}không làm tròn khối lượng &nbsp;${ck}có ghi đơn vị</div>
${foot(4)}</section>`;

const p5 = `<section class="page">
${head('BÀI TẬP VỀ NHÀ · MANG VỀ · THỬ THÁCH')}
${K.btvn()}
${h3(2, 'VI · Mang về: điều em dễ quên nhất', '5')}
${box(wl('1.', 2) + wl('2.', 2) + wl('3.', 2))}
${h3(3, 'Thử thách phân tầng')}
<div class="fig-side" style="${fs('', 52)}">${box(`<div class="ln"><b>★ ${m('{}^{16}_{\\ 8}\\mathrm{O}')}:</b> ${m('\\Delta m=0{,}137005\\ \\mathrm{u}')} → ${m('E_{lkr}=')} ${f(22)}</div>` + wl('★★ Vì sao urani có E<sub>lk</sub> lớn hơn sắt mà lại kém bền?', 3) + wl('★★★ Tổng E<sub>lk</sub> sau phản ứng lớn hơn trước: toả hay thu? Vì sao không cần Δm?', 4))}<div style="display:grid;gap:2mm">${hinh.anh('nang-luong-lien-ket-rieng.png', 'Trục dọc: năng lượng liên kết riêng (MeV/nuclôn). Đỉnh quanh Fe-56, Ni-62 (≈ 8,8); hạt nhân nặng bên phải kém bền hơn. (Halliday 42.2.3)')}</div></div>
${h3(4, 'Câu 8 và ví dụ 1 gam heli-4')}
${box(wl('Câu 8: D + T → He + n, khối lượng giảm 0,018883 u; năng lượng toả ra cho MỘT phản ứng = …', 2)
 + wl('1 g He-4 (N<sub>A</sub> = 6,02·10²³/mol; 1 MeV = 1,6·10⁻¹³ J) có N = … hạt; E = N·28,3 MeV = … J', 2)
 + wl('So với đốt than (2,9·10⁷ J/kg): … kg', 2))}
${foot(5)}</section>`;

// ----- Bài tập mẫu: 6 dạng (scripts/data/bai-tap-mau/16.json) -----
const dang = [
  { t: 'Dạng 1 · Dễ · Độ hụt khối từ khối lượng hạt nhân',
    de: `${m('{}^{14}_{7}\\mathrm{N}')}, ${m('m_X=13{,}999231\\ \\mathrm{u}')}:<br><b>a)</b> độ hụt khối<br><b>b)</b> năng lượng liên kết (MeV)`,
    nd: `Đề cho khối lượng <b>hạt nhân</b> → ${m('\\Delta m=Zm_p+(A-Z)m_n-')} ${f(8)}, rồi nhân ${f(10)}`, a: ['a', 'b'], gi: 0 },
  { t: 'Dạng 2 · Trung bình · So độ bền bằng năng lượng liên kết riêng',
    de: `${m('{}^{20}_{10}\\mathrm{Ne}')}, ${m('m_X=19{,}986950\\ \\mathrm{u}')}:<br><b>a)</b> ${m('E_{lkr}')}<br><b>b)</b> bền hơn hay kém bền hơn He-4 (7,07) và Fe-56 (8,79)?`,
    nd: `Hỏi độ bền → ${m('E_{lkr}=')} ${f(10)} / ${f(8)} rồi đặt cạnh hạt nhân đã biết`, a: ['a', 'b'], gi: 0 },
  { t: 'Dạng 3 · Trung bình · Xếp hạng độ bền bốn hạt nhân',
    de: `Bảng ${m('A,\\ E_{lk}')} (MeV): Be 9 · 58,16; Ne 20 · 160,64; Sr 90 · 782,63; Pb 208 · 1636,43.<br><b>a)</b> ${m('E_{lkr}')} từng hạt nhân<br><b>b)</b> xếp theo độ bền tăng dần`,
    nd: `Nhiều hạt nhân khác số khối → chia ${m('E_{lk}')} cho ${f(8)} từng hạt rồi xếp`, a: ['a', 'b'], gi: 5, fig: 'cotLkr' },
  { t: 'Dạng 4 · Khó · Khối lượng nguyên tử → độ hụt khối',
    de: `${m('{}^{40}_{20}\\mathrm{Ca}')}, ${m('m_{nt}=39{,}962591\\ \\mathrm{u}')}, ${m('m_e=0{,}000549\\ \\mathrm{u}')}:<br><b>a)</b> độ hụt khối<br><b>b)</b> ${m('E_{lk}')} và ${m('E_{lkr}')}`,
    nd: `Đề ghi khối lượng <b>nguyên tử</b> → cộng ${m('Z\\,m_e=')} ${f(10)} vào tổng hạt rời trước khi trừ`, a: ['a', 'b'], gi: 3 },
  { t: 'Dạng 5 · Khó · Đi ngược từ E<sub>lkr</sub> tìm khối lượng hạt nhân',
    de: `${m('{}^{84}_{36}\\mathrm{Kr}')}, ${m('E_{lkr}=8{,}72\\ \\mathrm{MeV}')}/nuclôn:<br><b>a)</b> độ hụt khối<br><b>b)</b> khối lượng hạt nhân`,
    nd: `Cho ${m('E_{lkr}')}, hỏi khối lượng → ${m('E_{lk}=')} ${f(8)}·${m('A')}, chia ${f(10)}, lấy tổng nuclôn rời trừ ${f(8)}`, a: ['a', 'b'], gi: 4, fig: 'hutKhoiKr' },
  { t: 'Dạng 6 · Nâng cao · Năng lượng tạo thành cả mẫu',
    de: `${m('{}^{12}_{6}\\mathrm{C}')}, ${m('\\Delta m=0{,}098940\\ \\mathrm{u}')}; mẫu ${m('3{,}0\\ \\mathrm{g}')}, ${m('M=12\\ \\mathrm{g/mol}')}; ${nw(m('N_A=6{,}02\\cdot10^{23}\\ \\mathrm{mol^{-1}}'))}; ${nw(m('1\\ \\mathrm{MeV}=1{,}6\\cdot10^{-13}\\ \\mathrm{J}'))}:<br><b>a)</b> năng lượng toả ra (J) khi tạo thành từ nuclôn rời<br><b>b)</b> bằng đốt bao nhiêu kg than (${m('2{,}9\\cdot10^{7}\\ \\mathrm{J/kg}')})?`,
    nd: `Cho khối lượng chất, hỏi năng lượng → ${m('N=')} ${f(8)} ${m('\\cdot N_A')}, nhân năng lượng ${f(10)}`, a: ['a', 'b'], gi: 3 },
];

// Bài tương tự (thầy chốt 10/11): bài về nhà, giải vào vở; mỗi dạng 2 bài; ô đáp số theo nhãn ý; đáp số in lật ngược.
// Khối lượng hạt nhân = khối lượng nguyên tử (AME2020) − Z·m_e, cùng bộ m_p, m_n, m_e, 931,5 như bài mẫu; đáp số tính bằng Python.
const oY = (s, o, w = 25) => s.split('<br>').map((p) => {
  const y = p.match(/^<b>([a-d])\)<\/b>/);
  if (!y) return `<div>${p}</div>`;
  const ls = o.filter((l) => l[0] === y[1]);
  return `<div class="yo"><span>${p}</span><span class="oo">${ls.map((l) => `<span class="nw"><b>${l})</b>${f(w)}</span>`).join('')}</span></div>`;
}).join('');
const ttDe = (b) => b.fig ? `<div class="fig-side" style="grid-template-columns:1fr ${b.fw}mm">${`<div>${oY(b.de, b.o, b.ow)}</div>`}${b.fig}</div>` : oY(b.de, b.o, b.ow);
const vaoVo = (ds) => ds.map((b) => (b.o ? { t: b.t, de: ttDe(b), k: 0 } : b));
const nhap = (n) => ({ t: '<span class="nhap-t">Nháp / chỗ em còn vướng</span>', de: lines(n), k: 0 });
const PN = `Cho ${nw(m('m_p=1{,}007276\\ \\mathrm u'))}, ${nw(m('m_n=1{,}008665\\ \\mathrm u'))}, ${nw(`${m('1\\ \\mathrm u=931{,}5\\ \\mathrm{MeV}/c^2')}.`)}`;
const PNE = `Cho ${nw(m('m_p=1{,}007276\\ \\mathrm u'))}, ${nw(m('m_n=1{,}008665\\ \\mathrm u'))}, ${nw(m('m_e=0{,}000549\\ \\mathrm u'))}, ${nw(`${m('1\\ \\mathrm u=931{,}5\\ \\mathrm{MeV}/c^2')}.`)}`;
const J6 = `${nw(m('1\\ \\mathrm u=931{,}5\\ \\mathrm{MeV}/c^2'))}, ${nw(m('1\\ \\mathrm{MeV}=1{,}6\\cdot10^{-13}\\ \\mathrm J'))}, ${nw(`${m('N_A=6{,}02\\cdot10^{23}\\ \\mathrm{mol^{-1}}')}.`)}`;
const tuongTu = {
  vo: true,
  tieuDe: ['DẠNG 1–3', 'DẠNG 4–6'],
  trang: [[
    { t: 'Dạng 1 · Bài 1', de: `Hạt nhân ${m('{}^{16}_{\\ 8}\\mathrm{O}')} có khối lượng hạt nhân ${nw(`${m('m_X=15{,}990523\\ \\mathrm u')}.`)} ${PN}<br><b>a)</b> độ hụt khối<br><b>b)</b> năng lượng liên kết (MeV)`, o: ['a', 'b'] },
    { t: 'Dạng 1 · Bài 2', de: `Hạt nhân ${m('{}^{7}_{3}\\mathrm{Li}')} có khối lượng hạt nhân ${nw(`${m('m_X=7{,}014356\\ \\mathrm u')}.`)} ${PN} ${nw(`${m('1\\ \\mathrm{MeV}=1{,}6\\cdot10^{-13}\\ \\mathrm J')}.`)}<br><b>a)</b> độ hụt khối<br><b>b)</b> năng lượng liên kết (MeV)<br><b>c)</b> năng lượng liên kết đó theo đơn vị jun`, o: ['a', 'b', 'c'], ow: 30 },
    { t: 'Dạng 2 · Bài 1', de: `Hạt nhân ${m('{}^{24}_{12}\\mathrm{Mg}')} có khối lượng hạt nhân ${nw(`${m('m_X=23{,}978454\\ \\mathrm u')}.`)} ${PN}<br><b>a)</b> năng lượng liên kết riêng<br><b>b)</b> bền hơn hay kém bền hơn He-4 (7,07) và Fe-56 (8,79 MeV/nuclôn)?`, o: ['a', 'b'], ow: 40 },
    { t: 'Dạng 2 · Bài 2', de: `Hạt nhân ${m('{}^{235}_{\\ 92}\\mathrm{U}')} có khối lượng hạt nhân ${nw(`${m('m_X=234{,}993422\\ \\mathrm u')}.`)} ${PN}<br><b>a)</b> năng lượng liên kết riêng<br><b>b)</b> bền hơn hay kém bền hơn Fe-56 (8,79 MeV/nuclôn)?`, o: ['a', 'b'], ow: 30 },
    { t: 'Dạng 3 · Bài 1', de: `Bảng ${m('A,\\ E_{lk}')} (MeV): He-3 · 3 · 7,72; Si-28 · 28 · 236,54; Ni-62 · 62 · 545,27; U-238 · 238 · 1801,71.<br><b>a)</b> ${m('E_{lkr}')} từng hạt nhân<br><b>b)</b> xếp theo độ bền tăng dần`, o: ['a', 'b'], ow: 45 },
    { t: 'Dạng 3 · Bài 2', de: `Bảng ${m('A,\\ E_{lk}')} (MeV): H-2 · 2 · 2,22; Na-23 · 23 · 186,57; Zr-90 · 90 · 783,91; Bi-209 · 209 · 1640,25.<br><b>a)</b> ${m('E_{lkr}')} từng hạt nhân<br><b>b)</b> xếp theo độ bền tăng dần`, o: ['a', 'b'], ow: 45 },
    nhap(1),
  ], [
    { t: 'Dạng 4 · Bài 1', de: `Nguyên tử ${m('{}^{56}_{26}\\mathrm{Fe}')} có khối lượng nguyên tử ${nw(`${m('m_{nt}=55{,}934936\\ \\mathrm u')}.`)} ${PNE}<br><b>a)</b> độ hụt khối của hạt nhân<br><b>b)</b> ${m('E_{lk}')} và ${m('E_{lkr}')}`, o: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>'] },
    { t: 'Dạng 4 · Bài 2', de: `Nguyên tử ${m('{}^{27}_{13}\\mathrm{Al}')} có khối lượng nguyên tử ${nw(`${m('m_{nt}=26{,}981538\\ \\mathrm u')}.`)} ${PNE}<br><b>a)</b> độ hụt khối của hạt nhân<br><b>b)</b> ${m('E_{lk}')} và ${m('E_{lkr}')}`, o: ['a', 'b<sub>1</sub>', 'b<sub>2</sub>'] },
    { t: 'Dạng 5 · Bài 1', de: `Hạt nhân ${m('{}^{32}_{16}\\mathrm{S}')} có ${nw(`${m('E_{lkr}=8{,}49\\ \\mathrm{MeV}')}/nuclôn.`)} ${PN}<br><b>a)</b> độ hụt khối<br><b>b)</b> khối lượng hạt nhân (u)`, o: ['a', 'b'], ow: 30 },
    { t: 'Dạng 5 · Bài 2', de: `Hạt nhân ${m('{}^{107}_{\\ 47}\\mathrm{Ag}')} có ${nw(`${m('E_{lkr}=8{,}55\\ \\mathrm{MeV}')}/nuclôn.`)} ${PN}<br><b>a)</b> độ hụt khối<br><b>b)</b> khối lượng hạt nhân (u)`, o: ['a', 'b'], ow: 30 },
    { t: 'Dạng 6 · Bài 1', de: `Hạt nhân ${m('{}^{20}_{10}\\mathrm{Ne}')} có ${nw(`${m('\\Delta m=0{,}172460\\ \\mathrm u')};`)} mẫu ${nw(`${m('4{,}0\\ \\mathrm g')},`)} ${nw(`${m('M=20\\ \\mathrm{g/mol}')}.`)} Lấy ${J6}<br><b>a)</b> năng lượng toả ra (J) khi tạo thành mẫu từ nuclôn rời<br><b>b)</b> bằng đốt bao nhiêu kg than (${nw(`${m('2{,}9\\cdot10^{7}\\ \\mathrm{J/kg}')})?`)}`, o: ['a', 'b'], ow: 30 },
    { t: 'Dạng 6 · Bài 2', de: `Hạt nhân ${m('{}^{9}_{4}\\mathrm{Be}')} có ${nw(`${m('\\Delta m=0{,}062442\\ \\mathrm u')};`)} mẫu ${nw(`${m('1{,}8\\ \\mathrm g')},`)} ${nw(`${m('M=9\\ \\mathrm{g/mol}')}.`)} Lấy ${J6}<br><b>a)</b> năng lượng toả ra (J) khi tạo thành mẫu từ nuclôn rời<br><b>b)</b> đủ cho đèn ${m('100\\ \\mathrm W')} sáng liên tục bao nhiêu năm (1 năm = 365 ngày)?`, o: ['a', 'b'], ow: 30 },
  ]],
  dap: [
    `D1·1: a) 0,1370 u · b) 127,6 MeV &nbsp;|&nbsp; D1·2: a) 0,0421 u · b) 39,2 MeV · ${nw('c) 6,28·10<sup>−12</sup> J')} &nbsp;|&nbsp; D2·1: a) 8,26 MeV/nuclôn · b) bền hơn He-4, kém Fe-56 &nbsp;|&nbsp; D2·2: a) 7,59 MeV/nuclôn · b) kém bền hơn Fe-56 &nbsp;|&nbsp; D3·1: a) 2,57 · 8,45 · 8,79 · 7,57 · b) He-3 &lt; U-238 &lt; Si-28 &lt; Ni-62 &nbsp;|&nbsp; D3·2: a) 1,11 · 8,11 · 8,71 · 7,85 · b) H-2 &lt; Bi-209 &lt; Na-23 &lt; Zr-90`,
    `D4·1: a) 0,5285 u · b<sub>1</sub>) 492,3 MeV · b<sub>2</sub>) 8,79 MeV/nuclôn &nbsp;|&nbsp; D4·2: a) 0,2415 u · b<sub>1</sub>) 225,0 MeV · b<sub>2</sub>) 8,33 MeV/nuclôn &nbsp;|&nbsp; D5·1: a) 0,2917 u · b) 31,9634 u &nbsp;|&nbsp; D5·2: a) 0,9821 u · b) 106,8797 u &nbsp;|&nbsp; D6·1: ${nw('a) 3,09·10<sup>12</sup> J')} · ${nw('b) 1,07·10<sup>5</sup> kg')} &nbsp;|&nbsp; D6·2: ${nw('a) 1,12·10<sup>12</sup> J')} · b) 355 năm`,
  ],
};

await K.dung({
  trang1to5: [p1, p2, p3, p4, p5].join('\n'),
  btm: { dang, tach: [3, 3], kq: [[1, 2, 3], [4, 5, 6]], khoNhat: false },
  tuongTu: { ...tuongTu, trang: tuongTu.trang.map(vaoVo) },
  tra: 'lực hạt nhân 1·4 · khối lượng, u 1·5 · Einstein 2·1 · Δm, E<sub>lk</sub>, E<sub>lkr</sub> 2·2 · bốn hạt nhân 2·3 · đường cong 2·4 · bẫy 3·2 · dạng 1–3 → 6·1 · dạng 4–6 → 7·1',
  out: process.argv[2],
});
