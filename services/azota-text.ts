/**
 * Thao tác trên văn bản đề kiểu Azota (nguồn sự thật của trang Đăng đề):
 * tách khối từng câu, đặt/đổi đáp án ngay trong văn bản (dấu `*` hoặc dòng "Đáp án:")
 * để phần xem trước và phần bảng đáp án luôn khớp với thứ người dùng đang gõ.
 *
 * Mốc câu và cách đọc đáp án phải trùng với `docx-exam-parser` (QUESTION_LINE, applyStarAnswers).
 */

const QUESTION_LINE = /^\s*(?:\*\s*)?C[âa]u\s*\d+\s*[.:)]/i;
const PART_LINE = /^\s*PH[ẦA]N\b/i;
const ANSWER_LINE = /^(\s*Đ[áa]p\s*[áa]n\s*[:.]?\s*)(.*)$/i;
const LETTERS = ["A", "B", "C", "D"] as const;

export interface QuestionBlock {
  /** dòng đầu (mốc "Câu n.") và dòng kết (không gồm) trong mảng dòng */
  start: number;
  end: number;
}

/** Tách văn bản thành các khối câu theo mốc "Câu n." (bỏ qua dòng PHẦN). */
export function questionBlocks(lines: string[]): QuestionBlock[] {
  const blocks: QuestionBlock[] = [];
  lines.forEach((line, i) => {
    if (QUESTION_LINE.test(line)) blocks.push({ start: i, end: lines.length });
  });
  blocks.forEach((b, idx) => {
    let end = idx + 1 < blocks.length ? blocks[idx + 1].start : lines.length;
    for (let i = b.start + 1; i < end; i += 1) {
      if (PART_LINE.test(lines[i])) {
        end = i;
        break;
      }
    }
    b.end = end;
  });
  return blocks;
}

/** Vị trí ký tự sau mốc "Câu n." trên dòng đầu — để không nhầm chữ "A." trong đề bài. */
function markerEnd(line: string): number {
  const m = line.match(QUESTION_LINE);
  return m ? m[0].length : 0;
}

function findAnswerLine(lines: string[], b: QuestionBlock): number {
  for (let i = b.start; i < b.end; i += 1) if (ANSWER_LINE.test(lines[i])) return i;
  return -1;
}

/** Đặt đáp án đúng cho câu trắc nghiệm thứ `index` (đếm từ 0) là chữ `letter` (A–D). */
export function setChoiceAnswer(text: string, index: number, letter: string): string {
  const L = letter.toUpperCase();
  if (!LETTERS.includes(L as (typeof LETTERS)[number])) return text;
  const lines = text.split("\n");
  const b = questionBlocks(lines)[index];
  if (!b) return text;

  // Đề dùng dòng "Đáp án: B" thì sửa dòng đó.
  const ansAt = findAnswerLine(lines, b);
  if (ansAt >= 0 && /^[A-D]\b/i.test(lines[ansAt].replace(ANSWER_LINE, "$2").trim())) {
    lines[ansAt] = lines[ansAt].replace(ANSWER_LINE, (_m, head: string) => `${head}${L}`);
    return lines.join("\n");
  }

  // Gỡ mọi dấu * cũ trước A–D trong khối, rồi đặt * trước phương án chọn.
  for (let i = b.start; i < b.end; i += 1)
    lines[i] = lines[i].replace(/(^|[\s\t(])\*\s*([A-D])([.)])/g, "$1$2$3");
  const target = new RegExp(`(^|[\\s\\t(])(${L})([.)])`);
  for (let i = b.start; i < b.end; i += 1) {
    const offset = i === b.start ? markerEnd(lines[i]) : 0;
    const head = lines[i].slice(0, offset);
    const tail = lines[i].slice(offset);
    if (target.test(tail)) {
      lines[i] = head + tail.replace(target, "$1*$2$3");
      return lines.join("\n");
    }
  }
  // Không thấy phương án nào → ghi dòng Đáp án ở cuối khối.
  return insertAnswerLine(lines, b, L);
}

/** Bật/tắt Đúng cho ý `letter` (a–d) của câu đúng–sai thứ `index`. */
export function toggleStatementAnswer(text: string, index: number, letter: string): string {
  const l = letter.toLowerCase();
  const lines = text.split("\n");
  const b = questionBlocks(lines)[index];
  if (!b) return text;

  const ansAt = findAnswerLine(lines, b);
  if (ansAt >= 0 && /[a-d]\)\s*[ĐS]/i.test(lines[ansAt])) {
    lines[ansAt] = lines[ansAt].replace(
      new RegExp(`(${l}\\)\\s*)([ĐS])`, "i"),
      (_m, head: string, v: string) => `${head}${v.toUpperCase() === "Đ" ? "S" : "Đ"}`,
    );
    return lines.join("\n");
  }

  const starred = new RegExp(`(^|[\\s\\t(])\\*\\s*(${l})([.)])`);
  const plain = new RegExp(`(^|[\\s\\t(])(${l})([.)])`);
  for (let i = b.start; i < b.end; i += 1) {
    const offset = i === b.start ? markerEnd(lines[i]) : 0;
    const head = lines[i].slice(0, offset);
    const tail = lines[i].slice(offset);
    if (starred.test(tail)) {
      lines[i] = head + tail.replace(starred, "$1$2$3");
      return lines.join("\n");
    }
    if (plain.test(tail)) {
      lines[i] = head + tail.replace(plain, "$1*$2$3");
      return lines.join("\n");
    }
  }
  return text;
}

