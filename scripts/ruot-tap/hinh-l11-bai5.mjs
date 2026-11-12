// Hình minh hoạ cho ruột tập VL11 · Bài 5 Động năng. Thế năng. Sự chuyển hoá năng lượng trong DĐĐH (lesson 24).
// Cùng quy tắc với hinh-l10-bai23.mjs: mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox (đồ thị: số trục 18–20),
// nét ≥ 2,8, phân biệt bằng nét (đặc – đứt), tự vẽ. Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh.
// Xem thử: node scripts/ruot-tap/l11-bai5.mjs --hinh (chụp vào out/hinh-l11-bai5/).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const Et = `E${sb('t')}`, Ed = `E${sb('d')}`;
const f1 = (v) => (+v).toFixed(1);
const arr = (x1, y1, x2, y2, id, c = INK, dash = '', w = SW) =>
  `<line x1="${f1(x1)}" y1="${f1(y1)}" x2="${f1(x2)}" y2="${f1(y2)}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${f1(x1)}" y1="${f1(y1)}" x2="${f1(x2)}" y2="${f1(y2)}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const vc = (s) => s.replace(/\./g, ',');

// lò xo zic-zắc từ x1 tới x2 ở độ cao y
const loXo = (x1, x2, y, n = 9, h = 10) => {
  const d = (x2 - x1 - 16) / (n * 2);
  let p = `M${x1},${y} L${x1 + 8},${y}`;
  for (let i = 0; i < n * 2; i++) p += ` L${f1(x1 + 8 + d * (i + 0.5))},${y + (i % 2 ? h : -h)}`;
  p += ` L${x2 - 8},${y} L${x2},${y}`;
  return `<path d="${p}" fill="none" stroke="${INK}" stroke-width="2.4"/>`;
};
const tuong = (x, y1, y2) => ln(x, y1, x, y2, INK, 4) + Array.from({ length: Math.floor((y2 - y1) / 14) }, (_, i) => ln(x, y1 + 6 + i * 14, x - 9, y1 + 14 + i * 14, GREY, 1.8)).join('');
const san = (x1, x2, y) => ln(x1, y, x2, y) + Array.from({ length: Math.floor((x2 - x1) / 18) }, (_, i) => ln(x1 + 8 + i * 18, y, x1 + i * 18, y + 8, GREY, 1.8)).join('');

// Con lắc lò xo nằm ngang: VTCB O ở x0, biên ±A cách a đơn vị; vật vẽ ở li độ xv (đơn vị vẽ). nhan: nhãn ba vạch.
const conLac = ({ cap = '', xv = 0, nhan = [`−A`, 'O', '+A'], dau = [], v = '', id = 'cl', W = 320 } = {}) => {
  const x0 = 186, a = 104, y = 92;
  let b = defs(id + 'a');
  b += tuong(18, 40, 124) + san(18, W - 6, 124);
  b += loXo(18, x0 + xv - 22, y);
  b += `<rect x="${x0 + xv - 22}" y="${y - 22}" width="44" height="44" rx="4" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
  [-a, 0, a].forEach((d, i) => { b += ln(x0 + d, 130, x0 + d, 146, INK, 2.4) + T(x0 + d, 170, nhan[i], { a: 'middle', w: 700 }); });
  b += ln(x0 - a, 138, x0 + a, 138, GREY, 2, '5 4');
  dau.forEach(([d, s]) => { b += ln(x0 + d, 130, x0 + d, 146, RED, 2.4) + T(x0 + d, 194, s, { a: 'middle', c: RED, w: 700 }); });
  if (v) b += arr(x0 + xv + 26, y - 34, x0 + xv + 86, y - 34, id + 'a', BLUE, '6 4') + T(x0 + xv + 30, y - 44, v, { c: BLUE, w: 700 });
  return wrap(`0 0 ${W} ${dau.some((q) => q[1]) ? 204 : 180}`, b, cap, 'Con lắc lò xo nằm ngang');
};

