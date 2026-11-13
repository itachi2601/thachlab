// Hình minh hoạ cho ruột tập VL11 · Bài 11 Sóng điện từ (lesson 30). Cùng quy tắc với hinh-l11-bai2.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, phân biệt bằng nét (liền – đứt) chứ không chỉ bằng màu, tự vẽ.
// Chữ Hi Lạp (λ) lấy từ font KaTeX (Source Sans 3 chỉ nạp latin/vietnamese → tránh rơi về Helvetica).
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh. Xem thử: node scripts/ruot-tap/l11-bai11.mjs --hinh
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const LAM = gk('λ');
const sup = (s) => `<tspan font-size="15" dy="-8">${s}</tspan><tspan dy="8"> </tspan>`;
const arr = (x1, y1, x2, y2, id, c = INK, dash = '', w = SW) =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const f1 = (v) => (+v).toFixed(1);
// đường lượn sóng từ (x1,y1) tới (x2,y2), biên độ a, số bước n
const luon = (x1, y1, x2, y2, a = 6, n = 8, c = INK, w = 2.4) => {
  const L = Math.hypot(x2 - x1, y2 - y1), ux = (x2 - x1) / L, uy = (y2 - y1) / L;
  let d = '';
  for (let k = 0; k <= 120; k++) {
    const s = (k / 120) * L, o = a * Math.sin((k / 120) * n * 2 * Math.PI);
    d += `${k ? 'L' : 'M'}${f1(x1 + ux * s - uy * o)},${f1(y1 + uy * s + ux * o)}`;
  }
  return `<path d="${d}" fill="none" stroke="${c}" stroke-width="${w}"/>`;
};
const veTinhHinh = (x, y) => `<rect x="${x - 14}" y="${y - 10}" width="28" height="20" rx="3" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
  + `<rect x="${x - 52}" y="${y - 7}" width="32" height="14" fill="${GREY}" opacity=".55" stroke="${INK}" stroke-width="1.6"/>`
  + `<rect x="${x + 20}" y="${y - 7}" width="32" height="14" fill="${GREY}" opacity=".55" stroke="${INK}" stroke-width="1.6"/>`
  + ln(x - 20, y, x - 14, y, INK, 2) + ln(x + 14, y, x + 20, y, INK, 2);
const chao = (x, y) => `<path d="M${x - 18},${y - 14} Q${x},${y + 10} ${x + 18},${y - 14}" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + ln(x, y - 2, x, y + 14, INK, 2.4);

