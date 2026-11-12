// Hình minh hoạ cho ruột tập Vật lí 10 · Bài 29 Định luật bảo toàn động lượng (lesson 74). Cùng quy tắc với hinh.mjs: mỗi hình trả
// lời MỘT câu hỏi (H1), chữ ≥ 20 đơn vị viewBox (≈ 3 mm khi in rộng 46 mm), nét ≥ 2,8, phân biệt bằng NÉT/HÌNH chứ không chỉ màu (in
// đen–trắng), tự vẽ. Chỗ HS phải tính để dấu "?" (không lộ đáp số; hình cạnh ô Dự đoán chỉ vẽ lúc TRƯỚC cú ôm).
// Chữ Hi Lạp trong SVG gắn font KaTeX_Math (Source Sans 3 bản cắt không có Greek). Mỗi hình dùng id marker riêng (cùng trang HTML).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`; // chỉ số dưới
const LIGHT = '#dfe7f5';
const arr = (x1, y1, x2, y2, id, c = INK, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${SW}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
// Xe trên ray: thân (x, y) rộng w cao 34, bánh ở dưới; nhãn khối lượng trong thân
const xe = (x, y, w, ten = '', fill = LIGHT) => `<rect x="${x}" y="${y}" width="${w}" height="34" rx="4" fill="${fill}" stroke="${INK}" stroke-width="${SW}"/>`
  + `<circle cx="${x + 16}" cy="${y + 40}" r="6" fill="#fff" stroke="${INK}" stroke-width="2.4"/><circle cx="${x + w - 16}" cy="${y + 40}" r="6" fill="#fff" stroke="${INK}" stroke-width="2.4"/>`
  + (ten ? T(x + w / 2, y + 24, ten, { a: 'middle', w: 700 }) : '');
const ray = (x1, x2, y) => `<line x1="${x1}" y1="${y}" x2="${x2}" y2="${y}" stroke="${INK}" stroke-width="${SW}"/>`;
// Người que: đầu ở (x, y), cao ≈ 78
const nguoi = (x, y) => `<circle cx="${x}" cy="${y}" r="11" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
  + `<path d="M${x},${y + 11} L${x},${y + 46} M${x - 16},${y + 28} L${x + 16},${y + 28} M${x},${y + 46} L${x - 12},${y + 76} M${x},${y + 46} L${x + 12},${y + 76}" fill="none" stroke="${INK}" stroke-width="${SW}" stroke-linecap="round"/>`;
// Trục chiều dương
const truc = (x1, x2, y, id) => arr(x1, y, x2, y, id, GREY) + T(x2 - 6, y - 8, '+', { a: 'end', w: 700, c: GREY });

export const hinhBai29 = {
  // Trang 1 · Dự đoán: chỉ vẽ lúc TRƯỚC cú ôm (không vẽ mũi tên sau ôm → không lộ đáp án)
  omNhau: (cap = 'Trước cú ôm: An trượt tới, Bình đứng yên. Mặt băng gần như không ma sát.') => {
    let b = defs('on1');
    b += `<line x1="6" y1="130" x2="304" y2="130" stroke="${INK}" stroke-width="${SW}"/>`;
    for (let x = 20; x < 300; x += 28) b += `<line x1="${x}" y1="136" x2="${x + 12}" y2="136" stroke="${GREY}" stroke-width="2"/>`;
    b += nguoi(64, 52) + nguoi(238, 52);
    b += T(64, 28, 'An', { a: 'middle', w: 700 }) + T(238, 28, 'Bình', { a: 'middle', w: 700 });
    b += arr(92, 78, 168, 78, 'on1') + T(130, 66, '4 m/s', { a: 'middle' });
    b += T(238, 160, 'đứng yên', { a: 'middle' }) + T(64, 160, '50 kg', { a: 'middle' }) + T(238, 182, '50 kg', { a: 'middle' });
    return wrap('0 0 310 190', b, cap, 'An trượt tới Bình đang đứng yên');
  },
  // Trang 1 · II.1: hệ hai xe trên ray đệm khí — ngoại lực (nét liền) cân bằng, nội lực (nét đứt) ở chỗ tiếp xúc
  heKin: (cap = 'Hệ hai xe trên ray đệm khí. Nét liền: lực do vật ngoài hệ. Nét đứt: lực hai xe đẩy nhau.') => {
    let b = defs('hk1') + defs('hk2');
    b += `<rect x="6" y="150" width="288" height="12" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    for (let x = 24; x < 290; x += 24) b += `<circle cx="${x}" cy="156" r="2.4" fill="${INK}"/>`;
    b += `<rect x="40" y="104" width="100" height="40" rx="4" fill="${LIGHT}" stroke="${INK}" stroke-width="${SW}"/>` + T(90, 130, 'xe 1', { a: 'middle', w: 700 });
    b += `<rect x="140" y="104" width="100" height="40" rx="4" fill="${LIGHT}" stroke="${INK}" stroke-width="${SW}"/>` + T(190, 130, 'xe 2', { a: 'middle', w: 700 });
    // ngoại lực: trọng lực xuống, lực đỡ của đệm khí lên, dài bằng nhau
    for (const x of [58, 222]) { b += arr(x, 124, x, 190, 'hk1') + arr(x, 124, x, 58, 'hk1'); }
    b += T(64, 64, 'N') + T(228, 64, 'N') + T(32, 190, 'P') + T(196, 190, 'P');
    // nội lực
    b += arr(140, 92, 100, 92, 'hk2', RED, '6 4') + arr(140, 92, 180, 92, 'hk2', RED, '6 4');
    b += T(98, 30, `F${sb('21')}`, { c: RED }) + T(166, 30, `F${sb('12')}`, { c: RED });
    b += `<line x1="112" y1="36" x2="112" y2="84" stroke="${RED}" stroke-width="1.4"/><line x1="170" y1="36" x2="170" y2="84" stroke="${RED}" stroke-width="1.4"/>`;
    return wrap('0 0 300 206', b, cap, 'Ngoại lực và nội lực của hệ hai xe');
  },
  // Trang 2 · thí nghiệm ray đệm khí, hai cổng quang
  rayDem: (cap = 'Xe 1 gắn kim, xe 2 gắn sáp. Cổng 1 đo v<sub>1</sub>; cổng 2 đo v khi hai xe đã dính.') => {
    let b = defs('rd1');
    b += `<rect x="4" y="112" width="302" height="10" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    for (const [x, n] of [[100, '1'], [266, '2']]) {
      b += `<rect x="${x - 4}" y="30" width="8" height="82" fill="${INK}"/><line x1="${x}" y1="40" x2="${x}" y2="104" stroke="${RED}" stroke-width="2" stroke-dasharray="4 3"/>`;
      b += T(x, 22, `cổng ${n}`, { a: 'middle' });
    }
    b += xe(14, 70, 66, 'xe 1') + `<line x1="80" y1="86" x2="94" y2="86" stroke="${INK}" stroke-width="2.4"/>`;
    b += `<path d="M164,74 a6,6 0 0 0 0,24 Z" fill="${GREY}"/>` + xe(164, 70, 66, 'xe 2', '#fff');
    b += arr(24, 52, 74, 52, 'rd1') + T(18, 44, `v${sb('1')}`, { w: 700 });
    return wrap('0 0 310 132', b, cap, 'Ray đệm khí với hai cổng quang');
  },
  // Trang 2 · II.3: hai kiểu va chạm, trước → sau (không ghi số, chỉ hình dạng)
  haiVaCham: (cap = 'Hàng trên: hai xe dính nhau. Hàng dưới: hai xe có đệm lò xo, bật ra.') => {
    let b = defs('vc1');
    // hàng 1 · mềm
    b += T(4, 20, 'mềm', { w: 700 });
    b += xe(64, 6, 54) + `<rect x="118" y="14" width="8" height="18" fill="${GREY}"/>` + xe(126, 6, 54) + arr(192, 23, 250, 23, 'vc1') + T(256, 30, 'v');
    b += ray(64, 300, 54);
    // hàng 2 · đàn hồi
    b += T(4, 94, 'đàn', { w: 700 }) + T(4, 116, 'hồi', { w: 700 });
    b += xe(64, 80, 54) + `<path d="M118,97 q6,-10 12,0 q6,10 12,0" fill="none" stroke="${INK}" stroke-width="2.4"/>` + xe(166, 80, 54);
    b += arr(91, 74, 70, 74, 'vc1', INK, '5 3') + T(94, 70, `v${sb('1')}'`) + arr(193, 74, 250, 74, 'vc1') + T(256, 80, `v${sb('2')}'`);
    b += ray(64, 300, 128);
    return wrap('0 0 306 136', b, cap, 'Va chạm mềm và va chạm đàn hồi');
  },
  // Trang 3 · II.4: tên lửa đứng yên rồi phụt khí — vận tốc tên lửa để "?"
  tenLua: (cap = 'Tên lửa đứng yên rồi phụt khí về sau.') => {
    let b = defs('tl1');
    b += `<path d="M120,46 L230,46 L282,66 L230,86 L120,86 Z" fill="${LIGHT}" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<path d="M120,46 L100,30 L100,46 Z M120,86 L100,102 L100,86 Z" fill="#fff" stroke="${INK}" stroke-width="2.4"/>`;
    b += T(176, 74, 'M', { a: 'middle', w: 700 });
    for (const [x, y, r] of [[86, 66, 12], [62, 58, 9], [58, 78, 10], [36, 68, 8]]) b += `<circle cx="${x}" cy="${y}" r="${r}" fill="#fff" stroke="${GREY}" stroke-width="2.4" stroke-dasharray="4 3"/>`;
    b += T(52, 110, 'khí m', { a: 'middle' });
    b += arr(70, 26, 14, 26, 'tl1', RED) + T(76, 32, 'v', { c: RED, w: 700 });
    b += arr(200, 122, 260, 122, 'tl1') + T(196, 128, 'V = ?', { a: 'end', w: 700 });
    return wrap('0 0 300 136', b, cap, 'Tên lửa phụt khí');
  },
  // Trang 3 · Bẫy 1: chọn chiều dương, hai vật chạy ngược nhau
  chieuDuong: (cap = 'Chọn chiều dương trước; đề chỉ cho tốc độ (số dương).') => {
    let b = defs('cd1') + defs('cd2');
    b += truc(10, 290, 24, 'cd1');
    b += `<circle cx="70" cy="86" r="24" fill="${LIGHT}" stroke="${INK}" stroke-width="${SW}"/>` + T(70, 93, 'A', { a: 'middle', w: 700 });
    b += `<circle cx="230" cy="86" r="24" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(230, 93, 'B', { a: 'middle', w: 700 });
    b += arr(100, 86, 150, 86, 'cd2') + arr(200, 86, 156, 86, 'cd2', INK, '6 4');
    b += T(70, 140, `v${sb('A')} = …`, { a: 'middle' }) + T(230, 140, `v${sb('B')} = …`, { a: 'middle' });
    return wrap('0 0 300 150', b, cap, 'Chọn chiều dương cho hai vật ngược chiều');
  },
  // Trang 4 · bài toán mẫu: hai cầu thủ khúc côn cầu
  cauThu: (cap = 'Hai cầu thủ lao vào nhau trên một đường thẳng.') => {
    let b = defs('ct1') + defs('ct2');
    b += truc(10, 290, 22, 'ct1');
    b += nguoi(70, 60) + nguoi(230, 60);
    b += `<line x1="6" y1="140" x2="294" y2="140" stroke="${INK}" stroke-width="${SW}"/>`;
    b += arr(96, 84, 150, 84, 'ct2') + T(124, 74, '6 m/s', { a: 'middle' });
    b += arr(204, 84, 164, 84, 'ct2', INK, '6 4') + T(186, 112, '3 m/s', { a: 'middle' });
    b += T(70, 166, 'A · 80 kg', { a: 'middle', w: 700 }) + T(230, 166, 'B · 100 kg', { a: 'middle', w: 700 });
    return wrap('0 0 300 176', b, cap, 'Hai cầu thủ chạy ngược chiều');
  },
  // Trang 5 · thử thách ★★★: đá rơi chéo vào xe cát
  xeCat: (cap = 'Ray chỉ đỡ theo phương đứng.') => {
    let b = defs('xc1') + defs('xc2');
    b += `<path d="M40,104 L60,140 L190,140 L210,104 Z" fill="#fff" stroke="${INK}" stroke-width="${SW}"/><path d="M48,108 Q125,96 202,108" fill="none" stroke="${GREY}" stroke-width="2.4"/>`;
    b += `<circle cx="80" cy="148" r="8" fill="#fff" stroke="${INK}" stroke-width="2.4"/><circle cx="170" cy="148" r="8" fill="#fff" stroke="${INK}" stroke-width="2.4"/>`;
    b += ray(4, 296, 156) + T(125, 132, '50 kg', { a: 'middle', w: 700 });
    b += arr(214, 126, 270, 126, 'xc1') + T(222, 116, '2 m/s');
    // hòn đá: vận tốc chếch xuống 60°, thành phần ngang ngược chiều xe
    const A = (60 * Math.PI) / 180, x0 = 238, y0 = 14, L = 78;
    b += `<circle cx="${x0}" cy="${y0 + 4}" r="10" fill="${GREY}" stroke="${INK}" stroke-width="2"/>` + T(x0 + 16, y0 + 12, '10 kg');
    b += arr(x0, y0 + 14, (x0 - L * Math.cos(A)).toFixed(1), (y0 + 14 + L * Math.sin(A)).toFixed(1), 'xc2', RED) + T(x0 - 14, y0 + 62, '6 m/s', { c: RED });
    b += `<line x1="${x0}" y1="${y0 + 14}" x2="${x0 - 60}" y2="${y0 + 14}" stroke="${GREY}" stroke-width="2" stroke-dasharray="4 3"/>`;
    b += `<path d="M${x0 - 34},${y0 + 14} A34,34 0 0 0 ${(x0 - 34 * Math.cos(A)).toFixed(1)},${(y0 + 14 + 34 * Math.sin(A)).toFixed(1)}" fill="none" stroke="${INK}" stroke-width="2"/>` + T(x0 - 66, y0 + 6, '60°');
    return wrap('0 0 300 166', b, cap, 'Hòn đá rơi chéo vào xe cát');
  },
  // Dạng 1: hai xe trên ray đệm khí, trước và sau va chạm
  d1: (cap = 'Trên: trước va chạm. Dưới: ngay sau.') => {
    let b = defs('d11');
    b += xe(10, 22, 112, '0,30 kg') + xe(170, 22, 112, '0,20 kg', '#fff') + ray(4, 296, 70);
    b += arr(40, 12, 96, 12, 'd11') + T(102, 18, '0,60 m/s') + T(226, 14, 'đứng yên', { a: 'middle' });
    b += xe(10, 96, 112, '0,30 kg') + xe(170, 96, 112, '0,20 kg', '#fff') + ray(4, 296, 144);
    b += T(66, 88, `v${sb('1')}' = ?`, { a: 'middle', w: 700 }) + arr(190, 82, 240, 82, 'd11') + T(246, 88, '0,45 m/s');
    return wrap('0 0 330 150', b, cap, 'Hai xe trước và sau va chạm');
  },
  // Dạng 4: hai goòng ngược chiều
  goong: (cap = 'Hai goòng chạy ngược chiều rồi móc dính.') => {
    let b = defs('go1');
    b += xe(10, 50, 116, '900 kg') + xe(174, 50, 116, '600 kg', '#fff') + ray(4, 296, 98);
    b += arr(40, 30, 100, 30, 'go1') + T(70, 20, '2,0 m/s', { a: 'middle' }) + T(68, 128, 'A', { a: 'middle', w: 700 });
    b += arr(262, 30, 214, 30, 'go1', INK, '6 4') + T(232, 20, '1,0 m/s', { a: 'middle' }) + T(232, 128, 'B', { a: 'middle', w: 700 });
    return wrap('0 0 300 136', b, cap, 'Hai goòng ngược chiều');
  },
  // Dạng 5: súng giật — vận tốc súng để "?"
  sung: (cap = 'Súng đặt tự do, bắn đạn theo phương ngang.') => {
    let b = defs('sg1');
    b += `<path d="M30,70 L70,58 L210,58 L210,74 L110,74 L96,104 L74,104 L80,80 L36,92 Z" fill="${LIGHT}" stroke="${INK}" stroke-width="${SW}" stroke-linejoin="round"/>`;
    b += T(124, 52, '2,5 kg', { a: 'middle', w: 700 }) + ray(4, 296, 120);
    b += `<ellipse cx="236" cy="66" rx="10" ry="5" fill="${INK}"/>` + arr(252, 66, 292, 66, 'sg1', RED) + T(272, 100, '10 g', { a: 'middle', c: RED }) + T(262, 44, '400 m/s', { a: 'middle', c: RED });
    b += T(48, 144, 'súng: V = ?', { w: 700 });
    return wrap('0 0 300 152', b, cap, 'Súng bắn đạn');
  },
};
