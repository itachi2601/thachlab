"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { NotebookPen, X } from "lucide-react";
import type { LessonNoteContext } from "@/components/lessons/LessonNoteFab";
import { fetchRemoteNotes, pushRemoteNote, type LessonNote, type LessonNotes } from "@/services/lesson-notes";

const STORE = "thachlab-notes-";
/** Khoá cũ: một ô cho cả bài. Chuyển thành ghi chú "chung" của bài rồi xoá. */
const LEGACY_STORE = "thachlab-note-";
const GENERAL = "_chung";
const KEY_MAX = 80;
export const OPEN_STUDENT_NOTE_EVENT = "thachlab:open-student-note";

function readLocal(lessonId: number): LessonNotes {
  try {
    const raw = window.localStorage.getItem(`${STORE}${lessonId}`);
    const notes: LessonNotes = raw ? (JSON.parse(raw) as LessonNotes) : {};
    const legacy = window.localStorage.getItem(`${LEGACY_STORE}${lessonId}`);
    if (legacy?.trim() && !notes[GENERAL]) notes[GENERAL] = { heading: "Cả bài", body: legacy, at: Date.now() };
    return notes;
  } catch {
    return {};
  }
}

function writeLocal(lessonId: number, notes: LessonNotes) {
  try {
    window.localStorage.setItem(`${STORE}${lessonId}`, JSON.stringify(notes));
    window.localStorage.removeItem(`${LEGACY_STORE}${lessonId}`);
  } catch {
    /* trình duyệt chặn bộ nhớ: vẫn giữ trong phiên */
  }
}

/**
 * Mục lý thuyết đang trong tầm mắt: đoạn `.theory-section` (h3 I., II.…) và mục con h4 (II.1…) gần dòng mắt nhất.
 * Không có (tab khác, bài chưa chia mục) thì dùng ngữ cảnh chung của trang.
 */
function theoryTarget(): { key: string; heading: string } | null {
  const line = window.innerHeight * 0.4;
  let section: HTMLElement | null = null;
  let sub: HTMLElement | null = null;
  let subIndex = 0;
  for (const sec of document.querySelectorAll<HTMLElement>(".theory-section[id]")) {
    if (sec.getBoundingClientRect().top > line) break;
    section = sec;
    sub = null;
    subIndex = 0;
    sec.querySelectorAll<HTMLElement>("h4").forEach((h, i) => {
      if (h.getBoundingClientRect().top <= line) {
        sub = h;
        subIndex = i + 1;
      }
    });
  }
  if (!section) return null;
  const head = (sub as HTMLElement | null) ?? section.querySelector<HTMLElement>("h3, h2");
  const heading = head?.textContent?.replace(/\s+/g, " ").trim() ?? "";
  return { key: subIndex ? `${section.id}-${subIndex}` : section.id, heading };
}

/** Mục (h2/h3) trong ngữ cảnh → khoá ghi chú + nhãn ngắn hiện cho em. */
function toTarget(ctx: LessonNoteContext): { key: string; heading: string } {
  const key = (ctx.pageKey || GENERAL).slice(0, KEY_MAX);
  const heading = ctx.pageHeading.split(" › ").pop() ?? "";
  return { key, heading: key === GENERAL ? "Cả bài" : heading };
}

/**
 * Nút nổi "Ghi chú" cho HỌC SINH + hộp ghi chú theo mục (đề mục đang trong tầm mắt lúc mở). Lưu trên máy trước,
 * rồi đồng bộ lên tài khoản (bảng lesson_notes, chỉ chủ sở hữu thấy) để đổi máy vẫn còn. Tải ghi chú từ tài khoản
 * chỉ khi em mở hộp lần đầu — không thêm request nào lúc tải trang.
 * Quy tắc: D3 (nút ≥44px, cách xa nút Báo lỗi: nằm góc trái), N1 (một hộp, một việc), L4.
 */
