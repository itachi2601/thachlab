"use client";

import { useEffect, useMemo, useState } from "react";
import { AlertTriangle, Calculator, Download, Search } from "lucide-react";
import { useToast } from "@/components/ui/Toast";
import { fetchAttendanceRecords, fetchAttendanceSessions, type AttendanceRecord } from "@/services/course-attendance";
import { fetchStudentRosterInfo, type StudentRosterInfo } from "@/services/student-profile";
import {
  CONDUCT_LABEL,
  exportHomeroomGradebook,
  fetchHomeroomTermRecords,
  setHomeroomTermRecord,
  type ConductGrade,
  type HomeroomTermRecord,
} from "@/services/homeroom-records";

type Student = { id: string; name: string; className: string };

/** Vắng quá ngưỡng này thì cảnh báo không đủ điều kiện dự kiểm tra học kì. */
const ELIGIBILITY_RATE = 80;
const CONDUCT_OPTIONS: ConductGrade[] = ["tot", "kha", "tb", "yeu"];

function errorMessage(error: unknown, fallback: string) {
  return error instanceof Error ? error.message : fallback;
}

function downloadBlob(blob: Blob, filename: string) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

function round1(value: number) {
  return Math.round(value * 10) / 10;
}

export default function HomeroomGradebook({ courseId, students, className, schoolYear }: {
  courseId: number;
  students: Student[];
  className: string;
  schoolYear: string;
}) {
  const toast = useToast();
  const [records, setRecords] = useState<HomeroomTermRecord[]>([]);
  const [rosterInfo, setRosterInfo] = useState<Map<string, StudentRosterInfo>>(new Map());
  const [attendance, setAttendance] = useState<AttendanceRecord[]>([]);
  const [sessionCount, setSessionCount] = useState(0);
  const [saving, setSaving] = useState("");
  const [query, setQuery] = useState("");
  const [exporting, setExporting] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;
    Promise.all([
      fetchHomeroomTermRecords(courseId),
      fetchAttendanceSessions(courseId).then(async (sessions) => ({
        count: sessions.length,
        records: (await Promise.all(sessions.map((session) => fetchAttendanceRecords(session.id).catch(() => [])))).flat(),
      })),
    ])
      .then(([termRows, attendanceData]) => {
        if (cancelled) return;
        setRecords(termRows);
        setSessionCount(attendanceData.count);
        setAttendance(attendanceData.records);
        setError("");
      })
      .catch((cause) => { if (!cancelled) setError(errorMessage(cause, "Không tải được bảng điểm.")); });
    return () => { cancelled = true; };
  }, [courseId]);

  useEffect(() => {
    fetchStudentRosterInfo(students.map((student) => student.id)).then(setRosterInfo).catch(() => setRosterInfo(new Map()));
  }, [students]);

  function recordFor(studentId: string, term: HomeroomTermRecord["term"]) {
    return records.find((row) => row.student_id === studentId && row.term === term);
  }

  const rows = useMemo(() => students.map((student) => {
    const find = (term: HomeroomTermRecord["term"]) => records.find((row) => row.student_id === student.id && row.term === term);
    const hk1 = find("hk1");
    const hk2 = find("hk2");
    const caNam = find("ca_nam");
    const examScores = [hk1?.exam_score, hk2?.exam_score].filter((value): value is number => value !== null && value !== undefined);
    const average = caNam?.exam_score ?? (examScores.length === 2 ? round1((examScores[0] + examScores[1]) / 2) : null);
    const own = attendance.filter((row) => row.student_id === student.id);
    const attended = own.filter((row) => row.status === "present" || row.status === "late").length;
    const attendanceRate = sessionCount ? Math.round((attended / sessionCount) * 100) : null;
    return { student, hk1, hk2, caNam, average, attendanceRate };
  }), [students, records, attendance, sessionCount]);

  const visibleRows = rows.filter(({ student }) =>
    `${student.name} ${student.className} ${rosterInfo.get(student.id)?.studentCode ?? ""}`
      .toLocaleLowerCase("vi-VN")
      .includes(query.trim().toLocaleLowerCase("vi-VN")),
  );

  const atRisk = rows.filter((row) => row.attendanceRate !== null && row.attendanceRate < ELIGIBILITY_RATE).length;

  async function saveExam(studentId: string, term: HomeroomTermRecord["term"], raw: string) {
    const cellKey = `${studentId}:${term}:exam`;
    const value = raw.trim() === "" ? null : Number(raw);
    if (value !== null && (Number.isNaN(value) || value < 0 || value > 10)) {
      toast("error", "Điểm phải trong khoảng 0 – 10.");
      return;
    }
    setSaving(cellKey);
    try {
      await setHomeroomTermRecord(courseId, studentId, term, { exam_score: value });
      setRecords((current) => [
        ...current.filter((row) => !(row.student_id === studentId && row.term === term)),
        { ...(recordFor(studentId, term) ?? { course_id: courseId, student_id: studentId, term, conduct: null, note: "" }), exam_score: value, updated_at: new Date().toISOString() } as HomeroomTermRecord,
      ]);
    } catch (cause) {
      toast("error", errorMessage(cause, "Không lưu được điểm."));
    } finally {
      setSaving("");
    }
  }

  async function saveConduct(studentId: string, term: HomeroomTermRecord["term"], raw: string) {
    const cellKey = `${studentId}:${term}:conduct`;
    const value = raw === "" ? null : (raw as ConductGrade);
    setSaving(cellKey);
    try {
      await setHomeroomTermRecord(courseId, studentId, term, { conduct: value });
      setRecords((current) => [
        ...current.filter((row) => !(row.student_id === studentId && row.term === term)),
        { ...(recordFor(studentId, term) ?? { course_id: courseId, student_id: studentId, term, exam_score: null, note: "" }), conduct: value, updated_at: new Date().toISOString() } as HomeroomTermRecord,
      ]);
    } catch (cause) {
      toast("error", errorMessage(cause, "Không lưu được hạnh kiểm."));
    } finally {
      setSaving("");
    }
  }

  async function handleExport() {
    setExporting(true);
    try {
      const blob = await exportHomeroomGradebook({
        className: className || "Lớp chủ nhiệm",
        schoolYear,
        rows: rows.map(({ student, hk1, hk2, average, attendanceRate }) => ({
          studentCode: rosterInfo.get(student.id)?.studentCode ?? "",
          fullName: student.name,
          birthDate: rosterInfo.get(student.id)?.birthDate ?? "",
          examHk1: hk1?.exam_score ?? null,
          conductHk1: hk1?.conduct ?? null,
          examHk2: hk2?.exam_score ?? null,
          conductHk2: hk2?.conduct ?? null,
          average,
          attendanceRate,
          note: attendanceRate !== null && attendanceRate < ELIGIBILITY_RATE ? "Thiếu chuyên cần" : "",
        })),
      });
      downloadBlob(blob, `bang-diem-gddd-ptnn-${(className || "lop").replace(/\s+/g, "-")}.xlsx`);
      toast("success", "Đã xuất file điểm.");
    } catch (cause) {
      toast("error", errorMessage(cause, "Chưa xuất được file."));
    } finally {
      setExporting(false);
    }
  }

  return (
    <div className="space-y-4">
      <section className="rounded-2xl border border-cyan-400/15 bg-gradient-to-r from-cyan-500/10 to-blue-500/5 p-5">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-2"><Calculator size={20} className="text-cyan-300" /><h3 className="font-display text-xl font-bold text-white">Bảng điểm & hạnh kiểm</h3></div>
          <button disabled={exporting} onClick={handleExport} className="flex items-center gap-2 rounded-full bg-blue-600 px-4 py-2 text-sm font-bold text-white disabled:opacity-40">
            <Download size={15} />{exporting ? "Đang xuất…" : "Xuất file điểm"}
          </button>
        </div>
        <p className="mt-2 text-sm text-slate-400">Mỗi học kì một bài kiểm tra (thang 10). <b className="text-white">TB cả năm</b> = trung bình 2 học kì, nhập tay để ghi đè. Hạnh kiểm do GVCN xếp loại. Chuyên cần lấy từ tab Điểm danh — dưới {ELIGIBILITY_RATE}% sẽ bị cảnh báo.</p>
        {atRisk > 0 && (
          <p className="mt-2 inline-flex items-center gap-1.5 rounded-lg bg-amber-500/10 px-3 py-1.5 text-xs font-bold text-amber-300">
            <AlertTriangle size={13} />{atRisk} học sinh chuyên cần dưới {ELIGIBILITY_RATE}%
          </p>
        )}
        <div className="mt-4 flex items-center gap-2 rounded-xl border border-white/10 bg-black/15 px-3 py-2">
          <Search size={15} className="text-slate-500" />
          <input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Tìm học sinh theo tên, lớp hoặc mã SV…" className="w-full bg-transparent text-sm text-white outline-none placeholder:text-slate-500" />
        </div>
        {error && <p className="mt-3 rounded-xl bg-red-500/10 p-3 text-sm text-red-200">{error}</p>}
      </section>

      <section className="overflow-auto rounded-2xl border border-white/10 bg-[#0B1020]">
        <table className="min-w-[1000px] border-collapse text-sm">
          <thead className="sticky top-0 z-10 bg-[#111a2e] text-xs text-slate-300">
            <tr>
              <th className="sticky left-0 z-20 min-w-52 border-b border-r border-white/10 bg-[#111a2e] p-3 text-left">Học sinh</th>
              <th className="border-b border-white/10 p-3 text-center">Mã SV</th>
              <th className="border-b border-l border-white/10 p-3 text-center text-cyan-200">KT HK1</th>
              <th className="border-b border-white/10 p-3 text-center text-cyan-200">Hạnh kiểm HK1</th>
              <th className="border-b border-l border-white/10 p-3 text-center text-violet-200">KT HK2</th>
              <th className="border-b border-white/10 p-3 text-center text-violet-200">Hạnh kiểm HK2</th>
              <th className="border-b border-l border-white/10 p-3 text-center text-emerald-200">TB cả năm</th>
              <th className="border-b border-white/10 p-3 text-center">Chuyên cần</th>
            </tr>
          </thead>
          <tbody>
            {visibleRows.map(({ student, hk1, hk2, caNam, average, attendanceRate }) => {
              const code = rosterInfo.get(student.id)?.studentCode ?? "";
              const lowRate = attendanceRate !== null && attendanceRate < ELIGIBILITY_RATE;
              return (
                <tr key={student.id} className="hover:bg-white/[.02]">
                  <td className="sticky left-0 z-10 border-b border-r border-white/5 bg-[#0B1020] p-3">
                    <strong className="block text-white">{student.name}</strong><small className="text-slate-500">{student.className}</small>
                  </td>
                  <td className="border-b border-white/5 p-3 text-center font-mono text-slate-300">{code || "—"}</td>
                  <ExamCell studentId={student.id} term="hk1" value={hk1?.exam_score ?? null} busy={saving === `${student.id}:hk1:exam`} onSave={saveExam} />
                  <ConductCell studentId={student.id} term="hk1" value={hk1?.conduct ?? null} busy={saving === `${student.id}:hk1:conduct`} onSave={saveConduct} />
                  <ExamCell studentId={student.id} term="hk2" value={hk2?.exam_score ?? null} busy={saving === `${student.id}:hk2:exam`} onSave={saveExam} />
                  <ConductCell studentId={student.id} term="hk2" value={hk2?.conduct ?? null} busy={saving === `${student.id}:hk2:conduct`} onSave={saveConduct} />
                  <td className="border-b border-l border-white/5 p-2 text-center">
                    <input
                      key={`${student.id}:canam:${caNam?.exam_score ?? average ?? ""}`}
                      aria-label="TB cả năm"
                      type="number" min={0} max={10} step={0.1}
                      disabled={saving === `${student.id}:ca_nam:exam`}
                      defaultValue={caNam?.exam_score ?? (average ?? "")}
                      placeholder={average !== null ? String(average) : ""}
                      onBlur={(e) => { const v = e.currentTarget.value; if (v === (caNam?.exam_score != null ? String(caNam.exam_score) : "")) return; void saveExam(student.id, "ca_nam", v); }}
                      onKeyDown={(e) => { if (e.key === "Enter") e.currentTarget.blur(); }}
                      className={`w-16 rounded-lg border bg-black/20 px-2 py-1.5 text-center font-mono outline-none focus:border-emerald-400/60 disabled:opacity-50 ${caNam?.exam_score != null ? "border-emerald-400/40 text-emerald-200" : "border-white/10 text-slate-400"}`}
                    />
                  </td>
                  <td className="border-b border-white/5 p-2 text-center">
                    {attendanceRate === null ? (
                      <span className="text-slate-600">—</span>
                    ) : (
                      <span className={`rounded-full px-2.5 py-1 text-xs font-bold ${lowRate ? "bg-red-500/10 text-red-300" : attendanceRate >= 90 ? "bg-emerald-500/10 text-emerald-300" : "bg-amber-500/10 text-amber-300"}`}>
                        {attendanceRate}%
                      </span>
                    )}
                  </td>
                </tr>
              );
            })}
            {!visibleRows.length && <tr><td colSpan={8} className="p-10 text-center text-slate-500">Chưa có học sinh — nhập danh sách ở tab Danh sách lớp.</td></tr>}
          </tbody>
        </table>
      </section>
    </div>
  );
}

