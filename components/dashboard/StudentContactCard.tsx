"use client";

import { useEffect, useState } from "react";
import { Copy, MessageCircle, Pencil, Phone } from "lucide-react";
import { useToast } from "@/components/ui/Toast";
import { fetchStudentAccount, saveStudentBirth, saveStudentPhones, type StudentAccountInfo } from "@/services/student-account";

const digits = (v: string | null | undefined) => (v ?? "").replace(/\D/g, "");
/** "2009-08-15" (hoặc chuỗi bắt đầu bằng ngày ISO) → "2009-08-15" cho ô date; khác → "". */
const isoDay = (v: string | null | undefined) => (/^\d{4}-\d{2}-\d{2}/.test(v ?? "") ? (v as string).slice(0, 10) : "");
const vnDay = (iso: string) => (iso ? `${iso.slice(8, 10)}/${iso.slice(5, 7)}/${iso.slice(0, 4)}` : "");

/**
 * Thẻ "Liên lạc gia đình": SĐT em + SĐT phụ huynh, sửa tại chỗ (thầy và trợ giảng phụ trách).
 * Là nơi DUY NHẤT hiện hai số này trong hồ sơ — thẻ tài khoản không lặp lại.
 * Ngày sinh (15/10/2026) sửa cùng chỗ: phụ huynh tự nối con cần đủ tên + ngày sinh + SĐT phụ huynh.
 */
