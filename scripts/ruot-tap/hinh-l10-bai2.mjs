// Hình minh hoạ cho ruột tập VL10 · Bài 2 Các quy tắc an toàn trong phòng thực hành Vật lí (lesson 47). Cùng quy tắc với hinh-l10-bai23.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, tự vẽ. Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh.
// Xem thử: node scripts/ruot-tap/l10-bai2.mjs --hinh (chụp vào out/hinh-l10-bai2/).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
const f1 = (v) => v.toFixed(1);
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const rc = (x, y, w, h, r = 4, fill = '#fff', c = INK, sw = SW) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r}" fill="${fill}" stroke="${c}" stroke-width="${sw}"/>`;
const ci = (x, y, r, fill = '#fff', c = INK, sw = SW) => `<circle cx="${x}" cy="${y}" r="${r}" fill="${fill}" stroke="${c}" stroke-width="${sw}"/>`;
const path = (d, fill = 'none', c = INK, sw = SW, extra = '') => `<path d="${d}" fill="${fill}" stroke="${c}" stroke-width="${sw}" stroke-linejoin="round" stroke-linecap="round" ${extra}/>`;
const dat = (x1, x2, y) => ln(x1, y, x2, y) + Array.from({ length: Math.floor((x2 - x1) / 18) }, (_, i) => ln(x1 + 8 + i * 18, y, x1 + i * 18, y + 8, GREY, 1.8)).join('');

// ---- hình bên trong các kí hiệu (tâm cx,cy; cỡ ≈ 56 đơn vị) ----
const ngon = (x, y) => path(`M${x},${y - 24} C${x + 20},${y - 6} ${x + 18},${y + 22} ${x},${y + 24} C${x - 18},${y + 22} ${x - 20},${y - 6} ${x},${y - 24} z`, '#fff', INK, 3)
  + path(`M${x},${y + 4} C${x + 8},${y + 10} ${x + 4},${y + 20} ${x},${y + 20} C${x - 4},${y + 20} ${x - 8},${y + 10} ${x},${y + 4} z`, INK, INK, 1);
const tiaChop = (x, y) => path(`M${x + 6},${y - 22} L${x - 12},${y + 3} L${x - 1},${y + 3} L${x - 7},${y + 24} L${x + 13},${y - 4} L${x + 1},${y - 4} z`, INK, INK, 1.5);
const dauLau = (x, y) => ci(x, y - 4, 10, '#fff', INK, 2.6) + ci(x - 4, y - 5, 2.4, INK, INK, 0) + ci(x + 4, y - 5, 2.4, INK, INK, 0)
  + ln(x - 14, y + 8, x + 14, y + 22, INK, 3) + ln(x + 14, y + 8, x - 14, y + 22, INK, 3);
const thungRac = (x, y) => rc(x - 12, y - 8, 24, 28, 2, '#fff', INK, 2.6) + ln(x - 16, y - 12, x + 16, y - 12, INK, 3) + rc(x - 5, y - 18, 10, 6, 1, '#fff', INK, 2.2)
  + ln(x - 4, y - 2, x - 4, y + 14, INK, 2) + ln(x + 4, y - 2, x + 4, y + 14, INK, 2);
const matNa = (x, y) => path(`M${x - 18},${y - 14} Q${x},${y - 22} ${x + 18},${y - 14} L${x + 15},${y + 8} Q${x},${y + 24} ${x - 15},${y + 8} z`, '#fff', INK, 2.8)
  + ci(x - 7, y + 10, 4, '#fff', INK, 2.2) + ci(x + 7, y + 10, 4, '#fff', INK, 2.2) + ln(x - 24, y - 4, x - 17, y - 4, INK, 2.4) + ln(x + 17, y - 4, x + 24, y - 4, INK, 2.4);
