// Hình SVG tự vẽ cho ruột tập Vật lí 10 · Bài 25 Động năng, thế năng (lesson 70). Cùng quy tắc với hinh.mjs/hinh-ch4.mjs:
// mỗi hình trả lời MỘT câu hỏi (H1), chữ ≥ 20 đơn vị viewBox (≈ 3 mm khi in rộng 46 mm), nét ≥ 2,8, phân biệt bằng nét đặc/đứt
// (in đen–trắng), chú thích không lộ đáp án ô Dự đoán. Kiểm cỡ in: xem file chú thích đầu l10-bai25.mjs (lệnh chụp từng hình).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`; // chỉ số dưới trong SVG
const L = (x1, y1, x2, y2, o = '') => `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${INK}" stroke-width="${SW}" ${o}/>`;
const arr = (x1, y1, x2, y2, id, c = INK, dash = '') =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${SW}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const dashG = (x1, y1, x2, y2) => `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${GREY}" stroke-width="2" stroke-dasharray="5 4"/>`;
const dim = (x, y1, y2, id) => `<line x1="${x}" y1="${y1}" x2="${x}" y2="${y2}" stroke="${INK}" stroke-width="2" marker-start="url(#${id})" marker-end="url(#${id})"/>`;
const dimDefs = (id) => `<defs><marker id="${id}" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto-start-reverse" markerUnits="userSpaceOnUse"><path d="M0,0 L8,4 L0,8 z" fill="${INK}"/></marker></defs>`;
const ground = (x1, x2, y) => L(x1, y, x2, y) + Array.from({ length: Math.floor((x2 - x1) / 16) }, (_, i) =>
  `<line x1="${x1 + 8 + i * 16}" y1="${y + 1}" x2="${x1 + i * 16}" y2="${y + 9}" stroke="${GREY}" stroke-width="1.6"/>`).join('');

// Xe đạp đơn giản: hai bánh + khung, bánh sau ở x
const xe = (x, g) => `<circle cx="${x}" cy="${g - 12}" r="12" fill="#fff" stroke="${INK}" stroke-width="${SW}"/><circle cx="${x + 38}" cy="${g - 12}" r="12" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
  + `<path d="M${x} ${g - 12} L${x + 16} ${g - 34} L${x + 38} ${g - 12} M${x + 16} ${g - 34} L${x + 32} ${g - 34} L${x + 38} ${g - 12} M${x + 30} ${g - 34} L${x + 28} ${g - 42} L${x + 36} ${g - 42}" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;

