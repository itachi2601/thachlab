// Hình minh hoạ cho ruột tập VL11 · Bài 19 Thế năng điện (lesson 38). Cùng quy tắc với hinh.mjs/hinh-l10-bai23.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh. Xem thử: node scripts/ruot-tap/l11-bai19.mjs --hinh (chụp vào out/hinh-l11-bai19/).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const GREEN = '#2e7d32';
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
// chữ Hi Lạp: Source Sans 3 chỉ nạp latin/vietnamese → lấy từ KaTeX_Math (đã nạp qua katex.min.css)
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const f1 = (v) => (+v).toFixed(1);
const arr = (x1, y1, x2, y2, id, c = INK, dash = '', w = SW) =>
  `<line x1="${f1(x1)}" y1="${f1(y1)}" x2="${f1(x2)}" y2="${f1(y2)}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${f1(x1)}" y1="${f1(y1)}" x2="${f1(x2)}" y2="${f1(y2)}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const dot = (x, y, c = INK, r = 5) => `<circle cx="${f1(x)}" cy="${f1(y)}" r="${r}" fill="${c}"/>`;
const R = (d) => (d * Math.PI) / 180;
const cung = (x, y, r, a1, a2, c = INK) => {
  const p = (a) => `${f1(x + r * Math.cos(R(a)))},${f1(y - r * Math.sin(R(a)))}`;
  return `<path d="M${p(a1)} A${r},${r} 0 0 0 ${p(a2)}" fill="none" stroke="${c}" stroke-width="2.2"/>`;
};
// đường sức nằm ngang (mũi tên sang phải), các hàng y
const sucNgang = (x1, x2, ys, id) => ys.map((y) => arr(x1, y, x2, y, id, GREY, '', 2)).join('');
// bản phẳng nằm ngang có dấu (+/−) bên trái
const ban = (x1, x2, y, dau) => `<rect x="${x1}" y="${y - 4}" width="${x2 - x1}" height="8" fill="${dau === '+' ? RED : BLUE}" opacity=".85"/>` + T(x1 - 6, y + 7, dau, { a: 'end', w: 700, c: dau === '+' ? RED : BLUE, size: 24 });
const Evec = (x, y, o = {}) => T(x, y, 'E', { w: 700, c: GREY, ...o });

export const hinhL11b19 = {
  // ===== Trang 1 =====
  hatBui: (cap = 'Đường đỏ: bay thẳng. Đường xanh: lượn cong.') => {
    let b = defs('hb1') + defs('hb2');
    b += `<path d="M14,86 L58,92 L14,98 z" fill="${INK}"/>` + T(10, 126, 'đầu kim');
    b += `<rect x="286" y="20" width="12" height="150" fill="${GREY}"/>` + T(280, 190, 'tấm thu', { a: 'end' });
    b += arr(62, 94, 276, 126, 'hb1', RED);
    b += `<path d="M62,92 C120,10 200,-6 250,50 S276,100 280,112" fill="none" stroke="${BLUE}" stroke-width="${SW}" stroke-dasharray="7 5" marker-end="url(#hb2)"/>`;
    b += dot(284, 121, INK, 6) + T(258, 154, 'N', { w: 700 });
    return wrap('0 0 320 198', b, cap, 'Hai hạt bụi từ đầu kim tới tấm thu');
  },
  hinhChieu: (cap = 'Đoạn d trong hình là gì?') => {
    let b = defs('hc1') + defs('hc2');
    b += sucNgang(10, 312, [34, 175], 'hc1') + Evec(296, 18);
    const Mx = 70, My = 140, Nx = 220, Ny = 60;
    b += arr(Mx, My, Nx, Ny, 'hc2', RED) + dot(Mx, My) + dot(Nx, Ny) + T(Mx - 24, My + 8, 'M', { w: 700 }) + T(Nx + 8, Ny - 4, 'N', { w: 700 });
    b += ln(Mx, My, 300, My, GREY, 1.8, '4 4') + cung(Mx, My, 34, 0, 28) + T(Mx + 40, My - 4, gk('α'));
    b += ln(Mx, My, Mx, 168, INK, 1.8, '5 4') + ln(Nx, Ny, Nx, 168, INK, 1.8, '5 4');
    b += ln(Mx, 168, Nx, 168, '#d9822b', 6) + T((Mx + Nx) / 2, 160, 'd', { a: 'middle', w: 700, c: '#b35f00' });
    return wrap('0 0 320 190', b, cap, 'Hình chiếu của MN lên đường sức');
  },
  // ===== Trang 2 =====
  baDuong: (cap = 'Ba đường từ M tới N: thẳng, gấp khúc qua P, cong.') => {
    let b = defs('bd1') + defs('bd2') + defs('bd3') + defs('bd4');
    b += sucNgang(10, 312, [32, 186], 'bd1') + Evec(296, 18);
    const Mx = 60, My = 150, Px = 60, Py = 62, Nx = 250, Ny = 62;
    b += arr(Mx, My, Nx - 6, Ny + 3, 'bd2', RED);
    b += arr(Mx, My, Px, Py + 6, 'bd3', BLUE, '7 5') + arr(Px, Py, Nx - 8, Ny, 'bd3', BLUE, '7 5');
    b += `<path d="M${Mx},${My} C140,210 300,170 ${Nx + 2},${Ny + 8}" fill="none" stroke="${GREEN}" stroke-width="${SW}" stroke-dasharray="2 5" stroke-linecap="round" marker-end="url(#bd4)"/>`;
    b += dot(Mx, My) + dot(Px, Py) + dot(Nx, Ny) + T(Mx - 26, My + 8, 'M', { w: 700 }) + T(Px - 26, Py + 6, 'P', { w: 700 }) + T(Nx + 8, Ny - 8, 'N', { w: 700 });
    return wrap('0 0 320 198', b, cap, 'Ba đường đi từ M tới N trong điện trường đều');
  },
  haiBan: (cap = 'Hai bản phẳng; đoạn d đo từ M.') => {
    let b = defs('hb3') + defs('hb4');
    b += ban(40, 300, 24, '+') + ban(40, 300, 170, '−');
    [90, 170, 250].forEach((x) => { b += arr(x, 34, x, 158, 'hb3', GREY, '', 2); });
    b += Evec(258, 104);
    b += dot(140, 80, INK, 6) + T(118, 72, 'M', { w: 700 });
    b += ln(140, 88, 140, 166, INK, 2, '5 4') + T(148, 132, 'd', { w: 700 });
    b += T(306, 196, 'mốc: W = 0', { a: 'end', size: 22 });
    return wrap('0 0 320 202', b, cap, 'Thế năng điện giữa hai bản phẳng');
  },
  // ===== Trang 3 =====
  doThi: (cap = 'Chấm 4 điểm (x; V) của bảng, nối thử bằng thước.') => {
    let b = defs('dt1');
    const X0 = 50, Y0 = 170, sx = 30, sy = 25; // 1 cm ↔ 30; 1 V ↔ 25
    for (let i = 1; i <= 8; i++) b += ln(X0 + i * sx, Y0, X0 + i * sx, Y0 - 150, '#d3dbec', 1.2);
    for (let j = 1; j <= 6; j++) b += ln(X0, Y0 - j * sy, X0 + 8 * sx + 10, Y0 - j * sy, '#d3dbec', 1.2);
    b += arr(X0, Y0, X0 + 8 * sx + 22, Y0, 'dt1') + arr(X0, Y0, X0, 10, 'dt1');
    [2, 4, 6, 8].forEach((x) => { b += T(X0 + x * sx, Y0 + 22, String(x), { a: 'middle', size: 22 }); });
    [2, 4].forEach((v) => { b += T(X0 - 8, Y0 - v * sy + 6, String(v), { a: 'end', size: 22 }); });
    b += T(X0 + 8 * sx + 4, Y0 - 10, 'x (cm)', { a: 'end', size: 22 }) + T(X0 + 20, 34, 'V (V)', { size: 22 });
    b += T(X0 - 10, Y0 + 22, '0', { a: 'end', size: 22 });
    return wrap('0 0 320 198', b, cap, 'Lưới đồ thị V theo x để học sinh tự chấm điểm');
  },
  // ===== Trang 4: bài toán mẫu =====
  mau: (cap = 'Electron đi M → P (ngang) rồi P → N (lên). Hai bản cách nhau 4&nbsp;cm.') => {
    let b = defs('mu1') + defs('mu2');
    b += ban(40, 300, 22, '+') + ban(40, 300, 182, '−');
    [70, 270].forEach((x) => { b += arr(x, 32, x, 170, 'mu1', GREY, '', 2); });
    b += Evec(278, 104);
    const Mx = 100, My = 142, Px = 220, Py = 142, Nx = 220, Ny = 62; // 1 cm ↔ 40
    b += arr(Mx, My, Px - 8, Py, 'mu2', RED) + arr(Px, Py, Nx, Ny + 8, 'mu2', RED);
    b += dot(Mx, My) + dot(Px, Py) + dot(Nx, Ny);
    b += T(Mx - 6, My - 10, 'M', { w: 700, a: 'end' }) + T(Px + 8, Py + 6, 'P', { w: 700 }) + T(Nx + 8, Ny + 6, 'N', { w: 700 });
    b += T((Mx + Px) / 2, My - 10, '3 cm', { a: 'middle', size: 22, c: RED }) + T(Nx - 8, (Py + Ny) / 2 + 6, '2 cm', { a: 'end', size: 22, c: RED });
    b += ln(Mx, My, Mx, 178, INK, 1.8, '4 4') + T(Mx + 6, 168, '1 cm', { size: 22 });
    return wrap('0 0 320 196', b, cap, 'Bài toán mẫu: electron giữa hai bản');
  },
  // ===== Trang 5: thử thách =====
  tamGiac: (cap = 'Tam giác đều cạnh 10 cm, E song song BC, chiều B → C.') => {
    let b = defs('tg1');
    const Bx = 50, By = 192, Cx = 250, Cy = 192, Ax = 150, Ay = 192 - 173.2;
    b += `<path d="M${Bx},${By} L${Cx},${Cy} L${Ax},${f1(Ay)} z" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
    b += T(Ax + 12, Ay + 18, 'A', { w: 700, size: 26 }) + T(Bx - 8, By + 8, 'B', { a: 'end', w: 700, size: 26 }) + T(Cx + 8, Cy + 8, 'C', { w: 700, size: 26 });
    b += arr(70, 220, 230, 220, 'tg1', GREY, '', 2.4) + Evec(240, 228, { size: 26 });
    return wrap('0 0 300 234', b, cap, 'Tam giác đều trong điện trường đều');
  },
  // ===== Bài tập mẫu =====
  d1: (cap = 'MN dài 8,0 cm, hợp với chiều đường sức góc 120°.') => {
    let b = defs('d1a') + defs('d1b');
    b += sucNgang(10, 312, [34, 176], 'd1a') + Evec(296, 18);
    const Mx = 210, My = 150, L = 150, Nx = Mx + L * Math.cos(R(120)), Ny = My - L * Math.sin(R(120));
    b += ln(Mx, My, 300, My, GREY, 1.8, '4 4') + cung(Mx, My, 30, 0, 120) + T(Mx + 28, My - 30, '120°', { size: 22 });
    b += arr(Mx, My, Nx, Ny, 'd1b', RED) + dot(Mx, My) + dot(Nx, Ny) + T(Mx + 4, My + 22, 'M', { w: 700 }) + T(Nx - 24, Ny + 4, 'N', { w: 700 });
    b += ln(Nx, Ny, Nx, 168, INK, 1.8, '5 4') + T((Mx + Nx) / 2, 172, 'd = ?', { a: 'middle', w: 700, c: '#b35f00' });
    return wrap('0 0 320 186', b, cap, 'Electron đi xiên ngược đường sức');
  },
  d2: (cap = 'Đường A → B → C và đường cong A → D; CD vuông góc đường sức.') => {
    let b = defs('d2a') + defs('d2b') + defs('d2c');
    b += arr(10, 190, 312, 190, 'd2a', GREY, '', 2) + Evec(292, 182);
    const Ax = 30, Ay = 130, Bx = 120, By = 130, Cx = Bx + 110 * Math.cos(R(60)), Cy = By - 110 * Math.sin(R(60)), Dx = Cx, Dy = Cy + 44;
    b += arr(Ax, Ay, Bx - 6, By, 'd2b', RED) + arr(Bx, By, Cx - 3, Cy + 6, 'd2b', RED);
    b += ln(Bx, By, Bx + 60, By, GREY, 1.6, '4 4') + cung(Bx, By, 26, 0, 60) + T(Bx + 30, By - 6, '60°', { size: 22 });
    b += `<path d="M${Ax},${Ay} C60,184 170,184 ${f1(Dx - 4)},${f1(Dy + 6)}" fill="none" stroke="${BLUE}" stroke-width="${SW}" stroke-dasharray="7 5" marker-end="url(#d2c)"/>`;
    b += ln(Cx, Cy, Dx, Dy, INK, 2, '3 3');
    b += [[Ax, Ay, 'A', -8, -10], [Bx, By, 'B', -6, 24], [Cx, Cy, 'C', 10, 4], [Dx, Dy, 'D', 10, 8]].map(([x, y, s, dx, dy]) => dot(x, y) + T(x + dx, y + dy, s, { w: 700, a: dx < 0 ? 'end' : 'start' })).join('');
    return wrap('0 0 320 200', b, cap, 'Đường gấp khúc và đường cong trong điện trường đều');
  },
  d3: (cap = 'Mốc ở bản trên. N ở đâu?') => {
    let b = defs('d3a');
    b += ban(40, 300, 22, '−') + ban(40, 300, 172, '+');
        const My = 22 + 30; // 1 cm ↔ 30
    b += dot(150, My) + T(160, My + 8, 'M', { w: 700 }) + ln(130, 22, 130, My, INK, 1.8, '4 4') + T(124, 46, '1 cm', { a: 'end', size: 22 });
    b += T(150, 130, 'N ?', { w: 700, a: 'middle' });
    b += T(306, 198, 'mốc: W = 0 ở bản trên', { a: 'end', size: 22 });
    return wrap('0 0 320 204', b, cap, 'Hạt bụi giữa hai bản, mốc ở bản trên');
  },
  d4: (cap = 'Thả nghỉ ở M; tới bản âm với v = 10 m/s.') => {
    let b = defs('d4a') + defs('d4b');
    b += ban(40, 300, 20, '+') + ban(40, 300, 182, '−');
    [70, 270].forEach((x) => { b += arr(x, 30, x, 170, 'd4a', GREY, '', 2); });
    b += Evec(278, 104);
    const X = 160, My = 182 - 5 * 28, Py = 182 - 2 * 28; // 1 cm ↔ 28
    b += arr(X, My, X, 174, 'd4b', RED, '6 4') + dot(X, My) + dot(X, Py, BLUE);
    b += T(X - 10, My + 6, 'M', { w: 700, a: 'end' }) + T(X - 10, Py + 6, 'P', { w: 700, a: 'end', c: BLUE });
    b += ln(210, My, 210, 178, INK, 1.6, '4 4') + T(216, (My + 182) / 2 - 18, '5,0 cm', { size: 22 });
    b += ln(110, Py, 110, 178, BLUE, 1.6, '4 4') + T(104, Py + 30, '2,0', { size: 22, a: 'end', c: BLUE });
    return wrap('0 0 320 196', b, cap, 'Hạt bụi rơi từ M tới bản âm');
  },
  // ===== Bài tương tự =====
  tt21: (cap = 'A → B dọc đường sức, B → C vuông góc; đường cong A → C.') => {
    let b = defs('t2a') + defs('t2b') + defs('t2c');
    b += arr(10, 186, 312, 186, 't2a', GREY, '', 2) + Evec(292, 178);
    const Ax = 40, Ay = 150, Bx = 180, By = 150, Cx = 180, Cy = 40;
    b += arr(Ax, Ay, Bx - 8, By, 't2b', RED) + arr(Bx, By, Cx, Cy + 8, 't2b', RED);
    b += `<path d="M${Ax},${Ay} C40,20 120,0 ${Cx - 6},${Cy + 2}" fill="none" stroke="${BLUE}" stroke-width="${SW}" stroke-dasharray="7 5" marker-end="url(#t2c)"/>`;
    b += [[Ax, Ay, 'A', -8, 8], [Bx, By, 'B', 10, 8], [Cx, Cy, 'C', 10, 6]].map(([x, y, s, dx, dy]) => dot(x, y) + T(x + dx, y + dy, s, { w: 700, a: dx < 0 ? 'end' : 'start' })).join('');
    b += T((Ax + Bx) / 2, Ay + 24, '5,0 cm', { a: 'middle', size: 22 }) + T(Bx + 10, (By + Cy) / 2 + 6, '8,0 cm', { size: 22 });
    return wrap('0 0 320 196', b, cap, 'Đường gấp khúc và đường cong');
  },
  tt32: (cap = 'Hai bản đứng cách 5,0 cm; mốc ở bản âm (bên phải).') => {
    let b = defs('t3a');
    b += `<rect x="40" y="20" width="8" height="150" fill="${RED}" opacity=".85"/><rect x="272" y="20" width="8" height="150" fill="${BLUE}" opacity=".85"/>`;
    b += T(44, 194, '+', { a: 'middle', w: 700, c: RED, size: 24 }) + T(276, 194, '−', { a: 'middle', w: 700, c: BLUE, size: 24 });
    [50, 140].forEach((y) => { b += arr(56, y, 262, y, 't3a', GREY, '', 2); });
    b += Evec(150, 42);
    const Mx = 272 - 3 * 44.8, Nx = 272 - 1 * 44.8; // 1 cm ↔ 44,8
    b += dot(Mx, 100) + dot(Nx, 100) + T(Mx, 90, 'M', { w: 700, a: 'middle' }) + T(Nx, 90, 'N', { w: 700, a: 'middle' });
    return wrap('0 0 320 200', b, cap, 'Electron giữa hai bản thẳng đứng');
  },
};
