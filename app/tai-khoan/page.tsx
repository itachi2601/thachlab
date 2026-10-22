"use client";
import StudentCodeField from "@/components/dashboard/StudentCodeField";
import { useCallback,useEffect,useRef,useState } from "react";
import { useRouter } from "next/navigation";
import dynamic from "next/dynamic";
import { LazyErrorBoundary } from "@/components/ui/LazyErrorBoundary";
import Link from "next/link";
import { ArrowRight, Clock3, GraduationCap, KeyRound, LayoutDashboard, LogOut, ShieldCheck, Users, Wrench } from "lucide-react";
import Navbar from "@/components/layout/Navbar";import Footer from "@/components/layout/Footer";import RequireAuth from "@/components/auth/RequireAuth";import {useAuth} from "@/components/auth/AuthProvider";import StudentLearningDashboard from "@/components/dashboard/StudentLearningDashboardLazy";import ThptStudentHome from "@/components/dashboard/ThptStudentHomeLazy";import ProfileEditCard from "@/components/account/ProfileEditCard";import WelcomePanel,{type WelcomeVariant} from "@/components/account/WelcomePanel";import StudentAttendancePanel from "@/components/attendance/StudentAttendancePanelLazy";import HomeroomStudentHome from "@/components/dashboard/HomeroomStudentHomeLazy";import {fetchMyEnrollments,requestEnrollment} from "@/services/course-enrollments";import {fetchCncLearningRecords,type CncLearningRecord} from "@/services/cnc-learning-records";import CttcStreakCard from "@/components/rank/CttcStreakCard";import {getSubject,HOMEROOM_SUBJECT_CODE,learningHrefOf} from "@/services/subjects";import {fetchClasses,fetchMyClassRequest,requestClassJoin,type MyClassRequest} from "@/services/classes";import type {SchoolClass} from "@/features/exams/types";

const StaffWeekPlan=dynamic(()=>import("@/components/account/StaffWeekPlan"),{ssr:false});
const DailyReminderCard=dynamic(()=>import("@/components/pwa/DailyReminderCard"),{ssr:false});

type Enrollment=Awaited<ReturnType<typeof fetchMyEnrollments>>[number];

function StaffAccountCard(){
  const router=useRouter();const{session,profile,signOut}=useAuth();
  const roleLabel=profile?.role==="admin"?"Quản trị viên":"Giảng viên";
  return <section className="rounded-3xl border border-line bg-panel p-8">
    <div className="flex flex-wrap items-center gap-4">
      <span className="flex h-14 w-14 shrink-0 items-center justify-center rounded-full bg-primary/15 text-xl font-bold text-primary">{(profile?.full_name??"?").charAt(0).toUpperCase()}</span>
      <div>
        <h1 className="font-display text-2xl font-bold text-ink">{profile?.full_name??"Tài khoản"}</h1>
        <p className="mt-1 text-sm text-muted">{session?.user.email}</p>
        <span className="mt-2 inline-flex items-center gap-1.5 rounded-full bg-primary-soft px-3 py-1 text-xs font-bold text-primary"><ShieldCheck size={13}/>{roleLabel}</span>
      </div>
    </div>
    <div className="mt-6 flex flex-wrap gap-3">
      <Link href="/dashboard" className="inline-flex items-center gap-2 rounded-xl bg-blue-600 px-5 py-2.5 text-sm font-bold text-white"><LayoutDashboard size={16}/>Vào Dashboard giáo viên</Link>
      {profile?.role==="admin"&&<Link href="/quan-tri" className="inline-flex items-center gap-2 rounded-xl border border-primary/30 bg-primary-soft px-5 py-2.5 text-sm font-bold text-primary"><ShieldCheck size={16}/>Vào Quản trị</Link>}
      <button onClick={async()=>{await signOut();router.push("/")}} className="inline-flex items-center gap-2 rounded-xl border border-line px-5 py-2.5 text-sm font-bold text-ink"><LogOut size={16}/>Đăng xuất</button>
    </div>
  </section>;
}

