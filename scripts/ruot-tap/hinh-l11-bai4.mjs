// Hình minh hoạ cho ruột tập VL11 · Bài 4 Bài tập về dao động điều hoà (lesson 23). Cùng quy tắc với hinh.mjs/hinh-ch4.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh. Xem thử: node scripts/ruot-tap/l11-bai4.mjs --hinh (chụp vào out/hinh-l11-bai4/).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
// chữ Hi Lạp: Source Sans 3 chỉ nạp latin/vietnamese → lấy từ KaTeX_Math / KaTeX_Main (đã nạp qua katex.min.css)
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const PI = '<tspan font-family="KaTeX_Main">π</tspan>';
const arr = (x1, y1, x2, y2, id, c = INK, dash = '', w = SW) =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const R = (d) => (d * Math.PI) / 180;
const f1 = (v) => (+v).toFixed(1);
// mũi tên hai đầu (orient auto-start-reverse)
const def2 = (id) => `<defs><marker id="${id}" markerWidth="7" markerHeight="7" refX="5.5" refY="3.5" orient="auto-start-reverse" markerUnits="strokeWidth"><path d="M0,0 L7,3.5 L0,7 z" fill="context-stroke"/></marker></defs>`;
// chỉ số dưới trong SVG (không dùng ký tự ₀ ₁ ₂: font không có, rơi về font hệ thống)
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
// chữ trong chú thích HTML
const pi = '<span style="font-family:KaTeX_Main">π</span>';
const so = (x, y, n) => `<circle cx="${x}" cy="${y}" r="12" fill="#fff" stroke="${RED}" stroke-width="2.4"/>` + T(x, y + 7, n, { a: 'middle', w: 700, c: RED });
// cung tròn tâm (x,y), bán kính r, từ a1 tới a2 (độ, ngược chiều kim đồng hồ), có thể kèm mũi tên
const cung = (x, y, r, a1, a2, c = INK, w = 2.4, id = '') => {
  const p = (a) => `${f1(x + r * Math.cos(R(a)))},${f1(y - r * Math.sin(R(a)))}`;
  const lg = Math.abs(a2 - a1) > 180 ? 1 : 0;
  return `<path d="M${p(a1)} A${r},${r} 0 ${lg} 0 ${p(a2)}" fill="none" stroke="${c}" stroke-width="${w}"${id ? ` marker-end="url(#${id})"` : ''}/>`;
};

// Đồ thị x–t vẽ từ phương trình thật x = A cos(2πt/T + φ): số đọc được trên trục, lưới đứt ở các mốc.
// xt: nhãn trục x [[giá trị, 'chữ']]; tt: nhãn trục t; diem: [[t, x]] chấm tròn kèm đường gióng.
const doThi = ({ A, T: P, phi, tmax, xt, tt, diem = [], cap = '', id = 'dt', w = 320, h = 186 }) => {
  const x0 = 58, x1 = w - 22, yc = h / 2 - 4, ky = (h / 2 - 34) / A, kx = (x1 - 10 - x0) / tmax;
  const X = (tv) => x0 + tv * kx, Y = (xv) => yc - xv * ky;
  let b = defs(id + 'a');
  // lưới gióng
  xt.forEach(([v]) => { if (v !== 0) b += ln(x0, f1(Y(v)), x1 - 10, f1(Y(v)), GREY, 1.4, '4 4'); });
  tt.forEach(([v]) => { b += ln(f1(X(v)), 22, f1(X(v)), h - 22, GREY, 1.4, '4 4'); });
  b += arr(x0, h - 14, x0, 10, id + 'a') + arr(x0 - 6, yc, x1 + 14, yc, id + 'a');
  b += T(x0 + 8, 22, 'x (cm)', { size: 20 }) + T(x1 + 14, yc + 26, 't (s)', { a: 'end', size: 20 });
  xt.forEach(([v, s]) => { b += ln(x0 - 6, f1(Y(v)), x0, f1(Y(v)), INK, 2) + T(x0 - 9, Y(v) + 7, s, { a: 'end' }); });
  tt.forEach(([v, s]) => { b += ln(f1(X(v)), yc, f1(X(v)), yc + 6, INK, 2) + T(X(v), yc + 26, s, { a: 'middle' }); });
  let d = '';
  for (let i = 0; i <= 240; i++) { const tv = (tmax * i) / 240; d += `${i ? 'L' : 'M'}${f1(X(tv))},${f1(Y(A * Math.cos((2 * Math.PI * tv) / P + phi)))}`; }
  b += `<path d="${d}" fill="none" stroke="${BLUE}" stroke-width="${SW}"/>`;
  diem.forEach(([tv, xv]) => { b += `<circle cx="${f1(X(tv))}" cy="${f1(Y(xv))}" r="4.5" fill="${RED}"/>`; });
  return wrap(`0 0 ${w} ${h}`, b, cap, 'Đồ thị li độ theo thời gian');
};

