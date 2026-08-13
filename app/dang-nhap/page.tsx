"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import { getSupabase, supabaseConfigured } from "@/services/supabase";

type UserType = "student" | "teacher";

export default function LoginPage() {
  const router = useRouter();
  const [userType, setUserType] = useState<UserType>("student");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function handleEmailLogin(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setBusy(true);

    const loginEmail = email.includes("@") ? email : `${email.trim()}@thachlab.local`;
    const { error } = await getSupabase().auth.signInWithPassword({
      email: loginEmail,
      password,
    });

    setBusy(false);
    if (error) {
      setError(
        error.message === "Invalid login credentials"
          ? "Email hoặc mật khẩu không đúng."
          : error.message,
      );
      return;
    }
    router.push(userType === "student" ? "/tai-khoan" : "/quan-tri");
  }

  async function handleGoogleLogin() {
    setError("");
    setBusy(true);

    const { error } = await getSupabase().auth.signInWithOAuth({
      provider: "google",
      options: {
        redirectTo: `${window.location.origin}/auth/callback?type=${userType}`,
      },
    });

    if (error) {
      setError(error.message);
      setBusy(false);
    }
  }

  const inputCls = "w-full rounded-xl border border-white/10 bg-white/5 px-4 py-2.5 text-white focus:border-[#3B82F6] focus:outline-none";
  const btnCls = "w-full rounded-full px-5 py-3 text-sm font-semibold transition-all disabled:opacity-50";

  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-md px-6 pt-32 pb-20">
        <h1 className="font-display text-3xl font-bold text-white">
          Đăng <span className="text-gradient">nhập</span>
        </h1>

        {!supabaseConfigured ? (
          <p className="mt-6 text-slate-400">
            Hệ thống đang được cấu hình, vui lòng quay lại sau.
          </p>
        ) : (
          <div className="mt-8">
            {/* User Type Tabs */}
            <div className="mb-6 flex gap-2 border-b border-white/10">
              <button
                onClick={() => setUserType("student")}
                className={`flex-1 px-4 py-3 text-sm font-semibold transition-colors ${
                  userType === "student"
                    ? "border-b-2 border-[#3B82F6] text-white"
                    : "text-slate-400 hover:text-slate-300"
                }`}
              >
                👨‍🎓 Học sinh
              </button>
              <button
                onClick={() => setUserType("teacher")}
                className={`flex-1 px-4 py-3 text-sm font-semibold transition-colors ${
                  userType === "teacher"
                    ? "border-b-2 border-[#3B82F6] text-white"
                    : "text-slate-400 hover:text-slate-300"
                }`}
              >
                👨‍🏫 Giáo viên
              </button>
            </div>

            {/* Google Login */}
            <button
              onClick={handleGoogleLogin}
              disabled={busy}
              className={`${btnCls} mb-4 border border-white/10 bg-white/5 text-white hover:bg-white/10`}
            >
              {busy ? "Đang xử lý…" : "🔐 Đăng nhập với Google"}
            </button>

            {/* Divider */}
            <div className="mb-4 flex items-center gap-3">
              <div className="flex-1 border-t border-white/10" />
              <span className="text-xs text-slate-500">Hoặc</span>
              <div className="flex-1 border-t border-white/10" />
            </div>

            {/* Email/Password Form */}
            <form onSubmit={handleEmailLogin} className="space-y-4">
              <div>
                <label
                  htmlFor="email"
                  className="mb-1 block text-sm font-medium text-slate-300"
                >
                  Email hoặc tên đăng nhập
                </label>
                <input
                  id="email"
                  type="text"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className={inputCls}
                />
              </div>
              <div>
                <label
                  htmlFor="password"
                  className="mb-1 block text-sm font-medium text-slate-300"
                >
                  Mật khẩu
                </label>
                <input
                  id="password"
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className={inputCls}
                />
              </div>
              {error && <p className="text-sm text-red-400">❌ {error}</p>}
              <button
                type="submit"
                disabled={busy}
                className={`${btnCls} bg-[#2563EB] text-white hover:bg-[#1D4ED8]`}
              >
                {busy ? "Đang đăng nhập…" : "Đăng nhập"}
              </button>
            </form>

            {/* Signup Link */}
            {userType === "student" && (
              <p className="mt-4 text-center text-sm text-slate-400">
                Chưa có tài khoản?{" "}
                <Link href="/dang-ky" className="text-[#3B82F6] hover:underline">
                  Đăng ký ngay
                </Link>
              </p>
            )}

            {userType === "teacher" && (
              <p className="mt-4 text-center text-xs text-slate-500">
                Liên hệ quản trị viên để được cấp tài khoản giáo viên
              </p>
            )}
          </div>
        )}
      </main>
      <Footer />
    </>
  );
}
