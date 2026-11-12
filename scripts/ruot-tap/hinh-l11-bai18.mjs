// Hình minh hoạ cho ruột tập VL11 · Bài 18 Điện trường đều (lesson 37). Cùng quy tắc với hinh.mjs/hinh-l10-bai23.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh (hình Dự đoán, hình hạt bay không vẽ quỹ đạo).
// Xem thử: node scripts/ruot-tap/l11-bai18.mjs --hinh (chụp vào out/hinh-l11-bai18/).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
// chữ Hi Lạp lấy từ KaTeX_Math (Source Sans 3 chỉ nạp latin/vietnamese)
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const f1 = (v) => (+v).toFixed(1);
const arr = (x1, y1, x2, y2, id, c = INK, dash = '', w = SW) =>
  `<line x1="${f1(x1)}" y1="${f1(y1)}" x2="${f1(x2)}" y2="${f1(y2)}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${f1(x1)}" y1="${f1(y1)}" x2="${f1(x2)}" y2="${f1(y2)}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const MINUS = '−';
// hạt mang điện: '+' đỏ đặc, '−' viền xanh
const hat = (x, y, s, r = 10) => s === '+'
  ? `<circle cx="${x}" cy="${y}" r="${r}" fill="${RED}"/>${t(x, y + 6, '+', { c: '#fff', size: 18, a: 'middle', w: 700 })}`
  : `<circle cx="${x}" cy="${y}" r="${r}" fill="#fff" stroke="${BLUE}" stroke-width="${SW}"/>${t(x, y + 6, MINUS, { c: BLUE, size: 20, a: 'middle', w: 700 })}`;
// mũi đo kích thước có hai đầu (nét mảnh xám)
const kt = (x1, y1, x2, y2, id) => `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${GREY}" stroke-width="2" marker-start="url(#${id})" marker-end="url(#${id})"/>`;
const defs2 = (id) => `<defs><marker id="${id}" markerWidth="7" markerHeight="7" refX="3.5" refY="3.5" orient="auto-start-reverse" markerUnits="strokeWidth"><path d="M0,0 L7,3.5 L0,7 z" fill="${GREY}"/></marker></defs>`;

// Hai bản nằm ngang: x1..x2, bản trên ở yT, bản dưới ở yB. tren/duoi: '+' hoặc '−'.
// o.hat: dấu hạt bay vào tại giữa mép trái; o.quy: { dy (độ lệch tại x2, + là xuống), man (x màn), dash, c, keo (kéo ngược nét đứt) }
const haiBan = (o = {}) => {
  const { x1 = 60, x2 = 230, yT = 40, yB = 140, tren = '+', duoi = MINUS, hatS = null, v0 = true, quy = null, man = null,
    duongSuc = false, L = '', d = '', U = '', hoi = '', id = 'hb', W = 320, H = 190, them = '', manTen = 'màn', truc = true } = o;
  const ym = (yT + yB) / 2;
  let b = defs(id + 'a') + defs(id + 'b') + defs2(id + 'k');
  const ban = (y, s) => {
    const c = s === '+' ? RED : BLUE;
    let r = `<rect x="${x1}" y="${y - 4}" width="${x2 - x1}" height="8" fill="#e4e9f4" stroke="${INK}" stroke-width="2.2"/>`;
    const ys = y < ym ? y - 10 : y + 24;
    for (let x = x1 + 14; x < x2 - 6; x += 32) r += t(x, ys, s, { c, size: 22, a: 'middle', w: 700 });
    return r;
  };
  b += ban(yT, tren) + ban(yB, duoi);
  if (duongSuc) {
    const xuong = tren === '+';
    for (let x = x1 + 30; x < x2 - 10; x += 36) b += xuong ? arr(x, yT + 8, x, yB - 10, id + 'b', GREY, '', 2) : arr(x, yB - 8, x, yT + 10, id + 'b', GREY, '', 2);
  }
  if (man) b += ln(man, yT - 30, man, yB + 30, INK, 4) + T(man - 10, yB + 28, manTen, { a: 'end', size: 20 });
  if (quy) {
    const { dy, dash = '', c = RED, keo = false } = quy;
    const xm = (x1 + x2) / 2;
    b += `<path d="M${x1},${ym} Q${xm},${ym} ${x2},${f1(ym + dy)}" fill="none" stroke="${c}" stroke-width="${SW}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
    if (man) { const k = dy / (x2 - xm), ye = ym + dy + k * (man - x2); b += ln(x2, ym + dy, man, ye, c, SW, dash); b += `<circle cx="${man}" cy="${f1(ye)}" r="5" fill="${c}"/>`;
      if (quy.Y) b += kt(man - 14, ym, man - 14, ye + 4, id + 'k') + T(man - 22, (ym + ye) / 2 + 12, quy.Y, { a: 'end', w: 700, c: RED }); }
    if (keo) b += ln(xm, ym, x2, ym + dy, GREY, 2, '4 4');
  }
  if (hatS) {
    if (truc) b += ln(x1 - 2, ym, (man ?? x2 + 40), ym, GREY, 1.8, '3 5');
    b += hat(x1 - 30, ym, hatS);
    if (v0) b += arr(x1 - 18, ym, x1 + 22, ym, id + 'a', INK) + T(x1 - 40, ym - 16, `v${sb('0')}`, { w: 700 });
  }
  if (L) b += kt(x1, yB + 36, x2, yB + 36, id + 'k') + T((x1 + x2) / 2, yB + 60, L, { a: 'middle' });
  if (d) b += kt(x2 + 14, yT, x2 + 14, yB, id + 'k') + T(x2 + 22, ym + 7, d);
  if (U) b += T(x1 - 50, yT + 6, U, { a: 'start' });
  if (hoi) b += T(x2 + 22, ym - 24, hoi, { w: 700, c: RED });
  return { b: b + them, vb: `0 0 ${W} ${H}` };
};
const fig = (o, cap, label) => { const { b, vb } = haiBan(o); return wrap(vb, b, cap, label); };

export const hinhL11b18 = {
  // ===== Trang 1 =====
  // Dự đoán: KHÔNG vẽ quỹ đạo (lộ đáp án)
  mayIn: (cap = 'Giọt mực mang điện âm bay ngang vào khe. Bỏ qua trọng lực.') => {
    let b = defs('mi');
    b += `<rect x="4" y="74" width="40" height="40" rx="4" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(24, 136, 'đầu in', { a: 'middle', size: 18 });
    const bb = haiBan({ x1: 90, x2: 220, yT: 44, yB: 144, hatS: MINUS, id: 'mi1', truc: false }).b;
    b += bb;
    b += `<rect x="286" y="34" width="26" height="120" rx="3" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(299, 178, 'lon', { a: 'middle', size: 18 });
    b += T(254, 102, '?', { a: 'middle', size: 30, w: 700, c: RED });
    return wrap('0 0 320 186', b, cap, 'Giọt mực bay vào khe giữa hai bản tích điện');
  },
  // II.1: HS tự vẽ đường sức
  veDuongSuc: (cap = 'Vẽ 5 đường sức giữa hai bản, cả chỗ gần mép.') => fig({ x1: 40, x2: 280, yT: 40, yB: 150, H: 180 }, cap, 'Hai bản trống để vẽ đường sức'),
  // TN hạt bột: nhìn từ trên xuống, hai lá đồng, hạt rải rác (chưa xếp)
  hatBot: (cap = 'Trước khi quay: bột nằm lộn xộn.') => {
    let b = `<rect x="8" y="10" width="304" height="150" rx="10" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<rect x="96" y="34" width="10" height="102" fill="#e4e9f4" stroke="${INK}" stroke-width="2.2"/><rect x="214" y="34" width="10" height="102" fill="#e4e9f4" stroke="${INK}" stroke-width="2.2"/>`;
    b += T(101, 28, '+', { a: 'middle', c: RED, w: 700, size: 22 }) + T(219, 28, MINUS, { a: 'middle', c: BLUE, w: 700, size: 22 });
    let s = 7;
    const r = () => (s = (s * 9301 + 49297) % 233280) / 233280;
    for (let i = 0; i < 70; i++) { const x = 20 + r() * 280, y = 20 + r() * 130, a = r() * 180; if (y > 132 && x > 225) continue; b += `<rect x="${f1(x - 4)}" y="${f1(y - 1.5)}" width="8" height="3" fill="${GREY}" transform="rotate(${f1(a)} ${f1(x)} ${f1(y)})"/>`; }
    b += kt(106, 148, 214, 148, 'hbk') + defs2('hbk') + T(250, 155, '4 cm', { a: 'middle' });
    return wrap('0 0 320 166', b, cap, 'Khay dầu có bột và hai lá đồng nhìn từ trên');
  },

  // ===== Trang 2 =====
  giayDan: (cap = 'Que dương cách thanh âm x.') => {
    let b = defs('gd') + defs2('gdk');
    b += `<rect x="10" y="10" width="300" height="140" fill="#fff" stroke="${GREY}" stroke-width="2"/>`;
    b += `<rect x="40" y="22" width="12" height="116" fill="#e4e9f4" stroke="${INK}" stroke-width="2.2"/><rect x="268" y="22" width="12" height="116" fill="#e4e9f4" stroke="${INK}" stroke-width="2.2"/>`;
    b += T(46, 172, MINUS, { a: 'middle', c: BLUE, w: 700, size: 24 }) + T(274, 172, '+', { a: 'middle', c: RED, w: 700, size: 24 });
    b += `<circle cx="160" cy="80" r="6" fill="${INK}"/>`;
    b += kt(52, 112, 160, 112, 'gdk') + T(106, 134, 'x', { a: 'middle', w: 700 });
    b += `<circle cx="160" cy="44" r="18" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(160, 51, 'V', { a: 'middle', w: 700 });
    b += ln(160, 62, 160, 74, INK, 2) + ln(142, 44, 52, 44, INK, 2);
    b += T(160, 190, `d = 6,0 cm · U = 9,0 V`, { a: 'middle' });
    return wrap('0 0 320 196', b, cap, 'Giấy dẫn điện, hai thanh đồng và que đo');
  },
  // II.3: hạt bay vào tại O, HS tự vẽ quỹ đạo — không vẽ quỹ đạo
  hatBay: (cap = 'Vẽ quỹ đạo proton (nét liền) và electron (nét đứt) bay vào tại O.') => {
    const { b, vb } = haiBan({ x1: 70, x2: 270, yT: 34, yB: 154, duongSuc: true, H: 190, id: 'hby',
      them: T(62, 88, 'O', { a: 'end', w: 700 }) });
    const d0 = defs('hby2');
    return wrap(vb, d0 + b + `<circle cx="70" cy="94" r="5" fill="${INK}"/>` + arr(70, 94, 120, 94, 'hby2', INK) + T(118, 118, `v${sb('0')}`, { w: 700 }), cap, 'Hai bản có đường sức, điểm vào O');
  },

  // ===== Trang 3 =====
  ongLech: (cap = 'U = 0: vệt sáng ở giữa màn. Tăng U, gấp đôi U, đảo cực?') => {
    let b = `<rect x="4" y="76" width="56" height="36" rx="4" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(32, 136, 'súng', { a: 'middle', size: 18 });
    b += haiBan({ x1: 100, x2: 210, yT: 50, yB: 138, id: 'ol', tren: '?', duoi: '?' }).b.replace(/fill="#b3261e"|fill="#1f5fa8"/g, `fill="${GREY}"`);
    b += ln(60, 94, 300, 94, BLUE, SW, '8 5');
    b += ln(300, 24, 300, 164, INK, 5) + `<circle cx="300" cy="94" r="6" fill="${BLUE}"/>` + T(300, 186, 'màn', { a: 'middle', size: 18 });
    return wrap('0 0 320 192', b, cap, 'Ống lệch tia điện tử');
  },

  // ===== Trang 4 · Bài toán mẫu (đúng tỉ lệ: 1 cm = 40 đơn vị) =====
  baiMau: (cap = 'Đúng tỉ lệ. Cách bản trên bao nhiêu mm?') =>
    fig({ x1: 60, x2: 260, yT: 56, yB: 136, hatS: MINUS, L: ' ', d: ' ', hoi: '', U: '', H: 178, id: 'bm',
      them: T(160, 126, 'L = 5,0 cm', { a: 'middle', size: 18, c: GREY }) + T(282, 94, '2,0', { size: 18 }) + T(282, 114, 'cm', { size: 18 }) + T(160, 22, 'U = 91 V', { a: 'middle' }) }, cap, 'Electron bay vào giữa hai bản, đúng tỉ lệ'),

  // ===== Trang 5 · Thử thách ⭐⭐⭐ =====
  manHinh: (cap = 'Ra khỏi bản: đi thẳng tới màn. Y = ?') =>
    fig({ x1: 50, x2: 150, yT: 60, yB: 128, hatS: MINUS, man: 300, quy: { dy: -14, c: BLUE, Y: 'Y' }, H: 196, id: 'mh',
      them: kt(150, 182, 300, 182, 'mhk') + T(225, 176, 'D', { a: 'middle', w: 700 }) }, cap, 'Electron ra khỏi hai bản rồi tới màn'),

  // ===== Bài tập mẫu =====
  d3Cham: (cap = 'Đi hết L thì lệch bao nhiêu?') =>
    fig({ x1: 60, x2: 250, yT: 32, yB: 98, tren: MINUS, duoi: '+', hatS: MINUS, L: '', d: '1,0 cm', H: 126, W: 340, id: 'd3', them: T(155, 89, 'L = 4,5 cm', { a: 'middle', size: 18, c: GREY }) }, cap, 'Electron bay vào giữa hai bản, bản dưới dương'),
  d4Giay: (cap = 'Trong bản: parabol. Ngoài bản: thẳng. Y = ?') =>
    fig({ x1: 50, x2: 150, yT: 60, yB: 128, hatS: MINUS, man: 300, quy: { dy: -12, c: BLUE, Y: 'Y' }, manTen: 'giấy', H: 196, id: 'd4',
      them: kt(150, 182, 300, 182, 'd4k') + T(225, 176, 'D', { a: 'middle', w: 700 }) }, cap, 'Giọt mực ra khỏi hai bản tới giấy'),
  d5SuotMep: (cap = 'Giới hạn: vừa sượt mép bản ở cuối đường bay.') =>
    fig({ x1: 60, x2: 250, yT: 44, yB: 124, hatS: MINUS, quy: { dy: -40, c: BLUE, dash: '7 5' }, L: 'L', H: 190, id: 'd5',
      them: kt(264, 44, 264, 84, 'd5k') + T(272, 72, 'd/2', { w: 700 }) }, cap, 'Electron vừa sượt mép bản trên'),
};
