import Link from "next/link";
import { ArrowRight } from "lucide-react";
import type { ScheduleCourse } from "@/components/home/teaching-schedule.server";

// Thời khoá biểu trong tuần cho trang chủ. Dữ liệu đọc lúc build (teaching-schedule.server.ts),
// KHÔNG gọi Supabase khi tải trang. Từ md trở lên: lưới ngày × giờ (vị trí/chiều cao lớp tỉ lệ khung giờ);
// điện thoại: danh sách theo ngày, chỉ liệt kê ngày có lớp.
const DAYS = [
  { n: 1, label: "Thứ 2" }, { n: 2, label: "Thứ 3" }, { n: 3, label: "Thứ 4" }, { n: 4, label: "Thứ 5" },
  { n: 5, label: "Thứ 6" }, { n: 6, label: "Thứ 7" }, { n: 7, label: "CN" },
];
const PX_PER_HOUR = 52;
// Mỗi khối lớp (theo className) một màu để phân biệt 12L1 / 11L2 ...
const TONES = [
  "border-cyan-300/40 bg-cyan-400/10 hover:bg-cyan-400/20",
  "border-amber-300/40 bg-amber-400/10 hover:bg-amber-400/20",
  "border-emerald-300/40 bg-emerald-400/10 hover:bg-emerald-400/20",
  "border-violet-300/40 bg-violet-400/10 hover:bg-violet-400/20",
];

// "Vật lí 12L1 — buổi A · Thứ 4 (A4)" → "12L1 · A4" cho ô lưới hẹp.
const shortName = (n: string) => n.replace(/^Vật lí\s*/, "").replace(/\s*—.*?\((\w+)\)/, " · $1");

const mins = (t: string) => {
  const [h, m] = t.split(":").map(Number);
  return h * 60 + m;
};

export default function TeachingSchedule({ courses }: { courses: ScheduleCourse[] | null }) {
  if (!courses || courses.length === 0) return null;

  const toneOf = new Map<string, string>();
  for (const c of courses) if (!toneOf.has(c.className)) toneOf.set(c.className, TONES[toneOf.size % TONES.length]);

  const slots = courses.flatMap((c) => c.slots.map((s) => ({ c, ...s, a: mins(s.start), b: mins(s.end) })));
  // Trục giờ chỉ giữ những giờ có lớp (+1 giờ đệm hai đầu mỗi cụm), bỏ khoảng trống giữa các cụm.
  const used = new Set<number>();
  for (const s of slots) for (let h = Math.floor(s.a / 60); h < Math.ceil(s.b / 60); h++) used.add(h);
  const hours = [...used].sort((x, y) => x - y);
  const rowOf = new Map(hours.map((h, i) => [h, i]));
  const yOf = (m: number) => (rowOf.get(Math.floor(m / 60))! + (m % 60) / 60) * PX_PER_HOUR;
  const yEnd = (m: number) => (rowOf.get(Math.ceil(m / 60) - 1)! + 1 - (Math.ceil(m / 60) * 60 - m) / 60) * PX_PER_HOUR;
  const height = hours.length * PX_PER_HOUR;
  const href = (id: number) => `/khoa-hoc/dang-ky/?id=${id}`;

  return (
    <section id="lich-day" className="scroll-mt-20 border-t border-line px-6 py-16 lg:px-12 lg:py-20">
      <div className="mx-auto max-w-5xl">
        <p className="font-mono text-xs uppercase tracking-widest text-cyan-300">Lịch học</p>
        <h2 className="mt-2 font-display text-2xl font-bold text-ink sm:text-3xl">Thời khoá biểu trong tuần</h2>
        <p className="mt-3 max-w-xl text-sm leading-relaxed text-muted sm:text-base">
          Các lớp Vật lý thầy Thạch đang mở. Bấm vào một buổi để xem chi tiết và đăng ký.
        </p>

        {/* Điện thoại: danh sách theo ngày */}
        <ul className="mt-8 space-y-3 md:hidden">
          {DAYS.map((d) => {
            const day = slots.filter((s) => s.weekday === d.n).sort((x, y) => x.a - y.a);
            if (day.length === 0) return null;
            return (
              <li key={d.n} className="rounded-xl border border-line p-3">
                <p className="font-mono text-xs font-semibold uppercase tracking-wide text-cyan-300">{d.label}</p>
                <ul className="mt-2 space-y-2">
                  {day.map((s) => (
                    <li key={`${s.c.id}-${s.start}`}>
                      <Link
                        href={href(s.c.id)}
                        className={`flex items-center justify-between gap-3 rounded-lg border px-3 py-2 transition ${toneOf.get(s.c.className)}`}
                      >
                        <span className="min-w-0">
                          <span className="block truncate text-sm font-semibold text-ink">Vật lí {shortName(s.c.name)}</span>
                          {s.location && <span className="block truncate text-xs text-muted">{s.location}</span>}
                        </span>
                        <span className="shrink-0 text-sm tabular-nums text-ink">{s.start}–{s.end}</span>
                      </Link>
                    </li>
                  ))}
                </ul>
              </li>
            );
          })}
        </ul>

        {/* Máy tính bảng / máy tính: lưới ngày × giờ */}
        <div className="mt-8 hidden overflow-hidden rounded-2xl border border-line md:block">
          <div className="grid" style={{ gridTemplateColumns: "48px repeat(7, 1fr)" }}>
            <div className="border-b border-line bg-panel" />
            {DAYS.map((d) => (
              <div key={d.n} className="border-b border-l border-line bg-panel py-2 text-center font-mono text-xs font-semibold uppercase tracking-wide text-cyan-300">
                {d.label}
              </div>
            ))}
            <div className="relative border-r border-line" style={{ height }}>
              {hours.map((h) => (
                <span key={h} className="absolute right-1.5 -translate-y-1/2 text-[11px] tabular-nums text-muted" style={{ top: rowOf.get(h)! * PX_PER_HOUR }}>
                  {h}g
                </span>
              ))}
            </div>
            {DAYS.map((d) => (
              <div key={d.n} className="relative border-l border-line" style={{ height }}>
                {hours.map((h) => (
                  <div key={h} className="absolute inset-x-0 border-t border-line/50" style={{ top: rowOf.get(h)! * PX_PER_HOUR }} />
                ))}
                {slots.filter((s) => s.weekday === d.n).map((s) => (
                  <Link
                    key={`${s.c.id}-${s.start}`}
                    href={href(s.c.id)}
                    className={`absolute inset-x-1 overflow-hidden rounded-lg border px-1.5 py-1 text-[11px] leading-tight transition ${toneOf.get(s.c.className)}`}
                    style={{ top: yOf(s.a), height: Math.max(yEnd(s.b) - yOf(s.a), 36) }}
                  >
                    <span className="block truncate font-semibold text-ink">{shortName(s.c.name)}</span>
                    <span className="block tabular-nums text-muted">{s.start}–{s.end}</span>
                  </Link>
                ))}
              </div>
            ))}
          </div>
        </div>

        <Link href="/khoa-hoc" className="mt-6 inline-flex items-center gap-1.5 text-sm font-semibold text-cyan-300 transition hover:text-cyan-200">
          Xem đầy đủ các lớp và đăng ký học <ArrowRight size={16} />
        </Link>
      </div>
    </section>
  );
}
