"use client";

import { Suspense, useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { Check, KeyRound, Mail } from "lucide-react";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import { useToast } from "@/components/ui/Toast";
import { claimPasswordReset, requestPasswordResetEmail } from "@/services/password-reset";

const inputCls =
  "w-full rounded-xl border border-white/10 bg-white/5 px-4 py-2.5 text-white placeholder:text-slate-500 focus:border-primary focus:outline-none";

function errorMessage(error: unknown, fallback: string) {
  return error instanceof Error ? error.message : fallback;
}

function Card({ children }: { children: React.ReactNode }) {
  return <div className="mx-auto max-w-md rounded-3xl border border-white/10 bg-panel p-8">{children}</div>;
}

function EmailReset({ onUseCode }: { onUseCode: () => void }) {
  const toast = useToast();
  const [login, setLogin] = useState("");
  const [busy, setBusy] = useState(false);
  const [state, setState] = useState<"form" | "sent" | "no_email">("form");

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!login.trim()) {
      toast("error", "Nhập email hoặc tên đăng nhập của em.");
      return;
    }
    setBusy(true);
    try {
      setState(await requestPasswordResetEmail(login));
    } catch (error) {
      toast("error", errorMessage(error, "Chưa gửi được email."));
    } finally {
      setBusy(false);
    }
  }

  if (state === "sent")
    return (
      <Card>
        <Mail className="mx-auto text-emerald-300" size={40} />
        <h1 className="mt-4 text-center font-display text-xl font-bold text-white">Kiểm tra email của em</h1>
        <p className="mt-2 text-center text-sm text-slate-400">
          Nếu tài khoản có email, em sẽ nhận được link đặt lại mật khẩu trong ít phút (xem cả mục Thư rác).
          Mở link bằng chính trình duyệt này.
        </p>
        <button type="button" onClick={() => setState("form")} className="mt-5 w-full text-center text-xs text-slate-400 hover:text-slate-200">
          Gửi lại / nhập email khác
        </button>
      </Card>
    );

  return (
    <Card>
      <Mail className="mx-auto text-primary" size={36} />
      <h1 className="mt-4 text-center font-display text-xl font-bold text-white">Quên mật khẩu</h1>
      <p className="mt-2 text-center text-sm text-slate-400">
        Nhập email hoặc tên đăng nhập, hệ thống gửi link đặt lại mật khẩu qua email cho em.
      </p>
      <form onSubmit={submit} className="mt-5 space-y-3">
        <input
          value={login}
          onChange={(e) => setLogin(e.target.value)}
          placeholder="Email hoặc tên đăng nhập"
          autoComplete="username"
          className={inputCls}
        />
        {state === "no_email" && (
          <p className="rounded-xl border border-amber-400/30 bg-amber-400/10 px-3 py-2 text-xs text-amber-200">
            Tài khoản này chưa có email thật nên không gửi được. Em nhờ giáo viên cấp mã rồi bấm “Đã có mã từ giáo viên” bên dưới.
          </p>
        )}
        <button
          type="submit"
          disabled={busy}
          className="w-full rounded-xl bg-primary py-3 text-sm font-bold text-white disabled:opacity-40"
        >
          {busy ? "Đang gửi…" : "Gửi link đặt lại mật khẩu"}
        </button>
      </form>
      <button type="button" onClick={onUseCode} className="mt-4 w-full text-center text-xs text-blue-300">
        Đã có mã từ giáo viên
      </button>
      <p className="mt-3 text-center text-xs text-slate-500">
        Nhớ mật khẩu rồi?{" "}
        <Link href="/dang-nhap" className="text-blue-300">
          Đăng nhập
        </Link>
      </p>
    </Card>
  );
}

function ResetContent() {
  const searchParams = useSearchParams();
  const toast = useToast();
  const [code, setCode] = useState((searchParams.get("ma") ?? "").toUpperCase());
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [busy, setBusy] = useState(false);
  const [done, setDone] = useState<string | null>(null);
  const [useCode, setUseCode] = useState(Boolean(searchParams.get("ma")));

  if (!useCode && !done) return <EmailReset onUseCode={() => setUseCode(true)} />;

  if (done)
    return (
      <Card>
        <Check className="mx-auto text-emerald-300" size={40} />
        <h1 className="mt-4 text-center font-display text-xl font-bold text-white">Đã đặt lại mật khẩu</h1>
        <p className="mt-2 text-center text-sm text-slate-400">
          Mật khẩu mới của {done} đã sẵn sàng — đăng nhập lại bằng mật khẩu vừa đặt.
        </p>
        <Link
          href="/dang-nhap"
          className="mt-6 flex items-center justify-center rounded-xl bg-primary py-3 text-sm font-bold text-white"
        >
          Đăng nhập
        </Link>
      </Card>
    );

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!code.trim()) {
      toast("error", "Nhập mã giáo viên đã gửi.");
      return;
    }
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
      const result = await claimPasswordReset(code, password);
      setDone(result.studentName || "bạn");
    } catch (error) {
      toast("error", errorMessage(error, "Chưa đặt lại được mật khẩu."));
    } finally {
      setBusy(false);
    }
  }

  return (
    <Card>
      <KeyRound className="mx-auto text-primary" size={36} />
      <h1 className="mt-4 text-center font-display text-xl font-bold text-white">Đặt lại mật khẩu</h1>
      <p className="mt-2 text-center text-sm text-slate-400">
        Nhập mã giáo viên đã gửi qua Zalo và mật khẩu mới. Chưa có mã thì nhờ giáo viên chủ
        nhiệm hoặc giáo viên bộ môn cấp mã, hoặc quay lại nhận link qua email.
      </p>
      <form onSubmit={submit} className="mt-5 space-y-3">
        <input
          value={code}
          onChange={(e) => setCode(e.target.value.toUpperCase())}
          placeholder="Mã giáo viên cấp (RSxxxxxx)"
          className={`${inputCls} font-mono uppercase`}
        />
        <input
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          type="password"
          placeholder="Mật khẩu mới (từ 6 ký tự)"
          className={inputCls}
        />
        <input
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          type="password"
          placeholder="Nhập lại mật khẩu mới"
          className={inputCls}
        />
        <button
          type="submit"
          disabled={busy}
          className="w-full rounded-xl bg-primary py-3 text-sm font-bold text-white disabled:opacity-40"
        >
          {busy ? "Đang đặt lại…" : "Đặt lại mật khẩu"}
        </button>
      </form>
      <p className="mt-4 text-center text-xs text-slate-500">
        <button type="button" onClick={() => setUseCode(false)} className="text-blue-300">
          ← Nhận link qua email thay vì dùng mã
        </button>
      </p>
    </Card>
  );
}

export default function QuenMatKhauPage() {
  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-4xl px-5 pt-28 pb-16">
        <Suspense fallback={<Card><p className="text-center text-slate-400">Đang tải…</p></Card>}>
          <ResetContent />
        </Suspense>
      </main>
      <Footer />
    </>
  );
}
