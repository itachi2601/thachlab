// Hình minh hoạ cho ruột tập VL11 · Bài 24 Nguồn điện (lesson 43). Cùng quy tắc với hinh.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh. Xem thử: node scripts/ruot-tap/l11-bai24.mjs --hinh (chụp vào out/hinh-l11-bai24/).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
// chữ Hi Lạp/chữ viết tay: Source Sans 3 không có ℰ → lấy từ KaTeX (đã nạp qua katex.min.css)
const sc = '<tspan font-family="KaTeX_Caligraphic">E</tspan>';
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const arr = (x1, y1, x2, y2, id, c = INK, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${SW}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const pl = (pts, c = INK, w = SW) => `<polyline points="${pts.map((p) => p.join(',')).join(' ')}" fill="none" stroke="${c}" stroke-width="${w}"/>`;
// pin nằm trên dây ngang tại x (giữa), y: vạch dài = cực (+), vạch ngắn đậm = cực (−). nguoc: đảo hai cực.
const pin = (x, y, nguoc = false) => {
  const xd = nguoc ? x + 5 : x - 5, xn = nguoc ? x - 5 : x + 5;
  return `<rect x="${x - 9}" y="${y - 20}" width="18" height="40" fill="#fff" stroke="none"/>`
    + ln(xd, y - 18, xd, y + 18, INK, 2.4) + ln(xn, y - 9, xn, y + 9, INK, 6);
};
// pin trên dây dọc tại (x, y): vạch dài (+) ở trên
const pinDoc = (x, y) => `<rect x="${x - 20}" y="${y - 9}" width="40" height="18" fill="#fff" stroke="none"/>`
  + ln(x - 18, y - 5, x + 18, y - 5, INK, 2.4) + ln(x - 9, y + 5, x + 9, y + 5, INK, 6);
const res = (x, y, w = 44, h = 16, nhan = '', doc = false) => (doc
  ? `<rect x="${x - h / 2}" y="${y - w / 2}" width="${h}" height="${w}" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
  : `<rect x="${x - w / 2}" y="${y - h / 2}" width="${w}" height="${h}" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`) + (nhan ? nhan : '');
const dh = (x, y, s) => `<circle cx="${x}" cy="${y}" r="15" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(x, y + 7, s, { a: 'middle', w: 700 });
const den = (x, y) => `<circle cx="${x}" cy="${y}" r="15" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
  + ln(x - 10.6, y - 10.6, x + 10.6, y + 10.6, INK, 2.2) + ln(x - 10.6, y + 10.6, x + 10.6, y - 10.6, INK, 2.2);
const cham = (x, y) => `<circle cx="${x}" cy="${y}" r="4" fill="${INK}"/>`;

export const hinhL11b24 = {
  // ===== Trang học bài mới =====
  // Dự đoán: đèn pha và mô tơ đề cùng mắc hai cực ắc quy (không vẽ điện trở trong — đó là đáp án)
  denPha: (cap = 'Đèn pha và mô tơ đề cùng mắc vào hai cực ắc quy.') => {
    let b = pl([[40, 40], [290, 40]]) + pl([[40, 40], [40, 170], [290, 170]]);
    b += `<rect x="16" y="78" width="48" height="56" rx="4" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(40, 104, '+', { a: 'middle', w: 700 }) + T(40, 126, '−', { a: 'middle', w: 700 });
    b += T(40, 158, 'ắc quy', { a: 'middle' });
    b += ln(130, 40, 130, 170) + den(130, 105) + T(152, 100, 'đèn');
    b += ln(290, 40, 290, 64) + ln(290, 64, 310, 52) + ln(290, 80, 290, 170) + cham(290, 64) + cham(290, 80);
    b += T(278, 78, 'nút đề', { a: 'end' });
    b += `<circle cx="290" cy="128" r="16" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(290, 135, 'M', { a: 'middle', w: 700 }) + T(266, 135, 'mô tơ', { a: 'end' });
    b += cham(130, 40) + cham(130, 170);
    return wrap('0 0 320 186', b, cap, 'Ắc quy nối đèn pha và mô tơ đề');
  },
  // II.1: hai quả cầu tích điện trái dấu nối dây (không vẽ chiều dòng — ô điền hỏi)
  haiQuaCau: (cap = 'Nối dây: dòng chỉ chạy một lát.') => {
    let b = `<path d="M60,66 C110,10 190,10 240,66" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<circle cx="60" cy="96" r="32" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(60, 104, '+q', { a: 'middle', w: 700 });
    b += `<circle cx="240" cy="96" r="32" fill="#fff" stroke="${INK}" stroke-width="${SW}" stroke-dasharray="7 4"/>` + T(240, 104, '−q', { a: 'middle', w: 700 });
    b += T(60, 156, 'A', { a: 'middle', w: 700, size: 24 }) + T(240, 156, 'B', { a: 'middle', w: 700, size: 24 }) + T(150, 104, 'dây', { a: 'middle' });
    return wrap('0 0 300 166', b, cap, 'Hai quả cầu tích điện trái dấu nối bằng dây dẫn');
  },
  // Thí nghiệm: tụ đã nạp và hai pin cùng nuôi điện trở 100 Ω, vôn kế ở hai đầu điện trở
  tuPin: (cap = 'Trái: tụ đã nạp. Phải: hai pin. Cùng R = 100 Ω.') => {
    let b = '';
    // mạch tụ (trái): tụ trên dây trái, điện trở + vôn kế ở dây phải
    b += pl([[30, 30], [120, 30], [120, 150], [30, 150], [30, 30]]);
    b += `<rect x="16" y="80" width="28" height="20" fill="#fff" stroke="none"/>` + ln(14, 84, 46, 84, INK, 3.4) + ln(14, 96, 46, 96, INK, 3.4);
    b += T(75, 98, 'tụ', { a: 'middle', w: 700 });
    b += res(120, 90, 46, 16, '', true);
    b += pl([[120, 56], [146, 56], [146, 75]], INK, 2.2) + pl([[120, 124], [146, 124], [146, 105]], INK, 2.2) + dh(146, 90, 'V');
    // mạch pin (phải)
    b += pl([[196, 30], [286, 30], [286, 150], [196, 150], [196, 30]]);
    b += pinDoc(196, 70) + pinDoc(196, 110);
    b += T(241, 98, 'pin', { a: 'middle', w: 700 });
    b += res(286, 90, 46, 16, '', true);
    b += pl([[286, 56], [312, 56], [312, 75]], INK, 2.2) + pl([[286, 124], [312, 124], [312, 105]], INK, 2.2) + dh(312, 90, 'V');
    return wrap('0 0 334 160', b, cap, 'Tụ đã nạp và hai pin cùng nuôi điện trở');
  },
  // II.2: bên trong nguồn — điện trường hướng từ (+) xuống (−); lực lạ đưa điện tích dương lên
  lucLa: (cap = 'Hai lực tác dụng lên điện tích dương bên trong nguồn.') => {
    let b = defs('lle') + defs('llf') + defs('lld') + defs('llv');
    b += `<rect x="20" y="20" width="150" height="16" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(180, 36, 'cực (+)', { w: 700 });
    b += `<rect x="20" y="174" width="150" height="16" fill="#fff" stroke="${INK}" stroke-width="${SW}" stroke-dasharray="7 4"/>` + T(180, 190, 'cực (−)', { w: 700 });
    b += [36, 154].map((x) => arr(x, 44, x, 164, 'lle', GREY)).join('');
    b += T(46, 116, 'E', { w: 700, c: GREY }) + `<line x1="44" y1="92" x2="60" y2="92" stroke="${GREY}" stroke-width="2" marker-end="url(#llv)"/>`;
    b += `<circle cx="100" cy="105" r="13" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(100, 112, '+', { a: 'middle', w: 700 });
    b += arr(100, 90, 100, 50, 'llf', RED) + T(180, 76, 'lực lạ', { c: RED, w: 700 }) + ln(110, 70, 174, 70, RED, 1.4, '3 3');
    b += arr(100, 120, 100, 160, 'lld', BLUE, '6 4') + T(180, 146, 'lực điện', { c: BLUE, w: 700 }) + ln(110, 140, 174, 140, BLUE, 1.4, '3 3');
    return wrap('0 0 270 200', b, cap, 'Lực lạ và lực điện tác dụng lên điện tích dương trong nguồn');
  },
  // II.3: số liệu U theo I (chỉ chấm điểm, học sinh tự kẻ đường thẳng)
  doThiUI: (cap = 'Năm cặp số đo (I; U) của bảng. Em tự kẻ đường thẳng.') => {
    const X = (i) => 50 + i * 380, Y = (u) => 186 - (u - 0.6) * 160; // I 0–0,7 A; U 0,6–1,6 V
    let b = defs('gx') + defs('gy');
    b += arr(50, 186, 318, 186, 'gx') + arr(50, 186, 50, 14, 'gy');
    [0.8, 1.0, 1.2, 1.4].forEach((u) => { b += ln(50, Y(u), 300, Y(u), GREY, 1.2, '3 4') + T(44, Y(u) + 7, String(u).replace('.', ','), { a: 'end', size: 18 }); });
    [0.1, 0.2, 0.3, 0.4, 0.5, 0.6].forEach((i) => { b += ln(X(i), 186, X(i), 22, GREY, 1.2, '3 4') + T(X(i), 208, String(i).replace('.', ','), { a: 'middle', size: 18 }); });
    [[0.1, 1.4], [0.15, 1.35], [0.3, 1.2], [0.5, 1.0], [0.6, 0.9]].forEach(([i, u]) => {
      b += ln(X(i) - 6, Y(u) - 6, X(i) + 6, Y(u) + 6, INK, 2.8) + ln(X(i) - 6, Y(u) + 6, X(i) + 6, Y(u) - 6, INK, 2.8);
    });
    b += T(58, 24, 'U (V)', { w: 700 }) + T(318, 172, 'I (A)', { a: 'end', w: 700 });
    return wrap('0 0 330 216', b, cap, 'Đồ thị hiệu điện thế hai cực theo cường độ dòng điện');
  },
  // Mạch kín một nguồn (ℰ, r) nối R; tuỳ chọn vôn kế ở hai cực nguồn, khoá K
  mach: (cap = '', o = {}) => {
    const { e = `${sc}, r`, R = 'R', von = false, khoa = false, ampe = false } = o;
    let b = pl([[40, 50], [40, 30], [260, 30], [260, 150], [40, 150], [40, 50]]);
    b += pinDoc(40, 90) + T(66, 98, e, { w: 700 });
    b += res(260, 90, 50, 18, '', true) + T(246, 98, R, { a: 'end', w: 700 });
    if (khoa) b += `<rect x="134" y="140" width="40" height="20" fill="#fff" stroke="none"/>` + ln(134, 150, 170, 136) + cham(134, 150) + cham(172, 150) + T(152, 182, 'K', { a: 'middle', w: 700 });
    if (ampe) b += dh(150, 30, 'A');
    if (von) b += pl([[40, 40], [10, 40], [10, 75]], INK, 2.2) + pl([[40, 140], [10, 140], [10, 105]], INK, 2.2) + dh(10, 90, 'V');
    return wrap(von ? '-14 10 290 180' : '20 10 260 180', b, cap, 'Mạch kín một nguồn và một điện trở');
  },
  // Bộ nguồn hỗn hợp đối xứng: n dãy song song, mỗi dãy m pin nối tiếp, nối R
  honHop: (cap = '', o = {}) => {
    const { n = 2, m = 3, R = 'R' } = o;
    const x0 = 50, x1 = 70 + m * 50, dy = 44;
    let b = '';
    for (let k = 0; k < n; k++) {
      const y = 36 + k * dy;
      b += ln(x0, y, x1, y);
      for (let i = 0; i < m; i++) b += pin(x0 + 40 + i * 50, y);
    }
    const yl = 36 + (n - 1) * dy;
    b += ln(x0, 36, x0, yl + 60) + ln(x1, 36, x1, yl + 60) + ln(x0, yl + 60, x1, yl + 60);
    b += res((x0 + x1) / 2, yl + 60, 50, 18) + T((x0 + x1) / 2, yl + 92, R, { a: 'middle', w: 700 });
    b += cham(x0, 36) + cham(x1, 36) + (n > 1 ? cham(x0, yl) + cham(x1, yl) : '');
    return wrap(`20 10 ${x1 + 10} ${yl + 92}`, b, cap, `Bộ nguồn ${n} dãy, mỗi dãy ${m} pin`);
  },
  // Bốn pin nối tiếp, một pin lắp ngược (bài tương tự dạng 4)
  nguoc: (cap = 'Pin thứ ba bị lắp ngược.') => {
    let b = pl([[30, 40], [290, 40], [290, 120], [30, 120], [30, 40]]);
    [70, 130, 190, 250].forEach((x, i) => { b += pin(x, 40, i === 2); });
    b += T(70, 84, '1', { a: 'middle' }) + T(130, 84, '2', { a: 'middle' }) + T(190, 84, '3', { a: 'middle', w: 700 }) + T(250, 84, '4', { a: 'middle' });
    b += res(160, 120, 50, 18) + T(160, 150, 'R', { a: 'middle', w: 700 });
    return wrap('10 12 300 148', b, cap, 'Bốn pin nối tiếp, một pin lắp ngược');
  },
};
