"use client";

/**
 * Họ hình `thau_kinh` (đợt Đ5 4/11/2026, mẫu đầu: HSG KHTN 9 CĐ07 Thấu kính, dạng 1): trục chính nằm ngang, thấu kính
 * mỏng, vật/ảnh là mũi tên đứng, tia sáng là đường gấp khúc qua các điểm (cm). Có lưới ô ly khi đề cho "mỗi ô … cm".
 *  - `phan`: một hay nhiều khung hình (câu a/b/c của đề khác số liệu). Khung dùng ở bước đang xem là khung cuối có
 *    `tu_buoc` ≤ chỉ số bước (0-based); khung đó vẽ `hinh` của nó + các lop[i] với i ≥ tu_buoc. Khung:
 *    {tu_buoc?, x_min, x_max, y_tren, y_duoi (cm, y lên), o_ly? (cm/ô), phong_doc? (giãn trục đứng), hinh?}.
 * Mục:
 *  - tk {x, kieu: "hoi_tu"|"phan_ki", ten?, ten_ben?, f?, tieu?: [F, F′], vi_tieu?} — f (độ lớn) thì đánh dấu F, F′ (phân kì: F′ phía vật).
 *  - vat {x, h, ten?: [A, B], ten_b_ben?, ao?, mau?} — mũi tên đứng; ảnh ảo vẽ nét đứt.
 *  - diem {x, y?, ten, vi?: "t"|"b"|"l"|"r"} · tia {qua: [[x, y], …], keo?: [[x, y], …] (đường kéo dài nét đứt), mau?, mep?}
 *    (mep: kéo đoạn cuối tới mép khung).
 *  - thuoc {tu, den, o, doc?, nhan, ben?: "tren"|"duoi"|"trai"|"phai"} — thước đo (ngang ở y = o, dọc ở x = o).
 *  - chu {x, y, text, a?, mau?} · ghi {text}. `het: k` = ẩn từ khi xong bước k.
 * Hình không đổi cao giữa các khung (D2: cao theo khung cao nhất); nhãn trên hình (N8, H3); tia khác màu + tên (H4).
 */

import { C_MAX, C_MIN, Chevron, Label, chiaDong, dangHien, ghiMoiNhat } from "@/components/lessons/cong-cu/chung";
import type { ThauKinhLop, ThauKinhPhan } from "@/features/lessons/types";

type Props = { phan: ThauKinhPhan[]; lop?: ThauKinhLop[][]; layer: number; buoc?: number };

const W = 20,
  FS = 1.05,
  TOP = 0.9;

const mauCua = (m?: string, md = "currentColor") => (m === "max" ? C_MAX : m === "min" ? C_MIN : md);

