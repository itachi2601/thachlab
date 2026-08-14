"use client";

import { useEffect,useState,type ComponentType } from "react";
import { Bot,Check,Code2,Cog,Factory,LockKeyhole,MonitorPlay,ShieldCheck,ShieldX,Wrench } from "lucide-react";
import { CNC_COMPETENCIES,cncCompetencyStates,fetchCourseCompetencyPermissions,type CompetencyId,type CompetencyPermission } from "@/services/cnc-competencies";
import type { CncLearningRecord } from "@/services/cnc-learning-records";

const icons:Record<CompetencyId,ComponentType<{size?:number}>>={
  "turn-programming":Code2,"turn-simulation":MonitorPlay,"turn-operation":Bot,"turn-tool-setup":Cog,"turn-machining":Factory,
  "mill-programming":Code2,"mill-simulation":MonitorPlay,"mill-operation":Bot,"mill-tool-setup":Cog,"mill-machining":Factory,
};

export default function StudentCompetencyCard({courseId,studentId,records}:{courseId:number;studentId:string;records:CncLearningRecord[]}){
  const[permissions,setPermissions]=useState<CompetencyPermission[]>([]);
  useEffect(()=>{void fetchCourseCompetencyPermissions(courseId,studentId).then(setPermissions).catch(()=>undefined)},[courseId,studentId]);
  const states=cncCompetencyStates(records,permissions);
  const unlocked=CNC_COMPETENCIES.filter(item=>states[item.id].approved).length;
  return <section className="mt-4 border-t border-white/10 pt-4 sm:mt-5">
    <div className="flex items-end justify-between gap-3"><div><div className="flex items-center gap-2"><Wrench size={17} className="text-cyan-300"/><strong className="text-sm text-white sm:text-base">Huy hiệu năng lực CNC</strong></div><p className="mt-1 text-[11px] text-slate-400 sm:text-xs">Vượt từng chốt để mở khóa năng lực và tiến đến gia công.</p></div><small className="whitespace-nowrap rounded-full bg-emerald-500/10 px-2.5 py-1 text-[10px] font-bold text-emerald-300">{unlocked}/10 đã mở</small></div>
    <div className="mt-4 grid gap-3">
      <BadgePath machine="turn" label="Hành trình Tiện CNC" states={states}/>
      <BadgePath machine="mill" label="Hành trình Phay CNC" states={states}/>
    </div>
  </section>;
}

function BadgePath({machine,label,states}:{machine:"turn"|"mill";label:string;states:ReturnType<typeof cncCompetencyStates>}){
  const items=CNC_COMPETENCIES.filter(item=>item.machine===machine);
  return <article className="overflow-hidden rounded-2xl border border-white/10 bg-black/20 p-3 sm:p-4">
    <div className="flex items-center justify-between"><strong className="text-xs text-white sm:text-sm">{label}</strong><span className="text-[10px] font-bold text-cyan-300">{items.filter(item=>states[item.id].approved).length}/5</span></div>
    <div className="mt-3 grid grid-cols-5 items-start gap-1 sm:gap-3">
      {items.map((item,index)=>{const state=states[item.id];const Icon=icons[item.id];const unlocked=state.approved;const waiting=state.eligible&&!unlocked;return <div key={item.id} className="flex shrink-0 snap-start items-start">
        <div title={item.permission} className="relative min-w-0 flex-1 text-center">
          <div className={`relative z-10 mx-auto grid h-11 w-11 place-items-center rounded-full p-[2px] transition min-[390px]:h-12 min-[390px]:w-12 sm:h-16 sm:w-16 ${unlocked?"bg-gradient-to-br from-amber-300 via-orange-400 to-cyan-400 shadow-[0_0_24px_rgba(34,211,238,.28)]":waiting?"bg-gradient-to-br from-amber-500/70 to-orange-500/40":"bg-white/10"}`}>
            <div className={`grid h-full w-full place-items-center rounded-full border ${unlocked?"border-white/25 bg-gradient-to-br from-[#183a4a] to-[#091627] text-amber-200":waiting?"border-amber-300/20 bg-[#172033] text-amber-300":"border-white/5 bg-[#0a1020] text-slate-600"}`}>{unlocked?<Icon size={25}/>:waiting?<ShieldCheck size={23}/>:state.revoked?<ShieldX size={22}/>:<LockKeyhole size={21}/>}</div>
            {unlocked&&<span className="absolute -bottom-0.5 -right-0.5 grid h-5 w-5 place-items-center rounded-full border-2 border-[#0e1c32] bg-emerald-400 text-[#052e25]"><Check size={11} strokeWidth={4}/></span>}
          </div>
          <strong className={`mt-1.5 block text-[8px] leading-[10px] min-[390px]:text-[9px] sm:mt-2 sm:text-[10px] sm:leading-3 ${unlocked?"text-white":waiting?"text-amber-200":"text-slate-600"}`}>{item.title.replace(/ (tiện|phay)$/i,"")}</strong>
          <small className={`mt-0.5 hidden text-[7px] font-bold min-[390px]:block sm:mt-1 sm:text-[8px] ${unlocked?"text-emerald-300":waiting?"text-amber-300":"text-slate-700"}`}>{unlocked?"ĐÃ MỞ":waiting?"CHỜ DUYỆT":"ĐANG KHÓA"}</small>
          {index<items.length-1&&<div className={`absolute left-[calc(50%+22px)] right-[calc(-50%+22px)] top-[21px] h-0.5 min-[390px]:left-[calc(50%+24px)] min-[390px]:right-[calc(-50%+24px)] min-[390px]:top-[23px] sm:left-[calc(50%+32px)] sm:right-[calc(-50%+32px)] sm:top-[31px] ${unlocked?"bg-gradient-to-r from-cyan-400 to-emerald-400":"bg-white/10"}`}/>}
        </div>
      </div>})}
    </div>
  </article>;
}
