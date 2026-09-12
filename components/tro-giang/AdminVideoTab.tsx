"use client";

import { useCallback, useEffect, useState } from "react";
import { AlertTriangle, BarChart3, Bookmark, Check, Plus, UserPlus } from "lucide-react";
import { useToast } from "@/components/ui/Toast";
import { formatVnd } from "@/lib/tro-giang/format";
import {
  approveSessions,
  createLead,
  fetchAssistants,
  fetchTopicExploitationRate,
  fetchVideoAdminSummary,
  fetchVideoLedger,
  upsertVideoStats,
  type TaAssistant,
  type TaTopicExploitation,
  type TaVideoAdminSummary,
  type TaVideoLedgerRow,
} from "@/lib/tro-giang/queries";

function currentMonthInput() {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}`;
}

function todayStr() {
  return new Date().toLocaleDateString("sv-SE");
}

function Tile({
  label,
  value,
  hint,
  tone = "normal",
  large = false,
  icon: Icon,
}: {
  label: string;
  value: string;
  hint?: string;
  tone?: "normal" | "good" | "warn";
  large?: boolean;
  icon?: typeof Bookmark;
}) {
  const toneClass =
    tone === "good"
      ? "border-emerald-400/30 bg-emerald-500/10"
      : tone === "warn"
        ? "border-red-500/40 bg-red-500/10"
        : "border-white/10 bg-white/5";
  return (
    <div className={`rounded-2xl border p-4 ${toneClass}`}>
      <p className="flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wide text-slate-400">
        {Icon && <Icon size={13} />}
        {label}
      </p>
      <p className={`mt-1.5 font-mono font-bold tabular-nums text-white ${large ? "text-3xl" : "text-lg"}`}>{value}</p>
      {hint && <p className="mt-1 text-xs text-slate-400">{hint}</p>}
    </div>
  );
}

export default function AdminVideoTab({ reloadKey = 0 }: { reloadKey?: number }) {
  const toast = useToast();
  const [month, setMonth] = useState(currentMonthInput());
  const [summary, setSummary] = useState<TaVideoAdminSummary | null>(null);
  const [topic, setTopic] = useState<TaTopicExploitation | null>(null);
  const [ledger, setLedger] = useState<TaVideoLedgerRow[] | null>(null);
  const [assistants, setAssistants] = useState<TaAssistant[]>([]);
  const [busy, setBusy] = useState(false);

  const [statsFor, setStatsFor] = useState<string | null>(null);
  const [stats, setStats] = useState({ checked_at: todayStr(), views: "", saves: "", comments: "" });

  const [leadOpen, setLeadOpen] = useState(false);
  const [lead, setLead] = useState({ student_name: "", attributed_session_id: "", registered_at: todayStr() });

  const load = useCallback(() => {
    fetchVideoAdminSummary(`${month}-01`).then(setSummary).catch(() => setSummary(null));
    fetchTopicExploitationRate(14).then(setTopic).catch(() => setTopic(null));
    fetchVideoLedger(null).then(setLedger).catch(() => setLedger([]));
    fetchAssistants().then(setAssistants).catch(() => {});
  }, [month]);

  useEffect(load, [load, reloadKey]);

  const nameOf = (id: string) => assistants.find((a) => a.id === id)?.short_name ?? "—";

  async function saveStats(sessionId: string) {
    setBusy(true);
    try {
      await upsertVideoStats({
        session_id: sessionId,
        checked_at: stats.checked_at,
        views: Number(stats.views) || 0,
        saves: Number(stats.saves) || 0,
        comments: Number(stats.comments) || 0,
      });
      toast("success", "Đã ghi số liệu tuần.");
      setStatsFor(null);
      setStats({ checked_at: todayStr(), views: "", saves: "", comments: "" });
      load();
    } catch (error) {
      toast("error", error instanceof Error ? error.message : "Không ghi được số liệu.");
    } finally {
      setBusy(false);
    }
  }

  async function submitLead() {
    if (!lead.student_name.trim()) {
      toast("error", "Nhập tên học sinh mới.");
      return;
    }
    setBusy(true);
    try {
      await createLead({
        student_name: lead.student_name.trim(),
        source: "tiktok",
        attributed_session_id: lead.attributed_session_id || null,
        registered_at: lead.registered_at,
      });
      toast("success", "Đã ghi nhận học sinh đăng ký qua TikTok.");
      setLead({ student_name: "", attributed_session_id: "", registered_at: todayStr() });
      setLeadOpen(false);
      load();
    } catch (error) {
      toast("error", error instanceof Error ? error.message : "Không ghi nhận được.");
    } finally {
      setBusy(false);
    }
  }

  async function approveVideo(id: string) {
    setBusy(true);
    try {
      await approveSessions([id]);
      toast("success", "Đã duyệt video.");
      load();
    } catch (error) {
      toast("error", error instanceof Error ? error.message : "Không duyệt được.");
    } finally {
      setBusy(false);
    }
  }

  const pending = (ledger ?? []).filter((v) => v.status === "submitted");

  return (
    <div className="space-y-5">
      <div className="flex flex-wrap items-center gap-3">
        <input
          type="month"
          value={month}
          onChange={(e) => setMonth(e.target.value)}
          className="rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-sm text-white"
        />
        <button
          type="button"
          onClick={() => setLeadOpen((v) => !v)}
          className="inline-flex items-center gap-2 rounded-xl bg-blue-600 px-4 py-2 text-sm font-bold text-white"
        >
          <UserPlus size={15} />
          Ghi nhận học sinh mới
        </button>
      </div>

      {leadOpen && (
        <div className="rounded-2xl border border-blue-400/30 bg-blue-500/10 p-4">
          <p className="font-semibold text-blue-100">Học sinh mới đăng ký qua TikTok</p>
          <div className="mt-3 flex flex-wrap gap-2">
            <input
              value={lead.student_name}
              onChange={(e) => setLead({ ...lead, student_name: e.target.value })}
              placeholder="Tên học sinh"
              className="min-w-0 flex-1 rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-sm text-white placeholder:text-slate-500"
            />
            <select
              value={lead.attributed_session_id}
              onChange={(e) => setLead({ ...lead, attributed_session_id: e.target.value })}
              className="rounded-xl border border-white/10 bg-[#0B1020] px-3 py-2 text-sm text-white"
            >
              <option value="">Không gắn video nào</option>
              {(ledger ?? []).map((v) => (
                <option key={v.session_id} value={v.session_id}>
                  {nameOf(v.assistant_id)} · {new Date(v.work_date).toLocaleDateString("vi-VN")} ·{" "}
                  {v.video_url?.slice(0, 40) ?? "video"}
                </option>
              ))}
            </select>
            <input
              type="date"
              value={lead.registered_at}
              onChange={(e) => setLead({ ...lead, registered_at: e.target.value })}
              className="rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-sm text-white"
            />
            <button
              type="button"
              disabled={busy}
              onClick={submitLead}
              className="rounded-xl bg-blue-600 px-4 py-2 text-sm font-bold text-white disabled:opacity-40"
            >
              Ghi nhận
            </button>
          </div>
          <p className="mt-2 text-xs text-blue-200/80">
            Gắn video sẽ chi thưởng đăng ký cho trợ giảng làm video đó.
          </p>
        </div>
      )}

      {summary && (
        <>
          <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
            <Tile
              label="Lượt lưu"
              value={summary.total_saves.toLocaleString("vi-VN")}
              hint="Tín hiệu thật — học sinh lưu để xem lại"
              large
              icon={Bookmark}
            />
            <Tile label="Học sinh đăng ký qua TikTok" value={String(summary.leads_count)} large icon={UserPlus} />
            <Tile label="Lượt xem" value={summary.total_views.toLocaleString("vi-VN")} icon={BarChart3} />
            <Tile label="Video đã đăng" value={String(summary.videos_published)} />
          </div>

          <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
            <Tile
              label="Chi sản xuất"
              value={formatVnd(summary.production_spend)}
              hint={`Trần ${summary.budget_cap.toLocaleString("vi-VN")} đ/tháng`}
              tone={summary.over_budget ? "warn" : "normal"}
            />
            <Tile label="Thưởng lượt xem" value={formatVnd(summary.view_bonus_spend)} />
            <Tile
              label="Thưởng đăng ký"
              value={formatVnd(summary.lead_bonus_spend)}
              hint="Không bị chặn bởi trần — càng cao càng tốt"
              tone="good"
            />
            <Tile
              label="Chi phí mỗi học sinh"
              value={summary.cost_per_lead == null ? "—" : formatVnd(summary.cost_per_lead)}
              hint={`Tổng chi ${formatVnd(summary.total_spend)}`}
            />
          </div>

          {summary.over_budget && (
            <p className="inline-flex items-center gap-2 rounded-xl bg-red-500/15 px-3 py-2 text-sm font-semibold text-red-200">
              <AlertTriangle size={15} />
              Chi sản xuất tháng này đã vượt trần ngân sách.
            </p>
          )}
        </>
      )}

      {topic && (
        <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">
            Đề tài từ phiếu lỗi đã được khai thác (14 ngày gần nhất)
          </p>
          <div className="mt-2 flex items-center gap-3">
            <span className="font-mono text-2xl font-bold tabular-nums text-white">
              {Math.round(topic.rate * 100)}%
            </span>
            <span className="text-sm text-slate-400">
              {topic.used_count}/{topic.eligible_count} lỗi lớp đã thành video
            </span>
          </div>
          {topic.eligible_count > topic.used_count && (
            <p className="mt-2 text-xs text-amber-300">
              Còn {topic.eligible_count - topic.used_count} đề tài chưa dùng — kho nội dung đang bị bỏ phí.
            </p>
          )}
        </div>
      )}

      <div>
        <h3 className="mb-3 font-display text-lg font-bold text-white">
          Video {pending.length > 0 && <span className="text-amber-300">· {pending.length} chờ duyệt</span>}
        </h3>
        {ledger === null ? (
          <p className="text-slate-400">Đang tải…</p>
        ) : ledger.length === 0 ? (
          <p className="rounded-2xl border border-dashed border-white/10 p-8 text-center text-sm text-slate-500">
            Chưa có video nào. Trợ giảng ghi buổi loại &quot;Video TikTok&quot; thì sẽ hiện ở đây.
          </p>
        ) : (
          <div className="space-y-2.5">
            {ledger.map((v) => (
              <div
                key={v.session_id}
                className={`rounded-2xl border p-4 ${v.status === "submitted" ? "border-amber-400/40 bg-amber-500/5" : "border-white/10 bg-white/5"}`}
              >
                <div className="flex flex-wrap items-start gap-3">
                  <div className="min-w-0 flex-1">
                    <p className="font-semibold text-white">
                      {nameOf(v.assistant_id)} · {v.video_tier === "dung_ky" ? "Dựng kỹ" : "Đơn giản"}
                      {v.topic_source_id && <span className="ml-2 text-xs text-emerald-300">từ phiếu lỗi</span>}
                    </p>
                    <p className="truncate text-xs text-slate-400">
                      {new Date(v.work_date).toLocaleDateString("vi-VN")} · {v.video_url ?? "chưa có link"}
                    </p>
                    <p className="mt-1.5 font-mono text-xs tabular-nums text-slate-300">
                      <span className="text-emerald-300">{v.latest_saves.toLocaleString("vi-VN")} lưu</span>
                      {" · "}
                      {v.latest_views.toLocaleString("vi-VN")} xem · {v.latest_comments.toLocaleString("vi-VN")} bình luận
                      {v.latest_checked_at && (
                        <span className="text-slate-500"> · đo {new Date(v.latest_checked_at).toLocaleDateString("vi-VN")}</span>
                      )}
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="font-mono font-bold tabular-nums text-white">{formatVnd(v.total_pay)}</p>
                    <p className="font-mono text-[11px] tabular-nums text-slate-400">
                      SX {formatVnd(v.production_pay)} · view {formatVnd(v.view_bonus)}
                      {v.lead_count > 0 && <span className="text-emerald-300"> · {v.lead_count} HS {formatVnd(v.lead_bonus)}</span>}
                    </p>
                  </div>
                  <div className="flex shrink-0 gap-2">
                    {v.status === "submitted" && (
                      <button
                        type="button"
                        disabled={busy}
                        onClick={() => approveVideo(v.session_id)}
                        className="inline-flex items-center gap-1.5 rounded-xl bg-emerald-600 px-3 py-2 text-xs font-bold text-white disabled:opacity-40"
                      >
                        <Check size={13} />
                        Duyệt
                      </button>
                    )}
                    <button
                      type="button"
                      onClick={() => {
                        setStatsFor(statsFor === v.session_id ? null : v.session_id);
                        setStats({ checked_at: todayStr(), views: "", saves: "", comments: "" });
                      }}
                      className="inline-flex items-center gap-1.5 rounded-xl border border-white/15 px-3 py-2 text-xs font-semibold text-slate-200"
                    >
                      <Plus size={13} />
                      Số liệu tuần
                    </button>
                  </div>
                </div>

                {statsFor === v.session_id && (
                  <div className="mt-3 flex flex-wrap gap-2 border-t border-white/10 pt-3">
                    <input
                      type="date"
                      value={stats.checked_at}
                      onChange={(e) => setStats({ ...stats, checked_at: e.target.value })}
                      className="rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-sm text-white"
                    />
                    <input
                      inputMode="numeric"
                      value={stats.views}
                      onChange={(e) => setStats({ ...stats, views: e.target.value })}
                      placeholder="Lượt xem"
                      className="w-28 rounded-xl border border-white/10 bg-white/5 px-3 py-2 font-mono text-sm tabular-nums text-white placeholder:font-sans placeholder:text-slate-500"
                    />
                    <input
                      inputMode="numeric"
                      value={stats.saves}
                      onChange={(e) => setStats({ ...stats, saves: e.target.value })}
                      placeholder="Lượt lưu"
                      className="w-28 rounded-xl border border-white/10 bg-white/5 px-3 py-2 font-mono text-sm tabular-nums text-white placeholder:font-sans placeholder:text-slate-500"
                    />
                    <input
                      inputMode="numeric"
                      value={stats.comments}
                      onChange={(e) => setStats({ ...stats, comments: e.target.value })}
                      placeholder="Bình luận"
                      className="w-28 rounded-xl border border-white/10 bg-white/5 px-3 py-2 font-mono text-sm tabular-nums text-white placeholder:font-sans placeholder:text-slate-500"
                    />
                    <button
                      type="button"
                      disabled={busy}
                      onClick={() => saveStats(v.session_id)}
                      className="rounded-xl bg-blue-600 px-4 py-2 text-sm font-bold text-white disabled:opacity-40"
                    >
                      Lưu
                    </button>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
