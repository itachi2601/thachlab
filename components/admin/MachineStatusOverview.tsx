"use client";

import { useCallback, useEffect, useState } from "react";
import { AlertOctagon, Check, History, Loader2, Pencil, RefreshCw, Users, Wrench, X } from "lucide-react";
import { fetchAllMachines, groupMachinesByType, groupMachinesByWorkshop, MACHINE_TYPE_LABELS, type Machine, type MachineStatus } from "@/services/attendance-machine";
import { addMachineStatusLog, fetchMachineStatusLog, updateMachineStatusLog, type MachineStatusLogEntry } from "@/services/machine-status-log";
import { fetchEquipmentBreakdownReportsByMachine, fetchOpenEquipmentBreakdownReports, fetchAdminProfiles, createEquipmentBreakdownPhotoUrl, startEquipmentRepair, resolveEquipmentBreakdown, type EquipmentBreakdownReportWithCourse, type BreakdownStatus, type AdminProfile } from "@/services/equipment-breakdown";
import { fetchMachineUsageHistory, type MachineUsageRecord } from "@/services/course-attendance";
import { useAuth } from "@/components/auth/AuthProvider";

const WORKSHOP_LABELS: Record<string, string> = {
  "C1.2": "Phòng CNC C1.2",
  "C1.1": "Xưởng máy công cụ C1.1",
  "F1.2": "Xưởng máy vạn năng F1.2",
};

function shortLabel(label: string) {
  return label.split(" — Xưởng ")[0];
}
function fmtDateTime(iso: string) {
  return new Date(iso).toLocaleString("vi-VN", { day: "2-digit", month: "2-digit", year: "numeric", hour: "2-digit", minute: "2-digit" });
}
function fmtElapsed(iso: string) {
  const ms = Date.now() - new Date(iso).getTime();
  const hours = Math.floor(ms / 3_600_000);
  if (hours < 1) return "vừa xong";
  if (hours < 24) return `${hours} giờ`;
  return `${Math.floor(hours / 24)} ngày`;
}
function isStale(iso: string, hours: number) {
  return Date.now() - new Date(iso).getTime() > hours * 3_600_000;
}
const BREAKDOWN_STATUS_LABELS: Record<BreakdownStatus, string> = { open: "Chờ xử lý", in_progress: "Đang sửa", resolved: "Đã xong" };
const BREAKDOWN_STATUS_STYLES: Record<BreakdownStatus, string> = {
  open: "bg-red-500/15 text-red-300", in_progress: "bg-amber-500/15 text-amber-300", resolved: "bg-emerald-500/15 text-emerald-300",
};
function toDateTimeLocal(iso: string) {
  const d = new Date(iso);
  const pad = (n: number) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
}

