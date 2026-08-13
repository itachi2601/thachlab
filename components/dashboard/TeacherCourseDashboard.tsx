"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { ArrowLeft, Award, BookOpenCheck, CalendarCheck, ChevronRight, Eye, GraduationCap, LayoutDashboard, Route, ShieldCheck } from "lucide-react";
import { CNC_COURSE_ITEMS } from "@/services/cnc-lms";
import { fetchCncCourses, fetchCourseEnrollments, type CourseOffering, type EnrollmentRow } from "@/services/course-enrollments";
import { fetchCncLearningRecords, subscribeToCncLearningRecords, unsubscribeFromCncLearningRecords, type CncLearningRecord } from "@/services/cnc-learning-records";
import TeacherAttendancePanel from "@/components/attendance/TeacherAttendancePanel";
import { cncAssessmentProgress, completedCncLessons, CNC_TOTAL_ASSESSMENTS } from "@/services/cnc-progress";
import ClassCompetencyMatrix from "@/components/competencies/ClassCompetencyMatrix";
import TeacherOverview from "@/components/dashboard/TeacherOverview";
import TeacherProgressGradebook from "@/components/dashboard/TeacherProgressGradebook";

type DashboardStudent = {
  id: string; name: string; className: string; xp: number; pct: number; score: string;
  status: string; color: "blue" | "amber"; last: string; steps: boolean[]; records: CncLearningRecord[];
};

const roadmap = CNC_COURSE_ITEMS.filter((item)=>item.id!=="intro").map((item)=>({id:item.id,title:item.title,duration:item.duration}));
function toDashboardStudent(row: EnrollmentRow, records: CncLearningRecord[]): DashboardStudent {
  const pending = row.status === "pending";
  const own = records.filter((record)=>record.student_id===row.student_id);
  const completed = completedCncLessons(own);
  const assessmentProgress = cncAssessmentProgress(own);
  const scored = own.filter((record)=>record.latest_score!==null&&record.total_questions);
  const latest = scored.toSorted((a,b)=>Date.parse(b.last_activity_at)-Date.parse(a.last_activity_at))[0];
  const pct = assessmentProgress.pct;
  return {
    id: row.student_id,
    name: row.profiles?.full_name || "Học sinh",
    className: row.profiles?.class_name || "Chưa cập nhật lớp",
    xp: assessmentProgress.passed,
    pct,
    score: latest ? `${latest.latest_score}/${latest.total_questions}` : "—",
    status: pending ? "Chờ giáo viên duyệt" : assessmentProgress.passed ? `Đã đạt ${assessmentProgress.passed}/${assessmentProgress.total} bài kiểm tra` : "Chưa bắt đầu",
    color: pending ? "amber" : "blue",
    last: new Intl.DateTimeFormat("vi-VN", { day: "2-digit", month: "2-digit", year: "numeric" }).format(new Date(latest?.last_activity_at ?? row.enrolled_at)),
    steps: roadmap.map((lesson) => completed.has(lesson.id)),
    records: own,
  };
}

function roadmapState(student:DashboardStudent,index:number) {
  const done=Boolean(student.steps[index]);
  return {done,locked:false,current:false};
}

