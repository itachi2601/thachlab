"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import { Check, Loader2, X } from "lucide-react";
import { useToast } from "@/components/ui/Toast";
import { SESSION_TYPE_META } from "@/lib/tro-giang/constants";
import {
  createSession,
  fetchTopicSuggestion,
  type TaAssistant,
  type TaSessionType,
  type TaTopicSuggestion,
  type TaVideoTier,
} from "@/lib/tro-giang/queries";

const DRAFT_KEY = "tro-giang-ghi-draft-v1";
const TOUCH_TARGET = 12;

const TYPE_OPTIONS = (Object.keys(SESSION_TYPE_META) as TaSessionType[]).map((value) => ({
  value,
  ...SESSION_TYPE_META[value],
}));

const TIME_CHIPS = ["16:30", "17:00", "17:30", "18:00", "18:30", "19:00", "19:30", "20:00", "20:30", "21:00"];

function todayStr() {
  return new Date().toLocaleDateString("sv-SE"); // yyyy-mm-dd theo giờ máy
}

interface Draft {
  sessionType: TaSessionType;
  workDate: string;
  classLabel: string;
  startTime: string | null;
  endTime: string | null;
  touchNames: string[];
  errorNote: string;
  homeworkGiven: string;
  studentRecapOk: boolean;
  papersGraded: string;
  videoUrl: string;
  videoTier: TaVideoTier | null;
  publishedAt: string;
  note: string;
}

function emptyDraft(): Draft {
  return {
    sessionType: "lop",
    workDate: todayStr(),
    classLabel: "",
    startTime: null,
    endTime: null,
    touchNames: [],
    errorNote: "",
    homeworkGiven: "",
    studentRecapOk: false,
    papersGraded: "",
    videoUrl: "",
    videoTier: null,
    publishedAt: todayStr(),
    note: "",
  };
}

function loadDraft(): Draft {
  if (typeof window === "undefined") return emptyDraft();
  try {
    const raw = window.localStorage.getItem(DRAFT_KEY);
    if (!raw) return emptyDraft();
    return { ...emptyDraft(), ...JSON.parse(raw) };
  } catch {
    return emptyDraft();
  }
}

function TimeChips({
  value,
  onChange,
  label,
}: {
  value: string | null;
  onChange: (v: string) => void;
  label: string;
}) {
  const [customOpen, setCustomOpen] = useState(false);
  return (
    <div>
      <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-400">{label}</p>
      <div className="flex flex-wrap gap-2">
        {TIME_CHIPS.map((t) => (
          <button
            key={t}
            type="button"
            onClick={() => {
              onChange(t);
              setCustomOpen(false);
            }}
            className={`rounded-full border px-3.5 py-2 font-mono text-sm tabular-nums transition ${
              value === t
                ? "border-blue-500 bg-blue-600 text-white"
                : "border-white/10 bg-white/5 text-slate-300 active:bg-white/10"
            }`}
          >
            {t}
          </button>
        ))}
        <button
          type="button"
          onClick={() => setCustomOpen((v) => !v)}
          className={`rounded-full border px-3.5 py-2 text-sm transition ${
            customOpen || (value && !TIME_CHIPS.includes(value))
              ? "border-blue-500 bg-blue-600 text-white"
              : "border-dashed border-white/20 text-slate-400"
          }`}
        >
          Giờ khác…
        </button>
      </div>
      {(customOpen || (value && !TIME_CHIPS.includes(value))) && (
        <input
          type="time"
          value={value ?? ""}
          onChange={(e) => onChange(e.target.value)}
          className="mt-2 w-full rounded-xl border border-white/10 bg-white/5 px-4 py-2.5 font-mono text-white tabular-nums"
        />
      )}
    </div>
  );
}

