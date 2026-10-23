"use client";

import { AlertTriangle } from "lucide-react";
import { FLAG_INFO, LEVEL_INFO } from "@/lib/tro-giang/co-bat-thuong";

/** Chú giải cờ dùng chung cho tổng quan, hàng chờ duyệt và màn từng người. */
export default function FlagLegend({ defaultOpen = false }: { defaultOpen?: boolean }) {
  return (
    <details open={defaultOpen} className="rounded-xl border border-white/10 bg-white/5 p-3 text-sm text-slate-300">
      <summary className="cursor-pointer font-semibold text-slate-200">Cờ đỏ, cờ vàng là gì?</summary>
      <div className="mt-3 space-y-3">
        <p className="text-xs text-slate-400">
          Cờ do hệ thống tự gắn khi đối chiếu phiếu với dữ liệu có sẵn. Cờ chỉ nhắc thầy xem, không tự trừ điểm hay chặn duyệt.
        </p>
        {(["red", "amber"] as const).map((level) => (
          <div key={level} className="flex gap-2">
            <AlertTriangle size={14} className={`mt-0.5 shrink-0 ${level === "red" ? "text-red-300" : "text-amber-300"}`} />
            <p>
              <b className={level === "red" ? "text-red-300" : "text-amber-300"}>{LEVEL_INFO[level].label}</b>: {LEVEL_INFO[level].meaning}
            </p>
          </div>
        ))}
        <ul className="space-y-1.5 border-t border-white/10 pt-3 text-xs text-slate-400">
          {Object.entries(FLAG_INFO).map(([code, info]) => (
            <li key={code}>
              <b className="text-slate-200">{info.title}</b>: {info.why}
            </li>
          ))}
        </ul>
      </div>
    </details>
  );
}
