/**
 * Đặc tả đồ thị (do AI trả về) → SVG vẽ bằng mã, không để AI tự tính toạ độ từng điểm.
 *
 * AI (Edge Function draw-figure) chỉ nêu THÔNG SỐ: trục, khoảng giá trị, vạch chia, các đường
 * (sin/cos theo A, T, φ; đường gấp khúc; hyperbol p·V = k; hàm mũ N₀·e^(−t/τ)), điểm đặc biệt,
 * đường gióng. Mọi toạ độ pixel đều tính ở đây nên đường cong luôn đúng toán học và khớp vạch chia.
 * Cùng một spec vẽ ra cùng một hình — thầy "Vẽ lại" chỉ đổi thông số, không đổi cách vẽ.
 */

export interface FigureTick {
  v: number;
  label?: string; // mặc định: số theo kiểu VN (dấu phẩy)
}

export type FigureSeries =
  | {
      type: "sinusoid";
      /** y = A·cos(2π·x/T + phi) + y0 (phi tính bằng rad). Muốn sin thì phi = −π/2. */
      A: number;
      T: number;
      phi?: number;
      y0?: number;
      domain?: [number, number];
      color?: string;
      label?: string;
      dashed?: boolean;
    }
  | {
      type: "polyline";
      points: [number, number][];
      color?: string;
      label?: string;
      dashed?: boolean;
    }
  | {
      /** y = k / x (đẳng nhiệt p–V, …) trên domain (x > 0). */
      type: "hyperbola";
      k: number;
      domain: [number, number];
      color?: string;
      label?: string;
      dashed?: boolean;
    }
  | {
      /** y = y0 · e^(−x/tau) + yInf (phóng xạ, phóng điện tụ, …). */
      type: "exponential";
      y0: number;
      tau: number;
      yInf?: number;
      domain?: [number, number];
      color?: string;
      label?: string;
      dashed?: boolean;
    };

export interface FigureSpec {
  kind: "plot";
  xLabel: string; // "t (s)"
  yLabel: string; // "x (cm)"
  xRange: [number, number];
  yRange: [number, number];
  xTicks?: FigureTick[];
  yTicks?: FigureTick[];
  series: FigureSeries[];
  /** Điểm đánh dấu (chấm đỏ) kèm nhãn tuỳ chọn. */
  points?: { x: number; y: number; label?: string }[];
  /** Đường gióng nét đứt: x = v (dọc) hoặc y = v (ngang), kèm nhãn tuỳ chọn. */
  guides?: { x?: number; y?: number; label?: string }[];
  /** Đường lưới mờ tại các vạch chia. */
  grid?: boolean;
}

const W = 440;
const H = 260;
const ML = 52;
const MR = 34;
const MT = 26;
const MB = 40;
const PALETTE = ["#2563eb", "#dc2626", "#16a34a", "#9333ea"];

const num = (v: unknown): number | null => (typeof v === "number" && Number.isFinite(v) ? v : null);

function fmtVN(v: number): string {
  const s = Number.isInteger(v) ? String(v) : String(Math.round(v * 1000) / 1000);
  return s.replace(".", ",").replace("-", "−");
}

