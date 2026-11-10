"use client";

import { useCallback, useState } from "react";
import { ChevronDown } from "lucide-react";
import ContentHtml from "@/components/exams/ContentHtml";
import SimilarBankPractice from "@/components/lessons/SimilarBankPractice";
import VariantPractice from "@/components/lessons/VariantPractice";
import StepwiseSolution from "@/components/lessons/StepwiseSolution";
import GiaiCungHinh, { HinhDe } from "@/components/lessons/cong-cu/GiaiCungHinh";
import { TomDeKhung } from "@/components/lessons/TomDe";
import type { LessonWorkedQuestion } from "@/features/lessons/types";

/** Số dạng từ nhãn "Dạng N · Mức · tên" (khớp question_dang.dang_label phía RPC). */
function dangNumber(label?: string): number | null {
  const m = /^\s*Dạng\s*(\d+)/.exec(label ?? "");
  return m ? Number(m[1]) : null;
}

/** Dạng có cấu trúc: đề + mô phỏng → (HS chọn) phân tích đề → (HS chọn) lời giải đầy đủ → làm bài tương tự.
 *  Bản cũ có `hints_html` (gợi ý theo tầng) vẫn hiển thị như trước. Dạng cũ chỉ có body_html ở dưới. */
function StructuredBody({ q, color, lessonId }: { q: LessonWorkedQuestion; color: string; lessonId?: number }) {
  const hints = q.hints_html ?? [];
  const [shown, setShown] = useState(0);
  const [analysed, setAnalysed] = useState(false);
  const [solved, setSolved] = useState(false);
  const [jump, setJump] = useState<{ idx: number; n: number } | null>(null);
  const [allOpen, setAllOpen] = useState(false); // tự giải từng bước: bài tương tự chỉ hiện khi đã mở hết các bước
  const markAllOpen = useCallback(() => setAllOpen(true), []);
  const [meoOpen, setMeoOpen] = useState(false); // 💡 Mẹo nhìn: gập sẵn, chỉ có sau lời giải (N6, B4)
  const [meoSeen, setMeoSeen] = useState(false); // đã từng mở mẹo — ghi kèm lượt bài tương tự để đo (chặng 5)
  const hasAnalysis = !!q.analysis_html;
  const stepwise = !!q.buoc?.length; // tự giải từng bước (9/10/2026)
  const dangNo = dangNumber(q.label);
  const canSimilar = !!q.topic_id || (!!lessonId && dangNo != null);
  return (
    <div className="space-y-3">
      {q.nhan_dang && (
        <p className="bt-nhan-dang" style={{ borderColor: color }}>
          <ContentHtml html={q.nhan_dang} className="inline" />
        </p>
      )}
      <ContentHtml html={q.problem_html ?? ""} className="block leading-relaxed" />
      {q.cong_cu?.de && <HinhDe tool={q.cong_cu} />}
      <p className="text-xs text-muted">
        {hasAnalysis ? "Tự thử giải trên giấy trước, kẹt thì mở phân tích đề." : "Tự thử giải trên giấy trước, kẹt thì mở từng gợi ý."}
      </p>
      {hasAnalysis && analysed && (
        <div className="rounded-lg border border-line p-3">
          <p className="mb-1 text-xs font-semibold" style={{ color }}>
            Phân tích đề
          </p>
          <ContentHtml html={q.analysis_html ?? ""} className="block leading-relaxed" />
        </div>
      )}
      {!hasAnalysis &&
        hints.slice(0, shown).map((h, i) => (
          <div key={i} className="rounded-lg border border-line p-3">
            <p className="mb-1 text-xs font-semibold" style={{ color }}>
              Gợi ý {i + 1}/{hints.length}
            </p>
            <ContentHtml html={h} className="block leading-relaxed" />
          </div>
        ))}
      <div className="flex flex-wrap gap-2">
        {hasAnalysis && !analysed && (
          <button type="button" className="lesson-btn-ghost" onClick={() => setAnalysed(true)}>
            Phân tích đề
          </button>
        )}
        {!hasAnalysis && shown < hints.length && (
          <button type="button" className="lesson-btn-ghost" onClick={() => setShown((n) => n + 1)}>
            Gợi ý {shown + 1}/{hints.length}
          </button>
        )}
        {!solved && (
          <button type="button" className="lesson-btn-ghost" onClick={() => setSolved(true)}>
            {stepwise ? "Giải từng bước" : "Xem lời giải đầy đủ"}
          </button>
        )}
      </div>
      {solved && (
        <>
          {stepwise && q.cong_cu ? (
            <GiaiCungHinh q={q} tool={q.cong_cu} color={color} jump={jump} onAllOpen={markAllOpen} />
          ) : stepwise ? (
            <TomDeKhung q={q}>
              <StepwiseSolution q={q} color={color} jump={jump} onAllOpen={markAllOpen} />
            </TomDeKhung>
          ) : (
            <ContentHtml html={q.solution_html ?? ""} className="block leading-relaxed" />
          )}
          {q.meo && (allOpen || !stepwise) && (
            <div className="bt-meo">
              <button type="button" className="bt-meo-head" aria-expanded={meoOpen} onClick={() => { setMeoOpen((o) => !o); setMeoSeen(true); }}>
                <span>💡 Mẹo nhìn: {q.meo.ten}</span>
                <ChevronDown size={16} className={meoOpen ? "rotate-180" : ""} />
              </button>
              {meoOpen && (
                <div className="bt-meo-body">
                  <p className="bt-meo-dk">
                    ⚠ <ContentHtml html={q.meo.dieu_kien} className="inline" />
                  </p>
                  <ContentHtml html={q.meo.html} className="block leading-relaxed" />
                </div>
              )}
            </div>
          )}
          {q.bien_the && (allOpen || !stepwise) && (
            <VariantPractice bt={q.bien_the} color={color} stepTitles={stepwise ? q.buoc!.map((b) => b.tieu_de) : undefined} defaultStep={q.go_roi?.buoc_hay_sai} onGoRoi={(idx) => setJump((j) => ({ idx, n: (j?.n ?? 0) + 1 }))} />
          )}
          {canSimilar && (allOpen || !stepwise) ? (
            <SimilarBankPractice
              lessonId={lessonId}
              dangNo={dangNo ?? undefined}
              topicId={q.topic_id}
              form={q.form}
              meo={{ co: !!q.meo, mo: meoSeen }}
              color={color}
              stepTitles={stepwise ? q.buoc!.map((b) => b.tieu_de) : undefined}
              defaultStep={q.go_roi?.buoc_hay_sai}
              onGoRoi={(idx) => setJump((j) => ({ idx, n: (j?.n ?? 0) + 1 }))}
            />
          ) : null}
        </>
      )}
    </div>
  );
}

