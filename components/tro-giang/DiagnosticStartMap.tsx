"use client";

import { Map as MapIcon } from "lucide-react";
import {
  buildStartMap,
  levelOf,
  LEVEL_LABEL,
  type DiagnosticLevel,
  type DiagnosticTopicResult,
} from "@/services/diagnostic";

const LEVEL_TONE: Record<DiagnosticLevel, string> = {
  hieu_sai: "border-rose-400/40 bg-rose-500/10 text-rose-200",
  chua_biet: "border-amber-400/40 bg-amber-500/10 text-amber-200",
  chua_vung: "border-sky-400/40 bg-sky-500/10 text-sky-200",
  vung: "border-emerald-400/40 bg-emerald-500/10 text-emerald-200",
};

/**
 * "Phiếu xuất phát" của em mới vào cho trợ giảng/thầy: bỏ qua gì (đã vững), bắt đầu từ đâu, rồi đi tiếp thế nào.
 * Chỉ thầy/trợ giảng thấy (phụ huynh nhận kết quả đã cắt nhóm). Dữ liệu từ kiểm tra đầu vào (diagnostic_*).
 */
export default function DiagnosticStartMap({
  rows,
  topicName,
  defaultOpen = false,
}: {
  rows: DiagnosticTopicResult[];
  topicName: Map<number, string>;
  defaultOpen?: boolean;
}) {
  if (rows.length === 0) return null;
  const { skip, order } = buildStartMap(rows);
  const name = (id: number) => topicName.get(id) ?? `Bài #${id}`;
  const first = order[0];

  return (
    <details open={defaultOpen} className="mt-3 rounded-xl border border-white/10 bg-white/3 p-3">
      <summary className="flex min-h-11 cursor-pointer items-center gap-2 text-sm font-semibold text-slate-200">
        <MapIcon size={14} aria-hidden /> Phiếu xuất phát (kiểm tra đầu vào)
      </summary>
      <div className="mt-2 space-y-3 text-sm text-slate-300">
        {first ? (
          <p>
            <span className="font-semibold text-white">Bắt đầu từ: {name(first.topicId)}</span> · {LEVEL_LABEL[levelOf(first)]}
            {skip.length > 0 && (
              <span className="block text-xs text-slate-400">
                Gợi ý mở đầu: “Em làm tốt {name(skip[0].topicId)} rồi, mình qua {name(first.topicId)} nhé.”
              </span>
            )}
          </p>
        ) : (
          <p className="font-semibold text-white">Em đã vững các bài đã kiểm tra, không cần dạy lại.</p>
        )}

        {order.length > 0 && (
          <ol className="space-y-1.5">
            {order.map((r, i) => (
              <li key={r.topicId} className="flex flex-wrap items-center gap-x-2 gap-y-1">
                <span className="w-5 shrink-0 text-xs text-slate-500">{i + 1}.</span>
                <span className="min-w-0 flex-1">{name(r.topicId)}</span>
                <span className={`rounded-full border px-2 py-0.5 text-xs font-semibold ${LEVEL_TONE[levelOf(r)]}`}>
                  {LEVEL_LABEL[levelOf(r)]}
                </span>
                <span className="text-xs tabular-nums text-slate-500">
                  đúng {r.correct}/{r.total}
                  {r.probe ? " · bài dò nền" : ""}
                </span>
              </li>
            ))}
          </ol>
        )}

        {skip.length > 0 && (
          <div>
            <p className="text-xs font-semibold text-emerald-300">Bỏ qua, đã vững (chỉ ôn nhanh vài phút cho em vui):</p>
            <ul className="mt-1 space-y-0.5 text-xs text-slate-400">
              {skip.map((r) => (
                <li key={r.topicId}>{name(r.topicId)}</li>
              ))}
            </ul>
          </div>
        )}

        {order.some((r) => levelOf(r) === "hieu_sai") && (
          <p className="rounded-lg border border-rose-400/30 bg-rose-500/10 p-2 text-xs text-rose-100">
            “Hiểu chưa đúng” = em sai mà tự thấy chắc chắn. Đừng giảng ngay: cho em tự giải một câu của phần này trước, để em tự thấy chỗ lệch.
          </p>
        )}
      </div>
    </details>
  );
}
