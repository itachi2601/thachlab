"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { ChevronRight, Target } from "lucide-react";
import Badge from "@/components/ui/Badge";
import { MASTERY_ICON, MASTERY_LABEL, MASTERY_TONE, fetchMyWeakestTopics, type WeakTopic } from "@/services/mastery";

/**
 * Thẻ "3 kỹ năng yếu nhất" ở trang chủ học sinh (N3: tối đa 3 mục, một việc để làm).
 * Mỗi dòng: nhãn bằng chữ + icon (không chỉ màu), tên YCCĐ, bài chứa nó, % đúng; bấm → bài đó
 * (thẻ mastery cuối bài có nút "Luyện 10 câu phần này"). Không có dữ liệu / RPC lỗi → ẩn hẳn.
 */
export default function WeakestSkillsCard() {
  const [items, setItems] = useState<WeakTopic[]>([]);
  useEffect(() => {
    fetchMyWeakestTopics(3).then(setItems).catch(() => setItems([]));
  }, []);
  if (items.length === 0) return null;
  return (
    <section className="rounded-2xl border border-amber-400/25 bg-gradient-to-r from-amber-500/10 to-transparent p-4 sm:p-5">
      <div className="flex items-center gap-2">
        <Target size={18} className="text-amber-300" />
        <h2 className="font-display font-bold text-white">3 kỹ năng em nên luyện trước</h2>
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
    </section>
  );
}
