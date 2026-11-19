// Hình minh hoạ cho ruột tập VL12 · Chương 3 · Bài 9 Khái niệm từ trường (lesson 10). Cùng quy tắc với hinh.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8 (đường sức 2,2 nét đứt), tự vẽ.
// Nam châm theo hình chuẩn (svg_lib.py bar_magnet: nửa N đỏ, nửa S xanh, chữ trắng đậm, hơi xiên); đường sức nét đứt, đầu mũi tên
// chữ V 30° (svg_lib.py chevron). Hình đứng cạnh ô hỏi CHIỀU từ trường thì đường sức để KHÔNG có mũi tên (HS tự vẽ) — không lộ đáp án.
// Xem thử: node scripts/ruot-tap/l12-c3-bai9.mjs --hinh (chụp vào out/hinh-l12-c3-bai9/).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const arr = (x1, y1, x2, y2, id, c = INK, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${SW}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;

// ---- đầu mũi tên chữ V 30° (chép svg_lib.py chevron) + đường sức nét đứt
const chev = (x, y, dx, dy, c = INK, w = 2.2, L = 12, ang = 30) => {
  const n = Math.hypot(dx, dy) || 1, ux = dx / n, uy = dy / n, a = (ang * Math.PI) / 180;
  const p = [1, -1].map((s) => { const bx = ux * Math.cos(a) - uy * Math.sin(s * a), by = ux * Math.sin(s * a) + uy * Math.cos(a); return [x - L * bx, y - L * by]; });
  return `<path d="M${p[0][0].toFixed(1)},${p[0][1].toFixed(1)} L${x},${y} L${p[1][0].toFixed(1)},${p[1][1].toFixed(1)}" fill="none" stroke="${c}" stroke-width="${w}" stroke-linejoin="miter" stroke-miterlimit="10"/>`;
};
const DS = '7 5';
const duong = (d, c = INK, w = 2.2) => `<path d="${d}" fill="none" stroke="${c}" stroke-width="${w}" stroke-dasharray="${DS}"/>`;

// ---- nam châm thẳng chuẩn (svg_lib.py bar_magnet): tâm (cx, cy), dài L, cao H; nRight = cực N bên phải; nhan = ['N','S'] hoặc ['?','?']
const UM_EDGE = '#334155', UM_N = ['#dc2626', '#f87171', '#b91c1c'], UM_S = ['#2563eb', '#60a5fa', '#1e40af'];
const thanh = (cx, cy, L, H, { nRight = true, d = [8, -6], fs = 22, nhan = null } = {}) => {
  const [dx, dy] = d, x0 = cx - L / 2, x1 = cx + L / 2, y0 = cy - H / 2, xm = cx;
  const [CL, CR] = nRight ? [UM_S, UM_N] : [UM_N, UM_S];
  const P = (pts, f) => `<polygon points="${pts.map(([a, b]) => `${a.toFixed(1)},${b.toFixed(1)}`).join(' ')}" fill="${f}" stroke="${UM_EDGE}" stroke-width="2" stroke-linejoin="round"/>`;
  let o = P([[x0, y0], [xm, y0], [xm + dx, y0 + dy], [x0 + dx, y0 + dy]], CL[1]) + P([[xm, y0], [x1, y0], [x1 + dx, y0 + dy], [xm + dx, y0 + dy]], CR[1])
    + P([[x1, y0], [x1 + dx, y0 + dy], [x1 + dx, y0 + H + dy], [x1, y0 + H]], CR[2]);
  o += `<rect x="${x0}" y="${y0}" width="${L / 2}" height="${H}" fill="${CL[0]}" stroke="${UM_EDGE}" stroke-width="2"/><rect x="${xm}" y="${y0}" width="${L / 2}" height="${H}" fill="${CR[0]}" stroke="${UM_EDGE}" stroke-width="2"/>`;
  const [l, r] = nhan ?? (nRight ? ['S', 'N'] : ['N', 'S']);
  o += T(x0 + L / 4, cy + fs * 0.36, l, { c: '#fff', size: fs, a: 'middle', w: 700 }) + T(x1 - L / 4, cy + fs * 0.36, r, { c: '#fff', size: fs, a: 'middle', w: 700 });
  return o;
};

