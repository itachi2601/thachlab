// Hình minh hoạ cho ruột tập VL11 · Bài 15 Thực hành: đo tốc độ truyền âm (lesson 34).
// Cùng quy tắc với hinh.mjs: mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét đặc–đứt
// chứ không chỉ bằng màu, tự vẽ. Chú thích không lộ đáp án ô Dự đoán/ô điền đứng cạnh.
// Xem thử: node scripts/ruot-tap/l11-bai15.mjs --hinh (chụp vào out/hinh-l11-bai15/).
import { ve } from './hinh.mjs';
const { t, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const gm = (ch) => `<tspan font-family="KaTeX_Main">${ch}</tspan>`;
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const dot = (x, y, r = 4.5, c = INK) => `<circle cx="${x}" cy="${y}" r="${r}" fill="${c}"/>`;
const rect = (x, y, w, h, fill = '#fff') => `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${fill}" stroke="${INK}" stroke-width="${SW}"/>`;
const arrow = (x1, y1, x2, y2, c = INK) => `<path d="M${x1},${y1} L${x2},${y2}" stroke="${c}" stroke-width="${SW}" fill="none"/>`
  + (() => { const a = Math.atan2(y2 - y1, x2 - x1), s = 9; return `<path d="M${x2},${y2} l${(-s * Math.cos(a - 0.5)).toFixed(1)},${(-s * Math.sin(a - 0.5)).toFixed(1)} M${x2},${y2} l${(-s * Math.cos(a + 0.5)).toFixed(1)},${(-s * Math.sin(a + 0.5)).toFixed(1)}" stroke="${c}" stroke-width="${SW}" fill="none"/>`; })();

export const hinhL11b15 = {
  // Trang 1 · Dự đoán: ba chai cùng loại, lượng nước khác nhau (không nói chai nào cao tiếng hơn)
  chai: (cap = 'Ba chai giống nhau, lượng nước khác nhau. Mũi tên: thổi ngang miệng chai.') => {
    let b = '';
    const nuoc = [92, 48, 12]; // chiều cao cột nước (A nhiều nhất, C ít nhất)
    for (const [i, ten] of ['A', 'B', 'C'].entries()) {
      const x = 22 + i * 100, yd = 150, yc = 52; // đáy, vai chai
      b += `<rect x="${x}" y="${yd - nuoc[i]}" width="56" height="${nuoc[i]}" fill="#d9e6f7" stroke="none"/>`;
      b += `<path d="M${x},${yd} V${yc + 18} Q${x},${yc} ${x + 16},${yc} H${x + 16} V${yc - 22} H${x + 40} V${yc} Q${x + 56},${yc} ${x + 56},${yc + 18} V${yd} Z" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
      b += ln(x, yd - nuoc[i], x + 56, yd - nuoc[i], BLUE, 2.4, '5 4');
      b += arrow(x + 6, yc - 40, x + 30, yc - 28, RED);
      b += T(x + 28, yd + 26, ten, { a: 'middle', w: 700 });
    }
    return wrap('0 0 320 184', b, cap, 'Ba chai nhựa giống nhau chứa lượng nước khác nhau, thổi ngang miệng');
  },
  // Trang 2 · ống cộng hưởng: biên độ dao động của không khí ở hai lần cộng hưởng đầu; l đo từ miệng ống, e là đoạn bụng nhô lên
  ong: (cap = 'Biên độ dao động của không khí ở hai lần to nhất đầu tiên. Nét đứt trên miệng ống: bụng nằm cao hơn miệng một đoạn e (vẽ phóng to).') => {
    let b = '';
    const ym = 40, yb = 26, qw = 50, yd = 208; // miệng ống, bụng (cao hơn miệng e), một phần tư bước sóng, đáy
    for (const [x0, n, lab] of [[56, 1, '(1)'], [186, 3, '(2)']]) {
      const mn = yb + n * qw; // mặt nước = nút
      b += `<rect x="${x0}" y="${mn}" width="40" height="${yd - mn}" fill="#d9e6f7" stroke="none"/>`;
      b += ln(x0, ym, x0, yd) + ln(x0 + 40, ym, x0 + 40, yd) + ln(x0, yd, x0 + 40, yd);
      b += ln(x0, mn, x0 + 40, mn, BLUE, 2.4);
      const pts = [];
      for (let k = 0; k <= 120; k++) { const s = k / 120; const y = yb + s * (mn - yb); const a = Math.abs(Math.cos((s * n * Math.PI) / 2)); pts.push(`${(x0 + 20 + a * 16).toFixed(1)},${y.toFixed(1)}`); }
      b += `<polyline points="${pts.join(' ')}" fill="none" stroke="${RED}" stroke-width="${SW}"/>`;
      b += ln(x0 - 6, yb, x0 + 46, yb, GREY, 2, '5 4');
      b += ln(x0 - 14, ym, x0 - 14, mn, INK, 2.2) + ln(x0 - 20, ym, x0 - 8, ym, INK, 2.2) + ln(x0 - 20, mn, x0 - 8, mn, INK, 2.2);
      b += T(x0 - 26, (ym + mn) / 2 + 7, `${gk('l')}${sb(n === 1 ? '1' : '2')}`, { a: 'end' });
      b += T(x0 + 20, yd + 26, lab, { a: 'middle', w: 700 });
    }
    b += ln(110, yb, 110, ym, INK, 2.2) + ln(105, yb, 115, yb, INK, 2.2) + ln(105, ym, 115, ym, INK, 2.2) + T(120, ym - 2, `${gk('e')}`, { w: 700 });
    return wrap('0 0 260 240', b, cap, 'Sóng dừng trong cột khí ở hai lần cộng hưởng đầu tiên');
  },
  // Trang 2 · bộ ống cộng hưởng: loa ở miệng ống, ống có thước, bình thông nhau
  boOng: (cap = 'Bộ ống cộng hưởng. Mặt nước ở ống và ở bình luôn cùng độ cao.') => {
    let b = '';
    b += `<path d="M55,8 h24 v12 l14,20 h-52 l14,-20 z" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(100, 24, 'loa', { w: 400 });
    b += rect(54, 50, 26, 156, '#fff');
    b += `<rect x="55.5" y="120" width="23" height="85" fill="#d9e6f7" stroke="none"/>` + ln(55, 120, 79, 120, BLUE, 2.4);
    for (let i = 0; i <= 10; i++) b += ln(80, 56 + i * 15, i % 5 === 0 ? 96 : 89, 56 + i * 15, INK, 2);
    b += T(102, 84, 'thước', { size: 20 });
    b += ln(67, 206, 67, 232) + ln(67, 232, 130, 232) + ln(130, 232, 130, 218);
    b += `<path d="M110,100 V210 Q110,222 122,222 H138 Q150,222 150,210 V100" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<rect x="111.5" y="120" width="37" height="90" fill="#d9e6f7" stroke="none"/>` + ln(110, 120, 150, 120, BLUE, 2.4);
    b += T(158, 126, 'cùng', { size: 20 }) + T(158, 148, 'mức', { size: 20 }) + T(130, 262, 'bình nước', { a: 'middle' });
    return wrap('0 0 220 272', b, cap, 'Ống cộng hưởng nối bình thông nhau, loa phát âm đặt ở miệng ống');
  },
  // Trang 4 · đọc thước: mắt ngang mặt nước (đúng) hay nhìn lệch (sai)
  docThuoc: (cap = 'Hai cách đặt mắt khi đọc l (đường nét đứt là tia nhìn).') => {
    let b = '';
    for (const [x0, lab, dy] of [[0, '(1)', 0], [168, '(2)', 44]]) {
      b += `<rect x="${x0 + 60}" y="40" width="34" height="108" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
      b += `<rect x="${x0 + 61.5}" y="96" width="31" height="50" fill="#d9e6f7" stroke="none"/>` + ln(x0 + 60, 96, x0 + 94, 96, BLUE, 2.4);
      for (let i = 0; i <= 7; i++) b += ln(x0 + 60, 44 + i * 14, x0 + (i % 2 ? 70 : 76), 44 + i * 14, INK, 2);
      b += `<ellipse cx="${x0 + 18}" cy="${96 - dy}" rx="14" ry="9" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + dot(x0 + 18, 96 - dy, 3.5);
      b += ln(x0 + 32, 96 - dy, x0 + 60, 96, INK, 2.4, '6 4');
      b += T(x0 + 76, 176, lab, { a: 'middle', w: 700 });
    }
    return wrap('0 0 320 188', b, cap, 'Mắt đặt ngang mặt nước và mắt đặt cao hơn mặt nước khi đọc thước');
  },
  // Trang 5 · khoảng đo v̄ ± Δv và giá trị tham khảo nằm trong/ngoài
  khoangDo: (cap = 'Khoảng đo (đoạn đậm) và giá trị tham khảo (chấm tròn) trong hai trường hợp.') => {
    let b = '';
    for (const [y, vtk, lab] of [[44, 156, '(1)'], [118, 262, '(2)']]) {
      b += T(8, y + 6, lab, { w: 700 });
      b += ln(46, y, 300, y, GREY, 2.2);
      b += ln(120, y, 220, y, INK, 7);
      b += ln(120, y - 11, 120, y + 11, INK, 3) + ln(220, y - 11, 220, y + 11, INK, 3) + ln(170, y - 8, 170, y + 8, INK, 3);
      b += `<circle cx="${vtk}" cy="${y}" r="7" fill="${RED}"/>`;
      b += T(120, y + 34, `${gk('v')}${gm('−Δ')}${gk('v')}`, { a: 'middle', size: 18 }) + T(170, y - 18, `${gk('v')}`, { a: 'middle', size: 20 }) + T(220, y + 34, `${gk('v')}${gm('+Δ')}${gk('v')}`, { a: 'middle', size: 18 });
    }
    return wrap('0 0 320 176', b, cap, 'Hai trường hợp giá trị tham khảo so với khoảng đo');
  },
};
