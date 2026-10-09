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
  fetchCourses,
  fetchPairCourses,
  fetchTaughtTopics,
  formatDate,
  formatSchedule,
  pairSlotLabel,
  pairSlots,
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
  return <div className="mx-auto max-w-lg rounded-3xl border border-white/10 bg-panel p-8">{children}</div>;
}

/** Tóm tắt lớp đang đăng ký: khoá đơn in tên khoá; lớp 2 buổi/tuần in tên lớp + từng buổi đã chọn (A, B). */
function CourseSummary({ courses }: { courses: ThptCourse[] }) {
  const first = courses[0];
  const paired = !!first.pairKey;
  return (
    <div className="rounded-2xl border border-white/10 bg-white/[.03] p-4">
      <p className="text-xs font-bold uppercase tracking-[.14em] text-blue-300">Khối {first.className}</p>
      <h2 className="mt-1 font-display text-lg font-bold text-white">{paired ? first.pairKey : first.name}</h2>
      {paired && <p className="mt-1 text-xs text-slate-400">Học {courses.length} buổi mỗi tuần.</p>}
      <ul className="mt-2 space-y-1 text-sm text-slate-300">
        {courses.flatMap((c) =>
          c.schedules.map((s) => (
            <li key={`${c.id}-${s.weekday}-${s.start_time}`} className="flex items-center gap-2">
              <CalendarDays size={14} className="text-blue-300" />
              {c.pairSlot && <span className="font-semibold text-white">{pairSlotLabel(c.pairSlot)} ·</span>}
              {formatSchedule(s)}
            </li>
          )),
        )}
      </ul>
      {first.starts_at && <p className="mt-2 text-xs text-slate-500">Khai giảng {formatDate(first.starts_at)}</p>}
      {first.fee_note && <p className="mt-1 text-xs text-slate-500">{first.fee_note}</p>}
    </div>
  );
}

