// Hình minh hoạ cho ruột tập VL12 · Bài 3 Nội năng. Định luật 1 của nhiệt động lực học (lesson 4). Cùng quy tắc với hinh.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh. Không dùng chữ Hi Lạp (Δ) trong SVG: Source Sans 3 chỉ nạp latin/vietnamese.
// Xem thử: node scripts/ruot-tap/l12-bai3.mjs --hinh (chụp vào out/hinh-l12-bai3/).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
const arr = (x1, y1, x2, y2, id, c = INK, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${SW}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const rect = (x, y, w, h, o = {}) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${o.rx ?? 0}" fill="${o.f ?? '#fff'}" stroke="${o.c ?? INK}" stroke-width="${o.sw ?? SW}"/>`;
// chấm phân tử khí
const cham = (pts) => pts.map(([x, y]) => `<circle cx="${x}" cy="${y}" r="3.2" fill="${GREY}"/>`).join('');
// ngọn lửa nhỏ
const lua = (x, y) => `<path d="M${x - 16},${y} Q${x - 18},${y - 18} ${x - 6},${y - 30} Q${x - 4},${y - 16} ${x + 2},${y - 14} Q${x + 2},${y - 32} ${x + 10},${y - 38} Q${x + 22},${y - 16} ${x + 16},${y} Z" fill="#fff" stroke="${RED}" stroke-width="${SW}"/>`;

// Ấm nước: thân (x, y, w, h), vòi trái, quai phải, mức nước đứt
const am = (x, y, w, h) => `<path d="M${x + 4},${y + h * .35} L${x - 22},${y + 4}" stroke="${INK}" stroke-width="${SW + 2}" stroke-linecap="round"/>`
  + `<path d="M${x + w - 4},${y + 10} Q${x + w + 26},${y + h * .4} ${x + w - 4},${y + h * .8}" fill="none" stroke="${INK}" stroke-width="${SW}"/>`
  + rect(x, y, w, h, { rx: 12 }) + `<ellipse cx="${x + w / 2}" cy="${y}" rx="${w * .28}" ry="6" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
  + ln(x + 6, y + h * .3, x + w - 6, y + h * .3, BLUE, 2, '6 4');

// Chu trình tủ lạnh / điều hoà: máy nén (phải), dàn nóng (trên), van (trái), dàn lạnh (dưới)
const chuTrinh = (cap, o = {}) => {
  const { a = '150 J', qn = '450 J', ql = '?', id = 'ct' } = o;
  let b = defs(id + 'a') + defs(id + 'b') + defs(id + 'c') + defs(id + 'd');
  const bx = (x, y, s) => rect(x, y, 112, 40, { rx: 6 }) + T(x + 56, y + 27, s, { a: 'middle', w: 700 });
  b += bx(104, 60, 'dàn nóng') + bx(104, 180, 'dàn lạnh') + bx(214, 120, 'máy nén') + bx(4, 120, 'van');
  // vòng gas (đứt, xám) theo chiều: máy nén → dàn nóng → van → dàn lạnh → máy nén
  b += `<path d="M270,120 L270,80 L220,80" fill="none" stroke="${GREY}" stroke-width="2.4" stroke-dasharray="6 4" marker-end="url(#${id}d)"/>`
    + `<path d="M104,80 L60,80 L60,116" fill="none" stroke="${GREY}" stroke-width="2.4" stroke-dasharray="6 4" marker-end="url(#${id}d)"/>`
    + `<path d="M60,160 L60,200 L100,200" fill="none" stroke="${GREY}" stroke-width="2.4" stroke-dasharray="6 4" marker-end="url(#${id}d)"/>`
    + `<path d="M216,200 L270,200 L270,164" fill="none" stroke="${GREY}" stroke-width="2.4" stroke-dasharray="6 4" marker-end="url(#${id}d)"/>`;
  b += arr(160, 58, 160, 14, id + 'a', BLUE, '7 4') + T(170, 30, `toả ${qn}`, { c: BLUE, w: 700 });
  b += arr(396, 140, 332, 140, id + 'b', RED) + T(394, 130, 'công', { c: RED, w: 700, a: 'end' }) + T(394, 166, a, { c: RED, w: 700, a: 'end' });
  b += arr(160, 262, 160, 224, id + 'c', RED) + T(170, 256, `thu ${ql}`, { c: RED, w: 700 });
  return wrap('0 0 400 270', b, cap, 'Chu trình của gas trong tủ lạnh');
};

// Đồ thị nhiệt độ hai giai đoạn: phanh (tăng) rồi nguội
const haiGiaiDoan = (cap, o = {}) => {
  const { t0 = '25,0 °C', t1 = '45,0 °C', t2 = '25,0 °C', y2 = 92, id = 'gd' } = o;
  let b = defs(id);
  b += arr(84, 104, 84, 6, id) + arr(84, 104, 334, 104, id) + T(94, 20, 't') + T(334, 126, 'thời gian', { a: 'end' });
  b += ln(84, 30, 156, 30, GREY, 1.8, '4 4') + ln(84, 92, 104, 92, GREY, 1.8, '4 4');
  b += T(78, 37, t1, { a: 'end' }) + T(78, 99, t0, { a: 'end' });
  b += `<polyline points="104,92 156,30 286,${y2}" fill="none" stroke="${RED}" stroke-width="${SW}"/>`;
  b += [[104, 92], [156, 30], [286, y2]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="5" fill="${RED}"/>`).join('');
  b += T(124, 52, 'phanh', { a: 'end', w: 700 }) + T(208, 44, 'nguội', { w: 700 });
  if (t2 !== t0) b += T(290, y2 + 26, t2, { a: 'end' });
  return wrap('0 0 340 132', b, cap, 'Nhiệt độ đĩa phanh theo thời gian');
};

