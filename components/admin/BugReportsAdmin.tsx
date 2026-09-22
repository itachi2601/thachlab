"use client";

import { useCallback, useEffect, useState } from "react";
import { Bug, Image as ImageIcon, Loader2, RefreshCw, X } from "lucide-react";
import {
  fetchBugReports,
  updateBugReportStatus,
  createBugReportScreenshotUrl,
  BUG_CATEGORY_LABELS,
  BUG_STATUS_LABELS,
  type BugReport,
  type BugStatus,
} from "@/services/bug-reports";

const STATUS_STYLES: Record<BugStatus, string> = {
  moi: "bg-red-500/15 text-red-300",
  dang_xu_ly: "bg-amber-500/15 text-amber-300",
  da_xu_ly: "bg-emerald-500/15 text-emerald-300",
};

const TABS: { value: BugStatus | "all"; label: string }[] = [
  { value: "all", label: "Tất cả" },
  { value: "moi", label: "Mới" },
  { value: "dang_xu_ly", label: "Đang xử lý" },
  { value: "da_xu_ly", label: "Đã xử lý" },
];

function fmt(iso: string) {
  return new Date(iso).toLocaleString("vi-VN", { day: "2-digit", month: "2-digit", year: "numeric", hour: "2-digit", minute: "2-digit" });
}

