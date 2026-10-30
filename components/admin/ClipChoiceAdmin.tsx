"use client";

import { useEffect, useState } from "react";
import type { SchoolClass } from "@/features/exams/types";
import { displayClassesByGrade, fetchClasses } from "@/services/classes";
import { fetchClipChoiceStats, type ClipChoiceStat } from "@/services/clip-choice";

const pct = (a: number, b: number) => (b > 0 ? `${Math.round((a / b) * 100)}%` : "—");

export default function ClipChoiceAdmin() {
  const [classes, setClasses] = useState<SchoolClass[]>([]);
  const [classId, setClassId] = useState<number | null>(null);
  const [rows, setRows] = useState<ClipChoiceStat[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchClasses().then((c) => setClasses(displayClassesByGrade(c)));
  }, []);

  useEffect(() => {
    if (classId == null) return;
    let alive = true;
    setRows(null);
    setError(null);
    fetchClipChoiceStats(classId)
      .then((r) => alive && setRows(r))
      .catch((e: Error) => alive && setError(e.message));
    return () => {
      alive = false;
    };
  }, [classId]);

  return (
    <div className="space-y-4">
      <div>
        <h1 className="text-xl font-bold text-white">Dự đoán ở khung video</h1>
        <p className="text-sm text-slate-400">
          Mỗi dòng là một khung thí nghiệm. Chỉ có số đếm theo lớp, không hiện tên học sinh.
        </p>
      </div>
      <div className="flex flex-wrap gap-2">
        {classes.map((c) => (
          <button
            key={c.id}
            type="button"
            onClick={() => setClassId(c.id)}
            className={`rounded-xl border px-3 py-1.5 text-sm ${
              classId === c.id ? "border-primary bg-primary/20 text-white" : "border-white/10 text-slate-300"
            }`}
          >
            {c.name}
          </button>
        ))}
      </div>
      {error && <p className="text-sm text-red-400">{error}</p>}
      {classId != null && !rows && !error && <p className="text-sm text-slate-400">Đang tải…</p>}
      {rows && rows.length === 0 && <p className="text-sm text-slate-400">Lớp này chưa có lượt chọn nào.</p>}
      {rows && rows.length > 0 && (
        <div className="overflow-x-auto rounded-xl border border-white/10">
          <table className="w-full text-left text-sm text-slate-200">
            <thead className="bg-white/5 text-xs text-slate-400">
              <tr>
                <th className="p-2">Khung</th>
                <th className="p-2">Bài</th>
                <th className="p-2">Tới điểm dừng</th>
                <th className="p-2">Bỏ qua</th>
                <th className="p-2">A</th>
                <th className="p-2">B</th>
                <th className="p-2">C</th>
                <th className="p-2">D</th>
                <th className="p-2">Đúng / đã chọn</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((r) => (
                <tr key={r.tn_id} className="border-t border-white/5">
                  <td className="p-2 font-mono">{r.tn_id}</td>
                  <td className="p-2">{r.lesson_id}</td>
                  <td className="p-2">
                    {r.n}/{r.class_students}
                  </td>
                  <td className="p-2">{r.n_bo_qua}</td>
                  <td className="p-2">{r.n_a}</td>
                  <td className="p-2">{r.n_b}</td>
                  <td className="p-2">{r.n_c}</td>
                  <td className="p-2">{r.n_d}</td>
                  <td className="p-2">
                    {r.n_dung}/{r.n_chon} ({pct(r.n_dung, r.n_chon)})
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
