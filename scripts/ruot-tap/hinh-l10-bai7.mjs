// Hình minh hoạ cho ruột tập VL10 · Bài 7 Đồ thị độ dịch chuyển – thời gian (lesson 52). Cùng quy tắc với hinh.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt đường bằng nét (liền – đứt – chấm) chứ không chỉ màu.
// Đồ thị có lưới đủ dày để ĐỌC số liệu (mỗi vạch lưới một bước, nhãn số cách 1–2 vạch). Chú thích không lộ đáp án ô Dự đoán.
// Xem thử: node scripts/ruot-tap/l10-bai7.mjs --hinh (chụp vào out/hinh-l10-bai7/).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
const it = (s) => `<tspan font-style="italic">${s}</tspan>`;
const so = (v) => String(+v.toFixed(4)).replace('.', ',').replace('-', '–');
const buoc = (a, b, s) => { const r = []; for (let i = 0; ; i++) { const v = +(a + i * s).toFixed(6); if (v > b + 1e-9) break; r.push(v); } return r; };
// số trong vòng tròn (thay ①②③: Source Sans 3 không có glyph, rơi về font hệ thống)
const vong = (x, y, s, c = INK) => `<circle cx="${x}" cy="${y}" r="13" fill="#fff" stroke="${c}" stroke-width="2"/>` + T(x, y + 7, s, { a: 'middle', w: 700, c });
const NET = { lien: '', dut: '9 6', cham: '2.5 5', gach: '12 5 3 5' };

// Đồ thị có lưới. t:[đầu, cuối, bước], d:[đầu, cuối, bước]; moiT/moiD: ghi số mỗi mấy vạch; so:false = không ghi số (đồ thị định tính).
// duong: [{ p: [[t,d],…], c, net, nhan: [t, d, chữ, dx, dy] }]; diem: [[t, d, chữ, dx, dy]]; them: SVG tuỳ ý (nhận X, Y).
const doThi = (o, cap = '') => {
  const { t: [t0, t1, dt], d: [d0, d1, dd], tl = 't (s)', dl = 'd (m)', moiT = 1, moiD = 1, so: coSo = true, luoi = true,
    duong = [], diem = [], them = () => '', w = 320, h = 230, label = 'Đồ thị độ dịch chuyển – thời gian', id = 'dt', ml = 48 } = o;
  const mr = 50, mt = 32, mb = coSo ? 30 : 14;
  const X = (v) => +(ml + ((v - t0) / (t1 - t0)) * (w - ml - mr)).toFixed(1);
  const Y = (v) => +(h - mb - ((v - d0) / (d1 - d0)) * (h - mt - mb)).toFixed(1);
  const y0 = Y(Math.min(Math.max(0, d0), d1));
  let b = defs(id);
  if (luoi) {
    buoc(t0, t1, dt).forEach((v) => { b += `<line x1="${X(v)}" y1="${Y(d0)}" x2="${X(v)}" y2="${Y(d1)}" stroke="${GREY}" stroke-width="1" opacity=".75"/>`; });
    buoc(d0, d1, dd).forEach((v) => { b += `<line x1="${X(t0)}" y1="${Y(v)}" x2="${X(t1)}" y2="${Y(v)}" stroke="${GREY}" stroke-width="1" opacity=".75"/>`; });
  }
  if (coSo) {
    buoc(t0, t1, dt).forEach((v, i) => { if (i % moiT === 0 && v !== 0) b += T(X(v), Y(d0) + 22, so(v), { a: 'middle' }); });
    buoc(d0, d1, dd).forEach((v, i) => { if (i % moiD === 0 && (v !== 0 || d0 < 0)) b += T(X(t0) - 6, Y(v) + 7, so(v), { a: 'end' }); });
    if (d0 >= 0) b += T(X(t0) - 6, y0 + 20, '0', { a: 'end' });
  }
  b += `<line x1="${X(t0)}" y1="${y0}" x2="${w - 8}" y2="${y0}" stroke="${INK}" stroke-width="2.4" marker-end="url(#${id})"/>`;
  b += `<line x1="${X(t0)}" y1="${Y(d0) + (coSo ? 0 : 4)}" x2="${X(t0)}" y2="8" stroke="${INK}" stroke-width="2.4" marker-end="url(#${id})"/>`;
  b += T(w - 4, y0 - 9, tl, { a: 'end' }) + T(X(t0) + 10, 22, dl);
  duong.forEach((g) => {
    b += `<polyline points="${g.p.map(([a, c]) => `${X(a)},${Y(c)}`).join(' ')}" fill="none" stroke="${g.c ?? INK}" stroke-width="${g.sw ?? 3.2}" stroke-linejoin="round"${g.net ? ` stroke-dasharray="${NET[g.net] ?? g.net}"` : ''}/>`;
    if (g.nhan) { const [a, c, s, dx = 0, dy = 0] = g.nhan; b += vong(X(a) + dx, Y(c) + dy, s, g.c ?? INK); }
  });
  diem.forEach(([a, c, s, dx = 6, dy = -8]) => { b += `<circle cx="${X(a)}" cy="${Y(c)}" r="4.5" fill="${INK}"/>` + (s ? T(X(a) + dx, Y(c) + dy, s, { w: 700 }) : ''); });
  b += them(X, Y);
  return wrap(`0 0 ${w} ${h}`, b, cap, label);
};

