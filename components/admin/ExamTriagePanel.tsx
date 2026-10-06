"use client";

import ContentHtml from "@/components/exams/ContentHtmlLazy";
import type { ExamQuestion } from "@/features/exams/types";
import type { TriageResult } from "@/services/exam-triage";

const REASON: Record<string, string> = {
  figure: "Thiếu hình",
  context: "Phụ thuộc câu khác",
};

/**
 * Ba nhóm câu của đề: ổn (đăng ngay) · trùng (tự loại) · cần duyệt (thiếu hình / phụ thuộc câu khác,
 * mặc định KHÔNG đăng, tick từng câu để vẫn đăng). Câu lỗi không bao giờ chặn nhóm câu ổn.
 */
export function ExamTriagePanel({
  questions,
  triage,
  include,
  onToggle,
}: {
  questions: ExamQuestion[];
  triage: TriageResult;
  include: Set<number>;
  onToggle: (index: number, on: boolean) => void;
}) {
  const { ok, duplicates, review } = triage;
  if (!questions.length) return null;
  return (
    <div className="space-y-3 text-xs">
      <div className="rounded-xl border border-emerald-500/30 bg-emerald-500/10 p-3 text-emerald-100">
        <b>{ok.length}</b> câu ổn sẽ được đăng
        {duplicates.length > 0 && <> · đã loại <b>{duplicates.length}</b> câu trùng</>}
        {review.length > 0 && <> · <b>{review.length}</b> câu cần duyệt (bên dưới, không đăng nếu không tick)</>}.
      </div>

      {review.length > 0 && (
        <div className="space-y-2 rounded-xl border border-red-500/40 bg-red-500/10 p-3">
          <p className="font-semibold text-red-200">Câu cần duyệt — đang để riêng, chưa vào đề</p>
          <p className="text-red-100/80">
            Chèn lại hình / chép đủ dữ kiện ở file gốc rồi tải lại, hoặc tick “Vẫn đăng” nếu câu thật ra không cần hình.
          </p>
          <ul className="space-y-2">
            {review.map(({ index, reasons }) => (
              <li key={index} className="rounded-lg border border-white/10 bg-black/20 p-2">
                <label className="mb-1 flex cursor-pointer items-center gap-2 text-red-100">
                  <input type="checkbox" checked={include.has(index)} onChange={(e) => onToggle(index, e.target.checked)} />
                  <span className="font-semibold">Câu {index + 1}</span>
                  {reasons.map((r) => (
                    <span key={r} className="rounded bg-red-500/30 px-1.5">{REASON[r]}</span>
                  ))}
                  <span className="ml-auto text-slate-300">Vẫn đăng</span>
                </label>
                <ContentHtml html={questions[index].question} className="max-h-40 overflow-y-auto text-slate-200" />
              </li>
            ))}
          </ul>
        </div>
      )}

      {duplicates.length > 0 && (
        <details className="rounded-xl border border-amber-500/30 bg-amber-500/10 p-3 text-amber-100">
          <summary className="cursor-pointer font-semibold">Đã loại {duplicates.length} câu trùng (bấm để xem)</summary>
          <ul className="mt-2 space-y-1">
            {duplicates.map((d) => (
              <li key={d.index}>
                Câu {d.index + 1} trùng câu {d.of + 1}
              </li>
            ))}
          </ul>
        </details>
      )}
    </div>
  );
}
