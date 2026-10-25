// Trang "Bài tập mẫu" của ruột tập bài 14 (5 dạng ở scripts/data/bai-tap-mau/15.json, mục Bài tập mẫu trên web).
// Đề đầy đủ + bước gợi ý nằm trên web; trên giấy chỉ ghi: tóm tắt đề, quy tắc nhận dạng (điền khuyết), đáp số từng ý,
// tự làm hay cần gợi ý (theo dõi fading), rồi kết quả 3 bài tương tự web tự đưa ra. Giải đầy đủ ra giấy nháp.
// Dùng trong bai14.mjs: `${btmCss}` trong <style>, `${btmPage(n, { m, head, foot, tag, lines })}` sau trang Bài toán mẫu.
export const btmCss = `
.bt{background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:1mm 2.5mm 1.2mm;margin-bottom:1.6mm}
.bt .hd{display:flex;justify-content:space-between;align-items:center;gap:2mm;font-weight:700;color:var(--navy);font-size:3.4mm}
.bt .hd span:last-child{font-weight:400;color:var(--ink);font-size:2.9mm;white-space:nowrap}
.bt .de{font-size:3.05mm;line-height:1.4;margin:.4mm 0 .6mm}
.bt .nd{font-size:3.1mm;background:var(--soft);border-radius:1mm;padding:.4mm 1.5mm;margin-bottom:.8mm}
.bt .ans{display:grid;grid-template-columns:repeat(4,1fr);gap:1mm 2.5mm;font-size:3.1mm}
.bt .ans.c3{grid-template-columns:repeat(3,1fr)}
.bt .ans div{display:flex;gap:1mm;align-items:flex-end}.bt .ans .fill{flex:1;min-width:0}
`;

const f = (w) => `<span class="fill" style="min-width:${w}mm"></span>`;
const ans = (labels) =>
  `<div class="ans${labels.length === 3 ? ' c3' : ''}">${labels.map((l) => `<div><b>${l})</b>${f(10)}</div>`).join('')}</div>`;
const tu = '<span><span class="ck"></span>tự làm &nbsp;<span class="ck"></span>cần gợi ý</span>';

export const btmPage = (n, { m, head, foot, tag, lines }) => {
  const dang = [
    {
      t: 'Dạng 1 · Dễ · Đọc kí hiệu hạt nhân',
      de: `${m('{}^{63}_{29}\\mathrm{Cu}')}: <b>a)</b> số prôtôn, nuclôn · <b>b)</b> số nơtron · <b>c)</b> số êlectron, điện tích hạt nhân (theo ${m('e')}) · <b>d)</b> hạt nhân có 82 prôtôn, 124 nơtron: số khối, kí hiệu.`,
      nd: `Thấy kí hiệu ${m('{}^{A}_{Z}\\mathrm{X}')} → đọc ${m('Z')} ở ${f(10)}, ${m('A')} ở ${f(10)}, dùng ${f(22)}`,
      a: ['a', 'b', 'c', 'd'],
    },
    {
      t: 'Dạng 2 · Trung bình · Nhận ra đồng vị',
      de: `${m('{}^{12}_{6}\\mathrm{C},\\ {}^{14}_{6}\\mathrm{C},\\ {}^{14}_{7}\\mathrm{N},\\ {}^{15}_{7}\\mathrm{N},\\ {}^{16}_{8}\\mathrm{O},\\ {}^{17}_{8}\\mathrm{O}')}: <b>a)</b> số nơtron từng hạt · <b>b)</b> bao nhiêu cặp đồng vị · <b>c)</b> ${m('{}^{14}_{6}\\mathrm{C}')} và ${m('{}^{14}_{7}\\mathrm{N}')} có phải đồng vị?`,
      nd: `Hỏi “có phải đồng vị” → so ${f(8)} trước (phải ${f(12)}), rồi xét ${f(8)} khác nhau`,
      a: ['a', 'b', 'c'],
    },
    {
      t: 'Dạng 3 · Trung bình · Bán kính, thể tích theo số khối',
      de: `${m('{}^{64}_{30}\\mathrm{Zn}')} và ${m('{}^{238}_{92}\\mathrm{U}')}, ${m('R=1{,}2\\cdot10^{-15}A^{1/3}')}: <b>a)</b> ${m('R_{\\mathrm{Zn}}')} · <b>b)</b> ${m('R_{\\mathrm{U}}')} (đơn vị ${m('10^{-15}')} m) · <b>c)</b> ${m('R_{\\mathrm{U}}/R_{\\mathrm{Zn}}')} · <b>d)</b> ${m('V_{\\mathrm{U}}/V_{\\mathrm{Zn}}')}`,
      nd: `Hỏi bán kính, tỉ số bán kính hay thể tích → ${m('R\\propto')} ${f(12)}, ${m('V\\propto R^3\\propto')} ${f(10)}`,
      a: ['a', 'b', 'c', 'd'],
    },
    {
      t: 'Dạng 4 · Khó · Đếm hạt trong một khối lượng chất',
      de: `${m('14')} g sắt ${m('{}^{56}_{26}\\mathrm{Fe}')}, ${m('M\\approx56')} g/mol: <b>a)</b> số mol · <b>b)</b> số hạt nhân · <b>c)</b> số nơtron · <b>d)</b> tổng điện tích các prôtôn (C).`,
      nd: `Cho khối lượng, hỏi số hạt → ${m('n=')} ${f(10)}, ${m('N=')} ${f(10)}, × số ${f(10)} mỗi hạt nhân`,
      a: ['a', 'b', 'c', 'd'],
    },
    {
      t: 'Dạng 5 · Nâng cao · Khối lượng nguyên tử trung bình',
      de: `Bo: ${m('{}^{10}_{5}\\mathrm{B}')} (${m('10{,}013')} u), ${m('{}^{11}_{5}\\mathrm{B}')} (${m('11{,}009')} u), trung bình ${m('10{,}811')} u: <b>a)</b> % mỗi đồng vị · <b>b)</b> khối lượng một nguyên tử ${m('{}^{11}_{5}\\mathrm{B}')} ra kg · <b>c)</b> ra ${m('\\mathrm{MeV}/c^2')}.`,
      nd: `Cho khối lượng từng đồng vị và trung bình → ${f(24)}, ${m('x_1+x_2=')} ${f(6)}`,
      a: ['a', 'b', 'c'],
    },
  ];
  return `<section class="page">
${head('BÀI TẬP MẪU · 5 DẠNG', 'Đề đủ + gợi ý từng bước: mục Bài tập mẫu trên web; giải ra nháp')}
<h3><i>1</i>Nhận dạng và đáp số <span class="hint">(làm xong mới bấm xem lời giải)</span></h3>${tag(`${n}·1`)}
${dang.map((d) => `<div class="bt"><div class="hd"><span>${d.t}</span>${tu}</div><div class="de">${d.de}</div><div class="nd">🔑 ${d.nd}</div>${ans(d.a)}</div>`).join('\n')}
<h3><i>2</i>Ba bài tương tự web đưa ra <span class="hint">(sau khi đọc xong một dạng)</span></h3>${tag(`${n}·2`)}
<div class="card soft" style="padding:1.2mm 3mm">Đúng: ${[1, 2, 3, 4, 5].map((i) => `D${i} ……/3`).join(' &nbsp;· ')}<br>Dạng em thấy khó nhất: D……, vì:${lines(2)}</div>
${foot(n)}</section>`;
};
