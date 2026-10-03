"use client";

import { useEffect, useRef, useState, type ReactNode } from "react";
import { Eye } from "lucide-react";

/**
 * Công cụ đọc dùng chung cho trang KHÔNG phải bài học (/phu-huynh, /kiem-tra/lam):
 * Dịu mắt · A− / A+. Cùng khoá localStorage với trang bài học (app/lop-hoc/bai/page.tsx)
 * để phụ huynh/học sinh chỉnh một lần là dùng ở mọi nơi.
 *
 * Khác trang bài học (chỉ phóng khối nội dung HTML, đơn vị em): ở đây chữ là Tailwind
 * (rem) nên phóng bằng font-size của <html> — mọi text-sm/text-base đều to theo, chữ nhãn
 * đặt bằng px (sàn 12px) giữ nguyên. Dịu mắt = bật theme sáng + lớp html.is-dim phủ tông
 * kem/nâu (CSS ở khối "P1/P2 kha-nang-doc" cuối app/globals.css). Rời trang là trả lại.
 */
const FONT_SCALES = [0.94, 1, 1.08];
const FONT_STORE = "thachlab-read-font";
const DIM_STORE = "thachlab-read-dim";
const THEME_STORE = "thachlab-theme";
const THEME_EVENT = "thachlab-theme-change";

type Theme = "light" | "dark";

/** Theme khi KHÔNG bật dịu mắt — cùng logic với script inline ở app/layout.tsx. */
function defaultTheme(): Theme {
  try {
    const saved = window.localStorage.getItem(THEME_STORE);
    if (saved === "light" || saved === "dark") return saved;
  } catch {}
  const p = window.location.pathname;
  if (p === "/phu-huynh" || p.startsWith("/phu-huynh/")) return "light";
  return window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark";
}

function applyTheme(theme: Theme) {
  document.documentElement.dataset.theme = theme;
  document.documentElement.style.colorScheme = theme;
  window.dispatchEvent(new Event(THEME_EVENT));
}

/**
 * plainLabels: nút cỡ chữ ghi thành lời ("Chữ nhỏ lại" / "Chữ to hơn") thay vì "A− / A+" — nhiều phụ huynh
 * 45–60 không nhận ra ký hiệu A−/A+. Chỉ trang phụ huynh bật; trang học sinh giữ bản gọn.
 */
export default function ReadingZone({
  children,
  className,
  plainLabels = false,
}: {
  children: ReactNode;
  className?: string;
  plainLabels?: boolean;
}) {
  const [fontLevel, setFontLevel] = useState(1);
  const [dim, setDim] = useState(false);
  const restored = useRef(false);

  /* eslint-disable react-hooks/set-state-in-effect -- đọc localStorage đúng 1 lần sau khi
     hydrate: không đọc được lúc SSR, và đã so sánh trước khi set nên không sinh vòng render thừa. */
  useEffect(() => {
    try {
      const raw = window.localStorage.getItem(FONT_STORE);
      const saved = raw === null ? null : Number(raw);
      if (saved !== null && Number.isInteger(saved) && saved >= 0 && saved < FONT_SCALES.length && saved !== fontLevel) {
        setFontLevel(saved);
      }
      if (window.localStorage.getItem(DIM_STORE) === "1") setDim(true);
    } catch {}
    restored.current = true;
    // eslint-disable-next-line react-hooks/exhaustive-deps -- chỉ khôi phục 1 lần khi mount
  }, []);
  /* eslint-enable react-hooks/set-state-in-effect */

  // Cỡ chữ: đặt lên <html> (rem) — rời trang thì xoá.
  useEffect(() => {
    const scale = FONT_SCALES[fontLevel];
    document.documentElement.style.fontSize = scale === 1 ? "" : `${scale * 100}%`;
    if (restored.current) {
      try {
        window.localStorage.setItem(FONT_STORE, String(fontLevel));
      } catch {}
    }
    return () => {
      document.documentElement.style.fontSize = "";
    };
  }, [fontLevel]);

  // Dịu mắt: theme sáng + html.is-dim; không ghi đè lựa chọn theme đã lưu. Tắt/rời trang → trả theme.
  useEffect(() => {
    const html = document.documentElement;
    if (dim) {
      html.classList.add("is-dim");
      if (html.dataset.theme !== "light") applyTheme("light");
    } else {
      html.classList.remove("is-dim");
      const want = defaultTheme();
      if (html.dataset.theme !== want) applyTheme(want);
    }
    if (restored.current) {
      try {
        if (dim) window.localStorage.setItem(DIM_STORE, "1");
        else window.localStorage.removeItem(DIM_STORE);
      } catch {}
    }
    return () => {
      html.classList.remove("is-dim");
    };
  }, [dim]);

  // Đang dịu mắt mà bấm nút Trăng/Mặt trời sang tối → coi như tắt dịu mắt.
  useEffect(() => {
    if (!dim) return;
    const onTheme = () => {
      if (document.documentElement.dataset.theme !== "light") setDim(false);
    };
    window.addEventListener(THEME_EVENT, onTheme);
    return () => window.removeEventListener(THEME_EVENT, onTheme);
  }, [dim]);

  return (
    <div className={className}>
      <div className="read-zone-tools" role="group" aria-label="Công cụ đọc">
        <button
          type="button"
          className={`lesson-tool ${dim ? "is-on" : ""}`}
          onClick={() => setDim((d) => !d)}
          aria-pressed={dim}
          title="Nền dịu mắt, chữ đậm hơn — đọc lâu đỡ mỏi"
        >
          <Eye size={14} aria-hidden />
          <span>Dịu mắt</span>
        </button>
        <div className="lesson-fonttools">
          <button
            type="button"
            onClick={() => setFontLevel((v) => Math.max(0, v - 1))}
            disabled={fontLevel === 0}
            aria-label="Cỡ chữ nhỏ hơn"
            style={plainLabels ? { padding: "0 14px" } : undefined}
          >
            {plainLabels ? "Chữ nhỏ lại" : "A−"}
          </button>
          <button
            type="button"
            onClick={() => setFontLevel((v) => Math.min(FONT_SCALES.length - 1, v + 1))}
            disabled={fontLevel === FONT_SCALES.length - 1}
            aria-label="Cỡ chữ lớn hơn"
            style={plainLabels ? { padding: "0 14px" } : undefined}
          >
            {plainLabels ? "Chữ to hơn" : "A+"}
          </button>
        </div>
      </div>
      {children}
    </div>
  );
}
