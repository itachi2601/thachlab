// Hình minh hoạ cho ruột tập VL10 · Bài 34 Khối lượng riêng. Áp suất chất lỏng (lesson 79). Cùng quy tắc với hinh.mjs/hinh-l10-bai23.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, tự vẽ. Chú thích/hình cạnh ô Dự đoán hay ô điền không lộ đáp án:
// mũi tên áp suất ở M, N và ở mặt trên/dưới khối chìm vẽ BẰNG nhau (HS tự so), mực nước khối gỗ nổi vẽ ở giữa (không đúng tỉ lệ 6/10).
// Xem thử: node scripts/ruot-tap/l10-bai34.mjs --hinh (chụp vào out/hinh-l10-bai34/).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
// chữ Hi Lạp không có trong bộ Source Sans đã nạp → lấy từ KaTeX_Math (đã nạp qua katex.min.css)
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const WATER = '#dfe9f7', OIL = '#f5e6c8', HG = '#c9ced9', WOOD = '#efe2cc';
const arr = (x1, y1, x2, y2, id, c = INK, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${SW}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const rect = (x, y, w, h, fill = '#fff', stroke = 'none', sw = SW, rx = 0) =>
  `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}"/>`;
const dot = (x, y, c = INK) => `<circle cx="${x}" cy="${y}" r="5" fill="${c}"/>`;
// thước đo dọc (mũi tên hai đầu nét mảnh) từ y1 tới y2 tại x, nhãn bên trái/phải
const doc = (x, y1, y2, nhan, ben = 'phai', id = 'dd') => {
  const tick = (y) => ln(x - 6, y, x + 6, y, GREY, 2);
  const tx = ben === 'phai' ? x + 9 : x - 9;
  return ln(x, y1, x, y2, GREY, 2) + tick(y1) + tick(y2) + T(tx, (y1 + y2) / 2 + 7, nhan, { a: ben === 'phai' ? 'start' : 'end' });
};
const ngang = (x1, x2, y, nhan) => ln(x1, y, x2, y, GREY, 2) + ln(x1, y - 6, x1, y + 6, GREY, 2) + ln(x2, y - 6, x2, y + 6, GREY, 2) + T((x1 + x2) / 2, y + 24, nhan, { a: 'middle' });
// bình hở thành thẳng: (x,y) góc trên trái, rộng w, cao h, mực chất lỏng tại yl
const binh = (x, y, w, h, yl, fill = WATER) => rect(x, yl, w, y + h - yl, fill) + `<path d="M${x},${y} L${x},${y + h} L${x + w},${y + h} L${x + w},${y}" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
// bốn mũi tên bằng nhau quanh một điểm (nước ép theo mọi phương)
const bonPhuong = (x, y, L, id) => [[0, -1], [0, 1], [-1, 0], [1, 0]].map(([dx, dy]) => arr(x + dx * (L + 6), y + dy * (L + 6), x + dx * 6, y + dy * 6, id, BLUE)).join('');

// Ống chữ U: lower = chất lỏng dưới (nối hai nhánh), upper = chất lỏng nhánh trái nằm trên mặt phân cách yA; tR = mặt chất lỏng dưới ở nhánh phải
const ongU = ({ tL, yA, tR, upper = OIL, lower = WATER, tenTren = 'dầu', tenDuoi = 'nước', h1 = `h${sb('1')}`, h2 = `h${sb('2')}`, AB = true, yb = 200 }) => {
  let b = '';
  const yi = yb - 30;
  b += rect(60, yA, 40, yb - yA, lower) + rect(60, yi, 200, 30, lower) + rect(220, tR, 40, yb - tR, lower) + rect(60, tL, 40, yA - tL, upper);
  b += `<path d="M60,10 L60,${yb} L260,${yb} L260,10 M100,10 L100,${yi} L220,${yi} L220,10" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
  b += ln(60, yA, 100, yA, INK, 2);
  if (AB) b += ln(100, yA, 220, yA, GREY, 2, '5 4') + dot(80, yA) + dot(240, yA) + T(84, yA + 22, 'A', { w: 700 }) + T(244, yA + 22, 'B', { w: 700 });
  b += doc(40, tL, yA, h1, 'trai') + doc(280, tR, yA, h2, 'phai');
  b += ln(104, (tL + yA) / 2, 122, (tL + yA) / 2, GREY, 2) + T(126, (tL + yA) / 2 + 7, tenTren);
  b += T(160, yb - 8, tenDuoi, { a: 'middle' });
  return b;
};

