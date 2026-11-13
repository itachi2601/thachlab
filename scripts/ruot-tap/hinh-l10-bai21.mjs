// Hình minh hoạ cho ruột tập VL10 · Bài 21 Moment lực. Cân bằng của vật rắn (lesson 66). Cùng quy tắc với hinh.mjs/hinh-l10-bai23.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh; mũi tên lực KHÔNG vẽ theo tỉ lệ ở hình có lực cần tìm (tránh lộ đáp số).
// Ảnh thật duy nhất: book/assets/anh-that/nho-dinh-bang-bua.jpg (Wikimedia, CC BY-SA 4.0, khai báo trong book/sach/l10-ch3-dong-luc-hoc.json).
// Xem thử: node scripts/ruot-tap/l10-bai21.mjs --hinh (chụp vào out/hinh-l10-bai21/).
import { dirname, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
// chữ Hi Lạp: Source Sans 3 chỉ nạp latin/vietnamese → lấy từ KaTeX_Math (đã nạp qua katex.min.css)
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const f1 = (v) => (+v).toFixed(1);
const arr = (x1, y1, x2, y2, id, c = INK, dash = '') =>
  `<line x1="${f1(x1)}" y1="${f1(y1)}" x2="${f1(x2)}" y2="${f1(y2)}" stroke="${c}" stroke-width="${SW}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${f1(x1)}" y1="${f1(y1)}" x2="${f1(x2)}" y2="${f1(y2)}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const R = (d) => (d * Math.PI) / 180;
const cung = (x, y, r, a1, a2, c = INK) => {
  const p = (a) => `${f1(x + r * Math.cos(R(a)))},${f1(y - r * Math.sin(R(a)))}`;
  return `<path d="M${p(a1)} A${r},${r} 0 0 0 ${p(a2)}" fill="none" stroke="${c}" stroke-width="2.2"/>`;
};
const truc = (x, y) => `<circle cx="${x}" cy="${y}" r="6" fill="#fff" stroke="${INK}" stroke-width="${SW}"/><circle cx="${x}" cy="${y}" r="1.8" fill="${INK}"/>`;
const giaDo = (x, y) => `<path d="M${x},${y} L${x - 13},${y + 24} L${x + 13},${y + 24} z" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
// đoạn đo kích thước có hai vạch đầu, nhãn ở giữa
const doDai = (x1, x2, y, s, c = GREY) => ln(x1, y, x2, y, c, 2) + ln(x1, y - 6, x1, y + 6, c, 2) + ln(x2, y - 6, x2, y + 6, c, 2)
  + T((x1 + x2) / 2, y - 6, s, { a: 'middle' });
const ANH = resolve(dirname(fileURLToPath(import.meta.url)), '../../book/assets/anh-that');
const anh = (file, cap, w) => `<figure class="fig"${w ? ` style="width:${w}mm"` : ''}><img src="${pathToFileURL(resolve(ANH, file)).href}" alt="" style="display:block;width:100%;aspect-ratio:1/1;object-fit:cover;object-position:75% 35%">${cap ? `<figcaption>${cap}</figcaption>` : ''}</figure>`;

// Thanh nằm ngang từ x0 tới x1 ở độ cao y (dày 12)
const thanh = (x0, x1, y) => `<rect x="${x0}" y="${y - 6}" width="${x1 - x0}" height="12" rx="2" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;

export const hinhL10b21 = {
  // Tr.1 · Dự đoán: búa nhổ đinh, hai chỗ đặt tay. Chú thích chỉ nhắc lại số liệu, không nêu kết luận.
  buaNhoDinh: (cap = 'Đầu búa tì lên gỗ tại O. Minh ấn 300 N cách O 8 cm; anh Tuấn ấn 150 N cách O 30 cm.') => {
    const O = [46, 136], a = 20, c = Math.cos(R(a)), s = Math.sin(R(a)), k = 7.6; // 7,6 đơn vị / cm dọc cán
    const P = (cm) => [O[0] + cm * k * c, O[1] - cm * k * s];
    const [mx, my] = P(8), [tx, ty] = P(30), [ex, ey] = P(34);
    let b = defs('bnA') + defs('bnB');
    b += `<rect x="6" y="${O[1] + 2}" width="70" height="14" fill="#fff" stroke="${GREY}" stroke-width="2"/>` + ln(40, O[1] + 2, 40, O[1] - 16, GREY, 3)
      + `<rect x="18" y="${O[1] - 22}" width="34" height="22" rx="3" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<line x1="${O[0]}" y1="${O[1] - 6}" x2="${f1(ex)}" y2="${f1(ey - 6)}" stroke="${INK}" stroke-width="9" stroke-linecap="round"/>`
      + `<line x1="${O[0]}" y1="${O[1] - 6}" x2="${f1(ex)}" y2="${f1(ey - 6)}" stroke="#fff" stroke-width="4" stroke-linecap="round"/>`;
    b += `<circle cx="${O[0]}" cy="${O[1]}" r="3.5" fill="${INK}"/>` + T(O[0] - 32, O[1] + 2, 'O', { w: 700, a: 'end' });
    const L1 = 66, L2 = 44; // không vẽ theo tỉ lệ độ lớn
    b += arr(mx - L1 * s, my - 6 - L1 * c, mx, my - 10, 'bnA', RED) + T(mx - L1 * s - 4, my - L1 * c - 14, 'Minh', { c: RED, w: 700, a: 'middle' });
    b += arr(tx - L2 * s, ty - 6 - L2 * c, tx, ty - 10, 'bnB', BLUE, '7 4') + T(tx - L2 * s - 8, ty - L2 * c + 18, 'Tuấn', { c: BLUE, w: 700, a: 'end' });
    // đoạn đo dọc cán, phía dưới cán (khung xoay theo cán), từ O tới chỗ đặt tay
    const dim = (cm, off, s0) => { const x2 = O[0] + cm * k; return ln(O[0], O[1] + off, x2, O[1] + off, GREY, 2) + ln(O[0], O[1] + off - 6, O[0], O[1] + off + 6, GREY, 2)
      + ln(x2, O[1] + off - 6, x2, O[1] + off + 6, GREY, 2) + T(O[0] + cm * k - 4, O[1] + off + 22, s0, { a: 'end' }); };
    b += `<g transform="rotate(${-a} ${O[0]} ${O[1]})">${dim(8, 30, '8 cm')}${dim(30, 30, '30 cm')}</g>`;
    return wrap('0 0 320 196', b, cap, 'Búa nhổ đinh, hai chỗ đặt tay');
  },

  // Tr.2 · Lực xiên: kéo dài giá, hạ vuông góc từ O. Không ghi d = r sin α (HS tự điền).
  lucXien: (cap = 'r: từ trục O tới điểm đặt A. Kéo dài giá của F (nét đứt), hạ vuông góc từ O: đoạn d.') => {
    const O = [34, 178], A = [214, 178], a = 40, u = [Math.cos(R(a)), Math.sin(R(a))]; // F chéo xuống phải
    const dot = (O[0] - A[0]) * u[0] + (O[1] - A[1]) * u[1], H = [A[0] + dot * u[0], A[1] + dot * u[1]];
    let b = defs('lxA') + defs('lxB');
    b += ln(O[0], O[1], A[0], A[1], INK, 5) + truc(O[0], O[1]) + T(O[0] - 4, O[1] + 30, 'O', { w: 700 }) + T(A[0] - 2, A[1] + 30, 'A', { w: 700 });
    b += T((O[0] + A[0]) / 2, O[1] + 28, 'r', { a: 'middle', w: 700 });
    b += ln(H[0] - 22 * u[0], H[1] - 22 * u[1], A[0], A[1], GREY, 2.4, '7 5');
    b += arr(A[0], A[1], A[0] + 86 * u[0], A[1] + 86 * u[1], 'lxA', RED) + T(A[0] + 86 * u[0] + 4, A[1] + 86 * u[1] - 4, 'F', { c: RED, w: 700 });
    b += ln(O[0], O[1], H[0], H[1], RED, 2.6, '4 3');
    // ô vuông góc tại H
    const v = [-u[1], u[0]], q = 9;
    b += `<path d="M${f1(H[0] - q * u[0])},${f1(H[1] - q * u[1])} l${f1(-q * v[0])},${f1(-q * v[1])} l${f1(q * u[0])},${f1(q * u[1])}" fill="none" stroke="${INK}" stroke-width="1.8"/>`;
    b += T((O[0] + H[0]) / 2 - 18, (O[1] + H[1]) / 2 - 2, 'd', { c: RED, w: 700 }) + T(H[0] - 22, H[1] - 6, 'H', { a: 'middle' });
    b += cung(A[0], A[1], 38, -a, 0) + ln(A[0], A[1], A[0] + 60, A[1], GREY, 2, '3 4') + T(A[0] + 44, A[1] + 34, gk('α'));
    return wrap('0 0 320 250', b, cap, 'Cánh tay đòn của lực xiên');
  },

  // Tr.2 · Thí nghiệm thước có trục ở giữa
  thuocTN: (cap = 'Thước nằm ngang. P<sub>1</sub> = 2,0 N treo cách O 15 cm; lực kế kéo thẳng đứng xuống ở d<sub>2</sub>.') => {
    const y = 74, O = 150, k = 5; // 5 đơn vị / cm
    const x1 = O - 15 * k, x2 = O + 26 * k;
    let b = defs('ttA');
    b += thanh(14, 306, y) + Array.from({ length: 15 }, (_, i) => ln(20 + i * 20, y - 6, 20 + i * 20, y, GREY, 1.4)).join('');
    b += truc(O, y) + T(O, y - 16, 'O', { a: 'middle', w: 700 });
    b += doDai(x1, O, 34, `d${sb('1')}`) + doDai(O, x2, 34, `d${sb('2')}`);
    b += ln(x1, y + 6, x1, y + 66, INK, 2) + `<rect x="${x1 - 18}" y="${y + 66}" width="36" height="30" rx="3" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
      + T(x1 + 24, y + 90, `P${sb('1')}`, { w: 700 });
    b += `<rect x="${x2 - 11}" y="${y + 18}" width="22" height="66" rx="4" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
      + Array.from({ length: 5 }, (_, i) => ln(x2 - 6, y + 32 + i * 10, x2 + 6, y + 32 + i * 10, GREY, 1.4)).join('')
      + ln(x2, y + 6, x2, y + 18, INK, 2) + arr(x2, y + 84, x2, y + 128, 'ttA', RED) + T(x2 - 16, y + 122, `F${sb('2')}`, { c: RED, w: 700, a: 'end' });
    return wrap('0 0 320 210', b, cap, 'Thước có trục quay ở giữa');
  },

  // Tr.3 · Ngẫu lực trên vô lăng
  voLang: (cap = 'Hai lực bằng nhau, song song, ngược chiều. d: khoảng cách giữa hai giá (nét đứt).') => {
    const C = [160, 112], r = 84;
    let b = defs('vlA') + defs('vlB');
    b += `<circle cx="${C[0]}" cy="${C[1]}" r="${r}" fill="none" stroke="${INK}" stroke-width="7"/>` + ln(C[0] - r, C[1], C[0] + r, C[1], INK, 4) + truc(C[0], C[1]);
    b += ln(C[0] - r, 10, C[0] - r, 206, GREY, 2, '7 5') + ln(C[0] + r, 10, C[0] + r, 206, GREY, 2, '7 5');
    b += arr(C[0] - r, C[1], C[0] - r, C[1] - 70, 'vlA', RED) + T(C[0] - r - 16, C[1] - 54, `F${sb('1')}`, { c: RED, w: 700, a: 'end' });
    b += arr(C[0] + r, C[1], C[0] + r, C[1] + 70, 'vlB', RED) + T(C[0] + r + 16, C[1] + 66, `F${sb('2')}`, { c: RED, w: 700 });
    b += doDai(C[0] - r, C[0] + r, 226, 'd');
    return wrap('0 0 320 236', b, cap, 'Ngẫu lực trên vô lăng');
  },

  // Tr.4 · Bài toán mẫu: thanh gỗ trên giá đỡ, túi gạo ở A. Mũi tên KHÔNG theo tỉ lệ (P1 là ẩn).
  thanhMau: (cap = 'Ba lực lên thanh: P<sub>1</sub> ở A, P ở G, N ở O. Mũi tên không vẽ theo tỉ lệ.') => {
    const y = 104, A = 22, B = 298, k = (B - A) / 1.2, O = A + 0.4 * k, G = A + 0.6 * k;
    let b = defs('tmA') + defs('tmB');
    b += thanh(A, B, y) + giaDo(O, y + 6);
    b += arr(A + 4, y, A + 4, y + 62, 'tmA', RED) + T(A + 16, y + 52, `P${sb('1')}`, { c: RED, w: 700 });
    b += arr(G, y, G, y + 62, 'tmA', RED) + T(G + 14, y + 52, 'P', { c: RED, w: 700 });
    b += arr(O, y, O, y - 70, 'tmB', BLUE, '7 4') + T(O + 14, y - 48, 'N', { c: BLUE, w: 700 });
    b += T(A, y - 14, 'A', { w: 700 }) + T(B - 14, y - 14, 'B', { w: 700 }) + T(O - 30, y + 30, 'O', { w: 700 }) + T(G - 4, y - 14, 'G', { w: 700, a: 'end' });
    b += doDai(A, O, 196, '0,4 m') + doDai(A, B, 226, '1,2 m');
    return wrap('0 0 320 236', b, cap, 'Thanh gỗ trên giá đỡ');
  },

  // Tr.5 · Thử thách ⭐⭐⭐: thanh nhẹ trên hai giá
  haiGia: (cap = 'Thanh nhẹ AB dài 1 m trên hai giá; vật 300 N cách A 0,4 m.') => {
    const y = 70, A = 30, B = 290, X = A + 0.4 * (B - A);
    let b = defs('hgA') + defs('hgB');
    b += thanh(A, B, y) + giaDo(A + 6, y + 6) + giaDo(B - 6, y + 6);
    b += ln(X, y + 6, X, y + 40, INK, 2) + `<rect x="${X - 34}" y="${y + 40}" width="68" height="32" rx="3" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(X, y + 63, '300 N', { a: 'middle' });
    b += arr(A + 6, y - 8, A + 6, y - 50, 'hgB', BLUE, '7 4') + T(A + 22, y - 30, `N${sb('A')}`, { c: BLUE, w: 700 });
    b += arr(B - 6, y - 8, B - 6, y - 50, 'hgB', BLUE, '7 4') + T(B - 22, y - 30, `N${sb('B')}`, { c: BLUE, w: 700, a: 'end' });
    b += T(A - 4, y + 52, 'A', { w: 700 }) + T(B - 6, y + 52, 'B', { w: 700 }) + ln(X, y + 72, X, y + 92, GREY, 1.6, '3 3') + ln(A, y + 8, A, y + 92, GREY, 1.6, '3 3') + doDai(A, X, y + 92, '0,4 m');
    return wrap('0 0 320 170', b, cap, 'Thanh nhẹ trên hai giá');
  },

  // Tr.5 · ảnh thật (dọc 2:3) đặt cột hẹp cạnh khối Mang về
  anhBua: (cap = 'Cầm cuối cán khi nhổ đinh.') => anh('nho-dinh-bang-bua.jpg', `${cap}<br><span style="font-size:2.4mm">Ảnh: Wikimedia Commons (File:Claw_hammer.JPG), CC BY-SA 4.0</span>`),

  // Tr.6 · Dạng 2: cối xay nhìn từ trên xuống
  coiXay: (cap = 'Nhìn từ trên xuống: tâm O, núm A.') => {
    const O = [60, 128], A = [220, 128], a = 40, u = [Math.cos(R(a)), -Math.sin(R(a))]; // F chéo lên phải
    let b = defs('cxA');
    b += cung(O[0], O[1], 186, -38, 38, GREY);
    b += ln(O[0], O[1], A[0], A[1], INK, 2.4, '6 4') + truc(O[0], O[1]) + T(O[0] - 4, O[1] + 30, 'O', { w: 700 });
    b += `<circle cx="${A[0]}" cy="${A[1]}" r="9" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(A[0] - 14, A[1] + 28, 'A', { w: 700, a: 'end' });
    b += T((O[0] + A[0]) / 2, O[1] + 28, '0,30 m', { a: 'middle' });
    b += arr(A[0], A[1], A[0] + 84 * u[0], A[1] + 84 * u[1], 'cxA', RED) + T(A[0] + 84 * u[0] - 12, A[1] + 84 * u[1] - 6, 'F', { c: RED, w: 700, a: 'end' });
    b += ln(A[0], A[1], A[0] + 62, A[1], GREY, 2, '3 4') + cung(A[0], A[1], 40, 0, a) + T(A[0] + 46, A[1] - 8, '40°');
    return wrap('0 0 320 166', b, cap, 'Cối xay nhìn từ trên xuống');
  },

  // Tr.7 · Dạng 4: thanh có hai khối, giá đỡ chưa biết chỗ
  thanhHaiKhoi: (cap = 'Giá đỡ O vẽ ở chỗ bất kì: OA = x cần tìm. P của thanh đặt ở G.') => {
    const y = 96, A = 40, B = 286, O = A + 0.66 * (B - A), G = (A + B) / 2;
    let b = defs('hkA');
    b += thanh(A, B, y) + `<rect x="${A - 17}" y="${y - 22}" width="34" height="34" rx="3" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
      + `<rect x="${B - 12}" y="${y - 16}" width="24" height="24" rx="3" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += giaDo(O, y + 6) + T(O + 16, y + 30, 'O', { w: 700 });
    b += T(A - 26, y - 30, 'A · 40 N', { w: 700 }) + T(B + 18, y - 26, '20 N · B', { w: 700, a: 'end' });
    b += arr(G, y, G, y + 50, 'hkA', RED) + T(G - 18, y + 48, 'P = 20 N', { c: RED, w: 700, a: 'end' }) + T(G - 4, y - 12, 'G', { w: 700, a: 'end' });
    b += doDai(A, O, 166, 'x') + doDai(A, B, 196, '1,0 m');
    return wrap('0 0 320 206', b, cap, 'Thanh có hai khối ở hai đầu');
  },

  // Tr.7 · Dạng 5: thanh gắn bản lề, dây xiên 30°
  banLe: (cap = 'Trục qua bản lề A. Dây hợp với thanh 30°: cánh tay đòn của T là đoạn vuông góc từ A tới dây.') => {
    const y = 172, A = 30, B = 300, k = (B - A) / 1.5, C = A + 1.2 * k, G = A + 0.75 * k, W = 24, Wy = y - 6 - (C - 24) * Math.tan(R(30));
    let b = defs('blA') + defs('blB');
    b += `<rect x="6" y="20" width="18" height="200" fill="#fff" stroke="${GREY}" stroke-width="2"/>` + Array.from({ length: 10 }, (_, i) => ln(6, 30 + i * 20, 24, 40 + i * 20, GREY, 1.4)).join('');
    b += thanh(A, B, y) + `<circle cx="${A}" cy="${y}" r="7" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += ln(C, y - 6, W, Wy, INK, 2.4);
    const u = [(W - C), (Wy - y)], L = Math.hypot(...u);
    b += arr(C, y - 6, C + 70 * u[0] / L, y - 6 + 70 * u[1] / L, 'blB', BLUE, '7 4') + T(C - 52, y - 62, 'T', { c: BLUE, w: 700 });
    b += cung(C, y - 6, 46, 150, 180) + T(C - 60, y - 18, '30°', { a: 'end' });
    b += arr(G, y, G, y + 44, 'blA', RED) + T(G + 14, y + 40, 'P', { c: RED, w: 700 }) + T(G - 16, y + 30, 'G', { w: 700, a: 'end' });
    b += ln(B - 8, y + 6, B - 8, y + 18, INK, 2) + `<rect x="${B - 58}" y="${y + 18}" width="64" height="26" rx="2" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(B - 26, y + 38, '16 N', { a: 'middle' });
    b += T(A + 10, y + 32, 'A', { w: 700 }) + T(C + 8, y - 14, 'C', { w: 700 }) + T(B - 2, y - 14, 'B', { w: 700, a: 'end' });
    return wrap('0 0 320 236', b, cap, 'Thanh gắn bản lề giữ bằng dây xiên');
  },
};
