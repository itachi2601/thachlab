// Hình minh hoạ cho ruột tập VL11 · Bài 22 Cường độ dòng điện (lesson 41). Cùng quy tắc với hinh.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh. Xem thử: node scripts/ruot-tap/l11-bai22.mjs --hinh (chụp vào out/hinh-l11-bai22/).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
const gk = (ch) => `<tspan font-family="KaTeX_Main">${ch}</tspan>`;
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const arr = (x1, y1, x2, y2, id, c = INK, dash = '', w = SW) =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const pl = (pts, c = INK, w = SW, dash = '') => `<polyline points="${pts}" fill="none" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''} stroke-linejoin="round"/>`;
// Ký hiệu mạch (nằm ngang, tâm x,y): pin (vạch dài = cực +), đèn (vòng tròn chữ X), ampe kế (vòng tròn chữ A), ô trống "?"
const pin = (x, y, nhan = true) => `<rect x="${x - 10}" y="${y - 20}" width="20" height="40" fill="#fff"/>` + ln(x - 6, y - 18, x - 6, y + 18) + ln(x + 6, y - 10, x + 6, y + 10, INK, 5)
  + (nhan ? T(x - 14, y - 22, '+', { a: 'middle', w: 700 }) + T(x + 16, y - 22, '−', { a: 'middle', w: 700 }) : '');
const den = (x, y, r = 15) => `<circle cx="${x}" cy="${y}" r="${r}" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
  + ln(x - r * .7, y - r * .7, x + r * .7, y + r * .7, INK, 2.2) + ln(x - r * .7, y + r * .7, x + r * .7, y - r * .7, INK, 2.2);
const ampe = (x, y, s = 'A', r = 16) => `<circle cx="${x}" cy="${y}" r="${r}" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(x, y + 7, s, { a: 'middle', w: 700, size: 21 });
const oTrong = (x, y) => `<rect x="${x - 15}" y="${y - 15}" width="30" height="30" rx="4" fill="#fff" stroke="${GREY}" stroke-width="2.2" stroke-dasharray="5 4"/>` + T(x, y + 7, '?', { a: 'middle', w: 700, c: GREY });
const eDot = (x, y) => `<circle cx="${x}" cy="${y}" r="6" fill="#fff" stroke="${BLUE}" stroke-width="2.2"/>` + ln(x - 3, y, x + 3, y, BLUE, 2);
// Dây dẫn hình trụ nằm ngang: tâm trục y, từ x1 tới x2, bán kính elip ry
const tru = (x1, x2, y, ry, rx = 12) => `<path d="M${x1},${y - ry} L${x2},${y - ry} M${x1},${y + ry} L${x2},${y + ry}" stroke="${INK}" stroke-width="${SW}" fill="none"/>`
  + `<ellipse cx="${x1}" cy="${y}" rx="${rx}" ry="${ry}" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
  + `<path d="M${x2},${y - ry} A${rx},${ry} 0 0 1 ${x2},${y + ry}" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;

