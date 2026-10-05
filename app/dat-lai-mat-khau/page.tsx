"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Check, KeyRound } from "lucide-react";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import { useToast } from "@/components/ui/Toast";
import { getSupabase } from "@/services/supabase";
import { setNewPasswordFromRecovery } from "@/services/password-reset";

const inputCls =
  "w-full rounded-xl border border-white/10 bg-white/5 px-4 py-2.5 text-white placeholder:text-slate-500 focus:border-primary focus:outline-none";

function Card({ children }: { children: React.ReactNode }) {
  return <div className="mx-auto max-w-md rounded-3xl border border-white/10 bg-panel p-8">{children}</div>;
}

export default function DatLaiMatKhauPage() {
  const toast = useToast();
  // Link trong email mở trang này kèm token; supabase-js đọc token và tạo phiên khôi phục.
  const [ready, setReady] = useState<"checking" | "ok" | "invalid">("checking");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [busy, setBusy] = useState(false);
  const [done, setDone] = useState(false);

  useEffect(() => {
    const supabase = getSupabase();
    const { data: sub } = supabase.auth.onAuthStateChange((event, session) => {
      if (event === "PASSWORD_RECOVERY" || (event === "SIGNED_IN" && session)) setReady("ok");
    });
    supabase.auth.getSession().then(({ data }) => {
      if (data.session) setReady("ok");
    });
    const t = setTimeout(() => setReady((r) => (r === "checking" ? "invalid" : r)), 4000);
    return () => {
      sub.subscription.unsubscribe();
      clearTimeout(t);
    };
  }, []);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (password.length < 6) {
      toast("error", "Mật khẩu mới phải từ 6 ký tự trở lên.");
      return;
    }
    if (password !== confirmPassword) {
      toast("error", "Hai lần nhập mật khẩu không khớp.");
      return;
    }
    setBusy(true);
    try {
      await setNewPasswordFromRecovery(password);
      setDone(true);
    } catch (error) {
      toast("error", error instanceof Error ? error.message : "Chưa đặt lại được mật khẩu.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-4xl px-5 pt-28 pb-16">
        {done ? (
          <Card>
            <Check className="mx-auto text-emerald-300" size={40} />
            <h1 className="mt-4 text-center font-display text-xl font-bold text-white">Đã đặt lại mật khẩu</h1>
            <p className="mt-2 text-center text-sm text-slate-400">Lần đăng nhập sau em dùng mật khẩu vừa đặt.</p>
            <Link href="/tai-khoan" className="mt-6 flex items-center justify-center rounded-xl bg-primary py-3 text-sm font-bold text-white">
              Vào Tài khoản của tôi
            </Link>
          </Card>
        ) : ready === "checking" ? (
          <Card><p className="text-center text-slate-400">Đang kiểm tra link…</p></Card>
        ) : ready === "invalid" ? (
          <Card>
            <h1 className="text-center font-display text-xl font-bold text-white">Link không dùng được</h1>
            <p className="mt-2 text-center text-sm text-slate-400">
              Link đã hết hạn, đã dùng rồi, hoặc mở bằng trình duyệt khác. Em gửi lại link mới nhé.
            </p>
            <Link href="/quen-mat-khau" className="mt-6 flex items-center justify-center rounded-xl bg-primary py-3 text-sm font-bold text-white">
              Gửi lại link
            </Link>
          </Card>
        ) : (
          <Card>
            <KeyRound className="mx-auto text-primary" size={36} />
            <h1 className="mt-4 text-center font-display text-xl font-bold text-white">Đặt mật khẩu mới</h1>
            <form onSubmit={submit} className="mt-5 space-y-3">
              <input value={password} onChange={(e) => setPassword(e.target.value)} type="password" placeholder="Mật khẩu mới (từ 6 ký tự)" autoComplete="new-password" className={inputCls} />
              <input value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} type="password" placeholder="Nhập lại mật khẩu mới" autoComplete="new-password" className={inputCls} />
              <button type="submit" disabled={busy} className="w-full rounded-xl bg-primary py-3 text-sm font-bold text-white disabled:opacity-40">
                {busy ? "Đang lưu…" : "Đặt mật khẩu"}
              </button>
            </form>
          </Card>
        )}
      </main>
      <Footer />
    </>
  );
}