export default function ThauKinh({ phan, lop, layer: Lr, buoc }: Props) {
  const b = buoc ?? Math.max(0, Lr - 1);
  const p = [...phan].reverse().find((ph) => (ph.tu_buoc ?? 0) <= b) ?? phan[0];
  const tb = p.tu_buoc ?? 0;
  const lopP = (lop ?? []).map((l, i) => (i >= tb ? l : []));
  const items = dangHien(lopP, Lr);
  const hinhHien = (p.hinh ?? []).filter((it) => it.het == null || Lr < it.het);
  const ghi = ghiMoiNhat(lopP, Lr).flatMap((t) => chiaDong(t, W, FS)).slice(0, 2);

  const kx = W / (p.x_max - p.x_min),
    ky = kx * (p.phong_doc ?? 1);
  const X = (x: number) => (x - p.x_min) * kx,
    Y = (y: number) => TOP + (p.y_tren - y) * ky;
  const caoKhung = (ph: ThauKinhPhan) => (ph.y_tren - ph.y_duoi) * (W / (ph.x_max - ph.x_min)) * (ph.phong_doc ?? 1);
  const H = TOP + Math.max(...phan.map(caoKhung)) + 0.3;
  const Y0 = Y(0);

  function diem(x: number, y: number, ten: string, vi: "t" | "b" | "l" | "r", c: string) {
    const px = X(x),
      py = Y(y);
    const [lx, ly, a] = vi === "t" ? [px, py - 0.4, "middle"] : vi === "b" ? [px, py + 1.15, "middle"] : vi === "l" ? [px - 0.35, py + 0.38, "end"] : [px + 0.35, py + 0.38, "start"];
    return (
      <>
        <circle cx={px} cy={py} r={0.13} fill={c} />
        <Label x={lx} y={ly} a={a as "start" | "middle" | "end"} fill={c} size={FS}>
          {ten}
        </Label>
      </>
    );
  }

  function duong(pts: number[][], c: string, dut: boolean, mui: boolean) {
    const out = [];
    for (let i = 0; i + 1 < pts.length; i++) {
      const x1 = X(pts[i][0]),
        y1 = Y(pts[i][1]),
        x2 = X(pts[i + 1][0]),
        y2 = Y(pts[i + 1][1]);
      const ang = Math.atan2(y2 - y1, x2 - x1),
        dai = Math.hypot(x2 - x1, y2 - y1);
      out.push(<line key={`d${i}`} x1={x1} y1={y1} x2={x2} y2={y2} stroke={c} strokeWidth={dut ? 0.08 : 0.12} strokeDasharray={dut ? "0.35 0.25" : undefined} strokeLinecap="round" />);
      if (mui && dai > 1.4) out.push(<Chevron key={`c${i}`} x={(x1 + x2) / 2 + 0.25 * Math.cos(ang)} y={(y1 + y2) / 2 + 0.25 * Math.sin(ang)} ang={ang} color={c} len={0.45} w={0.12} />);
    }
    return out;
  }

  function veMuc(it: ThauKinhLop, moi: boolean) {
    const cls = moi ? "cc-in" : undefined;
    if (it.loai === "tk") {
      const px = X(it.x),
        yt = TOP + 0.15,
        yb = Y(p.y_duoi) - 0.15,
        ht = it.kieu === "hoi_tu",
        s = ht ? 1 : -1; // hội tụ: mũi ra ngoài; phân kì: mũi vào trong
      const f = it.f != null ? Math.abs(it.f) : null;
      const [tF, tF2] = it.tieu ?? ["F", "F′"];
      return (
        <g className={cls}>
          <line x1={px} y1={yt} x2={px} y2={yb} stroke="currentColor" strokeWidth={0.13} />
          <Chevron x={px} y={ht ? yt : yt + 0.42} ang={(s * -Math.PI) / 2} len={0.5} w={0.13} />
          <Chevron x={px} y={ht ? yb : yb - 0.42} ang={(s * Math.PI) / 2} len={0.5} w={0.13} />
          {it.ten && (
            <Label x={px + (it.ten_ben === "trai" ? -0.4 : 0.4)} y={yb - 0.35} a={it.ten_ben === "trai" ? "end" : "start"} size={FS}>
              {it.ten}
            </Label>
          )}
          {f != null && (
            <>
              {diem(ht ? it.x - f : it.x + f, 0, tF, it.vi_tieu?.[0] ?? "b", "currentColor")}
              {diem(ht ? it.x + f : it.x - f, 0, tF2, it.vi_tieu?.[1] ?? "b", "currentColor")}
            </>
          )}
        </g>
      );
    }
    if (it.loai === "vat") {
      const c = mauCua(it.mau),
        px = X(it.x),
        py = Y(it.h),
        up = it.h > 0;
      const [tA, tB] = it.ten ?? ["A", "B"];
      return (
        <g className={cls}>
          <line x1={px} y1={Y0} x2={px} y2={py} stroke={c} strokeWidth={0.16} strokeDasharray={it.ao ? "0.3 0.2" : undefined} />
          <Chevron x={px} y={py} ang={up ? -Math.PI / 2 : Math.PI / 2} color={c} len={0.45} w={0.16} />
          {tA && (
            <Label x={px} y={up ? Y0 + 1.15 : Y0 - 0.4} fill={c} size={FS}>
              {tA}
            </Label>
          )}
          {tB && (
            <Label x={px + (it.ten_b_ben === "trai" ? -0.35 : it.ten_b_ben === "phai" ? 0.35 : 0)} y={up ? py - 0.4 : py + 1.15} a={it.ten_b_ben === "trai" ? "end" : it.ten_b_ben === "phai" ? "start" : "middle"} fill={c} size={FS}>
              {tB}
            </Label>
          )}
        </g>
      );
    }
    if (it.loai === "diem") {
      return <g className={cls}>{diem(it.x, it.y ?? 0, it.ten, it.vi ?? (it.y && it.y < 0 ? "b" : "t"), mauCua(it.mau))}</g>;
    }
    if (it.loai === "tia") {
      const c = mauCua(it.mau);
      const pts = it.qua.map((q) => [...q]);
      if (it.mep && pts.length >= 2) {
        const [a, bb] = [pts[pts.length - 2], pts[pts.length - 1]];
        const dx = bb[0] - a[0],
          dy = bb[1] - a[1];
        const ts = [dx > 0 ? (p.x_max - bb[0]) / dx : dx < 0 ? (p.x_min - bb[0]) / dx : Infinity, dy > 0 ? (p.y_tren - bb[1]) / dy : dy < 0 ? (p.y_duoi - bb[1]) / dy : Infinity];
        const t = Math.min(...ts);
        if (Number.isFinite(t) && t > 0) pts.push([bb[0] + dx * t, bb[1] + dy * t]);
      }
      return (
        <g className={cls}>
          {duong(pts, c, !!it.dut, true)}
          {it.keo && duong(it.keo, c, true, false)}
        </g>
      );
    }
    if (it.loai === "thuoc") {
      const c = C_MAX;
      if (it.doc) {
        const px = X(it.o),
          y1 = Y(it.tu),
          y2 = Y(it.den),
          trai = it.ben === "trai";
        return (
          <g className={cls}>
            <g stroke={c} strokeWidth={0.07}>
              <line x1={px} y1={y1} x2={px} y2={y2} />
              <line x1={px - 0.22} y1={y1} x2={px + 0.22} y2={y1} />
              <line x1={px - 0.22} y1={y2} x2={px + 0.22} y2={y2} />
            </g>
            <Label x={trai ? px - 0.3 : px + 0.3} y={(y1 + y2) / 2 + 0.38} a={trai ? "end" : "start"} fill={c} size={FS}>
              {it.nhan}
            </Label>
          </g>
        );
      }
      const py = Y(it.o),
        x1 = X(it.tu),
        x2 = X(it.den),
        duoi = it.ben === "duoi";
      return (
        <g className={cls}>
          <g stroke={c} strokeWidth={0.07}>
            <line x1={x1} y1={py} x2={x2} y2={py} />
            <line x1={x1} y1={py - 0.22} x2={x1} y2={py + 0.22} />
            <line x1={x2} y1={py - 0.22} x2={x2} y2={py + 0.22} />
          </g>
          <Label x={(x1 + x2) / 2} y={duoi ? py + 1.05 : py - 0.3} fill={c} size={FS}>
            {it.nhan}
          </Label>
        </g>
      );
    }
    if (it.loai === "chu") {
      return (
        <g className={cls}>
          <Label x={X(it.x)} y={Y(it.y)} a={it.a ?? "middle"} size={FS} fill={mauCua(it.mau)}>
            {it.text}
          </Label>
        </g>
      );
    }
    return null;
  }

  // thứ tự vẽ: lưới, trục, thấu kính, tia, vật/ảnh, nhãn
  const hang = (it: ThauKinhLop) => (it.loai === "tk" ? 0 : it.loai === "tia" ? 1 : it.loai === "vat" ? 2 : 3);
  const tat = [...hinhHien.map((it) => [it, false] as const), ...items.map((it) => [it, true] as const)].sort((a, c) => hang(a[0]) - hang(c[0]));

  const luoi = [];
  if (p.o_ly) {
    const o = p.o_ly;
    for (let x = Math.ceil(p.x_min / o) * o; x <= p.x_max + 1e-9; x += o) luoi.push(<line key={`gx${x}`} x1={X(x)} y1={TOP} x2={X(x)} y2={Y(p.y_duoi)} />);
    for (let y = Math.ceil(p.y_duoi / o) * o; y <= p.y_tren + 1e-9; y += o) luoi.push(<line key={`gy${y}`} x1={0} y1={Y(y)} x2={W} y2={Y(y)} />);
  }

  return (
    <svg viewBox={`-0.4 -0.2 ${W + 0.8} ${H + 3.7}`} className="cc-fig" role="img" aria-label="Thấu kính, vật và ảnh trên trục chính">
      <g key={`p${tb}`}>
        {luoi.length > 0 && (
          <g stroke="currentColor" strokeWidth={0.03} opacity={0.22}>
            {luoi}
          </g>
        )}
        <line x1={0} y1={Y0} x2={W} y2={Y0} stroke="currentColor" strokeWidth={0.07} />
        {tat.map(([it, m], j) => (
          <g key={`${tb}-${j}`}>{veMuc(it, m)}</g>
        ))}
      </g>
      {ghi.map((t, i) => (
        <Label key={`${Lr}-${b}-${i}`} x={W / 2} y={H + 1.2 + i * 1.45} size={FS}>
          {t}
        </Label>
      ))}
      {/* giữ chỗ dải dưới để hình không đổi cao (D2) */}
      <rect x={0} y={H} width={0.01} height={3.1} fill="none" />
    </svg>
  );
}
