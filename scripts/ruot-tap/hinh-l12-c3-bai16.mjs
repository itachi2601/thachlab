// Hình minh hoạ cho ruột tập VL12 Chương 3 · Bài 16 Điện từ trường. Mô hình sóng điện từ (lesson 127). Cùng quy tắc với hinh.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh (không ghi "vuông góc", "cùng pha", "biến thiên sinh…").
// Xem thử: node scripts/ruot-tap/l12-c3-bai16.mjs --hinh (chụp vào out/hinh-l12-c3-bai16/).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
// chữ Hi Lạp: Source Sans 3 chỉ nạp latin/vietnamese → lấy từ KaTeX_Math (đã nạp qua katex.min.css)
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const km = (ch) => `<tspan font-family="KaTeX_Main">${ch}</tspan>`;
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const arr = (x1, y1, x2, y2, id, c = INK, dash = '', w = SW) =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const pl = (pts, c = INK, w = SW, dash = '') =>
  `<polyline points="${pts.map((p) => p.map((v) => v.toFixed(1)).join(',')).join(' ')}" fill="none" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const rect = (x, y, w, h, o = {}) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${o.rx ?? 3}" fill="${o.fill ?? '#fff'}" stroke="${o.c ?? INK}" stroke-width="${o.w ?? SW}"/>`;
const circ = (x, y, r, o = {}) => `<circle cx="${x}" cy="${y}" r="${r}" fill="${o.fill ?? '#fff'}" stroke="${o.c ?? INK}" stroke-width="${o.w ?? SW}"${o.dash ? ` stroke-dasharray="${o.dash}"` : ''}/>`;
const doan = (x1, x2, y, nhan) => ln(x1, y, x2, y, GREY, 2) + ln(x1, y - 6, x1, y + 6, GREY, 2) + ln(x2, y - 6, x2, y + 6, GREY, 2)
  + T((x1 + x2) / 2, y - 7, nhan, { a: 'middle' });
const sinPts = (x0, x1, f) => Array.from({ length: 61 }, (_, i) => { const x = x0 + (x1 - x0) * i / 60; return f(x); });

