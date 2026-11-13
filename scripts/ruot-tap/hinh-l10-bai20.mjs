// Hình minh hoạ cho ruột tập VL10 · Bài 20 Một số ví dụ về cách giải bài toán động lực học (lesson 65). Cùng quy tắc với hinh.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh (thành phần của P ghi "?", ô giữa cầu nối ghi "?").
// Ảnh thật duy nhất: cầu trượt (book/assets/anh-that/cau-truot.jpg, Wikimedia CC BY-SA 3.0 — hồ sơ sách l10-ch3, mục anh_that 65).
// Xem thử: node scripts/ruot-tap/l10-bai20.mjs --hinh (chụp vào out/hinh-l10-bai20/).
import { dirname, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
// chữ Hi Lạp: Source Sans 3 chỉ nạp latin/vietnamese, α rơi về font hệ thống → lấy từ KaTeX_Math (đã nạp qua katex.min.css)
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const km = (ch, o = '') => `<tspan font-family="KaTeX_Main"${o}>${ch}</tspan>`; // ký hiệu ngoài bộ chữ Source Sans (Σ ∥ ⊥) → KaTeX_Main, tránh rơi về Helvetica
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
const hop = (x, y, w, h, lab = '') => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="4" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
  + (lab ? T(x + w / 2, y + h / 2 + 7, lab, { a: 'middle', w: 700 }) : '');

const ANH = resolve(dirname(fileURLToPath(import.meta.url)), '../../book/assets/anh-that');
const anh = (file, cap) => `<figure class="fig"><img src="${pathToFileURL(resolve(ANH, file)).href}" alt="${cap}" style="display:block;width:100%;height:auto">${cap ? `<figcaption>${cap}</figcaption>` : ''}</figure>`;

// Thùng trên sàn ngang, lực kéo F chếch lên góc goc (0 = kéo ngang). truc: vẽ Ox, Oy.
const keo = (cap, { F = 'F', goc = 30, nhanGoc = gk('α'), truc = false, id = 'k' } = {}) => {
  let b = defs(id + 'a') + defs(id + 'b') + defs(id + 'c');
  b += dat(10, 312, 150) + hop(96, 108, 112, 42);
  const cx = 152, cy = 129;
  if (goc > 0) {
    b += arr(208, 118, f1(208 + 86 * Math.cos(R(goc))), f1(118 - 86 * Math.sin(R(goc))), id + 'a', RED) + T(300, 52, F, { c: RED, w: 700, a: 'end' });
    b += ln(208, 118, 300, 118, GREY, 2, '5 4') + cung(208, 118, 36, 0, goc) + T(250, 112, nhanGoc);
  } else {
    b += arr(208, 129, 294, 129, id + 'a', RED) + T(300, 116, F, { c: RED, w: 700, a: 'end' });
  }
  b += arr(cx, cy, cx, 204, id + 'b', RED) + T(cx + 8, 202, 'P', { c: RED, w: 700 });
  b += arr(cx, 108, cx, goc > 0 ? 58 : 34, id + 'b', INK) + T(cx - 8, goc > 0 ? 66 : 42, 'N', { w: 700, a: 'end' });
  b += arr(96, 140, 40, 140, id + 'c', INK, '6 4') + T(12, 130, `F${sb('ms')}`);
  if (truc) b += arr(20, 30, 80, 30, id + 'c', BLUE) + T(84, 36, 'x', { c: BLUE, w: 700 }) + arr(20, 30, 20, 4, id + 'c', BLUE) + T(28, 18, 'y', { c: BLUE, w: 700 });
  return wrap('0 0 320 212', b, cap, 'Các lực tác dụng lên thùng kéo trên sàn ngang');
};

// Mặt nghiêng: chân dốc bên phải, vật trượt xuống (sang phải). tach: vẽ hai thành phần của P (nét đứt) ghi "?".
const doc = (cap, { goc = 30, nhanGoc = gk('α'), tach = false, N = true, ms = false, truc = false, s = '', id = 'd', vatLen = false } = {}) => {
  const c = Math.cos(R(goc)), sn = Math.sin(R(goc));
  const xf = 306, yf = 196, L = 290, xt = xf - L * c, yt = yf - L * sn;
  let b = defs(id + 'a') + defs(id + 'b') + defs(id + 'c') + defs(id + 'd');
  b += `<path d="M${f1(xt)},${f1(yt)} L${xf},${yf} L${f1(xt)},${yf} z" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
  b += cung(xf, yf, 46, 180 - goc, 180) + T(xf - 76, yf - 8, nhanGoc);
  const ux = c, uy = sn, nx = sn, ny = -c; // u: xuống dốc; n: pháp tuyến hướng ra ngoài mặt dốc
  const tp = 0.52, px = xt + L * tp * c, py = yt + L * tp * sn, w = 52, h = 32;
  const cx = px + nx * h / 2, cy = py + ny * h / 2;
  b += `<rect x="${f1(cx - w / 2)}" y="${f1(cy - h / 2)}" width="${w}" height="${h}" rx="3" fill="#fff" stroke="${INK}" stroke-width="${SW}" transform="rotate(${goc} ${f1(cx)} ${f1(cy)})"/>`;
  const Lp = tach ? 92 : 74;
  b += arr(f1(cx), f1(cy), f1(cx), f1(cy + Lp), id + 'a', RED) + T(cx + 8, cy + Lp - 2, 'P', { c: RED, w: 700 });
  if (tach) {
    const a1 = Lp * sn, a2 = Lp * c;
    b += arr(f1(cx), f1(cy), f1(cx + ux * a1), f1(cy + uy * a1), id + 'b', RED, '6 4') + T(cx + ux * a1 + 8, cy + uy * a1 + 4, `P${km('∥', ' font-size="15" dy="5"')}<tspan dy="-5"> </tspan>= ?`, { c: RED });
    b += arr(f1(cx), f1(cy), f1(cx - nx * a2), f1(cy - ny * a2), id + 'b', RED, '6 4') + T(cx - nx * a2 - 6, cy - ny * a2 + 8, `P${km('⊥', ' font-size="15" dy="5"')}<tspan dy="-5"> </tspan>= ?`, { c: RED, a: 'end' });
  }
  if (N) { const LN = tach ? Lp * c : 58; b += arr(f1(cx), f1(cy), f1(cx + nx * LN), f1(cy + ny * LN), id + 'c', INK) + T(cx + nx * LN + 6, cy + ny * LN + 4, 'N', { w: 700 }); }
  if (ms) { const d = vatLen ? 1 : -1, sx = cx + d * ux * (w / 2), sy = cy + d * uy * (w / 2);
    b += arr(f1(sx), f1(sy), f1(sx + d * ux * 50), f1(sy + d * uy * 50), id + 'c', INK, '6 4') + T(sx + d * ux * 50 + (d < 0 ? -4 : 4), sy + d * uy * 50 - 10, `F${sb('ms')}`, { a: d < 0 ? 'end' : 'start' }); }
  if (truc) { const ox = xt + 30 - nx * 0, oy = yt - 34; b += arr(f1(ox), f1(oy), f1(ox + ux * 70), f1(oy + uy * 70), id + 'd', BLUE) + T(ox + ux * 70 - 4, oy + uy * 70 - 12, 'x (+)', { c: BLUE, w: 700 }); }
  if (s) b += T(xt + L * 0.15 * c + 4, yt + L * 0.15 * sn + 36, s);
  return wrap(`0 0 320 ${tach ? 222 : 208}`, b, cap, 'Vật trên mặt phẳng nghiêng');
};

// Hai vật nối dây qua ròng rọc ở mép bàn; m1 trên bàn, m2 treo.
const rongRoc = (cap, { m1 = `m${sb('1')}`, m2 = `m${sb('2')}`, ms = true, duong = true, id = 'r' } = {}) => {
  let b = defs(id + 'a') + defs(id + 'b') + defs(id + 'c');
  b += `<rect x="10" y="86" width="236" height="14" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + ln(30, 100, 30, 200, INK, SW) + ln(226, 100, 226, 200, INK, SW);
  b += `<circle cx="262" cy="76" r="14" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + ln(246, 92, 258, 80, INK, 2.2);
  b += hop(64, 50, 74, 36, m1) + hop(250, 138, 42, 40, m2);
  b += ln(138, 62, 262, 62, INK, 2) + ln(276, 76, 276, 138, INK, 2);
  b += arr(138, 70, 186, 70, id + 'a', RED) + T(184, 56, 'T', { c: RED, w: 700 });
  b += arr(270, 138, 270, 104, id + 'a', RED) + T(264, 120, 'T', { c: RED, w: 700, a: 'end' });
  b += arr(271, 178, 271, 222, id + 'b', RED) + T(262, 218, `P${sb('2')}`, { c: RED, w: 700, a: 'end' });
  if (ms) b += arr(64, 78, 18, 78, id + 'c', INK, '6 4') + T(14, 70, `F${sb('ms')}`);
  if (duong) b += `<path d="M96,32 L232,32 Q300,32 304,100 L304,196" fill="none" stroke="${BLUE}" stroke-width="2.4" stroke-dasharray="6 4" marker-end="url(#${id}c)"/>` + T(150, 24, '(+)', { c: BLUE, w: 700 });
  return wrap('0 0 320 230', b, cap, 'Hai vật nối dây qua ròng rọc');
};

export const hinhL10b20 = {
  // Trang 1 · Dự đoán: ảnh thật cầu trượt (chú thích không nói ai tới trước)
  cauTruot: (cap = 'Cầu trượt: trọng lực kéo người xuống dốc, ma sát cản lại.') => anh('cau-truot.jpg', cap),
  // Trang 2 · cầu nối: ô giữa để "?"
  cauNoi: (cap = 'Ô giữa là đại lượng nào?') => {
    let b = defs('cn1') + defs('cn2');
    b += hop(6, 40, 86, 52) + T(49, 66, 'Lực', { a: 'middle', w: 700 }) + T(49, 86, `${km('Σ')}F`, { a: 'middle' });
    b += `<circle cx="160" cy="66" r="30" fill="#fff" stroke="${BLUE}" stroke-width="${SW}"/>` + T(160, 74, '?', { a: 'middle', w: 700, size: 26, c: BLUE });
    b += hop(228, 40, 86, 52) + T(271, 66, 'v, s, t', { a: 'middle', w: 700 }) + T(271, 86, 'c.động', { a: 'middle' });
    b += arr(94, 58, 126, 58, 'cn1') + arr(126, 76, 94, 76, 'cn1');
    b += arr(194, 58, 226, 58, 'cn2') + arr(226, 76, 194, 76, 'cn2');
    b += T(110, 124, 'ĐL II', { a: 'middle' }) + T(210, 124, 'CT c.động', { a: 'middle' });
    return wrap('0 0 320 136', b, cap, 'Lực, gia tốc và chuyển động');
  },
  keoXien: (cap = 'Dây kéo chếch lên. So độ dài N với P.') => keo(cap, { id: 'kx', truc: true }),
  docTach: (cap = 'Ox dọc dốc, chiều xuống. Hai thành phần của P bằng bao nhiêu?') => doc(cap, { tach: true, truc: true, id: 'dt' }),
  rongRoc: (cap = 'Vẽ chiều (+) vào hình.') => rongRoc(cap, { id: 'rr', duong: false }),
  xeLan: (cap = 'Xe nối quả nặng qua ròng rọc.') => rongRoc(cap, { m1: 'xe', m2: '', ms: false, duong: false, id: 'xl' }),
  // Bẫy 1: hộp đang trượt lên dốc, tay đã buông
  hopLen: (cap = 'Hộp đang trượt lên. Vẽ đủ lực.') => doc(cap, { N: false, id: 'hl', s: '' })
    .replace('</svg>', `${defs('hlm')}<path d="M150,60 L96,30" stroke="${BLUE}" stroke-width="2.4" stroke-dasharray="6 4" marker-end="url(#hlm)"/>${T(70, 22, 'v', { c: BLUE, w: 700 })}</svg>`),
  // Thử thách ★★★: vật chồng
  vatChong: (cap = 'Kéo ván; khối trên ván có trượt theo không?') => {
    let b = defs('vc1') + defs('vc2');
    b += dat(10, 312, 150) + hop(60, 122, 180, 28, 'ván 2 kg') + hop(110, 82, 70, 40, '1 kg');
    b += arr(240, 136, 304, 136, 'vc1', RED) + T(304, 122, 'F', { c: RED, w: 700, a: 'end' });
    b += T(160, 186, 'sàn nhẵn', { a: 'middle', c: GREY });
    return wrap('0 0 320 196', b, cap, 'Khối đặt trên ván, kéo ván');
  },
  // ===== Bài tập mẫu =====
  d1: (cap = 'Lực kéo nằm ngang: N so với P?') => keo(cap, { F: '100 N', goc: 0, id: 'd1' }),
  d2: (cap = 'sin 37° = 0,6; cos 37° = 0,8.') => keo(cap, { F: '120 N', nhanGoc: '37°', id: 'd2' }),
  d3: (cap = 'Trượt xuống: F<sub>ms</sub> hướng lên dốc.') => doc(cap, { nhanGoc: '30°', ms: true, s: '10 m', id: 'd3' }),
  d4: (cap = 'Bánh bị khoá, xe trượt.') => {
    let b = defs('d4a') + defs('d4b') + defs('d4c');
    b += dat(8, 312, 120);
    b += `<path d="M60,104 L66,80 L96,66 L150,66 L172,84 L196,88 L196,104 z" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<circle cx="88" cy="108" r="12" fill="#fff" stroke="${INK}" stroke-width="${SW}"/><circle cx="170" cy="108" r="12" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += arr(204, 52, 286, 52, 'd4a', BLUE) + T(250, 40, `v${sb('0')}= 15 m/s`, { c: BLUE, a: 'middle' });
    b += arr(60, 96, 14, 96, 'd4b', RED, '6 4') + T(10, 80, `F${sb('hãm')}`, { c: RED });
    b += ln(60, 140, 290, 140, GREY, 2) + arr(60, 140, 290, 140, 'd4c', INK) + T(175, 164, 'đi 22,5 m thì dừng', { a: 'middle' });
    return wrap('0 0 320 172', b, cap, 'Ô tô phanh trượt');
  },
  d5: (cap = 'Hệ số ma sát 0,2 cho cả lúc nghỉ và lúc trượt.') => rongRoc(cap, { m1: '2 kg', m2: '1 kg', id: 'd5' }),
  // ===== Bài tương tự =====
  t22: (cap = 'Cùng 40 N: kéo xiên 60° hay kéo ngang nhanh hơn?') => keo(cap, { F: '40 N', nhanGoc: '60°', goc: 60, id: 't22' }),
  t32: (cap = 'Dốc nhẵn; chiều (+) lên dốc.') => doc(cap, { nhanGoc: '30°', N: true, id: 't32' })
    .replace('</svg>', `${defs('t32m')}<path d="M150,70 L96,40" stroke="${BLUE}" stroke-width="2.4" stroke-dasharray="6 4" marker-end="url(#t32m)"/>${T(56, 34, `v${sb('0')}`, { c: BLUE, w: 700 })}</svg>`),
};
