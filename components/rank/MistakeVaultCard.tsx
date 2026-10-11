"use client";

import { useEffect, useState } from "react";
import { Sparkles, AlertCircle, CheckCircle2, ChevronRight } from "lucide-react";
import Button from "@/components/ui/Button";
import { fetchMistakeStats, type MistakeStats } from "@/services/mistakes";
import MistakeReviewModal from "@/components/rank/MistakeReviewModal";

export default function MistakeVaultCard() {
  const [stats, setStats] = useState<MistakeStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [openModal, setOpenModal] = useState(false);

  function reloadStats() {
    fetchMistakeStats().then((data) => {
      setStats(data);
      setLoading(false);
    });
  }

  useEffect(() => {
    reloadStats();
  }, []);

  if (loading || !stats || (stats.total_active === 0 && stats.cleared_count === 0)) {
    return null;
  }

  return (
    <>
      <div className="rounded-3xl border border-line bg-panel p-5 shadow-sm transition hover:border-line-strong">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-2xl bg-amber-500/10 text-amber-500">
              <Sparkles className="h-5 w-5" />
            </span>
            <div>
              <h3 className="text-sm font-semibold text-ink">Kho bẫy câu sai & Xoá bẫy cách quãng</h3>
              <p className="text-xs text-muted">
                {stats.due_count > 0
                  ? `Có ${stats.due_count} câu đã đến hạn ôn tập để nhận +RP thưởng`
                  : stats.total_active > 0
                  ? `Đang theo dõi ${stats.total_active} câu — chưa câu nào đến hạn, em vẫn luyện nhẹ được xen cả câu đã làm đúng`
                  : `Đã chinh phục thành công ${stats.cleared_count} câu bẫy!`}
              </p>
            </div>
          </div>

          <Button
            type="button"
            variant={stats.due_count > 0 ? "primary" : "outline"}
            onClick={() => setOpenModal(true)}
            className="min-h-11 shrink-0 px-4 text-xs font-semibold"
          >
            {stats.due_count > 0 ? `Xoá bẫy ngay (${stats.due_count})` : "Luyện nhẹ 5 câu"}
            <ChevronRight className="ml-1.5 h-4 w-4" />
          </Button>
        </div>

        {/* Stats indicators */}
        <div className="mt-4 grid grid-cols-3 gap-2 border-t border-line/60 pt-3 text-center sm:text-left">
          <div className="rounded-xl bg-panel-soft/60 px-3 py-2">
            <p className="text-[11px] font-medium text-muted">Đến hạn ôn</p>
            <p className={`text-base font-bold ${stats.due_count > 0 ? "text-amber-500" : "text-ink"}`}>
              {stats.due_count}
            </p>
          </div>
          <div className="rounded-xl bg-panel-soft/60 px-3 py-2">
            <p className="text-[11px] font-medium text-muted">Đang theo dõi</p>
            <p className="text-base font-bold text-ink">{stats.total_active}</p>
          </div>
          <div className="rounded-xl bg-panel-soft/60 px-3 py-2">
            <p className="text-[11px] font-medium text-muted">Đã xoá bẫy</p>
            <p className="text-base font-bold text-emerald-500">{stats.cleared_count}</p>
          </div>
        </div>

        {stats.weak_topics && stats.weak_topics.length > 0 && (
          <div className="mt-3 flex flex-wrap items-center gap-1.5 text-[11px] text-muted">
            <span className="font-medium text-ink">Chủ đề hay vấp:</span>
            {stats.weak_topics.map((t) => (
              <span key={t.topic_id} className="rounded-md border border-line bg-panel-soft px-2 py-0.5">
                {t.name} ({t.count})
              </span>
            ))}
          </div>
        )}
      </div>

      {openModal && (
        <MistakeReviewModal
          onClose={() => setOpenModal(false)}
          onFinished={() => {
            reloadStats();
          }}
        />
      )}
    </>
  );
}
