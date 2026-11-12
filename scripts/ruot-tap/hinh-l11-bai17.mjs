// Hình minh hoạ cho ruột tập VL11 · Bài 17 Khái niệm điện trường (lesson 36). Cùng quy tắc với hinh.mjs/hinh-l10-bai23.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh (hình ở mục lý thuyết để trống mũi tên cho học sinh tự vẽ).
// Xem thử: node scripts/ruot-tap/l11-bai17.mjs --hinh (chụp vào out/hinh-l11-bai17/).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
// chữ Hi Lạp/vectơ: Source Sans 3 chỉ nạp latin/vietnamese → lấy từ KaTeX_Math (đã nạp qua katex.min.css)
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const f1 = (v) => (+v).toFixed(1);
const R = (d) => (d * Math.PI) / 180;
const arr = (x1, y1, x2, y2, id, c = INK, dash = '', w = SW) =>
  `<line x1="${f1(x1)}" y1="${f1(y1)}" x2="${f1(x2)}" y2="${f1(y2)}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${f1(x1)}" y1="${f1(y1)}" x2="${f1(x2)}" y2="${f1(y2)}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
// điện tích: vòng tròn có dấu; dương nền đỏ chữ trắng, âm nền trắng viền xanh (phân biệt bằng cả nền lẫn dấu)
const dt = (x, y, s, r = 13) => s === '+'
  ? `<circle cx="${f1(x)}" cy="${f1(y)}" r="${r}" fill="${RED}"/>${t(x, y + r * 0.55, '+', { c: '#fff', size: r * 1.6, a: 'middle', w: 700 })}`
  : `<circle cx="${f1(x)}" cy="${f1(y)}" r="${r}" fill="#fff" stroke="${BLUE}" stroke-width="${SW}"/>${t(x, y + r * 0.5, '−', { c: BLUE, size: r * 1.6, a: 'middle', w: 700 })}`;
const cham = (x, y, r = 4.5) => `<circle cx="${f1(x)}" cy="${f1(y)}" r="${r}" fill="${INK}"/>`;
const vE = `${gk('E')}`;
// ô ngắn đánh dấu góc vuông tại P giữa hai hướng u, v (vectơ đơn vị)
const vuong = (P, u, v, s = 11) => `<path d="M${f1(P[0] + u[0] * s)},${f1(P[1] + u[1] * s)} L${f1(P[0] + (u[0] + v[0]) * s)},${f1(P[1] + (u[1] + v[1]) * s)} L${f1(P[0] + v[0] * s)},${f1(P[1] + v[1] * s)}" fill="none" stroke="${INK}" stroke-width="2"/>`;
const don = (a, b) => { const d = Math.hypot(b[0] - a[0], b[1] - a[1]); return [(b[0] - a[0]) / d, (b[1] - a[1]) / d]; };
// mũi đo khoảng cách hai đầu |—|
const doDai = (x1, y1, x2, y2, s, o = 14) => {
  const [ux, uy] = don([x1, y1], [x2, y2]), nx = -uy * o, ny = ux * o;
  return ln(x1 + nx, y1 + ny, x2 + nx, y2 + ny, GREY, 2) + ln(x1 + nx * 0.6, y1 + ny * 0.6, x1 + nx * 1.4, y1 + ny * 1.4, GREY, 2)
    + ln(x2 + nx * 0.6, y2 + ny * 0.6, x2 + nx * 1.4, y2 + ny * 1.4, GREY, 2)
    + T((x1 + x2) / 2 + nx * 2.1, (y1 + y2) / 2 + ny * 2.1 + 7, s, { a: 'middle' });
};

// Đường sức của hai điện tích +q (x1) và −q (x2) trên cùng hàng y: vạch số bằng Euler bước nhỏ
const duongSucLuong = (x1, x2, y, n = 10, r0 = 15, box = [0, 0, 320, 200]) => {
  const E = (x, yy) => {
    const d1 = Math.hypot(x - x1, yy - y) ** 3, d2 = Math.hypot(x - x2, yy - y) ** 3;
    return [(x - x1) / d1 - (x - x2) / d2, (yy - y) / d1 - (yy - y) / d2];
  };
  let out = '';
  for (let i = 0; i < n; i++) {
    const a = (2 * Math.PI * (i + 0.5)) / n;
    let px = x1 + r0 * Math.cos(a), py = y + r0 * Math.sin(a), d = `M${f1(px)},${f1(py)}`;
    for (let s = 0; s < 1600; s++) {
      const [ex, ey] = E(px, py), m = Math.hypot(ex, ey);
      px += (2 * ex) / m; py += (2 * ey) / m;
      if (s % 3 === 0) d += ` L${f1(px)},${f1(py)}`;
      if (Math.hypot(px - x2, py - y) < r0 || px < box[0] || px > box[2] || py < box[1] || py > box[3]) break;
    }
    out += `<path d="${d}" fill="none" stroke="${INK}" stroke-width="2.2"/>`;
  }
  return out;
};

// điểm trên trung trực: A, B cách nhau ab (cm), M cách H một đoạn mh (cm); tỉ lệ k px/cm
const trungTruc = ({ qa, qb, ab, mh, k = 28, nhan = {}, vec = false, cap, id = 'tt', w = 320, h = 210 }) => {
  const cx = w / 2, yAB = h - 40, A = [cx - (ab / 2) * k, yAB], B = [cx + (ab / 2) * k, yAB], H = [cx, yAB], M = [cx, yAB - mh * k];
  let b = defs(id + 'a') + defs(id + 'b');
  b += ln(A[0], A[1], B[0], B[1], GREY, 2) + ln(H[0], H[1] + 10, M[0], M[1] - (vec ? 62 : 22), GREY, 2, '5 4');
  b += ln(A[0], A[1], M[0], M[1], INK, 2, '6 4') + ln(B[0], B[1], M[0], M[1], INK, 2, '6 4');
  b += vuong(H, [0, -1], [1, 0], 9);
  b += dt(A[0], A[1], qa.s) + dt(B[0], B[1], qb.s) + cham(H[0], H[1], 4) + cham(M[0], M[1]);
  b += T(A[0], A[1] + 34, qa.t, { a: 'middle' }) + T(B[0], B[1] + 34, qb.t, { a: 'middle' }) + T(H[0], H[1] + 26, 'H', { a: 'middle', w: 700 });
  b += T(M[0] - 10, M[1] - 8, 'M', { a: 'end', w: 700 });
  b += T(cx - 8, (H[1] + M[1]) / 2 + 7, nhan.mh ?? `${String(mh).replace('.', ',')} cm`, { a: 'end' });
  b += T((A[0] + H[0]) / 2 + 6, yAB + 24, nhan.ah ?? `${String(ab / 2).replace('.', ',')} cm`, { a: 'middle' });
  if (vec) { // E1 dọc tia A→M, E2 dọc tia B→M (cùng dương), độ dài 58
    const ua = don(A, M), ub = don(B, M), L = 58;
    b += arr(M[0], M[1], M[0] + ua[0] * L, M[1] + ua[1] * L, id + 'a', RED) + T(M[0] + ua[0] * L + 6, M[1] + ua[1] * L + 4, `${vE}${sb('1')}`, { c: RED });
    b += arr(M[0], M[1], M[0] + ub[0] * L, M[1] + ub[1] * L, id + 'b', BLUE, '7 4') + T(M[0] + ub[0] * L - 6, M[1] + ub[1] * L + 4, `${vE}${sb('2')}`, { c: BLUE, a: 'end' });
  }
  return wrap(`0 0 ${w} ${h}`, b, cap, 'Hai điện tích và điểm M trên đường trung trực');
};

// tia Q → các điểm (r tính bằng cm, tỉ lệ k)
const tia = ({ q, pts, k = 20, cap, w = 320, h = 104 }) => {
  const x0 = 26, y = 52;
  let b = defs('tia') + arr(x0, y, w - 8, y, 'tia', GREY, '', 2);
  b += dt(x0, y, q.s) + T(x0, y + 38, q.t, { a: 'middle' });
  pts.forEach(([ten, r, nhan]) => { const x = x0 + r * k; b += cham(x, y) + T(x, y - 14, ten, { a: 'middle', w: 700 }) + T(x, y + 32, nhan, { a: 'middle' }); });
  return wrap(`0 0 ${w} ${h}`, b, cap, 'Các điểm trên một tia đi ra từ điện tích');
};

// đường thẳng qua hai điện tích với các điểm xét
const duong = ({ ds, pts, k = 30, cap, w = 320, h = 110, x0 = 40 }) => {
  const y = 50;
  let b = ln(10, y, w - 10, y, GREY, 2);
  ds.forEach(([ten, x, s, nh]) => { b += dt(x0 + x * k, y, s) + T(x0 + x * k, y - 22, ten, { a: 'middle', w: 700 }) + T(x0 + x * k, y + 36, nh, { a: 'middle' }); });
  pts.forEach(([ten, x, nh]) => { b += cham(x0 + x * k, y) + T(x0 + x * k, y - 14, ten, { a: 'middle', w: 700 }) + (nh ? T(x0 + x * k, y + 32, nh, { a: 'middle' }) : ''); });
  return wrap(`0 0 ${w} ${h}`, b, cap, 'Hai điện tích trên một đường thẳng');
};

export const hinhL11b17 = {
  // Trang 1 · Dự đoán: thước nhựa cọ tóc hút giấy vụn chưa chạm
  thuocGiay: (cap = 'Thước vừa cọ vào tóc, đưa lại gần giấy vụn.') => {
    let b = `<g transform="rotate(-6 160 50)"><rect x="40" y="34" width="250" height="30" rx="3" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += Array.from({ length: 12 }, (_, i) => ln(54 + i * 20, 34, 54 + i * 20, i % 2 ? 44 : 50, INK, 1.8)).join('');
    b += Array.from({ length: 6 }, (_, i) => T(64 + i * 40, 86, '−', { c: BLUE, w: 700, size: 24 })).join('') + '</g>';
    b += ln(10, 178, 310, 178);
    // giấy nằm, giấy đang bay lên
    const giay = [[30, 172, 0], [70, 170, 20], [250, 172, -10], [290, 171, 15]];
    b += giay.map(([x, y, a]) => `<rect x="${x}" y="${y}" width="16" height="6" fill="${GREY}" transform="rotate(${a} ${x + 8} ${y + 3})"/>`).join('');
    const bay = [[118, 128, 25], [160, 112, -20], [204, 124, 35]];
    b += bay.map(([x, y, a]) => `<rect x="${x}" y="${y}" width="16" height="6" fill="${GREY}" transform="rotate(${a} ${x + 8} ${y + 3})"/>`
      + ln(x + 8, y + 18, x + 8, y + 40, GREY, 2, '3 4')).join('');
    b += T(306, 160, 'không khí', { a: 'end', c: GREY });
    return wrap('0 0 320 188', b, cap, 'Thước nhựa nhiễm điện hút giấy vụn');
  },
  // Trang 1 · II.2: cùng E tại M, vẽ F cho q dương và q âm
  efDau: (cap = 'Cùng E tại M. Vẽ F lên từng q.') => {
    let b = defs('ef1');
    [[0, '+', 'q &gt; 0'], [160, '−', 'q &lt; 0']].forEach(([ox, s, nh]) => {
      b += arr(ox + 30, 40, ox + 130, 40, 'ef1', GREY, '7 4') + T(ox + 130, 28, vE, { c: GREY, a: 'end', w: 700 });
      b += dt(ox + 80, 92, s, 12) + T(ox + 80, 140, nh, { a: 'middle' }) + T(ox + 104, 98, 'M', { w: 700 });
    });
    b += ln(160, 10, 160, 140, GREY, 1.6, '3 4');
    return wrap('0 0 320 150', b, cap, 'Điện tích thử dương và âm trong cùng điện trường');
  },
  // Trang 2 · II.3: điểm quanh +Q và −Q, học sinh tự vẽ mũi tên E
  quanhQ: (cap = 'Vẽ E tại các chấm: chấm gần Q mũi tên dài hơn hay ngắn hơn?') => {
    let b = '';
    [[80, '+', '+Q'], [240, '−', '−Q']].forEach(([cx, s, nh]) => {
      const cy = 92;
      b += `<circle cx="${cx}" cy="${cy}" r="36" fill="none" stroke="${GREY}" stroke-width="1.6" stroke-dasharray="3 4"/>`;
      b += `<circle cx="${cx}" cy="${cy}" r="66" fill="none" stroke="${GREY}" stroke-width="1.6" stroke-dasharray="3 4"/>`;
      b += dt(cx, cy, s, 14);
      [[36, 0], [36, 180], [66, 90], [66, 270]].forEach(([r, a]) => { b += cham(cx + r * Math.cos(R(a)), cy - r * Math.sin(R(a))); });
      b += T(cx - 50, cy + 74 + 8, nh, { a: 'middle', w: 700 });
    });
    return wrap('0 0 320 184', b, cap, 'Các điểm quanh điện tích dương và âm');
  },
  // Trang 2 · thí nghiệm: cân điện tử đo lực điện
  canDien: (cap = 'Q giữ bằng cán cách điện, cách q một đoạn r (tính từ tâm hai quả cầu).') => {
    let b = defs('cd1');
    b += `<rect x="70" y="150" width="150" height="34" rx="5" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<rect x="90" y="158" width="64" height="18" rx="2" fill="#fff" stroke="${INK}" stroke-width="2"/>` + T(122, 174, `+<tspan font-family="KaTeX_Main">Δ</tspan>m`, { a: 'middle', size: 18 });
    b += ln(110, 150, 180, 150, INK, 5) + ln(145, 150, 145, 138, INK, 3) + dt(145, 124, '+', 13) + T(166, 132, 'q');
    b += dt(145, 50, '+', 15) + ln(145, 35, 145, 6, GREY, 5) + T(168, 50, 'Q');
    b += ln(214, 50, 214, 124, GREY, 2, '5 4') + ln(205, 50, 223, 50, GREY, 2) + ln(205, 124, 223, 124, GREY, 2) + T(228, 94, 'r');
    b += arr(118, 112, 118, 142, 'cd1', RED) + T(112, 132, `F`, { c: RED, w: 700, a: 'end' });
    b += T(234, 176, 'cân', { c: GREY });
    return wrap('0 0 320 192', b, cap, 'Cân điện tử đo lực điện');
  },
  // Trang 2 · II.4: đường sức của cặp điện tích trái dấu, chưa có mũi tên
  duongSuc: (cap = 'Đánh mũi tên chiều lên vài đường. E ở A hay ở B lớn hơn?') => {
    let b = duongSucLuong(110, 210, 100, 12, 16, [0, 0, 320, 200]);
    b += dt(110, 100, '+', 14) + dt(210, 100, '−', 14);
    b += `<circle cx="160" cy="100" r="6" fill="#fff" stroke="${RED}" stroke-width="2.6"/>` + T(160, 132, 'A', { a: 'middle', w: 700, c: RED });
    b += `<circle cx="22" cy="40" r="6" fill="#fff" stroke="${RED}" stroke-width="2.6"/>` + T(40, 34, 'B', { w: 700, c: RED });
    return wrap('0 0 320 200', b, cap, 'Đường sức của hai điện tích trái dấu');
  },
  // Trang 3 · II.5: quy tắc hình bình hành
  hbh: (cap = 'Góc <i style="font-family:KaTeX_Math">α</i> giữa hai vectơ đổi từ 0° tới 180°: E thay đổi thế nào?') => {
    let b = defs('hb1') + defs('hb2') + defs('hb3');
    const O = [40, 150], P1 = [200, 150], P2 = [100, 58], S = [P1[0] + P2[0] - O[0], P1[1] + P2[1] - O[1]];
    b += ln(P1[0], P1[1], S[0], S[1], GREY, 2, '5 4') + ln(P2[0], P2[1], S[0], S[1], GREY, 2, '5 4');
    b += arr(O[0], O[1], P1[0], P1[1], 'hb1', RED) + T(P1[0] - 4, P1[1] + 26, `${vE}${sb('1')}`, { c: RED, a: 'end' });
    b += arr(O[0], O[1], P2[0], P2[1], 'hb2', BLUE, '7 4') + T(P2[0] - 10, P2[1] + 6, `${vE}${sb('2')}`, { c: BLUE, a: 'end' });
    b += arr(O[0], O[1], S[0], S[1], 'hb3', INK, '', 3.4) + T(S[0] + 6, S[1] - 4, `${vE} = ?`, { w: 700 });
    const a2 = Math.atan2(O[1] - P2[1], P2[0] - O[0]);
    b += `<path d="M${O[0] + 30},${O[1]} A30,30 0 0 0 ${f1(O[0] + 30 * Math.cos(a2))},${f1(O[1] - 30 * Math.sin(a2))}" fill="none" stroke="${INK}" stroke-width="2.2"/>`;
    b += T(O[0] + 36, O[1] - 10, gk('α')) + cham(O[0], O[1]) + T(O[0] - 8, O[1] + 22, 'M', { w: 700, a: 'end' });
    return wrap('0 0 320 172', b, cap, 'Cộng hai vectơ cường độ điện trường');
  },
  // Trang 4 · bài toán mẫu: tam giác 3–4–5
  tamGiac345: (cap = 'Vẽ E<sub>1</sub>, E<sub>2</sub> tại M, rồi vẽ E.') => {
    let b = defs('tg1') + defs('tg2');
    const k = 46, A = [24, 170], B = [24 + 5 * k, 170], M = [24 + 1.8 * k, 170 - 2.4 * k];
    b += ln(A[0], A[1], B[0], B[1], GREY, 2) + ln(A[0], A[1], M[0], M[1], INK, 2) + ln(M[0], M[1], B[0], B[1], INK, 2);
    const ua = don(A, M), ub = don(M, B);
    b += dt(A[0], A[1], '+', 12) + dt(B[0], B[1], '−', 12) + cham(M[0], M[1]);
    b += T(M[0] - 10, M[1] - 6, 'M', { w: 700, a: 'end' }) + T(A[0] + 2, A[1] + 30, 'A', { w: 700, a: 'middle' }) + T(B[0], B[1] + 30, 'B', { w: 700, a: 'middle' });
    b += T((A[0] + M[0]) / 2 - 8, (A[1] + M[1]) / 2 + 4, '3', { a: 'end' }) + T((M[0] + B[0]) / 2 + 6, (M[1] + B[1]) / 2 + 2, '4') + T((A[0] + B[0]) / 2, A[1] + 22, '5 cm', { a: 'middle' });
    return wrap('0 0 300 200', b, cap, 'Tam giác AMB và hai vectơ điện trường tại M');
  },
  // Trang 5 · thử thách ★★★: ba điện tích ở ba đỉnh tam giác đều
  tamGiacDeu: (cap = 'Ba điện tích +q bằng nhau. E ở tâm O bằng bao nhiêu?') => {
    const O = [100, 104], r = 72;
    const V = [90, 210, 330].map((a) => [O[0] + r * Math.cos(R(a)), O[1] - r * Math.sin(R(a))]);
    let b = `<path d="M${V.map((p) => p.map(f1).join(',')).join(' L')} z" fill="none" stroke="${INK}" stroke-width="2.2"/>`;
    b += V.map((p) => ln(p[0], p[1], O[0], O[1], GREY, 1.8, '4 4')).join('') + V.map((p) => dt(p[0], p[1], '+', 13)).join('');
    b += cham(O[0], O[1]) + T(O[0] + 10, O[1] + 22, 'O', { w: 700 }) + T(O[0] + 10, O[1] - 8, '?', { c: RED, w: 700 });
    return wrap('0 0 200 158', b, cap, 'Ba điện tích ở đỉnh tam giác đều');
  },

  // ===== Bài tập mẫu =====
  d1: (cap = 'E tại M hướng nào?') => {
    let b = defs('d1a');
    b += arr(270, 100, 270, 40, 'd1a', GREY, '', 2) + T(270, 30, 'Bắc', { a: 'middle', c: GREY });
    b += dt(100, 96, '−', 13) + T(124, 114, 'M', { w: 700 }) + T(196, 102, `q${sb('1')} = −4 nC`, { a: 'middle' });
    b += arr(100, 80, 100, 14, 'd1a', RED) + T(112, 30, `F${sb('1')}`, { c: RED, w: 700 });
    return wrap('0 0 320 124', b, cap, 'Lực lên điện tích thử âm');
  },
  d2: (cap = 'Q &lt; 0: E tại M hướng nào?') => duong({ ds: [['Q', 0, '−', '−6 nC']], pts: [['M', 6, '3 cm']], k: 36, x0: 50, cap }),
  d3: (cap = 'Cùng Q, cùng dầu.') => tia({ q: { s: '+', t: '+8 nC' }, pts: [['M', 4, '4 cm'], ['N', 12, '12 cm']], k: 22, cap }),
  d4: (cap = 'Tại M, tại I: cùng hay ngược chiều?') => duong({ ds: [['A', 0, '+', '+9 nC'], ['B', 4, '−', '−4 nC']], pts: [['I', 2, ''], ['M', 6, '']], k: 40, x0: 30, cap,
    w: 320, h: 110 }).replace('</svg>', `${doDai(30, 50, 110, 50, '2 cm', -30)}${doDai(110, 50, 190, 50, '2 cm', -30)}${doDai(190, 50, 270, 50, '2 cm', -30)}</svg>`)
    .replace('viewBox="0 0 320 110"', 'viewBox="0 -40 320 150"'),
  d5: (cap = 'Nửa góc <i style="font-family:KaTeX_Math">α</i> bằng góc nào của tam giác MHA?') =>
    trungTruc({ qa: { s: '+', t: '+5 nC' }, qb: { s: '+', t: '+5 nC' }, ab: 8, mh: 3, k: 26, vec: true, cap, id: 'd5', h: 230 }),
  // ===== Bài tương tự =====
  ttD3: (cap = 'Dầu <i style="font-family:KaTeX_Math">ε</i> = 3.') => tia({ q: { s: '+', t: '+6 nC' }, pts: [['M', 3, '3 cm'], ['N', 6, '6 cm']], k: 40, cap }),
  ttD5: (cap = 'MA = MB = ?') => trungTruc({ qa: { s: '+', t: '+6 nC' }, qb: { s: '−', t: '−6 nC' }, ab: 6, mh: 4, k: 26, cap, id: 'tt5', h: 200 }),
};
