// Hình minh hoạ cho ruột tập VL12 · Chương 3 · Bài 10 Lực từ. Cảm ứng từ (lesson 11). Cùng quy tắc với hinh.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh (hình bài tập để "?" ở chỗ HS phải tìm chiều).
// Kí hiệu ⊙ ⊗ vẽ bằng vòng tròn + chấm/chéo (không dùng ký tự Unicode → không rơi về font hệ thống).
// Xem thử: node scripts/ruot-tap/l12-c3-bai10.mjs --hinh (chụp vào out/hinh-l12-c3-bai10/).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
// chữ Hi Lạp: Source Sans 3 chỉ nạp latin/vietnamese → lấy từ KaTeX_Math
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const arr = (x1, y1, x2, y2, id, c = INK, dash = '', w = SW) =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
// ⊙ (ra) và ⊗ (vào): r nhỏ cho lưới đường sức, r lớn cho dây cắt ngang
const ra = (x, y, r = 7, c = GREY) => `<circle cx="${x}" cy="${y}" r="${r}" fill="#fff" stroke="${c}" stroke-width="1.8"/><circle cx="${x}" cy="${y}" r="${r * .28}" fill="${c}"/>`;
const vao = (x, y, r = 7, c = GREY) => { const d = r * .62; return `<circle cx="${x}" cy="${y}" r="${r}" fill="#fff" stroke="${c}" stroke-width="1.8"/>`
  + ln(x - d, y - d, x + d, y + d, c, 1.8) + ln(x - d, y + d, x + d, y - d, c, 1.8); };
