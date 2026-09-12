"use client";

import Link from "next/link";
import { Drama, LogOut } from "lucide-react";
import { useAuth } from "@/components/auth/AuthProvider";

/**
 * Nút nổi cho admin: "Xem như học sinh" -> AuthProvider ghi đè profile.role thành
 * "student" (chỉ trên trình duyệt, không đổi session/đăng nhập thật). Học sinh giả lập
 * dùng chính user_id của admin nên vào /tai-khoan sẽ thấy màn "Bạn đang học ở đâu?"
 * (vì tài khoản admin không thuộc lớp/khóa nào) — bấm THPT hoặc CTTC ở đó để xem tiếp
 * từng luồng giao diện, giống hệt học sinh mới vào.
 */
export default function PreviewAsStudentToggle() {
  const { realProfile, previewAsStudent, setPreviewAsStudent } = useAuth();

  if (realProfile?.role !== "admin") return null;

  if (!previewAsStudent) {
    return (
      <button
        type="button"
        onClick={() => setPreviewAsStudent(true)}
        className="fixed bottom-5 left-5 z-50 flex items-center gap-2 rounded-full border border-white/15 bg-[#0B1020]/95 px-4 py-2.5 text-xs font-bold text-slate-200 shadow-xl backdrop-blur-md hover:border-white/30"
      >
        <Drama size={15} className="text-fuchsia-300" />
        Xem như học sinh
      </button>
    );
  }

  return (
    <div className="fixed bottom-5 left-5 z-50 flex items-center gap-2 rounded-full border border-fuchsia-400/30 bg-[#0B1020]/95 px-4 py-2.5 text-xs font-bold text-fuchsia-200 shadow-xl backdrop-blur-md">
      <Drama size={15} />
      Đang xem giao diện học sinh (giả lập)
      <Link
        href="/tai-khoan"
        className="rounded-full bg-fuchsia-500/15 px-2.5 py-1 text-fuchsia-100 hover:bg-fuchsia-500/25"
      >
        Vào /tai-khoan
      </Link>
      <button
        type="button"
        onClick={() => setPreviewAsStudent(false)}
        className="flex items-center gap-1 rounded-full border border-white/15 px-2.5 py-1 text-slate-300 hover:border-white/30"
      >
        <LogOut size={12} /> Thoát
      </button>
    </div>
  );
}
