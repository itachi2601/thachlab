// Hai trang "Bài tập mẫu" của ruột tập bài 14 (5 dạng ở scripts/data/bai-tap-mau/15.json, mục Bài tập mẫu trên web).
// Dạng bán cấu trúc, gợi ý mờ dần theo độ khó (N6, Sweller & Cooper 1985; Kalyuga 2003): đề đầy đủ + bước gợi ý nằm trên web;
// trên giấy: tóm tắt đề, mấu chốt nhận dạng (điền khuyết), ô đáp số, tick tự làm/cần gợi ý cho MỌI dạng; ô giải 9 dòng chỉ từ dạng 3
// (không có bảng phân tích đề riêng — thầy chốt 25/10: phân tích ngay trong ô giải khi học); kết quả 3 bài tương tự ghi ở cuối mỗi trang.
// Trang A = dạng 1–3 + chỗ hỏi, trang B = dạng 4–5. Dạng 1–2 giải nhẩm/nháp, chỉ ghi đáp số.
// Dùng trong bai14.mjs: `${btmCss}` trong <style>, `${btmPages(nA, { m, head, foot, tag, lines, wl })}` (trang nA và nA+1).
export const btmCss = `
.bt{background:#fff;border:.3mm solid var(--navy);border-radius:1.5mm;padding:1mm 2.5mm 1.2mm;margin-bottom:1.6mm}
.bt .hd{display:flex;justify-content:space-between;align-items:center;gap:2mm;font-weight:700;color:var(--navy);font-size:3.4mm}
.bt .hd span:last-child{font-weight:400;color:var(--ink);font-size:2.9mm;white-space:nowrap}
.bt .de{font-size:3.05mm;line-height:1.4;margin:.4mm 0 .6mm}
.bt .nd{font-size:3.1mm;background:var(--soft);border-radius:1mm;padding:.4mm 1.5mm;margin-bottom:.8mm}
.bt .ans{display:grid;grid-template-columns:repeat(4,1fr);gap:1mm 2.5mm;font-size:3.1mm}
.bt .ans.c3{grid-template-columns:repeat(3,1fr)}
.bt .ans div{display:flex;gap:1mm;align-items:flex-end}.bt .ans .fill{flex:1;min-width:0;height:9mm}
.bt .gi{border:.3mm solid var(--grid);border-radius:1mm;padding:0 2mm;margin-bottom:.8mm}
`;

const f = (w) => `<span class="fill" style="min-width:${w}mm"></span>`;
const ans = (labels) =>
  `<div class="ans${labels.length === 3 ? ' c3' : ''}">${labels.map((l) => `<div><b>${l})</b>${f(10)}</div>`).join('')}</div>`;
const tu = '<span><span class="ck"></span>tự làm &nbsp;<span class="ck"></span>cần gợi ý</span>';

