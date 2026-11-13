// Hình minh hoạ cho ruột tập VL11 · Bài 6 Dao động tắt dần. Dao động cưỡng bức. Hiện tượng cộng hưởng (lesson 25).
// Cùng quy tắc với hinh.mjs: mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,4, phân biệt bằng nét (đặc – đứt – chấm)
// chứ không chỉ bằng màu, tự vẽ. Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh.
// Đồ thị đọc số: có lưới + vạch chia ghi số. Xem thử: node scripts/ruot-tap/l11-bai6.mjs --hinh (chụp vào out/hinh-l11-bai6/).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const f1 = (v) => (+v).toFixed(1);
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${f1(x1)}" y1="${f1(y1)}" x2="${f1(x2)}" y2="${f1(y2)}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const arr = (x1, y1, x2, y2, id, c = INK, dash = '', w = SW) =>
  `<line x1="${f1(x1)}" y1="${f1(y1)}" x2="${f1(x2)}" y2="${f1(y2)}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const path = (pts, c = INK, w = 2.6, dash = '') =>
  `<path d="M${pts.map(([x, y]) => `${f1(x)},${f1(y)}`).join(' L')}" fill="none" stroke="${c}" stroke-width="${w}" stroke-linejoin="round"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const vs = (s) => s.replace('.', ',');

// Hệ trục có lưới đọc số. o: { x0, y0 (gốc trên giấy), w, h, xmin, xmax, ymin, ymax, xt: [vạch ghi số], yt, xl, yl, luoi: bước lưới phụ [dx, dy] }
const truc = (o, id) => {
  const { x0, y0, w, h, xmin, xmax, ymin, ymax, xt = [], yt = [], xl = '', yl = '', luoi, am = false } = o;
  const X = (v) => x0 + ((v - xmin) / (xmax - xmin)) * w, Y = (v) => y0 - ((v - ymin) / (ymax - ymin)) * h;
  let b = defs(id);
  if (luoi) {
    const [dx, dy] = luoi;
    for (let v = xmin + dx; v <= xmax + 1e-9; v += dx) b += ln(X(v), y0, X(v), y0 - h, GREY, 1, '');
    for (let v = ymin + dy; v <= ymax + 1e-9; v += dy) b += ln(x0, Y(v), x0 + w, Y(v), GREY, 1, '');
  }
  b += arr(x0, y0, x0 + w + 16, y0, id) + arr(x0, y0, x0, y0 - h - 16, id) + (am ? ln(x0, y0, x0, y0 + h) : '');
  xt.forEach((v) => { b += ln(X(v), y0, X(v), y0 + 6, INK, 2) + T(X(v), y0 + 26, vs(String(v)), { a: 'middle' }); });
  yt.forEach((v) => { b += ln(x0 - 6, Y(v), x0, Y(v), INK, 2) + T(x0 - 9, Y(v) + 7, vs(String(v)), { a: 'end' }); });
  b += (am ? T(x0 + w + 20, y0 + 7, xl) : T(x0 + w + 16, y0 - 10, xl, { a: 'end' })) + T(x0 + 8, y0 - h - 6, yl);
  return { b, X, Y };
};
const mau = (fn, a, z, n = 160) => Array.from({ length: n + 1 }, (_, i) => { const v = a + ((z - a) * i) / n; return [v, fn(v)]; });
const cong = (Ar, bw, f0) => (f) => (Ar * bw) / Math.sqrt((f - f0) ** 2 + bw ** 2);

// lò xo thẳng đứng từ (x, y1) xuống (x, y2)
const loXo = (x, y1, y2, n = 7, r = 9) => {
  const d = (y2 - y1) / (n * 2 + 2);
  let p = `M${x},${y1} L${x},${f1(y1 + d)}`;
  for (let i = 0; i < n * 2; i++) p += ` L${f1(x + (i % 2 ? -r : r))},${f1(y1 + d * (i + 1.5))}`;
  p += ` L${x},${f1(y2 - d)} L${x},${y2}`;
  return `<path d="${p}" fill="none" stroke="${INK}" stroke-width="2.4"/>`;
};
const dat = (x1, x2, y) => ln(x1, y, x2, y) + Array.from({ length: Math.floor((x2 - x1) / 18) }, (_, i) =>
  ln(x1 + 8 + i * 18, y, x1 + i * 18, y + 8, GREY, 1.8)).join('');

