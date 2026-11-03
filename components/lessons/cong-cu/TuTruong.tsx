"use client";

/**
 * Họ hình `tu_truong` (đợt Đ2 3/11/2026, mẫu đầu: bài 10 Lực từ L12, dạng 4): nền cảm ứng từ (⊙ ra, ⊗ vào, hoặc đường
 * sức nét đứt mũi chevron 30° — AGENTS), dây thẳng, mũi tên dòng điện, tiết diện dây ⊙/⊗, vectơ lực/pháp tuyến dài theo
 * tỉ lệ độ lớn, cung góc, nam châm thẳng (màu như `bar_magnet` trong svg_lib.py: N đỏ, S xanh). Không hoạt hình.
 * Hình không đổi cao giữa các bước (D2); nhãn trên hình (N8, H3); vectơ thứ hai nét đứt (H4).
 *
 * JSON: { loai: "tu_truong", nen?: {kieu: "ra"|"vao"|"duong_suc", goc?, nhan?, hang?}, hinh?: [mục…] (vẽ sẵn theo đề),
 *         lop: [[mục…] cho bước 1, …] }. Toạ độ 0..20 ngang, 0..11 dọc, gốc dưới trái, y hướng lên; góc theo độ.
 * Mục: day {tu,den,nhan?,mau?,dut?}  ·  dong {tu,den,nhan?} (mũi tên I)  ·  tiet_dien {x,y,chieu,ten?}
 *  ·  vec {x,y,goc,dai,nhan?,mau?,dut?,trai?}  ·  goc {x,y,tu,den,nhan?}  ·  chu {x,y,text,a?}  ·  nam_cham {x,y,dai,cao,n_trai?}
 *  ·  tran {x1,x2,y} (giá treo gạch chéo)  ·  khung {x,y,rong,sau:[dx,dy],ten?,B?,nhan?} (hình nhỏ khung ABCD nhìn nghiêng,
 *  A ở (x,y))  ·  ghi {text}. `het: k` = ẩn từ khi xong bước k (cả mục trong `hinh`).
 */

import { C_MAX, C_MIN, Chevron, Label, dangHien, ghiMoiNhat } from "@/components/lessons/cong-cu/chung";
import type { TuTruongLop, TuTruongNen } from "@/features/lessons/types";

type Props = { nen?: TuTruongNen; hinh?: TuTruongLop[]; lop?: TuTruongLop[][]; layer: number };

const W = 20,
  H = 11;
const Y = (y: number) => H - y;
const rad = (d: number) => (d * Math.PI) / 180;
const mau = (m?: string) => (m === "max" ? C_MAX : m === "min" ? C_MIN : "currentColor");
// bảng màu nam châm chuẩn (svg_lib.py UM_*)
const UM_EDGE = "#334155",
  UM_N = ["#dc2626", "#f87171", "#b91c1c"],
  UM_S = ["#2563eb", "#60a5fa", "#1e40af"];

function Nen({ nen }: { nen: TuTruongNen }) {
  if (nen.kieu === "duong_suc") {
    const g = rad(nen.goc ?? 0),
      c = Math.cos(g),
      s = Math.sin(g);
    const hang = nen.hang ?? [1, 3, 5, 7, 9];
    return (
      <g>
        <g opacity={0.5}>
          {hang.map((h) => {
            // đường sức qua (10, h) theo hướng góc g, cắt trong khung
            const x1 = 10 - 11 * c,
              y1 = h - 11 * s,
              x2 = 10 + 11 * c,
              y2 = h + 11 * s;
            return (
              <g key={h}>
                <line
                  x1={x1}
                  y1={Y(y1)}
                  x2={x2}
                  y2={Y(y2)}
                  stroke={C_MIN}
                  strokeWidth={0.06}
                  strokeDasharray="0.4 0.25"
                />
                <Chevron x={10 + 6 * c} y={Y(h + 6 * s)} ang={-g} color={C_MIN} len={0.4} w={0.07} />
                <Chevron x={10 - 4 * c} y={Y(h - 4 * s)} ang={-g} color={C_MIN} len={0.4} w={0.07} />
              </g>
            );
          })}
        </g>
        {nen.nhan && (
          // đường sức trên cùng sát mép trên thì đặt nhãn dưới đường, khỏi bị viewBox cắt
          <Label
            x={0.4}
            y={Y(hang[hang.length - 1]) - 0.35 < 1 ? Y(hang[hang.length - 1]) + 1.2 : Y(hang[hang.length - 1]) - 0.35}
            a="start"
            fill={C_MIN}
            size={1.05}
          >
            {nen.nhan}
          </Label>
        )}
      </g>
    );
  }
  const pts: [number, number][] = [];
  for (let x = 1; x < W; x += 2) for (let y = 1; y < H; y += 2) pts.push([x, y]);
  return (
    <g>
      <g opacity={0.38} stroke={C_MIN} fill="none" strokeWidth={0.05}>
        {pts.map(([x, y]) => (
          <g key={`${x}-${y}`}>
            <circle cx={x} cy={Y(y)} r={0.28} />
            {nen.kieu === "ra" ? (
              <circle cx={x} cy={Y(y)} r={0.07} fill={C_MIN} />
            ) : (
              <path d={`M${x - 0.18} ${Y(y) - 0.18} l0.36 0.36 M${x + 0.18} ${Y(y) - 0.18} l-0.36 0.36`} />
            )}
          </g>
        ))}
      </g>
      {nen.nhan && (
        <Label x={0.4} y={0.9} a="start" fill={C_MIN} size={1.05}>
          {nen.nhan}
        </Label>
      )}
    </g>
  );
}

