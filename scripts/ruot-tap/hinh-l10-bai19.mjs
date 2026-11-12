// Hình minh hoạ cho ruột tập VL10 · Bài 19 Lực cản và lực nâng (lesson 64). Cùng quy tắc với hinh.mjs/hinh-l10-bai23.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh. Xem thử: node scripts/ruot-tap/l10-bai19.mjs --hinh (chụp vào out/hinh-l10-bai19/).
// Ảnh thật duy nhất: book/assets/anh-that/nhay-du-roi-tu-do.jpg (Tony Danbury · Wikimedia Commons · CC BY 2.0, có trong git).
import { dirname, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
// chữ Hi Lạp: Source Sans 3 chỉ nạp latin/vietnamese → lấy từ KaTeX_Math (đã nạp qua katex.min.css)
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const arr = (x1, y1, x2, y2, id, c = INK, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${SW}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const NUOC = '#e3ecf8';
const ANH_THAT = resolve(dirname(fileURLToPath(import.meta.url)), '../../book/assets/anh-that');

// Lực kế treo vật: móc trên ở (x, y0), vạch số chỉ ghi chữ `so`; vật hình hộp ở dưới. Trả về chuỗi SVG.
const lucKe = (x, y0, so, { vat = 'hop', w = 40, h = 34, day = 40, trai = false } = {}) => {
  let b = ln(x, y0 - 14, x, y0) + `<rect x="${x - 13}" y="${y0}" width="26" height="70" rx="5" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
  for (let i = 0; i < 5; i++) b += ln(x - 7, y0 + 12 + i * 11, x + 7, y0 + 12 + i * 11, GREY, 1.8);
  b += ln(x, y0 + 70, x, y0 + 70 + day);
  const vy = y0 + 70 + day;
  b += vat === 'cau' ? `<circle cx="${x}" cy="${vy + h / 2}" r="${h / 2}" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
    : `<rect x="${x - w / 2}" y="${vy}" width="${w}" height="${h}" rx="3" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
  const bw = so.length * 10 + 14, bx = trai ? x - 18 - bw : x + 18;
  if (so) b += `<rect x="${bx}" y="${y0 + 22}" width="${bw}" height="28" rx="4" fill="#fff" stroke="${BLUE}" stroke-width="2"/>` + T(bx + 7, y0 + 43, so, { c: BLUE, w: 700 });
  return b;
};
const coc = (x, y, w, h, muc) => `<rect x="${x}" y="${y + muc}" width="${w}" height="${h - muc}" fill="${NUOC}"/>`
  + `<path d="M${x},${y} L${x},${y + h} L${x + w},${y + h} L${x + w},${y}" fill="none" stroke="${INK}" stroke-width="${SW}"/>`
  + ln(x, y + muc, x + w, y + muc, BLUE, 2, '6 4');

export const hinhL10b19 = {
  // Dự đoán: hai tờ A4 lúc vừa thả, cùng độ cao, KHÔNG vẽ lực và không vẽ tờ nào thấp hơn (không lộ đáp án).
  haiTo: (cap = '') => {
    let b = ln(20, 40, 300, 40, GREY, 2, '6 5') + T(160, 28, 'cùng độ cao, thả cùng lúc', { a: 'middle', c: GREY });
    // viên giấy vo: đường gấp khúc trong hình tròn
    b += `<circle cx="90" cy="70" r="20" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
      + `<path d="M76,64 L88,76 L95,60 L104,74" fill="none" stroke="${GREY}" stroke-width="2"/>`;
    // tờ phẳng: hình bình hành mỏng
    b += `<path d="M185,62 L285,62 L275,80 L175,80 z" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += T(90, 122, 'viên giấy vo', { a: 'middle' }) + T(230, 122, 'tờ để phẳng', { a: 'middle' });
    b += ln(20, 168, 300, 168) + Array.from({ length: 15 }, (_, i) => ln(28 + i * 18, 168, 20 + i * 18, 176, GREY, 1.8)).join('');
    b += T(160, 160, 'sàn', { a: 'middle', c: GREY });
    return wrap('0 0 320 182', b, cap, 'Hai tờ giấy A4 giống hệt nhau lúc vừa thả');
  },
  // Đồ thị v–t của vật rơi trong không khí; vùng giai đoạn để trống số cho HS ghi 1, 2, 3.
  vt: (cap = '') => {
    const X0 = 46, Y0 = 186, W = 260, H = 150;
    let b = defs('vta');
    b += arr(X0, Y0, X0 + W + 6, Y0, 'vta') + arr(X0, Y0, X0, Y0 - H - 14, 'vta');
    b += T(X0 + W + 4, Y0 + 24, 't', { a: 'end' }) + T(X0 - 8, Y0 - H - 4, 'v', { a: 'end' });
    const vg = 120; // tốc độ giới hạn (đơn vị hình)
    b += ln(X0, Y0 - vg, X0 + W, Y0 - vg, GREY, 2, '6 5') + T(X0 - 6, Y0 - vg + 7, `v${sb('gh')}`, { a: 'end', size: 20 });
    // v = vg·tanh(t/τ)
    const tau = 70, pts = Array.from({ length: 53 }, (_, i) => { const x = i * 5; return `${(X0 + x).toFixed(1)},${(Y0 - vg * Math.tanh(x / tau)).toFixed(1)}`; });
    b += `<polyline points="${pts.join(' ')}" fill="none" stroke="${RED}" stroke-width="${SW}"/>`;
    b += ln(X0, Y0, X0 + 82, Y0 - 141, BLUE, 2.2, '4 4') + T(X0 + 86, Y0 - 140, 'v = gt', { c: BLUE, size: 20 });
    // ranh giới giai đoạn
    b += ln(X0 + 28, Y0, X0 + 28, Y0 - 6, INK, 2) + ln(X0 + 160, Y0, X0 + 160, Y0 - 6, INK, 2);
    const o = (x) => `<rect x="${x - 13}" y="${Y0 - 50}" width="26" height="28" rx="4" fill="#fff" stroke="${INK}" stroke-width="2"/>`;
    b += o(X0 + 14) + o(X0 + 94) + o(X0 + 212);
    return wrap('0 0 320 200', b, cap, 'Đồ thị tốc độ theo thời gian của vật rơi trong không khí');
  },
  // Ảnh thật người nhảy dù chưa mở dù.
  nhayDu: (cap = '') => `<figure class="fig"><img src="${pathToFileURL(ANH_THAT + '/nhay-du-roi-tu-do.jpg').href}" alt="Người nhảy dù chưa mở dù" style="display:block;width:100%;height:auto">${cap ? `<figcaption>${cap}</figcaption>` : ''}</figure>`,
  // Thí nghiệm lực kế + bình tràn: ba lần đo, số chỉ để trống ở lần 3.
  binhTran: (cap = '') => {
    let b = '';
    b += lucKe(46, 24, '2,65', { day: 30 }) + T(46, 214, 'ngoài', { a: 'middle' }) + T(46, 236, 'không khí', { a: 'middle' });
    b += coc(118, 112, 64, 92, 18) + lucKe(150, 24, '2,16', { day: 19 }) + T(150, 230, 'chìm nửa', { a: 'middle' });
    b += coc(240, 112, 64, 92, 18) + lucKe(272, 24, '1,67', { day: 46, trai: true }) + T(272, 230, 'chìm hẳn', { a: 'middle' });
    return wrap('0 0 320 244', b, cap, 'Lực kế treo khối nhôm ở ba vị trí');
  },
  // Khối hộp chìm trong chất lỏng: áp lực F1 lên mặt trên, F2 lên mặt dưới, Δh, S. Không ghi độ lớn.
  hopApSuat: (cap = '') => {
    let b = defs('hpa') + defs('hpb');
    b += `<rect x="10" y="20" width="300" height="190" fill="${NUOC}"/>` + ln(10, 20, 310, 20, BLUE, 2.4);
    b += T(20, 46, 'chất lỏng', { c: BLUE });
    const x = 110, y = 86, w = 100, h = 64;
    b += `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += arr(x + w / 2, y - 44, x + w / 2, y - 4, 'hpa', RED) + T(x + w / 2 + 8, y - 22, `F${sb('1')}`, { c: RED, w: 700 });
    b += arr(x + w / 2, y + h + 58, x + w / 2, y + h + 4, 'hpb', RED) + T(x + w / 2 + 8, y + h + 36, `F${sb('2')}`, { c: RED, w: 700 });
    b += ln(x + w + 16, y, x + w + 16, y + h, INK, 2) + ln(x + w + 10, y, x + w + 22, y, INK, 2) + ln(x + w + 10, y + h, x + w + 22, y + h, INK, 2);
    b += T(x + w + 24, y + h / 2 + 7, `${gk('Δ')}h`);
    b += T(x + 8, y + h / 2 + 7, 'đáy S', { size: 20 });
    // mũi tên ngang cân bằng ở hai mặt bên (nét đứt)
    b += arr(x - 40, y + h / 2, x - 4, y + h / 2, 'hpa', GREY, '5 4') + arr(x + w + 72, y + h / 2 + 22, x + w + 4, y + h / 2 + 22, 'hpb', GREY, '5 4');
    return wrap('0 0 320 216', b, cap, 'Khối hộp chìm trong chất lỏng, áp lực lên mặt trên và mặt dưới');
  },
  // Bài toán mẫu: cùng khối nhôm, treo ngoài không khí và nhúng chìm trong nước; số chỉ trong nước để "?".
  nhomLucKe: (cap = '') => {
    let b = lucKe(70, 20, '5,4 N', { day: 34 }) + T(70, 210, 'ngoài không khí', { a: 'middle' });
    b += coc(190, 104, 84, 94, 14) + lucKe(232, 20, '?', { day: 52 }) + T(232, 222, 'trong nước', { a: 'middle' });
    return wrap('0 0 320 232', b, cap, 'Khối nhôm treo lực kế ngoài không khí và trong nước');
  },
  // Thử thách ⭐⭐⭐: tảng băng nổi, không ghi tỉ lệ (vẽ phần chìm lớn, không chia vạch).
  bang: (cap = '') => {
    let b = `<rect x="10" y="62" width="300" height="140" fill="${NUOC}"/>` + ln(10, 62, 310, 62, BLUE, 2.4);
    b += `<path d="M130,62 L148,36 L170,28 L190,44 L200,62 L236,120 L222,182 L150,194 L96,160 L104,104 z" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += T(20, 54, 'mặt nước biển', { c: BLUE }) + T(160, 130, 'băng', { a: 'middle' });
    return wrap('0 0 320 206', b, cap, 'Tảng băng nổi trên nước biển');
  },
  // Dạng 1: quả cầu chìm hoàn toàn trong nước biển (không vẽ lực đẩy).
  cauBien: (cap = '') => {
    let b = coc(60, 30, 200, 160, 20) + T(70, 44, 'nước biển', { c: BLUE });
    b += ln(160, 0, 160, 92, INK, 2) + `<circle cx="160" cy="120" r="28" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(160, 127, 'V', { a: 'middle', w: 700 });
    return wrap('0 0 320 196', b, cap, 'Quả cầu chìm hoàn toàn trong nước biển');
  },
  // Dạng 2: vừa bung dù — chỉ vẽ lực cản (lên) và vận tốc (xuống), không vẽ trọng lực.
  bungDu: (cap = '') => {
    let b = defs('bda') + defs('bdb');
    b += `<path d="M70,70 Q160,-10 250,70 Q205,56 160,66 Q115,56 70,70 z" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += ln(74, 70, 152, 140, GREY, 1.8) + ln(246, 70, 168, 140, GREY, 1.8) + ln(160, 66, 160, 140, GREY, 1.8);
    b += `<circle cx="160" cy="146" r="9" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + ln(160, 155, 160, 186) + ln(160, 186, 150, 212) + ln(160, 186, 170, 212);
    b += arr(206, 150, 206, 92, 'bda', RED) + T(214, 116, `F${sb('c')}`, { c: RED, w: 700 });
    b += arr(108, 150, 108, 206, 'bdb', BLUE, '6 4') + T(100, 196, 'v', { c: BLUE, w: 700, a: 'end' });
    return wrap('0 0 320 220', b, cap, 'Người vừa bung dù, lực cản hướng lên, vận tốc hướng xuống');
  },
  // Dạng 3: khối đồng treo lực kế chìm hẳn trong chất lỏng lạ.
  dongLong: (cap = '', so = '8,1 N') => {
    let b = coc(70, 104, 120, 100, 14) + T(84, 196, 'chất lỏng ?', { c: BLUE });
    b += lucKe(130, 20, so, { day: 54 });
    return wrap('0 0 320 210', b, cap, 'Khối đồng treo lực kế chìm hẳn trong chất lỏng');
  },
};
