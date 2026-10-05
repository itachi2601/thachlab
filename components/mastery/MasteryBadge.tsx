import { MASTERY_ICON, MASTERY_LABEL, type MasteryLevel } from "@/services/mastery";

/**
 * Icon nhỏ ✅🟡🔴⚪ cạnh tên bài trong danh sách bài của chương (app/lop-hoc/page.tsx).
 * `level` undefined = chưa tải xong / chưa đăng nhập → không hiện gì (không chiếm chỗ,
 * tránh nhấp nháy layout trong lúc RPC đang chạy).
 */
export default function MasteryBadge({ level, showLabel = false }: { level: MasteryLevel | undefined; showLabel?: boolean }) {
  if (!level) return null;
  // showLabel: chữ cạnh icon — màu không phải kênh duy nhất truyền nghĩa (nhãn bằng chữ, mục C4 đề xuất trang chương).
  if (showLabel) {
    return (
      <span className={`class-mastery class-mastery--text is-${level}`}>
        <span aria-hidden>{MASTERY_ICON[level]}</span> {MASTERY_LABEL[level]}
      </span>
    );
  }
  return (
    <span
      className="class-mastery"
      title={MASTERY_LABEL[level]}
      aria-label={`Mức độ thành thạo: ${MASTERY_LABEL[level]}`}
      style={{ marginLeft: 6, fontSize: "0.9em" }}
    >
      {MASTERY_ICON[level]}
    </span>
  );
}
