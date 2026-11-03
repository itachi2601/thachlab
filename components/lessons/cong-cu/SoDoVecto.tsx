"use client";

/**
 * 🧪 Họ hình `so_do_vecto` (3/11/2026, mẫu bài 18 Lực ma sát dạng 4): vectơ đồng quy trên một cảnh đơn giản.
 * Thầy chốt 3/11: MỘT component — cảnh vẽ bằng code (mặt ngang, mặt nghiêng, nút dây, ròng rọc, bàn + ròng rọc, không nền),
 * còn vectơ khai trong JSON ({ten, goc, do_lon, buoc, kieu}) nên dạng sau chỉ khai dữ liệu, không viết code.
 *
 * `layer` = số bước đã xong: vectơ có `buoc = i` chỉ vẽ khi em đã làm xong bước i (không lộ đáp số bước đang hỏi).
 * Độ lớn của vectơ đã biết nằm ở "bảng số" góc hình (nhãn trên mũi tên chỉ có tên → không chồng chữ).
 * viewBox tính từ MỌI lớp nên hình không đổi cao giữa các bước (nút ◀ ▶ đứng yên).
 * Quy tắc: N8 + H3 (nhãn trên hình), H4 (nét 2–3 màu, thành phần nét đứt — không chỉ dựa vào màu), N5 (lớp theo bước), B4 (không chạy).
 */

import type { ReactNode } from "react";
import type { SoDoVectoTool, VecDir, VecPoint } from "@/features/lessons/types";

type P = [number, number];
const MAU: Record<string, string> = { muc: "currentColor", cam: "#c2410c", lam: "#0e7490", tim: "#7c3aed" };
const FS = 1.15; // cỡ chữ (đơn vị hình) — cảnh rộng ~20 đơn vị nên ở 375px ≈ 14px (H4 ≥ 13px)
const rad = (d: number) => (d * Math.PI) / 180;
const dirv = (d: number): P => [Math.cos(rad(d)), Math.sin(rad(d))];
const add = (a: P, b: P, k = 1): P => [a[0] + k * b[0], a[1] + k * b[1]];
const sv = (p: P) => `${p[0].toFixed(3)} ${(-p[1]).toFixed(3)}`; // toán (y lên) → SVG (y xuống)

/** "F_ms" → F + chỉ số dưới; "m_1" → m₁ (tspan). */
function Sub({ s }: { s: string }) {
  const parts = s.split(/_(\w+|\{[^}]*\})/);
  return (
    <>
      {parts.map((p, i) =>
        i % 2 ? (
          <tspan key={i} dy={0.32} fontSize="0.72em">
            {p.replace(/[{}]/g, "")}
            <tspan dy={-0.32}>{"​"}</tspan>
          </tspan>
        ) : (
          <tspan key={i}>{p}</tspan>
        ),
      )}
    </>
  );
}
const textLen = (s: string) => s.replace(/_(\w+|\{[^}]*\})/g, (_, x: string) => x.replace(/[{}]/g, "").slice(0, Math.ceil(x.length * 0.75))).length;

function Label({ p, children, fill = "currentColor", a = "middle", size = FS, rot }: { p: P; children: ReactNode; fill?: string; a?: "start" | "middle" | "end"; size?: number; rot?: number }) {
  return (
    <text
      x={p[0]}
      y={-p[1]}
      fontSize={size}
      textAnchor={a}
      dominantBaseline="central"
      fill={fill}
      fontWeight={600}
      stroke="var(--cc-halo)"
      strokeWidth={0.3}
      paintOrder="stroke"
      transform={rot ? `rotate(${rot} ${p[0]} ${-p[1]})` : undefined}
    >
      {children}
    </text>
  );
}

