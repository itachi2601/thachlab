// Hình minh hoạ cho ruột tập VL10 · Bài 18 Lực ma sát (lesson 63). Cùng quy tắc với hinh.mjs/hinh-l10-bai23.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh (hình Dự đoán KHÔNG vẽ mũi tên ma sát).
// Ảnh thật duy nhất: gai lốp xe (book/assets/anh-that/gai-lop-xe.jpg, Ken T1381 · Wikimedia Commons · CC BY-SA 3.0, khai trong anh_that của hồ sơ sách).
// Xem thử: node scripts/ruot-tap/l10-bai18.mjs --hinh (chụp vào out/hinh-l10-bai18/).
import { existsSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const HERE = dirname(fileURLToPath(import.meta.url));
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
// chữ Hi Lạp lấy từ KaTeX_Math (Source Sans 3 chỉ nạp latin/vietnamese → α rơi về Helvetica)
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const arr = (x1, y1, x2, y2, id, c = INK, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${SW}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const R = (d) => (d * Math.PI) / 180;
const f1 = (v) => (+v).toFixed(1);
const cung = (x, y, r, a1, a2, c = INK) => {
  const p = (a) => `${f1(x + r * Math.cos(R(a)))},${f1(y - r * Math.sin(R(a)))}`;
  return `<path d="M${p(a1)} A${r},${r} 0 0 0 ${p(a2)}" fill="none" stroke="${c}" stroke-width="2.2"/>`;
};
const dat = (x1, x2, y) => ln(x1, y, x2, y) + Array.from({ length: Math.floor((x2 - x1) / 18) }, (_, i) =>
  ln(x1 + 8 + i * 18, y, x1 + i * 18, y + 8, GREY, 1.8)).join('');
const nguoiDay = (x, y) => `<circle cx="${x}" cy="${y}" r="11" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
  + ln(x + 2, y + 11, x + 12, y + 62) + ln(x + 12, y + 62, x - 10, y + 104) + ln(x + 12, y + 62, x + 24, y + 104)
  + ln(x + 6, y + 30, x + 40, y + 40);

// Vật trên mặt dốc: góc goc, lực P (đỏ), thành phần Px, Py (xám đứt), N, Fms (đứt) theo chiều chuyển động, mũi tên chiều đi (xanh đứt)
const doc = (o = {}) => {
  const { goc = 30, nhanGoc = `${gk('α')}`, h = false, P = true, tach = false, N = true, ms = true, chieu = 'xuong', v0 = '', truc = false, nhanL = '', cap = '', id = 'dc' } = o;
  const x0 = 20, y0 = 186, L = 270, c = Math.cos(R(goc)), sn = Math.sin(R(goc));
  const x1 = x0 + L * c, y1 = y0 - L * sn;
  let b = defs(id + 'a') + defs(id + 'b') + defs(id + 'c') + defs(id + 'd');
  b += `<path d="M${x0},${y0} L${f1(x1)},${f1(y1)} L${f1(x1)},${y0} z" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
  b += cung(x0, y0, 46, 0, goc) + T(x0 + 54, y0 - 6, nhanGoc);
  if (nhanL) b += T(x0 + L * 0.96 * c - 26 * sn, y0 - L * 0.96 * sn - 26 * c, nhanL, { a: 'end' }); // phía trên mặt dốc, không đè nét
  if (h) b += ln(f1(x1 + 12), f1(y1), f1(x1 + 12), y0, GREY, 2, '5 4') + T(x1 + 20, (y1 + y0) / 2 + 8, 'h');
  const u = 0.5, bx = x0 + L * u * c, by = y0 - L * u * sn, w = 46, hh = 30;
  b += `<g transform="rotate(${-goc} ${f1(bx)} ${f1(by)})"><rect x="${f1(bx - w / 2)}" y="${f1(by - hh)}" width="${w}" height="${hh}" rx="3" fill="#fff" stroke="${INK}" stroke-width="${SW}"/></g>`;
  const cx = bx - (hh / 2) * sn, cy = by - (hh / 2) * c;
  const LP = 70;
  if (P) b += arr(f1(cx), f1(cy), f1(cx), f1(cy + LP), id + 'a', RED) + T(cx + 7, cy + LP - 2, 'P', { c: RED, w: 700 });
  if (tach) {
    const lx = LP * sn, ly = LP * c; // Px dọc dốc xuống, Py vuông góc vào dốc
    b += arr(f1(cx), f1(cy), f1(cx - lx * c), f1(cy + lx * sn), id + 'd', GREY, '6 4') + T(cx - lx * c - 8, cy + lx * sn + 20, `P${sb('x')}`, { a: 'end', c: INK });
    b += arr(f1(cx), f1(cy), f1(cx + ly * sn), f1(cy + ly * c), id + 'd', GREY, '6 4') + T(cx + ly * sn + 6, cy + ly * c + 6, `P${sb('y')}`);
  }
  if (N) b += arr(f1(cx), f1(cy), f1(cx - 58 * sn), f1(cy - 58 * c), id + 'b', INK) + T(cx - 58 * sn - 8, cy - 58 * c, 'N', { w: 700, a: 'end' });
  if (ms) { // ma sát ngược chiều đi; đi xuống hoặc sắp trượt xuống (chieu rỗng): hướng lên dốc
    const dir = chieu === 'len' ? -1 : 1, ex = cx + dir * 24 * c, ey = cy - dir * 24 * sn - 6;
    b += arr(f1(ex), f1(ey), f1(ex + dir * 52 * c), f1(ey - dir * 52 * sn), id + 'c', INK, '6 4')
      + T(ex + dir * 52 * c + (dir > 0 ? -6 : -4), ey - dir * 52 * sn - 12, `F${sb('ms')}`, { a: 'end' });
  }
  if (truc) { // trục Ox dọc dốc hướng xuống, vẽ trong tam giác để không đè cung góc
    const P = (u) => [x0 + L * u * c + 28 * sn, y0 - L * u * sn + 28 * c];
    const [ax, ay] = P(0.78), [bx2, by2] = P(0.58);
    b += arr(f1(ax), f1(ay), f1(bx2), f1(by2), id + 'b', INK) + T(ax + 4, ay + 22, 'x', { w: 700 });
  }
  if (v0 || chieu) { // chiều chuyển động, phía trên mặt dốc
    const ox = -16 * sn - 0, oy = -16 * c - 52, a0 = chieu === 'len' ? 0.16 : 0.36, a1 = chieu === 'len' ? 0.36 : 0.16;
    const xa = x0 + L * a1 * c + ox, ya = y0 - L * a1 * sn + oy;
    b += arr(f1(x0 + L * a0 * c + ox), f1(y0 - L * a0 * sn + oy), f1(xa), f1(ya), id + 'c', BLUE, '6 4');
    if (v0) b += T(xa - 4, ya - 10, v0, { c: BLUE, a: chieu === 'len' ? 'end' : 'start' });
  }
  return wrap('0 0 320 200', b, cap, 'Vật trên mặt phẳng nghiêng');
};

// Thùng trên sàn ngang, lực kéo chếch lên (hoặc đẩy chếch xuống) góc goc; tuỳ chọn tách F thành hai thành phần
const keoCheo = (o = {}) => {
  const { F = 'F', goc = `${gk('α')}`, tach = true, ms = true, gon = false, cap = '', id = 'kc' } = o;
  let b = defs(id + 'a') + defs(id + 'b') + defs(id + 'c') + defs(id + 'd');
  b += dat(8, 314, 128);
  b += `<rect x="96" y="86" width="104" height="42" rx="4" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
  const ox = 148, oy = 107, L = 104, ex = ox + L * Math.cos(R(30)), ey = oy - L * Math.sin(R(30));
  b += arr(ox, oy, f1(ex), f1(ey), id + 'a', RED) + T(ex + 4, ey - 4, F, { c: RED, w: 700 });
  b += ln(ox, oy, ox + 112, oy, GREY, 2, '5 4') + cung(ox, oy, 40, 0, 30) + T(ox + 46, oy - 6, goc);
  if (tach) {
    b += arr(ox, oy, f1(ex), oy, id + 'd', GREY, '6 4');
    b += ln(f1(ex), oy, f1(ex), f1(ey), GREY, 2, '3 4');
    b += arr(ox, oy, ox, f1(ey), id + 'd', GREY, '6 4') + T(ox + 6, ey + 4, `F${sb('y')}`);
    b += T(ex + 6, oy + 4, `F${sb('x')}`);
  }
  if (gon) return wrap('0 36 320 104', b, cap, 'Thùng kéo bằng dây chếch lên'); // bản gọn: chỉ lực kéo và góc (ô giải Dạng 3)
  b += arr(ox, oy, ox, 164, id + 'b', RED) + T(ox - 8, 162, 'P', { c: RED, w: 700, a: 'end' });
  b += arr(116, 86, 116, 26, id + 'c', INK) + T(108, 34, 'N', { w: 700, a: 'end' });
  if (ms) b += arr(96, 118, 36, 118, id + 'c', INK, '6 4') + T(10, 110, `F${sb('ms')}`);
  return wrap('0 0 320 172', b, cap, 'Thùng kéo chếch lên trên sàn ngang');
};

export const hinhL10b18 = {
  // Trang 1 · Dự đoán: An đẩy thùng nước, KHÔNG vẽ ma sát (để không lộ đáp án)
  anDay: (cap = 'An đẩy ngang 50 N, thùng chưa nhúc nhích.') => {
    let b = defs('ad1');
    b += dat(6, 314, 160);
    b += nguoiDay(70, 52) + T(60, 34, 'An', { a: 'middle', w: 700 });
    b += `<rect x="118" y="86" width="96" height="74" rx="5" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
      + ln(130, 100, 202, 100, GREY, 2) + T(166, 134, 'nước', { a: 'middle', c: GREY });
    b += arr(214, 123, 300, 123, 'ad1', RED) + T(258, 112, '50 N', { c: RED, a: 'middle', w: 700 });
    b += T(258, 150, '?', { size: 26, a: 'middle', w: 700 });
    return wrap('0 0 320 172', b, cap, 'An đẩy thùng nước khoáng');
  },
  // Trang 1 · II.1: ma sát theo lực kéo (số đo hộp 0,60 kg ở bài web), các đoạn đánh chữ O, A, B, C
  doThi: (cap = 'Kéo hộp gỗ, tăng dần lực kéo. Trục đứng: lực ma sát.') => {
    let b = defs('dt1');
    const X = (v) => 46 + v * 80, Y = (v) => 176 - v * 66; // v: N
    b += arr(46, 176, 312, 176, 'dt1', INK) + arr(46, 176, 46, 14, 'dt1', INK);
    b += T(312, 166, `F${sb('kéo')}`, { a: 'end', w: 700 }) + T(54, 24, `F${sb('ms')}`, { w: 700 });
    [1, 2, 3].forEach((k) => { b += ln(X(k), 176, X(k), 182, INK, 2) + T(X(k), 200, `${k}`, { a: 'middle' }); });
    [1, 2].forEach((k) => { b += ln(40, Y(k), 46, Y(k), INK, 2) + T(34, Y(k) + 7, `${k}`, { a: 'end' }); });
    b += ln(46, Y(2.1), X(2.1), Y(2.1), GREY, 1.8, '4 4') + ln(46, Y(1.7), X(3.2), Y(1.7), GREY, 1.8, '4 4');
    b += `<path d="M${X(0)},${Y(0)} L${f1(X(2.1))},${f1(Y(2.1))} L${f1(X(2.25))},${f1(Y(1.7))} L${f1(X(3.2))},${f1(Y(1.7))}" fill="none" stroke="${INK}" stroke-width="3.4"/>`;
    b += T(52, 170, 'O', { w: 700 }) + T(X(2.1) - 6, Y(2.1) - 8, 'A', { w: 700, a: 'end' }) + T(X(2.25) + 4, Y(1.7) - 8, 'B', { w: 700 }) + T(X(3.2), Y(1.7) - 8, 'C', { w: 700, a: 'end' });
    return wrap('0 0 320 210', b, cap, 'Đồ thị lực ma sát theo lực kéo');
  },
  // Trang 2 · II.4 kéo chếch
  keoCheo: (cap = 'Tách F thành F<sub>x</sub> (ngang) và F<sub>y</sub> (đứng). Thành phần nào đỡ bớt thùng?') => keoCheo({ cap }),
  // Trang 2 · thí nghiệm hộp trên hai bút chì
  butChi: (cap = 'Kê hộp lên hai bút chì tròn rồi kéo.') => {
    let b = defs('bc1');
    b += dat(6, 314, 120);
    b += `<rect x="70" y="60" width="130" height="44" rx="4" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<circle cx="100" cy="112" r="8" fill="#fff" stroke="${INK}" stroke-width="${SW}"/><circle cx="170" cy="112" r="8" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += ln(200, 82, 236, 82) + `<rect x="236" y="72" width="62" height="20" rx="3" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + arr(298, 82, 316, 82, 'bc1', RED);
    b += T(267, 58, 'lực kế', { a: 'middle' });
    return wrap('0 0 320 132', b, cap, 'Hộp kê trên hai bút chì');
  },
  // Trang 3 · thí nghiệm nâng ván
  nangVan: (cap = 'Nâng dần một đầu ván dài <span class="nw"><i>L</i> = 1,00 m</span>.') => doc({ cap, id: 'nv', h: true, tach: true, N: true, ms: true, chieu: '', nhanL: 'L', P: true }),
  // Trang 3 · ảnh thật
  gaiLop: (cap = 'Gai lốp làm ma sát với đường tăng hay giảm?') => {
    const f = [resolve(HERE, '../../book/assets/anh-that/gai-lop-xe.jpg'), '/Users/MAC/Projects/thachlab/book/assets/anh-that/gai-lop-xe.jpg'].find(existsSync);
    return `<figure class="fig"><img src="${pathToFileURL(f).href}" alt="Gai lốp xe" style="display:block;width:100%;height:auto;filter:grayscale(1)"><figcaption>${cap}</figcaption></figure>`;
  },
  // Trang 4 · bài toán mẫu cầu trượt
  cauTruot: (cap = 'Chọn Ox dọc dốc hướng xuống. Chiếu từng lực lên Ox, Oy.') => doc({ cap, id: 'ct', goc: 30, nhanGoc: '30°', tach: true, truc: true, chieu: 'xuong', nhanL: '2,0 m' }),
  // Trang 5 · thử thách: vết phanh
  vetPhanh: (cap = 'Khoá bánh: xe trượt, để lại vết dài 45 m.') => {
    let b = defs('vp1');
    b += dat(6, 314, 120);
    b += ln(20, 117, 196, 117, INK, 5, '14 6');
    b += `<rect x="196" y="50" width="84" height="52" rx="4" fill="#fff" stroke="${INK}" stroke-width="${SW}"/><rect x="280" y="66" width="30" height="36" rx="4" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<circle cx="220" cy="110" r="10" fill="#fff" stroke="${INK}" stroke-width="${SW}"/><circle cx="290" cy="110" r="10" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += arr(20, 34, 186, 34, 'vp1', BLUE, '6 4') + T(102, 26, '45 m', { c: BLUE, a: 'middle', w: 700 });
    return wrap('0 0 320 132', b, cap, 'Vết phanh của xe tải');
  },
  // Bài tập mẫu
  d3: () => keoCheo({ id: 'k3', F: '30 N', goc: '30°', tach: false, gon: true }),
  d4: () => doc({ id: 'd4', goc: 35, nhanGoc: '35°', chieu: 'xuong', nhanL: '5,0 m', N: false, ms: false }),
  d5: () => doc({ id: 'd5', goc: 25, nhanGoc: '25°', chieu: 'len', v0: '6,0 m/s', N: false, ms: false }),
};
