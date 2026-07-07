import type {
  ExamQuestion,
  MultipleChoiceQuestion,
  ShortAnswerQuestion,
  TrueFalseQuestion,
} from "@/features/exams/types";

export interface ParseResult {
  questions: ExamQuestion[];
  warnings: string[];
}

interface Block {
  text: string; // văn bản thuần để nhận diện cấu trúc
  html: string; // giữ ảnh, sub/sup, in đậm
}

const Q_START = /^C[âa]u\s*(\d+)\s*[.:)]?\s*/i;
const ANSWER_LINE = /^Đáp\s*án\s*[:.]?\s*/i;
// Dạng "Chọn đáp án C" — bắt buộc theo sau là 1 chữ cái A–D (word boundary)
// để không nhận nhầm câu dẫn kiểu "…hãy chọn đáp án đúng nhất".
const ANSWER_CHOICE = /Chọn\s*đáp\s*án\s*[:.]?\s*([A-D])\b/i;
const EXPLANATION_LINE = /^(Lời\s*giải|Giải\s*thích|Hướng\s*dẫn(\s*giải)?)\s*[:.]?\s*/i;
const OPTION_TOKEN = /(?:^|\s)(\*?)([A-D])[.)]\s+/g;
const STATEMENT_LINE = /^([a-d])[.)]\s*/i;

function stripHtml(html: string): string {
  const div = document.createElement("div");
  div.innerHTML = html;
  return (div.textContent ?? "").trim();
}

/** Tách 1 đoạn có thể chứa nhiều đáp án trên cùng dòng: "A. xx B. yy *C. zz" */
function splitOptions(block: Block): { star: boolean; letter: string; html: string }[] {
  const found: { star: boolean; letter: string; index: number; length: number }[] = [];
  let m: RegExpExecArray | null;
  OPTION_TOKEN.lastIndex = 0;
  while ((m = OPTION_TOKEN.exec(block.text))) {
    found.push({
      star: m[1] === "*",
      letter: m[2],
      index: m.index,
      length: m[0].length,
    });
  }
  // map vị trí text sang html là không tin cậy — nếu block chỉ có text (không ảnh)
  // thì cắt theo text; nếu có ảnh thì cắt html theo cùng marker.
  return found.map((f, i) => {
    const end = i + 1 < found.length ? found[i + 1].index : block.text.length;
    let body = block.text.slice(f.index + f.length, end).trim();
    if (block.html.includes("<img")) {
      // cắt html theo marker chữ cái để giữ ảnh trong đáp án
      const parts = block.html.split(/(?:^|\s|>)\*?[A-D][.)]\s/);
      if (parts.length === found.length + 1) body = parts[i + 1].trim();
    }
    return { star: f.star, letter: f.letter, html: body };
  });
}

