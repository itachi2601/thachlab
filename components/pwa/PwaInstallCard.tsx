"use client";

/**
 * components/pwa/PwaInstallCard.tsx — thẻ gợi ý "Cài ThachLab như một app" ở trang chủ học sinh.
 *
 * Quy tắc: N1/B2 (một nút chính), D2/D3 (nút ≥ 44px), C1/M4 (chữ ≥ 14px). Tự ẩn khi đã cài (standalone),
 * khi trình duyệt không cho cài, hoặc khi em bấm "Để sau" (nhớ 14 ngày). Android/Chrome: beforeinstallprompt
 * (PwaBoot đã bắt sớm); iOS Safari: hướng dẫn tay từng bước, mỗi bước một dòng.
 */

import { useEffect, useState } from "react";
import { Smartphone, X } from "lucide-react";

const SNOOZE_KEY = "thachlab-pwa-card-snooze";
const SNOOZE_MS = 14 * 24 * 60 * 60 * 1000;

interface InstallPromptEvent extends Event {
  prompt: () => Promise<void>;
  userChoice: Promise<{ outcome: "accepted" | "dismissed" }>;
}

type Win = Window & { __thachlabInstallPrompt?: InstallPromptEvent };

function snoozed() {
  try {
    const t = Number(localStorage.getItem(SNOOZE_KEY));
    return t > 0 && Date.now() - t < SNOOZE_MS;
  } catch {
    return false;
  }
}

function standalone() {
  return (
    window.matchMedia("(display-mode: standalone)").matches ||
    (navigator as Navigator & { standalone?: boolean }).standalone === true
  );
}

export default function PwaInstallCard() {
  const [mode, setMode] = useState<"hidden" | "prompt" | "ios">("hidden");
  const [showSteps, setShowSteps] = useState(false);

  useEffect(() => {
    if (standalone() || snoozed()) return;
    const w = window as Win;
    const ios = /iphone|ipad|ipod/i.test(navigator.userAgent);
    const sync = () => {
      if (w.__thachlabInstallPrompt) setMode("prompt");
      else if (ios) setMode("ios");
    };
    sync();
    // Sự kiện có thể đến sau lần render đầu.
    const onPrompt = () => window.setTimeout(sync, 0);
    const onInstalled = () => setMode("hidden");
    window.addEventListener("beforeinstallprompt", onPrompt);
    window.addEventListener("appinstalled", onInstalled);
    return () => {
      window.removeEventListener("beforeinstallprompt", onPrompt);
      window.removeEventListener("appinstalled", onInstalled);
    };
  }, []);

  if (mode === "hidden") return null;

  const later = () => {
    try {
      localStorage.setItem(SNOOZE_KEY, String(Date.now()));
    } catch {
      // bỏ qua
    }
    setMode("hidden");
  };

  const install = async () => {
    if (mode === "ios") {
      setShowSteps((v) => !v);
      return;
    }
    const w = window as Win;
    const p = w.__thachlabInstallPrompt;
    if (p) {
      await p.prompt().catch(() => {});
      w.__thachlabInstallPrompt = undefined;
    }
    setMode("hidden");
  };

  return (
    <section
      aria-label="Cài ThachLab lên điện thoại"
      className="relative rounded-2xl border border-cyan-300/20 bg-cyan-400/[0.06] p-4"
    >
      <button
        type="button"
        onClick={later}
        aria-label="Để sau"
        className="absolute right-1 top-1 inline-flex h-11 w-11 items-center justify-center rounded-full text-slate-400 hover:text-white"
      >
        <X size={18} />
      </button>
      <div className="flex items-start gap-3 pr-9">
        <span className="mt-0.5 inline-flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-cyan-400/15 text-cyan-200">
          <Smartphone size={20} />
        </span>
        <div className="min-w-0">
          <h2 className="text-base font-bold text-white">Cài ThachLab lên màn hình chính</h2>
          <p className="mt-1 text-sm leading-relaxed text-slate-300">Mở bài luyện chỉ với một lần chạm, như một app.</p>
        </div>
      </div>
      {mode === "ios" && showSteps && (
        <ol className="mt-3 space-y-1.5 pl-1 text-sm leading-relaxed text-slate-200">
          <li>1. Mở trang này bằng Safari.</li>
          <li>2. Bấm nút Chia sẻ (ô vuông có mũi tên lên).</li>
          <li>3. Chọn “Thêm vào Màn hình chính”.</li>
        </ol>
      )}
      <div className="mt-3 flex gap-2">
        <button
          type="button"
          onClick={install}
          className="min-h-11 flex-1 rounded-xl bg-blue-600 px-4 text-base font-semibold text-white"
        >
          {mode === "ios" ? (showSteps ? "Ẩn hướng dẫn" : "Xem cách cài") : "Cài ngay"}
        </button>
        <a
          href="/cai-app/"
          className="inline-flex min-h-11 items-center justify-center rounded-xl border border-white/15 px-4 text-sm text-slate-200"
        >
          Hướng dẫn
        </a>
      </div>
    </section>
  );
}
