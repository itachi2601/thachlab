"use client";

import { useCallback, useEffect, useState } from "react";
import type { SchoolClass } from "@/features/exams/types";
import { fetchClasses } from "@/services/classes";
import { getSupabase } from "@/services/supabase";
import { useToast } from "@/components/ui/Toast";

const inputCls =
  "rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-sm text-white placeholder:text-slate-500 focus:border-[#3B82F6] focus:outline-none";

function toSlug(name: string) {
  return name
    .toLowerCase()
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .replace(/đ/g, "d")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/(^-|-$)/g, "");
}

export default function ClassesAdmin() {
  const toast = useToast();
  const [classes, setClasses] = useState<SchoolClass[]>([]);
  const [name, setName] = useState("");
  const [color, setColor] = useState("#3B82F6");
  const [icon, setIcon] = useState("");

  const reload = useCallback(() => {
    fetchClasses(true).then(setClasses);
  }, []);
  useEffect(reload, [reload]);

  async function addClass(e: React.FormEvent) {
    e.preventDefault();
    const trimmed = name.trim();
    if (!trimmed) return;
    const { error } = await getSupabase().from("classes").insert({
      name: trimmed,
      slug: toSlug(trimmed),
      color,
      icon,
      sort_order: classes.length + 1,
    });
    if (error) {
      toast("error", error.message.includes("duplicate") ? "Lớp này đã tồn tại." : error.message);
      return;
    }
    toast("success", `Đã thêm lớp ${trimmed}`);
    setName("");
    setIcon("");
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
      <form
        onSubmit={addClass}
        className="flex flex-wrap items-center gap-3 rounded-2xl border border-white/10 bg-[#0B1020] p-5"
      >
        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Tên lớp, vd 10A3"
          className={`${inputCls} w-36`}
        />
        <input
          value={icon}
          onChange={(e) => setIcon(e.target.value)}
          placeholder="Icon 🎓"
          className={`${inputCls} w-24`}
        />
        <label className="flex items-center gap-2 text-sm text-slate-400">
          Màu
          <input
            type="color"
            value={color}
            onChange={(e) => setColor(e.target.value)}
            className="h-9 w-12 cursor-pointer rounded-lg border border-white/10 bg-transparent"
          />
        </label>
        <button
          type="submit"
          className="rounded-full bg-[#2563EB] px-5 py-2 text-sm font-semibold text-white hover:bg-[#1D4ED8]"
        >
          + Thêm lớp
        </button>
      </form>

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