const cocVo = (x, y) => path(`M${x - 18},${y - 20} L${x - 13},${y + 20} L${x + 13},${y + 20} L${x + 18},${y - 20}`, 'none', INK, 3)
  + path(`M${x - 6},${y - 20} L${x + 2},${y - 6} L${x - 5},${y + 2} L${x + 4},${y + 20}`, 'none', INK, 2.4);
const chaiDung = (x, y) => rc(x - 8, y - 2, 16, 26, 2, '#fff', INK, 2.6) + rc(x - 4, y - 12, 8, 10, 1, '#fff', INK, 2.4)
  + ln(x + 22, y + 20, x + 22, y - 18, INK, 3) + path(`M${x + 15},${y - 10} L${x + 22},${y - 20} L${x + 29},${y - 10}`, 'none', INK, 3);
// khung kí hiệu
const tamGiac = (x, y, inner) => path(`M${x},${y - 46} L${x + 50},${y + 38} L${x - 50},${y + 38} z`, '#fff', INK, 3.4) + inner(x, y + 6);
const tronCam = (x, y, inner) => ci(x, y, 44, '#fff', RED, 4) + inner(x, y) + ln(x - 31, y - 31, x + 31, y + 31, RED, 5);
const tronBat = (x, y, inner) => ci(x, y, 44, '#e3edf9', BLUE, 4) + inner(x, y);
const so = (x, y, s) => T(x, y, s, { a: 'middle', w: 700, size: 22 });

