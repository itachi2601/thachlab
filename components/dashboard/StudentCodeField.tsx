"use client";

import { useEffect, useState } from "react";
import { IdCard, Pencil, Save, X } from "lucide-react";
import { fetchMyStudentCode, updateMyStudentCode } from "@/services/student-profile";

export default function StudentCodeField({ studentId, preview = false }: { studentId: string; preview?: boolean }) {
  const [code, setCode] = useState("");
  const [draft, setDraft] = useState("");
  const [editing, setEditing] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (preview) return;
    fetchMyStudentCode(studentId).then((value) => { setCode(value); setDraft(value); setEditing(!value); }).catch(() => setError("Chưa thể tải mã số sinh viên."));
  }, [studentId, preview]);

  if (preview) return null;
  async function save() { setBusy(true); setError(""); try { const value = await updateMyStudentCode(studentId, draft); setCode(value); setDraft(value); setEditing(false); } catch (cause) { setError(cause instanceof Error ? cause.message : "Không lưu được mã số sinh viên."); } finally { setBusy(false); } }

  return <div className="mt-3 max-w-md rounded-xl border border-cyan-400/15 bg-black/15 p-3">
    <div className="flex items-center justify-between gap-3"><span className="flex items-center gap-2 text-xs font-bold text-cyan-200"><IdCard size={15}/>Mã số sinh viên</span>{code&&!editing&&<button type="button" onClick={()=>setEditing(true)} className="flex items-center gap-1 text-[10px] font-bold text-slate-400 hover:text-white"><Pencil size={11}/>Sửa</button>}</div>
    {editing?<div className="mt-2 flex gap-2"><input autoFocus value={draft} onChange={(event)=>setDraft(event.target.value.toUpperCase())} onKeyDown={(event)=>{if(event.key==="Enter")void save()}} placeholder="Nhập mã số sinh viên" maxLength={30} className="min-w-0 flex-1 rounded-lg border border-white/10 bg-[#080d1d] px-3 py-2 font-mono text-sm uppercase text-white outline-none focus:border-cyan-400/50"/><button disabled={busy||draft.trim().length<2} onClick={()=>void save()} className="rounded-lg bg-cyan-600 px-3 text-white disabled:opacity-40"><Save size={15}/></button>{code&&<button onClick={()=>{setDraft(code);setEditing(false)}} className="rounded-lg border border-white/10 px-3 text-slate-400"><X size={15}/></button>}</div>:<strong className="mt-1 block font-mono text-base tracking-wider text-white">{code}</strong>}
    {error&&<p className="mt-2 text-[10px] text-red-300">{error}</p>}
  </div>;
}
