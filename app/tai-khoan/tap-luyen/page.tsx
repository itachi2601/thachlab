"use client";
import dynamic from "next/dynamic";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import Navbar from "@/components/layout/Navbar";
import RequireAuth from "@/components/auth/RequireAuth";
import { LazyErrorBoundary } from "@/components/ui/LazyErrorBoundary";

// Ứng dụng tập gym cá nhân kiểu Hevy (chương trình A/B/C ở lib/tap-luyen/chuong-trinh.ts).
const TapLuyenApp = dynamic(() => import("@/components/tap-luyen/TapLuyenApp"), { ssr: false });

export default function TapLuyenPage() {
  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-xl px-4 pt-24 pb-16">
        <RequireAuth>
          <div className="mb-3 flex items-center gap-2">
            <Link href="/tai-khoan" aria-label="Về tài khoản" className="grid h-11 w-11 place-items-center rounded-xl text-muted hover:bg-surface-2">
              <ArrowLeft size={20} />
            </Link>
            <h1 className="font-display text-xl font-bold text-ink">Tập luyện</h1>
          </div>
          <LazyErrorBoundary>
            <TapLuyenApp />
          </LazyErrorBoundary>
        </RequireAuth>
      </main>
    </>
  );
}
