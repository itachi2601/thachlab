"use client";

import { useEffect, useId, useMemo, useRef, useState } from "react";
import data from "@/content/thi-nghiem/tn-l10-newton3-04.json";
import { HALF_GAP, accel, biggerAccel, endTime, stateAt, type PushParams } from "./two-body-push-model";

/**
 * Mô phỏng thí nghiệm tn-l10-newton3-04 "Hai bạn đẩy nhau trên giày trượt" (bài Định luật III Newton).
 * Khoảng giá trị các thanh trượt đọc thẳng từ content/thi-nghiem/tn-l10-newton3-04.json (dữ liệu nguồn),
 * vật lí ở ./two-body-push-model.ts (hàm thuần, có kiểm riêng).
 * Luồng dạy: dự đoán trước → thả → đối chiếu số liệu. Gắn vào bài bằng <div data-sim="tn-l10-newton3-04">.
 */

interface ParamDef {
  ky_hieu: string;
  kieu: string;
  min?: number;
  max?: number;
  mac_dinh?: number;
  buoc?: number;
}

const DEFS = new Map((data.tham_so as ParamDef[]).map((p) => [p.ky_hieu, p]));
const def = (k: string) => {
  const d = DEFS.get(k);
  return { min: d?.min ?? 0, max: d?.max ?? 1, step: d?.buoc ?? 1, init: d?.mac_dinh ?? 0 };
};

const W = 440;
const H = 250;
const CX = W / 2;
const GROUND = 196;
const PX_PER_M = 38;
const RED = "#f87171";
const GREEN = "#34d399";
const CYAN = "#38bdf8";

const fmt = (n: number, d = 2) => n.toLocaleString("vi-VN", { maximumFractionDigits: d });

type Guess = "A" | "B" | "bang";
type Phase = "idle" | "running" | "done";

function Person({ x, m, contact, side, uid }: { x: number; m: number; contact: boolean; side: -1 | 1; uid: string }) {
  const s = 0.62 + (0.38 * (m - 30)) / 60;
  const px = CX + x * PX_PER_M;
  const head = GROUND - 100 * s;
  const shoulder = head + 22 * s;
  const hip = GROUND - 62 * s;
  const armEndX = contact ? CX : px + side * 14 * s;
  const armEndY = contact ? GROUND - 70 : shoulder + 26 * s;
  return (
    <g stroke="currentColor" strokeWidth={2.5} fill="none" strokeLinecap="round" aria-hidden="true" data-uid={uid}>
      <circle cx={px} cy={head} r={12 * s} />
      <line x1={px} y1={head + 12 * s} x2={px} y2={hip} />
      <line x1={px} y1={hip} x2={px - 12 * s} y2={GROUND - 6 * s} />
      <line x1={px} y1={hip} x2={px + 12 * s} y2={GROUND - 6 * s} />
      <line x1={px - 22 * s} y1={GROUND - 2} x2={px + 22 * s} y2={GROUND - 2} stroke={CYAN} strokeWidth={3} />
      <line x1={px} y1={shoulder} x2={armEndX} y2={armEndY} />
    </g>
  );
}

function Arrow({ id, x1, x2, y, color, label, labelAnchor }: { id: string; x1: number; x2: number; y: number; color: string; label: string; labelAnchor?: "start" | "end" | "middle" }) {
  if (Math.abs(x2 - x1) < 6) return null;
  return (
    <g aria-hidden="true">
      <line x1={x1} y1={y} x2={x2} y2={y} stroke={color} strokeWidth={3} markerEnd={`url(#${id})`} />
      <text x={Math.min(W - 44, Math.max(44, (x1 + x2) / 2))} y={y - 12} fill={color} fontSize={12} fontWeight={700} textAnchor={labelAnchor ?? "middle"}>
        {label}
      </text>
    </g>
  );
}

