// Hình minh hoạ ruột tập Vật lí 10 · Bài 24 Công suất (lesson 69). Cùng quy tắc hinh.mjs/hinh-ch4.mjs: mỗi hình trả lời MỘT câu hỏi,
// chữ ≥ 20 đơn vị viewBox (≈ 3 mm khi in rộng 46 mm), nét ≥ 2,8, phân biệt bằng NÉT (đặc – đứt – xám) chứ không chỉ bằng màu, tự vẽ.
// Chú thích hình ô Dự đoán chỉ mô tả cái em thấy, không nêu kết luận. Kiểm: chụp từng hình ở rộng 46 mm như xem-hinh.mjs (bản đó chỉ nạp hinh.mjs + hinh-ch4.mjs).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const arr = (x1, y1, x2, y2, id, c = INK, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${SW}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const rect = (x, y, w, h, o = '') => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="3" fill="#fff" stroke="${INK}" stroke-width="${SW}" ${o}/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') => `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
// mũi tên kích thước hai đầu (đo độ cao, quãng đường)
const kt = (x1, y1, x2, y2, id) => `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${GREY}" stroke-width="2.2" marker-start="url(#${id})" marker-end="url(#${id})"/>`;
const defs2 = (id) => `<defs><marker id="${id}" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto-start-reverse" markerUnits="strokeWidth"><path d="M0,0 L8,4 L0,8 z" fill="${GREY}"/></marker></defs>`;
const dat = (x1, x2, y) => ln(x1, y, x2, y) + Array.from({ length: Math.floor((x2 - x1) / 14) }, (_, i) => ln(x1 + 6 + i * 14, y, x1 + i * 14, y + 7, INK, 1.6)).join('');

