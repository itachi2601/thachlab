"use client";

import { Suspense, useEffect, useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { CalendarDays, Check, ChevronLeft } from "lucide-react";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import RequireAuth from "@/components/auth/RequireAuth";
import { useAuth } from "@/components/auth/AuthProvider";
import { useToast } from "@/components/ui/Toast";
import { fetchMyChildren, type LinkedChild } from "@/services/parent-links";
import {
  fetchCourse,
  fetchTaughtTopics,
  formatDate,
  formatSchedule,
  registerCourse,
  setCatchup,
  type RegisterResult,
  type TaughtTopic,
  type ThptCourse,
} from "@/services/thpt-courses";
import { supabaseConfigured } from "@/services/supabase";

const inputCls =
  "w-full rounded-xl border border-white/10 bg-white/5 px-4 py-2.5 text-white placeholder:text-slate-500 focus:border-primary focus:outline-none";

function Card({ children }: { children: React.ReactNode }) {
  return <div className="mx-auto max-w-lg rounded-3xl border border-white/10 bg-[#0B1020] p-8">{children}</div>;
}

function CourseSummary({ course }: { course: ThptCourse }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/[.03] p-4">
      <p className="text-xs font-bold uppercase tracking-[.14em] text-blue-300">Khối {course.className}</p>
      <h2 className="mt-1 font-display text-lg font-bold text-white">{course.name}</h2>
      <ul className="mt-2 space-y-1 text-sm text-slate-300">
        {course.schedules.map((s) => (
          <li key={`${s.weekday}-${s.start_time}`} className="flex items-center gap-2">
            <CalendarDays size={14} className="text-blue-300" /> {formatSchedule(s)}
          </li>
        ))}
      </ul>
      {course.starts_at && <p className="mt-2 text-xs text-slate-500">Khai giảng {formatDate(course.starts_at)}</p>}
      {course.fee_note && <p className="mt-1 text-xs text-slate-500">{course.fee_note}</p>}
    </div>
  );
}

