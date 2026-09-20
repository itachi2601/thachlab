"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import { getSupabase, supabaseConfigured } from "@/services/supabase";
import { useToast } from "@/components/ui/Toast";

const inputCls = "w-full rounded-xl border border-white/10 bg-white/5 px-4 py-2.5 text-white focus:border-primary focus:outline-none";

export default function ResetPasswordPage() {
  const router = useRouter();
  const toast = useToast();
  // "checking": đang đổi mã liên kết lấy phiên đăng nhập tạm; "ready": có thể nhập mật khẩu mới.
  const [status, setStatus] = useState<"checking" | "ready" | "invalid">("checking");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    if (!supabaseConfigured) return;

    const params = new URLSearchParams(window.location.search);
    const code = params.get("code");
    if (!code) {
      setStatus("invalid");
      return;
    }

    getSupabase()
      .auth.exchangeCodeForSession(code)
      .then(({ error }) => setStatus(error ? "invalid" : "ready"));
  }, []);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");

    if (password.length < 6) {
      setError("Mật khẩu phải dài tối thiểu 6 ký tự");
      return;
    }
    if (password !== confirmPassword) {
      setError("Mật khẩu xác nhận không khớp");
      return;
    }

    setBusy(true);
    const { error } = await getSupabase().auth.updateUser({ password });
    setBusy(false);

    if (error) {
      setError(error.message);
      return;
    }

    toast("success", "Đặt lại mật khẩu thành công!");
    router.replace("/tai-khoan");
  }

  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-md px-6 pt-32 pb-20">
        <h1 className="font-display text-3xl font-bold text-white">
          Đặt lại <span className="text-gradient">mật khẩu</span>
        </h1>

        {!supabaseConfigured ? (
          <p className="mt-6 text-slate-400">
            Hệ thống đang được cấu hình, vui lòng quay lại sau.
          </p>
        ) : status === "checking" ? (
          <p className="mt-6 text-slate-400">Đang xác thực liên kết…</p>
        ) : status === "invalid" ? (
          <div className="mt-8 space-y-4 rounded-2xl border border-white/10 bg-[#0B1020] p-6">
            <p className="text-sm text-slate-300">
              ❌ Liên kết không hợp lệ hoặc đã hết hạn. Hãy yêu cầu một liên kết mới.
            </p>
            <Link href="/quen-mat-khau" className="text-sm text-primary hover:underline">
              ← Gửi lại liên kết đặt lại mật khẩu
            </Link>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="mt-8 space-y-4">
            <div>
              <label htmlFor="password" className="mb-1 block text-sm font-medium text-slate-300">
                Mật khẩu mới
              </label>
              <input
                id="password"
                type="password"
                required
                autoFocus
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Tối thiểu 6 ký tự"
                className={inputCls}
              />
            </div>
            <div>
              <label htmlFor="confirmPassword" className="mb-1 block text-sm font-medium text-slate-300">
                Xác nhận mật khẩu mới
              </label>
              <input
                id="confirmPassword"
                type="password"
                required
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                className={inputCls}
              />
            </div>
            {error && <p className="text-sm text-red-400">❌ {error}</p>}
            <button
              type="submit"
              disabled={busy}
              className="w-full rounded-full bg-[#2563EB] px-5 py-3 text-sm font-semibold text-white transition-all hover:bg-primary-dark disabled:opacity-50"
            >
              {busy ? "Đang lưu…" : "Đặt lại mật khẩu"}
            </button>
          </form>
        )}
      </main>
      <Footer />
    </>
  );
}
