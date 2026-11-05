"use client";

/**
 * Họ hình `cot_chat_long` (đợt Đ4 3/11/2026, mẫu đầu: bài 34 Khối lượng riêng. Áp suất chất lỏng L10, dạng 4): bình chứa
 * chất lỏng vẽ nét đơn giản, độ cao đo bằng cm theo đúng tỉ lệ đề. Hai cảnh:
 *  - `ong_u`: ống chữ U hai nhánh hở, chất lỏng nặng (xám) ở đáy, chất lỏng nhẹ (lam) trên nhánh trái; y = 0 là mặt phân
 *    cách. Mục: muc {h1, h2} (cột nhẹ trên mặt phân cách · mặt chất nặng nhánh phải), diem {ten: "A"|"B"}, ngang (nét đứt
 *    nối A–B), thuoc {ong: "trai"|"phai"|"giua", tu, den, nhan} (giữa: thước giữa hai nhánh + gạch dóng hai mức).
 *  - `be`: bể rộng, mặt nước y = 0, khối hộp (`rong` × `cao` cm) ở giữa. Mục: khoi {chim, vat?} (khối mới nhất đang hiện
 *    là khối dùng cho lực), luc {ten, huong, do_lon, tu?: "khoi"|"vat", lech?}, thuoc {ong: "trai"|"phai", tu, den, nhan}.
 *  - `ong_kin` (Đ6 5/11/2026, bài 7 Boyle L12 dạng 5): ống thẳng đứng dài `dai` cm, một đầu kín, cột thuỷ ngân giam cột
 *    khí; y = 0 là đáy khung (cm, lên là dương), hai chỗ đặt ống trái/phải. Mục: ong {ben: "trai"|"phai", mieng:
 *    "len"|"xuong", khi, hg (cm), nhan_khi?, nhan_hg? (thước ở phía ngoài: ống trái thước bên trái, ống phải bên phải),
 *    p0? (nhãn mũi tên áp suất khí quyển ở miệng), dut? (vẽ nhạt, mặt phân cách nét đứt — chiều dài chưa biết)}.
 * Chung: chu {x (0..20), y (cm), text, a?} · ghi {text}. `het: k` = ẩn từ khi xong bước k.
 * Hình không đổi cao giữa các bước (D2: khung theo h_max/tren/sau); nhãn trên hình (N8, H3); lực bằng nét + tên (H4).
 */

import { C_MAX, C_MIN, Chevron, Label, chiaDong, dangHien, ghiMoiNhat } from "@/components/lessons/cong-cu/chung";
import type { CotChatLongCanh, CotChatLongLop } from "@/features/lessons/types";

type Props = { canh: CotChatLongCanh; hinh?: CotChatLongLop[]; lop?: CotChatLongLop[][]; layer: number };

const W = 20,
  FS = 1.05,
  XL = 6,
  XR = 14,
  R = 1; // nửa bề rộng lòng ống