// Hệ trục đồ thị năng lượng: trục ngang từ -xr..xr (li độ) hoặc 0..T (thời gian)
// Đồ thị đọc được số: E(x) parabol, lưới theo bước, nhãn trục ≥ 18 đơn vị.
const doThiE = ({ cap = '', loai = 'd', W = 0.04, A = 4, xr = 5, buoc = 0.01, ten, id = 'dt' } = {}) => {
  const L = 62, R = 306, Tp = 22, B = 196, xs = (x) => L + ((x + xr) / (2 * xr)) * (R - L), ymax = buoc * Math.ceil(W / buoc + 0.6);
  const ys = (e) => B - (e / ymax) * (B - Tp);
  let b = defs(id + 'a');
  for (let x = -xr; x <= xr; x++) b += ln(xs(x), Tp, xs(x), B, '#c9d1e3', 1.2);
  for (let e = 0; e <= ymax + 1e-9; e += buoc) b += ln(L, ys(e), R, ys(e), '#c9d1e3', 1.2) + (e > 1e-9 ? T(L - 6, ys(e) + 6, vc(e.toFixed((String(buoc).split('.')[1] || '').length)), { a: 'end', size: 18 }) : '');
  b += arr(L, B, R + 10, B, id + 'a') + arr(xs(0), B, xs(0), Tp - 14, id + 'a');
  for (let x = -xr; x <= xr; x += 1) if (x % 2 === 0 || xr <= 4) b += T(xs(x), B + 20, x < 0 ? `−${-x}` : `${x}`, { a: 'middle', size: 18 });
  b += T(R + 12, B - 8, 'x', { a: 'end', w: 700 }) + T(xs(0) + 8, Tp - 2, ten ?? `${loai === 'd' ? Ed : Et} (J)`, { size: 18 });
  let p = '';
  for (let i = 0; i <= 60; i++) { const x = -A + (2 * A * i) / 60, e = loai === 'd' ? W * (1 - (x / A) ** 2) : W * (x / A) ** 2; p += `${i ? 'L' : 'M'}${f1(xs(x))},${f1(ys(e))} `; }
  b += `<path d="${p}" fill="none" stroke="${RED}" stroke-width="3"/>`;
  b += `<circle cx="${f1(xs(-A))}" cy="${f1(ys(loai === 'd' ? 0 : W))}" r="4" fill="${RED}"/><circle cx="${f1(xs(A))}" cy="${f1(ys(loai === 'd' ? 0 : W))}" r="4" fill="${RED}"/>`;
  return wrap('0 0 320 228', b, cap, 'Đồ thị năng lượng theo li độ');
};

// Et(x) và Ed(x) chung một hệ trục, không số (chỉ −A, O, +A) — hỏi chỗ cắt nhau
const haiParabol = (cap = '') => {
  const L = 30, R = 300, Tp = 30, B = 176, xs = (x) => (L + R) / 2 + x * 118, ys = (e) => B - e * 132;
  let b = defs('hpa');
  b += arr(L, B, R + 10, B, 'hpa') + arr(xs(0), B, xs(0), Tp - 16, 'hpa');
  b += ln(xs(-1), ys(1), xs(1), ys(1), GREY, 2.2, '8 5') + T(xs(1) + 4, ys(1) - 6, 'W', { w: 700, a: 'end' });
  let p1 = '', p2 = '';
  for (let i = 0; i <= 60; i++) { const x = -1 + i / 30; p1 += `${i ? 'L' : 'M'}${f1(xs(x))},${f1(ys(x * x))} `; p2 += `${i ? 'L' : 'M'}${f1(xs(x))},${f1(ys(1 - x * x))} `; }
  b += `<path d="${p1}" fill="none" stroke="${INK}" stroke-width="3"/><path d="${p2}" fill="none" stroke="${RED}" stroke-width="3" stroke-dasharray="9 5"/>`;
  const c = Math.SQRT1_2;
  b += ln(xs(c), ys(0.5), xs(c), B, GREY, 1.8, '4 4') + ln(xs(-c), ys(0.5), xs(-c), B, GREY, 1.8, '4 4');
  b += T(xs(c), B + 22, '?', { a: 'middle', w: 700, c: RED }) + T(xs(-c), B + 22, '?', { a: 'middle', w: 700, c: RED });
  b += T(xs(-1), B + 22, '−A', { a: 'middle', w: 700 }) + T(xs(1), B + 22, '+A', { a: 'middle', w: 700 }) + T(xs(0) - 6, B + 22, 'O', { a: 'end', w: 700 });
  return wrap('0 0 320 206', b, cap, 'Thế năng và động năng theo li độ');
};

