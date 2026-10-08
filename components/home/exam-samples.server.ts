// Đọc public/data/exam-samples.json lúc render trang chủ (server). Không gọi Supabase.
import { readFileSync } from "node:fs";
import { join } from "node:path";
import type { ExamSample, ExamSampleCard } from "@/components/home/exam-sample-types";

function readFile(): ExamSample[] {
  try {
    const raw = readFileSync(join(process.cwd(), "public", "data", "exam-samples.json"), "utf8");
    const parsed = JSON.parse(raw) as { samples?: ExamSample[] };
    if (!Array.isArray(parsed.samples)) return [];
    return parsed.samples.filter(
      (s) =>
        s &&
        typeof s.id === "number" &&
        typeof s.label === "string" &&
        typeof s.question?.question === "string" &&
        s.question.question.length > 0,
    );
  } catch {
    return [];
  }
}

/** Thẻ trang chủ — không kèm câu hỏi, để HTML trang chủ không mang đề bài. */
export function readExamSampleCards(): ExamSampleCard[] {
  return readFile().map((sample) => ({
    id: sample.id,
    shelf: sample.shelf,
    label: sample.label,
    gradeLabel: sample.gradeLabel,
    grade: sample.grade,
    classId: sample.classId,
    classSlug: sample.classSlug,
    year: sample.year,
    questionCount: sample.questionCount,
    durationMinutes: sample.durationMinutes,
  }));
}