export default function BugReportsAdmin() {
  const [tab, setTab] = useState<BugStatus | "all">("moi");
  const [reports, setReports] = useState<BugReport[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selected, setSelected] = useState<BugReport | null>(null);

  const load = useCallback(() => {
    setLoading(true);
    fetchBugReports(tab === "all" ? undefined : tab)
      .then(setReports)
      .catch((cause) => setError(cause instanceof Error ? cause.message : "Không tải được danh sách báo lỗi."))
      .finally(() => setLoading(false));
  }, [tab]);
  useEffect(() => {
    load();
  }, [load]);

  const moiCount = reports.filter((r) => r.status === "moi").length;

  return (
    <div className="space-y-5">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <p className="admin-eyebrow">Báo lỗi từ người dùng</p>
          <p className="admin-lead">
            {reports.length} báo lỗi{tab === "all" && moiCount > 0 && <span className="ml-1 font-bold text-red-300">· {moiCount} mới</span>}
          </p>
        </div>
        <button onClick={load} disabled={loading} className="inline-flex items-center gap-2 rounded-xl border border-white/10 px-4 py-2.5 text-sm font-bold text-slate-300 disabled:opacity-40">
          <RefreshCw size={16} className={loading ? "animate-spin" : ""} />
          Làm mới
        </button>
      </div>

      <div className="flex flex-wrap gap-2">
        {TABS.map((t) => (
          <button
            key={t.value}
            type="button"
            onClick={() => setTab(t.value)}
            className={`rounded-xl border px-4 py-2 text-sm font-bold transition-colors ${
              tab === t.value ? "border-cyan-400/40 bg-cyan-500/10 text-white" : "border-white/10 text-slate-400 hover:border-white/20 hover:text-slate-200"
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>

      {error && <p className="rounded-xl bg-red-500/10 p-3 text-sm text-red-200">{error}</p>}

      {loading ? (
        <p className="admin-card flex items-center gap-2 text-sm text-slate-500">
          <Loader2 size={14} className="animate-spin" />
          Đang tải…
        </p>
      ) : reports.length === 0 ? (
        <p className="rounded-2xl border border-dashed border-white/10 p-8 text-center text-sm text-slate-500">Không có báo lỗi nào.</p>
      ) : (
        <div className="admin-table-wrap">
          <table className="min-w-[900px] text-xs">
            <thead>
              <tr>
                <th className="p-2">Thời gian</th>
                <th className="p-2">Người báo</th>
                <th className="p-2">Loại lỗi</th>
                <th className="p-2">Mô tả</th>
                <th className="p-2">Trang</th>
                <th className="p-2">Trạng thái</th>
                <th className="p-2" />
              </tr>
            </thead>
            <tbody>
              {reports.map((r) => (
                <tr key={r.id} className="border-b border-white/5">
                  <td className="p-2 text-slate-400">{fmt(r.created_at)}</td>
                  <td className="p-2 text-slate-300">{r.profiles?.full_name ?? (r.reporter_name || "Khách")}</td>
                  <td className="p-2 text-slate-300">{BUG_CATEGORY_LABELS[r.category]}</td>
                  <td className="max-w-[260px] truncate p-2 text-slate-400" title={r.description}>
                    {r.description}
                  </td>
                  <td className="max-w-[160px] truncate p-2 font-mono text-slate-500" title={r.page_url}>
                    {r.page_url || "—"}
                  </td>
                  <td className="p-2">
                    <span className={`rounded-full px-2 py-0.5 font-bold ${STATUS_STYLES[r.status]}`}>{BUG_STATUS_LABELS[r.status]}</span>
                  </td>
                  <td className="p-2">
                    <button type="button" onClick={() => setSelected(r)} className="font-bold text-cyan-300 hover:text-cyan-200">
                      Xem
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {selected && <BugReportDetailModal report={selected} onClose={() => setSelected(null)} onChanged={load} />}
    </div>
  );
}

function BugReportDetailModal({ report, onClose, onChanged }: { report: BugReport; onClose: () => void; onChanged: () => void }) {
  const [status, setStatus] = useState<BugStatus>(report.status);
  const [note, setNote] = useState(report.admin_note);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [screenshotUrl, setScreenshotUrl] = useState<string | null>(null);
  const [screenshotLoading, setScreenshotLoading] = useState(false);

  function loadScreenshot() {
    if (!report.screenshot_path || screenshotUrl) return;
    setScreenshotLoading(true);
    createBugReportScreenshotUrl(report.screenshot_path)
      .then(setScreenshotUrl)
      .catch(() => setError("Không mở được ảnh chụp màn hình."))
      .finally(() => setScreenshotLoading(false));
  }

  async function save() {
    setBusy(true);
    setError("");
    try {
      await updateBugReportStatus(report.id, status, note);
      onChanged();
      onClose();
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Không lưu được.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="fixed inset-0 z-50 grid place-items-center bg-black/60 p-4" onClick={onClose}>
      <section role="dialog" aria-modal="true" aria-label="Chi tiết báo lỗi" className="w-full max-w-lg rounded-2xl border border-white/10 bg-[#0B1020] p-6 shadow-2xl" onClick={(e) => e.stopPropagation()}>
        <div className="flex items-center justify-between">
          <h2 className="flex items-center gap-2 text-lg font-bold text-white">
            <Bug size={18} className="text-amber-300" />
            Chi tiết báo lỗi
          </h2>
          <button type="button" onClick={onClose} className="text-slate-400 hover:text-white">
            <X size={20} />
          </button>
        </div>

        <dl className="mt-4 space-y-2 text-sm">
          <div className="flex justify-between gap-3">
            <dt className="text-slate-500">Người báo</dt>
            <dd className="text-right text-slate-200">
              {report.profiles?.full_name ?? (report.reporter_name || "Khách")}
              {report.reporter_email && <span className="block text-xs text-slate-500">{report.reporter_email}</span>}
            </dd>
          </div>
          <div className="flex justify-between gap-3">
            <dt className="text-slate-500">Loại lỗi</dt>
            <dd className="text-slate-200">{BUG_CATEGORY_LABELS[report.category]}</dd>
          </div>
          <div className="flex justify-between gap-3">
            <dt className="text-slate-500">Trang</dt>
            <dd className="max-w-[260px] truncate font-mono text-xs text-slate-400" title={report.page_url}>
              {report.page_url || "—"}
            </dd>
          </div>
          <div className="flex justify-between gap-3">
            <dt className="text-slate-500">Thời gian</dt>
            <dd className="text-slate-200">{fmt(report.created_at)}</dd>
          </div>
        </dl>

        <p className="mt-4 whitespace-pre-wrap rounded-xl border border-white/10 bg-white/5 p-3 text-sm text-slate-200">{report.description}</p>

        {report.screenshot_path && (
          <div className="mt-3">
            {screenshotUrl ? (
              <a href={screenshotUrl} target="_blank" rel="noreferrer" className="inline-flex items-center gap-2 text-sm font-bold text-cyan-300 hover:text-cyan-200">
                <ImageIcon size={15} />
                Mở ảnh chụp màn hình
              </a>
            ) : (
              <button type="button" onClick={loadScreenshot} disabled={screenshotLoading} className="inline-flex items-center gap-2 text-sm font-bold text-cyan-300 hover:text-cyan-200 disabled:opacity-50">
                <ImageIcon size={15} />
                {screenshotLoading ? "Đang tải ảnh…" : "Xem ảnh chụp màn hình"}
              </button>
            )}
          </div>
        )}

        <div className="mt-5 space-y-3">
          <select value={status} onChange={(e) => setStatus(e.target.value as BugStatus)} className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-2.5 text-sm text-white focus:border-primary focus:outline-none">
            {Object.entries(BUG_STATUS_LABELS).map(([value, label]) => (
              <option key={value} value={value}>
                {label}
              </option>
            ))}
          </select>
          <textarea
            value={note}
            onChange={(e) => setNote(e.target.value)}
            placeholder="Ghi chú xử lý (chỉ admin thấy)"
            rows={3}
            className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-2.5 text-sm text-white placeholder:text-slate-500 focus:border-primary focus:outline-none"
          />
          {error && <p className="text-sm text-red-400">{error}</p>}
          <button type="button" onClick={save} disabled={busy} className="admin-btn admin-btn--primary w-full">
            {busy ? "Đang lưu…" : "Lưu"}
          </button>
        </div>
      </section>
    </div>
  );
}
