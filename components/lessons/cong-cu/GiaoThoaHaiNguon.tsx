"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";

/**
 * 🧪 "Mặt nước ảo" — công cụ giải dạng giao thoa hai nguồn cùng pha (thử 2/11/2026, bài 14 Sóng dạng 3).
 *
 * Hai chế độ, tách theo nguyên tắc mô phỏng không lộ đáp số (skill soan-bai-tap-mau):
 * - `opened === null` (em chưa bấm "Giải từng bước"): KHÁM PHÁ với số liệu KHÁC đề — kéo điểm P, đổi f, đọc
 *   d₁, d₂, |d₁ − d₂| : λ. Học cách nhìn, không ra đáp số của đề.
 * - `opened = n`: hình theo số liệu đề, lớp phủ chạy tới đúng bước thứ n đã mở (thứ tự bước chuẩn của dạng:
 *   λ → hiệu đường đi → loại M → đếm cực đại → đếm cực tiểu). Bước còn giấu (fading) thì hình chưa vẽ.
 *
 * Quy tắc: N5/N6 (chia nhịp, mờ dần), N8 + H3 (nhãn trên hình, số đo cạnh hình), V10 (bấm mới chạy, tự dừng),
 * D2 (điểm kéo ≥ 44px), D5 (không cần hover), H4 (chữ ≥ 13px ở 360px).
 */

type Props = { f: number; v: number; AB: number; d1: number; d2: number; opened: number | null; color: string; steps?: string[] };

const LOP = 5; // số lớp phủ: λ → hiệu đường đi → loại M → đếm cực đại → đếm cực tiểu

const KHAM_PHA = { AB: 10, v: 30 }; // số liệu khám phá: cố ý khác đề
const GW = 240; // độ phân giải lưới tính sóng (ô), kéo giãn mượt lên khung
const RUN_MS = 20000; // V10: chạy tối đa 20 s rồi tự dừng
const LO = [240, 247, 255], HI = [30, 58, 138]; // đáy sóng/biên độ 0 → đỉnh sóng/biên độ lớn
const C_MAX = "#c2410c", C_MIN = "#0e7490", C_INK = "#0f172a";

const fmt = (x: number, dp = 1) => {
  const s = x.toFixed(dp).replace(/\.?0+$/, "");
  return (s === "-0" ? "0" : s).replace(".", ",");
};

/** Nhánh hypebol |MA| − |MB| = s (A ở −c, B ở +c), toạ độ SVG (y lật). */
function hyperbola(s: number, c: number, yMax: number): string {
  const a = Math.abs(s) / 2;
  if (a < 1e-6) return `M0 ${-yMax} L0 ${yMax}`;
  if (a >= c) return "";
  const b = Math.sqrt(c * c - a * a), T = Math.asinh(yMax / b), sg = Math.sign(s);
  const pts: string[] = [];
  for (let i = 0; i <= 48; i++) {
    const t = -T + (2 * T * i) / 48;
    pts.push(`${(sg * a * Math.cosh(t)).toFixed(3)} ${(-b * Math.sinh(t)).toFixed(3)}`);
  }
  return "M" + pts.join(" L");
}

