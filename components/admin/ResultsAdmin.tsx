"use client";

import { useEffect, useMemo, useState } from "react";
import { getSupabase } from "@/services/supabase";

interface ResultRow {
  id: number;
  created_at: string;
  score: number;
  duration_seconds: number;
  exam_id: number;
  profiles: { full_name: string; class_name: string } | null;
  exams: { title: string } | null;
}

export default function ResultsAdmin() {
  const [rows, setRows] = useState<ResultRow[] | null>(null);
  const [examFilter, setExamFilter] = useState<number | "all">("all");
  const [classFilter, setClassFilter] = useState<string>("all");

  useEffect(() => {
    getSupabase()
      .from("exam_results")
      .select(
        "id, created_at, score, duration_seconds, exam_id, profiles(full_name, class_name), exams(title)",
      )
      .order("created_at", { ascending: false })
      .limit(1000)
      .then(({ data }) => setRows((data as unknown as ResultRow[]) ?? []));
  }, []);

  const examOptions = useMemo(() => {
    const map = new Map<number, string>();
    rows?.forEach((r) => map.set(r.exam_id, r.exams?.title ?? `Đề #${r.exam_id}`));
    return [...map.entries()];
  }, [rows]);

  const classOptions = useMemo(
    () =>
      [...new Set((rows ?? []).map((r) => r.profiles?.class_name ?? ""))].filter(
        Boolean,
      ),
    [rows],
  );

  const filtered = (rows ?? []).filter(
    (r) =>
      (examFilter === "all" || r.exam_id === examFilter) &&
      (classFilter === "all" || r.profiles?.class_name === classFilter),
  );

  function exportCsv() {
    const header = "Họ tên,Lớp,Đề,Điểm,Thời gian (giây),Ngày nộp";
    const lines = filtered.map((r) =>
      [
        r.profiles?.full_name ?? "",
        r.profiles?.class_name ?? "",
        (r.exams?.title ?? "").replaceAll(",", ";"),
        r.score,
        r.duration_seconds,
        new Date(r.created_at).toLocaleString("vi-VN"),
      ].join(","),
    );
    const blob = new Blob(["﻿" + [header, ...lines].join("\n")], {
      type: "text/csv;charset=utf-8",
    });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "diem-thachlab.csv";
    a.click();
    URL.revokeObjectURL(a.href);
  }

  if (!rows) return <p className="text-slate-400">Đang tải…</p>;

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center gap-3">
        <select
          value={String(examFilter)}
          onChange={(e) =>
            setExamFilter(e.target.value === "all" ? "all" : Number(e.target.value))
          }
          className="rounded-xl border border-white/10 bg-[#0B1020] px-3 py-2 text-sm text-white focus:border-[#3B82F6] focus:outline-none"
        >
          <option value="all">Tất cả đề</option>
          {examOptions.map(([id, title]) => (
            <option key={id} value={id}>
              {title}
            </option>
          ))}
        </select>
        <select
          value={classFilter}
          onChange={(e) => setClassFilter(e.target.value)}
          className="rounded-xl border border-white/10 bg-[#0B1020] px-3 py-2 text-sm text-white focus:border-[#3B82F6] focus:outline-none"
        >
          <option value="all">Tất cả lớp</option>
          {classOptions.map((c) => (
            <option key={c} value={c}>
              Lớp {c}
            </option>
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
        <p className="text-sm text-slate-400">Chưa có lượt làm bài nào.</p>
      ) : (
        <div className="overflow-x-auto rounded-2xl border border-white/10">
          <table className="w-full min-w-150 text-left text-sm">
            <thead className="bg-white/5 text-slate-400">
              <tr>
                <th className="px-4 py-3 font-medium">Học sinh</th>
                <th className="px-4 py-3 font-medium">Lớp</th>
                <th className="px-4 py-3 font-medium">Đề</th>
                <th className="px-4 py-3 text-right font-medium">Điểm</th>
                <th className="px-4 py-3 font-medium">Ngày nộp</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5 text-slate-300">
              {filtered.map((r) => (
                <tr key={r.id}>
                  <td className="px-4 py-3 text-white">
                    {r.profiles?.full_name ?? "(đã xóa)"}
                  </td>
                  <td className="px-4 py-3">{r.profiles?.class_name}</td>
                  <td className="px-4 py-3">{r.exams?.title}</td>
                  <td className="px-4 py-3 text-right font-mono font-semibold text-white">
                    {Number(r.score).toLocaleString("vi-VN")}
                  </td>
                  <td className="px-4 py-3 text-slate-400">
                    {new Date(r.created_at).toLocaleString("vi-VN")}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