function ExamCell({ studentId, term, value, busy, onSave }: {
  studentId: string;
  term: HomeroomTermRecord["term"];
  value: number | null;
  busy: boolean;
  onSave: (studentId: string, term: HomeroomTermRecord["term"], raw: string) => void;
}) {
  return (
    <td className="border-b border-l border-white/5 p-2 text-center">
      <input
        key={`${studentId}:${term}:${value ?? ""}`}
        aria-label={`Điểm kiểm tra ${term}`}
        type="number" min={0} max={10} step={0.1} disabled={busy}
        defaultValue={value === null ? "" : value}
        onBlur={(e) => { if (e.currentTarget.value === (value === null ? "" : String(value))) return; onSave(studentId, term, e.currentTarget.value); }}
        onKeyDown={(e) => { if (e.key === "Enter") e.currentTarget.blur(); }}
        className="w-16 rounded-lg border border-white/10 bg-black/20 px-2 py-1.5 text-center font-mono text-slate-300 outline-none focus:border-cyan-400/60 disabled:opacity-50"
      />
    </td>
  );
}

function ConductCell({ studentId, term, value, busy, onSave }: {
  studentId: string;
  term: HomeroomTermRecord["term"];
  value: ConductGrade | null;
  busy: boolean;
  onSave: (studentId: string, term: HomeroomTermRecord["term"], raw: string) => void;
}) {
  return (
    <td className="border-b border-white/5 p-2 text-center">
      <select
        aria-label={`Hạnh kiểm ${term}`}
        disabled={busy}
        value={value ?? ""}
        onChange={(e) => onSave(studentId, term, e.target.value)}
        className="rounded-lg border border-white/10 bg-[#080d1d] px-2 py-1.5 text-xs font-bold text-slate-200 outline-none focus:border-cyan-400/60 disabled:opacity-50"
      >
        <option value="">—</option>
        {CONDUCT_OPTIONS.map((option) => (
          <option key={option} value={option}>{CONDUCT_LABEL[option]}</option>
        ))}
      </select>
    </td>
  );
}
