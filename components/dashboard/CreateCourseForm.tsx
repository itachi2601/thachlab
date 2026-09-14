"use client";

import { useState } from "react";
import { Plus } from "lucide-react";
import { useToast } from "@/components/ui/Toast";
import { createCncCourse } from "@/services/course-enrollments";

/** Năm học hiện tại theo mốc khai giảng tháng 8. */
export function currentSchoolYear() {
  const now = new Date();
  const start = now.getMonth() >= 7 ? now.getFullYear() : now.getFullYear() - 1;
  return `${start}-${start + 1}`;
}

export interface CreateCourseFormProps {
  subjectCode: string;
  /** Mở sẵn ô nhập (dùng cho trạng thái "môn này chưa có lớp nào"). */
  defaultOpen?: boolean;
  onCreated?: () => void;
}

/** Form tạo lớp học phần mới — dùng cả trong tab Danh sách lớp lẫn màn hình trống chưa có lớp. */
export default function CreateCourseForm({ subjectCode, defaultOpen = false, onCreated }: CreateCourseFormProps) {
  const toast = useToast();
  const [open, setOpen] = useState(defaultOpen);
  const [form, setForm] = useState({ name: "", class_label: "", school_year: currentSchoolYear() });
  const [busy, setBusy] = useState(false);

  async function submit() {
    if (!form.name.trim()) return;
    setBusy(true);
    try {
      await createCncCourse({ ...form, enrollment_mode: "approval" }, subjectCode || "khac", "LOP");
      setOpen(defaultOpen);
      setForm({ name: "", class_label: "", school_year: currentSchoolYear() });
      toast("success", "Đã tạo lớp học phần. Chọn lớp vừa tạo ở bộ chọn phía trên để tiếp tục nhập.");
      onCreated?.();
    } catch (error) {
      toast("error", error instanceof Error ? error.message : "Chưa tạo được lớp học phần.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <>
      {!defaultOpen && (
        <button onClick={() => setOpen((v) => !v)} className="flex items-center gap-2 rounded-full bg-blue-600 px-4 py-2 text-sm font-bold text-white">
          <Plus size={15} /> Tạo lớp học phần
        </button>
      )}
      {open && (
        <div className="mt-4 w-full grid gap-3 rounded-2xl border border-blue-400/20 bg-blue-500/5 p-4 md:grid-cols-2">
          <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} placeholder="Tên: CĐ CK 21B-Tiếng Anh chuyên ngành" className="rounded-lg border border-white/10 bg-[#080d1d] px-3 py-2 text-sm text-white" />
          <input value={form.class_label} onChange={(e) => setForm({ ...form, class_label: e.target.value })} placeholder="Lớp: CĐ CK 21B" className="rounded-lg border border-white/10 bg-[#080d1d] px-3 py-2 text-sm text-white" />
          <input value={form.school_year} onChange={(e) => setForm({ ...form, school_year: e.target.value })} aria-label="Năm học" className="rounded-lg border border-white/10 bg-[#080d1d] px-3 py-2 text-sm text-white" />
          <button disabled={busy || !form.name.trim()} onClick={submit} className="rounded-lg bg-blue-600 px-3 py-2 text-sm font-bold text-white disabled:opacity-40">
            {busy ? "Đang tạo…" : "Lưu lớp"}
          </button>
        </div>
      )}
    </>
  );
}
