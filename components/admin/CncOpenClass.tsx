"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import CreateCourseForm from "@/components/dashboard/CreateCourseForm";
import { fetchCncCourses, type CourseOffering } from "@/services/course-enrollments";

/** Trang quản trị CTTC: mở lớp học phần CNC mới + xem các lớp đã mở. Nhập danh sách SV ở dashboard. */
export default function CncOpenClass() {
  const [courses, setCourses] = useState<CourseOffering[] | null>(null);
  const [error, setError] = useState("");

  const load = useCallback(async () => {
    try {
      setCourses(await fetchCncCourses("cnc"));
      setError("");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Chưa tải được danh sách lớp.");
    }
  }, []);

  useEffect(() => { void load(); }, [load]);

  return (
    <div className="admin-stack" style={{ gap: 24 }}>
      <header>
        <p className="admin-eyebrow">CTTC · Gia công CNC</p>
        <h2 className="mt-1 text-xl font-bold">Mở lớp học phần mới</h2>
        <p className="admin-lead">Tạo lớp cho sinh viên học CNC. Sau khi tạo, vào “Lớp học phần & sinh viên” để nhập danh sách từ Excel hoặc gửi mã vào lớp.</p>
      </header>

      <section>
        <CreateCourseForm subjectCode="cnc" defaultOpen onCreated={() => void load()} />
      </section>

      <section>
        <h3 className="admin-h2">Lớp đã mở</h3>
        {error && <p className="admin-muted mt-2">{error}</p>}
        {!error && courses === null && <p className="admin-muted mt-2">Đang tải…</p>}
        {courses?.length === 0 && <p className="admin-muted mt-2">Chưa có lớp CNC nào.</p>}
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
