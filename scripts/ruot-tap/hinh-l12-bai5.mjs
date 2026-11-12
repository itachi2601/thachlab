// Hình minh hoạ cho ruột tập VL12 · Bài 5 Thuyết động học phân tử chất khí (lesson 6). Cùng quy tắc với hinh.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh. Xem thử: node scripts/ruot-tap/l12-bai5.mjs --hinh (chụp vào out/hinh-l12-bai5/).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const sp = (s) => `<tspan font-size="14" dy="-9">${s}</tspan><tspan dy="9"> </tspan>`;
const arr = (x1, y1, x2, y2, id, c = INK, dash = '', w = SW) =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const rect = (x, y, w, h, o = {}) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${o.rx ?? 4}" fill="${o.fill ?? '#fff'}" stroke="${o.c ?? INK}" stroke-width="${o.sw ?? SW}"${o.dash ? ` stroke-dasharray="${o.dash}"` : ''}/>`;
const dot = (x, y, r = 4, c = INK) => `<circle cx="${x}" cy="${y}" r="${r}" fill="${c}"/>`;
const doan = (x1, x2, y, nhan) => ln(x1, y, x2, y, GREY, 2) + ln(x1, y - 6, x1, y + 6, GREY, 2) + ln(x2, y - 6, x2, y + 6, GREY, 2)
  + T((x1 + x2) / 2, y - 7, nhan, { a: 'middle' });
const N2 = `N${sb('2')}`, O2 = `O${sb('2')}`, CO2 = `CO${sb('2')}`, H2 = `H${sb('2')}`;
const gk = (ch, f = 'KaTeX_Math') => `<tspan font-family="${f}"${f === 'KaTeX_Math' ? ' font-style="italic"' : ''}>${ch}</tspan>`;
const NA = `6,02·10${sp('23')}`;

// Bình kín: n phân tử (chấm) có mũi tên vận tốc ngắn, hướng lộn xộn (giả ngẫu nhiên cố định)
const binh = (x, y, w, h, n, id, seed = 7) => {
  let s = seed, b = rect(x, y, w, h, { rx: 6 });
  const r = () => (s = (s * 9301 + 49297) % 233280) / 233280;
  for (let i = 0; i < n; i++) {
    const px = x + 16 + r() * (w - 32), py = y + 16 + r() * (h - 32), a = r() * 2 * Math.PI, L = 16 + r() * 10;
    b += dot(px, py, 4) + arr(px, py, (px + L * Math.cos(a)).toFixed(1), (py + L * Math.sin(a)).toFixed(1), id, INK, '', 2);
  }
  return b;
};

