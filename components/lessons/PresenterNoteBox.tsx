"use client";

import { useEffect, useRef, useState } from "react";
import { addTeacherNote } from "@/services/teacher-notes";
import { TEACHER_NOTE_MAX, TEACHER_NOTE_TAGS, type TeacherNoteTag } from "@/lib/teacher-note-labels";

const TAG_STORE = "thachlab-presenter-note-tag";

function readStoredTag(): TeacherNoteTag {
  try {
    const saved = window.localStorage.getItem(TAG_STORE);
    return TEACHER_NOTE_TAGS.some((t) => t.value === saved) ? (saved as TeacherNoteTag) : "y_tuong";
  } catch {
    return "y_tuong";
  }
}

/**
 * Hộp ghi chú nhanh lúc đang dạy (phím N trong chế độ trình chiếu): một dòng + một nhãn, gắn tự động
 * vào bài, mục và trang chiếu đang xem. Enter lưu, Esc đóng, Shift+Enter xuống dòng.
 * Đặt bên trong lớp phủ trình chiếu (không dùng portal) để vẫn hiện khi đang toàn màn hình.
 * Ghi chú chỉ giáo viên thấy (RLS) — cuối tuần xem lại cùng Claude.
 */
export default function PresenterNoteBox({
  lessonId,
  itemId,
  pageKey,
  pageHeading,
  onClose,
}: {
  lessonId: number;
  itemId: number | null;
  pageKey: string;
  pageHeading: string;
  /** saved = true khi vừa lưu xong (để trình chiếu báo "Đã ghi"). */
  onClose: (saved?: boolean) => void;
}) {
  const [text, setText] = useState("");
  const [tag, setTag] = useState<TeacherNoteTag>(readStoredTag);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  function pickTag(value: TeacherNoteTag) {
    setTag(value);
    try {
      window.localStorage.setItem(TAG_STORE, value);
    } catch {
      /* bỏ qua: chỉ là nhớ nhãn lần trước */
    }
    inputRef.current?.focus();
  }

  async function save() {
    const body = text.trim();
    if (!body || saving) return;
    setSaving(true);
    setError("");
    try {
      await addTeacherNote({ lessonId, itemId, pageKey, pageHeading, tag, body });
      onClose(true);
    } catch {
      // Giữ nguyên chữ đã gõ để thầy bấm lưu lại, không mất ý đang nghĩ.
      setError("Chưa lưu được — kiểm tra mạng rồi bấm Lưu lại.");
      setSaving(false);
    }
  }

  return (
    <div className="presenter-note" role="dialog" aria-label="Ghi chú nhanh cho bài này">
      <p className="presenter-note-where">Gắn vào: {pageHeading}</p>
      <div className="presenter-note-tags" role="group" aria-label="Loại ghi chú">
        {TEACHER_NOTE_TAGS.map((option) => (
          <button
            key={option.value}
            type="button"
            className={tag === option.value ? "is-on" : ""}
            aria-pressed={tag === option.value}
            onClick={() => pickTag(option.value)}
          >
            {option.label}
          </button>
        ))}
      </div>
      <textarea
        ref={inputRef}
        value={text}
        maxLength={TEACHER_NOTE_MAX}
        rows={2}
        placeholder="Một dòng thôi — Enter để lưu, Esc để đóng"
        onChange={(e) => setText(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Escape") {
            e.preventDefault();
            e.stopPropagation();
            onClose();
          } else if (e.key === "Enter" && !e.shiftKey && !e.nativeEvent.isComposing) {
            e.preventDefault();
            void save();
          }
        }}
      />
      {error && <p className="presenter-note-error" role="alert">{error}</p>}
      <div className="presenter-note-actions">
        <button type="button" onClick={() => onClose()}>Đóng</button>
        <button type="button" className="is-on" disabled={!text.trim() || saving} onClick={() => void save()}>
          {saving ? "Đang lưu…" : "Lưu"}
        </button>
      </div>
    </div>
  );
}
