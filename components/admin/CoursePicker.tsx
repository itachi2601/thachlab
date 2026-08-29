"use client";

import { useEffect, useState } from "react";
import {
  fetchAllCourseOfferings,
  type CourseOfferingWithSubject,
} from "@/services/course-enrollments";

/** Chọn nhiều khóa học CTTC dạng chip. Không chọn khóa nào = áp dụng toàn trường. */
export default function CoursePicker({
  selected,
  onChange,
}: {
  selected: number[];
  onChange: (ids: number[]) => void;
}) {
  const [courses, setCourses] = useState<CourseOfferingWithSubject[]>([]);

  useEffect(() => {
    fetchAllCourseOfferings().then(setCourses).catch(() => setCourses([]));
  }, []);

  return (
    <div>
      <p className="mb-2 text-sm font-medium text-slate-300">
        Khóa học CTTC{" "}
        <span className="font-normal text-slate-500">
          (không chọn = toàn trường)
        </span>
      </p>
      <div className="flex flex-wrap gap-2">
        {courses.map((c) => {
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
              className={`rounded-full border px-3 py-1.5 text-sm font-medium transition-colors ${
                on
                  ? "border-primary bg-white/5 text-primary"
                  : "border-white/10 text-slate-400 hover:border-white/30"
              }`}
            >
              {on ? "☑" : "☐"} {c.subjectLabel} · {c.name}
              {c.class_label && ` (${c.class_label})`} · {c.school_year}
            </button>
          );
        })}
        {courses.length === 0 && (
          <span className="text-sm text-slate-500">
            Chưa có khóa học CTTC — thêm ở mục Khóa học.
          </span>
        )}
      </div>
    </div>
  );
}