export default function TwoBodyPushSim() {
  const uid = useId().replace(/[^a-zA-Z0-9]/g, "");
  const dA = def("m_A");
  const dB = def("m_B");
  const dF = def("F");
  const dT = def("t_c");
  const [p, setP] = useState<PushParams>({ mA: dA.init, mB: dB.init, F: dF.init, tc: dT.init });
  const [t, setT] = useState(0);
  const [phase, setPhase] = useState<Phase>("idle");
  const [guess, setGuess] = useState<Guess | null>(null);
  const [checked, setChecked] = useState<Guess | null>(null); // dự đoán tại lúc thả
  const [slow, setSlow] = useState(false); // quay chậm ×0,25 để thầy giảng từng nhịp
  const tRef = useRef(0);
  const tEnd = useMemo(() => endTime(p, (W / 2 - 64) / PX_PER_M), [p]);

  useEffect(() => {
    if (phase !== "running") return;
    let raf = 0;
    let last = performance.now();
    const tick = (now: number) => {
      tRef.current = Math.min(tEnd, tRef.current + ((now - last) / 1000) * (slow ? 0.25 : 1));
      last = now;
      setT(tRef.current);
      if (tRef.current >= tEnd) setPhase("done");
      else raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [phase, tEnd, slow]);

  const release = () => {
    setChecked(guess);
    tRef.current = 0;
    if (typeof window !== "undefined" && window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      tRef.current = tEnd;
      setT(tEnd);
      setPhase("done");
      return;
    }
    setT(0);
    setPhase("running");
  };
  const reset = () => {
    tRef.current = 0;
    setT(0);
    setPhase("idle");
    setChecked(null);
  };
  const set = (k: keyof PushParams) => (e: React.ChangeEvent<HTMLInputElement>) => setP((q) => ({ ...q, [k]: Number(e.target.value) }));

  const s = stateAt(p, t);
  const aA = accel(p.F, p.mA);
  const aB = accel(p.F, p.mB);
  const vA = aA * p.tc;
  const vB = aB * p.tc;
  const answer = biggerAccel(p);
  const locked = phase === "running";
  const forceLen = Math.min(78, 26 + p.F * 0.2);
  const accLen = (a: number) => Math.min(116, 11 * a);
  const showForces = phase === "idle" || s.contact;
  const posA = CX + s.xA * PX_PER_M;
  const posB = CX + s.xB * PX_PER_M;
  const mkA = `${uid}r`;
  const mkG = `${uid}g`;
  const mkC = `${uid}c`;

  const sliders: { k: keyof PushParams; label: string; unit: string; d: ReturnType<typeof def> }[] = [
    { k: "mA", label: "Khối lượng bạn A", unit: "kg", d: dA },
    { k: "mB", label: "Khối lượng bạn B", unit: "kg", d: dB },
    { k: "F", label: "Lực đẩy mỗi bên", unit: "N", d: dF },
    { k: "tc", label: "Thời gian hai tay còn chạm nhau", unit: "s", d: dT },
  ];

  return (
    <section className="tl-sim__card" aria-label="Mô phỏng hai bạn đẩy nhau trên giày trượt">
      <p className="tl-sim__title">🧪 Mô phỏng: hai bạn đẩy nhau trên giày trượt</p>

      <div className="tl-sim__guess" role="radiogroup" aria-label="Dự đoán: bạn nào có gia tốc lớn hơn?">
        <p className="tl-sim__q">Dự đoán trước khi thả: bạn nào có gia tốc lớn hơn?</p>
        {(
          [
            ["A", "Bạn A"],
            ["B", "Bạn B"],
            ["bang", "Bằng nhau"],
          ] as [Guess, string][]
        ).map(([v, label]) => (
          <label key={v} className={`tl-sim__chip${guess === v ? " is-on" : ""}`}>
            <input type="radio" name={`${uid}guess`} checked={guess === v} disabled={locked} onChange={() => setGuess(v)} />
            {label}
          </label>
        ))}
      </div>

      <svg viewBox={`0 0 ${W} ${H}`} className="tl-sim__stage" role="img" aria-label="Hai bạn trên giày trượt đẩy nhau rồi trượt ngược chiều">
        <defs>
          {[
            [mkA, RED],
            [mkG, GREEN],
            [mkC, CYAN],
          ].map(([id, c]) => (
            <marker key={id} id={id} viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto">
              <path d="M0,0 L10,5 L0,10 z" fill={c} />
            </marker>
          ))}
        </defs>
        <line x1={8} y1={GROUND} x2={W - 8} y2={GROUND} stroke={CYAN} strokeWidth={2} opacity={0.6} />
        <Person x={s.xA} m={p.mA} contact={showForces} side={-1} uid={`${uid}a`} />
        <Person x={s.xB} m={p.mB} contact={showForces} side={1} uid={`${uid}b`} />
        <text x={posA} y={GROUND + 18} fill="currentColor" fontSize={12} fontWeight={600} textAnchor="middle">A: {fmt(p.mA, 0)} kg</text>
        <text x={posB} y={GROUND + 18} fill="currentColor" fontSize={12} fontWeight={600} textAnchor="middle">B: {fmt(p.mB, 0)} kg</text>
        {showForces && (
          <>
            <Arrow id={mkA} x1={posA + 6} x2={posA + 6 - forceLen} y={GROUND - 36} color={RED} label={`F = ${fmt(p.F, 0)} N`} />
            <Arrow id={mkA} x1={posB - 6} x2={posB - 6 + forceLen} y={GROUND - 36} color={RED} label={`F = ${fmt(p.F, 0)} N`} />
            {phase !== "idle" && (
              <>
                <Arrow id={mkG} x1={posA} x2={posA - accLen(aA)} y={30} color={GREEN} label={`a = ${fmt(aA)} m/s²`} />
                <Arrow id={mkG} x1={posB} x2={posB + accLen(aB)} y={30} color={GREEN} label={`a = ${fmt(aB)} m/s²`} />
              </>
            )}
          </>
        )}
        {!showForces && (
          <>
            <Arrow id={mkC} x1={posA} x2={posA - Math.min(110, 36 * vA)} y={30} color={CYAN} label={`v = ${fmt(vA)} m/s`} />
            <Arrow id={mkC} x1={posB} x2={posB + Math.min(110, 36 * vB)} y={30} color={CYAN} label={`v = ${fmt(vB)} m/s`} />
          </>
        )}
        <text x={CX} y={H - 6} fill="currentColor" fontSize={11} opacity={0.7} textAnchor="middle">
          {phase === "idle" ? "Chỉnh số liệu rồi bấm Thả" : s.contact ? "Hai tay còn chạm nhau: mỗi bạn chịu một lực F" : "Đã rời tay: không còn lực, chuyển động thẳng đều"}
          {" · "}t = {fmt(t)} s
        </text>
      </svg>

      <div className="tl-sim__controls">
        {sliders.map(({ k, label, unit, d }) => (
          <label key={k} className="tl-sim__slider">
            <span>
              {label}: <strong>{fmt(p[k], 2)} {unit}</strong>
            </span>
            <input type="range" min={d.min} max={d.max} step={d.step} value={p[k]} disabled={locked || phase === "done"} onChange={set(k)} />
          </label>
        ))}
      </div>

      <div className="tl-sim__buttons">
        <label className="tl-sim__chip">
          <input type="checkbox" checked={slow} disabled={locked} onChange={(e) => setSlow(e.target.checked)} />
          🐢 Quay chậm ×0,25
        </label>
        {phase === "idle" && (
          <button type="button" className="tl-sim__btn tl-sim__btn--go" onClick={release}>
            ▶ Thả
          </button>
        )}
        {phase === "running" && (
          <button type="button" className="tl-sim__btn" disabled>
            Đang chạy…
          </button>
        )}
        {phase === "done" && (
          <button type="button" className="tl-sim__btn" onClick={reset}>
            ↺ Đặt lại, đổi số liệu
          </button>
        )}
      </div>

      {phase !== "idle" && (
        <div className="tl-sim__result" aria-live="polite">
          {checked && (
            <p className={checked === answer ? "tl-sim__ok" : "tl-sim__no"}>
              {checked === answer ? "Dự đoán đúng. " : "Chưa đúng. "}
              {answer === "bang"
                ? "Hai bạn nặng như nhau và chịu lực bằng nhau nên gia tốc bằng nhau."
                : `Lực hai bên bằng nhau (định luật III), nên bạn nhẹ hơn (bạn ${answer}) có gia tốc lớn hơn (a = F/m).`}
            </p>
          )}
          <div className="table-scroll">
            <table className="tl-table">
              <thead>
                <tr>
                  <th></th>
                  <th>Bạn A</th>
                  <th>Bạn B</th>
                </tr>
              </thead>
              <tbody>
                <tr><td>Khối lượng m</td><td>{fmt(p.mA, 0)} kg</td><td>{fmt(p.mB, 0)} kg</td></tr>
                <tr><td>Lực F (bằng nhau)</td><td>{fmt(p.F, 0)} N</td><td>{fmt(p.F, 0)} N</td></tr>
                <tr><td>Gia tốc a = F/m</td><td>{fmt(aA)} m/s²</td><td>{fmt(aB)} m/s²</td></tr>
                <tr><td>Vận tốc khi rời tay v = a·t</td><td>{fmt(vA)} m/s</td><td>{fmt(vB)} m/s</td></tr>
                <tr><td>Quãng đường đã đi (lúc này)</td><td>{fmt(Math.abs(s.xA) - HALF_GAP + 0)} m</td><td>{fmt(s.xB - HALF_GAP)} m</td></tr>
              </tbody>
            </table>
          </div>
          <p className="tl-sim__eq">
            m<sub>A</sub>·a<sub>A</sub> = {fmt(p.mA, 0)} × {fmt(aA)} = {fmt(p.mA * aA, 1)} N &nbsp;và&nbsp; m<sub>B</sub>·a<sub>B</sub> = {fmt(p.mB, 0)} × {fmt(aB)} = {fmt(p.mB * aB, 1)} N: luôn bằng nhau.
          </p>
        </div>
      )}
    </section>
  );
}
