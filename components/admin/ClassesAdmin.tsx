"use client";

import { useCallback, useEffect, useState } from "react";
import type { SchoolClass } from "@/features/exams/types";
import { fetchClasses, isManagedClass, MANAGED_CLASSES } from "@/services/classes";
import { getSupabase } from "@/services/supabase";
import { useToast } from "@/components/ui/Toast";

export default function ClassesAdmin() {
  const toast = useToast();
  const [classes, setClasses] = useState<SchoolClass[]>([]);
  const [busy, setBusy] = useState(false);

  const reload = useCallback(() => {
    fetchClasses(true).then(setClasses);
  }, []);
  useEffect(reload, [reload]);

  async function syncManagedClasses() {
    setBusy(true);
    const supabase = getSupabase();
    for (const schoolClass of MANAGED_CLASSES) {
      const existing = classes.find(
        (c) => c.slug === schoolClass.slug || c.name === schoolClass.name,
      );
      const payload = { ...schoolClass, active: true };
      const { error } = existing
        ? await supabase.from("classes").update(payload).eq("id", existing.id)
        : await supabase.from("classes").insert(payload);
      if (error) {
        setBusy(false);
        toast("error", error.message);
        return;
      }
    }
    setBusy(false);
    toast("success", "Đã chuẩn hóa 4 lớp khối: KHTN 9, 10, 11, 12.");
    reload();
  }

  async function update(id: number, patch: Partial<SchoolClass>) {
    const { error } = await getSupabase().from("classes").update(patch).eq("id", id);
    if (error) toast("error", error.message);
    reload();
  }

  async function move(idx: number, dir: -1 | 1) {
    const other = idx + dir;
    if (other < 0 || other >= classes.length) return;
    const a = classes[idx];
    const b = classes[other];
    await getSupabase().from("classes").update({ sort_order: b.sort_order }).eq("id", a.id);
    await getSupabase().from("classes").update({ sort_order: a.sort_order }).eq("id", b.id);
    reload();
  }

  return (
    <div className="space-y-6">
      <section className="rounded-2xl border border-white/10 bg-[#0B1020] p-5">
        <h2 className="font-display text-lg font-semibold text-white">
          Hệ lớp theo khối
        </h2>
        <p className="mt-2 text-sm text-slate-400">
          Website chỉ dùng 4 lớp khối: KHTN 9, 10, 11 và 12. Chương, bài học và
          đề kiểm tra gắn trực tiếp với khối nên không cần tạo A1/A2 mỗi năm.
        </p>
        <button
          type="button"
          onClick={syncManagedClasses}
          disabled={busy}
          className="mt-4 rounded-full bg-[#2563EB] px-5 py-2 text-sm font-semibold text-white hover:bg-primary-dark disabled:opacity-50"
        >
          {busy ? "Đang chuẩn hóa..." : "Tạo/cập nhật 4 lớp khối"}
        </button>
      </section>

      <div className="space-y-2">
        {classes.map((c, idx) => (
          <div
            key={c.id}
            className={`flex flex-wrap items-center gap-3 rounded-2xl border border-white/10 bg-[#0B1020] px-4 py-3 ${
              c.active ? "" : "opacity-50"
            }`}
          >
            <span
              className="h-3 w-3 rounded-full"
              style={{ backgroundColor: c.color }}
            />
            <span className="font-medium text-white">
              {c.icon && `${c.icon} `}
              {c.name}
            </span>
            <span className="text-xs text-slate-500">/{c.slug}</span>
            {!isManagedClass(c) && (
              <span className="rounded-full bg-amber-500/10 px-2 py-0.5 text-xs text-amber-200">
                Lớp cũ, nên ẩn sau khi chuyển dữ liệu
              </span>
            )}
            <span className="ml-auto flex items-center gap-1">
              <button
                onClick={() => move(idx, -1)}
                title="Lên"
                className="rounded-lg bg-white/5 px-2 py-1 text-xs text-slate-300 hover:bg-white/15"
              >
                ↑
              </button>
              <button
                onClick={() => move(idx, 1)}
                title="Xuống"
                className="rounded-lg bg-white/5 px-2 py-1 text-xs text-slate-300 hover:bg-white/15"
              >
                ↓
              </button>
              <button
                onClick={() => update(c.id, { active: !c.active })}
                className="rounded-full border border-white/15 px-3 py-1 text-xs text-slate-300 hover:border-white/30"
              >
                {c.active ? "Ẩn" : "Hiện"}
              </button>
              <button
                onClick={async () => {
                  if (!confirm(`Xóa lớp ${c.name}? Học sinh và đề đã gán sẽ bị gỡ khỏi lớp.`)) return;
                  await getSupabase().from("classes").delete().eq("id", c.id);
                  toast("success", `Đã xóa lớp ${c.name}`);
                  reload();
                }}
                className="rounded-full border border-red-500/30 px-3 py-1 text-xs text-red-300 hover:border-red-500/60"
              >
                Xóa
              </button>
            </span>
          </div>
        ))}
        {classes.length === 0 && (
          <p className="text-sm text-slate-400">Chưa có lớp nào.</p>
        )}
      </div>
    </div>
  );
}
