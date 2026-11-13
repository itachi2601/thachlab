// Hình minh hoạ cho ruột tập VL11 · Bài 13 Sóng dừng (lesson 32). Cùng quy tắc với hinh-l11-bai2.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox (nhãn phụ ≥ 18), nét ≥ 2,8, phân biệt bằng nét (liền – đứt), tự vẽ.
// Chữ Hi Lạp (λ) lấy từ font KaTeX. Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh.
// Xem thử: node scripts/ruot-tap/l11-bai13.mjs --hinh (chụp vào out/hinh-l11-bai13/).
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
const gk = (ch) => `<tspan font-family="KaTeX_Math" font-style="italic">${ch}</tspan>`;
const LA = gk('λ');
const f1 = (v) => (+v).toFixed(1);
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${f1(x1)}" y1="${f1(y1)}" x2="${f1(x2)}" y2="${f1(y2)}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
const arr = (x1, y1, x2, y2, id, c = INK, w = 2.4) =>
  `<line x1="${f1(x1)}" y1="${f1(y1)}" x2="${f1(x2)}" y2="${f1(y2)}" stroke="${c}" stroke-width="${w}" marker-end="url(#${id})"/>`;
// kích thước hai đầu mũi tên (đo chiều dài)
const doDai = (x1, x2, y, id, nhan, c = INK, size = 20) =>
  arr((x1 + x2) / 2, y, x1 + 1, y, id, c, 2) + arr((x1 + x2) / 2, y, x2 - 1, y, id, c, 2)
  + ln(x1, y - 8, x1, y + 8, c, 1.8) + ln(x2, y - 8, x2, y + 8, c, 1.8)
  + `<rect x="${f1((x1 + x2) / 2 - nhan.length * 5.4 - 4)}" y="${f1(y - 13)}" width="${f1(nhan.length * 10.8 + 8)}" height="24" fill="#fff"/>`
  + T((x1 + x2) / 2, y + 7, nhan, { a: 'middle', c, size });
// tường (đầu cố định) ở x, dọc từ y1 tới y2; ben = 1 gạch sang phải, -1 sang trái
const tuong = (x, y1, y2, ben = 1) => {
  let s = ln(x, y1, x, y2, INK, 4);
  for (let y = y1 + 4; y < y2; y += 12) s += ln(x, y, x + ben * 10, y + 10, GREY, 1.8);
  return s;
};
// cọc thẳng đứng + vòng nhẹ (đầu tự do) ở x, vòng tại y
const coc = (x, y1, y2, yv) => ln(x, y1, x, y2, INK, 3.4) + `<rect x="${f1(x - 6)}" y="${f1(yv - 9)}" width="12" height="18" rx="4" fill="#fff" stroke="${INK}" stroke-width="2.4"/>`;
// sóng dừng: dây từ x0 tới x1 có `bo` bó (có thể lẻ nửa bó), biên độ amp; nét liền một lúc, nét đứt nửa chu kì sau
const songDung = (x0, x1, yc, amp, bo, { c = INK, cham = true, dut = true } = {}) => {
  const L = (x1 - x0) / bo; // dài một bó
  const p = (s) => { let d = ''; for (let k = 0; k <= 200; k++) { const x = x0 + (k / 200) * (x1 - x0); d += `${k ? 'L' : 'M'}${f1(x)},${f1(yc - s * amp * Math.sin(Math.PI * (x - x0) / L))}`; } return d; };
  let s = `<path d="${p(1)}" fill="none" stroke="${c}" stroke-width="${SW}"/>`;
  if (dut) s += `<path d="${p(-1)}" fill="none" stroke="${c}" stroke-width="2.2" stroke-dasharray="6 5"/>`;
  if (cham) for (let i = 0; i <= Math.floor(bo + 1e-9); i++) s += `<circle cx="${f1(x0 + i * L)}" cy="${yc}" r="4.5" fill="${INK}"/>`;
  return { s, L };
};

