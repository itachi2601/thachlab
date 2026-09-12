"use client";
import { useCallback,useEffect,useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Clock3, GraduationCap, KeyRound, LayoutDashboard, LogOut, ShieldCheck, Wrench } from "lucide-react";
import Navbar from "@/components/layout/Navbar";import Footer from "@/components/layout/Footer";import RequireAuth from "@/components/auth/RequireAuth";import {useAuth} from "@/components/auth/AuthProvider";import StudentLearningDashboard from "@/components/dashboard/StudentLearningDashboard";import StudentAttendancePanel from "@/components/attendance/StudentAttendancePanel";import {fetchMyEnrollment,requestEnrollment} from "@/services/course-enrollments";import {fetchCncLearningRecords,type CncLearningRecord} from "@/services/cnc-learning-records";import {getSubject} from "@/services/subjects";import {fetchClasses,fetchMyClassRequest,requestClassJoin,type MyClassRequest} from "@/services/classes";import type {SchoolClass} from "@/features/exams/types";

type Enrollment=Awaited<ReturnType<typeof fetchMyEnrollment>>;

function StaffAccountCard(){
  const router=useRouter();const{session,profile,signOut}=useAuth();
  const roleLabel=profile?.role==="admin"?"Quản trị viên":"Giảng viên";
  return <section className="rounded-3xl border border-white/10 bg-[#0B1020] p-8">
    <div className="flex flex-wrap items-center gap-4">
      <span className="flex h-14 w-14 shrink-0 items-center justify-center rounded-full bg-[#2563EB]/15 text-xl font-bold text-[#3B82F6]">{(profile?.full_name??"?").charAt(0).toUpperCase()}</span>
      <div>
        <h1 className="font-display text-2xl font-bold text-white">{profile?.full_name??"Tài khoản"}</h1>
        <p className="mt-1 text-sm text-slate-400">{session?.user.email}</p>
        <span className="mt-2 inline-flex items-center gap-1.5 rounded-full bg-cyan-500/10 px-3 py-1 text-xs font-bold text-cyan-300"><ShieldCheck size={13}/>{roleLabel}</span>
      </div>
    </div>
    <div className="mt-6 flex flex-wrap gap-3">
      <Link href="/dashboard" className="inline-flex items-center gap-2 rounded-xl bg-blue-600 px-5 py-2.5 text-sm font-bold text-white"><LayoutDashboard size={16}/>Vào Dashboard giáo viên</Link>
      {profile?.role==="admin"&&<Link href="/quan-tri" className="inline-flex items-center gap-2 rounded-xl border border-cyan-400/30 bg-cyan-500/10 px-5 py-2.5 text-sm font-bold text-cyan-200"><ShieldCheck size={16}/>Vào Quản trị</Link>}
      <button onClick={async()=>{await signOut();router.push("/")}} className="inline-flex items-center gap-2 rounded-xl border border-white/10 px-5 py-2.5 text-sm font-bold text-slate-300"><LogOut size={16}/>Đăng xuất</button>
    </div>
  </section>;
}

function JoinCourseForm(){
  const [code,setCode]=useState("");const [busy,setBusy]=useState(false);const [message,setMessage]=useState("");
  async function submit(event:React.FormEvent){event.preventDefault();if(!code.trim())return;setBusy(true);setMessage("");try{await requestEnrollment(code);window.location.reload();}catch(error){setMessage(error instanceof Error?error.message:"Mã khóa không hợp lệ.");}finally{setBusy(false);}}
  return <section className="rounded-3xl border border-dashed border-white/10 bg-[#0B1020] p-10 text-center">
    <KeyRound className="mx-auto text-blue-300" size={36}/>
    <h1 className="mt-4 font-display text-2xl font-bold text-white">Chưa có khóa đang học</h1>
    <p className="mt-2 text-slate-400">Nhập mã khóa do giáo viên cung cấp để gửi yêu cầu tham gia lớp.</p>
    <form onSubmit={submit} className="mx-auto mt-6 flex max-w-md flex-col gap-3 sm:flex-row">
      <input value={code} onChange={(e)=>setCode(e.target.value.toUpperCase())} placeholder="CNC-A1B2C3 hoặc TP-A1B2C3" className="min-w-0 flex-1 rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-center font-mono uppercase text-white"/>
      <button disabled={busy} className="rounded-xl bg-blue-600 px-5 py-3 text-sm font-bold text-white disabled:opacity-50">{busy?"Đang gửi…":"Gửi yêu cầu"}</button>
    </form>
    {message&&<p className="mt-4 text-sm text-amber-200">{message}</p>}
  </section>;
}