function esc(s: string): string {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

/** Kiểm tra + chuẩn hoá spec do AI trả về. Trả null nếu không dùng được. */
export function normalizeFigureSpec(input: unknown): FigureSpec | null {
  if (!input || typeof input !== "object") return null;
  const o = input as Record<string, unknown>;
  const range = (r: unknown): [number, number] | null => {
    if (!Array.isArray(r) || r.length !== 2) return null;
    const a = num(r[0]);
    const b = num(r[1]);
    return a !== null && b !== null && b > a ? [a, b] : null;
  };
  const xRange = range(o.xRange);
  const yRange = range(o.yRange);
  if (!xRange || !yRange) return null;
  const ticks = (t: unknown): FigureTick[] | undefined =>
    Array.isArray(t)
      ? t
          .map((x) => {
            if (typeof x === "number") return num(x) !== null ? { v: x } : null;
            if (x && typeof x === "object") {
              const v = num((x as Record<string, unknown>).v);
              const label = (x as Record<string, unknown>).label;
              return v !== null ? { v, label: typeof label === "string" ? label : undefined } : null;
            }
            return null;
          })
          .filter((x): x is FigureTick => !!x)
          .slice(0, 20)
      : undefined;
  const series: FigureSeries[] = [];
  if (Array.isArray(o.series)) {
    for (const s of o.series.slice(0, 4)) {
      if (!s || typeof s !== "object") continue;
      const r = s as Record<string, unknown>;
      const common = {
        color: typeof r.color === "string" && /^#[0-9a-f]{6}$/i.test(r.color) ? r.color : undefined,
        label: typeof r.label === "string" ? r.label.slice(0, 40) : undefined,
        dashed: r.dashed === true,
      };
      const dom = range(r.domain) ?? undefined;
      if (r.type === "sinusoid") {
        const A = num(r.A);
        const T = num(r.T);
        if (A === null || T === null || T <= 0) continue;
        series.push({ type: "sinusoid", A, T, phi: num(r.phi) ?? 0, y0: num(r.y0) ?? 0, domain: dom, ...common });
      } else if (r.type === "polyline") {
        const pts = Array.isArray(r.points)
          ? r.points
              .map((p) => (Array.isArray(p) && num(p[0]) !== null && num(p[1]) !== null ? ([p[0], p[1]] as [number, number]) : null))
              .filter((p): p is [number, number] => !!p)
          : [];
        if (pts.length < 2) continue;
        series.push({ type: "polyline", points: pts.slice(0, 200), ...common });
      } else if (r.type === "hyperbola") {
        const k = num(r.k);
        if (k === null || !dom || dom[0] <= 0) continue;
        series.push({ type: "hyperbola", k, domain: dom, ...common });
      } else if (r.type === "exponential") {
        const y0 = num(r.y0);
        const tau = num(r.tau);
        if (y0 === null || tau === null || tau <= 0) continue;
        series.push({ type: "exponential", y0, tau, yInf: num(r.yInf) ?? 0, domain: dom, ...common });
      }
    }
  }
  if (series.length === 0) return null;
  const points = Array.isArray(o.points)
    ? o.points
        .map((p): { x: number; y: number; label?: string } | null => {
          if (!p || typeof p !== "object") return null;
          const q = p as Record<string, unknown>;
          const x = num(q.x);
          const y = num(q.y);
          return x !== null && y !== null ? { x, y, label: typeof q.label === "string" ? q.label.slice(0, 24) : undefined } : null;
        })
        .filter((p): p is { x: number; y: number; label?: string } => !!p)
        .slice(0, 12)
    : undefined;
  const guides = Array.isArray(o.guides)
    ? o.guides
        .map((g): { x?: number; y?: number; label?: string } | null => {
          if (!g || typeof g !== "object") return null;
          const q = g as Record<string, unknown>;
          const x = num(q.x);
          const y = num(q.y);
          if (x === null && y === null) return null;
          return { x: x ?? undefined, y: y ?? undefined, label: typeof q.label === "string" ? q.label.slice(0, 24) : undefined };
        })
        .filter((g): g is { x?: number; y?: number; label?: string } => !!g)
        .slice(0, 12)
    : undefined;
  return {
    kind: "plot",
    xLabel: typeof o.xLabel === "string" ? o.xLabel.slice(0, 24) : "",
    yLabel: typeof o.yLabel === "string" ? o.yLabel.slice(0, 24) : "",
    xRange,
    yRange,
    xTicks: ticks(o.xTicks),
    yTicks: ticks(o.yTicks),
    series,
    points,
    guides,
    grid: o.grid !== false,
  };
}

/** Vẽ SVG từ spec. Trục/chữ dùng currentColor để hợp cả nền tối và sáng. */
export function renderFigureSpec(spec: FigureSpec): string {
  const [x0, x1] = spec.xRange;
  const [y0, y1] = spec.yRange;
  const px = (x: number) => ML + ((x - x0) / (x1 - x0)) * (W - ML - MR);
  const py = (y: number) => H - MB - ((y - y0) / (y1 - y0)) * (H - MT - MB);
  const inX = (x: number) => x >= x0 - 1e-9 && x <= x1 + 1e-9;
  const inY = (y: number) => y >= y0 - 1e-9 && y <= y1 + 1e-9;
  const axisY = inY(0) ? py(0) : py(y0); // vị trí trục hoành
  const axisX = inX(0) ? px(0) : px(x0); // vị trí trục tung
  const out: string[] = [];
  const text = (x: number, y: number, s: string, extra = "") =>
    out.push(`<text x="${x.toFixed(1)}" y="${y.toFixed(1)}" font-size="12" font-family="sans-serif" fill="currentColor" ${extra}>${esc(s)}</text>`);

  // Lưới
  if (spec.grid) {
    const g: string[] = [];
    for (const t of spec.xTicks ?? []) if (inX(t.v)) g.push(`<line x1="${px(t.v).toFixed(1)}" y1="${MT}" x2="${px(t.v).toFixed(1)}" y2="${H - MB}"/>`);
    for (const t of spec.yTicks ?? []) if (inY(t.v)) g.push(`<line x1="${ML}" y1="${py(t.v).toFixed(1)}" x2="${W - MR}" y2="${py(t.v).toFixed(1)}"/>`);
    if (g.length) out.push(`<g stroke="currentColor" stroke-width="0.6" opacity="0.15">${g.join("")}</g>`);
  }

  // Đường gióng
  for (const gd of spec.guides ?? []) {
    if (gd.x !== undefined && inX(gd.x))
      out.push(`<line x1="${px(gd.x).toFixed(1)}" y1="${MT}" x2="${px(gd.x).toFixed(1)}" y2="${axisY.toFixed(1)}" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.6"/>`);
    if (gd.y !== undefined && inY(gd.y))
      out.push(`<line x1="${axisX.toFixed(1)}" y1="${py(gd.y).toFixed(1)}" x2="${W - MR}" y2="${py(gd.y).toFixed(1)}" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.6"/>`);
    if (gd.label) {
      const lx = gd.x !== undefined ? px(gd.x) + 3 : axisX + 4;
      const ly = gd.y !== undefined ? py(gd.y) - 4 : MT + 12;
      text(lx, ly, gd.label);
    }
  }

  // Trục
  out.push(`<line x1="${ML - 8}" y1="${axisY.toFixed(1)}" x2="${W - MR + 14}" y2="${axisY.toFixed(1)}" stroke="currentColor" stroke-width="1.8"/>`);
  out.push(`<polygon points="${W - MR + 14},${axisY.toFixed(1)} ${W - MR + 5},${(axisY - 4).toFixed(1)} ${W - MR + 5},${(axisY + 4).toFixed(1)}" fill="currentColor"/>`);
  out.push(`<line x1="${axisX.toFixed(1)}" y1="${H - MB + 8}" x2="${axisX.toFixed(1)}" y2="${MT - 12}" stroke="currentColor" stroke-width="1.8"/>`);
  out.push(`<polygon points="${axisX.toFixed(1)},${MT - 12} ${(axisX - 4).toFixed(1)},${MT - 3} ${(axisX + 4).toFixed(1)},${MT - 3}" fill="currentColor"/>`);
  text(W - MR + 16, axisY - 7, spec.xLabel, 'text-anchor="end"');
  text(axisX + 8, MT - 4, spec.yLabel);
  text(axisX - 12, axisY + 14, "O");

  // Vạch chia
  for (const t of spec.xTicks ?? []) {
    if (!inX(t.v) || Math.abs(t.v) < 1e-9) continue;
    out.push(`<line x1="${px(t.v).toFixed(1)}" y1="${(axisY - 4).toFixed(1)}" x2="${px(t.v).toFixed(1)}" y2="${(axisY + 4).toFixed(1)}" stroke="currentColor" stroke-width="1.4"/>`);
    text(px(t.v), axisY + 15, t.label ?? fmtVN(t.v), 'text-anchor="middle"');
  }
  for (const t of spec.yTicks ?? []) {
    if (!inY(t.v) || Math.abs(t.v) < 1e-9) continue;
    out.push(`<line x1="${(axisX - 4).toFixed(1)}" y1="${py(t.v).toFixed(1)}" x2="${(axisX + 4).toFixed(1)}" y2="${py(t.v).toFixed(1)}" stroke="currentColor" stroke-width="1.4"/>`);
    text(axisX - 7, py(t.v) + 4, t.label ?? fmtVN(t.v), 'text-anchor="end"');
  }

  // Đường
  spec.series.forEach((s, i) => {
    const color = s.color ?? PALETTE[i % PALETTE.length];
    const dash = s.dashed ? ' stroke-dasharray="6,4"' : "";
    let pts: [number, number][] = [];
    if (s.type === "polyline") pts = s.points;
    else {
      const [d0, d1] = s.domain ?? [x0, x1];
      const N = 160;
      for (let k = 0; k <= N; k++) {
        const x = d0 + ((d1 - d0) * k) / N;
        let y: number;
        if (s.type === "sinusoid") y = s.A * Math.cos((2 * Math.PI * x) / s.T + (s.phi ?? 0)) + (s.y0 ?? 0);
        else if (s.type === "hyperbola") y = x !== 0 ? s.k / x : NaN;
        else y = s.y0 * Math.exp(-x / s.tau) + (s.yInf ?? 0);
        pts.push([x, y]);
      }
    }
    // Cắt phần ra ngoài khung: tách thành nhiều đoạn
    const segs: string[] = [];
    let cur: string[] = [];
    for (const [x, y] of pts) {
      if (Number.isFinite(y) && inX(x) && inY(y)) cur.push(`${px(x).toFixed(1)},${py(y).toFixed(1)}`);
      else if (cur.length) {
        segs.push(cur.join(" "));
        cur = [];
      }
    }
    if (cur.length) segs.push(cur.join(" "));
    for (const seg of segs)
      out.push(`<polyline points="${seg}" fill="none" stroke="${color}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"${dash}/>`);
    if (s.label) {
      // Nhãn đặt ở điểm 1/3 (đường lẻ) hay 2/3 (đường chẵn) chiều dài để hai đường gặp nhau ở cuối không đè nhãn lên nhau.
      const vis = pts.filter(([x, y]) => Number.isFinite(y) && inX(x) && inY(y));
      const at = vis[Math.min(vis.length - 1, Math.floor(vis.length * (i % 2 === 0 ? 0.33 : 0.66)))];
      if (at)
        out.push(`<text x="${(px(at[0]) + 4).toFixed(1)}" y="${(py(at[1]) - 7).toFixed(1)}" font-size="12" font-family="sans-serif" fill="${color}">${esc(s.label)}</text>`);
    }
  });

  // Điểm
  for (const p of spec.points ?? []) {
    if (!inX(p.x) || !inY(p.y)) continue;
    out.push(`<circle cx="${px(p.x).toFixed(1)}" cy="${py(p.y).toFixed(1)}" r="3.2" fill="#dc2626"/>`);
    if (p.label) text(px(p.x) + 6, py(p.y) - 6, p.label);
  }

  return (
    `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="100%" ` +
    `style="max-width:${W}px;height:auto;display:block;margin:8px auto">${out.join("")}</svg>`
  );
}
