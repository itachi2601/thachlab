// Hình minh hoạ cho ruột tập VL11 · Bài 8 Mô tả sóng (lesson 27). Cùng quy tắc với hinh-l11-bai2.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chữ Hi Lạp (λ π φ Δ) lấy từ font KaTeX (Source Sans 3 chỉ nạp latin/vietnamese → tránh rơi về Helvetica). Không dùng √ trong SVG.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh. Đồ thị đề bài vẽ đúng số (lưới + nhãn) để HS đọc được.
// Xem thử: node scripts/ruot-tap/l11-bai8.mjs --hinh (chụp vào out/hinh-l11-bai8/).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const LAM = gk('λ');
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const arr = (x1, y1, x2, y2, id, c = INK, dash = '', w = SW) =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const f1 = (v) => (+v).toFixed(1);
const so = (v) => String(+(+v).toFixed(3)).replace('.', ',').replace('-', '−'); // số kiểu Việt
const cham = (x, y, c = INK, r = 5) => `<circle cx="${f1(x)}" cy="${f1(y)}" r="${r}" fill="${c}"/>`;
// mũi tên hai đầu (đo đoạn)
const doan = (x1, y1, x2, y2, id, c = INK) => arr(x1, y1, x2, y2, id, c, '', 2.2) + arr(x2, y2, x1, y1, id, c, '', 2.2);
const song = (x0, x1, yc, amp, lam, ph = 0, c = INK, w = SW, dash = '', env = null) => {
  let d = '';
  for (let k = 0; k <= 200; k++) {
    const x = x0 + ((x1 - x0) * k) / 200, a = env ? env(x) : amp;
    d += `${k ? 'L' : 'M'}${f1(x)},${f1(yc - a * Math.sin((2 * Math.PI * (x - x0)) / lam + ph))}`;
  }
  return `<path d="${d}" fill="none" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
};

// Đồ thị đọc được số: u = fn(s) với s là x (cm) hoặc t (s); lưới mỗi `buoc`, nhãn mỗi `nhan` bước; nhãn trục tung ở ±A.
// M: [s, 'M'] chấm một điểm trên đường (đồ thị u–x).
const doThi = ({ fn, smax, buoc, nhan = 1, A, truc = 'x (cm)', id, vb = [320, 168], tieuDe = '', M = null, y0 = 0, dy = 0 }) => {
  const [W, H] = vb, x0 = 46, x1 = W - 34, yc = y0 + dy + (H - y0 - dy) / 2 - 6, ay = (H - y0 - dy) / 2 - 32;
  const X = (s) => x0 + (s / smax) * (x1 - x0), Y = (u) => yc - (u / A) * ay;
  let b = defs(id);
  const n = Math.round(smax / buoc);
  for (let i = 1; i <= n; i++) {
    const x = X(i * buoc);
    b += ln(f1(x), f1(yc - ay - 5), f1(x), f1(yc + ay + 5), '#c4cbdc', 1.4);
    if (i % nhan === 0) b += T(f1(x), f1(yc + ay + 26), so(i * buoc), { a: 'middle' });
  }
  [A, -A].forEach((v) => { b += ln(x0, f1(Y(v)), x1, f1(Y(v)), '#c4cbdc', 1.4) + T(x0 - 6, f1(Y(v) + 7), so(v), { a: 'end' }); });
  b += T(x0 - 6, f1(yc + 7), '0', { a: 'end' });
  b += arr(x0, f1(yc + ay + 8), x0, f1(y0 + 8), id, INK, '', 2.2) + arr(x0, f1(yc), W - 4, f1(yc), id, INK, '', 2.2);
  b += T(x0 + 8, f1(y0 + 24), 'u (cm)', { size: 20 }) + T(W - 2, f1(yc - 10), truc, { a: 'end', size: 20 });
  if (tieuDe) b += T(W - 2, f1(y0 + 24), tieuDe, { a: 'end', w: 700, c: BLUE });
  let d = '';
  for (let k = 0; k <= 240; k++) { const s = (k / 240) * smax; d += `${k ? 'L' : 'M'}${f1(X(s))},${f1(Y(fn(s)))}`; }
  b += `<path d="${d}" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
  if (M) b += `<circle cx="${f1(X(M[0]))}" cy="${f1(Y(fn(M[0])))}" r="6" fill="#fff" stroke="${RED}" stroke-width="2.8"/>` + T(f1(X(M[0]) + 10), f1(Y(fn(M[0])) + 24), M[1], { c: RED, w: 700 });
  return b;
};
// hai đồ thị (a) u–x lúc t = 0 và (b) u–t của M, xếp chồng trong một hình
const haiDoThi = (a, b, cap, id) => {
  const top = doThi({ ...a, id: id + 'a', tieuDe: '(a) t = 0', vb: [320, 152], dy: 18 });
  const bot = doThi({ ...b, id: id + 'b', tieuDe: '(b) điểm M', vb: [320, 312], y0: 160, dy: 18 });
  return wrap('0 0 320 312', top + bot, cap, 'Đồ thị u–x lúc t = 0 và đồ thị u–t của M');
};

