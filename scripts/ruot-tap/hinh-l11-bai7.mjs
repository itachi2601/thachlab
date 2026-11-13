// Hình minh hoạ cho ruột tập VL11 · Bài 7 Bài tập về sự chuyển hoá năng lượng trong dao động điều hoà (lesson 26).
// Cùng quy tắc với hinh.mjs: mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt)
// chứ không chỉ bằng màu, tự vẽ. Đồ thị dùng cho đề có số đọc được (vạch + đường gióng chấm). Chú thích không lộ đáp án ô điền.
// Xem thử: node scripts/ruot-tap/l11-bai7.mjs --hinh (chụp vào out/hinh-l11-bai7/).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
// chữ Hi Lạp lấy từ KaTeX_Math (Source Sans 3 chỉ nạp latin/vietnamese → α rơi về Helvetica)
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const Wt = `W${sb('t')}`, Wd = `W${sb('đ')}`, a0 = `${gk('α')}${sb('0')}`;
const arr = (x1, y1, x2, y2, id, c = INK, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${SW}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const R = (d) => (d * Math.PI) / 180;
const f1 = (v) => (+v).toFixed(1);
const cung = (x, y, r, a1, a2, c = INK) => {
  const p = (a) => `${f1(x + r * Math.cos(R(a)))},${f1(y - r * Math.sin(R(a)))}`;
  return `<path d="M${p(a1)} A${r},${r} 0 0 ${a2 > a1 ? 0 : 1} ${p(a2)}" fill="none" stroke="${c}" stroke-width="2.2"/>`;
};
const path = (pts, c = INK, w = SW, dash = '') => `<path d="M${pts.map(([x, y]) => `${f1(x)},${f1(y)}`).join(' L')}" fill="none" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
// lò xo ziczac nằm ngang từ x1 tới x2 ở độ cao y
const loxo = (x1, x2, y, n = 9, a = 9) => path([[x1, y], ...Array.from({ length: n }, (_, i) => [x1 + ((i + 0.5) * (x2 - x1)) / n, y + (i % 2 ? a : -a)]), [x2, y]], INK, 2.4);
const loxoDung = (y1, y2, x, n = 9, a = 9) => path([[x, y1], ...Array.from({ length: n }, (_, i) => [x + (i % 2 ? a : -a), y1 + ((i + 0.5) * (y2 - y1)) / n]), [x, y2]], INK, 2.4);
const tuong = (x, y1, y2) => ln(x, y1, x, y2) + Array.from({ length: Math.floor((y2 - y1) / 14) }, (_, i) => ln(x, y1 + 6 + i * 14, x - 9, y1 + 15 + i * 14, GREY, 1.8)).join('');
const tran = (x1, x2, y) => ln(x1, y, x2, y) + Array.from({ length: Math.floor((x2 - x1) / 14) }, (_, i) => ln(x1 + 6 + i * 14, y, x1 + 15 + i * 14, y - 9, GREY, 1.8)).join('');

// Đồ thị năng lượng theo li độ x: Wt parabol đáy ở O, Wđ parabol úp, W ngang (nét chấm gạch).
// xt: [[x/A, nhãn]] vạch trục x; yt: [[E/W, nhãn]] vạch trục năng lượng; ve: 'both' | 'd' (chỉ Wđ) | 't'.
const doThiX = ({ xt = [[-1, '−A'], [0, 'O'], [1, 'A']], xu = 'x', yt = [[1, 'W']], yu = '', ve: v = 'both', id = 'dx', cap = '' } = {}) => {
  const ox = 170, oy = 172, ax = 118, H = 128;
  const X = (u) => ox + u * ax, Y = (e) => oy - e * H;
  let b = defs(id);
  b += arr(30, oy, 312, oy, id) + arr(ox, oy + 6, ox, 18, id) + T(312, oy - 8, xu, { a: 'end' }) + T(ox + 8, 26, yu ? `E (${yu})` : 'E');
  yt.forEach(([e, s]) => { b += ln(X(-1.05), Y(e), X(1.05), Y(e), GREY, 1.6, '2 4') + T(ox - 8, Y(e) - 6, s, { a: 'end' }); });
  xt.forEach(([u, s]) => { if (u) b += ln(X(u), oy, X(u), Y(1), GREY, 1.6, '2 4'); b += ln(X(u), oy - 5, X(u), oy + 5, INK, 2) + T(X(u) + (u ? 0 : -10), oy + 24, s, { a: 'middle' }); });
  const N = 40, us = Array.from({ length: N + 1 }, (_, i) => -1 + (2 * i) / N);
  b += path([[X(-1.05), Y(1)], [X(1.05), Y(1)]], GREY, 2.4, '10 4 2 4');
  if (v !== 'd') b += path(us.map((u) => [X(u), Y(u * u)]), INK) + T(X(1) + 6, Y(0.86), Wt);
  if (v !== 't') b += path(us.map((u) => [X(u), Y(1 - u * u)]), RED, SW, '7 4') + T(X(-0.45), Y(1) - 8, Wd, { a: 'middle', c: RED });
  return wrap('0 0 320 200', b, cap, 'Đồ thị năng lượng theo li độ');
};

// Đồ thị năng lượng theo thời gian. tMax: t lớn nhất trên trục; Te: chu kì của năng lượng (= T/2); dau: 'bien' (Wt cực đại lúc t = 0) | 'vtcb'.
// xt: [[t, nhãn]] (cùng đơn vị với tMax); yt: [[E/W, nhãn]]; ve: 'both' | 'd'; li: vẽ thêm li độ x(t) ở trên (hình lý thuyết).
const doThiT = ({ tMax = 1, Te = 0.5, dau = 'bien', xt = [], tu = 't', yt = [[1, 'W']], yu = '', ve: v = 'both', li = false, id = 'dt', cap = '' } = {}) => {
  const ox = 46, x1 = 300, oy = li ? 266 : 172, H = 118;
  const X = (s) => ox + (s / tMax) * (x1 - ox), Y = (e) => oy - e * H;
  const Wtf = (s) => { const c = Math.cos((2 * Math.PI * s) / (2 * Te)); return dau === 'bien' ? c * c : 1 - c * c; };
  let b = defs(id);
  if (li) { // li độ x(t), chu kì 2Te, ở dải trên
    const my = 62, Ax = 40;
    b += arr(ox, my, 312, my, id) + arr(ox, my + Ax + 6, ox, my - Ax - 12, id) + T(30, my - Ax + 2, 'x', { a: 'end' }) + T(312, my + 22, tu, { a: 'end' });
    b += path(Array.from({ length: 121 }, (_, i) => { const s = (tMax * i) / 120; return [X(s), my - Ax * (dau === 'bien' ? Math.cos((Math.PI * s) / Te) : Math.sin((Math.PI * s) / Te))]; }), BLUE, SW);
  }
  b += arr(ox, oy, 312, oy, id) + arr(ox, oy + 6, ox, Y(1) - 34, id) + T(312, oy - 8, tu, { a: 'end' }) + T(ox + 10, Y(1) - 24, yu ? `E (${yu})` : 'E');
  yt.forEach(([e, s]) => { b += ln(ox, Y(e), x1, Y(e), GREY, 1.6, '2 4') + T(ox - 6, Y(e) + 7, s, { a: 'end' }); });
  xt.forEach(([s, lab]) => { b += ln(X(s), oy, X(s), Y(1), GREY, 1.6, '2 4') + ln(X(s), oy - 5, X(s), oy + 5, INK, 2) + T(X(s), oy + 24, lab, { a: 'middle' }); });
  b += T(ox - 6, oy + 22, 'O', { a: 'end' });
  const N = 160, ss = Array.from({ length: N + 1 }, (_, i) => (tMax * i) / N);
  if (v !== 'd') b += path(ss.map((s) => [X(s), Y(Wtf(s))]), INK);
  b += path(ss.map((s) => [X(s), Y(1 - Wtf(s))]), RED, SW, '7 4');
  // nhãn đường: đặt ở nơi đường ấy cao nhất trong khoảng đầu
  const sT = dau === 'bien' ? 0 : Te / 2, sD = dau === 'bien' ? Te / 2 : 0;
  if (v !== 'd') b += T(X(sT) + 6, Y(1) - 6, Wt);
  b += T(X(sD) + (sD ? 6 : 10), Y(1) - 6, Wd, { c: RED });
  return wrap(`0 0 320 ${oy + 30}`, b, cap, 'Đồ thị năng lượng theo thời gian');
};

// Con lắc đơn: điểm treo, dây lệch góc, vạch thẳng đứng, độ cao h của vật so với đáy.
const conLac = ({ goc = 38, gocL = a0, hL = 'h', lL = 'l', phu = null, id = 'cl', cap = '' } = {}) => {
  const px = 150, py = 24, L = 150, bx = px + L * Math.sin(R(goc)), by = py + L * Math.cos(R(goc)), dy = py + L;
  let b = defs(id) + tran(px - 60, px + 60, py);
  b += ln(px, py, px, dy + 14, GREY, 2, '6 4') + ln(px, py, f1(bx), f1(by));
  b += cung(px, py, 48, -90, -90 + goc) + T(px + 14, py + 74, gocL);
  b += T((px + bx) / 2 + 10, (py + by) / 2 - 6, lL);
  if (phu != null) { const qx = px + L * Math.sin(R(phu)), qy = py + L * Math.cos(R(phu)); b += ln(px, py, f1(qx), f1(qy), GREY, 2, '3 4') + `<circle cx="${f1(qx)}" cy="${f1(qy)}" r="10" fill="#fff" stroke="${GREY}" stroke-width="2.2" stroke-dasharray="3 3"/>`; }
  b += `<circle cx="${f1(bx)}" cy="${f1(by)}" r="12" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
  b += `<circle cx="${px}" cy="${dy}" r="12" fill="none" stroke="${GREY}" stroke-width="2" stroke-dasharray="4 3"/>`;
  b += ln(px - 30, dy + 12, f1(bx + 30), dy + 12, GREY, 1.8, '2 4') + ln(f1(bx - 14), f1(by + 12), f1(bx + 46), f1(by + 12), GREY, 1.8, '2 4');
  b += ln(f1(bx + 38), f1(by + 12), f1(bx + 38), dy + 12, INK, 2.2) + T(bx + 46, (by + dy) / 2 + 20, hL);
  b += T(px - 16, dy + 36, 'mốc thế năng (đáy)', { a: 'middle', size: 20 });
  return wrap(`0 0 320 ${dy + 44}`, b, cap, 'Con lắc đơn lệch khỏi phương thẳng đứng');
};

