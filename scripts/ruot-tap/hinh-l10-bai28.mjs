// Hình minh hoạ cho ruột tập VL10 · Bài 28 Động lượng (lesson 73). Cùng quy tắc với hinh.mjs/hinh-l10-bai23.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chú thích/hình cạnh ô Dự đoán và ô điền không lộ đáp án (chỗ HS phải tính để "?").
// Xem thử: node scripts/ruot-tap/l10-bai28.mjs --hinh (chụp vào out/hinh-l10-bai28/).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
// chữ Hi Lạp: Source Sans 3 bản cắt không có Greek → lấy từ KaTeX_Math (đã nạp qua katex.min.css)
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const arr = (x1, y1, x2, y2, id, c = INK, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${SW}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const f1 = (v) => v.toFixed(1);
const R = (d) => (d * Math.PI) / 180;
// người que đứng, đầu tại (x,y), cao theo hệ số k
const nguoi = (x, y, k = 1) => `<circle cx="${x}" cy="${y}" r="${11 * k}" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
  + ln(x, y + 11 * k, x, y + 56 * k) + ln(x, y + 56 * k, x - 14 * k, y + 96 * k) + ln(x, y + 56 * k, x + 14 * k, y + 96 * k)
  + ln(x, y + 26 * k, x - 18 * k, y + 46 * k) + ln(x, y + 26 * k, x + 18 * k, y + 46 * k);
const dat = (x1, x2, y) => ln(x1, y, x2, y) + Array.from({ length: Math.floor((x2 - x1) / 18) }, (_, i) =>
  ln(x1 + 8 + i * 18, y, x1 + i * 18, y + 8, GREY, 1.8)).join('');
const tuong = (x, y1, y2) => ln(x, y1, x, y2) + Array.from({ length: Math.floor((y2 - y1) / 16) }, (_, i) =>
  ln(x, y1 + 10 + i * 16, x + 10, y1 + i * 16, GREY, 1.8)).join('');
const p = (i) => `p${sb(i)}`;

export const hinhL10b28 = {
  // Trang 1 · Dự đoán: hai người trên sân băng, mũi tên dài theo tỉ lệ TỐC ĐỘ (không vẽ động lượng: không lộ đáp án)
  sanBang: (cap = 'Mũi tên dài theo tỉ lệ tốc độ.') => {
    let b = defs('sb1') + defs('sb2');
    b += nguoi(26, 8, 0.6) + arr(56, 34, 216, 34, 'sb1', BLUE) + T(136, 24, '4 m/s', { c: BLUE, w: 700, a: 'middle' }) + T(56, 62, '30 kg', { w: 700 });
    b += nguoi(26, 96, 0.8) + arr(60, 126, 140, 126, 'sb2', BLUE) + T(100, 116, '2 m/s', { c: BLUE, w: 700, a: 'middle' }) + T(60, 156, '60 kg', { w: 700 });
    b += ln(4, 68, 296, 68, GREY, 2) + ln(4, 174, 296, 174, GREY, 2);
    b += T(296, 60, 'bạn nhỏ', { a: 'end' }) + T(296, 166, 'người lớn', { a: 'end' });
    return wrap('0 0 300 180', b, cap, 'Bạn nhỏ 30 kg lướt 4 m/s, người lớn 60 kg lướt 2 m/s');
  },
  // Trang 1 · Thí nghiệm bi lăn va khúc gỗ: đo quãng d khúc gỗ trượt (để "?")
  biGo: (cap = 'Thả bi ở độ cao h; đo quãng d khúc gỗ trượt.') => {
    let b = defs('bg1');
    b += `<path d="M8,30 L130,130 L292,130" fill="none" stroke="${INK}" stroke-width="${SW}"/>` + dat(130, 292, 130);
    b += `<circle cx="34" cy="38" r="12" fill="${GREY}" stroke="${INK}" stroke-width="2.4"/>`;
    b += `<rect x="140" y="104" width="44" height="26" rx="2" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(162, 124, 'gỗ', { a: 'middle', size: 18 });
    b += ln(8, 30, 8, 130, GREY, 2, '4 4') + T(14, 96, 'h');
    b += arr(184, 92, 276, 92, 'bg1', RED, '6 4') + T(230, 80, 'd = ?', { a: 'middle', c: RED, w: 700 });
    return wrap('0 0 300 146', b, cap, 'Bi lăn từ máng nghiêng va khúc gỗ');
  },
  // Trang 2 · II.2 + Dạng 3: hai vector chung gốc, góc α, đường chéo hình bình hành = ?
  binhHanh: (cap = 'Hai vector chung gốc, hợp góc α.', a = 60, l1 = 'p<tspan font-size="15" dy="5">1</tspan>', l2 = 'p<tspan font-size="15" dy="5">2</tspan>') => {
    const O = [26, 168], L1 = 170, L2 = 120;
    const A = [O[0] + L1, O[1]], B = [O[0] + L2 * Math.cos(R(a)), O[1] - L2 * Math.sin(R(a))], S = [A[0] + B[0] - O[0], B[1]];
    let b = defs('bh1') + defs('bh2') + defs('bh3');
    b += ln(f1(A[0]), A[1], f1(S[0]), f1(S[1]), GREY, 2, '5 4') + ln(f1(B[0]), f1(B[1]), f1(S[0]), f1(S[1]), GREY, 2, '5 4');
    b += arr(O[0], O[1], f1(A[0] - 4), A[1], 'bh1') + arr(O[0], O[1], f1(B[0]), f1(B[1]), 'bh2');
    b += arr(O[0], O[1], f1(S[0]), f1(S[1]), 'bh3', RED);
    const r = 34;
    b += `<path d="M${O[0] + r},${O[1]} A${r},${r} 0 0 0 ${f1(O[0] + r * Math.cos(R(a)))},${f1(O[1] - r * Math.sin(R(a)))}" fill="none" stroke="${INK}" stroke-width="2.2"/>`;
    b += `<text x="${O[0] + 40}" y="${O[1] - 10}" font-size="22" fill="${INK}">${gk('α')}</text>`;
    b += `<text x="${f1(A[0] - 30)}" y="${A[1] + 26}" font-size="22" fill="${INK}" font-weight="700">${l1}</text>`;
    b += `<text x="${f1(B[0] - 40)}" y="${f1(B[1] - 2)}" font-size="22" fill="${INK}" font-weight="700">${l2}</text>`;
    b += T(f1(S[0] - 4), f1(S[1] - 10), 'p = ?', { c: RED, w: 700, a: 'end' });
    return wrap('0 0 300 196', b, cap, 'Cộng hai vector động lượng theo quy tắc hình bình hành');
  },
  // Trang 2 · Thí nghiệm xe bật vào đệm lò xo gắn cảm biến lực
  demLoXo: (cap = 'Xe tới với v₁, bật lại với v₂; cổng quang đo tốc độ.') => {
    let b = defs('dl1') + defs('dl2');
    b += ln(6, 120, 294, 120) + `<rect x="270" y="56" width="22" height="64" fill="${GREY}" stroke="${INK}" stroke-width="2.4"/>`;
    b += `<polyline points="270,92 262,82 254,102 246,82 238,102 230,82 222,102 216,92" fill="none" stroke="${INK}" stroke-width="2.4"/>`;
    b += T(292, 46, 'cảm biến', { a: 'end', size: 18 });
    b += `<rect x="30" y="80" width="70" height="32" rx="4" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + ln(30, 116, 100, 116, INK, 2);
    b += `<path d="M138,120 L138,64 L170,64 L170,120" fill="none" stroke="${INK}" stroke-width="2.4"/>` + T(154, 52, 'cổng quang', { a: 'middle', size: 18 });
    b += arr(40, 30, 108, 30, 'dl1', BLUE) + T(24, 36, `v${sb('1')}`, { c: BLUE, w: 700 });
    b += arr(108, 146, 50, 146, 'dl2', RED, '6 4') + T(114, 152, `v${sb('2')}`, { c: RED, w: 700 });
    return wrap('0 0 300 160', b, cap.replace('v₁', 'v<sub>1</sub>').replace('v₂', 'v<sub>2</sub>'), 'Xe trên ray đệm khí bật vào đệm lò xo gắn cảm biến lực');
  },
  // Trang 3 · Bẫy 3: đồ thị F–t khi dừng trên mặt cứng và trên đệm (cùng diện tích 30×120 = 120×30)
  ftDoThi: (cap = 'Cùng một vật dừng hẳn. So diện tích dưới hai đường.') => {
    const O = [40, 170];
    let b = defs('ft1') + defs('ft2');
    b += arr(O[0], O[1], 292, O[1], 'ft1') + arr(O[0], O[1], O[0], 16, 'ft2') + T(26, 30, 'F', { w: 700 }) + T(286, 194, 't', { w: 700, a: 'end' });
    b += `<path d="M60,170 C64,60 86,44 90,52 C94,60 92,150 96,170" fill="${RED}" fill-opacity=".12" stroke="${RED}" stroke-width="${SW}"/>`;
    b += `<path d="M60,170 C70,136 100,134 140,134 C190,134 200,140 210,170" fill="none" stroke="${BLUE}" stroke-width="${SW}" stroke-dasharray="7 4"/>`;
    b += T(100, 48, 'mặt cứng', { c: RED, w: 700 }) + T(164, 124, 'đệm mềm', { c: BLUE, w: 700, a: 'middle' });
    return wrap('0 0 300 200', b, cap, 'Đồ thị lực theo thời gian khi dừng trên mặt cứng và trên đệm');
  },
  // Trang 4 + Dạng 4 · bóng đập vuông góc vào tường rồi bật ngược lại
  bongTuong: (v1 = '12 m/s', v2 = '8 m/s', cap = 'Trước (nét liền) và sau va chạm (nét đứt).', l2 = 150) => {
    let b = defs('bt1') + defs('bt2');
    b += tuong(250, 14, 160) + `<circle cx="150" cy="88" r="22" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<path d="M132,76 Q150,88 132,100 M168,76 Q150,88 168,100" fill="none" stroke="${GREY}" stroke-width="2"/>`;
    b += arr(40, 36, 220, 36, 'bt1', BLUE) + T(42, 26, `trước: ${v1}`, { c: BLUE, w: 700 });
    b += arr(220, 140, 220 - l2, 140, 'bt2', RED, '7 4') + T(42, 168, `sau: ${v2}`, { c: RED, w: 700 });
    return wrap('0 0 290 178', b, cap, 'Bóng đập vào tường rồi bật ngược lại');
  },
  // Dạng 1 · hai xe chạy ngược chiều trên đường thẳng, chiều dương theo xe tải
  xeDuong: (cap = 'Chiều dương: chiều xe tải.') => {
    const xe = (x, y, w, h) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="4" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
      + `<circle cx="${x + 14}" cy="${y + h + 8}" r="8" fill="#fff" stroke="${INK}" stroke-width="${SW}"/><circle cx="${x + w - 14}" cy="${y + h + 8}" r="8" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    let b = defs('xd1') + defs('xd2') + defs('xd3');
    b += xe(10, 50, 92, 46) + T(56, 80, 'tải', { a: 'middle' }) + xe(214, 66, 70, 30) + T(249, 88, 'con', { a: 'middle' });
    b += dat(4, 296, 112);
    b += arr(14, 30, 120, 30, 'xd1', BLUE) + T(16, 22, '54 km/h', { c: BLUE, w: 700, size: 19 });
    b += arr(284, 46, 190, 46, 'xd2', RED, '7 4') + T(284, 38, '72 km/h', { c: RED, w: 700, a: 'end', size: 19 });
    b += arr(100, 146, 200, 146, 'xd3') + T(208, 152, '(+)', { w: 700 });
    return wrap('0 0 300 158', b, cap, 'Xe tải và ô tô con chạy ngược chiều');
  },
  // Trang 5 · Thử thách ★★★: người rơi từ độ cao h xuống đệm hơi
  demHoi: (cap = 'Rơi từ 5 m xuống đệm hơi.') => {
    let b = defs('dh1');
    b += nguoi(70, 16, 0.75);
    b += arr(120, 30, 120, 150, 'dh1', INK, '6 4') + T(130, 96, 'h = 5 m');
    b += `<rect x="20" y="160" width="190" height="34" rx="14" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(115, 184, 'đệm hơi', { a: 'middle' });
    b += dat(6, 224, 196);
    return wrap('0 0 230 206', b, cap, 'Người rơi xuống đệm hơi');
  },
};