export const hinhL10b34 = {
  // Trang 1 · Dự đoán: bể hẹp và hồ rộng, cùng sâu 2 m (không nói nơi nào ép mạnh hơn)
  beHo: (cap = 'Cùng sâu 2 m: bể bơi (trái) và hồ rộng (phải).') => {
    let b = '';
    b += binh(20, 34, 76, 136, 50);
    b += rect(130, 50, 186, 120, WATER) + `<path d="M130,34 L130,170 L316,170" fill="none" stroke="${INK}" stroke-width="${SW}"/>` + ln(130, 50, 316, 50, BLUE, 2);
    b += ln(20, 50, 96, 50, BLUE, 2);
    b += T(58, 24, 'bể bơi', { a: 'middle', w: 700 }) + T(222, 24, 'hồ', { a: 'middle', w: 700 });
    b += `<circle cx="58" cy="130" r="9" fill="#fff" stroke="${INK}" stroke-width="${SW}"/><circle cx="250" cy="130" r="9" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += doc(36, 50, 130, '2 m', 'phai') + doc(212, 50, 130, '2 m', 'trai');
    return wrap('0 0 320 180', b, cap, 'Bể bơi hẹp và hồ rộng, cùng độ sâu 2 m');
  },
  // Trang 2 · thí nghiệm: đo thể tích bằng nước dâng
  binhChia: (cap = 'Mực nước trước (trái) và sau khi thả khối nhôm (phải).') => {
    let b = '';
    const ong = (x, yl, khoi) => {
      let s = rect(x, yl, 64, 184 - yl, WATER) + `<path d="M${x},20 L${x},184 L${x + 64},184 L${x + 64},20" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
      for (let y = 40; y <= 170; y += 13) s += ln(x, y, x + (y % 26 === 14 ? 16 : 9), y, INK, 1.8);
      s += ln(x, yl, x + 64, yl, BLUE, 2.4);
      if (khoi) s += rect(x + 18, 150, 28, 28, GREY, INK, 2.4, 2);
      return s;
    };
    b += ong(40, 105, false) + ong(196, 79, true);
    b += T(112, 112, `V${sb('1')}`, { w: 700 }) + T(268, 86, `V${sb('2')}`, { w: 700 });
    b += `<path d="M126,140 Q160,118 186,140" fill="none" stroke="${GREY}" stroke-width="2.4" stroke-dasharray="5 4"/>`;
    return wrap('0 0 320 194', b, cap, 'Bình chia độ trước và sau khi thả khối');
  },
  // Trang 2 · bút chì giữa hai ngón
  butChi: (cap = 'Bút đứng yên giữa hai ngón. So lực ép lên hai ngón; so diện tích chạm.') => {
    let b = '';
    b += rect(14, 46, 56, 76, '#fff', INK, SW, 22) + rect(262, 46, 56, 76, '#fff', INK, SW, 22);
    b += rect(70, 74, 150, 22, '#fff', INK, SW, 2) + `<path d="M220,74 L262,85 L220,96 z" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + `<path d="M248,81.5 L262,85 L248,88.5 z" fill="${INK}"/>`;
    b += T(42, 150, 'ngón cái', { a: 'middle' }) + T(290, 150, 'ngón trỏ', { a: 'middle' });
    b += T(42, 30, 'đầu bằng', { a: 'middle', c: BLUE }) + T(290, 30, 'đầu nhọn', { a: 'middle', c: BLUE });
    b += T(166, 140, '? đau hơn', { a: 'middle', w: 700 });
    return wrap('-16 0 352 160', b, cap, 'Bút chì kẹp giữa hai ngón tay');
  },
  // Trang 3 · áp suất chất lỏng: h đo từ mặt thoáng; mũi tên ở M và N vẽ bằng nhau, HS tự so
  doSau: (cap = 'Mũi tên ở M, N: nước ép lên điểm (không vẽ theo độ lớn).') => {
    let b = defs('ds1');
    b += binh(30, 24, 260, 172, 44);
    b += ln(30, 44, 290, 44, BLUE, 2.4) + T(286, 38, 'mặt thoáng', { a: 'end', c: BLUE });
    b += dot(110, 96) + bonPhuong(110, 96, 22, 'ds1') + T(124, 84, 'M', { w: 700 });
    b += dot(214, 156) + bonPhuong(214, 156, 22, 'ds1') + T(228, 144, 'N', { w: 700 });
    b += doc(60, 44, 96, `h${sb('M')}`, 'phai') + doc(268, 44, 156, `h${sb('N')}`, 'trai');
    return wrap('0 0 320 204', b, cap, 'Hai điểm M, N ở hai độ sâu trong bể nước');
  },
  // Trang 3 · thí nghiệm chai ba lỗ (không vẽ tia nước: HS vẽ)
  chaiLo: (cap = 'Ba lỗ ở ba độ cao. Vẽ thêm tia nước em thấy ở từng lỗ.') => {
    let b = '';
    b += rect(70, 40, 80, 150, WATER) + `<path d="M98,10 L98,24 L70,40 L70,190 L150,190 L150,40 L122,24 L122,10" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
    b += ln(70, 40, 150, 40, BLUE, 2);
    [[80, '1'], [120, '2'], [160, '3']].forEach(([y, s]) => { b += `<circle cx="150" cy="${y}" r="5" fill="#fff" stroke="${INK}" stroke-width="2.4"/>` + T(132, y + 7, s, { a: 'middle', w: 700 }); });
    b += ln(6, 190, 314, 190);
    return wrap('0 0 320 198', b, cap, 'Chai nhựa có ba lỗ ở ba độ cao');
  },
  // Trang 3 · bình thông nhau hai chất lỏng (lý thuyết)
  thongNhau: (cap = 'Dầu (trên) nổi trên nước ở nhánh trái. A ở mặt phân cách, B cùng mức ngang với A.') =>
    wrap('0 0 320 210', ongU({ tL: 40, yA: 130, tR: 60 }), cap, 'Ống chữ U chứa dầu và nước'),
  // Trang 3 · lực đẩy Archimedes: mũi tên ở mặt trên/dưới vẽ bằng nhau, HS tự so
  archimedes: (cap = 'Khối chìm hẳn: mặt trên sâu h<sub>1</sub>, mặt dưới sâu h<sub>2</sub>. So áp lực lên hai mặt.') => {
    let b = defs('ar1');
    b += binh(10, 14, 300, 186, 30);
    b += rect(104, 84, 96, 60, WOOD, INK, SW, 2);
    b += arr(152, 50, 152, 80, 'ar1', RED) + T(160, 66, `F${sb('trên')}`, { c: RED, w: 700 });
    b += arr(152, 178, 152, 148, 'ar1', RED) + T(160, 176, `F${sb('dưới')}`, { c: RED, w: 700 });
    b += ln(200, 84, 254, 84, GREY, 2, '4 4') + ln(200, 144, 290, 144, GREY, 2, '4 4');
    b += doc(248, 30, 84, `h${sb('1')}`, 'trai') + doc(284, 30, 144, `h${sb('2')}`, 'trai');
    return wrap('0 0 320 206', b, cap, 'Khối hộp chìm hẳn trong nước');
  },
  // Trang 4 · bẫy 1: ba bình khác hình dạng, cùng độ sâu
  baBinh: (cap = 'Ba bình khác hình, cùng mực nước h. So p<sub>1</sub>, p<sub>2</sub>, p<sub>3</sub> ở đáy.') => {
    let b = '';
    const yl = 60, yb = 160;
    b += rect(22, yl, 64, yb - yl, WATER) + `<path d="M22,30 L22,${yb} L86,${yb} L86,30" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
    // loe miệng
    b += `<path d="M${120 + 30 * (100 - (yl - 30)) / 130},${yl} L${226 - 30 * (100 - (yl - 30)) / 130},${yl} L196,${yb} L150,${yb} z" fill="${WATER}"/>` + `<path d="M120,30 L150,${yb} L196,${yb} L226,30" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
    // thắt miệng
    b += `<path d="M${248 + 20 * (yl - 30) / 130},${yl} L${312 - 20 * (yl - 30) / 130},${yl} L312,${yb} L248,${yb} z" fill="${WATER}"/>` + `<path d="M268,30 L248,${yb} L312,${yb} L292,30" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
    b += ln(10, yl, 316, yl, BLUE, 2, '6 4') + doc(10, yl, yb, '', 'trai') + T(4, 120, 'h');
    b += T(54, 186, `p${sb('1')}`, { a: 'middle', w: 700 }) + T(173, 186, `p${sb('2')}`, { a: 'middle', w: 700 }) + T(280, 186, `p${sb('3')}`, { a: 'middle', w: 700 });
    return wrap('0 0 320 194', b, cap, 'Ba bình khác hình dạng cùng mực nước');
  },
  // Trang 5 · bài toán mẫu: bể cá nhìn từ trước
  beCa: (cap = 'Bể cá nhìn từ phía trước. M cách đáy 20 cm.') => {
    let b = '';
    b += binh(86, 26, 140, 164, 40);
    b += ln(86, 40, 226, 40, BLUE, 2) + dot(156, 130) + T(166, 124, 'M', { w: 700 });
    b += doc(72, 40, 190, '50 cm', 'trai') + doc(240, 130, 190, '20 cm', 'phai') + ngang(86, 226, 206, '60 cm');
    return wrap('0 0 320 238', b, cap, 'Bể cá chứa nước');
  },
  // Trang 5 · thử thách ★★★: bồn nước trên mái
  bonMai: (cap = 'Bồn trên mái nối ống xuống vòi tầng 1 và vòi tầng 6.') => {
    let b = '';
    b += binh(150, 14, 80, 34, 22) + ln(190, 48, 190, 194, INK, SW) + ln(190, 194, 230, 194, INK, SW) + ln(190, 74, 230, 74, INK, SW);
    b += rect(228, 188, 14, 12, INK) + rect(228, 68, 14, 12, INK) + T(248, 202, 'tầng 1') + T(248, 82, 'tầng 6');
    b += doc(60, 22, 194, '20 m', 'trai') + doc(120, 74, 194, '15 m', 'trai');
    b += ln(66, 22, 150, 22, GREY, 2, '4 4') + ln(66, 194, 190, 194, GREY, 2, '4 4') + ln(126, 74, 190, 74, GREY, 2, '4 4');
    return wrap('0 0 320 210', b, cap, 'Bồn nước trên mái và hai vòi');
  },

  // ===== Bài tập mẫu =====
  khoiHop: (cap = 'Cùng một khối, hai cách đặt: áp lực như nhau, diện tích chạm khác.', L = '15 cm') => {
    let b = ln(6, 96, 314, 96);
    b += rect(24, 78, 90, 18, GREY, INK, SW, 2) + T(69, 68, 'nằm', { a: 'middle', w: 700 });
    b += rect(214, 6, 18, 90, GREY, INK, SW, 2) + T(204, 32, 'đứng', { a: 'end', w: 700 });
    b += ngang(24, 114, 104, L) + doc(252, 6, 96, L, 'phai');
    return wrap('0 0 320 132', b, cap, 'Khối hộp nằm và đứng trên bàn');
  },
  beDau: (cap = 'Bể dầu: M sâu 1,0 m; nắp van ở đáy.', { H = '2,5 m', hM = '1,0 m', ten = 'dầu', fill = OIL, day = 'nắp van', hMday = false } = {}) => {
    let b = binh(70, 6, 170, 82, 10, fill);
    b += ln(70, 10, 240, 10, INK, 2) + T(84, 34, ten, { c: GREY, w: 700 });
    if (hMday) b += dot(140, 54) + T(126, 50, 'M', { w: 700, a: 'end' }) + doc(166, 54, 88, hM, 'phai');
    else b += dot(140, 42) + T(126, 50, 'M', { w: 700, a: 'end' }) + doc(166, 10, 42, hM, 'phai');
    b += rect(100, 84, 36, 9, INK) + T(118, 114, day, { a: 'middle' }) + doc(258, 10, 88, H, 'phai');
    return wrap('0 0 320 120', b, cap, 'Bể chứa chất lỏng có điểm M');
  },
  thungA: (cap = 'Thùng hở, đầy nước. A cách ĐÁY 50 cm; B chưa biết độ sâu.') => {
    let b = binh(80, 8, 140, 112, 12);
    b += ln(80, 12, 220, 12, BLUE, 2);
    b += dot(124, 90) + T(136, 96, 'A', { w: 700 }) + doc(66, 90, 120, '50 cm', 'trai') + ln(70, 90, 118, 90, GREY, 2, '4 4');
    b += dot(184, 54) + T(196, 60, 'B', { w: 700 });
    b += doc(244, 12, 120, '1,8 m', 'phai');
    return wrap('0 0 320 128', b, cap, 'Thùng nước hình trụ có điểm A, B');
  },
  uHg: (cap = 'Nước (trên) nằm trên thuỷ ngân ở nhánh trái; hai nhánh hở.') =>
    wrap('0 0 320 130', ongU({ tL: 14, yA: 84, tR: 72, yb: 124, upper: WATER, lower: HG, tenTren: 'nước', tenDuoi: 'thuỷ ngân', h2: '?' }), cap, 'Ống chữ U chứa nước và thuỷ ngân'),
  goNoi: (cap = 'Khối gỗ nổi, đáy nằm ngang (mực nước vẽ minh hoạ, chưa đúng tỉ lệ).') => {
    let b = binh(20, 40, 280, 86, 72);
    b += ln(20, 72, 300, 72, BLUE, 2);
    b += rect(110, 46, 100, 50, WOOD, INK, SW, 2);
    b += ngang(110, 210, 34, '') + T(160, 24, '20 cm', { a: 'middle' });
    b += doc(86, 46, 96, '', 'trai') + T(78, 62, '10 cm', { a: 'end' }) + doc(234, 72, 96, "h' = ?", 'phai');
    return wrap('0 0 320 132', b, cap, 'Khối gỗ nổi trên mặt nước');
  },
  // ===== Bài tương tự =====
  hoKinh: (cap = 'Hồ sâu 3,0 m; ô kính ở đáy; M cách ĐÁY 1,2 m.') => hinhL10b34.beDau(cap, { H: '3,0 m', hM: '1,2 m', ten: 'nước', fill: WATER, day: 'ô kính', hMday: true }),
  uDau: (cap = 'Dầu (trên) nổi trên nước ở nhánh trái; hai nhánh hở.') =>
    wrap('0 0 320 156', ongU({ tL: 24, yA: 112, tR: 48, yb: 150, h2: '?' }), cap, 'Ống chữ U chứa dầu và nước'),
};