export default function StudentNoteFab({
  lessonId,
  getContext,
}: {
  lessonId: number;
  getContext: () => LessonNoteContext;
}) {
  const [open, setOpen] = useState(false);
  const [notes, setNotes] = useState<LessonNotes>({});
  const [target, setTarget] = useState<{ key: string; heading: string }>({ key: GENERAL, heading: "Cả bài" });
  const [status, setStatus] = useState("");
  const fetchedFor = useRef<number | null>(null);
  const pushTimer = useRef<number | undefined>(undefined);

  const openBox = useCallback(() => {
    setNotes(readLocal(lessonId));
    setTarget(theoryTarget() ?? toTarget(getContext()));
    setOpen(true);
  }, [lessonId, getContext]);

  useEffect(() => {
    window.addEventListener(OPEN_STUDENT_NOTE_EVENT, openBox);
    return () => window.removeEventListener(OPEN_STUDENT_NOTE_EVENT, openBox);
  }, [openBox]);

  // Lần mở đầu của bài: gộp ghi chú trên tài khoản (bản nào mới hơn thì thắng).
  useEffect(() => {
    if (!open || fetchedFor.current === lessonId) return;
    fetchedFor.current = lessonId;
    void fetchRemoteNotes(lessonId).then((remote) => {
      if (!remote) return;
      setNotes((local) => {
        const merged: LessonNotes = { ...local };
        for (const [k, r] of Object.entries(remote)) if (!merged[k] || r.at > merged[k].at) merged[k] = r;
        writeLocal(lessonId, merged);
        return merged;
      });
    });
  }, [open, lessonId]);

  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => e.key === "Escape" && setOpen(false);
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open]);

  useEffect(() => () => window.clearTimeout(pushTimer.current), []);

  function edit(body: string) {
    const note: LessonNote = { heading: target.heading, body, at: Date.now() };
    const next = { ...notes };
    if (body.trim()) next[target.key] = note;
    else delete next[target.key];
    setNotes(next);
    writeLocal(lessonId, next);
    setStatus("Đã lưu");
    window.clearTimeout(pushTimer.current);
    pushTimer.current = window.setTimeout(() => void pushRemoteNote(lessonId, target.key, note), 1500);
  }

  const others = useMemo(
    () => Object.entries(notes).filter(([k, n]) => k !== target.key && n.body.trim()),
    [notes, target.key],
  );

  return (
    <div className="student-note-float">
      {!open && (
        <button type="button" className="student-note-fab" onClick={openBox} aria-label="Ghi chú của em cho bài này">
          <NotebookPen size={18} aria-hidden />
          <span>Ghi chú</span>
        </button>
      )}
      {open && (
        <section className="student-note" role="dialog" aria-label="Ghi chú của em">
          <header className="student-note-head">
            <p>
              <strong>Ghi chú của em</strong>
              <span>{target.heading ? `Ở mục: ${target.heading}` : ""}</span>
            </p>
            <button type="button" onClick={() => setOpen(false)} aria-label="Đóng ghi chú">
              <X size={18} aria-hidden />
            </button>
          </header>
          <label className="student-note-label" htmlFor="student-note-body">
            Em còn chưa chắc ở…
          </label>
          <textarea
            id="student-note-body"
            className="student-note-body"
            value={notes[target.key]?.body ?? ""}
            onChange={(e) => edit(e.target.value)}
            maxLength={4000}
            placeholder="Viết ngắn thôi, một dòng cũng được"
          />
          <p className="student-note-status" role="status">
            {status || "Tự lưu khi em gõ; đăng nhập thì đổi máy vẫn còn."}
          </p>
          {others.length > 0 && (
            <ul className="student-note-others" aria-label="Ghi chú ở các mục khác">
              {others.map(([k, n]) => (
                <li key={k}>
                  <button type="button" onClick={() => setTarget({ key: k, heading: n.heading })}>
                    <b>{n.heading || "Cả bài"}</b>
                    <span>{n.body.trim().slice(0, 60)}</span>
                  </button>
                </li>
              ))}
            </ul>
          )}
        </section>
      )}
    </div>
  );
}
