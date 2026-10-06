"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { DIFFICULTY_LABELS } from "@/features/exams/types";
import type { ExamMeta } from "@/services/content";

/**
 * Kệ đề thi của lớp: thay danh sách phẳng (hàng trăm đề xếp theo ngày đăng) bằng các "kệ" theo
 * mục đích dùng — học sinh vào là thấy ngay đề sắp thi / đề mới, không phải kéo hết trang.
 * Phân loại theo tiêu đề (đề đăng hàng loạt không có trường loại riêng).
 */
type ShelfKey = "moi" | "thi-thu" | "cuoi-ki" | "giua-ki" | "chuong";

const SHELVES: { key: ShelfKey; label: string; hint: string }[] = [
  { key: "moi", label: "Mới đăng", hint: "Đề thầy vừa thêm gần đây" },
  { key: "thi-thu", label: "Thi thử tốt nghiệp", hint: "Đề thi thử THPT, đề minh hoạ, đề của các sở/trường" },
  { key: "cuoi-ki", label: "Cuối học kì", hint: "Ôn trước kì thi cuối học kì" },
  { key: "giua-ki", label: "Giữa học kì", hint: "Ôn trước kì thi giữa học kì" },
  { key: "chuong", label: "Luyện theo chương", hint: "Đề 15–45 phút theo từng chương, từng chủ đề" },
];

const PAGE = 6;
const NEW_DAYS = 14;

export function examShelfOf(title: string): Exclude<ShelfKey, "moi"> {
  const t = title.toLowerCase();
  if (/thi thử|tốt nghiệp|\btn\s*thpt|minh họa|minh hoạ|đề thi sở|sở gd/.test(t)) return "thi-thu";
  if (/cuối\s*(học\s*)?(kì|kỳ)|\bck\s*\d?\b|\bhk\s*\d\b|học\s*(kì|kỳ)\s*\d?\s*$/.test(t)) return "cuoi-ki";
  if (/giữa\s*(học\s*)?(kì|kỳ)|\bgk\s*\d?\b/.test(t)) return "giua-ki";
  return "chuong";
}

export default function ExamShelf({ exams }: { exams: ExamMeta[] }) {
  const [active, setActive] = useState<ShelfKey | "all">("all");
  const [shown, setShown] = useState<Record<string, number>>({});

  const shelves = useMemo(() => {
    // Mốc "mới" tính từ đề đăng gần nhất (không dùng Date.now để render thuần).
    const newest = exams.reduce((m, e) => Math.max(m, new Date(e.created_at).getTime()), 0);
    const cutoff = newest - NEW_DAYS * 86400000;
    const map: Record<ShelfKey, ExamMeta[]> = { moi: [], "thi-thu": [], "cuoi-ki": [], "giua-ki": [], chuong: [] };
    for (const e of exams) {
      map[examShelfOf(e.title)].push(e);
      if (new Date(e.created_at).getTime() >= cutoff) map.moi.push(e);
    }
    map.moi = map.moi.slice(0, PAGE);
    return map;
  }, [exams]);

  const visible = SHELVES.filter((s) => shelves[s.key].length > 0 && (active === "all" || active === s.key));
  if (exams.length === 0) return null;

  return (
    <section className="lesson-section" aria-label="Đề thi">
      <h2>Đề thi</h2>
      <div className="class-subjects" role="tablist" aria-label="Loại đề">
        <button type="button" role="tab" aria-selected={active === "all"} className={active === "all" ? "is-active" : ""} onClick={() => setActive("all")}>
          Tất cả
        </button>
        {SHELVES.filter((s) => shelves[s.key].length > 0).map((s) => (
          <button
            key={s.key}
            type="button"
            role="tab"
            aria-selected={active === s.key}
            className={active === s.key ? "is-active" : ""}
            onClick={() => setActive(s.key)}
          >
            {s.label}
          </button>
        ))}
      </div>
      {visible.map((s) => {
        const list = shelves[s.key];
        const limit = shown[s.key] ?? PAGE;
        const rest = s.key === "moi" ? 0 : list.length - limit;
        return (
          <div key={s.key} className="mt-5">
            <h3 className="text-base font-semibold">
              {s.label} <span className="lesson-muted font-normal">· {list.length} đề</span>
            </h3>
            <p className="lesson-muted" style={{ marginTop: 2 }}>{s.hint}</p>
            <ol className="class-lessons class-lessons--flat">
              {list.slice(0, s.key === "moi" ? PAGE : limit).map((exam) => (
                <li key={`${s.key}-${exam.id}`}>
                  <Link href={`/kiem-tra/lam?id=${exam.id}`} className="class-lesson">
                    <span className="class-lesson-title">{exam.title}</span>
                    <span className="class-meta">
                      {exam.question_count} câu · {exam.duration_minutes} phút
                      {exam.difficulty && ` · ${DIFFICULTY_LABELS[exam.difficulty]}`}
                    </span>
                  </Link>
                </li>
              ))}
            </ol>
            {rest > 0 && (
              <button type="button" className="lesson-link" onClick={() => setShown((m) => ({ ...m, [s.key]: limit + 12 }))}>
                Xem thêm {Math.min(rest, 12)} đề
              </button>
            )}
          </div>
        );
      })}
    </section>
  );
}