export const btmPages = (n, { m, head, foot, tag, lines, wl }) => {
  const dang = [
    {
      t: 'Dạng 1 · Dễ · Đọc kí hiệu hạt nhân',
      de: `${m('{}^{63}_{29}\\mathrm{Cu}')}: <b>a)</b> số prôtôn, nuclôn · <b>b)</b> số nơtron · <b>c)</b> số êlectron, điện tích hạt nhân (theo ${m('e')}) · <b>d)</b> hạt nhân có 82 prôtôn, 124 nơtron: số khối, kí hiệu.`,
      nd: `Thấy kí hiệu ${m('{}^{A}_{Z}\\mathrm{X}')} → đọc ${m('Z')} ở ${f(10)}, ${m('A')} ở ${f(10)}, dùng ${f(22)}`,
      a: ['a', 'b', 'c', 'd'], gi: 0,
    },
    {
      t: 'Dạng 2 · Trung bình · Nhận ra đồng vị',
      de: `${m('{}^{12}_{6}\\mathrm{C},\\ {}^{14}_{6}\\mathrm{C},\\ {}^{14}_{7}\\mathrm{N},\\ {}^{15}_{7}\\mathrm{N},\\ {}^{16}_{8}\\mathrm{O},\\ {}^{17}_{8}\\mathrm{O}')}: <b>a)</b> số nơtron từng hạt · <b>b)</b> bao nhiêu cặp đồng vị · <b>c)</b> ${m('{}^{14}_{6}\\mathrm{C}')} và ${m('{}^{14}_{7}\\mathrm{N}')} có phải đồng vị?`,
      nd: `Hỏi “có phải đồng vị” → so ${f(8)} trước (phải ${f(12)}), rồi xét ${f(8)} khác nhau`,
      a: ['a', 'b', 'c'], gi: 0,
    },
    {
      t: 'Dạng 3 · Trung bình · Bán kính, thể tích theo số khối',
      de: `${m('{}^{64}_{30}\\mathrm{Zn}')} và ${m('{}^{238}_{92}\\mathrm{U}')}, ${m('R=1{,}2\\cdot10^{-15}A^{1/3}')}: <b>a)</b> ${m('R_{\\mathrm{Zn}}')} · <b>b)</b> ${m('R_{\\mathrm{U}}')} (đơn vị ${m('10^{-15}\\ \\mathrm{m}')}) · <b>c)</b> ${m('R_{\\mathrm{U}}/R_{\\mathrm{Zn}}')} · <b>d)</b> ${m('V_{\\mathrm{U}}/V_{\\mathrm{Zn}}')}`,
      nd: `Hỏi bán kính, tỉ số bán kính hay thể tích → ${m('R\\propto')} ${f(12)}, ${m('V\\propto R^3\\propto')} ${f(10)}`,
      a: ['a', 'b', 'c', 'd'], gi: 9,
    },
    {
      t: 'Dạng 4 · Khó · Đếm hạt trong một khối lượng chất',
      de: `${m('14\\ \\mathrm{g}')} sắt ${m('{}^{56}_{26}\\mathrm{Fe}')}, ${m('M\\approx56\\ \\mathrm{g/mol}')}: <b>a)</b> số mol · <b>b)</b> số hạt nhân · <b>c)</b> số nơtron · <b>d)</b> tổng điện tích các prôtôn (C).`,
      nd: `Cho khối lượng, hỏi số hạt → ${m('n=')} ${f(10)}, ${m('N=')} ${f(10)}, × số ${f(10)} mỗi hạt nhân`,
      a: ['a', 'b', 'c', 'd'], gi: 9,
    },
    {
      t: 'Dạng 5 · Nâng cao · Khối lượng nguyên tử trung bình',
      de: `Bo: ${m('{}^{10}_{5}\\mathrm{B}')} (${m('10{,}013\\ \\mathrm{u}')}), ${m('{}^{11}_{5}\\mathrm{B}')} (${m('11{,}009\\ \\mathrm{u}')}), trung bình ${m('10{,}811\\ \\mathrm{u}')}: <b>a)</b> % mỗi đồng vị · <b>b)</b> khối lượng một nguyên tử ${m('{}^{11}_{5}\\mathrm{B}')} ra kg · <b>c)</b> ra ${m('\\mathrm{MeV}/c^2')}.`,
      nd: `Cho khối lượng từng đồng vị và trung bình → ${f(20)}, ${m('x_1+x_2=')} ${f(6)}`,
      a: ['a', 'b', 'c'], gi: 9,
    },
  ];
  // Ô giải (phân tích đề + giải trong cùng ô): chỉ với dạng có gi > 0
  const gi = (k) => k ? `<div class="gi">${wl('Phân tích và giải:', k)}</div>` : '';
  const kq = (ds) => `<div class="card soft" style="padding:1.2mm 3mm"><b>Ba bài tương tự:</b> đúng ${ds.map((i) => `D${i} ……/3`).join(' · ')}</div>`;
  const block = (d) => `<div class="bt"><div class="hd"><span>${d.t}</span>${tu}</div><div class="de">${d.de}</div><div class="nd"><b>Mấu chốt:</b> ${d.nd}</div>${gi(d.gi)}${ans(d.a)}</div>`;
  return `<section class="page">
${head('BÀI TẬP MẪU · DẠNG 1–3', 'Đề đủ và gợi ý từng bước ở mục Bài tập mẫu trên web')}
<h3><i>1</i>Nhận dạng và đáp số</h3>${tag(`${n}·1`)}
${dang.slice(0, 3).map(block).join('\n')}
${kq([1, 2, 3])}
<h3><i>2</i>Dạng 1–3: chỗ em còn vướng, câu hỏi cho thầy / trợ giảng</h3>
<div class="card" style="padding:0 3mm">${lines(4)}</div>
${foot(n)}</section>
<section class="page">
${head('BÀI TẬP MẪU · DẠNG 4–5', 'Đề đủ và gợi ý từng bước ở mục Bài tập mẫu trên web')}
<h3><i>1</i>Giải</h3>${tag(`${n + 1}·1`)}
${dang.slice(3).map(block).join('\n')}
${kq([4, 5])}
<div class="card soft" style="padding:1.2mm 3mm">Dạng em thấy khó nhất: D……, vì:${lines(1)}</div>
${foot(n + 1)}</section>`;
};
