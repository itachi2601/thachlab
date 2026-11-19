// Hình minh hoạ cho ruột tập VL10 · Bài 30 Thực hành: động lượng trước và sau va chạm (lesson 75). Cùng quy tắc với hinh-l10-bai23.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét chứ không chỉ bằng màu, tự vẽ.
// Hình cạnh ô Dự đoán (dudoan) không vẽ mũi tên/độ dài nào cho biết xe nào chạy nhanh hơn. Xem thử: node scripts/ruot-tap/l10-bai30.mjs --hinh
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const f1 = (v) => v.toFixed(1);
const R = (d) => (d * Math.PI) / 180;
const arr = (x1, y1, x2, y2, id, c = INK, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${SW}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const box = (x, y, w, h, fill = '#fff', r = 4) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r}" fill="${fill}" stroke="${INK}" stroke-width="${SW}"/>`;

// Băng đệm khí: mặt trên y. Xe: thân (x,y-h → y), tấm cản quang nhô lên. Cổng quang: chữ U úp.
const rail = (y, x1 = 8, x2 = 312) => box(x1, y, x2 - x1, 10, '#fff', 2)
  + Array.from({ length: Math.floor((x2 - x1) / 24) }, (_, i) => `<circle cx="${x1 + 12 + i * 24}" cy="${y + 5}" r="1.6" fill="${GREY}"/>`).join('');
const xe = (x, y, w = 56, h = 24, tam = true, th = 'rgba(28,37,64,.18)') =>
  box(x, y - h, w, h - 2, '#fff', 3) + ln(x + 4, y - 1, x + w - 4, y - 1, GREY, 2)
  + (tam ? `<rect x="${x + w / 2 - 9}" y="${y - h - 16}" width="18" height="16" fill="${th}" stroke="${INK}" stroke-width="2.4"/>` : '');
const cong = (x, y) => `<path d="M${x - 12},${y} V${y - 62} H${x + 12} V${y}" fill="none" stroke="${INK}" stroke-width="${SW}"/>`
  + ln(x, y - 56, x, y - 6, GREY, 2, '4 4');
const lo = (x1, y1, x2, y2, n = 6) => { // lò xo răng cưa
  let d = `M${x1},${y1}`; const dx = (x2 - x1) / n;
  for (let i = 0; i < n; i++) d += ` L${f1(x1 + dx * (i + 0.25))},${y1 - 9} L${f1(x1 + dx * (i + 0.75))},${y1 + 9} L${f1(x1 + dx * (i + 1))},${y1}`;
  return `<path d="${d}" fill="none" stroke="${INK}" stroke-width="2.6"/>`;
};