/** Các "dạng bài" (bài tập mẫu): hàng thu/mở, tên dạng hiện rõ, lời giải mở ngay dưới hàng đó. */
export default function WorkedQuestionsGrid({
  questions,
  color = "#8B5CF6",
  lessonId,
}: {
  questions: LessonWorkedQuestion[];
  color?: string;
  /** Bài chứa các dạng — để "Làm bài tương tự" lấy đúng câu đã gán dạng (question_dang). */
  lessonId?: number;
}) {
  const [openIdx, setOpenIdx] = useState<Set<number>>(() => new Set(questions.length ? [0] : []));

  function toggle(idx: number) {
    setOpenIdx((current) => {
      const next = new Set(current);
      if (next.has(idx)) next.delete(idx);
      else next.add(idx);
      return next;
    });
  }

  if (questions.length === 0) return null;

  return (
    <div className="lesson-worked">
      {questions.map((q, idx) => {
        const open = openIdx.has(idx);
        return (
          <div key={idx} className="lesson-worked-row">
            <button
              type="button"
              onClick={() => toggle(idx)}
              aria-expanded={open}
              className="lesson-worked-head"
            >
              <span
                className="lesson-worked-num"
                style={open ? { borderColor: color, color } : undefined}
              >
                {idx + 1}
              </span>
              <span className="lesson-worked-label">{q.label || `Ví dụ ${idx + 1}`}</span>
              <ChevronDown size={16} className={open ? "rotate-180" : ""} />
            </button>
            {open && (
              <div className="lesson-worked-body exam-paper">
                {q.problem_html && q.solution_html ? (
                  <StructuredBody q={q} color={color} lessonId={lessonId} />
                ) : (
                  <ContentHtml html={q.body_html} className="block leading-relaxed" />
                )}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
