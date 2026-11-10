// Hình minh hoạ cho ruột tập VL10 · Bài 23 Năng lượng. Công cơ học (lesson 68). Cùng quy tắc với hinh.mjs/hinh-ch4.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh. Xem thử: node scripts/ruot-tap/l10-bai23.mjs --hinh (chụp vào out/hinh-l10-bai23/).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
// chữ Hi Lạp: Source Sans 3 chỉ nạp latin/vietnamese, α θ rơi về Helvetica → lấy từ KaTeX_Math (đã nạp qua katex.min.css)
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const arr = (x1, y1, x2, y2, id, c = INK, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${SW}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const R = (d) => (d * Math.PI) / 180;
const f1 = (v) => v.toFixed(1);
// cung góc tâm (x,y), bán kính r, từ góc a1 tới a2 (độ, ngược chiều kim đồng hồ theo toán học, y hướng xuống nên đổi dấu)
const cung = (x, y, r, a1, a2, c = INK) => {
  const p = (a) => `${f1(x + r * Math.cos(R(a)))},${f1(y - r * Math.sin(R(a)))}`;
  return `<path d="M${p(a1)} A${r},${r} 0 0 0 ${p(a2)}" fill="none" stroke="${c}" stroke-width="2.2"/>`;
};
// người que: đầu tại (x,y)
const nguoi = (x, y, { tay = '' } = {}) => `<circle cx="${x}" cy="${y}" r="11" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
  + ln(x, y + 11, x, y + 62) + ln(x, y + 62, x - 14, y + 104) + ln(x, y + 62, x + 14, y + 104) + tay;
const dat = (x1, x2, y) => ln(x1, y, x2, y) + Array.from({ length: Math.floor((x2 - x1) / 18) }, (_, i) =>
  ln(x1 + 8 + i * 18, y, x1 + i * 18, y + 8, GREY, 1.8)).join('');
const xe = (x, y, w = 64, h = 30) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="4" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
  + `<circle cx="${x + 13}" cy="${y + h + 7}" r="7" fill="#fff" stroke="${INK}" stroke-width="${SW}"/><circle cx="${x + w - 13}" cy="${y + h + 7}" r="7" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;

// Dốc nghiêng thật 30° (hoặc góc khác): chân (x0,y0), dài L đơn vị. Tuỳ chọn nhãn và lực.
const doc = (o = {}) => {
  const { goc = 30, s = 's', h = 'h', th = gk('θ'), vat = 'hop', F = false, P = true, N = false, ms = false, chieu = 'len', mui = true, cap = '', id = 'dc' } = o;
  const x0 = 20, y0 = 182, L = 256, c = Math.cos(R(goc)), sn = Math.sin(R(goc));
  const x1 = x0 + L * c, y1 = y0 - L * sn;
  let b = defs(id + 'a') + defs(id + 'b') + defs(id + 'c');
  b += `<path d="M${x0},${y0} L${f1(x1)},${f1(y1)} L${f1(x1)},${y0} z" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
  b += cung(x0, y0, 44, 0, goc) + T(x0 + 52, y0 - 8, th);
  b += ln(x1 + 12, y1, x1 + 12, y0, GREY, 2, '5 4') + T(x1 + 18, (y1 + y0) / 2 + 22, h);
  // vật ở giữa dốc, đáy nằm trên mặt dốc
  const u = 0.48, bx = x0 + L * u * c, by = y0 - L * u * sn, w = 48, hh = 30;
  const g = `transform="rotate(${-goc} ${f1(bx)} ${f1(by)})"`;
  b += vat === 'xe'
    ? `<g ${g}><rect x="${f1(bx - w / 2)}" y="${f1(by - hh - 10)}" width="${w}" height="${hh - 4}" rx="4" fill="#fff" stroke="${INK}" stroke-width="${SW}"/><circle cx="${f1(bx - 13)}" cy="${f1(by - 7)}" r="6" fill="#fff" stroke="${INK}" stroke-width="${SW}"/><circle cx="${f1(bx + 13)}" cy="${f1(by - 7)}" r="6" fill="#fff" stroke="${INK}" stroke-width="${SW}"/></g>`
    : `<g ${g}><rect x="${f1(bx - w / 2)}" y="${f1(by - hh)}" width="${w}" height="${hh}" rx="3" fill="#fff" stroke="${INK}" stroke-width="${SW}"/></g>`;
  const cx = bx - (hh / 2) * sn, cy = by - (hh / 2) * c; // tâm vật
  // nhãn s dọc mặt dốc, phía dưới-phải
  b += T(x0 + L * 0.7 * c + 4, y0 - L * 0.7 * sn + 30, s);
  if (P) b += arr(f1(cx), f1(cy), f1(cx), f1(cy + 62), id + 'a', RED) + T(cx + 8, cy + 62, 'P', { c: RED, w: 700 });
  if (N) b += arr(f1(cx), f1(cy), f1(cx - 48 * sn), f1(cy - 48 * c), id + 'a', INK) + T(cx - 48 * sn - 22, cy - 48 * c, 'N', { w: 700 });
  if (F) { const ex = cx + 22 * c, ey = cy - 22 * sn; b += arr(f1(ex), f1(ey), f1(ex + 70 * c), f1(ey - 70 * sn), id + 'b', RED) + T(ex + 70 * c - 6, ey - 70 * sn - 10, 'F', { c: RED, w: 700, a: 'end' }); }
  if (ms) { const dir = chieu === 'len' ? -1 : 1, ex = cx + dir * 26 * c, ey = cy - dir * 26 * sn - 4; b += arr(f1(ex), f1(ey), f1(ex + dir * 52 * c), f1(ey - dir * 52 * sn), id + 'c', INK, '6 4') + T(ex + dir * 52 * c + (dir > 0 ? 4 : -4), ey - dir * 52 * sn - 12, `F${sb('ms')}`, { a: dir > 0 ? 'start' : 'end' }); }
  if (mui) { // chiều chuyển động: mũi tên song song dốc, phía trên
    const ox = -14 * sn, oy = -14 * c - 38, a0 = chieu === 'len' ? 0.18 : 0.36, a1 = chieu === 'len' ? 0.36 : 0.18;
    b += arr(f1(x0 + L * a0 * c + ox), f1(y0 - L * a0 * sn + oy), f1(x0 + L * a1 * c + ox), f1(y0 - L * a1 * sn + oy), id + 'c', BLUE, '6 4');
  }
  return wrap('0 0 320 196', b, cap, 'Vật trên mặt dốc nghiêng');
};

// Ba (hay n) ô: cùng d nằm ngang, đổi hướng F
const baGoc = (gocs, cap, duoi = (g) => 'A ? 0', id = 'bg') => {
  let b = defs(id + 'a') + defs(id + 'b');
  gocs.forEach((g, i) => {
    const ox = 12 + i * 124, oy = 104;
    b += arr(ox, oy, ox + 78, oy, id + 'a', INK) + T(ox + 66, oy + 26, 'd', { w: 700 });
    const ex = ox + 64 * Math.cos(R(g)), ey = oy - 64 * Math.sin(R(g));
    b += arr(ox, oy, f1(ex), f1(ey), id + 'b', RED) + T(ex + (g > 100 ? -6 : 6), ey - 2, 'F', { c: RED, w: 700, a: g > 100 ? 'end' : 'start' });
    b += g === 90 ? `<path d="M${ox + 12},${oy} L${ox + 12},${oy - 12} L${ox},${oy - 12}" fill="none" stroke="${INK}" stroke-width="2"/>` : cung(ox, oy, 20, 0, g);
    b += T(ox + 34 * Math.cos(R(g / 2)) + (g > 100 ? -6 : 2), oy - 34 * Math.sin(R(g / 2)) + 4, `${g}°`, { a: g > 100 ? 'middle' : 'start' });
    b += T(ox + 41, 146, duoi(g), { a: 'middle', w: 700 });
  });
  return wrap(`0 0 ${gocs.length * 124 - 6} 156`, b, cap, 'Cùng độ dịch chuyển, đổi hướng lực');
};

// Ván/thùng trên mặt ngang, lực kéo chếch góc goc, đủ bốn lực
const vanTruot = (cap, { F = 'F', goc = '30°', xuong = false, id = 'vt' } = {}) => {
  let b = defs(id + 'a') + defs(id + 'b') + defs(id + 'c');
  b += dat(10, 312, 140);
  b += `<rect x="96" y="104" width="112" height="36" rx="4" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
  const cx = 152, cy = 122;
  if (!xuong) {
    b += arr(208, 112, f1(208 + 84 * Math.cos(R(30))), f1(112 - 84 * Math.sin(R(30))), id + 'a', RED) + T(286, 56, F, { c: RED, w: 700, a: 'end' });
    b += ln(208, 112, 296, 112, GREY, 2, '5 4') + cung(208, 112, 34, 0, 30) + T(248, 106, goc, { size: 20 });
  } else {
    const x0 = 96 - 84 * Math.cos(R(30)), y0 = 104 - 84 * Math.sin(R(30));
    b += arr(f1(x0), f1(y0), 96, 104, id + 'a', RED) + T(x0 - 2, y0 - 6, F, { c: RED, w: 700 });
    b += ln(10, 104, 96, 104, GREY, 2, '5 4') + T(30, 98, goc, { size: 20 });
  }
  b += arr(cx, cy, cx, 192, id + 'b', RED) + T(cx + 8, 190, 'P', { c: RED, w: 700 });
  b += arr(cx, 104, cx, xuong ? 36 : 52, id + 'b', INK) + T(cx - 8, xuong ? 44 : 60, 'N', { w: 700, a: 'end' });
  b += arr(96, 130, 40, 130, id + 'c', INK, '6 4') + T(14, 122, `F${sb('ms')}`);
  b += arr(214, 166, 300, 166, id + 'c', BLUE, '6 4') + T(300, 190, 'hướng đi', { c: BLUE, a: 'end', size: 20 });
  return wrap('0 0 320 200', b, cap, 'Các lực tác dụng lên vật kéo trên mặt ngang');
};

export const hinhL10b23 = {
  // Trang 1 · Dự đoán: Minh giữ ba lô, Lan đẩy Hà
  sanBang: (cap = 'Minh giữ ba lô 5 phút. Lan đẩy Hà rồi buông, Hà lướt 3 m.') => {
    let b = defs('sb1') + defs('sb2');
    b += dat(6, 314, 160);
    b += nguoi(52, 50, { tay: ln(52, 78, 74, 92) }) + `<rect x="70" y="84" width="30" height="34" rx="5" fill="${GREY}" stroke="${INK}" stroke-width="${SW}"/>`;
    b += T(52, 30, 'Minh', { a: 'middle', w: 700 }) + T(86, 146, '6 kg', { a: 'middle', size: 20 });
    b += ln(132, 20, 132, 150, GREY, 2, '4 4');
    b += nguoi(176, 50, { tay: ln(176, 80, 206, 84) }) + T(176, 30, 'Lan', { a: 'middle', w: 700 });
    b += nguoi(222, 50, { tay: ln(222, 76, 236, 98) }) + T(222, 30, 'Hà', { a: 'middle', w: 700 }) + ln(198, 160, 248, 160, INK, 5);
    b += arr(250, 120, 310, 120, 'sb2', BLUE, '6 4') + T(282, 110, '3 m', { c: BLUE, a: 'middle' });
    return wrap('0 0 320 172', b, cap, 'Hai cảnh ở sân băng');
  },
  // Trang 1 · thí nghiệm: bóng nảy thấp dần
  bongNay: (cap = 'Mỗi lần nảy, bóng lên thấp hơn. Phần thiếu đi đâu?') => {
    let b = dat(56, 316, 170);
    b += ln(44, 20, 44, 170) + [0, 1, 2, 3, 4].map((k) => ln(44, 170 - k * 37, 54, 170 - k * 37, INK, 2)).join('') + T(4, 28, '1 m');
    const peaks = [148, 108, 78, 56, 40]; // độ cao (đơn vị vẽ)
    let x = 76, d = `M76,22 Q80,96 88,${170}`;
    x = 88;
    peaks.slice(1).forEach((hp, i) => { const w = 60 - i * 8; d += ` Q${x + w / 2},${170 - 2 * hp} ${x + w},170`; x += w; });
    b += `<path d="${d}" fill="none" stroke="${INK}" stroke-width="2.4" stroke-dasharray="5 4"/>`;
    b += `<circle cx="76" cy="22" r="9" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    let xx = 88; peaks.slice(1).forEach((hp, i) => { const w = 60 - i * 8; b += `<circle cx="${xx + w / 2}" cy="${170 - hp - 9}" r="8" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`; xx += w; });
    b += T(316, 156, '“bộp”', { a: 'end', c: RED });
    return wrap('0 0 320 182', b, cap, 'Quả bóng nảy thấp dần');
  },
  // Trang 2 · phần nào của lực sinh công
  phanTichLuc: (cap = 'Lực F chếch lên so với đường đi. Phần nào của F kéo vật dọc đường đi?') => {
    let b = defs('pt1') + defs('pt2') + defs('pt3');
    b += dat(8, 312, 140);
    b += `<rect x="48" y="96" width="82" height="44" rx="4" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    const ox = 130, oy = 108, L = 124, ex = ox + L * Math.cos(R(32)), ey = oy - L * Math.sin(R(32));
    b += arr(ox, oy, f1(ex), f1(ey), 'pt1', RED) + T(ex - 4, ey - 6, 'F', { c: RED, w: 700, a: 'end' });
    b += arr(ox, oy, f1(ex), oy, 'pt2', BLUE, '6 4') + ln(f1(ex), f1(ey), f1(ex), oy, GREY, 2, '4 4') + T(ex + 6, oy + 6, '?', { c: BLUE, w: 700 });
    b += cung(ox, oy, 40, 0, 32) + T(ox + 46, oy - 8, gk('α'));
    b += arr(48, 166, 220, 166, 'pt3', INK) + T(232, 172, 'd');
    return wrap('0 0 320 180', b, cap, 'Phân tích lực xiên góc');
  },
  // Trang 2 · dấu của công theo góc
  dauCong: (cap = 'Cùng d, đổi hướng F. Điền &gt;, = hay &lt; vào chỗ “?”.') => baGoc([45, 90, 135], cap),
  // Trang 2 · công của trọng lực lên/xuống dốc
  docTrongLuc: (cap = 'Vật đi lên hay đi xuống dốc: công của P mang dấu gì, tính theo s hay h?') => doc({ cap, id: 'dtl', chieu: 'len', mui: true }),
  // Trang 3 · thí nghiệm kéo xe lên mặt nghiêng
  keoXe: (cap = 'Kéo đều xe P = 2,0 N lên cao h = 0,20 m theo mặt nghiêng dài s.') => doc({ cap, id: 'kx', vat: 'xe', goc: 15, s: 's', h: 'h', th: '', F: true, P: true, mui: false }),
  // Trang 3 · bẫy 1: xách xô đi ngang
  xachXo: (cap = 'Xách xô đi ngang, xô giữ ở độ cao không đổi.') => {
    let b = defs('xx1') + defs('xx2');
    b += dat(8, 312, 172);
    b += nguoi(80, 50, { tay: ln(80, 80, 110, 104) }) + ln(66, 154, 56, 172) + ln(94, 154, 104, 172);
    b += `<path d="M98,106 L130,106 L126,140 L102,140 z" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += arr(114, 100, 114, 30, 'xx1', RED) + T(124, 40, `F${sb('tay')}`, { c: RED, w: 700 });
    b += arr(150, 120, 290, 120, 'xx2', BLUE, '6 4') + T(220, 110, 'd', { c: BLUE, a: 'middle', w: 700 });
    b += T(220, 154, `${gk('α')} = ?`, { a: 'middle', w: 700 });
    return wrap('0 0 320 182', b, cap, 'Xách xô đi ngang');
  },
  // Trang 4 · bài toán mẫu: các lực lên ván trượt
  vanTruot: (cap = 'Các lực lên ván: F chếch lên 30°, P, N, F<sub>ms</sub>. Lực nào vuông góc với hướng đi?') => vanTruot(cap, { F: 'F = 40 N' }),
  // Trang 5 · thử thách ★★★: vật trượt xuống dốc có ma sát
  docTruot: (cap = 'Trượt xuống dốc: đánh dấu lực nào sinh công dương, âm, bằng 0.') => doc({ cap, id: 'dtr', chieu: 'xuong', N: true, ms: true, s: '4 m', th: '30°', h: '' }),

  // ===== Bài tập mẫu =====
  mayXay: (cap = 'Năng lượng vào bằng tổng năng lượng ra.') => {
    let b = '';
    b += `<rect x="110" y="48" width="84" height="70" rx="6" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(152, 90, 'máy', { a: 'middle', w: 700 });
    const mui = (x1, y1, x2, y2, w, c, dash = '') => { const a = Math.atan2(y2 - y1, x2 - x1), k = 16, q = 10;
      const bx = x2 - k * Math.cos(a), by = y2 - k * Math.sin(a);
      return `<line x1="${x1}" y1="${y1}" x2="${f1(bx)}" y2="${f1(by)}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`
        + `<path d="M${x2},${y2} L${f1(bx - q * Math.sin(a))},${f1(by + q * Math.cos(a))} L${f1(bx + q * Math.sin(a))},${f1(by - q * Math.cos(a))} z" fill="${c}"/>`; };
    b += mui(8, 83, 108, 83, 7, RED) + T(8, 64, 'điện 300 J', { c: RED, w: 700 });
    b += mui(196, 70, 300, 52, 5, INK) + T(316, 34, 'động năng 240 J', { a: 'end' });
    b += mui(196, 98, 300, 118, 3, GREY, '6 4') + T(316, 150, 'nhiệt + âm: ?', { a: 'end', w: 700 });
    return wrap('0 0 320 166', b, cap, 'Dòng năng lượng qua máy xay');
  },
  xeDay: (cap = 'Xe đi thẳng đều: so độ lớn F và F<sub>c</sub>.') => {
    let b = defs('xd1') + defs('xd2') + defs('xd3');
    b += dat(8, 312, 124) + xe(120, 72, 80, 38);
    b += arr(200, 90, 290, 90, 'xd1', RED) + T(296, 76, 'F = 25 N', { c: RED, w: 700, a: 'end' });
    b += arr(120, 100, 40, 100, 'xd2', INK, '6 4') + T(10, 86, `F${sb('c')} = ?`);
    b += arr(60, 150, 260, 150, 'xd3', BLUE) + T(160, 176, 's = 12 m', { c: BLUE, a: 'middle' });
    return wrap('0 0 320 184', b, cap, 'Xe đẩy trên sàn ngang');
  },
  baGoc3: (cap = 'Cùng F = 70 N, cùng s = 8,0 m.') => baGoc([60, 90, 120], cap, () => 'A = ?', 'bg3'),
  docD4: (cap = 'Lên rồi xuống cùng đoạn dốc: so công của P và của F<sub>ms</sub>.') => doc({ cap, id: 'd4', s: '6,0 m', th: '30°', h: 'h = ?', ms: true, chieu: 'len' }),
  thungKeo: (cap = 'N + F sin 30° = P: N lớn hơn hay nhỏ hơn P?') => vanTruot(cap, { F: '100 N', id: 'tk' }),
  // ===== Bài tương tự =====
  baGocTT: (cap = 'F = 50 N, s = 10 m.') => baGoc([30, 90, 150], cap, () => 'A = ?', 'bgt'),
  docTT: (cap = 'Dốc dài 8,0 m, nghiêng 30°.') => doc({ cap, id: 'dtt', s: '8,0 m', th: '30°', h: 'h = ?', ms: true, chieu: 'xuong' }),
};
