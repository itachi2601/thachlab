// Hình minh hoạ cho ruột tập VL11 · Bài 14 Bài tập về sóng (lesson 33). Cùng quy tắc với hinh.mjs/hinh-l11-bai4.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh. Xem thử: node scripts/ruot-tap/l11-bai14.mjs --hinh (chụp vào out/hinh-l11-bai14/).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
// chữ Hi Lạp: Source Sans 3 chỉ nạp latin/vietnamese → lấy từ KaTeX_Math
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const LAM = gk('λ');
const LAMh = '<span style="font-family:KaTeX_Math;font-style:italic">λ</span>'; // λ trong chú thích HTML
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const arr = (x1, y1, x2, y2, id, c = INK, w = 2.4) =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}" marker-end="url(#${id})"/>`;
const f1 = (v) => (+v).toFixed(1);
// mũi tên hai đầu
const def2 = (id) => `<defs><marker id="${id}" markerWidth="7" markerHeight="7" refX="5.5" refY="3.5" orient="auto-start-reverse" markerUnits="strokeWidth"><path d="M0,0 L7,3.5 L0,7 z" fill="context-stroke"/></marker></defs>`;
const hai = (x1, y1, x2, y2, id, c = RED) =>
  `<line x1="${f1(x1)}" y1="${f1(y1)}" x2="${f1(x2)}" y2="${f1(y2)}" stroke="${c}" stroke-width="2.4" marker-start="url(#${id})" marker-end="url(#${id})"/>`;
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;

// Hình dạng sóng u–x vẽ từ hàm cos thật: đỉnh đầu ở x = d0 (cm), bước sóng lam (cm), xmax; nhãn trục chỉ ở các mốc `moc`.
const songUX = ({ d0, lam, xmax, moc, cap, id, dinh = 0 }) => {
  const x0 = 40, x1 = 300, yc = 80, A = 38, kx = (x1 - x0) / xmax;
  const X = (v) => x0 + v * kx, Y = (u) => yc - u * A;
  let b = defs(id + 'a');
  b += arr(x0, 122, x0, 12, id + 'a') + arr(x0 - 6, yc, 316, yc, id + 'a');
  b += T(x0 + 8, 24, 'u') + T(316, yc + 28, 'x (cm)', { a: 'end' });
  let d = '';
  for (let i = 0; i <= 300; i++) { const v = ((xmax - 4) * i) / 300; d += `${i ? 'L' : 'M'}${f1(X(v))},${f1(Y(Math.cos((2 * Math.PI * (v - d0)) / lam)))}`; }
  b += `<path d="${d}" fill="none" stroke="${BLUE}" stroke-width="${SW}"/>`;
  moc.forEach((v) => { b += ln(f1(X(v)), Y(1), f1(X(v)), yc + 6, GREY, 1.6, '4 4') + T(X(v), yc + 28, String(v).replace('.', ','), { a: 'middle' }); });
  b += T(x0 - 8, yc + 24, '0', { a: 'end' });
  for (let k = 0; k < dinh; k++) b += `<circle cx="${f1(X(d0 + k * lam))}" cy="${f1(Y(1))}" r="5" fill="${RED}"/>`;
  b += arr(118, 22, 168, 22, id + 'a', INK, 2.2) + T(176, 29, 'truyền sóng');
  return wrap('0 0 320 120', b, cap, 'Hình dạng sợi dây tại một thời điểm');
};

// Sóng dừng trên dây hai đầu cố định: n bó, chiều dài ghi trên hình
const dayDung = ({ n, L, cap, id }) => {
  const x0 = 26, x1 = 294, yc = 46, A = 24, w = (x1 - x0) / n;
  let b = def2(id);
  b += `<rect x="${x0 - 14}" y="${yc - 26}" width="10" height="52" fill="${GREY}"/>` + `<rect x="${x1 + 4}" y="${yc - 26}" width="10" height="52" fill="${GREY}"/>`;
  let d1 = '', d2 = '';
  for (let i = 0; i <= 240; i++) { const x = x0 + ((x1 - x0) * i) / 240, s = Math.sin((Math.PI * (x - x0)) / w); d1 += `${i ? 'L' : 'M'}${f1(x)},${f1(yc - A * s)}`; d2 += `${i ? 'L' : 'M'}${f1(x)},${f1(yc + A * s)}`; }
  b += `<path d="${d1}" fill="none" stroke="${BLUE}" stroke-width="${SW}"/><path d="${d2}" fill="none" stroke="${BLUE}" stroke-width="2.2" stroke-dasharray="6 4"/>`;
  b += ln(x0, yc, x1, yc, GREY, 1.4, '3 4');
  b += T(x0 - 9, 16, 'A', { a: 'middle', w: 700 }) + T(x1 + 9, 16, 'B', { a: 'middle', w: 700 });
  b += hai(x0, 84, x1, 84, id, INK) + `<rect x="122" y="72" width="76" height="24" fill="#fff"/>` + T(160, 91, L, { a: 'middle', w: 700 });
  return wrap('0 0 320 94', b, cap, 'Sóng dừng trên dây hai đầu cố định');
};

export const hinhL11b14 = {
  // Trang 1 · Dự đoán: 5 ngọn sóng liên tiếp, cả đoạn 2 m (không vẽ khoảng con để HS tự đếm)
  namNgon: (cap = 'Từ ngọn thứ nhất tới ngọn thứ năm đo được 2 m.') => {
    const x0 = 34, x1 = 286, n = 5, lam = (x1 - x0) / (n - 1), yc = 96, A = 30;
    let b = def2('nn');
    let d = '';
    for (let i = 0; i <= 300; i++) { const x = 8 + (304 * i) / 300; d += `${i ? 'L' : 'M'}${f1(x)},${f1(yc - A * Math.cos((2 * Math.PI * (x - x0)) / lam))}`; }
    b += `<path d="${d}" fill="none" stroke="${BLUE}" stroke-width="${SW}"/>`;
    for (let k = 0; k < n; k++) { const x = x0 + k * lam; b += `<circle cx="${f1(x)}" cy="${yc - A}" r="5" fill="${RED}"/>`; }
    b += ln(x0, yc - A, x0, 156, GREY, 1.6, '4 4') + ln(x1, yc - A, x1, 156, GREY, 1.6, '4 4');
    b += hai(x0, 150, x1, 150, 'nn', INK) + `<rect x="138" y="138" width="44" height="24" fill="#fff"/>` + T(160, 157, '2 m', { a: 'middle', w: 700 });
    return wrap('0 0 320 168', b, cap, 'Năm ngọn sóng liên tiếp');
  },
  // Trang 2 · Họ A Dạng 2: cùng công suất trải trên hai mặt cầu R và 2R
  songCau: (cap = 'Cùng công suất P trải trên mặt cầu bán kính R và 2R. Diện tích mặt cầu lớn gấp mấy lần?') => {
    const cx = 80, cy = 100;
    let b = defs('sc');
    b += `<circle cx="${cx}" cy="${cy}" r="42" fill="none" stroke="${BLUE}" stroke-width="${SW}"/>`;
    b += `<path d="M${cx},${cy - 84} A84,84 0 0 1 ${cx},${cy + 84}" fill="none" stroke="${BLUE}" stroke-width="${SW}" stroke-dasharray="7 5"/>`;
    b += `<circle cx="${cx}" cy="${cy}" r="7" fill="${RED}"/>` + T(cx - 12, cy + 6, 'S', { a: 'end', w: 700 });
    b += arr(cx, cy, cx + 40, cy - 12, 'sc') + T(cx + 8, cy - 16, 'R', { w: 700 });
    b += arr(cx, cy, cx + 74, cy + 40, 'sc') + T(cx + 30, cy + 54, '2R', { w: 700 });
    b += `<circle cx="109.7" cy="70.3" r="5" fill="${BLUE}"/>` + T(100, 56, `I${sb('1')}`, { c: BLUE, w: 700, a: 'end' });
    b += `<circle cx="152.7" cy="58" r="5" fill="${BLUE}"/>` + T(162, 52, `I${sb('2')}`, { c: BLUE, w: 700 });
    return wrap('0 0 280 196', b, cap, 'Sóng cầu toả từ nguồn điểm');
  },
  // Trang 3 · Họ B: đoạn AB = 4λ, chấm đặc cực đại, vòng rỗng cực tiểu (để HS đếm, đối chiếu công thức)
  giaoThoaAB: (cap = `AB = 4${LAMh}. Chấm đặc: cực đại · vòng rỗng: cực tiểu. Không tính A, B.`) => {
    const xa = 24, xb = 296, y = 60, q = (xb - xa) / 16; // λ/4 = q
    let b = '';
    b += ln(xa, y, xb, y, INK, 2.4);
    for (let k = 1; k < 16; k++) {
      const x = xa + k * q;
      if (k % 2 === 0) b += `<circle cx="${f1(x)}" cy="${y}" r="6.5" fill="${RED}"/>`;
      else b += `<circle cx="${f1(x)}" cy="${y}" r="6" fill="#fff" stroke="${BLUE}" stroke-width="2.4"/>`;
    }
    b += `<rect x="${xa - 7}" y="${y - 7}" width="14" height="14" fill="${INK}"/>` + `<rect x="${xb - 7}" y="${y - 7}" width="14" height="14" fill="${INK}"/>`;
    b += T(xa, y + 34, 'A', { a: 'middle', w: 700 }) + T(xb, y + 34, 'B', { a: 'middle', w: 700 }) + T(160, y + 34, 'trung điểm', { a: 'middle', c: GREY });
    b += ln(160, y + 10, 160, y + 16, GREY, 2);
    return wrap('0 0 320 104', b, cap, 'Cực đại, cực tiểu trên đoạn nối hai nguồn');
  },
  // Trang 3 · Họ C: hệ vân trên màn, vân trung tâm O, một khoảng vân i
  vanYoung: (cap = 'Vân sáng (trắng) xen vân tối, vân trung tâm ở O. Đo cả đoạn nhiều vân rồi chia.') => {
    const y0 = 34, h = 56, x0 = 16, x1 = 304, c = 160, i = 36;
    let b = def2('vy');
    for (let x = x0; x <= x1; x += 1.5) {
      const g = Math.round(28 + 200 * Math.cos((Math.PI * (x - c)) / i) ** 2);
      b += `<rect x="${f1(x)}" y="${y0}" width="1.6" height="${h}" fill="rgb(${g},${g},${g})"/>`;
    }
    b += `<rect x="${x0}" y="${y0}" width="${x1 - x0}" height="${h}" fill="none" stroke="${INK}" stroke-width="2"/>`;
    b += ln(c, y0 + h, c, y0 + h + 10, INK, 2.4) + T(c, y0 + h + 30, 'O', { a: 'middle', w: 700 });
    b += ln(c, y0 - 14, c, y0, INK, 2) + ln(c + i, y0 - 14, c + i, y0, INK, 2) + hai(c, y0 - 8, c + i, y0 - 8, 'vy') + T(c + i + 8, y0 - 6, 'i', { c: RED, w: 700 });
    return wrap('0 0 320 128', b, cap, 'Hệ vân giao thoa trên màn');
  },
  // Trang 4 · Họ D: dây một đầu cố định (nút), một đầu tự do — L = 5λ/4 như hình 3 của bài web (n = 2)
  motDauTuDo: (cap = 'Đầu trái cố định, đầu phải tự do. Đếm số đoạn λ/4 trên dây, rồi đếm bụng, nút.') => {
    const x0 = 30, x1 = 294, yc = 66, A = 34, q = (x1 - x0) / 5; // q = λ/4
    let b = '';
    b += `<rect x="${x0 - 14}" y="${yc - 40}" width="10" height="80" fill="${GREY}"/>`;
    let d1 = '', d2 = '';
    for (let i = 0; i <= 240; i++) { const x = x0 + ((x1 - x0) * i) / 240, s = Math.sin((Math.PI / 2) * (x - x0) / q); d1 += `${i ? 'L' : 'M'}${f1(x)},${f1(yc - A * s)}`; d2 += `${i ? 'L' : 'M'}${f1(x)},${f1(yc + A * s)}`; }
    b += `<path d="${d1}" fill="none" stroke="${BLUE}" stroke-width="${SW}"/><path d="${d2}" fill="none" stroke="${BLUE}" stroke-width="2.2" stroke-dasharray="6 4"/>`;
    b += ln(x0, yc, x1 + 12, yc, GREY, 1.4, '3 4');
    for (let k = 0; k <= 5; k++) b += ln(f1(x0 + k * q), yc + 40, f1(x0 + k * q), yc + 48, INK, 2);
    b += ln(x0, yc + 44, x1, yc + 44, INK, 2) + T(x0, yc + 70, 'cố định', { a: 'start' }) + T(x1 + 4, yc + 70, 'tự do', { a: 'end' });
    return wrap('0 0 320 146', b, cap.replace('λ', LAMh), 'Sóng dừng một đầu cố định, một đầu tự do');
  },
  // Trang 5 · Bài toán mẫu: hai nguồn A, B phát sóng tròn
  haiNguon: (cap = 'Hai nguồn cùng pha A, B. Chỉ đếm điểm nằm giữa A và B.') => {
    const ya = 80, xa = 100, xb = 220;
    let b = def2('hn');
    [24, 48, 72, 96].forEach((r) => {
      b += `<circle cx="${xa}" cy="${ya}" r="${r}" fill="none" stroke="${BLUE}" stroke-width="1.8"/>`;
      b += `<circle cx="${xb}" cy="${ya}" r="${r}" fill="none" stroke="${GREY}" stroke-width="1.8" stroke-dasharray="5 4"/>`;
    });
    b += ln(xa, ya, xb, ya, INK, 2.8);
    b += `<circle cx="${xa}" cy="${ya}" r="7" fill="${RED}"/><circle cx="${xb}" cy="${ya}" r="7" fill="${RED}"/>`;
    b += `<rect x="${xa - 30}" y="${ya + 6}" width="26" height="24" fill="#fff"/>` + T(xa - 17, ya + 25, 'A', { a: 'middle', w: 700 });
    b += `<rect x="${xb + 4}" y="${ya + 6}" width="26" height="24" fill="#fff"/>` + T(xb + 17, ya + 25, 'B', { a: 'middle', w: 700 });
    return wrap('0 0 320 166', b, cap, 'Hai nguồn sóng nước');
  },
  // Trang 6 · Dạng 1: bốn đỉnh liên tiếp, đỉnh đầu ở 3 cm, đỉnh cuối ở 39 cm
  d1: (cap = '') => songUX({ d0: 3, lam: 12, xmax: 50, moc: [3, 39], cap, id: 'd1', dinh: 4 }),
  // Trang 7 · Dạng 5: dây 0,60 m, ba bó
  d5: (cap = '') => dayDung({ n: 3, L: '0,60 m', cap, id: 'd5' }),
  // Trang 8 · Bài tương tự Dạng 1 bài 1: năm đỉnh liên tiếp, 2 cm → 34 cm
  tt1: (cap = '') => songUX({ d0: 2, lam: 8, xmax: 44, moc: [2, 34], cap, id: 't1', dinh: 5 }),
  // Trang 9 · Bài tương tự Dạng 5 bài 1: dây 1,2 m, bốn bó
  tt5: (cap = '') => dayDung({ n: 4, L: '1,2 m', cap, id: 't5' }),
};