function TouchNamesInput({ names, onChange }: { names: string[]; onChange: (n: string[]) => void }) {
  const [text, setText] = useState("");
  const reachedTarget = names.length >= TOUCH_TARGET;

  const commit = useCallback(() => {
    const v = text.trim();
    if (!v) return;
    if (!names.includes(v)) onChange([...names, v]);
    setText("");
  }, [text, names, onChange]);

  return (
    <div>
      <div className="mb-2 flex items-center justify-between">
        <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">Học sinh đã gỡ bài</p>
        <span
          className={`rounded-full px-2.5 py-1 font-mono text-xs font-bold tabular-nums transition-colors ${
            reachedTarget
              ? "bg-emerald-500/20 text-emerald-300"
              : "bg-amber-500/15 text-amber-300"
          }`}
        >
          {names.length}/{TOUCH_TARGET}
        </span>
      </div>
      <div className="flex flex-wrap gap-2 rounded-2xl border border-white/10 bg-white/5 p-3">
        {names.map((n) => (
          <span
            key={n}
            className="flex items-center gap-1.5 rounded-full bg-blue-600/20 py-1.5 pl-3 pr-1.5 text-sm font-medium text-blue-200"
          >
            {n}
            <button
              type="button"
              onClick={() => onChange(names.filter((x) => x !== n))}
              className="rounded-full p-0.5 hover:bg-white/10"
              aria-label={`Bỏ ${n}`}
            >
              <X size={13} />
            </button>
          </span>
        ))}
        <input
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" || e.key === ",") {
              e.preventDefault();
              commit();
            } else if (e.key === "Backspace" && !text && names.length > 0) {
              onChange(names.slice(0, -1));
            }
          }}
          onBlur={commit}
          placeholder="Gõ tên rồi Enter…"
          className="min-w-[140px] flex-1 bg-transparent py-1.5 text-sm text-white outline-none placeholder:text-slate-500"
        />
      </div>
    </div>
  );
}