export default function StudentContactCard({ studentId }: { studentId: string }) {
  const toast = useToast();
  const [info, setInfo] = useState<StudentAccountInfo | null | undefined>(undefined);
  const [error, setError] = useState("");
  const [editing, setEditing] = useState(false);
  const [phone, setPhone] = useState("");
  const [parentPhone, setParentPhone] = useState("");
  const [birth, setBirth] = useState("");
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    let cancelled = false;
    fetchStudentAccount(studentId)
      .then((row) => {
        if (cancelled) return;
        setInfo(row);
        setPhone(row?.phone ?? "");
        setParentPhone(row?.parent_phone ?? "");
        setBirth(isoDay(row?.birth_date));
      })
      .catch((e) => { if (!cancelled) { setError(e instanceof Error ? e.message : "Lỗi."); setInfo(null); } });
    return () => { cancelled = true; };
  }, [studentId]);

  async function save() {
    setBusy(true);
    try {
      await saveStudentPhones(studentId, phone, parentPhone);
      if (birth !== isoDay(info?.birth_date)) await saveStudentBirth(studentId, birth);
      setInfo((cur) =>
        cur ? { ...cur, phone: digits(phone) || null, parent_phone: digits(parentPhone) || null, birth_date: birth || null } : cur,
      );
      setEditing(false);
      toast("success", "Đã lưu.");
    } catch (e) {
      toast("error", e instanceof Error ? e.message : "Chưa lưu được.");
    } finally {
      setBusy(false);
    }
  }

  async function copy(text: string) {
    try { await navigator.clipboard.writeText(text); toast("success", "Đã chép."); }
    catch { toast("error", "Trình duyệt không cho chép tự động — bôi đen rồi chép tay nhé."); }
  }

  const row = (label: string, value: string | null, zalo: boolean) => (
    <div className="min-w-0 text-sm">
      <dt className="text-xs font-bold uppercase tracking-wide text-slate-500">{label}</dt>
      <dd className="mt-1 flex flex-wrap items-center gap-2 text-white">
        {value ? (
          <>
            <span className="font-mono">{value}</span>
            <a href={`tel:${digits(value)}`} aria-label={`Gọi ${label}`} className="inline-flex h-9 w-9 items-center justify-center rounded-lg border border-white/10 text-slate-300 hover:bg-white/10"><Phone size={15} /></a>
            {zalo && <a href={`https://zalo.me/${digits(value)}`} target="_blank" rel="noreferrer" aria-label={`Mở Zalo ${label}`} className="inline-flex h-9 w-9 items-center justify-center rounded-lg border border-white/10 text-slate-300 hover:bg-white/10"><MessageCircle size={15} /></a>}
            <button type="button" aria-label={`Chép ${label}`} onClick={() => copy(value)} className="inline-flex h-9 w-9 items-center justify-center rounded-lg border border-white/10 text-slate-300 hover:bg-white/10"><Copy size={14} /></button>
          </>
        ) : <span className="text-amber-300">Chưa có — bấm Sửa để bổ sung</span>}
      </dd>
    </div>
  );

  const field = (label: string, value: string, set: (v: string) => void) => (
    <label className="block text-sm">
      <span className="text-xs font-bold uppercase tracking-wide text-slate-500">{label}</span>
      <input
        value={value}
        onChange={(e) => set(e.target.value)}
        inputMode="tel"
        placeholder="VD: 0912345678"
        className="mt-1 w-full rounded-xl border border-white/10 bg-panel-deep px-3 py-2.5 text-base text-white"
      />
    </label>
  );

  return (
    <section className="rounded-2xl border border-white/10 bg-panel p-5">
      <div className="flex items-center gap-3">
        <h4 className="min-w-0 flex-1 font-display text-lg font-bold text-white">Liên lạc gia đình</h4>
        {info && !editing && (
          <button type="button" onClick={() => setEditing(true)} className="inline-flex items-center gap-1.5 rounded-xl border border-white/15 px-3 py-2 text-xs font-bold text-slate-200 hover:bg-white/10">
            <Pencil size={14} /> Sửa
          </button>
        )}
      </div>
      {info === undefined && <p className="mt-3 text-sm text-slate-500">Đang tải…</p>}
      {info === null && <p className="mt-3 text-sm text-red-300">{error || "Không có dữ liệu."}</p>}
      {info && !editing && (
        <dl className="mt-3 grid gap-4 sm:grid-cols-2">
          {row("SĐT phụ huynh", info.parent_phone, true)}
          {row("SĐT học sinh", info.phone, true)}
          <div className="min-w-0 text-sm">
            <dt className="text-xs font-bold uppercase tracking-wide text-slate-500">Ngày sinh</dt>
            <dd className="mt-1 text-white">
              {isoDay(info.birth_date) ? (
                vnDay(isoDay(info.birth_date))
              ) : (
                <span className="text-amber-300">Chưa có — phụ huynh chưa tự nối được, bấm Sửa để bổ sung</span>
              )}
            </dd>
          </div>
          {info.contact_email && (
            <div className="min-w-0 text-sm sm:col-span-2">
              <dt className="text-xs font-bold uppercase tracking-wide text-slate-500">Email liên hệ</dt>
              <dd className="mt-1 break-all text-white">{info.contact_email}</dd>
            </div>
          )}
        </dl>
      )}
      {info && editing && (
        <div className="mt-3 space-y-3">
          <div className="grid gap-3 sm:grid-cols-2">
            {field("SĐT phụ huynh", parentPhone, setParentPhone)}
            {field("SĐT học sinh", phone, setPhone)}
            <label className="block text-sm">
              <span className="text-xs font-bold uppercase tracking-wide text-slate-500">Ngày sinh</span>
              <input
                type="date"
                value={birth}
                min="1990-01-01"
                max="2015-12-31"
                onChange={(e) => setBirth(e.target.value)}
                className="mt-1 w-full rounded-xl border border-white/10 bg-panel-deep px-3 py-2.5 text-base text-white"
              />
            </label>
          </div>
          <p className="text-xs text-slate-500">Chỉ cần chữ số (9–11 số). Để trống là xoá số.</p>
          <div className="flex gap-2">
            <button type="button" disabled={busy} onClick={() => void save()} className="rounded-xl bg-blue-600 px-4 py-2.5 text-sm font-bold text-white disabled:opacity-50">{busy ? "Đang lưu…" : "Lưu"}</button>
            <button type="button" disabled={busy} onClick={() => { setEditing(false); setPhone(info.phone ?? ""); setParentPhone(info.parent_phone ?? ""); setBirth(isoDay(info.birth_date)); }} className="rounded-xl border border-white/15 px-4 py-2.5 text-sm font-bold text-slate-200">Huỷ</button>
          </div>
        </div>
      )}
    </section>
  );
}
