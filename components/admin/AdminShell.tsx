"use client";

import { useState, useSyncExternalStore } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { ArrowUpRight, ChevronDown, ExternalLink, LogOut, Menu, X } from "lucide-react";
import { useAuth } from "@/components/auth/AuthProvider";
import ThemeToggle from "@/components/layout/ThemeToggle";
import AdminSearch from "@/components/admin/AdminSearch";
import {
  AREA_ITEMS,
  AREA_LABEL,
  OVERVIEW_ITEM,
  SHARED_ITEMS,
  areaOfPath,
  titleOfPath,
  type AdminArea,
  type AdminNavItem,
} from "@/components/admin/nav";

function NavLink({ item, pathname, onNavigate }: { item: AdminNavItem; pathname: string; onNavigate: () => void }) {
  // "Tổng quan" (/quan-tri) chỉ sáng khi ở đúng trang đó, không sáng cho mọi trang con.
  const active =
    pathname === item.href || (item.href !== "/quan-tri" && pathname.startsWith(`${item.href}/`));
  const Icon = item.icon;
  return (
    <Link
      href={item.href}
      onClick={onNavigate}
      className={`admin-side-link ${active && !item.external ? "is-active" : ""}`}
    >
      <Icon size={16} />
      <span>{item.label}</span>
      {item.external && <ExternalLink size={13} className="admin-side-ext" />}
    </Link>
  );
}

const COLLAPSE_KEY = "thachlab-admin-nav-collapsed";

function parseCollapsed(raw: string | null): string[] {
  try {
    const parsed: unknown = JSON.parse(raw ?? "[]");
    return Array.isArray(parsed) ? parsed.filter((v): v is string => typeof v === "string") : [];
  } catch {
    return [];
  }
}

function readCollapsed(): string[] {
  try {
    return parseCollapsed(localStorage.getItem(COLLAPSE_KEY));
  } catch {
    return [];
  }
}

// Chuỗi thô trong localStorage — ổn định giữa các lần render nên dùng được cho useSyncExternalStore.
function readCollapsedRaw(): string {
  try {
    return localStorage.getItem(COLLAPSE_KEY) ?? "[]";
  } catch {
    return "[]";
  }
}

function subscribeCollapsed(listener: () => void): () => void {
  window.addEventListener("storage", listener);
  return () => window.removeEventListener("storage", listener);
}

function NavGroup({
  label,
  tone,
  items,
  pathname,
  onNavigate,
}: {
  label: string;
  tone?: AdminArea;
  items: AdminNavItem[];
  pathname: string;
  onNavigate: () => void;
}) {
  // Nhóm gập lại được, nhớ lựa chọn; nhóm đang chứa trang hiện tại luôn mở để không mất dấu đang ở đâu.
  const storedCollapsed = useSyncExternalStore(subscribeCollapsed, readCollapsedRaw, () => "[]");
  const [override, setOverride] = useState<{ label: string; collapsed: boolean } | null>(null);
  const collapsed =
    override?.label === label ? override.collapsed : parseCollapsed(storedCollapsed).includes(label);
  const hasCurrent = items.some((item) => pathname === item.href || pathname.startsWith(`${item.href}/`));
  const hidden = collapsed && !hasCurrent;

  function toggle() {
    const next = !collapsed;
    setOverride({ label, collapsed: next });
    try {
      const rest = readCollapsed().filter((v) => v !== label);
      localStorage.setItem(COLLAPSE_KEY, JSON.stringify(next ? [...rest, label] : rest));
    } catch {
      /* chế độ riêng tư: bỏ qua, chỉ không nhớ được */
    }
  }

  return (
    <div className="admin-side-group">
      <button
        type="button"
        onClick={toggle}
        aria-expanded={!hidden}
        className={`admin-side-label flex w-full items-center gap-1 text-left ${tone ? `admin-side-label--${tone}` : ""}`}
      >
        {tone && <i />}
        <span className="flex-1">{label}</span>
        <ChevronDown size={13} className={`transition-transform ${hidden ? "-rotate-90" : ""}`} />
      </button>
      {!hidden && items.map((item) => <NavLink key={item.href} item={item} pathname={pathname} onNavigate={onNavigate} />)}
    </div>
  );
}