/** Ghi đáp án cho câu trả lời ngắn thứ `index`. */
export function setShortAnswer(text: string, index: number, value: string): string {
  const lines = text.split("\n");
  const b = questionBlocks(lines)[index];
  if (!b) return text;
  const v = value.trim();
  const ansAt = findAnswerLine(lines, b);
  if (ansAt >= 0) {
    lines[ansAt] = lines[ansAt].replace(ANSWER_LINE, (_m, head: string) => `${head}${v}`);
    return lines.join("\n");
  }
  return insertAnswerLine(lines, b, v);
}

/** Dòng nhãn phân loại — cùng mẫu với `extractTags` trong exam-latex-parser. */
const TAG_LINES = {
  topic: /^\s*(?:Chủ\s*đề|YCCĐ|Yêu\s*cầu\s*cần\s*đạt|Năng\s*lực)\s*[:：]/i,
  form: /^\s*(?:Dạng|Loại)\s*[:：]/i,
} as const;
const TAG_LABEL = { topic: "Chủ đề", form: "Dạng" } as const;
export type TagField = keyof typeof TAG_LINES;

/**
 * Ghi nhãn "Chủ đề: …" / "Dạng: …" cho câu thứ `index` thẳng vào văn bản:
 * có dòng sẵn thì thay giá trị, chưa có thì thêm vào cuối khối câu; giá trị rỗng = bỏ dòng.
 */
export function setQuestionTag(text: string, index: number, field: TagField, value: string): string {
  const lines = text.split("\n");
  const b = questionBlocks(lines)[index];
  if (!b) return text;
  const v = value.trim().replace(/\s+/g, " ");
  const re = TAG_LINES[field];
  let at = -1;
  for (let i = b.start + 1; i < b.end; i += 1)
    if (re.test(lines[i])) {
      at = i;
      break;
    }
  if (at >= 0) {
    if (v) lines[at] = `${TAG_LABEL[field]}: ${v}`;
    else lines.splice(at, 1);
    return lines.join("\n");
  }
  if (!v) return text;
  let end = b.end;
  while (end > b.start + 1 && lines[end - 1].trim() === "") end -= 1;
  lines.splice(end, 0, `${TAG_LABEL[field]}: ${v}`);
  return lines.join("\n");
}

/** Ghi cùng một nhãn cho nhiều câu (vd. cả đề là bài tập). */
export function setQuestionTagMany(text: string, indexes: number[], field: TagField, value: string): string {
  return indexes.reduce((t, i) => setQuestionTag(t, i, field, value), text);
}

function insertAnswerLine(lines: string[], b: QuestionBlock, value: string): string {
  // Chèn trước "Lời giải" nếu có, còn không thì đặt sau dòng có nội dung cuối cùng của khối.
  let at = b.end;
  for (let i = b.start + 1; i < b.end; i += 1) {
    if (/^\s*(L[ờo]i\s*gi[ảa]i|Gi[ảa]i|H[ướu][ớo]ng\s*d[ẫa]n)\b/i.test(lines[i])) {
      at = i;
      break;
    }
  }
  if (at === b.end) while (at > b.start + 1 && lines[at - 1].trim() === "") at -= 1;
  lines.splice(at, 0, `Đáp án: ${value}`);
  return lines.join("\n");
}

export const SAMPLE_TEXT = `ĐỀ KIỂM TRA 15 PHÚT – ĐỘNG HỌC
Thời gian làm bài: 15 phút

PHẦN I. Câu trắc nghiệm nhiều phương án lựa chọn
Câu 1. Tốc độ trung bình của một vật được tính bằng
A. quãng đường nhân thời gian.
*B. quãng đường chia thời gian.
C. thời gian chia quãng đường.
D. quãng đường cộng thời gian.
Lời giải: $v_{tb} = \\dfrac{s}{t}$.
Chủ đề: Nêu được định nghĩa tốc độ trung bình
Dạng: lý thuyết

Câu 2. Một xe đi được 120 m trong 10 s. Tốc độ trung bình của xe là
A. 6 m/s.   *B. 12 m/s.   C. 24 m/s.   D. 1200 m/s.
Lời giải: $v = 120/10 = 12$ m/s.
Chủ đề: Vận dụng công thức tốc độ trung bình
Dạng: bài tập

PHẦN II. Câu trắc nghiệm đúng sai
Câu 3. Một vật chuyển động thẳng đều với tốc độ 5 m/s.
*a) Quãng đường đi được trong 4 s là 20 m.
b) Vận tốc của vật thay đổi theo thời gian.
*c) Gia tốc của vật bằng 0.
d) Đồ thị (s–t) là đường cong.
Lời giải: Chuyển động thẳng đều có $a = 0$, $s = vt$.

PHẦN III. Câu trắc nghiệm trả lời ngắn
Câu 4. Một vật rơi tự do từ độ cao 20 m, lấy $g = 10$ m/s². Thời gian rơi là bao nhiêu giây?
Đáp án: 2
Lời giải: $t = \\sqrt{2h/g} = 2$ s.
`;
