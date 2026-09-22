"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { ChevronDown, Users } from "lucide-react";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import RequireAuth from "@/components/auth/RequireAuth";
import { useAuth } from "@/components/auth/AuthProvider";
import StudentResultsDashboard from "@/components/results/StudentResultsDashboard";
import { fetchMyChildren, type LinkedChild } from "@/services/parent-links";
import { supabaseConfigured } from "@/services/supabase";

function Notice({ children }: { children: React.ReactNode }) {
  return (
    <div className="mx-auto max-w-xl rounded-2xl border border-white/10 bg-[#0B1020] p-8 text-center text-slate-300">
      {children}
    </div>
  );
}

/**
 * Trang phụ huynh: chọn con (nếu nối nhiều em) rồi xem đúng bảng kết quả em thấy ở
 * /lop-hoc/ket-qua, đổi cách xưng hô. Không có gì để ghi — mọi quyền chỉ là đọc.
 */
function ParentHome() {
  const { session } = useAuth();
  const [children, setChildren] = useState<LinkedChild[] | null>(null);
  const [selectedId, setSelectedId] = useState<string | null>(null);

  useEffect(() => {
    if (!session) return;
    fetchMyChildren(session.user.id)
      .then((rows) => {
        setChildren(rows);
        setSelectedId((current) => current ?? rows[0]?.studentId ?? null);
      })
      .catch(() => setChildren([]));
  }, [session]);

  if (children === null) return <Notice>Đang tải…</Notice>;

  if (children.length === 0)
    return (
      <Notice>
        <Users className="mx-auto text-slate-500" size={36} />
        <h1 className="mt-4 font-display text-xl font-bold text-white">Chưa nối với học sinh nào</h1>
        <p className="mt-2 text-sm text-slate-400">
          Tài khoản này chưa được gắn với con. Nhờ giáo viên chủ nhiệm tạo mã phụ huynh cho con
          (dạng <code className="text-slate-300">PH1A2B3C</code>) rồi mở link{" "}
          <code className="text-slate-300">/loi-moi?ma=PH…</code> để nối.
        </p>
        <Link
          href="/tai-khoan"
          className="mt-6 inline-flex items-center justify-center rounded-xl border border-white/15 px-5 py-2.5 text-sm font-semibold text-slate-200"
        >
          Về tài khoản
        </Link>
      </Notice>
    );

  const selected = children.find((c) => c.studentId === selectedId) ?? children[0];

  return (
    <div className="mx-auto w-full max-w-4xl">
      {children.length > 1 && (
        <div className="mb-6 flex flex-wrap items-center gap-3">
          <span className="text-sm text-slate-400">Đang xem:</span>
          <label className="relative">
            <select
              value={selected.studentId}
              onChange={(e) => setSelectedId(e.target.value)}
              className="appearance-none rounded-xl border border-white/10 bg-[#0B1020] py-2 pl-4 pr-10 text-sm font-semibold text-white focus:border-primary focus:outline-none"
            >
              {children.map((c) => (
                <option key={c.studentId} value={c.studentId}>
                  {c.fullName}
                  {c.classLabel ? ` · lớp ${c.classLabel}` : ""}
                </option>
              ))}
            </select>
            <ChevronDown size={16} className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-slate-500" />
          </label>
        </div>
      )}
      {selected.classId === null && (
        <p className="mb-6 rounded-2xl border border-amber-500/25 bg-amber-500/[.06] p-4 text-sm text-amber-100/90">
          {selected.fullName} chưa được duyệt vào khối lớp nào trên thachlab, nên chưa có hạng trong lớp.
        </p>
      )}
      <StudentResultsDashboard
        key={selected.studentId}
        studentId={selected.studentId}
        viewer="parent"
        title={selected.fullName}
      />
    </div>
  );
}

export default function PhuHuynhPage() {
  return (
    <>
      <Navbar />
      <main className="min-h-screen w-full px-6 pb-20 pt-28">
        {!supabaseConfigured ? (
          <p className="text-center text-slate-400">Hệ thống đang được cấu hình.</p>
        ) : (
          <RequireAuth>
            <ParentHome />
          </RequireAuth>
        )}
      </main>
      <Footer />
    </>
  );
}