export const hinhL11b6 = {
  // Trang 1 · Dự đoán: xích đu. Chú thích chỉ tả cảnh, không nêu lí do (đáp án C).
  xichDu: (cap = 'Hai lần đu: ngồi yên, và nhún lúc đu đang đi xuống.') => {
    let b = defs('xd1');
    b += ln(40, 14, 280, 14, INK, 4) + ln(60, 14, 40, 200) + ln(260, 14, 280, 200) + dat(10, 310, 200);
    const tx = 160, ty = 14, L = 150, a = (g) => [tx + L * Math.sin((g * Math.PI) / 180), ty + L * Math.cos((g * Math.PI) / 180)];
    // vị trí giữa (mờ) và vị trí lệch 32°
    const [xm, ym] = a(0), [xl, yl] = a(32);
    b += ln(tx, ty, xm, ym, GREY, 2, '5 4') + ln(xm - 22, ym, xm + 22, ym, GREY, 3, '5 4');
    b += ln(tx, ty, xl, yl) + `<rect x="${f1(xl - 24)}" y="${f1(yl - 4)}" width="48" height="8" rx="2" fill="${INK}"/>`;
    // người ngồi
    b += `<circle cx="${f1(xl + 2)}" cy="${f1(yl - 46)}" r="10" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + ln(xl + 2, yl - 36, xl, yl - 6) + ln(xl, yl - 6, xl + 26, yl + 2) + ln(xl + 26, yl + 2, xl + 30, yl + 26);
    // cung chuyển động, mũi tên đi xuống
    const p = mau((g) => g, -32, 32, 40).map(([g]) => a(g)).map(([x, y]) => [x, y + 26]);
    b += path(p, BLUE, 2.2, '6 5');
    const [x1, y1] = a(26), [x2, y2] = a(14);
    b += arr(x1, y1 + 26, x2, y2 + 26, 'xd1', BLUE, '', 2.6) + T(xm - 8, y2 + 8, 'đi xuống', { c: BLUE, a: 'end' });
    return wrap('0 0 320 212', b, cap, 'Xích đu đang đi xuống');
  },

  // Trang 1 · thí nghiệm ba môi trường: x – t, cùng A0 = 5 cm, chu kì ≈ 1 s
  baMoiTruong: (cap = 'Cùng lệch 5,0 cm, cùng lúc thả. Nét đặc, đứt, chấm: ba môi trường.') => {
    const { b: ax, X, Y } = truc({ x0: 40, y0: 104, w: 222, h: 84, xmin: 0, xmax: 2.2, ymin: 0, ymax: 5, xt: [1, 2], yt: [5], xl: 't (s)', yl: 'x (cm)', am: true }, 'bm1');
    let b = ax + ln(40, Y(-5) + 0, 262, Y(-5), GREY, 1, '3 4') + T(31, Y(-5) + 7, '−5', { a: 'end' });
    const Yx = (v) => 104 - (v / 5) * 84;
    const dd = [[0.40, INK, ''], [1.15, BLUE, '7 5'], [2.8, RED, '2 4']];
    dd.forEach(([be, c, dash]) => { b += path(mau((s) => 5 * Math.exp(-be * s) * Math.cos(2 * Math.PI * s), 0, 2.2, 220).map(([s, v]) => [X(s), Yx(v)]), c, 2.6, dash); });
    return wrap('0 0 320 196', b, cap, 'Li độ theo thời gian trong không khí, nước, dầu');
  },

  // Trang 2 · duy trì: đồng hồ quả lắc, cơ cấu bù chỉ chạm trong đoạn ngắn
  dongHo: (cap = 'Mỗi nhịp, cơ cấu thoát chỉ đẩy quả lắc trong một đoạn ngắn (vùng tô đậm).') => {
    let b = defs('dh1');
    b += `<rect x="96" y="6" width="128" height="196" rx="10" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<circle cx="160" cy="44" r="28" fill="#fff" stroke="${INK}" stroke-width="2.4"/>` + ln(160, 44, 160, 26, INK, 2.6) + ln(160, 44, 174, 50, INK, 2.6);
    const px = 160, py = 78, L = 96, a = (g) => [px + L * Math.sin((g * Math.PI) / 180), py + L * Math.cos((g * Math.PI) / 180)];
    const [x, y] = a(-14);
    b += ln(px, py, x, y) + `<circle cx="${f1(x)}" cy="${f1(y)}" r="13" fill="${GREY}" stroke="${INK}" stroke-width="${SW}"/>`;
    const arc = mau((g) => g, -22, 22, 30).map(([g]) => a(g)).map(([xx, yy]) => [xx, yy + 22]);
    b += path(arc, GREY, 2, '4 4');
    const dam = mau((g) => g, -4, 4, 8).map(([g]) => a(g)).map(([xx, yy]) => [xx, yy + 22]);
    b += path(dam, RED, 7);
    b += T(304, 150, 'đẩy', { c: RED, a: 'end', w: 700 }) + ln(262, 152, 172, 196, RED, 1.6, '3 3');
    b += T(10, 40, 'pin /', { w: 700 }) + T(10, 64, 'dây cót', { w: 700 });
    return wrap('0 0 320 212', b, cap, 'Đồng hồ quả lắc');
  },

  // Trang 2 · cộng hưởng: hai đường ①, ② cùng F0, khác lực cản — HS ghi tên lực cản (không ghi sẵn)
  congHuong: (cap = 'Cùng F<sub>0</sub>, hai mức lực cản. Ghi “cản nhỏ”/“cản lớn” cạnh 1, 2.') => {
    const { b: ax, X, Y } = truc({ x0: 30, y0: 160, w: 262, h: 132, xmin: 0, xmax: 4, ymin: 0, ymax: 6.5, xl: 'f', yl: 'A' }, 'ch1');
    let b = ax;
    b += path(mau(cong(6, 0.25, 2), 0.05, 4).map(([f, a]) => [X(f), Y(a)]), INK, 2.8);
    b += path(mau(cong(2.5, 1.0, 2), 0.05, 4).map(([f, a]) => [X(f), Y(a)]), BLUE, 2.8, '8 5');
    b += ln(X(2), 160, X(2), Y(6), GREY, 1.8, '4 4') + T(X(2), 186, `f${sb('0')}`, { a: 'middle' });
    const so = (x, y, n, c = INK) => `<circle cx="${x}" cy="${y - 7}" r="13" fill="#fff" stroke="${c}" stroke-width="2"/>` + T(x, y, n, { w: 700, c, a: 'middle' });
    b += so(X(2) + 34, Y(5.8), '1') + so(X(3.3) + 16, Y(1.9) - 6, '2', BLUE);
    return wrap('0 0 320 196', b, cap, 'Biên độ dao động cưỡng bức theo tần số lực');
  },

  // Trang 3 · thí nghiệm quét tần số: lưới trống để HS chấm 5 điểm của bảng
  luoiQuet: (cap = 'Chấm 5 điểm (f; A) của bảng rồi nối thành đường cong.') => {
    const { b } = truc({ x0: 44, y0: 166, w: 250, h: 140, xmin: 0.5, xmax: 3.5, ymin: 0, ymax: 7, xt: [1, 1.5, 2, 2.5, 3], yt: [1, 2, 3, 4, 5, 6, 7], xl: 'f (Hz)', yl: 'A (cm)', luoi: [0.25, 0.5] }, 'lq1');
    return wrap('0 0 320 200', b, cap, 'Lưới vẽ đồ thị biên độ theo tần số');
  },

  // Trang 4 · bài toán mẫu: bệ máy trên lò xo, lực tuần hoàn
  beMay: (cap = 'Bệ máy trên lò xo. Lực F = 20 cos(2<span style="font-family:KaTeX_Main">π</span><i>f</i><i>t</i>) N đặt liên tục; f đổi được.') => {
    let b = defs('bm2') + dat(10, 310, 190);
    b += loXo(90, 132, 190) + loXo(230, 132, 190);
    b += `<rect x="60" y="104" width="200" height="28" rx="3" fill="${GREY}" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<rect x="112" y="56" width="96" height="48" rx="6" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(160, 88, 'máy', { a: 'middle', w: 700 });
    b += arr(160, 50, 160, 8, 'bm2', RED) + ln(160, 50, 160, 54, RED) + T(172, 26, 'F', { c: RED, w: 700 });
    b += `<path d="M268,90 l0,40" stroke="${BLUE}" stroke-width="2.6" marker-end="url(#bm2)" marker-start="url(#bm2)"/>` + T(278, 118, 'A ?', { c: BLUE, w: 700 });
    return wrap('0 0 320 200', b, cap, 'Bệ máy trên lò xo');
  },

  // Trang 5 · thử thách ★★★: động cơ trên đệm có giảm chấn dầu
  dongCo: (cap = 'Động cơ chạy 25 Hz trên bệ có lò xo và ống dầu.') => {
    let b = dat(10, 310, 190);
    b += loXo(80, 132, 190);
    b += `<rect x="208" y="150" width="34" height="40" fill="#fff" stroke="${INK}" stroke-width="2.4"/>` + ln(225, 132, 225, 168, INK, 2.4) + ln(212, 168, 238, 168, INK, 4);
    b += `<rect x="40" y="104" width="240" height="28" rx="3" fill="${GREY}" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<rect x="100" y="54" width="120" height="50" rx="8" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(160, 86, 'động cơ', { a: 'middle', w: 700 });
    b += T(80, 26, 'lò xo', { a: 'middle' }) + ln(80, 30, 80, 128, GREY, 1.4, '3 3');
    b += T(296, 26, 'ống dầu', { a: 'end' }) + ln(250, 30, 232, 148, GREY, 1.4, '3 3');
    return wrap('0 0 320 200', b, cap, 'Động cơ trên bệ có lò xo và giảm chấn');
  },

  // ===== Bài tập mẫu =====
  // D1: đồ thị x – t của ba con lắc trong 4 s, T0 = 1,0 s; (3) cưỡng bức 1,5 Hz
  d1: (cap = 'Li độ x (cm) theo t (s) của ba con lắc.') => {
    const row = (y0, fn, nhan, id) => {
      const { b, X } = truc({ x0: 46, y0, w: 252, h: 18, xmin: 0, xmax: 4, ymin: 0, ymax: 4, xt: [], xl: '', yl: '', am: true }, id);
      const Yv = (v) => y0 - (v / 4) * 18;
      return b + ln(46, Yv(-4), 298, Yv(-4), GREY, 1, '3 4') + T(8, y0 + 7, nhan, { w: 700 })
        + [1, 2, 3, 4].map((k) => ln(X(k), y0 - 22, X(k), y0 + 22, GREY, 1, '2 4')).join('')
        + path(mau(fn, 0, 4, 320).map(([s, v]) => [X(s), Yv(v)]), INK, 2.4);
    };
    let b = row(27, (s) => 4 * Math.exp(-0.35 * s) * Math.cos(2 * Math.PI * s), '(1)', 'p1')
      + row(76, (s) => 4 * Math.cos(2 * Math.PI * s), '(2)', 'p2')
      + row(125, (s) => 3 * Math.cos(2 * Math.PI * 1.5 * s), '(3)', 'p3');
    b += [1, 2, 3, 4].map((k) => T(46 + k * 63, 168, String(k), { a: 'middle' })).join('') + T(14, 168, 't (s)');
    return wrap('0 0 320 174', b, cap, 'Đồ thị li độ ba con lắc');
  },
  // D3: biên độ giảm theo hàm mũ, đường bao nét đứt, mốc 5 s
  d3: (cap = 'Đường đứt: biên độ A = 5,0 e<sup>−0,20t</sup> (cm).') => {
    const { b: ax, X, Y } = truc({ x0: 40, y0: 80, w: 222, h: 62, xmin: 0, xmax: 6, ymin: 0, ymax: 5, xt: [1, 2, 3, 4, 5, 6], yt: [5], xl: 't (s)', yl: 'x (cm)', am: true }, 'd31');
    const Yx = (v) => 80 - (v / 5) * 62;
    let b = ax + ln(40, Yx(-5), 262, Yx(-5), GREY, 1, '3 4') + T(31, Yx(-5) + 7, '−5', { a: 'end' });
    b += path(mau((s) => 5 * Math.exp(-0.2 * s) * Math.cos(2 * Math.PI * s), 0, 6, 360).map(([s, v]) => [X(s), Yx(v)]), INK, 2.2);
    b += path(mau((s) => 5 * Math.exp(-0.2 * s), 0, 6, 60).map(([s, v]) => [X(s), Yx(v)]), RED, 2.4, '7 5');
    b += ln(X(5), Yx(5 * Math.exp(-1)) - 6, X(5), 80, BLUE, 2, '3 3');
    return wrap('0 0 320 152', b, cap, 'Biên độ tắt dần theo thời gian');
  },
  // D4: xe qua các gờ cách đều L
  d4: (cap = 'Gờ cách đều L = 6,0 m. Thời gian đi giữa hai gờ = chu kì lực.') => {
    let b = defs('d41') + dat(6, 314, 132);
    [30, 170, 310].forEach((x) => { b += `<path d="M${x - 14},132 Q${x},112 ${x + 14},132" fill="${GREY}" stroke="${INK}" stroke-width="2.4"/>`; });
    b += `<path d="M64,96 L84,70 L150,70 L168,96 Z" fill="#fff" stroke="${INK}" stroke-width="${SW}"/><rect x="52" y="94" width="130" height="18" rx="4" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<circle cx="80" cy="118" r="12" fill="#fff" stroke="${INK}" stroke-width="${SW}"/><circle cx="156" cy="118" r="12" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += arr(190, 82, 250, 82, 'd41', BLUE, '6 4') + T(220, 70, 'v', { c: BLUE, w: 700, a: 'middle' });
    b += `<path d="M30,154 L310,154" stroke="${INK}" stroke-width="2" marker-end="url(#d41)" marker-start="url(#d41)"/>`;
    b += T(170, 180, 'L', { a: 'middle', w: 700 }) + ln(170, 138, 170, 160, GREY, 1.4, '3 3');
    return wrap('0 0 320 190', b, cap, 'Xe qua gờ giảm tốc cách đều');
  },
  // D5: hai đường cộng hưởng của đệm X, Y (cùng f0 = 5 Hz) — vạch 20 Hz
  d5: (cap = 'Đệm X (đặc) và Y (đứt), cùng f<sub>0</sub> = 5,0 Hz. Máy chạy ổn định ở 20 Hz.') => {
    const { b: ax, X, Y } = truc({ x0: 40, y0: 160, w: 252, h: 130, xmin: 0, xmax: 22, ymin: 0, ymax: 8, xt: [5, 10, 15, 20], yt: [2, 4, 6, 8], xl: 'f (Hz)', yl: 'A (cm)', luoi: [5, 1] }, 'd51');
    let b = ax;
    b += path(mau(cong(7.5, 0.4, 5), 0.05, 22, 400).map(([f, a]) => [X(f), Y(a)]), INK, 2.6);
    b += path(mau(cong(2.0, 1.5, 5), 0.05, 22, 200).map(([f, a]) => [X(f), Y(a)]), BLUE, 2.6, '8 5');
    b += ln(40, Y(3), 292, Y(3), RED, 1.8, '3 3') + T(290, Y(3) - 6, '3,0', { c: RED, a: 'end' });
    b += ln(X(20), 160, X(20), Y(2), GREY, 2, '4 4') + T(X(5) + 10, Y(7.5) + 6, 'X', { w: 700 }) + T(X(8.5), Y(1.3) - 4, 'Y', { w: 700, c: BLUE });
    return wrap('0 0 320 196', b, cap, 'Đường cộng hưởng của hai loại đệm');
  },
  // ===== Bài tương tự =====
  beRung: (cap = 'Con lắc lò xo trên bệ rung.') => {
    let b = defs('br1') + dat(10, 310, 172);
    b += `<rect x="70" y="128" width="180" height="22" rx="3" fill="${GREY}" stroke="${INK}" stroke-width="${SW}"/>` + ln(100, 150, 100, 172, INK, 4) + ln(220, 150, 220, 172, INK, 4);
    b += ln(110, 128, 110, 20, INK, 3) + ln(110, 20, 180, 20, INK, 3) + loXo(170, 20, 84, 6, 9);
    b += `<rect x="150" y="84" width="40" height="30" rx="3" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<path d="M270,118 L300,118" stroke="${BLUE}" stroke-width="2.6" marker-end="url(#br1)" marker-start="url(#br1)"/>` + T(285, 104, 'rung', { c: BLUE, a: 'middle' });
    return wrap('0 0 320 182', b, cap, 'Con lắc lò xo trên bệ rung');
  },
  ganhNuoc: (cap = 'Mỗi bước dài 0,60 m: thùng bị đẩy một lần.') => {
    let b = defs('gn1') + dat(6, 314, 186);
    b += `<circle cx="160" cy="40" r="12" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + ln(160, 52, 160, 120) + ln(160, 120, 140, 184) + ln(160, 120, 184, 184);
    b += ln(40, 60, 280, 60, INK, 5) + ln(160, 64, 160, 64);
    [[60, 74], [260, 74]].forEach(([x]) => { b += ln(x, 60, x - 14, 100, GREY, 1.6) + ln(x, 60, x + 14, 100, GREY, 1.6) + `<path d="M${x - 22},100 L${x + 22},100 L${x + 18},146 L${x - 18},146 Z" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + `<path d="M${x - 20},114 Q${x - 8},106 ${x},114 T${x + 20},114" fill="none" stroke="${BLUE}" stroke-width="2.4"/>`; });
    b += `<path d="M140,198 L184,198" stroke="${INK}" stroke-width="2" marker-end="url(#gn1)" marker-start="url(#gn1)"/>`;
    return wrap('0 0 320 206', b, cap, 'Người gánh hai thùng nước');
  },
};
