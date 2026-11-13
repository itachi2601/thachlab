// Hình minh hoạ cho ruột tập VL11 · Bài 12 Giao thoa sóng (lesson 31). Cùng quy tắc với hinh-l11-bai2.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, phân biệt bằng nét (liền – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chữ Hi Lạp (λ) lấy từ font KaTeX (Source Sans 3 chỉ nạp latin/vietnamese → tránh rơi về Helvetica), cả trong SVG lẫn chú thích.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh. Xem thử: node scripts/ruot-tap/l11-bai12.mjs --hinh (chụp vào out/hinh-l11-bai12/).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const L = gk('λ');
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const hl = '<span style="font-family:KaTeX_Math;font-style:italic">λ</span>'; // λ trong chú thích HTML
const f1 = (v) => (+v).toFixed(1);
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${f1(x1)}" y1="${f1(y1)}" x2="${f1(x2)}" y2="${f1(y2)}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const arr2 = (x1, y1, x2, y2, id, c = INK, w = 2) =>
  `<line x1="${f1(x1)}" y1="${f1(y1)}" x2="${f1(x2)}" y2="${f1(y2)}" stroke="${c}" stroke-width="${w}" marker-start="url(#${id})" marker-end="url(#${id})"/>`;
const arr = (x1, y1, x2, y2, id, c = INK, w = 2.4) =>
  `<line x1="${f1(x1)}" y1="${f1(y1)}" x2="${f1(x2)}" y2="${f1(y2)}" stroke="${c}" stroke-width="${w}" marker-end="url(#${id})"/>`;
const mk2 = (id) => `<defs><marker id="${id}" markerWidth="7" markerHeight="7" refX="3.5" refY="3.5" orient="auto-start-reverse" markerUnits="strokeWidth"><path d="M0,0 L7,3.5 L0,7 z" fill="context-stroke"/></marker></defs>`;
const cham = (x, y, c = INK, r = 5.5) => `<circle cx="${f1(x)}" cy="${f1(y)}" r="${r}" fill="${c}"/>`;
const rong = (x, y, c = BLUE, r = 5.5) => `<circle cx="${f1(x)}" cy="${f1(y)}" r="${r}" fill="#fff" stroke="${c}" stroke-width="2.4"/>`;
const so = (v) => String(v).replace('.', ',');

// Họ hyperbol |d2 − d1| = s quanh hai nguồn A(cx − c, cy), B(cx + c, cy); s > 0: nhánh gần A (d1 nhỏ hơn), s < 0: nhánh gần B, s = 0: trung trực.
// yr: [ymin, ymax] (đơn vị SVG tính từ cy, âm là phía trên)
const hyp = (cx, cy, c, s, yr, st) => {
  if (Math.abs(s) < 1e-9) return `<line x1="${cx}" y1="${f1(cy + yr[0])}" x2="${cx}" y2="${f1(cy + yr[1])}" ${st}/>`;
  const a = Math.abs(s) / 2, b = Math.sqrt(c * c - a * a), sg = s > 0 ? -1 : 1;
  let d = '';
  for (let k = 0; k <= 80; k++) { const y = yr[0] + ((yr[1] - yr[0]) * k) / 80; d += `${k ? 'L' : 'M'}${f1(cx + sg * a * Math.sqrt(1 + (y * y) / (b * b)))},${f1(cy + y)}`; }
  return `<path d="${d}" fill="none" ${st}/>`;
};

