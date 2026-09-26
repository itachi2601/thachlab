// Chế độ "Xem như học sinh" của admin: mở khoá HẾT năng lực rank để thầy xem trước
// mọi trạng thái cao nhất (danh vị Vô Song, 45/45 danh hiệu Huyền Thoại, chuỗi ngày,
// mục tiêu tuần, đứng đầu bảng tuần) mà không đụng vào dữ liệu thật.
//
// Chỉ bật khi sessionStorage "thachlab_preview_as_student" = "1" (đúng khoá AuthProvider dùng),
// KHÔNG bật ở chế độ "cttc" (giả lập SV CTTC chạy đường thật). Mọi hàm ở đây thuần túy,
// nhận dữ liệu thật rồi trả bản đã "mở khoá" — services/rank.ts gọi sau khi RPC trả về,
// nên mùa/lớp/tên vẫn là thật, chỉ số liệu rank là giả lập.

import type { ClassRankBoard, RankSeasonSummary, RankStatus, RankTitle, TitleLevel } from "@/features/rank/types";

const PREVIEW_STORAGE_KEY = "thachlab_preview_as_student";

/** Đang xem giao diện học sinh giả lập (không tính chế độ SV CTTC). An toàn khi prerender. */
export function isStudentPreview(): boolean {
  if (typeof window === "undefined") return false;
  try {
    return sessionStorage.getItem(PREVIEW_STORAGE_KEY) === "1";
  } catch {
    return false;
  }
}

const PREVIEW_RP = 999;
const PREVIEW_STREAK = 30;

/** Ngày ISO lùi `d` ngày so với hôm nay — để các mốc "nhận danh hiệu" trông có thật. */
function daysAgo(d: number): string {
  return new Date(Date.now() - d * 86_400_000).toISOString();
}

export function unlockStatus(real: RankStatus | null): RankStatus {
  const today = new Date().toISOString().slice(0, 10);
  const season = real?.season ?? {
    id: 0,
    name: "Mùa xem thử",
    starts_on: today,
    ends_on: today,
    status: "active" as const,
  };
  const weeklyTarget = real?.weekly?.target ?? 3;
  return {
    season,
    rp: Math.max(real?.rp ?? 0, PREVIEW_RP),
    tier: {
      code: "thach_dau",
      name: "Chí Tôn",
      sort: 7,
      tier_min: real?.tier?.code === "thach_dau" ? real.tier.tier_min : 420,
      next_min: null,
      division: null,
      div_min: real?.tier?.code === "thach_dau" ? real.tier.div_min : 420,
      div_max: null,
      paragon: true,
    },
    next: null,
    tier_reached_at: real?.tier_reached_at ?? daysAgo(3),
    joined_at: real?.joined_at ?? daysAgo(30),
    display_title: real?.display_title ?? { code: "ke_giai_ma_vu_tru", name: "Kẻ Giải Mã Vũ Trụ", level: "don", group: "bo_suu_tap" },
    titles_count: 45,
    weekly: {
      week_start: real?.weekly?.week_start ?? today,
      done: weeklyTarget,
      target: weeklyTarget,
      min_score: real?.weekly?.min_score ?? 7,
      rp: real?.weekly?.rp ?? 30,
      achieved: true,
    },
    daily: {
      date: real?.daily?.date ?? today,
      streak: PREVIEW_STREAK,
      min_score: real?.daily?.min_score ?? 7,
      rp: real?.daily?.rp ?? 5,
      today_done: true,
    },
  };
}

/** Mọi danh hiệu đều hiện, đều kích hoạt, đều ở mức cao nhất; tiến độ đầy 100 %. */
export function unlockTitles(real: RankTitle[]): RankTitle[] {
  return real.map((t, i) => {
    const top: TitleLevel = t.kind === "achievement" ? "don" : "huyen_thoai";
    const levels: RankTitle["levels"] =
      top === "don"
        ? { don: daysAgo(20 - (i % 15)) }
        : { thuc_tinh: daysAgo(24 - (i % 10)), lam_chu: daysAgo(14 - (i % 8)), huyen_thoai: daysAgo(4 - (i % 4)) };
    let progress = t.progress;
    if (progress && "min_questions" in progress) {
      progress = {
        ...progress,
        n: Math.max(progress.n, progress.min_questions * 2),
        correct: Math.max(progress.correct, progress.min_questions * 2),
        acc: 100,
        covered: progress.total_topics,
        legend_best: 100,
      };
    } else if (progress && "required" in progress) {
      progress = { ...progress, met: progress.required };
    }
    return { ...t, visible: true, active: true, level: top, levels, progress };
  });
}

/** Em đứng đầu bảng tuần của lớp với danh vị Vô Song; các bạn khác giữ nguyên. */
export function unlockBoard(real: ClassRankBoard | null, myName: string, myAvatar: string | null): ClassRankBoard | null {
  if (!real || !real.season) return real;
  const top = Math.max(0, ...real.top_week.map((m) => m.rp_week));
  const rpWeek = top + 25;
  const others = real.top_week.filter((m) => !m.is_me);
  const me = { pos: 1, name: myName, avatar: myAvatar, rp_week: rpWeek, tier_code: "thach_dau" as const, division: null, is_me: true, paragon: true };
  const top_week = [me, ...others.map((m) => ({ ...m, pos: m.pos + 1 }))].slice(0, 3);
  const below = others[0] ? { name: others[0].name, avatar: others[0].avatar, rp_week: others[0].rp_week } : null;
  return {
    ...real,
    top_week,
    me: { pos: 1, rp_week: rpWeek, tied: 0, above: null, below },
  };
}

export function unlockSeasons(real: RankSeasonSummary[]): RankSeasonSummary[] {
  return real.map((s) =>
    s.status === "active" ? { ...s, rp: Math.max(s.rp, PREVIEW_RP), tier_code: "thach_dau", division: null, titles_count: 45, paragon: true } : s,
  );
}
