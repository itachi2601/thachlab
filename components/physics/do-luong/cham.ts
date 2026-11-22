/**
 * components/physics/do-luong/cham.ts — số học phần chấm của bốn dụng cụ đo (Gói A). Không React để thử bằng `npx tsx`.
 * Mọi phép tính làm trên SỐ NGUYÊN đơn vị nhỏ (phần trăm mm…) để tránh lỗi dấu phẩy động (0,1 + 0,2).
 * Quy ước ghi kết quả theo L10 Bài 3 (lesson 48): số chữ số sau dấu phẩy do dụng cụ quyết định (Bẫy 3 "ghi thêm số 0").
 */

import { docSo, soNguyenRaChuoi, type KetQuaCham } from "./chung";

/* ---------------- Thước kẹp ---------------- */

/** Ba loại du xích: p = độ chính xác (phần trăm mm), N vạch dài `len` mm → mỗi khoảng du xích = len/N mm. */
export const DU_XICH = {
  10: { pH: 10, N: 10, len: 9, nhanMoi: 5, decimals: 1, ten: "0,1 mm" },
  5: { pH: 5, N: 20, len: 19, nhanMoi: 4, decimals: 2, ten: "0,05 mm" },
  2: { pH: 2, N: 50, len: 49, nhanMoi: 5, decimals: 2, ten: "0,02 mm" },
} as const;
export type LoaiDuXich = keyof typeof DU_XICH;

/** Tách số đọc (phần trăm mm) thành phần nguyên n (mm) và số thứ tự vạch du xích trùng k. */
export function tachThuocKep(zH: number, pH: LoaiDuXich) {
  const n = Math.floor(zH / 100);
  const k = (zH - n * 100) / pH;
  return { n, k };
}

/** Chuỗi số đọc đúng cách ghi của loại du xích: (1234, 2) → "12,34"; (1230, 10) → "12,3". */
export function ghiThuocKep(zH: number, pH: LoaiDuXich) {
  const d = DU_XICH[pH].decimals;
  return soNguyenRaChuoi(d === 1 ? zH / 10 : zH, d);
}

/**
 * Chấm số học sinh gõ cho số đọc thật zH (phần trăm mm). null = gõ không phải số.
 * Đúng giá trị nhưng sai số chữ số sau dấu phẩy → "chu-so" (không tính vào chuỗi đúng).
 */
export function chamThuocKep(raw: string, zH: number, pH: LoaiDuXich): KetQuaCham | null {
  const so = docSo(raw);
  if (!so) return null;
  const { N, decimals, ten } = DU_XICH[pH];
  const { n, k } = tachThuocKep(zH, pH);
  const dapAn = `${ghiThuocKep(zH, pH)} mm`;
  const xH = k * pH;
  const phanLe = `${k} × ${soNguyenRaChuoi(pH, 2).replace(/0$/, "")} = ${soNguyenRaChuoi(decimals === 1 ? xH / 10 : xH, decimals)} mm`;

  const sH = Math.round(so.value * 100);
  const chinhXacToiPhanTram = Math.abs(so.value * 100 - sH) < 1e-6;

  if (chinhXacToiPhanTram && sH === zH) {
    if (so.decimals === decimals) return { loai: "dung", loi: `Số đọc ${dapAn}.` };
    return {
      loai: "chu-so",
      loi: `Du xích ${ten} cho kết quả tới ${decimals === 1 ? "một" : "hai"} chữ số sau dấu phẩy: ghi ${dapAn}. Chữ số cuối cho biết dụng cụ đo tới đâu.`,
    };
  }

  const nHs = Math.floor(so.value + 1e-9);
  if (nHs !== n) {
    if (k === 0 && nHs === n + 1) {
      return {
        loai: "sai",
        loi: `Vạch 0 du xích trùng đúng vạch ${n} mm (vạch cuối du xích cũng trùng, đừng đếm vạch cuối). Phần lẻ bằng 0: ${dapAn}.`,
      };
    }
    if (nHs === n + 1) {
      return {
        loai: "sai",
        loi: `Phần nguyên lấy vạch thước chính ngay TRƯỚC vạch 0 du xích (${n} mm), không lấy vạch sau nó. Đáp số ${dapAn}.`,
      };
    }
    return {
      loai: "sai",
      loi: `Phần nguyên: vạch 0 du xích nằm sau vạch ${n} mm của thước chính → ${n} mm. Phần lẻ: vạch số ${k} trùng, ${phanLe}. Đáp số ${dapAn}.`,
    };
  }

  const leHs = sH - n * 100;
  if (chinhXacToiPhanTram && leHs % pH === 0 && leHs / pH <= N) {
    const kHs = leHs / pH;
    return {
      loai: "sai",
      loi: `Phần nguyên ${n} mm đúng. Em lấy vạch du xích số ${kHs}; vạch thẳng hàng nhất là vạch số ${k}: ${phanLe}. Đáp số ${dapAn}.`,
    };
  }
  return {
    loai: "sai",
    loi: `Phần nguyên ${n} mm đúng. Phần lẻ = số thứ tự vạch du xích trùng × ${ten}; vạch số ${k} trùng nên ${phanLe}. Đáp số ${dapAn}.`,
  };
}