const luoi = (x0, y0, nx, ny, d, kieu) => { let s = ''; for (let i = 0; i < nx; i++) for (let j = 0; j < ny; j++) s += kieu(x0 + i * d, y0 + j * d); return s; };
const hoi = (x, y, c = RED) => T(x, y, '?', { c, w: 700, size: 26, a: 'middle' });
const cuc = (x, y, w, h, s) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="3" fill="${s === 'N' ? '#e9edf6' : '#fff'}" stroke="${INK}" stroke-width="${SW}"/>`
  + T(x + w / 2, y + h / 2 + 8, s, { a: 'middle', w: 700, size: 24 });
const goc = (cx, cy, r, a1, a2, nhan, nx, ny) => {
  const p = (a) => [cx + r * Math.cos(a * Math.PI / 180), cy - r * Math.sin(a * Math.PI / 180)];
  const [x1, y1] = p(a1), [x2, y2] = p(a2);
  return `<path d="M${x1.toFixed(1)},${y1.toFixed(1)} A${r},${r} 0 0 0 ${x2.toFixed(1)},${y2.toFixed(1)}" fill="none" stroke="${INK}" stroke-width="2"/>` + T(nx, ny, nhan);
};
// Đoạn dây MN nằm ngang, dòng điện mũi tên đỏ giữa dây
const dayMN = (x1, x2, y, id, chieu = 1, nhan = true) => ln(x1, y, x2, y, INK, 4)
  + (chieu ? arr(chieu > 0 ? (x1 + x2) / 2 - 22 : (x1 + x2) / 2 + 22, y - 14, chieu > 0 ? (x1 + x2) / 2 + 22 : (x1 + x2) / 2 - 22, y - 14, id, RED) + T((x1 + x2) / 2, y - 24, 'I', { c: RED, w: 700, a: 'middle' }) : '')
  + (nhan ? T(x1 - 6, y + 7, 'M', { w: 700, a: 'end' }) + T(x2 + 6, y + 7, 'N', { w: 700 }) : '');

export const hinhL12c3b10 = {
  // ===== Trang 1 =====
  // Dự đoán: dây dọc đường sức giữa hai cực — không vẽ lực, không gợi ý
  kheDuDoan: (cap = 'Dây dọc đường sức, có dòng I.') => {
    let b = defs('kd1') + defs('kd2');
    b += cuc(40, 4, 200, 30, 'N') + cuc(40, 136, 200, 30, 'S');
    [70, 110, 170, 210].forEach((x) => { b += arr(x, 40, x, 128, 'kd1', GREY, '6 5', 2); });
    b += ln(140, 44, 140, 126, INK, 5) + arr(158, 110, 158, 62, 'kd2', RED) + T(166, 92, 'I', { c: RED, w: 700 });
    b += T(248, 90, 'B', { w: 700 }) + arr(262, 70, 262, 110, 'kd1', GREY, '', 2);
    return wrap('0 0 290 170', b, cap, 'Đoạn dây thẳng đứng giữa hai cực nam châm, đường sức hướng xuống');
  },
  // Thí nghiệm: dây nhôm treo giữa hai cực (đường sức thẳng đứng), nối nguồn qua khoá K
  dayTreo: (cap = 'Cực N trên, S dưới.') => {
    let b = defs('dt1');
    b += ln(30, 12, 270, 12, INK, 5) + ln(70, 12, 70, 104, INK, 1.8) + ln(230, 12, 230, 104, INK, 1.8);
    b += cuc(110, 30, 80, 30, 'N') + cuc(110, 150, 80, 30, 'S');
    [130, 170].forEach((x) => { b += arr(x, 66, x, 92, 'dt1', GREY, '5 4', 2) + arr(x, 116, x, 144, 'dt1', GREY, '5 4', 2); });
    b += ln(60, 104, 240, 104, INK, 5);
    b += ln(60, 104, 30, 104, INK, 2) + ln(30, 104, 30, 196) + ln(240, 104, 270, 104, INK, 2) + ln(270, 104, 270, 196);
    b += ln(30, 196, 128, 196) + ln(128, 184, 128, 208, INK, 3) + ln(140, 190, 140, 202, INK, 5) + ln(140, 196, 186, 196);
    b += ln(186, 196, 214, 184, INK, 2.4) + ln(218, 196, 270, 196) + T(200, 178, 'K', { a: 'middle', w: 700 });
    b += T(134, 228, 'nguồn 3–6 V', { a: 'middle' });
    return wrap('0 0 300 236', b, cap, 'Dây nhôm treo bằng hai dây mảnh giữa hai cực nam châm, nối nguồn');
  },
  // ===== Trang 2 =====
  // Cân dòng điện: nam châm trên cân, dây MN (cắt ngang) kẹp trên giá riêng nằm trong khe N → S
  canDong: (cap = 'MN cắt ngang, dòng chạy vào trang.') => {
    let b = defs('cd1');
    b += `<rect x="20" y="176" width="250" height="34" rx="5" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(34, 199, 'cân');
    b += `<rect x="150" y="182" width="108" height="22" rx="3" fill="#fff" stroke="${INK}" stroke-width="2"/>` + T(250, 200, '…, … g', { a: 'end', w: 700 });
    b += `<path d="M40,176 L40,96 L86,96 L86,150 L194,150 L194,96 L240,96 L240,176 Z" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += T(63, 132, 'N', { a: 'middle', w: 700, size: 24 }) + T(217, 132, 'S', { a: 'middle', w: 700, size: 24 });
    b += arr(92, 108, 186, 108, 'cd1', GREY, '6 5', 2) + arr(92, 136, 120, 136, 'cd1', GREY, '6 5', 2) + arr(160, 136, 186, 136, 'cd1', GREY, '6 5', 2);
    b += ln(140, 6, 140, 110, GREY, 6) + ln(100, 6, 180, 6, INK, 4) + vao(140, 124, 12, INK) + T(140, 166, 'MN', { a: 'middle', w: 700 });
    b += T(250, 60, 'giá', { a: 'middle' }) + ln(180, 6, 250, 6, INK, 4) + ln(250, 6, 250, 40, INK, 4);
    return wrap('0 0 290 216', b, cap, 'Cân dòng điện: nam châm chữ U đặt trên cân, dây MN nằm trong khe');
  },
  // ===== Trang 3 =====
  // Ngẫu lực từ: khung nhìn dọc trục quay, mặt khung song song B
  nguLuc: (cap = 'Khung nhìn dọc trục quay; mặt khung song song đường sức.') => {
    let b = defs('ng1') + defs('ng2');
    [30, 200].forEach((y) => { b += arr(10, y, 290, y, 'ng1', GREY, '6 5', 2); });
    b += T(282, 22, 'B', { w: 700, a: 'end' });
    b += ln(70, 115, 230, 115, INK, 3) + `<circle cx="150" cy="115" r="5" fill="${INK}"/>` + T(150, 146, 'trục', { a: 'middle' });
    b += ra(70, 115, 13, INK) + vao(230, 115, 13, INK);
    b += arr(70, 98, 70, 46, 'ng2', RED) + T(82, 62, 'F', { c: RED, w: 700 });
    b += arr(230, 132, 230, 184, 'ng2', RED) + T(218, 178, 'F', { c: RED, w: 700, a: 'end' });
    return wrap('0 0 300 214', b, cap, 'Hai cạnh của khung dây chịu hai lực từ tạo ngẫu lực');
  },
  // Nắm tay phải: dây thẳng, đường sức chưa có chiều — HS tự vẽ mũi tên
  dayThang: (cap = 'Tự vẽ chiều đường sức (nắm tay phải).') => {
    let b = defs('dth');
    b += ln(110, 10, 110, 200, INK, 5) + arr(130, 170, 130, 120, 'dth', RED) + T(138, 152, 'I', { c: RED, w: 700 });
    [[34, 10], [64, 18], [92, 26]].forEach(([rx, ry]) => {
      b += `<ellipse cx="110" cy="96" rx="${rx}" ry="${ry}" fill="none" stroke="${GREY}" stroke-width="2.2"${rx === 64 ? ' stroke-dasharray="6 4"' : ''}/>`;
    });
    b += hoi(202, 104) + hoi(18, 104);
    return wrap('0 0 220 206', b, cap, 'Dây thẳng mang dòng điện và các đường sức tròn quanh dây');
  },
  // Lực Lorentz: hạt dương trong B hướng vào trang, quỹ đạo tròn
  lorentz: (cap = 'Hạt dương, B hướng vào trang: v tiếp tuyến, f hướng vào tâm.') => {
    let b = defs('lz1') + defs('lz2');
    b += luoi(30, 24, 6, 5, 44, (x, y) => (y === 24 && x > 40 && x < 240) || (x === 162 && y === 68) ? '' : vao(x, y, 6));
    b += `<circle cx="140" cy="112" r="72" fill="none" stroke="${INK}" stroke-width="2.4" stroke-dasharray="7 5"/>`;
    b += `<circle cx="140" cy="40" r="9" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(140, 47, '+', { a: 'middle', w: 700 });
    b += arr(128, 40, 66, 40, 'lz1', BLUE, '7 4') + T(62, 30, 'v', { c: BLUE, w: 700, a: 'end' });
    b += arr(140, 52, 140, 100, 'lz2', RED) + T(148, 90, 'f', { c: RED, w: 700 });
    return wrap('0 0 280 204', b, cap, 'Hạt mang điện dương chuyển động tròn đều trong từ trường đều');
  },
  // ===== Trang 4 · Bẫy 1 =====
  vuongSong: (cap = '(a) dây vuông góc đường sức · (b) dây song song đường sức.') => {
    let b = defs('vs1') + defs('vs2');
    [20, 60, 100].forEach((y) => { b += arr(8, y + 20, 128, y + 20, 'vs1', GREY, '6 5', 2) + arr(162, y + 20, 292, y + 20, 'vs1', GREY, '6 5', 2); });
    b += ln(66, 22, 66, 138, INK, 5) + arr(80, 110, 80, 64, 'vs2', RED);
    b += ln(176, 98, 280, 98, INK, 5) + arr(206, 86, 250, 86, 'vs2', RED);
    b += T(66, 166, '(a)', { a: 'middle', w: 700 }) + T(228, 166, '(b)', { a: 'middle', w: 700 });
    return wrap('0 0 300 176', b, cap, 'Dây vuông góc và dây song song với đường sức');
  },
  // ===== Trang 5 · Bài toán mẫu =====
  dayXien: (cap = 'Dây xiên 30° so với đường sức.') => {
    let b = defs('dx1') + defs('dx2');
    [14, 128].forEach((y) => { b += arr(8, y, 292, y, 'dx1', GREY, '6 5', 2); });
    b += T(284, 36, 'B', { w: 700, a: 'end' });
    b += ln(60, 112, 226, 16, INK, 5) + arr(130, 96, 182, 66, 'dx2', RED) + T(170, 98, 'I', { c: RED, w: 700 });
    b += ln(60, 112, 150, 112, GREY, 2, '4 4') + goc(60, 112, 50, 0, 30, `${gk('α')}`, 116, 106);
    return wrap('0 0 300 136', b, cap, 'Đoạn dây xiên góc với đường sức từ');
  },
  // ===== Bài tập mẫu =====
  // Dạng 2: ba ô a), b), c) — chiều chưa biết đánh "?"
  d2: (cap = 'Mỗi ô: biết hai chiều, tìm chiều “?”.') => {
    let b = defs('d2a') + defs('d2b');
    b += ln(110, 6, 110, 176, GREY, 1.5, '3 4') + ln(220, 6, 220, 176, GREY, 1.5, '3 4');
    // a) dây thẳng đứng, I lên, F sang phải, B = ?
    b += T(4, 24, 'a)', { w: 700 }) + ln(50, 30, 50, 160, INK, 5) + arr(32, 130, 32, 80, 'd2a', RED) + T(24, 112, 'I', { c: RED, w: 700, a: 'end' });
    b += arr(58, 90, 100, 90, 'd2b', BLUE, '7 4') + T(80, 78, 'F', { c: BLUE, w: 700, a: 'middle' }) + T(80, 140, 'B ?', { c: RED, w: 700, a: 'middle' });
    // b) dây ⊥ trang giữa N (trái) S (phải), F xuống, I = ?
    b += T(114, 24, 'b)', { w: 700 }) + cuc(118, 52, 26, 56, 'N') + cuc(186, 52, 26, 56, 'S');
    b += `<circle cx="165" cy="80" r="13" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(165, 87, '?', { c: RED, w: 700, a: 'middle' });
    b += arr(165, 96, 165, 146, 'd2b', BLUE, '7 4') + T(176, 140, 'F', { c: BLUE, w: 700 }) + T(165, 172, 'I ?', { c: RED, w: 700, a: 'middle' });
    // c) MN ngang, B xuống, F vào trang, I = ?
    b += T(224, 24, 'c)', { w: 700 }) + arr(256, 32, 256, 66, 'd2a', GREY, '5 4', 2) + arr(306, 32, 306, 66, 'd2a', GREY, '5 4', 2) + T(281, 54, 'B', { w: 700, a: 'middle' });
    b += ln(240, 100, 322, 100, INK, 5) + T(240, 128, 'M', { w: 700 }) + T(322, 128, 'N', { w: 700, a: 'end' });
    b += vao(281, 132, 10, BLUE) + T(296, 139, 'F', { c: BLUE, w: 700 }) + T(281, 172, 'I ?', { c: RED, w: 700, a: 'middle' });
    return wrap('0 0 330 180', b, cap, 'Ba trường hợp tìm chiều chưa biết bằng quy tắc bàn tay trái');
  },
  // Dạng 5: dây MN treo hai sợi chỉ trong B hướng ra
  d5: (cap = 'Lực từ hướng nào?') => {
    let b = defs('d5a');
    b += ln(40, 8, 250, 8, INK, 5) + ln(70, 8, 70, 84, INK, 1.8) + ln(220, 8, 220, 84, INK, 1.8);
    b += luoi(30, 36, 6, 1, 46, (x, y) => ra(x, y, 7)) + luoi(30, 116, 6, 1, 46, (x, y) => (Math.abs(x - 145) < 30 ? '' : ra(x, y, 7)));
    b += ln(60, 84, 230, 84, INK, 5) + T(54, 91, 'M', { w: 700, a: 'end' }) + T(236, 91, 'N', { w: 700 });
    b += arr(145, 92, 145, 138, 'd5a', BLUE, '7 4') + T(130, 136, 'P', { c: BLUE, w: 700, a: 'end' });
    return wrap('0 0 290 146', b, cap, 'Đoạn dây treo nằm ngang bằng hai sợi chỉ trong từ trường');
  },
  // Dạng 6: khung nhìn dọc AB, mặt khung song song B, chiều dòng ở AB ra, CD vào
  d6: (cap = 'Nhìn dọc cạnh AB.') => {
    let b = defs('d6a');
    [16, 134].forEach((y) => { b += arr(10, y, 290, y, 'd6a', GREY, '6 5', 2); });
    b += T(282, 124, 'B', { w: 700, a: 'end' });
    b += ln(70, 76, 230, 76, INK, 3) + ra(70, 76, 13, INK) + vao(230, 76, 13, INK);
    b += T(70, 114, 'AB', { a: 'middle', w: 700 }) + T(230, 114, 'CD', { a: 'middle', w: 700 }) + T(150, 66, 'BC', { a: 'middle' });
    b += hoi(100, 54) + hoi(260, 54);
    return wrap('0 0 300 146', b, cap, 'Khung dây nhìn dọc cạnh AB trong từ trường đều');
  },
};
