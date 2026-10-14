/**
 * components/physics/stage-theme.ts
 *
 * Nguồn sự thật duy nhất về bảng màu cho mọi canvas mô phỏng Vật lí (M1, M3, M6, G2).
 *
 * Canvas 2D không đọc trực tiếp utility Tailwind hay CSS variables từ stylesheet,
 * nên file này cầu nối giữa hệ thống token của site (app/globals.css) và ngữ cảnh
 * vẽ 2D (CanvasRenderingContext2D / ImageData).
 *
 * Mặc định: nền sáng (đọc từ getComputedStyle).
 * Tuỳ chọn: nền tối (khi html[data-theme="dark"], giữ nguyên màu cũ).
 */

export interface StagePalette {
  bgTop: string;
  bgBottom: string; // nền sân khấu (gradient nhẹ, KHÔNG neon)
  bgRgb: [number, number, number]; // bản RGB của bgBottom cho sim tô pixel
  grid: string;
  gridStrong: string; // lưới mờ / trục
  ink: string;
  muted: string; // chữ số liệu / chữ phụ
  line: string; // viền, thước
  accent: string;
  accentSoft: string; // họ màu chính (quỹ đạo, bóng)
  warm: string; // điểm nhấn ấm (vật thể, mốc)
  primary: string;
  primaryEdge: string; // họ xanh (con lắc, nguồn sóng)
  waveMax: string;
  waveMin: string; // cực đại / cực tiểu giao thoa
}

/** Bảng màu nền tối gốc: giữ nguyên 100% hình ảnh cũ cho người dùng nền tối. */
const DARK_PALETTE: StagePalette = {
  bgTop: "#070C15",
  bgBottom: "#04070C",
  bgRgb: [4, 7, 12],
  grid: "rgba(148, 163, 184, 0.10)",
  gridStrong: "#334155", // SLATE_700
  ink: "#E2E8F0", // TEXT
  muted: "#94A3B8", // SLATE_400
  line: "#475569", // SLATE_600
  accent: "#22D3EE", // ACCENT
  accentSoft: "rgba(34, 211, 238, 0.55)",
  warm: "#FBBF24", // WARM
  primary: "#3B82F6", // PEND_TOP
  primaryEdge: "#60A5FA", // PEND_EDGE
  waveMax: "#E6FEFF", // M_MAX
  waveMin: "#93C5FD", // M_MIN
};

function hexToRgb(hex: string, fallback: [number, number, number] = [238, 241, 246]): [number, number, number] {
  const clean = hex.replace("#", "").trim();
  if (clean.length === 3) {
    return [
      parseInt(clean[0] + clean[0], 16),
      parseInt(clean[1] + clean[1], 16),
      parseInt(clean[2] + clean[2], 16),
    ];
  }
  if (clean.length >= 6) {
    return [
      parseInt(clean.slice(0, 2), 16),
      parseInt(clean.slice(2, 4), 16),
      parseInt(clean.slice(4, 6), 16),
    ];
  }
  return fallback;
}

export function colorToRgb(color: string, fallback: [number, number, number]): [number, number, number] {
  if (color.startsWith("#")) {
    return hexToRgb(color, fallback);
  }
  const match = color.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
  if (match) {
    return [Number(match[1]), Number(match[2]), Number(match[3])];
  }
  return fallback;
}

/** Chuyển mã màu hex/rgb sang chuỗi rgba(...) có độ mờ alpha tuỳ chọn. */
export function withAlpha(color: string, alpha: number): string {
  const [r, g, b] = colorToRgb(color, [14, 116, 144]);
  return `rgba(${r}, ${g}, ${b}, ${Math.max(0, Math.min(1, alpha))})`;
}

/**
 * Đọc bảng màu hiện tại theo data-theme của <html>.
 * Chỉ chạy phía client; phía SSR fallback về nền sáng mặc định.
 */
export function getStagePalette(): StagePalette {
  if (typeof document === "undefined") {
    // SSR fallback: nền sáng mặc định toàn site (từ 11/10/2026)
    return {
      bgTop: "#f8fafc",
      bgBottom: "#eef1f6",
      bgRgb: [238, 241, 246],
      grid: "#7c8ba1",
      gridStrong: "#475569",
      ink: "#0f172a",
      muted: "#475569",
      line: "#8b93a1",
      accent: "#0e7490",
      accentSoft: "rgba(14, 116, 144, 0.35)",
      warm: "#b45309",
      primary: "#1d4ed8",
      primaryEdge: "#1e40af",
      waveMax: "#1d4ed8",
      waveMin: "#eef1f6",
    };
  }

  const isDark = document.documentElement.dataset.theme === "dark";
  if (isDark) {
    return DARK_PALETTE;
  }

  const style = getComputedStyle(document.documentElement);
  const surface2 = style.getPropertyValue("--color-surface-2").trim() || "#eef1f6";
  const ink = style.getPropertyValue("--color-ink").trim() || "#0f172a";
  const muted = style.getPropertyValue("--color-muted").trim() || "#475569";
  const lineStrong = style.getPropertyValue("--color-line-strong").trim() || "#8b93a1";
  const cyan = style.getPropertyValue("--color-cyan").trim() || "#0e7490";
  const accent = style.getPropertyValue("--color-accent").trim() || "#b45309";
  const primary = style.getPropertyValue("--color-primary").trim() || "#1d4ed8";
  const primaryDark = style.getPropertyValue("--color-primary-dark").trim() || "#1e40af";

  const bgRgb = hexToRgb(surface2.startsWith("#") ? surface2 : "#eef1f6", [238, 241, 246]);

  return {
    bgTop: "#f8fafc",
    bgBottom: surface2,
    bgRgb,
    // #7c8ba1 đạt 3,06:1 trên #eef1f6 và 3,32:1 trên #f8fafc (WCAG 1.4.11 ≥ 3:1)
    grid: "#7c8ba1",
    // gridStrong là trục và vạch phân định chính: #475569 (6,69:1)
    gridStrong: muted,
    ink,
    muted,
    line: lineStrong,
    accent: cyan,
    accentSoft: "rgba(14, 116, 144, 0.35)",
    warm: accent,
    primary,
    primaryEdge: primaryDark,
    waveMax: primary,
    waveMin: surface2,
  };
}

/**
 * Lắng nghe thay đổi theme (qua MutationObserver trên data-theme của <html>
 * hoặc sự kiện tuỳ biến thachlab-theme-change).
 * Trả hàm huỷ đăng ký.
 */
export function subscribeStageTheme(cb: () => void): () => void {
  if (typeof document === "undefined") {
    return () => {};
  }

  const observer =
    typeof MutationObserver !== "undefined"
      ? new MutationObserver((mutations) => {
          for (const mutation of mutations) {
            if (mutation.type === "attributes" && mutation.attributeName === "data-theme") {
              cb();
              break;
            }
          }
        })
      : null;

  if (observer) {
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ["data-theme"],
    });
  }

  const onCustomThemeChange = () => cb();
  window.addEventListener("thachlab-theme-change", onCustomThemeChange);

  return () => {
    observer?.disconnect();
    window.removeEventListener("thachlab-theme-change", onCustomThemeChange);
  };
}