/** Gạch chéo phía "cứng" của tường/trần/mặt sàn: đoạn a→b, gạch về phía `side` (vectơ đơn vị). */
function Hatch({ a, b, side }: { a: P; b: P; side: P }) {
  const L = Math.hypot(b[0] - a[0], b[1] - a[1]), n = Math.max(2, Math.floor(L / 0.7));
  const u: P = [(b[0] - a[0]) / L, (b[1] - a[1]) / L];
  const t: P = [side[0] * 0.5 - u[0] * 0.35, side[1] * 0.5 - u[1] * 0.35];
  let d = `M${sv(a)} L${sv(b)}`;
  for (let i = 0; i <= n; i++) {
    const p = add(a, u, (i * L) / n);
    d += ` M${sv(p)} L${sv(add(p, t))}`;
  }
  return <path d={d} stroke="currentColor" strokeWidth={0.08} fill="none" opacity={0.8} />;
}

function Block({ c, w, h, rot = 0, text, tx = 0 }: { c: P; w: number; h: number; rot?: number; text?: string; tx?: number }) {
  const u = dirv(rot), n = dirv(rot + 90);
  const pts = [add(add(c, u, -w / 2), n, -h / 2), add(add(c, u, w / 2), n, -h / 2), add(add(c, u, w / 2), n, h / 2), add(add(c, u, -w / 2), n, h / 2)];
  return (
    <g>
      <path d={"M" + pts.map(sv).join(" L") + " Z"} fill="var(--cc-halo)" stroke="currentColor" strokeWidth={0.12} />
      {text && (
        <Label p={add(c, u, tx)} size={0.95} rot={-rot}>
          <Sub s={text} />
        </Label>
      )}
    </g>
  );
}

/** `can`: điểm mẫu trên nét cảnh để bảng số "trong" tránh đè. */
type Scene = { el: ReactNode; pts: Record<string, P>; box: [number, number, number, number]; doc?: number; day?: Record<string, number>; can?: P[] };

