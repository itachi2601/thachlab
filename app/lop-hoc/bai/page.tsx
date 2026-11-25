"use client";

import {
  Suspense,
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
  type KeyboardEvent as ReactKeyboardEvent,
  type TouchEvent,
} from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { ArrowLeft, ArrowRight, Check, ChevronDown, Eye, Maximize2, Menu, MonitorPlay, Tv, Search, X } from "lucide-react";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import ContentHtml from "@/components/exams/ContentHtml";
import { useAuth } from "@/components/auth/AuthProvider";
import TeacherViewBanner from "@/components/auth/TeacherViewBanner";
import { useTeacherView } from "@/components/auth/useTeacherView";
import AroundReadMore from "@/components/lessons/AroundReadMore";
import LessonPresenter from "@/components/lessons/LessonPresenterLazy";
import BtmPresenter from "@/components/lessons/btm-trinh-chieu/BtmPresenterLazy";
import { banChieuCuaBai, linkBanChieu } from "@/features/lessons/tren-lop";
import LessonNoteFab, { type LessonNoteContext } from "@/components/lessons/LessonNoteFab";
import StudentNoteFab, { OPEN_STUDENT_NOTE_EVENT } from "@/components/lessons/StudentNoteFab";
import RandomCallFab, { type CallClass } from "@/components/lessons/RandomCallFab";
import NenKhtn9 from "@/components/lop-hoc/NenKhtn9";
import { HSG_SUBJECT_CODE } from "@/services/academic-subjects";
import ChapterTree from "@/components/lessons/ChapterTree";
import LessonMasteryCard from "@/components/mastery/LessonMasteryCard";
import type { SchoolClass } from "@/features/exams/types";
import {
  consumeTheoryReviewContext,
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
  isGradedKind,
  isItemLive,
  isPeriodicExam,
  isSemesterExam,
  type Chapter,
  type Lesson,
  type LessonItem,
  type LessonItemKind,
  type LessonKind,
} from "@/features/lessons/types";
import { markItemDone, type LessonExamMeta } from "@/services/lessons";
import { fetchLessonPageStudent } from "@/services/lesson-page";
import type { LessonMasteryInitial } from "@/components/mastery/LessonMasteryCard";
import { clearResumeSpot, writeResumeSpot } from "@/features/lessons/resume-spot";
import {
  fetchChaptersStatic,
  fetchClassesStatic,
  fetchLessonWithItemsStatic,
  fetchLessonsStatic,
  retryLessonRevalidate,
  type LessonBundle,
} from "@/services/static-content";
import type { ItemProgress } from "@/services/progress";
import { expandClassIdsByGrade, isCttcClassSlug } from "@/services/classes";
import { visibleTo } from "@/services/content";
import { supabaseConfigured } from "@/services/supabase";
import { SGK_L12 } from "@/lib/sgk-l12";

import {
  TAB_LABEL,
  TAB_SLUG,
  FONT_SCALES,
  FONT_STORE,
  DIM_STORE,
  LESSON_DONE_STORE,
  TOC_READ_STORE,
  clearPendingDang,
  parseDangHash,
  parseTabHash,
  requestOpenDang,
  currentHash,
  scrollToPart,
  writeTabHash,
  flashTheorySection,
  highlightTheorySectionOnly,
} from "./_parts/lesson-nav";
import { ProgressRing, formatDue, LessonLoginWall, LessonSkeleton, LessonHomeLink } from "./_parts/LessonBits";
import { VideoBlock } from "./_parts/VideoBlock";
import { TheoryBlock, TheoryQuizBlock } from "./_parts/TheoryBlock";
import OnNamPhutGon from "@/components/lessons/OnNamPhutGon";
import { ExamRow } from "./_parts/ExamRow";
import { GradedItemBlock } from "./_parts/GradedItemBlock";
import { WorkedPracticeBlock } from "./_parts/WorkedPracticeBlock";

