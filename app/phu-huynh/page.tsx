"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { CalendarPlus, ChevronDown, Users } from "lucide-react";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import RequireAuth from "@/components/auth/RequireAuth";
import ReadingZone from "@/components/ui/ReadingZone";
import { useAuth } from "@/components/auth/AuthProvider";
import StudentResultsDashboard from "@/components/results/StudentResultsDashboardLazy";
import ParentChildCards from "@/components/parent/ParentChildCardsLazy";
import ParentFaq from "@/components/parent/ParentFaq";
import ParentGuestLanding from "@/components/parent/ParentGuestLanding";
import TeacherContact from "@/components/parent/TeacherContact";
import ParentTuitionCard from "@/components/parent/ParentTuitionCard";
import { fetchCoursesByIds } from "@/services/parent-view";
import type { ThptCourse } from "@/services/thpt-courses-public";
import { fetchMyChildren, type LinkedChild } from "@/services/parent-links";
import { fetchMyRegistrations, REGISTRATION_STATUS_LABEL, type MyRegistration } from "@/services/thpt-courses";
import { supabaseConfigured } from "@/services/supabase";

/**
 * Trang phụ huynh — người đọc chính là cha/mẹ 45–60 tuổi (docs/QUY-TAC-THIET-KE-PHU-HUYNH.md).
 * Khác trang học sinh ở 4 điểm, có chủ ý:
 *   - Thứ tự: trả lời "con học thế nào" trước, việc phụ (đăng ký lớp khác, xem thành tích) xuống cuối (P7).
 *   - Liên hệ thầy ở cả đầu và cuối trang, dạng gọi điện/Zalo chứ không phải form (P10, P18).
 *   - Chữ to hơn và tương phản cao hơn (P1, P2) — qua class .parent-page ở app/globals.css.
 *   - Không có gì ghi: mọi quyền của phụ huynh đều là đọc.
 */
function Notice({ children }: { children: React.ReactNode }) {
  return (
    <div className="mx-auto max-w-xl rounded-2xl border border-line bg-panel p-8 text-center text-ink">
      {children}
    </div>
  );
}

const REG_TONE: Record<MyRegistration["status"], string> = {
  pending: "text-warn",
  catchup: "text-warn",
  active: "text-ok",
  rejected: "text-danger",
  left: "text-muted",
};

/**
 * Đăng ký học của con đang chờ duyệt / bị từ chối / đã nghỉ. Đăng ký đã duyệt (active) không hiện:
 * nó không còn là việc phải làm, mà lại chiếm chỗ của phần kết quả học tập (N3, P7).
 */
function RegistrationList({ items }: { items: MyRegistration[] }) {
  const needAttention = items.filter((r) => r.status !== "active");
  if (needAttention.length === 0) return null;
  return (
    <section className="mb-6 rounded-2xl border border-line bg-panel p-5">
      <h2 className="font-display text-lg font-semibold text-ink">Đăng ký học</h2>
      <ul className="mt-3 space-y-2">
        {needAttention.map((r) => (
          <li key={r.id} className="flex flex-wrap items-center gap-2 rounded-xl bg-surface-2 px-3 py-2">
            <span className="min-w-0 flex-1">
              <span className="block font-semibold text-ink">{r.courseName}</span>
              <span className="block text-muted">
                {r.student_id === null ? `${r.child_name} (chưa có tài khoản)` : r.studentName}
                {r.className ? ` · khối ${r.className}` : ""}
                {r.joined_late ? " · vào trễ, sẽ bù bài" : ""}
              </span>
            </span>
            <span className={`font-bold ${REG_TONE[r.status]}`}>{REGISTRATION_STATUS_LABEL[r.status]}</span>
          </li>
        ))}
      </ul>
    </section>
  );
}

/** Chưa nối với con nào: phụ huynh cần biết xin mã ở đâu — nút gọi/Zalo phải nằm ngay đây (P9, P10). */
function NoChildYet({ registrations }: { registrations: MyRegistration[] }) {
  return (
    <Notice>
      <Users className="mx-auto text-muted" size={36} />
      <h1 className="mt-4 font-display text-xl font-bold text-ink">Tài khoản này chưa nối với con</h1>
      <p className="mt-3 text-left text-muted">
        Thầy cần gửi phụ huynh một <b>link mời</b> (dạng{" "}
        <code className="rounded bg-surface-2 px-1.5 py-0.5 text-ink">/loi-moi?ma=PH…</code>) để
        tài khoản này nối với con. Nhắn Zalo hoặc gọi thầy, cho biết tên con đang học.
      </p>
      <RegistrationList items={registrations} />
      <div className="mt-5 flex flex-wrap justify-center gap-3">
        <Link
          href="/khoa-hoc"
          className="inline-flex items-center gap-2 rounded-xl border border-line px-5 py-2.5 font-semibold text-ink hover:border-line-strong"
        >
          <CalendarPlus size={16} /> Đăng ký học cho con
        </Link>
        <Link
          href="/tai-khoan"
          className="inline-flex items-center justify-center rounded-xl border border-line px-5 py-2.5 font-semibold text-ink hover:border-line-strong"
        >
          Về tài khoản
        </Link>
      </div>
    </Notice>
  );
}

