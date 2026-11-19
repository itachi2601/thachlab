"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import CreateCourseForm from "@/components/dashboard/CreateCourseForm";
import { fetchCncCourses, type CourseOffering } from "@/services/course-enrollments";
import { getSubject, HOMEROOM_SUBJECT_CODE, SUBJECTS } from "@/services/subjects";

/** Môn mở lớp được ở trang này (lớp chủ nhiệm GDĐĐ có luồng riêng). */
const OPEN_SUBJECTS = SUBJECTS.filter((s) => s.code !== HOMEROOM_SUBJECT_CODE);

/** Trang quản trị CTTC: mở lớp học phần mới (chọn môn: CNC, Anh văn chuyên ngành…) + xem các lớp đã mở của môn đó. */
export default function CncOpenClass() {
  const [subjectCode, setSubjectCode] = useState("cnc");
  const subject = getSubject(subjectCode);
  const [courses, setCourses] = useState<CourseOffering[] | null>(null);
  const [error, setError] = useState("");

  const [reload, setReload] = useState(0);

  useEffect(() => {
    let alive = true;
    setCourses(null);
    fetchCncCourses(subjectCode)
      .then((rows) => { if (alive) { setCourses(rows); setError(""); } })
      .catch((e) => { if (alive) setError(e instanceof Error ? e.message : "Chưa tải được danh sách lớp."); });
    return () => { alive = false; };
  }, [reload, subjectCode]);

  return (
    <div className="admin-stack" style={{ gap: 24 }}>
      <header>
        <p className="admin-eyebrow">CTTC · {subject.label}</p>
        <h2 className="mt-1 text-xl font-bold">Mở lớp học phần mới</h2>
        <p className="admin-lead">Chọn môn rồi tạo lớp. Sau khi tạo, vào “Lớp học phần & sinh viên” để nhập danh sách từ Excel hoặc gửi mã vào lớp.</p>
      </header>

      <section>
        <p className="text-sm font-semibold">Môn học</p>
        <div role="radiogroup" aria-label="Môn học" className="mt-2 flex flex-wrap gap-2">
          {OPEN_SUBJECTS.map((s) => {
            const on = s.code === subjectCode;
            return (
              <button key={s.code} type="button" role="radio" aria-checked={on} onClick={() => setSubjectCode(s.code)}
                className={`min-h-11 rounded-full border px-4 py-2 text-sm font-semibold ${on ? "border-blue-600 bg-blue-600 text-white" : "border-white/15"}`}>
                {s.label}
              </button>
            );
          })}
        </div>
      </section>

      <section>
        <CreateCourseForm key={subjectCode} subjectCode={subjectCode} defaultOpen onCreated={() => setReload((n) => n + 1)} />
      </section>

      <section>
        <h3 className="admin-h2">Lớp đã mở · {subject.label}</h3>
        {error && <p className="admin-muted mt-2">{error}</p>}
        {!error && courses === null && <p className="admin-muted mt-2">Đang tải…</p>}
        {courses?.length === 0 && <p className="admin-muted mt-2">Môn {subject.label} chưa có lớp nào.</p>}
        <ul className="mt-3 grid gap-2">
          {courses?.map((c) => (
            <li key={c.id} className="flex flex-wrap items-center justify-between gap-2 rounded-xl border border-white/10 p-3 text-sm">
              <span><strong>{c.name}</strong> · {c.class_label} · {c.school_year}</span>
              <span className="font-mono">{c.join_code}</span>
            </li>
          ))}
        </ul>
        <Link href="/dashboard" className="mt-4 inline-block min-h-11 py-2 text-sm font-semibold underline">Nhập danh sách sinh viên →</Link>
      </section>
    </div>
  );
}
