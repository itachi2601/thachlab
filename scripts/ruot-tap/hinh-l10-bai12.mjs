// Hình minh hoạ cho ruột tập VL10 · Bài 12 Chuyển động ném (lesson 57). Cùng quy tắc với hinh.mjs/hinh-l10-bai23.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh. Xem thử: node scripts/ruot-tap/l10-bai12.mjs --hinh (chụp vào out/hinh-l10-bai12/).
// Quỹ đạo vẽ theo số liệu thật của đề (hàm nem), trục đứng được phóng tối đa 3 lần so với trục ngang khi quỹ đạo quá dẹt.
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
// chữ Hi Lạp: Source Sans 3 chỉ nạp latin/vietnamese, α rơi về Helvetica → lấy từ KaTeX_Math (đã nạp qua katex.min.css)
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const v0 = `v${sb('0')}`;
const f1 = (v) => (+v).toFixed(1);
const R = (d) => (d * Math.PI) / 180;
const arr = (x1, y1, x2, y2, id, c = INK, dash = '', w = SW) =>
  `<line x1="${f1(x1)}" y1="${f1(y1)}" x2="${f1(x2)}" y2="${f1(y2)}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${f1(x1)}" y1="${f1(y1)}" x2="${f1(x2)}" y2="${f1(y2)}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const cung = (x, y, r, a1, a2, c = INK) => {
  const p = (a) => `${f1(x + r * Math.cos(R(a)))},${f1(y - r * Math.sin(R(a)))}`;
  return `<path d="M${p(a1)} A${r},${r} 0 0 ${a2 > a1 ? 0 : 1} ${p(a2)}" fill="none" stroke="${c}" stroke-width="2.2"/>`;
};
const dat = (x1, x2, y) => ln(x1, y, x2, y) + Array.from({ length: Math.floor((x2 - x1) / 18) }, (_, i) =>
  ln(x1 + 8 + i * 18, y, x1 + i * 18, y + 8, GREY, 1.8)).join('');
const vat = (x, y, r = 7, fill = '#fff') => `<circle cx="${f1(x)}" cy="${f1(y)}" r="${r}" fill="${fill}" stroke="${INK}" stroke-width="${SW}"/>`;
const hop = (x, y, s = 14) => `<rect x="${f1(x - s / 2)}" y="${f1(y - s / 2)}" width="${s}" height="${s}" rx="2" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
const mayBayH = (x, y) => `<path d="M${x - 46},${y} L${x + 30},${y} Q${x + 46},${y} ${x + 46},${y + 7} Q${x + 46},${y + 14} ${x + 30},${y + 14} L${x - 40},${y + 14} L${x - 52},${y - 10} L${x - 44},${y - 10} z" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
  + `<path d="M${x - 6},${y + 6} L${x - 20},${y + 26} L${x - 8},${y + 26} L${x + 10},${y + 6}" fill="#fff" stroke="${INK}" stroke-width="2.4"/>`;
const trucThang = (x, y) => `<ellipse cx="${x}" cy="${y + 10}" rx="26" ry="14" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
  + ln(x + 24, y + 8, x + 58, y + 4) + ln(x + 58, y - 4, x + 58, y + 12, INK, 2.4) + ln(x - 34, y - 10, x + 34, y - 10, INK, 3) + ln(x, y - 10, x, y - 4, INK, 2.4)
  + ln(x - 16, y + 30, x + 16, y + 30, INK, 2.4);

