// Hình minh hoạ cho ruột tập VL10 · Bài 8 Chuyển động biến đổi. Gia tốc (lesson 53). Cùng quy tắc với hinh.mjs/hinh-l10-bai23.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh. Xem thử: node scripts/ruot-tap/l10-bai8.mjs --hinh (chụp vào out/hinh-l10-bai8/).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const arr = (x1, y1, x2, y2, id, c = INK, dash = '', w = SW) =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
// số trong vòng tròn tự vẽ (①②③ không có trong Source Sans 3 → rơi về Hiragino)
const vong = (x, y, n) => `<circle cx="${x}" cy="${y}" r="12" fill="#fff" stroke="${INK}" stroke-width="2"/>` + T(x, y + 7, n, { a: 'middle', w: 700 });
export const vongH = (n) => `<span style="display:inline-block;width:4.2mm;height:4.2mm;border:.25mm solid currentColor;border-radius:50%;text-align:center;line-height:3.8mm;font-weight:700">${n}</span>`;
const f1 = (v) => Math.round(v * 10) / 10;
const so = (v) => String(v).replace('.', ',');
const dat = (x1, x2, y) => ln(x1, y, x2, y) + Array.from({ length: Math.floor((x2 - x1) / 18) }, (_, i) =>
  ln(x1 + 8 + i * 18, y, x1 + i * 18, y + 8, GREY, 1.8)).join('');
