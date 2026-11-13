// Hình minh hoạ cho ruột tập VL10 · Bài 17 Trọng lực và lực căng (lesson 62). Cùng quy tắc với hinh.mjs/hinh-l10-bai23.mjs:
// mỗi hình trả lời MỘT câu hỏi, chữ ≥ 20 đơn vị viewBox, nét ≥ 2,8, tự vẽ (trừ ảnh dây dọi thật từ book/assets/anh-that, Wikimedia CC BY-SA 4.0).
// Chú thích không lộ đáp án ô Dự đoán / ô điền đứng cạnh. Xem thử: node scripts/ruot-tap/l10-bai17.mjs --hinh (chụp vào out/hinh-l10-bai17/).
import { dirname, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { ve } from './hinh.mjs';
const { t, defs, wrap, INK, RED, BLUE, GREY, SW } = ve;
const T = (x, y, s, o = {}) => t(x, y, s, { size: 20, ...o });
const sb = (s) => `<tspan font-size="15" dy="5">${s}</tspan><tspan dy="-5"> </tspan>`;
const f1 = (v) => (+v).toFixed(1);
const arr = (x1, y1, x2, y2, id, c = INK, dash = '') =>
  `<line x1="${f1(x1)}" y1="${f1(y1)}" x2="${f1(x2)}" y2="${f1(y2)}" stroke="${c}" stroke-width="${SW}"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#${id})"/>`;
const ln = (x1, y1, x2, y2, c = INK, w = SW, dash = '') =>
  `<line x1="${f1(x1)}" y1="${f1(y1)}" x2="${f1(x2)}" y2="${f1(y2)}" stroke="${c}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`;
// trần/tường gạch chéo: đoạn ngang (x1→x2) tại y, gạch phía trên
const tran = (x1, x2, y) => ln(x1, y, x2, y) + Array.from({ length: Math.floor((x2 - x1) / 16) }, (_, i) =>
  ln(x1 + i * 16, y, x1 + 8 + i * 16, y - 8, GREY, 1.8)).join('');
// mặt bàn/sàn: gạch phía dưới
const san = (x1, x2, y) => ln(x1, y, x2, y) + Array.from({ length: Math.floor((x2 - x1) / 16) }, (_, i) =>
  ln(x1 + 8 + i * 16, y, x1 + i * 16, y + 8, GREY, 1.8)).join('');
const hop = (x, y, w, h, lab = '', o = {}) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="3" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`
  + (lab ? T(x + w / 2, y + h / 2 + 7, lab, { a: 'middle', w: 700, ...o }) : '');
const rongRoc = (x, y, r = 16) => `<circle cx="${x}" cy="${y}" r="${r}" fill="#fff" stroke="${INK}" stroke-width="${SW}"/><circle cx="${x}" cy="${y}" r="3" fill="${INK}"/>`;
const ANH = resolve(dirname(fileURLToPath(import.meta.url)), '../../book/assets/anh-that');

// Hệ A trên bàn nhẵn nối B treo qua ròng rọc ở mép bàn. la, lb: nhãn khối lượng; mui: vẽ chiều chuyển động (nét đứt xanh)
const heBan = (cap, { la = 'A', lb = 'B', ga = '', gb = '', mui = true, id = 'hb' } = {}) => {
  let b = defs(id + 'a');
  b += san(4, 232, 92);
  b += hop(56, 48, 78, 44, la);
  b += ln(232, 92, 250, 78, INK, 2.4) + rongRoc(250, 78, 15);
  b += ln(134, 63, 250, 63, INK, 2.2) + ln(265, 78, 265, 114, INK, 2.2);
  b += hop(243, 114, 44, 38, lb);
  if (ga) b += T(95, 38, ga, { a: 'middle' });
  if (gb) b += T(236, 140, gb, { a: 'end' });
  if (mui) b += arr(70, 126, 150, 126, id + 'a', BLUE, '6 4') + arr(304, 114, 304, 160, id + 'a', BLUE, '6 4');
  return wrap('0 0 320 166', b, cap, 'Khối A trên bàn nhẵn nối vật B treo qua ròng rọc ở mép bàn');
};
// Hai vật treo hai bên ròng rọc cố định
const atwood = (cap, { l1 = `m${sb('1')}`, l2 = `m${sb('2')}`, id = 'aw' } = {}) => {
  let b = tran(70, 190, 14) + ln(130, 14, 130, 30, INK, 2.4) + rongRoc(130, 50, 20);
  b += ln(110, 50, 110, 108, INK, 2.2) + ln(150, 50, 150, 108, INK, 2.2);
  b += hop(90, 108, 40, 46, '') + hop(134, 108, 32, 34, '');
  b += T(82, 138, l1, { a: 'end', w: 700, size: 22 }) + T(174, 130, l2, { w: 700, size: 22 });
  b += ln(40, 108, 220, 108, GREY, 1.6, '5 4');
  return wrap('0 0 260 160', b, cap, 'Hai vật treo hai đầu dây vắt qua ròng rọc cố định');
};

export const hinhL10b17 = {
  // Trang 1 · Dự đoán: đĩa CD treo trên đinh (không vẽ đường kéo dài, không đánh dấu tâm)
  diaCD: (cap = 'Đĩa CD treo đứng yên trên đinh, dây buộc ở mép đĩa.') => {
    let b = `<rect x="0" y="0" width="200" height="232" fill="#f3f5fa"/>`;
    b += `<circle cx="100" cy="22" r="5" fill="${INK}"/>` + T(112, 28, 'đinh');
    b += ln(100, 22, 100, 70, INK, 2.2) + T(108, 56, 'dây');
    b += `<circle cx="100" cy="146" r="76" fill="#fff" stroke="${INK}" stroke-width="${SW}"/><circle cx="100" cy="146" r="22" fill="none" stroke="${GREY}" stroke-width="1.8"/>`;
    b += `<circle cx="100" cy="146" r="9" fill="#f3f5fa" stroke="${INK}" stroke-width="2.2"/>`;
    b += `<circle cx="100" cy="70" r="3.5" fill="${INK}"/>`;
    return wrap('0 0 200 232', b, cap, 'Đĩa CD treo bằng dây buộc ở mép');
  },
  // Trang 1 · ảnh thật dây dọi
  dayDoi: (cap = 'Dây dọi: quả nặng treo đứng yên.') => `<figure class="fig"><img src="${pathToFileURL(resolve(ANH, 'day-doi.jpg')).href}" alt="Dây dọi" style="display:block;width:100%;height:auto;filter:grayscale(1)"><figcaption>${cap}<br><span style="font-size:2.4mm">Ảnh: SpeakingArch · Wikimedia · CC BY-SA 4.0</span></figcaption></figure>`,
  // Trang 1 · trọng lực ở nhiều nơi trên Trái Đất
  traiDat: (cap = 'Trọng lực ở bốn nơi trên Trái Đất (không theo tỉ lệ).') => {
    let b = defs('tda');
    b += `<circle cx="120" cy="110" r="70" fill="#fff" stroke="${INK}" stroke-width="${SW}"/><circle cx="120" cy="110" r="4" fill="${INK}"/>` + T(128, 132, 'tâm');
    for (const g of [90, 0, 210, 320]) {
      const r = (g * Math.PI) / 180, c = Math.cos(r), s = Math.sin(r);
      const x0 = 120 + 100 * c, y0 = 110 - 100 * s;
      b += `<circle cx="${f1(x0)}" cy="${f1(y0)}" r="7" fill="#fff" stroke="${INK}" stroke-width="2.2"/>`;
      b += arr(x0 - 9 * c, y0 + 9 * s, 120 + 74 * c, 110 - 74 * s, 'tda', RED);
    }
    b += T(132, 22, 'P', { c: RED, w: 700 });
    return wrap('0 0 240 220', b, cap, 'Trọng lực hướng về tâm Trái Đất ở mọi nơi');
  },
  // Trang 2 · thí nghiệm tìm trọng tâm bằng dây dọi
  biaDayDoi: (cap = 'Treo ở A, kẻ theo dây dọi; rồi treo ở B, kẻ tiếp.') => {
    const A = [62, 46], B = [196, 62], G = [120, 116];
    let b = `<path d="M38,32 L204,40 L222,124 L150,190 L56,176 L22,98 z" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    const ext = (P, k) => [G[0] + k * (G[0] - P[0]), G[1] + k * (G[1] - P[1])];
    const ea = ext(A, 0.75), eb = ext(B, 0.6);
    b += ln(A[0], A[1], ea[0], ea[1], BLUE, 2.4, '7 5') + ln(B[0], B[1], eb[0], eb[1], BLUE, 2.4, '7 5');
    for (const [P, l, dx] of [[A, 'A', 10], [B, 'B', -26]]) b += `<circle cx="${P[0]}" cy="${P[1]}" r="5" fill="#fff" stroke="${INK}" stroke-width="2.2"/>` + T(P[0] + dx, P[1] + 8, l, { w: 700 });
    b += `<circle cx="${G[0]}" cy="${G[1]}" r="5" fill="${RED}"/>` + T(G[0] + 10, G[1] + 22, 'G', { c: RED, w: 700 });
    return wrap('0 0 240 200', b, cap, 'Tấm bìa với hai đường dây dọi cắt nhau');
  },
  // Trang 2 · lực kế treo quả nặng
  lucKe: (cap = 'Lực kế 0–2,5 N, vạch chia 0,05 N; treo thêm từng quả 50 g.') => {
    let b = tran(40, 160, 12) + ln(100, 12, 100, 28, INK, 2.4);
    b += `<rect x="82" y="28" width="36" height="104" rx="5" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>`;
    for (let i = 0; i <= 10; i++) b += ln(104, 40 + i * 8, i % 2 ? 112 : 116, 40 + i * 8, INK, 1.6);
    b += ln(92, 40, 92, 104, GREY, 2.4) + ln(100, 132, 100, 146, INK, 2.2);
    for (let i = 0; i < 4; i++) b += `<rect x="86" y="${146 + i * 17}" width="28" height="15" rx="2" fill="#fff" stroke="${INK}" stroke-width="2.4"/>`;
    b += T(124, 184, '4 × 50 g');
    return wrap('0 0 220 218', b, cap, 'Lực kế treo các quả nặng');
  },
  // Trang 3 · đèn treo trần: HS tự vẽ hai lực căng (chỉ đánh dấu điểm đặt)
  denTreo: (cap = 'Vẽ T lên đèn (điểm 1) và lên móc (điểm 2).') => {
    let b = tran(30, 190, 16) + `<rect x="92" y="16" width="16" height="10" fill="#fff" stroke="${INK}" stroke-width="2.2"/>`;
    b += ln(100, 26, 100, 100, INK, 2.2);
    b += `<path d="M100,100 L62,138 L138,138 z" fill="#fff" stroke="${INK}" stroke-width="${SW}"/><circle cx="100" cy="148" r="10" fill="#fff" stroke="${INK}" stroke-width="2.2"/>`;
    b += `<circle cx="100" cy="100" r="4.5" fill="${RED}"/>` + T(112, 98, '1', { c: RED, w: 700 });
    b += `<circle cx="100" cy="27" r="4.5" fill="${RED}"/>` + T(112, 50, '2', { c: RED, w: 700 });
    return wrap('0 0 200 166', b, cap, 'Đèn treo trần bằng dây');
  },
  // Trang 3 · thí nghiệm lực kế qua ròng rọc: ba hướng kéo
  rongRocLucKe: (cap = 'Kéo lực kế theo hướng 1, 2, 3.') => {
    let b = tran(20, 120, 14) + ln(70, 14, 70, 34, INK, 2.4) + rongRoc(70, 50, 16);
    b += ln(54, 50, 54, 108, INK, 2.2) + hop(38, 108, 32, 28, '');
    b += ln(86, 50, 86, 130, INK, 2.2, '5 4') + T(94, 134, '1');
    b += ln(83, 58, 150, 125, INK, 2.2, '5 4') + T(158, 134, '2');
    b += ln(70, 34, 210, 34, INK, 2.2, '5 4') + T(214, 40, '3');
    b += `<rect x="168" y="22" width="40" height="24" rx="4" fill="#fff" stroke="${INK}" stroke-width="2.4"/>`;
    return wrap('0 0 240 144', b, cap, 'Dây vắt qua ròng rọc, lực kế kéo theo ba hướng');
  },
  // Trang 3 · hệ vật nối dây (lý thuyết)
  heLyThuyet: (cap = 'Nét đứt: chiều chuyển động.') => heBan(cap, { id: 'hl' }),
  // Trang 3 · bẫy 3: con lắc lệch (vẽ T)
  conLac: (cap = 'Vẽ T lên quả cầu.') => {
    let b = tran(20, 140, 14) + ln(80, 14, 132, 120, INK, 2.2) + ln(80, 14, 80, 130, GREY, 1.6, '5 4');
    b += `<circle cx="138" cy="132" r="14" fill="#fff" stroke="${INK}" stroke-width="${SW}"/><circle cx="133" cy="121" r="3.5" fill="${RED}"/>`;
    return wrap('0 0 180 156', b, cap, 'Con lắc đang lệch sang phải');
  },
  // Trang 4 · bài toán mẫu
  vdMau: (cap = 'Bàn nhẵn, B treo, thả từ nghỉ.') => heBan(cap, { ga: '2 kg', gb: '0,5 kg', id: 'vm' }),
  // Trang 5 · thử thách ★★★
  atwoodTT: (cap = 'Thả từ nghỉ: vật nào đi xuống?') => atwood(cap, { l1: '3 kg', l2: '2 kg', id: 'awt' }),

  // ===== Bài tập mẫu =====
  toiCap: (cap = 'Mỗi giai đoạn: a hướng lên hay xuống?', kg = '800 kg', xuong = false) => {
    let b = defs('tc1') + tran(40, 180, 14) + ln(110, 14, 110, 24, INK, 2.4);
    b += `<circle cx="110" cy="40" r="16" fill="#fff" stroke="${INK}" stroke-width="${SW}"/>` + T(134, 46, 'tời');
    b += ln(110, 56, 110, 84, INK, 2.2) + hop(66, 84, 88, 50, kg, { size: 20 });
    b += (xuong ? arr(178, 86, 178, 134, 'tc1', BLUE, '6 4') : arr(178, 134, 178, 86, 'tc1', BLUE, '6 4')) + T(186, 116, 'v', { c: BLUE, w: 700 });
    return wrap('0 0 220 144', b, cap, 'Tời nâng thùng hàng bằng cáp thẳng đứng');
  },
  heD3: (cap = 'm<sub>A</sub> = 1,5 kg; m<sub>B</sub> = 1,0 kg.') => heBan(cap, { id: 'd3' }),
  atwoodD4: (cap = 'm<sub>1</sub> = 5,0 kg; m<sub>2</sub> = 3,0 kg; thả từ cùng độ cao.') => atwood(cap, { id: 'aw4' }),
  heD5: (cap = 'Dây chịu tối đa 12 N; m<sub>B</sub> chưa biết.') => heBan(cap, { gb: 'm = ?', id: 'd5' }),
  // ===== Bài tương tự =====
  heTT: (cap = 'Bàn nhẵn, dây nhẹ không dãn.') => heBan(cap, { id: 'htt', mui: false }),
  atwoodTT2: (cap = 'Ròng rọc cố định nhẹ, nhẵn.') => atwood(cap, { id: 'awt2' }),
};
