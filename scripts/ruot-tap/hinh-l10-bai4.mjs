// Hình minh hoạ cho ruột tập VL10 · Bài 4 Độ dịch chuyển và quãng đường đi được (lesson 49). Cùng quy tắc với hinh.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8; đường đi thật = nét đứt xanh, độ dịch chuyển = mũi tên đỏ.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh (độ dịch chuyển ghi "?"). Xem thử: node scripts/ruot-tap/l10-bai4.mjs --hinh
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const arr = (x1, y1, x2, y2, id, c = INK, dash = '', w = SW) =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const R = (d) => (d * Math.PI) / 180;
const f1 = (v) => (+v).toFixed(1);
const cung = (x, y, r, a1, a2, c = INK) => {
  const p = (a) => `${f1(x + r * Math.cos(R(a)))},${f1(y - r * Math.sin(R(a)))}`;
  return `<path d="M${p(a1)} A${r},${r} 0 0 0 ${p(a2)}" fill="none" stroke="${c}" stroke-width="2.2"/>`;
};
const cham = (x, y, dac = true) => `<circle cx="${x}" cy="${y}" r="6" fill="${dac ? INK : '#fff'}" stroke="${INK}" stroke-width="2.4"/>`;
// la bàn nhỏ: gốc (x,y), mũi Bắc lên, mũi Đông sang phải
const laBan = (x, y, id) => defs(id) + arr(x, y, x, y - 34, id, GREY, '', 2.4) + arr(x, y, x + 34, y, id, GREY, '', 2.4)
  + T(x, y - 40, 'B', { a: 'middle', c: GREY, w: 700 }) + T(x + 40, y + 7, 'Đ', { c: GREY, w: 700 });

