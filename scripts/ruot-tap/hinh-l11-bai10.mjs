// Hình minh hoạ cho ruột tập VL11 · Bài 10 Thực hành: đo tần số của sóng âm (lesson 29).
// Cùng quy tắc với hinh.mjs: mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt), tự vẽ.
// Chú thích không lộ đáp án ô Dự đoán/ô điền đứng cạnh. Xem thử: node scripts/ruot-tap/l11-bai10.mjs --hinh (vào out/hinh-l11-bai10/).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const dot = (x, y, r = 5, c = INK) => `<circle cx="${x}" cy="${y}" r="${r}" fill="${c}"/>`;
const rect = (x, y, w, h, r = 0, fill = '#fff') => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r}" fill="${fill}" stroke="${INK}" stroke-width="${SW}"/>`;
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const path = (pts, c = INK, w = SW, dash = '') => `<path d="M${pts.map(([x, y]) => `${x.toFixed(1)},${y.toFixed(1)}`).join(' L')}" fill="none" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''} stroke-linejoin="round"/>`;
const arrow = (x1, y, x2, c = INK) => ln(x1, y, x2, y, c, 2.6) + `<path d="M${x1},${y} l9,-5 v10 z M${x2},${y} l-9,-5 v10 z" fill="${c}"/>`;
const C = 26; // một ô = 26 đơn vị
// màn dao động kí: lưới 10×rows ô, gốc (X, Y) góc trên trái; trục ngang ở giữa
const luoi = (X, Y, rows) => {
  let b = rect(X, Y, 10 * C, rows * C, 0, '#fff');
  for (let i = 1; i < 10; i++) b += ln(X + i * C, Y, X + i * C, Y + rows * C, '#d3dbec', i === 5 ? 1.6 : 1);
  for (let j = 1; j < rows; j++) b += ln(X, Y + j * C, X + 10 * C, Y + j * C, '#d3dbec', j === rows / 2 ? 1.6 : 1);
  return b;
};
// sóng hình sin: biên độ a ô, chu kì per ô, đỉnh đầu tiên ở ô `start`, từ ô `x0` đến `x1`
const song = (X, Yc, a, per, start, x0, x1, c = INK, w = SW) => {
  const pts = [];
  for (let x = x0; x <= x1 + 1e-9; x += 0.05) pts.push([X + x * C, Yc - a * C * Math.cos((2 * Math.PI * (x - start)) / per)]);
  return path(pts, c, w);
};

