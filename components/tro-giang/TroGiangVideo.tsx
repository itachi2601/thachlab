"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { ArrowLeft, Bookmark, Lightbulb, PenLine } from "lucide-react";
import { STATUS_META } from "@/lib/tro-giang/constants";
import { formatVnd } from "@/lib/tro-giang/format";
import {
  fetchTopicSuggestions,
  fetchVideoLedger,
  fetchVideoRates,
  type TaAssistant,
  type TaTopicSuggestion,
  type TaVideoLedgerRow,
  type TaVideoRates,
} from "@/lib/tro-giang/queries";

function currentMonthStr() {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-01`;
}

function sameMonth(dateStr: string, monthStr: string) {
  return dateStr.slice(0, 7) === monthStr.slice(0, 7);
}

/** Mốc thưởng lượt xem lấy từ ta_video_rates, không viết cứng ngưỡng trong code. */
function milestoneText(views: number, rates: TaVideoRates | null): string {
  if (!rates) return "";
  if (views >= rates.view_threshold_2)
    return `Đã đạt mốc ${rates.view_threshold_2.toLocaleString("vi-VN")} lượt xem — thưởng tối đa`;
  if (views >= rates.view_threshold_1)
    return `Đã đạt mốc ${rates.view_threshold_1.toLocaleString("vi-VN")} — còn ${(rates.view_threshold_2 - views).toLocaleString("vi-VN")} lượt nữa lên mốc cao`;
  return `Còn ${(rates.view_threshold_1 - views).toLocaleString("vi-VN")} lượt xem nữa đạt mốc thưởng đầu tiên`;
}

export default function TroGiangVideo({ assistant }: { assistant: TaAssistant }) {
  const [ledger, setLedger] = useState<TaVideoLedgerRow[] | null>(null);
  const [topics, setTopics] = useState<TaTopicSuggestion[] | null>(null);
  const [rates, setRates] = useState<TaVideoRates | null>(null);

  useEffect(() => {
    const month = currentMonthStr();
    fetchVideoLedger(assistant.id).then(setLedger).catch(() => setLedger([]));
    fetchTopicSuggestions(14).then(setTopics).catch(() => setTopics([]));
    fetchVideoRates(month).then(setRates).catch(() => setRates(null));
  }, [assistant.id]);

  const month = currentMonthStr();
  const thisMonth = (ledger ?? []).filter((v) => sameMonth(v.work_date, month));
  const sum = (pick: (v: TaVideoLedgerRow) => number) => thisMonth.reduce((acc, v) => acc + pick(v), 0);

  return (
    <div className="flex flex-col gap-6">
      <div>
        <Link href="/tro-giang" className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-400">
          <ArrowLeft size={14} />
          Trang chính
        </Link>
        <h1 className="mt-2 font-display text-2xl font-bold text-white">Video TikTok</h1>
        <p className="mt-1 text-sm text-slate-400">
          Mảng này trả riêng, không cộng vào giờ công lên lớp và không tính vào điểm hiệu suất.
        </p>
      </div>

      <section className="rounded-3xl border border-white/10 bg-[#0B1020] p-6">
        <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">Thu nhập mảng video tháng này</p>
        <p className="mt-1.5 font-mono text-3xl font-bold tabular-nums text-white">
          {formatVnd(sum((v) => v.total_pay))}
        </p>
        <div className="mt-4 grid grid-cols-3 gap-3 text-center">
          <div className="rounded-xl bg-white/5 p-3">
            <p className="text-[11px] font-semibold uppercase text-slate-400">Sản xuất</p>
            <p className="mt-1 font-mono text-sm font-bold tabular-nums text-slate-200">
              {formatVnd(sum((v) => v.production_pay))}
            </p>
          </div>
          <div className="rounded-xl bg-white/5 p-3">
            <p className="text-[11px] font-semibold uppercase text-slate-400">Lượt xem</p>
            <p className="mt-1 font-mono text-sm font-bold tabular-nums text-slate-200">
              {formatVnd(sum((v) => v.view_bonus))}
            </p>
          </div>
          <div className="rounded-xl bg-emerald-500/10 p-3">
            <p className="text-[11px] font-semibold uppercase text-emerald-300/80">Đăng ký</p>
            <p className="mt-1 font-mono text-sm font-bold tabular-nums text-emerald-300">
              {formatVnd(sum((v) => v.lead_bonus))}
            </p>
          </div>
        </div>
      </section>

      <section>
        <h2 className="mb-3 flex items-center gap-2 font-display text-lg font-bold text-white">
          <Lightbulb size={18} className="text-amber-300" />
          Đề tài gợi ý
        </h2>
        {topics === null ? (
          <p className="text-slate-500">Đang tải…</p>
        ) : topics.length === 0 ? (
          <p className="rounded-2xl border border-dashed border-white/10 p-6 text-center text-sm text-slate-500">
            Chưa có lỗi lớp nào trong 14 ngày gần nhất chờ làm video. Ghi phiếu lỗi sau mỗi buổi lên lớp để có kho đề tài.
          </p>
        ) : (
          <div className="flex flex-col gap-2.5">
            {topics.map((t) => (
              <div
                key={t.session_id}
                className="flex flex-wrap items-center gap-3 rounded-2xl border border-amber-400/25 bg-amber-500/5 p-4"
              >
                <div className="min-w-0 flex-1">
                  <p className="text-sm font-medium text-white">{t.error_note}</p>
                  <p className="mt-0.5 text-xs text-slate-400">
                    {new Date(t.work_date).toLocaleDateString("vi-VN")}
                    {t.class_label ? ` · ${t.class_label}` : ""}
                  </p>
                </div>
                <Link
                  href={`/tro-giang/ghi?topic=${t.session_id}`}
                  className="inline-flex shrink-0 items-center gap-1.5 rounded-xl bg-amber-600 px-3.5 py-2 text-xs font-bold text-white"
                >
                  <PenLine size={13} />
                  Làm video từ lỗi này
                </Link>
              </div>
            ))}
          </div>
        )}
      </section>

      <section>
        <h2 className="mb-3 font-display text-lg font-bold text-white">Video của mình</h2>
        {ledger === null ? (
          <p className="text-slate-500">Đang tải…</p>
        ) : ledger.length === 0 ? (
          <p className="rounded-2xl border border-dashed border-white/10 p-6 text-center text-sm text-slate-500">
            Chưa có video nào. Ghi buổi loại &quot;Video TikTok&quot; sau khi đăng video lên.
          </p>
        ) : (
          <div className="flex flex-col gap-2.5">
            {ledger.map((v) => {
              const statusMeta = STATUS_META[v.status];
              const StatusIcon = statusMeta.icon;
              return (
                <div key={v.session_id} className="rounded-2xl border border-white/10 bg-white/5 p-4">
                  <div className="flex flex-wrap items-start gap-3">
                    <div className="min-w-0 flex-1">
                      <p className="font-medium text-white">
                        {v.video_tier === "dung_ky" ? "Dựng kỹ" : "Đơn giản"}
                        <span className="ml-2 text-xs text-slate-400">
                          {new Date(v.work_date).toLocaleDateString("vi-VN")}
                        </span>
                        {v.topic_source_id && (
                          <span className="ml-2 text-xs text-emerald-300">làm từ phiếu lỗi</span>
                        )}
                      </p>
                      {v.video_url && <p className="truncate text-xs text-slate-500">{v.video_url}</p>}
                      <p className="mt-1.5 font-mono text-xs tabular-nums text-slate-300">
                        <span className="inline-flex items-center gap-1 text-emerald-300">
                          <Bookmark size={11} />
                          {v.latest_saves.toLocaleString("vi-VN")} lưu
                        </span>
                        {" · "}
                        {v.latest_views.toLocaleString("vi-VN")} xem
                        {v.latest_checked_at && (
                          <span className="text-slate-500">
                            {" "}
                            · đo {new Date(v.latest_checked_at).toLocaleDateString("vi-VN")}
                          </span>
                        )}
                      </p>
                      <p className="mt-1 text-xs text-amber-300">{milestoneText(v.latest_views, rates)}</p>
                      {v.status === "rejected" && v.reject_reason && (
                        <p className="mt-1 text-xs text-red-300">Lý do: {v.reject_reason}</p>
                      )}
                    </div>
                    <div className="text-right">
                      <p className="font-mono font-bold tabular-nums text-white">{formatVnd(v.total_pay)}</p>
                      <p className="font-mono text-[11px] tabular-nums text-slate-400">
                        SX {formatVnd(v.production_pay)} · view {formatVnd(v.view_bonus)}
                        {v.lead_count > 0 && (
                          <span className="text-emerald-300"> · {v.lead_count} HS {formatVnd(v.lead_bonus)}</span>
                        )}
                      </p>
                      <span
                        className={`mt-1.5 inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-[11px] font-bold ${statusMeta.className}`}
                      >
                        <StatusIcon size={11} />
                        {statusMeta.label}
                      </span>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </section>
    </div>
  );
}