export const hinhL10b2 = {
  // Trang 1 · Dự đoán: bàn thực hành lúc còn một đầu dây hở
  banDay: (cap = 'Bàn thực hành: bộ nguồn đang bật, bóng đèn đã nối một đầu, còn một đầu dây hở.') => {
    let b = dat(6, 314, 164);
    b += rc(12, 64, 100, 100, 6) + T(62, 92, 'bộ nguồn', { a: 'middle', w: 700 });
    b += ci(40, 118, 8, RED, RED, 2) + ln(40, 100, 40, 94, RED, 2.4) + ln(25, 106, 20, 101, RED, 2.4) + ln(55, 106, 60, 101, RED, 2.4);
    b += ci(112, 124, 6, INK, INK, 1) + ci(112, 148, 6, INK, INK, 1);
    b += path('M112,124 C160,124 190,128 242,138', 'none', INK, 3.2);
    b += path('M112,148 C140,148 150,156 190,150', 'none', INK, 3.2) + ci(194, 150, 5, '#fff', INK, 2.4);
    b += ci(262, 96, 28, '#fff', INK, SW) + path('M250,118 L250,102 L257,92 L262,100 L267,92 L274,102 L274,118', 'none', INK, 2.4) + rc(246, 120, 32, 18, 3, '#fff', INK, SW);
    b += T(262, 56, 'bóng đèn', { a: 'middle' });
    b += T(236, 190, 'đầu dây hở', { a: 'end' }) + ln(214, 176, 198, 156, GREY, 2.4);
    return wrap('0 0 320 198', b, cap, 'Bàn thực hành còn một đầu dây hở');
  },
  // Trang 1 · II.1: nhãn bộ nguồn học đường
  nhanNguon: (cap = 'Bộ nguồn học đường: núm xoay chọn vạch 3; 6; 9; 12 V.') => {
    let b = rc(8, 12, 304, 178, 6);
    b += ln(112, 12, 112, 190, GREY, 2.4, '5 4');
    b += T(22, 44, 'Input', { w: 700 }) + T(22, 76, '220 V ~', { w: 700, size: 22 });
    b += rc(30, 112, 54, 34, 3) + ln(18, 122, 30, 122) + ln(18, 136, 30, 136) + path('M84,129 L102,129', 'none', INK, 3);
    b += T(126, 44, 'Output', { w: 700 }) + T(126, 76, 'DC 3–12 V', { w: 700 });
    const cx = 172, cy = 140;
    b += ci(cx, cy, 24) + ln(cx, cy, cx - 14, cy - 14, INK, 4);
    [[3, 225], [6, 135], [9, 45], [12, -45]].forEach(([v, a]) => {
      const r = 44, x = cx + r * Math.cos(a * Math.PI / 180), y = cy - r * Math.sin(a * Math.PI / 180);
      b += T(f1(x), f1(y + 7), String(v), { a: 'middle' });
    });
    b += ci(268, 112, 14, RED, RED, 2) + T(268, 119, '+', { c: '#fff', a: 'middle', w: 700 });
    b += ci(268, 164, 14, '#fff', BLUE, 3.4) + T(268, 172, '−', { c: BLUE, a: 'middle', w: 700 });
    return wrap('0 0 320 198', b, cap, 'Nhãn bộ nguồn học đường');
  },
  // Trang 2 · II.2: bốn kí hiệu (ba có khung, một không khung)
  kiHieu: (cap = 'Năm kí hiệu hay gặp: hình dạng và màu cho biết nhóm.') => {
    let b = tamGiac(52, 54, tiaChop) + tronCam(160, 56, ngon) + tronBat(268, 56, matNa);
    b += so(52, 134, '1') + so(160, 134, '2') + so(268, 134, '3');
    b += cocVo(52, 176) + chaiDung(160, 176) ;
    b += so(52, 218, '4') + so(160, 218, '5');
    return wrap('0 0 320 232', b, cap, 'Các kí hiệu an toàn');
  },
  // Trang 3 · thí nghiệm khoảng cách: nhiệt kế cạnh đèn cồn
  khoangCach: (cap = 'Nhiệt kế đặt lần lượt cách đèn cồn 2; 5; 10; 20 cm.', ds = [2, 5, 10, 20]) => {
    const k = 196 / Math.max(...ds), x0 = 62;
    let b = ln(x0, 160, 314, 160, INK, 3);
    b += rc(12, 124, 36, 36, 4) + ln(30, 124, 30, 112, INK, 3) + ngon(30, 90);
    ds.forEach((d, i) => {
      const x = x0 + d * k;
      b += ln(x, 160, x, 168, INK, 2.4) + T(f1(x), 190, String(d), { a: 'middle' });
      b += rc(x - 5, 100, 10, 46, 3, '#fff', INK, 2.6) + ci(x, 150, 7, RED, INK, 2.2) + ln(x, 146, x, 118 + i * 3, RED, 3);
    });
    b += T(316, 190, 'cm', { a: 'end' });
    b += T(6, 52, 'đèn cồn');
    return wrap('0 0 320 198', b, cap, 'Nhiệt kế cách đèn cồn các khoảng khác nhau');
  },
  // Trang 4 · bài toán mẫu: bàn của nhóm trước khi bật nguồn
  banLoi: (cap = 'Bàn của nhóm trước khi bật nguồn. Bóng đèn ghi 6 V, DC.') => {
    let b = dat(6, 314, 150);
    b += ln(30, 150, 30, 196, INK, 3) + ln(290, 150, 290, 196, INK, 3);
    b += rc(14, 56, 86, 94, 6) + T(57, 86, 'nguồn', { a: 'middle', w: 700 }) + ci(40, 122, 16) + ln(40, 122, 30, 112, INK, 4) + T(78, 130, '12 V', { a: 'middle' });
    b += ci(150, 108, 22) + rc(140, 128, 20, 14, 2) + T(150, 66, 'bóng', { a: 'middle' });
    b += path('M100,124 C124,124 130,132 140,134', 'none', INK, 3);
    b += rc(238, 118, 58, 32, 4) + ci(256, 134, 4, INK, INK, 1) + ci(278, 134, 4, INK, INK, 1) + T(267, 110, 'ổ cắm', { a: 'middle' });
    b += path('M192,98 L200,148 L222,148 L230,98', '#fff', INK, SW) + path('M195,112 Q205,106 215,112 Q222,116 228,112', 'none', BLUE, 2.4);
    b += path('M100,140 C140,190 170,204 200,204 L280,204 C290,204 296,170 288,152', 'none', INK, 3.2);
    return wrap('0 0 320 212', b, cap, 'Bàn thực hành có nhiều chỗ chưa ổn');
  },
  // Trang 5 · thử thách: bố trí bàn nhìn từ trên xuống
  banDen: (cap = 'Nhìn từ trên xuống: bàn đang đun nước bằng đèn cồn và dùng bộ nguồn.') => {
    let b = rc(6, 6, 308, 138, 6, '#fff', GREY, 2.4);
    b += rc(18, 20, 88, 44, 4) + T(62, 48, 'đèn cồn', { a: 'middle' });
    b += rc(18, 76, 88, 44, 4) + T(62, 104, 'lọ cồn', { a: 'middle' });
    b += rc(122, 20, 92, 58, 4) + T(168, 54, 'bộ nguồn', { a: 'middle' });
    b += rc(228, 20, 80, 44, 4) + T(268, 48, 'ổ cắm', { a: 'middle' });
    b += rc(228, 82, 80, 44, 4) + T(268, 110, 'cốc nước', { a: 'middle' });
    b += path('M214,42 L228,42', 'none', INK, 3.4);
    return wrap('0 0 320 152', b, cap, 'Bố trí bàn thực hành nhìn từ trên xuống');
  },
  // Bài tập mẫu D1 · bộ sạc và quạt mini
  sac: (cap = 'Bộ sạc có hai đầu; quạt mini còn hở hai dây.') => {
    let b = rc(60, 14, 120, 86) + T(120, 62, 'bộ sạc', { a: 'middle', w: 700 });
    b += ln(8, 44, 60, 44) + T(8, 30, 'Input') + ln(180, 64, 222, 64) + T(186, 50, 'Output');
    b += ci(262, 108, 22) + [0, 120, 240].map((a) => { const r = a * Math.PI / 180; return path(`M262,108 L${f1(262 + 18 * Math.cos(r))},${f1(108 + 18 * Math.sin(r))}`, 'none', INK, 5); }).join('');
    b += T(262, 80, 'quạt', { a: 'middle' });
    b += path('M254,128 C240,152 160,134 120,146', 'none', RED, 3.2) + T(120, 174, 'dây đỏ', { a: 'middle', c: RED });
    b += path('M272,128 C274,164 240,160 214,160', 'none', INK, 3.2, 'stroke-dasharray="7 5"') + T(236, 182, 'dây xanh', { a: 'middle' });
    return wrap('0 0 320 188', b, cap, 'Bộ sạc và quạt mini');
  },
  // Bài tập mẫu D2 · bốn nhãn trên thùng thu pin
  nhanThung: (cap = 'Bốn nhãn dán trên thùng thu pin cũ.') => {
    let b = tamGiac(46, 50, dauLau) + tronCam(138, 52, thungRac).replace(/r="44"/, 'r="40"') + tronBat(230, 52, matNa).replace(/r="44"/, 'r="40"') + cocVo(300, 56);
    b += so(46, 126, '(1)') + so(138, 126, '(2)') + so(230, 126, '(3)') + so(300, 126, '(4)');
    return wrap('0 0 330 136', b, cap, 'Bốn nhãn trên thùng thu pin');
  },
  // Bài tương tự D2·1: ba nhãn trên tủ hoá chất
  nhanTu: (cap = 'Ba nhãn dán trên tủ hoá chất.') => {
    let b = tamGiac(46, 50, tiaChop) + tronCam(138, 52, ngon).replace(/r="44"/, 'r="40"') + tronBat(230, 52, matNa).replace(/r="44"/, 'r="40"');
    b += so(46, 126, '(1)') + so(138, 126, '(2)') + so(230, 126, '(3)');
    return wrap('0 0 280 136', b, cap, 'Ba nhãn trên tủ hoá chất');
  },
};
