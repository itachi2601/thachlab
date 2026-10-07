"use client";

/**
 * components/layout/MobileTabBar.tsx
 *
 * Thanh đáy kiểu app cho điện thoại/tablet, mỗi vai một bộ nút (thầy chốt 7/10/2026):
 *   khách        Trang chủ · Học thử · Luyện tập · Đăng nhập
 *   HS THPT      Hôm nay · Bài học · Luyện tập · Xếp hạng · Thêm        (chấm đỏ "Hôm nay", số chưa đọc ở "Thêm")
 *   SV CTTC      Khoá học · Bài học · Thông báo · Thêm
 *   phụ huynh    Kết quả của con · Thông báo · Thêm                     (nút cao 64px, chữ 14px — P-quy tắc tuổi 45–60)
 *   trợ giảng    Việc của tôi · Phụ đạo · Ghi buổi · Thông báo · Thêm
 *   GV/admin     Lớp của tôi · Thông báo · [Quản trị] · Thêm
 *   (/tin-nhan là hộp thư "gửi cho em" — chỉ HS/SV có trong menu Thêm.)
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
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useState, useSyncExternalStore } from "react";
import { useAuth } from "@/components/auth/auth-context";
import { useTodayBadge } from "@/lib/today-badge";

const HIDDEN_PREFIXES = ["/quan-tri", "/kiem-tra/lam", "/lop-hoc/bai", "/tro-giang/ghi"];

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

type TabIconName = "home" | "class" | "practice" | "account" | "today" | "rank" | "more" | "bell" | "family" | "tasks" | "dash" | "shield";

const ICON_PATHS: Record<Exclude<TabIconName, "more">, React.ReactNode> = {
  home: (
    <>
      <path d="M3 10.5 12 3l9 7.5" />
      <path d="M5 9.5V21h14V9.5" />
    </>
  ),
  class: (
    <>
      <path d="M3 5.5h6a3 3 0 0 1 3 3V20a2.5 2.5 0 0 0-2.5-2.5H3z" />
      <path d="M21 5.5h-6a3 3 0 0 0-3 3V20a2.5 2.5 0 0 1 2.5-2.5H21z" />
    </>
  ),
  practice: (
    <>
      <path d="M4 6h9" />
      <path d="M4 12h6" />
      <path d="M4 18h5" />
      <path d="m15 15 2.5 2.5L21 13" />
    </>
  ),
  account: (
    <>
      <circle cx="12" cy="8.5" r="3.7" />
      <path d="M4.8 20a7.2 7.2 0 0 1 14.4 0" />
    </>
  ),
  today: (
    <>
      <rect x="4" y="5" width="16" height="15" rx="2.5" />
      <path d="M4 10h16" />
      <path d="M8 3v4" />
      <path d="M16 3v4" />
      <path d="m9.5 15 2 2 3.5-3.5" />
    </>
  ),
  rank: (
    <>
      <path d="M8 4h8v5a4 4 0 0 1-8 0z" />
      <path d="M8 6H4.5a3 3 0 0 0 3 4" />
      <path d="M16 6h3.5a3 3 0 0 1-3 4" />
      <path d="M12 13v4" />
      <path d="M8.5 20h7" />
    </>
  ),
  bell: (
    <>
      <path d="M6 16.5V11a6 6 0 0 1 12 0v5.5l1.5 1.5h-15z" />
      <path d="M10 20.5a2.2 2.2 0 0 0 4 0" />
    </>
  ),
  family: (
    <>
      <circle cx="8.5" cy="8" r="3" />
      <circle cx="17" cy="10" r="2.3" />
      <path d="M2.8 19.5a5.7 5.7 0 0 1 11.4 0" />
      <path d="M15 14.4a4.4 4.4 0 0 1 6.2 4.1" />
    </>
  ),
  tasks: (
    <>
      <rect x="5" y="4" width="14" height="17" rx="2.5" />
      <path d="M9 4V3h6v1" />
      <path d="M9 10h6" />
      <path d="M9 14h6" />
    </>
  ),
  dash: (
    <>
      <rect x="4" y="4" width="7" height="7" rx="1.5" />
      <rect x="13" y="4" width="7" height="7" rx="1.5" />
      <rect x="4" y="13" width="7" height="7" rx="1.5" />
      <rect x="13" y="13" width="7" height="7" rx="1.5" />
    </>
  ),
  shield: (
    <>
      <path d="M12 3 5 6v5.5c0 4.2 2.8 7.6 7 9.5 4.2-1.9 7-5.3 7-9.5V6z" />
      <path d="m9.5 12 2 2 3-3.5" />
    </>
  ),
};

/** Icon SVG inline, nét 1.7 — đồng bộ với bộ icon lucide đang dùng ở Navbar. */
function TabIcon({ name }: { name: TabIconName }) {
  return (
    <svg
      width={22}
      height={22}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={1.7}
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden
    >
      {name === "more" ? (
        <>
          <circle cx="5.5" cy="12" r="1.2" />
          <circle cx="12" cy="12" r="1.2" />
          <circle cx="18.5" cy="12" r="1.2" />
        </>
      ) : (
        ICON_PATHS[name]
      )}
    </svg>
  );
}

