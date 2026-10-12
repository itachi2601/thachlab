"use client";

import { useCallback, useEffect, useRef, useState } from "react";

const V = 343; // m/s
const W_M = 2.4; // bề ngang vùng vẽ (m), x ∈ [-1,2; 1,2]
const H_M = 1.6; // chiều sâu vùng vẽ (m)
const RES_X = 240;
const RES_Y = 160;

type Mode = "both" | "left" | "right";

/** Tỉ số cường độ so với hai nguồn không giao thoa: |a1 e^{ikr1} + a2 e^{ikr2}|² / (a1² + a2²), nằm trong [0, 2]. */
function ratioAt(x: number, y: number, k: number, d: number, mode: Mode) {
  const r1 = Math.hypot(x + d / 2, y);
  const r2 = Math.hypot(x - d / 2, y);
  const a1 = mode === "right" ? 0 : 1 / r1;
  const a2 = mode === "left" ? 0 : 1 / r2;
  const re = a1 * Math.cos(k * r1) + a2 * Math.cos(k * r2);
  const im = a1 * Math.sin(k * r1) + a2 * Math.sin(k * r2);
  const sum = a1 * a1 + a2 * a2;
  return sum > 0 ? (re * re + im * im) / sum : 0;
}

function colour(t: number): [number, number, number] {
  // t ∈ [0,1]: tối (nhỏ) → vàng sáng (to)
  const c = Math.max(0, Math.min(1, t));
  return [Math.round(15 + 240 * c), Math.round(23 + 190 * c * c + 20 * c), Math.round(60 * (1 - c) + 20)];
}

const sliderClass =
  "h-1.5 w-full cursor-pointer appearance-none rounded-full bg-white/10 accent-[#2563EB] " +
  "[&::-webkit-slider-thumb]:h-3.5 [&::-webkit-slider-thumb]:w-3.5 [&::-webkit-slider-thumb]:appearance-none " +
  "[&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-primary " +
  "[&::-webkit-slider-thumb]:shadow-[0_0_0_3px_rgba(37,99,235,0.25)] " +
  "[&::-moz-range-thumb]:h-3.5 [&::-moz-range-thumb]:w-3.5 [&::-moz-range-thumb]:rounded-full " +
  "[&::-moz-range-thumb]:border-0 [&::-moz-range-thumb]:bg-primary";

