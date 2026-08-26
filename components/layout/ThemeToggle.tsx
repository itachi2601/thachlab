"use client";

import { Moon, Sun } from "lucide-react";
import { useSyncExternalStore } from "react";

type Theme = "dark" | "light";

function getTheme(): Theme {
  return document.documentElement.dataset.theme === "light" ? "light" : "dark";
}

function subscribe(onChange: () => void) {
  window.addEventListener("thachlab-theme-change", onChange);
  return () => window.removeEventListener("thachlab-theme-change", onChange);
}

export default function ThemeToggle() {
  const theme = useSyncExternalStore(subscribe, getTheme, () => "dark");

  function toggleTheme() {
    const nextTheme: Theme = getTheme() === "dark" ? "light" : "dark";
    document.documentElement.dataset.theme = nextTheme;
    document.documentElement.style.colorScheme = nextTheme;
    localStorage.setItem("thachlab-theme", nextTheme);
    window.dispatchEvent(new Event("thachlab-theme-change"));
  }

  const nextThemeLabel = theme === "dark" ? "giao diện sáng" : "giao diện tối";

  return (
    <button
      type="button"
      onClick={toggleTheme}
      aria-label={`Chuyển sang ${nextThemeLabel}`}
      title={`Chuyển sang ${nextThemeLabel}`}
      className="theme-toggle inline-flex h-11 w-11 shrink-0 items-center justify-center rounded-xl border border-white/10 bg-white/[0.06] text-slate-200 transition-colors hover:bg-white/10 hover:text-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3B82F6]"
    >
      {theme === "dark" ? <Sun size={20} /> : <Moon size={20} />}
    </button>
  );
}
