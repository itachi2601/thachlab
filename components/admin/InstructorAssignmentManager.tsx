"use client";

import { useCallback, useEffect, useState } from "react";
import { GraduationCap, UserPlus, X } from "lucide-react";
import { useToast } from "@/components/ui/Toast";
import StaffInvitePanel from "@/components/admin/StaffInvitePanel";
import AccountRolePanel from "@/components/admin/AccountRolePanel";
import { fetchCncCourses, type CourseOffering } from "@/services/course-enrollments";
import { SUBJECTS } from "@/services/subjects";
import { displayClassesByGrade, fetchClasses } from "@/services/classes";
import {
  assignClassInstructor,
  fetchClassInstructors,
  unassignClassInstructor,
  type ClassInstructor,
} from "@/services/class-instructors";
import type { SchoolClass } from "@/features/exams/types";
import {
  assignInstructor,
  fetchCourseInstructors,
  fetchInstructorRoster,
  unassignInstructor,
  type CourseInstructor,
} from "@/services/course-instructors";

// Mọi môn CTTC (SUBJECTS chỉ gồm môn CTTC) — kể cả môn lý thuyết "khac" nhập từ Excel,
// để admin phân công được giảng viên phụ trách lớp học phần lý thuyết.
const CTTC_SUBJECTS = SUBJECTS;

function errorMessage(error: unknown, fallback: string) {
  if (error instanceof Error) return error.message;
  if (error && typeof error === "object" && "message" in error && typeof error.message === "string") return error.message;
  return fallback;
}

const TABS = [
  { id: "thpt", label: "THPT" },
  { id: "cttc", label: "CTTC" },
] as const;

export default function InstructorAssignmentManager() {
  const [view, setView] = useState<(typeof TABS)[number]["id"]>("thpt");
  const [roster, setRoster] = useState<{ id: string; full_name: string; class_name: string }[]>([]);
  const reloadRoster = useCallback(() => {
    void fetchInstructorRoster().then(setRoster).catch(() => setRoster([]));
  }, []);
  useEffect(reloadRoster, [reloadRoster]);

  return <div className="space-y-5">
    <header>
      <p className="admin-eyebrow">Nhân sự</p>
      <p className="admin-lead">Chọn khu vực rồi gán giảng viên phụ trách từng lớp/khóa. Giảng viên được gán sẽ thấy đúng phạm vi đó, với đầy đủ quyền thao tác cần thiết.</p>
    </header>

    <div className="flex gap-2">
      {TABS.map((tab) => (
        <button
          key={tab.id}
          onClick={() => setView(tab.id)}
          className={`rounded-full border px-5 py-2.5 text-sm font-bold transition-colors ${
            view === tab.id ? "border-blue-400/50 bg-blue-500/15 text-blue-200" : "border-white/10 text-slate-400 hover:border-white/30"
          }`}
        >
          {tab.label}
        </button>
      ))}
    </div>

    {view === "thpt"
      ? <ThptInstructorPanel roster={roster} />
      : <CttcInstructorPanel roster={roster} />}

    <StaffInvitePanel />

    <AccountRolePanel onChanged={reloadRoster} />
  </div>;
}