export default function MachineStatusOverview() {
  const { profile } = useAuth();
  const [machines, setMachines] = useState<Machine[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selected, setSelected] = useState<Machine | null>(null);
  const [selectedTab, setSelectedTab] = useState<"status" | "breakdown" | "usage">("status");
  const [activeWorkshop, setActiveWorkshop] = useState<string | null>(null);
  const [openBreakdowns, setOpenBreakdowns] = useState<EquipmentBreakdownReportWithCourse[]>([]);
  const [openBreakdownsLoading, setOpenBreakdownsLoading] = useState(true);
  const [openBreakdownsError, setOpenBreakdownsError] = useState("");
  const [lecturers, setLecturers] = useState<AdminProfile[]>([]);
  useEffect(() => { void fetchAdminProfiles().then(setLecturers).catch(() => undefined); }, []);
  const load = useCallback(() => {
    setLoading(true);
    fetchAllMachines()
      .then(setMachines)
      .catch((cause) => setError(cause instanceof Error ? cause.message : "Không tải được danh sách máy."))
      .finally(() => setLoading(false));
    setOpenBreakdownsLoading(true);
    fetchOpenEquipmentBreakdownReports()
      .then(setOpenBreakdowns)
      .catch((cause) => setOpenBreakdownsError(cause instanceof Error ? cause.message : "Không tải được danh sách máy đang hư."))
      .finally(() => setOpenBreakdownsLoading(false));
  }, []);
  useEffect(() => { load(); }, [load]);
  useEffect(() => { if (!selected) return; setSelected((current) => machines.find((m) => m.code === current?.code) ?? null); }, [machines]); // eslint-disable-line react-hooks/exhaustive-deps

  function openMachine(machine: Machine, tab: "status" | "breakdown" | "usage" = "status") {
    setSelectedTab(tab);
    setSelected(machine);
  }

  const workshops = groupMachinesByWorkshop(machines);
  const totalBroken = machines.filter((m) => m.status === "broken").length;
  const currentWorkshop = workshops.find((ws) => ws.workshop === activeWorkshop) ?? workshops[0] ?? null;

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
              {" · "}Click vào 1 máy để xem/sửa lịch sử tình trạng.
            </p>
          </div>
          <button onClick={load} disabled={loading} className="inline-flex items-center gap-2 rounded-xl border border-white/10 px-4 py-2.5 text-sm font-bold text-slate-300 disabled:opacity-40">
            <RefreshCw size={16} className={loading ? "animate-spin" : ""} />Làm mới
          </button>
        </div>
        {error && <p className="mt-3 rounded-xl bg-red-500/10 p-3 text-sm text-red-200">{error}</p>}
      </section>

      <OpenBreakdownsBoard reports={openBreakdowns} loading={openBreakdownsLoading} error={openBreakdownsError} machines={machines} onOpenMachine={(code) => { const m = machines.find((item) => item.code === code); if (m) openMachine(m, "breakdown"); }} />

      {!loading && workshops.length === 0 && !error && (
        <p className="rounded-2xl border border-dashed border-white/10 p-8 text-center text-sm text-slate-500">Chưa có dữ liệu máy.</p>
      )}

      {workshops.length > 1 && (
        <div className="flex flex-wrap gap-2">
          {workshops.map((ws) => {
            const broken = ws.machines.filter((m) => m.status === "broken").length;
            const active = ws.workshop === currentWorkshop?.workshop;
            return (
              <button
                key={ws.workshop}
                type="button"
                onClick={() => setActiveWorkshop(ws.workshop)}
                className={`flex items-center gap-2 rounded-xl border px-4 py-2.5 text-sm font-bold transition-colors ${
                  active ? "border-cyan-400/40 bg-cyan-500/10 text-white" : "border-white/10 text-slate-400 hover:border-white/20 hover:text-slate-200"
                }`}
              >
                {WORKSHOP_LABELS[ws.workshop] ?? (ws.workshop || "Chưa gán xưởng")}
                <span className="rounded-full bg-white/10 px-2 py-0.5 text-[11px] font-bold text-slate-300">{ws.machines.length}</span>
                {broken > 0 && <span className="rounded-full bg-red-500/20 px-2 py-0.5 text-[11px] font-bold text-red-300">{broken}</span>}
              </button>
            );
          })}
        </div>
      )}

      {currentWorkshop && <WorkshopSection key={currentWorkshop.workshop} workshop={currentWorkshop.workshop} machines={currentWorkshop.machines} onSelect={(m) => openMachine(m)} />}

      {selected && <MachineDetailModal machine={selected} initialTab={selectedTab} onClose={() => setSelected(null)} onChanged={load} lecturers={lecturers} currentUserId={profile?.id ?? null} />}
    </div>
  );
}

