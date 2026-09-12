import {
  Briefcase,
  CheckCircle2,
  ClipboardList,
  Clock3,
  GraduationCap,
  type LucideIcon,
  Users,
  Video,
  XCircle,
} from "lucide-react";
import type { TaSessionStatus, TaSessionType } from "./queries";

export const SESSION_TYPE_META: Record<TaSessionType, { label: string; icon: LucideIcon }> = {
  lop: { label: "Lên lớp", icon: GraduationCap },
  phudao: { label: "Phụ đạo", icon: Users },
  chambai: { label: "Chấm bài", icon: ClipboardList },
  hanhchinh: { label: "Hành chính", icon: Briefcase },
  video: { label: "Video TikTok", icon: Video },
};

export const STATUS_META: Record<
  TaSessionStatus,
  { label: string; icon: LucideIcon; className: string }
> = {
  submitted: { label: "Chờ duyệt", icon: Clock3, className: "bg-amber-500/15 text-amber-300" },
  approved: { label: "Đã duyệt", icon: CheckCircle2, className: "bg-emerald-500/15 text-emerald-300" },
  rejected: { label: "Bị từ chối", icon: XCircle, className: "bg-red-500/15 text-red-300" },
};
