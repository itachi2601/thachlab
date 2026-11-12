// Hình minh hoạ cho ruột tập VL11 · Bài 26 Thực hành: đo suất điện động và điện trở trong của pin (lesson 45).
// Cùng quy tắc với hinh.mjs: mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox (hình rộng: ≥ 3 mm ở cỡ in), nét ≥ 2,8,
// phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ. Chú thích không lộ đáp án ô Dự đoán/ô điền đứng cạnh.
// Xem thử: node scripts/ruot-tap/l11-bai26.mjs --hinh (chụp vào out/hinh-l11-bai26/).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
// chữ nghiêng toán (ℰ, I, U): lấy từ KaTeX_Math (đã nạp qua katex.min.css) để không rơi về font hệ thống
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const dot = (x, y, r = 4.5, c = INK) => `<circle cx="${x}" cy="${y}" r="${r}" fill="${c}"/>`;
const meter = (x, y, s) => `<circle cx="${x}" cy="${y}" r="17" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(x, y + 7, s, { a: 'middle', w: 700 });
const rect = (x, y, w, h) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
// pin: hai bản nằm ngang, bản dài (+) ở trên; đặt giữa (x, y1) và (x, y2)
const pin = (x, y, dau = true) => ln(x - 22, y - 9, x + 22, y - 9) + ln(x - 11, y + 9, x + 11, y + 9, INK, 6) + (dau ? T(x + 30, y - 4, '+', { w: 700 }) : '');

export const hinhL11b26 = {
  // Trang 1 · Dự đoán: cùng một viên pin, hai số đo (chỉ mô tả cái thấy, không nêu nguyên nhân)
  xeDoChoi: (cap = 'Cùng một viên pin: vôn kế đo ở hai thời điểm.') => {
    let b = defs('xd1');
    // trái: hở mạch
    b += rect(38, 28, 62, 40) + T(69, 55, '1,50 V', { a: 'middle', w: 700 });
    b += ln(69, 68, 69, 92) + pin(69, 110) + ln(69, 119, 69, 142) + T(69, 168, 'không nối gì', { a: 'middle', size: 20 });
    // phải: có động cơ
    b += rect(190, 28, 62, 40) + T(221, 55, '1,06 V', { a: 'middle', w: 700 });
    b += ln(221, 68, 221, 92) + pin(221, 110) + ln(221, 119, 221, 142);
    b += ln(221, 92, 290, 92) + ln(290, 92, 290, 112) + `<circle cx="290" cy="130" r="18" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(290, 138, 'M', { a: 'middle', w: 700 }) + ln(290, 148, 290, 142) + ln(290, 142, 221, 142);
    b += T(256, 168, 'động cơ quay', { a: 'middle' });
    return wrap('0 0 320 182', b, cap, 'Số chỉ vôn kế hai đầu một viên pin trước và sau khi nối động cơ');
  },
  // Trang 1 · II.1 và BTM D1: đường thẳng U–I, hai điểm bất kì
  duongThang: (cap = 'Đường U–I của một pin; hai điểm bất kì (1) và (2).') => {
    const x0 = 56, y0 = 150, xe = 300, ye = 18;
    let b = defs('dt1') + ln(x0, y0, xe, y0) + ln(x0, y0, x0, ye) + `<path d="M${xe},${y0} l-9,-5 v10 z" fill="${INK}"/><path d="M${x0},${ye} l-5,9 h10 z" fill="${INK}"/>`;
    b += T(xe, y0 + 24, `${gk('I')} (A)`, { a: 'end' }) + T(x0 + 10, ye + 8, `${gk('U')} (V)`);
    const f = (x) => 52 + (x - x0) * 0.4;
    b += ln(x0, f(x0), 276, f(276), INK, SW);
    const P = [112, 214];
    for (const [i, x] of P.entries()) {
      const y = f(x);
      b += ln(x0, y, x, y, GREY, 2, '5 4') + ln(x, y, x, y0, GREY, 2, '5 4') + dot(x, y, 5.5);
      b += T(x0 - 6, y + 7, `${gk('U')}${sb(i + 1)}`, { a: 'end' }) + T(x, y0 + 24, `${gk('I')}${sb(i + 1)}`, { a: 'middle' });
    }
    b += dot(x0, f(x0), 5.5, RED) + T(x0 - 6, f(x0) - 6, `${gk('E')}`, { a: 'end', c: RED, w: 700 }) + T(x0 - 8, y0 + 24, '0', { a: 'end' });
    return wrap('0 0 320 186', b, cap, 'Đường thẳng U theo I đi xuống, hai điểm trên đường');
  },
  // Trang 2 · sơ đồ mạch đo: M, N hai cực pin; vôn kế song song M–N; ampe kế, R0, Rx nối tiếp
  soDo: (cap = 'Sơ đồ mạch đo. M, N là hai cực của pin.') => {
    const xl = 34, xr = 296, yt = 28, yb = 168;
    let b = '';
    // khung dây chính
    b += ln(xl, yt, 82, yt) + ln(106, yt, 160, yt) + ln(184, yt, xr, yt) + ln(xr, yt, xr, yb) + ln(xr, yb, 238, yb) + ln(180, yb, 156, yb) + ln(100, yb, xl, yb);
    // khoá K: hai chốt và lưỡi nghiêng
    b += dot(82, yt, 4.5) + dot(106, yt, 4.5) + ln(82, yt, 102, yt - 16) + T(100, yt + 34, 'K', { a: 'middle', w: 700 });
    // ampe kế
    b += meter(172, yt, 'A');
    // pin giữa dây trái (M phía trên, N phía dưới)
    b += ln(xl, yt, xl, 82) + pin(xl, 96, false) + ln(xl, 105, xl, yb);
    b += dot(xl, 66) + T(xl - 8, 70, 'M', { a: 'end', w: 700 }) + dot(xl, 128) + T(xl - 8, 140, 'N', { a: 'end', w: 700 });
    // vôn kế song song hai cực pin
    b += ln(xl, 66, 90, 66) + ln(90, 66, 90, 76) + meter(90, 93, 'V') + ln(90, 110, 90, 128) + ln(90, 128, xl, 128);
    // R0 (điện trở cố định) và Rx (biến trở có mũi tên) trên dây dưới
    b += rect(100, yb - 9, 56, 18) + T(128, yb + 28, `R${sb('0')}`, { a: 'middle', w: 700 });
    b += rect(180, yb - 9, 58, 18) + `<path d="M196,${yb - 26} L226,${yb - 7}" stroke="${INK}" stroke-width="${SW}" fill="none"/><path d="M226,${yb - 7} l-9,-1 l5,-8 z" fill="${INK}"/>` + T(209, yb + 28, `R${sb('x')}`, { a: 'middle', w: 700 });
    return wrap('0 0 320 204', b, cap, 'Sơ đồ mạch đo suất điện động và điện trở trong của pin');
  },
  // Trang 2 · Bẫy: ampe kế mắc nhầm vào hai cực pin (chỉ mô tả cách mắc)
  ampeSongSong: (cap = 'Một bạn mắc ampe kế như hình.') => {
    let b = '';
    b += ln(40, 20, 130, 20) + ln(130, 20, 130, 58) + ln(40, 20, 40, 52) + pin(40, 66, false) + ln(40, 75, 40, 140) + ln(40, 140, 130, 140) + ln(130, 100, 130, 140);
    b += dot(40, 40) + T(30, 44, 'M', { a: 'end', w: 700 }) + dot(40, 108) + T(30, 114, 'N', { a: 'end', w: 700 });
    b += ln(40, 40, 82, 40) + ln(82, 40, 82, 52) + meter(82, 69, 'A') + ln(82, 86, 82, 108) + ln(82, 108, 40, 108);
    b += rect(116, 58, 28, 42) + T(130, 86, 'R', { a: 'middle', w: 700 }) + ln(130, 20, 130, 58) + ln(130, 100, 130, 140);
    return wrap('0 0 180 156', b, cap, 'Ampe kế mắc song song với hai cực pin');
  },
  // Trang 4 · sai số: vôn kế kẹp sát cực pin hay qua dây dài
  kepVon: (cap = 'Hai cách kẹp vôn kế vào pin.') => {
    let b = '';
    for (const [x0, lab, dai] of [[0, '(1)', false], [168, '(2)', true]]) {
      b += `<rect x="${x0 + 30}" y="30" width="84" height="32" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(x0 + 72, 53, 'pin', { a: 'middle' });
      b += ln(x0 + 30, 46, x0 + 14, 46) + ln(x0 + 114, 46, x0 + 130, 46) + T(x0 + 8, 20, lab, { w: 700 });
      b += dot(x0 + 30, 46) + dot(x0 + 114, 46);
      if (!dai) { b += ln(x0 + 36, 62, x0 + 36, 100) + ln(x0 + 108, 62, x0 + 108, 100) + meter(x0 + 72, 118, 'V') + ln(x0 + 36, 100, x0 + 72, 100) + ln(x0 + 72, 100, x0 + 72, 101) + ln(x0 + 108, 100, x0 + 72, 100); }
      else { b += ln(x0 + 14, 46, x0 + 14, 120) + ln(x0 + 130, 46, x0 + 130, 120) + ln(x0 + 14, 120, x0 + 55, 120) + ln(x0 + 90, 120, x0 + 130, 120) + meter(x0 + 72, 120, 'V') + T(x0 + 72, 160, 'dây dài', { a: 'middle' }); }
    }
    return wrap('0 0 320 172', b, cap, 'Vôn kế nối sát cực pin hoặc nối qua dây dài');
  },
  // Trang 5 · lưới vẽ đồ thị: trục I (0–0,8 A, vạch 0,1) và U (1,0–1,6 V, vạch 0,1); lưới mịn 0,02
  luoi: (cap = 'Vẽ cả hai đường: pin cũ nét liền, pin mới nét đứt. Số đo nằm ngoài lưới thì đổi thang và ghi lại.') => {
    const X0 = 62, Y0 = 296, W = 400, H = 240; // 400 = 0,8 A; 240 = 0,6 V
    let b = '';
    for (let i = 0; i <= 40; i++) b += ln(X0 + i * 10, Y0, X0 + i * 10, Y0 - H, '#d3dbec', i % 5 === 0 ? 1.1 : .5);
    for (let j = 0; j <= 30; j++) b += ln(X0, Y0 - j * 8, X0 + W, Y0 - j * 8, '#d3dbec', j % 5 === 0 ? 1.1 : .5);
    b += `<rect x="${X0}" y="${Y0 - H}" width="${W}" height="${H}" fill="none" stroke="${INK}" stroke-width="2.2"/>`;
    for (let i = 0; i <= 8; i++) b += ln(X0 + i * 50, Y0, X0 + i * 50, Y0 + 8, INK, 2.2) + T(X0 + i * 50, Y0 + 28, i === 0 ? '0' : `0,${i}`, { a: 'middle', size: 16 });
    for (let j = 0; j <= 6; j++) b += ln(X0 - 8, Y0 - j * 40, X0, Y0 - j * 40, INK, 2.2) + T(X0 - 12, Y0 - j * 40 + 6, `1,${j}`, { a: 'end', size: 16 });
    b += T(X0 + W, Y0 + 52, `${gk('I')} (A)`, { a: 'end', size: 18, w: 700 }) + T(8, Y0 - H - 14, `${gk('U')} (V)`, { size: 18, w: 700 });
    return wrap('0 0 480 360', b, cap, 'Lưới vẽ đồ thị U theo I');
  },
  // Bài tương tự · so hai đường U–I (không số): dùng cạnh nháp
  haiPin: (cap = 'Đường U–I của hai pin cùng ℰ.') => {
    const x0 = 56, y0 = 150, xe = 300, ye = 18;
    let b = ln(x0, y0, xe, y0) + ln(x0, y0, x0, ye) + `<path d="M${xe},${y0} l-9,-5 v10 z" fill="${INK}"/><path d="M${x0},${ye} l-5,9 h10 z" fill="${INK}"/>`;
    b += T(xe, y0 + 24, `${gk('I')} (A)`, { a: 'end' }) + T(x0 + 10, ye + 8, `${gk('U')} (V)`);
    b += ln(x0, 48, 276, 80, INK, SW) + T(278, 90, '(1)', { w: 700 });
    b += ln(x0, 48, 276, 128, INK, SW, '8 5') + T(278, 142, '(2)', { w: 700 });
    b += dot(x0, 48, 5.5, RED) + T(x0 - 6, 54, `${gk('E')}`, { a: 'end', c: RED, w: 700 });
    return wrap('0 0 320 186', b, cap.replace('ℰ', 'E'), 'Hai đường thẳng U theo I cùng cắt trục U');
  },
};
