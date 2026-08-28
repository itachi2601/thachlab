import Link from "next/link";
import { BookOpen, ChevronRight, Clock3, FileText, Video } from "lucide-react";
import { CNC_COURSE_ITEMS } from "@/services/cnc-lms";

export default function CncLmsLessonIndex() {
  return (
    <div className="space-y-6">
      <section className="rounded-2xl border border-white/10 bg-[#0B1020] p-5">
        <h2 className="font-display text-lg font-semibold text-white">Quản lý bài học Gia công CNC</h2>
        <p className="mt-2 text-sm leading-6 text-slate-400">
          Chọn một bài để mở trang soạn riêng. Các bài kiểm tra, video, tệp học liệu, checklist và nội dung hiện có được giữ nguyên.
        </p>
      </section>

      <section className="space-y-3">
        {CNC_COURSE_ITEMS.map((item, index) => (
          <Link
            key={item.id}
            href={`/quan-tri/lms-cnc/${item.id}`}
            className="group flex items-center gap-4 rounded-2xl border border-white/10 bg-[#0B1020] p-4 transition hover:border-primary/50 hover:bg-white/[0.07]"
          >
            <span className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-primary/15 font-display font-bold text-[#60A5FA]">
              {item.id === "intro" ? "MĐ" : index}
            </span>
            <span className="min-w-0 flex-1">
              <strong className="block font-display text-white group-hover:text-primary">{item.shortTitle}</strong>
              <span className="mt-1 block text-sm text-slate-400">{item.title}</span>
              <span className="mt-2 flex flex-wrap gap-3 text-xs text-slate-500">
                <span className="inline-flex items-center gap-1"><Clock3 size={13} />{item.duration}</span>
                <span className="inline-flex items-center gap-1"><BookOpen size={13} />Nội dung</span>
                <span className="inline-flex items-center gap-1"><Video size={13} />Video</span>
                <span className="inline-flex items-center gap-1"><FileText size={13} />Học liệu</span>
              </span>
            </span>
            <span className="inline-flex shrink-0 items-center gap-1 text-sm font-semibold text-[#60A5FA]">
              Soạn bài <ChevronRight size={17} />
            </span>
          </Link>
        ))}
      </section>
    </div>
  );
}
