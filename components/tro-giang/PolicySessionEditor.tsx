'use client';
import { useState } from 'react';
import type { TaSessionRow } from '@/lib/tro-giang/queries';
import { emptyPolicy, updatePolicySession } from '@/lib/tro-giang/policy';
import PolicySessionFields from './PolicySessionFields';
import { useToast } from '@/components/ui/Toast';
const cls='mt-1 w-full rounded-xl border border-white/15 bg-[#0B1020] px-3 py-2 text-white';
export default function PolicySessionEditor({ session, onSaved, onCancel }: { session: TaSessionRow; onSaved:()=>void; onCancel:()=>void }) {
 const [draft,setDraft]=useState({...session,policy:{...emptyPolicy(),...session.policy}});const [reason,setReason]=useState('');const [busy,setBusy]=useState(false);const toast=useToast();
 async function save(){if(!reason.trim()){toast('error','Ghi lý do điều chỉnh.');return}setBusy(true);try{await updatePolicySession(session.id,{work_date:draft.work_date,class_label:draft.class_label,start_time:draft.start_time,end_time:draft.end_time,student_touches:draft.student_touches,papers_graded:draft.papers_graded,policy:draft.policy,status:draft.status,phudao_students:draft.phudao_students,note:`${session.note??''}\nĐiều chỉnh: ${reason.trim()}`.trim()});toast('success','Đã sửa buổi. Nếu tháng đã chốt, cần chốt lại.');onSaved()}catch(e){toast('error',e instanceof Error?e.message:'Không lưu được')}finally{setBusy(false)}}
 return <section className="space-y-3 rounded-2xl border border-blue-400/30 p-4"><h3 className="font-semibold text-white">Điều chỉnh công · {session.work_date}</h3><p className="text-xs text-slate-400">Thay đổi được ghi vào nhật ký; tháng đã chốt sẽ mở lại.</p>
  <label className="block text-sm text-slate-300">Ngày<input className={cls} type="date" min="2026-10-01" value={draft.work_date} onChange={e=>setDraft({...draft,work_date:e.target.value})}/></label>
  <label className="block text-sm text-slate-300">Lớp<input className={cls} value={draft.class_label??''} onChange={e=>setDraft({...draft,class_label:e.target.value})}/></label>
  {session.session_type!=='video' && <div className="grid grid-cols-2 gap-3"><label className="text-sm text-slate-300">Bắt đầu<input className={cls} type="time" value={draft.start_time??''} onChange={e=>setDraft({...draft,start_time:e.target.value})}/></label><label className="text-sm text-slate-300">Kết thúc<input className={cls} type="time" value={draft.end_time??''} onChange={e=>setDraft({...draft,end_time:e.target.value})}/></label></div>}
  {session.session_type==='lop' && <label className="block text-sm text-slate-300">Số lượt tiếp xúc<input className={cls} type="number" min="0" step="1" value={draft.student_touches??0} onChange={e=>setDraft({...draft,student_touches:Number(e.target.value)})}/></label>}
  {session.session_type==='phudao' && <label className="block text-sm text-slate-300">Các em phụ đạo (mỗi dòng một em, tối đa 4)<textarea className={cls} value={draft.phudao_students.join('\n')} onChange={e=>{const names=e.target.value.split('\n');setDraft({...draft,phudao_students:names,policy:{...draft.policy,followups:names.map(student=>draft.policy.followups.find(f=>f.student===student)??{student,lesson:'',difficulty:''})}})}}/></label>}
  {['lop','phudao'].includes(session.session_type)&&<PolicySessionFields value={draft.policy} onChange={policy=>setDraft({...draft,policy})} type={session.session_type} students={draft.phudao_students}/>}
  {session.session_type==='chambai'&&<label className="block text-sm text-slate-300">Số bài chấm<input className={cls} type="number" min="1" step="1" value={draft.papers_graded??0} onChange={e=>setDraft({...draft,papers_graded:Number(e.target.value)})}/></label>}
  <label className="block text-sm text-slate-300">Trạng thái<select className={cls} value={draft.status} onChange={e=>setDraft({...draft,status:e.target.value as TaSessionRow['status']})}><option value="submitted">Chờ duyệt</option><option value="approved">Đã duyệt</option><option value="rejected">Từ chối</option></select></label>
  <label className="block text-sm text-slate-300">Lý do điều chỉnh<textarea className={cls} value={reason} onChange={e=>setReason(e.target.value)}/></label>
  <div className="flex gap-3"><button disabled={busy} onClick={save} className="rounded-xl bg-blue-600 px-4 py-2 text-white disabled:opacity-50">Lưu điều chỉnh</button><button onClick={onCancel} className="px-4 py-2 text-slate-300">Hủy</button></div>
 </section>;
}
