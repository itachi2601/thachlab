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
  Difficulty,
  DifficultySource,
  ExamQuestion,
  MultipleChoiceQuestion,
  QuestionForm,
  ShortAnswerQuestion,
  TrueFalseQuestion,
} from "@/features/exams/types";
import { missingFigureWarning, questionsMissingFigure } from "@/services/question-figures";

export interface ExamParseResult {
  title: string;
  questions: ExamQuestion[];
  warnings: string[];
}

export interface ExamParseOptions {
  /**
   * Giữ lại cả câu còn thiếu (chưa đủ 4 phương án, chưa rõ đáp án) thay vì bỏ đi:
   * câu thiếu vẫn hiện trong trình sửa để người dùng điền nốt, và số thứ tự các
   * câu không bị lệch. Chỗ còn thiếu để `answer = -1` / phương án rỗng nên
   * validateBundle vẫn chặn, không thể đăng nhầm một đáp án bịa.
   */
  lenient?: boolean;
}

type QuestionType = "multiple_choice" | "true_false" | "short_answer";

/** Mốc thay cho hình TikZ — web không vẽ được, phải render ra SVG/PNG trước rồi \includegraphics. */
export const TIKZ_MARK = "⟦hình TikZ⟧";

/**
 * `\includegraphics[...]{duong/dan/hinh.png}` → thẻ <img> trỏ placeholder `media/hinh.png`
 * (cùng quy ước với ảnh trong lý thuyết: bundle khai báo trong raster_images, lúc đăng
 * uploadLessonMedia thay placeholder bằng URL Storage). Bỏ vỏ figure/center/caption.
 */
function figuresToHtml(input: string): string {
  let s = input;
  s = s.replace(/\\begin\{(?:figure|center|wrapfigure)\*?\}(?:\[[^\]]*\])?(?:\{[^{}]*\})*/g, "");
  s = s.replace(/\\end\{(?:figure|center|wrapfigure)\*?\}/g, "");
  s = s.replace(/\\centering\b/g, "");
  s = s.replace(/\\caption\{([^{}]*)\}/g, "<em>$1</em>");
  s = s.replace(/\\includegraphics\s*(?:\[[^\]]*\])?\s*\{([^{}]+)\}/g, (_m, path: string) => {
    const base = path.trim().replace(/\\/g, "/").split("/").pop() ?? "";
    if (!base) return "";
    const name = /\.[a-z0-9]+$/i.test(base) ? base : `${base}.png`;
    return `<img src="media/${name}" alt="Hình" class="mx-auto my-2 max-w-full rounded-lg" />`;
  });
  return s;
}

