"use client";

import { Suspense, useCallback, useEffect, useMemo, useRef, useState, type KeyboardEvent as ReactKeyboardEvent, type TouchEvent } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { ArrowLeft, ArrowRight, Check, ChevronDown, Eye, FileText, Home, Maximize2, Menu, MonitorPlay, Play, Search, X } from "lucide-react";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import ContentHtml from "@/components/exams/ContentHtml";
import { useAuth } from "@/components/auth/AuthProvider";
import WorkedQuestionsGrid from "@/components/lessons/WorkedQuestionsGrid";
import SampleQuestionsGrid from "@/components/lessons/SampleQuestionsGridLazy";
import LessonPresenter from "@/components/lessons/LessonPresenterLazy";
import PracticeSession from "@/components/lessons/PracticeSessionLazy";
import ChapterTree from "@/components/lessons/ChapterTree";
import LessonMasteryCard from "@/components/mastery/LessonMasteryCard";
import type { SchoolClass } from "@/features/exams/types";
import {
  consumeTheoryReviewContext,
  splitTheorySections,
  estimateTheoryTime,
  theorySectionItemId,
  wrapTheorySections,
  type TheoryReviewContext,
} from "@/features/lessons/theory-sections";
import {
  LESSON_KIND_META,
  SECTION_ORDER,
  chapterDisplayTitle,
  chapterLabel,
  formatTypeCounts,
  isGradedKind,
  isItemLive,
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
import { fetchExamMetas, markItemDone, type LessonExamMeta } from "@/services/lessons";
import {
  fetchChaptersStatic,
  fetchClassesStatic,
  fetchLessonWithItemsStatic,
  fetchLessonsStatic,
  retryLessonRevalidate,
  type LessonBundle,
} from "@/services/static-content";
import { fetchMyLessonPageProgress, type ItemProgress } from "@/services/progress";
import type { TheoryStatusResult } from "@/features/progress/types";
import { expandClassIdsByGrade } from "@/services/classes";
import { visibleTo } from "@/services/content";
import { supabaseConfigured } from "@/services/supabase";

/** Một màu nhấn duy nhất cho cả trang — tránh mỗi mục một màu gây phân tâm. */
const ACCENT = "#3B82F6";

/** Nhãn ngắn cho tab — tên đầy đủ (SECTION_META) quá dài để nằm cạnh nhau trên một hàng tab. */
const TAB_LABEL: Record<LessonItemKind, string> = {
  ly_thuyet: "Lý thuyết",
  video: "Video",
  bai_tap_mau: "Bài mẫu",
  luyen_tap: "Luyện tập",
  bai_tap_ve_nha: "BTVN",
  kiem_tra: "Kiểm tra",
};

/** Slug trên URL hash cho từng tab — `#muc=luyen-tap` để chia sẻ link đúng tab đang mở. */
const TAB_SLUG: Record<LessonItemKind, string> = {
  ly_thuyet: "ly-thuyet",
  video: "video",
  bai_tap_mau: "bai-tap-mau",
  luyen_tap: "luyen-tap",
  bai_tap_ve_nha: "btvn",
  kiem_tra: "kiem-tra",
};

const SLUG_TAB = Object.fromEntries(
  Object.entries(TAB_SLUG).map(([kind, slug]) => [slug, kind as LessonItemKind]),
) as Record<string, LessonItemKind>;

/** 3 mức cỡ chữ đọc (A− / A / A+) — nhân vào cỡ chữ gốc của khối nội dung. */
const FONT_SCALES = [0.94, 1, 1.08];
const FONT_STORE = "thachlab-read-font";
const DIM_STORE = "thachlab-read-dim";
const LESSON_DONE_STORE = "thachlab-lesson-done-";
const NOTE_STORE = "thachlab-note-";
/** Mục <h3> lý thuyết đọc dở lần trước, theo lesson_items.id — để "Tiếp tục" trỏ đúng chỗ (L5). */
const THEORY_POS_STORE = "thachlab-theory-pos-";
/** Sự kiện nội bộ: yêu cầu TheoryBlock mở một mục <h3> đang thu gọn trước khi cuộn/tô tới nó
 *  (mục lục, "Ôn ngay", thẻ câu sai) — detail là id `theory-sec-<itemId>-<n>`. */
const OPEN_SECTION_EVENT = "thachlab:open-theory-section";

function requestOpenTheorySection(hashId: string) {
  window.dispatchEvent(new CustomEvent<string>(OPEN_SECTION_EVENT, { detail: hashId }));
}

/**
 * Đọc tab muốn mở từ hash của URL. Nhận cả 2 kiểu:
 *  - `#muc=luyen-tap` — link chia sẻ tab (trang này tự sinh khi bấm tab)
 *  - `#theory-sec-<itemId>-<n>` — link từ trang làm đề / "Ôn ngay" nhảy tới đúng đoạn lý thuyết
 */
function parseTabHash(hash: string): { kind: LessonItemKind | null; theoryId: string | null } {
  const raw = hash.replace(/^#/, "");
  if (raw.startsWith("theory-sec-")) return { kind: "ly_thuyet", theoryId: raw };
  for (const part of raw.split("&")) {
    const value = part.startsWith("muc=") ? part.slice(4) : "";
    if (value && SLUG_TAB[value]) return { kind: SLUG_TAB[value], theoryId: null };
  }
  return { kind: null, theoryId: null };
}

function currentHash() {
  return typeof window === "undefined" ? "" : window.location.hash;
}

/** Cao thêm mà thanh dính (navbar + header bài) che mất khi cuộn tới một đoạn — đo bằng DOM. */
function stickyOffset() {
  const head = document.querySelector<HTMLElement>(".lesson-head");
  return (head?.offsetHeight ?? 0) + 92;
}

/** Cuộn tới một phần tử với chừa chỗ cho thanh dính; không có id thì cuộn về đầu bài. */
function scrollToPart(id: string | null) {
  const target = id ? document.getElementById(id) : null;
  if (target) {
    const y = target.getBoundingClientRect().top + window.scrollY - stickyOffset();
    window.scrollTo({ top: Math.max(0, y), behavior: "smooth" });
  } else {
    window.scrollTo({ top: 0, behavior: "smooth" });
  }
}

/** Đổi hash không thêm vào lịch sử duyệt (bấm tab không làm nút "Quay lại" nhảy lung tung). */
function writeTabHash(hash: string) {
  if (typeof window === "undefined") return;
  window.history.replaceState(null, "", hash || window.location.pathname + window.location.search);
}

/** Cuộn tới + tô vàng một đoạn lý thuyết, tô lại vài nhịp vì bản tĩnh có thể bị bản mới thay thế. */
function flashTheorySection(hashId: string, times = 6) {
  requestOpenTheorySection(hashId); // mục đang thu gọn thì mở ra trước; các nhịp cuộn lại bên dưới sẽ tới đúng chỗ sau khi React dựng xong
  const el = document.getElementById(hashId);
  if (!el) return;
  el.scrollIntoView({ behavior: "smooth", block: "start" });
  el.classList.add("theory-section--highlight");
  let count = 0;
  const reapply = window.setInterval(() => {
    const target = document.getElementById(hashId);
    target?.classList.add("theory-section--highlight");
    count += 1;
    if (count <= times) target?.scrollIntoView({ behavior: "smooth", block: "start" });
  }, 150);
  window.setTimeout(() => {
    window.clearInterval(reapply);
    document.getElementById(hashId)?.classList.remove("theory-section--highlight");
  }, 2600);
}

/** Tô vàng (không giành quyền cuộn) — dùng cho các đoạn phụ khi sai nhiều câu một lúc. */
function highlightTheorySectionOnly(hashId: string) {
  requestOpenTheorySection(hashId);
  document.getElementById(hashId)?.classList.add("theory-section--highlight");
  window.setTimeout(() => document.getElementById(hashId)?.classList.remove("theory-section--highlight"), 2600);
}

/** Vòng tiến độ bằng SVG thuần — không thêm thư viện, không request. */
function ProgressRing({ percent, size = 52 }: { percent: number; size?: number }) {
  const r = (size - 6) / 2;
  const c = 2 * Math.PI * r;
  const value = Math.max(0, Math.min(100, percent));
  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} aria-hidden="true">
      <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="var(--lesson-line)" strokeWidth="5" />
      <circle
        cx={size / 2}
        cy={size / 2}
        r={r}
        fill="none"
        stroke="var(--lesson-accent)"
        strokeWidth="5"
        strokeLinecap="round"
        strokeDasharray={`${(c * value) / 100} ${c}`}
        transform={`rotate(-90 ${size / 2} ${size / 2})`}
      />
      <text x="50%" y="50%" textAnchor="middle" dominantBaseline="central" fill="var(--color-ink)" fontSize={size * 0.27} fontWeight="700">
        {Math.round(value)}%
      </text>
    </svg>
  );
}

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

/** Ý chính/công thức cần thuộc của các mục lý thuyết — đặt ở đầu tab Luyện tập (không còn
 *  nằm trong tab Lý thuyết) để học sinh ôn lại ngay trước khi làm bài. Mặc định THU GỌN chỉ
 *  còn dòng nhãn (bài có nhiều mục lý thuyết thì khối này dài, đẩy câu hỏi xuống xa) — bấm
 *  nhãn mới xổ ra. Rỗng (chưa backfill) thì không hiện gì. */
function TheorySummary({ html, title }: { html: string; title?: string }) {
  const [open, setOpen] = useState(false);
  if (!html.trim()) return null;
  return (
    <div className={`lesson-summary ${open ? "is-open" : ""}`}>
      <button
        type="button"
        className="lesson-summary-toggle"
        onClick={() => setOpen((o) => !o)}
        aria-expanded={open}
      >
        <span className="lesson-summary-label">
          📌 Tóm tắt ý chính cần thuộc{title ? <span className="lesson-summary-title"> · {title}</span> : null}
        </span>
        <ChevronDown size={16} className={open ? "rotate-180" : ""} />
      </button>
      {open && <ContentHtml html={html} className="block leading-relaxed" />}
    </div>
  );
}