export const hinhL11b11 = {
  // Trang 1 · Dự đoán: vệ tinh địa tĩnh — chú thích chỉ tả cảnh, không nói sóng gì/đi qua cái gì
  veTinh: (cap = 'Vệ tinh cao 36 000 km; chảo thu trên mái nhà.') => {
    let b = defs('vt1');
    b += `<path d="M0,212 Q160,176 320,212" fill="#eef2fa" stroke="${INK}" stroke-width="2.4"/>`;
    b += `<rect x="190" y="164" width="56" height="34" fill="#fff" stroke="${INK}" stroke-width="2.4"/><path d="M184,166 L218,140 L252,166" fill="none" stroke="${INK}" stroke-width="2.4"/>`;
    b += chao(218, 132);
    b += veTinhHinh(84, 48);
    b += ln(110, 64, 206, 114, GREY, 2.2, '5 6') + T(170, 82, '?', { size: 26, w: 700 }); // không vẽ sóng lượn: gợi đáp án C
    b += `<line x1="24" y1="50" x2="24" y2="184" stroke="${GREY}" stroke-width="2" stroke-dasharray="6 5" marker-start="url(#vt1)" marker-end="url(#vt1)"/>` + T(32, 150, '36 000 km', { size: 20 }) + T(32, 172, '(không đúng tỉ lệ)', { size: 17, c: GREY });
    b += T(84, 22, 'vệ tinh', { a: 'middle', size: 20 }) + T(268, 148, 'chảo', { a: 'middle', size: 20 });
    return wrap('0 0 320 216', b, cap, 'Vệ tinh và chảo thu');
  },
  // Trang 2 · E ⊥ B ⊥ phương truyền, vẽ phối cảnh: mặt phẳng ngang (hình bình hành xám) chứa B; E đứng, x nằm ngang.
  // Vẽ vectơ tại 5 điểm (không vẽ đường bao của B vì phối cảnh làm nó trông như vòng khép); góc vuông đánh dấu tại điểm đầu.
  eb: (cap = 'E (liền, đỏ) đứng; B (đứt, xanh) nằm ngang, chĩa ra trước trang; Ox: phương truyền.') => {
    let b = defs('eb1') + defs('eb2') + defs('eb3');
    const x0 = 34, x1 = 292, yc = 112, A = 66, zx = -0.55, zy = 0.5, Bm = 56; // trục z (ra trước trang) vẽ xiên xuống trái
    b += `<path d="M${x0 + 30},${yc - 26} L${x1},${yc - 26} L${x1 - 52},${yc + 22} L${x0 - 22},${yc + 22} Z" fill="#eef2fa" stroke="${GREY}" stroke-width="1.2"/>`;
    let dE = '';
    for (let k = 0; k <= 160; k++) { const s = k / 160, x = x0 + s * (x1 - x0 - 26); dE += `${k ? 'L' : 'M'}${f1(x)},${f1(yc - A * Math.sin(s * 2 * Math.PI))}`; }
    b += `<path d="${dE}" fill="none" stroke="${RED}" stroke-width="2" opacity=".55"/>`;
    b += arr(x0 - 14, yc, x1 + 4, yc, 'eb1', INK, '', 2.4) + T(x1 + 2, yc - 10, 'x', { a: 'end', w: 700 });
    [0.25, 0.5, 0.75, 1, 1.25].map((q) => q / 1.25).forEach((s, i) => {
      const x = x0 + s * (x1 - x0 - 26) * 1, v = Math.sin(s * 2 * Math.PI);
      if (Math.abs(v) < 0.2) return;
      b += arr(f1(x), yc, f1(x), f1(yc - A * v * 0.92), 'eb2', RED, '', 2.8);
      b += arr(f1(x), yc, f1(x + Bm * zx * v), f1(yc + Bm * zy * v), 'eb3', BLUE, '6 4', 2.8);
    });
    // điểm đầu (s = 0,25): góc vuông E–x và nhãn rời mũi tên
    const xs = x0 + 0.2 * (x1 - x0 - 26);
    b += `<path d="M${f1(xs + 10)},${yc} L${f1(xs + 10)},${yc - 10} L${f1(xs)},${yc - 10}" fill="none" stroke="${INK}" stroke-width="1.6"/>`;
    b += T(f1(xs - 10), yc - A + 6, '<tspan font-weight="700">E</tspan>', { c: RED, a: 'end', size: 22 });
    b += T(f1(xs + Bm * zx - 6), f1(yc + Bm * zy + 24), '<tspan font-weight="700">B</tspan>', { c: BLUE, a: 'middle', size: 22 });
    return wrap('0 0 320 196', b, cap, 'Điện trường và từ trường trong sóng điện từ');
  },
  // Trang 2 · lò vi sóng: thanh sô-cô-la, các vệt chảy, d đo giữa tâm hai vệt liền nhau
  soCoLa: (cap = 'Thanh sô-cô-la sau khi bật lò (đĩa không xoay). d: khoảng cách tâm hai vệt chảy liền nhau.') => {
    let b = defs('sc1');
    b += `<rect x="14" y="40" width="292" height="56" rx="6" fill="#efe6dc" stroke="${INK}" stroke-width="${SW}"/>`;
    const cx = [52, 128, 204, 280];
    cx.forEach((x) => { b += `<ellipse cx="${x}" cy="68" rx="20" ry="18" fill="${GREY}" opacity=".7" stroke="${INK}" stroke-width="1.8" stroke-dasharray="4 3"/>` + ln(x, 36, x, 106, INK, 1.6, '3 3'); });
    b += `<line x1="128" y1="124" x2="204" y2="124" stroke="${RED}" stroke-width="2.6" marker-start="url(#sc1)" marker-end="url(#sc1)"/>`;
    b += ln(128, 108, 128, 132, RED, 2) + ln(204, 108, 204, 132, RED, 2);
    b += T(166, 152, '<tspan font-style="italic" font-weight="700">d</tspan>', { a: 'middle', c: RED, size: 22 });
    b += T(52, 26, 'vệt chảy', { a: 'middle' });
    return wrap('0 0 320 160', b, cap, 'Thanh sô-cô-la trong lò vi sóng');
  },
  // Trang 3 · thang sóng điện từ dọc, trục luỹ thừa 10 (m), bước sóng giảm dần từ trên xuống
  thang: (cap = `Trục ${'chia theo'} luỹ thừa 10 của mét. Vạch hẹp tô đậm: ánh sáng nhìn thấy.`) => {
    let b = '';
    const y0 = 44, dy = 22, Y = (e) => y0 + (3 - e) * dy; // e = số mũ của 10 (m), từ 3 xuống −12
    const x = 92;
    b += ln(x, Y(3), x, Y(-12), INK, 2.4);
    [3, 0, -3, -6, -9, -12].forEach((e) => { b += ln(x - 7, f1(Y(e)), x, f1(Y(e)), INK, 2.2) + T(x - 10, f1(Y(e) + 7), `10${sup(e < 0 ? '−' + -e : e)}`, { a: 'end', size: 20 }); });
    // ranh giới vùng (log10 m): vô tuyến >0 · vi sóng −3..0 · hồng ngoại −6,12..−3 · nhìn thấy −6,42..−6,12 · tử ngoại −8..−6,42 · X −11..−8 · gamma < −11
    const vung = [[3, 0, 'vô tuyến'], [0, -3, 'vi sóng'], [-3, -6.12, 'hồng ngoại'], [-6.12, -6.42, ''], [-6.42, -8, 'tử ngoại'], [-8, -11, 'tia X'], [-11, -12.6, 'gamma']];
    vung.forEach(([a, c, n], i) => {
      const ya = Y(a), yc = Y(c);
      b += `<rect x="${x + 4}" y="${f1(ya)}" width="18" height="${f1(yc - ya)}" fill="${n ? (i % 2 ? '#fff' : '#e3e8f3') : INK}" stroke="${INK}" stroke-width="1.4"/>`;
      const lift = n === 'hồng ngoại' ? -14 : n === 'tử ngoại' ? 10 : 0;
      if (n) b += T(x + 30, f1((ya + yc) / 2 + 7 + lift), n, { size: 20 });
    });
    b += ln(x + 22, f1(Y(-6.27)), x + 40, f1(Y(-6.27)), INK, 2) + T(x + 44, f1(Y(-6.27) + 7), 'nhìn thấy', { size: 20, w: 700 });
    b += T(x + 2, 22, `${LAM} (m)`, { a: 'middle', size: 20 });
    return wrap('0 0 230 400', b, cap, 'Thang sóng điện từ');
  },
  // Trang 3 · ra-đa: sóng đi tới vật rồi phản xạ về (không ghi s = 2d để HS tự điền)
  raDa: (cap = 'Ra-đa phát xung, xung gặp máy bay rồi phản xạ về; t đo từ lúc phát đến lúc thu.') => {
    let b = defs('rd1') + defs('rd2');
    b += `<path d="M18,150 Q40,112 62,150 Z" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + ln(40, 150, 40, 176, INK, 3) + ln(14, 178, 306, 178, INK, 2.4);
    b += `<path d="M262,58 l34,-6 l4,6 l-34,8 z M274,56 l10,-16 l6,2 l-6,16 z" fill="${GREY}" stroke="${INK}" stroke-width="1.8"/>`;
    b += luon(60, 128, 252, 64, 5, 7, RED, 2.6) + arr(244, 67, 254, 63, 'rd1', RED, '', 2.6);
    b += luon(250, 82, 70, 144, 5, 7, BLUE, 2.6) + `<path d="M78,141 l-10,5" stroke="${BLUE}" stroke-width="2.6" marker-end="url(#rd2)"/>`;
    b += T(150, 74, 'đi', { a: 'middle', c: RED, w: 700 }) + T(178, 140, 'về', { a: 'middle', c: BLUE, w: 700 });
    b += `<line x1="40" y1="198" x2="278" y2="198" stroke="${INK}" stroke-width="2" marker-start="url(#rd1)" marker-end="url(#rd1)"/>` + T(160, 222, '<tspan font-style="italic">d</tspan>', { a: 'middle', size: 22 });
    return wrap('0 0 320 230', b, cap, 'Ra-đa đo khoảng cách');
  },
  // Trang 4 · bài toán mẫu nhà Minh: ba nguồn sóng quanh nhà
  nhaMinh: (cap = 'Nhà Minh: đài FM, bộ phát wifi hai băng, chảo thu vệ tinh.') => {
    let b = defs('nm1');
    b += `<rect x="60" y="120" width="200" height="90" fill="#fff" stroke="${INK}" stroke-width="2.4"/><path d="M48,122 L160,58 L272,122" fill="none" stroke="${INK}" stroke-width="2.4"/>`;
    b += chao(220, 92);
    b += `<rect x="84" y="164" width="52" height="30" rx="4" fill="#fff" stroke="${INK}" stroke-width="2.2"/>` + ln(94, 164, 84, 140, INK, 2) + T(110, 186, 'FM', { a: 'middle', size: 20, w: 700 });
    b += `<rect x="168" y="176" width="56" height="18" rx="4" fill="#fff" stroke="${INK}" stroke-width="2.2"/>` + ln(178, 176, 174, 156, INK, 2) + ln(214, 176, 218, 156, INK, 2) + T(196, 170, 'wifi', { a: 'middle', size: 20 });
    b += veTinhHinh(250, 22) + luon(240, 38, 222, 76, 3, 4, RED, 2.2);
    return wrap('0 0 320 216', b, cap, 'Nhà Minh và ba nguồn sóng');
  },
  // Trang 5 · điền bước: trạm A – vệ tinh – trạm B, mỗi chặng 36 000 km
  abVeTinh: (cap = 'Tiếng nói đi A → vệ tinh → B; mỗi chặng 36 000 km.') => {
    let b = defs('ab1');
    b += `<path d="M0,196 Q160,166 320,196" fill="#eef2fa" stroke="${INK}" stroke-width="2.4"/>`;
    b += veTinhHinh(160, 30);
    b += chao(52, 168) + chao(268, 168) + T(52, 206, 'A', { a: 'middle', w: 700 }) + T(268, 206, 'B', { a: 'middle', w: 700 });
    b += arr(60, 148, 148, 46, 'ab1', RED, '', 2.6) + arr(172, 46, 260, 148, 'ab1', RED, '', 2.6);
    b += T(84, 92, '36 000 km', { a: 'end', size: 20 }) + T(236, 92, '36 000 km', { size: 20 });
    return wrap('0 0 320 212', b, cap, 'Gọi điện qua vệ tinh');
  },
  // Trang 6 · dạng 2: mốc thang đổi ra mét (để so cùng đơn vị) — HS dùng khi xếp vùng
  mocThang: (cap = 'Mốc một số vùng (bước sóng trong chân không).') => {
    let b = '';
    const hang = [['vi sóng', '1 mm – 1 m'], ['hồng ngoại', '760 nm – 1 mm'], ['nhìn thấy', '380 – 760 nm'], ['tử ngoại', '10 – 380 nm'], ['tia X', '10 pm – 10 nm']];
    hang.forEach(([n, r], i) => {
      const y = 12 + i * 34;
      b += `<rect x="6" y="${y}" width="308" height="30" fill="${i % 2 ? '#fff' : '#eef2fa'}" stroke="${GREY}" stroke-width="1.2"/>`;
      b += T(16, y + 22, n, { size: 20, w: 700 }) + T(304, y + 22, r, { a: 'end', size: 20 });
    });
    return wrap('0 0 320 186', b, cap, 'Mốc thang sóng điện từ');
  },
  // Trang 7 · dạng 4: ra-đa và drone ở hai lần đo
  drone: (cap = 'Hai lần đo cách nhau 30 s; drone bay thẳng ra xa ra-đa.') => {
    let b = defs('dr1');
    b += `<path d="M14,120 Q34,88 54,120 Z" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + ln(34, 120, 34, 142, INK, 3) + ln(10, 144, 310, 144, INK, 2.4);
    const dr = (x, c, dash = '') => `<rect x="${x - 16}" y="44" width="32" height="10" rx="3" fill="#fff" stroke="${c}" stroke-width="2.4"${dash ? ` stroke-dasharray="${dash}"` : ''}/>` + ln(x - 22, 40, x - 8, 40, c, 2.2) + ln(x + 8, 40, x + 22, 40, c, 2.2);
    b += dr(200, GREY, '4 3') + dr(276, INK);
    b += arr(220, 30, 256, 30, 'dr1', INK, '', 2.2);
    b += `<line x1="34" y1="166" x2="200" y2="166" stroke="${GREY}" stroke-width="2" stroke-dasharray="6 4" marker-start="url(#dr1)" marker-end="url(#dr1)"/>` + T(117, 156, 'd<tspan font-size="15" dy="5">1</tspan>', { a: 'middle' });
    b += `<line x1="34" y1="190" x2="276" y2="190" stroke="${INK}" stroke-width="2" marker-start="url(#dr1)" marker-end="url(#dr1)"/>` + T(155, 214, 'd<tspan font-size="15" dy="5">2</tspan>', { a: 'middle' });
    b += T(200, 76, 'lần 1', { a: 'middle', size: 20, c: GREY }) + T(276, 76, 'lần 2', { a: 'middle', size: 20 });
    return wrap('0 0 320 222', b, cap, 'Ra-đa và drone ở hai lần đo');
  },
};
