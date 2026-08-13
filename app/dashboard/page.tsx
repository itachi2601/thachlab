"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import RequireAuth from "@/components/auth/RequireAuth";
import { useAuth } from "@/components/auth/AuthProvider";
import TeacherCourseDashboard from "@/components/dashboard/TeacherCourseDashboard";

function DashboardRouter() {
  const router = useRouter();
  const { profile, loading } = useAuth();
  useEffect(() => { if (!loading && profile?.role !== "admin") router.replace("/tai-khoan"); }, [loading, profile?.role, router]);
  if (loading || profile?.role !== "admin") return <p className="text-slate-400">Đang mở tài khoản sinh viên…</p>;
  return <TeacherCourseDashboard/>;
}

export default function DashboardPage() {
  return <><Navbar/><main className="mx-auto min-h-screen w-full max-w-6xl px-6 pb-20 pt-28 lg:px-8"><RequireAuth><DashboardRouter/></RequireAuth></main><Footer/></>;
}
