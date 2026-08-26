"use client";

import { useEffect, useMemo, useState } from "react";
import type { ClassStudent } from "@/services/classes";
import { fetchClassExamResults, type ClassExamResult } from "@/services/class-results";

export default function TeacherThptGradebook({ students }: { students: ClassStudent[] }) {
  const [rows, setRows] = useState<ClassExamResult[] | null>(null);
  const [examFilter, setExamFilter] = useState<number | "all">("all");
  const studentIds = useMemo(() => students.map((item) => item.id), [students]);
  const studentById = useMemo(() => new Map(students.map((item) => [item.id, item])), [students]);

  useEffect(() => {
    fetchClassExamResults(studentIds).then(setRows).catch(() => setRows([]));
  }, [studentIds]);

  const examOptions = useMemo(() => {
    const map = new Map<number, string>();
    rows?.forEach((row) => map.set(row.exam_id, row.exams?.title ?? `Đề #${row.exam_id}`));
    return [...map.entries()];
  }, [rows]);

  const filtered = (rows ?? []).filter((row) => examFilter === "all" || row.exam_id === examFilter);

  function exportCsv() {
    const header = "Họ tên,Đề,Điểm,Thời gian (giây),Ngày nộp";
    const lines = filtered.map((row) =>
      [
        studentById.get(row.student_id)?.full_name ?? "",
        (row.exams?.title ?? "").replaceAll(",", ";"),
        row.score,
        row.duration_seconds,
        new Date(row.created_at).toLocaleString("vi-VN"),
      ].join(","),
    );
    const blob = new Blob(["﻿" + [header, ...lines].join("\n")], { type: "text/csv;charset=utf-8" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "bang-diem-lop.csv";
    a.click();
    URL.revokeObjectURL(a.href);
  }

  if (!rows) return <p className="text-slate-400">Đang tải…</p>;

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center gap-3">
        <select
          value={String(examFilter)}
          onChange={(e) => setExamFilter(e.target.value === "all" ? "all" : Number(e.target.value))}
          className="rounded-xl border border-white/10 bg-[#0B1020] px-3 py-2 text-sm text-white focus:border-primary focus:outline-none"
        >
          <option value="all">Tất cả đề</option>
          {examOptions.map(([id, title]) => (
            <option key={id} value={id}>{title}</option>
          ))}
        </select>
        <span className="text-sm text-slate-400">{filtered.length} lượt làm</span>
        <button
          onClick={exportCsv}
          disabled={filtered.length === 0}
          className="ml-auto rounded-full border border-white/15 px-4 py-2 text-sm font-medium text-slate-200 hover:border-white/30 disabled:opacity-40"
        >
          Xuất CSV
        </button>
      </div>

      {filtered.length === 0 ? (
        <p className="text-sm text-slate-400">Lớp chưa có lượt làm bài nào.</p>
      ) : (
        <div className="overflow-x-auto rounded-2xl border border-white/10">
          <table className="w-full min-w-150 text-left text-sm">
            <thead className="bg-white/5 text-slate-400">
              <tr>
                <th className="px-4 py-3 font-medium">Học sinh</th>
                <th className="px-4 py-3 font-medium">Đề</th>
                <th className="px-4 py-3 text-right font-medium">Điểm</th>
                <th className="px-4 py-3 font-medium">Ngày nộp</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5 text-slate-300">
              {filtered.map((row) => (
                <tr key={row.id}>
                  <td className="px-4 py-3 text-white">{studentById.get(row.student_id)?.full_name ?? "(đã rời lớp)"}</td>
                  <td className="px-4 py-3">{row.exams?.title}</td>
                  <td className="px-4 py-3 text-right font-mono font-semibold text-white">{Number(row.score).toLocaleString("vi-VN")}</td>
                  <td className="px-4 py-3 text-slate-400">{new Date(row.created_at).toLocaleString("vi-VN")}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
