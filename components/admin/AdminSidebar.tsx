"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const SECTIONS = [
  {
    title: "Nội dung học",
    items: [
      { href: "/quan-tri/bai-hoc", label: "Bài học" },
      { href: "/quan-tri/lms-cnc", label: "LMS CNC" },
      { href: "/quan-tri/de-kiem-tra", label: "Đề kiểm tra" },
      { href: "/quan-tri/import-word", label: "Import từ Word" },
      { href: "/quan-tri/import-de", label: "Import đề" },
    ],
  },
  {
    title: "Vận hành lớp",
    items: [
      { href: "/quan-tri/khoa-hoc", label: "Khóa học theo môn" },
      { href: "/quan-tri/lop-hoc", label: "Lớp học" },
      { href: "/quan-tri/thi-truc-tiep", label: "Thi trực tiếp CNC" },
      { href: "/quan-tri/tin-nhan", label: "Tin nhắn" },
    ],
  },
  {
    title: "Kết quả",
    items: [{ href: "/quan-tri/bang-diem", label: "Bảng điểm" }],
  },
  {
    title: "Khác",
    items: [{ href: "/quan-tri/bai-dang", label: "Bài đăng" }],
  },
] as const;

export default function AdminSidebar() {
  const pathname = usePathname();

  return (
    <nav className="w-full shrink-0 lg:w-60">
      <div className="space-y-5 lg:sticky lg:top-28">
        {SECTIONS.map((section) => (
          <div key={section.title}>
            <p className="px-1 text-xs font-bold uppercase tracking-wider text-slate-500 lg:px-3">{section.title}</p>
            <div className="mt-2 flex flex-wrap gap-1.5 lg:flex-col lg:gap-1">
              {section.items.map((item) => {
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
          </div>
        ))}
      </div>
    </nav>
  );
}
