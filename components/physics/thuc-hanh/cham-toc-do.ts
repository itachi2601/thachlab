/**
 * components/physics/thuc-hanh/cham-toc-do.ts — số học của thí nghiệm ảo "Đo tốc độ" (L10 Bài 6, lesson 51; Gói C,
 * docs/KE-HOACH-MO-PHONG-HOC-TU-EDUTOOLKIT.md mục 5). Không React để thử bằng `npx tsx`.
 *
 * Thông số lấy từ content/thi-nghiem/tn-l10-do-toc-do-01.json (hai cổng, MODE A↔B) và tn-l10-do-toc-do-02.json
 * (một cổng F, MODE B, tia lệch tâm). Quy ước sai số theo đúng bài 51:
 *   Δt = trung bình |t_i − t̄| + Δt_dc, Δt_dc = 1 độ chia = 0,001 s; Δs = nửa độ chia thước mm = 0,0005 m;
 *   δv = Δs/s + Δt/t̄ (hai cổng) hoặc Δd/d + Δt/t̄ (một cổng, Δd = 0,05 mm thước kẹp); Δv = δv · v̄.
 * Thời gian giữ bằng SỐ NGUYÊN mili giây (đồng hồ chia 0,001 s) để tránh lỗi dấu phẩy động.
 */

import tn1 from "@/content/thi-nghiem/tn-l10-do-toc-do-01.json";
import tn2 from "@/content/thi-nghiem/tn-l10-do-toc-do-02.json";
import { docSo, type KetQuaCham } from "@/components/physics/do-luong/chung";
import { lanChanBiLan, type LanChan } from "@/components/physics/do-luong/cham";
import { gan, phanLoai, vnSo } from "./cham-chung";

export { vnSo };

type ThamSo = {
  ky_hieu: string;
  min?: number;
  max?: number;
  mac_dinh?: number;
  buoc?: number;
  gia_tri?: number;
  sai_so_do?: number;
};
const bang = (ds: ThamSo[]) => Object.fromEntries(ds.map((p) => [p.ky_hieu, p])) as Record<string, ThamSo>;
const TS1 = bang(tn1.tham_so as ThamSo[]);
const TS2 = bang(tn2.tham_so as ThamSo[]);

/** Mức tăng tốc độ của bi trên máng (m/s²), giả định của kho thí nghiệm. */
export const A_MANG = TS1.a.mac_dinh ?? 0.6;
/** Từ chỗ nam châm thả bi tới cổng E (m). */
export const X_E = TS1.x_E.gia_tri ?? 0.1;
/** Đường kính bi (m) — thước kẹp đo 20,0 mm. */
export const D_BI = (TS2.d.mac_dinh ?? 20) / 1000;
export const DC_T = 0.001; // s — 1 độ chia đồng hồ (bài 51 lấy 1 độ chia)
export const DELTA_S = 0.0005; // m — nửa độ chia thước mm
export const DELTA_D = 0.00005; // m — thước kẹp 0,05 mm
/** Độ lệch tia so với tâm bi khi bật "lệch" (mm) — tn-l10-do-toc-do-02 ghi_chu: 6 mm → dây cung 16 mm. */
export const LECH_MM = 6;
/** Khoảng cách EF, đơn vị cm (bước 5 cm) để cộng trừ không lệch. */
export const S_CM = {
  min: Math.round((TS1.s.min ?? 0.2) * 100),
  max: Math.round((TS1.s.max ?? 0.7) * 100),
  macDinh: Math.round((TS1.s.mac_dinh ?? 0.5) * 100),
  buoc: Math.round((TS1.s.buoc ?? 0.05) * 100),
};
/** Biên độ nhiễu mỗi lần thả ở MODE A↔B (ms) — sai_so_do của t. */
export const NHIEU_MS = Math.round((TS1.t.sai_so_do ?? 0.002) * 1000);

/** Thời điểm (ms, chưa làm tròn) tâm bi tới vị trí x (m) tính từ chỗ thả. */
const tg = (x: number) => Math.sqrt(Math.max(0, (2 * x) / A_MANG)) * 1000;

/** Tốc độ thật của bi tại cổng F (m/s). */
export const vTaiF = (s: number) => Math.sqrt(2 * A_MANG * (X_E + s));

/** Dây cung tia sáng cắt qua bi (m): tia ngang tâm → bằng đường kính. */
export const dayCung = (lechMm: number) => 2 * Math.sqrt(Math.max(0, (D_BI / 2) ** 2 - (lechMm / 1000) ** 2));