// Cảnh ném theo số liệu thật: h độ cao điểm ném (m), v vận tốc ném (m/s), a góc ném (độ, 0 = ném ngang), g.
// Tuỳ chọn: lb {h, v, L, a} nhãn; vat 'da' | 'goi'; vach (vẽ vách/nhà ở điểm ném); can {x, H, ten} vật cản; comps (tách v0); vEnd (vectơ chạm đất); dinh (vạch H);
// W, Hh: viewBox; id: tiền tố marker.
const nem = (o) => {
  const { h = 0, v = 10, a = 0, g = 10, lb = {}, vach = h > 0, can = null, comps = false, vEnd = false, dinh = false, id = 'nm', W = 320, Hh = 200,
    cap = '', alt = 'Quỹ đạo vật bị ném', ml = 58, mr = 26, mt = 26, mb = 42, dau = true, cham = true, s = 0 } = o;
  const vx = v * Math.cos(R(a)), vy = v * Math.sin(R(a));
  const tb = (vy + Math.sqrt(vy * vy + 2 * g * h)) / g, L = vx * tb, ymax = h + (vy * vy) / (2 * g);
  let sx = (W - ml - mr) / L, sy = Math.min((Hh - mt - mb) / ymax, 3 * sx);
  if (a > 0) sx = sy = s || Math.min(sx, (Hh - mt - mb) / ymax);
  const X = (x) => ml + x * sx, Y = (y) => Hh - mb - y * sy;
  let b = defs(id + 'a') + defs(id + 'b') + defs(id + 'c');
  b += dat(Math.max(6, ml - 50), W - 4, Y(0));
  if (vach && h > 0) b += `<rect x="${ml - 44}" y="${f1(Y(h))}" width="44" height="${f1(Y(0) - Y(h))}" fill="#eef2fa" stroke="${INK}" stroke-width="${SW}"/>`;
  if (h > 0 && lb.h) b += ln(ml - 50, Y(h), ml - 50, Y(0), GREY, 2, '5 4') + T(ml - 40, (Y(h) + Y(0)) / 2 + 8, lb.h, { w: 700 });
  const pts = Array.from({ length: 41 }, (_, i) => { const tt = (tb * i) / 40; return `${f1(X(vx * tt))},${f1(Y(h + vy * tt - (g * tt * tt) / 2))}`; });
  b += `<polyline points="${pts.join(' ')}" fill="none" stroke="${INK}" stroke-width="2.4" stroke-dasharray="6 4"/>`;
  if (can) b += (can.tuong ? `<rect x="${f1(X(can.x) - 5)}" y="${f1(Y(can.H))}" width="10" height="${f1(Y(0) - Y(can.H))}" fill="#eef2fa" stroke="${INK}" stroke-width="2.4"/>`
      : ln(X(can.x), Y(0), X(can.x), Y(can.H) + 16, INK, 5) + `<circle cx="${f1(X(can.x))}" cy="${f1(Y(can.H) + 10)}" r="10" fill="#fff" stroke="${INK}" stroke-width="2.4"/>`)
    + (can.ten ? T(X(can.x) - 12, Y(can.H * 0.45), can.ten, { size: 20, a: 'end' }) : '');
  if (dau) b += vat(X(0), Y(h));
  // vận tốc ném (đỏ) và hai thành phần (xanh đứt)
  const k = (comps ? 80 : 52) / v, ex = X(0) + vx * k, ey = Y(h) - vy * k;
  b += arr(X(0), Y(h), ex, ey, id + 'a', RED) + (a > 0 ? T(ex - 10, ey - 4, lb.v ?? v0, { c: RED, w: 700, a: 'end' }) : T(ex - 4, ey - 10, lb.v ?? v0, { c: RED, w: 700 }));
  if (a > 0) {
    b += cung(X(0), Y(h), 26, 0, a) + T(X(0) + (h > 0 || comps ? 30 : 40), Y(h) + (h > 0 ? 22 : comps ? -8 : -5), lb.a ?? gk('α'), { size: 20 });
    if (comps) b += arr(X(0), Y(h), ex, Y(h), id + 'b', BLUE, '6 4') + arr(X(0), Y(h), X(0), ey, id + 'b', BLUE, '6 4')
      + T(ex + 8, Y(h) - 16, `v${sb('0x')}`, { c: BLUE }) + T(X(0) - 14, ey + 10, `v${sb('0y')}`, { c: BLUE, a: 'end' });
    else b += ln(X(0), Y(h), X(0) + 50, Y(h), GREY, 2, '5 4');
  }
  if (dinh) { const td = vy / g, xd = X(vx * td), yd = Y(ymax); b += ln(xd, yd, xd, Y(h), GREY, 2, '5 4') + T(xd + 6, (yd + Y(h)) / 2 + 8, dinh === true ? 'H' : dinh, { w: 700 }); }
  if (cham) b += vat(X(L), Y(0), 6, GREY);
  if (vEnd) { // vectơ vận tốc lúc chạm: mũi tên kết thúc đúng điểm chạm, góc với phương ngang (vạch xám) là α
    const vyE = vy - g * tb, dxs = vx * sx, dys = -vyE * sy, n = 60 / Math.hypot(dxs, dys), x1 = X(L) - dxs * n, y1 = Y(0) - dys * n;
    b += ln(x1, y1, x1 + 46, y1, GREY, 2, '5 4') + arr(x1, y1, X(L) - dxs * n * 0.12, Y(0) - dys * n * 0.12, id + 'c', RED)
      + T(x1 - 4, y1 - 8, 'v', { c: RED, w: 700, a: 'end' }) + T(x1 + 40, y1 + 20, gk('α'));
  }
  if (lb.L) b += arr(X(0), Y(0) + 16, X(L), Y(0) + 16, id + 'c', BLUE, '6 4', 2.2) + T(X(0) + 0.72 * (X(L) - X(0)), Y(0) + 38, lb.L, { c: BLUE, a: 'middle', w: 700 });
  return wrap(`0 0 ${W} ${Hh}`, b, cap, alt);
};