/**
 * Phụ huynh đã đăng nhập: chọn con (nếu nối nhiều em) rồi xem đúng số liệu con thấy ở
 * /lop-hoc/ket-qua, đổi cách xưng hô. Phần "tóm tắt cho phụ huynh" nằm trong dashboard (nó cần
 * dữ liệu điểm đã tải ở đó — không gọi thêm Supabase lần nào).
 */
function ParentHome() {
  const { session } = useAuth();
  const [children, setChildren] = useState<LinkedChild[] | null>(null);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [registrations, setRegistrations] = useState<MyRegistration[]>([]);
  const [courses, setCourses] = useState<ThptCourse[]>([]);

  useEffect(() => {
    if (!session) return;
    fetchMyRegistrations()
      .then((rows) => {
        setRegistrations(rows);
        // Lịch học + ghi chú học phí của các khoá con đang học (1 request, dùng cho "Sắp tới" và "Học phí").
        const ids = rows.filter((r) => r.status === "active" || r.status === "catchup").map((r) => r.course_id);
        return fetchCoursesByIds(ids).then(setCourses);
      })
      .catch(() => setRegistrations([]));
    fetchMyChildren(session.user.id)
      .then((rows) => {
        setChildren(rows);
        setSelectedId((current) => current ?? rows[0]?.studentId ?? null);
      })
      .catch(() => setChildren([]));
  }, [session]);

  if (children === null) return <Notice>Đang tải kết quả của con…</Notice>;

  if (children.length === 0) return <NoChildYet registrations={registrations} />;

  const selected = children.find((c) => c.studentId === selectedId) ?? children[0];
  const selectedRegistrations = registrations.filter(
    (r) => r.student_id === selected.studentId || r.student_id === null,
  );
  const selectedCourses = courses.filter((c) =>
    selectedRegistrations.some((r) => r.course_id === c.id && (r.status === "active" || r.status === "catchup")),
  );

  return (
    <div className="mx-auto w-full max-w-4xl">
      <div className="mb-5 flex flex-wrap items-center gap-x-4 gap-y-2">
        {children.length > 1 && (
          <>
            <label htmlFor="chon-con" className="font-semibold text-ink">
              Chọn con:
            </label>
            <span className="relative">
              <select
                id="chon-con"
                value={selected.studentId}
                onChange={(e) => setSelectedId(e.target.value)}
                className="appearance-none rounded-xl border border-line-strong bg-panel py-2.5 pl-4 pr-10 font-semibold text-ink focus:border-primary focus:outline-none"
              >
                {children.map((c) => (
                  <option key={c.studentId} value={c.studentId}>
                    {c.fullName}
                    {c.classLabel ? ` · lớp ${c.classLabel}` : ""}
                  </option>
                ))}
              </select>
              <ChevronDown
                size={18}
                className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-muted"
              />
            </span>
          </>
        )}
        {selected.classLabel && (
          <span className="rounded-full border border-line px-3 py-1 font-semibold text-ink">
            Lớp {selected.classLabel}
          </span>
        )}
      </div>

      <TeacherContact variant="slim" className="mb-6" />

      {selected.classId === null && (
        <p className="parent-copy mb-6 rounded-2xl border border-amber-500/25 bg-amber-500/[.06] p-4 text-warn">
          {selected.fullName} chưa được thầy duyệt vào lớp trên thachlab, nên chưa có điểm và chưa có
          hạng trong lớp. Phụ huynh nhắn thầy nếu con đã đi học mà vẫn thấy dòng này.
        </p>
      )}

      <StudentResultsDashboard
        key={selected.studentId}
        studentId={selected.studentId}
        viewer="parent"
        title={`Con: ${selected.fullName}`}
        afterSummary={
          selected.classId !== null ? (
            <ParentChildCards
              key={selected.studentId}
              studentId={selected.studentId}
              classId={selected.classId}
              courses={selectedCourses}
            />
          ) : null
        }
      />

      <div className="mt-8 space-y-6">
        <ParentTuitionCard registrations={selectedRegistrations} courses={selectedCourses} />
        <RegistrationList items={selectedRegistrations} />

        <section className="flex flex-wrap items-center gap-3 rounded-2xl border border-line bg-panel px-5 py-4">
          <span className="text-ink">Muốn đăng ký cho con học lớp khác, hoặc cho em nhỏ?</span>
          <Link
            href="/khoa-hoc"
            className="ml-auto inline-flex items-center gap-2 rounded-xl bg-primary px-5 py-3 font-semibold text-white hover:bg-primary-dark"
          >
            <CalendarPlus size={18} /> Xem lớp đang mở
          </Link>
        </section>

        <TeacherContact />
        <ParentFaq />
      </div>
    </div>
  );
}

export default function PhuHuynhPage() {
  return (
    <>
      <Navbar />
      <main className="parent-page min-h-screen w-full px-5 pb-20 pt-28 sm:px-6">
        {!supabaseConfigured ? (
          <p className="text-center text-muted">Hệ thống đang được cấu hình.</p>
        ) : (
          <RequireAuth
            loginHref="/dang-nhap?next=/phu-huynh"
            showSignUp={false}
            guestWide
            guestHideAuthRow
            guestNotice={<ParentGuestLanding />}
          >
            <ReadingZone plainLabels>
              <ParentHome />
            </ReadingZone>
          </RequireAuth>
        )}
      </main>
      <Footer variant="parent" />
    </>
  );
}
