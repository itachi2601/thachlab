"use client";

/**
 * Họ hình `mach_dien` (đợt Đ3 3/11/2026, mẫu đầu: bài 24 Nguồn điện L11, dạng 3): sơ đồ mạch nét đơn — nguồn/pin (vạch
 * dài mảnh là cực +), điện trở, đèn, vôn kế/ampe kế, khoá, nút nối; mũi tên dòng điện cam, ngoặc gom nhóm (dãy pin, đoạn
 * mạch), bảng số nhỏ điền dần theo bước. Linh kiện đặt TÂM tại (x, y), nền halo che dây bên dưới nên dây vẽ một nét
 * xuyên qua. Hình không đổi cao giữa các bước (D2); nhãn cạnh linh kiện (N8, H3); dây giả định nét đứt (H4).
 *
 * JSON: { loai: "mach_dien", hinh?: [mục…] (vẽ sẵn theo đề), lop: [[mục…] cho bước 1, …] }. Toạ độ 0..20 ngang, 0..11
 * dọc, gốc dưới trái, y hướng lên. Mục: day {diem: [[x,y],…], dut?, mau?} · nut {x,y} · nguon {x,y,huong?,duong?,ten?,vi?}
 *  (duong "sau" = cực + ở phía x lớn / y lớn, mặc định) · dien_tro {x,y,huong?,ten?,vi?} · den {x,y,ten?,vi?}
 *  · dong_ho {x,y,kieu: "V"|"A",ten?,vi?} · khoa {x,y,huong?,mo?} · dong {tu,den,nhan?,vi?} · ngoac {tu,den,nhan,vi?,mau?}
 *  · chu {x,y,text,a?,mau?} · bang {x (giữa), y (mép trên), hang: [[ô…],…]} (ô "?" vẽ mờ) · ghi {text}.
 *  `vi` = chỗ đặt nhãn: t trên, b dưới, l trái, r phải. `het: k` = ẩn từ khi xong bước k (cả mục trong `hinh`).
 */

import { C_MAX, C_MIN, Chevron, Label, chiaDong, dangHien, ghiMoiNhat } from "@/components/lessons/cong-cu/chung";
import type { MachDienLop } from "@/features/lessons/types";

type Props = { hinh?: MachDienLop[]; lop?: MachDienLop[][]; layer: number };
type Vi = "t" | "b" | "l" | "r";

const W = 20,
  H = 11;
const Y = (y: number) => H - y;
const mau = (m?: string) => (m === "max" ? C_MAX : m === "min" ? C_MIN : "currentColor");
const HALO = "var(--cc-halo)";

/** Nhãn cạnh linh kiện bán kính r (đơn vị hình) tại (x, Y). */
function NhanCanh({ x, y, r, vi = "t", text, fill }: { x: number; y: number; r: number; vi?: Vi; text: string; fill?: string }) {
  const [lx, ly, a] =
    vi === "t"
      ? [x, y - r - 0.35, "middle"]
      : vi === "b"
        ? [x, y + r + 1.05, "middle"]
        : vi === "l"
          ? [x - r - 0.35, y + 0.4, "end"]
          : [x + r + 0.35, y + 0.4, "start"];
  return (
    <Label x={lx as number} y={ly as number} a={a as "start" | "middle" | "end"} fill={fill} size={1.05}>
      {text}
    </Label>
  );
}

