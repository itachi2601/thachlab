"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { BookOpenCheck, Clock3, GraduationCap, LogOut, ShieldAlert } from "lucide-react";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import RequireAuth from "@/components/auth/RequireAuth";
import { useAuth } from "@/components/auth/AuthProvider";
import { fetchMyCncEnrollments } from "@/services/course-enrollments";
import { fetchCncLearningRecords, type CncLearningRecord } from "@/services/cnc-learning-records";
import { CNC_COURSE_ITEMS } from "@/services/cnc-lms";
import StudentAttendancePanel from "@/components/attendance/StudentAttendancePanel";
import { cncAssessmentProgress } from "@/services/cnc-progress";
import StudentCompetencyCard from "@/components/competencies/StudentCompetencyCard";

type MyEnrollment=Awaited<ReturnType<typeof fetchMyCncEnrollments>>[number];
const lessons=CNC_COURSE_ITEMS.filter((item)=>item.id!=="intro");
const assessmentLabels:Record<string,string>={final:"Kiểm tra cuối bài",basic:"Bài tập 1 · Nhận biết",translate:"Bài tập 2 · Dịch lệnh",drawing:"Bài tập 4 · Bản vẽ","exercise-1":"Bài tập 1 · Nhận biết","exercise-2":"Bài tập 2 · Dịch block","exercise-3":"Bài tập 3 · Điền khuyết","exercise-4":"Bài tập 4 · Viết chương trình","exercise-5":"Bài tập 5 · Mô phỏng",safety:"Kiểm tra an toàn","machine-operation":"Bài 1 · Vận hành máy","tool-setup":"Bài 2 · Cài đặt dao"};

function Account(){
  const router=useRouter(); const{session,profile,signOut}=useAuth();
  const[enrollments,setEnrollments]=useState<MyEnrollment[]|null>(null); const[records,setRecords]=useState<CncLearningRecord[]>([]); const[error,setError]=useState("");
  useEffect(()=>{if(!session)return;let cancelled=false;fetchMyCncEnrollments(session.user.id).then(async rows=>({rows,records:(await Promise.all(rows.filter(item=>item.status==="active").map(item=>fetchCncLearningRecords(item.course.id,session.user.id).catch(()=>[])))).flat()})).then(result=>{if(!cancelled){setEnrollments(result.rows);setRecords(result.records);setError("");}}).catch(reason=>{if(!cancelled){setEnrollments([]);setError(reason&&typeof reason==="object"&&"message" in reason?String(reason.message):"Không tải được khóa học.");}});return()=>{cancelled=true};},[session]);
  const active=enrollments?.filter(item=>item.status==="active")??[]; const pending=enrollments?.filter(item=>item.status==="pending")??[]; const suspended=enrollments?.filter(item=>item.status==="suspended")??[];
  return <div className="space-y-8">
    <section className="rounded-3xl border border-white/10 bg-gradient-to-br from-[#172c46] to-[#071426] p-6 sm:p-8"><div className="flex flex-wrap items-center justify-between gap-5"><div><p className="text-xs font-bold uppercase tracking-[.16em] text-blue-300">Tài khoản sinh viên</p><h1 className="mt-2 font-display text-3xl font-bold text-white">{profile?.full_name||"Học sinh"}</h1><p className="mt-2 text-sm text-slate-400">{profile?.class_name?`Lớp ${profile.class_name} · `:""}{session?.user.email}</p></div><button onClick={async()=>{await signOut();router.push("/");}} className="inline-flex items-center gap-2 rounded-full border border-white/15 px-4 py-2 text-sm font-bold text-slate-300"><LogOut size={16}/>Đăng xuất</button></div></section>
    <section><div className="mb-4 flex items-center gap-2"><GraduationCap size={20} className="text-orange-300"/><h2 className="font-display text-2xl font-bold text-white">Khóa học đang học</h2></div>
      {enrollments===null?<p className="rounded-2xl border border-white/10 bg-[#0B1020] p-6 text-slate-400">Đang tải khóa học…</p>:active.length===0?<div className="rounded-2xl border border-dashed border-white/10 bg-[#0B1020] p-8 text-center"><BookOpenCheck className="mx-auto text-slate-500" size={32}/><p className="mt-3 text-slate-300">Em chưa tham gia khóa học nào.</p><Link href="/lop-hoc/cnc" className="mt-4 inline-flex rounded-full bg-blue-600 px-5 py-2.5 text-sm font-bold text-white">Nhập mã khóa CNC</Link></div>:<div className="space-y-4">{active.map(item=><CourseResult key={item.course.id} enrollment={item} studentId={session?.user.id??""} records={records.filter(record=>record.course_id===item.course.id)}/>)}</div>}
    </section>
    {pending.length>0&&<section><div className="mb-3 flex items-center gap-2"><Clock3 size={18} className="text-amber-300"/><h2 className="font-display text-lg font-bold text-white">Yêu cầu đang chờ</h2></div>{pending.map(item=><article key={item.course.id} className="rounded-2xl border border-amber-400/20 bg-amber-500/5 p-5"><strong className="text-white">{item.course.name}</strong><p className="text-sm text-slate-400">{item.course.class_label} · {item.course.school_year}</p></article>)}</section>}
    {suspended.length>0&&<section className="rounded-2xl border border-red-400/20 bg-red-500/5 p-5"><div className="flex items-center gap-2 text-red-200"><ShieldAlert size={18}/><strong>Khóa học đang tạm khóa</strong></div></section>}{error&&<p className="text-red-200">{error}</p>}
  </div>;
}