function ParentAccountCard(){
  const router=useRouter();const{session,profile,signOut}=useAuth();
  return <section className="rounded-3xl border border-line bg-panel p-8">
    <div className="flex flex-wrap items-center gap-4">
      <span className="flex h-14 w-14 shrink-0 items-center justify-center rounded-full bg-primary/15 text-xl font-bold text-primary">{(profile?.full_name??"?").charAt(0).toUpperCase()}</span>
      <div>
        <h1 className="font-display text-2xl font-bold text-ink">{profile?.full_name??"Tài khoản"}</h1>
        <p className="mt-1 text-sm text-muted">{session?.user.email}</p>
        <span className="mt-2 inline-flex items-center gap-1.5 rounded-full bg-emerald-500/10 px-3 py-1 text-xs font-bold text-emerald-300"><Users size={13}/>Phụ huynh</span>
      </div>
    </div>
    <div className="mt-6 flex flex-wrap gap-3">
      <Link href="/phu-huynh" className="inline-flex items-center gap-2 rounded-xl bg-blue-600 px-5 py-2.5 text-sm font-bold text-white"><Users size={16}/>Xem kết quả của con</Link>
      <button onClick={async()=>{await signOut();router.push("/")}} className="inline-flex items-center gap-2 rounded-xl border border-line px-5 py-2.5 text-sm font-bold text-ink"><LogOut size={16}/>Đăng xuất</button>
    </div>
  </section>;
}

function JoinCourseForm(){
  const [code,setCode]=useState("");const [busy,setBusy]=useState(false);const [message,setMessage]=useState("");
  async function submit(event:React.FormEvent){event.preventDefault();if(!code.trim())return;setBusy(true);setMessage("");try{await requestEnrollment(code);window.location.reload();}catch(error){setMessage(error instanceof Error?error.message:"Mã khóa không hợp lệ.");}finally{setBusy(false);}}
  return <section className="rounded-3xl border border-dashed border-orange-400/20 bg-panel p-10 text-center">
    <KeyRound className="mx-auto text-orange-300" size={36}/>
    <h1 className="mt-4 font-display text-2xl font-bold text-ink">Chưa có khóa đang học</h1>
    <p className="mt-2 text-muted">Sinh viên CTTC — nhập mã khóa do giảng viên cung cấp để gửi yêu cầu tham gia lớp.</p>
    <form onSubmit={submit} className="mx-auto mt-6 flex max-w-md flex-col gap-3 sm:flex-row">
      <input value={code} onChange={(e)=>setCode(e.target.value.toUpperCase())} placeholder="CNC-A1B2C3 hoặc TP-A1B2C3" className="min-w-0 flex-1 rounded-xl border border-line-strong bg-surface-2 px-4 py-3 text-center font-mono uppercase text-ink"/>
      <button disabled={busy} className="rounded-xl bg-orange-600 px-5 py-3 text-sm font-bold text-white disabled:opacity-50">{busy?"Đang gửi…":"Gửi yêu cầu"}</button>
    </form>
    {message&&<p className="mt-4 text-sm text-amber-200">{message}</p>}
  </section>;
}

function TrackStatusCard({track,icon:Icon,title,desc,action}:{track:"thpt"|"cttc";icon:typeof Clock3;title:string;desc:React.ReactNode;action?:React.ReactNode}){
  const accent=track==="cttc"?"border-orange-400/25 text-orange-300":"border-blue-400/25 text-blue-300";
  const [borderClass,textClass]=accent.split(" ");
  return <section className={`rounded-3xl border border-dashed ${borderClass} bg-panel p-10 text-center`}>
    <Icon className={`mx-auto ${textClass}`} size={38}/>
    <h1 className="mt-4 font-display text-2xl font-bold text-ink">{title}</h1>
    <p className="mt-2 text-muted">{desc}</p>
    {action}
  </section>;
}