// ---------- Tab THPT: gán giảng viên theo khối lớp ----------
function ThptInstructorPanel({ roster }: { roster: { id: string; full_name: string; class_name: string }[] }) {
  const toast = useToast();
  const [classes, setClasses] = useState<SchoolClass[]>([]);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [assigned, setAssigned] = useState<ClassInstructor[]>([]);
  const [busy, setBusy] = useState(false);
  const selected = classes.find((c) => c.id === selectedId) ?? null;
  const displayClasses = displayClassesByGrade(classes);

  useEffect(() => {
    void fetchClasses().then((items) => {
      setClasses(items);
      setSelectedId((current) => (current && items.some((c) => c.id === current) ? current : items[0]?.id ?? null));
    });
  }, []);

  const reloadAssigned = useCallback(async (classId: number) => {
    try { setAssigned(await fetchClassInstructors(classId)); }
    catch (error) { toast("error", errorMessage(error, "Chưa tải được danh sách giảng viên được phân công.")); }
  }, [toast]);
  useEffect(() => { if (!selectedId) return; const timer = window.setTimeout(() => void reloadAssigned(selectedId), 0); return () => clearTimeout(timer); }, [reloadAssigned, selectedId]);

  const assignedIds = new Set(assigned.map((row) => row.instructor_id));
  const availableRoster = roster.filter((item) => !assignedIds.has(item.id));

  async function addInstructor(instructorId: string) {
    if (!selectedId) return;
    setBusy(true);
    try { await assignClassInstructor(selectedId, instructorId); await reloadAssigned(selectedId); toast("success", "Đã phân công giảng viên."); }
    catch (error) { toast("error", errorMessage(error, "Chưa phân công được.")); }
    finally { setBusy(false); }
  }
  async function removeInstructor(instructorId: string) {
    if (!selectedId) return;
    setBusy(true);
    try { await unassignClassInstructor(selectedId, instructorId); await reloadAssigned(selectedId); toast("success", "Đã gỡ phân công."); }
    catch (error) { toast("error", errorMessage(error, "Chưa gỡ được.")); }
    finally { setBusy(false); }
  }

  return <div className="grid gap-5 lg:grid-cols-[280px_1fr]">
    <aside className="admin-card">
      <h3 className="font-semibold text-white">Khối lớp</h3>
      <div className="mt-3 space-y-2">
        {displayClasses.map((schoolClass) => (
          <button key={schoolClass.id} onClick={() => setSelectedId(schoolClass.id)} className={`w-full rounded-xl border p-3 text-left ${selectedId === schoolClass.id ? "border-blue-400 bg-blue-500/10" : "border-white/5"}`}>
            <strong className="block text-sm text-white">{schoolClass.icon} {schoolClass.name}</strong>
          </button>
        ))}
        {displayClasses.length === 0 && <p className="text-sm text-slate-400">Chưa có lớp — thêm lớp ở mục Lớp học trước.</p>}
      </div>
    </aside>

    <main className="space-y-5">
      {selected ? <>
        <section className="admin-card">
          <h3 className="text-xl font-bold text-white">{selected.icon} Lớp {selected.name}</h3>
          <div className="mt-4 space-y-2">
            {assigned.map((row) => (
              <article key={row.instructor_id} className="flex items-center gap-3 rounded-xl border border-white/5 p-3">
                <span className="grid h-9 w-9 shrink-0 place-items-center rounded-full bg-blue-500/15 text-blue-200"><GraduationCap size={17}/></span>
                <div className="min-w-0 flex-1"><strong className="block text-sm text-white">{row.profiles?.full_name ?? "Giảng viên"}</strong><small className="text-slate-400">{row.profiles?.class_name || "—"}</small></div>
                <button disabled={busy} onClick={() => void removeInstructor(row.instructor_id)} className="admin-chip admin-chip--danger"><X size={14}/>Gỡ</button>
              </article>
            ))}
            {assigned.length === 0 && <p className="text-sm text-slate-400">Chưa có giảng viên nào được phân công cho khối này.</p>}
          </div>
        </section>

        <section className="admin-card">
          <h3 className="font-semibold text-white">Thêm giảng viên vào khối</h3>
          <div className="mt-3 space-y-2">
            {availableRoster.map((item) => (
              <button key={item.id} disabled={busy} onClick={() => void addInstructor(item.id)} className="flex w-full items-center gap-3 rounded-xl border border-white/5 p-3 text-left hover:border-blue-400/40 hover:bg-blue-500/5 disabled:opacity-40">
                <span className="grid h-9 w-9 shrink-0 place-items-center rounded-full bg-white/5 text-slate-300"><UserPlus size={17}/></span>
                <div className="min-w-0 flex-1"><strong className="block text-sm text-white">{item.full_name}</strong><small className="text-slate-400">{item.class_name || "—"}</small></div>
              </button>
            ))}
            {availableRoster.length === 0 && <p className="text-sm text-slate-400">Không còn giảng viên nào khác trong danh sách để thêm. Cấp vai trò giảng viên cho tài khoản mới ở mục bên dưới.</p>}
          </div>
        </section>
      </> : <div className="admin-empty">Chọn một khối lớp.</div>}
    </main>
  </div>;
}

