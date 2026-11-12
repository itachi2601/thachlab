// Hình minh hoạ cho ruột tập VL10 · Bài 32 Lực hướng tâm và gia tốc hướng tâm (lesson 77). Cùng quy tắc với hinh.mjs/hinh-l10-bai23.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh (hình khúc cua KHÔNG vẽ gia tốc; hình Δv để HS tự vẽ Δv).
// Xem thử: node scripts/ruot-tap/l10-bai32.mjs --hinh (chụp vào out/hinh-l10-bai32/).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
// chữ Hi Lạp: Source Sans 3 chỉ nạp latin/vietnamese, ω Δ rơi về Helvetica → lấy từ KaTeX_Math / KaTeX_Main
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const DL = '<tspan font-family="KaTeX_Main">Δ</tspan>';
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const f1 = (v) => (+v).toFixed(1);
const R = (d) => (d * Math.PI) / 180;
const arr = (x1, y1, x2, y2, id, c = INK, dash = '', w = SW) =>
  `<line x1="${f1(x1)}" y1="${f1(y1)}" x2="${f1(x2)}" y2="${f1(y2)}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${f1(x1)}" y1="${f1(y1)}" x2="${f1(x2)}" y2="${f1(y2)}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const ci = (x, y, r, { fill = '#fff', c = INK, w = SW, dash = '' } = {}) =>
  `<circle cx="${f1(x)}" cy="${f1(y)}" r="${r}" fill="${fill}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const dot = (x, y, r = 4, c = INK) => `<circle cx="${f1(x)}" cy="${f1(y)}" r="${r}" fill="${c}"/>`;
// cung tâm (x,y) bán kính r từ góc a1 tới a2 (độ, toán học, ngược chiều kim đồng hồ)
const cung = (x, y, r, a1, a2, { c = INK, w = 2.2, dash = '', mk = '' } = {}) => {
  const p = (a) => `${f1(x + r * Math.cos(R(a)))},${f1(y - r * Math.sin(R(a)))}`;
  const big = Math.abs(a2 - a1) > 180 ? 1 : 0;
  return `<path d="M${p(a1)} A${r},${r} 0 ${big} 0 ${p(a2)}" fill="none" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}${mk ? ` marker-end="url(#${mk})"` : ''}/>`;
};
const P = (x, y, r, a) => [x + r * Math.cos(R(a)), y - r * Math.sin(R(a))];

// Đĩa quay nhìn từ trên: tâm O, các điểm [{r (đơn vị vẽ), nhan, goc}], chú thích bán kính
const dia = (cap, diem, { id = 'dq', vat = false, nhanO = 'O', R0 = 92 } = {}) => {
  const x = 120, y = R0 + 18;
  let b = defs(id + 'a');
  b += ci(x, y, R0) + dot(x, y, 4.5) + T(x - 10, y + 24, nhanO, { a: 'end', w: 700 });
  b += cung(x, y, R0 + 14, 40, 100, { mk: id + 'a', w: 2.6 }) + T(x + 60, y - R0 + 2, gk('ω'), { size: 24 });
  diem.forEach(({ r, nhan, goc = -10, dai = '' }, i) => {
    const [px, py] = P(x, y, r, goc);
    b += ln(x, y, px, py, GREY, 2, '5 4');
    b += vat && i === 0 ? `<rect x="${f1(px - 9)}" y="${f1(py - 9)}" width="18" height="18" rx="3" fill="${GREY}" stroke="${INK}" stroke-width="${SW}"/>` : dot(px, py, 6);
    b += T(px + (vat ? 14 : 10), py - 10, nhan, { w: 700 });
    if (dai) b += T(px + 4, py + 30 + i * 0, dai, { size: 20 });
  });
  return wrap(`0 0 320 ${2 * R0 + 32}`, b, cap, 'Đĩa quay đều nhìn từ trên xuống');
};

