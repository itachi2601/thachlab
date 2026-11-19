"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { Activity, BarChart3, BookOpen, ChevronRight, Dumbbell, Moon, Play, Ruler, Salad } from "lucide-react";
import { MODULES } from "@/lib/suc-khoe/modules";
import { TARGET, programFor } from "@/lib/tap-luyen/chuong-trinh";
import { fetchMeasurements, fetchWorkouts, setTapLuyenUser, weekPlan, type Measurement, type Workout } from "@/lib/tap-luyen/store";
import { useAuth } from "@/components/auth/AuthProvider";
import { fmtDay, vn } from "@/components/tap-luyen/ui";

const ICON: Record<string, React.ReactNode> = {
  "tap-luyen": <Dumbbell size={20} />,
  "so-do": <Ruler size={20} />,
  "tien-bo": <BarChart3 size={20} />,
  "dinh-duong": <Salad size={20} />,
  "ngu-hoi-phuc": <Moon size={20} />,
  "bai-hoc": <BookOpen size={20} />,
};

export default function SucKhoeHub() {
  const { profile } = useAuth();
  const program = programFor(profile?.role);
  const staff = program.kind === "thay";
  if (profile?.id) setTapLuyenUser(profile.id, staff);
  const ROUTINES = program.routines;
  const modules = staff ? MODULES : MODULES.filter((m) => m.forStudents && m.status === "dang-dung"); // N3: học sinh không thấy mục chưa dùng được
  const [history, setHistory] = useState<Workout[] | null>(null);
  const [meas, setMeas] = useState<Measurement[]>([]);
  const [now] = useState(() => Date.now());

  useEffect(() => {
    fetchWorkouts().then((r) => setHistory(r.list));
    if (staff) fetchMeasurements().then((r) => setMeas(r.list));
  }, [staff]);

  const plan = weekPlan(history ?? [], ROUTINES.map((r) => r.key));
  const nextR = ROUTINES.find((r) => r.key === plan.next);
  const lastW = history?.[0];
  const latest = meas[meas.length - 1];
  const days = latest ? Math.floor((now - new Date(`${latest.measured_on}T00:00:00`).getTime()) / 864e5) : null;
  const chestWaist = latest?.chest_cm && latest?.waist_cm ? latest.chest_cm / latest.waist_cm : TARGET.start.chest / TARGET.start.waist;

  return (
    <div className="space-y-4">
      {/* Hôm nay: một việc chính + hai con số theo dõi */}
      <section className="rounded-2xl border border-line bg-panel p-4">
        <p className="flex items-center gap-1.5 text-sm font-semibold text-muted"><Activity size={16} /> Hôm nay</p>
        {history === null ? (
          <p className="mt-2 h-14 animate-pulse rounded-xl bg-surface-2" aria-label="Đang tải" />
        ) : nextR ? (
          <>
            <p className="mt-1 text-lg font-bold text-ink">Buổi tập tiếp theo: {nextR.name}</p>
            <p className="text-sm text-muted">
              {nextR.items.length} bài · {nextR.items.reduce((a, i) => a + i.sets, 0)} hiệp · {program.minutes}
              {lastW && <> · buổi gần nhất {fmtDay(lastW.started_at)}</>}
            </p>
            <Link href={`/suc-khoe/tap-luyen?buoi=${nextR.key}`} className="mt-3 flex min-h-12 items-center justify-center gap-2 rounded-xl bg-primary text-sm font-bold text-white">
              <Play size={16} /> Bắt đầu buổi {nextR.key}
            </Link>
          </>
        ) : (
          <>
            <p className="mt-1 text-lg font-bold text-ink">Tuần này đã đủ {ROUTINES.length} buổi 🎉</p>
            <p className="text-sm text-muted">
              {staff ? "Nghỉ ngơi, trượt băng nhẹ. Tuần sau bắt đầu lại từ buổi A." : "Những ngày còn lại: đi bộ, đạp xe, chơi thể thao cùng bạn. Tuần sau bắt đầu lại từ buổi 1."}
            </p>
          </>
        )}
        {!staff && (
          <p className="mt-3 text-sm text-muted">Tuần này: <b className="tabular-nums text-ink">{plan.count}/{ROUTINES.length}</b> buổi</p>
        )}
        {staff && <dl className="mt-3 grid grid-cols-3 gap-2 text-center">
          <div className="rounded-xl bg-surface-2 px-1 py-2">
            <dt className="text-xs text-muted">Tuần này</dt>
            <dd className="text-lg font-bold tabular-nums text-ink">{plan.count}/3</dd>
          </div>
          <div className="rounded-xl bg-surface-2 px-1 py-2">
            <dt className="text-xs text-muted">Ngực / eo</dt>
            <dd className={`text-lg font-bold tabular-nums ${chestWaist >= 1.2 ? "text-ok" : "text-warn"}`}>{vn(chestWaist, 2)}</dd>
          </div>
          <div className="rounded-xl bg-surface-2 px-1 py-2">
            <dt className="text-xs text-muted">Đo lại</dt>
            <dd className={`text-lg font-bold tabular-nums ${days != null && days >= TARGET.remeasureDays ? "text-warn" : "text-ink"}`}>
              {days == null ? "Chưa đo" : days >= TARGET.remeasureDays ? "Hôm nay" : `${TARGET.remeasureDays - days} ngày`}
            </dd>
          </div>
        </dl>}
      </section>

      <section aria-labelledby="sk-muc">
        <h2 id="sk-muc" className="mb-2 text-sm font-bold uppercase tracking-wide text-muted">Các mục</h2>
        <ul className="grid gap-2 sm:grid-cols-2">
          {modules.map((m) => {
            const inner = (
              <>
                <span className={`grid h-11 w-11 shrink-0 place-items-center rounded-xl ${m.status === "dang-dung" ? "bg-primary-soft text-primary" : "bg-surface-2 text-muted"}`}>{ICON[m.key]}</span>
                <span className="min-w-0 flex-1">
                  <span className="flex items-center gap-2">
                    <span className="font-bold text-ink">{m.title}</span>
                    {m.status === "sap-co" && <span className="rounded-full bg-surface-2 px-2 py-0.5 text-[11px] font-semibold text-muted">Sắp có</span>}
                  </span>
                  <span className="mt-0.5 block text-sm leading-snug text-muted">{staff ? m.desc : (m.descHs ?? m.desc)}</span>
                </span>
                {m.href && <ChevronRight size={18} className="shrink-0 text-muted" />}
              </>
            );
            const cls = "flex min-h-20 items-center gap-3 rounded-2xl border border-line bg-panel p-3";
            return (
              <li key={m.key}>
                {m.href ? <Link href={m.href} className={`${cls} hover:border-primary/50`}>{inner}</Link> : <div className={`${cls} opacity-80`}>{inner}</div>}
              </li>
            );
          })}
        </ul>
      </section>

      {staff && <details className="rounded-2xl border border-dashed border-line-strong bg-panel p-4">
        <summary className="cursor-pointer text-sm font-bold text-ink">Lộ trình thành môn học cho học sinh</summary>
        <ol className="mt-2 list-decimal space-y-1.5 pl-5 text-sm text-ink">
          <li><b>Thầy dùng thử</b> — xong. Từ 19/11/2026 học sinh, sinh viên đã vào được Tập luyện + Tiến bộ với chương trình không dụng cụ.</li>
          <li><b>Soạn phần Bài học</b>: mỗi bài ngắn, có thử ngay (khởi động, đo nhịp tim, tính năng lượng bữa ăn).</li>
          <li><b>Chỉnh cho tuổi 14–18</b> — đã làm: học sinh tập theo số lần/số giây, không thấy số cân/vòng đo, không bảng xếp hạng.</li>
          <li><b>Mở cho một lớp thử</b>, xem bao nhiêu em quay lại tuần thứ 2–3, rồi mới mở rộng.</li>
        </ol>
      </details>}
    </div>
  );
}