// Dải màn có n vân sáng liên tiếp (ô trắng trên nền xám), ngoặc trên ghi tổng chiều dài
const dai = (n, nhan, id) => {
  const x0 = 34, x1 = 286, y = 62, h = 34, step = (x1 - x0) / (n - 1), wv = Math.min(18, step * 0.42);
  let b = mk2(id) + `<rect x="10" y="${y}" width="300" height="${h}" fill="#c9cfdc" stroke="${INK}" stroke-width="1.6"/>`;
  for (let k = 0; k < n; k++) b += `<rect x="${f1(x0 + k * step - wv / 2)}" y="${y}" width="${f1(wv)}" height="${h}" fill="#fff" stroke="${INK}" stroke-width="1.2"/>`;
  b += ln(x0, y - 4, x0, y - 22, INK, 1.6) + ln(x1, y - 4, x1, y - 22, INK, 1.6) + arr2(x0 + 3, y - 15, x1 - 3, y - 15, id, INK, 2);
  b += T(160, y - 26, nhan, { a: 'middle', w: 700 });
  for (let k = 0; k < n; k++) b += T(f1(x0 + k * step), y + h + 22, String(k + 1), { a: 'middle', size: 20, c: GREY });
  return b;
};

export const hinhL11b12 = {
  // Trang 1 · Dự đoán: hai loa và hàng ghế đầu (không đánh dấu chỗ to/nhỏ)
  haiLoa: (cap = 'Hai loa cùng phát một bản nhạc; em đi dọc hàng ghế đầu.') => {
    let b = defs('hl1');
    b += `<rect x="20" y="16" width="280" height="34" fill="#eef2fa" stroke="${GREY}" stroke-width="1.6"/>` + T(160, 40, 'sân khấu', { a: 'middle', c: GREY });
    const loa = (x, s) => `<rect x="${x - 15}" y="56" width="30" height="34" rx="3" fill="#fff" stroke="${INK}" stroke-width="2.6"/><circle cx="${x}" cy="73" r="9" fill="none" stroke="${INK}" stroke-width="2.2"/>` + T(x, 114, s, { a: 'middle', w: 700 });
    b += loa(42, 'Loa 1') + loa(278, 'Loa 2');
    for (let k = 0; k < 4; k++) { const r = 14 + k * 14; b += `<path d="M${42 + r * 0.7},${73 - r * 0.7} A${r},${r} 0 0 1 ${42 + r * 0.7},${73 + r * 0.7}" fill="none" stroke="${GREY}" stroke-width="1.6"/><path d="M${278 - r * 0.7},${73 - r * 0.7} A${r},${r} 0 0 0 ${278 - r * 0.7},${73 + r * 0.7}" fill="none" stroke="${GREY}" stroke-width="1.6"/>`; }
    for (let k = 0; k < 11; k++) b += `<rect x="${32 + k * 24}" y="150" width="18" height="16" rx="2" fill="#fff" stroke="${INK}" stroke-width="1.6"/>`;
    b += T(160, 194, 'hàng ghế đầu', { a: 'middle', c: GREY });
    b += `<circle cx="70" cy="134" r="7" fill="${RED}"/>` + arr(82, 134, 250, 134, 'hl1', RED, 2.6) + T(160, 128, 'em đi', { a: 'middle', c: RED });
    return wrap('0 0 320 202', b, cap, 'Hai loa và hàng ghế đầu');
  },

  // Trang 1 · Thí nghiệm khay sóng: gợn tròn từ hai mũi nhọn
  khay: (cap = 'Gợn tròn từ hai mũi nhọn A, B: nét liền là đỉnh sóng, nét đứt là hõm.') => {
    const A = [118, 100], B = [202, 100];
    let b = `<defs><clipPath id="kclip"><rect x="4" y="4" width="312" height="192"/></clipPath></defs><rect x="4" y="4" width="312" height="192" fill="#f4f6fb" stroke="${GREY}" stroke-width="1.4"/><g clip-path="url(#kclip)">`;
    for (const [x, y] of [A, B]) for (let k = 1; k <= 7; k++) {
      b += `<circle cx="${x}" cy="${y}" r="${k * 24}" fill="none" stroke="${INK}" stroke-width="1.5"/>`;
      b += `<circle cx="${x}" cy="${y}" r="${k * 24 - 12}" fill="none" stroke="${BLUE}" stroke-width="1.3" stroke-dasharray="4 4"/>`;
    }
    b += '</g>' + cham(A[0], A[1], RED, 6) + cham(B[0], B[1], RED, 6);
    b += `<rect x="${A[0] - 30}" y="${A[1] + 8}" width="22" height="24" fill="#fff"/>` + T(A[0] - 19, A[1] + 27, 'A', { a: 'middle', w: 700 });
    b += `<rect x="${B[0] + 8}" y="${B[1] + 8}" width="22" height="24" fill="#fff"/>` + T(B[0] + 19, B[1] + 27, 'B', { a: 'middle', w: 700 });
    return wrap('0 0 320 200', b, cap, 'Khay sóng hai mũi nhọn');
  },

  // Trang 2 · Điểm M và hai khoảng cách d1, d2
  diemM: (cap = 'M cách hai nguồn A, B lần lượt d₁, d₂.') => {
    const A = [50, 170], B = [270, 170], M = [118, 40];
    let b = ln(A[0], A[1], B[0], B[1], GREY, 2, '6 5');
    b += ln(A[0], A[1], M[0], M[1], INK, 2.6) + ln(B[0], B[1], M[0], M[1], INK, 2.6);
    b += cham(A[0], A[1], RED) + cham(B[0], B[1], RED) + cham(M[0], M[1]);
    b += T(A[0], A[1] + 30, 'A', { a: 'middle', w: 700, size: 27 }) + T(B[0], B[1] + 30, 'B', { a: 'middle', w: 700, size: 27 }) + T(M[0], M[1] - 12, 'M', { a: 'middle', w: 700, size: 27 });
    b += T(70, 100, `<tspan font-size="28">d</tspan><tspan font-size="20" dy="6">1</tspan>`, { a: 'end' }) + T(200, 98, `<tspan font-size="28">d</tspan><tspan font-size="20" dy="6">2</tspan>`);
    return wrap('24 6 272 204', b, cap.replace('d₁', '<i>d</i><sub>1</sub>').replace('d₂', '<i>d</i><sub>2</sub>'), 'Điểm M và hai nguồn');
  },

  // Trang 2 · Cộng hai sóng: HS tự vẽ sóng tổng (không vẽ sẵn để khỏi lộ dòng Biên độ trong bảng)
  congSong: (cap = 'Vẽ sóng tổng vào dải dưới cùng của mỗi cột (lưới chấm cách nhau đúng biên độ một sóng).') => {
    const A = 14;
    const song = (x0, y0, w, ph, dash = '', c = INK) => {
      let d = '';
      for (let k = 0; k <= 60; k++) { const x = x0 + (w * k) / 60; d += `${k ? 'L' : 'M'}${f1(x)},${f1(y0 - A * Math.sin((2 * Math.PI * k) / 30 + ph))}`; }
      return `<path d="${d}" fill="none" stroke="${c}" stroke-width="2.4"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
    };
    const cot = (x0, ph, nhan) => {
      let b = T(x0 + 68, 22, nhan, { a: 'middle', w: 700, size: 20 });
      b += ln(x0, 52, x0 + 136, 52, GREY, 1.2) + song(x0, 52, 136, 0) + T(x0 - 4, 58, '1', { a: 'end', size: 20 });
      b += ln(x0, 102, x0 + 136, 102, GREY, 1.2) + song(x0, 102, 136, ph, '6 4', BLUE) + T(x0 - 4, 108, '2', { a: 'end', size: 20 });
      b += ln(x0, 164, x0 + 136, 164, INK, 1.6);
      for (const dy of [-28, -14, 14, 28]) b += ln(x0, 164 + dy, x0 + 136, 164 + dy, '#c4cbdc', 1.2, '2 4');
      return b + T(x0 + 68, 212, 'tổng', { a: 'middle', size: 20, c: GREY });
    };
    return wrap('0 0 320 218', cot(20, 0, '(a) cùng pha') + cot(176, Math.PI, '(b) ngược pha'), cap, 'Hai sóng cùng pha, ngược pha');
  },

  // Trang 2 · Vân giao thoa quanh AB = 4λ: đếm đường cực đại, cực tiểu
  vanAB: (cap = `AB = 4${hl}. Nét liền: cực đại; nét đứt: cực tiểu.`) => {
    const cx = 160, cy = 112, lam = 30, c = 2 * lam;
    let b = `<defs><clipPath id="vclip"><rect x="2" y="4" width="316" height="216"/></clipPath></defs><g clip-path="url(#vclip)">`;
    for (let k = -3; k <= 3; k++) b += hyp(cx, cy, c, k * lam, [-106, 106], `stroke="${RED}" stroke-width="2.4"`);
    for (let k = -4; k <= 3; k++) b += hyp(cx, cy, c, (k + 0.5) * lam, [-106, 106], `stroke="${BLUE}" stroke-width="1.8" stroke-dasharray="5 4"`);
    b += '</g>' + ln(cx - c, cy, cx + c, cy, INK, 2.2) + cham(cx - c, cy, INK, 6) + cham(cx + c, cy, INK, 6);
    b += `<rect x="${cx - c - 30}" y="${cy + 6}" width="22" height="22" fill="#fff"/>` + T(cx - c - 19, cy + 24, 'A', { a: 'middle', w: 700 });
    b += `<rect x="${cx + c + 8}" y="${cy + 6}" width="22" height="22" fill="#fff"/>` + T(cx + c + 19, cy + 24, 'B', { a: 'middle', w: 700 });
    return wrap('0 0 320 224', b, cap, 'Đường cực đại, cực tiểu quanh hai nguồn');
  },

  // Trang 3 · Trên đoạn AB: cực đại, cực tiểu xen kẽ; hai khoảng để HS điền
  doanAB: (cap = 'Chấm đặc: cực đại; chấm rỗng: cực tiểu. Điền hai khoảng có dấu “?” theo λ.') => {
    const x0 = 20, x1 = 300, cx = 160, h = 32, y = 66;
    let b = mk2('da') + ln(x0, y, x1, y, INK, 2.4);
    b += cham(x0, y, INK, 6.5) + cham(x1, y, INK, 6.5) + T(x0, y + 30, 'A', { a: 'middle', w: 700 }) + T(x1, y + 30, 'B', { a: 'middle', w: 700 });
    for (let n = -4; n <= 4; n++) b += cham(cx + n * h, y, RED, 5);
    for (let n = -4; n <= 3; n++) b += rong(cx + (n + 0.5) * h, y);
    b += ln(cx, y + 8, cx, y + 16, INK, 1.6) + T(cx, y + 34, 'O', { a: 'middle', w: 700 });
    b += arr2(cx + h + 2, y - 16, cx + 2 * h - 2, y - 16, 'da') + T(cx + 1.5 * h, y - 24, '?', { a: 'middle', w: 700, c: RED });
    b += arr2(cx - 2 * h + 2, y - 16, cx - 1.5 * h - 2, y - 16, 'da') + T(cx - 1.75 * h, y - 24, '?', { a: 'middle', w: 700, c: BLUE });
    return wrap('0 0 320 106', b, cap.replace('λ', hl), 'Cực đại, cực tiểu trên đoạn AB');
  },

  // Trang 3 · Khe Young: a, D, i
  young: (cap = 'Hai khe S₁, S₂ cách nhau a; màn cách hai khe D; ô trắng trên màn là vân sáng.') => {
    const yc = 102, s1 = yc - 26, s2 = yc + 26, xs = 96, xm = 262;
    let b = mk2('yg') + defs('yg2');
    b += `<circle cx="22" cy="${yc}" r="9" fill="#fff" stroke="${INK}" stroke-width="2.4"/>` + T(10, 34, 'nguồn', { size: 20 }) + T(10, 54, 'sáng', { size: 20 });
    b += arr(34, yc, 84, yc, 'yg2', INK, 2);
    b += ln(xs, 14, xs, s1 - 5, INK, 4) + ln(xs, s1 + 5, xs, s2 - 5, INK, 4) + ln(xs, s2 + 5, xs, 172, INK, 4);
    b += T(xs - 8, s1 + 4, `S${sb('1')}`, { a: 'end', size: 20 }) + T(xs - 8, s2 + 18, `S${sb('2')}`, { a: 'end', size: 20 });
    for (const yy of [s1, s2]) for (const yt of [yc - 60, yc, yc + 60]) b += ln(xs, yy, xm, yt, GREY, 1.1, '3 4');
    b += arr2(xs + 12, s1, xs + 12, s2, 'yg', INK, 1.8) + T(xs + 18, yc + 6, gk('a'), { size: 22 });
    b += `<rect x="${xm}" y="14" width="20" height="158" fill="#c9cfdc" stroke="${INK}" stroke-width="1.6"/>`;
    const i = 30;
    for (let k = -2; k <= 2; k++) b += `<rect x="${xm}" y="${f1(yc + k * i - 6)}" width="20" height="12" fill="#fff" stroke="${INK}" stroke-width="1.2"/>`;
    b += T(xm - 6, yc + 6, 'O', { a: 'end', w: 700, size: 20 });
    b += ln(xm + 22, yc - i, xm + 34, yc - i, INK, 1.4) + ln(xm + 22, yc - 2 * i, xm + 34, yc - 2 * i, INK, 1.4) + arr2(xm + 30, yc - 2 * i + 2, xm + 30, yc - i - 2, 'yg', INK, 1.6) + T(xm + 36, yc - 1.5 * i + 7, gk('i'), { size: 22 });
    b += ln(xs, 184, xs, 196, INK, 1.4) + ln(xm, 184, xm, 196, INK, 1.4) + arr2(xs + 3, 190, xm - 3, 190, 'yg', INK, 1.8);
    b += `<rect x="${(xs + xm) / 2 - 14}" y="176" width="28" height="24" fill="#fff"/>` + T((xs + xm) / 2, 197, gk('D'), { a: 'middle', size: 22 });
    return wrap('0 0 320 204', b, cap.replace('S₁', 'S<sub>1</sub>').replace('S₂', 'S<sub>2</sub>').replace(' a;', ' <i>a</i>;').replace(' D;', ' <i>D</i>;'), 'Thí nghiệm khe Young');
  },

  // Trang 5 · Bài toán mẫu: thước AB = 10 cm, HS đánh dấu cực đại
  thuocAB: (cap = 'AB = 10 cm, O là trung điểm. Đánh dấu các cực đại từ O ra hai phía, mỗi bước λ/2; đếm, rồi đối chiếu câu b.') => {
    const x0 = 22, x1 = 298, y = 50, s = (x1 - x0) / 10;
    let b = ln(x0, y, x1, y, INK, 2.4);
    for (let k = 0; k <= 40; k++) { const x = x0 + (s * k) / 4; b += ln(x, y, x, y + (k % 4 === 0 ? 14 : 7), INK, k % 4 === 0 ? 2 : 1.2); }
    for (let k = 0; k <= 10; k++) b += T(f1(x0 + s * k), y + 36, String(k), { a: 'middle', size: 20 });
    b += cham(x0, y, INK, 6) + cham(x1, y, INK, 6) + T(x0, y - 12, 'A', { a: 'middle', w: 700 }) + T(x1, y - 12, 'B', { a: 'middle', w: 700 });
    b += cham(x0 + 5 * s, y, RED, 5) + T(x0 + 5 * s, y - 12, 'O', { a: 'middle', w: 700, c: RED }) + T(x1, y + 58, 'cm', { a: 'end', size: 20, c: GREY });
    return wrap('0 0 320 116', b, cap.replace('λ', hl), 'Thước AB 10 cm');
  },

  // Dạng 3 · Trung trực, 3 dãy cực đại khác và dãy qua M (hình đúng tỉ lệ: AB = 24 cm, MA = 14 cm, MB = 26 cm)
  dayM: (cap = 'Giữa M và trung trực có 3 dãy cực đại khác (nét mảnh).') => {
    const sc = 8, cx = 172, cy = 186, c = 12 * sc, lam = 3 * sc;
    let b = `<defs><clipPath id="dmclip"><rect x="2" y="2" width="316" height="${cy}"/></clipPath></defs><g clip-path="url(#dmclip)">`;
    b += hyp(cx, cy, c, 0, [-184, 0], `stroke="${GREY}" stroke-width="2" stroke-dasharray="7 5"`);
    for (let k = 1; k <= 3; k++) b += hyp(cx, cy, c, k * lam, [-184, 0], `stroke="${RED}" stroke-width="1.5"`);
    b += hyp(cx, cy, c, 4 * lam, [-184, 0], `stroke="${RED}" stroke-width="3"`) + '</g>';
    const Mx = cx - 10 * sc, My = cy - Math.sqrt(192) * sc;
    b += ln(cx - c, cy, cx + c, cy, INK, 2.2) + cham(cx - c, cy, INK, 6) + cham(cx + c, cy, INK, 6) + cham(Mx, My, INK, 6);
    b += T(cx - c, cy + 26, 'A', { a: 'middle', w: 700 }) + T(cx + c, cy + 26, 'B', { a: 'middle', w: 700 });
    b += `<rect x="${Mx - 34}" y="${My - 26}" width="26" height="24" fill="#fff"/>` + T(Mx - 21, My - 8, 'M', { a: 'middle', w: 700 });
    b += `<rect x="${cx + 6}" y="50" width="100" height="24" fill="#fff"/>` + T(cx + 8, 68, 'trung trực', { size: 20, c: GREY });
    return wrap('0 44 320 172', b, cap, 'Dãy cực đại qua M');
  },

  // Dạng 4 (BTM): 7 vân sáng liên tiếp trải trên 6,0 mm
  vanD4: (cap = 'Đoạn màn có 7 vân sáng liên tiếp (ô trắng), đo từ tâm vân đầu tới tâm vân cuối.') =>
    wrap('0 0 320 126', dai(7, '6,0 mm', 'v4'), cap, 'Bảy vân sáng liên tiếp'),
  // Bài tương tự Dạng 4 · Bài 2: 5 vân sáng liên tiếp trải trên 8,0 mm
  vanTT: (cap = 'Năm vân sáng liên tiếp, tâm tới tâm.') =>
    wrap('0 0 320 126', dai(5, '8,0 mm', 'vt'), cap, 'Năm vân sáng liên tiếp'),

  // Dạng 5 (BTM): trục toạ độ 0–3,5 mm, hai hàng trống để HS chấm vân sáng của từng bức xạ
  thangD5: (cap = `Chấm vân sáng của ${hl}<sub>1</sub> và ${hl}<sub>2</sub> (dùng <i>i</i><sub>1</sub>, <i>i</i><sub>2</sub> vừa tính) rồi tìm chỗ trùng.`) => {
    const x0 = 40, sc = 76, y = 132;
    let b = ln(x0, y, x0 + 3.5 * sc, y, INK, 2.2);
    for (let k = 0; k <= 14; k++) { const x = x0 + (k * sc) / 4; b += ln(x, y, x, y + (k % 2 === 0 ? 12 : 6), INK, k % 2 === 0 ? 1.8 : 1.1); }
    for (let k = 0; k <= 7; k++) b += T(f1(x0 + (k * sc) / 2), y + 34, so(k / 2), { a: 'middle', size: 20 });
    b += T(x0 + 3.5 * sc, y + 56, 'x (mm)', { a: 'end', size: 20, c: GREY });
    for (const [yy, s] of [[38, '1'], [88, '2']]) {
      b += ln(x0, yy, x0 + 3.5 * sc, yy, GREY, 1.4, '3 4') + T(x0 - 8, yy + 7, `${L}${sb(s)}`, { a: 'end', size: 21 });
      for (let k = 0; k <= 14; k++) b += ln(x0 + (k * sc) / 4, yy - 4, x0 + (k * sc) / 4, yy + 4, '#c4cbdc', 1);
    }
    b += cham(x0, 38, RED, 5) + cham(x0, 88, RED, 5);
    return wrap('0 0 320 196', b, cap, 'Trục chấm vân hai bức xạ');
  },
};