// ---------- Tab CTTC: gán giảng viên theo khóa học (thực hành hoặc lý thuyết) ----------
function CttcInstructorPanel({ roster }: { roster: { id: string; full_name: string; class_name: string }[] }) {
  const toast = useToast();
  const [subjectCode, setSubjectCode] = useState(CTTC_SUBJECTS[0]?.code ?? "");
  const [courses, setCourses] = useState<CourseOffering[]>([]);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [assigned, setAssigned] = useState<CourseInstructor[]>([]);
  const [busy, setBusy] = useState(false);
  const subject = CTTC_SUBJECTS.find((item) => item.code === subjectCode) ?? CTTC_SUBJECTS[0];
  const selected = courses.find((course) => course.id === selectedId) ?? null;

  const reloadCourses = useCallback(async () => {
    if (!subjectCode) return;
    try {
      const rows = await fetchCncCourses(subjectCode);
      setCourses(rows);
      setSelectedId((current) => (rows.some((row) => row.id === current) ? current : rows[0]?.id ?? null));
    } catch (error) {
      toast("error", errorMessage(error, "Chưa tải được danh sách khóa học."));
    }
  }, [toast, subjectCode]);
  const reloadAssigned = useCallback(async (courseId: number) => {
    try {
      setAssigned(await fetchCourseInstructors(courseId));
    } catch (error) {
      toast("error", errorMessage(error, "Chưa tải được danh sách giảng viên được phân công."));
    }
  }, [toast]);

  useEffect(() => { const timer = window.setTimeout(() => { setCourses([]); setSelectedId(null); void reloadCourses(); }, 0); return () => clearTimeout(timer); }, [reloadCourses]);
  useEffect(() => { if (!selectedId) return; const timer = window.setTimeout(() => void reloadAssigned(selectedId), 0); return () => clearTimeout(timer); }, [reloadAssigned, selectedId]);

  const assignedIds = new Set(assigned.map((row) => row.instructor_id));
  const availableRoster = roster.filter((item) => !assignedIds.has(item.id));

  async function addInstructor(instructorId: string) {
    if (!selectedId) return;
    setBusy(true);
    try { await assignInstructor(selectedId, instructorId); await reloadAssigned(selectedId); toast("success", "Đã phân công giảng viên."); }
    catch (error) { toast("error", errorMessage(error, "Chưa phân công được.")); }
    finally { setBusy(false); }
  }
  async function removeInstructor(instructorId: string) {
    if (!selectedId) return;
    setBusy(true);
    try { await unassignInstructor(selectedId, instructorId); await reloadAssigned(selectedId); toast("success", "Đã gỡ phân công."); }
    catch (error) { toast("error", errorMessage(error, "Chưa gỡ được.")); }
    finally { setBusy(false); }
  }

  return <div className="grid gap-5 lg:grid-cols-[280px_1fr]">
    <aside className="admin-card">
      <select aria-label="Môn học" value={subjectCode} onChange={(e) => setSubjectCode(e.target.value)} className="w-full rounded-xl border border-white/10 bg-[#080d1d] px-4 py-2.5 text-sm text-white">
        {CTTC_SUBJECTS.map((item) => <option key={item.code} value={item.code}>{item.label}</option>)}
      </select>
      <h3 className="mt-4 font-semibold text-white">Các khóa · {subject?.label}</h3>
      <div className="mt-3 space-y-2">
        {courses.map((course) => (
          <button key={course.id} onClick={() => setSelectedId(course.id)} className={`w-full rounded-xl border p-3 text-left ${selectedId === course.id ? "border-blue-400 bg-blue-500/10" : "border-white/5"}`}>
            <strong className="block text-sm text-white">{course.name}</strong>
            <small className="text-slate-400">{course.school_year} · {course.class_label}</small>
          </button>
        ))}
        {courses.length === 0 && <p className="text-sm text-slate-400">Chưa có khóa học.</p>}
      </div>
    </aside>

    <main className="space-y-5">
      {selected ? <>
        <section className="admin-card">
          <h3 className="text-xl font-bold text-white">{selected.name}</h3>
          <p className="mt-1 text-sm text-slate-400">{selected.school_year} · {selected.class_label}</p>
          <div className="mt-4 space-y-2">
            {assigned.map((row) => (
              <article key={row.instructor_id} className="flex items-center gap-3 rounded-xl border border-white/5 p-3">
                <span className="grid h-9 w-9 shrink-0 place-items-center rounded-full bg-blue-500/15 text-blue-200"><GraduationCap size={17}/></span>
                <div className="min-w-0 flex-1"><strong className="block text-sm text-white">{row.profiles?.full_name ?? "Giảng viên"}</strong><small className="text-slate-400">{row.profiles?.class_name || "—"}</small></div>
                <button disabled={busy} onClick={() => void removeInstructor(row.instructor_id)} className="admin-chip admin-chip--danger"><X size={14}/>Gỡ</button>
              </article>
            ))}
            {assigned.length === 0 && <p className="text-sm text-slate-400">Chưa có giảng viên nào được phân công cho khóa này.</p>}
          </div>
        </section>

        <section className="admin-card">
          <h3 className="font-semibold text-white">Thêm giảng viên vào khóa</h3>
          <div className="mt-3 space-y-2">
            {availableRoster.map((item) => (
              <button key={item.id} disabled={busy} onClick={() => void addInstructor(item.id)} className="flex w-full items-center gap-3 rounded-xl border border-white/5 p-3 text-left hover:border-blue-400/40 hover:bg-blue-500/5 disabled:opacity-40">
                <span className="grid h-9 w-9 shrink-0 place-items-center rounded-full bg-white/5 text-slate-300"><UserPlus size={17}/></span>
                <div className="min-w-0 flex-1"><strong className="block text-sm text-white">{item.full_name}</strong><small className="text-slate-400">{item.class_name || "—"}</small></div>
              </button>
            ))}
            {availableRoster.length === 0 && <p className="text-sm text-slate-400">Không còn giảng viên nào khác trong danh sách để thêm. Cấp vai trò giảng viên cho tài khoản mới ở mục bên dưới.</p>}
          </div>
        </section>
      </> : <div className="admin-empty">Chọn một khóa học.</div>}
    </main>
  </div>;
}
