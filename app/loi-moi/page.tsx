"use client";

import { Suspense, useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { Check, Mail } from "lucide-react";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import { useAuth } from "@/components/auth/AuthProvider";
import { useToast } from "@/components/ui/Toast";
import { claimStaffInvite, fetchGrantedStaffRole, signUpWithInvite } from "@/services/staff-invites";

const inputCls =
  "w-full rounded-xl border border-white/10 bg-white/5 px-4 py-2.5 text-white placeholder:text-slate-500 focus:border-primary focus:outline-none";

function errorMessage(error: unknown, fallback: string) {
  if (error instanceof Error) return error.message;
  return fallback;
}

function roleLabel(role: string, tier: string | null) {
  return role === "instructor" ? "Giảng viên" : `Trợ giảng${tier ? ` bậc ${tier}` : ""}`;
}

function Card({ children }: { children: React.ReactNode }) {
  return <div className="mx-auto max-w-md rounded-3xl border border-white/10 bg-[#0B1020] p-8">{children}</div>;
}

function InviteContent() {
  const searchParams = useSearchParams();
  const code = (searchParams.get("ma") ?? "").trim();
  const { session, realProfile, loading } = useAuth();
  const toast = useToast();

  const [busy, setBusy] = useState(false);
  const [done, setDone] = useState<string | null>(null);
  const [failed, setFailed] = useState<string | null>(null);
  const [needConfirm, setNeedConfirm] = useState(false);

  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  if (!code)
    return (
      <Card>
        <h1 className="font-display text-xl font-bold text-white">Thiếu mã mời</h1>
        <p className="mt-2 text-sm text-slate-400">
          Mở đúng đường dẫn thầy cô gửi cho bạn, dạng <code className="text-slate-300">/loi-moi?ma=ABC12345</code>.
        </p>
      </Card>
    );

  if (done)
    return (
      <Card>
        <Check className="mx-auto text-emerald-300" size={40} />
        <h1 className="mt-4 text-center font-display text-xl font-bold text-white">Đã nhận lời mời</h1>
        <p className="mt-2 text-center text-sm text-slate-400">{done}</p>
        <Link
          href="/tai-khoan"
          className="mt-6 flex items-center justify-center rounded-xl bg-[#2563EB] py-3 text-sm font-bold text-white"
        >
          Vào tài khoản
        </Link>
      </Card>
    );

  if (failed)
    return (
      <Card>
        <Mail className="mx-auto text-amber-300" size={40} />
        <h1 className="mt-4 text-center font-display text-xl font-bold text-white">Chưa nhận được lời mời</h1>
        <p className="mt-2 text-center text-sm text-slate-400">{failed}</p>
        <Link
          href="/dang-nhap"
          className="mt-6 flex items-center justify-center rounded-xl bg-[#2563EB] py-3 text-sm font-bold text-white"
        >
          Đăng nhập
        </Link>
      </Card>
    );

  if (needConfirm)
    return (
      <Card>
        <Mail className="mx-auto text-sky-300" size={40} />
        <h1 className="mt-4 text-center font-display text-xl font-bold text-white">Kiểm tra email</h1>
        <p className="mt-2 text-center text-sm text-slate-400">
          Tài khoản đã được tạo. Mở email <strong className="text-slate-200">{email}</strong> và bấm link xác nhận,
          sau đó đăng nhập là đã có sẵn quyền được cấp.
        </p>
      </Card>
    );

  async function claim() {
    setBusy(true);
    try {
      const result = await claimStaffInvite(code);
      setDone(
        `Bạn được cấp quyền ${roleLabel(result.role, result.tier)}${result.class_name ? ` · lớp ${result.class_name}` : ""}.`,
      );
    } catch (error) {
      toast("error", errorMessage(error, "Không nhận được lời mời."));
    } finally {
      setBusy(false);
    }
  }

  async function register(e: React.FormEvent) {
    e.preventDefault();
    if (!fullName.trim() || !email.trim() || password.length < 6) {
      toast("error", "Nhập họ tên, email và mật khẩu từ 6 ký tự trở lên.");
      return;
    }
    setBusy(true);
    try {
      const { needsEmailConfirm, userId } = await signUpWithInvite({ email, password, fullName, code });
      // Dự án đang tắt xác nhận email: không có thư nào được gửi, tài khoản dùng được ngay.
      // Chỉ hiện màn "kiểm tra email" khi Supabase thật sự bắt xác nhận (không trả session).
      if (needsEmailConfirm) {
        setNeedConfirm(true);
        return;
      }
      const granted = userId ? await fetchGrantedStaffRole(userId) : null;
      if (granted) {
        setDone(`Tài khoản đã tạo xong và bạn được cấp quyền ${roleLabel(granted.role, granted.tier)}.`);
      } else {
        setFailed(
          "Tài khoản đã được tạo nhưng mã mời không còn hiệu lực, nên chưa có quyền nào được cấp. " +
            "Nhắn thầy cô gửi mã mới, đăng nhập rồi mở lại link mời để nhận quyền.",
        );
      }
    } catch (error) {
      toast("error", errorMessage(error, "Không tạo được tài khoản."));
    } finally {
      setBusy(false);
    }
  }

  if (loading) return <Card><p className="text-center text-slate-400">Đang tải…</p></Card>;

  // Thầy/cô chủ trang bấm nhầm link mời thì nhận lời mời sẽ tự hạ quyền chính mình
  // (xem chặn ở apply_staff_invite). Nói rõ trước, đừng để chạm vào nút.
  if (session && realProfile?.role === "admin")
    return (
      <Card>
        <h1 className="font-display text-xl font-bold text-white">Không cần nhận lời mời</h1>
        <p className="mt-2 text-sm text-slate-400">
          <strong className="text-slate-200">{session.user.email}</strong> là tài khoản quản trị, đã có sẵn mọi quyền.
          Mã <strong className="font-mono text-slate-200">{code.toUpperCase()}</strong> vẫn còn nguyên — gửi link này
          cho đúng người được mời.
        </p>
        <Link
          href="/quan-tri/phan-cong-giang-vien"
          className="mt-6 flex items-center justify-center rounded-xl bg-[#2563EB] py-3 text-sm font-bold text-white"
        >
          Về trang phân công
        </Link>
      </Card>
    );

  if (session)
    return (
      <Card>
        <h1 className="font-display text-xl font-bold text-white">Nhận lời mời</h1>
        <p className="mt-2 text-sm text-slate-400">
          Bạn đang đăng nhập bằng <strong className="text-slate-200">{session.user.email}</strong>. Bấm nút dưới để
          nhận quyền theo mã <strong className="font-mono text-slate-200">{code.toUpperCase()}</strong>.
        </p>
        <button
          type="button"
          disabled={busy}
          onClick={claim}
          className="mt-6 w-full rounded-xl bg-[#2563EB] py-3 text-sm font-bold text-white disabled:opacity-40"
        >
          {busy ? "Đang nhận…" : "Nhận lời mời"}
        </button>
      </Card>
    );

  return (
    <Card>
      <h1 className="font-display text-xl font-bold text-white">Tạo tài khoản</h1>
      <p className="mt-2 text-sm text-slate-400">
        Mã mời <strong className="font-mono text-slate-200">{code.toUpperCase()}</strong> — tạo tài khoản xong là có
        ngay quyền được cấp.
      </p>
      <form onSubmit={register} className="mt-5 space-y-3">
        <input value={fullName} onChange={(e) => setFullName(e.target.value)} placeholder="Họ và tên" className={inputCls} />
        <input value={email} onChange={(e) => setEmail(e.target.value)} type="email" placeholder="Email" className={inputCls} />
        <input
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          type="password"
          placeholder="Mật khẩu (từ 6 ký tự)"
          className={inputCls}
        />
        <button
          type="submit"
          disabled={busy}
          className="w-full rounded-xl bg-[#2563EB] py-3 text-sm font-bold text-white disabled:opacity-40"
        >
          {busy ? "Đang tạo…" : "Tạo tài khoản"}
        </button>
      </form>
      <p className="mt-4 text-center text-xs text-slate-500">
        Đã có tài khoản?{" "}
        <Link href={`/dang-nhap?next=${encodeURIComponent(`/loi-moi?ma=${code}`)}`} className="text-blue-300">
          Đăng nhập rồi quay lại đây
        </Link>
      </p>
    </Card>
  );
}

export default function InvitePage() {
  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-4xl px-5 pt-28 pb-16">
        <Suspense fallback={<Card><p className="text-center text-slate-400">Đang tải…</p></Card>}>
          <InviteContent />
        </Suspense>
      </main>
      <Footer />
    </>
  );
}
