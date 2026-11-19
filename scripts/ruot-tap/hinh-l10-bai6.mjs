// Hình minh hoạ cho ruột tập VL10 · Bài 6 Thực hành: đo tốc độ của vật chuyển động (lesson 51).
// Cùng quy tắc với hinh.mjs: mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox (≈ 3 mm ở cỡ in 46 mm), nét ≥ 2,8,
// phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ. Chú thích không lộ đáp án ô Dự đoán/ô điền đứng cạnh.
// Không dùng kí tự mũi tên/↔ trong SVG (tránh rơi về font hệ thống). Xem thử: node scripts/ruot-tap/l10-bai6.mjs --hinh.
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const dot = (x, y, r = 4.5, c = INK) => `<circle cx="${x}" cy="${y}" r="${r}" fill="${c}"/>`;
const rect = (x, y, w, h, fill = '#fff') => `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${fill}" stroke="${INK}" stroke-width="${SW}"/>`;
const ball = (x, y, r = 9, dash = '') => `<circle cx="${x}" cy="${y}" r="${r}" fill="#fff" stroke="${INK}" stroke-width="${SW}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
// máng nghiêng: đường dốc y = y0 + k (x − x0)
const mang = (x1, y1, x2, y2) => `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${INK}" stroke-width="7" stroke-linecap="round"/>`;
// cổng quang: khung chữ nhật đứng, tâm tia là chấm đỏ
const cong = (x, y, nhan) => rect(x - 10, y - 38, 20, 46) + dot(x, y - 14, 4.5, RED) + T(x, y - 46, nhan, { a: 'middle', w: 700 });