// Lò xo nằm ngang + trục li độ (−A, O, x, A); vật ở li độ u (theo A).
const loXo = ({ u = 0.55, nhan = [[-1, '−A'], [0, 'O'], [0.55, 'x'], [1, 'A']], cap = '', id = 'lx' } = {}) => {
  const ox = 170, ax = 118, X = (s) => ox + s * ax, y = 66, w = 40;
  let b = defs(id) + tuong(18, 30, 110) + ln(18, 108, 314, 108);
  b += loxo(18, X(u) - w / 2, y + 16) + `<rect x="${f1(X(u) - w / 2)}" y="${y - 4}" width="${w}" height="40" rx="3" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
  b += arr(30, 150, 312, 150, id) + T(312, 140, 'x', { a: 'end' });
  nhan.forEach(([s, lab]) => { b += ln(X(s), 145, X(s), 155, INK, 2) + ln(X(s), 112, X(s), 145, GREY, 1.6, '2 4') + T(X(s), 176, lab, { a: 'middle' }); });
  return wrap('0 0 320 186', b, cap, 'Con lắc lò xo nằm ngang và trục li độ');
};

export const hinhL11b7 = {
  // Trang 1 · Dự đoán: xích đu lệch α0 và 2α0 (chú thích chỉ mô tả, không nêu tỉ lệ năng lượng)
  xichDu: (cap = 'Cùng xích đu, lần 2 góc lệch lớn nhất gấp đôi lần 1.') => {
    let b = tran(8, 312, 18);
    const one = (px, goc, lab, ten) => {
      const L = 132, bx = px + L * Math.sin(R(goc)), by = 18 + L * Math.cos(R(goc));
      return ln(px, 18, px, 166, GREY, 2, '6 4') + ln(px, 18, f1(bx), f1(by)) + ln(px - 12, 18, f1(bx - 12), f1(by), INK, 2)
        + `<rect x="${f1(bx - 24)}" y="${f1(by)}" width="34" height="8" rx="2" fill="${GREY}" stroke="${INK}" stroke-width="2"/>`
        + cung(px, 18, 62, -90, -90 + goc) + T(px + 4, 104, lab) + T(px + 30, 192, ten, { a: 'middle', w: 700 });
    };
    b += one(70, 12, a0, 'Lần 1') + one(220, 24, `2${a0}`, 'Lần 2');
    return wrap('0 0 320 200', b, cap, 'Hai lần đẩy xích đu');
  },
  // Trang 1 · Họ 1: thế năng dùng li độ x, không dùng A
  loXo: (cap = 'Lò xo nằm ngang, mốc thế năng ở VTCB O.') => loXo({ cap }),
  // Trang 2 · thí nghiệm: lò xo treo, kéo xuống A rồi thả
  loXoTreo: (cap = 'Treo vật 250 g, lò xo dãn 5,0 cm; kéo xuống thêm A (A &lt; 5 cm) rồi thả.') => {
    let b = defs('lt') + tran(60, 200, 20);
    b += loxoDung(20, 120, 130, 11, 11) + `<rect x="108" y="120" width="44" height="38" rx="3" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += ln(156, 139, 250, 139, GREY, 1.8, '2 4') + T(256, 145, 'VTCB');
    b += ln(156, 180, 250, 180, GREY, 1.8, '2 4') + `<rect x="108" y="161" width="44" height="38" rx="3" fill="none" stroke="${GREY}" stroke-width="2" stroke-dasharray="4 3"/>`;
    b += ln(232, 139, 232, 180, INK, 2.2) + T(240, 172, 'A');
    b += arr(80, 150, 80, 196, 'lt', BLUE, '6 4') + T(60, 214, 'kéo', { a: 'middle', c: BLUE });
    return wrap('0 0 320 222', b, cap, 'Con lắc lò xo treo thẳng đứng');
  },
  // Trang 2 · Họ 2: cơ năng chia thành phần bằng nhau
  phanN: (cap = 'Ví dụ W<sub>đ</sub> = 3W<sub>t</sub>: mỗi ô bằng W<sub>t</sub>; đếm số ô của cả W.') => {
    let b = '';
    const x0 = 20, w = 70, y = 56, h = 46;
    for (let i = 0; i < 4; i++) {
      const dong = i < 3;
      b += `<rect x="${x0 + i * w}" y="${y}" width="${w}" height="${h}" fill="${dong ? '#fbeceb' : '#fff'}" stroke="${dong ? RED : INK}" stroke-width="${SW}"${dong ? ' stroke-dasharray="7 4"' : ''}/>`;
      b += T(x0 + i * w + w / 2, y + 30, dong ? Wd : Wt, { a: 'middle', c: dong ? RED : INK });
    }
    b += path([[x0, 40], [x0, 30], [x0 + 4 * w, 30], [x0 + 4 * w, 40]], INK, 2.2) + T(160, 22, 'W', { a: 'middle', w: 700 });
    b += path([[x0, 118], [x0, 128], [x0 + 3 * w, 128], [x0 + 3 * w, 118]], RED, 2.2) + T(x0 + 1.5 * w, 152, 'n = 3 phần động', { a: 'middle', c: RED });
    b += T(x0 + 3.5 * w, 152, '1 phần thế', { a: 'middle' });
    return wrap('0 0 320 162', b, cap, 'Cơ năng chia thành các phần bằng nhau');
  },
  // Trang 2 · Họ 3: đồ thị theo li độ (không số)
  doThiXLT: (cap = 'Năng lượng theo li độ x. Hai đường cắt nhau tại x = ?') => doThiX({ id: 'dxl', cap }),
  // Trang 3 · Họ 3: li độ và năng lượng theo thời gian, gốc thời gian ở biên
  doThiTLT: (cap = 'Trên: li độ x(t). Dưới: W<sub>t</sub> (liền) và W<sub>đ</sub> (đứt). Đếm số đỉnh W<sub>t</sub> trong một chu kì của x.') =>
    doThiT({ tMax: 1, Te: 0.5, li: true, yt: [[1, 'W'], [0.5, '']], id: 'dtl', cap }),
  // Trang 3 · Họ 4: con lắc đơn, mốc ở đáy
  conLac: (cap = 'Mốc thế năng ở đáy. Độ cao h của vật tính theo l và góc lệch.') => conLac({ cap, id: 'cl1' }),
  // Trang 3 · Bẫy 3: radian
  radian: (cap = 'Cung dài đúng bằng bán kính r thì góc ở tâm là 1&nbsp;rad.') => {
    const cx = 60, cy = 150, r = 120, a = 180 / Math.PI;
    let b = ln(cx, cy, cx + r, cy) + ln(cx, cy, f1(cx + r * Math.cos(R(a))), f1(cy - r * Math.sin(R(a))));
    b += cung(cx, cy, r, 0, a, RED).replace('stroke-width="2.2"', `stroke-width="${SW}" stroke-dasharray="7 4"`) + cung(cx, cy, 30, 0, a);
    b += T(cx + 36, cy - 14, '1 rad') + T(cx + r / 2, cy + 24, 'r', { a: 'middle' }) + T(cx + 86, cy - 92, 'cung = r', { c: RED });
    b += T(cx + 14, cy - 62, 'r');
    return wrap('0 0 260 182', b, cap, 'Góc một radian');
  },
  // Trang 4 · bài toán mẫu: lò xo nằm ngang kéo 4 cm
  loXoMau: (cap = 'm = 100 g, k = 100 N/m, kéo 4 cm rồi thả nhẹ. Tìm vị trí W<sub>đ</sub> = 3W<sub>t</sub>.') =>
    loXo({ u: 1, nhan: [[-1, '−4'], [0, '0'], [1, '4 cm']], cap, id: 'lxm' }),
  // Trang 5 · thử thách ⭐⭐: thả từ 60°, xét khi dây lệch 30°
  conLacTT: (cap = 'Thả từ 60°; xét lúc dây lệch 30° (vòng chấm).') => conLac({ goc: 50, gocL: '60°', hL: '', lL: '1,0 m', phu: 25, id: 'cl2', cap }),

  // ---- Bài tập mẫu ----
  // Dạng 3: A = 6 cm, W = 36 mJ (đọc được), không ghi 9 mJ hay 27 mJ (đáp án)
  d3: () => doThiX({ xt: [[-1, '−6'], [-0.5, '−3'], [0, '0'], [0.5, '3'], [1, '6']], xu: 'x (cm)', yt: [[1, '36']], yu: 'mJ', id: 'd3', cap: 'Liền W<sub>t</sub> · đứt W<sub>đ</sub> · chấm gạch W.' }),
  // Dạng 5: W = 90 mJ (không ghi), cắt nhau ở 45 mJ tại 0,05 s và 0,15 s; gốc ở biên
  d5: () => doThiT({ tMax: 0.25, Te: 0.2, xt: [[0.05, '0,05'], [0.15, '0,15']], tu: 't (s)', yt: [[0.5, '45']], yu: 'mJ', id: 'd5', cap: 'Liền W<sub>t</sub> · đứt W<sub>đ</sub>; gốc ở biên.' }),
  // Con lắc đơn dạng 4 (60°)
  d4: () => conLac({ goc: 50, gocL: '60°', hL: 'h<tspan font-size="15" dy="5">0</tspan>', lL: '0,9 m', phu: 25, id: 'cl3', cap: 'Hình không theo tỉ lệ. h<sub>0</sub>: độ cao của vật ở biên so với đáy; vòng chấm: lúc dây lệch 30°.' }),

  // ---- Bài tương tự ----
  tt3a: () => doThiX({ xt: [[-1, '−5'], [0, '0'], [0.8, '4'], [1, '5']], xu: 'x (cm)', yt: [[1, '50']], yu: 'mJ', id: 't3a', cap: '' }),
  tt3b: () => doThiX({ xt: [[-1, '−4'], [-0.5, '−2'], [0, '0'], [0.5, '2'], [1, '4']], xu: 'x (cm)', yt: [[1, '80'], [0.5, '40']], yu: 'mJ', ve: 'd', id: 't3b', cap: '' }),
  tt5a: () => doThiT({ tMax: 0.125, Te: 0.1, xt: [[0.025, '0,025'], [0.075, '0,075']], tu: 't (s)', yt: [[0.5, '10']], yu: 'mJ', id: 't5a', cap: 'Liền W<sub>t</sub>, đứt W<sub>đ</sub>; gốc ở biên.' }),
  tt5b: () => doThiT({ tMax: 0.45, Te: 0.2, dau: 'vtcb', ve: 'd', xt: [[0.1, '0,1'], [0.2, '0,2'], [0.3, '0,3'], [0.4, '0,4']], tu: 't (s)', yt: [[1, '60']], yu: 'mJ', id: 't5b', cap: 'Động năng W<sub>đ</sub> theo t; gốc lúc qua VTCB.' }),
};
