import type { ExamQuestion } from "@/features/exams/types";

// Hệ thống rank — kiểu dữ liệu dùng chung cho các RPC rank_* (docs/supabase-migration-rank-system.sql).

export type TierCode =
  | "tan_binh"
  | "chien_binh"
  | "tinh_anh"
  | "tinh_nhue"
  | "dai_su"
  | "cao_thu"
  | "thach_dau";

export const TIER_ORDER: TierCode[] = [
  "tan_binh",
  "chien_binh",
  "tinh_anh",
  "tinh_nhue",
  "dai_su",
  "cao_thu",
  "thach_dau",
];

export interface TierMeta {
  /** Tên tiếng Việt. */
  name: string;
  /** Tên tiếng Anh in lớn trên huy hiệu. */
  en: string;
  /** Màu chủ đạo của huy hiệu. */
  color: string;
  /** Màu sáng hơn cho gradient/viền. */
  light: string;
  /** Lớp Tailwind cho nền nhạt + chữ. */
  tone: string;
}

// Tên bậc theo bậc rank Liên Quân Mobile (Đồng → Cao Thủ, thấp lên cao); `code` nội bộ
// giữ nguyên (khớp cột rank_tiers.code trong DB — xem
// supabase/migrations/20260928190000_rank_tier_names_lien_quan.sql), chỉ đổi nhãn hiển thị.
export const TIER_META: Record<TierCode, TierMeta> = {
  tan_binh: { name: "Đồng", en: "Bronze", color: "#8a5a3b", light: "#d9a97a", tone: "bg-amber-700/15 text-amber-200" },
  chien_binh: { name: "Bạc", en: "Silver", color: "#8a97a8", light: "#e2e8f0", tone: "bg-slate-400/15 text-slate-200" },
  tinh_anh: { name: "Vàng", en: "Gold", color: "#d4a836", light: "#ffe08a", tone: "bg-yellow-500/15 text-yellow-200" },
  tinh_nhue: { name: "Bạch Kim", en: "Platinum", color: "#2fb6a6", light: "#a6f0e4", tone: "bg-teal-500/15 text-teal-200" },
  dai_su: { name: "Kim Cương", en: "Diamond", color: "#2952c8", light: "#a9c4ff", tone: "bg-indigo-500/15 text-indigo-200" },
  cao_thu: { name: "Tinh Anh", en: "Elite", color: "#6d3fc7", light: "#d3b0ff", tone: "bg-violet-500/15 text-violet-200" },
  thach_dau: { name: "Cao Thủ", en: "Master", color: "#c1122a", light: "#ffb3c0", tone: "bg-rose-600/15 text-rose-200" },
};

/**
 * Danh vị Vô Song (Paragon) — trên cả Cao Thủ, không nằm trên thang RP và không có phân bậc,
 * đặt tên "Thách Đấu" theo bậc cao nhất của Liên Quân Mobile.
 * Không phải bậc thứ tám: `tier.code` vẫn là "thach_dau", chỉ thêm cờ `tier.paragon`.
 */
export const PARAGON_META: TierMeta = { name: "Thách Đấu", en: "Challenger", color: "#7c4dff", light: "#fff0bf", tone: "bg-violet-500/15 text-amber-100" };

export function tierMeta(code: string | null | undefined, paragon?: boolean | null): TierMeta {
  if (paragon) return PARAGON_META;
  return TIER_META[(code ?? "tan_binh") as TierCode] ?? TIER_META.tan_binh;
}

export function divisionLabel(division: number | null | undefined): string {
  return division === 1 ? "I" : division === 2 ? "II" : division === 3 ? "III" : "";
}

/** "Starlight III · Tinh Quang" — dùng cho chỗ chỉ có một dòng chữ. */
export function tierLabel(code: string | null | undefined, division?: number | null, paragon?: boolean | null): string {
  const m = tierMeta(code, paragon);
  const d = paragon ? "" : divisionLabel(division);
  return `${m.en}${d ? ` ${d}` : ""} · ${m.name}`;
}

export function formatRp(n: number | null | undefined): string {
  return (n ?? 0).toLocaleString("vi-VN");
}

