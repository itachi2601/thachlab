"use client";

import { useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/components/auth/AuthProvider";
import { useToast } from "@/components/ui/Toast";
import { quizErrorText } from "@/features/quiz-live/types";
import { createRoom, deleteQuizSet, fetchQuizSets, type QuizSet } from "@/services/quiz-live";
import QuizSetEditor from "./QuizSetEditor";

const btn = "min-h-11 rounded-xl border border-line px-4 text-sm font-semibold text-ink hover:bg-surface-2";

/** /tro-giang/do-vui — danh sách bộ câu, soạn bộ mới, mở phòng chơi. Dành cho admin / giảng viên / trợ giảng. */
export default function QuizHostHome() {
  const { profile, loading } = useAuth();
  const toast = useToast();
  const router = useRouter();
  const [sets, setSets] = useState<QuizSet[] | null>(null);
  const [view, setView] = useState<{ kind: "list" } | { kind: "edit"; set: QuizSet | null }>({ kind: "list" });
  const [seconds, setSeconds] = useState(20);
  const [busyId, setBusyId] = useState<number | null>(null);

  const allowed = profile?.role === "admin" || profile?.role === "instructor" || profile?.role === "tro_giang";

  const load = useCallback(async () => {
    try {
      setSets(await fetchQuizSets());
    } catch (e) {
      setSets([]);
      toast("error", quizErrorText(e));
    }
  }, [toast]);
  useEffect(() => {
    if (allowed) setTimeout(() => void load(), 0);
  }, [allowed, load]);

  async function play(id: number) {
    setBusyId(id);
    try {
      const r = await createRoom(id, seconds);
      router.push(`/tro-giang/do-vui/phong?id=${r.room_id}`);
    } catch (e) {
      toast("error", quizErrorText(e));
      setBusyId(null);
    }
  }

  if (loading) return <p className="text-muted">Đang tải…</p>;
  if (!allowed) return <p className="text-ink">Trang này dành cho thầy/cô và trợ giảng.</p>;

  if (view.kind === "edit")
    return (
      <QuizSetEditor
        key={view.set?.id ?? "new"}
        initial={view.set}
        onBack={() => { setView({ kind: "list" }); void load(); }}
        onSaved={(id, doPlay) => { if (doPlay) void play(id); else void load(); }}
      />
    );

  return (
    <div className="space-y-5">
      <div className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <h1 className="font-display text-2xl font-bold text-ink">Đố vui lớp học</h1>
          <p className="mt-1 text-sm text-muted">Chiếu câu hỏi lên màn hình, học sinh vào bằng mã PIN trên điện thoại.</p>
        </div>
        <button onClick={() => setView({ kind: "edit", set: null })} className="min-h-11 rounded-xl bg-primary px-5 font-bold text-white">+ Bộ câu mới</button>
      </div>

      <label className="flex items-center gap-2 text-sm text-ink">
        Thời gian mỗi câu
        <select className="rounded-xl border border-line-strong bg-panel px-3 py-2 text-ink" value={seconds} onChange={(e) => setSeconds(Number(e.target.value))}>
          {[10, 20, 30, 45, 60, 90].map((s) => <option key={s} value={s}>{s} giây</option>)}
        </select>
      </label>

      {sets === null && <p className="text-muted">Đang tải…</p>}
      {sets?.length === 0 && <p className="rounded-2xl border border-dashed border-line p-6 text-center text-muted">Chưa có bộ câu nào. Bấm “Bộ câu mới” để soạn hoặc bốc từ ngân hàng.</p>}
      <ul className="space-y-3">
        {sets?.map((s) => (
          <li key={s.id} className="flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-line bg-panel p-4">
            <div className="min-w-0">
              <p className="truncate font-semibold text-ink">{s.title}</p>
              <p className="text-xs text-muted">{s.questions.length} câu{s.grade ? ` · lớp ${s.grade}` : ""}{s.bankedAt ? " · đã đưa vào ngân hàng" : ""}</p>
            </div>
            <div className="flex gap-2">
              <button disabled={busyId !== null || s.questions.length === 0} onClick={() => void play(s.id)} className="min-h-11 rounded-xl bg-primary px-5 font-bold text-white disabled:opacity-40">{busyId === s.id ? "Đang mở…" : "Chơi"}</button>
              <button onClick={() => setView({ kind: "edit", set: s })} className={btn}>Sửa</button>
              <button
                onClick={async () => {
                  if (!confirm(`Xoá bộ “${s.title}”?`)) return;
                  try { await deleteQuizSet(s.id); void load(); } catch (e) { toast("error", quizErrorText(e)); }
                }}
                className={btn}
              >Xoá</button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
