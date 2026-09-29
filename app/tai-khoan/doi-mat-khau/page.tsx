"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Check, KeyRound } from "lucide-react";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import RequireAuth from "@/components/auth/RequireAuth";
import { useToast } from "@/components/ui/Toast";
import { changeMyPassword } from "@/services/password-reset";

const inputCls =
  "w-full rounded-xl border border-white/10 bg-white/5 px-4 py-2.5 text-white placeholder:text-slate-500 focus:border-primary focus:outline-none";

function errorMessage(error: unknown, fallback: string) {
  return error instanceof Error ? error.message : fallback;
}

function Card({ children }: { children: React.ReactNode }) {
  return <div className="mx-auto max-w-md rounded-3xl border border-white/10 bg-panel p-8">{children}</div>;
}

function ChangePasswordForm() {
  const router = useRouter();
  const toast = useToast();
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [busy, setBusy] = useState(false);
  const [done, setDone] = useState(false);

  if (done)
    return (
      <Card>
        <Check className="mx-auto text-emerald-300" size={40} />
        <h1 className="mt-4 text-center font-display text-xl font-bold text-white">Đã đổi mật khẩu</h1>
        <p className="mt-2 text-center text-sm text-slate-400">
          Mật khẩu mới đã có hiệu lực — lần đăng nhập sau nhớ dùng mật khẩu này.
        </p>
        <Link
          href="/tai-khoan"
          className="mt-6 flex items-center justify-center rounded-xl bg-primary py-3 text-sm font-bold text-white"
        >
          Về Tài khoản của tôi
        </Link>
      </Card>
    );

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!currentPassword) {
      toast("error", "Nhập mật khẩu hiện tại.");
      return;
    }
    if (newPassword.length < 6) {
      toast("error", "Mật khẩu mới phải từ 6 ký tự trở lên.");
      return;
    }
    if (newPassword !== confirmPassword) {
      toast("error", "Hai lần nhập mật khẩu mới không khớp.");
      return;
    }
    setBusy(true);
    try {
      await changeMyPassword(currentPassword, newPassword);
      setDone(true);
    } catch (error) {
      toast("error", errorMessage(error, "Chưa đổi được mật khẩu."));
    } finally {
      setBusy(false);
    }
  }

  return (
    <Card>
      <KeyRound className="mx-auto text-primary" size={36} />
      <h1 className="mt-4 text-center font-display text-xl font-bold text-white">Đổi mật khẩu</h1>
      <p className="mt-2 text-center text-sm text-slate-400">
        Nhập mật khẩu hiện tại và mật khẩu mới muốn dùng từ giờ.
      </p>
      <form onSubmit={submit} className="mt-5 space-y-3">
        <input
          value={currentPassword}
          onChange={(e) => setCurrentPassword(e.target.value)}
          type="password"
          placeholder="Mật khẩu hiện tại"
          autoComplete="current-password"
          className={inputCls}
        />
        <input
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
          type="password"
          placeholder="Mật khẩu mới (từ 6 ký tự)"
          autoComplete="new-password"
          className={inputCls}
        />
        <input
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          type="password"
          placeholder="Nhập lại mật khẩu mới"
          autoComplete="new-password"
          className={inputCls}
        />
        <button
          type="submit"
          disabled={busy}
          className="w-full rounded-xl bg-primary py-3 text-sm font-bold text-white disabled:opacity-40"
        >
          {busy ? "Đang đổi…" : "Đổi mật khẩu"}
        </button>
      </form>
      <p className="mt-4 text-center text-xs text-slate-500">
        Quên mật khẩu hiện tại?{" "}
        <Link href="/quen-mat-khau" className="text-blue-300">
          Nhờ giáo viên cấp mã đặt lại
        </Link>
      </p>
      <button
        type="button"
        onClick={() => router.push("/tai-khoan")}
        className="mt-2 w-full text-center text-xs text-slate-500 hover:text-slate-300"
      >
        ← Quay lại Tài khoản của tôi
      </button>
    </Card>
  );
}

export default function DoiMatKhauPage() {
  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-4xl px-5 pt-28 pb-16">
        <RequireAuth>
          <ChangePasswordForm />
        </RequireAuth>
      </main>
      <Footer />
    </>
  );
}
