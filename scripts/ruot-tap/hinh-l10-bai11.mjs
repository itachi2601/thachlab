// Hình minh hoạ cho ruột tập VL10 · Bài 11 Thực hành: đo gia tốc rơi tự do (lesson 56).
// Cùng quy tắc với hinh.mjs: mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét chứ không chỉ bằng màu, tự vẽ.
// Chú thích không lộ đáp án ô Dự đoán/ô điền đứng cạnh. Xem thử: node scripts/ruot-tap/l10-bai11.mjs --hinh
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const sp = (s) => `<tspan font-size="15" dy="-8">${s}</tspan><tspan dy="8"> </tspan>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const dot = (x, y, r = 4.5, c = INK) => `<circle cx="${x}" cy="${y}" r="${r}" fill="${c}"/>`;
const rect = (x, y, w, h, fill = '#fff') => `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${fill}" stroke="${INK}" stroke-width="${SW}"/>`;
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const arrowV = (x, y1, y2) => ln(x, y1, x, y2) + `<path d="M${x},${y1} l-5,10 h10 z" fill="${INK}"/><path d="M${x},${y2} l-5,-10 h10 z" fill="${INK}"/>`;

// bố trí thí nghiệm: nam châm giữ bi, cổng quang, thước, đồng hồ. sMark: ghi chữ s ở đoạn rơi.
const boTri = (cap, sMark = true) => {
  let b = '';
  b += ln(40, 14, 40, 206, INK, 5) + rect(8, 206, 84, 12, '#e4e9f5');          // giá + đế
  b += rect(40, 24, 80, 20, '#dfe5f2') + T(128, 40, 'nam châm', { size: 20 });     // nam châm điện
  b += `<circle cx="80" cy="55" r="11" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(96, 66, 'bi thép', { size: 20 });
  // cổng quang: hai chân + đáy, tia sáng nét đứt đỏ
  b += ln(58, 150, 58, 184) + ln(102, 150, 102, 184) + ln(58, 184, 102, 184) + ln(58, 166, 102, 166, RED, 3, '7 5');
  b += T(112, 176, 'cổng quang', { size: 20 });
  if (sMark) b += arrowV(80, 70, 164) + T(90, 124, 's', { w: 700 });
  // thước đứng bên phải
  b += rect(300, 24, 18, 170, '#fff');
  for (let y = 34; y < 194; y += 10) b += ln(300, y, y % 50 === 4 ? 310 : 306, y, INK, 1.6);
  b += T(309, 216, 'thước', { a: 'middle', size: 20 });
  // đồng hồ hiện số
  b += rect(196, 96, 88, 44, '#fff') + T(240, 126, 'đồng hồ', { a: 'middle', size: 20 });
  return wrap('0 0 340 226', b, cap, 'Bố trí đo gia tốc rơi tự do: nam châm giữ bi, cổng quang, thước, đồng hồ hiện số');
};

export const hinhL10b11 = {
  // Trang 1 · Dự đoán: ba lần thả, hai cách bấm giờ (chỉ ghi số đo)
  tayCong: (cap = 'Hai cách đo thời gian rơi của cùng một viên bi, thả từ độ cao 0,500 m.') => {
    let b = '';
    // trái: đồng hồ bấm giây
    b += rect(10, 10, 140, 120, '#fff') + T(80, 36, 'Bấm tay', { a: 'middle', w: 700 });
    b += `<circle cx="80" cy="86" r="30" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + ln(80, 86, 80, 66) + ln(80, 86, 94, 92) + ln(74, 50, 86, 50, INK, 5) + ln(80, 50, 80, 56);
    b += T(80, 128, '', {});
    // phải: cổng quang + đồng hồ hiện số
    b += rect(170, 10, 140, 120, '#fff') + T(240, 36, 'Cổng quang', { a: 'middle', w: 700 });
    b += ln(192, 56, 192, 100) + ln(236, 56, 236, 100) + ln(192, 100, 236, 100) + ln(192, 78, 236, 78, RED, 3, '7 5');
    b += rect(250, 66, 52, 26, '#fff');
    b += ln(236, 78, 250, 78);
    return wrap('0 0 320 142', b, cap, 'Hai cách đo thời gian rơi: bấm tay và cổng quang nối đồng hồ hiện số');
  },
  // Trang 1 · II.1 và BTM D3: đường s theo t²
  duongS: (cap = 'Đồ thị s theo t²: đường thẳng qua gốc O; hai điểm bất kì (1), (2).', moVach = true) => {
    const x0 = 56, y0 = 150, xe = 300, ye = 18;
    let b = defs('ds1') + ln(x0, y0, xe, y0) + ln(x0, y0, x0, ye) + `<path d="M${xe},${y0} l-9,-5 v10 z" fill="${INK}"/><path d="M${x0},${ye} l-5,9 h10 z" fill="${INK}"/>`;
    b += T(xe, y0 + 24, `${gk('t')}${sp('2')} (s${sp('2')})`, { a: 'end' }) + T(x0 + 10, ye + 8, `${gk('s')} (m)`) + T(x0 - 8, y0 + 22, 'O', { a: 'end' });
    const f = (x) => y0 - (x - x0) * 0.42;
    b += ln(x0, y0, 276, f(276));
    if (moVach) for (const [i, x] of [112, 220].entries()) {
      const y = f(x);
      b += ln(x0, y, x, y, GREY, 2, '5 4') + ln(x, y, x, y0, GREY, 2, '5 4') + dot(x, y, 5.5);
      b += T(x0 - 6, y + 7, `${gk('s')}${sb(i + 1)}`, { a: 'end' }) + T(x, y0 + 24, `${gk('t')}${sb(i + 1)}${sp('2')}`, { a: 'middle' });
    }
    return wrap('0 0 320 186', b, cap, 'Đồ thị s theo t bình phương');
  },
  boTri,
  // BTM D3: chỉ có trục s–t² (không vẽ đường) để HS tự vẽ nháp
  truc: (cap = 'Trục s theo t²: vẽ nháp các điểm của bảng.') => {
    const x0 = 56, y0 = 150, xe = 300, ye = 18;
    let b = ln(x0, y0, xe, y0) + ln(x0, y0, x0, ye) + `<path d="M${xe},${y0} l-9,-5 v10 z" fill="${INK}"/><path d="M${x0},${ye} l-5,9 h10 z" fill="${INK}"/>`;
    b += T(xe, y0 + 24, `${gk('t')}${sp('2')} (s${sp('2')})`, { a: 'end' }) + T(x0 + 10, ye + 8, `${gk('s')} (m)`) + T(x0 - 8, y0 + 22, 'O', { a: 'end' });
    return wrap('0 0 320 186', b, cap, 'Hai trục s và t bình phương để vẽ nháp');
  },
  // Bẫy 1 · hai cách đặt đầu thước (chỉ mô tả vị trí)
  saiGoc: (cap = 'Hai cách đặt đầu thước: (1) mép dưới bi, (2) mặt nam châm.') => {
    let b = '';
    b += rect(70, 20, 110, 20, '#dfe5f2') + T(190, 36, 'nam châm', { size: 20 });
    b += `<circle cx="125" cy="51" r="11" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += ln(14, 150, 180, 150, RED, 3, '7 5') + T(190, 156, 'tia sáng', { size: 20 });
    b += ln(62, 62, 112, 62, GREY, 2, '5 4') + ln(14, 40, 70, 40, GREY, 2, '5 4');
    b += arrowV(64, 62, 150) + arrowV(22, 40, 150);
    b += T(64, 172, '(1)', { a: 'middle', w: 700 }) + T(22, 172, '(2)', { a: 'middle', w: 700 });
    return wrap('0 0 290 180', b, cap, 'Hai cách đo độ cao s: từ mép dưới bi hoặc từ mặt nam châm');
  },
  // Trang 5 · lưới đồ thị s theo t²: t² 0–0,14 s² (vạch 0,02; lưới mịn 0,01), s 0–0,70 m (vạch 0,10; lưới mịn 0,02)
  luoi: (cap = 'Vẽ đường thẳng qua các điểm (t̄², s); số đo nằm ngoài lưới thì đổi thang và ghi lại.') => {
    const X0 = 64, Y0 = 312, W = 420, H = 280;
    let b = '';
    for (let i = 0; i <= 14; i++) b += ln(X0 + i * 30, Y0, X0 + i * 30, Y0 - H, '#d3dbec', i % 2 === 0 ? 1.1 : .6);
    for (let j = 0; j <= 35; j++) b += ln(X0, Y0 - j * 8, X0 + W, Y0 - j * 8, '#d3dbec', j % 5 === 0 ? 1.1 : .5);
    b += `<rect x="${X0}" y="${Y0 - H}" width="${W}" height="${H}" fill="none" stroke="${INK}" stroke-width="2.2"/>`;
    for (let i = 0; i <= 7; i++) b += ln(X0 + i * 60, Y0, X0 + i * 60, Y0 + 8, INK, 2.2) + T(X0 + i * 60, Y0 + 28, i === 0 ? '0' : `0,${String(i * 2).padStart(2, '0')}`, { a: 'middle', size: 16 });
    for (let j = 0; j <= 7; j++) b += ln(X0 - 8, Y0 - j * 40, X0, Y0 - j * 40, INK, 2.2) + T(X0 - 12, Y0 - j * 40 + 6, j === 0 ? '0' : `0,${j}`, { a: 'end', size: 16 });
    b += T(X0 + W, Y0 + 54, `${gk('t')}${sp('2')} (s${sp('2')})`, { a: 'end', size: 18, w: 700 }) + T(8, Y0 - H - 14, `${gk('s')} (m)`, { size: 18, w: 700 });
    return wrap('0 0 500 372', b, cap, 'Lưới vẽ đồ thị s theo t bình phương');
  },
};
