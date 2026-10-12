"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { ClipboardCheck } from "lucide-react";
import Button from "@/components/ui/Button";
import EntryDiagnosticQuiz from "@/components/results/EntryDiagnosticQuizLazy";
import { fetchQuestionTopics, type QuestionTopic } from "@/services/analytics";
import { fetchMyRegistrations } from "@/services/thpt-courses";
import { DIAGNOSTIC_MAX_TOPICS, fetchDiagnostic, type DiagnosticStatus } from "@/services/diagnostic";

/**
 * Kiểm tra đầu vào cho em vào lớp trễ (thầy chốt 12/10/2026). Chỉ hiện với em có đăng ký `joined_late`
 * (đang bù bài hoặc đã vào lớp) và có bài lớp đã học trước khi em vào.
 *  - viewer "student", chưa làm: thẻ mời, bấm là làm (không bắt buộc — G/động lực nội tại, không khoá tính năng nào).
 *  - viewer "student", đã làm: không hiện gì (mục phụ đạo đã nằm ở khối "Phụ đạo").
 *  - viewer "parent": chưa làm → một dòng nhắc nhẹ; đã làm → kết quả từng bài, giọng báo tin chứ không chấm điểm.
 */
export default function EntryDiagnosticCard({ studentId, viewer }: { studentId: string; viewer: "student" | "parent" }) {
  const [scope, setScope] = useState<number[] | null>(null);
  const [status, setStatus] = useState<DiagnosticStatus | null>(null);
  const [topics, setTopics] = useState<QuestionTopic[]>([]);
  const [open, setOpen] = useState(false);

  const load = useCallback(() => {
    fetchDiagnostic(studentId).then(setStatus).catch(() => setStatus(null));
  }, [studentId]);

  useEffect(() => {
    let cancelled = false;
    fetchMyRegistrations()
      .then((rows) => {
        if (cancelled) return;
        const reg = rows.find(
          (r) => r.student_id === studentId && r.joined_late && (r.status === "catchup" || r.status === "active"),
        );
        // Bài gần nhất trước (catchup_topic_ids đã sắp theo thứ tự đó), bài đã bù nối sau.
        const ids = reg ? [...new Set([...reg.catchup_topic_ids, ...reg.catchup_done_topic_ids])] : [];
        setScope(ids.slice(0, DIAGNOSTIC_MAX_TOPICS));
      })
      .catch(() => setScope([]));
    load();
    return () => {
      cancelled = true;
    };
  }, [studentId, load]);

  useEffect(() => {
    if (status?.done || (scope && scope.length > 0)) fetchQuestionTopics().then(setTopics).catch(() => setTopics([]));
  }, [status?.done, scope]);

  const names = useMemo(() => new Map(topics.map((t) => [t.id, t.name])), [topics]);

  if (!status || scope === null) return null;

  if (status.done) {
    if (viewer !== "parent") return null;
    const rows = status.perTopic ?? [];
    return (
      <section className="rounded-2xl border border-line bg-panel p-4 sm:p-5">
        <div className="flex items-center gap-2">
          <ClipboardCheck size={18} className="text-primary" />
          <h2 className="font-display font-bold text-ink">Kiểm tra đầu vào của con</h2>
        </div>
        <p className="mt-2 text-sm text-ink">
          {status.needCount
            ? `Có ${status.needCount} bài cần củng cố. Con đã được mở sẵn mục phụ đạo, có thể đăng ký buổi ngay.`
            : "Nền tảng của con ổn, chưa có phần nào cần phụ đạo gấp."}
        </p>
        <ul className="mt-3 space-y-1.5">
          {rows.map((r) => {
            const wrong = r.total - r.correct;
            const weak = r.total >= 2 && wrong >= 2 && (wrong * 100) / r.total >= 60;
            return (
              <li key={r.topicId} className="flex items-center justify-between gap-3 text-sm text-ink">
                <span className="min-w-0">{names.get(r.topicId) ?? "Bài đã học"}</span>
                <span className={`shrink-0 font-semibold ${weak ? "text-amber-700" : "text-emerald-700"}`}>
                  {weak ? "Cần củng cố" : "Ổn"} · {r.correct}/{r.total}
                </span>
              </li>
            );
          })}
        </ul>
      </section>
    );
  }

  if (scope.length === 0) return null;

  if (viewer === "parent") {
    return (
      <section className="rounded-2xl border border-line bg-panel p-4 sm:p-5">
        <div className="flex items-center gap-2">
          <ClipboardCheck size={18} className="text-primary" />
          <h2 className="font-display font-bold text-ink">Kiểm tra đầu vào</h2>
        </div>
        <p className="mt-2 text-sm text-ink">
          Con vào lớp sau khai giảng nên có một bài kiểm tra đầu vào ngắn (khoảng 10 phút, không tính điểm) để biết con cần kèm phần nào. Con chưa làm. Phụ huynh nhắc con mở trang chủ của con để làm.
        </p>
      </section>
    );
  }

  return (
    <section className="rounded-2xl border border-line bg-panel p-4 sm:p-5">
      <div className="flex items-center gap-2">
        <ClipboardCheck size={18} className="text-primary" />
        <h2 className="font-display font-bold text-ink">Kiểm tra đầu vào</h2>
      </div>
      <p className="mt-2 text-sm text-ink">
        Em vào lớp sau nên chưa có dữ liệu để biết em cần kèm phần nào. Làm bài này khoảng 10 phút, không tính điểm, không xếp hạng.
      </p>
      <Button onClick={() => setOpen(true)} className="mt-3 min-h-11 w-full sm:w-auto">
        Làm kiểm tra đầu vào
      </Button>
      {open && (
        <EntryDiagnosticQuiz
          studentId={studentId}
          topicIds={scope}
          topicNames={names}
          onClose={() => setOpen(false)}
          onSubmitted={load}
        />
      )}
    </section>
  );
}
