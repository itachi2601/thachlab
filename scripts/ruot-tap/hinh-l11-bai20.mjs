// Hình minh hoạ cho ruột tập VL11 · Bài 20 Điện thế (lesson 39). Cùng quy tắc với hinh.mjs/hinh-l10-bai23.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh. Xem thử: node scripts/ruot-tap/l11-bai20.mjs --hinh (chụp vào out/hinh-l11-bai20/).
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
const dot = (x, y, r = 5, c = INK) => `<circle cx="${x}" cy="${y}" r="${r}" fill="${c}"/>`;
const R = (d) => (d * Math.PI) / 180;
const f1 = (v) => v.toFixed(1);
const cung = (x, y, r, a1, a2, c = INK) => {
  const p = (a) => `${f1(x + r * Math.cos(R(a)))},${f1(y - r * Math.sin(R(a)))}`;
  return `<path d="M${p(a1)} A${r},${r} 0 0 0 ${p(a2)}" fill="none" stroke="${c}" stroke-width="2.2"/>`;
};
const dat = (x1, x2, y) => ln(x1, y, x2, y) + Array.from({ length: Math.floor((x2 - x1) / 18) }, (_, i) =>
  ln(x1 + 8 + i * 18, y, x1 + i * 18, y + 8, GREY, 1.8)).join('');
// mũi tên hai đầu (đo khoảng cách)
const doDai = (x1, y1, x2, y2, id, c = BLUE) => `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="2.2" marker-start="url(#${id})" marker-end="url(#${id})"/>`;
const defs2 = (id) => `<defs><marker id="${id}" markerWidth="7" markerHeight="7" refX="3.5" refY="3.5" orient="auto-start-reverse" markerUnits="strokeWidth"><path d="M0,0 L7,3.5 L0,7 z" fill="context-stroke"/></marker></defs>`;

// Đường sức ngang, M → N đi thẳng và đi cong; hình chiếu d của MN lên đường sức
const duongDi = (cap, { d = 'd = ?', id = 'dd' } = {}) => {
  let b = defs(id + 'a') + defs(id + 'b') + defs2(id + 'c');
  [14, 100].forEach((y) => { b += arr(8, y, 300, y, id + 'a', GREY, '', 2); });
  b += T(306, 38, 'E', { w: 700, c: GREY, a: 'end' });
  const M = [50, 84], N = [240, 34];
  b += `<path d="M${M} C 80,10 190,130 ${N}" fill="none" stroke="${RED}" stroke-width="${SW}" stroke-dasharray="7 5"/>`;
  b += arr(M[0], M[1], N[0] - 6, N[1] + 2, id + 'b', INK);
  b += dot(...M) + dot(...N) + T(M[0] - 10, M[1] + 4, 'M', { w: 700, a: 'end' }) + T(N[0] + 8, N[1] - 4, 'N', { w: 700 });
  b += ln(M[0], M[1], M[0], 140, GREY, 2, '4 4') + ln(N[0], N[1], N[0], 140, GREY, 2, '4 4');
  b += doDai(M[0] + 2, 134, N[0] - 2, 134, id + 'c') + T((M[0] + N[0]) / 2, 126, d, { c: BLUE, w: 700, a: 'middle' });
  return wrap('0 0 320 144', b, cap, 'Hai đường đi từ M đến N trong điện trường đều');
};

