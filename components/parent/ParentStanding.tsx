"use client";

import { useState } from "react";
import { fetchClassStanding, type ClassStanding } from "@/services/parent-view";
import { scoreText } from "@/lib/parent-format";

/**
 * Vị trí của con trong lớp — TUỲ CHỌN, mặc định đóng, tự phụ huynh mở (không đẩy thứ hạng lên mặt).
 * Nhiều phụ huynh muốn biết con so với lớp thế nào; cũng có người không muốn thấy. Nên cho họ chọn,
 * và nói bằng dải ("nhóm 25% đầu") + điểm trung bình lớp, không nói "hạng 32/40".
 * Lớp dưới 8 em có điểm thì không hiện gì: dải sẽ lộ ra con của ai.
 */
const MIN_CLASS = 8;

function sentence(s: ClassStanding): string {
  const ratio = s.rank / s.total;
  if (ratio <= 0.25) return "Con nằm trong nhóm 25% cao điểm nhất của lớp.";
  if (ratio <= 0.5) return "Con nằm ở nửa trên của lớp.";
  if (ratio <= 0.75) return "Con ở khoảng giữa của lớp.";
  return "Điểm của con đang dưới mức trung bình của lớp; thầy đang theo dõi và hỗ trợ thêm.";
}

export default function ParentStanding({ studentId, classId }: { studentId: string; classId: number }) {
  const [state, setState] = useState<"idle" | "loading" | "done">("idle");
  const [standing, setStanding] = useState<ClassStanding | null>(null);

  function onToggle(e: React.SyntheticEvent<HTMLDetailsElement>) {
    if (!e.currentTarget.open || state !== "idle") return;
    setState("loading");
    fetchClassStanding(studentId, classId)
      .then(setStanding)
      .finally(() => setState("done"));
  }

  return (
    <details onToggle={onToggle} className="mb-6 rounded-2xl border border-white/10 bg-panel p-5">
      <summary className="flex min-h-12 cursor-pointer items-center font-display font-semibold text-white">
        Xem con so với cả lớp (không bắt buộc)
      </summary>
      <div className="mt-3">
        {state === "loading" && <p className="text-slate-400">Đang tính…</p>}
        {state === "done" && (standing === null || standing.total < MIN_CLASS) && (
          <p className="parent-copy text-slate-400">
            Chưa đủ số bài kiểm tra của lớp để so sánh. Khi lớp có thêm bài, mục này sẽ hiện.
          </p>
        )}
        {state === "done" && standing !== null && standing.total >= MIN_CLASS && (
          <>
            <p className="parent-copy text-slate-200">{sentence(standing)}</p>
            <p className="parent-num mt-3 text-slate-300">
              Điểm trung bình của con: <b className="text-white">{scoreText(Math.round(standing.myAvg * 10) / 10)}</b> · Trung
              bình cả lớp: <b className="text-white">{scoreText(Math.round(standing.classAvg * 10) / 10)}</b>
            </p>
            <p className="parent-copy mt-3 text-slate-400">
              Tính từ các bài kiểm tra của lớp ({standing.total} em có điểm), không tính điểm thưởng. Mỗi em tiến bộ theo
              nhịp riêng — phụ huynh đối chiếu với con của hôm qua trước, rồi mới với lớp.
            </p>
          </>
        )}
      </div>
    </details>
  );
}
