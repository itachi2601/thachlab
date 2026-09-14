"use client";

import { useCallback, useEffect, useState } from "react";
import { CalendarDays, ClipboardPaste, Loader2, Plus, Save, Trash2, Wand2 } from "lucide-react";
import {
  deleteWeeklySession,
  fetchDailyAttendance,
  fetchWeeklySessions,
  prefillHeadcount,
  upsertWeeklySession,
  vnToday,
  weekRange,
  type WeeklySession,
} from "@/services/homeroom-shcn";
import { parseTuanJson } from "@/lib/shcn/tuan-json";

const emptyForm = {
  weekNo: "",
  metOn: "",
  announcements: [""],
  notes: [""],
  ethicsTopic: "",
  ethicsTaught: "",
  headcount: "",
  presentCount: "",
};

type Form = typeof emptyForm;

function toForm(week: WeeklySession): Form {
  return {
    weekNo: String(week.week_no),
    metOn: week.met_on ?? "",
    announcements: week.announcements.length ? week.announcements.map((item) => item.tieu_de) : [""],
    notes: week.announcements.length ? week.announcements.map((item) => item.ghi_chu ?? "") : [""],
    ethicsTopic: week.ethics_topic,
    ethicsTaught: week.ethics_taught.join("; "),
    headcount: week.headcount === null ? "" : String(week.headcount),
    presentCount: week.present_count === null ? "" : String(week.present_count),
  };
}

/**
 * GVCN nhập nội dung sinh hoạt tuần để sinh viên xem lại. Nội dung giữ đúng bản đã lược của
 * biên bản tuần (tối đa 5 mục) — dán thẳng tuan-XX.json vào là điền sẵn cả form.
 */
