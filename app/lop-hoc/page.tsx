"use client";

import { Fragment, Suspense, useEffect, useMemo, useRef, useState } from "react";
import { ArrowLeft, ArrowRight, Check, ChevronDown, Search, X } from "lucide-react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import { SkeletonGrid } from "@/components/ui/Skeleton";
import EmptyState from "@/components/ui/EmptyState";
import ExamShelf from "@/components/lop-hoc/ExamShelf";
import ContentSearch from "@/components/home/ContentSearch";
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
  AVCN_CLASS_SLUG,
  AVCN_SUBJECT_CODE,
  CASIO_CLASS_SLUG,
  CASIO_SUBJECT_CODE,
  expandClassIdsByGrade,
  fetchMyClassRequest,
} from "@/services/classes";
import {
  fetchMyProgressMarks,
  summarizeLessonProgress,
  type LessonWithItemRefs,
  type MyProgressMarks,
} from "@/services/lessons";
import { fetchChaptersStatic, fetchClassesStatic, fetchLessonsStatic } from "@/services/static-content";
import { unassignedExamFitsGrade } from "@/features/exams/exam-grade";
import {
  fetchPublishedExams,
  fetchPublishedPosts,
  visibleTo,
  type ExamMeta,
  type PostMeta,
} from "@/services/content";
import { useAuth } from "@/components/auth/AuthProvider";
import TeacherViewBanner from "@/components/auth/TeacherViewBanner";
import { useTeacherView } from "@/components/auth/useTeacherView";
import { supabaseConfigured } from "@/services/supabase";
import { HSG_HREF, HSG_SUBJECT_CODE, academicSubject, subjectsForGrade } from "@/services/academic-subjects";
import type { InlineLessonProgress } from "@/components/lessons/InlineLessonAccordion";
import { fetchChapterMastery, type MasteryLevel } from "@/services/mastery";
// Bảng ôn lỗi sai kéo theo QuestionCard + framer-motion (~140 KB); tách chunk riêng.
// Panel vốn trả null khi chưa có dữ liệu nên lúc chờ cũng không hiện gì — không nhảy layout.
import { MistakeVaultChip } from "@/components/lessons/MistakeReviewPanel";
import { ClassProgressLine, ParentBand } from "@/components/lessons/ClassOverview";
import { stripHtmlToText } from "@/lib/strip-html";
import { fetchMyChildren, type LinkedChild } from "@/services/parent-links";
import { fetchMyRankStatus, fetchRankStatusOf } from "@/services/rank";
import LiveStudyStrip from "@/components/lessons/LiveStudyStrip";
import ReviewBanner from "@/components/review/ReviewBanner";
import type { RankStatus } from "@/features/rank/types";
import ChapterTree, { type ChapterTreeEntry } from "@/components/lessons/ChapterTree";
import Hsg9WeekCard from "@/components/lop-hoc/Hsg9WeekCard";

const LAST_LESSON_KEY = "thachlab-last-secondary-lesson";

const GRADE_LABELS: Record<string, string> = { "9": "KHTN 9" };
const GRADE_ORDER = ["10", "11", "12", "9"];
const GRADE_DESCRIPTIONS: Record<string, string> = {
  "10": "Xây nền tảng cơ học",
  "11": "Dao động, sóng và điện",
  "12": "Củng cố kiến thức, ôn thi",
  "9": "Kiến thức nền tảng Khoa học tự nhiên",
};

function subjectFromParam(param: string | null): string {
  return ["hoa-hoc", "sinh-hoc", HSG_SUBJECT_CODE].includes(param ?? "") ? param! : "vat-ly";
}

export default function ClassHubPage({ classSlug }: { classSlug?: string } = {}) {
  return <Suspense fallback={<div className="mx-auto max-w-6xl px-6 pt-28"><SkeletonGrid count={3} /></div>}>
    <ClassHubContent classSlug={classSlug} />
  </Suspense>;
}

