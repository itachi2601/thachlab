"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { ArrowRight, GraduationCap, Wrench } from "lucide-react";
import { useAuth } from "@/components/auth/AuthProvider";
import RequireAuth from "@/components/auth/RequireAuth";

const AREA_ENTRY: Record<"thpt" | "cttc", string> = {
  thpt: "/quan-tri/bai-hoc",
  cttc: "/quan-tri/lms-cnc",
};

export default function AdminChooserPage() {
  const { profile, loading } = useAuth();
  const router = useRouter();
  const restrictedArea = profile?.role === "instructor" ? profile.admin_area : null;

  // Giảng viên chỉ được phân công 1 khu vực thì vào thẳng khu đó, không thấy màn hình chọn.
  useEffect(() => {
    if (loading || !restrictedArea) return;
    router.replace(AREA_ENTRY[restrictedArea]);
  }, [loading, restrictedArea, router]);

  if (loading || restrictedArea) {
    return <p className="text-sm text-slate-400">Đang chuyển hướng…</p>;
  }

  return (
    <RequireAuth restrictToAdmin>
      <div className="space-y-6">
        <p className="text-sm text-slate-400">Chọn khu vực quản trị.</p>
        <div className="grid gap-4 sm:grid-cols-2">
          <Link
            href="/quan-tri/bai-hoc"
            className="group flex items-center gap-4 rounded-2xl border border-blue-400/20 bg-blue-500/[0.06] p-6 transition hover:border-blue-400/40 hover:bg-blue-500/10"
          >
            <span className="grid h-12 w-12 shrink-0 place-items-center rounded-xl bg-blue-500/15 text-blue-300">
              <GraduationCap size={24} />
            </span>
            <div className="flex-1">
              <strong className="block text-lg text-white">Quản trị THPT</strong>
              <span className="text-sm text-slate-400">Bài học, lớp học, bảng điểm Vật lý 9–12</span>
            </div>
            <ArrowRight size={18} className="shrink-0 text-blue-300 opacity-0 transition group-hover:opacity-100" />
          </Link>
          <Link
            href="/quan-tri/lms-cnc"
            className="group flex items-center gap-4 rounded-2xl border border-orange-400/20 bg-orange-500/[0.06] p-6 transition hover:border-orange-400/40 hover:bg-orange-500/10"
          >
            <span className="grid h-12 w-12 shrink-0 place-items-center rounded-xl bg-orange-500/15 text-orange-300">
              <Wrench size={24} />
            </span>
            <div className="flex-1">
              <strong className="block text-lg text-white">Quản trị CTTC</strong>
              <span className="text-sm text-slate-400">LMS CNC, khóa học, tình trạng máy, thi trực tiếp</span>
            </div>
            <ArrowRight size={18} className="shrink-0 text-orange-300 opacity-0 transition group-hover:opacity-100" />
          </Link>
        </div>

        <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">
          <p className="text-xs font-bold uppercase tracking-wider text-slate-500">Dùng chung cho cả hai khu vực</p>
          <div className="mt-3 flex flex-wrap gap-2">
            <Link href="/quan-tri/phan-cong-giang-vien" className="rounded-full border border-white/10 px-4 py-2 text-sm font-semibold text-slate-300 hover:border-white/30 hover:text-white">
              Phân công giảng viên
            </Link>
            <Link href="/quan-tri/tin-nhan" className="rounded-full border border-white/10 px-4 py-2 text-sm font-semibold text-slate-300 hover:border-white/30 hover:text-white">
              Tin nhắn
            </Link>
            <Link href="/quan-tri/bai-dang" className="rounded-full border border-white/10 px-4 py-2 text-sm font-semibold text-slate-300 hover:border-white/30 hover:text-white">
              Bài đăng
            </Link>
          </div>
        </div>
      </div>
    </RequireAuth>
  );
}