export type TitleLevel = "thuc_tinh" | "lam_chu" | "huyen_thoai" | "don";

export const LEVEL_LABELS: Record<TitleLevel, string> = {
  thuc_tinh: "Thức Tỉnh",
  lam_chu: "Làm Chủ",
  huyen_thoai: "Huyền Thoại",
  don: "",
};

export const LEVEL_ORDER: TitleLevel[] = ["thuc_tinh", "lam_chu", "huyen_thoai"];

export function levelRank(level: string | null | undefined): number {
  return level === "thuc_tinh" ? 1 : level === "lam_chu" ? 2 : level === "huyen_thoai" || level === "don" ? 3 : 0;
}

export type TitleGroup = "co_hoc" | "dao_dong_song" | "dien_tu" | "nhiet_hoc" | "hien_dai" | "bo_suu_tap" | "thanh_tich";

export const GROUP_LABELS: Record<TitleGroup, string> = {
  co_hoc: "Cơ học",
  dao_dong_song: "Dao động và sóng",
  dien_tu: "Điện và từ",
  nhiet_hoc: "Nhiệt học",
  hien_dai: "Ánh sáng và vật lý hiện đại",
  bo_suu_tap: "Danh hiệu bộ sưu tập",
  thanh_tich: "Danh hiệu thành tích",
};

export const GROUP_ORDER: TitleGroup[] = ["co_hoc", "dao_dong_song", "dien_tu", "nhiet_hoc", "hien_dai", "bo_suu_tap", "thanh_tich"];

export function titleDisplay(name: string, level: string | null | undefined): string {
  const l = LEVEL_LABELS[(level ?? "don") as TitleLevel] ?? "";
  return l ? `${name} · ${l}` : name;
}

// ---------- rank_my_status / rank_status_of ----------
export interface RankSeasonInfo {
  id: number;
  name: string;
  starts_on: string;
  ends_on: string;
  status: "draft" | "active" | "closed";
}

export interface RankTierInfo {
  code: TierCode;
  name: string;
  sort: number;
  tier_min: number;
  next_min: number | null;
  division: number | null;
  div_min: number;
  div_max: number | null;
  /** Danh vị Thách Đấu (Vô Song): đang Cao Thủ + đủ mọi danh hiệu mức cao nhất (rank_is_paragon). */
  paragon?: boolean;
}

export interface RankGate {
  passed: boolean;
  required_title_count: number;
  required_title_level: TitleLevel | null;
  titles_have: number;
  challenge_required: boolean;
  challenge_exam_id: number | null;
  challenge_title: string | null;
  challenge_pass_pct: number;
  challenge_best_pct: number | null;
}

export interface RankNext {
  code: TierCode;
  name: string;
  min_rp: number;
  rp_needed: number;
  gate: RankGate | null;
}

export interface DisplayTitle {
  code: string;
  name: string;
  level: TitleLevel | null;
  group: TitleGroup;
}

export interface RankWeekly {
  week_start: string;
  done: number;
  target: number;
  min_score: number;
  rp: number;
  achieved: boolean;
  /** true = mục tiêu đặt riêng từ 2 tuần trước của em (migration 20260929130000); RPC cũ không trả. */
  personal?: boolean;
}

export interface RankDaily {
  date: string;
  streak: number;
  min_score: number;
  rp: number;
  today_done: boolean;
  /** Giờ (giờ VN) ngày mới của chuỗi bắt đầu — 3 nghĩa là 3h sáng (migration 20260930130000). */
  reset_hour?: number;
  /** Số ngày bỏ lỡ được đóng băng mỗi tuần (0 = tắt) và số đã dùng trong tuần này. */
  freeze_per_week?: number;
  freeze_used_week?: number;
  /** Có ngày trống hôm qua/hôm nay vừa được đóng băng giữ chuỗi. */
  freeze_saved_recent?: boolean;
}

export interface RankStatus {
  season: RankSeasonInfo | null;
  rp: number;
  tier: RankTierInfo | null;
  next: RankNext | null;
  tier_reached_at: string | null;
  joined_at: string | null;
  display_title: DisplayTitle | null;
  titles_count: number;
  weekly: RankWeekly | null;
  daily: RankDaily | null;
}