function LessonLoader() {
  const { session, loading } = useAuth();
  const { isTeacherView } = useTeacherView();
  // B1/N1: Trình chiếu và ghi chú lúc dạy chỉ ở chế độ giáo viên.
  // "Xem như học sinh" tắt isTeacherView nên hiện đúng giao diện học sinh.
  const canPresent = isTeacherView;
  // Chờ hồ sơ: lúc loading, isTeacherView còn false — đừng ghi tiến độ trong khoảng đó.
  const recordProgress = !loading && !!session && !isTeacherView;
  const searchParams = useSearchParams();
  const id = Number(searchParams.get("id"));
  const classSlug = searchParams.get("class");
  const subjectCode = searchParams.get("subject") ?? "vat-ly";

  const [title, setTitle] = useState("");
  const [chapterTitle, setChapterTitle] = useState("");
  // Trang xuất tĩnh nên <title> mặc định là tên site — đặt tên bài để tab/lịch sử trình duyệt phân biệt được.
  useEffect(() => {
    if (title) document.title = `${title} | ThachLab`;
  }, [title]);
  const [chapterId, setChapterId] = useState<number | null>(null);
  const [lessonKind, setLessonKind] = useState<LessonKind>("bai_hoc");
  const [items, setItems] = useState<LessonItem[] | null>(null);
  /** Lời giải bài tập mẫu không nằm trong file tĩnh — theo dõi lượt tải thêm để không hiện lưới trống. */
  const [workedFailedId, setWorkedFailedId] = useState<number | null>(null);
  const workedState: "loading" | "failed" = workedFailedId === id ? "failed" : "loading";
  const [examMetas, setExamMetas] = useState<Map<number, LessonExamMeta>>(new Map());
  const [examMetaStatus, setExamMetaStatus] = useState<"loading" | "error" | "ready">("loading");
  const [masteryInitial, setMasteryInitial] = useState<LessonMasteryInitial>("pending");
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
  // Trình chiếu bài tập mẫu (17/11/2026): mục đang chiếu + dạng bắt đầu; chỉ giáo viên, tải chậm.
  const [chieuBtm, setChieuBtm] = useState<{ itemId: number; start: number } | null>(null);
  // "#chieu" trên URL → mở thẳng chế độ trình chiếu (thầy lưu sẵn link cho tiết dạy). Đọc
  // trong effect chứ không phải giá trị khởi tạo của useState: trang này được prerender lúc
  // build (lúc đó chưa có hash), khởi tạo bằng hash sẽ lệch cây DOM khi hydrate. Đẩy sang
  // setTimeout 0 để không setState ngay trong thân effect (gây render chồng).
  useEffect(() => {
    if (currentHash().replace(/^#/, "").toLowerCase() !== "chieu") return;
    const timer = window.setTimeout(() => setPresenting(true), 0);
    return () => window.clearTimeout(timer);
  }, []);
  // "#chieu-btm-3" → mở thẳng trình chiếu dạng 3 của mục Bài tập mẫu đầu tiên (thầy lưu link cho tiết chữa bài).
  // Chờ items tải xong và đã xác định quyền giáo viên; chỉ mở một lần mỗi lần vào trang.
  const daMoBtmRef = useRef(false);
  useEffect(() => {
    if (daMoBtmRef.current || !canPresent || !items) return;
    const m = /^#chieu-btm-(\d+)$/i.exec(currentHash());
    if (!m) return;
    daMoBtmRef.current = true;
    const it = items.find((x) => x.kind === "bai_tap_mau" && x.questions.length > 0);
    if (!it) return;
    const start = Math.min(Math.max(Number(m[1]) - 1, 0), it.questions.length - 1);
    const timer = window.setTimeout(() => setChieuBtm({ itemId: it.id, start }), 0);
    return () => window.clearTimeout(timer);
  }, [canPresent, items]);
  // Mục lý thuyết đã đăng và có nội dung — nguồn duy nhất cho bộ trang chiếu, không gọi mạng.
  const theoryItems = useMemo(
    () => (items ?? []).filter((item) => item.kind === "ly_thuyet" && item.body_html.trim() !== ""),
    [items],
  );
  // Dòng meta ngay dưới tên bài (bản duyệt 26/10/2026): "~17 phút · 6 mục · 7 câu tự kiểm tra" của mục lý thuyết
  // duy nhất — trước đây nằm trong thẻ đọc cạnh "Mở tất cả". Bài nhiều mục lý thuyết giữ số đếm trong từng thẻ.
  const headTheory = theoryItems.length === 1 ? theoryItems[0] : null;
  const theoryMeta = useMemo(() => {
    if (!headTheory) return null;
    const est = estimateTheoryTime(headTheory.body_html);
    const total = wrapTheorySections(headTheory.body_html, headTheory.id).sections.length;
    return total > 1 ? { ...est, total } : null;
  }, [headTheory]);
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

  // Dữ liệu cần đăng nhập — thông tin đề kiểm tra (RLS), điểm, tiến độ, mức thành thạo — gộp trong MỘT RPC
  // get_lesson_page_student (services/lesson-page.ts; RPC chưa chạy thì tự lùi về các truy vấn cũ). Chạy song
  // song với phần còn lại ngay khi có session (không chờ hồ sơ); chế độ giáo viên chỉ bỏ tiến độ, không áp.
  // Khoá theo mục + mã đề chứ không theo đối tượng `items`: bản đối chiếu DB (thêm lời giải bài tập mẫu) thay
  // `items` nhưng không đổi dữ liệu cần tải, không được gọi lại lần hai.
  const teacherViewRef = useRef(isTeacherView);
  useEffect(() => {
    teacherViewRef.current = isTeacherView;
  }, [isTeacherView]);
  const itemsRef = useRef(items);
  useEffect(() => {
    itemsRef.current = items;
  });
  const studentDataKey = items ? items.map((i) => `${i.id}:${i.kind}:${i.exam_ids.join(".")}`).join(",") : null;
  const studentId = session?.user.id ?? null;
  // Đổi bài trong cùng trang (?id= mới): về "đang tải" như bản cũ, không để đề/mastery của bài trước hiện tạm.
  const [studentDataFor, setStudentDataFor] = useState(id);
  if (studentDataFor !== id) {
    setStudentDataFor(id);
    setExamMetaStatus("loading");
    setMasteryInitial("pending");
  }
  useEffect(() => {
    const current = itemsRef.current;
    if (!studentId || !current || studentDataKey === null) return;
    let stale = false;
    void fetchLessonPageStudent(id, studentId, current).then((data) => {
      if (stale) return;
      setMasteryInitial(data.mastery === undefined ? "self" : data.mastery);
      if (data.examMetas) {
        setExamMetas(data.examMetas);
        setExamMetaStatus("ready");
      } else setExamMetaStatus("error");
      if (teacherViewRef.current) return;
      if (data.progress) {
        setProgress(data.progress.progress);
        setScores(data.progress.scores);
        setDone(data.progress.done);
      } else setProgress(new Map());
    });
    return () => {
      stale = true;
    };
  }, [id, studentId, studentDataKey]);

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
      // Chỉ giữ dạng chờ mở khi link thật sự đưa sang tab Bài mẫu — không để số dạng "kẹt" cho grid bài khác.
      clearPendingDang();
      const dang = parseDangHash(hash);
      if (dang && parsed.kind === "bai_tap_mau") requestOpenDang(dang);
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
    if (!recordProgress) return;
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
    if (!recordProgress || !session || done.has(item.id)) return;
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

  // Lớp có thể "Gọi tên ngẫu nhiên" trong bài này: các lớp gắn với chương đang xem (dữ liệu đã tải,
  // không thêm request); mặc định lớp theo ?class=.
  const callClasses = useMemo((): CallClass[] => {
    if (!siblingChapters || !siblingClasses || chapterId == null) return [];
    const ch = siblingChapters.find((c) => c.id === chapterId);
    if (!ch) return [];
    return siblingClasses
      .filter((c) => ch.classIds.includes(c.id))
      .sort((a, b) => a.sort_order - b.sort_order)
      .map((c) => ({ id: c.id, name: c.name }));
  }, [siblingChapters, siblingClasses, chapterId]);
  const callDefaultClassId = (classSlug && siblingClasses?.find((c) => c.slug === classSlug)?.id) || null;

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
    if (isTeacherView || !session || !items || lesson.id !== id) return false;
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

  // useMemo để các useCallback/useMemo phía dưới phụ thuộc đúng vào activeKind (React Compiler
  // mới giữ được memo thủ công — rule preserve-manual-memoization).
  const activeKind = useMemo<LessonItemKind | undefined>(
    () => (visibleSections.some((s) => s.kind === activeTab) ? activeTab : visibleSections[0]?.kind),
    [visibleSections, activeTab],
  );
  const activeSection = visibleSections.find((s) => s.kind === activeKind);
  // Ghi chú nhanh của giáo viên (nút "Ghi chú"/phím N): chụp mục đang đọc LÚC MỞ hộp, đọc từ DOM của
  // phần thân bài — đề mục h2/h3 (lý thuyết) hoặc dạng bài mẫu (.lesson-worked-row) gần dòng mắt nhất.
  const getNoteContext = useCallback((): LessonNoteContext => {
    const root = bodyRef.current;
    const tab = TAB_LABEL[activeKind ?? "ly_thuyet"];
    if (!root) return { itemId: null, pageKey: "", pageHeading: tab };
    const line = window.innerHeight * 0.4;
    const anchors = Array.from(root.querySelectorAll<HTMLElement>("[data-item], h2[id], h3[id], .lesson-worked-row"));
    let current: HTMLElement | null = null;
    for (const el of anchors) {
      if (el.getBoundingClientRect().top <= line) current = el;
      else break;
    }
    const itemEl = current?.closest<HTMLElement>("[data-item]") ?? root.querySelector<HTMLElement>("[data-item]");
    const itemId = itemEl?.dataset.item ? Number(itemEl.dataset.item) : null;
    const item = items?.find((it) => it.id === itemId);
    const parts = [tab];
    if (item?.title) parts.push(item.title);
    let pageKey = itemId != null ? `item-${itemId}` : "";
    if (current?.matches("h2[id], h3[id]")) {
      const text = current.textContent?.replace(/\s+/g, " ").trim();
      if (text && text !== item?.title) parts.push(text);
      pageKey = current.id;
    } else if (current?.matches(".lesson-worked-row")) {
      const label = current.querySelector(".lesson-worked-label")?.textContent?.trim();
      if (label) parts.push(label);
      const rows = Array.from(current.parentElement?.children ?? []);
      pageKey = `item-${itemId}-dang-${rows.indexOf(current) + 1}`;
    }
    return { itemId, pageKey, pageHeading: parts.join(" › ") };
  }, [activeKind, items]);
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

  // Tô mục đang đọc trong mục lục (B7): mục cuối cùng có đỉnh đã qua dòng mắt (~35% màn hình). Đo theo cuộn
  // thay vì IntersectionObserver vì mốc đang gập cao gần 0px; bỏ qua mốc gập (data-open="0"). Không gọi mạng.
  useEffect(() => {
    const root = bodyRef.current;
    if (!root || !bodyReady || tocEntries.length === 0) return;
    const ids = new Set(tocEntries.map((e) => e.id));
    let targets: HTMLElement[] = [];
    let raf = 0;
    const collect = () => {
      targets = Array.from(root.querySelectorAll<HTMLElement>("[id]")).filter(
        (el) => ids.has(el.id) && el.dataset.open !== "0",
      );
    };
    const compute = () => {
      raf = 0;
      const line = Math.min(window.innerHeight * 0.35, 240);
      let cur: string | null = targets[0]?.id ?? null;
      for (const el of targets) {
        if (el.getBoundingClientRect().top <= line) cur = el.id;
        else break;
      }
      setActiveHeading(cur);
    };
    const schedule = () => {
      if (!raf) raf = window.requestAnimationFrame(compute);
    };
    const mo = new MutationObserver(() => {
      collect();
      schedule();
    });
    collect();
    schedule();
    mo.observe(root, { childList: true, subtree: true, attributes: true, attributeFilter: ["data-open"] });
    window.addEventListener("scroll", schedule, { passive: true });
    window.addEventListener("resize", schedule);
    return () => {
      mo.disconnect();
      window.removeEventListener("scroll", schedule);
      window.removeEventListener("resize", schedule);
      if (raf) window.cancelAnimationFrame(raf);
    };
  }, [activeTab, items, bodyReady, tocEntries]);

  // ✓ cho mục đã đọc: mục đứng trước mục xa nhất em từng đọc tới trong tab này. Nhớ trên máy (localStorage),
  // không thêm bảng/round-trip — tiến độ chính thức vẫn là "Tôi đã đọc xong"/RP như cũ.
  const tocStoreKey = `${TOC_READ_STORE}${id}-${activeTab}`;
  const [tocRead, setTocRead] = useState<{ key: string; max: number }>({ key: "", max: 0 });
  const tocActiveIndex = tocEntries.findIndex((e) => e.id === activeHeading);
  /* eslint-disable react-hooks/set-state-in-effect -- đọc/ghi localStorage theo tab (trang prerender tĩnh, không đọc được lúc khởi tạo). */
  useEffect(() => {
    let max = 0;
    try {
      max = Number(window.localStorage.getItem(tocStoreKey)) || 0;
    } catch {}
    setTocRead({ key: tocStoreKey, max });
  }, [tocStoreKey]);
  useEffect(() => {
    if (tocRead.key !== tocStoreKey || tocActiveIndex <= tocRead.max) return;
    setTocRead({ key: tocStoreKey, max: tocActiveIndex });
    try {
      window.localStorage.setItem(tocStoreKey, String(tocActiveIndex));
    } catch {}
  }, [tocActiveIndex, tocRead, tocStoreKey]);
  /* eslint-enable react-hooks/set-state-in-effect */
  // Chỗ dừng cho trang chương ("Dừng ở mục IV. Trả bài · còn ~8 phút") — chỉ mục lý thuyết, chỉ học sinh.
  // Chỉ ghi khi tới mục xa nhất từng đọc — mở bài (scroll-spy về mục 1) không đè chỗ dừng cũ. Xong tab → xoá.
  const userId = session?.user.id;
  const theoryTabDone =
    !!session && (items ?? []).some((it) => it.kind === "ly_thuyet") && (items ?? []).filter((it) => it.kind === "ly_thuyet").every((it) => done.has(it.id));
  useEffect(() => {
    if (!recordProgress || !userId || !theoryMeta) return;
    if (theoryTabDone) {
      clearResumeSpot(userId, id);
      return;
    }
    if (activeTab !== "ly_thuyet" || tocActiveIndex < 0 || tocRead.key !== tocStoreKey || tocActiveIndex < tocRead.max) return;
    const entry = tocEntries[tocActiveIndex];
    const total = tocEntries.length;
    writeResumeSpot(userId, id, {
      heading: entry.heading || entry.itemTitle,
      index: tocActiveIndex,
      total,
      minutesLeft: Math.max(1, Math.round((theoryMeta.minutes * (total - tocActiveIndex)) / total)),
    });
  }, [recordProgress, userId, theoryTabDone, activeTab, theoryMeta, tocActiveIndex, tocRead, tocStoreKey, tocEntries, id]);


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
  // Từ 21/10/2026 nội dung bài (trừ vài bài xem thử) chỉ mở cho tài khoản đăng nhập — RLS trả mục rỗng cho khách.
  if (!loading && !session && items.length === 0) return <LessonLoginWall title={title} />;

  // AVCN, WorldSkills là học phần CTTC: gốc đường dẫn về hub CTTC, không về bộ chọn lớp THPT.
  const isAvcn = isCttcClassSlug(classSlug);
  const rootHref = isAvcn ? "/lop-hoc/cttc" : "/lop-hoc";
  const rootLabel = isAvcn ? "CTTC" : "Lớp học";
  const classHref = classSlug
    ? `/lop-hoc/${classSlug}?subject=${encodeURIComponent(subjectCode)}${chapterId ? `&chapter=${chapterId}#chapter-${chapterId}` : ""}`
    : "/lop-hoc";

  if (isPeriodicExam(lessonKind)) {
    const kindMeta = LESSON_KIND_META[lessonKind];
    const kiemTraItems = items.filter((i) => i.kind === "kiem_tra");
    const examIds = visibleExamIds(kiemTraItems.flatMap((i) => i.exam_ids));
    const itemByExamId = new Map(kiemTraItems.flatMap((i) => i.exam_ids.map((eid) => [eid, i])));
    return (
      <div className={`lesson-shell lesson-page ${isAvcn ? "lesson-shell--cttc" : ""} ${drawerOpen ? "is-drawer-open" : ""}`}>
        <TeacherViewBanner />
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
                    <Link href={rootHref}>{rootLabel}</Link>
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
                      teacherView={isTeacherView}
                      showQr
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
                  showProgress={!!session && !isTeacherView}
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
  // Bài tương ứng trong SGK thống nhất (chỉ L12) — HS mở đúng trang sách.
  const sgkRef = SGK_L12[id];
  const hasLessonMeta =
    lessonKind !== "bai_hoc" || !!assignmentItem?.due_at || lessonTheoryPassed || !!theoryMeta || !!sgkRef;
  // Mục lục: số mục đã đọc (✓). Tab đã xong hết → mọi mục ✓.
  const tocComplete = !!session && !!activeSection && activeSection.items.every(isDone);
  const tocDoneCount = tocComplete ? tocEntries.length : Math.min(tocRead.key === tocStoreKey ? tocRead.max : 0, tocEntries.length);
  const tocCount = !isTeacherView && tocEntries.length > 1 ? `${tocDoneCount}/${tocEntries.length}` : "";
  const stepLabel = !isTeacherView && lessonMarked ? "Đã học xong" : `Mục ${Math.max(activeIndex, 0) + 1}/${totalTabs || 1}`;

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
    const theoryItemsAll = (items ?? []).filter((i) => i.kind === "ly_thuyet");
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
            showMarkDone={recordProgress}
          />
        );

      if (item.kind === "ly_thuyet")
        return (
          <div
            key={item.id}
            id={`lesson-item-${item.id}`}
            className="lesson-stack"
            data-item={item.id}
            // KhungPortals đọc mã bài ở đây để ghi lượt xem/lựa chọn clip (lesson_clip_views, lesson_clip_choices);
            // chỉ học sinh — thiếu thuộc tính này thì không ghi gì (0 dòng 6–25/11/2026).
            data-lesson-id={recordProgress && Number.isFinite(id) ? id : undefined}
          >
            <TheoryBlock
              item={item}
              defaultOpen={itemIndex === 0 || item.id === hashTargetItemId}
              hideTitle={plain}
              done={done.has(item.id)}
              loggedIn={!!session}
              onDone={() => markDone(item)}
              recordProgress={recordProgress}
              forceAllOpen={isTeacherView}
              estimateInHead={plain && theoryMeta !== null}
            />
            {item.exam_ids.length > 0 && (
              <TheoryQuizBlock
                examId={item.exam_ids[0]}
                itemId={item.id}
                status={progress.get(item.id)?.theory}
                loggedIn={!!session}
                teacherView={isTeacherView}
              />
            )}
            {/* Ôn 5 phút: cuối mục Lý thuyết, trước Bài tập mẫu (thầy chốt 25/11/2026; L1, N2, B2). */}
            {Number.isFinite(id) && item.id === theoryItemsAll[theoryItemsAll.length - 1]?.id && (
              <OnNamPhutGon lessonId={id} theoryHtml={item.body_html ?? undefined} theoryItemId={item.id} />
            )}
          </div>
        );

      if (isGradedKind(item.kind))
        return (
          <GradedItemBlock
            key={item.id}
            item={item}
            plain={plain}
            examIds={visibleExamIds(item.exam_ids)}
            graded={progress.get(item.id)?.graded}
            examMetas={examMetas}
            scores={scores}
            loggedIn={!!session}
            metaStatus={examMetaStatus}
            teacherView={isTeacherView}
          />
        );

      // bai_tap_mau / luyen_tap: lưới từng câu
      return (
        <WorkedPracticeBlock
          key={item.id}
          item={item}
          plain={plain}
          showSummaries={item.kind === "luyen_tap" && itemIndex === 0}
          theoryItems={theoryItemsAll}
          workedState={workedState}
          onRetryWorked={retryWorked}
          onPresent={canPresent ? (start) => setChieuBtm({ itemId: item.id, start }) : undefined}
          lessonId={id}
          poolExamIds={lessonExamIds}
          recordProgress={recordProgress}
          practiceActiveRef={practiceActiveRef}
          done={done.has(item.id)}
          onDone={() => markDone(item)}
        />
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

  // Trình chiếu (chỉ giáo viên) tách khỏi bảng Aa: còn đúng 2 nút ở đầu trang (N2, 26/10/2026).
  const presentButton = canPresent && theoryItems.length > 0 && (
    <button
      type="button"
      className="lesson-present-btn"
      onClick={() => setPresenting(true)}
      title="Chiếu lên tivi / máy chiếu: lật từng mục, bút khoanh ý chính, phóng to chữ"
      aria-label="Trình chiếu"
    >
      <MonitorPlay size={16} aria-hidden />
      <span className="lesson-tool-text">Trình chiếu</span>
    </button>
  );

  // Bản chiếu "trên lớp" dựng riêng cho tivi (features/lessons/tren-lop.ts) — chỉ giáo viên, chỉ bài đã có bản chiếu.
  const banChieu = canPresent ? banChieuCuaBai(id) : undefined;
  const banChieuButton = banChieu && (
    <a
      className="lesson-present-btn"
      href={linkBanChieu(banChieu.slug)}
      target="_blank"
      rel="noopener"
      title="Bản chiếu trên lớp cho tivi: mỗi màn một ý, clip tự dừng, cuối tiết mã QR đề kiểm tra (mở tab mới, F11)"
      aria-label="Bản chiếu lớp"
    >
      <Tv size={16} aria-hidden />
      <span className="lesson-tool-text">Bản chiếu lớp</span>
    </a>
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
        {courseLessons.length > 0 && !isTeacherView && (
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
    const multiItemToc = new Set(tocEntries.map((e) => e.itemTitle)).size > 1;
    return (
      <>
        {/* Mục lục bài này — scroll-spy trên các h2/h3 của tab đang mở, 0 request. */}
        <div className="lesson-panel lesson-toc">
          <p className="lesson-panel-title lesson-toc-title">
            Mục lục bài {tocCount && <span>{tocCount}</span>}
          </p>
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
                    multiItemToc &&
                    !!entry.heading &&
                    entry.heading !== entry.itemTitle &&
                    shownToc[index - 1]?.itemTitle !== entry.itemTitle;
                  const label = entry.heading || entry.itemTitle;
                  const numbered = /^([IVXLC]+|\d+)[.)]\s+(.+)$/.exec(label);
                  const order = tocEntries.indexOf(entry);
                  const isActive = activeHeading === entry.id;
                  const isRead = !isActive && !isTeacherView && (tocComplete || order < tocDoneCount);
                  return (
                    <li key={entry.id}>
                      <a
                        href={`#${entry.id}`}
                        className={`${isActive ? "is-active" : ""} ${isRead ? "is-done" : ""}`}
                        aria-current={isActive ? "location" : undefined}
                        onClick={(e) => {
                          e.preventDefault();
                          flashTheorySection(entry.id, 2);
                        }}
                      >
                        <i className="lesson-toc-n" aria-hidden>
                          {isRead ? "✓" : numbered ? numbered[1] : order + 1}
                        </i>
                        <span>
                          {showItemLabel && <small className="lesson-toc-item">{entry.itemTitle}</small>}
                          {numbered ? numbered[2] : label}
                          {isRead && <span className="sr-only"> (đã đọc)</span>}
                        </span>
                      </a>
                    </li>
                  );
                })}
              </ol>
              {shownToc.length === 0 && <p className="lesson-panel-empty">Không thấy đề mục nào khớp.</p>}
            </>
          )}
        </div>

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
            Sổ câu sai của bài ›
          </Link>
        )}
      </>
    );
  }

  /** Cuối bài: Mức độ thành thạo (kèm Làm mới, Luyện thêm) và Ghi chú của em. Dời khỏi rail để rail chỉ còn
   *  "mình đang ở đâu" như bản duyệt (B5/B7); đặt ở cuối vì mức độ có nghĩa sau khi học/làm xong (L5). */
  function renderEndPanels() {
    if (!items || items.length === 0) return null;
    return (
      <div className="lesson-endpanels">
        <LessonMasteryCard lessonId={id} examIds={lessonExamIds} loggedIn={recordProgress} initial={masteryInitial} />
        {!canPresent && (
          <button
            type="button"
            className="lesson-panel lesson-note-open"
            onClick={() => window.dispatchEvent(new Event(OPEN_STUDENT_NOTE_EVENT))}
          >
            Ghi chú của em
          </button>
        )}
      </div>
    );
  }

  /** Dòng meta: ≥1024 ngay dưới tên bài; < 1024 tên bài lên thanh bài nên dòng này xuống dưới dải tab (bản duyệt). */
  function renderMeta(className: string) {
    return (
      <div className={className}>
        {theoryMeta && (
          <span className="lesson-meta-time">
            ~{theoryMeta.minutes} phút · {theoryMeta.total} mục
            {theoryMeta.quizzes > 0 ? ` · ${theoryMeta.quizzes} câu tự kiểm tra` : ""}
          </span>
        )}
        {sgkRef && <span className="lesson-meta-sgk">SGK: {sgkRef}</span>}
        {lessonKind !== "bai_hoc" && <span className="lesson-meta-chip">{lessonTypeLabel}</span>}
        {assignmentItem?.due_at && <span>BTVN hạn {formatDue(assignmentItem.due_at)}</span>}
        {lessonTheoryPassed && (
          <span className="lesson-meta-ok">
            <Check size={13} aria-hidden /> Đã xem lý thuyết
          </span>
        )}
      </div>
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
    <div className={`lesson-shell lesson-page ${isAvcn ? "lesson-shell--cttc" : ""} ${dim ? "is-dim" : ""} ${drawerOpen ? "is-drawer-open" : ""}`}>
      <TeacherViewBanner />
      <div className="lesson-layout lesson-layout--rail">
        {/* Rail trái = "mình đang ở đâu", cùng cạnh với rail chương ở trang chương (B5, 26/10/2026): lối về
            chương + mục lục bài này + dụng cụ. Bài trước/Bài sau xuống cuối bài (.lesson-pager) và thanh đáy.
            Cây chương đầy đủ vẫn ở ngăn kéo "Mục lục" và trang lớp (N4). */}
        <aside className="lesson-nav lesson-nav--rail" aria-label="Điều hướng bài học">
          <Link href={classHref} className="lesson-rail-back">
            <ArrowLeft size={15} aria-hidden />
            <span>{chapterFullLabel || "Về chương"}</span>
          </Link>
          {renderSidePanels()}
        </aside>

        <div className="lesson-main" ref={mainRef}>
          <header className="lesson-head">
            {/* < 1024: ‹ về chương (bản duyệt) thay cho "Quay lại" lịch sử — trang chương có đủ thanh site. */}
            <Link href={classHref} className="lesson-head-back" aria-label={`Về ${chapterFullLabel || "chương"}`}>
              <ArrowLeft size={16} aria-hidden />
            </Link>
            <div className="lesson-head-text">
              <nav className="lesson-breadcrumb" aria-label="Đường dẫn">
                <span className="lesson-crumb-class">
                  {classSlug ? <Link href={rootHref}>{rootLabel}</Link> : <span>Lớp học</span>}
                  <span aria-hidden className="lesson-crumb-sep">›</span>
                </span>
                <Link href={classHref} className="lesson-crumb-chapter">
                  {chapterFullLabel || "Chương"}
                </Link>
              </nav>
              <h1>{title}</h1>
              {hasLessonMeta && renderMeta("lesson-meta")}
            </div>
            {banChieuButton ? (
              <div className="lesson-present-group">
                {presentButton}
                {banChieuButton}
              </div>
            ) : (
              presentButton
            )}
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
            {!isTeacherView && (
              <div className="lesson-progressbar" aria-label={`Đã học ${progressDone} trên ${totalTabs} mục`}>
                <span style={{ width: `${totalTabs ? Math.round((progressDone / totalTabs) * 100) : 0}%` }} />
                <small>
                  Đã học {progressDone}/{totalTabs} mục
                </small>
              </div>
            )}

            {tabNav}
            {hasLessonMeta && renderMeta("lesson-meta lesson-meta--below-tabs")}

            <div className="lesson-body" ref={bodyRef}>
            {reviewBanner}

            {subjectCode === HSG_SUBJECT_CODE && activeSection?.kind === "ly_thuyet" && <NenKhtn9 lessonIds={[id]} />}

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
                {activeSection.kind === "ly_thuyet" && <AroundReadMore lessonId={id} />}
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

            {bodyReady && renderEndPanels()}

            {/* Bài trước / Bài sau ở CUỐI bài (B5/D3): hết bài mới mời đi tiếp, không treo ở góc trên. */}
            {(prevLesson || nextLesson) && (
              <nav className="lesson-pager" aria-label="Bài trước và bài sau">
                {prevLesson ? (
                  <Link href={siblingHref(prevLesson)} className="lesson-pager-link">
                    <small>‹ Bài trước</small>
                    <span>{prevLesson.title}</span>
                  </Link>
                ) : (
                  <Link href={classHref} className="lesson-pager-link">
                    <small>‹ Về chương</small>
                    <span>{chapterFullLabel || "Chương"}</span>
                  </Link>
                )}
                {nextLesson && (
                  <Link href={siblingHref(nextLesson)} className="lesson-pager-link lesson-pager-link--next">
                    <small>Bài sau ›</small>
                    <span>{nextLesson.title}</span>
                  </Link>
                )}
              </nav>
            )}

            </div>
          </div>
        </div>
      </div>

      {/* Thanh đáy theo bản duyệt: Mục lục x/y · Học xong · Bài sau. Bỏ nút Trang chủ: nút ‹ ở thanh bài đã về
          trang chương (có đủ thanh site), ba nút còn lại rộng hơn cho ngón cái (D2). */}
      <nav className="lesson-bottombar lesson-bottombar--mobile lesson-bottombar--3" aria-label="Điều hướng bài học">
        <button
          type="button"
          className="lesson-bottom-link"
          onClick={() => setDrawerOpen(true)}
          aria-expanded={drawerOpen}
          aria-controls="lesson-drawer"
        >
          <Menu size={16} aria-hidden />
          <span>Mục lục{tocCount ? ` ${tocCount}` : ""}</span>
        </button>
        {!isTeacherView && (
          <button
            type="button"
            className={`lesson-bottom-done ${lessonMarked ? "is-done" : ""}`}
            onClick={markLessonDone}
            disabled={lessonMarked}
            aria-pressed={lessonMarked}
            aria-label={lessonMarked ? "Đã đánh dấu: học xong bài này" : "Đánh dấu đã học xong bài này"}
          >
            {lessonMarked ? <Check size={16} aria-hidden /> : <span className="lesson-checkbox" aria-hidden />}
            <span>Học xong</span>
          </button>
        )}

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
                {!isTeacherView && (
                  <small>
                    Đã học {progressDone}/{totalTabs} mục
                  </small>
                )}
              </div>
              <button type="button" onClick={() => setDrawerOpen(false)} aria-label="Đóng mục lục">
                <X size={17} aria-hidden />
              </button>
            </div>
            <div className="lesson-drawer-body">
              {/* Mục lục BÀI này lên đầu — cùng nội dung rail trái máy tính (B5); cây cả khoá ở dưới. */}
              {renderSidePanels()}
              {renderCourseInfo()}
              <ChapterTree
                entries={courseChapters}
                mode="learn"
                currentLessonId={id}
                openChapterIds={openChapterIds}
                onToggleChapter={toggleChapter}
                lessonHref={siblingHref}
                isLessonDone={lessonComplete}
                showProgress={!!session && !isTeacherView}
                filterLessonIds={matchingLessonIds}
              />
            </div>
          </div>
        </div>
      )}

      {canPresent && Number.isFinite(id) && <LessonNoteFab lessonId={id} getContext={getNoteContext} />}
      {canPresent && Number.isFinite(id) && (
        <RandomCallFab lessonId={id} classes={callClasses} defaultClassId={callDefaultClassId} />
      )}
      {!canPresent && Number.isFinite(id) && <StudentNoteFab lessonId={id} getContext={getNoteContext} />}

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
      {/* Trình chiếu bài tập mẫu — dựng từ các dạng đã tải sẵn của mục (0 request mới), tải chậm, chỉ giáo viên. */}
      {chieuBtm && (() => {
        const it = items?.find((x) => x.id === chieuBtm.itemId);
        return it && it.questions.length > 0 ? (
          <BtmPresenter
            questions={it.questions}
            start={chieuBtm.start}
            title={title}
            lessonId={Number.isFinite(id) ? id : undefined}
            itemId={it.id}
            onClose={() => setChieuBtm(null)}
          />
        ) : null;
      })()}
    </div>
  );
}

export default function LessonPage() {
  return (
    <>
      <Navbar />
      <main className="min-h-screen w-full pt-[76px] lesson-page-main">
        <Suspense fallback={<p className="lesson-notice">Đang tải…</p>}>
          <LessonLoader />
        </Suspense>
      </main>
      <Footer variant="app" />
    </>
  );
}