export const hinhL11b10 = {
  // Trang 1 · Dự đoán: điện thoại cạnh đàn (chỉ mô tả cảnh, không nói cách đo)
  dienThoai: (cap = 'Điện thoại đặt cạnh đàn lúc lên dây.') => {
    let b = '';
    b += `<ellipse cx="86" cy="118" rx="48" ry="36" fill="#fff" stroke="${INK}" stroke-width="${SW}"/><ellipse cx="86" cy="80" rx="32" ry="26" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += rect(78, 6, 16, 80, 0) + `<circle cx="86" cy="110" r="12" fill="${GREY}" opacity=".35" stroke="${INK}" stroke-width="2.4"/>`;
    for (const dx of [-5, -1.7, 1.7, 5]) b += ln(86 + dx, 8, 86 + dx, 140, INK, 1.6);
    b += T(86, 182, 'ukulele', { a: 'middle' });
    b += rect(196, 28, 70, 124, 8) + rect(204, 40, 54, 84, 2, '#eef2fa');
    b += `<path d="M212,100 A22,22 0 0 1 250,100" fill="none" stroke="${INK}" stroke-width="2.6"/>` + ln(231, 104, 238, 84, RED, 3) + dot(231, 104, 3.6);
    b += T(231, 182, 'điện thoại', { a: 'middle' });
    return wrap('0 0 320 194', b, cap, 'Điện thoại đặt cạnh cây đàn ukulele, màn hình có kim chỉ');
  },
  // Trang 1 · II.1: đồ thị âm đơn theo thời gian, T là khoảng giữa hai đỉnh liền nhau
  sinSong: (cap = 'Âm đơn: đồ thị hình sin theo thời gian.') => {
    const x0 = 40, yc = 80;
    let b = defs('ss1') + ln(x0, yc, 300, yc) + `<path d="M300,${yc} l-9,-5 v10 z" fill="${INK}"/>` + ln(x0, 18, x0, 140) + T(296, yc + 26, `${gk('t')} (ms)`, { a: 'end' });
    b += path(Array.from({ length: 231 }, (_, i) => [x0 + i, yc - 46 * Math.sin((2 * Math.PI * i) / 100)]));
    // hai đỉnh liên tiếp: i = 25 và 125
    b += dot(x0 + 25, yc - 46, 5.5, RED) + dot(x0 + 125, yc - 46, 5.5, RED) + ln(x0 + 25, yc - 46, x0 + 25, 18, GREY, 2, '5 4') + ln(x0 + 125, yc - 46, x0 + 125, 18, GREY, 2, '5 4');
    b += arrow(x0 + 27, 24, x0 + 123, RED);
    return wrap('0 0 320 160', b, cap, 'Đồ thị sin theo thời gian, hai đỉnh liên tiếp cách nhau một chu kì');
  },
  // Trang 2 · sơ đồ: nguồn âm đơn → micro → CH1 của dao động kí
  soDo: (cap = 'Sơ đồ nối: nguồn âm, micro, dao động kí.') => {
    let b = '';
    // âm thoa
    b += `<path d="M28,24 v66 q0,12 12,12 q12,0 12,-12 v-66" fill="none" stroke="${INK}" stroke-width="5"/>` + ln(40, 102, 40, 140, INK, 5) + T(40, 170, 'âm thoa', { a: 'middle' });
    // micro
    b += rect(100, 60, 36, 30, 6) + ln(136, 75, 140, 75) + T(118, 112, 'micro', { a: 'middle' }) + ln(118, 90, 118, 96) ;
    // dây tới CH1
    b += ln(140, 75, 170, 75) + ln(170, 75, 170, 118) + ln(170, 118, 196, 118) + dot(196, 118, 5);
    // dao động kí
    b += rect(190, 14, 120, 154, 6) + rect(200, 24, 100, 62, 3, '#eef2fa') + `<path d="M204,55 q8,-22 16,0 t16,0 t16,0 t16,0 t16,0" fill="none" stroke="${INK}" stroke-width="2.6"/>`;
    b += T(208, 122, 'CH1', { w: 700, size: 18 }) + `<circle cx="258" cy="116" r="9" fill="#fff" stroke="${INK}" stroke-width="2.6"/><circle cx="288" cy="116" r="9" fill="#fff" stroke="${INK}" stroke-width="2.6"/>`;
    b += T(258, 146, 'ms', { a: 'middle', size: 16 }) + T(288, 146, 'V', { a: 'middle', size: 16 }) + T(250, 194, 'dao động kí', { a: 'middle' });
    return wrap('0 0 320 204', b, cap, 'Âm thoa, micro nối vào kênh CH1 của dao động kí');
  },
  // Trang 3 và BTM D1: màn dao động kí với các chấm ở đỉnh sóng. start/per tính bằng ô; n = số chu kì (n+1 đỉnh)
  man: ({ start = 1, per = 2, n = 4, cap = 'Chấm: các đỉnh sóng liên tiếp.' } = {}) => {
    const X = 20, Y = 14, rows = 8;
    let b = luoi(X, Y, rows) + song(X, Y + 4 * C, 3, per, start, 0, 10);
    for (let i = 0; i <= n; i++) b += dot(X + (start + i * per) * C, Y + C, 6, RED);
    const xa = X + start * C, xb = X + (start + n * per) * C;
    b += ln(xa, Y + 8 * C + 12, xb, Y + 8 * C + 12, INK, 2.6) + ln(xa, Y + 8 * C + 5, xa, Y + 8 * C + 19, INK, 2.6) + ln(xb, Y + 8 * C + 5, xb, Y + 8 * C + 19, INK, 2.6) + T((xa + xb) / 2, Y + 8 * C + 38, gk('L'), { a: 'middle', w: 700 });
    return wrap('0 0 300 270', b, cap, 'Màn dao động kí chia lưới, sóng hình sin với các chấm tại đỉnh');
  },
  // Trang 3 · Bẫy 3: hai âm cùng biên độ, cùng thang thời gian
  haiAm: (cap = 'Cùng thang thời gian, cùng biên độ.') => {
    const X = 20;
    let b = '';
    for (const [i, per, lab] of [[0, 3, 'A'], [1, 1.5, 'B']]) {
      const Y = 10 + i * 112;
      b += luoi(X, Y, 4) + song(X, Y + 2 * C, 1.4, per, 0.5, 0, 10) + T(X + 10 * C + 6, Y + 2 * C + 7, lab, { w: 700, size: 22 });
    }
    return wrap('0 0 330 238', b, cap, 'Hai màn dao động kí cùng thang: âm A sóng thưa, âm B sóng dày');
  },
  // Trang 4 · đọc ô: cùng một sóng, đo 1 chu kì (1) hay nhiều chu kì (2)
  haiCach: (cap = 'Hai cách đo trên cùng một màn.') => {
    const X = 20, Y = 14, rows = 6, yb = Y + rows * C;
    let b = luoi(X, Y, rows) + song(X, Y + 3 * C, 2, 2, 1, 0, 10);
    const br = (xa, xb, y, lab, dash = '') => ln(xa, y, xb, y, INK, 3, dash) + ln(xa, y - 7, xa, y + 7, INK, 3) + ln(xb, y - 7, xb, y + 7, INK, 3) + T(xb + 12, y + 7, lab, { w: 700 });
    b += br(X + 1 * C, X + 3 * C, yb + 18, '(1)') + br(X + 1 * C, X + 9 * C, yb + 50, '(2)', '9 5');
    return wrap('0 0 300 250', b, cap, 'Màn dao động kí: đoạn (1) đo một chu kì, đoạn (2) đo nhiều chu kì liên tiếp');
  },
  // Trang 5 · màn trống để em vẽ lại hình sóng của nhóm
  manTrong: (cap = 'Màn của nhóm em: vẽ sóng, đánh dấu N chu kì và L.') => {
    const X = 20, Y = 14;
    return wrap('0 0 300 240', luoi(X, Y, 8), cap, 'Lưới màn dao động kí trống để vẽ');
  },
};
