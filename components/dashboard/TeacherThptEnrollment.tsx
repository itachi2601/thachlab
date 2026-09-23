"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { CalendarDays, Check, ChevronDown, Eye, EyeOff, Link2, Plus, Trash2, UserCheck, UserX, X } from "lucide-react";
import { useToast } from "@/components/ui/Toast";
import { SITE_URL } from "@/lib/site";
import { currentSchoolYear } from "@/components/dashboard/CreateCourseForm";
import { classGrade, fetchUnassignedStudents, type ClassStudent, type UnassignedStudent } from "@/services/classes";
import { fetchQuestionTopics, lessonTopics, type QuestionTopic } from "@/services/analytics";
import {
  attachStudent,
  createCourse,
  deleteCourse,
  fetchCoursesForClass,
  fetchRegistrationsForCourse,
  formatDate,
  formatSchedule,
  PAYMENT_STATUS_LABEL,
  REGISTRATION_STATUS_LABEL,
  replaceSchedules,
  reviewRegistration,
  setPayment,
  updateCourse,
  WEEKDAY_LABEL,
  type CourseSchedule,
  type PaymentStatus,
  type Registration,
  type ThptCourse,
} from "@/services/thpt-courses";

function errorMessage(error: unknown, fallback: string) {
  return error instanceof Error ? error.message : fallback;
}

const inputCls =
  "rounded-lg border border-white/10 bg-panel-deep px-3 py-2 text-sm text-white placeholder:text-slate-500 focus:border-primary focus:outline-none";

const EMPTY_SLOT: CourseSchedule = { weekday: 1, start_time: "18:00", end_time: "19:30", location: "" };

// ---------- Lịch tuần ----------
function ScheduleEditor({ value, onChange }: { value: CourseSchedule[]; onChange: (v: CourseSchedule[]) => void }) {
  const update = (i: number, patch: Partial<CourseSchedule>) =>
    onChange(value.map((s, idx) => (idx === i ? { ...s, ...patch } : s)));
  return (
    <div className="space-y-2">
      {value.map((s, i) => (
        <div key={i} className="flex flex-wrap items-center gap-2">
          <select value={s.weekday} onChange={(e) => update(i, { weekday: Number(e.target.value) })} className={inputCls}>
            {Object.entries(WEEKDAY_LABEL).map(([d, label]) => (
              <option key={d} value={d}>{label}</option>
            ))}
          </select>
          <input type="time" value={s.start_time} onChange={(e) => update(i, { start_time: e.target.value })} className={inputCls} aria-label="Bắt đầu" />
          <span className="text-slate-500">–</span>
          <input type="time" value={s.end_time} onChange={(e) => update(i, { end_time: e.target.value })} className={inputCls} aria-label="Kết thúc" />
          <input value={s.location} onChange={(e) => update(i, { location: e.target.value })} placeholder="Phòng / địa điểm" className={`${inputCls} min-w-0 flex-1`} />
          <button type="button" onClick={() => onChange(value.filter((_, idx) => idx !== i))} className="rounded-lg border border-red-500/30 p-1.5 text-red-300 hover:bg-red-500/10" title="Bỏ buổi">
            <X size={14} />
          </button>
        </div>
      ))}
      <button type="button" onClick={() => onChange([...value, { ...EMPTY_SLOT }])} className="inline-flex items-center gap-1.5 text-xs font-semibold text-blue-300 hover:underline">
        <Plus size={13} /> Thêm buổi trong tuần
      </button>
    </div>
  );
}

