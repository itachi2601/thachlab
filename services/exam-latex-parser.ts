/**
 * Parser đề LaTeX → mảng ExamQuestion (multiple_choice / true_false / short_answer).
 *
 * Định dạng chuẩn (khớp skill de-vat-ly-thpt / azota):
 *
 *   \subsection*{PHẦN I. Câu trắc nghiệm nhiều phương án lựa chọn}
 *   \textbf{Câu 1.} <đề>
 *   A. ...   B. ...   C. ...   D. ...
 *   \textbf{Đáp án:} B
 *   \textbf{Lời giải:} ...
 *
 *   \subsection*{PHẦN II. Câu trắc nghiệm đúng sai}
 *   \textbf{Câu 1.} <đề>
 *   a) [0, NB] ...   b) ...   c) ...   d) ...
 *   \textbf{Đáp án:} a) Đ  b) Đ  c) S  d) Đ
 *
 *   \subsection*{PHẦN III. Câu trắc nghiệm trả lời ngắn}
 *   \textbf{Câu 1.} <đề> (ghi số)
 *   \textbf{Đáp án:} 2
 *
 * Vẫn nhận định dạng cũ `\question{Loại: multiple_choice} ... \answer{A} \explanation{...}`.
 */

import type {
  ExamQuestion,
  MultipleChoiceQuestion,
  ShortAnswerQuestion,
  TrueFalseQuestion,
} from "@/features/exams/types";

export interface ExamParseResult {
  title: string;
  questions: ExamQuestion[];
  warnings: string[];
}

type QuestionType = "multiple_choice" | "true_false" | "short_answer";

/** Chuyển LaTeX inline nhẹ → HTML, giữ nguyên `$...$`. */
function inlineLatex(input: string): string {
  let s = input.trim();
  s = s.replace(/\\textbf\{([^{}]*)\}/g, "<strong>$1</strong>");
  s = s.replace(/\\textit\{([^{}]*)\}/g, "<em>$1</em>");
  s = s.replace(/\\emph\{([^{}]*)\}/g, "<em>$1</em>");
  s = s.replace(/\\%/g, "%").replace(/\\&/g, "&").replace(/\\_/g, "_");
  s = s.replace(/\\\\\s*/g, "<br>");
  s = s.replace(/[ \t]*\n[ \t]*/g, " ").trim();
  return s;
}

const PART_TYPES: { re: RegExp; type: QuestionType }[] = [
  { re: /\bI{3}\b|\b3\b|ng[ắăa]n/i, type: "short_answer" },
  { re: /\bII\b|\b2\b|sai/i, type: "true_false" },
  { re: /\bI\b|\b1\b|ph[ươ]+ng\s*[áa]n/i, type: "multiple_choice" },
];

function detectPartType(header: string): QuestionType | null {
  for (const { re, type } of PART_TYPES) if (re.test(header)) return type;
  return null;
}

const FIELD_LINE_RE =
  /^\\?(?:textbf\{)?\s*(?:Đáp\s*án|Đáp\s*số|Giải|Lời\s*giải|Hướng\s*dẫn|answer|explanation)/i;

/** Phần thân câu, cắt bỏ từ dòng "Đáp án" / "Lời giải" trở đi. */
function bodyBeforeAnswer(block: string): string {
  const lines = block.split("\n");
  const cut = lines.findIndex((l) => FIELD_LINE_RE.test(l.trim()));
  return (cut === -1 ? lines : lines.slice(0, cut)).join("\n");
}

/**
 * Tách phần dẫn (stem) và các lựa chọn A–D (hoặc ý a–d) của một câu.
 * Nhận cả hai cách trình bày: mỗi lựa chọn một dòng, hoặc cả bốn nằm chung một
 * dòng ngăn bằng tab/khoảng trắng (kiểu xuất từ Word/Azota).
 * Quét NGƯỢC từ lựa chọn cuối: khối lựa chọn luôn nằm sau phần dẫn, nên bộ mốc
 * đúng là bộ A→B→C→D xuất hiện muộn nhất. Nhờ vậy không bám nhầm chữ cái lạc
 * trong đề dẫn ("Ba điểm A. B. C nằm trên đường thẳng...").
 */
function splitStemAndOptions(
  block: string,
  letters: string[],
): { stem: string; options: string[] } {
  const body = bodyBeforeAnswer(block);
  const marks: { at: number; textFrom: number }[] = [];
  let limit = body.length;
  for (let i = letters.length - 1; i >= 0; i--) {
    const re = new RegExp(`(?:^|\\s)\\(?${letters[i]}[.)][ \\t]+`, "g");
    let hit: RegExpExecArray | null = null;
    let m: RegExpExecArray | null;
    while ((m = re.exec(body))) {
      if (m.index >= limit) break;
      hit = m;
      re.lastIndex = m.index + 1; // mốc kề nhau có thể chồng ký tự trắng
    }
    if (!hit) break;
    marks.unshift({ at: hit.index, textFrom: hit.index + hit[0].length });
    limit = hit.index;
  }
  if (marks.length < letters.length) return { stem: inlineLatex(body), options: [] };
  const options = marks.map((mk, i) =>
    inlineLatex(body.slice(mk.textFrom, i + 1 < marks.length ? marks[i + 1].at : body.length)),
  );
  return { stem: inlineLatex(body.slice(0, marks[0].at)), options };
}

function findField(block: string, names: string): string | null {
  const cmd = block.match(new RegExp(`\\\\(?:${names})\\{([^}]*)\\}`, "i"));
  if (cmd) return cmd[1].trim();
  const label = block.match(
    new RegExp(`\\\\?(?:textbf\\{)?\\s*(?:${names})\\}?\\s*[:：]?\\s*([^\\n]*)`, "i"),
  );
  return label ? label[1].replace(/^\}/, "").trim() : null;
}

