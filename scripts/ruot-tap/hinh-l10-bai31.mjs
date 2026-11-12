// Hình minh hoạ cho ruột tập VL10 · Bài 31 Động học của chuyển động tròn đều (lesson 76). Cùng quy tắc với hinh.mjs/hinh-l10-bai23.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh (hình Dự đoán không vẽ quỹ đạo tròn của từng người — vẽ ra là lộ "ngoài đi xa hơn").
// Xem thử: node scripts/ruot-tap/xem-hinh.mjs (hoặc node scripts/ruot-tap/l10-bai31.mjs --hinh → out/hinh-l10-bai31/).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
// chữ Hi Lạp lấy từ KaTeX_Math (Source Sans 3 chỉ nạp latin/vietnamese, ω θ π rơi về Helvetica)
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const D = '<tspan font-family="KaTeX_Main">Δ</tspan>';
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const vec = (s) => `<tspan font-weight="700">${s}</tspan>`;
const R = (d) => (d * Math.PI) / 180;
const f1 = (v) => Number(v).toFixed(1);
const arr = (x1, y1, x2, y2, id, c = INK, dash = '', w = SW) =>
  `<line x1="${f1(x1)}" y1="${f1(y1)}" x2="${f1(x2)}" y2="${f1(y2)}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${f1(x1)}" y1="${f1(y1)}" x2="${f1(x2)}" y2="${f1(y2)}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const tron = (x, y, r, { c = INK, w = SW, fill = 'none', dash = '' } = {}) =>
  `<circle cx="${f1(x)}" cy="${f1(y)}" r="${r}" fill="${fill}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const cham = (x, y, r = 5, c = INK) => `<circle cx="${f1(x)}" cy="${f1(y)}" r="${r}" fill="${c}"/>`;
// điểm trên đường tròn tâm (x,y) bán kính r, góc a (độ, ngược chiều kim đồng hồ từ phải sang, y hướng xuống)
const P = (x, y, r, a) => [x + r * Math.cos(R(a)), y - r * Math.sin(R(a))];
// cung từ a1 tới a2 (a2 > a1: đi ngược chiều kim đồng hồ); mũi tên ở cuối khi có id
const cung = (x, y, r, a1, a2, { c = INK, w = 2.4, id = '', dash = '' } = {}) => {
  const [xa, ya] = P(x, y, r, a1), [xb, yb] = P(x, y, r, a2);
  const lon = Math.abs(a2 - a1) > 180 ? 1 : 0, sw = a2 > a1 ? 0 : 1;
  return `<path d="M${f1(xa)},${f1(ya)} A${r},${r} 0 ${lon} ${sw} ${f1(xb)},${f1(yb)}" fill="none" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}${id ? ` marker-end="url(#${id})"` : ''}/>`;
};

// Quỹ đạo tròn nhìn từ trên: tâm O, các điểm có tên; v: true vẽ mẫu vectơ vận tốc (ngược chiều kim đồng hồ) tại điểm đó
const vong = ({ cap, label, id, r = 74, diem = [], nhanR = '', nhanRxy = null, quay = true, banKinh = true, vb = '0 0 300 210', x = 120, y = 104 }) => {
  let b = defs(id + 'a') + defs(id + 'b');
  b += tron(x, y, r) + cham(x, y, 4) + T(x - 8, y + 24, 'O', { a: 'end' });
  if (quay) b += cung(x, y, r + 20, 200, 240, { id: id + 'b', c: BLUE, dash: '6 4' });
  diem.forEach(({ g, ten, v = false, dx = 10, dy = -10, a = 'start' }) => {
    const [px, py] = P(x, y, r, g);
    if (banKinh) b += ln(x, y, px, py, GREY, 2, '5 4');
    b += cham(px, py, 6) + T(px + dx, py + dy, ten, { w: 700, a });
    if (v) { const [tx, ty] = [-Math.sin(R(g)), -Math.cos(R(g))]; b += arr(px, py, px + 62 * tx, py + 62 * ty, id + 'a', RED) + T(px + 62 * tx - 6, py + 62 * ty - 8, vec('v'), { c: RED, a: 'end' }); }
  });
  if (nhanR) b += nhanRxy ? T(x + nhanRxy[0], y + nhanRxy[1], nhanR, { a: 'start', size: 18 }) : T(x, y - 12, nhanR, { a: 'middle' });
  return wrap(vb, b, cap, label);
};