export const hinhL10b30 = {
  // Trang 1 · Dự đoán: hai xe đứng yên, lò xo nén giữa hai xe, xe 2 nặng gấp đôi. Không mũi tên, không độ dài gợi ý.
  dudoan: (cap = 'Hai xe đứng yên trên băng đệm khí; lò xo nén ở giữa, buộc bằng dây. Cắt dây.') => {
    let b = rail(110) + xe(64, 110, 56, 26, false) + xe(180, 110, 84, 38, false);
    b += lo(120, 92, 180, 92, 6) + ln(124, 80, 176, 80, GREY, 2.4, '3 3');
    b += T(92, 56, 'm', { a: 'middle', w: 700 }) + T(222, 56, '2m', { a: 'middle', w: 700 });
    b += T(160, 150, 'băng đệm khí', { a: 'middle', c: GREY });
    return wrap('0 0 320 160', b, cap, 'Hai xe và lò xo nén trên băng đệm khí');
  },
  // Trang 2 · bố trí thí nghiệm 1: hai cổng quang, xe 1 tới, xe 2 đứng yên. Chỉ nêu cái cần đo, chưa có kết quả.
  boTri1: (cap = 'Thí nghiệm 1: đo t<sub>1</sub> ở cổng 1 và t<sub>1</sub>′ ở cổng 2.') => {
    let b = defs('b1a') + defs('b1b');
    b += rail(110) + cong(64, 110) + cong(280, 110) + xe(90, 110) + xe(178, 110, 56, 24, false);
    b += T(64, 22, 'cổng 1', { a: 'middle' }) + T(280, 22, 'cổng 2', { a: 'middle' });
    b += ln(109, 60, 127, 60, BLUE, 2.4) + ln(109, 54, 109, 66, BLUE, 2.4) + ln(127, 54, 127, 66, BLUE, 2.4) + T(118, 46, 's', { a: 'middle', w: 700, c: BLUE }) + T(206, 70, 'xe 2', { a: 'middle' });
    b += arr(94, 140, 148, 140, 'b1a', RED) + T(121, 164, `v${sb('1')}`, { a: 'middle', c: RED, w: 700 });
    b += T(64, 164, `t${sb('1')}`, { a: 'middle' }) + T(280, 164, `t${sb('1')}′`, { a: 'middle' });
    return wrap('0 0 320 176', b, cap, 'Bố trí thí nghiệm va chạm mềm');
  },
  // Trang 4 · bố trí thí nghiệm 2: hai xe đẩy nhau, mỗi xe qua cổng của mình. Chiều dương ghi rõ.
  boTri2: (cap = 'Thí nghiệm 2: xe 1 qua cổng 1, xe 2 qua cổng 2. Chiều dương sang phải.') => {
    let b = defs('b2a') + defs('b2b');
    b += rail(110) + cong(36, 110) + cong(284, 110) + xe(106, 110, 50, 24) + xe(166, 110, 50, 24);
    b += lo(156, 98, 166, 98, 1);
    b += T(36, 22, 'cổng 1', { a: 'middle' }) + T(284, 22, 'cổng 2', { a: 'middle' });
    b += T(131, 56, 'xe 1', { a: 'middle' }) + T(191, 56, 'xe 2', { a: 'middle' });
    b += T(36, 164, `t${sb('1')}′`, { a: 'middle' }) + T(284, 164, `t${sb('2')}′`, { a: 'middle' });
    b += arr(120, 152, 200, 152, 'b2a', BLUE) + T(210, 160, '+', { c: BLUE, w: 700, size: 26 });
    return wrap('0 0 320 176', b, cap, 'Bố trí thí nghiệm hai xe đẩy nhau');
  },
  // Trang 6 · Dạng 1: một xe chắn cổng
  congQuang: (cap = 'Tấm cản quang chắn tia sáng trong t; bề rộng s.') => {
    let b = defs('cqa');
    b += rail(100) + cong(160, 100) + xe(130, 100, 56, 24);
    b += T(160, 20, 'cổng quang', { a: 'middle' });
    b += T(158, 52, 's', { a: 'middle', c: BLUE, w: 700 });
    b += arr(40, 138, 100, 138, 'cqa', RED) + T(104, 144, 'xe', { c: RED, w: 700 });
    return wrap('0 0 320 160', b, cap, 'Xe chắn cổng quang');
  },
  // Trang 7 · Dạng 3 dùng lại boTri2 · Dạng 4: băng nghiêng (góc phóng đại)
  bangNghieng: (cap = 'Góc nghiêng vẽ phóng đại.') => {
    const g = 8, x0 = 28, y0 = 76, L = 268;
    const P = (u, v) => [x0 + u * Math.cos(R(g)) - v * Math.sin(R(g)), y0 + u * Math.sin(R(g)) + v * Math.cos(R(g))];
    const pt = (u, v) => P(u, v).map(f1).join(',');
    let b = '';
    b += `<g transform="rotate(${g} ${x0} ${y0})">${rail(y0, x0, x0 + L)}${cong(x0 + 56, y0)}${xe(x0 + 130, y0, 40, 24, false)}${xe(x0 + 200, y0, 40, 24, false)}</g>`;
    const hy = y0 + L * Math.sin(R(g));
    b += ln(x0, y0 + 12, x0, hy + 14, BLUE, 2.4, '5 4') + ln(x0, hy + 14, x0 + L * Math.cos(R(g)) + 8, hy + 14, BLUE, 2.4, '5 4');
    b += T(x0 - 6, (y0 + hy) / 2 + 16, 'h', { a: 'end', c: BLUE, w: 700 });
    const tx = (u, v, s, o = {}) => { const [a, c] = P(u, v); return T(a, c, s, { a: 'middle', ...o }); };
    b += tx(150, -62, 'xe 1') + tx(220, -62, 'xe 2') + tx(56, 34, 'cổng 1');
    const [x1, y1] = P(56, -36), [x2, y2] = P(220, -36);
    b += `<line x1="${f1(x1)}" y1="${f1(y1)}" x2="${f1(x2)}" y2="${f1(y2)}" stroke="${INK}" stroke-width="2.2" stroke-dasharray="6 4"/>` + tx(138, -42, 'x', { w: 700 });
    b += T(300, 152, 'L = cả băng', { a: 'end', c: GREY });
    return wrap('0 0 320 164', b, cap, 'Băng đệm khí kê nghiêng một đầu');
  },
  // Trang 5 · lưới trống p′/p cho ba lần đo (HS tự chấm, vẽ ± ε)
  luoiSS: (cap = 'Chấm p′/p mỗi lần, vẽ thanh dọc ± sai số gộp quanh điểm.') => {
    let b = ln(54, 14, 54, 150, INK, 2.6) + ln(54, 150, 300, 150, INK, 2.6);
    const ys = [[1.04, 18], [1.02, 52], [1.00, 86], [0.98, 118], [0.96, 150]];
    ys.forEach(([v, y]) => { b += ln(50, y, 300, y, y === 86 ? INK : GREY, y === 86 ? 2.2 : 1.4, y === 86 ? '' : '4 4') + T(46, y + 6, v.toFixed(2).replace('.', ','), { a: 'end', size: 20 }); });
    [110, 180, 250].forEach((x, i) => { b += ln(x, 146, x, 154, INK, 2.2) + T(x, 176, `lần ${i + 1}`, { a: 'middle' }); });
    b += T(60, 12, 'p′/p', { w: 700, c: BLUE });
    return wrap('0 0 320 184', b, cap, 'Lưới trống để chấm tỉ số p′/p của ba lần đo');
  },
};