// Et(t), Ed(t), W theo thời gian 0..T, thả từ biên lúc t = 0
const theoT = (cap = '', { vach = ['T/4', 'T/2', '3T/4', 'T'] } = {}) => {
  const L = 34, R = 300, Tp = 30, B = 170, xs = (s) => L + s * (R - L - 14), ys = (e) => B - e * 120;
  let b = defs('tta');
  b += arr(L, B, R + 12, B, 'tta') + arr(L, B, L, Tp - 16, 'tta') + T(R + 14, B - 8, 't', { a: 'end', w: 700 });
  b += ln(L, ys(1), xs(1), ys(1), GREY, 2.2, '8 5') + T(xs(1) + 2, ys(1) - 8, 'W', { w: 700, a: 'end' });
  let p1 = '', p2 = '';
  for (let i = 0; i <= 80; i++) { const s = i / 80, c = Math.cos(2 * Math.PI * s) ** 2; p1 += `${i ? 'L' : 'M'}${f1(xs(s))},${f1(ys(c))} `; p2 += `${i ? 'L' : 'M'}${f1(xs(s))},${f1(ys(1 - c))} `; }
  b += `<path d="${p1}" fill="none" stroke="${INK}" stroke-width="3"/><path d="${p2}" fill="none" stroke="${RED}" stroke-width="3" stroke-dasharray="9 5"/>`;
  vach.forEach((s, i) => { const x = xs((i + 1) / 4); b += ln(x, B - 5, x, B + 5, INK, 2) + T(x, B + 24, s, { a: 'middle', size: 18 }); });
  b += T(L - 4, B + 24, '0', { a: 'middle', size: 18 });
  return wrap('0 0 320 204', b, cap, 'Thế năng và động năng theo thời gian');
};