// Đĩa quay có hai điểm M (mép) và N (bên trong)
const dia = ({ cap, id, nhanD, nhanN, rN = 40 }) => {
  const x = 112, y = 108, r = 84;
  let b = defs(id + 'a');
  b += tron(x, y, r, { fill: '#fff' }) + tron(x, y, 7, { fill: GREY }) + cung(x, y, r + 16, 100, 150, { id: id + 'a', c: BLUE, dash: '6 4' });
  b += ln(x - r, y, x + r, y, GREY, 2, '5 4') + T(x - 30, y - 12, nhanD, { a: 'middle' });
  const [mx, my] = P(x, y, r, 40), [nx, ny] = P(x, y, rN, -40);
  b += cham(mx, my, 6) + T(mx + 10, my - 4, 'M', { w: 700 });
  b += ln(x, y, nx, ny, INK, 2.4) + cham(nx, ny, 6) + T(nx + 10, ny + 16, 'N', { w: 700 }) + T(x + r + 10, y + 64, nhanN, { a: 'start' }) + ln(x + rN * 0.38, y + rN * 0.32 + 4, x + r + 8, y + 58, GREY, 1.6);
  return wrap('0 0 310 206', b, cap, 'Đĩa quay, điểm M ở mép, điểm N bên trong');
};

