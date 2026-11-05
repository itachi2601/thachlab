"use client";

/**
 * Chuyển động trên hình `cong_cu` ("một dạng — một hình", 5/11/2026): thay mô phỏng SVG riêng dưới đề bằng chuyển động
 * chạy trên CHÍNH hình em dùng để giải — cùng toạ độ, màu, nhãn (N8, N4). Chỉ chạy khi bấm, một lượt rồi về hình gốc
 * (B4, V10); máy đặt giảm chuyển động thì nhảy thẳng tới cuối. Không biết gì về từng họ hình: chỉ đổi số trong JSON theo
 * đường dẫn (`hinh.2.goc`) rồi vẽ lại bằng component sẵn có.
 */

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import type { WorkedDong } from "@/features/lessons/types";

type Val = number | string | boolean;

function giaTri(d: WorkedDong["doi"][number], t: number): Val | undefined {
  const cac: Val[] | undefined = d.cac ?? (d.tu != null && d.den != null ? [d.tu, d.den] : undefined);
  if (!cac?.length) return undefined;
  if (cac.length === 1) return cac[0];
  const x = Math.min(Math.max(t, 0), 1) * (cac.length - 1),
    i = Math.min(Math.floor(x), cac.length - 2),
    a = cac[i],
    b = cac[i + 1];
  if (typeof a === "number" && typeof b === "number") return a + (b - a) * (x - i);
  return x - i < 0.5 ? a : b;
}

function datTheoDuong(obj: unknown, p: string, v: Val) {
  const k = p.split(".");
  let o = obj as Record<string, unknown>;
  for (let i = 0; i < k.length - 1; i++) {
    const n = o?.[k[i]];
    if (n == null || typeof n !== "object") return;
    o = n as Record<string, unknown>;
  }
  if (o) o[k[k.length - 1]] = v;
}

/** Áp mốc t (0..1) của chuyển động lên bản sao JSON hình. */
export function apDong<T>(tool: T, d: WorkedDong, t: number): T {
  const c = structuredClone(tool);
  for (const x of d.doi) {
    const v = giaTri(x, t);
    if (v !== undefined) datTheoDuong(c, x.p, v);
  }
  return c;
}

export function useDong<T extends { dong?: WorkedDong[] }>(tool: T) {
  const [run, setRun] = useState<{ i: number; t: number } | null>(null);
  const raf = useRef(0);
  useEffect(() => () => cancelAnimationFrame(raf.current), []);
  const play = useCallback(
    (i: number) => {
      const d = tool.dong?.[i];
      if (!d) return;
      cancelAnimationFrame(raf.current);
      const reduce = typeof window !== "undefined" && window.matchMedia?.("(prefers-reduced-motion: reduce)").matches;
      if (reduce) {
        setRun(null);
        return;
      }
      const ms = Math.max(0.5, d.giay ?? 3) * 1000,
        t0 = performance.now();
      const tick = (now: number) => {
        const t = (now - t0) / ms;
        if (t >= 1) {
          setRun(null);
          return;
        }
        setRun({ i, t });
        raf.current = requestAnimationFrame(tick);
      };
      setRun({ i, t: 0 });
      raf.current = requestAnimationFrame(tick);
    },
    [tool],
  );
  const cur = useMemo(() => (run && tool.dong?.[run.i] ? apDong(tool, tool.dong[run.i], run.t) : tool), [tool, run]);
  return { cur, play, dangChay: run?.i ?? null };
}

/** Nút chạy chuyển động: chỉ những `dong` khớp chỗ đang xem (`buoc` của dòng = bước đang làm, hoặc hình dưới đề). */
export function DongNut({
  dong,
  khop,
  play,
  dangChay,
}: {
  dong?: WorkedDong[];
  khop: (d: WorkedDong) => boolean;
  play: (i: number) => void;
  dangChay: number | null;
}) {
  const ds = (dong ?? []).map((d, i) => ({ d, i })).filter(({ d }) => khop(d));
  if (!ds.length) return null;
  return (
    <div className="cc-dong">
      {ds.map(({ d, i }) => (
        <button key={i} type="button" className="cc-dong-nut" disabled={dangChay != null} onClick={() => play(i)}>
          {dangChay === i ? "Đang chạy…" : d.nut}
        </button>
      ))}
    </div>
  );
}