export const hinhL11b22 = {
  // ===== Trang 1 · Dự đoán: công tắc – 5 m dây – đèn =====
  congTac: (cap = 'Bật công tắc: đèn cách 5 m sáng gần như tức thì.') => {
    let b = defs('ct1');
    b += ln(20, 60, 96, 60) + `<circle cx="100" cy="60" r="4" fill="${INK}"/>` + ln(100, 60, 132, 40) + `<circle cx="136" cy="60" r="4" fill="${INK}"/>`;
    b += T(116, 92, 'công tắc', { a: 'middle' });
    b += ln(136, 60, 266, 60) + den(282, 60) + ln(297, 60, 312, 60);
    b += ln(140, 126, 262, 126, GREY, 2) + ln(140, 118, 140, 134, GREY, 2) + ln(262, 118, 262, 134, GREY, 2) + T(201, 118, '5 m', { a: 'middle' });
    b += eDot(170, 60) + eDot(200, 60) + eDot(230, 60);
    b += arr(150, 160, 114, 160, 'ct1', BLUE, '6 4', 2.4) + T(158, 166, `electron: v = ?`, { c: BLUE, w: 700 });
    return wrap('0 0 320 180', b, cap, 'Công tắc nối với đèn bằng dây dài 5 m');
  },
  // ===== Trang 2 · ampe kế trong mạch pin – đèn =====
  mach: (cap = 'Mạch pin – đèn – ampe kế. Mũi tên: chiều dòng điện quy ước.') => {
    let b = defs('m1');
    b += pl('60,40 60,30 260,30 260,150 60,150 60,40') + `<rect x="40" y="70" width="40" height="40" fill="#fff"/>`;
    b += `<g transform="rotate(90 60 90)">${pin(60, 90, false)}</g>` + T(36, 70, '+', { a: 'middle', w: 700 }) + T(36, 122, '−', { a: 'middle', w: 700 });
    b += ampe(160, 30) + den(260, 90);
    b += arr(84, 30, 124, 30, 'm1', RED) + arr(260, 128, 260, 140, 'm1', RED) + arr(220, 150, 180, 150, 'm1', RED);
    b += T(92, 180, 'pin 3 V', { a: 'middle' }) + T(226, 96, 'đèn', { a: 'end' });
    return wrap('0 0 300 190', b, cap, 'Mạch điện có ampe kế mắc trong mạch pin và đèn');
  },
  // ===== Trang 2 · khung đồ thị Δq theo t (học sinh tự chấm điểm) =====
  khungDoThi: (cap = 'Chấm 5 điểm từ bảng rồi nối lại.') => {
    const X0 = 62, Y0 = 186, sx = 4.4, sy = 0.034; // 50 phút → 220 đơn vị; 4500 C → 153 đơn vị
    let b = defs('kd1');
    for (let i = 1; i <= 5; i++) b += ln(X0 + i * 10 * sx, Y0, X0 + i * 10 * sx, Y0 - 4500 * sy, GREY, 1.2, '3 4') + T(X0 + i * 10 * sx, Y0 + 24, String(i * 10), { a: 'middle' });
    for (let k = 1; k <= 5; k++) b += ln(X0, Y0 - k * 900 * sy, X0 + 50 * sx, Y0 - k * 900 * sy, GREY, 1.2, '3 4') + T(X0 - 6, Y0 - k * 900 * sy + 7, String(k * 900), { a: 'end' });
    b += arr(X0, Y0, X0 + 50 * sx + 22, Y0, 'kd1') + arr(X0, Y0, X0, Y0 - 4500 * sy - 18, 'kd1');
    b += T(X0 + 10, 16, `${gk('Δ')}q (C)`, { w: 700 }) + T(X0 + 50 * sx + 20, Y0 - 14, 't (phút)', { a: 'end', w: 700 }) + T(X0 - 6, Y0 + 24, '0', { a: 'end' });
    return wrap('0 0 310 220', b, cap, 'Khung đồ thị điện lượng theo thời gian');
  },
  // ===== Trang 3 · hai đồ thị I(t) =====
  haiDong: (cap = 'Hai đồ thị I theo t: (a) và (b).') => {
    let b = defs('hd1') + defs('hd2');
    const truc = (x0, y0, id) => arr(x0, y0, x0 + 128, y0, id) + arr(x0, y0, x0, y0 - 104, id) + T(x0 + 12, y0 - 90, 'I', { w: 700 }) + T(x0 + 118, y0 + 24, 't', { a: 'end', w: 700 });
    b += truc(20, 130, 'hd1') + ln(20, 70, 136, 70, RED) + T(76, 162, '(a)', { a: 'middle', w: 700 });
    b += truc(172, 130, 'hd2');
    let d = `M172,130`;
    for (let k = 0; k < 4; k++) { const x = 172 + k * 29; d += ` Q${x + 14.5},${10} ${x + 29},130`; }
    b += `<path d="${d}" fill="none" stroke="${BLUE}" stroke-width="${SW}" stroke-dasharray="7 4"/>` + T(232, 162, '(b)', { a: 'middle', w: 700 });
    return wrap('0 0 310 172', b, cap, 'Hai đồ thị cường độ dòng điện theo thời gian');
  },
  // ===== Trang 3 · hình trụ hạt tải trôi qua tiết diện S =====
  hinhTru: (cap = 'Hạt tải trong trụ đáy S, dài vΔt sẽ qua tiết diện S trong thời gian Δt.') => {
    let b = defs('ht1');
    b += tru(30, 290, 80, 42);
    b += `<ellipse cx="200" cy="80" rx="12" ry="42" fill="none" stroke="${RED}" stroke-width="${SW}"/>` + T(200, 30, 'S', { c: RED, w: 700, a: 'middle' });
    b += `<ellipse cx="80" cy="80" rx="12" ry="42" fill="none" stroke="${GREY}" stroke-width="2" stroke-dasharray="5 4"/>`;
    [[100, 62], [124, 96], [146, 70], [168, 100], [180, 58], [112, 84], [158, 84]].forEach(([x, y]) => {
      b += `<circle cx="${x}" cy="${y}" r="7" fill="#fff" stroke="${INK}" stroke-width="2.2"/>` + ln(x - 4, y, x + 4, y, INK, 2) + ln(x, y - 4, x, y + 4, INK, 2);
    });
    b += arr(224, 80, 270, 80, 'ht1', INK) + T(250, 70, 'v', { w: 700, a: 'middle' });
    b += ln(80, 140, 200, 140, GREY, 2) + ln(80, 132, 80, 148, GREY, 2) + ln(200, 132, 200, 148, GREY, 2) + T(140, 168, `v${gk('Δ')}t`, { a: 'middle', w: 700 });
    return wrap('0 0 310 176', b, cap, 'Hình trụ chứa các hạt tải điện trôi qua tiết diện');
  },
  // ===== Trang 4 · bẫy 3: ampe kế mắc sai =====
  ampeSai: (cap = 'Hai cách mắc ampe kế: (1) và (2).') => {
    let b = '';
    // (1) song song với đèn
    b += pl('20,40 20,130 130,130 130,40 20,40') + `<rect x="0" y="66" width="40" height="40" fill="#fff"/>` + `<g transform="rotate(90 20 86)">${pin(20, 86, false)}</g>`;
    b += den(130, 86) + `<rect x="120" y="60" width="0" height="0"/>`;
    b += ln(130, 56, 166, 56) + ln(130, 116, 166, 116) + ln(166, 56, 166, 70) + ln(166, 102, 166, 116) + ampe(166, 86) ;
    b += T(84, 162, '(1)', { a: 'middle', w: 700 });
    // (2) nối tiếp
    b += pl('206,40 206,130 300,130 300,40 206,40') + `<rect x="186" y="66" width="40" height="40" fill="#fff"/>` + `<g transform="rotate(90 206 86)">${pin(206, 86, false)}</g>`;
    b += den(300, 86) + ampe(253, 40);
    b += T(253, 162, '(2)', { a: 'middle', w: 700 });
    return wrap('0 0 320 172', b, cap, 'Hai cách mắc ampe kế với đèn');
  },
  // ===== Trang 5 · bài toán mẫu cáp kích bình =====
  capKich: (cap = 'Bộ kích bình nối cáp đồng 25 mm² vào ắc quy ô tô.') => {
    let b = defs('ck1');
    b += `<rect x="14" y="40" width="100" height="70" rx="6" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(64, 82, 'bộ kích', { a: 'middle', w: 700 });
    b += `<rect x="200" y="56" width="104" height="70" rx="4" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(252, 98, 'ắc quy', { a: 'middle', w: 700 });
    b += `<rect x="216" y="44" width="16" height="12" fill="${INK}"/><rect x="272" y="44" width="16" height="12" fill="${INK}"/>`;
    b += `<path d="M90,40 C110,8 200,8 224,44" fill="none" stroke="${RED}" stroke-width="5"/>`;
    b += `<path d="M40,40 C60,-6 270,-6 280,44" fill="none" stroke="${INK}" stroke-width="5"/>`;
    b += T(64, 140, 'I = 120 A', { a: 'middle', w: 700 });
    return wrap('0 0 320 150', b, cap, 'Bộ kích bình nối cáp vào ắc quy');
  },
  // ===== Bài tập mẫu =====
  sacD1: (cap = 'Ampe kế đặt ở ô nào?') => {
    let b = defs('d1');
    b += pl('60,40 60,24 280,24 280,112 60,112 60,40') + `<rect x="40" y="48" width="40" height="40" fill="#fff"/>`;
    b += `<g transform="rotate(90 60 68)">${pin(60, 68, false)}</g>` + T(36, 50, '+', { a: 'middle', w: 700 }) + T(36, 100, '−', { a: 'middle', w: 700 });
    b += `<rect x="146" y="92" width="70" height="40" rx="4" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(181, 119, 'ắc quy', { a: 'middle', size: 20 });
    b += oTrong(180, 24) + oTrong(280, 68) + T(60, 134, 'nguồn sạc', { a: 'middle', size: 18 });
    b += arr(84, 24, 130, 24, 'd1', RED) + T(146, 18, 'I', { c: RED, w: 700, a: 'middle' });
    return wrap('0 0 310 142', b, cap, 'Mạch nạp ắc quy có hai chỗ có thể đặt ampe kế');
  },
  dayD4: (cap = 'Hai đoạn lõi đồng nối tiếp, cùng dòng I.') => {
    let b = tru(20, 160, 70, 40) + tru(160, 290, 70, 20, 7);
    b += T(90, 140, `S${sb('1')}= 2,5 mm²`, { a: 'middle' }) + T(226, 140, `S${sb('2')}= 1,0 mm²`, { a: 'middle' });
    b += T(90, 22, `v${sb('1')}`, { a: 'middle', w: 700 }) + T(226, 40, `v${sb('2')}`, { a: 'middle', w: 700 });
    return wrap('0 0 310 150', b, cap, 'Dây to nối tiếp dây nhỏ');
  },
  dayD5: (cap = 'Dây bếp từ: tiết diện S, trong Δt có Δq qua S.') => {
    let b = defs('d5') + tru(30, 280, 70, 34);
    b += `<ellipse cx="170" cy="70" rx="11" ry="34" fill="none" stroke="${RED}" stroke-width="${SW}"/>` + T(170, 26, 'S = 6,0 mm²', { c: RED, w: 700, a: 'middle' });
    b += arr(100, 136, 240, 136, 'd5', INK) + T(170, 128, 'I', { a: 'middle', w: 700 });
    return wrap('0 0 310 150', b, cap, 'Đoạn dây đồng có tiết diện S');
  },
};
