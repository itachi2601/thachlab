"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { CalendarPlus, ChevronDown, Users } from "lucide-react";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import RequireAuth from "@/components/auth/RequireAuth";
import { useAuth } from "@/components/auth/AuthProvider";
import StudentResultsDashboard from "@/components/results/StudentResultsDashboard";
import CatchupCard from "@/components/results/CatchupCard";
import { fetchMyChildren, type LinkedChild } from "@/services/parent-links";
import { fetchMyRegistrations, REGISTRATION_STATUS_LABEL, type MyRegistration } from "@/services/thpt-courses";
import { supabaseConfigured } from "@/services/supabase";

function Notice({ children }: { children: React.ReactNode }) {
  return (
    <div className="mx-auto max-w-xl rounded-2xl border border-white/10 bg-[#0B1020] p-8 text-center text-slate-300">
      {children}
    </div>
  );
}

const REG_TONE: Record<MyRegistration["status"], string> = {
  pending: "text-amber-300",
  catchup: "text-amber-300",
  active: "text-emerald-300",
  rejected: "text-red-300",
  left: "text-slate-500",
};

/** Các đăng ký học (của con đã nối, hoặc con chưa có tài khoản) và trạng thái duyệt. */
function RegistrationList({ items }: { items: MyRegistration[] }) {
  if (items.length === 0) return null;
  return (
    <section className="mb-6 rounded-2xl border border-white/10 bg-[#0B1020] p-5 text-left">
      <h2 className="font-display font-semibold text-white">Đăng ký học</h2>
      <ul className="mt-3 space-y-2">
        {items.map((r) => (
          <li key={r.id} className="flex flex-wrap items-center gap-2 rounded-xl bg-white/[.02] px-3 py-2 text-sm">
            <span className="min-w-0 flex-1">
              <span className="block font-semibold text-white">{r.courseName}</span>
              <span className="block text-xs text-slate-400">
                {r.student_id === null ? `${r.child_name} (chưa có tài khoản)` : r.studentName}
                {r.className ? ` · khối ${r.className}` : ""}
                {r.joined_late ? " · vào trễ, sẽ bù bài" : ""}
              </span>
            </span>
            <span className={`text-xs font-bold ${REG_TONE[r.status]}`}>{REGISTRATION_STATUS_LABEL[r.status]}</span>
          </li>
        ))}
      </ul>
    </section>
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
  const [registrations, setRegistrations] = useState<MyRegistration[]>([]);

  useEffect(() => {
    if (!session) return;
    fetchMyRegistrations().then(setRegistrations).catch(() => setRegistrations([]));
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
        <RegistrationList items={registrations} />
        <div className="mt-6 flex flex-wrap justify-center gap-3">
          <Link
            href="/khoa-hoc"
            className="inline-flex items-center gap-2 rounded-xl bg-[#2563EB] px-5 py-2.5 text-sm font-bold text-white"
          >
            <CalendarPlus size={16} /> Đăng ký học cho con
          </Link>
          <Link
            href="/tai-khoan"
            className="inline-flex items-center justify-center rounded-xl border border-white/15 px-5 py-2.5 text-sm font-semibold text-slate-200"
          >
            Về tài khoản
          </Link>
        </div>
      </Notice>
    );

  const selected = children.find((c) => c.studentId === selectedId) ?? children[0];
  const selectedRegistrations = registrations.filter((r) => r.student_id === selected.studentId || r.student_id === null);

  return (
    <div className="mx-auto w-full max-w-4xl">
      <div className="mb-6 flex flex-wrap items-center gap-3 rounded-2xl border border-white/10 bg-[#0B1020] px-5 py-3">
        <span className="text-sm text-slate-300">Muốn con học thêm lớp khác hoặc đăng ký cho em nhỏ?</span>
        <Link href="/khoa-hoc" className="ml-auto inline-flex items-center gap-2 rounded-xl bg-[#2563EB] px-4 py-2 text-sm font-bold text-white">
          <CalendarPlus size={15} /> Đăng ký học
        </Link>
      </div>
      <RegistrationList items={selectedRegistrations} />
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
      <div className="mb-6">
        <CatchupCard key={`catchup-${selected.studentId}`} studentId={selected.studentId} classId={selected.classId} viewer="parent" />
      </div>
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
