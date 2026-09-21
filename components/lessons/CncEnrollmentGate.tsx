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
  if(!session)return <Shell><LogIn className="cnc-gate-icon" size={36}/><h1>Đăng nhập để học CNC</h1><p>Đăng nhập rồi nhập mã khóa do giáo viên cung cấp.</p><Link href="/dang-nhap" className="lesson-btn">Đăng nhập</Link></Shell>;
  if(profile?.role==="admin")return <CncCourseWorkspace embedded initialLessonId={lessonId}/>;
  if(!loaded)return <Shell>Đang tải thông tin khóa…</Shell>;
  if(access?.status==="active")return <><div className="cnc-enrolled-note cnc-enrolled-note--page"><CheckCircle2 size={18}/><strong>{access.course.name}</strong><span>· {access.course.school_year}</span></div><CncCourseWorkspace embedded courseId={access.course.id} initialLessonId={lessonId}/></>;
  if(access?.status==="pending")return <Shell><Clock3 className="cnc-gate-icon is-warn" size={38}/><h1>Đang chờ giáo viên duyệt</h1><p>Yêu cầu vào <strong>{access.course.name}</strong> đã được gửi.</p><button type="button" onClick={()=>void reload()} className="lesson-btn-ghost">Kiểm tra lại</button></Shell>;
  if(access?.status==="suspended")return <Shell><ShieldCheck className="cnc-gate-icon is-bad" size={38}/><h1>Quyền truy cập đang tạm khóa</h1><p>Hãy liên hệ giáo viên phụ trách khóa học.</p></Shell>;
  return <Shell><KeyRound className="cnc-gate-icon" size={38}/><h1>Tham gia khóa Gia công CNC</h1><p>Nhập mã khóa để gửi yêu cầu đến giáo viên.</p><form onSubmit={async(e)=>{e.preventDefault();if(!code.trim())return;setBusy(true);setMessage("");try{await requestEnrollment(code);await reload();}catch(err){setMessage(err instanceof Error?err.message:"Mã khóa không hợp lệ.");}finally{setBusy(false);}}}><input value={code} onChange={(e)=>setCode(e.target.value.toUpperCase())} placeholder="CNC-A1B2C3" className="cnc-gate-input"/><button disabled={busy} className="lesson-btn">{busy?"Đang gửi…":"Gửi yêu cầu"}</button></form>{message&&<p className="cnc-gate-msg">{message}</p>}</Shell>;
}
function Shell({children}:{children:React.ReactNode}){return <section className="lesson-shell lesson-shell--cttc cnc-shell cnc-gate-shell"><div className="lesson-main lesson-main--single"><div className="lesson-block cnc-gate-card">{children}</div></div></section>}
