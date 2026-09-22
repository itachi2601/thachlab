import { getSupabase } from "@/services/supabase";

// Field trong app dùng camelCase để khớp với cấu trúc CncCourseItem cũ
// (shortTitle/duration/…) — cột DB vẫn snake_case như các bảng khác.
export interface CncLesson {
  id: string;
  title: string;
  shortTitle: string;
  duration: string;
  emphasis: string | null;
  bodyHtml: string;
  resources: string[];
  sortOrder: number;
}

const COLUMNS = "id, title, short_title, duration_label, emphasis, body_html, resources, sort_order";

function normalize(row: Record<string, unknown>): CncLesson {
  return {
    id: row.id as string,
    title: row.title as string,
    shortTitle: row.short_title as string,
    duration: (row.duration_label as string) ?? "",
    emphasis: (row.emphasis as string | null) ?? null,
    bodyHtml: (row.body_html as string) ?? "",
    resources: (row.resources as string[] | null) ?? [],
    sortOrder: (row.sort_order as number) ?? 0,
  };
}

export async function fetchCncLessons(): Promise<CncLesson[]> {
  const { data, error } = await getSupabase()
    .from("cnc_lessons")
    .select(COLUMNS)
    .order("sort_order")
    .order("id");
  if (error) throw error;
  return (data ?? []).map(normalize);
}

export async function fetchCncLesson(id: string): Promise<CncLesson | null> {
  const { data, error } = await getSupabase()
    .from("cnc_lessons")
    .select(COLUMNS)
    .eq("id", id)
    .maybeSingle();
  if (error) throw error;
  return data ? normalize(data) : null;
}

export interface CncLessonInput {
  id: string;
  title: string;
  shortTitle: string;
  duration: string;
  emphasis: string | null;
  bodyHtml: string;
  resources: string[];
  sortOrder: number;
}

function toRow(input: Partial<CncLessonInput>): Record<string, unknown> {
  const row: Record<string, unknown> = {};
  if (input.id !== undefined) row.id = input.id;
  if (input.title !== undefined) row.title = input.title;
  if (input.shortTitle !== undefined) row.short_title = input.shortTitle;
  if (input.duration !== undefined) row.duration_label = input.duration;
  if (input.emphasis !== undefined) row.emphasis = input.emphasis;
  if (input.bodyHtml !== undefined) row.body_html = input.bodyHtml;
  if (input.resources !== undefined) row.resources = input.resources;
  if (input.sortOrder !== undefined) row.sort_order = input.sortOrder;
  return row;
}

export async function createCncLesson(input: CncLessonInput): Promise<CncLesson> {
  const { data, error } = await getSupabase()
    .from("cnc_lessons")
    .insert(toRow(input))
    .select(COLUMNS)
    .single();
  if (error) throw error;
  return normalize(data);
}

export async function updateCncLesson(id: string, patch: Partial<CncLessonInput>): Promise<CncLesson> {
  const { data, error } = await getSupabase()
    .from("cnc_lessons")
    .update(toRow(patch))
    .eq("id", id)
    .select(COLUMNS)
    .single();
  if (error) throw error;
  return normalize(data);
}

export async function deleteCncLesson(id: string): Promise<void> {
  const { error } = await getSupabase().from("cnc_lessons").delete().eq("id", id);
  if (error) throw error;
}

/** Sinh id slug mới không trùng danh sách hiện có, từ tiêu đề gõ vào. */
export function suggestCncLessonId(title: string, existingIds: string[]): string {
  const base =
    title
      .toLowerCase()
      .normalize("NFD")
      .replace(/[̀-ͯ]/g, "")
      .replace(/đ/g, "d")
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-+|-+$/g, "") || "bai-hoc";
  if (!existingIds.includes(base)) return base;
  let i = 2;
  while (existingIds.includes(`${base}-${i}`)) i += 1;
  return `${base}-${i}`;
}