function ClassJoinPicker({onSubmitted}:{onSubmitted:()=>void}){
  const [classes,setClasses]=useState<SchoolClass[]>([]);const [selected,setSelected]=useState<number|null>(null);const [busy,setBusy]=useState(false);const [message,setMessage]=useState("");
  useEffect(()=>{fetchClasses().then(setClasses)},[]);
  async function submit(){if(!selected)return;setBusy(true);setMessage("");try{await requestClassJoin(selected);onSubmitted();}catch(error){setMessage(error instanceof Error?error.message:"Không gửi được yêu cầu.");}finally{setBusy(false);}}
  return <div className="mx-auto mt-6 max-w-md space-y-3">
    <div className="grid gap-2 sm:grid-cols-2">
      {classes.map((c)=>(
        <button key={c.id} type="button" onClick={()=>setSelected(c.id)} className={`rounded-xl border px-4 py-3 text-left text-sm font-semibold transition-colors ${selected===c.id?"border-blue-400 bg-blue-500/10 text-white":"border-white/10 text-slate-300 hover:border-white/30"}`}>
          {c.icon&&`${c.icon} `}{c.name}
        </button>
      ))}
      {classes.length===0&&<p className="col-span-2 text-sm text-slate-500">Chưa có khối lớp nào.</p>}
    </div>
    <button onClick={submit} disabled={busy||!selected} className="w-full rounded-xl bg-blue-600 px-5 py-2.5 text-sm font-bold text-white disabled:opacity-50">{busy?"Đang gửi…":"Gửi yêu cầu vào lớp"}</button>
    {message&&<p className="text-sm text-amber-200">{message}</p>}
  </div>;
}

function StudentTrackChooser({onSubmitted}:{onSubmitted:()=>void}){
  const [track,setTrack]=useState<"thpt"|"cttc"|null>(null);
  if(track==="cttc")return <JoinCourseForm/>;
  if(track==="thpt")return <section className="rounded-3xl border border-dashed border-white/10 bg-[#0B1020] p-10 text-center">
    <GraduationCap className="mx-auto text-blue-300" size={36}/>
    <h1 className="mt-4 font-display text-2xl font-bold text-white">Chọn khối lớp</h1>
    <p className="mt-2 text-slate-400">Gửi yêu cầu vào khối lớp — giáo viên sẽ duyệt trước khi bạn xem được nội dung của lớp.</p>
    <ClassJoinPicker onSubmitted={onSubmitted}/>
    <button onClick={()=>setTrack(null)} className="mt-4 text-xs text-slate-500 hover:text-slate-300">← Chọn lại luồng học</button>
  </section>;
  return <section className="rounded-3xl border border-dashed border-white/10 bg-[#0B1020] p-10 text-center">
    <h1 className="font-display text-2xl font-bold text-white">Bạn đang học ở đâu?</h1>
    <p className="mt-2 text-slate-400">Chọn đúng luồng học để vào đúng lớp / khóa của mình.</p>
    <div className="mx-auto mt-6 grid max-w-md gap-3 sm:grid-cols-2">
      <button type="button" onClick={()=>setTrack("thpt")} className="rounded-2xl border border-blue-400/20 bg-blue-500/[.06] p-5 text-left transition-colors hover:border-blue-400/40">
        <GraduationCap className="text-blue-300" size={22}/>
        <strong className="mt-2 block text-white">Học sinh THPT</strong>
        <span className="text-sm text-slate-400">Chọn khối lớp 9–12</span>
      </button>
      <button type="button" onClick={()=>setTrack("cttc")} className="rounded-2xl border border-orange-400/20 bg-orange-500/[.06] p-5 text-left transition-colors hover:border-orange-400/40">
        <Wrench className="text-orange-300" size={22}/>
        <strong className="mt-2 block text-white">Sinh viên CTTC</strong>
        <span className="text-sm text-slate-400">Nhập mã khóa CNC / Tiện – Phay</span>
      </button>
    </div>
  </section>;
}

