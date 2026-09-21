"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { Ban, Users } from "lucide-react";
import { useToast } from "@/components/ui/Toast";
import { fetchClassStudents, type ClassStudent } from "@/services/classes";
import {
  ACTIVE_NEED_STATUSES,
  cancelSlot,
  createSlot,
  fetchNeedsForStudents,
  fetchRegistrationsForSlots,
  fetchSlotsForAssistant,
  type SlotRegistration,
  type TutoringNeed,
  type TutoringSlot,
} from "@/services/tutoring";
import { fetchMyAssistantClasses, type TaAssistant, type TaAssistantClass } from "@/lib/tro-giang/queries";
import { demoClasses, isDemoAssistant } from "@/lib/tro-giang/demo";

function todayStr() {
  return new Date().toISOString().slice(0, 10);
}

function shortDate(date: string) {
  return new Date(`${date}T00:00:00`).toLocaleDateString("vi-VN", { weekday: "short", day: "2-digit", month: "2-digit" });
}

/**
 * "Lịch tuần" của trợ giảng: đăng trước một buổi phụ đạo sắp tới (ngày giờ, chủ đề
 * dự kiến, sức chứa) — học sinh của lớp thấy ở trang chủ và tự đăng ký. Khác với
 * "ghi buổi" ở /tro-giang/ghi (ghi LẠI sau khi đã dạy, dùng tính lương): đây chỉ là
 * lịch mời trước, không tự nối vào phiếu lương.
 */