/**
 * Số thông báo chưa đọc (cùng RPC rẻ với NotificationBell trên Navbar, 2 phút/lần, bỏ qua khi tab ẩn).
 * services/notifications kéo theo supabase-js nên import động và chỉ chạy khi đã đăng nhập trên điện thoại.
 */
function useUnreadCount(enabled: boolean) {
  const [count, setCount] = useState(0);
  useEffect(() => {
    if (!enabled) return;
    const refresh = () => {
      if (document.visibilityState === "hidden") return;
      import("@/services/notifications").then(({ fetchUnreadCount }) => fetchUnreadCount().then(setCount).catch(() => undefined));
    };
    refresh();
    const timer = window.setInterval(refresh, 120_000);
    document.addEventListener("visibilitychange", refresh);
    return () => {
      window.clearInterval(timer);
      document.removeEventListener("visibilitychange", refresh);
    };
  }, [enabled]);
  return enabled ? count : 0;
}

/**
 * Slug lớp THPT mà học sinh đã được duyệt (vd. "lop-10") để nút "Bài học" vào thẳng lớp, không qua bộ chọn.
 * services/classes kéo theo supabase-js nên chỉ import động, và chỉ khi là học sinh THPT đã đăng nhập;
 * kết quả cache theo user trong sessionStorage để đổi trang không gọi lại.
 */
function useMyClassSlug(userId: string | null) {
  const [found, setFound] = useState<{ userId: string; slug: string } | null>(null);
  useEffect(() => {
    if (!userId) return;
    const key = `thachlab-my-class-slug:${userId}`;
    let cancelled = false;
    (async () => {
      try {
        const cached = window.sessionStorage.getItem(key);
        if (cached) {
          if (!cancelled) setFound({ userId, slug: cached });
          return;
        }
      } catch {
        /* sessionStorage bị chặn — vẫn tra bình thường */
      }
      const [{ fetchMyClassRequest, displayClassesByGrade, classGrade }, { fetchClassesStatic }] = await Promise.all([
        import("@/services/classes"),
        import("@/services/static-content"),
      ]);
      const request = await fetchMyClassRequest(userId);
      if (!request || request.status !== "active") return;
      const classes = await fetchClassesStatic();
      const grade = classGrade(request.className);
      const target = displayClassesByGrade(classes).find((c) => classGrade(c.name) === grade);
      if (!target || cancelled) return;
      setFound({ userId, slug: target.slug });
      try {
        window.sessionStorage.setItem(key, target.slug);
      } catch {
        /* bỏ qua */
      }
    })().catch(() => undefined);
    return () => {
      cancelled = true;
    };
  }, [userId]);
  return found && found.userId === userId ? found.slug : null;
}

type Badge = { kind: "dot" | "count"; count?: number };
type TabItem = { key: string; label: string; href: string; icon: TabIconName; active: boolean; badge?: Badge };
type MoreLink = { href: string; label: string };
type BarKind = "guest" | "thpt" | "cttc" | "parent" | "ta" | "staff";

const LOGOUT_LINKS = { password: { href: "/tai-khoan/doi-mat-khau", label: "Đổi mật khẩu" } };

function barKindOf(session: unknown, role: string | undefined, track: string | null | undefined): BarKind {
  if (!session) return "guest";
  if (role === "parent") return "parent";
  if (role === "tro_giang") return "ta";
  if (role === "admin" || role === "instructor") return "staff";
  return track === "cttc" ? "cttc" : "thpt";
}