/** Số đọc ngẫu nhiên (phần trăm mm), n ≤ maxN; ~15% ca vạch 0 trùng, ~10% ca vạch kế cuối trùng (ca biên). */
export function ngauNhienThuocKep(pH: LoaiDuXich, maxN: number, tranh?: number): number {
  const { N } = DU_XICH[pH];
  for (let lan = 0; lan < 20; lan++) {
    const n = Math.floor(Math.random() * (maxN + 1));
    const r = Math.random();
    const k = r < 0.15 ? 0 : r < 0.25 ? N - 1 : 1 + Math.floor(Math.random() * (N - 2));
    const z = n * 100 + k * pH;
    if (z !== tranh) return z;
  }
  return 0;
}

/* ---------------- Panme ---------------- */

/** Tách số đọc panme (phần trăm mm): m = vạch mm cuối lộ ra, nua = 1 nếu vạch nửa mm sau nó đã lộ ra, k = vạch thước tròn (0..49). */
export function tachPanme(zH: number) {
  const m = Math.floor(zH / 100);
  const du = zH - m * 100;
  const nua = du >= 50 ? 1 : 0;
  return { m, nua, k: du - nua * 50 };
}

export const ghiPanme = (zH: number) => soNguyenRaChuoi(zH, 2);

function giaiPanme(zH: number) {
  const { m, nua, k } = tachPanme(zH);
  return `${m} mm${nua ? " + 0,50 mm" : ""} + ${k} × 0,01 mm = ${ghiPanme(zH)} mm`;
}

/** Chấm số đọc panme. Ba lỗi hay gặp: quên/thừa 0,5 mm, đọc sai vạch mm trên ống, đọc sai vạch thước tròn. */
export function chamPanme(raw: string, zH: number): KetQuaCham | null {
  const so = docSo(raw);
  if (!so) return null;
  const { m, nua, k } = tachPanme(zH);
  const dapAn = `${ghiPanme(zH)} mm`;
  const sH = Math.round(so.value * 100);
  const chinhXac = Math.abs(so.value * 100 - sH) < 1e-6;

  if (chinhXac && sH === zH) {
    if (so.decimals === 2) return { loai: "dung", loi: `Số đọc ${dapAn}.` };
    return {
      loai: "chu-so",
      loi: `Panme đo tới 0,01 mm nên ghi đủ hai chữ số sau dấu phẩy: ${dapAn}. Chữ số cuối cho biết dụng cụ đo tới đâu.`,
    };
  }
  if (chinhXac && nua === 1 && sH === zH - 50) {
    return {
      loai: "sai",
      loi: `Em quên vạch nửa milimét: dưới đường ngang, sau vạch ${m} mm đã lộ ra một vạch nữa nên cộng thêm 0,50 mm. ${giaiPanme(zH)}.`,
    };
  }
  if (chinhXac && nua === 0 && sH === zH + 50) {
    return {
      loai: "sai",
      loi: `Vạch nửa milimét sau vạch ${m} mm chưa lộ ra (mép thước tròn còn che) nên không cộng 0,50 mm. ${giaiPanme(zH)}.`,
    };
  }
  if (chinhXac && sH >= 0) {
    const t = tachPanme(sH);
    if (t.m !== m) {
      return {
        loai: "sai",
        loi: `Vạch milimét cuối cùng lộ ra trên ống (trên đường ngang) là vạch ${m} mm, không phải ${t.m} mm. ${giaiPanme(zH)}.`,
      };
    }
    if (t.nua === nua) {
      return {
        loai: "sai",
        loi: `Phần milimét đúng. Trên thước tròn, vạch nằm đúng đường ngang là vạch số ${k} (em lấy vạch ${t.k}). ${giaiPanme(zH)}.`,
      };
    }
  }
  return { loai: "sai", loi: `Đọc lần lượt: ${giaiPanme(zH)}.` };
}

