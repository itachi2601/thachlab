// Kiểm + dựng dữ liệu "Bài tập mẫu có cấu trúc" (scripts/data/bai-tap-mau/<lesson_id>.json).
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
export const ROOT = path.resolve(here, "../../../..");
export const DATA_DIR = path.join(ROOT, "scripts/data/bai-tap-mau");
const TOPICS_FILE = path.join(ROOT, "scripts/data/question-topics.json");

export interface Topic { id: number; lesson_id: number; name: string; parent_id: number | null }
export function loadTopics(): Topic[] | null {
  return fs.existsSync(TOPICS_FILE) ? JSON.parse(fs.readFileSync(TOPICS_FILE, "utf8")) : null;
}

const dollarsBalanced = (s: string) => ((s.replace(/\\\$/g, "").match(/\$/g) ?? []).length % 2) === 0;
const ROLE_THAY = /\b(thầy|cô giáo)\b/i; // bài soạn cho HS không dùng vai "thầy" (feedback giọng văn 2/10/2026)

export interface Dang {
  label: string;
  topic: string;
  topic_id?: number;
  form?: string;
  problem_html: string;
  hints_html: string[];
  solution_html: string;
}

/** Gộp thành body_html để mọi nơi cũ (trang tĩnh, importer, accordion) vẫn đọc được. */
export function composeBody(d: Dang): string {
  const hints = d.hints_html.map((h, i) => `<p><strong>Gợi ý ${i + 1}.</strong></p>${h}`).join("\n");
  return `${d.problem_html}\n<details><summary>Gợi ý và lời giải</summary>\n${hints}\n${d.solution_html}\n</details>`;
}

export function validate(data: any, topics: Topic[] | null): { errors: string[]; warnings: string[] } {
  const errors: string[] = [], warnings: string[] = [];
  if (!data || typeof data !== "object") return { errors: ["không phải object JSON"], warnings };
  if (!Number.isInteger(data.lesson_id)) errors.push("thiếu lesson_id (số nguyên)");
  if (!data.review?.checked) errors.push("review.checked chưa true — chưa qua bước kiểm chéo");
  const ds: Dang[] = data.dang_bai;
  if (!Array.isArray(ds) || ds.length < 2 || ds.length > 8) { errors.push("dang_bai cần 2–8 dạng, xếp từ dễ đến khó"); return { errors, warnings }; }
  ds.forEach((d, i) => {
    const at = `dạng ${i + 1}`;
    for (const k of ["label", "topic", "problem_html", "solution_html"] as const)
      if (typeof d[k] !== "string" || !d[k].trim()) errors.push(`${at}: thiếu ${k}`);
    if (!Array.isArray(d.hints_html) || d.hints_html.length !== 3 || d.hints_html.some((h) => !String(h).trim()))
      errors.push(`${at}: cần đúng 3 gợi ý (kiến thức+điều kiện → dữ kiện/hướng → công thức)`);
    const all = [d.problem_html, d.solution_html, ...(d.hints_html ?? [])].join("\n");
    if (!dollarsBalanced(all)) errors.push(`${at}: số dấu $ lẻ`);
    if (/[<>]/.test((all.match(/\$[^$]*\$/g) ?? []).join(""))) errors.push(`${at}: công thức có < hoặc > — viết \\lt / \\gt`);
    if (ROLE_THAY.test(all)) errors.push(`${at}: có vai "thầy/cô" trong nội dung bài`);
    if (!/điều kiện/i.test(d.hints_html?.[0] ?? "")) warnings.push(`${at}: gợi ý 1 chưa nhắc "điều kiện áp dụng" (quy tắc AI-TUTOR 9.1)`);
    if (topics) {
      const hit = topics.find((t) => t.name.trim() === d.topic?.trim());
      if (!hit) errors.push(`${at}: topic "${d.topic}" không có trong question-topics.json`);
      else if (hit.parent_id === null) warnings.push(`${at}: topic là chủ đề cha — nên chọn YCCĐ con sát dạng`);
    } else warnings.push("chưa có question-topics.json — không kiểm topic");
  });
  if (data.tu_luan && (!data.tu_luan.label || !String(data.tu_luan.body_html ?? "").trim())) errors.push("tu_luan cần label + body_html");
  return { errors, warnings };
}