// Vòng tròn pha: tâm (cx,cy), bán kính r = A; trục x nằm ngang qua tâm. moc: vạch trên trục [[tỉ lệ theo A, 'nhãn']].
// M: [{g: góc độ, s: 'nhãn', c}] ; quet: [{tu, den, c, s, r}] cung có mũi tên; gion: gióng thẳng đứng từ điểm M xuống trục.
const vongTron = ({ moc = [[-1, '−A'], [0, 'O'], [1, 'A']], M = [], quet = [], gion = true, nua = false, cap = '', id = 'vt', h = 200, ve2 = '' }) => {
  const cx = 160, cy = 96, r = 70;
  let b = defs(id + 'a') + defs(id + 'b');
  b += `<circle cx="${cx}" cy="${cy}" r="${r}" fill="none" stroke="${INK}" stroke-width="2.4"/>`;
  b += arr(cx - r - 26, cy, cx + r + 34, cy, id + 'a', INK, '', 2.4) + T(cx + r + 34, cy - 8, 'x', { a: 'end', w: 700 });
  moc.forEach(([k, s]) => { const x = cx + k * r; b += ln(f1(x), cy - 5, f1(x), cy + 5, INK, 2.4) + (s ? T(x, cy + 27, s, { a: 'middle' }) : ''); });
  if (nua) b += T(6, 34, nua[0], { c: GREY }) + T(6, cy + r + 4, nua[1], { c: GREY });
  quet.forEach(({ tu, den, c = RED, s = '', rr = 40, sr = rr + 22 }) => {
    b += cung(cx, cy, rr, tu, den, c, 2.6, id + 'b');
    if (s) { const g = (tu + den) / 2; b += T(cx + sr * Math.cos(R(g)), cy - sr * Math.sin(R(g)) + 7, s, { a: 'middle', c, w: 700 }); }
  });
  M.forEach(({ g, s = 'M', c = INK, dx = 8, dy = -8 }) => {
    const x = cx + r * Math.cos(R(g)), y = cy - r * Math.sin(R(g));
    b += ln(cx, cy, f1(x), f1(y), c, 2, '5 4');
    if (gion) b += ln(f1(x), f1(y), f1(x), cy, GREY, 2, '3 4');
    b += `<circle cx="${f1(x)}" cy="${f1(y)}" r="6" fill="${c}"/>` + T(x + dx, y + dy, s, { c, w: 700, a: dx < 0 ? 'end' : 'start' });
  });
  b += ve2;
  return wrap(`0 0 320 ${h}`, b, cap, 'Vòng tròn pha');
};

