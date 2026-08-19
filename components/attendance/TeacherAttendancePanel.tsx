"use client";

import { useCallback, useEffect, useState } from "react";
import { AlertOctagon, AlertTriangle, Camera, Check, CalendarCheck, CheckCheck, Clock3, Copy, Grid3x3, LockKeyhole, NotebookPen, Plus, RefreshCw, Search, ShieldCheck, Trash2, Unlock, UserCheck, Users, Wrench, XCircle } from "lucide-react";
import { closeAttendanceSession, createAttendanceSession, fetchAttendanceRecords, fetchAttendanceSessions, setAttendanceRecord, setAttendanceRecordBonus, setAttendanceRecordMachine, setAttendanceRecordNote, setMachineSelectionOpen, updateAttendanceSessionNote, type AttendanceRecord, type AttendanceSession, type AttendanceStatus } from "@/services/course-attendance";
import { createAttendanceMachinePhotoUrl, EQUIPMENT_STATUS_META, fetchAttendanceMachinePhotos, fetchAttendanceMachineScores, fetchMachines, fiveSScore, FIVE_S_CRITERIA, groupMachinesByType, updateAttendanceMachineScore, type AttendanceMachinePhoto, type AttendanceMachineScore, type EquipmentStatus, type Machine, type MachineCheckpoint } from "@/services/attendance-machine";
import { createEquipmentBreakdownPhotoUrl, fetchEquipmentBreakdownReports, reportEquipmentBreakdown, resolveEquipmentBreakdown, type EquipmentBreakdownReport } from "@/services/equipment-breakdown";

type Student={id:string;name:string;className:string};
const statusMeta:Record<AttendanceStatus,{label:string;short:string;code:string;style:string;active:string;icon:typeof UserCheck}>={
  present:{label:"Có mặt",short:"Có mặt",code:"C",style:"text-emerald-300",active:"border-emerald-400/50 bg-emerald-500/15 text-emerald-200",icon:UserCheck},
  late:{label:"Đi trễ",short:"Muộn",code:"T",style:"text-amber-300",active:"border-amber-400/50 bg-amber-500/15 text-amber-200",icon:Clock3},
  excused:{label:"Vắng có phép",short:"Có phép",code:"VP",style:"text-blue-300",active:"border-blue-400/50 bg-blue-500/15 text-blue-200",icon:ShieldCheck},
  absent:{label:"Vắng không phép",short:"Vắng",code:"V",style:"text-red-300",active:"border-red-400/50 bg-red-500/15 text-red-200",icon:XCircle},
};

