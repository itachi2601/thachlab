"use client";

import Link from "next/link";
import { ChevronLeft } from "lucide-react";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import RequireAuth from "@/components/auth/RequireAuth";
import { useAuth } from "@/components/auth/AuthProvider";
import RankPage from "@/components/rank/RankPage";
import { supabaseConfigured } from "@/services/supabase";

function Content() {
  const { session, profile } = useAuth();
  if (!session) return null;
  return (
    <div className="mx-auto w-full max-w-4xl px-4 pb-20 pt-28 sm:px-6">
      <Link href="/tai-khoan/" className="mb-5 inline-flex items-center gap-1.5 text-sm text-slate-400 hover:text-white">
        <ChevronLeft size={16} /> Về trang của em
      </Link>
      <RankPage studentId={session.user.id} studentName={profile?.full_name ?? "Học sinh"} />
    </div>
  );
}

export default function XepHangPage() {
  return (
    <>
      <Navbar />
      <main className="min-h-screen w-full">
        {!supabaseConfigured ? (
          <p className="pt-28 text-center text-slate-400">Hệ thống đang được cấu hình.</p>
        ) : (
          <RequireAuth>
            <Content />
          </RequireAuth>
        )}
      </main>
      <Footer />
    </>
  );
}
