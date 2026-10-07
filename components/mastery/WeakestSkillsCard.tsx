"use client";

import { useEffect, useState, type ComponentProps } from "react";
import dynamic from "next/dynamic";
import Link from "next/link";
import { ChevronRight, Target, Zap } from "lucide-react";
import Badge from "@/components/ui/Badge";
import { LazyErrorBoundary } from "@/components/ui/LazyErrorBoundary";
import { fetchLessonsStatic } from "@/services/static-content";
import { MASTERY_ICON, MASTERY_LABEL, MASTERY_TONE, fetchMyWeakestTopics, type WeakTopic } from "@/services/mastery";

// Modal luyện: cùng chunk lazy với thẻ mastery ở trang bài (perf4) — chỉ tải khi bấm nút, có boundary.
const PracticeModalLazy = dynamic(() => import("@/components/mastery/TopicPracticeModal"), {
  ssr: false,
  loading: () => null,
});

function PracticeModal(props: ComponentProps<typeof PracticeModalLazy>) {
  return (
    <LazyErrorBoundary
      fallback={
        <div role="alertdialog" className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4">
          <div className="max-w-sm rounded-2xl border border-white/10 bg-panel p-5 text-center text-sm text-slate-300">
            <p>Không tải được phần luyện tập (có thể do mạng chập chờn). Thử tải lại trang.</p>
            <button
              type="button"
              onClick={props.onClose}
              className="mt-3 min-h-11 rounded-full border border-white/15 px-4 text-xs font-semibold text-white hover:border-white/30"
            >
              Đóng
            </button>
          </div>
        </div>
      }
    >
      <PracticeModalLazy {...props} />
    </LazyErrorBoundary>
  );
}

/**
 * Thẻ "3 kỹ năng yếu nhất" ở trang chủ học sinh (N3: tối đa 3 mục, một việc để làm). Nền panel + nút viền
 * (7/10/2026, B2): nút nền đặc duy nhất của trang là ở thẻ "Hôm nay em làm gì".
 * Mỗi dòng: nhãn bằng chữ + icon (không chỉ màu), tên YCCĐ, bài chứa nó, % đúng; bấm → bài đó
 * (thẻ mastery cuối bài có nút "Luyện 10 câu phần này"). Nút "Luyện nhanh 10 câu" (M2, GĐ 2.6) mở
 * thẳng modal luyện cho kỹ năng yếu nhất: 10 câu, từng câu một, ghi phiên luyện như mọi lượt luyện (D2, N1). Không có dữ liệu / RPC lỗi → ẩn hẳn.
 */
export default function WeakestSkillsCard() {
  const [items, setItems] = useState<WeakTopic[]>([]);
  const [run, setRun] = useState<{ lessonId: number; examIds: number[]; topicName: string } | null>(null);
  const [starting, setStarting] = useState(false);
  const [startError, setStartError] = useState(false);
  useEffect(() => {
    fetchMyWeakestTopics(3).then(setItems).catch(() => setItems([]));
  }, []);
  if (items.length === 0) return null;
  const weakest = items[0];

  // Danh mục bài lấy từ bản tĩnh (đã cache ở trang chủ) — không thêm lượt gọi Supabase.
  async function startQuick() {
    setStarting(true);
    setStartError(false);
    try {
      const lessons = await fetchLessonsStatic();
      const lesson = lessons.find((l) => l.id === weakest.lessonId);
      const examIds = lesson ? Array.from(new Set(lesson.itemRefs.flatMap((r) => r.exam_ids))) : [];
      if (examIds.length === 0) {
        setStartError(true);
        return;
      }
      setRun({ lessonId: weakest.lessonId, examIds, topicName: weakest.topicName });
    } catch {
      setStartError(true);
    } finally {
      setStarting(false);
    }
  }
  return (
    <section className="rounded-2xl border border-white/10 bg-panel p-4 sm:p-5">
      <div className="flex items-center gap-2">
        <Target size={18} className="text-amber-300" />
        <h2 className="font-display font-bold text-white">Kỹ năng cần luyện thêm</h2>
      </div>
      <ul className="mt-3 space-y-2">
        {items.map((t) => (
          <li key={t.topicId}>
            <Link
              href={`/lop-hoc/bai/?id=${t.lessonId}`}
              className="flex min-h-11 items-center justify-between gap-3 rounded-xl border border-white/10 bg-black/15 p-3 hover:bg-black/25"
            >
              <span className="min-w-0">
                <strong className="block text-sm text-white">{t.topicName}</strong>
                <small className="block truncate text-[13px] text-slate-400">
                  {t.lessonTitle} · đúng {t.pct}%
                </small>
              </span>
              <span className="flex shrink-0 items-center gap-2">
                <Badge tone={MASTERY_TONE[t.level]}>
                  <span aria-hidden>{MASTERY_ICON[t.level]}</span> {MASTERY_LABEL[t.level]}
                </Badge>
                <ChevronRight size={16} className="text-slate-400" />
              </span>
            </Link>
          </li>
        ))}
      </ul>
      <button
        type="button"
        onClick={startQuick}
        disabled={starting}
        className="mt-3 flex min-h-12 w-full items-center justify-center gap-2 rounded-xl border border-amber-400/50 px-4 text-sm font-bold text-amber-200 hover:bg-amber-500/10 disabled:opacity-60"
      >
        <Zap size={16} aria-hidden />
        {starting ? "Đang chuẩn bị…" : "Luyện nhanh 10 câu"}
        <span className="font-medium opacity-80">· khoảng 5 phút</span>
      </button>
      <p className="mt-1.5 text-[13px] text-slate-400">
        {startError
          ? "Chưa mở được bài luyện này. Em bấm vào kỹ năng ở trên để luyện trong bài nhé."
          : `Luyện kỹ năng yếu nhất: ${weakest.topicName}`}
      </p>
      {run && (
        <PracticeModal
          lessonId={run.lessonId}
          examIds={run.examIds}
          topicName={run.topicName}
          count={10}
          onClose={() => setRun(null)}
          onFinished={() => fetchMyWeakestTopics(3).then(setItems).catch(() => {})}
        />
      )}
    </section>
  );
}
