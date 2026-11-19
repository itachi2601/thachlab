// Hình minh hoạ cho ruột tập VL11 · Bài 1 Dao động điều hoà (lesson 20). Cùng quy tắc với hinh.mjs/hinh-l10-bai23.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh. Đồ thị x–t có lưới + số trên trục để đọc được A, T, x(0).
// Xem thử: node scripts/ruot-tap/l11-bai1.mjs --hinh (chụp vào out/hinh-l11-bai1/).
import { ve } from './hinh.mjs';
import { m } from './khung.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
// chữ Hi Lạp: Source Sans 3 chỉ nạp latin/vietnamese → lấy từ KaTeX_Math (đã nạp qua katex.min.css)
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const it = (ch) => `<tspan font-style="italic">${ch}</tspan>`;
const arr = (x1, y1, x2, y2, id, c = INK, dash = '', w = SW) =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const R = (d) => (d * Math.PI) / 180;
const f1 = (v) => (Math.round(v * 10) / 10).toString();
const so = (v) => String(v).replace('.', ',');
// cung tâm (x,y) bán kính r từ góc a1 tới a2 (độ, ngược chiều kim đồng hồ), có thể gắn mũi tên ở cuối
const cung = (x, y, r, a1, a2, c = INK, w = 2.2, id = '') => {
  const p = (a) => `${f1(x + r * Math.cos(R(a)))},${f1(y - r * Math.sin(R(a)))}`;
  const big = Math.abs(a2 - a1) > 180 ? 1 : 0;
  return `<path d="M${p(a1)} A${r},${r} 0 ${big} 0 ${p(a2)}" fill="none" stroke="${c}" stroke-width="${w}"${id ? ` marker-end="url(#${id})"` : ''}/>`;
};
const lxo = (x1, x2, y, n = 9, h = 10) => {
  const d = (x2 - x1) / (n * 2);
  let s = `M${x1},${y}`;
  for (let i = 0; i < n * 2; i++) s += ` L${f1(x1 + d * (i + 1))},${y + (i % 2 ? h : -h)}`;
  return `<path d="${s} L${x2},${y}" fill="none" stroke="${INK}" stroke-width="2.4"/>`;
};

// Đồ thị li độ – thời gian, có lưới. A (cm), T (s), phi (rad), tMax (s), dt: bước lưới t, lt: bước nhãn t, dx: bước lưới x.
const doThi = ({ A, Tc, phi, tMax, dt, lt, dx = 1, cap, id, nhanX = [A, -A], H = 74 }) => {
  const x0 = 56, x1 = 304, y0 = 38 + H, sx = (x1 - x0) / tMax, sy = H / A;
  const P = (tt) => x0 + tt * sx, Y = (x) => y0 - x * sy;
  let b = defs(id);
  for (let k = -A; k <= A + 1e-9; k += dx) b += ln(x0, f1(Y(k)), x1, f1(Y(k)), '#c9d1e3', 1.4);
  for (let k = 0; k <= tMax + 1e-9; k += dt) b += ln(f1(P(k)), Y(A), f1(P(k)), Y(-A), '#c9d1e3', 1.4);
  b += arr(x0, y0, x1 + 12, y0, id) + arr(x0, Y(-A) + 6, x0, Y(A) - 22, id);
  b += T(x0 + 8, Y(A) - 18, `${it('x')} (cm)`) + T(x1 + 12, y0 + 24, `${it('t')} (s)`, { a: 'end' });
  nhanX.forEach((v) => { b += T(x0 - 6, Y(v) + 7, so(v).replace('-', '−'), { a: 'end' }); });
  b += T(x0 - 6, y0 + 7, '0', { a: 'end' });
  for (let k = lt; k <= tMax + 1e-9; k += lt) { const kk = Math.round(k * 1000) / 1000; b += T(P(kk), Y(-A) + 22, so(kk), { a: 'middle' }); }
  let d = '';
  for (let i = 0; i <= 160; i++) { const tt = (tMax * i) / 160; d += `${i ? ' L' : 'M'}${f1(P(tt))},${f1(Y(A * Math.cos((2 * Math.PI / Tc) * tt + phi)))}`; }
  b += `<path d="${d}" fill="none" stroke="${RED}" stroke-width="${SW}"/>`;
  return wrap(`0 0 320 ${68 + 2 * H}`, b, cap, 'Đồ thị li độ theo thời gian');
};