/** Ai đang đăng ký: phụ huynh chọn con (hoặc khai con chưa có tài khoản), học sinh đăng ký cho mình. */
function RegisterForm({ course }: { course: ThptCourse }) {
  const { session, profile } = useAuth();
  const toast = useToast();
  const isStaff = profile?.role === "admin" || profile?.role === "instructor" || profile?.role === "tro_giang";
  const isParent = profile?.role === "parent";

  const [children, setChildren] = useState<LinkedChild[] | null>(isParent ? null : []);
  const [target, setTarget] = useState<string>(""); // studentId hoặc "new"
  const [childName, setChildName] = useState("");
  const [contact, setContact] = useState("");
  const [note, setNote] = useState("");
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState<RegisterResult | null>(null);
  // Lớp đã khai giảng: phần lớp đã học (bài gần nhất trước) để em tick bài đã học nơi khác.
  const [taught, setTaught] = useState<TaughtTopic[]>([]);
  const [known, setKnown] = useState<Set<number>>(new Set());
  const [catchupCount, setCatchupCount] = useState<number | null>(null);

  const started = course.starts_at ? new Date(course.starts_at) < new Date(new Date().toDateString()) : false;
  useEffect(() => {
    if (!started) return;
    fetchTaughtTopics(course.id).then(setTaught).catch(() => setTaught([]));
  }, [started, course.id]);

  useEffect(() => {
    if (!session || !isParent) return;
    fetchMyChildren(session.user.id)
      .then((rows) => {
        setChildren(rows);
        setTarget((current) => current || rows[0]?.studentId || "new");
      })
      .catch(() => {
        setChildren([]);
        setTarget("new");
      });
  }, [session, isParent]);

  if (!session) return null;

  if (isStaff)
    return (
      <Card>
        <h1 className="font-display text-xl font-bold text-white">Tài khoản giáo viên</h1>
        <p className="mt-2 text-sm text-slate-400">
          Trang này dành cho phụ huynh và học sinh. Giáo viên xem và duyệt đăng ký trong Dashboard THPT → tab Ghi danh.
        </p>
        <Link href="/dashboard-thpt" className="mt-6 flex items-center justify-center rounded-xl bg-[#2563EB] py-3 text-sm font-bold text-white">
          Mở Dashboard THPT
        </Link>
      </Card>
    );

  if (result)
    return (
      <Card>
        <Check className="mx-auto text-emerald-300" size={40} />
        <h1 className="mt-4 text-center font-display text-xl font-bold text-white">Đã gửi đăng ký</h1>
        <p className="mt-2 text-center text-sm text-slate-400">
          Đăng ký vào <strong className="text-slate-200">{result.course_name}</strong> đang chờ giáo viên duyệt. Học
          phí đóng tại trung tâm; giáo viên sẽ xác nhận sau khi nhận.
        </p>
        {result.joined_late && (
          <p className="mt-3 rounded-xl border border-amber-500/25 bg-amber-500/[.06] p-3 text-sm text-amber-100/90">
            {catchupCount === null
              ? "Lớp đã học được một phần. Giáo viên sẽ xếp buổi phụ đạo bù bài với trợ giảng trước khi vào lớp chính thức."
              : catchupCount === 0
                ? "Lớp đã học được một phần nhưng các bài đó đã học ở nơi khác — giáo viên duyệt là vào lớp luôn."
                : `Cần bù ${catchupCount} bài trước khi vào lớp chính thức. Sau khi giáo viên duyệt, mục "Bù bài" ở trang ${isParent ? "phụ huynh" : "tài khoản"} sẽ hiện các ca phụ đạo để đăng ký, bài lớp vừa học trước.`}
          </p>
        )}
        <Link
          href={isParent ? "/phu-huynh" : "/tai-khoan"}
          className="mt-6 flex items-center justify-center rounded-xl bg-[#2563EB] py-3 text-sm font-bold text-white"
        >
          {isParent ? "Về trang phụ huynh" : "Về tài khoản"}
        </Link>
      </Card>
    );

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!session) return;
    const studentId = isParent ? (target === "new" ? null : target) : session.user.id;
    if (isParent && studentId === null && !childName.trim()) {
      toast("error", "Nhập họ tên của con.");
      return;
    }
    setBusy(true);
    try {
      const res = await registerCourse({ courseId: course.id, studentId, childName, contact, note });
      if (res.joined_late && taught.length > 0) {
        try {
          const remaining = await setCatchup(res.registration_id, [...known]);
          setCatchupCount(remaining.length);
        } catch {
          // Không chặn: giáo viên vẫn sửa được danh sách bù trong tab Ghi danh.
        }
      }
      setResult(res);
    } catch (error) {
      toast("error", error instanceof Error ? error.message : "Chưa đăng ký được.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <Card>
      <h1 className="font-display text-xl font-bold text-white">Đăng ký học</h1>
      <div className="mt-4">
        <CourseSummary course={course} />
      </div>
      <form onSubmit={submit} className="mt-5 space-y-3">
        {isParent ? (
          children === null ? (
            <p className="text-sm text-slate-400">Đang tải danh sách con…</p>
          ) : (
            <>
              <label className="block text-sm text-slate-300">
                <span className="mb-1 block text-xs font-bold uppercase tracking-wide text-slate-400">Đăng ký cho</span>
                <select value={target} onChange={(e) => setTarget(e.target.value)} className={inputCls}>
                  {children.map((c) => (
                    <option key={c.studentId} value={c.studentId}>
                      {c.fullName}
                      {c.classLabel ? ` · đang ở lớp ${c.classLabel}` : ""}
                    </option>
                  ))}
                  <option value="new">Con chưa có tài khoản thachlab</option>
                </select>
              </label>
              {target === "new" && (
                <>
                  <input value={childName} onChange={(e) => setChildName(e.target.value)} placeholder="Họ và tên của con" className={inputCls} />
                  <input value={contact} onChange={(e) => setContact(e.target.value)} placeholder="Số điện thoại / Zalo liên hệ" className={inputCls} />
                  <p className="text-xs text-slate-500">
                    Giáo viên sẽ tạo tài khoản cho con và gửi mã phụ huynh để anh/chị theo dõi kết quả.
                  </p>
                </>
              )}
            </>
          )
        ) : (
          <p className="text-sm text-slate-300">
            Đăng ký cho <strong className="text-white">{profile?.full_name || session.user.email}</strong>.
          </p>
        )}
        {started && taught.length > 0 && (
          <div className="rounded-2xl border border-amber-500/25 bg-amber-500/[.05] p-4">
            <p className="text-sm font-semibold text-white">Lớp đã học tới bài dưới đây. {isParent ? "Con" : "Em"} đã học bài nào ở nơi khác rồi?</p>
            <p className="mt-1 text-xs text-slate-400">
              Bài chưa tick sẽ được phụ đạo bù trước khi vào lớp chính thức, bài lớp vừa học trước. Chưa học ở đâu thì bỏ qua.
            </p>
            <div className="mt-3 space-y-3">
              {[...new Map(taught.map((t) => [t.chapterTitle, taught.filter((x) => x.chapterTitle === t.chapterTitle)])).entries()].map(
                ([chapter, items]) => (
                  <div key={chapter}>
                    <p className="text-xs font-bold uppercase tracking-wide text-slate-500">{chapter}</p>
                    <ul className="mt-1 space-y-1">
                      {items.map((t) => (
                        <li key={t.id}>
                          <label className="flex cursor-pointer items-center gap-2 text-sm text-slate-300">
                            <input
                              type="checkbox"
                              checked={known.has(t.id)}
                              onChange={(e) =>
                                setKnown((prev) => {
                                  const next = new Set(prev);
                                  if (e.target.checked) next.add(t.id);
                                  else next.delete(t.id);
                                  return next;
                                })
                              }
                            />
                            {t.name}
                          </label>
                        </li>
                      ))}
                    </ul>
                  </div>
                ),
              )}
            </div>
            <p className="mt-3 text-xs text-amber-200/90">
              Cần bù: <strong>{taught.length - known.size}</strong>/{taught.length} bài.
            </p>
          </div>
        )}
        <textarea
          value={note}
          onChange={(e) => setNote(e.target.value)}
          placeholder="Ghi chú cho giáo viên (đã học ở đâu, mong muốn…) — không bắt buộc"
          rows={3}
          className={inputCls}
        />
        <button
          type="submit"
          disabled={busy || (isParent && children === null)}
          className="w-full rounded-xl bg-[#2563EB] py-3 text-sm font-bold text-white disabled:opacity-40"
        >
          {busy ? "Đang gửi…" : "Gửi đăng ký"}
        </button>
      </form>
    </Card>
  );
}

