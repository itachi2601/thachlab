// Hai trang "Bài tương tự" của ruột tập bài 14: mỗi dạng của Bài tập mẫu (bai14-btm.mjs) có 2 bài cùng dạng, làm ngay tại chỗ.
// Lí do (thầy chốt 10/11/2026): nhịp buổi 10′ ôn → 20′ kiểm tra → 30′ sửa bài → bài mới → BTVN; sau mỗi bài mẫu HS tự làm bài cùng dạng
// trên giấy (viết tay), còn trắc nghiệm/bài tập nhiều câu luyện trên web có đáp án ngay (Dunlosky 2013: luyện tập nhớ lại + phản hồi tức thì).
// Số liệu đã tính lại bằng Python (đáp số ở dải cuối trang, in nhỏ để HS đối chiếu sau khi làm xong, không nhìn trước).
// Dùng trong bai14.mjs: `${ttCss}` trong <style>, `${ttPages(nA, { m, head, foot, lines })}` (trang nA và nA+1).
export const ttCss = `
.tt{background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:1mm 2.5mm 0;margin-bottom:1.6mm}
.tt .hd{display:flex;justify-content:space-between;align-items:center;gap:2mm;font-weight:700;color:var(--navy);font-size:var(--fs-body)}
.tt .hd span:last-child{font-weight:400;color:var(--ink);font-size:var(--fs-sm);white-space:nowrap}
.tt .de{font-size:var(--fs-sm);line-height:1.4;margin:.3mm 0 .4mm}
.dap{font-size:var(--fs-sm);color:var(--hint);border-top:.3mm dashed var(--hint);padding-top:.8mm;margin-top:1.5mm;line-height:1.35;transform:rotate(180deg)}
`;

const ok = '<span><span class="ck"></span>đúng &nbsp;<span class="ck"></span>sai, đã sửa</span>';

