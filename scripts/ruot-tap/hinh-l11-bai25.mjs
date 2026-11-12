// Hình minh hoạ cho ruột tập VL11 · Bài 25 Năng lượng điện và công suất điện (lesson 44). Cùng quy tắc với hinh.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh. Xem thử: node scripts/ruot-tap/l11-bai25.mjs --hinh (chụp vào out/hinh-l11-bai25/).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
// chữ Hi Lạp/ký hiệu ngoài latin (ℰ, Ω): lấy từ KaTeX_Math/KaTeX_Main để không rơi về Helvetica
const E = '<tspan font-family="KaTeX_Caligraphic">E</tspan>';
const OM = '<tspan font-family="KaTeX_Main">Ω</tspan>';
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const sp = (s) => `<tspan font-size="15" dy="-8">${s}</tspan><tspan dy="8"> </tspan>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const arr = (x1, y1, x2, y2, id, c = INK, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${SW}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const pl = (pts, c = INK, w = SW) => `<polyline points="${pts.map((p) => p.join(',')).join(' ')}" fill="none" stroke="${c}" stroke-width="${w}"/>`;
// nguồn nằm ngang tại (x,y): vạch dài (+) bên trái, vạch ngắn (−) bên phải, nét dây hai bên đến x±g
const nguon = (x, y, g = 30) => ln(x - g, y, x - 5, y) + ln(x + 5, y, x + g, y) + ln(x - 5, y - 18, x - 5, y + 18) + ln(x + 5, y - 9, x + 5, y + 9, INK, 5);
// điện trở nằm ngang tâm (x,y)
const dtro = (x, y, w = 56) => `<rect x="${x - w / 2}" y="${y - 11}" width="${w}" height="22" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
const dtroDoc = (x, y, h = 56) => `<rect x="${x - 11}" y="${y - h / 2}" width="22" height="${h}" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
const dongHo = (x, y, s) => `<circle cx="${x}" cy="${y}" r="15" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(x, y + 7, s, { a: 'middle', w: 700 });
const den = (x, y, r = 15) => `<circle cx="${x}" cy="${y}" r="${r}" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
  + ln(x - r * 0.7, y - r * 0.7, x + r * 0.7, y + r * 0.7, INK, 2.2) + ln(x - r * 0.7, y + r * 0.7, x + r * 0.7, y - r * 0.7, INK, 2.2);
const cauChi = (x, y) => `<rect x="${x - 22}" y="${y - 8}" width="44" height="16" fill="#fff" stroke="${INK}" stroke-width="2.4"/>` + ln(x - 22, y, x + 22, y, INK, 2);
const khung = (x1, y1, x2, y2) => pl([[x1, y1], [x2, y1], [x2, y2], [x1, y2], [x1, y1]]);

// Mạch kín một nguồn (ℰ, r) nối với R: nguồn ở cạnh trên, R ở cạnh dưới. o.A/o.V thêm ampe kế/vôn kế; o.cc thêm cầu chì; o.den thay R bằng đèn
const mach = (cap, o = {}) => {
  const { nE = '', nR = '', A = false, V = false, cc = false, laDen = false, chap = false, gon = false, id = 'mk', label = 'Mạch kín một nguồn' } = o;
  // gon: mạch dẹt (cao 150) để hình cạnh 5 dòng giải không cao hơn khối chữ
  const x1 = 40, x2 = 280, y1 = gon ? 42 : 50, y2 = gon ? 112 : 150, xm = 160;
  let b = defs(id);
  b += ln(x1, y1, xm - 30, y1) + nguon(xm, y1) + ln(xm + 30, y1, x2, y1);
  b += ln(x1, y1, x1, y2) + ln(x2, y1, x2, y2);
  if (nE) b += T(xm, y1 - 26, nE, { a: 'middle' });
  // cạnh dưới
  let xs = [x1];
  if (A) { b += ln(x1, y2, 74, y2) + dongHo(89, y2, 'A'); xs = [104]; }
  if (cc) { b += ln(xs[0], y2, 96, y2) + cauChi(118, y2) + T(118, y2 + 34, 'cầu chì', { a: 'middle' }); xs = [140]; }
  b += ln(xs[0], y2, xm + 10 - 28, y2);
  if (laDen) b += den(xm + 10, y2, 16); else b += dtro(xm + 10, y2);
  b += ln(xm + 10 + 28, y2, x2, y2);
  if (nR) b += T(xm + 10, y2 + 36, nR, { a: 'middle' });
  if (V) { b += ln(xm - 30, y2, xm - 30, y2 + 50, INK, 2.4) + ln(xm + 50, y2, xm + 50, y2 + 50, INK, 2.4) + ln(xm - 30, y2 + 50, xm + 50, y2 + 50, INK, 2.4) + dongHo(xm + 10, y2 + 50, 'V'); }
  if (chap) b += `<path d="M${xm - 34},${y2} C${xm - 24},${y2 - 40} ${xm + 44},${y2 - 40} ${xm + 54},${y2}" fill="none" stroke="${RED}" stroke-width="3.2" stroke-dasharray="7 4"/>` + T(xm + 10, y2 - 36, 'dây chập', { c: RED, w: 700, a: 'middle' });
  return wrap(`0 0 320 ${V ? 214 : gon ? 156 : 196}`, b, cap, label);
};

export const hinhL11b25 = {
  // ===== Trang học bài mới =====
  // Dự đoán "100 W trong 10 giờ là bao nhiêu số": hình chỉ cho thấy công tơ đếm cộng dồn, không ghi phép đổi.
  congTo: (cap = 'Công tơ: dãy số chỉ cộng dồn, mỗi đơn vị là một “số điện”.') => {
    let b = `<rect x="40" y="14" width="220" height="168" rx="10" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<rect x="62" y="46" width="176" height="44" fill="#fff" stroke="${INK}" stroke-width="2.4"/>`;
    ['0', '3', '1', '2', '4', '5'].forEach((d, i) => {
      const x = 62 + i * 29.3;
      if (i) b += ln(x, 46, x, 90, INK, 1.8);
      b += `${i === 5 ? `<rect x="${x}" y="46" width="29.3" height="44" fill="#e8ebf2"/>` : ''}` + T(x + 14.6, 79, d, { a: 'middle', w: 700, size: 26 });
    });
    b += T(150, 38, 'kWh', { a: 'middle', w: 700 });
    b += `<circle cx="150" cy="134" r="22" fill="#fff" stroke="${INK}" stroke-width="2.4"/>` + ln(128, 134, 172, 134, GREY, 2);
    b += T(150, 176, '220 V', { a: 'middle' });
    return wrap('0 0 300 192', b, cap, 'Công tơ điện trong nhà');
  },
  // Nhãn thiết bị: chỉ hai số định mức, phần còn lại để học sinh tự suy ra
  nhan: (cap = 'Nhãn bóng đèn: hai giá trị định mức.') => {
    let b = `<path d="M110,150 L110,124 C70,104 60,40 120,22 C150,14 180,14 200,22 C260,40 250,104 210,124 L210,150 Z" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<rect x="110" y="150" width="100" height="34" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + [160, 168, 176].map((y) => ln(110, y, 210, y, GREY, 1.8)).join('');
    b += `<rect x="96" y="58" width="128" height="50" rx="6" fill="#fff" stroke="${INK}" stroke-width="2.2"/>` + T(160, 80, '220 V', { a: 'middle', w: 700 }) + T(160, 102, '100 W', { a: 'middle', w: 700 });
    return wrap('0 0 320 194', b, cap, 'Bóng đèn có nhãn 220 V – 100 W');
  },
  // Thí nghiệm kiểm nhãn đèn xe máy: sơ đồ đo, không ghi kết quả
  denXe: (cap = 'Ampe kế nối tiếp, vôn kế song song với đèn.') =>
    mach(cap, { nE: 'nguồn chỉnh được', A: true, V: true, laDen: true, id: 'dx', label: 'Mạch đo công suất đèn xe máy' }),
  // Cân bằng công suất: ba khối, vẽ KHÔNG theo tỉ lệ để không lộ số
  canBang: (cap = 'Nguồn phát: một phần mạch ngoài nhận, một phần làm nóng nguồn (không theo tỉ lệ).') => {
    let b = defs('cb1') + defs('cb2');
    b += `<rect x="20" y="60" width="96" height="76" rx="6" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(68, 94, 'nguồn', { a: 'middle', w: 700 }) + T(68, 120, `${E}I`, { a: 'middle' });
    b += arr(118, 84, 182, 52, 'cb1', BLUE) + arr(118, 112, 182, 146, 'cb2', RED, '7 4');
    b += `<rect x="186" y="18" width="116" height="62" rx="6" fill="#fff" stroke="${BLUE}" stroke-width="${SW}"/>` + T(244, 44, 'mạch ngoài', { a: 'middle', w: 700, c: BLUE }) + T(244, 68, 'UI', { a: 'middle' });
    b += `<rect x="186" y="118" width="116" height="62" rx="6" fill="#fff" stroke="${RED}" stroke-width="${SW}" stroke-dasharray="7 4"/>` + T(244, 144, 'nóng trong', { a: 'middle', w: 700, c: RED }) + T(244, 168, `nguồn: I${sp('2')}r`, { a: 'middle' });
    return wrap('0 0 320 196', b, cap, 'Phân chia công suất của nguồn điện');
  },
  // Thí nghiệm hiệu suất hai pin AA: sơ đồ, không vẽ đồ thị (đồ thị lộ ô Rút ra)
  haiPin: (cap = 'Hai pin AA nối tiếp. Đổi R, đọc U và I.') =>
    mach(cap, { nE: `${E}, r`, nR: 'hộp điện trở R', A: true, V: true, id: 'hp', label: 'Mạch đo hiệu suất của hai pin' }),
  // Đoản mạch: chìa khoá nối hai cực ắc quy
  doanMach: (cap = 'Chìa khoá kim loại chạm hai cực ắc quy.') => {
    let b = `<rect x="40" y="70" width="200" height="104" rx="6" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(140, 132, 'ắc quy 12 V', { a: 'middle', w: 700 });
    b += `<rect x="70" y="52" width="30" height="18" fill="#fff" stroke="${INK}" stroke-width="2.4"/><rect x="180" y="52" width="30" height="18" fill="#fff" stroke="${INK}" stroke-width="2.4"/>`;
    b += T(85, 98, '+', { a: 'middle', w: 700, size: 26 }) + T(195, 98, '−', { a: 'middle', w: 700, size: 26 });
    b += `<rect x="64" y="34" width="166" height="16" rx="8" fill="#fff" stroke="${RED}" stroke-width="3.2"/><circle cx="246" cy="42" r="16" fill="#fff" stroke="${RED}" stroke-width="3.2"/>`;
    b += T(150, 24, 'chìa khoá', { a: 'middle', c: RED, w: 700 });
    return wrap('0 0 280 184', b, cap, 'Đoản mạch ắc quy bằng chìa khoá');
  },
  // Bẫy 3: hai đèn nối tiếp, nhãn khác nhau; không ghi đèn nào sáng hơn
  noiTiep: (cap = 'Hai đèn nối tiếp vào 220 V.') => {
    let b = ln(30, 40, 290, 40) + ln(30, 40, 30, 140) + ln(290, 40, 290, 140) + ln(30, 140, 110, 140) + ln(150, 140, 190, 140) + ln(230, 140, 290, 140);
    b += den(130, 140, 20) + den(210, 140, 20);
    b += T(130, 186, '100 W', { a: 'middle', w: 700 }) + T(210, 186, '40 W', { a: 'middle', w: 700 });
    b += `<circle cx="160" cy="40" r="6" fill="#fff" stroke="${INK}" stroke-width="2.4"/>` + T(160, 26, '220 V', { a: 'middle' });
    return wrap('0 0 320 196', b, cap, 'Hai đèn 220 V nối tiếp');
  },
  // Bài toán mẫu: mạch kín ℰ, r nuôi R
  sayMau: (cap = 'Nguồn có r nuôi bộ sấy R.') =>
    mach(cap, { nE: `${E} = 12 V, r = 1,0 ${OM}`, nR: `R = 5,0 ${OM}`, gon: true, id: 'sm', label: 'Mạch kín nguồn nuôi bộ sấy' }),
  // ===== Bài tập mẫu =====
  pinD3: (cap = 'Tìm I trước, rồi tách ba công suất.') =>
    mach(cap, { nE: `6,0 V; 0,40 ${OM}`, nR: `R = 2,6 ${OM}`, gon: true, id: 'p3', label: 'Mạch kín pin và điện trở sưởi' }),
  chapD5: (cap = 'Dây chập nối tắt bộ đèn: điện trở trong vẫn còn trong mạch.') =>
    mach(cap, { nE: `12 V; 0,030 ${OM}`, cc: true, laDen: true, chap: true, id: 'c5', label: 'Mạch đèn xe máy có cầu chì bị chập' }),
};
