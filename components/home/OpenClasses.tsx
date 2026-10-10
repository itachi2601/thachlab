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
    <section className="bg-bg px-6 pb-8 pt-2 lg:px-12">
      <div className="mx-auto max-w-6xl">
        <h2 className="font-display text-xl font-bold text-ink sm:text-2xl">Chọn lớp để bắt đầu</h2>
        <ul className="mt-4 flex gap-3 overflow-x-auto pb-2">
          {MANAGED_CLASSES.map((managed) => {
            const copy = CLASS_COPY[managed.slug] ?? { title: managed.name };
            const s = statsByGrade.get(classGrade(managed.name));
            const detail = s ? `${s.chapters} chương · ${s.lessons} bài` : undefined;
            return (
              <li key={managed.slug} className="shrink-0">
                <Link
                  href={`/lop-hoc/${managed.slug}`}
                  style={{ borderColor: `${managed.color}99`, boxShadow: `inset 3px 0 0 ${managed.color}` }}
                  className="flex min-h-14 min-w-36 flex-col justify-center rounded-xl border bg-surface-2 py-2 pl-5 pr-5 text-ink transition-colors hover:bg-primary-soft"
                >
                  <span className="text-base font-bold">{copy.title}</span>
                  {detail && <span className="text-sm text-ink">{detail}</span>}
                </Link>
              </li>
            );
          })}
        </ul>

        <div className="mt-3 grid grid-cols-1 gap-3 sm:grid-cols-2 sm:max-w-xl">
          <Link
            href="/lop-hoc/cttc"
            style={{ borderColor: "#fbbf2499", boxShadow: "inset 3px 0 0 #fbbf24" }}
            className="flex min-h-14 flex-col justify-center rounded-xl border bg-surface-2 py-2 pl-5 pr-5 text-ink transition-colors hover:bg-primary-soft"
          >
            <span className="text-base font-bold">Sinh viên CTTC</span>
            <span className="text-sm text-ink">Vào lớp học phần của em</span>
          </Link>
          <Link
            href="/khoa-hoc"
            style={{ borderColor: "#67e8f999", boxShadow: "inset 3px 0 0 #67e8f9" }}
            className="flex min-h-14 flex-col justify-center rounded-xl border bg-surface-2 py-2 pl-5 pr-5 text-ink transition-colors hover:bg-primary-soft"
          >
            <span className="text-base font-bold">Khoá học đang mở</span>
            <span className="text-sm text-ink">Xem và ghi danh</span>
          </Link>
        </div>

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
