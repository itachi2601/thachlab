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

export const TIER_META: Record<TierCode, TierMeta> = {
  tan_binh: { name: "Tinh Quang", en: "Starlight", color: "#3b6fd4", light: "#9fc3ff", tone: "bg-blue-500/15 text-blue-200" },
  chien_binh: { name: "Tiên Phong", en: "Vanguard", color: "#4f7a3a", light: "#c9d6a3", tone: "bg-lime-600/15 text-lime-200" },
  tinh_anh: { name: "Nhật Hoa", en: "Corona", color: "#d9701e", light: "#ffd27a", tone: "bg-orange-500/15 text-orange-200" },
  tinh_nhue: { name: "Vương Lễ", en: "Regalia", color: "#c1122a", light: "#ffb3c0", tone: "bg-rose-600/15 text-rose-200" },
  dai_su: { name: "Vương Triều", en: "Dynasty", color: "#2952c8", light: "#a9c4ff", tone: "bg-indigo-500/15 text-indigo-200" },
  cao_thu: { name: "Thiên Thể", en: "Celestial", color: "#6d3fc7", light: "#d3b0ff", tone: "bg-violet-500/15 text-violet-200" },
  thach_dau: { name: "Chí Tôn", en: "Sovereign", color: "#d4a836", light: "#fff0c2", tone: "bg-amber-400/15 text-amber-100" },
};

export function tierMeta(code: string | null | undefined): TierMeta {
  return TIER_META[(code ?? "tan_binh") as TierCode] ?? TIER_META.tan_binh;
}

export function divisionLabel(division: number | null | undefined): string {
  return division === 1 ? "I" : division === 2 ? "II" : division === 3 ? "III" : "";
}

/** "Starlight III · Tinh Quang" — dùng cho chỗ chỉ có một dòng chữ. */
export function tierLabel(code: string | null | undefined, division?: number | null): string {
  const m = tierMeta(code);
  const d = divisionLabel(division);
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
}

export interface RankDaily {
  date: string;
  streak: number;
  min_score: number;
  rp: number;
  today_done: boolean;
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
  acc: number;
  covered: number;
  total_topics: number;
  min_questions: number;
  awaken_accuracy: number;
  master_accuracy: number;
  legend_exam_id: number | null;
  legend_accuracy: number;
  legend_best: number | null;
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
  return !!p && "min_questions" in p;
}

// ---------- lịch sử ----------
export interface RankLedgerEntry {
  id: number;
  season_id: number;
  source_kind: "practice" | "fix" | "weekly_goal" | "manual";
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
}

// ---------- trang lớp ----------
export interface ClassRankMember {
  name: string;
  avatar: string | null;
  division: number | null;
  title: { name: string; level: TitleLevel | null } | null;
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
}

export interface ClassRankBoard {
  season: { id: number; name: string; starts_on: string; ends_on: string } | null;
  week_start: string;
  total: number;
  top_week: (ClassRankBoardMember & { pos: number; tier_code: TierCode | null; division: number | null; is_me: boolean })[];
  me: {
    pos: number;
    rp_week: number;
    tied: number;
    above: ClassRankBoardMember | null;
    below: ClassRankBoardMember | null;
  } | null;
  improved: (ClassRankBoardMember & { delta: number }) | null;
  weekly: { name: string; kind: "weekly_goal" | "tier_up" | "title"; label: string; at: string }[];
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
