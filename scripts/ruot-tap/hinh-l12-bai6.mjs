// Hình minh hoạ cho ruột tập VL12 · Bài 6 Định luật Boyle. Định luật Charles (lesson 7). Cùng quy tắc với hinh.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh: đồ thị chỉ đánh số đường (1), (2), không ghi đường nào nóng hơn/áp suất lớn hơn.
// Xem thử: node scripts/ruot-tap/l12-bai6.mjs --hinh (chụp vào out/hinh-l12-bai6/).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const arr = (x1, y1, x2, y2, id, c = INK, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${SW}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const HG = '#5d6680';

// Hệ trục: gốc O tại (x0, y0), trục tung cao h, trục hoành dài w
const truc = (x0, y0, w, h, ty, tx, id) => defs(id) + arr(x0, y0, x0, y0 - h, id) + arr(x0, y0, x0 + w, y0, id)
  + T(x0 + 8, y0 - h + 10, ty, { w: 700 }) + T(x0 + w - 2, y0 + 24, tx, { w: 700, a: 'end' }) + T(x0 - 6, y0 + 20, 'O', { a: 'end' });
// Nhánh hypebol p = k/V trong khung toạ độ (đơn vị px)
const hyp = (x0, y0, k, v1, v2, c, dash = '') => {
  const pts = Array.from({ length: 24 }, (_, i) => { const v = v1 + (v2 - v1) * i / 23; return `${(x0 + v).toFixed(1)},${(y0 - k / v).toFixed(1)}`; });
  return `<polyline points="${pts.join(' ')}" fill="none" stroke="${c}" stroke-width="${SW}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
};

// Ống thuỷ tinh thẳng đứng một đầu kín, cột khí (trắng) bị giam bởi cột Hg (sẫm). len = [khí, Hg] (px), up = miệng hướng lên
const ong = (x, yTop, L, up, len, nh = {}) => {
  const w = 32, yB = yTop + L, [lk, lh] = len;
  let b = '';
  // khí và Hg
  if (up) {
    b += `<rect x="${x}" y="${yB - lk - lh}" width="${w}" height="${lh}" fill="${HG}"/>`;
    b += T(x + w / 2, yB - lk / 2 + 7, nh.khi ?? 'khí', { a: 'middle' });
  } else {
    b += `<rect x="${x}" y="${yTop + lk}" width="${w}" height="${lh}" fill="${HG}"/>`;
    b += T(x + w / 2, yTop + lk / 2 + 7, nh.khi ?? 'khí', { a: 'middle' });
  }
  // thành ống: hở ở đầu miệng
  b += up ? `<path d="M${x},${yTop} L${x},${yB} L${x + w},${yB} L${x + w},${yTop}" fill="none" stroke="${INK}" stroke-width="${SW}"/>`
    : `<path d="M${x},${yB} L${x},${yTop} L${x + w},${yTop} L${x + w},${yB}" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
  // kích thước bên phải
  const xd = x + w + 8, cap = (y1, y2, s) => ln(xd, y1, xd, y2, GREY, 2) + ln(xd - 4, y1, xd + 4, y1, GREY, 2) + ln(xd - 4, y2, xd + 4, y2, GREY, 2)
    + T(xd + 7, (y1 + y2) / 2 + 7, s);
  if (up) b += cap(yB - lk - lh, yB - lk, nh.h ?? 'h') + (nh.l ? cap(yB - lk, yB, nh.l) : '');
  else b += cap(yTop + lk, yTop + lk + lh, nh.h ?? 'h') + (nh.l ? cap(yTop, yTop + lk, nh.l) : '');
  // áp suất khí quyển ở miệng ống
  if (nh.p0 !== false) b += up ? arr(x + w / 2, yTop - 30, x + w / 2, yTop - 4, nh.id, BLUE) + T(x - 4, yTop - 14, `p${sb('0')}`, { c: BLUE, w: 700, a: 'end' })
    : arr(x + w / 2, yB + 30, x + w / 2, yB + 4, nh.id, BLUE) + T(x - 4, yB + 24, `p${sb('0')}`, { c: BLUE, w: 700, a: 'end' });
  return b;
};

