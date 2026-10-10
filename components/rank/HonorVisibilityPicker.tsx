"use client";

import { useEffect, useState } from "react";
import { Eye } from "lucide-react";
import { HONOR_VISIBILITY_LABELS, type HonorVisibility } from "@/features/rank/types";
import { fetchMyHonorVisibility, setMyHonorVisibility } from "@/services/rank";

/**
 * Học sinh chọn cách mình xuất hiện ở mục "Vinh danh tuần" trên trang chủ công khai.
 * Cột chưa có (migration chưa chạy) hoặc lỗi → không render gì.
 */
export default function HonorVisibilityPicker({ className = "" }: { className?: string }) {
  const [value, setValue] = useState<HonorVisibility | null | undefined>(undefined);
  const [state, setState] = useState<"idle" | "saving" | "saved" | "error">("idle");

  useEffect(() => {
    fetchMyHonorVisibility().then(setValue).catch(() => setValue(null));
  }, []);

  if (!value) return null;

  async function change(next: HonorVisibility) {
    const prev = value;
    setValue(next);
    setState("saving");
    try {
      await setMyHonorVisibility(next);
      setState("saved");
    } catch {
      setValue(prev);
      setState("error");
    }
  }

  return (
    <div className={`flex flex-wrap items-center gap-x-3 gap-y-1 rounded-2xl border border-line bg-panel px-4 py-3 text-xs text-muted ${className}`}>
      <Eye size={14} className="text-primary" />
      <label htmlFor="honor-visibility" className="text-ink">
        Trên bảng vinh danh trang chủ, em hiện là
      </label>
      <select
        id="honor-visibility"
        value={value}
        onChange={(e) => change(e.target.value as HonorVisibility)}
        className="rounded-lg border border-line-strong bg-panel px-2 py-1 text-xs text-ink"
      >
        {(Object.keys(HONOR_VISIBILITY_LABELS) as HonorVisibility[]).map((k) => (
          <option key={k} value={k}>
            {HONOR_VISIBILITY_LABELS[k]}
          </option>
        ))}
      </select>
      {state === "saving" && <span>Đang lưu…</span>}
      {state === "saved" && <span className="text-emerald-300">Đã lưu</span>}
      {state === "error" && <span className="text-red-300">Chưa lưu được, thử lại nhé.</span>}
    </div>
  );
}
