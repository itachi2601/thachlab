"use client";

import { useEffect, useState } from "react";
import { Award, CalendarCheck, Construction, FileSpreadsheet, GraduationCap, LayoutDashboard, Users2, X } from "lucide-react";
import { CNC_COURSE_ITEMS } from "@/services/cnc-lms";
import { fetchCncCourses, fetchCourseEnrollments, type CourseOffering, type EnrollmentRow } from "@/services/course-enrollments";
import { fetchCncLearningRecords, subscribeToCncLearningRecords, unsubscribeFromCncLearningRecords, type CncLearningRecord } from "@/services/cnc-learning-records";
import TeacherAttendancePanel from "@/components/attendance/TeacherAttendancePanel";
import { cncAssessmentProgress, completedCncLessons } from "@/services/cnc-progress";
import TeacherCompetencyHub from "@/components/dashboard/TeacherCompetencyHub";
import TeacherOverview from "@/components/dashboard/TeacherOverview";
import TeacherProgressGradebook from "@/components/dashboard/TeacherProgressGradebook";
import TeacherFinalGradebook from "@/components/dashboard/TeacherFinalGradebook";
import TeacherStudentProfile from "@/components/dashboard/TeacherStudentProfile";
import CourseRosterPanel from "@/components/dashboard/CourseRosterPanel";
import CncMillingLiveMonitor from "@/components/admin/CncMillingLiveMonitor";
import { SUBJECTS, getSubject } from "@/services/subjects";
import { useAuth } from "@/components/auth/AuthProvider";

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
  const { profile } = useAuth();
  const isInstructor = profile?.role === "instructor";
  const isAdmin = profile?.role === "admin";
  // Giảng viên không quen công nghệ: vào là thấy ngay điểm danh + gán máy + báo hỏng,
  // thay vì tab Tổng quan nhiều biểu đồ/chỉ số họ chưa cần đến.
  const [activeTab,setActiveTab]=useState<"overview"|"grades"|"competencies"|"attendance"|"roster">(isInstructor?"attendance":"overview");
  // Gộp "Điểm & tiến độ" + "Tổng kết điểm" thành 1 tab Bảng điểm với 2 chế độ xem.
  const [gradeView,setGradeView]=useState<"process"|"final">("process");
  // Hồ sơ học sinh mở dạng drawer thay vì tab riêng.
  const [profileOpen,setProfileOpen]=useState(false);
  // Phòng thi trực tiếp CNC: overlay toàn màn hình, dữ liệu toàn hệ thống (không theo lớp).
  const [liveExamOpen,setLiveExamOpen]=useState(false);
  const [activeStudent, setActiveStudent] = useState(0);
  // Môn lý thuyết ("khac") không có chương trình học nhưng vẫn cần tab Nhập danh sách & điểm.
  const availableSubjects = isInstructor ? SUBJECTS.filter((item) => item.isPracticum || item.code === "khac") : SUBJECTS;
  const [subjectCode, setSubjectCode] = useState<string>(availableSubjects[0]?.code ?? SUBJECTS[0].code);
  const [courses, setCourses] = useState<CourseOffering[]>([]);
  const [selectedCourseId, setSelectedCourseId] = useState<number | null>(null);
  const [students, setStudents] = useState<DashboardStudent[]>([]);
  const [courseError, setCourseError] = useState("");
  const student = students[activeStudent] ?? null;
  const selectedCourse = courses.find((course) => course.id === selectedCourseId) ?? null;
  const subject = getSubject(subjectCode);

  const openProfile = (id: string) => {
    const index = students.findIndex((item) => item.id === id);
    if (index >= 0) setActiveStudent(index);
    setProfileOpen(true);
  };

  const [coursesNonce, setCoursesNonce] = useState(0);
  useEffect(() => {
    let cancelled = false;
    fetchCncCourses(subjectCode)
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
  }, [subjectCode, coursesNonce]);

  // Bump để nạp lại danh sách học sinh sau khi nhập danh sách từ Excel (tab Nhập danh sách & điểm).
  const [studentsNonce, setStudentsNonce] = useState(0);
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
  }, [selectedCourseId, studentsNonce]);

  return <div className="teacher-dashboard space-y-6">
    <section className="relative overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-[#172c46] via-[#0e1c32] to-[#071426] p-6 sm:p-8">
      <div className="absolute -right-20 -top-24 h-64 w-64 rounded-full bg-orange-500/10 blur-3xl" />
      <div className="relative">
        <p className="text-xs font-bold uppercase tracking-[.16em] text-orange-300">Dashboard giáo viên</p>
        <h2 className="mt-2 font-display text-2xl font-bold text-white">Chào {profile?.full_name || "thầy/cô"} 👋</h2>
        <p className="mt-2 text-sm text-slate-400">{selectedCourse ? `Đang xem ${selectedCourse.class_label || selectedCourse.name} · ${selectedCourse.school_year} · ${students.length} học sinh` : "Chọn môn học và lớp bên dưới để bắt đầu theo dõi học sinh."}</p>
        {courseError&&<p className="mt-2 text-xs text-red-300">{courseError}</p>}
      </div>
    </section>

    <section className="grid gap-3 rounded-2xl border border-white/10 bg-[#0B1020] p-4 sm:grid-cols-2 sm:p-5">
      <label className="block">
        <span className="mb-1.5 flex items-center gap-1.5 text-xs font-bold uppercase tracking-wide text-slate-400"><GraduationCap size={14}/> Môn học</span>
        <select aria-label="Môn học" value={subjectCode} onChange={(event)=>{setCourses([]);setSelectedCourseId(null);setSubjectCode(event.target.value);}} className="w-full rounded-xl border border-white/10 bg-[#080d1d] px-4 py-3 text-sm font-semibold text-white">
          {availableSubjects.map((item)=><option key={item.code} value={item.code}>{item.label}</option>)}
        </select>
      </label>
      <label className="block">
        <span className="mb-1.5 flex items-center gap-1.5 text-xs font-bold uppercase tracking-wide text-slate-400"><Users2 size={14}/> Lớp đang dạy{courses.length>0 && ` · ${courses.length} lớp`}</span>
        <select aria-label="Lớp đang dạy" value={selectedCourseId ?? ""} onChange={(event)=>{setStudents([]);setActiveStudent(0);setSelectedCourseId(Number(event.target.value));}} className="w-full rounded-xl border border-white/10 bg-[#080d1d] px-4 py-3 text-sm font-semibold text-white">
          <option value="" disabled>{courses.length ? "Chọn lớp đang dạy" : "Chưa có lớp nào"}</option>
          {courses.map((course)=><option key={course.id} value={course.id}>{course.class_label || course.name} · {course.school_year}</option>)}
        </select>
      </label>
    </section>

    <nav className="sticky top-20 z-40 flex gap-2 overflow-x-auto rounded-2xl border border-white/10 bg-[#080d1d]/95 p-2 shadow-xl backdrop-blur">{([{id:"overview",label:"Tổng quan",icon:LayoutDashboard},{id:"grades",label:"Bảng điểm",icon:GraduationCap},{id:"competencies",label:"Chấm & cấp quyền",icon:Award},{id:"attendance",label:"Điểm danh",icon:CalendarCheck},{id:"roster",label:"Danh sách lớp",icon:FileSpreadsheet}] as const).map(item=>{const Icon=item.icon;return <button key={item.id} onClick={()=>setActiveTab(item.id)} className={`inline-flex shrink-0 items-center gap-2 rounded-xl px-4 py-3 text-sm font-bold ${activeTab===item.id?"bg-blue-600 text-white":"text-slate-400 hover:bg-white/5 hover:text-white"}`}><Icon size={17}/>{item.label}</button>})}</nav>

    {activeTab==="attendance"&&selectedCourseId&&<TeacherAttendancePanel courseId={selectedCourseId} students={students.map(item=>({id:item.id,name:item.name,className:item.className}))} workshop={subject.workshop}/>}
    {activeTab==="competencies"&&selectedCourseId&&(subject.hasCurriculum?<TeacherCompetencyHub courseId={selectedCourseId} students={students.map(item=>({id:item.id,name:item.name,className:item.className,records:item.records}))}/>:<CurriculumPending subjectLabel={subject.label}/>)}

    {activeTab==="overview"&&selectedCourseId&&(subject.hasCurriculum?<TeacherOverview courseId={selectedCourseId} students={students.map(item=>({id:item.id,name:item.name,className:item.className,pct:item.pct,xp:item.xp,records:item.records}))} onOpenTab={setActiveTab} onOpenStudent={openProfile} onOpenLiveExam={()=>setLiveExamOpen(true)}/>:<CurriculumPending subjectLabel={subject.label}/>)}

    {activeTab==="grades"&&selectedCourseId&&(subject.hasCurriculum?<div className="space-y-4">
      <div className="flex w-fit rounded-xl border border-white/10 bg-black/20 p-1">{([["process","Quá trình"],["final","Tổng kết học phần"]] as const).map(([id,label])=><button key={id} onClick={()=>setGradeView(id)} className={`rounded-lg px-4 py-2 text-sm font-bold transition ${gradeView===id?"bg-blue-600 text-white":"text-slate-400 hover:text-white"}`}>{label}</button>)}</div>
      {gradeView==="process"
        ? <TeacherProgressGradebook students={students} selectedId={student?.id} onSelect={openProfile}/>
        : <TeacherFinalGradebook courseId={selectedCourseId} students={students.map(item=>({id:item.id,name:item.name,className:item.className,records:item.records}))}/>}
    </div>:<CurriculumPending subjectLabel={subject.label}/>)}

    {activeTab==="roster"&&(selectedCourseId&&selectedCourse?<CourseRosterPanel courseId={selectedCourseId} courseName={selectedCourse.name} classLabel={selectedCourse.class_label} schoolYear={selectedCourse.school_year} subjectLabel={subject.label} subjectCode={subjectCode} isPracticum={subject.isPracticum} isAdmin={isAdmin} joinCode={selectedCourse.join_code} onImported={()=>setStudentsNonce((n)=>n+1)} onCourseCreated={()=>setCoursesNonce((n)=>n+1)} onEnrollmentChange={()=>setStudentsNonce((n)=>n+1)}/>:<div className="rounded-2xl border border-dashed border-white/10 bg-[#0B1020] p-10 text-center text-sm text-slate-500">Chọn môn học và lớp bên trên để nhập danh sách.</div>)}

    {profileOpen&&selectedCourseId&&subject.hasCurriculum&&<>
      <div className="fixed inset-0 z-40 bg-black/60 backdrop-blur-sm" onClick={()=>setProfileOpen(false)}/>
      <aside className="fixed inset-y-0 right-0 z-50 w-full max-w-2xl overflow-y-auto border-l border-white/10 bg-[#080d1d] p-5 shadow-2xl">
        <div className="mb-4 flex justify-end"><button onClick={()=>setProfileOpen(false)} className="inline-flex items-center gap-1.5 rounded-full border border-white/10 px-3 py-2 text-xs font-bold text-slate-300 hover:bg-white/5"><X size={14}/>Đóng</button></div>
        <TeacherStudentProfile courseId={selectedCourseId} students={students} selectedId={student?.id} onSelect={openProfile} onRemoved={()=>{setStudents(current=>current.filter(item=>item.id!==student?.id));setActiveStudent(0);setProfileOpen(false)}}/>
      </aside>
    </>}

    {liveExamOpen&&<div className="fixed inset-0 z-[60] overflow-y-auto bg-[#070b16] p-4 sm:p-6">
      <div className="mx-auto max-w-6xl">
        <div className="mb-4 flex justify-end"><button onClick={()=>setLiveExamOpen(false)} className="inline-flex items-center gap-1.5 rounded-full border border-white/10 px-3 py-2 text-xs font-bold text-slate-300 hover:bg-white/5"><X size={14}/>Đóng phòng thi</button></div>
        <CncMillingLiveMonitor/>
      </div>
    </div>}
  </div>;
}

function CurriculumPending({ subjectLabel }: { subjectLabel: string }) {
  return <div className="rounded-2xl border border-dashed border-white/10 bg-[#0B1020] p-10 text-center">
    <Construction size={28} className="mx-auto text-amber-300" />
    <p className="mt-3 text-sm font-bold text-white">Nội dung cho môn {subjectLabel} đang được xây dựng</p>
    <p className="mt-1 text-sm text-slate-500">Tab này cần dữ liệu chương trình học (bài giảng, năng lực, thang điểm) riêng cho môn. Trong lúc chờ, hãy dùng tab Điểm danh để theo dõi lớp.</p>
  </div>;
}
