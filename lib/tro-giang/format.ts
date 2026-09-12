import type { TaMonthlyScore } from "./queries";

export function formatVnd(n: number): string {
  return `${Math.round(n).toLocaleString("vi-VN")} đ`;
}

export function formatHours(n: number): string {
  return n.toLocaleString("vi-VN", { maximumFractionDigits: 2 });
}

/**
 * Dòng gợi ý "còn thiếu gì để lên mức thưởng kế tiếp" — luôn chọn đúng 1 đòn bẩy có
 * nhiều điểm để cải thiện nhất, tránh liệt kê dàn trải làm mất động lực.
 */
export function buildNextTierMessage(s: TaMonthlyScore): string {
  if (s.total_score >= 85) {
    return "Đã đạt mức thưởng đầy đủ (4.000 đ/giờ quy đổi) — giữ vững phong độ nhé.";
  }

  const target = s.total_score < 70 ? 70 : 85;
  const targetLabel = target === 85 ? "đầy đủ (4.000 đ/giờ)" : "cơ bản (2.000 đ/giờ)";
  const gap = Math.max(0, Math.round((target - s.total_score) * 10) / 10);

  const levers: { room: number; text: string }[] = [];

  if (s.avg_touches < 12) {
    levers.push({
      room: 40 - s.touches_score,
      text: `trung bình đang ${s.avg_touches.toLocaleString("vi-VN", { maximumFractionDigits: 1 })} lượt chạm mỗi buổi, cần 12`,
    });
  }
  if (s.lop_sessions > 0 && s.error_note_rate < 1) {
    levers.push({
      room: 20 - s.error_note_score,
      text: `mới nộp phiếu lỗi đúng hạn ${s.ontime_error_notes}/${s.lop_sessions} buổi lên lớp`,
    });
  }
  if (s.phudao_sessions > 0 && s.phudao_complete_rate < 1) {
    levers.push({
      room: 20 - s.phudao_score,
      text: `hồ sơ phụ đạo mới đủ điều kiện ${s.complete_phudao}/${s.phudao_sessions} buổi`,
    });
  }
  if (s.flag_count > 0) {
    levers.push({
      room: 20 - s.focus_score,
      text: `đang có ${s.flag_count} lượt nhắc nhở làm việc riêng trong tháng`,
    });
  }

  const best = levers.sort((a, b) => b.room - a.room)[0];
  const detail = best ? ` — ${best.text}` : "";
  return `Còn ${gap} điểm nữa đạt mức thưởng ${targetLabel}${detail}.`;
}
