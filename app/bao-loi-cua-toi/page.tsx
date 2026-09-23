"use client";

import { useEffect, useState } from "react";
import { Bug, Loader2 } from "lucide-react";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import RequireAuth from "@/components/auth/RequireAuth";
import { useAuth } from "@/components/auth/AuthProvider";
import { fetchMyBugReports, BUG_CATEGORY_LABELS, BUG_STATUS_LABELS, type BugReport, type BugStatus } from "@/services/bug-reports";

const STATUS_STYLES: Record<BugStatus, string> = {
  moi: "bg-red-500/15 text-red-300",
  dang_xu_ly: "bg-amber-500/15 text-amber-300",
  da_xu_ly: "bg-emerald-500/15 text-emerald-300",
};

function fmt(iso: string) {
  return new Date(iso).toLocaleString("vi-VN", { day: "2-digit", month: "2-digit", year: "numeric", hour: "2-digit", minute: "2-digit" });
}

function List() {
  const { session } = useAuth();
  const [reports, setReports] = useState<BugReport[] | null>(null);

  useEffect(() => {
    if (!session) return;
    fetchMyBugReports(session.user.id).then(setReports).catch(() => setReports([]));
  }, [session]);

  if (!reports) {
    return (
      <p className="flex items-center gap-2 text-sm text-slate-500">
        <Loader2 size={14} className="animate-spin" />
        Đang tải…
      </p>
    );
  }

  if (reports.length === 0) {
    return <p className="rounded-2xl border border-dashed border-white/10 p-8 text-center text-sm text-slate-500">Bạn chưa gửi báo lỗi hay đề xuất nào.</p>;
  }

  return (
    <div className="space-y-3">
      {reports.map((r) => (
        <div key={r.id} className="rounded-2xl border border-white/10 bg-panel px-5 py-4">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <span className="text-xs font-bold text-slate-400">{BUG_CATEGORY_LABELS[r.category]}</span>
            <div className="flex items-center gap-2">
              <span className="text-xs text-slate-500">{fmt(r.created_at)}</span>
              <span className={`rounded-full px-2.5 py-0.5 text-xs font-bold ${STATUS_STYLES[r.status]}`}>{BUG_STATUS_LABELS[r.status]}</span>
            </div>
          </div>
          <p className="mt-2 whitespace-pre-wrap text-sm text-slate-200">{r.description}</p>
          {r.admin_note && (
            <div className="mt-3 rounded-xl border border-cyan-400/20 bg-cyan-500/[.06] p-3 text-sm text-cyan-200">
              <span className="font-bold">Phản hồi: </span>
              {r.admin_note}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

export default function MyBugReportsPage() {
  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-3xl px-6 pb-24 pt-28 lg:px-8">
        <RequireAuth>
          <h1 className="flex items-center gap-2 font-display text-2xl font-bold text-white">
            <Bug size={22} className="text-amber-300" />
            Báo lỗi &amp; góp ý của tôi
          </h1>
          <p className="mt-1 text-sm text-slate-400">Danh sách các báo lỗi, đề xuất bạn đã gửi và trạng thái xử lý.</p>
          <div className="mt-6">
            <List />
          </div>
        </RequireAuth>
      </main>
      <Footer />
    </>
  );
}
