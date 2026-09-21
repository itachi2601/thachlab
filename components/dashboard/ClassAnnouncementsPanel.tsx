"use client";

import { useCallback, useEffect, useState } from "react";
import { Trash2 } from "lucide-react";
import { useAuth } from "@/components/auth/AuthProvider";
import { useToast } from "@/components/ui/Toast";
import {
  deleteAnnouncement,
  fetchRecentAnnouncements,
  postAnnouncement,
  type AnnouncementKind,
  type ClassAnnouncement,
} from "@/services/announcements";

const KIND_META: Record<AnnouncementKind, { label: string; placeholder: string }> = {
  today_task: { label: "Việc cần làm hôm nay", placeholder: "VD: Hoàn thành trắc nghiệm Bài 9 trước 21h…" },
  homework: { label: "Bài tập về nhà", placeholder: "VD: Làm câu 1-10 trang 45, nộp qua Zalo lớp…" },
};

function AnnouncementColumn({ classId, kind }: { classId: number; kind: AnnouncementKind }) {
  const { profile } = useAuth();
  const toast = useToast();
  const [items, setItems] = useState<ClassAnnouncement[] | null>(null);
  const [draft, setDraft] = useState("");
  const [busy, setBusy] = useState(false);

  const load = useCallback(() => {
    fetchRecentAnnouncements(classId, kind)
      .then(setItems)
      .catch(() => setItems([]));
  }, [classId, kind]);
  useEffect(load, [load]);

  async function send() {
    if (!profile || !draft.trim()) return;
    setBusy(true);
    try {
      await postAnnouncement({ classId, kind, body: draft, createdBy: profile.id });
      setDraft("");
      toast("success", "Đã đăng thông báo.");
      load();
    } catch (e) {
      toast("error", e instanceof Error ? e.message : "Chưa đăng được.");
    } finally {
      setBusy(false);
    }
  }

  async function remove(id: number) {
    try {
      await deleteAnnouncement(id);
      load();
    } catch (e) {
      toast("error", e instanceof Error ? e.message : "Chưa xoá được.");
    }
  }

  const meta = KIND_META[kind];

  return (
    <section className="rounded-2xl border border-white/10 bg-[#0B1020] p-4 sm:p-5">
      <h3 className="font-display font-bold text-white">{meta.label}</h3>
      <div className="mt-3 flex flex-col gap-2 sm:flex-row">
        <textarea
          value={draft}
          onChange={(event) => setDraft(event.target.value)}
          placeholder={meta.placeholder}
          rows={2}
          className="flex-1 rounded-xl border border-white/10 bg-[#080d1d] px-3 py-2 text-sm text-white placeholder:text-slate-600"
        />
        <button
          type="button"
          onClick={send}
          disabled={busy || !draft.trim()}
          className="shrink-0 self-end rounded-xl bg-blue-600 px-4 py-2 text-sm font-bold text-white disabled:opacity-40 sm:self-stretch"
        >
          Đăng
        </button>
      </div>
      <div className="mt-3 space-y-2">
        {items === null ? (
          <p className="text-xs text-slate-500">Đang tải…</p>
        ) : items.length === 0 ? (
          <p className="text-xs text-slate-500">Chưa có thông báo nào.</p>
        ) : (
          items.map((item) => (
            <div key={item.id} className="flex items-start justify-between gap-3 rounded-xl bg-white/[.02] p-3">
              <div className="min-w-0">
                <p className="whitespace-pre-wrap text-sm text-slate-200">{item.body}</p>
                <p className="mt-1 text-[11px] text-slate-500">
                  {item.createdByName || "—"} ·{" "}
                  {new Date(item.createdAt).toLocaleString("vi-VN", {
                    day: "2-digit",
                    month: "2-digit",
                    hour: "2-digit",
                    minute: "2-digit",
                  })}
                </p>
              </div>
              <button
                type="button"
                onClick={() => remove(item.id)}
                aria-label="Xoá thông báo"
                className="shrink-0 text-slate-500 hover:text-red-300"
              >
                <Trash2 size={14} />
              </button>
            </div>
          ))
        )}
      </div>
    </section>
  );
}

/**
 * Đăng thông báo cho một lớp — "việc cần làm hôm nay" + "bài tập về nhà". Giáo viên
 * và trợ giảng của lớp đó đều đăng được (RLS: manages_class hoặc assists_class).
 * Dùng chung ở dashboard giáo viên (tab Thông báo) và /tro-giang/thong-bao.
 */
export default function ClassAnnouncementsPanel({ classId }: { classId: number }) {
  return (
    <div className="space-y-4">
      <AnnouncementColumn classId={classId} kind="today_task" />
      <AnnouncementColumn classId={classId} kind="homework" />
    </div>
  );
}