const xe = (x, y, w = 64, h = 28) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="5" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
  + `<circle cx="${x + 14}" cy="${y + h + 7}" r="7" fill="#fff" stroke="${INK}" stroke-width="${SW}"/><circle cx="${x + w - 14}" cy="${y + h + 7}" r="7" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;

// Đồ thị v–t: pts = [[t, v], …] (đơn vị thật), tm/vm = giá trị lớn nhất trục, tk/vk = vạch có số; o.so = nhãn đoạn ①②③;
// o.to = tô diện tích dưới đồ thị; o.an = true thì chỉ vẽ trục + lưới (HS tự vẽ); o.vmin < 0 cho trục v có phần âm.
const vt = (pts, o = {}) => {
  const { tm, vm, vmin = 0, tk = [], vk = [], so: nhan = [], to = false, an = false, cap = '', id = 'vt', dau = '', luoi = true, cao = 170 } = o;
  const X0 = 46, X1 = 300, Y0 = 18, Y1 = cao; // khung vẽ
  const X = (tt) => X0 + (tt / tm) * (X1 - X0), Y = (v) => Y1 - ((v - vmin) / (vm - vmin)) * (Y1 - Y0);
  let b = defs(id);
  if (luoi) b += tk.map((tt) => ln(f1(X(tt)), Y0, f1(X(tt)), Y1, '#d3dbec', 1.4)).join('') + vk.map((v) => ln(X0, f1(Y(v)), X1, f1(Y(v)), '#d3dbec', 1.4)).join('');
  if (to && !an) b += `<path d="M${f1(X(pts[0][0]))},${f1(Y(0))} ${pts.map(([tt, v]) => `L${f1(X(tt))},${f1(Y(v))}`).join(' ')} L${f1(X(pts.at(-1)[0]))},${f1(Y(0))} z" fill="#dfe6f5" stroke="none"/>`;
  b += arr(X0, f1(Y(0)), X1 + 14, f1(Y(0)), id) + arr(X0, Y1 + 4, X0, Y0 - 12, id);
  b += T(X1 + 14, f1(Y(0)) + 24, 't (s)', { a: 'end' }) + T(X0 + 8, Y0 - 2, 'v (m/s)');
  b += tk.map((tt) => ln(f1(X(tt)), f1(Y(0)) - 4, f1(X(tt)), f1(Y(0)) + 4, INK, 2) + T(f1(X(tt)), f1(Y(0)) + 22, so(tt), { a: 'middle' })).join('');
  b += vk.map((v) => ln(X0 - 4, f1(Y(v)), X0 + 4, f1(Y(v)), INK, 2) + T(X0 - 8, f1(Y(v)) + 7, so(v), { a: 'end' })).join('');
  b += T(X0 - 8, f1(Y(0)) + 22, '0', { a: 'end' });
  if (!an) {
    b += `<polyline points="${pts.map(([tt, v]) => `${f1(X(tt))},${f1(Y(v))}`).join(' ')}" fill="none" stroke="${RED}" stroke-width="3.4"/>`;
    // đường gióng chấm tới hai trục ở các điểm gãy
    b += pts.filter(([, v]) => v !== 0).map(([tt, v]) => ln(X0, f1(Y(v)), f1(X(tt)), f1(Y(v)), GREY, 1.6, '4 4') + ln(f1(X(tt)), f1(Y(v)), f1(X(tt)), f1(Y(0)), GREY, 1.6, '4 4')).join('');
    nhan.forEach((s, i) => {
      if (!s) return;
      const [a, c] = [pts[i], pts[i + 1]], mx = (X(a[0]) + X(c[0])) / 2, my = (Y(a[1]) + Y(c[1])) / 2;
      b += vong(f1(mx), f1(my - 20), s);
    });
  }
  b += dau;
  return wrap(`0 0 330 ${cao + 36}`, b, cap, 'Đồ thị vận tốc theo thời gian');
};

export const hinhL10b8 = {
  // Trang 1 · Dự đoán: xe máy ở vạch dừng, ô tô trên cầu vượt — chỉ ghi số liệu, không so sánh
  denXanh: (cap = 'Cả hai cùng tăng thêm 10 m/s.') => {
    let b = defs('dx1');
    b += `<rect x="8" y="10" width="20" height="54" rx="5" fill="#fff" stroke="${INK}" stroke-width="2.4"/>`
      + `<circle cx="18" cy="24" r="6" fill="#fff" stroke="${INK}" stroke-width="2"/><circle cx="18" cy="50" r="7" fill="${INK}"/>`;
    b += ln(40, 20, 40, 86, INK, 4) + T(46, 30, 'vạch dừng', { c: GREY });
    // xe máy
    b += `<circle cx="72" cy="78" r="9" fill="#fff" stroke="${INK}" stroke-width="${SW}"/><circle cx="116" cy="78" r="9" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
      + `<path d="M72,78 L90,60 L110,60 L116,78" fill="none" stroke="${INK}" stroke-width="${SW}"/>` + ln(46, 92, 320, 92);
    b += T(136, 64, 'Xe máy', { w: 700 }) + T(136, 86, 'từ 0 lên 10 m/s trong 5 s');
    // ô tô trên cầu
    b += ln(10, 132, 320, 132, INK, 4) + ln(30, 132, 30, 186, GREY, 3) + ln(300, 132, 300, 186, GREY, 3);
    b += xe(56, 96, 66, 26);
    b += T(136, 160, 'Ô tô', { w: 700 }) + T(136, 182, 'từ 10 lên 20 m/s trong 10 s');
    return wrap('0 0 330 194', b, cap, 'Xe máy và ô tô lúc đèn xanh');
  },
  // Trang 1 · thí nghiệm: vị trí bi sau mỗi 0,2 s ở ba đoạn
  vetBi: (cap = 'Vị trí viên bi sau mỗi 0,2 s ở ba đoạn đường.') => {
    let b = defs('vb');
    const hang = [['trên bàn', [0, 48, 96, 144, 192]], ['xuống máng', [0, 20, 52, 98, 158]], ['lên máng', [0, 72, 128, 168, 192]]];
    hang.forEach(([ten, xs], i) => {
      const y = 36 + i * 66;
      b += T(6, y - 14, ten, { w: 700 }) + ln(110, y, 318, y, GREY, 2);
      b += xs.map((x, k) => `<circle cx="${118 + x}" cy="${y}" r="7" fill="${k ? '#fff' : INK}" stroke="${INK}" stroke-width="2.4"/>`).join('');
      b += arr(8, y + 8, 30, y + 8, 'vb', BLUE, '', 2.4) + T(36, y + 15, 'chiều đi', { c: BLUE });
    });
    return wrap('0 0 330 190', b, cap, 'Vết viên bi sau mỗi 0,2 s');
  },
  // Trang 2 · thí nghiệm xe lăn xuống máng nghiêng có cảm biến
  xeMang: (cap = 'Cảm biến ở đỉnh máng ghi vận tốc xe mỗi 0,2 s.') => {
    let b = defs('xm1');
    b += `<path d="M14,170 L300,170 L300,80 z" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    const g = 'transform="rotate(-17.5 180 132)"';
    b += `<g ${g}><rect x="150" y="104" width="60" height="22" rx="4" fill="#fff" stroke="${INK}" stroke-width="${SW}"/><circle cx="162" cy="131" r="6" fill="#fff" stroke="${INK}" stroke-width="2.4"/><circle cx="198" cy="131" r="6" fill="#fff" stroke="${INK}" stroke-width="2.4"/></g>`;
    b += `<rect x="282" y="46" width="34" height="28" rx="4" fill="${GREY}" stroke="${INK}" stroke-width="2.4"/>` + T(312, 34, 'cảm biến', { a: 'end' });
    b += arr(150, 96, 92, 114, 'xm1', BLUE, '6 4') + T(70, 98, 'v ?', { c: BLUE, w: 700, a: 'end' });
    return wrap('0 0 330 184', b, cap, 'Xe lăn trên máng nghiêng');
  },
  // Trang 2 · bốn trường hợp v và a — HS ghi nhanh/chậm dần dưới mỗi ô
  bonChieu: (cap = 'Chiều dương sang phải. v nét liền, a nét đứt. Ghi “nhanh” hay “chậm” vào ô.') => {
    let b = defs('bc1') + defs('bc2');
    const ca = [['a', 1, 1], ['b', 1, -1], ['c', -1, 1], ['d', -1, -1]];
    ca.forEach(([n, sv, sa], i) => {
      const cx = 44 + i * 80, y1 = 40, y2 = 86;
      b += T(cx, 18, `(${n})`, { a: 'middle', w: 700 });
      b += arr(f1(cx - sv * 30), y1, f1(cx + sv * 30), y1, 'bc1', BLUE) + T(cx, y1 - 8, 'v', { c: BLUE, w: 700, a: 'middle' });
      b += arr(f1(cx - sa * 22), y2, f1(cx + sa * 22), y2, 'bc2', RED, '6 4') + T(cx, y2 - 8, 'a', { c: RED, w: 700, a: 'middle' });
      b += `<rect x="${cx - 32}" y="104" width="64" height="30" rx="4" fill="#fff" stroke="${INK}" stroke-width="2"/>`;
    });
    b += arr(8, 158, 320, 158, 'bc1', INK) + T(318, 184, '+', { a: 'end', w: 700 });
    return wrap('0 0 330 192', b, cap, 'Bốn cặp vectơ vận tốc và gia tốc');
  },
  // Trang 3 · ba dạng đồ thị v–t
  baDoThi: (cap = `Ba vật, v > 0. Ghi tên chuyển động cạnh ${vongH(1)} ${vongH(2)} ${vongH(3)}.`) => {
    let b = defs('bd');
    const X0 = 40, X1 = 300, Y0 = 18, Y1 = 170;
    b += arr(X0, Y1, X1 + 16, Y1, 'bd') + arr(X0, Y1 + 4, X0, Y0 - 10, 'bd') + T(X1 + 16, Y1 + 24, 't', { a: 'end' }) + T(X0 + 8, Y0, 'v');
    b += ln(X0, 120, 290, 120, RED, 3.4) + vong(306, 120, 1);
    b += ln(X0, 150, 280, 40, RED, 3.4, '9 5') + vong(296, 40, 2);
    b += ln(X0, 60, 260, 164, RED, 3.4, '3 5') + vong(276, 166, 3);
    return wrap('0 0 330 198', b, cap, 'Ba dạng đồ thị vận tốc – thời gian');
  },
  // Trang 4 · bài toán mẫu: ô tô hãm phanh, diện tích tam giác
  phanh: (cap = 'Ô tô hãm phanh: v giảm đều về 0. Diện tích phần tô là gì?') => vt([[0, 15], [5, 0]], { tm: 6, vm: 18, tk: [1, 2, 3, 4, 5], vk: [5, 10, 15], to: true, cap, id: 'ph' }),
  // Trang 5 · thử thách ★★★: v = 4 − 2t, vạch số nguyên, đổi dấu
  doiChieu: (cap = 'v = 4 − 2t. Đọc dấu của v và a lúc t = 3 s.') => vt([[0, 4], [3.5, -3]], { tm: 4, vm: 5, vmin: -4, tk: [1, 2, 3, 4], vk: [-2, 2, 4], cap, id: 'dc' }),

  // ===== Bài tập mẫu =====
  chieuDuong: (cap = 'Hai cách chọn chiều dương cho cùng một xe đang phanh.') => {
    let b = defs('cd1') + defs('cd2');
    b += xe(130, 20, 64, 26) + arr(200, 34, 270, 34, 'cd1', BLUE) + T(276, 30, 'v', { c: BLUE, w: 700 });
    b += arr(30, 106, 300, 106, 'cd2', INK) + T(306, 112, '+', { w: 700 }) + T(20, 96, 'câu a)', { w: 700 });
    b += arr(300, 160, 30, 160, 'cd2', INK) + T(14, 166, '+', { w: 700 }) + T(240, 150, 'câu b)', { w: 700 });
    return wrap('0 0 330 182', b, cap, 'Hai chiều dương');
  },
  tauDien: (cap = 'Đồ thị v–t của tàu điện.') => vt([[0, 0], [6, 12], [16, 12], [24, 0]], { tm: 29, vm: 14, tk: [6, 16, 24], vk: [12], so: [1, 2, 3], cap, id: 'td', cao: 136 }),
  luoiTrong: (cap = 'Nối các mốc đề cho thành đồ thị v–t.') => vt([[0, 0]], { tm: 35, vm: 14, tk: [8, 20, 30], vk: [4, 8, 12], an: true, cap, id: 'lt' }),
  bongTuong: (cap = 'Vectơ v<sub>1</sub> (trước) và v<sub>2</sub> (sau) ngược hướng nhau.') => {
    let b = defs('bt1') + defs('bt2');
    b += `<rect x="292" y="10" width="24" height="168" fill="${GREY}" stroke="${INK}" stroke-width="2.4"/>`;
    b += `<circle cx="250" cy="70" r="14" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + `<circle cx="250" cy="138" r="14" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += arr(120, 70, 228, 70, 'bt1', BLUE) + T(120, 56, `v${sb('1')}= 25 m/s`, { c: BLUE, w: 700 });
    b += arr(232, 138, 160, 138, 'bt2', RED, '6 4') + T(30, 166, `v${sb('2')}= 15 m/s`, { c: RED, w: 700 });
    b += T(10, 30, 'tây', { c: GREY }) + T(280, 30, 'đông', { c: GREY, a: 'end' });
    return wrap('0 0 330 186', b, cap, 'Bóng đập tường bật lại');
  },
  // ===== Bài tương tự =====
  thangMay: (cap = 'Thang máy đi lên.') => vt([[0, 0], [2, 3], [8, 3], [11, 0]], { tm: 13.5, vm: 4, tk: [2, 8, 11], vk: [1, 2, 3], so: [1, 2, 3], cap, id: 'tm' }),
  xeBon: (cap = 'Xe chạy thẳng, không đổi chiều.') => vt([[0, 2], [4, 10], [10, 10], [15, 0]], { tm: 18.5, vm: 12, tk: [4, 10, 15], vk: [2, 10], so: [1, 2, 3], cap, id: 'xb' }),
};
