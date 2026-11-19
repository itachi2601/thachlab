// Hình minh hoạ cho ruột tập VL12 · Bài 7 Phương trình trạng thái của khí lí tưởng (lesson 8). Cùng quy tắc với hinh.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh. Xem thử: node scripts/ruot-tap/l12-bai7.mjs --hinh (chụp vào out/hinh-l12-bai7/).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
const sp = (s) => `<tspan font-size="14" dy="-8">${s}</tspan><tspan dy="8"> </tspan>`;
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const arr = (x1, y1, x2, y2, id, c = INK, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${SW}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const dot = (x, y, r = 5, c = INK) => `<circle cx="${x}" cy="${y}" r="${r}" fill="${c}"/>`;
// Trục toạ độ p–T: gốc (ox, oy), dài (w, h); nhãn trục p (đứng) và T (ngang)
const truc = (id, ox, oy, w, h, ny = 'p', nx = 'T (K)') => defs(id) + arr(ox, oy, ox, oy - h, id) + arr(ox, oy, ox + w, oy, id)
  + T(ox - 8, oy - h + 8, ny, { a: 'end', w: 700 }) + T(ox + w, oy + 26, nx, { a: 'end', w: 700 }) + T(ox - 6, oy + 22, 'O', { a: 'end' });
// Đồng hồ áp suất tròn có kim, nhãn ở giữa
const dongHo = (x, y, r, goc, nhan) => `<circle cx="${x}" cy="${y}" r="${r}" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
  + ln(x, y, x + r * .75 * Math.cos(goc), y - r * .75 * Math.sin(goc), RED, 3) + dot(x, y, 3.5)
  + T(x, y + r * .62, nhan, { a: 'middle', w: 700, size: 20 });
// Bình khí (thân bo tròn) + cổ + đồng hồ trên đỉnh
const binh = (x, y, w, h, nhan = '') => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${w * .3}" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
  + `<rect x="${x + w / 2 - 7}" y="${y - 14}" width="14" height="14" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
  + (nhan ? T(x + w / 2, y + h / 2 + 7, nhan, { a: 'middle', w: 700 }) : '');
// Mặt trời
const nang = (x, y, r = 14) => `<circle cx="${x}" cy="${y}" r="${r}" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
  + Array.from({ length: 8 }, (_, i) => { const a = i * Math.PI / 4; return ln(x + (r + 4) * Math.cos(a), y + (r + 4) * Math.sin(a), x + (r + 12) * Math.cos(a), y + (r + 12) * Math.sin(a), INK, 2.2); }).join('');
// Xi lanh nằm ngang có pittông: cột khí dài L (đơn vị viewBox), ghi chữ trong cột khí
const xiLanh = (x, y, L, nhan, cot = 160) => `<path d="M${x + cot},${y} L${x},${y} L${x},${y + 56} L${x + cot},${y + 56}" fill="none" stroke="${INK}" stroke-width="${SW}"/>`
  + `<rect x="${x + L}" y="${y + 3}" width="10" height="50" fill="${GREY}"/>` + ln(x + L + 10, y + 28, x + cot + 30, y + 28, INK, 4)
  + T(x + L / 2, y + 35, nhan, { a: 'middle', w: 700 });
// Thân bình chứa phân tử (dấu chấm), số chấm tượng trưng lượng khí
const binhHat = (x, y, w, h, k, seed = 1) => {
  let s = seed, b = `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="12" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
  for (let i = 0; i < k; i++) { s = (s * 9301 + 49297) % 233280; const u = s / 233280; s = (s * 9301 + 49297) % 233280; const v = s / 233280; b += dot(x + 10 + u * (w - 20), y + 10 + v * (h - 20), 3.4, BLUE); }
  return b;
};

