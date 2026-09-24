"use client";

import { Suspense, useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { ArrowLeft, ArrowRight, Check, ChevronDown, FileText, Play } from "lucide-react";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import ContentHtml from "@/components/exams/ContentHtml";
import { useAuth } from "@/components/auth/AuthProvider";
import WorkedQuestionsGrid from "@/components/lessons/WorkedQuestionsGrid";
import SampleQuestionsGrid from "@/components/lessons/SampleQuestionsGrid";
import PracticeSession from "@/components/lessons/PracticeSession";
import type { SchoolClass } from "@/features/exams/types";
import {
  LESSON_KIND_META,
  SECTION_META,
  SECTION_ORDER,
  formatTypeCounts,
  isGradedKind,
  isPeriodicExam,
  isSemesterExam,
  youTubeEmbed,
  youTubeThumb,
  type Chapter,
  type Lesson,
  type LessonItem,
  type LessonItemKind,
  type LessonKind,
} from "@/features/lessons/types";
import {
  fetchExamMetas,
  fetchChapters,
  fetchLesson,
  fetchLessonItems,
  fetchLessons,
  fetchMyExamScores,
  fetchMyProgress,
  markItemDone,
  type LessonExamMeta,
} from "@/services/lessons";
import { fetchMyLearningProgress, summarizeItemProgress, type ItemProgress } from "@/services/progress";
import type { TheoryStatusResult } from "@/features/progress/types";
import { expandClassIdsByGrade, fetchClasses } from "@/services/classes";
import { visibleTo } from "@/services/content";
import { supabaseConfigured } from "@/services/supabase";

/** Một màu nhấn duy nhất cho cả trang — tránh mỗi mục một màu gây phân tâm. */
const ACCENT = "#3B82F6";

/** Hạn nộp bài tập về nhà, vd "20:00 · 25/09/2026". */
function formatDue(iso: string) {
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  return `${d.toLocaleTimeString("vi-VN", { hour: "2-digit", minute: "2-digit" })} · ${d.toLocaleDateString("vi-VN")}`;
}

/** Video YouTube: ảnh bìa, bấm thì nhúng player ngay tại chỗ. Xem xong tự bấm "Đánh dấu đã xem". */
function VideoBlock({
  item,
  done,
  loggedIn,
  onDone,
}: {
  item: LessonItem;
  done: boolean;
  loggedIn: boolean;
  onDone: () => void;
}) {
  const [playing, setPlaying] = useState(false);
  const embed = youTubeEmbed(item.video_url);
  const thumb = youTubeThumb(item.video_url);

  return (
    <div className="lesson-block">
      <div className="lesson-block-head">
        <p className="lesson-block-title">{item.title}</p>
        {item.subtitle && <p className="lesson-block-sub">{item.subtitle}</p>}
      </div>
      {embed && (
        <div className="lesson-video">
          {playing ? (
            <iframe
              src={`${embed}?autoplay=1`}
              title={item.title}
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            />
          ) : (
            <button type="button" onClick={() => setPlaying(true)} aria-label={`Xem video ${item.title}`}>
              {thumb && (
                /* eslint-disable-next-line @next/next/no-img-element */
                <img src={thumb} alt="" loading="lazy" decoding="async" />
              )}
              <span>
                <Play size={22} fill="currentColor" />
              </span>
            </button>
          )}
        </div>
      )}
      <div className="lesson-block-foot">
        {item.pdf_url && (
          <a href={item.pdf_url} target="_blank" rel="noreferrer" className="lesson-link">
            <FileText size={15} /> Tài liệu PDF
          </a>
        )}
        {loggedIn && (
          <button type="button" className={`lesson-done ${done ? "is-done" : ""}`} onClick={onDone} disabled={done}>
            <Check size={14} /> {done ? "Đã xem" : "Đánh dấu đã xem"}
          </button>
        )}
      </div>
    </div>
  );
}

/** Lý thuyết: hiện thẳng nội dung; mục thứ hai trở đi thu gọn để trang không quá dài. */
function TheoryBlock({
  item,
  defaultOpen,
  hideTitle,
  done,
  loggedIn,
  onDone,
}: {
  item: LessonItem;
  defaultOpen: boolean;
  hideTitle: boolean; // tên mục trùng tên phần → khỏi lặp

  done: boolean;
  loggedIn: boolean;
  onDone: () => void;
}) {
  const [open, setOpen] = useState(defaultOpen);
  const hasBody = item.body_html.trim() !== "";

  return (
    <div className={`lesson-block ${hideTitle ? "lesson-block--plain" : ""}`}>
      {!hideTitle && <button
        type="button"
        className="lesson-block-head lesson-block-toggle"
        onClick={() => setOpen((o) => !o)}
        aria-expanded={open}
        disabled={!hasBody}
      >
        <span>
          <span className="lesson-block-title">{item.title}</span>
          {item.subtitle && <span className="lesson-block-sub">{item.subtitle}</span>}
        </span>
        {hasBody && <ChevronDown size={18} className={open ? "rotate-180" : ""} />}
      </button>}
      {open && hasBody && (
        <div className={hideTitle ? "lesson-prose lesson-prose--plain" : "lesson-prose"}>
          <ContentHtml html={item.body_html} className="block leading-relaxed" />
        </div>
      )}
      <div className="lesson-block-foot">
        {item.pdf_url && (
          <a href={item.pdf_url} target="_blank" rel="noreferrer" className="lesson-link">
            <FileText size={15} /> Tài liệu PDF
          </a>
        )}
        {loggedIn && open && (
          <button type="button" className={`lesson-done ${done ? "is-done" : ""}`} onClick={onDone} disabled={done}>
            <Check size={14} /> {done ? "Đã tự xác nhận đọc" : "Tôi đã đọc xong"}
          </button>
        )}
      </div>
    </div>
  );
}

/** Quiz kiểm tra nhanh cuối lý thuyết: badge trạng thái + nút vào làm/làm lại, giữ lịch sử từng lần. */
function TheoryQuizBlock({
  examId,
  itemId,
  status,
}: {
  examId: number;
  itemId: number;
  status: TheoryStatusResult | undefined;
}) {
  const attempted = !!status && status.attemptCount > 0;
  const tone =
    status?.status === "passed" ? "lesson-status-done" : attempted ? "lesson-status" : "lesson-status";
  return (
    <div className="lesson-exam">
      <div>
        <p className="lesson-block-title">Kiểm tra nhanh</p>
        <p className="lesson-block-sub">
          {status?.status === "passed" && `Đúng ${status.bestCorrect} câu — `}
          {status?.status === "completed_not_passed" &&
            `Đúng ${status.bestCorrect} câu, chưa đạt (lần ${status.attemptCount}) — `}
          <span className={tone}>{status?.label ?? "Chưa bắt đầu"}</span>
        </p>
      </div>
      <Link href={`/kiem-tra/lam?id=${examId}&item=${itemId}`} className={attempted ? "lesson-btn-ghost" : "lesson-btn"}>
        {attempted ? "Làm lại" : "Làm kiểm tra nhanh"}
      </Link>
    </div>
  );
}

/** Một đề: tên, thời gian + số câu, trạng thái, nút làm bài. */
function ExamRow({
  examId,
  itemId,
  exam,
  score,
  loggedIn,
  metaStatus,
  statusLabel,
  passed,
}: {
  examId: number;
  itemId?: number | null;
  exam: LessonExamMeta | undefined;
  score: number | undefined;
  loggedIn: boolean;
  /** Trạng thái tải thông tin đề (chỉ có ý nghĩa khi đã đăng nhập) — phân biệt đang tải/lỗi/không thấy đề với chưa đăng nhập. */
  metaStatus: "loading" | "error" | "ready";
  /** Nhãn Đạt/Chưa đạt/Chờ chấm/Đã nộp — chỉ có khi mục này đã tính được trạng thái. */
  statusLabel?: string;
  passed?: boolean;
}) {
  if (!exam) {
    const notice = !loggedIn
      ? "Đăng nhập để xem đề"
      : metaStatus === "loading"
        ? "Đang tải…"
        : metaStatus === "error"
          ? "Không tải được, thử tải lại trang"
          : "Đề không khả dụng";
    return (
      <div className="lesson-exam">
        <div>
          <p className="lesson-block-title">Đề kiểm tra</p>
        </div>
        {loggedIn ? (
          <span className="lesson-muted">{notice}</span>
        ) : (
          <Link href="/dang-nhap" className="lesson-btn-ghost">
            {notice}
          </Link>
        )}
      </div>
    );
  }

  const counts = formatTypeCounts(exam.type_counts);
  const attempted = score !== undefined;

  return (
    <div className="lesson-exam">
      <div>
        <p className="lesson-block-title">{exam.title}</p>
        <p className="lesson-block-sub">
          {exam.duration_minutes} phút · {counts || `${exam.question_count} câu`}
          <span className={attempted && passed !== false ? "lesson-status-done" : attempted ? "lesson-status" : "lesson-status"}>
            {attempted ? `${statusLabel ?? "Đã làm"} · ${score} điểm` : "Chưa làm"}
          </span>
        </p>
      </div>
      <Link
        href={`/kiem-tra/lam?id=${examId}${itemId ? `&item=${itemId}` : ""}`}
        className={attempted ? "lesson-btn-ghost" : "lesson-btn"}
      >
        {attempted ? "Làm lại" : "Làm bài"}
      </Link>
    </div>
  );
}

function LessonLoader() {
  const { session } = useAuth();
  const searchParams = useSearchParams();
  const id = Number(searchParams.get("id"));
  const classSlug = searchParams.get("class");
  const subjectCode = searchParams.get("subject") ?? "vat-ly";

  const [title, setTitle] = useState("");
  const [chapterTitle, setChapterTitle] = useState("");
  const [chapterId, setChapterId] = useState<number | null>(null);
  const [lessonKind, setLessonKind] = useState<LessonKind>("bai_hoc");
  const [items, setItems] = useState<LessonItem[] | null>(null);
  const [examMetas, setExamMetas] = useState<Map<number, LessonExamMeta>>(new Map());
  const [examMetaStatus, setExamMetaStatus] = useState<"loading" | "error" | "ready">("loading");
  const [scores, setScores] = useState<Map<number, number>>(new Map());
  const [done, setDone] = useState<Set<number>>(new Set());
  const [progress, setProgress] = useState<Map<number, ItemProgress>>(new Map());
  const [error, setError] = useState("");
  const [activeSection, setActiveSection] = useState<LessonItemKind | null>(null);
  const mainRef = useRef<HTMLDivElement>(null);

  // fetchExamMetas() không trả về đề đang ẩn — sau khi tải xong, bỏ luôn các mã đề
  // ẩn khỏi danh sách hiển thị (đang tải thì cứ giữ nguyên, tránh nhấp nháy).
  function visibleExamIds(ids: number[]) {
    return examMetaStatus === "ready" ? ids.filter((id) => examMetas.has(id)) : ids;
  }

  // Chương trình lớp+môn đầy đủ, chỉ để tính Bài trước/Bài tiếp theo (không phải nội dung bài học).
  const [siblingClasses, setSiblingClasses] = useState<SchoolClass[] | null>(null);
  const [siblingChapters, setSiblingChapters] = useState<Chapter[] | null>(null);
  const [siblingLessons, setSiblingLessons] = useState<Lesson[] | null>(null);

  useEffect(() => {
    if (!supabaseConfigured || !id) return;
    fetchLesson(id).then((res) => {
      if (!res) setError("Không tìm thấy bài học này.");
      else {
        setTitle(res.lesson.title);
        setChapterTitle(res.chapterTitle);
        setChapterId(res.lesson.chapter_id);
        setLessonKind(res.lesson.lesson_kind);
      }
    });
    fetchLessonItems(id).then(setItems);
  }, [id]);

  useEffect(() => {
    if (!supabaseConfigured) return;
    fetchClasses().then(setSiblingClasses);
    fetchChapters().then(setSiblingChapters);
    fetchLessons().then(setSiblingLessons);
  }, []);

  // dữ liệu cần đăng nhập: thông tin đề kiểm tra (RLS), điểm, tiến độ
  useEffect(() => {
    if (!session || !items) return;
    const examIds = items.filter((i) => isGradedKind(i.kind)).flatMap((i) => i.exam_ids);
    void (async () => {
      if (examIds.length === 0) {
        setExamMetaStatus("ready");
        return;
      }
      setExamMetaStatus("loading");
      try {
        setExamMetas(await fetchExamMetas(examIds));
        setExamMetaStatus("ready");
      } catch {
        setExamMetaStatus("error");
      }
    })();
    fetchMyExamScores(session.user.id).then(setScores);
    fetchMyProgress(session.user.id).then(setDone);
    fetchMyLearningProgress(session.user.id, items).then(setProgress).catch(() => setProgress(new Map()));
  }, [session, items]);

  const progressSummary = useMemo(
    () => summarizeItemProgress(progress, items ?? []),
    [progress, items],
  );

  const sections = useMemo(() => {
    if (!items) return [];
    return SECTION_ORDER.map((kind) => ({ kind, items: items.filter((i) => i.kind === kind) }));
  }, [items]);

  // Đánh dấu mục đang đọc trên thanh điều hướng theo vị trí cuộn.
  useEffect(() => {
    const root = mainRef.current;
    if (!root || !items) return;
    const targets = Array.from(root.querySelectorAll<HTMLElement>("section[data-kind]"));
    if (targets.length === 0) return;
    setActiveSection(targets[0].dataset.kind as LessonItemKind);
    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((e) => e.isIntersecting)
          .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
        if (visible[0]) setActiveSection(visible[0].target.getAttribute("data-kind") as LessonItemKind);
      },
      { rootMargin: "-120px 0px -60% 0px", threshold: 0 },
    );
    targets.forEach((t) => observer.observe(t));
    return () => observer.disconnect();
  }, [items]);

  function isDone(item: LessonItem) {
    if (isGradedKind(item.kind)) {
      const ids = visibleExamIds(item.exam_ids);
      return ids.length > 0 && ids.every((id) => scores.has(id));
    }
    return done.has(item.id);
  }

  function markDone(item: LessonItem) {
    if (!session || done.has(item.id)) return;
    setDone((prev) => new Set(prev).add(item.id));
    markItemDone(session.user.id, item.id);
  }

  // Đến từ "Tiếp tục học" (resume=1): cuộn tới mục đầu tiên chưa hoàn thành nếu xác định được,
  // nếu không (chưa đăng nhập, đã xong hết…) thì cứ mở bài bình thường ở đầu trang.
  useEffect(() => {
    if (searchParams.get("resume") !== "1" || !session || !items || items.length === 0) return;
    const firstIncomplete = items.find((item) => !isDone(item));
    if (!firstIncomplete) return;
    const timer = window.setTimeout(() => {
      document.getElementById(`secondary-stage-${firstIncomplete.kind}`)?.scrollIntoView({ behavior: "smooth", block: "start" });
    }, 150);
    return () => window.clearTimeout(timer);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [searchParams, items, session, done, scores]);

  // Bài trước/Bài tiếp theo: thứ tự bài trong cùng lớp (theo lớp đang xem qua ?class=) và môn,
  // dùng lại đúng luật hiển thị chương của trang lớp — không tự suy luận lớp khác khi chưa chắc.
  const { prevLesson, nextLesson } = useMemo((): { prevLesson: Lesson | null; nextLesson: Lesson | null } => {
    if (!siblingChapters || !siblingLessons || !siblingClasses || chapterId == null) {
      return { prevLesson: null, nextLesson: null };
    }
    const currentChapter = siblingChapters.find((c) => c.id === chapterId);
    if (!currentChapter) return { prevLesson: null, nextLesson: null };
    const activeClass = classSlug ? siblingClasses.find((c) => c.slug === classSlug) : undefined;
    const scopeClassId = activeClass?.id ?? currentChapter.classIds[0];
    const visibleClassIds = scopeClassId !== undefined ? expandClassIdsByGrade([scopeClassId], siblingClasses) : null;
    const chaptersInScope = siblingChapters.filter(
      (ch) => ch.subjectCode === currentChapter.subjectCode && visibleTo(ch.classIds, visibleClassIds),
    );
    const flat: Lesson[] = [];
    for (const ch of chaptersInScope) {
      flat.push(...siblingLessons.filter((l) => l.chapter_id === ch.id && !isSemesterExam(l.lesson_kind)));
      flat.push(...siblingLessons.filter((l) => l.chapter_id === ch.id && isSemesterExam(l.lesson_kind)));
    }
    const idx = flat.findIndex((l) => l.id === id);
    if (idx === -1) return { prevLesson: null, nextLesson: null };
    return { prevLesson: idx > 0 ? flat[idx - 1] : null, nextLesson: idx < flat.length - 1 ? flat[idx + 1] : null };
  }, [siblingChapters, siblingLessons, siblingClasses, chapterId, classSlug, id]);

  function siblingHref(lesson: Lesson) {
    const params = new URLSearchParams({ id: String(lesson.id), subject: subjectCode, chapter: String(lesson.chapter_id) });
    if (classSlug) params.set("class", classSlug);
    return `/lop-hoc/bai?${params.toString()}`;
  }

  const pager = (prevLesson || nextLesson) && (
    <nav className="lesson-pager" aria-label="Điều hướng bài học">
      {prevLesson ? (
        <Link href={siblingHref(prevLesson)} className="lesson-pager-link lesson-pager-prev">
          <ArrowLeft size={16} />
          <span>
            <small>Bài trước</small>
            <strong>{prevLesson.title}</strong>
          </span>
        </Link>
      ) : (
        <span aria-hidden="true" />
      )}
      {nextLesson ? (
        <Link href={siblingHref(nextLesson)} className="lesson-pager-link lesson-pager-next">
          <span>
            <small>Bài tiếp theo</small>
            <strong>{nextLesson.title}</strong>
          </span>
          <ArrowRight size={16} />
        </Link>
      ) : (
        <span aria-hidden="true" />
      )}
    </nav>
  );

  if (!id) return <p className="lesson-notice">Thiếu mã bài học trong địa chỉ.</p>;
  if (error) return <p className="lesson-notice text-red-400">{error}</p>;
  if (!items) return <p className="lesson-notice">Đang tải bài học…</p>;

  const classHref = classSlug
    ? `/lop-hoc/${classSlug}?subject=${encodeURIComponent(subjectCode)}${chapterId ? `&chapter=${chapterId}#chapter-${chapterId}` : ""}`
    : "/lop-hoc";

  const backLink = (
    <Link href={classHref} className="lesson-back">
      <ArrowLeft size={15} /> {chapterTitle || "Lớp học"}
    </Link>
  );

  if (isPeriodicExam(lessonKind)) {
    const kindMeta = LESSON_KIND_META[lessonKind];
    const kiemTraItems = items.filter((i) => i.kind === "kiem_tra");
    const examIds = visibleExamIds(kiemTraItems.flatMap((i) => i.exam_ids));
    const itemByExamId = new Map(kiemTraItems.flatMap((i) => i.exam_ids.map((eid) => [eid, i])));
    return (
      <div className="lesson-shell">
        <div className="lesson-main lesson-main--single">
          {backLink}
          <header className="lesson-head">
            <p className="lesson-eyebrow">{kindMeta.label}</p>
            <h1>{title}</h1>
            <p className="lesson-lead">Làm bài trực tuyến, hệ thống chấm điểm tự động.</p>
          </header>
          <div className="lesson-stack">
            {examIds.length === 0 ? (
              <p className="lesson-muted">Đề kiểm tra đang được giảng viên cập nhật.</p>
            ) : (
              examIds.map((examId) => {
                const owningItem = itemByExamId.get(examId);
                const graded = owningItem ? progress.get(owningItem.id)?.graded : undefined;
                return (
                  <ExamRow
                    key={examId}
                    examId={examId}
                    itemId={owningItem?.id ?? null}
                    exam={examMetas.get(examId)}
                    score={scores.get(examId)}
                    loggedIn={!!session}
                    metaStatus={examMetaStatus}
                    statusLabel={graded?.label}
                    passed={graded ? graded.status === "passed" : undefined}
                  />
                );
              })
            )}
          </div>
          {pager}
        </div>
      </div>
    );
  }

  const visibleSections = sections.filter((s) => s.items.length > 0);

  return (
    <div className="lesson-shell">
      <div className="lesson-layout">
        <aside className="lesson-nav" aria-label="Các phần của bài học">
          {backLink}
          <ol>
            {visibleSections.map(({ kind, items: sectionItems }) => {
              const meta = SECTION_META[kind];
              const number = SECTION_ORDER.indexOf(kind) + 1;
              const complete = !!session && sectionItems.every(isDone);
              return (
                <li key={kind}>
                  <a
                    href={`#secondary-stage-${kind}`}
                    className={`${activeSection === kind ? "is-active" : ""} ${complete ? "is-complete" : ""}`}
                    onClick={(e) => {
                      e.preventDefault();
                      document
                        .getElementById(`secondary-stage-${kind}`)
                        ?.scrollIntoView({ behavior: "smooth", block: "start" });
                    }}
                  >
                    <i>{complete ? <Check size={12} /> : number}</i>
                    <span>{meta.label}</span>
                  </a>
                </li>
              );
            })}
          </ol>
          {session && items.length > 0 && progressSummary.totalRequired > 0 && (
            <div style={{ marginTop: 8 }}>
              <div
                className="lesson-progress"
                aria-label={`Hoàn thành ${progressSummary.completedRequired} trên ${progressSummary.totalRequired} mục bắt buộc`}
              >
                <span
                  style={{
                    width: `${Math.round((progressSummary.completedRequired / progressSummary.totalRequired) * 100)}%`,
                  }}
                />
                <small>
                  Hoàn thành {progressSummary.completedRequired}/{progressSummary.totalRequired}
                </small>
              </div>
              <div
                className="lesson-progress"
                style={{ marginTop: 22 }}
                aria-label={`Đạt ${progressSummary.passedRequired} trên ${progressSummary.totalRequired} mục bắt buộc`}
              >
                <span
                  style={{
                    width: `${Math.round((progressSummary.passedRequired / progressSummary.totalRequired) * 100)}%`,
                    background: "#10B981",
                  }}
                />
                <small>
                  Đạt {progressSummary.passedRequired}/{progressSummary.totalRequired}
                </small>
              </div>
            </div>
          )}
        </aside>

        <div className="lesson-main" ref={mainRef}>
          <header className="lesson-head">
            <p className="lesson-eyebrow">{chapterTitle}</p>
            <h1>{title}</h1>
          </header>

          {visibleSections.length === 0 && (
            <p className="lesson-muted">Học liệu đang được giảng viên cập nhật.</p>
          )}

          {visibleSections.map((section) => {
            const meta = SECTION_META[section.kind];
            const number = SECTION_ORDER.indexOf(section.kind) + 1;
            return (
              <section
                key={section.kind}
                id={`secondary-stage-${section.kind}`}
                data-kind={section.kind}
                className="lesson-section"
              >
                <h2>
                  <span>{number}</span>
                  {meta.label}
                </h2>
                <div className="lesson-stack">
                  {section.items.map((item, itemIndex) => {
                    // Mục duy nhất của phần → tiêu đề riêng (thường là "<Loại> — <tên bài>")
                    // chỉ lặp lại ý tiêu đề phần "N. <Tên phần>" ngay trên, ẩn cho đỡ trùng.
                    // Phụ đề (hạn nộp, số câu…) vẫn hiện bình thường.
                    const plain = section.items.length === 1;
                    if (item.kind === "video")
                      return (
                        <VideoBlock
                          key={item.id}
                          item={item}
                          done={done.has(item.id)}
                          loggedIn={!!session}
                          onDone={() => markDone(item)}
                        />
                      );

                    if (item.kind === "ly_thuyet")
                      return (
                        <div key={item.id} className="lesson-stack">
                          <TheoryBlock
                            item={item}
                            defaultOpen={itemIndex === 0}
                            hideTitle={plain}
                            done={done.has(item.id)}
                            loggedIn={!!session}
                            onDone={() => markDone(item)}
                          />
                          {session && item.exam_ids.length > 0 && (
                            <TheoryQuizBlock
                              examId={item.exam_ids[0]}
                              itemId={item.id}
                              status={progress.get(item.id)?.theory}
                            />
                          )}
                        </div>
                      );

                    if (isGradedKind(item.kind)) {
                      const gradedExamIds = visibleExamIds(item.exam_ids);
                      return (
                        <div key={item.id} className="lesson-block">
                          {(!plain || item.due_at) && (
                            <div className="lesson-block-head">
                              {!plain && <p className="lesson-block-title">{item.title}</p>}
                              {item.due_at && (
                                <p className="lesson-block-sub">Hạn nộp: {formatDue(item.due_at)}</p>
                              )}
                            </div>
                          )}
                          {gradedExamIds.length === 0 ? (
                            <p className="lesson-muted">Chưa gắn đề</p>
                          ) : (
                            <div className="lesson-stack">
                              {gradedExamIds.map((examId) => {
                                const graded = progress.get(item.id)?.graded;
                                return (
                                  <ExamRow
                                    key={examId}
                                    examId={examId}
                                    itemId={item.id}
                                    exam={examMetas.get(examId)}
                                    score={scores.get(examId)}
                                    loggedIn={!!session}
                                    metaStatus={examMetaStatus}
                                    statusLabel={graded?.label}
                                    passed={graded ? graded.status === "passed" : undefined}
                                  />
                                );
                              })}
                            </div>
                          )}
                        </div>
                      );
                    }

                    // bai_tap_mau / luyen_tap: lưới từng câu
                    return (
                      <div key={item.id} className="lesson-block">
                        {(!plain || item.subtitle) && (
                          <div className="lesson-block-head">
                            {!plain && <p className="lesson-block-title">{item.title}</p>}
                            {item.subtitle && <p className="lesson-block-sub">{item.subtitle}</p>}
                          </div>
                        )}
                        {item.kind === "bai_tap_mau" ? (
                          <>
                            {item.exam_ids.length > 0 && (
                              <SampleQuestionsGrid examIds={item.exam_ids} color={ACCENT} />
                            )}
                            <WorkedQuestionsGrid questions={item.questions} color={ACCENT} />
                          </>
                        ) : (
                          <PracticeSession
                            examIds={item.exam_ids}
                            lessonId={id}
                            itemId={item.id}
                            passScore={item.practice_pass_score}
                            color={ACCENT}
                          />
                        )}
                        {session && (
                          <div className="lesson-block-foot">
                            <button
                              type="button"
                              className={`lesson-done ${done.has(item.id) ? "is-done" : ""}`}
                              onClick={() => markDone(item)}
                              disabled={done.has(item.id)}
                            >
                              <Check size={14} /> {done.has(item.id) ? "Đã làm" : "Đánh dấu đã làm"}
                            </button>
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              </section>
            );
          })}
          {pager}
        </div>
      </div>
    </div>
  );
}

export default function LessonPage() {
  return (
    <>
      <Navbar />
      <main className="min-h-screen w-full pt-[76px]">
        <Suspense fallback={<p className="lesson-notice">Đang tải…</p>}>
          <LessonLoader />
        </Suspense>
      </main>
      <Footer />
    </>
  );
}