export function SoundInterferenceSimulation({ compact = false }: { compact?: boolean }) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [f, setF] = useState(3000);
  const [dCm, setDCm] = useState(28);
  const [mode, setMode] = useState<Mode>("both");
  const [mic, setMic] = useState({ x: 0.35, y: 0.9 });
  const [playing, setPlaying] = useState(false);
  const [vol, setVol] = useState(0.15);
  const [warn, setWarn] = useState(false);

  const audio = useRef<{ ctx: AudioContext; osc: OscillatorNode; gl: GainNode; gr: GainNode; master: GainNode } | null>(null);

  const d = dCm / 100;
  const lambda = V / f;
  const k = (2 * Math.PI) / lambda;

  // Vẽ bản đồ cường độ
  useEffect(() => {
    const cv = canvasRef.current;
    if (!cv) return;
    cv.width = RES_X;
    cv.height = RES_Y;
    const ctx = cv.getContext("2d");
    if (!ctx) return;
    const img = ctx.createImageData(RES_X, RES_Y);
    for (let j = 0; j < RES_Y; j++) {
      const y = 0.03 + (j / (RES_Y - 1)) * (H_M - 0.03);
      for (let i = 0; i < RES_X; i++) {
        const x = -W_M / 2 + (i / (RES_X - 1)) * W_M;
        const [r, g, b] = colour(ratioAt(x, y, k, d, mode) / 2);
        const p = ((RES_Y - 1 - j) * RES_X + i) * 4; // y lớn lên phía trên
        img.data[p] = r;
        img.data[p + 1] = g;
        img.data[p + 2] = b;
        img.data[p + 3] = 255;
      }
    }
    ctx.putImageData(img, 0, 0);
  }, [k, d, mode]);

  // Âm thanh
  useEffect(() => {
    const a = audio.current;
    if (!a) return;
    const t = a.ctx.currentTime;
    a.osc.frequency.setTargetAtTime(f, t, 0.02);
    a.gl.gain.setTargetAtTime(mode === "right" ? 0 : 1, t, 0.02);
    a.gr.gain.setTargetAtTime(mode === "left" ? 0 : 1, t, 0.02);
    a.master.gain.setTargetAtTime(vol, t, 0.02);
  }, [f, mode, vol, playing]);

  const stop = useCallback(() => {
    const a = audio.current;
    if (a) {
      try {
        a.osc.stop();
        a.ctx.close();
      } catch {
        /* đã dừng */
      }
      audio.current = null;
    }
    setPlaying(false);
  }, []);

  useEffect(() => stop, [stop]);

  const start = () => {
    const AC = window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
    const ctx = new AC();
    const osc = ctx.createOscillator();
    osc.type = "sine";
    osc.frequency.value = f;
    const gl = ctx.createGain();
    const gr = ctx.createGain();
    const master = ctx.createGain();
    master.gain.value = vol;
    const merger = ctx.createChannelMerger(2);
    osc.connect(gl).connect(merger, 0, 0);
    osc.connect(gr).connect(merger, 0, 1);
    merger.connect(master).connect(ctx.destination);
    // Ép đầu ra 2 kênh rời nhau (không trộn xuống mono)
    ctx.destination.channelCount = Math.min(2, ctx.destination.maxChannelCount || 2);
    ctx.destination.channelInterpretation = "discrete";
    osc.start();
    audio.current = { ctx, osc, gl, gr, master };
    setPlaying(true);
  };

  const pickMic = (e: React.PointerEvent<HTMLCanvasElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width) * W_M - W_M / 2;
    const y = (1 - (e.clientY - rect.top) / rect.height) * H_M;
    setMic({ x: Math.max(-W_M / 2, Math.min(W_M / 2, x)), y: Math.max(0.1, Math.min(H_M, y)) });
  };

  const r1 = Math.hypot(mic.x + d / 2, mic.y);
  const r2 = Math.hypot(mic.x - d / 2, mic.y);
  const delta = (r2 - r1) / lambda; // hiệu đường đi theo λ
  const ratio = ratioAt(mic.x, mic.y, k, d, mode);
  const label = mode !== "both" ? "chỉ một loa — không giao thoa" : ratio > 1.6 ? "TO (gần cực đại)" : ratio < 0.4 ? "NHỎ (gần cực tiểu)" : "trung gian";
  const spacing = (lambda * 1) / d; // khoảng vân i = λL/d tại L = 1 m

  const px = ((mic.x + W_M / 2) / W_M) * 100;
  const py = (1 - mic.y / H_M) * 100;
  const sx1 = ((-d / 2 + W_M / 2) / W_M) * 100;
  const sx2 = ((d / 2 + W_M / 2) / W_M) * 100;

  return (
    <div className={compact ? "space-y-2.5" : "mt-6 space-y-5"}>
      <div className={`relative w-full overflow-hidden rounded-xl border border-white/10 bg-slate-900 ${compact ? "lg:mx-auto lg:max-w-[560px]" : ""}`} style={{ aspectRatio: `${W_M} / ${H_M}` }}>
        <canvas
          ref={canvasRef}
          className="absolute inset-0 h-full w-full cursor-crosshair touch-none"
          style={{ imageRendering: "auto" }}
          onPointerDown={(e) => {
            e.currentTarget.setPointerCapture(e.pointerId);
            pickMic(e);
          }}
          onPointerMove={(e) => e.buttons && pickMic(e)}
          aria-label="Bản đồ cường độ âm nhìn từ trên xuống; chạm để đặt vị trí tai hoặc micro"
        />
        {/* màn hình + hai loa */}
        <div className="pointer-events-none absolute bottom-0 left-0 right-0 h-1.5 bg-slate-200/80" />
        {[sx1, sx2].map((x, i) => (
          <span
            key={i}
            className="pointer-events-none absolute bottom-0 h-3 w-3 -translate-x-1/2 rounded-full border-2 border-white bg-sky-400"
            style={{ left: `${x}%` }}
          />
        ))}
        <span className="pointer-events-none absolute bottom-3 left-2 text-[12px] font-semibold text-white/80">Màn hình · 2 loa (chấm xanh)</span>
        {/* tai / micro */}
        <span
          className="pointer-events-none absolute h-5 w-5 -translate-x-1/2 -translate-y-1/2 rounded-full border-2 border-white bg-emerald-400/90 shadow"
          style={{ left: `${px}%`, top: `${py}%` }}
        />
        <span className="pointer-events-none absolute right-2 top-2 rounded bg-black/50 px-2 py-1 text-[12px] text-white/80">
          Sáng = to · Tối = nhỏ
        </span>
      </div>

      {/* Hàng điều khiển nút: Phát/Tắt âm + Chọn chế độ loa */}
      <div className="flex flex-wrap items-center gap-2">
        <button
          type="button"
          onClick={playing ? stop : () => setWarn(true)}
          className={`inline-flex min-h-10 items-center justify-center gap-1.5 rounded-lg px-3.5 text-xs sm:text-sm font-semibold transition active:scale-[0.98] ${
            playing
              ? "border border-rose-400/40 bg-rose-500/20 text-rose-200 hover:bg-rose-500/30"
              : "border border-cyan-400/40 bg-cyan-300/[0.16] text-cyan-200 hover:bg-cyan-300/[0.25]"
          }`}
        >
          {playing ? "■ Tắt âm" : "▶ Phát âm"}
        </button>

        <div className="flex overflow-hidden rounded-lg border border-white/10" role="group" aria-label="Chế độ phát loa">
          {(
            [
              ["both", "Cả hai loa"],
              ["left", "Chỉ loa trái"],
              ["right", "Chỉ loa phải"],
            ] as [Mode, string][]
          ).map(([m, t]) => (
            <button
              key={m}
              type="button"
              aria-pressed={mode === m}
              onClick={() => setMode(m)}
              className={`inline-flex min-h-10 items-center px-3 text-xs font-medium transition ${
                mode === m
                  ? "bg-cyan-300/[0.14] text-cyan-300"
                  : "text-slate-400 hover:bg-white/[0.06]"
              }`}
            >
              {t}
            </button>
          ))}
        </div>
      </div>

      {/* Thông số điều chỉnh: f, vol, d (nếu không compact) */}
      <div className={`grid gap-2 ${compact ? "grid-cols-1 sm:grid-cols-2" : "grid-cols-1 sm:grid-cols-3"}`}>
        <label className="flex items-center gap-2 rounded-lg border border-white/10 bg-white/[0.03] px-2.5 py-1.5 text-xs text-slate-400 cursor-pointer">
          <span className="whitespace-nowrap shrink-0">f: <b className="font-mono text-slate-200">{f} Hz</b> <span className="text-[11px] text-slate-500">(λ = {(lambda * 100).toFixed(1)} cm)</span></span>
          <input
            type="range"
            min={1000}
            max={5000}
            step={100}
            value={f}
            onChange={(e) => setF(+e.target.value)}
            className={sliderClass}
            aria-label="Tần số âm thanh"
          />
        </label>

        {!compact && (
          <label className="flex items-center gap-2 rounded-lg border border-white/10 bg-white/[0.03] px-2.5 py-1.5 text-xs text-slate-400 cursor-pointer">
            <span className="whitespace-nowrap shrink-0">Khoảng cách d: <b className="font-mono text-slate-200">{dCm} cm</b></span>
            <input
              type="range"
              min={10}
              max={60}
              step={1}
              value={dCm}
              onChange={(e) => setDCm(+e.target.value)}
              className={sliderClass}
              aria-label="Khoảng cách hai loa"
            />
          </label>
        )}

        <label className="flex items-center gap-2 rounded-lg border border-white/10 bg-white/[0.03] px-2.5 py-1.5 text-xs text-slate-400 cursor-pointer">
          <span className="whitespace-nowrap shrink-0">Âm lượng: <b className="font-mono text-slate-200">{Math.round(vol * 100)}%</b></span>
          <input
            type="range"
            min={0.02}
            max={0.5}
            step={0.01}
            value={vol}
            onChange={(e) => setVol(+e.target.value)}
            className={sliderClass}
            aria-label="Âm lượng"
          />
        </label>
      </div>

      {compact ? (
        <div className="flex flex-wrap items-center justify-between gap-2 rounded-lg border border-white/10 bg-white/[0.03] px-3 py-2 text-xs text-slate-300" aria-live="polite">
          <div>
            <span>d₂ − d₁ = </span>
            <b className="font-mono text-white">{delta.toFixed(2)} λ</b>
            <span className="text-slate-400"> → </span>
            <b className={ratio > 1.6 ? "text-cyan-300" : ratio < 0.4 ? "text-slate-400" : "text-amber-300"}>{label}</b>
          </div>
          <span className="text-[11px] text-slate-500">Chạm bản đồ để đổi vị trí tai</span>
        </div>
      ) : (
        <div className="grid gap-3 rounded-xl border border-white/10 bg-white/[0.03] p-4 text-sm text-slate-200 sm:grid-cols-2">
          <div>
            <span className="text-slate-400">Vị trí tai (chấm xanh lá):</span> ngang {(mic.x * 100).toFixed(0)} cm, cách màn {(mic.y * 100).toFixed(0)} cm
          </div>
          <div>
            <span className="text-slate-400">Hiệu đường đi d₂ − d₁:</span> {delta.toFixed(2)} λ
            <span className="text-slate-400"> (nguyên λ → to, bán nguyên → nhỏ)</span>
          </div>
          <div>
            <span className="text-slate-400">Cường độ so với hai nguồn không giao thoa:</span> ×{ratio.toFixed(2)} → <b className="text-white">{label}</b>
          </div>
          <div>
            <span className="text-slate-400">Khoảng vân ở cách màn 1 m:</span> i ≈ λL/d = {(spacing * 100).toFixed(0)} cm
          </div>
        </div>
      )}

      {/* Hướng dẫn sử dụng: thu gọn tinh tế */}
      <details className="group rounded-lg border border-white/10 bg-white/[0.02] text-xs text-slate-300">
        <summary className="flex min-h-8 cursor-pointer items-center justify-between px-3 py-1.5 font-medium text-slate-400 hover:text-slate-200">
          <span>{compact ? "Cách nghe vân giao thoa âm" : "Cách dùng thí nghiệm"}</span>
          <span className="text-[11px] text-slate-500 transition-transform group-open:rotate-180">▾</span>
        </summary>
        <div className="border-t border-white/5 p-3 leading-relaxed space-y-2">
          <ol className="list-decimal space-y-1.5 pl-4 text-slate-300">
            <li>Dùng loa ngoài của máy tính (laptop hoặc hai loa rời), <b>không đeo tai nghe</b> — mỗi tai nghe chỉ nhận một loa nên không có giao thoa.</li>
            <li>Hạ âm lượng thiết bị xuống thấp, bấm <b>▶ Phát âm</b>, rồi chỉnh thanh âm lượng cho vừa nghe.</li>
            <li>Ngồi thẳng trước màn hình, <b>nghiêng đầu hoặc dịch người sang trái–phải</b> khoảng 10–20 cm: âm lúc to lúc nhỏ là các vân giao thoa.</li>
            <li>Chạm vào bản đồ để đặt chấm xanh lá (vị trí tai) và đối chiếu: số nguyên lần λ → to, bán nguyên → nhỏ.</li>
            <li>Thử <b>Chỉ loa trái</b> / <b>Chỉ loa phải</b>: một loa thì âm đều, không còn chỗ to chỗ nhỏ — chứng tỏ cần hai nguồn kết hợp.</li>
          </ol>
          {!compact && (
            <>
              <p className="font-semibold text-white pt-1">Thiết bị cần có hai loa tách trái – phải</p>
              <p className="leading-relaxed text-slate-400">
                Thí nghiệm chỉ chạy khi máy phát được âm stereo qua hai loa cách nhau vài chục cm. Máy chỉ có một loa (hoặc hai loa sát nhau) sẽ không có vân giao thoa.
              </p>
            </>
          )}
        </div>
      </details>

      {warn && (
        <div
          role="alertdialog"
          aria-modal="true"
          aria-labelledby="snd-warn-title"
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 p-4"
          onClick={() => setWarn(false)}
        >
          <div
            className="w-full max-w-sm space-y-3 rounded-2xl border border-amber-400/40 bg-slate-900 p-5 text-slate-100 shadow-xl"
            onClick={(e) => e.stopPropagation()}
          >
            <h3 id="snd-warn-title" className="text-lg font-bold text-amber-300">
              ⚠ Sắp phát âm thanh
            </h3>
            <p className="text-sm leading-relaxed">
              Thí nghiệm sẽ phát âm đơn sắc (có thể chói tai ở tần số cao). Hãy hạ âm lượng thiết bị, không đeo tai nghe sát tai, và tắt âm khi không dùng.
            </p>
            <div className="flex gap-3">
              <button type="button" onClick={() => setWarn(false)} className="min-h-11 flex-1 rounded-xl border border-white/20 font-bold">
                Huỷ
              </button>
              <button
                type="button"
                autoFocus
                onClick={() => {
                  setWarn(false);
                  start();
                }}
                className="min-h-11 flex-1 rounded-xl bg-emerald-500 font-bold text-white"
              >
                Phát âm
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