export const hinhL12b7 = {
  // ===== Trang 1 · Dự đoán: bình khí nén ngoài nắng =====
  binhNang: (cap = 'Bình kín để ngoài sân từ sáng tới trưa.') => {
    const L = { size: 24, a: 'middle' };
    let b = binh(40, 76, 70, 110) + dongHo(75, 38, 24, Math.PI * .62, '') + T(75, 214, 'sáng 27 °C', L) + T(75, 242, '5,0 bar', { ...L, w: 700 });
    b += binh(190, 76, 70, 110) + `<circle cx="225" cy="38" r="24" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(225, 47, '?', { ...L, w: 700, c: RED, size: 26 })
      + T(225, 214, 'trưa 47 °C', L) + T(225, 242, '? bar', { ...L, w: 700, c: RED });
    b += nang(280, 24, 10);
    return wrap('0 0 300 252', b, cap, 'Bình khí nén mini buổi sáng và giữa trưa');
  },
  // ===== Trang 2 · Suy ra phương trình trạng thái qua trạng thái trung gian =====
  trungGian: (cap = 'Hai bước biến đổi: mỗi bước giữ một thông số.') => {
    const o = (x, s1, s2, s3, nh) => `<rect x="${x}" y="40" width="82" height="92" rx="6" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
      + T(x + 41, 28, nh, { a: 'middle', w: 700 }) + T(x + 41, 66, s1, { a: 'middle' }) + T(x + 41, 94, s2, { a: 'middle' }) + T(x + 41, 122, s3, { a: 'middle' });
    let b = defs('tg1') + o(4, `p${sb('1')}`, `V${sb('1')}`, `T${sb('1')}`, '(1)') + o(120, `p${sb('2')}`, 'V’', `T${sb('1')}`, '(1’)') + o(236, `p${sb('2')}`, `V${sb('2')}`, `T${sb('2')}`, '(2)');
    b += arr(88, 86, 116, 86, 'tg1') + arr(204, 86, 232, 86, 'tg1');
    b += T(102, 160, 'giữ T', { a: 'middle' }) + T(218, 160, 'giữ p', { a: 'middle' });
    return wrap('0 0 322 170', b, cap, 'Trạng thái 1 qua trạng thái trung gian 1’ tới trạng thái 2');
  },
  bongBan: (cap = 'Bóng bàn bẹp (chưa nứt) thả vào nước khoảng 80 °C.') => {
    let b = `<path d="M60,60 L72,200 L228,200 L240,60" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += ln(64, 96, 236, 96, BLUE, 2.2, '8 5');
    b += `<path d="M150,86 m-34,0 a34,34 0 1,0 68,0 a34,34 0 0,0 -20,-31 q-10,18 -28,4 a34,34 0 0,0 -20,27 z" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += [90, 130, 170, 210].map((x) => `<path d="M${x},44 q-6,-10 0,-20 q6,-10 0,-20" fill="none" stroke="${GREY}" stroke-width="2"/>`).join('');
    b += T(150, 170, 'nước nóng', { a: 'middle' });
    return wrap('0 0 300 210', b, cap, 'Quả bóng bàn bẹp trong cốc nước nóng');
  },
  // ===== Trang 3 · Đường đẳng tích =====
  dangTich: (cap = 'Hai đường đẳng tích của cùng một lượng khí; nét đứt: phần kéo dài.') => {
    const ox = 46, oy = 200;
    let b = truc('dt', ox, oy, 240, 186);
    b += ln(ox, oy, ox + 46, oy - 64, INK, 2.2, '6 5') + ln(ox + 46, oy - 64, ox + 120, oy - 168, INK, SW);
    b += ln(ox, oy, ox + 92, oy - 52, BLUE, 2.2, '6 5') + ln(ox + 92, oy - 52, ox + 226, oy - 128, BLUE, SW);
    b += T(ox + 124, oy - 160, `V${sb('a')}`, { w: 700 }) + T(ox + 214, oy - 140, `V${sb('b')}`, { w: 700, c: BLUE, a: 'end' });
    b += ln(ox + 100, oy, ox + 100, oy - 150, GREY, 1.8, '3 4') + T(ox + 100, oy + 24, 'T', { a: 'middle' });
    return wrap('0 0 300 232', b, cap, 'Đồ thị áp suất theo nhiệt độ tuyệt đối với hai đường đẳng tích');
  },
  // ===== Trang 4 · Clapeyron – Mendeleev và bẫy Celsius =====
  molKhi: (cap = '1 mol khí ở 0 °C, 1 atm.') => {
    let b = `<path d="M40,80 L180,80 L180,210 L40,210 Z M40,80 L90,40 L230,40 L180,80 M230,40 L230,170 L180,210" fill="#fff" stroke="${INK}" stroke-width="${SW}" stroke-linejoin="round"/>`;
    b += binhHat(52, 92, 116, 106, 14, 3).replace(/<rect[^>]*\/>/, '');
    b += T(110, 236, '22,4 lít', { a: 'middle', w: 700 });
    return wrap('0 0 270 246', b, cap, 'Khối khí một mol ở điều kiện tiêu chuẩn');
  },
  haiThang: (cap = 'Cùng ba mức nóng, đọc trên hai thang.') => {
    // cùng một ống: 47 °C ↔ 320 K (y 50), 27 °C ↔ 300 K (y 80), 0 °C ↔ 273 K (y 120,5); 1,5 đơn vị/độ
    const L = { size: 24 };
    const nk = (x, nh, v) => `<rect x="${x - 9}" y="34" width="18" height="140" rx="9" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
      + `<circle cx="${x}" cy="186" r="15" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(x, 22, nh, { a: 'middle', w: 700, size: 22 })
      + [[50, v[0]], [80, v[1]], [120.5, v[2]]].map(([y, s]) => ln(x + 10, y, x + 22, y) + T(x + 26, y + 8, s, L)).join('');
    let b = nk(50, 'thang °C', ['47', '27', '0']) + nk(200, 'thang K', ['320', '300', '273']);
    b += ln(96, 120.5, 188, 120.5, GREY, 1.6, '4 4');
    b += T(150, 228, '0 K (−273 °C) ở rất xa', { a: 'middle', size: 22 }) + T(150, 254, 'bên dưới ống', { a: 'middle', size: 22 });
    return wrap('0 0 300 262', b, cap, 'Nhiệt kế thang Celsius và thang Kelvin');
  },
  // ===== Trang 5 · Bài toán mẫu: thân bơm xe đạp =====
  bom: (cap = 'Bịt đầu vòi, nén nhanh pittông.') => {
    let b = defs('bm');
    b += xiLanh(10, 10, 160, '200 cm³', 190) + T(10, 94, `27 °C · 1,0·10${sp('5')}Pa`, { size: 22 });
    b += arr(120, 104, 120, 124, 'bm');
    b += xiLanh(10, 132, 40, '', 190) + T(10, 216, '40 cm³ · 87 °C ·', { size: 22 }) + T(168, 216, 'p = ?', { c: RED, w: 700, size: 22 });
    return wrap('0 0 240 226', b, cap, 'Thân bơm xe đạp trước và sau khi nén');
  },
  // ===== Bài tập mẫu =====
  doThiD3: () => {
    const ox = 40, oy = 124, sx = 0.44, sy = 15; // T(K)·sx, p(10^5 Pa)·sy
    let b = defs('d3') + arr(ox, oy, ox, oy - 112, 'd3') + arr(ox, oy, ox + 256, oy, 'd3')
      + T(ox + 18, oy - 100, `p (10${sp('5')}Pa)`, { w: 700 }) + T(ox + 256, oy - 10, 'T (K)', { a: 'end', w: 700 }) + T(ox - 6, oy + 22, 'O', { a: 'end' });
    const P = (Tk, p) => [ox + Tk * sx, oy - p * sy];
    const M = P(300, 3), N = P(500, 5), Q = P(300, 1.5), Q2 = P(540, 2.7);
    b += ln(ox, oy, ...M, INK, 2.2, '6 5') + ln(...M, ...N, INK, SW) + ln(ox, oy, ...Q2, BLUE, 2.2, '6 5');
    b += ln(M[0], oy, M[0], M[1], GREY, 1.6, '3 4') + ln(ox, M[1], M[0], M[1], GREY, 1.6, '3 4') + ln(ox, Q[1], Q[0], Q[1], GREY, 1.6, '3 4') + ln(N[0], oy, N[0], N[1], GREY, 1.6, '3 4');
    b += dot(...M) + dot(...N) + dot(...Q, 5, BLUE);
    b += T(M[0] - 8, M[1] - 8, 'M', { w: 700, a: 'end' }) + T(N[0] + 8, N[1] + 8, 'N', { w: 700 }) + T(N[0] - 10, N[1] - 4, 'p = ?', { c: RED, w: 700, a: 'end' }) + T(Q[0] + 12, Q[1] + 22, 'Q', { w: 700, c: BLUE });
    b += T(P(420, 4.2)[0] - 16, P(420, 4.2)[1] - 4, '(1)', { w: 700, a: 'end' }) + T(P(400, 2)[0] - 4, P(400, 2)[1] - 10, '(2)', { w: 700, c: BLUE, a: 'end' });
    b += T(M[0], oy + 22, '300', { a: 'middle' }) + T(N[0], oy + 22, '500', { a: 'middle' }) + T(ox - 6, M[1] + 7, '3,0', { a: 'end' }) + T(ox - 6, Q[1] + 7, '1,5', { a: 'end' });
    return wrap('0 0 300 150', b, '', 'Đồ thị p–T của hai đường đẳng tích với các điểm M, N, Q');
  },
  haiLanD5: (cap = 'Lúc mới nạp và lúc còn lại: cùng bình 8,0 lít.') => {
    let b = binhHat(14, 30, 110, 150, 26, 7) + binhHat(170, 30, 110, 150, 9, 11);
    b += T(69, 20, 'mới nạp', { a: 'middle', w: 700 }) + T(225, 20, 'còn lại', { a: 'middle', w: 700 });
    b += T(69, 206, '27 °C', { a: 'middle' }) + T(69, 230, `4,5·10${sp('6')}Pa`, { a: 'middle' }) + T(225, 206, '17 °C', { a: 'middle' }) + T(225, 230, `1,5·10${sp('6')}Pa`, { a: 'middle' });
    return wrap('0 0 294 240', b, cap, 'Bình oxygen lúc mới nạp và lúc còn lại');
  },
};
