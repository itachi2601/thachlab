/** Dữ liệu một thẻ "Vật lý quanh ta" (trang chủ + /blog). Chỉ chứa kiểu, import được từ cả server lẫn client. */

export interface PostQuiz {
  question: string;
  /** Câu trả lời ngắn (≤ ~60 ký tự) — thẻ nhỏ, đọc trên điện thoại. Nhãn A. B. C. do giao diện gắn (E1). */
  options: string[];
  /** Chỉ số (0 = A) của đáp án đúng. */
  answer: number;
  /** Một câu giải thích hiện sau khi chọn. */
  why: string;
}

/** Ghi công ảnh — thiếu một trường bắt buộc thì KHÔNG hiện ảnh (xem docs/ANH-VAT-LY-QUANH-TA.md). */
export interface PhotoCredit {
  author: string;
  license: string;
  sourceUrl: string;
  licenseUrl?: string;
}

export interface PhysicsCardData {
  slug: string;
  title: string;
  href: string;
  /** Nhãn gây tò mò (vd "Đố vui 30s"). */
  badge?: string;
  /** Một câu nghịch lý dưới tiêu đề. */
  hook?: string;
  quiz?: PostQuiz;
  /** Ảnh thẻ 16:9 đã có trong public/ và có đủ ghi công; null → hiện khung giữ chỗ. */
  photo: string | null;
  photoAlt?: string;
  photoCredit?: PhotoCredit;
  readingMinutes: number;
}
