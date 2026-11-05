"use client";

/**
 * Họ hình `do_thi` (đợt Đ2 3/11/2026, mẫu đầu: bài 1 Sự chuyển thể L12, dạng 4): đồ thị trên lưới — gấp khúc (đọc số
 * T–t, x–t, v–t, U–I…) hoặc hàm lấy mẫu (cos, mũ, nghịch đảo, đa thức: W–t, N(t), p–V…). Một component cho cả hai vì
 * trục, lưới, chiếu, thước, độ dốc, tô diện tích dùng chung (thầy duyệt 3/11). Không chạy hoạt hình (thầy 2/11).
 * Hình không đổi cao giữa các bước (D2); nhãn trên hình (N8, H3); đường thứ hai nét đứt (H4).
 *
 * JSON: { loai: "do_thi", x: {min, max, ten, vach?, luoi?}, y: {…}, duong: [{diem: [[x,y]…]} | {ham: {kieu…}}],
 *         diem?: [{x, y, ten, vi?}], lop: [[mục…] cho bước 1, …] }. `vach` = số ghi trên trục, chỉ khai số đề cho.
 * Mục: diem {x,y,ten,vi}  ·  duong {duong}  ·  chieu {x,y,nhan_x?,nhan_y?} (nét đứt xuống hai trục)
 *  ·  ngang {y,nhan?,tu?,den?}  ·  dung {x,nhan?}  ·  doan {tu,den,duong?,nhan?,vi?,nhan_xy?} (tô đậm khúc đường theo x)
 *  ·  thuoc {tu,den,y,nhan}  ·  doc {tu:[x,y],den:[x,y],nhan_x?,nhan_y?} (tam giác độ dốc)
 *  ·  dien_tich {tu,den,duong?,nhan?}  ·  chu {x,y,text,a?,mau?} (chữ tự do theo toạ độ đồ thị)  ·  ghi {text}.
 *  `hinh?: [mục…]` = vẽ sẵn theo đề (lớp 0), dùng khi hình đồ thị là hình dưới đề (`de: true`). `het: k` = ẩn từ khi xong bước k.
 */

import { C_HL, C_MAX, C_MIN, Chevron, Label, chiaDong, dangHien, fmt, ghiMoiNhat } from "@/components/lessons/cong-cu/chung";
import type { DoThiDiem, DoThiDuong, DoThiHam, DoThiLop, DoThiTruc, DoThiVi } from "@/features/lessons/types";

type Props = { x: DoThiTruc; y: DoThiTruc; duong?: DoThiDuong[]; diem?: DoThiDiem[]; hinh?: DoThiLop[]; lop?: DoThiLop[][]; layer: number };

// vùng vẽ (đơn vị hình): trái, phải, trên, dưới
const PL = 2.9, PR = 20.6, PT = 1.3, PB = 10.4;
const NHAN = 1.05;

function giaTri(h: DoThiHam, x: number) {
  if (h.kieu === "cos") return (h.c ?? 0) + h.a * Math.cos(h.w * Math.PI * x + (h.phi ?? 0) * Math.PI);
  if (h.kieu === "mu") return (h.c ?? 0) + h.a * Math.pow(2, -x / h.T);
  if (h.kieu === "nghich") return x === 0 ? NaN : h.a / x;
  return h.he.reduce((s, c, i) => s + c * Math.pow(x, i), 0);
}

/** Các điểm số liệu của đường trong khoảng [tu, den] theo x. */
function mau(d: DoThiDuong, ax: DoThiTruc, tu?: number, den?: number): [number, number][] {
  const a = Math.max(tu ?? -Infinity, d.tu ?? ax.min), b = Math.min(den ?? Infinity, d.den ?? ax.max);
  if (d.ham) {
    const n = 220;
    return Array.from({ length: n + 1 }, (_, i) => {
      const x = a + ((b - a) * i) / n;
      return [x, giaTri(d.ham!, x)] as [number, number];
    });
  }
  const p = d.diem ?? [];
  const out: [number, number][] = [];
  const yAt = (x: number) => {
    for (let i = 0; i + 1 < p.length; i++) {
      const [x1, y1] = p[i], [x2, y2] = p[i + 1];
      if (x >= Math.min(x1, x2) - 1e-9 && x <= Math.max(x1, x2) + 1e-9) return x2 === x1 ? y1 : y1 + ((y2 - y1) * (x - x1)) / (x2 - x1);
    }
    return NaN;
  };
  if (tu == null && den == null) return p;
  out.push([a, yAt(a)]);
  for (const q of p) if (q[0] > a && q[0] < b) out.push(q);
  out.push([b, yAt(b)]);
  return out;
}

