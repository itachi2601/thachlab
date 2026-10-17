"use client";

import { useEffect, useMemo, useState } from "react";
import { Check, Loader2, Send, X } from "lucide-react";
import { fetchQuestionTopics } from "@/services/analytics";
import { assignHomework, searchExams, type ExamOption } from "@/services/ta-homework";
import { useToast } from "@/components/ui/Toast";

export interface HomeworkStudent {
  id: string;
  name: string;
}

/** Hạn mặc định: 21h tối ngày thứ 3 sau hôm nay (giờ máy), định dạng ô datetime-local. */
function defaultDue(): string {
  const d = new Date();
  d.setDate(d.getDate() + 3);
  d.setHours(21, 0, 0, 0);
  const pad = (n: number) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
}

/**
 * Bước "Giao bài về nhà" trong phiếu phụ đạo: giao một đề cho các em vừa kèm, em thấy ở chuông + thẻ "Hôm nay".
 * Gợi ý đề theo đúng chủ đề vừa dạy (tên bài/yêu cầu cần đạt); trợ giảng vẫn tự tìm theo tên đề được.
 */
export default function TaAssignHomework({
  classId,
  students,
  taughtTopicIds,
  demo,
}: {
  classId: number | null;
  students: HomeworkStudent[];
  taughtTopicIds: number[];
  demo: boolean;
}) {
  const toast = useToast();
  const [topicNames, setTopicNames] = useState<string[]>([]);
  const [suggestions, setSuggestions] = useState<ExamOption[]>([]);
  const [query, setQuery] = useState("");
  const [found, setFound] = useState<ExamOption[]>([]);
  const [exam, setExam] = useState<ExamOption | null>(null);
  const [picked, setPicked] = useState<Set<string>>(new Set());
  const [due, setDue] = useState(defaultDue);
  const [note, setNote] = useState("");
  const [busy, setBusy] = useState(false);
  const [sentCount, setSentCount] = useState<number | null>(null);

  const studentKey = students.map((s) => s.id).join(",");
  // Mặc định giao cho tất cả em đang được chọn trong phiếu; trợ giảng bỏ tick em nào thì không giao em đó.
  useEffect(() => {
    setPicked(new Set(students.map((s) => s.id)));
    setSentCount(null);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [studentKey]);

  const topicKey = taughtTopicIds.join(",");
  useEffect(() => {
    if (demo || taughtTopicIds.length === 0) {
      setTopicNames([]);
      return;
    }
    let alive = true;
    fetchQuestionTopics()
      .then((all) => {
        if (!alive) return;
        const wanted = new Set(taughtTopicIds);
        setTopicNames(Array.from(new Set(all.filter((t) => wanted.has(t.id)).map((t) => t.name))).slice(0, 6));
      })
      .catch(() => alive && setTopicNames([]));
    return () => {
      alive = false;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [topicKey, demo]);

  useEffect(() => {
    if (demo || topicNames.length === 0) {
      setSuggestions([]);
      return;
    }
    let alive = true;
    searchExams(topicNames, 5)
      .then((rows) => alive && setSuggestions(rows))
      .catch(() => alive && setSuggestions([]));
    return () => {
      alive = false;
    };
  }, [topicNames, demo]);

  useEffect(() => {
    const trimmed = query.trim();
    if (demo || !trimmed) {
      setFound([]);
      return;
    }
    let alive = true;
    const timer = setTimeout(() => {
      searchExams([trimmed], 8)
        .then((rows) => alive && setFound(rows))
        .catch(() => alive && setFound([]));
    }, 300);
    return () => {
      alive = false;
      clearTimeout(timer);
    };
  }, [query, demo]);

  const targets = useMemo(() => students.filter((s) => picked.has(s.id)), [students, picked]);
  const canSend = !demo && !busy && classId !== null && exam !== null && targets.length > 0;

  function toggle(id: string) {
    setPicked((current) => {
      const next = new Set(current);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  }

  async function send() {
    if (!canSend || classId === null || exam === null) return;
    setBusy(true);
    try {
      const count = await assignHomework({
        classId,
        studentIds: targets.map((s) => s.id),
        examId: exam.id,
        dueAt: due ? new Date(due).toISOString() : null,
        note,
      });
      setSentCount(count);
      setExam(null);
      setNote("");
      toast("success", `Đã giao bài cho ${count} em. Các em nhận chuông thông báo.`);
    } catch (e) {
      toast("error", e instanceof Error ? e.message : "Chưa giao được bài.");
    } finally {
      setBusy(false);
    }
  }

  if (students.length === 0) return null;

  const options = query.trim() ? found : suggestions;

  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
      <h3 className="font-display font-bold text-white">Giao bài về nhà trên web</h3>
      <p className="mt-1 text-xs text-slate-400">
        Em nhận chuông thông báo và thấy bài ở trang chủ cho tới khi nộp. Không cần báo miệng.
      </p>

      <div className="mt-3 flex flex-wrap gap-2">
        {students.map((s) => {
          const on = picked.has(s.id);
          return (
            <button
              key={s.id}
              type="button"
              onClick={() => toggle(s.id)}
              aria-pressed={on}
              className={`inline-flex min-h-11 items-center gap-1.5 rounded-full border px-3.5 text-sm font-semibold ${
                on ? "border-blue-400/50 bg-blue-500/15 text-blue-200" : "border-white/10 text-slate-400"
              }`}
            >
              {on && <Check size={14} />}
              {s.name || "Học sinh"}
            </button>
          );
        })}
      </div>

      <div className="mt-3">
        {exam ? (
          <div className="flex items-center gap-2 rounded-xl border border-cyan-400/25 bg-cyan-500/10 px-3 py-2 text-sm text-cyan-200">
            <span className="min-w-0 flex-1 truncate">Đề: {exam.title}</span>
            <button type="button" onClick={() => setExam(null)} aria-label="Bỏ chọn đề" className="inline-flex min-h-11 min-w-11 shrink-0 items-center justify-center text-cyan-300">
              <X size={16} />
            </button>
          </div>
        ) : (
          <>
            <input
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Tìm đề theo tên…"
              className="w-full rounded-xl border border-white/10 bg-panel-deep px-3 py-2.5 text-sm text-white placeholder:text-slate-500"
            />
            {options.length > 0 && (
              <>
                {!query.trim() && (
                  <p className="mt-2 text-xs font-semibold text-slate-400">Gợi ý theo chủ đề vừa dạy: {topicNames.join(", ")}</p>
                )}
                <ul className="mt-2 space-y-1">
                  {options.map((item) => (
                    <li key={item.id}>
                      <button
                        type="button"
                        onClick={() => {
                          setExam(item);
                          setQuery("");
                        }}
                        className="block min-h-11 w-full rounded-xl border border-white/10 px-3 py-2 text-left text-sm text-slate-200 hover:bg-white/5"
                      >
                        {item.title}
                      </button>
                    </li>
                  ))}
                </ul>
              </>
            )}
            {!query.trim() && options.length === 0 && topicNames.length > 0 && (
              <p className="mt-2 text-xs text-slate-500">Chưa có đề khớp chủ đề vừa dạy, hãy tìm theo tên đề.</p>
            )}
          </>
        )}
      </div>

      <div className="mt-3 grid gap-3 sm:grid-cols-2">
        <label className="block text-xs font-semibold text-slate-400">
          Hạn nộp
          <input
            type="datetime-local"
            value={due}
            onChange={(event) => setDue(event.target.value)}
            className="mt-1 w-full rounded-xl border border-white/10 bg-panel-deep px-3 py-2.5 text-sm text-white"
          />
        </label>
        <label className="block text-xs font-semibold text-slate-400">
          Dặn thêm (tuỳ chọn)
          <input
            value={note}
            onChange={(event) => setNote(event.target.value.slice(0, 200))}
            placeholder="Làm câu 1–8 trước, chưa chắc thì xem lại bài"
            className="mt-1 w-full rounded-xl border border-white/10 bg-panel-deep px-3 py-2.5 text-sm text-white placeholder:text-slate-500"
          />
        </label>
      </div>

      <button
        type="button"
        onClick={send}
        disabled={!canSend}
        className="mt-4 inline-flex min-h-11 items-center gap-2 rounded-xl bg-blue-600 px-5 text-sm font-bold text-white disabled:opacity-40"
      >
        {busy ? <Loader2 size={16} className="animate-spin" /> : <Send size={16} />}
        Giao cho {targets.length} em
      </button>
      {demo && <p className="mt-2 text-xs text-slate-500">Chế độ giả lập không ghi dữ liệu thật.</p>}
      {sentCount !== null && <p className="mt-2 text-xs text-emerald-300">Đã giao cho {sentCount} em.</p>}
    </div>
  );
}
