// Hình minh hoạ cho ruột tập VL11 · Bài 21 Tụ điện (lesson 40). Cùng quy tắc với hinh.mjs/hinh-l10-bai23.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh. Xem thử: node scripts/ruot-tap/l11-bai21.mjs --hinh (chụp vào out/hinh-l11-bai21/).
// Chữ "µ" dùng U+00B5 (có trong bộ latin của Source Sans 3), không dùng U+03BC; chữ Hi Lạp khác lấy từ KaTeX_Math (gk).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const arr = (x1, y1, x2, y2, id, c = INK, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${SW}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const rect = (x, y, w, h, o = {}) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${o.rx ?? 3}" fill="${o.fill ?? '#fff'}" stroke="${o.c ?? INK}" stroke-width="${o.w ?? SW}"${o.dash ? ` stroke-dasharray="${o.dash}"` : ''}/>`;
const dot = (x, y) => `<circle cx="${x}" cy="${y}" r="4.5" fill="${INK}"/>`;
const C = (i) => `C${sb(i)}`;
const km = (ch) => `<tspan font-family="KaTeX_Main">${ch}</tspan>`; // ≈ ≤ không có trong Source Sans 3 đã nạp

// Tụ trên dây NGANG, tâm (x,y): che dây bằng ô trắng rồi vẽ hai bản dọc. lab ở trên.
const tuN = (x, y, lab = '', o = {}) => `<rect x="${x - 7}" y="${y - 4}" width="14" height="8" fill="#fff"/>`
  + ln(x - 7, y - 20, x - 7, y + 20, INK, 4.5) + ln(x + 7, y - 20, x + 7, y + 20, INK, 4.5) + (lab ? T(x, y - 28, lab, { a: 'middle', w: 700, ...o }) : '');
// Tụ trên dây DỌC
const tuD = (x, y, lab = '', o = {}) => `<rect x="${x - 4}" y="${y - 7}" width="8" height="14" fill="#fff"/>`
  + ln(x - 20, y - 7, x + 20, y - 7, INK, 4.5) + ln(x - 20, y + 7, x + 20, y + 7, INK, 4.5) + (lab ? T(x + 28, y + 7, lab, { w: 700, ...o }) : '');
// Nguồn trên dây NGANG: vạch dài mảnh (+) bên trái, vạch ngắn dày (−) bên phải
const pinN = (x, y, lab = '') => `<rect x="${x - 7}" y="${y - 4}" width="14" height="8" fill="#fff"/>`
  + ln(x - 6, y - 20, x - 6, y + 20, INK, 2.4) + ln(x + 6, y - 11, x + 6, y + 11, INK, 6.5)
  + T(x - 12, y - 18, '+', { a: 'end', w: 700 }) + T(x + 13, y - 14, '−', { w: 700 }) + (lab ? T(x, y + 42, lab, { a: 'middle' }) : '');
// LED trên dây ngang, mũi chỉ chiều dòng đi qua được
const led = (x, y, phai = true) => {
  const s = phai ? 1 : -1;
  return `<rect x="${x - 12}" y="${y - 4}" width="24" height="8" fill="#fff"/><path d="M${x - 11 * s},${y - 12} L${x + 9 * s},${y} L${x - 11 * s},${y + 12} z" fill="#fff" stroke="${INK}" stroke-width="2.6"/>`
    + ln(x + 10 * s, y - 13, x + 10 * s, y + 13, INK, 3) + ln(x + 2, y - 16, x + 12, y - 28, RED, 2.2) + ln(x + 10, y - 14, x + 20, y - 26, RED, 2.2);
};
// khoá K mở trên dây ngang
const khoaMo = (x, y) => `<rect x="${x - 16}" y="${y - 4}" width="32" height="8" fill="#fff"/>${dot(x - 16, y)}${dot(x + 16, y)}` + ln(x - 16, y, x + 12, y - 18, INK, 2.8);

