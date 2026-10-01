"use client";

import { Suspense, useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { ArrowLeft, ArrowRight, Check, ChevronDown, Eye, FileText, Maximize2, Play, Search, X } from "lucide-react";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import ContentHtml from "@/components/exams/ContentHtml";
import { useAuth } from "@/components/auth/AuthProvider";
import WorkedQuestionsGrid from "@/components/lessons/WorkedQuestionsGrid";
import SampleQuestionsGrid from "@/components/lessons/SampleQuestionsGridLazy";
import PracticeSession from "@/components/lessons/PracticeSession";
import LessonMasteryCard from "@/components/mastery/LessonMasteryCard";
import type { SchoolClass } from "@/features/exams/types";
import {
  consumeTheoryReviewContext,
  theorySectionItemId,
  wrapTheorySections,
  type TheoryReviewContext,
} from "@/features/lessons/theory-sections";
import {
  LESSON_KIND_META,
  SECTION_ORDER,
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
  bai_tap_mau: "Bài tập mẫu",
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

/** Ý chính/công thức cần thuộc của 1 mục lý thuyết — hiện luôn (không thu gọn thêm lần
 *  nữa), độc lập với việc mục lý thuyết đầy đủ bên dưới đang mở hay đóng, để học sinh
 *  xem nhanh mà không cần mở hết bài dài. Rỗng (chưa backfill) thì không hiện gì. */
function TheorySummary({ html }: { html: string }) {
  if (!html.trim()) return null;
  return (
    <div className="lesson-summary">
      <p className="lesson-summary-label">📌 Tóm tắt ý chính cần thuộc</p>
      <ContentHtml html={html} className="block leading-relaxed" />
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
  // Gắn id theo từng khối <h3> để quiz "Kiểm tra nhanh" cuộn + tô màu đúng đoạn khi trả lời
  // sai (xem "Ôn ngay" trong ExamRunner) — chỉ tính lại khi nội dung mục thật sự đổi.
  const sectionedHtml = useMemo(() => wrapTheorySections(item.body_html, item.id).html, [item.body_html, item.id]);

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
      <TheorySummary html={item.summary_html} />
      {open && hasBody && (
        <div className={hideTitle ? "lesson-prose lesson-prose--plain" : "lesson-prose"}>
          <ContentHtml html={sectionedHtml} className="block leading-relaxed" />
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
  // "Đánh dấu đã học xong bài này" ở thanh đáy: không có API lưu cấp-bài (chỉ có API cấp-mục),
  // nên ghi trên máy — nút vẫn phản hồi ngay, tiến độ "x/y mục" cộng thêm 1 khi đã đánh dấu.
  const [lessonMarked, setLessonMarked] = useState(false);
  // Cây chương ở cột trái: chỉ chương đang học mở sẵn, chương khác gấp lại (khoá có thể dài
  // hơn 100 bài nên không xổ hết), và một ô tìm bài lọc ngay trên siblingLessons — không gọi mạng.
  const [treeQuery, setTreeQuery] = useState("");
  const [openChapters, setOpenChapters] = useState<Set<number>>(new Set());
  const reviewBannerRef = useRef<HTMLDivElement>(null);
  const bodyRef = useRef<HTMLDivElement>(null);
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
    fetchLessonWithItemsStatic(id, apply).then(apply);
    return () => {
      stale = true;
    };
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
      const savedFont = Number(window.localStorage.getItem(FONT_STORE));
      if (Number.isInteger(savedFont) && savedFont >= 0 && savedFont < FONT_SCALES.length && savedFont !== fontLevel) {
        setFontLevel(savedFont);
      }
      const savedDim = window.localStorage.getItem(DIM_STORE) === "1";
      if (savedDim !== dim) setDim(savedDim);
      const savedDone = window.localStorage.getItem(`${LESSON_DONE_STORE}${id}`) === "1";
      if (savedDone !== lessonMarked) setLessonMarked(savedDone);
    } catch {}
    // Chỉ khôi phục 1 lần khi mở bài (theo id) — thêm dim/fontLevel/lessonMarked vào deps sẽ
    // làm effect chạy lại sau mỗi lần đổi cỡ chữ và ghi đè lựa chọn vừa bấm.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);
  /* eslint-enable react-hooks/set-state-in-effect */

  // Đổi cỡ chữ thì đổi luôn cỡ chữ gốc của khối nội dung (--lesson-read-size), không nhân
  // từng phần tử — công thức KaTeX cũng to lên theo.
  useEffect(() => {
    bodyRef.current?.style.setProperty("--lesson-read-size", `${FONT_SCALES[fontLevel]}rem`);
  }, [fontLevel, items, activeTab]);

  // Chỉ ghi lại sau khi đã khôi phục xong — nếu không, lần render đầu (mức mặc định) sẽ ghi đè
  // lựa chọn đã lưu của học sinh trước khi effect khôi phục kịp chạy.
  const settingsLoadedRef = useRef(false);
  useEffect(() => {
    if (!settingsLoadedRef.current) {
      settingsLoadedRef.current = true;
      return;
    }
    try {
      window.localStorage.setItem(FONT_STORE, String(fontLevel));
    } catch {}
  }, [fontLevel]);

  useEffect(() => {
    if (!settingsLoadedRef.current) return;
    try {
      if (dim) window.localStorage.setItem(DIM_STORE, "1");
      else window.localStorage.removeItem(DIM_STORE);
    } catch {}
  }, [dim]);

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

  function isChapterOpen(chapterIdInTree: number, lessons: Lesson[]) {
    if (openChapters.has(chapterIdInTree)) return true;
    if (matchingLessonIds) return lessons.some((l) => matchingLessonIds.has(l.id));
    return chapterIdInTree === chapterId;
  }

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

  if (!id) return <p className="lesson-notice">Thiếu mã bài học trong địa chỉ.</p>;
  if (error) return <p className="lesson-notice text-red-400">{error}</p>;
  if (!items) return <LessonSkeleton />;

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
      <div className="lesson-shell lesson-page">
        <div className="lesson-layout">
          <div className="lesson-main lesson-main--single">
            {backLink}
            <nav className="lesson-breadcrumb" aria-label="Đường dẫn">
              <Link href="/lop-hoc">Lớp học</Link>
              <span aria-hidden>›</span>
              <Link href={classHref}>{chapterTitle || "Chương"}</Link>
              <span aria-hidden>›</span>
              <span className="lesson-breadcrumb-current">{title}</span>
            </nav>
            <header className="lesson-head lesson-head--single">
              <div className="lesson-head-text">
                <h1>{title}</h1>
                <div className="lesson-meta">
                  <span className="lesson-meta-chip">{kindMeta.label}</span>
                  <span>{examIds.length} đề</span>
                </div>
              </div>
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

        <nav className="lesson-bottombar" aria-label="Điều hướng bài học">
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
      </div>
    );
  }

  const visibleSections = sections.filter((s) => s.items.length > 0);
  const activeSection = visibleSections.find((s) => s.kind === activeTab) ?? visibleSections[0];
  const activeIndex = activeSection ? visibleSections.findIndex((s) => s.kind === activeSection.kind) : -1;
  const nextSection = activeIndex >= 0 ? visibleSections[activeIndex + 1] : undefined;
  const totalTabs = visibleSections.length;
  const doneTabs = visibleSections.filter((s) => !!session && s.items.every(isDone)).length;
  const progressDone = Math.min(totalTabs, doneTabs + (lessonMarked ? 1 : 0));

  const assignmentItem = items.find((i) => i.kind === "bai_tap_ve_nha" && i.due_at);
  const itemCount = items.length;
  const lessonTypeLabel = LESSON_KIND_META[lessonKind]?.label ?? "Bài học";
  const stepLabel = lessonMarked ? "Đã học xong" : `Mục ${Math.max(activeIndex, 0) + 1}/${totalTabs || 1}`;

  // Mục lục bài này = các h2/h3 có id trong TAB đang mở (heading do nội dung soạn sẵn sinh ra).
  // Cột phải dùng; ở bước này chỉ cần activeHeading được cập nhật.

  function selectTabAndScroll(kind: LessonItemKind) {
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
          <div key={item.id} className="lesson-stack" data-item={item.id}>
            <TheoryBlock
              item={item}
              defaultOpen={itemIndex === 0 || item.id === hashTargetItemId}
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
          <div key={item.id} className="lesson-block" data-item={item.id}>
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
      return (
        <div key={item.id} className="lesson-block" data-item={item.id}>
          {(!plain || item.subtitle) && (
            <div className="lesson-block-head">
              {!plain && <p className="lesson-block-title">{item.title}</p>}
              {item.subtitle && <p className="lesson-block-sub">{item.subtitle}</p>}
            </div>
          )}
          {item.kind === "bai_tap_mau" ? (
            <>
              {item.exam_ids.length > 0 && <SampleQuestionsGrid examIds={item.exam_ids} color={ACCENT} />}
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
    });
  }

  /** 6 tab ngang: badge số mục, dấu ✓ khi xong, tab đang mở gạch chân màu nhấn. */
  const tabNav = (extraClass: string) => (
    <nav className={`lesson-tabs ${extraClass}`} aria-label="Các mục của bài học">
      <ol role="tablist">
        {visibleSections.map((section) => {
          const complete = !!session && section.items.every(isDone);
          return (
            <li key={section.kind}>
              <button
                type="button"
                role="tab"
                id={`lesson-tab-${section.kind}`}
                className={`${section.kind === activeTab ? "is-active" : ""} ${complete ? "is-complete" : ""}`}
                aria-selected={section.kind === activeTab}
                aria-controls={`secondary-stage-${section.kind}`}
                onClick={() => selectTabAndScroll(section.kind)}
              >
                {complete && <Check size={13} aria-hidden />}
                <span>{TAB_LABEL[section.kind]}</span>
                <i>{section.items.length}</i>
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

  // Tiến độ cả khoá (chỉ tính được bài đang mở vì dữ liệu từng bài tải riêng) + bài "Học tiếp".
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
    <div className={`lesson-shell lesson-page ${dim ? "is-dim" : ""}`}>
      <div className="lesson-layout">
        <aside className="lesson-nav" aria-label="Nội dung khoá học">
          {/* Thẻ tiến độ khoá: vòng tròn %, số bài đã học, nút Học tiếp. */}
          {courseLessons.length > 0 && (
            <div className="lesson-progress-summary">
              <ProgressRing percent={courseLessons.length ? (courseDone / courseLessons.length) * 100 : 0} />
              <div>
                <p>
                  {courseDone}/{courseLessons.length} bài
                </p>
                <small>
                  Em đã học {courseDone}/{courseLessons.length} bài
                  {session && items.length > 0 ? ` · ${doneTabs}/${totalTabs} phần đã xong` : ""}
                </small>
                {nextInCourse && (
                  <Link href={siblingHref(nextInCourse)} className="lesson-btn lesson-continue-btn">
                    Học tiếp <ArrowRight size={14} aria-hidden />
                  </Link>
                )}
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

          {/* Cây chương: số · tên · đã xong/tổng; chỉ chương đang học mở sẵn. */}
          <div className="lesson-tree">
            {courseChapters.map(({ chapter, lessons }, chapterIndex) => {
              const shown = matchingLessonIds ? lessons.filter((l) => matchingLessonIds.has(l.id)) : lessons;
              if (shown.length === 0) return null;
              const open = isChapterOpen(chapter.id, lessons);
              const doneInChapter = lessons.filter(lessonComplete).length;
              return (
                <div key={chapter.id}>
                  <button
                    type="button"
                    className="lesson-tree-chapter"
                    onClick={() => toggleChapter(chapter.id)}
                    aria-expanded={open}
                  >
                    <em>{chapterIndex + 1}</em>
                    <span>{chapter.title}</span>
                    <small>
                      {doneInChapter}/{lessons.length}
                    </small>
                    <ChevronDown size={15} className={open ? "is-open" : ""} aria-hidden />
                  </button>
                  {open && (
                    <ol>
                      {shown.map((lesson) => {
                        const current = lesson.id === id;
                        const done = lessonComplete(lesson);
                        return (
                          <li key={lesson.id}>
                            {current ? (
                              <span className="lesson-tree-current is-current" aria-current="page">
                                <i aria-hidden>{done ? <Check size={11} /> : "●"}</i>
                                <span>{lesson.title}</span>
                              </span>
                            ) : (
                              <Link href={siblingHref(lesson)} className={done ? "is-done" : ""}>
                                <i aria-hidden>{done ? <Check size={11} /> : "○"}</i>
                                <span>{lesson.title}</span>
                              </Link>
                            )}
                          </li>
                        );
                      })}
                    </ol>
                  )}
                </div>
              );
            })}
            {matchingLessonIds?.size === 0 && <p className="lesson-panel-empty">Không thấy bài nào khớp.</p>}
          </div>

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
                  {chapterTitle || "Chương"}
                </Link>
                <span aria-hidden className="lesson-crumb-sep">›</span>
                <span className="lesson-breadcrumb-current">{title}</span>
              </nav>
              <h1>{title}</h1>
              <div className="lesson-meta">
                <span className="lesson-meta-chip">{lessonTypeLabel}</span>
                <span>
                  {itemCount} mục{totalTabs > 0 ? ` · ${totalTabs} phần` : ""}
                </span>
                {assignmentItem?.due_at && <span>BTVN hạn {formatDue(assignmentItem.due_at)}</span>}
                {session && progress.get(assignmentItem?.id ?? -1)?.theory?.status === "passed" && (
                  <span className="lesson-meta-ok">
                    <Check size={13} aria-hidden /> Đã xem lý thuyết
                  </span>
                )}
              </div>
            </div>
            {readToolButton}
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

            {tabNav("lesson-tabs--mobile")}
            {tabNav("lesson-tabs--desktop")}

            <div className="lesson-body" ref={bodyRef}>
            {reviewBanner}

            {visibleSections.length === 0 && <p className="lesson-muted">Học liệu đang được giảng viên cập nhật.</p>}

            {activeSection && (
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

            {items && items.length > 0 && (
              <LessonMasteryCard lessonId={id} examIds={lessonExamIds} loggedIn={!!session} />
            )}
            </div>
          </div>
        </div>

        <aside className="lesson-side" aria-label="Dụng cụ học bài" />
      </div>

      <nav className="lesson-bottombar" aria-label="Điều hướng bài học">
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

        <button
          type="button"
          className={`lesson-bottom-done ${lessonMarked ? "is-done" : ""}`}
          onClick={markLessonDone}
          disabled={lessonMarked}
          aria-pressed={lessonMarked}
        >
          {lessonMarked ? <Check size={16} aria-hidden /> : <span className="lesson-checkbox" aria-hidden />}
          <span>{lessonMarked ? "Đã học xong bài này" : "Đánh dấu đã học xong"}</span>
        </button>

        <span className="lesson-bottom-step" aria-live="polite">
          {stepLabel}
        </span>

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
