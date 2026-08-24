"use client";

import { useCallback, useEffect, useState } from "react";
import { GraduationCap, Search, ShieldCheck, ShieldX, UserPlus, X } from "lucide-react";
import { useToast } from "@/components/ui/Toast";
import { fetchCncCourses, type CourseOffering } from "@/services/course-enrollments";
import { SUBJECTS } from "@/services/subjects";
import {
  assignInstructor,
  fetchCourseInstructors,
  fetchInstructorRoster,
  searchProfiles,
  setInstructorRole,
  unassignInstructor,
  type AssignableProfile,
  type CourseInstructor,
} from "@/services/course-instructors";

const PRACTICUM_SUBJECTS = SUBJECTS.filter((item) => item.isPracticum);

function errorMessage(error: unknown, fallback: string) {
  if (error instanceof Error) return error.message;
  if (error && typeof error === "object" && "message" in error && typeof error.message === "string") return error.message;
  return fallback;
}

export default function InstructorAssignmentManager() {
  const toast = useToast();
  const [subjectCode, setSubjectCode] = useState(PRACTICUM_SUBJECTS[0]?.code ?? "");
  const [courses, setCourses] = useState<CourseOffering[]>([]);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [assigned, setAssigned] = useState<CourseInstructor[]>([]);
  const [roster, setRoster] = useState<{ id: string; full_name: string; class_name: string }[]>([]);
  const [busy, setBusy] = useState(false);
  const subject = PRACTICUM_SUBJECTS.find((item) => item.code === subjectCode) ?? PRACTICUM_SUBJECTS[0];
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
  useEffect(() => { void fetchInstructorRoster().then(setRoster).catch(() => setRoster([])); }, [assigned]);

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

  return <div className="space-y-5">
    <section className="rounded-3xl border border-white/10 bg-gradient-to-br from-[#172c46] to-[#071426] p-6">
      <p className="text-xs font-bold uppercase tracking-[.16em] text-sky-300">Nhân sự</p>
      <h2 className="mt-2 font-display text-2xl font-bold text-white">Phân công giảng viên</h2>
      <p className="mt-2 text-sm text-slate-400">Chọn khóa thực tập rồi gán giảng viên phụ trách. Giảng viên được gán sẽ thấy đúng khóa đó trong trang Dashboard của họ, với đầy đủ quyền điểm danh, chấm năng lực và tổng kết điểm — không cần vào trang quản trị.</p>
    </section>

    <div className="grid gap-5 lg:grid-cols-[280px_1fr]">
      <aside className="rounded-2xl border border-white/10 bg-[#0B1020] p-4">
        <select aria-label="Môn học" value={subjectCode} onChange={(e) => setSubjectCode(e.target.value)} className="w-full rounded-xl border border-white/10 bg-[#080d1d] px-4 py-2.5 text-sm text-white">
          {PRACTICUM_SUBJECTS.map((item) => <option key={item.code} value={item.code}>{item.label}</option>)}
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
          <section className="rounded-2xl border border-white/10 bg-[#0B1020] p-5">
            <h3 className="text-xl font-bold text-white">{selected.name}</h3>
            <p className="mt-1 text-sm text-slate-400">{selected.school_year} · {selected.class_label}</p>
            <div className="mt-4 space-y-2">
              {assigned.map((row) => (
                <article key={row.instructor_id} className="flex items-center gap-3 rounded-xl border border-white/5 p-3">
                  <span className="grid h-9 w-9 shrink-0 place-items-center rounded-full bg-blue-500/15 text-blue-200"><GraduationCap size={17}/></span>
                  <div className="min-w-0 flex-1"><strong className="block text-sm text-white">{row.profiles?.full_name ?? "Giảng viên"}</strong><small className="text-slate-400">{row.profiles?.class_name || "—"}</small></div>
                  <button disabled={busy} onClick={() => void removeInstructor(row.instructor_id)} className="inline-flex items-center gap-1 rounded-full bg-red-500/15 px-3 py-1.5 text-xs font-bold text-red-200 disabled:opacity-40"><X size={14}/>Gỡ</button>
                </article>
              ))}
              {assigned.length === 0 && <p className="text-sm text-slate-400">Chưa có giảng viên nào được phân công cho khóa này.</p>}
            </div>
          </section>

          <section className="rounded-2xl border border-white/10 bg-[#0B1020] p-5">
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
        </> : <div className="rounded-2xl border border-dashed border-white/10 p-12 text-center text-slate-400">Chọn một khóa học.</div>}

        <InstructorRoleSearch onChanged={() => void fetchInstructorRoster().then(setRoster).catch(() => undefined)} />
      </main>
    </div>
  </div>;
}