export default function CotChatLong({ canh, hinh = [], lop, layer: Lr }: Props) {
  if (canh.kieu === "ong_kin") return <OngKin dai={canh.dai} hinh={hinh} lop={lop} layer={Lr} />;
  const items = dangHien(lop, Lr);
  const hinhHien = hinh.filter((it) => it.het == null || Lr < it.het);
  const hien = [...hinhHien, ...items];
  const ghi = ghiMoiNhat(lop, Lr).flatMap((t) => chiaDong(t, W, FS)).slice(0, 2);

  const u = canh.kieu === "ong_u";
  const k = u ? 8 / canh.h_max : 0.3;
  const TOP = u ? 1.5 : 0.8 + canh.tren * 0.3;
  // y (cm) → toạ độ hình
  const Y0 = u ? TOP + canh.h_max * k : TOP;
  const Y = (y: number) => Y0 - y * k;
  const YB = u ? Y0 + 2.8 : Y0 + canh.sau * k; // đáy
  const H = YB + 0.5;

  // cảnh be: khối đang dùng
  const khoi = [...hien].reverse().find((it) => it.loai === "khoi") as Extract<CotChatLongLop, { loai: "khoi" }> | undefined;
  const BW = !u ? canh.rong * k : 0,
    BH = !u ? canh.cao * k : 0;
  const bTop = khoi ? Y(canh.kieu === "be" ? canh.cao - khoi.chim : 0) : 0;
  const allLuc = [...hinh, ...(lop ?? []).flat()].filter((it) => it.loai === "luc") as Extract<CotChatLongLop, { loai: "luc" }>[];
  const maxF = Math.max(1, ...allLuc.map((f) => f.do_lon));

  function veMuc(it: CotChatLongLop, moi: boolean) {
    const cls = moi ? "cc-in" : undefined;
    if (it.loai === "muc" && u) {
      const yc = YB - 2; // trần kênh nối
      const hg = `M${XL - R} ${Y(0)} H${XL + R} V${yc} H${XR - R} V${Y(it.h2)} H${XR + R} V${YB} H${XL - R} Z`;
      return (
        <g className={cls}>
          <path d={hg} fill="currentColor" fillOpacity={0.32} />
          <rect x={XL - R} y={Y(it.h1)} width={2 * R} height={Y(0) - Y(it.h1)} fill={C_MIN} fillOpacity={0.22} />
          <line x1={XL - R} y1={Y(it.h1)} x2={XL + R} y2={Y(it.h1)} stroke={C_MIN} strokeWidth={0.08} />
          <line x1={XR - R} y1={Y(it.h2)} x2={XR + R} y2={Y(it.h2)} stroke="currentColor" strokeWidth={0.08} />
          <line x1={XL - R} y1={Y(0)} x2={XL + R} y2={Y(0)} stroke="currentColor" strokeWidth={0.06} />
        </g>
      );
    }
    if (it.loai === "diem" && u) {
      const x = it.ten === "B" ? XR : XL;
      return (
        <g className={cls}>
          <circle cx={x} cy={Y(0)} r={0.2} fill={C_MAX} />
          <Label x={x} y={Y(0) + 1.15} fill={C_MAX} size={FS}>
            {it.ten}
          </Label>
        </g>
      );
    }
    if (it.loai === "ngang" && u) {
      return (
        <g className={cls}>
          <line x1={XL - R - 0.6} y1={Y(0)} x2={XR + R + 0.6} y2={Y(0)} stroke={C_MAX} strokeWidth={0.07} strokeDasharray="0.35 0.22" />
          {it.nhan && (
            <Label x={W / 2} y={Y(0) - 0.35} fill={C_MAX} size={FS}>
              {it.nhan}
            </Label>
          )}
        </g>
      );
    }
    if (it.loai === "thuoc") {
      const giua = it.ong === "giua";
      const x = giua ? W / 2 : it.ong === "trai" ? (u ? XL - R - 0.7 : W / 2 - BW / 2 - 0.7) : u ? XR + R + 0.7 : W / 2 + BW / 2 + 0.7;
      const y1 = Y(it.tu),
        y2 = Y(it.den),
        trai = it.ong === "trai";
      return (
        <g className={cls}>
          {giua && (
            <g stroke={C_MAX} strokeWidth={0.05} strokeDasharray="0.2 0.18">
              <line x1={XL + R} y1={y2} x2={x} y2={y2} />
              <line x1={x} y1={y1} x2={XR - R} y2={y1} />
            </g>
          )}
          <g stroke={C_MAX} strokeWidth={0.08}>
            <line x1={x} y1={y1} x2={x} y2={y2} />
            <line x1={x - 0.25} y1={y1} x2={x + 0.25} y2={y1} />
            <line x1={x - 0.25} y1={y2} x2={x + 0.25} y2={y2} />
          </g>
          <Label x={trai ? x - 0.35 : x + 0.35} y={(y1 + y2) / 2 + 0.4} a={trai ? "end" : "start"} fill={C_MAX} size={FS}>
            {it.nhan}
          </Label>
        </g>
      );
    }
    if (it.loai === "khoi" && !u) {
      const top = Y(canh.kieu === "be" ? canh.cao - it.chim : 0);
      return (
        <g className={cls}>
          <rect x={W / 2 - BW / 2} y={top} width={BW} height={BH} fill="var(--cc-halo)" stroke="currentColor" strokeWidth={0.12} />
          <rect x={W / 2 - BW / 2} y={top} width={BW} height={BH} fill="#a16207" fillOpacity={0.18} />
          {it.vat && (
            <g>
              <rect x={W / 2 - 1.3} y={top - 1.1} width={2.6} height={1.1} rx={0.15} fill="var(--cc-halo)" stroke="currentColor" strokeWidth={0.1} />
              <Label x={W / 2} y={top - 0.25} size={0.85}>
                {it.vat}
              </Label>
            </g>
          )}
        </g>
      );
    }
    if (it.loai === "luc" && !u && khoi) {
      const tuVat = it.tu === "vat",
        x = W / 2 + (it.lech ?? 0),
        y0 = tuVat ? bTop - 0.55 : bTop + BH / 2,
        len = (it.do_lon / maxF) * 4.2,
        s = it.huong === "len" ? -1 : 1,
        y1 = y0 + s * len,
        c = it.huong === "len" ? C_MIN : C_MAX;
      return (
        <g className={cls}>
          <circle cx={x} cy={y0} r={0.12} fill={c} />
          <line x1={x} y1={y0} x2={x} y2={y1 - s * 0.05} stroke={c} strokeWidth={0.14} />
          <Chevron x={x} y={y1} ang={(s * Math.PI) / 2} color={c} len={0.5} w={0.14} />
          <Label x={x + (it.lech != null && it.lech < 0 ? -0.35 : 0.35)} y={y1 + (s > 0 ? 0.1 : 0.75)} a={it.lech != null && it.lech < 0 ? "end" : "start"} fill={c} size={FS}>
            {it.ten}
          </Label>
        </g>
      );
    }
    if (it.loai === "chu") {
      return (
        <g className={cls}>
          <Label x={it.x} y={Y(it.y)} a={it.a ?? "middle"} size={FS} fill={it.mau === "min" ? C_MIN : it.mau === "max" ? C_MAX : "currentColor"}>
            {it.text}
          </Label>
        </g>
      );
    }
    return null;
  }

  const thu = (arr: CotChatLongLop[], moi: boolean, key: string) =>
    arr.map((it, j) => <g key={`${key}${j}`}>{veMuc(it, moi)}</g>);
  const sau = (it: CotChatLongLop) => it.loai === "luc" || it.loai === "thuoc" || it.loai === "chu" || it.loai === "diem" || it.loai === "ngang";

  return (
    <svg viewBox={`-0.4 -0.2 ${W + 0.8} ${H + 3.7}`} className="cc-fig" role="img" aria-label={u ? "Ống chữ U chứa hai chất lỏng" : "Khối hộp nổi trong bể nước"}>
      {/* chất lỏng + khối trước, nét bình đè lên, nhãn/lực sau cùng */}
      {!u && <rect x={1.6} y={Y0} width={W - 3.2} height={YB - Y0} fill={C_MIN} fillOpacity={0.14} />}
      {thu(hinhHien.filter((it) => !sau(it)), false, "h")}
      {thu(items.filter((it) => !sau(it)), true, "l")}
      {u ? (
        <path
          d={`M${XL - R} ${TOP - 0.5} V${YB} H${XR + R} V${TOP - 0.5} M${XL + R} ${TOP - 0.5} V${YB - 2} H${XR - R} V${TOP - 0.5}`}
          fill="none"
          stroke="currentColor"
          strokeWidth={0.14}
          strokeLinejoin="round"
        />
      ) : (
        <g>
          <path d={`M1.6 ${Y0 - 1.6} V${YB} H${W - 1.6} V${Y0 - 1.6}`} fill="none" stroke="currentColor" strokeWidth={0.14} />
          <line x1={1.6} y1={Y0} x2={W - 1.6} y2={Y0} stroke={C_MIN} strokeWidth={0.08} />
        </g>
      )}
      {thu(hinhHien.filter(sau), false, "hs")}
      {thu(items.filter(sau), true, "ls")}
      {ghi.map((t, i) => (
        <Label key={`${Lr}-${i}`} x={W / 2} y={H + 1.2 + i * 1.45} size={FS}>
          {t}
        </Label>
      ))}
      {/* giữ chỗ dải dưới để hình không đổi cao (D2) */}
      <rect x={0} y={H} width={0.01} height={3.1} fill="none" />
    </svg>
  );
}