/** Số đọc panme ngẫu nhiên (phần trăm mm, ≤ maxMm,99); ~20% thước tròn gần vạch 0 (0–2), ~15% gần vạch 49 (47–49). */
export function ngauNhienPanme(maxMm: number, tranh?: number): number {
  for (let lan = 0; lan < 20; lan++) {
    const m = Math.floor(Math.random() * (maxMm + 1));
    const nua = Math.random() < 0.5 ? 1 : 0;
    const r = Math.random();
    const k = r < 0.2 ? Math.floor(Math.random() * 3) : r < 0.35 ? 47 + Math.floor(Math.random() * 3) : Math.floor(Math.random() * 50);
    const z = m * 100 + nua * 50 + k;
    if (z !== tranh) return z;
  }
  return 0;
}

/* ---------------- Đồng hồ đo điện đa năng ---------------- */

export type DaiLuongDH = "DCV" | "ACV" | "DCA" | "OHM";
export type LoCam = "10A" | "mA" | "VΩ";
export type CachMac = "song-song" | "noi-tiep";
export type ThangDo = { T: number; donVi: string; heSo: number; decimals: number; ten: string };

/** Thang đo kiểu đồng hồ 3½ chữ số (2000 số đếm). Số trên màn = giá trị / heSo, làm tròn `decimals` chữ số. */
export const THANG_DH: Record<DaiLuongDH, ThangDo[]> = {
  DCV: [
    { T: 2, donVi: "V", heSo: 1, decimals: 3, ten: "2 V" },
    { T: 20, donVi: "V", heSo: 1, decimals: 2, ten: "20 V" },
    { T: 200, donVi: "V", heSo: 1, decimals: 1, ten: "200 V" },
    { T: 1000, donVi: "V", heSo: 1, decimals: 0, ten: "1000 V" },
  ],
  ACV: [
    { T: 200, donVi: "V", heSo: 1, decimals: 1, ten: "200 V" },
    { T: 750, donVi: "V", heSo: 1, decimals: 0, ten: "750 V" },
  ],
  DCA: [
    { T: 0.002, donVi: "mA", heSo: 1e-3, decimals: 3, ten: "2 mA" },
    { T: 0.02, donVi: "mA", heSo: 1e-3, decimals: 2, ten: "20 mA" },
    { T: 0.2, donVi: "mA", heSo: 1e-3, decimals: 1, ten: "200 mA" },
    { T: 10, donVi: "A", heSo: 1, decimals: 2, ten: "10 A" },
  ],
  OHM: [
    { T: 200, donVi: "Ω", heSo: 1, decimals: 1, ten: "200 Ω" },
    { T: 2000, donVi: "kΩ", heSo: 1e3, decimals: 3, ten: "2 kΩ" },
    { T: 20000, donVi: "kΩ", heSo: 1e3, decimals: 2, ten: "20 kΩ" },
    { T: 200000, donVi: "kΩ", heSo: 1e3, decimals: 1, ten: "200 kΩ" },
  ],
};

export const TEN_DL: Record<DaiLuongDH, string> = { DCV: "V⎓", ACV: "V~", DCA: "A⎓", OHM: "Ω" };