/** Chuyển LaTeX inline nhẹ → HTML, giữ nguyên `$...$`. */
function inlineLatex(input: string): string {
  let s = figuresToHtml(input.trim());
  s = s.replace(/\\textbf\{([^{}]*)\}/g, "<strong>$1</strong>");
  s = s.replace(/\\textit\{([^{}]*)\}/g, "<em>$1</em>");
  s = s.replace(/\\emph\{([^{}]*)\}/g, "<em>$1</em>");
  s = s.replace(/\\%/g, "%").replace(/\\&/g, "&").replace(/\\_/g, "_");
  s = s.replace(/\\\\\s*/g, "<br>");
  // Văn bản Azota gõ tay (không phải LaTeX thật): mỗi Enter là chủ ý xuống dòng
  // (liệt kê bước thí nghiệm, ý a)/b)...), không phải chỗ wrap tự động — giữ lại
  // bằng <br> thay vì gộp thành khoảng trắng như trước, kẻo các ý dính liền một câu.
  s = s.replace(/\n{2,}/g, "\n");
  s = s.replace(/[ \t]*\n[ \t]*/g, "<br>").trim();
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

/**
 * Dòng nhãn phân loại của một câu (đặt ở bất kỳ đâu trong khối câu, thường sau "Lời giải"):
 *   Chủ đề: <tên yêu cầu cần đạt trong danh mục>     (cũng nhận YCCĐ: / Yêu cầu cần đạt: / Năng lực:)
 *   Dạng: lý thuyết | bài tập                           (cũng nhận Loại:)
 *   Mức độ: dễ | trung bình | khó                       (cũng nhận Độ khó:)
 * Bắt buộc có dấu hai chấm để không cắt nhầm câu dẫn bắt đầu bằng "Dạng…".
 */
const TAG_LINE_RE =
  /^\\?(?:textbf\{)?\s*(Chủ\s*đề|YCCĐ|Yêu\s*cầu\s*cần\s*đạt|Năng\s*lực|Dạng|Loại|Mức\s*độ|Độ\s*khó)\}?\s*[:：]\s*(.*?)\s*$/i;

export function parseFormLabel(raw: string): QuestionForm | "" {
  const v = raw.trim().toLowerCase();
  if (!v) return "";
  if (/^(l[ýi]\s*thuy[ếe]t|lt|ly_thuyet)$/.test(v)) return "ly_thuyet";
  if (/^(b[àa]i\s*t[ậa]p|bt|bai_tap)$/.test(v)) return "bai_tap";
  return "";
}

/** Hậu tố nguồn gắn kèm giá trị "Mức độ: …" — vd "dễ (AI)" / "dễ (GV)" (xem `DifficultySource`). */
const DIFFICULTY_SOURCE_SUFFIX_RE = /\s*\((AI|GV)\)\s*$/i;

export function parseDifficultyLabel(raw: string): Difficulty {
  const v = raw.trim().replace(DIFFICULTY_SOURCE_SUFFIX_RE, "").toLowerCase();
  if (!v) return "";
  if (/^(d[ễe]|de)$/.test(v)) return "de";
  if (/^(trung\s*b[ìi]nh|tb|trung-binh)$/.test(v)) return "trung-binh";
  if (/^(kh[óo]|kho)$/.test(v)) return "kho";
  return "";
}

/** Nguồn kèm theo giá trị "Mức độ: …", nếu có ghi (vd "dễ (AI)"). Không có hậu tố → không rõ
 *  nguồn (đề gắn từ trước khi có tính năng phân biệt gv/ai, hoặc soạn tay ngoài luồng UI). */
export function parseDifficultySourceSuffix(raw: string): DifficultySource | undefined {
  const m = raw.trim().match(DIFFICULTY_SOURCE_SUFFIX_RE);
  return m ? (m[1].toLowerCase() as DifficultySource) : undefined;
}

/** Rút dòng "Chủ đề:" / "Dạng:" / "Mức độ:" ra khỏi khối câu; trả về khối đã bỏ các dòng đó. */
function extractTags(
  block: string,
  n: number,
  warnings: string[],
): {
  block: string;
  topic: string;
  form: QuestionForm | "";
  difficulty: Difficulty;
  difficultySource: DifficultySource | undefined;
} {
  let topic = "";
  let form: QuestionForm | "" = "";
  let difficulty: Difficulty = "";
  let difficultySource: DifficultySource | undefined;
  const kept: string[] = [];
  for (const line of block.split("\n")) {
    const m = line.match(TAG_LINE_RE);
    if (!m) {
      kept.push(line);
      continue;
    }
    const key = m[1].toLowerCase();
    const value = m[2].replace(/\}$/, "").trim();
    if (/^(d[ạa]ng|lo[ạa]i)$/.test(key)) {
      form = parseFormLabel(value);
      if (value && !form) warnings.push(`Câu ${n}: "Dạng: ${value}" không hiểu — chỉ nhận "lý thuyết" hoặc "bài tập".`);
    } else if (/^(m[ứu]c\s*độ|độ\s*kh[óo])$/.test(key)) {
      difficulty = parseDifficultyLabel(value);
      difficultySource = parseDifficultySourceSuffix(value);
      if (value && !difficulty) warnings.push(`Câu ${n}: "Mức độ: ${value}" không hiểu — chỉ nhận "dễ", "trung bình" hoặc "khó".`);
    } else topic = value.replace(/\s+/g, " ");
  }
  return { block: kept.join("\n"), topic, form, difficulty, difficultySource };
}

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
  // Neo vào ĐẦU DÒNG (xét từng dòng, giống bodyBeforeAnswer/explanationOf) — không thì cụm
  // "đáp án" xuất hiện tự nhiên giữa đề dẫn (vd "Chọn đáp án không đúng") bị bắt nhầm thành
  // dòng khai báo đáp án thật, nuốt mất chữ cái đúng nằm ở dòng "Đáp án: B" thật sự phía sau.
  // Cho phép tiền tố "Chọn " (quy ước lời giải của xuat_thachlab.py: dòng đầu lời giải là
  // "Chọn đáp án D", không có dấu hai chấm) — vẫn phải là ĐẦU DÒNG, không khớp giữa câu dẫn.
  const re = new RegExp(`^\\\\?(?:textbf\\{)?\\s*(?:Chọn\\s+)?(?:${names})\\}?\\s*[:：]?\\s*([^\\n]*)`, "i");
  for (const line of block.split("\n")) {
    const m = line.match(re);
    if (m) return m[1].replace(/^\}/, "").trim();
  }
  return null;
}

