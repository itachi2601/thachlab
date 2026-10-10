"use client";

import { Moon, Sun } from "lucide-react";
import { useSyncExternalStore } from "react";

type Theme = "dark" | "light";

function getTheme(): Theme {
  return document.documentElement.dataset.theme === "light" ? "light" : "dark";
}

/** Nền sáng là mặc định toàn site (app/layout.tsx) nên snapshot lúc SSR cũng phải là "light",
 *  nếu không icon và nhãn sẽ nhảy một nhịp sau khi hydrate. */
const DEFAULT_THEME: Theme = "light";

function subscribe(onChange: () => void) {
  window.addEventListener("thachlab-theme-change", onChange);
  return () => window.removeEventListener("thachlab-theme-change", onChange);
}

/** Thanh trạng thái của trình duyệt/PWA đọc <meta name="theme-color"> — giá trị này không tự
 *  đổi theo data-theme, nên khi người dùng bật nền tối phải cập nhật tay. */
function setMetaThemeColor(theme: Theme) {
  const meta = document.querySelector('meta[name="theme-color"]');
  if (meta) meta.setAttribute("content", theme === "dark" ? "#05070b" : "#f5f7fa");
}

export default function ThemeToggle() {
  const theme = useSyncExternalStore(subscribe, getTheme, () => DEFAULT_THEME);

  function toggleTheme() {
    const nextTheme: Theme = getTheme() === "dark" ? "light" : "dark";
    document.documentElement.dataset.theme = nextTheme;
    document.documentElement.style.colorScheme = nextTheme;
    setMetaThemeColor(nextTheme);
    try {
      localStorage.setItem("thachlab-theme", nextTheme);
    } catch {}
    window.dispatchEvent(new Event("thachlab-theme-change"));
  }

  const nextThemeLabel = theme === "dark" ? "giao diện sáng" : "giao diện tối";

  return (
    <button
      type="button"
      onClick={toggleTheme}
      aria-label={`Chuyển sang ${nextThemeLabel}`}
      title={`Chuyển sang ${nextThemeLabel}`}
      className="theme-toggle inline-flex h-11 w-11 shrink-0 items-center justify-center rounded-xl border border-line bg-surface-2 text-muted transition-colors hover:text-ink focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary"
    >
      {theme === "dark" ? <Sun size={20} /> : <Moon size={20} />}
    </button>
  );
}
