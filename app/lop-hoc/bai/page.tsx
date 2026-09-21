"use client";

import { Suspense, useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { ArrowLeft, Check, ChevronDown, FileText, Play } from "lucide-react";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import ContentHtml from "@/components/exams/ContentHtml";
import { useAuth } from "@/components/auth/AuthProvider";
import WorkedQuestionsGrid from "@/components/lessons/WorkedQuestionsGrid";
import SampleQuestionsGrid from "@/components/lessons/SampleQuestionsGrid";
import PracticeSession from "@/components/lessons/PracticeSession";
import {
  LESSON_KIND_META,
  SECTION_META,
  SECTION_ORDER,
  formatTypeCounts,
  isGradedKind,
  isPeriodicExam,
  youTubeEmbed,
  youTubeThumb,
  type LessonItem,
  type LessonItemKind,
  type LessonKind,
} from "@/features/lessons/types";
import {
  fetchExamMetas,
  fetchLesson,
  fetchLessonItems,
  fetchMyExamScores,
  fetchMyProgress,
  markItemDone,
  type LessonExamMeta,
} from "@/services/lessons";
import { supabaseConfigured } from "@/services/supabase";

/** Một màu nhấn duy nhất cho cả trang — tránh mỗi mục một màu gây phân tâm. */
const ACCENT = "#3B82F6";

/** Hạn nộp bài tập về nhà, vd "20:00 · 25/09/2026". */
function formatDue(iso: string) {
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  return `${d.toLocaleTimeString("vi-VN", { hour: "2-digit", minute: "2-digit" })} · ${d.toLocaleDateString("vi-VN")}`;
}

/** Video YouTube: ảnh bìa, bấm thì nhúng player ngay tại chỗ. */
function VideoBlock({ item, onOpen }: { item: LessonItem; onOpen: () => void }) {
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
            <button
              type="button"
              onClick={() => {
                setPlaying(true);
                onOpen();
              }}
              aria-label={`Xem video ${item.title}`}
            >
              {thumb && (
                /* eslint-disable-next-line @next/next/no-img-element */
                <img src={thumb} alt="" />
              )}
              <span>
                <Play size={22} fill="currentColor" />
              </span>
            </button>
          )}
        </div>
      )}
      {item.pdf_url && (
        <a href={item.pdf_url} target="_blank" rel="noreferrer" onClick={onOpen} className="lesson-link">
          <FileText size={15} /> Tài liệu PDF
        </a>
      )}
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
            <Check size={14} /> {done ? "Đã đọc" : "Đánh dấu đã đọc"}
          </button>
        )}
      </div>
    </div>
  );
}