function ClassJoinPicker({onSubmitted}:{onSubmitted:()=>void}){
  const [classes,setClasses]=useState<SchoolClass[]>([]);const [selected,setSelected]=useState<number|null>(null);const [busy,setBusy]=useState(false);const [message,setMessage]=useState("");
  useEffect(()=>{fetchClasses().then(setClasses)},[]);
  async function submit(){if(!selected)return;setBusy(true);setMessage("");try{await requestClassJoin(selected);onSubmitted();}catch(error){setMessage(error instanceof Error?error.message:"Không gửi được yêu cầu.");}finally{setBusy(false);}}
  return <div className="mx-auto mt-6 max-w-md space-y-3">
    <div className="grid gap-2 sm:grid-cols-2">
      {classes.map((c)=>(
        <button key={c.id} type="button" onClick={()=>setSelected(c.id)} className={`rounded-xl border px-4 py-3 text-left text-sm font-semibold transition-colors ${selected===c.id?"border-primary bg-primary-soft text-ink":"border-line text-ink hover:border-line-strong"}`}>
          {c.icon&&`${c.icon} `}{c.name}
        </button>
      ))}
      {classes.length===0&&<p className="col-span-2 text-sm text-slate-500">Chưa có khối lớp nào.</p>}
    </div>
    <button onClick={submit} disabled={busy||!selected} className="w-full rounded-xl bg-blue-600 px-5 py-2.5 text-sm font-bold text-white disabled:opacity-50">{busy?"Đang vào lớp…":"Vào lớp"}</button>
    {message&&<p className="text-sm text-amber-200">{message}</p>}
  </div>;
}

function StudentTrackChooser({onSubmitted}:{onSubmitted:()=>void}){
  const [track,setTrack]=useState<"thpt"|"cttc"|null>(null);
  if(track==="cttc")return <JoinCourseForm/>;
  if(track==="thpt")return <section className="rounded-3xl border border-dashed border-line bg-panel p-10 text-center">
    <GraduationCap className="mx-auto text-blue-300" size={36}/>
    <h1 className="mt-4 font-display text-2xl font-bold text-ink">Chọn khối lớp</h1>
    <p className="mt-2 text-muted">Chọn khối lớp của bạn để vào lớp ngay, không cần chờ duyệt.</p>
    <ClassJoinPicker onSubmitted={onSubmitted}/>
    <button onClick={()=>setTrack(null)} className="mt-4 text-xs text-slate-500 hover:text-ink">← Chọn lại luồng học</button>
  </section>;
  return <section className="rounded-3xl border border-dashed border-line bg-panel p-10 text-center">
    <h1 className="font-display text-2xl font-bold text-ink">Bạn đang học ở đâu?</h1>
    <p className="mt-2 text-muted">Chọn đúng luồng học để vào đúng lớp / khóa của mình.</p>
    <div className="mx-auto mt-6 grid max-w-md gap-3 sm:grid-cols-2">
      <button type="button" onClick={()=>setTrack("thpt")} className="rounded-2xl border border-blue-400/20 bg-blue-500/[.06] p-5 text-left transition-colors hover:border-blue-400/40">
        <GraduationCap className="text-blue-300" size={22}/>
        <strong className="mt-2 block text-ink">Học sinh THPT</strong>
        <span className="text-sm text-muted">Chọn khối lớp 9–12</span>
      </button>
      <button type="button" onClick={()=>setTrack("cttc")} className="rounded-2xl border border-orange-400/20 bg-orange-500/[.06] p-5 text-left transition-colors hover:border-orange-400/40">
        <Wrench className="text-orange-300" size={22}/>
        <strong className="mt-2 block text-ink">Sinh viên CTTC</strong>
        <span className="text-sm text-muted">Nhập mã khóa CNC / Tiện – Phay</span>
      </button>
    </div>
  </section>;
}

