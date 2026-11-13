// Hình minh hoạ cho ruột tập VL10 · Bài 22 Thực hành: Tổng hợp lực (lesson 67). Quyển Chương 3 lớp 10: bài 22 = tr. 109–120.
// Cùng quy tắc với hinh.mjs: mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt),
// tự vẽ. Chú thích không lộ đáp án ô Dự đoán/ô điền đứng cạnh. Xem thử: node scripts/ruot-tap/l10-bai22.mjs --hinh
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
const ga = '<i style="font-family:KaTeX_Math">α</i>';
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const dot = (x, y, r = 4.5, c = INK) => `<circle cx="${x}" cy="${y}" r="${r}" fill="${c}"/>`;
const rect = (x, y, w, h, extra = '') => `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="#fff" stroke="${INK}" stroke-width="${SW}"${extra}/>`;
// mũi tên vectơ có đầu tam giác đặc (không dùng marker để chắc chắn in được)
const arr = (x1, y1, x2, y2, c = INK, w = SW, dash = '') => {
  const a = Math.atan2(y2 - y1, x2 - x1), h = 11, k = 0.45;
  const p1 = [x2 - h * Math.cos(a - k), y2 - h * Math.sin(a - k)], p2 = [x2 - h * Math.cos(a + k), y2 - h * Math.sin(a + k)];
  return ln(x1, y1, x2 - 5 * Math.cos(a), y2 - 5 * Math.sin(a), c, w, dash) + `<path d="M${x2},${y2} L${p1[0]},${p1[1]} L${p2[0]},${p2[1]} z" fill="${c}"/>`;
};
// cung góc tại (cx, cy), bán kính r, từ góc a1 đến a2 (độ, hệ toạ độ màn hình: y xuống)
const cung = (cx, cy, r, a1, a2) => {
  const p = (a) => [cx + r * Math.cos(a * Math.PI / 180), cy + r * Math.sin(a * Math.PI / 180)];
  const [x1, y1] = p(a1), [x2, y2] = p(a2);
  return `<path d="M${x1},${y1} A${r},${r} 0 0 ${a2 > a1 ? 1 : 0} ${x2},${y2}" fill="none" stroke="${INK}" stroke-width="2.4"/>`;
};
// lực kế treo xiên: thân chữ nhật xoay quanh trục dây, đánh số
const luKe = (x, y, ang, s) => `<g transform="translate(${x},${y}) rotate(${ang})">${rect(-11, -20, 22, 40, ' rx="3"')}${T(0, 7, s, { a: 'middle', w: 700 })}</g>`;