export default function HomeroomWeeklyEditor({ courseId }: { courseId: number }) {
  const [weeks, setWeeks] = useState<WeeklySession[]>([]);
  const [form, setForm] = useState<Form>(emptyForm);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [pasting, setPasting] = useState(false);
  const [pasted, setPasted] = useState("");
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const load = useCallback(
    () =>
      fetchWeeklySessions(courseId)
        .then(setWeeks)
        .catch((cause) => setError(cause instanceof Error ? cause.message : "Không tải được danh sách tuần.")),
    [courseId],
  );
  useEffect(() => { void load(); }, [load]);

  function update(patch: Partial<Form>) {
    setForm((current) => ({ ...current, ...patch }));
  }

  function reset() {
    setForm(emptyForm);
    setEditingId(null);
    setMessage("");
    setError("");
  }

  function applyPastedJson() {
    setError("");
    try {
      const parsed = parseTuanJson(JSON.parse(pasted));
      setForm({
        weekNo: String(parsed.weekNo),
        metOn: parsed.metOn ?? "",
        announcements: parsed.announcements.length ? parsed.announcements.map((item) => item.tieu_de) : [""],
        notes: parsed.announcements.length ? parsed.announcements.map((item) => item.ghi_chu ?? "") : [""],
        ethicsTopic: parsed.ethicsTopic,
        ethicsTaught: parsed.ethicsTaught.join("; "),
        headcount: parsed.headcount === null ? "" : String(parsed.headcount),
        presentCount: parsed.presentCount === null ? "" : String(parsed.presentCount),
      });
      setEditingId(weeks.find((week) => week.week_no === parsed.weekNo)?.id ?? null);
      setPasting(false);
      setPasted("");
      setMessage(`Đã đọc tuần ${parsed.weekNo} từ JSON — kiểm tra lại rồi bấm lưu.`);
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Không đọc được JSON.");
    }
  }

  /** Lấy sĩ số/có mặt từ điểm danh hàng ngày của lớp trưởng, khỏi nhập tay. */
  async function prefillFromDaily() {
    setError("");
    const anchor = form.metOn || vnToday();
    const range = weekRange(anchor);
    try {
      const rows = await fetchDailyAttendance(courseId, range.from, range.to);
      const prefill = prefillHeadcount(rows, form.metOn || null);
      if (!prefill) { setError("Tuần này lớp trưởng chưa nộp điểm danh ngày nào."); return; }
      update({ headcount: String(prefill.headcount), presentCount: String(prefill.presentCount) });
      setMessage(prefill.source === "day" ? "Đã lấy số liệu đúng ngày sinh hoạt." : "Đã lấy trung bình các ngày điểm danh trong tuần.");
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Không lấy được số liệu điểm danh.");
    }
  }

  async function save() {
    const weekNo = Number(form.weekNo);
    if (!weekNo) { setError("Nhập số tuần trước khi lưu."); return; }
    setBusy(true);
    setMessage("");
    setError("");
    try {
      await upsertWeeklySession({
        courseId,
        weekNo,
        metOn: form.metOn || null,
        announcements: form.announcements.map((title, index) => ({ tieu_de: title, ghi_chu: form.notes[index] ?? "" })),
        ethicsTopic: form.ethicsTopic,
        ethicsTaught: form.ethicsTaught.split(";").map((item) => item.trim()).filter(Boolean),
        headcount: form.headcount === "" ? null : Number(form.headcount),
        presentCount: form.presentCount === "" ? null : Number(form.presentCount),
      });
      await load();
      reset();
      setMessage(`Đã lưu nội dung sinh hoạt tuần ${weekNo}.`);
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Không lưu được nội dung tuần.");
    } finally {
      setBusy(false);
    }
  }

  async function remove(week: WeeklySession) {
    if (!window.confirm(`Xóa nội dung sinh hoạt tuần ${week.week_no}? Sinh viên sẽ không xem lại được nữa.`)) return;
    try {
      await deleteWeeklySession(week.id);
      if (editingId === week.id) reset();
      await load();
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Không xóa được tuần.");
    }
  }

  return (
    <div className="space-y-5">
      <section className="rounded-2xl border border-white/10 bg-[#0B1020] p-5">
        <div className="flex flex-wrap items-start justify-between gap-3">
          <div>
            <p className="text-xs font-bold uppercase tracking-[.16em] text-violet-300">Sinh hoạt chủ nhiệm</p>
            <h3 className="mt-1 font-display text-xl font-bold text-white">{editingId ? "Sửa nội dung tuần" : "Thêm nội dung tuần"}</h3>
            <p className="mt-1 text-sm text-slate-500">Chép lại bản đã lược của biên bản tuần (tối đa 5 mục) để sinh viên xem lại — không thay cho biên bản nộp portal.</p>
          </div>
          <button onClick={() => setPasting((value) => !value)} className="inline-flex items-center gap-2 rounded-xl border border-white/10 px-4 py-2 text-sm font-bold text-slate-300 hover:bg-white/5">
            <ClipboardPaste size={16} />Dán tuan-XX.json
          </button>
        </div>

        {pasting && (
          <div className="mt-4 rounded-2xl border border-violet-400/20 bg-violet-500/5 p-4">
            <textarea
              value={pasted}
              onChange={(event) => setPasted(event.target.value)}
              rows={6}
              placeholder='{"tuan_so": 3, "ngay_sinh_hoat": "2026-09-10", "noi_dung_pho_bien": [...]}'
              className="w-full rounded-xl border border-white/10 bg-[#080d1d] px-3 py-2 font-mono text-xs text-white placeholder:text-slate-600"
            />
            <button disabled={!pasted.trim()} onClick={applyPastedJson} className="mt-2 rounded-xl bg-violet-600 px-4 py-2 text-sm font-bold text-white disabled:opacity-40">Điền vào form</button>
          </div>
        )}

        {error && <p className="mt-3 rounded-xl bg-red-500/10 p-3 text-sm text-red-200">{error}</p>}
        {message && <p className="mt-3 rounded-xl bg-emerald-500/10 p-3 text-sm text-emerald-200">{message}</p>}

        <div className="mt-4 grid gap-3 sm:grid-cols-2">
          <label className="block">
            <span className="mb-1.5 block text-xs font-bold uppercase tracking-wide text-slate-400">Tuần số</span>
            <input type="number" min={1} max={53} value={form.weekNo} onChange={(event) => update({ weekNo: event.target.value })} className="w-full rounded-xl border border-white/10 bg-[#080d1d] px-4 py-2.5 text-sm text-white" />
          </label>
          <label className="block">
            <span className="mb-1.5 block text-xs font-bold uppercase tracking-wide text-slate-400">Ngày sinh hoạt</span>
            <input type="date" value={form.metOn} onChange={(event) => update({ metOn: event.target.value })} className="w-full rounded-xl border border-white/10 bg-[#080d1d] px-4 py-2.5 text-sm text-white" />
          </label>
        </div>

        <div className="mt-4">
          <span className="text-xs font-bold uppercase tracking-wide text-slate-400">Nội dung phổ biến (tối đa 5 mục)</span>
          <div className="mt-2 space-y-2">
            {form.announcements.map((title, index) => (
              <div key={index} className="grid gap-2 sm:grid-cols-[1fr_1fr_auto]">
                <input
                  value={title}
                  onChange={(event) => update({ announcements: form.announcements.map((item, i) => (i === index ? event.target.value : item)) })}
                  placeholder={`Mục ${index + 1}`}
                  className="rounded-xl border border-white/10 bg-[#080d1d] px-3 py-2 text-sm text-white placeholder:text-slate-600"
                />
                <input
                  value={form.notes[index] ?? ""}
                  onChange={(event) => update({ notes: form.announcements.map((_, i) => (i === index ? event.target.value : form.notes[i] ?? "")) })}
                  placeholder="Ghi chú (không bắt buộc)"
                  className="rounded-xl border border-white/10 bg-[#080d1d] px-3 py-2 text-sm text-white placeholder:text-slate-600"
                />
                <button
                  type="button"
                  aria-label={`Xóa mục ${index + 1}`}
                  onClick={() => update({ announcements: form.announcements.filter((_, i) => i !== index), notes: form.notes.filter((_, i) => i !== index) })}
                  className="rounded-xl border border-white/10 px-3 text-slate-400 hover:border-red-400/40 hover:text-red-300"
                >
                  <Trash2 size={15} />
                </button>
              </div>
            ))}
          </div>
          {form.announcements.length < 5 && (
            <button type="button" onClick={() => update({ announcements: [...form.announcements, ""], notes: [...form.notes, ""] })} className="mt-2 inline-flex items-center gap-1.5 text-xs font-bold text-blue-300">
              <Plus size={14} />Thêm mục
            </button>
          )}
        </div>

        <div className="mt-4 grid gap-3 sm:grid-cols-2">
          <label className="block">
            <span className="mb-1.5 block text-xs font-bold uppercase tracking-wide text-slate-400">Chủ đề GDĐĐ &amp; PTNN</span>
            <input value={form.ethicsTopic} onChange={(event) => update({ ethicsTopic: event.target.value })} placeholder="Chủ đề 2: Kỹ năng sống" className="w-full rounded-xl border border-white/10 bg-[#080d1d] px-4 py-2.5 text-sm text-white placeholder:text-slate-600" />
          </label>
          <label className="block">
            <span className="mb-1.5 block text-xs font-bold uppercase tracking-wide text-slate-400">Trọng tâm đã dạy (cách nhau dấu ;)</span>
            <input value={form.ethicsTaught} onChange={(event) => update({ ethicsTaught: event.target.value })} placeholder="An toàn giao thông; Số điện thoại khẩn cấp" className="w-full rounded-xl border border-white/10 bg-[#080d1d] px-4 py-2.5 text-sm text-white placeholder:text-slate-600" />
          </label>
        </div>

        <div className="mt-4 flex flex-wrap items-end gap-3">
          <label className="block">
            <span className="mb-1.5 block text-xs font-bold uppercase tracking-wide text-slate-400">Sĩ số</span>
            <input type="number" min={0} value={form.headcount} onChange={(event) => update({ headcount: event.target.value })} className="w-24 rounded-xl border border-white/10 bg-[#080d1d] px-3 py-2.5 text-sm text-white" />
          </label>
          <label className="block">
            <span className="mb-1.5 block text-xs font-bold uppercase tracking-wide text-slate-400">Có mặt</span>
            <input type="number" min={0} value={form.presentCount} onChange={(event) => update({ presentCount: event.target.value })} className="w-24 rounded-xl border border-white/10 bg-[#080d1d] px-3 py-2.5 text-sm text-white" />
          </label>
          <button type="button" onClick={() => void prefillFromDaily()} className="inline-flex items-center gap-2 rounded-xl border border-cyan-400/30 bg-cyan-500/10 px-4 py-2.5 text-sm font-bold text-cyan-200">
            <Wand2 size={15} />Điền sẵn từ điểm danh ngày
          </button>
        </div>

        <div className="mt-5 flex flex-wrap gap-2">
          <button disabled={busy} onClick={() => void save()} className="inline-flex items-center gap-2 rounded-xl bg-blue-600 px-5 py-2.5 text-sm font-bold text-white disabled:opacity-40">
            {busy ? <Loader2 size={16} className="animate-spin" /> : <Save size={16} />}{editingId ? "Lưu thay đổi" : "Lưu tuần này"}
          </button>
          {editingId && <button onClick={reset} className="rounded-xl border border-white/10 px-5 py-2.5 text-sm font-bold text-slate-300">Hủy sửa</button>}
        </div>
      </section>

      <section className="rounded-2xl border border-white/10 bg-[#0B1020] p-5">
        <div className="flex items-center gap-2"><CalendarDays size={18} className="text-blue-300" /><h3 className="font-display text-lg font-bold text-white">Các tuần đã đăng ({weeks.length})</h3></div>
        <div className="mt-3 space-y-2">
          {weeks.map((week) => (
            <div key={week.id} className="flex flex-wrap items-center justify-between gap-3 rounded-xl border border-white/5 bg-black/15 p-3">
              <div className="min-w-0">
                <strong className="text-sm text-white">Tuần {week.week_no}</strong>
                {week.met_on && <small className="ml-2 text-slate-500">{new Date(`${week.met_on}T00:00:00`).toLocaleDateString("vi-VN")}</small>}
                <p className="truncate text-xs text-slate-500">
                  {week.announcements.length} mục phổ biến{week.ethics_topic && ` · ${week.ethics_topic}`}
                  {week.headcount !== null && ` · ${week.present_count ?? "—"}/${week.headcount}`}
                </p>
              </div>
              <div className="flex shrink-0 gap-2">
                <button onClick={() => { setForm(toForm(week)); setEditingId(week.id); setMessage(""); setError(""); }} className="rounded-lg border border-white/10 px-3 py-1.5 text-xs font-bold text-slate-300 hover:bg-white/5">Sửa</button>
                <button onClick={() => void remove(week)} className="rounded-lg border border-red-400/25 px-3 py-1.5 text-xs font-bold text-red-300 hover:bg-red-500/10">Xóa</button>
              </div>
            </div>
          ))}
          {!weeks.length && <p className="rounded-xl border border-dashed border-white/10 p-6 text-center text-sm text-slate-500">Chưa có tuần nào.</p>}
        </div>
      </section>
    </div>
  );
}
