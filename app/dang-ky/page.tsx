"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import { getSupabase, supabaseConfigured } from "@/services/supabase";

export default function RegisterPage() {
  const router = useRouter();
  const [fullName, setFullName] = useState("");
  const [className, setClassName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [needConfirm, setNeedConfirm] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setBusy(true);
    const { data, error } = await getSupabase().auth.signUp({
      email,
      password,
      options: {
        data: { full_name: fullName.trim(), class_name: className.trim() },
      },
    });
    setBusy(false);
    if (error) {
      setError(
        error.message.includes("already registered")
          ? "Email này đã được đăng ký."
          : error.message,
      );
      return;
    }
    // Nếu dự án bật xác nhận email thì chưa có session ngay
    if (!data.session) {
      setNeedConfirm(true);
      return;
    }
    router.push("/kiem-tra");
  }

  if (needConfirm) {
    return (
      <>
        <Navbar />
        <main className="mx-auto min-h-screen w-full max-w-md px-6 pt-32 pb-20">
          <div className="rounded-2xl border border-white/10 bg-[#0B1020] p-8 text-center">
            <p className="text-3xl">📩</p>
            <h1 className="mt-3 font-display text-xl font-bold text-white">
              Kiểm tra email của em
            </h1>
            <p className="mt-3 text-sm text-slate-400">
              Thầy đã gửi link xác nhận đến <b>{email}</b>. Bấm vào link trong
              email rồi quay lại{" "}
              <Link href="/dang-nhap" className="text-[#3B82F6] hover:underline">
                đăng nhập
              </Link>{" "}
              nhé.
            </p>
          </div>
        </main>
        <Footer />
      </>
    );
  }

  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-md px-6 pt-32 pb-20">
        <h1 className="font-display text-3xl font-bold text-white">
          Đăng ký <span className="text-gradient">tài khoản</span>
        </h1>
        {!supabaseConfigured ? (
          <p className="mt-6 text-slate-400">
            Hệ thống đang được cấu hình, vui lòng quay lại sau.
          </p>
        ) : (
          <form onSubmit={handleSubmit} className="mt-8 space-y-4">
            <div>
              <label
                htmlFor="full-name"
                className="mb-1 block text-sm font-medium text-slate-300"
              >
                Họ và tên
              </label>
              <input
                id="full-name"
                required
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                placeholder="Nguyễn Văn A"
                className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-2.5 text-white placeholder:text-slate-500 focus:border-[#3B82F6] focus:outline-none"
              />
            </div>
            <div>
              <label
                htmlFor="class-name"
                className="mb-1 block text-sm font-medium text-slate-300"
              >
                Lớp
              </label>
              <input
                id="class-name"
                required
                value={className}
                onChange={(e) => setClassName(e.target.value)}
                placeholder="11A1"
                className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-2.5 text-white placeholder:text-slate-500 focus:border-[#3B82F6] focus:outline-none"
              />
            </div>
            <div>
              <label
                htmlFor="email"
                className="mb-1 block text-sm font-medium text-slate-300"
              >
                Email
              </label>
              <input
                id="email"
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-2.5 text-white focus:border-[#3B82F6] focus:outline-none"
              />
            </div>
            <div>
              <label
                htmlFor="password"
                className="mb-1 block text-sm font-medium text-slate-300"
              >
                Mật khẩu (tối thiểu 6 ký tự)
              </label>
              <input
                id="password"
                type="password"
                required
                minLength={6}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-2.5 text-white focus:border-[#3B82F6] focus:outline-none"
              />
            </div>
            {error && <p className="text-sm text-red-400">{error}</p>}
            <button
              type="submit"
              disabled={busy}
              className="w-full rounded-full bg-[#2563EB] px-5 py-3 text-sm font-semibold text-white hover:bg-[#1D4ED8] disabled:opacity-50"
            >
              {busy ? "Đang tạo tài khoản…" : "Đăng ký"}
            </button>
            <p className="text-center text-sm text-slate-400">
              Đã có tài khoản?{" "}
              <Link
                href="/dang-nhap"
                className="text-[#3B82F6] hover:underline"
              >
                Đăng nhập
              </Link>
            </p>
          </form>
        )}
      </main>
      <Footer />
    </>
  );
}
