"use client";

import { useState } from "react";
import { AlertCircle, FileSpreadsheet, Upload, UserCheck2, UserPlus2 } from "lucide-react";
import { useToast } from "@/components/ui/Toast";
import { parseRosterFile, importRosterToClass, type ParsedRoster, type ImportResultRow } from "@/services/roster-import";

function errorMessage(error: unknown, fallback: string) {
  return error instanceof Error ? error.message : fallback;
}

export default function ClassRosterImportPanel({ classId, className, onImported }: {
  classId: number;
  className: string;
  onImported?: () => void;
}) {
  const toast = useToast();
  const [parsed, setParsed] = useState<ParsedRoster | null>(null);
  const [importing, setImporting] = useState(false);
  const [importResults, setImportResults] = useState<ImportResultRow[] | null>(null);

  async function handleFile(file: File) {
    try {
      setParsed(await parseRosterFile(file));
      setImportResults(null);
    } catch (error) {
      toast("error", errorMessage(error, "Không đọc được file — kiểm tra lại đúng định dạng .xls/.xlsx."));
    }
  }

  async function handleImport() {
    if (!parsed) return;
    setImporting(true);
    try {
      const students = parsed.students.map((s) => ({
        studentCode: s.studentCode,
        fullName: s.fullName,
        className,
        birthDate: s.birthDate,
      }));
      const results = await importRosterToClass(classId, students);
      setImportResults(results);
      const ok = results.filter((r) => r.status !== "error");
      toast(ok.length ? "success" : "error", `Đã xử lý ${results.length} dòng — ${ok.length} thành công.`);
      onImported?.();
    } catch (error) {
      toast("error", errorMessage(error, "Chưa nhập được danh sách — kiểm tra Edge Function import-roster đã deploy chưa."));
    } finally {
      setImporting(false);
    }
  }

  return (
    <div className="space-y-5">
      <section className="rounded-3xl border border-white/10 bg-gradient-to-br from-[#172c46] to-[#071426] p-6">
        <p className="text-xs font-bold uppercase tracking-[.16em] text-blue-300">THPT · Nhập danh sách</p>
        <h2 className="mt-2 font-display text-2xl font-bold text-white">Nhập danh sách lớp {className}</h2>
        <p className="mt-2 text-sm text-slate-400">
          Chọn file Excel danh sách học sinh → tự tạo tài khoản (mật khẩu là mã số học sinh) và thêm
          vào lớp. Học sinh đã có tài khoản sẽ được thêm vào lớp mà không đổi mật khẩu.
        </p>
      </section>

      <section className="rounded-2xl border border-white/10 bg-[#0B1020] p-5">
        <label className="flex cursor-pointer items-center gap-2 rounded-xl border border-dashed border-white/20 bg-white/[.03] px-4 py-3 text-sm text-slate-300 hover:border-blue-400/40">
          <Upload size={16} />
          Chọn file Excel danh sách (.xls, .xlsx)
          <input type="file" accept=".xls,.xlsx" className="hidden" onChange={(e) => { const f = e.target.files?.[0]; if (f) void handleFile(f); e.target.value = ""; }} />
        </label>

        {parsed && (
          <div className="mt-4 space-y-3">
            <div className="flex flex-wrap items-center gap-2 rounded-xl bg-white/[.04] p-3 text-sm text-slate-300">
              <FileSpreadsheet size={16} className="text-emerald-300" />
              <span>{parsed.className || "(không đọc được tên lớp)"} · {parsed.students.length} học sinh</span>
            </div>
            <div className="max-h-56 overflow-auto rounded-xl border border-white/10">
              <table className="min-w-full text-xs">
                <thead className="bg-white/5 text-slate-400"><tr><th className="p-2 text-left">Mã HS</th><th className="p-2 text-left">Họ tên</th><th className="p-2 text-left">Ngày sinh</th></tr></thead>
                <tbody>{parsed.students.slice(0, 8).map((s) => (
                  <tr key={s.studentCode} className="border-t border-white/5 text-slate-300">
                    <td className="p-2 font-mono">{s.studentCode}</td><td className="p-2">{s.fullName}</td><td className="p-2">{s.birthDate}</td>
                  </tr>
                ))}</tbody>
              </table>
              {parsed.students.length > 8 && <p className="p-2 text-xs text-slate-500">… và {parsed.students.length - 8} dòng khác.</p>}
            </div>
            <button disabled={importing} onClick={handleImport} className="flex items-center gap-2 rounded-full bg-emerald-600 px-5 py-2.5 text-sm font-bold text-white disabled:opacity-40">
              <UserPlus2 size={16} /> {importing ? "Đang tạo tài khoản…" : "Tạo tài khoản & thêm vào lớp"}
            </button>
          </div>
        )}

        {importResults && (
          <div className="mt-4 max-h-56 overflow-auto rounded-xl border border-white/10 p-3 text-xs">
            <p className="mb-2 text-slate-300">
              <UserCheck2 size={13} className="mr-1 inline text-emerald-300" />
              Mật khẩu ban đầu = mã số học sinh. Học sinh đăng nhập bằng mã số ở cả 2 ô.
            </p>
            {importResults.map((r) => (
              <div key={r.studentCode} className={`flex items-center gap-2 py-0.5 ${r.status === "error" ? "text-red-300" : r.status === "created" ? "text-emerald-300" : "text-slate-400"}`}>
                {r.status === "error" && <AlertCircle size={12} />}
                <span className="font-mono">{r.studentCode}</span>
                <span>{r.status === "created" ? "đã tạo tài khoản mới" : r.status === "linked" ? "đã có tài khoản, thêm vào lớp" : r.message}</span>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
