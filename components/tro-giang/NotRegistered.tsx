import { AlertTriangle } from "lucide-react";

/** Màn hình cho tài khoản đã đăng nhập nhưng không có hàng trong ta_assistants. */
export default function NotRegistered({ note }: { note?: string }) {
  return (
    <div className="rounded-3xl border border-dashed border-white/10 bg-panel p-10 text-center">
      <AlertTriangle className="mx-auto text-amber-300" size={36} />
      <h1 className="mt-4 font-display text-xl font-bold text-white">
        Tài khoản này chưa được đăng ký làm trợ giảng
      </h1>
      <p className="mt-2 text-sm text-slate-400">
        {note ?? "Liên hệ giáo viên để được thêm vào danh sách trợ giảng."}
      </p>
    </div>
  );
}