/** Ai đang đăng ký: phụ huynh chọn con (hoặc khai con chưa có tài khoản), học sinh đăng ký cho mình. */
function RegisterForm({ courses }: { courses: ThptCourse[] }) {
  // Lớp 2 buổi/tuần: cùng khối, cùng chương trình → phần "lớp đã học tới" và bù bài tính theo khoá đầu.
  const course = courses[0];
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
  const [result, setResult] = useState<RegisterResult[] | null>(null);
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
        <Link href="/dashboard-thpt" className="mt-6 flex items-center justify-center rounded-xl bg-primary py-3 text-sm font-bold text-white">
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
          Đăng ký vào{" "}
          <strong className="text-slate-200">{course.pairKey ?? result.map((r) => r.course_name).join(", ")}</strong>
          {course.pairKey ? ` (${result.length} buổi/tuần)` : ""} đang chờ giáo viên duyệt. Học phí đóng tại trung
          tâm; giáo viên sẽ xác nhận sau khi nhận.
        </p>
        {result.some((r) => r.joined_late) && (
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
          className="mt-6 flex items-center justify-center rounded-xl bg-primary py-3 text-sm font-bold text-white"
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
    const done: RegisterResult[] = [];
    try {
      // Lớp 2 buổi/tuần = 2 lượt ghi danh (buổi A rồi buổi B). RPC hiện nhận một khoá mỗi lần; nếu buổi sau
      // lỗi (hết chỗ…) thì buổi trước vẫn đã ghi — báo rõ để giáo viên xếp tay, không âm thầm bỏ.
      for (const c of courses) {
        const res = await registerCourse({ courseId: c.id, studentId, childName, contact, note });
        done.push(res);
        if (res.joined_late && taught.length > 0) {
          try {
            const remaining = await setCatchup(res.registration_id, [...known]);
            setCatchupCount(remaining.length);
          } catch {
            // Không chặn: giáo viên vẫn sửa được danh sách bù trong tab Ghi danh.
          }
        }
      }
      setResult(done);
    } catch (error) {
      const msg = error instanceof Error ? error.message : "Chưa đăng ký được.";
      if (done.length > 0) {
        const failed = courses[done.length];
        toast(
          "error",
          `Đã ghi ${done.map((r) => r.course_name).join(", ")}; ${failed?.pairSlot ? `buổi ${failed.pairSlot}` : "buổi còn lại"} chưa được: ${msg} Nhắn giáo viên để xếp buổi.`,
        );
        setResult(done);
      } else toast("error", msg);
    } finally {
      setBusy(false);
    }
  }

  return (
    <Card>
      <h1 className="font-display text-xl font-bold text-white">Đăng ký học</h1>
      <div className="mt-4">
        <CourseSummary courses={courses} />
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
          className="w-full rounded-xl bg-primary py-3 text-sm font-bold text-white disabled:opacity-40"
        >
          {busy ? "Đang gửi…" : "Gửi đăng ký"}
        </button>
      </form>
    </Card>
  );
}

/**
 * Kiểm bộ khoá đã chọn. Khoá đơn: đúng 1 id. Lớp 2 buổi/tuần (pairKey): phải có đúng MỘT khoá cho MỖI loại
 * buổi đang mở của lớp (A và B), không trộn lớp khác. Trả về câu báo lỗi, null = hợp lệ.
 */
function validateSelection(selected: ThptCourse[], pairAll: ThptCourse[]): string | null {
  if (selected.length === 0) return "Chưa chọn lớp.";
  const keys = new Set(selected.map((c) => c.pairKey ?? `#${c.id}`));
  if (keys.size > 1) return "Mỗi lần chỉ đăng ký một lớp. Quay lại trang Đăng ký học và chọn lại.";
  const first = selected[0];
  if (!first.pairKey) return selected.length === 1 ? null : "Mỗi lần chỉ đăng ký một lớp.";
  const required = pairSlots(pairAll);
  const chosen = selected.map((c) => c.pairSlot ?? "");
  const ok = required.length === chosen.length && required.every((slot) => chosen.filter((x) => x === slot).length === 1);
  if (ok) return null;
  const words = required.map((slot) => `một buổi ${slot}`).join(" và ");
  return `Lớp ${first.pairKey} học ${required.length} buổi mỗi tuần: cần chọn ${words}. Quay lại trang Đăng ký học để chọn đủ.`;
}

function Loader() {
  const searchParams = useSearchParams();
  // ?id=5&id=7 (lớp 2 buổi/tuần) hoặc ?id=1 (khoá đơn). Chuỗi hoá để effect không chạy lại vô ích.
  const idsKey = [...new Set(searchParams.getAll("id").map(Number).filter((n) => Number.isInteger(n) && n > 0))].join(",");
  const [state, setState] = useState<{ courses: ThptCourse[]; problem: string | null } | null | undefined>(undefined);

  useEffect(() => {
    const ids = idsKey ? idsKey.split(",").map(Number) : [];
    let cancelled = false;
    // Không có id → đi cùng đường promise (không setState đồng bộ trong effect).
    (async () => {
      if (ids.length === 0) return null;
      const courses = await fetchCourses(ids);
      if (courses.length === 0) return null;
      const pairAll = courses[0].pairKey ? await fetchPairCourses(courses[0]) : courses;
      return { courses, problem: validateSelection(courses, pairAll) };
    })()
      .then((r) => {
        if (!cancelled) setState(r);
      })
      .catch(() => {
        if (!cancelled) setState(null);
      });
    return () => {
      cancelled = true;
    };
  }, [idsKey]);

  if (state === undefined) return <Card><p className="text-center text-slate-400">Đang tải…</p></Card>;
  if (state === null)
    return (
      <Card>
        <h1 className="font-display text-xl font-bold text-white">Không tìm thấy khoá học</h1>
        <p className="mt-2 text-sm text-slate-400">Khoá có thể đã đóng đăng ký. Xem các lớp đang mở ở trang Đăng ký học.</p>
        <Link href="/khoa-hoc" className="mt-6 flex items-center justify-center rounded-xl bg-primary py-3 text-sm font-bold text-white">
          Xem lớp đang mở
        </Link>
      </Card>
    );
  if (state.problem)
    return (
      <Card>
        <h1 className="font-display text-xl font-bold text-white">Chưa chọn đủ buổi</h1>
        <p className="mt-2 text-sm text-slate-400">{state.problem}</p>
        <Link href="/khoa-hoc" className="mt-6 flex items-center justify-center rounded-xl bg-primary py-3 text-sm font-bold text-white">
          Chọn lại buổi học
        </Link>
      </Card>
    );

  return (
    <RequireAuth>
      <RegisterForm courses={state.courses} />
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
      <Footer variant="app" />
    </>
  );
}
