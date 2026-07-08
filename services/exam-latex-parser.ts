/**
 * LaTeX Exam Parser
 * Parse structured LaTeX exam format into ExamQuestion array
 */

import type { ExamQuestion, MultipleChoiceQuestion, TrueFalseQuestion, ShortAnswerQuestion } from "@/features/exams/types";

export interface ExamParseResult {
  title: string;
  questions: ExamQuestion[];
  warnings: string[];
}

/**
 * Parse LaTeX exam format
 *
 * Format:
 * \section{Exam Title}
 *
 * \question{Loại: multiple_choice}
 * Question content
 * A) Option A
 * B) Option B
 * C) Option C
 * D) Option D
 * \answer{A}
 * \explanation{Explanation text}
 *
 * OR
 *
 * \question{Loại: true_false}
 * Statement
 * a) True/False statement
 * b) True/False statement
 * ...
 * \answer{a, c}
 * \explanation{Explanation}
 *
 * OR
 *
 * \question{Loại: short_answer}
 * Question?
 * \answer{correct answer}
 * \explanation{Explanation}
 */
export function parseExamLatex(latex: string): ExamParseResult {
  const warnings: string[] = [];

  // Extract title from \section
  const titleMatch = latex.match(/\\section\{([^}]+)\}/);
  const title = titleMatch?.[1] || "Untitled Exam";

  // Split by \question
  const questionBlocks = latex.split(/\\question\s*\{([^}]*)\}/);

  if (questionBlocks.length < 3) {
    warnings.push("Không tìm thấy câu hỏi nào. Kiểm tra định dạng \\question{Loại: ...}");
    return { title, questions: [], warnings };
  }

  const questions: ExamQuestion[] = [];

  // Process question blocks (skip first empty element)
  for (let i = 1; i < questionBlocks.length; i += 2) {
    const typeStr = questionBlocks[i].trim();
    const content = questionBlocks[i + 1]?.trim() || "";

    // Parse type from "Loại: multiple_choice" or similar
    let type: ExamQuestion["type"] = "short_answer";
    if (typeStr.includes("multiple_choice") || typeStr.includes("trắc") || typeStr.includes("A/B/C/D")) {
      type = "multiple_choice";
    } else if (typeStr.includes("true_false") || typeStr.includes("đúng/sai") || typeStr.includes("4 ý")) {
      type = "true_false";
    }

    // Extract question, answer, explanation
    const questionMatch = content.match(/^([\s\S]*?)(?=\\answer\{|$)/);
    const answerMatch = content.match(/\\answer\{([^}]+)\}/);
    const explanationMatch = content.match(/\\explanation\{([^}]+)\}/);

    const questionText = questionMatch?.[1]?.trim() || "";
    const answerText = answerMatch?.[1]?.trim() || "";
    const explanationText = explanationMatch?.[1]?.trim() || "";

    if (!questionText) {
      warnings.push(`Câu ${questions.length + 1}: Nội dung câu hỏi trống`);
      continue;
    }

    if (!answerText) {
      warnings.push(`Câu ${questions.length + 1}: Thiếu \\answer{...}`);
      continue;
    }

    try {
      const q = parseQuestion(type, questionText, answerText, explanationText, questions.length + 1);
      if (q) {
        questions.push(q);
      }
    } catch (err) {
      warnings.push(`Câu ${questions.length + 1}: ${err instanceof Error ? err.message : "Lỗi không xác định"}`);
    }
  }

  return { title, questions, warnings };
}

function parseQuestion(
  type: ExamQuestion["type"],
  questionText: string,
  answerText: string,
  explanationText: string,
  index: number,
): ExamQuestion | null {
  if (type === "multiple_choice") {
    return parseMultipleChoice(questionText, answerText, explanationText, index);
  } else if (type === "true_false") {
    return parseTrueFalse(questionText, answerText, explanationText, index);
  } else {
    return parseShortAnswer(questionText, answerText, explanationText, index);
  }
}

function parseMultipleChoice(
  questionText: string,
  answerText: string,
  explanationText: string,
  index: number,
): MultipleChoiceQuestion | null {
  // Extract A) B) C) D) options
  const optionMatches = questionText.match(/[A-D]\)\s*([^\n]+)/g) || [];

  if (optionMatches.length < 4) {
    throw new Error(`Câu ${index}: Trắc nghiệm phải có 4 option (A/B/C/D)`);
  }

  const options = optionMatches.slice(0, 4).map((opt) => opt.replace(/^[A-D]\)\s*/, ""));

  // Parse answer (A, B, C, or D)
  const answerLetter = answerText.trim().toUpperCase();
  if (!["A", "B", "C", "D"].includes(answerLetter)) {
    throw new Error(`Câu ${index}: Đáp án phải là A/B/C/D`);
  }

  const answerIndex = answerLetter.charCodeAt(0) - 65; // A=0, B=1, C=2, D=3

  return {
    type: "multiple_choice",
    question: questionText,
    options,
    answer: answerIndex,
    explanation: explanationText,
  };
}

function parseTrueFalse(
  questionText: string,
  answerText: string,
  explanationText: string,
  index: number,
): TrueFalseQuestion | null {
  // Extract a) b) c) d) statements
  const statementMatches = questionText.match(/[a-d]\)\s*([^\n]+)/g) || [];

  if (statementMatches.length < 4) {
    throw new Error(`Câu ${index}: Đúng/Sai phải có 4 ý (a/b/c/d)`);
  }

  // Parse which are correct: "a, c" or "a" or "b, d"
  const correctLetters = answerText
    .split(/[,;]/)
    .map((s) => s.trim().toLowerCase())
    .filter((s) => /^[a-d]$/.test(s));

  if (correctLetters.length === 0) {
    throw new Error(`Câu ${index}: \\answer phải chứa a/b/c/d (ví dụ: a,c)`);
  }

  const statements = statementMatches.slice(0, 4).map((stmt, idx) => ({
    text: stmt.replace(/^[a-d]\)\s*/, ""),
    answer: correctLetters.includes(String.fromCharCode(97 + idx)), // a=97, b=98, ...
  }));

  return {
    type: "true_false",
    question: questionText,
    statements,
    explanation: explanationText,
  };
}

function parseShortAnswer(
  questionText: string,
  answerText: string,
  explanationText: string,
  index: number,
): ShortAnswerQuestion {
  return {
    type: "short_answer",
    question: questionText,
    answer: answerText,
    explanation: explanationText,
  };
}