function CourseSwitcher({enrollments,currentId,onPick}:{enrollments:Enrollment[];currentId:number|null;onPick:(id:number)=>void}){
  const [code,setCode]=useState("");const [busy,setBusy]=useState(false);const [message,setMessage]=useState("");
  async function submit(event:React.FormEvent){event.preventDefault();if(!code.trim())return;setBusy(true);setMessage("");try{const r=await requestEnrollment(code);try{window.localStorage.setItem("tl-tai-khoan-lop",String(r.course_id));}catch{}window.location.reload();}catch(error){setMessage(error instanceof Error?error.message:"Mã khóa không hợp lệ.");setBusy(false);}}
  return <section className="mb-5 rounded-2xl border border-line bg-panel p-4">
    {enrollments.length>1&&<div className="flex flex-wrap gap-2" role="tablist" aria-label="Lớp đang học">
      {enrollments.map(e=><button key={e.course.id} type="button" role="tab" aria-selected={e.course.id===currentId} onClick={()=>onPick(e.course.id)} className={`min-h-11 rounded-xl border px-4 py-2 text-left text-sm font-semibold ${e.course.id===currentId?"border-primary bg-primary-soft text-ink":"border-line text-ink hover:border-line-strong"}`}>{e.subjectName}<span className="block text-xs font-normal">{e.course.class_label}{e.status==="pending"?" · chờ duyệt":""}</span></button>)}
    </div>}
    <details className={enrollments.length>1?"mt-3":""}>
      <summary className="min-h-11 cursor-pointer py-2 text-sm font-semibold text-ink">+ Nhập mã để học thêm lớp khác</summary>
      <form onSubmit={submit} className="flex flex-col gap-2 pt-2 sm:flex-row">
        <input value={code} onChange={(e)=>setCode(e.target.value.toUpperCase())} placeholder="Ví dụ AVCN-CK23A" className="min-h-11 min-w-0 flex-1 rounded-xl border border-line-strong bg-surface-2 px-4 py-2 font-mono uppercase text-ink"/>
        <button disabled={busy} className="min-h-11 rounded-xl bg-orange-600 px-5 py-2 text-sm font-bold text-white disabled:opacity-50">{busy?"Đang gửi…":"Gửi yêu cầu"}</button>
      </form>
      {message&&<p className="pt-2 text-sm text-amber-200">{message}</p>}
    </details>
  </section>;
}

function ClassRequestNotice({request,onRetry}:{request:MyClassRequest;onRetry:()=>void}){
  if(request.status==="pending")return <TrackStatusCard track="thpt" icon={Clock3} title="Đang chờ giáo viên duyệt" desc={<>Yêu cầu vào lớp <strong className="text-ink">{request.className}</strong> đã được gửi.</>} action={<button onClick={onRetry} className="mt-5 rounded-full border border-line px-5 py-2 text-sm text-ink">Kiểm tra lại</button>}/>;
  if(request.status==="rejected")return <section className="rounded-3xl border border-dashed border-red-500/20 bg-panel p-10 text-center">
    <ShieldCheck className="mx-auto text-red-300" size={38}/>
    <h1 className="mt-4 font-display text-2xl font-bold text-ink">Yêu cầu chưa được duyệt</h1>
    <p className="mt-2 text-muted">Yêu cầu vào lớp <strong className="text-ink">{request.className}</strong> đã bị từ chối. Chọn lại đúng khối lớp để vào.</p>
    <ClassJoinPicker onSubmitted={onRetry}/>
  </section>;
  return null;
}

const PREVIEW_CLASS_KEY="tl-preview-thpt-class";
function PreviewThptHome({studentId,profile,onSignOut}:{studentId:string;profile:ReturnType<typeof useAuth>["profile"];onSignOut:()=>void}){
  const [classes,setClasses]=useState<SchoolClass[]|null>(null);const [classId,setClassId]=useState<number|null>(null);
  useEffect(()=>{fetchClasses().then(cs=>{setClasses(cs);let saved=0;try{saved=Number(window.sessionStorage.getItem(PREVIEW_CLASS_KEY));}catch{}setClassId(cs.find(c=>c.id===saved)?.id??cs[0]?.id??null);}).catch(()=>setClasses([]));},[]);
  function pick(id:number){setClassId(id);try{window.sessionStorage.setItem(PREVIEW_CLASS_KEY,String(id));}catch{}}
  if(classes===null)return <p className="rounded-2xl border border-line bg-panel p-6 text-muted">Đang tải lớp giả lập…</p>;
  const current=classes.find(c=>c.id===classId);
  if(!current)return <p className="rounded-2xl border border-line bg-panel p-6 text-muted">Chưa có khối lớp nào để xem thử.</p>;
  return <>
    <label className="mb-3 flex items-center gap-3 rounded-2xl border border-fuchsia-400/30 bg-panel px-3 py-2 text-[13px] font-semibold text-ink">
      Xem thử lớp
      <select value={current.id} onChange={e=>pick(Number(e.target.value))} className="min-h-11 min-w-0 flex-1 rounded-xl border border-line-strong bg-surface-2 px-3 text-sm text-ink">
        {classes.map(c=><option key={c.id} value={c.id}>{c.icon?`${c.icon} `:""}{c.name}</option>)}
      </select>
    </label>
    <ThptStudentHome key={current.id} profile={profile} studentId={studentId} classId={current.id} className={current.name} onSignOut={onSignOut}/>
  </>;
}

