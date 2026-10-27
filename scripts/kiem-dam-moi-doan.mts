// Kiểm quy tắc "mỗi đoạn một chỗ in đậm" (N7, thầy duyệt 26/10/2026) trong bài lý thuyết soạn sẵn.
// CHỈ ĐỌC file, KHÔNG GHI gì. Báo các <p>/<li> có từ 2 cụm <strong>/<b> trở lên — đoạn in đậm nhiều chỗ thì
// không chỗ nào nổi nữa. Bỏ qua dòng nhãn (.tl-label, .tl-meo), dòng từ khoá "🔑", ô đáp án quiz (.tl-opt) và
// phản hồi quiz (.tl-fb mở đầu bằng <strong>Chính xác.</strong>/<strong>Chưa đúng.</strong>) và nhãn đầu dòng "<strong>X:</strong>".
//   npx tsx scripts/kiem-dam-moi-doan.mts                              # mọi content/**/theory.src.html (không có thì theory.html)
//   npx tsx scripts/kiem-dam-moi-doan.mts content/lesson-samples/l12-su-chuyen-the/theory.html
// Thoát mã 1 khi có vi phạm (dùng được trong bước kiểm của skill soan-bai-ly-thuyet-tuong-tac).
import fs from "node:fs";
import path from "node:path";

function findTheoryFiles(dir: string, out: string[] = []): string[] {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name === "node_modules" || entry.name.startsWith(".")) continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) findTheoryFiles(full, out);
    else if (entry.name === "theory.src.html") out.push(full);
    else if (entry.name === "theory.html" && !fs.existsSync(path.join(dir, "theory.src.html"))) out.push(full);
  }
  return out;
}

const SKIP_CLASS = /class="[^"]*\b(tl-label|tl-meo|tl-opt)\b/;
const BOLD = /<(strong|b)\b[^>]*>/gi;

// Quét thẻ theo ngăn xếp để <li> lồng nhau (danh sách con) được tính riêng: chữ của danh sách con thuộc <li> con,
// không cộng dồn vào <li> cha. (Bản trước dùng regex lười nên <li> cha bị cắt ở </li> đầu tiên của danh sách con.)
// Giới hạn: không hiểu thẻ đóng thiếu (<li> không có </li>) — file soạn tay luôn đóng đủ.
const TAG = /<(\/?)(p|li|ul|ol)\b([^>]*)>/gi;
type Frame = { tag: string; attrs: string; start: number; own: string };

function check(file: string): string[] {
  const html = fs.readFileSync(file, "utf8");
  const problems: string[] = [];
  const stack: Frame[] = [];
  let last = 0;
  let m: RegExpExecArray | null;
  const judge = ({ tag, attrs, start, own: inner }: Frame) => {
    if (SKIP_CLASS.test(`class="${attrs}"`) || SKIP_CLASS.test(attrs)) return;
    const text = inner.replace(/<[^>]+>/g, "").trim();
    if (text.startsWith("🔑")) return;
    // Bỏ cụm mở đầu phản hồi quiz ("Chính xác." / "Chưa đúng.") — đó là nhãn, không phải chỗ nhấn ý.
    // Cũng bỏ nhãn đầu dòng kiểu "<strong>Rời:</strong>", "<b>⭐⭐ Khá:</b>" — nhãn mở dòng, không phải chỗ nhấn ý.
    const body = inner
      .replace(/^\s*<(strong|b)>\s*(Chính xác|Chưa đúng|Đúng|Sai)[^<]*<\/\1>/i, "")
      .replace(/^\s*<(strong|b)>[^<]{1,40}:\s*<\/\1>/i, "")
      .replace(/^\s*<(strong|b)>[^<]{1,40}<\/\1>\s*:/i, "");
    const count = (body.match(BOLD) ?? []).length;
    if (count >= 2) {
      const line = html.slice(0, start).split("\n").length;
      problems.push(`${file}:${line} <${tag}> có ${count} chỗ in đậm — "${text.slice(0, 80)}${text.length > 80 ? "…" : ""}"`);
    }
  };
  while ((m = TAG.exec(html))) {
    const [whole, closing, rawTag, attrs] = m;
    const tag = rawTag.toLowerCase();
    if (stack.length) stack[stack.length - 1].own += html.slice(last, m.index);
    last = m.index + whole.length;
    if (!closing) {
      stack.push({ tag, attrs, start: m.index, own: "" });
      continue;
    }
    // Đóng thẻ: bật tới đúng thẻ mở tương ứng; <ul>/<ol> chỉ là vách ngăn, không chấm.
    while (stack.length) {
      const frame = stack.pop()!;
      if (frame.tag === "p" || frame.tag === "li") judge(frame);
      if (frame.tag === tag) break;
    }
  }
  return problems;
}

const args = process.argv.slice(2);
const files = args.length ? args : findTheoryFiles(path.resolve("content"));
let total = 0;
for (const file of files) {
  const problems = check(file);
  total += problems.length;
  for (const p of problems) console.log(p);
}
console.log(`\n${files.length} file, ${total} đoạn in đậm từ 2 chỗ trở lên.`);
process.exit(total > 0 ? 1 : 0);
