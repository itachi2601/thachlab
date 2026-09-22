"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { BookOpenCheck, Check, ChevronRight, Sparkles } from "lucide-react";
import { useToast } from "@/components/ui/Toast";
import { fetchQuestionTopics, type QuestionTopic } from "@/services/analytics";
import {
  cancelRegistration,
  fetchMyRegistrations as fetchMySlotRegistrations,
  fetchUpcomingSlots,
  registerForSlot,
  type TutoringSlot,
} from "@/services/tutoring";
import { fetchCatchupForStudent, type MyRegistration } from "@/services/thpt-courses";

/**
 * Em vào lớp trễ: danh sách bài cần bù (gần nhất trước), bài đã bù, và các ca phụ đạo trong
 * lịch tuần của trợ giảng khối — ca nào dạy đúng bài kế tiếp được gợi ý lên đầu.
 * Dùng ở trang học sinh (viewer = student, tự đăng ký) và trang phụ huynh (viewer = parent,
 * đăng ký hộ con — policy "parent registers child" trong supabase-migration-bu-bai.sql).
 * Không có đăng ký đang bù bài thì không hiện gì.
 */
export default function CatchupCard({
  studentId,
  classId,
  viewer,
}: {
  studentId: string;
  classId: number | null;
  viewer: "student" | "parent";
}) {
  const toast = useToast();
  const [reg, setReg] = useState<MyRegistration | null | undefined>(undefined);
  const [topics, setTopics] = useState<QuestionTopic[]>([]);
  const [slots, setSlots] = useState<TutoringSlot[]>([]);
  const [mine, setMine] = useState<Set<number>>(new Set());
  const [busySlot, setBusySlot] = useState<number | null>(null);

  const reload = useCallback(() => {
    fetchCatchupForStudent(studentId).then(setReg).catch(() => setReg(null));
    if (classId !== null) {
      fetchUpcomingSlots(classId).then(setSlots).catch(() => setSlots([]));
      fetchMySlotRegistrations(studentId).then((ids) => setMine(new Set(ids))).catch(() => setMine(new Set()));
    }
  }, [studentId, classId]);

  useEffect(() => {
    reload();
  }, [reload]);

  useEffect(() => {
    if (!reg) return;
    fetchQuestionTopics().then(setTopics).catch(() => setTopics([]));
  }, [reg]);

  const topicName = useMemo(() => new Map(topics.map((t) => [t.id, t.name])), [topics]);

  const { ordered, nextId } = useMemo(() => {
    if (!reg) return { ordered: [] as number[], nextId: null as number | null };
    return { ordered: reg.catchup_topic_ids, nextId: reg.catchup_topic_ids[0] ?? null };
  }, [reg]);

  const { suggested, others } = useMemo(() => {
    const want = new Set(ordered);
    const s: TutoringSlot[] = [];
    const o: TutoringSlot[] = [];
    for (const slot of slots) (slot.topicIds.some((t) => want.has(t)) ? s : o).push(slot);
    // Ca dạy đúng bài kế tiếp lên trước, rồi các ca dạy bài khác trong danh sách bù.
    s.sort((a, b) => Number(b.topicIds.includes(nextId ?? -1)) - Number(a.topicIds.includes(nextId ?? -1)));
    return { suggested: s, others: o };
  }, [slots, ordered, nextId]);

  if (!reg) return null;

  const who = viewer === "parent" ? "con" : "em";

  async function toggle(slot: TutoringSlot) {
    setBusySlot(slot.id);
    try {
      if (mine.has(slot.id)) {
        await cancelRegistration(slot.id, studentId);
        toast("success", "Đã huỷ đăng ký ca này.");
      } else {
        await registerForSlot(slot.id, studentId);
        toast("success", "Đã đăng ký ca phụ đạo.");
      }
      reload();
    } catch (error) {
      toast("error", error instanceof Error ? error.message : "Chưa cập nhật được.");
    } finally {
      setBusySlot(null);
    }
  }

  function renderSlot(slot: TutoringSlot, highlight: boolean) {
    const registered = mine.has(slot.id);
    const full = slot.registeredCount >= slot.capacity && !registered;
    const date = new Date(`${slot.workDate}T00:00:00`).toLocaleDateString("vi-VN", { weekday: "short", day: "2-digit", month: "2-digit" });
    const slotTopics = slot.topicIds.map((t) => topicName.get(t)).filter(Boolean) as string[];
    return (
      <div key={slot.id} className={`rounded-xl border p-3 ${highlight ? "border-blue-400/40 bg-blue-500/[.06]" : "border-white/10 bg-white/[.02]"}`}>
        <div className="flex flex-wrap items-center gap-2">
          {highlight && <Sparkles size={14} className="text-blue-300" />}
          <strong className="text-sm text-white">
            {date} · {slot.startTime.slice(0, 5)}–{slot.endTime.slice(0, 5)}
          </strong>
          {slot.assistantName && <span className="text-xs text-slate-500">{slot.assistantName}</span>}
          <span className="ml-auto text-xs text-slate-500">{slot.registeredCount}/{slot.capacity}</span>
        </div>
        {slotTopics.length > 0 && <p className="mt-1 text-xs text-slate-400">{slotTopics.join(" · ")}</p>}
        {slot.note && <p className="mt-1 text-xs text-slate-500">{slot.note}</p>}
        <button
          type="button"
          onClick={() => toggle(slot)}
          disabled={busySlot === slot.id || full}
          className={`mt-2 w-full rounded-lg py-2 text-xs font-bold disabled:opacity-40 ${registered ? "border border-white/15 text-slate-300" : "bg-blue-600 text-white"}`}
        >
          {registered ? "Huỷ đăng ký" : full ? "Đã đủ số lượng" : viewer === "parent" ? "Đăng ký cho con" : "Đăng ký"}
        </button>
      </div>
    );
  }

  return (
    <section className="rounded-2xl border border-amber-400/25 bg-gradient-to-r from-amber-500/10 to-transparent p-5">
      <div className="flex items-center gap-2 text-amber-300">
        <BookOpenCheck size={18} />
        <h2 className="font-display font-bold text-white">Bù bài trước khi vào lớp chính thức</h2>
      </div>
      <p className="mt-1 text-sm text-amber-100/80">
        {who === "con" ? "Con" : "Em"} vào <strong className="text-white">{reg.courseName}</strong> sau khai giảng. Học bù theo thứ tự dưới đây:
        bài lớp vừa học trước để theo kịp ngay, rồi lùi dần về các bài trước.
      </p>

      <ol className="mt-3 space-y-1.5">
        {reg.catchup_done_topic_ids.map((id) => (
          <li key={`done-${id}`} className="flex items-center gap-2 text-sm text-emerald-300/80 line-through">
            <Check size={14} /> {topicName.get(id) ?? `Bài #${id}`}
          </li>
        ))}
        {ordered.map((id, i) => (
          <li key={id} className={`flex items-center gap-2 text-sm ${i === 0 ? "font-semibold text-white" : "text-slate-300"}`}>
            {i === 0 ? <ChevronRight size={14} className="text-amber-300" /> : <span className="w-3.5 text-center text-xs text-slate-500">{i + 1}</span>}
            {topicName.get(id) ?? `Bài #${id}`}
            {i === 0 && <span className="rounded-full bg-amber-500/20 px-2 py-0.5 text-[10px] font-bold text-amber-200">kế tiếp</span>}
          </li>
        ))}
      </ol>

      {classId === null ? (
        <p className="mt-4 text-sm text-slate-400">Giáo viên duyệt xong sẽ thấy lịch phụ đạo của khối ở đây.</p>
      ) : (
        <div className="mt-4">
          <p className="mb-2 text-xs font-bold uppercase tracking-wide text-slate-400">Ca phụ đạo của trợ giảng khối</p>
          {slots.length === 0 ? (
            <p className="text-sm text-slate-500">Trợ giảng chưa đăng ca nào trong tuần tới. Quay lại sau vài ngày.</p>
          ) : (
            <div className="space-y-2">
              {suggested.map((slot) => renderSlot(slot, slot.topicIds.includes(nextId ?? -1)))}
              {others.length > 0 && (
                <details>
                  <summary className="cursor-pointer text-xs text-slate-400">Ca khác trong tuần ({others.length}) — không đúng bài cần bù</summary>
                  <div className="mt-2 space-y-2">
                    {others.map((slot) => renderSlot(slot, false))}
                  </div>
                </details>
              )}
            </div>
          )}
        </div>
      )}
    </section>
  );
}
