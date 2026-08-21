"use client";

import { useCallback, useEffect, useState } from "react";
import { AlertOctagon, Check, History, Loader2, Pencil, RefreshCw, Users, Wrench, X } from "lucide-react";
import { fetchAllMachines, groupMachinesByType, groupMachinesByWorkshop, MACHINE_TYPE_LABELS, type Machine, type MachineStatus } from "@/services/attendance-machine";
import { addMachineStatusLog, fetchMachineStatusLog, updateMachineStatusLog, type MachineStatusLogEntry } from "@/services/machine-status-log";
import { fetchEquipmentBreakdownReportsByMachine, createEquipmentBreakdownPhotoUrl, type EquipmentBreakdownReportWithCourse, type BreakdownStatus } from "@/services/equipment-breakdown";
import { fetchMachineUsageHistory, type MachineUsageRecord } from "@/services/course-attendance";

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
  const [machines, setMachines] = useState<Machine[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selected, setSelected] = useState<Machine | null>(null);
  const [activeWorkshop, setActiveWorkshop] = useState<string | null>(null);
  const load = useCallback(() => {
    setLoading(true);
    fetchAllMachines()
      .then(setMachines)
      .catch((cause) => setError(cause instanceof Error ? cause.message : "Không tải được danh sách máy."))
      .finally(() => setLoading(false));
  }, []);
  useEffect(() => { load(); }, [load]);
  useEffect(() => { if (!selected) return; setSelected((current) => machines.find((m) => m.code === current?.code) ?? null); }, [machines]); // eslint-disable-line react-hooks/exhaustive-deps

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

      {currentWorkshop && <WorkshopSection key={currentWorkshop.workshop} workshop={currentWorkshop.workshop} machines={currentWorkshop.machines} onSelect={setSelected} />}

      {selected && <MachineDetailModal machine={selected} onClose={() => setSelected(null)} onChanged={load} />}
    </div>
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

function MachineDetailModal({ machine, onClose, onChanged }: { machine: Machine; onClose: () => void; onChanged: () => void }) {
  const [tab, setTab] = useState<"status" | "breakdown" | "usage">("status");
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
  }, [machine.code]);

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

        {tab === "breakdown" && <BreakdownSection reports={breakdowns} loading={breakdownLoading} error={breakdownError} />}
        {tab === "usage" && <UsageSection records={usage} loading={usageLoading} error={usageError} />}
      </div>
    </div>
  );
}

function BreakdownSection({ reports, loading, error }: { reports: EquipmentBreakdownReportWithCourse[]; loading: boolean; error: string }) {
  if (loading) return <p className="mt-4 flex items-center gap-2 text-sm text-slate-500"><Loader2 size={14} className="animate-spin" />Đang tải…</p>;
  if (error) return <p className="mt-4 text-sm text-red-300">{error}</p>;
  if (reports.length === 0) return <p className="mt-4 text-sm text-slate-500">Máy này chưa từng được báo hỏng.</p>;
  return (
    <div className="mt-4 space-y-2.5">
      {reports.map((r) => (
        <div key={r.id} className="rounded-lg border border-white/5 bg-black/15 p-2.5 text-xs">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <span className={`rounded-full px-2 py-0.5 font-bold ${BREAKDOWN_STATUS_STYLES[r.status]}`}>{BREAKDOWN_STATUS_LABELS[r.status]}</span>
            <span className="text-slate-500">{r.course_offerings ? `${r.course_offerings.name} · ${r.course_offerings.class_label}` : "—"}</span>
          </div>
          <p className="mt-1.5 text-slate-500">Hư lúc {fmtDateTime(r.broken_at)} · {r.profiles?.full_name ?? "—"} báo</p>
          {r.description && <p className="mt-1 text-slate-300">{r.description}</p>}
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
