// Hình minh hoạ cho ruột tập VL12 · Bài 2 Thang nhiệt độ (lesson 3). Cùng quy tắc với hinh.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh (vd thang Kelvin ở hình dự đoán để "?", đồ thị p–t để "?" chỗ cắt trục).
// Xem thử: node scripts/ruot-tap/l12-bai2.mjs --hinh (chụp vào out/hinh-l12-bai2/).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const arr = (x1, y1, x2, y2, id, c = INK, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${SW}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const rect = (x, y, w, h, o = {}) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${o.rx ?? 3}" fill="${o.fill ?? '#fff'}" stroke="${o.c ?? INK}" stroke-width="${o.sw ?? SW}"${o.dash ? ` stroke-dasharray="${o.dash}"` : ''}/>`;
// nhiệt kế đứng: ống từ y1 đến y2, bầu ở dưới, mực chất lỏng tại yl
const nk = (x, y1, y2, yl) => `<rect x="${x - 7}" y="${y1}" width="14" height="${y2 - y1}" rx="7" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
  + `<rect x="${x - 3}" y="${yl}" width="6" height="${y2 - yl + 4}" fill="${RED}"/>`
  + `<circle cx="${x}" cy="${y2 + 10}" r="12" fill="${RED}" stroke="${INK}" stroke-width="${SW}"/>`;
const nuoc = (x1, x2, y) => ln(x1, y, x2, y, BLUE, 2, '6 4');

export const hinhL12b2 = {
  // ===== Trang học bài mới =====
  // Dự đoán: cùng một thân nhiệt trên ba thang; thang Kelvin để "?" — không vẽ mốc 0 °C / 273 K để khỏi lộ đáp án.
  baThang: (cap = 'Cùng một cơn sốt, ba nhiệt kế ba thang.') => {
    let b = '';
    [[50, '38,5 °C', 'Celsius'], [150, '101,3 °F', 'Fahrenheit'], [250, '? K', 'Kelvin']].forEach(([x, s, ten]) => {
      b += nk(x, 46, 150, 84) + ln(x - 22, 84, x + 22, 84, GREY, 1.8, '4 3');
      b += T(x, 30, s, { a: 'middle', w: 700, c: s[0] === '?' ? RED : INK }) + T(x, 198, ten, { a: 'middle' });
    });
    return wrap('0 0 300 206', b, cap, 'Ba nhiệt kế ba thang đo cùng một thân nhiệt');
  },
  // II.1: hai vật trước và sau khi tiếp xúc (không vẽ mũi tên chiều truyền — ô điền hỏi chiều truyền)
  tiepXuc: (cap = 'a) Trước: T<sub>1</sub> khác T<sub>2</sub>. b) Sau một lúc tiếp xúc.') => {
    let b = T(4, 24, 'a)', { w: 700 }) + rect(40, 34, 90, 54) + rect(170, 34, 90, 54, { dash: '7 4' });
    b += T(85, 68, `T${sb('1')}`, { a: 'middle', w: 700 }) + T(215, 68, `T${sb('2')}`, { a: 'middle', w: 700 });
    b += T(4, 124, 'b)', { w: 700 }) + rect(60, 134, 90, 54) + rect(150, 134, 90, 54);
    b += T(105, 168, `T${sb('1')}′`, { a: 'middle', w: 700 }) + T(195, 168, `T${sb('2')}′`, { a: 'middle', w: 700 });
    return wrap('0 0 300 196', b, cap, 'Hai vật trước và sau khi tiếp xúc nhiệt');
  },
  // II.2: hai mốc — nước đá đang tan và hơi nước đang sôi
  haiMoc: (cap = 'Trái: nước đá đập nhỏ trộn nước cất. Phải: bầu nhiệt kế trong hơi, trên mặt nước sôi.') => {
    let b = '';
    b += `<path d="M20,70 L20,180 L120,180 L120,70" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + nuoc(20, 120, 92);
    [[30, 100], [62, 112], [90, 98], [40, 140], [78, 146], [96, 128]].forEach(([x, y]) => { b += rect(x, y, 18, 18, { sw: 2, rx: 2 }); });
    b += nk(60, 8, 124, 70);
    b += `<path d="M170,92 L170,180 L280,180 L280,92 Z" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + nuoc(170, 280, 140);
    [[190, 130], [215, 124], [245, 130], [265, 122]].forEach(([x, y]) => { b += `<path d="M${x},${y} q6,-10 0,-20 q-6,-10 0,-20" fill="none" stroke="${GREY}" stroke-width="2"/>`; });
    b += nk(225, 12, 96, 28);
    b += `<path d="M195,196 q8,-14 16,0 q8,-14 16,0 q8,-14 16,0 q8,-14 16,0" fill="none" stroke="${RED}" stroke-width="2.6"/>`;
    return wrap('0 0 300 204', b, cap, 'Kiểm tra hai mốc của nhiệt kế');
  },
  // II.3: áp suất khí theo nhiệt độ, kéo dài đường thẳng — chỗ cắt trục để "?"
  doThiP: (cap = 'Năm điểm đo; nét đứt kéo dài tới khi áp suất bằng 0.') => {
    const X = (tc) => 30 + (tc + 300) * 0.66, Y = (p) => 176 - p * 1.1;
    let b = defs('dtp1') + defs('dtp2');
    b += arr(14, 176, 296, 176, 'dtp1') + arr(X(-300) + 4, 188, X(-300) + 4, 12, 'dtp2');
    b += T(X(-300) + 22, 26, 'p (kPa)') + T(296, 202, 't (°C)', { a: 'end' });
    b += ln(X(-273.15), Y(0), X(100), Y(136.6), GREY, 2.2, '6 4');
    [[0, 100], [25, 109.2], [50, 118.3], [75, 127.5], [100, 136.6]].forEach(([tc, p]) => { b += `<circle cx="${X(tc)}" cy="${Y(p)}" r="4.5" fill="${INK}"/>`; });
    b += ln(X(0), 172, X(0), 180, INK, 2) + T(X(0), 200, '0', { a: 'middle' });
    b += T(X(-273.15), 200, '?', { a: 'middle', w: 700, c: RED });
    return wrap('0 0 300 208', b, cap, 'Đồ thị áp suất khí theo nhiệt độ, kéo dài về áp suất 0');
  },
  // II.5: nhiệt kế hồng ngoại không chạm trán (không ghi tên tính chất — ô bảng hỏi)
  hongNgoai: (cap = 'Nhiệt kế hồng ngoại: không chạm trán vẫn có số đo.') => {
    let b = `<circle cx="60" cy="80" r="44" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(60, 88, 'trán', { a: 'middle' });
    [0, 1, 2].forEach((i) => { b += `<path d="M${118 + i * 22},56 q8,24 0,48" fill="none" stroke="${RED}" stroke-width="2.4" stroke-dasharray="5 3"/>`; });
    b += `<path d="M190,62 L290,62 L290,98 L250,98 L242,150 L216,150 L222,98 L190,98 Z" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += rect(232, 70, 50, 22, { sw: 2 }) + T(257, 88, '37,2', { a: 'middle', w: 700, size: 18 });
    return wrap('0 0 300 158', b, cap, 'Nhiệt kế hồng ngoại đo trán');
  },
  // Bài toán mẫu: mặt số lò nướng
  loNuong: (cap = 'Lò đặt 200 °C; mặt số chia theo °F.') => {
    let b = `<circle cx="130" cy="96" r="74" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    for (let i = 0; i <= 10; i++) {
      const a = (-220 + i * 26) * Math.PI / 180, c = Math.cos(a), s = Math.sin(a);
      b += ln(130 + 62 * c, 96 + 62 * s, 130 + 72 * c, 96 + 72 * s, INK, i % 5 ? 2 : 3);
    }
    const a = (-220 + 6.6 * 26) * Math.PI / 180;
    b += ln(130, 96, 130 + 52 * Math.cos(a), 96 + 52 * Math.sin(a), RED, 4) + `<circle cx="130" cy="96" r="6" fill="${INK}"/>`;
    b += T(130, 152, '392 °F', { a: 'middle', w: 700 });
    return wrap('0 0 260 180', b, cap, 'Mặt số lò nướng chia theo độ Fahrenheit');
  },
  // ===== Bài tập mẫu / bài tương tự =====
  // vật nhỏ trong bể lớn (không vẽ chiều truyền)
  trongBe: (cap = 'Bể lớn, cách nhiệt; viên bi nhỏ.', nho = 'bi 120 °C', be = 'nước 25 °C') => {
    let b = `<path d="M14,8 L14,96 L286,96 L286,8" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + nuoc(14, 286, 22);
    b += `<circle cx="80" cy="72" r="14" fill="${GREY}" stroke="${INK}" stroke-width="${SW}"/>`;
    b += T(104, 79, nho, { w: 700 }) + T(150, 50, be, { a: 'middle', w: 700 });
    return wrap('0 0 300 104', b, cap, 'Vật nhỏ thả vào bể nước lớn cách nhiệt');
  },
  // ba vật tiếp xúc, mỗi vật một số đọc ở một thang
  baVat: (cap = 'Ba vật tiếp xúc, ba nhiệt kế khác thang.', so = ['68 °F', '293 K', '25 °C']) => {
    let b = '';
    ['A', 'B', 'C'].forEach((n, i) => {
      b += rect(14 + i * 92, 34, 92, 52, { rx: 0 }) + T(60 + i * 92, 68, n, { a: 'middle', w: 700, size: 24 });
      b += T(60 + i * 92, 24, so[i], { a: 'middle', w: 700 });
    });
    return wrap('0 0 300 92', b, cap, 'Ba vật tiếp xúc nhau với ba số đọc nhiệt độ');
  },
};
