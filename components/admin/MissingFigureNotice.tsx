"use client";

import { missingFigureWarning } from "@/services/question-figures";
import { contextDependencyWarning } from "@/services/question-context";

/**
 * Khung đỏ: câu nhắc đồ thị/hình vẽ nhưng không có ảnh. Nút Đăng bị khoá cho tới khi
 * thầy tick "đã xem" — để không bao giờ đăng nhầm một đề mất hình mà không biết.
 */
export function MissingFigureNotice({
  nums,
  dependentNums = [],
  ack,
  onAck,
}: {
  nums: number[];
  /** Câu dựa vào "câu trên" — mất ngữ cảnh khi đảo/bốc ngẫu nhiên. */
  dependentNums?: number[];
  ack: boolean;
  onAck: (v: boolean) => void;
}) {
  if (!nums.length && !dependentNums.length) return null;
  return (
    <div className="space-y-2 rounded-xl border border-red-500/40 bg-red-500/10 p-3 text-xs text-red-100">
      {nums.length > 0 && (
        <>
          <p className="font-semibold text-red-200">Thiếu hình ở {nums.length} câu</p>
          <p>{missingFigureWarning(nums)}</p>
        </>
      )}
      {dependentNums.length > 0 && (
        <>
          <p className="font-semibold text-red-200">{dependentNums.length} câu phụ thuộc câu khác</p>
          <p>{contextDependencyWarning(dependentNums)}</p>
        </>
      )}
      <label className="flex cursor-pointer items-start gap-2 text-red-100">
        <input type="checkbox" checked={ack} onChange={(e) => onAck(e.target.checked)} className="mt-0.5" />
        <span>Tôi đã xem từng câu trên: câu nào cần hình đã chèn lại, câu nào phụ thuộc đã chép đủ dữ kiện, câu còn lại không cần. Cho phép Đăng.</span>
      </label>
    </div>
  );
}