export default function GhiBuoiForm({
  assistant,
  initialTopicId,
}: {
  assistant: TaAssistant;
  initialTopicId?: string | null;
}) {
  const toast = useToast();
  const [draft, setDraft] = useState<Draft>(() => {
    const d = loadDraft();
    // Đến từ /tro-giang/video?topic=<id> — chuyển thẳng sang loại "video" kèm đề tài điền sẵn.
    if (initialTopicId) d.sessionType = "video";
    return d;
  });
  const [topicSourceId, setTopicSourceId] = useState<string | null>(initialTopicId ?? null);
  const [topicInfo, setTopicInfo] = useState<TaTopicSuggestion | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [justSaved, setJustSaved] = useState(false);
  const hydrated = useRef(false);

  useEffect(() => {
    if (!initialTopicId) return;
    fetchTopicSuggestion(initialTopicId)
      .then((info) => setTopicInfo(info))
      .catch(() => {});
  }, [initialTopicId]);

  // Lưu nháp — bỏ qua lần render đầu (vừa load từ localStorage lên, khỏi ghi lại chính nó).
  useEffect(() => {
    if (!hydrated.current) {
      hydrated.current = true;
      return;
    }
    if (justSaved) return;
    try {
      window.localStorage.setItem(DRAFT_KEY, JSON.stringify(draft));
    } catch {
      // localStorage đầy/bị chặn — bỏ qua, không chặn việc nhập liệu.
    }
  }, [draft, justSaved]);

  function patch(fields: Partial<Draft>) {
    setJustSaved(false);
    setDraft((d) => ({ ...d, ...fields }));
  }

  const needsTime = draft.sessionType !== "video";
  const timeValid =
    !needsTime || (draft.startTime && draft.endTime && draft.endTime > draft.startTime);

  const validationError = useMemo(() => {
    if (!draft.workDate) return "Chọn ngày làm việc.";
    if (needsTime && (!draft.startTime || !draft.endTime)) return "Chọn giờ bắt đầu và kết thúc.";
    if (needsTime && draft.startTime && draft.endTime && draft.endTime <= draft.startTime)
      return "Giờ kết thúc phải sau giờ bắt đầu.";
    if (draft.sessionType === "lop" && !draft.errorNote.trim())
      return "Buổi lên lớp bắt buộc phải ghi lỗi sai lặp lại của lớp.";
    if (draft.sessionType === "chambai" && !(Number(draft.papersGraded) > 0))
      return "Nhập số bài đã chấm.";
    if (draft.sessionType === "video") {
      if (!draft.videoUrl.trim()) return "Dán link video đã đăng.";
      if (!draft.videoTier) return "Chọn loại video: đơn giản hay dựng kỹ.";
    }
    return null;
  }, [draft, needsTime]);

  async function submit() {
    if (validationError) {
      toast("error", validationError);
      return;
    }
    setSubmitting(true);
    try {
      await createSession({
        assistant_id: assistant.id,
        work_date: draft.workDate,
        session_type: draft.sessionType,
        class_label: draft.classLabel.trim() || null,
        start_time: needsTime ? draft.startTime : null,
        end_time: needsTime ? draft.endTime : null,
        student_touches: draft.sessionType === "lop" ? draft.touchNames.length : null,
        touch_names: draft.sessionType === "lop" ? draft.touchNames : [],
        error_note: draft.sessionType === "lop" ? draft.errorNote.trim() : null,
        homework_given: draft.sessionType === "phudao" ? draft.homeworkGiven.trim() || null : null,
        student_recap_ok: draft.sessionType === "phudao" ? draft.studentRecapOk : null,
        papers_graded: draft.sessionType === "chambai" ? Number(draft.papersGraded) : null,
        video_url: draft.sessionType === "video" ? draft.videoUrl.trim() : null,
        video_tier: draft.sessionType === "video" ? draft.videoTier : null,
        published_at:
          draft.sessionType === "video" && draft.publishedAt
            ? new Date(`${draft.publishedAt}T12:00:00`).toISOString()
            : null,
        topic_source_id: draft.sessionType === "video" ? topicSourceId : null,
        note: draft.note.trim() || null,
      });
      toast("success", "Đã ghi buổi làm việc — chờ giáo viên duyệt.");
      setJustSaved(true);
      try {
        window.localStorage.removeItem(DRAFT_KEY);
      } catch {}
      const type = draft.sessionType;
      setDraft({ ...emptyDraft(), sessionType: type });
      setTopicSourceId(null);
      setTopicInfo(null);
    } catch (error) {
      toast("error", error instanceof Error ? error.message : "Không lưu được, thử lại.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="pb-28">
      <div className="mb-5 flex gap-2 overflow-x-auto pb-1">
        {TYPE_OPTIONS.map(({ value, label, icon: Icon }) => (
          <button
            key={value}
            type="button"
            onClick={() => patch({ sessionType: value })}
            className={`flex shrink-0 items-center gap-2 rounded-2xl border px-4 py-3 text-sm font-bold transition ${
              draft.sessionType === value
                ? "border-blue-500 bg-blue-600 text-white"
                : "border-white/10 bg-white/5 text-slate-300"
            }`}
          >
            <Icon size={16} />
            {label}
          </button>
        ))}
      </div>

      <div className="flex flex-col gap-5">
        {draft.sessionType === "video" && topicInfo && (
          <div className="rounded-2xl border border-amber-400/30 bg-amber-500/10 p-4 text-sm text-amber-100">
            <p className="font-bold">Đề tài từ buổi {topicInfo.work_date}{topicInfo.class_label ? ` · ${topicInfo.class_label}` : ""}</p>
            <p className="mt-1 text-amber-200/90">{topicInfo.error_note}</p>
          </div>
        )}

        <div>
          <label className="mb-2 block text-xs font-semibold uppercase tracking-wide text-slate-400">
            Ngày
          </label>
          <input
            type="date"
            value={draft.workDate}
            onChange={(e) => patch({ workDate: e.target.value })}
            className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-white"
          />
        </div>

        {draft.sessionType !== "video" && draft.sessionType !== "hanhchinh" && (
          <div>
            <label className="mb-2 block text-xs font-semibold uppercase tracking-wide text-slate-400">
              {draft.sessionType === "phudao" ? "Tên học sinh" : "Lớp"}
            </label>
            <input
              value={draft.classLabel}
              onChange={(e) => patch({ classLabel: e.target.value })}
              placeholder={draft.sessionType === "phudao" ? "Nguyễn Văn A" : "12A2"}
              className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-white placeholder:text-slate-500"
            />
          </div>
        )}

        {needsTime && (
          <>
            <TimeChips label="Giờ bắt đầu" value={draft.startTime} onChange={(t) => patch({ startTime: t })} />
            <TimeChips label="Giờ kết thúc" value={draft.endTime} onChange={(t) => patch({ endTime: t })} />
            {!timeValid && draft.startTime && draft.endTime && (
              <p className="-mt-3 text-xs font-medium text-red-300">Giờ kết thúc phải sau giờ bắt đầu.</p>
            )}
          </>
        )}

        {draft.sessionType === "lop" && (
          <>
            <TouchNamesInput names={draft.touchNames} onChange={(n) => patch({ touchNames: n })} />
            <div>
              <label className="mb-2 block text-xs font-semibold uppercase tracking-wide text-slate-400">
                Lỗi sai lặp lại của lớp <span className="text-red-400">*</span>
              </label>
              <textarea
                value={draft.errorNote}
                onChange={(e) => patch({ errorNote: e.target.value })}
                rows={3}
                placeholder="Ví dụ: sai dấu khi chuyển vế, nhầm công thức chu kỳ…"
                className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-white placeholder:text-slate-500"
              />
            </div>
          </>
        )}

        {draft.sessionType === "phudao" && (
          <>
            <div>
              <label className="mb-2 block text-xs font-semibold uppercase tracking-wide text-slate-400">
                Các câu đã giao
              </label>
              <textarea
                value={draft.homeworkGiven}
                onChange={(e) => patch({ homeworkGiven: e.target.value })}
                rows={2}
                placeholder="Bài 5, 6, 7 trang 42…"
                className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-white placeholder:text-slate-500"
              />
            </div>
            <button
              type="button"
              onClick={() => patch({ studentRecapOk: !draft.studentRecapOk })}
              className="flex items-center justify-between rounded-2xl border border-white/10 bg-white/5 px-4 py-3.5"
            >
              <span className="text-sm font-medium text-white">Học sinh tự trình bày lại được</span>
              <span
                className={`relative h-7 w-12 shrink-0 rounded-full transition-colors ${
                  draft.studentRecapOk ? "bg-emerald-500" : "bg-white/15"
                }`}
              >
                <span
                  className={`absolute top-0.5 h-6 w-6 rounded-full bg-white shadow transition-transform ${
                    draft.studentRecapOk ? "translate-x-5" : "translate-x-0.5"
                  }`}
                />
              </span>
            </button>
          </>
        )}

        {draft.sessionType === "chambai" && (
          <div>
            <label className="mb-2 block text-xs font-semibold uppercase tracking-wide text-slate-400">
              Số bài đã chấm
            </label>
            <input
              type="number"
              inputMode="numeric"
              min={0}
              value={draft.papersGraded}
              onChange={(e) => patch({ papersGraded: e.target.value })}
              className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 font-mono text-white tabular-nums"
            />
          </div>
        )}

        {draft.sessionType === "video" && (
          <>
            <div>
              <label className="mb-2 block text-xs font-semibold uppercase tracking-wide text-slate-400">
                Link video đã đăng
              </label>
              <input
                value={draft.videoUrl}
                onChange={(e) => patch({ videoUrl: e.target.value })}
                placeholder="https://www.tiktok.com/@..."
                className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-white placeholder:text-slate-500"
              />
            </div>
            <div>
              <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-400">Loại video</p>
              <div className="flex gap-2">
                {(
                  [
                    ["don_gian", "Đơn giản"],
                    ["dung_ky", "Dựng kỹ"],
                  ] as [TaVideoTier, string][]
                ).map(([value, label]) => (
                  <button
                    key={value}
                    type="button"
                    onClick={() => patch({ videoTier: value })}
                    className={`flex-1 rounded-xl border px-4 py-3 text-sm font-bold transition ${
                      draft.videoTier === value
                        ? "border-blue-500 bg-blue-600 text-white"
                        : "border-white/10 bg-white/5 text-slate-300"
                    }`}
                  >
                    {label}
                  </button>
                ))}
              </div>
            </div>
            <div>
              <label className="mb-2 block text-xs font-semibold uppercase tracking-wide text-slate-400">
                Ngày đăng
              </label>
              <input
                type="date"
                value={draft.publishedAt}
                onChange={(e) => patch({ publishedAt: e.target.value })}
                className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-white"
              />
            </div>
          </>
        )}

        <div>
          <label className="mb-2 block text-xs font-semibold uppercase tracking-wide text-slate-400">
            Ghi chú thêm (không bắt buộc)
          </label>
          <textarea
            value={draft.note}
            onChange={(e) => patch({ note: e.target.value })}
            rows={2}
            className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-white"
          />
        </div>
      </div>

      <div className="fixed inset-x-0 bottom-0 z-40 border-t border-white/10 bg-[#05070B]/95 p-4 backdrop-blur-md">
        <div className="mx-auto flex max-w-lg gap-2">
          <button
            type="button"
            disabled={submitting || !!validationError}
            onClick={submit}
            className="flex flex-1 items-center justify-center gap-2 rounded-2xl bg-blue-600 py-4 text-base font-bold text-white transition disabled:cursor-not-allowed disabled:opacity-40"
          >
            {submitting ? (
              <Loader2 size={18} className="animate-spin" />
            ) : justSaved ? (
              <Check size={18} />
            ) : null}
            {submitting ? "Đang lưu…" : justSaved ? "Đã lưu — Ghi buổi tiếp theo" : "Lưu buổi"}
          </button>
          {justSaved && (
            <Link
              href="/tro-giang"
              className="flex shrink-0 items-center justify-center rounded-2xl border border-white/15 px-5 text-sm font-bold text-slate-200"
            >
              Về trang chính
            </Link>
          )}
        </div>
      </div>
    </div>
  );
}
