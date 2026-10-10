"use client";

import { useEffect,useState,type ComponentType } from "react";
import Link from "next/link";
import { Bot,Check,Code2,Cog,Factory,LockKeyhole,MonitorPlay,ShieldCheck,ShieldX,Wrench } from "lucide-react";
import { CNC_COMPETENCIES,cncCompetencyStates,fetchCourseCompetencyPermissions,type CompetencyId,type CompetencyPermission } from "@/services/cnc-competencies";
import type { CncLearningRecord } from "@/services/cnc-learning-records";

const icons:Record<CompetencyId,ComponentType<{size?:number}>>={
  "turn-programming":Code2,"turn-simulation":MonitorPlay,"turn-operation":Bot,"turn-tool-setup":Cog,"turn-machining":Factory,
  "mill-programming":Code2,"mill-simulation":MonitorPlay,"mill-operation":Bot,"mill-tool-setup":Cog,"mill-machining":Factory,
};

export default function StudentCompetencyCard({courseId,studentId,records,demo=false}:{courseId:number;studentId:string;records:CncLearningRecord[];demo?:boolean}){
  const[permissions,setPermissions]=useState<CompetencyPermission[]>([]);
  useEffect(()=>{void fetchCourseCompetencyPermissions(courseId,studentId).then(setPermissions).catch(()=>undefined)},[courseId,studentId]);
  const effectivePermissions=(demo||studentId==="demo-preview")?[...permissions,{course_id:courseId,student_id:studentId,competency_id:"turn-operation" as const,status:"approved" as const,note:"",approved_at:new Date().toISOString(),updated_at:new Date().toISOString(),approved_by:null},{course_id:courseId,student_id:studentId,competency_id:"turn-tool-setup" as const,status:"approved" as const,note:"",approved_at:new Date().toISOString(),updated_at:new Date().toISOString(),approved_by:null}]:permissions;
  const states=cncCompetencyStates(records,effectivePermissions);
  const unlocked=CNC_COMPETENCIES.filter(item=>states[item.id].approved).length;
  return <section className="student-competencies mt-4 border-t border-line pt-4 sm:mt-5">
    <div className="flex items-end justify-between gap-3"><div><div className="flex items-center gap-2"><Wrench size={17} className="text-primary"/><strong className="text-sm text-ink sm:text-base">Huy hiệu năng lực CNC</strong></div><p className="mt-1 text-[12px] text-muted sm:text-xs">Vượt từng chốt để mở khóa năng lực và tiến đến gia công.</p></div><small className="whitespace-nowrap rounded-full bg-emerald-500/10 px-2.5 py-1 text-[12px] font-bold text-emerald-300">{unlocked}/10 đã mở</small></div>
    <div className="mt-4 grid gap-3">
      <BadgePath machine="turn" label="Hành trình Tiện CNC" states={states}/>
      <BadgePath machine="mill" label="Hành trình Phay CNC" states={states}/>
    </div>
  </section>;
}

function BadgePath({machine,label,states}:{machine:"turn"|"mill";label:string;states:ReturnType<typeof cncCompetencyStates>}){
  const items=CNC_COMPETENCIES.filter(item=>item.machine===machine);
  return <article className="competency-path overflow-hidden rounded-2xl border border-line bg-surface-2 p-3 sm:p-4">
    <div className="flex items-center justify-between"><strong className="text-xs text-ink sm:text-sm">{label}</strong><span className="text-[12px] font-bold text-primary">{items.filter(item=>states[item.id].approved).length}/5</span></div>
    <div className="mt-3 grid grid-cols-5 items-start gap-1 sm:gap-3">
      {items.map((item,index)=>{const state=states[item.id];const Icon=icons[item.id];const unlocked=state.approved;const waiting=state.eligible&&!unlocked;return <div key={item.id} className="flex shrink-0 snap-start items-start">
        <Link href={`/lop-hoc/cnc/?bai=${item.lessonId}`} title={`${item.permission} — bấm để vào học`} className="group relative block min-w-0 flex-1 text-center">
          <div className={`relative z-10 mx-auto grid h-11 w-11 place-items-center rounded-full p-[2px] transition group-hover:scale-105 min-[390px]:h-12 min-[390px]:w-12 sm:h-16 sm:w-16 ${unlocked?"bg-primary":waiting?"bg-warn/60":"bg-surface-2"}`}>
            <div className={`grid h-full w-full place-items-center rounded-full border ${unlocked?"border-primary bg-primary-soft text-primary":waiting?"border-warn/30 bg-surface-2 text-warn":"border-line bg-surface-2 text-muted"}`}>{unlocked?<Icon size={25}/>:waiting?<ShieldCheck size={23}/>:state.revoked?<ShieldX size={22}/>:<LockKeyhole size={21}/>}</div>
            {unlocked&&<span className="absolute -bottom-0.5 -right-0.5 grid h-5 w-5 place-items-center rounded-full border-2 border-panel bg-emerald-400 text-[#052e25]"><Check size={11} strokeWidth={4}/></span>}
          </div>
          <strong className={`mt-1.5 block text-[12px] leading-[10px] underline-offset-2 group-hover:underline min-[390px]:text-[12px] sm:mt-2 sm:text-[12px] sm:leading-3 ${unlocked?"text-ink":waiting?"text-warn":"text-muted"}`}>{item.title.replace(/ (tiện|phay)$/i,"")}</strong>
          <small className={`mt-0.5 hidden text-[12px] font-bold min-[390px]:block sm:mt-1 sm:text-[12px] ${unlocked?"text-ok":waiting?"text-warn":"text-muted"}`}>{unlocked?"ĐÃ MỞ":waiting?"CHỜ DUYỆT":"ĐANG KHÓA"}</small>
          {index<items.length-1&&<div className={`absolute left-[calc(50%+22px)] right-[calc(-50%+22px)] top-[21px] h-0.5 min-[390px]:left-[calc(50%+24px)] min-[390px]:right-[calc(-50%+24px)] min-[390px]:top-[23px] sm:left-[calc(50%+32px)] sm:right-[calc(-50%+32px)] sm:top-[31px] ${unlocked?"bg-primary":"bg-surface-2"}`}/>}
        </Link>
      </div>})}
    </div>
  </article>;
}
