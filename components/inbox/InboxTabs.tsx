"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/components/auth/auth-context";

const TABS = [
  { href: "/hop-thu", label: "Tất cả" },
  { href: "/thong-bao", label: "Thông báo" },
  { href: "/tin-nhan", label: "Tin nhắn" },
  { href: "/tin-tuc", label: "Tin tức" },
];

/**
 * Hộp thư: một cửa vào từ chuông, ba ngăn (thông báo, tin nhắn, tin tức) chung một thanh lọc —
 * trước đây là ba mục rời nhau trong menu (N3, C2: bớt chỗ lặp). Chỉ là thanh chuyển ngăn, không thêm request.
 */
export default function InboxTabs() {
  const pathname = usePathname();
  const { session } = useAuth();
  if (!session) return null; // /tin-tuc mở công khai: khách chưa đăng nhập không có hộp thư
  return (
    <nav aria-label="Hộp thư" className="mb-5 flex gap-2 overflow-x-auto">
      {TABS.map((t) => {
        const on = pathname === t.href || pathname.startsWith(`${t.href}/`);
        return (
          <Link
            key={t.href}
            href={t.href}
            aria-current={on ? "page" : undefined}
            className={`inline-flex min-h-11 shrink-0 items-center rounded-full border px-4 text-sm font-semibold ${
              on ? "border-primary bg-primary-soft text-primary" : "border-line text-ink hover:border-line-strong"
            }`}
          >
            {t.label}
          </Link>
        );
      })}
    </nav>
  );
}
