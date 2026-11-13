// Hình minh hoạ cho ruột tập VL11 · Bài 3 Vận tốc, gia tốc trong dao động điều hoà (lesson 22). Cùng quy tắc hinh.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (liền – đứt – chấm), tự vẽ.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh. Xem thử: node scripts/ruot-tap/l11-bai3.mjs --hinh
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
// chữ Hi Lạp/kí hiệu toán lấy từ KaTeX_Math/KaTeX_Main (Source Sans 3 chỉ nạp latin/vietnamese)
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const km = (ch) => `<tspan font-family="KaTeX_Main">${ch}</tspan>`;
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const sp = (s) => `<tspan font-size="15" dy="-8">${s}</tspan><tspan dy="8"> </tspan>`;
const f1 = (v) => (+v).toFixed(1);
const arr = (x1, y1, x2, y2, id, c = INK, dash = '', w = SW) =>
  `<line x1="${f1(x1)}" y1="${f1(y1)}" x2="${f1(x2)}" y2="${f1(y2)}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${f1(x1)}" y1="${f1(y1)}" x2="${f1(x2)}" y2="${f1(y2)}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const dot = (x, y, r = 5, c = INK) => `<circle cx="${f1(x)}" cy="${f1(y)}" r="${r}" fill="${c}"/>`;
const hop = (x, y, s = 'đây') => `<rect x="${f1(x - 15)}" y="${f1(y - 13)}" width="30" height="26" rx="4" fill="#fff" stroke="${RED}" stroke-width="2.4"/>${T(x, y + 7, s, { a: 'middle', c: RED, w: 700 })}`;
const vs = (s) => s.replace(/\./g, ',');

// Đồ thị x–t đọc được số: lưới nét đứt mờ ở mọi vạch, số trên trục ≥ 20 đơn vị.
// o: { A, w, phi, tmax, dt (bước vạch t), xs (các vạch x), dau (in số ở vạch t thứ mấy, mặc định mọi vạch), ten ('x (cm)') }
const doThi = (o, cap, label) => {
  const { A, w, phi, tmax, dt, xs, ten = 'x (cm)', moi = 1, h = 210 } = o;
  const X0 = 46, X1 = 306, Y0 = 20, Y1 = h - 40, YM = (Y0 + Y1) / 2, Am = Math.max(...xs.map(Math.abs));
  const sx = (tt) => X0 + (tt / tmax) * (X1 - X0), sy = (x) => YM - (x / Am) * (YM - Y0 - 6);
  let b = defs('dt' + label.length);
  const n = Math.round(tmax / dt);
  for (let i = 1; i <= n; i++) b += ln(sx(i * dt), Y0, sx(i * dt), Y1, GREY, 1.4, '3 4');
  xs.forEach((x) => { if (x) b += ln(X0, sy(x), X1, sy(x), GREY, 1.4, '3 4'); });
  b += arr(X0, Y1 + 4, X0, Y0 - 12, 'dt' + label.length) + arr(X0, YM, X1 + 14, YM, 'dt' + label.length);
  b += T(X0 + 6, Y0 - 2, ten, { size: 20 }) + T(X1 + 14, Y0 - 2, 't (s)', { a: 'end', size: 20 });
  xs.forEach((x) => { b += T(X0 - 5, sy(x) + 7, vs(String(x)), { a: 'end', size: 20 }); });
  for (let i = moi; i <= n; i += moi) b += T(sx(i * dt), Y1 + 24, vs(String(+(i * dt).toFixed(2))), { a: 'middle', size: 20 });
  let d = '';
  for (let k = 0; k <= 240; k++) { const tt = (k / 240) * tmax; d += `${k ? 'L' : 'M'}${f1(sx(tt))},${f1(sy(A * Math.cos(w * tt + phi)))}`; }
  b += `<path d="${d}" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
  return wrap(`0 0 320 ${h}`, b, cap, label);
};

