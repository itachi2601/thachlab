"use client";

import { Fragment, Suspense, useEffect, useState } from "react";
import { ArrowLeft, ArrowRight, Check, ChevronDown } from "lucide-react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import { SkeletonGrid } from "@/components/ui/Skeleton";
import type { SchoolClass } from "@/features/exams/types";
import { DIFFICULTY_LABELS } from "@/features/exams/types";
import {
  LESSON_KIND_META,
  isPeriodicExam,
  isSemesterExam,
  type Chapter,
  type Lesson,
} from "@/features/lessons/types";
import {
  classGrade,
  displayClassesByGrade,
  expandClassIdsByGrade,
  fetchClasses,
} from "@/services/classes";
import { fetchChapters, fetchLessonProgressSummaries, fetchLessons } from "@/services/lessons";
import {
  fetchPublishedExams,
  fetchPublishedPosts,
  visibleTo,
  type ExamMeta,
  type PostMeta,
} from "@/services/content";
import { useAuth } from "@/components/auth/AuthProvider";
import { supabaseConfigured } from "@/services/supabase";
import { academicSubject, subjectsForGrade } from "@/services/academic-subjects";
import type { InlineLessonProgress } from "@/components/lessons/InlineLessonAccordion";
import MistakeReviewPanel from "@/components/lessons/MistakeReviewPanel";

const LAST_LESSON_KEY = "thachlab-last-secondary-lesson";

const GRADE_IMAGES: Record<string, string> = {
  "9": "/images/learning-path/khtn-9.jpg",
  "10": "/images/learning-path/vat-ly-10.jpg",
  "11": "/images/learning-path/vat-ly-11.jpg",
  "12": "/images/learning-path/vat-ly-12.jpg",
};
const GRADE_LABELS: Record<string, string> = { "9": "KHTN 9" };
const GRADE_ORDER = ["10", "11", "12", "9"];
const GRADE_DETAILS: Record<string, { description: string; accent: string }> = {
  "10": { description: "Xây nền tảng cơ học", accent: "text-blue-300 border-blue-400/30 hover:border-blue-300 bg-blue-500/10" },
  "11": { description: "Dao động, sóng và điện", accent: "text-violet-300 border-violet-400/30 hover:border-violet-300 bg-violet-500/10" },
  "12": { description: "Củng cố kiến thức, ôn thi", accent: "text-orange-300 border-orange-400/30 hover:border-orange-300 bg-orange-500/10" },
  "9": { description: "Kiến thức nền tảng Khoa học tự nhiên", accent: "text-emerald-300 border-emerald-400/30 hover:border-emerald-300 bg-emerald-500/10" },
};
const CLASS_TABS = [
  { id: "secondary", label: "THPT – THCS" },
  { id: "university", label: "CTTC" },
] as const;
const UNIVERSITY_CLASSES = [
  {
    title: "Vật lý đại cương",
    icon: "⚙️",
    description: "Nền tảng cơ học, nhiệt, điện từ và các mô hình vật lý ứng dụng.",
    href: "",
  },
  {
    title: "Gia công CNC",
    icon: "🛠️",
    description: "Quy trình, thông số cắt, lập trình và vận hành gia công CNC.",
    href: "/lop-hoc/cnc",
  },
  {
    title: "Tiện – Phay truyền thống",
    icon: "🔧",
    description: "Điểm danh, chọn máy và theo dõi 5S khi thực hành tại Xưởng C1.1.",
    href: "/lop-hoc/tien-phay",
  },
  {
    title: "Công nghệ chế tạo máy",
    icon: "🏭",
    description: "Kiến thức về phôi, dụng cụ, nguyên công và tổ chức sản xuất cơ khí.",
    href: "",
  },
  {
    title: "Anh văn chuyên ngành cơ khí",
    icon: "📘",
    description: "Từ vựng, đọc hiểu tài liệu kỹ thuật và giao tiếp trong ngành cơ khí.",
    href: "",
  },
];

export default function ClassHubPage({ classSlug }: { classSlug?: string } = {}) {
  return <Suspense fallback={<div className="mx-auto max-w-6xl px-6 pt-28"><SkeletonGrid count={3} /></div>}>
    <ClassHubContent classSlug={classSlug} />
  </Suspense>;
}

