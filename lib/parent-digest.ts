import { dayMonth, gradeBand, scoreText } from "@/lib/parent-format";

/**
 * Soạn sẵn tin Zalo tóm tắt tuần gửi phụ huynh — để phụ huynh nhận được điều cần biết NGAY TRONG ZALO,
 * không phải đăng nhập (đăng nhập là chỗ rớt nhiều nhất với người 45–60 sợ "quê" trước công nghệ).
 * Thầy sửa lại trước khi gửi; hàm này chỉ dựng bản nháp từ số liệu thật, không bịa gì.
 */
export interface DigestInput {
  studentName: string;
  /** Bài đã làm, mới nhất ở cuối. */
  points: { score: number; at: string; examTitle: string }[];
  worstTopic: string | null;
  /** Số buổi điểm danh 30 ngày: có mặt (kể cả trễ) / tổng buổi đã điểm danh; null = không có dữ liệu. */
  attendance: { attended: number; total: number; absent: number } | null;
  phone: string;
  siteUrl: string;
}

export function buildParentDigest(d: DigestInput): string {
  const lines: string[] = [`Chào phụ huynh em ${d.studentName}. Thầy gửi tóm tắt việc học của con trên ThachLab:`, ""];
  const latest = d.points[d.points.length - 1];
  if (latest) {
    const prev = d.points.length > 1 ? d.points[d.points.length - 2] : null;
    let line = `• Bài gần nhất: ${scoreText(latest.score)}/10 (${gradeBand(latest.score).label}), ${dayMonth(new Date(latest.at))} — ${latest.examTitle}.`;
    if (prev) {
      const delta = Math.round((latest.score - prev.score) * 100) / 100;
      line += delta === 0 ? " Bằng bài trước." : ` ${delta > 0 ? "Tăng" : "Giảm"} ${scoreText(Math.abs(delta))} điểm so với bài trước.`;
    }
    lines.push(line);
    const avg = Math.round((d.points.reduce((a, p) => a + p.score, 0) / d.points.length) * 10) / 10;
    lines.push(`• Điểm trung bình ${d.points.length} bài: ${scoreText(avg)}.`);
  } else {
    lines.push("• Con chưa làm bài kiểm tra nào trên web; khi có bài, thầy sẽ báo điểm.");
  }
  if (d.attendance && d.attendance.total > 0) {
    lines.push(
      `• Đi học 30 ngày gần đây: ${d.attendance.attended}/${d.attendance.total} buổi` +
        (d.attendance.absent > 0 ? ` (vắng không phép ${d.attendance.absent}).` : "."),
    );
  }
  if (d.worstTopic) lines.push(`• Phần cần ôn thêm: ${d.worstTopic}. Phụ huynh có thể hỏi con phần này khó ở chỗ nào, rồi cùng con xem lại một câu.`);
  lines.push("", `Xem chi tiết (cần đăng nhập): ${d.siteUrl}/phu-huynh`);
  if (d.phone) lines.push(`Cần trao đổi, phụ huynh gọi hoặc nhắn thầy số ${d.phone}.`);
  return lines.join("\n");
}