export function parseWordHtml(rawHtml: string): ParseResult {
  const warnings: string[] = [];
  const doc = new DOMParser().parseFromString(rawHtml, "text/html");
  // Word hay dùng danh sách tự đánh số (a. / A.) — mammoth xoá ký tự đầu dòng,
  // nên với <li> trong <ol> ta tự khôi phục marker theo thứ tự.
  const blocks: Block[] = [...doc.body.querySelectorAll("p, li, tr")]
    .map((el) => {
      let text = (el.textContent ?? "").replace(/\s+/g, " ").trim();
      const html = el.innerHTML.trim();
      if (
        el.tagName === "LI" &&
        el.parentElement?.tagName === "OL" &&
        !Q_START.test(text) &&
        !/^[*]?[A-Da-d][.)]\s/.test(text)
      ) {
        const idx = [...el.parentElement.children].indexOf(el);
        if (idx < 4) text = `${String.fromCharCode(97 + idx)}. ${text}`;
      }
      return { html, text };
    })
    .filter((b) => b.text !== "" || b.html.includes("<img"));

  // gom block theo câu
  const questionBlocks: Block[][] = [];
  let current: Block[] | null = null;
  for (const b of blocks) {
    // "Câu 1 : Chọn đáp án C" là dòng ĐÁP ÁN của câu hiện tại, không phải câu mới
    if (Q_START.test(b.text) && !ANSWER_CHOICE.test(b.text)) {
      current = [b];
      questionBlocks.push(current);
    } else if (current) {
      current.push(b);
    }
  }

  const questions: ExamQuestion[] = [];

  for (const qb of questionBlocks) {
    const numMatch = qb[0].text.match(Q_START);
    const qNum = numMatch?.[1] ?? String(questions.length + 1);
    // bỏ tiền tố "Câu N." khỏi block đầu
    qb[0] = {
      text: qb[0].text.replace(Q_START, ""),
      html: qb[0].html.replace(/^(<strong>)?\s*C[âa]u\s*\d+\s*[.:)]?\s*(<\/strong>)?\s*/i, ""),
    };

    const stemParts: string[] = [];
    const options: { star: boolean; letter: string; html: string }[] = [];
    const statements: { letter: string; html: string }[] = [];
    const explanationParts: string[] = [];
    let answerText = "";
    let inExplanation = false;

    for (const b of qb) {
      // "Chọn đáp án C" (xuất hiện trước và/hoặc sau lời giải) → lấy chữ cái đúng
      const chosen = b.text.match(ANSWER_CHOICE);
      if (chosen) {
        answerText = chosen[1];
        inExplanation = false;
        continue;
      }
      if (ANSWER_LINE.test(b.text)) {
        answerText = b.text.replace(ANSWER_LINE, "").trim();
        inExplanation = false;
        continue;
      }
      if (EXPLANATION_LINE.test(b.text)) {
        inExplanation = true;
        const rest = b.html.replace(
          /^(<strong>|<em>)*\s*(Lời\s*giải|Giải\s*thích|Hướng\s*dẫn(\s*giải)?)\s*[:.]?\s*(<\/strong>|<\/em>)*\s*/i,
          "",
        );
        if (stripHtml(rest)) explanationParts.push(rest);
        continue;
      }
      if (inExplanation) {
        explanationParts.push(b.html);
        continue;
      }
      // chỉ coi là dòng đáp án khi có ≥2 marker (A. x B. y) hoặc marker nằm
      // ngay đầu dòng — tránh nhận nhầm "…biên độ A. Xét…" giữa câu dẫn
      OPTION_TOKEN.lastIndex = 0;
      const optMatches = [...b.text.matchAll(OPTION_TOKEN)];
      if (
        optMatches.length >= 2 ||
        (optMatches.length === 1 && optMatches[0].index === 0)
      ) {
        options.push(...splitOptions(b));
        continue;
      }
      const st = b.text.match(STATEMENT_LINE);
      if (st && options.length === 0) {
        statements.push({
          letter: st[1].toLowerCase(),
          html: b.html.replace(/^(<strong>|<em>)*\s*[a-d][.)]\s*(<\/strong>|<\/em>)*\s*/i, ""),
        });
        continue;
      }
      stemParts.push(b.html);
    }

    // danh sách tự đánh số có thể là 4 đáp án A–D: nếu đáp án là 1 chữ cái
    // (không phải Đúng/Sai) thì chuyển statements thành options
    if (
      options.length === 0 &&
      statements.length >= 2 &&
      /^[A-Da-d]\b/.test(answerText.trim()) &&
      !/Đúng|Sai/i.test(answerText)
    ) {
      options.push(
        ...statements.map((s, i) => ({
          star: false,
          letter: String.fromCharCode(65 + i),
          html: s.html,
        })),
      );
      statements.length = 0;
    }

    const stem = stemParts.join("<br>");
    const explanation = explanationParts.join("<br>");

    if (options.length >= 2) {
      // ----- Trắc nghiệm A/B/C/D -----
      const opts = ["", "", "", ""];
      let answer = -1;
      for (const o of options) {
        const idx = o.letter.charCodeAt(0) - 65;
        if (idx >= 0 && idx < 4) {
          opts[idx] = o.html;
          if (o.star) answer = idx;
        }
      }
      if (answer < 0 && answerText) {
        const am = answerText.match(/[A-D]/i);
        if (am) answer = am[0].toUpperCase().charCodeAt(0) - 65;
      }
      if (answer < 0) {
        warnings.push(`Câu ${qNum}: không tìm thấy đáp án đúng — tạm chọn A.`);
        answer = 0;
      }
      if (options.length !== 4)
        warnings.push(`Câu ${qNum}: có ${options.length} đáp án (chuẩn là 4).`);
      questions.push({
        type: "multiple_choice",
        question: stem,
        options: opts,
        answer,
        explanation,
      } satisfies MultipleChoiceQuestion);
    } else if (statements.length >= 2) {
      // ----- Đúng / Sai -----
      // đáp án dạng "a Đúng b Sai c Đúng d Sai" hoặc "a-Đ b-S..."
      const truth: Record<string, boolean> = {};
      const tfRe = /([a-d])\s*[-.):]?\s*(Đúng|Sai|Đ\b|S\b)/gi;
      let tm: RegExpExecArray | null;
      while ((tm = tfRe.exec(answerText))) {
        truth[tm[1].toLowerCase()] = /^(Đúng|Đ)$/i.test(tm[2]);
      }
      if (Object.keys(truth).length === 0)
        warnings.push(`Câu ${qNum}: không đọc được đáp án Đúng/Sai — mặc định tất cả Đúng.`);
      const four = ["a", "b", "c", "d"].map((letter) => {
        const st = statements.find((s) => s.letter === letter);
        return { text: st?.html ?? "", answer: truth[letter] ?? true };
      });
      if (statements.length !== 4)
        warnings.push(`Câu ${qNum}: có ${statements.length} ý (chuẩn là 4).`);
      questions.push({
        type: "true_false",
        question: stem,
        statements: four,
        explanation,
      } satisfies TrueFalseQuestion);
    } else {
      // ----- Trả lời ngắn -----
      const answer = answerText.replace(/[^0-9,.\-]/g, "").slice(0, 4);
      if (!answer)
        warnings.push(`Câu ${qNum}: không có đáp án trả lời ngắn — cần điền tay.`);
      questions.push({
        type: "short_answer",
        question: stem || options.map((o) => o.html).join(" "),
        answer,
        explanation,
      } satisfies ShortAnswerQuestion);
    }
  }

  if (questions.length === 0)
    warnings.push(
      'Không nhận diện được câu hỏi nào. Đề cần có dạng "Câu 1." ở đầu mỗi câu.',
    );

  return { questions, warnings };
}
