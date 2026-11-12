// Hình minh hoạ cho ruột tập VL10 · Bài 33 Biến dạng của vật rắn (lesson 78). Cùng quy tắc với hinh-l10-bai23.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh (lò xo 2 túi bị che, không thước đo).
// Xem thử: node scripts/ruot-tap/l10-bai33.mjs --hinh (chụp vào out/hinh-l10-bai33/).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const f1 = (v) => (+v).toFixed(1);
const arr = (x1, y1, x2, y2, id, c = INK, dash = '') =>
  `<line x1="${f1(x1)}" y1="${f1(y1)}" x2="${f1(x2)}" y2="${f1(y2)}" stroke="${c}" stroke-width="${SW}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${f1(x1)}" y1="${f1(y1)}" x2="${f1(x2)}" y2="${f1(y2)}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
// lò xo đứng từ (x,y1) xuống (x,y2), n khúc, nửa bề rộng w
const lxD = (x, y1, y2, n = 9, w = 11, c = INK, dash = '') => {
  const a = y1 + 6, b = y2 - 6, h = (b - a) / n;
  let d = `M${f1(x)},${f1(y1)} L${f1(x)},${f1(a)}`;
  for (let i = 0; i < n; i++) d += ` L${f1(x + (i % 2 ? -w : w))},${f1(a + h * (i + 0.5))}`;
  d += ` L${f1(x)},${f1(b)} L${f1(x)},${f1(y2)}`;
  return `<path d="${d}" fill="none" stroke="${c}" stroke-width="2.4"${dash ? ` stroke-dasharray="${dash}"` : ''} stroke-linejoin="round"/>`;
};
// lò xo nằm ngang từ (x1,y) tới (x2,y)
const lxN = (x1, x2, y, n = 9, w = 11, c = INK) => {
  const a = x1 + 6, b = x2 - 6, h = (b - a) / n;
  let d = `M${f1(x1)},${f1(y)} L${f1(a)},${f1(y)}`;
  for (let i = 0; i < n; i++) d += ` L${f1(a + h * (i + 0.5))},${f1(y + (i % 2 ? -w : w))}`;
  d += ` L${f1(b)},${f1(y)} L${f1(x2)},${f1(y)}`;
  return `<path d="${d}" fill="none" stroke="${c}" stroke-width="2.4" stroke-linejoin="round"/>`;
};
const tran = (x1, x2, y) => ln(x1, y, x2, y) + Array.from({ length: Math.floor((x2 - x1) / 16) }, (_, i) =>
  ln(x1 + 4 + i * 16, y, x1 + 12 + i * 16, y - 9, GREY, 1.8)).join('');
const tuong = (x, y1, y2) => ln(x, y1, x, y2) + Array.from({ length: Math.floor((y2 - y1) / 16) }, (_, i) =>
  ln(x, y1 + 4 + i * 16, x - 9, y1 + 12 + i * 16, GREY, 1.8)).join('');
const san = (x1, x2, y) => ln(x1, y, x2, y) + Array.from({ length: Math.floor((x2 - x1) / 16) }, (_, i) =>
  ln(x1 + 12 + i * 16, y, x1 + 4 + i * 16, y + 9, GREY, 1.8)).join('');
const tui = (x, y, s = '200 g', w = 64) => `<rect x="${f1(x - w / 2)}" y="${f1(y)}" width="${w}" height="34" rx="7" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(x, y + 24, s, { a: 'middle' });
const moc = (x, y) => `<path d="M${x},${y} q0,8 -6,8" fill="none" stroke="${INK}" stroke-width="2.4"/>`;
// ngoặc đo chiều dài đứng ở cột x, từ y1 tới y2, nhãn bên phải
const doD = (x, y1, y2, s, c = INK, a = 'start') => ln(x - 5, y1, x + 5, y1, c, 2) + ln(x - 5, y2, x + 5, y2, c, 2) + ln(x, y1, x, y2, c, 2)
  + T(a === 'start' ? x + 7 : x - 7, (y1 + y2) / 2 + 7, s, { c, a });

