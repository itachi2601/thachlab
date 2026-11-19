// Hình minh hoạ cho ruột tập VL11 · Bài 2 Mô tả dao động điều hoà (lesson 21). Cùng quy tắc với hinh.mjs/hinh-l10-bai23.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chữ Hi Lạp (π φ ω Δ) lấy từ font KaTeX (Source Sans 3 chỉ nạp latin/vietnamese → tránh rơi về Helvetica). Không dùng √ trong SVG.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh. Xem thử: node scripts/ruot-tap/l11-bai2.mjs --hinh (chụp vào out/hinh-l11-bai2/).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const gu = (ch) => `<tspan font-family="KaTeX_Main">${ch}</tspan>`; // Δ, π đứng
const PI = gk('π');
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const arr = (x1, y1, x2, y2, id, c = INK, dash = '', w = SW) =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const R = (d) => (d * Math.PI) / 180;
const f1 = (v) => (+v).toFixed(1);
const so = (v) => String(v).replace('.', ','); // số kiểu Việt
// cung tâm (x,y) bán kính r từ góc a1 tới a2 (độ, chiều toán học); sweep tự chọn theo dấu
const cung = (x, y, r, a1, a2, c = INK, id = '') => {
  const p = (a) => `${f1(x + r * Math.cos(R(a)))},${f1(y - r * Math.sin(R(a)))}`;
  return `<path d="M${p(a1)} A${r},${r} 0 0 ${a2 > a1 ? 0 : 1} ${p(a2)}" fill="none" stroke="${c}" stroke-width="2.2"${id ? ` marker-end="url(#${id})"` : ''}/>`;
};
const cham = (x, y, c = INK, r = 5) => `<circle cx="${f1(x)}" cy="${f1(y)}" r="${r}" fill="${c}"/>`;

