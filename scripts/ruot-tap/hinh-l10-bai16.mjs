// Hình minh hoạ cho ruột tập VL10 · Bài 16 Định luật 3 Newton (lesson 61). Cùng quy tắc với hinh.mjs/hinh-l10-bai23.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh. Ảnh thực tế duy nhất: tên lửa (book/assets/anh-that, public domain).
// Xem thử: node scripts/ruot-tap/l10-bai16.mjs --hinh (chụp vào out/hinh-l10-bai16/).
import { dirname, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const HERE = dirname(fileURLToPath(import.meta.url));
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const arr = (x1, y1, x2, y2, id, c = INK, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${SW}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const rect = (x, y, w, h, rx = 3) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
const tron = (x, y, r) => `<circle cx="${x}" cy="${y}" r="${r}" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
// tường/thành có gạch chéo ở mặt sau (bên trái)
const tuong = (x, y1, y2) => rect(x, y1, 14, y2 - y1, 0) + Array.from({ length: Math.floor((y2 - y1) / 16) }, (_, i) =>
  ln(x - 10, y1 + 18 + i * 16, x, y1 + 8 + i * 16, GREY, 1.8)).join('');
// người que đứng: đầu (x,y); chân chạm y+104
const nguoi = (x, y) => tron(x, y, 11) + ln(x, y + 11, x, y + 62) + ln(x, y + 62, x - 14, y + 104) + ln(x, y + 62, x + 14, y + 104);
const giay = (x, y) => ln(x - 22, y, x + 22, y, INK, 3.2) + `<circle cx="${x - 14}" cy="${y + 5}" r="3" fill="${INK}"/><circle cx="${x + 14}" cy="${y + 5}" r="3" fill="${INK}"/>`;

// xe kéo / ngựa: dùng cho Dạng 2 và Thử thách ★★★
const nguaXe = ({ cap = '', mXe = '300 kg', keo = '', ms = '', mNgua = '', dat = '', hoi = '', id = 'nx' } = {}) => {
  let b = defs(id + 'a') + defs(id + 'b');
  b += ln(4, 160, 336, 160);
  b += rect(20, 100, 92, 34) + tron(42, 145, 10) + tron(90, 145, 10) + T(66, 124, mXe, { a: 'middle', w: 700, size: 18 });
  b += ln(112, 112, 176, 104, INK, 2.2);
  b += rect(176, 86, 84, 30, 12) + [186, 200, 236, 250].map((x) => ln(x, 116, x, 160)).join('');
  b += ln(256, 90, 274, 66) + tron(282, 58, 11);
  if (mNgua) b += T(218, 108, mNgua, { a: 'middle', w: 700, size: 18 });
  if (keo) b += arr(66, 80, 136, 80, id + 'a', RED) + T(66, 70, keo, { c: RED, w: 700 });
  if (ms) b += arr(66, 176, 14, 176, id + 'b', INK, '7 4') + T(74, 182, ms);
  if (dat) b += arr(214, 176, 290, 176, id + 'a', RED) + T(212, 200, dat, { c: RED, w: 700 });
  if (hoi) b += T(336, 24, hoi, { a: 'end', w: 700 });
  return wrap(`0 0 340 ${dat ? 206 : 192}`, b, cap, 'Ngựa kéo xe bằng dây trên đường nằm ngang');
};

// hai xe trên đường ray nhẵn (Dạng 3 và bài tương tự)
const haiXe = ({ cap = '', A = 'A: 1,5 kg', B = 'B: 0,5 kg', duoi = '', id = 'hx' } = {}) => {
  let b = defs(id + 'a');
  b += ln(6, 112, 314, 112) + ln(6, 118, 314, 118, GREY, 2);
  b += rect(40, 70, 90, 30) + tron(60, 104, 8) + tron(110, 104, 8);
  b += rect(130, 76, 60, 24) + tron(145, 104, 8) + tron(175, 104, 8);
  b += T(85, 60, A, { a: 'middle', w: 700 }) + T(200, 90, B, { w: 700 });
  b += arr(50, 22, 100, 22, id + 'a', BLUE, '7 4') + T(106, 28, 'v', { c: BLUE });
  if (duoi) b += T(6, 146, duoi, { size: 19 });
  return wrap(`0 0 320 ${duoi ? 156 : 128}`, b, cap, 'Xe A chạy tới va vào xe B đang đứng yên trên đường ray nhẵn');
};

// người đi giày trượt đặt tay lên thành/tường (Dự đoán và Dạng 1)
const thanhSan = ({ cap = '', ve = '', m = '', hoi = '', id = 'ts' } = {}) => {
  let b = defs(id + 'a');
  b += ln(4, 178, 296, 178) + tuong(34, 30, 178);
  b += nguoi(120, 64) + giay(120, 170);
  b += ln(120, 88, 48, 96) + ln(120, 94, 48, 104);
  if (ve) b += arr(100, 150, 52, 150, id + 'a', RED) + T(50, 138, ve, { c: RED, w: 700, size: 19 });
  if (m) b += T(120, 40, m, { a: 'middle', w: 700 });
  b += T(176, 70, 'thành gắn') + T(176, 92, 'chặt với đất');
  if (hoi) b += T(296, 130, hoi, { a: 'end', w: 700 });
  return wrap('0 0 300 190', b, cap, 'Người đi giày trượt đặt hai tay lên thành sân');
};

export const hinhL10b16 = {
  // Dự đoán: không vẽ chiều chuyển động, không vẽ lực của thành
  thanhSan: (cap = 'Em đi giày trượt, hai tay đẩy mạnh vào thành sân.') => thanhSan({ cap, ve: 'em đẩy' }),
  // II.1: người bơi đẩy thành bể — hai mũi tên ở hai vật khác nhau, nét khác nhau
  boiBe: (cap = 'Người bơi đạp chân vào thành bể.<br>Mũi tên đặc đặt lên thành, mũi tên đứt đặt lên người.') => {
    let b = defs('bba') + defs('bbb');
    b += tuong(100, 16, 156);
    b += ln(114, 50, 356, 50, GREY, 2, '8 5') + T(356, 40, 'mặt nước', { a: 'end', size: 18, c: GREY });
    b += ln(196, 88, 290, 88) + tron(302, 88, 11) + ln(290, 88, 350, 76) + ln(196, 88, 114, 80) + ln(196, 88, 114, 96);
    b += arr(100, 128, 30, 128, 'bba', RED) + T(4, 152, 'lên thành', { c: RED, w: 700 });
    b += arr(114, 128, 184, 128, 'bbb', BLUE, '8 4') + T(118, 152, 'lên người', { c: BLUE, w: 700 });
    return wrap('0 0 360 162', b, cap, 'Người bơi đạp chân vào thành bể, thành đẩy lại người');
  },
  // II.3: hai lực kế móc vào nhau; số chỉ để trống
  lucKe: (cap = 'Giữ đầu lực kế 1, kéo đầu lực kế 2.<br>Mỗi lực kế đo lực đặt lên chính nó.') => {
    let b = defs('lka');
    b += rect(4, 30, 14, 84, 0);
    const ke = (x, so) => rect(x, 56, 106, 32, 4) + Array.from({ length: 9 }, (_, i) => ln(x + 12 + i * 10, 56, x + 12 + i * 10, i % 2 ? 64 : 70, INK, 1.6)).join('')
      + T(x + 53, 46, `lực kế ${so}`, { a: 'middle', size: 19, w: 700 }) + T(x + 53, 112, '…… N', { a: 'middle', size: 19 });
    b += ln(18, 72, 32, 72) + ke(32, 1) + ln(138, 72, 168, 72) + ke(168, 2) + ln(274, 72, 290, 72);
    b += arr(290, 72, 336, 72, 'lka', RED) + T(338, 104, 'kéo', { a: 'end', c: RED, w: 700 });
    return wrap('0 0 340 122', b, cap, 'Hai lực kế lò xo móc vào nhau, một đầu giữ, một đầu kéo');
  },
  // Bẫy 1: sách nằm trên bàn
  sachBan: (cap = 'Sách nằm yên. P, N đặt lên sách; N’ đặt lên bàn.') => {
    let b = defs('sba') + defs('sbb');
    b += rect(20, 116, 260, 12, 2) + ln(36, 128, 36, 192) + ln(264, 128, 264, 192);
    b += rect(90, 86, 120, 30, 2) + T(150, 108, 'sách', { a: 'middle', size: 18 });
    b += arr(110, 101, 110, 168, 'sba', RED) + T(88, 166, 'P', { c: RED, w: 700 });
    b += arr(190, 116, 190, 44, 'sbb', BLUE) + T(200, 54, 'N', { c: BLUE, w: 700 });
    b += arr(190, 128, 190, 186, 'sbb', INK, '7 4') + T(200, 184, 'N’', { w: 700 });
    b += T(262, 108, 'bàn', { a: 'end', size: 18 });
    return wrap('0 0 300 198', b, cap, 'Quyển sách nằm yên trên mặt bàn');
  },
  // Bẫy 3: ảnh thực tế (Wikimedia, public domain) — chú thích chỉ tả cái em thấy
  tenLua: (cap = 'Tên lửa rời bệ phóng, khí nóng phụt xuống.<br><span style="font-size:.85em">Ảnh: Bill Ingalls · Wikimedia · PD</span>') =>
    `<figure class="fig"><img src="${pathToFileURL(resolve(HERE, '../../book/assets/anh-that/phong-ten-lua.jpg')).href}" alt="Tên lửa rời bệ phóng" style="display:block;width:100%;height:auto;filter:grayscale(1)"><figcaption>${cap}</figcaption></figure>`,
  // V: hai bạn trượt băng đẩy nhau — lực lên A để "?"
  haiBan: (cap = 'A đẩy B. Lực lên mỗi bạn và gia tốc của mỗi bạn?') => {
    let b = defs('hba') + defs('hbb');
    b += ln(4, 160, 316, 160);
    b += nguoi(100, 46) + giay(100, 152) + nguoi(220, 46) + giay(220, 152);
    b += ln(100, 70, 160, 80) + ln(220, 70, 160, 80);
    b += T(100, 22, 'A · 40 kg', { a: 'middle', w: 700 }) + T(220, 22, 'B · 60 kg', { a: 'middle', w: 700 });
    b += arr(220, 124, 296, 124, 'hba', RED) + T(316, 114, '120 N', { a: 'end', c: RED, w: 700 });
    b += arr(100, 124, 24, 124, 'hbb', RED, '8 4') + T(4, 114, 'F = ?', { c: RED, w: 700 });
    return wrap('0 0 320 172', b, cap, 'Hai bạn đi giày trượt đẩy tay nhau');
  },
  // Thử thách ★★★
  nguaXeTT: (cap = 'Đất đẩy chân ngựa 900 N; ma sát cản xe 300 N. Dây kéo xe T, kéo ngựa T theo chiều nào?') =>
    nguaXe({ cap, mXe: '200 kg', mNgua: '400 kg', ms: '300 N', dat: '900 N', id: 'nxt' }),
  // Dạng 1
  d1: (cap = 'Bỏ qua ma sát. Hình không vẽ lực của tường.') => thanhSan({ cap, ve: '90 N', m: '60 kg', hoi: 'a = ?', id: 'd1' }),
  // Dạng 2
  d2: (cap = 'Lực ngựa kéo xe (đặc), ma sát lên xe (đứt).') => nguaXe({ cap, keo: '800 N', ms: '200 N', id: 'd2' }),
  // Dạng 3
  d3: (cap = 'Hình không vẽ lực tương tác.') => haiXe({ cap, duoi: 'tương tác 0,2 s: B từ 0 lên 2,4 m/s', id: 'd3' }),
};