/** Một tình huống đo. giaTri theo đơn vị SI (V, A, Ω); uNguon: hiệu điện thế nguồn của mạch (tình huống đo dòng). */
export type NhiemVuDH = { dl: DaiLuongDH; giaTri: number; de: string; vat: string; uNguon?: number };
export type CauHinhDH = { dl: DaiLuongDH; thang: number; lo: LoCam; mac: CachMac };
export type KetQuaDo = {
  /** Chữ trên màn (dấu chấm như máy thật; "1" = quá thang; "—" = không đo được). */
  man: string;
  donVi: string;
  loai: "dung" | "chua-toi-uu" | "sai" | "nguy-hiem";
  chiDut: boolean;
  loi: string;
};

/** Chữ trên màn cho giá trị ở thang th (quá thang → "1", như đồng hồ thật). */
export function manHinhDH(giaTri: number, th: ThangDo): string {
  if (Math.abs(giaTri) >= th.T) return "1";
  return (giaTri / th.heSo).toFixed(th.decimals);
}

/** Cách đặt đúng: thang nhỏ nhất còn lớn hơn giá trị; dòng ≥ 200 mA dùng lỗ 10A; đo dòng mắc nối tiếp, còn lại song song. */
export function cauHinhDung(nv: NhiemVuDH): CauHinhDH {
  const ds = THANG_DH[nv.dl];
  const thang = Math.max(
    0,
    ds.findIndex((t) => t.T > nv.giaTri),
  );
  const lo: LoCam = nv.dl === "DCA" ? (nv.giaTri < 0.2 ? "mA" : "10A") : "VΩ";
  return { dl: nv.dl, thang, lo, mac: nv.dl === "DCA" ? "noi-tiep" : "song-song" };
}

function moTaDung(nv: NhiemVuDH) {
  const c = cauHinhDung(nv);
  return `núm ${TEN_DL[c.dl]} thang ${THANG_DH[c.dl][c.thang].ten}, que đỏ lỗ ${c.lo}, que đen lỗ COM, mắc ${c.mac === "noi-tiep" ? "nối tiếp" : "song song"}`;
}

