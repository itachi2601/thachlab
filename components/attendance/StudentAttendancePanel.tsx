"use client";

import { useCallback, useEffect, useState } from "react";
import { CalendarCheck, ChevronDown, ChevronUp, CheckCircle2, Clock3, Wrench, Camera, Trash2, Check, Loader2, Pencil, Dices } from "lucide-react";
import { fetchMyAttendance, submitAttendanceCode } from "@/services/course-attendance";
import { TURN_MACHINE_CODES, MILL_MACHINE_CODES, selectAttendanceMachine, isPhotoDutyMachine, isPhotoDutyWorkshop, fetchAttendanceMachinePhotos, submitAttendanceMachinePhoto, createAttendanceMachinePhotoUrl, type AttendanceMachinePhoto, type MachineCheckpoint } from "@/services/attendance-machine";

const labels:Record<string,string>={present:"Có mặt",late:"Đi muộn",excused:"Vắng có phép",absent:"Vắng không phép"};
function sessionOf(row:{attendance_sessions:unknown}){const value=row.attendance_sessions as {id:number;title:string;session_date:string;starts_at:string;status:string;machine_selection_open:boolean}|{id:number;title:string;session_date:string;starts_at:string;status:string;machine_selection_open:boolean}[];return Array.isArray(value)?value[0]:value}

