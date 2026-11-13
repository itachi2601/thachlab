// Hình minh hoạ cho ruột tập VL10 · Bài 1 Làm quen với Vật lí (lesson 46). Cùng quy tắc với hinh-l10-bai23.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chú thích hình đứng cạnh ô Dự đoán/ô điền không nêu kết luận. Xem thử: node scripts/ruot-tap/l10-bai1.mjs --hinh (chụp vào out/hinh-l10-bai1/).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const arr = (x1, y1, x2, y2, id, c = INK, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${SW}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const circ = (x, y, r, fill = '#fff', c = INK, w = SW) => `<circle cx="${x}" cy="${y}" r="${r}" fill="${fill}" stroke="${c}" stroke-width="${w}"/>`;
const rect = (x, y, w, h, r = 3, fill = '#fff', c = INK, sw = SW) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r}" fill="${fill}" stroke="${c}" stroke-width="${sw}"/>`;
const LIGHT = '#dfe6f4';

// ly/cốc hình thang: đỉnh (x1..x2, y1), đáy (x3..x4, y2)
const coc = (x1, x2, y1, x3, x4, y2, fill = '#fff', w = SW) =>
  `<path d="M${x1},${y1} L${x3},${y2} L${x4},${y2} L${x2},${y1}" fill="${fill}" stroke="${INK}" stroke-width="${w}" stroke-linejoin="round"/>`;
const da = (x, y, s = 20) => `<rect x="${x}" y="${y}" width="${s}" height="${s}" rx="3" fill="#fff" stroke="${BLUE}" stroke-width="2.4"/>`;
const giot = (x, y) => `<path d="M${x},${y - 9} C${x + 8},${y + 1} ${x + 7},${y + 9} ${x},${y + 9} C${x - 7},${y + 9} ${x - 8},${y + 1} ${x},${y - 9} z" fill="#fff" stroke="${BLUE}" stroke-width="2.2"/>`;

