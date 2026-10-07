"use client";

/**
 * components/pwa/PwaInstallBanner.tsx — banner "Thêm vào màn hình chính", hiện ĐÚNG 1 lần.
 *
 * Quy tắc thiết kế: L6/B4 (chỉ hiện sau khi xong bài luyện đầu, không giữa lúc làm bài), N1/B2 (một
 * nút chính), B6 (nằm đè chỗ thanh đáy, không thêm thanh thứ hai), D2/D3 (nút ≥ 44px, vùng ngón cái),
 * M4/C1 (chữ ≥ 14px). Chỉ học sinh thật: không phụ huynh/admin/GV/trợ giảng.
 * Android: beforeinstallprompt. iOS Safari: hướng dẫn tay (không có API).
 */

import { useCallback, useEffect, useRef, useState } from "react";
import { useAuth } from "@/components/auth/auth-context";
import {
  PWA_BANNER_SEEN_KEY,
  PWA_FIRST_PRACTICE_EVENT,
  PWA_FIRST_PRACTICE_KEY,
} from "@/lib/pwa-install";

interface InstallPromptEvent extends Event {
  prompt: () => Promise<void>;
  userChoice: Promise<{ outcome: "accepted" | "dismissed" }>;
}

function readFlag(key: string) {
  try {
    return localStorage.getItem(key) === "1";
  } catch {
    return false;
  }
}

function writeFlag(key: string) {
  try {
    localStorage.setItem(key, "1");
  } catch {
    // bỏ qua
  }
}

function isStandalone() {
  return (
    window.matchMedia("(display-mode: standalone)").matches ||
    (navigator as Navigator & { standalone?: boolean }).standalone === true
  );
}

function isIos() {
  return /iphone|ipad|ipod/i.test(navigator.userAgent);
}

export default function PwaInstallBanner() {
  const { profile } = useAuth();
  const isStudent = profile?.role === "student";
  const [visible, setVisible] = useState(false);
  const [iosMode, setIosMode] = useState(false);
  const triggered = useRef(false);

  // beforeinstallprompt được PwaBoot bắt sớm và để ở window.__thachlabInstallPrompt.
  const getPrompt = () =>
    (window as unknown as { __thachlabInstallPrompt?: InstallPromptEvent }).__thachlabInstallPrompt ?? null;

  const tryShow = useCallback(() => {
    if (triggered.current) return;
    if (readFlag(PWA_BANNER_SEEN_KEY) || isStandalone()) return;
    const ios = isIos();
    if (!ios && !getPrompt()) return; // trình duyệt không cho cài
    triggered.current = true;
    // Chờ 2,5s và không hiện khi còn hộp thoại đang mở (không popup chồng).
    let waited = 0;
    const timer = window.setInterval(() => {
      waited += 500;
      if (waited < 2500) return;
      if (document.querySelector('[role="dialog"],[aria-modal="true"]')) {
        if (waited > 60000) window.clearInterval(timer);
        return;
      }
      window.clearInterval(timer);
      writeFlag(PWA_BANNER_SEEN_KEY);
      setIosMode(ios && !getPrompt());
      setVisible(true);
    }, 500);
  }, []);

  useEffect(() => {
    if (!isStudent) return;
    if (readFlag(PWA_FIRST_PRACTICE_KEY)) tryShow();
    window.addEventListener(PWA_FIRST_PRACTICE_EVENT, tryShow);
    return () => window.removeEventListener(PWA_FIRST_PRACTICE_EVENT, tryShow);
  }, [isStudent, tryShow]);

  if (!visible || !isStudent) return null;

  const install = async () => {
    const p = getPrompt();
    if (p) {
      await p.prompt().catch(() => {});
      (window as unknown as { __thachlabInstallPrompt?: unknown }).__thachlabInstallPrompt = undefined;
    }
    setVisible(false);
  };

  return (
    <div
      role="region"
      aria-label="Thêm ThachLab vào màn hình chính"
      className="fixed inset-x-0 bottom-0 z-50 border-t border-white/10 bg-panel px-4 pt-4 shadow-2xl"
      style={{ paddingBottom: "max(1rem, env(safe-area-inset-bottom))" }}
    >
      <div className="mx-auto max-w-md">
        <p className="text-base font-semibold text-slate-100">Thêm ThachLab vào màn hình chính</p>
        <p className="mt-1 text-sm leading-relaxed text-slate-300">
          {iosMode
            ? "Bấm nút Chia sẻ (ô vuông có mũi tên lên) ở thanh Safari, rồi chọn “Thêm vào Màn hình chính”."
            : "Mở bài luyện chỉ với một lần chạm, như một ứng dụng."}
        </p>
        <a href="/cai-app/" className="mt-1 inline-block min-h-11 py-2 text-sm text-cyan-300 underline">
          Xem hướng dẫn chi tiết
        </a>
        <div className="mt-1 flex gap-2">
          {!iosMode && (
            <button
              type="button"
              onClick={install}
              className="min-h-11 flex-1 rounded-xl bg-blue-600 px-4 text-base font-semibold text-white"
            >
              Thêm
            </button>
          )}
          <button
            type="button"
            onClick={() => setVisible(false)}
            className="min-h-11 flex-1 rounded-xl border border-white/15 px-4 text-base text-slate-200"
          >
            {iosMode ? "Đã hiểu" : "Để sau"}
          </button>
        </div>
      </div>
    </div>
  );
}