export default function TeacherAttendancePanel({courseId,students}:{courseId:number;students:Student[]}){
  const[view,setView]=useState<"live"|"machines"|"summary">("live");
  const[sessions,setSessions]=useState<AttendanceSession[]>([]);const[selectedId,setSelectedId]=useState<number|null>(null);const[records,setRecords]=useState<AttendanceRecord[]>([]);const[allRecords,setAllRecords]=useState<AttendanceRecord[]>([]);const[creating,setCreating]=useState(false);const[busy,setBusy]=useState(false);const[error,setError]=useState("");const[search,setSearch]=useState("");const[copied,setCopied]=useState(false);const[noteDraft,setNoteDraft]=useState("");const[bonusDrafts,setBonusDrafts]=useState<Record<string,string>>({});const[recordNoteDrafts,setRecordNoteDrafts]=useState<Record<string,string>>({});const[machinePhotos,setMachinePhotos]=useState<AttendanceMachinePhoto[]>([]);const[machineScores,setMachineScores]=useState<AttendanceMachineScore[]>([]);const[breakdowns,setBreakdowns]=useState<EquipmentBreakdownReport[]>([]);const[machines,setMachines]=useState<Machine[]>([]);
  const loadBreakdowns=useCallback(()=>void fetchEquipmentBreakdownReports(courseId).then(setBreakdowns).catch(()=>undefined),[courseId]);
  useEffect(()=>{loadBreakdowns()},[loadBreakdowns]);
  useEffect(()=>{void fetchMachines().then(setMachines).catch(()=>undefined)},[]);
  const now=new Date();const[title,setTitle]=useState("Thực hành CNC");const[startsAt,setStartsAt]=useState(new Date(now.getTime()-now.getTimezoneOffset()*60000).toISOString().slice(0,16));
  const selected=sessions.find(item=>item.id===selectedId)??null;
  const loadSessions=useCallback(()=>fetchAttendanceSessions(courseId).then(rows=>{setSessions(rows);setSelectedId(current=>rows.some(item=>item.id===current)?current:rows[0]?.id??null)}).catch(cause=>setError(cause instanceof Error?cause.message:"Không tải được phiên điểm danh.")),[courseId]);
  useEffect(()=>{void loadSessions()},[loadSessions]);
  useEffect(()=>{let cancelled=false;Promise.all(sessions.map(session=>fetchAttendanceRecords(session.id).catch(()=>[]))).then(rows=>{if(!cancelled)setAllRecords(rows.flat())});return()=>{cancelled=true}},[sessions]);
  useEffect(()=>{if(!selectedId)return;void fetchAttendanceRecords(selectedId).then(setRecords).catch(cause=>setError(cause instanceof Error?cause.message:"Không tải được kết quả điểm danh."))},[selectedId]);
  const loadMachineData=useCallback(()=>{if(!selectedId)return;void fetchAttendanceMachinePhotos(selectedId).then(setMachinePhotos).catch(()=>undefined);void fetchAttendanceMachineScores(selectedId).then(setMachineScores).catch(()=>undefined)},[selectedId]);
  useEffect(()=>{loadMachineData()},[loadMachineData]);
  useEffect(()=>{setNoteDraft(selected?.note??"")},[selected?.id]);
  useEffect(()=>{setBonusDrafts({});setRecordNoteDrafts({})},[selectedId]);
  async function createSession(){setBusy(true);setError("");try{const item=await createAttendanceSession({courseId,title,startsAt,durationMinutes:60,lateMinutes:15});setSessions(current=>[item,...current]);setSelectedId(item.id);setCreating(false)}catch(cause){setError(cause instanceof Error?cause.message:"Không tạo được phiên điểm danh.")}finally{setBusy(false)}}
  async function mark(studentId:string,status:AttendanceStatus){if(!selected)return;setBusy(true);try{await setAttendanceRecord(selected.id,studentId,status);setRecords(await fetchAttendanceRecords(selected.id))}catch(cause){setError(cause instanceof Error?cause.message:"Không cập nhật được điểm danh.")}finally{setBusy(false)}}
  async function markRemainingPresent(){if(!selected)return;const unmarked=students.filter(student=>!records.some(record=>record.student_id===student.id));if(!unmarked.length)return;setBusy(true);try{await Promise.all(unmarked.map(student=>setAttendanceRecord(selected.id,student.id,"present")));setRecords(await fetchAttendanceRecords(selected.id))}catch(cause){setError(cause instanceof Error?cause.message:"Không cập nhật được điểm danh.")}finally{setBusy(false)}}
  async function saveNote(){if(!selected||noteDraft===selected.note)return;try{await updateAttendanceSessionNote(selected.id,noteDraft);setSessions(current=>current.map(item=>item.id===selected.id?{...item,note:noteDraft}:item))}catch(cause){setError(cause instanceof Error?cause.message:"Không lưu được ghi chú.")}}
  async function saveStudentBonus(studentId:string){if(!selected)return;const raw=bonusDrafts[studentId];if(raw===undefined)return;const value=Math.trunc(Number(raw))||0;try{await setAttendanceRecordBonus(selected.id,studentId,value);setRecords(current=>current.map(item=>item.student_id===studentId?{...item,bonus_points:value}:item))}catch(cause){setError(cause instanceof Error?cause.message:"Không lưu được điểm cộng/trừ.")}}
  async function saveStudentNote(studentId:string){if(!selected)return;const value=recordNoteDrafts[studentId];if(value===undefined)return;try{await setAttendanceRecordNote(selected.id,studentId,value);setRecords(current=>current.map(item=>item.student_id===studentId?{...item,note:value}:item))}catch(cause){setError(cause instanceof Error?cause.message:"Không lưu được ghi chú.")}}
  async function assignMachine(studentId:string,machineCode:string){if(!selected)return;setBusy(true);try{await setAttendanceRecordMachine(selected.id,studentId,machineCode||null);setRecords(current=>current.map(item=>item.student_id===studentId?{...item,machine_code:machineCode||null}:item))}catch(cause){setError(cause instanceof Error?cause.message:"Không gán được máy.")}finally{setBusy(false)}}
  function copyCode(){if(!selected)return;navigator.clipboard.writeText(selected.code);setCopied(true);setTimeout(()=>setCopied(false),1500)}
  async function toggleMachineSelection(){if(!selected)return;setBusy(true);try{await setMachineSelectionOpen(selected.id,!selected.machine_selection_open);await loadSessions()}catch(cause){setError(cause instanceof Error?cause.message:"Không đổi được trạng thái chọn máy.")}finally{setBusy(false)}}
  const presentCount=records.filter(item=>item.status==="present"||item.status==="late").length;
  const unmarkedCount=selected?students.filter(student=>!records.some(record=>record.student_id===student.id)).length:0;
  const visibleStudents=students.filter(student=>`${student.name} ${student.className}`.toLocaleLowerCase("vi-VN").includes(search.trim().toLocaleLowerCase("vi-VN")));
  const machineCodes=[...new Set(records.map(item=>item.machine_code).filter((code):code is string=>Boolean(code)))].sort();
  const machineGroups=machineCodes.map(code=>({code,members:students.filter(student=>records.find(record=>record.student_id===student.id)?.machine_code===code)}));
  const machinesFullyChecked=machineGroups.filter(group=>machinePhotos.some(p=>p.machine_code===group.code&&p.checkpoint==="start")&&machinePhotos.some(p=>p.machine_code===group.code&&p.checkpoint==="end")).length;
  const avgFiveS=machineGroups.length?Math.round(machineGroups.reduce((sum,group)=>sum+fiveSScore(machineScores.find(s=>s.machine_code===group.code)),0)/machineGroups.length):0;
  const machineIssues=machineGroups.filter(group=>{const status=machineScores.find(s=>s.machine_code===group.code)?.equipment_status;return status==="maintenance"||status==="broken"}).length;
  const openBreakdowns=breakdowns.filter(r=>r.status==="open").length;

  return <div className="space-y-5">
    <div className="flex flex-wrap gap-2">
      <button onClick={()=>setView("live")} className={`inline-flex items-center gap-2 rounded-xl border px-4 py-2 text-sm font-bold ${view==="live"?"border-cyan-400/40 bg-cyan-500/10 text-cyan-200":"border-white/10 text-slate-400"}`}><CalendarCheck size={16}/>Điểm danh trực tiếp</button>
      <button onClick={()=>setView("machines")} className={`inline-flex items-center gap-2 rounded-xl border px-4 py-2 text-sm font-bold ${view==="machines"?"border-orange-400/40 bg-orange-500/10 text-orange-200":"border-white/10 text-slate-400"}`}><Wrench size={16}/>Tình trạng máy</button>
      <button onClick={()=>setView("summary")} className={`inline-flex items-center gap-2 rounded-xl border px-4 py-2 text-sm font-bold ${view==="summary"?"border-cyan-400/40 bg-cyan-500/10 text-cyan-200":"border-white/10 text-slate-400"}`}><Grid3x3 size={16}/>Tổng hợp điểm danh</button>
    </div>

    {view==="live"&&<section className="rounded-2xl border border-white/10 bg-[#0B1020] p-5 sm:p-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div><p className="text-xs font-bold uppercase tracking-[.16em] text-cyan-300">Tham dự offline</p><h3 className="mt-1 font-display text-2xl font-bold text-white">Điểm danh khóa học</h3><p className="mt-1 text-sm text-slate-500">Mở phiên theo buổi học để sinh viên nhập mã điểm danh; mã 6 số hiệu lực 60 phút, sau 15 phút hệ thống ghi nhận đi muộn.</p></div>
        <button onClick={()=>setCreating(value=>!value)} className="inline-flex items-center gap-2 rounded-xl bg-orange-500 px-4 py-2.5 text-sm font-bold text-white"><Plus size={17}/>Mở phiên điểm danh</button>
      </div>
      {creating&&<div className="mt-5 grid gap-3 rounded-2xl border border-orange-400/20 bg-orange-500/5 p-4 sm:grid-cols-[1fr_1fr_auto]"><input value={title} onChange={e=>setTitle(e.target.value)} placeholder="Nội dung buổi học" className="rounded-xl border border-white/10 bg-[#080d1d] px-4 py-3 text-sm text-white"/><input type="datetime-local" value={startsAt} onChange={e=>setStartsAt(e.target.value)} className="rounded-xl border border-white/10 bg-[#080d1d] px-4 py-3 text-sm text-white"/><button disabled={busy||!title.trim()} onClick={createSession} className="rounded-xl bg-blue-600 px-5 py-3 text-sm font-bold text-white disabled:opacity-40">Mở phiên</button></div>}
      {error&&<p className="mt-3 rounded-xl bg-red-500/10 p-3 text-sm text-red-200">{error}</p>}

      <div className="mt-5 flex flex-wrap items-center gap-3">
        <select aria-label="Chọn buổi điểm danh" value={selectedId??""} onChange={e=>setSelectedId(Number(e.target.value))} className="min-w-64 flex-1 rounded-xl border border-white/10 bg-[#080d1d] px-4 py-2.5 text-sm text-white sm:flex-none">
          <option value="" disabled>Chọn buổi điểm danh…</option>
          {sessions.map(item=><option key={item.id} value={item.id}>{item.title} · {new Date(item.starts_at).toLocaleString("vi-VN")} · {item.status==="open"?"Đang mở":"Đã khóa"}</option>)}
        </select>
        <button aria-label="Làm mới" onClick={()=>void loadSessions()} className="text-slate-400"><RefreshCw size={16}/></button>
        {!sessions.length&&<p className="text-sm text-slate-500">Chưa có buổi điểm danh nào, hãy mở phiên đầu tiên.</p>}
      </div>

      {selected?<>
        <div className="mt-4 grid gap-4 lg:grid-cols-[1.3fr_1fr]">
          <div className="rounded-2xl border border-cyan-400/20 bg-gradient-to-br from-cyan-500/10 to-blue-500/5 p-5">
            <div className="flex flex-wrap items-center justify-between gap-4">
              <div><small className="font-bold uppercase tracking-wider text-cyan-300">Mã điểm danh</small><div className="mt-1 flex items-center gap-3"><strong className="font-mono text-4xl tracking-[.18em] text-white">{selected.code}</strong><button onClick={copyCode} className="flex items-center gap-1 text-cyan-300">{copied?<><CheckCheck size={18}/><small className="text-xs font-bold">Đã chép</small></>:<Copy size={18}/>}</button></div></div>
              <div className="text-right text-sm text-slate-400"><p className="flex items-center justify-end gap-2"><Users size={15}/>{presentCount}/{students.length} đã tham dự</p><p className="mt-1 flex items-center justify-end gap-2"><Clock3 size={15}/>Đóng {new Date(selected.closes_at).toLocaleTimeString("vi-VN",{hour:"2-digit",minute:"2-digit"})}</p></div>
            </div>
            <div className="mt-4 flex flex-wrap items-center gap-2">
              {selected.status==="open"&&<button onClick={async()=>{await closeAttendanceSession(selected.id);await loadSessions()}} className="inline-flex items-center gap-2 rounded-full border border-white/10 px-4 py-2 text-xs font-bold text-slate-300"><LockKeyhole size={14}/>Khóa phiên</button>}
              {selected.status==="open"&&unmarkedCount>0&&<button disabled={busy} onClick={()=>void markRemainingPresent()} className="inline-flex items-center gap-2 rounded-full border border-emerald-400/30 bg-emerald-500/10 px-4 py-2 text-xs font-bold text-emerald-200 disabled:opacity-40"><Check size={14}/>Đánh dấu {unmarkedCount} SV còn lại: Có mặt</button>}
              <button disabled={busy} onClick={()=>void toggleMachineSelection()} title="Bật/tắt việc sinh viên tự chọn/đổi máy cho buổi này, độc lập với khoá điểm danh" className={`inline-flex items-center gap-2 rounded-full border px-4 py-2 text-xs font-bold disabled:opacity-40 ${selected.machine_selection_open?"border-emerald-400/30 bg-emerald-500/10 text-emerald-200":"border-white/10 text-slate-300"}`}>{selected.machine_selection_open?<Unlock size={14}/>:<LockKeyhole size={14}/>}{selected.machine_selection_open?"Đang cho chọn máy":"Đã khoá chọn máy"}</button>
            </div>
          </div>
          <div className="rounded-2xl border border-white/10 bg-white/[.02] p-5">
            <div className="flex items-center gap-2 text-sm font-bold text-white"><NotebookPen size={16} className="text-violet-300"/>Ghi chú buổi học</div>
            <textarea value={noteDraft} onChange={e=>setNoteDraft(e.target.value)} onBlur={saveNote} rows={5} placeholder="Ghi chú nhanh về buổi học: sự cố máy, nội dung đặc biệt, sinh viên xin nghỉ đột xuất…" className="mt-3 w-full resize-none rounded-xl border border-white/10 bg-[#080d1d] px-3 py-2.5 text-sm text-white placeholder:text-slate-500 focus:outline-none"/>
          </div>
        </div>

        <div className="mt-4 flex items-center gap-2 rounded-xl border border-white/10 bg-[#080d1d] px-3 py-2"><Search size={15} className="text-slate-500"/><input value={search} onChange={e=>setSearch(e.target.value)} placeholder="Tìm sinh viên theo tên hoặc lớp…" className="w-full bg-transparent text-sm text-white placeholder:text-slate-500 focus:outline-none"/></div>
        <div className="mt-3 overflow-x-auto"><table className="w-full min-w-[1050px] text-left text-sm"><thead><tr className="border-b border-white/10 text-xs uppercase text-slate-500"><th className="p-3">Sinh viên</th><th className="p-3">Thời gian</th><th className="p-3">Điểm danh</th><th className="p-3">Máy</th><th className="p-3">Điểm cộng/trừ</th><th className="p-3">Ghi chú</th></tr></thead><tbody>{visibleStudents.map(student=>{const record=records.find(item=>item.student_id===student.id);const bonusValue=bonusDrafts[student.id]??String(record?.bonus_points??0);const noteValue=recordNoteDrafts[student.id]??record?.note??"";const bonusNum=Number(bonusValue)||0;return <tr key={student.id} className="border-b border-white/5"><td className="p-3"><strong className="text-white">{student.name}</strong><small className="block text-slate-500">{student.className}</small></td><td className="p-3 text-slate-400">{record?.checked_in_at?new Date(record.checked_in_at).toLocaleTimeString("vi-VN",{hour:"2-digit",minute:"2-digit"}):"—"}</td><td className="p-3"><select disabled={busy} value={record?.status??""} onChange={e=>void mark(student.id,e.target.value as AttendanceStatus)} className={`rounded-lg border bg-[#080d1d] px-2.5 py-1.5 text-xs font-bold disabled:opacity-40 ${record?statusMeta[record.status].style:"text-slate-500"} border-white/10`}><option value="" disabled>Chọn</option>{Object.entries(statusMeta).map(([value,meta])=><option key={value} value={value}>{meta.label}</option>)}</select></td><td className="p-3"><select disabled={!record||busy} title={!record?"Điểm danh trước khi gán máy":""} value={record?.machine_code??""} onChange={e=>void assignMachine(student.id,e.target.value)} className="rounded-lg border border-white/10 bg-[#080d1d] px-2.5 py-1.5 text-xs font-bold text-slate-300 disabled:cursor-not-allowed disabled:opacity-30"><option value="">— Chưa chọn —</option>{groupMachinesByType(machines).map(group=><optgroup key={group.type} label={group.label}>{group.machines.map(m=><option key={m.code} value={m.code} title={m.label}>{m.code}</option>)}</optgroup>)}</select></td><td className="p-3"><input type="number" step={1} disabled={!record} title={!record?"Điểm danh trước khi cộng/trừ điểm":""} value={bonusValue} onChange={e=>setBonusDrafts(current=>({...current,[student.id]:e.target.value}))} onBlur={()=>void saveStudentBonus(student.id)} className={`w-20 rounded-lg border bg-[#080d1d] px-2 py-1.5 text-xs font-bold disabled:cursor-not-allowed disabled:opacity-30 ${bonusNum>0?"border-emerald-400/30 text-emerald-300":bonusNum<0?"border-red-400/30 text-red-300":"border-white/10 text-slate-300"}`}/></td><td className="p-3"><input type="text" disabled={!record} title={!record?"Điểm danh trước khi ghi chú":""} value={noteValue} onChange={e=>setRecordNoteDrafts(current=>({...current,[student.id]:e.target.value}))} onBlur={()=>void saveStudentNote(student.id)} placeholder={record?"Ghi chú…":"—"} className="w-40 rounded-lg border border-white/10 bg-[#080d1d] px-2 py-1.5 text-xs text-white placeholder:text-slate-600 disabled:cursor-not-allowed disabled:opacity-30"/></td></tr>})}{!visibleStudents.length&&<tr><td colSpan={6} className="p-6 text-center text-sm text-slate-500">Không tìm thấy sinh viên phù hợp.</td></tr>}</tbody></table></div>
      </>:<div className="mt-5 grid min-h-72 place-items-center rounded-2xl border border-dashed border-white/10 text-sm text-slate-500"><CalendarCheck size={30}/><span className="mt-2">Chọn hoặc mở một phiên điểm danh.</span></div>}
    </section>}

    {view==="machines"&&<section className="rounded-2xl border border-white/10 bg-[#0B1020] p-5 sm:p-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div><p className="text-xs font-bold uppercase tracking-[.16em] text-orange-300">Thiết bị &amp; 5S</p><h3 className="mt-1 font-display text-2xl font-bold text-white">Tình trạng máy</h3><p className="mt-1 text-sm text-slate-500">Sinh viên tự chọn máy khi điểm danh (hoặc giáo viên gán ở tab Điểm danh trực tiếp); mỗi máy chỉ cần 1 bạn nộp ảnh đầu ca/cuối ca cho cả nhóm.</p></div>
      </div>
      <div className="mt-5 flex flex-wrap items-center gap-3">
        <select aria-label="Chọn buổi điểm danh" value={selectedId??""} onChange={e=>setSelectedId(Number(e.target.value))} className="min-w-64 flex-1 rounded-xl border border-white/10 bg-[#080d1d] px-4 py-2.5 text-sm text-white sm:flex-none">
          <option value="" disabled>Chọn buổi điểm danh…</option>
          {sessions.map(item=><option key={item.id} value={item.id}>{item.title} · {new Date(item.starts_at).toLocaleString("vi-VN")} · {item.status==="open"?"Đang mở":"Đã khóa"}</option>)}
        </select>
        <button aria-label="Làm mới" onClick={loadMachineData} className="text-slate-400"><RefreshCw size={16}/></button>
      </div>
      {selected&&<div className="mt-4 grid gap-3 sm:grid-cols-4">
        <SummaryMetric icon={<CalendarCheck size={16}/>} value={`${machinesFullyChecked}/${machineGroups.length}`} label="Máy đủ ảnh đầu/cuối ca"/>
        <SummaryMetric icon={<Check size={16}/>} value={`${avgFiveS}/10`} label="Điểm 5S trung bình"/>
        <SummaryMetric icon={<AlertTriangle size={16}/>} value={String(machineIssues)} label="Máy cần bảo trì/hỏng" danger={machineIssues>0}/>
        <SummaryMetric icon={<AlertOctagon size={16}/>} value={String(openBreakdowns)} label="Báo hỏng đang mở" danger={openBreakdowns>0}/>
      </div>}
      {selected?<div className="mt-4 grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
        {machineGroups.map(group=><MachineGroupCard key={group.code} courseId={courseId} sessionId={selected.id} code={group.code} label={machines.find(m=>m.code===group.code)?.label} members={group.members} photos={machinePhotos} score={machineScores.find(item=>item.machine_code===group.code)} onScoreSaved={loadMachineData} reports={breakdowns.filter(r=>r.machine_code===group.code)} onReported={loadBreakdowns}/>)}
        <MachineGroupCard courseId={courseId} sessionId={selected.id} code="XUONG" label="Ảnh toàn xưởng" icon={Camera} members={[]} photos={machinePhotos} score={machineScores.find(item=>item.machine_code==="XUONG")} onScoreSaved={loadMachineData} singlePhoto showFiveS={false} reports={breakdowns.filter(r=>r.machine_code==="XUONG")} onReported={loadBreakdowns}/>
        <MachineGroupCard courseId={courseId} sessionId={selected.id} code="RAC" label="Ảnh thùng rác" icon={Trash2} members={[]} photos={machinePhotos} score={machineScores.find(item=>item.machine_code==="RAC")} onScoreSaved={loadMachineData} singlePhoto showFiveS={false} reports={breakdowns.filter(r=>r.machine_code==="RAC")} onReported={loadBreakdowns}/>
        {!machineGroups.length&&<p className="rounded-xl border border-dashed border-white/10 p-6 text-center text-sm text-slate-500 sm:col-span-2 xl:col-span-1">Chưa có sinh viên nào chọn máy trong buổi này.</p>}
      </div>:<div className="mt-5 grid min-h-56 place-items-center rounded-2xl border border-dashed border-white/10 text-sm text-slate-500"><Wrench size={26}/><span className="mt-2">Chọn một buổi điểm danh để xem tình trạng máy.</span></div>}
    </section>}

    {view==="summary"&&<AttendanceMatrixSummary students={students} sessions={sessions} allRecords={allRecords}/>}
  </div>;
}