export const hinhL11b3 = {
  // Trang 1 · Dự đoán: ghế xích đu đưa qua lại (không đánh dấu chỗ nhanh nhất)
  xichDu: (cap = 'Ghế đưa từ điểm cao bên trái sang điểm cao bên phải rồi quay lại.') => {
    const cx = 160, cy = 14, L = 150, R = (d) => (d * Math.PI) / 180;
    const P = (g) => [cx + L * Math.sin(R(g)), cy + L * Math.cos(R(g))];
    let b = `<rect x="70" y="6" width="180" height="8" fill="${GREY}"/>`;
    b += `<path d="M${f1(P(-38)[0])},${f1(P(-38)[1])} A${L},${L} 0 0 0 ${f1(P(38)[0])},${f1(P(38)[1])}" fill="none" stroke="${GREY}" stroke-width="2.4" stroke-dasharray="6 5"/>`;
    [-38, 0, 38].forEach((g, i) => {
      const [x, y] = P(g);
      b += ln(cx, cy, x, y, i === 1 ? INK : GREY, i === 1 ? SW : 2, i === 1 ? '' : '5 4');
      b += `<rect x="${f1(x - 20)}" y="${f1(y - 4)}" width="40" height="9" rx="3" fill="#fff" stroke="${i === 1 ? INK : GREY}" stroke-width="${SW}"/>`;
    });
    b += T(P(-38)[0] - 6, P(-38)[1] + 32, 'điểm cao', { a: 'middle' }) + T(P(38)[0] + 6, P(38)[1] + 32, 'điểm cao', { a: 'middle' });
    b += T(cx, cy + L + 32, 'chỗ thấp nhất', { a: 'middle' });
    return wrap('0 0 320 206', b, cap, 'Ghế xích đu đưa qua lại');
  },
  // Trang 1 · vận tốc: trục Ox, vật đi từ +A sang −A; HS vẽ mũi tên v
  trucV: (cap = 'Vật đi từ +A sang −A. Vẽ vectơ vận tốc tại 5 điểm, dài ngắn theo tốc độ.') => {
    let b = defs('tv1');
    const xs = [40, 100, 160, 220, 280], lab = ['−A', '−A/2', 'O', 'A/2', '+A'], Y = 96;
    b += arr(20, Y, 312, Y, 'tv1') + T(312, Y + 28, 'x', { a: 'end' });
    xs.forEach((x, i) => { b += ln(x, Y - 8, x, Y + 8) + T(x, Y + 32, lab[i], { a: 'middle' }) + dot(x, Y - 26, 6, BLUE) + ln(x - 36, Y - 52, x + 36, Y - 52, GREY, 1.6, '3 4'); });
    b += arr(270, 18, 50, 18, 'tv1', BLUE, '7 5') + T(160, 12, 'chiều đi', { a: 'middle', c: BLUE });
    return wrap('0 0 320 140', b, cap, 'Trục Ox, vật đi từ biên dương sang biên âm');
  },
  // Trang 2 · đồ thị x, v, a theo t với φ = 0 (đọc mốc T/4, T/2, 3T/4)
  xva: (cap = '<span style="font-family:KaTeX_Math;font-style:italic">φ</span> = 0. Ba đồ thị chung trục t; vạch đứt ở T/4, T/2, 3T/4, T.') => {
    let b = defs('xva');
    const X0 = 66, X1 = 300, rows = [['x', 'A', 0], ['v', `A${gk('ω')}`, 1], ['a', `A${gk('ω')}${sp('2')}`, 2]], H = 74;
    const sx = (u) => X0 + u * (X1 - X0);
    rows.forEach(([n, amp, k], r) => {
      const ym = 46 + r * H, s = 26;
      b += arr(X0, ym, X1 + 12, ym, 'xva') + ln(X0, ym - s - 6, X0, ym + s + 6);
      b += T(8, ym + 7, n, { w: 700, size: 22 }) + T(X0 - 4, ym - s + 7, amp, { a: 'end', size: 19 });
      let d = '';
      const f = [(u) => Math.cos(2 * Math.PI * u), (u) => -Math.sin(2 * Math.PI * u), (u) => -Math.cos(2 * Math.PI * u)][k];
      for (let i = 0; i <= 160; i++) { const u = i / 160; d += `${i ? 'L' : 'M'}${f1(sx(u))},${f1(ym - s * f(u))}`; }
      b += `<path d="${d}" fill="none" stroke="${[INK, BLUE, RED][k]}" stroke-width="${SW}"${k === 1 ? ' stroke-dasharray="8 5"' : k === 2 ? ' stroke-dasharray="2 4"' : ''}/>`;
    });
    ['1/4', '1/2', '3/4', '1'].forEach((q, i) => { const x = sx((i + 1) / 4); b += ln(x, 14, x, 3 * H + 8, GREY, 1.6, '3 4'); });
    b += T(sx(0.25), 3 * H + 30, 'T/4', { a: 'middle', size: 19 }) + T(sx(0.5), 3 * H + 30, 'T/2', { a: 'middle', size: 19 }) + T(sx(0.75), 3 * H + 30, '3T/4', { a: 'middle', size: 19 }) + T(sx(1), 3 * H + 30, 'T', { a: 'middle', size: 19 });
    return wrap(`0 0 320 ${3 * H + 40}`, b, cap, 'Đồ thị li độ, vận tốc, gia tốc theo thời gian');
  },
  // Trang 2 · gia tốc: trục Ox, HS vẽ mũi tên a (cùng khung với trucV)
  trucA: (cap = 'Vẽ vectơ gia tốc tại −A, O, +A. Mũi nào dài nhất? Ở đâu bằng 0?') => {
    let b = defs('ta1');
    const xs = [40, 160, 280], lab = ['−A', 'O', '+A'], Y = 70;
    b += arr(20, Y, 312, Y, 'ta1') + T(312, Y + 28, 'x', { a: 'end' });
    xs.forEach((x, i) => { b += ln(x, Y - 8, x, Y + 8) + T(x, Y + 32, lab[i], { a: 'middle' }) + dot(x, Y - 24, 6, RED) + ln(x - 40, Y - 46, x + 40, Y - 46, GREY, 1.6, '3 4'); });
    return wrap('0 0 320 112', b, cap, 'Trục Ox để vẽ gia tốc');
  },
  // Trang 3 · thí nghiệm con lắc lò xo nằm ngang
  conLac: (cap = 'Kéo vật lệch 4,0 cm rồi thả; bấm giờ 10 dao động.') => {
    let b = defs('cl1');
    b += `<rect x="10" y="40" width="12" height="80" fill="${GREY}"/>` + ln(10, 120, 312, 120);
    let d = 'M22,92'; for (let i = 0; i < 10; i++) d += ` L${30 + i * 12},${i % 2 ? 80 : 104}`; d += ' L150,92 L162,92';
    b += `<path d="${d}" fill="none" stroke="${INK}" stroke-width="2.4"/>`;
    b += `<rect x="162" y="72" width="44" height="46" rx="4" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += ln(140, 28, 140, 132, GREY, 2, '5 4') + T(140, 154, 'O', { a: 'middle', w: 700 });
    b += ln(184, 28, 184, 66, RED, 2, '5 4') + arr(140, 40, 184, 40, 'cl1', RED) + T(212, 46, 'A = 4,0 cm', { c: RED });
    return wrap('0 0 320 162', b, cap, 'Con lắc lò xo nằm ngang');
  },
  // Trang 3 · hệ thức x–v: elip (để trống v tại x = A/2)
  elip: (cap = 'Mỗi điểm trên elip là một cặp (x, v). Tại x = A/2, |v| = ?') => {
    let b = defs('el1');
    const cx = 160, cy = 100, a = 120, bb = 72;
    b += arr(20, cy, 306, cy, 'el1') + arr(cx, 186, cx, 12, 'el1') + T(306, cy + 26, 'x', { a: 'end' }) + T(cx + 8, 24, 'v');
    b += `<ellipse cx="${cx}" cy="${cy}" rx="${a}" ry="${bb}" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
    b += T(cx + a + 6, cy + 24, 'A') + T(cx - a - 4, cy + 24, '−A', { a: 'end' }) + T(cx - 8, cy - bb - 8, `${gk('ω')}A`, { a: 'end' });
    const xh = cx + a / 2, yh = cy - bb * Math.sqrt(3) / 2;
    b += ln(xh, cy, xh, yh, RED, 2, '5 4') + dot(xh, yh, 6, RED) + T(xh, cy + 26, 'A/2', { a: 'middle' }) + T(xh + 10, yh - 8, '?', { c: RED, w: 700, size: 24 });
    return wrap('0 0 320 196', b, cap, 'Đồ thị v theo x là elip');
  },
  // Trang 3 · vòng tròn: mốc A/2, A√2/2, A√3/2 chiếu xuống trục x
  vongTron: (cap = 'Điểm chạy đều trên vòng tròn, bóng của nó trên trục x là vật. Một vòng mất T.') => {
    let b = defs('vt1');
    const cx = 120, cy = 150, R = 110, mk = [[0, 'O'], [30, 'A/2'], [45, ''], [60, ''], [90, 'A']];
    b += arr(cx - R - 6, cy, cx + R + 24, cy, 'vt1') + T(cx + R + 24, cy + 26, 'x', { a: 'end' });
    b += `<path d="M${cx - R},${cy} A${R},${R} 0 0 1 ${cx + R},${cy}" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
    mk.forEach(([g]) => {
      const x = cx + R * Math.sin((g * Math.PI) / 180), y = cy - R * Math.cos((g * Math.PI) / 180);
      b += ln(cx, cy, x, y, GREY, 2) + ln(x, y, x, cy, BLUE, 2, '4 4') + dot(x, y, 5, BLUE) + dot(x, cy, 5);
    });
    b += T(cx, cy + 26, 'O', { a: 'middle' }) + T(cx + R * 0.5, cy + 26, 'A/2', { a: 'middle', size: 19 }) + T(cx + R, cy + 26, 'A', { a: 'middle' });
    b += T(cx + R * Math.sin(Math.PI / 4) - 2, cy + 50, `A${km('√2')}/2`, { a: 'middle', size: 19 }) + ln(cx + R * Math.sin(Math.PI / 4), cy + 6, cx + R * Math.sin(Math.PI / 4), cy + 30, GREY, 1.4);
    b += T(cx + R * Math.sin(Math.PI / 3) + 14, cy + 74, `A${km('√3')}/2`, { a: 'middle', size: 19 }) + ln(cx + R * Math.sin(Math.PI / 3), cy + 6, cx + R * Math.sin(Math.PI / 3) + 10, cy + 54, GREY, 1.4);
    return wrap('0 0 320 236', b, cap, 'Vòng tròn và các mốc li độ');
  },
  // Trang 5 · bài toán mẫu: trục x, biên dương, điểm x = 2 cm đi chiều âm
  btm: (cap = 'A = 4 cm, <span style="font-family:KaTeX_Math;font-style:italic">ω</span> = 10 rad/s. Lúc t = 0 vật ở +4 cm. Dấu của v, a tại x = 2 cm?') => {
    let b = defs('bm1') + defs('bm2');
    const sx = (x) => 160 + x * 34, Y = 80;
    b += arr(10, Y, 314, Y, 'bm1') + T(314, Y - 10, 'x (cm)', { a: 'end', size: 19 });
    [-4, -2, 0, 2, 4].forEach((x) => { b += ln(sx(x), Y - 7, sx(x), Y + 7) + T(sx(x), Y + 30, x < 0 ? `−${-x}` : String(x), { a: 'middle' }); });
    b += dot(sx(4), Y - 20, 6) + dot(sx(2), Y - 20, 7, RED) + arr(sx(2) - 8, Y - 46, sx(2) - 58, Y - 46, 'bm2', BLUE, '7 5') + T(sx(2) - 33, Y - 56, 'chiều âm', { a: 'middle', c: BLUE, size: 19 });
    b += T(sx(4), Y - 34, 't = 0', { a: 'middle', size: 19 });
    return wrap('0 0 320 122', b, cap, 'Trục x của bài toán mẫu');
  },
  // Trang 6 · Dạng 3: đồ thị x–t A = 6 cm, T = 1,2 s, x(0) = 3 cm đi xuống
  d3: (cap = 'Đồ thị x–t, vẽ từ t = 0 đến 1,8 s.') => doThi({ A: 6, w: (2 * Math.PI) / 1.2, phi: Math.PI / 3, tmax: 1.8, dt: 0.2, xs: [6, 3, 0, -3, -6], moi: 2, h: 166 }, cap, 'Đồ thị li độ theo thời gian dạng 3'),
  // Trang 7 · Dạng 4: từ biên dương tới chỗ |v| = v_max/2
  d4: (cap = 'Lúc t = 0 vật ở +8 cm rồi đi về O.') => {
    let b = defs('d41');
    const sx = (x) => 30 + (x + 8) * 17, Y = 64;
    b += arr(10, Y, 314, Y, 'd41') + T(150, Y - 12, 'x (cm)', { a: 'middle', size: 19 });
    [-8, 0, 8].forEach((x) => { b += ln(sx(x), Y - 7, sx(x), Y + 7) + T(sx(x), Y + 30, x < 0 ? `−${-x}` : String(x), { a: 'middle' }); });
    b += dot(sx(8), Y - 18, 6) + T(sx(8), Y - 30, 't = 0', { a: 'middle', size: 19 }) + arr(sx(8) - 10, Y - 22, sx(8) - 80, Y - 22, 'd41', BLUE, '7 5');
    return wrap('0 0 320 104', b, cap, 'Trục x của dạng 4');
  },
  // Trang 8 · Bài tương tự dạng 3
  tt31: (cap = 'Bài 1: đồ thị x–t.') => doThi({ A: 4, w: (5 * Math.PI) / 6, phi: (-2 * Math.PI) / 3, tmax: 2.8, dt: 0.4, xs: [4, 2, 0, -2, -4], moi: 1, h: 196 }, cap, 'Đồ thị li độ bài tương tự dạng 3 bài 1'),
  tt32: (cap = 'Bài 2: đồ thị x–t.') => doThi({ A: 5, w: 2.5 * Math.PI, phi: Math.PI / 2, tmax: 1.2, dt: 0.1, xs: [5, 0, -5], moi: 2, h: 196 }, cap, 'Đồ thị li độ bài tương tự dạng 3 bài 2'),
};
export { sb, sp };
