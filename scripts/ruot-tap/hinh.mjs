// Hình minh hoạ cho ruột tập in (SVG nét, in đen–trắng vẫn đọc được). Quy tắc: mỗi hình trả lời đúng MỘT câu hỏi (H1), nhãn đặt
// ngay trên hình (H3), phân biệt hạt bằng HÌNH DẠNG (prôtôn đặc có "+", nơtron rỗng), không chỉ bằng màu (M4). Hình đứng cạnh câu
// nó minh hoạ (N8), không có hình trang trí. Tự vẽ, không chép SGK (docs/AGENTS-CHUYEN-DE.md mục bản quyền).
// CỠ CHỮ TRONG HÌNH: hình in rộng 40–46 mm, viewBox rộng ~300 đơn vị → 1 đơn vị ≈ 0,15 mm, nên chữ phải ≥ 20 đơn vị mới ra ≈ 3 mm
// (≈ 8,5 pt, bằng --fs-sm). Lần đầu vẽ chữ 10–11 đơn vị ra 1,5 mm, không đọc được — đừng lặp lại. Nét ≥ 2,5 đơn vị (≈ 0,4 mm).
// Dùng: `${hinh.laVang()}` trả về <figure class="fig">…</figure>; truyền chú thích riêng: hinh.laVang('chú thích khác').
// Bài sau thêm hàm mới vào đây, giữ cùng bộ màu/nét; kiểm bằng `node scripts/ruot-tap/xem-hinh.mjs` (chụp từng hình ở cỡ in thật).
const INK = '#1c2540', RED = '#b3261e', BLUE = '#1f5fa8', GREY = '#8a94ad';
const FS = 20; // ≈ 3 mm khi hình rộng 46 mm
const SW = 2.8;
const t = (x, y, s, { c = INK, size = FS, a = 'start', w = 400 } = {}) =>
  `<text x="${x}" y="${y}" fill="${c}" font-size="${size}" text-anchor="${a}" font-weight="${w}">${s}</text>`;
// Kí hiệu hạt nhân ^A_Z X: A trên, Z dưới, cùng cột bên trái X
const nuc = (x, y, A, Z, X, size = 24) => {
  const s = size * .6, w = s * .58 * Math.max(String(A).length, String(Z).length);
  return `<text font-size="${s}" fill="${INK}" font-weight="700" text-anchor="end"><tspan x="${x + w}" y="${y - size * .45}">${A}</tspan><tspan x="${x + w}" y="${y + size * .25}">${Z}</tspan></text>`
    + `<text x="${x + w + 2}" y="${y}" font-size="${size}" fill="${INK}" font-weight="700">${X}</text>`;
};
const p = (x, y, r = 11) => `<circle cx="${x}" cy="${y}" r="${r}" fill="${RED}"/>${t(x, y + r * .5, '+', { c: '#fff', size: r * 1.5, a: 'middle', w: 700 })}`;
const n = (x, y, r = 11) => `<circle cx="${x}" cy="${y}" r="${r}" fill="#fff" stroke="${BLUE}" stroke-width="${SW}"/>`;
const defs = (id) => `<defs><marker id="${id}" markerWidth="7" markerHeight="7" refX="5.5" refY="3.5" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L7,3.5 L0,7 z" fill="context-stroke"/></marker></defs>`;
const wrap = (vb, body, cap, label) =>
  `<figure class="fig"><svg viewBox="${vb}" role="img" aria-label="${label}">${body}</svg>${cap ? `<figcaption>${cap}</figcaption>` : ''}</figure>`;

