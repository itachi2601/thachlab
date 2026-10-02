"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { ClipboardCheck, Trash2, X } from "lucide-react";
import { useAuth } from "@/components/auth/AuthProvider";
import { useToast } from "@/components/ui/Toast";
import { getSupabase } from "@/services/supabase";
import {
  deleteAnnouncement,
  fetchRecentAnnouncements,
  postAnnouncement,
  type AnnouncementKind,
  type ClassAnnouncement,
} from "@/services/announcements";
import HomeworkCheckPanel from "@/components/dashboard/HomeworkCheckPanel";

interface ExamOption {
  id: number;
  title: string;
}

function ExamPicker({ selected, onSelect }: { selected: ExamOption | null; onSelect: (exam: ExamOption | null) => void }) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<ExamOption[]>([]);
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    if (timer.current) clearTimeout(timer.current);
    const trimmed = query.trim();
    if (!trimmed) return;
    timer.current = setTimeout(() => {
      getSupabase()
        .from("exams")
        .select("id, title")
        .ilike("title", `%${trimmed}%`)
        .order("id", { ascending: false })
        .limit(8)
        .then(({ data }) => setResults((data as ExamOption[]) ?? []));
    }, 300);
    return () => {
      if (timer.current) clearTimeout(timer.current);
    };
  }, [query]);

  const visibleResults = query.trim() ? results : [];

  if (selected) {
    return (
      <div className="flex items-center gap-2 rounded-xl border border-cyan-400/25 bg-cyan-500/10 px-3 py-1.5 text-xs text-cyan-200">
        <span className="min-w-0 truncate">Gắn đề: {selected.title}</span>
        <button type="button" onClick={() => onSelect(null)} aria-label="Bỏ gắn đề" className="shrink-0 text-cyan-300 hover:text-white">
          <X size={13} />
        </button>
      </div>
    );
  }

  return (
    <div className="relative">
      <input
        value={query}
        onChange={(event) => setQuery(event.target.value)}
        placeholder="Tìm đề để gắn nút Làm bài (tuỳ chọn)…"
        className="w-full rounded-xl border border-white/10 bg-panel-deep px-3 py-1.5 text-xs text-white placeholder:text-slate-600"
      />
      {visibleResults.length > 0 && (
        <ul className="absolute z-10 mt-1 w-full overflow-hidden rounded-xl border border-white/10 bg-panel-deep shadow-lg">
          {visibleResults.map((exam) => (
            <li key={exam.id}>
              <button
                type="button"
                onClick={() => {
                  onSelect(exam);
                  setQuery("");
                  setResults([]);
                }}
                className="block w-full truncate px-3 py-2 text-left text-xs text-slate-200 hover:bg-white/5"
              >
                {exam.title}
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

const KIND_META: Record<AnnouncementKind, { label: string; placeholder: string }> = {
  today_task: { label: "Việc cần làm hôm nay", placeholder: "VD: Hoàn thành trắc nghiệm Bài 9 trước 21h…" },
  homework: { label: "Bài tập về nhà", placeholder: "VD: Làm câu 1-10 trang 45, nộp qua Zalo lớp…" },
};

function AnnouncementColumn({ classId, kind }: { classId: number; kind: AnnouncementKind }) {
  const { profile } = useAuth();
  const toast = useToast();
  const [items, setItems] = useState<ClassAnnouncement[] | null>(null);
  const [draft, setDraft] = useState("");
  const [exam, setExam] = useState<ExamOption | null>(null);
  const [busy, setBusy] = useState(false);
  const [checkingId, setCheckingId] = useState<number | null>(null);

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
      await postAnnouncement({ classId, kind, body: draft, createdBy: profile.id, examId: exam?.id ?? null });
      setDraft("");
      setExam(null);
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
    <section className="rounded-2xl border border-white/10 bg-panel p-4 sm:p-5">
      <h3 className="font-display font-bold text-white">{meta.label}</h3>
      <div className="mt-3 flex flex-col gap-2">
        <div className="flex flex-col gap-2 sm:flex-row">
          <textarea
            value={draft}
            onChange={(event) => setDraft(event.target.value)}
            placeholder={meta.placeholder}
            rows={2}
            className="flex-1 rounded-xl border border-white/10 bg-panel-deep px-3 py-2 text-sm text-white placeholder:text-slate-600"
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
        <ExamPicker selected={exam} onSelect={setExam} />
      </div>
      <div className="mt-3 space-y-2">
        {items === null ? (
          <p className="text-xs text-slate-500">Đang tải…</p>
        ) : items.length === 0 ? (
          <p className="text-xs text-slate-500">Chưa có thông báo nào.</p>
        ) : (
          items.map((item) => (
            <div key={item.id} className="rounded-xl bg-white/[.02] p-3">
              <div className="flex items-start justify-between gap-3">
                <div className="min-w-0">
                  <p className="whitespace-pre-wrap text-sm text-slate-200">{item.body}</p>
                  {item.examTitle && (
                    <p className="mt-1 truncate text-[12px] font-semibold text-cyan-300">Đề: {item.examTitle}</p>
                  )}
                  <p className="mt-1 text-[12px] text-slate-500">
                    {item.createdByName || "—"} ·{" "}
                    {new Date(item.createdAt).toLocaleString("vi-VN", {
                      day: "2-digit",
                      month: "2-digit",
                      hour: "2-digit",
                      minute: "2-digit",
                    })}
                  </p>
                </div>
                <div className="flex shrink-0 items-center gap-2">
                  {kind === "homework" && (
                    <button
                      type="button"
                      onClick={() => setCheckingId((current) => (current === item.id ? null : item.id))}
                      aria-label="Chấm BTVN"
                      title="Chấm % học sinh đã làm"
                      className={checkingId === item.id ? "text-cyan-300" : "text-slate-500 hover:text-cyan-300"}
                    >
                      <ClipboardCheck size={14} />
                    </button>
                  )}
                  <button
                    type="button"
                    onClick={() => remove(item.id)}
                    aria-label="Xoá thông báo"
                    className="text-slate-500 hover:text-red-300"
                  >
                    <Trash2 size={14} />
                  </button>
                </div>
              </div>
              {kind === "homework" && checkingId === item.id && (
                <div className="mt-3">
                  <HomeworkCheckPanel announcementId={item.id} classId={classId} />
                </div>
              )}
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
