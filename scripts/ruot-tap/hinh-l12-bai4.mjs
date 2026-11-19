// Hình minh hoạ cho ruột tập VL12 · Bài 4 Thực hành: đo nhiệt dung riêng, nhiệt nóng chảy riêng, nhiệt hoá hơi riêng (lesson 5).
// Cùng quy tắc với hinh.mjs: mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét chứ không chỉ bằng màu,
// tự vẽ. Chú thích không lộ đáp án ô Dự đoán/ô điền đứng cạnh.
// Xem thử: node scripts/ruot-tap/l12-bai4.mjs --hinh (chụp vào out/hinh-l12-bai4/).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const dot = (x, y, r = 4.5, c = INK) => `<circle cx="${x}" cy="${y}" r="${r}" fill="${c}"/>`;
const rect = (x, y, w, h, fill = '#fff', st = INK) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${fill}" stroke="${st}" stroke-width="${SW}"/>`;
const arrow = (x, y, dir) => dir === 'r' ? `<path d="M${x},${y} l-9,-5 v10 z" fill="${INK}"/>` : `<path d="M${x},${y} l-5,9 h10 z" fill="${INK}"/>`;
const cube = (x, y, s = 16) => `<rect x="${x}" y="${y}" width="${s}" height="${s}" rx="2" fill="#fff" stroke="${BLUE}" stroke-width="2.4" transform="rotate(12 ${x + s / 2} ${y + s / 2})"/>`;
const nhietKe = (x, ytop, ybot) => `<rect x="${x - 4}" y="${ytop}" width="8" height="${ybot - ytop}" fill="#fff" stroke="${INK}" stroke-width="2.4"/><circle cx="${x}" cy="${ybot + 3}" r="7" fill="${RED}" stroke="${INK}" stroke-width="2.4"/>`;