export default function GiaoThoaHaiNguon({ f, v, AB, d1, d2, opened, color, steps }: Props) {
  const solving = opened !== null;
  // N5: em tự lật từng lớp hình (◀ ▶), không quá số bước đã mở trong lời giải — bước còn giấu thì hình chưa vẽ.
  const cap = Math.min(opened ?? 0, LOP);
  const [shown, setShown] = useState(1);
  const L = solving ? Math.min(shown, cap) : 0;
  const [fExp, setFExp] = useState(12);
  const geo = useMemo(() => {
    const ab = solving ? AB : KHAM_PHA.AB;
    const lam = solving ? v / f : KHAM_PHA.v / fExp;
    const c = ab / 2;
    // M theo đề: (x + c)² + y² = d1², (x − c)² + y² = d2²
    const mx = (d1 * d1 - d2 * d2) / (4 * c);
    const my = Math.sqrt(Math.max(d2 * d2 - (mx - c) ** 2, 0));
    const X = Math.max(c + 5, solving ? Math.abs(mx) + 2.5 : 0);
    const Y1 = Math.max(c + 5, solving ? my + 2.5 : 0), Y0 = 4.5;
    return { ab, lam, c, mx, my, X, Y1, Y0, GH: Math.round((GW * (Y1 + Y0)) / (2 * X)) };
  }, [solving, AB, v, f, fExp, d1, d2]);
  const { lam, c, X, Y1, Y0, GH } = geo;

  const [p, setP] = useState({ x: -2.6, y: 6.2 }); // điểm P khám phá
  const [view, setView] = useState<"song" | "bien_do">("song");
  const [playing, setPlaying] = useState(false);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const svgRef = useRef<SVGSVGElement>(null);

  // khoảng cách mỗi ô tới A, B — tính lại khi đổi hình
  const field = useMemo(() => {
    const r1 = new Float32Array(GW * GH), r2 = new Float32Array(GW * GH);
    for (let j = 0; j < GH; j++) {
      const y = Y1 - ((j + 0.5) * (Y1 + Y0)) / GH;
      for (let i = 0; i < GW; i++) {
        const x = -X + ((i + 0.5) * 2 * X) / GW;
        r1[j * GW + i] = Math.hypot(x + c, y);
        r2[j * GW + i] = Math.hypot(x - c, y);
      }
    }
    return { r1, r2 };
  }, [GH, X, Y0, Y1, c]);

  const draw = useCallback(
    (phase: number) => {
      const cv = canvasRef.current;
      const ctx = cv?.getContext("2d");
      if (!cv || !ctx) return;
      const img = ctx.createImageData(GW, GH);
      const k = (2 * Math.PI) / lam;
      const { r1, r2 } = field;
      for (let n = 0; n < r1.length; n++) {
        const t =
          view === "song"
            ? (Math.cos(phase - k * r1[n]) + Math.cos(phase - k * r2[n]) + 2) / 4
            : Math.abs(Math.cos((Math.PI * (r1[n] - r2[n])) / lam));
        const o = n * 4;
        img.data[o] = LO[0] + (HI[0] - LO[0]) * t;
        img.data[o + 1] = LO[1] + (HI[1] - LO[1]) * t;
        img.data[o + 2] = LO[2] + (HI[2] - LO[2]) * t;
        img.data[o + 3] = 255;
      }
      ctx.putImageData(img, 0, 0);
    },
    [field, lam, view, GH],
  );

  useEffect(() => {
    if (!playing || view !== "song") {
      draw(0);
      return;
    }
    let raf = 0;
    const t0 = performance.now();
    const tick = (now: number) => {
      const dt = now - t0;
      draw(2 * Math.PI * 0.6 * (dt / 1000)); // chạy chậm: 0,6 dao động/giây trên màn hình
      if (dt < RUN_MS) raf = requestAnimationFrame(tick);
      else setPlaying(false);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [playing, view, draw]);

  // kéo P (chuột/chạm/bàn phím)
  const toWorld = (e: React.PointerEvent) => {
    const svg = svgRef.current, m = svg?.getScreenCTM();
    if (!svg || !m) return null;
    const pt = new DOMPoint(e.clientX, e.clientY).matrixTransform(m.inverse());
    return { x: Math.min(Math.max(pt.x, -X + 0.3), X - 0.3), y: Math.min(Math.max(-pt.y, -Y0 + 0.3), Y1 - 0.3) };
  };
  const dragging = useRef(false);
  const onDown = (e: React.PointerEvent) => {
    dragging.current = true;
    try {
      (e.currentTarget as Element).setPointerCapture(e.pointerId); // kéo ra khỏi vòng chạm vẫn bám theo
    } catch {}
    const w = toWorld(e);
    if (w) setP(w);
  };
  const onMove = (e: React.PointerEvent) => {
    if (!dragging.current) return;
    const w = toWorld(e);
    if (w) setP(w);
  };
  const onUp = () => {
    dragging.current = false;
  };
  const onKey = (e: React.KeyboardEvent) => {
    const d = { ArrowLeft: [-0.2, 0], ArrowRight: [0.2, 0], ArrowUp: [0, 0.2], ArrowDown: [0, -0.2] }[e.key];
    if (!d) return;
    e.preventDefault();
    setP((q) => ({ x: q.x + d[0], y: q.y + d[1] }));
  };

  const pt = solving ? { x: geo.mx, y: geo.my } : p;
  const pd1 = Math.hypot(pt.x + c, pt.y), pd2 = Math.hypot(pt.x - c, pt.y);
  const ratio = Math.abs(pd1 - pd2) / lam;
  const frac = ratio - Math.floor(ratio);
  const verdict =
    Math.min(frac, 1 - frac) < 0.08
      ? { t: `trên vân cực đại (k = ${Math.round(ratio)})`, c: C_MAX }
      : Math.abs(frac - 0.5) < 0.08
        ? { t: "trên vân cực tiểu", c: C_MIN }
        : { t: "giữa hai vân", c: "inherit" };

  // đếm trên AB (bước 4, 5)
  const nAB = geo.ab / lam;
  const maxima: number[] = [], minima: number[] = [];
  for (let k = Math.ceil(-nAB); k <= Math.floor(nAB); k++) if (Math.abs(k) < nAB - 1e-9) maxima.push(k);
  for (let k = Math.ceil(-nAB - 0.5); k <= Math.floor(nAB - 0.5); k++) if (Math.abs(k + 0.5) < nAB - 1e-9) minima.push(k + 0.5);
  const sM = d1 - d2; // hiệu đường đi có dấu của M theo đề
  const kM = sM / lam;
  const mOnMax = Math.abs(kM - Math.round(kM)) < 1e-6;
  const fs = 0.95; // cỡ chữ (đơn vị cm của hình) ≈ 14–15px ở 375px

  const label = (x: number, y: number, text: string, fill = C_INK, anchor: "start" | "middle" | "end" = "middle") => (
    <text
      x={x}
      y={y}
      fontSize={fs}
      textAnchor={anchor}
      fill={fill}
      stroke="#fff"
      strokeWidth={0.28}
      paintOrder="stroke"
      fontWeight={600}
    >
      {text}
    </text>
  );

  return (
    <figure className="cc-tool" style={{ borderColor: color }}>
      <figcaption className="cc-head">
        <span className="cc-title">🧪 Mặt nước ảo</span>
        <span className="cc-sub">
          {solving
            ? "Số liệu của đề — mở bước nào, hình vẽ thêm bước đó."
            : "Thử trước khi giải (số liệu khác đề): kéo P lên vệt đậm, vệt nhạt rồi so |d₁ − d₂| với λ."}
        </span>
      </figcaption>

      <div className="cc-stage" style={{ aspectRatio: `${2 * X} / ${Y1 + Y0}` }}>
        <canvas ref={canvasRef} width={GW} height={GH} className="cc-canvas" aria-hidden="true" />
        <svg
          ref={svgRef}
          viewBox={`${-X} ${-Y1} ${2 * X} ${Y1 + Y0}`}
          className="cc-svg"
          role="img"
          aria-label={
            solving
              ? `Hai nguồn A, B cách nhau ${fmt(geo.ab)} cm, điểm M cách A ${fmt(d1)} cm, cách B ${fmt(d2)} cm`
              : `Hai nguồn A, B cách nhau ${fmt(geo.ab)} cm, điểm P kéo được`
          }
        >
          {/* bước 4–5: mọi vân cực đại / cực tiểu, mờ */}
          {solving && L >= 4 &&
            maxima.map((k) => <path key={`M${k}`} d={hyperbola(k * lam, c, Y1 + Y0)} stroke={C_MAX} strokeWidth={0.06} fill="none" opacity={0.55} />)}
          {solving && L >= 5 &&
            minima.map((k) => (
              <path key={`m${k}`} d={hyperbola(k * lam, c, Y1 + Y0)} stroke={C_MIN} strokeWidth={0.06} strokeDasharray="0.3 0.25" fill="none" opacity={0.7} />
            ))}
          {/* bước 3: vân qua M và hai vân cực đại kẹp hai bên */}
          {solving && L >= 3 && (
            <g className="cc-in">
              {[Math.floor(kM), Math.ceil(kM)].filter((k, i, a) => a.indexOf(k) === i).map((k) => (
                <path key={k} d={hyperbola(k * lam, c, Y1 + Y0)} stroke={C_MAX} strokeWidth={0.12} fill="none" />
              ))}
              <path
                d={hyperbola(sM, c, Y1 + Y0)}
                stroke={mOnMax ? C_MAX : C_MIN}
                strokeWidth={0.2}
                strokeDasharray={mOnMax ? undefined : "0.45 0.3"}
                fill="none"
              />
            </g>
          )}
          {/* trục AB */}
          <line x1={-c} y1={0} x2={c} y2={0} stroke={C_INK} strokeWidth={0.08} opacity={0.6} />
          {/* bước 1 (hoặc luôn có khi khám phá): thước λ */}
          {(!solving || L >= 1) && (
            <g className="cc-in">
              <path
                d={`M${c + 0.7} 1.0 v0.5 h${lam} v-0.5`}
                stroke={C_INK}
                strokeWidth={0.1}
                fill="none"
              />
              {label(c + 0.7 + lam / 2, 2.6, solving ? `λ = ${fmt(lam, 2)} cm` : "λ")}
            </g>
          )}
          {/* đoạn d1, d2 */}
          {(!solving || L >= 2) && (
            <g className="cc-in">
              <line x1={-c} y1={0} x2={pt.x} y2={-pt.y} stroke={C_INK} strokeWidth={0.1} />
              <line x1={c} y1={0} x2={pt.x} y2={-pt.y} stroke={C_INK} strokeWidth={0.1} />
              {solving && label((pt.x - c) / 2 - 0.9, -pt.y / 2 - 0.3, `d₁ = ${fmt(d1)}`, C_INK, "end")}
              {solving && label((pt.x + c) / 2 + 0.6, -pt.y / 2 + 0.9, `d₂ = ${fmt(d2)}`, C_INK, "start")}
            </g>
          )}
          {/* bước 4–5: điểm trên AB */}
          {solving && L >= 4 &&
            maxima.map((k, i) => (
              <circle key={`pM${k}`} cx={(k * lam) / 2} cy={0} r={0.22} fill={C_MAX} className="cc-pop" style={{ animationDelay: `${i * 90}ms` }} />
            ))}
          {solving && L >= 5 &&
            minima.map((k, i) => (
              <circle key={`pm${k}`} cx={(k * lam) / 2} cy={0} r={0.18} fill="#fff" stroke={C_MIN} strokeWidth={0.1} className="cc-pop" style={{ animationDelay: `${i * 90}ms` }} />
            ))}
          {/* nguồn */}
          {[-c, c].map((x, i) => (
            <g key={i}>
              <circle cx={x} cy={0} r={0.32} fill={C_INK} />
              {label(x, 1.35, i ? "B" : "A")}
            </g>
          ))}
          {/* M (đề) hoặc P (kéo được) */}
          {solving ? (
            <g>
              <circle cx={pt.x} cy={-pt.y} r={0.3} fill="#facc15" stroke={C_INK} strokeWidth={0.08} />
              {label(pt.x + 0.5, -pt.y - 0.5, "M", C_INK, "start")}
            </g>
          ) : (
            <g
              className="cc-drag"
              tabIndex={0}
              role="slider"
              aria-label="Điểm P — kéo hoặc dùng phím mũi tên"
              aria-valuetext={`d1 ${fmt(pd1)} cm, d2 ${fmt(pd2)} cm`}
              onKeyDown={onKey}
              onPointerDown={onDown}
              onPointerMove={onMove}
              onPointerUp={onUp}
              onPointerCancel={onUp}
            >
              <circle cx={pt.x} cy={-pt.y} r={1.45} fill="transparent" />
              <circle cx={pt.x} cy={-pt.y} r={0.34} fill="#facc15" stroke={C_INK} strokeWidth={0.08} />
              {label(pt.x + 0.55, -pt.y - 0.5, "P", C_INK, "start")}
            </g>
          )}
        </svg>
      </div>

      {solving && cap > 0 && (
        <div className="cc-stepper">
          <button type="button" aria-label="Hình bước trước" disabled={L <= 1} onClick={() => setShown(L - 1)}>
            ◀
          </button>
          <span>
            Hình bước {L}/{LOP}
            {steps?.[L - 1] ? ` · ${steps[L - 1]}` : ""}
          </span>
          <button type="button" aria-label="Hình bước sau" disabled={L >= cap} onClick={() => setShown(L + 1)}>
            ▶
          </button>
        </div>
      )}
      <div className="cc-controls">
        <button type="button" className="lesson-btn-ghost" onClick={() => setPlaying((x) => !x)} disabled={view !== "song"}>
          {playing ? "❚❚ Dừng" : "▶ Chạy"}
        </button>
        <div className="cc-seg" role="group" aria-label="Cách xem">
          <button type="button" aria-pressed={view === "song"} onClick={() => setView("song")}>
            Mặt nước
          </button>
          <button
            type="button"
            aria-pressed={view === "bien_do"}
            onClick={() => {
              setView("bien_do");
              setPlaying(false);
            }}
          >
            Biên độ
          </button>
        </div>
        {!solving && (
          <label className="cc-slider">
            <span>
              f = {fmt(fExp)} Hz · λ = {fmt(lam, 2)} cm
            </span>
            <input type="range" min={10} max={25} step={0.5} value={fExp} onChange={(e) => setFExp(Number(e.target.value))} style={{ accentColor: color }} />
          </label>
        )}
      </div>
      <p className="cc-note">
        {view === "song" ? "Màu đậm = đỉnh sóng, nhạt = đáy sóng." : "Màu đậm = dao động mạnh, gần trắng = gần như đứng yên."}
        {solving && L >= 3 && !mOnMax && (
          <>
            {" "}
            <span style={{ color: C_MAX }}>Nét liền: vân cực đại k = {Math.floor(kM)} và k = {Math.ceil(kM)}</span>;{" "}
            <span style={{ color: C_MIN }}>nét đứt: vân qua M</span>.
          </>
        )}
      </p>

      {/* thước đo: khám phá luôn có; khi giải chỉ từ bước 2 */}
      {(!solving || L >= 2) && (
        <div className="cc-readout">
          <div className="cc-nums">
            <span>d₁ = {fmt(pd1)} cm</span>
            <span>d₂ = {fmt(pd2)} cm</span>
            <span>
              |d₁ − d₂| = {fmt(Math.abs(pd1 - pd2))} cm = <b>{fmt(ratio, 2)} λ</b>
            </span>
          </div>
          <TileBar ratio={ratio} />
          {(!solving || L >= 3) && (
            <p className="cc-verdict" style={{ color: verdict.c }}>
              {solving ? "M" : "P"} {verdict.t}
            </p>
          )}
        </div>
      )}

      {solving && L >= 4 && <NumberLine n={nAB} maxima={maxima} minima={L >= 5 ? minima : []} />}
    </figure>
  );
}

/** |d₁ − d₂| xếp thành các khúc λ: thấy ngay "3 khúc trọn + nửa khúc". */
function TileBar({ ratio }: { ratio: number }) {
  const full = Math.floor(ratio + 1e-9), rest = ratio - full, W = Math.max(Math.ceil(ratio), 4);
  return (
    <svg viewBox={`-0.1 -0.1 ${W + 0.2} 1.2`} className="cc-tiles" style={{ width: `${(W + 0.2) * 34}px` }} aria-hidden="true">
      {Array.from({ length: full }, (_, i) => (
        <g key={i} className="cc-pop" style={{ animationDelay: `${i * 120}ms` }}>
          <rect x={i + 0.04} y={0} width={0.92} height={1} rx={0.12} fill={C_MAX} opacity={0.85} />
          <text x={i + 0.5} y={0.68} fontSize={0.5} textAnchor="middle" fill="#fff" fontWeight={700}>
            λ
          </text>
        </g>
      ))}
      {rest > 0.02 && (
        <rect x={full + 0.04} y={0} width={Math.max(rest * 0.92, 0.04)} height={1} rx={0.12} fill={C_MIN} opacity={0.85} className="cc-pop" style={{ animationDelay: `${full * 120}ms` }} />
      )}
    </svg>
  );
}

/** Trục số k: hai đầu ±AB/λ rỗng (không tính A, B), chấm cực đại (k) và cực tiểu (k + ½) hiện lần lượt. */
function NumberLine({ n, maxima, minima }: { n: number; maxima: number[]; minima: number[] }) {
  const R = Math.ceil(n) + 1, step = R > 8 ? 2 : 1;
  const ticks: number[] = [];
  for (let k = -R; k <= R; k += step) ticks.push(k);
  return (
    <div className="cc-nl">
      <svg viewBox={`${-R - 0.6} -1.6 ${2 * R + 1.2} 3.2`} aria-label={`Trục số k từ ${-R} đến ${R}`}>
        <line x1={-R - 0.4} y1={0} x2={R + 0.4} y2={0} stroke="currentColor" strokeWidth={0.05} />
        {ticks.map((k) => (
          <g key={k}>
            <line x1={k} y1={-0.15} x2={k} y2={0.15} stroke="currentColor" strokeWidth={0.04} />
            <text x={k} y={1.15} fontSize={0.55} textAnchor="middle" fill="currentColor">
              {k}
            </text>
          </g>
        ))}
        {[-n, n].map((x) => (
          <circle key={x} cx={x} cy={0} r={0.22} fill="var(--bg, #fff)" stroke="currentColor" strokeWidth={0.07} />
        ))}
        {maxima.map((k, i) => (
          <circle key={`M${k}`} cx={k} cy={0} r={0.17} fill={C_MAX} className="cc-pop" style={{ animationDelay: `${i * 90}ms` }} />
        ))}
        {minima.map((k, i) => (
          <circle key={`m${k}`} cx={k} cy={0} r={0.14} fill="var(--bg, #fff)" stroke={C_MIN} strokeWidth={0.07} className="cc-pop" style={{ animationDelay: `${i * 90}ms` }} />
        ))}
        <text x={0} y={-0.75} fontSize={0.55} textAnchor="middle" fill="currentColor">
          {`−${fmt(n, 2)} < k < ${fmt(n, 2)}`}
        </text>
      </svg>
      <p className="cc-count">
        <span style={{ color: C_MAX }}>● {maxima.length} cực đại</span>
        {minima.length > 0 && <span style={{ color: C_MIN }}>○ {minima.length} cực tiểu</span>}
      </p>
    </div>
  );
}
