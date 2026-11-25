"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import { ArrowRight, Check, ChevronDown, FileText, Play } from "lucide-react";
import ContentHtml from "@/components/exams/ContentHtml";
import TheoryRpBar, { TheoryRpHint, useTheoryRp } from "@/components/lessons/TheoryRpBar";
import { useReadDepth } from "@/components/lessons/useReadDepth";
import {
  splitTheorySections,
  splitTheorySteps,
  estimateTheoryTime,
  decorateGoalBox,
} from "@/features/lessons/theory-sections";
import { withMarginNotes } from "@/features/lessons/margin-notes";
import { type LessonItem } from "@/features/lessons/types";
import type { TheoryStatusResult } from "@/features/progress/types";

import { THEORY_POS_STORE, OPEN_SECTION_EVENT, scrollToPart } from "./lesson-nav";

/** Ý chính/công thức cần thuộc của các mục lý thuyết — đặt ở đầu tab Luyện tập (không còn
 *  nằm trong tab Lý thuyết) để học sinh ôn lại ngay trước khi làm bài. Mặc định THU GỌN chỉ
 *  còn dòng nhãn (bài có nhiều mục lý thuyết thì khối này dài, đẩy câu hỏi xuống xa) — bấm
 *  nhãn mới xổ ra. Rỗng (chưa backfill) thì không hiện gì. */
