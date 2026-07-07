"use client";

import { useEffect, useState } from "react";
import type { SchoolClass } from "@/features/exams/types";
import { fetchClasses } from "@/services/classes";

/** Chọn nhiều lớp dạng chip. Không chọn lớp nào = áp dụng toàn trường. */
export default function ClassPicker({
  selected,
  onChange,
}: {
  selected: number[];
  onChange: (ids: number[]) => void;
}) {
  const [classes, setClasses] = useState<SchoolClass[]>([]);

  useEffect(() => {
    fetchClasses().then(setClasses);
  }, []);

  return (
    <div>
      <p className="mb-2 text-sm font-medium text-slate-300">
        Lớp học{" "}
        <span className="font-normal text-slate-500">
          (không chọn = toàn trường)
        </span>
      </p>
      <div className="flex flex-wrap gap-2">
        {classes.map((c) => {
          const on = selected.includes(c.id);
          return (
            <button
              key={c.id}
              type="button"
              onClick={() =>
                onChange(
                  on
                    ? selected.filter((id) => id !== c.id)
                    : [...selected, c.id],
                )
              }
              style={on ? { borderColor: c.color, color: c.color } : undefined}
              className={`rounded-full border px-3 py-1.5 text-sm font-medium transition-colors ${
                on
                  ? "bg-white/5"
                  : "border-white/10 text-slate-400 hover:border-white/30"
              }`}
            >
              {on ? "☑" : "☐"} {c.icon && `${c.icon} `}
              {c.name}
            </button>
          );
        })}
        {classes.length === 0 && (
          <span className="text-sm text-slate-500">
            Chưa có lớp — thêm ở mục Lớp học.
          </span>
        )}
      </div>
    </div>
  );
}
