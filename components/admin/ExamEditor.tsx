"use client";

import { useMemo, useState } from "react";
import { CheckSquare, FileText, ListChecks, PenLine, Plus, Trash2 } from "lucide-react";
import type { EssayQuestion, Exam, ExamQuestion, MultipleChoiceQuestion, ShortAnswerQuestion, TrueFalseQuestion } from "@/features/exams/types";
import LaTexEditor from "@/components/admin/LaTexEditor";
import { getSupabase } from "@/services/supabase";
import { useToast } from "@/components/ui/Toast";

const inputCls="w-full rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-sm text-white placeholder:text-slate-500 focus:border-primary focus:outline-none";
const LETTERS=["A","B","C","D"];
const TYPE_META={
  multiple_choice:{label:"Trắc nghiệm",description:"Chọn một đáp án đúng",icon:ListChecks,color:"blue"},
  true_false:{label:"Đúng / Sai",description:"Đánh giá từng nhận định",icon:CheckSquare,color:"emerald"},
  short_answer:{label:"Điền khuyết",description:"Nhập đáp án ngắn",icon:PenLine,color:"amber"},
  essay:{label:"Tự luận",description:"Giáo viên chấm theo hướng dẫn",icon:FileText,color:"violet"},
} as const;
type QuestionType=keyof typeof TYPE_META;

function newQuestion(type:QuestionType):ExamQuestion{
  if(type==="multiple_choice")return {type,question:"",options:["","","",""],answer:0,explanation:""};
  if(type==="true_false")return {type,question:"",statements:Array.from({length:4},()=>({text:"",answer:true})),explanation:""};
  if(type==="short_answer")return {type,question:"",answer:"",explanation:""};
  return {type,question:"",suggestedAnswer:"",gradingGuide:"",explanation:""};
}

export default function ExamEditor({exam,initialQuestions,initialTitle,cncBank,onDone}:{exam:Exam|null;initialQuestions?:MultipleChoiceQuestion[];initialTitle?:string;cncBank:{key:string;label:string};onDone:()=>void}){
  const toast=useToast();
  const [title,setTitle]=useState(exam?.title??initialTitle??cncBank.label);
  const [questions,setQuestions]=useState<ExamQuestion[]>(exam?.questions??initialQuestions??[]);
  const [busy,setBusy]=useState(false);const[error,setError]=useState("");
  const counts=useMemo(()=>Object.fromEntries((Object.keys(TYPE_META) as QuestionType[]).map(type=>[type,questions.filter(q=>q.type===type).length])) as Record<QuestionType,number>,[questions]);

  function update(index:number,next:ExamQuestion){setQuestions(current=>current.map((question,i)=>i===index?next:question))}
  async function save(){
    if(!title.trim()){setError("Ngân hàng cần có tiêu đề.");return}if(!questions.length){setError("Hãy thêm ít nhất 1 câu hỏi.");return}
    if(questions.some(q=>!q.question.trim())){setError("Mỗi câu hỏi cần có nội dung.");return}
    setBusy(true);setError("");const payload={title:title.trim(),duration_minutes:20,topic:"CNC",difficulty:"" as const,questions,published:false,cnc_key:cncBank.key};const supabase=getSupabase();
    const result=exam?await supabase.from("exams").update(payload).eq("id",exam.id):await supabase.from("exams").upsert(payload,{onConflict:"cnc_key"});
    setBusy(false);if(result.error){setError(result.error.message??"Không lưu được ngân hàng câu hỏi.");return}toast("success","Đã lưu ngân hàng câu hỏi.");onDone();
  }

  return <div className="space-y-6">
    <header className="rounded-3xl border border-orange-400/20 bg-[radial-gradient(circle_at_90%_0%,rgba(249,115,22,.18),transparent_35%),#0B1020] p-6">
      <p className="text-xs font-bold uppercase tracking-wider text-orange-300">Phần kiểm tra · {questions.length} câu hỏi</p>
      <input value={title} onChange={e=>setTitle(e.target.value)} placeholder={cncBank.label} className={`${inputCls} mt-3 text-lg font-bold`}/>
      <div className="mt-5 grid gap-3 sm:grid-cols-2 xl:grid-cols-4">{(Object.keys(TYPE_META) as QuestionType[]).map(type=><AddTypeCard key={type} type={type} count={counts[type]} onAdd={()=>setQuestions(current=>[...current,newQuestion(type)])}/>)}</div>
    </header>

    {(Object.keys(TYPE_META) as QuestionType[]).map(type=>{const entries=questions.map((q,index)=>({q,index})).filter(item=>item.q.type===type);const meta=TYPE_META[type];const Icon=meta.icon;return <section key={type} className="rounded-3xl border border-white/10 bg-[#0B1020] p-5">
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-white/10 pb-4"><div className="flex items-center gap-3"><span className="flex h-10 w-10 items-center justify-center rounded-xl bg-white/5 text-blue-300"><Icon size={19}/></span><div><h2 className="font-display font-semibold text-white">{meta.label}</h2><p className="text-xs text-slate-500">{meta.description} · {entries.length} câu</p></div></div><button type="button" onClick={()=>setQuestions(current=>[...current,newQuestion(type)])} className="inline-flex items-center gap-1 rounded-full border border-blue-400/25 bg-blue-500/10 px-4 py-2 text-xs font-bold text-blue-200"><Plus size={14}/> Thêm câu {meta.label.toLowerCase()}</button></div>
      <div className="mt-4 space-y-4">{entries.map(({q,index},order)=><QuestionEditor key={index} q={q} number={order+1} onChange={next=>update(index,next)} onRemove={()=>setQuestions(current=>current.filter((_,i)=>i!==index))}/>)}{!entries.length&&<p className="rounded-2xl border border-dashed border-white/10 px-4 py-8 text-center text-sm text-slate-500">Chưa có câu {meta.label.toLowerCase()}.</p>}</div>
    </section>})}
    {error&&<p className="text-sm text-red-400">{error}</p>}
    <div className="sticky bottom-4 flex flex-wrap gap-3 rounded-2xl border border-white/10 bg-[#080D1A]/95 p-4 shadow-2xl backdrop-blur"><button onClick={save} disabled={busy} className="rounded-full bg-[#2563EB] px-6 py-2.5 text-sm font-semibold text-white disabled:opacity-50">{busy?"Đang lưu…":"Lưu toàn bộ câu hỏi"}</button><button onClick={onDone} disabled={busy} className="rounded-full px-5 py-2.5 text-sm text-slate-400 hover:text-white">Quay lại</button></div>
  </div>;
}

