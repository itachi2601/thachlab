"use client";

/**
 * components/pwa/PwaBoot.tsx — gắn 1 lần ở app/layout.tsx.
 * Đăng ký service worker (chỉ production) và nạp banner cài đặt theo kiểu lazy (ssr:false +
 * LazyErrorBoundary) để không thêm JS vào lần tải đầu. Không có round-trip Supabase.
 */

import dynamic from "next/dynamic";
import { useEffect } from "react";
import { LazyErrorBoundary } from "@/components/ui/LazyErrorBoundary";

const PwaInstallBanner = dynamic(() => import("./PwaInstallBanner"), { ssr: false });
const OfflineSync = dynamic(() => import("./OfflineSync"), { ssr: false });

export default function PwaBoot() {
  useEffect(() => {
    // Bắt sớm beforeinstallprompt (banner nạp lazy nên có thể chậm hơn sự kiện này).
    const onPrompt = (e: Event) => {
      e.preventDefault();
      (window as unknown as { __thachlabInstallPrompt?: Event }).__thachlabInstallPrompt = e;
    };
    window.addEventListener("beforeinstallprompt", onPrompt);
    return () => window.removeEventListener("beforeinstallprompt", onPrompt);
  }, []);

  useEffect(() => {
    if (process.env.NODE_ENV !== "production") return;
    if (!("serviceWorker" in navigator)) return;
    const register = () => navigator.serviceWorker.register("/sw.js", { scope: "/" }).catch(() => {});
    // Đăng ký sau khi trang tải xong để không tranh băng thông với nội dung.
    if (document.readyState === "complete") register();
    else window.addEventListener("load", register, { once: true });
  }, []);

  return (
    <LazyErrorBoundary>
      <PwaInstallBanner />
      <OfflineSync />
    </LazyErrorBoundary>
  );
}
