"use client";

import { useEffect, useState } from "react";
import { useToast } from "@/components/ui/Toast";
import {
  createCncDrawingDownloadUrl,
  fetchCncDrawingSubmissionsByCourse,
  reviewCncDrawingSubmission,
  type CncDrawingSubmission,
} from "@/services/cnc-drawing-submissions";

export default function TeacherDrawingApprovals({ courseId }: { courseId: number }) {
  const toast = useToast();
  const [submissions, setSubmissions] = useState<CncDrawingSubmission[]>([]);
  const [feedback, setFeedback] = useState<Record<number, string>>({});
  const [loading, setLoading] = useState(true);
  const [ready, setReady] = useState(true);
  const [reviewingId, setReviewingId] = useState<number | null>(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    fetchCncDrawingSubmissionsByCourse(courseId)
      .then((data) => {
        if (!cancelled) {
          setSubmissions(data);
          setFeedback(Object.fromEntries(data.map((item) => [item.id, item.teacher_feedback])));
          setReady(true);
        }
      })
      .catch(() => {
        if (!cancelled) setReady(false);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => { cancelled = true; };
  }, [courseId]);

  async function openDrawing(submission: CncDrawingSubmission) {
    try {
      const url = await createCncDrawingDownloadUrl(submission.storage_path);
      window.open(url, "_blank", "noopener,noreferrer");
    } catch (error) {
      toast("error", `Không mở được bản vẽ: ${error instanceof Error ? error.message : error}`);
    }
  }

  async function review(submission: CncDrawingSubmission, status: "approved" | "rejected") {
    if (status === "rejected" && !feedback[submission.id]?.trim()) {
      toast("error", "Hãy nhập yêu cầu chỉnh sửa trước khi yêu cầu sinh viên nộp lại.");
      return;
    }
    setReviewingId(submission.id);
    try {
      const updated = await reviewCncDrawingSubmission(submission.id, status, feedback[submission.id] ?? "");
      setSubmissions((current) => current.map((item) => item.id === updated.id ? { ...item, ...updated } : item));
      toast("success", status === "approved" ? "Đã duyệt bản vẽ và mở quyền gia công CNC cho sinh viên." : "Đã gửi yêu cầu chỉnh sửa bản vẽ.");
    } catch (error) {
      toast("error", `Không cập nhật được hồ sơ: ${error instanceof Error ? error.message : error}`);
    } finally {
      setReviewingId(null);
    }
  }

  const pendingCount = submissions.filter((item) => item.status === "pending").length;
  return <section className="rounded-2xl border border-emerald-500/25 bg-emerald-500/5 p-5">
    <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
      <div>
        <p className="text-xs font-bold tracking-wide text-emerald-300 uppercase">Duyệt trước khi gia công</p>
        <h3 className="mt-1 font-display text-lg font-bold text-white">Bản vẽ &amp; minh chứng mô phỏng CNC</h3>
        <p className="mt-1 text-xs leading-5 text-slate-400">Gồm bản vẽ trước khi gia công (Bài 5, Bài 6) và minh chứng mô phỏng Bài tập 5 của Lập trình tiện/phay. Chỉ hồ sơ được duyệt mới mở quyền tương ứng cho sinh viên.</p>
      </div>
      <span className="w-fit rounded-full bg-amber-500/15 px-3 py-1 text-xs font-bold text-amber-200">{pendingCount} hồ sơ chờ duyệt</span>
    </div>

    {!ready && !loading && <div className="mt-4 rounded-xl border border-amber-500/30 bg-amber-500/10 px-4 py-3 text-xs leading-5 text-amber-200">Chưa có bảng nộp bản vẽ. Hãy chạy migration <strong>supabase-migration-cnc-drawing-submissions.sql</strong>.</div>}
    <div className="mt-5 space-y-3">
      {loading ? <p className="text-xs text-slate-400">Đang tải hồ sơ bản vẽ…</p> : submissions.length === 0 ? <p className="rounded-xl border border-dashed border-white/10 px-4 py-6 text-center text-xs text-slate-500">Chưa có sinh viên nộp bản vẽ.</p> : submissions.map((submission) => {
        const machine = submission.lesson_id === "lesson-5" ? "Gia công tiện" : submission.lesson_id === "lesson-6" ? "Gia công phay" : submission.lesson_id === "lesson-2-simulation" ? "Mô phỏng tiện (BT5)" : submission.lesson_id === "lesson-3-simulation" ? "Mô phỏng phay (BT5)" : submission.lesson_id;
        return <article key={submission.id} className="rounded-xl border border-white/10 bg-[#080D1A] p-4">
          <div className="flex flex-col gap-3 md:flex-row md:items-start">
            <div className="min-w-0 flex-1">
              <div className="flex flex-wrap items-center gap-2">
                <strong className="text-sm text-white">{submission.profiles?.full_name || "Sinh viên"}</strong>
                <span className="rounded-full bg-white/5 px-2 py-0.5 text-[10px] text-slate-400">{submission.profiles?.class_name || "Chưa có lớp"}</span>
                <span className="rounded-full bg-blue-500/10 px-2 py-0.5 text-[10px] font-bold text-blue-200">{machine}</span>
                <span className={`rounded-full px-2 py-0.5 text-[10px] font-bold ${submission.status === "approved" ? "bg-emerald-500/15 text-emerald-200" : submission.status === "rejected" ? "bg-red-500/15 text-red-200" : "bg-amber-500/15 text-amber-200"}`}>{submission.status === "approved" ? "Đã duyệt" : submission.status === "rejected" ? "Yêu cầu nộp lại" : "Chờ duyệt"}</span>
              </div>
              <button type="button" onClick={() => openDrawing(submission)} className="mt-2 block max-w-full truncate text-left text-xs font-semibold text-[#60A5FA] hover:text-[#93C5FD]">Mở bản vẽ: {submission.file_name}</button>
              <p className="mt-1 text-[10px] text-slate-500">Cập nhật {new Date(submission.updated_at).toLocaleString("vi-VN")}</p>
            </div>
            <div className="flex gap-2">
              <button type="button" disabled={reviewingId === submission.id} onClick={() => review(submission, "approved")} className="rounded-lg bg-emerald-600 px-3 py-2 text-xs font-bold text-white hover:bg-emerald-500 disabled:opacity-50">Duyệt & mở khóa</button>
              <button type="button" disabled={reviewingId === submission.id} onClick={() => review(submission, "rejected")} className="rounded-lg border border-red-500/30 px-3 py-2 text-xs font-bold text-red-200 hover:bg-red-500/10 disabled:opacity-50">Yêu cầu nộp lại</button>
            </div>
          </div>
          <textarea value={feedback[submission.id] ?? ""} onChange={(event) => setFeedback((current) => ({ ...current, [submission.id]: event.target.value }))} rows={2} placeholder="Nhận xét của giảng viên hoặc yêu cầu chỉnh sửa…" className="mt-3 w-full rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-xs text-white placeholder:text-slate-500" />
        </article>;
      })}
    </div>
  </section>;
}
