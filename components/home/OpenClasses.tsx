import Link from "next/link";
import { ArrowRight, Wrench } from "lucide-react";
import { MANAGED_CLASSES, classGrade } from "@/services/classes";
import type { HomeStats } from "@/components/home/home-stats.server";

// Thay AudienceChooser (2 thẻ THPT / CTTC): hiện thẳng 4 lớp đang mở kèm số chương · bài · mục
// (số đọc lúc build từ home-stats.json, không gọi Supabase), CTTC giữ 1 dòng riêng bên dưới.
const CLASS_COPY: Record<string, { title: string; desc: string }> = {
  "khtn-9": { title: "KHTN 9", desc: "Nền tảng KHTN, định hướng thi chuyên" },
  "lop-10": { title: "Vật lý 10", desc: "Nhập môn và nền tảng cơ học" },
  "lop-11": { title: "Vật lý 11", desc: "Dao động, sóng và điện" },
  "lop-12": { title: "Vật lý 12", desc: "Nhiệt, khí và vật lý hiện đại" },
};

function formatCount(n: number) {
  return n.toLocaleString("vi-VN");
}

// Số nhỏ hơn ngưỡng này thì KHÔNG hiện: "37 học sinh" hay "12 lượt làm đề" làm phụ huynh
// đánh giá thấp mức độ dùng thật, phản tác dụng. Không đủ dữ liệu (null) cũng ẩn.
const MIN_STAT_TO_SHOW = 50;

function showStat(n: number | null | undefined): number | null {
  return typeof n === "number" && n >= MIN_STAT_TO_SHOW ? n : null;
}

export default function OpenClasses({ stats }: { stats: HomeStats | null }) {
  const statsByGrade = new Map<string | null, HomeStats["classes"][number]>();
  for (const c of stats?.classes ?? []) statsByGrade.set(classGrade(c.name), c);
  const students = showStat(stats?.totals.students);
  const attempts = showStat(stats?.totals.attempts);

  return (
    <section className="bg-[#05070B] px-6 pb-8 pt-24 sm:pb-10 sm:pt-28 lg:px-12">
      <div className="mx-auto max-w-4xl">
        <p className="font-mono text-xs uppercase tracking-widest text-cyan-300">Bắt đầu từ đây</p>
        <h2 className="mt-2 font-display text-xl font-bold text-ink sm:text-2xl">Em đang học ở đâu?</h2>

        <ul className="mt-5 grid grid-cols-2 gap-3 lg:grid-cols-4">
          {MANAGED_CLASSES.map((managed) => {
            const copy = CLASS_COPY[managed.slug] ?? { title: managed.name, desc: "" };
            const s = statsByGrade.get(classGrade(managed.name));
            return (
              <li key={managed.slug}>
                <Link
                  href={`/lop-hoc/${managed.slug}`}
                  className="group relative flex h-full flex-col gap-2 rounded-xl border border-line p-4 pl-5 transition-colors hover:bg-white/[0.04] sm:p-5 sm:pl-6"
                >
                  <span
                    aria-hidden
                    className="absolute left-0 top-4 bottom-4 w-0.5 rounded-full sm:top-5 sm:bottom-5"
                    style={{ backgroundColor: managed.color }}
                  />
                  <span className="flex items-center justify-between gap-2">
                    <strong className="font-display text-base text-ink sm:text-lg">{copy.title}</strong>
                    <ArrowRight
                      size={16}
                      className="shrink-0 text-muted transition group-hover:translate-x-0.5 group-hover:text-cyan-300"
                    />
                  </span>
                  <span className="text-sm leading-snug text-muted">{copy.desc}</span>
                  {s && (
                    <span className="mt-auto pt-1 font-mono text-[11px] text-muted sm:text-xs">
                      {s.chapters} chương · {s.lessons} bài · {s.items} mục
                    </span>
                  )}
                </Link>
              </li>
            );
          })}
        </ul>

        <Link
          href="/lop-hoc/cttc"
          className="group mt-3 flex items-center gap-4 rounded-xl border border-line p-4 transition-colors hover:bg-white/[0.04] sm:p-5"
        >
          <span className="grid h-10 w-10 shrink-0 place-items-center rounded-lg bg-amber-400/10 text-amber-300">
            <Wrench size={20} />
          </span>
          <span className="min-w-0 flex-1">
            <strong className="block text-ink">Sinh viên CTTC</strong>
            <span className="text-sm text-muted">Gia công CNC, Tiện – Phay truyền thống</span>
          </span>
          <ArrowRight
            size={18}
            className="shrink-0 text-muted transition group-hover:translate-x-0.5 group-hover:text-cyan-300"
          />
        </Link>

        {stats && (
          <p className="mt-5 flex flex-wrap items-center gap-x-5 gap-y-1 font-mono text-xs text-muted">
            <span>
              <strong className="font-semibold text-ink">{formatCount(stats.totals.classes)}</strong> lớp
            </span>
            <span>
              <strong className="font-semibold text-ink">{formatCount(stats.totals.chapters)}</strong> chương
            </span>
            <span>
              <strong className="font-semibold text-ink">{formatCount(stats.totals.lessons)}</strong> bài giảng
            </span>
            <span>
              <strong className="font-semibold text-ink">{formatCount(stats.totals.items)}</strong> mục học
            </span>
            {students !== null && (
              <span>
                <strong className="font-semibold text-ink">{formatCount(students)}</strong> học sinh
              </span>
            )}
            {attempts !== null && (
              <span>
                <strong className="font-semibold text-ink">{formatCount(attempts)}</strong> lượt làm đề đã chấm
              </span>
            )}
            <Link href="/khoa-hoc" className="ml-auto font-sans text-sm font-medium text-cyan-300 hover:underline">
              Khoá học đang mở →
            </Link>
          </p>
        )}
      </div>
    </section>
  );
}
