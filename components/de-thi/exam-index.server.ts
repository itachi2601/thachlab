// Đọc public/data/exam-index.json (sinh bởi scripts/build-content.mjs) lúc render trang /de-thi.
// Chỉ metadata — không câu hỏi/đáp án. Không gọi Supabase.
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { displayExamName } from "@/lib/exam-title";

export type ExamShelf = "giua-ki" | "cuoi-ki" | "thi-thu";

export interface ExamIndexItem {
  id: number;
  /** Tên đã bỏ tiền tố loại đề và hậu tố "(đã lược…)". */
  name: string;
  shelf: ExamShelf;
  grade: string;
  year: string;
  /** "HK1" / "HK2" khi tên đề có ghi, ngược lại rỗng. */
  term: string;
  questionCount: number;
  durationMinutes: number;
}

interface RawExam {
  id: number;
  title: string;
  shelf: string;
  grade: string;
  year: string;
  questionCount: number;
  durationMinutes: number;
}

const SHELVES = new Set<string>(["giua-ki", "cuoi-ki", "thi-thu"]);

export function readExamIndex(): ExamIndexItem[] {
  try {
    const raw = readFileSync(join(process.cwd(), "public", "data", "exam-index.json"), "utf8");
    const parsed = JSON.parse(raw) as { exams?: RawExam[] };
    if (!Array.isArray(parsed.exams)) return [];
    return parsed.exams
      .filter((e) => e && typeof e.id === "number" && SHELVES.has(e.shelf) && !/^luyện tập/i.test(e.title))
      .map((e) => ({
        id: e.id,
        name: displayExamName(e.title),
        shelf: e.shelf as ExamShelf,
        grade: e.grade,
        year: e.year,
        term: e.title.match(/\bHK([12])\b/i)?.[0].toUpperCase() ?? "",
        questionCount: e.questionCount,
        durationMinutes: e.durationMinutes,
      }));
  } catch {
    return [];
  }
}
