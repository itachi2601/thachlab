'use client';
import { useEffect, useState } from 'react';
import Link from 'next/link';
import type { TaAssistant } from '@/lib/tro-giang/queries';
import { getPolicyMonth, type MonthPolicy } from '@/lib/tro-giang/policy';
import { isDemoAssistant } from '@/lib/tro-giang/demo';
import PolicyMonthSummary from './PolicyMonthSummary';
function demoMonth(id:string,month:string):MonthPolicy {return {assistant_id:id,month,closed_at:null,note:'Số liệu minh họa, không phải công thực tế.',overrides:{},touches:27,phudao:25,homework:20,attendance:15,observation:8,total_score:95,hourly_rate:60000,class_factor:1,class_count:8,tutoring_count:2,pending_count:0,class_hours:11.25,teaching_hours:0.75,tutoring_hours:3,tutoring_weighted_hours:4.2,papers:20,class_pay:675000,teaching_pay:72000,tutoring_pay:252000,grading_pay:30000,total_pay:1029000,missing:[],trial:month==='2026-10-01'}};
export default function PolicyStudentMonth({assistant,month}:{assistant:TaAssistant;month:string}){
 const demo=isDemoAssistant(assistant);const [score,setScore]=useState<MonthPolicy|null>(()=>demo?demoMonth(assistant.id,month):null);const [error,setError]=useState('');const [retry,setRetry]=useState(0);
 useEffect(()=>{if(demo)return;let active=true;getPolicyMonth(assistant.id,month).then(s=>{if(active){setScore(s);setError('')}}).catch(e=>{if(active)setError(e.message)});return()=>{active=false}},[assistant.id,month,demo,retry]);
 return <div className="space-y-5"><div><h1 className="text-2xl font-bold text-white">Chào {assistant.short_name}</h1><p className="mt-1 text-sm text-slate-400">Công việc và thù lao tháng {month.slice(0,7)}</p></div><div className="grid grid-cols-2 gap-3"><Link href="/tro-giang/ghi" className="rounded-xl bg-blue-600 px-4 py-3 text-center font-semibold text-white">Ghi buổi làm việc</Link><Link href="/tro-giang/video" className="rounded-xl border border-white/15 px-4 py-3 text-center text-white">Video TikTok</Link></div>{error?<p role="alert" className="rounded-xl bg-red-500/10 p-4 text-sm text-red-200">{error}<button onClick={()=>setRetry(r=>r+1)} className="ml-2 underline">Thử lại</button></p>:score?<PolicyMonthSummary score={score}/>:<p className="text-slate-400">Đang tải điểm và công…</p>}<p className="rounded-xl border border-white/10 p-4 text-sm text-slate-400">Từ khóa sau: thang bậc và điều kiện lên bậc sẽ được công bố riêng. Hiện giữ đơn giá thỏa thuận, chưa áp dụng Phần B.</p></div>;
}
