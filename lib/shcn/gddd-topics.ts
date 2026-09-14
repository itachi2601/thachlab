// Chủ đề GDĐĐ & PTNN dùng cho phần "Tự đọc thêm" của thẻ sinh hoạt tuần.
//
// Mỗi buổi SHCN chỉ dạy 1–2 trọng tâm của một chủ đề; phần còn lại của chủ đề để sinh viên tự
// đọc. Danh sách mục con vì vậy là dữ liệu tĩnh, không lưu lặp trong từng dòng
// homeroom_weekly_sessions.
//
// QUAN TRỌNG: chỉ điền vào đây những mục con đọc được từ tài liệu gốc. Chủ đề nào chưa có đủ
// danh sách thì để `complete: false` — giao diện sẽ không hiện dòng "Tự đọc thêm" thay vì bịa
// ra các mục sinh viên không hề có trong tài liệu. Khi bổ sung đủ mục con của một chủ đề, thêm
// vào `items` rồi đổi `complete: true`.

export interface GdddTopic {
  /** Số chủ đề trong chương trình (1–12). */
  id: number;
  /** Tên hiển thị, khớp cách ghi trong biên bản: "Chủ đề 2: Kỹ năng sống". */
  title: string;
  /** Các mục con (trọng tâm) của chủ đề. */
  items: string[];
  /** true khi `items` đã đủ toàn bộ mục con của chủ đề — điều kiện để tính "phần còn lại". */
  complete: boolean;
}

/**
 * Link thư mục Drive chung cho toàn bộ 12 chủ đề. Đổi bằng NEXT_PUBLIC_GDDD_DOCS_URL trong
 * .env.local nếu thầy/cô chuyển thư mục. Khi nào mỗi chủ đề có link riêng thì chuyển sang bảng
 * map chu_de_id → url, chưa cần lúc này.
 */
export const GDDD_DOCS_URL =
  process.env.NEXT_PUBLIC_GDDD_DOCS_URL ??
  "https://drive.google.com/drive/u/2/folders/1Tkf3m_yF-ztZADp3T_wcthabV0oc-PaM";

/**
 * Mới có chủ đề 2, và mới 2/8 mục con của nó (lấy từ biên bản tuần 03). 11 chủ đề còn lại và 6
 * mục con còn lại của chủ đề 2 bổ sung dần khi có tài liệu — xem docs/SHCN-MODULE.md.
 */
export const GDDD_TOPICS: GdddTopic[] = [
  {
    id: 2,
    title: "Chủ đề 2: Kỹ năng sống",
    items: ["An toàn giao thông", "Những điều cần cảnh giác và số điện thoại khẩn cấp"],
    complete: false,
  },
];

/** Bỏ dấu + hạ chữ thường để so khớp tên trọng tâm không phụ thuộc cách gõ. */
function normalize(value: string) {
  return value.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().replace(/\s+/g, " ").trim();
}

/** Tìm chủ đề theo nhãn tự do ghi trong biên bản, vd "Chủ đề 2: Kỹ năng sống" → chủ đề id 2. */
export function findGdddTopic(label: string): GdddTopic | null {
  if (!label.trim()) return null;
  const number = Number(label.match(/ch[uủ]\s*đ[eề]\s*(\d{1,2})/i)?.[1] ?? label.match(/^\s*(\d{1,2})\b/)?.[1]);
  if (Number.isFinite(number)) {
    const byNumber = GDDD_TOPICS.find((topic) => topic.id === number);
    if (byNumber) return byNumber;
  }
  const key = normalize(label);
  return GDDD_TOPICS.find((topic) => normalize(topic.title) === key || key.includes(normalize(topic.title))) ?? null;
}

/**
 * Các mục con của chủ đề chưa dạy trong buổi này — phần "Tự đọc thêm".
 * Rỗng khi chưa biết đủ mục con của chủ đề (tránh gợi ý thiếu/sai cho sinh viên).
 */
export function selfStudyItems(topicLabel: string, taught: string[]): string[] {
  const topic = findGdddTopic(topicLabel);
  if (!topic || !topic.complete) return [];
  const done = new Set(taught.map(normalize));
  return topic.items.filter((item) => !done.has(normalize(item)));
}
