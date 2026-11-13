// Hình minh hoạ cho ruột tập VL10 · Bài 10 Sự rơi tự do (lesson 55). Cùng quy tắc với hinh.mjs/hinh-l10-bai23.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh. Xem thử: node scripts/ruot-tap/l10-bai10.mjs --hinh (chụp vào out/hinh-l10-bai10/).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const arr = (x1, y1, x2, y2, id, c = INK, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${SW}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const f1 = (v) => (+v).toFixed(1);
const dat = (x1, x2, y) => ln(x1, y, x2, y) + Array.from({ length: Math.floor((x2 - x1) / 18) }, (_, i) =>
  ln(x1 + 8 + i * 18, y, x1 + i * 18, y + 8, GREY, 1.8)).join('');
const bi = (x, y, r = 9) => `<circle cx="${x}" cy="${y}" r="${r}" fill="${GREY}" stroke="${INK}" stroke-width="${SW}"/>`;
const da = (x, y) => `<path d="M${x - 10},${y + 4} L${x - 6},${y - 8} L${x + 5},${y - 9} L${x + 11},${y + 2} L${x + 3},${y + 9} z" fill="${GREY}" stroke="${INK}" stroke-width="2.4"/>`;
// viên giấy vo: đa giác lởm chởm, nền trắng
const vienGiay = (x, y) => `<path d="M${x - 11},${y - 3} L${x - 6},${y - 11} L${x + 3},${y - 9} L${x + 11},${y - 5} L${x + 10},${y + 5} L${x + 2},${y + 11} L${x - 8},${y + 8} z" fill="#fff" stroke="${INK}" stroke-width="2.4"/><path d="M${x - 5},${y - 2} L${x + 4},${y + 3} M${x - 2},${y + 5} L${x + 5},${y - 4}" stroke="${GREY}" stroke-width="1.6" fill="none"/>`;
// ngoặc đứng (kích thước) bên phải đoạn y1..y2 tại x, nhãn ở giữa
const ngoac = (x, y1, y2, nhan, { c = INK, trai = false, dash = '' } = {}) => {
  const d = trai ? -8 : 8;
  return `<path d="M${x + d},${y1} L${x},${y1} L${x},${y2} L${x + d},${y2}" fill="none" stroke="${c}" stroke-width="2.4"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`
    + T(x + (trai ? -6 : 6) + d, (y1 + y2) / 2 + 7, nhan, { c, a: trai ? 'end' : 'start' });
};
// lông chim: cuống cong + phiến
const long = (x, y) => `<path d="M${x - 16},${y + 10} Q${x},${y - 2} ${x + 18},${y - 10}" fill="none" stroke="${INK}" stroke-width="2.2"/>`
  + `<path d="M${x - 10},${y + 6} Q${x - 2},${y - 14} ${x + 18},${y - 10} Q${x + 6},${y + 8} ${x - 10},${y + 6} z" fill="#fff" stroke="${INK}" stroke-width="2"/>`;

