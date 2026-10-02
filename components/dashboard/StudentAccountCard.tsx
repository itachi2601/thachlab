"use client";

import { useEffect, useState } from "react";
import { Copy } from "lucide-react";
import { useToast } from "@/components/ui/Toast";
import { fetchStudentAccount, type StudentAccountInfo } from "@/services/student-account";

const GENDER_LABEL: Record<string, string> = { male: "Nam", female: "Nữ", other: "Khác", nam: "Nam", nu: "Nữ", "nữ": "Nữ" };

function fmtDate(value: string | null, withTime = false) {
  if (!value) return null;
  const d = new Date(value);
  if (Number.isNaN(d.getTime())) return value;
  return withTime ? d.toLocaleString("vi-VN") : d.toLocaleDateString("vi-VN");
}

/**
 * Thẻ "Thông tin tài khoản" trong hồ sơ học sinh: username, email, SĐT, ngày sinh… cho admin/GV phụ trách.
 * Mật khẩu mã hoá một chiều nên không đọc lại được — dùng thẻ "Mật khẩu" bên dưới để đặt lại.
 */
export default function StudentAccountCard({ studentId }: { studentId: string }) {
  const toast = useToast();
  const [info, setInfo] = useState<StudentAccountInfo | null | undefined>(undefined);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;
    fetchStudentAccount(studentId)
      .then((row) => { if (!cancelled) setInfo(row); })
      .catch((e) => { if (!cancelled) { setError(e instanceof Error ? e.message : "Lỗi."); setInfo(null); } });
    return () => { cancelled = true; };
  }, [studentId]);

  async function copy(text: string) {
    try {
      await navigator.clipboard.writeText(text);
      toast("success", "Đã chép.");
    } catch {
      toast("error", "Trình duyệt không cho chép tự động — bôi đen rồi chép tay nhé.");
    }
  }

  const rows: [string, string | null | undefined][] = info
    ? [
        ["Username đăng nhập", info.username],
        ["Email đăng nhập (hệ thống)", info.login_email],
        ["Email liên hệ", info.contact_email],
        ["Số điện thoại", info.phone],
        ["SĐT phụ huynh", info.parent_phone],
        ["Ngày sinh", fmtDate(info.birth_date)],
        ["Giới tính", info.gender ? GENDER_LABEL[info.gender.toLowerCase()] ?? info.gender : null],
        ["Mã học sinh", info.student_code],
        ["Tạo tài khoản", fmtDate(info.created_at, true)],
        ["Đăng nhập gần nhất", info.last_sign_in_at ? fmtDate(info.last_sign_in_at, true) : "Chưa từng đăng nhập"],
      ]
    : [];

  return (
    <section className="rounded-2xl border border-white/10 bg-panel p-5">
      <h4 className="font-display text-lg font-bold text-white">Thông tin tài khoản</h4>
      {info === undefined && <p className="mt-3 text-sm text-slate-500">Đang tải…</p>}
      {info === null && (
        <p className="mt-3 text-sm text-red-300">
          {error || "Không có dữ liệu."} {error.includes("staff_student_account") && "(Chưa chạy migration 20261002110000.)"}
        </p>
      )}
      {info && (
        <>
          <dl className="mt-3 grid gap-x-6 gap-y-2 sm:grid-cols-2">
            {rows.map(([label, value]) => (
              <div key={label} className="min-w-0 text-sm">
                <dt className="text-xs font-bold uppercase tracking-wide text-slate-500">{label}</dt>
                <dd className="mt-0.5 flex items-center gap-1.5 break-all text-white">
                  {value || <span className="text-slate-600">Chưa có</span>}
                  {value && (label.includes("mail") || label.includes("Username") || label.includes("SĐT") || label.includes("điện thoại")) && (
                    <button type="button" aria-label={`Chép ${label}`} onClick={() => copy(value)} className="shrink-0 text-slate-500 hover:text-white">
                      <Copy size={13} />
                    </button>
                  )}
                </dd>
              </div>
            ))}
          </dl>
          <p className="mt-4 rounded-xl border border-white/10 bg-white/[.02] p-3 text-xs text-slate-400">
            <strong className="text-slate-300">Mật khẩu</strong> được mã hoá một chiều nên không ai xem lại được.
            {info.from_roster && info.student_code
              ? " Tài khoản này tạo từ danh sách Excel: mật khẩu ban đầu là mã học sinh, nếu em chưa tự đổi."
              : ""}{" "}
            Cần thì đặt lại ở thẻ &quot;Mật khẩu&quot; bên dưới.
          </p>
        </>
      )}
    </section>
  );
}