export default function TeacherCourseDashboard() {
  const [activeTab,setActiveTab]=useState<"overview"|"progress"|"competencies"|"attendance">("overview");
  const [activeStudent, setActiveStudent] = useState(0);
  const [studentPreview, setStudentPreview] = useState(false);
  const [courses, setCourses] = useState<CourseOffering[]>([]);
  const [selectedCourseId, setSelectedCourseId] = useState<number | null>(null);
  const [students, setStudents] = useState<DashboardStudent[]>([]);
  const [courseError, setCourseError] = useState("");
  const student = students[activeStudent] ?? null;
  const selectedCourse = courses.find((course) => course.id === selectedCourseId) ?? null;

  useEffect(() => {
    let cancelled = false;
    fetchCncCourses()
      .then((rows) => {
        if (cancelled) return;
        setCourses(rows);
        setSelectedCourseId((current) => rows.some((course) => course.id === current) ? current : rows[0]?.id ?? null);
        setCourseError("");
      })
      .catch((error: unknown) => {
        if (cancelled) return;
        setCourseError(error && typeof error === "object" && "message" in error ? String(error.message) : "Không tải được danh sách khóa học.");
      });
    return () => { cancelled = true; };
  }, []);

  useEffect(() => {
    if (!selectedCourseId) return;
    let cancelled = false;
    const reload = () => Promise.all([fetchCourseEnrollments(selectedCourseId), fetchCncLearningRecords(selectedCourseId).catch(()=>[])])
      .then(([rows,records]) => {
        if (cancelled) return;
        setStudents(rows.filter((row) => row.status === "active" || row.status === "pending").map((row)=>toDashboardStudent(row,records)));
        setActiveStudent(0);
        setCourseError("");
      })
      .catch((error: unknown) => {
        if (cancelled) return;
        setStudents([]);
        setCourseError(error && typeof error === "object" && "message" in error ? String(error.message) : "Không tải được danh sách học sinh.");
      });
    void reload();
    const channel=subscribeToCncLearningRecords(selectedCourseId,()=>void reload());
    return () => { cancelled = true; void unsubscribeFromCncLearningRecords(channel); };
  }, [selectedCourseId]);

  if (studentPreview && student) return <StudentDashboardPreview student={student} course={selectedCourse} onBack={()=>setStudentPreview(false)} />;

  return <div className="space-y-6">
    <section className="relative overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-[#172c46] via-[#0e1c32] to-[#071426] p-6 sm:p-8">
      <div className="absolute -right-20 -top-24 h-64 w-64 rounded-full bg-orange-500/10 blur-3xl" />
      <div className="relative flex flex-wrap items-end justify-between gap-5">
        <div><p className="text-xs font-bold uppercase tracking-[.16em] text-orange-300">Dashboard giáo viên · CNC</p><h2 className="mt-2 font-display text-3xl font-bold text-white">{selectedCourse?.name ?? "Tiến độ khóa học"}</h2><p className="mt-2 text-sm text-slate-400">{selectedCourse ? `${selectedCourse.class_label || "Chưa đặt tên lớp"} · ${selectedCourse.school_year}` : "Theo dõi lộ trình, điểm chốt chặn và điều kiện lên máy của từng học sinh."}</p>{courseError&&<p className="mt-2 text-xs text-red-300">{courseError}</p>}</div>
        <div className="flex flex-wrap gap-2"><button disabled={!student} onClick={()=>setStudentPreview(true)} className="inline-flex items-center gap-2 rounded-xl border border-cyan-400/30 bg-cyan-500/10 px-4 py-2.5 text-sm font-bold text-cyan-200 disabled:cursor-not-allowed disabled:opacity-40"><Eye size={16}/> Xem giao diện học sinh</button><select aria-label="Môn học" className="rounded-xl border border-white/10 bg-[#080d1d] px-4 py-2.5 text-sm text-white"><option>Gia công CNC</option></select><select aria-label="Khóa học" value={selectedCourseId ?? ""} onChange={(event)=>{setStudents([]);setActiveStudent(0);setSelectedCourseId(Number(event.target.value));}} className="rounded-xl border border-white/10 bg-[#080d1d] px-4 py-2.5 text-sm text-white"><option value="" disabled>{courses.length ? "Chọn khóa học" : "Chưa có khóa CNC"}</option>{courses.map((course)=><option key={course.id} value={course.id}>{course.name} · {course.school_year}</option>)}</select></div>
      </div>
    </section>

    <nav className="sticky top-20 z-40 flex gap-2 overflow-x-auto rounded-2xl border border-white/10 bg-[#080d1d]/95 p-2 shadow-xl backdrop-blur">{([{id:"overview",label:"Tổng quan",icon:LayoutDashboard},{id:"progress",label:"Điểm & tiến độ",icon:Route},{id:"competencies",label:"Năng lực & cấp quyền",icon:Award},{id:"attendance",label:"Điểm danh",icon:CalendarCheck}]as const).map(item=>{const Icon=item.icon;return <button key={item.id} onClick={()=>setActiveTab(item.id)} className={`inline-flex shrink-0 items-center gap-2 rounded-xl px-4 py-3 text-sm font-bold ${activeTab===item.id?"bg-blue-600 text-white":"text-slate-400 hover:bg-white/5 hover:text-white"}`}><Icon size={17}/>{item.label}</button>})}</nav>

    {activeTab==="attendance"&&selectedCourseId&&<TeacherAttendancePanel courseId={selectedCourseId} students={students.map(item=>({id:item.id,name:item.name,className:item.className}))}/>}
    {activeTab==="competencies"&&selectedCourseId&&<ClassCompetencyMatrix courseId={selectedCourseId} students={students.map(item=>({id:item.id,name:item.name,className:item.className,records:item.records}))}/>}

    {activeTab==="overview"&&selectedCourseId&&<TeacherOverview courseId={selectedCourseId} students={students.map(item=>({id:item.id,name:item.name,className:item.className,pct:item.pct,xp:item.xp,records:item.records}))} onOpenTab={setActiveTab} onOpenStudent={(id)=>{const index=students.findIndex(item=>item.id===id);if(index>=0)setActiveStudent(index);setActiveTab("progress")}}/>}

    {activeTab==="progress"&&<TeacherProgressGradebook students={students} selectedId={student?.id} onSelect={(id)=>{const index=students.findIndex(item=>item.id===id);if(index>=0)setActiveStudent(index)}}/>}
  </div>;
}