// ---------- Tạo khoá ----------
function CreateThptCourseForm({ classId, className, onCreated }: { classId: number; className: string; onCreated: () => void }) {
  const toast = useToast();
  const [open, setOpen] = useState(false);
  const [busy, setBusy] = useState(false);
  const [form, setForm] = useState({
    name: `Vật lí ${className}`, description: "", school_year: currentSchoolYear(), starts_at: "", ends_at: "",
    capacity: "", fee_note: "Học phí đóng tại trung tâm", is_public: true,
  });
  const [schedules, setSchedules] = useState<CourseSchedule[]>([{ ...EMPTY_SLOT }]);

  async function submit() {
    if (!form.name.trim()) { toast("error", "Nhập tên lớp."); return; }
    setBusy(true);
    try {
      await createCourse(
        {
          class_id: classId, name: form.name.trim(), description: form.description.trim(), school_year: form.school_year.trim(),
          starts_at: form.starts_at || null, ends_at: form.ends_at || null,
          capacity: form.capacity ? Number(form.capacity) : null, fee_note: form.fee_note.trim(),
          is_public: form.is_public, status: "active",
        },
        schedules,
      );
      toast("success", "Đã tạo lớp. Phụ huynh thấy ngay ở trang Đăng ký học.");
      setOpen(false);
      onCreated();
    } catch (error) {
      toast("error", errorMessage(error, "Chưa tạo được lớp."));
    } finally {
      setBusy(false);
    }
  }

  return (
    <>
      <button onClick={() => setOpen((v) => !v)} className="flex items-center gap-2 rounded-full bg-blue-600 px-4 py-2 text-sm font-bold text-white">
        <Plus size={15} /> Mở lớp mới cho khối {className}
      </button>
      {open && (
        <div className="mt-4 grid gap-3 rounded-2xl border border-blue-400/20 bg-blue-500/5 p-4">
          <div className="grid gap-3 md:grid-cols-2">
            <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} placeholder="Tên lớp: Vật lí 12 — ca tối T2/T5" className={inputCls} />
            <input value={form.school_year} onChange={(e) => setForm({ ...form, school_year: e.target.value })} placeholder="Năm học" className={inputCls} />
            <label className="text-xs text-slate-400">Khai giảng
              <input type="date" value={form.starts_at} onChange={(e) => setForm({ ...form, starts_at: e.target.value })} className={`${inputCls} mt-1 w-full`} />
            </label>
            <label className="text-xs text-slate-400">Kết thúc (dự kiến)
              <input type="date" value={form.ends_at} onChange={(e) => setForm({ ...form, ends_at: e.target.value })} className={`${inputCls} mt-1 w-full`} />
            </label>
            <input type="number" min={1} value={form.capacity} onChange={(e) => setForm({ ...form, capacity: e.target.value })} placeholder="Sĩ số tối đa (bỏ trống = không giới hạn)" className={inputCls} />
            <input value={form.fee_note} onChange={(e) => setForm({ ...form, fee_note: e.target.value })} placeholder="Ghi chú học phí" className={inputCls} />
          </div>
          <textarea value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} placeholder="Mô tả ngắn cho phụ huynh (nội dung, mục tiêu…)" rows={2} className={inputCls} />
          <div>
            <p className="mb-2 text-xs font-bold uppercase tracking-wide text-slate-400">Lịch tuần</p>
            <ScheduleEditor value={schedules} onChange={setSchedules} />
          </div>
          <label className="flex items-center gap-2 text-sm text-slate-300">
            <input type="checkbox" checked={form.is_public} onChange={(e) => setForm({ ...form, is_public: e.target.checked })} />
            Hiện trên trang Đăng ký học (công khai)
          </label>
          <div className="flex gap-2">
            <button disabled={busy} onClick={submit} className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-bold text-white disabled:opacity-40">
              {busy ? "Đang tạo…" : "Lưu lớp"}
            </button>
            <button onClick={() => setOpen(false)} className="rounded-lg border border-white/10 px-4 py-2 text-sm text-slate-300">Huỷ</button>
          </div>
        </div>
      )}
    </>
  );
}

