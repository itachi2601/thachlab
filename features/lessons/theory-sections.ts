// "Kiểm tra hiểu bài": chia body_html của mục lý thuyết thành từng khối theo mốc <h3>
// (I., II., III…; lùi về mốc in đậm đánh số rồi <h2> nếu bài không có <h3>) sẵn có trong nội dung, gắn id để quiz "Kiểm tra nhanh" (ExamRunner,
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

// Bậc dự phòng thứ ba: một số bài chỉ dùng <h2> ("I. Nam châm", "II. …") làm mốc. Bỏ qua
// <h2> chỉ ghi "LÝ THUYẾT"/"LÍ THUYẾT" — đó là tiêu đề chung cả mục, không phải một đoạn.
const H2_RE = /<h2\b[^>]*>(.*?)<\/h2>/gi;
const H2_GENERIC_RE = /^l[ýí]thuy[ếe]t$/i;

function h2Matches(html: string): RegExpMatchArray[] {
  return [...html.matchAll(H2_RE)].filter((m) => {
    const text = m[1].replace(/<[^>]+>/g, "").replace(/&nbsp;/gi, " ").replace(/\s+/g, "");
    return text !== "" && !H2_GENERIC_RE.test(text);
  });
}

function headingMatches(html: string, mode: TheorySplitMode): RegExpMatchArray[] {
  const h3 = [...html.matchAll(H3_RE)];
  const bold = [...html.matchAll(BOLD_NUMBERED_RE)];
  const h2 = h2Matches(html);

  // Trình chiếu: mốc LỚN trước. Trang chiếu cần mỗi trang là một mục I., II., III.; nếu chia
  // theo mốc nhỏ, mọi mục lớn đứng TRƯỚC mốc nhỏ đầu tiên bị dồn hết vào "phần mở bài" và nằm
  // chung một trang (đã thấy thật ở bài "Khái niệm từ trường": I, II, III + hình nằm chung một
  // trang, còn 5 trang sau chỉ là các mục con "1. Định nghĩa", "2. Hướng…" mất ngữ cảnh).
  if (mode === "chieu") {
    if (h2.length > 0) return h2;
    if (h3.length > 0) return h3;
    return bold;
  }

  if (h3.length > 0) return h3;
  if (bold.length > 0) return bold;
  return h2;
}

/** Cách chọn mốc chia đoạn lý thuyết — xem `headingMatches`. */
export type TheorySplitMode = "doc" | "chieu";

/** Một đoạn lý thuyết đã tách rời (không bọc <div>) — dùng chung cho trang đọc và chế độ trình chiếu. */
export interface TheorySectionPart extends TheorySection {
  /** Cả đoạn, GỒM thẻ tiêu đề ở đầu — đúng thứ tự trong body_html gốc. */
  html: string;
  /** Đoạn đã bỏ thẻ tiêu đề ở đầu, để chế độ trình chiếu render tiêu đề bằng kiểu chữ riêng
   *  (mốc tiêu đề có thể là <h3>, <h2> hoặc <p><strong> — trình chiếu cần một kiểu chữ duy nhất). */
  bodyHtml: string;
}

/**
 * Tách body_html của một mục lý thuyết thành từng đoạn theo mốc tiêu đề có sẵn trong nội dung,
 * KHÔNG bọc thêm gì — `wrapTheorySections` (trang đọc) và chế độ trình chiếu (LessonPresenter)
 * cùng dùng hàm này nên hai nơi không bao giờ chia đoạn lệch nhau về vị trí cắt.
 *
 * `mode` chỉ đổi THỨ TỰ ƯU TIÊN mốc chia (trang đọc ưu tiên mốc nhỏ, trình chiếu ưu tiên mốc
 * lớn — xem `headingMatches`), không đổi nội dung.
 *
 * `introHtml` là phần mở bài nằm trước mốc tiêu đề đầu tiên (thường là rỗng).
 */