function scene(nen: SoDoVectoTool["nen"]): Scene {
  if (nen.kieu === "mat_nghieng") {
    const al = nen.alpha, S = 17, s = -al; // s: hướng xuống dốc (dốc cao bên trái)
    const B: P = [(S * Math.cos(rad(al))) / 2, 0], T: P = [-(S * Math.cos(rad(al))) / 2, S * Math.sin(rad(al))];
    const down = dirv(s), nrm = dirv(s + 90);
    const bw = 3, bh = 1.9, t = nen.vat_t ?? 0.3;
    const foot = add(T, down, t * S + bw / 2), c = add(foot, nrm, bh / 2);
    const arc = 2.2, a0 = 180 - al;
    const arcP = (d: number): P => add(B, dirv(d), arc);
    return {
      el: (
        <g>
          <path d={`M${sv(T)} L${sv(B)} L${sv([T[0], 0])} Z`} fill="currentColor" fillOpacity={0.06} stroke="currentColor" strokeWidth={0.12} />
          <Hatch a={[T[0] - 1, 0]} b={[B[0] + 2.5, 0]} side={[0, -1]} />
          <path d={`M${sv(arcP(180))} A${arc} ${arc} 0 0 1 ${sv(arcP(a0))}`} fill="none" stroke="currentColor" strokeWidth={0.08} />
          <Label p={add(B, dirv(180 - al / 2), arc + 1.5)}>{`${String(al).replace(".", ",")}°`}</Label>
          {nen.dai && (
            <Label p={add(add(T, down, S * 0.84), nrm, 0.9)} size={1} rot={al}>
              <Sub s={nen.dai} />
            </Label>
          )}
          <Block c={c} w={bw} h={bh} rot={s} text={nen.vat} tx={-bw / 4 - 0.1} /> {/* chữ lệch nửa trên dốc: P vẽ từ tâm không cắt chữ */}
        </g>
      ),
      pts: { vat: c, vat_day: foot, dinh: add(T, nrm, 0.25), chan: add(B, nrm, 0.25) },
      box: [T[0] - 1, -0.6, B[0] + 2.5, T[1] + 0.5],
      doc: s,
      can: Array.from({ length: 21 }, (_, i) => add(T, down, (i * S) / 20)).concat([add(c, nrm, bh / 2 + 0.2), add(add(c, nrm, bh / 2), down, bw / 2)]),
    };
  }
  if (nen.kieu === "mat_ngang") {
    const x = nen.vat_x ?? 0, c: P = [x, 1];
    return {
      el: (
        <g>
          <Hatch a={[-9, 0]} b={[9, 0]} side={[0, -1]} />
          <Block c={c} w={3} h={2} text={nen.vat} />
        </g>
      ),
      pts: { vat: c, vat_day: [x, 0] },
      box: [-9, -0.6, 9, 2],
    };
  }
  if (nen.kieu === "nut") {
    const O: P = [0, 0], pts: Record<string, P> = { O }, day: Record<string, number> = {};
    const els: ReactNode[] = [];
    let box: [number, number, number, number] = [-1, -1, 1, 1];
    const grow = (p: P, m = 0) => (box = [Math.min(box[0], p[0] - m), Math.min(box[1], p[1] - m), Math.max(box[2], p[0] + m), Math.max(box[3], p[1] + m)]);
    nen.day.forEach((d, i) => {
      const u = dirv(d.goc), E = add(O, u, d.dai);
      if (d.ten) {
        pts[d.ten] = E;
        day[d.ten] = d.goc;
      }
      els.push(<line key={`d${i}`} x1={0} y1={0} x2={E[0]} y2={-E[1]} stroke="currentColor" strokeWidth={0.1} />);
      grow(E, 0.6);
      if (d.neo === "tuong") els.push(<Hatch key={`h${i}`} a={add(E, [0, -1.4])} b={add(E, [0, 1.4])} side={[Math.sign(u[0]) || 1, 0]} />);
      if (d.neo === "tran") els.push(<Hatch key={`h${i}`} a={add(E, [-1.4, 0])} b={add(E, [1.4, 0])} side={[0, Math.sign(u[1]) || 1]} />);
      if (d.neo === "cot") {
        els.push(<line key={`c${i}`} x1={E[0]} y1={-E[1] + 0.2} x2={E[0]} y2={-E[1] + 3.2} stroke="currentColor" strokeWidth={0.22} />);
        grow(add(E, [0, -3.2]));
      }
      if (d.neo === "vat") {
        const c = add(E, [0, -0.7]);
        pts.vat = c;
        els.push(<Block key={`v${i}`} c={c} w={2} h={1.4} text={d.vat} />);
        grow(add(c, [0, -0.7]), 1);
      }
      if (d.ten && d.neo !== "vat") els.push(<Label key={`t${i}`} p={add(E, u, 0.9)}>{d.ten}</Label>);
    });
    els.push(<circle key="O" cx={0} cy={0} r={0.22} fill="var(--cc-halo)" stroke="currentColor" strokeWidth={0.1} />);
    return { el: <g>{els}</g>, pts, box, day };
  }
  if (nen.kieu === "rong_roc") {
    const r = 1.6, dy = nen.lech ?? 0, y1 = -5.5 - dy / 2, y2 = -5.5 + dy / 2;
    const c1: P = [-r, y1 - 0.8], c2: P = [r, y2 - 0.8];
    return {
      el: (
        <g>
          <Hatch a={[-3, 2.6]} b={[3, 2.6]} side={[0, 1]} />
          <line x1={0} y1={-2.6} x2={0} y2={0} stroke="currentColor" strokeWidth={0.1} />
          <circle cx={0} cy={0} r={r} fill="none" stroke="currentColor" strokeWidth={0.12} />
          <circle cx={0} cy={0} r={0.15} fill="currentColor" />
          <line x1={-r} y1={0} x2={-r} y2={-y1} stroke="currentColor" strokeWidth={0.1} />
          <line x1={r} y1={0} x2={r} y2={-y2} stroke="currentColor" strokeWidth={0.1} />
          <Block c={c1} w={2.2} h={1.6} text={nen.vat1 ?? "m_1"} />
          <Block c={c2} w={2.2} h={1.6} text={nen.vat2 ?? "m_2"} />
        </g>
      ),
      pts: { m1: c1, m2: c2, rr: [0, 0] },
      box: [-4, Math.min(y1, y2) - 1.6, 4, 2.6],
    };
  }
  if (nen.kieu === "ban_rong_roc") {
    const A: P = [-3.5, 0.8], rc: P = [3.6, 0.1], r = 0.7, B: P = [rc[0] + r, -4.8];
    return {
      el: (
        <g>
          <Hatch a={[-9, 0]} b={[3, 0]} side={[0, -1]} />
          <line x1={3} y1={0} x2={3} y2={6} stroke="currentColor" strokeWidth={0.1} />
          <line x1={3} y1={0} x2={rc[0]} y2={-rc[1]} stroke="currentColor" strokeWidth={0.1} />
          <circle cx={rc[0]} cy={-rc[1]} r={r} fill="var(--cc-halo)" stroke="currentColor" strokeWidth={0.12} />
          <line x1={A[0] + 1.2} y1={-0.8} x2={rc[0]} y2={-0.8} stroke="currentColor" strokeWidth={0.1} />
          <line x1={B[0]} y1={-rc[1]} x2={B[0]} y2={-(B[1] + 0.8)} stroke="currentColor" strokeWidth={0.1} />
          <Block c={A} w={2.4} h={1.6} text={nen.vat1 ?? "A"} />
          <Block c={B} w={1.8} h={1.6} text={nen.vat2 ?? "B"} />
        </g>
      ),
      pts: { A, B, A_day: [A[0], 0] },
      box: [-9, -6, 5.5, 1.6],
    };
  }
  return { el: null, pts: { O: [0, 0] }, box: [-1, -1, 1, 1] };
}

