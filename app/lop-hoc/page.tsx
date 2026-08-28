"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import { SkeletonGrid } from "@/components/ui/Skeleton";
import type { SchoolClass } from "@/features/exams/types";
import { DIFFICULTY_LABELS } from "@/features/exams/types";
import type { Chapter, Lesson } from "@/features/lessons/types";
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
import ContinueLearningCard from "@/components/lessons/ContinueLearningCard";
import MistakeReviewPanel from "@/components/lessons/MistakeReviewPanel";

const LAST_LESSON_KEY = "thachlab-last-secondary-lesson";

const GRADE_IMAGES: Record<string, string> = {
  "9": "/images/learning-path/khtn-9.jpg",
  "10": "/images/learning-path/vat-ly-10.jpg",
  "11": "/images/learning-path/vat-ly-11.jpg",
  "12": "/images/learning-path/vat-ly-12.jpg",
};
const GRADE_LABELS: Record<string, string> = { "9": "KHTN 9" };
const GRADE_ORDER = ["9", "10", "11", "12"];
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
  const { session } = useAuth();
  const router = useRouter();
  const [classes, setClasses] = useState<SchoolClass[] | null>(null);
  const [activeId, setActiveId] = useState<number | null>(null);
  const [activeTab, setActiveTab] = useState<(typeof CLASS_TABS)[number]["id"]>(
    "secondary",
  );
  const [activeSubjectCode, setActiveSubjectCode] = useState("vat-ly");
  const [requestedChapterId, setRequestedChapterId] = useState<number | null>(null);
  const [openChapterId, setOpenChapterId] = useState<number | null>(null);
  const [lastLessonId, setLastLessonId] = useState<number | null>(null);
  const [lessonProgress, setLessonProgress] = useState<Map<number, InlineLessonProgress>>(new Map());
  const [chapters, setChapters] = useState<Chapter[] | null>(null);
  const [lessons, setLessons] = useState<Lesson[] | null>(null);
  const [exams, setExams] = useState<ExamMeta[] | null>(null);
  const [posts, setPosts] = useState<PostMeta[] | null>(null);

  useEffect(() => {
    const savedLessonId = Number(window.localStorage.getItem(LAST_LESSON_KEY));
    if (savedLessonId > 0) setLastLessonId(savedLessonId);
    const requestedTab = new URLSearchParams(window.location.search).get("tab");
    if (requestedTab === "cttc") setActiveTab("university");
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

  const active = classes?.find((c) => c.id === activeId);
  const activeDisplayName = active
    ? `${classGrade(active.name) === "9" ? "KHTN 9" : active.name} - ${academicSubject(activeSubjectCode).label}`
    : undefined;
  const displayClasses = classes ? displayClassesByGrade(classes) : [];
  const visibleClassIds =
    classes && activeId !== null ? expandClassIdsByGrade([activeId], classes) : null;
  const classChapters = (chapters ?? []).filter(
    (ch) => visibleTo(ch.classIds, visibleClassIds) && ch.subjectCode === activeSubjectCode,
  );
  const classPosts = (posts ?? []).filter(
    (p) => visibleTo(p.classIds, visibleClassIds) && p.subjectCode === activeSubjectCode,
  );
  const classExams = (exams ?? []).filter(
    (e) => visibleTo(e.classIds, visibleClassIds) && e.subjectCode === activeSubjectCode,
  );
  const visibleLessonIds = new Set(classChapters.map((chapter) => chapter.id));
  const lastLesson = (lessons ?? []).find((lesson) => lesson.id === lastLessonId && visibleLessonIds.has(lesson.chapter_id)) ?? null;
  const lastLessonChapter = lastLesson ? classChapters.find((chapter) => chapter.id === lastLesson.chapter_id) ?? null : null;

  function lessonHref(lesson: Lesson) {
    const params = new URLSearchParams({
      id: String(lesson.id),
      subject: activeSubjectCode,
      chapter: String(lesson.chapter_id),
    });
    if (classSlug) params.set("class", classSlug);
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
      setOpenChapterId(requestedChapterId);
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
      setOpenChapterId(requestedChapterId);
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
  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-6xl px-6 pt-28 pb-20 lg:px-8">
        <h1 className="font-display text-3xl font-bold text-white sm:text-4xl">
          {classSlug && activeDisplayName ? (
            <>Lớp <span className="text-gradient">{activeDisplayName}</span></>
          ) : (
            <>Lớp <span className="text-gradient">học</span></>
          )}
        </h1>
        <p className="mt-3 mb-8 text-slate-400">
          {classSlug
            ? "Không gian học tập, bài giảng và đề thi dành riêng cho lớp này."
            : "Chọn lớp để mở không gian học tập và theo dõi tiến độ."}
        </p>

        {!classSlug && <div className="mb-6 inline-flex rounded-full border border-white/10 bg-white/5 p-1">
          {CLASS_TABS.map((tab) => (
            <button
              key={tab.id}
              onClick={() => {
                setActiveTab(tab.id);
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

        {!classSlug && activeTab === "university" && (
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
                    Chương trình phổ thông (THPT – THCS)
                  </h2>
                  <p className="mt-1 text-sm text-slate-400">
                    Chọn lớp hoặc môn học để xem chương trình và mở từng bài học.
                  </p>
                </div>
                {activeDisplayName && (
                  <span className="rounded-full border border-blue-400/20 bg-blue-400/10 px-3 py-1.5 text-xs font-semibold text-blue-300">
                    Đang chọn: {activeDisplayName}
                  </span>
                )}
              </div>

              {!classSlug && <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                {GRADE_ORDER.map((grade) => {
                  const gradeClasses = displayClasses.filter(
                    (c) => classGrade(c.name) === grade,
                  );
                  if (gradeClasses.length === 0) return null;
                  return (
                    <Link
                      key={grade}
                      href={`/lop-hoc/${gradeClasses[0].slug}`}
                      className="overflow-hidden rounded-2xl border border-white/10 bg-[#0B1020]"
                    >
                      <img
                        src={GRADE_IMAGES[grade]}
                        alt={GRADE_LABELS[grade] ?? `Vật lý lớp ${grade}`}
                        className="aspect-[2/3] w-full object-cover"
                        loading="lazy"
                      />
                      <div className="p-4">
                        <span className="font-display text-lg font-bold text-white">
                          {GRADE_LABELS[grade] ?? `Vật lý lớp ${grade}`}
                        </span>
                        <span className="mt-3 flex items-center justify-between border-t border-white/10 pt-3 text-sm font-semibold text-[#60A5FA]">
                          Mở lớp học <span aria-hidden="true">→</span>
                        </span>
                      </div>
                    </Link>
                  );
                })}
              </div>}

            {classSlug && active && (
              <div className="mt-10 space-y-12">
                <div className="flex flex-wrap items-center justify-between gap-4">
                  <Link href="/lop-hoc" className="text-sm font-semibold text-slate-400 hover:text-white">
                    ← Tất cả lớp học
                  </Link>
                  <div className="flex flex-wrap gap-2">
                    {subjectsForGrade(classGrade(active.name) ?? "").map((subject) => (
                      <button
                        key={subject.code}
                        type="button"
                        onClick={() => {
                          setActiveSubjectCode(subject.code);
                          setOpenChapterId(null);
                        }}
                        className={`rounded-full px-4 py-2 text-sm font-semibold transition-colors ${
                          activeSubjectCode === subject.code
                            ? "bg-primary text-white"
                            : "bg-white/5 text-slate-300 hover:bg-white/10"
                        }`}
                      >
                        {subject.icon} {subject.label}
                      </button>
                    ))}
                  </div>
                </div>
                <section>
                  <h2 className="mb-4 font-display text-xl font-semibold text-white">
                    Chương trình lớp {activeDisplayName}
                  </h2>
                  {!chapters || !lessons ? (
                    <SkeletonGrid count={2} />
                  ) : classChapters.length === 0 ? (
                    <p className="text-sm text-slate-400">
                      Chưa có chương trình học cho lớp này.
                    </p>
                  ) : (
                    <div className="space-y-6">
                      {lastLesson && lastLessonChapter && (
                        <ContinueLearningCard
                          chapterTitle={lastLessonChapter.title}
                          lessonTitle={lastLesson.title}
                          progress={lessonProgress.get(lastLesson.id)}
                          onContinue={() => continueLesson(lastLesson)}
                        />
                      )}
                      <MistakeReviewPanel />
                      {classChapters.map((ch) => {
                        const chapterLessons = lessons.filter(
                          (l) => l.chapter_id === ch.id,
                        );
                        const chapterTotal = chapterLessons.reduce((sum, lesson) => sum + (lessonProgress.get(lesson.id)?.total ?? lesson.itemCount), 0);
                        const chapterCompleted = chapterLessons.reduce((sum, lesson) => sum + (lessonProgress.get(lesson.id)?.completed ?? 0), 0);
                        const chapterPercent = chapterTotal > 0 ? Math.round((chapterCompleted / chapterTotal) * 100) : 0;
                        return (
                          <div
                            key={ch.id}
                            id={`chapter-${ch.id}`}
                            className="rounded-2xl border border-white/10 bg-[#080D1A] p-2"
                            style={{ scrollMarginTop: "104px" }}
                          >
                            <button
                              type="button"
                              onClick={() => {
                                setOpenChapterId((current) => current === ch.id ? null : ch.id);
                              }}
                              aria-expanded={openChapterId === ch.id}
                              aria-controls={`chapter-lessons-${ch.id}`}
                              className="flex w-full items-center justify-between gap-4 rounded-xl px-4 py-3 text-left text-sm font-bold tracking-wide text-slate-200 uppercase hover:bg-white/5 hover:text-white"
                            >
                              <span className="min-w-0 flex-1">
                                <span className="block truncate">{ch.title}</span>
                                <span className="mt-1 block h-1 max-w-48 overflow-hidden rounded-full bg-white/10">
                                  <span className="block h-full rounded-full bg-blue-500 transition-[width]" style={{ width: `${chapterPercent}%` }} />
                                </span>
                              </span>
                              <span className="flex shrink-0 items-center gap-3">
                                <span className="text-xs font-semibold normal-case tracking-normal text-slate-500">{chapterPercent}%</span>
                                <span className={`text-lg text-slate-500 transition-transform ${openChapterId === ch.id ? "rotate-180" : ""}`} aria-hidden="true">⌄</span>
                              </span>
                            </button>
                            {openChapterId === ch.id && <div id={`chapter-lessons-${ch.id}`} className="space-y-2 px-1 pb-1">
                              {chapterLessons.length === 0 && (
                                <p className="px-4 pb-3 text-sm text-slate-500">
                                  Chưa có bài học trong chương này.
                                </p>
                              )}
                              {chapterLessons.map((lesson) => {
                                const progress = lessonProgress.get(lesson.id);
                                const percent = progress?.total
                                  ? Math.round((progress.completed / progress.total) * 100)
                                  : 0;
                                return (
                                  <Link
                                    key={lesson.id}
                                    href={lessonHref(lesson)}
                                    onClick={() => {
                                      setLastLessonId(lesson.id);
                                      window.localStorage.setItem(LAST_LESSON_KEY, String(lesson.id));
                                    }}
                                    className="group flex items-center gap-4 rounded-xl border border-transparent px-4 py-4 transition-all hover:border-blue-400/20 hover:bg-white/5"
                                  >
                                    <span className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-[#1D3461] text-xl">
                                      📖
                                    </span>
                                    <span className="min-w-0 flex-1">
                                      <span className="block font-display text-sm font-bold tracking-wide text-white uppercase group-hover:text-primary">
                                        {lesson.title}
                                      </span>
                                      <span className="mt-1 block text-xs font-semibold tracking-wide text-[#60A5FA] uppercase">
                                        {lesson.itemCount} mục · {percent}% hoàn thành
                                      </span>
                                      <span className="mt-2 block h-1.5 max-w-64 overflow-hidden rounded-full bg-white/10">
                                        <span className="block h-full rounded-full bg-blue-500" style={{ width: `${percent}%` }} />
                                      </span>
                                    </span>
                                    <span className="shrink-0 text-sm font-semibold text-slate-500 transition-all group-hover:translate-x-1 group-hover:text-primary">
                                      Vào bài →
                                    </span>
                                  </Link>
                                );
                              })}
                            </div>}
                          </div>
                        );
                      })}
                    </div>
                  )}
                </section>

                {classExams.length > 0 && (
                  <section>
                    <h2 className="mb-4 font-display text-xl font-semibold text-white">
                      Đề thi lớp {activeDisplayName}
                    </h2>
                    <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
                      {classExams.map((exam) => (
                        <Link
                          key={exam.id}
                          href={`/kiem-tra/lam?id=${exam.id}`}
                          className="group rounded-2xl border border-white/10 bg-[#0B1020] p-6 transition-all hover:-translate-y-1 hover:border-primary/50"
                        >
                          <h3 className="font-display font-semibold text-white group-hover:text-primary">
                            {exam.title}
                          </h3>
                          <p className="mt-2 text-sm text-slate-400">
                            {exam.question_count} câu · {exam.duration_minutes}{" "}
                            phút
                            {exam.difficulty &&
                              ` · ${DIFFICULTY_LABELS[exam.difficulty]}`}
                          </p>
                        </Link>
                      ))}
                    </div>
                  </section>
                )}

                {!session && (
                  <p className="text-sm text-slate-400">
                    <Link
                      href="/dang-nhap"
                      className="text-primary hover:underline"
                    >
                      Đăng nhập
                    </Link>{" "}
                    để xem đề thi và lưu tiến độ học của em.
                  </p>
                )}

                {classPosts.length > 0 && (
                  <section>
                    <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
                      <h2 className="font-display text-xl font-semibold text-white">
                        Thông báo và học liệu lớp {activeDisplayName}
                      </h2>
                      <Link href="/blog" className="text-sm font-semibold text-primary hover:underline">
                        Xem blog kiến thức →
                      </Link>
                    </div>
                    <div className="grid gap-5 sm:grid-cols-2">
                      {classPosts.map((p) => (
                        <Link
                          key={p.id}
                          href={`/tin-tuc#post-${p.id}`}
                          className="rounded-2xl border border-white/10 bg-[#0B1020] p-6 transition-all hover:-translate-y-1 hover:border-primary/50"
                        >
                          <h3 className="font-display font-semibold text-white">
                            {p.title}
                          </h3>
                          <p className="mt-2 line-clamp-2 text-sm text-slate-400">
                            {p.body || (p.video_url && "🎬 Video bài giảng")}
                          </p>
                        </Link>
                      ))}
                    </div>
                  </section>
                )}
              </div>
            )}
            {classSlug && !active && (
              <div className="rounded-2xl border border-white/10 bg-[#0B1020] p-8 text-center">
                <p className="text-slate-300">Không tìm thấy lớp học này.</p>
                <Link href="/lop-hoc" className="mt-4 inline-block font-semibold text-primary hover:underline">
                  Quay lại danh sách lớp học
                </Link>
              </div>
            )}
          </>
        ))}
      </main>
      <Footer />
    </>
  );
}