function Muc({ it, moi }: { it: TuTruongLop; moi: boolean }) {
  const cls = moi ? "cc-in" : undefined;
  if (it.loai === "day") {
    const [x1, y1] = it.tu,
      [x2, y2] = it.den;
    return (
      <g className={cls}>
        <line
          x1={x1}
          y1={Y(y1)}
          x2={x2}
          y2={Y(y2)}
          stroke={mau(it.mau)}
          strokeWidth={it.dut ? 0.1 : 0.2}
          strokeDasharray={it.dut ? "0.4 0.25" : undefined}
          strokeLinecap="round"
        />
        {it.nhan && (
          <Label x={(x1 + x2) / 2} y={Y((y1 + y2) / 2) - 0.45}>
            {it.nhan}
          </Label>
        )}
      </g>
    );
  }
  if (it.loai === "dong") {
    const [x1, y1] = it.tu,
      [x2, y2] = it.den,
      ang = Math.atan2(-(y2 - y1), x2 - x1);
    return (
      <g className={cls}>
        <line x1={x1} y1={Y(y1)} x2={x2} y2={Y(y2)} stroke={C_MAX} strokeWidth={0.12} />
        <Chevron x={x2} y={Y(y2)} ang={ang} color={C_MAX} len={0.5} w={0.12} />
        {it.nhan && (
          <Label x={(x1 + x2) / 2} y={Y((y1 + y2) / 2) + 1.25} fill={C_MAX}>
            {it.nhan}
          </Label>
        )}
      </g>
    );
  }
  if (it.loai === "tiet_dien") {
    const cx = it.x,
      cy = Y(it.y);
    return (
      <g className={cls}>
        <circle cx={cx} cy={cy} r={0.5} fill="var(--cc-halo)" stroke="currentColor" strokeWidth={0.1} />
        {it.chieu === "ra" ? (
          <circle cx={cx} cy={cy} r={0.13} fill="currentColor" />
        ) : (
          <path
            d={`M${cx - 0.3} ${cy - 0.3} l0.6 0.6 M${cx + 0.3} ${cy - 0.3} l-0.6 0.6`}
            stroke="currentColor"
            strokeWidth={0.1}
          />
        )}
        {it.ten && (
          <Label x={cx} y={cy - 0.8}>
            {it.ten}
          </Label>
        )}
      </g>
    );
  }
  if (it.loai === "vec") {
    const g = rad(it.goc),
      x2 = it.x + it.dai * Math.cos(g),
      y2 = it.y + it.dai * Math.sin(g),
      c = mau(it.mau ?? "max");
    // nhãn ở mũi: vectơ gần thẳng đứng thì đặt sang bên (phải, hoặc trái nếu `trai`), còn lại đặt phía trên mũi
    const dung = Math.abs(Math.cos(g)) < 0.3,
      s = it.trai ? -1 : 1;
    // vectơ đứng dài ≥ 1,5: nhãn cạnh thân, ngay sau mũi (khỏi đụng trần/sợi chỉ phía trên mũi — HS ảo 3/11)
    const canhThan = dung && it.dai >= 1.5,
      lx = dung ? x2 + s * 0.45 : x2 + 0.6 * Math.cos(g),
      ly = canhThan
        ? y2 + (Math.sin(g) > 0 ? -0.55 : 0.65)
        : dung
          ? y2 + 0.3 * Math.sin(g)
          : y2 + 0.6 * Math.sin(g) + 0.6;
    return (
      <g className={cls}>
        <line
          x1={it.x}
          y1={Y(it.y)}
          x2={x2}
          y2={Y(y2)}
          stroke={c}
          strokeWidth={0.14}
          strokeDasharray={it.dut ? "0.35 0.22" : undefined}
        />
        <Chevron x={x2} y={Y(y2)} ang={-g} color={c} len={0.5} w={0.14} />
        {it.nhan && (
          <Label x={lx} y={Y(ly) + 0.4} fill={c} a={dung ? (s > 0 ? "start" : "end") : "middle"}>
            {it.nhan}
          </Label>
        )}
      </g>
    );
  }
  if (it.loai === "goc") {
    const r = 1.1,
      a1 = rad(it.tu),
      a2 = rad(it.den),
      large = Math.abs(it.den - it.tu) > 180 ? 1 : 0,
      sweep = it.den > it.tu ? 0 : 1;
    const p = (a: number, rr = r) => [it.x + rr * Math.cos(a), Y(it.y + rr * Math.sin(a))];
    const [sx, sy] = p(a1),
      [ex, ey] = p(a2),
      [mx, my] = p((a1 + a2) / 2, r + 1.05);
    return (
      <g className={cls}>
        <path
          d={`M${sx} ${sy} A${r} ${r} 0 ${large} ${sweep} ${ex} ${ey}`}
          stroke={C_MIN}
          strokeWidth={0.08}
          fill="none"
        />
        {it.nhan && (
          <Label x={mx} y={my + 0.4} fill={C_MIN} size={1}>
            {it.nhan}
          </Label>
        )}
      </g>
    );
  }
  if (it.loai === "chu") {
    return (
      <g className={cls}>
        <Label x={it.x} y={Y(it.y)} a={it.a ?? "middle"}>
          {it.text}
        </Label>
      </g>
    );
  }
  if (it.loai === "tran") {
    const n = Math.floor((it.x2 - it.x1) / 0.6);
    return (
      <g className={cls} stroke="currentColor">
        <line x1={it.x1} y1={Y(it.y)} x2={it.x2} y2={Y(it.y)} strokeWidth={0.12} />
        {Array.from({ length: n + 1 }, (_, i) => (
          <line
            key={i}
            x1={it.x1 + i * 0.6}
            y1={Y(it.y)}
            x2={it.x1 + i * 0.6 + 0.4}
            y2={Y(it.y) - 0.4}
            strokeWidth={0.05}
          />
        ))}
      </g>
    );
  }
  if (it.loai === "khung") {
    // hình nhỏ khung ABCD nhìn nghiêng (hình chiếu xiên) trong ô nền halo: A trước-trái, AB đi vào trong hình
    const [dx, dy] = it.sau,
      A = [it.x, it.y],
      B = [it.x + dx, it.y + dy],
      C = [it.x + it.rong + dx, it.y + dy],
      D = [it.x + it.rong, it.y];
    const [tA, tB, tC, tD] = it.ten ?? ["A", "B", "C", "D"];
    const pts = [A, B, C, D].map(([x, y]) => `${x},${Y(y)}`).join(" ");
    const giua = (P: number[], Q: number[]) => [(P[0] + Q[0]) / 2, Y((P[1] + Q[1]) / 2)];
    const [ab1, ab2] = giua(B, A),
      [cd1, cd2] = giua(D, C);
    const x1 = it.x - 1,
      x2 = C[0] + 0.75,
      y1 = it.y - 1.55,
      y2 = it.y + dy + 2;
    return (
      <g className={cls}>
        <rect
          x={x1}
          y={Y(y2)}
          width={x2 - x1}
          height={y2 - y1}
          rx={0.3}
          fill="none"
          stroke="currentColor"
          strokeWidth={0.05}
          opacity={0.6}
        />
        <polygon points={pts} fill="none" stroke="currentColor" strokeWidth={0.12} strokeLinejoin="round" />
        {/* chiều dòng điện: B → A ở cạnh AB (ra phía người nhìn), D → C ở cạnh CD */}
        <Chevron x={ab1} y={ab2} ang={Math.atan2(dy, -dx)} color={C_MAX} len={0.35} w={0.1} />
        <Chevron x={cd1} y={cd2} ang={Math.atan2(-dy, dx)} color={C_MAX} len={0.35} w={0.1} />
        <Label x={A[0] - 0.25} y={Y(A[1]) + 0.35} a="end" size={0.85}>
          {tA}
        </Label>
        <Label x={B[0] - 0.25} y={Y(B[1])} a="end" size={0.85}>
          {tB}
        </Label>
        <Label x={C[0] + 0.2} y={Y(C[1])} a="start" size={0.85}>
          {tC}
        </Label>
        <Label x={D[0] + 0.2} y={Y(D[1]) + 0.35} a="start" size={0.85}>
          {tD}
        </Label>
        {it.B && (
          <g>
            <line x1={B[0] - 0.2} y1={Y(y2 - 0.75)} x2={C[0]} y2={Y(y2 - 0.75)} stroke={C_MIN} strokeWidth={0.08} />
            <Chevron x={C[0]} y={Y(y2 - 0.75)} ang={0} color={C_MIN} len={0.35} w={0.08} />
            <Label x={B[0] - 0.5} y={Y(y2 - 0.75) + 0.3} a="end" size={0.85} fill={C_MIN}>
              B
            </Label>
          </g>
        )}
        {it.nhan && (
          <Label x={(x1 + x2) / 2} y={Y(y1 + 0.4)} size={0.85}>
            {it.nhan}
          </Label>
        )}
      </g>
    );
  }
  if (it.loai === "nam_cham") {
    // như bar_magnet: mặt trước hai nửa, mặt trên và mặt bên dời (dx, dy) lên-phải
    const dx = it.cao * 0.4,
      dy = -it.cao * 0.3,
      x0 = it.x - it.dai / 2,
      x1 = it.x + it.dai / 2,
      y0 = Y(it.y) - it.cao / 2,
      y1 = Y(it.y) + it.cao / 2;
    const [CL, CR] = it.n_trai === false ? [UM_S, UM_N] : [UM_N, UM_S];
    const P = (pts: number[][], f: string) => (
      <polygon
        points={pts.map((q) => q.join(",")).join(" ")}
        fill={f}
        stroke={UM_EDGE}
        strokeWidth={0.08}
        strokeLinejoin="round"
      />
    );
    return (
      <g className={cls}>
        {P(
          [
            [x0, y0],
            [it.x, y0],
            [it.x + dx, y0 + dy],
            [x0 + dx, y0 + dy],
          ],
          CL[1],
        )}
        {P(
          [
            [it.x, y0],
            [x1, y0],
            [x1 + dx, y0 + dy],
            [it.x + dx, y0 + dy],
          ],
          CR[1],
        )}
        {P(
          [
            [x1, y0],
            [x1 + dx, y0 + dy],
            [x1 + dx, y1 + dy],
            [x1, y1],
          ],
          CR[2],
        )}
        <rect x={x0} y={y0} width={it.dai / 2} height={it.cao} fill={CL[0]} stroke={UM_EDGE} strokeWidth={0.08} />
        <rect x={it.x} y={y0} width={it.dai / 2} height={it.cao} fill={CR[0]} stroke={UM_EDGE} strokeWidth={0.08} />
        <text
          x={x0 + it.dai / 4}
          y={Y(it.y) + it.cao * 0.18}
          fontSize={it.cao * 0.5}
          textAnchor="middle"
          fill="#fff"
          fontWeight={800}
        >
          {it.n_trai === false ? "S" : "N"}
        </text>
        <text
          x={x1 - it.dai / 4}
          y={Y(it.y) + it.cao * 0.18}
          fontSize={it.cao * 0.5}
          textAnchor="middle"
          fill="#fff"
          fontWeight={800}
        >
          {it.n_trai === false ? "N" : "S"}
        </text>
      </g>
    );
  }
  return null;
}

export default function TuTruong({ nen, hinh = [], lop, layer: L }: Props) {
  const items = dangHien(lop, L);
  const ghi = ghiMoiNhat(lop, L);
  const ghiY = H + 1.5;
  return (
    <svg
      viewBox={`-0.4 -0.2 ${W + 0.8} ${H + 2.5}`}
      className="cc-fig"
      role="img"
      aria-label="Hình từ trường, dây dẫn và lực từ"
    >
      {nen && <Nen nen={nen} />}
      {hinh.map((it, k) => (it.het != null && L >= it.het ? null : <Muc key={`h${k}`} it={it} moi={false} />))}
      {items.map((it, k) => (
        <Muc key={`l${k}`} it={it} moi />
      ))}
      {ghi.slice(0, 1).map((t, i) => (
        <Label key={`${L}-${i}`} x={W / 2} y={ghiY} size={Math.min(1.05, (W + 0.6) / (t.length * 0.6))}>
          {t}
        </Label>
      ))}
      {/* giữ chỗ dải dưới để hình không đổi cao (D2) */}
      <rect x={0} y={H + 0.3} width={0.01} height={1.8} fill="none" />
    </svg>
  );
}