export const hinh = {
  // Trang 1 · Dự đoán: chùm alpha gặp lá vàng, ba số phận
  laVang: (cap = 'Chùm hạt alpha bắn vào lá vàng mỏng: ba số phận của hạt.') => {
    let b = defs('al');
    b += `<rect x="4" y="78" width="66" height="40" rx="4" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + t(37, 105, 'nguồn', { a: 'middle', size: 18 });
    b += `<rect x="186" y="14" width="9" height="150" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + t(190, 190, 'lá vàng', { a: 'middle', size: 18 });
    b += `<line x1="70" y1="98" x2="312" y2="98" stroke="${INK}" stroke-width="${SW}" marker-end="url(#al)"/>` + t(312, 128, 'hầu hết', { a: 'end', size: 18 }) + t(312, 148, 'bay thẳng', { a: 'end', size: 18 });
    b += `<path d="M70,90 L190,74 L306,20" fill="none" stroke="${INK}" stroke-width="${SW}" stroke-dasharray="6 4" marker-end="url(#al)"/>` + t(80, 46, 'vài hạt lệch', { size: 18 });
    b += `<path d="M70,106 L190,122 L96,174" fill="none" stroke="${RED}" stroke-width="${SW}" marker-end="url(#al)"/>` + t(8, 160, 'rất hiếm:', { c: RED, size: 18 }) + t(8, 180, 'bật ngược', { c: RED, size: 18 });
    b += `<circle cx="190" cy="74" r="5" fill="${RED}"/><circle cx="190" cy="122" r="5" fill="${RED}"/>`;
    return wrap('0 0 320 196', b, cap, 'Thí nghiệm lá vàng của Rutherford');
  },
  // Trang 2 · Đồng vị: ba hạt nhân hiđrô
  dongViH: (cap = 'Ba đồng vị của hiđrô: cùng 1 prôtôn (đặc, +), khác số nơtron (rỗng).') => {
    let b = '';
    const nhom = [[50, 1, [p(50, 46)]], [160, 2, [p(148, 46), n(172, 46)]], [270, 3, [p(270, 34), n(256, 58), n(284, 58)]]];
    for (const [x, A, hat] of nhom) {
      b += `<circle cx="${x}" cy="46" r="34" fill="none" stroke="${GREY}" stroke-width="1.6" stroke-dasharray="4 4"/>` + hat.join('');
      b += nuc(x - 18, 118, A, 1, 'H', 26);
    }
    return wrap('0 0 320 128', b, cap, 'Ba đồng vị của hiđrô');
  },
  // Trang 5 · Thử thách ★★★: sân vận động và hạt đậu
  kichThuoc: (cap = 'Nếu nguyên tử to bằng sân vận động (100 m) thì hạt nhân chỉ bằng hạt đậu (1 mm) giữa sân.') => {
    let b = `<ellipse cx="150" cy="84" rx="140" ry="54" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<ellipse cx="150" cy="84" rx="118" ry="40" fill="none" stroke="${GREY}" stroke-width="1.6" stroke-dasharray="4 4"/>`;
    b += `<circle cx="150" cy="84" r="3.5" fill="${RED}"/>`;
    b += `<line x1="153" y1="81" x2="200" y2="40" stroke="${RED}" stroke-width="2"/>` + t(206, 30, 'hạt nhân', { c: RED, size: 18 }) + t(206, 50, '~10⁻¹⁵ m', { c: RED, size: 18 });
    b += t(150, 170, 'nguyên tử ~10⁻¹⁰ m', { a: 'middle', size: 18 });
    return wrap('0 0 300 178', b, cap, 'So sánh kích thước nguyên tử và hạt nhân');
  },
  // Trang 4 · Bài toán mẫu: nhãn treo trên mẫu kim loại
  nhanKimLoai: (cap = '') => {
    let b = `<path d="M8,12 L160,12 L196,56 L160,100 L8,100 z" fill="#fff" stroke="${INK}" stroke-width="${SW}"/><circle cx="28" cy="56" r="7" fill="none" stroke="${INK}" stroke-width="2.4"/>`;
    b += nuc(48, 52, 27, 13, 'Al', 30) + t(100, 88, '26,98 g/mol', { size: 17, a: 'middle' });
    return wrap('0 0 204 112', b, cap, 'Nhãn mẫu kim loại nhôm');
  },
  // Trang 6 · Dạng 3: bán kính tăng theo A^{1/3}, chậm hơn A rất nhiều — để trống tỉ số cho HS điền
  banKinh: (cap = 'Số khối tăng 3,7 lần (64 → 238) nhưng bán kính chỉ tăng ∛3,7 ≈ ? lần. Ước lượng rồi tính ở câu c).') => {
    const k = 11, rZn = k * Math.cbrt(64), rU = k * Math.cbrt(238); // 44 · 68
    let b = `<circle cx="64" cy="82" r="${rZn.toFixed(1)}" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<circle cx="236" cy="82" r="${rU.toFixed(1)}" fill="none" stroke="${INK}" stroke-width="${SW}"/>`;
    b += `<line x1="64" y1="82" x2="${(64 + rZn).toFixed(1)}" y2="82" stroke="${RED}" stroke-width="${SW}"/><line x1="236" y1="82" x2="${(236 + rU).toFixed(1)}" y2="82" stroke="${RED}" stroke-width="${SW}"/>`;
    b += t(84, 74, 'R', { c: RED, size: 20, w: 700 }) + t(266, 74, 'R′', { c: RED, size: 20, w: 700 });
    b += nuc(36, 178, 64, 30, 'Zn', 26) + nuc(206, 178, 238, 92, 'U', 26);
    b += t(150, 30, 'R′/R = ?', { a: 'middle', size: 22, w: 700 });
    return wrap('0 0 320 190', b, cap, 'Hai hạt nhân kẽm và urani vẽ đúng tỉ lệ bán kính');
  },
  // Trang 7 · Dạng 5: khối lượng trung bình là "điểm cân" giữa hai đồng vị
  canDongVi: (cap = 'Khối lượng trung bình 10,811 u nằm gần ¹¹B hơn → đồng vị nào chiếm phần trăm lớn hơn?') => {
    const x0 = 36, x1 = 284, f = (u) => x0 + (u - 10) * (x1 - x0) / 1.1; // thang 10,0 → 11,1 u
    let b = `<line x1="${x0}" y1="70" x2="${x1}" y2="70" stroke="${INK}" stroke-width="${SW + 1}"/>`;
    for (const [u, lab, A] of [[10.013, '10,013 u', 10], [11.009, '11,009 u', 11]]) {
      const x = f(u);
      b += `<rect x="${x - 26}" y="14" width="52" height="46" rx="4" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + nuc(x - 20, 46, A, 5, 'B', 24);
      b += t(x, 96, lab, { a: 'middle', size: 18 });
    }
    const xm = f(10.811);
    b += `<path d="M${xm},74 L${xm - 14},106 L${xm + 14},106 z" fill="${RED}"/>` + t(xm - 30, 128, '10,811 u (trung bình)', { a: 'middle', size: 18, c: RED, w: 700 });
    return wrap('0 0 320 136', b, cap, 'Hai đồng vị bo trên một thanh cân, điểm tựa tại khối lượng trung bình');
  },
};