/** Đồng hồ hiện gì khi chạm que với cấu hình ch. chiDutSan: cầu chì lỗ mA đã đứt từ trước. */
export function doDongHo(nv: NhiemVuDH, ch: CauHinhDH, chiDutSan = false): KetQuaDo {
  const ds = THANG_DH[ch.dl];
  const th = ds[Math.min(ch.thang, ds.length - 1)];
  const loA = ch.lo !== "VΩ";
  const coNguon = nv.dl !== "OHM";
  const dung = moTaDung(nv);
  const kq = (loai: KetQuaDo["loai"], man: string, loi: string, chiDut = false): KetQuaDo => ({
    man,
    donVi: th.donVi,
    loai,
    chiDut,
    loi,
  });

  // 1. Lỗ ampe kế chạm song song vào chỗ có điện = chập mạch.
  if (loA && ch.mac === "song-song" && coNguon) {
    if (ch.lo === "mA")
      return kq(
        "nguy-hiem",
        "—",
        `Que đỏ ở lỗ mA là đường của ampe kế, điện trở rất nhỏ. Chạm song song vào ${nv.vat} là chập mạch: cầu chì trong đồng hồ đứt. Cách đúng: ${dung}.`,
        true,
      );
    return kq(
      "nguy-hiem",
      "—",
      `Lỗ 10A thường không có cầu chì bảo vệ. Chạm song song vào ${nv.vat} là chập mạch qua đồng hồ: dòng rất lớn, dây và que nóng lên, có thể cháy. Cách đúng: ${dung}.`,
    );
  }
  // 2. Thang Ω trên mạch đang có điện.
  if (ch.dl === "OHM" && coNguon)
    return kq(
      nv.dl === "ACV" ? "nguy-hiem" : "sai",
      "—",
      `Không đo điện trở khi mạch đang có điện: thang Ω dùng pin riêng của đồng hồ, gặp điện ngoài thì số đọc sai và dễ hỏng máy. Cách đúng: ${dung}.`,
    );
  // 3. Cầu chì lỗ mA đã đứt.
  if (chiDutSan && ch.lo === "mA")
    return kq("sai", manHinhDH(0, th), "Cầu chì lỗ mA đã đứt nên đồng hồ chỉ 0. Bấm “Thay cầu chì” rồi đo lại.");

  if (nv.dl === "OHM") {
    if (ch.dl !== "OHM")
      return kq("sai", manHinhDH(0, th), `Điện trở đã tháo khỏi mạch, không có nguồn nên thang V, A chỉ 0. Vặn núm về Ω. Cách đúng: ${dung}.`);
    if (loA) return kq("sai", "1", `Đo điện trở cắm que đỏ ở lỗ VΩ. Cách đúng: ${dung}.`);
    if (ch.mac !== "song-song")
      return kq("sai", "1", `Đo điện trở thì chạm hai que vào hai đầu ${nv.vat} (đã tháo khỏi mạch). Cách đúng: ${dung}.`);
  } else if (ch.dl !== nv.dl) {
    const thV = ch.dl === "DCV" || ch.dl === "ACV";
    if (nv.dl === "DCA" && thV) {
      if (loA) return kq("sai", manHinhDH(0, th), `Núm ở thang V nhưng que đỏ ở lỗ ${ch.lo}: núm và lỗ cắm phải khớp nhau. Cách đúng: ${dung}.`);
      const u = nv.uNguon ?? 0;
      if (ch.mac === "noi-tiep")
        return kq(
          "sai",
          manHinhDH(u, th),
          `Vôn kế (núm V) mắc nối tiếp có điện trở rất lớn: mạch gần như hở, đèn tắt, màn chỉ gần bằng hiệu điện thế nguồn. Đo dòng: ${dung}.`,
        );
      return kq("sai", manHinhDH(u, th), `Núm V mắc song song là đo hiệu điện thế hai đầu ${nv.vat}, không phải dòng điện. Đo dòng: ${dung}.`);
    }
    if (nv.dl === "DCV" && ch.dl === "ACV")
      return kq("sai", manHinhDH(0, th), `${nv.vat[0].toUpperCase()}${nv.vat.slice(1)} là nguồn một chiều: vặn núm về V⎓. Cách đúng: ${dung}.`);
    if (nv.dl === "ACV" && ch.dl === "DCV")
      return kq("sai", manHinhDH(0, th), `Ổ điện là xoay chiều, thang một chiều chỉ quanh 0: vặn núm về V~. Cách đúng: ${dung}.`);
    return kq("sai", manHinhDH(0, th), `Đo hiệu điện thế thì vặn núm về V, không phải A. Cách đúng: ${dung}.`);
  } else if (nv.dl === "DCV" || nv.dl === "ACV") {
    if (loA) return kq("sai", manHinhDH(0, th), `Đo hiệu điện thế cắm que đỏ ở lỗ VΩ. Cách đúng: ${dung}.`);
    if (ch.mac === "noi-tiep")
      return kq("sai", manHinhDH(nv.giaTri, th), `Vôn kế phải mắc song song: chạm hai que vào hai cực của ${nv.vat}. Cách đúng: ${dung}.`);
  } else {
    // DCA, núm đúng
    if (!loA) return kq("sai", manHinhDH(0, th), `Núm ở A⎓ thì que đỏ phải cắm lỗ mA hoặc 10A. Cách đúng: ${dung}.`);
    const thang10 = th.T === 10;
    if (thang10 && ch.lo === "mA") return kq("sai", manHinhDH(0, th), `Thang 10 A đi với lỗ 10A, không phải lỗ mA. Cách đúng: ${dung}.`);
    if (!thang10 && ch.lo === "10A") return kq("sai", manHinhDH(0, th), `Thang mA đi với lỗ mA, không phải lỗ 10A. Cách đúng: ${dung}.`);
    if (ch.lo === "mA" && nv.giaTri >= 0.2)
      return kq(
        "nguy-hiem",
        "—",
        `Dòng qua ${nv.vat} lớn hơn 200 mA: cầu chì lỗ mA đứt. Dòng từ 200 mA trở lên dùng lỗ 10A, thang 10 A.`,
        true,
      );
  }

  // Núm, lỗ, cách mắc đều đúng: còn thang.
  const can = cauHinhDung(nv);
  const man = manHinhDH(nv.giaTri, th);
  if (nv.giaTri >= th.T)
    return kq("sai", man, `Quá thang: màn chỉ hiện số 1 ở bên trái. Chuyển lên thang lớn hơn: ${THANG_DH[can.dl][can.thang].ten}.`);
  if (ch.thang !== can.thang)
    return kq(
      "chua-toi-uu",
      man,
      `Đo được nhưng thang ${th.ten} quá lớn nên số chỉ ít chữ số. Chọn thang nhỏ nhất còn lớn hơn giá trị cần đo: ${THANG_DH[can.dl][can.thang].ten}.`,
    );
  return kq("dung", man, `Đặt đúng: ${dung}. Đọc: ${man.replace(".", ",")} ${th.donVi}.`);
}