function AttendanceMatrixSummary({students,sessions,allRecords}:{students:Student[];sessions:AttendanceSession[];allRecords:AttendanceRecord[]}){
  const orderedSessions=sessions.toSorted((a,b)=>Date.parse(a.starts_at)-Date.parse(b.starts_at));
  const rows=students.map(student=>{
    const own=allRecords.filter(row=>row.student_id===student.id);
    const present=own.filter(row=>row.status==="present").length;
    const late=own.filter(row=>row.status==="late").length;
    const absent=own.filter(row=>row.status==="absent").length;
    const rate=orderedSessions.length?Math.min(100,Math.round((present+late)/orderedSessions.length*100)):0;
    const cells=orderedSessions.map(session=>own.find(row=>row.session_id===session.id)?.status??null);
    return {...student,present,late,absent,rate,cells};
  });
  const classRate=orderedSessions.length&&students.length?Math.round(allRecords.filter(row=>row.status==="present"||row.status==="late").length/(orderedSessions.length*students.length)*100):0;
  const perfect=rows.filter(row=>orderedSessions.length>0&&row.present===orderedSessions.length).length;
  const concern=rows.filter(row=>row.absent>=2||row.late>=3||(orderedSessions.length>=3&&row.rate<75)).length;

  return <section className="rounded-2xl border border-white/10 bg-[#0B1020] p-5">
    <div className="flex items-center gap-2"><Grid3x3 size={19} className="text-cyan-300"/><h3 className="font-display text-xl font-bold text-white">Tổng hợp điểm danh theo học sinh</h3></div>
    <p className="mt-1 text-xs text-slate-500">Ký hiệu: <b className="text-emerald-300">C</b> Có mặt · <b className="text-amber-300">T</b> Đi trễ · <b className="text-blue-300">VP</b> Vắng có phép · <b className="text-red-300">V</b> Vắng không phép</p>
    <div className="mt-4 grid gap-3 sm:grid-cols-2 xl:grid-cols-4"><SummaryMetric icon={<CalendarCheck size={16}/>} value={String(orderedSessions.length)} label="Buổi đã tổ chức"/><SummaryMetric icon={<Users size={16}/>} value={orderedSessions.length?`${classRate}%`:"—"} label="Tham dự trung bình"/><SummaryMetric icon={<UserCheck size={16}/>} value={String(perfect)} label="Chuyên cần"/><SummaryMetric icon={<AlertTriangle size={16}/>} value={String(concern)} label="Cần nhắc nhở" danger/></div>
    {!orderedSessions.length?<p className="mt-4 rounded-xl border border-dashed border-white/10 p-8 text-center text-sm text-slate-500">Chưa có buổi điểm danh nào.</p>:
    <div className="mt-4 max-h-[70vh] overflow-auto rounded-xl border border-white/10">
      <table className="w-full min-w-max border-separate border-spacing-0 text-sm">
        <thead className="sticky top-0 z-20 bg-[#10192a]">
          <tr>
            <th className="sticky left-0 z-30 min-w-48 border-b border-r border-white/10 bg-[#10192a] p-3 text-left text-xs uppercase text-slate-400">Sinh viên</th>
            {orderedSessions.map(session=><th key={session.id} className="min-w-14 border-b border-white/10 p-2 text-center text-[11px] font-bold text-slate-400" title={session.title}>{new Date(session.starts_at).toLocaleDateString("vi-VN",{day:"2-digit",month:"2-digit"})}</th>)}
            <th className="min-w-16 border-b border-white/10 p-2 text-center text-xs uppercase text-slate-400">Tỷ lệ</th>
          </tr>
        </thead>
        <tbody>
          {rows.map(row=><tr key={row.id} className="group">
            <td className="sticky left-0 z-10 border-b border-r border-white/5 bg-[#0B1020] p-3 group-hover:bg-[#10192a]"><strong className="block text-sm text-white">{row.name}</strong><small className="text-slate-500">{row.className}</small></td>
            {row.cells.map((status,index)=><td key={index} className="border-b border-white/5 p-1.5 text-center">{status?<span className={`inline-flex h-6 w-9 items-center justify-center rounded-md text-[11px] font-bold ${statusMeta[status].active}`}>{statusMeta[status].code}</span>:<span className="text-slate-700">–</span>}</td>)}
            <td className="border-b border-white/5 p-2 text-center"><span className={`rounded-full px-2.5 py-1 text-xs font-bold ${row.rate>=90?"bg-emerald-500/10 text-emerald-300":row.rate>=75?"bg-amber-500/10 text-amber-300":"bg-red-500/10 text-red-300"}`}>{orderedSessions.length?`${row.rate}%`:"—"}</span></td>
          </tr>)}
          {!rows.length&&<tr><td colSpan={orderedSessions.length+2} className="p-8 text-center text-slate-500">Chưa có sinh viên.</td></tr>}
        </tbody>
      </table>
    </div>}
  </section>;
}
function SummaryMetric({icon,value,label,danger=false}:{icon:React.ReactNode;value:string;label:string;danger?:boolean}){return <div className={`rounded-xl border p-4 ${danger?"border-red-400/15 bg-red-500/5 text-red-300":"border-cyan-400/10 bg-cyan-500/5 text-cyan-300"}`}><div className="flex items-center gap-2 text-xs font-bold uppercase">{icon}{label}</div><strong className="mt-2 block text-2xl text-white">{value}</strong></div>}

