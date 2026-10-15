"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import { ArrowUpCircle, Flame, TrendingUp } from "lucide-react";
import Avatar from "@/components/ui/Avatar";
import RankAvatarFrame from "@/components/rank/RankAvatarFrame";
import RankBadge from "@/components/rank/RankBadge";
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
            <p className="font-mono text-xs uppercase tracking-widest text-[color-mix(in_srgb,var(--color-primary)_75%,var(--color-ink))]">
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

        <div className="grid">
          {grades.map((g) => (
            <div key={g.grade} className={`[grid-area:1/1] ${g.grade === active.grade ? "" : "pointer-events-none invisible"}`}>
              <Podium g={g} />
            </div>
          ))}
        </div>

        {board.me && <MyWeek me={board.me} />}

        <p className="mt-8 text-xs text-slate-500">
          Tên hiện rút gọn theo lựa chọn của từng bạn. Học sinh đổi cách hiện (đầy đủ, rút gọn hoặc ẩn) trong{" "}
          <Link href="/tai-khoan/" className="text-[color-mix(in_srgb,var(--color-primary)_75%,var(--color-ink))] underline-offset-4 hover:underline">
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
                  <TrendingUp size={14} className="text-[color-mix(in_srgb,var(--color-primary)_75%,var(--color-ink))]" aria-hidden /> Tiến bộ nhất tuần
                </p>
                <p className="mt-0.5 truncate text-base font-semibold text-ink">{improved.name}</p>
                <p className="mt-0.5 text-sm text-muted">{improved.detail}</p>
              </div>
            </div>
          )}
          {g.streak && (
            <div className="flex items-center gap-4 rounded-2xl border border-line bg-panel p-4">
              <span className="inline-flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-primary-soft text-[color-mix(in_srgb,var(--color-primary)_75%,var(--color-ink))]">
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
              <ArrowUpCircle size={14} className="shrink-0 text-[color-mix(in_srgb,var(--color-primary)_75%,var(--color-ink))]" aria-hidden />
              <span className="font-medium text-ink">{t.name}</span> lên {tierLabel(t)} tuần này
            </li>
          ))}
        </ul>
      )}
    </>
  );
}

type TierUp = PublicHonorGrade["tier_ups"][number];

