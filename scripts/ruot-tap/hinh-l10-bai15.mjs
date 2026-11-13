// Hình minh hoạ cho ruột tập VL10 · Bài 15 Định luật 2 Newton (lesson 60). Cùng quy tắc với hinh.mjs/hinh-l10-bai23.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh (hình Dự đoán KHÔNG vẽ mũi tên gia tốc).
// Ảnh thực tế duy nhất: book/assets/anh-that/day-xe-truot-bang.jpg (Wikimedia, CC BY-SA 4.0, khai báo ở book/sach/l10-ch3-dong-luc-hoc.json).
// Xem thử: node scripts/ruot-tap/l10-bai15.mjs --hinh (chụp vào out/hinh-l10-bai15/).
import { dirname, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const f1 = (v) => (+v).toFixed(1);
const arr = (x1, y1, x2, y2, id, c = INK, dash = '') =>
  `<line x1="${f1(x1)}" y1="${f1(y1)}" x2="${f1(x2)}" y2="${f1(y2)}" stroke="${c}" stroke-width="${SW}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${f1(x1)}" y1="${f1(y1)}" x2="${f1(x2)}" y2="${f1(y2)}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const dat = (x1, x2, y) => ln(x1, y, x2, y) + Array.from({ length: Math.floor((x2 - x1) / 18) }, (_, i) =>
  ln(x1 + 8 + i * 18, y, x1 + i * 18, y + 8, GREY, 1.8)).join('');
// người que, đầu tại (x,y), k = tỉ lệ chiều cao
const nguoi = (x, y, k = 1, tay = '') => `<circle cx="${x}" cy="${y}" r="${11 * k}" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
  + ln(x, y + 11 * k, x, y + 62 * k) + ln(x, y + 62 * k, x - 14 * k, y + 104 * k) + ln(x, y + 62 * k, x + 14 * k, y + 104 * k) + tay;
const banh = (x, y, r = 8) => `<circle cx="${x}" cy="${y}" r="${r}" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
const oto = (x, y) => `<path d="M${x},${y + 34} L${x},${y + 14} L${x + 18},${y + 14} L${x + 30},${y} L${x + 62},${y} L${x + 76},${y + 14} L${x + 92},${y + 16} L${x + 92},${y + 34} z" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
  + banh(x + 20, y + 36, 9) + banh(x + 72, y + 36, 9);
const anhThat = (file, cap) => `<figure class="fig"><img src="${pathToFileURL(resolve(dirname(fileURLToPath(import.meta.url)), '../../book/assets/anh-that', file)).href}" alt="" style="display:block;width:100%;height:auto">${cap ? `<figcaption>${cap}</figcaption>` : ''}</figure>`;

export const hinhL10b15 = {
  // Trang 1 · Dự đoán: cùng lực 80 N đẩy hai người khác khối lượng — KHÔNG vẽ gia tốc, không vẽ quãng đường
  sanBang: (cap = 'Cùng một lực đẩy 80 N vào lưng; băng trơn, ma sát coi bằng 0.') => {
    let b = defs('sb1');
    b += dat(6, 314, 168);
    b += nguoi(78, 92, 0.72) + T(78, 70, '40 kg', { a: 'middle', w: 700 });
    b += arr(18, 120, 64, 120, 'sb1', RED) + T(16, 108, '80 N', { c: RED, w: 700 });
    b += ln(160, 20, 160, 160, GREY, 2, '4 4');
    b += nguoi(256, 56, 1.08) + T(256, 34, '80 kg', { a: 'middle', w: 700 });
    b += arr(186, 120, 240, 120, 'sb1', RED) + T(184, 108, '80 N', { c: RED, w: 700 });
    return wrap('0 0 320 180', b, cap, 'Cùng lực đẩy hai người khối lượng khác nhau');
  },
  // Trang 1 · ảnh thực tế (chú thích không nêu kết luận a = F/m)
  xeTruotBang: (cap = 'Xuất phát xe trượt băng: cả đội đẩy thật mạnh trong vài giây đầu rồi mới nhảy lên xe.') =>
    anhThat('day-xe-truot-bang.jpg', cap + '<br><span style="font-size:2.4mm">Ảnh: 121a0012 · Wikimedia Commons · CC BY-SA 4.0</span>'),
  // Trang 2 · thí nghiệm: xe trên máng đệm khí, ròng rọc, quả nặng, hai cổng quang
  mangDemKhi: (cap = 'Quả nặng kéo xe qua dây vắt ròng rọc; cảm biến đo F, hai cổng quang đo t.') => {
    let b = defs('md1');
    b += `<rect x="8" y="112" width="270" height="10" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += [20, 50, 80, 110, 140, 170, 200, 230, 260].map((x) => `<circle cx="${x}" cy="117" r="2" fill="${GREY}"/>`).join('');
    b += `<rect x="12" y="88" width="54" height="24" rx="3" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
      + `<rect x="66" y="92" width="14" height="14" fill="${GREY}" stroke="${INK}" stroke-width="2"/>` + T(30, 80, 'xe', { a: 'middle' });
    b += `<circle cx="290" cy="112" r="12" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + ln(278, 117, 286, 140, INK, 2.4);
    b += ln(80, 100, 290, 100, INK, 1.8) + ln(302, 112, 302, 150, INK, 1.8);
    b += `<rect x="290" y="150" width="24" height="26" fill="${GREY}" stroke="${INK}" stroke-width="${SW}"/>`;
    [[74, 'cổng 1'], [224, 'cổng 2']].forEach(([x, s]) => {
      b += ln(x, 40, x, 112, INK, 2.4) + ln(x - 8, 40, x + 8, 40, INK, 2.4) + ln(x, 50, x, 112, RED, 1.6, '3 3') + T(x, 30, s, { a: 'middle' });
    });
    b += ln(74, 150, 224, 150, INK, 2) + ln(74, 142, 74, 158, INK, 2) + ln(224, 142, 224, 158, INK, 2) + T(149, 176, 's = 0,50 m', { a: 'middle' });
    return wrap('0 0 320 186', b, cap, 'Xe trên máng đệm khí kéo bởi quả nặng');
  },
  // Trang 2 · lưới đồ thị a–F để HS tự chấm 4 điểm (không vẽ sẵn điểm/đường)
  doThiAF: (cap = 'Chấm 4 điểm (F; a) từ bảng, rồi thử kẻ một đường thẳng qua gốc O.') => {
    const ox = 58, oy = 190, sx = 50, sy = 38; // 0,1 N = 60 đơn vị; 0,2 m/s² = 38 đơn vị
    let b = defs('dt1');
    for (let i = 1; i <= 4; i++) b += ln(ox + i * sx, oy, ox + i * sx, oy - 4 * sy - 6, GREY, 1.2, '3 3') + T(ox + i * sx, oy + 24, `0,${i}`, { a: 'middle' });
    for (let j = 1; j <= 4; j++) b += ln(ox, oy - j * sy, ox + 4 * sx + 6, oy - j * sy, GREY, 1.2, '3 3') + T(ox - 6, oy - j * sy + 7, `0,${2 * j}`, { a: 'end' });
    b += arr(ox, oy, ox + 4 * sx + 40, oy, 'dt1') + arr(ox, oy, ox, 14, 'dt1');
    b += T(ox - 8, oy + 24, 'O', { a: 'end' }) + T(318, oy - 10, 'F (N)', { a: 'end', w: 700 }) + T(ox + 12, 22, 'a (m/s²)', { w: 700 });
    return wrap('0 0 320 222', b, cap, 'Lưới đồ thị gia tốc theo lực để học sinh tự chấm điểm');
  },
  // Trang 3 · bẫy 2: xe đang phanh — vẽ v và lực hãm, gia tốc để HS tự vẽ
  xePhanh: (cap = 'Xe đang phanh, vẫn chạy sang phải. Vẽ mũi tên gia tốc vào ô nét đứt.') => {
    let b = defs('xp1') + defs('xp2');
    b += dat(6, 314, 134);
    b += oto(110, 82);
    b += arr(206, 64, 296, 64, 'xp1', BLUE, '7 4') + T(300, 56, 'v', { c: BLUE, w: 700, a: 'end' });
    b += arr(110, 104, 34, 104, 'xp2', RED) + T(30, 94, `F${sb('hãm')}`, { c: RED, w: 700 });
    b += `<rect x="20" y="16" width="170" height="36" rx="4" fill="#fff" stroke="${INK}" stroke-width="2" stroke-dasharray="5 4"/>` + T(30, 42, 'a:', { w: 700 });
    return wrap('0 0 320 146', b, cap, 'Xe đang phanh: vận tốc và lực hãm');
  },
  // Trang 4 · bài toán mẫu: xe đẩy siêu thị, F : Fms = 3 : 1, P và N thu nhỏ, chung điểm đặt tại tâm xe
  xeDay: (cap = 'F và F<sub>ms</sub> vẽ đúng tỉ lệ 3 : 1; P, N thu nhỏ, triệt tiêu nhau.', { F = 'F', ms = 'ms' } = {}) => {
    let b = defs('xd1') + defs('xd2') + defs('xd3');
    b += dat(6, 314, 176);
    b += `<path d="M104,82 L216,82 L206,150 L114,150 z" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + ln(216, 82, 236, 64) + banh(124, 164, 10) + banh(196, 164, 10);
    const cx = 160, cy = 116;
    b += arr(cx, cy, cx + 138, cy, 'xd1', RED) + T(300, cy - 10, F, { c: RED, w: 700, a: 'end' });
    b += arr(cx, cy, cx - 46, cy, 'xd2', INK, '6 4') + T(cx - 32, cy + 28, `F${sb(ms)}`, { a: 'middle', w: 700 });
    b += arr(cx, cy, cx, cy - 56, 'xd3', INK) + T(cx + 8, cy - 42, 'N', { w: 700 });
    b += arr(cx, cy, cx, cy + 46, 'xd3', INK) + T(cx + 10, cy + 30, 'P', { w: 700 });
    b += `<circle cx="${cx}" cy="${cy}" r="3.5" fill="${INK}"/>`;
    return wrap('0 0 320 188', b, cap, 'Các lực tác dụng lên xe đẩy');
  },
  // BTM Dạng 2: thùng bị kéo bằng dây nằm ngang, trượt về phía người kéo
  thungKeo: (cap = '', { F = '120 N', ms = '50 N', m = '35 kg' } = {}) => {
    let b = defs('tk1') + defs('tk2') + defs('tk3');
    b += dat(6, 314, 140);
    b += `<rect x="44" y="90" width="80" height="50" rx="3" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(84, 121, m, { a: 'middle', w: 700 });
    b += ln(124, 110, 256, 110, INK, 2) + nguoi(276, 36, 1, ln(276, 62, 256, 108));
    b += arr(128, 80, 212, 80, 'tk1', RED) + T(128, 66, `F = ${F}`, { c: RED, w: 700 });
    b += arr(44, 126, 8, 126, 'tk2', INK, '6 4') + T(6, 166, `F${sb('ms')}= ${ms}`, { w: 700 });
    b += arr(170, 164, 250, 164, 'tk3', BLUE, '7 4') + T(170, 190, 'hướng trượt', { c: BLUE });
    return wrap('0 0 320 198', b, cap, 'Thùng bị kéo bằng dây nằm ngang');
  },
  // BTM Dạng 5 / bài tương tự: ô tô phanh, vết phanh dài s rồi dừng
  otoPhanh: (cap = '', { v0 = '108 km/h', s = '90 m' } = {}) => {
    let b = defs('op1') + defs('op2');
    b += dat(6, 314, 112);
    b += oto(8, 60) + oto(214, 60);
    b += arr(40, 44, 108, 44, 'op1', BLUE, '7 4') + T(8, 24, `v${sb('0')}= ${v0}`, { c: BLUE, w: 700 });
    b += T(258, 48, 'v = 0', { a: 'middle', w: 700 });
    b += ln(100, 104, 222, 104, INK, 4, '2 6');
    b += ln(100, 130, 222, 130, INK, 2) + ln(100, 122, 100, 138, INK, 2) + ln(222, 122, 222, 138, INK, 2) + T(161, 156, `vết phanh ${s}`, { a: 'middle' });
    return wrap('0 0 320 162', b, cap, 'Ô tô phanh để lại vết phanh rồi dừng');
  },
  // BTM Dạng 6 / bài tương tự: chạy đều (Fk = Fc) tới O thì tắt máy, chậm dần tới khi dừng
  tatMay: (cap = '', { v = '90 km/h', Fk = '900 N' } = {}) => {
    let b = defs('tm1') + defs('tm2') + defs('tm3');
    b += dat(6, 314, 112);
    b += oto(40, 60);
    b += arr(132, 82, 176, 82, 'tm1', RED) + T(154, 72, `F${sb('k')}`, { c: RED, w: 700, a: 'middle' });
    b += arr(40, 82, 6, 82, 'tm2', INK, '6 4') + T(8, 106, `F${sb('c')}`, { w: 700 });
    b += T(10, 22, `chạy đều ${v}`, { w: 700 }) + T(10, 44, `F${sb('k')}= ${Fk}`, { c: RED });
    b += ln(196, 40, 196, 124, INK, 2.4) + T(196, 144, 'O: tắt máy', { a: 'middle', w: 700 });
    b += arr(206, 82, 306, 82, 'tm3', BLUE, '7 4') + T(312, 68, 'chậm dần', { a: 'end', c: BLUE }) + T(312, 144, 'dừng', { a: 'end' });
    return wrap('0 0 320 152', b, cap, 'Ô tô chạy đều rồi tắt máy');
  },
};