export const hinhL10b33 = {
  // 1·2 Dự đoán: lò xo 2 túi bị che — không có thước, không vẽ đầu dưới (không lộ đáp án)
  canTreo: (cap = 'Cùng một lò xo: chưa treo, treo 1 túi, treo 2 túi.') => {
    let b = tran(10, 310, 18);
    b += lxD(36, 18, 138) + doD(60, 18, 138, '20 cm');
    b += lxD(146, 18, 150) + moc(146, 150) + tui(140, 158) + doD(176, 18, 150, '22 cm');
    b += lxD(278, 18, 100, 6) + `<rect x="240" y="92" width="76" height="122" rx="10" fill="#eef2fa" stroke="${GREY}" stroke-width="2" stroke-dasharray="6 4"/>`
      + T(278, 150, '?', { size: 40, a: 'middle', w: 700, c: RED }) + T(278, 196, '2 túi', { a: 'middle' });
    b += T(40, 236, 'chưa treo', { a: 'middle' }) + T(140, 236, '1 túi', { a: 'middle' });
    return wrap('0 0 320 246', b, cap, 'Ba lò xo treo, lò xo thứ ba bị che');
  },
  // 1·4 hai thanh: một bị kéo, một bị nén — HS ghi tên dưới (a), (b)
  keoNen: (cap = 'Nét đứt: đầu thanh lúc chưa có lực. Ghi tên biến dạng ở (a), (b).') => {
    let b = defs('kna');
    b += `<rect x="90" y="24" width="140" height="28" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + ln(210, 18, 210, 58, GREY, 2, '5 4');
    b += arr(90, 38, 36, 38, 'kna', RED) + arr(230, 38, 288, 38, 'kna', RED) + T(10, 45, '(a)', { w: 700 });
    b += `<rect x="90" y="96" width="120" height="28" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + ln(230, 90, 230, 130, GREY, 2, '5 4');
    b += arr(36, 110, 88, 110, 'kna', RED) + arr(288, 110, 212, 110, 'kna', RED) + T(10, 117, '(b)', { w: 700 });
    b += T(36, 82, 'F', { c: RED, w: 700 }) + T(282, 82, 'F', { c: RED, a: 'end', w: 700 });
    return wrap('0 0 320 140', b, cap, 'Thanh bị kéo và thanh bị nén');
  },
  // 1·5 lò xo bút bi trước và sau khi kéo mạnh
  butBi: (cap = 'Trước khi kéo (trên); kéo mạnh rồi thả (dưới).') => {
    let b = lxN(20, 150, 30, 14, 10) + lxN(20, 290, 92, 14, 10);
    b += ln(150, 14, 150, 112, GREY, 2, '5 4') + T(154, 128, 'chiều dài cũ', { c: GREY });
    return wrap('0 0 320 136', b, cap, 'Lò xo bút bi trước và sau khi kéo mạnh');
  },
  // 2·1 lực đàn hồi: HS tự vẽ mũi tên lên vật
  lucDH: (cap = 'Vạch đứt: đầu lò xo khi chưa biến dạng. Vẽ mũi tên lực đàn hồi lên vật.') => {
    let b = tuong(24, 10, 190);
    b += lxN(24, 190, 52, 10, 12) + `<rect x="190" y="30" width="54" height="44" rx="3" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(256, 60, '(1)', { w: 700 });
    b += lxN(24, 96, 148, 8, 13) + `<rect x="96" y="126" width="54" height="44" rx="3" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(256, 156, '(2)', { w: 700 });
    b += ln(140, 14, 140, 186, GREY, 2, '5 4');
    return wrap('0 0 320 196', b, cap, 'Lò xo dãn và lò xo nén gắn vật');
  },
  // 3·1 khung đồ thị để HS chấm điểm F theo Δl
  doThi: (cap = 'Chấm 5 điểm (Δl; F) từ bảng, nối thử bằng thước.') => {
    const ox = 56, oy = 206, sx = 24, sy = 72; // 1 cm → 24 đơn vị, 1 N → 72 đơn vị
    let b = defs('dta');
    for (let i = 1; i <= 10; i++) b += ln(ox + i * sx, oy, ox + i * sx, oy - 2.5 * sy - 6, '#d3dbec', 1.4);
    for (let j = 1; j <= 5; j++) b += ln(ox, oy - j * 0.5 * sy, ox + 10 * sx + 4, oy - j * 0.5 * sy, '#d3dbec', 1.4);
    b += arr(ox, oy, ox + 10 * sx + 22, oy, 'dta') + arr(ox, oy, ox, oy - 2.5 * sy - 22, 'dta');
    for (const i of [0, 2, 4, 6, 8, 10]) b += T(ox + i * sx, oy + 24, String(i), { a: 'middle' });
    for (const j of [1, 2]) b += T(ox - 8, oy - j * sy + 7, String(j), { a: 'end' });
    b += T(ox + 10 * sx + 20, oy - 10, `${gk('Δl')} (cm)`, { a: 'end' }) + T(ox + 8, 18, `${gk('F')} (N)`);
    return wrap('0 0 320 238', b, cap, 'Khung đồ thị lực theo độ dãn');
  },
  // lò xo treo một vật: bên trái bóng mờ chiều dài tự nhiên, bên phải lò xo có vật
  treo: ({ l0 = 'l0', l = 'l', m = 'm', h0 = 110, h = 150, cap = '' } = {}) => {
    let b = tran(10, 310, 16);
    b += lxD(112, 16, 16 + h0, 8, 11, GREY, '5 3') + doD(86, 16, 16 + h0, l0, INK, 'end');
    b += lxD(212, 16, 16 + h, 8) + moc(212, 16 + h) + tui(206, 24 + h, m, 74) + doD(254, 16, 16 + h, l);
    return wrap(`0 0 320 ${h + 70}`, b, cap, 'Lò xo treo vật');
  },
  // Dạng 5: hai lần treo, l0 chưa biết
  haiLan: ({ m1 = '160 g', m2 = '480 g', l1 = '24 cm', l2 = '28 cm', cap = '' } = {}) => {
    let b = tran(10, 310, 16);
    b += lxD(60, 16, 146, 8) + moc(60, 146) + tui(54, 154, m1, 74) + doD(106, 16, 146, l1);
    b += lxD(196, 16, 168, 8) + moc(196, 168) + tui(190, 176, m2, 74) + doD(242, 16, 168, l2);
    return wrap('0 0 320 220', b, cap, 'Cùng lò xo, hai lần treo');
  },
  // Dạng 3: lò xo nằm ngang gắn tường, kéo / đẩy đầu tự do
  ngang: ({ l0 = 24, cap = '' } = {}) => {
    let b = defs('nga') + tuong(20, 4, 116);
    b += ln(200, 24, 200, 116, GREY, 2, '5 4') + T(200, 18, `l${sb('0')} = ${l0} cm`, { c: GREY, a: 'middle' });
    b += lxN(20, 236, 44, 11, 10) + arr(236, 44, 300, 44, 'nga', RED) + T(304, 74, 'kéo', { c: RED, a: 'end', w: 700 });
    b += lxN(20, 168, 98, 11, 11) + arr(226, 98, 172, 98, 'nga', RED) + T(232, 105, 'đẩy', { c: RED, w: 700 });
    return wrap('0 0 320 120', b, cap, 'Lò xo ngang gắn tường bị kéo và bị đẩy');
  },
  // Bài tương tự D4·2: lò xo dựng trên bàn, vật đặt lên đầu trên
  nenBan: (cap = '') => {
    let b = san(10, 310, 196);
    b += lxD(70, 66, 196, 8, 12, GREY, '5 3') + T(70, 52, 'chưa đặt vật', { c: GREY, a: 'middle' });
    b += lxD(230, 92, 196, 8, 13) + `<rect x="196" y="58" width="68" height="34" rx="4" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(230, 82, '500 g', { a: 'middle' });
    return wrap('0 0 320 206', b, cap, 'Lò xo dựng đứng bị vật đè');
  },
  // Thử thách ⭐⭐⭐: thang máy đi lên nhanh dần
  thangMay: (cap = 'Thang máy đi lên nhanh dần.') => {
    let b = defs('tma');
    b += `<rect x="40" y="12" width="170" height="212" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += lxD(125, 12, 132, 8) + moc(125, 132) + tui(119, 140, '200 g', 74);
    b += arr(262, 170, 262, 70, 'tma', BLUE) + T(272, 128, `${gk('a')}`, { c: BLUE, w: 700 });
    return wrap('0 0 320 236', b, cap, 'Lò xo treo vật trong thang máy');
  },
};