function parseMultipleChoice(
  block: string,
  answerRaw: string | null,
  explanation: string,
  n: number,
  warnings: string[],
): MultipleChoiceQuestion | null {
  const { stem, options } = splitStemAndOptions(block, ["A", "B", "C", "D"]);
  if (options.length < 4) {
    warnings.push(`Câu ${n} (trắc nghiệm): cần đủ 4 phương án A–D (thấy ${options.length}).`);
    return null;
  }
  const letter = (answerRaw ?? "").trim().toUpperCase().match(/[A-D]/)?.[0];
  if (!letter) {
    warnings.push(`Câu ${n} (trắc nghiệm): thiếu đáp án đúng (A/B/C/D).`);
    return null;
  }
  return {
    type: "multiple_choice",
    question: stem,
    options,
    answer: letter.charCodeAt(0) - 65,
    explanation: inlineLatex(explanation),
  };
}

function parseTrueFalse(
  block: string,
  answerRaw: string | null,
  explanation: string,
  n: number,
  warnings: string[],
): TrueFalseQuestion | null {
  const { stem, options } = splitStemAndOptions(block, ["a", "b", "c", "d"]);
  // bỏ tiền tố Azota "[thứ tự, mức độ]"
  const items = options.map((t) => t.replace(/^\[[^\]]*\]\s*/, ""));
  if (items.length < 4) {
    warnings.push(`Câu ${n} (đúng/sai): cần đủ 4 ý a–d (thấy ${items.length}).`);
    return null;
  }
  const ans = (answerRaw ?? "").toLowerCase().trim();
  let flags: boolean[];
  const perItem = [...ans.matchAll(/([a-d])\s*[).:]*\s*(đúng|sai|true|false|đ|s|t|f)/g)];
  if (perItem.length >= 4) {
    // "a) Đ  b) S  c) Đ  d) Đ"
    flags = ["a", "b", "c", "d"].map((L) => {
      const hit = perItem.find((p) => p[1] === L);
      return !!hit && /^(đúng|true|đ|t)$/.test(hit[2]);
    });
  } else {
    // "Đúng: a, c"  |  "a, c"  → các chữ cái liệt kê là Đúng
    const listed = new Set((ans.replace(/^.*?(đúng|true)\s*[:：]?/, "").match(/[a-d]/g) ?? ans.match(/[a-d]/g) ?? []));
    flags = ["a", "b", "c", "d"].map((L) => listed.has(L));
  }
  if (!answerRaw) warnings.push(`Câu ${n} (đúng/sai): thiếu dòng đáp án — tạm để tất cả là Sai.`);
  return {
    type: "true_false",
    question: stem,
    statements: items.map((text, i) => ({ text, answer: flags[i] ?? false })),
    explanation: inlineLatex(explanation),
  };
}

