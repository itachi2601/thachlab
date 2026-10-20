// Chọn từ cần phát âm khi học sinh bấm một phương án quiz AVCN (thầy chốt 20/10/2026).
//
// Quy tắc:
// - Quiz có khai từ đang hỏi (`data-tl-word`, dùng cho câu "workpieces nghĩa là gì?" có phương án tiếng Việt):
//   đọc chính từ đó, không đọc phương án.
// - Còn lại đọc đúng phương án vừa bấm nếu nó là tiếng Anh ("lathe", "milling machine", "press").
//   Không đọc phương án tiếng Việt ("phôi") hay "True (Đúng)"/"False (Sai)".
//
// Cùng luật này được build_avcn.py + tao_giong_doc.py dùng để gắn mp3; sửa một bên thì sửa cả ba.

/** Chữ có dấu tiếng Việt (đủ bộ, kể cả chữ hoa nhờ cờ i). */
const VIET = /[àáảãạăằắẳẵặâầấẩẫậđèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵ]/i;

/** Bỏ nhãn phương án ở đầu ("a. ", "b) ") — cùng dạng với nhãn đề thật. */
export function stripOptionLabel(text: string): string {
  return text
    .replace(/\s+/g, " ")
    .replace(/^\s*[a-dA-D][.)]\s+/, "")
    .trim();
}

/**
 * Từ sẽ đọc khi bấm một phương án.
 * @param optionText chữ của phương án (đã render, có thể còn nhãn "a. ")
 * @param quizWord  từ tiếng Anh đang hỏi (`data-tl-word` trên .tl-quiz), rỗng nếu không khai
 * @returns chuỗi cần đọc, hoặc "" nếu không nên phát âm (phương án tiếng Việt, True/False, chú thích)
 */
export function quizSpeakText(optionText: string, quizWord = ""): string {
  const word = quizWord.replace(/\s+/g, " ").trim();
  if (word) return word;
  const text = stripOptionLabel(optionText);
  if (!text || text.length > 80) return "";
  if (!/[A-Za-z]/.test(text)) return "";
  if (VIET.test(text)) return "";
  // "True (Đúng)" / "False (Sai)" và phương án có chú thích trong ngoặc: không đọc.
  if (/[()]/.test(text)) return "";
  return text;
}