export const hinhL12b6 = {
  // ===== Trang học bài mới =====
  // Dự đoán: bơm xe bịt đầu ra, ấn chậm. Không ghi số áp suất (lộ đáp án ô Dự đoán).
  bomXe: (cap = 'Bịt đầu ra, ấn cán bơm thật chậm: khí bị nhốt trong thân bơm.') => {
    let b = defs('bx');
    b += ln(60, 14, 180, 14, INK, 6) + ln(120, 14, 120, 86, INK, 5);                       // tay cầm + cán
    b += `<path d="M80,40 L80,214 L160,214 L160,40" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<rect x="82" y="86" width="76" height="12" fill="${GREY}"/>` + T(170, 98, 'pittông');
    for (let i = 0; i < 9; i++) b += `<circle cx="${94 + (i % 3) * 26}" cy="${124 + Math.floor(i / 3) * 32}" r="3.6" fill="${INK}"/>`;
    b += T(170, 160, 'khí') + ln(160, 206, 196, 206) + `<rect x="196" y="198" width="12" height="16" fill="${INK}"/>` + T(214, 214, 'bịt');
    b += arr(200, 4, 200, 44, 'bx', RED) + T(208, 34, 'ấn', { c: RED, w: 700 });
    return wrap('0 0 300 224', b, cap, 'Bơm xe đạp bịt đầu ra, pittông ấn xuống');
  },
  // Boyle: hai đường đẳng nhiệt, chỉ đánh số (1), (2)
  doThiPV: (cap = 'Hai đường đẳng nhiệt của cùng một lượng khí.') => {
    let b = truc(40, 196, 250, 186, 'p', 'V', 'pv');
    b += hyp(40, 196, 3400, 22, 236, INK) + hyp(40, 196, 9000, 52, 236, RED, '8 5');
    b += T(200, 166, '(1)', { w: 700 }) + T(194, 128, '(2)', { c: RED, w: 700 });
    return wrap('0 0 300 222', b, cap, 'Hai đường đẳng nhiệt trên đồ thị p–V');
  },
  // Charles: hai đường đẳng áp, nét đứt là phần kéo dài về gốc
  doThiVT: (cap = 'Hai đường đẳng áp của cùng một lượng khí; nét đứt: phần kéo dài, không đo.') => {
    let b = truc(40, 196, 250, 186, 'V', 'T (K)', 'vt');
    const d = (k, c, dash) => ln(40, 196, 40 + 110, 196 - 110 * k, c, 2, '4 5') + ln(150, 196 - 110 * k, 262, 196 - 222 * k, c, SW, dash);
    b += d(.48, INK, '') + d(.74, RED, '9 5');
    b += T(270, 196 - 222 * .48 + 6, '(1)', { w: 700 }) + T(254, 196 - 222 * .74 - 4, '(2)', { c: RED, w: 700, a: 'end' });
    return wrap('0 0 300 222', b, cap, 'Hai đường đẳng áp trên đồ thị V–T');
  },
  // Cột khí trong ống (thí nghiệm Charles): giọt dầu nhốt khí, ngâm vào cốc nước
  ongCharles: (cap = 'Ống hở trên, giọt dầu nhốt cột khí dài ℓ; đổi cốc nước, đo ℓ.') => {
    let b = `<path d="M20,70 L20,210 L170,210 L170,70" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<path d="M20,96 L170,96" stroke="${BLUE}" stroke-width="2" stroke-dasharray="7 5"/>` + T(164, 88, 'nước', { a: 'end', c: BLUE });
    b += `<path d="M90,14 L90,198 L112,198 L112,14" fill="none" stroke="${INK}" stroke-width="${SW}"/>` + T(118, 30, 'hở');
    b += `<rect x="92" y="110" width="18" height="12" fill="${HG}"/>` + ln(112, 116, 186, 116, GREY, 1.6) + T(190, 122, 'giọt dầu');
    b += ln(126, 122, 126, 198, GREY, 2) + ln(120, 122, 132, 122, GREY, 2) + ln(120, 198, 132, 198, GREY, 2) + T(136, 168, 'ℓ', { w: 700 });
    b += ln(112, 170, 186, 170, GREY, 1.6) + T(190, 176, 'cột khí');
    b += `<rect x="40" y="120" width="8" height="78" fill="#fff" stroke="${INK}" stroke-width="2"/>` + T(44, 114, 't', { a: 'middle', w: 700 });
    return wrap('0 0 300 220', b, cap, 'Ống có cột khí nhúng trong cốc nước');
  },
  // Áp suất khí bị cột Hg giam: hai cách đặt ống
  haiOng: (cap = 'Cột Hg (sẫm) cao h giam cột khí: (a) miệng hướng lên, (b) miệng hướng xuống.') => {
    let b = defs('ho');
    b += T(80, 230, '(a)', { w: 700, a: 'middle' }) + ong(64, 46, 150, true, [70, 46], { id: 'ho' });
    b += T(230, 230, '(b)', { w: 700, a: 'middle' }) + ong(214, 20, 150, false, [70, 46], { id: 'ho' });
    return wrap('0 0 300 238', b, cap, 'Hai ống thuỷ tinh có cột thuỷ ngân giam khí');
  },
  // Bài toán mẫu: xilanh y tế bịt đầu
  xilanh: (cap = 'Bịt đầu xilanh, ấn pittông từ từ: 60 ml → 25 ml.') => {
    let b = defs('xl');
    b += `<path d="M30,40 L250,40 M30,92 L250,92 M30,40 L30,92" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
    b += ln(30, 66, 8, 66, INK, 6) + `<rect x="2" y="56" width="8" height="20" fill="${INK}"/>`;
    b += `<rect x="176" y="42" width="12" height="48" fill="${GREY}"/>` + ln(188, 66, 280, 66, INK, 5) + ln(280, 44, 280, 88, INK, 6);
    for (let i = 0; i <= 6; i++) b += ln(30 + i * 24, 92, 30 + i * 24, 100, GREY, 2);
    b += T(100, 72, 'khí', { a: 'middle' }) + arr(240, 120, 196, 120, 'xl', RED) + T(246, 126, 'ấn', { c: RED, w: 700 });
    return wrap('0 0 300 136', b, cap, 'Xilanh y tế bịt đầu, pittông ấn vào');
  },
  // ===== Bài tập mẫu =====
  vtD3: (cap = 'A, B cùng T = 300 K.') => {
    const y0 = 158;
    let b = truc(40, y0, 250, 150, 'V (lít)', 'T (K)', 'v3');
    const sx = 0.6, sy = 17;                       // 1 K = 0,6 px; 1 lít = 17 px → 300 K ở x = 220
    const P = (Tk, V) => [40 + Tk * sx, y0 - V * sy];
    const l = (k, c, dash) => ln(40, 196, ...P(150, 150 * k), c, 2, '4 5') + ln(...P(150, 150 * k), ...P(400, 400 * k), c, SW, dash);
    b += l(4 / 300, INK, '') + l(6 / 300, RED, '9 5');
    const A = P(300, 4), B = P(300, 6);
    b += ln(A[0], y0, B[0], B[1], GREY, 1.6, '3 4') + ln(40, A[1], A[0], A[1], GREY, 1.6, '3 4') + ln(40, B[1], B[0], B[1], GREY, 1.6, '3 4');
    b += `<circle cx="${A[0]}" cy="${A[1]}" r="5" fill="${INK}"/><circle cx="${B[0]}" cy="${B[1]}" r="5" fill="${RED}"/>`;
    b += T(A[0] + 8, A[1] + 20, 'A', { w: 700 }) + T(B[0] - 8, B[1] - 6, 'B', { w: 700, a: 'end', c: RED });
    b += T(34, A[1] + 7, '4', { a: 'end' }) + T(34, B[1] + 7, '6', { a: 'end' }) + T(A[0], y0 + 22, '300', { a: 'middle' });
    b += T(P(400, 400 * 4 / 300)[0] + 4, P(400, 400 * 4 / 300)[1] + 20, '(1)', { w: 700, a: 'end' }) + T(P(370, 370 * 6 / 300)[0] - 6, P(370, 370 * 6 / 300)[1] - 4, '(2)', { w: 700, a: 'end', c: RED });
    return wrap('0 0 300 188', b, cap, 'Đồ thị V–T hai đường đẳng áp qua A và B');
  },
  latD5: (cap = 'Trước và sau khi lật; ℓ<sub>2</sub> = ?') => {
    let b = defs('l5');
    b += ong(50, 40, 160, true, [56, 40], { h: '20 cm', l: '28 cm', id: 'l5' });
    b += arr(146, 110, 176, 110, 'l5', INK);
    b += ong(196, 20, 160, false, [70, 40], { h: '20 cm', l: '?', id: 'l5' });
    return wrap('0 0 300 222', b, cap, 'Ống có cột thuỷ ngân trước và sau khi lật');
  },
};
