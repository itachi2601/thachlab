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
        <Stage top={g.top} upByName={upByName} tierLabel={tierLabel} />
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

type TierUp = PublicHonorGrade["tier_ups"][number];

// Sân khấu vinh danh đen–vàng (thầy chốt 15/10/2026, theo mẫu bục trao giải): cố ý giữ nền tối ở CẢ hai giao diện
// như một khung trưng bày (M5 – khung tối có chủ đích, đệm đều), nên màu chữ cố định ở đây thay vì token theme.
// Chữ chính #F1F5F9 trên #0A0A0D (không trắng tinh trên đen tinh — M2); vàng #E9C46A ~11:1. Không chuyển động (B4).
// Ba bục hình trụ cao 1 > 2 > 3, hạng 1 đứng giữa ở mọi khổ màn hình; hạng 4–5 (khi hoà điểm) xuống hàng gọn bên dưới.
const PEDESTAL = {
  1: { body: "h-20 sm:h-28", avatar: 64, avatarSm: 80, medal: "h-9 w-9 sm:h-11 sm:w-11" },
  2: { body: "h-12 sm:h-[72px]", avatar: 48, avatarSm: 64, medal: "h-7 w-7 sm:h-9 sm:w-9" },
  3: { body: "h-8 sm:h-12", avatar: 48, avatarSm: 64, medal: "h-7 w-7 sm:h-9 sm:w-9" },
} as const;

function Stage({
  top,
  upByName,
  tierLabel,
}: {
  top: PublicHonorGrade["top"];
  upByName: Map<string, TierUp>;
  tierLabel: (t: TierUp) => string;
}) {
  const podium = [top[1], top[0], top[2]].filter(Boolean);
  const rest = top.slice(3);
  return (
    <div className="relative mt-10 overflow-hidden rounded-3xl border border-[#E9C46A]/25 bg-[#0A0A0D] px-2 pb-6 pt-10 sm:px-10 sm:pb-10 sm:pt-14">
      {/* Đèn rọi từ trên xuống + vệt sáng chéo mờ: chỉ là nền, aria-hidden. */}
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_60%_55%_at_50%_0%,rgba(233,196,106,0.28),transparent_70%),linear-gradient(115deg,transparent_38%,rgba(233,196,106,0.07)_45%,transparent_52%),linear-gradient(65deg,transparent_48%,rgba(233,196,106,0.05)_55%,transparent_62%)]"
      />
      <ul className="relative grid grid-cols-3 items-end gap-2 sm:gap-6">
        {podium.map((m) => (
          <PodiumSpot key={`${m.name}-${m.pos}`} m={m} up={upByName.get(m.name)} tierLabel={tierLabel} />
        ))}
      </ul>
      {/* Mặt sàn sân khấu */}
      <div aria-hidden className="relative mx-auto -mt-3 h-6 w-[96%] rounded-[50%] bg-[radial-gradient(ellipse_at_center,rgba(233,196,106,0.18),transparent_70%)]" />

      {rest.length > 0 && (
        <ul className="relative mt-4 divide-y divide-white/10 rounded-2xl border border-white/10 bg-white/[0.03]">
          {rest.map((m) => (
            <li key={`${m.name}-${m.pos}`} className="flex items-center gap-3 px-4 py-2.5 text-sm">
              <span className="w-14 shrink-0 text-[#CBD5E1]">Hạng {m.pos}</span>
              <Avatar url={m.avatar} name={m.name} size={32} />
              <span className="min-w-0 flex-1 truncate font-medium text-[#F1F5F9]">{m.name}</span>
              <span className="font-mono text-[#E9C46A]">+{m.rp_week} RP</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

function PodiumSpot({ m, up, tierLabel }: { m: PublicHonorGrade["top"][number]; up?: TierUp; tierLabel: (t: TierUp) => string }) {
  const p = PEDESTAL[(m.pos >= 1 && m.pos <= 3 ? m.pos : 3) as 1 | 2 | 3];
  const first = m.pos === 1;
  const meta = tierMeta(m.tier_code, m.paragon);
  return (
    <li className="flex min-w-0 flex-col items-center text-center">
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img src={`/images/honor/hang-${Math.min(Math.max(m.pos, 1), 3)}.svg`} alt="" width={44} height={44} className={`${p.medal} mb-1.5`} />
      <span className="sm:hidden">
        <RankAvatarFrame tier={{ code: m.tier_code, division: m.division, paragon: m.paragon }} size={p.avatar}>
          <Avatar url={m.avatar} name={m.name} size={p.avatar} />
        </RankAvatarFrame>
      </span>
      <span className="hidden sm:block">
        <RankAvatarFrame tier={{ code: m.tier_code, division: m.division, paragon: m.paragon }} size={p.avatarSm}>
          <Avatar url={m.avatar} name={m.name} size={p.avatarSm} />
        </RankAvatarFrame>
      </span>
      <p className={`mt-2 w-full truncate px-1 font-semibold text-[#F1F5F9] ${first ? "text-base sm:text-lg" : "text-sm sm:text-base"}`}>{m.name}</p>
      {m.title && (
        <span className="hidden max-w-full sm:block">
          <WornTitle title={m.title} className="mt-0.5 justify-center" />
        </span>
      )}
      <p className="mt-0.5 w-full truncate px-1 text-[11px] text-[#CBD5E1] sm:text-xs">
        {up ? (
          <span className="inline-flex items-center gap-1 text-[#E9C46A]">
            <ArrowUpCircle size={12} aria-hidden /> <span className="sm:hidden">{tierLabel(up)}</span>
            <span className="hidden sm:inline">Lên {tierLabel(up)} tuần này</span>
          </span>
        ) : (
          `${meta.name} ${m.paragon ? "" : divisionLabel(m.division)}`.trim()
        )}
      </p>
      <p className="mt-1 font-mono text-xs text-[#E9C46A] sm:text-sm">+{m.rp_week} RP</p>

      {/* Bục hình trụ: mặt trên elip viền vàng phát sáng, thân đen bóng, bảng tên vàng ở mặt trước. */}
      <div className="relative mt-3 w-full">
        <div className="relative z-10 mx-auto h-4 w-full rounded-[50%] border border-[#E9C46A]/80 bg-[linear-gradient(180deg,#2A2A30,#141418)] shadow-[0_0_16px_rgba(233,196,106,0.45)] sm:h-6" />
        <div
          className={`relative -mt-2 flex w-full items-start justify-center rounded-b-[50%_14px] bg-[linear-gradient(90deg,#060607_0%,#1F1F24_35%,#2C2C32_50%,#1F1F24_65%,#060607_100%)] pt-3 sm:-mt-3 sm:pt-5 ${p.body}`}
        >
          <span className="rounded-md bg-[linear-gradient(180deg,#F6DE97,#C9973A)] px-1.5 py-0.5 text-[11px] font-bold text-[#2A1A05] shadow-sm sm:px-2.5 sm:text-sm">
            Hạng {m.pos}
          </span>
        </div>
      </div>
    </li>
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