export const hinhL12b4 = {
  // Trang 1 · Dự đoán: cốc nước đá trên bếp, nhiệt kế — chỉ mô tả cách đặt, không nêu số chỉ
  cocDa: (cap = 'Đun cốc nước đá đang tan, khuấy đều; nhiệt kế cắm giữa cốc.') => {
    let b = '';
    b += `<path d="M70,40 V132 Q70,148 86,148 H174 Q190,148 190,132 V40" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += cube(90, 62) + cube(122, 78) + cube(150, 58) + cube(106, 100) + cube(140, 108) + cube(86, 118) + cube(164, 94);
    b += nhietKe(130, 14, 100) + ln(130, 100, 130, 100);
    b += rect(62, 160, 136, 22, '#eef2fa') + T(130, 178, 'bếp điện', { a: 'middle', size: 18 });
    b += T(206, 28, 'nhiệt kế', { size: 18 });
    return wrap('0 0 300 190', b, cap, 'Cốc nước đá đặt trên bếp điện, nhiệt kế cắm trong cốc');
  },
  // Trang 2 · bố trí nhiệt lượng kế: bình xốp, dây điện trở, oát kế, nhiệt kế, que khuấy, cân
  soDo: (cap = 'Bố trí đo c: dây điện trở trong bình xốp nối oát kế và nguồn; cân đo m, nhiệt kế đo t.') => {
    let b = '';
    b += `<path d="M104,52 V150 Q104,162 116,162 H196 Q208,162 208,150 V52" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += rect(98, 40, 116, 12, '#eef2fa');
    b += `<path d="M106,84 H206" stroke="${BLUE}" stroke-width="2.4" stroke-dasharray="6 4" fill="none"/>`;
    b += T(156, 104, 'nước', { a: 'middle', c: BLUE, size: 18 });
    b += `<path d="M122,140 l8,-12 l12,24 l12,-24 l12,24 l12,-24 l12,24 l8,-12" fill="none" stroke="${RED}" stroke-width="3.2"/>`;
    b += T(158, 124, 'dây R', { a: 'middle', c: RED, size: 18 });
    b += nhietKe(190, 14, 96);
    b += T(204, 30, 'nhiệt kế', { size: 18 });
    b += ln(120, 18, 120, 126, INK, 3) + `<circle cx="120" cy="14" r="5" fill="#fff" stroke="${INK}" stroke-width="2.4"/>`;
    b += T(108, 30, 'que khuấy', { a: 'end', size: 18 });
    b += rect(92, 162, 128, 12, '#eef2fa') + T(156, 198, 'cân điện tử', { a: 'middle', size: 18 });
    b += ln(122, 140, 62, 140) + ln(194, 140, 262, 140);
    b += `<circle cx="40" cy="140" r="22" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(40, 148, 'W', { a: 'middle', w: 700, size: 22 }) + T(40, 108, 'oát kế', { a: 'middle', size: 18 });
    b += rect(262, 122, 36, 36) + T(280, 148, '~', { a: 'middle', size: 26, w: 700 }) + T(280, 108, 'nguồn', { a: 'middle', size: 18 });
    b += ln(40, 162, 40, 222) + ln(40, 222, 280, 222) + ln(280, 158, 280, 222);
    return wrap('0 0 320 232', b, cap, 'Sơ đồ bố trí nhiệt lượng kế vỏ xốp, dây điện trở, oát kế, cân, nhiệt kế, que khuấy');
  },
  // Trang 2 · đồ thị t–τ khi đun nước đá liên tục: bốn đoạn đánh số, không số liệu
  doThi: (cap = 'Đun đá liên tục tới khi sôi: ba đoạn đánh số (1)–(3).', moc = null) => {
    const x0 = 56, y0 = 150, xe = 300, ye = 18;
    let b = ln(x0, y0, xe, y0) + ln(x0, y0, x0, ye) + arrow(xe, y0, 'r') + arrow(x0, ye, 'u');
    b += T(xe, moc ? y0 - 10 : y0 + 24, `${gk('τ')} (s)`, { a: 'end' }) + T(x0 + 10, ye + 8, `${gk('t')} (°C)`);
    const A = [x0, 130], B = [114, 130], C = [166, 46], D = [276, 46];
    b += ln(A[0], A[1], B[0], B[1], INK, SW) + ln(B[0], B[1], C[0], C[1], INK, SW) + ln(C[0], C[1], D[0], D[1], INK, SW);
    b += T(x0 + 28, 118, '(1)', { w: 700 }) + T(142, 98, '(2)', { w: 700, a: 'end' }) + T(212, 36, '(3)', { w: 700 });
    b += ln(x0, 46, C[0], 46, GREY, 2, '5 4') + T(x0 - 6, 53, '100', { a: 'end' }) + T(x0 - 6, 137, '0', { a: 'end' });
    if (moc) for (const [x, s] of [[B[0], moc[0]], [C[0], moc[1]], [D[0], moc[2]]]) b += ln(x, y0, x, y0 - 6, INK, 2.4) + T(x, y0 + 22, s, { a: 'middle', size: 18, c: RED });
    return wrap('0 0 320 186', b, cap, 'Đồ thị nhiệt độ theo thời gian khi đun nước đá tới sôi, có hai đoạn nằm ngang');
  },
  // Trang 4/6 · phễu nước đá hai giai đoạn
  pheu: (cap = 'Phễu nước đá: dây điện trở vùi trong đá; cân đo nước chảy xuống cốc.') => {
    let b = '';
    b += `<path d="M60,24 H200 L140,98 V118 H120 V98 Z" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += cube(78, 34) + cube(150, 34) + cube(176, 40) + cube(96, 74) + cube(138, 72);
    b += `<path d="M98,56 l5,-12 l10,24 l10,-24 l10,24 l10,-24 l5,12" fill="none" stroke="${RED}" stroke-width="3"/>`;
    b += ln(98, 56, 20, 56, INK, 2.8) + ln(20, 56, 20, 96, INK, 2.8) + T(20, 120, 'nguồn', { a: 'middle', size: 18 });
    b += `<path d="M118,142 H142 V176 Q142,182 136,182 H124 Q118,182 118,176 Z" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<circle cx="130" cy="124" r="3" fill="${BLUE}"/><circle cx="130" cy="134" r="3" fill="${BLUE}"/>`;
    b += rect(78, 188, 104, 12, '#eef2fa') + T(130, 222, 'cân điện tử', { a: 'middle', size: 18 });
    b += T(214, 168, 'cốc hứng', { size: 18 });
    return wrap('0 0 320 232', b, cap, 'Phễu chứa nước đá có dây điện trở, cốc hứng đặt trên cân');
  },
  // Trang 5 · lưới đồ thị t theo τ: τ 0–300 s (vạch 50 s, lưới mịn 10 s), t 20–90 °C (vạch 10 °C, lưới mịn 2 °C)
  luoi: (cap = 'Vẽ các điểm trung bình (t̄) và kẻ một đường thẳng đi gần mọi điểm.') => {
    const X0 = 62, Y0 = 296, W = 360, H = 245;   // 360 = 300 s (1,2 đơn vị/s); 245 = 70 °C (3,5 đơn vị/°C)
    let b = '';
    for (let i = 0; i <= 30; i++) b += ln(X0 + i * 12, Y0, X0 + i * 12, Y0 - H, '#d3dbec', i % 5 === 0 ? 1.1 : .5);
    for (let j = 0; j <= 35; j++) b += ln(X0, Y0 - j * 7, X0 + W, Y0 - j * 7, '#d3dbec', j % 5 === 0 ? 1.1 : .5);
    b += `<rect x="${X0}" y="${Y0 - H}" width="${W}" height="${H}" fill="none" stroke="${INK}" stroke-width="2.2"/>`;
    for (let i = 0; i <= 6; i++) b += ln(X0 + i * 60, Y0, X0 + i * 60, Y0 + 8, INK, 2.2) + T(X0 + i * 60, Y0 + 28, `${i * 50}`, { a: 'middle', size: 16 });
    for (let j = 0; j <= 7; j++) b += ln(X0 - 8, Y0 - j * 35, X0, Y0 - j * 35, INK, 2.2) + T(X0 - 12, Y0 - j * 35 + 6, `${20 + j * 10}`, { a: 'end', size: 16 });
    b += T(X0 + W, Y0 + 52, `${gk('τ')} (s)`, { a: 'end', size: 18, w: 700 }) + T(8, Y0 - H - 14, `${gk('t')} (°C)`, { size: 18, w: 700 });
    return wrap('0 0 450 360', b, cap, 'Lưới vẽ đồ thị nhiệt độ theo thời gian');
  },
  // Bài tương tự / Dạng 2 · không dùng
};