function ClassHubContent({ classSlug }: { classSlug?: string }) {
  const { session, profile } = useAuth();
  const { isTeacherView } = useTeacherView();
  const searchParams = useSearchParams();
  const router = useRouter();
  const [classes, setClasses] = useState<SchoolClass[] | null>(null);
  const [activeId, setActiveId] = useState<number | null>(null);
  // ?subject= đổi được khi bấm menu trên cùng trong cùng trang (KHTN 9 ↔ Luyện thi chuyên & HSG).
  // Khởi tạo từ URL; đổi URL thì đồng bộ ngay lúc render (mẫu "so khoá trước", thay effect + setState).
  const subjectParam = searchParams.get("subject");
  const [activeSubjectCode, setActiveSubjectCode] = useState(() => subjectFromParam(subjectParam));
  const [seenSubjectParam, setSeenSubjectParam] = useState(subjectParam);
  // ?chapter= là giá trị dẫn xuất từ URL, không cần state riêng.
  const chapterParam = Number(searchParams.get("chapter"));
  const requestedChapterId = chapterParam > 0 ? chapterParam : null;
  const [collapsedChapters, setCollapsedChapters] = useState<Set<number>>(new Set());
  // >= 1024: chương đang chọn (cột giữa chỉ hiện chương này) + chương người dùng tự mở trong cây.
  // Tách khỏi collapsedChapters của accordion điện thoại để hai chế độ không giật nhau.
  const [pickedChapterId, setPickedChapterId] = useState<number | null>(null);
  const [treeOpenIds, setTreeOpenIds] = useState<Set<number>>(new Set());
  const [defaultChapterApplied, setDefaultChapterApplied] = useState(false);
  const [handledRequestedChapterKey, setHandledRequestedChapterKey] = useState<string | null>(null);
  // Bài học cuối cùng đã mở, đọc từ localStorage lúc khởi tạo. Toàn trang nằm trong Suspense + useSearchParams
  // nên chỉ render ở client (không lệch hydrate với static export).
  const [lastLessonId, setLastLessonId] = useState<number | null>(() => {
    if (typeof window === "undefined") return null;
    try {
      const saved = Number(window.localStorage.getItem(LAST_LESSON_KEY));
      return saved > 0 ? saved : null;
    } catch {
      return null;
    }
  });
  const [chapters, setChapters] = useState<Chapter[] | null>(null);
  const [lessons, setLessons] = useState<LessonWithItemRefs[] | null>(null);
  const [progressMarks, setProgressMarks] = useState<MyProgressMarks | null>(null);
  const [exams, setExams] = useState<ExamMeta[] | null>(null);
  // Phụ huynh xem trang này thay cho con: tiến độ phải đọc theo id của con (policy "parent reads child
  // lesson progress"), không phải id của chính phụ huynh — nếu không mọi bài đều hiện "Chưa học".
  const isParent = profile?.role === "parent";
  const [parentChildren, setParentChildren] = useState<LinkedChild[] | null>(null);
  const [selectedChildId, setSelectedChildId] = useState<string | null>(null);
  const [rank, setRank] = useState<RankStatus | null>(null);
  // Chờ profile tải xong mới biết đang xem với tư cách nào (tránh đọc nhầm tiến độ của phụ huynh).
  const viewId = !session || !profile ? null : isParent ? selectedChildId : session.user.id;
  const [posts, setPosts] = useState<PostMeta[] | null>(null);
  // Nhãn ✅🟡🔴⚪ cạnh tên bài, theo chương: chapterId -> (lessonId -> nhãn). Chỉ tải cho chương
  // đang MỞ (get_chapter_mastery) — mặc định trang chỉ mở sẵn đúng 1 chương nên vẫn đúng quy ước
  // "1 RPC là đủ, không lặp query"; chương khác chỉ tải khi người dùng tự mở.
  const [chapterMastery, setChapterMastery] = useState<Map<number, Map<number, MasteryLevel>>>(new Map());
  const chapterMasteryFetching = useRef<Set<number>>(new Set());

  if (subjectParam !== seenSubjectParam) {
    setSeenSubjectParam(subjectParam);
    setActiveSubjectCode(subjectFromParam(subjectParam));
    setCollapsedChapters(new Set());
  }

  // link cũ /lop-hoc?tab=cttc → luồng CTTC riêng
  useEffect(() => {
    if (searchParams.get("tab") === "cttc") router.replace("/lop-hoc/cttc");
  }, [searchParams, router]);

  useEffect(() => {
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

  // Sinh viên CTTC không học ở khối THPT: /lop-hoc (không kèm lớp) → hub CTTC.
  useEffect(() => {
    if (!classSlug && profile?.role === "student" && profile.track === "cttc") router.replace("/lop-hoc/cttc");
  }, [classSlug, profile, router]);

  // Học sinh THPT đã được duyệt vào lớp thì không cần bộ chọn lớp: vào thẳng lớp của em (thầy chốt 7/10/2026).
  const [classRedirect, setClassRedirect] = useState(false);
  const [searchOpen, setSearchOpen] = useState(false);
  useEffect(() => {
    if (classSlug || !classes || !supabaseConfigured || !session || profile?.role !== "student" || profile.track === "cttc") return;
    let cancelled = false;
    fetchMyClassRequest(session.user.id)
      .then((request) => {
        if (cancelled || request?.status !== "active") return;
        const grade = classGrade(request.className);
        const target = displayClassesByGrade(classes).find((c) => classGrade(c.name) === grade);
        if (!target) return;
        setClassRedirect(true);
        router.replace(`/lop-hoc/${target.slug}`);
      })
      .catch(() => undefined);
    return () => {
      cancelled = true;
    };
  }, [classSlug, classes, session, profile, router]);

  // đề thi yêu cầu đăng nhập (RLS) — chỉ tải khi có session
  // đề thi yêu cầu đăng nhập (RLS) — chỉ tải khi có session; dấu "đã học" tải cùng lúc,
  // không chờ danh sách bài (tiến độ tính từ itemRefs của fetchLessons, không truy vấn thêm).
  useEffect(() => {
    if (!supabaseConfigured || !session || !profile || isParent) return;
    fetchPublishedExams().then(setExams);
  }, [session, profile, isParent]);

  useEffect(() => {
    if (!supabaseConfigured || !session || !isParent) return;
    fetchMyChildren(session.user.id)
      .then((rows) => {
        setParentChildren(rows);
        setSelectedChildId((current) => current ?? rows[0]?.studentId ?? null);
      })
      .catch(() => setParentChildren([]));
  }, [session, isParent]);

  useEffect(() => {
    if (!supabaseConfigured || !viewId || isTeacherView) return;
    let cancelled = false;
    fetchMyProgressMarks(viewId)
      .then((m) => { if (!cancelled) setProgressMarks(m); })
      .catch(() => { if (!cancelled) setProgressMarks(null); });
    (isParent ? fetchRankStatusOf(viewId) : fetchMyRankStatus())
      .then((r) => { if (!cancelled) setRank(r); })
      .catch(() => { if (!cancelled) setRank(null); });
    return () => { cancelled = true; };
  }, [viewId, isParent, isTeacherView]);

  const lessonProgress = useMemo(
    (): Map<number, InlineLessonProgress> =>
      session && lessons?.length && progressMarks ? summarizeLessonProgress(lessons, progressMarks) : new Map(),
    [session, lessons, progressMarks],
  );

  // Tải nhãn mastery của một chương khi nó được mở ra (mặc định 1 chương/khi thầy tự mở thêm) —
  // cache theo chapterId để mở/đóng lại không gọi lại RPC.
  function ensureChapterMastery(chapterId: number) {
    if (!session || isParent || isTeacherView) return;
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
  const isAvcn = active?.slug === AVCN_CLASS_SLUG;
  const isCasio = active?.slug === CASIO_CLASS_SLUG;
  const subjectCode = isAvcn
    ? AVCN_SUBJECT_CODE
    : isCasio
    ? CASIO_SUBJECT_CODE
    : classGrade(active?.name ?? "") === "9"
    ? activeSubjectCode
    : "vat-ly";
  const activeDisplayName = active
    ? isAvcn || isCasio
      ? active.name
      : classGrade(active.name) === "9"
      ? subjectCode === HSG_SUBJECT_CODE
        ? academicSubject(subjectCode).label
        : `KHTN 9 · ${academicSubject(subjectCode).label}`
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
  // Đề không gán lớp (phần lớn đề đăng hàng loạt) mặc định hiện ở mọi lớp → kệ lớp 12 bày cả đề lớp 11 (17/10/2026).
  // Lọc thêm: đề gắn trong bài học thì theo lớp của chương chứa bài; không gắn thì đoán khối từ tiêu đề; mù thì giữ.
  const activeGrade = active ? classGrade(active.name) : null;
  const examGradeByLesson = (() => {
    const map = new Map<number, string | null>();
    if (!classes || !chapters || !lessons) return map;
    const chapterGrade = new Map<number, string | null>();
    for (const ch of chapters) {
      const grades = new Set(classes.filter((c) => ch.classIds.includes(c.id)).map((c) => classGrade(c.name)).filter(Boolean));
      chapterGrade.set(ch.id, grades.size === 1 ? [...grades][0]! : null);
    }
    for (const l of lessons) {
      const g = chapterGrade.get(l.chapter_id);
      if (g === undefined) continue;
      for (const item of l.itemRefs) for (const id of item.exam_ids) if (!map.has(id)) map.set(id, g);
    }
    return map;
  })();
  const classExams = (exams ?? []).filter(
    (e) =>
      visibleTo(e.classIds, visibleClassIds) &&
      e.subjectCode === subjectCode &&
      (e.classIds.length > 0 || visibleClassIds === null || unassignedExamFitsGrade(e.id, e.title, activeGrade, examGradeByLesson)),
  );
  const visibleLessonIds = new Set(classChapters.map((chapter) => chapter.id));

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

  // Mặc định chỉ mở một chương: chương trên URL, không thì chương của bài đang dở.
  // Điện thoại thu các chương còn lại để danh sách bài bắt đầu sớm. Chỉ áp dụng một lần.
  // Chạy đúng một lần ngay lúc render khi đủ dữ liệu (setState có điều kiện trong render, không dùng effect).
  if (
    !defaultChapterApplied &&
    classes && chapters && lessons &&
    classChapters.length > 0 &&
    !(session && !isParent && !isTeacherView && progressMarks === null)
  ) {
    setDefaultChapterApplied(true);
    let targetId = requestedChapterId;
    if (targetId === null && progressMarks) {
      const regular = lessons.filter(
        (lesson) => classChapters.some((chapter) => chapter.id === lesson.chapter_id) && !isPeriodicExam(lesson.lesson_kind),
      );
      const pct = (lesson: LessonWithItemRefs) => {
        const progress = lessonProgress.get(lesson.id);
        return progress?.total ? Math.round((progress.completed / progress.total) * 100) : 0;
      };
      const current = regular.find((lesson) => {
        const done = pct(lesson);
        return done > 0 && done < 100;
      }) ?? regular.find((lesson) => pct(lesson) < 100);
      targetId = current?.chapter_id ?? null;
    }
    if (targetId === null) targetId = classChapters[0]?.id ?? null;
    const openId = targetId;
    setCollapsedChapters(new Set(classChapters.filter((chapter) => chapter.id !== openId).map((chapter) => chapter.id)));
    if (openId !== null) setPickedChapterId((current) => current ?? openId);
  }

  // Nhãn mastery cho các chương ĐANG MỞ — chạy lại mỗi khi mở thêm chương hoặc session tới sau
  // (ensureChapterMastery tự bỏ qua chương đã tải/đang tải nên gọi lặp không tốn thêm request).
  useEffect(() => {
    if (!session || isParent || isTeacherView) return;
    if (selectedChapterId !== null) ensureChapterMastery(selectedChapterId);
    for (const ch of classChapters) {
      if (!collapsedChapters.has(ch.id)) ensureChapterMastery(ch.id);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [session, isParent, isTeacherView, collapsedChapters, classChapters, selectedChapterId]);

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

  // ?chapter= trên URL: mở chương đó (trang lớp) hoặc chuyển sang lớp chứa chương (trang chung) — một lần cho
  // mỗi (chương, lớp) khi đã có dữ liệu, ngay lúc render.
  const requestedChapterKey = requestedChapterId && classes && chapters ? `${requestedChapterId}|${classSlug ?? ""}` : null;
  if (requestedChapterKey !== null && requestedChapterKey !== handledRequestedChapterKey && requestedChapterId && classes && chapters) {
    setHandledRequestedChapterKey(requestedChapterKey);
    if (classSlug) {
      setCollapsedChapters((prev) => {
        if (!prev.has(requestedChapterId)) return prev;
        const next = new Set(prev);
        next.delete(requestedChapterId);
        return next;
      });
    } else {
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
    }
  }

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
    if (isTeacherView) return false;
    const p = lessonProgress.get(lesson.id);
    const percent = p?.total ? Math.round((p.completed / p.total) * 100) : 0;
    return !!session && percent === 100;
  }

  /**
   * "Nên làm tiếp" (A2): bài đang dở (ưu tiên bài vừa học) → bài có nhãn mastery thấp → bài đầu chưa học.
   * Suy từ dữ liệu đã tải nên máy khác vẫn ra cùng gợi ý (không dựa vào localStorage).
   */
  const nextAction = (() => {
    if (isParent || !session || !progressMarks) return null;
    const regular = treeEntries.flatMap((e) => e.lessons).filter((l) => !isPeriodicExam(l.lesson_kind));
    if (regular.length === 0) return null;
    const pct = (l: Lesson) => {
      const p = lessonProgress.get(l.id);
      return p?.total ? Math.round((p.completed / p.total) * 100) : 0;
    };
    const started = regular.filter((l) => pct(l) > 0 && pct(l) < 100);
    if (started.length > 0) {
      const lesson = started.find((l) => l.id === lastLessonId) ?? started[0];
      const p = lessonProgress.get(lesson.id)!;
      return { lesson, why: `Xong ${p.completed}/${p.total} mục` };
    }
    for (const lesson of regular) {
      const level = chapterMastery.get(lesson.chapter_id)?.get(lesson.id);
      if (level === "weak" || level === "practicing") {
        return { lesson, why: "Ôn lại bài này trước khi học bài mới." };
      }
    }
    const next = regular.find((l) => pct(l) < 100);
    if (next) {
      const anyDone = regular.some((l) => pct(l) === 100);
      return { lesson: next, why: anyDone ? "Bài kế tiếp." : "Bắt đầu từ bài này." };
    }
    return { lesson: null, why: "Đã học xong mọi bài. Vào Luyện tập để giữ phong độ." };
  })();

  /** Một dòng bấm được (B1/G1, 18/10/2026): "Tiếp theo: <bài> · <vì sao>" — thay thẻ 3 dòng + nút riêng. */
  function renderNextCard() {
    if (isTeacherView || !nextAction) return null;
    const { lesson, why } = nextAction;
    if (!lesson) return <p className="class-next-line class-next-line--done">{why}</p>;
    return (
      <button type="button" className="class-next-line" onClick={() => continueLesson(lesson)}>
        <span className="class-next-line-label">Tiếp theo</span>
        <span className="class-next-line-title">{lesson.title}</span>
        <span className="class-next-line-why">{why}</span>
        <ArrowRight size={16} aria-hidden />
      </button>
    );
  }

  /** Số liệu cho dải A1: chỉ tính bài thường (kiểm tra giữa/cuối kì không nằm trong "x mục"). */
  const statsLessons = treeEntries.flatMap((e) => e.lessons).filter((l) => !isPeriodicExam(l.lesson_kind));
  const statsTotalItems = statsLessons.reduce((n, l) => n + (lessonProgress.get(l.id)?.total ?? l.itemCount), 0);
  const statsDoneItems = statsLessons.reduce((n, l) => n + (lessonProgress.get(l.id)?.completed ?? 0), 0);

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
    const showAccountProgress = !!session && !isTeacherView;
    // Chương chỉ có đúng 1 bài (AVCN: mỗi chương là 1 bài): tiêu đề chương chính là link vào bài —
    // không lặp lại một dòng bài cùng tên ngay bên dưới (N4 — không lặp thông tin).
    const only = chapterLessons.length === 1 && semesterExams.length === 0 ? chapterLessons[0] : null;
    const onlyP = only ? lessonProgress.get(only.id) : undefined;
    const onlyPercent = onlyP?.total ? Math.round((onlyP.completed / onlyP.total) * 100) : 0;
    const onlyMeta = !only
      ? ""
      : !showAccountProgress
        ? `${only.itemCount} mục`
        : onlyPercent === 100
          ? "Hoàn thành"
          : onlyPercent > 0
            ? `Đang học · ${onlyPercent}%`
            : "Chưa học";
    let lessonNumber = 0;
    return (
      <Fragment key={ch.id}>
        <section id={desktop ? `chapter-pick-${ch.id}` : `chapter-${ch.id}`} className="class-chapter">
          {only ? (
            <Link prefetch={false}
              href={lessonHref(only)}
              onClick={() => rememberLesson(only)}
              className="class-chapter-head class-chapter-head--link"
            >
              <span className="class-chapter-title">
                <span className="class-chapter-num">Chương {chapterIndex + 1}</span> · {chapterDisplayTitle(ch.title)}
              </span>
              <small className={`class-chapter-count ${onlyPercent === 100 ? "is-done" : ""}`}>
                {onlyPercent === 100 ? <Check size={13} aria-label="Xong" /> : onlyMeta}
              </small>
              <ArrowRight size={16} aria-hidden />
            </Link>
          ) : desktop ? (
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
              {showAccountProgress && chapterTotal > 0 && (
                <small className={`class-chapter-count ${chapterCompleted === chapterTotal ? "is-done" : ""}`}>
                  {chapterCompleted === chapterTotal ? <Check size={13} aria-label="Xong" /> : `${chapterCompleted}/${chapterTotal}`}
                </small>
              )}
              <ChevronDown size={17} className={collapsed ? "" : "rotate-180"} />
            </button>
          )}
          {!only && showAccountProgress && chapterTotal > 0 && (
            <div className="class-chapter-progress">
              <span className="class-chapter-progress-bar">
                <i style={{ width: `${Math.round((chapterCompleted / chapterTotal) * 100)}%` }} />
              </span>
              <small>{chapterCompleted}/{chapterTotal} mục</small>
            </div>
          )}
          {!only && !collapsed && (
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
                const complete = showAccountProgress && percent === 100;
                const started = showAccountProgress && percent > 0 && !complete;
                const level = chapterMastery.get(ch.id)?.get(lesson.id);
                const review = (started || complete) && (level === "weak" || level === "practicing");
                const isNext = lesson.id === nextAction?.lesson?.id;
                const rowClass = `class-lesson ${complete && !review ? "is-complete" : isNext ? "is-started" : ""}`;
                const rowInner = (
                  <>
                      <span className={`class-num ${periodic ? "class-num--exam" : ""}`}>
                        {complete && !review ? <Check size={13} /> : periodic ? "KT" : lessonNumber}
                      </span>
                      <span className="class-lesson-title">
                        {lesson.title}
                        {lesson.description && <small>{lesson.description}</small>}
                      </span>
                      <span className={`class-meta ${showAccountProgress && !periodic && !review && !complete && !started ? "class-meta--idle" : ""}`}>
                        {periodic
                          ? showAccountProgress ? (complete ? "Đã làm" : "Chưa làm") : "Kiểm tra"
                          : !showAccountProgress
                            ? `${lesson.itemCount} mục`
                            : review
                              ? "Ôn lại"
                              : complete
                                ? "Hoàn thành"
                                : started
                                  ? `Đang học · ${percent}%`
                                  : "Chưa học"}
                      </span>
                  </>
                );
                return (
                  <li key={lesson.id}>
                    {isParent ? (
                      <div className={`${rowClass} class-lesson--static`}>{rowInner}</div>
                    ) : (
                      <Link prefetch={false} href={lessonHref(lesson)} onClick={() => rememberLesson(lesson)} className={rowClass}>
                        {rowInner}
                      </Link>
                    )}
                  </li>
                );
              })}
            </ol>
          )}
        </section>
        {semesterExams.length > 0 && (
          <div className="class-semester">
            {semesterExams.map((exam) => {
              const meta = LESSON_KIND_META[exam.lesson_kind];
              const examProgress = lessonProgress.get(exam.id);
              const done = showAccountProgress && !!examProgress?.total && examProgress.completed >= examProgress.total;
              const examClass = `class-lesson ${done ? "is-complete" : ""}`;
              const examInner = (
                <>
                  <span className="class-num class-num--exam">{done ? <Check size={13} /> : "KT"}</span>
                  <span className="class-lesson-title">
                    {exam.title}
                    <small>{meta.label}</small>
                  </span>
                  <span className="class-meta">{showAccountProgress ? (done ? "Đã làm" : "Chưa làm") : "Kiểm tra"}</span>
                </>
              );
              return isParent ? (
                <div key={exam.id} className={`${examClass} class-lesson--static`}>{examInner}</div>
              ) : (
                <Link prefetch={false}
                  key={exam.id}
                  id={desktop ? undefined : `lesson-${exam.id}`}
                  href={lessonHref(exam)}
                  onClick={() => rememberLesson(exam)}
                  className={examClass}
                >
                  {examInner}
                </Link>
              );
            })}
          </div>
        )}
      </Fragment>
    );
  }

  // Trang của một lớp: mục lục chương → bài, cùng ngôn ngữ với trang bài học.
  if (effectiveSlug) {
    const grade = active ? classGrade(active.name) : null;
    return (
      <>
        <Navbar />
        <main className="min-h-screen w-full pt-[76px]">
          <div className={isAvcn ? "lesson-shell lesson-shell--cttc" : "lesson-shell"}>
            <TeacherViewBanner />
            <ReviewBanner />
            <div className="lesson-layout lesson-layout--pick">
              <aside className="lesson-nav" aria-label="Chương trình lớp">
                {active && chapters && lessons && classChapters.length > 0 && (
                  <ChapterTree
                    entries={treeEntries}
                    mode="pick"
                    chaptersOnly
                    currentChapterId={selectedChapterId ?? undefined}
                    openChapterIds={openIdsForTree}
                    onToggleChapter={toggleTreeChapter}
                    onPickChapter={pickChapter}
                    lessonHref={lessonHref}
                    isLessonDone={lessonIsComplete}
                    showProgress={false}
                    readOnly={isParent}
                    onLessonClick={rememberLesson}
                  />
                )}
              </aside>
              <div className="lesson-main lesson-main--single">
                {!supabaseConfigured ? (
                  <p className="lesson-notice">Hệ thống đang được cấu hình.</p>
                ) : !classes ? (
                  <div className="pt-8"><SkeletonGrid count={2} /></div>
                ) : !active ? (
                  <p className="lesson-notice">Không tìm thấy lớp học này.</p>
                ) : (
                  <>
                    <header className="lesson-head">
                      {isAvcn && (
                        <p className="lesson-eyebrow">
                          <Link prefetch={false} href="/lop-hoc/cttc">Sinh viên CTTC</Link>
                        </p>
                      )}
                      <h1>{activeDisplayName}</h1>
                      {!isParent && !isTeacherView && session && rank?.season && rank.daily && rank.daily.streak > 0 && (
                        <p className="class-streak-chip">🔥 Chuỗi {rank.daily.streak} ngày</p>
                      )}
                      {/* Ô tìm bài thu thành icon (B1): bấm mới mở ô nhập ngay dưới tiêu đề. */}
                      <button
                        type="button"
                        className="class-search-btn"
                        aria-label={searchOpen ? "Đóng ô tìm bài" : "Tìm bài"}
                        aria-expanded={searchOpen}
                        aria-controls="class-search"
                        onClick={() => setSearchOpen((v) => !v)}
                      >
                        {searchOpen ? <X size={20} aria-hidden /> : <Search size={20} aria-hidden />}
                      </button>
                      {grade && GRADE_DESCRIPTIONS[grade] && (
                        <p className="lesson-lead">{GRADE_DESCRIPTIONS[grade]}</p>
                      )}
                      {grade === "9" && activeSubjectCode === HSG_SUBJECT_CODE && (
                        <p className="lesson-lead">
                          <Link prefetch={false} href="/lop-hoc/khtn-9" className="lesson-link">
                            <ArrowLeft size={14} /> Về KHTN 9
                          </Link>
                        </p>
                      )}
                      {grade === "9" && activeSubjectCode !== HSG_SUBJECT_CODE && (
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
                        {isParent && parentChildren && parentChildren.length > 0 && selectedChildId && (
                          <ParentBand childList={parentChildren} selectedId={selectedChildId} onSelect={setSelectedChildId} />
                        )}
                        {isParent && parentChildren?.length === 0 && (
                          <p className="class-parent-band">
                            Tài khoản chưa nối với em nào. <Link prefetch={false} href="/phu-huynh">Nối mã phụ huynh ở đây</Link> để xem tiến độ của con.
                          </p>
                        )}
                        {isParent && session && progressMarks && (
                          <ClassProgressLine completedItems={statsDoneItems} totalItems={statsTotalItems} />
                        )}
                        {renderNextCard()}
                        {/* Khoá HSG Vật lí 9: buổi thứ Bảy tới + việc hôm nay (lộ trình 18 buổi ở /lop-hoc/lo-trinh-hsg). */}
                        {!isParent && subjectCode === HSG_SUBJECT_CODE && (
                          <Hsg9WeekCard
                            userId={session?.user.id ?? null}
                            lessons={lessons}
                            progress={isTeacherView ? null : session && progressMarks ? lessonProgress : null}
                          />
                        )}

                        {/* Ô tìm bài chỉ hiện khi bấm icon kính lúp ở tiêu đề (B1, 18/10/2026). */}
                        {searchOpen && (
                          <div id="class-search">
                            <ContentSearch variant="account" autoFocus />
                          </div>
                        )}

                        {/* Một hàng chip thay 3 khối rời (Kho bẫy gập tại chỗ, link đề, link xếp hạng): mỗi chip là link
                            thẳng tới trang chính; chip Kho bẫy tự ẩn khi chưa có câu sai (N3). */}
                        {!isParent && session && (
                          <div className="class-chips" aria-label="Lối tắt">
                            <MistakeVaultChip />
                            {classExams.length > 0 && (
                              <a href="#de-thi" className="class-chip">Đề thi</a>
                            )}
                            {rank && (rank.rp > 0 || (rank.daily?.streak ?? 0) > 0) && (
                              <Link prefetch={false} href="/lop-hoc/xep-hang/" className="class-chip">Xếp hạng</Link>
                            )}
                          </div>
                        )}

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
                        {!isParent && session && <LiveStudyStrip />}
                      </div>
                    )}

                    {!isParent && <ExamShelf exams={classExams} bestScores={session && !isTeacherView ? progressMarks?.bestScores ?? null : null} />}

                    {!session && (
                      <p className="lesson-muted class-login-hint">
                        <Link prefetch={false} href="/dang-nhap" className="lesson-link">Đăng nhập</Link> để xem đề thi và lưu tiến độ học.
                      </p>
                    )}

                    {classPosts.length > 0 && (
                      <section className="lesson-section">
                        <h2>Thông báo và học liệu</h2>
                        <ol className="class-lessons class-lessons--flat">
                          {classPosts.map((p) => (
                            <li key={p.id}>
                              <Link prefetch={false} href={`/tin-tuc#post-${p.id}`} className="class-lesson">
                                <span className="class-lesson-title">
                                  {p.title}
                                  {(p.body || p.video_url) && (
                                    <small className="line-clamp-1">{p.body ? stripHtmlToText(p.body) : "Video bài giảng"}</small>
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

          </div>
        </main>
        <Footer variant="app" />
      </>
    );
  }

  return (
    <>
      <Navbar />
      <main className="min-h-screen w-full pt-[76px]">
        <div className="lesson-shell">
          <TeacherViewBanner />
            <ReviewBanner />
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
            ) : !classes || classRedirect ? (
              <SkeletonGrid count={2} />
            ) : classes.length === 0 ? (
              <EmptyState title="Chưa có lớp nào" description="Lớp học sẽ hiện ở đây khi hệ thống mở." />
            ) : (
              <div className="hub-grid">
                {GRADE_ORDER.map((grade) => {
                  const schoolClass = displayClasses.find((c) => classGrade(c.name) === grade);
                  if (!schoolClass) return null;
                  return (
                    <Link prefetch={false} key={grade} href={`/lop-hoc/${schoolClass.slug}`} className="hub-card">
                      <span className="hub-tile">{grade}</span>
                      <span className="hub-card-body">
                        <span className="hub-card-title">{GRADE_LABELS[grade] ?? `Vật lý ${grade}`}</span>
                        <span className="hub-card-desc">{GRADE_DESCRIPTIONS[grade]}</span>
                      </span>
                      <ArrowRight size={18} />
                    </Link>
                  );
                })}
                <Link prefetch={false} href={HSG_HREF} className="hub-card">
                  <span className="hub-tile">🏆</span>
                  <span className="hub-card-body">
                    <span className="hub-card-title">Luyện thi chuyên & HSG</span>
                    <span className="hub-card-desc">Vật lí lớp 9: ôn thi vào lớp 10 chuyên, học sinh giỏi</span>
                  </span>
                  <ArrowRight size={18} />
                </Link>
              </div>
            )}
            <p className="hub-switch">
              Bạn là sinh viên CTTC?
              <Link prefetch={false} href="/lop-hoc/cttc" className="lesson-link">
                Sang không gian CTTC <ArrowRight size={14} />
              </Link>
            </p>
          </div>
        </div>
      </main>
      <Footer variant="app" />
    </>
  );
}
