"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import { ChevronDown, ChevronRight, ClipboardList, LayoutDashboard, LogOut, Menu, ShieldCheck, Target, User, Users, X } from "lucide-react";
import { useAuth } from "@/components/auth/AuthProvider";
import ThemeToggle from "@/components/layout/ThemeToggle";
import NotificationBell from "@/components/layout/NotificationBell";
import Avatar from "@/components/ui/Avatar";

// các đường dẫn thuộc luồng CTTC (dưới /lop-hoc nhưng là hub riêng)
const CTTC_PATHS = ["/lop-hoc/cttc", "/lop-hoc/cnc", "/lop-hoc/tien-phay"];

const links = [
  { label: "THPT – THCS", href: "/lop-hoc" },
  { label: "CTTC", href: "/lop-hoc/cttc" },
  { label: "Đăng ký học", href: "/khoa-hoc" },
  { label: "Blog", href: "/blog" },
  { label: "Tin tức", href: "/tin-tuc" },
  { label: "Giới thiệu", href: "/#about" },
  { label: "Liên hệ", href: "/#contact" },
];

export default function Navbar() {
  const { session, profile, signOut } = useAuth();
  const pathname = usePathname();
  const router = useRouter();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [accountMenuOpen, setAccountMenuOpen] = useState(false);
  const accountMenuRef = useRef<HTMLDivElement>(null);
  const isStaff = profile?.role === "admin" || profile?.role === "instructor";

  useEffect(() => {
    if (!accountMenuOpen) return;
    function onClickOutside(event: MouseEvent) {
      if (accountMenuRef.current && !accountMenuRef.current.contains(event.target as Node)) setAccountMenuOpen(false);
    }
    document.addEventListener("mousedown", onClickOutside);
    return () => document.removeEventListener("mousedown", onClickOutside);
  }, [accountMenuOpen]);

  return (
    <header className="fixed inset-x-0 top-0 z-50 border-b border-white/10 bg-[#05070B]/90 backdrop-blur-md">
      <nav className="relative mx-auto flex max-w-6xl items-center justify-between px-4 py-3 sm:px-6 sm:py-4 lg:px-8">
        <Link href="/" className="flex items-center gap-2">
          <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-sm font-bold text-white font-display">
            T
          </span>
          <span className="font-display text-lg font-semibold tracking-tight text-white">
            Thach<span className="text-[#3B82F6]">Lab</span>
          </span>
        </Link>

        <ul className="hidden items-center gap-8 lg:flex">
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
        </ul>

        <div className="flex items-center gap-2 sm:gap-3">
          <ThemeToggle />
          <NotificationBell />
          {session ? (
            <div className="relative" ref={accountMenuRef}>
              <button
                type="button"
                aria-expanded={accountMenuOpen}
                aria-haspopup="menu"
                onClick={() => setAccountMenuOpen((open) => !open)}
                className="flex items-center gap-2 rounded-full bg-primary/15 py-1.5 pl-1.5 pr-3.5 text-sm font-semibold text-[#3B82F6] transition-colors hover:bg-primary/25 sm:pr-4"
              >
                <Avatar url={profile?.avatar_url} name={profile?.full_name} size={26} />
                {profile?.full_name?.split(" ").pop() ?? "Tài khoản"}
                <ChevronDown size={15} className={`transition-transform ${accountMenuOpen ? "rotate-180" : ""}`} />
              </button>
              {accountMenuOpen && (
                <div
                  role="menu"
                  className="absolute right-0 top-[calc(100%+8px)] w-56 overflow-hidden rounded-2xl border border-white/10 bg-[#0B1220]/[0.98] p-1.5 shadow-2xl shadow-black/50"
                >
                  <Link
                    href="/tai-khoan"
                    onClick={() => setAccountMenuOpen(false)}
                    className="flex items-center gap-2.5 rounded-xl px-3.5 py-2.5 text-sm font-semibold text-slate-200 transition-colors hover:bg-white/[0.07] hover:text-white"
                  >
                    <User size={16} /> Tài khoản của tôi
                  </Link>
                  {profile?.role === "parent" && (
                    <Link
                      href="/phu-huynh"
                      onClick={() => setAccountMenuOpen(false)}
                      className="flex items-center gap-2.5 rounded-xl px-3.5 py-2.5 text-sm font-semibold text-slate-200 transition-colors hover:bg-white/[0.07] hover:text-white"
                    >
                      <Users size={16} /> Kết quả của con
                    </Link>
                  )}
                  {!isStaff && profile?.role !== "parent" && (
                    <Link
                      href="/lop-hoc/ket-qua"
                      onClick={() => setAccountMenuOpen(false)}
                      className="flex items-center gap-2.5 rounded-xl px-3.5 py-2.5 text-sm font-semibold text-slate-200 transition-colors hover:bg-white/[0.07] hover:text-white"
                    >
                      <Target size={16} /> Kết quả học tập
                    </Link>
                  )}
                  {isStaff && profile?.admin_area !== "thpt" && (
                    <Link
                      href="/dashboard"
                      onClick={() => setAccountMenuOpen(false)}
                      className="flex items-center gap-2.5 rounded-xl px-3.5 py-2.5 text-sm font-semibold text-slate-200 transition-colors hover:bg-white/[0.07] hover:text-white"
                    >
                      <LayoutDashboard size={16} /> Dashboard giáo viên · CTTC
                    </Link>
                  )}
                  {isStaff && profile?.admin_area !== "cttc" && (
                    <Link
                      href="/dashboard-thpt"
                      onClick={() => setAccountMenuOpen(false)}
                      className="flex items-center gap-2.5 rounded-xl px-3.5 py-2.5 text-sm font-semibold text-slate-200 transition-colors hover:bg-white/[0.07] hover:text-white"
                    >
                      <LayoutDashboard size={16} /> Dashboard giáo viên · THPT
                    </Link>
                  )}
                  {/* Trợ giảng trước đây phải tự gõ /tro-giang mới vào được khu làm việc của mình. */}
                  {profile?.role === "tro_giang" && (
                    <Link
                      href="/tro-giang"
                      onClick={() => setAccountMenuOpen(false)}
                      className="flex items-center gap-2.5 rounded-xl px-3.5 py-2.5 text-sm font-semibold text-slate-200 transition-colors hover:bg-white/[0.07] hover:text-white"
                    >
                      <ClipboardList size={16} /> Khu trợ giảng
                    </Link>
                  )}
                  {profile?.role === "admin" && (
                    <Link
                      href="/quan-tri"
                      onClick={() => setAccountMenuOpen(false)}
                      className="flex items-center gap-2.5 rounded-xl px-3.5 py-2.5 text-sm font-semibold text-[#22D3EE] transition-colors hover:bg-cyan-400/10"
                    >
                      <ShieldCheck size={16} /> Quản trị
                    </Link>
                  )}
                  <button
                    type="button"
                    onClick={() => { setAccountMenuOpen(false); void signOut().then(() => router.push("/")); }}
                    className="flex w-full items-center gap-2.5 rounded-xl px-3.5 py-2.5 text-left text-sm font-semibold text-red-300 transition-colors hover:bg-red-500/10"
                  >
                    <LogOut size={16} /> Đăng xuất
                  </button>
                </div>
              )}
            </div>
          ) : (
            <>
              <Link
                href="/dang-nhap"
                className="inline-flex min-h-11 shrink-0 items-center justify-center whitespace-nowrap rounded-full border border-blue-400/40 bg-blue-500/10 px-3.5 py-2 text-sm font-semibold text-white transition-colors hover:border-blue-400/70 hover:bg-blue-500/20 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3B82F6] sm:px-4"
              >
                Đăng nhập
              </Link>
              <Link
                href="/dang-ky"
                className="hidden rounded-full bg-primary px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm shadow-blue-900/30 transition-transform hover:-translate-y-0.5 hover:bg-primary-dark sm:inline-block sm:px-5"
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
            className="inline-flex h-11 w-11 items-center justify-center rounded-xl border border-white/10 bg-white/[0.06] text-slate-200 transition-colors hover:bg-white/10 hover:text-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3B82F6] lg:hidden"
          >
            {mobileMenuOpen ? <X size={22} /> : <Menu size={22} />}
          </button>
        </div>

        {mobileMenuOpen && (
          <div
            id="mobile-main-navigation"
            className="absolute left-3 right-3 top-[calc(100%+8px)] overflow-hidden rounded-2xl border border-white/10 bg-[#0B1220]/[0.98] p-2 shadow-2xl shadow-black/50 lg:hidden"
          >
            <ul className="grid gap-1">
              {links.map((link) => {
                const inCttc = CTTC_PATHS.some((path) => pathname.startsWith(path));
                const isActive =
                  link.href !== "/" &&
                  !link.href.startsWith("/#") &&
                  pathname.startsWith(link.href) &&
                  // hai luồng riêng: /lop-hoc/cttc, /cnc, /tien-phay không tính cho mục THPT
                  (link.href !== "/lop-hoc" || !inCttc);

                return (
                  <li key={link.href}>
                    <Link
                      href={link.href}
                      onClick={() => setMobileMenuOpen(false)}
                      aria-current={isActive ? "page" : undefined}
                      className={`flex min-h-12 items-center justify-between rounded-xl px-4 py-3 text-[15px] font-semibold transition-colors ${
                        isActive
                          ? "bg-primary/20 text-[#60A5FA]"
                          : "text-slate-200 hover:bg-white/[0.07] hover:text-white"
                      }`}
                    >
                      {link.label}
                      <ChevronRight size={18} className="text-slate-500" />
                    </Link>
                  </li>
                );
              })}
              {!session && (
                <li className="border-t border-white/10 pt-1 sm:hidden">
                  <Link
                    href="/dang-ky"
                    onClick={() => setMobileMenuOpen(false)}
                    className="flex min-h-12 items-center justify-between rounded-xl px-4 py-3 text-[15px] font-semibold text-[#60A5FA] transition-colors hover:bg-blue-500/10"
                  >
                    Đăng ký
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