// Chuyển động tròn đều: M ở góc g (độ), hình chiếu Q lên Ox. phi: vẽ cung góc từ Ox tới OM; nhanPhi: chữ cạnh cung.
const tron = ({ g = 50, phi = true, nhanPhi = gk('φ'), R0 = 'A', cap, id, ox = true }) => {
  const cx = 150, cy = 112, r = 80, mx = cx + r * Math.cos(R(g)), my = cy - r * Math.sin(R(g));
  let b = defs(id) + defs(id + 'w');
  b += `<circle cx="${cx}" cy="${cy}" r="${r}" fill="none" stroke="${INK}" stroke-width="2.4"/>`;
  b += arr(cx - r - 26, cy, cx + r + 34, cy, id) + T(cx + r + 34, cy + 26, it('x'), { a: 'end' });
  b += `<circle cx="${cx}" cy="${cy}" r="3.5" fill="${INK}"/>` + T(cx - 8, cy + 24, 'O', { a: 'end' });
  b += ln(cx, cy, f1(mx), f1(my), INK, 2.6) + `<circle cx="${f1(mx)}" cy="${f1(my)}" r="7" fill="${BLUE}"/>`;
  b += T(mx + (Math.cos(R(g)) >= 0 ? 10 : -10), my - 10, 'M', { a: Math.cos(R(g)) >= 0 ? 'start' : 'end', w: 700, c: BLUE });
  if (Math.abs(Math.sin(R(g))) > 0.05) b += ln(f1(mx), f1(my), f1(mx), cy, GREY, 2.2, '6 4');
  b += `<circle cx="${f1(mx)}" cy="${cy}" r="7" fill="#fff" stroke="${RED}" stroke-width="${SW}"/>` + (Math.abs(Math.cos(R(g))) < 0.1 ? T(mx + 12, cy + 28, 'Q', { w: 700, c: RED }) : T(mx, cy + (Math.sin(R(g)) > 0 ? 28 : -14), 'Q', { a: 'middle', w: 700, c: RED }));
  if (R0) { const a = g + 90, rx = cx + (r / 2) * Math.cos(R(g)), ry = cy - (r / 2) * Math.sin(R(g)); b += T(rx + 16 * Math.cos(R(a)), ry - 16 * Math.sin(R(a)) + 7, R0, { a: Math.abs(Math.cos(R(g))) < 0.1 ? 'end' : 'middle' }); }
  if (phi && g > 4) b += cung(cx, cy, 26, 0, g) + T(cx + 36 * Math.cos(R(g / 2)), cy - 36 * Math.sin(R(g / 2)) + 8, nhanPhi);
  b += cung(cx, cy, r + 14, 120, 160, BLUE, 2.4, id + 'w') + T(cx + (r + 26) * Math.cos(R(140)) - 4, cy - (r + 26) * Math.sin(R(140)), gk('ω'), { a: 'end', c: BLUE });
  if (!ox) b += '';
  return wrap('0 0 300 210', b, cap, 'Hình chiếu của chuyển động tròn đều');
};