export function TheorySummary({ html, title }: { html: string; title?: string }) {
  const [open, setOpen] = useState(false);
  if (!html.trim()) return null;
  return (
    <div className={`lesson-summary ${open ? "is-open" : ""}`}>
      <button type="button" className="lesson-summary-toggle" onClick={() => setOpen((o) => !o)} aria-expanded={open}>
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
export function TheoryBlock({
  item,
  defaultOpen,
  hideTitle,
  done,
  loggedIn,
  onDone,
  recordProgress = true,
  forceAllOpen = false,
  estimateInHead = false,
}: {
  item: LessonItem;
  defaultOpen: boolean;
  hideTitle: boolean; // tên mục trùng tên phần → khỏi lặp

  done: boolean;
  loggedIn: boolean;
  onDone: () => void;
  /** false = chế độ giáo viên: không gọi RP, không gửi độ sâu đọc. */
  recordProgress?: boolean;
  /** Mở sẵn mọi mốc để đọc, không đi lần lượt bằng nút Tiếp. */
  forceAllOpen?: boolean;
  /** Thời lượng · số mục · số câu đã hiện ở dòng meta dưới tên bài → không lặp trong thẻ đọc (N4). */
  estimateInHead?: boolean;
}) {
  const [open, setOpen] = useState(defaultOpen);
  const hasBody = item.body_html.trim() !== "";
  // Tách theo từng mốc <h3> — cùng hàm với mục lục (tocEntries) và "Ôn ngay" nên id
  // `theory-sec-<itemId>-<n>` khớp nhau; chỉ tính lại khi nội dung mục thật sự đổi.
  // Chú thích/định nghĩa/ô số của từng đoạn chép thêm một bản cho cột lề phải ≥ 1280px (features/lessons/margin-notes.ts).
  const displayHtml = useMemo(() => withMarginNotes(decorateGoalBox(item.body_html)), [item.body_html]);
  const { introHtml, sections } = useMemo(() => splitTheorySections(displayHtml, item.id), [displayHtml, item.id]);
  const total = sections.length;
  // Mốc có ≥ 2 mục con cấp đầu (<h4>, hộp bẫy) → đi từng mục con (xem splitTheorySteps).
  const steps = useMemo(() => sections.map((s) => splitTheorySteps(s.html)), [sections]);
  // Số mục con đang hiện của mỗi mốc. Chỉ đặt khi học sinh đi bằng "Tiếp" / tiêu đề / "Tiếp tục"; mốc mở bằng
  // mục lục / "Ôn ngay" / "Mở tất cả" không có khoá → hiện đủ (đích cuộn có thể nằm ở mục con cuối).
  const [stepShown, setStepShown] = useState<Record<number, number>>({ 0: 1 });
  const estimate = useMemo(() => estimateTheoryTime(item.body_html), [item.body_html]);
  const [openSections, setOpenSections] = useState<Set<number>>(() => new Set([0]));
  const [allOpen, setAllOpen] = useState(forceAllOpen);
  const [seenForceAll, setSeenForceAll] = useState(forceAllOpen);
  // Hồ sơ giáo viên có thể về sau lúc mount: mở hết mốc khi biết là chế độ giáo viên.
  if (forceAllOpen !== seenForceAll) {
    setSeenForceAll(forceAllOpen);
    if (forceAllOpen) setAllOpen(true);
  }
  const [resumeIndex, setResumeIndex] = useState<number | null>(null);
  const rootRef = useRef<HTMLDivElement>(null);
  const rp = useTheoryRp(item.id, recordProgress && loggedIn && open ? item.body_html : "", rootRef);
  const quizTotal = useMemo(() => (item.body_html.match(/class="[^"]*\btl-quiz\b/g) ?? []).length, [item.body_html]);
  // Việc 6: độ sâu cuộn (mốc h3) + tỉ lệ bấm quiz, gửi khi rời mục/ẩn tab — không thêm round-trip lúc tải.
  useReadDepth({
    itemId: item.id,
    active: recordProgress && loggedIn && open && hasBody,
    h3Total: total,
    quizTotal,
    rootRef,
    openKey: allOpen ? "all" : `${Array.from(openSections).join(",")}|${JSON.stringify(stepShown)}`,
  });
  const isOpen = (i: number) => allOpen || openSections.has(i);
  // Mốc i đã hiện hết mục con chưa (mốc không chia mục con coi như đã hết) — chỉ khi đó mới hiện nút "Tiếp" sang mốc sau.
  const stepsDone = (i: number) => allOpen || !steps[i] || (stepShown[i] ?? Infinity) >= steps[i]!.length;
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
    setStepShown((prev) => (index in prev ? prev : { ...prev, [index]: 1 }));
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
      if (Number.isInteger(index) && index >= 0) {
        openSection(index);
        setStepShown((prev) => {
          if (!(index in prev)) return prev;
          const next = { ...prev };
          delete next[index]; // đích cuộn có thể ở mục con chưa mở → hiện đủ cả mốc
          return next;
        });
      }
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
  }, [item.id, total, open, openSections, allOpen, stepShown]);

  const resume = resumeIndex !== null && !isOpen(resumeIndex) ? sections[resumeIndex] : null;

  return (
    <div className={`lesson-block ${hideTitle ? "lesson-block--plain" : ""}`} ref={rootRef}>
      {!hideTitle && (
        <button
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
        </button>
      )}
      {open && hasBody && (
        <div className={hideTitle ? "lesson-prose lesson-prose--plain" : "lesson-prose"}>
          <TheoryRpHint rp={rp} />
          {total === 0 ? (
            <ContentHtml html={displayHtml} className="block leading-relaxed" />
          ) : (
            <>
              {total > 1 && (
                <div className="theory-nav">
                  {resume ? (
                    <button
                      type="button"
                      className="theory-next theory-resume"
                      onClick={() => goTo(resumeIndex!, true)}
                    >
                      <small>
                        Tiếp tục · {resumeIndex! + 1}/{total}
                      </small>
                      <strong>{resume.heading}</strong>
                      <Play size={14} fill="currentColor" aria-hidden />
                    </button>
                  ) : estimateInHead ? (
                    <span />
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
                const coveredByNext = !opened && i > 0 && isOpen(i - 1) && stepsDone(i - 1);
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
                        {(() => {
                          const parts = steps[i];
                          const shown = allOpen || !parts ? Infinity : (stepShown[i] ?? Infinity);
                          // Mốc có mục con luôn dựng theo từng mục con (kể cả khi đã hiện đủ) để bấm "Tiếp" không
                          // dựng lại phần đã đọc — dựng lại sẽ xoá lựa chọn quiz em vừa bấm.
                          if (!parts) return <ContentHtml html={section.html} className="block leading-relaxed" />;
                          const after = shown < parts.length ? parts[shown] : null;
                          return (
                            <>
                              {parts.slice(0, shown).map((p, k) => (
                                <div key={k} id={`theory-step-${item.id}-${i}-${k}`}>
                                  <ContentHtml html={p.html} className="block leading-relaxed" />
                                </div>
                              ))}
                              {after && (
                                <button
                                  type="button"
                                  className="theory-next theory-next--step"
                                  onClick={() => {
                                    setStepShown((prev) => ({ ...prev, [i]: shown + 1 }));
                                    window.setTimeout(() => scrollToPart(`theory-step-${item.id}-${i}-${shown}`), 60);
                                  }}
                                >
                                  <small>
                                    Tiếp · phần {shown + 1}/{parts.length}
                                  </small>
                                  <strong>{after.heading}</strong>
                                  <ArrowRight size={16} aria-hidden />
                                </button>
                              )}
                            </>
                          );
                        })()}
                        {next && !isOpen(i + 1) && stepsDone(i) && (
                          <button type="button" className="theory-next" onClick={() => goTo(i + 1, true)}>
                            <small>
                              Tiếp · {i + 2}/{total}
                            </small>
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
        {recordProgress && loggedIn && open && hasBody && <TheoryRpBar rp={rp} />}
        {recordProgress && loggedIn && open && (
          <button type="button" className={`lesson-done ${done ? "is-done" : ""}`} onClick={onDone} disabled={done}>
            <Check size={14} /> {done ? "Đã tự xác nhận đọc" : "Tôi đã đọc xong"}
          </button>
        )}
      </div>
    </div>
  );
}

/** Quiz kiểm tra nhanh cuối lý thuyết: badge trạng thái + nút vào làm/làm lại, giữ lịch sử từng lần. */
export function TheoryQuizBlock({
  examId,
  itemId,
  status,
  loggedIn,
  teacherView = false,
}: {
  examId: number;
  itemId: number;
  status: TheoryStatusResult | undefined;
  loggedIn: boolean;
  teacherView?: boolean;
}) {
  const attempted = !!status && status.attemptCount > 0;
  const tone = status?.status === "passed" ? "lesson-status-done" : attempted ? "lesson-status" : "lesson-status";
  return (
    <div className="lesson-exam">
      <div>
        <p className="lesson-block-title">Kiểm tra nhanh</p>
        <p className="lesson-block-sub">
          {!teacherView && status?.status === "passed" && `Đúng ${status.bestCorrect} câu — `}
          {!teacherView &&
            status?.status === "completed_not_passed" &&
            `Đúng ${status.bestCorrect} câu, chưa đạt (lần ${status.attemptCount}) — `}
          {teacherView ? (
            <span className="lesson-status">Xem đáp án, không ghi lượt làm</span>
          ) : loggedIn ? (
            <span className={tone}>{status?.label ?? "Chưa bắt đầu"}</span>
          ) : (
            <span className="lesson-status">Đăng nhập để làm và lưu kết quả</span>
          )}
        </p>
      </div>
      {loggedIn ? (
        <Link
          href={`/kiem-tra/lam?id=${examId}&item=${itemId}`}
          className={attempted && !teacherView ? "lesson-btn-ghost" : "lesson-btn"}
        >
          {teacherView ? "Xem đề và đáp án" : attempted ? "Làm lại" : "Làm kiểm tra nhanh"}
        </Link>
      ) : (
        <Link href="/dang-nhap" className="lesson-btn">
          Đăng nhập để làm
        </Link>
      )}
    </div>
  );
}