const VI: Record<DoThiVi, [number, number, "start" | "middle" | "end"]> = {
  t: [0, -0.55, "middle"],
  b: [0, 1.45, "middle"],
  l: [-0.5, 0.4, "end"],
  r: [0.5, 0.4, "start"],
  tl: [-0.35, -0.45, "end"],
  tr: [0.35, -0.45, "start"],
  bl: [-0.35, 1.35, "end"],
  br: [0.35, 1.35, "start"],
};

export default function DoThi({ x: ax, y: ay, duong = [], diem = [], hinh = [], lop, layer: L }: Props) {
  // `hinh` = mục vẽ sẵn theo đề (lớp 0, "một dạng — một hình" 5/11/2026), cùng cú pháp mục của `lop`
  const items = [...hinh.filter((h) => h.het == null || L < h.het), ...dangHien(lop, L)];
  const ghi = ghiMoiNhat(lop, L);
  const X = (v: number) => PL + ((v - ax.min) / (ax.max - ax.min)) * (PR - PL);
  const Y = (v: number) => PB - ((v - ay.min) / (ay.max - ay.min)) * (PB - PT);
  const allDuong = [...duong, ...items.flatMap((it) => (it.loai === "duong" ? [it.duong] : []))];
  const path = (pts: [number, number][]) => {
    let d = "", pen = false;
    for (const [px, py] of pts) {
      if (!Number.isFinite(py) || py < ay.min - (ay.max - ay.min) * 0.02 || py > ay.max + (ay.max - ay.min) * 0.02) {
        pen = false;
        continue;
      }
      d += `${pen ? "L" : "M"}${X(px).toFixed(3)} ${Y(py).toFixed(3)} `;
      pen = true;
    }
    return d;
  };
  const mauNet = (m?: string) => (m === "max" ? C_MAX : m === "min" ? C_MIN : "currentColor");
  const luoi = (t: DoThiTruc) => {
    if (!t.luoi) return [];
    const out: number[] = [];
    for (let v = Math.ceil(t.min / t.luoi) * t.luoi; v <= t.max + 1e-9; v += t.luoi) out.push(+v.toFixed(6));
    return out;
  };
  const gocO = ax.min === 0 && ay.min === 0;
  // số trên trục do bước thêm (chiếu, ngang, dung): số in sẵn quá gần thì ẩn cho khỏi chồng chữ
  const soY = items.flatMap((it) => ((it.loai === "chieu" && it.nhan_y) || (it.loai === "ngang" && it.nhan) ? [Y(it.y)] : []));
  const soX = items.flatMap((it) => ((it.loai === "chieu" && it.nhan_x) || (it.loai === "dung" && it.nhan) ? [X(it.x)] : []));
  const gan = (v: number, ds: number[], d: number) => ds.some((u) => Math.abs(u - v) < d && Math.abs(u - v) > 1e-6);
  // xét nhãn chiếu của MỌI bước để tên trục không nhảy chỗ giữa các bước (D2)
  const soXMoi = (lop ?? []).flat().flatMap((it) => ((it.loai === "chieu" && it.nhan_x) || (it.loai === "dung" && it.nhan) ? [X(it.x)] : []));
  const tenTrai = PR + 1.1 - ax.ten.length * 0.6 * 0.95;
  const tenDuoi = [...(ax.vach ?? []).map((v) => X(v) + fmt(v, 3).length * 0.3 * 0.95), ...soXMoi.map((v) => v + 1.3)].every(
    (e) => e + 0.3 < tenTrai,
  );
  const ghiY = PB + 2.85;
  const bot = ghiY + 1.35 * 1 + 0.6;

  return (
    <svg viewBox={`0 0 ${PR + 1.2} ${bot}`} className="cc-fig" role="img" aria-label={`Đồ thị ${ay.ten} theo ${ax.ten}`}>
      {/* lưới mờ */}
      <g stroke="currentColor" strokeWidth={0.03} opacity={0.22}>
        {luoi(ax).map((v) => (
          <line key={`gx${v}`} x1={X(v)} y1={PT} x2={X(v)} y2={PB} />
        ))}
        {luoi(ay).map((v) => (
          <line key={`gy${v}`} x1={PL} y1={Y(v)} x2={PR} y2={Y(v)} />
        ))}
      </g>
      {/* trục */}
      <line x1={PL} y1={PB} x2={PR + 0.7} y2={PB} stroke="currentColor" strokeWidth={0.08} />
      <Chevron x={PR + 0.7} y={PB} ang={0} len={0.45} w={0.08} />
      <line x1={PL} y1={PB} x2={PL} y2={PT - 0.9} stroke="currentColor" strokeWidth={0.08} />
      <Chevron x={PL} y={PT - 0.9} ang={-Math.PI / 2} len={0.45} w={0.08} />
      {ay.min !== 0 && (
        // trục dọc không bắt đầu từ 0: dấu gãy trục
        <path d={`M${PL - 0.3} ${PB - 0.35} l0.6 -0.25 M${PL - 0.3} ${PB - 0.6} l0.6 -0.25`} stroke="currentColor" strokeWidth={0.07} />
      )}
      {/* tên trục ngang: dưới trục nếu không đụng số vạch/nhãn chiếu, để khỏi đè đường cong sát trục (HS ảo 3/11) */}
      <Label x={PR + 1.1} y={tenDuoi ? PB + 1.15 : PB - 0.45} a="end" size={0.95}>
        {ax.ten}
      </Label>
      <Label x={PL + 0.4} y={PT - 0.35} a="start" size={0.95}>
        {ay.ten}
      </Label>
      {gocO && (
        <Label x={PL - 0.35} y={PB + 1.05} a="end" size={0.95}>
          O
        </Label>
      )}
      {(ax.vach ?? []).map((v) =>
        (gocO && v === 0) || gan(X(v), soX, 1.6) ? null : (
          <g key={`vx${v}`}>
            <line x1={X(v)} y1={PB} x2={X(v)} y2={PB + 0.25} stroke="currentColor" strokeWidth={0.06} />
            <Label x={X(v)} y={PB + 1.15} size={0.95}>
              {fmt(v, 3)}
            </Label>
          </g>
        ),
      )}
      {(ay.vach ?? []).map((v) =>
        (gocO && v === 0) || gan(Y(v), soY, 0.95) ? null : (
          <g key={`vy${v}`}>
            <line x1={PL - 0.25} y1={Y(v)} x2={PL} y2={Y(v)} stroke="currentColor" strokeWidth={0.06} />
            <Label x={PL - 0.35} y={Y(v) + 0.35} a="end" size={0.95}>
              {fmt(v, 3)}
            </Label>
          </g>
        ),
      )}
      {/* diện tích (dưới đường) — vẽ trước đường */}
      {items.map((it, k) => {
        if (it.loai !== "dien_tich") return null;
        const d = allDuong[it.duong ?? 0];
        if (!d) return null;
        const pts = mau(d, ax, it.tu, it.den).filter((p) => Number.isFinite(p[1]));
        const base = Y(Math.max(ay.min, Math.min(0, ay.max)));
        const poly = [`${X(it.tu)} ${base}`, ...pts.map(([px, py]) => `${X(px).toFixed(3)} ${Y(py).toFixed(3)}`), `${X(it.den)} ${base}`].join(" L");
        const mid = pts[Math.floor(pts.length / 2)];
        return (
          <g key={`dt${k}`} className="cc-in">
            <path d={"M" + poly + " Z"} fill={C_HL} opacity={0.35} />
            {it.nhan && mid && (
              <Label x={X(mid[0])} y={(Y(mid[1]) + base) / 2 + 0.4} size={NHAN}>
                {it.nhan}
              </Label>
            )}
          </g>
        );
      })}
      {/* các đường */}
      {allDuong.map((d, i) => (
        <g key={`d${i}`}>
          <path
            d={path(mau(d, ax))}
            stroke={mauNet(d.mau)}
            strokeWidth={0.13}
            fill="none"
            strokeLinejoin="round"
            strokeDasharray={d.mau === "min" ? "0.45 0.25" : undefined}
          />
          {d.ten && d.ten_xy && (
            <Label x={X(d.ten_xy[0])} y={Y(d.ten_xy[1])} size={NHAN} fill={mauNet(d.mau)}>
              {d.ten}
            </Label>
          )}
        </g>
      ))}
      {/* mục theo bước (trừ điểm — điểm vẽ sau cùng cho nổi) */}
      {items.map((it, k) => {
        if (it.loai === "chu") {
          return (
            <Label key={k} x={X(it.x)} y={Y(it.y)} a={it.a ?? "middle"} size={0.95} fill={mauNet(it.mau)}>
              {it.text}
            </Label>
          );
        }
        if (it.loai === "doan") {
          const d = allDuong[it.duong ?? 0];
          if (!d) return null;
          const pts = mau(d, ax, it.tu, it.den);
          const mid = pts.reduce((s, p) => [s[0] + p[0] / pts.length, s[1] + p[1] / pts.length], [0, 0]);
          return (
            <g key={k} className="cc-in">
              <path d={path(pts)} stroke={C_MAX} strokeWidth={0.34} fill="none" strokeLinecap="round" opacity={0.85} />
              {it.nhan && (
                <Label
                  x={it.nhan_xy ? X(it.nhan_xy[0]) : X(mid[0])}
                  y={it.nhan_xy ? Y(it.nhan_xy[1]) : Y(mid[1]) + (it.vi === "b" ? 1.35 : -0.55)}
                  size={NHAN}
                  fill={C_MAX}
                >
                  {it.nhan}
                </Label>
              )}
            </g>
          );
        }
        if (it.loai === "chieu") {
          return (
            <g key={k} className="cc-in">
              <path d={`M${PL} ${Y(it.y)} H${X(it.x)} V${PB}`} stroke={C_MIN} strokeWidth={0.07} fill="none" strokeDasharray="0.3 0.2" />
              {it.nhan_y && (
                <Label x={PL - 0.35} y={Y(it.y) + 0.35} a="end" size={0.95} fill={C_MIN}>
                  {it.nhan_y}
                </Label>
              )}
              {it.nhan_x && (
                <Label x={X(it.x)} y={PB + 1.15} size={0.95} fill={C_MIN}>
                  {it.nhan_x}
                </Label>
              )}
            </g>
          );
        }
        if (it.loai === "ngang") {
          const x1 = X(it.tu ?? ax.min), x2 = X(it.den ?? ax.max);
          return (
            <g key={k} className="cc-in">
              <line x1={x1} y1={Y(it.y)} x2={x2} y2={Y(it.y)} stroke={C_MIN} strokeWidth={0.07} strokeDasharray="0.3 0.2" />
              {it.nhan && (
                <Label x={PL - 0.35} y={Y(it.y) + 0.35} a="end" size={0.95} fill={C_MIN}>
                  {it.nhan}
                </Label>
              )}
            </g>
          );
        }
        if (it.loai === "dung") {
          return (
            <g key={k} className="cc-in">
              <line x1={X(it.x)} y1={PT} x2={X(it.x)} y2={PB} stroke={C_MIN} strokeWidth={0.07} strokeDasharray="0.3 0.2" />
              {it.nhan && (
                <Label x={X(it.x)} y={PB + 1.15} size={0.95} fill={C_MIN}>
                  {it.nhan}
                </Label>
              )}
            </g>
          );
        }
        if (it.loai === "thuoc") {
          const x1 = X(it.tu), x2 = X(it.den), y = Y(it.y);
          return (
            <g key={k} className="cc-in">
              <line x1={x1} y1={y} x2={x2} y2={y} stroke={C_MAX} strokeWidth={0.09} />
              <Chevron x={x1} y={y} ang={Math.PI} color={C_MAX} w={0.09} len={0.4} />
              <Chevron x={x2} y={y} ang={0} color={C_MAX} w={0.09} len={0.4} />
              <Label x={(x1 + x2) / 2} y={y - 0.4} size={NHAN} fill={C_MAX}>
                {it.nhan}
              </Label>
            </g>
          );
        }
        if (it.loai === "doc") {
          const [x1, y1] = it.tu, [x2, y2] = it.den;
          return (
            <g key={k} className="cc-in">
              <path d={`M${X(x1)} ${Y(y1)} H${X(x2)} V${Y(y2)}`} stroke={C_MAX} strokeWidth={0.09} fill="none" />
              {it.nhan_x && (
                <Label x={(X(x1) + X(x2)) / 2} y={Y(y1) + 1.3} size={NHAN} fill={C_MAX}>
                  {it.nhan_x}
                </Label>
              )}
              {it.nhan_y && (
                <Label x={X(x2) + 0.35} y={(Y(y1) + Y(y2)) / 2 + 0.4} a="start" size={NHAN} fill={C_MAX}>
                  {it.nhan_y}
                </Label>
              )}
            </g>
          );
        }
        return null;
      })}
      {/* điểm: theo đề + theo bước */}
      {[...diem, ...items.flatMap((it) => (it.loai === "diem" ? [it] : []))].map((p, k) => {
        const [dx, dy, a] = VI[p.vi ?? "tl"];
        return (
          <g key={`p${k}`} className={k >= diem.length ? "cc-in" : undefined}>
            <circle cx={X(p.x)} cy={Y(p.y)} r={0.22} fill={k >= diem.length ? C_HL : "currentColor"} stroke="currentColor" strokeWidth={0.06} />
            {p.ten && (
              <Label x={X(p.x) + dx} y={Y(p.y) + dy} a={a} size={NHAN}>
                {p.ten}
              </Label>
            )}
          </g>
        );
      })}
      {ghi.slice(0, 1).flatMap((t) => {
        // ghi dài: hai dòng thay vì thu chữ (≥ 10px ở 375 — HS ảo 3/11); dải dưới đủ chỗ hai dòng nên hình không đổi cao
        const ds = chiaDong(t, PR + 0.6, NHAN),
          y0 = ds.length > 1 ? ghiY - 0.35 : ghiY;
        return ds.map((d, i) => (
          <Label key={`${L}-${i}`} x={(PL + PR) / 2} y={y0 + i * 1.4} size={Math.min(NHAN, (PR + 0.6) / (d.length * 0.6))}>
            {d}
          </Label>
        ));
      })}
    </svg>
  );
}