export const hinhL12b5 = {
  // ===== Trang học bài mới =====
  // Dự đoán: chỉ vẽ dụng cụ và các chấm sáng đứng tại chỗ, KHÔNG vẽ quỹ đạo (đáp án D)
  hopKhoi: (cap = 'Hộp kín chứa khói, đèn rọi ngang, nhìn qua kính lúp.') => {
    let b = rect(70, 70, 190, 110, { rx: 4 }) + T(165, 202, 'hộp kín', { a: 'middle' });
    b += rect(4, 108, 40, 34, { rx: 4 }) + T(24, 168, 'đèn', { a: 'middle' });
    b += [112, 125, 138].map((y) => ln(46, y, 66, y + (y - 125) * .4, GREY, 2, '6 4')).join('');
    [[110, 100], [150, 140], [196, 96], [226, 150], [130, 160], [240, 112], [180, 122]].forEach(([x, y]) => { b += dot(x, y, 4.5); });
    b += `<circle cx="196" cy="34" r="24" fill="none" stroke="${INK}" stroke-width="${SW}"/>` + ln(213, 51, 236, 70, INK, 6);
    b += T(150, 30, 'kính lúp', { a: 'end' });
    return wrap('0 0 280 210', b, cap, 'Hộp kín chứa khói hương, đèn rọi ngang và kính lúp');
  },
  vaDap: (cap = 'Phân tử khí (chấm nhỏ) va vào hạt khói từ mọi phía.') => {
    let b = defs('vd1') + `<circle cx="150" cy="96" r="36" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(150, 103, 'hạt khói', { a: 'middle', size: 18, w: 700 });
    const tia = [[0, 60], [40, 34], [95, 52], [150, 28], [200, 56], [250, 40], [300, 64], [330, 30]];
    tia.forEach(([d, L]) => {
      const a = d * Math.PI / 180, x2 = 150 + 40 * Math.cos(a), y2 = 96 + 40 * Math.sin(a), x1 = 150 + (40 + L) * Math.cos(a), y1 = 96 + (40 + L) * Math.sin(a);
      b += dot(x1.toFixed(1), y1.toFixed(1), 5) + arr(x1.toFixed(1), y1.toFixed(1), x2.toFixed(1), y2.toFixed(1), 'vd1', RED, '', 2.4);
    });
    return wrap('0 0 300 192', b, cap, 'Phân tử khí va đập vào hạt khói từ mọi phía');
  },
  baNoiDung: (cap = 'Chấm: phân tử · mũi tên: vận tốc · F: lực phân tử tác dụng lên thành.') => {
    let b = defs('bn1') + defs('bn2') + binh(10, 14, 220, 160, 9, 'bn1', 11);
    b += dot(214, 80, 4) + arr(190, 64, 212, 79, 'bn1', INK, '', 2);
    b += arr(232, 80, 280, 80, 'bn2', RED) + T(270, 66, 'F', { c: RED, w: 700, a: 'middle' });
    return wrap('0 0 300 186', b, cap, 'Phân tử khí trong bình chuyển động hỗn loạn và va vào thành');
  },
  ongKhoi: (cap = 'Ống dài 40 cm nằm ngang; x: khoảng cách từ đầu NH<sub>3</sub> tới vòng khói trắng.') => {
    let b = rect(14, 40, 292, 44, { rx: 20 });
    b += rect(18, 46, 28, 32, { rx: 8, fill: '#eef2fa', sw: 2 }) + rect(274, 46, 28, 32, { rx: 8, fill: '#eef2fa', sw: 2 });
    b += T(32, 26, `NH${sb('3')}`, { a: 'middle', w: 700 }) + T(288, 26, 'HCl', { a: 'middle', w: 700 });
    b += `<ellipse cx="190" cy="62" rx="7" ry="20" fill="#fff" stroke="${INK}" stroke-width="2" stroke-dasharray="4 3"/>`;
    b += doan(32, 190, 112, 'x') + doan(32, 288, 148, '40 cm');
    return wrap('0 0 320 160', b, cap, 'Ống thuỷ tinh khuếch tán NH3 và HCl');
  },
  vaThanh: (cap = 'Tới: nét liền; bật ra: nét đứt. v<sub>x</sub> vuông góc thành, v<sub>y</sub> dọc thành.') => {
    let b = defs('vt1') + defs('vt2') + defs('vt3');
    b += ln(240, 10, 240, 180, INK, 5) + Array.from({ length: 9 }, (_, i) => ln(240, 18 + i * 18, 254, 8 + i * 18, GREY, 1.8)).join('');
    b += dot(232, 96, 6);
    b += arr(110, 26, 228, 92, 'vt1', INK) + T(176, 86, 'v', { w: 700 });
    b += arr(232, 96, 114, 162, 'vt2', INK, '7 5') + T(180, 160, `v${gk('′', 'KaTeX_Main')}`, { w: 700 });
    b += arr(110, 26, 222, 26, 'vt3', RED, '', 2.4) + T(160, 18, `v${sb('x')}`, { c: RED, w: 700 });
    b += arr(110, 26, 110, 92, 'vt3', BLUE, '', 2.4) + T(100, 70, `v${sb('y')}`, { c: BLUE, w: 700, a: 'end' });
    b += T(250, 196, 'thành', { a: 'end' });
    return wrap('0 0 280 204', b, cap, 'Phân tử va chạm đàn hồi với thành bình');
  },
  thung1mol: (cap = `Cùng 1 mol, cùng điều kiện: thể tích và số phân tử ba thùng so với nhau thế nào?`) => {
    let b = '';
    [[N2, '28 g'], [O2, '32 g'], [CO2, '44 g']].forEach(([s, kg], i) => {
      const x = 8 + i * 102;
      b += rect(x, 30, 90, 96, { rx: 6 }) + T(x + 45, 72, s, { a: 'middle', w: 700, size: 24 }) + T(x + 45, 108, kg, { a: 'middle' });
    });
    b += T(155, 20, 'Mỗi thùng: 1 mol khí ở đktc', { a: 'middle' });
    return wrap('0 0 312 134', b, cap, 'Ba thùng 1 mol khí N2, O2, CO2');
  },
  gapKhuc: (cap = 'Một phân tử: đường đi gấp khúc (nét liền) dài, đoạn dời chỗ (nét đứt) ngắn.') => {
    let b = defs('gk1');
    const P = [[20, 120], [70, 60], [96, 150], [150, 100], [128, 30], [196, 70], [180, 150], [248, 110], [280, 40]];
    b += `<polyline points="${P.map((p) => p.join(',')).join(' ')}" fill="none" stroke="${INK}" stroke-width="2.4"/>`;
    P.slice(1, -1).forEach(([x, y]) => { b += dot(x, y, 3.5, GREY); });
    b += arr(20, 120, 276, 44, 'gk1', RED, '8 5', 2.4) + dot(20, 120, 6) + T(26, 150, 'đầu', { a: 'middle' }) + T(240, 30, 'cuối', { a: 'end' });
    return wrap('0 0 300 166', b, cap, 'Đường đi gấp khúc của một phân tử khí');
  },
  tuiKhi: (cap = `Túi khí: 84 g N<sub>2</sub> ở đktc.`) => {
    let b = `<circle cx="72" cy="96" r="54" fill="none" stroke="${INK}" stroke-width="${SW}"/><circle cx="72" cy="96" r="14" fill="${INK}"/>`;
    b += ln(72, 82, 72, 44, INK, 4) + ln(60, 104, 30, 128, INK, 4) + ln(84, 104, 114, 128, INK, 4);
    b += `<ellipse cx="200" cy="92" rx="86" ry="70" fill="#eef2fa" stroke="${INK}" stroke-width="${SW}"/>`;
    b += T(204, 88, `${N2}`, { a: 'middle', w: 700, size: 26 }) + T(204, 118, 'm = 84 g', { a: 'middle' });
    return wrap('0 0 292 176', b, cap, 'Túi khí ô tô phồng lên bằng khí nitrogen');
  },
  // ===== Bài tập mẫu =====
  haiBinhD3: (cap = 'Hai bình cùng thể tích, cùng 0 °C, 1 atm.') => {
    let b = rect(14, 40, 120, 120, { rx: 10 }) + rect(170, 40, 120, 120, { rx: 10 });
    b += T(74, 94, 'He', { a: 'middle', w: 700, size: 26 }) + T(74, 126, 'M = 4', { a: 'middle' });
    b += T(230, 94, H2, { a: 'middle', w: 700, size: 26 }) + T(230, 126, 'M = 2', { a: 'middle' });
    b += T(74, 28, 'bình 1', { a: 'middle' }) + T(230, 28, 'bình 2', { a: 'middle' });
    return wrap('0 0 304 170', b, cap, 'Hai bình cùng thể tích đựng helium và hydrogen');
  },
  giotD4: (cap = 'Đi theo chuỗi, mỗi bước dùng kết quả bước trước.') => {
    let b = defs('gd1') + `<circle cx="44" cy="54" r="32" fill="#eef2fa" stroke="${INK}" stroke-width="${SW}"/>` + doan(12, 76, 116, 'd');
    const S = ['V', 'm', 'n', 'N'];
    S.forEach((s, i) => {
      const x = 104 + i * 50;
      b += rect(x, 36, 34, 36, { rx: 5, sw: 2.4 }) + T(x + 17, 61, s, { a: 'middle', w: 700 });
      if (i < 3) b += arr(x + 35, 54, x + 44, 54, 'gd1', INK, '', 2.2);
    });
    b += T(208, 100, `${gk('ρ')} · M · N${sb('A')}`, { a: 'middle' }) + T(208, 124, 'cho ở đề', { a: 'middle' });
    return wrap('0 0 304 136', b, cap, 'Giọt nước hình cầu và chuỗi V, m, n, N');
  },
  lapPhuongD5: (cap = 'Mỗi phân tử ở tâm một ô lập phương cạnh d; D: đường kính.') => {
    let b = '';
    for (let i = 0; i < 3; i++) for (let j = 0; j < 1; j++) {
      const x = 20 + i * 86, y = 20 + j * 86;
      b += rect(x, y, 86, 86, { rx: 0, sw: 2, c: GREY, dash: '6 4' }) + `<circle cx="${x + 43}" cy="${y + 43}" r="6" fill="${INK}"/>`;
    }
    b += doan(20, 106, 128, 'd');
    b += ln(242, 58, 262, 36, GREY, 1.6) + T(266, 40, 'D', { w: 700 });
    return wrap('0 0 300 138', b, cap, 'Mô hình mỗi phân tử chiếm một hình lập phương');
  },
  // ===== Bài tương tự =====
  bongTT: (cap = 'Bóng buộc kín nhúng vào nước nóng.') => {
    let b = `<ellipse cx="150" cy="70" rx="56" ry="62" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + ln(150, 132, 150, 160, INK, 2);
    b += `<path d="M30,120 L30,196 L270,196 L270,120" fill="none" stroke="${INK}" stroke-width="${SW}"/>` + ln(30, 148, 270, 148, BLUE, 2, '8 5');
    b += T(60, 182, 'nước nóng');
    return wrap('0 0 300 206', b, cap, 'Quả bóng bay nhúng vào chậu nước nóng');
  },
  khoiNhomTT: (cap = 'Khối nhôm lập phương cạnh 1,0 cm.') => {
    let b = `<path d="M40,70 L170,70 L170,190 L40,190 Z M40,70 L90,30 L220,30 L170,70 M220,30 L220,150 L170,190" fill="#fff" stroke="${INK}" stroke-width="${SW}" stroke-linejoin="round"/>`;
    b += doan(40, 170, 212, '1,0 cm') + T(105, 136, 'Al', { a: 'middle', w: 700, size: 26 });
    return wrap('0 0 240 222', b, cap, 'Khối nhôm hình lập phương');
  },
};