function InstructorRoleSearch({ onChanged }: { onChanged: () => void }) {
  const toast = useToast();
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<AssignableProfile[]>([]);
  const [busyId, setBusyId] = useState("");

  useEffect(() => {
    let cancelled = false;
    const timer = window.setTimeout(() => {
      void searchProfiles(query).then((rows) => { if (!cancelled) setResults(rows); }).catch(() => { if (!cancelled) setResults([]); });
    }, 250);
    return () => { cancelled = true; clearTimeout(timer); };
  }, [query]);

  async function toggle(profile: AssignableProfile) {
    setBusyId(profile.id);
    try {
      await setInstructorRole(profile.id, profile.role !== "instructor");
      setResults((current) => current.map((item) => item.id === profile.id ? { ...item, role: profile.role === "instructor" ? "student" : "instructor" } : item));
      onChanged();
      toast("success", profile.role === "instructor" ? "Đã thu hồi vai trò giảng viên." : "Đã cấp vai trò giảng viên.");
    } catch (error) {
      toast("error", error instanceof Error ? error.message : "Chưa cập nhật được vai trò.");
    } finally { setBusyId(""); }
  }

  return <section className="rounded-2xl border border-violet-400/15 bg-violet-500/5 p-5">
    <h3 className="font-semibold text-white">Cấp / thu hồi vai trò giảng viên</h3>
    <p className="mt-1 text-xs text-slate-500">Tìm tài khoản theo tên, lớp hoặc MSSV để bật vai trò giảng viên — tài khoản đó sẽ có thể được phân công vào khóa thực tập ở trên.</p>
    <div className="mt-3 flex items-center gap-2 rounded-xl border border-white/10 bg-black/15 px-3 py-2"><Search size={15} className="text-slate-500"/><input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Tìm theo tên, lớp hoặc MSSV…" className="w-full bg-transparent text-sm text-white outline-none placeholder:text-slate-500"/></div>
    <div className="mt-3 space-y-2">
      {results.filter((item) => item.role !== "admin").map((item) => (
        <article key={item.id} className="flex items-center gap-3 rounded-xl border border-white/5 bg-black/15 p-3">
          <div className="min-w-0 flex-1"><strong className="block text-sm text-white">{item.full_name}</strong><small className="text-slate-400">{item.class_name || "—"} {item.student_code ? `· ${item.student_code}` : ""}</small></div>
          {item.role === "instructor" ? (
            <button disabled={busyId === item.id} onClick={() => void toggle(item)} className="inline-flex items-center gap-1 rounded-full bg-red-500/15 px-3 py-1.5 text-xs font-bold text-red-200 disabled:opacity-40"><ShieldX size={14}/>Thu hồi</button>
          ) : (
            <button disabled={busyId === item.id} onClick={() => void toggle(item)} className="inline-flex items-center gap-1 rounded-full bg-emerald-500/15 px-3 py-1.5 text-xs font-bold text-emerald-200 disabled:opacity-40"><ShieldCheck size={14}/>Đặt làm giảng viên</button>
          )}
        </article>
      ))}
      {results.length === 0 && <p className="text-sm text-slate-400">Nhập từ khóa để tìm tài khoản.</p>}
    </div>
  </section>;
}