export default function AdminShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const { profile, signOut } = useAuth();
  // Đổi trang thì đóng ngăn kéo trên điện thoại: trạng thái mở gắn với trang lúc mở.
  const [drawer, setDrawer] = useState<{ path: string; open: boolean }>({ path: pathname, open: false });
  const open = drawer.open && drawer.path === pathname;

  const isAdmin = profile?.role === "admin";
  // Giảng viên chỉ được phân công đúng 1 khu vực — chỉ thấy khu đó, không thấy mục dùng chung.
  const restrictedArea = profile?.role === "instructor" ? profile.admin_area : null;
  const showNav = isAdmin || !!restrictedArea;
  const area = areaOfPath(pathname) ?? restrictedArea;
  const closeDrawer = () => setDrawer({ path: pathname, open: false });

  const areas: AdminArea[] = restrictedArea ? [restrictedArea] : ["thpt", "cttc"];
  const initial = (profile?.full_name ?? "?").trim().charAt(0).toUpperCase();

  return (
    <div className={`admin-shell ${open ? "is-open" : ""}`} data-area={area ?? "thpt"}>
      {showNav && (
        <>
          <div className="admin-scrim" onClick={closeDrawer} aria-hidden />
          <nav className="admin-side" aria-label="Điều hướng quản trị">
            <Link href="/quan-tri" className="admin-side-brand" onClick={closeDrawer}>
              <span className="admin-side-mark">TL</span>
              <span className="min-w-0">
                <span className="admin-side-name">ThachLab</span>
                <span className="admin-side-tag">Quản trị</span>
              </span>
            </Link>

            <div className="admin-side-scroll">
              {!restrictedArea && (
                <div className="admin-side-group">
                  <NavLink item={OVERVIEW_ITEM} pathname={pathname} onNavigate={closeDrawer} />
                </div>
              )}

              {areas.map((key) => (
                <NavGroup
                  key={key}
                  label={AREA_LABEL[key]}
                  tone={key}
                  items={AREA_ITEMS[key]}
                  pathname={pathname}
                  onNavigate={closeDrawer}
                />
              ))}

              {!restrictedArea && (
                <NavGroup label="Dùng chung" items={SHARED_ITEMS} pathname={pathname} onNavigate={closeDrawer} />
              )}
            </div>

            <div className="admin-side-foot">
              <div className="admin-side-user">
                <span className="admin-side-avatar">{initial}</span>
                <span className="min-w-0">
                  <b>{profile?.full_name ?? "Tài khoản"}</b>
                  <small>{isAdmin ? "Quản trị viên" : `Giảng viên · ${AREA_LABEL[restrictedArea!]}`}</small>
                </span>
              </div>
              <Link href="/" className="admin-side-act" onClick={closeDrawer}>
                <ArrowUpRight size={15} /> Về trang chủ
              </Link>
              <button type="button" className="admin-side-act admin-side-act--danger" onClick={() => void signOut()}>
                <LogOut size={15} /> Đăng xuất
              </button>
            </div>
          </nav>
        </>
      )}

      <div className="admin-main">
        <header className="admin-top">
          {showNav && (
            <button
              type="button"
              className="admin-burger"
              onClick={() => setDrawer({ path: pathname, open: !open })}
              aria-label={open ? "Đóng menu" : "Mở menu"}
            >
              {open ? <X size={18} /> : <Menu size={18} />}
            </button>
          )}
          <div className="admin-top-titles">
            <p className="admin-top-crumb">{area ? AREA_LABEL[area] : "Quản trị"}</p>
            <h1 className="admin-top-title">{titleOfPath(pathname)}</h1>
          </div>
          <div className="admin-top-acts">
            {showNav && <AdminSearch />}
            <ThemeToggle />
          </div>
        </header>
        <div className="admin-content">{children}</div>
      </div>
    </div>
  );
}