function OpenBreakdownsBoard({ reports, loading, error, machines, onOpenMachine }: { reports: EquipmentBreakdownReportWithCourse[]; loading: boolean; error: string; machines: Machine[]; onOpenMachine: (machineCode: string) => void }) {
  if (loading) return <section className="flex items-center gap-2 rounded-2xl border border-white/10 bg-[#0B1020] p-5 text-sm text-slate-500"><Loader2 size={14} className="animate-spin" />Đang tải danh sách máy đang hư…</section>;
  if (error) return <p className="rounded-xl bg-red-500/10 p-3 text-sm text-red-200">{error}</p>;
  const openCount = reports.filter((r) => r.status === "open").length;
  const inProgressCount = reports.filter((r) => r.status === "in_progress").length;
  return (
    <section className={`rounded-2xl border p-5 sm:p-6 ${reports.length ? "border-red-400/20 bg-red-500/[.04]" : "border-emerald-400/15 bg-emerald-500/[.03]"}`}>
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <AlertOctagon size={18} className={reports.length ? "text-red-300" : "text-emerald-300"} />
          <h3 className="font-display text-lg font-bold text-white">Máy đang hư / chờ sửa</h3>
        </div>
        {reports.length > 0 && (
          <div className="flex gap-2 text-xs font-bold">
            <span className="rounded-full bg-red-500/15 px-3 py-1 text-red-300">{openCount} chờ xử lý</span>
            <span className="rounded-full bg-amber-500/15 px-3 py-1 text-amber-300">{inProgressCount} đang sửa</span>
          </div>
        )}
      </div>
      {reports.length === 0 ? (
        <p className="mt-3 flex items-center gap-2 text-sm text-emerald-300"><Check size={15} />Không có máy nào đang chờ xử lý — toàn bộ thiết bị đang hoạt động bình thường.</p>
      ) : (
        <div className="mt-4 overflow-x-auto">
          <table className="w-full min-w-[900px] text-left text-xs">
            <thead>
              <tr className="border-b border-white/10 text-[10px] uppercase text-slate-500">
                <th className="p-2">Máy / xưởng</th>
                <th className="p-2">Trạng thái</th>
                <th className="p-2">Hư đã</th>
                <th className="p-2">GV báo hỏng</th>
                <th className="p-2">GV phụ trách sửa</th>
                <th className="p-2">Mô tả</th>
                <th className="p-2">Khóa học</th>
                <th className="p-2" />
              </tr>
            </thead>
            <tbody>
              {reports.map((r) => {
                const m = machines.find((item) => item.code === r.machine_code);
                const longWait = r.status === "open" && isStale(r.broken_at, 72);
                return (
                  <tr key={r.id} className="border-b border-white/5">
                    <td className="p-2"><span className="font-mono text-cyan-300">{r.machine_code}</span> <span className="text-slate-500">{m ? `(${WORKSHOP_LABELS[m.workshop] ?? m.workshop})` : ""}</span></td>
                    <td className="p-2"><span className={`rounded-full px-2 py-0.5 font-bold ${BREAKDOWN_STATUS_STYLES[r.status]}`}>{BREAKDOWN_STATUS_LABELS[r.status]}</span></td>
                    <td className="p-2"><span className={longWait ? "font-bold text-red-300" : "text-slate-300"}>{fmtElapsed(r.broken_at)}</span></td>
                    <td className="p-2 text-slate-300">{r.profiles?.full_name ?? "—"}</td>
                    <td className="p-2 text-slate-300">{r.assigned_profile?.full_name ?? "—"}</td>
                    <td className="max-w-[220px] truncate p-2 text-slate-400" title={r.description}>{r.description || "—"}</td>
                    <td className="p-2 text-slate-500">{r.course_offerings ? `${r.course_offerings.name} · ${r.course_offerings.class_label}` : "—"}</td>
                    <td className="p-2"><button type="button" onClick={() => onOpenMachine(r.machine_code)} className="font-bold text-cyan-300 hover:text-cyan-200">Xem</button></td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}

function WorkshopSection({ workshop, machines, onSelect }: { workshop: string; machines: Machine[]; onSelect: (m: Machine) => void }) {
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
              {group.machines.map((m) => <MachineTile key={m.code} machine={m} onClick={() => onSelect(m)} />)}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

function MachineTile({ machine, onClick }: { machine: Machine; onClick: () => void }) {
  const broken = machine.status === "broken";
  return (
    <button type="button" onClick={onClick} className={`rounded-xl border p-3 text-left transition-colors hover:border-cyan-400/30 ${broken ? "border-red-400/25 bg-red-500/5" : "border-white/10 bg-white/[.02]"}`}>
      <div className="flex items-center justify-between gap-2">
        <span className="truncate text-sm font-bold text-white" title={shortLabel(machine.label)}>
          <span className="font-mono text-cyan-300">{machine.code}</span> <span className="font-normal text-slate-300">({shortLabel(machine.label)})</span>
        </span>
        <span className={`flex shrink-0 items-center gap-1 rounded-full px-2 py-0.5 text-[10px] font-bold ${broken ? "bg-red-500/15 text-red-300" : "bg-emerald-500/15 text-emerald-300"}`}>
          {broken ? <AlertOctagon size={10} /> : <Check size={10} />}{broken ? "NG" : "OK"}
        </span>
      </div>
      {broken && machine.note && <p className="mt-1 text-[11px] text-red-200/80">{machine.note}</p>}
    </button>
  );
}

function MachineDetailModal({ machine, initialTab = "status", onClose, onChanged, lecturers, currentUserId }: { machine: Machine; initialTab?: "status" | "breakdown" | "usage"; onClose: () => void; onChanged: () => void; lecturers: AdminProfile[]; currentUserId: string | null }) {
  const [tab, setTab] = useState<"status" | "breakdown" | "usage">(initialTab);
  const [log, setLog] = useState<MachineStatusLogEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [status, setStatus] = useState<MachineStatus>(machine.status);
  const [note, setNote] = useState(machine.note);
  const [saving, setSaving] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editStatus, setEditStatus] = useState<MachineStatus>("ok");
  const [editNote, setEditNote] = useState("");
  const [editDate, setEditDate] = useState("");
  const [editSaving, setEditSaving] = useState(false);

  const [breakdowns, setBreakdowns] = useState<EquipmentBreakdownReportWithCourse[]>([]);
  const [breakdownLoading, setBreakdownLoading] = useState(true);
  const [breakdownError, setBreakdownError] = useState("");
  const [usage, setUsage] = useState<MachineUsageRecord[]>([]);
  const [usageLoading, setUsageLoading] = useState(true);
  const [usageError, setUsageError] = useState("");

  const load = useCallback(() => {
    setLoading(true);
    fetchMachineStatusLog(machine.code).then(setLog).catch((cause) => setError(cause instanceof Error ? cause.message : "Không tải được lịch sử.")).finally(() => setLoading(false));
  }, [machine.code]);
  const [breakdownRefreshKey, setBreakdownRefreshKey] = useState(0);
  useEffect(() => { load(); }, [load]);
  useEffect(() => { setStatus(machine.status); setNote(machine.note); }, [machine.status, machine.note]);
  useEffect(() => {
    setBreakdownLoading(true);
    fetchEquipmentBreakdownReportsByMachine(machine.code).then(setBreakdowns)
      .catch((cause) => setBreakdownError(cause instanceof Error ? cause.message : "Không tải được lịch sử báo hỏng."))
      .finally(() => setBreakdownLoading(false));
    setUsageLoading(true);
    fetchMachineUsageHistory(machine.code).then(setUsage)
      .catch((cause) => setUsageError(cause instanceof Error ? cause.message : "Không tải được lịch sử sử dụng."))
      .finally(() => setUsageLoading(false));
  }, [machine.code, breakdownRefreshKey]);
  const handleBreakdownChanged = useCallback(() => { setBreakdownRefreshKey((k) => k + 1); onChanged(); }, [onChanged]);

  async function saveNew() {
    setSaving(true); setError("");
    try { await addMachineStatusLog(machine.code, status, note); await load(); onChanged(); }
    catch (cause) { setError(cause instanceof Error ? cause.message : "Không lưu được."); }
    finally { setSaving(false); }
  }
  function startEdit(entry: MachineStatusLogEntry) {
    setEditingId(entry.id); setEditStatus(entry.status); setEditNote(entry.note); setEditDate(toDateTimeLocal(entry.created_at));
  }
  async function saveEdit(id: number) {
    setEditSaving(true); setError("");
    try {
      const createdAt = editDate ? new Date(editDate).toISOString() : undefined;
      await updateMachineStatusLog(id, editStatus, editNote, createdAt);
      setEditingId(null); await load(); onChanged();
    }
    catch (cause) { setError(cause instanceof Error ? cause.message : "Không lưu được."); }
    finally { setEditSaving(false); }
  }

  return (
    <div className="fixed inset-0 z-50 grid place-items-center bg-black/60 p-4" onClick={onClose}>
      <div className="max-h-[85vh] w-full max-w-xl overflow-y-auto rounded-2xl border border-white/10 bg-[#0B1020] p-5" onClick={(e) => e.stopPropagation()}>
        <div className="flex items-start justify-between gap-3">
          <div>
            <p className="font-mono text-sm text-cyan-300">{machine.code}</p>
            <h3 className="font-display text-lg font-bold text-white">{shortLabel(machine.label)}</h3>
          </div>
          <button onClick={onClose} className="rounded-lg p-1.5 text-slate-400 hover:bg-white/5 hover:text-white"><X size={18} /></button>
        </div>

        <div className="mt-3 flex gap-1.5 border-b border-white/10 pb-3">
          {([
            { key: "status", label: "Tình trạng" },
            { key: "breakdown", label: `Báo hỏng${breakdowns.length ? ` (${breakdowns.length})` : ""}` },
            { key: "usage", label: "Sinh viên sử dụng" },
          ] as const).map((t) => (
            <button
              key={t.key}
              type="button"
              onClick={() => setTab(t.key)}
              className={`rounded-lg px-3 py-1.5 text-xs font-bold transition-colors ${tab === t.key ? "bg-cyan-500/15 text-cyan-200" : "text-slate-400 hover:text-slate-200"}`}
            >
              {t.label}
            </button>
          ))}
        </div>

        {tab === "status" && <>
        <div className="mt-4 rounded-xl border border-white/10 bg-white/[.02] p-3">
          <p className="text-xs font-bold uppercase tracking-wider text-slate-500">Cập nhật tình trạng</p>
          <div className="mt-2 flex gap-2">
            <button type="button" onClick={() => setStatus("ok")} className={`flex-1 rounded-lg border py-2 text-xs font-bold ${status === "ok" ? "border-emerald-400/40 bg-emerald-500/10 text-emerald-200" : "border-white/10 text-slate-400"}`}>Bình thường</button>
            <button type="button" onClick={() => setStatus("broken")} className={`flex-1 rounded-lg border py-2 text-xs font-bold ${status === "broken" ? "border-red-400/40 bg-red-500/10 text-red-200" : "border-white/10 text-slate-400"}`}>Đang hỏng</button>
          </div>
          <textarea value={note} onChange={(e) => setNote(e.target.value)} rows={2} placeholder="Ghi chú tình trạng…" className="mt-2 w-full resize-none rounded-lg border border-white/10 bg-[#080d1d] px-3 py-2 text-sm text-white placeholder:text-slate-600" />
          <button type="button" disabled={saving} onClick={saveNew} className="mt-2 rounded-lg bg-cyan-600 px-4 py-2 text-xs font-bold text-white disabled:opacity-40">
            {saving ? "Đang lưu…" : "Lưu, thêm vào lịch sử"}
          </button>
          {error && <p className="mt-2 text-xs text-red-300">{error}</p>}
        </div>

        <div className="mt-4">
          <p className="flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider text-slate-500"><History size={13} />Lịch sử tình trạng</p>
          {loading ? <p className="mt-2 flex items-center gap-2 text-sm text-slate-500"><Loader2 size={14} className="animate-spin" />Đang tải…</p>
          : log.length === 0 ? <p className="mt-2 text-sm text-slate-500">Chưa có lịch sử.</p>
          : <div className="mt-2 space-y-2">
              {log.map((entry) => (
                <div key={entry.id} className="rounded-lg border border-white/5 bg-black/15 p-2.5 text-xs">
                  {editingId === entry.id ? <>
                    <div className="flex gap-2">
                      <button type="button" onClick={() => setEditStatus("ok")} className={`flex-1 rounded-md border py-1.5 font-bold ${editStatus === "ok" ? "border-emerald-400/40 bg-emerald-500/10 text-emerald-200" : "border-white/10 text-slate-400"}`}>Bình thường</button>
                      <button type="button" onClick={() => setEditStatus("broken")} className={`flex-1 rounded-md border py-1.5 font-bold ${editStatus === "broken" ? "border-red-400/40 bg-red-500/10 text-red-200" : "border-white/10 text-slate-400"}`}>Đang hỏng</button>
                    </div>
                    <textarea value={editNote} onChange={(e) => setEditNote(e.target.value)} rows={2} className="mt-1.5 w-full resize-none rounded-md border border-white/10 bg-[#080d1d] px-2 py-1 text-white" />
                    <input type="datetime-local" value={editDate} onChange={(e) => setEditDate(e.target.value)} className="mt-1.5 w-full rounded-md border border-white/10 bg-[#080d1d] px-2 py-1 text-white [color-scheme:dark]" />
                    <div className="mt-1.5 flex gap-1.5">
                      <button type="button" disabled={editSaving} onClick={() => void saveEdit(entry.id)} className="rounded-md bg-cyan-600 px-2.5 py-1 font-bold text-white disabled:opacity-40">Lưu</button>
                      <button type="button" onClick={() => setEditingId(null)} className="rounded-md border border-white/10 px-2.5 py-1 font-bold text-slate-300">Hủy</button>
                    </div>
                  </> : <>
                    <div className="flex items-center justify-between gap-2">
                      <span className={`rounded-full px-2 py-0.5 font-bold ${entry.status === "broken" ? "bg-red-500/15 text-red-300" : "bg-emerald-500/15 text-emerald-300"}`}>{entry.status === "broken" ? "NG" : "OK"}</span>
                      <span className="text-slate-500">{fmtDateTime(entry.created_at)}</span>
                    </div>
                    {entry.note && <p className="mt-1 text-slate-300">{entry.note}</p>}
                    <div className="mt-1.5 flex items-center justify-between gap-2 text-[11px] text-slate-500">
                      <span>{entry.profiles?.full_name ?? "—"}</span>
                      <button type="button" onClick={() => startEdit(entry)} className="flex items-center gap-1 font-bold text-cyan-300 hover:text-cyan-200"><Pencil size={11} />Sửa</button>
                    </div>
                  </>}
                </div>
              ))}
            </div>}
        </div>
        </>}

        {tab === "breakdown" && <BreakdownSection reports={breakdowns} loading={breakdownLoading} error={breakdownError} lecturers={lecturers} currentUserId={currentUserId} onChanged={handleBreakdownChanged} />}
        {tab === "usage" && <UsageSection records={usage} loading={usageLoading} error={usageError} />}
      </div>
    </div>
  );
}

function BreakdownSection({ reports, loading, error, lecturers, currentUserId, onChanged }: { reports: EquipmentBreakdownReportWithCourse[]; loading: boolean; error: string; lecturers: AdminProfile[]; currentUserId: string | null; onChanged: () => void }) {
  if (loading) return <p className="mt-4 flex items-center gap-2 text-sm text-slate-500"><Loader2 size={14} className="animate-spin" />Đang tải…</p>;
  if (error) return <p className="mt-4 text-sm text-red-300">{error}</p>;
  if (reports.length === 0) return <p className="mt-4 text-sm text-slate-500">Máy này chưa từng được báo hỏng.</p>;
  const currentIssue = reports.find((r) => r.status === "open" || r.status === "in_progress");
  const history = reports.filter((r) => r.status === "resolved");
  return (
    <div className="mt-4 space-y-2.5">
      {currentIssue && <CurrentBreakdownActions report={currentIssue} lecturers={lecturers} currentUserId={currentUserId} onDone={onChanged} />}
      {history.map((r) => (
        <div key={r.id} className="rounded-lg border border-white/5 bg-black/15 p-2.5 text-xs">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <span className={`rounded-full px-2 py-0.5 font-bold ${BREAKDOWN_STATUS_STYLES[r.status]}`}>{BREAKDOWN_STATUS_LABELS[r.status]}</span>
            <span className="text-slate-500">{r.course_offerings ? `${r.course_offerings.name} · ${r.course_offerings.class_label}` : "—"}</span>
          </div>
          <p className="mt-1.5 text-slate-500">Hư lúc {fmtDateTime(r.broken_at)} · {r.profiles?.full_name ?? "—"} báo</p>
          {r.description && <p className="mt-1 text-slate-300">{r.description}</p>}
          <p className="mt-1 text-slate-500">GV sửa chữa: {r.assigned_profile?.full_name ?? "—"}</p>
          <div className="mt-1.5 flex flex-wrap gap-1.5">
            <BreakdownPhotoLink path={r.broken_photo_path} label="Ảnh lúc hỏng" />
            {r.resolved_photo_path && <BreakdownPhotoLink path={r.resolved_photo_path} label="Ảnh lúc khắc phục" />}
          </div>
          {r.status === "resolved" && (
            <p className="mt-1.5 text-emerald-200/90">
              Xong lúc {r.resolved_at ? fmtDateTime(r.resolved_at) : "—"}{r.resolved_note ? ` — ${r.resolved_note}` : ""}
            </p>
          )}
        </div>
      ))}
    </div>
  );
}

function LecturerSelect({ lecturers, value, onChange, placeholder }: { lecturers: AdminProfile[]; value: string; onChange: (id: string) => void; placeholder: string }) {
  return (
    <select value={value} onChange={(e) => onChange(e.target.value)} className="mt-1 w-full rounded-lg border border-white/10 bg-[#080d1d] px-3 py-2 text-xs text-white">
      <option value="" disabled>{placeholder}</option>
      {lecturers.map((l) => <option key={l.id} value={l.id}>{l.full_name}</option>)}
    </select>
  );
}

function CurrentBreakdownActions({ report, lecturers, currentUserId, onDone }: { report: EquipmentBreakdownReportWithCourse; lecturers: AdminProfile[]; currentUserId: string | null; onDone: () => void }) {
  const [assigning, setAssigning] = useState(false);
  const [assignedTo, setAssignedTo] = useState(currentUserId ?? "");
  const [resolving, setResolving] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  async function start() {
    if (!assignedTo) return;
    setBusy(true); setError("");
    try { await startEquipmentRepair(report.id, assignedTo); setAssigning(false); onDone(); }
    catch (cause) { setError(cause instanceof Error ? cause.message : "Không nhận sửa được."); }
    finally { setBusy(false); }
  }
  return (
    <div className="rounded-xl border border-red-400/20 bg-red-500/5 p-3 text-xs">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <span className={`rounded-full px-2 py-0.5 font-bold ${BREAKDOWN_STATUS_STYLES[report.status]}`}>{BREAKDOWN_STATUS_LABELS[report.status]}</span>
        <span className="text-slate-500">{report.course_offerings ? `${report.course_offerings.name} · ${report.course_offerings.class_label}` : "—"}</span>
      </div>
      <p className="mt-1.5 text-slate-500">Hư lúc {fmtDateTime(report.broken_at)} ({fmtElapsed(report.broken_at)} trước)</p>
      {report.description && <p className="mt-1 text-slate-300">{report.description}</p>}
      <p className="mt-1 text-slate-500">GV báo hỏng: {report.profiles?.full_name ?? "—"}{report.status === "in_progress" && <> · GV phụ trách sửa: {report.assigned_profile?.full_name ?? "—"}</>}</p>
      <div className="mt-2 flex flex-wrap items-center gap-2">
        <BreakdownPhotoLink path={report.broken_photo_path} label="Ảnh lúc hỏng" />
        {report.status === "open" && !assigning && <button type="button" onClick={() => setAssigning(true)} className="rounded-md border border-amber-400/30 bg-amber-500/10 px-3 py-1.5 font-bold text-amber-200">Nhận sửa</button>}
        {!resolving && <button type="button" onClick={() => setResolving(true)} className="rounded-md border border-emerald-400/30 bg-emerald-500/10 px-3 py-1.5 font-bold text-emerald-200">Đã sửa xong</button>}
      </div>
      {assigning && (
        <div className="mt-2 rounded-lg border border-amber-400/20 bg-amber-500/5 p-2.5">
          <label className="block text-slate-500">Giảng viên phụ trách sửa</label>
          <LecturerSelect lecturers={lecturers} value={assignedTo} onChange={setAssignedTo} placeholder="Chọn giảng viên…" />
          {error && <p className="mt-1.5 text-red-300">{error}</p>}
          <div className="mt-2 flex gap-2">
            <button type="button" disabled={busy || !assignedTo} onClick={() => void start()} className="rounded-md bg-amber-600 px-3 py-1.5 font-bold text-white disabled:opacity-40">Xác nhận</button>
            <button type="button" onClick={() => setAssigning(false)} className="rounded-md border border-white/10 px-3 py-1.5 font-bold text-slate-300">Hủy</button>
          </div>
        </div>
      )}
      {resolving && <ResolveBreakdownForm report={report} lecturers={lecturers} currentUserId={currentUserId} onDone={() => { setResolving(false); onDone(); }} />}
    </div>
  );
}

function ResolveBreakdownForm({ report, lecturers, currentUserId, onDone }: { report: EquipmentBreakdownReportWithCourse; lecturers: AdminProfile[]; currentUserId: string | null; onDone: () => void }) {
  const [file, setFile] = useState<File | null>(null);
  const [note, setNote] = useState("");
  const [resolvedBy, setResolvedBy] = useState(report.assigned_to ?? currentUserId ?? "");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const missing = [!file && "ảnh", !resolvedBy && "giảng viên sửa chữa"].filter((v): v is string => Boolean(v));
  async function submit() {
    if (missing.length) return;
    setBusy(true); setError("");
    try { await resolveEquipmentBreakdown({ id: report.id, courseId: report.course_id, machineCode: report.machine_code, note, file: file!, resolvedBy }); onDone(); }
    catch (cause) { setError(cause instanceof Error ? cause.message : "Không lưu được."); }
    finally { setBusy(false); }
  }
  return (
    <div className="mt-2 rounded-lg border border-emerald-400/20 bg-emerald-500/5 p-2.5">
      <label className="block text-slate-500">Ảnh sau khi khắc phục</label>
      <input type="file" accept="image/*" onChange={(e) => setFile(e.target.files?.[0] ?? null)} className="mt-0.5 block w-full text-slate-400" />
      <label className="mt-1.5 block text-slate-500">Giảng viên sửa chữa</label>
      <LecturerSelect lecturers={lecturers} value={resolvedBy} onChange={setResolvedBy} placeholder="Chọn giảng viên…" />
      <textarea value={note} onChange={(e) => setNote(e.target.value)} rows={2} placeholder="Tình trạng khắc phục…" className="mt-1.5 w-full resize-none rounded-lg border border-white/10 bg-[#080d1d] px-2 py-1.5 text-white placeholder:text-slate-600" />
      {error && <p className="mt-1 text-red-300">{error}</p>}
      <button type="button" disabled={busy || missing.length > 0} onClick={submit} className="mt-1.5 rounded-md bg-emerald-600 px-3 py-1.5 font-bold text-white disabled:opacity-40">Nộp ảnh, hoàn tất</button>
      {!busy && missing.length > 0 && <p className="mt-1 text-amber-300">Cần nhập: {missing.join(", ")}.</p>}
    </div>
  );
}

function BreakdownPhotoLink({ path, label }: { path: string; label: string }) {
  const [url, setUrl] = useState<string | null>(null);
  const [loadingUrl, setLoadingUrl] = useState(false);
  async function open() {
    if (url) { window.open(url, "_blank", "noopener,noreferrer"); return; }
    setLoadingUrl(true);
    try { const signed = await createEquipmentBreakdownPhotoUrl(path); setUrl(signed); window.open(signed, "_blank", "noopener,noreferrer"); }
    finally { setLoadingUrl(false); }
  }
  return (
    <button type="button" onClick={open} disabled={loadingUrl} className="rounded-md border border-white/10 px-2 py-1 font-bold text-cyan-300 hover:text-cyan-200 disabled:opacity-40">
      {loadingUrl ? "Đang mở…" : label}
    </button>
  );
}

function UsageSection({ records, loading, error }: { records: MachineUsageRecord[]; loading: boolean; error: string }) {
  if (loading) return <p className="mt-4 flex items-center gap-2 text-sm text-slate-500"><Loader2 size={14} className="animate-spin" />Đang tải…</p>;
  if (error) return <p className="mt-4 text-sm text-red-300">{error}</p>;
  if (records.length === 0) return <p className="mt-4 text-sm text-slate-500">Chưa có sinh viên nào dùng máy này.</p>;
  return (
    <div className="mt-4">
      <p className="flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider text-slate-500"><Users size={13} />Lượt sử dụng gần nhất</p>
      <div className="mt-2 space-y-1.5">
        {records.map((rec, i) => (
          <div key={`${rec.session_id}-${rec.student_id}-${i}`} className="flex items-center justify-between gap-2 rounded-lg border border-white/5 bg-black/15 px-2.5 py-2 text-xs">
            <span className="font-bold text-white">{rec.profiles?.full_name ?? "—"} <span className="font-normal text-slate-500">({rec.profiles?.class_name ?? "—"})</span></span>
            <span className="text-slate-500">
              {rec.attendance_sessions ? new Date(rec.attendance_sessions.session_date).toLocaleDateString("vi-VN") : "—"}
              {rec.attendance_sessions?.course_offerings ? ` · ${rec.attendance_sessions.course_offerings.name}` : ""}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