/** Mẫu tình huống: [đại lượng, min, max, bước làm tròn, đề, vật, uNguon]. */
const MAU_DH: [DaiLuongDH, number, number, number, string, string, number?][] = [
  ["DCV", 1.48, 1.62, 0.001, "Đo suất điện động một pin 1,5 V (mạch ngoài để hở).", "pin"],
  ["DCV", 11.6, 12.6, 0.01, "Đo hiệu điện thế hai cực một nguồn điện một chiều 12 V.", "nguồn điện"],
  ["DCV", 4.4, 5.2, 0.01, "Đo hiệu điện thế hai cực bộ nguồn 3 pin nối tiếp.", "bộ nguồn"],
  ["ACV", 215, 235, 1, "Đo hiệu điện thế ổ điện 220 V xoay chiều của bàn thí nghiệm.", "ổ điện"],
  ["DCA", 0.22, 0.32, 0.01, "Đo cường độ dòng điện qua bóng đèn 6 V – 1,8 W đang sáng (cỡ 0,3 A).", "bóng đèn", 6],
  ["DCA", 0.012, 0.018, 0.0001, "Đo cường độ dòng điện qua một đèn LED đang sáng (cỡ 15 mA).", "đèn LED", 5],
  ["DCA", 0.056, 0.064, 0.0001, "Đo cường độ dòng điện qua điện trở 100 Ω nối vào nguồn 6 V.", "điện trở", 6],
  ["OHM", 46.5, 47.5, 0.1, "Đo điện trở ghi 47 Ω (đã tháo khỏi mạch).", "điện trở"],
  ["OHM", 216, 224, 1, "Đo điện trở ghi 220 Ω (đã tháo khỏi mạch).", "điện trở"],
  ["OHM", 4620, 4780, 10, "Đo điện trở ghi 4,7 kΩ (đã tháo khỏi mạch).", "điện trở"],
  ["OHM", 46200, 47800, 100, "Đo điện trở ghi 47 kΩ (đã tháo khỏi mạch).", "điện trở"],
];
export const SO_MAU_DH = MAU_DH.length;

/** Tình huống thứ i (i cho trước → giá trị giữa khoảng; không cho → ngẫu nhiên). */
export function taoNhiemVuDH(i: number, ngauNhien = true): NhiemVuDH {
  const [dl, lo, hi, buoc, de, vat, uNguon] = MAU_DH[((i % MAU_DH.length) + MAU_DH.length) % MAU_DH.length];
  const raw = ngauNhien ? lo + Math.random() * (hi - lo) : (lo + hi) / 2;
  const giaTri = Number((Math.round(raw / buoc) * buoc).toFixed(6));
  return { dl, giaTri, de, vat, uNguon };
}

/* ---------------- Đồng hồ đo thời gian hiện số + cổng quang ---------------- */

export type ModeDem = "A" | "B" | "A+B" | "A↔B";
/** Một lần vật chắn tia của cổng nối ổ `o`, từ `vao` tới `ra` (mili giây, tính từ lúc thả). */
export type LanChan = { o: "A" | "B"; vao: number; ra: number };

