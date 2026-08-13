"use client";

import { useCallback, useEffect, useState } from "react";
import { Check, Copy, Plus, UserRoundCheck, Users, X } from "lucide-react";
import { useToast } from "@/components/ui/Toast";
import { createCncCourse, fetchCncCourses, fetchCourseEnrollments, reviewEnrollment, type CourseOffering, type EnrollmentMode, type EnrollmentRow } from "@/services/course-enrollments";

function schoolYear() { const now = new Date(); const start = now.getMonth() >= 7 ? now.getFullYear() : now.getFullYear() - 1; return `${start}-${start + 1}`; }
function errorMessage(error: unknown, fallback: string) {
  if (error instanceof Error) return error.message;
  if (error && typeof error === "object" && "message" in error && typeof error.message === "string") return error.message;
  return fallback;
}

const DEMO_STUDENTS = [
  { id: "demo-nguyen-minh-anh", full_name: "Nguyễn Minh Anh (học sinh mẫu)", class_name: "CĐ CK 25A", status: "active" as const },
  { id: "demo-tran-quoc-bao", full_name: "Trần Quốc Bảo (học sinh mẫu)", class_name: "CĐ CK 25A", status: "pending" as const },
];

export default function CncCourseManager() {
  const toast = useToast();
  const [courses, setCourses] = useState<CourseOffering[]>([]);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [enrollments, setEnrollments] = useState<EnrollmentRow[]>([]);
  const [showCreate, setShowCreate] = useState(false);
  const [busy, setBusy] = useState(false);
  const [demoCourseId, setDemoCourseId] = useState<number | null>(null);
  const [form, setForm] = useState({ name: "", class_label: "", school_year: schoolYear(), enrollment_mode: "approval" as EnrollmentMode });

  const reloadCourses = useCallback(async () => {
    try { const rows = await fetchCncCourses(); setCourses(rows); setSelectedId((current) => rows.some((row) => row.id === current) ? current : rows[0]?.id ?? null); }
    catch (error) { toast("error", errorMessage(error, "Chưa tải được khóa CNC.")); }
  }, [toast]);
  const reloadEnrollments = useCallback(async (courseId: number) => {
    try { setEnrollments(await fetchCourseEnrollments(courseId)); }
    catch (error) { toast("error", errorMessage(error, "Chưa tải được danh sách học sinh.")); }
  }, [toast]);

  useEffect(() => { const timer = window.setTimeout(() => void reloadCourses(), 0); return () => clearTimeout(timer); }, [reloadCourses]);
  useEffect(() => { if (!selectedId) return; const timer = window.setTimeout(() => void reloadEnrollments(selectedId), 0); return () => clearTimeout(timer); }, [reloadEnrollments, selectedId]);
  const selected = courses.find((course) => course.id === selectedId);
  const demoEnrollments: EnrollmentRow[] = selectedId === demoCourseId ? DEMO_STUDENTS.map((student) => ({
    course_id: selectedId!, student_id: student.id, status: student.status, enrolled_at: new Date().toISOString(),
    profiles: { id: student.id, full_name: student.full_name, class_name: student.class_name },
  })) : [];
  const visibleEnrollments = [...enrollments, ...demoEnrollments];
  const pending = visibleEnrollments.filter((row) => row.status === "pending");
  const active = visibleEnrollments.filter((row) => row.status === "active");

  async function decide(row: EnrollmentRow, status: "active" | "rejected" | "suspended") {
    if (row.student_id.startsWith("demo-")) { toast("success", "Đây là học sinh mẫu; thao tác đã được mô phỏng."); return; }
    if (!selectedId) return; await reviewEnrollment(selectedId, row.student_id, status); await reloadEnrollments(selectedId);
    toast("success", status === "active" ? "Đã duyệt học sinh vào khóa." : status === "rejected" ? "Đã từ chối yêu cầu." : "Đã tạm khóa học sinh.");
  }

  return <div className="space-y-5">
    <section className="rounded-3xl border border-white/10 bg-gradient-to-br from-[#172c46] to-[#071426] p-6"><div className="flex flex-wrap items-start justify-between gap-4"><div><p className="text-xs font-bold uppercase tracking-[.16em] text-sky-300">CTTC · Gia công CNC</p><h2 className="mt-2 font-display text-2xl font-bold text-white">Quản lý khóa học CNC</h2><p className="mt-2 text-sm text-slate-400">Tạo khóa theo năm, gửi mã cho học sinh và duyệt danh sách tham gia.</p></div><button onClick={() => setShowCreate((value) => !value)} className="flex items-center gap-2 rounded-full bg-blue-600 px-5 py-2.5 text-sm font-bold text-white"><Plus size={16}/> Tạo khóa CNC</button></div></section>
    {showCreate && <section className="rounded-2xl border border-blue-400/20 bg-blue-500/5 p-5"><div className="grid gap-3 md:grid-cols-2"><input value={form.name} onChange={(e)=>setForm({...form,name:e.target.value})} placeholder="Tên khóa: CNC K25A" className="rounded-xl border border-white/10 bg-[#080d1d] px-4 py-3 text-white"/><input value={form.class_label} onChange={(e)=>setForm({...form,class_label:e.target.value})} placeholder="Lớp: CĐ CK 25A" className="rounded-xl border border-white/10 bg-[#080d1d] px-4 py-3 text-white"/><input value={form.school_year} onChange={(e)=>setForm({...form,school_year:e.target.value})} className="rounded-xl border border-white/10 bg-[#080d1d] px-4 py-3 text-white"/><select value={form.enrollment_mode} onChange={(e)=>setForm({...form,enrollment_mode:e.target.value as EnrollmentMode})} className="rounded-xl border border-white/10 bg-[#080d1d] px-4 py-3 text-white"><option value="approval">Giáo viên duyệt</option><option value="automatic">Tự động duyệt</option><option value="closed">Đóng đăng ký</option></select></div><button disabled={busy||!form.name.trim()} onClick={async()=>{setBusy(true);try{await createCncCourse(form);setShowCreate(false);setForm({...form,name:"",class_label:""});await reloadCourses();toast("success","Đã tạo khóa CNC.");}catch(error){toast("error",errorMessage(error,"Chưa tạo được khóa CNC."));}finally{setBusy(false);}}} className="mt-4 rounded-full bg-blue-600 px-5 py-2 text-sm font-bold text-white disabled:opacity-40">Lưu khóa</button></section>}
    <div className="grid gap-5 lg:grid-cols-[280px_1fr]"><aside className="rounded-2xl border border-white/10 bg-[#0B1020] p-4"><h3 className="font-semibold text-white">Các khóa CNC</h3><div className="mt-3 space-y-2">{courses.map((course)=><button key={course.id} onClick={()=>setSelectedId(course.id)} className={`w-full rounded-xl border p-3 text-left ${selectedId===course.id?"border-blue-400 bg-blue-500/10":"border-white/5"}`}><strong className="block text-sm text-white">{course.name}</strong><small className="text-slate-400">{course.school_year} · {course.class_label}</small></button>)}{courses.length===0&&<p className="text-sm text-slate-400">Chưa có khóa học.</p>}</div></aside>
    <main className="space-y-5">{selected ? <><section className="rounded-2xl border border-white/10 bg-[#0B1020] p-5"><h3 className="text-xl font-bold text-white">{selected.name}</h3><p className="mt-1 text-sm text-slate-400">{selected.school_year} · {selected.class_label}</p><div className="mt-4 flex flex-wrap gap-2"><button onClick={async()=>{await navigator.clipboard.writeText(selected.join_code);toast("success","Đã sao chép mã khóa.");}} className="inline-flex items-center gap-2 rounded-xl bg-blue-500/10 px-4 py-2 font-mono font-bold text-blue-200"><Copy size={15}/>{selected.join_code}</button><button onClick={()=>setDemoCourseId(demoCourseId===selected.id?null:selected.id)} className="rounded-xl border border-violet-400/30 bg-violet-500/10 px-4 py-2 text-sm font-bold text-violet-200">{demoCourseId===selected.id?"Ẩn 2 học sinh mẫu":"Thêm 2 học sinh mẫu"}</button></div>{demoCourseId===selected.id&&<p className="mt-2 text-xs text-violet-300">Dữ liệu chỉ dùng xem thử giao diện, không tạo tài khoản thật.</p>}<div className="mt-4 grid grid-cols-2 gap-3"><div className="rounded-xl bg-white/[.04] p-3"><Users className="text-blue-300" size={18}/><strong className="mt-2 block text-xl text-white">{active.length}</strong><small className="text-slate-400">Đang học</small></div><div className="rounded-xl bg-white/[.04] p-3"><UserRoundCheck className="text-amber-300" size={18}/><strong className="mt-2 block text-xl text-white">{pending.length}</strong><small className="text-slate-400">Chờ duyệt</small></div></div></section>
    <List title="Yêu cầu chờ duyệt" rows={pending} renderActions={(row)=><><button onClick={()=>void decide(row,"active")} className="rounded-full bg-emerald-600 px-3 py-1.5 text-xs font-bold text-white"><Check size={13} className="inline"/> Duyệt</button><button onClick={()=>void decide(row,"rejected")} className="rounded-full border border-red-500/30 px-3 py-1.5 text-xs text-red-300"><X size={13} className="inline"/> Từ chối</button></>}/><List title="Học sinh đang học" rows={active} renderActions={(row)=><button onClick={()=>void decide(row,"suspended")} className="rounded-full border border-amber-500/30 px-3 py-1.5 text-xs text-amber-300">Tạm khóa</button>}/></>:<div className="rounded-2xl border border-dashed border-white/10 p-12 text-center text-slate-400">Chọn hoặc tạo một khóa CNC.</div>}</main></div>
  </div>;
}

function List({title,rows,renderActions}:{title:string;rows:EnrollmentRow[];renderActions:(row:EnrollmentRow)=>React.ReactNode}){return <section className="rounded-2xl border border-white/10 bg-[#0B1020] p-5"><h3 className="font-semibold text-white">{title}</h3><div className="mt-3 space-y-2">{rows.map((row)=><article key={row.student_id} className="flex flex-wrap items-center gap-3 rounded-xl border border-white/5 p-3"><div className="min-w-0 flex-1"><strong className="block text-sm text-white">{row.profiles?.full_name||"Học sinh"}</strong><small className="text-slate-400">{row.profiles?.class_name||"Chưa có lớp"}</small></div>{renderActions(row)}</article>)}{rows.length===0&&<p className="text-sm text-slate-400">Chưa có dữ liệu.</p>}</div></section>}