export const hinhL10b7 = {
  // Trang 1 · Dự đoán: đồ thị chuyến đi xe đạp, ba đoạn, không ghi số (định tính) — chú thích không nói đoạn ② là gì
  xeDap: (cap = 'Toạ độ x của bạn đi xe đạp theo thời gian t (gốc ở nhà bạn).') => doThi({
    t: [0, 10, 1], d: [0, 6, 1], so: false, luoi: false, tl: 't', dl: 'x', h: 190, ml: 20, id: 'xd',
    duong: [{ p: [[0, 0], [3.5, 4.8], [6, 4.8], [9.5, 1.2]], sw: 3.4 }],
    them: (X, Y) => vong(X(1.4), Y(3.2), '1') + vong(X(4.75), Y(5.75), '2') + vong(X(8.4), Y(3.6), '3'),
  }, cap),
  // Trang 1 · II.1: trượt băng đi 30 m rồi quay lại 10 m trên trục toạ độ
  truotBang: (cap = 'Đi 30 m theo chiều dương rồi quay lại 10 m.') => {
    let b = defs('tb1') + defs('tb2');
    const X = (v) => 20 + v * 8.2;
    b += `<line x1="10" y1="92" x2="310" y2="92" stroke="${INK}" stroke-width="2.4" marker-end="url(#tb1)"/>` + T(314, 80, 'x', { a: 'end' });
    [0, 10, 20, 30].forEach((v) => { b += `<line x1="${X(v)}" y1="86" x2="${X(v)}" y2="98" stroke="${INK}" stroke-width="2.4"/>` + T(X(v), 122, `${v}`, { a: 'middle' }); });
    b += `<line x1="${X(0)}" y1="40" x2="${X(30) - 2}" y2="40" stroke="${BLUE}" stroke-width="${SW}" marker-end="url(#tb2)"/>` + T(X(15), 30, 'đi 30 m', { a: 'middle', c: BLUE });
    b += `<line x1="${X(30)}" y1="66" x2="${X(20) + 2}" y2="66" stroke="${RED}" stroke-width="${SW}" stroke-dasharray="7 5" marker-end="url(#tb2)"/>` + T(X(20) - 6, 72, 'về 10 m', { a: 'end', c: RED });
    b += `<line x1="${X(30)}" y1="40" x2="${X(30)}" y2="66" stroke="${GREY}" stroke-width="1.6"/>`;
    b += T(X(0), 152, 'xuất phát', { a: 'start', size: 20 });
    return wrap('0 0 320 160', b, cap, 'Trượt băng đi rồi quay lại');
  },
  // Trang 2 · Thí nghiệm bọt khí: lưới trống để HS chấm 5 điểm (t; d) từ bảng
  luoiBotKhi: (cap = 'Chấm 5 điểm (t; d) từ bảng, kẻ một đường thẳng đi gần mọi điểm.') => doThi({
    t: [0, 10, 1], d: [0, 50, 5], moiT: 2, moiD: 2, dl: 'd (cm)', id: 'bk', h: 236,
  }, cap),
  // Trang 2 · II.4: bốn xe trên cùng đường thẳng (Hình 3 của web)
  bonXe: (cap = 'Bốn xe trên cùng một đường thẳng. Chấm tròn: chỗ đường 1 cắt đường 4.') => doThi({
    t: [0, 4, 0.5], d: [0, 14, 1], moiT: 2, moiD: 2, id: 'bx', h: 250,
    duong: [
      { p: [[0, 0], [3.5, 14]], nhan: [3.1, 12.4, '1', -24, 0] },
      { p: [[0, 0], [4, 4]], net: 'dut', c: BLUE, nhan: [3.4, 3.4, '2', 4, -22] },
      { p: [[0, 6], [4, 6]], net: 'gach', nhan: [3.4, 6, '3', 0, -20] },
      { p: [[0, 14], [4, 2]], net: 'cham', c: RED, sw: 3.6, nhan: [3.4, 3.8, '4', 18, 10] },
    ],
    diem: [[2, 8, '', 0, 0]],
  }, cap),
  // Trang 3 · Thí nghiệm đi bộ: hệ trục trống để HS phác đồ thị
  diBo: (cap = 'Phác đồ thị d–t của bạn đi bộ: ra 5 m, đứng 3 s, về nhanh.') => doThi({
    t: [0, 12, 1], d: [0, 6, 1], moiT: 2, id: 'db', h: 200, luoi: true,
  }, cap),
  // Trang 4 · Bài toán mẫu: xe đồ chơi O–A–B–C (Hình 4 của web)
  xeDoChoi: (cap = 'Xe đồ chơi; chiều dương từ vạch mốc ra cọc cờ.') => doThi({
    t: [0, 10, 1], d: [0, 10, 1], moiT: 2, moiD: 2, id: 'xc', h: 236,
    duong: [{ p: [[0, 0], [4, 8], [6, 8], [10, 0]] }],
    diem: [[0, 0, 'O', 8, 22], [4, 8, 'A', -8, -10], [6, 8, 'B', 2, -10], [10, 0, 'C', -26, -12]],
  }, cap),
  // ---- Bài tập mẫu (trang 6–7) ----
  d1: (cap = '') => doThi({
    t: [0, 10, 1], d: [-1, 5, 1], moiT: 2, id: 'g1', h: 206,
    duong: [{ p: [[0, 0], [2, 4], [4, 4], [9, -1], [10, -1]] }],
  }, cap),
  d2: (cap = '') => doThi({
    t: [0, 50, 5], d: [0, 25, 5], moiT: 2, id: 'g2', h: 200,
    duong: [{ p: [[0, 0], [10, 20], [20, 20], [50, 5]] }],
  }, cap),
  d3: (cap = '') => doThi({
    t: [0, 2.5, 0.5], d: [0, 150, 25], moiD: 2, tl: 't (h)', dl: 'x (km)', id: 'g3', h: 210, ml: 52,
    duong: [{ p: [[0, 0], [2.5, 100]], nhan: [2.1, 84, 'I', -6, -26] }, { p: [[0, 150], [2.5, 0]], net: 'dut', c: BLUE, nhan: [1.6, 54, 'II', 16, 4] }],
  }, cap),
  d4: (cap = 'Vẽ hai đường vào hệ trục này.') => doThi({
    t: [0, 2, 0.25], d: [0, 10, 1], moiT: 2, moiD: 2, tl: 't (h)', dl: 'x (km)', id: 'g4', h: 200,
  }, cap),
  // ---- Bài tương tự (trang 8–9) ----
  tt1a: (cap = '') => doThi({
    t: [0, 10, 1], d: [-2, 6, 1], moiT: 2, id: 't1', h: 236,
    duong: [{ p: [[0, 0], [3, 6], [5, 6], [9, -2], [10, -2]] }],
  }, cap),
  tt1b: (cap = '') => doThi({
    t: [0, 12, 1], d: [0, 10, 1], moiT: 2, moiD: 2, id: 't2', h: 236,
    duong: [{ p: [[0, 2], [2, 2], [6, 10], [8, 10], [12, 4]] }],
  }, cap),
  tt2a: (cap = '') => doThi({
    t: [0, 25, 2.5], d: [0, 15, 3], moiT: 2, id: 't3', h: 220,
    duong: [{ p: [[0, 0], [5, 15], [10, 15], [25, 0]] }],
  }, cap),
  tt2b: (cap = '') => doThi({
    t: [0, 40, 5], d: [0, 50, 10], moiT: 2, id: 't4', h: 220,
    duong: [{ p: [[0, 10], [10, 10], [30, 50], [40, 30]] }],
  }, cap),
  tt3a: (cap = '') => doThi({
    t: [0, 3, 0.5], d: [0, 180, 30], tl: 't (h)', dl: 'x (km)', id: 't5', h: 186, ml: 52,
    duong: [{ p: [[0, 0], [3, 180]], nhan: [2.6, 156, 'I', -26, 0] }, { p: [[0, 180], [2, 0]], net: 'dut', c: BLUE, nhan: [1.75, 22, 'II', 22, -4] }],
  }, cap),
  tt3b: (cap = '') => doThi({
    t: [0, 3, 0.5], d: [0, 150, 30], tl: 't (h)', dl: 'x (km)', id: 't6', h: 186, ml: 52,
    duong: [{ p: [[0, 0], [3, 150]], nhan: [2.5, 125, 'I', -26, -4] }, { p: [[0, 60], [3, 120]], net: 'dut', c: BLUE, nhan: [2.5, 110, 'II', 4, 26] }],
  }, cap),
};
