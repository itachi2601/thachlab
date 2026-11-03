"use client";

/**
 * Họ hình `thanh_nang_luong` (đợt Đ2 3/11/2026, mẫu đầu: bài 7 Chuyển hoá năng lượng trong dao động L11, dạng 2):
 * cảnh bên trái (lò xo ngang, con lắc đơn, vật ở độ cao, hộp hệ ĐL1) + các cột năng lượng cùng một thang bên phải.
 * Cột rỗng (viền đứt) giữ chỗ từ đầu, bước nào tính xong thì cột đó đầy và có số trên đầu cột (H3, M4: số đi kèm màu).
 * Hình không đổi cao giữa các bước (D2); không hoạt hình (thầy 2/11).
 *
 * JSON: { loai: "thanh_nang_luong", canh: {kieu…}, cot: [{ten, mau?}], max, don_vi?, lop: [[mục…] cho bước 1, …] }.
 * canh: lo_xo_ngang {A, don_vi?, x?}  ·  con_lac_don {goc0, goc?}  ·  doc {h, don_vi?, vi?}  ·  hop_he {ten?}
 * Mục: cot {ten, gia_tri, nhan?}  ·  vat {x? | goc? | vi?, bong?} (đặt lại vật; bong = bóng đối xứng −x)
 *  ·  v {nhan, chieu?: 1|-1} (mũi tên vận tốc ở vật)  ·  mui {vao, nhan, hang?} (hộp hệ: Q, A vào/ra)  ·  ghi {text}.
 * `het: k` = ẩn từ khi xong bước k.
 */

import { C_MAX, C_MIN, Chevron, Label, dangHien, fmt, ghiMoiNhat } from "@/components/lessons/cong-cu/chung";
import type { NangLuongCanh, NangLuongLop } from "@/features/lessons/types";

type Props = {
  canh: NangLuongCanh;
  cot: { ten: string; mau?: "max" | "min" | "chu" }[];
  max: number;
  don_vi?: string;
  lop?: NangLuongLop[][];
  layer: number;
};

const BASE = 10,
  CAO = 7.6; // đáy cột và chiều cao ứng với `max`
const mau = (m?: string) => (m === "max" ? C_MAX : m === "min" ? C_MIN : "currentColor");

function MuiTen({
  x1,
  y1,
  x2,
  y2,
  c,
  nhan,
  w = 0.14,
}: {
  x1: number;
  y1: number;
  x2: number;
  y2: number;
  c: string;
  nhan?: string;
  w?: number;
}) {
  const ang = Math.atan2(y2 - y1, x2 - x1);
  return (
    <g className="cc-in">
      <line x1={x1} y1={y1} x2={x2} y2={y2} stroke={c} strokeWidth={w} />
      <Chevron x={x2} y={y2} ang={ang} color={c} len={0.5} w={w} />
      {nhan && (
        <Label x={(x1 + x2) / 2} y={Math.min(y1, y2) - 0.45} fill={c} size={1.05}>
          {nhan}
        </Label>
      )}
    </g>
  );
}

function LoXo({ x1, x2, y }: { x1: number; x2: number; y: number }) {
  const n = 10,
    d = (x2 - x1 - 0.6) / n;
  let p = `M${x1} ${y} h0.3`;
  for (let i = 0; i < n; i++) p += ` l${d / 2} ${i % 2 ? 0.45 : -0.45} l${d / 2} ${i % 2 ? -0.45 : 0.45}`;
  p += " h0.3";
  return <path d={p} stroke="currentColor" strokeWidth={0.08} fill="none" strokeLinejoin="round" />;
}