export default function TutoringSlotsPlanner({ assistant }: { assistant: TaAssistant }) {
  const demo = isDemoAssistant(assistant);
  const toast = useToast();
  const [classes, setClasses] = useState<TaAssistantClass[]>(() => (demo ? demoClasses() : []));
  const [pickedClassId, setPickedClassId] = useState<number | null>(null);
  const [students, setStudents] = useState<ClassStudent[]>([]);
  const [needs, setNeeds] = useState<TutoringNeed[]>([]);
  const [slots, setSlots] = useState<TutoringSlot[] | null>(null);
  const [registrations, setRegistrations] = useState<SlotRegistration[]>([]);
  const [busy, setBusy] = useState(false);

  const [workDate, setWorkDate] = useState(todayStr());
  const [startTime, setStartTime] = useState("18:00");
  const [endTime, setEndTime] = useState("19:30");
  const [capacity, setCapacity] = useState(6);
  const [note, setNote] = useState("");
  const [pickedTopicIds, setPickedTopicIds] = useState<number[]>([]);

  useEffect(() => {
    if (demo) return;
    fetchMyAssistantClasses(assistant.id).then(setClasses).catch(() => setClasses([]));
  }, [assistant.id, demo]);

  const classId = pickedClassId ?? classes[0]?.class_id ?? null;

  useEffect(() => {
    if (demo || !classId) return;
    let alive = true;
    fetchClassStudents(classId)
      .then((list) => alive && setStudents(list))
      .catch(() => alive && setStudents([]));
    return () => {
      alive = false;
    };
  }, [classId, demo]);

  const studentIds = useMemo(() => students.map((s) => s.id), [students]);

  useEffect(() => {
    if (demo) return;
    fetchNeedsForStudents(studentIds, ACTIVE_NEED_STATUSES).then(setNeeds).catch(() => setNeeds([]));
  }, [studentIds, demo]);

  const topicOptions = useMemo(() => {
    const map = new Map<number, string>();
    for (const need of needs) map.set(need.topicId, need.topicName);
    return [...map.entries()]
      .map(([id, name]) => ({ id, name }))
      .sort((a, b) => a.name.localeCompare(b.name, "vi"));
  }, [needs]);

  const load = useCallback(() => {
    if (demo || !classId) return;
    fetchSlotsForAssistant(assistant.id, classId)
      .then((rows) => {
        setSlots(rows);
        return fetchRegistrationsForSlots(rows.map((r) => r.id));
      })
      .then(setRegistrations)
      .catch(() => {
        setSlots([]);
        setRegistrations([]);
      });
  }, [assistant.id, classId, demo]);
  useEffect(load, [load]);

  const registrationsBySlot = useMemo(() => {
    const map = new Map<number, SlotRegistration[]>();
    for (const reg of registrations) {
      const list = map.get(reg.slotId) ?? [];
      list.push(reg);
      map.set(reg.slotId, list);
    }
    return map;
  }, [registrations]);

  function toggleTopic(id: number) {
    setPickedTopicIds((current) => (current.includes(id) ? current.filter((x) => x !== id) : [...current, id]));
  }

  async function submit() {
    if (!classId) return;
    if (endTime <= startTime) {
      toast("error", "Giờ kết thúc phải sau giờ bắt đầu.");
      return;
    }
    setBusy(true);
    try {
      await createSlot({
        assistantId: assistant.id,
        classId,
        workDate,
        startTime,
        endTime,
        topicIds: pickedTopicIds,
        capacity,
        note,
      });
      toast("success", "Đã đăng lịch — học sinh trong lớp thấy ngay ở trang chủ.");
      setNote("");
      setPickedTopicIds([]);
      load();
    } catch (e) {
      toast("error", e instanceof Error ? e.message : "Chưa đăng được lịch.");
    } finally {
      setBusy(false);
    }
  }

  async function cancel(id: number) {
    try {
      await cancelSlot(id);
      toast("info", "Đã huỷ buổi này.");
      load();
    } catch (e) {
      toast("error", e instanceof Error ? e.message : "Chưa huỷ được.");
    }
  }

  if (demo) {
    return (
      <p className="rounded-2xl border border-dashed border-white/10 p-6 text-center text-sm text-slate-400">
        Chế độ giả lập không đọc/ghi dữ liệu thật nên trang này để trống.
      </p>
    );
  }

  if (classes.length === 0) {
    return (
      <p className="rounded-2xl border border-dashed border-white/10 p-6 text-center text-sm text-slate-400">
        Bạn chưa được gán lớp nào. Nhờ thầy gán lớp ở trang Nhân sự để đăng lịch.
      </p>
    );
  }

  return (
    <div className="space-y-4">
      {classes.length > 1 && (
        <div className="flex flex-wrap gap-2">
          {classes.map((item) => (
            <button
              key={item.class_id}
              type="button"
              onClick={() => setPickedClassId(item.class_id)}
              className={`rounded-full border px-4 py-2 text-sm font-semibold ${
                classId === item.class_id
                  ? "border-blue-400/50 bg-blue-500/15 text-blue-200"
                  : "border-white/10 text-slate-400"
              }`}
            >
              {item.name}
            </button>
          ))}
        </div>
      )}

      <section className="space-y-3 rounded-2xl border border-white/10 bg-[#0B1020] p-4">
        <h2 className="font-semibold text-white">Đăng buổi mới</h2>
        <div className="grid grid-cols-2 gap-2 sm:grid-cols-4">
          <label className="col-span-2 sm:col-span-1">
            <span className="mb-1 block text-xs text-slate-400">Ngày</span>
            <input
              type="date"
              value={workDate}
              min={todayStr()}
              onChange={(e) => setWorkDate(e.target.value)}
              className="w-full rounded-xl border border-white/10 bg-[#080d1d] px-3 py-2 text-sm text-white"
            />
          </label>
          <label>
            <span className="mb-1 block text-xs text-slate-400">Bắt đầu</span>
            <input
              type="time"
              value={startTime}
              onChange={(e) => setStartTime(e.target.value)}
              className="w-full rounded-xl border border-white/10 bg-[#080d1d] px-3 py-2 text-sm text-white"
            />
          </label>
          <label>
            <span className="mb-1 block text-xs text-slate-400">Kết thúc</span>
            <input
              type="time"
              value={endTime}
              onChange={(e) => setEndTime(e.target.value)}
              className="w-full rounded-xl border border-white/10 bg-[#080d1d] px-3 py-2 text-sm text-white"
            />
          </label>
          <label>
            <span className="mb-1 block text-xs text-slate-400">Sức chứa</span>
            <input
              type="number"
              min={1}
              value={capacity}
              onChange={(e) => setCapacity(Math.max(1, Number(e.target.value) || 1))}
              className="w-full rounded-xl border border-white/10 bg-[#080d1d] px-3 py-2 text-sm text-white"
            />
          </label>
        </div>

        {topicOptions.length > 0 && (
          <div>
            <span className="mb-1.5 block text-xs text-slate-400">Chủ đề dự kiến (tuỳ chọn)</span>
            <div className="flex flex-wrap gap-1.5">
              {topicOptions.map((topic) => (
                <button
                  key={topic.id}
                  type="button"
                  onClick={() => toggleTopic(topic.id)}
                  className={`rounded-full border px-3 py-1.5 text-xs font-semibold ${
                    pickedTopicIds.includes(topic.id)
                      ? "border-blue-400/50 bg-blue-500/15 text-blue-200"
                      : "border-white/10 text-slate-400"
                  }`}
                >
                  {topic.name}
                </button>
              ))}
            </div>
          </div>
        )}

        <label className="block">
          <span className="mb-1 block text-xs text-slate-400">Ghi chú (tuỳ chọn)</span>
          <input
            type="text"
            value={note}
            onChange={(e) => setNote(e.target.value)}
            placeholder="VD: Phòng B203"
            className="w-full rounded-xl border border-white/10 bg-[#080d1d] px-3 py-2 text-sm text-white placeholder:text-slate-600"
          />
        </label>

        <button
          type="button"
          onClick={submit}
          disabled={busy || !classId}
          className="w-full rounded-xl bg-blue-600 py-3 text-sm font-bold text-white disabled:opacity-40"
        >
          Đăng lịch
        </button>
      </section>

      <section className="space-y-3">
        <h2 className="font-semibold text-white">Buổi đã đăng</h2>
        {slots === null ? (
          <p className="text-sm text-slate-400">Đang tải…</p>
        ) : slots.length === 0 ? (
          <p className="rounded-2xl border border-dashed border-white/10 p-6 text-center text-sm text-slate-500">
            Chưa đăng buổi nào cho lớp này.
          </p>
        ) : (
          <div className="space-y-2">
            {slots.map((slot) => {
              const regs = registrationsBySlot.get(slot.id) ?? [];
              return (
                <article
                  key={slot.id}
                  className={`rounded-2xl border p-4 ${
                    slot.status === "cancelled" ? "border-white/5 bg-white/[.02] opacity-60" : "border-white/10 bg-[#0B1020]"
                  }`}
                >
                  <div className="flex flex-wrap items-center gap-2">
                    <strong className="text-sm text-white">
                      {shortDate(slot.workDate)} · {slot.startTime.slice(0, 5)}–{slot.endTime.slice(0, 5)}
                    </strong>
                    <span className="inline-flex items-center gap-1 text-xs text-slate-400">
                      <Users size={12} /> {slot.registeredCount}/{slot.capacity}
                    </span>
                    {slot.status === "cancelled" && (
                      <span className="rounded-full border border-white/15 px-2 py-0.5 text-[11px] font-semibold text-slate-400">
                        Đã huỷ
                      </span>
                    )}
                    {slot.status === "open" && (
                      <button
                        type="button"
                        onClick={() => cancel(slot.id)}
                        className="ml-auto inline-flex items-center gap-1 rounded-full border border-red-400/30 px-2.5 py-1 text-xs font-semibold text-red-300"
                      >
                        <Ban size={12} /> Huỷ buổi
                      </button>
                    )}
                  </div>
                  {slot.note && <p className="mt-1.5 text-xs text-slate-400">{slot.note}</p>}
                  <p className="mt-2 text-xs text-slate-500">
                    {regs.length === 0 ? "Chưa có em nào đăng ký." : regs.map((r) => r.studentName).join(", ")}
                  </p>
                </article>
              );
            })}
          </div>
        )}
      </section>
    </div>
  );
}
