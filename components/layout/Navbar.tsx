"use client";

import Link from "next/link";
import { useAuth } from "@/components/auth/AuthProvider";

const links = [
  { label: "Lớp học", href: "/lop-hoc" },
  { label: "Đề thi", href: "/kiem-tra" },
  { label: "Blog", href: "/blog" },
  { label: "Tin tức", href: "/tin-tuc" },
  { label: "Giới thiệu", href: "/#about" },
  { label: "Liên hệ", href: "/#contact" },
];

export default function Navbar() {
  const { session, profile } = useAuth();

  return (
    <header className="fixed top-0 inset-x-0 z-50 border-b border-white/10 bg-[#05070B]/90 backdrop-blur-md">
      <nav className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4 lg:px-8">
        <Link href="/" className="flex items-center gap-2">
          <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-[#2563EB] text-sm font-bold text-white font-display">
            T
          </span>
          <span className="font-display text-lg font-semibold tracking-tight text-white">
            Thach<span className="text-[#3B82F6]">Lab</span>
          </span>
        </Link>

        <ul className="hidden items-center gap-8 md:flex">
          {links.map((link) => (
            <li key={link.href}>
              <Link
                href={link.href}
                className="text-sm font-medium text-slate-300 transition-colors hover:text-white"
              >
                {link.label}
              </Link>
            </li>
          ))}
          {session && (
            <li>
              <Link
                href="/tin-nhan"
                className="text-sm font-medium text-slate-300 transition-colors hover:text-white"
              >
                Tin nhắn
              </Link>
            </li>
          )}
          {profile?.role === "admin" && (
            <li>
              <Link
                href="/quan-tri"
                className="text-sm font-medium text-[#22D3EE] transition-colors hover:text-white"
              >
                Quản trị
              </Link>
            </li>
          )}
        </ul>

        <div className="flex items-center gap-3">
          {session ? (
            <Link
              href="/tai-khoan"
              className="rounded-full bg-[#2563EB]/15 px-4 py-2 text-sm font-semibold text-[#3B82F6] transition-colors hover:bg-[#2563EB]/25"
            >
              {profile?.full_name?.split(" ").pop() ?? "Tài khoản"}
            </Link>
          ) : (
            <>
              <Link
                href="/dang-nhap"
                className="hidden rounded-full px-4 py-2 text-sm font-medium text-slate-300 transition-colors hover:text-white sm:inline-block"
              >
                Đăng nhập
              </Link>
              <Link
                href="/dang-ky"
                className="rounded-full bg-[#2563EB] px-5 py-2.5 text-sm font-semibold text-white shadow-sm shadow-blue-900/30 transition-transform hover:-translate-y-0.5 hover:bg-[#1D4ED8]"
              >
                Đăng ký
              </Link>
            </>
          )}
        </div>
      </nav>
    </header>
  );
}
