"use client";

import { useEffect, useState } from "react";
import ClassAnnouncementsPanel from "@/components/dashboard/ClassAnnouncementsPanel";
import { fetchMyAssistantClasses, type TaAssistant, type TaAssistantClass } from "@/lib/tro-giang/queries";
import { demoClasses, isDemoAssistant } from "@/lib/tro-giang/demo";

/** Trang "Thông báo lớp" của trợ giảng: chọn lớp mình phụ trách rồi đăng thông báo. */
export default function TaClassAnnouncements({ assistant }: { assistant: TaAssistant }) {
  const demo = isDemoAssistant(assistant);
  const [classes, setClasses] = useState<TaAssistantClass[]>(() => (demo ? demoClasses() : []));
  const [pickedClassId, setPickedClassId] = useState<number | null>(null);

  useEffect(() => {
    if (demo) return;
    fetchMyAssistantClasses(assistant.id).then(setClasses).catch(() => setClasses([]));
  }, [assistant.id, demo]);

  const classId = pickedClassId ?? classes[0]?.class_id ?? null;

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
        Bạn chưa được gán lớp nào. Nhờ thầy gán lớp ở trang Nhân sự để đăng thông báo.
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
      {classId && <ClassAnnouncementsPanel classId={classId} />}
    </div>
  );
}
