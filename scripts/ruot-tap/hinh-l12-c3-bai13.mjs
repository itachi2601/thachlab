// Hình minh hoạ cho ruột tập VL12 · Chương 3 · Bài 13 Đại cương về dòng điện xoay chiều (lesson 14). Cùng quy tắc với hinh.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh (đỉnh sóng ổ điện để "?", không ghi 311 V; hình bài tập chỉ vẽ dữ kiện đề).
// Xem thử: node scripts/ruot-tap/l12-c3-bai13.mjs --hinh (chụp vào out/hinh-l12-c3-bai13/).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
// chữ Hi Lạp: Source Sans 3 chỉ nạp latin/vietnamese → lấy từ KaTeX_Math (đã nạp qua katex.min.css)
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
// √ trong SVG: font hình chỉ có BV → lấy từ KaTeX_Main
const can = '<tspan font-family="KaTeX_Main">√</tspan>';
// chữ Hi Lạp trong chú thích HTML
const gH = (ch) => `<span style="font-family:KaTeX_Math;font-style:italic">${ch}</span>`;
const gM = (ch) => `<span style="font-family:KaTeX_Main">${ch}</span>`;
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const arr = (x1, y1, x2, y2, id, c = INK, dash = '', w = SW) =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
// đường cos: từ x0 đến x0+w, trục ở y0, biên độ A (đơn vị viewBox), chu kì Tp (đơn vị viewBox), pha ban đầu ph (rad)
const song = (x0, y0, w, A, Tp, ph = 0, c = INK, dash = '', sw = SW) => {
  const pts = [];
  for (let x = 0; x <= w + .01; x += 2) pts.push(`${(x0 + x).toFixed(1)},${(y0 - A * Math.cos(2 * Math.PI * x / Tp + ph)).toFixed(1)}`);
  return `<polyline points="${pts.join(' ')}" fill="none" stroke="${c}" stroke-width="${sw}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
};
// trục toạ độ: gốc (x0,y0), trục t dài w, trục tung cao h lên và h xuống
const truc = (x0, y0, w, h, nhan, id) => defs(id) + arr(x0, y0, x0 + w, y0, id, INK, '', 2) + arr(x0, y0 + h, x0, y0 - h, id, INK, '', 2)
  + T(x0 + w - 2, y0 + 24, 't', { a: 'end' }) + T(x0 + 8, y0 - h + 12, nhan);
const cham = (x, y, c = INK, r = 5) => `<circle cx="${x}" cy="${y}" r="${r}" fill="${c}"/>`;
// khung dây nhìn dọc trục: tâm (cx,cy), pháp tuyến hợp B góc a (độ, B nằm ngang hướng phải)
const khung = (cx, cy, a, id, o = {}) => {
  const { L = 62, nL = 74, cung = true } = o;
  const r = (a * Math.PI) / 180, ux = Math.cos(r), uy = -Math.sin(r);   // pháp tuyến
  const vx = -uy, vy = ux;                                               // mặt khung ⟂ pháp tuyến
  let b = ln(cx - vx * L, cy - vy * L, cx + vx * L, cy + vy * L, INK, 6);
  b += `<circle cx="${cx}" cy="${cy}" r="6" fill="#fff" stroke="${INK}" stroke-width="2.4"/>`;
  b += arr(cx, cy, cx + ux * nL, cy + uy * nL, id, RED, '', 3) + T(cx + ux * (nL + 8), cy + uy * (nL + 8) + (uy < -0.3 ? 0 : 6), 'n', { c: RED, w: 700, a: ux < -0.2 ? 'end' : 'start' });
  if (cung && a > 8) {
    const R = 30, ex = cx + R * Math.cos(r), ey = cy - R * Math.sin(r);
    b += `<path d="M${cx + R},${cy} A${R},${R} 0 0 0 ${ex.toFixed(1)},${ey.toFixed(1)}" fill="none" stroke="${INK}" stroke-width="2"/>`;
    const m = r / 2;
    b += T(cx + (R + 12) * Math.cos(m), cy - (R + 12) * Math.sin(m) + 6, gk('α'));
  }
  return b;
};
const duongB = (x1, x2, ys, id) => ys.map((y) => arr(x1, y, x2, y, id, BLUE, '8 5', 2.4)).join('');

export const hinhL12c3b13 = {
  // ===== Trang học bài mới =====
  // Dự đoán: dao động ký ở ổ điện — đỉnh để "?" (không lộ 311 V)
  oDien: (cap = 'Ổ điện ghi 220 V – 50 Hz. Đỉnh sóng trên màn: ?') => {
    let b = `<rect x="14" y="46" width="72" height="96" rx="10" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
      + `<rect x="36" y="74" width="8" height="22" rx="2" fill="${INK}"/><rect x="56" y="74" width="8" height="22" rx="2" fill="${INK}"/>`
      + T(50, 66, '220 V', { a: 'middle', size: 18, w: 700 }) + T(50, 36, 'ổ điện', { a: 'middle' });
    b += `<path d="M40,96 C40,170 120,170 132,120" fill="none" stroke="${GREY}" stroke-width="2.4"/><path d="M60,96 C64,150 120,150 132,104" fill="none" stroke="${GREY}" stroke-width="2.4"/>`;
    b += `<rect x="132" y="22" width="160" height="150" rx="6" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += ln(142, 97, 282, 97, GREY, 1.6) + song(142, 97, 140, 52, 70, 0, BLUE, '', 3);
    b += ln(142, 45, 282, 45, GREY, 1.6, '5 4') + T(287, 52, '?', { w: 700, c: RED, size: 24, a: 'end' });
    b += T(212, 194, 'dao động ký', { a: 'middle' });
    return wrap('0 0 300 202', b, cap, 'Dao động ký nối vào ổ điện, đỉnh sóng chưa biết');
  },
  // II.1: khung quay nhìn dọc trục, B ngang, pháp tuyến n hợp B góc α
  khungQuay: (cap = `Nhìn dọc trục quay. Khung quay đều thì ${gH('α')} = ${gH('ω')}t + ${gH('φ')} tăng đều.`) => {
    let b = defs('kq1') + defs('kq2') + defs('kq3');
    b += duongB(20, 290, [30, 196], 'kq1') + T(290, 22, 'B', { c: BLUE, w: 700, a: 'end' });
    b += khung(150, 113, 50, 'kq2', { L: 64, nL: 80 });
    b += `<path d="M196,174 A70,70 0 0 0 216,130" fill="none" stroke="${INK}" stroke-width="2.2" marker-end="url(#kq3)"/>` + T(222, 172, gk('ω'), { size: 22 });
    return wrap('0 0 300 206', b, cap, 'Khung dây quay quanh trục vuông góc với từ trường');
  },
  // Thí nghiệm máy phát mini quay tay → dao động ký, đọc U0
  mayPhat: (cap = 'Quay tay đều n vòng/s, đọc biên độ U<sub>0</sub> trên màn.') => {
    let b = defs('mp1');
    b += `<rect x="12" y="62" width="92" height="74" rx="8" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(58, 106, 'máy phát', { a: 'middle', size: 18 });
    b += ln(58, 62, 58, 30, INK, 3) + ln(58, 30, 92, 30, INK, 3) + `<circle cx="92" cy="30" r="6" fill="${INK}"/>`;
    b += `<path d="M24,40 A36,24 0 0 1 40,22" fill="none" stroke="${INK}" stroke-width="2" marker-end="url(#mp1)"/>`;
    b += ln(104, 84, 140, 84, GREY, 2.4) + ln(104, 114, 140, 114, GREY, 2.4);
    b += `<rect x="140" y="24" width="152" height="140" rx="6" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += ln(150, 94, 282, 94, GREY, 1.6) + song(150, 94, 132, 44, 66, 0, BLUE, '', 3);
    b += ln(160, 50, 160, 94, RED, 2) + ln(154, 50, 166, 50, RED, 2) + T(170, 72, `U${sb('0')}`, { c: RED, w: 700 });
    b += T(216, 188, 'dao động ký', { a: 'middle' });
    return wrap('0 0 300 196', b, cap, 'Máy phát mini quay tay nối dao động ký');
  },
  // Thí nghiệm hai LED mắc song song ngược chiều
  haiLed: (cap = 'Hai LED song song, ngược chiều, qua điện trở bảo vệ R.') => {
    const led = (x, xuong) => {
      const y1 = 80, y2 = 110, tip = xuong ? y2 : y1, day = xuong ? y1 : y2;
      return ln(x, 50, x, y1, INK, 2.6) + ln(x, y2, x, 140, INK, 2.6)
        + `<path d="M${x - 15},${day} L${x + 15},${day} L${x},${tip} Z" fill="#fff" stroke="${INK}" stroke-width="2.6"/>` + ln(x - 15, tip, x + 15, tip, INK, 2.6);
    };
    let b = ln(60, 50, 270, 50, INK, 2.6) + ln(60, 140, 270, 140, INK, 2.6) + ln(60, 50, 60, 140, INK, 2.6);
    b += `<rect x="96" y="40" width="56" height="20" fill="#fff" stroke="${INK}" stroke-width="2.6"/>` + T(124, 32, 'R', { a: 'middle', w: 700 });
    b += led(200, true) + led(270, false);
    b += T(180, 102, '1', { w: 700, a: 'end' }) + T(290, 102, '2', { w: 700 });
    b += `<circle cx="60" cy="95" r="22" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(60, 104, '~', { a: 'middle', w: 700, size: 30 });
    b += T(16, 176, 'máy phát tín hiệu', { size: 20 }) + T(235, 176, 'LED 1, 2', { a: 'middle', size: 20 });
    return wrap('0 0 300 186', b, cap, 'Hai đèn LED mắc song song ngược chiều với nguồn xoay chiều');
  },
  // II.3: u(t) ổ điện, mức hiệu dụng nét đứt, đỉnh để trống
  dienAp: (cap = 'Đường liền: u(t). Nét đứt: mức hiệu dụng U = 220 V. Đỉnh U<sub>0</sub> = ?') => {
    let b = truc(30, 100, 262, 86, 'u', 'da1');
    b += song(30, 100, 240, 70, 120, 0, BLUE, '', 3);
    b += ln(30, 50.5, 270, 50.5, RED, 2, '7 5') + T(274, 46, 'U', { c: RED, w: 700, a: 'end' });
    b += ln(24, 30, 36, 30, INK, 2) + T(58, 30, `U${sb('0')} = ?`, { w: 700 });
    b += ln(30, 182, 150, 182, GREY, 2) + ln(30, 176, 30, 188, GREY, 2) + ln(150, 176, 150, 188, GREY, 2) + T(160, 190, 'T');
    return wrap('0 0 300 196', b, cap, 'Đồ thị điện áp ổ điện theo thời gian');
  },
  // Bẫy 2: Φ (liền) và e (đứt) theo thời gian
  phiE: (cap = `Đường liền: ${gM('Φ')}. Nét đứt: e. Đọc e ở chỗ ${gM('Φ')} đạt đỉnh.`) => {
    let b = truc(24, 96, 268, 82, '', 'pe1');
    b += song(24, 96, 248, 64, 128, 0, INK, '', 3) + song(24, 96, 248, 64, 128, -Math.PI / 2, RED, '8 5', 3);
    b += T(40, 22, gk('Φ'), { w: 700, size: 22 }) + T(72, 22, 'e', { c: RED, w: 700, size: 22 });
    b += ln(88, 18, 88, 176, GREY, 1.6, '3 4') + ln(152, 18, 152, 176, GREY, 1.6, '3 4');
    return wrap('0 0 300 186', b, cap, 'Đồ thị từ thông và suất điện động theo thời gian');
  },
  // Bài toán mẫu: i(t) chỉ ghi dữ kiện (i(0) = 2 A, đang giảm), I0 để trống
  iMau: (cap = 'Lúc t = 0: i = 2 A và đang giảm.') => {
    let b = truc(30, 72, 262, 64, 'i', 'im1') + defs('im2');
    b += song(30, 72, 240, 50, 120, Math.PI / 4, BLUE, '', 3);
    b += cham(30, 72 - 50 * Math.cos(Math.PI / 4), RED) + T(52, 34, '2 A', { c: RED, w: 700 });
    b += arr(46, 46, 64, 66, 'im2', RED, '', 2.4);
    b += ln(24, 22, 36, 22, INK, 2) + T(270, 20, `I${sb('0')} = ?`, { w: 700, a: 'end' });
    return wrap('0 0 300 142', b, cap, 'Đồ thị cường độ dòng điện, điểm lúc t = 0');
  },
  // ===== Bài tập mẫu =====
  // Dạng 3: chỉ vẽ dữ kiện (i(0) = −√2 A, đang tăng)
  d3: (cap = 'Dữ kiện lúc t = 0. Pha ban đầu dấu gì?') => {
    let b = truc(30, 48, 262, 42, 'i', 'd31') + defs('d32');
    b += cham(30, 72, RED) + T(42, 92, `−${can}2 A`, { c: RED, w: 700 });
    b += arr(48, 66, 66, 46, 'd32', RED, '', 2.4) + T(76, 70, 'đang tăng', { c: RED });
    b += T(270, 24, `I${sb('0')} = I${can}2`, { a: 'end' });
    return wrap('0 0 300 98', b, cap, 'Điểm của dòng điện lúc t = 0');
  },
  // Dạng 2: i (liền) và i² (đứt) — nhiệt theo i², trung bình i² để trống
  d2: (cap = 'Liền: i. Đứt: i².') => {
    let b = truc(30, 50, 262, 46, '', 'd21');
    b += song(30, 50, 240, 38, 120, 0, BLUE, '', 3);
    const pts = []; for (let x = 0; x <= 240; x += 2) pts.push(`${30 + x},${(50 - 38 * Math.cos(2 * Math.PI * x / 120) ** 2).toFixed(1)}`);
    b += `<polyline points="${pts.join(' ')}" fill="none" stroke="${RED}" stroke-width="3" stroke-dasharray="7 5"/>`;
    b += T(44, 18, 'i', { c: BLUE, w: 700 }) + T(62, 18, 'i²', { c: RED, w: 700 });
    return wrap('0 0 300 98', b, cap, 'Đồ thị cường độ dòng điện và bình phương của nó');
  },
  // Dạng 4: khung lúc t = 0, pháp tuyến cùng hướng B
  d4: (cap = 'Lúc t = 0: n cùng hướng B.') => {
    let b = defs('d41') + defs('d42');
    b += duongB(16, 290, [26, 136], 'd41') + T(290, 18, 'B', { c: BLUE, w: 700, a: 'end' });
    b += khung(130, 81, 0, 'd42', { L: 44, nL: 86, cung: false });
    b += T(30, 86, 'khung', { c: GREY });
    return wrap('0 0 300 146', b, cap, 'Khung dây lúc t = 0 nhìn dọc trục');
  },
  // Dạng 5: u(t) với hai mức ngưỡng ±100√3 V (không tô vùng sáng)
  d5: (cap = `Nét đứt: |u| = 100${gM('√')}3 V. Đèn sáng ở phần nào của sóng?`) => {
    let b = truc(30, 96, 262, 84, 'u', 'd51');
    b += song(30, 96, 240, 74, 120, 0, BLUE, '', 3);
    const h = 74 * Math.sqrt(3) / 2; b = b.replace(`>u</text>`, '></text>');
    b += ln(30, 96 - h, 272, 96 - h, RED, 2, '7 5') + ln(30, 96 + h, 272, 96 + h, RED, 2, '7 5');
    b += T(272, 96 - h - 8, `+100${can}3`, { c: RED, a: 'end', size: 18 }) + T(272, 96 + h + 22, `−100${can}3`, { c: RED, a: 'end', size: 18 });
    b += T(150, 16, '200 V', { size: 18, a: 'middle' });
    return wrap('0 0 300 190', b, cap, 'Điện áp đặt vào đèn và hai mức ngưỡng');
  },
};
