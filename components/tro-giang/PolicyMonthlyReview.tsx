'use client';
import { useEffect, useState } from 'react';
import PolicyPersonReview from './PolicyPersonReview';
import { fetchAssistants, type TaAssistant } from '@/lib/tro-giang/queries';
const cls='mt-1 w-full rounded-xl border border-white/15 bg-panel px-3 py-2 text-white';
export default function PolicyMonthlyReview({month,reloadKey=0,initialId}:{month:string;reloadKey?:number;initialId?:string}){
 const [assistants,setAssistants]=useState<TaAssistant[]>([]);const [selected,setSelected]=useState('');const [error,setError]=useState('');
 useEffect(()=>{let active=true;fetchAssistants().then(a=>{if(active){setAssistants(a);setSelected(initialId&&a.some(x=>x.id===initialId)?initialId:a[0]?.id??'')}}).catch(e=>{if(active)setError(e.message)});return()=>{active=false}},[]);
 return <div className="space-y-4">{error&&<p role="alert" className="text-red-300">{error}</p>}<label className="block text-sm text-slate-300">Trợ giảng<select className={cls} value={selected} onChange={e=>setSelected(e.target.value)}>{assistants.map(a=><option key={a.id} value={a.id}>{a.full_name}{!a.active?' · ngừng hoạt động':''}</option>)}</select></label>{selected&&<PolicyPersonReview key={`${selected}-${month}-${reloadKey}`} id={selected} month={month}/>}</div>;
}