function parseMultipleChoice(
  block: string,
  answerRaw: string | null,
  explanation: string,
  n: number,
  warnings: string[],
  lenient: boolean,
): MultipleChoiceQuestion | null {
  const { stem, options } = splitStemAndOptions(block, ["A", "B", "C", "D"]);
  if (options.length < 4) {
    warnings.push(`Câu ${n} (trắc nghiệm): cần đủ 4 phương án A–D (thấy ${options.length}).`);
    if (!lenient) return null;
  }
  const letter = (answerRaw ?? "").trim().toUpperCase().match(/[A-D]/)?.[0];
  if (!letter) {
    warnings.push(`Câu ${n} (trắc nghiệm): thiếu đáp án đúng (A/B/C/D).`);
    if (!lenient) return null;
  }
  return {
    type: "multiple_choice",
    question: stem,
    options: [0, 1, 2, 3].map((i) => options[i] ?? ""),
    answer: letter ? letter.charCodeAt(0) - 65 : -1,
    explanation: inlineLatex(explanation),
  };
}

function parseTrueFalse(
  block: string,
  answerRaw: string | null,
  explanation: string,
  n: number,
  warnings: string[],
  lenient: boolean,
): TrueFalseQuestion | null {
  const { stem, options } = splitStemAndOptions(block, ["a", "b", "c", "d"]);
  // bỏ tiền tố Azota "[thứ tự, mức độ]"
  const items = options.map((t) => t.replace(/^\[[^\]]*\]\s*/, ""));
  if (items.length < 4) {
    warnings.push(`Câu ${n} (đúng/sai): cần đủ 4 ý a–d (thấy ${items.length}).`);
    if (!lenient) return null;
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
    statements: [0, 1, 2, 3].map((i) => ({ text: items[i] ?? "", answer: flags[i] ?? false })),
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

const EXPLANATION_LINE_RE =
  /^\\?(?:textbf\{)?\s*(?:Lời\s*giải|Giải|Hướng\s*dẫn|explanation)\}?\s*[:：]?\s*(.*)$/i;
const ANSWER_FIELD_RE = /^\\?(?:textbf\{)?\s*(?:Đáp\s*án|Đáp\s*số|answer)\b/i;

/**
 * Lời giải = từ dòng "Lời giải:" tới hết khối câu (nhiều đoạn — đề Word/Azota hay
 * giải 3–5 dòng), bỏ dòng "Đáp án:" nếu nằm sau. Các đoạn nối bằng <br>.
 * Dạng lệnh `\explanation{…}` cũ vẫn nhận.
 */
function explanationOf(block: string): string {
  const cmd = block.match(/\\explanation\{([^}]*)\}/i);
  if (cmd) return cmd[1].trim();
  const lines = block.split("\n");
  const at = lines.findIndex((l) => EXPLANATION_LINE_RE.test(l.trim()));
  if (at === -1) return "";
  const first = lines[at].trim().match(EXPLANATION_LINE_RE)?.[1].replace(/^\}/, "").trim() ?? "";
  const rest = lines
    .slice(at + 1)
    .map((l) => l.trim())
    .filter((l) => l && !ANSWER_FIELD_RE.test(l));
  return [first, ...rest].filter(Boolean).join("<br>");
}