// ---- la bàn nhìn từ trên: vòng + kim (nửa đỏ = đầu N); goc = độ, 0 = chỉ lên, dương = quay theo chiều kim đồng hồ
const laBan = (cx, cy, r, goc = 0, kim = true) => {
  let o = `<circle cx="${cx}" cy="${cy}" r="${r}" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
  if (kim) {
    const k = r * 0.78, w = r * 0.2;
    o += `<g transform="rotate(${goc} ${cx} ${cy})"><polygon points="${cx},${cy - k} ${cx + w},${cy} ${cx - w},${cy}" fill="${RED}"/><polygon points="${cx},${cy + k} ${cx + w},${cy} ${cx - w},${cy}" fill="#fff" stroke="${INK}" stroke-width="1.6"/></g>`;
    o += `<circle cx="${cx}" cy="${cy}" r="3" fill="${INK}"/>`;
  }
  return o;
};
// ký hiệu dòng điện vuông góc trang: ra (⊙) hay vào (⊗)
const dongDien = (x, y, ra, r = 13) => `<circle cx="${x}" cy="${y}" r="${r}" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
  + (ra ? `<circle cx="${x}" cy="${y}" r="4" fill="${INK}"/>` : ln(x - r * 0.62, y - r * 0.62, x + r * 0.62, y + r * 0.62, INK, 2.4) + ln(x - r * 0.62, y + r * 0.62, x + r * 0.62, y - r * 0.62, INK, 2.4));
const diem = (x, y, s, o = {}) => `<circle cx="${x}" cy="${y}" r="5" fill="${INK}"/>` + T(x + (o.dx ?? 9), y + (o.dy ?? -8), s, { w: 700, ...o });
// hoa hướng: Bắc trên, Đông phải
const huong = (x, y) => arr(x, y + 26, x, y - 6, 'hh', GREY) + T(x, y - 12, 'Bắc', { a: 'middle', size: 18, c: GREY });

// đường sức quanh thanh nằm ngang (tâm cx, cy, dài L): các vòng từ đầu phải sang đầu trái, trên và dưới; không mũi tên
const vongThanh = (cx, cy, L, hs = [34, 66], c = INK) => {
  const x0 = cx - L / 2 + 6, x1 = cx + L / 2 - 6;
  let o = '';
  for (const h of hs) for (const s of [-1, 1]) {
    const yy = cy + s * 14, k = h * 1.35;
    o += duong(`M${x1},${yy} C${x1 + k},${yy + s * h * 1.2} ${x0 - k},${yy + s * h * 1.2} ${x0},${yy}`, c);
  }
  return o;
};

export const hinhL12c3b9 = {
  // ===== Trang 1 =====
  laBanCua: (cap = 'Xoay máy: kim vẫn chỉ một phía. Đặt sát cửa sắt: kim lệch.') => {
    let b = `<rect x="14" y="28" width="96" height="150" rx="12" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + laBan(62, 103, 34, 0);
    b += `<g transform="rotate(-25 62 103)">${''}</g>`;
    b += `<rect x="250" y="8" width="54" height="190" fill="#e7eaf1" stroke="${INK}" stroke-width="${SW}"/>` + T(277, 220, 'cửa sắt', { a: 'middle' });
    for (let y = 26; y < 190; y += 22) b += ln(256, y, 298, y, GREY, 1.6);
    b += `<rect x="146" y="28" width="96" height="150" rx="12" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + laBan(194, 103, 34, 58);
    b += T(62, 220, 'xa cửa', { a: 'middle' });
    return wrap('0 0 312 230', b, cap, 'La bàn điện thoại xa và gần cửa sắt');
  },
  tuongTac: (cap = 'Vẽ mũi tên lực lên mỗi nam châm.') => {
    let b = thanh(70, 40, 110, 30, { nRight: true }) + thanh(234, 40, 110, 30, { nRight: false });
    b += T(152, 47, '?', { a: 'middle', w: 700, size: 24 });
    b += thanh(70, 118, 110, 30, { nRight: true }) + thanh(234, 118, 110, 30, { nRight: true });
    b += T(152, 125, '?', { a: 'middle', w: 700, size: 24 });
    b += T(4, 84, '(1)', { w: 700 }) + T(4, 162, '(2)', { w: 700 });
    return wrap('0 0 300 172', b, cap, 'Hai cặp nam châm đặt đối diện');
  },
  // ===== Trang 2 =====
  oersted: (cap = 'Nhìn từ trên: dây căng song song, ngay phía trên kim.') => {
    let b = laBan(110, 96, 50, 0);
    b += ln(124, 12, 124, 176, '#b45309', 4) + T(134, 30, 'dây đồng', { size: 18 });
    b += ln(124, 12, 250, 12, INK, SW) + ln(250, 12, 250, 70, INK, SW) + ln(124, 176, 250, 176, INK, SW) + ln(250, 126, 250, 176, INK, SW);
    b += ln(236, 80, 264, 80, INK, SW) + ln(243, 92, 257, 92, INK, 5) + ln(250, 70, 250, 80, INK, SW) + ln(250, 92, 250, 104, INK, SW) + T(270, 92, 'pin', { size: 18 });
    b += `<circle cx="250" cy="104" r="3.5" fill="${INK}"/>` + ln(250, 104, 268, 120, INK, SW) + `<circle cx="250" cy="126" r="3.5" fill="${INK}"/>` + T(272, 128, 'K', { w: 700 });
    b += huong(26, 40);
    return wrap('0 0 300 190', b, cap, 'Thí nghiệm Oersted nhìn từ trên');
  },
  // ===== Trang 3 =====
  duongSucThanh: (cap = 'Vẽ thêm mũi tên chiều đường sức, cả đoạn trong thanh.') => {
    let b = vongThanh(150, 100, 120) + thanh(150, 100, 120, 30, { nRight: true });
    b += duong('M30,100 L84,100') + duong('M216,100 L278,100');
    return wrap('0 0 300 200', b, cap, 'Đường sức quanh thanh nam châm, chưa có mũi tên');
  },
  dayThang: (cap = 'Dòng điện hướng ra phía em. Vẽ chiều đường sức.') => {
    let b = '';
    for (const r of [34, 62, 92]) b += `<circle cx="110" cy="104" r="${r}" fill="none" stroke="${INK}" stroke-width="2.2" stroke-dasharray="${DS}"/>`;
    b += dongDien(110, 104, true) + T(214, 60, 'mặt phẳng', { size: 18 }) + T(214, 82, 'vuông góc', { size: 18 }) + T(214, 104, 'với dây', { size: 18 });
    return wrap('0 0 300 206', b, cap, 'Đường sức quanh dây thẳng, chưa có mũi tên');
  },
  // ===== Trang 4 =====
  traiDat: (cap = 'Ghi tên cực từ vào hai ô “?”.') => {
    let b = `<circle cx="120" cy="110" r="84" fill="#eef2fa" stroke="${INK}" stroke-width="${SW}"/>`;
    b += ln(120, 10, 120, 210, GREY, 2, '6 5') + T(120, 6 + 18, '', {});
    b += `<g transform="rotate(12 120 110)">${thanh(120, 110, 30, 110, { nRight: true, d: [0, 0], nhan: ['', ''] }).replace(/<text[^>]*>[^<]*<\/text>/g, '')}</g>`;
    b += `<g transform="rotate(12 120 110)"><rect x="104" y="40" width="32" height="30" fill="#fff" stroke="${INK}" stroke-width="2"/>${T(120, 62, '?', { a: 'middle', w: 700, size: 22 })}<rect x="104" y="150" width="32" height="30" fill="#fff" stroke="${INK}" stroke-width="2"/>${T(120, 172, '?', { a: 'middle', w: 700, size: 22 })}</g>`;
    b += T(214, 24, 'Bắc địa lí', { a: 'middle', size: 19 }) + T(214, 210, 'Nam địa lí', { a: 'middle', size: 19 });
    b += ln(170, 24, 128, 24, GREY, 1.6) + ln(170, 206, 128, 206, GREY, 1.6);
    return wrap('0 0 290 220', b, cap, 'Trái Đất như một nam châm, trục từ lệch trục quay');
  },
  camBien: (cap = 'Điện thoại có cảm biến từ, lùi xa dần nam châm.') => {
    let b = thanh(70, 60, 100, 28, { nRight: true });
    b += `<rect x="196" y="22" width="54" height="80" rx="9" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(223, 70, 'B', { a: 'middle', w: 700, size: 24 });
    b += ln(124, 122, 196, 122, GREY, 2) + ln(124, 114, 124, 130, GREY, 2) + ln(196, 114, 196, 130, GREY, 2) + T(160, 148, 'd', { a: 'middle', w: 700, size: 22 });
    return wrap('0 0 270 156', b, cap, 'Đo cảm ứng từ theo khoảng cách');
  },
  // ===== Trang 5 =====
  vectoMau: (cap = 'Kim chỉ theo vectơ tổng; góc lệch đo từ hướng bắc.') => {
    let b = defs('vm1') + defs('vm2') + defs('vm3');
    const O = [60, 186];
    b += arr(...O, 60, 70, 'vm1', BLUE) + T(68, 92, `B${sb('đ')}`, { c: BLUE, w: 700 });
    b += arr(...O, 214, 186, 'vm2', RED, '7 4') + T(200, 214, `B${sb('1')}`, { c: RED, w: 700, a: 'middle' });
    b += ln(60, 70, 214, 70, GREY, 1.8, '4 4') + ln(214, 186, 214, 70, GREY, 1.8, '4 4');
    b += arr(...O, 212, 72, 'vm3', INK) + T(222, 66, 'B', { w: 700 });
    b += `<path d="M60,140 A46,46 0 0 1 89,150" fill="none" stroke="${INK}" stroke-width="2"/>` + T(80, 132, gk('α'), { size: 22 });
    b += T(60, 50, 'Bắc', { a: 'middle', size: 18, c: GREY }) + T(256, 192, 'Đông', { a: 'end', size: 18, c: GREY });
    return wrap('0 0 270 222', b, cap, 'Tổng hợp hai từ trường vuông góc');
  },
  // ===== Bài tập mẫu =====
  thanhD1: (cap = 'Đường sức chưa có mũi tên.') => {
    let b = vongThanh(140, 88, 120, [26, 50]) + thanh(140, 88, 120, 30, { nRight: true });
    b += duong('M206,88 L286,88');
    b += diem(140, 52, 'M', { dx: -8, dy: -6, a: 'end' }) + diem(250, 88, 'P', { dy: -10 });
    b += `<circle cx="140" cy="88" r="4" fill="${INK}"/>` + T(146, 128, 'Q', { w: 700 });
    b += diem(226, 60, 'A', { dy: -2 }) + diem(30, 150, 'B', { dy: 6 });
    return wrap('0 0 296 166', b, cap, 'Thanh nam châm với các điểm M, P, Q, A, B');
  },
  dayD2: (cap = 'Dòng điện hướng ra phía em.') => {
    let b = '';
    for (const r of [30, 84]) b += `<circle cx="112" cy="100" r="${r}" fill="none" stroke="${GREY}" stroke-width="2" stroke-dasharray="${DS}"/>`;
    b += dongDien(112, 100, true);
    b += diem(142, 100, 'A', { dy: 24 }) + diem(112, 70, 'B', { dx: 9, dy: -4 }) + diem(28, 100, 'C', { dx: 9, dy: 24 });
    return wrap('0 26 240 148', b, cap, 'Ba điểm A, B, C quanh dây thẳng');
  },
  laBanD3: (cap = 'Nhìn từ trên; dây ngay trên la bàn.') => {
    let b = defs('d3a') + laBan(110, 96, 46, 0, false);
    b += ln(110, 24, 110, 170, '#b45309', 4) + chev(110, 38, 0, -1, '#b45309', 3.2, 14) + T(120, 32, 'I', { w: 700, c: '#b45309' });
    b += arr(210, 150, 210, 60, 'd3a', BLUE) + T(218, 108, `B${sb('đ')}`, { c: BLUE, w: 700 });
    b += T(210, 42, 'Bắc', { a: 'middle', size: 18, c: GREY }) + T(30, 102, 'Tây', { a: 'middle', size: 18, c: GREY }) + T(210, 172, 'Nam', { a: 'middle', size: 18, c: GREY });
    return wrap('0 18 262 162', b, cap, 'La bàn dưới dây dẫn nằm theo phương bắc nam');
  },
  haiDayD4: (cap = 'Nhìn về hướng bắc (vào trang).') => {
    let b = dongDien(140, 24, false) + T(162, 30, '(1)', { w: 700 });
    b += `<ellipse cx="140" cy="88" rx="60" ry="15" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(206, 94, 'la bàn', { size: 18 });
    b += dongDien(140, 152, true) + T(162, 158, '(2)', { w: 700 });
    b += T(40, 94, 'Tây', { a: 'middle', size: 19, c: GREY }) + T(270, 130, 'Đông', { a: 'end', size: 19, c: GREY });
    return wrap('0 0 280 172', b, cap, 'Hai dây trên và dưới la bàn, nhìn về hướng bắc');
  },
  // ===== Bài tương tự =====
  dayTT: (cap = 'Dòng điện đi vào trang.') => {
    let b = `<circle cx="120" cy="100" r="60" fill="none" stroke="${GREY}" stroke-width="2" stroke-dasharray="${DS}"/>` + dongDien(120, 100, false);
    b += diem(60, 100, 'A', { dx: -8, dy: -10, a: 'end' }) + diem(120, 160, 'B', { dx: 9, dy: 20 }) + diem(140, 100, 'C', { dy: -10 });
    return wrap('0 0 240 196', b, cap, 'Ba điểm quanh dây có dòng điện đi vào trang');
  },
};
