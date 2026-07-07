// Cấu trúc học liệu: Chương → Bài học → Mục (6 loại, thứ tự cố định §1–§6)

export type LessonItemKind =
  | "ly_thuyet"
  | "video"
  | "bai_tap_mau"
  | "luyen_tap_sach"
  | "luyen_tap_de"
  | "kiem_tra";

export interface Chapter {
  id: number;
  title: string;
  sort_order: number;
  classIds: number[]; // rỗng = toàn trường
}

export interface Lesson {
  id: number;
  chapter_id: number;
  title: string;
  sort_order: number;
  published: boolean;
  itemCount: number;
}

export interface LessonItem {
  id: number;
  lesson_id: number;
  kind: LessonItemKind;
  title: string;
  subtitle: string;
  body_html: string;
  video_url: string;
  pdf_url: string;
  exam_id: number | null;
  sort_order: number;
}

export const SECTION_ORDER: LessonItemKind[] = [
  "ly_thuyet",
  "video",
  "bai_tap_mau",
  "luyen_tap_sach",
  "luyen_tap_de",
  "kiem_tra",
];

export interface SectionMeta {
  label: string;
  icon: string;
  color: string; // màu chủ đạo của mục (tiêu đề, icon)
  action: string; // nhãn nút hành động
}

export const SECTION_META: Record<LessonItemKind, SectionMeta> = {
  ly_thuyet: { label: "Lý thuyết", icon: "📖", color: "#3B82F6", action: "Xem" },
  video: { label: "Video/PDF bổ trợ", icon: "🎬", color: "#38BDF8", action: "Xem video" },
  bai_tap_mau: { label: "Bài tập mẫu", icon: "✏️", color: "#8B5CF6", action: "Làm bài" },
  luyen_tap_sach: { label: "Luyện tập sách", icon: "📄", color: "#10B981", action: "Làm bài" },
  luyen_tap_de: { label: "Luyện tập (đề)", icon: "📚", color: "#F59E0B", action: "Làm bài" },
  kiem_tra: { label: "Kiểm tra cuối bài", icon: "📝", color: "#F43F5E", action: "Làm bài" },
};

// Nhãn viết tắt số câu theo dạng: 12 TN · 2 ĐS · 4 TLN
export const TYPE_SHORT: Record<string, string> = {
  multiple_choice: "TN",
  true_false: "ĐS",
  short_answer: "TLN",
};

export type TypeCounts = Partial<Record<string, number>>;

export function formatTypeCounts(counts: TypeCounts | null | undefined): string {
  if (!counts) return "";
  return Object.entries(TYPE_SHORT)
    .filter(([type]) => (counts[type] ?? 0) > 0)
    .map(([type, short]) => `${counts[type]} ${short}`)
    .join(" · ");
}

/** Đổi link YouTube bất kỳ (watch/youtu.be/shorts) thành id video. */
export function youTubeId(url: string): string | null {
  const m = url.match(
    /(?:youtube\.com\/(?:watch\?v=|shorts\/|embed\/)|youtu\.be\/)([\w-]{11})/,
  );
  return m ? m[1] : null;
}

export function youTubeEmbed(url: string): string | null {
  const id = youTubeId(url);
  return id ? `https://www.youtube.com/embed/${id}` : null;
}

export function youTubeThumb(url: string): string | null {
  const id = youTubeId(url);
  return id ? `https://i.ytimg.com/vi/${id}/hqdefault.jpg` : null;
}
