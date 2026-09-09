// Cấu trúc học liệu: Chương → Bài học → Mục (5 loại, thứ tự cố định §1–§5)

export type LessonItemKind =
  | "ly_thuyet"
  | "video"
  | "bai_tap_mau"
  | "luyen_tap"
  | "kiem_tra";

export interface Chapter {
  id: number;
  title: string;
  sort_order: number;
  classIds: number[]; // rỗng = toàn trường
  subjectCode: string;
}

// Bài học thường, hoặc một bài kiểm tra định kỳ đặt cuối chương tương ứng chương trình.
export type LessonKind = "bai_hoc" | "kiem_tra_giua_ki" | "kiem_tra_cuoi_ki";

export interface Lesson {
  id: number;
  chapter_id: number;
  title: string;
  sort_order: number;
  published: boolean;
  lesson_kind: LessonKind;
  itemCount: number;
}

export function isPeriodicExam(kind: LessonKind): boolean {
  return kind === "kiem_tra_giua_ki" || kind === "kiem_tra_cuoi_ki";
}

export interface LessonKindMeta {
  label: string; // nhãn đầy đủ, cũng là tên bài mặc định
  badge: string; // nhãn ngắn hiển thị dạng chip ("" = không hiện)
  icon: string;
  color: string;
}

export const LESSON_KIND_META: Record<LessonKind, LessonKindMeta> = {
  bai_hoc: { label: "Bài học", badge: "", icon: "📖", color: "#3B82F6" },
  kiem_tra_giua_ki: {
    label: "Kiểm tra giữa học kì",
    badge: "GIỮA HỌC KÌ",
    icon: "📝",
    color: "#F59E0B",
  },
  kiem_tra_cuoi_ki: {
    label: "Kiểm tra cuối học kì",
    badge: "CUỐI HỌC KÌ",
    icon: "🏁",
    color: "#F43F5E",
  },
};

export function normalizeLessonKind(kind: unknown): LessonKind {
  return kind === "kiem_tra_giua_ki" || kind === "kiem_tra_cuoi_ki"
    ? kind
    : "bai_hoc";
}

// Một "dạng bài" trong mục Các dạng bài tập: đề + lời giải soạn tự do (LaTeX/HTML)
export interface LessonWorkedQuestion {
  label: string;
  body_html: string;
}

export interface LessonItem {
  id: number;
  lesson_id: number;
  kind: LessonItemKind;
  title: string;
  subtitle: string;
  body_html: string; // chỉ dùng cho ly_thuyet
  video_url: string;
  pdf_url: string;
  questions: LessonWorkedQuestion[]; // bai_tap_mau
  exam_ids: number[]; // luyen_tap / kiem_tra
  sort_order: number;
}

export const SECTION_ORDER: LessonItemKind[] = [
  "ly_thuyet",
  "video",
  "bai_tap_mau",
  "luyen_tap",
  "kiem_tra",
];

export interface SectionMeta {
  label: string;
  icon: string;
  color: string; // màu chủ đạo của mục (tiêu đề, icon)
  action: string; // nhãn nút hành động
}

export const SECTION_META: Record<LessonItemKind, SectionMeta> = {
  ly_thuyet: { label: "Lý thuyết trọng tâm", icon: "📖", color: "#3B82F6", action: "Xem" },
  video: { label: "Video bài giảng", icon: "🎬", color: "#38BDF8", action: "Xem video" },
  bai_tap_mau: { label: "Các dạng bài tập", icon: "✏️", color: "#8B5CF6", action: "Làm bài" },
  luyen_tap: { label: "Luyện tập", icon: "📚", color: "#F59E0B", action: "Làm bài" },
  kiem_tra: { label: "Kiểm tra", icon: "📝", color: "#F43F5E", action: "Làm bài" },
};

/** Chuẩn hóa dữ liệu của cấu trúc 6 mục cũ trong lúc migration DB chưa được chạy. */
export function normalizeLessonItemKind(kind: unknown): LessonItemKind {
  if (kind === "luyen_tap_sach" || kind === "luyen_tap_de") return "luyen_tap";
  return SECTION_ORDER.includes(kind as LessonItemKind)
    ? (kind as LessonItemKind)
    : "ly_thuyet";
}

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
