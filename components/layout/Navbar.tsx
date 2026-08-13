"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { ChevronRight, Menu, X } from "lucide-react";
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
  const pathname = usePathname();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="fixed inset-x-0 top-0 z-50 border-b border-white/10 bg-[#05070B]/90 backdrop-blur-md">
      <nav className="relative mx-auto flex max-w-6xl items-center justify-between px-4 py-3 sm:px-6 sm:py-4 lg:px-8">
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
          {session && profile?.role === "admin" && (
            <li>
              <Link
                href="/dashboard"
                className="text-sm font-medium text-slate-300 transition-colors hover:text-white"
              >
                Dashboard giáo viên
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

        <div className="flex items-center gap-2 sm:gap-3">
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
                className="rounded-full bg-[#2563EB] px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm shadow-blue-900/30 transition-transform hover:-translate-y-0.5 hover:bg-[#1D4ED8] sm:px-5"
              >
                Đăng ký
              </Link>
            </>
          )}

          <button
            type="button"
            aria-expanded={mobileMenuOpen}
            aria-controls="mobile-main-navigation"
            aria-label={mobileMenuOpen ? "Đóng menu điều hướng" : "Mở menu điều hướng"}
            onClick={() => setMobileMenuOpen((open) => !open)}
            className="inline-flex h-11 w-11 items-center justify-center rounded-xl border border-white/10 bg-white/[0.06] text-slate-200 transition-colors hover:bg-white/10 hover:text-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3B82F6] md:hidden"
          >
            {mobileMenuOpen ? <X size={22} /> : <Menu size={22} />}
          </button>
        </div>

        {mobileMenuOpen && (
          <div
            id="mobile-main-navigation"
            className="absolute left-3 right-3 top-[calc(100%+8px)] overflow-hidden rounded-2xl border border-white/10 bg-[#0B1220]/[0.98] p-2 shadow-2xl shadow-black/50 md:hidden"
          >
            <ul className="grid gap-1">
              {links.map((link) => {
                const isActive =
                  link.href !== "/" &&
                  !link.href.startsWith("/#") &&
                  pathname.startsWith(link.href);

                return (
                  <li key={link.href}>
                    <Link
                      href={link.href}
                      onClick={() => setMobileMenuOpen(false)}
                      aria-current={isActive ? "page" : undefined}
                      className={`flex min-h-12 items-center justify-between rounded-xl px-4 py-3 text-[15px] font-semibold transition-colors ${
                        isActive
                          ? "bg-[#2563EB]/20 text-[#60A5FA]"
                          : "text-slate-200 hover:bg-white/[0.07] hover:text-white"
                      }`}
                    >
                      {link.label}
                      <ChevronRight size={18} className="text-slate-500" />
                    </Link>
                  </li>
                );
              })}

              {session && profile?.role === "admin" && (
                <li>
                  <Link
                    href="/dashboard"
                    onClick={() => setMobileMenuOpen(false)}
                    className="flex min-h-12 items-center justify-between rounded-xl px-4 py-3 text-[15px] font-semibold text-slate-200 transition-colors hover:bg-white/[0.07] hover:text-white"
                  >
                    Dashboard giáo viên
                    <ChevronRight size={18} className="text-slate-500" />
                  </Link>
                </li>
              )}

              {profile?.role === "admin" && (
                <li>
                  <Link
                    href="/quan-tri"
                    onClick={() => setMobileMenuOpen(false)}
                    className="flex min-h-12 items-center justify-between rounded-xl bg-cyan-400/10 px-4 py-3 text-[15px] font-semibold text-[#22D3EE] transition-colors hover:bg-cyan-400/15"
                  >
                    Quản trị
                    <ChevronRight size={18} />
                  </Link>
                </li>
              )}
            </ul>
          </div>
        )}
      </nav>
    </header>
  );
}