export const hinhL12b3 = {
  // ===== Trang học bài mới =====
  haiAm: (cap = 'Hai ấm cùng 60 °C, khác lượng nước.') => {
    let b = am(40, 104, 70, 64) + am(170, 46, 116, 122);
    b += T(75, 194, 'A: 200 g', { a: 'middle', w: 700 }) + T(228, 194, 'B: 2 kg', { a: 'middle', w: 700 });
    b += T(75, 92, '60 °C', { a: 'middle', c: RED, w: 700 }) + T(228, 32, '60 °C', { a: 'middle', c: RED, w: 700 });
    return wrap('0 0 300 204', b, cap, 'Hai ấm nước cùng nhiệt độ, khối lượng khác nhau');
  },
  haiCach: (cap = '(a) Ấn nhanh pit-tông. (b) Đặt bình lên bếp.') => {
    let b = defs('hc1');
    // (a) xilanh + pit-tông
    b += T(4, 24, '(a)', { w: 700 }) + `<path d="M40,60 L40,180 L120,180 L120,60" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
    b += rect(42, 92, 76, 14, { f: GREY, c: INK }) + ln(80, 92, 80, 40, INK, 5);
    b += arr(100, 30, 100, 82, 'hc1', RED) + T(108, 52, 'F', { c: RED, w: 700 });
    b += cham([[56, 124], [86, 118], [106, 132], [66, 152], [96, 160], [52, 170], [80, 140], [110, 168]]);
    // (b) bình nước trên bếp
    b += T(170, 24, '(b)', { w: 700 }) + `<path d="M196,70 L196,160 L286,160 L286,70" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
    b += ln(198, 92, 284, 92, BLUE, 2, '6 4') + lua(241, 194) + rect(186, 160, 110, 6, { f: INK });
    return wrap('0 0 300 200', b, cap, 'Hai cách làm khí, nước nóng lên');
  },
  bomXe: (cap = 'Sờ thân bơm ở 1, 2, 3 sau khi bơm nhanh.') => {
    let b = rect(110, 30, 50, 170, { rx: 4 }) + ln(90, 14, 180, 14, INK, 7) + ln(135, 14, 135, 74, INK, 5) + rect(112, 74, 46, 12, { f: GREY });
    b += `<path d="M135,200 Q135,224 180,214 L214,204" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<circle cx="252" cy="176" r="40" fill="#fff" stroke="${INK}" stroke-width="${SW + 3}"/><circle cx="252" cy="176" r="22" fill="none" stroke="${GREY}" stroke-width="2"/>`;
    b += [[60, 1], [130, 2], [186, 3]].map(([y, i]) => ln(100, y - 6, 110, y - 6, GREY, 2) + T(92, y, String(i), { a: 'end', w: 700 })).join('');
    b += T(170, 192, 'van', { a: 'end', size: 18 });
    return wrap('0 0 300 230', b, cap, 'Bơm xe đạp: ba vị trí sờ thân bơm');
  },
  joule: (cap = 'Quả nặng M rơi độ cao h, dây quay cánh khuấy trong bình nước cách nhiệt.') => {
    let b = defs('jl1');
    b += `<path d="M24,80 L24,206 L176,206 L176,80" fill="none" stroke="${INK}" stroke-width="${SW + 1}"/>` + ln(28, 100, 172, 100, BLUE, 2, '6 4');
    b += ln(96, 44, 96, 190, INK, 4) + rect(80, 34, 32, 22, { rx: 3 }) + rect(66, 136, 60, 10, { f: GREY }) + rect(66, 172, 60, 10, { f: GREY });
    b += ln(112, 44, 236, 44, INK, 2) + `<circle cx="244" cy="52" r="14" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + ln(258, 52, 258, 120, INK, 2);
    b += rect(240, 120, 36, 34, { rx: 3 }) + T(258, 144, 'M', { a: 'middle', w: 700 });
    b += arr(288, 128, 288, 196, 'jl1', RED) + T(294, 178, 'h', { c: RED, w: 700 });
    b += rect(146, 60, 10, 116, { rx: 5 }) + `<circle cx="151" cy="180" r="9" fill="${RED}" stroke="${INK}" stroke-width="2"/>`;
    b += T(26, 70, 'nước', { size: 18 }) + T(180, 92, 'nhiệt kế', { size: 18 });
    return wrap('0 0 310 214', b, cap, 'Thí nghiệm Joule: quả nặng quay cánh khuấy');
  },
  dauAQ: (cap = 'Năng lượng đi vào hệ mang dấu +, đi ra khỏi hệ mang dấu −.') => {
    let b = defs('da1') + defs('da2');
    b += rect(140, 40, 80, 120, { rx: 8, f: '#eef2fa' }) + T(180, 106, 'hệ', { a: 'middle', w: 700, size: 24 });
    b += arr(66, 70, 134, 70, 'da1', RED) + arr(66, 130, 134, 130, 'da1', RED);
    b += T(8, 77, 'A > 0', { c: RED, w: 700 }) + T(8, 137, 'Q > 0', { c: RED, w: 700 });
    b += arr(226, 70, 294, 70, 'da2', BLUE, '7 4') + arr(226, 130, 294, 130, 'da2', BLUE, '7 4');
    b += T(352, 77, 'A < 0', { c: BLUE, w: 700, a: 'end' }) + T(352, 137, 'Q < 0', { c: BLUE, w: 700, a: 'end' });
    b += T(8, 26, 'nhận vào', { c: RED, w: 700 }) + T(352, 26, 'mất đi', { c: BLUE, w: 700, a: 'end' });
    b += T(8, 186, 'nhận công, thu nhiệt', { size: 18 }) + T(352, 186, 'sinh công, toả nhiệt', { size: 18, a: 'end' });
    return wrap('0 0 360 196', b, cap, 'Quy ước dấu của A và Q');
  },
  satVaBe: (cap = 'Vật nào có nội năng lớn hơn?') => {
    let b = rect(34, 118, 34, 34, { f: GREY }) + T(51, 104, 'sắt', { a: 'middle', w: 700 }) + T(51, 82, '1000 °C', { a: 'middle', c: RED, w: 700 });
    b += `<path d="M118,70 L134,158 L276,158 L292,70" fill="none" stroke="${INK}" stroke-width="${SW}"/>` + ln(122, 92, 288, 92, BLUE, 2, '6 4');
    b += T(205, 128, 'bể nước', { a: 'middle', w: 700 }) + T(205, 56, '30 °C', { a: 'middle', c: BLUE, w: 700 });
    return wrap('0 0 300 168', b, cap, 'Miếng sắt nhỏ rất nóng và bể nước ấm');
  },
  bomMau: (cap = 'Hệ: khối khí trong ống bơm.') => {
    let b = defs('bm1') + defs('bm2');
    b += `<path d="M110,30 L110,190 L170,190 L170,30" fill="none" stroke="${INK}" stroke-width="${SW}"/>` + rect(112, 74, 56, 12, { f: GREY }) + ln(140, 74, 140, 14, INK, 5);
    b += cham([[124, 110], [150, 104], [160, 130], [128, 150], [152, 170], [120, 178], [140, 128]]);
    b += arr(90, 36, 90, 104, 'bm1', RED) + T(82, 64, 'công', { c: RED, w: 700, a: 'end' }) + T(82, 88, '60 J', { c: RED, w: 700, a: 'end' });
    b += arr(176, 150, 236, 150, 'bm2', BLUE, '7 4') + T(242, 142, 'nhiệt', { c: BLUE, w: 700 }) + T(242, 166, '15 J', { c: BLUE, w: 700 });
    return wrap('0 0 300 200', b, cap, 'Một lần ấn bơm: công vào khí, nhiệt ra ngoài');
  },
  // ===== Bài tập mẫu =====
  phanhD1: (cap = 'Phanh rồi nguội.') => haiGiaiDoan(cap, { id: 'pd1' }),
  khoanD4: (cap = 'Đặt dấu riêng cho đồng và cho nước.') => {
    let b = defs('kd1') + defs('kd2');
    b += `<path d="M30,70 L30,200 L230,200 L230,70" fill="none" stroke="${INK}" stroke-width="${SW + 1}"/>` + ln(34, 90, 226, 90, BLUE, 2, '6 4');
    b += rect(80, 130, 90, 54, { f: '#eef2fa' }) + T(125, 164, 'đồng', { a: 'middle', w: 700 });
    b += rect(112, 14, 26, 40, { rx: 3 }) + `<path d="M118,54 L118,110 L125,126 L132,110 L132,54" fill="#fff" stroke="${INK}" stroke-width="2.4"/>`;
    b += arr(160, 30, 160, 116, 'kd1', RED) + T(168, 60, 'A', { c: RED, w: 700 });
    b += arr(176, 156, 214, 156, 'kd2', BLUE, '7 4') + T(240, 146, 'Q', { c: BLUE, w: 700 }) + T(240, 170, '?', { c: BLUE, w: 700 });
    b += T(40, 118, 'nước', { size: 18 });
    return wrap('0 0 270 210', b, cap, 'Khoan khối đồng đặt trong cốc nước');
  },
  tuLanhD5: (cap = 'Mũi tên đứt: đường đi của gas.') => chuTrinh(cap, { id: 'tl5' }),
  // ===== Bài tương tự =====
  phanhTT: (cap = 'Đĩa thép: phanh rồi nguội.') => haiGiaiDoan(cap, { t0: '30,0 °C', t1: '50,0 °C', t2: '35,0 °C', y2: 76, id: 'ptt' }),
  dieuHoaTT: (cap = 'Điều hoà: dàn lạnh trong phòng, dàn nóng ngoài trời.') => chuTrinh(cap, { a: '200 J', qn: '?', ql: '600 J', id: 'dh' }),
};
