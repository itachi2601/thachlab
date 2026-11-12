// Hình minh hoạ cho ruột tập VL10 · Bài 3 Thực hành tính sai số trong phép đo. Ghi kết quả đo (lesson 48, Chương 1 Mở đầu).
// Cùng quy tắc với hinh.mjs: mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh. Xem thử: node scripts/ruot-tap/l10-bai3.mjs --hinh (chụp vào out/hinh-l10-bai3/).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const dot = (x, y, r = 6, c = INK) => `<circle cx="${x}" cy="${y}" r="${r}" fill="${c}"/>`;
const rect = (x, y, w, h, r = 3) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r}" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
// thước kẻ: từ vạch a tới b (mm), mỗi mm 22 đơn vị, bắt đầu x0; vạch dài ở số chẵn, ghi số mỗi 2 mm
const thuoc = (x0, y, a, b, step = 22) => {
  let s = rect(x0 - 12, y, (b - a) * step + 24, 34, 2);
  for (let k = a; k <= b; k++) {
    const x = x0 + (k - a) * step, dai = k % 2 === 0;
    s += ln(x, y, x, y + (dai ? 17 : 10), INK, 2);
    if (dai) s += T(x, y + 32, String(k), { a: 'middle', size: 18 });
  }
  return s;
};

export const hinhL10b3 = {
  // Trang 1 · Dự đoán: cùng một cục tẩy, hai dụng cụ (chỉ mô tả cái thấy)
  haiThuoc: (cap = 'Cùng một cục tẩy, đo bằng hai dụng cụ.') => {
    let b = T(8, 22, 'Thước kẻ 1 mm', { w: 700 });
    b += rect(14, 36, 12 * 15, 40, 4) + T(14 + 6 * 15, 62, 'tẩy', { a: 'middle' });
    b += thuoc(14, 76, 0, 12, 15);
    b += T(8, 160, 'Thước điện tử', { w: 700 });
    b += rect(8, 172, 176, 70, 8) + rect(24, 184, 96, 42, 4) + T(72, 214, '12,05 mm', { a: 'middle', w: 700 });
    b += ln(136, 206, 168, 206, INK, 5) + dot(152, 206, 4);
    return wrap('0 0 216 256', b, cap, 'Một cục tẩy đo bằng thước kẻ chia vạch và thước điện tử');
  },
  // Trang 2 · mép vật đúng vạch 12 của thước chia vạch 1 mm
  thuocDoc: (cap = 'Mép cục tẩy nằm đúng vạch 12 của thước vạch 1 mm.') => {
    let b = rect(8, 24, 84, 40, 4) + ln(92, 14, 92, 64, RED, 2.2, '5 4');
    b += thuoc(20, 64, 10, 14, 36);
    b += T(160, 118, 'mm', { size: 20 });
    return wrap('0 0 190 124', b, cap, 'Thước chia vạch 1 mm với mép vật nằm đúng vạch 12');
  },
  // Trang 3 · năm lần đo thời gian 10 dao động, không đánh dấu trung bình
  diemDo: (cap = 'Năm lần đo thời gian 10 dao động (s).') => {
    const vals = [20.19, 19.85, 20.14, 19.94, 20.23], x0 = 24, k = 600; // 1 s = 600 đơn vị
    const X = (v) => x0 + (v - 19.8) * k;
    let b = ln(x0, 78, x0 + 0.5 * k, 78, INK, 2.5);
    for (const v of [19.8, 20.0, 20.2, 20.3]) b += ln(X(v), 78, X(v), 90, INK, 2.2) + T(X(v), 114, v.toFixed(1).replace('.', ','), { a: 'middle', size: 20 });
    vals.forEach((v, i) => { b += dot(X(v), 78 - 16 - (i % 2) * 22, 7, RED) + T(X(v), 78 - 46 - (i % 2) * 22 + 6, String(i + 1), { a: 'middle', size: 20, w: 700 }); });
    return wrap('0 0 340 126', b, cap, 'Năm chấm trên trục thời gian từ 19,8 s đến 20,3 s');
  },
  // Trang 4 · bẫy 1: hai hàng năm lần đo, giá trị thật là nét đứt
  haiHang: (cap = 'Hai dãy năm lần đo; nét đứt là giá trị thật.') => {
    let b = '';
    const hang = (y, xs, nhan) => ln(24, y, 296, y, GREY, 2) + ln(160, y - 24, 160, y + 24, INK, 2.5, '6 4')
      + xs.map((x) => dot(x, y, 6.5, RED)).join('') + T(8, y - 30, nhan, { w: 700 });
    b += hang(60, [184, 198, 212, 226, 240], 'Dãy 1') + hang(150, [128, 190, 150, 176, 160], 'Dãy 2');
    return wrap('0 0 320 190', b, cap, 'Hai dãy chấm: dãy 1 nằm lệch về một phía, dãy 2 nằm hai phía của nét đứt');
  },
  // Bài tập mẫu D1 · cân điện tử (không hiện số)
  can: (cap = 'Cân điện tử, viên bi đặt trên đĩa.') => {
    let b = rect(40, 100, 200, 44, 8) + rect(120, 112, 80, 22, 3) + T(160, 130, '? ? ?', { a: 'middle', size: 20 });
    b += ln(80, 100, 200, 100, INK, 4) + `<circle cx="140" cy="82" r="16" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    return wrap('0 0 280 160', b, cap, 'Viên bi đặt trên đĩa cân điện tử');
  },
  // Bài tập mẫu D2 · xe trên đường ray dài s
  rayXe: (cap = 'Xe lăn trên đường ray dài s.') => {
    let b = ln(20, 120, 300, 120, INK, 4) + rect(40, 76, 56, 30, 4) + `<circle cx="54" cy="114" r="8" fill="#fff" stroke="${INK}" stroke-width="${SW}"/><circle cx="82" cy="114" r="8" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += ln(40, 148, 290, 148, GREY, 2) + ln(40, 142, 40, 154, GREY, 2) + ln(290, 142, 290, 154, GREY, 2) + T(165, 182, 's', { a: 'middle', w: 700, size: 26 });
    b += `<path d="M96,92 L136,92" stroke="${BLUE}" stroke-width="${SW}" fill="none"/><path d="M136,92 l-9,-5 v10 z" fill="${BLUE}"/>`;
    return wrap('0 0 320 190', b, cap, 'Xe lăn chạy dọc đường ray');
  },
  // Bài tập mẫu D3 · mặt phẳng nghiêng dài s
  mpn: (cap = 'Vật trượt xuống mặt nghiêng dài s.') => {
    let b = `<path d="M20,160 L280,160 L280,40 z" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<g transform="rotate(-24.8 120 124)"><rect x="96" y="96" width="48" height="26" rx="3" fill="#fff" stroke="${INK}" stroke-width="${SW}"/></g>`;
    b += T(176, 96, 's', { w: 700, size: 26 }) + `<path d="M130,128 L160,108" stroke="${BLUE}" stroke-width="${SW}" fill="none" stroke-dasharray="6 4"/>`;
    return wrap('0 0 320 190', b, cap, 'Vật trên mặt phẳng nghiêng, quãng đường s dọc mặt nghiêng');
  },
  // Bài tập mẫu D3 · bài tương tự: hai thước đo cạnh khối
  cungDoDai: (cap = 'Dây dài 1 m, đo bằng thước vạch 1 mm.') => {
    let b = ln(30, 20, 30, 150, INK, 3) + dot(30, 20, 5) + ln(30, 150, 30, 150) + ln(30, 20, 130, 112, INK, 3) + `<circle cx="130" cy="124" r="14" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += T(60, 96, 'l', { w: 700 });
    return wrap('0 0 220 170', b, cap, 'Con lắc đơn dài l');
  },
};