export const hinhL12c3b16 = {
  // ===== Trang 1 · Dự đoán: bếp từ và radio, không vẽ sóng (không lộ đáp án) =====
  bepTu: (cap = 'Bếp từ đang nấu; radio chạy pin đặt cách 2 m kêu rè.') => {
    let b = ln(6, 150, 294, 150, GREY, 2);
    b += rect(10, 112, 116, 38) + `<ellipse cx="68" cy="122" rx="40" ry="6" fill="none" stroke="${GREY}" stroke-width="2"/>`;
    b += rect(34, 78, 68, 34, { rx: 4 }) + ln(26, 84, 34, 84) + ln(102, 84, 110, 84);
    b += T(68, 140, 'bếp từ', { a: 'middle' }) + T(68, 70, 'nồi', { a: 'middle' });
    b += rect(196, 100, 92, 50, { rx: 6 }) + circ(222, 125, 13, { w: 2.2 }) + [252, 262, 272].map((x) => ln(x, 112, x, 138, INK, 2)).join('');
    b += ln(278, 100, 290, 30, INK, 2.4) + `<circle cx="290" cy="30" r="3" fill="${INK}"/>` + T(270, 40, 'ăng ten', { a: 'end' });
    b += T(242, 92, 'radio', { a: 'middle' });
    b += doan(126, 196, 176, '2 m');
    return wrap('0 0 300 186', b, cap, 'Bếp từ và radio chạy pin cách nhau hai mét');
  },
  // ===== Trang 1 · II.1: nam châm rơi qua ống dây nối điện kế =====
  namCham: (cap = 'Nam châm rơi qua ống dây nối kín với điện kế G.') => {
    let b = defs('nc');
    for (let i = 0; i < 8; i++) b += `<ellipse cx="170" cy="${96 + i * 14}" rx="34" ry="6" fill="none" stroke="${INK}" stroke-width="2.4"/>`;
    b += rect(156, 12, 28, 30, { rx: 0, fill: '#f3d6d3' }) + rect(156, 42, 28, 30, { rx: 0 });
    b += T(170, 34, 'N', { a: 'middle', w: 700 }) + T(170, 64, 'S', { a: 'middle', w: 700 });
    b += arr(222, 20, 222, 66, 'nc', RED) + T(232, 50, 'rơi', { c: RED });
    b += pl([[136, 96], [60, 96], [60, 128]]) + pl([[136, 194], [60, 194], [60, 164]]);
    b += circ(60, 146, 18) + T(60, 153, 'G', { a: 'middle', w: 700 });
    b += T(214, 160, 'ống dây');
    return wrap('0 0 300 206', b, cap, 'Nam châm thẳng rơi qua ống dây nối điện kế');
  },
  // ===== Trang 2 · II.2: mạch có tụ nối nguồn xoay chiều =====
  tuXoayChieu: (cap = 'Mạch có tụ C nối nguồn xoay chiều tần số f; ampe kế A.') => {
    let b = '';
    b += pl([[50, 72], [50, 26], [250, 26], [250, 82]]) + pl([[50, 118], [50, 166], [250, 166], [250, 112]]);
    b += circ(50, 95, 22) + `<path d="M38,95 q6,-10 12,0 t12,0" fill="none" stroke="${INK}" stroke-width="2.4"/>`;
    b += T(16, 101, 'f', { a: 'middle', w: 700 });
    b += circ(150, 26, 16) + T(150, 33, 'A', { a: 'middle', w: 700 });
    b += ln(212, 82, 288, 82, INK, 4) + ln(212, 112, 288, 112, INK, 4);
    b += [226, 250, 274].map((x) => ln(x, 86, x, 108, GREY, 2, '4 3')).join('');
    b += T(204, 104, 'cách điện', { a: 'end' }) + T(282, 146, 'C', { a: 'middle', w: 700 });
    return wrap('0 0 300 180', b, cap, 'Mạch điện có tụ điện nối nguồn xoay chiều');
  },
  // ===== Trang 3 · II.4: ảnh chụp sóng điện từ tại một thời điểm =====
  songEB: (cap = 'Sóng điện từ chụp tại một thời điểm, lan theo chiều mũi tên v.') => {
    const y0 = 104, x0 = 30, k = 2 * Math.PI / 120, A = 56;
    let b = defs('sea') + defs('seb') + defs('sev');
    b += arr(x0, y0, 292, y0, 'sev', INK) + T(288, y0 + 26, 'v', { a: 'end', w: 700 });
    b += ln(x0, y0 - 70, x0, y0 + 10, GREY, 1.8, '4 4');
    b += pl(sinPts(x0, 270, (x) => [x, y0 - A * Math.sin(k * (x - x0))]), RED);
    b += pl(sinPts(x0, 270, (x) => { const s = Math.sin(k * (x - x0)); return [x - 0.55 * A * s, y0 + 0.5 * A * s]; }), BLUE, SW, '7 4');
    for (const x of [60, 180]) {
      b += arr(x, y0, x, y0 - A + 4, 'sea', RED, '', 2.4);
      b += arr(x, y0, x - 0.55 * A + 3, y0 + 0.5 * A - 3, 'seb', BLUE, '', 2.4);
    }
    b += T(66, y0 - A - 4, 'E', { c: RED, w: 700 }) + T(26, y0 + 40, 'B', { c: BLUE, w: 700 });
    return wrap('0 0 300 172', b, cap, 'Vectơ điện trường và cảm ứng từ của sóng điện từ');
  },
  // ===== Trang 3 · II.5: thang sóng — sáu ô để học sinh tự ghi tên =====
  thangSong: (cap = 'Sáu vùng của thang sóng điện từ: ghi tên vùng vào bảng theo số (1)–(6).') => {
    const w = [70, 50, 14, 50, 50, 46];
    let x = 10, b = defs('ts');
    w.forEach((d, i) => {
      b += rect(x, 40, d, 38, { rx: 0, fill: i === 2 ? '#e3e8f3' : '#fff', w: 2.4 });
      b += T(x + d / 2, i === 2 ? 30 : 66, `(${i + 1})`, { a: 'middle', w: 700, size: i === 2 ? 18 : 20 });
      x += d;
    });
    b += arr(14, 100, 286, 100, 'ts', INK, '', 2.4) + T(150, 124, `bước sóng ${gk('λ')} giảm dần`, { a: 'middle' });
    return wrap('0 0 300 132', b, cap, 'Thang sóng điện từ chia sáu vùng');
  },
  // ===== Trang 4 · Bẫy 1: hai kiểu đường sức điện =====
  duongSuc: (cap = 'Hai kiểu đường sức điện trường (1) và (2); vòng tròn có dấu ×: đường cảm ứng từ đi vào trang.') => {
    let b = defs('ds1') + defs('ds2');
    b += circ(34, 76, 14) + T(34, 83, '+', { a: 'middle', w: 700, size: 22 }) + circ(126, 76, 14) + T(126, 83, '−', { a: 'middle', w: 700, size: 22 });
    b += ln(48, 76, 112, 76, RED, 2.4) + `<path d="M46,68 Q80,26 114,68" fill="none" stroke="${RED}" stroke-width="2.4"/><path d="M46,84 Q80,126 114,84" fill="none" stroke="${RED}" stroke-width="2.4"/>`;
    b += arr(78, 76, 86, 76, 'ds1', RED, '', 2.4) + T(80, 150, '(1)', { a: 'middle', w: 700 });
    const X = (x, y) => circ(x, y, 9, { w: 2 }) + ln(x - 6, y - 6, x + 6, y + 6, BLUE, 2) + ln(x - 6, y + 6, x + 6, y - 6, BLUE, 2);
    b += X(214, 66) + X(240, 66) + X(227, 88);
    b += `<ellipse cx="227" cy="76" rx="46" ry="34" fill="none" stroke="${RED}" stroke-width="2.4"/><ellipse cx="227" cy="76" rx="64" ry="52" fill="none" stroke="${RED}" stroke-width="2.4"/>`;
    b += arr(229, 42, 222, 42, 'ds2', RED, '', 2.4) + arr(229, 24, 220, 24, 'ds2', RED, '', 2.4);
    b += T(227, 150, '(2)', { a: 'middle', w: 700 });
    return wrap('0 0 300 158', b, cap, 'Đường sức điện trường tĩnh và điện trường xoáy');
  },
  // ===== Trang 5 · Bài toán mẫu: đài FM qua vệ tinh địa tĩnh =====
  veTinh: (cap = 'Không theo tỉ lệ.') => {
    let b = defs('vt1') + defs('vt2');
    b += `<path d="M6,166 Q150,130 294,166" fill="none" stroke="${INK}" stroke-width="${SW}"/>` + T(150, 166, 'Trái Đất', { a: 'middle', c: GREY });
    b += rect(140, 14, 20, 16, { rx: 1 }) + rect(110, 17, 26, 10, { rx: 0, w: 2, fill: '#e3e8f3' }) + rect(164, 17, 26, 10, { rx: 0, w: 2, fill: '#e3e8f3' });
    b += T(196, 30, 'vệ tinh');
    b += `<path d="M108,148 l8,-16 l8,16 z" fill="#fff" stroke="${INK}" stroke-width="2.4"/>` + `<rect x="178" y="138" width="16" height="10" fill="#fff" stroke="${INK}" stroke-width="2.4"/>`;
    b += T(102, 148, 'đài', { a: 'end' }) + T(200, 150, 'máy thu');
    b += arr(118, 128, 146, 36, 'vt1', RED) + arr(154, 36, 184, 132, 'vt2', BLUE, '7 4');
    b += ln(254, 22, 254, 142, GREY, 2) + ln(246, 22, 262, 22, GREY, 2) + ln(246, 142, 262, 142, GREY, 2) + T(264, 90, 'h', { w: 700 });
    return wrap('0 0 300 174', b, cap, 'Tín hiệu đi từ đài lên vệ tinh rồi xuống máy thu');
  },
  // ===== Trang 6 · Dạng 3: E và B theo thời gian tại một điểm =====
  dongPha: (cap = 'Đường đứt: lúc E = 6,0 V/m.') => {
    const A = 26, P = (yc, x) => [x, yc - A * Math.cos(2 * Math.PI * (x - 40) / 200)];
    let b = defs('dp');
    b += arr(40, 36, 292, 36, 'dp', GREY, '', 2) + arr(40, 102, 292, 102, 'dp', GREY, '', 2);
    b += pl(sinPts(40, 280, (x) => P(36, x)), RED) + pl(sinPts(40, 280, (x) => P(102, x)), BLUE, SW, '7 4');
    b += T(8, 42, 'E', { c: RED, w: 700 }) + T(8, 108, 'B', { c: BLUE, w: 700 }) + T(292, 58, 't', { a: 'end' }) + T(292, 124, 't', { a: 'end' });
    const xm = 40 + Math.acos(1 / 3) / (2 * Math.PI) * 200;
    b += ln(xm, 4, xm, 134, INK, 2, '5 4') + `<circle cx="${xm}" cy="${36 - A / 3}" r="4" fill="${RED}"/><circle cx="${xm}" cy="${102 - A / 3}" r="4" fill="${BLUE}"/>`;
    b += T(xm + 8, 22, '6,0') + T(xm + 8, 88, '?', { w: 700 });
    return wrap('0 0 300 136', b, cap, 'Đồ thị E và B theo thời gian tại một điểm');
  },
  // ===== Trang 7 · Dạng 5: ra-đa – Mặt Trăng =====
  raDa: (cap = 'Không theo tỉ lệ.') => {
    let b = defs('rd1') + defs('rd2');
    b += circ(36, 44, 28) + T(36, 51, 'TĐ', { a: 'middle', w: 700 }) + circ(270, 44, 14, { fill: '#e3e8f3' }) + T(270, 80, 'Mặt Trăng', { a: 'middle' });
    b += arr(70, 32, 250, 32, 'rd1', RED) + arr(250, 58, 70, 58, 'rd2', BLUE, '7 4');
    b += T(150, 24, 'đi', { a: 'middle', c: RED }) + T(130, 82, 'về', { a: 'middle', c: BLUE });
    b += doan(36, 270, 104, 'd');
    return wrap('0 0 300 110', b, cap, 'Xung ra-đa đi tới Mặt Trăng rồi quay về');
  },
  // ===== Trang 7 · Dạng 6: vòng tròn pha (t tăng: điểm quay ngược chiều kim đồng hồ), điểm lúc t = 0 ở pha π/3 =====
  vongPha: (cap = '') => {
    const cx = 90, cy = 64, r = 48, a = Math.PI / 3, mx = cx + r * Math.cos(a), my = cy - r * Math.sin(a);
    let b = defs('vp');
    b += circ(cx, cy, r, { w: 2.4 }) + ln(cx - r - 14, cy, cx + r + 20, cy, GREY, 2) + ln(cx, cy - r - 10, cx, cy + r + 10, GREY, 2);
    b += T(cx + r + 24, cy + 7, `E/E${sb('0')}`) + T(cx + r + 4, cy + 26, '1') + T(cx - r - 4, cy + 26, km('−') + '1', { a: 'end' });
    b += ln(cx, cy, mx, my, INK, 2.4) + `<circle cx="${mx}" cy="${my}" r="6" fill="${RED}"/>` + T(mx + 10, my - 4, 't = 0', { c: RED, w: 700 });
    b += `<path d="M${cx + 26},${cy} A26,26 0 0 0 ${cx + 26 * Math.cos(a)},${cy - 26 * Math.sin(a)}" fill="none" stroke="${INK}" stroke-width="2"/>` + T(cx + 32, cy - 8, `${gk('π')}/3`);
    const R = r + 10, P = (d) => [cx + R * Math.cos(d * Math.PI / 180), cy - R * Math.sin(d * Math.PI / 180)];
    b += `<path d="M${P(200).join(',')} A${R},${R} 0 0 0 ${P(250).join(',')}" fill="none" stroke="${BLUE}" stroke-width="2.4" marker-end="url(#vp)"/>`;
    b += T(296, 116, 't tăng', { a: 'end', c: BLUE }) + T(296, 26, '(chiếu lên', { a: 'end' }) + T(296, 48, 'trục ngang)', { a: 'end' });
    return wrap('0 0 300 124', b, cap, 'Vòng tròn pha của điện trường');
  },
  // ===== Trang 8 · Bài tương tự Dạng 1: lõi sắt, cuộn dây, vòng dây kín =====
  loiSat: (cap = 'Vòng dây kín quanh lõi sắt.') => {
    let b = rect(132, 10, 36, 140, { rx: 2, fill: '#e3e8f3' }) + T(176, 26, 'lõi sắt');
    for (let i = 0; i < 5; i++) b += `<ellipse cx="150" cy="${88 + i * 13}" rx="30" ry="6" fill="none" stroke="${INK}" stroke-width="2.4"/>`;
    b += pl([[120, 88], [60, 88], [60, 104]]) + pl([[120, 140], [60, 140], [60, 130]]) + rect(42, 104, 36, 26, { rx: 3 }) + T(60, 124, '~', { a: 'middle', w: 700, size: 24 });
    b += T(12, 78, 'nguồn');
    b += `<ellipse cx="150" cy="50" rx="44" ry="10" fill="none" stroke="${RED}" stroke-width="${SW}"/>` + T(198, 58, 'vòng dây', { c: RED });
    return wrap('0 0 300 156', b, cap, 'Lõi sắt có cuộn dây và vòng dây kín');
  },
  // ===== Trang 9 · Bài tương tự Dạng 5: ra-đa – máy bay =====
  mayBay: (cap = 'Xung ra-đa tới máy bay rồi phản xạ về.') => {
    let b = defs('mb1') + defs('mb2');
    b += `<path d="M14,96 Q34,60 66,58" fill="none" stroke="${INK}" stroke-width="${SW}"/>` + ln(40, 80, 40, 112) + ln(22, 112, 58, 112) + T(40, 136, 'ra-đa', { a: 'middle' });
    b += `<path d="M232,62 l52,0 l6,-6 l-6,12 l-52,0 z M250,62 l-12,-16 l10,0 l18,16 M250,68 l-12,16 l10,0 l18,-16" fill="#fff" stroke="${INK}" stroke-width="2.4"/>`;
    b += arr(70, 52, 222, 52, 'mb1', RED) + arr(222, 80, 70, 80, 'mb2', BLUE, '7 4');
    b += T(146, 42, 'đi', { a: 'middle', c: RED }) + T(146, 104, 'về', { a: 'middle', c: BLUE });
    return wrap('0 0 300 144', b, cap, 'Xung ra-đa tới máy bay rồi quay về');
  },
};