export const hinhL10b31 = {
  // Trang 1 · Dự đoán: hàng người nắm tay xoay quanh người trụ (nhìn từ trên). Không vẽ quỹ đạo từng người.
  hangXoay: (cap = 'Nhìn từ trên xuống: cả hàng nắm tay, luôn thẳng, quay quanh người trụ O.') => {
    const x0 = 36, y0 = 118, g = 18;
    let b = defs('hx1');
    b += cung(x0, y0, 26, 40, 150, { id: 'hx1', c: BLUE, dash: '5 4' });
    const pts = [0, 1, 2, 3, 4].map((k) => P(x0, y0, k * 62, g));
    b += ln(pts[0][0], pts[0][1], pts[4][0], pts[4][1], GREY, 2.4);
    pts.forEach(([px, py], k) => { b += tron(px, py, 13, { fill: k === 0 ? GREY : '#fff' }); });
    b += T(x0, y0 + 40, 'O', { a: 'middle', w: 700 });
    b += T(pts[1][0] + 4, pts[1][1] + 38, 'người 2', { a: 'middle' });
    b += T(pts[4][0] - 4, pts[4][1] + 40, 'ngoài cùng', { a: 'middle' });
    return wrap('0 0 300 170', b, cap, 'Hàng người xoay quanh người trụ');
  },
  // Trang 1 · thí nghiệm 1 rad: cung dài đúng bằng bán kính
  radian: (cap = 'Sợi chỉ dài bằng bán kính, quấn theo vành từ A tới B. Góc AOB bao nhiêu độ?') => {
    const x = 104, y = 112, r = 86;
    let b = tron(x, y, r, { c: GREY, w: 2.2 });
    const [ax, ay] = P(x, y, r, 0), [bx, by] = P(x, y, r, 57.3);
    b += ln(x, y, ax, ay) + ln(x, y, bx, by) + cung(x, y, r, 0, 57.3, { c: RED, w: 6 });
    b += cung(x, y, 24, 0, 57.3, { w: 2 }) + T(x + 30, y - 12, '?', { w: 700 });
    b += cham(x, y, 4) + T(x - 8, y + 22, 'O', { a: 'end' }) + cham(ax, ay, 5) + T(ax + 8, ay + 8, 'A', { w: 700 }) + cham(bx, by, 5) + T(bx + 6, by - 8, 'B', { w: 700 });
    b += T(x + r / 2, y + 24, 'r', { a: 'middle' }) + T(ax + 14, ay - 52, 'cung = r', { c: RED });
    return wrap('0 0 300 206', b, cap, 'Cung dài bằng bán kính');
  },
  // Trang 2 · thí nghiệm đĩa xoay lò vi sóng
  diaLoVi: (cap = 'Mẩu băng dính cách tâm 14,0 cm. Bấm giờ đĩa quay 3 vòng.') => {
    const x = 118, y = 104, r = 86;
    let b = defs('lv1');
    b += tron(x, y, r, { fill: '#fff' }) + tron(x, y, 26, { dash: '5 4', c: GREY, w: 2.2 }) + T(x, y + 7, 'cốc', { a: 'middle', size: 20 });
    const [mx, my] = P(x, y, 70, -20);
    b += ln(x, y, mx, my, GREY, 2, '5 4') + `<rect x="${f1(mx - 8)}" y="${f1(my - 6)}" width="16" height="12" fill="${INK}"/>`;
    b += T(x - 4, y + 56, '14,0 cm', { a: 'middle' });
    b += cung(x, y, r + 14, 60, 120, { id: 'lv1', c: BLUE, dash: '6 4' });
    return wrap('0 0 300 210', b, cap, 'Đĩa xoay có mẩu băng dính ở mép');
  },
  // Trang 2 · II.3: cùng góc quét, hai điểm ở hai bán kính
  haiDiem: (cap = 'Hai điểm cùng quay một góc <span style="font-family:KaTeX_Main">Δ</span><i style="font-family:KaTeX_Math">θ</i> trong cùng thời gian. Cung nào dài hơn?') => {
    const x = 22, y = 188, a1 = 8, a2 = 44, r1 = 110, r2 = 236;
    let b = ln(x, y, ...P(x, y, r2 + 10, a1)) + ln(x, y, ...P(x, y, r2 + 10, a2));
    b += cung(x, y, r1, a1, a2, { c: RED, w: 4 }) + cung(x, y, r2, a1, a2, { c: RED, w: 4, dash: '10 5' });
    b += cung(x, y, 40, a1, a2, { w: 2 }) + T(x + 46, y - 18, `${D}${gk('θ')}`);
    const [p1x, p1y] = P(x, y, r1, a1), [p2x, p2y] = P(x, y, r2, a1);
    b += cham(p1x, p1y, 6) + cham(p2x, p2y, 6) + T(p1x, p1y + 26, '1', { w: 700, a: 'middle' }) + T(p2x, p2y + 26, '2', { w: 700, a: 'middle' });
    const [l1x, l1y] = P(x, y, r1 + 22, 30), [l2x, l2y] = P(x, y, r2 + 18, 30);
    b += T(l1x, l1y, `${D}s${sb('1')}`, { c: RED }) + T(l2x, l2y, `${D}s${sb('2')}`, { c: RED });
    b += cham(x, y, 4) + T(x + 2, y - 8 - 0, '', {}) + T(x - 4, y + 2, 'O', { a: 'end' });
    return wrap('0 0 300 200', b, cap, 'Hai điểm khác bán kính cùng quay một góc');
  },
  // Trang 3 · II.4: mẫu v tại B, em vẽ tại A, C, D
  veVanToc: (cap = 'Vật quay ngược chiều kim đồng hồ. Mẫu: <b>v</b> tại B. Em vẽ <b>v</b> tại A, C, D.') => vong({
    cap, id: 'vv', label: 'Vẽ vectơ vận tốc tại bốn điểm',
    diem: [{ g: 0, ten: 'A', dx: 10, dy: 26 }, { g: 90, ten: 'B', v: true, dx: 12, dy: -6 }, { g: 180, ten: 'C', dx: -10, dy: 26, a: 'end' }, { g: 270, ten: 'D', dx: 12, dy: 24 }],
  }),
  // Trang 4 · bài toán mẫu bánh xe đạp
  banhXe: (cap = 'Bánh xe đường kính 60 cm, quay đều 120 vòng/phút. Bán kính quỹ đạo của M là bao nhiêu mét?') => {
    const x = 118, y = 106, r = 86;
    let b = defs('bx1');
    b += tron(x, y, r, { w: 6 }) + tron(x, y, 9, { fill: GREY });
    for (let k = 0; k < 12; k++) { const [sx, sy] = P(x, y, r - 3, k * 30); b += ln(x, y, sx, sy, GREY, 1.4); }
    b += ln(x - r, y + r + 16, x + r, y + r + 16, INK, 2) + ln(x - r, y + r + 8, x - r, y + r + 24, INK, 2) + ln(x + r, y + r + 8, x + r, y + r + 24, INK, 2);
    b += `<rect x="${x - 48}" y="${y + r + 4}" width="96" height="22" fill="#fff"/>` + T(x, y + r + 22, 'd = 60 cm', { a: 'middle' });
    const [mx, my] = P(x, y, r, 35);
    b += cham(mx, my, 7, RED) + T(mx + 10, my - 6, 'M', { w: 700, c: RED });
    b += cung(x, y, r + 18, 120, 165, { id: 'bx1', c: BLUE, dash: '6 4' });
    return wrap('0 0 300 222', b, cap, 'Bánh xe đạp và điểm M trên vành');
  },
  // Trang 5 · thử thách ⭐⭐⭐: Hà Nội quay quanh trục Trái Đất
  traiDat: (cap = 'Hà Nội (H) ở vĩ độ 21°, quay quanh trục Bắc–Nam. Đoạn nào là bán kính quỹ đạo của H?') => {
    const x = 176, y = 112, r = 86;
    let b = tron(x, y, r, { fill: '#fff' });
    b += ln(x, y - r - 18, x, y + r + 18, GREY, 2.2, '7 5') + T(x + 6, y - r - 2, 'Bắc');
    b += ln(x - r, y, x + r, y, GREY, 2, '4 4') + T(x - r - 4, y + 24, 'xích đạo', { a: 'end', size: 20 });
    const [hx, hy] = P(x, y, r, 21);
    b += ln(x, y, hx, hy, INK, 2.4) + cham(hx, hy, 6, RED) + T(hx + 10, hy - 4, 'H', { w: 700, c: RED });
    b += ln(x, hy, hx, hy, RED, 2.4, '6 4') + T(x + 26, hy - 8, 'r = ?', { c: RED });
    b += cung(x, y, 36, 0, 21, { w: 2 }) + T(x + 42, y - 2, '21°', { size: 20 }) + T(x + 50, y + 26, 'R');
    b += cham(x, y, 4) + T(x - 8, y + 24, 'O', { a: 'end' });
    return wrap('0 0 300 222', b, cap, 'Trái Đất tự quay, điểm H ở vĩ độ 21°');
  },
  // Trang 6 · Dạng 1: xe đồ chơi trên ray tròn, qua A
  ray: (cap = 'Xe đang qua A. Em vẽ <b>v</b> tại A.') => vong({
    cap, id: 'ry', label: 'Ray tròn, điểm A bên phải tâm', nhanR: 'r = 0,50 m', r: 62, vb: '0 8 300 170', x: 130, y: 92,
    diem: [{ g: 0, ten: 'A', dx: 10, dy: 26 }],
  }),
  // Trang 7 · Dạng 4: đĩa than
  diaThan: (cap = 'M ở mép đĩa, N cách tâm 5,0 cm. Hai điểm chung đại lượng nào?') => dia({ cap, id: 'dt', nhanD: 'd = 30 cm', nhanN: '5,0 cm', rN: 40 }),
  // Trang 7 · Dạng 5: cánh quạt
  canhQuat: (cap = 'Đầu cánh vạch đường tròn bán kính bằng chiều dài cánh.') => {
    const x = 60, y = 104, L = 196;
    let b = defs('cq1');
    b += tron(x, y, L, { c: GREY, w: 2, dash: '6 5' });
    b += `<path d="M${x},${y - 6} L${x + L - 14},${y - 16} Q${x + L + 4},${y} ${x + L - 14},${y + 16} L${x},${y + 6} z" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<path d="M${x},${y - 6} L${x - 40},${y - 14} Q${x - 52},${y} ${x - 40},${y + 14} L${x},${y + 6} z" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += tron(x, y, 12, { fill: GREY });
    b += ln(x, y + 34, x + L, y + 34, INK, 2) + ln(x, y + 26, x, y + 42, INK, 2) + ln(x + L, y + 26, x + L, y + 42, INK, 2) + T(x + L / 2, y + 60, `r${sb('1')} = 0,40 m`, { a: 'middle' });
    b += cham(x + L, y, 6, RED) + cung(x, y, L, 10, 30, { id: 'cq1', c: BLUE, w: 2.8 });
    return wrap('0 0 300 190', b, cap, 'Cánh quạt quay quanh trục');
  },
  // Trang 8 · Bài tương tự D1·2: vòng xuyến, điểm D thấp nhất (phía nam)
  vongXuyen: (cap = 'Xe đi ngược chiều kim đồng hồ (nhìn từ trên), đang qua D.') => vong({
    cap, id: 'vx', label: 'Vòng xuyến, xe qua điểm D', nhanR: 'r = 20 m', nhanRxy: [6, 40], r: 84, vb: '0 12 300 202', x: 136, y: 100,
    diem: [{ g: 270, ten: 'D', dx: 12, dy: 24 }],
  }),
  // Trang 9 · Bài tương tự D4·1: đĩa CD
  diaCD: (cap = 'Đĩa CD: M ở mép, N cách tâm 2,0 cm.') => dia({ cap, id: 'cd', nhanD: 'd = 12 cm', nhanN: '2,0 cm', rN: 40 }),
};