// Hai bản song song dựng đứng: trái/phải, đường sức từ bản dương sang bản âm, điểm M, đo khoảng cách
const haiBan = (cap, { trai = '−', phai = '+', nhanT = '', nhanP = '', mx = 0.25, mLab = '', mBen = 'trai', tong = '', e = false, id = 'hb' } = {}) => {
  let b = defs(id + 'a') + defs2(id + 'c') + defs(id + 'b');
  const xL = 40, xR = 280, y1 = 34, y2 = 150;
  b += `<rect x="${xL - 8}" y="${y1}" width="8" height="${y2 - y1}" fill="${INK}"/><rect x="${xR}" y="${y1}" width="8" height="${y2 - y1}" fill="${INK}"/>`;
  b += T(xL - 4, y1 - 8, trai, { a: 'middle', w: 700, size: 24 }) + T(xR + 4, y1 - 8, phai, { a: 'middle', w: 700, size: 24 });
  if (nhanT) b += T(xL + 6, y1 - 10, nhanT, { w: 700 });
  if (nhanP) b += T(xR - 6, y1 - 10, nhanP, { w: 700, a: 'end' });
  const sangPhai = trai === '+';
  [52, 132].forEach((y) => { b += sangPhai ? arr(xL + 6, y, xR - 8, y, id + 'a', GREY, '', 2) : arr(xR - 6, y, xL + 8, y, id + 'a', GREY, '', 2); });
  const mxp = xL + (xR - xL) * mx;
  b += dot(mxp, 92, 6, RED) + T(mxp + 8, 86, 'M', { w: 700, c: RED });
  if (mLab) {
    const xa = mBen === 'trai' ? xL : xR;
    b += ln(mxp, 98, mxp, 182, GREY, 2, '4 4');
    b += doDai(Math.min(xa, mxp) + 2, 176, Math.max(xa, mxp) - 2, 176, id + 'c') + T((xa + mxp) / 2, 168, mLab, { c: BLUE, w: 700, a: 'middle' });
  }
  if (tong) b += doDai(xL + 2, 200, xR - 2, 200, id + 'c', INK) + T((xL + xR) / 2, 194, tong, { w: 700, a: 'middle' });
  if (e) b += `<circle cx="${xL + 18}" cy="120" r="9" fill="#fff" stroke="${INK}" stroke-width="2.4"/>` + T(xL + 18, 127, 'e', { a: 'middle', w: 700, size: 18 });
  return wrap(`0 0 320 ${tong ? 210 : mLab ? 188 : 160}`, b, cap, 'Hai bản kim loại phẳng song song');
};