// Sân khấu vinh danh theo thiết kế "Bục vinh danh 2b" (thầy chọn 15/10/2026): ba huy chương treo dây ruy-băng dưới thanh vàng,
// hạng 1 ở giữa, dây ngắn nhất nên huy chương cao nhất và to nhất. Nền/chữ theo token (nền sáng + tối); chỉ ruy-băng và
// viền huy chương dùng màu cố định vì là "vật liệu" (vàng/bạc/đồng). Không chuyển động (B4). Hạng 4–5 (hoà điểm) xuống danh sách gọn.
const GOLD = "linear-gradient(180deg,#FFF1B8,#E9B949 45%,#9A6A18)";
const SHADE = "linear-gradient(90deg,rgba(0,0,0,0.3),transparent 25%,transparent 75%,rgba(0,0,0,0.3))";
const MEDAL = {
  1: {
    ribbon: "linear-gradient(90deg,#6E111C 0 12%,#A81E2C 12% 42%,#E9B949 42% 58%,#A81E2C 58% 88%,#6E111C 88%)",
    ring: "linear-gradient(135deg,#FFF6C0,#FFD23F 30%,#E0A100 62%,#FFE98A)",
    num: "#F2D27A",
    drop: "h-9 w-[30px] sm:h-12 sm:w-10",
    size: 76,
    sizeSm: 100,
  },
  2: {
    ribbon: "linear-gradient(90deg,#14234A 0 12%,#2B4C8C 12% 30%,#DDE6F5 30% 38%,#2B4C8C 38% 62%,#DDE6F5 62% 70%,#2B4C8C 70% 88%,#14234A 88%)",
    ring: "linear-gradient(135deg,#FFFFFF,#C9D1DC 35%,#7D8796 65%,#E8EDF3)",
    num: "#DDE3EC",
    drop: "h-16 w-[26px] sm:h-[84px] sm:w-8",
    size: 68,
    sizeSm: 84,
  },
  3: {
    ribbon: "linear-gradient(90deg,#6B2F10 0 12%,#B85A22 12% 32%,#F3D9B5 32% 38%,#B85A22 38% 62%,#F3D9B5 62% 68%,#B85A22 68% 88%,#6B2F10 88%)",
    ring: "linear-gradient(135deg,#D9966B,#A4531F 35%,#5E2A0E 65%,#B9733F)",
    num: "#EDB487",
    drop: "h-[84px] w-[26px] sm:h-[112px] sm:w-8",
    size: 68,
    sizeSm: 84,
  },
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
  const ref = useRef<HTMLDivElement>(null);
  const [play, setPlay] = useState(false);
  // Chạy hiệu ứng đúng một lần khi bục vào khung nhìn (khối ẩn bằng `invisible` không giao nhau nên không chạy sớm).
  useEffect(() => {
    const el = ref.current;
    if (!el || typeof IntersectionObserver === "undefined") return;
    const io = new IntersectionObserver(
      (es) => {
        if (es.some((e) => e.isIntersecting)) {
          setPlay(true);
          io.disconnect();
        }
      },
      { threshold: 0.6 },
    );
    io.observe(el);
    return () => io.disconnect();
  }, []);
  return (
    <div ref={ref} className={`relative mt-10 overflow-hidden rounded-3xl border border-line bg-panel px-2 pb-6 pt-5 sm:px-10 sm:pb-10 sm:pt-6 ${play ? "honor-play" : ""}`}>
      {/* Đèn rọi từ trên xuống: chỉ là nền, aria-hidden. */}
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 bg-[radial-gradient(60%_40%_at_50%_30%,color-mix(in_srgb,var(--color-accent)_10%,transparent),transparent_70%)]"
      />
      {/* Sao băng vụt qua một lần; chỉ trang trí. */}
      <div aria-hidden className="honor-fx pointer-events-none absolute inset-0 overflow-hidden">
        <span className="honor-shoot absolute left-[8%] top-[6%] h-0.5 w-16 rounded-full bg-gradient-to-r from-transparent to-[#FFF1B8] opacity-0" />
        <span className="honor-shoot honor-shoot-2 absolute left-[30%] top-[2%] h-0.5 w-12 rounded-full bg-gradient-to-r from-transparent to-white opacity-0" />
      </div>
      {/* Thanh vàng treo ba huy chương. */}
      <div aria-hidden className="relative mx-1.5 h-2 rounded shadow-[0_2px_4px_rgba(0,0,0,0.35)]" style={{ background: GOLD }} />
      <ul className="relative mx-auto grid max-w-[720px] grid-cols-[1fr_1.2fr_1fr] items-start gap-1 sm:gap-3">
        {podium.map((m) => (
          <PodiumSpot key={`${m.name}-${m.pos}`} m={m} up={upByName.get(m.name)} tierLabel={tierLabel} />
        ))}
      </ul>

      {rest.length > 0 && (
        <ul className="relative mt-6 divide-y divide-line rounded-2xl border border-line bg-surface-2">
          {rest.map((m) => (
            <li key={`${m.name}-${m.pos}`} className="flex items-center gap-3 px-4 py-2.5 text-sm">
              <span className="w-14 shrink-0 text-muted">Hạng {m.pos}</span>
              <Avatar url={m.avatar} name={m.name} size={32} />
              <span className="min-w-0 flex-1 truncate font-medium text-ink">{m.name}</span>
              <span className="font-mono text-[color-mix(in_srgb,var(--color-primary)_75%,var(--color-ink))]">+{m.rp_week} RP</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

function PodiumSpot({ m, up, tierLabel }: { m: PublicHonorGrade["top"][number]; up?: TierUp; tierLabel: (t: TierUp) => string }) {
  const key = (m.pos >= 1 && m.pos <= 3 ? m.pos : 3) as 1 | 2 | 3;
  const d = MEDAL[key];
  const first = m.pos === 1;
  // Thứ tự dọc: ruy-băng (số hạng) → thanh kẹp vàng → vòng treo → huy chương (ảnh) → tên (+danh hiệu, ↑) → RP.
  // Bỏ dòng tên bậc dưới tên (N4, N7): bậc tích luỹ cả mùa, đặt cạnh RP tuần dễ thành "hạng 1 mà bậc thấp hơn hạng 2".
  return (
    <li className="flex min-w-0 flex-col items-center text-center">
      <div
        className={`flex items-center justify-center ${d.drop}`}
        style={{ background: `${SHADE},${d.ribbon}` }}
      >
        <span
          aria-label={`Hạng ${m.pos}`}
          className="flex h-5 w-5 items-center justify-center rounded-full bg-[rgba(8,12,22,0.85)] font-display text-[15px] font-bold leading-none sm:h-6 sm:w-6 sm:text-lg"
          style={{ color: d.num }}
        >
          {m.pos}
        </span>
      </div>
      <div aria-hidden className="h-1.5 w-[34px] rounded-sm sm:w-11" style={{ background: GOLD }} />
      <div aria-hidden className="relative z-[2] -mt-px h-3 w-3 rounded-full border-[3px] border-[#E9B949]" />
      <div
        className={`relative z-[1] -mt-1.5 rounded-full p-1 ${first ? "shadow-[0_0_34px_rgba(255,210,63,0.75)]" : "shadow-[0_4px_12px_rgba(0,0,0,0.35)]"}`}
        style={{ background: d.ring }}
      >
        <span className="block overflow-hidden rounded-full border-2 border-[#10141D] sm:hidden">
          <Avatar url={m.avatar} name={m.name} size={d.size} />
        </span>
        <span className="hidden overflow-hidden rounded-full border-2 border-[#10141D] sm:block">
          <Avatar url={m.avatar} name={m.name} size={d.sizeSm} />
        </span>
        {first && (
          <span aria-hidden className="honor-fx pointer-events-none absolute left-1/2 top-1/2 h-0 w-0">
            {[0, 45, 90, 135, 180, 225, 270, 315].map((a, i) => (
              <span
                key={a}
                className="honor-spark absolute -ml-[3px] -mt-[3px] block h-1.5 w-1.5 rounded-full opacity-0"
                style={{ ["--a" as string]: `${a}deg`, ["--d" as string]: `${i % 2 ? 62 : 82}px`, background: i % 2 ? "#FFF1B8" : "#FFD23F" }}
              />
            ))}
            <span className="honor-glint absolute -left-8 -top-12 block h-3 w-3 rotate-45 bg-[#FFF1B8] opacity-0 [clip-path:polygon(50%_0,62%_38%,100%_50%,62%_62%,50%_100%,38%_62%,0_50%,38%_38%)]" />
          </span>
        )}
        {/* Huy hiệu rank đạt được: ô "rank" ở góc dưới phải huy chương trong thiết kế. */}
        {m.tier_code && (
          <RankBadge
            code={m.tier_code}
            division={m.division}
            paragon={m.paragon}
            size={36}
            className="pointer-events-none absolute -bottom-2 -right-3 drop-shadow-[0_2px_4px_rgba(0,0,0,.7)]"
          />
        )}
      </div>
      <p className={`mt-3.5 w-full truncate px-1 font-bold text-ink ${first ? "text-base sm:text-lg" : "text-[15px] sm:text-base"}`}>{m.name}</p>
      {m.title && <WornTitle title={m.title} className="mt-1 max-w-full justify-center" />}
      {m.tier_code && !up && (
        <p className="mt-0.5 max-w-full truncate px-1 text-[11px] text-muted">
          {`${tierMeta(m.tier_code, m.paragon).name} ${divisionLabel(m.division)}`.trim()}
        </p>
      )}
      {up && (
        <p className="mt-1 inline-flex max-w-full items-center gap-1 truncate px-1 text-[11px] text-[color-mix(in_srgb,var(--color-primary)_75%,var(--color-ink))] sm:text-xs">
          <ArrowUpCircle size={12} className="shrink-0" aria-hidden /> <span className="sm:hidden">{tierLabel(up)}</span>
          <span className="hidden sm:inline">Lên {tierLabel(up)} tuần này</span>
        </p>
      )}
      <p
        className={`mt-2 font-display font-bold tracking-[0.06em] text-ink ${first ? "text-xl sm:text-2xl" : "text-lg sm:text-xl"}`}
      >
        +{m.rp_week} RP
      </p>
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
      <span className="font-mono text-[color-mix(in_srgb,var(--color-primary)_75%,var(--color-ink))]">+{me.rp_week} RP</span>
      <span className="text-muted">{msg}</span>
      <Link href="/lop-hoc/xep-hang/" className="ml-auto text-[color-mix(in_srgb,var(--color-primary)_75%,var(--color-ink))] underline-offset-4 hover:underline">
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
