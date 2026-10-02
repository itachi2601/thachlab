"use client";

import { useState } from "react";
import Link from "next/link";
import { KeyRound } from "lucide-react";
import { useAuth } from "@/components/auth/AuthProvider";
import { useToast } from "@/components/ui/Toast";
import { getSupabase } from "@/services/supabase";

/** Thông tin tài khoản của học sinh: sửa họ tên (RLS chỉ cho role student tự sửa), xem email đăng nhập, đổi mật khẩu. */
export default function ProfileEditCard() {
  const { session, profile, refreshProfile } = useAuth();
  const toast = useToast();
  const [name, setName] = useState(profile?.full_name ?? "");
  const [busy, setBusy] = useState(false);
  if (!session || profile?.role !== "student") return null;

  const trimmed = name.trim();
  const changed = trimmed !== (profile?.full_name ?? "") && trimmed.length >= 2;

  async function save(event: React.FormEvent) {
    event.preventDefault();
    if (!changed || !session) return;
    setBusy(true);
    try {
      const { error } = await getSupabase().from("profiles").update({ full_name: trimmed }).eq("id", session.user.id);
      if (error) throw error;
      await refreshProfile();
      toast("success", "Đã lưu họ tên.");
    } catch {
      toast("error", "Không lưu được, thử lại nhé.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <section className="mt-6 rounded-3xl border border-white/10 bg-panel p-6">
      <h2 className="font-display text-lg font-bold text-white">Thông tin tài khoản</h2>
      <form onSubmit={save} className="mt-4 grid gap-4 sm:grid-cols-2">
        <label className="block text-sm text-slate-300">
          Họ và tên
          <input value={name} onChange={(e) => setName(e.target.value)} maxLength={80} className="mt-1.5 min-h-11 w-full rounded-xl border border-white/10 bg-white/5 px-4 py-2.5 text-white" />
        </label>
        <label className="block text-sm text-slate-300">
          Email đăng nhập
          <input value={session.user.email ?? ""} readOnly className="mt-1.5 min-h-11 w-full rounded-xl border border-white/10 bg-white/[0.03] px-4 py-2.5 text-slate-400" />
          <span className="mt-1 block text-xs text-slate-400">Email gắn với tài khoản, muốn đổi hãy nhắn thầy.</span>
        </label>
        <div className="flex flex-wrap items-center gap-3 sm:col-span-2">
          <button disabled={!changed || busy} className="min-h-11 rounded-xl bg-blue-600 px-5 text-sm font-bold text-white disabled:opacity-50">{busy ? "Đang lưu…" : "Lưu họ tên"}</button>
          <Link href="/tai-khoan/doi-mat-khau" className="inline-flex min-h-11 items-center gap-2 rounded-xl border border-white/10 px-5 text-sm font-bold text-slate-200"><KeyRound size={15} />Đổi mật khẩu</Link>
        </div>
      </form>
    </section>
  );
}