export const hinhL10b10 = {
  // Trang 1 · Dự đoán: viên giấy vo và hòn bi thả cùng lúc từ 1,5 m (không vẽ kết quả)
  giayBi: (cap = 'Viên giấy vo chặt và hòn bi, thả cùng lúc từ cùng độ cao 1,5 m.') => {
    let b = defs('gb1');
    b += dat(10, 232, 196);
    b += ln(30, 30, 30, 196, GREY, 2, '5 4') + ln(22, 30, 38, 30, GREY, 2) + T(40, 118, '1,5 m');
    b += vienGiay(118, 34) + T(118, 72, 'giấy vo', { a: 'middle' });
    b += bi(190, 34, 10) + T(190, 72, 'bi thép', { a: 'middle' });
    b += arr(118, 84, 118, 170, 'gb1', BLUE, '6 4') + arr(190, 84, 190, 170, 'gb1', BLUE, '6 4');
    b += T(154, 140, '?', { a: 'middle', w: 700, size: 26, c: BLUE });
    return wrap('0 0 240 206', b, cap, 'Viên giấy vo và hòn bi thả cùng lúc');
  },
  // Trang 1 · thí nghiệm: ống Newton, chụp cùng một lúc
  ongNewton: (cap = 'Chụp cùng lúc sau khi thả cả hai ống.') => {
    let b = '';
    const ong = (x, nhan) => `<rect x="${x}" y="8" width="70" height="130" rx="12" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(x + 35, 162, nhan, { a: 'middle' });
    b += ong(30, 'có khí') + ong(190, 'chân không');
    b += long(65, 44) + bi(65, 112);           // có không khí: lông còn cao, bi gần đáy
    b += long(210, 112) + bi(245, 112);        // chân không: cùng độ cao
    b += ln(30, 126, 260, 126, GREY, 2, '4 4');
    return wrap('0 0 300 170', b, cap, 'Ống Newton có không khí và chân không');
  },
  // Trang 2 · thí nghiệm dây dọi: ảnh chụp nhiều lần, vị trí sau mỗi 0,1 s (đọc số ở bảng bên)
  dayDoi: (cap = 'Bi rơi sát dây dọi. Chấm: vị trí bi sau mỗi 0,1 s.') => {
    const k = 1.5, y0 = 22, pos = [0, 4.9, 19.6, 44.1, 78.4, 122.5];
    let b = ln(60, 8, 60, 214, INK, 1.6) + `<path d="M54,214 L66,214 L60,228 z" fill="${INK}"/>` + T(18, 30, 'dây', { size: 20 });
    b += `<rect x="96" y="${y0}" width="22" height="${125 * k + 4}" fill="#fff" stroke="${INK}" stroke-width="2"/>`;
    [0, 50, 100].forEach((c) => { b += ln(96, y0 + c * k, 108, y0 + c * k, INK, 2) + T(124, y0 + c * k + 7, `${c} cm`); });
    for (let c = 10; c <= 120; c += 10) if (c % 50) b += ln(96, y0 + c * k, 102, y0 + c * k, INK, 1.4);
    pos.forEach((p) => { b += `<circle cx="72" cy="${f1(y0 + p * k)}" r="4" fill="${GREY}" stroke="${INK}" stroke-width="2"/>`; });
    return wrap('0 0 200 232', b, cap, 'Ảnh chụp nhiều lần bi rơi cạnh dây dọi');
  },
  // Trang 3 · đo g bằng cổng quang
  congQuang: (cap = 'Ngắt điện: bi rơi, đồng hồ bắt đầu đếm; bi qua cổng quang thì đồng hồ dừng.') => {
    let b = defs('cq1');
    b += ln(40, 12, 40, 214) + ln(20, 214, 120, 214);
    b += `<rect x="40" y="14" width="64" height="26" rx="3" fill="${GREY}" stroke="${INK}" stroke-width="${SW}"/>` + bi(72, 50, 9);
    b += T(112, 34, 'nam châm điện');
    b += `<path d="M44,150 L44,172 L104,172 L104,150" fill="none" stroke="${INK}" stroke-width="${SW}"/>` + ln(52, 160, 96, 160, RED, 2, '4 3');
    b += T(44, 198, 'cổng quang');
    b += ln(72, 62, 72, 156, BLUE, 2.2, '6 4');
    b += ngoac(150, 50, 160, 's', { c: BLUE });
    b += `<rect x="186" y="186" width="104" height="34" rx="4" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(238, 210, '_,_ _ _ s', { a: 'middle', w: 700 });
    b += T(238, 178, 'đồng hồ', { a: 'middle' });
    return wrap('0 0 300 226', b, cap, 'Đo gia tốc rơi bằng cổng quang');
  },
  // Trang 3 · Bẫy 2: "trong 3 giây đầu" và "trong giây thứ 3"
  giayThu: (cap = 'g = 9,8 m/s². Vị trí lúc t = 0, 1, 2, 3 s.') => {
    const k = 4, y0 = 16, pos = [0, 4.9, 19.6, 44.1];
    let b = ln(60, y0, 60, y0 + 46 * k, INK, 2.4);
    pos.forEach((p, i) => {
      const y = y0 + p * k;
      b += `<circle cx="60" cy="${f1(y)}" r="7" fill="${GREY}" stroke="${INK}" stroke-width="2"/>` + T(48, y + 7, `${i} s`, { a: 'end' });
      if (i) b += T(76, y + 7, `${String(p).replace('.', ',')} m`);
    });
    b += ngoac(170, y0, y0 + 44.1 * k, '3 s đầu');
    b += ngoac(266, y0 + 19.6 * k, y0 + 44.1 * k, 'giây', { c: RED }) + T(280, y0 + 32 * k + 30, 'thứ 3', { c: RED });
    return wrap('0 0 340 210', b, cap, 'Quãng đường trong 3 giây đầu và trong giây thứ 3');
  },
  // Trang 4 · bài toán mẫu: chậu hoa rơi từ ban công 20 m
  chauHoa: (cap = 'Gốc tại móc, chiều dương hướng xuống. “Giây cuối”: từ vị trí lúc t − 1 tới mặt đất.') => {
    let b = defs('ch1');
    b += dat(4, 312, 206);
    b += `<rect x="12" y="10" width="64" height="196" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    for (let y = 26; y < 196; y += 30) b += `<rect x="26" y="${y}" width="36" height="16" fill="#fff" stroke="${GREY}" stroke-width="1.6"/>`;
    b += ln(76, 22, 112, 22) + ln(104, 22, 104, 30, INK, 2);
    b += `<path d="M96,30 L112,30 L109,44 L99,44 z" fill="${GREY}" stroke="${INK}" stroke-width="2.2"/>`;
    b += ln(104, 50, 104, 200, BLUE, 2, '6 4');
    b += ln(96, 160, 160, 160, GREY, 2, '4 3') + T(164, 166, 'lúc t − 1');
    b += ngoac(126, 160, 206, '?', { c: RED });
    b += ngoac(250, 22, 206, '20 m');
    b += arr(150, 40, 150, 92, 'ch1', INK) + T(160, 72, '+');
    return wrap('0 0 318 216', b, cap, 'Chậu hoa rơi từ ban công');
  },
  // Trang 5 · thử thách: thước đo phản xạ
  thuoc: (cap = 'Bạn buông thước, em bắt. Thước rơi được bao nhiêu thì em bắt kịp?') => {
    let b = `<rect x="70" y="10" width="34" height="196" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    for (let i = 0; i <= 18; i++) b += ln(70, 18 + i * 10, i % 5 ? 78 : 86, 18 + i * 10, INK, 1.4);
    // ngón cái + ngón trỏ ở vạch 0 (lúc buông) — vẽ bằng hai cung
    b += `<path d="M38,150 Q60,140 66,150 Q60,160 38,158" fill="#fff" stroke="${INK}" stroke-width="2.4"/><path d="M136,150 Q114,140 108,150 Q114,160 136,158" fill="#fff" stroke="${INK}" stroke-width="2.4"/>`;
    b += T(4, 186, 'tay em', { size: 20 });
    b += ngoac(150, 18, 150, 'đoạn rơi', { c: BLUE }) ;
    return wrap('0 0 250 214', b, cap, 'Thước đo thời gian phản xạ');
  },
  // ===== Bài tập mẫu =====
  // Dạng 1: thả đá từ cầu, rơi 4,0 s
  cauSong: (cap = 'Thả nhẹ từ mép cầu.') => {
    let b = defs('cs1');
    b += `<rect x="10" y="30" width="170" height="16" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + ln(150, 46, 150, 200) + ln(170, 46, 170, 200);
    b += da(196, 36) + arr(196, 52, 196, 186, 'cs1', BLUE, '6 4');
    b += `<path d="M120,200 q12,-8 24,0 t24,0 t24,0 t24,0 t24,0" fill="none" stroke="${INK}" stroke-width="2.4"/>`;
    b += ngoac(240, 36, 200, 'h = ?') + T(14, 74, 'cầu') + T(14, 196, 'sông');
    return wrap('0 0 310 210', b, cap, 'Hòn đá thả từ cầu xuống sông');
  },
  // Dạng 3: viên sỏi rơi từ cửa sổ, biết quãng giây cuối
  toaNha: (cap = 'Biết quãng giây cuối: tìm t trước.') => {
    let b = '';
    b += dat(4, 300, 118) + `<rect x="10" y="6" width="70" height="112" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<rect x="54" y="12" width="26" height="24" fill="#fff" stroke="${INK}" stroke-width="2"/>` + `<circle cx="94" cy="24" r="7" fill="${GREY}" stroke="${INK}" stroke-width="2"/>`;
    b += ln(94, 34, 94, 114, BLUE, 2, '6 4') + ln(86, 70, 160, 70, GREY, 2, '4 3');
    b += ngoac(120, 70, 118, '', { c: RED }) + T(136, 88, 'giây cuối', { c: RED }) + T(136, 108, '24,5 m', { c: RED });
    b += ngoac(250, 24, 118, 'h = ?');
    return wrap('0 0 310 126', b, cap, 'Viên sỏi rơi từ cửa sổ');
  },
  // Dạng 4: rơi + truyền âm
  hang: (cap = 'Đá rơi xuống mất t<sub>1</sub>, tiếng động đi lên mất t<sub>2</sub>.', { tong = `t${sb('1')} + t${sb('2')} = 4,25 s` } = {}) => {
    let b = defs('hg1') + defs('hg2');
    b += `<path d="M10,40 L100,40 L100,206 L200,206 L200,40 L300,40" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
    for (let y = 56; y < 206; y += 22) b += ln(100, y, 92, y + 10, GREY, 1.8) + ln(200, y, 208, y + 10, GREY, 1.8);
    b += da(130, 54) + arr(130, 68, 130, 192, 'hg1', INK, '6 4') + T(118, 140, `t${sb('1')}`, { a: 'end' });
    b += arr(172, 192, 172, 62, 'hg2', BLUE) + T(184, 140, `t${sb('2')}`, { c: BLUE });
    b += `<path d="M160,56 q12,-8 24,0 M156,46 q16,-11 32,0" fill="none" stroke="${BLUE}" stroke-width="2"/>`;
    b += T(150, 26, tong, { a: 'middle', w: 700 });
    return wrap('0 0 310 214', b, cap, 'Hòn đá rơi xuống hang và tiếng vọng lên');
  },
  // Dạng 5: hai bi thả cách nhau 1 s
  haiBi: (cap = 'Bi A thả trước 1 s. Khi A rơi được t giây thì B rơi được bao lâu?', { tre = '1 s' } = {}) => {
    let b = '';
    b += ln(30, 24, 120, 24) + ln(75, 24, 75, 210, GREY, 2, '5 4');
    b += bi(75, 74) + T(92, 80, 'B') + bi(75, 170) + T(92, 176, 'A');
    b += ngoac(150, 74, 170, 'd = ?', { c: RED });
    b += T(150, 30, `thả B sau A ${tre}`);
    return wrap('0 0 310 216', b, cap, 'Hai bi thả cách nhau một khoảng thời gian');
  },
};
