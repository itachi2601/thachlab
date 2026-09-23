'use client';
import { useEffect, useState } from 'react';
import './local-preview.css';
import { useSearchParams } from 'next/navigation';
import { demoAssistant } from '@/lib/tro-giang/demo';
import PolicyStudentMonth from './PolicyStudentMonth';
import GhiBuoiForm from './GhiBuoiForm';
import TroGiangVideo from './TroGiangVideo';
const assistant=demoAssistant();
const tabs=[['tong-quan','Tổng quan'],['ghi','Ghi buổi'],['video','Video TikTok']] as const;
export default function LocalAssistantPreview({embedded=false,theme='dark',initialTab='ghi'}:{embedded?:boolean;theme?:'dark'|'light';initialTab?:string}){
 const [tab,setTab]=useState<string>(initialTab);
 useEffect(()=>{document.documentElement.dataset.theme=embedded?theme:'dark'},[embedded,theme]);
 const [month,setMonth]=useState('2026-10');
 if(!embedded)return <main className="min-h-screen space-y-4 bg-[#080d18] px-4 py-5 text-slate-200">
  <header className="flex flex-wrap items-center justify-between gap-3"><div><h1 className="text-xl font-bold text-white">Trợ giảng · so sánh Dark / Light</h1><p className="mt-1 text-sm text-slate-400">Hai giao diện chạy thật với dữ liệu mẫu. Thầy thử nhập riêng trong từng khung.</p></div><nav aria-label="Phần xem mẫu" className="flex gap-2">{tabs.map(([key,label])=><button key={key} onClick={()=>setTab(key)} className={`rounded-xl px-4 py-2 text-sm font-semibold ${tab===key?'bg-blue-600 text-white':'border border-white/15 text-slate-300'}`}>{label}</button>)}</nav></header>
  <div className="overflow-x-auto"><div className="grid grid-cols-[repeat(2,minmax(360px,1fr))] gap-4">{(['dark','light'] as const).map(t=><section key={t} className="overflow-hidden rounded-2xl border border-slate-600/40"><h2 className={`px-4 py-2 text-sm font-bold ${t==='light'?'bg-slate-100 text-slate-800':'bg-slate-900 text-slate-100'}`}>{t==='dark'?'Dark · nền tối':'Light · nền sáng'}</h2><iframe title={`Mẫu trợ giảng ${t}`} src={`/tro-giang/mau/?frame=1&theme=${t}&tab=${tab}`} className="h-[calc(100dvh-155px)] min-h-[620px] w-full border-0" style={{background:t==='light'?'#f8fafc':'#05070b',colorScheme:t}}/></section>)}</div></div>
 </main>;
 return <main className="ta-preview mx-auto min-h-screen w-full min-w-0 max-w-xl space-y-5 px-5 py-5" onClick={e=>{
   const link=(e.target as HTMLElement).closest('a');if(!link)return;
   const href=link.getAttribute('href')??'';
   if(href.startsWith('/tro-giang')){e.preventDefault();setTab(href.startsWith('/tro-giang/ghi')?'ghi':href.startsWith('/tro-giang/video')?'video':'tong-quan')}
 }}>
  <header className="rounded-2xl border border-fuchsia-400/30 bg-fuchsia-500/10 p-4"><p className="font-semibold text-fuchsia-200">{tab==='ghi'?'Ghi buổi làm việc':'Bản mẫu trợ giảng'}</p><p className="mt-1 text-sm text-slate-300">Dữ liệu giả lập, không ghi công hoặc thay đổi tiền thật.</p></header>
  <nav className="flex min-w-0 gap-2" aria-label="Trang trợ giảng">{tabs.map(([key,label])=><button key={key} onClick={()=>setTab(key)} className={`min-w-0 flex-1 rounded-xl px-2 py-3 text-xs font-semibold ${tab===key?'bg-blue-600 text-white':'border border-white/15 text-slate-300'}`}>{label}</button>)}</nav>
  {tab==='tong-quan'&&<><label className="block text-sm text-slate-300">Tháng xem mẫu<select className="ml-3 rounded-xl border border-white/15 bg-panel px-3 py-2 text-white" value={month} onChange={e=>setMonth(e.target.value)}><option value="2026-10">Tháng 10/2026 · chạy thử</option><option value="2026-11">Tháng 11/2026 · áp dụng hệ số</option></select></label><PolicyStudentMonth key={month} assistant={assistant} month={`${month}-01`}/></>}
  {tab==='ghi'&&<GhiBuoiForm assistant={assistant} initialWorkDate="2026-10-01" previewDraftScope={theme}/>}
  {tab==='video'&&<TroGiangVideo assistant={assistant}/>}
 </main>;
}

export function LocalPreviewRoute(){
 const params=useSearchParams();
 return <LocalAssistantPreview key={params.toString()} embedded={params.get('frame')==='1'} theme={params.get('theme')==='light'?'light':'dark'} initialTab={params.get('tab')??'ghi'}/>;
}
