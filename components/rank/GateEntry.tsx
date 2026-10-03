"use client";

import { useState } from "react";
import { ClipboardCheck } from "lucide-react";
import Button from "@/components/ui/Button";
import { formatRp, type RankNext } from "@/features/rank/types";

function formatUntil(iso: string): string {
  return new Date(iso).toLocaleString("vi-VN", { hour: "2-digit", minute: "2-digit", day: "2-digit", month: "2-digit" });
}

/**
 * Cửa vào bài thi thăng hạng thích ứng ở "Điều kiện lên hạng": đủ RP + thiếu cửa → nút "Thi thăng hạng".
 * Chỉ là phần hiển thị; modal làm bài (GateQuizModal, tách lazy) do RankPage giữ để không bị gỡ khi trạng thái tải lại.
 * Quy tắc: N2 một nút chính, D2 nút ≥ 44px, M4 trạng thái chờ có chữ, L4 lời hướng việc tiếp theo.
 */
export default function GateEntry({ next, onStart }: { next: RankNext; onStart: () => void }) {
  const gate = next.gate;
  const [now] = useState(() => Date.now());
  if (!gate?.adaptive || gate.passed || gate.last_passed) return null;

  const waiting = gate.cooldown_until && new Date(gate.cooldown_until).getTime() > now;

  return (
    <div className="mt-4 rounded-xl border border-white/10 bg-white/[0.03] p-3 sm:p-4">
      {next.rp_needed > 0 ? (
        <p className="text-sm text-slate-300">
          Bài thi thăng hạng mở khi em đạt {formatRp(next.min_rp)} RP (còn {formatRp(next.rp_needed)} RP).
        </p>
      ) : waiting ? (
        <p className="text-base leading-relaxed text-slate-200">
          Đủ RP rồi, còn bài thi thăng hạng. Em thi lại được sau <b className="text-white">{formatUntil(gate.cooldown_until!)}</b> — lúc đó ôn lại chủ đề sai nhiều rồi thử tiếp.
        </p>
      ) : gate.can_start ? (
        <>
          <p className="text-base leading-relaxed text-slate-200">
            Đủ RP rồi, còn bài thi thăng hạng lên <b className="text-white">{next.name}</b>: {gate.quiz_count ?? 12} câu, độ khó tự điều chỉnh, đạt từ {gate.pass_pct ?? 70}%.
          </p>
          <Button onClick={onStart} className="mt-3 min-h-11 w-full sm:w-auto">
            <ClipboardCheck size={16} aria-hidden />
            {gate.open_attempt ? "Tiếp tục thi" : "Thi thăng hạng"}
          </Button>
        </>
      ) : (
        <p className="text-sm text-slate-300">Bài thi thăng hạng chưa mở cho khối của em lúc này — em hỏi giáo viên nhé.</p>
      )}
      {gate.attempts !== undefined && gate.attempts > 0 && !waiting && (
        <p className="mt-2 text-sm text-slate-400">Em đã thi {gate.attempts} lần ở bậc này.</p>
      )}
    </div>
  );
}
