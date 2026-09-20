"use client";

import { useState } from "react";
import Link from "next/link";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import { getSupabase, supabaseConfigured } from "@/services/supabase";

const inputCls = "w-full rounded-xl border border-white/10 bg-white/5 px-4 py-2.5 text-white focus:border-primary focus:outline-none placeholder:text-slate-600";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [sent, setSent] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim())) {
      setError("Vui lòng nhập một địa chỉ email hợp lệ.");
      return;
    }

    setBusy(true);
    const { error } = await getSupabase().auth.resetPasswordForEmail(email.trim(), {
      redirectTo: `${window.location.origin}/dat-lai-mat-khau/`,
    });
    setBusy(false);

    // Luôn báo thành công dù email có tồn tại hay không, tránh lộ thông tin tài khoản nào đã đăng ký.
    if (error) setError(error.message);
    else setSent(true);
  }

  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-md px-6 pt-32 pb-20">
        <h1 className="font-display text-3xl font-bold text-white">
          Quên <span className="text-gradient">mật khẩu</span>
        </h1>

        {!supabaseConfigured ? (
          <p className="mt-6 text-slate-400">
            Hệ thống đang được cấu hình, vui lòng quay lại sau.
          </p>
        ) : sent ? (
          <div className="mt-8 space-y-4 rounded-2xl border border-white/10 bg-[#0B1020] p-6">
            <p className="text-sm text-slate-300">
              ✓ Nếu <strong className="text-white">{email}</strong> đã được đăng ký, một liên kết đặt lại
              mật khẩu vừa được gửi tới email đó. Kiểm tra cả hộp thư Spam/Quảng cáo nếu chưa thấy.
            </p>
            <Link href="/dang-nhap" className="text-sm text-primary hover:underline">
              ← Quay lại đăng nhập
            </Link>
          </div>
        ) : (
          <div className="mt-8">
            <p className="mb-6 text-sm text-slate-400">
              Nhập email đã đăng ký, hệ thống sẽ gửi liên kết để bạn đặt lại mật khẩu.
            </p>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="email" className="mb-1 block text-sm font-medium text-slate-300">
                  Email
                </label>
                <input
                  id="email"
                  type="email"
                  required
                  autoFocus
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="example@gmail.com"
                  className={inputCls}
                />
              </div>
              {error && <p className="text-sm text-red-400">❌ {error}</p>}
              <button
                type="submit"
                disabled={busy}
                className="w-full rounded-full bg-[#2563EB] px-5 py-3 text-sm font-semibold text-white transition-all hover:bg-primary-dark disabled:opacity-50"
              >
                {busy ? "Đang gửi…" : "Gửi liên kết đặt lại mật khẩu"}
              </button>
            </form>

            <div className="mt-4 rounded-lg border border-amber-500/30 bg-amber-500/5 p-3">
              <p className="text-xs text-amber-300">
                ℹ️ Nếu bạn đăng ký chỉ bằng tên đăng nhập (không có email), cách này sẽ không dùng được —
                hãy nhờ giáo viên phụ trách lớp cấp lại mật khẩu.
              </p>
            </div>

            <p className="mt-4 text-center text-sm text-slate-400">
              Đã nhớ mật khẩu?{" "}
              <Link href="/dang-nhap" className="text-primary hover:underline">
                Đăng nhập
              </Link>
            </p>
          </div>
        )}
      </main>
      <Footer />
    </>
  );
}
