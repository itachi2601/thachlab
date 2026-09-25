"use client";

import { useCallback, useEffect, useState } from "react";
import { Clock3, Copy, KeyRound, Link2, Trash2 } from "lucide-react";
import { useToast } from "@/components/ui/Toast";
import { SITE_URL } from "@/lib/site";
import {
  adminResetPasswordToStudentCode,
  createPasswordResetCode,
  fetchPasswordResetCodesForStudent,
  revokePasswordResetCode,
  type PasswordResetCode,
} from "@/services/password-reset";

function errorMessage(error: unknown, fallback: string) {
  return error instanceof Error ? error.message : fallback;
}

function resetLink(code: string) {
  return `${SITE_URL}/quen-mat-khau?ma=${code}`;
}

/**
 * Thẻ "Mật khẩu" trong hồ sơ một học sinh (dashboard THPT): gặp trực tiếp thì đặt thẳng
 * mật khẩu về mã số HS; không gặp mặt thì tạo mã, gửi link qua Zalo để em tự đặt mật khẩu
 * mới ở /quen-mat-khau (không cần đăng nhập trước).
 */
export default function PasswordResetCard({ studentId, studentName }: { studentId: string; studentName: string }) {
  const toast = useToast();
  const [codes, setCodes] = useState<PasswordResetCode[] | null>(null);
  // Chụp lại "bây giờ" mỗi lần tải danh sách, thay vì gọi Date.now() ngay trong render
  // (impure, ESLint react-hooks/purity chặn) — đủ chính xác vì component không cần đếm giây.
  const [now, setNow] = useState(() => Date.now());
  const [busyDirect, setBusyDirect] = useState(false);
  const [busyCode, setBusyCode] = useState(false);

  const reload = useCallback(() => {
    fetchPasswordResetCodesForStudent(studentId)
      .then((rows) => { setCodes(rows); setNow(Date.now()); })
      .catch(() => { setCodes([]); setNow(Date.now()); });
  }, [studentId]);

  // Đổi học sinh -> hồ sơ truyền key={studentId} nên component dựng lại, state tự về đầu.
  useEffect(() => {
    reload();
  }, [reload]);

  async function copy(text: string, what: string) {
    try {
      await navigator.clipboard.writeText(text);
      toast("success", `Đã chép ${what}.`);
    } catch {
      toast("error", "Trình duyệt không cho chép tự động — bôi đen rồi chép tay nhé.");
    }
  }

  async function resetDirect() {
    if (!window.confirm(`Đặt lại mật khẩu của "${studentName}" về đúng mã số học sinh?`)) return;
    setBusyDirect(true);
    try {
      const password = await adminResetPasswordToStudentCode(studentId);
      reload();
      toast("success", `Đã đặt lại — mật khẩu mới là "${password}".`);
    } catch (error) {
      toast("error", errorMessage(error, "Chưa đặt lại được mật khẩu."));
    } finally {
      setBusyDirect(false);
    }
  }

  async function createCode() {
    setBusyCode(true);
    try {
      const created = await createPasswordResetCode(studentId);
      reload();
      await copy(resetLink(created.code), "link đặt lại mật khẩu");
    } catch (error) {
      toast("error", errorMessage(error, "Chưa tạo được mã."));
    } finally {
      setBusyCode(false);
    }
  }

  async function revoke(code: PasswordResetCode) {
    if (!window.confirm(`Huỷ mã ${code.code}?`)) return;
    try {
      await revokePasswordResetCode(code.id);
      reload();
      toast("success", "Đã huỷ mã.");
    } catch (error) {
      toast("error", errorMessage(error, "Chưa huỷ được mã."));
    }
  }

  const pending = (codes ?? []).filter((c) => !c.used_at && new Date(c.expires_at).getTime() > now);

  return (
    <section className="rounded-2xl border border-white/10 bg-panel p-5">
      <h4 className="font-display text-lg font-bold text-white">Mật khẩu</h4>
      <p className="mt-1 text-sm text-slate-400">
        Gặp trực tiếp thì đặt thẳng về mã số HS; không gặp mặt thì tạo mã, gửi link qua Zalo để
        em tự đặt mật khẩu mới. Mã chỉ dùng được 1 lần và hết hạn sau 24 giờ.
      </p>

      <div className="mt-4 flex flex-wrap gap-2">
        <button
          type="button"
          onClick={resetDirect}
          disabled={busyDirect}
          className="inline-flex items-center gap-2 rounded-xl border border-white/10 px-4 py-2 text-sm font-bold text-white hover:bg-white/5 disabled:opacity-40"
        >
          <KeyRound size={15} /> {busyDirect ? "Đang đặt lại…" : "Đặt về mã số HS"}
        </button>
        <button
          type="button"
          onClick={createCode}
          disabled={busyCode}
          className="inline-flex items-center gap-2 rounded-xl bg-primary px-4 py-2 text-sm font-bold text-white disabled:opacity-40"
        >
          <Link2 size={15} /> {busyCode ? "Đang tạo…" : "Tạo mã & chép link"}
        </button>
      </div>

      {pending.length > 0 && (
        <ul className="mt-4 space-y-2">
          {pending.map((code) => (
            <li
              key={code.id}
              className="flex flex-wrap items-center gap-3 rounded-xl border border-white/10 bg-white/[.02] px-3 py-2.5 text-sm"
            >
              <Clock3 size={16} className="shrink-0 text-amber-300" />
              <span className="min-w-0 flex-1">
                <span className="font-mono font-bold text-white">{code.code}</span>
                <small className="block text-slate-500">
                  Hết hạn {new Date(code.expires_at).toLocaleString("vi-VN")}
                </small>
              </span>
              <button
                type="button"
                onClick={() => copy(code.code, "mã")}
                title="Chép mã"
                className="rounded-lg border border-white/10 p-1.5 text-slate-300 hover:border-white/30"
              >
                <Copy size={14} />
              </button>
              <button
                type="button"
                onClick={() => copy(resetLink(code.code), "link")}
                title="Chép link"
                className="rounded-lg border border-white/10 p-1.5 text-slate-300 hover:border-white/30"
              >
                <Link2 size={14} />
              </button>
              <button
                type="button"
                onClick={() => revoke(code)}
                title="Huỷ mã"
                className="rounded-lg border border-red-500/30 p-1.5 text-red-300 hover:bg-red-500/10"
              >
                <Trash2 size={14} />
              </button>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