export const hinhL11b13 = {
  // Trang 1 · Dự đoán: bấm phím giữa dây đàn (không nêu tần số đổi thế nào)
  danBam: (cap = 'Trên: gảy cả dây. Dưới: bấm phím ở giữa rồi gảy; sức căng giữ nguyên.') => {
    let b = '';
    const ngua = (x, y) => `<path d="M${x - 9},${y + 12} L${x},${y} L${x + 9},${y + 12} z" fill="${GREY}"/>`;
    // dây 1: rung cả dây
    b += ngua(30, 58) + ngua(290, 58) + songDung(30, 290, 58, 22, 1, { cham: false }).s;
    b += T(160, 26, 'gảy cả dây', { a: 'middle', size: 19, c: GREY });
    // dây 2: bấm ở giữa
    const y2 = 148;
    b += ngua(30, y2) + ngua(290, y2) + ln(30, y2, 160, y2, INK, 2.2) + songDung(160, 290, y2, 22, 1, { cham: false }).s;
    b += `<ellipse cx="160" cy="${y2 - 16}" rx="11" ry="15" fill="#e9ecf3" stroke="${INK}" stroke-width="2.2"/>`;
    b += T(146, y2 - 30, 'bấm', { a: 'end', size: 19, c: RED, w: 700 });
    return wrap('0 0 320 176', b, cap, 'Dây đàn gảy cả dây và khi bấm phím ở giữa');
  },
  // Trang 1 · II.1 xung phản xạ ở đầu cố định và đầu tự do
  phanXa: (cap = 'Xung tới (liền) đi sang phải; xung phản xạ (đứt) quay lại.') => {
    let b = defs('px1');
    const xung = (xc, y, h, dash = '', c = INK) => {
      let d = ''; for (let k = 0; k <= 40; k++) { const x = xc - 30 + k * 1.5; d += `${k ? 'L' : 'M'}${f1(x)},${f1(y - h * Math.exp(-(((x - xc) / 11) ** 2)))}`; }
      return `<path d="${d}" fill="none" stroke="${c}" stroke-width="${SW}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
    };
    // hàng 1: đầu cố định
    const y1 = 66;
    b += ln(14, y1, 280, y1, INK, 2) + tuong(280, y1 - 44, y1 + 40, 1);
    b += xung(80, y1, 36) + arr(110, y1 - 30, 140, y1 - 30, 'px1') + xung(210, y1, -36, '6 4', BLUE) + arr(170, y1 + 32, 136, y1 + 32, 'px1', BLUE);
    b += T(274, 18, 'đầu cố định', { a: 'end', size: 19, w: 700 });
    // hàng 2: đầu tự do (vòng trên cọc)
    const y2 = 176;
    b += ln(14, y2, 282, y2, INK, 2) + coc(288, y2 - 50, y2 + 40, y2);
    b += xung(80, y2, 36) + arr(110, y2 - 30, 140, y2 - 30, 'px1') + xung(210, y2, 36, '6 4', BLUE) + arr(230, y2 + 22, 196, y2 + 22, 'px1', BLUE);
    b += T(270, 128, 'đầu tự do', { a: 'end', size: 19, w: 700 });
    return wrap('0 0 320 226', b, cap, 'Xung phản xạ ở đầu cố định và đầu tự do');
  },
  // Trang 2 · thí nghiệm dây thun (không ghi nút/bụng — HS điền ở Rút ra)
  dayThun: (cap = 'Dây thun rung: có chỗ đứng yên, có chỗ vồng mạnh nhất.') => {
    let b = defs('dt1');
    b += tuong(22, 50, 140, -1);
    const { s, L } = songDung(22, 282, 95, 30, 3);
    b += s;
    b += `<ellipse cx="292" cy="95" rx="13" ry="18" fill="#e9ecf3" stroke="${INK}" stroke-width="2.2"/>` + arr(292, 132, 292, 158, 'dt1', RED) + arr(292, 58, 292, 32, 'dt1', RED);
    b += doDai(22 + L, 22 + 2 * L, 166, 'dt1', 'một bó = ?', RED, 19);
    b += T(30, 30, 'chân ghế', { size: 18, c: GREY });
    return wrap('0 0 320 186', b, cap, 'Sóng dừng trên dây thun rung bằng tay');
  },
  // Trang 2 · II.3 hai trường hợp điều kiện sóng dừng
  haiTH: (cap = 'Trên: hai đầu cố định, dây có 3 bó. Dưới: đầu phải là vòng trượt trên cọc.') => {
    let b = defs('ht1');
    const y1 = 56, y2 = 170;
    b += tuong(22, y1 - 34, y1 + 34, -1) + tuong(282, y1 - 34, y1 + 34, 1) + songDung(22, 282, y1, 26, 3).s;
    b += doDai(22, 282, y1 + 46, 'ht1', 'l = 3 · ?', RED, 19);
    b += tuong(22, y2 - 34, y2 + 34, -1) + coc(290, y2 - 40, y2 + 40, y2) + songDung(22, 290, y2, 26, 1.5).s;
    b += doDai(22, 290, y2 + 46, 'ht1', 'l = 3 · ?', RED, 19);
    return wrap('0 0 320 232', b, cap, 'Sóng dừng hai đầu cố định và một đầu tự do');
  },
  // Trang 3 · II.4 bố trí máy rung đo bước sóng
  mayRung: (cap = 'Đầu A gắn máy rung (coi là nút), đầu B buộc vào giá.') => {
    let b = defs('mr1');
    b += `<rect x="6" y="66" width="44" height="54" rx="4" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(28, 144, 'máy rung', { a: 'middle', size: 18 });
    b += ln(50, 82, 60, 82, INK, 3) + songDung(60, 288, 82, 30, 2).s + tuong(288, 46, 118, 1);
    b += T(60, 40, 'A', { a: 'middle', w: 700 }) + T(276, 40, 'B', { a: 'middle', w: 700 });
    b += doDai(60, 288, 164, 'mr1', '0,80 m');
    return wrap('0 0 320 182', b, cap, 'Máy rung tạo sóng dừng trên dây hai đầu cố định');
  },
  // Trang 3 · II.6 đường bao biên độ
  bienDo: (cap = 'M cách nút gần nhất (chấm đen ở giữa) đoạn x.') => {
    let b = defs('bd1');
    const x0 = 30, x1 = 290, yc = 74, amp = 50;
    const { s, L } = songDung(x0, x1, yc, amp, 2);
    b += ln(x0 - 10, yc, x1 + 10, yc, GREY, 1.4) + s;
    // bụng thứ nhất: biên độ (đỏ, từ trục lên đỉnh) và bề rộng vùng dao động (xanh, đỉnh xuống đáy)
    const xb = x0 + L / 2;
    b += ln(xb - 20, yc - amp, xb + 26, yc - amp, GREY, 1.6) + ln(xb - 20, yc + amp, xb + 26, yc + amp, GREY, 1.6);
    b += arr(xb + 14, yc, xb + 14, yc - amp + 2, 'bd1', RED);
    b += arr(xb - 12, yc, xb - 12, yc - amp + 2, 'bd1', BLUE, 2) + arr(xb - 12, yc, xb - 12, yc + amp - 2, 'bd1', BLUE, 2);
    b += T(xb + 14, yc + amp + 26, 'biên độ', { a: 'start', size: 18, c: RED }) + T(xb - 16, yc + amp + 26, 'bề rộng', { a: 'end', size: 18, c: BLUE });
    // điểm M trên bó thứ hai
    const xm = x0 + L + L / 6, am = amp * Math.sin(Math.PI / 6);
    b += ln(xm, yc, xm, yc + am, INK, 2.2) + `<circle cx="${f1(xm)}" cy="${f1(yc + am)}" r="5" fill="#fff" stroke="${RED}" stroke-width="2.6"/>`;
    b += T(xm + 8, yc + am + 20, 'M', { w: 700, c: RED }) + doDai(x0 + L, xm, yc - 18, 'bd1', 'x', INK, 19);
    return wrap('0 0 320 156', b, cap, 'Đường bao biên độ sóng dừng');
  },
  // Trang 5 · bài toán mẫu: dây AB 1,0 m hai đầu cố định (chưa vẽ sóng — HS tự vẽ số bó)
  mauDay: (cap = 'Vẽ thêm số bó ở f = 40 Hz rồi đếm nút (kể cả A, B).') => {
    let b = defs('md1');
    b += tuong(26, 30, 110, -1) + tuong(286, 30, 110, 1) + ln(26, 70, 286, 70, INK, 2.2);
    b += T(26, 22, 'A', { a: 'middle', w: 700 }) + T(286, 22, 'B', { a: 'middle', w: 700 });
    for (let i = 1; i < 8; i++) b += ln(26 + i * 32.5, 64, 26 + i * 32.5, 76, GREY, 1.6);
    b += doDai(26, 286, 136, 'md1', '1,0 m');
    return wrap('0 0 320 156', b, cap, 'Dây AB hai đầu cố định, vạch chia 12,5 cm');
  },
  // ===== Bài tập mẫu =====
  // Dạng 2: đầu A buộc tường, đầu B vòng trượt trên cọc
  d2Vong: (cap = 'B: vòng trượt trên cọc.') => {
    let b = defs('d2');
    b += tuong(18, 34, 96, -1) + coc(196, 18, 110, 65) + ln(18, 65, 190, 65, INK, 2.4);
    b += T(30, 30, 'A', { w: 700, size: 24 }) + T(180, 30, 'B', { a: 'end', w: 700, size: 24 });
    b += doDai(18, 196, 138, 'd2', '0,9 m', INK, 24);
    return wrap('0 0 220 156', b, cap, 'Dây một đầu cố định, một đầu tự do');
  },
  // Dạng 5: dây 90 cm, 3 bó, M cách A 5 cm — đọc số trên hình
  d5Day: (cap = 'Dây AB có 3 bó.') => {
    let b = defs('d5');
    const x0 = 24, x1 = 294, yc = 56;
    b += songDung(x0, x1, yc, 34, 3).s;
    const xm = x0 + (x1 - x0) * 5 / 90;
    b += `<circle cx="${f1(xm)}" cy="${f1(yc - 34 * Math.sin(Math.PI / 6))}" r="5" fill="#fff" stroke="${RED}" stroke-width="2.6"/>` + T(xm + 2, yc - 28, 'M', { w: 700, c: RED });
    b += T(x0, yc + 30, 'A', { a: 'middle', w: 700 }) + T(x1, yc + 30, 'B', { a: 'middle', w: 700 });
    const xb = x0 + (x1 - x0) / 2;
    b += arr(xb, yc, xb, yc - 32, 'd5', BLUE, 2) + T(xb + 26, yc - 34, '4 cm', { size: 18, c: BLUE });
    b += doDai(x0, x1, 118, 'd5', '90 cm');
    return wrap('0 0 320 134', b, cap, 'Dây AB 90 cm có sóng dừng 3 bó, điểm M');
  },
  // ===== Bài tương tự =====
  // Dạng 3 · Bài 2: đọc hình — thước 0–120 cm, vạch 10 cm, số mỗi 30 cm
  tt3Hinh: (cap = 'Thước chia cm.') => {
    let b = '';
    const x0 = 22, x1 = 298, yc = 44, u = (x1 - x0) / 120;
    b += songDung(x0, x1, yc, 28, 4).s;
    const yr = 90;
    b += ln(x0, yr, x1, yr, INK, 2);
    for (let c = 0; c <= 120; c += 10) { const x = x0 + c * u; b += ln(x, yr, x, yr + (c % 30 ? 8 : 14), INK, 1.8); if (c % 30 === 0) b += T(x, yr + 34, String(c), { a: 'middle', size: 19 }); }
    return wrap('0 0 320 132', b, cap, 'Sóng dừng trên dây đặt cạnh thước');
  },
};