function AddTypeCard({type,count,onAdd}:{type:QuestionType;count:number;onAdd:()=>void}){const meta=TYPE_META[type];const Icon=meta.icon;return <button type="button" onClick={onAdd} className="group rounded-2xl border border-white/10 bg-white/5 p-4 text-left hover:border-blue-400/35 hover:bg-white/[.08]"><span className="flex items-center justify-between"><Icon size={20} className="text-blue-300"/><b className="rounded-full bg-white/5 px-2 py-0.5 text-xs text-slate-400">{count}</b></span><strong className="mt-3 block text-sm text-white">{meta.label}</strong><small className="mt-1 block text-slate-500">+ Thêm câu hỏi</small></button>}

function QuestionEditor({q,number,onChange,onRemove}:{q:ExamQuestion;number:number;onChange:(q:ExamQuestion)=>void;onRemove:()=>void}){return <article className="space-y-4 rounded-2xl border border-white/10 bg-white/[.035] p-4">
  <div className="flex items-center justify-between"><span className="text-sm font-bold text-blue-300">Câu {number}</span><button type="button" onClick={onRemove} className="inline-flex items-center gap-1 text-xs text-red-300"><Trash2 size={13}/> Xóa câu</button></div>
  <LaTexEditor value={q.question} onChange={html=>onChange({...q,question:html})} placeholder="Nhập nội dung câu hỏi (hỗ trợ LaTeX hoặc HTML)"/>
  {q.type==="multiple_choice"&&<MultipleChoiceFields q={q} onChange={onChange}/>}
  {q.type==="true_false"&&<TrueFalseFields q={q} onChange={onChange}/>}
  {q.type==="short_answer"&&<ShortAnswerFields q={q} onChange={onChange}/>}
  {q.type==="essay"&&<EssayFields q={q} onChange={onChange}/>}
  <textarea value={q.explanation} onChange={e=>onChange({...q,explanation:e.target.value})} placeholder="Lời giải / phản hồi cho người học (không bắt buộc)" rows={2} className={inputCls}/>
</article>}

function MultipleChoiceFields({q,onChange}:{q:MultipleChoiceQuestion;onChange:(q:ExamQuestion)=>void}){return <div className="space-y-2">{q.options.map((option,i)=><div key={i} className="flex items-center gap-2"><button type="button" onClick={()=>onChange({...q,answer:i})} className={`h-9 w-9 shrink-0 rounded-lg text-sm font-bold ${q.answer===i?"bg-emerald-500 text-white":"bg-white/10 text-slate-400"}`}>{LETTERS[i]}</button><input value={option} onChange={e=>{const options=[...q.options];options[i]=e.target.value;onChange({...q,options})}} placeholder={`Phương án ${LETTERS[i]}`} className={inputCls}/></div>)}</div>}
function TrueFalseFields({q,onChange}:{q:TrueFalseQuestion;onChange:(q:ExamQuestion)=>void}){return <div className="space-y-2">{q.statements.map((statement,i)=><div key={i} className="grid gap-2 sm:grid-cols-[32px_minmax(0,1fr)_auto]"><span className="pt-2 text-sm font-bold text-slate-500">{String.fromCharCode(97+i)})</span><input value={statement.text} onChange={e=>{const statements=q.statements.map((s,si)=>si===i?{...s,text:e.target.value}:s);onChange({...q,statements})}} placeholder="Nhập nhận định" className={inputCls}/><button type="button" onClick={()=>{const statements=q.statements.map((s,si)=>si===i?{...s,answer:!s.answer}:s);onChange({...q,statements})}} className={`rounded-xl px-4 py-2 text-xs font-bold ${statement.answer?"bg-emerald-500/15 text-emerald-300":"bg-red-500/15 text-red-300"}`}>{statement.answer?"Đúng":"Sai"}</button></div>)}</div>}
function ShortAnswerFields({q,onChange}:{q:ShortAnswerQuestion;onChange:(q:ExamQuestion)=>void}){return <label className="block text-xs font-bold text-amber-200">Đáp án điền khuyết<input value={q.answer} onChange={e=>onChange({...q,answer:e.target.value})} placeholder="Ví dụ: G54 hoặc 12,5" className={`${inputCls} mt-2`}/></label>}
function EssayFields({q,onChange}:{q:EssayQuestion;onChange:(q:ExamQuestion)=>void}){return <div className="grid gap-3 lg:grid-cols-2"><label className="text-xs font-bold text-violet-200">Đáp án gợi ý<textarea value={q.suggestedAnswer} onChange={e=>onChange({...q,suggestedAnswer:e.target.value})} rows={4} className={`${inputCls} mt-2`}/></label><label className="text-xs font-bold text-violet-200">Hướng dẫn / tiêu chí chấm<textarea value={q.gradingGuide} onChange={e=>onChange({...q,gradingGuide:e.target.value})} rows={4} className={`${inputCls} mt-2`}/></label></div>}
