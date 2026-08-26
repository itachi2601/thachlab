import Link from "next/link";
import { ArrowRight, GraduationCap, Wrench } from "lucide-react";

export default function AudienceChooser() {
  return (
    <section className="relative overflow-hidden bg-[#05070B] px-6 pt-28 pb-2 sm:pt-32 lg:px-12">
      <div className="relative mx-auto max-w-4xl text-center">
        <p className="text-xs font-bold uppercase tracking-[.2em] text-slate-500">ThachLab</p>
        <h2 className="mt-2 font-display text-xl font-bold text-white sm:text-2xl">Bạn đang học ở đâu?</h2>
      </div>
      <div className="relative mx-auto mt-6 grid max-w-4xl gap-4 sm:grid-cols-2">
        <a
          href="#thpt"
          className="group flex items-center gap-4 rounded-2xl border border-blue-400/20 bg-blue-500/[0.06] p-5 transition hover:border-blue-400/40 hover:bg-blue-500/10"
        >
          <span className="grid h-12 w-12 shrink-0 place-items-center rounded-xl bg-blue-500/15 text-blue-300">
            <GraduationCap size={24} />
          </span>
          <div className="flex-1">
            <strong className="block text-white">Học sinh THPT</strong>
            <span className="text-sm text-slate-400">Vật lý lớp 9–12 theo chương trình GDPT 2018</span>
          </div>
          <ArrowRight size={18} className="shrink-0 text-blue-300 opacity-0 transition group-hover:opacity-100" />
        </a>
        <Link
          href="/lop-hoc?tab=cttc"
          className="group flex items-center gap-4 rounded-2xl border border-orange-400/20 bg-orange-500/[0.06] p-5 transition hover:border-orange-400/40 hover:bg-orange-500/10"
        >
          <span className="grid h-12 w-12 shrink-0 place-items-center rounded-xl bg-orange-500/15 text-orange-300">
            <Wrench size={24} />
          </span>
          <div className="flex-1">
            <strong className="block text-white">Sinh viên CTTC</strong>
            <span className="text-sm text-slate-400">Gia công CNC, Tiện – Phay truyền thống</span>
          </div>
          <ArrowRight size={18} className="shrink-0 text-orange-300 opacity-0 transition group-hover:opacity-100" />
        </Link>
      </div>
    </section>
  );
}
