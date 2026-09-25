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

/** Bọc mỗi đoạn từ một <h3> tới trước <h3> kế tiếp trong <div id="…">, để có thể scrollIntoView. */
export function wrapTheorySections(html: string, itemId: number | string): { html: string; sections: TheorySection[] } {
  const matches = [...html.matchAll(H3_RE)];
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
