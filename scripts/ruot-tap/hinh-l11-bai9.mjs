// Hình minh hoạ cho ruột tập VL11 · Bài 9 Sóng ngang, sóng dọc, sự truyền năng lượng của sóng cơ (lesson 28).
// Cùng quy tắc với hinh-l11-bai2.mjs: mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox (nhãn phụ ≥ 18), nét ≥ 2,2,
// phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ. Chữ Hi Lạp (λ) lấy từ font KaTeX để không rơi về Helvetica.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh. Xem thử: node scripts/ruot-tap/l11-bai9.mjs --hinh
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const LAM = gk('λ');
const f1 = (v) => (+v).toFixed(1);
const arr = (x1, y1, x2, y2, id, c = INK, dash = '', w = SW) =>
  `<line x1="${f1(x1)}" y1="${f1(y1)}" x2="${f1(x2)}" y2="${f1(y2)}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${f1(x1)}" y1="${f1(y1)}" x2="${f1(x2)}" y2="${f1(y2)}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
// mũi tên hai đầu (đoạn đo)
const doan = (x1, y, x2, id, c = INK) => arr(x1 + 2, y, x2 - 1, y, id, c, '', 2.2) + arr(x2 - 2, y, x1 + 1, y, id, c, '', 2.2);
const phao = (x, y) => `<path d="M${x - 9},${y} Q${x},${y + 13} ${x + 9},${y} Z" fill="#fff" stroke="${RED}" stroke-width="2.4"/>${ln(x, y, x, y - 22, RED, 2.4)}`;
const la = (x, y) => `<path d="M${x - 16},${y} Q${x},${y - 12} ${x + 16},${y} Q${x},${y + 8} ${x - 16},${y} Z" fill="#fff" stroke="${BLUE}" stroke-width="2.4"/>`;

// Dãy vòng lò xo / lớp khí: vị trí cân bằng cách đều d0, lệch u = a·sin(k(x0 − pha)) dọc trục → chỗ sít, chỗ thưa
const vong = (x0, x1, n, a, lam, y1, y2, mau = -1) => {
  let b = '';
  for (let i = 0; i < n; i++) {
    const xc = x0 + (i * (x1 - x0)) / (n - 1);
    const x = xc + a * Math.sin((2 * Math.PI * (xc - x0)) / lam);
    b += ln(x, y1, x, y2, i === mau ? RED : INK, i === mau ? 4 : 2.2);
  }
  return b;
};

export const hinhL11b9 = {
  // Trang 1 · Dự đoán: sỏi rơi, gợn tròn lan tới phao và lá
  hoPhao: (cap = 'Gợn tròn lan ra từ chỗ sỏi rơi (O) về phía phao câu và chiếc lá.') => {
    let b = '';
    const cx = 70, cy = 92;
    [22, 48, 74].forEach((r) => { b += `<ellipse cx="${cx}" cy="${cy}" rx="${r}" ry="${r * 0.42}" fill="none" stroke="${GREY}" stroke-width="2.4"/>`; });
    b += `<circle cx="${cx}" cy="${cy}" r="5" fill="${INK}"/>` + T(cx, cy - 46, 'O', { a: 'middle', w: 700 });
    b += ln(cx, 22, cx, cy - 56, INK, 2, '4 4') + `<circle cx="${cx}" cy="18" r="7" fill="${GREY}"/>` + T(cx + 14, 24, 'sỏi', { size: 18 });
    b += ln(10, cy + 40, 310, cy + 40, GREY, 1.6, '6 6');
    b += phao(205, cy) + T(205, cy + 30, 'phao', { a: 'middle', c: RED });
    b += la(275, cy) + T(275, cy + 30, 'lá', { a: 'middle', c: BLUE });
    return wrap('0 0 320 140', b, cap, 'Mặt hồ, gợn sóng, phao và lá');
  },
  // Trang 1 · thí nghiệm dây nhảy: bướu chạy dọc dây, dải băng buộc giữa dây
  dayNhay: (cap = 'Bướu chạy về phía cột. Dải băng (đỏ) dao động theo phương nào?') => {
    let b = defs('dn1');
    const y0 = 110;
    b += `<rect x="296" y="20" width="14" height="140" fill="#fff" stroke="${INK}" stroke-width="2.4"/>`;
    let d = 'M22,110';
    for (let x = 22; x <= 296; x += 4) {
      const g = Math.exp(-(((x - 110) / 26) ** 2));
      d += ` L${x},${f1(y0 - 52 * g)}`;
    }
    b += `<path d="${d}" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<circle cx="18" cy="${y0}" r="9" fill="#fff" stroke="${INK}" stroke-width="2.4"/>` + T(18, y0 + 32, 'tay', { a: 'middle', size: 18 });
    b += `<rect x="200" y="${y0 - 2}" width="8" height="22" fill="${RED}"/>` + T(204, y0 + 44, 'dải băng', { a: 'middle', c: RED, size: 18 });
    b += arr(110, 32, 200, 32, 'dn1', BLUE) + T(155, 22, 'bướu chạy', { a: 'middle', c: BLUE, size: 18 });
    return wrap('0 0 320 170', b, cap, 'Dây nhảy buộc vào cột, một bướu đang chạy');
  },
  // Trang 2 · lò xo slinky: chỗ sít (A) và chỗ thưa (B), một vòng dán băng
  slinky: (cap = 'Chỗ A và chỗ B chạy dọc lò xo. Vòng đỏ dán băng màu.') => {
    let b = defs('sl1');
    b += vong(20, 300, 29, 8, 140, 50, 110, 14);
    // λ = 140: vùng sít khi du/dx < 0 nhiều nhất → x0 = 20 + 70 (sin giảm qua 0); thưa ở x0 = 20, 160, 300
    b += T(90, 136, 'A', { a: 'middle', w: 700 }) + T(160, 136, 'B', { a: 'middle', w: 700 }) + T(230, 136, 'A', { a: 'middle', w: 700, c: GREY });
    b += arr(40, 26, 280, 26, 'sl1', BLUE) + T(160, 18, 'chiều truyền', { a: 'middle', c: BLUE, size: 18 });
    return wrap('0 0 320 146', b, cap, 'Lò xo slinky có chỗ vòng sít và chỗ vòng thưa');
  },
  // Trang 3 · nguồn nhỏ phát đều: năng lượng trải trên mặt cầu r và 2r
  matCau: (cap = 'Cùng công suất P trải trên mặt cầu bán kính r rồi 2r.') => {
    let b = defs('mc1');
    const cx = 30, cy = 172;
    b += `<circle cx="${cx}" cy="${cy}" r="7" fill="${RED}"/>` + T(cx - 4, cy + 26, 'nguồn', { a: 'start', size: 18 });
    const cung = (r, c, w, dash = '') => `<path d="M${f1(cx + r * Math.cos(1.3))},${f1(cy - r * Math.sin(1.3))} A${r},${r} 0 0 1 ${f1(cx + r * Math.cos(-0.25))},${f1(cy - r * Math.sin(-0.25))}" fill="none" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
    b += cung(85, INK, 2.4) + cung(170, GREY, 2.4, '7 5');
    b += arr(cx, cy, cx + 85 * Math.cos(0.5), cy - 85 * Math.sin(0.5), 'mc1', INK, '', 2.2);
    b += T(cx + 34, cy - 34, 'r', { size: 22, w: 700 });
    b += arr(cx, cy, cx + 170 * Math.cos(0.12), cy - 170 * Math.sin(0.12), 'mc1', GREY, '', 2.2);
    b += T(cx + 130, cy - 26, '2r', { size: 22, w: 700, c: GREY });
    // mảnh diện tích S trên hai mặt
    const manh = (r, c) => { const a1 = 0.85, a2 = 0.85 + 13 / r; /* cùng độ dài cung = cùng diện tích S */ return `<path d="M${f1(cx + r * Math.cos(a2))},${f1(cy - r * Math.sin(a2))} A${r},${r} 0 0 1 ${f1(cx + r * Math.cos(a1))},${f1(cy - r * Math.sin(a1))}" fill="none" stroke="${c}" stroke-width="7"/>`; };
    b += manh(85, RED) + manh(170, RED);
    b += T(cx + 85 * Math.cos(0.92) + 10, cy - 85 * Math.sin(0.92) - 6, 'S', { c: RED, w: 700 }) + T(cx + 170 * Math.cos(0.92) + 10, cy - 170 * Math.sin(0.92) - 4, 'S', { c: RED, w: 700 });
    return wrap('0 0 300 206', b, cap, 'Mặt cầu bán kính r và 2r quanh nguồn nhỏ');
  },
  // Trang 3 · Bẫy 2: đồ thị u–x (trên) và vị trí thật của các lớp (dưới); P, Q, R để HS chỉ chỗ nén, dãn
  uxDoc: (cap = 'Trên: đồ thị u–x lúc t, u > 0 lệch theo chiều +x. Dưới: vị trí thật của các lớp.') => {
    let b = defs('ux1');
    const x0 = 30, x1 = 300, lam = 180, yc = 70, A = 40;
    const X = (x) => x0 + x;
    b += arr(x0, yc, x1 + 12, yc, 'ux1', INK, '', 2) + T(x1 + 12, yc + 24, 'x', { a: 'end' }) + arr(x0, yc + 50, x0, 10, 'ux1', INK, '', 2) + T(x0 + 8, 22, 'u', {});
    let d = '';
    for (let k = 0; k <= 270; k += 3) d += `${k ? 'L' : 'M'}${f1(X(k))},${f1(yc - A * Math.sin((2 * Math.PI * k) / lam))}`;
    b += `<path d="${d}" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
    // P: u = 0 đi xuống (x = λ/2 = 90) · Q: đỉnh (x = λ/4 = 45) · R: u = 0 đi lên (x = λ = 180)
    [[90, 'P'], [45, 'Q'], [180, 'R']].forEach(([x, s]) => {
      const y = yc - A * Math.sin((2 * Math.PI * x) / lam);
      b += `<circle cx="${f1(X(x))}" cy="${f1(y)}" r="5" fill="#fff" stroke="${RED}" stroke-width="2.6"/>` + T(X(x) + 8, y - 8, s, { c: RED, w: 700 });
      b += ln(X(x), yc + 4, X(x), 150, GREY, 1.6, '4 4');
    });
    // dãy lớp: cân bằng cách đều 15, lệch u (thu nhỏ 0,3)
    for (let k = 0; k <= 270; k += 15) { const u = 0.3 * A * Math.sin((2 * Math.PI * k) / lam); b += ln(X(k + u), 130, X(k + u), 170, INK, 2.2); }
    return wrap('0 0 320 180', b, cap, 'Đồ thị u–x của sóng dọc và vị trí các lớp');
  },
  // Trang 4/5 · bài toán mẫu & Dạng 3: loa phát vào ống, các vùng nén đánh số
  ongLoa: ({ so = true, doanNN = '?', doanND = '?', cap = 'Loa phát âm vào ống: các vùng nén (sít) và vùng dãn (thưa).' } = {}) => {
    let b = defs('ol1');
    b += `<path d="M6,70 L22,70 L36,52 L36,128 L22,110 L6,110 Z" fill="#fff" stroke="${INK}" stroke-width="2.4"/>`;
    b += ln(40, 50, 314, 50, INK, 2.4) + ln(40, 130, 314, 130, INK, 2.4);
    const lam = 64;
    b += vong(46, 302, 33, 4.6, lam, 56, 124);
    // vùng nén (sít) ở x0 = 46 + λ/2 + nλ
    const nen = [0, 1, 2, 3].map((n) => 46 + lam / 2 + n * lam);
    if (so) nen.forEach((x, i) => { b += T(x, 44, String(i + 1), { a: 'middle', size: 18, w: 700 }); });
    const y = 152;
    b += ln(nen[0], 132, nen[0], y + 6, GREY, 1.6, '3 3') + ln(nen[1], 132, nen[1], y + 6, GREY, 1.6, '3 3') + ln(nen[2], 132, nen[2], y + 30, GREY, 1.6, '3 3') + ln(nen[2] + lam / 2, 132, nen[2] + lam / 2, y + 30, GREY, 1.6, '3 3');
    b += doan(nen[0], y, nen[1], 'ol1') + T((nen[0] + nen[1]) / 2 - 8, y + 24, doanNN, { a: 'middle', size: 18 });
    b += ln(nen[2], y + 24, nen[2] + lam / 2, y + 24, RED, 2.6) + ln(nen[2], y + 17, nen[2], y + 31, RED, 2.6) + ln(nen[2] + lam / 2, y + 17, nen[2] + lam / 2, y + 31, RED, 2.6) + T(nen[2] + lam / 2 + 6, y + 30, doanND, { size: 18, c: RED });
    return wrap('0 0 320 190', b, cap, 'Loa và ống chứa không khí với các vùng nén, dãn');
  },
  // Dạng 2 · O, phao, lá thẳng hàng
  hoThang: (cap = 'O, phao, lá thẳng hàng, cùng một phía.') => {
    let b = defs('ht1');
    const y = 70, O = 24, k = 28;   // 1 m = 28 đơn vị → 9,6 m = 269
    b += ln(10, y, 312, y, GREY, 1.6, '6 6');
    b += `<circle cx="${O}" cy="${y}" r="6" fill="${INK}"/>` + T(O, y - 18, 'O', { a: 'middle', w: 700 });
    b += phao(O + 6 * k, y - 4) + la(O + 9.6 * k, y - 2);
    b += T(O + 6 * k, y - 32, 'phao', { a: 'middle', c: RED, size: 18 }) + T(O + 9.6 * k, y - 18, 'lá', { a: 'middle', c: BLUE, size: 18 });
    b += doan(O, y + 26, O + 6 * k, 'ht1') + T(O + 3 * k, y + 50, '6,0 m', { a: 'middle' });
    b += doan(O, y + 64, O + 9.6 * k, 'ht1') + T(O + 4.8 * k, y + 88, '9,6 m', { a: 'middle' });
    return wrap('0 0 320 166', b, cap, 'Khoảng cách từ O tới phao và lá');
  },
  // Dạng 5 · nguồn điểm, M cách 3,0 m, N cách 6,0 m, tấm S tại M
  nguonMN: (cap = 'N, M cùng phương truyền; tấm S đặt tại M, vuông góc phương truyền.') => {
    let b = defs('mn1');
    const y = 80, O = 20, k = 46;
    b += `<circle cx="${O}" cy="${y}" r="7" fill="${RED}"/>` + T(O, y + 32, 'nguồn', { a: 'start', size: 18 });
        b += arr(O + 8, y, 304, y, 'mn1', INK, '', 2);
    b += ln(O + 3 * k, y - 30, O + 3 * k, y + 30, BLUE, 6) + T(O + 3 * k + 8, y - 22, 'tấm S', { c: BLUE, size: 18 });
    b += `<circle cx="${O + 3 * k}" cy="${y}" r="5" fill="${INK}"/>` + T(O + 3 * k - 8, y + 26, 'M', { a: 'end', w: 700 });
    b += `<circle cx="${O + 6 * k}" cy="${y}" r="5" fill="${INK}"/>` + T(O + 6 * k, y - 14, 'N', { a: 'middle', w: 700 });
    b += doan(O, y + 50, O + 3 * k, 'mn1') + T(O + 1.5 * k, y + 74, '3,0 m', { a: 'middle' });
    b += doan(O + 3 * k, y + 50, O + 6 * k, 'mn1') + T(O + 4.5 * k, y + 74, '3,0 m', { a: 'middle' });
    return wrap('0 0 320 164', b, cap, 'Nguồn âm điểm, điểm M, N và tấm S');
  },
  // Dạng 6 / thử thách · tâm chấn, trạm đo, sóng P và S cùng đường
  dongDat: (cap = 'Hai sóng xuất phát cùng lúc, cùng đường d. Trạm ghi P trước S.') => {
    let b = defs('dd1');
    const y = 70;
    b += ln(10, 120, 310, 120, INK, 2.4) + Array.from({ length: 12 }, (_, i) => ln(20 + i * 25, 120, 10 + i * 25, 132, GREY, 1.6)).join('');
    b += `<path d="M30,${y} l6,-14 l6,14 l14,-6 l-8,12 l12,8 l-15,0 l-3,14 l-6,-12 l-12,8 l4,-14 l-12,-6 z" fill="${RED}"/>`;
    b += T(36, y + 44, 'tâm chấn', { size: 18, a: 'start' });
    b += `<path d="M282,${y + 14} l12,-26 l12,26 z" fill="#fff" stroke="${INK}" stroke-width="2.4"/>` + T(294, y - 20, 'trạm', { size: 18, a: 'middle' });
    b += arr(62, y - 8, 276, y - 8, 'dd1', INK) + T(170, y - 18, 'sóng P (dọc)', { a: 'middle', size: 18 });
    b += arr(62, y + 14, 220, y + 14, 'dd1', BLUE, '8 5') + T(212, y + 38, 'sóng S (ngang)', { a: 'middle', size: 18, c: BLUE });
    b += doan(30, 158, 294, 'dd1') + T(162, 182, 'd = ?', { a: 'middle' });
    return wrap('0 0 320 190', b, cap, 'Tâm chấn động đất và trạm đo');
  },
};