function CourseResult({enrollment,records,studentId}:{enrollment:MyEnrollment;records:CncLearningRecord[];studentId:string}){
  const assessmentProgress=cncAssessmentProgress(records); const pct=assessmentProgress.pct;
  return <article className="rounded-2xl border border-blue-400/20 bg-gradient-to-br from-blue-500/10 to-[#0B1020] p-5"><div className="flex flex-wrap justify-between gap-3"><div><span className="rounded-full bg-emerald-500/15 px-3 py-1 text-xs font-bold text-emerald-300">Đang học</span><h3 className="mt-4 font-display text-xl font-bold text-white">{enrollment.course.name}</h3><p className="mt-2 text-sm text-slate-400">Gia công CNC · {enrollment.course.class_label||"Chưa đặt tên lớp"} · {enrollment.course.school_year}</p><p className="mt-1 text-xs text-cyan-300">Đã đạt {assessmentProgress.passed}/{assessmentProgress.total} bài kiểm tra</p></div><strong className="text-3xl text-white">{pct}%</strong></div><div className="mt-4 h-3 overflow-hidden rounded-full bg-[#050914]"><div className="h-full bg-gradient-to-r from-blue-600 to-cyan-300" style={{width:`${pct}%`}}/></div>
    {studentId&&<><StudentAttendancePanel courseId={enrollment.course.id} studentId={studentId}/><StudentCompetencyCard courseId={enrollment.course.id} studentId={studentId} records={records}/></>}<div className="mt-5 space-y-3">{lessons.map(lesson=>{const tests=records.filter(record=>record.lesson_id===lesson.id&&record.total_questions);if(!tests.length)return null;return <section key={lesson.id} className="rounded-xl border border-white/10 bg-black/15 p-3"><strong className="text-sm text-white">{lesson.title}</strong><div className="mt-2 grid gap-2 sm:grid-cols-2">{tests.map(test=><div key={`${test.lesson_id}-${test.assessment_id}`} className="rounded-lg border border-white/10 p-3"><small className="text-slate-400">{assessmentLabels[test.assessment_id]??test.assessment_id}</small><div className="mt-1 flex justify-between"><strong className="text-white">{test.latest_score}/{test.total_questions}</strong><span className={test.completed?"text-xs font-bold text-emerald-300":"text-xs font-bold text-amber-300"}>{test.completed?"Đạt":"Chưa đạt"}</span></div><small className="text-slate-500">Cao nhất {test.best_score}/{test.total_questions} · {test.attempt_count} lần</small></div>)}</div></section>})}</div><Link href="/lop-hoc/cnc" className="mt-5 inline-flex rounded-full bg-blue-600 px-5 py-2.5 text-sm font-bold text-white">Tiếp tục học</Link></article>;
}

export default function AccountPage(){return <><Navbar/><main className="mx-auto min-h-screen w-full max-w-5xl px-6 pb-20 pt-28 lg:px-8"><RequireAuth><Account/></RequireAuth></main><Footer/></>}
