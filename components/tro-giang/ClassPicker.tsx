"use client";

import { useState } from "react";
import { Star } from "lucide-react";
import type { TaAssistantClass } from "@/lib/tro-giang/queries";

/**
 * Chọn lớp cho buổi đang ghi. Bấm 1 chạm là đổi khối — một buổi tối các em hay chạy cả 10, 11
 * lẫn 12 nên danh sách mở cho mọi khối đang học, lớp thầy phân công chỉ được đánh dấu sao và
 * xếp trước chứ không chặn các lớp còn lại. Lớp lẻ (12A2, đội tuyển…) gõ tay ở ô "Lớp khác".
 */
export default function ClassPicker({
  classes,
  value,
  onChange,
  loading = false,
}: {
  classes: TaAssistantClass[];
  value: string;
  onChange: (name: string) => void;
  loading?: boolean;
}) {
  const known = classes.some((item) => item.name === value);
  const hasAssigned = classes.some((item) => item.assigned);
  const hasOthers = classes.some((item) => !item.assigned);
  const [customOpen, setCustomOpen] = useState(false);
  // Không lấy được lớp nào (chưa phân công + chưa đọc được bảng lớp) thì mở luôn ô gõ tay,
  // đừng bắt các em bấm thêm một nút mới ghi được buổi.
  const customActive = customOpen || (!!value && !known) || (!loading && classes.length === 0);

  return (
    <div>
      <div className="mb-2 flex items-center justify-between gap-3">
        <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">Lớp</p>
        {value ? (
          <span className="rounded-full bg-blue-500/15 px-2.5 py-1 text-xs font-bold text-blue-200">{value}</span>
        ) : (
          <span className="text-xs text-slate-500">Chọn đúng khối của buổi này</span>
        )}
      </div>

      <div className="flex flex-wrap gap-2">
        {classes.map((item) => {
          const active = value === item.name && !customOpen;
          return (
            <button
              key={item.class_id}
              type="button"
              onClick={() => {
                onChange(item.name);
                setCustomOpen(false);
              }}
              className={`flex items-center gap-1.5 rounded-full border px-4 py-2.5 text-sm font-bold transition ${
                active
                  ? "border-blue-500 bg-blue-600 text-white"
                  : "border-white/10 bg-white/5 text-slate-300 active:bg-white/10"
              }`}
            >
              {item.assigned && (
                <Star
                  size={13}
                  className={active ? "text-white" : "text-amber-300"}
                  fill="currentColor"
                  aria-label="Lớp được phân công"
                />
              )}
              {item.name}
            </button>
          );
        })}

        <button
          type="button"
          onClick={() => {
            // Bỏ chọn chip khối khi chuyển sang gõ tay, tránh lưu nhầm lớp cũ.
            // Đóng lại bằng cách chạm một chip khối bất kỳ.
            if (known) onChange("");
            setCustomOpen(true);
          }}
          className={`rounded-full border px-4 py-2.5 text-sm transition ${
            customActive
              ? "border-blue-500 bg-blue-600 text-white"
              : "border-dashed border-white/20 text-slate-400"
          }`}
        >
          Lớp khác…
        </button>
      </div>

      {customActive && (
        <input
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder="12A2"
          className="mt-2 w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-white placeholder:text-slate-500"
        />
      )}

      {loading && classes.length === 0 ? (
        <p className="mt-2 text-xs text-slate-500">Đang tải danh sách lớp…</p>
      ) : (
        hasAssigned &&
        hasOthers && (
          <p className="mt-2 text-xs text-slate-500">
            <Star size={11} className="mr-1 inline text-amber-300" fill="currentColor" /> lớp thầy phân công · dạy
            hỗ trợ khối khác vẫn chọn và ghi bình thường.
          </p>
        )
      )}
    </div>
  );
}
