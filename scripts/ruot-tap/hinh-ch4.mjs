// Hình minh hoạ cho ruột tập Bài 15–18 (VL12 Chương 4). Cùng quy tắc với hinh.mjs: mỗi hình trả lời MỘT câu hỏi, chữ ≥ 18 đơn vị
// viewBox (≈ 3 mm khi in rộng 46 mm), nét ≥ 2,8, phân biệt bằng NÉT/HÌNH (đặc – đứt) chứ không chỉ bằng màu (in đen–trắng), tự vẽ.
// Kiểm bằng `node scripts/ruot-tap/xem-hinh.mjs` (chụp từng hình ở cỡ in thật vào out/hinh/).
import { ve } from './hinh.mjs';
const { t, nuc, p, n, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const arr = (x1, y1, x2, y2, id, c = INK, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${SW}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const rect = (x, y, w, h, o = '') => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="4" fill="#fff" stroke="${INK}" stroke-width="${SW}" ${o}/>`;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
const sb = (s) => `<tspan font-size="14" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`; // chỉ số dưới trong SVG
const tri = (x, y, c = INK) => `<path d="M${x} ${y - 7} L${x + 11} ${y} L${x} ${y + 7} z" fill="${c}"/>`; // mũi tên nhỏ cho khe hẹp

// Hai thanh so sánh khối lượng: thanh trên dài hơn thanh dưới, phần chênh nét đứt ghi nhãn (độ hụt khối, năng lượng toả…)
const haiThanh = (l1, l2, gap, cap, id) => {
  let b = rect(8, 14, 288, 36) + T(18, 39, l1);
  b += rect(8, 70, 236, 36) + T(18, 95, l2);
  b += `<rect x="244" y="70" width="52" height="36" rx="4" fill="none" stroke="${RED}" stroke-width="${SW}" stroke-dasharray="6 4"/>`;
  b += `<line x1="244" y1="50" x2="244" y2="70" stroke="${GREY}" stroke-width="2" stroke-dasharray="3 3"/><line x1="296" y1="50" x2="296" y2="70" stroke="${GREY}" stroke-width="2" stroke-dasharray="3 3"/>`;
  b += T(270, 134, gap, { a: 'middle', c: RED, w: 700 });
  return wrap('0 0 304 144', b, cap, 'Hai thanh khối lượng: phần chênh là độ giảm khối lượng');
};

// Đường cong phân rã mũ qua các điểm 1, 1/2, 1/4, 1/8 (mốc thời gian nhãn xl); dấu ? cho HS điền
const phanRa = (xl, cap, id, ylab = 'N₀') => {
  const X = (k) => 52 + k * 78, Y = (v) => 150 - 118 * v;
  let b = `<line x1="40" y1="150" x2="306" y2="150" stroke="${INK}" stroke-width="${SW}"/><line x1="40" y1="150" x2="40" y2="20" stroke="${INK}" stroke-width="${SW}"/>`;
  let d = '';
  for (let i = 0; i <= 30; i++) { const k = i / 10; d += `${i ? 'L' : 'M'}${X(k).toFixed(1)},${Y(2 ** -k).toFixed(1)}`; }
  b += `<path d="${d}" fill="none" stroke="${RED}" stroke-width="${SW}"/>`;
  [0, 1, 2, 3].forEach((k) => {
    const x = X(k), y = Y(2 ** -k);
    b += `<line x1="${x}" y1="${y}" x2="${x}" y2="150" stroke="${GREY}" stroke-width="2" stroke-dasharray="4 4"/>`;
    if (k) b += `<line x1="40" y1="${y}" x2="${x}" y2="${y}" stroke="${GREY}" stroke-width="2" stroke-dasharray="4 4"/>`;
    b += `<circle cx="${x}" cy="${y}" r="5" fill="${INK}"/>` + T(x, 174, xl[k], { a: 'middle' });
    b += k ? T(x + 10, y - 8, '?', { c: RED, w: 700 }) : T(36, y + 7, ylab, { size: 20, a: 'end' });
  });
  return wrap('0 0 320 184', b, cap, 'Đồ thị số hạt nhân còn lại theo thời gian');
};

const luoi = (x, y, s, c) => { // ô vuông chia lưới c×c
  const w = s / c; let g = `<rect x="${x}" y="${y}" width="${s}" height="${s}" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
  for (let i = 1; i < c; i++) g += `<line x1="${x + i * w}" y1="${y}" x2="${x + i * w}" y2="${y + s}" stroke="${GREY}" stroke-width="1.6"/><line x1="${x}" y1="${y + i * w}" x2="${x + s}" y2="${y + i * w}" stroke="${GREY}" stroke-width="1.6"/>`;
  return g;
};

// Nhóm nơtron r=5 xếp lưới 4 cột
const nhom = (x, y, k) => Array.from({ length: k }, (_, i) =>
  `<circle cx="${x + (i % 4) * 14}" cy="${y + Math.floor(i / 4) * 14}" r="5.2" fill="#fff" stroke="${BLUE}" stroke-width="2.4"/>`).join('');

export const hinhCh4 = {
  // ===== Bài 15 · Năng lượng liên kết =====
  // Trang 1 · hai prôtôn: đẩy tĩnh điện (đặc, ra ngoài) – lực hạt nhân (đứt, vào trong)
  lucHatNhan: (cap = 'Hai prôtôn cách ~10⁻¹⁵ m: lực đẩy tĩnh điện (nét đặc) bị lực hạt nhân (nét đứt) thắng.') => {
    let b = defs('lh1') + defs('lh2');
    b += p(92, 56, 24) + p(208, 56, 24);
    b += arr(66, 56, 12, 56, 'lh1', RED) + arr(234, 56, 288, 56, 'lh1', RED);
    b += arr(120, 40, 142, 40, 'lh2', BLUE, '6 4') + arr(180, 40, 158, 40, 'lh2', BLUE, '6 4');
    b += T(150, 104, 'lực hạt nhân', { a: 'middle', c: BLUE }) + T(150, 126, 'hút vào', { a: 'middle', c: BLUE });
    b += T(40, 104, 'đẩy ra', { a: 'middle', c: RED }) + T(260, 104, 'đẩy ra', { a: 'middle', c: RED });
    return wrap('0 0 300 136', b, cap, 'Lực đẩy tĩnh điện và lực hạt nhân giữa hai prôtôn');
  },
  // Trang 2 · độ hụt khối: nguyên tử He-4 nhẹ hơn tổng hạt rời
  doHutKhoi: (cap = 'Vẽ phóng đại: phần chênh chỉ 0,76 %. Nguyên tử nhẹ hơn tổng các hạt rời.') =>
    haiThanh('hạt rời: 4,032980 u', 'nguyên tử: 4,002603 u', 'Δm = ?', cap, 'dhk'),
  // Trang 3 · đường cong năng lượng liên kết riêng
  duongCongLkr: (cap = 'Đỉnh ở giữa (sắt-56). Hạt nhân nhẹ hợp lại và hạt nhân nặng vỡ ra đều tiến về phía đỉnh.') => {
    const X = (a) => 44 + a * 1.1, Y = (e) => 172 - e * 16;
    let b = defs('dc');
    b += `<line x1="44" y1="172" x2="306" y2="172" stroke="${INK}" stroke-width="${SW}"/><line x1="44" y1="172" x2="44" y2="20" stroke="${INK}" stroke-width="${SW}"/>`;
    b += T(306, 168, 'A', { a: 'end' }) + T(306, 16, `E${sb('lkr')} (MeV/nuclôn)`, { a: 'end', size: 18 });
    const pts = [[2, 1.11], [4, 7.07], [16, 7.98], [56, 8.79], [120, 8.5], [235, 7.59]];
    b += `<path d="M${pts.map(([a, e]) => `${X(a).toFixed(1)},${Y(e).toFixed(1)}`).join(' L')}" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
    for (const [a, e, lab, dx, dy, c] of [[4, 7.07, 'He-4', 12, 30, INK], [16, 7.98, 'O-16', 6, 28, INK], [56, 8.79, 'Fe-56', 4, -14, RED], [235, 7.59, 'U-235', -50, 30, INK]])
      b += `<circle cx="${X(a)}" cy="${Y(e)}" r="5" fill="${c}"/>` + T(X(a) + dx, Y(e) + dy, lab, { c, size: 18, w: c === RED ? 700 : 400 });
    [[0, '0'], [5, '5'], [8.8, '8,8']].forEach(([e, l]) => { b += `<line x1="38" y1="${Y(e)}" x2="44" y2="${Y(e)}" stroke="${INK}" stroke-width="2"/>` + T(34, Y(e) + 6, l, { a: 'end', size: 18 }); });
    [100, 200].forEach((a) => { b += `<line x1="${X(a)}" y1="172" x2="${X(a)}" y2="178" stroke="${INK}" stroke-width="2"/>` + T(X(a), 196, String(a), { a: 'middle', size: 18 }); });
    b += arr(70, 140, 112, 140, 'dc', BLUE, '6 4') + arr(292, 140, 190, 140, 'dc', BLUE, '6 4');
    b += T(58, 162, 'hợp lại: toả', { size: 18, c: BLUE }) + T(296, 162, 'vỡ ra: toả', { size: 18, c: BLUE, a: 'end' });
    return wrap('0 0 320 204', b, cap, 'Năng lượng liên kết riêng theo số khối');
  },
  // Trang 4 · bậc thang năng lượng của heli-4
  bacThangNL: (cap = '') => {
    let b = defs('bt1') + defs('bt2');
    b += `<line x1="10" y1="34" x2="330" y2="34" stroke="${INK}" stroke-width="${SW}"/>` + T(12, 26, 'p, n rời', { size: 20 });
    b += `<line x1="10" y1="126" x2="330" y2="126" stroke="${INK}" stroke-width="${SW}"/>` + T(12, 152, 'He-4', { size: 20 });
    b += arr(40, 40, 40, 118, 'bt1', RED) + T(54, 86, 'tạo thành: toả', { size: 18, c: RED });
    b += arr(214, 120, 214, 42, 'bt2', BLUE, '6 4') + T(228, 76, 'tách ra:', { size: 18, c: BLUE }) + T(228, 98, 'cấp vào', { size: 18, c: BLUE });
    b += T(328, 152, `E${sb('lk')} = ?`, { a: 'end', size: 20, w: 700 });
    return wrap('0 0 340 162', b, cap, 'Bậc thang năng lượng của heli-4');
  },
  // Trang 5 · năng lượng hoá học và hạt nhân (thang logarit)
  soSanhNL: (cap = 'Thang logarit: mỗi vạch cách nhau 1000 lần. Cột nào dài hơn, và hơn nhau cỡ bao nhiêu lần?') => {
    let b = '';
    const bar = (y, w, c) => `<rect x="24" y="${y}" width="${w}" height="26" rx="4" fill="${c}" stroke="${INK}" stroke-width="${SW}"/>`;
    [[0, '1 eV'], [3, '1 keV'], [6, '1 MeV']].forEach(([d, l]) => {
      const x = 24 + d * 34;
      b += `<line x1="${x}" y1="104" x2="${x}" y2="112" stroke="${INK}" stroke-width="${SW}"/>` + T(x, 134, l, { a: 'middle', size: 18 });
    });
    b += `<line x1="24" y1="108" x2="290" y2="108" stroke="${INK}" stroke-width="${SW}"/>`;
    b += bar(14, 0.9 * 34, '#fff') + T(62, 34, 'đốt 1 phân tử: 8 eV', { size: 18 });
    b += bar(56, 7.45 * 34, GREY) + T(32, 76, 'He-4: 28,3 MeV', { size: 18, c: '#fff', w: 700 });
    return wrap('0 0 304 142', b, cap, 'So sánh năng lượng hoá học và năng lượng hạt nhân');
  },
  // Dạng 3 · cột năng lượng liên kết của bốn hạt nhân
  cotLkr: (cap = 'Cột cao tỉ lệ với E<sub>lk</sub>. Chì cao nhất — có phải bền nhất?') => {
    const data = [[9, 4, 'Be', 58.16], [20, 10, 'Ne', 160.64], [90, 38, 'Sr', 782.63], [208, 82, 'Pb', 1636.43]];
    let b = `<line x1="8" y1="160" x2="300" y2="160" stroke="${INK}" stroke-width="${SW}"/>`;
    data.forEach(([A, Z, X, e], i) => {
      const x = 22 + i * 72, h = e * 0.082 + 3;
      b += `<rect x="${x}" y="${160 - h}" width="48" height="${h}" fill="${GREY}" stroke="${INK}" stroke-width="${SW}"/>`;
      b += T(x + 24, 160 - h - 6, String(e).replace('.', ','), { a: 'middle', size: 18 });
      b += nuc(x + 6, 190, A, Z, X, 26);
    });
    return wrap('0 0 308 204', b, cap, 'Năng lượng liên kết của bốn hạt nhân');
  },
  // Dạng 5 · khối lượng hạt nhân so với tổng nuclôn rời
  hutKhoiKr: (cap = 'Biết E<sub>lkr</sub> thì tìm Δm rồi suy ra khối lượng hạt nhân: nhẹ hơn tổng nuclôn rời.') =>
    haiThanh(`nuclôn rời: Zm${sb('p')} + (A−Z)m${sb('n')}`, `hạt nhân Kr: m${sb('X')} = ?`, 'Δm = ?', cap, 'kr'),

  // ===== Bài 16 · Phân hạch, nhiệt hạch =====
  // Trang 1 · một nơtron làm vỡ U-235
  phanHach: (cap = 'Một nơtron chậm làm vỡ U-235 thành hai mảnh, thêm vài nơtron và tia γ.') => {
    let b = defs('ph');
    b += `<circle cx="22" cy="86" r="9" fill="#fff" stroke="${BLUE}" stroke-width="${SW}"/>` + arr(34, 86, 62, 86, 'ph', BLUE);
    b += `<circle cx="104" cy="86" r="38" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + nuc(80, 94, 235, 92, 'U', 28);
    b += arr(146, 72, 178, 46, 'ph') + arr(146, 100, 178, 126, 'ph');
    b += `<circle cx="206" cy="36" r="26" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + nuc(184, 42, 144, 56, 'Ba', 22);
    b += `<circle cx="206" cy="136" r="24" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + nuc(186, 142, 89, 36, 'Kr', 22);
    [64, 88, 112].forEach((y) => { b += `<circle cx="284" cy="${y}" r="8" fill="#fff" stroke="${BLUE}" stroke-width="${SW}"/>`; });
    b += arr(146, 88, 262, 88, 'ph', BLUE, '6 4') + T(284, 140, '3n', { c: BLUE, a: 'middle' });
    b += `<path d="M60 20 q8 -8 16 0 t16 0 t16 0" fill="none" stroke="${RED}" stroke-width="2.4"/>` + T(40, 28, 'γ', { c: RED, a: 'middle', size: 22, w: 700 });
    return wrap('0 0 310 170', b, cap, 'Phân hạch urani-235');
  },
  // Trang 2 · khối lượng nghỉ trước – sau
  canPhanUng: (cap = 'Khối lượng nghỉ sau phản ứng nhỏ hơn trước thì phần hụt thành năng lượng W.') =>
    haiThanh('trước: U + n', 'sau: Ba + Kr + 3n', 'W = ?', cap, 'cpu'),
  // Trang 3 · hệ số nhân k: ba thế hệ nơtron
  chuoiNotron: (cap = 'Ba thế hệ nơtron: số nơtron mỗi thế hệ so với thế hệ trước cho biết k.') => {
    let b = defs('cn');
    [[8, 4, 2, 'k < 1'], [4, 4, 4, 'k = 1'], [2, 4, 8, 'k > 1']].forEach(([a, c, d, lab], r) => {
      const y = 22 + r * 56;
      b += T(4, y + 12, lab, { w: 700 });
      [[92, a], [170, c], [248, d]].forEach(([x, k]) => { b += nhom(x, y, k); });
      b += `<line x1="146" y1="${y + 4}" x2="156" y2="${y + 4}" stroke="${INK}" stroke-width="${SW}"/>` + tri(156, y + 4) + `<line x1="224" y1="${y + 4}" x2="234" y2="${y + 4}" stroke="${INK}" stroke-width="${SW}"/>` + tri(234, y + 4);
    });
    return wrap('0 0 310 168', b, cap, 'Số nơtron qua ba thế hệ ứng với k nhỏ hơn, bằng và lớn hơn 1');
  },
  // Trang 3/4 · sơ đồ nhà máy điện hạt nhân
  loPhanUng: (cap = 'Thanh điều khiển hấp thụ nơtron: đẩy vào sâu thì k giảm.') => {
    let b = '';
    [['Lò'], ['Trao đổi', 'nhiệt'], ['Tua', 'bin'], ['Máy', 'phát']].forEach((l, i) => {
      const x = 2 + i * 82;
      b += rect(x, 60, 70, 52);
      l.length === 1 ? b += T(x + 35, 92, l[0], { a: 'middle', size: 18 }) : b += T(x + 35, 82, l[0], { a: 'middle', size: 18 }) + T(x + 35, 104, l[1], { a: 'middle', size: 18 });
      if (i < 3) b += `<line x1="${x + 70}" y1="86" x2="${x + 72}" y2="86" stroke="${INK}" stroke-width="${SW}"/>` + tri(x + 72, 86);
    });
    b += `<rect x="20" y="14" width="10" height="42" fill="${GREY}" stroke="${INK}" stroke-width="2.4"/><rect x="38" y="14" width="10" height="42" fill="${GREY}" stroke="${INK}" stroke-width="2.4"/>`;
    b += T(60, 40, 'thanh điều khiển', { size: 18 });
    b += T(326, 140, 'điện', { a: 'end', c: RED, w: 700, size: 20 });
    return wrap('0 0 330 148', b, cap, 'Sơ đồ nhà máy điện hạt nhân');
  },
  // Trang 3 · phản ứng nhiệt hạch D + T
  nhietHach: (cap = 'Hai hạt nhân nhẹ ghép lại thành He-4, bay ra một nơtron và toả 17,6 MeV.') => {
    let b = defs('nh');
    b += `<circle cx="34" cy="50" r="26" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + nuc(16, 56, 2, 1, 'H', 22);
    b += T(76, 58, '+', { size: 26, a: 'middle' });
    b += `<circle cx="118" cy="50" r="26" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + nuc(100, 56, 3, 1, 'H', 22);
    b += arr(152, 50, 178, 50, 'nh');
    b += `<circle cx="214" cy="50" r="30" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + nuc(194, 56, 4, 2, 'He', 24);
    b += T(252, 58, '+', { size: 26, a: 'middle' }) + `<circle cx="286" cy="50" r="10" fill="#fff" stroke="${BLUE}" stroke-width="${SW}"/>` + T(286, 92, 'n', { a: 'middle', c: BLUE });
    return wrap('0 0 312 100', b, cap, 'Phản ứng nhiệt hạch đơteri với triti');
  },
  // Dạng 1 · hệ số nhân từ ba thế hệ
  baTheHe: (cap = 'Mỗi thế hệ nhân với k. Cột vẽ đúng tỉ lệ (trục từ 0) nên trông gần bằng nhau.') => {
    let b = defs('btg') + `<line x1="8" y1="120" x2="300" y2="120" stroke="${INK}" stroke-width="${SW}"/>`;
    [50000, 50200, 50400].forEach((v, i) => {
      const x = 20 + i * 98;
      b += `<rect x="${x}" y="22" width="60" height="98" fill="${GREY}" stroke="${INK}" stroke-width="${SW}"/>` + T(x + 30, 100, String(v).replace(/(\d)(?=(\d{3})+$)/, '$1 '), { a: 'middle', size: 18, c: '#fff', w: 700 });
      if (i < 2) b += arr(x + 62, 60, x + 96, 60, 'btg', RED) + T(x + 79, 50, '× k', { a: 'middle', c: RED, w: 700, size: 18 });
    });
    return wrap('0 0 310 130', b, cap, 'Số nơtron của ba thế hệ liên tiếp');
  },
  // Dạng 5 · công suất × thời gian = năng lượng
  congSuat: (cap = 'Diện tích hình chữ nhật dưới đường công suất chính là năng lượng lò toả ra.') => {
    let b = defs('cs');
    b += `<line x1="46" y1="130" x2="306" y2="130" stroke="${INK}" stroke-width="${SW}"/><line x1="46" y1="130" x2="46" y2="14" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<rect x="46" y="40" width="230" height="90" fill="${GREY}" opacity=".35" stroke="${INK}" stroke-width="${SW}"/>`;
    b += T(40, 52, 'P', { a: 'end', w: 700 }) + T(40, 82, '900', { a: 'end', size: 18 }) + T(40, 102, 'MW', { a: 'end', size: 18 });
    b += T(276, 160, '30 ngày', { a: 'end' }) + T(306, 126, 't', { a: 'end' });
    b += T(161, 92, 'E = P·t = ?', { a: 'middle', w: 700 });
    return wrap('0 0 312 168', b, cap, 'Đồ thị công suất của lò theo thời gian');
  },

  // ===== Bài 17 · Hiện tượng phóng xạ =====
  // Trang 1 · máy đếm không ngừng dù làm lạnh
  maDem: (cap = 'Nhúng nguồn vào nitơ lỏng, máy đếm vẫn kêu. Nhịp đếm có đổi không?') => {
    let b = defs('md');
    b += `<path d="M8 40 L8 112 Q8 128 24 128 L74 128 Q90 128 90 112 L90 40" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<rect x="12" y="68" width="74" height="56" fill="${GREY}" opacity=".35"/>` + `<circle cx="49" cy="104" r="9" fill="${RED}"/>`;
    b += T(49, 156, 'nitơ lỏng', { a: 'middle', size: 18 }) + T(49, 20, '−196 °C', { a: 'middle', size: 18 });
    b += arr(92, 104, 140, 104, 'md', RED, '6 4') + arr(92, 92, 140, 80, 'md', RED, '6 4');
    b += rect(150, 56, 90, 76) + T(195, 84, 'ống', { a: 'middle', size: 18 }) + T(195, 106, 'đếm', { a: 'middle', size: 18 });
    b += `<rect x="252" y="62" width="62" height="40" rx="3" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(283, 90, '≈500', { a: 'middle', size: 20, w: 700 }) + T(316, 124, 'xung/phút', { a: 'end', size: 18 });
    b += arr(242, 82, 250, 82, 'md');
    return wrap('0 0 320 164', b, cap, 'Nguồn phóng xạ trong nitơ lỏng trước ống đếm');
  },
  // Trang 2 · ba tia trong điện trường
  batTia: (cap = 'Trong điện trường: α lệch về bản âm, β⁻ lệch về bản dương (nhiều hơn), γ không lệch.') => {
    let b = `<rect x="90" y="34" width="144" height="9" fill="${INK}"/><rect x="90" y="136" width="144" height="9" fill="${INK}"/>`;
    b += T(250, 44, '+', { size: 24, w: 700 }) + T(250, 154, '−', { size: 28, w: 700 });
    b += rect(2, 76, 58, 28) + T(26, 96, 'nguồn', { a: 'middle', size: 18 });
    b += `<line x1="60" y1="90" x2="312" y2="90" stroke="${INK}" stroke-width="${SW}"/>` + T(316, 84, 'γ', { a: 'end', size: 22, w: 700 });
    b += `<path d="M60 90 L90 90 Q180 90 234 62 L312 40" fill="none" stroke="${RED}" stroke-width="${SW}"/>` + T(316, 30, 'β⁻', { a: 'end', c: RED, size: 22, w: 700 });
    b += `<path d="M60 90 L90 90 Q180 90 234 100 L312 118" fill="none" stroke="${BLUE}" stroke-width="${SW}" stroke-dasharray="7 4"/>` + T(316, 144, 'α', { a: 'end', c: BLUE, size: 22, w: 700 });
    return wrap('0 0 320 160', b, cap, 'Ba tia phóng xạ trong điện trường giữa hai bản');
  },
  // Trang 2 · khả năng đâm xuyên
  xuyen: (cap = 'Mỗi tia dừng ở tấm chắn khác nhau: giấy, nhôm, chì.') => {
    let b = defs('xy');
    [['α', 'giấy', 96, 2, BLUE], ['β', 'nhôm', 178, 10, RED], ['γ', 'chì', 262, 30, INK]].forEach(([s, v, x, w, c], i) => {
      const y = 24 + i * 46;
      b += T(4, y + 8, s, { c, w: 700, size: 22 }) + arr(30, y, x - 2, y, 'xy', c, i === 0 ? '7 4' : '');
      b += `<rect x="${x}" y="${y - 18}" width="${w + 4}" height="36" fill="${GREY}" stroke="${INK}" stroke-width="2.4"/>`;
      b += T(x + w + 12, y + 7, v, { size: 18 });
    });
    return wrap('0 0 330 160', b, cap, 'Ba tia phóng xạ và tấm chắn của chúng');
  },
  // Trang 2 · dịch chuyển ô trong bảng tuần hoàn
  dichChuyenO: (cap = 'Mỗi tia đưa hạt nhân con sang ô nào so với hạt nhân mẹ ở ô Z?') => {
    let b = defs('dc2');
    ['Z−2', 'Z−1', 'Z', 'Z+1'].forEach((l, i) => {
      const x = 6 + i * 76;
      b += rect(x, 70, 66, 40, i === 2 ? `stroke="${RED}"` : '') + T(x + 33, 98, l, { a: 'middle', w: i === 2 ? 700 : 400 });
    });
    b += `<path d="M190 66 Q110 22 44 66" fill="none" stroke="${BLUE}" stroke-width="${SW}" stroke-dasharray="7 4" marker-end="url(#dc2)"/>` + T(118, 26, 'α', { a: 'middle', c: BLUE, w: 700, size: 22 });
    b += `<path d="M190 114 Q150 142 120 114" fill="none" stroke="${INK}" stroke-width="${SW}" marker-end="url(#dc2)"/>` + T(154, 148, 'β⁺', { a: 'middle', w: 700, size: 22 });
    b += `<path d="M196 66 Q226 30 262 66" fill="none" stroke="${RED}" stroke-width="${SW}" marker-end="url(#dc2)"/>` + T(230, 26, 'β⁻', { a: 'middle', c: RED, w: 700, size: 22 });
    return wrap('0 0 312 156', b, cap, 'Dịch chuyển ô của hạt nhân con trong bảng tuần hoàn');
  },
  // Trang 3 · phân rã mũ theo chu kì bán rã
  phanRaMu: (cap = 'Mỗi chu kì T, số hạt nhân còn lại giảm một nửa. Điền tỉ lệ còn lại ở các mốc.') =>
    phanRa(['0', 'T', '2T', '3T'], cap, 'prm'),
  // Trang 4 · Na-24 (T = 15 giờ)
  na24: (cap = 'Mẫu Na-24 có T = 15 giờ: sau 45 giờ là mấy chu kì? Còn lại bao nhiêu?') =>
    phanRa(['0', '15 h', '30 h', '45 h'], cap, 'na'),
  // Trang 5 · chia đôi mẫu
  chiaDoiMau: (cap = 'Chia mẫu làm hai: N và H giảm một nửa, còn T thì sao?') => {
    let b = defs('cd');
    b += rect(4, 40, 100, 80) + T(54, 72, 'N, H', { a: 'middle' }) + T(54, 100, 'T = 8 ngày', { a: 'middle', size: 18 });
    b += arr(108, 70, 150, 40, 'cd') + arr(108, 90, 150, 120, 'cd');
    b += rect(156, 6, 100, 64) + T(206, 36, 'N/2, H/2', { a: 'middle', size: 18 }) + T(206, 60, 'T = ?', { a: 'middle', size: 18, c: RED, w: 700 });
    b += rect(156, 90, 100, 64) + T(206, 120, 'N/2, H/2', { a: 'middle', size: 18 }) + T(206, 144, 'T = ?', { a: 'middle', size: 18, c: RED, w: 700 });
    return wrap('0 0 262 162', b, cap, 'Chia đôi mẫu phóng xạ');
  },
  // Dạng 1 · chuỗi phân rã của urani-238
  chuoiU: (cap = 'Điền A và Z của X, Y, W sau mỗi lần phân rã.') => {
    let b = defs('cu');
    ['', 'X', 'Y', 'W'].forEach((l, i) => {
      const x = 4 + i * 80;
      b += rect(x, 40, 64, 56);
      if (i === 0) b += nuc(x + 8, 76, 238, 92, 'U', 28);
      else b += T(x + 32, 62, 'A = ?', { a: 'middle', size: 18 }) + T(x + 32, 86, 'Z = ?', { a: 'middle', size: 18 }) + T(x + 32, 124, l, { a: 'middle', w: 700 });
      if (i < 3) b += `<line x1="${x + 64}" y1="68" x2="${x + 68}" y2="68" stroke="${INK}" stroke-width="${SW}"/>` + tri(x + 68, 68);
    });
    b += T(74, 30, 'α', { a: 'middle', c: BLUE, w: 700 }) + T(154, 30, 'β⁻', { a: 'middle', c: RED, w: 700 }) + T(234, 30, 'β⁻', { a: 'middle', c: RED, w: 700 });
    return wrap('0 0 316 134', b, cap, 'Chuỗi phân rã alpha rồi hai lần beta trừ của urani-238');
  },
  // Dạng 5 · định tuổi bằng C-14
  c14: (cap = 'Đo độ phóng xạ riêng h của mẫu, so với cây sống h₀, đọc ra số chu kì đã qua.') => {
    const X = (k) => 50 + k * 80, Y = (v) => 150 - 118 * v;
    let b = defs('c14') + `<line x1="44" y1="150" x2="306" y2="150" stroke="${INK}" stroke-width="${SW}"/><line x1="44" y1="150" x2="44" y2="14" stroke="${INK}" stroke-width="${SW}"/>`;
    let d = ''; for (let i = 0; i <= 30; i++) { const k = i / 10; d += `${i ? 'L' : 'M'}${X(k).toFixed(1)},${Y(2 ** -k).toFixed(1)}`; }
    b += `<path d="${d}" fill="none" stroke="${RED}" stroke-width="${SW}"/>`;
    b += T(50, 22, 'h₀ (cây sống)', { size: 18 }) + T(300, 182, 't', { a: 'end' });
    const y = Y(0.319);
    b += `<line x1="44" y1="${y}" x2="${X(1.65)}" y2="${y}" stroke="${GREY}" stroke-width="2" stroke-dasharray="4 4"/><line x1="${X(1.65)}" y1="${y}" x2="${X(1.65)}" y2="150" stroke="${GREY}" stroke-width="2" stroke-dasharray="4 4"/>`;
    b += `<circle cx="${X(1.65)}" cy="${y}" r="5" fill="${INK}"/>` + T(52, y - 8, 'h = ?', { size: 18, c: RED, w: 700 }) + T(X(1.65) + 8, 138, 't = ?', { size: 18, c: RED, w: 700 });
    [1, 2].forEach((k) => { b += `<line x1="${X(k)}" y1="146" x2="${X(k)}" y2="154" stroke="${INK}" stroke-width="${SW}"/>` + T(X(k), 176, k + 'T', { a: 'middle', size: 18 }); });
    return wrap('0 0 320 186', b, cap, 'Độ phóng xạ riêng của carbon-14 giảm theo thời gian');
  },

  // ===== Bài 18 · An toàn phóng xạ =====
  // Trang 1 · hai người ở 1 m và 3 m (l1, l2 là suất liều ghi trên hình)
  nguoiSauChi: (cap = 'Kỹ thuật viên lùi từ 1 m ra 3 m: suất liều ở chỗ mới ra sao?', h1 = 'H̊₁', h2 = 'H̊₂ = ?') => {
    const nguoi = (x) => `<circle cx="${x}" cy="62" r="11" fill="#fff" stroke="${INK}" stroke-width="${SW}"/><path d="M${x} 74 V102 M${x - 14} 84 H${x + 14} M${x} 102 L${x - 10} 124 M${x} 102 L${x + 10} 124" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
    let b = `<circle cx="26" cy="94" r="14" fill="${RED}"/>` + T(26, 136, 'nguồn', { a: 'middle', size: 18 });
    b += nguoi(110) + nguoi(278);
    b += `<line x1="26" y1="146" x2="110" y2="146" stroke="${INK}" stroke-width="${SW}"/>` + T(68, 170, '1 m', { a: 'middle', size: 18 });
    b += `<line x1="26" y1="146" x2="278" y2="146" stroke="${INK}" stroke-width="${SW}" stroke-dasharray="7 4"/>` + T(194, 170, '3 m', { a: 'middle', size: 18 });
    b += T(110, 38, h1, { a: 'middle', size: 18 }) + T(278, 38, h2, { a: 'middle', size: 18, c: RED, w: 700 });
    b += `<path d="M40 86 L96 70 M40 102 L96 110" stroke="${RED}" stroke-width="2" stroke-dasharray="4 4" fill="none"/>`;
    return wrap('0 0 310 180', b, cap, 'Hai người ở hai khoảng cách khác nhau từ nguồn phóng xạ');
  },
  // Trang 2 · các mốc liều trên thang logarit
  bacLieu: (cap = 'Thang logarit: mỗi mốc cao hơn là gấp nhiều lần mốc dưới. Đơn vị mSv.') => {
    const Y = (v) => 270 - 56 * (Math.log10(v) + 1);
    let b = `<line x1="40" y1="${Y(0.1)}" x2="40" y2="${Y(4000)}" stroke="${INK}" stroke-width="${SW}"/>`;
    [[0.1, '0,1 · X-quang ngực'], [2.4, '2,4 · phông/năm'], [7, '7 · chụp CT'], [20, '20 · nghề nghiệp/năm'], [4000, '4 000 · chết 50 %']].forEach(([v, l], i) => {
      const y = Y(v);
      b += `<circle cx="40" cy="${y}" r="6" fill="${i === 3 ? RED : INK}"/>` + T(56, y + 7, l, { size: 18, c: i === 3 ? RED : INK, w: i === 3 ? 700 : 400 });
    });
    return wrap('0 0 300 282', b, cap, 'Các mốc liều trên thang logarit');
  },
  // Dạng 3 · suất liều theo bình phương khoảng cách
  nghichBinhPhuong: (cap = 'Cùng chùm tia trải trên diện tích 1 ô, ? ô, ? ô khi xa r, 2r, 3r. Đếm ô rồi suy ra suất liều.') => {
    let b = `<circle cx="16" cy="70" r="9" fill="${RED}"/>`;
    [[56, 14, 'r'], [96, 28, '2r'], [136, 42, '3r']].forEach(([x, h, l]) => { b += `<line x1="${x}" y1="${70 - h / 2}" x2="${x}" y2="${70 + h / 2}" stroke="${INK}" stroke-width="5"/>` + T(x, 112, l, { a: 'middle', size: 18 }); });
    b += `<path d="M16 70 L136 49 M16 70 L136 91" stroke="${GREY}" stroke-width="2" stroke-dasharray="4 4" fill="none"/>`;
    b += luoi(186, 100 - 14, 14, 1) + luoi(220, 100 - 28, 28, 2) + luoi(262, 100 - 42, 42, 3);
    b += T(193, 124, '1 ô', { a: 'middle', size: 18 }) + T(234, 124, '? ô', { a: 'middle', size: 18, c: RED }) + T(283, 124, '? ô', { a: 'middle', size: 18, c: RED });
    return wrap('0 0 314 132', b, cap, 'Diện tích mà chùm tia trải ra tăng theo bình phương khoảng cách');
  },
  // Dạng 5 · tô phần liều còn lại của từng biện pháp
  baBienPhap: (cap = 'Mỗi thanh là 100 % liều ban đầu: tô phần còn lại.') => {
    let b = '';
    ['A · lùi ra 3 m', 'B · còn 10 phút', 'C · chì 5 mm', 'D · nhôm 3 mm'].forEach((l, i) => {
      const y = 8 + i * 38;
      b += T(4, y + 16, l, { size: 18 }) + rect(150, y, 150, 22);
    });
    b += T(150, 172, '0', { size: 18, a: 'middle' }) + T(300, 172, '100 %', { size: 18, a: 'end' });
    return wrap('0 0 306 180', b, cap, 'Bốn thanh trống để tô phần liều còn lại');
  },
  // Trang 5 · biển cảnh báo phóng xạ
  bienCanhBao: (cap = 'Biển ba cánh quạt, đặt ở nơi có nguồn phóng xạ.') => {
    const cx = 70, cy = 70, R = 52, r = 12;
    const sector = (a0) => { // quạt 60° từ góc a0
      const rad = (d) => (d * Math.PI) / 180, P = (rr, d) => `${(cx + rr * Math.cos(rad(d))).toFixed(1)},${(cy - rr * Math.sin(rad(d))).toFixed(1)}`;
      return `<path d="M${P(r, a0)} L${P(R, a0)} A${R},${R} 0 0 0 ${P(R, a0 + 60)} L${P(r, a0 + 60)} A${r},${r} 0 0 1 ${P(r, a0)} Z" fill="${INK}"/>`;
    };
    let b = `<rect x="4" y="4" width="132" height="132" rx="8" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + [90, 210, 330].map(sector).join('') + `<circle cx="${cx}" cy="${cy}" r="${r - 3}" fill="${INK}"/>`;
    return wrap('0 0 140 140', b, cap, 'Biển cảnh báo phóng xạ ba cánh quạt');
  },
};
