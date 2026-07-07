"use client";

import { useCallback, useEffect, useState } from "react";
import type { Exam } from "@/features/exams/types";
import ExamEditor from "@/components/admin/ExamEditor";
import { getSupabase } from "@/services/supabase";

interface ExamRow {
  id: number;
  created_at: string;
  title: string;
  duration_minutes: number;
  published: boolean;
  question_count: number;
}

export default function ExamsAdmin() {
  const [exams, setExams] = useState<ExamRow[]>([]);
  const [editing, setEditing] = useState<Exam | null | "new">();

  const reload = useCallback(() => {
    getSupabase()
      .from("exams")
      .select("id, created_at, title, duration_minutes, published, question_count")
      .order("created_at", { ascending: false })
      .then(({ data }) => setExams((data as ExamRow[]) ?? []));
  }, []);

  useEffect(reload, [reload]);

  if (editing !== undefined) {
    return (
      <ExamEditor
        exam={editing === "new" ? null : editing}
        onDone={() => {
          setEditing(undefined);
          reload();
        }}
      />
    );
  }

  return (
    <div className="space-y-6">
      <button
        onClick={() => setEditing("new")}
        className="rounded-full bg-[#2563EB] px-5 py-2.5 text-sm font-semibold text-white hover:bg-[#1D4ED8]"
      >
        + Tạo đề mới
      </button>

      <div className="space-y-3">
        {exams.map((e) => (
          <div
            key={e.id}
            className="flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-white/10 bg-[#0B1020] px-5 py-4"
          >
            <div>
              <p className="font-medium text-white">{e.title}</p>
              <p className="text-xs text-slate-500">
                {e.question_count} câu · {e.duration_minutes} phút ·{" "}
                {e.published ? "đang mở" : "bản nháp"}
              </p>
            </div>
            <div className="flex gap-2">
              <button
                onClick={async () => {
                  const { data } = await getSupabase()
                    .from("exams")
                    .select("*")
                    .eq("id", e.id)
                    .single();
                  if (data) setEditing(data as Exam);
                }}
                className="rounded-full border border-white/15 px-3 py-1.5 text-xs font-medium text-slate-300 hover:border-white/30"
              >
                Sửa
              </button>
              <button
                onClick={async () => {
                  await getSupabase()
                    .from("exams")
                    .update({ published: !e.published })
                    .eq("id", e.id);
                  reload();
                }}
                className="rounded-full border border-white/15 px-3 py-1.5 text-xs font-medium text-slate-300 hover:border-white/30"
              >
                {e.published ? "Đóng đề" : "Mở đề"}
              </button>
              <button
                onClick={async () => {
                  if (
                    !confirm(
                      `Xóa đề "${e.title}"? Toàn bộ điểm của đề này cũng bị xóa.`,
                    )
                  )
                    return;
                  await getSupabase().from("exams").delete().eq("id", e.id);
                  reload();
                }}
                className="rounded-full border border-red-500/30 px-3 py-1.5 text-xs font-medium text-red-300 hover:border-red-500/60"
              >
                Xóa
              </button>
            </div>
          </div>
        ))}
        {exams.length === 0 && (
          <p className="text-sm text-slate-400">
            Chưa có đề nào. Bấm &ldquo;Tạo đề mới&rdquo; hoặc nhờ Claude nhập đề
            từ file Word/Azota.
          </p>
        )}
      </div>
    </div>
  );
}