export const hinhL10b24 = {
  // Trang 1 · Dự đoán: hai thang máy nâng cùng thùng lên cùng độ cao, thời gian khác nhau (không nêu kết luận)
  haiThangMay: (cap = 'Hai thang nâng cùng thùng 500 kg lên cao 20 m: A hết 10 s, B hết 20 s.') => {
    let b = defs('tm') + defs2('tmk');
    for (const [x, ten] of [[16, 'A'], [196, 'B']]) {
      b += ln(x, 14, x, 172, GREY, 2) + ln(x + 92, 14, x + 92, 172, GREY, 2);
      b += rect(x + 10, 20, 72, 46, `stroke-dasharray="6 4"`);
      b += rect(x + 10, 124, 72, 46) + T(x + 46, 154, '500 kg', { a: 'middle', size: 19 });
      b += arr(x + 46, 118, x + 46, 76, 'tm', INK, '6 4');
      b += T(x + 46, 202, ten, { a: 'middle', w: 700 });
    }
    b += dat(4, 304, 172);
    b += kt(126, 26, 126, 166, 'tmk') + T(136, 90, 'h', { w: 700 }) + T(136, 114, '20 m');
    return wrap('0 0 308 210', b, cap, 'Hai thang máy nâng cùng thùng hàng lên cùng độ cao');
  },
  // Trang 2 · Thí nghiệm leo cầu thang: cùng độ cao h, bấm giờ t
  cauThang: (cap = 'Leo cùng độ cao h = 3,0 m, bấm giờ từ chân tới đỉnh.') => {
    let b = defs('ct') + defs2('ctk');
    let d = 'M10,176';
    for (let i = 0; i < 5; i++) d += ` L${10 + i * 44},${176 - (i + 1) * 28} L${54 + i * 44},${176 - (i + 1) * 28}`;
    d += ' L230,176';
    b += `<path d="${d}" fill="#fff" stroke="${INK}" stroke-width="${SW}" stroke-linejoin="round"/>`;
    b += ln(4, 176, 300, 176);
    // người: đầu + thân ở bậc 1
    b += `<circle cx="34" cy="104" r="11" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + ln(34, 115, 34, 140) + ln(34, 140, 24, 148) + ln(34, 140, 44, 148) + ln(34, 122, 22, 132) + ln(34, 122, 46, 130);
    b += arr(60, 110, 196, 30, 'ct', INK, '6 4');
    b += kt(262, 36, 262, 172, 'ctk') + T(272, 98, 'h', { w: 700 });
    // đồng hồ bấm giờ
    b += `<circle cx="150" cy="140" r="20" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + ln(150, 120, 150, 113) + ln(144, 112, 156, 112) + ln(150, 140, 160, 130, RED, 2.6);
    b += T(178, 147, 't');
    return wrap('0 0 304 184', b, cap, 'Học sinh leo cầu thang cao h, bạn bấm giờ t');
  },
  // Trang 2 · P = F v: lực kéo lớn nhất theo vận tốc khi công suất giữ 6 kW (trục F không ghi số để HS tự tính bảng)
  duongFv: (cap = 'Công suất giữ 6 kW: đi càng nhanh, lực kéo lớn nhất càng nhỏ.') => {
    const X = (v) => 52 + v * 9, Y = (F) => 170 - F * 0.046;
    let b = defs('fv');
    b += arr(52, 170, 304, 170, 'fv') + arr(52, 170, 52, 12, 'fv');
    b += T(306, 152, 'v (m/s)', { a: 'end' }) + T(62, 24, 'F (N)');
    let d = '';
    for (let i = 0; i <= 40; i++) { const v = 2 + i * 0.5; d += `${i ? 'L' : 'M'}${X(v).toFixed(1)},${Y(6000 / v).toFixed(1)}`; }
    b += `<path d="${d}" fill="none" stroke="${RED}" stroke-width="${SW}"/>`;
    for (const v of [2, 5, 10, 20]) {
      b += ln(X(v), 170, X(v), Y(6000 / v), GREY, 1.8, '4 4') + `<circle cx="${X(v)}" cy="${Y(6000 / v)}" r="5.5" fill="${INK}"/>`;
      b += T(X(v), 194, String(v), { a: 'middle', size: 19 });
    }
    b += T(176, 104, 'P = 6 kW', { c: RED, w: 700 });
    return wrap('0 0 312 204', b, cap, 'Đồ thị lực kéo lớn nhất theo vận tốc khi công suất không đổi');
  },
  // Trang 3 · Bẫy 1: diện tích hình chữ nhật P·t = công; X cao mà hẹp, Y thấp mà rộng
  cotPt: (cap = 'Mỗi máy: chiều cao là P, chiều rộng là t. Diện tích là công A = P·t.') => {
    let b = defs('pt');
    const ax = (x0, x1) => arr(x0, 166, x1, 166, 'pt') + arr(x0, 166, x0, 14, 'pt') + T(x0 + 8, 26, 'P') + T(x1, 190, 't', { a: 'end' });
    b += ax(18, 92) + ax(116, 304);
    b += `<rect x="18" y="46" width="42" height="120" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(39, 112, 'X', { a: 'middle', w: 700 });
    b += `<rect x="116" y="128" width="174" height="38" fill="#fff" stroke="${INK}" stroke-width="${SW}" stroke-dasharray="7 4"/>` + T(203, 154, 'Y', { a: 'middle', w: 700 });
    b += T(36, 196, '10 s', { a: 'middle', size: 19 }) + T(203, 196, '100 s', { a: 'middle', size: 19 });
    b += T(70, 62, '5 kW', { size: 19 }) + T(203, 118, '1 kW', { a: 'middle', size: 19 });
    return wrap('0 0 308 202', b, cap, 'Hai hình chữ nhật: chiều cao công suất, chiều rộng thời gian');
  },
  // Trang 4 · Bài toán mẫu: nâng đều, F và mg dài bằng nhau
  cabin: (cap = 'Nâng đều 15 m trong 30 s: hai mũi tên lực dài bằng nhau.', m = '800 kg', h = '15 m') => {
    let b = defs('cb') + defs2('cbk');
    b += ln(20, 8, 20, 222, GREY, 2) + ln(150, 8, 150, 222, GREY, 2);
    b += rect(40, 90, 90, 56) + T(85, 125, m, { a: 'middle' });
    b += arr(85, 90, 85, 24, 'cb', RED) + T(96, 42, 'F', { c: RED, w: 700 });
    b += arr(85, 146, 85, 212, 'cb', BLUE, '6 4') + T(96, 204, 'mg', { c: BLUE, w: 700 });
    b += arr(178, 150, 178, 80, 'cb', GREY) + T(188, 122, 'v', { w: 700 });
    b += kt(230, 14, 230, 216, 'cbk') + T(240, 112, h);
    return wrap('0 0 292 226', b, cap, 'Cabin thang máy nâng đều: lực kéo F lên, trọng lực mg xuống');
  },
  // Thử thách / Dạng 5: xe lên dốc, lực kéo hướng lên dốc, lực cản và thành phần trọng lực hướng xuống dốc
  xeDoc: (cap = 'Lên dốc đều: lực kéo cân bằng lực cản cộng thành phần trọng lực dọc dốc.', ngang = '100 m', cao = '6 m') => {
    const a = Math.atan2(110, 290), c = Math.cos(a), s = Math.sin(a);
    const S = (x) => [10 + x * c, 190 - x * s];  // điểm trên mặt dốc cách chân x
    let b = defs('xd');
    b += `<path d="M10,190 L300,190 L300,80 z" fill="#fff" stroke="${INK}" stroke-width="${SW}" stroke-linejoin="round"/>`;
    const [cx, cy] = S(150), nx = -s, ny = -c;   // pháp tuyến hướng ra ngoài mặt dốc
    const C = [cx + nx * 20, cy + ny * 20];
    b += `<g transform="translate(${C[0].toFixed(1)},${C[1].toFixed(1)}) rotate(${(-a * 180 / Math.PI).toFixed(1)})"><rect x="-34" y="-17" width="68" height="34" rx="5" fill="#fff" stroke="${INK}" stroke-width="${SW}"/></g>`;
    const P = (k, dx) => [C[0] + c * k + dx * nx, C[1] - s * k + dx * ny];
    const [f1, f2] = [P(36, 0), P(100, 0)], [r1, r2] = [P(-36, 6), P(-96, 6)];
    b += arr(f1[0].toFixed(1), f1[1].toFixed(1), f2[0].toFixed(1), f2[1].toFixed(1), 'xd', RED) + T(f2[0] - 6, f2[1] - 14, `F${sb('k')}`, { c: RED, w: 700 });
    b += arr(r1[0].toFixed(1), r1[1].toFixed(1), r2[0].toFixed(1), r2[1].toFixed(1), 'xd', BLUE, '6 4');
    b += T(8, 108, `F${sb('c')} +`, { c: BLUE, size: 19 }) + T(8, 130, 'mg sin<tspan font-family="KaTeX_Math" font-style="italic">α</tspan>', { c: BLUE, size: 19 });
    b += T(250, 214, ngang, { a: 'middle', size: 19 }) + T(296, 146, cao, { a: 'end', size: 19 });
    return wrap('0 0 308 220', b, cap, 'Ô tô lên dốc: lực kéo lên dốc, lực cản và thành phần trọng lực xuống dốc');
  },
  // Dạng 2: kéo thùng trên sàn và nâng thùng lên giá
  keoNang: (cap = 'Kéo trên sàn: F cùng hướng đi. Nâng đều: lực nâng bằng mg.') => {
    let b = defs('kn') + defs2('knk');
    b += dat(4, 188, 160) + rect(16, 116, 48, 44) + arr(64, 138, 124, 138, 'kn', RED) + T(98, 128, 'F', { c: RED, w: 700 });
    b += kt(16, 182, 176, 182, 'knk') + T(96, 210, 'd', { a: 'middle', w: 700 });
    b += dat(200, 304, 160) + ln(296, 160, 296, 60) + ln(248, 60, 304, 60);
    b += rect(254, 18, 40, 40, 'stroke-dasharray="6 4"') + rect(208, 116, 40, 44);
    b += arr(228, 116, 228, 70, 'kn', RED) + T(212, 92, 'F', { c: RED, w: 700, a: 'end' });
    b += kt(282, 64, 282, 156, 'knk') + T(272, 114, 'h', { a: 'end', w: 700 });
    return wrap('0 0 308 218', b, cap, 'Kéo thùng trên sàn ngang và nâng thùng lên giá');
  },
  // Dạng 4: cần cẩu nâng đều kiện hàng
  canCau: (cap = 'Cần cẩu nâng đều: lực căng cáp bằng trọng lượng kiện.') => {
    let b = defs('cc') + defs2('cck');
    b += dat(4, 304, 200) + ln(50, 200, 50, 24) + ln(30, 200, 70, 200) + ln(14, 28, 290, 28) + ln(50, 24, 70, 44, INK, 2) + ln(14, 28, 14, 46);
    b += rect(4, 46, 22, 22) ;
    b += ln(210, 28, 210, 100, INK, 2) + rect(180, 100, 60, 40) + T(210, 128, 'm', { a: 'middle', w: 700 });
    b += arr(250, 120, 250, 70, 'cc', RED) + T(260, 84, 'F', { c: RED, w: 700 });
    b += arr(210, 140, 210, 192, 'cc', BLUE, '6 4') + T(222, 186, 'mg', { c: BLUE, w: 700 });
    b += kt(130, 44, 130, 196, 'cck') + T(140, 124, 'h', { w: 700 });
    return wrap('0 0 308 208', b, cap, 'Cần cẩu tháp nâng đều kiện vật liệu lên cao h');
  },
};
