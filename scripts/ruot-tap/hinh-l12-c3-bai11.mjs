// Hình minh hoạ cho ruột tập VL12 · Chương 3 · Bài 11 Thực hành: đo độ lớn cảm ứng từ bằng cân dòng điện (lesson 12).
// Cùng quy tắc với hinh.mjs: mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ màu.
// Chú thích hình cạnh ô Dự đoán/ô điền không nêu kết luận. Xem thử: node scripts/ruot-tap/l12-c3-bai11.mjs --hinh
import { ve } from './hinh.mjs';
const { t, wrap, INK, RED, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const dot = (x, y, r = 4.5, c = INK) => `<circle cx="${x}" cy="${y}" r="${r}" fill="${c}"/>`;
const rect = (x, y, w, h, fill = '#fff') => `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${fill}" stroke="${INK}" stroke-width="${SW}"/>`;
const head = (x, y, dir = 'r', c = INK) => (dir === 'r' ? `<path d="M${x},${y} l-10,-5 v10 z" fill="${c}"/>` : dir === 'u' ? `<path d="M${x},${y} l-5,10 h10 z" fill="${c}"/>` : `<path d="M${x},${y} l10,-5 v10 z" fill="${c}"/>`);

export const hinhL12c3b11 = {
  // Bố trí cân dòng điện. tua = true: chân giá đứng đặt lên chính đĩa cân (lỗi).
  soDo: (cap = 'Cân dòng điện: nam châm chữ U trên đĩa cân, khung dây treo trên giá đứng riêng.', tua = false) => {
    const px = tua ? 268 : 32;
    let b = '';
    b += ln(10, 190, 310, 190, GREY, 2.4);                                   // mặt bàn
    b += rect(140, 160, 160, 30) + T(220, 184, '0,00 g', { a: 'middle', w: 700, size: 20 }); // thân cân + số chỉ
    b += ln(146, 156, 292, 156, INK, 5);                                      // đĩa cân
    // giá đứng
    b += tua ? ln(px, 156, px, 28, INK, 5) : ln(px, 190, px, 28, INK, 5);
    b += ln(px, 28, 205, 28, INK, 5);
    b += ln(205, 28, 205, 114);                                               // khung (nhìn nghiêng)
    // nam châm U
    b += rect(150, 138, 108, 18) + rect(150, 98, 24, 40) + rect(236, 98, 22, 40);
    b += T(162, 125, 'N', { a: 'middle', w: 700 }) + T(247, 125, 'S', { a: 'middle', w: 700 });
    // cạnh dây dưới trong khe
    b += `<circle cx="205" cy="120" r="8" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + dot(205, 120, 3);
    b += T(194, 72, `dây dài ${gk('l')}`, { a: 'end' }) + ln(180, 78, 198, 112, GREY, 2, '4 3');
    // nguồn + ampe kế (nối vào khung)
    b += rect(44, 94, 96, 52) + T(92, 117, 'nguồn', { a: 'middle' }) + T(92, 138, '+ ampe kế', { a: 'middle' });
    b += ln(92, 94, 92, 28);
    // nhãn
    b += tua ? T(px + 8, 64, 'giá') + T(px + 8, 86, 'đứng') : T(px + 8, 176, 'giá riêng');
    b += T(300, 150, 'cân', { a: 'end', size: 20 });
    return wrap('0 0 320 200', b, cap, tua ? 'Chân giá đứng của khung đặt lên đĩa cân cùng nam châm' : 'Sơ đồ bố trí cân dòng điện');
  },
  // Dây hợp với đường sức góc θ (nhìn từ trên xuống)
  goc: (cap = 'Nhìn từ trên xuống: đường sức (mũi tên) và dây cùng nằm trên mặt giấy.') => {
    let b = '';
    for (const y of [34, 70, 120, 156]) b += ln(24, y, 292, y, GREY, 2.4) + head(292, y, 'r', GREY);
    b += T(24, 24, `${gk('B')}`, { w: 700 });
    b += ln(125, 156, 195, 34, INK, 5.5) + T(204, 56, `dây dài ${gk('l')}`, {});
    b += `<path d="M205,95 A44,44 0 0 0 188,67" fill="none" stroke="${RED}" stroke-width="3"/>`;
    b += T(214, 80, `${gk('θ')}`, { c: RED, w: 700 }) + dot(160, 95, 4);
    return wrap('0 0 320 186', b, cap, 'Dây nghiêng góc θ so với đường sức từ');
  },
  // Lưới vẽ đồ thị Δm–I: I 0–5,0 A (vạch 1 A, lưới mịn 0,2 A); Δm 0–3,5 g (vạch 0,5 g, lưới mịn 0,1 g)
  luoi: (cap = 'Vẽ đường thẳng đi qua các điểm đo, nét đặc; lấy hai điểm A, B nằm trên đường (không nhất thiết là điểm đo).') => {
    const X0 = 62, Y0 = 296, W = 400, H = 245;   // 7 đơn vị/0,1 g → 3,5 g
    let b = '';
    for (let i = 0; i <= 25; i++) b += ln(X0 + i * 16, Y0, X0 + i * 16, Y0 - H, '#d3dbec', i % 5 === 0 ? 1.1 : .5);
    for (let j = 0; j <= 35; j++) b += ln(X0, Y0 - j * 7, X0 + W, Y0 - j * 7, '#d3dbec', j % 5 === 0 ? 1.1 : .5);
    b += `<rect x="${X0}" y="${Y0 - H}" width="${W}" height="${H}" fill="none" stroke="${INK}" stroke-width="2.2"/>`;
    for (let i = 0; i <= 5; i++) b += ln(X0 + i * 80, Y0, X0 + i * 80, Y0 + 8, INK, 2.2) + T(X0 + i * 80, Y0 + 28, `${i}`, { a: 'middle', size: 16 });
    for (let j = 0; j <= 7; j++) b += ln(X0 - 8, Y0 - j * 35, X0, Y0 - j * 35, INK, 2.2) + T(X0 - 12, Y0 - j * 35 + 6, j === 0 ? '0' : `${Math.floor(j / 2)},${j % 2 ? 5 : 0}`, { a: 'end', size: 16 });
    b += T(X0 + W, Y0 + 52, `${gk('I')} (A)`, { a: 'end', size: 18, w: 700 }) + T(8, Y0 - H - 14, `${gk('Δ')}${gk('m')} (g)`, { size: 18, w: 700 });
    return wrap('0 0 480 360', b, cap, 'Lưới vẽ đồ thị Δm theo I');
  },
  // Bài tương tự · so hai đường Δm–I (không số)
  haiDuong: (cap = 'Hai nam châm, cùng một khung dây.') => {
    const x0 = 56, y0 = 150, xe = 300, ye = 18;
    let b = ln(x0, y0, xe, y0) + ln(x0, y0, x0, ye) + `<path d="M${xe},${y0} l-9,-5 v10 z" fill="${INK}"/><path d="M${x0},${ye} l-5,9 h10 z" fill="${INK}"/>`;
    b += T(xe, y0 + 24, `${gk('I')} (A)`, { a: 'end' }) + T(x0 + 10, ye + 8, `${gk('Δ')}${gk('m')} (g)`);
    b += ln(x0, y0, 258, 44, INK, SW) + T(262, 50, '(1)', { w: 700 });
    b += ln(x0, y0, 276, 96, INK, SW, '8 5') + T(279, 108, '(2)', { w: 700 });
    return wrap('0 0 320 186', b, cap, 'Hai đường thẳng Δm theo I cùng đi qua gốc toạ độ');
  },
};