export const hinhL11b4 = {
  // Trang 1 · Dự đoán: quả lắc đồng hồ, bấm giờ biên trái → biên phải
  quaLac: (cap = 'Bấm giờ từ lúc quả lắc ở biên trái tới lúc vừa tới biên phải.') => {
    let b = defs('ql1');
    b += `<rect x="110" y="6" width="100" height="40" rx="6" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(160, 33, '12 : 00', { a: 'middle', w: 700 });
    const px = 160, py = 46, L = 112;
    const pos = (g) => [px + L * Math.sin(R(g)), py + L * Math.cos(R(g))];
    const [lx, ly] = pos(-28), [rx, ry] = pos(28), [ox, oy] = pos(0);
    b += ln(px, py, f1(lx), f1(ly), GREY, 2.4, '6 4') + `<circle cx="${f1(lx)}" cy="${f1(ly)}" r="15" fill="#fff" stroke="${GREY}" stroke-width="2.4" stroke-dasharray="5 4"/>`;
    b += ln(px, py, f1(ox), f1(oy), GREY, 1.6, '3 5');
    b += ln(px, py, f1(rx), f1(ry), INK) + `<circle cx="${f1(rx)}" cy="${f1(ry)}" r="15" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += cung(px, py, L + 30, 242, 298, BLUE, 2.6, 'ql1');
    b += T(lx - 20, ly + 8, 'biên trái', { a: 'end' }) + T(rx + 20, ry + 8, 'biên phải');
    b += T(160, 208, 'bấm 0,8 s', { a: 'middle', c: BLUE, w: 700 });
    return wrap('0 0 320 216', b, cap, 'Quả lắc đồng hồ đi giữa hai biên');
  },
  // Trang 1 · Họ 1: đồ thị x–t, ba khoảng đánh số để HS gọi tên (không ghi sẵn A, T)
  doThiBaKhoang: (cap = 'Gọi tên ba khoảng 1, 2, 3 ở ô bên.') => {
    const P = 1, A = 1, x0 = 40, x1 = 300, yc = 100, ky = 62, kx = (x1 - x0) / 1.75;
    const X = (tv) => x0 + tv * kx, Y = (xv) => yc - xv * ky;
    let b = defs('bk1') + def2('bk2');
    b += arr(x0, 186, x0, 14, 'bk1', INK, '', 2.4) + arr(x0 - 6, yc, 314, yc, 'bk1', INK, '', 2.4) + T(x0 + 8, 24, 'x') + T(312, yc + 24, 't', { a: 'end' });
    let d = '';
    for (let i = 0; i <= 200; i++) { const tv = (1.75 * i) / 200; d += `${i ? 'L' : 'M'}${f1(X(tv))},${f1(Y(A * Math.cos(2 * Math.PI * (tv - 0.25) / P)))}`; }
    b += `<path d="${d}" fill="none" stroke="${BLUE}" stroke-width="${SW}"/>`;
    // ① đỉnh – đáy (thẳng đứng) ở t = 0,75 (đáy) so với đỉnh t = 0,25
    b += ln(X(0.25), Y(1), X(0.92), Y(1), GREY, 1.6, '4 4') + ln(X(0.75), Y(-1), X(0.92), Y(-1), GREY, 1.6, '4 4');
    b += `<line x1="${f1(X(0.92))}" y1="${f1(Y(1))}" x2="${f1(X(0.92))}" y2="${f1(Y(-1))}" stroke="${RED}" stroke-width="2.4" marker-start="url(#bk2)" marker-end="url(#bk2)"/>` + so(X(0.92) + 22, yc + 30, '1');
    // ② đỉnh – đỉnh liền kề (ngang, phía trên)
    b += `<line x1="${f1(X(0.25))}" y1="${f1(Y(1) - 14)}" x2="${f1(X(1.25))}" y2="${f1(Y(1) - 14)}" stroke="${RED}" stroke-width="2.4" marker-start="url(#bk2)" marker-end="url(#bk2)"/>` + so(X(0.75), Y(1) - 14, '2');
    // ③ đỉnh – đáy liền kề (ngang, phía dưới)
    b += ln(X(1.25), Y(1), X(1.25), Y(-1) + 16, GREY, 1.6, '4 4');
    b += `<line x1="${f1(X(0.75))}" y1="${f1(Y(-1) + 16)}" x2="${f1(X(1.25))}" y2="${f1(Y(-1) + 16)}" stroke="${RED}" stroke-width="2.4" marker-start="url(#bk2)" marker-end="url(#bk2)"/>` + so(X(1.0), Y(-1) + 16, '3');
    return wrap('0 0 320 196', b, cap, 'Đồ thị li độ – thời gian, ba khoảng đánh số');
  },
  // Trang 2 · Họ 2: chiều gia tốc ở hai phía O
  trucXVA: (cap = 'Mũi tên đỏ: chiều gia tốc khi vật ở hai phía của O.') => {
    let b = defs('xa1') + defs('xa2');
    const y = 92, xm = 30, xo = 160, xp = 290;
    b += arr(14, y, 312, y, 'xa1', INK, '', 2.4) + T(312, y - 10, 'x', { a: 'end', w: 700 });
    [[xm, '−A'], [xo, 'O'], [xp, '+A']].forEach(([x, s]) => { b += ln(x, y - 6, x, y + 6, INK, 2.4) + T(x, y + 30, s, { a: 'middle' }); });
    b += `<circle cx="96" cy="${y}" r="13" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + `<circle cx="236" cy="${y}" r="13" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += arr(96, y - 34, 146, y - 34, 'xa2', RED) + T(121, y - 44, 'a', { a: 'middle', c: RED, w: 700 });
    b += arr(236, y - 34, 186, y - 34, 'xa2', RED) + T(211, y - 44, 'a', { a: 'middle', c: RED, w: 700 });
    b += T(96, y + 56, 'x < 0', { a: 'middle' }) + T(236, y + 56, 'x > 0', { a: 'middle' });
    return wrap('0 0 320 160', b, cap, 'Gia tốc ở hai phía vị trí cân bằng');
  },
  // Trang 2 · Họ 3: cos φ = x0/A cho hai điểm M đối xứng
  haiDiemM: (cap = 'Cùng x<sub>0</sub> có hai điểm M: trên và dưới trục. Chiều đi chọn điểm nào?') => vongTron({
    id: 'hm', moc: [[-1, '−A'], [0, ''], [0.5, ''], [1, 'A']], gion: true,
    M: [{ g: 60, s: `M${sb('1')}` }, { g: -60, s: `M${sb('2')}`, dy: 22 }],
    ve2: T(150, 120, 'O', { a: 'end' }) + T(198, 120, `x${sb('0')}`),
  }),
  // Trang 3 · Họ 4: mốc thời gian O ↔ A/2 ↔ biên (góc quét ghi sẵn, thời gian để trống)
  mocThoiGian: (cap = 'Góc quét từ O tới A/2 và từ A/2 ra biên. Mỗi góc ứng với bao nhiêu phần T?') => vongTron({
    id: 'mt', moc: [[-1, '−A'], [0, 'O'], [0.5, 'A/2'], [1, 'A']], gion: true, nua: ['nửa trên', 'nửa dưới'],
    M: [{ g: 60, s: '', c: INK }],
    quet: [{ tu: 90, den: 60, c: RED, s: '30°', rr: 46, sr: 96 }, { tu: 60, den: 0, c: BLUE, s: '60°', rr: 28 }],
    ve2: ln(160, 96, 160, 26, GREY, 2, '5 4'), h: 196,
  }),
  // Trang 4 · Bài toán mẫu: M xuất phát ở −π/3, quay ngược chiều kim đồng hồ
  mau: (cap = `Lúc t = 0, M ở pha −${pi}/3. Tô cung M quét tới lúc vật qua O lần đầu.`) => vongTron({
    id: 'bm', moc: [[-1, '−8'], [0, '0'], [0.5, '4'], [1, '8']],
    M: [{ g: -60, s: `M${sb('0')}`, dy: 24 }],
    ve2: cung(160, 96, 30, -60, -10, INK, 2.4, 'bmb'),
  }),
  // Trang 6 · Dạng 3 (bài mẫu): đồ thị đọc được số — đáy t = 0,4 s, đỉnh t = 1,0 s, x₀ = 2 cm
  doThiD3: (cap = '') => doThi({
    id: 'd3', A: 4, T: 1.2, phi: Math.PI / 3, tmax: 1.3,
    xt: [[4, '4'], [2, '2'], [0, '0'], [-4, '−4']], tt: [[0.4, '0,4'], [1.0, '1,0']], diem: [[0, 2], [0.4, -4], [1.0, 4]], cap, h: 166,
  }),
  // Trang 7 · Dạng 4: M xuất phát ở π/3; hai đường x = −3 cm cắt vòng tròn
  d4: (cap = `M<sub>0</sub> ở pha ${pi}/3. Đường đứt: x = −3 cm cắt vòng tròn ở hai điểm.`) => vongTron({
    id: 'd4', moc: [[-1, '−6'], [-0.5, '−3'], [0, '0'], [0.5, '3'], [1, '6']],
    M: [{ g: 60, s: `M${sb('0')}` }], gion: true,
    ve2: ln(125, 22, 125, 170, RED, 2.2, '6 4') + cung(160, 96, 26, 60, 110, INK, 2.4, 'd4b'),
  }),
  // Trang 7 · Dạng 5: x₀ = A/2 đi về biên âm (M nửa trên), quét thêm phần dư
  d5: (cap = 'Lúc t = 0: x = 2 cm, đi về biên âm. Phần dư T/3 quét bao nhiêu độ?') => vongTron({
    id: 'd5', moc: [[-1, '−4'], [0, '0'], [0.5, '2'], [1, '4']],
    M: [{ g: 60, s: `M${sb('0')}` }], nua: ['nửa trên', 'nửa dưới'],
  }),
  // Trang 9 · Bài tương tự Dạng 4: M₀ ở pha π/6, đường x = A/2
  ttD4: (cap = `x = 10 cos(${pi}t + ${pi}/6) cm. Đường đứt: x = 5 cm.`) => vongTron({
    id: 't4', moc: [[-1, '−10'], [0, '0'], [0.5, '5'], [1, '10']],
    M: [{ g: 30, s: `M${sb('0')}` }],
    ve2: ln(195, 22, 195, 170, RED, 2.2, '6 4'),
  }),
  // Trang 8 · Bài tương tự Dạng 3 (hai đồ thị khác số)
  ttD3a: (cap = '') => doThi({
    id: 't3a', A: 6, T: 0.6, phi: (2 * Math.PI) / 3, tmax: 0.7,
    xt: [[6, '6'], [0, '0'], [-3, '−3'], [-6, '−6']], tt: [[0.1, '0,1'], [0.4, '0,4']], diem: [[0, -3], [0.1, -6], [0.4, 6]], cap,
  }),
  ttD3b: (cap = '') => doThi({
    id: 't3b', A: 3, T: 2.4, phi: -Math.PI / 3, tmax: 2.0,
    xt: [[3, '3'], [1.5, '1,5'], [0, '0'], [-3, '−3']], tt: [[0.4, '0,4'], [1.6, '1,6']], diem: [[0, 1.5], [0.4, 3], [1.6, -3]], cap,
  }),
};
