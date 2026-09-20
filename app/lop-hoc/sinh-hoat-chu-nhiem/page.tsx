"use client";

import { useEffect, useMemo, useState } from "react";
import { CalendarDays, CheckCircle2, Circle, ClipboardList, Users } from "lucide-react";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import RequireAuth from "@/components/auth/RequireAuth";
import { useAuth } from "@/components/auth/AuthProvider";
import { supabaseConfigured } from "@/services/supabase";
import { fetchMyActiveCncCourse } from "@/services/course-enrollments";
import { HOMEROOM_SUBJECT_CODE } from "@/services/subjects";
import {
  fetchHomeroomMeetings,
  fetchMyHomeroomTaskCompletions,
  fetchMyHomeroomTasks,
  setHomeroomTaskDone,
  type HomeroomMeeting,
  type HomeroomTask,
  type HomeroomTaskCompletion,
} from "@/services/homeroom-meetings";

function errorMessage(error: unknown, fallback: string) {
  return error instanceof Error ? error.message : fallback;
}

function Dashboard() {
  const { session } = useAuth();
  const [course, setCourse] = useState<{ id: number; name: string; class_label: string } | null | undefined>(undefined);
  const [meetings, setMeetings] = useState<HomeroomMeeting[] | null>(null);
  const [tasks, setTasks] = useState<HomeroomTask[]>([]);
  const [completions, setCompletions] = useState<HomeroomTaskCompletion[]>([]);
  const [error, setError] = useState("");
  const [pendingTaskId, setPendingTaskId] = useState<number | null>(null);

  useEffect(() => {
    if (!session) return;
    fetchMyActiveCncCourse(session.user.id, HOMEROOM_SUBJECT_CODE)
      .then((enrollment) => setCourse(enrollment?.status === "active" ? enrollment.course : null))
      .catch(() => setCourse(null));
  }, [session]);

  useEffect(() => {
    if (!course || !session) return;
    Promise.all([
      fetchHomeroomMeetings(course.id),
      fetchMyHomeroomTasks(course.id, session.user.id),
      fetchMyHomeroomTaskCompletions(session.user.id),
    ])
      .then(([meetingRows, taskRows, completionRows]) => {
        setMeetings(meetingRows);
        setTasks(taskRows);
        setCompletions(completionRows);
      })
      .catch((cause) => setError(errorMessage(cause, "Không tải được biên bản sinh hoạt chủ nhiệm.")));
  }, [course, session]);

  const doneTaskIds = useMemo(() => new Set(completions.map((c) => c.task_id)), [completions]);

  async function toggleTask(task: HomeroomTask) {
    if (!session) return;
    const done = doneTaskIds.has(task.id);
    setPendingTaskId(task.id);
    try {
      await setHomeroomTaskDone(task.id, session.user.id, !done);
      setCompletions((current) =>
        done ? current.filter((c) => c.task_id !== task.id) : [...current, { task_id: task.id, student_id: session.user.id, done_at: new Date().toISOString() }],
      );
    } catch (cause) {
      setError(errorMessage(cause, "Không lưu được dấu tick."));
    } finally {
      setPendingTaskId(null);
    }
  }

  return (
    <div className="mx-auto w-full max-w-3xl px-6 pb-20 pt-28">
      <div className="flex items-center gap-3">
        <span className="flex h-11 w-11 items-center justify-center rounded-xl bg-violet-500/15 text-violet-300">
          <ClipboardList size={20} />
        </span>
        <div>
          <h1 className="font-display text-2xl font-bold text-white">Sinh hoạt chủ nhiệm</h1>
          <p className="text-sm text-slate-400">Nội dung sinh hoạt tuần và những việc em cần làm.</p>
        </div>
      </div>

      {error && <p className="mt-6 rounded-xl bg-red-500/10 p-3 text-sm text-red-200">{error}</p>}

      {course === undefined ? (
        <p className="mt-8 text-sm text-slate-400">Đang tải…</p>
      ) : course === null ? (
        <p className="mt-8 rounded-2xl border border-white/10 bg-[#0B1020] p-6 text-sm text-slate-400">
          Em chưa thuộc lớp chủ nhiệm nào, hoặc yêu cầu vào lớp đang chờ giáo viên duyệt.
        </p>
      ) : meetings === null ? (
        <p className="mt-8 text-sm text-slate-400">Đang tải…</p>
      ) : meetings.length === 0 ? (
        <p className="mt-8 rounded-2xl border border-white/10 bg-[#0B1020] p-6 text-sm text-slate-400">Chưa có biên bản sinh hoạt tuần nào.</p>
      ) : (
        <div className="mt-8 space-y-4">
          {meetings.map((meeting) => {
            const meetingTasks = tasks.filter((t) => t.meeting_id === meeting.id);
            return (
              <section key={meeting.id} className="rounded-2xl border border-white/10 bg-[#0B1020] p-5">
                <div className="flex items-center gap-2 text-sm font-bold text-white">
                  <CalendarDays size={16} className="text-violet-300" />
                  {meeting.week_label}
                </div>
                <p className="mt-0.5 text-xs text-slate-500">{new Date(meeting.meeting_date).toLocaleDateString("vi-VN")}</p>
                {meeting.content && <p className="mt-3 whitespace-pre-line text-sm text-slate-300">{meeting.content}</p>}

                {meetingTasks.length > 0 && (
                  <ul className="mt-4 space-y-2">
                    {meetingTasks.map((task) => {
                      const done = doneTaskIds.has(task.id);
                      return (
                        <li key={task.id}>
                          <button
                            type="button"
                            onClick={() => toggleTask(task)}
                            disabled={pendingTaskId === task.id}
                            className={`flex w-full items-center gap-3 rounded-xl border px-4 py-3 text-left transition disabled:opacity-50 ${
                              done ? "border-emerald-400/30 bg-emerald-500/[.06]" : "border-white/10 hover:border-white/25"
                            }`}
                          >
                            {done ? <CheckCircle2 size={18} className="shrink-0 text-emerald-300" /> : <Circle size={18} className="shrink-0 text-slate-500" />}
                            <span className="min-w-0 flex-1">
                              <span className={`block text-sm ${done ? "text-emerald-100 line-through decoration-emerald-400/40" : "text-white"}`}>{task.title}</span>
                              {!task.student_id && (
                                <span className="mt-0.5 flex items-center gap-1 text-xs text-slate-500">
                                  <Users size={11} />Việc chung cả lớp
                                </span>
                              )}
                            </span>
                          </button>
                        </li>
                      );
                    })}
                  </ul>
                )}
              </section>
            );
          })}
        </div>
      )}
    </div>
  );
}

export default function SinhHoatChuNhiemPage() {
  return (
    <>
      <Navbar />
      <main className="min-h-screen w-full">
        {!supabaseConfigured ? (
          <p className="pt-28 text-center text-slate-400">Hệ thống đang được cấu hình.</p>
        ) : (
          <RequireAuth>
            <Dashboard />
          </RequireAuth>
        )}
      </main>
      <Footer />
    </>
  );
}
