import Link from "next/link";
import { MANAGED_CLASSES, classGrade } from "@/services/classes";
import type { HomeStats } from "@/components/home/home-stats.server";

// Một hàng chip, đặt ngay dưới mô phỏng — không còn là màn hình đầu.
// Số lớn + nhãn cấp: nhận ra "lớp mình" bằng một con số (nhận diện hơn là đọc chữ), gom THCS / THPT bằng nhãn nhỏ.
const CLASS_COPY: Record<string, { level: string; grade: string; title: string }> = {
  "khtn-9": { level: "THCS", grade: "9", title: "KHTN 9" },
  "lop-10": { level: "THPT", grade: "10", title: "Vật lý 10" },
  "lop-11": { level: "THPT", grade: "11", title: "Vật lý 11" },
  "lop-12": { level: "THPT", grade: "12", title: "Vật lý 12" },
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
    <section className="bg-bg px-6 pb-8 pt-2 lg:px-12">
      <div className="mx-auto max-w-6xl">
        <h2 className="font-display text-xl font-bold text-ink sm:text-2xl">Em học lớp mấy?</h2>
        <p className="mt-1 text-sm text-ink">Bấm vào lớp của em để vào bài học.</p>
        <ul className="mt-4 grid grid-cols-2 gap-3 md:grid-cols-4">
          {MANAGED_CLASSES.map((managed) => {
            const copy = CLASS_COPY[managed.slug] ?? { level: "", grade: classGrade(managed.name) ?? "", title: managed.name };
            const s = statsByGrade.get(classGrade(managed.name));
            return (
              <li key={managed.slug}>
                <Link
                  href={`/lop-hoc/${managed.slug}`}
                  style={{ borderTopColor: managed.color }}
                  className="flex h-full min-h-36 flex-col rounded-2xl border border-line border-t-4 bg-surface-2 p-4 text-ink transition-colors hover:bg-primary-soft"
                >
                  <span className="text-xs font-bold tracking-wide text-ink">{copy.level}</span>
                  <span className="mt-1 flex items-baseline gap-1.5">
                    <span className="text-sm font-semibold">Lớp</span>
                    <span className="font-display text-5xl font-extrabold leading-none">{copy.grade}</span>
                  </span>
                  <span className="mt-2 text-base font-bold">{copy.title}</span>
                  {s && s.lessons > 0 && <span className="mt-auto pt-2 text-sm">{s.chapters} chương · {s.lessons} bài</span>}
                </Link>
              </li>
            );
          })}
        </ul>

        <ul className="mt-4 flex flex-wrap gap-x-6 gap-y-1 text-base font-semibold text-ink">
          <li>
            <Link href="/khoa-hoc" className="inline-flex min-h-11 items-center underline underline-offset-4 hover:text-primary">
              Khoá học đang mở – ghi danh →
            </Link>
          </li>
          <li>
            <Link href="/lop-hoc/cttc" className="inline-flex min-h-11 items-center underline underline-offset-4 hover:text-primary">
              Sinh viên CTTC →
            </Link>
          </li>
        </ul>

        <p className="mt-3 flex flex-wrap items-center gap-x-4 gap-y-2 text-sm text-ink">
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
