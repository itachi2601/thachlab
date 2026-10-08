"use client";

import { useEffect, useState } from "react";
import { ChevronRight, Target } from "lucide-react";
import QuickPractice, { type QuickPracticeRequest } from "@/components/mastery/QuickPractice";
import { fetchMyWeakestTopics, type WeakTopic } from "@/services/mastery";

/**
 * Hàng "Dành cho em" đầu trang Luyện tập (thầy chốt 8/10/2026): tối đa 3 kỹ năng yếu nhất của em, bấm là luyện nhanh 10 câu
 * ngay tại trang. Cùng nguồn dữ liệu (get_my_weakest_topics) với thẻ "Hôm nay em làm gì" nên hai nơi không gợi hai việc khác nhau.
 * Không có dữ liệu / RPC lỗi → ẩn hẳn (N3); chế độ tự chọn bên dưới giữ nguyên.
 */
export default function ForYouRow() {
  const [items, setItems] = useState<WeakTopic[]>([]);
  const [request, setRequest] = useState<QuickPracticeRequest | null>(null);
  useEffect(() => {
    fetchMyWeakestTopics(3).then(setItems).catch(() => setItems([]));
  }, []);
  if (items.length === 0) return null;
  return (
    <section className="mt-5 rounded-2xl border border-white/10 bg-panel p-4" aria-label="Dành cho em">
      <h2 className="flex items-center gap-2 font-display font-bold text-white">
        <Target size={18} className="text-amber-300" aria-hidden />
        Dành cho em
      </h2>
      <p className="mt-1 text-[13px] text-slate-400">Những kỹ năng em đang cần luyện thêm, mỗi lần 10 câu, khoảng 5 phút.</p>
      <ul className="mt-3 space-y-2">
        {items.map((t) => (
          <li key={t.topicId}>
            <button
              type="button"
              onClick={() => setRequest({ lessonId: t.lessonId, topicName: t.topicName })}
              className="flex min-h-14 w-full items-center justify-between gap-3 rounded-xl border border-white/10 bg-white/5 p-3 text-left hover:bg-white/10"
            >
              <span className="min-w-0">
                <strong className="block text-sm text-white">{t.topicName}</strong>
                <small className="block truncate text-[13px] text-slate-400">
                  {t.lessonTitle} · đúng {t.pct}%
                </small>
              </span>
              <ChevronRight size={16} className="shrink-0 text-slate-500" aria-hidden />
            </button>
          </li>
        ))}
      </ul>
      <QuickPractice
        request={request}
        onClose={() => setRequest(null)}
        onFinished={() => fetchMyWeakestTopics(3).then(setItems).catch(() => undefined)}
        onUnavailable={(req) => {
          setRequest(null);
          window.location.assign(`/lop-hoc/bai?id=${req.lessonId}`);
        }}
      />
    </section>
  );
}
