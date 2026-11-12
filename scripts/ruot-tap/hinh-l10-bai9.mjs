// Hình minh hoạ cho ruột tập VL10 · Bài 9 Chuyển động thẳng biến đổi đều (lesson 54). Cùng quy tắc với hinh-l10-bai23.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh (hình phanh: đoạn trượt thứ hai vẽ đứt quãng, không theo tỉ lệ).
// Xem thử: node scripts/ruot-tap/l10-bai9.mjs --hinh (chụp vào out/hinh-l10-bai9/).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
const gk = (ch) => `<tspan font-family="KaTeX_Main">${ch}</tspan>`;
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const arr = (x1, y1, x2, y2, id, c = INK, dash = '', w = SW) =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const R = (d) => (d * Math.PI) / 180;
const f1 = (v) => (+v).toFixed(1);
const dat = (x1, x2, y) => ln(x1, y, x2, y) + Array.from({ length: Math.floor((x2 - x1) / 18) }, (_, i) =>
  ln(x1 + 8 + i * 18, y, x1 + i * 18, y + 8, GREY, 1.8)).join('');
// ô tô nhìn ngang, đáy bánh tại y
const oto = (x, y, w = 58) => `<path d="M${x},${y - 9} L${x},${y - 24} L${x + w * 0.22},${y - 24} L${x + w * 0.34},${y - 38} L${x + w * 0.74},${y - 38} L${x + w * 0.86},${y - 24} L${x + w},${y - 22} L${x + w},${y - 9} Z" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
  + `<circle cx="${x + w * 0.22}" cy="${y - 7}" r="7" fill="#fff" stroke="${INK}" stroke-width="${SW}"/><circle cx="${x + w * 0.78}" cy="${y - 7}" r="7" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
