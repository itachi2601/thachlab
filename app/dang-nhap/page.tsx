"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import { getSupabase, supabaseConfigured } from "@/services/supabase";
import { useAuth } from "@/components/auth/AuthProvider";
import { useToast } from "@/components/ui/Toast";

type UserType = "student" | "teacher";

export default function LoginPage() {
  const router = useRouter();
  const toast = useToast();
  const { session, profile, loading: authLoading } = useAuth();
  const [userType, setUserType] = useState<UserType>("student");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  // Đã đăng nhập rồi (vd bấm Back, hoặc mở lại tab cũ) -> đưa thẳng vào đúng không gian, không hiện lại form.
  // ?next=/duong-dan (chỉ nhận đường dẫn nội bộ bắt đầu bằng 1 dấu "/") để quay lại trang vừa bị chặn,
  // vd /phu-huynh; phụ huynh không có next thì về thẳng trang kết quả của con.
  useEffect(() => {
    if (authLoading || !session) return;
    const next = new URLSearchParams(window.location.search).get("next");
    let to = "/tai-khoan";
    if (next && /^\/(?!\/)/.test(next)) to = next;
    else if (profile?.role === "admin" || profile?.role === "instructor") to = "/quan-tri";
    else if (profile?.role === "parent") to = "/phu-huynh";
    router.replace(to);
    // WebView cũ / mạng yếu đôi khi router.replace không chạy (kẹt "đang chuyển hướng"): sau 2,5s chuyển cứng.
    const t = window.setTimeout(() => window.location.assign(to), 2500);
    return () => window.clearTimeout(t);
  }, [authLoading, session, profile, router]);

  async function handleEmailLogin(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setBusy(true);

    const typed = email.trim().toLowerCase();
    let loginEmail = typed;
    if (!typed.includes("@")) {
      // Em đăng ký kèm email thật thì tài khoản auth dùng email đó — tra theo username; chưa có hàm/không khớp thì dùng email nội bộ.
      const { data: resolved } = await getSupabase().rpc("resolve_login_email", { p_login: typed });
      loginEmail = typeof resolved === "string" && resolved ? resolved : `${typed}@thachlab.local`;
    }
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
    toast("success", "Đăng nhập thành công!");
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

  const inputCls = "w-full rounded-xl border border-line-strong bg-surface-2 px-4 py-2.5 text-ink focus:border-primary focus:outline-none";
  const btnCls = "w-full rounded-full px-5 py-3 text-sm font-semibold transition-all disabled:opacity-50";

  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-md px-6 pt-32 pb-20">
        <h1 className="font-display text-3xl font-bold text-ink">
          Đăng <span className="text-gradient">nhập</span>
        </h1>

        {authLoading || session ? (
          <p className="mt-6 text-muted">
            {session ? "Bạn đã đăng nhập — đang chuyển hướng…" : "Đang kiểm tra đăng nhập…"}
            {session && (
              <>
                {" "}
                <a href="/tai-khoan" className="font-semibold text-primary underline">Bấm vào đây nếu không tự chuyển</a>
              </>
            )}
          </p>
        ) : !supabaseConfigured ? (
          <p className="mt-6 text-muted">
            Hệ thống đang được cấu hình, vui lòng quay lại sau.
          </p>
        ) : (
          <div className="mt-8">
            {/* User Type Tabs */}
            <div className="mb-6 flex gap-2 border-b border-line">
              <button
                onClick={() => setUserType("student")}
                className={`flex-1 px-4 py-3 text-sm font-semibold transition-colors ${
                  userType === "student"
                    ? "border-b-2 border-primary text-ink"
                    : "text-muted hover:text-ink"
                }`}
              >
                👨‍🎓 Học sinh
              </button>
              <button
                onClick={() => setUserType("teacher")}
                className={`flex-1 px-4 py-3 text-sm font-semibold transition-colors ${
                  userType === "teacher"
                    ? "border-b-2 border-primary text-ink"
                    : "text-muted hover:text-ink"
                }`}
              >
                👨‍🏫 Giáo viên
              </button>
            </div>

            {/* Google Login */}
            <button
              onClick={handleGoogleLogin}
              disabled={busy}
              className={`${btnCls} mb-4 border border-line-strong bg-panel text-ink hover:bg-primary-soft`}
            >
              {busy ? "Đang xử lý…" : "🔐 Đăng nhập với Google"}
            </button>

            {/* Divider */}
            <div className="mb-4 flex items-center gap-3">
              <div className="flex-1 border-t border-line" />
              <span className="text-xs text-muted">Hoặc</span>
              <div className="flex-1 border-t border-line" />
            </div>

            {/* Email/Password Form */}
            <form onSubmit={handleEmailLogin} className="space-y-4">
              <div>
                <label
                  htmlFor="email"
                  className="mb-1 block text-sm font-medium text-ink"
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
                <div className="mb-1 flex items-center justify-between">
                  <label htmlFor="password" className="block text-sm font-medium text-ink">
                    Mật khẩu
                  </label>
                  {userType === "student" && (
                    <Link href="/quen-mat-khau" className="text-xs text-primary hover:underline">
                      Quên mật khẩu?
                    </Link>
                  )}
                </div>
                <input
                  id="password"
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className={inputCls}
                />
              </div>
              {error && <p className="text-sm text-danger">❌ {error}</p>}
              <button
                type="submit"
                disabled={busy}
                className={`${btnCls} bg-primary text-white hover:bg-primary-dark`}
              >
                {busy ? "Đang đăng nhập…" : "Đăng nhập"}
              </button>
            </form>

            {/* Signup Link */}
            {userType === "student" && (
              <p className="mt-4 text-center text-sm text-muted">
                Chưa có tài khoản?{" "}
                <Link href="/dang-ky" className="text-primary hover:underline">
                  Đăng ký ngay
                </Link>
              </p>
            )}

            {userType === "teacher" && (
              <p className="mt-4 text-center text-xs text-muted">
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
