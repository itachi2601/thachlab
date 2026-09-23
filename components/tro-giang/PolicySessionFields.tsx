'use client';
import type { SessionPolicy } from '@/lib/tro-giang/policy';
const input = 'mt-1 w-full rounded-xl border border-white/15 bg-panel px-3 py-2.5 text-white';
export default function PolicySessionFields({ value, onChange, type, students = [] }: {
 value: SessionPolicy; onChange: (v: SessionPolicy) => void; type: string; students?: string[];
}) {
 const patch = (p: Partial<SessionPolicy>) => onChange({ ...value, ...p });
 const checks: [keyof SessionPolicy, string][] = type === 'lop' ? [
  ['arrived_early','Đến sớm 10 phút, đã hỏi nội dung buổi học'], ['homework_checked','Đã kiểm tra bài tập đầu buổi và ghi lỗi lên bài'],
  ['walked_tables','Đã đi hết các bàn'], ['reported_students','Đã báo thầy các em cần chú ý'],
 ] : [['prepared','Đã nắm nội dung trước buổi'],['recalled','Đã dò lại bài cũ'],['asked_each','Mỗi em đều được hỏi ít nhất một lần']];
 return <section className="space-y-4 rounded-2xl border border-blue-400/25 bg-blue-500/5 p-4">
  <h2 className="font-semibold text-white">{type === 'lop' ? 'Phiếu buổi lên lớp' : 'Phiếu phụ đạo'} · Quy chế từ 01/10/2026</h2>
  {type === 'lop' && <label className="block text-sm text-slate-300">Chuyên cần<select className={input} value={value.attendance} onChange={e=>patch({attendance:e.target.value as SessionPolicy['attendance']})}>
   <option value="on_time">Đúng giờ</option><option value="late">Đi muộn</option><option value="excused_absence">Vắng có báo trước / được thầy chấp nhận</option><option value="unexcused_absence">Vắng không báo / muộn quá 15 phút không báo</option>
  </select><span className="mt-1 block text-xs text-slate-400">Buổi vắng không tính giờ lên lớp hay chữa bài.</span></label>}
  {checks.map(([key,label])=><label key={key} className="flex items-start gap-3 text-sm text-slate-200"><input type="checkbox" className="mt-1 h-4 w-4 accent-blue-500" checked={value[key] === true} onChange={e=>patch({[key]:e.target.checked})}/>{label}</label>)}
  {type === 'lop' ? <>
   <label className="block text-sm text-slate-300">Số em chưa làm bài<input className={input} type="number" min="0" step="1" value={value.homework_missing} onChange={e=>patch({homework_missing:Number(e.target.value)})}/></label>
   <label className="block text-sm text-slate-300">Em cần chú ý — tên và lý do<textarea className={input} rows={3} value={value.attention_note} onChange={e=>patch({attention_note:e.target.value})} placeholder="Tên em · bài đang vướng · lỗi cần sửa"/></label>
   <div className="space-y-3 border-t border-white/10 pt-4"><h3 className="font-semibold text-white">Chữa bài thay thầy</h3><p className="text-xs text-slate-400">Ghi phần thời gian đứng bảng trong buổi này. Thầy duyệt sau; ×1,6 riêng phần này, không nhân chồng hệ số đứng lớp.</p>
    <label className="block text-sm text-slate-300">Số phút đứng bảng (0 nếu không có)<input className={input} type="number" min="0" step="1" value={value.teaching_minutes} onChange={e=>patch({teaching_minutes:Number(e.target.value)})}/></label>
    {value.teaching_minutes > 0 && <label className="block text-sm text-slate-300">Nội dung chữa bài / lời giải đã chuẩn bị<textarea className={input} rows={2} value={value.teaching_note} onChange={e=>patch({teaching_note:e.target.value})}/></label>}
   </div>
  </> : <div className="space-y-3">{students.map((student,i)=>{
   const row=value.followups.find(f=>f.student===student) ?? {student,lesson:'',difficulty:''};
   const change=(p: Partial<typeof row>)=>patch({followups:students.map(s=>s===student?{...row,...p}:value.followups.find(f=>f.student===s)??{student:s,lesson:'',difficulty:''})});
   return <div key={`${student}-${i}`} className="rounded-xl border border-white/10 p-3"><h3 className="font-medium text-white">{student}</h3><label className="block text-sm text-slate-300">Bài đã làm<input className={input} value={row.lesson} onChange={e=>change({lesson:e.target.value})}/></label><label className="mt-2 block text-sm text-slate-300">Còn vướng gì (hoặc ghi đã làm được)<textarea className={input} value={row.difficulty} onChange={e=>change({difficulty:e.target.value})}/></label></div>;
  })}</div>}
 </section>;
}
