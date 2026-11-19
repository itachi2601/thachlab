// Hình minh hoạ cho ruột tập VL10 · Bài 13 Tổng hợp và phân tích lực. Cân bằng lực (lesson 58). Cùng quy tắc với hinh.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh; hình không vẽ đúng tỉ lệ ở chỗ HS phải tính (đòn gánh, dây võng).
// Ảnh thật duy nhất: hai ngựa kéo cày (book/assets/anh-that, Wikimedia CC0). Xem thử: node scripts/ruot-tap/l10-bai13.mjs --hinh
import { dirname, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { ve } from './hinh.mjs';
const nw = (s) => `<span style="white-space:nowrap">${s}</span>`;
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const ANH = resolve(dirname(fileURLToPath(import.meta.url)), '../../book/assets/anh-that');
// K: hệ số phóng chữ cho hình in hẹp (cột 32–36 mm ở trang Bài tập mẫu) để chữ vẫn ≥ 7 pt
let K = 1;
const to = (k, fn) => { K = k; try { return fn(); } finally { K = 1; } };
const T = (x, y, s, o = {}) => t(x, y, s, { ...o, size: (o.size ?? 20) * K });
// chữ Hi Lạp: Source Sans 3 chỉ nạp latin/vietnamese, α θ rơi về Helvetica → lấy từ KaTeX_Math (đã nạp qua katex.min.css)
const gc = (ch) => `<span style="font-family:KaTeX_Math;font-style:italic">${ch}</span>`; // chữ Hi Lạp trong chú thích HTML
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const sb = (s) => `<tspan font-size="${15 * K}" dy="${5 * K}">${s}</tspan><tspan dy="${-5 * K}"> </tspan>`;
const arr = (x1, y1, x2, y2, id, c = INK, dash = '') =>
  `<line x1="${f1(x1)}" y1="${f1(y1)}" x2="${f1(x2)}" y2="${f1(y2)}" stroke="${c}" stroke-width="${SW}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${f1(x1)}" y1="${f1(y1)}" x2="${f1(x2)}" y2="${f1(y2)}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const R = (d) => (d * Math.PI) / 180;
const f1 = (v) => Number(v).toFixed(1);
// cung góc tâm (x,y), bán kính r, từ góc a1 tới a2 (độ, chiều toán học; y SVG hướng xuống nên đổi dấu)
const cung = (x, y, r, a1, a2, c = INK) => {
  const p = (a) => `${f1(x + r * Math.cos(R(a)))},${f1(y - r * Math.sin(R(a)))}`;
  return `<path d="M${p(a1)} A${r},${r} 0 0 0 ${p(a2)}" fill="none" stroke="${c}" stroke-width="2.2"/>`;
};
const dat = (x1, x2, y) => ln(x1, y, x2, y) + Array.from({ length: Math.floor((x2 - x1) / 18) }, (_, i) =>
  ln(x1 + 8 + i * 18, y, x1 + i * 18, y + 8, GREY, 1.8)).join('');
const tran = (x1, x2, y) => ln(x1, y, x2, y) + Array.from({ length: Math.floor((x2 - x1) / 18) }, (_, i) =>
  ln(x1 + i * 18, y, x1 + 8 + i * 18, y - 8, GREY, 1.8)).join('');
const hop = (x, y, w, h) => `<rect x="${f1(x)}" y="${f1(y)}" width="${w}" height="${h}" rx="3" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
// điểm cuối của vectơ từ (x,y), dài L, góc a (độ, chiều toán học)
const dau = (x, y, L, a) => [x + L * Math.cos(R(a)), y - L * Math.sin(R(a))];

// Thùng trên sàn, dây chếch góc goc; tách F thành Fx (ngang), Fy (đứng) bằng nét đứt
const keoChech = (cap, { goc = 35, nhan = gk('α'), F = 'F', id = 'kc' } = {}) => {
  let b = defs(id + 'a') + defs(id + 'b');
  b += dat(10, 312, 150) + hop(40, 106, 90, 44);
  const x0 = 130, y0 = 118, [xe, ye] = dau(x0, y0, 150, goc);
  b += arr(x0, y0, xe, ye, id + 'a', RED) + T(xe + 8, ye + 14, F, { c: RED, w: 700 });
  b += arr(x0, y0, xe, y0, id + 'b', BLUE, '7 5') + T(xe + 8, y0 + 8, `F${sb('x')}`, { c: BLUE });
  b += arr(x0, y0, x0, ye, id + 'b', BLUE, '7 5') + T(x0 - 8, ye + 14, `F${sb('y')}`, { c: BLUE, a: 'end' });
  b += ln(xe, ye, xe, y0, GREY, 1.8, '3 3') + ln(xe, ye, x0, ye, GREY, 1.8, '3 3');
  b += cung(x0, y0, 40, 0, goc) + T(x0 + 46, y0 - 8, nhan);
  return wrap('0 0 320 162', b, cap, 'Lực kéo chếch tách thành hai thành phần');
};

// Vật trên dốc nghiêng goc: P tách thành Px (dọc dốc) và Py (vuông góc dốc)
const docP = (cap, { goc = 30, nhan = gk('α'), id = 'dp', lucKe = false } = {}) => {
  let b = defs(id + 'a') + defs(id + 'b');
  const x0 = 14, y0 = 196, L = 292, c = Math.cos(R(goc)), s = Math.sin(R(goc));
  const x1 = x0 + L * c, y1 = y0 - L * s;
  b += `<path d="M${x0},${y0} L${f1(x1)},${f1(y1)} L${f1(x1)},${y0} z" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
  b += cung(x0, y0, 46, 0, goc) + T(x0 + 54, y0 - 8, nhan);
  const u = 0.5, bx = x0 + L * u * c, by = y0 - L * u * s, w = 50, hh = 30;
  b += `<g transform="rotate(${-goc} ${f1(bx)} ${f1(by)})">${hop(bx - w / 2, by - hh, w, hh)}</g>`;
  const cx = bx - (hh / 2) * s, cy = by - (hh / 2) * c; // tâm vật
  const Lp = 92, py = cy + Lp;
  // thành phần: Px dọc dốc hướng xuống (độ dài Lp·sin), Py vuông góc dốc hướng vào dốc (Lp·cos)
  const Px = [cx - Lp * s * c, cy + Lp * s * s], Py = [cx + Lp * c * s, cy + Lp * c * c];
  b += ln(Px[0], Px[1], cx, py, GREY, 1.8, '3 3') + ln(Py[0], Py[1], cx, py, GREY, 1.8, '3 3');
  b += arr(cx, cy, cx, py, id + 'a', RED) + T(cx - 5, cy + 64, 'P', { c: RED, w: 700, a: 'end' });
  b += arr(cx, cy, Px[0], Px[1], id + 'b', BLUE, '7 5') + T(Px[0] - 6, Px[1] + 8, `P${sb('x')}`, { c: BLUE, a: 'end' });
  b += arr(cx, cy, Py[0], Py[1], id + 'b', BLUE, '7 5') + T(Py[0] + 8, Py[1] + 6, `P${sb('y')}`, { c: BLUE });
  // góc giữa P và Py
  b += cung(cx, cy, 34, -90, -90 + goc) + T(cx + 12, cy + 58, gk('α'), { size: 18 });
  if (lucKe) { // lực kế song song dốc, móc vào mép trên vật, kéo lên dốc
    const sx = cx + (w / 2) * c, sy = cy - (w / 2) * s;
    b += ln(sx, sy, sx + 14 * c, sy - 14 * s, INK, 2.2);
    b += `<g transform="rotate(${-goc} ${f1(sx + 14 * c)} ${f1(sy - 14 * s)})"><rect x="${f1(sx + 14 * c)}" y="${f1(sy - 14 * s - 7)}" width="56" height="14" rx="3" fill="#fff" stroke="${INK}" stroke-width="2.2"/></g>`;
  }
  return wrap('0 0 320 206', b, cap, 'Trọng lực trên dốc tách thành hai thành phần');
};

export const hinhL10b13 = {
  // Tr.1 · Dự đoán: nhìn từ trên xuống, hai dây kéo xe hợp góc α (không vẽ hợp lực)
  haiDay: (cap = `Nhìn từ trên xuống. Mỗi bạn kéo 100 N, hai dây hợp góc ${gc('α')}.`) => {
    let b = defs('hda');
    b += hop(16, 78, 70, 50) + T(51, 110, 'xe', { a: 'middle' });
    const x0 = 86, y0 = 103;
    b += ln(x0, y0, 288, 30) + ln(x0, y0, 288, 176);
    b += `<circle cx="300" cy="26" r="9" fill="#fff" stroke="${INK}" stroke-width="${SW}"/><circle cx="300" cy="180" r="9" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    const a1 = Math.atan2(73, 202) * 180 / Math.PI;
    b += arr(x0, y0, ...dau(x0, y0, 108, a1), 'hda', RED) + T(150, 56, '100 N', { c: RED, w: 700 });
    b += arr(x0, y0, ...dau(x0, y0, 108, -a1), 'hda', RED) + T(150, 170, '100 N', { c: RED, w: 700 });
    b += cung(x0, y0, 40, -a1, a1) + T(x0 + 48, y0 + 7, gk('α'));
    return wrap('0 0 320 194', b, cap, 'Hai dây kéo xe hợp góc alpha');
  },
  // Tr.1 · Thí nghiệm ba lực kế và vòng nhẫn
  vongNhan: (cap = `Kéo lực kế 1, 2 hợp góc ${gc('α')}; lực kế 3 giữ vòng nằm yên.`) => {
    let b = '';
    const x0 = 160, y0 = 96, lk = (a, n, lx, ly) => {
      const [x, y] = dau(x0, y0, 70, a);
      return ln(x0, y0, x, y) + `<g transform="rotate(${-a} ${f1(x)} ${f1(y)})"><rect x="${f1(x)}" y="${f1(y - 9)}" width="58" height="18" rx="3" fill="#fff" stroke="${INK}" stroke-width="2.4"/></g>`
        + T(lx, ly, n, { w: 700 });
    };
    b += lk(150, '1', 30, 22) + lk(30, '2', 280, 22) + lk(270, '3', 176, 224);
    b += `<circle cx="${x0}" cy="${y0}" r="10" fill="#fff" stroke="${RED}" stroke-width="${SW}"/>`;
    b += cung(x0, y0, 34, 30, 150) + T(x0, y0 - 42, gk('α'), { a: 'middle' });
    return wrap('0 0 320 236', b, cap, 'Vòng nhẫn nối ba lực kế');
  },
  // Tr.2 · Ảnh thật: hai ngựa kéo cày (Wikimedia Commons, CC0)
  ngua: (cap = `Hai con ngựa cùng kéo một máy cày. Ảnh: State Government Photographer · Wikimedia Commons · CC0`) =>
    `<figure class="fig"><img src="${pathToFileURL(resolve(ANH, 'hai-ngua-keo-cay.jpg')).href}" alt="Hai con ngựa kéo cày" style="display:block;width:100%;height:auto">${cap ? `<figcaption>${cap}</figcaption>` : ''}</figure>`,
  // Tr.2 · Quy tắc hình bình hành
  hbh: (cap = `Dựng hình bình hành từ hai lực chung gốc O.`) => {
    let b = defs('hba') + defs('hbb');
    const O = [24, 168], F1 = [190, 0], a = 55, L2 = 120, F2 = [L2 * Math.cos(R(a)), -L2 * Math.sin(R(a))];
    const P1 = [O[0] + F1[0], O[1]], P2 = [O[0] + F2[0], O[1] + F2[1]], P = [P1[0] + F2[0], P1[1] + F2[1]];
    b += ln(P1[0], P1[1], P[0], P[1], GREY, 2, '5 4') + ln(P2[0], P2[1], P[0], P[1], GREY, 2, '5 4');
    b += arr(O[0], O[1], P1[0], P1[1], 'hba', RED) + T(P1[0] - 30, O[1] + 24, `F${sb('1')}`, { c: RED, w: 700 });
    b += arr(O[0], O[1], P2[0], P2[1], 'hba', RED) + T(P2[0] - 30, P2[1] + 4, `F${sb('2')}`, { c: RED, w: 700 });
    b += arr(O[0], O[1], P[0], P[1], 'hbb', BLUE, '9 5') + T(P[0] - 4, P[1] - 8, 'F', { c: BLUE, w: 700, a: 'end' });
    b += cung(O[0], O[1], 30, 0, a) + T(O[0] + 36, O[1] - 12, gk('α')) + T(O[0] - 6, O[1] + 22, 'O', { a: 'middle' });
    return wrap('0 0 320 196', b, cap, 'Quy tắc hình bình hành');
  },
  // Tr.3 · Đòn gánh: vai đặt ở đâu? (vai vẽ ở giữa, có dấu ? — không vẽ đúng tỉ lệ để khỏi lộ đáp số)
  donGanh: (cap = `Đòn dài 1 m, hai thùng ${nw('30 N')} và ${nw('20 N')}. Vai đặt ở đâu?`) => {
    let b = defs('dga');
    b += `<rect x="20" y="50" width="280" height="10" rx="4" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += ln(30, 60, 30, 92) + hop(4, 92, 52, 40) + T(30, 120, '30 N', { a: 'middle', size: 18, w: 700 });
    b += ln(290, 60, 290, 92) + hop(264, 92, 52, 40) + T(290, 120, '20 N', { a: 'middle', size: 18, w: 700 });
    b += `<path d="M160,62 L146,92 L174,92 z" fill="#fff" stroke="${RED}" stroke-width="${SW}"/>` + T(160, 118, 'vai ?', { a: 'middle', c: RED, w: 700 });
    b += ln(30, 26, 30, 40, GREY, 2) + ln(160, 26, 160, 40, GREY, 2) + ln(290, 26, 290, 40, GREY, 2);
    b += ln(34, 33, 156, 33, GREY, 2) + ln(164, 33, 286, 33, GREY, 2) + T(95, 22, `d${sb('1')}`, { a: 'middle' }) + T(225, 22, `d${sb('2')}`, { a: 'middle' });
    return wrap('0 0 320 134', b, cap, 'Đòn gánh hai thùng');
  },
  // Tr.3 · Phân tích lực kéo chếch
  keo: (cap = `Dây chếch lên: thành phần nào kéo thùng tiến, thành phần nào nhấc bớt thùng?`) => keoChech(cap, { id: 'kk' }),
  // Tr.3 · Thí nghiệm mặt phẳng nghiêng
  docTN: (cap = `Lực kế song song ván giữ vật P = 2,0 N đứng yên.`) => docP(cap, { id: 'dtn', lucKe: true }),
  // Tr.4 · Bẫy 3: góc giữa P và Py bằng góc nghiêng
  docBay: (cap = `Góc giữa P và P<sub>y</sub> bằng góc nghiêng ${gc('α')}. P<sub>x</sub> kề hay đối góc ấy?`) => docP(cap, { id: 'dby' }),
  // Tr.5 · Bài toán mẫu 2: đèn treo hai dây đối xứng
  den: (cap = `Đèn đứng yên: hợp lực của T<sub>1</sub>, T<sub>2</sub> cân bằng với P.`) => {
    let b = defs('dna') + defs('dnb');
    b += tran(30, 290, 22);
    const J = [160, 120];
    b += ln(J[0], J[1], 90, 22) + ln(J[0], J[1], 230, 22);
    const a = Math.atan2(98, 70) * 180 / Math.PI; // góc của dây so với phương ngang
    b += arr(J[0], J[1], ...dau(J[0], J[1], 64, 180 - a), 'dna', RED) + T(108, 92, `T${sb('1')}`, { c: RED, w: 700, a: 'end' });
    b += arr(J[0], J[1], ...dau(J[0], J[1], 64, a), 'dna', RED) + T(212, 92, `T${sb('2')}`, { c: RED, w: 700 });
    b += ln(J[0], J[1], J[0], 146) + `<path d="M140,146 L180,146 L192,170 L128,170 z" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += arr(J[0], 160, J[0], 214, 'dnb', RED) + T(J[0] + 8, 212, 'P', { c: RED, w: 700 });
    b += cung(J[0], J[1], 30, a, 180 - a) + T(J[0], J[1] - 36, gk('α'), { a: 'middle' });
    return wrap('0 0 320 222', b, cap, 'Đèn treo bằng hai dây đối xứng');
  },
  // Tr.7 · Dạng 3: kéo thùng 45 N chếch 40°
  keoD3: (cap = `F = 45 N, dây chếch 40°.`) => to(1.3, () => keoChech(cap, { goc: 40, nhan: '40°', id: 'kd3' })),
  // Tr.7 · Dạng 4: thùng trên dốc 40°
  docD4: (cap = `Thùng 8,0 kg trên dốc 40°.`) => to(1.3, () => docP(cap, { goc: 40, nhan: '40°', id: 'dd4' })),
  // Tr.7 · Dạng 5: vòng O, dây OA ngang, OB lệch 30° so với phương thẳng đứng
  oab: (cap = `Vòng O đứng yên dưới ba lực.`, k = 1) => to(k, () => {
    let b = defs('oaa');
    b += ln(16, 16, 16, 200) + Array.from({ length: 10 }, (_, i) => ln(16, 24 + i * 18, 8, 32 + i * 18, GREY, 1.8)).join('');
    b += tran(16, 310, 16);
    const O = [170, 118], B = [170 + 102 * Math.tan(R(30)), 16];
    b += ln(16, O[1], O[0], O[1]) + T(30, O[1] - 8, 'A') + ln(O[0], O[1], B[0], B[1]) + T(B[0] + 8, 40, 'B');
    b += ln(O[0], O[1], O[0], 30, GREY, 2, '5 4') + cung(O[0], O[1], 46, 60, 90) + T(O[0] + 8, O[1] - 52, '30°', { size: 18 });
    b += `<circle cx="${O[0]}" cy="${O[1]}" r="7" fill="#fff" stroke="${RED}" stroke-width="${SW}"/>` + T(O[0] - 10, O[1] + 26, 'O', { a: 'end' });
    b += ln(O[0], O[1] + 7, O[0], 160) + hop(146, 160, 48, 34) + T(O[0] + 30, 186, '3,0 kg', { size: 18 });
    return wrap('0 0 320 206', b, cap, 'Vòng nhẫn treo bằng dây ngang OA và dây xiên OB');
  }),
  // Tr.7 · Dạng 6: dây võng (độ võng vẽ phóng to để nhìn rõ góc)
  vong: (cap = `Độ võng vẽ phóng to để dễ nhìn góc ${gc('θ')}.`, k = 1) => to(k, () => {
    let b = '';
    const A = [30, 56], B = [290, 56], M = [160, 102];
    b += `<rect x="22" y="44" width="16" height="130" fill="#fff" stroke="${INK}" stroke-width="2.4"/><rect x="282" y="44" width="16" height="130" fill="#fff" stroke="${INK}" stroke-width="2.4"/>`;
    b += ln(A[0], A[1], B[0], B[1], GREY, 2, '5 4') + ln(A[0], A[1], M[0], M[1]) + ln(M[0], M[1], B[0], B[1]);
    b += T(A[0] - 6, A[1] - 16, 'A') + T(B[0] - 8, B[1] - 16, 'B');
    b += ln(M[0], A[1], M[0], M[1], RED, 2) + T(M[0] + 8, 78, 'h', { c: RED, w: 700 });
    const a = Math.atan2(M[1] - A[1], M[0] - A[0]) * 180 / Math.PI;
    b += cung(A[0], A[1], 58, -a, 0) + T(A[0] + 64, A[1] + 22, gk('θ'));
    b += ln(M[0], M[1], M[0], 116) + `<path d="M144,116 L176,116 L186,138 L134,138 z" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += ln(A[0], 184, B[0], 184, GREY, 2) + ln(A[0], 176, A[0], 192, GREY, 2) + ln(B[0], 176, B[0], 192, GREY, 2) + T(160, 176, 'AB', { a: 'middle' });
    return wrap('0 0 320 196', b, cap, 'Dây điện võng giữa hai cột, đèn treo ở giữa');
  }),
};
