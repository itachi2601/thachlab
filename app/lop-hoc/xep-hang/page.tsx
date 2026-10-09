"use client";

import { useEffect, useState } from "react";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import RequireAuth from "@/components/auth/RequireAuth";
import { useAuth } from "@/components/auth/AuthProvider";
import RankPage from "@/components/rank/RankPage";
import { supabaseConfigured } from "@/services/supabase";
import { fetchMyClassRequest } from "@/services/classes";

function Content() {
  const { session, profile } = useAuth();
  const userId = session?.user.id ?? null;
  // Lớp đang học (status active) → RankPage hiện "Bảng tuần của lớp"; không có lớp thì bỏ qua khối đó.
  const [classId, setClassId] = useState<number | null>(null);
  useEffect(() => {
    if (!userId) return;
    fetchMyClassRequest(userId)
      .then((r) => setClassId(r?.status === "active" ? r.classId : null))
      .catch(() => setClassId(null));
  }, [userId]);
  if (!session) return null;
  return (
    <div className="mx-auto w-full max-w-4xl px-4 pb-20 pt-28 sm:px-6">
      <RankPage studentId={session.user.id} studentName={profile?.full_name ?? "Học sinh"} classId={classId} />
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
      <Footer variant="app" />
    </>
  );
}