export const ttPages = (n, { m, head, foot, lines }) => {
  const bai = (t, de, k) => `<div class="tt"><div class="hd"><span>${t}</span>${ok}</div><div class="de">${de}</div>${lines(k)}</div>`;
  const u = (s) => m(`${s}\\ \\mathrm{u}`);
  const p1 = [
    bai('Dạng 1 · Bài 1', `${m('{}^{40}_{20}\\mathrm{Ca}')}: <b>a)</b> số prôtôn, nơtron, êlectron của nguyên tử Ca trung hoà · <b>b)</b> hạt nhân có 92 prôtôn và 143 nơtron: số khối, kí hiệu.`, 2),
    bai('Dạng 1 · Bài 2', `${m('{}^{197}_{79}\\mathrm{Au}')}: <b>a)</b> ${m('Z')}, ${m('N')} · <b>b)</b> điện tích hạt nhân (theo ${m('e')}) · <b>c)</b> hạt nhân X có ${m('A=14')}, ${m('N=8')}: ${m('Z')} và kí hiệu.`, 3),
    bai('Dạng 2 · Bài 1', `${m('{}^{1}_{1}\\mathrm{H},\\ {}^{2}_{1}\\mathrm{H},\\ {}^{3}_{1}\\mathrm{H},\\ {}^{3}_{2}\\mathrm{He},\\ {}^{4}_{2}\\mathrm{He}')}: <b>a)</b> số nơtron từng hạt · <b>b)</b> bao nhiêu cặp đồng vị · <b>c)</b> ${m('{}^{3}_{1}\\mathrm{H}')} và ${m('{}^{3}_{2}\\mathrm{He}')} có phải đồng vị?`, 3),
    bai('Dạng 2 · Bài 2', `${m('{}^{35}_{17}\\mathrm{Cl},\\ {}^{37}_{17}\\mathrm{Cl},\\ {}^{39}_{19}\\mathrm{K}')}: <b>a)</b> số nơtron từng hạt · <b>b)</b> cặp nào là đồng vị · <b>c)</b> cặp nào cùng số nơtron nhưng không phải đồng vị.`, 3),
    bai('Dạng 3 · Bài 1', `${m('R=1{,}2\\cdot10^{-15}A^{1/3}\\ \\mathrm{m}')}; ${m('{}^{8}_{4}\\mathrm{Be}')} và ${m('{}^{125}_{53}\\mathrm{I}')}: <b>a)</b> ${m('R_{\\mathrm{Be}}')} · <b>b)</b> ${m('R_{\\mathrm{I}}')} · <b>c)</b> ${m('R_{\\mathrm{I}}/R_{\\mathrm{Be}}')} · <b>d)</b> ${m('V_{\\mathrm{I}}/V_{\\mathrm{Be}}')}.`, 5),
    bai('Dạng 3 · Bài 2', `Hạt nhân X có bán kính ${m('4{,}8\\cdot10^{-15}\\ \\mathrm{m}')}: <b>a)</b> số khối ${m('A')} · <b>b)</b> thể tích X gấp mấy lần thể tích ${m('{}^{4}_{2}\\mathrm{He}')}?`, 2),
  ].join('\n');
  const p2 = [
    bai('Dạng 4 · Bài 1', `${m('6{,}0\\ \\mathrm{g}')} cacbon ${m('{}^{12}_{6}\\mathrm{C}')}, ${m('M=12\\ \\mathrm{g/mol}')}, ${m('N_A=6{,}022\\cdot10^{23}\\ \\mathrm{mol}^{-1}')}, ${m('e=1{,}6\\cdot10^{-19}\\ \\mathrm{C}')}: <b>a)</b> số mol · <b>b)</b> số hạt nhân · <b>c)</b> số nơtron · <b>d)</b> tổng điện tích các prôtôn (C).`, 7),
    bai('Dạng 4 · Bài 2', `${m('2{,}7\\ \\mathrm{g}')} nhôm ${m('{}^{27}_{13}\\mathrm{Al}')}, ${m('M=27\\ \\mathrm{g/mol}')}, ${m('N_A=6{,}022\\cdot10^{23}\\ \\mathrm{mol}^{-1}')}: <b>a)</b> số mol · <b>b)</b> số hạt nhân · <b>c)</b> số nơtron.`, 5),
    bai('Dạng 5 · Bài 1', `Clo: ${m('{}^{35}\\mathrm{Cl}')} (${u('34{,}969')}), ${m('{}^{37}\\mathrm{Cl}')} (${u('36{,}966')}), trung bình ${u('35{,}453')}: <b>a)</b> % mỗi đồng vị · <b>b)</b> khối lượng một nguyên tử ${m('{}^{35}\\mathrm{Cl}')} ra kg (${m('1\\ \\mathrm{u}=1{,}6605\\cdot10^{-27}\\ \\mathrm{kg}')}).`, 5),
    bai('Dạng 5 · Bài 2', `Neon: ${m('{}^{20}\\mathrm{Ne}')} (${u('19{,}992')}), ${m('{}^{22}\\mathrm{Ne}')} (${u('21{,}991')}), trung bình ${u('20{,}180')}: <b>a)</b> % mỗi đồng vị · <b>b)</b> trong 500 nguyên tử Ne tự nhiên có khoảng bao nhiêu nguyên tử ${m('{}^{22}\\mathrm{Ne}')}?`, 5),
  ].join('\n');
  return `<section class="page">
${head('BÀI TƯƠNG TỰ · DẠNG 1–3', 'Làm tại chỗ, không nhìn trang Bài tập mẫu; xong mới tick và đối chiếu đáp số')}
${p1}
<div class="dap"><b>Đáp số (lật ngược trang để đọc, làm xong mới xem):</b> D1·1: a) 20; 20; 20 · b) 235, ${m('{}^{235}_{92}\\mathrm{U}')} &nbsp;|&nbsp; D1·2: a) 79; 118 · b) ${m('+79e')} · c) 6, ${m('{}^{14}_{6}\\mathrm{C}')} &nbsp;|&nbsp; D2·1: a) 0; 1; 2; 1; 2 · b) 4 · c) không &nbsp;|&nbsp; D2·2: a) 18; 20; 20 · b) Cl-35 và Cl-37 · c) Cl-37 và K-39 &nbsp;|&nbsp; D3·1: a) ${m('2{,}4\\cdot10^{-15}')} m · b) ${m('6{,}0\\cdot10^{-15}')} m · c) 2,5 · d) 15,6 &nbsp;|&nbsp; D3·2: a) 64 · b) 16 lần</div>
${foot(n)}</section>
<section class="page">
${head('BÀI TƯƠNG TỰ · DẠNG 4–5', 'Chỗ trống còn lại dùng làm nháp')}
${p2}
<div class="dap"><b>Đáp số (lật ngược trang để đọc, làm xong mới xem):</b> D4·1: a) 0,5 mol · b) ${m('3{,}01\\cdot10^{23}')} · c) ${m('1{,}81\\cdot10^{24}')} · d) ${m('2{,}89\\cdot10^{5}')} C &nbsp;|&nbsp; D4·2: a) 0,1 mol · b) ${m('6{,}02\\cdot10^{22}')} · c) ${m('8{,}43\\cdot10^{23}')} &nbsp;|&nbsp; D5·1: a) 75,8% Cl-35; 24,2% Cl-37 · b) ${m('5{,}81\\cdot10^{-26}')} kg &nbsp;|&nbsp; D5·2: a) 90,6% Ne-20; 9,4% Ne-22 · b) khoảng 47</div>
${foot(n + 1)}</section>`;
};
