// Hình minh hoạ cho ruột tập VL12 · Bài 1 Sự chuyển thể (lesson 2). Cùng quy tắc với hinh.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh. Xem thử: node scripts/ruot-tap/l12-bai1.mjs --hinh (chụp vào out/hinh-l12-bai1/).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
// mũi tên → ← trong <text> rơi về font hệ thống → lấy từ KaTeX_Main
const km = (ch) => `<tspan font-family="KaTeX_Main">${ch}</tspan>`;
const arr = (x1, y1, x2, y2, id, c = INK, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${SW}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const rect = (x, y, w, h, o = {}) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${o.rx ?? 3}" fill="${o.fill ?? '#fff'}" stroke="${o.c ?? INK}" stroke-width="${o.sw ?? SW}"${o.dash ? ` stroke-dasharray="${o.dash}"` : ''}/>`;
const dot = (x, y, r = 7, fill = '#fff') => `<circle cx="${x}" cy="${y}" r="${r}" fill="${fill}" stroke="${INK}" stroke-width="2.2"/>`;

// Cốc thuỷ tinh hình thang (miệng rộng hơn đáy), mực nước ở y = muc
const coc = (x, y, w, h, muc = null) => {
  const d = 8;
  let b = '';
  if (muc != null) b += `<path d="M${x + d * (muc - y) / h},${muc} L${x + w - d * (muc - y) / h},${muc} L${x + w - d},${y + h} L${x + d},${y + h} Z" fill="#e3ebf7" stroke="none"/>`;
  b += `<path d="M${x},${y} L${x + d},${y + h} L${x + w - d},${y + h} L${x + w},${y}" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
  return b;
};
// Nhiệt kế dọc: bầu ở dưới, ô số ở đỉnh
const nhietKe = (x, y1, y2, chu = '?') => `<rect x="${x - 5}" y="${y1}" width="10" height="${y2 - y1}" rx="5" fill="#fff" stroke="${INK}" stroke-width="2.2"/>`
  + `<circle cx="${x}" cy="${y2 + 4}" r="9" fill="${RED}" stroke="${INK}" stroke-width="2.2"/>` + ln(x, y2 - 2, x, y1 + (y2 - y1) * .45, RED, 4)
  + rect(x - 22, y1 - 34, 44, 28, { sw: 2 }) + T(x, y1 - 13, chu, { a: 'middle', w: 700 });

// Đồ thị nhiệt độ – thời gian: pts [[t, T, nhãn]], tx/ty: các mốc ghi số; khung viewBox 320 × 210
const doThi = (pts, o = {}) => {
  const { tMax, TMin = 0, TMax, tx = [], ty = [], cap = '', id = 'dt', nhan = true, dash = [] } = o;
  const X0 = 58, X1 = 300, Y0 = 176, Y1 = 26;
  const X = (v) => X0 + (v / tMax) * (X1 - X0), Y = (v) => Y0 - ((v - TMin) / (TMax - TMin)) * (Y0 - Y1);
  let b = defs(id);
  b += arr(X0, Y0, X1 + 14, Y0, id) + arr(X0, Y0, X0, Y1 - 16, id);
  b += T(X0 + 8, 16, 'T (°C)', { w: 700 }) + T(X1 + 14, Y0 + 40, 't (phút)', { a: 'end', w: 700 });
  tx.forEach((q) => { const [v, dx = 0] = [].concat(q); b += ln(X(v), Y0, X(v), Y0 + 6, INK, 2) + T(X(v) + dx, Y0 + 24, String(v), { a: 'middle' }); });
  ty.forEach((v) => { b += ln(X0 - 6, Y(v), X0, Y(v), INK, 2) + T(X0 - 9, Y(v) + 7, String(v).replace('-', '−'), { a: 'end' }); });
  dash.forEach(([tv, Tv]) => { b += ln(X(tv), Y(Tv), X(tv), Y0, GREY, 1.8, '5 4') + ln(X0, Y(Tv), X(tv), Y(Tv), GREY, 1.8, '5 4'); });
  b += `<polyline points="${pts.map(([a, c]) => `${X(a)},${Y(c)}`).join(' ')}" fill="none" stroke="${BLUE}" stroke-width="3.2" stroke-linejoin="round"/>`;
  if (nhan) pts.forEach(([a, c, s, dx = 0, dy = -10]) => { if (s) b += dot(X(a), Y(c), 4.5, INK) + T(X(a) + dx, Y(c) + dy, s, { a: 'middle', w: 700 }); });
  return wrap('0 0 330 222', b, cap, 'Đồ thị nhiệt độ theo thời gian');
};

export const hinhL12b1 = {
  // ===== Trang học bài mới =====
  liDa: (cap = 'Li đá đang tan giữa trưa nắng. Nhiệt kế chỉ bao nhiêu?') => {
    let b = coc(70, 70, 120, 130, 96);
    [[92, 104, 14], [124, 112, -10], [150, 100, 8]].forEach(([x, y, r]) => { b += `<rect x="${x}" y="${y}" width="28" height="28" rx="4" fill="#fff" stroke="${INK}" stroke-width="2.4" transform="rotate(${r} ${x + 14} ${y + 14})"/>`; });
    b += nhietKe(214, 64, 170);
    [[62, 120], [60, 150], [196, 132], [64, 180]].forEach(([x, y]) => { b += `<path d="M${x},${y - 7} Q${x + 5},${y} ${x},${y + 4} Q${x - 5},${y} ${x},${y - 7}" fill="${BLUE}"/>`; });
    b += defs('ld1') + arr(10, 40, 46, 66, 'ld1', RED, '7 4') + arr(286, 40, 250, 66, 'ld1', RED, '7 4') + T(112, 24, 'không khí nóng', { a: 'middle', c: RED });
    return wrap('0 0 300 212', b, cap, 'Li nước đá đang tan có cắm nhiệt kế');
  },
  baThe: (cap = 'Cùng một chất ở ba thể, nhìn ở mức phân tử.') => {
    let b = '';
    const o = [[6, 'Rắn'], [108, 'Lỏng'], [210, 'Khí']];
    o.forEach(([x, s]) => { b += rect(x, 30, 88, 96, { sw: 2.4 }) + T(x + 44, 22, s, { a: 'middle', w: 700 }); });
    for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) b += dot(22 + i * 19, 48 + j * 20, 7.5, '#cfdcf0');
    [[124, 104], [141, 110], [158, 103], [176, 108], [130, 86], [148, 90], [167, 85], [183, 88], [122, 68], [140, 72], [160, 66], [178, 70]].forEach(([x, y]) => { b += dot(x, y, 7.5, '#cfdcf0'); });
    [[230, 50], [276, 62], [248, 100], [286, 110], [228, 112]].forEach(([x, y], i) => {
      b += dot(x, y, 7.5, '#cfdcf0');
      const [dx, dy] = [[18, 10], [-14, 16], [20, -14], [-12, -18], [16, -6]][i];
      b += ln(x + dx * .6, y + dy * .6, x + dx * 1.5, y + dy * 1.5, GREY, 2, '4 3');
    });
    return wrap('0 0 304 134', b, cap, 'Phân tử ở thể rắn, lỏng, khí');
  },
  vong: (cap = 'Điền tên quá trình (1)–(6). Nét đứt: hai quá trình ít gặp.') => {
    let b = defs('vg1') + defs('vg2');
    const bx = [[8, 'RẮN'], [118, 'LỎNG'], [228, 'KHÍ']];
    bx.forEach(([x, s]) => { b += rect(x, 88, 84, 42) + T(x + 42, 116, s, { a: 'middle', w: 700 }); });
    b += arr(94, 98, 116, 98, 'vg1') + arr(116, 122, 94, 122, 'vg1') + arr(204, 98, 226, 98, 'vg1') + arr(226, 122, 204, 122, 'vg1');
    b += T(105, 80, '(1)', { a: 'middle', w: 700 }) + T(105, 152, '(2)', { a: 'middle', w: 700 }) + T(215, 80, '(3)', { a: 'middle', w: 700 }) + T(215, 152, '(4)', { a: 'middle', w: 700 });
    b += `<path d="M50,86 Q160,0 268,82" fill="none" stroke="${INK}" stroke-width="${SW}" stroke-dasharray="7 5" marker-end="url(#vg2)"/>` + T(160, 34, '(5)', { a: 'middle', w: 700 });
    b += `<path d="M268,132 Q160,214 52,136" fill="none" stroke="${INK}" stroke-width="${SW}" stroke-dasharray="7 5" marker-end="url(#vg2)"/>` + T(160, 200, '(6)', { a: 'middle', w: 700 });
    return wrap('0 0 320 210', b, cap, 'Sơ đồ sáu quá trình chuyển thể');
  },
  nuocDa: (cap = 'Đun 0,20 kg nước đá từ −6 °C, mỗi phút ghi nhiệt độ.') =>
    doThi([[0, -6], [1, 0], [4.2, 0], [9.1, 100], [35.5, 100]], { tMax: 38, TMin: -20, TMax: 120, tx: [0, 5, 10, 20, 30], ty: [0, 100], nhan: false, id: 'nd' }),
  bayHoiSoi: (cap = '(a) đĩa nước trước quạt, nhiệt độ phòng · (b) nồi nước trên bếp đang sủi bọt.') => {
    let b = defs('bs1') + T(6, 26, '(a)', { w: 700 }) + T(166, 26, '(b)', { w: 700 });
    b += `<path d="M20,120 L36,140 L124,140 L140,120" fill="none" stroke="${INK}" stroke-width="${SW}"/><path d="M28,130 L132,130 L124,140 L36,140 Z" fill="#e3ebf7"/>`;
    [44, 80, 116].forEach((x, i) => { b += dot(x, 122, 6, '#cfdcf0') + arr(x, 112, x + (i - 1) * 8, 74, 'bs1', BLUE, '6 4'); });
    b += coc(186, 50, 116, 100, 64);
    [[214, 130, 7], [236, 104, 9], [262, 124, 6], [280, 92, 8], [222, 82, 6], [254, 78, 7]].forEach(([x, y, r]) => { b += `<circle cx="${x}" cy="${y}" r="${r}" fill="#fff" stroke="${BLUE}" stroke-width="2.2"/>`; });
    b += `<path d="M200,172 Q210,154 218,172 M234,172 Q244,150 254,172 M270,172 Q280,154 288,172" fill="none" stroke="${RED}" stroke-width="3"/>` + ln(182, 152, 306, 152, INK, 4);
    return wrap('0 0 316 182', b, cap, 'Bay hơi ở đĩa nước và sôi ở nồi nước');
  },
  binhKhi: (cap = 'Bình 20 lít đã đầy oxygen; bơm thêm lượng khí mà ngoài trời chiếm 2 lít.') => {
    let b = defs('bk1') + rect(130, 30, 150, 120, { rx: 18 }) + T(205, 84, '20 lít', { a: 'middle', w: 700 }) + T(205, 116, 'V khí = ?', { a: 'middle' });
    b += rect(12, 70, 80, 40, { rx: 6, dash: '7 4' }) + T(52, 98, '2 lít', { a: 'middle' }) + arr(96, 90, 126, 90, 'bk1', BLUE);
    return wrap('0 0 292 160', b, cap, 'Bơm thêm khí vào bình kín');
  },
  truc: (cap = 'Chấm 13 điểm của bảng rồi nối lại.') => {
    const X0 = 50, X1 = 300, Y0 = 186, Y1 = 26, X = (v) => X0 + v * (X1 - X0) / 12, Y = (v) => Y0 - v * (Y0 - Y1) / 140;
    let b = defs('tr1');
    for (let v = 1; v <= 12; v++) b += ln(X(v), Y0, X(v), Y1, '#c3cce0', 1.2);
    for (let v = 20; v <= 140; v += 20) b += ln(X0, Y(v), X1, Y(v), '#c3cce0', 1.2);
    b += arr(X0, Y0, X1 + 14, Y0, 'tr1') + arr(X0, Y0, X0, Y1 - 16, 'tr1');
    for (let v = 0; v <= 12; v += 2) b += T(X(v), Y0 + 24, String(v), { a: 'middle' });
    for (let v = 20; v <= 140; v += 40) b += T(X0 - 12, Y(v) + 7, String(v), { a: 'end' });
    b += T(X0 + 10, 16, 'T (°C)', { w: 700 }) + T(X1 + 14, Y0 + 44, 't (phút)', { a: 'end', w: 700 });
    return wrap('0 0 330 236', b, cap, 'Hệ trục để vẽ đồ thị nhiệt độ – thời gian');
  },
  // ===== Bài tập mẫu =====
  cocD1: (cap = 'Cốc đá và đĩa nước sau 30 phút.') => {
    let b = coc(40, 40, 110, 130, 70);
    [[62, 80, 10], [100, 86, -8]].forEach(([x, y, r]) => { b += `<rect x="${x}" y="${y}" width="24" height="24" rx="4" fill="#fff" stroke="${INK}" stroke-width="2.4" transform="rotate(${r} ${x + 12} ${y + 12})"/>`; });
    [[30, 110], [158, 128], [34, 150]].forEach(([x, y]) => { b += `<path d="M${x},${y - 7} Q${x + 5},${y} ${x},${y + 4} Q${x - 5},${y} ${x},${y - 7}" fill="${BLUE}"/>`; });
    b += `<path d="M184,150 L196,166 L284,166 L296,150" fill="none" stroke="${INK}" stroke-width="${SW}"/><path d="M190,158 L290,158 L284,166 L196,166 Z" fill="#e3ebf7"/>`;
    b += T(100, 34, '(1)', { a: 'middle', w: 700, size: 34 }) + T(-26, 104, '(2)', { w: 700, size: 34 }) + T(240, 140, '(3)', { a: 'middle', w: 700, size: 34 });
    return wrap('-28 -4 332 182', b, cap, 'Cốc nước đá và đĩa nước');
  },
  binhD2: (cap = 'Ba bình rỗng 1,5 lít, đậy kín.') => {
    let b = '';
    [[10, 'sáp'], [110, 'dầu'], [210, 'He']].forEach(([x, s]) => { b += rect(x, 40, 84, 100, { rx: 14 }) + T(x + 42, 98, s, { a: 'middle', w: 700 }) + T(x + 42, 30, '1,5 lít', { a: 'middle' }); });
    return wrap('0 0 304 148', b, cap, 'Ba bình thuỷ tinh giống nhau');
  },
  doThiD4: (cap = 'BC, DE nằm ngang; đun nóng đều.') =>
    doThi([[0, 20, 'A', 0, 26], [2, 60, 'B', -8, -10], [7, 60, 'C', 6, 24], [12, 200, 'D', -10, -10], [20, 200, 'E'], [22, 280, 'F', -14, 0]],
      { tMax: 24, TMax: 300, tx: [2, 7, 12, [20, -7], [22, 9]], ty: [20, 60, 200, 280], dash: [[2, 60], [7, 60], [12, 200], [20, 200], [22, 280]], id: 'd4' }),
  // ===== Bài tương tự =====
  doThiT1: (cap = 'BC, DE nằm ngang; đun nóng đều.') =>
    doThi([[0, 20, 'A', 0, 26], [3, 80, 'B', -8, -10], [7, 80, 'C', 6, 24], [12, 230, 'D', -10, -10], [19, 230, 'E'], [21, 290, 'F', -14, 0]],
      { tMax: 23, TMax: 310, tx: [3, 7, 12, 19], ty: [20, 80, 230, 290], dash: [[3, 80], [7, 80], [12, 230], [19, 230], [21, 290]], id: 't1' }),
  doThiT2: (cap = 'Làm nguội đều hơi của chất Z.') =>
    doThi([[0, 150, 'A', 18, -2], [2, 110, 'B', 0, -10], [6, 110, 'C', 6, -10], [10, 30, 'D', 0, -10], [16, 30, 'E', 0, -10], [18, 10, 'F', 0, -10]],
      { tMax: 20, TMax: 160, tx: [2, 6, 10, 16], ty: [30, 110, 150], dash: [[2, 110], [6, 110], [10, 30], [16, 30]], id: 't2' }),
};