export const hinhL10b4 = {
  // Trang 1 · Dự đoán: một vòng sân băng, xuất phát và dừng ở cửa
  sanBang: (cap = 'Trượt một vòng sát rào chắn rồi dừng ở cửa vào.') => {
    let b = defs('sb1');
    b += `<rect x="16" y="12" width="288" height="128" rx="62" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<rect x="142" y="134" width="36" height="12" fill="#fff"/>` + ln(142, 132, 142, 148) + ln(178, 132, 178, 148);
    b += `<rect x="36" y="30" width="248" height="92" rx="44" fill="none" stroke="${BLUE}" stroke-width="2.6" stroke-dasharray="7 5"/>`;
    b += arr(150, 30, 186, 30, 'sb1', BLUE, '', 2.6) + arr(176, 122, 140, 122, 'sb1', BLUE, '', 2.6);
    b += cham(160, 122);
    b += T(160, 72, 'Đồng hồ: đi 60 m', { a: 'middle', w: 700 }) + T(160, 98, '(số liệu minh hoạ)', { a: 'middle', c: GREY });
    b += T(160, 168, 'cửa vào', { a: 'middle' });
    return wrap('0 0 320 176', b, cap, 'Một vòng sân băng');
  },
  // Trang 2 · toạ độ có dấu trên trục Ox
  trucToaDo: (cap = 'Mỗi vạch 1 m. Toạ độ của M? Của N?') => {
    let b = defs('tt1');
    b += arr(10, 64, 312, 64, 'tt1') + T(306, 50, 'x', { a: 'end', w: 700 });
    for (let k = -2; k <= 4; k++) { const x = 110 + k * 40; b += ln(x, 58, x, 70, INK, 2.4); if (k === 0) b += T(x, 96, 'O', { a: 'middle', w: 700 }); }
    b += `<circle cx="230" cy="64" r="7" fill="${RED}"/>` + T(230, 44, 'M', { a: 'middle', c: RED, w: 700 });
    b += `<circle cx="30" cy="64" r="7" fill="${BLUE}"/>` + T(30, 44, 'N', { a: 'middle', c: BLUE, w: 700 });
    b += T(56, 100, 'phía âm', { a: 'middle', c: GREY }) + T(200, 100, 'phía dương', { a: 'middle', c: GREY });
    return wrap('0 0 320 110', b, cap, 'Trục toạ độ có hai điểm M và N');
  },
  // Trang 2 · ví dụ: xe điều khiển chạy tới rồi lùi dọc cây thước
  xeToiLui: (cap = 'Nét đứt: đường xe chạy. Mũi tên đặc: nối vị trí đầu với vị trí cuối.') => {
    const px = (cm) => 20 + cm * 2.8;
    let b = defs('xt1') + defs('xt2');
    b += ln(px(0), 120, px(100), 120);
    for (let c = 0; c <= 100; c += 10) b += ln(px(c), 114, px(c), 126, INK, 2);
    [0, 20, 40, 60, 80, 100].forEach((c) => { b += T(px(c), 148, String(c), { a: 'middle' }); });
    b += arr(px(20), 34, px(80), 34, 'xt1', BLUE, '7 5', 2.6) + ln(px(80), 34, px(80), 60, GREY, 2, '4 4') + arr(px(80), 60, px(50), 60, 'xt1', BLUE, '7 5', 2.6);
    b += ln(px(20), 34, px(20), 120, GREY, 2, '4 4') + ln(px(50), 60, px(50), 120, GREY, 2, '4 4');
    b += arr(px(20), 96, px(50), 96, 'xt2', RED) + T(px(35), 88, 'd = ?', { a: 'middle', c: RED, w: 700 });
    b += T(px(100), 112, 'cm', { a: 'end', c: GREY });
    return wrap('0 0 320 156', b, cap, 'Xe chạy tới rồi lùi dọc cây thước');
  },
  // Trang 3 · thí nghiệm: bốn hình ray
  rayUon: (cap = 'Vòng rỗng: điểm đầu; chấm đặc: điểm dừng của xe.') => {
    let b = '';
    const o = [0, 80, 160, 240];
    b += ln(o[0] + 10, 90, o[0] + 70, 90, BLUE, 4) + cham(o[0] + 10, 90, false) + cham(o[0] + 70, 90);
    b += `<path d="M${o[1] + 12},90 A28,28 0 0 1 ${o[1] + 68},90" fill="none" stroke="${BLUE}" stroke-width="4"/>` + cham(o[1] + 12, 90, false) + cham(o[1] + 68, 90);
    b += `<path d="M${o[2] + 14},40 L${o[2] + 14},90 L${o[2] + 70},90" fill="none" stroke="${BLUE}" stroke-width="4"/>` + cham(o[2] + 14, 40, false) + cham(o[2] + 70, 90);
    b += `<circle cx="${o[3] + 40}" cy="62" r="28" fill="none" stroke="${BLUE}" stroke-width="4"/>` + `<circle cx="${o[3] + 40}" cy="90" r="9" fill="#fff" stroke="${INK}" stroke-width="2.4"/>` + `<circle cx="${o[3] + 40}" cy="90" r="4" fill="${INK}"/>`;
    ['thẳng', 'nửa vòng', 'chữ L', 'trọn vòng'].forEach((s, i) => { b += T(o[i] + 40, 124, s, { a: 'middle' }); });
    return wrap('0 0 320 132', b, cap, 'Bốn hình ray: thẳng, nửa vòng, chữ L, trọn vòng');
  },
  // Trang 3 · Bẫy 3: hai đoạn vuông góc nối đuôi
  vuongGoc: (cap = 'Đi 3 m về Bắc rồi 4 m về Đông. Độ dịch chuyển là mũi tên nào?') => {
    let b = defs('vg1') + defs('vg2');
    b += arr(40, 146, 40, 56, 'vg1', BLUE, '7 5', 2.8) + arr(40, 56, 160, 56, 'vg1', BLUE, '7 5', 2.8);
    b += arr(40, 146, 158, 58, 'vg2', RED) + T(112, 118, '?', { c: RED, w: 700, size: 24 });
    b += T(32, 106, '3 m', { a: 'end' }) + T(100, 44, '4 m', { a: 'middle' }) + cham(40, 146, false);
    b += laBan(200, 140, 'vg3');
    return wrap('0 0 250 156', b, cap, 'Hai đoạn vuông góc');
  },
  // Trang 4 · bài toán mẫu: đạp xe từ nhà tới trường
  dapXe: (cap = 'Đường xanh nét đứt: đường đạp xe. Mũi tên đỏ: độ dịch chuyển, hợp với hướng Đông góc <span style="font-family:KaTeX_Math;font-style:italic">α</span>.') => {
    let b = defs('dx1') + defs('dx2');
    b += arr(24, 140, 240, 140, 'dx1', BLUE, '7 5', 2.8) + arr(244, 140, 244, 52, 'dx1', BLUE, '7 5', 2.8);
    b += arr(24, 140, 240, 50, 'dx2', RED) + T(118, 82, 'd', { c: RED, w: 700 });
    b += cung(24, 140, 50, 0, 22.6) + T(80, 134, gk('α'));
    b += cham(24, 140, false) + T(24, 166, 'Nhà', { a: 'middle', w: 700 }) + T(244, 166, 'ngã tư', { a: 'middle' }) + T(244, 34, 'Trường', { a: 'middle', w: 700 });
    b += T(134, 166, '1,2 km', { a: 'middle' }) + T(252, 102, '0,5 km');
    b += laBan(44, 46, 'dx3');
    return wrap('0 0 320 174', b, cap, 'Đường đạp xe từ nhà tới trường');
  },
  // Trang 5 · thử thách ⭐⭐: chạy 1,5 vòng sân tròn
  vongRuoi: (cap = 'Chạy 1,5 vòng từ chỗ xuất phát. Em dừng ở đâu?') => {
    let b = defs('vr1');
    b += `<circle cx="110" cy="80" r="62" fill="none" stroke="${INK}" stroke-width="${SW}"/>` + `<circle cx="110" cy="80" r="3" fill="${INK}"/>`;
    b += ln(110, 80, 172, 80, GREY, 2, '4 4') + T(141, 74, 'R', { a: 'middle', w: 700 });
    b += `<path d="M110,142 A50,50 0 0 1 60,92" fill="none" stroke="${BLUE}" stroke-width="2.6" stroke-dasharray="7 5" marker-end="url(#vr1)"/>`;
    b += cham(110, 142, false) + T(110, 166, 'xuất phát', { a: 'middle' });
    b += T(196, 40, 'R = 50 m');
    return wrap('0 0 280 172', b, cap, 'Sân chạy tròn');
  },
  // Bài tập mẫu D1: nhà A, tiệm C, bưu điện B trên một trục
  d1Truc: (cap = 'Đường xanh: A → B rồi quay về C.') => {
    const px = (m) => 30 + m * 0.33;
    let b = defs('d1a') + defs('d1b');
    b += arr(14, 96, 314, 96, 'd1a') + T(312, 84, 'x', { a: 'end', w: 700 });
    [[0, 'A', '0'], [300, 'C', '300'], [800, 'B', '800']].forEach(([m, n, v]) => { b += cham(px(m), 96) + T(px(m), 82, n, { a: 'middle', w: 700 }) + T(px(m), 122, v, { a: 'middle' }); });
    b += T(312, 122, '(m)', { a: 'end', c: GREY });
    b += arr(px(0), 26, px(800) - 2, 26, 'd1b', BLUE, '7 5', 2.6) + ln(px(800), 26, px(800), 50, GREY, 2, '4 4') + arr(px(800), 50, px(300) + 2, 50, 'd1b', BLUE, '7 5', 2.6);
    return wrap('0 0 320 130', b, cap, 'Ba điểm A, C, B trên một trục');
  },
  // Bài tập mẫu D2: toạ độ có dấu, đơn vị km
  d2Truc: (cap = 'Ox hướng Đông; toạ độ tính bằng km.') => {
    const px = (x) => 30 + (x + 4) * 16;
    let b = defs('d2a') + defs('d2b');
    b += arr(14, 96, 314, 96, 'd2a') + T(312, 84, 'x', { a: 'end', w: 700 });
    [[12, `x${sb('1')}`, '12'], [-3, `x${sb('2')}`, '−3'], [2, `x${sb('3')}`, '2'], [0, 'O', '0']].forEach(([x, n, v]) => { b += (x === 0 ? ln(px(x), 90, px(x), 102, INK, 2.4) : cham(px(x), 96)) + T(px(x), 82, n, { a: 'middle', w: 700 }) + T(px(x), 122, v, { a: 'middle' }); });
    b += arr(px(12), 26, px(-3) + 2, 26, 'd2b', BLUE, '7 5', 2.6) + ln(px(-3), 26, px(-3), 50, GREY, 2, '4 4') + arr(px(-3), 50, px(2) - 2, 50, 'd2b', BLUE, '7 5', 2.6);
    return wrap('0 0 320 130', b, cap, 'Xe tải chạy về Tây rồi quay về Đông');
  },
  // Bài tập mẫu D3: hai đoạn vuông góc 900 m Đông, 1200 m Bắc (tỉ lệ 0,07 đơn vị/m)
  d3VuongGoc: (cap = 'Độ dịch chuyển là cạnh nào?') => {
    let b = defs('d3a') + defs('d3b');
    b += arr(70, 82, 113, 82, 'd3a', BLUE, '6 4', 1.8) + arr(117, 82, 117, 25, 'd3a', BLUE, '6 4', 1.8);
    b += arr(70, 82, 114, 28, 'd3b', RED, '', 2.2) + T(78, 52, '?', { c: RED, w: 700, size: 24 });
    b += cung(70, 82, 26, 0, 51) + T(100, 77, gk('α'));
    b += T(92, 104, '900 m', { a: 'middle' }) + T(126, 58, '1200 m');
    b += T(60, 88, 'Nhà', { a: 'end', w: 700 }) + T(118, 18, 'Trường', { a: 'middle', w: 700 });
    b += laBan(240, 84, 'd3c');
    return wrap('0 0 300 108', b, cap, 'Đi Đông rồi rẽ Bắc');
  },
  // Bài tập mẫu D4: trục thời gian có đoạn nghỉ
  d4ThoiGian: (cap = 'Đoạn nghỉ có tính vào t không?') => {
    const px = (p) => 20 + p * 5.6;
    let b = '';
    b += ln(px(0), 56, px(20), 56, BLUE, 8) + ln(px(20), 56, px(30), 56, GREY, 8, '4 4') + ln(px(30), 56, px(50), 56, BLUE, 8);
    [0, 20, 30, 50].forEach((p) => { b += ln(px(p), 46, px(p), 66, INK, 2) + T(px(p), 90, String(p), { a: 'middle' }); });
    b += T(px(10), 36, '4 km', { a: 'middle', w: 700 }) + T(px(25), 36, 'nghỉ', { a: 'middle', c: GREY }) + T(px(40), 36, '2 km', { a: 'middle', w: 700 });
    b += T(px(50), 112, 'phút', { a: 'end', c: GREY });
    return wrap('0 0 320 118', b, cap, 'Trục thời gian của hành trình đạp xe');
  },
  // Bài tập mẫu D5: Đông, quay Tây, rẽ Bắc
  d5QuayRe: (cap = 'Đoạn quay đầu vẽ lệch cho dễ nhìn.') => {
    let b = defs('d5a') + defs('d5b');
    b += arr(24, 140, 204, 140, 'd5a', BLUE, '7 5', 2.8) + ln(206, 140, 206, 124, GREY, 2, '4 4') + arr(206, 124, 132, 124, 'd5a', BLUE, '7 5', 2.8) + arr(128, 124, 128, 50, 'd5a', BLUE, '7 5', 2.8);
    b += arr(24, 140, 126, 52, 'd5b', RED) + T(62, 88, '?', { c: RED, w: 700, size: 24 });
    b += cham(24, 140, false) + T(24, 166, 'O', { a: 'middle', w: 700 });
    b += T(116, 166, '7 m', { a: 'middle' }) + T(170, 116, '3 m', { a: 'middle' }) + T(136, 92, '3 m');
    b += laBan(246, 64, 'd5c');
    return wrap('0 0 300 174', b, cap, 'Xe mô hình: Đông, quay Tây, rẽ Bắc');
  },
};
