// Hình minh hoạ cho ruột tập VL12 · Bài 8 Áp suất – động năng của phân tử khí (lesson 9). Cùng quy tắc với hinh.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh. Xem thử: node scripts/ruot-tap/l12-bai8.mjs --hinh (chụp vào out/hinh-l12-bai8/).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
// chữ Hi Lạp: Source Sans 3 chỉ nạp latin/vietnamese → lấy từ KaTeX_Math (đã nạp qua katex.min.css)
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const sp = (s) => `<tspan font-size="15" dy="-8">${s}</tspan><tspan dy="8"> </tspan>`;
const arr = (x1, y1, x2, y2, id, c = INK, dash = '', w = SW) =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const dot = (x, y, r = 6, fill = INK) => `<circle cx="${x}" cy="${y}" r="${r}" fill="${fill}" stroke="${INK}" stroke-width="1.6"/>`;
// tường gạch chéo thẳng đứng ở x, từ y1 tới y2, gạch về phía phải
const tuong = (x, y1, y2) => ln(x, y1, x, y2, INK, 4) + Array.from({ length: Math.floor((y2 - y1) / 16) }, (_, i) =>
  ln(x + 2, y1 + 6 + i * 16, x + 12, y1 - 4 + i * 16, GREY, 1.8)).join('');
// bình kín: hình chữ nhật bo góc
const binh = (x, y, w, h) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="10" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;