function parseShortAnswer(
  block: string,
  answerRaw: string | null,
  explanation: string,
  n: number,
  warnings: string[],
): ShortAnswerQuestion {
  const answer = (answerRaw ?? "").trim().replace(/\$/g, "").replace(/\./g, ",");
  if (!answer) warnings.push(`Câu ${n} (trả lời ngắn): thiếu đáp án.`);
  else {
    if (!/^-?\d+(,\d+)?$/.test(answer))
      warnings.push(`Câu ${n} (trả lời ngắn): đáp án "${answer}" không phải dạng số.`);
    // Giữ nguyên đáp án dài quá khổ để validateBundle chặn lại — cắt bớt sẽ
    // đẻ ra một đáp án SAI mà vẫn trông hợp lệ.
    if (answer.length > 4)
      warnings.push(
        `Câu ${n} (trả lời ngắn): đáp án "${answer}" dài quá 4 ký tự — sửa lại đề (làm tròn hoặc đổi đơn vị), đừng cắt bớt.`,
      );
  }
  return {
    type: "short_answer",
    question: inlineLatex(bodyBeforeAnswer(block)),
    answer,
    explanation: inlineLatex(explanation),
  };
}

function parseBlock(
  block: string,
  kind: QuestionType,
  n: number,
  warnings: string[],
): ExamQuestion | null {
  const answerRaw = findField(block, "Đáp\\s*án\\s*đúng|Đáp\\s*án|Đáp\\s*số|answer");
  const explanation = findField(block, "Lời\\s*giải|Giải|Hướng\\s*dẫn|explanation") ?? "";
  if (kind === "multiple_choice")
    return parseMultipleChoice(block, answerRaw, explanation, n, warnings);
  if (kind === "true_false") return parseTrueFalse(block, answerRaw, explanation, n, warnings);
  return parseShortAnswer(block, answerRaw, explanation, n, warnings);
}

/** Cắt một vùng văn bản theo mốc "Câu n." thành từng khối câu. */
function splitQuestions(section: string): string[] {
  const marker = /(?:^|\n)\s*(?:\\textbf\{)?\s*C[âa]u\s*\d+\s*[.:)]?\s*\}?/i;
  const hasMarker = marker.test(section);
  const parts = section.split(new RegExp(marker.source, "gi"));
  const body = hasMarker ? parts.slice(1) : parts;
  return body.map((p) => p.trim()).filter(Boolean);
}

export function parseExamLatex(latex: string): ExamParseResult {
  const warnings: string[] = [];
  const titleMatch = latex.match(/\\(?:sub)?section\*?\{([^}]+)\}/);
  const title =
    titleMatch && !/PH[ẦA]N/i.test(titleMatch[1]) ? titleMatch[1].trim() : "Đề mới";

  const questions: ExamQuestion[] = [];

  // Định dạng cũ: \question{Loại: ...}
  if (/\\question\s*\{/.test(latex)) {
    const blocks = latex.split(/\\question\s*\{([^}]*)\}/);
    for (let i = 1; i < blocks.length; i += 2) {
      const typeStr = blocks[i].toLowerCase();
      const body = blocks[i + 1] ?? "";
      const kind: QuestionType = /multiple_choice|trắc|a\/b\/c\/d/.test(typeStr)
        ? "multiple_choice"
        : /true_false|đúng\s*\/?\s*sai|4 ý/.test(typeStr)
          ? "true_false"
          : "short_answer";
      const q = parseBlock(body, kind, questions.length + 1, warnings);
      if (q) questions.push(q);
    }
    return { title, questions, warnings };
  }

  // Định dạng chuẩn: tách theo PHẦN I/II/III
  const partSplit = latex.split(/(?:^|\n)\s*(?:\\(?:sub)?section\*?\{)?\s*(PH[ẦA]N[^\n}]*)\}?/i);
  if (partSplit.length >= 3) {
    for (let i = 1; i < partSplit.length; i += 2) {
      const kind = detectPartType(partSplit[i]);
      if (!kind) {
        warnings.push(`Không nhận ra loại phần: "${partSplit[i].trim().slice(0, 40)}"`);
        continue;
      }
      for (const block of splitQuestions(partSplit[i + 1] ?? "")) {
        const q = parseBlock(block, kind, questions.length + 1, warnings);
        if (q) questions.push(q);
      }
    }
  } else {
    warnings.push("Không tìm thấy 'PHẦN I/II/III' — kiểm tra lại định dạng đề.");
  }

  if (questions.length === 0) warnings.push("Không parse được câu hỏi nào.");
  return { title, questions, warnings };
}