export default function SoDoVecto({ nen, vec, hbh = [], truc, goc = [], bang = [], bang_vi_tri, ti_le, layer: L }: SoDoVectoTool & { layer: number }) {
  const sc = scene(nen);
  const pt = (p: VecPoint | undefined): P => (Array.isArray(p) ? p : sc.pts[p ?? Object.keys(sc.pts)[0]] ?? [0, 0]);
  const dir = (d: VecDir): number => {
    if (typeof d === "number") return d;
    const s = sc.doc ?? -90;
    const named: Record<string, number> = { phai: 0, len: 90, trai: 180, xuong: -90, doc_xuong: s, doc_len: s + 180, phap_tuyen: s + 90, vao_doc: s - 90 };
    if (d in named) return named[d];
    if (d.startsWith("day:")) return sc.day?.[d.slice(4)] ?? 0;
    return 0;
  };
  const show = (b?: number, den?: number) => L >= (b ?? 0) && (den === undefined || L < den);

  // tỉ lệ độ dài: cùng kiểu đại lượng thì cùng tỉ lệ (lực với lực, a với a…)
  const nhom = (k?: string) => (k === "dong_hoc" ? "dh" : "luc");
  const maxBy: Record<string, number> = {};
  vec.forEach((v) => (maxBy[nhom(v.kieu)] = Math.max(maxBy[nhom(v.kieu)] ?? 0, Math.abs(v.do_lon))));
  // a, v khác đơn vị với lực và với nhau → độ dài cố định (chỉ chỉ hướng), lực thì theo tỉ lệ độ lớn
  const len = (v: (typeof vec)[number]) => (v.kieu === "dong_hoc" ? 3 : Math.max(1.6, (Math.abs(v.do_lon) / (maxBy[nhom(v.kieu)] || 1)) * (ti_le ?? 5)));

  const geo = vec.map((v) => {
    const d = dir(v.goc), o = add(pt(v.tu), v.lech ?? [0, 0]), u = dirv(d), e = add(o, u, len(v));
    const c = Math.cos(rad(d)), s = Math.sin(rad(d));
    const lp = add(add(e, u, 0.75), v.nhan_lech ?? [0, 0]);
    const a: "start" | "middle" | "end" = v.nhan_lech ? "middle" : c > 0.35 ? "start" : c < -0.35 ? "end" : "middle";
    const lpp: P = v.nhan_lech ? lp : [lp[0] - (a === "start" ? 0.15 : a === "end" ? -0.15 : 0), lp[1] + (Math.abs(c) <= 0.35 ? (s > 0 ? 0.2 : -0.2) : 0)];
    return { v, d, o, e, u, lp: lpp, a };
  });
  const byName = (n: string) => geo.find((g) => g.v.ten === n);

  // khung hình: cảnh + mọi vectơ + nhãn ở MỌI lớp (không đổi cao giữa các bước)
  let [x0, y0, x1, y1] = sc.box;
  const obs: P[] = [...(sc.can ?? [])];
  const grow = (p: P, wx = 0.4, wy = 0.4) => {
    obs.push([p[0] + wx, p[1] + wy], [p[0] + wx, p[1] - wy], [p[0] - wx, p[1]]);
    x0 = Math.min(x0, p[0] - wx);
    x1 = Math.max(x1, p[0] + wx);
    y0 = Math.min(y0, p[1] - wy);
    y1 = Math.max(y1, p[1] + wy);
  };
  geo.forEach((g) => {
    for (let k = 1; k < 8; k++) obs.push(add(g.o, [g.e[0] - g.o[0], g.e[1] - g.o[1]], k / 8));
    grow(g.o);
    grow(g.e);
    const w = textLen(g.v.ten) * FS * 0.62;
    grow([g.lp[0] + (g.a === "start" ? w / 2 : g.a === "end" ? -w / 2 : 0), g.lp[1]], w / 2 + 0.2, FS * 0.7);
  });
  if (truc) {
    const o = pt(truc.tai), ex = dirv(truc.goc), ey = dirv(truc.goc + 90), R = truc.dai ?? 6.5;
    [add(o, ex, R + 0.8), add(o, ey, R + 0.8), add(o, ex, -R * 0.45), add(o, ey, -R * 0.45)].forEach((p) => grow(p, 0.7, 0.7));
  }
  goc.forEach((g) => {
    const m = (dir(g.tu) + dir(g.den)) / 2;
    grow(add(pt(g.tai), dirv(m), (g.r ?? 1.6) + 1.4), 1.2, 0.8);
  });
  // bảng số: mọi dòng ở mọi lớp để giữ chỗ
  const rows = [
    ...geo.filter((g) => g.v.so).map((g) => ({ text: `${g.v.ten} = ${g.v.so}`, fill: MAU[g.v.mau ?? "muc"], b: g.v.so_buoc ?? g.v.buoc ?? 0, den: undefined as number | undefined })),
    ...bang.map((r) => ({ text: r.text, fill: MAU[r.mau ?? "muc"], b: r.buoc ?? 0, den: r.den })),
  ];
  const bw = rows.length ? Math.max(...rows.map((r) => textLen(r.text))) * FS * 0.6 + 1 : 0;
  const lh = FS * 1.45;
  const bh = rows.length * lh;
  if (y1 - y0 < bh + 0.6) y0 = y1 - bh - 0.6;
  // "trong": góc trên phải của khung (mặt nghiêng để trống góc đó) — không nới bề ngang, hình to hơn ở 375px
  const vt = bang_vi_tri ?? (nen.kieu === "mat_nghieng" ? "trong" : "phai");
  // "trong": dời sang phải cho tới khi không đè nét/nhãn nào trong dải cao của bảng
  const band = obs.filter((p) => p[1] >= y1 - bh - 0.5 && p[1] <= y1 + 0.5);
  const bx = vt === "trai" ? x0 - bw : vt === "trong" ? Math.max(x1 - bw, ...band.map((p) => p[0] + 0.5)) : x1 + 0.6;
  if (vt === "trong") x1 = Math.max(x1, bx + bw);
  if (vt === "trai") x0 -= bw;
  else if (vt === "phai") x1 += bw + 0.6;
  x0 -= 0.3;
  x1 += 0.3;
  y0 -= 0.3;
  y1 += 0.3;

  const sw = (k?: string) => (k === "thanh_phan" ? 0.12 : 0.17);
  return (
    <svg viewBox={`${x0} ${-y1} ${x1 - x0} ${y1 - y0}`} className="cc-fig" role="img" aria-label={vec.map((v) => v.ten).join(", ")}>
      {sc.el}
      {truc && show(truc.buoc, truc.den) && (
        <g className="cc-in" opacity={0.7}>
          {[0, 90].map((k, i) => {
            const o = pt(truc.tai), R = truc.dai ?? 6.5, u = dirv(truc.goc + k);
            const a = add(o, u, -R * 0.45), b = add(o, u, R);
            return (
              <g key={k}>
                <line x1={a[0]} y1={-a[1]} x2={b[0]} y2={-b[1]} stroke="currentColor" strokeWidth={0.06} strokeDasharray="0.15 0.2" />
                <path d={`M${sv(add(b, dirv(truc.goc + k + 150), 0.45))} L${sv(b)} L${sv(add(b, dirv(truc.goc + k - 150), 0.45))}`} stroke="currentColor" strokeWidth={0.06} fill="none" />
                <Label p={add(b, u, 0.6)} size={1}>
                  {(truc.ten ?? ["x", "y"])[i]}
                </Label>
              </g>
            );
          })}
        </g>
      )}
      {hbh.map(
        (h, i) =>
          show(h.buoc, h.den) &&
          byName(h.vec) && (
            <g key={`h${i}`} className="cc-in">
              {h.thanh.map((t) => {
                const a = byName(h.vec)!.e, b = byName(t)?.e;
                return b ? <line key={t} x1={a[0]} y1={-a[1]} x2={b[0]} y2={-b[1]} stroke="currentColor" strokeWidth={0.06} strokeDasharray="0.12 0.18" opacity={0.8} /> : null;
              })}
            </g>
          ),
      )}
      {goc.map((g, i) => {
        if (!show(g.buoc, g.an)) return null;
        const o = pt(g.tai), r = g.r ?? 1.6, a = dir(g.tu), b = dir(g.den);
        const p0 = add(o, dirv(a), r), p1 = add(o, dirv(b), r), sweep = ((b - a + 360) % 360) < 180 ? 0 : 1;
        return (
          <g key={`g${i}`} className="cc-in">
            <path d={`M${sv(p0)} A${r} ${r} 0 0 ${sweep} ${sv(p1)}`} fill="none" stroke={MAU[g.mau ?? "muc"]} strokeWidth={0.08} />
            {g.text && (
              <Label p={add(o, dirv((a + b) / 2 + (Math.abs(b - a) > 180 ? 180 : 0)), r + 0.9)} fill={MAU[g.mau ?? "muc"]} size={1}>
                <Sub s={g.text} />
              </Label>
            )}
          </g>
        );
      })}
      {geo.map(({ v, o, e, d, lp, a }, i) => {
        if (!show(v.buoc, v.den)) return null;
        const col = MAU[v.mau ?? (v.kieu === "dong_hoc" ? "lam" : "muc")];
        const w = sw(v.kieu), hl = 0.6;
        const h1 = add(e, dirv(d + 150), hl), h2 = add(e, dirv(d - 150), hl);
        return (
          <g key={i} className={(v.buoc ?? 0) > 0 ? "cc-in" : undefined} opacity={v.kieu === "thanh_phan" ? 0.85 : 1}>
            <line x1={o[0]} y1={-o[1]} x2={e[0]} y2={-e[1]} stroke={col} strokeWidth={w} strokeDasharray={v.kieu === "thanh_phan" ? "0.4 0.25" : undefined} />
            <path d={`M${sv(h1)} L${sv(e)} L${sv(h2)}`} stroke={col} strokeWidth={w} fill="none" strokeLinejoin="round" strokeLinecap="round" />
            <Label p={lp} a={a} fill={col}>
              <Sub s={v.ten} />
            </Label>
          </g>
        );
      })}
      {rows.map((r, i) =>
        show(r.b, r.den) ? (
          <g key={`b${i}`} className={r.b > 0 ? "cc-in" : undefined}>
            <Label p={[bx + 0.3, y1 - 0.3 - lh * (i + 0.5)]} a="start" fill={r.fill}>
              <Sub s={r.text} />
            </Label>
          </g>
        ) : null,
      )}
    </svg>
  );
}