// Xích đu: ba vị trí, hai biên và đáy
const xichDu = (cap = '') => {
  const ox = 160, oy = 18, Lr = 140;
  let b = ln(40, oy, 280, oy, INK, 4);
  [-38, 0, 38].forEach((g, i) => {
    const r = (g * Math.PI) / 180, x = ox + Lr * Math.sin(r), y = oy + Lr * Math.cos(r);
    const dash = i === 1 ? '' : '6 4';
    b += ln(ox, oy, x, y, i === 1 ? INK : GREY, 2.4, dash) + `<rect x="${f1(x - 20)}" y="${f1(y - 4)}" width="40" height="9" rx="2" fill="#fff" stroke="${i === 1 ? INK : GREY}" stroke-width="2.4"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
    b += `<circle cx="${f1(x)}" cy="${f1(y - 22)}" r="10" fill="#fff" stroke="${i === 1 ? INK : GREY}" stroke-width="2.4"/>`;
  });
  b += T(36, 150, 'dừng', { a: 'middle', size: 20 }) + T(284, 150, 'dừng', { a: 'middle', size: 20 }) + T(160, 190, 'nhanh nhất', { a: 'middle', w: 700 });
  return wrap('0 0 320 198', b, cap, 'Xích đu dao động');
};

// Thanh chia cơ năng W thành n+1 phần: 1 phần Et, n phần Ed (để trống số)
const chiaW = (cap = '', n = 8) => {
  const L = 14, R = 306, w = (R - L) / (n + 1);
  let b = `<rect x="${L}" y="40" width="${R - L}" height="40" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
  for (let i = 1; i <= n; i++) b += ln(L + i * w, 40, L + i * w, 80, INK, i === 1 ? SW : 1.6, i === 1 ? '' : '4 3');
  b += `<rect x="${L}" y="40" width="${f1(w)}" height="40" fill="#d9deea"/>` + ln(L + w, 40, L + w, 80, INK, SW);
  b += T(L + w / 2, 30, Et, { a: 'middle', w: 700 }) + T((L + w + R) / 2, 30, `${Ed} = ${n} ${Et}`, { a: 'middle', c: RED, w: 700 });
  return wrap('0 0 320 90', b, cap, 'Chia cơ năng theo tỉ lệ');
};

export const hinhL11b5 = {
  // Trang 1 · Dự đoán
  xichDu: (cap = 'Lên chỗ cao nhất, đu dừng một lát rồi lao xuống.') => xichDu(cap),
  // Trang 1 · thế năng, động năng: đánh dấu chỗ lớn nhất
  conLacTrang1: (cap = 'Vật đi qua lại giữa −A và +A. Đánh dấu chỗ E<sub>t</sub> lớn nhất, chỗ E<sub>d</sub> lớn nhất.') => conLac({ cap, xv: 52, id: 'c1' }),
  // Trang 2 · hai parabol
  haiParabol: (cap = 'Nét liền, nét đứt: đường nào là E<sub>t</sub>, đường nào là E<sub>d</sub>? Hai đường cắt nhau ở x = ?') => haiParabol(cap),
  // Trang 2 · theo thời gian
  theoT: (cap = 'Thả từ biên lúc t = 0. Nét liền: E<sub>t</sub>; nét đứt: E<sub>d</sub>.') => theoT(cap),
  // Trang 3 · thí nghiệm năm vạch
  namVach: (cap = 'k = 40 N/m, A = 8,0 cm. Năm vạch đánh dấu từ VTCB ra biên.') => conLac({ cap, xv: 104, nhan: ['−8,0', '0', '8,0'], dau: [[52, '4,0'], [73.5, ''], [90, '']], id: 'c3' }),
  // Trang 4 · bài toán mẫu
  mau: (cap = 'A = 8,0 cm; vật đang ở x = 4,0 cm.') => conLac({ cap, xv: 52, nhan: ['−8 cm', 'O', '+8 cm'], dau: [[52, '4 cm']], id: 'c4' }),
  // Trang 5 · thử thách đổi biên độ
  doiA: (cap = 'Cùng k, m. Biên độ từ 8,0 cm còn 6,0 cm.') => conLac({ cap, xv: 0, nhan: ['−8', 'O', '8'], dau: [[-78, '−6'], [78, '6']], v: 'v<tspan font-size="15" dy="5">max</tspan>', id: 'c5' }),
  // ===== Bài tập mẫu =====
  d1: (cap = 'A = 10 cm, vật đang ở x = 6,0 cm.') => conLac({ cap, xv: 62, nhan: ['−10', 'O', '+10'], dau: [[62, '6 cm']], v: 'v = ?', id: 'd1' }),
  d2: (cap = 'Cả thanh là W.') => chiaW(cap, 8),
  d3: (cap = 'Biết x và v cùng lúc; chưa biết A.') => conLac({ cap, xv: 31, nhan: ['−A?', 'O', '+A?'], dau: [[31, '3 cm']], v: '40 cm/s', id: 'd3' }),
  d4: (cap = 'Nét liền E<sub>t</sub>, nét đứt E<sub>d</sub>.') => theoT(cap),
  d5: (cap = '') => doThiE({ loai: 'd', W: 0.04, A: 4, xr: 5, buoc: 0.01, cap, id: 'g5' }),
  // ===== Bài tương tự =====
  t5a: (cap = '') => doThiE({ loai: 'd', W: 0.09, A: 6, xr: 7, buoc: 0.02, cap, id: 'g6' }),
  t5b: (cap = '') => doThiE({ loai: 't', W: 0.125, A: 5, xr: 6, buoc: 0.025, cap, id: 'g7' }),
};