// ---------- Gắn tài khoản cho đăng ký chưa có student ----------
function AttachPicker({ registration, students, onDone }: { registration: Registration; students: (ClassStudent | UnassignedStudent)[]; onDone: () => void }) {
  const toast = useToast();
  const [pick, setPick] = useState("");
  const [busy, setBusy] = useState(false);
  async function attach() {
    if (!pick) return;
    setBusy(true);
    try {
      await attachStudent(registration.id, pick);
      toast("success", "Đã gắn tài khoản — giờ duyệt được.");
      onDone();
    } catch (error) {
      toast("error", errorMessage(error, "Chưa gắn được."));
    } finally {
      setBusy(false);
    }
  }
  return (
    <div className="mt-2 flex flex-wrap items-center gap-2">
      <select value={pick} onChange={(e) => setPick(e.target.value)} className={inputCls}>
        <option value="">Gắn tài khoản học sinh…</option>
        {students.map((s) => (
          <option key={s.id} value={s.id}>{s.full_name}</option>
        ))}
      </select>
      <button type="button" disabled={!pick || busy} onClick={attach} className="inline-flex items-center gap-1.5 rounded-lg border border-blue-400/30 px-3 py-2 text-xs font-bold text-blue-200 disabled:opacity-40">
        <Link2 size={13} /> Gắn
      </button>
    </div>
  );
}