export const hinhL11b21 = {
  // Trang 1 · Dự đoán: đèn flash rời chạy bằng 2 pin tiểu
  flash: (cap = 'Đèn flash rời chạy bằng 2 pin tiểu.') => {
    let b = '';
    b += rect(70, 60, 120, 120, { rx: 8 }) + rect(80, 18, 100, 42, { rx: 5 }) + ln(90, 39, 170, 39, GREY, 2, '4 3');
    // tia sáng hai bên đèn
    b += [[-22, -10], [-26, 6], [-22, 22]].map(([dx, dy]) => ln(76, 39 + dy / 2, 76 + dx, 39 + dy, RED, 2.6) + ln(184, 39 + dy / 2, 184 - dx, 39 + dy, RED, 2.6)).join('');
    // hai pin
    b += rect(88, 120, 30, 50, { rx: 4 }) + rect(142, 120, 30, 50, { rx: 4 }) + T(103, 152, '+', { a: 'middle', w: 700 }) + T(157, 152, '+', { a: 'middle', w: 700 });
    b += T(130, 106, '2 × 1,5 V', { a: 'middle' });
    b += T(218, 100, 'píííp…', { c: BLUE }) + T(218, 128, 'vài giây', { c: BLUE });
    b += T(218, 30, 'loé', { c: RED, w: 700 }) + T(218, 56, `${km('≈')} 0,001 s`, { c: RED });
    return wrap('0 0 320 186', b, cap, 'Đèn flash rời của máy ảnh');
  },
  // Trang 1 · II.1: tụ phẳng nối nguồn — bản nào tích +Q?
  tuPhang: (cap = 'Tụ phẳng nối với nguồn. Bên phải: kí hiệu tụ trong sơ đồ.') => {
    let b = '';
    b += rect(70, 22, 12, 112, { fill: GREY }) + rect(150, 22, 12, 112, { fill: GREY });
    b += `<rect x="84" y="24" width="64" height="108" fill="${'#eef2fa'}" stroke="none"/>` + T(116, 84, 'điện', { a: 'middle', size: 20 }) + T(116, 106, 'môi', { a: 'middle', size: 20 });
    b += T(50, 70, '?', { a: 'middle', w: 700, c: RED }) + T(184, 70, '?', { a: 'middle', w: 700, c: RED });
    b += ln(76, 134, 76, 170) + ln(156, 134, 156, 170) + ln(76, 170, 156, 170) + pinN(116, 170);
    b += T(116, 16, 'd', { a: 'middle' });
    // kí hiệu
    b += ln(222, 78, 258, 78, INK, 2.8) + ln(278, 78, 314, 78, INK, 2.8) + ln(258, 54, 258, 102, INK, 4.5) + ln(278, 54, 278, 102, INK, 4.5);
    b += T(268, 132, 'kí hiệu', { a: 'middle' });
    return wrap('0 0 320 200', b, cap, 'Tụ điện phẳng nối với nguồn');
  },
  // Trang 1 · thí nghiệm: nạp qua LED rồi phóng qua LED đảo chiều
  ledMach: (cap = 'Trái: nạp. Phải: phóng, LED đảo chiều.') => {
    let b = '';
    // nạp: vòng chữ nhật (14..150, 40..150)
    b += rect(14, 40, 136, 110, { fill: 'none', rx: 0 }) + pinN(82, 150, '') + tuD(150, 95) + led(82, 40, true);
    b += T(82, 186, 'nạp (9 V)', { a: 'middle', w: 700 });
    // phóng
    b += rect(184, 40, 120, 110, { fill: 'none', rx: 0 }) + led(244, 40, false) + tuD(304, 95);
    b += T(244, 186, 'phóng', { a: 'middle', w: 700 });
    return wrap('0 0 320 196', b, cap, 'Mạch nạp và phóng tụ qua đèn LED');
  },
  // Trang 2 · đồ thị Q theo U: 5 điểm đo, để HS tự kẻ đường
  doThiQU: (cap = 'Năm điểm đo của bảng bên. Kẻ đường thẳng qua gốc và các điểm.') => {
    const X = (u) => 64 + u * 22, Y = (q) => 176 - q * 0.028; // U 0–10 V → 64..304; Q 0–5000 µC → 176..26
    let b = defs('dq');
    for (let u = 2; u <= 10; u += 2) b += ln(X(u), 26, X(u), 176, '#d3dbec', 1.4) + T(X(u), 198, String(u), { a: 'middle' });
    for (let q = 1000; q <= 5000; q += 1000) b += ln(64, Y(q), 304, Y(q), '#d3dbec', 1.4) + T(58, Y(q) + 7, String(q), { a: 'end' });
    b += arr(64, 176, 312, 176, 'dq') + arr(64, 176, 64, 14, 'dq');
    b += T(312, 166, 'U (V)', { a: 'end' }) + T(72, 16, 'Q (µC)');
    [[2, 980], [4, 1900], [6, 2890], [8, 3820], [10, 4800]].forEach(([u, q]) => { b += `<circle cx="${X(u)}" cy="${Y(q).toFixed(1)}" r="5.5" fill="${BLUE}"/>`; });
    return wrap('0 0 320 206', b, cap, 'Đồ thị điện tích theo hiệu điện thế');
  },
  // Trang 2 · thí nghiệm hai tấm nhôm: mỗi lần chỉ đổi một yếu tố
  tamNhom: (cap = 'Nhìn ngang hai tấm nhôm. Mỗi lần chỉ đổi một yếu tố so với “gốc”.') => {
    let b = '';
    const o = [[10, 40, 'gốc'], [170, 40, 'tăng d'], [10, 150, 'trượt lệch'], [170, 150, 'chèn nhựa']];
    o.forEach(([x, y, lb], i) => {
      const g = i === 1 ? 28 : 14, dx = i === 2 ? 50 : 0;
      b += rect(x + 20, y, 100, 6, { fill: GREY, w: 2 }) + rect(x + 20 + dx, y + 6 + g, 100, 6, { fill: GREY, w: 2 });
      if (i === 3) b += rect(x + 20, y + 6, 100, g, { fill: '#eef2fa', w: 1.6, dash: '4 3' });
      b += T(x + 70, y - 10, lb, { a: 'middle', w: 700 });
      b += T(x + 70 + dx / 2, y + 6 + g + 34, i === 1 ? 'C = ?' : i === 0 ? `${km('≈')} 350 pF` : 'C = ?', { a: 'middle', c: i === 0 ? INK : RED });
    });
    return wrap('0 0 320 236', b, cap, 'Tụ tự chế từ hai tấm nhôm');
  },
  // Trang 3 · năng lượng = diện tích dưới đường Q–U
  tamGiac: (cap = 'Nạp tụ: U tăng dần từ 0. Phần tô là năng lượng của tụ.') => {
    let b = defs('tg');
    b += `<path d="M60,170 L250,40 L250,170 z" fill="#fde7d6" stroke="none"/>`;
    b += arr(60, 170, 300, 170, 'tg') + arr(60, 170, 60, 14, 'tg');
    b += ln(60, 170, 262, 32, BLUE, 3.2) + ln(250, 40, 250, 170, GREY, 2, '5 4') + ln(60, 40, 250, 40, GREY, 2, '5 4');
    b += T(252, 194, 'U', { a: 'middle' }) + T(48, 46, 'Q', { a: 'end' }) + T(300, 160, 'U', { a: 'end', c: GREY }) + T(72, 24, 'Q', { c: GREY });
    b += T(190, 140, 'W = ?', { a: 'middle', w: 700, c: RED });
    return wrap('0 0 320 202', b, cap, 'Đồ thị Q theo U khi nạp tụ');
  },
  // Trang 3 · ghép nối tiếp và song song
  ghep: (cap = 'Trên: nối tiếp. Dưới: song song. Cái gì chung ở mỗi cách?') => {
    let b = '';
    b += ln(20, 50, 300, 50) + dot(20, 50) + dot(300, 50) + tuN(120, 50, C(1)) + tuN(210, 50, C(2));
    b += T(20, 82, 'A', { a: 'middle', w: 700 }) + T(300, 82, 'B', { a: 'middle', w: 700 });
    b += ln(20, 160, 100, 160) + ln(220, 160, 300, 160) + ln(100, 120, 100, 200) + ln(220, 120, 220, 200) + ln(100, 120, 220, 120) + ln(100, 200, 220, 200);
    b += dot(20, 160) + dot(300, 160) + tuN(160, 120, C(1)) + tuN(160, 200, '') + T(186, 192, C(2), { w: 700 });
    b += T(20, 192, 'A', { a: 'middle', w: 700 }) + T(300, 192, 'B', { a: 'middle', w: 700 });
    return wrap('0 0 320 222', b, cap, 'Hai cách ghép tụ');
  },
  // Trang 3 · bẫy 3: còn nối nguồn hay đã ngắt
  nguon: (cap = 'Trái: vẫn nối nguồn. Phải: đã ngắt nguồn. Đại lượng nào giữ nguyên?') => {
    let b = '';
    b += rect(14, 30, 120, 120, { fill: 'none', rx: 0 }) + tuN(74, 30) + pinN(74, 150);
    b += rect(186, 30, 120, 120, { fill: 'none', rx: 0 }) + tuN(246, 30) + pinN(246, 150);
    b += `<rect x="301" y="72" width="10" height="36" fill="#fff"/>` + dot(306, 72) + dot(306, 108) + ln(306, 108, 324, 80, INK, 2.8);
    b += T(74, 84, 'giữ gì?', { a: 'middle', c: RED }) + T(246, 84, 'giữ gì?', { a: 'middle', c: RED });
    return wrap('0 0 330 166', b, cap, 'Tụ còn nối nguồn và tụ đã ngắt nguồn');
  },
  // Trang 4 · bài toán mẫu: hai tụ nối tiếp vào 12 V
  baiMau: (cap = 'Hai tụ nối tiếp. Tụ nào chịu hiệu điện thế lớn hơn?') => {
    let b = '';
    b += rect(30, 50, 260, 120, { fill: 'none', rx: 0 }) + tuN(110, 50, `${C(1)} 3 µF`) + tuN(210, 50, `${C(2)} 6 µF`) + pinN(160, 170, '');
    b += T(110, 104, `U${sb(1)} = ?`, { a: 'middle', c: RED }) + T(210, 104, `U${sb(2)} = ?`, { a: 'middle', c: RED }) + T(186, 178, '12 V');
    return wrap('0 0 320 184', b, cap, 'Hai tụ ghép nối tiếp vào nguồn 12 V');
  },
  // Trang 5 · thử thách khá: hai tụ nối tiếp, mỗi tụ chịu tối đa 50 V
  thuThach: (cap = 'Mỗi tụ chịu tối đa 50 V. Tụ nào chạm 50 V trước?') => {
    let b = '';
    b += ln(14, 70, 306, 70) + dot(14, 70) + dot(306, 70) + tuN(110, 70, '2 µF') + tuN(210, 70, '4 µF');
    b += T(110, 124, `${km('≤')} 50 V`, { a: 'middle' }) + T(210, 124, `${km('≤')} 50 V`, { a: 'middle' }) + T(160, 166, 'U bộ tối đa = ?', { a: 'middle', c: RED, w: 700 });
    return wrap('0 0 320 180', b, cap, 'Hai tụ nối tiếp có giới hạn hiệu điện thế');
  },
  // Bài tập mẫu D3 / Bài tương tự D3: tụ phẳng bản vuông — nhìn trên + nhìn ngang
  tuVuong: (a = 'a', d = 'd', cap = '') => {
    let b = defs('tv');
    b += rect(40, 30, 96, 96, { fill: '#eef2fa' }) + T(88, 22, a, { a: 'middle' }) + T(144, 86, a, {});
    b += rect(200, 50, 110, 8, { fill: GREY, w: 2 }) + rect(200, 100, 110, 8, { fill: GREY, w: 2 });
    b += arr(255, 74, 255, 60, 'tv', BLUE) + arr(255, 84, 255, 98, 'tv', BLUE) + T(268, 86, d, { c: BLUE });
    b += T(88, 150, 'mặt bản', { a: 'middle', c: GREY }) + T(255, 150, 'nhìn ngang', { a: 'middle', c: GREY });
    return wrap('0 0 320 158', b, cap, 'Tụ phẳng hai bản vuông');
  },
  // Bài tập mẫu D4: (C1 nối tiếp C2) song song C3
  honHop: (cap = '', v = ['5 µF', '20 µF', '6 µF'], U = '60 V') => {
    let b = '';
    b += ln(14, 120, 50, 120) + ln(270, 120, 306, 120) + ln(50, 60, 50, 170) + ln(270, 60, 270, 170) + ln(50, 60, 270, 60) + ln(50, 170, 270, 170);
    b += dot(14, 120) + dot(306, 120) + tuN(120, 60, `${C(1)} ${v[0]}`) + tuN(200, 60, `${C(2)} ${v[1]}`) + tuN(160, 170, '') + T(160, 206, `${C(3)} ${v[2]}`, { a: 'middle', w: 700 });
    b += T(14, 108, 'A', { a: 'middle', w: 700 }) + T(306, 108, 'B', { a: 'middle', w: 700 }) + T(160, 128, `U${sb('AB')} = ${U}`, { a: 'middle' });
    return wrap('0 0 320 214', b, cap, 'Ghép tụ hỗn hợp');
  },
  // Bài tương tự D4·2: (C1 song song C2) nối tiếp C3
  honHop2: (cap = '', v = ['2 µF', '4 µF', '3 µF'], U = '18 V') => {
    let b = '';
    b += ln(14, 110, 60, 110) + ln(160, 110, 306, 110) + ln(60, 60, 60, 160) + ln(160, 60, 160, 160) + ln(60, 60, 160, 60) + ln(60, 160, 160, 160);
    b += dot(14, 110) + dot(306, 110) + tuN(110, 60, `${C(1)} ${v[0]}`) + tuN(110, 160, '') + T(110, 196, `${C(2)} ${v[1]}`, { a: 'middle', w: 700 }) + tuN(234, 110, `${C(3)} ${v[2]}`);
    b += T(14, 98, 'A', { a: 'middle', w: 700 }) + T(306, 98, 'B', { a: 'middle', w: 700 }) + T(234, 160, `U${sb('AB')} = ${U}`, { a: 'middle' });
    return wrap('0 0 320 206', b, cap, 'Ghép tụ hỗn hợp: cụm song song nối tiếp một tụ');
  },
  // Bài tập mẫu D5: ngắt nguồn rồi kéo hai bản ra xa
  keoBan: (cap = '', k = '3d') => {
    let b = defs('kb');
    b += rect(20, 40, 100, 8, { fill: GREY, w: 2 }) + rect(20, 80, 100, 8, { fill: GREY, w: 2 }) + T(130, 72, 'd', {}) + T(70, 30, 'trước', { a: 'middle', w: 700 });
    b += T(70, 146, 'đã ngắt nguồn', { a: 'middle', c: GREY, size: 20 });
    b += arr(160, 64, 196, 64, 'kb', BLUE);
    b += rect(208, 20, 100, 8, { fill: GREY, w: 2 }) + rect(208, 112, 100, 8, { fill: GREY, w: 2 }) + T(258, 74, k, { a: 'middle', c: BLUE }) + T(258, 146, 'sau', { a: 'middle', w: 700 });
    return wrap('0 0 320 156', b, cap, 'Kéo hai bản tụ ra xa sau khi ngắt nguồn');
  },
};
