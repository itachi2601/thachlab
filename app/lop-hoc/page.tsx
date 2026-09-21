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

const GRADE_LABELS: Record<string, string> = { "9": "KHTN 9" };
const GRADE_ORDER = ["10", "11", "12", "9"];
const GRADE_DESCRIPTIONS: Record<string, string> = {
  "10": "Xây nền tảng cơ học",
  "11": "Dao động, sóng và điện",
  "12": "Củng cố kiến thức, ôn thi",
  "9": "Kiến thức nền tảng Khoa học tự nhiên",
};

export default function ClassHubPage({ classSlug }: { classSlug?: string } = {}) {
  return <Suspense fallback={<div className="mx-auto max-w-6xl px-6 pt-28"><SkeletonGrid count={3} /></div>}>
    <ClassHubContent classSlug={classSlug} />
  </Suspense>;
}

function ClassHubContent({ classSlug }: { classSlug?: string }) {
  const { session } = useAuth();
  const searchParams = useSearchParams();
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

  // link cũ /lop-hoc?tab=cttc → luồng CTTC riêng
  useEffect(() => {
    if (searchParams.get("tab") === "cttc") router.replace("/lop-hoc/cttc");
  }, [searchParams, router]);

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
                                    const started = !!session && percent > 0 && !complete;
                                    return (
                                      <li key={lesson.id}>
                                        <Link
                                          href={lessonHref(lesson)}
                                          onClick={() => rememberLesson(lesson)}
                                          className={`class-lesson ${complete ? "is-complete" : started ? "is-started" : ""}`}
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
      <main className="min-h-screen w-full pt-[76px]">
        <div className="lesson-shell">
          <div className="lesson-main lesson-main--single">
            <header className="lesson-head">
              <p className="lesson-eyebrow">Học sinh THPT · THCS</p>
              <h1>
                Chọn lớp để <span className="text-gradient">bắt đầu học.</span>
              </h1>
              <p className="lesson-lead">
                Vật lý 10–12 và Khoa học tự nhiên 9 theo chương trình GDPT 2018. Mở lớp của bạn để xem
                chương trình và lưu tiến độ.
              </p>
            </header>
            {!supabaseConfigured ? (
              <p className="lesson-muted">Hệ thống đang được cấu hình.</p>
            ) : !classes ? (
              <SkeletonGrid count={2} />
            ) : classes.length === 0 ? (
              <p className="lesson-muted">Chưa có lớp nào.</p>
            ) : (
              <div className="hub-grid">
                {GRADE_ORDER.map((grade) => {
                  const schoolClass = displayClasses.find((c) => classGrade(c.name) === grade);
                  if (!schoolClass) return null;
                  return (
                    <Link key={grade} href={`/lop-hoc/${schoolClass.slug}`} className="hub-card">
                      <span className="hub-tile">{grade}</span>
                      <span className="hub-card-body">
                        <span className="hub-card-title">{GRADE_LABELS[grade] ?? `Vật lý ${grade}`}</span>
                        <span className="hub-card-desc">{GRADE_DESCRIPTIONS[grade]}</span>
                      </span>
                      <ArrowRight size={18} />
                    </Link>
                  );
                })}
              </div>
            )}
            <p className="hub-switch">
              Bạn là sinh viên CTTC?
              <Link href="/lop-hoc/cttc" className="lesson-link">
                Sang không gian CTTC <ArrowRight size={14} />
              </Link>
            </p>
          </div>
        </div>
      </main>
      <Footer />
    </>
  );
}