function Canh({ canh, items }: { canh: NangLuongCanh; items: NangLuongLop[] }) {
  const vat = [...items].reverse().find((it) => it.loai === "vat") as
    Extract<NangLuongLop, { loai: "vat" }> | undefined;
  const v = [...items].reverse().find((it) => it.loai === "v") as Extract<NangLuongLop, { loai: "v" }> | undefined;
  if (canh.kieu === "lo_xo_ngang") {
    const O = 6.6,
      S = 4.4 / canh.A,
      X = (x: number) => O + x * S,
      x = vat?.x ?? canh.x ?? canh.A;
    const yS = 5.4,
      bw = 1.6,
      bh = 1.4;
    const khoi = (cx: number, dut: boolean) => (
      <rect
        x={cx - bw / 2}
        y={yS - bh / 2}
        width={bw}
        height={bh}
        rx={0.15}
        fill={dut ? "none" : "var(--cc-halo)"}
        stroke="currentColor"
        strokeWidth={0.1}
        strokeDasharray={dut ? "0.3 0.2" : undefined}
      />
    );
    return (
      <g>
        <line x1={0.8} y1={3.4} x2={0.8} y2={yS + bh / 2 + 0.1} stroke="currentColor" strokeWidth={0.12} />
        {[3.6, 4.3, 5.0, 5.7].map((y) => (
          <line key={y} x1={0.8} y1={y} x2={0.35} y2={y + 0.4} stroke="currentColor" strokeWidth={0.05} />
        ))}
        <line
          x1={0.8}
          y1={yS + bh / 2 + 0.1}
          x2={12}
          y2={yS + bh / 2 + 0.1}
          stroke="currentColor"
          strokeWidth={0.07}
          opacity={0.6}
        />
        <LoXo x1={0.8} x2={X(x) - bw / 2} y={yS} />
        {vat?.bong && x !== 0 && <g className="cc-in">{khoi(X(-x), true)}</g>}
        {khoi(X(x), false)}
        {/* trục x: −A, O, A */}
        <line x1={X(-canh.A) - 0.4} y1={8} x2={X(canh.A) + 0.8} y2={8} stroke="currentColor" strokeWidth={0.06} />
        <Chevron x={X(canh.A) + 0.8} y={8} ang={0} len={0.35} w={0.06} />
        {[-canh.A, 0, canh.A].map((t) => (
          <g key={t}>
            <line x1={X(t)} y1={7.8} x2={X(t)} y2={8.2} stroke="currentColor" strokeWidth={0.06} />
            <Label x={X(t)} y={9.3} size={0.95}>
              {t === 0 ? "O" : fmt(t)}
            </Label>
          </g>
        ))}
        {vat && vat.x != null && Math.abs(vat.x) !== canh.A && vat.x !== 0 && (
          <g className="cc-in">
            <line
              x1={X(x)}
              y1={yS + bh / 2}
              x2={X(x)}
              y2={9.9}
              stroke={C_MIN}
              strokeWidth={0.06}
              strokeDasharray="0.25 0.2"
            />
            <Label x={X(x)} y={10.95} size={0.95} fill={C_MIN}>
              {fmt(x)}
            </Label>
            {vat.bong && (
              <>
                <line
                  x1={X(-x)}
                  y1={yS + bh / 2}
                  x2={X(-x)}
                  y2={9.9}
                  stroke={C_MIN}
                  strokeWidth={0.06}
                  strokeDasharray="0.25 0.2"
                />
                <Label x={X(-x)} y={10.95} size={0.95} fill={C_MIN}>
                  {fmt(-x)}
                </Label>
              </>
            )}
          </g>
        )}
        <Label x={X(canh.A) + 0.8} y={7.5} a="end" size={0.95}>
          {`x (${canh.don_vi ?? "cm"})`}
        </Label>
        {v && (
          <MuiTen
            x1={X(x)}
            y1={yS - bh / 2 - 0.9}
            x2={X(x) + (v.chieu ?? 1) * 2.4}
            y2={yS - bh / 2 - 0.9}
            c={C_MAX}
            nhan={v.nhan}
          />
        )}
      </g>
    );
  }
  if (canh.kieu === "con_lac_don") {
    const px = 6.4,
      py = 1.2,
      len = 6.4,
      g = ((vat?.goc ?? canh.goc ?? canh.goc0) * Math.PI) / 180,
      g0 = (canh.goc0 * Math.PI) / 180;
    const bx = px + len * Math.sin(g),
      by = py + len * Math.cos(g);
    const arc = (a: number) => `${px + len * Math.sin(a)} ${py + len * Math.cos(a)}`;
    return (
      <g>
        <line x1={px - 2} y1={py} x2={px + 2} y2={py} stroke="currentColor" strokeWidth={0.12} />
        <line
          x1={px}
          y1={py}
          x2={px}
          y2={py + len + 0.6}
          stroke="currentColor"
          strokeWidth={0.05}
          strokeDasharray="0.3 0.2"
          opacity={0.7}
        />
        <path
          d={`M${arc(-g0)} A${len} ${len} 0 0 0 ${arc(g0)}`}
          stroke="currentColor"
          strokeWidth={0.05}
          fill="none"
          strokeDasharray="0.3 0.2"
          opacity={0.7}
        />
        <line x1={px} y1={py} x2={bx} y2={by} stroke="currentColor" strokeWidth={0.08} />
        <circle cx={bx} cy={by} r={0.5} fill="var(--cc-halo)" stroke="currentColor" strokeWidth={0.1} />
        {v && (
          <MuiTen
            x1={bx}
            y1={by}
            x2={bx + (v.chieu ?? 1) * 2.2 * Math.cos(g)}
            y2={by - (v.chieu ?? 1) * 2.2 * Math.sin(g)}
            c={C_MAX}
            nhan={v.nhan}
          />
        )}
      </g>
    );
  }
  if (canh.kieu === "doc") {
    const vi = vat?.vi ?? canh.vi ?? 1,
      yG = 9.6,
      yT = 2,
      y = yG - (yG - yT) * vi;
    return (
      <g>
        <line x1={0.6} y1={yG} x2={12} y2={yG} stroke="currentColor" strokeWidth={0.1} />
        {Array.from({ length: 19 }, (_, i) => (
          <line
            key={i}
            x1={0.8 + i * 0.6}
            y1={yG}
            x2={0.4 + i * 0.6}
            y2={yG + 0.4}
            stroke="currentColor"
            strokeWidth={0.04}
          />
        ))}
        <line x1={2} y1={yT} x2={2} y2={yG} stroke={C_MIN} strokeWidth={0.06} />
        <Chevron x={2} y={yT} ang={-Math.PI / 2} color={C_MIN} len={0.35} w={0.06} />
        <Chevron x={2} y={yG} ang={Math.PI / 2} color={C_MIN} len={0.35} w={0.06} />
        <Label x={2.4} y={(yT + yG) / 2} a="start" size={1} fill={C_MIN}>
          {`h = ${fmt(canh.h)} ${canh.don_vi ?? "m"}`}
        </Label>
        <line
          x1={7}
          y1={yT}
          x2={7}
          y2={yG}
          stroke="currentColor"
          strokeWidth={0.05}
          strokeDasharray="0.3 0.2"
          opacity={0.6}
        />
        <circle cx={7} cy={y - 0.5} r={0.5} fill="var(--cc-halo)" stroke="currentColor" strokeWidth={0.1} />
        {v && <MuiTen x1={8} y1={y - 0.5} x2={8} y2={y - 0.5 + 2.2} c={C_MAX} nhan={v.nhan} />}
      </g>
    );
  }
  // hop_he: hộp hệ, mũi tên Q / A vào (trái → hộp) hoặc ra (hộp → phải)
  const mui = items.filter((it) => it.loai === "mui") as Extract<NangLuongLop, { loai: "mui" }>[];
  return (
    <g>
      <rect x={4} y={3} width={5} height={4.6} rx={0.3} fill="none" stroke="currentColor" strokeWidth={0.12} />
      <Label x={6.5} y={5.7} size={1.1}>
        {canh.ten ?? "hệ"}
      </Label>
      {mui.map((m, k) => {
        const y = 3.9 + (m.hang ?? k) * 1.5;
        return m.vao ? (
          <MuiTen key={k} x1={0.6} y1={y} x2={3.8} y2={y} c={C_MAX} nhan={m.nhan} />
        ) : (
          <MuiTen key={k} x1={9.2} y1={y} x2={12.4} y2={y} c={C_MIN} nhan={m.nhan} />
        );
      })}
    </g>
  );
}

