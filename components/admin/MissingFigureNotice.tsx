"use client";

import { missingFigureWarning } from "@/services/question-figures";

/**
 * Khung đỏ: câu nhắc đồ thị/hình vẽ nhưng không có ảnh. Nút Đăng bị khoá cho tới khi
 * thầy tick "đã xem" — để không bao giờ đăng nhầm một đề mất hình mà không biết.
 */
export function MissingFigureNotice({
  nums,
  ack,
  onAck,
}: {
  nums: number[];
  ack: boolean;
  onAck: (v: boolean) => void;
}) {
  if (!nums.length) return null;
  return (
    <div className="space-y-2 rounded-xl border border-red-500/40 bg-red-500/10 p-3 text-xs text-red-100">
      <p className="font-semibold text-red-200">Thiếu hình ở {nums.length} câu</p>
      <p>{missingFigureWarning(nums)}</p>
      <label className="flex cursor-pointer items-start gap-2 text-red-100">
        <input type="checkbox" checked={ack} onChange={(e) => onAck(e.target.checked)} className="mt-0.5" />
        <span>Tôi đã xem từng câu trên: câu nào cần hình đã chèn lại, câu còn lại không cần hình. Cho phép Đăng.</span>
      </label>
    </div>
  );
}