function Badged({ badge, children }: { badge?: Badge; children: React.ReactNode }) {
  return (
    <span className="tab-ic">
      {children}
      {badge?.kind === "dot" && <i className="tab-dot" aria-hidden />}
      {badge?.kind === "count" && (
        <b className="tab-count" aria-hidden>
          {(badge.count ?? 0) > 99 ? "99+" : badge.count}
        </b>
      )}
    </span>
  );
}

function badgeLabel(item: TabItem) {
  if (item.badge?.kind === "count") return `${item.label}, ${item.badge.count} chưa đọc`;
  if (item.badge?.kind === "dot") return `${item.label}, có việc mới`;
  return undefined;
}

export default function MobileTabBar() {
  const pathname = usePathname();
  const router = useRouter();
  const { session, profile, signOut } = useAuth();
  const isMobile = useSyncExternalStore(subscribeViewport, isMobileViewport, () => false);
  const [moreOpen, setMoreOpen] = useState(false);

  const kind = barKindOf(session, profile?.role, profile?.track);
  const userId = session?.user.id ?? null;
  const unread = useUnreadCount(isMobile && kind !== "guest");
  const classSlug = useMyClassSlug(kind === "thpt" ? userId : null);
  const todayDot = useTodayBadge(kind === "thpt" ? userId : null);

  if (!isMobile) return null;
  if (!tabBarShownOn(pathname)) return null;

  const match = (href: string) => pathname === href || pathname.startsWith(`${href}/`);
  const countBadge: Badge | undefined = unread > 0 ? { kind: "count", count: unread } : undefined;
  const dotIfUnread: Badge | undefined = unread > 0 ? { kind: "dot" } : undefined;
  const onNotice = match("/thong-bao");

  let items: TabItem[] = [];
  let more: MoreLink[] = [];

  if (kind === "guest") {
    items = [
      { key: "home", label: "Trang chủ", href: "/", icon: "home", active: pathname === "/" },
      { key: "class", label: "Học thử", href: "/lop-hoc", icon: "class", active: match("/lop-hoc") },
      { key: "practice", label: "Luyện tập", href: "/luyen-tap", icon: "practice", active: match("/luyen-tap") },
      { key: "login", label: "Đăng nhập", href: "/dang-nhap", icon: "account", active: match("/dang-nhap") },
    ];
  } else if (kind === "thpt") {
    const onRank = match("/lop-hoc/xep-hang");
    const onResults = match("/lop-hoc/ket-qua");
    items = [
      { key: "today", label: "Hôm nay", href: "/tai-khoan", icon: "today", active: pathname === "/tai-khoan", badge: todayDot ? { kind: "dot" } : undefined },
      { key: "class", label: "Bài học", href: classSlug ? `/lop-hoc/${classSlug}` : "/lop-hoc", icon: "class", active: match("/lop-hoc") && !onRank && !onResults },
      { key: "practice", label: "Luyện tập", href: "/luyen-tap", icon: "practice", active: match("/luyen-tap") },
      { key: "rank", label: "Xếp hạng", href: "/lop-hoc/xep-hang", icon: "rank", active: onRank },
    ];
    more = [
      { href: "/lop-hoc/ket-qua", label: "Kết quả học tập" },
      { href: "/thong-bao", label: unread > 0 ? `Thông báo (${unread})` : "Thông báo" },
      { href: "/tin-nhan", label: "Tin nhắn" },
      { href: "/tin-tuc", label: "Tin tức" },
      LOGOUT_LINKS.password,
    ];
  } else if (kind === "cttc") {
    items = [
      { key: "course", label: "Khoá học", href: "/tai-khoan", icon: "today", active: pathname === "/tai-khoan" },
      { key: "class", label: "Bài học", href: "/lop-hoc/cttc", icon: "class", active: match("/lop-hoc") },
      { key: "notice", label: "Thông báo", href: "/thong-bao", icon: "bell", active: onNotice, badge: countBadge },
    ];
    more = [{ href: "/tin-nhan", label: "Tin nhắn" }, { href: "/tin-tuc", label: "Tin tức" }, LOGOUT_LINKS.password];
  } else if (kind === "parent") {
    items = [
      { key: "child", label: "Kết quả của con", href: "/phu-huynh", icon: "family", active: match("/phu-huynh") },
      { key: "notice", label: "Thông báo", href: "/thong-bao", icon: "bell", active: onNotice, badge: countBadge },
    ];
    more = [{ href: "/tai-khoan", label: "Tài khoản" }, LOGOUT_LINKS.password];
  } else if (kind === "ta") {
    const onTaOther = match("/tro-giang/phu-dao") || match("/tro-giang/ghi") || match("/tro-giang/thong-bao");
    items = [
      { key: "work", label: "Việc của tôi", href: "/tro-giang", icon: "tasks", active: match("/tro-giang") && !onTaOther },
      { key: "tutor", label: "Phụ đạo", href: "/tro-giang/phu-dao", icon: "class", active: match("/tro-giang/phu-dao") },
      { key: "log", label: "Ghi buổi", href: "/tro-giang/ghi", icon: "practice", active: match("/tro-giang/ghi") },
      { key: "notice", label: "Thông báo", href: "/tro-giang/thong-bao", icon: "bell", active: match("/tro-giang/thong-bao") },
    ];
    more = [
      { href: "/thong-bao", label: unread > 0 ? `Thông báo chung (${unread})` : "Thông báo chung" },
      { href: "/tro-giang/video", label: "Video" },
      { href: "/tro-giang/quy-che", label: "Quy chế" },
      { href: "/dashboard-thpt", label: "Quản lớp · THPT" },
      LOGOUT_LINKS.password,
    ];
  } else {
    const cttcOnly = profile?.admin_area === "cttc";
    items = [
      { key: "mine", label: "Lớp của tôi", href: cttcOnly ? "/dashboard" : "/dashboard-thpt", icon: "dash", active: match("/dashboard") || match("/dashboard-thpt") },
      { key: "notice", label: "Thông báo", href: "/thong-bao", icon: "bell", active: onNotice, badge: countBadge },
    ];
    if (profile?.role === "admin") items.push({ key: "admin", label: "Quản trị", href: "/quan-tri", icon: "shield", active: false });
    more = [{ href: "/tai-khoan", label: "Tài khoản" }, LOGOUT_LINKS.password];
  }

  const hasMore = more.length > 0;
  const moreBadge = kind === "thpt" || kind === "ta" ? dotIfUnread : undefined;
  const onMore =
    moreOpen ||
    (kind === "thpt" && (match("/lop-hoc/ket-qua") || match("/thong-bao") || match("/tin-nhan") || match("/tin-tuc")));
  const columns = items.length + (hasMore ? 1 : 0);

  return (
    <>
      {moreOpen && hasMore && (
        <>
          <button type="button" className="mobile-more-backdrop" aria-label="Đóng menu" onClick={() => setMoreOpen(false)} />
          <div className="mobile-more" role="menu" onClick={() => setMoreOpen(false)}>
            {more.map((l) => (
              <Link key={l.href} href={l.href} role="menuitem">
                {l.label}
              </Link>
            ))}
            <button type="button" role="menuitem" className="is-danger" onClick={() => void signOut().then(() => router.push("/"))}>
              Đăng xuất
            </button>
          </div>
        </>
      )}
      <nav
        className={`mobile-tabbar${kind === "parent" ? " mobile-tabbar--big" : ""}`}
        style={{ gridTemplateColumns: `repeat(${columns}, minmax(0, 1fr))` }}
        aria-label="Điều hướng nhanh"
      >
        {items.map((item) => (
          <Link
            key={item.key}
            href={item.href}
            aria-current={item.active ? "page" : undefined}
            aria-label={badgeLabel(item)}
            className={item.active ? "is-active" : undefined}
          >
            <Badged badge={item.badge}>
              <TabIcon name={item.icon} />
            </Badged>
            <span>{item.label}</span>
          </Link>
        ))}
        {hasMore && (
          <button
            type="button"
            aria-expanded={moreOpen}
            aria-label={moreBadge ? "Thêm, có thông báo chưa đọc" : undefined}
            className={onMore ? "is-active" : undefined}
            onClick={() => setMoreOpen((open) => !open)}
          >
            <Badged badge={moreBadge}>
              <TabIcon name="more" />
            </Badged>
            <span>Thêm</span>
          </button>
        )}
      </nav>
    </>
  );
}
