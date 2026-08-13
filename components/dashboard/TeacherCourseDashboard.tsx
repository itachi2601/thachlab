"use client";

import { useEffect, useState } from "react";
import { Award, CalendarCheck, Eye, LayoutDashboard, Route, UserRound } from "lucide-react";
import { CNC_COURSE_ITEMS } from "@/services/cnc-lms";
import { fetchCncCourses, fetchCourseEnrollments, type CourseOffering, type EnrollmentRow } from "@/services/course-enrollments";
import { fetchCncLearningRecords, subscribeToCncLearningRecords, unsubscribeFromCncLearningRecords, type CncLearningRecord } from "@/services/cnc-learning-records";
import TeacherAttendancePanel from "@/components/attendance/TeacherAttendancePanel";
import { cncAssessmentProgress, completedCncLessons } from "@/services/cnc-progress";
import ClassCompetencyMatrix from "@/components/competencies/ClassCompetencyMatrix";
import TeacherOverview from "@/components/dashboard/TeacherOverview";
import TeacherProgressGradebook from "@/components/dashboard/TeacherProgressGradebook";
import StudentLearningDashboard from "@/components/dashboard/StudentLearningDashboard";
import TeacherStudentProfile from "@/components/dashboard/TeacherStudentProfile";

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

export default function TeacherCourseDashboard() {
  const [activeTab,setActiveTab]=useState<"overview"|"progress"|"profile"|"competencies"|"attendance">("overview");
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

  if (studentPreview && student && selectedCourse) return <StudentLearningDashboard preview profile={{id:student.id,full_name:student.name,class_name:student.className,role:"student"}} studentId={student.id} enrollment={{status:"active",enrolled_at:new Date().toISOString(),course:{...selectedCourse,status:selectedCourse.status}}} records={student.records} onSignOut={()=>setStudentPreview(false)}/>;

  return <div className="space-y-6">
    <section className="relative overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-[#172c46] via-[#0e1c32] to-[#071426] p-6 sm:p-8">
      <div className="absolute -right-20 -top-24 h-64 w-64 rounded-full bg-orange-500/10 blur-3xl" />
      <div className="relative flex flex-wrap items-end justify-between gap-5">
        <div><p className="text-xs font-bold uppercase tracking-[.16em] text-orange-300">Dashboard giáo viên · CNC</p><h2 className="mt-2 font-display text-3xl font-bold text-white">{selectedCourse?.name ?? "Tiến độ khóa học"}</h2><p className="mt-2 text-sm text-slate-400">{selectedCourse ? `${selectedCourse.class_label || "Chưa đặt tên lớp"} · ${selectedCourse.school_year}` : "Theo dõi lộ trình, điểm chốt chặn và điều kiện lên máy của từng học sinh."}</p>{courseError&&<p className="mt-2 text-xs text-red-300">{courseError}</p>}</div>
        <div className="flex flex-wrap gap-2"><button disabled={!student} onClick={()=>setStudentPreview(true)} className="inline-flex items-center gap-2 rounded-xl border border-cyan-400/30 bg-cyan-500/10 px-4 py-2.5 text-sm font-bold text-cyan-200 disabled:cursor-not-allowed disabled:opacity-40"><Eye size={16}/> Xem giao diện học sinh</button><select aria-label="Môn học" className="rounded-xl border border-white/10 bg-[#080d1d] px-4 py-2.5 text-sm text-white"><option>Gia công CNC</option></select><select aria-label="Khóa học" value={selectedCourseId ?? ""} onChange={(event)=>{setStudents([]);setActiveStudent(0);setSelectedCourseId(Number(event.target.value));}} className="rounded-xl border border-white/10 bg-[#080d1d] px-4 py-2.5 text-sm text-white"><option value="" disabled>{courses.length ? "Chọn khóa học" : "Chưa có khóa CNC"}</option>{courses.map((course)=><option key={course.id} value={course.id}>{course.name} · {course.school_year}</option>)}</select></div>
      </div>
    </section>

    <nav className="sticky top-20 z-40 flex gap-2 overflow-x-auto rounded-2xl border border-white/10 bg-[#080d1d]/95 p-2 shadow-xl backdrop-blur">{([{id:"overview",label:"Tổng quan",icon:LayoutDashboard},{id:"progress",label:"Điểm & tiến độ",icon:Route},{id:"profile",label:"Hồ sơ học sinh",icon:UserRound},{id:"competencies",label:"Năng lực & cấp quyền",icon:Award},{id:"attendance",label:"Điểm danh",icon:CalendarCheck}]as const).map(item=>{const Icon=item.icon;return <button key={item.id} onClick={()=>setActiveTab(item.id)} className={`inline-flex shrink-0 items-center gap-2 rounded-xl px-4 py-3 text-sm font-bold ${activeTab===item.id?"bg-blue-600 text-white":"text-slate-400 hover:bg-white/5 hover:text-white"}`}><Icon size={17}/>{item.label}</button>})}</nav>

    {activeTab==="attendance"&&selectedCourseId&&<TeacherAttendancePanel courseId={selectedCourseId} students={students.map(item=>({id:item.id,name:item.name,className:item.className}))}/>}
    {activeTab==="competencies"&&selectedCourseId&&<ClassCompetencyMatrix courseId={selectedCourseId} students={students.map(item=>({id:item.id,name:item.name,className:item.className,records:item.records}))}/>}

    {activeTab==="overview"&&selectedCourseId&&<TeacherOverview courseId={selectedCourseId} students={students.map(item=>({id:item.id,name:item.name,className:item.className,pct:item.pct,xp:item.xp,records:item.records}))} onOpenTab={setActiveTab} onOpenStudent={(id)=>{const index=students.findIndex(item=>item.id===id);if(index>=0)setActiveStudent(index);setActiveTab("profile")}}/>}

    {activeTab==="progress"&&<TeacherProgressGradebook students={students} selectedId={student?.id} onSelect={(id)=>{const index=students.findIndex(item=>item.id===id);if(index>=0)setActiveStudent(index)}}/>}
    {activeTab==="profile"&&selectedCourseId&&<TeacherStudentProfile courseId={selectedCourseId} students={students} selectedId={student?.id} onSelect={(id)=>{const index=students.findIndex(item=>item.id===id);if(index>=0)setActiveStudent(index)}} onRemoved={()=>{setStudents(current=>current.filter(item=>item.id!==student?.id));setActiveStudent(0)}}/>}
  </div>;
}
