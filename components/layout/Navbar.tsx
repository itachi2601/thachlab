"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import { ChevronDown, ChevronRight, ClipboardList, KeyRound, LayoutDashboard, LogOut, Menu, MessageCircle, Phone, ShieldCheck, Target, User, Users, X } from "lucide-react";
import { useAuth } from "@/components/auth/auth-context";
import { tabBarShownOn } from "@/components/layout/MobileTabBar";
import ThemeToggle from "@/components/layout/ThemeToggle";
import NotificationBell from "@/components/layout/NotificationBell";
import Avatar from "@/components/ui/Avatar";
import { CONTACT } from "@/lib/contact";

// các đường dẫn thuộc luồng CTTC (dưới /lop-hoc nhưng là hub riêng)
const CTTC_PATHS = ["/lop-hoc/cttc", "/lop-hoc/cnc", "/lop-hoc/tien-phay"];

// Mục "Phụ huynh" chỉ hiện với khách và học sinh: phụ huynh đã có mục "Kết quả của con" trong menu
// tài khoản, giáo viên/admin không dùng trang đó — thêm cho mọi role sẽ chật thanh điều hướng.
type NavLink = { label: string; href: string; audience?: "guest-student"; menu?: { label: string; href: string; hint?: string }[]; note?: string };

// N2 cho phép tối đa 4 mục nhìn thấy; "Thêm" là chỗ gom phần còn lại. "Luyện tập" vẫn để ngoài
// vì đây là việc học sinh mở mỗi ngày — giấu vào "Thêm" thì em không thấy trang. Đo 1024px vẫn một hàng.
const links: NavLink[] = [
  { label: "THPT – THCS", href: "/lop-hoc" },
  { label: "Luyện tập", href: "/luyen-tap" },
  { label: "CTTC", href: "/lop-hoc/cttc" },
  { label: "Đăng ký học", href: "/khoa-hoc" },
  { label: "Phụ huynh", href: "/phu-huynh", audience: "guest-student" },
];

// Khách và phụ huynh đang cân nhắc cho con học (P8, P10, P14): mỗi mục trả lời một câu hỏi họ tự hỏi, không dùng từ nội bộ
// ("CTTC", "THPT – THCS"). Học sinh đã đăng nhập giữ bộ `links` ở trên (việc học hằng ngày).
const EVALUATOR_LINKS: NavLink[] = [
  // "Con học được gì?" — vào thẳng từng lớp, và có chỗ xem thử không cần tài khoản (P14: chỉ link tới thứ có thật)
  {
    label: "Học thử",
    href: "/lop-hoc",
    menu: [
      { label: "KHTN 9", href: "/lop-hoc/khtn-9" },
      { label: "Vật lý 10", href: "/lop-hoc/lop-10" },
      { label: "Vật lý 11", href: "/lop-hoc/lop-11" },
      { label: "Vật lý 12", href: "/lop-hoc/lop-12" },
      { label: "Thí nghiệm mô phỏng", href: "/#thpt", hint: "Tự kéo, tự thử — không cần đăng nhập" },
      { label: "Giao thoa sóng âm", href: "/mo-phong/giao-thoa-am", hint: "Nghe bằng hai loa của máy" },
    ],
  },
  // "Có hiệu quả không?"
  {
    label: "Kết quả học sinh",
    href: "/phu-huynh",
    menu: [
      { label: "Bảng kết quả thật", href: "/phu-huynh#ket-qua" },
      { label: "Phụ huynh xem được gì", href: "/phu-huynh#phu-huynh-thay-gi", hint: "Điểm, điểm danh, học phí của con" },
      { label: "Bảng xếp hạng", href: "/lop-hoc/xep-hang" },
    ],
  },
  // "Ai dạy?" — số năm và nơi công tác lấy từ lib/contact.ts, không viết tay ở đây
  {
    label: "Về thầy",
    href: "/#about",
    note: `${CONTACT.years} năm dạy Vật lý · ${CONTACT.school}`,
    menu: [
      { label: "Giới thiệu thầy", href: "/#about" },
      { label: "Thầy đứng lớp", href: "/phu-huynh#thay-dung-lop", hint: "Ảnh thật và cách liên hệ" },
    ],
  },
  // "Học khi nào, bao nhiêu?"
  { label: "Lớp & học phí", href: "/khoa-hoc" },
];
const EVALUATOR_MORE: NavLink[] = [
  { label: "Luyện tập", href: "/luyen-tap" },
  { label: "Blog", href: "/blog" },
  { label: "Tin tức", href: "/tin-tuc" },
  { label: "Liên hệ", href: "/#contact" },
];

