"use client";

import { Fragment, Suspense, useEffect, useMemo, useRef, useState } from "react";
import { ArrowLeft, ArrowRight, Check, ChevronDown } from "lucide-react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import { SkeletonGrid } from "@/components/ui/Skeleton";
import EmptyState from "@/components/ui/EmptyState";
import type { SchoolClass } from "@/features/exams/types";
import { DIFFICULTY_LABELS } from "@/features/exams/types";
import {
  LESSON_KIND_META,
  chapterDisplayTitle,
  isPeriodicExam,
  isSemesterExam,
  type Chapter,
  type Lesson,
} from "@/features/lessons/types";
import {
  classGrade,
  displayClassesByGrade,
  expandClassIdsByGrade,
} from "@/services/classes";
import {
  fetchMyProgressMarks,
  summarizeLessonProgress,
  type LessonWithItemRefs,
  type MyProgressMarks,
} from "@/services/lessons";
import { fetchChaptersStatic, fetchClassesStatic, fetchLessonsStatic } from "@/services/static-content";
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
import MasteryBadge from "@/components/mastery/MasteryBadge";
import { fetchChapterMastery, type MasteryLevel } from "@/services/mastery";
import dynamic from "next/dynamic";
import { LazyErrorBoundary } from "@/components/ui/LazyErrorBoundary";
import type { ComponentProps } from "react";
// Bảng ôn lỗi sai kéo theo QuestionCard + framer-motion (~140 KB); tách chunk riêng.
// Panel vốn trả null khi chưa có dữ liệu nên lúc chờ cũng không hiện gì — không nhảy layout.
const MistakeReviewPanelLazy = dynamic(() => import("@/components/lessons/MistakeReviewPanel"), { ssr: false, loading: () => null });
// Panel phụ, vốn đã trả null khi không có lỗi sai nào — lỗi render thì cũng chỉ ẩn đi.
function MistakeReviewPanel(props: ComponentProps<typeof MistakeReviewPanelLazy>) {
  return (
    <LazyErrorBoundary>
      <MistakeReviewPanelLazy {...props} />
    </LazyErrorBoundary>
  );
}
import ClassRankGroups from "@/components/rank/ClassRankGroups";
import ChapterTree, { type ChapterTreeEntry } from "@/components/lessons/ChapterTree";

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
  // >= 1024: chương đang chọn (cột giữa chỉ hiện chương này) + chương người dùng tự mở trong cây.
  // Tách khỏi collapsedChapters của accordion điện thoại để hai chế độ không giật nhau.
  const [pickedChapterId, setPickedChapterId] = useState<number | null>(null);
  const [treeOpenIds, setTreeOpenIds] = useState<Set<number>>(new Set());
  const defaultChapterAppliedRef = useRef(false);
  const [lastLessonId, setLastLessonId] = useState<number | null>(null);
  const [chapters, setChapters] = useState<Chapter[] | null>(null);
  const [lessons, setLessons] = useState<LessonWithItemRefs[] | null>(null);
  const [progressMarks, setProgressMarks] = useState<MyProgressMarks | null>(null);
  const [exams, setExams] = useState<ExamMeta[] | null>(null);
  const [posts, setPosts] = useState<PostMeta[] | null>(null);
  // Nhãn ✅🟡🔴⚪ cạnh tên bài, theo chương: chapterId -> (lessonId -> nhãn). Chỉ tải cho chương
  // đang MỞ (get_chapter_mastery) — mặc định trang chỉ mở sẵn đúng 1 chương nên vẫn đúng quy ước
  // "1 RPC là đủ, không lặp query"; chương khác chỉ tải khi người dùng tự mở.
  const [chapterMastery, setChapterMastery] = useState<Map<number, Map<number, MasteryLevel>>>(new Map());
  const chapterMasteryFetching = useRef<Set<number>>(new Set());

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
    // Lớp/chương/bài: ưu tiên file tĩnh /data/catalog.json (cùng origin); Supabase đối chiếu
    // ngầm phía sau, có khác thì thay (setter được gọi lần nữa với bản mới).
    const applyClasses = (cs: SchoolClass[]) => {
      setClasses(cs);
      if (classSlug) {
        const selectedClass = cs.find((item) => item.slug === classSlug);
        setActiveId(selectedClass?.id ?? null);
      }
    };
    fetchClassesStatic(applyClasses).then(applyClasses);
    fetchChaptersStatic(setChapters).then(setChapters);
    fetchLessonsStatic(setLessons).then(setLessons);
    fetchPublishedPosts().then(setPosts);
  }, [classSlug]);

  // đề thi yêu cầu đăng nhập (RLS) — chỉ tải khi có session
  // đề thi yêu cầu đăng nhập (RLS) — chỉ tải khi có session; dấu "đã học" tải cùng lúc,
  // không chờ danh sách bài (tiến độ tính từ itemRefs của fetchLessons, không truy vấn thêm).
  useEffect(() => {
    if (!supabaseConfigured || !session) return;
    fetchPublishedExams().then(setExams);
    fetchMyProgressMarks(session.user.id).then(setProgressMarks).catch(() => setProgressMarks(null));
  }, [session]);

  const lessonProgress = useMemo(
    (): Map<number, InlineLessonProgress> =>
      session && lessons?.length && progressMarks ? summarizeLessonProgress(lessons, progressMarks) : new Map(),
    [session, lessons, progressMarks],
  );

  // Tải nhãn mastery của một chương khi nó được mở ra (mặc định 1 chương/khi thầy tự mở thêm) —
  // cache theo chapterId để mở/đóng lại không gọi lại RPC.
  function ensureChapterMastery(chapterId: number) {
    if (!session) return;
    if (chapterMastery.has(chapterId) || chapterMasteryFetching.current.has(chapterId)) return;
    chapterMasteryFetching.current.add(chapterId);
    fetchChapterMastery(chapterId)
      .then((m) => setChapterMastery((prev) => new Map(prev).set(chapterId, m)))
      .catch(() => {
        /* RPC chưa chạy/lỗi mạng — bỏ qua lặng lẽ, icon mastery chỉ là trang trí. */
      })
      .finally(() => chapterMasteryFetching.current.delete(chapterId));
  }

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

  // Cây chương cột trái (>= 1024): cùng quy tắc gom với courseChapters của trang bài — bài thường
  // trước, kiểm tra giữa/cuối kì cuối chương, bỏ chương không có bài. (Không useMemo: classChapters
  // được tính lại mỗi lần render nên memo cũng không giữ được — xem cảnh báo react-hooks.)
  const treeEntries: ChapterTreeEntry[] = (() => {
    const all = lessons ?? [];
    return classChapters
      .map((chapter) => {
        const inChapter = all.filter((lesson) => lesson.chapter_id === chapter.id);
        return {
          chapter,
          lessons: [
            ...inChapter.filter((lesson) => !isSemesterExam(lesson.lesson_kind)),
            ...inChapter.filter((lesson) => isSemesterExam(lesson.lesson_kind)),
          ],
        };
      })
      .filter((entry) => entry.lessons.length > 0);
  })();

  // Chương đang chọn ở chế độ máy tính: ưu tiên người dùng bấm trong cây, rồi ?chapter= trên URL,
  // cuối cùng là chương đầu tiên có bài. Chưa có dữ liệu thì null (cột giữa vẫn hiện skeleton).
  const selectedChapterId =
    pickedChapterId !== null && classChapters.some((c) => c.id === pickedChapterId)
      ? pickedChapterId
      : requestedChapterId !== null && classChapters.some((c) => c.id === requestedChapterId)
        ? requestedChapterId
        : treeEntries[0]?.chapter.id ?? null;

  const selectedChapterIndex = classChapters.findIndex((c) => c.id === selectedChapterId);
  const selectedChapter = selectedChapterIndex >= 0 ? classChapters[selectedChapterIndex] : null;

  // Chương đang chọn luôn mở trên cây; người dùng vẫn gấp/mở được các chương khác.
  const openIdsForTree = new Set(treeOpenIds);
  if (selectedChapterId !== null) openIdsForTree.add(selectedChapterId);

  // Mặc định thu gọn tất cả các chương khi vào trang (trừ chương được yêu cầu mở qua đường dẫn).
  // Chỉ áp dụng một lần — sau đó người dùng tự mở/thu theo ý mình.
  useEffect(() => {
    if (defaultChapterAppliedRef.current) return;
    if (!classes || !chapters || !lessons) return;
    if (classChapters.length === 0) return;
    defaultChapterAppliedRef.current = true;
    const targetId = requestedChapterId;
    setCollapsedChapters(new Set(classChapters.filter((c) => c.id !== targetId).map((c) => c.id)));
  }, [classes, chapters, lessons, classChapters, requestedChapterId]);

  // Nhãn mastery cho các chương ĐANG MỞ — chạy lại mỗi khi mở thêm chương hoặc session tới sau
  // (ensureChapterMastery tự bỏ qua chương đã tải/đang tải nên gọi lặp không tốn thêm request).
  useEffect(() => {
    if (!session) return;
    for (const ch of classChapters) {
      if (!collapsedChapters.has(ch.id)) ensureChapterMastery(ch.id);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [session, collapsedChapters, classChapters]);

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
    // resume=1: trang bài học sẽ tự cuộn tới mục đầu tiên chưa hoàn thành nếu xác định được.
    router.push(`${lessonHref(lesson)}&resume=1`);
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

  function toggleAllChapters() {
    setCollapsedChapters((prev) => (prev.size > 0 ? new Set() : new Set(classChapters.map((c) => c.id))));
  }

  function rememberLesson(lesson: Lesson) {
    setLastLessonId(lesson.id);
    window.localStorage.setItem(LAST_LESSON_KEY, String(lesson.id));
  }

  /** Gấp/mở một chương trên cây cột trái (>= 1024) — không dùng chung state với accordion điện thoại. */
  function toggleTreeChapter(chapterId: number) {
    setTreeOpenIds((prev) => {
      const next = new Set(prev);
      if (next.has(chapterId)) next.delete(chapterId);
      else next.add(chapterId);
      return next;
    });
  }

  /** Bấm tên chương trên cây (>= 1024): đổi cột giữa + ghi ?chapter= lên URL để F5/chia sẻ link vẫn đúng. */
  function pickChapter(chapterId: number) {
    setPickedChapterId(chapterId);
    ensureChapterMastery(chapterId);
    const params = new URLSearchParams(window.location.search);
    params.set("chapter", String(chapterId));
    router.replace(`/lop-hoc/${effectiveSlug}?${params.toString()}`, { scroll: false });
  }

  /** Bài đã học xong = đủ 100% số mục — đúng công thức thanh tiến độ trong accordion. */
  function lessonIsComplete(lesson: Lesson): boolean {
    const p = lessonProgress.get(lesson.id);
    const percent = p?.total ? Math.round((p.completed / p.total) * 100) : 0;
    return !!session && percent === 100;
  }

  /** % hoàn thành của bài học gần nhất — dùng cho thẻ "Tiếp tục học". */
  const lastPercent = lastLesson
    ? (() => {
        const p = lessonProgress.get(lastLesson.id);
        return p?.total ? Math.round((p.completed / p.total) * 100) : null;
      })()
    : null;

  /** Thẻ "Tiếp tục học": <1024 nằm đầu cột giữa như trước, >= 1024 chuyển lên cột trái cạnh cây chương. */
  function renderContinueCard(variant: "main" | "nav") {
    if (!lastLesson || !lastLessonChapter) return null;
    return (
      <div className={`class-continue class-continue--${variant}`}>
        <div>
          <p className="lesson-eyebrow">Tiếp tục học</p>
          <p className="lesson-block-title">{lastLesson.title}</p>
          <p className="lesson-block-sub">
            {lastLessonChapter.title}
            {lastPercent !== null && ` · ${lastPercent}%`}
          </p>
        </div>
        <button type="button" className="lesson-btn" onClick={() => continueLesson(lastLesson)}>
          Tiếp tục học <ArrowRight size={15} />
        </button>
      </div>
    );
  }

  /**
   * Một chương của mục lục: tiêu đề + thanh tiến độ + danh sách bài, kèm các bài kiểm tra giữa/cuối
   * kì hiện ngay sau chương. `desktop` = bản ở cột giữa từ 1024px (chương đang chọn: luôn mở, không
   * nút gấp, id khác bản accordion để không trùng id trong DOM).
   */
  function renderChapterSection(ch: Chapter, chapterIndex: number, desktop: boolean) {
    // Kiểm tra giữa/cuối học kì không nằm trong nội dung chương:
    // tách ra khỏi danh sách bài, hiện thành mục riêng ngay sau chương.
    const all = lessons ?? [];
    const chapterLessons = all.filter((l) => l.chapter_id === ch.id && !isSemesterExam(l.lesson_kind));
    const semesterExams = all.filter((l) => l.chapter_id === ch.id && isSemesterExam(l.lesson_kind));
    const chapterTotal = chapterLessons.reduce((sum, lesson) => sum + (lessonProgress.get(lesson.id)?.total ?? lesson.itemCount), 0);
    const chapterCompleted = chapterLessons.reduce((sum, lesson) => sum + (lessonProgress.get(lesson.id)?.completed ?? 0), 0);
    const collapsed = !desktop && collapsedChapters.has(ch.id);
    let lessonNumber = 0;
    return (
      <Fragment key={ch.id}>
        <section id={desktop ? `chapter-pick-${ch.id}` : `chapter-${ch.id}`} className="class-chapter">
          {desktop ? (
            <div className="class-chapter-head class-chapter-head--static">
              <span className="class-chapter-title">
                <span className="class-chapter-num">Chương {chapterIndex + 1}</span> · {chapterDisplayTitle(ch.title)}
              </span>
            </div>
          ) : (
            <button
              type="button"
              className="class-chapter-head"
              onClick={() => toggleChapter(ch.id)}
              aria-expanded={!collapsed}
              aria-controls={`chapter-lessons-${ch.id}`}
            >
              <span className="class-chapter-title">
                <span className="class-chapter-num">Chương {chapterIndex + 1}</span> · {chapterDisplayTitle(ch.title)}
              </span>
              <ChevronDown size={17} className={collapsed ? "" : "rotate-180"} />
            </button>
          )}
          {session && chapterTotal > 0 && (
            <div className="class-chapter-progress">
              <span className="class-chapter-progress-bar">
                <i style={{ width: `${Math.round((chapterCompleted / chapterTotal) * 100)}%` }} />
              </span>
              <small>{chapterCompleted}/{chapterTotal} mục</small>
            </div>
          )}
          {!collapsed && (
            <ol id={desktop ? `chapter-lessons-pick-${ch.id}` : `chapter-lessons-${ch.id}`} className="class-lessons">
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
                      <span className="class-lesson-title">
                        {lesson.title}
                        {!periodic && <MasteryBadge level={chapterMastery.get(ch.id)?.get(lesson.id)} />}
                        {lesson.description && <small>{lesson.description}</small>}
                      </span>
                      <span className="class-meta">
                        {periodic
                          ? session ? (complete ? "Đã làm" : "Chưa làm") : "Kiểm tra"
                          : session
                            ? complete
                              ? "Hoàn thành"
                              : started
                                ? `Đang học · ${percent}%`
                                : "Chưa học"
                            : `${lesson.itemCount} mục`}
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
              id={desktop ? undefined : `lesson-${exam.id}`}
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
  }

  // Trang của một lớp: mục lục chương → bài, cùng ngôn ngữ với trang bài học.
  if (effectiveSlug) {
    const grade = active ? classGrade(active.name) : null;
    // Nút "Tiếp tục học" ở thanh đáy điện thoại: bài học gần nhất → bài đầu chưa học xong →
    // bài đầu khoá (khách chưa đăng nhập thì mọi bài đều "chưa xong" nên ra đúng bài đầu).
    const treeLessons = treeEntries.flatMap((entry) => entry.lessons);
    const bottomLesson =
      lastLesson ?? treeLessons.find((lesson) => !lessonIsComplete(lesson)) ?? treeLessons[0] ?? null;
    return (
      <>
        <Navbar />
        <main className="min-h-screen w-full pt-[76px]">
          <div className="lesson-shell">
            <div className="lesson-layout lesson-layout--pick">
              <aside className="lesson-nav" aria-label="Chương trình lớp">
                {active && chapters && lessons && classChapters.length > 0 && (
                  <>
                    {renderContinueCard("nav")}
                    <ChapterTree
                      entries={treeEntries}
                      mode="pick"
                      currentChapterId={selectedChapterId ?? undefined}
                      openChapterIds={openIdsForTree}
                      onToggleChapter={toggleTreeChapter}
                      onPickChapter={pickChapter}
                      lessonHref={lessonHref}
                      isLessonDone={lessonIsComplete}
                      onLessonClick={rememberLesson}
                    />
                  </>
                )}
              </aside>
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
                      {grade && GRADE_DESCRIPTIONS[grade] && (
                        <p className="lesson-lead">{GRADE_DESCRIPTIONS[grade]}</p>
                      )}
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
                        {renderContinueCard("main")}
                        <MistakeReviewPanel />

                        {classChapters.length > 1 && (
                          <div className="class-toc-toolbar">
                            <button type="button" className="lesson-link" onClick={toggleAllChapters}>
                              {collapsedChapters.size > 0 ? "Mở tất cả" : "Thu gọn"}
                            </button>
                          </div>
                        )}

                        {/* <1024: accordion cả khoá như trước. >= 1024: chỉ chương đang chọn, cây chương ở cột trái. */}
                        <div className="class-pick-mobile">
                          {classChapters.map((ch, chapterIndex) => renderChapterSection(ch, chapterIndex, false))}
                        </div>

                        {selectedChapter && (
                          <div className="class-pick-desktop">
                            {renderChapterSection(selectedChapter, selectedChapterIndex, true)}
                          </div>
                        )}
                      </div>
                    )}

                    {session && activeId !== null && <ClassRankGroups classId={activeId} />}

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

            {/* Thanh đáy điện thoại (< 640px): 3 nút, dùng lại CSS của trang bài. Khi thanh này hiện thì
                tabbar toàn site được ẩn đi (xem khối CSS cuối globals.css) — hai thanh fixed không thể cùng hiện. */}
            {active && chapters && lessons && classChapters.length > 0 && (
              <nav className="lesson-bottombar lesson-bottombar--mobile lesson-bottombar--pick" aria-label="Điều hướng lớp học">
                <Link href="/lop-hoc" className="lesson-bottom-link">
                  <ArrowLeft size={16} aria-hidden />
                  <span>Lớp học</span>
                </Link>
                {bottomLesson ? (
                  <button
                    type="button"
                    className="lesson-bottom-link lesson-bottom-link--next"
                    onClick={() => continueLesson(bottomLesson)}
                    title={bottomLesson.title}
                  >
                    <span>Tiếp tục học</span>
                    <ArrowRight size={16} aria-hidden />
                  </button>
                ) : (
                  <span className="lesson-bottom-link lesson-bottom-link--next is-empty" aria-hidden>
                    <span>Tiếp tục học</span>
                    <ArrowRight size={16} />
                  </span>
                )}
                <button type="button" className="lesson-bottom-link" onClick={toggleAllChapters}>
                  <span>{collapsedChapters.size > 0 ? "Mở tất cả" : "Thu gọn"}</span>
                </button>
              </nav>
            )}
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
              <EmptyState title="Chưa có lớp nào" description="Lớp học sẽ hiện ở đây khi hệ thống mở." />
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
