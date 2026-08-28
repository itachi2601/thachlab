"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { FileSpreadsheet, Plus, Upload, Download, UserCheck2, UserPlus2, AlertCircle } from "lucide-react";
import { useToast } from "@/components/ui/Toast";
import { createCncCourse, fetchCourseEnrollments, type EnrollmentRow } from "@/services/course-enrollments";
import { parseRosterFile, importRosterToCourse, type ParsedRoster, type ImportResultRow } from "@/services/roster-import";
import { exportCourseRoster } from "@/services/roster-export";
import { fetchStudentRosterInfo, type StudentRosterInfo } from "@/services/student-profile";
import { fetchCourseGradeOverrides, setCourseGradeOverride, type CourseGradeOverride } from "@/services/course-grade-overrides";
import { fetchCncLearningRecords, type CncLearningRecord } from "@/services/cnc-learning-records";
import { fetchRubricExamAttemptsByCourse, type RubricExamAttempt } from "@/services/cnc-rubric-exam";
import { fetchAttendanceRecords, fetchAttendanceSessions, type AttendanceRecord } from "@/services/course-attendance";
import { computeCncFinalGrade } from "@/services/cnc-final-grade";
import { LT_GRADE_COLUMNS } from "@/services/roster-schema";
import TeacherFinalGradebook from "@/components/dashboard/TeacherFinalGradebook";

function schoolYear() {
  const now = new Date();
  const start = now.getMonth() >= 7 ? now.getFullYear() : now.getFullYear() - 1;
  return `${start}-${start + 1}`;
}
function errorMessage(error: unknown, fallback: string) {
  if (error instanceof Error) return error.message;
  return fallback;
}
function downloadBlob(blob: Blob, filename: string) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

export interface CourseRosterPanelProps {
  courseId: number;
  courseName: string;
  classLabel: string;
  schoolYear: string;
  subjectLabel: string;
  subjectCode: string;
  isPracticum: boolean;
  /** Chỉ admin mới tạo được lớp học phần mới ngay tại đây. */
  isAdmin: boolean;
  /** Gọi sau khi nhập danh sách xong để dashboard nạp lại danh sách học sinh. */
  onImported?: () => void;
  /** Gọi sau khi admin tạo lớp học phần mới. */
  onCourseCreated?: () => void;
}

