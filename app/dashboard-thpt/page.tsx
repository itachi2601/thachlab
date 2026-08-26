"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import RequireAuth from "@/components/auth/RequireAuth";
import { useAuth } from "@/components/auth/AuthProvider";
import TeacherThptDashboard from "@/components/dashboard/TeacherThptDashboard";

function DashboardThptRouter() {
  const router = useRouter();
  const { profile, loading } = useAuth();
  const isAdmin = profile?.role === "admin";
  const isThptInstructor = profile?.role === "instructor" && profile.admin_area === "thpt";
  const isCttcInstructor = profile?.role === "instructor" && profile.admin_area === "cttc";

  useEffect(() => {
    if (loading) return;
    if (isCttcInstructor) { router.replace("/dashboard"); return; }
    if (!isAdmin && !isThptInstructor) router.replace("/tai-khoan");
  }, [loading, isAdmin, isThptInstructor, isCttcInstructor, router]);

  if (loading || (!isAdmin && !isThptInstructor)) {
    return <p className="text-slate-400">Đang mở dashboard giáo viên THPT…</p>;
  }
  return <TeacherThptDashboard />;
}

export default function DashboardThptPage() {
  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-6xl px-6 pb-20 pt-28 lg:px-8">
        <RequireAuth>
          <DashboardThptRouter />
        </RequireAuth>
      </main>
      <Footer />
    </>
  );
}
