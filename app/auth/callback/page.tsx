"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import { getSupabase, supabaseConfigured } from "@/services/supabase";

export default function AuthCallbackPage() {
  const router = useRouter();
  const [message, setMessage] = useState("Đang hoàn tất đăng nhập...");

  useEffect(() => {
    async function completeLogin() {
      if (!supabaseConfigured) {
        setMessage("Hệ thống đăng nhập chưa được cấu hình.");
        return;
      }

      const params = new URLSearchParams(window.location.search);
      const code = params.get("code");
      const userType = params.get("type") || "student";

      if (!code) {
        router.replace("/dang-nhap");
        return;
      }

      const { error } = await getSupabase().auth.exchangeCodeForSession(code);
      if (error) {
        router.replace(`/dang-nhap?error=${encodeURIComponent(error.message)}`);
        return;
      }

      router.replace(userType === "teacher" ? "/quan-tri" : "/tai-khoan");
    }

    completeLogin().catch(() => {
      setMessage("Không thể hoàn tất đăng nhập. Vui lòng thử lại.");
    });
  }, [router]);

  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-md px-6 pt-32 pb-20">
        <h1 className="font-display text-3xl font-bold text-white">
          Đăng <span className="text-gradient">nhập</span>
        </h1>
        <p className="mt-4 text-slate-400">{message}</p>
      </main>
      <Footer />
    </>
  );
}
