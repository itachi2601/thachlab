"use client";

import { useSyncExternalStore } from "react";
import { scoreText } from "@/lib/parent-format";

/**
 * "Điểm con hướng tới": phụ huynh tự đặt mục tiêu, trang đo khoảng cách tới mục tiêu đó — thay vì chỉ
 * nói "qua / chưa qua" (mốc qua quá thấp so với kỳ vọng của nhiều gia đình).
 * Lưu trên chính điện thoại này (localStorage), thầy KHÔNG thấy — nói rõ ra để phụ huynh yên tâm.
 */
const GOALS = [7, 8, 9] as const;
const EVENT = "thachlab-parent-goal-change";
const key = (studentId: string) => `thachlab-parent-goal:${studentId}`;

function read(studentId: string): number | null {
  try {
    const raw = window.localStorage.getItem(key(studentId));
    const n = raw === null ? NaN : Number(raw);
    return GOALS.includes(n as (typeof GOALS)[number]) ? n : null;
  } catch {
    return null;
  }
}

function subscribe(onChange: () => void) {
  window.addEventListener(EVENT, onChange);
  window.addEventListener("storage", onChange);
  return () => {
    window.removeEventListener(EVENT, onChange);
    window.removeEventListener("storage", onChange);
  };
}

export function useChildGoal(studentId: string): number | null {
  return useSyncExternalStore(subscribe, () => read(studentId), () => null);
}

function save(studentId: string, goal: number | null) {
  try {
    if (goal === null) window.localStorage.removeItem(key(studentId));
    else window.localStorage.setItem(key(studentId), String(goal));
  } catch {}
  window.dispatchEvent(new Event(EVENT));
}

export default function ParentGoal({ studentId, avg }: { studentId: string; avg: number | null }) {
  const goal = useChildGoal(studentId);
  const chip = (active: boolean) =>
    `inline-flex min-h-12 min-w-14 items-center justify-center rounded-xl border px-4 font-semibold ${
      active ? "border-cyan-300 bg-cyan-400/15 text-cyan-300" : "border-white/15 text-slate-200 hover:border-white/30"
    }`;

  return (
    <div className="border-t border-white/10 pt-3">
      <p className="text-slate-400">Điểm con hướng tới</p>
      <div className="mt-2 flex flex-wrap gap-2" role="group" aria-label="Chọn điểm mục tiêu">
        {GOALS.map((g) => (
          <button key={g} type="button" className={chip(goal === g)} aria-pressed={goal === g} onClick={() => save(studentId, g)}>
            {g}
          </button>
        ))}
        {goal !== null && (
          <button type="button" className={chip(false)} onClick={() => save(studentId, null)}>
            Bỏ mục tiêu
          </button>
        )}
      </div>
      {goal === null ? (
        <p className="parent-copy mt-2 text-slate-400">
          Chọn một mức để xem con còn cách bao xa. Mục tiêu chỉ lưu trên điện thoại này, thầy không thấy.
        </p>
      ) : avg === null ? null : avg >= goal ? (
        <p className="parent-copy mt-2 text-emerald-300">
          Điểm trung bình của con ({scoreText(avg)}) đã đạt mục tiêu {goal}.
        </p>
      ) : (
        <p className="parent-copy mt-2 text-slate-300">
          Điểm trung bình hiện tại {scoreText(avg)} — còn cách mục tiêu {goal} khoảng{" "}
          <b className="text-white">{scoreText(Math.round((goal - avg) * 10) / 10)} điểm</b>.
        </p>
      )}
    </div>
  );
}
