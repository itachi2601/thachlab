// Hình minh hoạ cho ruột tập VL12 · Chương 3 · Bài 15 Một số ứng dụng của cảm ứng điện từ (lesson 126). Cùng quy tắc với hinh.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (đặc – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh. Xem thử: node scripts/ruot-tap/l12-c3-bai15.mjs --hinh
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const arr = (x1, y1, x2, y2, id, c = INK, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${SW}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const rect = (x, y, w, h, o = {}) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${o.rx ?? 0}" fill="${o.fill ?? '#fff'}" stroke="${o.c ?? INK}" stroke-width="${o.sw ?? SW}"${o.dash ? ` stroke-dasharray="${o.dash}"` : ''}/>`;
const ell = (cx, cy, rx, ry, c = INK, w = SW, dash = '') => `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="none" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
// tiết diện dây cuộn: ⊙ / ⊗
const dot = (x, y, r = 8) => `<circle cx="${x}" cy="${y}" r="${r}" fill="#fff" stroke="${INK}" stroke-width="2.2"/><circle cx="${x}" cy="${y}" r="2.4" fill="${INK}"/>`;
const crs = (x, y, r = 8) => `<circle cx="${x}" cy="${y}" r="${r}" fill="#fff" stroke="${INK}" stroke-width="2.2"/>` + ln(x - 5, y - 5, x + 5, y + 5, INK, 2) + ln(x - 5, y + 5, x + 5, y - 5, INK, 2);
// nồi: thân + hai quai
const noi = (x, y, w, h) => rect(x, y, w, h, { sw: SW }) + ln(x - 18, y + 12, x, y + 12) + ln(x + w, y + 12, x + w + 18, y + 12) + rect(x - 6, y - 8, w + 12, 8, { fill: '#fff' });

export const hinhL12c3b15 = {
  // ===== Trang 1 · Dự đoán: bếp từ đang đun (không vẽ đường sức, không chỉ chỗ nóng) =====
  bepTu: (cap = 'Bếp từ đang đun: không lửa, không mâm nóng đỏ.') => {
    let b = noi(90, 42, 120, 70);
    b += T(150, 98, 'nồi gang', { a: 'middle' });
    b += rect(20, 112, 260, 14, { fill: '#eef2fa' }) + T(6, 104, 'mặt kính');
    b += [70, 100, 130, 170, 200, 230].map((x) => `<circle cx="${x}" cy="${144}" r="8" fill="#fff" stroke="${INK}" stroke-width="2.2"/>`).join('');
    b += T(150, 178, 'cuộn dây', { a: 'middle' }) + ln(150, 160, 150, 152, GREY, 2);
    return wrap('0 0 300 186', b, cap, 'Nồi gang đặt trên bếp từ');
  },
  // ===== Trang 1 · II.1: bộ cảm ứng của đàn ghi ta điện =====
  pickup: (cap = 'Bộ cảm ứng: dây thép rung ngay trên nam châm quấn cuộn dây.') => {
    let b = defs('pk');
    b += ln(10, 34, 290, 34) + `<path d="M10,34 Q150,14 290,34" fill="none" stroke="${GREY}" stroke-width="2" stroke-dasharray="5 4"/><path d="M10,34 Q150,54 290,34" fill="none" stroke="${GREY}" stroke-width="2" stroke-dasharray="5 4"/>`;
    b += T(200, 24, 'dây thép');
    b += rect(132, 60, 36, 92, { fill: '#fff' }) + T(150, 82, 'N', { a: 'middle', w: 700 }) + T(150, 146, 'S', { a: 'middle', w: 700 });
    b += [88, 100, 112, 124].map((y) => ell(150, y, 32, 6, BLUE, 2.4)).join('');
    b += T(12, 112, 'cuộn dây') + ln(96, 106, 116, 106, GREY, 2);
    b += T(12, 146, 'nam châm') + ln(108, 140, 130, 140, GREY, 2);
    b += ln(182, 124, 214, 124, BLUE, 2.4) + ln(182, 100, 214, 100, BLUE, 2.4) + ln(214, 100, 214, 124, BLUE, 2.4) + arr(214, 112, 226, 112, 'pk', BLUE);
    b += rect(228, 92, 66, 40, { rx: 4 }) + T(261, 118, 'tăng âm', { a: 'middle', size: 18 });
    b += arr(261, 134, 261, 146, 'pk', INK) + T(261, 164, 'loa', { a: 'middle' });
    return wrap('0 0 300 170', b, cap, 'Dây thép dao động trên bộ cảm ứng của đàn ghi ta điện');
  },
  // ===== Trang 2 · II.2: sạc không dây (hai cuộn rời) =====
  sacKhongDay: (cap = 'Hai cuộn đồng trục, không chạm nhau, khe hở d.', o = {}) => {
    const { d = 'd', bia = false } = o;
    let b = '';
    b += rect(60, 14, 180, 46, { rx: 8 }) + T(150, 34, 'điện thoại', { a: 'middle' });
    b += ell(150, 50, 60, 6, BLUE, 2.4) + ell(150, 50, 40, 4, BLUE, 2.4) + T(248, 54, `N${sb('2')}`, { w: 700 });
    if (bia) b += rect(70, 72, 160, 10, { fill: '#eef2fa', sw: 1.8 }) + rect(70, 82, 160, 10, { fill: '#eef2fa', sw: 1.8 }) + T(234, 90, 'bìa');
    b += rect(60, 106, 180, 40, { rx: 6 }) + ell(150, 114, 60, 6, RED, 2.4) + ell(150, 114, 40, 4, RED, 2.4) + T(248, 120, `N${sb('1')}`, { w: 700 });
    b += T(150, 140, 'đế sạc', { a: 'middle' });
    b += ln(50, 60, 50, 106, GREY, 2) + ln(44, 60, 56, 60, GREY, 2) + ln(44, 106, 56, 106, GREY, 2) + T(42, 90, d, { w: 700, a: 'end' });
    b += ln(150, 146, 150, 162, INK, 2.4) + `<circle cx="150" cy="174" r="12" fill="#fff" stroke="${INK}" stroke-width="2.4"/>` + T(150, 181, '~', { a: 'middle', w: 700, size: 24 });
    b += T(170, 181, `U${sb('1')}`, { w: 700 });
    return wrap('0 0 300 194', b, cap, 'Đế sạc không dây và điện thoại');
  },
  // ===== Trang 3 · II.3: con lắc tấm nhôm liền khối / xẻ rãnh giữa hai cực =====
  conLac: (cap = 'Hai tấm nhôm cùng cỡ, cùng dây treo; vùng đứt nét là chỗ hai cực nam châm kẹp hai bên.') => {
    const tam = (x, ranh) => {
      let s = ln(x + 40, 12, x + 18, 100) + ln(x + 40, 12, x + 62, 100) + `<circle cx="${x + 40}" cy="12" r="4" fill="${INK}"/>`;
      s += rect(x + 6, 100, 68, 46, { fill: '#e3e7f0' });
      if (ranh) s += [20, 34, 48, 62].map((dx) => `<rect x="${x + dx - 2}" y="${112}" width="4" height="34" fill="#fff" stroke="${INK}" stroke-width="1.6"/>`).join('');
      s += `<circle cx="${x + 40}" cy="128" r="26" fill="none" stroke="${RED}" stroke-width="2.4" stroke-dasharray="6 4"/>`;
      return s;
    };
    let b = tam(20, false) + tam(170, true);
    b += T(60, 176, 'a) liền khối', { a: 'middle', w: 700 }) + T(210, 176, 'b) xẻ rãnh', { a: 'middle', w: 700 });
    return wrap('0 0 290 186', b, cap, 'Hai con lắc tấm nhôm dao động giữa hai cực nam châm');
  },
  // ===== Trang 3 · II.4: mặt cắt bếp từ =====
  bepCat: (cap = 'Mặt cắt bếp từ; đứt nét: đường sức từ.') => {
    let b = rect(100, 18, 100, 36, { fill: '#fff' }) + T(6, 40, 'đáy nồi') + ln(78, 34, 98, 34, GREY, 2);
    b += rect(14, 60, 272, 12, { fill: '#eef2fa' }) + T(294, 52, 'mặt kính', { a: 'end' });
    b += [80, 110, 140].map((x) => crs(x, 92)).join('') + [160, 190, 220].map((x) => dot(x, 92)).join('');
    b += [[60, 34], [90, 24], [210, 24], [240, 34]].map(([x, h]) => `<path d="M150,108 C${x},${120 + h} ${x},${30 - h} 150,${36}" fill="none" stroke="${BLUE}" stroke-width="2" stroke-dasharray="5 4"/>`).join('');
    b += T(150, 140, 'cuộn dây', { a: 'middle' });
    return wrap('0 0 300 150', b, cap, 'Mặt cắt bếp từ: cuộn dây, mặt kính, đáy nồi');
  },
  // ===== Trang 4 · Bẫy 3: lực hãm theo tốc độ =====
  phanh: (cap = 'Lực hãm theo tốc độ xe: phanh điện từ (đặc), phanh ma sát (đứt).') => {
    let b = defs('ph1') + defs('ph2');
    b += arr(40, 150, 280, 150, 'ph1') + arr(40, 150, 40, 14, 'ph2');
    b += T(282, 142, 'v', { a: 'end', w: 700 }) + T(48, 28, `F${sb('hãm')}`, { w: 700 });
    b += ln(40, 150, 250, 40, RED, 3.2) + ln(40, 86, 250, 86, BLUE, 3, '9 6');
    b += T(26, 168, 'O', { w: 700 });
    return wrap('0 0 300 176', b, cap, 'Đồ thị lực hãm theo tốc độ');
  },
  // ===== Trang 5 · bài toán mẫu: U₂ đo được theo khoảng cách d =====
  uTheoD: (cap = 'Chấm: số đo; đứt: lí tưởng 9,0 V.') => {
    const X = (d) => 50 + d * 56, Y = (u) => 160 - u * 14;
    let b = defs('ud1') + defs('ud2');
    b += arr(50, 160, 290, 160, 'ud1') + arr(50, 160, 50, 14, 'ud2');
    b += ln(50, Y(9), 284, Y(9), GREY, 2.2, '8 5') + T(40, Y(9) + 6, '9,0', { a: 'end' });
    b += [0, 1, 2, 3, 4].map((d) => ln(X(d), 160, X(d), 166, INK, 2) + T(X(d), 186, String(d), { a: 'middle' })).join('');
    b += [[0, 8.4], [1, 7.1], [2, 5.9], [3, 4.8], [4, 3.9]].map(([d, u]) => `<circle cx="${X(d)}" cy="${Y(u)}" r="5" fill="${RED}"/>`).join('');
    b += T(292, 150, 'd (cm)', { a: 'end' }) + T(64, 30, `U${sb('2')} (V)`, { w: 700 });
    return wrap('0 0 300 194', b, cap, 'Điện áp thứ cấp đo được theo khoảng cách hai cuộn');
  },
  // ===== Bài tập mẫu D3: tấm nhôm rơi qua khe hai cực =====
  tamRoi: (cap = 'Tình huống (2).') => {
    let b = defs('tr');
    b += rect(20, 70, 70, 60, { fill: '#e3e7f0' }) + T(55, 108, 'N', { a: 'middle', w: 700 });
    b += rect(210, 70, 70, 60, { fill: '#e3e7f0' }) + T(245, 108, 'S', { a: 'middle', w: 700 });
    b += [84, 100, 116].map((y) => arr(92, y, 202, y, 'tr', BLUE, '6 4')).join('');
    b += rect(144, 40, 12, 96, { fill: '#fff' }) + T(150, 30, 'tấm nhôm (nhìn từ cạnh)', { a: 'middle' });
    b += arr(150, 138, 150, 160, 'tr', RED) + T(160, 158, 'v', { c: RED, w: 700 });
    return wrap('0 0 300 166', b, cap, 'Tấm nhôm rơi qua khe giữa hai cực nam châm');
  },
  // ===== Bài tương tự D3·1: nam châm rơi trong ống đồng =====
  ongDong: (cap = 'Nam châm rơi trong ống.') => {
    let b = defs('od');
    b += rect(40, 14, 16, 196, { fill: '#e3e7f0', sw: 2.4 }) + rect(104, 14, 16, 196, { fill: '#e3e7f0', sw: 2.4 });
    b += rect(64, 70, 32, 46, { fill: '#fff' }) + T(80, 90, 'N', { a: 'middle', w: 700 }) + T(80, 112, 'S', { a: 'middle', w: 700 });
    b += arr(80, 122, 80, 168, 'od', RED) + T(88, 160, 'v', { c: RED, w: 700 });
    b += T(80, 234, 'ống', { a: 'middle' });
    return wrap('0 0 160 244', b, cap, 'Nam châm rơi trong ống kim loại dựng đứng');
  },
};
