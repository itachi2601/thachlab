"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/components/auth/AuthProvider";

const AREA_LABEL = { thpt: "THPT", cttc: "CTTC" } as const;
type Area = keyof typeof AREA_LABEL;

const AREA_ITEMS: Record<Area, { href: string; label: string }[]> = {
  thpt: [
    { href: "/quan-tri/bai-hoc", label: "Bài học" },
    { href: "/quan-tri/lop-hoc", label: "Lớp học" },
    { href: "/quan-tri/bang-diem", label: "Bảng điểm" },
  ],
  cttc: [
    { href: "/quan-tri/lms-cnc", label: "LMS CNC" },
    { href: "/quan-tri/khoa-hoc", label: "Khóa học theo môn" },
    { href: "/quan-tri/tinh-trang-may", label: "Tình trạng máy" },
    { href: "/quan-tri/thi-truc-tiep", label: "Thi trực tiếp CNC" },
  ],
};

const AREA_ENTRY_HREF: Record<Area, string> = {
  thpt: "/quan-tri/bai-hoc",
  cttc: "/quan-tri/lms-cnc",
};

const SHARED_ITEMS = [
  { href: "/quan-tri/phan-cong-giang-vien", label: "Phân công giảng viên" },
  { href: "/quan-tri/tin-nhan", label: "Tin nhắn" },
  { href: "/quan-tri/bai-dang", label: "Bài đăng" },
];

function SidebarLinks({ items, pathname }: { items: { href: string; label: string }[]; pathname: string }) {
  return (
    <div className="mt-2 flex flex-wrap gap-1.5 lg:flex-col lg:gap-1">
      {items.map((item) => {
        const active = pathname === item.href;
        return (
          <Link
            key={item.href}
            href={item.href}
            className={`rounded-full px-4 py-2 text-sm font-semibold transition-colors lg:w-full lg:rounded-xl lg:px-3 lg:text-left ${
              active
                ? "bg-[#2563EB] text-white"
                : "bg-white/5 text-slate-300 hover:bg-white/10 lg:bg-transparent lg:hover:bg-white/5"
            }`}
          >
            {item.label}
          </Link>
        );
      })}
    </div>
  );
}

// area = null khi đang ở 1 trong 3 trang dùng chung (không thuộc riêng THPT hay CTTC).
export default function AdminSidebar({ area }: { area: Area | null }) {
  const pathname = usePathname();
  const { profile } = useAuth();
  // Giảng viên chỉ được phân công đúng 1 khu vực — không có gì để "đổi khu vực" hay xem mục dùng chung.
  const isRestrictedInstructor = profile?.role === "instructor" && !!profile.admin_area;

  return (
    <nav className="w-full shrink-0 lg:w-60">
      <div className="space-y-5 lg:sticky lg:top-28">
        {!isRestrictedInstructor && (
          <Link
            href="/quan-tri"
            className="inline-block px-1 text-xs font-semibold text-slate-500 hover:text-slate-300 lg:px-3"
          >
            ← Đổi khu vực
          </Link>
        )}

        {area && (
          <div>
            <p className="px-1 text-xs font-bold uppercase tracking-wider text-slate-500 lg:px-3">
              {AREA_LABEL[area]}
            </p>
            <SidebarLinks items={AREA_ITEMS[area]} pathname={pathname} />
          </div>
        )}

        {!isRestrictedInstructor && (
          <div>
            <p className="px-1 text-xs font-bold uppercase tracking-wider text-slate-500 lg:px-3">
              Dùng chung
            </p>
            <SidebarLinks items={SHARED_ITEMS} pathname={pathname} />
          </div>
        )}

        {!isRestrictedInstructor && (
          <div className="flex flex-col gap-1 px-1 lg:px-3">
            {(["thpt", "cttc"] as const)
              .filter((other) => other !== area)
              .map((other) => (
                <Link
                  key={other}
                  href={AREA_ENTRY_HREF[other]}
                  className="text-xs font-semibold text-[#60A5FA] hover:text-[#93C5FD]"
                >
                  → Quản trị {AREA_LABEL[other]}
                </Link>
              ))}
          </div>
        )}
      </div>
    </nav>
  );
}
