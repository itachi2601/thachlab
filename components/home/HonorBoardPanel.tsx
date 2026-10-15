"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { ArrowUpCircle, Crown, Flame, TrendingUp } from "lucide-react";
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

        <Podium key={active.grade} g={active} />

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

// Sân khấu vinh danh (thầy chốt 15/10/2026): GIỮ CẤU TRÚC mẫu bục trao giải (đèn rọi, 3 bục trụ, bảng tên) nhưng
// MÀU theo token của site — tự đổi theo nền sáng/tối, một màu nhấn primary (M3, M7). Vàng/bạc/đồng chỉ ở huy chương.
// Không chuyển động (B4). Bục trụ cao 1 > 2 > 3, hạng 1 đứng giữa ở mọi khổ; hạng 4–5 (khi hoà điểm) xuống hàng gọn bên dưới.
// Ánh kim lấy từ token có sẵn (không thêm màu mới — M3/M7): vàng = accent, bạc = muted,
// đồng = accent + danger pha ink (nền tối ra cam đào, nền sáng ra nâu đỏ — tách được với vàng ở cả hai nền).
const METAL = {
  1: "var(--color-accent)",
  2: "var(--color-muted)",
  3: "color-mix(in srgb, color-mix(in srgb, var(--color-accent) 50%, var(--color-danger)) 75%, var(--color-ink))",
} as const;
const PEDESTAL = {
  1: { body: "h-32 sm:h-44", avatar: 64, avatarSm: 84, num: "text-5xl sm:text-6xl" },
  2: { body: "h-24 sm:h-36", avatar: 52, avatarSm: 68, num: "text-4xl sm:text-5xl" },
  3: { body: "h-[84px] sm:h-32", avatar: 52, avatarSm: 68, num: "text-4xl sm:text-5xl" },
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
    <div className="relative mt-10 overflow-hidden rounded-3xl border border-line bg-panel px-2 pb-6 pt-12 shadow-[0_0_48px_-12px_color-mix(in_srgb,var(--color-primary)_45%,transparent)] sm:px-10 sm:pb-10 sm:pt-16">
      {/* Đèn rọi từ trên xuống + vệt sáng chéo mờ: chỉ là nền, aria-hidden. */}
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_60%_55%_at_50%_0%,color-mix(in_srgb,var(--color-primary)_16%,transparent),transparent_70%),linear-gradient(115deg,transparent_38%,color-mix(in_srgb,var(--color-primary)_5%,transparent)_45%,transparent_52%),linear-gradient(65deg,transparent_48%,color-mix(in_srgb,var(--color-primary)_4%,transparent)_55%,transparent_62%)]"
      />
      <ul className="relative mx-auto grid max-w-[720px] grid-cols-3 items-end gap-2 sm:gap-3">
        {podium.map((m) => (
          <PodiumSpot key={`${m.name}-${m.pos}`} m={m} up={upByName.get(m.name)} tierLabel={tierLabel} />
        ))}
      </ul>
      {/* Mặt sàn sân khấu */}
      <div aria-hidden className="relative mx-auto -mt-3 h-6 w-[96%] rounded-[50%] bg-[radial-gradient(ellipse_at_center,color-mix(in_srgb,var(--color-primary)_14%,transparent),transparent_70%)]" />

      {rest.length > 0 && (
        <ul className="relative mt-4 divide-y divide-line rounded-2xl border border-line bg-surface-2">
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
  const p = PEDESTAL[key];
  const metal = METAL[key];
  const first = m.pos === 1;
  // Bỏ huy chương trên đầu + dòng tên bậc trên bục (N7, N4): số hạng trên thân bục đã nói hạng; bậc là tích luỹ cả mùa,
  // đặt cạnh RP tuần dễ gây "hạng 1 mà bậc thấp hơn hạng 2". Chỉ giữ nhãn ↑ khi em lên bậc trong tuần.
  // Thứ tự: tên (+↑) → ảnh đứng đè 1/3 dưới lên miệng bục → số hạng ánh kim + RP trên thân bục (B3: một khối liền).
  return (
    <li className="relative flex min-w-0 flex-col items-center text-center" style={{ ["--metal" as string]: metal }}>
      <Sparkles pos={key} />
      <p className={`w-full truncate px-1 font-semibold text-ink ${first ? "text-base sm:text-lg" : "text-sm sm:text-base"}`}>{m.name}</p>
      {m.title && (
        <span className="hidden max-w-full sm:block">
          <WornTitle title={m.title} className="mt-0.5 justify-center" />
        </span>
      )}
      {up && (
        <p className="mt-0.5 inline-flex max-w-full items-center gap-1 truncate px-1 text-[11px] text-[color-mix(in_srgb,var(--color-primary)_75%,var(--color-ink))] sm:text-xs">
          <ArrowUpCircle size={12} className="shrink-0" aria-hidden /> <span className="sm:hidden">{tierLabel(up)}</span>
          <span className="hidden sm:inline">Lên {tierLabel(up)} tuần này</span>
        </p>
      )}

      <div className={`relative w-full ${first ? "mt-5 sm:mt-10" : "mt-2"}`}>
        {/* Bóng tiếp đất — đặt trước để thân bục vẽ đè lên, không che chữ RP. */}
        <div aria-hidden className="absolute -bottom-2 left-1/2 h-4 w-[115%] -translate-x-1/2 rounded-[50%] bg-[radial-gradient(ellipse_at_center,rgba(0,0,0,0.28),transparent_70%)]" />
        {/* Ảnh đứng trên bục: đáy ảnh đè xuống mặt elip (z-20 trên mặt bục). */}
        <div className={`relative z-20 mx-auto flex w-fit justify-center ${first ? "-mb-7 sm:-mb-9" : "-mb-6 sm:-mb-7"}`}>
          {first && (
            <Crown
              aria-hidden
              strokeWidth={1.75}
              className="absolute -right-3 -top-4 z-30 h-7 w-7 rotate-[18deg] fill-[var(--color-accent)] text-[color-mix(in_srgb,var(--color-accent)_70%,black)] drop-shadow-[0_0_6px_color-mix(in_srgb,var(--color-accent)_60%,transparent)] sm:-right-4 sm:-top-4 sm:h-8 sm:w-8"
            />
          )}
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
        </div>
        {/* Mặt trên elip: viền ánh kim theo hạng; hạng 1 thêm đèn hắt từ tâm (radial) — điểm nhấn duy nhất của sân khấu (B2). */}
        <div
          className={`relative z-10 mx-auto h-7 w-full rounded-[50%] border-2 border-[var(--metal)] sm:h-10 ${
            first
              ? "bg-[radial-gradient(ellipse_at_center,color-mix(in_srgb,var(--color-accent)_45%,var(--color-panel))_0%,color-mix(in_srgb,var(--color-accent)_12%,var(--color-panel))_60%,var(--color-panel)_100%)] shadow-[0_0_22px_color-mix(in_srgb,var(--color-accent)_40%,transparent)]"
              : "bg-[radial-gradient(ellipse_at_center,color-mix(in_srgb,var(--metal)_30%,var(--color-panel)),color-mix(in_srgb,var(--metal)_10%,var(--color-panel)))] shadow-[0_0_14px_color-mix(in_srgb,var(--metal)_35%,transparent)]"
          }`}
        />
        <div
          className={`relative -mt-3.5 flex w-full flex-col items-center justify-start overflow-hidden rounded-b-[50%_14px] border-x-2 border-b-2 border-[color-mix(in_srgb,var(--metal)_70%,transparent)] bg-[linear-gradient(90deg,color-mix(in_srgb,var(--metal)_40%,var(--color-bg))_0%,color-mix(in_srgb,var(--metal)_10%,var(--color-panel))_30%,color-mix(in_srgb,var(--metal)_6%,var(--color-panel))_50%,color-mix(in_srgb,var(--metal)_10%,var(--color-panel))_70%,color-mix(in_srgb,var(--metal)_40%,var(--color-bg))_100%)] pt-5 sm:-mt-5 sm:pt-6 ${
            first ? "shadow-[0_0_28px_color-mix(in_srgb,var(--metal)_45%,transparent)]" : "shadow-[0_0_14px_color-mix(in_srgb,var(--metal)_25%,transparent)]"
          } ${p.body}`}
        >
          {/* Hai vạch đèn dọc ở mép thân bục (như bục trao giải), màu kim loại của hạng. */}
          <span aria-hidden className="absolute bottom-3 left-[9%] top-4 w-[3px] rounded-full bg-[var(--metal)] opacity-80 shadow-[0_0_8px_var(--metal)]" />
          <span aria-hidden className="absolute bottom-3 right-[9%] top-4 w-[3px] rounded-full bg-[var(--metal)] opacity-80 shadow-[0_0_8px_var(--metal)]" />
          {/* Số hạng đậm, ánh kim theo hạng (gradient chữ từ token); RP chữ ink cùng hệ, không màu nhấn neon. */}
          <span
            aria-label={`Hạng ${m.pos}`}
            className={`bg-[linear-gradient(180deg,color-mix(in_srgb,var(--metal)_55%,white),var(--metal)_55%,color-mix(in_srgb,var(--metal)_75%,black))] bg-clip-text font-display font-black leading-none text-transparent ${p.num}`}
          >
            {m.pos}
          </span>
          <span className={`mt-1 font-mono font-semibold text-ink ${first ? "text-sm sm:text-base" : "text-xs sm:text-sm"}`}>+{m.rp_week} RP</span>
        </div>
      </div>
    </li>
  );
}

// Trang trí TĨNH quanh bục (thầy chốt 15/10/2026 theo ảnh mẫu): hạng 1 có pháo hoa + hoa giấy, hạng 2–3 vài ngôi sao lấp lánh.
// Không chuyển động (B4), aria-hidden, màu từ token. Giữ thưa để không lấn tên/ảnh (N7) và không thổi phồng thứ hạng.
const STAR = "M0,-6 L1.4,-1.4 L6,0 L1.4,1.4 L0,6 L-1.4,1.4 L-6,0 L-1.4,-1.4Z";
function Sparkles({ pos }: { pos: 1 | 2 | 3 }) {
  if (pos !== 1) {
    const stars = pos === 2 ? [[14, 62, 1], [88, 74, 0.7], [20, 92, 0.55]] : [[86, 60, 1], [12, 76, 0.7], [82, 92, 0.55]];
    return (
      <svg aria-hidden viewBox="0 0 100 120" className="pointer-events-none absolute inset-x-0 top-0 z-0 h-[60%] w-full overflow-visible">
        {stars.map(([x, y, k], i) => (
          <path key={i} d={STAR} transform={`translate(${x} ${y}) scale(${k})`} style={{ fill: "var(--metal)" }} opacity={0.9} />
        ))}
      </svg>
    );
  }
  const rays = Array.from({ length: 12 }, (_, i) => (i * Math.PI) / 6);
  const confetti: [number, number, number, string][] = [
    [80, 34, 25, "var(--color-accent)"], [84, 48, -30, "var(--color-primary)"], [92, 26, 60, "var(--color-muted)"],
    [72, 30, 10, "var(--color-accent)"], [6, 26, -20, "var(--color-primary)"], [94, 42, 45, "var(--color-muted)"],
    [24, 54, 35, "var(--color-accent)"],
  ];
  return (
    <svg aria-hidden viewBox="0 0 100 120" className="pointer-events-none absolute -inset-x-6 top-2 z-0 h-[62%] w-[calc(100%+3rem)] overflow-visible">
      <g transform="translate(14 40)" style={{ stroke: "var(--color-accent)" }} strokeWidth={1.1} strokeLinecap="round">
        {rays.map((a, i) => (
          <line key={i} x1={Math.cos(a) * 4} y1={Math.sin(a) * 4} x2={Math.cos(a) * 10} y2={Math.sin(a) * 10} />
        ))}
      </g>
      {confetti.map(([x, y, r, c], i) => (
        <rect key={i} x={-1.6} y={-0.7} width={3.2} height={1.4} rx={0.4} transform={`translate(${x} ${y}) rotate(${r})`} style={{ fill: c }} />
      ))}
      <path d={STAR} transform="translate(84 58) scale(0.8)" style={{ fill: "var(--color-accent)" }} />
      <path d={STAR} transform="translate(10 66) scale(0.6)" style={{ fill: "var(--color-accent)" }} />
    </svg>
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
