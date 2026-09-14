'use client';
import { POLICY_SCORES, type MonthPolicy } from '@/lib/tro-giang/policy';
import { formatVnd, formatHours } from '@/lib/tro-giang/format';
export default function PolicyMonthSummary({ score }: { score: MonthPolicy }) {
 const money=(n:number|null)=>n===null?'Chờ đủ dữ liệu':formatVnd(n);
 return <div className="space-y-4">
  <div className="flex flex-wrap items-center justify-between gap-3"><span className={`rounded-full px-3 py-1 text-xs font-semibold ${score.closed_at?'bg-emerald-500/15 text-emerald-300':'bg-amber-500/15 text-amber-200'}`}>{score.closed_at?'Đã chốt':'Tạm tính · chưa chốt'}</span><span className="text-sm text-slate-300">Hệ số đứng lớp: <b>{score.class_factor?.toFixed(1) ?? 'Chờ điểm'}</b></span></div>
  {score.trial && <p className="rounded-xl bg-blue-500/10 p-3 text-sm text-blue-200">Tháng 10 chỉ chấm điểm, chưa giảm lương: hệ số đứng lớp 1,0 cho mọi trợ giảng.</p>}
  <div className="grid gap-3 sm:grid-cols-2">{POLICY_SCORES.map(([key,label,max])=><div key={key} className="rounded-xl border border-white/10 p-3"><div className="flex justify-between gap-2 text-sm"><span className="text-slate-300">{label}</span><b className="text-white">{score[key] ?? '—'} / {max}</b></div><div className="mt-2 h-1.5 overflow-hidden rounded-full bg-white/10"><div className="h-full bg-blue-400" style={{width:`${100*(score[key]??0)/max}%`}}/></div></div>)}</div>
  <div className="flex justify-between text-lg font-bold text-white"><span>Tổng điểm</span><span>{score.total_score ?? 'Chưa đủ điểm'}{score.total_score!==null?' / 100':''}</span></div>
  {!!score.missing.length && <ul className="list-inside list-disc rounded-xl bg-amber-500/10 p-3 text-sm text-amber-200">{score.missing.map(m=><li key={m}>{m}</li>)}</ul>}
  <dl className="space-y-2 border-t border-white/10 pt-4 text-sm text-slate-300">
   <div className="flex justify-between"><dt>Đơn giá giờ</dt><dd>{money(score.hourly_rate)}</dd></div>
   <div className="flex justify-between"><dt>Lên lớp · {formatHours(score.class_hours)} giờ × {score.class_factor??'?'}</dt><dd>{money(score.class_pay)}</dd></div>
   <div className="flex justify-between"><dt>Chữa bài · {formatHours(score.teaching_hours*60)} phút × 1,6</dt><dd>{money(score.teaching_pay)}</dd></div>
   <div className="flex justify-between"><dt>Phụ đạo · {formatHours(score.tutoring_hours)} giờ (×1,2 / ×1,4)</dt><dd>{money(score.tutoring_pay)}</dd></div>
   <div className="flex justify-between"><dt>Chấm kiểm tra · {score.papers} bài × 1.500 đ</dt><dd>{money(score.grading_pay)}</dd></div>
   <div className="flex justify-between border-t border-white/10 pt-3 text-lg font-bold text-white"><dt>{score.closed_at?'Tiền đã chốt':'Tiền tạm tính'}</dt><dd>{money(score.total_pay)}</dd></div>
  </dl>
  <p className="text-xs text-slate-400">Video, thưởng lượt xem và giới thiệu học sinh tính riêng ở mục Video TikTok. Không có thưởng hiệu suất theo giờ.</p>
  {score.note && <p className="rounded-xl bg-white/5 p-3 text-sm text-slate-300">Ghi chú của thầy: {score.note}</p>}
  {score.closed_at && <p className="text-xs text-slate-400">Công bố {new Date(score.closed_at).toLocaleString('vi-VN')}. Báo thầy trong 3 ngày nếu cần đối chiếu.</p>}
 </div>;
}
