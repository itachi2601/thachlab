"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import { ChevronDown, ChevronRight, ClipboardList, KeyRound, LayoutDashboard, LogOut, Menu, ShieldCheck, Target, User, Users, X } from "lucide-react";
import { useAuth } from "@/components/auth/auth-context";
import ThemeToggle from "@/components/layout/ThemeToggle";
import NotificationBell from "@/components/layout/NotificationBell";
import Avatar from "@/components/ui/Avatar";

// các đường dẫn thuộc luồng CTTC (dưới /lop-hoc nhưng là hub riêng)
const CTTC_PATHS = ["/lop-hoc/cttc", "/lop-hoc/cnc", "/lop-hoc/tien-phay"];

// Mục "Phụ huynh" chỉ hiện với khách và học sinh: phụ huynh đã có mục "Kết quả của con" trong menu
// tài khoản, giáo viên/admin không dùng trang đó — thêm cho mọi role sẽ chật thanh điều hướng.
type NavLink = { label: string; href: string; audience?: "guest-student" };

const links: NavLink[] = [
  { label: "THPT – THCS", href: "/lop-hoc" },
  { label: "CTTC", href: "/lop-hoc/cttc" },
  { label: "Đăng ký học", href: "/khoa-hoc" },
  { label: "Blog", href: "/blog" },
  { label: "Tin tức", href: "/tin-tuc" },
  { label: "Phụ huynh", href: "/phu-huynh", audience: "guest-student" },
  { label: "Giới thiệu", href: "/#about" },
  { label: "Liên hệ", href: "/#contact" },
];

// Vào nhanh từng lớp (menu thả xuống dưới "THPT – THCS" trên desktop, hàng chip trong menu mobile) —
// học sinh quay lại hằng ngày vào thẳng lớp mình từ mọi trang, không qua /lop-hoc.
const THPT_QUICK_LINKS = [
  { label: "KHTN 9", href: "/lop-hoc/khtn-9" },
  { label: "Vật lý 10", href: "/lop-hoc/lop-10" },
  { label: "Vật lý 11", href: "/lop-hoc/lop-11" },
  { label: "Vật lý 12", href: "/lop-hoc/lop-12" },
  { label: "Bảng xếp hạng", href: "/lop-hoc/xep-hang" },
];

export default function Navbar() {
  const { session, profile, signOut } = useAuth();
  const pathname = usePathname();
  const router = useRouter();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [accountMenuOpen, setAccountMenuOpen] = useState(false);
  const accountMenuRef = useRef<HTMLDivElement>(null);
  const isStaff = profile?.role === "admin" || profile?.role === "instructor";
  const showParentLink = !session || profile?.role === "student";
  const navLinks = links.filter((link) => link.audience !== "guest-student" || showParentLink);

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
      <nav className="relative mx-auto flex max-w-6xl items-center justify-between gap-3 px-4 py-3 sm:gap-4 sm:px-6 sm:py-4 lg:px-8">
        <Link href="/" className="flex items-center gap-2">
          <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-sm font-bold text-white font-display">
            T
          </span>
          <span className="font-display text-lg font-semibold tracking-tight text-white">
            Thach<span className="text-[#3B82F6]">Lab</span>
          </span>
        </Link>

        <ul className="hidden items-center gap-5 lg:flex xl:gap-8">
          {navLinks.map((link) => {
            const hasQuick = link.href === "/lop-hoc";
            return (
              <li key={link.href} className={hasQuick ? "group relative" : undefined}>
                <Link
                  href={link.href}
                  className="inline-flex items-center gap-1 text-sm font-medium text-slate-300 transition-colors hover:text-white"
                >
                  {link.label}
                  {hasQuick && (
                    <ChevronDown size={14} className="text-slate-500 transition-transform group-hover:rotate-180" />
                  )}
                </Link>
                {hasQuick && (
                  // pt-3 làm "cầu" để chuột đi từ chữ xuống menu không bị đóng; hiện khi hover hoặc focus (bàn phím).
                  <div className="invisible absolute left-1/2 top-full -translate-x-1/2 pt-3 opacity-0 transition-opacity group-focus-within:visible group-focus-within:opacity-100 group-hover:visible group-hover:opacity-100">
                    <ul className="w-52 overflow-hidden rounded-2xl border border-white/10 bg-[#0B1220]/[0.98] p-1.5 shadow-2xl shadow-black/50">
                      {THPT_QUICK_LINKS.map((q) => (
                        <li key={q.href}>
                          <Link
                            href={q.href}
                            className="flex items-center justify-between rounded-xl px-3.5 py-2.5 text-sm font-semibold text-slate-200 transition-colors hover:bg-white/[0.07] hover:text-white"
                          >
                            {q.label}
                            <ChevronRight size={15} className="text-slate-500" />
                          </Link>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </li>
            );
          })}
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
                  <Link
                    href="/tai-khoan/doi-mat-khau"
                    onClick={() => setAccountMenuOpen(false)}
                    className="flex items-center gap-2.5 rounded-xl px-3.5 py-2.5 text-sm font-semibold text-slate-200 transition-colors hover:bg-white/[0.07] hover:text-white"
                  >
                    <KeyRound size={16} /> Đổi mật khẩu
                  </Link>
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
                className="hidden whitespace-nowrap rounded-full bg-primary px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm shadow-blue-900/30 transition-transform hover:-translate-y-0.5 hover:bg-primary-dark sm:inline-block sm:px-5"
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
              {navLinks.map((link) => {
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
                    {link.href === "/lop-hoc" && (
                      <div className="flex flex-wrap gap-1.5 px-4 pb-2 pt-1">
                        {THPT_QUICK_LINKS.map((q) => (
                          <Link
                            key={q.href}
                            href={q.href}
                            onClick={() => setMobileMenuOpen(false)}
                            className="rounded-full border border-white/10 px-3 py-1.5 text-xs font-semibold text-slate-300 transition-colors hover:bg-white/[0.07] hover:text-white"
                          >
                            {q.label}
                          </Link>
                        ))}
                      </div>
                    )}
                    {link.href === "/phu-huynh" && (
                      <div className="flex flex-wrap gap-1.5 px-4 pb-2 pt-1">
                        <Link
                          href={link.href}
                          onClick={() => setMobileMenuOpen(false)}
                          className="rounded-full border border-white/10 px-3 py-1.5 text-xs font-semibold text-slate-300 transition-colors hover:bg-white/[0.07] hover:text-white"
                        >
                          Xem kết quả của con
                        </Link>
                      </div>
                    )}
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