export default function StudentAttendancePanel({courseId,studentId}:{courseId:number;studentId:string}){const[code,setCode]=useState("");const[rows,setRows]=useState<Awaited<ReturnType<typeof fetchMyAttendance>>>([]);const[message,setMessage]=useState("");const[busy,setBusy]=useState(false);const[expanded,setExpanded]=useState(false);const load=useCallback(()=>fetchMyAttendance(courseId,studentId).then(setRows).catch(()=>undefined),[courseId,studentId]);useEffect(()=>{void load()},[load]);const attended=rows.filter(row=>row.status==="present"||row.status==="late").length;const rate=rows.length?Math.round(attended/rows.length*100):0;const visibleRows=expanded?rows:rows.slice(0,4);const latest=rows[0];const otherOpenRows=rows.filter(row=>row!==latest&&(row.status==="present"||row.status==="late")&&sessionOf(row)?.machine_selection_open);async function submit(){setBusy(true);try{const result=await submitAttendanceCode(courseId,code);setMessage(`${result.status==="late"?"Điểm danh muộn":"Điểm danh thành công"}: ${result.session_title}`);setCode("");await load()}catch(cause){setMessage(cause instanceof Error?cause.message:"Không thể điểm danh.")}finally{setBusy(false)}}return <section className="mt-5 rounded-2xl border border-cyan-400/15 bg-cyan-500/5 p-4"><div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between"><div><div className="flex items-center gap-2"><CalendarCheck size={18} className="text-cyan-300"/><strong className="text-white">Điểm danh offline</strong></div><p className="mt-1 text-xs text-slate-400">Đã tham dự {attended}/{rows.length} buổi · {rate}%</p></div><div className="flex gap-2"><input inputMode="numeric" maxLength={6} value={code} onChange={e=>setCode(e.target.value.replace(/\D/g,""))} placeholder="Mã 6 số" className="w-full min-w-0 flex-1 rounded-xl border border-white/10 bg-[#080d1d] px-3 py-2 font-mono text-sm tracking-wider text-white sm:w-32 sm:flex-none"/><button disabled={busy||code.length!==6} onClick={submit} className="shrink-0 rounded-xl bg-cyan-600 px-4 py-2 text-xs font-bold text-white disabled:opacity-40">Xác nhận</button></div></div>{message&&<p className="mt-3 rounded-lg bg-black/20 p-2 text-xs text-cyan-100">{message}</p>}
  {latest&&(latest.status==="present"||latest.status==="late")&&<MachineDutyPanel sessionId={latest.session_id} machineCode={latest.machine_code} open={Boolean(sessionOf(latest)?.machine_selection_open)} onMachineChosen={load}/>}
  {otherOpenRows.map(row=>{const session=sessionOf(row);return <div key={`open-${row.session_id}`}><p className="mt-4 text-xs font-bold text-orange-300">Giáo viên đang cho chọn máy cho buổi {session?.title??""} · {session?.session_date?new Date(`${session.session_date}T00:00:00`).toLocaleDateString("vi-VN"):""}</p><MachineDutyPanel sessionId={row.session_id} machineCode={row.machine_code} open={true} onMachineChosen={load}/></div>})}
  <div className="mt-3 grid gap-2 sm:grid-cols-2">{visibleRows.map(row=>{const session=Array.isArray(row.attendance_sessions)?row.attendance_sessions[0]:row.attendance_sessions;return <div key={row.session_id} className="flex items-center justify-between rounded-xl border border-white/5 bg-black/15 p-3"><div className="min-w-0"><strong className="block text-xs text-white">{session?.title??"Buổi học CNC"}</strong><small className="text-slate-500">{session?.session_date?new Date(`${session.session_date}T00:00:00`).toLocaleDateString("vi-VN"):""}</small>{(row.bonus_points!==0||row.note)&&<div className="mt-1 flex flex-wrap items-center gap-1.5">{row.bonus_points!==0&&<span className={`rounded-full px-1.5 py-0.5 text-[10px] font-bold ${row.bonus_points>0?"bg-emerald-500/15 text-emerald-300":"bg-red-500/15 text-red-300"}`}>{row.bonus_points>0?`+${row.bonus_points}`:row.bonus_points} điểm</span>}{row.note&&<small className="truncate text-slate-500" title={row.note}>{row.note}</small>}</div>}</div><div className="flex shrink-0 flex-col items-end gap-1"><span className={`flex items-center gap-1 text-xs font-bold ${row.status==="present"?"text-emerald-300":row.status==="late"?"text-amber-300":row.status==="excused"?"text-blue-300":"text-red-300"}`}>{row.status==="present"?<CheckCircle2 size={14}/>:<Clock3 size={14}/>} {labels[row.status]}</span>{row.machine_code&&<span className="flex items-center gap-1 rounded-full bg-orange-500/10 px-1.5 py-0.5 text-[10px] font-bold text-orange-200"><Wrench size={10}/>{row.machine_code}</span>}</div></div>})}</div>{rows.length>4&&<button type="button" onClick={()=>setExpanded(value=>!value)} className="mt-3 flex w-full items-center justify-center gap-1 rounded-lg border border-white/5 py-2 text-xs font-bold text-slate-400 hover:text-cyan-200">{expanded?<>Thu gọn<ChevronUp size={14}/></>:<>Xem tất cả {rows.length} buổi<ChevronDown size={14}/></>}</button>}</section>}

function DutyBadge(){return <span className="flex items-center gap-1 rounded-full bg-fuchsia-500/15 px-1.5 py-0.5 text-[9px] font-bold text-fuchsia-200"><Dices size={9}/>Bạn được chọn</span>}

function MachineDutyPanel({sessionId,machineCode,open,onMachineChosen}:{sessionId:number;machineCode:string|null;open:boolean;onMachineChosen:()=>void}){
  const[picked,setPicked]=useState("");
  const[busy,setBusy]=useState(false);
  const[error,setError]=useState("");
  const[editing,setEditing]=useState(false);
  const[photos,setPhotos]=useState<AttendanceMachinePhoto[]>([]);
  const[machineDuty,setMachineDuty]=useState(false);
  const[workshopDuty,setWorkshopDuty]=useState(false);
  const load=useCallback(()=>fetchAttendanceMachinePhotos(sessionId).then(setPhotos).catch(()=>undefined),[sessionId]);
  useEffect(()=>{void load()},[load]);
  useEffect(()=>{setPicked(machineCode??"")},[machineCode]);
  useEffect(()=>{if(!machineCode){setMachineDuty(false);return}void isPhotoDutyMachine(sessionId,machineCode).then(setMachineDuty).catch(()=>setMachineDuty(false))},[sessionId,machineCode]);
  useEffect(()=>{void isPhotoDutyWorkshop(sessionId).then(setWorkshopDuty).catch(()=>setWorkshopDuty(false))},[sessionId]);

  async function chooseMachine(){if(!picked||!open)return;setBusy(true);setError("");try{await selectAttendanceMachine(sessionId,picked);setEditing(false);onMachineChosen()}catch(cause){setError(cause instanceof Error?cause.message:"Không chọn được máy.")}finally{setBusy(false)}}

  if(!machineCode||editing)return <div className="mt-3 rounded-xl border border-orange-400/20 bg-orange-500/5 p-3">
    <div className="flex items-center gap-2 text-sm font-bold text-white"><Wrench size={15} className="text-orange-300"/>{machineCode?"Đổi máy đã chọn":"Chọn máy bạn đã dùng buổi này"}</div>
    {open?<div className="mt-2 flex flex-wrap gap-2">
      <select value={picked} onChange={e=>setPicked(e.target.value)} className="min-w-40 flex-1 rounded-lg border border-white/10 bg-[#080d1d] px-3 py-2 text-sm text-white">
        <option value="">Chọn máy…</option>
        <optgroup label="Máy tiện">{TURN_MACHINE_CODES.map(code=><option key={code} value={code}>{code}</option>)}</optgroup>
        <optgroup label="Máy phay">{MILL_MACHINE_CODES.map(code=><option key={code} value={code}>{code}</option>)}</optgroup>
      </select>
      <button disabled={!picked||busy||picked===machineCode}onClick={chooseMachine} className="rounded-lg bg-orange-600 px-4 py-2 text-xs font-bold text-white disabled:opacity-40">Xác nhận</button>
      {machineCode&&<button type="button" onClick={()=>{setEditing(false);setPicked(machineCode)}} className="rounded-lg border border-white/10 px-4 py-2 text-xs font-bold text-slate-300">Hủy</button>}
    </div>:<p className="mt-2 text-xs text-slate-500">Giáo viên đã khoá chọn máy cho buổi này.</p>}
    {error&&<p className="mt-2 text-xs text-red-300">{error}</p>}
  </div>;

  return <div className="mt-3 space-y-2">
    <div className="rounded-xl border border-orange-400/20 bg-orange-500/5 p-3">
      <div className="flex items-center justify-between gap-2"><div className="flex items-center gap-2 text-sm font-bold text-white"><Wrench size={15} className="text-orange-300"/>Vệ sinh máy {machineCode}{machineDuty&&<DutyBadge/>}</div>{open&&<button type="button" onClick={()=>setEditing(true)} className="flex items-center gap-1 text-xs font-bold text-orange-300 hover:text-orange-200"><Pencil size={12}/>Đổi máy</button>}</div>
      <p className="mt-0.5 text-xs text-slate-400">{machineDuty?"Hệ thống đã chọn ngẫu nhiên bạn phụ trách nộp ảnh máy cho cả nhóm.":"Hệ thống đã chọn ngẫu nhiên 1 bạn trong nhóm phụ trách nộp ảnh; bạn có thể xem trạng thái bên dưới."}</p>
      <div className="mt-2 grid gap-2 sm:grid-cols-2">
        <MachineCheckpointSlot sessionId={sessionId} machineCode={machineCode} checkpoint="start" label="Đầu ca" photos={photos} onUploaded={load} canUpload={machineDuty}/>
        <MachineCheckpointSlot sessionId={sessionId} machineCode={machineCode} checkpoint="end" label="Cuối ca" photos={photos} onUploaded={load} canUpload={machineDuty}/>
      </div>
    </div>
    <div className="rounded-xl border border-white/10 bg-white/[.02] p-3">
      <div className="flex items-center gap-2 text-sm font-bold text-white"><Camera size={15} className="text-cyan-300"/>Ảnh chung buổi học</div>
      <p className="mt-0.5 text-xs text-slate-400">Ảnh toàn xưởng: hệ thống chọn ngẫu nhiên 1 bạn trong buổi phụ trách. Ảnh thùng rác: bạn nào cũng nộp được.</p>
      <div className="mt-2 grid gap-2 sm:grid-cols-2">
        <MachineCheckpointSlot sessionId={sessionId} machineCode="XUONG" checkpoint="end" label="Ảnh toàn xưởng" icon={Camera} photos={photos} onUploaded={load} canUpload={workshopDuty} duty={workshopDuty}/>
        <MachineCheckpointSlot sessionId={sessionId} machineCode="RAC" checkpoint="end" label="Ảnh thùng rác" icon={Trash2} photos={photos} onUploaded={load}/>
      </div>
    </div>
  </div>;
}

function MachineCheckpointSlot({sessionId,machineCode,checkpoint,label,icon:Icon=Camera,photos,onUploaded,canUpload=true,duty=false}:{sessionId:number;machineCode:string;checkpoint:MachineCheckpoint;label:string;icon?:typeof Camera;photos:AttendanceMachinePhoto[];onUploaded:()=>void;canUpload?:boolean;duty?:boolean}){
  const[uploading,setUploading]=useState(false);
  const[error,setError]=useState("");
  const[previewUrl,setPreviewUrl]=useState("");
  const photo=photos.find(item=>item.machine_code===machineCode&&item.checkpoint===checkpoint);

  async function selectFile(file:File|undefined){
    if(!file)return;
    if(!/^image\//.test(file.type)){setError("Chỉ nhận file ảnh.");return}
    if(file.size>10*1024*1024){setError("Ảnh vượt quá 10 MB.");return}
    setError("");setUploading(true);
    try{await submitAttendanceMachinePhoto({sessionId,machineCode,checkpoint,file});onUploaded()}
    catch(cause){setError(cause instanceof Error?cause.message:"Không nộp được ảnh.")}
    finally{setUploading(false)}
  }
  async function viewPhoto(){if(!photo)return;try{setPreviewUrl(await createAttendanceMachinePhotoUrl(photo.storage_path))}catch{setError("Không mở được ảnh.")}}

  return <div className="rounded-lg border border-white/10 bg-[#080d1d] p-2.5">
    <div className="flex items-center justify-between gap-2">
      <span className="flex items-center gap-1.5 text-xs font-bold text-white"><Icon size={13}/>{label}{duty&&<DutyBadge/>}</span>
      {photo?<span className="flex items-center gap-1 text-[10px] font-bold text-emerald-300"><Check size={12}/>Đã nộp</span>:<span className="text-[10px] text-slate-500">Chưa nộp</span>}
    </div>
    {photo?<div className="mt-1.5 flex items-center justify-between gap-2 text-[10px] text-slate-500"><span className="truncate">{photo.profiles?.full_name??"Bạn học"} · {new Date(photo.created_at).toLocaleTimeString("vi-VN",{hour:"2-digit",minute:"2-digit"})}</span><button type="button" onClick={viewPhoto} className="shrink-0 font-bold text-cyan-300">Xem</button></div>
    :canUpload?<label className="mt-1.5 flex cursor-pointer items-center justify-center gap-1.5 rounded-md border border-dashed border-white/15 py-1.5 text-[10px] font-bold text-slate-400 hover:border-cyan-400/40 hover:text-cyan-200">
      {uploading?<Loader2 size={12} className="animate-spin"/>:<Camera size={12}/>}{uploading?"Đang nộp…":"Chụp / chọn ảnh"}
      <input type="file" accept="image/*" capture="environment" disabled={uploading} className="hidden" onChange={e=>{void selectFile(e.target.files?.[0]);e.currentTarget.value=""}}/>
    </label>
    :<p className="mt-1.5 rounded-md border border-dashed border-white/10 py-1.5 text-center text-[10px] text-slate-600">Đang chờ bạn phụ trách nộp</p>}
    {error&&<p className="mt-1 text-[10px] text-red-300">{error}</p>}
    {previewUrl&&<a href={previewUrl} target="_blank" rel="noreferrer" className="mt-1 block truncate text-[10px] font-bold text-cyan-300 underline">Mở ảnh trong tab mới</a>}
  </div>;
}