function parseBlock(
  raw: string,
  kind: QuestionType,
  n: number,
  warnings: string[],
  lenient: boolean,
): ExamQuestion | null {
  const { block, topic, form, difficulty, difficultySource } = extractTags(raw, n, warnings);
  const answerRaw = findField(block, "Đáp\\s*án\\s*đúng|Đáp\\s*án|Đáp\\s*số|answer");
  const explanation = explanationOf(block);
  const q =
    kind === "multiple_choice"
      ? parseMultipleChoice(block, answerRaw, explanation, n, warnings, lenient)
      : kind === "true_false"
        ? parseTrueFalse(block, answerRaw, explanation, n, warnings, lenient)
        : parseShortAnswer(block, answerRaw, explanation, n, warnings);
  if (!q) return q;
  if (topic) q.topic = topic;
  if (form) q.form = form;
  if (difficulty) {
    q.difficulty = difficulty;
    if (difficultySource) q.difficultySource = difficultySource;
  }
  return q;
}

/** Cắt một vùng văn bản theo mốc "Câu n." thành từng khối câu. */
function splitQuestions(section: string): string[] {
  const marker = /(?:^|\n)\s*(?:\\textbf\{)?\s*C[âa]u\s*\d+\s*[.:)]\s*\}?/i;
  const hasMarker = marker.test(section);
  const parts = section.split(new RegExp(marker.source, "gi"));
  const body = hasMarker ? parts.slice(1) : parts;
  return body.map((p) => p.trim()).filter(Boolean);
}

export function parseExamLatex(latexInput: string, opts: ExamParseOptions = {}): ExamParseResult {
  const lenient = opts.lenient === true;
  const warnings: string[] = [];

  // Hình TikZ: web không vẽ được — thay bằng mốc để câu vẫn dựng được, và cảnh báo rõ.
  let tikzCount = 0;
  const latex = latexInput.replace(/\\begin\{tikzpicture\}[\s\S]*?\\end\{tikzpicture\}/g, () => {
    tikzCount += 1;
    return ` ${TIKZ_MARK} `;
  });
  if (tikzCount > 0)
    warnings.push(
      `Có ${tikzCount} hình TikZ — web không vẽ được, chỗ đó hiện là "${TIKZ_MARK}". ` +
        "Render TikZ ra PNG/SVG rồi thay bằng \\includegraphics{...} trước khi đăng.",
    );
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
      const q = parseBlock(body, kind, questions.length + 1, warnings, lenient);
      if (q) questions.push(q);
    }
    const missingFigOld = missingFigureWarning(questionsMissingFigure(questions));
    if (missingFigOld) warnings.push(missingFigOld);
    return { title, questions, warnings };
  }

  // Định dạng chuẩn: tách theo PHẦN I/II/III — bắt buộc ngay sau "PHẦN" phải là số La Mã/số
  // thường (I/II/III/1/2/3…) mới coi là mốc tiêu đề thật. Không có điều kiện này thì một câu
  // dẫn bình thường bắt đầu đoạn văn bằng "Phần trăm…"/"Phần công…"/"Phần ứng…" cũng bị nhận
  // nhầm thành ranh giới PHẦN mới, cắt đôi đề và làm sai loại câu (trắc nghiệm/đúng-sai/ngắn)
  // của mọi câu phía sau mốc giả đó.
  const partSplit = latex.split(/(?:^|\n)\s*(?:\\(?:sub)?section\*?\{)?\s*(PH[ẦA]N\s+(?:[IVXivx]+|\d+)\b[^\n}]*)\}?/i);
  if (partSplit.length >= 3) {
    for (let i = 1; i < partSplit.length; i += 2) {
      const kind = detectPartType(partSplit[i]);
      if (!kind) {
        warnings.push(`Không nhận ra loại phần: "${partSplit[i].trim().slice(0, 40)}"`);
        continue;
      }
      for (const block of splitQuestions(partSplit[i + 1] ?? "")) {
        const q = parseBlock(block, kind, questions.length + 1, warnings, lenient);
        if (q) questions.push(q);
      }
    }
  } else {
    warnings.push("Không tìm thấy 'PHẦN I/II/III' — kiểm tra lại định dạng đề.");
  }

  if (questions.length === 0) warnings.push("Không parse được câu hỏi nào.");
  const missingFig = missingFigureWarning(questionsMissingFigure(questions));
  if (missingFig) warnings.push(missingFig);
  return { title, questions, warnings };
}