export const hinhL12b8 = {
  // ===== Trang học bài mới =====
  bongBan: (cap = 'Bóng bẹp nhúng vào nước 80 °C: cái gì đẩy vỏ ra?') => {
    let b = defs('bb1');
    b += `<path d="M30,80 Q60,104 90,80 A34,34 0 1 1 30,80 z" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(60, 156, 'bóng bẹp', { a: 'middle' });
    b += arr(104, 96, 150, 96, 'bb1') + T(127, 84, 'nhúng', { a: 'middle' });
    b += `<path d="M168,34 L168,160 L292,160 L292,34" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<path d="M168,56 q15,-8 31,0 t31,0 t31,0 t31,0" fill="none" stroke="${BLUE}" stroke-width="2.4" stroke-dasharray="7 4"/>`;
    b += `<circle cx="230" cy="110" r="30" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(230, 119, '?', { a: 'middle', w: 700, size: 26 });
    b += T(230, 24, 'nước 80 °C', { a: 'middle' });
    return wrap('0 0 300 170', b, cap, 'Quả bóng bàn bẹp nhúng vào cốc nước nóng');
  },
  hopKhi: (cap = 'Khí trong bình nhìn qua “kính hiển vi tưởng tượng”.') => {
    let b = defs('hk1');
    b += `<rect x="12" y="12" width="276" height="150" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    const P = [[50, 44, 36, 14], [120, 40, -28, 22], [210, 50, 34, -6], [256, 112, 26, 20], [70, 120, -30, -22], [150, 100, 20, 32], [196, 130, -36, 8], [110, 145, 34, -4], [240, 34, -10, 28], [40, 90, 6, -36]];
    P.forEach(([x, y, dx, dy]) => { b += dot(x, y) + arr(x, y, x + dx, y + dy, 'hk1', RED, '', 2.4); });
    b += T(150, 186, 'thành bình', { a: 'middle', c: GREY });
    return wrap('0 0 300 194', b, cap, 'Các phân tử khí chuyển động trong bình');
  },
  vaCham: (cap = 'Va chạm vuông góc, đàn hồi.') => {
    let b = defs('vc1') + defs('vc2');
    b += tuong(250, 14, 150);
    b += T(8, 44, 'trước', { w: 700 }) + dot(120, 52, 8) + arr(132, 52, 220, 52, 'vc1', RED) + T(176, 40, '+mv', { c: RED, w: 700, a: 'middle' });
    b += T(8, 118, 'sau', { w: 700 }) + dot(220, 112, 8) + arr(208, 112, 120, 112, 'vc2', BLUE, '7 4') + T(164, 100, '?', { c: BLUE, w: 700, a: 'middle', size: 24 });
    b += ln(120, 146, 250, 146, GREY, 2) + ln(120, 140, 120, 152, GREY, 2) + T(185, 170, 'l', { a: 'middle', size: 22 }) + arr(14, 146, 70, 146, 'vc1') + T(74, 152, 'x');
    return wrap('0 0 280 176', b, cap, 'Phân tử va chạm đàn hồi với thành bình');
  },
  phanBo: (cap = 'Phân bố tốc độ phân tử của cùng một khí ở hai nhiệt độ T<sub>1</sub>, T<sub>2</sub>.') => {
    let b = defs('pb1');
    const X0 = 36, Y0 = 170, W = 250, H = 140;
    b += arr(X0, Y0, X0 + W, Y0, 'pb1') + arr(X0, Y0, X0, Y0 - H - 10, 'pb1');
    const cv = (a, c, dash, id) => {
      const pts = Array.from({ length: 61 }, (_, i) => { const v = i * 4; const f = (v * v) / (a ** 3) * Math.exp(-(v * v) / (a * a)); return [X0 + v, f]; });
      return pts;
    };
    const A1 = 60, A2 = 105;
    const c1 = cv(A1), c2 = cv(A2), mx = Math.max(...c1.map((p) => p[1]));
    const path = (pts, c, dash) => `<path d="${pts.map((p, i) => `${i ? 'L' : 'M'}${p[0].toFixed(1)},${(Y0 - (p[1] / mx) * (H - 14)).toFixed(1)}`).join(' ')}" fill="none" stroke="${c}" stroke-width="${SW}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
    b += path(c1, RED, '') + path(c2, BLUE, '8 5');
    const pk2 = c2.reduce((m, p) => (p[1] > m[1] ? p : m));
    b += T(X0 + A1 + 16, Y0 - H + 14, `T${sb('1')}`, { c: RED, w: 700 }) + T(pk2[0] + 22, Y0 - (pk2[1] / mx) * (H - 14) - 4, `T${sb('2')}`, { c: BLUE, w: 700 });
    b += T(X0 + W, Y0 + 24, 'tốc độ v', { a: 'end' }) + T(X0 + 8, 20, 'số phân tử');
    return wrap('0 0 300 200', b, cap, 'Hai đường phân bố tốc độ phân tử');
  },
  binhKin: (cap = 'Bình kín nhúng trong nước đun dần; đọc áp kế và nhiệt kế.') => {
    let b = '';
    b += `<path d="M20,70 L20,200 L200,200 L200,70" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<path d="M20,88 q15,-8 30,0 t30,0 t30,0 t30,0 t30,0 t30,0" fill="none" stroke="${BLUE}" stroke-width="2.4" stroke-dasharray="7 4"/>`;
    b += `<circle cx="90" cy="148" r="36" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(90, 155, 'khí', { a: 'middle', w: 700 });
    b += ln(90, 112, 90, 40, INK, 3) + ln(90, 40, 236, 40, INK, 3) + ln(236, 40, 236, 64, INK, 3);
    b += `<circle cx="236" cy="96" r="32" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + ln(236, 96, 254, 76, RED, 3) + `<circle cx="236" cy="96" r="4" fill="${INK}"/>`;
    b += T(236, 154, 'áp kế', { a: 'middle' });
    b += `<rect x="156" y="30" width="12" height="150" rx="6" fill="#fff" stroke="${INK}" stroke-width="2.4"/><circle cx="162" cy="182" r="9" fill="${RED}"/>` + T(150, 24, 'nhiệt kế', { a: 'middle' });
    b += T(110, 226, 'nước đun nóng dần', { a: 'middle' });
    return wrap('0 0 290 236', b, cap, 'Thí nghiệm đo áp suất khí trong bình kín theo nhiệt độ');
  },
  thang: (cap = 'Cùng một nhiệt độ đọc trên hai thang. Thang nào có gốc 0 thật?') => {
    let b = '';
    const Y = { 0: 196, 273: 112, 293: 78, 313: 44 };
    b += ln(110, 30, 110, 150) + ln(110, 176, 110, 200) + `<path d="M100,150 L120,158 L100,166 L120,174" fill="none" stroke="${INK}" stroke-width="2.4"/>`;
    b += ln(190, 30, 190, 150) + ln(190, 176, 190, 200) + `<path d="M180,150 L200,158 L180,166 L200,174" fill="none" stroke="${INK}" stroke-width="2.4"/>`;
    for (const [kv, y] of Object.entries(Y)) {
      b += ln(102, y, 118, y, INK, 2.4) + ln(182, y, 198, y, INK, 2.4) + ln(118, y, 182, y, GREY, 1.6, '4 4');
      b += T(94, y + 7, `${(kv - 273).toString().replace('-', '−')}`, { a: 'end' }) + T(206, y + 7, kv === '293' || kv === '313' ? '?' : `${kv}`, { w: kv > 280 ? 700 : 400 });
    }
    b += T(110, 20, '°C', { a: 'middle', w: 700 }) + T(190, 20, 'K', { a: 'middle', w: 700 });
    return wrap('0 0 280 210', b, cap, 'Thang Celsius và thang Kelvin đặt cạnh nhau');
  },
  binhN2: (cap = 'Bình kín 3,0 lít chứa 0,20 mol N<sub>2</sub> ở 27 °C.') => {
    let b = binh(40, 40, 150, 140) + `<rect x="94" y="20" width="42" height="22" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    [[70, 80], [120, 66], [160, 98], [88, 130], [140, 150], [168, 140], [60, 160], [116, 110]].forEach(([x, y]) => { b += dot(x, y, 5, '#fff'); });
    b += T(206, 80, `N${sb('2')}`, { w: 700 }) + T(206, 112, '3,0 lít') + T(206, 144, '27 °C');
    return wrap('0 0 290 196', b, cap, 'Bình khí nitơ');
  },
  // ===== Bài tập mẫu =====
  honHop: (cap = 'Cùng một bình, cùng 47 °C.') => {
    let b = binh(16, 12, 200, 106);
    [[50, 40], [100, 30], [170, 50], [70, 96], [140, 90], [196, 104], [120, 108]].forEach(([x, y]) => { b += dot(x, y, 5, '#fff'); });
    [[60, 68], [130, 56], [180, 80], [100, 92], [40, 100], [160, 100]].forEach(([x, y]) => { b += dot(x, y, 11, '#fff'); });
    b += dot(236, 46, 5, '#fff') + T(248, 53, `H${sb('2')}`) + dot(236, 90, 11, '#fff') + T(252, 97, `O${sb('2')}`);
    return wrap('0 0 300 128', b, cap, 'Hỗn hợp hydrogen và oxygen trong bình kín');
  },
  truocSau: (cap = 'Cùng bình: hút bớt một nửa số phân tử rồi nung.') => {
    let b = defs('ts1');
    b += binh(8, 30, 120, 130) + binh(184, 30, 120, 130);
    [[30, 60], [60, 50], [96, 70], [40, 100], [80, 96], [110, 120], [30, 140], [70, 138]].forEach(([x, y]) => { b += dot(x, y, 5, '#fff'); });
    [[214, 60], [270, 84], [230, 120], [284, 140]].forEach(([x, y]) => { b += dot(x, y, 5, '#fff'); });
    b += arr(134, 95, 176, 95, 'ts1');
    b += T(68, 22, 'trước', { a: 'middle', w: 700 }) + T(244, 22, 'sau', { a: 'middle', w: 700 });
    b += T(68, 186, `${gk('μ')}, p, T = ?`, { a: 'middle' }) + T(244, 186, `${gk('μ')}/2, 117 °C`, { a: 'middle' });
    return wrap('0 0 312 196', b, cap, 'Bình khí trước và sau khi hút bớt rồi nung');
  },
};