export const hinhL10b22 = {
  // Trang 1 · Dự đoán: khung ảnh treo bằng hai dây (chỉ mô tả cách treo, không nêu kết quả)
  khungAnh: (cap = `Khung ảnh treo bằng hai dây buộc vào hai đinh; ${ga} là góc giữa hai dây.`, nhan = '2,0 N') => {
    const O = [160, 98];
    let b = ln(20, 20, 300, 20, GREY, 2) + dot(80, 20, 6) + dot(240, 20, 6);
    b += ln(80, 20, ...O) + ln(240, 20, ...O) + dot(...O, 5.5) + T(O[0] + 10, O[1] + 4, 'O', { w: 700 });
    b += ln(O[0], O[1], O[0], 128) + rect(124, 128, 72, 46) + T(160, 158, nhan, { a: 'middle', w: 700 });
    b += cung(O[0], O[1], 36, -136, -44);
    b += T(O[0], O[1] - 46, `${gk('α')}`, { a: 'middle', w: 700 });
    b += arr(100, 12, 56, 12, GREY, 2) + arr(220, 12, 264, 12, GREY, 2);
    return wrap('0 0 320 190', b, cap, 'Khung ảnh nặng treo bằng hai dây buộc vào hai đinh trên tường');
  },
  // Trang 1 · II.1 nhắc lại: hai lực chung gốc, hình bình hành, đường chéo
  hbh: (cap = `Hai lực chung gốc O, hợp góc ${ga}; nét đứt hoàn thành hình bình hành.`) => {
    const O = [40, 160], A = [200, 124], B = [118, 52], C = [A[0] + B[0] - O[0], A[1] + B[1] - O[1]];
    let b = ln(...A, ...C, GREY, 2.4, '6 4') + ln(...B, ...C, GREY, 2.4, '6 4');
    b += arr(...O, ...A) + arr(...O, ...B) + arr(...O, ...C, RED, 3.4);
    b += T(A[0] + 4, A[1] + 22, `${gk('F')}${sb('1')}`) + T(B[0] - 34, B[1] + 8, `${gk('F')}${sb('2')}`);
    b += T(C[0] - 4, C[1] - 12, `${gk('F')}`, { c: RED, w: 700, a: 'end' });
    b += cung(O[0], O[1], 38, -12, -60) + T(86, 140, `${gk('α')}`, { w: 700 });
    b += dot(...O, 5);
    return wrap('0 -16 320 200', b, cap, 'Hình bình hành dựng từ hai lực chung gốc, đường chéo là lực tổng hợp');
  },
  // Trang 2 · bố trí thí nghiệm: giá, hai lực kế xiên, nút O, lực kế 3 treo vật
  boTri: (cap = 'Bố trí: ba dây gặp nhau ở nút O; vật kéo O xuống qua lực kế 3.') => {
    const O = [160, 96];
    let b = ln(20, 20, 300, 20, INK, 3.4) + dot(56, 20, 5) + dot(264, 20, 5);
    b += ln(56, 20, 82, 38) + luKe(100, 52, -55, '1') + ln(112, 68, ...O);
    b += ln(264, 20, 238, 38) + luKe(220, 52, 55, '2') + ln(208, 68, ...O);
    b += dot(...O, 6, RED) + T(O[0] + 12, O[1] - 2, 'O', { w: 700 });
    b += ln(O[0], O[1], O[0], 112) + rect(149, 112, 22, 40, ' rx="3"') + T(160, 139, '3', { a: 'middle', w: 700 });
    b += ln(160, 152, 160, 160) + rect(136, 160, 48, 28) + T(160, 181, 'vật', { a: 'middle' });
    b += cung(O[0], O[1], 30, -142, -38) + T(O[0], O[1] - 38, `${gk('α')}`, { a: 'middle', w: 700 });
    return wrap('0 0 320 196', b, cap, 'Giá đỡ, hai lực kế treo xiên, nút O và lực kế thứ ba treo vật nặng');
  },
  // Trang 3 · Bẫy 1: lực kế treo thẳng, chưa móc vật, kim chưa về 0
  soKhong: (cap = 'Lực kế treo thẳng đứng, chưa móc vật gì.') => {
    let b = ln(160, 8, 160, 22) + rect(140, 22, 40, 138, ' rx="4"');
    for (let i = 0; i <= 5; i++) b += ln(140, 40 + i * 20, 152, 40 + i * 20, INK, 2.4) + T(190, 46 + i * 20, String(i), { size: 18 });
    b += arr(100, 51, 138, 51, RED, 3) + T(94, 44, 'kim', { a: 'end', c: RED, w: 700 });
    b += ln(160, 160, 160, 176) + `<path d="M160,176 q-14,0 -14,12 q0,10 14,10" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
    b += T(94, 80, 'N', { a: 'end' });
    return wrap('0 0 320 204', b, cap, 'Lực kế chưa móc vật mà kim nằm dưới vạch 0');
  },
  // Trang 3 · Bẫy 2: hai cách vẽ — chung gốc và nối đuôi (chỉ mô tả cách vẽ)
  gocAlpha: (cap = 'Hai cách vẽ cùng hai lực: (1) chung gốc, (2) nối đuôi.') => {
    let b = T(6, 24, '(1)', { w: 700 }) + T(170, 24, '(2)', { w: 700 });
    const O = [30, 150];
    b += arr(...O, 120, 108) + arr(...O, 98, 56) + cung(O[0], O[1], 34, -25, -62) + T(62, 118, `${gk('α')}`, { w: 700 });
    b += T(118, 130, `${gk('F')}${sb('1')}`) + T(52, 68, `${gk('F')}${sb('2')}`);
    const P = [196, 150], Q = [262, 110], R = [252, 60];
    b += arr(...P, ...Q) + arr(...Q, ...R) + dot(...Q, 3.5);
    b += ln(Q[0], Q[1], 296, 89, GREY, 2.2, '5 4') + cung(Q[0], Q[1], 30, -101, -31) + T(290, 74, `${gk('α')}`, { w: 700 });
    b += cung(Q[0], Q[1], 20, 149, 259) + T(214, 96, '?', { w: 700, c: RED });
    b += T(226, 160, `${gk('F')}${sb('1')}`) + T(208, 66, `${gk('F')}${sb('2')}`);
    return wrap('0 0 320 176', b, cap, 'Hai lực vẽ chung gốc và vẽ nối đuôi');
  },
  // Trang 4 · mẫu bảng đo vẽ: hai lực kế và độ chia (dùng cạnh bảng số liệu)
  doChia: (cap = 'Mặt lực kế 5 N: mỗi độ chia 0,1 N. Nhìn thẳng mặt chỉ.') => {
    let b = rect(24, 40, 272, 70, ' rx="6"');
    for (let i = 0; i <= 50; i++) {
      const x = 40 + i * 5, big = i % 10 === 0, mid = i % 5 === 0;
      b += ln(x, 40, x, 40 + (big ? 22 : mid ? 16 : 10), INK, big ? 2.6 : 1.6);
      if (big) b += T(x, 78, String(i / 10), { a: 'middle', size: 20, w: 700 });
    }
    b += arr(40 + 23 * 5, 128, 40 + 23 * 5, 108, RED, 3) + T(40 + 23 * 5, 152, '?', { a: 'middle', c: RED, w: 700 });
    return wrap('0 0 320 160', b, cap, 'Mặt chia độ của lực kế 5 N');
  },
  // Trang 5 · lưới vẽ hình bình hành, kích thước thật: 1 cm = 40 đơn vị → in rộng 120 mm thì 1 cm = 10 mm. 1 cm ↔ 0,5 N
  luoi: (cap = 'Kích thước thật, ô lớn 1 cm. Tỉ lệ xích: 1 cm ứng với 0,5 N. Chấm O là nút, nét đứt là phương thẳng đứng.') => {
    const X0 = 20, Y0 = 20, W = 440, H = 360; // 11 cm × 9 cm
    let b = '';
    for (let i = 0; i <= 22; i++) b += ln(X0 + i * 20, Y0, X0 + i * 20, Y0 + H, '#c3ccdf', i % 2 === 0 ? 1.2 : .5);
    for (let j = 0; j <= 18; j++) b += ln(X0, Y0 + j * 20, X0 + W, Y0 + j * 20, '#c3ccdf', j % 2 === 0 ? 1.2 : .5);
    b += `<rect x="${X0}" y="${Y0}" width="${W}" height="${H}" fill="none" stroke="${INK}" stroke-width="2.2"/>`;
    const O = [X0 + 220, Y0 + 340];
    b += ln(O[0], O[1] + 20, O[0], Y0, GREY, 2.2, '8 6') + dot(...O, 6, RED) + T(O[0] + 10, O[1] + 24, 'O', { w: 700 });
    return wrap('0 0 480 400', b, cap, 'Lưới ô 1 cm để vẽ hình bình hành lực');
  },
};