// Câu "Khoảng 17 phút · 6 mục · 8 câu tự kiểm tra" do người soạn chèn trong mục tiêu.
// Thanh lý thuyết đã hiện một ước lượng duy nhất (~N phút) — bỏ câu này lúc hiển thị
// để không còn hai con số thời lượng. Không khớp "Khoảng cách / Khoảng chênh".
const AUTHORED_DURATION_RE =
  /(?:\s*[—–-]\s*|\s+)[Kk]hoảng\s+\d+\s+phút\s*·\s*(?:\d+\s+mục\s*·\s*)?\d+\s+câu tự kiểm tra\.?/g;

export function stripAuthoredDuration(html: string): string {
  return html.replace(AUTHORED_DURATION_RE, "");
}

export function splitTheorySections(
  html: string,
  itemId: number | string,
  mode: TheorySplitMode = "doc",
): { introHtml: string; sections: TheorySectionPart[] } {
  html = stripAuthoredDuration(html);
  const matches = headingMatches(html, mode);
  if (matches.length === 0) return { introHtml: html, sections: [] };

  const sections: TheorySectionPart[] = [];
  let introHtml = "";

  matches.forEach((m, i) => {
    const start = m.index ?? 0;
    if (i === 0 && start > 0) introHtml = html.slice(0, start); // mở bài trước mốc đầu tiên, không bọc

    const end = i + 1 < matches.length ? (matches[i + 1].index ?? html.length) : html.length;
    const slice = html.slice(start, end);
    sections.push({
      id: `theory-sec-${itemId}-${i}`,
      heading: m[1].replace(/<[^>]+>/g, "").trim(),
      html: slice,
      // m[0] là đúng thẻ tiêu đề nằm ở đầu `slice` (mọi regex mốc đều bắt đầu bằng thẻ mở),
      // nên cắt bỏ đúng độ dài chuỗi khớp là ra phần thân mà không đụng nội dung.
      bodyHtml: slice.slice(m[0].length).replace(/^\s+/, ""),
    });
  });

  return { introHtml, sections };
}

/** Bọc mỗi đoạn từ một mốc tiêu đề tới trước mốc kế tiếp trong <div id="…">, để có thể scrollIntoView. */
export function wrapTheorySections(html: string, itemId: number | string): { html: string; sections: TheorySection[] } {
  const { introHtml, sections } = splitTheorySections(html, itemId);
  if (sections.length === 0) return { html, sections: [] };

  const out =
    introHtml +
    sections.map((section) => `<div class="theory-section" id="${section.id}">${section.html}</div>`).join("");
  return { html: out, sections: sections.map(({ id, heading }) => ({ id, heading })) };
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

export interface TheoryEstimate {
  /** Số phút đã làm tròn lên (tối thiểu 1). */
  minutes: number;
  /** Số câu tự kiểm tra (quiz) trong bài. */
  quizzes: number;
}

// 140 từ/phút: tốc độ đọc chữ Việt trên điện thoại (docs/PHUONG-PHAP-NOI-DUNG-LY-THUYET.md mục 2).
// Phần trong <details> (lời giải, phần mở rộng) không tính vì không hiện ngay.
const WORDS_PER_MIN = 140;
const MIN_PER_INTERACTION = 1;

/** Ước tính thời gian học một mục lý thuyết: chữ hiện ngay + ~1 phút cho mỗi quiz / thí nghiệm / câu dự đoán. */
export function estimateTheoryTime(html: string): TheoryEstimate {
  const quizzes = (html.match(/class="[^"]*\btl-quiz\b/g) ?? []).length;
  const interactions =
    quizzes + (html.match(/class="[^"]*\btl-box--(?:exp|think)\b/g) ?? []).length;
  const visible = html
    .replace(/<details\b[\s\S]*?<\/details>/gi, " ")
    .replace(/<(script|style|svg)\b[\s\S]*?<\/\1>/gi, " ")
    .replace(/<[^>]+>/g, " ")
    .replace(/&nbsp;/gi, " ");
  const words = visible.split(/\s+/).filter(Boolean).length;
  const minutes = Math.max(1, Math.ceil(words / WORDS_PER_MIN + interactions * MIN_PER_INTERACTION));
  return { minutes, quizzes };
}