// Đồ thị x–t đọc được số: x = A cos(2π t/T + φ), lưới theo bước thời gian `buoc`, nhãn thời gian mỗi `nhan` bước,
// nhãn trục x ở ±A, ±A/2, 0. `cham`: các thời điểm chấm tròn. `cong2`: đường thứ hai (nét đứt).
const doThi = ({ A, T: Tc, phi, tmax, buoc, nhan = 1, cham: chs = [], cong2 = null, vb = [320, 210], id = 'dt', xLabel = true, yTicks = null, fz = 21 }) => {
  const [W, H] = vb, x0 = 50, x1 = W - 50, yc = H / 2 - 4, ay = H / 2 - 30;
  const X = (tt) => x0 + (tt / tmax) * (x1 - x0), Y = (x, Am = A) => yc - (x / Am) * ay;
  let b = defs(id + 'a');
  const n = Math.round(tmax / buoc);
  for (let i = 1; i <= n; i++) {
    const tt = i * buoc, x = X(tt);
    b += ln(f1(x), yc - ay - 6, f1(x), yc + ay + 6, '#c4cbdc', 1.4);
    if (i % nhan === 0) b += T(f1(x), yc + ay + 30, so(+tt.toFixed(3)), { a: 'middle', size: fz });
  }
  const yt = yTicks ?? [A, A / 2, -A / 2, -A];
  yt.forEach((v) => { b += ln(x0, f1(Y(v)), x1, f1(Y(v)), '#c4cbdc', 1.4) + T(x0 - 6, f1(Y(v) + 6), so(v).replace('-', '−'), { a: 'end', size: fz }); });
  b += T(x0 - 6, yc + 6, '0', { a: 'end', size: fz });
  b += arr(x0, yc + ay + 10, x0, 10, id + 'a', INK, '', 2.2) + arr(x0, yc, W - 4, yc, id + 'a', INK, '', 2.2);
  b += T(x0 + 8, 22, 'x (cm)', { size: 18 }) + (xLabel ? T(W - 4, yc - 10, 't (s)', { a: 'end', size: 19 }) : '');
  const path = (Am, Tt, ph, dash = '', c = INK) => {
    let d = '';
    for (let k = 0; k <= 240; k++) { const tt = (k / 240) * tmax; d += `${k ? 'L' : 'M'}${f1(X(tt))},${f1(Y(Am * Math.cos((2 * Math.PI * tt) / Tt + ph), A))}`; }
    return `<path d="${d}" fill="none" stroke="${c}" stroke-width="${SW}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
  };
  b += path(A, Tc, phi);
  if (cong2) b += path(cong2.A ?? A, cong2.T ?? Tc, cong2.phi, '7 5', BLUE);
  chs.forEach((tt) => { b += `<circle cx="${f1(X(tt))}" cy="${f1(Y(A * Math.cos((2 * Math.PI * tt) / Tc + phi)))}" r="5.5" fill="#fff" stroke="${RED}" stroke-width="2.6"/>`; });
  return { b, X, Y, yc, ay, W, H };
};

// Vòng tròn pha: M trên vòng bán kính A ở góc `goc` (độ), P là hình chiếu lên Ox. hai = góc bán kính thứ hai (nét đứt).
const vongTron = ({ goc = 60, nhanGoc = gk('φ'), hai = null, nhan = ['M', 'P'], xA = ['−A', 'A'], id = 'vt', cap, label = 'Vòng tròn pha', om = 118, oTren = false }) => {
  const cx = 150, cy = 112, r = 82;
  let b = defs(id + 'a') + defs(id + 'b');
  b += `<circle cx="${cx}" cy="${cy}" r="${r}" fill="none" stroke="${GREY}" stroke-width="2.2"/>`;
  b += arr(cx - r - 26, cy, cx + r + 34, cy, id + 'a', INK, '', 2.2) + T(cx + r + 34, cy + 24, 'x', { a: 'end' });
  b += T(cx - r - 4, cy + 26, xA[0], { a: 'end', size: 20 }) + T(cx + r + 4, cy + 26, xA[1], { size: 20 }) + T(cx - 6, cy + (oTren ? -10 : 24), 'O', { a: 'end' });
  // chiều quay ngược chiều kim đồng hồ
  b += cung(cx, cy, r + 14, om, om + 34, BLUE, id + 'b') + T(cx + (r + 30) * Math.cos(R(om + 17)), cy - (r + 30) * Math.sin(R(om + 17)) + 8, gk('ω'), { c: BLUE, size: 22, a: 'middle' });
  const M = (g) => [cx + r * Math.cos(R(g)), cy - r * Math.sin(R(g))];
  const [mx, my] = M(goc);
  b += ln(cx, cy, f1(mx), f1(my), RED) + cham(mx, my, RED, 6);
  b += ln(f1(mx), f1(my), f1(mx), cy, GREY, 2, '5 4') + cham(mx, cy, INK, 6);
  b += T(mx + (goc > 90 || goc < -90 ? -10 : 10), my + (goc >= 0 ? -6 : 22), nhan[0], { c: RED, w: 700, a: goc > 90 || goc < -90 ? 'end' : 'start' });
  b += T(mx + 4, cy + (goc >= 0 ? 26 : -10), nhan[1], { w: 700 });
  if (nhanGoc) b += cung(cx, cy, 30, 0, goc) + T(cx + 40 * Math.cos(R(goc / 2)) + 2, cy - 40 * Math.sin(R(goc / 2)) + 8, nhanGoc);
  if (hai) {
    const [hx, hy] = M(hai.goc);
    b += ln(cx, cy, f1(hx), f1(hy), BLUE, SW, '7 5') + cham(hx, hy, BLUE, 6);
    b += T(hx + (hai.goc > 90 || hai.goc < -90 ? -10 : 10), hy + (hai.goc >= 0 ? -6 : 22), hai.nhan, { c: BLUE, w: 700, a: hai.goc > 90 || hai.goc < -90 ? 'end' : 'start' });
  }
  return wrap('0 0 300 216', b, cap, label);
};

export const hinhL11b2 = {
  // Trang 1 · Dự đoán: hai người bắt đầu nhìn quả lắc ở hai lúc khác nhau
  conLac: (cap = 'An bấm lúc quả lắc ở +A, Bình bấm lúc nó qua O.') => {
    let b = defs('cl1');
    const px = 160, py = 18, L = 140;
    b += ln(110, py, 210, py, INK, 4) + Array.from({ length: 6 }, (_, i) => ln(116 + i * 17, py, 108 + i * 17, py - 9, GREY, 1.8)).join('');
    [-22, 0, 22].forEach((g, i) => {
      const bx = px + L * Math.sin(R(g)), by = py + L * Math.cos(R(g));
      b += ln(px, py, f1(bx), f1(by), i === 1 ? INK : GREY, i === 1 ? SW : 2, i === 1 ? '' : '6 4');
      b += `<circle cx="${f1(bx)}" cy="${f1(by)}" r="13" fill="#fff" stroke="${i === 1 ? INK : GREY}" stroke-width="${SW}"${i === 1 ? '' : ' stroke-dasharray="6 4"'}/>`;
    });
    const yR = 196, xL = px - L * Math.sin(R(22)), xR = px + L * Math.sin(R(22));
    b += ln(xL - 30, yR, xR + 30, yR, INK, 2.2);
    [xL, px, xR].forEach((x) => { b += ln(f1(x), yR - 7, f1(x), yR + 7, INK, 2.2); });
    b += T(xL, yR + 28, '−A', { a: 'middle' }) + T(px, yR + 28, 'O', { a: 'middle' }) + T(xR, yR + 28, '+A', { a: 'middle' });
    b += T(xR + 20, py + L * Math.cos(R(22)) - 10, 'An', { c: RED, w: 700 }) + T(px - 20, py + L + 4, 'Bình', { c: BLUE, w: 700, a: 'end' });
    return wrap('0 0 320 232', b, cap, 'Quả lắc đồng hồ, hai lúc bắt đầu nhìn');
  },
  // Trang 1 · thí nghiệm lò xo kéo lệch 4 cm
  loXo: (cap = 'Bên kia O, vật đi tới vạch nào?') => {
    let b = defs('lx1');
    b += ln(14, 30, 14, 108, INK, 4) + Array.from({ length: 5 }, (_, i) => ln(14, 36 + i * 16, 4, 46 + i * 16, GREY, 1.8)).join('');
    b += ln(14, 108, 312, 108, INK, 2.4);
    // lò xo zigzag từ x=14 tới khối ở vị trí kéo lệch (O = 170, 1 cm = 22 đơn vị) → khối ở 170+88
    const O = 170, cm = 22, bx = O + 4 * cm;
    let d = `M14,80 L30,80`; const n = 12, w = (bx - 22 - 30) / n;
    for (let i = 0; i < n; i++) d += ` L${f1(30 + (i + 0.5) * w)},${i % 2 ? 92 : 68}`;
    d += ` L${f1(bx - 22)},80`;
    b += `<path d="${d}" fill="none" stroke="${INK}" stroke-width="2.4"/>`;
    b += `<rect x="${bx - 22}" y="58" width="44" height="44" rx="4" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    // thước
    for (let k = -6; k <= 6; k++) {
      const x = O + k * cm;
      b += ln(x, 118, x, k % 2 ? 126 : 132, INK, 2);
      if (k % 2 === 0) b += T(x, 156, String(k).replace('-', '−'), { a: 'middle', size: 18 });
    }
    b += T(O, 182, 'O', { a: 'middle', w: 700 }) + T(312, 182, 'x (cm)', { a: 'end', size: 18 });
    b += ln(O, 40, O, 112, GREY, 2, '5 4');
    b += arr(O, 44, bx - 2, 44, 'lx1', RED) + T((O + bx) / 2, 30, 'kéo 4 cm', { c: RED, a: 'middle', size: 18 });
    return wrap('0 0 320 192', b, cap, 'Con lắc lò xo nằm ngang và thước');
  },
  // Trang 2 · vòng tròn pha
  vongPha: (cap = 'M quay đều ngược chiều kim đồng hồ; P là hình chiếu của M lên Ox.') => vongTron({ goc: 50, id: 'vp', cap }),
  // Trang 2 · hai dao động lệch pha
  lechPha: (cap = 'Đường 1 (liền) và đường 2 (đứt) cùng chu kì T. Đỉnh nào đến trước?') => {
    const g = doThi({ A: 1, T: 1, phi: 0, tmax: 1.3, buoc: 0.25, nhan: 99, cong2: { phi: -Math.PI / 2 }, yTicks: [], id: 'lp', vb: [320, 236] });
    let b = g.b;
    b += T(g.X(0.13) + 8, g.Y(0.7), '1', { w: 700 }) + T(g.X(0.38) + 8, g.Y(0.7), '2', { w: 700, c: BLUE });
    const yy = g.yc + 34;
    b += ln(g.X(1), g.Y(1), g.X(1), yy, GREY, 1.6, '4 3') + ln(g.X(1.25), g.Y(1), g.X(1.25), yy, GREY, 1.6, '4 3');
    b += `<path d="M${f1(g.X(1))},${f1(yy)} L${f1(g.X(1.25))},${f1(yy)}" stroke="${RED}" stroke-width="2.4"/>` + T(g.X(1.125) - 6, yy + 24, `${gu('Δ')}t = ?`, { c: RED, a: 'middle', w: 700, size: 19 });
    b += ln(g.X(1), g.yc - 6, g.X(1), g.yc + 6, INK, 2.2) + T(g.X(1) - 4, g.yc + g.ay + 30, 'T', { a: 'middle', size: 20 });
    return wrap('0 0 320 236', b, cap, 'Hai đồ thị lệch pha');
  },
  // Trang 3 · đồ thị năm chấm x = 5cos(2πt)
  namCham: (cap = 'Năm chấm là năm lần đọc thước, mỗi lần cách 0,10 s.') => {
    const g = doThi({ A: 5, T: 1, phi: 0, tmax: 1.2, buoc: 0.1, nhan: 2, cham: [0, 0.1, 0.2, 0.3, 0.4], yTicks: [5, -5], id: 'nc' });
    return wrap('0 0 320 210', g.b, cap, 'Đồ thị li độ – thời gian, năm lần đọc');
  },
  // Trang 4 · bài toán mẫu: vòng tròn cho φ = π/3
  mauVong: (cap = 'M lúc t = 0. Tăng t một chút: P đi về phía nào?') => vongTron({ goc: 60, nhanGoc: `${PI}/3`, xA: ['−6', '6'], id: 'mv', cap }),
  // ===== Bài tập mẫu =====
  // Dạng 3: hai bán kính lúc t = 0
  haiBanKinh: (cap = 'Hai bán kính lúc t = 0.') =>
    vongTron({ goc: 30, nhanGoc: '', nhan: ['1', ''], hai: { goc: -60, nhan: '2' }, id: 'hb', cap, label: 'Hai bán kính pha' }),
  // Dạng 4: đồ thị đọc số (A = 4 cm, T = 1,5 s, φ = π/3)
  doThiD4: (cap = 'Đọc A, T và điểm lúc t = 0 (đi lên hay đi xuống?).') => {
    const g = doThi({ A: 4, T: 1.5, phi: Math.PI / 3, tmax: 3, buoc: 0.25, nhan: 2, id: 'd4' });
    return wrap('0 0 320 210', g.b, cap, 'Đồ thị li độ – thời gian dạng 4');
  },
  // Dạng 5: hai đồng hồ lệch 0,25 s
  haiDongHo: (cap = 'Cùng lúc: An chỉ t, Bình chỉ t′.') => {
    let b = defs('hd1');
    const x0 = 30, u = 220; // 1 s = 220 đơn vị
    const truc = (y, ten, lech, c) => {
      let s = arr(x0 - 10, y, 312, y, 'hd1', c, '', 2.4) + T(x0 - 10, y - 16, ten, { c, w: 700 });
      for (let k = 0; k <= 4; k++) { const tt = k * 0.25, x = x0 + (tt + lech) * u; if (x > 300) continue; s += ln(f1(x), y - 7, f1(x), y + 7, c, 2.2) + T(f1(x), y + 28, so(tt), { a: 'middle', size: 18, c }); }
      return s;
    };
    b += truc(50, 'An: t (s)', 0, INK) + truc(130, 'Bình: t′ (s)', 0.25, BLUE);
    return wrap('0 0 320 170', b, cap, 'Hai trục thời gian lệch nhau');
  },
  // ===== Bài tương tự =====
  haiBanKinhTT: (cap = 'Hai bán kính lúc t = 0.') =>
    vongTron({ goc: 150, nhanGoc: '', nhan: ['1', ''], hai: { goc: -150, nhan: '2' }, id: 'hbt', cap, label: 'Hai bán kính pha', om: 40, oTren: true }),
  doThiTT1: (cap = 'Đồ thị x–t của vật ở bài 1.') => {
    const g = doThi({ A: 6, T: 1.2, phi: -2 * Math.PI / 3, tmax: 2, buoc: 0.2, nhan: 2, yTicks: [6, 3, -3, -6], id: 't1' });
    return wrap('0 0 320 210', g.b, cap, 'Đồ thị li độ – thời gian bài tương tự 1');
  },
  doThiTT2: (cap = 'Đồ thị x–t của vật ở bài 2.') => {
    const g = doThi({ A: 5, T: 0.8, phi: Math.PI / 2, tmax: 1.6, buoc: 0.2, nhan: 1, yTicks: [5, -5], id: 't2', fz: 18 });
    return wrap('0 0 320 210', g.b, cap, 'Đồ thị li độ – thời gian bài tương tự 2');
  },
};
