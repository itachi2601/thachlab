"use client";

import { Suspense, useEffect, useMemo, useState, type CSSProperties } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { Check, ChevronDown, ChevronRight } from "lucide-react";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import ContentHtml from "@/components/exams/ContentHtml";
import { useAuth } from "@/components/auth/AuthProvider";
import WorkedQuestionsGrid from "@/components/lessons/WorkedQuestionsGrid";
import PracticeQuestionsGrid from "@/components/lessons/PracticeQuestionsGrid";
import {
  SECTION_META,
  SECTION_ORDER,
  formatTypeCounts,
  youTubeEmbed,
  youTubeThumb,
  type LessonItem,
  type LessonItemKind,
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

function hexAlpha(hex: string, alpha: string) {
  return `${hex}${alpha}`;
}

/** Thẻ video YouTube: thumbnail + nút xem, bấm thì nhúng player. */
function VideoCard({
  item,
  color,
  onOpen,
}: {
  item: LessonItem;
  color: string;
  onOpen: () => void;
}) {
  const [open, setOpen] = useState(false);
  const embed = youTubeEmbed(item.video_url);
  const thumb = youTubeThumb(item.video_url);

  return (
    <div className="overflow-hidden rounded-2xl border border-white/10 bg-[#0B1020]">
      <div className="flex flex-wrap items-stretch">
        <div className="relative flex min-h-36 w-full items-center justify-center bg-gradient-to-br from-[#2563EB] to-primary-dark sm:w-56">
          {thumb ? (
            /* eslint-disable-next-line @next/next/no-img-element */
            <img
              src={thumb}
              alt=""
              className="absolute inset-0 h-full w-full object-cover opacity-70"
            />
          ) : null}
          <span className="relative flex h-14 w-14 items-center justify-center rounded-full border border-white/40 bg-white/10 text-2xl text-white backdrop-blur">
            ▶
          </span>
          <span className="absolute right-2 bottom-2 rounded bg-black/70 px-2 py-0.5 text-[10px] font-semibold text-white">
            YouTube
          </span>
        </div>
        <div className="flex min-w-0 flex-1 flex-col justify-center gap-2 p-5">
          <p className="font-display text-base font-bold tracking-wide text-white uppercase">
            {item.title}
          </p>
          <p className="text-sm text-slate-400">
            {item.subtitle || (item.video_url ? "Video" : "Tài liệu")}
          </p>
          <div className="mt-1 flex flex-wrap gap-2">
            {embed && (
              <button
                onClick={() => {
                  setOpen((o) => !o);
                  if (!open) onOpen();
                }}
                className="inline-flex items-center gap-2 rounded-xl px-4 py-2 text-sm font-semibold text-white"
                style={{ backgroundColor: "#2563EB" }}
              >
                ▶ {open ? "Ẩn video" : "Xem video"}
              </button>
            )}
            {item.pdf_url && (
              <a
                href={item.pdf_url}
                target="_blank"
                rel="noreferrer"
                onClick={onOpen}
                className="inline-flex items-center gap-2 rounded-xl border px-4 py-2 text-sm font-semibold"
                style={{ borderColor: hexAlpha(color, "66"), color }}
              >
                📄 Xem PDF
              </a>
            )}
          </div>
        </div>
      </div>
      {open && embed && (
        <div className="aspect-video w-full border-t border-white/10">
          <iframe
            src={embed}
            title={item.title}
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
            className="h-full w-full"
          />
        </div>
      )}
    </div>
  );
}

/** Thẻ nội dung lý thuyết: bấm nút để mở nội dung. */
function ContentCard({
  item,
  kind,
  onOpen,
}: {
  item: LessonItem;
  kind: LessonItemKind;
  onOpen: () => void;
}) {
  const meta = SECTION_META[kind];
  const [open, setOpen] = useState(false);
  const hasBody = item.body_html.trim() !== "";

  return (
    <div className="rounded-2xl border border-white/10 bg-[#0B1020]">
      <div className="flex flex-wrap items-center gap-4 p-5">
        <span
          className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl text-lg"
          style={{ backgroundColor: hexAlpha(meta.color, "26") }}
        >
          {meta.icon}
        </span>
        <span className="min-w-0 flex-1">
          <span className="block font-display font-bold text-white">
            {item.title}
          </span>
          {item.subtitle && (
            <span className="mt-0.5 block text-sm" style={{ color: meta.color }}>
              {item.subtitle}
            </span>
          )}
        </span>
        <span className="flex items-center gap-2">
          {item.pdf_url && (
            <a
              href={item.pdf_url}
              target="_blank"
              rel="noreferrer"
              onClick={onOpen}
              className="rounded-xl border px-4 py-2 text-sm font-semibold"
              style={{ borderColor: hexAlpha(meta.color, "66"), color: meta.color }}
            >
              📄 PDF
            </a>
          )}
          {hasBody && (
            <button
              onClick={() => {
                setOpen((o) => !o);
                if (!open) onOpen();
              }}
              className="inline-flex items-center gap-2 rounded-xl px-5 py-2 text-sm font-semibold text-white"
              style={{ backgroundColor: meta.color }}
            >
              {meta.action} {open ? "▴" : "▾"}
            </button>
          )}
        </span>
      </div>
      {open && hasBody && (
        <div className="border-t border-white/10 p-5 text-slate-200">
          <ContentHtml html={item.body_html} className="block leading-relaxed" />
        </div>
      )}
    </div>
  );
}

/** Thẻ 1 đề kiểm tra: thời gian + số câu theo dạng + trạng thái. Một mục có thể có nhiều thẻ (nhiều đề). */
function ExamCard({
  examId,
  kind,
  exam,
  score,
  loggedIn,
}: {
  examId: number;
  kind: LessonItemKind;
  exam: LessonExamMeta | undefined;
  score: number | undefined;
  loggedIn: boolean;
}) {
  const meta = SECTION_META[kind];
  const counts = exam ? formatTypeCounts(exam.type_counts) : "";

  return (
    <div className="flex flex-wrap items-center gap-4 rounded-2xl border border-white/10 bg-[#0B1020] p-5">
      <span
        className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl text-lg"
        style={{ backgroundColor: hexAlpha(meta.color, "26") }}
      >
        {meta.icon}
      </span>
      <span className="min-w-0 flex-1">
        <span className="block font-display font-bold tracking-wide text-white uppercase">
          {exam?.title ?? `Đề #${examId}`}
        </span>
        <span className="mt-1 flex flex-wrap items-center gap-2 text-sm">
          {exam && (
            <span style={{ color: meta.color }}>
              {exam.duration_minutes} phút
              {counts ? ` · ${counts}` : ` · ${exam.question_count} câu`}
            </span>
          )}
          {loggedIn && (
            <span
              className={`rounded-full border px-2.5 py-0.5 text-xs ${
                score !== undefined
                  ? "border-emerald-500/40 text-emerald-300"
                  : "border-white/15 text-slate-400"
              }`}
            >
              {score !== undefined ? `Đã làm · ${score} điểm` : "Chưa làm"}
            </span>
          )}
        </span>
      </span>
      {loggedIn ? (
        <Link
          href={`/kiem-tra/lam?id=${examId}`}
          className="rounded-xl px-5 py-2.5 text-sm font-bold text-white"
          style={{ backgroundColor: meta.color }}
        >
          {score !== undefined ? "Làm lại" : "Làm bài"}
        </Link>
      ) : (
        <Link
          href="/dang-nhap"
          className="rounded-xl border px-5 py-2.5 text-sm font-semibold"
          style={{ borderColor: hexAlpha(meta.color, "66"), color: meta.color }}
        >
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
  const [items, setItems] = useState<LessonItem[] | null>(null);
  const [examMetas, setExamMetas] = useState<Map<number, LessonExamMeta>>(new Map());
  const [scores, setScores] = useState<Map<number, number>>(new Map());
  const [done, setDone] = useState<Set<number>>(new Set());
  const [error, setError] = useState("");
  const [activeSection, setActiveSection] = useState<LessonItemKind | null>(
    "ly_thuyet",
  );

  useEffect(() => {
    if (!supabaseConfigured || !id) return;
    fetchLesson(id).then((res) => {
      if (!res) setError("Không tìm thấy bài học này.");
      else {
        setTitle(res.lesson.title);
        setChapterTitle(res.chapterTitle);
        setChapterId(res.lesson.chapter_id);
      }
    });
    fetchLessonItems(id).then(setItems);
    setActiveSection("ly_thuyet");
  }, [id]);

  // dữ liệu cần đăng nhập: thông tin đề kiểm tra (RLS), điểm, tiến độ
  // (mục Luyện tập tự lấy đề đầy đủ bên trong PracticeQuestionsGrid)
  useEffect(() => {
    if (!session || !items) return;
    const examIds = items
      .filter((i) => i.kind === "kiem_tra")
      .flatMap((i) => i.exam_ids);
    fetchExamMetas(examIds).then(setExamMetas);
    fetchMyExamScores(session.user.id).then(setScores);
    fetchMyProgress(session.user.id).then(setDone);
  }, [session, items]);

  const sections = useMemo(() => {
    if (!items) return [];
    return SECTION_ORDER.map((kind) => ({
      kind,
      items: items.filter((i) => i.kind === kind),
    }));
  }, [items]);

  function isDone(item: LessonItem) {
    if (item.kind === "kiem_tra")
      return item.exam_ids.length > 0 && item.exam_ids.every((id) => scores.has(id));
    return done.has(item.id);
  }

  function markDone(item: LessonItem) {
    if (!session || done.has(item.id)) return;
    setDone((prev) => new Set(prev).add(item.id));
    markItemDone(session.user.id, item.id);
  }

  if (!id)
    return (
      <p className="text-center text-slate-400">Thiếu mã bài học trong địa chỉ.</p>
    );
  if (error) return <p className="text-center text-red-400">{error}</p>;
  if (!items)
    return <p className="text-center text-slate-400">Đang tải bài học…</p>;

  const completedItems = items.filter(isDone).length;
  const progress = items.length > 0
    ? Math.round((completedItems / items.length) * 100)
    : 0;
  const classHref = classSlug
    ? `/lop-hoc/${classSlug}?subject=${encodeURIComponent(subjectCode)}${chapterId ? `&chapter=${chapterId}#chapter-${chapterId}` : ""}`
    : "/lop-hoc";

  return (
    <div className="cnc-embedded secondary-lesson-shell">
      <div className="cnc-accordion-workspace secondary-lesson-workspace">
        <div className="cnc-lesson-hero">
          <div className="cnc-breadcrumb">
            <Link href="/lop-hoc">Lớp học</Link>
            <ChevronRight size={14} />
            <Link href={classHref}>Trung học</Link>
            {chapterTitle && <>
              <ChevronRight size={14} />
              <Link href={classHref}>{chapterTitle}</Link>
            </>}
          </div>

          <div className="secondary-hero-grid">
            <div className="secondary-hero-copy">
              <span className="cnc-eyebrow">TRUNG HỌC · {chapterTitle || "BÀI HỌC"}</span>
              <h1>{title}</h1>
              <p>Học theo từng chặng, tự kiểm tra kiến thức và hoàn thành bài kiểm tra cuối bài.</p>
              <div className="cnc-stats">
                <span>📚 5 chặng học</span>
                <span>📄 {items.length} nội dung</span>
                <span>{session ? "✓ Đang lưu tiến độ" : "○ Đăng nhập để lưu"}</span>
              </div>
            </div>
            <div className="cnc-progress-card" aria-label={`Tiến độ bài học ${progress}%`}>
              <div><span>Tiến độ bài học</span><strong>{progress}%</strong></div>
              <div className="cnc-progress-track"><i style={{ width: `${progress}%` }} /></div>
              <small>{completedItems}/{items.length} nội dung đã hoàn thành</small>
            </div>
          </div>

          <div className="cnc-lesson-progress-row">
            <div className="cnc-section-progress-ring">
              <strong>{activeSection ? SECTION_ORDER.indexOf(activeSection) + 1 : 0}<small>/5</small></strong>
            </div>
            <nav className="cnc-section-pills" aria-label="Đi nhanh đến phần bài học">
              {sections.map(({ kind, items: sectionItems }, index) => {
                const meta = SECTION_META[kind];
                return (
                  <button
                    key={kind}
                    type="button"
                    disabled={sectionItems.length === 0}
                    onClick={() => {
                      setActiveSection(kind);
                      document.getElementById(`secondary-stage-${kind}`)?.scrollIntoView({ behavior: "smooth", block: "start" });
                    }}
                    className={`${kind} ${activeSection === kind ? "active" : ""} ${sectionItems.length === 0 ? "empty" : ""}`}
                    style={{ color: meta.color }}
                  >
                    <i />{index + 1}. {meta.label}
                  </button>
                );
              })}
            </nav>
          </div>
        </div>

        <div className="cnc-learning-sections">
          {sections.map((section, idx) => {
            const meta = SECTION_META[section.kind];
            const remaining = section.items.filter((item) => !isDone(item)).length;
            const isActive = activeSection === section.kind;
            const isEmpty = section.items.length === 0;
            const sectionComplete = !isEmpty && remaining === 0 && !!session;

            return (
              <section
                key={section.kind}
                id={`secondary-stage-${section.kind}`}
                className={`cnc-learning-section ${section.kind} ${isActive ? "active" : ""} ${isEmpty ? "empty" : ""}`}
                style={{ "--section-color": meta.color } as CSSProperties}
              >
                <header>
                  <span>§ {idx + 1}</span>
                  <div><span aria-hidden="true">{meta.icon}</span><strong>{meta.label}</strong></div>
                  <i />
                  <small>{isEmpty ? "Đang cập nhật" : sectionComplete ? "Đã xong" : isActive ? "Đang mở" : "Chưa xong"}</small>
                  <b>{section.items.length}</b>
                </header>

                <button
                  type="button"
                  disabled={isEmpty}
                  className="cnc-learning-card"
                  onClick={() => setActiveSection((current) => current === section.kind ? null : section.kind)}
                  aria-expanded={isActive}
                  aria-controls={`secondary-section-${section.kind}`}
                >
                  <span>{sectionComplete ? <Check size={22} /> : <span aria-hidden="true">{meta.icon}</span>}</span>
                  <div>
                    <strong>{meta.label}</strong>
                    <small>{isEmpty ? "Học liệu đang được giảng viên cập nhật" : `${section.items.length} nội dung trong phần này`}</small>
                  </div>
                  <b>{isEmpty ? "Sắp có" : isActive ? "Thu gọn" : meta.action}<ChevronDown size={17} /></b>
                </button>

                {isActive && !isEmpty && (
                  <div id={`secondary-section-${section.kind}`} className="cnc-section-body cnc-content">
                    <div className="space-y-3">
                      {section.items.map((item) => {
                        if (item.kind === "video")
                          return (
                            <VideoCard
                              key={item.id}
                              item={item}
                              color={meta.color}
                              onOpen={() => markDone(item)}
                            />
                          );
                        if (item.kind === "ly_thuyet")
                          return (
                            <ContentCard
                              key={item.id}
                              item={item}
                              kind={item.kind}
                              onOpen={() => markDone(item)}
                            />
                          );
                        if (item.kind === "kiem_tra")
                          return (
                            <div key={item.id} className="space-y-3">
                              <p className="font-display font-bold text-white">{item.title}</p>
                              {item.exam_ids.length === 0 ? (
                                <p className="text-sm text-slate-500">Chưa gắn đề</p>
                              ) : (
                                item.exam_ids.map((examId) => (
                                  <ExamCard
                                    key={examId}
                                    examId={examId}
                                    kind={item.kind}
                                    exam={examMetas.get(examId)}
                                    score={scores.get(examId)}
                                    loggedIn={!!session}
                                  />
                                ))
                              )}
                            </div>
                          );
                        // bai_tap_mau / luyen_tap: lưới từng câu, tự đánh dấu đã làm
                        return (
                          <div
                            key={item.id}
                            className="space-y-4 rounded-2xl border border-white/10 bg-[#0B1020] p-5"
                          >
                            <div>
                              <p className="font-display font-bold text-white">{item.title}</p>
                              {item.subtitle && (
                                <p className="mt-0.5 text-sm" style={{ color: meta.color }}>
                                  {item.subtitle}
                                </p>
                              )}
                            </div>
                            {item.kind === "bai_tap_mau" ? (
                              <WorkedQuestionsGrid questions={item.questions} color={meta.color} />
                            ) : (
                              <PracticeQuestionsGrid examIds={item.exam_ids} color={meta.color} />
                            )}
                            {session && !done.has(item.id) && (
                              <button
                                type="button"
                                onClick={() => markDone(item)}
                                className="rounded-lg border border-white/15 px-3 py-2 text-xs font-semibold text-slate-300 hover:border-emerald-400/40 hover:text-emerald-300"
                              >
                                Đánh dấu đã làm
                              </button>
                            )}
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}
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
        <Suspense
          fallback={<p className="text-center text-slate-400">Đang tải…</p>}
        >
          <LessonLoader />
        </Suspense>
      </main>
      <Footer />
    </>
  );
}
