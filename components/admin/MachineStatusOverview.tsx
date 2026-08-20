"use client";

import { useCallback, useEffect, useState } from "react";
import { AlertOctagon, Check, RefreshCw, Wrench } from "lucide-react";
import { fetchAllMachines, groupMachinesByType, groupMachinesByWorkshop, MACHINE_TYPE_LABELS, type Machine } from "@/services/attendance-machine";

const WORKSHOP_LABELS: Record<string, string> = {
  "C1.2": "Phòng CNC C1.2",
  "C1.1": "Xưởng máy công cụ C1.1",
  "F1.2": "Xưởng máy vạn năng F1.2",
};

export default function MachineStatusOverview() {
  const [machines, setMachines] = useState<Machine[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const load = useCallback(() => {
    setLoading(true);
    fetchAllMachines()
      .then(setMachines)
      .catch((cause) => setError(cause instanceof Error ? cause.message : "Không tải được danh sách máy."))
      .finally(() => setLoading(false));
  }, []);
  useEffect(() => { load(); }, [load]);

  const workshops = groupMachinesByWorkshop(machines);
  const totalBroken = machines.filter((m) => m.status === "broken").length;

  return (
    <div className="space-y-5">
      <section className="rounded-3xl border border-white/10 bg-gradient-to-br from-[#172c46] to-[#071426] p-6">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <p className="text-xs font-bold uppercase tracking-[.16em] text-sky-300">Cơ khí chế tạo</p>
            <h2 className="mt-2 font-display text-2xl font-bold text-white">Tổng quan tình trạng máy</h2>
            <p className="mt-2 text-sm text-slate-400">
              {machines.length} thiết bị · {workshops.length} xưởng thực tập
              {totalBroken > 0 && <span className="ml-1 font-bold text-red-300">· {totalBroken} đang hỏng</span>}
            </p>
          </div>
          <button onClick={load} disabled={loading} className="inline-flex items-center gap-2 rounded-xl border border-white/10 px-4 py-2.5 text-sm font-bold text-slate-300 disabled:opacity-40">
            <RefreshCw size={16} className={loading ? "animate-spin" : ""} />Làm mới
          </button>
        </div>
        {error && <p className="mt-3 rounded-xl bg-red-500/10 p-3 text-sm text-red-200">{error}</p>}
      </section>

      {!loading && workshops.length === 0 && !error && (
        <p className="rounded-2xl border border-dashed border-white/10 p-8 text-center text-sm text-slate-500">Chưa có dữ liệu máy.</p>
      )}

      {workshops.map((ws) => <WorkshopSection key={ws.workshop} workshop={ws.workshop} machines={ws.machines} />)}
    </div>
  );
}

function WorkshopSection({ workshop, machines }: { workshop: string; machines: Machine[] }) {
  const broken = machines.filter((m) => m.status === "broken").length;
  const groups = groupMachinesByType(machines);
  return (
    <section className="rounded-2xl border border-white/10 bg-[#0B1020] p-5 sm:p-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <Wrench size={18} className="text-orange-300" />
          <h3 className="font-display text-xl font-bold text-white">{WORKSHOP_LABELS[workshop] ?? (workshop || "Chưa gán xưởng")}</h3>
        </div>
        <div className="flex items-center gap-2 text-xs font-bold">
          <span className="rounded-full border border-white/10 px-3 py-1 text-slate-300">{machines.length} máy</span>
          <span className={`rounded-full border px-3 py-1 ${broken > 0 ? "border-red-400/30 bg-red-500/10 text-red-200" : "border-emerald-400/20 bg-emerald-500/5 text-emerald-300"}`}>
            {broken > 0 ? `${broken} đang hỏng` : "Tất cả hoạt động tốt"}
          </span>
        </div>
      </div>
      <div className="mt-4 space-y-4">
        {groups.map((group) => (
          <div key={group.type}>
            <p className="text-xs font-bold uppercase tracking-wider text-slate-500">{MACHINE_TYPE_LABELS[group.type]} · {group.machines.length}</p>
            <div className="mt-2 grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
              {group.machines.map((m) => <MachineTile key={m.code} machine={m} />)}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

function MachineTile({ machine }: { machine: Machine }) {
  const broken = machine.status === "broken";
  return (
    <div className={`rounded-xl border p-3 ${broken ? "border-red-400/25 bg-red-500/5" : "border-white/10 bg-white/[.02]"}`}>
      <div className="flex items-center justify-between gap-2">
        <span className="truncate text-sm font-bold text-white" title={machine.label}>{machine.label}</span>
        <span className={`flex shrink-0 items-center gap-1 rounded-full px-2 py-0.5 text-[10px] font-bold ${broken ? "bg-red-500/15 text-red-300" : "bg-emerald-500/15 text-emerald-300"}`}>
          {broken ? <AlertOctagon size={10} /> : <Check size={10} />}{broken ? "NG" : "OK"}
        </span>
      </div>
      <p className="mt-1 font-mono text-[11px] text-slate-500">{machine.code}</p>
      {broken && machine.note && <p className="mt-1 text-[11px] text-red-200/80">{machine.note}</p>}
    </div>
  );
}
