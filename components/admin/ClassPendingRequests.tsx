"use client";

import { useCallback, useEffect, useState } from "react";
import { Check, Clock3, X } from "lucide-react";
import { fetchPendingClassRequests, setUserClassStatus, type ClassJoinRequest } from "@/services/classes";
import { useToast } from "@/components/ui/Toast";

export default function ClassPendingRequests({
  classId,
  className,
  onReviewed,
}: {
  classId: number;
  className: string;
  onReviewed?: () => void;
}) {
  const toast = useToast();
  const [requests, setRequests] = useState<ClassJoinRequest[]>([]);
  const [busyId, setBusyId] = useState<string | null>(null);

  const reload = useCallback(() => {
    fetchPendingClassRequests(classId)
      .then(setRequests)
      .catch((error: unknown) => toast("error", error instanceof Error ? error.message : "Không tải được danh sách chờ duyệt."));
  }, [classId, toast]);
  useEffect(reload, [reload]);

  async function review(userId: string, status: "active" | "rejected") {
    setBusyId(userId);
    try {
      await setUserClassStatus(userId, classId, status);
      toast("success", status === "active" ? "Đã duyệt vào lớp." : "Đã từ chối yêu cầu.");
      reload();
      onReviewed?.();
    } catch (error) {
      toast("error", error instanceof Error ? error.message : "Không xử lý được yêu cầu.");
    } finally {
      setBusyId(null);
    }
  }

  if (!requests.length) {
    return (
      <p className="rounded-2xl border border-dashed border-white/10 p-10 text-center text-sm text-slate-500">
        Không có yêu cầu nào đang chờ duyệt vào lớp {className}.
      </p>
    );
  }

  return (
    <div className="space-y-2">
      {requests.map((request) => (
        <div
          key={request.userId}
          className="flex flex-wrap items-center gap-3 rounded-2xl border border-white/10 bg-[#0B1020] px-4 py-3"
        >
          <Clock3 size={16} className="text-amber-300" />
          <span className="font-medium text-white">{request.fullName}</span>
          <span className="text-xs text-slate-500">
            {new Date(request.requestedAt).toLocaleString("vi-VN")}
          </span>
          <span className="ml-auto flex items-center gap-1.5">
            <button
              onClick={() => review(request.userId, "active")}
              disabled={busyId === request.userId}
              className="inline-flex items-center gap-1 rounded-full bg-emerald-600 px-3 py-1.5 text-xs font-semibold text-white disabled:opacity-50"
            >
              <Check size={13} /> Duyệt
            </button>
            <button
              onClick={() => review(request.userId, "rejected")}
              disabled={busyId === request.userId}
              className="inline-flex items-center gap-1 rounded-full border border-red-500/30 px-3 py-1.5 text-xs font-semibold text-red-300 disabled:opacity-50"
            >
              <X size={13} /> Từ chối
            </button>
          </span>
        </div>
      ))}
    </div>
  );
}