/** Nhiễu một lần thả: n (ms nguyên, MODE A↔B) và u ∈ [−0,5; 0,5] ms (làm tròn thời gian chắn ở MODE B). */
export type Nhieu = { n: number; u: number };
export const nhieuNgauNhien = (): Nhieu => ({
  n: Math.floor(Math.random() * (2 * NHIEU_MS + 1)) - NHIEU_MS,
  u: Math.random() - 0.5,
});

/**
 * Các lần chắn tia (ms) cho đồng hồ. Hai cổng: cổng F trễ thêm n ms (T8). Một cổng: cổng F bị chắn trong thời gian bi đi
 * hết dây cung (tia lệch → dây cung ngắn → chắn ngắn hơn: T7), làm tròn tới độ chia.
 */
export function lanChan(s: number, motCong: boolean, lechMm: number, nh: Nhieu): LanChan[] {
  const [a, b] = lanChanBiLan(A_MANG, D_BI, X_E, s);
  if (!motCong) return [a, { o: "B", vao: b.vao + nh.n, ra: b.ra + nh.n }];
  const c = dayCung(lechMm);
  const vao = Math.round(tg(X_E + s - c / 2));
  const chan = Math.max(1, Math.round(tg(X_E + s + c / 2) - tg(X_E + s - c / 2) + nh.u));
  return [a, { o: "B", vao, ra: vao + chan }];
}

/** Số chỉ đồng hồ (ms) của lần thả: A↔B hoặc B. */
export const soChiLan = (lan: LanChan[], motCong: boolean) => {
  const b = lan.find((l) => l.o === "B")!;
  return motCong ? b.ra - b.vao : b.vao - lan.find((l) => l.o === "A")!.vao;
};

export type KetQuaLoat = {
  tbar: number; // s
  lech: number[]; // |t_i − t̄|, s
  dbar: number; // trung bình độ lệch, s
  dt: number; // Δt = dbar + DC_T, s
  v: number; // v̄, m/s
  delta: number; // sai số tỉ đối
  dv: number; // Δv, m/s
};

/** Xử lí một loạt đo như bài 51. tMs: các số chỉ (ms); dai: s (hai cổng) hoặc d (một cổng), m; dDai: Δs hoặc Δd. */
export function tinhLoat(tMs: number[], dai: number, dDai: number): KetQuaLoat {
  const n = tMs.length;
  const tbar = tMs.reduce((x, y) => x + y, 0) / n / 1000;
  const lech = tMs.map((t) => Math.abs(t / 1000 - tbar));
  const dbar = lech.reduce((x, y) => x + y, 0) / n;
  const dt = dbar + DC_T;
  const v = dai / tbar;
  const delta = dDai / dai + dt / tbar;
  return { tbar, lech, dbar, dt, v, delta, dv: delta * v };
}

/* ---------------- Chấm bốn ô học sinh tự tính (bảng hai cổng) ---------------- */

export function chamTbar(raw: string, tMs: number[], kq: KetQuaLoat): KetQuaCham | null {
  const so = docSo(raw);
  if (!so) return null;
  const tong = tMs.reduce((x, y) => x + y, 0) / 1000;
  const cach = `t̄ = (${tMs.map((t) => vnSo(t / 1000, 3)).join(" + ")}) : ${tMs.length} ≈ ${vnSo(kq.tbar, 4)} s.`;
  if (gan(so.value, kq.tbar, 0.0005)) return { loai: "dung", loi: cach };
  if (gan(so.value, tong, 0.001))
    return { loai: "sai", loi: `Đó là tổng ${tMs.length} lần, còn phải chia cho ${tMs.length}. ${cach}` };
  return { loai: "sai", loi: `Cộng ${tMs.length} số rồi chia ${tMs.length}: ${cach}` };
}

export function chamDt(raw: string, kq: KetQuaLoat): KetQuaCham | null {
  const so = docSo(raw);
  if (!so) return null;
  const cach = `Độ lệch từng lần (cột thứ ba) trung bình ${vnSo(kq.dbar, 4)} s; cộng sai số dụng cụ ${vnSo(DC_T, 3)} s: Δt ≈ ${vnSo(kq.dt, 4)} s.`;
  return phanLoai(
    so.value,
    cach,
    [
      [kq.dt, 0.00045],
      [Math.round(kq.dt * 1000) / 1000, 1e-7],
    ],
    [
      [kq.dbar, 0.0003, "Em mới có phần phân tán, quên cộng sai số dụng cụ của đồng hồ."],
      [
        kq.dbar + DC_T / 2,
        0.0002,
        "Bài này lấy sai số dụng cụ của đồng hồ hiện số bằng 1 độ chia (0,001 s), không phải nửa độ chia.",
      ],
    ],
  );
}