export const hinhL10b1 = {
  // Trang 1 · Dự đoán: ấm nước sắp sôi (chỉ cảnh nhìn thấy)
  amNuoc: (cap = 'Ấm nước trên bếp sắp sôi.') => {
    let b = defs('an1');
    b += ln(80, 150, 252, 150, INK, 4);
    b += `<path d="M106,60 L226,60 L236,146 L96,146 z" fill="#fff" stroke="${INK}" stroke-width="${SW}" stroke-linejoin="round"/>`;
    b += `<path d="M236,84 C276,84 276,128 240,128" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<path d="M106,84 L68,66 L60,74 L100,106" fill="#fff" stroke="${INK}" stroke-width="${SW}" stroke-linejoin="round"/>`;
    b += `<path d="M120,60 Q166,36 212,60" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + circ(166, 38, 6);
    b += ln(112, 30, 104, 22, GREY, 2.4) + ln(222, 30, 230, 22, GREY, 2.4) + ln(104, 44, 94, 42, GREY, 2.4) + ln(230, 44, 240, 42, GREY, 2.4);
    b += `<path d="M60,66 C46,52 70,40 54,24" fill="none" stroke="${GREY}" stroke-width="${SW}" stroke-dasharray="6 5"/>`;
    b += `<path d="M48,70 C30,58 52,48 36,34" fill="none" stroke="${GREY}" stroke-width="${SW}" stroke-dasharray="6 5"/>`;
    b += T(126, 112, 'nước', { c: INK });
    b += `<path d="M120,150 q6,-16 12,0 M152,150 q6,-16 12,0 M184,150 q6,-16 12,0" fill="none" stroke="${RED}" stroke-width="${SW}"/>`;
    return wrap('0 0 320 172', b, cap, 'Ấm nước trên bếp, nắp rung, hơi nước phun ra từ vòi');
  },
  // Trang 1 · Thí nghiệm giọt mực: hai cốc, cùng một lúc
  giotMuc: (cap = 'Hai cốc, nhìn cùng một lúc sau khi nhỏ mực.') => {
    let b = '';
    b += coc(24, 140, 40, 40, 124, 140) + coc(180, 296, 40, 196, 280, 140);
    b += `<path d="M30,66 L134,66" stroke="${LIGHT}" stroke-width="2.4"/>`;
    b += circ(82, 80, 14, GREY, INK, 2.4);
    b += `<ellipse cx="238" cy="92" rx="46" ry="34" fill="${GREY}" fill-opacity=".45" stroke="${INK}" stroke-width="2.4" stroke-dasharray="5 4"/>`;
    b += T(82, 30, 'nước lạnh', { a: 'middle' }) + T(238, 30, 'nước nóng', { a: 'middle' });
    b += T(238, 168, '60 °C', { a: 'middle', c: RED });
    return wrap('0 0 320 176', b, cap, 'Mực loang trong hai cốc nước');
  },
  // Trang 2 · Thang vi mô – vĩ mô (đi từ nhỏ đến lớn)
  thang: (cap = 'Năm đối tượng từ nhỏ đến lớn (không theo tỉ lệ).') => {
    let b = defs('th1');
    b += arr(12, 186, 12, 14, 'th1', GREY);
    const L = (y, s) => T(70, y + 6, s);
    // nguyên tử
    b += circ(40, 24, 3.4, INK) + `<ellipse cx="40" cy="24" rx="13" ry="6" fill="none" stroke="${INK}" stroke-width="2"/>` + L(24, 'nguyên tử');
    // phân tử nước
    b += circ(34, 66, 9) + circ(48, 62, 5) + circ(46, 72, 5) + L(66, 'phân tử nước');
    // hạt cát
    b += `<path d="M30,108 L38,100 L50,102 L52,112 L42,116 z" fill="${GREY}" stroke="${INK}" stroke-width="2.4"/>` + L(108, 'hạt cát');
    // người
    b += circ(40, 132, 6) + ln(40, 138, 40, 156, INK, 2.8) + ln(40, 144, 30, 152, INK, 2.8) + ln(40, 144, 50, 152, INK, 2.8) + ln(40, 156, 32, 168, INK, 2.8) + ln(40, 156, 48, 168, INK, 2.8) + L(150, 'người');
    // Trái Đất
    b += circ(42, 190, 14, LIGHT) + `<path d="M30,186 q8,-8 14,0 M36,196 q10,4 14,-4" fill="none" stroke="${INK}" stroke-width="2"/>` + L(190, 'Trái Đất');
    return wrap('0 0 240 210', b, cap, 'Năm đối tượng từ nhỏ đến lớn');
  },
  // Trang 3 · Năm bước, vòng lặp khi không khớp
  nam: (cap = 'Năm bước nghiên cứu; có đường quay lại.') => {
    let b = defs('nb1');
    const ten = ['Thấy', 'Hỏi', 'Đoán', 'Thử', 'Chốt'];
    ten.forEach((s, i) => {
      const y = 8 + i * 44;
      b += rect(8, y, 128, 32, 5, i === 2 ? LIGHT : '#fff') + T(22, y + 23, `${i + 1}`, { w: 700, c: BLUE }) + T(46, y + 23, s, { w: 700 });
      if (i < 4) b += arr(72, y + 32, 72, y + 44, 'nb1');
    });
    // quay lại từ bước 4 về bước 3
    b += `<path d="M136,164 L164,164 L164,106 L142,106" fill="none" stroke="${RED}" stroke-width="${SW}" stroke-dasharray="6 4" marker-end="url(#nb1)"/>`;
    b += T(172, 128, 'không', { c: RED }) + T(172, 150, 'khớp', { c: RED });
    return wrap('0 0 240 228', b, cap, 'Quy trình năm bước nghiên cứu');
  },
  // Trang 3 · Thí nghiệm rơi: bốn vật, cùng thời điểm
  roi: (cap = 'Thả cùng lúc từ cùng độ cao; ảnh chụp cùng một thời điểm (minh hoạ).') => {
    let b = ln(4, 196, 316, 196, INK, 4) + ln(4, 14, 316, 14, GREY, 2.4, '6 4') + T(8, 36, 'độ cao thả', { c: GREY });
    const xs = [44, 122, 200, 278];
    const sach = (x, y) => rect(x - 22, y, 44, 16, 2, LIGHT);
    b += sach(xs[0], 176);
    b += rect(xs[1] - 24, 120, 48, 4, 1, '#fff') + `<path d="M${xs[1] - 24},124 q12,10 24,0 t24,0" fill="none" stroke="${GREY}" stroke-width="2"/>`;
    b += sach(xs[2], 176) + rect(xs[2] - 20, 172, 40, 4, 1, '#fff');
    b += circ(xs[3], 160, 12, GREY, INK, 2.4);
    xs.forEach((x, i) => { b += ln(x, 40, x, i === 1 ? 110 : i === 3 ? 140 : 160, GREY, 1.8, '4 5'); });
    const lab = [['sách'], ['giấy', 'phẳng'], ['giấy', '+ sách'], ['giấy', 'vo']];
    lab.forEach((l, i) => l.forEach((s, j) => { b += T(xs[i], 218 + j * 22, s, { a: 'middle' }); }));
    return wrap('0 0 320 262', b, cap, 'Bốn vật rơi cùng lúc');
  },
  // Trang 4 · Bẫy 1: robot hút bụi đi dọc bốn cạnh ô vuông
  robot: (cap = 'Robot hút bụi đi dọc bốn cạnh ô vuông cạnh 1,5 m.') => {
    let b = defs('rb1');
    b += `<path d="M70,36 L190,36 L190,156 L70,156 z" fill="none" stroke="${GREY}" stroke-width="2.4" stroke-dasharray="6 5"/>`;
    b += arr(76, 156, 76, 100, 'rb1', BLUE) + arr(120, 36, 160, 36, 'rb1', BLUE) + arr(190, 70, 190, 110, 'rb1', BLUE) + arr(170, 156, 130, 156, 'rb1', BLUE);
    [[70, 36], [190, 36], [190, 156], [70, 156]].forEach(([x, y]) => { b += circ(x, y, 7, '#fff', RED, 2.6); });
    b += circ(70, 156, 17, '#fff', INK, SW) + T(70, 163, 'R', { a: 'middle', w: 700 });
    b += T(130, 100, '1,5 m', { a: 'middle' }) + T(230, 100, 'bốn góc rẽ', { c: RED });
    return wrap('0 0 320 176', b, cap, 'Đường đi của robot hút bụi');
  },
  // Trang 5 · Bài toán mẫu: ly nước đá đọng giọt
  lyNuoc: (cap = 'Ly nước đá để ngoài trời nóng vài phút.') => {
    let b = coc(40, 160, 30, 56, 144, 150);
    b += `<path d="M46,64 L154,64" stroke="${BLUE}" stroke-width="2.4"/>`;
    b += da(66, 70, 20) + da(94, 78, 20) + da(118, 66, 18);
    [[34, 70], [28, 94], [36, 120], [166, 72], [172, 98], [160, 124], [64, 164], [136, 164]].forEach(([x, y]) => { b += giot(x, y); });
    b += T(100, 190, 'ly', { a: 'middle' });
    return wrap('0 0 200 196', b, cap, 'Ly nước đá có giọt nước bên ngoài');
  },
  // Dạng 2 (BTM / tương tự): xe đi hết đoạn đường
  xeDuong: (cap = '', dai = '2,4 m') => {
    let b = defs('xd1');
    b += ln(10, 96, 310, 96, INK, 4);
    b += rect(22, 60, 52, 24, 4) + circ(36, 90, 7) + circ(60, 90, 7);
    b += ln(14, 30, 14, 96, INK, 3) + ln(304, 30, 304, 96, INK, 3);
    b += arr(24, 22, 296, 22, 'xd1', BLUE) + T(160, 16, dai, { a: 'middle', c: BLUE });
    b += T(14, 130, 'xuất phát', { a: 'start' }) + T(304, 130, 'đích', { a: 'end' });
    return wrap('0 0 320 142', b, cap, 'Xe đồ chơi chạy trên đoạn đường thẳng');
  },
  // Dạng 3 (BTM / tương tự): hai cốc có đá
  haiCoc: (cap = '', a = 'kim loại', b2 = 'xốp') => {
    let b = coc(24, 136, 44, 38, 124, 134, LIGHT) + coc(184, 296, 44, 200, 280, 134, '#fff', 6);
    b += da(50, 96, 20) + da(78, 100, 20) + da(206, 96, 20) + da(236, 100, 20);
    b += T(80, 30, a, { a: 'middle' }) + T(240, 30, b2, { a: 'middle' });
    return wrap('0 0 320 150', b, cap, 'Hai cốc đựng đá');
  },
};
