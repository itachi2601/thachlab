"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { ArrowUpCircle, Flame, TrendingUp } from "lucide-react";
import Avatar from "@/components/ui/Avatar";
import RankAvatarFrame from "@/components/rank/RankAvatarFrame";
import WornTitle from "@/components/rank/WornTitle";
import { divisionLabel, tierMeta, type PublicHonorBoard, type PublicHonorGrade } from "@/features/rank/types";
import { fetchPublicHonor } from "@/services/rank";

/** Mục "Vinh danh tuần" trên trang chủ công khai — chỉ render khi RPC trả về ít nhất một khối có dữ liệu. */
export default function HonorBoardPanel() {
  const [board, setBoard] = useState<PublicHonorBoard | null | undefined>(undefined);
  const [grade, setGrade] = useState<string | null>(null);

  useEffect(() => {
    fetchPublicHonor().then(setBoard).catch(() => setBoard(null));
  }, []);

  const grades = useMemo(
    () => (board?.grades ?? []).filter((g) => g.top.length > 0 || g.tier_ups.length > 0 || g.streak),
    [board],
  );
  // Mặc định mở khối lớn nhất có bục (thường là khối đông và sôi nổi nhất).
  const active = grades.find((g) => g.grade === grade) ?? [...grades].reverse().find((g) => g.top.length > 0) ?? grades[0];

  if (!board || grades.length === 0 || !active) return null;

  return (
    <section id="vinh-danh" className="scroll-mt-20 border-t border-line py-20 lg:py-28">
      <div className="mx-auto max-w-6xl px-6 lg:px-8">
        <div className="flex flex-wrap items-end justify-between gap-4">
          <div className="max-w-2xl">
            <p className="font-mono text-xs uppercase tracking-widest text-primary">
              Vinh danh tuần · {weekLabel(board.week_start, active.use_prev)}
            </p>
            <h2 className="mt-3 font-display text-3xl font-bold tracking-tight text-ink sm:text-4xl">
              Các bạn học chăm nhất tuần này
            </h2>
            <p className="mt-4 text-base leading-relaxed text-muted">
              Xếp theo RP kiếm được trong tuần, làm mới sáng Thứ Hai — tuần nào cũng là một cuộc đua mới.
            </p>
          </div>
          <div className="flex gap-2" role="tablist" aria-label="Chọn khối">
            {grades.map((g) => {
              const on = g.grade === active.grade;
              return (
                <button
                  key={g.grade}
                  role="tab"
                  aria-selected={on}
                  onClick={() => setGrade(g.grade)}
                  className={`rounded-full border px-4 py-1.5 text-sm font-medium transition ${
                    on ? "border-primary bg-primary text-white" : "border-line text-muted hover:border-line-strong hover:text-ink"
                  }`}
                >
                  Khối {g.grade}
                </button>
              );
            })}
          </div>
        </div>

        <Podium key={active.grade} g={active} />

        {board.me && <MyWeek me={board.me} />}

        <p className="mt-8 text-xs text-slate-500">
          Tên hiện rút gọn theo lựa chọn của từng bạn. Học sinh đổi cách hiện (đầy đủ, rút gọn hoặc ẩn) trong{" "}
          <Link href="/tai-khoan/" className="text-primary underline-offset-4 hover:underline">
            trang tài khoản
          </Link>
          .
        </p>
      </div>
    </section>
  );
}