export default function CourseRosterPanel({
  courseId, courseName, classLabel, schoolYear: courseYear, subjectLabel, subjectCode,
  isPracticum, isAdmin, onImported, onCourseCreated,
}: CourseRosterPanelProps) {
  const toast = useToast();

  const [showCreate, setShowCreate] = useState(false);
  const [createForm, setCreateForm] = useState({ name: "", class_label: "", school_year: schoolYear() });
  const [busy, setBusy] = useState(false);

  const [parsed, setParsed] = useState<ParsedRoster | null>(null);
  const [importing, setImporting] = useState(false);
  const [importResults, setImportResults] = useState<ImportResultRow[] | null>(null);

  const [enrollments, setEnrollments] = useState<EnrollmentRow[]>([]);
  const [rosterInfo, setRosterInfo] = useState<Map<string, StudentRosterInfo>>(new Map());
  const [ltOverrides, setLtOverrides] = useState<CourseGradeOverride[]>([]);
  const [cncRecords, setCncRecords] = useState<CncLearningRecord[]>([]);
  const [cncAttempts, setCncAttempts] = useState<RubricExamAttempt[]>([]);
  const [cncAttendance, setCncAttendance] = useState<AttendanceRecord[]>([]);
  const [cncSessionCount, setCncSessionCount] = useState(0);
  const [exporting, setExporting] = useState(false);

  const reloadCourseData = useCallback(async (id: number, practicum: boolean) => {
    try {
      const rows = await fetchCourseEnrollments(id);
      const active = rows.filter((row) => row.status === "active");
      setEnrollments(active);
      const info = await fetchStudentRosterInfo(active.map((row) => row.student_id));
      setRosterInfo(info);
      if (practicum) {
        const [attempts, sessions, overrides] = await Promise.all([
          Promise.all([fetchRubricExamAttemptsByCourse(id, "tien"), fetchRubricExamAttemptsByCourse(id, "phay")]).then((r) => r.flat()),
          fetchAttendanceSessions(id),
          fetchCourseGradeOverrides(id).catch(() => []),
        ]);
        const allRecords = (await Promise.all(sessions.map((s) => fetchAttendanceRecords(s.id)))).flat();
        setCncAttempts(attempts);
        setCncAttendance(allRecords);
        setCncSessionCount(sessions.length);
        setLtOverrides(overrides);
        setCncRecords(await fetchCncLearningRecords(id).catch(() => []));
      } else {
        setLtOverrides(await fetchCourseGradeOverrides(id).catch(() => []));
      }
    } catch (error) {
      toast("error", errorMessage(error, "Chưa tải được dữ liệu khóa học."));
    }
  }, [toast]);

  useEffect(() => {
    const timer = window.setTimeout(() => {
      setParsed(null);
      setImportResults(null);
      void reloadCourseData(courseId, isPracticum);
    }, 0);
    return () => clearTimeout(timer);
  }, [courseId, isPracticum, reloadCourseData]);

  async function handleFile(file: File) {
    try {
      const result = await parseRosterFile(file);
      setParsed(result);
      setImportResults(null);
    } catch (error) {
      toast("error", errorMessage(error, "Không đọc được file — kiểm tra lại đúng định dạng .xls/.xlsx."));
    }
  }

  async function handleCreateCourse() {
    if (!createForm.name.trim()) return;
    setBusy(true);
    try {
      await createCncCourse({ ...createForm, enrollment_mode: "approval" }, subjectCode || "khac", "LOP");
      setShowCreate(false);
      setCreateForm({ name: "", class_label: "", school_year: schoolYear() });
      toast("success", "Đã tạo lớp học phần. Chọn lớp vừa tạo ở bộ chọn phía trên để tiếp tục nhập.");
      onCourseCreated?.();
    } catch (error) {
      toast("error", errorMessage(error, "Chưa tạo được lớp học phần."));
    } finally {
      setBusy(false);
    }
  }

  async function handleImport() {
    if (!parsed) return;
    setImporting(true);
    try {
      const students = parsed.students.map((s) => ({
        studentCode: s.studentCode,
        fullName: s.fullName,
        className: classLabel || parsed.className,
        birthDate: s.birthDate,
      }));
      const results = await importRosterToCourse(courseId, students);
      setImportResults(results);
      const okStudents = results.filter((r) => r.status !== "error");
      toast(okStudents.length ? "success" : "error", `Đã xử lý ${results.length} dòng — ${okStudents.length} thành công.`);

      if (parsed.template === "lt" && okStudents.length) {
        const activeRows = (await fetchCourseEnrollments(courseId)).filter((r) => r.status === "active");
        const info = await fetchStudentRosterInfo(activeRows.map((r) => r.student_id));
        const codeToId = new Map<string, string>();
        info.forEach((value, id) => { if (value.studentCode) codeToId.set(value.studentCode.toUpperCase(), id); });
        const writes: Promise<void>[] = [];
        for (const student of parsed.students) {
          const studentId = codeToId.get(student.studentCode.toUpperCase());
          if (!studentId) continue;
          for (const [key, value] of Object.entries(student.scores)) {
            if (value === null) continue;
            writes.push(setCourseGradeOverride(courseId, studentId, key, value));
          }
        }
        if (writes.length) await Promise.all(writes);
      }
      await reloadCourseData(courseId, isPracticum);
      onImported?.();
    } catch (error) {
      toast("error", errorMessage(error, "Chưa nhập được danh sách — kiểm tra Edge Function import-roster đã deploy chưa."));
    } finally {
      setImporting(false);
    }
  }

  const ltRows = useMemo(() => enrollments.map((row) => ({
    id: row.student_id,
    name: row.profiles?.full_name ?? "Học sinh",
    className: row.profiles?.class_name ?? "",
    studentCode: rosterInfo.get(row.student_id)?.studentCode ?? "",
  })), [enrollments, rosterInfo]);

  async function handleExport() {
    setExporting(true);
    try {
      if (isPracticum) {
        const rows = enrollments.map((row, index) => {
          const grade = computeCncFinalGrade(row.student_id, cncAttempts, cncAttendance, cncSessionCount, ltOverrides);
          return {
            stt: index + 1,
            studentCode: rosterInfo.get(row.student_id)?.studentCode ?? "",
            fullName: row.profiles?.full_name ?? "",
            birthDate: rosterInfo.get(row.student_id)?.birthDate ?? "",
            scores: { tong_ket: Math.round(grade.total * 100) / 100 },
          };
        });
        const blob = await exportCourseRoster({ className: courseName, teacherName: "", sessionType: "TH", template: "th", students: rows });
        downloadBlob(blob, `${courseName}-tong-ket.xlsx`);
      } else {
        const rows = enrollments.map((row, index) => ({
          stt: index + 1,
          studentCode: rosterInfo.get(row.student_id)?.studentCode ?? "",
          fullName: row.profiles?.full_name ?? "",
          birthDate: rosterInfo.get(row.student_id)?.birthDate ?? "",
          scores: Object.fromEntries(LT_GRADE_COLUMNS.map((c) => [
            c.key,
            ltOverrides.find((o) => o.student_id === row.student_id && o.grade_key === c.key)?.score ?? null,
          ])),
        }));
        const blob = await exportCourseRoster({ className: courseName, teacherName: "", sessionType: "LT", template: "lt", students: rows });
        downloadBlob(blob, `${courseName}-bang-diem.xlsx`);
      }
      toast("success", "Đã xuất file điểm.");
    } catch (error) {
      toast("error", errorMessage(error, "Chưa xuất được file."));
    } finally {
      setExporting(false);
    }
  }

  return (
    <div className="space-y-5">
      <section className="rounded-3xl border border-white/10 bg-gradient-to-br from-[#172c46] to-[#071426] p-6">
        <div className="flex flex-wrap items-start justify-between gap-3">
          <div>
            <p className="text-xs font-bold uppercase tracking-[.16em] text-sky-300">CTTC · {subjectLabel}</p>
            <h2 className="mt-2 font-display text-2xl font-bold text-white">Nhập danh sách & Bảng điểm</h2>
            <p className="mt-2 text-sm text-slate-400">
              Nhập file Excel danh sách lớp từ phòng đào tạo → tự tạo tài khoản (mật khẩu là mã số sinh viên) và
              ghi danh vào khóa. Cuối kỳ xuất lại đúng file mẫu kèm điểm.
            </p>
          </div>
          {isAdmin && (
            <button onClick={() => setShowCreate((v) => !v)} className="flex items-center gap-2 rounded-full bg-blue-600 px-4 py-2 text-sm font-bold text-white">
              <Plus size={15} /> Tạo lớp học phần
            </button>
          )}
        </div>
        {isAdmin && showCreate && (
          <div className="mt-4 grid gap-3 rounded-2xl border border-blue-400/20 bg-blue-500/5 p-4 md:grid-cols-2">
            <input value={createForm.name} onChange={(e) => setCreateForm({ ...createForm, name: e.target.value })} placeholder="Tên: CĐ CK 21B-Tiếng Anh chuyên ngành" className="rounded-lg border border-white/10 bg-[#080d1d] px-3 py-2 text-sm text-white" />
            <input value={createForm.class_label} onChange={(e) => setCreateForm({ ...createForm, class_label: e.target.value })} placeholder="Lớp: CĐ CK 21B" className="rounded-lg border border-white/10 bg-[#080d1d] px-3 py-2 text-sm text-white" />
            <input value={createForm.school_year} onChange={(e) => setCreateForm({ ...createForm, school_year: e.target.value })} className="rounded-lg border border-white/10 bg-[#080d1d] px-3 py-2 text-sm text-white" />
            <button disabled={busy || !createForm.name.trim()} onClick={handleCreateCourse} className="rounded-lg bg-blue-600 px-3 py-2 text-sm font-bold text-white disabled:opacity-40">Lưu lớp</button>
          </div>
        )}
      </section>

      <section className="rounded-2xl border border-white/10 bg-[#0B1020] p-5">
        <h3 className="text-xl font-bold text-white">{courseName}</h3>
        <p className="mt-1 text-sm text-slate-400">
          {subjectLabel} · {courseYear}{classLabel ? ` · ${classLabel}` : ""} · {enrollments.length} sinh viên
        </p>

        <label className="mt-4 flex cursor-pointer items-center gap-2 rounded-xl border border-dashed border-white/20 bg-white/[.03] px-4 py-3 text-sm text-slate-300 hover:border-blue-400/40">
          <Upload size={16} />
          Chọn file Excel danh sách (.xls, .xlsx)
          <input type="file" accept=".xls,.xlsx" className="hidden" onChange={(e) => { const f = e.target.files?.[0]; if (f) void handleFile(f); e.target.value = ""; }} />
        </label>

        {parsed && (
          <div className="mt-4 space-y-3">
            <div className="flex flex-wrap items-center gap-2 rounded-xl bg-white/[.04] p-3 text-sm text-slate-300">
              <FileSpreadsheet size={16} className="text-emerald-300" />
              <span>{parsed.className || "(không đọc được tên lớp)"} · {parsed.students.length} sinh viên · mẫu {parsed.template === "lt" ? "lý thuyết" : "thực hành"}</span>
            </div>
            <div className="max-h-56 overflow-auto rounded-xl border border-white/10">
              <table className="min-w-full text-xs">
                <thead className="bg-white/5 text-slate-400"><tr><th className="p-2 text-left">Mã SV</th><th className="p-2 text-left">Họ tên</th><th className="p-2 text-left">Ngày sinh</th></tr></thead>
                <tbody>{parsed.students.slice(0, 8).map((s) => (
                  <tr key={s.studentCode} className="border-t border-white/5 text-slate-300">
                    <td className="p-2 font-mono">{s.studentCode}</td><td className="p-2">{s.fullName}</td><td className="p-2">{s.birthDate}</td>
                  </tr>
                ))}</tbody>
              </table>
              {parsed.students.length > 8 && <p className="p-2 text-xs text-slate-500">… và {parsed.students.length - 8} dòng khác.</p>}
            </div>
            <button disabled={importing} onClick={handleImport} className="flex items-center gap-2 rounded-full bg-emerald-600 px-5 py-2.5 text-sm font-bold text-white disabled:opacity-40">
              <UserPlus2 size={16} /> {importing ? "Đang tạo tài khoản…" : "Tạo tài khoản & ghi danh"}
            </button>
          </div>
        )}

        {importResults && (
          <div className="mt-4 max-h-56 overflow-auto rounded-xl border border-white/10 p-3 text-xs">
            <p className="mb-2 text-slate-300">
              <UserCheck2 size={13} className="mr-1 inline text-emerald-300" />
              Mật khẩu ban đầu = mã số sinh viên. Học sinh đăng nhập bằng mã SV ở cả 2 ô.
            </p>
            {importResults.map((r) => (
              <div key={r.studentCode} className={`flex items-center gap-2 py-0.5 ${r.status === "error" ? "text-red-300" : r.status === "created" ? "text-emerald-300" : "text-slate-400"}`}>
                {r.status === "error" && <AlertCircle size={12} />}
                <span className="font-mono">{r.studentCode}</span>
                <span>{r.status === "created" ? "đã tạo tài khoản mới" : r.status === "linked" ? "đã có tài khoản, ghi danh" : r.message}</span>
              </div>
            ))}
          </div>
        )}
      </section>

      {enrollments.length > 0 && (
        <section className="space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="font-display text-lg font-bold text-white">Bảng điểm</h3>
            <button disabled={exporting} onClick={handleExport} className="flex items-center gap-2 rounded-full bg-blue-600 px-4 py-2 text-sm font-bold text-white disabled:opacity-40">
              <Download size={15} /> {exporting ? "Đang xuất…" : "Xuất file điểm"}
            </button>
          </div>
          {isPracticum ? (
            <TeacherFinalGradebook courseId={courseId} students={ltRows.map((r) => ({ id: r.id, name: r.name, className: r.className, records: cncRecords.filter((rec) => rec.student_id === r.id) }))} />
          ) : (
            <LtGradebook courseId={courseId} rows={ltRows} overrides={ltOverrides} onSaved={(next) => setLtOverrides(next)} />
          )}
        </section>
      )}
    </div>
  );
}