// Gom vào mục "Thêm" trên desktop (N2: ≤4 lựa chọn/vùng); menu mobile vẫn liệt kê đủ.
const MORE_LINKS: NavLink[] = [
  { label: "Blog", href: "/blog" },
  { label: "Tin tức", href: "/tin-tuc" },
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
  const mobileMenuRef = useRef<HTMLDivElement>(null);
  const mobileToggleRef = useRef<HTMLButtonElement>(null);
  const moreRef = useRef<HTMLLIElement>(null);
  const isStaff = profile?.role === "admin" || profile?.role === "instructor";
  const isTa = profile?.role === "tro_giang";
  const showParentLink = !session || profile?.role === "student";
  // Chỉ khách = người đang đánh giá (phụ huynh đã đăng nhập có ParentHome, không có các mã neo của trang khách).
  const isEvaluator = !session;
  const navLinks = isEvaluator ? EVALUATOR_LINKS : links.filter((link) => link.audience !== "guest-student" || showParentLink);
  const moreLinks = isEvaluator ? EVALUATOR_MORE : MORE_LINKS;
  // Thanh đáy đã có Lớp học và Luyện tập: khi nó hiện thì menu ☰ bỏ hai hàng đó (giữ chip vào nhanh từng lớp).
  const tabBarShown = tabBarShownOn(pathname);
  // Chỉ thanh đáy của khách và học sinh THPT có Lớp học/Học thử + Luyện tập; vai khác (phụ huynh, CTTC, GV, TA) thì menu ☰ vẫn giữ hai hàng đó.
  const barHasClassAndPractice = !session || (profile?.role === "student" && profile.track !== "cttc");
  const mobileLinks = isEvaluator ? [...navLinks, ...moreLinks] : [...navLinks.slice(0, 3), ...moreLinks.slice(0, 2), ...navLinks.slice(3), ...moreLinks.slice(2)];

  useEffect(() => {
    if (!accountMenuOpen) return;
    function onClickOutside(event: MouseEvent) {
      if (accountMenuRef.current && !accountMenuRef.current.contains(event.target as Node)) setAccountMenuOpen(false);
    }
    document.addEventListener("mousedown", onClickOutside);
    return () => document.removeEventListener("mousedown", onClickOutside);
  }, [accountMenuOpen]);

  // Menu mobile: đóng khi bấm ra ngoài, nhấn Escape, hoặc đổi trang.
  useEffect(() => {
    if (!mobileMenuOpen) return;
    function onClickOutside(event: MouseEvent) {
      const t = event.target as Node;
      if (mobileMenuRef.current?.contains(t) || mobileToggleRef.current?.contains(t)) return;
      setMobileMenuOpen(false);
    }
    document.addEventListener("mousedown", onClickOutside);
    return () => document.removeEventListener("mousedown", onClickOutside);
  }, [mobileMenuOpen]);

  useEffect(() => {
    setMobileMenuOpen(false);
    setAccountMenuOpen(false);
  }, [pathname]);

  // Escape đóng mọi menu; với dropdown "Thêm" (mở bằng hover/focus) thì bỏ focus để đóng.
  useEffect(() => {
    function onKey(event: KeyboardEvent) {
      if (event.key !== "Escape") return;
      setMobileMenuOpen(false);
      setAccountMenuOpen(false);
      const active = document.activeElement as HTMLElement | null;
      if (active && (moreRef.current?.contains(active))) active.blur();
    }
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, []);

  return (
    <header className="fixed inset-x-0 top-0 z-50 border-b border-white/10 bg-[#05070B]/90 backdrop-blur-md">
      <nav className="relative mx-auto flex max-w-6xl items-center justify-between gap-3 px-4 py-3 sm:gap-4 sm:px-6 sm:py-4 lg:px-8">
        <Link href="/" className="flex items-center gap-2">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src="/brand/logo-mark.svg" alt="" width={32} height={32} className="h-8 w-8" />
          <span className="font-display text-lg font-semibold tracking-tight text-white">
            Thach<span className="text-[#3B82F6]">Lab</span>
          </span>
          <span className="shrink-0 whitespace-nowrap rounded-full border border-amber-400/30 bg-amber-500/10 px-2 py-0.5 text-[11px] font-semibold leading-none text-amber-300 sm:text-xs">
            <span className="2xl:hidden">Alpha</span>
            <span className="hidden 2xl:inline">Alpha test · miễn phí</span>
          </span>
        </Link>

        <ul className="hidden items-center gap-4 lg:flex xl:gap-5 2xl:gap-8">
          {navLinks.map((link) => {
            const quick: { label: string; href: string; hint?: string }[] | undefined = link.menu ?? (link.href === "/lop-hoc" ? THPT_QUICK_LINKS : undefined);
            const hasQuick = !!quick;
            const inCttc = CTTC_PATHS.some((path) => pathname.startsWith(path));
            const isActive =
              !link.href.startsWith("/#") &&
              (pathname === link.href || pathname.startsWith(`${link.href}/`)) &&
              (link.href !== "/lop-hoc" || !inCttc);
            return (
              <li key={link.href} className={hasQuick ? "group relative" : undefined}>
                <Link
                  href={link.href}
                  aria-current={isActive ? "page" : undefined}
                  className={`inline-flex items-center gap-1 whitespace-nowrap text-sm font-medium transition-colors hover:text-white ${
                    isActive ? "text-white" : "text-slate-300"
                  }`}
                >
                  {link.label}
                  {hasQuick && (
                    <ChevronDown size={14} className="text-slate-500 transition-transform group-hover:rotate-180" />
                  )}
                </Link>
                {hasQuick && (
                  // pt-3 làm "cầu" để chuột đi từ chữ xuống menu không bị đóng; hiện khi hover hoặc focus (bàn phím).
                  <div className="invisible absolute left-1/2 top-full -translate-x-1/2 pt-3 opacity-0 transition-opacity group-focus-within:visible group-focus-within:opacity-100 group-hover:visible group-hover:opacity-100">
                    <ul className="w-64 overflow-hidden rounded-2xl border border-white/10 bg-[#0B1220]/[0.98] p-1.5 shadow-2xl shadow-black/50">
                      {link.note && <li className="px-3.5 pb-1 pt-2 text-xs font-medium text-slate-400">{link.note}</li>}
                      {quick!.map((q) => (
                        <li key={q.href}>
                          <Link
                            href={q.href}
                            className="flex items-center justify-between gap-2 rounded-xl px-3.5 py-2.5 text-sm font-semibold text-slate-200 transition-colors hover:bg-white/[0.07] hover:text-white"
                          >
                            <span>
                              {q.label}
                              {q.hint && <span className="block text-xs font-normal text-slate-400">{q.hint}</span>}
                            </span>
                            <ChevronRight size={15} className="shrink-0 text-slate-500" />
                          </Link>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </li>
            );
          })}
          <li ref={moreRef} className="group relative">
            <button
              type="button"
              aria-haspopup="menu"
              className="inline-flex items-center gap-1 whitespace-nowrap text-sm font-medium text-slate-300 transition-colors hover:text-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3B82F6]"
            >
              Thêm
              <ChevronDown size={14} className="text-slate-500 transition-transform group-hover:rotate-180 group-focus-within:rotate-180" />
            </button>
            <div className="invisible absolute right-0 top-full pt-3 opacity-0 transition-opacity group-focus-within:visible group-focus-within:opacity-100 group-hover:visible group-hover:opacity-100">
              <ul className="w-48 overflow-hidden rounded-2xl border border-white/10 bg-[#0B1220]/[0.98] p-1.5 shadow-2xl shadow-black/50">
                {moreLinks.map((q) => (
                  <li key={q.href}>
                    <Link
                      href={q.href}
                      className="flex items-center justify-between whitespace-nowrap rounded-xl px-3.5 py-2.5 text-sm font-semibold text-slate-200 transition-colors hover:bg-white/[0.07] hover:text-white"
                    >
                      {q.label}
                      <ChevronRight size={15} className="text-slate-500" />
                    </Link>
                  </li>
                ))}
                {isEvaluator && CONTACT.zalo && (
                  <li className="mt-1 border-t border-white/10 pt-1">
                    <a href={CONTACT.zalo} target="_blank" rel="noopener noreferrer" className="flex items-center gap-2 rounded-xl px-3.5 py-2.5 text-sm font-semibold text-slate-200 hover:bg-white/[0.07] hover:text-white"><MessageCircle size={15} aria-hidden /> Nhắn Zalo cho thầy</a>
                  </li>
                )}
                {isEvaluator && CONTACT.phone && (
                  <li>
                    <a href={`tel:${CONTACT.phone}`} className="flex items-center gap-2 rounded-xl px-3.5 py-2.5 text-sm font-semibold text-slate-200 hover:bg-white/[0.07] hover:text-white"><Phone size={15} aria-hidden /> Gọi {CONTACT.phone}</a>
                  </li>
                )}
              </ul>
            </div>
          </li>
        </ul>

        <div className="flex items-center gap-2 sm:gap-3">
          {isEvaluator && (CONTACT.phone || CONTACT.zalo) && (
            // P10: gọi/nhắn thầy bấm được ngay tại chỗ đang đọc. Chỉ từ 1800px vì dưới đó thanh đã đủ chật (N2); mobile có trong menu ☰.
            <span className="hidden items-center gap-1.5 whitespace-nowrap min-[1800px]:flex">
              {CONTACT.zalo && (
                <a href={CONTACT.zalo} target="_blank" rel="noopener noreferrer" className="inline-flex min-h-11 items-center gap-1.5 rounded-full px-3 text-sm font-semibold text-slate-200 transition-colors hover:bg-white/[0.07] hover:text-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3B82F6]">
                  <MessageCircle size={16} aria-hidden /> Nhắn Zalo
                </a>
              )}
              {CONTACT.phone && (
                <a href={`tel:${CONTACT.phone}`} className="inline-flex min-h-11 items-center gap-1.5 rounded-full px-3 text-sm font-semibold text-slate-200 transition-colors hover:bg-white/[0.07] hover:text-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3B82F6]">
                  <Phone size={16} aria-hidden /> Gọi thầy
                </a>
              )}
            </span>
          )}
          <span className="hidden sm:inline-flex">
            <ThemeToggle />
          </span>
          <NotificationBell />
          {session ? (
            <div className="relative" ref={accountMenuRef}>
              <button
                type="button"
                aria-expanded={accountMenuOpen}
                aria-haspopup="menu"
                aria-label="Tài khoản"
                onClick={() => setAccountMenuOpen((open) => !open)}
                className="flex h-11 w-11 items-center justify-center gap-2 rounded-full bg-primary/15 text-sm font-semibold text-[#3B82F6] transition-colors hover:bg-primary/25 sm:w-auto sm:py-1.5 sm:pl-1.5 sm:pr-4"
              >
                <Avatar url={profile?.avatar_url} name={profile?.full_name} size={26} />
                <span className="hidden sm:inline">{profile?.full_name?.split(" ").pop() ?? "Tài khoản"}</span>
                <ChevronDown size={15} className={`hidden transition-transform sm:inline ${accountMenuOpen ? "rotate-180" : ""}`} />
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
                  {isTa && (
                    <Link
                      href="/dashboard-thpt"
                      onClick={() => setAccountMenuOpen(false)}
                      className="flex items-center gap-2.5 rounded-xl px-3.5 py-2.5 text-sm font-semibold text-slate-200 transition-colors hover:bg-white/[0.07] hover:text-white"
                    >
                      <LayoutDashboard size={16} /> Quản lớp · THPT
                    </Link>
                  )}
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
                className="hidden min-h-11 items-center whitespace-nowrap rounded-full bg-primary px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm shadow-blue-900/30 transition-transform hover:-translate-y-0.5 hover:bg-primary-dark sm:inline-flex sm:px-5"
              >
                <span className="xl:hidden">Đăng ký</span>
                <span className="hidden xl:inline">Học thử miễn phí</span>
              </Link>
            </>
          )}

          <button
            type="button"
            ref={mobileToggleRef}
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
            ref={mobileMenuRef}
            className="absolute left-3 right-3 top-[calc(100%+8px)] max-h-[calc(100dvh-80px)] overflow-y-auto rounded-2xl border border-white/10 bg-[#0B1220] p-2 shadow-2xl shadow-black/50 lg:hidden"
          >
            <ul className="grid gap-1">
              {mobileLinks.map((link) => {
                const inCttc = CTTC_PATHS.some((path) => pathname.startsWith(path));
                const isActive =
                  link.href !== "/" &&
                  !link.href.startsWith("/#") &&
                  pathname.startsWith(link.href) &&
                  // hai luồng riêng: /lop-hoc/cttc, /cnc, /tien-phay không tính cho mục THPT
                  (link.href !== "/lop-hoc" || !inCttc);
                const onTabBar = tabBarShown && barHasClassAndPractice && (link.href === "/lop-hoc" || link.href === "/luyen-tap");
                if (onTabBar && link.href !== "/lop-hoc") return null;

                return (
                  <li key={link.href}>
                    {!onTabBar && (
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
                    )}
                    {(link.menu ?? (link.href === "/lop-hoc" ? THPT_QUICK_LINKS : null)) && (
                      <div className="flex flex-wrap gap-1.5 px-4 pb-2 pt-1">
                        {(link.menu ?? THPT_QUICK_LINKS).map((q) => (
                          <Link
                            key={q.href}
                            href={q.href}
                            onClick={() => setMobileMenuOpen(false)}
                            className="inline-flex min-h-11 items-center rounded-full border border-white/10 px-3.5 text-xs font-semibold text-slate-300 transition-colors hover:bg-white/[0.07] hover:text-white"
                          >
                            {q.label}
                          </Link>
                        ))}
                      </div>
                    )}
                  </li>
                );
              })}
              <li className="border-t border-white/10 pt-1 sm:hidden">
                <div className="flex min-h-12 items-center justify-between rounded-xl px-4 text-[15px] font-semibold text-slate-200">
                  Giao diện sáng/tối
                  <ThemeToggle />
                </div>
              </li>
              {isEvaluator && (CONTACT.phone || CONTACT.zalo) && (
                <li className="grid grid-cols-2 gap-2 border-t border-white/10 px-2 pb-1 pt-2">
                  {CONTACT.zalo && (
                    <a href={CONTACT.zalo} target="_blank" rel="noopener noreferrer" className="inline-flex min-h-12 items-center justify-center gap-2 rounded-xl border border-white/10 text-[15px] font-semibold text-slate-100 hover:bg-white/[0.07]">
                      <MessageCircle size={18} aria-hidden /> Nhắn Zalo
                    </a>
                  )}
                  {CONTACT.phone && (
                    <a href={`tel:${CONTACT.phone}`} className="inline-flex min-h-12 items-center justify-center gap-2 rounded-xl border border-white/10 text-[15px] font-semibold text-slate-100 hover:bg-white/[0.07]">
                      <Phone size={18} aria-hidden /> Gọi thầy
                    </a>
                  )}
                </li>
              )}
              {!session && (
                <li className="border-t border-white/10 pt-1 sm:hidden">
                  <Link
                    href="/dang-ky"
                    onClick={() => setMobileMenuOpen(false)}
                    className="flex min-h-12 items-center justify-between rounded-xl px-4 py-3 text-[15px] font-semibold text-blue-300 transition-colors hover:bg-blue-500/10"
                  >
                    Học thử miễn phí
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