export const hinhL10b32 = {
  // Trang 1 · Dự đoán: xe qua khúc cua, kim tốc độ đứng yên. KHÔNG vẽ gia tốc.
  khucCua: (cap = 'Kim tốc độ đứng yên ở 36 km/h suốt khúc cua.') => {
    let b = defs('kc1');
    const x = 40, y = 186;
    b += cung(x, y, 150, 0, 90, { w: SW }) + cung(x, y, 110, 0, 90, { w: SW });
    b += cung(x, y, 130, 0, 90, { c: GREY, w: 2, dash: '8 6' });
    b += dot(x, y, 4.5, GREY) + T(x + 6, y - 6, 'O', { c: GREY });
    [[72, 'v', '1'], [32, 'v', '2']].forEach(([a, v, k]) => {
      const [px, py] = P(x, y, 130, a);
      // xe là hình chữ nhật nhỏ xoay theo tiếp tuyến
      b += `<g transform="rotate(${-a} ${f1(px)} ${f1(py)})"><rect x="${f1(px - 10)}" y="${f1(py - 16)}" width="20" height="32" rx="4" fill="#fff" stroke="${INK}" stroke-width="${SW}"/></g>`;
      // HS ảo 12/11 (B2): bỏ mũi tên v1, v2 — hai vectơ vận tốc đổi hướng gợi sẵn đáp án C
    });
    return wrap('0 0 300 200', b, cap, 'Xe qua khúc cua với tốc độ không đổi');
  },
  // Trang 1 · II.1: dời v2 về chung gốc với v1, HS tự vẽ Δv
  deltaV: (cap = 'Bên phải: v<sub>1</sub>, v<sub>2</sub> dời về chung gốc. Em vẽ Δv = v<sub>2</sub> − v<sub>1</sub>.') => {
    let b = defs('dv1') + defs('dv2');
    const x = 88, y = 150, r = 74;
    b += ci(x, y, r) + dot(x, y, 4.5) + T(x - 6, y + 26, 'O', { a: 'end', w: 700 });
    const vv = [[118, 'B', '1'], [62, 'C', '2']];
    vv.forEach(([a, nh, k]) => {
      const [px, py] = P(x, y, r, a), tx = Math.sin(R(a)), ty = Math.cos(R(a));
      b += dot(px, py, 5) + T(px + (a > 90 ? -10 : 6), py + 24, nh, { w: 700, a: a > 90 ? 'end' : 'start' });
      b += arr(px, py, px + tx * 62, py + ty * 62, 'dv1', RED) + T(px + tx * 62 + (a > 90 ? -18 : 4), py + ty * 62 - 8, `v${sb(k)}`, { c: RED, w: 700 });
    });
    // chung gốc
    const ox = 214, oy = 100;
    vv.forEach(([a, , k]) => {
      const tx = Math.sin(R(a)), ty = Math.cos(R(a));
      b += arr(ox, oy, ox + tx * 86, oy + ty * 86, 'dv2', RED, k === '2' ? '7 4' : '') + T(ox + tx * 86 - 4, oy + ty * 86 + (ty < 0 ? -8 : 22), `v${sb(k)}`, { c: RED, w: 700 });
    });
    b += dot(ox, oy, 4) + T(ox + 40, 196, `${DL}v = ?`, { a: 'middle', w: 700 });
    return wrap('0 0 320 206', b, cap, 'Hiệu hai vectơ vận tốc');
  },
  // Trang 2 · thí nghiệm đồng xu trên bàn xoay
  dongXu: (cap = 'Quay chậm rồi nhanh dần. Lực nào giữ xu đi vòng?') => dia(cap, [{ r: 56, nhan: 'xu', goc: -20 }], { id: 'dx', R0: 80 }),
  // Trang 3 · thí nghiệm nút cao su quay trên đầu ống
  nutCaoSu: (cap = 'Kẹp sát miệng ống thì r = 0,50 m. Quả nặng đứng yên: lực căng T bằng bao nhiêu?') => {
    let b = defs('nc1') + defs('nc2');
    const ox = 58, top = 70;
    b += `<rect x="${ox - 8}" y="${top}" width="16" height="78" rx="3" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<ellipse cx="170" cy="${top}" rx="124" ry="22" fill="none" stroke="${GREY}" stroke-width="2" stroke-dasharray="7 5"/>`;
    b += ln(ox, top, 282, top, INK, 2);
    b += ci(288, top, 11, { fill: GREY }) + T(296, top - 18, 'm', { a: 'end', w: 700 });
    b += arr(270, top + 1, 210, top + 1, 'nc1', RED) + T(220, top + 26, 'T', { c: RED, w: 700 });
    b += ln(ox, top + 78, ox, 176, INK, 2);
    b += `<rect x="${ox - 18}" y="176" width="36" height="22" rx="3" fill="${GREY}" stroke="${INK}" stroke-width="${SW}"/>` + T(ox + 26, 194, 'M', { w: 700 });
    b += ln(ox + 14, top - 34, 282, top - 34, BLUE, 2) + ln(ox + 14, top - 42, ox + 14, top - 26, BLUE, 2) + ln(282, top - 42, 282, top - 26, BLUE, 2);
    b += T(170, top - 40, 'r = 0,50 m', { c: BLUE, a: 'middle' });
    b += `<rect x="${ox + 4}" y="${top + 2}" width="8" height="6" fill="${INK}"/>` + T(ox + 16, top + 40, 'kẹp', { size: 20 });
    return wrap('0 0 320 206', b, cap, 'Nút cao su quay tròn, dây luồn qua ống, treo quả nặng');
  },
  // Trang 3 · Bẫy 2: bi trong vòng có chỗ hở
  viBi: (cap = 'Tới chỗ hở, bi đi theo đường 1 hay 2?') => {
    let b = defs('vb1');
    const x = 110, y = 110, r = 80;
    b += cung(x, y, r, 30, 360, { w: 4 });
    b += dot(x, y, 4.5) + T(x - 6, y + 26, 'O', { a: 'end', w: 700 });
    const [px, py] = P(x, y, r - 8, 8);
    b += ci(px, py, 8, { fill: GREY });
    b += arr(px, py - 10, px, py - 96, 'vb1', BLUE, '7 5') + T(px + 8, py - 82, '1', { c: BLUE, w: 700 });
    b += arr(px + 10, py - 1, px + 104, py - 14, 'vb1', INK, '3 5') + T(px + 104, py + 18, '2', { w: 700, a: 'end' });
    b += cung(x, y, r - 24, 250, 330, { c: GREY, w: 2.4, mk: 'vb1' });
    return wrap('0 0 320 200', b, cap, 'Viên bi chạy sát thành vòng có chỗ hở');
  },
  // Trang 4 · bài toán mẫu: xe qua cua, nhìn từ phía sau
  xeSau: (cap = 'Nhìn từ phía sau, tâm cua ở bên trái. Lực nào hướng vào tâm?') => {
    let b = defs('xs1') + defs('xs2') + defs('xs3');
    b += ln(10, 160, 310, 160);
    b += `<rect x="112" y="64" width="96" height="76" rx="10" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<rect x="118" y="134" width="18" height="26" rx="3" fill="${INK}"/><rect x="184" y="134" width="18" height="26" rx="3" fill="${INK}"/>`;
    b += arr(146, 104, 146, 196, 'xs1', RED) + T(156, 194, 'P', { c: RED, w: 700 });
    b += arr(176, 156, 176, 44, 'xs2', INK) + T(186, 60, 'N', { w: 700 });
    b += arr(118, 160, 52, 160, 'xs1', RED) + T(46, 150, `F${sb('ms')}`, { c: RED, w: 700, a: 'end' });
    b += arr(100, 34, 20, 34, 'xs3', BLUE, '7 5') + T(106, 40, 'về tâm cua', { c: BLUE });
    return wrap('0 0 320 206', b, cap, 'Các lực lên ô tô khi qua cua đường phẳng');
  },
  // Trang 5 · thử thách ★★★: trạm vũ trụ
  traiDat: (cap = 'Trạm cách tâm Trái Đất r = R + h.') => {
    let b = defs('td1');
    const x = 120, y = 108;
    b += ci(x, y, 64, { fill: '#eef2fa' }) + dot(x, y, 4) + ci(x, y, 92, { fill: 'none', c: GREY, w: 2.2, dash: '7 5' });
    b += ln(x, y, x - 64, y, INK, 2) + T(x - 34, y + 24, 'R', { a: 'middle', w: 700 });
    const [px, py] = P(x, y, 92, 40);
    b += ci(px, py, 8, { fill: GREY }) + arr(px + 6, py + 7, px + 6 + 66 * Math.sin(R(40)), py + 7 + 66 * Math.cos(R(40)), 'td1', RED) + T(px + 58, py + 72, 'v', { c: RED, w: 700 });
    b += T(px + 12, py - 12, 'trạm', {});
    b += ln(x - 64, y, x - 92, y, BLUE, 2.4) + T(x - 78, y - 8, 'h', { c: BLUE, a: 'middle', w: 700 });
    return wrap('0 0 320 208', b, cap, 'Trạm vũ trụ bay tròn quanh Trái Đất');
  },

  // ===== Bài tập mẫu =====
  biDay: (cap = '') => {
    let b = '';
    const x = 150, y = 92, r = 84;
    b += ci(x, y, r, { c: GREY, w: 2.2, dash: '7 5' }) + dot(x, y, 5) + T(x, y - 12, 'O', { a: 'middle', w: 700 });
    b += ln(x, y, x - r, y, INK, 2) + ci(x - r, y, 9, { fill: GREY }) + ci(x + r, y, 9, { fill: '#fff', c: GREY, dash: '4 3' });
    b += T(x - r - 4, y + 34, 'A', { w: 700 }) + T(x + r - 4, y + 34, 'B', { w: 700 });
    b += T(x - r - 22, y - 16, '?', { c: RED, w: 700 }) + T(x + r + 14, y - 16, '?', { c: RED, w: 700 });
    b += T(x - 40, y + 26, 'r', { w: 700 });
    return wrap('0 0 300 186', b, cap, 'Hòn bi quay tròn trên bàn, hai vị trí A và B');
  },
  vongQuay: (cap = '') => {
    let b = '';
    const x = 150, y = 98, r = 78;
    b += ci(x, y, r) + dot(x, y, 5);
    for (let a = 0; a < 360; a += 45) {
      const [px, py] = P(x, y, r, a);
      b += ln(x, y, px, py, GREY, 2) + `<rect x="${f1(px - 9)}" y="${f1(py)}" width="18" height="16" rx="2" fill="#fff" stroke="${INK}" stroke-width="2.4"/>`;
    }
    b += ln(x, y + 4, x - 30, 196, INK) + ln(x, y + 4, x + 30, 196, INK);
    b += T(x + 40, y - 6, 'r = 15 m', { w: 700 }) + T(8, 26, 'T = 40 s', { w: 700 });
    return wrap('0 0 300 200', b, cap, 'Vòng quay công viên');
  },
  quat: (cap = '') => dia(cap, [{ r: 26, nhan: 'A', goc: 60 }, { r: 76, nhan: 'B', goc: -12 }], { id: 'qt', R0: 80 })
    .replace('aria-label="Đĩa quay đều nhìn từ trên xuống"', 'aria-label="Quạt trần, điểm A gần trục, B ở đầu cánh"'),
  diaVat: (cap = '') => dia(cap, [{ r: 62, nhan: '50 g', goc: -20 }], { id: 'dv', vat: true }),
  moTo: (cap = '') => {
    let b = defs('mt1');
    const x = 34, y = 190;
    b += cung(x, y, 168, 2, 88, { w: SW }) + cung(x, y, 122, 2, 88, { w: SW });
    b += dot(x, y, 4.5) + T(x + 8, y - 8, 'tâm');
    const [px, py] = P(x, y, 145, 45);
    b += ci(px, py, 9, { fill: GREY }) + ln(x, y, px, py, GREY, 2, '5 4') + T((x + px) / 2 + 10, (y + py) / 2 + 16, 'r');
    b += arr(px + 10, py + 10, px + 64, py + 64, 'mt1', RED) + T(px + 70, py + 56, 'v', { c: RED, w: 700 });
    b += T(296, 30, 'đường nằm ngang', { a: 'end', size: 20 });
    return wrap('0 0 300 200', b, cap, 'Mô tô vào đường vòng nằm ngang');
  },
  // ===== Bài tương tự =====
  diaMN: (cap = 'Cùng một đĩa quay đều.') => dia(cap, [{ r: 30, nhan: 'M', goc: 60 }, { r: 88, nhan: 'N', goc: -12 }], { id: 'mn' }),
  xuTT: (cap = 'Xu cách tâm 12 cm.') => dia(cap, [{ r: 58, nhan: 'xu', goc: -20 }], { id: 'xt' }),
};