function Podium({ g }: { g: PublicHonorGrade }) {
  // Desktop: hạng 1 đứng giữa (2 · 1 · 3); mobile: danh sách 1 · 2 · 3 theo thứ tự tự nhiên.
  const ORDER = ["sm:order-2", "sm:order-1", "sm:order-3"];
  // "Tiến bộ nhất" đứng ngay dưới bục: em làm ít mà làm tốt hơn trước cũng được ghi nhận (thầy chốt 15/10/2026).
  const improved = g.improved_acc
    ? {
        name: g.improved_acc.name,
        avatar: g.improved_acc.avatar,
        detail: `Tỉ lệ làm đúng tăng ${String(g.improved_acc.gain).replace(".", ",")}% so với 2 tuần trước`,
      }
    : g.improved && { name: g.improved.name, avatar: g.improved.avatar, detail: `+${g.improved.delta} RP so với tuần trước` };
  // Lên bậc: ai đứng trên bục thì gắn nhãn ngay trên thẻ (không lặp tên ở dòng dưới — N4); chỉ người ngoài bục mới ghi riêng.
  const tierLabel = (t: { tier_code: PublicHonorGrade["tier_ups"][number]["tier_code"]; division: number | null }) =>
    `${tierMeta(t.tier_code).name} ${divisionLabel(t.division)}`.trim();
  const upByName = new Map(g.tier_ups.map((t) => [t.name, t]));
  const onPodium = new Set(g.top.map((m) => m.name));
  const upsOff = g.tier_ups.filter((t) => !onPodium.has(t.name));

  return (
    <>
      {g.top.length === 0 ? (
        <p className="mt-10 rounded-2xl border border-dashed border-line p-6 text-sm text-muted">
          Khối {g.grade} chưa có bạn nào nhận RP tuần này. Bài luyện tập đầu tiên sẽ đưa em lên bục.
        </p>
      ) : (
        <ul className="mt-10 grid gap-3 sm:grid-cols-3 sm:items-end">
          {g.top.map((m, i) => {
            const first = m.pos === 1;
            const meta = tierMeta(m.tier_code, m.paragon);
            const up = upByName.get(m.name);
            return (
              <li
                key={`${m.name}-${i}`}
                // Hạng 1 là điểm nổi duy nhất của mục (B2): cao hơn rõ trên desktop + một sắc ấm duy nhất (token accent, M3).
                className={`flex items-center gap-4 rounded-2xl border p-4 sm:flex-col sm:text-center ${ORDER[i] ?? "sm:order-4"} ${
                  first ? "border-accent/60 bg-[color-mix(in_srgb,var(--color-accent)_7%,var(--color-panel))] sm:pb-8 sm:pt-10" : "border-line bg-panel"
                }`}
              >
                <div className="flex shrink-0 flex-col items-center gap-2">
                  <span className={`inline-flex items-center gap-1.5 text-sm font-semibold ${first ? "text-ink" : "text-muted"}`}>
                    {m.pos >= 1 && m.pos <= 3 && (
                      // eslint-disable-next-line @next/next/no-img-element
                      <img
                        src={`/images/honor/hang-${m.pos}.svg`}
                        alt=""
                        width={first ? 44 : 36}
                        height={first ? 44 : 36}
                        className={first ? "h-11 w-11" : "h-9 w-9"}
                      />
                    )}
                    Hạng {m.pos}
                  </span>
                  <RankAvatarFrame tier={{ code: m.tier_code, division: m.division, paragon: m.paragon }} size={first ? 72 : 56}>
                    <Avatar url={m.avatar} name={m.name} size={first ? 72 : 56} />
                  </RankAvatarFrame>
                </div>
                <div className="min-w-0 flex-1 sm:mt-2">
                  <p className={`truncate font-semibold text-ink ${first ? "text-lg" : "text-base"}`}>{m.name}</p>
                  {m.title && <WornTitle title={m.title} className="mt-0.5 sm:justify-center" />}
                  {up ? (
                    <p className="mt-1 inline-flex items-center gap-1 text-xs font-medium text-primary">
                      <ArrowUpCircle size={13} aria-hidden /> Lên {tierLabel(up)} tuần này
                    </p>
                  ) : (
                    <p className="mt-1 text-xs text-muted">
                      {meta.name} {m.paragon ? "" : divisionLabel(m.division)}
                    </p>
                  )}
                  <p className="mt-1.5 font-mono text-sm text-primary">+{m.rp_week} RP tuần</p>
                </div>
              </li>
            );
          })}
        </ul>
      )}
      {(g.top_more ?? 0) > 0 && (
        <p className="mt-3 text-xs text-muted">
          và {g.top_more} bạn khác bằng điểm các bạn trên — bục chỉ đủ chỗ 5 bạn, mỗi tuần đổi thứ tự ngẫu nhiên.
        </p>
      )}

      {/* Ghi nhận ngoài bục: ô trung tính, không viền nhấn để không giành chú ý với hạng 1 (B2); 2 ô cạnh nhau trên desktop. */}
      {(improved || g.streak) && (
        <div className="mt-6 grid gap-3 sm:grid-cols-2">
          {improved && (
            <div className="flex items-center gap-4 rounded-2xl border border-line bg-panel p-4">
              <Avatar url={improved.avatar} name={improved.name} size={48} />
              <div className="min-w-0 flex-1">
                <p className="flex items-center gap-1.5 text-xs font-medium text-muted">
                  <TrendingUp size={14} className="text-primary" aria-hidden /> Tiến bộ nhất tuần
                </p>
                <p className="mt-0.5 truncate text-base font-semibold text-ink">{improved.name}</p>
                <p className="mt-0.5 text-sm text-muted">{improved.detail}</p>
              </div>
            </div>
          )}
          {g.streak && (
            <div className="flex items-center gap-4 rounded-2xl border border-line bg-panel p-4">
              <span className="inline-flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-primary-soft text-primary">
                <Flame size={22} aria-hidden />
              </span>
              <div className="min-w-0 flex-1">
                <p className="text-xs font-medium text-muted">Chuỗi ngày dài nhất</p>
                <p className="mt-0.5 truncate text-base font-semibold text-ink">{g.streak.name}</p>
                <p className="mt-0.5 text-sm text-muted">{g.streak.days} ngày học liên tiếp</p>
              </div>
            </div>
          )}
        </div>
      )}

      {upsOff.length > 0 && (
        <ul className="mt-3 space-y-1 text-sm text-muted">
          {upsOff.map((t) => (
            <li key={t.name} className="flex items-center gap-2">
              <ArrowUpCircle size={14} className="shrink-0 text-primary" aria-hidden />
              <span className="font-medium text-ink">{t.name}</span> lên {tierLabel(t)} tuần này
            </li>
          ))}
        </ul>
      )}
    </>
  );
}

