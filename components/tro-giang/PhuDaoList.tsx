"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { Check, HandHeart, PenLine } from "lucide-react";
import { useAuth } from "@/components/auth/AuthProvider";
import { useToast } from "@/components/ui/Toast";
import { fetchClassStudents, type ClassStudent } from "@/services/classes";
import {
  ACTIVE_NEED_STATUSES,
  NEED_STATUS_LABEL,
  fetchCoverageForStudents,
  fetchNeedsForStudents,
  needLabel,
  updateNeed,
  type NeedStatus,
  type TutoringCoverage,
  type TutoringNeed,
} from "@/services/tutoring";
import { fetchMyAssistantClasses, type TaAssistant, type TaAssistantClass } from "@/lib/tro-giang/queries";
import { demoClasses, isDemoAssistant } from "@/lib/tro-giang/demo";

const TONE: Record<NeedStatus, string> = {
  open: "border-red-500/40 bg-red-500/10 text-red-200",
  assigned: "border-amber-500/40 bg-amber-500/10 text-amber-200",
  tutored: "border-blue-500/40 bg-blue-500/10 text-blue-200",
  cleared: "border-emerald-500/40 bg-emerald-500/10 text-emerald-200",
  dismissed: "border-white/15 bg-white/5 text-slate-400",
};

function shortDate(iso: string | null) {
  return iso ? new Date(iso).toLocaleDateString("vi-VN", { day: "2-digit", month: "2-digit" }) : "";
}

/**
 * Trang "Cần phụ đạo" của trợ giảng: mở ra là biết hôm nay nên kèm em nào, phần nào,
 * phần nào mình (hoặc bạn khác) đã dạy rồi. Nguồn: tutoring_needs, sinh tự động từ
 * kết quả từng câu của bài kiểm tra.
 */
export default function PhuDaoList({ assistant }: { assistant: TaAssistant }) {
  const demo = isDemoAssistant(assistant);
  const { profile } = useAuth();
  const toast = useToast();
  const [classes, setClasses] = useState<TaAssistantClass[]>(() => (demo ? demoClasses() : []));
  const [pickedClassId, setPickedClassId] = useState<number | null>(null);
  const [students, setStudents] = useState<ClassStudent[]>([]);
  const [needs, setNeeds] = useState<TutoringNeed[] | null>(null);
  const [coverage, setCoverage] = useState<TutoringCoverage[]>([]);
  const [showDone, setShowDone] = useState(false);

  useEffect(() => {
    if (demo) return;
    fetchMyAssistantClasses(assistant.id).then(setClasses).catch(() => setClasses([]));
  }, [assistant.id, demo]);

  // Chưa chọn thì mặc định lớp đầu tiên — tính ra chứ không setState trong effect.
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
  const nameById = useMemo(() => new Map(students.map((s) => [s.id, s.full_name])), [students]);

  const load = useCallback(() => {
    if (demo) return;
    fetchNeedsForStudents(studentIds, showDone ? [] : ACTIVE_NEED_STATUSES)
      .then(setNeeds)
      .catch(() => setNeeds([]));
    fetchCoverageForStudents(studentIds).then(setCoverage).catch(() => setCoverage([]));
  }, [studentIds, showDone, demo]);
  useEffect(load, [load]);

  const taughtByKey = useMemo(() => {
    const map = new Map<string, TutoringCoverage>();
    for (const item of coverage) {
      const key = `${item.studentId}|${item.topicId}`;
      if (!map.has(key)) map.set(key, item);
    }
    return map;
  }, [coverage]);

  const grouped = useMemo(() => {
    const map = new Map<string, TutoringNeed[]>();
    for (const need of needs ?? []) {
      const list = map.get(need.studentId) ?? [];
      list.push(need);
      map.set(need.studentId, list);
    }
    return [...map.entries()]
      .map(([id, list]) => ({ id, name: nameById.get(id) ?? "(không rõ)", list }))
      .sort((a, b) => {
        const open = (x: TutoringNeed[]) => x.filter((n) => n.status === "open").length;
        return open(b.list) - open(a.list) || a.name.localeCompare(b.name, "vi");
      });
  }, [needs, nameById]);

  async function claim(need: TutoringNeed) {
    if (!profile) return;
    try {
      await updateNeed(need.id, { status: "assigned", assignedTo: profile.id });
      load();
    } catch (e) {
      toast("error", e instanceof Error ? e.message : "Chưa nhận được mục này.");
    }
  }

  if (demo) {
    return (
      <p className="rounded-2xl border border-dashed border-white/10 p-6 text-center text-sm text-slate-400">
        Chế độ giả lập không đọc dữ liệu thật nên danh sách này để trống.
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

      <button
        type="button"
        onClick={() => setShowDone((v) => !v)}
        className="text-xs font-semibold text-slate-400 underline underline-offset-2"
      >
        {showDone ? "Chỉ xem phần còn phải làm" : "Xem cả phần đã xong"}
      </button>

      {classes.length === 0 ? (
        <p className="rounded-2xl border border-dashed border-white/10 p-6 text-center text-sm text-slate-400">
          Bạn chưa được gán lớp nào. Nhờ thầy gán lớp ở trang Nhân sự để thấy danh sách này.
        </p>
      ) : needs === null ? (
        <p className="text-sm text-slate-400">Đang tải…</p>
      ) : grouped.length === 0 ? (
        <p className="rounded-2xl border border-dashed border-white/10 p-6 text-center text-sm text-slate-500">
          Chưa em nào trong lớp bị đánh dấu cần phụ đạo.
        </p>
      ) : (
        <div className="space-y-3">
          {grouped.map((student) => (
            <article key={student.id} className="rounded-2xl border border-white/10 bg-[#0B1020] p-4">
              <h2 className="font-semibold text-white">{student.name}</h2>
              <div className="mt-2 space-y-2">
                {student.list.map((need) => {
                  const taught = taughtByKey.get(`${need.studentId}|${need.topicId}`);
                  return (
                    <div key={need.id} className="flex flex-wrap items-center gap-2">
                      <span className={`rounded-full border px-3 py-1 text-xs font-semibold ${TONE[need.status]}`}>
                        {needLabel(need)}
                      </span>
                      <span className="text-xs text-slate-500">
                        sai {need.wrong}/{need.total} · {NEED_STATUS_LABEL[need.status]}
                      </span>
                      {taught && (
                        <span className="inline-flex items-center gap-1 text-xs text-blue-300">
                          <Check size={12} />
                          {shortDate(taught.workDate ?? taught.createdAt)}
                          {taught.assistantName ? ` · ${taught.assistantName}` : ""}
                        </span>
                      )}
                      {need.status === "open" && (
                        <button
                          type="button"
                          onClick={() => claim(need)}
                          className="ml-auto inline-flex items-center gap-1 rounded-full border border-amber-400/40 px-2.5 py-1 text-xs font-semibold text-amber-200"
                        >
                          <HandHeart size={12} /> Tôi nhận
                        </button>
                      )}
                    </div>
                  );
                })}
              </div>
            </article>
          ))}
        </div>
      )}

      <Link
        href="/tro-giang/ghi"
        className="flex items-center justify-center gap-2 rounded-2xl bg-blue-600 py-3.5 text-sm font-bold text-white"
      >
        <PenLine size={16} /> Ghi buổi phụ đạo
      </Link>
    </div>
  );
}
