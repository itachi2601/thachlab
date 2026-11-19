// Hình minh hoạ cho ruột tập VL12 Chương 3 · Bài 14 Máy phát điện xoay chiều. Máy biến áp (lesson 125). Cùng quy tắc với hinh.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh. Xem thử: node scripts/ruot-tap/l12-c3-bai14.mjs --hinh (chụp vào out/hinh-l12-c3-bai14/).
import { ve } from './hinh.mjs';
import { m } from './khung.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
// chữ Hi Lạp/Ω/→: Source Sans 3 chỉ nạp latin/vietnamese → lấy từ KaTeX (đã nạp qua katex.min.css), không thì rơi về Helvetica
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const km = (ch) => `<tspan font-family="KaTeX_Main">${ch}</tspan>`;
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const arr = (x1, y1, x2, y2, id, c = INK, dash = '', w = SW) =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const rect = (x, y, w, h, o = {}) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${o.rx ?? 3}" fill="${o.fill ?? '#fff'}" stroke="${o.c ?? INK}" stroke-width="${o.sw ?? SW}"/>`;
// cuộn dây đứng: k vòng (nửa elip) dọc theo x, từ y0 tới y1
const cuon = (x, y0, y1, k, c = INK) => {
  const h = (y1 - y0) / k;
  return Array.from({ length: k }, (_, i) => `<path d="M${x - 12},${y0 + i * h} Q${x + 18},${y0 + (i + .5) * h} ${x - 12},${y0 + (i + 1) * h}" fill="none" stroke="${c}" stroke-width="2.6"/>`).join('');
};
// nguồn xoay chiều (vòng tròn có ~)
const ac = (x, y, r = 16) => `<circle cx="${x}" cy="${y}" r="${r}" fill="#fff" stroke="${INK}" stroke-width="${SW}"/><path d="M${x - 9},${y} q4.5,-9 9,0 t9,0" fill="none" stroke="${INK}" stroke-width="2.4"/>`;
// máy biến áp nhỏ (hai cuộn trên lõi) cho sơ đồ truyền tải
const mbaNho = (x, y, nhan) => `<circle cx="${x - 9}" cy="${y}" r="15" fill="#fff" stroke="${INK}" stroke-width="2.6"/><circle cx="${x + 9}" cy="${y}" r="15" fill="none" stroke="${INK}" stroke-width="2.6"/>`
  + T(x, y + 40, nhan, { a: 'middle' });