const xemay = (x, y) => `<circle cx="${x + 8}" cy="${y - 8}" r="8" fill="#fff" stroke="${INK}" stroke-width="${SW}"/><circle cx="${x + 40}" cy="${y - 8}" r="8" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
  + `<path d="M${x + 8},${y - 8} L${x + 20},${y - 24} L${x + 34},${y - 24} L${x + 40},${y - 8}" fill="none" stroke="${INK}" stroke-width="${SW}"/>`
  + `<circle cx="${x + 26}" cy="${y - 38}" r="6" fill="#fff" stroke="${INK}" stroke-width="2.4"/>${ln(x + 26, y - 32, x + 26, y - 24, INK, 2.4)}`;

// Hệ trục v–t: gốc (ox,oy), sx đơn vị/giây, sy đơn vị/(m/s). Trả về {b, X, Y}
const truc = (ox, oy, wx, hy, id, nhanT = 't (s)', nhanV = 'v (m/s)') => {
  const b = defs(id) + arr(ox, oy, ox + wx, oy, id, INK, '', 2.4) + arr(ox, oy, ox, oy - hy, id, INK, '', 2.4)
    + T(ox + wx, oy + 24, nhanT, { a: 'end' }) + T(ox + 6, oy - hy + 4, nhanV);
  return b;
};

export const hinhL10b9 = {
  // Trang 1 · Dự đoán: hai lần phanh. Đoạn trượt lần 2 vẽ đứt + "?" — KHÔNG theo tỉ lệ (vẽ đúng tỉ lệ là lộ đáp án)
  phanh: (cap = 'Cùng xe, cùng đường, cùng cách phanh. Chỉ khác tốc độ lúc bắt đầu phanh.') => {
    let b = defs('ph');
    b += dat(6, 314, 74) + oto(14, 74) + T(14, 26, '36 km/h', { w: 700 });
    b += ln(76, 52, 76, 92, GREY, 2, '4 3') + ln(176, 52, 176, 92, GREY, 2, '4 3') + arr(80, 86, 172, 86, 'ph', RED, '', 2.4) + T(126, 112, '10 m', { a: 'middle', c: RED, w: 700 });
    b += dat(6, 314, 178) + oto(14, 178) + T(14, 130, '72 km/h', { w: 700 });
    b += ln(76, 156, 76, 196, GREY, 2, '4 3') + `<path d="M80,190 L150,190 M164,190 L176,182 L188,198 L200,190 L292,190" fill="none" stroke="${RED}" stroke-width="2.4" stroke-dasharray="7 4" marker-end="url(#ph)"/>`;
    b += T(118, 176, '? m', { a: 'middle', c: RED, w: 700 }) + T(312, 140, 'hình không', { a: 'end', c: GREY, size: 18 }) + T(312, 160, 'theo tỉ lệ', { a: 'end', c: GREY, size: 18 });
    return wrap('0 0 320 206', b, cap, 'Hai lần phanh ở hai tốc độ');
  },
  // Trang 2 · đồ thị v–t ba xe A, B, C (theo Hình 2 bài web): A 1→7 (dốc lên), B 7→1 (dốc xuống), C nằm ngang 3 m/s
  vt3: (cap = 'Ba xe A, B, C. Tam giác nét đứt trên đường A: đọc Δv, Δt.') => {
    const ox = 46, oy = 190, sx = 37, sy = 22;
    const X = (s) => ox + s * sx, Y = (v) => oy - v * sy;
    let b = truc(ox, oy, 274, 182, 'v3');
    for (let s = 1; s <= 6; s++) b += ln(X(s), oy, X(s), oy + 6, INK, 2) + (s % 2 === 0 ? T(X(s), oy + 24, String(s), { a: 'middle' }) : '');
    for (const v of [1, 3, 4, 5, 7]) b += ln(ox - 6, Y(v), ox, Y(v), INK, 2) + T(ox - 10, Y(v) + 7, String(v), { a: 'end' });
    b += ln(X(0), Y(1), X(6), Y(7), INK, SW) + T(X(6) + 6, Y(7) + 6, 'A', { w: 700 });
    b += ln(X(0), Y(7), X(6), Y(1), RED, SW, '9 5') + T(X(6) + 6, Y(1) + 6, 'B', { w: 700, c: RED });
    b += ln(X(0), Y(3), X(6), Y(3), BLUE, SW, '3 4') + T(X(6) + 6, Y(3) + 14, 'C', { w: 700, c: BLUE });
    // tam giác độ dốc A: từ t=4 (v=5) tới t=6 (v=7)
    b += ln(X(4), Y(5), X(6), Y(5), GREY, 2.2, '5 4') + ln(X(6), Y(5), X(6), Y(7), GREY, 2.2, '5 4');
    b += T(X(5), Y(5) + 22, gk('Δ') + 't', { a: 'middle', c: GREY }) + T(X(6) + 6, Y(6) + 10, gk('Δ') + 'v', { c: GREY });
    return wrap('0 0 320 222', b, cap, 'Đồ thị vận tốc – thời gian của ba xe');
  },
  // Trang 2 · diện tích dưới v–t: v0 = 2, a = 1, t = 4 → hình thang = chữ nhật + tam giác (để trống số đo cho HS điền)
  thang: (cap = 'v<sub>0</sub> = 2 m/s, a = 1 m/s², t = 4 s. Diện tích = chữ nhật + tam giác.') => {
    const ox = 46, oy = 186, sx = 54, sy = 25;
    const X = (s) => ox + s * sx, Y = (v) => oy - v * sy;
    let b = `<path d="M${X(0)},${oy} L${X(0)},${Y(2)} L${X(4)},${Y(2)} L${X(4)},${oy} Z" fill="#dfe8f6" stroke="${BLUE}" stroke-width="2"/>`;
    b += `<path d="M${X(0)},${Y(2)} L${X(4)},${Y(6)} L${X(4)},${Y(2)} Z" fill="#fff" stroke="${INK}" stroke-width="2" stroke-dasharray="5 4"/>`;
    b += truc(ox, oy, 274, 168, 'th');
    b += ln(X(0), Y(2), X(4), Y(6), INK, SW);
    b += T(ox - 10, Y(2) + 7, '2', { a: 'end' }) + T(ox - 10, Y(6) + 7, '6', { a: 'end' }) + ln(ox, Y(6), X(4), Y(6), GREY, 1.8, '3 4');
    b += T(X(4), oy + 24, '4', { a: 'middle' }) + T(X(2), Y(1) + 7, 'v' + sb('0') + 't', { a: 'middle', c: BLUE, w: 700 });
    b += T(X(3) + 4, Y(3.2) + 4, '½at²', { a: 'middle', w: 700 });
    return wrap('0 0 320 218', b, cap, 'Diện tích dưới đồ thị vận tốc – thời gian');
  },
  // Trang 2 · thí nghiệm máng nghiêng, cổng quang điện
  mang: (cap = 'Thả xe từ nghỉ. Cổng quang điện đặt cách chỗ thả 10, 20, 40, 60 cm.') => {
    const x0 = 14, y0 = 40, x1 = 306, y1 = 150, g = Math.atan2(y1 - y0, x1 - x0) * 180 / Math.PI;
    let b = defs('mg') + ln(x0, y0, x1, y1, INK, SW) + ln(x1 - 40, y1 + 30, x1, y1 + 30) + ln(x0, y0, x0, y1 + 30, GREY, 2) + ln(x0, y1 + 30, x1, y1 + 30, GREY, 2);
    b += `<g transform="rotate(${f1(g)} ${x0 + 30} ${y0 + 11})"><rect x="${x0 + 16}" y="${y0 - 10}" width="38" height="16" rx="3" fill="#fff" stroke="${INK}" stroke-width="${SW}"/><rect x="${x0 + 30}" y="${y0 - 24}" width="5" height="14" fill="${INK}"/></g>`;
    for (const u of [0.38, 0.66]) {
      const cx = x0 + u * (x1 - x0), cy = y0 + u * (y1 - y0);
      b += `<path d="M${f1(cx - 10)},${f1(cy - 4)} L${f1(cx - 10)},${f1(cy - 44)} L${f1(cx + 10)},${f1(cy - 44)} L${f1(cx + 10)},${f1(cy - 4)}" fill="none" stroke="${RED}" stroke-width="${SW}"/>`;
    }
    b += T(x0 + 0.38 * (x1 - x0), y0 + 0.38 * (y1 - y0) - 52, 'cổng 1', { a: 'middle', c: RED, size: 18 }) + T(x0 + 0.66 * (x1 - x0), y0 + 0.66 * (y1 - y0) - 52, 'cổng 2', { a: 'middle', c: RED, size: 18 });
    b += T(140, 172, 'đồng hồ hiện số', { size: 18, c: GREY });
    return wrap('0 0 320 186', b, cap, 'Xe lăn trên máng nghiêng qua cổng quang điện');
  },
  // Trang 3 · Bẫy 2: xe phanh tới dừng — đường v–t chạm trục t rồi nằm trên trục; nét đứt đi xuống dưới trục là sai
  bayDung: (cap = 'Phanh: v giảm tới 0 ở t<sub>d</sub>, rồi xe đứng yên. Phần nét đứt dưới trục t là sai.') => {
    const ox = 40, oy = 120, X = (s) => ox + s * 28, Y = (v) => oy - v * 9;
    let b = defs('bd') + arr(ox, oy, ox + 270, oy, 'bd', INK, '', 2.4) + arr(ox, 200, ox, 8, 'bd', INK, '', 2.4) + T(ox + 270, oy + 24, 't (s)', { a: 'end' }) + T(ox - 10, 18, 'v', { a: 'end' });
    b += ln(X(0), Y(10), X(5), Y(0), INK, SW) + ln(X(5), Y(0), X(9), Y(0), INK, 5);
    b += ln(X(5), Y(0), X(8), Y(-6), RED, SW, '7 5') + T(X(8) + 4, Y(-6) + 4, 'sai', { c: RED, w: 700 });
    b += T(X(5), oy - 10, 't' + sb('d'), { a: 'middle', w: 700 }) + T(ox - 8, Y(10) + 14, 'v' + sb('0'), { a: 'end' });
    return wrap('0 0 320 206', b, cap, 'Đồ thị vận tốc khi phanh tới dừng');
  },
  // Trang 4 · bài toán mẫu: ô tô ở vạch dừng, xe máy đi qua vạch cùng lúc
  haiXe: (cap = 'Lúc đèn xanh (t = 0): ô tô bắt đầu chạy, xe máy vừa qua vạch.') => {
    let b = defs('hx') + dat(6, 314, 96) + ln(70, 40, 70, 104, INK, 4) + T(76, 124, 'vạch dừng', { size: 18 });
    b += oto(10, 96) + T(36, 124, 'ô tô', { a: 'middle', size: 18 }) + arr(14, 42, 60, 42, 'hx', RED, '', 2.4) + T(10, 26, 'a = 2 m/s²', { c: RED, size: 18 });
    b += xemay(80, 96) + arr(132, 74, 186, 74, 'hx', BLUE, '6 4', 2.4) + T(190, 80, '10 m/s', { c: BLUE, size: 18 });
    b += arr(70, 160, 306, 160, 'hx', INK, '', 2.4) + T(70, 186, 'O', { a: 'middle', w: 700 }) + T(304, 186, 'x', { a: 'end', w: 700 });
    return wrap('0 0 320 196', b, cap, 'Ô tô và xe máy ở vạch dừng');
  },
  // Trang 5 · thử thách ⭐⭐⭐: phản xạ rồi phanh (không ghi số đáp án)
  phanXa: (cap = 'Thời gian phản xạ: xe còn chạy đều; sau đó mới chậm dần.') => {
    const ox = 40, oy = 170, X = (s) => ox + s * 86, Y = (v) => oy - v * 9;
    let b = truc(ox, oy, 274, 152, 'px');
    b += `<path d="M${X(0)},${Y(15)} L${X(0.8)},${Y(15)} L${X(3.3)},${oy}" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
    b += ln(X(0.8), Y(15), X(0.8), oy, GREY, 2, '5 4') + T(X(0.8), oy + 24, '0,8', { a: 'middle' }) + T(ox - 8, Y(15) + 7, '15', { a: 'end' });
    b += T(X(0.4), Y(7), 'phản', { a: 'middle', size: 18, c: GREY }) + T(X(0.4), Y(7) + 20, 'xạ', { a: 'middle', size: 18, c: GREY }) + T(X(1.7), Y(4), 'phanh', { a: 'middle', size: 18, c: GREY });
    return wrap('0 0 320 202', b, cap, 'Đồ thị v–t khi phản xạ rồi phanh');
  },
  // BTM Dạng 2: đồ thị theo đề (4 → 16 m/s trong 6 s, giữ tới 10 s, về 0 lúc 14 s)
  d2: () => {
    const ox = 40, oy = 176, X = (s) => ox + s * 16, Y = (v) => oy - v * 9;
    let b = truc(ox, oy, 280, 162, 'd2');
    b += `<path d="M${X(0)},${Y(4)} L${X(6)},${Y(16)} L${X(10)},${Y(16)} L${X(14)},${oy}" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
    for (const s of [6, 10, 14]) b += ln(X(s), oy, X(s), Y(16), GREY, 1.8, '4 4') + T(X(s), oy + 22, String(s), { a: 'middle' });
    b += T(ox - 8, Y(4) + 7, '4', { a: 'end' }) + T(ox - 8, Y(16) + 7, '16', { a: 'end' }) + ln(ox, Y(16), X(6), Y(16), GREY, 1.8, '4 4');
    return wrap('0 0 320 206', b, '', 'Đồ thị vận tốc – thời gian của xe ở Dạng 2');
  },
  // BTM Dạng 5: dốc AB rồi mặt ngang BC
  d5: () => {
    let b = defs('d5') + `<path d="M10,40 L150,150 L312,150" fill="none" stroke="${INK}" stroke-width="${SW}"/>` + dat(150, 312, 150);
    b += `<circle cx="22" cy="38" r="10" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += T(10, 76, 'A', { w: 700 }) + T(150, 178, 'B', { a: 'middle', w: 700 }) + T(300, 178, 'C', { a: 'middle', w: 700 });
    b += T(46, 130, '64 m', { size: 20 }) + T(74, 152, '8 s', { size: 20 }) + T(230, 140, '32 m', { a: 'middle' });
    b += arr(64, 54, 110, 90, 'd5', BLUE, '6 4', 2.4) + arr(180, 116, 260, 116, 'd5', BLUE, '6 4', 2.4);
    return wrap('0 0 320 188', b, '', 'Quả cầu lăn xuống dốc rồi lăn trên mặt ngang');
  },
  // BTM Dạng 6: dốc, ô tô ở chân đi lên, xe đạp ở đỉnh đi xuống; trục Ox từ chân dốc lên đỉnh
  d6: () => {
    const x0 = 16, y0 = 168, x1 = 300, y1 = 40, g = Math.atan2(y1 - y0, x1 - x0) * 180 / Math.PI;
    let b = defs('d6') + `<path d="M${x0},${y0} L${x1},${y1} L${x1},${y0} Z" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    const P = (u) => [f1(x0 + u * (x1 - x0)), f1(y0 + u * (y1 - y0))];
    b += `<g transform="translate(${P(0.1)}) rotate(${f1(g)})">${oto(-25, 0, 50)}</g>`;
    b += `<g transform="translate(${P(0.86)}) rotate(${f1(g)})">${xemay(-24, 0)}</g>`;
    b += `<text transform="translate(${P(0.55)}) rotate(${f1(g)}) translate(0 26)" font-size="18" fill="${INK}" text-anchor="middle">dốc dài 570 m</text>`;
    b += arr(x0 + 74, y0 - 72, x0 + 128, y0 - 96, 'd6', RED, '', 2.4) + T(x0 + 30, y0 - 84, '20 m/s', { c: RED, size: 18 });
    b += arr(x1 - 70, y1 - 26, x1 - 120, y1 - 4, 'd6', BLUE, '6 4', 2.4) + T(x1 - 160, y1 - 26, '2 m/s', { c: BLUE, size: 18 });
    b += T(x0, y0 + 24, 'O (chân dốc)', { size: 18 }) ;
    return wrap('0 0 320 196', b, '', 'Ô tô lên dốc, xe đạp xuống dốc');
  },
};