function LtGradebook({ courseId, rows, overrides, onSaved }: {
  courseId: number;
  rows: { id: string; name: string; className: string; studentCode: string }[];
  overrides: CourseGradeOverride[];
  onSaved: (next: CourseGradeOverride[]) => void;
}) {
  const toast = useToast();
  const [saving, setSaving] = useState("");

  async function save(studentId: string, key: string, value: number) {
    const cellKey = `${studentId}:${key}`;
    setSaving(cellKey);
    try {
      await setCourseGradeOverride(courseId, studentId, key, value);
      onSaved([...overrides.filter((o) => !(o.student_id === studentId && o.grade_key === key)), { course_id: courseId, student_id: studentId, grade_key: key, score: value, updated_at: new Date().toISOString() }]);
    } catch (error) {
      toast("error", errorMessage(error, "Không lưu được điểm."));
    } finally {
      setSaving("");
    }
  }

  return (
    <div className="overflow-auto rounded-2xl border border-white/10 bg-[#0B1020]">
      <table className="min-w-[1200px] border-collapse text-sm">
        <thead className="sticky top-0 z-10 bg-[#111a2e] text-xs text-slate-300">
          <tr>
            <th className="sticky left-0 z-20 min-w-56 border-b border-r border-white/10 bg-[#111a2e] p-3 text-left">Sinh viên</th>
            <th className="border-b border-white/10 p-3 text-center">Mã SV</th>
            {LT_GRADE_COLUMNS.map((c, i) => <th key={i} className="border-b border-white/10 p-3 text-center">{c.label}</th>)}
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.id} className="hover:bg-white/[.02]">
              <td className="sticky left-0 z-10 border-b border-r border-white/5 bg-[#0B1020] p-3">
                <strong className="block text-white">{row.name}</strong><small className="text-slate-500">{row.className}</small>
              </td>
              <td className="border-b border-white/5 p-3 text-center font-mono text-slate-300">{row.studentCode || "—"}</td>
              {LT_GRADE_COLUMNS.map((c) => {
                const value = overrides.find((o) => o.student_id === row.id && o.grade_key === c.key)?.score ?? null;
                const busy = saving === `${row.id}:${c.key}`;
                return (
                  <td key={c.key} className="border-b border-white/5 p-2 text-center">
                    <input
                      key={`${row.id}:${c.key}:${value}`}
                      aria-label={c.label}
                      type="number" min={0} max={10} step={0.01} disabled={busy}
                      defaultValue={value === null ? "" : value}
                      onBlur={(e) => { if (e.currentTarget.value.trim() === "" || Number.isNaN(e.currentTarget.valueAsNumber)) return; void save(row.id, c.key, e.currentTarget.valueAsNumber); }}
                      onKeyDown={(e) => { if (e.key === "Enter") e.currentTarget.blur(); }}
                      className="w-16 rounded-lg border border-white/10 bg-black/20 px-2 py-1.5 text-center font-mono text-slate-300 outline-none focus:border-cyan-400/60 disabled:opacity-50"
                    />
                  </td>
                );
              })}
            </tr>
          ))}
          {!rows.length && <tr><td colSpan={2 + LT_GRADE_COLUMNS.length} className="p-10 text-center text-slate-500">Chưa có sinh viên.</td></tr>}
        </tbody>
      </table>
    </div>
  );
}
