// Hình minh hoạ cho ruột tập VL12 · Bài 12 Hiện tượng cảm ứng điện từ (lesson 13). Cùng quy tắc với hinh.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh: không vẽ chiều dòng cảm ứng, không vẽ chiều B cảm ứng, kim điện kế ở 0.
// Xem thử: node scripts/ruot-tap/l12-c3-bai12.mjs --hinh (chụp vào out/hinh-l12-c3-bai12/).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
// chữ Hi Lạp: Source Sans 3 chỉ nạp latin/vietnamese → lấy từ KaTeX_Math (đã nạp qua katex.min.css)
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const arr = (x1, y1, x2, y2, id, c = INK, dash = '', w = SW) =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;

// Nam châm thẳng nằm ngang: nửa trái nhãn L, nửa phải nhãn R (N đỏ, S xanh, chữ trắng)
const magH = (x, y, w, h, L, R) => {
  const c = (s) => (s === 'N' ? RED : BLUE);
  return `<rect x="${x}" y="${y}" width="${w / 2}" height="${h}" fill="${c(L)}" stroke="${INK}" stroke-width="2"/>`
    + `<rect x="${x + w / 2}" y="${y}" width="${w / 2}" height="${h}" fill="${c(R)}" stroke="${INK}" stroke-width="2"/>`
    + T(x + w / 4, y + h / 2 + 7, L, { a: 'middle', w: 700, c: '#fff', size: 21 }) + T(x + 3 * w / 4, y + h / 2 + 7, R, { a: 'middle', w: 700, c: '#fff', size: 21 });
};
// Nam châm thẳng đứng: nửa trên nhãn U, nửa dưới nhãn D
const magV = (x, y, w, h, U, D) => {
  const c = (s) => (s === 'N' ? RED : BLUE);
  return `<rect x="${x}" y="${y}" width="${w}" height="${h / 2}" fill="${c(U)}" stroke="${INK}" stroke-width="2"/>`
    + `<rect x="${x}" y="${y + h / 2}" width="${w}" height="${h / 2}" fill="${c(D)}" stroke="${INK}" stroke-width="2"/>`
    + T(x + w / 2, y + h / 4 + 7, U, { a: 'middle', w: 700, c: '#fff', size: 21 }) + T(x + w / 2, y + 3 * h / 4 + 7, D, { a: 'middle', w: 700, c: '#fff', size: 21 });
};
// Cuộn dây nhìn ngang: n vòng elip dọc theo trục ngang
const cuon = (x0, cy, n = 6, gap = 16, ry = 34) => Array.from({ length: n }, (_, i) =>
  `<ellipse cx="${x0 + i * gap}" cy="${cy}" rx="8" ry="${ry}" fill="none" stroke="${INK}" stroke-width="2.4"/>`).join('');
