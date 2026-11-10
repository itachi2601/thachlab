// Hình minh hoạ cho ruột tập Vật lí 10 · Bài 26 Cơ năng và định luật bảo toàn cơ năng (lesson 71). Cùng quy tắc với hinh.mjs / hinh-ch4.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox (≈ 3 mm khi in rộng 46 mm), nét ≥ 2,8, phân biệt bằng NÉT/HÌNH (đặc – đứt – gạch),
// không chỉ bằng màu (in đen–trắng). Tự vẽ, không chép SGK. Độ cao trong các hình bài toán vẽ đúng tỉ lệ.
// Kiểm cỡ chữ: chụp từng hình ở cỡ in thật (xem chú thích đầu l10-bai26.mjs).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
const T24 = (x, y, s, o = {}) => T(x, y, s, { size: 24, ...o }); // hình đặt hẹp (≤40 mm): chữ 24 đơn vị để in ≥ 2,9 mm
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`; // chỉ số dưới
const ln = (x1, y1, x2, y2, o = {}) => `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${o.c ?? INK}" stroke-width="${o.w ?? SW}"${o.d ? ` stroke-dasharray="${o.d}"` : ''}${o.m ? ` marker-end="url(#${o.m})"` : ''}/>`;
const dot = (x, y, r = 6, c = INK) => `<circle cx="${x}" cy="${y}" r="${r}" fill="${c}"/>`;
const bob = (x, y, r = 11) => `<circle cx="${x}" cy="${y}" r="${r}" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
// Mũi tên kích thước hai đầu (đo độ cao)
const dim = (x, y1, y2, id) => `<line x1="${x}" y1="${y1}" x2="${x}" y2="${y2}" stroke="${INK}" stroke-width="2.2" marker-start="url(#${id}s)" marker-end="url(#${id})"/>`;
const defs2 = (id) => defs(id) + `<defs><marker id="${id}s" markerWidth="7" markerHeight="7" refX="1.5" refY="3.5" orient="auto" markerUnits="strokeWidth"><path d="M7,0 L0,3.5 L7,7 z" fill="context-stroke"/></marker></defs>`;
const gach = (id) => `<defs><pattern id="${id}" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="9" stroke="${GREY}" stroke-width="2.4"/></pattern></defs>`;

// Lòng chảo: thành trái/phải là cung elip (cao H px), đáy phẳng. Trả về path và hàm toạ độ điểm trên thành theo độ cao px.
const chao = (x0, x1, y0, H, W) => {
  // thành trái: x = x0 + W - W sin s, y = y0 - H (1 - cos s), s ∈ [0, π/2]  (y0 = đáy)
  const L = (hpx) => { const s = Math.acos(1 - hpx / H); return [x0 + W - W * Math.sin(s), y0 - hpx]; };
  const R = (hpx) => { const s = Math.acos(1 - hpx / H); return [x1 - W + W * Math.sin(s), y0 - hpx]; };
  let d = '';
  for (let i = 0; i <= 20; i++) { const [x, y] = L(H * (1 - i / 20)); d += `${i ? 'L' : 'M'}${x.toFixed(1)},${y.toFixed(1)}`; }
  for (let i = 0; i <= 20; i++) { const [x, y] = R(H * i / 20); d += `L${x.toFixed(1)},${y.toFixed(1)}`; }
  return { d: `<path d="${d}" fill="none" stroke="${INK}" stroke-width="${SW + .6}"/>`, L, R };
};

export const hinh26 = {
  // Trang 1 · Dự đoán: Lan thả mình từ mép trái lòng chảo. Không vẽ vạch ngang mức xuất phát (lộ đáp án B).
  longChao: (cap = 'Lan thả mình ở mép trái, không đạp, không nhún. Lượt đầu, Lan lên thành bên phải tới đâu?') => {
    const c = chao(20, 300, 150, 112, 80);
    let b = defs('lc') + c.d;
    const [xa, ya] = c.L(112);
    b += `<circle cx="${xa + 10}" cy="${ya - 14}" r="12" fill="${INK}"/>` + T(xa + 30, ya - 8, 'Lan');
    b += `<path d="M${xa + 22},${ya + 14} Q${xa + 40},${ya + 92} ${xa + 96},${ya + 104}" fill="none" stroke="${GREY}" stroke-width="2.4" stroke-dasharray="6 4" marker-end="url(#lc)"/>`;
    b += T(160, 140, 'đáy', { a: 'middle' });
    // ba dấu ? ở ba độ cao (thấp hơn · ngang · cao hơn mép) — không gợi sẵn đáp án
    [[c.R(56), -14], [c.R(112), -14]].forEach(([[x, y], dx]) => { b += T(x + dx, y + 10, '?', { size: 28, c: RED, w: 700, a: 'end' }); });
    b += T(c.R(112)[0] + 8, c.R(112)[1] - 26, '?', { size: 28, c: RED, w: 700, a: 'end' });
    return wrap('0 -10 320 172', b, cap, 'Lòng chảo trượt ván, Lan ở mép trái');
  },
  // Trang 2 · II.2: cột năng lượng của quả táo ở ba độ cao (tô = thế năng, gạch = động năng)
  cotTao: (cap = 'Quả táo 0,2&nbsp;kg rơi từ 5&nbsp;m, bỏ qua cản. Phần tô: thế năng; phần gạch: động năng. Cột giữa: em tự tô.') => {
    let b = gach('gt');
    const top = 30, H = 120, w = 54;
    [[22, 1, '5 m'], [124, .5, '2,5 m'], [226, 0, '0 m']].forEach(([x, k, l]) => {
      const ht = H * k;
      if (k === .5) b += `<rect x="${x}" y="${top}" width="${w}" height="${H}" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`; // cột giữa để trống cho HS tô
      else if (ht) b += `<rect x="${x}" y="${top + H - ht}" width="${w}" height="${ht}" fill="#c9d4ea" stroke="${INK}" stroke-width="${SW}"/>`;
      else b += `<rect x="${x}" y="${top}" width="${w}" height="${H}" fill="url(#gt)" stroke="${INK}" stroke-width="${SW}"/>`;
      b += T(x + w / 2, top + H + 26, `z = ${l}`, { a: 'middle' });
      b += T(x + w / 2, top - 8, '?', { a: 'middle', c: RED, w: 700 });
    });
    b += T(49, top + 66, `W${sb('t')}`, { size: 20, a: 'middle' }) + `<rect x="236" y="${top + 46}" width="34" height="28" fill="#fff"/>` + T(253, top + 66, `W${sb('đ')}`, { size: 20, a: 'middle' });
    return wrap('0 0 300 184', b, cap, 'Cột động năng và thế năng của quả táo ở ba độ cao');
  },
  // Trang 2 · II.3: con lắc qua cổng quang
  conLacCong: (cap = 'Kéo quả nặng lên độ cao h rồi thả; cổng quang ở vị trí thấp nhất đo thời gian chắn sáng.') => {
    const px = 120, py = 14, L = 140, a = 42 * Math.PI / 180;
    const xb = px + L * Math.sin(a), yb = py + L * Math.cos(a);
    let b = defs2('cq');
    b += `<rect x="${px - 40}" y="6" width="80" height="8" fill="${GREY}"/>`;
    b += ln(px, py, px, py + L, { d: '6 4', c: GREY, w: 2.2 }) + ln(px, py, xb, yb);
    b += bob(xb, yb) + bob(px, py + L, 11).replace('#fff', '#eef2fa');
    // cổng quang hình chữ U ngược quanh vị trí thấp nhất
    b += `<path d="M${px - 26},${py + L + 26} V${py + L - 22} H${px + 26} V${py + L + 26}" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
    b += T24(px, py + L + 50, 'cổng quang', { a: 'middle' });
    b += ln(xb, yb, 290, yb, { d: '4 4', c: GREY, w: 2 }) + ln(px + 30, py + L, 290, py + L, { d: '4 4', c: GREY, w: 2 });
    b += dim(278, yb + 2, py + L - 2, 'cq') + T24(262, (yb + py + L) / 2 + 8, 'h', { a: 'end', w: 700 });
    return wrap('0 0 300 212', b, cap, 'Con lắc thả từ độ cao h qua cổng quang');
  },
  // Trang 3 · II.4: có ma sát, đỉnh sau thấp hơn đỉnh trước (độ cao minh hoạ 3,0; 2,6; 2,2 m)
  dinhThapDan: (cap = 'Có ma sát và lực cản: mỗi lượt lên thấp hơn lượt trước. Phần cơ năng mất thành nhiệt.') => {
    const Y = (h) => 150 - 36 * h;
    let b = defs('dt');
    b += ln(10, 150, 310, 150, { w: 2 });
    b += `<path d="M20,${Y(3)} Q55,150 90,150 Q125,150 160,${Y(2.6)} Q195,150 230,150 Q265,150 300,${Y(2.2)}" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
    b += ln(20, Y(3), 300, Y(3), { d: '5 5', c: GREY, w: 2 });
    b += dot(20, Y(3)) + T(28, Y(3) - 10, '3,0 m') + dot(160, Y(2.6)) + T(170, Y(2.6) + 22, '2,6 m') + dot(300, Y(2.2)) + T(306, Y(2.2) - 12, '2,2 m', { a: 'end' });
    b += T(90, 124, 'nhiệt', { a: 'middle', c: RED, w: 700 }) + `<path d="M82,100 q4,-8 0,-16 q-4,-8 0,-16 M98,100 q4,-8 0,-16 q-4,-8 0,-16" fill="none" stroke="${RED}" stroke-width="2.2"/>`;
    return wrap('0 0 320 160', b, cap, 'Độ cao các đỉnh giảm dần khi có ma sát');
  },
  // Trang 4 · bài toán mẫu: A, M, B cao 3,2; 1,4; 2,8 m so với đáy O (mốc). Độ cao đúng tỉ lệ 36 px/m.
  baiMau: (cap = 'A, M, B cao 3,2; 1,4; 2,8&nbsp;m so với đáy O (mốc thế năng). Độ cao vẽ đúng tỉ lệ.') => {
    const k = 36, c = chao(20, 300, 150, 3.2 * k, 80);
    let b = c.d + ln(10, 150, 310, 150, { d: '6 4', c: GREY, w: 2 });
    const [xa, ya] = c.L(3.2 * k), [xm, ym] = c.L(1.4 * k), [xB, yB] = c.R(2.8 * k);
    b += dot(xa, ya) + T(xa + 10, ya + 4, 'A') + dot(xm, ym) + T(xm + 12, ym + 6, 'M') + dot(xB, yB) + T(xB - 12, yB + 6, 'B', { a: 'end' });
    b += dot(160, 150) + T(160, 176, 'O · mốc', { a: 'middle' });
    b += T(xa + 34, ya + 4, '3,2 m', { size: 20 }) + T(xm + 36, ym + 6, '1,4 m') + T(xB - 36, yB + 6, '2,8 m', { a: 'end' });
    return wrap('0 0 320 184', b, cap, 'Lòng chảo bài toán mẫu với các điểm A, M, B, O');
  },
  // Trang 5 · Thử thách ★★: con lắc dây 0,8 m kéo lệch 60°
  conLac60: (cap = 'Dây dài 0,8&nbsp;m, kéo lệch 60° rồi thả. Vị trí thả cao hơn chỗ thấp nhất bao nhiêu?') => {
    const px = 70, py = 16, L = 150, a = Math.PI / 3;
    const xb = px + L * Math.sin(a), yb = py + L * Math.cos(a);
    let b = defs2('c6');
    b += `<rect x="${px - 30}" y="8" width="60" height="8" fill="${GREY}"/>`;
    b += ln(px, py, px, py + L, { d: '6 4', c: GREY, w: 2.2 }) + ln(px, py, xb, yb) + bob(xb, yb) + bob(px, py + L);
    b += `<path d="M${px},${py + 40} A40,40 0 0 0 ${(px + 40 * Math.sin(a)).toFixed(1)},${(py + 40 * Math.cos(a)).toFixed(1)}" fill="none" stroke="${INK}" stroke-width="2"/>` + T24(px + 14, py + 66, '60°');
    b += T24((px + xb) / 2 + 10, (py + yb) / 2 - 6, 'l', { w: 700 });
    b += ln(xb, yb, 250, yb, { d: '4 4', c: GREY, w: 2 }) + ln(px + 14, py + L, 250, py + L, { d: '4 4', c: GREY, w: 2 });
    b += dim(236, yb + 2, py + L - 2, 'c6') + T24(244, (yb + py + L) / 2 + 8, 'h = ?', { c: RED, w: 700 });
    return wrap('0 0 310 182', b, cap, 'Con lắc đơn kéo lệch 60 độ');
  },
  // Dạng 1 · ba mốc thế năng: mặt đất, cửa sổ 6 m, mái 10 m; điểm P ở 8 m
  baMoc: (cap = 'Ba mốc: mặt đất, cửa sổ, mái. Đo z của P từ mốc đang chọn; dưới mốc thì z < 0.') => {
    const Y = (z) => 146 - 11.5 * z;
    let b = defs('bm');
    b += `<rect x="20" y="${Y(10)}" width="70" height="${Y(0) - Y(10)}" fill="#eef2fa" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<rect x="70" y="${Y(6) - 18}" width="20" height="18" fill="#fff" stroke="${INK}" stroke-width="2"/>`;
    [[0, 'mặt đất'], [6, 'cửa sổ 6 m'], [10, 'mái 10 m']].forEach(([z, l]) => { b += ln(90, Y(z), 300, Y(z), { d: '6 4', c: GREY, w: 2 }) + T24(300, Y(z) - 6, l, { a: 'end' }); });
    b += dot(124, Y(8), 7, RED) + T24(110, Y(8) + 7, 'P', { a: 'end', w: 700 }) + ln(124, Y(8) - 9, 124, Y(8) - 22, { m: 'bm' }) + T24(134, Y(8) - 12, '3 m/s');
    b += ln(10, Y(0), 310, Y(0));
    return wrap('0 0 312 152', b, cap, 'Ba mốc thế năng và điểm P');
  },
  // Dạng 2 · máng cong nhẵn: A cao 2,45 m, M cao 1,2 m, N chưa biết độ cao
  mangCong: (cap = 'Máng nhẵn, bi thả từ A. Ở N bi có 3,0&nbsp;m/s: N cao bao nhiêu?', o = {}) => {
    const { hA = '2,45 m', hM = '1,2 m' } = o;
    const k = 42, y0 = 142, X = (s) => 20 + 270 * s, Yf = (s) => y0 - 2.45 * k * (1 - s) ** 1.3;
    let d = ''; for (let i = 0; i <= 30; i++) { const s = i / 30; d += `${i ? 'L' : 'M'}${X(s).toFixed(1)},${Yf(s).toFixed(1)}`; }
    let b = `<path d="${d}" fill="none" stroke="${INK}" stroke-width="${SW + .6}"/>` + ln(10, y0, 300, y0, { w: 2 });
    const sOf = (z) => 1 - (z / 2.45) ** (1 / 1.3);
    const pt = (z, l, lab, dx = 10, dy = -8) => { const s = sOf(z); return dot(X(s), Yf(s)) + T24(X(s) + dx, Yf(s) + dy, lab, { w: 700 }) + (l ? T24(X(s) + dx + 22, Yf(s) + dy, l) : ''); };
    b += pt(2.45, hA, 'A', 4, -12) + (hM ? pt(1.2, hM, 'M') : '') + dot(X(sOf(2)), Yf(sOf(2))) + T24(X(sOf(2)) - 8, Yf(sOf(2)) + 24, 'N', { w: 700, a: 'end' }) + T24(X(sOf(2)) - 8, Yf(sOf(2)) + 48, 'z = ?', { c: RED, w: 700, a: 'end' });
    b += dot(X(1), y0) + T24(X(1) - 4, y0 - 12, 'O', { a: 'end', w: 700 });
    return wrap('0 0 310 156', b, cap, 'Máng cong nhẵn với các điểm A, M, N, O');
  },
  // Dạng 4 · ném lên từ sân thượng 3 m, lên tới 8 m so với đất
  sanThuong: (cap = 'Ném lên từ sân thượng 3,0&nbsp;m; sỏi lên tới 8,0&nbsp;m so với mặt đất rồi rơi xuống.', o = {}) => {
    const { top = '8,0 m', base = '3,0 m', ten = 'sân thượng' } = o;
    const Y = (z) => 180 - 19 * z;
    let b = defs('st') + defs2('sd');
    b += `<rect x="20" y="${Y(3)}" width="96" height="${Y(0) - Y(3)}" fill="#eef2fa" stroke="${INK}" stroke-width="${SW}"/>` + ln(8, Y(0), 304, Y(0));
    b += ln(140, Y(3) - 4, 140, Y(8) + 10, { m: 'st' }) + ln(164, Y(8) + 10, 164, Y(0) - 6, { d: '6 4', c: GREY, w: 2.4, m: 'st' });
    b += dot(140, Y(3)) + `<circle cx="152" cy="${Y(8)}" r="7" fill="#fff" stroke="${INK}" stroke-width="2.4"/>` + T24(176, Y(8) + 6, 'v = 0');
    b += ln(244, Y(8), 290, Y(8), { d: '4 4', c: GREY, w: 2 }) + ln(116, Y(3), 290, Y(3), { d: '4 4', c: GREY, w: 2 });
    b += dim(282, Y(8) + 2, Y(0) - 2, 'sd') + T24(274, Y(5.5), top, { a: 'end' });
    b += dim(106, Y(3) + 2, Y(0) - 2, 'sd') + T24(98, Y(1.2), base, { a: 'end' }); // độ cao sân thượng ghi trong khối nhà, tránh đè mũi tên rơi
    b += T24(68, Y(3) - 8, ten, { a: 'middle' });
    return wrap('0 0 310 190', b, cap, 'Ném sỏi lên từ sân thượng');
  },
  // Dạng 5 · dốc trượt tuyết A cao 10 m, chân dốc B
  docTruot: (cap = 'Xuất phát từ nghỉ ở A, tới B được 12&nbsp;m/s: cơ năng hụt đi đâu?', o = {}) => {
    const { h = '10 m', v = '12 m/s' } = o;
    let b = defs('dtr') + defs2('dd');
    b += `<path d="M20,30 L240,150 L20,150 Z" fill="#eef2fa" stroke="${INK}" stroke-width="${SW}"/>` + ln(8, 150, 304, 150);
    b += dot(36, 30, 8, INK) + T24(52, 26, 'A · v = 0', { w: 700 });
    b += dot(240, 150) + T24(240, 176, 'B · mốc', { a: 'middle', w: 700 }) + ln(248, 140, 298, 140, { m: 'dtr' }) + T24(302, 126, v, { a: 'end' });
    b += dim(8, 32, 148, 'dd') + T24(28, 106, h);
    b += T24(150, 72, 'ma sát, gió', { c: RED });
    return wrap('0 0 310 182', b, cap, 'Dốc trượt tuyết từ A xuống B');
  },
};