// ---------- rank_my_titles / rank_titles_of ----------
export interface TitleTopicRef {
  id: number;
  name: string;
  lesson_id: number | null;
}

export interface SpecialistProgress {
  n: number;
  correct: number;
  de_correct: number;
  de_need: number;
  tb_correct: number;
  tb_need: number;
  kho_correct: number;
  kho_need: number;
  /** Số tuần khác nhau đã giải đúng câu Khó / số tuần cần (Huyền Thoại cần rải ≥ 2 tuần; migration 20260930120000). */
  kho_weeks?: number;
  kho_weeks_need?: number;
  topics: TitleTopicRef[];
}

export interface CollectionProgress {
  required: number;
  met: number;
  level: TitleLevel;
  titles: string[];
}

export interface RankTitle {
  code: string;
  group: TitleGroup;
  kind: "specialist" | "collection" | "achievement";
  name: string;
  description: string;
  /** Có chủ đề thuộc chương lớp em đang học (hoặc là danh hiệu thành tích). */
  visible: boolean;
  /** Có ánh xạ chủ đề — đạt được về nguyên tắc. */
  active: boolean;
  /** Mức cao nhất đã có. */
  level: TitleLevel | null;
  /** Mức → thời điểm nhận. */
  levels: Partial<Record<TitleLevel, string>>;
  progress: SpecialistProgress | CollectionProgress | null;
}

export function isSpecialistProgress(p: RankTitle["progress"]): p is SpecialistProgress {
  return !!p && "de_need" in p;
}

// ---------- lịch sử ----------
export interface RankLedgerEntry {
  id: number;
  season_id: number;
  source_kind: "practice" | "fix" | "weekly_goal" | "daily_streak" | "progress_week" | "homework_check" | "class_goal" | "manual";
  source_ref: string;
  amount: number;
  reason: string;
  ref_result_id: number | null;
  actor_name: string | null;
  created_at: string;
}

export const LEDGER_KIND_LABELS: Record<RankLedgerEntry["source_kind"], string> = {
  practice: "Bài luyện tập",
  fix: "Sửa sai",
  weekly_goal: "Mục tiêu tuần",
  daily_streak: "Chuỗi ngày",
  progress_week: "Tiến bộ tuần",
  homework_check: "Bài tập về nhà",
  class_goal: "Mục tiêu chung của lớp",
  manual: "Giáo viên điều chỉnh",
};

export interface RankSeasonSummary {
  season_id: number;
  name: string;
  starts_on: string;
  ends_on: string;
  status: "draft" | "active" | "closed";
  rp: number;
  tier_code: TierCode;
  division: number | null;
  titles_count: number;
  paragon?: boolean;
}

// ---------- trang lớp ----------
export interface ClassRankMember {
  name: string;
  avatar: string | null;
  division: number | null;
  /** `code` có từ migration 20260928130000 (để lấy logo); RPC cũ chỉ trả name/level. */
  title: { code?: string | null; name: string; level: TitleLevel | null } | null;
}

export interface ClassRankGroups {
  season: { id: number; name: string; starts_on: string; ends_on: string } | null;
  tiers: { code: TierCode; name: string; sort: number; members: ClassRankMember[] }[];
  unranked: { name: string; avatar: string | null }[];
  weekly: { name: string; kind: "weekly_goal" | "tier_up" | "title"; label: string; at: string }[];
  week_start: string;
}

export interface ClassRankBoardMember {
  name: string;
  avatar: string | null;
  rp_week: number;
  /** Danh hiệu đang đeo — có từ migration 20260928130000; RPC cũ không trả. */
  title?: { code: string; name: string; level: TitleLevel | null } | null;
}