export const hinhL11b1 = {
  // Trang 1 · Dự đoán: cái đu
  du: (cap = 'Đu đi tới, dừng, quay về, sang phía bên kia… Em bấm giờ.') => {
    let b = defs('du1');
    b += ln(18, 182, 36, 16) + ln(54, 182, 36, 16) + ln(266, 182, 284, 16) + ln(302, 182, 284, 16) + ln(36, 16, 284, 16, INK, 5);
    b += ln(10, 182, 310, 182);
    const O = [160, 18], L = 130;
    [[-28, GREY, '6 4'], [0, GREY, '3 5'], [28, INK, '']].forEach(([a, c, d]) => {
      const x = O[0] + L * Math.sin(R(a)), y = O[1] + L * Math.cos(R(a));
      b += ln(O[0], O[1], f1(x), f1(y), c, 2.4, d) + `<rect x="${f1(x - 20)}" y="${f1(y)}" width="40" height="8" rx="3" fill="${c === INK ? INK : '#fff'}" stroke="${c}" stroke-width="2.4"/>`;
    });
    b += cung(O[0], O[1], L + 22, -116, -64, BLUE, 2.4, 'du1');
    b += T(160, 205, '3 s ?', { a: 'middle', c: BLUE, w: 700 });
    return wrap('0 0 320 212', b, cap, 'Cái đu đi rồi lại về');
  },
  // Trang 1 · thí nghiệm con lắc lò xo nằm ngang
  conLac: (cap = 'Kéo vật lệch rồi thả. Vật đi tới đâu, quay về qua chỗ nào?') => {
    let b = defs('cl1');
    b += ln(20, 30, 20, 120, INK, 4) + ln(20, 120, 312, 120);
    for (let i = 0; i < 6; i++) b += ln(20, 34 + i * 16, 8, 46 + i * 16, GREY, 1.8);
    b += lxo(20, 150, 92, 8, 11);
    b += `<rect x="150" y="70" width="44" height="44" rx="4" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<rect x="236" y="70" width="44" height="44" rx="4" fill="none" stroke="${GREY}" stroke-width="2.2" stroke-dasharray="6 4"/>`;
    b += `<rect x="64" y="70" width="44" height="44" rx="4" fill="none" stroke="${GREY}" stroke-width="2.2" stroke-dasharray="6 4"/>`;
    const tick = (x, s) => ln(x, 132, x, 146) + T(x, 172, s, { a: 'middle' });
    b += ln(86, 139, 258, 139, INK, 2) + tick(86, '−A') + tick(172, 'O') + tick(258, '+A');
    b += arr(204, 52, 268, 52, 'cl1', BLUE, '6 4') + arr(140, 52, 76, 52, 'cl1', BLUE, '6 4');
    return wrap('0 0 320 182', b, cap, 'Con lắc lò xo nằm ngang');
  },
  // Trang 2 · bút vẽ đồ thị trên giấy chạy đều
  butVe: (cap = 'Giấy chạy đều sang trái. Đoạn nào là A, đoạn nào là T?') => {
    let b = defs('bv1') + defs('bv2');
    b += `<rect x="44" y="20" width="218" height="152" fill="#fff" stroke="${GREY}" stroke-width="2"/>`;
    b += ln(44, 96, 262, 96, GREY, 1.6, '4 4');
    let d = ''; for (let i = 0; i <= 109; i++) { const x = 262 - i * 2; d += `${i ? ' L' : 'M'}${x},${f1(96 - 56 * Math.cos((2 * Math.PI * i * 2) / 112))}`; }
    b += `<path d="${d}" fill="none" stroke="${RED}" stroke-width="${SW}"/>`;
    b += `<path d="M262,40 L296,40 L304,26 L304,54 z" fill="#fff" stroke="${INK}" stroke-width="2.4"/>`;
    b += arr(200, 190, 110, 190, 'bv1', BLUE, '6 4') + T(210, 198, 'giấy', { c: BLUE });
    // chỗ "?" cho A và T
    b += ln(28, 40, 28, 96, INK, 2.2) + ln(20, 40, 36, 40, INK, 2) + ln(20, 96, 36, 96, INK, 2) + T(14, 76, '?', { w: 700, a: 'middle' });
    b += ln(94, 30, 206, 30, INK, 2.2) + ln(94, 24, 94, 36, INK, 2) + ln(206, 24, 206, 36, INK, 2) + T(150, 18, '?', { a: 'middle', w: 700 });
    return wrap('0 0 320 206', b, cap, 'Bút gắn vào vật vẽ lên giấy chạy đều');
  },
  // Trang 3 · hình chiếu của chuyển động tròn đều
  tronDeu: (cap = 'M quay đều ngược chiều kim đồng hồ; Q là hình chiếu của M lên Ox.') => tron({ g: 40, cap, id: 'td' }),
  // Trang 4 · bài toán mẫu: φ = π/2 → M lúc t = 0 ở đâu?
  tronMau: (cap = `Lúc t = 0, pha bằng ${m('\\varphi=\\frac{\\pi}{2}')}. Đánh dấu M và Q lúc đó, rồi lúc pha bằng ${m('\\pi')}.`) => {
    const cx = 150, cy = 112, r = 80;
    let b = defs('tm') + defs('tmw');
    b += `<circle cx="${cx}" cy="${cy}" r="${r}" fill="none" stroke="${INK}" stroke-width="2.4"/>`;
    b += arr(cx - r - 26, cy, cx + r + 34, cy, 'tm') + T(cx + r + 34, cy + 26, it('x'), { a: 'end' });
    b += `<circle cx="${cx}" cy="${cy}" r="3.5" fill="${INK}"/>` + T(cx - 8, cy + 24, 'O', { a: 'end' });
    b += T(cx - r - 4, cy + 26, '−6', { a: 'middle' }) + T(cx + r + 2, cy - 10, '+6', { a: 'start' });
    b += ln(cx - r, cy - 6, cx - r, cy + 6, INK, 2.4) + ln(cx + r, cy - 6, cx + r, cy + 6, INK, 2.4);
    b += cung(cx, cy, r + 14, 120, 160, BLUE, 2.4, 'tmw') + T(cx + (r + 26) * Math.cos(R(140)) - 4, cy - (r + 26) * Math.sin(R(140)), gk('ω'), { a: 'end', c: BLUE });
    return wrap('0 0 300 210', b, cap, 'Vòng tròn để đánh dấu M');
  },
  // Trang 5 · thử thách: M từ biên này sang biên kia
  tronTT: (cap = 'Q từ biên này sang biên kia: M quay bao nhiêu?') => tron({ g: 0, phi: false, R0: '10 cm', cap, id: 'tt' }),
  // Trang 6 · Dạng 3: đồ thị x–t xuất phát từ đáy
  doThiD3: (cap = 'Đọc A, T, x(0) trên lưới.') => doThi({ A: 4, Tc: 1, phi: Math.PI, tMax: 1.75, dt: 0.25, lt: 0.5, cap, id: 'd3', nhanX: [4, 2, -2, -4], H: 48 }),
  // Trang 7 · Dạng 4: quỹ đạo thẳng 16 cm, t = 0 ở biên âm
  quyDao: (cap = `Lúc t = 0 vật ở biên âm. ${m('\\cos\\varphi=\\,?')}`) => {
    let b = defs('qd1');
    const xa = 40, xo = 160, xb = 280, y = 96;
    b += ln(xa, y, xb, y, INK, 2.4) + arr(xb, y, 312, y, 'qd1') + T(312, y + 28, it('x'), { a: 'end' });
    [[xa, '−A'], [xo, 'O'], [xb, '+A']].forEach(([x, s]) => { b += ln(x, y - 8, x, y + 8, INK, 2.4) + T(x, y + 32, s, { a: 'middle' }); });
    b += `<circle cx="${xa}" cy="${y - 18}" r="12" fill="${BLUE}"/>` + T(xa, y - 40, 't = 0', { a: 'middle', c: BLUE });
    b += ln(xa, 150, xb, 150, INK, 2) + ln(xa, 142, xa, 158, INK, 2) + ln(xb, 142, xb, 158, INK, 2) + T(xo, 176, '16 cm', { a: 'middle', w: 700 });
    return wrap('0 0 320 186', b, cap, 'Quỹ đạo thẳng dài 16 cm');
  },
  // Trang 7 · Dạng 5: đĩa quay, M ở điểm cao nhất lúc t = 0
  diaD5: (cap = 'M ở điểm cao nhất lúc t = 0.') => tron({ g: 90, R0: 'R', nhanPhi: '?', cap, id: 'd5' }),
  // Trang 2 · Làm nhanh: đọc A, T trên đồ thị
  doThiP2: (cap = '') => doThi({ A: 2, Tc: 0.8, phi: 0, tMax: 1.2, dt: 0.1, lt: 0.4, cap, id: 'p2', nhanX: [2, 1, -1, -2], H: 56 }),
  // Trang 8 · Bài tương tự Dạng 3
  doThiTT1: (cap = '') => doThi({ A: 5, Tc: 2, phi: 0, tMax: 2.5, dt: 0.25, lt: 0.5, cap, id: 't31', nhanX: [5, -5], H: 54 }),
  doThiTT2: (cap = '') => doThi({ A: 3, Tc: 0.4, phi: Math.PI / 2, tMax: 0.6, dt: 0.1, lt: 0.2, cap, id: 't32', nhanX: [3, -3], H: 54 }),
};
