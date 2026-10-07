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

export function SoundInterferenceSimulation({ compact = false }: { compact?: boolean }) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [f, setF] = useState(3000);
  const [dCm, setDCm] = useState(28);
  const [mode, setMode] = useState<Mode>("both");
  const [mic, setMic] = useState({ x: 0.35, y: 0.9 });
  const [playing, setPlaying] = useState(false);
  const [vol, setVol] = useState(0.15);

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
    <div className={compact ? "space-y-3" : "mt-6 space-y-5"}>
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
        <span className="pointer-events-none absolute bottom-3 left-2 text-[11px] font-semibold text-white/80">Màn hình · 2 loa (chấm xanh)</span>
        {/* tai / micro */}
        <span
          className="pointer-events-none absolute h-5 w-5 -translate-x-1/2 -translate-y-1/2 rounded-full border-2 border-white bg-emerald-400/90 shadow"
          style={{ left: `${px}%`, top: `${py}%` }}
        />
        <span className="pointer-events-none absolute right-2 top-2 rounded bg-black/50 px-2 py-1 text-[11px] text-white/80">
          Sáng = to · Tối = nhỏ
        </span>
      </div>

      {compact ? (
        <p className="text-sm text-slate-200" aria-live="polite">
          d₂ − d₁ = <b className="text-white">{delta.toFixed(2)} λ</b> → <b className="text-white">{label}</b>
          <span className="text-slate-400"> · chạm bản đồ để đổi chỗ đứng</span>
        </p>
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

      <div className="grid gap-4 sm:grid-cols-2">
        <label className="block text-sm text-slate-200">
          Tần số: <b className="text-white">{f} Hz</b> (λ = {(lambda * 100).toFixed(1)} cm)
          <input type="range" min={1000} max={5000} step={100} value={f} onChange={(e) => setF(+e.target.value)} className="mt-1 w-full" />
        </label>
        <label className={`block text-sm text-slate-200 ${compact ? "hidden" : ""}`}>
          Khoảng cách hai loa d: <b className="text-white">{dCm} cm</b> (MacBook thường 25–30 cm)
          <input type="range" min={10} max={60} step={1} value={dCm} onChange={(e) => setDCm(+e.target.value)} className="mt-1 w-full" />
        </label>
        <label className="block text-sm text-slate-200">
          Âm lượng: <b className="text-white">{Math.round(vol * 100)}%</b>
          <input type="range" min={0.02} max={0.5} step={0.01} value={vol} onChange={(e) => setVol(+e.target.value)} className="mt-1 w-full" />
        </label>
        <div className="flex flex-wrap items-center gap-2 text-sm">
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
              onClick={() => setMode(m)}
              className={`min-h-11 rounded-lg px-3 font-semibold ${mode === m ? "bg-sky-500 text-white" : "bg-white/10 text-slate-200 hover:bg-white/15"}`}
            >
              {t}
            </button>
          ))}
        </div>
      </div>

      <button
        type="button"
        onClick={playing ? stop : start}
        className={`min-h-12 w-full rounded-xl px-5 text-base font-bold text-white sm:w-auto ${playing ? "bg-rose-500" : "bg-emerald-500"}`}
      >
        {playing ? "■ Tắt âm" : "▶ Phát âm đơn sắc"}
      </button>

      {!compact && (
        <>
      <ol className="list-decimal space-y-1 pl-5 text-sm leading-relaxed text-slate-300">
        <li>Dùng loa trong của máy (rút tai nghe, tắt AirPods/Bluetooth), ngồi cách màn khoảng 1 m, chỉnh âm lượng vừa phải.</li>
        <li>Đặt tần số 3000 Hz, bật &quot;Cả hai loa&quot;. Che một tai, dịch đầu sang trái–phải khoảng 40 cm và nghe to nhỏ thay đổi.</li>
        <li>Bấm &quot;Chỉ loa trái&quot; hoặc &quot;Chỉ loa phải&quot;: chỗ nhỏ biến mất vì chỉ còn một nguồn, không giao thoa.</li>
        <li>Muốn đo: để điện thoại cạnh tai, mở app đo dB, so với vị trí chấm xanh trên bản đồ.</li>
      </ol>
      <p className="text-xs leading-relaxed text-slate-400">
        Lưu ý: phòng có tường và bàn phản xạ âm nên vân thật không sạch như bản đồ lý thuyết. Loa ngoài Bluetooth hoặc loa của điện thoại không đồng bộ pha với loa máy nên không dùng làm nguồn thứ hai.
      </p>
        </>
      )}
    </div>
  );
}