function veMuc(it: MachDienLop, moi: boolean) {
  const cls = moi ? "cc-in" : undefined;
  if (it.loai === "day") {
    return (
      <polyline
        className={cls}
        points={it.diem.map(([x, y]) => `${x},${Y(y)}`).join(" ")}
        fill="none"
        stroke={mau(it.mau)}
        strokeWidth={it.dut ? 0.1 : 0.11}
        strokeDasharray={it.dut ? "0.4 0.25" : undefined}
        strokeLinejoin="round"
        strokeLinecap="round"
      />
    );
  }
  if (it.loai === "nut") return <circle className={cls} cx={it.x} cy={Y(it.y)} r={0.17} fill="currentColor" />;
  if (it.loai === "nguon") {
    // vạch dài mảnh = cực +, vạch ngắn đậm = cực −
    const doc = it.huong === "doc",
      s = it.duong === "truoc" ? -1 : 1,
      cx = it.x,
      cy = Y(it.y),
      g = 0.17;
    const vach = (o: number, dai: number, day: number) =>
      doc ? (
        <line x1={cx - dai} y1={cy - o} x2={cx + dai} y2={cy - o} stroke="currentColor" strokeWidth={day} />
      ) : (
        <line x1={cx + o} y1={cy - dai} x2={cx + o} y2={cy + dai} stroke="currentColor" strokeWidth={day} />
      );
    return (
      <g className={cls}>
        <rect
          x={doc ? cx - 0.8 : cx - g - 0.08}
          y={doc ? cy - g - 0.08 : cy - 0.8}
          width={doc ? 1.6 : 2 * g + 0.16}
          height={doc ? 2 * g + 0.16 : 1.6}
          fill={HALO}
        />
        {vach(s * g, 0.75, 0.08)}
        {vach(-s * g, 0.4, 0.22)}
        {it.ten && <NhanCanh x={cx} y={cy} r={0.75} vi={it.vi} text={it.ten} />}
      </g>
    );
  }
  if (it.loai === "dien_tro") {
    const doc = it.huong === "doc",
      [w, h] = doc ? [0.75, 2] : [2, 0.75];
    return (
      <g className={cls}>
        <rect x={it.x - w / 2} y={Y(it.y) - h / 2} width={w} height={h} fill={HALO} stroke="currentColor" strokeWidth={0.1} />
        {it.ten && <NhanCanh x={it.x} y={Y(it.y)} r={(it.vi === "l" || it.vi === "r" ? w : h) / 2} vi={it.vi} text={it.ten} />}
      </g>
    );
  }
  if (it.loai === "den") {
    const cx = it.x,
      cy = Y(it.y),
      r = 0.65,
      k = r * 0.7;
    return (
      <g className={cls}>
        <circle cx={cx} cy={cy} r={r} fill={HALO} stroke="currentColor" strokeWidth={0.1} />
        <path d={`M${cx - k} ${cy - k} L${cx + k} ${cy + k} M${cx + k} ${cy - k} L${cx - k} ${cy + k}`} stroke="currentColor" strokeWidth={0.08} />
        {it.ten && <NhanCanh x={cx} y={cy} r={r} vi={it.vi} text={it.ten} />}
      </g>
    );
  }
  if (it.loai === "dong_ho") {
    const cx = it.x,
      cy = Y(it.y);
    return (
      <g className={cls}>
        <circle cx={cx} cy={cy} r={0.78} fill={HALO} stroke="currentColor" strokeWidth={0.1} />
        <text x={cx} y={cy + 0.4} fontSize={1.15} textAnchor="middle" fontWeight={800} fill="currentColor">
          {it.kieu}
        </text>
        {it.ten && <NhanCanh x={cx} y={cy} r={0.78} vi={it.vi} text={it.ten} />}
      </g>
    );
  }
  if (it.loai === "khoa") {
    const doc = it.huong === "doc",
      cx = it.x,
      cy = Y(it.y);
    const [ax, ay, bx, by] = doc ? [cx, cy + 0.7, cx, cy - 0.7] : [cx - 0.7, cy, cx + 0.7, cy];
    const [ex, ey] = it.mo ? (doc ? [cx - 0.75, by + 0.3] : [bx - 0.3, cy - 0.75]) : [bx, by];
    return (
      <g className={cls}>
        <rect x={doc ? cx - 0.3 : ax} y={doc ? by : cy - 0.3} width={doc ? 0.6 : 1.4} height={doc ? 1.4 : 0.6} fill={HALO} />
        <line x1={ax} y1={ay} x2={ex} y2={ey} stroke="currentColor" strokeWidth={0.1} strokeLinecap="round" />
        <circle cx={ax} cy={ay} r={0.13} fill="currentColor" />
        <circle cx={bx} cy={by} r={0.13} fill="none" stroke="currentColor" strokeWidth={0.07} />
      </g>
    );
  }
  if (it.loai === "dong") {
    const [x1, y1] = it.tu,
      [x2, y2] = it.den,
      ang = Math.atan2(-(y2 - y1), x2 - x1),
      mx = (x1 + x2) / 2,
      my = Y((y1 + y2) / 2);
    return (
      <g className={cls}>
        <line x1={x1} y1={Y(y1)} x2={x2} y2={Y(y2)} stroke={C_MAX} strokeWidth={0.16} strokeLinecap="round" />
        <Chevron x={x2} y={Y(y2)} ang={ang} color={C_MAX} len={0.5} w={0.14} />
        {it.nhan && <NhanCanh x={mx} y={my} r={0.1} vi={it.vi ?? "t"} text={it.nhan} fill={C_MAX} />}
      </g>
    );
  }
  if (it.loai === "ngoac") {
    // ngoặc vuông song song đoạn tu → den (ngang hoặc dọc), râu chỉ về phía linh kiện
    const [x1, y1] = it.tu,
      [x2, y2] = it.den,
      c = mau(it.mau),
      ngang = Math.abs(y2 - y1) < Math.abs(x2 - x1),
      s = it.vi === "b" ? 1 : -1; // SVG: t (trên) là y nhỏ hơn
    const p = ngang
      ? `M${x1} ${Y(y1) - s * 0.35} L${x1} ${Y(y1)} L${x2} ${Y(y2)} L${x2} ${Y(y2) - s * 0.35}`
      : `M${x1 - s * 0.35} ${Y(y1)} L${x1} ${Y(y1)} L${x2} ${Y(y2)} L${x2 - s * 0.35} ${Y(y2)}`;
    const mx = (x1 + x2) / 2,
      my = Y((y1 + y2) / 2);
    return (
      <g className={cls}>
        <path d={p} fill="none" stroke={c} strokeWidth={0.08} />
        {ngang ? (
          <Label x={mx} y={s < 0 ? my - 0.35 : my + 1.15} fill={c} size={1.05}>
            {it.nhan}
          </Label>
        ) : (
          <Label x={s < 0 ? mx + 0.35 : mx - 0.35} y={my + 0.4} a={s < 0 ? "start" : "end"} fill={c} size={1.05}>
            {it.nhan}
          </Label>
        )}
      </g>
    );
  }
  if (it.loai === "chu") {
    return (
      <g className={cls}>
        <Label x={it.x} y={Y(it.y)} a={it.a ?? "middle"} fill={it.mau ? mau(it.mau) : undefined} size={1.05}>
          {it.text}
        </Label>
      </g>
    );
  }
  if (it.loai === "bang") {
    // bảng số nhỏ: cột rộng theo ô dài nhất (≈ 0,6 × cỡ chữ mỗi ký tự), hàng đầu là tiêu đề
    const size = 1,
      rh = 1.35,
      cols = Math.max(...it.hang.map((r) => r.length)),
      cw = Array.from({ length: cols }, (_, j) =>
        Math.max(...it.hang.map((r) => (r[j] ?? "").replace(/_\{?/g, "").length)) * 0.6 * size + 0.9,
      ),
      tw = cw.reduce((a, b) => a + b, 0),
      x0 = it.x - tw / 2,
      y0 = Y(it.y);
    const cx = (j: number) => x0 + cw.slice(0, j).reduce((a, b) => a + b, 0) + cw[j] / 2;
    return (
      <g className={cls}>
        <rect x={x0} y={y0} width={tw} height={rh * it.hang.length} fill="none" stroke="currentColor" strokeWidth={0.05} opacity={0.5} />
        <line x1={x0} y1={y0 + rh} x2={x0 + tw} y2={y0 + rh} stroke="currentColor" strokeWidth={0.05} opacity={0.5} />
        <line x1={x0 + cw[0]} y1={y0} x2={x0 + cw[0]} y2={y0 + rh * it.hang.length} stroke="currentColor" strokeWidth={0.05} opacity={0.5} />
        {it.hang.map((r, i) =>
          r.map((o, j) => (
            <g key={`${i}-${j}`} opacity={o === "?" ? 0.45 : 1}>
              <Label x={cx(j)} y={y0 + rh * i + 0.98} size={size} fill={i > 0 && j === cols - 1 && o !== "?" ? C_MAX : undefined}>
                {o}
              </Label>
            </g>
          )),
        )}
      </g>
    );
  }
  return null;
}

export default function MachDien({ hinh = [], lop, layer: L }: Props) {
  const items = dangHien(lop, L);
  const ghi = ghiMoiNhat(lop, L).flatMap((t) => chiaDong(t, W, 1.05)).slice(0, 2);
  // dây vẽ trước linh kiện để nền halo của linh kiện che được dây
  const thu = (it: MachDienLop) => (it.loai === "day" ? 0 : 1);
  const hinhHien = hinh.filter((it) => it.het == null || L < it.het);
  return (
    <svg viewBox={`-0.4 -1.1 ${W + 0.8} ${H + 4.9}`} className="cc-fig" role="img" aria-label="Sơ đồ mạch điện">
      {[...hinhHien.map((it) => [it, false] as const), ...items.map((it) => [it, true] as const)]
        .map(([it, moi], k) => ({ it, moi, k }))
        .sort((a, b) => thu(a.it) - thu(b.it) || a.k - b.k)
        .map(({ it, moi, k }) => (
          <g key={`${moi ? "l" : "h"}${k}`}>{veMuc(it, moi)}</g>
        ))}
      {ghi.map((t, i) => (
        <Label key={`${L}-${i}`} x={W / 2} y={H + 1.7 + i * 1.45} size={1.05}>
          {t}
        </Label>
      ))}
      {/* giữ chỗ dải dưới để hình không đổi cao (D2) */}
      <rect x={0} y={H} width={0.01} height={3.6} fill="none" />
    </svg>
  );
}