// ---------- Một khoá + danh sách đăng ký ----------
function CourseBlock({ course, students, topics, onChanged }: { course: ThptCourse; students: ClassStudent[]; topics: QuestionTopic[]; onChanged: () => void }) {
  const toast = useToast();
  const topicName = useMemo(() => new Map(topics.map((t) => [t.id, t.name])), [topics]);

  async function setCurrentTopic(id: number | null) {
    try {
      await updateCourse(course.id, { current_topic_id: id });
      toast("success", id ? "Đã ghi mốc lớp đang dạy tới." : "Đã bỏ mốc.");
      onChanged();
    } catch (error) {
      toast("error", errorMessage(error, "Chưa lưu được."));
    }
  }
  const [open, setOpen] = useState(true);
  const [regs, setRegs] = useState<Registration[] | null>(null);
  const [editingSchedule, setEditingSchedule] = useState(false);
  const [schedules, setSchedules] = useState<CourseSchedule[]>(course.schedules);
  const [unassigned, setUnassigned] = useState<UnassignedStudent[]>([]);

  const reload = useCallback(() => {
    fetchRegistrationsForCourse(course.id).then(setRegs).catch(() => setRegs([]));
  }, [course.id]);

  useEffect(() => { reload(); }, [reload]);

  const needsAttach = (regs ?? []).some((r) => r.student_id === null);
  useEffect(() => {
    if (!needsAttach) return;
    fetchUnassignedStudents().then(setUnassigned).catch(() => setUnassigned([]));
  }, [needsAttach]);

  async function review(r: Registration, status: "active" | "rejected" | "left" | "pending") {
    try {
      await reviewRegistration(r.id, status);
      toast("success", status === "active" ? `${r.studentName} đã vào lớp.` : "Đã cập nhật.");
      reload();
      onChanged();
    } catch (error) {
      toast("error", errorMessage(error, "Chưa cập nhật được."));
    }
  }

  async function pay(r: Registration, payment_status: PaymentStatus) {
    try {
      await setPayment(r.id, payment_status, r.payment_note);
      reload();
    } catch (error) {
      toast("error", errorMessage(error, "Chưa lưu được."));
    }
  }

  async function togglePublic() {
    try {
      await updateCourse(course.id, { is_public: !course.is_public });
      onChanged();
    } catch (error) {
      toast("error", errorMessage(error, "Chưa lưu được."));
    }
  }

  async function setStatus(status: ThptCourse["status"]) {
    try {
      await updateCourse(course.id, { status });
      onChanged();
    } catch (error) {
      toast("error", errorMessage(error, "Chưa lưu được."));
    }
  }

  async function saveSchedules() {
    try {
      await replaceSchedules(course.id, schedules);
      setEditingSchedule(false);
      toast("success", "Đã lưu lịch.");
      onChanged();
    } catch (error) {
      toast("error", errorMessage(error, "Chưa lưu được lịch."));
    }
  }

  async function remove() {
    if (!window.confirm(`Xoá lớp "${course.name}" và toàn bộ đăng ký của lớp? Học sinh đã vào khối vẫn giữ nguyên.`)) return;
    try {
      await deleteCourse(course.id);
      onChanged();
    } catch (error) {
      toast("error", errorMessage(error, "Chưa xoá được."));
    }
  }

  const attachable = useMemo(() => {
    const seen = new Set<string>();
    const out: (ClassStudent | UnassignedStudent)[] = [];
    for (const s of [...unassigned, ...students]) {
      if (seen.has(s.id)) continue;
      seen.add(s.id);
      out.push(s);
    }
    return out.sort((a, b) => a.full_name.localeCompare(b.full_name, "vi"));
  }, [unassigned, students]);

  const pending = (regs ?? []).filter((r) => r.status === "pending");
  const catchup = (regs ?? []).filter((r) => r.status === "catchup");
  const active = (regs ?? []).filter((r) => r.status === "active");
  const others = (regs ?? []).filter((r) => r.status === "rejected" || r.status === "left");
  const publicLink = `${SITE_URL}/khoa-hoc/dang-ky/?id=${course.id}`;

  return (
    <section className="rounded-2xl border border-white/10 bg-panel p-5">
      <div className="flex flex-wrap items-start gap-3">
        <button type="button" onClick={() => setOpen((v) => !v)} className="flex min-w-0 flex-1 items-start gap-3 text-left">
          <ChevronDown size={18} className={`mt-1 shrink-0 text-slate-500 transition-transform ${open ? "" : "-rotate-90"}`} />
          <span className="min-w-0">
            <span className="block font-display text-lg font-bold text-white">{course.name}</span>
            <span className="block text-xs text-slate-400">
              {course.school_year}
              {course.starts_at ? ` · khai giảng ${formatDate(course.starts_at)}` : ""}
              {course.capacity !== null ? ` · ${course.taken}/${course.capacity} chỗ` : ` · ${course.taken} đăng ký`}
              {" · "}
              <span className={course.status === "active" ? "text-emerald-300" : "text-slate-500"}>
                {course.status === "active" ? "đang mở" : course.status === "draft" ? "nháp" : course.status === "completed" ? "đã kết thúc" : "lưu trữ"}
              </span>
            </span>
          </span>
        </button>
        <div className="flex flex-wrap gap-1.5">
          <button type="button" onClick={togglePublic} title={course.is_public ? "Đang hiện công khai — bấm để ẩn" : "Đang ẩn — bấm để hiện"} className={`rounded-lg border p-1.5 ${course.is_public ? "border-emerald-500/30 text-emerald-300" : "border-white/10 text-slate-400"}`}>
            {course.is_public ? <Eye size={15} /> : <EyeOff size={15} />}
          </button>
          <button type="button" onClick={() => navigator.clipboard.writeText(publicLink).then(() => toast("success", "Đã chép link đăng ký.")).catch(() => toast("error", "Không chép được."))} title="Chép link đăng ký" className="rounded-lg border border-white/10 p-1.5 text-slate-300">
            <Link2 size={15} />
          </button>
          {course.status === "active" ? (
            <button type="button" onClick={() => setStatus("completed")} className="rounded-lg border border-white/10 px-2.5 py-1.5 text-xs text-slate-300">Kết thúc</button>
          ) : (
            <button type="button" onClick={() => setStatus("active")} className="rounded-lg border border-emerald-500/30 px-2.5 py-1.5 text-xs text-emerald-200">Mở lại</button>
          )}
          <button type="button" onClick={remove} title="Xoá lớp" className="rounded-lg border border-red-500/30 p-1.5 text-red-300 hover:bg-red-500/10">
            <Trash2 size={15} />
          </button>
        </div>
      </div>

      {open && (
        <div className="mt-4 space-y-4">
          <div className="rounded-xl bg-white/[.02] p-3">
            <div className="flex items-center justify-between">
              <p className="flex items-center gap-1.5 text-xs font-bold uppercase tracking-wide text-slate-400"><CalendarDays size={13} /> Lịch tuần</p>
              {!editingSchedule && (
                <button type="button" onClick={() => { setSchedules(course.schedules); setEditingSchedule(true); }} className="text-xs font-semibold text-blue-300 hover:underline">Sửa lịch</button>
              )}
            </div>
            {editingSchedule ? (
              <div className="mt-2 space-y-2">
                <ScheduleEditor value={schedules} onChange={setSchedules} />
                <div className="flex gap-2">
                  <button type="button" onClick={saveSchedules} className="rounded-lg bg-blue-600 px-3 py-1.5 text-xs font-bold text-white">Lưu lịch</button>
                  <button type="button" onClick={() => setEditingSchedule(false)} className="rounded-lg border border-white/10 px-3 py-1.5 text-xs text-slate-300">Huỷ</button>
                </div>
              </div>
            ) : course.schedules.length === 0 ? (
              <p className="mt-1 text-sm text-slate-500">Chưa có lịch.</p>
            ) : (
              <ul className="mt-1 text-sm text-slate-300">
                {course.schedules.map((s) => <li key={`${s.weekday}-${s.start_time}`}>{formatSchedule(s)}</li>)}
              </ul>
            )}
          </div>

          <div className="rounded-xl bg-white/[.02] p-3">
            <p className="text-xs font-bold uppercase tracking-wide text-slate-400">Lớp đang dạy tới bài</p>
            <select
              value={course.current_topic_id ?? ""}
              onChange={(e) => setCurrentTopic(e.target.value ? Number(e.target.value) : null)}
              className={`${inputCls} mt-2 w-full max-w-md`}
            >
              <option value="">— chưa đặt (em vào trễ sẽ không có danh sách bù) —</option>
              {topics.map((t) => (
                <option key={t.id} value={t.id}>{t.name}</option>
              ))}
            </select>
            <p className="mt-1 text-xs text-slate-500">
              Mọi bài từ đầu tới mốc này là phần em vào trễ phải bù (trừ bài em đã học nơi khác). Cập nhật mỗi khi qua bài mới.
            </p>
          </div>

          {regs === null ? (
            <p className="text-sm text-slate-500">Đang tải đăng ký…</p>
          ) : regs.length === 0 ? (
            <p className="text-sm text-slate-500">Chưa có đăng ký nào. Gửi link đăng ký (nút chép link phía trên) cho phụ huynh.</p>
          ) : (
            <>
              {pending.length > 0 && (
                <div>
                  <h4 className="mb-2 text-xs font-bold uppercase tracking-wide text-amber-300">Chờ duyệt · {pending.length}</h4>
                  <ul className="space-y-2">
                    {pending.map((r) => (
                      <li key={r.id} className="rounded-xl border border-amber-500/20 bg-amber-500/[.04] p-3 text-sm">
                        <div className="flex flex-wrap items-center gap-2">
                          <strong className="text-white">{r.studentName}</strong>
                          {r.student_id === null && <span className="rounded-full bg-white/10 px-2 py-0.5 text-[10px] font-bold text-slate-300">chưa có tài khoản</span>}
                          {r.joined_late && <span className="rounded-full bg-amber-500/20 px-2 py-0.5 text-[10px] font-bold text-amber-200">vào trễ · cần bù bài</span>}
                          <span className="rounded-full border border-current px-2 py-0.5 text-[10px] font-bold text-amber-200">{REGISTRATION_STATUS_LABEL[r.status]}</span>
                          <span className="ml-auto text-xs text-slate-500">{new Date(r.created_at).toLocaleDateString("vi-VN")}</span>
                        </div>
                        <p className="mt-1 text-xs text-slate-400">
                          {r.registrantName && r.registered_by !== r.student_id ? `Đăng ký bởi ${r.registrantName}` : "Tự đăng ký"}
                          {r.contact ? ` · ${r.contact}` : ""}
                          {r.note ? ` · "${r.note}"` : ""}
                        </p>
                        {r.joined_late && (
                          <p className="mt-1 text-xs text-slate-400">
                            {r.catchup_topic_ids.length > 0
                              ? `Cần bù ${r.catchup_topic_ids.length} bài: ${r.catchup_topic_ids.map((id) => topicName.get(id) ?? `#${id}`).join(" → ")}`
                              : course.current_topic_id
                                ? "Không còn bài phải bù (đã học hết ở nơi khác) — duyệt là vào lớp."
                                : "Chưa đặt mốc “Lớp đang dạy tới bài” nên chưa tính được phần bù — đặt mốc rồi duyệt."}
                          </p>
                        )}
                        {r.student_id === null ? (
                          <AttachPicker registration={r} students={attachable} onDone={reload} />
                        ) : (
                          <div className="mt-2 flex flex-wrap gap-2">
                            <button type="button" onClick={() => review(r, "active")} className="inline-flex items-center gap-1.5 rounded-lg bg-emerald-600 px-3 py-1.5 text-xs font-bold text-white"><UserCheck size={13} /> {r.joined_late && r.catchup_topic_ids.length > 0 ? "Duyệt · bù bài trước" : "Duyệt vào lớp"}</button>
                            <button type="button" onClick={() => review(r, "rejected")} className="inline-flex items-center gap-1.5 rounded-lg border border-red-500/30 px-3 py-1.5 text-xs font-bold text-red-300"><UserX size={13} /> Từ chối</button>
                          </div>
                        )}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {catchup.length > 0 && (
                <div>
                  <h4 className="mb-2 text-xs font-bold uppercase tracking-wide text-blue-300">Đang bù bài · {catchup.length}</h4>
                  <ul className="space-y-2">
                    {catchup.map((r) => (
                      <li key={r.id} className="rounded-xl border border-blue-500/20 bg-blue-500/[.04] p-3 text-sm">
                        <div className="flex flex-wrap items-center gap-2">
                          <strong className="text-white">{r.studentName}</strong>
                          <span className="text-xs text-slate-400">
                            đã bù {r.catchup_done_topic_ids.length} · còn {r.catchup_topic_ids.length}
                          </span>
                          <button type="button" onClick={() => review(r, "active")} className="ml-auto inline-flex items-center gap-1.5 rounded-lg bg-emerald-600 px-3 py-1.5 text-xs font-bold text-white"><Check size={13} /> Xong bù bài · vào lớp</button>
                        </div>
                        <p className="mt-1 text-xs text-slate-400">
                          Kế tiếp: {r.catchup_topic_ids.map((id) => topicName.get(id) ?? `#${id}`).join(" → ") || "—"}
                        </p>
                        <p className="mt-0.5 text-xs text-slate-500">
                          Trợ giảng ghi buổi phụ đạo đúng bài là tự gạch; hết danh sách tự chuyển sang “Đã vào lớp”.
                        </p>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {active.length > 0 && (
                <div>
                  <h4 className="mb-2 text-xs font-bold uppercase tracking-wide text-emerald-300">Đã vào lớp · {active.length}</h4>
                  <ul className="space-y-1.5">
                    {active.map((r) => (
                      <li key={r.id} className="flex flex-wrap items-center gap-2 rounded-xl bg-white/[.02] px-3 py-2 text-sm">
                        <Check size={14} className="text-emerald-300" />
                        <strong className="text-white">{r.studentName}</strong>
                        {r.joined_late && <span className="rounded-full bg-amber-500/20 px-2 py-0.5 text-[10px] font-bold text-amber-200">vào trễ</span>}
                        <select
                          value={r.payment_status}
                          onChange={(e) => pay(r, e.target.value as PaymentStatus)}
                          className={`ml-auto rounded-lg border px-2 py-1 text-xs ${r.payment_status === "unpaid" ? "border-red-500/30 bg-red-500/[.06] text-red-200" : "border-emerald-500/30 bg-emerald-500/[.06] text-emerald-200"}`}
                        >
                          {(Object.keys(PAYMENT_STATUS_LABEL) as PaymentStatus[]).map((k) => (
                            <option key={k} value={k}>{PAYMENT_STATUS_LABEL[k]}</option>
                          ))}
                        </select>
                        <button type="button" onClick={() => review(r, "left")} className="text-xs text-slate-500 hover:text-red-300">Cho nghỉ</button>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {others.length > 0 && (
                <details className="text-sm">
                  <summary className="cursor-pointer text-xs font-bold uppercase tracking-wide text-slate-500">Từ chối / đã nghỉ · {others.length}</summary>
                  <ul className="mt-2 space-y-1">
                    {others.map((r) => (
                      <li key={r.id} className="flex items-center gap-2 px-3 py-1 text-slate-400">
                        {r.studentName} · {REGISTRATION_STATUS_LABEL[r.status]}
                        <button type="button" onClick={() => review(r, "pending")} className="ml-auto text-xs text-blue-300 hover:underline">Đưa lại hàng chờ</button>
                      </li>
                    ))}
                  </ul>
                </details>
              )}
            </>
          )}
        </div>
      )}
    </section>
  );
}

// ---------- Tab ----------
export default function TeacherThptEnrollment({ classId, className, students, onStudentsChanged }: {
  classId: number;
  className: string;
  students: ClassStudent[];
  onStudentsChanged?: () => void;
}) {
  const [courses, setCourses] = useState<ThptCourse[] | null>(null);
  const [error, setError] = useState("");
  const [topics, setTopics] = useState<QuestionTopic[]>([]);

  useEffect(() => {
    const grade = classGrade(className);
    const load = grade ? fetchQuestionTopics(grade).then(lessonTopics) : Promise.resolve([] as QuestionTopic[]);
    load.then(setTopics).catch(() => setTopics([]));
  }, [className]);

  const reload = useCallback(() => {
    fetchCoursesForClass(classId)
      .then((rows) => { setCourses(rows); setError(""); })
      .catch((e: unknown) => { setCourses([]); setError(errorMessage(e, "Chưa tải được khoá học.")); });
  }, [classId]);

  useEffect(() => { reload(); }, [reload]);

  return (
    <div className="space-y-4">
      <section className="rounded-2xl border border-white/10 bg-panel p-5">
        <h3 className="font-display text-lg font-bold text-white">Ghi danh · khối {className}</h3>
        <p className="mt-1 text-sm text-slate-400">
          Mở lớp kèm lịch tuần, phụ huynh và học sinh tự đăng ký ở trang <span className="text-slate-200">/khoa-hoc</span>. Duyệt xong là em vào khối
          (như duyệt yêu cầu vào lớp). Học phí đóng tại trung tâm — tích tay ở cột phí sau khi trung tâm báo.
        </p>
        <div className="mt-4">
          <CreateThptCourseForm classId={classId} className={className} onCreated={reload} />
        </div>
        {error && <p className="mt-3 text-xs text-red-300">{error}</p>}
      </section>

      {courses === null ? (
        <p className="text-sm text-slate-500">Đang tải…</p>
      ) : courses.length === 0 ? (
        <p className="rounded-2xl border border-dashed border-white/10 p-6 text-center text-sm text-slate-500">Khối này chưa có lớp nào. Mở lớp mới ở trên.</p>
      ) : (
        courses.map((course) => (
          <CourseBlock key={`${course.id}-${course.taken}-${course.is_public}-${course.status}-${course.current_topic_id ?? 0}`} course={course} students={students} topics={topics} onChanged={() => { reload(); onStudentsChanged?.(); }} />
        ))
      )}
    </div>
  );
}