export const hinhL10b12 = {
  // Trang 1 · Dự đoán: hai gói hàng — chỉ vẽ lúc thả, không vẽ đường rơi (không lộ đáp án)
  thaGoi: (cap = 'Gói 1 rời máy bay đang bay ngang, gói 2 rời trực thăng đứng yên.') => {
    let b = defs('tg1');
    b += dat(6, 314, 140);
    b += mayBayH(84, 30) + arr(136, 36, 176, 36, 'tg1', BLUE, '6 4') + hop(80, 66) + T(98, 72, '1', { w: 700 });
    b += trucThang(240, 30) + hop(240, 66) + T(258, 72, '2', { w: 700 });
    b += T(160, 118, '?', { size: 30, a: 'middle', w: 700, c: RED });
    return wrap('0 0 320 150', b, cap, 'Hai gói hàng thả cùng lúc');
  },
  // Trang 1 · thí nghiệm hai bi — chỉ vẽ bố trí lúc bắt đầu
  haiBi: (cap = 'Lúc bắt đầu: bi 1 rời mép bàn, bi 2 được thả.') => {
    let b = defs('hb1');
    b += dat(6, 314, 150);
    b += `<rect x="10" y="60" width="120" height="10" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + ln(24, 70, 24, 150) + ln(118, 70, 118, 150);
    b += vat(124, 52) + arr(134, 52, 186, 52, 'hb1', RED) + T(150, 40, v0, { c: RED, w: 700 }) + T(104, 40, '1', { w: 700, a: 'end' });
    b += vat(146, 76) + T(160, 98, '2', { w: 700 });
    b += ln(132, 60, 214, 60, GREY, 1.6, '3 3') + ln(206, 60, 206, 150, GREY, 2, '5 4') + T(214, 112, 'h', { w: 700 });
    return wrap('0 0 320 160', b, cap, 'Bố trí thí nghiệm hai viên bi');
  },
  // Trang 2 · quỹ đạo: vị trí sau những khoảng thời gian bằng nhau
  quyDao: (cap = 'Vị trí vật sau mỗi khoảng thời gian bằng nhau. So các đoạn ngang, các đoạn rơi.') => {
    let b = defs('qd1') + defs('qd2');
    const O = [34, 30], dx = 62, ky = 8.6;
    b += arr(O[0], O[1], 312, O[1], 'qd1') + T(304, O[1] - 8, 'x', { a: 'end', w: 700 });
    b += arr(O[0], O[1], O[0], 192, 'qd1') + T(O[0] - 10, 176, 'y', { a: 'end', w: 700 }) + T(O[0] - 8, O[1] - 6, 'O', { a: 'end', w: 700 });
    const P = [0, 1, 2, 3, 4].map((k) => [O[0] + k * dx, O[1] + ky * k * k]);
    b += `<polyline points="${Array.from({ length: 41 }, (_, i) => { const k = i / 10; return `${f1(O[0] + k * dx)},${f1(O[1] + ky * k * k)}`; }).join(' ')}" fill="none" stroke="${INK}" stroke-width="2.2" stroke-dasharray="6 4"/>`;
    P.forEach(([x, y], k) => { if (k) b += ln(x, O[1], x, y, GREY, 1.6, '3 3') + ln(O[0], y, x, y, GREY, 1.6, '3 3'); });
    P.forEach(([x, y]) => { b += vat(x, y, 6); });
    return wrap('0 0 320 200', b, cap, 'Vị trí vật ném ngang theo thời gian');
  },
  // Trang 2 · vận tốc tại một điểm
  vanToc: (cap = 'Tại điểm M: v<sub>x</sub> nằm ngang, v<sub>y</sub> thẳng đứng, v là tổng hai vectơ vuông góc.') => {
    let b = defs('vt1') + defs('vt2') + defs('vt3');
    const O = [20, 30], k = 0.0042;
    b += `<polyline points="${Array.from({ length: 31 }, (_, i) => { const x = i * 10; return `${f1(O[0] + x)},${f1(O[1] + k * x * x)}`; }).join(' ')}" fill="none" stroke="${INK}" stroke-width="2.2" stroke-dasharray="6 4"/>`;
    b += vat(O[0], O[1], 6) + arr(O[0] + 6, O[1], 76, O[1], 'vt3', RED) + T(46, O[1] - 12, v0, { c: RED, w: 700 });
    const xm = 120, M = [O[0] + xm, O[1] + k * xm * xm], s = 2 * k * xm, L = 64;
    b += vat(M[0], M[1], 6) + T(M[0] + 6, M[1] - 12, 'M', { w: 700 });
    b += arr(M[0], M[1], M[0] + L, M[1], 'vt1', BLUE, '6 4') + T(M[0] + L + 4, M[1] + 6, `v${sb('x')}`, { c: BLUE, w: 700 });
    b += arr(M[0], M[1], M[0], M[1] + L * s, 'vt2', BLUE, '6 4') + T(M[0] - 8, M[1] + L * s, `v${sb('y')}`, { c: BLUE, w: 700, a: 'end' });
    b += arr(M[0], M[1], M[0] + L, M[1] + L * s, 'vt3', RED) + T(M[0] + L + 6, M[1] + L * s + 4, 'v', { c: RED, w: 700 });
    b += ln(M[0] + L, M[1], M[0] + L, M[1] + L * s, GREY, 1.6, '3 3') + cung(M[0], M[1], 30, 0, -Math.atan(s) * 180 / Math.PI) + T(M[0] + 36, M[1] + 22, gk('α'));
    return wrap('0 0 320 196', b, cap, 'Vận tốc của vật ném ngang tại điểm M');
  },
  // Trang 3 · bài toán mẫu bờ kè
  boKe: (cap = 'Hai ẩn: tầm xa L và vectơ vận tốc lúc chạm nước.') =>
    nem({ h: 20, v: 15, g: 9.8, lb: { h: 'h', L: 'L = ?' }, vEnd: true, id: 'bk', cap, alt: 'Ném ngang từ bờ kè', Hh: 180 }),
  // Trang 4 · ném xiên: tách v0
  nemXien: (cap = 'Tách v<sub>0</sub> thành hai thành phần; H tầm cao, L tầm xa.') =>
    nem({ v: 20, a: 50, lb: { L: 'L' }, comps: true, dinh: true, id: 'nx', cap, alt: 'Ném xiên từ mặt đất', ml: 54, Hh: 160, mt: 16 }),
  // Trang 4 · bài toán mẫu ném xiên: cú sút
  sutBong: (cap = 'Sút từ mặt sân: v<sub>0</sub> = 20 m/s, góc 30°.') =>
    nem({ v: 20, a: 30, lb: { L: 'L = ?', a: '30°' }, dinh: 'H = ?', id: 'sb', cap, alt: 'Cú sút bóng', ml: 30, Hh: 140, mt: 26 }),
  // Trang 5 · thử thách ★★★: thả hàng cứu trợ
  thaHang: (cap = 'Máy bay bay ngang ở 500 m, 100 m/s. Thả hàng ở đâu để trúng lá cờ?') => {
    let b = defs('th1') + defs('th2');
    b += dat(6, 314, 176);
    b += mayBayH(70, 26) + arr(122, 32, 168, 32, 'th1', BLUE, '6 4') + T(174, 38, '100 m/s', { c: BLUE, size: 20 });
    b += ln(70, 46, 70, 176, GREY, 2, '5 4') + T(78, 120, '500 m', { w: 700 });
    b += ln(276, 176, 276, 136, INK, 2.6) + `<path d="M276,136 L302,144 L276,152 z" fill="${RED}"/>`;
    b += arr(70, 194, 276, 194, 'th2', BLUE, '6 4', 2.2) + T(173, 214, '?', { a: 'middle', w: 700, c: BLUE });
    return wrap('0 0 320 220', b, cap, 'Thả hàng cứu trợ từ máy bay');
  },

  // ===== Bài tập mẫu =====
  nhaCay: (cap = '') =>
    nem({ h: 19.6, v: 7.5, g: 9.8, lb: { h: 'h', L: '15 m' }, can: { x: 10, H: 10, ten: '10 m' }, id: 'nc', cap, alt: 'Ném ngang qua ngọn cây', Hh: 150, W: 300, mt: 30 }),
  vachXien: (cap = '') =>
    nem({ h: 22.05, v: 14.7, a: 30, g: 9.8, lb: { h: 'h', L: 'L = ?', a: '30°' }, id: 'vx', cap, alt: 'Ném xiên từ vách đá', Hh: 150, W: 300, mt: 40 }),
  phao: (cap = 'Cùng v<sub>0</sub>, cùng chỗ rơi: có mấy góc nòng?') => {
    const c = { v: 14, g: 9.8, ml: 70, Hh: 150, W: 300, mt: 14, s: 11.4 }; // chung tỉ lệ để hai quỹ đạo cùng chạm tại 15 m
    const a1 = nem({ ...c, a: 24.3, id: 'p1', lb: { v: ' ', a: ' ', L: '15 m' } });
    const a2 = nem({ ...c, a: 65.7, id: 'p2', lb: { v: ' ', a: ' ' }, cham: false });
    const body = (s) => s.replace(/^[\s\S]*?<svg[^>]*>/, '').replace(/<\/svg>[\s\S]*$/, '');
    return wrap('0 0 300 150', body(a1) + body(a2).replace(/<line[^>]*stroke="#8a94ad" stroke-width="1.8"\/>/g, '') + T(62, 60, `${gk('α')}${sb('2')} = ?`, { w: 700, a: 'end' }) + T(62, 100, `${gk('α')}${sb('1')} = ?`, { w: 700, a: 'end' }), cap, 'Hai góc nòng cùng tầm xa');
  },
  // ===== Bài tương tự =====
  ttTuong: (cap = '') =>
    nem({ h: 11.25, v: 6, lb: { h: 'h', L: '9 m' }, can: { x: 6, H: 5, ten: '5 m', tuong: true }, id: 'tw', cap, alt: 'Ném ngang qua bức tường', Hh: 150, W: 300, mt: 30 }),
  ttMai: (cap = '') =>
    nem({ h: 25, v: 20, a: 30, lb: { h: 'h', L: 'L = ?', a: '30°' }, id: 'tm', cap, alt: 'Ném xiên từ mái nhà', Hh: 150, W: 300, mt: 40 }),
};