/** Chỉ em đang đăng nhập thấy: so RP tuần này với tuần trước của CHÍNH em, không hiện hạng (SDT — so với mình, không so với bạn). */
function MyWeek({ me }: { me: { rp_week: number; rp_prev: number } }) {
  const diff = me.rp_week - me.rp_prev;
  const msg =
    me.rp_week === 0
      ? "Em chưa có RP tuần này. Một bài luyện tập là bắt đầu."
      : diff > 0
        ? `Nhiều hơn tuần trước ${diff} RP.`
        : diff === 0
          ? "Bằng tuần trước."
          : `Còn ${-diff} RP nữa là bằng tuần trước.`;
  return (
    <div className="mt-4 flex flex-wrap items-center gap-x-4 gap-y-1 rounded-2xl border border-line bg-panel px-4 py-3 text-sm">
      <span className="font-semibold text-ink">Tuần của em</span>
      <span className="font-mono text-primary">+{me.rp_week} RP</span>
      <span className="text-muted">{msg}</span>
      <Link href="/lop-hoc/xep-hang/" className="ml-auto text-primary underline-offset-4 hover:underline">
        Xem mục tiêu tuần
      </Link>
    </div>
  );
}

function weekLabel(weekStart: string, usePrev: boolean): string {
  const start = new Date(`${weekStart}T00:00:00+07:00`);
  if (usePrev) start.setDate(start.getDate() - 7);
  const end = new Date(start);
  end.setDate(end.getDate() + 6);
  const f = (d: Date) => {
    const p = new Intl.DateTimeFormat("en-GB", { day: "2-digit", month: "2-digit", timeZone: "Asia/Ho_Chi_Minh" }).formatToParts(d);
    const get = (t: string) => p.find((x) => x.type === t)?.value ?? "";
    return `${get("day")}/${get("month")}`;
  };
  return `${usePrev ? "tuần trước " : ""}${f(start)} đến ${f(end)}`;
}