function MachineGroupCard({courseId,sessionId,code,label,icon:Icon=Wrench,members,photos,score,onScoreSaved,singlePhoto=false,showFiveS=true,reports,onReported}:{courseId:number;sessionId:number;code:string;label?:string;icon?:typeof Wrench;members:{id:string;name:string}[];photos:AttendanceMachinePhoto[];score?:AttendanceMachineScore;onScoreSaved:()=>void;singlePhoto?:boolean;showFiveS?:boolean;reports:EquipmentBreakdownReport[];onReported:()=>void}){
  const[noteDraft,setNoteDraft]=useState(score?.note??"");
  useEffect(()=>{setNoteDraft(score?.note??"")},[score?.note]);
  const openReports=reports.filter(r=>r.status==="open");
  async function toggleCriterion(key:typeof FIVE_S_CRITERIA[number]["key"]){try{await updateAttendanceMachineScore(sessionId,code,{[key]:!score?.[key]});onScoreSaved()}catch{/* silent: hiển thị lại giá trị cũ ở lần tải sau */}}
  async function saveEquipment(status:EquipmentStatus){try{await updateAttendanceMachineScore(sessionId,code,{equipment_status:status});onScoreSaved()}catch{/* silent */}}
  async function saveNote(){try{await updateAttendanceMachineScore(sessionId,code,{note:noteDraft});onScoreSaved()}catch{/* silent */}}
  const equipmentStatus=score?.equipment_status??"normal";
  return <div className="rounded-xl border border-white/10 bg-white/[.02] p-3">
    <div className="flex items-center justify-between gap-2">
      <span className="flex items-center gap-1.5 text-sm font-bold text-white"><Icon size={14} className="text-orange-300"/>{label??`Máy ${code}`}</span>
      {showFiveS&&<span className="text-xs font-bold text-emerald-300">{fiveSScore(score)}<span className="text-[10px] font-normal text-slate-500">/10</span></span>}
    </div>
    {members.length>0&&<p className="mt-1 truncate text-[11px] text-slate-500" title={members.map(m=>m.name).join(", ")}>{members.map(m=>m.name).join(", ")}</p>}
    <div className={`mt-2 grid gap-1.5 ${singlePhoto?"grid-cols-1":"grid-cols-2"}`}>
      {singlePhoto?<PhotoCheckpointCell label="Ảnh" code={code} checkpoint="end" photos={photos}/>:<>
        <PhotoCheckpointCell label="Đầu ca" code={code} checkpoint="start" photos={photos}/>
        <PhotoCheckpointCell label="Cuối ca" code={code} checkpoint="end" photos={photos}/>
      </>}
    </div>
    {showFiveS&&<>
      <select value={equipmentStatus} onChange={e=>void saveEquipment(e.target.value as EquipmentStatus)} className={`mt-2 w-full rounded-lg border bg-[#080d1d] px-2 py-1.5 text-[11px] font-bold ${EQUIPMENT_STATUS_META[equipmentStatus].style}`}>
        {(Object.entries(EQUIPMENT_STATUS_META) as [EquipmentStatus,{label:string;style:string}][]).map(([value,meta])=><option key={value} value={value}>{meta.label}</option>)}
      </select>
      <div className="mt-2 space-y-1">
        {FIVE_S_CRITERIA.map(item=>{const achieved=Boolean(score?.[item.key]);return <button key={item.key} type="button" onClick={()=>void toggleCriterion(item.key)} className="flex w-full items-center justify-between gap-2 rounded-lg px-1 py-1 text-left hover:bg-white/[.03]">
          <span className="min-w-0 flex-1 truncate text-[11px] text-slate-300">{item.label} <small className="text-slate-600">— {item.hint}</small></span>
          <span className={`flex h-5 w-5 shrink-0 items-center justify-center rounded-md ${achieved?"bg-emerald-500 text-white":"border border-white/15 text-transparent"}`}><Check size={12}/></span>
        </button>})}
      </div>
    </>}
    <input type="text" value={noteDraft} onChange={e=>setNoteDraft(e.target.value)} onBlur={saveNote} placeholder="Ghi chú nhóm…" className="mt-2 w-full rounded-lg border border-white/10 bg-[#080d1d] px-2 py-1 text-xs text-white placeholder:text-slate-600"/>
    <BreakdownReportSection courseId={courseId} sessionId={sessionId} code={code} openReports={openReports} onReported={onReported}/>
  </div>;
}