function StudentDashboardPreview({student,course,onBack}:{student:DashboardStudent;course:CourseOffering|null;onBack:()=>void}) {
  return <div className="space-y-6">
    <button onClick={onBack} className="inline-flex items-center gap-2 rounded-full border border-white/10 px-4 py-2 text-sm font-bold text-slate-300 hover:border-blue-400/40 hover:text-white"><ArrowLeft size={16}/> Quay lại Dashboard giáo viên</button>
    <section className="relative overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-[#172c46] via-[#0e1c32] to-[#071426] p-6 sm:p-8"><div className="absolute -right-16 -top-20 h-56 w-56 rounded-full bg-cyan-500/10 blur-3xl"/><div className="relative"><p className="text-xs font-bold uppercase tracking-[.16em] text-cyan-300">Chế độ xem thử · Học sinh</p><h2 className="mt-2 font-display text-3xl font-bold text-white">Chào {student.name} 👋</h2><p className="mt-2 text-sm text-slate-400">{student.className} · {course?.name ?? "Khóa CNC mẫu"} · {course?.school_year ?? "2026–2027"}</p><ManaBar pct={student.pct} xp={student.xp} color={student.color}/></div></section>
    <section className="grid gap-3 sm:grid-cols-3"><Stat icon={<Route size={18}/>} value={`${student.pct}%`} label="Tiến độ khóa" tone="blue"/><Stat icon={<BookOpenCheck size={18}/>} value={student.score} label="Quiz an toàn" tone="emerald"/><Stat icon={<ShieldCheck size={18}/>} value={student.steps[4]?"Đã mở":"Đang khóa"} label="Quyền lên máy" tone="amber"/></section>
    <section className="rounded-2xl border border-white/10 bg-[#0B1020] p-5 sm:p-6"><div className="flex items-center gap-2"><GraduationCap size={19} className="text-orange-300"/><h3 className="font-display text-xl font-bold text-white">Các bài học CNC</h3></div><p className="mt-1 text-sm text-slate-500">Các bài học độc lập; sinh viên có thể chọn bất kỳ bài nào để học và làm kiểm tra.</p><div className="mt-5 grid gap-3 md:grid-cols-2 xl:grid-cols-3">{roadmap.map((item,index)=>{const state=roadmapState(student,index);return <div key={item.id} className={`relative flex min-h-48 flex-col rounded-2xl border p-4 ${state.done?"border-emerald-500/25 bg-emerald-500/5":state.current?"border-orange-400/35 bg-orange-500/5":"border-blue-500/15 bg-blue-500/[.03]"}`}><span className={`flex h-9 w-9 items-center justify-center rounded-full text-sm font-bold ${state.done?"bg-emerald-500 text-white":state.current?"bg-orange-500 text-white":"bg-blue-500/20 text-blue-300"}`}>{state.done?"✓":index+1}</span><strong className="mt-4 block text-sm text-white">{item.title}</strong><small className={state.done?"text-emerald-300":state.current?"text-orange-300":"text-slate-500"}>{state.done?"Đã hoàn thành":state.current?"Có thể học tiếp":item.duration}</small><div className="mt-auto pt-4"><Link href={`/lop-hoc/cnc/?bai=${item.id}`} className={`inline-flex items-center gap-1.5 rounded-full px-3 py-1.5 text-xs font-bold ${state.current?"bg-orange-500 text-white":"bg-blue-600 text-white hover:bg-blue-500"}`}>{state.done?"Xem lại":"Vào bài học"}<ChevronRight size={14}/></Link></div></div>})}</div></section>
  </div>;
}

function ManaBar({pct,xp,color,compact=false}:{pct:number;xp:number;color:string;compact?:boolean}) { const fill=color==="amber"?"from-amber-500 via-orange-400 to-yellow-300":"from-blue-600 via-cyan-400 to-sky-300"; return <div className={compact?"mt-3":"mt-6 rounded-2xl border border-white/5 bg-black/20 p-4"}><div className="mb-2 flex items-center justify-between"><span className="text-xs font-bold text-slate-300">Tiến độ đánh giá</span><span className="font-mono text-xs text-slate-400">{xp}/{CNC_TOTAL_ASSESSMENTS} bài đạt · {pct}%</span></div><div className={`relative overflow-hidden rounded-full border border-white/10 bg-[#050914] ${compact?"h-2.5":"h-4"}`}><div className={`h-full rounded-full bg-gradient-to-r ${fill} shadow-[0_0_18px_rgba(56,189,248,.45)] transition-all duration-700`} style={{width:`${pct}%`}}/><div className="absolute inset-0 bg-[linear-gradient(90deg,transparent_49%,rgba(255,255,255,.08)_50%,transparent_51%)] bg-[length:20%_100%]"/></div></div> }

function Stat({icon,value,label,tone}:{icon:React.ReactNode;value:string;label:string;tone:string}) { const tones:Record<string,string>={blue:"border-blue-500/20 bg-blue-500/8 text-blue-300",violet:"border-violet-500/20 bg-violet-500/8 text-violet-300",emerald:"border-emerald-500/20 bg-emerald-500/8 text-emerald-300",amber:"border-amber-500/20 bg-amber-500/8 text-amber-300"};return <div className={`rounded-2xl border p-5 ${tones[tone]}`}><div className="flex items-center gap-2">{icon}<span className="text-xs font-semibold uppercase tracking-wider">{label}</span></div><strong className="mt-3 block text-3xl text-white">{value}</strong></div> }