function ClassHubContent({ classSlug }: { classSlug?: string }) {
  const { session } = useAuth();
  const searchParams = useSearchParams();
  const activeTab = searchParams.get("tab") === "cttc" ? "university" : "secondary";
  const router = useRouter();
  const [classes, setClasses] = useState<SchoolClass[] | null>(null);
  const [activeId, setActiveId] = useState<number | null>(null);
  const [activeSubjectCode, setActiveSubjectCode] = useState("vat-ly");
  const [requestedChapterId, setRequestedChapterId] = useState<number | null>(null);
  const [collapsedChapters, setCollapsedChapters] = useState<Set<number>>(new Set());
  const [lastLessonId, setLastLessonId] = useState<number | null>(null);
  const [lessonProgress, setLessonProgress] = useState<Map<number, InlineLessonProgress>>(new Map());
  const [chapters, setChapters] = useState<Chapter[] | null>(null);
  const [lessons, setLessons] = useState<Lesson[] | null>(null);
  const [exams, setExams] = useState<ExamMeta[] | null>(null);
  const [posts, setPosts] = useState<PostMeta[] | null>(null);

  useEffect(() => {
    const savedLessonId = Number(window.localStorage.getItem(LAST_LESSON_KEY));
    if (savedLessonId > 0) setLastLessonId(savedLessonId);
    const requestedSubject = new URLSearchParams(window.location.search).get("subject");
    if (["vat-ly", "hoa-hoc", "sinh-hoc"].includes(requestedSubject ?? "")) {
      setActiveSubjectCode(requestedSubject!);
    }
    const chapterParam = Number(new URLSearchParams(window.location.search).get("chapter"));
    if (chapterParam > 0) setRequestedChapterId(chapterParam);

    if (!supabaseConfigured) return;
    fetchClasses().then((cs) => {
      setClasses(cs);
      if (classSlug) {
        const selectedClass = cs.find((item) => item.slug === classSlug);
        setActiveId(selectedClass?.id ?? null);
      }
    });
    fetchChapters().then(setChapters);
    fetchLessons().then(setLessons);
    fetchPublishedPosts().then(setPosts);
  }, [classSlug]);

  // đề thi yêu cầu đăng nhập (RLS) — chỉ tải khi có session
  useEffect(() => {
    if (!supabaseConfigured || !session) return;
    fetchPublishedExams().then(setExams);
  }, [session]);

  useEffect(() => {
    if (!session || !lessons?.length) return;
    fetchLessonProgressSummaries(session.user.id, lessons.map((lesson) => lesson.id))
      .then(setLessonProgress)
      .catch(() => setLessonProgress(new Map()));
  }, [session, lessons]);

  const effectiveSlug = classSlug;
  const active = classes?.find((c) =>
    effectiveSlug ? c.slug === effectiveSlug : c.id === activeId,
  );
  const subjectCode = classGrade(active?.name ?? "") === "9" ? activeSubjectCode : "vat-ly";
  const activeDisplayName = active
    ? classGrade(active.name) === "9"
      ? `KHTN 9 · ${academicSubject(subjectCode).label}`
      : `Vật lý ${classGrade(active.name) ?? active.name}`
    : undefined;
  const displayClasses = classes ? displayClassesByGrade(classes) : [];
  const visibleClassIds = classes && active ? expandClassIdsByGrade([active.id], classes) : null;
  const classChapters = (chapters ?? []).filter(
    (ch) => visibleTo(ch.classIds, visibleClassIds) && ch.subjectCode === subjectCode,
  );
  const classPosts = (posts ?? []).filter(
    (p) => visibleTo(p.classIds, visibleClassIds) && p.subjectCode === subjectCode,
  );
  const classExams = (exams ?? []).filter(
    (e) => visibleTo(e.classIds, visibleClassIds) && e.subjectCode === subjectCode,
  );
  const visibleLessonIds = new Set(classChapters.map((chapter) => chapter.id));
  const lastLesson = (lessons ?? []).find((lesson) => lesson.id === lastLessonId && visibleLessonIds.has(lesson.chapter_id)) ?? null;
  const lastLessonChapter = lastLesson ? classChapters.find((chapter) => chapter.id === lastLesson.chapter_id) ?? null : null;

  function lessonHref(lesson: Lesson) {
    const params = new URLSearchParams({
      id: String(lesson.id),
      subject: subjectCode,
      chapter: String(lesson.chapter_id),
    });
    if (effectiveSlug) params.set("class", effectiveSlug);
    return `/lop-hoc/bai?${params.toString()}`;
  }

  function continueLesson(lesson: Lesson) {
    setLastLessonId(lesson.id);
    window.localStorage.setItem(LAST_LESSON_KEY, String(lesson.id));
    router.push(lessonHref(lesson));
  }

  useEffect(() => {
    if (!requestedChapterId || !classes || !chapters) return;
    if (classSlug) {
      setCollapsedChapters((prev) => {
        if (!prev.has(requestedChapterId)) return prev;
        const next = new Set(prev);
        next.delete(requestedChapterId);
        return next;
      });
      return;
    }
    const requestedChapter = chapters.find((chapter) => chapter.id === requestedChapterId);
    const targetClassId = requestedChapter?.classIds[0];
    if (targetClassId) {
      const targetClass = classes.find((item) => item.id === targetClassId);
      const representative = targetClass
        ? displayClassesByGrade(classes).find(
            (item) => classGrade(item.name) === classGrade(targetClass.name),
          )
        : undefined;
      setActiveId(representative?.id ?? targetClassId);
    }
  }, [chapters, classSlug, classes, requestedChapterId]);

  useEffect(() => {
    if (!requestedChapterId || !lessons) return;
    const timer = window.setTimeout(() => {
      document
        .getElementById(`chapter-${requestedChapterId}`)
        ?.scrollIntoView({ behavior: "smooth", block: "start" });
    }, 80);
    return () => window.clearTimeout(timer);
  }, [activeId, lessons, requestedChapterId]);
  function toggleChapter(chapterId: number) {
    setCollapsedChapters((prev) => {
      const next = new Set(prev);
      if (next.has(chapterId)) next.delete(chapterId);
      else next.add(chapterId);
      return next;
    });
  }

  function rememberLesson(lesson: Lesson) {
    setLastLessonId(lesson.id);
    window.localStorage.setItem(LAST_LESSON_KEY, String(lesson.id));
  }

  // Trang của một lớp: mục lục chương → bài, cùng ngôn ngữ với trang bài học.
  if (effectiveSlug) {
    const grade = active ? classGrade(active.name) : null;
    const lastPercent = lastLesson
      ? (() => {
          const p = lessonProgress.get(lastLesson.id);
          return p?.total ? Math.round((p.completed / p.total) * 100) : null;
        })()
      : null;
    return (
      <>
        <Navbar />
        <main className="min-h-screen w-full pt-[76px]">
          <div className="lesson-shell">
            <div className="lesson-main lesson-main--single">
              <Link href="/lop-hoc" className="lesson-back">
                <ArrowLeft size={15} /> Lớp học
              </Link>

              {!supabaseConfigured ? (
                <p className="lesson-notice">Hệ thống đang được cấu hình.</p>
              ) : !classes ? (
                <div className="pt-8"><SkeletonGrid count={2} /></div>
              ) : !active ? (
                <p className="lesson-notice">Không tìm thấy lớp học này.</p>
              ) : (
                <>
                  <header className="lesson-head">
                    <p className="lesson-eyebrow">{grade === "9" ? "Trung học cơ sở" : "Trung học phổ thông"}</p>
                    <h1>{activeDisplayName}</h1>
                    {grade === "9" && (
                      <div className="class-subjects" role="tablist" aria-label="Môn học">
                        {subjectsForGrade("9").map((subject) => (
                          <button
                            key={subject.code}
                            type="button"
                            role="tab"
                            aria-selected={activeSubjectCode === subject.code}
                            onClick={() => {
                              setActiveSubjectCode(subject.code);
                              setCollapsedChapters(new Set());
                            }}
                            className={activeSubjectCode === subject.code ? "is-active" : ""}
                          >
                            {subject.label}
                          </button>
                        ))}
                      </div>
                    )}
                  </header>

                  {!chapters || !lessons ? (
                    <SkeletonGrid count={2} />
                  ) : classChapters.length === 0 ? (
                    <p className="lesson-muted">Chưa có chương trình học cho lớp này.</p>
                  ) : (
                    <div className="class-toc">
                      {lastLesson && lastLessonChapter && (
                        <div className="class-continue">
                          <div>
                            <p className="lesson-eyebrow">Tiếp tục học</p>
                            <p className="lesson-block-title">{lastLesson.title}</p>
                            <p className="lesson-block-sub">
                              {lastLessonChapter.title}
                              {lastPercent !== null && ` · ${lastPercent}%`}
                            </p>
                          </div>
                          <button type="button" className="lesson-btn" onClick={() => continueLesson(lastLesson)}>
                            Tiếp tục <ArrowRight size={15} />
                          </button>
                        </div>
                      )}
                      <MistakeReviewPanel />

                      {classChapters.map((ch, chapterIndex) => {
                        // Kiểm tra giữa/cuối học kì không nằm trong nội dung chương:
                        // tách ra khỏi danh sách bài, hiện thành mục riêng ngay sau chương.
                        const chapterLessons = lessons.filter(
                          (l) => l.chapter_id === ch.id && !isSemesterExam(l.lesson_kind),
                        );
                        const semesterExams = lessons.filter(
                          (l) => l.chapter_id === ch.id && isSemesterExam(l.lesson_kind),
                        );
                        const chapterTotal = chapterLessons.reduce((sum, lesson) => sum + (lessonProgress.get(lesson.id)?.total ?? lesson.itemCount), 0);
                        const chapterCompleted = chapterLessons.reduce((sum, lesson) => sum + (lessonProgress.get(lesson.id)?.completed ?? 0), 0);
                        const collapsed = collapsedChapters.has(ch.id);
                        let lessonNumber = 0;
                        return (
                          <Fragment key={ch.id}>
                            <section id={`chapter-${ch.id}`} className="class-chapter">
                              <button
                                type="button"
                                className="class-chapter-head"
                                onClick={() => toggleChapter(ch.id)}
                                aria-expanded={!collapsed}
                                aria-controls={`chapter-lessons-${ch.id}`}
                              >
                                <span className="class-num">{chapterIndex + 1}</span>
                                <span className="class-chapter-title">{ch.title}</span>
                                {session && chapterTotal > 0 && (
                                  <span className="class-meta">{chapterCompleted}/{chapterTotal}</span>
                                )}
                                <ChevronDown size={17} className={collapsed ? "" : "rotate-180"} />
                              </button>
                              {!collapsed && (
                                <ol id={`chapter-lessons-${ch.id}`} className="class-lessons">
                                  {chapterLessons.length === 0 && (
                                    <li className="lesson-muted">Chưa có bài học trong chương này.</li>
                                  )}
                                  {chapterLessons.map((lesson) => {
                                    const progress = lessonProgress.get(lesson.id);
                                    const percent = progress?.total
                                      ? Math.round((progress.completed / progress.total) * 100)
                                      : 0;
                                    const periodic = isPeriodicExam(lesson.lesson_kind);
                                    if (!periodic) lessonNumber += 1;
                                    const complete = !!session && percent === 100;
                                    return (
                                      <li key={lesson.id}>
                                        <Link
                                          href={lessonHref(lesson)}
                                          onClick={() => rememberLesson(lesson)}
                                          className={`class-lesson ${complete ? "is-complete" : ""}`}
                                        >
                                          <span className={`class-num ${periodic ? "class-num--exam" : ""}`}>
                                            {complete ? <Check size={13} /> : periodic ? "KT" : lessonNumber}
                                          </span>
                                          <span className="class-lesson-title">{lesson.title}</span>
                                          <span className="class-meta">
                                            {periodic
                                              ? session ? (complete ? "Đã làm" : "Chưa làm") : "Kiểm tra"
                                              : session ? `${percent}%` : `${lesson.itemCount} mục`}
                                          </span>
                                        </Link>
                                      </li>
                                    );
                                  })}
                                </ol>
                              )}
                            </section>
                            {semesterExams.map((exam) => {
                              const meta = LESSON_KIND_META[exam.lesson_kind];
                              const examProgress = lessonProgress.get(exam.id);
                              const done = !!examProgress?.total && examProgress.completed >= examProgress.total;
                              return (
                                <Link
                                  key={exam.id}
                                  id={`lesson-${exam.id}`}
                                  href={lessonHref(exam)}
                                  onClick={() => rememberLesson(exam)}
                                  className={`class-lesson class-lesson--semester ${done ? "is-complete" : ""}`}
                                >
                                  <span className="class-num class-num--exam">{done ? <Check size={13} /> : "KT"}</span>
                                  <span className="class-lesson-title">
                                    {exam.title}
                                    <small>{meta.label}</small>
                                  </span>
                                  <span className="class-meta">{session ? (done ? "Đã làm" : "Chưa làm") : "Kiểm tra"}</span>
                                </Link>
                              );
                            })}
                          </Fragment>
                        );
                      })}
                    </div>
                  )}

                  {classExams.length > 0 && (
                    <section className="lesson-section">
                      <h2>Đề thi</h2>
                      <ol className="class-lessons class-lessons--flat">
                        {classExams.map((exam) => (
                          <li key={exam.id}>
                            <Link href={`/kiem-tra/lam?id=${exam.id}`} className="class-lesson">
                              <span className="class-lesson-title">{exam.title}</span>
                              <span className="class-meta">
                                {exam.question_count} câu · {exam.duration_minutes} phút
                                {exam.difficulty && ` · ${DIFFICULTY_LABELS[exam.difficulty]}`}
                              </span>
                            </Link>
                          </li>
                        ))}
                      </ol>
                    </section>
                  )}

                  {!session && (
                    <p className="lesson-muted class-login-hint">
                      <Link href="/dang-nhap" className="lesson-link">Đăng nhập</Link> để xem đề thi và lưu tiến độ học.
                    </p>
                  )}

                  {classPosts.length > 0 && (
                    <section className="lesson-section">
                      <h2>Thông báo và học liệu</h2>
                      <ol className="class-lessons class-lessons--flat">
                        {classPosts.map((p) => (
                          <li key={p.id}>
                            <Link href={`/tin-tuc#post-${p.id}`} className="class-lesson">
                              <span className="class-lesson-title">
                                {p.title}
                                {(p.body || p.video_url) && (
                                  <small className="line-clamp-1">{p.body || "Video bài giảng"}</small>
                                )}
                              </span>
                            </Link>
                          </li>
                        ))}
                      </ol>
                    </section>
                  )}
                </>
              )}
            </div>
          </div>
        </main>
        <Footer />
      </>
    );
  }

  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-6xl px-6 pt-28 pb-20 lg:px-8">
        <h1 className="font-display text-3xl font-bold text-white sm:text-4xl">
          {effectiveSlug && activeDisplayName ? (
            <span className="text-gradient">{activeDisplayName}</span>
          ) : (
            <>Lớp <span className="text-gradient">học</span></>
          )}
        </h1>
        <p className="mt-3 mb-8 text-slate-400">
          {effectiveSlug
            ? "Không gian học tập, bài giảng và đề thi dành riêng cho lớp này."
            : "Chọn lớp để mở không gian học tập và theo dõi tiến độ."}
        </p>

        {!effectiveSlug && <div className="mb-6 inline-flex rounded-full border border-white/10 bg-white/5 p-1">
          {CLASS_TABS.map((tab) => (
            <button
              key={tab.id}
              onClick={() => {
                const url = tab.id === "university" ? "/lop-hoc?tab=cttc" : "/lop-hoc";
                window.history.replaceState(null, "", url);
              }}
              aria-pressed={activeTab === tab.id}
              className={`rounded-full px-5 py-2 text-sm font-semibold transition-colors ${
                activeTab === tab.id
                  ? "bg-primary text-white"
                  : "text-slate-300 hover:bg-white/10 hover:text-white"
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>}

        {!effectiveSlug && activeTab === "university" && (
          <section aria-labelledby="cttc-course-heading">
            <div className="mb-5 flex flex-wrap items-end justify-between gap-3">
              <div>
                <h2 id="cttc-course-heading" className="font-display text-xl font-semibold text-white">
                  Chương trình thực hành (CTTC)
                </h2>
                <p className="mt-1 text-sm text-slate-400">
                  Chọn môn học để mở không gian học tập và theo dõi tiến độ.
                </p>
              </div>
              <span className="rounded-full border border-emerald-400/20 bg-emerald-400/10 px-3 py-1.5 text-xs font-semibold text-emerald-300">
                {UNIVERSITY_CLASSES.filter((item) => item.href).length} môn đang hoạt động
              </span>
            </div>

            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
              {UNIVERSITY_CLASSES.filter((universityClass) => universityClass.href).map((universityClass) => (
                <Link
                  key={universityClass.title}
                  href={universityClass.href}
                  className="group rounded-2xl border border-white/10 bg-[#0B1020] p-5 text-left transition-all hover:-translate-y-1 hover:border-primary/50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary"
                >
                  <span className="flex h-12 w-12 items-center justify-center rounded-xl bg-white/5 text-2xl">
                    {universityClass.icon}
                  </span>
                  <h3 className="mt-5 font-display text-lg font-bold text-white">
                    {universityClass.title}
                  </h3>
                  <p className="mt-3 min-h-18 text-sm leading-6 text-slate-400">
                    {universityClass.description}
                  </p>
                  <span className="mt-5 flex items-center justify-between border-t border-white/10 pt-4 text-sm font-semibold text-[#60A5FA]">
                    Mở môn học
                    <span aria-hidden="true">→</span>
                  </span>
                </Link>
              ))}
            </div>
          </section>
        )}

        {activeTab === "secondary" && (!supabaseConfigured ? (
          <p className="text-slate-400">Hệ thống đang được cấu hình.</p>
        ) : !classes ? (
          <SkeletonGrid count={3} />
        ) : classes.length === 0 ? (
          <p className="text-slate-400">Chưa có lớp nào.</p>
        ) : (
          <>
              <div className="mb-5 flex flex-wrap items-end justify-between gap-3">
                <div>
                  <h2 className="font-display text-xl font-semibold text-white">
                    Chọn lớp học
                  </h2>
                  <p className="mt-1 text-sm text-slate-400">
                    Chọn khối lớp để vào chương trình học.
                  </p>
                </div>
              </div>

              {!effectiveSlug && <div className="grid gap-4 md:grid-cols-3">
                {GRADE_ORDER.map((grade) => {
                  const schoolClass = displayClasses.find((c) => classGrade(c.name) === grade);
                  if (!schoolClass) return null;
                  const details = GRADE_DETAILS[grade];
                  return (
                    <Link
                      key={grade}
                      href={`/lop-hoc/${schoolClass.slug}`}
                      className={`group rounded-2xl border p-5 transition hover:-translate-y-1 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white ${details.accent} ${grade === "9" ? "md:col-span-3" : ""}`}
                    >
                      <div className="flex items-center gap-5">
                        <div className="min-w-0 flex-1">
                          <p className="text-xs font-bold uppercase tracking-widest">{grade === "9" ? "THCS" : "THPT"} · Lớp</p>
                          <p className="mt-1 font-display text-5xl font-bold sm:text-6xl">{grade}</p>
                          <h3 className="mt-3 text-xl font-bold text-white">{GRADE_LABELS[grade] ?? `Vật lý ${grade}`}</h3>
                          <p className="mt-1 text-sm text-slate-300">{details.description}</p>
                        </div>
                        <img src={GRADE_IMAGES[grade]} alt="" className="h-28 w-20 shrink-0 rounded-lg object-cover shadow-lg" loading="lazy" />
                      </div>
                      <span className="mt-5 flex items-center justify-between border-t border-current/20 pt-4 text-sm font-bold">
                        Vào học <span aria-hidden="true" className="transition-transform group-hover:translate-x-1">→</span>
                      </span>
                    </Link>
                  );
                })}
              </div>}

          </>
        ))}
      </main>
      <Footer />
    </>
  );
}
