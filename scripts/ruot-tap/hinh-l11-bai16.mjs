// Hình minh hoạ cho ruột tập VL11 · Bài 16 Lực tương tác giữa hai điện tích (lesson 35). Cùng quy tắc với hinh.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh. Xem thử: node scripts/ruot-tap/l11-bai16.mjs --hinh (chụp vào out/hinh-l11-bai16/).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
// chữ Hi Lạp: Source Sans 3 chỉ nạp latin/vietnamese, α ε φ rơi về Helvetica → lấy từ KaTeX_Math (đã nạp qua katex.min.css)
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const arr = (x1, y1, x2, y2, id, c = INK, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${SW}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const f1 = (v) => (+v).toFixed(1);
const dat = (x1, x2, y) => ln(x1, y, x2, y) + Array.from({ length: Math.floor((x2 - x1) / 18) }, (_, i) =>
  ln(x1 + 8 + i * 18, y, x1 + i * 18, y + 8, GREY, 1.8)).join('');
// điện tích: vòng tròn có dấu (+ / − / ?) ở giữa
const q = (x, y, s, r = 15) => `<circle cx="${x}" cy="${y}" r="${r}" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
  + T(x, y + 7, s, { a: 'middle', w: 700, size: 22 });
// thước đo khoảng cách hai đầu có gạch
const doan = (x1, x2, y, nhan) => ln(x1, y, x2, y, GREY, 2) + ln(x1, y - 6, x1, y + 6, GREY, 2) + ln(x2, y - 6, x2, y + 6, GREY, 2)
  + T((x1 + x2) / 2, y - 6, nhan, { a: 'middle' });

// Tam giác vuông tại C: A phía trên C, B bên phải C. o.luc = [hướng F1, hướng F2] ('ve' = về phía điện tích, 'xa' = ra xa) → vẽ lực + hợp lực.
const tamGiac = (cap, o = {}) => {
  const { ca = 3, cb = 4, s = 30, qa = '−', qb = '+', q0 = '+', la = '3 cm', lb = '4 cm', luc = null, id = 'tg' } = o;
  const x0 = luc ? 150 : 40, y0 = 190, A = [x0, y0 - ca * s], B = [x0 + cb * s, y0];
  let b = defs(id + 'a') + defs(id + 'b') + defs(id + 'c');
  b += ln(...A, x0, y0) + ln(x0, y0, ...B) + ln(...A, ...B, GREY, 2, '6 4');
  b += `<path d="M${x0 + 14},${y0} L${x0 + 14},${y0 - 14} L${x0},${y0 - 14}" fill="none" stroke="${INK}" stroke-width="2"/>`;
  if (luc) {
    const L = 64, u1 = luc[0] === 've' ? -1 : 1, u2 = luc[1] === 've' ? 1 : -1; // F1 dọc CA (y), F2 dọc CB (x)
    const e1 = [x0, y0 + u1 * L], e2 = [x0 + u2 * L, y0];
    b += ln(e1[0], e1[1], e1[0] + u2 * L, e1[1], GREY, 1.8, '4 4') + ln(e2[0], e2[1], e2[0], e2[1] + u1 * L, GREY, 1.8, '4 4');
    b += arr(x0, y0, ...e1, id + 'a', RED) + T(e1[0] - 8, e1[1] + (u1 < 0 ? 24 : -4), `F${sb('1')}`, { c: RED, w: 700, a: 'end' });
    b += arr(x0, y0, ...e2, id + 'b', BLUE, '7 4') + T(e2[0], e2[1] + 24, `F${sb('2')}`, { c: BLUE, w: 700, a: 'middle' });
    b += arr(x0, y0, e2[0], e1[1], id + 'c', INK) + T(e2[0] + u2 * 6, e1[1] - 8, 'F', { w: 700, a: u2 < 0 ? 'end' : 'start' });
  }
  b += q(...A, qa) + T(A[0] + 22, A[1] + 7, 'A', { w: 700 });
  b += q(...B, qb) + T(B[0] - 4, B[1] - 22, 'B', { w: 700, a: 'end' });
  b += q(x0, y0, q0) + T(x0 - 20, y0 + 26, 'C', { w: 700, a: 'end' });
  b += T(x0 + 10, (A[1] + y0) / 2 + 8, la) + T((x0 + B[0]) / 2, y0 + 30, lb, { a: 'middle' });
  return wrap(`0 0 ${Math.max(B[0] + 24, 300)} 226`, b, cap, 'Ba điện tích ở ba đỉnh tam giác vuông tại C');
};

// Ba điện tích thẳng hàng: A, B cố định; o.c = vị trí C (null → đánh số ba miền để học sinh tự xét)
const thangHang = (cap, o = {}) => {
  const { xa = 50, xb = 250, qa = '+', qb = '+', c = null, ra = `r${sb('1')}`, rb = `r${sb('2')}`, ab = '', id = 'th' } = o;
  let b = defs(id + 'a') + defs(id + 'b');
  b += ln(8, 70, 312, 70, GREY, 2);
  b += q(xa, 70, qa) + T(xa, 40, 'A', { a: 'middle', w: 700 }) + q(xb, 70, qb) + T(xb, 40, 'B', { a: 'middle', w: 700 });
  if (c != null) {
    b += q(c, 70, '+', 12) + T(c, 40, 'C', { a: 'middle', w: 700 });
    b += arr(c + 14, 70, c + 46, 70, id + 'a', RED) + arr(c - 14, 70, c - 46, 70, id + 'b', BLUE, '7 4');
    b += T(c + 34, 100, `F${sb('1')}`, { c: RED, w: 700, a: 'middle' }) + T(c - 34, 100, `F${sb('2')}`, { c: BLUE, w: 700, a: 'middle' });
    b += doan(xa, c, 134, ra) + doan(c, xb, 134, rb);
  } else {
    b += T((8 + xa) / 2 + 2, 62, '(1)', { a: 'middle', w: 700 }) + T((xa + xb) / 2, 62, '(2)', { a: 'middle', w: 700 }) + T((xb + 312) / 2, 62, '(3)', { a: 'middle', w: 700 });
    if (ab) b += doan(xa, xb, 134, ab);
  }
  return wrap('0 0 320 146', b, cap, 'Ba điện tích trên một đường thẳng');
};

// Các quả cầu giống hệt: trước khi chạm (ghi điện tích) → sau khi tách (dấu ?)
const chamTach = (cap, qs, id = 'ct') => {
  const n = qs.length, d = 76, x0 = 40, xm = x0 + (n - 1) * d + 34, x1 = xm + 64, d2 = 44;
  let b = defs(id);
  qs.forEach((s, i) => { b += q(x0 + i * d, 50, s[0] === '−' ? '−' : '+', 17) + T(x0 + i * d, 98, s, { a: 'middle' }); });
  b += arr(xm, 50, xm + 40, 50, id, INK);
  qs.forEach((_, i) => { b += q(x1 + i * d2, 50, '?', 17); });
  return wrap(`0 0 ${x1 + (n - 1) * d2 + 24} 110`, b, cap, 'Quả cầu giống hệt chạm nhau rồi tách ra');
};

export const hinhL11b16 = {
  // ===== Trang học bài mới =====
  sieuThi: (cap = 'Chạm tay vào kệ sắt: tách!') => {
    let b = dat(8, 292, 186);
    b += `<rect x="206" y="34" width="70" height="152" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + [76, 118, 156].map((y) => ln(206, y, 276, y)).join('');
    b += T(241, 26, 'kệ sắt', { a: 'middle' });
    b += `<circle cx="70" cy="44" r="14" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + ln(70, 58, 70, 130) + ln(70, 130, 54, 180) + ln(70, 130, 86, 180)
      + ln(70, 80, 182, 96) + ln(70, 80, 40, 112);
    b += `<rect x="40" y="178" width="22" height="8" fill="${INK}"/><rect x="78" y="178" width="22" height="8" fill="${INK}"/>`;
    b += `<path d="M184,96 L191,86 L196,104 L205,92" fill="none" stroke="${RED}" stroke-width="3.2"/>` + T(176, 74, 'tách!', { c: RED, w: 700, a: 'middle' });
    return wrap('0 0 300 196', b, cap, 'Người chạm tay vào kệ sắt ở siêu thị');
  },
  lonNhom: (cap = 'Thước đưa lại gần, chưa chạm lon.') => {
    let b = defs('ln1') + dat(8, 292, 150);
    b += `<rect x="58" y="22" width="26" height="104" rx="3" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + [46, 74, 102].map((y) => T(71, y + 7, '−', { a: 'middle', w: 700, size: 24 })).join('');
    b += T(71, 16, 'thước nhựa', { a: 'middle' });
    b += `<circle cx="210" cy="110" r="38" fill="#fff" stroke="${INK}" stroke-width="${SW}"/><circle cx="210" cy="110" r="26" fill="none" stroke="${GREY}" stroke-width="1.8"/>`;
    b += T(210, 117, 'lon', { a: 'middle', w: 700 });
    return wrap('0 0 300 160', b, cap, 'Thước nhựa đã cọ tóc đưa gần lon nhôm');
  },
  haiDienTich: (cap = 'F<sub>12</sub>: lực q<sub>1</sub> tác dụng lên q<sub>2</sub>; F<sub>21</sub>: lực q<sub>2</sub> lên q<sub>1</sub>.') => {
    let b = defs('hd1') + defs('hd2');
    b += T(4, 30, '(a)', { w: 700 }) + q(118, 50, '+') + q(192, 50, '+') + T(118, 84, `q${sb('1')}`, { a: 'middle' }) + T(192, 84, `q${sb('2')}`, { a: 'middle' });
    b += arr(102, 50, 46, 50, 'hd1', RED) + T(56, 36, `F${sb('21')}`, { c: RED, w: 700 }) + arr(208, 50, 264, 50, 'hd1', RED) + T(232, 36, `F${sb('12')}`, { c: RED, w: 700 });
    b += T(4, 122, '(b)', { w: 700 }) + q(70, 142, '+') + q(240, 142, '−') + T(70, 176, `q${sb('1')}`, { a: 'middle' }) + T(240, 176, `q${sb('2')}`, { a: 'middle' });
    b += arr(86, 142, 140, 142, 'hd2', BLUE, '7 4') + T(100, 128, `F${sb('21')}`, { c: BLUE, w: 700 }) + arr(224, 142, 170, 142, 'hd2', BLUE, '7 4') + T(178, 128, `F${sb('12')}`, { c: BLUE, w: 700 });
    return wrap('0 0 300 186', b, cap, 'Lực giữa hai điện tích cùng dấu và trái dấu');
  },
  canDien: (cap = 'B đặt thẳng trên A. Đổi r, đọc số cân.') => {
    let b = defs('cd1');
    b += `<rect x="40" y="166" width="190" height="34" rx="5" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(56, 190, 'cân');
    b += `<rect x="128" y="172" width="94" height="22" rx="3" fill="#fff" stroke="${INK}" stroke-width="2"/>` + T(214, 190, '0,92 g', { a: 'end', w: 700 });
    b += ln(110, 166, 110, 130, GREY, 6) + q(110, 114, '+', 15) + T(132, 120, 'A', { w: 700 });
    b += ln(110, 6, 110, 32, GREY, 6) + q(110, 48, '+', 15) + T(132, 54, 'B', { w: 700 });
    b += ln(172, 48, 172, 114, GREY, 2) + ln(164, 48, 180, 48, GREY, 2) + ln(164, 114, 180, 114, GREY, 2) + T(184, 88, 'r');
    b += arr(76, 104, 76, 150, 'cd1', RED) + T(68, 140, 'F', { c: RED, w: 700, a: 'end' });
    return wrap('0 0 270 206', b, cap, 'Cân điện tử đo lực đẩy giữa hai quả cầu');
  },
  tongHop: (cap = 'q<sub>0</sub> &gt; 0 tại C: A hút, B đẩy. Hợp lực theo quy tắc hình bình hành.') =>
    tamGiac(cap, { luc: ['ve', 'xa'], id: 'th2' }),
  canBang: (cap = 'q<sub>1</sub>, q<sub>2</sub> cùng dấu: F<sub>1</sub> (đỏ) do q<sub>1</sub>, F<sub>2</sub> (xanh) do q<sub>2</sub>.') =>
    thangHang(cap, { c: 184, id: 'cb' }),
  quaCauTreo: (cap = 'Quả bên phải: P, F, T. F + P nằm dọc dây.') => {
    let b = defs('qc1') + defs('qc2') + defs('qc3');
    const O = [160, 18], L = [82, 96], R = [238, 96];
    b += ln(110, 18, 210, 18, INK, 4) + ln(...O, ...L, INK, 2.4) + ln(...O, ...R, INK, 2.4) + ln(160, 18, 160, 132, GREY, 1.8, '5 4');
    b += `<path d="M146,32 A20,20 0 0 0 174,32" fill="none" stroke="${INK}" stroke-width="2"/>` + T(160, 64, '90°', { a: 'middle' });
    b += `<circle cx="${L[0]}" cy="${L[1]}" r="12" fill="#fff" stroke="${INK}" stroke-width="${SW}"/><circle cx="${R[0]}" cy="${R[1]}" r="12" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += arr(250, 96, 302, 96, 'qc1', RED) + T(300, 86, 'F', { c: RED, w: 700, a: 'end' });
    b += arr(238, 108, 238, 164, 'qc2', BLUE, '7 4') + T(248, 160, 'P', { c: BLUE, w: 700 });
    b += arr(230, 88, 204, 62, 'qc3', INK) + T(214, 92, 'T', { w: 700, a: 'end' });
    b += doan(82, 238, 196, 'r = 6 cm');
    return wrap('0 0 320 206', b, cap, 'Hai quả cầu tích điện treo vào một điểm');
  },
  capLuc: (cap = 'Hai lực cùng độ lớn, ngược chiều, đặt lên hai vật khác nhau.') => {
    let b = defs('cl1');
    b += q(110, 56, '+', 24) + q(196, 56, '+', 13);
    b += arr(84, 56, 24, 56, 'cl1', RED) + T(30, 40, `F${sb('21')}`, { c: RED, w: 700 }) + arr(211, 56, 271, 56, 'cl1', RED) + T(226, 40, `F${sb('12')}`, { c: RED, w: 700 });
    b += T(110, 108, `4 ${gk('μ')}C`, { a: 'middle' }) + T(196, 108, `1 ${gk('μ')}C`, { a: 'middle' });
    return wrap('0 0 290 118', b, cap, 'Cặp lực giữa hai điện tích khác độ lớn');
  },
  // ===== Bài tập mẫu =====
  chamD1: (cap = 'Cộng có dấu rồi chia đều.') => chamTach(cap, ['−8,0 nC', '+2,0 nC'], 'cd1x'),
  mienD4: (cap = 'Xét chiều hai lực lên q<sub>0</sub> ở từng miền (1), (2), (3).') => thangHang(cap, { xa: 80, xb: 200, qb: '−', ab: '9,0 cm', id: 'md4' }),
  tamGiacD5: (cap = 'Vẽ F<sub>1</sub>, F<sub>2</sub> tại C (hút hay đẩy?) rồi cộng.') =>
    tamGiac(cap, { ca: 3, cb: 6, s: 30, qa: '+', qb: '−', la: '3,0 cm', lb: '6,0 cm', id: 'tg5' }),
  // ===== Bài tương tự =====
  baQuaTT: (cap = 'Ba quả giống hệt chạm cùng lúc rồi tách.') => chamTach(cap, ['+6 nC', '−3 nC', '+9 nC'], 'bq'),
  deuTT: (cap = 'CA = CB = AB = 6,0 cm.') => {
    const A = [40, 196], B = [240, 196], C = [140, 30];
    let b = ln(...A, ...B) + ln(...A, ...C) + ln(...B, ...C);
    b += q(...A, '+') + T(A[0], A[1] - 26, 'A', { w: 700, a: 'middle' }) + q(...B, '+') + T(B[0], B[1] - 26, 'B', { w: 700, a: 'middle' });
    b += q(...C, '+') + T(C[0] + 24, C[1] + 6, 'C', { w: 700 });
    b += `<path d="M126,54 A28,28 0 0 0 154,54" fill="none" stroke="${INK}" stroke-width="2"/>` + T(140, 90, '60°', { a: 'middle' });
    return wrap('0 0 280 216', b, cap, 'Ba điện tích ở ba đỉnh tam giác đều');
  },
};
