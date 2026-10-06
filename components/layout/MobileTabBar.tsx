"use client";

/**
 * components/layout/MobileTabBar.tsx
 *
 * Thanh đáy kiểu app cho điện thoại/tablet: Trang chủ · Lớp học · Luyện tập · Tài khoản.
 * Chỉ hiện dưới 1024px (đúng breakpoint mà thanh điều hướng ngang của Navbar biến mất).
 *
 * Ba chỗ CỐ TÌNH ẩn thanh này:
 *  - /quan-tri/**            — khu quản trị có bảng rộng, thanh đáy che mất dòng cuối.
 *  - /kiem-tra/lam           — đang làm bài, không cho điều hướng đi nơi khác.
 *  - /lop-hoc/bai            — trang bài học đã có thanh đáy riêng (3 nút), hai thanh chồng nhau.
 *  - /tro-giang/ghi          — form ghi buổi/chấm công có thanh "Lưu buổi" dán đáy (cùng z-40);
 *                              thanh này render sau nên đè lên nút Lưu, trợ giảng không nộp được.
 *
 * Thuần CSS + usePathname, không thêm request, không thêm thư viện icon (SVG inline).
 */

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useSyncExternalStore } from "react";
import { useAuth } from "@/components/auth/auth-context";

// /phu-huynh: thanh này là của học sinh (Lớp học, Luyện tập) — phụ huynh bấm vào sẽ lạc sang trang không dành cho họ.
const HIDDEN_PREFIXES = ["/quan-tri", "/kiem-tra/lam", "/lop-hoc/bai", "/tro-giang/ghi", "/phu-huynh"];

/** Thanh đáy có đang hiện ở đường dẫn này không — Navbar dùng để bỏ mục trùng khỏi menu ☰. */
export function tabBarShownOn(pathname: string) {
  return !HIDDEN_PREFIXES.some((prefix) => pathname.startsWith(prefix));
}

const MOBILE_QUERY = "(max-width: 1023px)";

function subscribeViewport(onChange: () => void) {
  const mql = window.matchMedia(MOBILE_QUERY);
  mql.addEventListener("change", onChange);
  return () => mql.removeEventListener("change", onChange);
}

function isMobileViewport() {
  return window.matchMedia(MOBILE_QUERY).matches;
}

/** Icon SVG inline, nét 1.7 — đồng bộ với bộ icon lucide đang dùng ở Navbar. */
function TabIcon({ name }: { name: "home" | "class" | "practice" | "account" }) {
  const common = {
    width: 22,
    height: 22,
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: 1.7,
    strokeLinecap: "round" as const,
    strokeLinejoin: "round" as const,
    "aria-hidden": true,
  };
  if (name === "home")
    return (
      <svg {...common}>
        <path d="M3 10.5 12 3l9 7.5" />
        <path d="M5 9.5V21h14V9.5" />
      </svg>
    );
  if (name === "class")
    return (
      <svg {...common}>
        <path d="M3 5.5h6a3 3 0 0 1 3 3V20a2.5 2.5 0 0 0-2.5-2.5H3z" />
        <path d="M21 5.5h-6a3 3 0 0 0-3 3V20a2.5 2.5 0 0 1 2.5-2.5H21z" />
      </svg>
    );
  if (name === "practice")
    return (
      <svg {...common}>
        <path d="M4 6h9" />
        <path d="M4 12h6" />
        <path d="M4 18h5" />
        <path d="m15 15 2.5 2.5L21 13" />
      </svg>
    );
  return (
    <svg {...common}>
      <circle cx="12" cy="8.5" r="3.7" />
      <path d="M4.8 20a7.2 7.2 0 0 1 14.4 0" />
    </svg>
  );
}

export default function MobileTabBar() {
  const pathname = usePathname();
  const { session } = useAuth();
  const isMobile = useSyncExternalStore(subscribeViewport, isMobileViewport, () => false);

  if (!isMobile) return null;
  if (!tabBarShownOn(pathname)) return null;

  const items = [
    { key: "home", label: "Trang chủ", href: "/", icon: "home" as const },
    { key: "class", label: "Lớp học", href: "/lop-hoc", icon: "class" as const },
    { key: "practice", label: "Luyện tập", href: "/luyen-tap", icon: "practice" as const },
    {
      key: "account",
      label: "Tài khoản",
      href: session ? "/tai-khoan" : "/dang-nhap",
      icon: "account" as const,
    },
  ];

  return (
    <nav className="mobile-tabbar" aria-label="Điều hướng nhanh">
      {items.map((item) => {
        const active =
          item.href === "/"
            ? pathname === "/"
            : pathname === item.href || pathname.startsWith(`${item.href}/`);
        return (
          <Link
            key={item.key}
            href={item.href}
            aria-current={active ? "page" : undefined}
            className={active ? "is-active" : undefined}
          >
            <TabIcon name={item.icon} />
            <span>{item.label}</span>
          </Link>
        );
      })}
    </nav>
  );
}