function Account(){
  const router=useRouter();const{session,profile,signOut,previewMode}=useAuth();
  const [enrollments,setEnrollments]=useState<Enrollment[]|undefined>(undefined);
  const [pickedCourseId,setPickedCourseId]=useState<number|null>(()=>{try{const v=Number(window.localStorage.getItem("tl-tai-khoan-lop"));return v>0?v:null;}catch{return null;}});
  const enrollment:Enrollment|null|undefined=enrollments===undefined?undefined:(enrollments.find(e=>e.course.id===pickedCourseId)??enrollments[0]??null);
  const pickCourse=(id:number)=>{setPickedCourseId(id);try{window.localStorage.setItem("tl-tai-khoan-lop",String(id));}catch{}};
  const [classRequest,setClassRequest]=useState<MyClassRequest|null|undefined>(undefined);
  const [recordsState,setRecordsState]=useState<{courseId:number;items:CncLearningRecord[]}|null>(null);
  const isStaff=profile?.role==="admin"||profile?.role==="instructor";
  const isParent=profile?.role==="parent";
  const reload=useCallback(()=>{
    if(!session||isStaff||isParent||previewMode==="student")return;
    fetchMyEnrollments(session.user.id).then(setEnrollments).catch(()=>setEnrollments([]));
    fetchMyClassRequest(session.user.id).then(setClassRequest).catch(()=>setClassRequest(null));
  },[session,isStaff,isParent,previewMode]);
  useEffect(()=>{reload();},[reload]);
  // Link mời vào lớp học phần: /tai-khoan?ma=AVCN-CK23A → tự gửi yêu cầu bằng mã đó (một lần), rồi gỡ ?ma khỏi địa chỉ.
  const inviteDone=useRef(false);
  useEffect(()=>{
    if(!session||isStaff||isParent||enrollments===undefined||inviteDone.current)return;
    const ma=new URLSearchParams(window.location.search).get("ma")?.trim().toUpperCase();
    if(!ma)return;
    inviteDone.current=true;
    requestEnrollment(ma).then(r=>{try{window.localStorage.setItem("tl-tai-khoan-lop",String(r.course_id));}catch{}}).catch(()=>undefined).finally(()=>{window.history.replaceState(null,"",window.location.pathname);reload();});
  },[session,isStaff,isParent,enrollments,reload]);
  const activeCourseId=enrollment?.status==="active"?enrollment.course.id:null;
  useEffect(()=>{
    if(!session||activeCourseId===null)return;
    let cancelled=false;
    fetchCncLearningRecords(activeCourseId,session.user.id).catch(()=>[]).then(own=>{if(!cancelled)setRecordsState({courseId:activeCourseId,items:own});});
    return()=>{cancelled=true;};
  },[session,activeCourseId]);
  const records:CncLearningRecord[]=activeCourseId!==null&&recordsState!==null&&recordsState.courseId===activeCourseId?recordsState.items:[];

  if(!session)return <p className="rounded-2xl border border-line bg-panel p-6 text-muted">Đang tải không gian học tập…</p>;
  const welcome=(v:WelcomeVariant)=><WelcomePanel variant={v} userId={session.user.id} name={profile?.full_name} loginKey={v==="welcome_back"?session.user.last_sign_in_at:undefined}/>;
  if(isStaff)return <>{welcome(profile?.role==="admin"?"admin":"instructor")}<StaffAccountCard/><LazyErrorBoundary><StaffWeekPlan/></LazyErrorBoundary></>;
  if(isParent)return <>{welcome("parent")}<ParentAccountCard/></>;
  // Admin bấm "Xem như học sinh": chỉ đường THPT, chọn lớp giả lập — không đọc/ghi user_classes hay course_enrollments của admin (trước đây lẫn nhánh CTTC).
  if(previewMode==="student")return <PreviewThptHome studentId={session.user.id} profile={profile} onSignOut={async()=>{await signOut();router.push("/")}}/>;
  if(enrollment===undefined||classRequest===undefined)return <p className="rounded-2xl border border-line bg-panel p-6 text-muted">Đang tải không gian học tập…</p>;

  const track=profile?.track??null;
  const cttcStatus=enrollment?.status;
  const thptStatus=classRequest?.status;
  const variant:WelcomeVariant=profile?.role==="tro_giang"?"tro_giang"
    :track==="cttc"||(track!=="thpt"&&cttcStatus&&!thptStatus)
      ?(cttcStatus==="active"?"cttc_active":cttcStatus==="pending"?"cttc_pending":"cttc_join")
    :thptStatus==="active"?"thpt_active"
    :thptStatus==="pending"?"thpt_pending"
    :track==="thpt"?"thpt_pick_class":"student_new";
  const body=(()=>{

  // Hệ CTTC (profiles.track='cttc') — chỉ nhìn vào course_enrollments, bỏ qua mọi user_classes cũ/lẫn.
  if(track==="cttc"){
    if(!enrollment)return <JoinCourseForm/>;
    if(enrollment.status==="pending")return <TrackStatusCard track="cttc" icon={Clock3} title="Đang chờ giảng viên duyệt" desc={<>Yêu cầu tham gia <strong className="text-ink">{enrollment.course.name}</strong> đã được gửi.</>} action={<button onClick={reload} className="mt-5 rounded-full border border-line px-5 py-2 text-sm text-ink">Kiểm tra lại</button>}/>;
    if(enrollment.status==="suspended")return <TrackStatusCard track="cttc" icon={ShieldCheck} title="Quyền truy cập đang tạm khóa" desc="Hãy liên hệ giảng viên phụ trách khóa học."/>;
    if(enrollment.status==="rejected"||enrollment.status==="left"||enrollment.status==="completed")return <JoinCourseForm/>;

    const subject=getSubject(enrollment.subjectCode);
    if(subject.hasCurriculum)return <StudentLearningDashboard profile={profile} email={session.user.email} studentId={session.user.id} enrollment={{status:"active",enrolled_at:new Date().toISOString(),course:enrollment.course}} records={records} onSignOut={async()=>{await signOut();router.push("/")}}/>;
    // Lớp chủ nhiệm: xem lại nội dung sinh hoạt tuần, điểm danh của mình, và điểm danh hộ cả lớp nếu là lớp trưởng.
    if(enrollment.subjectCode===HOMEROOM_SUBJECT_CODE)return <HomeroomStudentHome courseId={enrollment.course.id} courseName={enrollment.course.name} schoolYear={enrollment.course.school_year} studentId={session.user.id}/>;
    return <><div className="mb-5 flex items-center gap-2 rounded-2xl border border-emerald-400/25 bg-emerald-500/10 px-5 py-3 text-sm text-emerald-200"><strong>{enrollment.course.name}</strong><span>· {enrollment.course.school_year}</span></div><div className="mb-5"><StudentCodeField studentId={session.user.id}/></div>{learningHrefOf(enrollment.subjectCode)!=="/tai-khoan"&&<Link href={learningHrefOf(enrollment.subjectCode)} className="mb-5 flex min-h-14 items-center justify-between rounded-2xl bg-primary px-5 py-3 font-semibold text-white">Vào bài học<ArrowRight size={18}/></Link>}<CttcStreakCard className="mb-5"/><StudentAttendancePanel courseId={enrollment.course.id} studentId={session.user.id}/></>;
  }

  // Hệ THPT (profiles.track='thpt') — chỉ nhìn vào user_classes, bỏ qua mọi course_enrollments cũ/lẫn.
  if(track==="thpt"){
    if(classRequest?.status==="active")return <ThptStudentHome profile={profile} email={session.user.email} studentId={session.user.id} classId={classRequest.classId} className={classRequest.className} onSignOut={async()=>{await signOut();router.push("/")}}/>;
    if(classRequest)return <ClassRequestNotice request={classRequest} onRetry={reload}/>;
    return <section className="rounded-3xl border border-dashed border-blue-400/20 bg-panel p-10 text-center">
      <GraduationCap className="mx-auto text-blue-300" size={36}/>
      <h1 className="mt-4 font-display text-2xl font-bold text-ink">Chọn khối lớp</h1>
      <p className="mt-2 text-muted">Chọn khối lớp của bạn để vào lớp ngay, không cần chờ duyệt.</p>
      <ClassJoinPicker onSubmitted={reload}/>
    </section>;
  }

  // Track chưa xác định (tài khoản mới, chưa từng gửi yêu cầu nào ở cả 2 hệ) — dùng logic gộp cũ để không khoá nhầm ai.
  if(enrollment){
    if(enrollment.status==="pending")return <TrackStatusCard track="cttc" icon={Clock3} title="Đang chờ giáo viên duyệt" desc={<>Yêu cầu tham gia <strong className="text-ink">{enrollment.course.name}</strong> đã được gửi.</>} action={<button onClick={reload} className="mt-5 rounded-full border border-line px-5 py-2 text-sm text-ink">Kiểm tra lại</button>}/>;
    if(enrollment.status==="suspended")return <TrackStatusCard track="cttc" icon={ShieldCheck} title="Quyền truy cập đang tạm khóa" desc="Hãy liên hệ giáo viên phụ trách khóa học."/>;

    const subject=getSubject(enrollment.subjectCode);
    if(subject.hasCurriculum)return <StudentLearningDashboard profile={profile} email={session.user.email} studentId={session.user.id} enrollment={{status:"active",enrolled_at:new Date().toISOString(),course:enrollment.course}} records={records} onSignOut={async()=>{await signOut();router.push("/")}}/>;
    if(enrollment.subjectCode===HOMEROOM_SUBJECT_CODE)return <HomeroomStudentHome courseId={enrollment.course.id} courseName={enrollment.course.name} schoolYear={enrollment.course.school_year} studentId={session.user.id}/>;
    return <><div className="mb-5 flex items-center gap-2 rounded-2xl border border-emerald-400/25 bg-emerald-500/10 px-5 py-3 text-sm text-emerald-200"><strong>{enrollment.course.name}</strong><span>· {enrollment.course.school_year}</span></div><div className="mb-5"><StudentCodeField studentId={session.user.id}/></div><StudentAttendancePanel courseId={enrollment.course.id} studentId={session.user.id}/></>;
  }

  if(classRequest?.status==="active")return <ThptStudentHome profile={profile} email={session.user.email} studentId={session.user.id} classId={classRequest.classId} className={classRequest.className} onSignOut={async()=>{await signOut();router.push("/")}}/>;
  if(classRequest)return <ClassRequestNotice request={classRequest} onRetry={reload}/>;
  return <StudentTrackChooser onSubmitted={reload}/>;
  })();
  const switcher=track==="cttc"&&enrollments&&enrollments.length>0?<CourseSwitcher enrollments={enrollments} currentId={enrollment?.course.id??null} onPick={pickCourse}/>:null;
  return <>{variant==="thpt_active"?null:welcome(variant)}{switcher}{body}{variant!=="thpt_active"&&profile?.role==="student"&&<LazyErrorBoundary><DailyReminderCard/></LazyErrorBoundary>}{variant!=="thpt_active"&&<ProfileEditCard/>}</>;
}

export default function AccountPage(){return <><Navbar/><main className="mx-auto min-h-screen w-full max-w-6xl px-6 pb-24 pt-28 lg:px-8"><RequireAuth><Account/></RequireAuth></main><Footer variant="app"/></>}