// Điện kế: kim ở vạch 0 (không lộ đáp án)
const dienKe = (cx, cy, r = 24) => `<circle cx="${cx}" cy="${cy}" r="${r}" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
  + `<path d="M${cx - r + 7},${cy - 2} A${r - 7},${r - 7} 0 0 1 ${cx + r - 7},${cy - 2}" fill="none" stroke="${GREY}" stroke-width="1.8"/>`
  + ln(cx, cy + 4, cx, cy - r + 6, INK, 2.4) + T(cx, cy + r - 4, 'G', { a: 'middle', w: 700, size: 20 });
// Kí hiệu B vào giấy (⊗) / ra khỏi giấy (⊙) vẽ bằng nét
const vao = (x, y, r = 8) => `<circle cx="${x}" cy="${y}" r="${r}" fill="#fff" stroke="${GREY}" stroke-width="1.8"/>`
  + ln(x - r * .7, y - r * .7, x + r * .7, y + r * .7, GREY, 1.8) + ln(x - r * .7, y + r * .7, x + r * .7, y - r * .7, GREY, 1.8);
const ra = (x, y, r = 8) => `<circle cx="${x}" cy="${y}" r="${r}" fill="#fff" stroke="${GREY}" stroke-width="1.8"/><circle cx="${x}" cy="${y}" r="2.6" fill="${GREY}"/>`;

// Nam châm + cuộn dây nối điện kế; o.mui: 'vao' (một mũi tên đưa vào) | 'hai' (vào ⇄ ra) | ''
const namChamCuon = (cap, o = {}) => {
  const { mui = 'vao', id = 'nc' } = o;
  let b = defs(id);
  b += magH(8, 45, 112, 30, 'S', 'N');
  b += cuon(170, 60, 6, 16, 34);
  b += ln(170, 94, 170, 150) + ln(170, 150, 189, 150) + ln(250, 94, 250, 150) + ln(250, 150, 237, 150);
  b += dienKe(213, 150);
  b += T(210, 18, 'cuộn dây', { a: 'middle' });
  if (mui === 'vao') b += arr(40, 104, 112, 104, id, INK, '7 4') + T(76, 132, 'đưa vào', { a: 'middle' });
  if (mui === 'hai') {
    b += arr(20, 100, 112, 100, id, INK) + T(66, 124, 'đưa vào', { a: 'middle' });
    b += arr(112, 146, 20, 146, id, INK, '7 4') + T(66, 172, 'rút ra', { a: 'middle' });
  }
  return wrap('0 0 280 184', b, cap, 'Thanh nam châm và cuộn dây nối điện kế');
};

// Khung dây nhìn nghiêng (cạnh khung là đoạn đậm) trong từ trường đều nằm ngang.
// o.nDeg: góc pháp tuyến so với B; o.mode: 'alpha' (cung α giữa n và B) | 'mat' (cung giữa mặt khung và B, ghi o.matLabel; n có dấu ?)
const khungNghieng = (cap, o = {}) => {
  const { nDeg = 40, mode = 'alpha', matLabel = '30°', id = 'kn', gon = false } = o;
  const C = [140, gon ? 66 : 82], L = gon ? 44 : 52, NL = gon ? 60 : 72, rad = (d) => (d * Math.PI) / 180;
  const n = [Math.cos(rad(nDeg)), -Math.sin(rad(nDeg))], p = [Math.sin(rad(nDeg)), Math.cos(rad(nDeg))];
  let b = defs(id + 'b') + defs(id + 'n');
  (gon ? [14, 40, 92, 118] : [18, 50, 114, 146]).forEach((y) => { b += arr(10, y, 270, y, id + 'b', GREY, '', 2); });
  b += T(276, gon ? 20 : 24, 'B', { w: 700, c: GREY });
  b += ln(C[0], C[1], 250, C[1], GREY, 1.8, '5 4');
  b += ln(C[0] - L * p[0], C[1] - L * p[1], C[0] + L * p[0], C[1] + L * p[1], INK, 6);
  const nE = [C[0] + NL * n[0], C[1] + NL * n[1]];
  b += arr(...C, ...nE, id + 'n', RED) + T(nE[0] + 8, nE[1] + 4, 'n', { w: 700, c: RED });
  if (mode === 'alpha') {
    const R = 40, E = [C[0] + R * n[0], C[1] + R * n[1]];
    b += `<path d="M${C[0] + R},${C[1]} A${R},${R} 0 0 0 ${E[0].toFixed(1)},${E[1].toFixed(1)}" fill="none" stroke="${INK}" stroke-width="2"/>`;
    b += T(C[0] + R + 8, C[1] - 10, gk('α'), { size: 22 });
  } else {
    // mặt khung đi lên về phía trái: hướng (−p) có y âm khi nDeg < 90
    const R = gon ? 38 : 44, d = [-p[0], -p[1]], E = [C[0] + R * d[0], C[1] + R * d[1]];
    b += `<path d="M${C[0] - R},${C[1]} A${R},${R} 0 0 1 ${E[0].toFixed(1)},${E[1].toFixed(1)}" fill="none" stroke="${INK}" stroke-width="2"/>`;
    b += ln(C[0] - 70, C[1], C[0], C[1], GREY, 1.8, '5 4');
    b += T(C[0] - R - 8, C[1] - 14, matLabel, { a: 'end', w: 700 });
    b += T(nE[0] + 30, nE[1] + 34, `${gk('α')} = ?`, { size: 20 });
  }
  b += T(C[0] + L * p[0] + 8, C[1] + L * p[1] + 4, 'khung', { size: 20 });
  return wrap(`0 0 300 ${gon ? 128 : 162}`, b, cap, 'Khung dây nhìn nghiêng trong từ trường đều');
};

// Vòng (hoặc khung vuông) dây kín trong mặt giấy, B vuông góc giấy
const vongGiay = (cap, o = {}) => {
  const { ki = 'vao', vuong = false, nhan = '' } = o;
  let b = '';
  const W = vuong ? 240 : 280, H = vuong ? 190 : 132, cx = W / 2, cy = H / 2;
  for (let x = 22; x <= W - 16; x += 48) for (let y = 20; y <= H - 14; y += 46) b += ki === 'vao' ? vao(x, y) : ra(x, y);
  b += vuong ? `<rect x="${cx - 62}" y="${cy - 62}" width="124" height="124" fill="none" stroke="${INK}" stroke-width="4"/>`
    : `<circle cx="${cx}" cy="${cy}" r="54" fill="none" stroke="${INK}" stroke-width="4"/>`;
  if (nhan) b += `<rect x="${cx - 50}" y="${cy - 12}" width="100" height="26" rx="4" fill="#fff"/>` + T(cx, cy + 8, nhan, { a: 'middle', w: 700 });
  return wrap(`0 0 ${W} ${H}`, b, cap, 'Vòng dây kín trong từ trường vuông góc mặt giấy');
};

// Đồ thị Φ–t gồm các đoạn thẳng: pts [[t (s), Φ (mWb)]…], nhan: nhãn trục t ở các điểm gãy (sau gốc), doan: đánh số (1)(2)(3)
const doThi = (cap, o = {}) => {
  const { id = 'dt', pts = [[0, 0], [0.1, 20], [0.3, 20], [0.35, 0]], max = 20, sx = 640, doan = true,
    nhan = [['0,10', 'middle'], ['0,30', 'end'], ['0,35', 'middle']] } = o;
  let b = defs(id);
  const X = (s) => 50 + s * sx, Y = (mw) => 156 - (mw / max) * 100;
  b += arr(50, 160, 318, 160, id, INK, '', 2.4) + arr(50, 160, 50, 14, id, INK, '', 2.4);
  b += T(58, 22, `${gk('Φ')} (mWb)`, { size: 20 }) + T(326, 146, 't (s)', { a: 'end' });
  b += ln(50, Y(max), X(pts[2][0]), Y(max), GREY, 1.6, '4 4') + T(44, Y(max) + 7, String(max), { a: 'end' });
  pts.slice(1).forEach(([s], i) => {
    b += ln(X(s), 160, X(s), Y(max), GREY, 1.4, '4 4');
    const [txt, a] = nhan[i];
    b += T(X(s) + (a === 'end' ? 4 : 0), 184, txt, { a });
  });
  b += T(44, 166, '0', { a: 'end' });
  b += `<polyline points="${pts.map(([s, f]) => `${X(s)},${Y(f)}`).join(' ')}" fill="none" stroke="${RED}" stroke-width="3.4"/>`;
  if (doan) {
    const mid = (i) => [(X(pts[i][0]) + X(pts[i + 1][0])) / 2, (Y(pts[i][1]) + Y(pts[i + 1][1])) / 2];
    b += T(mid(0)[0] - 10, mid(0)[1] - 4, '(1)', { a: 'end', w: 700 }) + T(mid(1)[0], mid(1)[1] - 8, '(2)', { a: 'middle', w: 700 }) + T(mid(2)[0] + 8, mid(2)[1] - 4, '(3)', { w: 700 });
  }
  return wrap('0 0 330 194', b, cap, 'Đồ thị từ thông theo thời gian');
};

export const hinhL12c3b12 = {
  // ===== Trang học bài mới =====
  duDoan: (cap = 'Cuộn dây nối điện kế, không có pin. Kim đang ở vạch 0.') => namChamCuon(cap, { mui: 'vao', id: 'dd' }),
  tuThong: (cap = 'Cạnh khung nhìn nghiêng; n vuông góc mặt khung.') => khungNghieng(cap, { nDeg: 40, id: 'tt' }),
  thiNghiem: (cap = 'Mỗi thao tác: nhìn kim điện kế.') => namChamCuon(cap, { mui: 'hai', id: 'tn' }),
  lenz: (cap = 'Cực N đang lại gần vòng dây kín. Đường nét đứt: từ trường của nam châm.') => {
    let b = defs('lz1') + defs('lz2');
    b += `<ellipse cx="80" cy="84" rx="15" ry="56" fill="none" stroke="${INK}" stroke-width="4"/>`;
    b += T(80, 168, 'vòng dây', { a: 'middle' });
    b += magH(176, 69, 120, 30, 'N', 'S');
    [64, 84, 104].forEach((y) => { b += arr(170, y, 108, y, 'lz1', BLUE, '7 4'); });
    b += T(134, 50, 'B', { w: 700, c: BLUE, a: 'middle' });
    b += arr(260, 128, 196, 128, 'lz2', RED) + T(272, 134, 'v', { w: 700, c: RED });
    b += T(18, 44, `B${sb('c')}?`, { w: 700 });
    return wrap('0 0 300 180', b, cap, 'Nam châm lại gần vòng dây kín');
  },
  ongNhom: (cap = '1: nam châm; 2: cục nhôm.') => {
    let b = `<rect x="16" y="8" width="64" height="184" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<rect x="28" y="24" width="16" height="22" fill="${RED}" stroke="${INK}" stroke-width="2"/><rect x="52" y="24" width="16" height="22" fill="#fff" stroke="${INK}" stroke-width="2"/>`;
    b += T(36, 70, '1', { a: 'middle', w: 700 }) + T(60, 70, '2', { a: 'middle', w: 700 });
    b += T(88, 120, 'ống', { w: 700 }) + T(88, 144, 'nhôm');
    return wrap('0 0 140 200', b, cap, 'Nam châm và cục nhôm thả vào ống nhôm');
  },
  thanhTruot: (cap = 'Thanh trượt sang phải trên hai ray; B hướng ra khỏi giấy.') => {
    let b = defs('tr1');
    for (let x = 76; x <= 290; x += 46) for (const y of [62, 128]) if (Math.abs(x - 214) > 14) b += ra(x, y);
    b += ln(40, 36, 304, 36) + ln(40, 156, 304, 156);
    b += ln(40, 36, 40, 74) + `<rect x="30" y="74" width="20" height="44" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + ln(40, 118, 40, 156);
    b += T(22, 103, 'R', { w: 700, a: 'end' });
    b += ln(192, 26, 192, 166, INK, 6);
    b += arr(200, 96, 252, 96, 'tr1', RED) + T(258, 102, 'v', { w: 700, c: RED });
    b += T(176, 104, `<tspan font-family="KaTeX_Main">ℓ</tspan>`, { a: 'end', size: 22 });
    b += T(300, 186, 'B ra', { a: 'end', c: GREY, w: 700 });
    return wrap('0 0 310 194', b, cap, 'Thanh kim loại trượt trên hai ray');
  },
  khungMau: (cap = 'Mặt khung vuông góc B; B tăng đều.') => vongGiay(cap, { ki: 'vao', vuong: true }),
  // ===== Bài tập mẫu =====
  khungD1: (cap = '') => khungNghieng(cap, { nDeg: 60, mode: 'mat', id: 'd1', gon: true }),
  doThiD5: (cap = 'Từ thông qua vòng dây theo thời gian.') => doThi(cap, { id: 'd5' }),
  // ===== Bài tương tự =====
  doThiTT: (cap = '') => doThi(cap, { id: 'd5t', pts: [[0, 0], [0.04, 12], [0.1, 12], [0.16, 0]], max: 12, sx: 1400,
    nhan: [['0,040', 'middle'], ['0,10', 'middle'], ['0,16', 'middle']], doan: false }),
  roiTT: (cap = 'Nhìn từ trên xuống.') => {
    let b = defs('rt');
    b += magV(64, 6, 32, 76, 'S', 'N');
    b += arr(124, 24, 124, 78, 'rt', RED) + T(132, 60, 'v', { w: 700, c: RED });
    b += `<ellipse cx="80" cy="124" rx="62" ry="16" fill="none" stroke="${INK}" stroke-width="4"/>`;
    b += T(80, 164, 'vòng dây', { a: 'middle' });
    return wrap('0 0 170 172', b, cap, 'Nam châm rơi theo trục về phía vòng dây');
  },
};
