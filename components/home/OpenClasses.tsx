import Link from "next/link";
import { MANAGED_CLASSES, classGrade } from "@/services/classes";
import type { HomeStats } from "@/components/home/home-stats.server";

// Một hàng chip, đặt ngay dưới mô phỏng — không còn là màn hình đầu.
const CLASS_COPY: Record<string, { title: string }> = {
  "khtn-9": { title: "KHTN 9" },
  "lop-10": { title: "Vật lý 10" },
  "lop-11": { title: "Vật lý 11" },
  "lop-12": { title: "Vật lý 12" },
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
    <section className="bg-[#05070B] px-6 pb-8 pt-2 lg:px-12">
      <div className="mx-auto max-w-6xl">
        <h2 className="font-display text-lg font-bold text-ink">Chọn lớp</h2>
        <ul className="mt-3 flex gap-2 overflow-x-auto pb-1">
          {MANAGED_CLASSES.map((managed) => {
            const copy = CLASS_COPY[managed.slug] ?? { title: managed.name };
            const s = statsByGrade.get(classGrade(managed.name));
            const detail = s ? `${s.chapters} chương · ${s.lessons} bài` : undefined;
            return (
              <li key={managed.slug} className="shrink-0">
                <Link
                  href={`/lop-hoc/${managed.slug}`}
                  title={detail}
                  className="inline-flex min-h-11 items-center gap-2 rounded-full border border-line px-4 text-sm font-semibold text-ink transition-colors hover:bg-white/[0.04]"
                >
                  <span
                    aria-hidden
                    className="h-2 w-2 shrink-0 rounded-full"
                    style={{ backgroundColor: managed.color }}
                  />
                  {copy.title}
                </Link>
              </li>
            );
          })}
        </ul>

        <p className="mt-3 flex flex-wrap items-center gap-x-4 gap-y-2 text-sm text-muted">
          <Link href="/lop-hoc/cttc" className="inline-flex min-h-11 items-center font-medium text-ink hover:underline">
            Sinh viên CTTC
          </Link>
          <Link href="/khoa-hoc" className="inline-flex min-h-11 items-center font-medium text-cyan-300 hover:underline">
            Khoá học đang mở
          </Link>
          {stats && (
            <span className="inline-flex min-h-11 flex-wrap items-center gap-x-3">
              <span>{formatCount(stats.totals.lessons)} bài giảng</span>
              {students !== null && <span>{formatCount(students)} học sinh</span>}
              {attempts !== null && <span>{formatCount(attempts)} lượt làm đề</span>}
            </span>
          )}
        </p>
      </div>
    </section>
  );
}
