// Hình minh hoạ cho ruột tập VL11 · Bài 23 Điện trở. Định luật Ohm (lesson 42). Cùng quy tắc với hinh.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh (đồ thị đèn để trống cho học sinh chấm điểm, không vẽ sẵn đường cong).
// Xem thử: node scripts/ruot-tap/l11-bai23.mjs --hinh (chụp vào out/hinh-l11-bai23/).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
// chữ Hi Lạp/Ω: lấy từ KaTeX_Main/Math (đã nạp qua katex.min.css) để không rơi về Helvetica
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const OM = '<tspan font-family="KaTeX_Main">Ω</tspan>';
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const arr = (x1, y1, x2, y2, id, c = INK, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${SW}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const tron = (x, y, r, s) => `<circle cx="${x}" cy="${y}" r="${r}" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(x, y + 7, s, { a: 'middle', w: 700 });
const dtro = (x, y, w = 46, h = 18) => `<rect x="${x - w / 2}" y="${y - h / 2}" width="${w}" height="${h}" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
const cham = (x, y, c = INK) => `<circle cx="${x}" cy="${y}" r="5" fill="${c}"/>`;

// Hệ trục: gốc (x0, y0), rộng W, cao H; xs/ys = nhãn vạch chia; lưới mờ để học sinh chấm điểm.
const truc = (id, { x0 = 56, y0 = 196, W = 220, H = 170, xs = [], ys = [], xl = 'U (V)', yl = 'I (A)', luoi = true } = {}) => {
  let b = defs(id);
  if (luoi) {
    xs.forEach((_, i) => { const x = x0 + (W * (i + 1)) / xs.length; b += ln(x, y0, x, y0 - H, GREY, 1, '3 4'); });
    ys.forEach((_, i) => { const y = y0 - (H * (i + 1)) / ys.length; b += ln(x0, y, x0 + W, y, GREY, 1, '3 4'); });
  }
  b += arr(x0, y0, x0 + W + 18, y0, id) + arr(x0, y0, x0, y0 - H - 18, id);
  xs.forEach((s, i) => { const x = x0 + (W * (i + 1)) / xs.length; b += ln(x, y0, x, y0 + 6, INK, 2) + T(x, y0 + 26, s, { a: 'middle' }); });
  ys.forEach((s, i) => { const y = y0 - (H * (i + 1)) / ys.length; b += ln(x0 - 6, y, x0, y, INK, 2) + T(x0 - 9, y + 7, s, { a: 'end' }); });
  b += T(x0 + W + 16, y0 - 10, xl, { a: 'end' }) + T(x0 + 8, y0 - H - 6, yl);
  b += T(x0 - 8, y0 + 24, 'O', { a: 'end' });
  return b;
};

export const hinhL11b23 = {
  // ===== Trang học bài mới =====
  denBat: (cap = 'Cùng bóng, cùng ổ 220 V.') => {
    let b = ln(40, 40, 40, 170) + ln(40, 40, 140, 40) + ln(40, 170, 250, 170);
    b += `<rect x="8" y="84" width="64" height="44" rx="5" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(40, 113, '220 V', { a: 'middle', w: 700 });
    b += ln(140, 40, 178, 22) + cham(140, 40) + cham(186, 40) + ln(186, 40, 250, 40) + T(160, 16, 'công tắc', { a: 'middle' });
    b += ln(250, 40, 250, 76) + ln(250, 134, 250, 170);
    b += `<circle cx="250" cy="105" r="30" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<path d="M236,120 L240,96 L246,110 L254,96 L260,110 L264,120" fill="none" stroke="${INK}" stroke-width="2.2"/>`;
    b += `<path d="M284,86 L294,80 M286,104 L298,104 M284,122 L294,128" stroke="${RED}" stroke-width="2.4"/>` + T(214, 156, 'dây tóc', { a: 'end' });
    return wrap('0 0 304 186', b, cap, 'Bóng đèn sợi đốt nối ổ điện qua công tắc');
  },
  dayAB: (cap = 'Cùng 12 V, ampe kế chỉ khác nhau.') => {
    let b = '';
    [[40, 'A', '2 A'], [130, 'B', '0,5 A']].forEach(([y, n, i]) => {
      b += `<rect x="8" y="${y - 20}" width="40" height="40" rx="4" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(28, y + 7, '12V', { a: 'middle', size: 17, w: 700 });
      b += ln(48, y, 92, y) + tron(112, y, 20, 'A') + ln(132, y, 162, y);
      b += `<path d="M162,${y} q8,-14 16,0 t16,0 t16,0 t16,0 t16,0" fill="none" stroke="${INK}" stroke-width="${SW}"/>` + T(194, y - 18, `dây ${n}`, { a: 'middle' });
      b += ln(242, y, 262, y) + T(112, y + 44, i, { a: 'middle', w: 700 });
    });
    return wrap('0 0 270 186', b, cap, 'Hai sợi dây cùng hiệu điện thế 12 V');
  },
  machDo: (cap = 'Ampe kế nối tiếp, vôn kế song song với R.') => {
    let b = ln(30, 40, 270, 40) + ln(30, 40, 30, 150) + ln(30, 150, 270, 150) + ln(270, 40, 270, 150);
    b += `<rect x="12" y="76" width="36" height="40" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(30, 103, 'U', { a: 'middle', w: 700 });
    b += T(56, 102, 'nguồn', { size: 18 });
    b += tron(150, 40, 20, 'A') + dtro(220, 150) + T(220, 128, 'R', { a: 'middle', w: 700 });
    b += ln(186, 150, 186, 196) + ln(254, 150, 254, 196) + ln(186, 196, 200, 196) + ln(240, 196, 254, 196) + tron(220, 196, 20, 'V');
    return wrap('0 0 290 222', b, cap, 'Mạch đo điện trở bằng ampe kế và vôn kế');
  },
  luoiR: (cap = 'Chấm 5 điểm đo của R = 10 Ω, nối lại.') =>
    wrap('0 0 300 236', truc('lr', { xs: ['1', '2', '3', '4', '5'], ys: ['0,1', '0,2', '0,3', '0,4', '0,5'] }), cap, 'Hệ trục I theo U để chấm điểm đo'),
  mangIon: (cap = 'Trái: kim loại lạnh. Phải: kim loại nóng. Đường đỏ: một electron trôi qua.') => {
    let b = '';
    const ion = (x, y, dx = 0, dy = 0) => `<circle cx="${x + dx}" cy="${y + dy}" r="11" fill="#fff" stroke="${INK}" stroke-width="2.4"/>` + T(x + dx, y + dy + 7, '+', { a: 'middle', w: 700, size: 20 });
    const lech = [[3, -4], [-5, 3], [4, 5], [-4, -5], [5, 2], [-3, 5], [4, -3], [-5, -2], [2, 5]];
    for (let r = 0; r < 3; r++) for (let c = 0; c < 3; c++) {
      b += ion(26 + c * 44, 40 + r * 52);
      const [dx, dy] = lech[r * 3 + c];
      const x = 186 + c * 44, y = 40 + r * 52;
      b += `<circle cx="${x}" cy="${y}" r="20" fill="none" stroke="${GREY}" stroke-width="1.6" stroke-dasharray="3 3"/>` + ion(x, y, dx * 1.6, dy * 1.6);
    }
    b += `<path d="M4,66 L50,62 L96,70 L128,66" fill="none" stroke="${RED}" stroke-width="2.4"/>`;
    b += `<path d="M164,66 L196,72 L184,88 L212,100 L226,74 L250,92 L238,116 L272,104 L290,118" fill="none" stroke="${RED}" stroke-width="2.4"/>`;
    b += ln(150, 10, 150, 160, GREY, 2, '6 4') + T(70, 182, 'lạnh', { a: 'middle', w: 700 }) + T(230, 182, 'nóng', { a: 'middle', w: 700 });
    return wrap('0 0 300 192', b, cap, 'Mạng ion kim loại khi lạnh và khi nóng');
  },
  luoiDen: (cap = 'Chấm 6 điểm đo của đèn. Đường đứt: R = 12 Ω không đổi.') => {
    let b = truc('ld', { xs: ['1', '2', '3', '4', '5', '6'], ys: ['0,1', '0,2', '0,3', '0,4', '0,5'] });
    b += ln(56, 196, 276, 26, GREY, 2.4, '8 5') + T(270, 22, `12 ${OM}`, { a: 'end', size: 18 });
    return wrap('0 0 300 236', b, cap, 'Hệ trục I theo U để chấm điểm đo của bóng đèn');
  },
  ntcCoc: (cap = 'NTC và nhiệt kế cùng nhúng trong nước.') => {
    let b = `<path d="M40,70 L52,196 L148,196 L160,70" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + ln(46, 110, 154, 110, BLUE, 2, '7 4');
    b += ln(80, 40, 80, 160, INK, 2.4) + ln(92, 40, 92, 160, INK, 2.4) + `<ellipse cx="86" cy="168" rx="12" ry="9" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(86, 175, 'N', { a: 'middle', size: 15, w: 700 });
    b += `<rect x="114" y="84" width="12" height="96" rx="6" fill="#fff" stroke="${INK}" stroke-width="2.4"/><circle cx="120" cy="182" r="9" fill="${RED}"/>` + ln(120, 180, 120, 120, RED, 4);
    b += ln(80, 40, 200, 40) + ln(92, 40, 92, 58) + ln(92, 58, 200, 58);
    b += `<rect x="200" y="22" width="88" height="56" rx="6" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(244, 58, `? k${OM}`, { a: 'middle', w: 700 });
    b += T(244, 100, `thang ${OM}`, { a: 'middle', size: 18 }) + T(150, 222, `nước 25 <tspan font-family="KaTeX_Main">→</tspan> 55 °C`, { a: 'middle' });
    return wrap('0 0 300 230', b, cap, 'Điện trở nhiệt NTC nhúng trong cốc nước ấm');
  },
  haiDuong: (cap = 'Hai điện trở. Đường nào dốc hơn?') => {
    let b = truc('hd', { xs: ['1', '2', '3', '4'], ys: ['0,1', '0,2', '0,3', '0,4'] });
    b += ln(56, 196, 276, 26, RED, SW) + T(250, 20, '(1)', { c: RED, w: 700 }) + cham(276, 26, RED);
    b += ln(56, 196, 276, 111, BLUE, SW, '8 5') + T(250, 100, '(2)', { c: BLUE, w: 700 }) + cham(276, 111, BLUE);
    return wrap('0 0 300 236', b, cap, 'Hai đường đặc trưng thẳng qua gốc');
  },
  dayToc: (cap = 'Một dây tóc, hai trạng thái.') => {
    const bong = (x, s, nong) => `<circle cx="${x}" cy="60" r="36" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
      + `<path d="M${x - 16},78 L${x - 12},48 L${x - 4},66 L${x + 4},48 L${x + 12},66 L${x + 16},78" fill="none" stroke="${nong ? RED : INK}" stroke-width="${nong ? 3.4 : 2.2}"/>`
      + `<rect x="${x - 14}" y="96" width="28" height="18" fill="#fff" stroke="${INK}" stroke-width="2.4"/>` + T(x, 140, s, { a: 'middle', w: 700 });
    let b = bong(70, 'vừa bật', false) + bong(220, 'đang sáng', true);
    b += T(70, 166, '20 °C', { a: 'middle' }) + T(70, 190, `R${sb('0')} = 4,0 ${OM}`, { a: 'middle' });
    b += T(220, 166, '12 V; 0,25 A', { a: 'middle' }) + T(220, 190, 't = ?', { a: 'middle' });
    return wrap('0 0 292 200', b, cap, 'Dây tóc bóng đèn lúc nguội và lúc sáng');
  },
  // ===== Bài tập mẫu =====
  haiDuongD3: (cap = 'Trục đứng là I (mA). Đọc một điểm trên mỗi đường.') => {
    let b = truc('d3', { y0: 170, H: 140, xs: ['2', '4', '6'], ys: ['1', '2', '3'], yl: 'I (mA)' });
    b += ln(56, 170, 276, 30, RED, SW) + cham(276, 30, RED) + T(246, 26, '(1)', { c: RED, w: 700 });
    b += ln(56, 170, 276, 114, BLUE, SW, '8 5') + cham(276, 114, BLUE) + T(246, 104, '(2)', { c: BLUE, w: 700 });
    return wrap('0 0 300 206', b, cap, 'Hai đường đặc trưng, trục I tính bằng mA');
  },
  loPt: (cap = 'R<sub>0</sub> ứng với t<sub>0</sub> = 0 °C, không phải 20 °C.') => {
    let b = `<rect x="150" y="40" width="130" height="110" rx="8" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(215, 172, 'lò', { a: 'middle', w: 700 });
    b += `<path d="M178,96 q8,-16 16,0 t16,0 t16,0 t16,0" fill="none" stroke="${RED}" stroke-width="${SW}"/>` + T(215, 72, 'dây Pt', { a: 'middle', size: 18 });
    b += ln(178, 96, 120, 96) + ln(258, 96, 270, 96) + ln(270, 96, 270, 190) + ln(270, 190, 20, 190) + ln(20, 190, 20, 96) + ln(20, 96, 40, 96);
    b += tron(80, 96, 20, 'A') + ln(60, 96, 40, 96) + ln(100, 96, 120, 96);
    b += `<rect x="2" y="128" width="36" height="40" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(20, 155, 'U', { a: 'middle', w: 700 });
    return wrap('0 0 292 200', b, cap, 'Nhiệt kế điện trở platin đặt trong lò');
  },
  rTheoT: (cap = 'R tăng bậc nhất theo t (nicrom tăng rất ít).') => {
    let b = truc('rt', { xs: ['20', '', '', '', '', '270'], ys: [], xl: 't (°C)', yl: `R (${OM})`, luoi: false });
    b += ln(82, 120, 276, 98, RED, SW) + cham(92, 119, RED) + cham(276, 98, RED);
    b += ln(92, 119, 92, 196, GREY, 1.8, '4 4') + ln(276, 98, 276, 196, GREY, 1.8, '4 4');
    b += T(98, 146, '40,0', { size: 18 }) + T(266, 84, '?', { a: 'end', w: 700, c: RED });
    return wrap('0 0 300 236', b, cap, 'Điện trở dây nicrom theo nhiệt độ');
  },
  // ===== Bài tương tự =====
  uTheoI: (cap = 'Trục đứng là U, trục ngang là I.') => {
    let b = truc('ui', { y0: 170, H: 140, xs: ['1', '2'], ys: ['2', '4', '6'], xl: 'I (mA)', yl: 'U (V)' });
    b += ln(56, 170, 276, 30, RED, SW) + cham(276, 30, RED) + T(250, 26, '(1)', { c: RED, w: 700 });
    b += ln(56, 170, 276, 100, BLUE, SW, '8 5') + cham(276, 100, BLUE) + T(250, 90, '(2)', { c: BLUE, w: 700 });
    return wrap('0 0 300 206', b, cap, 'Hai đường U theo I');
  },
};
