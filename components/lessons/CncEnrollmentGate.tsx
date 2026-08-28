"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { CheckCircle2, Clock3, KeyRound, LogIn, ShieldCheck } from "lucide-react";
import { useAuth } from "@/components/auth/AuthProvider";
import CncCourseWorkspace from "@/components/lessons/CncCourseWorkspace";
import { fetchMyActiveCncCourse, requestEnrollment } from "@/services/course-enrollments";

type Access = Awaited<ReturnType<typeof fetchMyActiveCncCourse>>;
export default function CncEnrollmentGate({ lessonId }: { lessonId?: string }){
  const {session,profile,loading:authLoading}=useAuth(); const [access,setAccess]=useState<Access>(null); const [loaded,setLoaded]=useState(false); const [code,setCode]=useState(""); const [busy,setBusy]=useState(false); const [message,setMessage]=useState("");
  const reload=useCallback(async()=>{if(!session)return;try{setAccess(await fetchMyActiveCncCourse(session.user.id));}catch(e){setMessage(e instanceof Error?e.message:"Không kiểm tra được khóa học.");}finally{setLoaded(true);}},[session]);
  useEffect(()=>{const timer=setTimeout(()=>void reload(),0);return()=>clearTimeout(timer);},[reload]);
  if(authLoading)return <Shell>Đang kiểm tra khóa học…</Shell>;
  if(!session)return <Shell><LogIn className="mx-auto text-blue-300" size={36}/><h1 className="mt-4 text-2xl font-bold text-white">Đăng nhập để học CNC</h1><p className="mt-2 text-sm text-slate-400">Đăng nhập rồi nhập mã khóa do giáo viên cung cấp.</p><Link href="/dang-nhap" className="mt-5 inline-flex rounded-full bg-blue-600 px-6 py-2.5 text-sm font-bold text-white">Đăng nhập</Link></Shell>;
  if(profile?.role==="admin")return <CncCourseWorkspace embedded initialLessonId={lessonId}/>;
  if(!loaded)return <Shell>Đang tải thông tin khóa…</Shell>;
  if(access?.status==="active")return <><div className="mx-5 mt-5 flex items-center gap-2 rounded-2xl border border-emerald-400/25 bg-emerald-500/10 px-5 py-3 text-sm text-emerald-200"><CheckCircle2 size={18}/><strong>{access.course.name}</strong><span>· {access.course.school_year}</span></div><CncCourseWorkspace embedded courseId={access.course.id} initialLessonId={lessonId}/></>;
  if(access?.status==="pending")return <Shell><Clock3 className="mx-auto text-amber-300" size={38}/><h1 className="mt-4 text-2xl font-bold text-white">Đang chờ giáo viên duyệt</h1><p className="mt-2 text-sm text-slate-400">Yêu cầu vào <strong className="text-white">{access.course.name}</strong> đã được gửi.</p><button onClick={()=>void reload()} className="mt-5 rounded-full border border-white/15 px-5 py-2 text-sm text-slate-200">Kiểm tra lại</button></Shell>;
  if(access?.status==="suspended")return <Shell><ShieldCheck className="mx-auto text-red-300" size={38}/><h1 className="mt-4 text-2xl font-bold text-white">Quyền truy cập đang tạm khóa</h1><p className="mt-2 text-sm text-slate-400">Hãy liên hệ giáo viên phụ trách khóa học.</p></Shell>;
  return <Shell><KeyRound className="mx-auto text-blue-300" size={38}/><h1 className="mt-4 text-2xl font-bold text-white">Tham gia khóa Gia công CNC</h1><p className="mt-2 text-sm text-slate-400">Nhập mã khóa để gửi yêu cầu đến giáo viên.</p><form className="mx-auto mt-6 flex max-w-md flex-col gap-3 sm:flex-row" onSubmit={async(e)=>{e.preventDefault();if(!code.trim())return;setBusy(true);setMessage("");try{await requestEnrollment(code);await reload();}catch(err){setMessage(err instanceof Error?err.message:"Mã khóa không hợp lệ.");}finally{setBusy(false);}}}><input value={code} onChange={(e)=>setCode(e.target.value.toUpperCase())} placeholder="CNC-A1B2C3" className="min-w-0 flex-1 rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-center font-mono uppercase text-white"/><button disabled={busy} className="rounded-xl bg-blue-600 px-5 py-3 text-sm font-bold text-white">{busy?"Đang gửi…":"Gửi yêu cầu"}</button></form>{message&&<p className="mt-4 text-sm text-amber-200">{message}</p>}</Shell>;
}
function Shell({children}:{children:React.ReactNode}){return <section className="grid min-h-[70vh] place-items-center bg-[#071426] px-5 py-16"><div className="w-full max-w-2xl rounded-3xl border border-white/10 bg-[#0B1020] p-8 text-center shadow-2xl">{children}</div></section>}