export interface ClassRankBoard {
  season: { id: number; name: string; starts_on: string; ends_on: string } | null;
  week_start: string;
  top_week: (ClassRankBoardMember & { pos: number; tier_code: TierCode | null; division: number | null; is_me: boolean; paragon?: boolean })[];
  me: {
    rp_week: number;
    /** Bậc của em + số bạn cùng bậc (gồm em) — chỉ so với bạn cùng bậc, không có thứ tự tuyệt đối. */
    tier_code: TierCode | null;
    division: number | null;
    tier_size: number;
    in_top: boolean;
    tied: number;
    above: ClassRankBoardMember | null;
    below: ClassRankBoardMember | null;
  } | null;
  improved: (ClassRankBoardMember & { delta: number }) | null;
  weekly: { name: string; kind: "weekly_goal" | "tier_up" | "title"; label: string; at: string }[];
  /** Mục tiêu chung của lớp trong tuần (migration 20260930140000; RPC cũ không trả). */
  class_goal?: ClassGoal | null;
}

/** "Cả lớp đạt N huy hiệu tuần này" — mọi huy hiệu của bất kỳ ai trong lớp đều tính. */
export interface ClassGoal {
  week_start: string;
  target: number;
  done: number;
  members: number;
  my_contrib: number;
  rp: number;
  reached: boolean;
}

// ---------- Báo cáo cho thầy (migration 20260930150000) ----------
export interface MondayList {
  week_start: string;
  week_end: string;
  level_ups: { student_id: string; name: string; count: number; items: string[] }[];
  improved: { student_id: string; name: string; acc_now: number; acc_base: number; gain: number }[];
}

export interface QuartileGroup {
  n: number;
  active_season: number;
  /** null khi chưa tới tuần 4 của mùa. */
  active_w45: number | null;
  with_badge: number;
  cleared: number;
}

export interface QuartileMetrics {
  season_id: number;
  starts_on: string;
  ends_on: string;
  w45_ready: boolean;
  baseline: string;
  groups: { bottom?: QuartileGroup; rest?: QuartileGroup; no_baseline?: QuartileGroup };
}

// ---------- sửa sai ----------
export interface FixQuizStart {
  attemptId: number;
  topicName: string;
  total: number;
  attemptsLeft: number;
  passPct: number;
  questions: ExamQuestion[];
}

export interface FixQuizResult {
  pct: number;
  passed: boolean;
  rpDelta: number;
  fixedTopics: number;
  wrongTopics: number;
}

export interface FixableTopic {
  topicId: number;
  name: string;
  wrong: number;
  total: number;
  attemptsDone: number;
  passed: boolean;
}

// ---------- rank_public_honor (trang chủ công khai, anon) ----------
/** Mức lộ tên của học sinh trên mục Vinh danh tuần ở trang chủ (profiles.honor_visibility). */
export type HonorVisibility = "hidden" | "short" | "full";

export const HONOR_VISIBILITY_LABELS: Record<HonorVisibility, string> = {
  short: "Tên rút gọn + ảnh",
  full: "Tên đầy đủ + ảnh",
  hidden: "Không hiện",
};

export interface PublicHonorMember {
  pos: number;
  /** Đã rút gọn/ẩn theo mức của em đó ngay trong RPC — client không bao giờ nhận tên đầy đủ khi em chọn rút gọn. */
  name: string;
  avatar: string | null;
  rp_week: number;
  tier_code: TierCode | null;
  division: number | null;
  paragon: boolean;
  title: { code: string; name: string; level: TitleLevel | null } | null;
}

export interface PublicHonorGrade {
  grade: string;
  /** Tuần này chưa ai có RP → số liệu là của tuần trước. */
  use_prev: boolean;
  season: { id: number; name: string; ends_on: string } | null;
  total: number;
  top: PublicHonorMember[];
  /** Số bạn cùng top 3 nhưng không hiện vì bục tối đa 5 ô (migration 20260928180000; RPC cũ không trả). */
  top_more?: number;
  improved: { name: string; avatar: string | null; delta: number; rp_week: number } | null;
  /** Tiến bộ theo tỉ lệ đúng so với 2 tuần trước (migration 20260929120000; RPC cũ không trả). Ưu tiên hơn `improved`. */
  improved_acc?: { name: string; avatar: string | null; gain: number; acc: number } | null;
  tier_ups: { name: string; tier_code: TierCode; division: number | null }[];
  streak: { name: string; days: number } | null;
}

export interface PublicHonorBoard {
  week_start: string;
  grades: PublicHonorGrade[];
}