function ClassRequestNotice({request,onRetry}:{request:MyClassRequest;onRetry:()=>void}){
  if(request.status==="pending")return <section className="rounded-3xl border border-dashed border-white/10 bg-[#0B1020] p-10 text-center"><Clock3 className="mx-auto text-amber-300" size={38}/><h1 className="mt-4 font-display text-2xl font-bold text-white">Đang chờ giáo viên duyệt</h1><p className="mt-2 text-slate-400">Yêu cầu vào lớp <strong className="text-white">{request.className}</strong> đã được gửi.</p><button onClick={onRetry} className="mt-5 rounded-full border border-white/15 px-5 py-2 text-sm text-slate-200">Kiểm tra lại</button></section>;
  if(request.status==="rejected")return <section className="rounded-3xl border border-dashed border-red-500/20 bg-[#0B1020] p-10 text-center">
    <ShieldCheck className="mx-auto text-red-300" size={38}/>
    <h1 className="mt-4 font-display text-2xl font-bold text-white">Yêu cầu chưa được duyệt</h1>
    <p className="mt-2 text-slate-400">Yêu cầu vào lớp <strong className="text-white">{request.className}</strong> đã bị từ chối. Kiểm tra lại đúng khối lớp rồi gửi lại.</p>
    <ClassJoinPicker onSubmitted={onRetry}/>
  </section>;
  return <section className="rounded-3xl border border-emerald-400/25 bg-emerald-500/10 p-6 text-center">
    <p className="text-sm text-emerald-200">Bạn thuộc lớp <strong>{request.className}</strong>.</p>
    <Link href="/lop-hoc" className="mt-3 inline-flex items-center gap-2 rounded-full bg-blue-600 px-5 py-2.5 text-sm font-bold text-white">Vào lớp học</Link>
  </section>;
}

function Account(){
  const router=useRouter();const{session,profile,signOut}=useAuth();
  const [enrollment,setEnrollment]=useState<Enrollment|null|undefined>(undefined);
  const [classRequest,setClassRequest]=useState<MyClassRequest|null|undefined>(undefined);
  const [records,setRecords]=useState<CncLearningRecord[]>([]);
  const isStaff=profile?.role==="admin"||profile?.role==="instructor";
  const reload=useCallback(()=>{
    if(!session||isStaff)return;
    fetchMyEnrollment(session.user.id).then(async result=>{const own=result?.status==="active"?await fetchCncLearningRecords(result.course.id,session.user.id).catch(()=>[]):[];return{result,own};}).then(({result,own})=>{setEnrollment(result);setRecords(own);}).catch(()=>setEnrollment(null));
    fetchMyClassRequest(session.user.id).then(setClassRequest).catch(()=>setClassRequest(null));
  },[session,isStaff]);
  useEffect(()=>{reload();},[reload]);

  if(!session)return <p className="rounded-2xl border border-white/10 bg-[#0B1020] p-6 text-slate-400">Đang tải không gian học tập…</p>;
  if(isStaff)return <StaffAccountCard/>;
  if(enrollment===undefined||classRequest===undefined)return <p className="rounded-2xl border border-white/10 bg-[#0B1020] p-6 text-slate-400">Đang tải không gian học tập…</p>;

  if(enrollment){
    if(enrollment.status==="pending")return <section className="rounded-3xl border border-dashed border-white/10 bg-[#0B1020] p-10 text-center"><Clock3 className="mx-auto text-amber-300" size={38}/><h1 className="mt-4 font-display text-2xl font-bold text-white">Đang chờ giáo viên duyệt</h1><p className="mt-2 text-slate-400">Yêu cầu tham gia <strong className="text-white">{enrollment.course.name}</strong> đã được gửi.</p><button onClick={reload} className="mt-5 rounded-full border border-white/15 px-5 py-2 text-sm text-slate-200">Kiểm tra lại</button></section>;
    if(enrollment.status==="suspended")return <section className="rounded-3xl border border-dashed border-white/10 bg-[#0B1020] p-10 text-center"><ShieldCheck className="mx-auto text-red-300" size={38}/><h1 className="mt-4 font-display text-2xl font-bold text-white">Quyền truy cập đang tạm khóa</h1><p className="mt-2 text-slate-400">Hãy liên hệ giáo viên phụ trách khóa học.</p></section>;

    const subject=getSubject(enrollment.subjectCode);
    if(subject.hasCurriculum)return <StudentLearningDashboard profile={profile} email={session.user.email} studentId={session.user.id} enrollment={{status:"active",enrolled_at:new Date().toISOString(),course:enrollment.course}} records={records} onSignOut={async()=>{await signOut();router.push("/")}}/>;
    return <><div className="mb-5 flex items-center gap-2 rounded-2xl border border-emerald-400/25 bg-emerald-500/10 px-5 py-3 text-sm text-emerald-200"><strong>{enrollment.course.name}</strong><span>· {enrollment.course.school_year}</span></div><StudentAttendancePanel courseId={enrollment.course.id} studentId={session.user.id}/></>;
  }

  if(classRequest)return <ClassRequestNotice request={classRequest} onRetry={reload}/>;
  return <StudentTrackChooser onSubmitted={reload}/>;
}

export default function AccountPage(){return <><Navbar/><main className="mx-auto min-h-screen w-full max-w-6xl px-6 pb-24 pt-28 lg:px-8"><RequireAuth><Account/></RequireAuth></main><Footer/></>}