/** Cảnh `ong_kin`: ống một đầu kín giam khí bằng cột thuỷ ngân (Boyle). Khung cao cố định theo `dai` (D2). */
function OngKin({ dai, hinh, lop, layer: Lr }: { dai: number; hinh: CotChatLongLop[]; lop?: CotChatLongLop[][]; layer: number }) {
  const items = dangHien(lop, Lr);
  const hinhHien = hinh.filter((it) => it.het == null || Lr < it.het);
  const ghi = ghiMoiNhat(lop, Lr).flatMap((t) => chiaDong(t, W, FS)).slice(0, 2);
  const k = 8.5 / dai,
    TOP = 2.1,
    R2 = 0.9;
  const Y = (y: number) => TOP + (dai - y) * k;
  const YB = Y(0),
    H = YB + 2.3;
  const XC = (ben: "trai" | "phai") => (ben === "trai" ? 6.5 : 13.5);

  function thuoc(x: number, y1: number, y2: number, nhan: string, trai: boolean) {
    return (
      <g>
        <g stroke={C_MAX} strokeWidth={0.07}>
          <line x1={x} y1={y1} x2={x} y2={y2} />
          <line x1={x - 0.22} y1={y1} x2={x + 0.22} y2={y1} />
          <line x1={x - 0.22} y1={y2} x2={x + 0.22} y2={y2} />
        </g>
        <Label x={trai ? x - 0.35 : x + 0.35} y={(y1 + y2) / 2 + 0.38} a={trai ? "end" : "start"} fill={C_MAX} size={FS}>
          {nhan}
        </Label>
      </g>
    );
  }

  function veMuc(it: CotChatLongLop, moi: boolean) {
    const cls = moi ? "cc-in" : undefined;
    if (it.loai === "ong") {
      const x = XC(it.ben),
        len = it.mieng === "len",
        trai = it.ben === "trai";
      // khí sát đầu kín, thuỷ ngân ngay sau khí về phía miệng
      const kA = len ? 0 : dai - it.khi,
        kB = len ? it.khi : dai,
        gA = len ? it.khi : dai - it.khi - it.hg,
        gB = len ? it.khi + it.hg : dai - it.khi;
      const op = it.dut ? 0.5 : 1,
        yKin = len ? Y(0) : Y(dai),
        xt = trai ? x - R2 - 0.55 : x + R2 + 0.55;
      const yMat = len ? Y(it.khi) : Y(dai - it.khi); // mặt phân cách khí–Hg
      return (
        <g className={cls}>
          <rect x={x - R2} y={Y(kB)} width={2 * R2} height={Y(kA) - Y(kB)} fill={C_MIN} fillOpacity={0.16 * op} />
          <rect x={x - R2} y={Y(gB)} width={2 * R2} height={Y(gA) - Y(gB)} fill="currentColor" fillOpacity={0.34 * op} />
          <line x1={x - R2} y1={yMat} x2={x + R2} y2={yMat} stroke="currentColor" strokeWidth={0.07} strokeDasharray={it.dut ? "0.25 0.18" : undefined} />
          <path d={`M${x - R2} ${Y(0)} V${Y(dai)} M${x + R2} ${Y(0)} V${Y(dai)}`} stroke="currentColor" strokeWidth={0.14} fill="none" />
          <line x1={x - R2 - 0.07} y1={yKin} x2={x + R2 + 0.07} y2={yKin} stroke="currentColor" strokeWidth={0.3} />
          {it.nhan_khi && thuoc(xt, Y(kA), Y(kB), it.nhan_khi, trai)}
          {it.nhan_hg && thuoc(xt, Y(gA), Y(gB), it.nhan_hg, trai)}
          {it.p0 && (
            <g>
              <line x1={x} y1={len ? TOP - 1.9 : YB + 1.9} x2={x} y2={len ? TOP - 0.3 : YB + 0.3} stroke={C_MAX} strokeWidth={0.12} />
              <Chevron x={x} y={len ? TOP - 0.25 : YB + 0.25} ang={len ? Math.PI / 2 : -Math.PI / 2} color={C_MAX} len={0.45} w={0.12} />
              <Label x={x + 0.45} y={len ? TOP - 0.85 : YB + 1.55} a="start" fill={C_MAX} size={FS}>
                {it.p0}
              </Label>
            </g>
          )}
        </g>
      );
    }
    if (it.loai === "chu") {
      return (
        <g className={cls}>
          <Label x={it.x} y={Y(it.y)} a={it.a ?? "middle"} size={FS} fill={it.mau === "min" ? C_MIN : it.mau === "max" ? C_MAX : "currentColor"}>
            {it.text}
          </Label>
        </g>
      );
    }
    return null;
  }

  return (
    <svg viewBox={`-0.4 -0.2 ${W + 0.8} ${H + 3.7}`} className="cc-fig" role="img" aria-label="Ống thuỷ tinh một đầu kín, cột thuỷ ngân giam cột khí">
      {hinhHien.map((it, j) => (
        <g key={`h${j}`}>{veMuc(it, false)}</g>
      ))}
      {items.map((it, j) => (
        <g key={`l${j}`}>{veMuc(it, true)}</g>
      ))}
      {ghi.map((t, i) => (
        <Label key={`${Lr}-${i}`} x={W / 2} y={H + 1.2 + i * 1.45} size={FS}>
          {t}
        </Label>
      ))}
      <rect x={0} y={H} width={0.01} height={3.1} fill="none" />
    </svg>
  );
}