export const hinhL10b6 = {
  // Trang 1 · Dự đoán: đoạn đo 0,500 m trên máng, người cầm đồng hồ bấm tay (chỉ mô tả, không nêu độ tin cậy)
  mayBam: (cap = 'Bi lăn qua đoạn 0,500 m; một bạn bấm đồng hồ cầm tay.') => {
    const k = 0.25, y = (x) => 40 + k * (x - 20);
    let b = mang(20, 40, 300, 110);
    b += ball(52, y(52) - 14, 9);
    for (const [x, n] of [[100, 'E'], [240, 'F']]) b += ln(x, y(x) + 6, x, 122, GREY, 2, '5 4') + T(x, y(x) - 10, n, { a: 'middle', w: 700 });
    b += ln(100, 122, 240, 122) + ln(100, 114, 100, 130) + ln(240, 114, 240, 130) + T(170, 150, '0,500 m', { a: 'middle', w: 700 });
    b += `<circle cx="284" cy="34" r="18" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + ln(284, 34, 284, 21, INK, 2.8) + ln(284, 34, 293, 38, INK, 2.8) + rect(279, 8, 10, 6);
    return wrap('0 0 320 160', b, cap, 'Viên bi lăn trên máng nghiêng qua đoạn 0,500 m, một người bấm đồng hồ bằng tay');
  },
  // Trang 1 · II.1: cổng quang (bi chắn tia) nối ổ A của đồng hồ hiện số có núm MODE
  congQuang: (cap = 'Cổng quang nối ổ A của đồng hồ hiện số.') => {
    let b = '';
    b += ln(30, 24, 30, 108) + ln(100, 24, 100, 108) + ln(30, 108, 100, 108);
    b += ln(30, 66, 51, 66, RED, 2.8, '5 4') + ln(79, 66, 100, 66, RED, 2.8, '5 4') + ball(65, 66, 14) + T(65, 18, 'cổng', { a: 'middle' });
    b += rect(150, 16, 160, 112) + rect(164, 28, 70, 28, '#eef2fa') + T(199, 50, '0,000', { a: 'middle', w: 700 });
    b += `<circle cx="276" cy="44" r="16" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + ln(276, 44, 276, 32) + T(276, 86, 'MODE', { a: 'middle', size: 18 });
    for (const [x, n] of [[176, 'A'], [226, 'B']]) b += `<circle cx="${x}" cy="102" r="8" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(x + 12, 109, n, { w: 700 });
    b += `<path d="M65,108 V152 H176 V110" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
    return wrap('0 0 320 160', b, cap, 'Cổng quang có viên bi chắn tia, nối với ổ A của đồng hồ đo thời gian hiện số');
  },
  // Trang 2 · Phương án 1: nam châm điện giữ bi ở đỉnh máng, hai cổng E, F cách nhau s, đồng hồ MODE A–B
  boTri: (cap = 'Bố trí đo tốc độ trung bình trên đoạn EF.') => {
    const k = 0.38, y = (x) => 46 + k * (x - 20);
    let b = mang(20, 46, 216, y(216));
    b += rect(10, 14, 40, 18) + T(4, 6, 'nam châm', { size: 20 }) + ball(30, 44, 9);
    b += cong(112, y(112), 'E') + cong(196, y(196), 'F');
    b += ln(112, y(112) + 12, 112, 150, GREY, 2, '5 4') + ln(196, y(196) + 12, 196, 150, GREY, 2, '5 4') + ln(112, 150, 196, 150) + T(154, 178, 's = EF', { a: 'middle', w: 700 });
    b += rect(232, 112, 82, 66) + rect(240, 120, 66, 22, '#eef2fa') + T(273, 138, '0,000', { a: 'middle', size: 20, w: 700 });
    b += T(250, 168, 'A', { a: 'middle', w: 700 }) + T(296, 168, 'B', { a: 'middle', w: 700 });
    return wrap('0 -10 320 200', b, cap, 'Máng nghiêng có nam châm điện, hai cổng quang E và F, đồng hồ hiện số');
  },
  // Trang 3 · hai vị trí tia sáng trên viên bi: qua tâm và lệch tâm (chỉ hình học, không số)
  tiaLech: (cap = 'Vết của tia sáng lướt qua viên bi trong lúc bi chắn tia.') => {
    const r = 50, h = 30, hx = Math.sqrt(r * r - h * h);
    let b = ball(80, 70, r) + ball(240, 70, r);
    b += ln(30, 70, 130, 70, RED, 3.2) + dot(80, 70, 3.5) + T(80, 100, 'd', { a: 'middle', w: 700 }).replace('y="100"', 'y="92"');
    b += ln(240 - hx, 70 - h, 240 + hx, 70 - h, RED, 3.2) + ln(240, 70, 240, 70 - h, GREY, 2.5, '4 3') + dot(240, 70, 3.5) + T(246, 62, 'h', { w: 700 }).replace('y="62"', 'y="62"');
    b += T(80, 140, '(1) qua tâm', { a: 'middle' }) + T(240, 140, '(2) lệch tâm', { a: 'middle' });
    return wrap('0 0 320 150', b, cap, 'Hai viên bi, tia sáng qua tâm và tia sáng lệch tâm cắt bi theo dây cung ngắn hơn');
  },
  // Trang 4 · một độ chia 0,001 s so với cả số đo: hai thanh cùng độ dài, phần đỏ = sai số tỉ đối (không ghi số)
  soSai: (cap = 'Hai số đo, mỗi thanh là cả số đo; phần đỏ là một độ chia 0,001 s.') => {
    const W = 270, x0 = 40;
    let b = T(x0, 22, 't = 0,837 s', { w: 700 }) + `<rect x="${x0}" y="32" width="${W}" height="24" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<rect x="${x0}" y="32" width="${Math.max(0.001 / 0.837 * W, 1.4)}" height="24" fill="${RED}"/>`;
    b += T(x0, 96, 't = 0,024 s', { w: 700 }) + `<rect x="${x0}" y="106" width="${W}" height="24" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<rect x="${x0}" y="106" width="${0.001 / 0.024 * W}" height="24" fill="${RED}"/>`;
    return wrap('0 0 320 142', b, cap, 'Hai thanh dài bằng nhau, phần đỏ ở thanh thứ hai rộng hơn nhiều so với thanh thứ nhất');
  },
};
