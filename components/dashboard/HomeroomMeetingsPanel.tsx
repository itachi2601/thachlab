"use client";

import { useEffect, useMemo, useState } from "react";
import { CalendarDays, CheckCircle2, ClipboardList, Plus, Trash2, User, Users } from "lucide-react";
import { useToast } from "@/components/ui/Toast";
import {
  createHomeroomMeeting,
  createHomeroomTask,
  deleteHomeroomMeeting,
  deleteHomeroomTask,
  fetchHomeroomMeetings,
  fetchHomeroomTaskCompletions,
  fetchHomeroomTasks,
  updateHomeroomMeeting,
  type HomeroomMeeting,
  type HomeroomTask,
  type HomeroomTaskCompletion,
} from "@/services/homeroom-meetings";

type Student = { id: string; name: string; className: string };

function errorMessage(error: unknown, fallback: string) {
  return error instanceof Error ? error.message : fallback;
}

function isoToday() {
  return new Date().toISOString().slice(0, 10);
}

export default function HomeroomMeetingsPanel({ courseId, students }: { courseId: number; students: Student[] }) {
  const toast = useToast();
  const [meetings, setMeetings] = useState<HomeroomMeeting[]>([]);
  const [tasks, setTasks] = useState<HomeroomTask[]>([]);
  const [completions, setCompletions] = useState<HomeroomTaskCompletion[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [creating, setCreating] = useState(false);
  const [weekLabel, setWeekLabel] = useState("");
  const [meetingDate, setMeetingDate] = useState(isoToday());
  const [content, setContent] = useState("");
  const [busy, setBusy] = useState(false);

  const studentById = useMemo(() => new Map(students.map((s) => [s.id, s])), [students]);

  function reload() {
    setLoading(true);
    Promise.all([fetchHomeroomMeetings(courseId), fetchHomeroomTasks(courseId), fetchHomeroomTaskCompletions(courseId)])
      .then(([meetingRows, taskRows, completionRows]) => {
        setMeetings(meetingRows);
        setTasks(taskRows);
        setCompletions(completionRows);
        setError("");
      })
      .catch((cause) => setError(errorMessage(cause, "Không tải được biên bản SHCN.")))
      .finally(() => setLoading(false));
  }

  useEffect(reload, [courseId]);

  async function handleCreateMeeting() {
    if (!weekLabel.trim()) {
      toast("error", "Nhập tên tuần (ví dụ: Tuần 3 · 15/09 – 21/09).");
      return;
    }
    setBusy(true);
    try {
      const created = await createHomeroomMeeting({ courseId, weekLabel: weekLabel.trim(), meetingDate, content });
      setMeetings((current) => [created, ...current]);
      setWeekLabel("");
      setContent("");
      setMeetingDate(isoToday());
      setCreating(false);
      toast("success", "Đã tạo biên bản tuần.");
    } catch (cause) {
      toast("error", errorMessage(cause, "Không tạo được biên bản."));
    } finally {
      setBusy(false);
    }
  }

  async function handleDeleteMeeting(meetingId: number) {
    if (!window.confirm("Xóa biên bản tuần này? Toàn bộ việc và dấu tick trong tuần cũng bị xóa.")) return;
    try {
      await deleteHomeroomMeeting(meetingId);
      setMeetings((current) => current.filter((m) => m.id !== meetingId));
      setTasks((current) => current.filter((t) => t.meeting_id !== meetingId));
    } catch (cause) {
      toast("error", errorMessage(cause, "Không xóa được biên bản."));
    }
  }

  async function handleSaveContent(meeting: HomeroomMeeting, value: string) {
    if (value === meeting.content) return;
    try {
      await updateHomeroomMeeting(meeting.id, { content: value });
      setMeetings((current) => current.map((m) => (m.id === meeting.id ? { ...m, content: value } : m)));
    } catch (cause) {
      toast("error", errorMessage(cause, "Không lưu được nội dung."));
    }
  }

  return (
    <div className="space-y-5">
      <section className="rounded-2xl border border-violet-400/15 bg-gradient-to-r from-violet-500/10 to-transparent p-5">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <ClipboardList size={20} className="text-violet-300" />
            <h3 className="font-display text-xl font-bold text-white">Biên bản sinh hoạt chủ nhiệm</h3>
          </div>
          <button onClick={() => setCreating((v) => !v)} className="inline-flex items-center gap-2 rounded-xl bg-violet-600 px-4 py-2.5 text-sm font-bold text-white">
            <Plus size={16} />Thêm biên bản tuần
          </button>
        </div>
        <p className="mt-2 text-sm text-slate-400">
          Ghi nội dung sinh hoạt tuần và giao việc — việc chung cho cả lớp hoặc riêng từng sinh viên. Sinh viên xem và tự tick đã làm ở trang lớp học của các em.
        </p>
        {error && <p className="mt-3 rounded-xl bg-red-500/10 p-3 text-sm text-red-200">{error}</p>}

        {creating && (
          <div className="mt-4 space-y-3 rounded-2xl border border-violet-400/20 bg-violet-500/5 p-4">
            <div className="grid gap-3 sm:grid-cols-[1fr_auto]">
              <input value={weekLabel} onChange={(e) => setWeekLabel(e.target.value)} placeholder="Ví dụ: Tuần 3 · 15/09 – 21/09" className="rounded-xl border border-white/10 bg-[#080d1d] px-4 py-3 text-sm text-white placeholder:text-slate-500" />
              <input type="date" value={meetingDate} onChange={(e) => setMeetingDate(e.target.value)} className="rounded-xl border border-white/10 bg-[#080d1d] px-4 py-3 text-sm text-white" />
            </div>
            <textarea value={content} onChange={(e) => setContent(e.target.value)} rows={4} placeholder="Nội dung sinh hoạt tuần: thông báo, nhận xét chung, kế hoạch tuần tới…" className="w-full resize-none rounded-xl border border-white/10 bg-[#080d1d] px-4 py-3 text-sm text-white placeholder:text-slate-500" />
            <button disabled={busy} onClick={handleCreateMeeting} className="rounded-xl bg-violet-600 px-5 py-2.5 text-sm font-bold text-white disabled:opacity-40">
              {busy ? "Đang tạo…" : "Tạo biên bản"}
            </button>
          </div>
        )}
      </section>

      {loading ? (
        <p className="text-sm text-slate-400">Đang tải…</p>
      ) : meetings.length === 0 ? (
        <p className="rounded-2xl border border-dashed border-white/10 p-8 text-center text-sm text-slate-500">Chưa có biên bản tuần nào.</p>
      ) : (
        <div className="space-y-4">
          {meetings.map((meeting) => (
            <MeetingCard
              key={meeting.id}
              meeting={meeting}
              tasks={tasks.filter((t) => t.meeting_id === meeting.id)}
              completions={completions}
              students={students}
              studentById={studentById}
              onDelete={() => handleDeleteMeeting(meeting.id)}
              onSaveContent={(value) => handleSaveContent(meeting, value)}
              onTaskCreated={(task) => setTasks((current) => [...current, task])}
              onTaskDeleted={(taskId) => setTasks((current) => current.filter((t) => t.id !== taskId))}
            />
          ))}
        </div>
      )}
    </div>
  );
}

function MeetingCard({
  meeting,
  tasks,
  completions,
  students,
  studentById,
  onDelete,
  onSaveContent,
  onTaskCreated,
  onTaskDeleted,
}: {
  meeting: HomeroomMeeting;
  tasks: HomeroomTask[];
  completions: HomeroomTaskCompletion[];
  students: Student[];
  studentById: Map<string, Student>;
  onDelete: () => void;
  onSaveContent: (value: string) => void;
  onTaskCreated: (task: HomeroomTask) => void;
  onTaskDeleted: (taskId: number) => void;
}) {
  const toast = useToast();
  const [addingTask, setAddingTask] = useState(false);
  const [taskTitle, setTaskTitle] = useState("");
  const [taskScope, setTaskScope] = useState<"class" | string>("class");
  const [busy, setBusy] = useState(false);

  async function handleAddTask() {
    if (!taskTitle.trim()) {
      toast("error", "Nhập nội dung việc cần làm.");
      return;
    }
    setBusy(true);
    try {
      const task = await createHomeroomTask({
        meetingId: meeting.id,
        courseId: meeting.course_id,
        studentId: taskScope === "class" ? null : taskScope,
        title: taskTitle.trim(),
      });
      onTaskCreated(task);
      setTaskTitle("");
      setTaskScope("class");
      setAddingTask(false);
    } catch (cause) {
      toast("error", errorMessage(cause, "Không thêm được việc."));
    } finally {
      setBusy(false);
    }
  }

  async function handleDeleteTask(taskId: number) {
    try {
      await deleteHomeroomTask(taskId);
      onTaskDeleted(taskId);
    } catch (cause) {
      toast("error", errorMessage(cause, "Không xóa được việc."));
    }
  }

  return (
    <section className="rounded-2xl border border-white/10 bg-[#0B1020] p-5">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <div className="flex items-center gap-2 text-sm font-bold text-white">
            <CalendarDays size={16} className="text-violet-300" />
            {meeting.week_label}
          </div>
          <p className="mt-0.5 text-xs text-slate-500">{new Date(meeting.meeting_date).toLocaleDateString("vi-VN")}</p>
        </div>
        <button onClick={onDelete} className="inline-flex items-center gap-1.5 rounded-full border border-red-400/25 px-3 py-1.5 text-xs font-bold text-red-300 hover:bg-red-500/10">
          <Trash2 size={13} />Xóa
        </button>
      </div>

      <textarea
        defaultValue={meeting.content}
        onBlur={(e) => onSaveContent(e.currentTarget.value)}
        rows={3}
        placeholder="Nội dung sinh hoạt tuần…"
        className="mt-3 w-full resize-none rounded-xl border border-white/10 bg-black/20 px-3 py-2.5 text-sm text-slate-200 placeholder:text-slate-500 focus:outline-none"
      />

      <div className="mt-4 space-y-2">
        {tasks.map((task) => {
          const scopeStudent = task.student_id ? studentById.get(task.student_id) : null;
          const doneCount = completions.filter((c) => c.task_id === task.id).length;
          const doneForStudent = task.student_id ? doneCount > 0 : false;
          return (
            <div key={task.id} className="flex items-center gap-3 rounded-xl border border-white/10 bg-white/[.02] px-3 py-2.5">
              <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-white/5 text-slate-400">
                {task.student_id ? <User size={14} /> : <Users size={14} />}
              </span>
              <span className="min-w-0 flex-1">
                <span className="block text-sm text-white">{task.title}</span>
                <span className="text-xs text-slate-500">{task.student_id ? scopeStudent?.name ?? "Sinh viên" : "Cả lớp"}</span>
              </span>
              {task.student_id ? (
                <span className={`flex items-center gap-1 text-xs font-bold ${doneForStudent ? "text-emerald-300" : "text-slate-500"}`}>
                  <CheckCircle2 size={14} />{doneForStudent ? "Đã làm" : "Chưa làm"}
                </span>
              ) : (
                <span className="text-xs font-bold text-slate-400">{doneCount}/{students.length} đã làm</span>
              )}
              <button onClick={() => handleDeleteTask(task.id)} aria-label="Xóa việc" className="text-slate-500 hover:text-red-300">
                <Trash2 size={14} />
              </button>
            </div>
          );
        })}
        {!tasks.length && !addingTask && <p className="text-xs text-slate-500">Chưa có việc nào trong tuần này.</p>}
      </div>

      {addingTask ? (
        <div className="mt-3 grid gap-2 rounded-xl border border-white/10 bg-black/20 p-3 sm:grid-cols-[1fr_auto_auto]">
          <input value={taskTitle} onChange={(e) => setTaskTitle(e.target.value)} placeholder="Nội dung việc cần làm…" className="rounded-lg border border-white/10 bg-[#080d1d] px-3 py-2 text-sm text-white placeholder:text-slate-500" />
          <select value={taskScope} onChange={(e) => setTaskScope(e.target.value)} className="rounded-lg border border-white/10 bg-[#080d1d] px-3 py-2 text-sm text-white">
            <option value="class">Cả lớp</option>
            {students.map((s) => (
              <option key={s.id} value={s.id}>{s.name}</option>
            ))}
          </select>
          <button disabled={busy} onClick={handleAddTask} className="rounded-lg bg-violet-600 px-4 py-2 text-sm font-bold text-white disabled:opacity-40">Thêm</button>
        </div>
      ) : (
        <button onClick={() => setAddingTask(true)} className="mt-3 inline-flex items-center gap-1.5 text-xs font-bold text-violet-300 hover:text-violet-200">
          <Plus size={13} />Thêm việc cần làm
        </button>
      )}
    </section>
  );
}
