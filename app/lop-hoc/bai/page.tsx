"use client";

import { Suspense, useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import ContentHtml from "@/components/exams/ContentHtml";
import { useAuth } from "@/components/auth/AuthProvider";
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
        <div className="relative flex min-h-36 w-full items-center justify-center bg-gradient-to-br from-[#2563EB] to-[#1D4ED8] sm:w-56">
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

/** Thẻ nội dung (lý thuyết, bài tập mẫu, luyện tập sách): bấm nút để mở nội dung. */
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

/** Thẻ đề (luyện tập/kiểm tra): thời gian + số câu theo dạng + trạng thái. */
function ExamCard({
  item,
  kind,
  exam,
  score,
  loggedIn,
}: {
  item: LessonItem;
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
          {item.title}
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
      {item.exam_id ? (
        loggedIn ? (
          <Link
            href={`/kiem-tra/lam?id=${item.exam_id}`}
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
        )
      ) : (
        <span className="text-sm text-slate-500">Chưa gắn đề</span>
      )}
    </div>
  );
}

function LessonLoader() {
  const { session } = useAuth();
  const searchParams = useSearchParams();
  const id = Number(searchParams.get("id"));

  const [title, setTitle] = useState("");
  const [chapterTitle, setChapterTitle] = useState("");
  const [items, setItems] = useState<LessonItem[] | null>(null);
  const [examMetas, setExamMetas] = useState<Map<number, LessonExamMeta>>(new Map());
  const [scores, setScores] = useState<Map<number, number>>(new Map());
  const [done, setDone] = useState<Set<number>>(new Set());
  const [error, setError] = useState("");

  useEffect(() => {
    if (!supabaseConfigured || !id) return;
    fetchLesson(id).then((res) => {
      if (!res) setError("Không tìm thấy bài học này.");
      else {
        setTitle(res.lesson.title);
        setChapterTitle(res.chapterTitle);
      }
    });
    fetchLessonItems(id).then(setItems);
  }, [id]);

  // dữ liệu cần đăng nhập: thông tin đề (RLS), điểm, tiến độ
  useEffect(() => {
    if (!session || !items) return;
    const examIds = items
      .map((i) => i.exam_id)
      .filter((v): v is number => v !== null);
    fetchExamMetas(examIds).then(setExamMetas);
    fetchMyExamScores(session.user.id).then(setScores);
    fetchMyProgress(session.user.id).then(setDone);
  }, [session, items]);

  const sections = useMemo(() => {
    if (!items) return [];
    return SECTION_ORDER.map((kind) => ({
      kind,
      items: items.filter((i) => i.kind === kind),
    })).filter((s) => s.items.length > 0);
  }, [items]);

  function isDone(item: LessonItem) {
    if (item.kind === "luyen_tap_de" || item.kind === "kiem_tra")
      return item.exam_id !== null && scores.has(item.exam_id);
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

  return (
    <div>
      <p className="text-sm text-slate-400">
        <Link href="/lop-hoc" className="text-[#3B82F6] hover:underline">
          Lớp học
        </Link>
        {chapterTitle && <> · {chapterTitle}</>}
      </p>
      <h1 className="mt-2 font-display text-2xl font-bold tracking-wide text-white uppercase sm:text-3xl">
        {title}
      </h1>

      {sections.length === 0 && (
        <p className="mt-10 text-slate-400">Bài học này chưa có nội dung.</p>
      )}

      <div className="mt-10 space-y-10">
        {sections.map((section, idx) => {
          const meta = SECTION_META[section.kind];
          const remaining = section.items.filter((i) => !isDone(i)).length;
          return (
            <section key={section.kind}>
              <div className="mb-4 flex items-center gap-3">
                <span className="text-xs text-slate-500">§{idx + 1}</span>
                <span
                  className="flex h-9 w-9 items-center justify-center rounded-xl text-base"
                  style={{ backgroundColor: hexAlpha(meta.color, "26") }}
                >
                  {meta.icon}
                </span>
                <span
                  className="font-display text-sm font-bold tracking-widest uppercase"
                  style={{ color: meta.color }}
                >
                  {meta.label}
                </span>
                <span className="h-px flex-1 bg-white/10" />
                {session && (
                  <span className="flex items-center gap-2 text-xs text-slate-400">
                    {remaining > 0 ? "Chưa xong" : "Đã xong"}
                    {remaining > 0 && (
                      <span className="flex h-5 min-w-5 items-center justify-center rounded-full bg-white/10 px-1.5 font-semibold text-white">
                        {remaining}
                      </span>
                    )}
                  </span>
                )}
              </div>
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
                  if (item.kind === "luyen_tap_de" || item.kind === "kiem_tra")
                    return (
                      <ExamCard
                        key={item.id}
                        item={item}
                        kind={item.kind}
                        exam={item.exam_id ? examMetas.get(item.exam_id) : undefined}
                        score={
                          item.exam_id !== null
                            ? scores.get(item.exam_id)
                            : undefined
                        }
                        loggedIn={!!session}
                      />
                    );
                  return (
                    <ContentCard
                      key={item.id}
                      item={item}
                      kind={item.kind}
                      onOpen={() => markDone(item)}
                    />
                  );
                })}
              </div>
            </section>
          );
        })}
      </div>
    </div>
  );
}

export default function LessonPage() {
  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-4xl px-6 pt-28 pb-20 lg:px-8">
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
