// Hình minh hoạ cho ruột tập Vật lí 10 · Bài 27 Hiệu suất (lesson 72). Cùng quy tắc với hinh.mjs / hinh-ch4.mjs: mỗi hình trả lời
// MỘT câu hỏi (H1), chữ ≥ 20 đơn vị viewBox (≈ 3 mm khi in rộng 46 mm), nét ≥ 2,8, phân biệt bằng NÉT/HÌNH chứ không chỉ màu (in
// đen–trắng), tự vẽ. Mũi tên năng lượng vẽ dạng "dải" (Sankey): bề dày tỉ lệ năng lượng; dải có ích tô nhạt, dải hao phí viền đứt.
// Chỗ HS phải tính để dấu "?" (không lộ đáp số). xem-hinh.mjs chỉ nạp hinh.mjs + hinh-ch4.mjs: muốn chụp các hình này thì đổi
// import trong một bản sao tạm của xem-hinh.mjs sang `hinhBai27` (đã kiểm như vậy ngày 10/11/2026).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`; // chỉ số dưới
const LIGHT = '#dfe7f5';
const arr = (x1, y1, x2, y2, id, c = INK, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${SW}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const box = (x, y, w, h, fill = '#fff') => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="5" fill="${fill}" stroke="${INK}" stroke-width="${SW}"/>`;
// Dải ngang từ x1 tới x2 (mũi ở x2 nếu tip), tâm yc, bề dày w
const bandH = (x1, x2, yc, w, { tip = true, hp = false } = {}) => {
  const h = w / 2, e = tip ? Math.max(10, h + 6) : 0, xb = x2 - (tip ? 12 : 0);
  const d = tip ? `M${x1},${yc - h} L${xb},${yc - h} L${xb},${yc - e} L${x2},${yc} L${xb},${yc + e} L${xb},${yc + h} L${x1},${yc + h} Z`
    : `M${x1},${yc - h} L${x2},${yc - h} L${x2},${yc + h} L${x1},${yc + h} Z`;
  return `<path d="${d}" fill="${hp ? '#fff' : LIGHT}" stroke="${hp ? RED : INK}" stroke-width="2.4"${hp ? ' stroke-dasharray="5 3"' : ''}/>`;
};
// Dải dọc đi xuống từ y1 tới y2, tâm xc
const bandV = (xc, y1, y2, w, hp = true) => {
  const h = w / 2, e = Math.max(10, h + 6), yb = y2 - 12;
  return `<path d="M${xc - h},${y1} L${xc - h},${yb} L${xc - e},${yb} L${xc},${y2} L${xc + e},${yb} L${xc + h},${yb} L${xc + h},${y1} Z" fill="${hp ? '#fff' : LIGHT}" stroke="${hp ? RED : INK}" stroke-width="2.4"${hp ? ' stroke-dasharray="5 3"' : ''}/>`;
};
// Một máy: vào (trái) → có ích (phải) + hao phí (xuống). w* là bề dày dải.
const motMay = (vao, ci, hp, wv, wc, wh, may = 'máy') => {
  let b = bandH(6, 118, 76, wv, { tip: false }) + box(118, 40, 70, 72) + T(153, 83, may, { a: 'middle' });
  b += bandH(188, 300, 76 - (wv - wc) / 2 + 0, wc) + bandV(153, 112, 168, wh);
  b += T(8, 32, `vào: ${vao}`) + T(300, 32, `có ích: ${ci}`, { a: 'end' });
  b += T(176, 160, `hao phí: ${hp}`, { c: RED });
  return b;
};

export const hinhBai27 = {
  // Trang 1 · Dự đoán: hai bóng sáng ngang nhau, công suất ghi trên bóng khác nhau (không vẽ nhiệt: không lộ đáp án)
  haiBong: (cap = 'Hai bóng sáng ngang nhau, số oát ghi trên bóng khác nhau.') => {
    const bong = (x, led) => {
      let g = `<circle cx="${x}" cy="62" r="34" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
      g += `<rect x="${x - 15}" y="94" width="30" height="22" rx="3" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
      g += `<line x1="${x - 15}" y1="102" x2="${x + 15}" y2="102" stroke="${INK}" stroke-width="2"/><line x1="${x - 15}" y1="109" x2="${x + 15}" y2="109" stroke="${INK}" stroke-width="2"/>`;
      g += led ? `<rect x="${x - 12}" y="58" width="24" height="12" fill="${INK}"/><line x1="${x - 8}" y1="70" x2="${x - 8}" y2="94" stroke="${INK}" stroke-width="2"/><line x1="${x + 8}" y1="70" x2="${x + 8}" y2="94" stroke="${INK}" stroke-width="2"/>`
        : `<path d="M${x - 8},94 L${x - 8},66 L${x - 4},56 L${x},66 L${x + 4},56 L${x + 8},66 L${x + 8},94" fill="none" stroke="${INK}" stroke-width="2.2"/>`;
      for (const a of [-150, -115, -90, -65, -30]) {
        const r = (a * Math.PI) / 180;
        g += `<line x1="${(x + 42 * Math.cos(r)).toFixed(1)}" y1="${(62 + 42 * Math.sin(r)).toFixed(1)}" x2="${(x + 56 * Math.cos(r)).toFixed(1)}" y2="${(62 + 56 * Math.sin(r)).toFixed(1)}" stroke="${GREY}" stroke-width="2.6"/>`;
      }
      return g;
    };
    let b = bong(76, false) + bong(232, true);
    b += T(76, 144, 'sợi đốt', { a: 'middle' }) + T(76, 168, '60 W', { a: 'middle', w: 700 });
    b += T(232, 144, 'LED', { a: 'middle' }) + T(232, 168, '9 W', { a: 'middle', w: 700 });
    return wrap('0 0 310 178', b, cap, 'Bóng sợi đốt 60 W và bóng LED 9 W');
  },
  // Trang 1 · II.1: một máy, 100 J vào → 80 J có ích + ? hao phí
  baLoai: (cap = 'Bề dày mũi tên tỉ lệ năng lượng. Dải nét đứt là hao phí.') =>
    wrap('0 0 306 176', motMay('100 J', '80 J', '?', 50, 40, 10), cap, 'Năng lượng vào, có ích và hao phí của một máy'),
  // Bài tương tự · một máy bất kỳ (vào, có ích, hao phí, tên máy)
  mayChung: (vao = '60 kJ', ci = '42 kJ', hp = '?', ten = 'máy', cap = 'Bề dày dải tỉ lệ năng lượng.') =>
    wrap('0 0 306 176', motMay(vao, ci, hp, 50, 35, 15, ten), cap, 'Năng lượng vào, có ích và hao phí'),
  // Dạng 1 · máy khoan 150 kJ → 105 kJ có ích
  khoan: (cap = 'Bề dày dải tỉ lệ năng lượng.') =>
    wrap('0 0 306 176', motMay('150 kJ', '105 kJ', '?', 60, 42, 18, 'khoan'), cap, 'Năng lượng của máy khoan'),
  // Trang 1 · thí nghiệm quạt bàn: hai chỗ sờ tay
  quat: (cap = 'Chỗ 1: vỏ động cơ; chỗ 2: chân đế.') => {
    let b = `<circle cx="110" cy="70" r="58" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    for (const a of [0, 120, 240]) b += `<ellipse cx="110" cy="40" rx="15" ry="28" fill="${LIGHT}" stroke="${INK}" stroke-width="2.2" transform="rotate(${a} 110 70)"/>`;
    b += `<circle cx="110" cy="70" r="9" fill="${INK}"/>`;
    b += `<rect x="158" y="56" width="58" height="30" rx="8" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`; // vỏ động cơ sau quạt
    b += `<rect x="100" y="128" width="20" height="56" fill="#fff" stroke="${INK}" stroke-width="${SW}"/><rect x="56" y="184" width="108" height="16" rx="4" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<circle cx="236" cy="50" r="13" fill="#fff" stroke="${RED}" stroke-width="2.4"/>` + T(236, 57, '1', { a: 'middle', c: RED, w: 700 });
    b += `<line x1="226" y1="58" x2="214" y2="66" stroke="${RED}" stroke-width="2"/>`;
    b += `<circle cx="186" cy="192" r="13" fill="#fff" stroke="${RED}" stroke-width="2.4"/>` + T(186, 199, '2', { a: 'middle', c: RED, w: 700 });
    return wrap('0 0 254 208', b, cap, 'Quạt bàn: 1 vỏ động cơ, 2 chân đế');
  },
  // Trang 2 · thí nghiệm ván nghiêng: các lực tác dụng lên xe
  vanNghieng: (cap = 'Kéo đều xe lên ván: lực kéo F dọc ván, ma sát (nét đứt) ngược chiều chuyển động.') => {
    const A = (30 * Math.PI) / 180, x0 = 18, y0 = 176, L = 270;
    const P = (s) => [x0 + s * Math.cos(A), y0 - s * Math.sin(A)];
    const [xe, ye] = P(150);
    let b = defs('vn1') + defs('vn2') + defs('vn3');
    b += `<path d="M${x0},${y0} L${(x0 + L * Math.cos(A)).toFixed(1)},${y0} L${(x0 + L * Math.cos(A)).toFixed(1)},${(y0 - L * Math.sin(A)).toFixed(1)} Z" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<g transform="rotate(-30 ${xe.toFixed(1)} ${ye.toFixed(1)})"><rect x="${(xe - 26).toFixed(1)}" y="${(ye - 30).toFixed(1)}" width="52" height="26" rx="4" fill="${LIGHT}" stroke="${INK}" stroke-width="${SW}"/>`
      + `<circle cx="${(xe - 15).toFixed(1)}" cy="${(ye - 3).toFixed(1)}" r="4" fill="${INK}"/><circle cx="${(xe + 15).toFixed(1)}" cy="${(ye - 3).toFixed(1)}" r="4" fill="${INK}"/>`;
    const cx = xe, cy = ye - 17;
    b += `<line x1="${(cx + 26).toFixed(1)}" y1="${cy.toFixed(1)}" x2="${(cx + 84).toFixed(1)}" y2="${cy.toFixed(1)}" stroke="${RED}" stroke-width="${SW}" marker-end="url(#vn1)"/>`;
    b += `<line x1="${(cx - 26).toFixed(1)}" y1="${(cy + 8).toFixed(1)}" x2="${(cx - 76).toFixed(1)}" y2="${(cy + 8).toFixed(1)}" stroke="${BLUE}" stroke-width="${SW}" stroke-dasharray="6 4" marker-end="url(#vn2)"/></g>`;
    const rot = (dx, dy) => [xe + dx * Math.cos(A) + dy * Math.sin(A), ye - dx * Math.sin(A) + dy * Math.cos(A)]; // quay −30° quanh (xe, ye)
    const [fx, fy] = rot(92, -17), [mx, my] = rot(-84, -9), [gx, gy] = rot(0, -17);
    b += arr(gx.toFixed(1), gy.toFixed(1), gx.toFixed(1), (gy + 74).toFixed(1), 'vn3');
    b += T(gx + 8, gy + 70, 'mg') + T(fx - 4, fy - 12, 'F', { c: RED, w: 700 }) + T(mx - 44, my - 6, `F${sb('ms')}`, { c: BLUE });
    const xr = x0 + L * Math.cos(A), yt = y0 - L * Math.sin(A);
    b += `<line x1="${(xr + 14).toFixed(1)}" y1="${yt.toFixed(1)}" x2="${(xr + 14).toFixed(1)}" y2="${y0}" stroke="${GREY}" stroke-width="2" stroke-dasharray="4 4"/>` + T(xr + 20, (yt + y0) / 2 + 8, 'h');
    b += `<path d="M${x0 + 46},${y0} A46,46 0 0 0 ${(x0 + 46 * Math.cos(A)).toFixed(1)},${(y0 - 46 * Math.sin(A)).toFixed(1)}" fill="none" stroke="${INK}" stroke-width="2"/>` + T(x0 + 52, y0 - 8, 'α').replace('<text ', '<text font-family="KaTeX_Math" font-style="italic" ') /* Source Sans 3 bản cắt không có chữ Hi Lạp */;
    return wrap('0 0 290 186', b, cap, 'Xe kéo lên ván nghiêng và các lực');
  },
  // Trang 2 · II.3: hai khâu nối tiếp 100 kJ → 30 kJ → ?
  noiTiep: (cap = 'Hai khâu nối tiếp (số minh hoạ). Khâu sau nhận phần ra của khâu trước.') => {
    let b = bandH(4, 46, 60, 40, { tip: false }) + box(46, 26, 74, 68) + T(83, 56, 'động', { a: 'middle' }) + T(83, 78, 'cơ', { a: 'middle' });
    b += bandH(120, 190, 49, 12, { tip: false }) + box(190, 26, 76, 68) + T(228, 56, 'truyền', { a: 'middle' }) + T(228, 78, 'động', { a: 'middle' });
    b += bandH(266, 316, 49, 9.6) + bandV(90, 94, 160, 28) + bandV(236, 94, 150, 3);
    b += T(4, 20, '100 kJ') + T(150, 34, '30 kJ', { a: 'middle' }) + T(316, 24, '24 kJ', { a: 'end' });
    b += T(108, 146, '70 kJ', { c: RED }) + T(254, 140, '6 kJ', { c: RED });
    return wrap('0 0 320 166', b, cap, 'Hai khâu nối tiếp');
  },
  // Trang 3 · Bẫy 1: hiệu suất khác công suất
  haiMay: (cap = 'Cột = P toàn phần; phần tô = P có ích, số % là H. Máy nào mạnh hơn?') => {
    const k = 14, y0 = 170;
    const cot = (x, ptp, pci, ten) => `<rect x="${x}" y="${y0 - ptp * k}" width="62" height="${ptp * k}" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
      + `<rect x="${x}" y="${y0 - pci * k}" width="62" height="${pci * k}" fill="${LIGHT}" stroke="${INK}" stroke-width="${SW}"/>`
      + T(x + 31, y0 + 24, ten, { a: 'middle', w: 700 }) + T(x + 72, y0 - ptp * k + 18, `${String(ptp).replace('.', ',')} kW`);
    let b = `<line x1="10" y1="${y0}" x2="290" y2="${y0}" stroke="${INK}" stroke-width="${SW}"/>`;
    b += cot(30, 10, 6, 'X') + T(61, y0 - 36, '60 %', { a: 'middle', w: 700 });
    b += cot(176, 4, 3.2, 'Y') + T(207, y0 - 16, '80 %', { a: 'middle', w: 700 });
    return wrap('0 0 300 200', b, cap, 'Hai máy: công suất toàn phần và có ích');
  },
  // Trang 4 · bài toán mẫu: thang máy
  thangMay: (cap = 'Cabin cùng người 300 kg đi lên đều.') => {
    let b = defs('tm');
    b += `<rect x="40" y="40" width="120" height="208" fill="none" stroke="${GREY}" stroke-width="2.4"/>`;
    b += box(56, 4, 88, 32) + T(100, 27, 'động cơ', { a: 'middle' });
    b += `<line x1="100" y1="36" x2="100" y2="186" stroke="${INK}" stroke-width="2"/>`;
    b += `<rect x="62" y="74" width="76" height="56" rx="3" fill="none" stroke="${GREY}" stroke-width="2.4" stroke-dasharray="6 4"/>`;
    b += `<rect x="62" y="186" width="76" height="56" rx="3" fill="${LIGHT}" stroke="${INK}" stroke-width="${SW}"/>` + T(100, 221, '300 kg', { a: 'middle', w: 700 });
    b += `<line x1="180" y1="240" x2="180" y2="134" stroke="${INK}" stroke-width="${SW}" marker-end="url(#tm)"/>` + T(186, 196, 'h = 5 m');
    b += `<line x1="150" y1="242" x2="186" y2="242" stroke="${GREY}" stroke-width="2"/><line x1="150" y1="130" x2="186" y2="130" stroke="${GREY}" stroke-width="2"/>`;
    b += T(158, 22, '1,25 kW') + T(186, 100, 't = 20 s');
    return wrap('0 0 270 252', b, cap, 'Thang máy nâng cabin');
  },
  // Trang 5 · thử thách ★★: tấm pin mặt trời
  pinMT: (cap = 'Ánh sáng chiếu lên tấm pin, pin cho ra điện.') => {
    let b = defs('pm');
    b += `<path d="M30,150 L200,150 L240,100 L70,100 Z" fill="${LIGHT}" stroke="${INK}" stroke-width="${SW}"/>`;
    for (const x of [112, 155, 198]) b += `<line x1="${x - 42}" y1="150" x2="${x}" y2="100" stroke="${INK}" stroke-width="1.6"/>`;
    b += `<line x1="50" y1="125" x2="220" y2="125" stroke="${INK}" stroke-width="1.6"/>`;
    for (const x of [80, 130, 180]) b += arr(x, 20, x, 88, 'pm', RED);
    b += T(196, 32, '1000 W/m²', { c: RED }) + T(70, 178, 'S = 1,6 m²') + T(250, 128, 'P = ?', { w: 700 });
    return wrap('0 0 320 186', b, cap, 'Tấm pin mặt trời');
  },
  // Dạng 4 · tời kéo thùng vữa qua ròng rọc
  toi: (cap = 'Tời kéo đều thùng vữa qua ròng rọc cố định.') => {
    let b = defs('to');
    b += `<line x1="4" y1="210" x2="296" y2="210" stroke="${INK}" stroke-width="${SW}"/><line x1="44" y1="30" x2="44" y2="210" stroke="${GREY}" stroke-width="2.4"/>`;
    b += `<line x1="44" y1="30" x2="124" y2="30" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<circle cx="96" cy="44" r="14" fill="#fff" stroke="${INK}" stroke-width="${SW}"/><line x1="96" y1="30" x2="96" y2="44" stroke="${INK}" stroke-width="2"/>`;
    b += `<line x1="82" y1="44" x2="82" y2="150" stroke="${INK}" stroke-width="2"/><line x1="110" y1="44" x2="236" y2="172" stroke="${INK}" stroke-width="2"/>`;
    b += `<path d="M62,150 L102,150 L98,196 L66,196 Z" fill="${LIGHT}" stroke="${INK}" stroke-width="${SW}"/>` + T(108, 192, '350 kg', { w: 700 });
    b += box(208, 172, 56, 36) + T(236, 197, 'tời', { a: 'middle' }) + T(170, 62, '2,5 kW') + T(170, 88, 't = 24 s');
    b += arr(22, 206, 22, 56, 'to') + T(4, 22, 'h = 12 m');
    return wrap('0 0 300 218', b, cap, 'Tời kéo thùng vữa');
  },
  // Dạng 5 · ba khâu nối tiếp
  baKhau: (cap = 'Năng lượng đi qua ba khâu rồi mới tới bánh xe.') => {
    let b = defs('bk');
    b += `<rect x="4" y="66" width="30" height="44" rx="3" fill="#fff" stroke="${INK}" stroke-width="${SW}"/><rect x="13" y="60" width="12" height="6" fill="${INK}"/>` + T(19, 136, 'pin', { a: 'middle' });
    const cx = [80, 168, 256], hs = ['95 %', '80 %', '75 %'], ten = ['điều khiển', 'động cơ', 'hộp số'];
    cx.forEach((x, i) => { b += box(x - 34, 66, 68, 44) + T(x, 95, hs[i], { a: 'middle', w: 700 }) + T(x, 48, ten[i], { a: 'middle' }); });
    b += arr(34, 88, 41, 88, 'bk') + arr(114, 88, 129, 88, 'bk') + arr(202, 88, 217, 88, 'bk');
    b += `<circle cx="256" cy="160" r="22" fill="#fff" stroke="${INK}" stroke-width="${SW}"/><circle cx="256" cy="160" r="5" fill="${INK}"/>` + T(226, 167, 'bánh xe', { a: 'end' });
    b += `<path d="M290,88 L304,88 L304,160 L282,160" fill="none" stroke="${INK}" stroke-width="2.4" marker-end="url(#bk)"/>`;
    return wrap('0 0 316 204', b, cap, 'Ba khâu nối tiếp');
  },
};
