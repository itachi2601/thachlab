"use client";

/**
 * components/pwa/InstallGuide.tsx — hướng dẫn cài ThachLab thành app, tự nhận máy (trang /cai-app).
 * Android/Chrome: nút Cài đặt (beforeinstallprompt do PwaBoot bắt sớm). iPhone/iPad: 3 bước tay (Safari
 * không có API). Máy tính: nút cài nếu trình duyệt cho, không thì hướng dẫn thanh địa chỉ.
 * Quy tắc: M4/C1 chữ ≥ 14px, D2/D3 nút ≥ 44px, mỗi ý một dòng, một nút chính.
 */

import { useEffect, useState } from "react";

type Platform = "ios" | "android" | "desktop";

interface InstallPromptEvent extends Event {
  prompt: () => Promise<void>;
  userChoice: Promise<{ outcome: "accepted" | "dismissed" }>;
}

const STEPS: Record<Platform, string[]> = {
  ios: [
    "Mở trang này bằng Safari (không dùng Zalo hay Facebook mở sẵn).",
    "Bấm nút Chia sẻ: ô vuông có mũi tên hướng lên, ở thanh dưới.",
    "Kéo xuống, chọn “Thêm vào Màn hình chính”, rồi bấm Thêm.",
  ],
  android: [
    "Mở trang này bằng Chrome.",
    "Bấm nút Cài đặt ở trên (hoặc menu ⋮ → “Cài đặt ứng dụng”).",
    "Bấm Cài đặt. Biểu tượng ThachLab sẽ xuất hiện ở màn hình chính.",
  ],
  desktop: [
    "Dùng Chrome hoặc Edge.",
    "Bấm biểu tượng cài đặt ở bên phải thanh địa chỉ (hoặc nút Cài đặt ở trên).",
    "Bấm Cài đặt. ThachLab mở thành cửa sổ riêng.",
  ],
};

const TITLE: Record<Platform, string> = {
  ios: "iPhone / iPad",
  android: "Điện thoại Android",
  desktop: "Máy tính",
};

function detect(): Platform {
  const ua = navigator.userAgent;
  if (/iphone|ipad|ipod/i.test(ua) || (/macintosh/i.test(ua) && navigator.maxTouchPoints > 1)) return "ios";
  if (/android/i.test(ua)) return "android";
  return "desktop";
}

function getPrompt() {
  return (window as unknown as { __thachlabInstallPrompt?: InstallPromptEvent }).__thachlabInstallPrompt ?? null;
}

export default function InstallGuide() {
  const [platform, setPlatform] = useState<Platform>("android");
  const [canPrompt, setCanPrompt] = useState(false);
  const [installed, setInstalled] = useState(false);

  useEffect(() => {
    setPlatform(detect());
    setInstalled(
      window.matchMedia("(display-mode: standalone)").matches ||
        (navigator as Navigator & { standalone?: boolean }).standalone === true,
    );
    setCanPrompt(!!getPrompt());
    // PwaBoot bắt sự kiện sớm; nghe thêm phòng trường hợp sự kiện đến sau khi trang này mở.
    const onPrompt = () => window.setTimeout(() => setCanPrompt(!!getPrompt()), 0);
    window.addEventListener("beforeinstallprompt", onPrompt);
    return () => window.removeEventListener("beforeinstallprompt", onPrompt);
  }, []);

  const install = async () => {
    const p = getPrompt();
    if (!p) return;
    await p.prompt().catch(() => {});
    (window as unknown as { __thachlabInstallPrompt?: unknown }).__thachlabInstallPrompt = undefined;
    setCanPrompt(false);
  };

  if (installed)
    return (
      <p className="rounded-2xl border border-emerald-400/30 bg-emerald-400/10 p-4 text-base text-emerald-200">
        ThachLab đã được cài trên máy này. Mở từ biểu tượng ở màn hình chính.
      </p>
    );

  const others = (Object.keys(STEPS) as Platform[]).filter((p) => p !== platform);

  return (
    <div className="space-y-6">
      <section className="rounded-3xl border border-white/10 bg-panel p-6">
        <h2 className="font-display text-xl font-bold text-white">{TITLE[platform]}</h2>
        {canPrompt && (
          <button
            type="button"
            onClick={install}
            className="mt-4 min-h-12 w-full rounded-xl bg-blue-600 px-4 text-base font-semibold text-white"
          >
            Cài đặt ThachLab
          </button>
        )}
        <ol className="mt-4 space-y-3 text-base leading-relaxed text-slate-200">
          {STEPS[platform].map((s, i) => (
            <li key={s} className="flex gap-3">
              <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-white/10 text-sm font-bold text-white">
                {i + 1}
              </span>
              <span>{s}</span>
            </li>
          ))}
        </ol>
      </section>

      {others.map((p) => (
        <details key={p} className="rounded-2xl border border-white/10 bg-white/[0.03] p-4">
          <summary className="min-h-11 cursor-pointer py-2 text-base font-semibold text-slate-200">
            Hướng dẫn cho {TITLE[p].toLowerCase()}
          </summary>
          <ol className="mt-2 list-decimal space-y-2 pl-6 text-base leading-relaxed text-slate-300">
            {STEPS[p].map((s) => (
              <li key={s}>{s}</li>
            ))}
          </ol>
        </details>
      ))}
    </div>
  );
}