function BreakdownReportSection({courseId,sessionId,code,openReports,onReported}:{courseId:number;sessionId:number;code:string;openReports:EquipmentBreakdownReport[];onReported:()=>void}){
  const[reporting,setReporting]=useState(false);
  const[file,setFile]=useState<File|null>(null);
  const[description,setDescription]=useState("");
  const[busy,setBusy]=useState(false);
  const[error,setError]=useState("");
  async function submit(){if(!file||!description.trim())return;setBusy(true);setError("");try{await reportEquipmentBreakdown({courseId,sessionId,machineCode:code,description,file});setReporting(false);setFile(null);setDescription("");onReported()}catch(cause){setError(cause instanceof Error?cause.message:"Không báo hỏng được.")}finally{setBusy(false)}}
  async function resolve(id:number){try{await resolveEquipmentBreakdown(id,"");onReported()}catch{/* silent */}}
  async function view(path:string){const win=window.open("","_blank","noopener,noreferrer");try{const signed=await createEquipmentBreakdownPhotoUrl(path);if(win)win.location.href=signed}catch{win?.close()}}
  return <div className="mt-2 border-t border-white/5 pt-2">
    {openReports.map(report=><div key={report.id} className="mb-1.5 rounded-lg border border-red-400/20 bg-red-500/10 p-2">
      <div className="flex items-center gap-1.5 text-[11px] font-bold text-red-200"><AlertOctagon size={12}/>Báo hỏng</div>
      <p className="mt-0.5 text-[11px] text-red-100/80">{report.description}</p>
      <div className="mt-1.5 flex items-center gap-2">
        <button type="button" onClick={()=>void view(report.storage_path)} className="text-[10px] font-bold text-red-200 underline">Xem ảnh</button>
        <button type="button" onClick={()=>void resolve(report.id)} className="text-[10px] font-bold text-emerald-300">Đã sửa xong</button>
      </div>
    </div>)}
    {reporting?<div className="rounded-lg border border-white/10 bg-black/15 p-2">
      <input type="file" accept="image/*" capture="environment" onChange={e=>setFile(e.target.files?.[0]??null)} className="block w-full text-[10px] text-slate-400"/>
      <textarea value={description} onChange={e=>setDescription(e.target.value)} rows={2} placeholder="Mô tả tình trạng hỏng…" className="mt-1.5 w-full resize-none rounded-md border border-white/10 bg-[#080d1d] px-2 py-1 text-[11px] text-white placeholder:text-slate-600"/>
      {error&&<p className="mt-1 text-[10px] text-red-300">{error}</p>}
      <div className="mt-1.5 flex gap-1.5">
        <button type="button" disabled={busy||!file||!description.trim()} onClick={submit} className="rounded-md bg-red-600 px-2.5 py-1 text-[10px] font-bold text-white disabled:opacity-40">Gửi báo hỏng</button>
        <button type="button" onClick={()=>setReporting(false)} className="rounded-md border border-white/10 px-2.5 py-1 text-[10px] font-bold text-slate-300">Hủy</button>
      </div>
    </div>:<button type="button" onClick={()=>setReporting(true)} className="flex items-center gap-1 text-[10px] font-bold text-red-300 hover:text-red-200"><AlertOctagon size={11}/>Báo hỏng máy</button>}
  </div>;
}

function PhotoCheckpointCell({label,code,checkpoint,photos}:{label:string;code:string;checkpoint:MachineCheckpoint;photos:AttendanceMachinePhoto[]}){
  const photo=photos.find(item=>item.machine_code===code&&item.checkpoint===checkpoint);
  async function view(){if(!photo)return;const win=window.open("","_blank","noopener,noreferrer");try{const signed=await createAttendanceMachinePhotoUrl(photo.storage_path);if(win)win.location.href=signed}catch{win?.close()}}
  return <button type="button" disabled={!photo} onClick={view} className={`rounded-lg border px-2 py-1.5 text-left text-[10px] font-bold disabled:cursor-not-allowed ${photo?"border-emerald-400/30 bg-emerald-500/10 text-emerald-200":"border-white/10 bg-white/[.01] text-slate-600"}`}>
    <span className="flex items-center gap-1">{photo?<Check size={10}/>:null}{label}</span>
    <small className="block font-normal opacity-70">{photo?(photo.profiles?.full_name??"Đã nộp"):"Chưa nộp"}</small>
  </button>;
}
