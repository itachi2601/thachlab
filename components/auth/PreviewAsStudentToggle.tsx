"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { Drama, LogOut, Wrench } from "lucide-react";
import { useAuth } from "@/components/auth/AuthProvider";
import { useTaDemoMode } from "@/lib/tro-giang/demo";

/**
 * Nút nổi cho admin: "Xem như học sinh" -> AuthProvider ghi đè profile.role thành
 * "student" (chỉ trên trình duyệt, không đổi session/đăng nhập thật). Học sinh giả lập
 * dùng chính user_id của admin nên vào /tai-khoan sẽ thấy màn "Bạn đang học ở đâu?"
 * (vì tài khoản admin không thuộc lớp/khóa nào) — bấm THPT hoặc CTTC ở đó để xem tiếp
 * từng luồng giao diện, giống hệt học sinh mới vào.
 *
 * "Xem như học sinh CTTC" làm y hệt nhưng đi thẳng vào /lop-hoc/cttc, bỏ qua bước chọn
 * luồng học — dùng để xem nhanh giao diện phía CTTC (vd. nút mở điểm danh của cán bộ lớp).
 */
export default function PreviewAsStudentToggle() {
  const router = useRouter();
  const { realProfile, previewAsStudent, setPreviewAsStudent } = useAuth();
  const [taDemo] = useTaDemoMode();

  if (realProfile?.role !== "admin") return null;
  // Đang xem giả lập trợ giảng — banner của chế độ đó chiếm chỗ này rồi.
  if (taDemo) return null;

  if (!previewAsStudent) {
    return (
      <div className="fixed bottom-5 left-5 z-50 flex flex-col items-start gap-2">
        <button
          type="button"
          onClick={() => setPreviewAsStudent(true)}
          className="flex items-center gap-2 rounded-full border border-white/15 bg-[#0B1020]/95 px-4 py-2.5 text-xs font-bold text-slate-200 shadow-xl backdrop-blur-md hover:border-white/30"
        >
          <Drama size={15} className="text-fuchsia-300" />
          Xem như học sinh
        </button>
        <button
          type="button"
          onClick={() => {
            setPreviewAsStudent(true);
            router.push("/lop-hoc/cttc");
          }}
          className="flex items-center gap-2 rounded-full border border-orange-400/25 bg-[#0B1020]/95 px-4 py-2.5 text-xs font-bold text-orange-200 shadow-xl backdrop-blur-md hover:border-orange-400/40"
        >
          <Wrench size={15} className="text-orange-300" />
          Xem như học sinh CTTC
        </button>
      </div>
    );
  }

  return (
    <div className="fixed bottom-5 left-5 z-50 flex flex-wrap items-center gap-2 rounded-full border border-fuchsia-400/30 bg-[#0B1020]/95 px-4 py-2.5 text-xs font-bold text-fuchsia-200 shadow-xl backdrop-blur-md">
      <Drama size={15} />
      Đang xem giao diện học sinh (giả lập)
      <Link
        href="/tai-khoan"
        className="rounded-full bg-fuchsia-500/15 px-2.5 py-1 text-fuchsia-100 hover:bg-fuchsia-500/25"
      >
        Vào /tai-khoan
      </Link>
      <Link
        href="/lop-hoc/cttc"
        className="rounded-full bg-orange-500/15 px-2.5 py-1 text-orange-100 hover:bg-orange-500/25"
      >
        Vào CTTC
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