// Tam giác vuông MNP, MP dọc đường sức
const tamGiac = (cap, { mn = '5,0 cm', np = '4,0 cm', mp = '?', id = 'tg' } = {}) => {
  let b = defs(id + 'a');
  const M = [40, 170], P = [145, 170], N = [145, 30];
  b += `<path d="M${M} L${P} L${N} z" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
  b += `<path d="M${P[0] - 14},${P[1]} L${P[0] - 14},${P[1] - 14} L${P[0]},${P[1] - 14}" fill="none" stroke="${INK}" stroke-width="2"/>`;
  b += dot(...M) + dot(...N) + dot(...P);
  b += T(M[0] - 8, M[1] + 6, 'M', { w: 700, a: 'end' }) + T(P[0] + 8, P[1] + 8, 'P', { w: 700 }) + T(N[0] + 8, N[1] + 4, 'N', { w: 700 });
  b += T(80, 94, mn, { a: 'end' }) + T(153, 106, np) + T(92, 196, mp, { a: 'middle', c: BLUE, w: 700 });
  b += arr(210, 120, 304, 120, id + 'a', GREY, '', 2.4) + arr(210, 170, 304, 170, id + 'a', GREY, '', 2.4) + T(258, 106, 'E', { a: 'middle', w: 700, c: GREY });
  return wrap('0 0 320 205', b, cap, 'Tam giác vuông MNP trong điện trường đều');
};

export const hinhL11b20 = {
  // Trang 1 · Dự đoán: chim đậu trên dây 500 kV
  chimDay: (cap = 'Chim đậu trên dây 500 kV; cột sắt nối đất.') => {
    let b = '';
    b += ln(0, 70, 224, 70, INK, 5) + T(8, 104, 'dây 500 kV', { w: 700 });
    [230, 242, 254].forEach((x) => { b += `<ellipse cx="${x}" cy="70" rx="5" ry="12" fill="#fff" stroke="${INK}" stroke-width="2.2"/>`; });
    b += ln(224, 70, 262, 70, INK, 2) + `<rect x="262" y="40" width="14" height="140" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += dat(220, 316, 180) + T(254, 160, 'cột', { a: 'end' });
    // chim
    b += `<ellipse cx="112" cy="42" rx="28" ry="14" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<circle cx="140" cy="30" r="10" fill="#fff" stroke="${INK}" stroke-width="${SW}"/><path d="M149,28 L160,32 L149,34 z" fill="${INK}"/>`;
    b += `<path d="M85,40 L64,30 L68,46 z" fill="#fff" stroke="${INK}" stroke-width="2.4"/>`;
    b += ln(104, 55, 100, 70, INK, 2.4) + ln(122, 55, 126, 70, INK, 2.4);
    b += T(96, 138, 'A', { w: 700, c: RED, a: 'middle' }) + T(130, 138, 'B', { w: 700, c: RED, a: 'middle' });
    b += ln(100, 72, 96, 120, RED, 1.6, '3 3') + ln(126, 72, 130, 120, RED, 1.6, '3 3');
    return wrap('0 0 320 192', b, cap, 'Chim đậu trên dây điện cao thế');
  },
  // Trang 1 · II.1 công không phụ thuộc đường đi
  duongDi: (cap = 'Đi thẳng (liền) hay đi cong (đứt) từ M đến N: công có khác nhau không?') => duongDi(cap),
  // Trang 2 · II.2 điện thế như độ cao của bậc thang
  bacThang: (cap = 'Đặt quả bóng hay cái tủ lên bậc trên cùng: độ cao h của bậc có đổi không?') => {
    let b = defs2('bt');
    b += `<path d="M10,170 L10,130 L90,130 L90,90 L170,90 L170,50 L250,50 L250,170 z" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<circle cx="188" cy="38" r="12" fill="#fff" stroke="${RED}" stroke-width="${SW}"/>`;
    b += `<rect x="208" y="6" width="32" height="44" rx="2" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + ln(224, 10, 224, 46, INK, 2);
    b += doDai(282, 52, 282, 168, 'bt') + T(290, 116, 'h', { w: 700, c: BLUE });
    b += dat(4, 316, 170) + T(10, 198, 'mốc: mặt đất (h = 0)');
    return wrap('0 0 320 206', b, cap, 'Bậc thang: độ cao là của bậc');
  },
  // Trang 2 · II.3 đường đẳng thế vuông góc đường sức
  dangThe: (cap = 'Nét đứt: đường đẳng thế. V<sub>1</sub>, V<sub>2</sub>, V<sub>3</sub>: số nào lớn nhất?') => {
    let b = defs('dt');
    [36, 100, 164].forEach((y) => { b += arr(8, y, 304, y, 'dt', INK, '', 2.4); });
    [[70, '1'], [160, '2'], [250, '3']].forEach(([x, i]) => { b += ln(x, 14, x, 180, BLUE, 2.6, '8 6') + T(x, 204, `V${sb(i)}`, { a: 'middle', c: BLUE, w: 700 }); });
    b += dot(70, 100, 6, RED) + T(62, 90, 'M', { a: 'end', w: 700, c: RED }) + dot(250, 100, 6, RED) + T(258, 90, 'N', { w: 700, c: RED });
    b += T(312, 28, 'E', { a: 'end', w: 700 });
    return wrap('0 0 320 212', b, cap, 'Đường sức và đường đẳng thế');
  },
  // Trang 3 · thí nghiệm: vôn kế số và pin
  vonKe: (cap = 'Lần 1: que đỏ chạm cực (+), que đen chạm cực (−).') => {
    let b = '';
    b += `<rect x="20" y="120" width="150" height="46" rx="6" fill="#fff" stroke="${INK}" stroke-width="${SW}"/><rect x="170" y="132" width="10" height="22" fill="${INK}"/>`;
    b += T(95, 151, 'pin 1,5 V', { a: 'middle', w: 700 }) + T(196, 152, '+', { w: 700, size: 24 }) + T(8, 152, '−', { w: 700, size: 24 });
    b += `<rect x="190" y="10" width="120" height="84" rx="8" fill="#fff" stroke="${INK}" stroke-width="${SW}"/><rect x="204" y="22" width="92" height="34" rx="3" fill="#fff" stroke="${INK}" stroke-width="2"/>`;
    b += T(250, 47, '? V', { a: 'middle', w: 700 }) + T(250, 82, 'vôn kế', { a: 'middle' });
    b += `<path d="M280,94 C 280,120 230,120 182,138" fill="none" stroke="${RED}" stroke-width="${SW}"/>` + T(300, 124, 'đỏ', { c: RED, w: 700, a: 'end' });
    b += `<path d="M220,94 C 200,112 60,96 18,138" fill="none" stroke="${INK}" stroke-width="${SW}" stroke-dasharray="7 5"/>` + T(70, 100, 'đen', { w: 700 });
    return wrap('0 0 320 176', b, cap, 'Đo hiệu điện thế giữa hai cực pin');
  },
  // Trang 3 · thí nghiệm đo: V theo x giữa hai lá đồng
  doThiVx: (cap = 'Bốn số đo trong khay nước muối, que đen ở lá âm (0 V).') => {
    let b = defs('vx');
    const X = (x) => 50 + x * 25, Y = (v) => 172 - v * 24;
    b += arr(50, 172, 306, 172, 'vx') + arr(50, 172, 50, 14, 'vx');
    [0, 2, 4, 6, 8, 10].forEach((x) => { b += ln(X(x), 172, X(x), 178, INK, 2) + T(X(x), 198, String(x), { a: 'middle' }); });
    [2, 4, 6].forEach((v) => { b += ln(44, Y(v), 50, Y(v), INK, 2) + T(38, Y(v) + 7, String(v), { a: 'end' }); });
    b += T(58, 24, 'V (V)', { w: 700 }) + T(312, 160, 'x (cm)', { a: 'end', w: 700 });
    b += ln(X(0), Y(0), X(10), Y(6), GREY, 2, '6 5');
    [[2, 1.18], [4, 2.43], [6, 3.57], [8, 4.84]].forEach(([x, v]) => { b += `<circle cx="${f1(X(x))}" cy="${f1(Y(v))}" r="6" fill="${RED}"/>`; });
    return wrap('0 0 320 206', b, cap, 'Đồ thị điện thế theo khoảng cách');
  },
  // Trang 4 · bẫy 2: hình chiếu của MN lên đường sức
  hinhChieu: (cap = 'MN xiên góc α với đường sức. Đoạn nào dùng làm d trong U = Ed?') => {
    let b = defs('hc') + defs2('hc2');
    [16, 174].forEach((y) => { b += arr(8, y, 304, y, 'hc', GREY, '', 2); });
    b += T(310, 32, 'E', { a: 'end', w: 700, c: GREY });
    const M = [50, 140], N = [220, 46];
    b += ln(...M, ...N, INK, SW) + dot(...M) + dot(...N) + T(M[0] - 8, M[1] + 6, 'M', { w: 700, a: 'end' }) + T(N[0] + 8, N[1], 'N', { w: 700 });
    b += ln(M[0], M[1], 290, M[1], GREY, 2, '5 4') + cung(M[0], M[1], 44, 0, 29) + T(M[0] + 52, M[1] - 8, gk('α'), { size: 22 });
    b += ln(N[0], N[1], N[0], M[1], BLUE, 2, '4 4') + doDai(M[0] + 2, 158, N[0] - 2, 158, 'hc2') + T(135, 152, '?', { c: BLUE, w: 700, a: 'middle' });
    return wrap('0 0 320 184', b, cap.replace('α', '<i style="font-family:KaTeX_Math">α</i>'), 'Hình chiếu của MN lên đường sức');
  },
  // Trang 5 · bài toán mẫu: hai bản cách 2 cm, mốc ở bản âm
  banMau: (cap = 'Mốc 0 V ở bản âm. M cách bản âm 0,5 cm; electron rời bản âm.') => haiBan(cap, { trai: '−', phai: '+', mx: 0.25, mLab: '0,5 cm', mBen: 'trai', tong: '2 cm', e: true, id: 'bm' }),
  // Trang 5 · thử thách ⋆⋆⋆: hạt bụi lơ lửng giữa hai bản nằm ngang
  hatBui: (cap = 'Hạt bụi âm đứng yên. Lực điện phải hướng lên hay xuống?') => {
    let b = defs('hb1');
    b += `<rect x="30" y="20" width="260" height="8" fill="${INK}"/><rect x="30" y="150" width="260" height="8" fill="${INK}"/>`;
    b += T(296, 30, '?', { w: 700, size: 24 }) + T(296, 160, '?', { w: 700, size: 24 });
    b += `<circle cx="160" cy="88" r="10" fill="#fff" stroke="${INK}" stroke-width="2.4"/>` + T(160, 95, '−', { a: 'middle', w: 700 });
    b += arr(160, 100, 160, 140, 'hb1', RED) + T(172, 136, 'P', { c: RED, w: 700 });
    b += arr(160, 76, 160, 40, 'hb1', INK, '6 4') + T(172, 54, 'F = ?', { w: 700 });
    return wrap('0 0 320 166', b, cap, 'Hạt bụi lơ lửng giữa hai bản');
  },

  // ===== Bài tập mẫu =====
  duongD1: (cap = 'Đi cong hay đi thẳng: d vẫn là 4,0 cm.') => duongDi(cap, { d: '4,0 cm', id: 'd1' }),
  tamD4: (cap = 'MP dọc đường sức, NP vuông góc đường sức. Đoạn nào là d?') => tamGiac(cap, { id: 'td4' }),
  banD5: (cap = 'Mốc ở bản A. M cách bản B 1,5 cm.') => haiBan(cap, { trai: '+', phai: '−', nhanT: 'A', nhanP: 'B', mx: 0.7, mLab: '1,5 cm', mBen: 'phai', tong: '5,0 cm', id: 'b5' }),
  // ===== Bài tương tự =====
  duongTT: (cap = 'N lệch ngược chiều đường sức 2,0 cm so với M.') => {
    let b = defs('dta') + defs('dtb') + defs2('dtc');
    [14, 100].forEach((y) => { b += arr(8, y, 300, y, 'dta', GREY, '', 2); });
    b += T(306, 38, 'E', { w: 700, c: GREY, a: 'end' });
    const M = [230, 84], N = [90, 34], P = [90, 84];
    b += arr(M[0], M[1], N[0] + 6, N[1] + 2, 'dtb', INK);
    b += ln(N[0], N[1] + 4, P[0], P[1] - 6, INK, SW, '7 5') + dot(...P, 5, BLUE) + T(P[0] - 10, P[1] + 4, 'P', { w: 700, a: 'end', c: BLUE });
    b += dot(...M) + dot(...N) + T(M[0] + 10, M[1] + 4, 'M', { w: 700 }) + T(N[0] - 8, N[1] - 2, 'N', { w: 700, a: 'end' });
    b += ln(M[0], M[1], M[0], 140, GREY, 2, '4 4') + ln(N[0], P[1], N[0], 140, GREY, 2, '4 4');
    b += doDai(N[0] + 2, 134, M[0] - 2, 134, 'dtc') + T((M[0] + N[0]) / 2, 126, '2,0 cm', { c: BLUE, w: 700, a: 'middle' });
    return wrap('0 0 320 144', b, cap, 'Điện tích đi ngược chiều đường sức');
  },
  tamTT: (cap = 'MP = 6,0 cm dọc đường sức, NP = 8,0 cm.') => tamGiac(cap, { mn: '', np: '8,0 cm', mp: '6,0 cm', id: 'ttt' }),
  banTT: (cap = 'Bản A (+), bản B (−); M cách bản A 2,0 cm.') => haiBan(cap, { trai: '+', phai: '−', nhanT: 'A', nhanP: 'B', mx: 1 / 3, mLab: '2,0 cm', mBen: 'trai', tong: '6,0 cm', id: 'btt' }),
};