/**
 * Lý thuyết: mục bài thứ hai trở đi thu gọn để trang không quá dài. BÊN TRONG một mục, các đoạn
 * <h3> (I., II., III…) cũng chỉ mở đoạn đầu; đoạn sau mở bằng nút "Tiếp" cuối đoạn trước hoặc chạm
 * tiêu đề (N5 segmenting: học sinh bấm "tiếp" chứ không cuộn vô tận — xem
 * docs/PHUONG-PHAP-NOI-DUNG-LY-THUYET.md mục 2, "toàn bộ <h3> render một mạch"). Đoạn đang đọc
 * được ghi vào localStorage để lần mở sau có nút "Tiếp tục ở mục N" (L5), không tự cuộn (B4).
 * Mục lục / "Ôn ngay" / thẻ câu sai trỏ vào đoạn đang thu gọn thì đoạn tự mở (OPEN_SECTION_EVENT).
 */
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
  // Tách theo từng mốc <h3> — cùng hàm với mục lục (tocEntries) và "Ôn ngay" nên id
  // `theory-sec-<itemId>-<n>` khớp nhau; chỉ tính lại khi nội dung mục thật sự đổi.
  const { introHtml, sections } = useMemo(
    () => splitTheorySections(item.body_html, item.id),
    [item.body_html, item.id],
  );
  const total = sections.length;
  const estimate = useMemo(() => estimateTheoryTime(item.body_html), [item.body_html]);
  const [openSections, setOpenSections] = useState<Set<number>>(() => new Set([0]));
  const [allOpen, setAllOpen] = useState(false);
  const [resumeIndex, setResumeIndex] = useState<number | null>(null);
  const rootRef = useRef<HTMLDivElement>(null);
  const isOpen = (i: number) => allOpen || openSections.has(i);
  // Số mốc chưa từng mở — hiện cạnh "Mở tất cả" để biết bài còn bao nhiêu (bản đồ "còn gì").
  const unopenedCount = allOpen ? 0 : Math.max(0, total - openSections.size);

  const openSection = useCallback((index: number) => {
    setOpen(true);
    setOpenSections((prev) => (prev.has(index) ? prev : new Set(prev).add(index)));
  }, []);

  function savePos(index: number) {
    try {
      window.localStorage.setItem(`${THEORY_POS_STORE}${item.id}`, String(index));
    } catch {}
  }

  /** Mở đoạn `index` do học sinh bấm (nút Tiếp / tiêu đề / Tiếp tục) rồi cuộn tới nếu cần. */
  function goTo(index: number, scroll: boolean) {
    openSection(index);
    savePos(index);
    setResumeIndex(null);
    if (scroll) window.setTimeout(() => scrollToPart(sections[index]?.id ?? null), 60);
  }

  // Mục lục / "Ôn ngay" / thẻ câu sai muốn cuộn tới một đoạn đang thu gọn → mở đoạn đó trước.
  useEffect(() => {
    const prefix = `theory-sec-${item.id}-`;
    const onOpen = (e: Event) => {
      const id = (e as CustomEvent<string>).detail;
      if (typeof id !== "string" || !id.startsWith(prefix)) return;
      const index = Number(id.slice(prefix.length));
      if (Number.isInteger(index) && index >= 0) openSection(index);
    };
    window.addEventListener(OPEN_SECTION_EVENT, onOpen);
    return () => window.removeEventListener(OPEN_SECTION_EVENT, onOpen);
  }, [item.id, openSection]);

  /* eslint-disable react-hooks/set-state-in-effect -- đọc localStorage đúng 1 lần lúc có nội dung:
     giá trị khởi tạo useState không đọc được vì trang được prerender tĩnh (window chưa có). */
  useEffect(() => {
    if (total < 2 || done) return;
    try {
      const raw = window.localStorage.getItem(`${THEORY_POS_STORE}${item.id}`);
      const idx = raw == null ? NaN : Number(raw);
      if (Number.isInteger(idx) && idx > 0 && idx < total) setResumeIndex(idx);
    } catch {}
  }, [item.id, total, done]);
  /* eslint-enable react-hooks/set-state-in-effect */

  // Ghi đoạn đang đọc: đoạn ĐÃ MỞ nào vừa đi vào 40% phía trên màn hình (cùng vùng với mục lục).
  useEffect(() => {
    const root = rootRef.current;
    if (!root || total < 2 || !open) return;
    const targets = Array.from(root.querySelectorAll<HTMLElement>('.theory-section[data-open="1"]'));
    if (targets.length === 0) return;
    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((e) => e.isIntersecting)
          .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
        const idx = Number((visible[0]?.target as HTMLElement | undefined)?.dataset.index);
        if (Number.isInteger(idx)) savePos(idx);
      },
      { rootMargin: "-130px 0px -60% 0px", threshold: 0 },
    );
    targets.forEach((t) => observer.observe(t));
    return () => observer.disconnect();
    // savePos chỉ dùng item.id — đã nằm trong deps qua `total`/`open`; openSections/allOpen đổi → danh sách đoạn mở đổi.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [item.id, total, open, openSections, allOpen]);

  const resume = resumeIndex !== null && !isOpen(resumeIndex) ? sections[resumeIndex] : null;

  return (
    <div className={`lesson-block ${hideTitle ? "lesson-block--plain" : ""}`} ref={rootRef}>
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
          {total === 0 ? (
            <ContentHtml html={item.body_html} className="block leading-relaxed" />
          ) : (
            <>
              {total > 1 && (
                <div className="theory-nav">
                  {resume ? (
                    <button type="button" className="theory-next theory-resume" onClick={() => goTo(resumeIndex!, true)}>
                      <small>Tiếp tục · {resumeIndex! + 1}/{total}</small>
                      <strong>{resume.heading}</strong>
                      <Play size={14} fill="currentColor" aria-hidden />
                    </button>
                  ) : (
                    <span>
                      ~{estimate.minutes} phút · {total} mục
                      {estimate.quizzes > 0 ? ` · ${estimate.quizzes} câu tự kiểm tra` : ""}
                    </span>
                  )}
                  <button type="button" className="theory-nav-all" onClick={() => setAllOpen((a) => !a)}>
                    {allOpen ? "Thu gọn" : unopenedCount > 0 ? `Mở tất cả · còn ${unopenedCount} mốc` : "Mở tất cả"}
                  </button>
                </div>
              )}
              {introHtml.trim() !== "" && <ContentHtml html={introHtml} className="block leading-relaxed" />}
              {sections.map((section, i) => {
                const opened = isOpen(i);
                const next = sections[i + 1];
                // Đoạn thu gọn ngay sau một đoạn đang mở đã có nút "Tiếp" ở cuối đoạn đó → không
                // hiện thêm dòng tiêu đề (N4 không lặp); vẫn giữ <div id> để mục lục/"Ôn ngay" cuộn tới.
                const coveredByNext = !opened && i > 0 && isOpen(i - 1);
                return (
                  <div
                    key={section.id}
                    id={section.id}
                    className={`theory-section ${opened ? "" : "theory-section--closed"}`}
                    data-index={i}
                    data-open={opened ? "1" : "0"}
                  >
                    {opened ? (
                      <>
                        <ContentHtml html={section.html} className="block leading-relaxed" />
                        {next && !isOpen(i + 1) && (
                          <button type="button" className="theory-next" onClick={() => goTo(i + 1, true)}>
                            <small>Tiếp · {i + 2}/{total}</small>
                            <strong>{next.heading}</strong>
                            <ArrowRight size={16} aria-hidden />
                          </button>
                        )}
                      </>
                    ) : coveredByNext ? null : (
                      <button
                        type="button"
                        className="theory-section-toggle"
                        aria-expanded={false}
                        onClick={() => goTo(i, false)}
                      >
                        <span>{section.heading}</span>
                        <ChevronDown size={18} aria-hidden />
                      </button>
                    )}
                  </div>
                );
              })}
            </>
          )}
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
  loggedIn,
}: {
  examId: number;
  itemId: number;
  status: TheoryStatusResult | undefined;
  loggedIn: boolean;
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
          {loggedIn ? (
            <span className={tone}>{status?.label ?? "Chưa bắt đầu"}</span>
          ) : (
            <span className="lesson-status">Đăng nhập để làm và lưu kết quả</span>
          )}
        </p>
      </div>
      {loggedIn ? (
        <Link href={`/kiem-tra/lam?id=${examId}&item=${itemId}`} className={attempted ? "lesson-btn-ghost" : "lesson-btn"}>
          {attempted ? "Làm lại" : "Làm kiểm tra nhanh"}
        </Link>
      ) : (
        <Link href="/dang-nhap" className="lesson-btn">
          Đăng nhập để làm
        </Link>
      )}
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

/** Khung xương trong lúc chờ bài học — cùng lớp bố cục (lesson-shell/lesson-layout) để nội dung về không nhảy. */
function LessonSkeleton() {
  return (
    <div className="lesson-shell" aria-busy="true" aria-label="Đang tải bài học">
      <div className="lesson-layout animate-pulse">
        <aside className="lesson-nav" aria-hidden="true">
          <div className="h-4 w-28 rounded bg-white/10" />
          <div className="mt-6 space-y-3">
            {Array.from({ length: 4 }, (_, i) => (
              <div key={i} className="h-4 w-full rounded bg-white/5" />
            ))}
          </div>
        </aside>
        <div className="lesson-main">
          <div className="h-3 w-24 rounded bg-white/10" />
          <div className="mt-4 h-8 w-3/4 rounded bg-white/10" />
          <div className="mt-3 h-4 w-1/2 rounded bg-white/5" />
          <div className="mt-8 space-y-5">
            {Array.from({ length: 3 }, (_, i) => (
              <div key={i} className="rounded-2xl border border-white/10 bg-white/5 p-6">
                <div className="h-5 w-1/3 rounded bg-white/10" />
                <div className="mt-4 h-4 w-full rounded bg-white/5" />
                <div className="mt-2 h-4 w-5/6 rounded bg-white/5" />
                <div className="mt-2 h-4 w-2/3 rounded bg-white/5" />
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

/** Lối thoát khỏi trang bài: thanh đáy toàn site bị ẩn ở đây, nên cần một nút về lại 5 nút chính (Hôm nay…). */
function LessonHomeLink() {
  const { session } = useAuth();
  return (
    <Link href={session ? "/tai-khoan" : "/"} className="lesson-bottom-link lesson-bottom-home" aria-label="Về trang chính">
      <Home size={18} aria-hidden />
    </Link>
  );
}

function LessonLoader() {
  const { session, profile } = useAuth();
  // B1/N1 (docs/QUY-TAC-THIET-KE.md): Trình chiếu là công cụ của người dạy, học sinh không thấy.
  // `profile` đã tính cả chế độ "Xem như học sinh" của admin nên preview hiện đúng giao diện HS.
  const canPresent = profile?.role === "admin" || profile?.role === "instructor" || profile?.role === "tro_giang";
  const searchParams = useSearchParams();
  const id = Number(searchParams.get("id"));
  const classSlug = searchParams.get("class");
  const subjectCode = searchParams.get("subject") ?? "vat-ly";

  const [title, setTitle] = useState("");
  const [chapterTitle, setChapterTitle] = useState("");
  const [chapterId, setChapterId] = useState<number | null>(null);
  const [lessonKind, setLessonKind] = useState<LessonKind>("bai_hoc");
  const [items, setItems] = useState<LessonItem[] | null>(null);
  /** Lời giải bài tập mẫu không nằm trong file tĩnh — theo dõi lượt tải thêm để không hiện lưới trống. */
  const [workedFailedId, setWorkedFailedId] = useState<number | null>(null);
  const workedState: "loading" | "failed" = workedFailedId === id ? "failed" : "loading";
  const [examMetas, setExamMetas] = useState<Map<number, LessonExamMeta>>(new Map());
  const [examMetaStatus, setExamMetaStatus] = useState<"loading" | "error" | "ready">("loading");
  const [scores, setScores] = useState<Map<number, number>>(new Map());
  const [done, setDone] = useState<Set<number>>(new Set());
  const [progress, setProgress] = useState<Map<number, ItemProgress>>(new Map());
  const [error, setError] = useState("");
  const mainRef = useRef<HTMLDivElement>(null);
  // Sáu mục của bài giờ là 6 TAB ngang (trước đây là accordion dọc): một thời điểm chỉ mở một
  // mục, tab đang mở lấy từ hash `#muc=<slug>` để chia sẻ link đúng tab. Tab mặc định là
  // "Lý thuyết" — đúng bằng số công thức KaTeX phải render lúc tải đầu như bản accordion cũ
  // (mục đầu tiên vốn mở sẵn), các tab khác chỉ render khi học sinh bấm.
  const [activeTab, setActiveTab] = useState<LessonItemKind>(() => parseTabHash(currentHash()).kind ?? "ly_thuyet");
  // Công cụ đọc: cỡ chữ 3 mức (A− / A / A+) và chế độ dịu mắt — lưu trên máy, không gửi lên máy chủ.
  const [fontLevel, setFontLevel] = useState(1);
  const [dim, setDim] = useState(false);
  const [fullscreen, setFullscreen] = useState(false);
  const [toolsOpen, setToolsOpen] = useState(false);
  // Chế độ TRÌNH CHIẾU bài giảng — dạy lý thuyết trên lớp, chiếu lên tivi/máy chiếu: lớp phủ
  // toàn màn hình lật từng đoạn lý thuyết theo mốc LỚN I., II., III. (chia khác trang đọc một
  // chút — xem `splitTheorySections` mode "chieu"). Chỉ mount khi bấm nút, và cả component
  // được tải chậm (LessonPresenterLazy) nên phần vẽ tay/điều hướng không nằm trong JS ban đầu.
  const [presenting, setPresenting] = useState(false);
  // "#chieu" trên URL → mở thẳng chế độ trình chiếu (thầy lưu sẵn link cho tiết dạy). Đọc
  // trong effect chứ không phải giá trị khởi tạo của useState: trang này được prerender lúc
  // build (lúc đó chưa có hash), khởi tạo bằng hash sẽ lệch cây DOM khi hydrate. Đẩy sang
  // setTimeout 0 để không setState ngay trong thân effect (gây render chồng).
  useEffect(() => {
    if (currentHash().replace(/^#/, "").toLowerCase() !== "chieu") return;
    const timer = window.setTimeout(() => setPresenting(true), 0);
    return () => window.clearTimeout(timer);
  }, []);
  // Mục lý thuyết đã đăng và có nội dung — nguồn duy nhất cho bộ trang chiếu, không gọi mạng.
  const theoryItems = useMemo(
    () => (items ?? []).filter((item) => item.kind === "ly_thuyet" && item.body_html.trim() !== ""),
    [items],
  );
  // "Đánh dấu đã học xong bài này" ở thanh đáy: không có API lưu cấp-bài (chỉ có API cấp-mục),
  // nên ghi trên máy — nút vẫn phản hồi ngay, tiến độ "x/y mục" cộng thêm 1 khi đã đánh dấu.
  const [lessonMarked, setLessonMarked] = useState(false);
  // Cây chương ở cột trái: chỉ chương đang học mở sẵn, chương khác gấp lại (khoá có thể dài
  // hơn 100 bài nên không xổ hết), và một ô tìm bài lọc ngay trên siblingLessons — không gọi mạng.
  const [treeQuery, setTreeQuery] = useState("");
  /** id của đề mục (h2/h3) đang trong tầm mắt — tô đậm ở "Mục lục bài này". */
  const [activeHeading, setActiveHeading] = useState<string | null>(null);
  /** Tìm trong mục lục: khớp theo itemId trong nội dung bài (không phải tiêu đề đề mục). */
  const [tocQuery, setTocQuery] = useState("");
  /** Ghi chú của em — chỉ lưu trên máy, khoá thachlab-note-<lessonId>. */
  const [note, setNote] = useState("");
  const [noteOpen, setNoteOpen] = useState(false);
  /**
   * Nội dung của tab đang mở chỉ render SAU lần vẽ đầu (1 frame + requestIdleCallback), không
   * nằm trong lần render đầu tiên. Bối cảnh: bản accordion cũ để tất cả 6 mục ĐÓNG nên lúc tải
   * đầu không render công thức nào; tab mặc định "Lý thuyết" thì render 19 nút KaTeX ngay lúc
   * tải (đo được FCP 2,4s → 3,6s, LCP 11,8s → 14,0s, Lighthouse mobile 72 → 67 trên máy local).
   * Hoãn sang sau lần vẽ đầu giữ được FCP/LCP của khung trang; KaTeX vẫn nạp ĐỒNG BỘ (không
   * lazy, không chunk mới) — chỉ thời điểm render nội dung đổi. Đổi tab sau đó hiện ngay.
   */
  const [bodyReady, setBodyReady] = useState(false);
  /** Ngăn kéo "Nội dung khoá" trên điện thoại: gộp cột trái + cột phải vào một bottom sheet. */
  const [drawerOpen, setDrawerOpen] = useState(false);
  const drawerRef = useRef<HTMLDivElement>(null);
  const drawerDragRef = useRef<number | null>(null);
  const [openChapters, setOpenChapters] = useState<Set<number>>(new Set());
  const reviewBannerRef = useRef<HTMLDivElement>(null);
  const bodyRef = useRef<HTMLDivElement>(null);
  // Mục Luyện tập đang làm dở (PracticeSession báo lên) — đổi tab sẽ unmount và mất bài, nên hỏi trước.
  const practiceActiveRef = useRef(false);
  // Thanh tab cuộn ngang: mask mờ mép nào còn tab bị khuất (D4 không phụ thuộc số tab).
  const tabListRef = useRef<HTMLOListElement>(null);
  const [tabOverflow, setTabOverflow] = useState<"" | "left" | "right" | "both">("");
  // Quay lại từ "Ôn ngay" (ExamRunner) qua #theory-sec-<itemId>-<n>: mục lý thuyết đó phải tự
  // mở (mặc định các mục từ thứ hai trở đi đang thu gọn) trước khi cuộn + tô màu tới đúng đoạn.
  const [hashTargetItemId, setHashTargetItemId] = useState<number | null>(() =>
    typeof window !== "undefined" ? theorySectionItemId(window.location.hash) : null,
  );
  // (Tất cả) câu vừa làm sai mang theo từ "Ôn ngay" (đọc 1 lần, service tự xoá khỏi
  // sessionStorage) — hiện thành thẻ dán cố định liệt kê đủ, tô vàng đủ mọi đoạn liên quan,
  // để không quên đang ôn vì sai (những) câu nào — sai nhiều câu ở nhiều đoạn khác nhau vẫn
  // thấy đủ, không chỉ đoạn của câu vừa bấm "Ôn ngay".
  const [reviewContexts, setReviewContexts] = useState<TheoryReviewContext[] | null>(() => {
    if (typeof window === "undefined") return null;
    const ctxs = consumeTheoryReviewContext();
    return ctxs && ctxs[0]?.itemId === hashTargetItemId ? ctxs : null;
  });
  // Mặc định THU GỌN — bản đầy đủ che mất đúng đoạn vừa tô vàng bên dưới, nhất là trên điện
  // thoại (màn hẹp, danh sách nhiều câu dễ chiếm hết màn hình). Thu gọn chỉ còn 1 dòng, bấm để
  // mở/đóng khi cần đọc lại đề.
  const [reviewBannerOpen, setReviewBannerOpen] = useState(false);

  // fetchExamMetas() không trả về đề đang ẩn — sau khi tải xong, bỏ luôn các mã đề
  // ẩn khỏi danh sách hiển thị (đang tải thì cứ giữ nguyên, tránh nhấp nháy).
  function visibleExamIds(ids: number[]) {
    return examMetaStatus === "ready" ? ids.filter((id) => examMetas.has(id)) : ids;
  }

  // Chương trình lớp+môn đầy đủ, chỉ để tính Bài trước/Bài tiếp theo (không phải nội dung bài học).
  const [siblingClasses, setSiblingClasses] = useState<SchoolClass[] | null>(null);
  const [siblingChapters, setSiblingChapters] = useState<Chapter[] | null>(null);
  const [siblingLessons, setSiblingLessons] = useState<Lesson[] | null>(null);

  // Bài + chương + mục: ưu tiên file tĩnh /data/lessons/<id>.json (cùng origin), Supabase đối chiếu
  // ngầm phía sau và thay nội dung nếu đã khác; chương trình lớp (cho Bài trước/sau) tải song song.
  useEffect(() => {
    if (!supabaseConfigured || !id) return;
    let stale = false;
    const apply = (res: LessonBundle | null) => {
      if (stale) return;
      if (!res) {
        setError("Không tìm thấy bài học này.");
        setItems([]);
        return;
      }
      setTitle(res.lesson.title);
      setChapterTitle(res.chapterTitle);
      setChapterId(res.lesson.chapter_id);
      setLessonKind(res.lesson.lesson_kind);
      setItems(res.items.filter(isItemLive));
    };
    fetchLessonWithItemsStatic(id, apply, () => {
      if (!stale) setWorkedFailedId(id);
    }).then(apply);
    return () => {
      stale = true;
    };
  }, [id]);
  // Nút "Tải lại" ở mục bài tập mẫu: đối chiếu lại DB (không reload cả trang, giữ tab/cuộn).
  const retryWorked = useCallback(() => {
    setWorkedFailedId(null);
    retryLessonRevalidate(id).then((res) => {
      if (res === undefined) setWorkedFailedId(id);
      else if (res) setItems(res.items.filter(isItemLive));
    });
  }, [id]);

  useEffect(() => {
    if (!supabaseConfigured) return;
    fetchClassesStatic(setSiblingClasses).then(setSiblingClasses);
    fetchChaptersStatic(setSiblingChapters).then(setSiblingChapters);
    fetchLessonsStatic(setSiblingLessons).then(setSiblingLessons);
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
    // điểm cao nhất, mục đã đánh dấu và trạng thái từng mục: cùng 1 lượt truy vấn song song
    fetchMyLessonPageProgress(session.user.id, items)
      .then(({ progress: nextProgress, scores: nextScores, done: nextDone }) => {
        setProgress(nextProgress);
        setScores(nextScores);
        setDone(nextDone);
      })
      .catch(() => setProgress(new Map()));
  }, [session, items]);

  // Mọi mã đề đã gắn vào bài (luyện tập/kiểm tra/bài tập mẫu/lý thuyết) — nguồn câu hỏi cho
  // "Luyện 10 câu phần này" của LessonMasteryCard, tái dùng examIds đã có sẵn từ items, không
  // thêm truy vấn Supabase mới.
  const lessonExamIds = useMemo(
    () => Array.from(new Set((items ?? []).flatMap((i) => i.exam_ids))),
    [items],
  );

  const sections = useMemo(() => {
    if (!items) return [];
    return SECTION_ORDER.map((kind) => ({ kind, items: items.filter((i) => i.kind === kind) }));
  }, [items]);

  // Học sinh bấm tab → đổi nội dung + ghi hash để link chia sẻ mở đúng tab đó.
  function selectTab(kind: LessonItemKind) {
    setActiveTab(kind);
    writeTabHash(`#muc=${TAB_SLUG[kind]}`);
  }
  // Mở tab theo hash: tự mở (không cuộn) khi hash là link từ trang làm đề / "Ôn ngay".
  // KHÔNG phụ thuộc `items` — dữ liệu tĩnh về sau cũng phải giữ đúng tab đang mở.
  useEffect(() => {
    function applyHash() {
      const hash = currentHash();
      setReviewBannerOpen(false);
      setHashTargetItemId(theorySectionItemId(hash));
      const parsed = parseTabHash(hash);
      if (parsed.kind) selectTab(parsed.kind);
    }
    window.addEventListener("hashchange", applyHash);
    return () => window.removeEventListener("hashchange", applyHash);
  }, []);

  // Khôi phục công cụ đọc đã lưu trên máy + trạng thái "đã học xong bài này". So sánh trước khi
  // set để không tạo thêm vòng render (và không vi phạm react-hooks/set-state-in-effect).
  /* eslint-disable react-hooks/set-state-in-effect -- đọc localStorage đúng 1 lần lúc mở bài:
     không có cách đọc khi SSR, và mỗi nhánh đã so sánh trước khi set nên không sinh vòng render thừa. */
  useEffect(() => {
    try {
      // Number(null) === 0 ⇒ chưa có gì đã lưu thì phải giữ mức mặc định, không rơi về A−.
      const rawFont = window.localStorage.getItem(FONT_STORE);
      const savedFont = rawFont === null ? null : Number(rawFont);
      if (
        savedFont !== null &&
        Number.isInteger(savedFont) &&
        savedFont >= 0 &&
        savedFont < FONT_SCALES.length &&
        savedFont !== fontLevel
      ) {
        setFontLevel(savedFont);
      }
      const savedDim = window.localStorage.getItem(DIM_STORE) === "1";
      if (savedDim !== dim) setDim(savedDim);
      const savedDone = window.localStorage.getItem(`${LESSON_DONE_STORE}${id}`) === "1";
      if (savedDone !== lessonMarked) setLessonMarked(savedDone);
      const savedNote = window.localStorage.getItem(`${NOTE_STORE}${id}`) ?? "";
      if (savedNote !== note) setNote(savedNote);
      if (savedNote) setNoteOpen(true);
    } catch {}
    // Chỉ khôi phục 1 lần khi mở bài (theo id) — thêm dim/fontLevel/lessonMarked vào deps sẽ
    // làm effect chạy lại sau mỗi lần đổi cỡ chữ và ghi đè lựa chọn vừa bấm.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);
  /* eslint-enable react-hooks/set-state-in-effect */

  useEffect(() => {
    let idle: number | undefined;
    const timer = window.setTimeout(() => {
      if (typeof window.requestIdleCallback === "function") {
        idle = window.requestIdleCallback(() => setBodyReady(true), { timeout: 300 });
      } else {
        setBodyReady(true);
      }
    }, 0);
    return () => {
      window.clearTimeout(timer);
      if (idle !== undefined) window.cancelIdleCallback(idle);
    };
    // Chỉ 1 lần cho mỗi bộ dữ liệu: sau lần vẽ đầu thì đổi tab hiện nội dung ngay (đúng cảm giác
  // "một cú bấm là thấy"), không phải chờ thêm nhịp nào nữa.
  }, [items]);

  // Đổi cỡ chữ thì đổi cỡ chữ gốc của khối nội dung (--lesson-read-scale), không nhân từng
  // phần tử — công thức KaTeX (đơn vị em) cũng to lên theo.
  useEffect(() => {
    bodyRef.current?.style.setProperty("--lesson-read-scale", String(FONT_SCALES[fontLevel]));
  }, [fontLevel, items, activeTab]);

  /**
   * Công bố chiều cao THẬT của thanh đáy lên :root để CSS chừa đúng chỗ — nội dung cuối (footer)
   * không bị thanh đáy che ở mọi bề rộng (kể cả khi chữ hệ thống to làm nhãn xuống dòng).
   */
  useEffect(() => {
    const bar = document.querySelector<HTMLElement>(".lesson-bottombar");
    if (!bar) return;
    const publish = () => {
      const height = bar.offsetHeight;
      // 0px = thanh đang ẩn (ngăn kéo mở, hoặc màn hình ≥640) — giữ số cũ để trang không nhảy.
      if (height > 0) document.documentElement.style.setProperty("--lesson-bottombar-h", `${height}px`);
    };
    publish();
    const observer = new ResizeObserver(publish);
    observer.observe(bar);
    return () => {
      observer.disconnect();
      document.documentElement.style.removeProperty("--lesson-bottombar-h");
    };
  }, [items]);

  // Chỉ ghi lại sau khi đã khôi phục xong — nếu không, lần render đầu (mức mặc định) sẽ ghi đè
  // lựa chọn đã lưu của học sinh trước khi effect khôi phục kịp chạy.
  // Bỏ qua lần chạy đầu (giá trị mặc định) — nếu không, lần render đầu sẽ ghi 1rem/mặc định
  // đè lên lựa chọn đã lưu TRƯỚC KHI effect khôi phục kịp đọc lại.
  const skipFirstPersistRef = useRef(true);
  useEffect(() => {
    if (skipFirstPersistRef.current) {
      skipFirstPersistRef.current = false;
      return;
    }
    try {
      window.localStorage.setItem(FONT_STORE, String(fontLevel));
    } catch {}
  }, [fontLevel]);

  const skipFirstDimRef = useRef(true);
  useEffect(() => {
    if (skipFirstDimRef.current) {
      skipFirstDimRef.current = false;
      return;
    }
    try {
      if (dim) window.localStorage.setItem(DIM_STORE, "1");
      else window.localStorage.removeItem(DIM_STORE);
    } catch {}
  }, [dim]);

  // Ngăn kéo: Esc để đóng, và khoá cuộn trang nền khi đang mở (không thì cuộn ngăn kéo lại
  // kéo theo cả bài phía sau).
  useEffect(() => {
    if (!drawerOpen) return;
    function onKey(e: KeyboardEvent) {
      if (e.key === "Escape") setDrawerOpen(false);
    }
    const previous = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    document.addEventListener("keydown", onKey);
    return () => {
      document.body.style.overflow = previous;
      document.removeEventListener("keydown", onKey);
    };
  }, [drawerOpen]);

  /** Vuốt xuống ở đầu ngăn kéo để đóng (ngưỡng 90px). */
  function onDrawerTouchStart(e: TouchEvent) {
    drawerDragRef.current = e.touches[0]?.clientY ?? null;
  }
  function onDrawerTouchMove(e: TouchEvent) {
    const start = drawerDragRef.current;
    const current = e.touches[0]?.clientY;
    if (start == null || current == null) return;
    drawerRef.current?.style.setProperty("--lesson-drawer-drag", `${Math.max(0, current - start)}px`);
  }
  function onDrawerTouchEnd() {
    const sheet = drawerRef.current;
    const moved = Number((sheet?.style.getPropertyValue("--lesson-drawer-drag") ?? "0px").replace("px", "")) || 0;
    sheet?.style.removeProperty("--lesson-drawer-drag");
    drawerDragRef.current = null;
    if (moved > 90) setDrawerOpen(false);
  }

  // Trạng thái toàn màn hình (học sinh thoát bằng Esc thì nút phải trở lại bình thường).
  useEffect(() => {
    function onChange() {
      setFullscreen(document.fullscreenElement === mainRef.current && mainRef.current != null);
    }
    document.addEventListener("fullscreenchange", onChange);
    return () => document.removeEventListener("fullscreenchange", onChange);
  }, []);

  function toggleFullscreen() {
    const el = mainRef.current;
    if (!el) return;
    if (document.fullscreenElement) void document.exitFullscreen();
    else void el.requestFullscreen?.().catch(() => setFullscreen(false));
  }

  function markLessonDone() {
    setLessonMarked(true);
    try {
      window.localStorage.setItem(`${LESSON_DONE_STORE}${id}`, "1");
    } catch {}
  }

  // Mục lục bài này: theo dõi h2/h3 của TAB ĐANG MỞ (nội dung soạn sẵn sinh ra id), không gọi
  // mạng. Quan sát lại mỗi khi đổi tab / có dữ liệu mới vì panel được dựng lại.
  useEffect(() => {
    const root = bodyRef.current;
    if (!root) return;
    const targets = Array.from(root.querySelectorAll<HTMLElement>("h2[id], h3[id]"));
    if (targets.length === 0) return;
    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((e) => e.isIntersecting)
          .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
        if (visible[0]) setActiveHeading(visible[0].target.id);
      },
      { rootMargin: "-130px 0px -65% 0px", threshold: 0 },
    );
    targets.forEach((t) => observer.observe(t));
    return () => observer.disconnect();
  }, [activeTab, items]);

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

  // Phạm vi "khoá đang học": chương cùng môn và cùng khối lớp đang xem (theo ?class= — dùng lại
  // đúng luật hiển thị chương của trang lớp, không tự suy luận lớp khác khi chưa chắc). Vừa dùng
  // cho cây chương cột trái, vừa là nguồn tính Bài trước/Bài sau — không thêm request nào.
  const courseChapters = useMemo((): { chapter: Chapter; lessons: Lesson[] }[] => {
    if (!siblingChapters || !siblingLessons || !siblingClasses || chapterId == null) return [];
    const currentChapter = siblingChapters.find((c) => c.id === chapterId);
    if (!currentChapter) return [];
    const activeClass = classSlug ? siblingClasses.find((c) => c.slug === classSlug) : undefined;
    const scopeClassId = activeClass?.id ?? currentChapter.classIds[0];
    const visibleClassIds = scopeClassId !== undefined ? expandClassIdsByGrade([scopeClassId], siblingClasses) : null;
    return siblingChapters
      .filter((ch) => ch.subjectCode === currentChapter.subjectCode && visibleTo(ch.classIds, visibleClassIds))
      .sort((a, b) => a.sort_order - b.sort_order || a.id - b.id)
      .map((chapter) => {
        const inChapter = siblingLessons.filter((l) => l.chapter_id === chapter.id);
        return {
          chapter,
          lessons: [
            ...inChapter.filter((l) => !isSemesterExam(l.lesson_kind)),
            ...inChapter.filter((l) => isSemesterExam(l.lesson_kind)),
          ],
        };
      })
      .filter((entry) => entry.lessons.length > 0);
  }, [siblingChapters, siblingLessons, siblingClasses, chapterId, classSlug]);

  const courseLessons = useMemo(() => courseChapters.flatMap((entry) => entry.lessons), [courseChapters]);

  // "Chương N · Tên" — nhãn dùng chung cho breadcrumb, link quay lại và tiêu đề ngăn kéo, để
  // trang bài nói cùng một thứ tiếng với trang chương (số chương lấy theo vị trí trong khoá).
  const chapterFullLabel = useMemo(() => {
    const idx = courseChapters.findIndex((e) => e.chapter.id === chapterId);
    if (idx < 0) return chapterDisplayTitle(chapterTitle);
    return chapterLabel(idx, courseChapters[idx].chapter.title);
  }, [courseChapters, chapterId, chapterTitle]);

  // Bài trước/Bài tiếp theo: thứ tự bài trong cùng lớp và môn (xem courseChapters ở trên).
  const { prevLesson, nextLesson } = useMemo((): { prevLesson: Lesson | null; nextLesson: Lesson | null } => {
    const idx = courseLessons.findIndex((l) => l.id === id);
    if (idx === -1) return { prevLesson: null, nextLesson: null };
    return {
      prevLesson: idx > 0 ? courseLessons[idx - 1] : null,
      nextLesson: idx < courseLessons.length - 1 ? courseLessons[idx + 1] : null,
    };
  }, [courseLessons, id]);

  /** Bài đã học xong = mọi mục học liệu của bài đều đã đánh dấu/đã làm đề. */
  function lessonComplete(lesson: Lesson): boolean {
    if (!session || !items || lesson.id !== id) return false;
    return items.length > 0 && items.every(isDone);
  }

  // Chương đang học mở sẵn; đang tìm bài thì mở luôn chương có kết quả khớp.
  const matchingLessonIds = useMemo(() => {
    const q = treeQuery.trim().toLowerCase();
    if (!q) return null;
    return new Set(courseLessons.filter((l) => l.title.toLowerCase().includes(q)).map((l) => l.id));
  }, [courseLessons, treeQuery]);

  // Cây chương (ChapterTree) là component thuần: trang tự quyết chương nào đang mở rồi truyền xuống.
  const openChapterIds = useMemo(() => {
    const ids = new Set<number>();
    for (const { chapter, lessons } of courseChapters) {
      if (
        openChapters.has(chapter.id) ||
        (matchingLessonIds ? lessons.some((l) => matchingLessonIds.has(l.id)) : chapter.id === chapterId)
      ) {
        ids.add(chapter.id);
      }
    }
    return ids;
  }, [courseChapters, openChapters, matchingLessonIds, chapterId]);

  function toggleChapter(chapterIdInTree: number) {
    setOpenChapters((prev) => {
      const next = new Set(prev);
      if (next.has(chapterIdInTree)) next.delete(chapterIdInTree);
      else next.add(chapterIdInTree);
      return next;
    });
  }

  function siblingHref(lesson: Lesson) {
    const params = new URLSearchParams({ id: String(lesson.id), subject: subjectCode, chapter: String(lesson.chapter_id) });
    if (classSlug) params.set("class", classSlug);
    return `/lop-hoc/bai?${params.toString()}`;
  }

  const visibleSections = sections.filter((s) => s.items.length > 0);
  // Đo thanh tab còn khuất tab nào ở mép trái/phải (resize + cuộn) → CSS mask đúng mép đó.
  useEffect(() => {
    const ol = tabListRef.current;
    if (!ol) return;
    const measure = () => {
      const max = ol.scrollWidth - ol.clientWidth;
      if (max <= 2) return setTabOverflow("");
      const left = ol.scrollLeft > 2;
      const right = ol.scrollLeft < max - 2;
      setTabOverflow(left && right ? "both" : left ? "left" : right ? "right" : "");
    };
    measure();
    ol.addEventListener("scroll", measure, { passive: true });
    const ro = typeof ResizeObserver !== "undefined" ? new ResizeObserver(measure) : null;
    ro?.observe(ol);
    window.addEventListener("resize", measure);
    return () => {
      ol.removeEventListener("scroll", measure);
      ro?.disconnect();
      window.removeEventListener("resize", measure);
    };
  }, [visibleSections.length]);

  const activeKind: LessonItemKind | undefined = visibleSections.some((s) => s.kind === activeTab)
    ? activeTab
    : visibleSections[0]?.kind;
  const activeSection = visibleSections.find((s) => s.kind === activeKind);
  // Mục lục của TAB đang mở: các h2/h3 có id trong nội dung soạn sẵn. Lấy từ items (không đọc
  // DOM, không gọi mạng) nên hiện được ngay, kể cả trước khi panel kịp paint.
  const tocEntries = useMemo(() => {
    const out: { id: string; itemTitle: string; heading: string }[] = [];
    for (const item of items ?? []) {
      if (item.kind !== activeTab) continue;
      // Dùng lại đúng hàm sinh id mà TheoryContent dùng khi render (theory-sec-<itemId>-<i>) —
      // không đoán id bằng tay, và không đọc DOM.
      const { sections: parts } = wrapTheorySections(item.body_html, item.id);
      if (parts.length > 0) {
        for (const part of parts) out.push({ id: part.id, itemTitle: item.title, heading: part.heading });
      } else {
        // Không có đề mục nhỏ (tab video/luyện tập/BTVN/kiểm tra) → mục lục là chính các mục.
        out.push({ id: `lesson-item-${item.id}`, itemTitle: item.title, heading: "" });
      }
    }
    return out;
  }, [items, activeTab]);

  const shownToc = useMemo(() => {
    const q = tocQuery.trim().toLowerCase();
    if (!q) return tocEntries;
    return tocEntries.filter(
      (entry) => entry.heading.toLowerCase().includes(q) || entry.itemTitle.toLowerCase().includes(q),
    );
  }, [tocEntries, tocQuery]);


  // Ghi chú: chỉ lưu trên máy, ghi sau khi học sinh ngừng gõ 400ms để không ghi localStorage
  // liên tục theo từng ký tự.
  const skipFirstNoteRef = useRef(true);
  useEffect(() => {
    if (skipFirstNoteRef.current) {
      skipFirstNoteRef.current = false;
      return;
    }
    const timer = window.setTimeout(() => {
      try {
        if (note) window.localStorage.setItem(`${NOTE_STORE}${id}`, note);
        else window.localStorage.removeItem(`${NOTE_STORE}${id}`);
      } catch {}
    }, 400);
    return () => window.clearTimeout(timer);
  }, [note, id]);
  // Đến từ "Tiếp tục học" (resume=1): mở tab chứa mục đầu tiên chưa hoàn thành rồi cuộn tới đó;
  // không xác định được (chưa đăng nhập, đã xong hết…) thì cứ mở bài bình thường ở đầu trang.
  useEffect(() => {
    if (searchParams.get("resume") !== "1" || !session || !items || items.length === 0) return;
    const firstIncomplete = items.find((item) => !isDone(item));
    if (!firstIncomplete) return;
    const timer = window.setTimeout(() => {
      selectTab(firstIncomplete.kind);
      scrollToPart(`secondary-stage-${firstIncomplete.kind}`);
    }, 220);
    return () => window.clearTimeout(timer);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [searchParams, items, session, done, scores]);

  // Quay lại từ "Ôn ngay" (#theory-sec-<itemId>-<n>): cuộn + tô vàng tạm đúng đoạn lý thuyết
  // liên quan tới câu vừa làm sai. Tô màu bằng classList trực tiếp, KHÔNG qua state đổi html
  // của ContentHtml — nếu đổi, dangerouslySetInnerHTML thay cả node đang cuộn tới, huỷ luôn
  // animation scrollIntoView giữa chừng (đã tự kiểm khi làm pilot, xem lịch sử sửa).
  //
  // reviewContexts (đọc snapshot 1 lần qua ref, KHÔNG qua state trong deps của effect dưới) —
  // đóng thẻ nhắc không được kích lại hiệu ứng cuộn/tô, chỉ đóng UI.
  const reviewContextsRef = useRef(reviewContexts);

  // KHÔNG được chỉ chạy 1 lần: trang này ưu tiên hiển thị bản tĩnh build sẵn trước
  // (fetchLessonWithItemsStatic), rồi âm thầm đối chiếu với Supabase và render lại bằng bản
  // mới nếu khác (revalidateLesson trong services/static-content.ts) — nếu chỉ tô màu 1 lần
  // ngay khi có `items` đầu tiên (bản tĩnh, có thể đã cũ), khối vừa tô sẽ bị bản mới thay mất
  // (dangerouslySetInnerHTML dựng lại DOM) mà không tô lại. Tự kiểm bằng epoch timestamp thấy
  // đúng vậy: tô lúc t, mất trước 6s dù hẹn giờ tắt là 30s → do bản mới đè lên, không phải do
  // hẹn giờ. Nên bỏ cờ "đã làm 1 lần", chạy lại mỗi khi `items` đổi — vô hại vì lần cuối cùng
  // (ứng với bản dữ liệu ổn định) sẽ luôn thắng.
  useEffect(() => {
    if (!items || items.length === 0) return;
    const hash = window.location.hash.replace(/^#/, "");
    const contexts = reviewContextsRef.current;
    const timer = window.setTimeout(() => {
      if (contexts && contexts.length > 0) {
        const ids = contexts.map((ctx) => `theory-sec-${ctx.itemId}-${ctx.sectionIndex}`);
        let primaryId = ids[0];
        if (hash.startsWith("theory-sec-") && ids.includes(hash)) primaryId = hash;
        ids.forEach((hid) => {
          if (hid === primaryId) flashTheorySection(hid);
          else highlightTheorySectionOnly(hid);
        });
      } else if (hash.startsWith("theory-sec-")) {
        flashTheorySection(hash);
      }
    }, 200);
    return () => window.clearTimeout(timer);
  }, [items]);

  if (!id) return <p className="lesson-notice">Thiếu mã bài học trong địa chỉ.</p>;
  if (error) return <p className="lesson-notice text-red-400">{error}</p>;
  if (!items) return <LessonSkeleton />;

  const classHref = classSlug
    ? `/lop-hoc/${classSlug}?subject=${encodeURIComponent(subjectCode)}${chapterId ? `&chapter=${chapterId}#chapter-${chapterId}` : ""}`
    : "/lop-hoc";

  if (isPeriodicExam(lessonKind)) {
    const kindMeta = LESSON_KIND_META[lessonKind];
    const kiemTraItems = items.filter((i) => i.kind === "kiem_tra");
    const examIds = visibleExamIds(kiemTraItems.flatMap((i) => i.exam_ids));
    const itemByExamId = new Map(kiemTraItems.flatMap((i) => i.exam_ids.map((eid) => [eid, i])));
    return (
      <div className={`lesson-shell lesson-page ${drawerOpen ? "is-drawer-open" : ""}`}>
        <div className="lesson-layout lesson-layout--exam">
          <aside className="lesson-nav lesson-nav--compact" aria-label="Điều hướng bài học">
            {prevLesson && (
              <Link href={siblingHref(prevLesson)} className="lesson-nav-step">
                <small>‹ Bài trước</small>
                <span>{prevLesson.title}</span>
              </Link>
            )}
            {nextLesson && (
              <Link href={siblingHref(nextLesson)} className="lesson-nav-step lesson-nav-step--next">
                <small>Bài sau ›</small>
                <span>{nextLesson.title}</span>
              </Link>
            )}
          </aside>

          <div className="lesson-main">
            <header className="lesson-head">
              <button type="button" className="lesson-head-back" onClick={() => window.history.back()} aria-label="Quay lại">
                <ArrowLeft size={16} aria-hidden />
              </button>
              <div className="lesson-head-text">
                <nav className="lesson-breadcrumb" aria-label="Đường dẫn">
                  <span className="lesson-crumb-class">
                    <Link href="/lop-hoc">Lớp học</Link>
                    <span aria-hidden className="lesson-crumb-sep">›</span>
                  </span>
                  <Link href={classHref} className="lesson-crumb-chapter">
                    {chapterFullLabel || "Chương"}
                  </Link>
                </nav>
                <h1>{title}</h1>
                <div className="lesson-meta">
                  <span className="lesson-meta-chip">{kindMeta.label}</span>
                  <span>{examIds.length} đề</span>
                </div>
              </div>
              <button
                type="button"
                className="lesson-drawer-toggle"
                onClick={() => setDrawerOpen(true)}
                aria-expanded={drawerOpen}
                aria-controls="lesson-drawer"
                aria-label="Mở mục lục khoá học"
              >
                <Menu size={17} aria-hidden />
              </button>
            </header>
            <p className="lesson-lead">Làm bài trực tuyến, hệ thống chấm điểm tự động.</p>
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
          </div>
        </div>

        <nav className="lesson-bottombar lesson-bottombar--mobile lesson-bottombar--home" aria-label="Điều hướng bài học">
        <LessonHomeLink />
          <button
            type="button"
            className="lesson-bottom-link"
            onClick={() => setDrawerOpen(true)}
            aria-expanded={drawerOpen}
            aria-controls="lesson-drawer"
          >
            <Menu size={16} aria-hidden />
            <span>Mục lục</span>
          </button>
          {prevLesson ? (
            <Link href={siblingHref(prevLesson)} className="lesson-bottom-link" title={prevLesson.title}>
              <ArrowLeft size={16} aria-hidden />
              <span>Bài trước</span>
            </Link>
          ) : (
            <span className="lesson-bottom-link is-empty" aria-hidden>
              <ArrowLeft size={16} />
              <span>Bài trước</span>
            </span>
          )}
          <span className="lesson-bottom-step">Đề kiểm tra</span>
          {nextLesson ? (
            <Link href={siblingHref(nextLesson)} className="lesson-bottom-link lesson-bottom-link--next" title={nextLesson.title}>
              <span>Bài sau</span>
              <ArrowRight size={16} aria-hidden />
            </Link>
          ) : (
            <span className="lesson-bottom-link lesson-bottom-link--next is-empty" aria-hidden>
              <span>Bài sau</span>
              <ArrowRight size={16} />
            </span>
          )}
        </nav>

        {drawerOpen && (
          <div className="lesson-drawer" role="dialog" aria-modal="true" aria-label={`Nội dung khoá ${chapterFullLabel}`}>
            <button type="button" className="lesson-drawer-scrim" aria-label="Đóng mục lục" onClick={() => setDrawerOpen(false)} />
            <div
              id="lesson-drawer"
              className="lesson-drawer-sheet"
              ref={drawerRef}
              onTouchStart={onDrawerTouchStart}
              onTouchMove={onDrawerTouchMove}
              onTouchEnd={onDrawerTouchEnd}
            >
              <div className="lesson-drawer-head">
                <p className="lesson-drawer-title">Nội dung khoá {chapterFullLabel || ""}</p>
                <button type="button" onClick={() => setDrawerOpen(false)} aria-label="Đóng mục lục">
                  <X size={17} aria-hidden />
                </button>
              </div>
              <div className="lesson-drawer-body">
                <ChapterTree
                  entries={courseChapters}
                  mode="learn"
                  currentLessonId={id}
                  openChapterIds={openChapterIds}
                  onToggleChapter={toggleChapter}
                  lessonHref={siblingHref}
                  isLessonDone={lessonComplete}
                  showProgress={!!session}
                  filterLessonIds={matchingLessonIds}
                />
              </div>
            </div>
          </div>
        )}
      </div>
    );
  }


  const activeIndex = activeSection ? visibleSections.findIndex((s) => s.kind === activeSection.kind) : -1;
  const nextSection = activeIndex >= 0 ? visibleSections[activeIndex + 1] : undefined;
  const totalTabs = visibleSections.length;
  const doneTabs = visibleSections.filter((s) => !!session && s.items.every(isDone)).length;
  const progressDone = Math.min(totalTabs, doneTabs + (lessonMarked ? 1 : 0));

  const assignmentItem = items.find((i) => i.kind === "bai_tap_ve_nha" && i.due_at);
  const lessonTypeLabel = LESSON_KIND_META[lessonKind]?.label ?? "Bài học";
  const lessonTheoryPassed = !!session && progress.get(assignmentItem?.id ?? -1)?.theory?.status === "passed";
  // N4: chip "Bài học" và đếm "4 mục · 4 phần" bị bỏ (tab ngay dưới đã cho biết) — chỉ giữ thứ có ích.
  const hasLessonMeta = lessonKind !== "bai_hoc" || !!assignmentItem?.due_at || lessonTheoryPassed;
  const stepLabel = lessonMarked ? "Đã học xong" : `Mục ${Math.max(activeIndex, 0) + 1}/${totalTabs || 1}`;

  // Mục lục bài này = các h2/h3 có id trong TAB đang mở (heading do nội dung soạn sẵn sinh ra).
  // Cột phải dùng; ở bước này chỉ cần activeHeading được cập nhật.

  function selectTabAndScroll(kind: LessonItemKind) {
    if (
      kind !== activeTab &&
      practiceActiveRef.current &&
      !confirm("Em đang luyện tập dở — đổi mục sẽ mất bài đang làm (chưa nộp, chưa lưu). Vẫn đổi?")
    )
      return;
    const target = kind === activeTab ? bodyRef.current : null;
    const firstItemId = target?.querySelector<HTMLElement>("[data-item]")?.dataset.item ?? null;
    selectTab(kind);
    window.setTimeout(() => scrollToPart(firstItemId), 60);
  }

  /** Nội dung của đúng tab đang mở — tách riêng vì commit sau còn dùng lại ở ngăn kéo. */
  function renderSectionItems(section: { kind: LessonItemKind; items: LessonItem[] }) {
    const plain = section.items.length === 1;
    return section.items.map((item, itemIndex) => {
      // Mục duy nhất của phần → tiêu đề riêng (thường là "<Loại> — <tên bài>")
      // chỉ lặp lại ý tiêu đề phần "N. <Tên phần>" ngay trên, ẩn cho đỡ trùng.
      // Phụ đề (hạn nộp, số câu…) vẫn hiện bình thường.
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
          <div key={item.id} id={`lesson-item-${item.id}`} className="lesson-stack" data-item={item.id}>
            <TheoryBlock
              item={item}
              defaultOpen={itemIndex === 0 || item.id === hashTargetItemId}
              hideTitle={plain}
              done={done.has(item.id)}
              loggedIn={!!session}
              onDone={() => markDone(item)}
            />
            {item.exam_ids.length > 0 && (
              <TheoryQuizBlock
                examId={item.exam_ids[0]}
                itemId={item.id}
                status={progress.get(item.id)?.theory}
                loggedIn={!!session}
              />
            )}
          </div>
        );

      if (isGradedKind(item.kind)) {
        const gradedExamIds = visibleExamIds(item.exam_ids);
        return (
          <div key={item.id} id={`lesson-item-${item.id}`} className="lesson-block" data-item={item.id}>
            {(!plain || item.due_at) && (
              <div className="lesson-block-head">
                {!plain && <p className="lesson-block-title">{item.title}</p>}
                {item.due_at && <p className="lesson-block-sub">Hạn nộp: {formatDue(item.due_at)}</p>}
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
      const showSummaries = item.kind === "luyen_tap" && itemIndex === 0;
      return (
        <div key={item.id} id={`lesson-item-${item.id}`} className="lesson-block" data-item={item.id}>
          {showSummaries && (
            <div className="mb-4">
              {(items ?? [])
                .filter((i) => i.kind === "ly_thuyet")
                .map((t) => (
                  <TheorySummary key={t.id} html={t.summary_html} title={t.title} />
                ))}
            </div>
          )}
          {(!plain || item.subtitle) && (
            <div className="lesson-block-head">
              {!plain && <p className="lesson-block-title">{item.title}</p>}
              {item.subtitle && <p className="lesson-block-sub">{item.subtitle}</p>}
            </div>
          )}
          {item.kind === "bai_tap_mau" ? (
            <>
              {item.exam_ids.length > 0 && <SampleQuestionsGrid examIds={item.exam_ids} color={ACCENT} />}
              {item.questions.length === 0 && (item.questions_count ?? 0) > 0 ? (
                // DB có dạng bài nhưng lời giải chưa về (file tĩnh không chứa): báo rõ, không để lưới trống (N3, L4).
                <p className="lesson-block-sub" role="status" aria-live="polite">
                  {workedState === "failed" ? (
                    <>
                      Chưa tải được {item.questions_count} dạng bài.{" "}
                      <button type="button" className="lesson-btn-ghost" onClick={retryWorked}>
                        Tải lại
                      </button>
                    </>
                  ) : (
                    `Đang tải ${item.questions_count} dạng bài…`
                  )}
                </p>
              ) : (
                <WorkedQuestionsGrid questions={item.questions} color={ACCENT} />
              )}
            </>
          ) : (
            <PracticeSession
              examIds={item.exam_ids}
              poolExamIds={lessonExamIds}
              lessonId={id}
              itemId={item.id}
              passScore={item.practice_pass_score}
              color={ACCENT}
              onActiveChange={(active) => {
                practiceActiveRef.current = active;
              }}
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
    });
  }

  /** Thanh tab (một tablist duy nhất cho mọi cỡ màn hình — CSS lo kiểu dáng): badge số mục, dấu ✓
      khi xong, chấm cam ở phần có hạn nộp còn dang dở, tab đang mở gạch chân màu nhấn. Phím ←/→,
      Home/End chuyển tab theo mẫu ARIA tabs (kích hoạt tự động, tabindex xoay vòng). */
  function onTabKeyDown(e: ReactKeyboardEvent<HTMLOListElement>) {
    const kinds = visibleSections.map((sec) => sec.kind);
    const i = kinds.indexOf(activeTab);
    if (i < 0 || kinds.length === 0) return;
    let next = i;
    if (e.key === "ArrowRight") next = (i + 1) % kinds.length;
    else if (e.key === "ArrowLeft") next = (i - 1 + kinds.length) % kinds.length;
    else if (e.key === "Home") next = 0;
    else if (e.key === "End") next = kinds.length - 1;
    else return;
    e.preventDefault();
    if (next === i) return;
    selectTabAndScroll(kinds[next]);
    document.getElementById(`lesson-tab-${kinds[next]}`)?.focus();
  }
  const tabNav = (
    <nav className={`lesson-tabs ${tabOverflow ? `is-overflow-${tabOverflow}` : ""}`} aria-label="Các mục của bài học">
      <ol role="tablist" ref={tabListRef} onKeyDown={onTabKeyDown}>
        {visibleSections.map((section) => {
          const active = section.kind === activeTab;
          const complete = !!session && section.items.every(isDone);
          const dueOpen = !complete && section.items.some((it) => !!it.due_at && !isDone(it));
          return (
            <li key={section.kind}>
              <button
                type="button"
                role="tab"
                id={`lesson-tab-${section.kind}`}
                className={`${active ? "is-active" : ""} ${complete ? "is-complete" : ""}`}
                aria-selected={active}
                aria-controls={active ? `secondary-stage-${section.kind}` : undefined}
                tabIndex={active ? 0 : -1}
                onClick={() => selectTabAndScroll(section.kind)}
              >
                {complete && <Check size={13} aria-hidden />}
                <span>{TAB_LABEL[section.kind]}</span>
                {section.items.length > 1 && <i>{section.items.length}</i>}
                {dueOpen && (
                  <em className="lesson-tab-due" title="Có hạn nộp">
                    <span className="sr-only">, có hạn nộp</span>
                  </em>
                )}
              </button>
            </li>
          );
        })}
      </ol>
    </nav>
  );

  const readToolButton = (
    <button
      type="button"
      className={`lesson-tool-toggle ${dim ? "is-on" : ""}`}
      onClick={() => setToolsOpen((o) => !o)}
      aria-expanded={toolsOpen}
      aria-label="Công cụ đọc: cỡ chữ và chế độ dịu mắt"
    >
      Aa
    </button>
  );

  const readTools = (
    <>
      <button
        type="button"
        className={`lesson-tool ${dim ? "is-on" : ""}`}
        onClick={() => setDim((d) => !d)}
        aria-pressed={dim}
        title="Nền dịu mắt, chữ đậm hơn — đọc lâu đỡ mỏi"
      >
        <Eye size={14} aria-hidden />
        <span>Dịu mắt</span>
      </button>
      <div className="lesson-fonttools">
        <button
          type="button"
          onClick={() => setFontLevel((v) => Math.max(0, v - 1))}
          disabled={fontLevel === 0}
          aria-label="Cỡ chữ nhỏ hơn"
        >
          A−
        </button>
        <button
          type="button"
          onClick={() => setFontLevel((v) => Math.min(FONT_SCALES.length - 1, v + 1))}
          disabled={fontLevel === FONT_SCALES.length - 1}
          aria-label="Cỡ chữ lớn hơn"
        >
          A+
        </button>
      </div>
      {canPresent && theoryItems.length > 0 && (
        <button
          type="button"
          className="lesson-tool"
          onClick={() => setPresenting(true)}
          title="Chiếu lên tivi / máy chiếu: lật từng mục, bút khoanh ý chính, phóng to chữ"
        >
          <MonitorPlay size={14} aria-hidden />
          <span className="lesson-tool-text">Trình chiếu</span>
        </button>
      )}
      <button
        type="button"
        className={`lesson-tool ${fullscreen ? "is-on" : ""}`}
        onClick={toggleFullscreen}
        aria-pressed={fullscreen}
        title="Toàn màn hình"
      >
        <Maximize2 size={14} aria-hidden />
        <span className="lesson-tool-text">Toàn màn hình</span>
      </button>
    </>
  );

  /** Thẻ tiến độ khoá + ô tìm bài — dùng chung cho cột trái (máy tính) và ngăn kéo. */
  /** Nút "Tiếp tục học" của thẻ tiến độ khoá — dùng chung cột trái (máy tính) và ngăn kéo. */
  function renderContinueLink() {
    if (!nextInCourse) return null;
    return (
      <Link href={siblingHref(nextInCourse)} className="lesson-continue-btn">
        Tiếp tục học <ArrowRight size={14} aria-hidden />
      </Link>
    );
  }

  function renderCourseInfo() {
    return (
      <>
        {/* Thẻ tiến độ khoá: vòng tròn %, số bài đã học, nút Tiếp tục học. */}
        {courseLessons.length > 0 && (
          <div className="lesson-progress-summary">
            <ProgressRing percent={courseLessons.length ? (courseDone / courseLessons.length) * 100 : 0} />
            <div>
              <p>
                {courseDone}/{courseLessons.length} bài
              </p>
              <small>
                Em đã học {courseDone}/{courseLessons.length} bài
                {session && !!items ? ` · ${doneTabs}/${totalTabs} phần đã xong` : ""}
              </small>
              {renderContinueLink()}
            </div>
          </div>
        )}
        {/* Ô tìm bài trong khoá — lọc ngay trên siblingLessons đã tải sẵn, không gọi mạng. */}
        {courseLessons.length > 0 && (
          <label className="lesson-nav-search">
            <Search size={15} aria-hidden />
            <input
              type="search"
              value={treeQuery}
              onChange={(e) => setTreeQuery(e.target.value)}
              placeholder="Tìm bài trong khoá"
              aria-label="Tìm bài trong khoá"
            />
          </label>
        )}
      </>
    );
  }

  /** Hộp dụng cụ cột phải — dùng chung cho cột phải (máy tính) và ngăn kéo (điện thoại). */
  function renderSidePanels() {
    return (
      <>
        {/* Mục lục bài này — scroll-spy trên các h2/h3 của tab đang mở, 0 request. */}
        <div className="lesson-panel lesson-toc">
          <p className="lesson-panel-title">Mục lục bài này</p>
          {tocEntries.length === 0 ? (
            <p className="lesson-panel-empty">Mục này chưa có đề mục nhỏ.</p>
          ) : (
            <>
              {tocEntries.length > 6 && (
                <label className="lesson-nav-search lesson-toc-search">
                  <Search size={14} aria-hidden />
                  <input
                    type="search"
                    value={tocQuery}
                    onChange={(e) => setTocQuery(e.target.value)}
                    placeholder="Tìm trong mục lục"
                    aria-label="Tìm trong mục lục"
                  />
                </label>
              )}
              <ol>
                {shownToc.map((entry, index) => {
                  // Nhãn mục (vd "Lý thuyết trọng tâm") chỉ hiện ở dòng ĐẦU của nhóm: một mục có
                  // nhiều đề mục con mà lặp nhãn ở mọi dòng thì rất rối. Lọc theo ô tìm kiếm vẫn
                  // hiện nhãn cho dòng khớp đầu tiên của mục đó (so với dòng liền trước trong danh
                  // sách đang hiện, không phải trong danh sách gốc).
                  const showItemLabel =
                    !!entry.heading &&
                    entry.heading !== entry.itemTitle &&
                    shownToc[index - 1]?.itemTitle !== entry.itemTitle;
                  return (
                    <li key={entry.id}>
                      <a
                        href={`#${entry.id}`}
                        className={activeHeading === entry.id ? "is-active" : ""}
                        onClick={(e) => {
                          e.preventDefault();
                          flashTheorySection(entry.id, 2);
                        }}
                      >
                        {showItemLabel && <small className="lesson-toc-item">{entry.itemTitle}</small>}
                        <span>{entry.heading || entry.itemTitle}</span>
                      </a>
                    </li>
                  );
                })}
              </ol>
              {shownToc.length === 0 && <p className="lesson-panel-empty">Không thấy đề mục nào khớp.</p>}
            </>
          )}
        </div>

        {/* Mức độ nắm vững — chuyển từ cuối bài sang đây, giữ nguyên props và nút "Luyện thêm". */}
        {items && items.length > 0 && (
          <LessonMasteryCard lessonId={id} examIds={lessonExamIds} loggedIn={!!session} />
        )}

        {/* Câu sai liên quan: chỉ dùng reviewContexts đã mang theo từ trang làm đề — 0 request.
            Không có câu sai thì KHÔNG dựng thẻ (N3: trạng thái rỗng là nhiễu) — chỉ còn một dòng liên kết. */}
        {reviewContexts && reviewContexts.length > 0 ? (
          <div className="lesson-panel lesson-controls">
            <p className="lesson-panel-title">Câu sai liên quan</p>
            <p className="lesson-panel-note">
              {reviewContexts.length === 1
                ? `Câu ${reviewContexts[0].questionIndex} em vừa làm sai thuộc bài này.`
                : `${reviewContexts.length} câu em vừa làm sai thuộc bài này.`}
            </p>
            <ul>
              {reviewContexts.map((ctx, i) => (
                <li key={i}>
                  <button
                    type="button"
                    onClick={() => {
                      selectTab("ly_thuyet");
                      window.setTimeout(() => flashTheorySection(`theory-sec-${ctx.itemId}-${ctx.sectionIndex}`), 80);
                    }}
                  >
                    Câu {ctx.questionIndex} — xem đoạn lý thuyết
                  </button>
                </li>
              ))}
            </ul>
            <Link href="/lop-hoc" className="lesson-panel-link">
              Xem sổ câu sai đầy đủ ›
            </Link>
          </div>
        ) : (
          <Link href="/lop-hoc" className="lesson-side-link">
            Sổ câu sai ›
          </Link>
        )}

        {/* Ghi chú của em — chỉ lưu trên máy, không gửi lên máy chủ. Thu thành một nút nhỏ; tự mở
            khi đã có ghi chú để em không quên mình từng viết. */}
        <details
          className="lesson-panel lesson-note-panel"
          open={noteOpen}
          onToggle={(e) => setNoteOpen(e.currentTarget.open)}
        >
          <summary>Ghi chú của em</summary>
          <textarea
            className="lesson-note"
            value={note}
            onChange={(e) => setNote(e.target.value)}
            placeholder="Chỗ này em chưa hiểu…"
            aria-label="Ghi chú của em cho bài này"
          />
          <p className="lesson-panel-note">Chỉ lưu trên máy em.</p>
        </details>
      </>
    );
  }

  const reviewBanner = reviewContexts && reviewContexts.length > 0 && (
    <div ref={reviewBannerRef} className={`lesson-review-banner ${reviewBannerOpen ? "is-open" : ""}`} role="note">
      <div className="lesson-review-banner-head">
        <button
          type="button"
          className="lesson-review-banner-toggle"
          onClick={() => setReviewBannerOpen((o) => !o)}
          aria-expanded={reviewBannerOpen}
        >
          <span>
            {reviewContexts.length === 1
              ? `Câu ${reviewContexts[0].questionIndex} em làm sai`
              : `${reviewContexts.length} câu em làm sai`}{" "}
            — {reviewBannerOpen ? "bấm để thu gọn" : "bấm vào đây để xem danh sách"}
          </span>
          <ChevronDown size={15} className={reviewBannerOpen ? "rotate-180" : ""} />
        </button>
        <button type="button" onClick={() => setReviewContexts(null)} aria-label="Đóng">
          <X size={15} />
        </button>
      </div>
      {reviewBannerOpen && (
        <div className="lesson-review-banner-list">
          {reviewContexts.map((ctx, i) => (
            <div key={i} className="lesson-review-banner-item">
              <div className="lesson-review-banner-item-head">
                <span>Câu {ctx.questionIndex}</span>
                <button
                  type="button"
                  onClick={() => {
                    setReviewBannerOpen(false);
                    selectTab("ly_thuyet");
                    window.setTimeout(() => flashTheorySection(`theory-sec-${ctx.itemId}-${ctx.sectionIndex}`), 80);
                  }}
                >
                  ↑ Xem đoạn này
                </button>
              </div>
              <p className="lesson-review-banner-q">
                <ContentHtml html={ctx.questionHtml} />
              </p>
              {ctx.correctHtml && (
                <p className="lesson-review-banner-answer is-correct">
                  <span>Đáp án đúng: </span>
                  <ContentHtml html={ctx.correctHtml} />
                </p>
              )}
              {ctx.pickedHtml && (
                <p className="lesson-review-banner-answer is-wrong">
                  <span>Em đã chọn: </span>
                  <ContentHtml html={ctx.pickedHtml} />
                </p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );

  // Tiến độ cả khoá (chỉ tính được bài đang mở vì dữ liệu từng bài tải riêng) + bài "Tiếp tục học".
  const courseDone = courseLessons.filter(lessonComplete).length;
  let nextInCourse: Lesson | null = null;
  for (const lesson of courseLessons) {
    if (lesson.id !== id && !lessonComplete(lesson)) {
      nextInCourse = lesson;
      break;
    }
  }
  if (!nextInCourse) nextInCourse = nextLesson;

  return (
    <div className={`lesson-shell lesson-page ${dim ? "is-dim" : ""} ${drawerOpen ? "is-drawer-open" : ""}`}>
      <div className="lesson-layout">
        {/* Cột trái trong bài chỉ cần: bài trước · bài sau (link về chương đã có ở breadcrumb) (N4: không lặp mục lục cả lớp —
            cây chương đầy đủ nằm trong ngăn kéo "Mục lục" và ở trang lớp). */}
        <aside className="lesson-nav lesson-nav--compact" aria-label="Điều hướng bài học">
          {prevLesson && (
            <Link href={siblingHref(prevLesson)} className="lesson-nav-step">
              <small>‹ Bài trước</small>
              <span>{prevLesson.title}</span>
            </Link>
          )}
          {nextLesson && (
            <Link href={siblingHref(nextLesson)} className="lesson-nav-step lesson-nav-step--next">
              <small>Bài sau ›</small>
              <span>{nextLesson.title}</span>
            </Link>
          )}
        </aside>

        <div className="lesson-main" ref={mainRef}>
          <header className="lesson-head">
            <button type="button" className="lesson-head-back" onClick={() => window.history.back()} aria-label="Quay lại">
              <ArrowLeft size={16} aria-hidden />
            </button>
            <div className="lesson-head-text">
              <nav className="lesson-breadcrumb" aria-label="Đường dẫn">
                <span className="lesson-crumb-class">
                  {classSlug ? <Link href="/lop-hoc">Lớp học</Link> : <span>Lớp học</span>}
                  <span aria-hidden className="lesson-crumb-sep">›</span>
                </span>
                <Link href={classHref} className="lesson-crumb-chapter">
                  {chapterFullLabel || "Chương"}
                </Link>
              </nav>
              <h1>{title}</h1>
              {hasLessonMeta && (
                <div className="lesson-meta">
                  {lessonKind !== "bai_hoc" && <span className="lesson-meta-chip">{lessonTypeLabel}</span>}
                  {assignmentItem?.due_at && <span>BTVN hạn {formatDue(assignmentItem.due_at)}</span>}
                  {lessonTheoryPassed && (
                    <span className="lesson-meta-ok">
                      <Check size={13} aria-hidden /> Đã xem lý thuyết
                    </span>
                  )}
                </div>
              )}
            </div>
            {readToolButton}
            <button
              type="button"
              className="lesson-drawer-toggle"
              onClick={() => setDrawerOpen(true)}
              aria-expanded={drawerOpen}
              aria-controls="lesson-drawer"
              aria-label="Mở mục lục khoá học"
            >
              <Menu size={17} aria-hidden />
            </button>
            <div className={`lesson-tools ${toolsOpen ? "is-open" : ""}`}>{readTools}</div>
          </header>

          {/* Header + thanh tiến độ + 6 tab nằm chung một khối: cả khối dính dưới navbar, mà
              header vẫn chỉ cao bằng nội dung (không phình ra che bài). */}
          <div className="lesson-content">
            <div className="lesson-progressbar" aria-label={`Đã học ${progressDone} trên ${totalTabs} mục`}>
              <span style={{ width: `${totalTabs ? Math.round((progressDone / totalTabs) * 100) : 0}%` }} />
              <small>
                Đã học {progressDone}/{totalTabs} mục
              </small>
            </div>

            {tabNav}

            <div className="lesson-body" ref={bodyRef}>
            {reviewBanner}

            {visibleSections.length === 0 && <p className="lesson-muted">Học liệu đang được giảng viên cập nhật.</p>}

            {!bodyReady && <p className="lesson-body-loading">Đang mở nội dung…</p>}

            {bodyReady && activeSection && (
              <section
                key={activeSection.kind}
                id={`secondary-stage-${activeSection.kind}`}
                data-kind={activeSection.kind}
                className="lesson-section"
                role="tabpanel"
                aria-labelledby={`lesson-tab-${activeSection.kind}`}
              >
                <div className="lesson-stack">{renderSectionItems(activeSection)}</div>
                <div className="lesson-tabfoot">
                  {nextSection ? (
                    <button type="button" className="lesson-next" onClick={() => selectTabAndScroll(nextSection.kind)}>
                      Mục tiếp theo: {TAB_LABEL[nextSection.kind]} <ArrowRight size={15} aria-hidden />
                    </button>
                  ) : (
                    <span className="lesson-tabfoot-end">
                      <Check size={15} aria-hidden /> Đây là mục cuối của bài
                    </span>
                  )}
                </div>
              </section>
            )}

            </div>
          </div>
        </div>

        <aside className="lesson-side" aria-label="Dụng cụ học bài">
          {renderSidePanels()}
        </aside>
      </div>

      <nav className="lesson-bottombar lesson-bottombar--mobile lesson-bottombar--home" aria-label="Điều hướng bài học">
        <LessonHomeLink />
        <button
          type="button"
          className="lesson-bottom-link"
          onClick={() => setDrawerOpen(true)}
          aria-expanded={drawerOpen}
          aria-controls="lesson-drawer"
        >
          <Menu size={16} aria-hidden />
          <span>Mục lục</span>
        </button>
        <button
          type="button"
          className={`lesson-bottom-done ${lessonMarked ? "is-done" : ""}`}
          onClick={markLessonDone}
          disabled={lessonMarked}
          aria-pressed={lessonMarked}
          aria-label={lessonMarked ? "Đã đánh dấu: học xong bài này" : "Đánh dấu đã học xong bài này"}
        >
          {lessonMarked ? <Check size={16} aria-hidden /> : <span className="lesson-checkbox" aria-hidden />}
          <span>Đã học xong</span>
        </button>

        <span className="lesson-bottom-step" aria-live="polite">
          {stepLabel}
        </span>

        {nextLesson ? (
          <Link href={siblingHref(nextLesson)} className="lesson-bottom-link lesson-bottom-link--next" title={nextLesson.title}>
            <span>Bài sau ›</span>
            <ArrowRight size={16} aria-hidden />
          </Link>
        ) : (
          <span className="lesson-bottom-link lesson-bottom-link--next is-empty" aria-hidden>
            <span>Bài sau</span>
            <ArrowRight size={16} />
          </span>
        )}
      </nav>

      {/* Ngăn kéo "Nội dung khoá" (chỉ hiện dưới 640px): gộp cột trái + cột phải vào một
          bottom sheet, trượt từ đáy, đóng bằng ✕ / vuốt xuống / Esc. Chỉ render khi đang mở
          nên nội dung bên trong không tốn gì lúc tải trang. */}
      {drawerOpen && (
        <div className="lesson-drawer" role="dialog" aria-modal="true" aria-label={`Nội dung khoá ${chapterFullLabel}`}>
          <button type="button" className="lesson-drawer-scrim" aria-label="Đóng mục lục" onClick={() => setDrawerOpen(false)} />
          <div
            id="lesson-drawer"
            className="lesson-drawer-sheet"
            ref={drawerRef}
            onTouchStart={onDrawerTouchStart}
            onTouchMove={onDrawerTouchMove}
            onTouchEnd={onDrawerTouchEnd}
          >
            <div className="lesson-drawer-head">
              <div>
                <p className="lesson-drawer-title">Nội dung khoá {chapterFullLabel || ""}</p>
                <small>
                  Đã học {progressDone}/{totalTabs} mục
                </small>
              </div>
              <button type="button" onClick={() => setDrawerOpen(false)} aria-label="Đóng mục lục">
                <X size={17} aria-hidden />
              </button>
            </div>
            <div className="lesson-drawer-body">
              {renderCourseInfo()}
              <ChapterTree
                entries={courseChapters}
                mode="learn"
                currentLessonId={id}
                openChapterIds={openChapterIds}
                onToggleChapter={toggleChapter}
                lessonHref={siblingHref}
                isLessonDone={lessonComplete}
                showProgress={!!session}
                filterLessonIds={matchingLessonIds}
              />
              {renderSidePanels()}
            </div>
          </div>
        </div>
      )}

      {/* Chế độ trình chiếu bài giảng — lớp phủ toàn màn hình, tải chậm, chỉ mount khi bấm nút
          (hoặc mở link có #chieu). Dựng từ theoryItems đã tải sẵn nên không thêm request nào. */}
      {presenting && (
        <LessonPresenter
          lessonTitle={title}
          chapterLabel={chapterFullLabel}
          items={theoryItems}
          onClose={() => setPresenting(false)}
        />
      )}
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
      <Footer variant="app" />
    </>
  );
}