function Loader() {
  const searchParams = useSearchParams();
  const id = Number(searchParams.get("id"));
  const [course, setCourse] = useState<ThptCourse | null | undefined>(undefined);

  useEffect(() => {
    // id không hợp lệ -> fetchCourse trả null qua cùng một đường, không setState đồng bộ trong effect.
    const load = !id || Number.isNaN(id) ? Promise.resolve(null) : fetchCourse(id);
    load.then(setCourse).catch(() => setCourse(null));
  }, [id]);

  if (course === undefined) return <Card><p className="text-center text-slate-400">Đang tải…</p></Card>;
  if (course === null)
    return (
      <Card>
        <h1 className="font-display text-xl font-bold text-white">Không tìm thấy khoá học</h1>
        <p className="mt-2 text-sm text-slate-400">Khoá có thể đã đóng đăng ký. Xem các lớp đang mở ở trang Đăng ký học.</p>
        <Link href="/khoa-hoc" className="mt-6 flex items-center justify-center rounded-xl bg-[#2563EB] py-3 text-sm font-bold text-white">
          Xem lớp đang mở
        </Link>
      </Card>
    );

  return (
    <RequireAuth>
      <RegisterForm course={course} />
    </RequireAuth>
  );
}

export default function DangKyKhoaHocPage() {
  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-4xl px-5 pb-16 pt-28">
        <Link href="/khoa-hoc" className="mb-6 inline-flex items-center gap-1.5 text-sm text-slate-400 hover:text-white">
          <ChevronLeft size={16} /> Các lớp đang mở
        </Link>
        {!supabaseConfigured ? (
          <p className="text-center text-slate-400">Hệ thống đang được cấu hình.</p>
        ) : (
          <Suspense fallback={<Card><p className="text-center text-slate-400">Đang tải…</p></Card>}>
            <Loader />
          </Suspense>
        )}
      </main>
      <Footer />
    </>
  );
}
