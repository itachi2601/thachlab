// Hình minh hoạ cho ruột tập VL10 · Bài 14 Định luật 1 Newton (lesson 59). Cùng quy tắc với hinh.mjs / hinh-l10-bai23.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, tự vẽ. Chú thích không lộ đáp án ô Dự đoán / ô điền cạnh hình:
// hình cạnh ô điền chỉ vẽ lực đã biết, lực cần tìm ghi "?" (không vẽ mũi tên có độ dài để khỏi lộ "bằng nhau").
// Ảnh thật (hình nhân thử va chạm) lấy từ book/assets/anh-that (Wikimedia, CC BY 3.0, ghi nguồn trong chú thích).
// Xem thử: node scripts/ruot-tap/l10-bai14.mjs --hinh (chụp vào out/hinh-l10-bai14/).
import { existsSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const arr = (x1, y1, x2, y2, id, c = INK, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${SW}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const R = (d) => (d * Math.PI) / 180;
const f1 = (v) => v.toFixed(1);
const cung = (x, y, r, a1, a2, c = INK) => {
  const p = (a) => `${f1(x + r * Math.cos(R(a)))},${f1(y - r * Math.sin(R(a)))}`;
  return `<path d="M${p(a1)} A${r},${r} 0 0 ${a2 > a1 ? 0 : 1} ${p(a2)}" fill="none" stroke="${c}" stroke-width="2.2"/>`;
};
const dat = (x1, x2, y) => ln(x1, y, x2, y) + Array.from({ length: Math.floor((x2 - x1) / 18) }, (_, i) =>
  ln(x1 + 8 + i * 18, y, x1 + i * 18, y + 8, GREY, 1.8)).join('');
const nguoi = (x, y) => `<circle cx="${x}" cy="${y}" r="11" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
  + ln(x, y + 11, x, y + 62) + ln(x, y + 62, x - 14, y + 104) + ln(x, y + 62, x + 14, y + 104) + ln(x, y + 26, x + 20, y + 46);
const xe = (x, y, w, h) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="4" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
  + `<circle cx="${x + 18}" cy="${y + h + 7}" r="7" fill="#fff" stroke="${INK}" stroke-width="${SW}"/><circle cx="${x + w - 18}" cy="${y + h + 7}" r="7" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;

// Thùng trên sàn ngang, dây/lực chếch góc α (lên hoặc xuống); chỉ vẽ lực đã cho
const thung = (cap, { nhan = 'T = 50 N', xuong = false, v = true, id = 'th' } = {}) => {
  let b = defs(id + 'a') + defs(id + 'b');
  b += dat(10, 310, 150);
  b += `<rect x="110" y="104" width="90" height="46" rx="4" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
  if (!xuong) {
    const x0 = 200, y0 = 112, L = 96, ex = x0 + L * 0.8, ey = y0 - L * 0.6;
    b += arr(x0, y0, f1(ex), f1(ey), id + 'a', RED) + T(ex - 4, ey - 8, nhan, { c: RED, w: 700, a: 'end' });
    b += ln(x0, y0, x0 + 70, y0, GREY, 2, '5 4') + cung(x0, y0, 36, 0, 36.87) + T(x0 + 42, y0 - 6, gk('α'));
  } else { // đẩy từ phía sau, chếch xuống: lực đặt vào góc trên-trái của thùng
    const x1 = 106, y1 = 106, L = 90, sx = x1 - L * 0.8, sy = y1 - L * 0.6;
    b += arr(f1(sx), f1(sy), x1, y1, id + 'a', RED) + T(sx, sy - 8, nhan, { c: RED, w: 700 });
    b += ln(x1 - 76, y1, x1, y1, GREY, 2, '5 4') + cung(x1, y1, 36, 180, 143.13) + T(x1 - 60, y1 - 4, gk('α'));
  }
  if (v) b += arr(120, 178, 200, 178, id + 'b', BLUE, '6 4') + T(208, 184, 'v không đổi', { c: BLUE });
  return wrap('0 0 320 192', b, cap, 'Thùng trên sàn ngang, lực chếch góc α');
};

// Xe trên đường ngang: lực nào đã biết thì vẽ, lực cần tìm ghi "?" tại điểm đặt
const oTo = (cap, { taiXe = false, id = 'ot', biet = ['Fk', 'P'] } = {}) => {
  let b = defs(id + 'a') + defs(id + 'b');
  b += dat(8, 312, 150);
  b += taiXe
    ? xe(70, 80, 130, 56) + `<rect x="200" y="100" width="46" height="36" rx="4" fill="#fff" stroke="${INK}" stroke-width="${SW}"/><circle cx="228" cy="143" r="7" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
    : xe(110, 98, 100, 38);
  const cx = taiXe ? 158 : 160, cy = 118, phai = taiXe ? 246 : 210, trai = taiXe ? 70 : 110;
  const co = (k) => biet.includes(k);
  b += co('Fk') ? arr(phai, cy, phai + 50, cy, id + 'a', RED) + T(phai + 52, cy - 12, `F${sb('k')}`, { c: RED, w: 700, a: 'end' }) : T(phai + 6, cy - 6, `F${sb('k')} ?`, { w: 700 });
  b += co('Fc') ? arr(trai, cy, trai - 50, cy, id + 'b', INK, '6 4') + T(trai - 50, cy - 20, `F${sb('c')}`, { w: 700 }) : T(trai - 6, cy - 6, `F${sb('c')} ?`, { w: 700, a: 'end' });
  b += co('P') ? arr(cx, cy, cx, cy + 58, id + 'a', RED) + T(cx + 12, cy + 50, 'P', { c: RED, w: 700 }) : '';
  b += co('N') ? arr(cx, cy, cx, cy - 58, id + 'b', INK) + T(cx + 8, cy - 46, 'N', { w: 700 }) : T(cx - 6, cy - 30, 'N ?', { w: 700 });
  return wrap('0 0 320 184', b, cap, 'Xe trên đường ngang và các lực');
};

const ANH = [resolve(dirname(fileURLToPath(import.meta.url)), '../../book/assets/anh-that'), '/Users/MAC/Projects/thachlab/book/assets/anh-that'].find((d) => existsSync(d));

export const hinhL10b14 = {
  // Trang 1 · Dự đoán: bánh khúc côn cầu vừa rời gậy (không vẽ gì sau khi rời gậy)
  banh: (cap = 'Bánh vừa rời gậy. Mặt băng không ma sát, không có không khí.') => {
    let b = defs('bk');
    b += ln(10, 104, 310, 104) + Array.from({ length: 6 }, (_, i) => ln(40 + i * 48, 114, 64 + i * 48, 114, GREY, 1.8)).join('');
    b += ln(30, 14, 70, 98, INK, 4) + ln(70, 98, 104, 98, INK, 5);
    b += `<ellipse cx="150" cy="96" rx="24" ry="8" fill="${INK}"/>`;
    b += T(310, 138, 'băng', { a: 'end', c: GREY });
    return wrap('0 0 320 146', b, cap, 'Bánh khúc côn cầu trượt trên băng');
  },
  // Trang 2 · thí nghiệm Galilei: hai máng, hạ dần máng (2)
  haiMang: (cap = 'Thả bi từ độ cao h<sub>0</sub> trên máng (1). Hạ máng (2): 30° → 15° → 5°.') => {
    let b = '';
    b += ln(10, 54, 320, 54, GREY, 2, '6 5') + T(316, 46, `h${sb('0')}`, { a: 'end', c: GREY });
    b += ln(14, 54, 104, 154) + ln(4, 154, 316, 154, INK, 2);
    [[30, ''], [15, '6 4'], [5, '2 5']].forEach(([g, d]) => {
      const L = 200, ex = 104 + L * Math.cos(R(g)), ey = 154 - L * Math.sin(R(g));
      b += ln(104, 154, f1(ex), f1(ey), INK, SW, d) + T(ex - 6, ey - 8, `${g}°`, { a: 'end' });
    });
    b += `<circle cx="24" cy="56" r="9" fill="${GREY}" stroke="${INK}" stroke-width="2"/>`;
    b += T(36, 128, '(1)', { w: 700 }) + T(150, 178, '(2)', { w: 700 });
    return wrap('0 0 320 186', b, cap, 'Hai máng nghiêng của Galilei');
  },
  // Trang 2 · định luật 1: ô tô chạy thẳng đều, chỉ cho F_k và P
  oTo: (cap = 'Xe chạy thẳng đều. Vẽ thêm F<sub>c</sub> và N với độ dài em chọn.') => oTo(cap),
  // Trang 3 · thí nghiệm đồng xu – bìa – cốc (không vẽ kết quả)
  dongXu: (cap = 'Búng thật nhanh vào mép bìa theo phương ngang.') => {
    let b = defs('dx');
    b += `<path d="M110,74 L126,166 L194,166 L210,74" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<rect x="86" y="64" width="150" height="10" fill="#fff" stroke="${INK}" stroke-width="2.4"/>`;
    b += `<ellipse cx="160" cy="58" rx="18" ry="6" fill="${GREY}" stroke="${INK}" stroke-width="2"/>`;
    b += arr(14, 69, 80, 69, 'dx', RED) + T(12, 54, 'búng', { c: RED, w: 700 });
    b += T(244, 74, 'bìa') + T(184, 38, 'đồng xu') + T(214, 136, 'cốc');
    return wrap('0 0 320 176', b, cap, 'Đồng xu đặt trên tấm bìa trên miệng cốc');
  },
  // Trang 3 · bẫy 3: phanh gấp — chỉ vẽ lực có thật (ma sát sàn lên chân)
  phanhGap: (cap = 'Xe phanh gấp: sàn kéo chân chậm lại. Còn thân người?') => {
    let b = defs('pg1') + defs('pg2');
    b += ln(8, 152, 312, 152) + T(312, 176, 'sàn xe', { a: 'end', c: GREY });
    b += arr(40, 22, 130, 22, 'pg1', BLUE, '6 4') + T(138, 28, 'xe đang chạy', { c: BLUE });
    b += nguoi(170, 48);
    b += arr(196, 146, 120, 146, 'pg2', RED) + T(114, 140, `F${sb('ms')}`, { c: RED, w: 700, a: 'end' });
    return wrap('0 0 320 184', b, cap, 'Người đứng trên xe đang phanh');
  },
  // Trang 4 · bài toán mẫu: xe tải, bốn lực
  xeTai: (cap = 'Bốn lực lên xe tải. Viết cân bằng cho từng phương.') => oTo(cap, { taiXe: true, id: 'xt', biet: ['Fk', 'Fc', 'P', 'N'] }),
  // Trang 5 · ảnh thật: hình nhân thử va chạm
  anhVaCham: (cap = 'Thử va chạm: dây an toàn giữ người.<br><span style="font-size:2.4mm">Ảnh: Brady Holt · Wikimedia · <span style="white-space:nowrap">CC BY 3.0</span></span>') =>
    `<figure class="fig"><img src="${pathToFileURL(resolve(ANH, 'hinh-nhan-thu-va-cham.jpg')).href}" alt="Hình nhân thử va chạm" style="display:block;width:100%;height:19mm;object-fit:cover;object-position:60% 40%;filter:grayscale(1)"><figcaption>${cap}</figcaption></figure>`,

  // ===== Bài tập mẫu =====
  tuTruot: (cap = 'Tủ trượt đều. F<sub>ms</sub> và N chưa vẽ.') => {
    let b = defs('tt1') + defs('tt2');
    b += dat(10, 310, 150);
    b += `<rect x="100" y="70" width="70" height="80" rx="3" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + ln(135, 76, 135, 144, INK, 2);
    b += arr(170, 110, 262, 110, 'tt1', RED) + T(176, 98, 'F = 150 N', { c: RED, w: 700 });
    b += arr(110, 176, 190, 176, 'tt2', BLUE, '6 4') + T(198, 182, 'v không đổi', { c: BLUE });
    return wrap('0 0 320 190', b, cap, 'Tủ bị đẩy trên sàn ngang');
  },
  canCau: (cap = 'Kiện hàng đi lên đều. Lực căng T của cáp = ?') => {
    let b = defs('cc1') + defs('cc2');
    b += ln(130, 6, 130, 70, INK, 3) + `<path d="M130,70 L104,90 M130,70 L156,90" stroke="${INK}" stroke-width="2.4" fill="none"/>`;
    b += `<rect x="90" y="90" width="80" height="62" rx="3" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(130, 128, '450 kg', { a: 'middle', w: 700 });
    b += arr(130, 152, 130, 200, 'cc1', RED) + T(140, 190, 'P', { c: RED, w: 700 });
    b += arr(220, 170, 220, 80, 'cc2', BLUE, '6 4') + T(230, 120, 'v =', { c: BLUE }) + T(230, 144, '0,5 m/s', { c: BLUE });
    b += T(140, 40, 'T ?', { w: 700 });
    return wrap('0 0 320 208', b, cap, 'Cần cẩu nâng kiện hàng');
  },
  thungD3: (cap = 'Dây chếch lên góc <i style="font-family:KaTeX_Math">α</i>. F<sub>ms</sub> và N chưa vẽ.') => thung(cap, { id: 'd3' }),
  // ===== Bài tương tự =====
  thungTT: (cap = 'Đẩy chếch xuống: N lớn hơn hay nhỏ hơn P?') => thung(cap, { nhan: 'F = 50 N', xuong: true, id: 'ttx' }),
};