export const hinhL11b8 = {
  // Trang 1 · Dự đoán: làn sóng người trên khán đài (chụp một lúc)
  khanDai: (cap = 'Một lúc khi làn sóng chạy qua khán đài.') => {
    let b = defs('kd');
    b += ln(10, 168, 310, 168, INK, 3);
    for (let i = 0; i < 11; i++) {
      const x = 22 + i * 27.6, h = 46 * Math.exp(-((i - 6) ** 2) / 2.2); // người ở giữa đứng cao nhất
      const yh = 128 - h;
      b += ln(f1(x), f1(yh + 10), f1(x), 168, INK, 3.4) + `<circle cx="${f1(x)}" cy="${f1(yh)}" r="9" fill="#fff" stroke="${INK}" stroke-width="2.6"/>`;
      if (h > 20) b += ln(f1(x), f1(yh + 16), f1(x - 9), f1(yh - 12), INK, 2.6) + ln(f1(x), f1(yh + 16), f1(x + 9), f1(yh - 12), INK, 2.6);
    }
    b += arr(120, 26, 250, 26, 'kd', RED) + T(116, 33, 'làn sóng', { c: RED, a: 'end' });
    return wrap('0 0 320 180', b, cap, 'Làn sóng người trên khán đài');
  },
  // Trang 1 · thí nghiệm khay nước + miếng xốp C (nhìn ngang)
  khayNuoc: (cap = 'Gợn sóng lan từ O qua chỗ miếng xốp C. C đi đâu?') => {
    let b = defs('kn');
    b += `<path d="M10,70 L10,170 L310,170 L310,70" fill="none" stroke="${INK}" stroke-width="3"/>`;
    b += song(40, 306, 110, 12, 52, Math.PI / 2, BLUE, 2.8, '', (x) => 14 * Math.exp(-(x - 40) / 260));
    b += ln(40, 30, 40, 100, INK, 4) + arr(52, 46, 52, 22, 'kn', INK, '', 2.2) + arr(52, 46, 52, 70, 'kn', INK, '', 2.2);
    b += T(28, 44, 'O', { a: 'end', w: 700 });
    // miếng xốp C ở x ≈ 220 (trên mặt nước)
    const xc = 222, yc = 110 - 14 * Math.exp(-(xc - 40) / 260) * Math.sin((2 * Math.PI * (xc - 40)) / 52 + Math.PI / 2);
    b += `<rect x="${f1(xc - 13)}" y="${f1(yc - 12)}" width="26" height="12" rx="2" fill="#fff" stroke="${RED}" stroke-width="2.8"/>` + T(xc, f1(yc - 20), 'C', { c: RED, w: 700, a: 'middle' });
    b += arr(120, 150, 270, 150, 'kn', GREY, '6 4', 2.2) + T(195, 194, 'gợn lan ra', { a: 'middle', c: GREY });
    return wrap('0 0 320 202', b, cap, 'Khay nước, nguồn O và miếng xốp C');
  },
  // Trang 2 · dây lúc chụp: đoạn (1) giữa hai đỉnh liên tiếp, đoạn (2) từ VTCB tới đỉnh
  dayChup: (cap = 'Dây lúc chụp: đoạn (1), (2) là gì?') => {
    let b = defs('dc');
    const yc = 112, x0 = 20, lam = 120;
    b += ln(x0, yc, 306, yc, GREY, 2, '6 4') + song(x0, 300, yc, 44, lam);
    // đỉnh ở x0 + lam/4 và x0 + 5lam/4
    const p1 = x0 + lam / 4, p2 = x0 + (5 * lam) / 4;
    b += ln(p1, 68, p1, 30, GREY, 1.8, '4 3') + ln(p2, 68, p2, 30, GREY, 1.8, '4 3');
    b += doan(p1, 36, p2, 36, 'dc', RED) + T((p1 + p2) / 2, 26, '(1)', { c: RED, w: 700, a: 'middle' });
    const x3 = x0 + (3 * lam) / 4;
    b += doan(x3, yc, x3, yc + 44, 'dc', BLUE) + T(x3, yc + 68, '(2)', { c: BLUE, w: 700, a: 'middle' });
    b += arr(262, yc + 70, 306, yc + 70, 'dc', GREY, '', 2.2) + T(256, yc + 77, 'phương truyền', { a: 'end', size: 20, c: GREY });
    return wrap('0 0 320 196', b, cap, 'Hình dạng sợi dây lúc chụp');
  },
  // Trang 3 · nguồn O, điểm M cách O đoạn d
  truyenOM: (cap = 'Sóng rời O, đi hết đoạn d mới tới M.') => {
    let b = defs('om');
    const yc = 96;
    b += arr(14, yc, 312, yc, 'om', INK, '', 2.2) + T(312, yc + 28, 'x', { a: 'end' });
    b += song(30, 250, yc, 26, 74, 0, INK, SW);
    b += cham(30, yc, INK, 6) + T(20, yc + 26, 'O', { w: 700, a: 'end' }) + doan(30, 42, 30, 150, 'om', GREY);
    b += cham(250, yc, RED, 6) + T(250, yc + 30, 'M', { c: RED, w: 700, a: 'middle' });
    b += doan(30, 172, 250, 172, 'om', INK) + T(140, 164, 'd', { a: 'middle', w: 700 });
    b += arr(170, 30, 240, 30, 'om', BLUE) + T(162, 37, 'v', { c: BLUE, w: 700, a: 'end' });
    return wrap('0 0 320 186', b, cap, 'Nguồn O và điểm M trên phương truyền');
  },
  // Trang 3 · cùng đường sin, khác nhãn trục hoành
  haiTruc: (cap = 'Cùng đường sin, khác nhãn trục hoành.') => {
    const fn = (s) => -2 * Math.cos(Math.PI * s);
    const top = doThi({ fn, smax: 4, buoc: 1, A: 2, truc: 't (s)', id: 'ht1', vb: [320, 168], dy: 30 });
    const bot = doThi({ fn, smax: 4, buoc: 1, A: 2, truc: 'x (cm)', id: 'ht2', vb: [320, 344], y0: 176, dy: 30 });
    let b = top + bot;
    // ngoặc "?" giữa hai đỉnh (s = 1 và s = 3), đặt trên đỉnh, dưới dòng nhãn u (cm)
    const X = (s) => 46 + (s / 4) * (320 - 34 - 46);
    b += doan(X(1), 44, X(3), 44, 'ht1', RED) + T(X(2), 38, '?', { c: RED, w: 700, a: 'middle' });
    b += doan(X(1), 220, X(3), 220, 'ht2', RED) + T(X(2), 214, '?', { c: RED, w: 700, a: 'middle' });
    return wrap('0 0 320 344', b, cap, 'Đồ thị u–t và u–x');
  },
  // Trang 4 · bài toán mẫu: O và M cách 9 cm trên Ox
  mauOM: (cap = 'O dao động, sóng truyền theo chiều +Ox.') => {
    let b = defs('mo');
    const yc = 70, O = 34, M = 268;
    b += arr(14, yc, 312, yc, 'mo', INK, '', 2.2) + T(312, yc + 28, 'x', { a: 'end' });
    b += cham(O, yc) + T(O - 8, yc + 26, 'O', { w: 700, a: 'end' }) + doan(O, 30, O, 110, 'mo', GREY);
    b += cham(M, yc, RED, 6) + T(M, yc + 30, 'M', { c: RED, w: 700, a: 'middle' });
    b += doan(O, 130, M, 130, 'mo', INK) + T((O + M) / 2, 122, '9 cm', { a: 'middle', w: 700 });
    b += arr(120, 30, 200, 30, 'mo', BLUE) + T(208, 37, 'v = 60 cm/s', { c: BLUE, size: 20 });
    return wrap('0 0 320 142', b, cap, 'Nguồn O và điểm M cách 9 cm');
  },
  // Trang 5 · thử thách: P sau đỉnh, Q trước đỉnh, sóng truyền sang phải
  suon: (cap = 'Sóng truyền sang phải. P ở sau đỉnh, Q ở trước đỉnh.') => {
    let b = defs('su');
    const yc = 120, lam = 200, x0 = 10;
    b += ln(10, yc, 310, yc, GREY, 2, '6 4') + song(x0, 310, yc, 56, lam, -Math.PI);
    // đỉnh tại x = 160 (sin phase = π/2 khi (x-10)/200·2π + φ = π/2)
    const u = (x) => yc - 56 * Math.sin((2 * Math.PI * (x - x0)) / lam - Math.PI);
    const xp = 112, xq = 208;
    b += cham(xp, u(xp), RED, 6) + T(xp - 10, u(xp) + 4, 'P', { c: RED, w: 700, a: 'end' });
    b += cham(xq, u(xq), BLUE, 6) + T(xq + 10, u(xq) + 4, 'Q', { c: BLUE, w: 700 });
    b += arr(200, 26, 300, 26, 'su', INK) + T(194, 33, 'chiều truyền', { a: 'end', size: 20 });
    return wrap('0 0 320 196', b, cap, 'Một đỉnh sóng, điểm P và Q hai bên');
  },
  // Trang 6 · Dạng 2: dây, M và N cách 10,5 cm
  dayMN: (cap = 'Sóng truyền từ M tới N.') => {
    let b = defs('mn');
    const yc = 66, M = 40, N = 284;
    b += ln(10, yc, 312, yc, INK, SW);
    b += cham(M, yc, RED, 6) + T(M, yc + 30, 'M', { c: RED, w: 700, a: 'middle' }) + cham(N, yc, RED, 6) + T(N, yc + 30, 'N', { c: RED, w: 700, a: 'middle' });
    b += doan(M, 112, N, 112, 'mn') + T((M + N) / 2, 104, '10,5 cm', { a: 'middle', w: 700 });
    b += arr(120, 30, 210, 30, 'mn', BLUE) + T(218, 37, 'v', { c: BLUE, w: 700 });
    return wrap('0 0 320 124', b, cap, 'Dây, hai điểm M và N');
  },
  // Trang 7 · Dạng 5: (a) u = 3 sin(πx/12) lúc t = 0, M ở x = 6 cm; (b) u_M = 3 cos(5πt)
  d5: (cap = '') => haiDoThi(
    { fn: (x) => 3 * Math.sin((Math.PI * x) / 12), smax: 36, buoc: 3, nhan: 2, A: 3, truc: 'x (cm)', M: [6, 'M'] },
    { fn: (s) => 3 * Math.cos(5 * Math.PI * s), smax: 0.8, buoc: 0.1, nhan: 2, A: 3, truc: 't (s)' }, cap, 'd5'),
  // Trang 9 · Bài tương tự D5·1: A = 4 cm, λ = 20 cm, T = 0,5 s, M ở x = 5 cm
  tt51: (cap = '') => haiDoThi(
    { fn: (x) => 4 * Math.sin((Math.PI * x) / 10), smax: 30, buoc: 2.5, nhan: 2, A: 4, truc: 'x (cm)', M: [5, 'M'] },
    { fn: (s) => 4 * Math.cos(4 * Math.PI * s), smax: 1, buoc: 0.125, nhan: 2, A: 4, truc: 't (s)' }, cap, 't51'),
  // Trang 9 · Bài tương tự D5·2: A = 2 cm, λ = 40 cm, T = 0,2 s, M ở x = 10 cm (u = 0, đang đi lên)
  tt52: (cap = '') => haiDoThi(
    { fn: (x) => 2 * Math.cos((Math.PI * x) / 20), smax: 50, buoc: 5, nhan: 2, A: 2, truc: 'x (cm)', M: [10, 'M'] },
    { fn: (s) => 2 * Math.sin(10 * Math.PI * s), smax: 0.3, buoc: 0.05, nhan: 1, A: 2, truc: 't (s)' }, cap, 't52'),
};
export { LAM, sb };