/** Thang 9,999 s: quá 9999 ms màn đứng ở 9999. */
export const MS_TOI_DA = 9999;

/**
 * Số chỉ (ms, số nguyên) của đồng hồ ở MODE `mode` tại thời điểm `t` ms sau khi thả (mặc định: đã chạy xong).
 * Chỉ tính lần chắn ĐẦU TIÊN của mỗi cổng. A↔B: thiếu lần chắn cổng B thì đồng hồ không dừng (đếm tới thang).
 */
export function soChiDongHo(mode: ModeDem, lan: LanChan[], t = Infinity): number {
  const dau = (o: "A" | "B") => lan.find((l) => l.o === o);
  const chan = (l: LanChan | undefined) => (!l || t <= l.vao ? 0 : Math.min(t, l.ra) - l.vao);
  const a = dau("A");
  const b = dau("B");
  let ms: number;
  if (mode === "A") ms = chan(a);
  else if (mode === "B") ms = chan(b);
  else if (mode === "A+B") ms = chan(a) + chan(b);
  else ms = !a || t <= a.vao ? 0 : (b && b.vao > a.vao ? Math.min(t, b.vao) : t) - a.vao;
  return Math.min(MS_TOI_DA, Math.round(ms));
}

/** "0,605" — số chỉ ms → giây, ba chữ số sau dấu phẩy. */
export const ghiGiay = (ms: number) => soNguyenRaChuoi(ms, 3);

export const TEN_MODE: Record<ModeDem, string> = {
  A: "lúc vật đang chắn cổng nối ổ A",
  B: "lúc vật đang chắn cổng nối ổ B",
  "A+B": "tổng thời gian vật chắn cổng A và chắn cổng B",
  "A↔B": "từ lúc vật chắn cổng A tới lúc vật chắn cổng B",
};

/**
 * Chấm số học sinh đọc (giây) khi nhiệm vụ cần MODE `can`, học sinh đang để MODE `dangChon`.
 * Đọc đúng màn nhưng MODE sai → chỉ ra MODE đúng.
 */
export function chamDongHoHienSo(raw: string, can: ModeDem, dangChon: ModeDem, lan: LanChan[]): KetQuaCham | null {
  const so = docSo(raw);
  if (!so) return null;
  const dungMs = soChiDongHo(can, lan);
  const dapAn = `${ghiGiay(dungMs)} s`;
  const sMs = Math.round(so.value * 1000);
  const chinhXac = Math.abs(so.value * 1000 - sMs) < 1e-6;
  if (chinhXac && sMs === dungMs) {
    if (so.decimals === 3) return { loai: "dung", loi: `MODE ${can}, số chỉ ${dapAn}.` };
    return { loai: "chu-so", loi: `Đồng hồ chia tới 0,001 s nên ghi đủ ba chữ số sau dấu phẩy: ${dapAn}.` };
  }
  if (dangChon !== can && chinhXac && sMs === soChiDongHo(dangChon, lan)) {
    return {
      loai: "sai",
      loi: `Em đọc đúng màn, nhưng MODE ${dangChon} đo ${TEN_MODE[dangChon]}. Việc này cần MODE ${can} (${TEN_MODE[can]}): ${dapAn}.`,
    };
  }
  return {
    loai: "sai",
    loi: `Để MODE ${can}, bấm RESET rồi thả lại và đọc màn: ${dapAn}. Màn ghi dấu chấm, em ghi dấu phẩy.`,
  };
}

/**
 * Lần chắn của viên bi đường kính d (m) lăn không vận tốc đầu với gia tốc a (m/s²) qua cổng E (ổ A) cách chỗ thả xE (m)
 * và cổng F (ổ B) cách thêm s (m); tia sáng đi ngang tâm bi.
 */
export function lanChanBiLan(a: number, d: number, xE: number, s: number): LanChan[] {
  const tg = (x: number) => Math.round(Math.sqrt((2 * x) / a) * 1000);
  return [
    { o: "A", vao: tg(xE - d / 2), ra: tg(xE + d / 2) },
    { o: "B", vao: tg(xE + s - d / 2), ra: tg(xE + s + d / 2) },
  ];
}
