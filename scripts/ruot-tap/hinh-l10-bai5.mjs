// Hình minh hoạ cho ruột tập VL10 · Bài 5 Tốc độ và vận tốc (lesson 50). Cùng quy tắc với hinh.mjs/hinh-l10-bai23.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh; hình sông KHÔNG theo tỉ lệ (đo hình không ra đáp số).
// Xem thử: node scripts/ruot-tap/l10-bai5.mjs --hinh (chụp vào out/hinh-l10-bai5/).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const v = (s) => `v${sb(s)}`;
const arr = (x1, y1, x2, y2, id, c = INK, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${SW}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const R = (d) => (d * Math.PI) / 180;
const f1 = (x) => x.toFixed(1);
const dot = (x, y, r = 4.5, c = INK) => `<circle cx="${x}" cy="${y}" r="${r}" fill="${c}"/>`;
const nguoi = (x, y, tay = '') => `<circle cx="${x}" cy="${y}" r="11" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
  + ln(x, y + 11, x, y + 62) + ln(x, y + 62, x - 14, y + 104) + ln(x, y + 62, x + 16, y + 100) + tay;
// bờ sông có gạch: y, x1..x2, gạch quay ra ngoài sông (len = true: gạch hướng lên)
const bo = (y, x1, x2, len) => ln(x1, y, x2, y) + Array.from({ length: Math.floor((x2 - x1) / 18) }, (_, i) =>
  ln(x1 + 6 + i * 18, y, x1 + i * 18, y + (len ? -8 : 8), GREY, 1.8)).join('');

// Sông: bờ dưới y=184, bờ trên y=34; A ở bờ dưới, B đối diện. Hình KHÔNG theo tỉ lệ.
// kieu 'thang' (mũi vuông góc bờ, trôi tới C) · 'lech' (mũi lệch thượng lưu, tới đúng B) · 'ca2' (cả hai lần, dạng 6)
const song = ({ kieu = 'thang', rong = '120 m', id = 'sg', nuoc = 'nước' } = {}) => {
  const Ax = kieu === 'thang' ? 72 : 150, Ay = 150, By = 30;
  let b = defs(id + 'a') + defs(id + 'b') + defs(id + 'c') + defs(id + 'd');
  b += bo(By, 6, 314, true) + bo(Ay, 6, 314, false);
  b += arr(208, 92, 300, 92, id + 'd', GREY, '7 5') + T(300, 82, nuoc, { c: GREY, a: 'end' });
  b += dot(Ax, Ay) + dot(Ax, By) + T(Ax - 8, Ay - 4, 'A', { a: 'end', w: 700 }) + T(Ax - 8, By + 22, 'B', { a: 'end', w: 700 });
  b += ln(Ax, Ay, Ax, By, GREY, 1.8, '3 5');
  // kích thước bề rộng sông ở mép trái
  b += ln(10, By + 6, 10, Ay - 6, INK, 1.8) + ln(4, By + 6, 16, By + 6, INK, 1.8) + ln(4, Ay - 6, 16, Ay - 6, INK, 1.8);
  b += `<text x="22" y="${(By + Ay) / 2 + 7}" font-size="20" fill="${INK}" font-family="BV,sans-serif" transform="rotate(-90 22 ${(By + Ay) / 2})" text-anchor="middle">${rong}</text>`;
  if (kieu === 'thang' || kieu === 'ca2') {
    const x0 = Ax, Cx = x0 + 180; // C không theo tỉ lệ
    b += ln(x0, Ay, Cx, By, INK, 2, '2 5') + dot(Cx, By) + T(Cx + 8, By + 22, 'C', { w: 700 });
    if (kieu === 'thang') {
      b += arr(x0, Ay, x0, Ay - 60, id + 'a', BLUE) + T(x0 - 8, Ay - 30, v('12'), { c: BLUE, w: 700, a: 'end' });
      b += arr(x0, Ay - 60, x0 + 90, Ay - 60, id + 'b', GREY, '6 4') + T(x0 + 46, Ay - 68, v('23'), { c: GREY, w: 700, a: 'middle' });
      b += arr(x0, Ay, x0 + 90, Ay - 60, id + 'c', RED, '8 4') + T(x0 + 70, Ay - 8, `${v('13')}?`, { c: RED, w: 700 });
    }
  }
  if (kieu === 'lech' || kieu === 'ca2') {
    const L = 68, a = 34, tx = Ax - L * Math.sin(R(a)), ty = Ay - L * Math.cos(R(a));
    b += ln(Ax, Ay, f1(Ax - 104 * Math.sin(R(a))), f1(Ay - 104 * Math.cos(R(a))), INK, 1.6, '2 4') + T(Ax - 104 * Math.sin(R(a)) - 4, Ay - 104 * Math.cos(R(a)) - 4, 'D', { w: 700, a: 'end' });
    b += arr(Ax, Ay, f1(tx), f1(ty), id + 'a', BLUE) + T(tx - 6, ty + 22, v('12'), { c: BLUE, w: 700, a: 'end' });
    b += arr(f1(tx), f1(ty), Ax, f1(ty), id + 'b', GREY, '6 4');
    b += arr(Ax, Ay, Ax, f1(ty), id + 'c', RED, '8 4') + T(Ax + 8, ty + 24, v('13'), { c: RED, w: 700 });
    const p = (deg) => `${f1(Ax - 30 * Math.sin(R(deg)))},${f1(Ay - 30 * Math.cos(R(deg)))}`;
    b += `<path d="M${p(0)} A30,30 0 0 0 ${p(a)}" fill="none" stroke="${INK}" stroke-width="2.2"/>` + T(Ax - 26, Ay - 40, `${gk('α')}`, { a: 'end' });
  }
  return wrap('0 0 320 162', b, '', 'Ca nô qua sông');
};

// Sông khổ hẹp (viewBox 240 × 104, in rộng 38–40 mm): bờ trên y=16, bờ dưới y=88. Không theo tỉ lệ.
const song2 = ({ kieu = 'thang', id = 's2', cap = '' } = {}) => {
  const By = 16, Ay = 88;
  let b = defs(id + 'a') + defs(id + 'b') + defs(id + 'c') + defs(id + 'd');
  b += bo(By, 4, 236, true) + bo(Ay, 4, 236, false);
  b += arr(196, 52, 234, 52, id + 'd', GREY, '6 4');
  if (kieu === 'thang') {
    const Ax = 44;
    b += dot(Ax, Ay) + dot(Ax, By) + T(Ax - 8, Ay - 4, 'A', { a: 'end', w: 700 }) + T(Ax - 6, By + 22, 'B', { a: 'end', w: 700 });
    b += ln(Ax, Ay, Ax + 108, By, INK, 2, '2 5') + dot(Ax + 108, By) + T(Ax + 114, By + 22, 'C', { w: 700 });
    b += arr(Ax, Ay, Ax, Ay - 44, id + 'a', BLUE) + T(Ax - 8, Ay - 28, v('12'), { c: BLUE, w: 700, a: 'end' });
    b += arr(Ax, Ay - 44, Ax + 64, Ay - 44, id + 'b', GREY, '6 4') + T(Ax + 30, Ay - 52, v('23'), { c: GREY, w: 700, a: 'middle', size: 18 });
    b += arr(Ax, Ay, Ax + 64, Ay - 44, id + 'c', RED, '8 4') + T(Ax + 72, Ay - 10, `${v('13')} ?`, { c: RED, w: 700 });
  } else {
    const Ax = 96, a = 32, L = 56, tx = Ax - L * Math.sin(R(a)), ty = Ay - L * Math.cos(R(a));
    b += dot(Ax, Ay) + dot(Ax, By) + T(Ax - 14, Ay - 2, 'A', { a: 'end', w: 700 }) + T(Ax + 8, By + 22, 'B', { w: 700 });
    b += ln(Ax, Ay, Ax, By, GREY, 1.8, '3 5');
    if (kieu === 'ca2') b += ln(Ax, Ay, Ax + 96, By, INK, 2, '2 5') + dot(Ax + 96, By) + T(Ax + 102, By + 22, 'C', { w: 700 });
    b += arr(Ax, Ay, f1(tx), f1(ty), id + 'a', BLUE) + T(tx - 6, ty + 6, 'D', { w: 700, a: 'end' });
    const p = (deg) => `${f1(Ax - 22 * Math.sin(R(deg)))},${f1(Ay - 22 * Math.cos(R(deg)))}`;
    b += `<path d="M${p(0)} A22,22 0 0 0 ${p(a)}" fill="none" stroke="${INK}" stroke-width="2.2"/>` + T(Ax - 6, Ay - 28, gk('α'), { a: 'end' });
  }
  return wrap('0 0 240 104', b, cap, 'Ca nô qua sông');
};
const cap = (svgFig, c) => c ? svgFig.replace(/<\/figure>$/, `<figcaption>${c}</figcaption></figure>`) : svgFig;

export const hinhL10b5 = {
  // Trang 1 · Dự đoán: một vòng đường đua trượt băng
  duongDua: (c = 'Một vòng 111 m, hết khoảng 9 s.') => {
    let b = defs('dd1');
    b += `<rect x="14" y="14" width="292" height="140" rx="70" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<rect x="52" y="52" width="216" height="64" rx="32" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += ln(160, 116, 160, 154, RED, 5) + T(160, 176, 'vạch xuất phát', { a: 'middle', c: RED });
    b += arr(186, 136, 246, 136, 'dd1', BLUE, '6 4') + arr(246, 34, 186, 34, 'dd1', BLUE, '6 4');
    b += T(160, 92, '1 vòng = 111 m', { a: 'middle', w: 700 });
    return wrap('0 0 320 184', b, c, 'Đường đua trượt băng nhìn từ trên xuống');
  },
  // Trang 2 · thí nghiệm: bấm giờ đi bộ qua 10 m
  diBo: (c = 'Bấm giờ lúc chân chạm vạch 1 và vạch 2.') => {
    let b = defs('db1') + defs('db2');
    b += ln(10, 146, 310, 146);
    b += ln(50, 100, 50, 156, RED, 5) + ln(270, 100, 270, 156, RED, 5);
    b += T(50, 92, 'vạch 1', { a: 'middle', c: RED }) + T(270, 92, 'vạch 2', { a: 'middle', c: RED });
    b += nguoi(130, 40);
    b += arr(156, 74, 226, 74, 'db1', BLUE, '6 4');
    b += ln(50, 170, 270, 170, INK, 1.8) + ln(50, 162, 50, 178, INK, 1.8) + ln(270, 162, 270, 178, INK, 1.8);
    b += `<rect x="128" y="160" width="64" height="22" fill="#fff"/>` + T(160, 178, '10,0 m', { a: 'middle', w: 700 });
    b += `<circle cx="282" cy="40" r="20" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + ln(282, 20, 282, 12, INK, 4) + ln(282, 40, 282, 26, INK, 2.4) + ln(282, 40, 292, 44, INK, 2.4);
    return wrap('0 0 320 188', b, c, 'Đo tốc độ đi bộ');
  },
  // Trang 2 · tốc kế
  tocKe: (c = 'Tốc kế xe máy.') => {
    const cx = 120, cy = 116, r = 96;
    let b = `<path d="M${cx - r},${cy} A${r},${r} 0 0 1 ${cx + r},${cy}" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    for (let k = 0; k <= 120; k += 20) {
      const a = R(180 - k * 1.5), x1 = cx + r * Math.cos(a), y1 = cy - r * Math.sin(a), x2 = cx + (r - 14) * Math.cos(a), y2 = cy - (r - 14) * Math.sin(a);
      b += ln(f1(x1), f1(y1), f1(x2), f1(y2), INK, 2.4);
      if (k % 40 === 0) b += T(cx + (r - 34) * Math.cos(a), cy - (r - 34) * Math.sin(a) + 7, String(k), { a: 'middle' });
    }
    const a = R(180 - 50 * 1.5);
    b += ln(cx, cy, f1(cx + (r - 20) * Math.cos(a)), f1(cy - (r - 20) * Math.sin(a)), RED, 4) + dot(cx, cy, 7, INK);
    b += T(cx, cy + 26, 'km/h', { a: 'middle' });
    return wrap('0 0 240 146', b, c, 'Tốc kế');
  },
  // Trang 2 · xe đồ chơi nửa vòng tròn
  nuaVong: (c = 'Xe đi nửa vòng từ A tới B. M là một điểm trên cung.') => {
    let b = defs('nv1') + defs('nv2');
    const O = [160, 158], Rr = 118, A = [O[0] - Rr, O[1]], B = [O[0] + Rr, O[1]];
    b += `<path d="M${A[0]},${A[1]} A${Rr},${Rr} 0 0 1 ${B[0]},${B[1]}" fill="none" stroke="${BLUE}" stroke-width="${SW}" stroke-dasharray="9 5" marker-end="url(#nv1)"/>`;
    b += arr(A[0], A[1], B[0] - 4, B[1], 'nv2', RED);
    b += dot(O[0], O[1], 3.5) + T(O[0], O[1] - 10, 'O', { a: 'middle' });
    b += ln(O[0], O[1], O[0] - Rr * Math.cos(R(60)), O[1] - Rr * Math.sin(R(60)), GREY, 1.8, '4 4') + T(112, 112, 'R');
    const M = [O[0] + Rr * Math.cos(R(45)), O[1] - Rr * Math.sin(R(45))];
    b += dot(f1(M[0]), f1(M[1]), 5) + T(M[0] + 10, M[1] - 6, 'M', { w: 700 });
    b += T(A[0] - 6, A[1] + 6, 'A', { a: 'end', w: 700 }) + T(B[0] + 6, B[1] + 6, 'B', { w: 700 });
    b += T(160, 28, 's = ?', { a: 'middle', c: BLUE, w: 700 }) + T(160, 186, 'd = ?', { a: 'middle', c: RED, w: 700 });
    return wrap('0 0 320 194', b, c, 'Nửa vòng tròn');
  },
  // Trang 3 · ba trường hợp cộng vận tốc (độ dài không theo tỉ lệ của bài nào)
  baTH: (c = 'Nối đuôi nhau; mũi tên đứt đỏ là tổng.') => {
    let b = defs('bt1') + defs('bt2') + defs('bt3');
    const ba = (x0, y0, x1, y1, x2, y2) => arr(x0, y0, x1, y1, 'bt1', BLUE) + arr(x1, y1, x2, y2, 'bt2', GREY, '6 4') + arr(x0, y0 + (y2 === y0 ? 16 : 0), x2, y2 + (y2 === y0 ? 16 : 0), 'bt3', RED, '8 4');
    b += T(4, 40, 'cùng', { w: 700 }) + ba(90, 34, 190, 34, 280, 34) + T(140, 24, v('12'), { c: BLUE, a: 'middle' }) + T(236, 24, v('23'), { c: GREY, a: 'middle' }) + T(290, 58, '?', { c: RED, w: 700 });
    b += T(4, 108, 'ngược', { w: 700 }) + arr(90, 104, 250, 104, 'bt1', BLUE) + arr(250, 92, 172, 92, 'bt2', GREY, '6 4') + ln(250, 88, 250, 108, GREY, 1.4) + arr(90, 120, 170, 120, 'bt3', RED, '8 4') + T(120, 96, v('12'), { c: BLUE, a: 'middle' }) + T(262, 98, v('23'), { c: GREY }) + T(180, 126, '?', { c: RED, w: 700 });
    b += T(4, 176, 'vuông', { w: 700 }) + arr(110, 196, 110, 150, 'bt1', BLUE) + arr(110, 150, 220, 150, 'bt2', GREY, '6 4') + arr(110, 196, 220, 152, 'bt3', RED, '8 4');
    b += T(100, 180, v('12'), { c: BLUE, a: 'end' }) + T(165, 140, v('23'), { c: GREY, a: 'middle' }) + T(176, 194, '?', { c: RED, w: 700 });
    b += `<path d="M110,162 L122,162 L122,150" fill="none" stroke="${INK}" stroke-width="1.8"/>`;
    return wrap('0 0 300 204', b, c, 'Ba trường hợp cộng vận tốc');
  },
  // Trang 3 · thí nghiệm bút vẽ trên giấy bị kéo
  giayKeo: (c = 'Vệt mực trên giấy có dạng gì?') => {
    let b = defs('gk1') + defs('gk2');
    b += `<rect x="8" y="58" width="304" height="78" fill="#fff" stroke="${GREY}" stroke-width="2.4"/>`;
    b += `<rect x="146" y="10" width="26" height="150" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
    for (let y = 22; y < 160; y += 16) b += ln(146, y, 156, y, INK, 1.6);
    b += T(196, 30, 'thước', {});
    b += arr(138, 124, 138, 74, 'gk1', RED) + T(130, 104, 'bút', { c: RED, a: 'end', w: 700 });
    b += arr(196, 148, 300, 148, 'gk2', GREY, '6 4') + T(70, 156, 'kéo giấy', { c: GREY, a: 'middle' });
    b += T(60, 104, '?', { w: 700, a: 'middle' });
    return wrap('0 0 320 166', b, c, 'Vẽ trên giấy đang bị kéo');
  },
  // Trang 4 · bẫy 1: đi rồi về
  diVe: (c = 'Đi 3 km rồi về chỗ cũ: s = ?, d = ?') => {
    let b = defs('dv1') + defs('dv2');
    b += ln(16, 84, 224, 84) + ln(16, 76, 16, 92) + ln(224, 76, 224, 92);
    b += T(16, 112, '0', { a: 'middle' }) + T(216, 112, '3 km', { a: 'middle' });
    b += arr(20, 30, 216, 30, 'dv1', BLUE) + T(120, 22, 'đi', { c: BLUE, a: 'middle', w: 700 });
    b += arr(220, 58, 24, 58, 'dv2', RED, '8 4') + T(120, 80, 'về', { c: RED, a: 'middle', w: 700 });
    return wrap('0 0 240 118', b, c, 'Đi rồi về');
  },
  // Trang 5 · bài toán mẫu ca nô qua sông (không theo tỉ lệ)
  caNo: (c = 'Hình không theo tỉ lệ. Đường đi thật A → C.') => cap(song({ id: 'cn' }), c),
  // Trang 4 · thử thách ★★★: mũi chếch lên thượng lưu
  caNoLech: (c = 'Hình không theo tỉ lệ.') => song2({ kieu: 'lech', id: 'cl', cap: c }),

  // ===== Bài tập mẫu ===== (khổ hẹp: viewBox rộng 240 để in rộng 40 mm chữ vẫn ≈ 3,3 mm)
  chayBo: (c = '') => {
    let b = ln(10, 46, 230, 46) + dot(10, 46, 5) + dot(104, 46, 4) + dot(230, 46, 5);
    b += T(57, 30, '4 phút', { a: 'middle', w: 700 }) + T(57, 74, '4 m/s', { a: 'middle' });
    b += T(167, 30, '6 phút', { a: 'middle', w: 700 }) + T(167, 74, '3 m/s', { a: 'middle' });
    return wrap('0 0 240 84', b, c, 'Chạy bộ hai đoạn');
  },
  loTrinh: (c = '') => {
    let b = defs('lt1') + defs('lt2');
    const A = [16, 92], B = [176, 92], C = [176, 14];
    b += arr(A[0], A[1], B[0] - 4, B[1], 'lt1', INK) + arr(B[0], B[1], C[0], C[1] + 4, 'lt1', INK);
    b += arr(A[0], A[1], C[0] - 4, C[1] + 4, 'lt2', RED, '8 4') + T(88, 44, 'd = ?', { c: RED, w: 700, a: 'end' });
    b += `<path d="M${B[0] - 12},${B[1]} L${B[0] - 12},${B[1] - 12} L${B[0]},${B[1] - 12}" fill="none" stroke="${INK}" stroke-width="1.8"/>`;
    b += T(A[0], A[1] + 22, 'A', { w: 700, a: 'middle' }) + T(B[0], B[1] + 22, 'B', { w: 700, a: 'middle' }) + T(C[0] - 8, C[1] + 8, 'C', { w: 700, a: 'end' });
    b += T(96, 86, '480 m', { a: 'middle' }) + T(184, 60, '360', {});
    b += arr(226, 60, 226, 22, 'lt1', INK) + T(226, 84, 'B', { a: 'middle', size: 18 }) + T(214, 108, '(bắc)', { a: 'middle', size: 18 });
    return wrap('0 0 240 118', b, c, 'Lộ trình gấp khúc');
  },
  beBoi: (c = '') => {
    let b = defs('bb1') + defs('bb2') + defs('bb3');
    b += `<rect x="8" y="30" width="224" height="58" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += arr(20, 48, 150, 48, 'bb1', BLUE) + T(160, 55, '40 s', { c: BLUE });
    b += arr(220, 72, 90, 72, 'bb2', RED, '8 4') + T(80, 79, '50 s', { c: RED, a: 'end' });
    b += arr(80, 14, 150, 14, 'bb3', INK) + T(158, 20, 'chiều +', {});
    b += T(8, 108, 'đầu', {}) + T(232, 108, 'cuối', { a: 'end' }) + T(120, 108, '50 m', { a: 'middle' });
    return wrap('0 0 240 114', b, c, 'Bể bơi');
  },
  moTo: (c = '') => {
    let b = defs('mt1');
    b += ln(4, 74, 236, 74);
    b += `<rect x="10" y="46" width="44" height="16" rx="4" fill="#fff" stroke="${INK}" stroke-width="${SW}"/><circle cx="20" cy="66" r="7" fill="#fff" stroke="${INK}" stroke-width="${SW}"/><circle cx="46" cy="66" r="7" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<circle cx="168" cy="64" r="9" fill="none" stroke="${INK}" stroke-width="${SW}"/><circle cx="196" cy="64" r="9" fill="none" stroke="${INK}" stroke-width="${SW}"/>` + ln(168, 64, 182, 46, INK, 2.4) + ln(182, 46, 196, 64, INK, 2.4) + `<circle cx="184" cy="32" r="7" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += arr(58, 40, 100, 40, 'mt1', BLUE) + T(8, 26, '60 km/h', { c: BLUE });
    b += arr(204, 40, 234, 40, 'mt1', BLUE) + T(220, 26, '?', { c: BLUE, a: 'middle', w: 700 });
    b += ln(32, 92, 182, 92, INK, 1.8) + ln(32, 85, 32, 99, INK, 1.8) + ln(182, 85, 182, 99, INK, 1.8);
    b += `<rect x="80" y="82" width="56" height="20" fill="#fff"/>` + T(108, 99, '10 km', { a: 'middle', w: 700 });
    return wrap('0 0 240 104', b, c, 'Mô tô và vận động viên');
  },
  caNoD5: (c = '') => song2({ id: 'c5', cap: c }),
  caNoD6: (c = '') => song2({ kieu: 'ca2', id: 'c6', cap: c }),
};
