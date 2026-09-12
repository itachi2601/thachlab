"use client";

import { useCallback, useEffect, useState } from "react";
import { Check, Clock3, Mail, Phone, UserCheck, X } from "lucide-react";
import { useToast } from "@/components/ui/Toast";
import {
  fetchThptRegistrations,
  reviewThptRegistration,
  type ThptRegistrationRequest,
} from "@/services/thpt-registrations";

export default function ThptRegistrationRequestsPanel({
  classId,
  className,
  onChanged,
}: {
  classId: number;
  className: string;
  onChanged?: () => void;
}) {
  const toast = useToast();
  const [requests, setRequests] = useState<ThptRegistrationRequest[]>([]);
  const [loading, setLoading] = useState(true);
  const [busyId, setBusyId] = useState<number | null>(null);
  const [error, setError] = useState("");

  const reload = useCallback(async () => {
    setLoading(true);
    try {
      setRequests(await fetchThptRegistrations(classId));
      setError("");
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Không tải được yêu cầu đăng ký.");
    } finally {
      setLoading(false);
    }
  }, [classId]);

  useEffect(() => {
    const timer = window.setTimeout(() => void reload(), 0);
    return () => window.clearTimeout(timer);
  }, [reload]);

  async function review(request: ThptRegistrationRequest, status: "approved" | "rejected") {
    setBusyId(request.id);
    try {
      await reviewThptRegistration(request.id, status);
      toast("success", status === "approved" ? `Đã thêm ${request.full_name} vào ${className}.` : `Đã từ chối đăng ký của ${request.full_name}.`);
      await reload();
      onChanged?.();
    } catch (cause) {
      toast("error", cause instanceof Error ? cause.message : "Chưa xử lý được yêu cầu.");
    } finally {
      setBusyId(null);
    }
  }

  const pending = requests.filter((request) => request.status === "pending");
  const reviewed = requests.filter((request) => request.status !== "pending").slice(0, 10);

  return (
    <div className="space-y-5">
      <section className="rounded-3xl border border-white/10 bg-gradient-to-br from-[#172c46] to-[#071426] p-6">
        <p className="text-xs font-bold uppercase tracking-[.16em] text-blue-300">THPT · Đăng ký trực tuyến</p>
        <h2 className="mt-2 font-display text-2xl font-bold text-white">Học sinh chờ duyệt · {className}</h2>
        <p className="mt-2 text-sm text-slate-400">Kiểm tra thông tin học sinh tự đăng ký trước khi thêm tài khoản vào khối lớp.</p>
      </section>

      {error && <p className="rounded-xl border border-red-500/20 bg-red-500/5 p-4 text-sm text-red-300">{error}</p>}
      {loading ? <p className="text-sm text-slate-400">Đang tải yêu cầu…</p> : (
        <section className="space-y-3">
          <div className="flex items-center gap-2"><Clock3 size={17} className="text-amber-300" /><h3 className="font-display font-bold text-white">Chờ duyệt ({pending.length})</h3></div>
          {pending.map((request) => (
            <article key={request.id} className="rounded-2xl border border-amber-400/20 bg-[#0B1020] p-5">
              <div className="flex flex-wrap items-start justify-between gap-4">
                <div>
                  <h4 className="font-display text-lg font-bold text-white">{request.full_name}</h4>
                  <p className="mt-1 text-xs text-slate-500">Tài khoản: {request.username || "—"} · Mã HS: {request.student_code || "—"} · Đăng ký {new Date(request.created_at).toLocaleString("vi-VN")}</p>
                  <div className="mt-3 flex flex-wrap gap-x-5 gap-y-2 text-xs text-slate-400">
                    {request.email && <span className="inline-flex items-center gap-1.5"><Mail size={13} />{request.email}</span>}
                    {request.phone && <span className="inline-flex items-center gap-1.5"><Phone size={13} />{request.phone}</span>}
                    {request.parent_phone && <span>PH: {request.parent_phone}</span>}
                    {request.birth_date && <span>Ngày sinh: {new Date(`${request.birth_date}T00:00:00`).toLocaleDateString("vi-VN")}</span>}
                    {request.gender && <span>{request.gender === "1" ? "Nam" : request.gender === "0" ? "Nữ" : request.gender}</span>}
                  </div>
                </div>
                <div className="flex gap-2">
                  <button disabled={busyId === request.id} onClick={() => void review(request, "rejected")} className="inline-flex items-center gap-1.5 rounded-xl border border-red-400/25 px-3 py-2 text-xs font-bold text-red-200 disabled:opacity-40"><X size={14} />Từ chối</button>
                  <button disabled={busyId === request.id} onClick={() => void review(request, "approved")} className="inline-flex items-center gap-1.5 rounded-xl bg-emerald-600 px-3 py-2 text-xs font-bold text-white disabled:opacity-40"><Check size={14} />Duyệt vào lớp</button>
                </div>
              </div>
            </article>
          ))}
          {!pending.length && <p className="rounded-2xl border border-dashed border-white/10 p-8 text-center text-sm text-slate-500">Không có học sinh nào đang chờ duyệt.</p>}
        </section>
      )}

      {reviewed.length > 0 && (
        <section className="space-y-2">
          <div className="flex items-center gap-2"><UserCheck size={17} className="text-emerald-300" /><h3 className="font-display font-bold text-white">Đã xử lý gần đây</h3></div>
          {reviewed.map((request) => <div key={request.id} className="flex items-center justify-between rounded-xl border border-white/10 bg-[#0B1020] px-4 py-3 text-sm"><span className="text-slate-300">{request.full_name}</span><span className={request.status === "approved" ? "text-emerald-300" : "text-red-300"}>{request.status === "approved" ? "Đã duyệt" : "Đã từ chối"}</span></div>)}
        </section>
      )}
    </div>
  );
}
