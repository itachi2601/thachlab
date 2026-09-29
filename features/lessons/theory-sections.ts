// "Kiểm tra hiểu bài": chia body_html của mục lý thuyết thành từng khối theo mốc <h3>
// (I., II., III…) sẵn có trong nội dung, gắn id để quiz "Kiểm tra nhanh" (ExamRunner,
// xem "Ôn ngay" trong components/exams/ExamRunner.tsx) có thể cuộn + tô màu đúng đoạn
// liên quan khi học sinh trả lời sai, thay vì chỉ nhảy tới đầu cả mục lý thuyết. Biến
// đổi chuỗi HTML thô — cùng cách làm với components/exams/ContentHtml.tsx — không đụng
// DOM, không sửa dữ liệu gốc.

export interface TheorySection {
  id: string;
  heading: string; // text thô của <h3>, dùng làm nhãn liên kết "Xem lại: <heading>"
}

const H3_RE = /<h3\b[^>]*>(.*?)<\/h3>/gi;
// Một số bài (đặc biệt lớp 12) không dùng <h3> mà đánh số mục lớn bằng <strong> riêng một
// <p> ("1. Mô hình động học…", "2. Cấu trúc…"). Chỉ khớp <p> mà TOÀN BỘ nội dung là một
// <strong> bắt đầu bằng số + dấu chấm, để không nhầm với nhãn phụ giữa đoạn văn kiểu
// "a. …", "Chú ý:", "- Giải thích …:" (không có số ở đầu, hoặc không đứng riêng 1 <p>).
const BOLD_NUMBERED_RE = /<p\b[^>]*>\s*<strong\b[^>]*>(\d+\.\s*[^<]*)<\/strong>\s*<\/p>/gi;

function headingMatches(html: string): RegExpMatchArray[] {
  const h3 = [...html.matchAll(H3_RE)];
  if (h3.length > 0) return h3;
  return [...html.matchAll(BOLD_NUMBERED_RE)];
}

/** Bọc mỗi đoạn từ một mốc tiêu đề tới trước mốc kế tiếp trong <div id="…">, để có thể scrollIntoView. */
export function wrapTheorySections(html: string, itemId: number | string): { html: string; sections: TheorySection[] } {
  const matches = headingMatches(html);
  if (matches.length === 0) return { html, sections: [] };

  const sections: TheorySection[] = [];
  let out = "";
  let cursor = 0;

  matches.forEach((m, i) => {
    const start = m.index ?? 0;
    if (i === 0 && start > 0) out += html.slice(0, start); // mở bài trước <h3> đầu tiên, không bọc

    const end = i + 1 < matches.length ? (matches[i + 1].index ?? html.length) : html.length;
    const id = `theory-sec-${itemId}-${i}`;
    const heading = m[1].replace(/<[^>]+>/g, "").trim();
    sections.push({ id, heading });
    out += `<div class="theory-section" id="${id}">${html.slice(start, end)}</div>`;
    cursor = end;
  });

  out += html.slice(cursor);
  return { html: out, sections };
}

/** "#theory-sec-278-2" -> 278 — đọc lesson_items.id đích từ hash khi quay lại trang bài học
 *  (link "Ôn ngay" trong ExamRunner), để biết cần tự mở mục lý thuyết nào (mặc định các mục
 *  từ thứ hai trở đi đang thu gọn) trước khi cuộn + tô màu tới đúng đoạn. */
export function theorySectionItemId(hash: string): number | null {
  const m = /^#?theory-sec-(\d+)-\d+$/.exec(hash);
  return m ? Number(m[1]) : null;
}

// ---------- Mang theo (TẤT CẢ) câu vừa làm sai khi quay lại xem lý thuyết ----------
// Chỉ tô vàng đúng đoạn thì học sinh cuộn tới nơi rồi... quên mất mình đang tìm hiểu vì sai
// câu nào — và nếu sai nhiều câu ở nhiều đoạn khác nhau, bấm "Ôn ngay" ở 1 câu thì các câu sai
// khác sẽ mất dấu nếu chỉ mang theo đúng câu vừa bấm. Mang CẢ BỘ đề bài + đáp án đã chọn/đáp án
// đúng của mọi câu sai (cùng thuộc 1 lượt làm) qua sessionStorage (không qua URL vì HTML câu hỏi
// có thể dài, không qua React context vì hai trang không cùng cây component) để trang bài học
// hiện lại thành thẻ dán cố định liệt kê đủ, tô vàng đủ MỌI đoạn liên quan — đọc xong thì xoá
// luôn, tránh hiện lại bộ cũ nếu học sinh quay lại trang này sau, không qua "Ôn ngay" nữa.
const REVIEW_CONTEXT_KEY = "thachlab:theory-review-context";

export interface TheoryReviewContext {
  itemId: number;
  sectionIndex: number;
  questionIndex: number; // 1-based, để hiện "Câu N"
  questionHtml: string;
  pickedHtml: string | null; // null nếu bỏ qua câu, không chọn gì
  correctHtml: string | null; // null nếu không phải trắc nghiệm 4 đáp án (chưa hỗ trợ tóm tắt các dạng câu khác)
}

export function saveTheoryReviewContext(contexts: TheoryReviewContext[]): void {
  try {
    sessionStorage.setItem(REVIEW_CONTEXT_KEY, JSON.stringify(contexts));
  } catch {
    // Riêng tư trình duyệt chặn sessionStorage — bỏ qua, "Ôn ngay" vẫn cuộn+tô đúng đoạn như thường.
  }
}

/** Đọc rồi xoá luôn (dùng 1 lần) — gọi khi trang bài học vừa tải xong. */
export function consumeTheoryReviewContext(): TheoryReviewContext[] | null {
  try {
    const raw = sessionStorage.getItem(REVIEW_CONTEXT_KEY);
    if (!raw) return null;
    sessionStorage.removeItem(REVIEW_CONTEXT_KEY);
    const parsed = JSON.parse(raw) as TheoryReviewContext[];
    return Array.isArray(parsed) && parsed.length > 0 ? parsed : null;
  } catch {
    return null;
  }
}