const nha = (x, y) => `<path d="M${x},${y} L${x + 22},${y - 20} L${x + 44},${y} Z" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + rect(x + 5, y, 34, 26, { rx: 0 });
const cot = (x, y) => `<path d="M${x - 10},${y + 60} L${x},${y} L${x + 10},${y + 60} M${x - 14},${y + 10} L${x + 14},${y + 10}" fill="none" stroke="${GREY}" stroke-width="2.4"/>`;

// Sơ đồ máy phát → (máy biến áp) → đường dây R → tải, dùng cho II.5, bài toán mẫu, Dạng 4–5
const soDo = (cap, o = {}) => {
  const { up = 'U', mba = null, r = 'R', p = 'P', id = 'sd' } = o;
  let b = defs(id);
  b += ac(46, 70, 20) + T(46, 116, 'máy phát', { a: 'middle' }) + T(46, 30, p, { a: 'middle', w: 700 });
  let x = 66;
  if (mba) { b += ln(66, 70, 96, 70) + mbaNho(114, 70, mba); x = 132; }
  b += ln(x, 70, x + 22, 70) + T(x + 6, 52, up, { w: 700 });
  // đường dây = điện trở R
  b += rect(x + 22, 60, 80, 20, { rx: 0 }) + T(x + 62, 104, r, { a: 'middle', w: 700 });
  b += arr(x + 30, 46, x + 70, 46, id, RED) + T(x + 76, 46, 'I', { c: RED, w: 700 });
  b += ln(x + 102, 70, x + 124, 70) + rect(x + 124, 50, 44, 40) + T(x + 146, 116, 'tải', { a: 'middle' });
  return wrap(`0 0 ${x + 176} 128`, b, cap, 'Sơ đồ truyền tải điện từ máy phát qua đường dây tới nơi tiêu thụ');
};

export const hinhL12c3b14 = {
  // ===== Trang học bài mới =====
  // Dự đoán: KHÔNG có chữ "hao phí", không vẽ dòng nhỏ/lớn — chỉ con số điện áp trên đường đi
  duongDay: (cap = 'Từ nhà máy tới ổ cắm: điện áp đổi hai lần.') => {
    let b = ac(44, 70, 20) + T(44, 112, 'nhà máy', { a: 'middle' });
    b += ln(64, 70, 96, 70) + mbaNho(114, 70, 'trạm 1');
    b += ln(132, 70, 150, 40) + cot(156, 30) + cot(222, 30) + ln(156, 40, 222, 40, INK, 2.6) + ln(222, 40, 238, 70);
    b += T(189, 22, '500 kV', { a: 'middle', w: 700 });
    b += mbaNho(256, 70, 'trạm 2') + ln(274, 70, 290, 70) + nha(290, 76) + T(312, 128, '220 V', { a: 'middle', w: 700 });
    return wrap('0 0 344 136', b, cap, 'Đường đi của điện từ nhà máy qua hai trạm biến áp tới nhà');
  },
  khungQuay: (cap = 'Khung N vòng quay đều quanh trục vuông góc với B; ' + m('\\alpha') + ' là góc giữa pháp tuyến n và B.') => {
    let b = defs('kq1') + defs('kq2');
    b += rect(8, 40, 46, 120, { rx: 2 }) + T(31, 108, 'N', { a: 'middle', w: 700, size: 26 });
    b += rect(246, 40, 46, 120, { rx: 2 }) + T(269, 108, 'S', { a: 'middle', w: 700, size: 26 });
    [70, 100, 130].forEach((y) => { b += arr(60, y, 238, y, 'kq1', GREY, '6 5', 1.8); });
    b += T(226, 58, 'B', { c: GREY, w: 700 });
    // khung nghiêng (hình bình hành) + trục dọc
    b += ln(150, 18, 150, 186, INK, 2, '4 4') + T(158, 24, 'trục');
    b += `<path d="M118,58 L182,44 L182,148 L118,162 Z" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
    b += arr(150, 103, 196, 142, 'kq2', RED) + T(202, 160, 'n', { c: RED, w: 700 });
    b += `<path d="M180,103 A30,30 0 0 1 173,122" fill="none" stroke="${RED}" stroke-width="2"/>` + T(186, 124, gk('α'), { c: RED });
    b += `<path d="M126,182 A26,8 0 1 0 174,182" fill="none" stroke="${INK}" stroke-width="2"/>` + arr(172, 184, 176, 180, 'kq2', INK, '', 2) + T(186, 196, gk('ω'));
    return wrap('0 0 300 204', b, cap, 'Khung dây quay trong từ trường đều giữa hai cực nam châm');
  },
  // II.2: hỏi số cặp cực → chú thích không nói số
  roTo4: (cap = 'Rô-to nam châm quay trong stato có cuộn dây. Đếm cực N, S để tìm p.') => {
    let b = `<circle cx="110" cy="100" r="92" fill="none" stroke="${INK}" stroke-width="${SW}"/><circle cx="110" cy="100" r="74" fill="none" stroke="${GREY}" stroke-width="1.8"/>`;
    b += rect(96, 2, 28, 22, { rx: 2 }) + cuon(110, 4, 24, 3, BLUE);
    // 4 cực xen kẽ
    [['N', 0], ['S', 90], ['N', 180], ['S', 270]].forEach(([c, a]) => {
      const r = (a - 90) * Math.PI / 180, x = 110 + 44 * Math.cos(r), y = 100 + 44 * Math.sin(r);
      b += `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="20" fill="${c === 'N' ? '#e9ecf4' : '#fff'}" stroke="${INK}" stroke-width="2.4"/>` + T(x, y + 7, c, { a: 'middle', w: 700 });
    });
    b += `<circle cx="110" cy="100" r="6" fill="${INK}"/>`;
    b += T(214, 30, 'stato') + ln(212, 36, 196, 52, GREY, 1.8) + T(214, 186, 'rô-to') + ln(212, 176, 150, 136, GREY, 1.8);
    b += T(214, 92, 'cuộn') + T(214, 114, 'dây') + ln(212, 86, 128, 16, GREY, 1.8);
    return wrap('0 0 280 204', b, cap, 'Máy phát có rô-to nam châm nhiều cực quay trong stato');
  },
  baPha: (cap = 'Ba cuộn giống nhau đặt lệch nhau trên stato; nam châm quay ở giữa.') => {
    const cx = 130, cy = 124, R = 88;
    let b = `<circle cx="${cx}" cy="${cy}" r="${R}" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
    [0, 120, 240].forEach((a, i) => {
      const r = (a - 90) * Math.PI / 180, x = cx + R * Math.cos(r), y = cy + R * Math.sin(r);
      b += `<g transform="rotate(${a} ${x.toFixed(1)} ${y.toFixed(1)})">${rect(x - 16, y - 12, 32, 24, { rx: 2 })}</g>` + T(cx + 116 * Math.cos(r), cy + 116 * Math.sin(r) + 7, String(i + 1), { a: 'middle', w: 700 });
    });
    // hai bán kính tới cuộn 1 và cuộn 2 + cung góc
    const r2 = 30 * Math.PI / 180;
    b += ln(cx, cy, cx, cy - R + 14, GREY, 1.8, '5 4') + ln(cx, cy, cx + (R - 14) * Math.cos(r2), cy + (R - 14) * Math.sin(r2), GREY, 1.8, '5 4');
    b += `<path d="M${cx},${cy - 62} A62,62 0 0 1 ${(cx + 62 * Math.cos(r2)).toFixed(1)},${(cy + 62 * Math.sin(r2)).toFixed(1)}" fill="none" stroke="${GREY}" stroke-width="2"/>` + T(cx + 68, cy - 42, '?', { w: 700 });
    b += `<rect x="${cx - 12}" y="${cy - 40}" width="24" height="40" fill="#e9ecf4" stroke="${INK}" stroke-width="2.4"/><rect x="${cx - 12}" y="${cy}" width="24" height="40" fill="#fff" stroke="${INK}" stroke-width="2.4"/>`;
    b += T(cx, cy - 14, 'N', { a: 'middle', w: 700, size: 18 }) + T(cx, cy + 28, 'S', { a: 'middle', w: 700, size: 18 });
    b += `<path d="M${cx - 30},${cy + 22} A36,36 0 0 1 ${cx - 30},${cy - 22}" fill="none" stroke="${RED}" stroke-width="2.4"/>` + T(cx - 52, cy + 7, gk('ω'), { c: RED });
    return wrap('0 0 260 226', b, cap, 'Ba cuộn dây trên stato của máy phát ba pha');
  },
  bienAp: (cap = 'Hai cuộn quấn trên một lõi thép kín. Đường đứt: đường sức từ trong lõi.', o = {}) => {
    const { k1 = 4, k2 = 7 } = o;
    let b = defs('ba1');
    b += `<path d="M70,20 H230 V180 H70 Z M100,50 H200 V150 H100 Z" fill="#eef2fa" fill-rule="evenodd" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<path d="M85,35 H215 V165 H85 Z" fill="none" stroke="${GREY}" stroke-width="1.8" stroke-dasharray="6 5"/>`;
    b += cuon(85, 62, 138, k1, BLUE) + cuon(215, 46, 154, k2, RED);
    b += ln(73, 62, 30, 62) + ln(73, 138, 30, 138) + ac(30, 100) + ln(30, 62, 30, 84) + ln(30, 116, 30, 138);
    b += ln(203, 46, 270, 46) + ln(203, 154, 270, 154) + rect(258, 82, 24, 36, { rx: 2 }) + ln(270, 46, 270, 82) + ln(270, 118, 270, 154);
    b += T(4, 196, `U${sb('1')}`, { w: 700 }) + T(296, 196, `U${sb('2')}`, { w: 700, a: 'end' });
    b += T(112, 108, `N${sb('1')}`, { w: 700 }) + T(190, 108, `N${sb('2')}`, { w: 700, a: 'end' });
    return wrap('0 0 300 204', b, cap, 'Máy biến áp có hai cuộn dây trên một lõi thép');
  },
  truyenTai: (cap = 'Cùng P, R: dòng I trên dây do điện áp nơi phát U quyết định.') => soDo(cap, { id: 'tt5' }),
  // Bẫy 2: hai rô-to, cùng tốc độ
  capCuc: (cap = 'Cùng quay 25 vòng/s. Rô-to (b) đi qua cuộn dây nhiều cực hơn.') => {
    let b = '';
    const ro = (cx, poles, lab) => {
      let s = `<circle cx="${cx}" cy="76" r="54" fill="none" stroke="${GREY}" stroke-width="1.8"/>` + T(cx, 22, lab, { a: 'middle', w: 700 });
      poles.forEach((c, i) => {
        const r = (i * 360 / poles.length - 90) * Math.PI / 180, x = cx + 30 * Math.cos(r), y = 76 + 30 * Math.sin(r);
        s += `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="16" fill="${c === 'N' ? '#e9ecf4' : '#fff'}" stroke="${INK}" stroke-width="2.4"/>` + T(x, y + 7, c, { a: 'middle', w: 700, size: 18 });
      });
      return s;
    };
    b += ro(70, ['N', 'S'], '(a)') + ro(214, ['N', 'S', 'N', 'S'], '(b)');
    return wrap('0 0 284 140', b, cap, 'Rô-to một cặp cực và rô-to hai cặp cực');
  },
  // ===== Bài toán mẫu =====
  mau: (cap = 'Tổ máy 20 kW, 500 V; dây R = 2 Ω.') => soDo(cap, { up: 'U', mba: 'MBA', r: `R = 2 ${km('Ω')}`, p: '20 kW', id: 'mau' }),
  // ===== Bài tập mẫu =====
  soDoD5: (cap = 'Máy biến áp đặt ngay sau máy phát.') => soDo(cap, { up: `U${sb('2')}`, mba: 'MBA', r: 'R', p: 'P', id: 'd5' }),
};