export const hinhB25 = {
  // Trang 1 · Dự đoán: cùng xe, cùng lực phanh, tốc độ gấp đôi
  xeDap: (cap = 'Cùng xe, cùng lực phanh. Mũi tên vận tốc vẽ theo tỉ lệ; vạch lết hôm sau vẽ ngắt quãng, không theo tỉ lệ.') => {
    const row = (g, ten, vl, vlab, sk, sklab, dash) => {
      let b = T(4, g - 8, ten, { w: 700 }) + xe(96, g);
      b += arr(116, g - 54, 116 + vl, g - 54, 'xd') + T(124 + vl, g - 47, vlab);
      // hôm sau: vạch ngắt quãng (không theo tỉ lệ) để không đo được tỉ số bằng thước — HS ảo 10/11 đo ra đáp án
      b += dash ? `<line x1="140" y1="${g + 5}" x2="196" y2="${g + 5}" stroke="${RED}" stroke-width="6"/><path d="M200 ${g + 14} L210 ${g - 4} M210 ${g + 14} L220 ${g - 4}" stroke="${RED}" stroke-width="2.4"/><line x1="224" y1="${g + 5}" x2="${140 + sk}" y2="${g + 5}" stroke="${RED}" stroke-width="6"/>`
        : `<line x1="140" y1="${g + 5}" x2="${140 + sk}" y2="${g + 5}" stroke="${INK}" stroke-width="6"/>`;
      b += T(140 + sk / 2, g + 30, sklab, { a: 'middle', c: dash ? RED : INK, w: dash ? 700 : 400 });
      return b + `<line x1="0" y1="${g}" x2="320" y2="${g}" stroke="${GREY}" stroke-width="1.6"/>`;
    };
    const b = defs('xd') + row(84, 'hôm qua', 40, '10 km/h', 40, '2 m', false) + row(184, 'hôm sau', 80, '20 km/h', 120, '? m', true);
    return wrap('0 0 320 222', b, cap, 'Hai lần phanh xe đạp với hai tốc độ');
  },
  // Trang 2 · Thí nghiệm: khúc gỗ qua cổng quang rồi trượt tới khi dừng
  congQuang: (cap = 'Cổng quang đo tốc độ v khúc gỗ lúc đi qua; thước đo quãng trượt s tới chỗ dừng.') => {
    let b = defs('cq') + dimDefs('cqd') + ground(4, 316, 120);
    b += `<path d="M62 120 V40 H92 V120" fill="none" stroke="${INK}" stroke-width="${SW}"/>` + `<line x1="62" y1="104" x2="92" y2="104" stroke="${RED}" stroke-width="2.4" stroke-dasharray="4 3"/>`;
    b += T(77, 30, 'cổng quang', { a: 'middle' });
    b += `<rect x="100" y="96" width="44" height="24" rx="2" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + arr(148, 84, 198, 84, 'cq') + T(204, 90, 'v', { w: 700 });
    b += `<rect x="252" y="96" width="44" height="24" rx="2" fill="none" stroke="${GREY}" stroke-width="${SW}" stroke-dasharray="6 4"/>` + T(274, 86, 'dừng', { a: 'middle', c: GREY });
    b += dashG(77, 120, 77, 150) + dashG(274, 120, 274, 150) + `<line x1="77" y1="146" x2="274" y2="146" stroke="${INK}" stroke-width="2" marker-start="url(#cqd)" marker-end="url(#cqd)"/>`;
    b += T(176, 172, 's', { a: 'middle', w: 700 });
    return wrap('0 0 320 180', b, cap, 'Khúc gỗ trượt qua cổng quang');
  },
  // Trang 2 · Thế năng: trục z hướng lên, gốc tại mốc; HS điền dấu Wt
  trucZ: (cap = 'Trục z hướng lên, gốc tại mốc. Điền dấu của W<sub>t</sub> ở ba vị trí.') => {
    let b = defs('tz') + arr(50, 206, 50, 14, 'tz') + T(62, 26, 'z', { w: 700 });
    b += `<line x1="30" y1="110" x2="116" y2="110" stroke="${INK}" stroke-width="2.4" stroke-dasharray="8 5"/>` + T(4, 104, 'mốc');
    [[46, 'z &gt; 0'], [110, 'z = 0'], [174, 'z &lt; 0']].forEach(([y, l]) => {
      b += `<circle cx="104" cy="${y}" r="10" fill="${INK}"/>` + T(126, y + 7, l);
      b += T(200, y + 7, `W${sb('t')}`) + `<rect x="240" y="${y - 13}" width="22" height="22" rx="3" fill="#fff" stroke="${RED}" stroke-width="2.4"/>` + T(270, y + 7, '0');
    });
    return wrap('0 0 300 214', b, cap, 'Dấu của thế năng trên, tại và dưới mốc');
  },
  // Trang 3 · Công trọng lực không phụ thuộc đường đi
  haiDuong: (cap = 'Đưa vật từ A lên B theo bậc thang (nét đặc) hoặc kéo dây thẳng đứng rồi dời ngang (nét đứt). Công của trọng lực hai đường so với nhau thế nào?') => {
    let b = dimDefs('hd') + ground(4, 300, 186);
    let st = 'M60 186'; for (let i = 0; i < 5; i++) st += ` h36 v-28`;
    b += `<path d="${st}" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<path d="M60 186 V46 H240" fill="none" stroke="${BLUE}" stroke-width="${SW}" stroke-dasharray="8 5"/>`;
    b += `<circle cx="60" cy="186" r="7" fill="${RED}"/><circle cx="240" cy="46" r="7" fill="${RED}"/>`;
    b += T(40, 178, 'A', { w: 700, a: 'end' }) + T(240, 30, 'B', { w: 700, a: 'middle' });
    b += dashG(248, 46, 290, 46) + dim(282, 48, 184, 'hd') + T(292, 124, 'h', { w: 700 });
    b += T(192, 176, 'bậc thang') + T(72, 36, 'dây', { c: BLUE });
    return wrap('0 0 310 200', b, cap, 'Hai đường đi khác nhau giữa cùng hai điểm');
  },
  // Trang 3 · Thí nghiệm con lắc vướng đinh
  conLac: (cap = 'Thả quả nặng từ vạch. Dây vướng đinh ở dưới điểm treo: bên kia quả nặng lên tới đâu?') => {
    const P = [160, 20], R = 130, a = (50 * Math.PI) / 180;
    const xl = P[0] - R * Math.sin(a), yl = P[1] + R * Math.cos(a), nail = [160, 85], r2 = 65;
    const dy = yl - nail[1], xr = nail[0] + Math.sqrt(r2 * r2 - dy * dy);
    let b = `<rect x="130" y="10" width="60" height="10" fill="${GREY}"/>`;
    b += `<line x1="20" y1="${yl}" x2="300" y2="${yl}" stroke="${GREY}" stroke-width="2.4" stroke-dasharray="8 5"/>` + T(300, yl + 26, 'vạch', { a: 'end' });
    b += L(P[0], P[1], xl, yl) + `<path d="M${xl.toFixed(1)} ${yl.toFixed(1)} A${R} ${R} 0 0 0 160 ${P[1] + R}" fill="none" stroke="${GREY}" stroke-width="2" stroke-dasharray="4 4"/>`;
    b += `<path d="M160 ${P[1] + R} A${r2} ${r2} 0 0 0 ${xr.toFixed(1)} ${yl.toFixed(1)}" fill="none" stroke="${GREY}" stroke-width="2" stroke-dasharray="4 4"/>`;
    b += `<line x1="160" y1="20" x2="160" y2="85" stroke="${INK}" stroke-width="${SW}" stroke-dasharray="7 4"/>`;
    b += `<line x1="160" y1="85" x2="${xr.toFixed(1)}" y2="${yl.toFixed(1)}" stroke="${INK}" stroke-width="${SW}" stroke-dasharray="7 4"/>`;
    b += `<circle cx="${xl.toFixed(1)}" cy="${yl.toFixed(1)}" r="10" fill="${INK}"/><circle cx="${xr.toFixed(1)}" cy="${yl.toFixed(1)}" r="10" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<circle cx="160" cy="85" r="5" fill="${RED}"/>` + T(172, 80, 'đinh', { c: RED });
    b += T(xl - 4, yl - 16, 'thả', { a: 'end' });
    return wrap('0 0 310 160', b, cap, 'Con lắc vướng đinh');
  },
  // Trang 4 · Bài toán mẫu: ray tàu lượn (độ cao theo tỉ lệ 8 đơn vị/m)
  tauLuon: (cap = 'Độ cao tính từ mặt đất, vẽ theo tỉ lệ; khoảng cách ngang không theo tỉ lệ.') => {
    const Y = (z) => 180 - 8 * z;
    let b = defs('tl') + ground(4, 316, 180);
    b += `<path d="M8 ${Y(18)} L48 ${Y(18)} C98 ${Y(18)} 120 ${Y(3)} 160 ${Y(3)} C200 ${Y(3)} 226 ${Y(13)} 266 ${Y(13)} C286 ${Y(13)} 300 ${Y(12)} 314 ${Y(10)}" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
    [[48, 18, 'A'], [160, 3, 'B']].forEach(([x, z, n]) => {
      b += dashG(x, Y(z), x, 180) + `<circle cx="${x}" cy="${Y(z)}" r="6" fill="${RED}"/>` + T(x, Y(z) - 12, n, { a: 'middle', w: 700 });
      b += T(x + 8, z > 5 ? Y(z / 2) + 7 : 172, `${z} m`);
    });
    b += arr(58, Y(18) - 30, 108, Y(18) - 30, 'tl', RED) + T(114, Y(18) - 23, '10 m/s', { c: RED });
    return wrap('0 0 320 194', b, cap, 'Ray tàu lượn qua A và B');
  },
  // Trang 5 · Thử thách ★★★: ném đá từ mép vực theo ba hướng
  vuc: (cap = 'Ném cùng tốc độ đầu theo ba hướng. Tốc độ lúc chạm nước có khác nhau không?') => {
    let b = defs('vc') + dimDefs('vcd');
    b += `<path d="M4 60 H120 V176 H310" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<path d="M126 176 Q200 168 310 176" fill="none" stroke="${BLUE}" stroke-width="2.4" stroke-dasharray="6 4"/>`;
    b += `<circle cx="108" cy="50" r="9" fill="${INK}"/>`;
    b += arr(116, 44, 162, 14, 'vc') + arr(118, 50, 172, 50, 'vc') + arr(116, 56, 160, 86, 'vc');
    b += `<line x1="4" y1="60" x2="300" y2="60" stroke="${GREY}" stroke-width="2" stroke-dasharray="5 4"/>` + T(8, 50, 'mốc');
    b += dim(250, 62, 174, 'vcd') + T(258, 124, '20 m');
    b += T(180, 26, '10 m/s');
    return wrap('0 0 320 186', b, cap, 'Ném đá từ mép vực xuống lòng suối');
  },
  // Dạng 3 · toà nhà: sàn hầm, mặt đường, tầng 3, tầng 6 (8 đơn vị/m)
  toaNha: (cap = 'Độ cao các sàn tính từ mặt đường. Đổi mốc thì z của chậu cây đổi ra sao?') => {
    const Y = (z) => 156 - 8 * z;
    let b = `<rect x="30" y="${Y(15) - 8}" width="100" height="${Y(-4) - Y(15) + 8}" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<line x1="0" y1="${Y(0)}" x2="300" y2="${Y(0)}" stroke="${INK}" stroke-width="${SW}"/>`;
    [[15, 'tầng 6: 15 m'], [6, 'tầng 3: 6,0 m'], [0, 'mặt đường: 0'], [-4, 'hầm: −4,0 m']].forEach(([z, l]) => {
      if (z) b += `<line x1="30" y1="${Y(z)}" x2="130" y2="${Y(z)}" stroke="${INK}" stroke-width="2.4"/>`;
      b += T(140, Y(z) + (z === 0 ? -6 : 7), l);
    });
    b += `<path d="M70 ${Y(6)} L66 ${Y(6) - 18} H90 L86 ${Y(6)} Z" fill="${INK}"/><path d="M78 ${Y(6) - 18} q-12 -20 -2 -30 q12 10 2 30" fill="none" stroke="${INK}" stroke-width="2.4"/>`;
    return wrap('0 0 300 196', b, cap, 'Toà nhà có tầng hầm và chậu cây ở tầng 3');
  },
  // Dạng 4 · đường đồi A → B → C (3 đơn vị/m)
  doi: (cap = 'Các độ cao tính từ cùng một mức chuẩn; đường đi quanh co.') => {
    const Y = (z) => 156 - 3 * z;
    let b = ground(4, 316, 156);
    b += `<path d="M8 ${Y(36)} C30 ${Y(40)} 40 ${Y(40)} 56 ${Y(40)} C100 ${Y(40)} 120 ${Y(12)} 160 ${Y(12)} C200 ${Y(12)} 230 ${Y(25)} 264 ${Y(25)} C284 ${Y(25)} 300 ${Y(22)} 314 ${Y(18)}" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
    [[56, 40, 'A'], [160, 12, 'B'], [264, 25, 'C']].forEach(([x, z, n]) => {
      b += dashG(x, Y(z), x, 156) + `<circle cx="${x}" cy="${Y(z)}" r="6" fill="${RED}"/>` + T(x, Y(z) - 12, n, { a: 'middle', w: 700 });
      b += T(x + 8, Y(z / 2) + 7, `${z} m`);
    });
    return wrap('0 0 320 166', b, cap, 'Đường đồi qua A, B, C');
  },
  // Dạng 5 · dốc nghiêng 30°: các lực tác dụng lên thùng
  doc: (cap = 'Kể đủ các lực tác dụng lên thùng và dấu công của từng lực.', sLab = 's = 10 m') => {
    const u = [Math.cos(Math.PI / 6), -0.5], nrm = [-0.5, -Math.cos(Math.PI / 6)];
    const p0 = [20 + 130 * u[0], 170 + 130 * u[1]], c = [p0[0] + 15 * nrm[0], p0[1] + 15 * nrm[1]];
    const at = (k, v, o = c) => [o[0] + k * v[0], o[1] + k * v[1]].map((x) => x.toFixed(1));
    let b = defs('dc') + `<path d="M20 170 H280 V${(170 - 260 * Math.tan(Math.PI / 6)).toFixed(1)} Z" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<rect x="${(c[0] - 22).toFixed(1)}" y="${(c[1] - 15).toFixed(1)}" width="44" height="30" fill="#fff" stroke="${INK}" stroke-width="${SW}" transform="rotate(-30 ${c[0].toFixed(1)} ${c[1].toFixed(1)})"/>`;
    const [fx, fy] = at(62, u), [nx, ny] = at(50, nrm), back = at(-22, u).map(Number), [mx, my] = at(-34, u, back);
    b += arr(c[0].toFixed(1), c[1].toFixed(1), fx, fy, 'dc', RED) + T(+fx + 4, +fy - 6, 'F', { c: RED, w: 700 });
    b += arr(c[0].toFixed(1), c[1].toFixed(1), nx, ny, 'dc', BLUE, '6 4') + T(+nx - 6, +ny - 6, 'N', { c: BLUE, w: 700, a: 'end' });
    b += arr(c[0].toFixed(1), c[1].toFixed(1), c[0].toFixed(1), (c[1] + 58).toFixed(1), 'dc') + T(c[0] + 8, c[1] + 62, 'P', { w: 700 });
    b += arr(back[0].toFixed(1), back[1].toFixed(1), mx, my, 'dc', INK, '4 3') + T(+mx - 4, +my - 8, `F${sb('ms')}`, { a: 'end', w: 700 });
    b += `<path d="M62 170 A42 42 0 0 0 56.4 149" fill="none" stroke="${INK}" stroke-width="2"/>` + T(70, 163, '30°');
    b += T(182, 158, sLab);
    return wrap('0 0 290 180', b, cap, 'Thùng trên dốc nghiêng và các lực');
  },
  // Bài tương tự Dạng 3 · giếng: mặt nước sâu 5,0 m, gàu ở 1,2 m trên mặt đất (20 đơn vị/m)
  gieng: (cap = 'Mặt đất, mặt nước giếng và chỗ gàu treo.') => {
    const Y = (z) => 64 - 20 * z;
    let b = dimDefs('gg') + `<path d="M4 ${Y(0)} H100 V${Y(-5.6)} M160 ${Y(-5.6)} V${Y(0)} H296" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<rect x="102" y="${Y(-5)}" width="56" height="${Y(-5.6) - Y(-5)}" fill="#dfe6f3"/><line x1="100" y1="${Y(-5)}" x2="160" y2="${Y(-5)}" stroke="${BLUE}" stroke-width="2.4"/>`;
    b += `<line x1="130" y1="4" x2="130" y2="${Y(1.2) - 10}" stroke="${INK}" stroke-width="2"/><path d="M118 ${Y(1.2) - 10} H142 L138 ${Y(1.2) + 10} H122 Z" fill="${INK}"/>`;
    b += T(4, Y(0) - 8, 'mặt đất') + T(170, Y(-5) + 7, 'mặt nước');
    b += dim(84, Y(0) + 2, Y(-5) - 2, 'gg') + T(16, Y(-2.5) + 7, '5,0 m');
    b += dashG(142, Y(1.2), 230, Y(1.2)) + dim(222, Y(1.2) + 2, Y(0) - 2, 'gg') + T(232, Y(0.6) + 7, '1,2 m');
    return wrap('0 0 300 180', b, cap, 'Gàu nước phía trên giếng');
  },
};