/** Một đề: tên, thời gian + số câu, trạng thái, nút làm bài. */
function ExamRow({
  examId,
  exam,
  score,
  loggedIn,
}: {
  examId: number;
  exam: LessonExamMeta | undefined;
  score: number | undefined;
  loggedIn: boolean;
}) {
  const counts = exam ? formatTypeCounts(exam.type_counts) : "";
  const attempted = score !== undefined;

  return (
    <div className="lesson-exam">
      <div>
        <p className="lesson-block-title">{exam?.title ?? `Đề #${examId}`}</p>
        <p className="lesson-block-sub">
          {exam && `${exam.duration_minutes} phút · ${counts || `${exam.question_count} câu`}`}
          {loggedIn && (
            <span className={attempted ? "lesson-status-done" : "lesson-status"}>
              {attempted ? `Đã làm · ${score} điểm` : "Chưa làm"}
            </span>
          )}
        </p>
      </div>
      {loggedIn ? (
        <Link href={`/kiem-tra/lam?id=${examId}`} className={attempted ? "lesson-btn-ghost" : "lesson-btn"}>
          {attempted ? "Làm lại" : "Làm bài"}
        </Link>
      ) : (
        <Link href="/dang-nhap" className="lesson-btn-ghost">
          Đăng nhập để làm
        </Link>
      )}
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
  const [scores, setScores] = useState<Map<number, number>>(new Map());
  const [done, setDone] = useState<Set<number>>(new Set());
  const [error, setError] = useState("");
  const [activeSection, setActiveSection] = useState<LessonItemKind | null>(null);
  const mainRef = useRef<HTMLDivElement>(null);

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

  // dữ liệu cần đăng nhập: thông tin đề kiểm tra (RLS), điểm, tiến độ
  useEffect(() => {
    if (!session || !items) return;
    const examIds = items.filter((i) => isGradedKind(i.kind)).flatMap((i) => i.exam_ids);
    fetchExamMetas(examIds).then(setExamMetas);
    fetchMyExamScores(session.user.id).then(setScores);
    fetchMyProgress(session.user.id).then(setDone);
  }, [session, items]);

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
    if (isGradedKind(item.kind))
      return item.exam_ids.length > 0 && item.exam_ids.every((id) => scores.has(id));
    return done.has(item.id);
  }

  function markDone(item: LessonItem) {
    if (!session || done.has(item.id)) return;
    setDone((prev) => new Set(prev).add(item.id));
    markItemDone(session.user.id, item.id);
  }

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
    const examIds = items.filter((i) => i.kind === "kiem_tra").flatMap((i) => i.exam_ids);
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
              examIds.map((examId) => (
                <ExamRow
                  key={examId}
                  examId={examId}
                  exam={examMetas.get(examId)}
                  score={scores.get(examId)}
                  loggedIn={!!session}
                />
              ))
            )}
          </div>
        </div>
      </div>
    );
  }

  const completedItems = items.filter(isDone).length;
  const visibleSections = sections.filter((s) => s.items.length > 0);

  return (
    <div className="lesson-shell">
      <div className="lesson-layout">
        <aside className="lesson-nav" aria-label="Các phần của bài học">
          {backLink}
          <ol>
            {sections.map(({ kind, items: sectionItems }, index) => {
              const meta = SECTION_META[kind];
              const empty = sectionItems.length === 0;
              const complete = !empty && !!session && sectionItems.every(isDone);
              return (
                <li key={kind}>
                  <a
                    href={`#secondary-stage-${kind}`}
                    className={`${activeSection === kind ? "is-active" : ""} ${empty ? "is-empty" : ""} ${complete ? "is-complete" : ""}`}
                    aria-disabled={empty}
                    onClick={(e) => {
                      e.preventDefault();
                      if (empty) return;
                      document
                        .getElementById(`secondary-stage-${kind}`)
                        ?.scrollIntoView({ behavior: "smooth", block: "start" });
                    }}
                  >
                    <i>{complete ? <Check size={12} /> : index + 1}</i>
                    <span>{meta.label}</span>
                  </a>
                </li>
              );
            })}
          </ol>
          {session && items.length > 0 && (
            <div className="lesson-progress" aria-label={`Đã hoàn thành ${completedItems} trên ${items.length} nội dung`}>
              <span style={{ width: `${Math.round((completedItems / items.length) * 100)}%` }} />
              <small>
                {completedItems}/{items.length} nội dung
              </small>
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
                    // tên mục trùng tên phần và là mục duy nhất → khỏi lặp tiêu đề
                    const plain =
                      section.items.length === 1 &&
                      item.title.trim().toLowerCase() === meta.label.toLowerCase();
                    if (item.kind === "video")
                      return <VideoBlock key={item.id} item={item} onOpen={() => markDone(item)} />;

                    if (item.kind === "ly_thuyet")
                      return (
                        <TheoryBlock
                          key={item.id}
                          item={item}
                          defaultOpen={itemIndex === 0}
                          hideTitle={plain}
                          done={done.has(item.id)}
                          loggedIn={!!session}
                          onDone={() => markDone(item)}
                        />
                      );

                    if (isGradedKind(item.kind))
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
                          {item.exam_ids.length === 0 ? (
                            <p className="lesson-muted">Chưa gắn đề</p>
                          ) : (
                            <div className="lesson-stack">
                              {item.exam_ids.map((examId) => (
                                <ExamRow
                                  key={examId}
                                  examId={examId}
                                  exam={examMetas.get(examId)}
                                  score={scores.get(examId)}
                                  loggedIn={!!session}
                                />
                              ))}
                            </div>
                          )}
                        </div>
                      );

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