export function chamV(raw: string, s: number, kq: KetQuaLoat): KetQuaCham | null {
  const so = docSo(raw);
  if (!so) return null;
  const cach = `v̄ = s : t̄ = ${vnSo(s, 3)} : ${vnSo(kq.tbar, 4)} ≈ ${vnSo(kq.v, 3)} m/s.`;
  return phanLoai(
    so.value,
    cach,
    [[kq.v, 0.001]],
    [
      [kq.tbar / s, 0.01, "Em lấy t̄ chia s; tốc độ là quãng đường chia thời gian."],
      [s * kq.tbar, 0.005, "Em nhân s với t̄; tốc độ là s chia t̄."],
    ],
  );
}

/**
 * Δv chấm theo Δt và v̄ CỦA HỌC SINH ở hai ô trước (ô đó sai thì dùng số đúng), như chamDg bài 56.
 * Dung sai 0,00055 = làm tròn 3 chữ số thập phân. Giới hạn đã biết: phần Δs/s chỉ cỡ 0,0006 m/s ở s = 0,500 m nên
 * "quên Δs/s" có thể lọt vào dung sai đúng; ở s nhỏ (0,200 m) thì bắt được.
 */
export function chamDv(raw: string, s: number, kq: KetQuaLoat, dtHs = kq.dt, vHs = kq.v): KetQuaCham | null {
  const so = docSo(raw);
  if (!so) return null;
  const voi = (dt: number, coDs: boolean) => ((coDs ? DELTA_S / s : 0) + dt / kq.tbar) * vHs;
  const delta = DELTA_S / s + dtHs / kq.tbar;
  const dv = voi(dtHs, true);
  const cach = `δv = Δs/s + Δt/t̄ = ${vnSo(DELTA_S, 4)}/${vnSo(s, 3)} + ${vnSo(dtHs, 4)}/${vnSo(kq.tbar, 4)} ≈ ${vnSo(delta, 4)}; Δv = δv · v̄ ≈ ${vnSo(dv, 3)} m/s.`;
  return phanLoai(
    so.value,
    cach,
    [[dv, 0.00055]],
    [
      [voi(dtHs, false), 0.0002, "Thiếu phần Δs/s của thước (0,0005 m chia cho s)."],
      [delta, 0.0003, "Đó là sai số tỉ đối δv; Δv = δv · v̄ mới là sai số tuyệt đối (m/s)."],
      [delta * 100, 0.03, "Đó là sai số tỉ đối δv tính theo %; Δv = δv · v̄ mới là sai số tuyệt đối (m/s)."],
      [
        voi(2 * dtHs, true),
        0.0003,
        "v = s/t chỉ có t ở mẫu một lần nên cộng Δt/t̄ một lần; hệ số 2 là của g = 2s/t² (t bình phương).",
      ],
    ],
  );
}

/* ---------------- Ô của bảng một cổng ---------------- */

/** v = d : t̄ với d = 20,0 mm. Học sinh có thể làm tròn t̄ tới 0,001 s nên dung sai rộng (t̄ chỉ cỡ 24 độ chia). */
export function chamVF(raw: string, kq: KetQuaLoat): KetQuaCham | null {
  const so = docSo(raw);
  if (!so) return null;
  const tRound = Math.round(kq.tbar * 1000) / 1000;
  const cach = `v = d : t̄ = ${vnSo(D_BI, 3)} : ${vnSo(kq.tbar, 4)} ≈ ${vnSo(kq.v, 2)} m/s (d = 20,0 mm = 0,020 m).`;
  return phanLoai(
    so.value,
    cach,
    [
      [kq.v, 0.01],
      [D_BI / tRound, 0.005],
    ],
    [
      [kq.v * 1000, 15, "Em chưa đổi d = 20,0 mm ra mét (0,020 m)."],
      [kq.v / 2, 0.01, "Em lấy bán kính; bi chắn tia suốt một đường kính d = 20,0 mm."],
    ],
  );
}
