"use client";

import { useEffect, useState } from "react";
import { fetchAttendanceForParent, type AttendanceRow, type AttendanceStatus } from "@/services/parent-view";
import { longDate } from "@/lib/parent-format";

/**
 * "Con có đi học đều không?" — câu hỏi thường nằm trong ba nỗi lo đầu của phụ huynh lớp học thêm
 * (trả tiền mà không tận mắt thấy con có đến lớp). Mỗi trạng thái đều có chữ, không chỉ màu (P12).
 * RPC `parent_attendance_summary` chưa có trên DB (migration chưa chạy) hoặc lỗi → ẩn cả khối.
 */
const LABEL: Record<AttendanceStatus, { text: string; cls: string }> = {
  present: { text: "Có mặt", cls: "text-ok" },
  late: { text: "Đến trễ", cls: "text-warn" },
  excused: { text: "Vắng có phép", cls: "text-ink" },
  absent: { text: "Vắng không phép", cls: "text-danger" },
};

const DAY = 24 * 60 * 60 * 1000;

export default function ParentAttendanceCard({ studentId }: { studentId: string }) {
  const [rows, setRows] = useState<AttendanceRow[] | null>(null);
  const [now] = useState(() => new Date().getTime());

  useEffect(() => {
    let cancelled = false;
    fetchAttendanceForParent(studentId).then((r) => {
      if (!cancelled) setRows(r);
    });
    return () => {
      cancelled = true;
    };
  }, [studentId]);

  if (rows === null || rows.length === 0) return null;

  const marked = rows.filter((r) => r.status !== null);
  const recent = marked.filter((r) => now - new Date(`${r.date}T00:00:00`).getTime() <= 30 * DAY);
  const count = (s: AttendanceStatus) => recent.filter((r) => r.status === s).length;
  const attended = count("present") + count("late");

  return (
    <section className="mb-6 rounded-2xl border border-line bg-panel p-5">
      <h2 className="font-display text-lg font-semibold text-ink">Con có đi học đều không?</h2>
      {recent.length === 0 ? (
        <p className="parent-copy mt-2 text-muted">
          Trong 30 ngày qua thầy chưa điểm danh buổi nào. Khi có điểm danh, phụ huynh sẽ thấy ở đây.
        </p>
      ) : (
        <>
          <p className="mt-2 text-muted">30 ngày gần đây</p>
          <p className="parent-num font-display text-2xl font-bold text-ink">
            Có mặt {attended}/{recent.length} buổi
          </p>
          <p className="parent-copy mt-0.5 text-muted">
            Trễ {count("late")} · Vắng có phép {count("excused")} · Vắng không phép {count("absent")}
          </p>
        </>
      )}
      {marked.length > 0 && (
        <ul className="mt-3 divide-y divide-line">
          {marked.slice(0, 5).map((r) => {
            const label = LABEL[r.status as AttendanceStatus];
            return (
              <li key={r.sessionId} className="flex flex-wrap items-baseline justify-between gap-x-3 py-2">
                <span className="text-ink">{longDate(r.date)}</span>
                <span className={`font-semibold ${label.cls}`}>{label.text}</span>
              </li>
            );
          })}
        </ul>
      )}
    </section>
  );
}
