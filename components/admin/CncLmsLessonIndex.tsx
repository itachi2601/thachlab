import Link from "next/link";
import { BookOpen, ChevronRight, FileQuestion, FileText, GraduationCap, Layers3, MonitorPlay, Settings2, ShieldCheck, Video } from "lucide-react";
import { CNC_COURSE_ITEMS } from "@/services/cnc-lms";

const learningItems = CNC_COURSE_ITEMS.filter((item) => item.id !== "intro");

export default function CncLmsLessonIndex() {
  return <div className="space-y-6">
    <section className="overflow-hidden rounded-3xl border border-blue-400/20 bg-[radial-gradient(circle_at_90%_0%,rgba(37,99,235,.22),transparent_35%),#0B1020] p-6 sm:p-8">
      <div className="flex flex-col gap-6 xl:flex-row xl:items-end xl:justify-between">
        <div className="max-w-3xl">
          <span className="inline-flex items-center gap-2 rounded-full border border-blue-400/20 bg-blue-500/10 px-3 py-1 text-xs font-bold uppercase tracking-wider text-blue-200"><Settings2 size={14}/> Trung tâm nội dung CNC</span>
          <h1 className="mt-4 font-display text-3xl font-bold text-white sm:text-4xl">Quản trị học phần Gia công CNC</h1>
          <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-400">Mỗi bài học có một trang soạn riêng. Chọn bài bên dưới để quản lý nội dung, video, học liệu, bài nộp và ngân hàng câu hỏi.</p>
        </div>
        <div className="grid grid-cols-3 gap-2 sm:min-w-[390px]">
          <Stat icon={<BookOpen size={17}/>} value={`${learningItems.length}`} label="Bài học"/>
          <Stat icon={<Layers3 size={17}/>} value="5" label="Nhóm nội dung"/>
          <Stat icon={<ShieldCheck size={17}/>} value="2" label="Cổng an toàn"/>
        </div>
      </div>
    </section>

    <section className="grid gap-4 lg:grid-cols-[minmax(0,1fr)_280px]">
      <div className="space-y-3">
        <div className="flex items-end justify-between gap-4 px-1"><div><p className="text-xs font-bold uppercase tracking-wider text-blue-300">Chương trình học</p><h2 className="mt-1 font-display text-xl font-semibold text-white">Danh sách bài học</h2></div><span className="text-xs text-slate-500">{learningItems.length} bài · 70 tiết</span></div>
        {learningItems.map((item,index)=><Link key={item.id} href={`/quan-tri/lms-cnc/${item.id}`} className="group grid gap-4 rounded-2xl border border-white/10 bg-[#0B1020] p-4 transition hover:-translate-y-0.5 hover:border-blue-400/40 hover:bg-[#10182b] sm:grid-cols-[56px_minmax(0,1fr)_auto] sm:items-center">
          <span className="flex h-14 w-14 items-center justify-center rounded-2xl border border-blue-400/15 bg-blue-500/10 font-display text-lg font-black text-blue-300">{String(index+1).padStart(2,"0")}</span>
          <span className="min-w-0"><span className="block text-xs font-bold uppercase tracking-wider text-blue-300">Bài {index+1} · {item.duration}</span><strong className="mt-1 block font-display text-base text-white group-hover:text-blue-200">{item.title.replace(/^Bài \d+: /,"")}</strong><span className="mt-2 flex flex-wrap gap-x-4 gap-y-1 text-xs text-slate-500"><span className="inline-flex items-center gap-1"><GraduationCap size={13}/> Chuẩn đầu ra</span><span className="inline-flex items-center gap-1"><Video size={13}/> Video</span><span className="inline-flex items-center gap-1"><FileText size={13}/> Học liệu</span><span className="inline-flex items-center gap-1"><FileQuestion size={13}/> Kiểm tra</span></span></span>
          <span className="inline-flex items-center justify-end gap-1 text-sm font-bold text-blue-300">Mở trang soạn <ChevronRight size={18} className="transition-transform group-hover:translate-x-1"/></span>
        </Link>)}
      </div>
      <aside className="space-y-4 lg:sticky lg:top-28 lg:self-start">
        <Link href="/quan-tri/lms-cnc/intro" className="group block rounded-2xl border border-emerald-400/20 bg-emerald-500/[0.07] p-5 hover:border-emerald-400/40"><span className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-500/15 text-emerald-300"><MonitorPlay size={19}/></span><strong className="mt-4 block font-display text-white">Trang giới thiệu học phần</strong><p className="mt-2 text-xs leading-5 text-slate-400">Chỉnh mô tả chung, tài nguyên nhập môn và hoạt động mở đầu.</p><span className="mt-4 inline-flex items-center gap-1 text-xs font-bold text-emerald-300">Mở trang soạn <ChevronRight size={15}/></span></Link>
        <div className="rounded-2xl border border-amber-400/20 bg-amber-500/[0.06] p-5"><span className="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-500/15 text-amber-200"><ShieldCheck size={19}/></span><strong className="mt-4 block font-display text-white">Luồng mở khóa</strong><ol className="mt-3 space-y-3 text-xs leading-5 text-slate-400"><li><b className="text-amber-100">1.</b> Bài 2 và 3 đạt từ 80%</li><li><b className="text-amber-100">2.</b> Mở bài vận hành tiện/phay</li><li><b className="text-amber-100">3.</b> Đạt vận hành để mở bài gia công</li></ol></div>
      </aside>
    </section>
  </div>;
}

function Stat({icon,value,label}:{icon:React.ReactNode;value:string;label:string}){return <div className="rounded-2xl border border-white/10 bg-black/15 p-3 text-center"><span className="mx-auto flex w-fit text-blue-300">{icon}</span><strong className="mt-2 block text-xl text-white">{value}</strong><small className="text-[10px] font-bold uppercase tracking-wider text-slate-500">{label}</small></div>}