export default function ThanhNangLuong({ canh, cot, max, lop, layer: L }: Props) {
  const items = dangHien(lop, L);
  const ghi = ghiMoiNhat(lop, L);
  const val = new Map<string, { v: number; nhan?: string }>();
  for (const it of items) if (it.loai === "cot") val.set(it.ten, { v: it.gia_tri, nhan: it.nhan });
  const x0 = 14.2,
    step = 2.5,
    bw = 1.6;
  const ghiY = BASE + 2.9;
  return (
    <svg
      viewBox={`0 0 ${x0 + step * cot.length + 0.2} ${ghiY + 0.8}`}
      className="cc-fig"
      role="img"
      aria-label="Cảnh và các cột năng lượng"
    >
      <Canh canh={canh} items={items} />
      <line
        x1={x0 - 0.6}
        y1={BASE}
        x2={x0 + step * cot.length - 0.4}
        y2={BASE}
        stroke="currentColor"
        strokeWidth={0.08}
      />
      {cot.map((c, i) => {
        const x = x0 + i * step,
          d = val.get(c.ten),
          h = d ? Math.max(0.06, (d.v / max) * CAO) : 0,
          f = mau(c.mau);
        return (
          <g key={c.ten}>
            {/* viền đứt giữ chỗ chỉ khi cột chưa có số — đầy rồi thì nhãn đầu cột khỏi chạm viền (HS ảo 3/11) */}
            {!d && (
              <rect
                x={x}
                y={BASE - CAO}
                width={bw}
                height={CAO}
                fill="none"
                stroke="currentColor"
                strokeWidth={0.04}
                strokeDasharray="0.25 0.2"
                opacity={0.45}
              />
            )}
            {d && (
              <g className="cc-in">
                <rect
                  x={x}
                  y={BASE - h}
                  width={bw}
                  height={h}
                  fill={f}
                  fillOpacity={c.mau === "chu" || !c.mau ? 0.28 : 0.55}
                  stroke={f}
                  strokeWidth={0.08}
                />
                {d.nhan && (
                  <Label
                    x={x + bw / 2}
                    y={BASE - h - 0.4}
                    size={Math.min(0.95, (2 * step - bw - 0.4) / (d.nhan.length * 0.6))}
                  >
                    {d.nhan}
                  </Label>
                )}
              </g>
            )}
            <Label x={x + bw / 2} y={BASE + 1.2} size={1.05} fill={f}>
              {c.ten}
            </Label>
          </g>
        );
      })}
      {ghi.slice(0, 1).map((t, i) => (
        <Label
          key={`${L}-${i}`}
          x={(x0 + step * cot.length) / 2}
          y={ghiY}
          size={Math.min(1.05, (x0 + step * cot.length) / (t.length * 0.6))}
        >
          {t}
        </Label>
      ))}
    </svg>
  );
}
