// Gửi bài lý thuyết cho Gemini đóng vai học sinh (hoặc nhờ nháp bài tập mẫu) và tự lưu kết quả JSON
// vào đúng thư mục mà skill `chinh-ly-thuyet-theo-phan-hoi` / `soan-bai-tap-mau` đọc.
//
//   npx tsx scripts/gemini-phan-hoi.mts --bai l10-do-dich-chuyen-quang-duong --ten "Độ dịch chuyển và quãng đường đi được" [--lop 10]
//        [--vai yeu,trung-binh,kha] [--dry-run]
//   npx tsx scripts/gemini-phan-hoi.mts --che-do bai-tap-mau --bai <thư mục> --ten "<tên bài>" --lesson-id <id> [--dry-run]
//
// Hai đường gọi: (a) Gemini CLI đăng nhập tài khoản Google, không cần API key (mặc định khi thiếu GEMINI_API_KEY);
// (b) API nếu có GEMINI_API_KEY + GEMINI_MODEL trong .env.local. KHÔNG hard-code tên model
// (model bị khai tử theo thời gian, xem AGENTS.md "Gọi AI provider trong code"). Chỉ gửi nội dung bài —
// không có dữ liệu học sinh. Chạy trong tab terminal (cần mạng). Không ghi DB, chỉ ghi file.
//
// Chế độ học sinh gọi 2 lượt mỗi vai: (1) "mù" — bài đã bỏ lời giải/đáp án của các câu tự kiểm tra, vai chọn
// đáp án; (2) đọc đủ bài, nêu góp ý (có kèm đáp án lượt 1 để so). Nhờ vậy phép thử quiz có nghĩa.

import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

function envVar(key: string): string | undefined {
  if (process.env[key]) return process.env[key];
  const p = path.join(root, ".env.local");
  if (!fs.existsSync(p)) return undefined;
  const line = fs.readFileSync(p, "utf8").split("\n").find((l) => l.startsWith(`${key}=`));
  return line ? line.slice(key.length + 1).trim().replace(/^["']|["']$/g, "") : undefined;
}

function arg(name: string): string | undefined {
  const i = process.argv.indexOf(`--${name}`);
  return i >= 0 ? process.argv[i + 1] : undefined;
}
const flag = (n: string) => process.argv.includes(`--${n}`);

const mode = arg("che-do") ?? "hoc-sinh";
const bai = arg("bai");
const ten = arg("ten");
if (!bai || !ten) {
  console.error("Thiếu --bai <thư mục trong content/lesson-samples> hoặc --ten \"<tên bài>\"");
  process.exit(1);
}
const lop = arg("lop") ?? bai.match(/^l(\d+)-/)?.[1] ?? "10";
const dir = path.join(root, "content", "lesson-samples", bai);
const theoryPath = path.join(dir, "theory.html");
if (!fs.existsSync(theoryPath)) {
  console.error(`Không thấy ${theoryPath}`);
  process.exit(1);
}

// --- chuẩn bị nội dung bài gửi đi ------------------------------------------------------------
function stripHeavy(html: string): string {
  return html
    .replace(/<script[\s\S]*?<\/script>/gi, "")
    .replace(/<style[\s\S]*?<\/style>/gi, "")
    .replace(/<svg[\s\S]*?<\/svg>/gi, "[hình vẽ minh hoạ]")
    .replace(/<img[^>]*>/gi, "[ảnh]")
    .replace(/data:[a-z/+-]+;base64,[A-Za-z0-9+/=]+/g, "");
}
const full = stripHeavy(fs.readFileSync(theoryPath, "utf8"));
// bản "mù": bỏ khối phản hồi đúng/sai và mọi thuộc tính (lớp tl-ok/tl-no lộ đáp án)
const blind = full
  .replace(/<div class="tl-fb[^"]*">[\s\S]*?<\/div>/gi, "")
  .replace(/<(\w+)\s[^>]*>/g, "<$1>");

// --- lấy prompt từ file tham chiếu của skill --------------------------------------------------
const promptFile =
  mode === "bai-tap-mau"
    ? ".claude/skills/soan-bai-tap-mau/references/PROMPT-GEMINI-BAI-TAP-MAU.md"
    : ".claude/skills/cap-nhat-bai-hoc-theo-gemini/references/PROMPT-GEMINI-HOC-SINH.md";
const marker = "## PROMPT (sao chép từ đây)";
const rawMd = fs.readFileSync(path.join(root, promptFile), "utf8");
if (!rawMd.includes(marker)) {
  console.error(`Không thấy "${marker}" trong ${promptFile}`);
  process.exit(1);
}
const promptTpl = rawMd.split(marker)[1].split("\n---\n")[0].trim();
const fill = (s: string, vai = "") =>
  s.replaceAll("{TÊN BÀI}", ten).replaceAll("{LỚP}", lop).replaceAll("{VAI}", vai);

// --- gọi Gemini -------------------------------------------------------------------------------
function parseJsonText(text: string): unknown {
  const t = text.trim().replace(/^```(?:json)?\s*|\s*```$/g, "");
  const a = t.indexOf("{"), b = t.lastIndexOf("}");
  try {
    return JSON.parse(a >= 0 ? t.slice(a, b + 1) : t);
  } catch {
    throw new Error(`Gemini trả JSON hỏng: ${text.slice(0, 300)}`);
  }
}

// Không cần API key: dùng Gemini CLI đăng nhập bằng tài khoản Google (gói Pro/miễn phí). Cài một lần:
//   npm i -g @google/gemini-cli && gemini      (chọn "Login with Google", đăng nhập trên trình duyệt)
function callGeminiCli(prompt: string, bodyText: string): unknown {
  const model = envVar("GEMINI_MODEL");
  const args = ["-p", `${prompt}\n\nCHỈ IN MỘT JSON HỢP LỆ, KHÔNG DÙNG CÔNG CỤ, KHÔNG THÊM CHỮ NÀO KHÁC.`];
  if (model) args.push("-m", model);
  const r = spawnSync("gemini", args, {
    input: `=== NỘI DUNG BÀI (HTML) ===\n${bodyText}`,
    encoding: "utf8",
    maxBuffer: 64 * 1024 * 1024,
    timeout: 10 * 60 * 1000,
  });
  if (r.error) {
    throw new Error(`Không chạy được lệnh gemini (${r.error.message}). Cài: npm i -g @google/gemini-cli, chạy \`gemini\` một lần để đăng nhập Google.`);
  }
  if (r.status !== 0) throw new Error(`gemini thoát mã ${r.status}: ${(r.stderr || r.stdout).slice(0, 400)}`);
  return parseJsonText(r.stdout);
}

async function callGemini(prompt: string, bodyText: string): Promise<unknown> {
  const key = envVar("GEMINI_API_KEY");
  const model = envVar("GEMINI_MODEL");
  if (!key || !model) return callGeminiCli(prompt, bodyText); // không có API key → dùng Gemini CLI
  const url = `https://generativelanguage.googleapis.com/v1beta/models/${encodeURIComponent(model)}:generateContent`;
  for (let attempt = 1; attempt <= 3; attempt++) {
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json", "x-goog-api-key": key },
      body: JSON.stringify({
        contents: [{ role: "user", parts: [{ text: `${prompt}\n\n=== NỘI DUNG BÀI (HTML) ===\n${bodyText}` }] }],
        generationConfig: { responseMimeType: "application/json", temperature: 0.7 },
      }),
    });
    if (res.status === 429 || res.status >= 500) {
      console.warn(`  Gemini trả ${res.status}, thử lại (${attempt}/3)…`);
      await new Promise((r) => setTimeout(r, 4000 * attempt));
      continue;
    }
    const j = (await res.json()) as any;
    if (!res.ok) throw new Error(`Gemini ${res.status}: ${JSON.stringify(j).slice(0, 400)}`);
    const text: string | undefined = j.candidates?.[0]?.content?.parts?.map((p: any) => p.text ?? "").join("");
    if (!text) throw new Error(`Gemini không trả văn bản: ${JSON.stringify(j).slice(0, 400)}`);
    return parseJsonText(text);
  }
  throw new Error("Gemini lỗi sau 3 lần thử");
}

const today = new Date().toISOString().slice(0, 10);

async function main() {
  if (mode === "bai-tap-mau") {
    const id = arg("lesson-id");
    if (!id) { console.error("Thiếu --lesson-id"); process.exit(1); }
    const prompt = fill(promptTpl);
    if (flag("dry-run")) {
      console.log(`[dry-run] bai-tap-mau · prompt ${prompt.length} ký tự · bài ${full.length} ký tự`);
      return;
    }
    const out = await callGemini(prompt, full);
    const dest = path.join(dir, "gemini", "nhan");
    fs.mkdirSync(dest, { recursive: true });
    const file = path.join(dest, "bai-tap-mau.json");
    fs.writeFileSync(file, JSON.stringify(out, null, 2));
    console.log(`Đã lưu ${path.relative(root, file)}\nTiếp: python3 .claude/skills/soan-bai-tap-mau/scripts/kiem-ban-nhap-gemini.py ${path.relative(root, file)} --lesson-id ${id}`);
    return;
  }

  const vais = (arg("vai") ?? "yeu,trung-binh,kha").split(",").map((s) => s.trim());
  const dest = path.join(dir, "gemini", "nhan");
  fs.mkdirSync(dest, { recursive: true });
  for (const vai of vais) {
    const prompt = fill(promptTpl, vai);
    if (flag("xuat")) {
      // Không gọi Gemini: xuất sẵn file để thầy dán tay vào gemini.google.com (mỗi vai một cuộc chat, 2 tin nhắn)
      const out = path.join(dir, "gemini", "gui");
      fs.mkdirSync(out, { recursive: true });
      const blindIns =
        `Bạn là học sinh lớp ${lop} hồ sơ "${vai}" (yeu = nền yếu, hay quên; trung-binh = hiểu khi ví dụ rõ, hay nhầm điều kiện; kha = nắm nhanh). ` +
        `Dưới đây là bài "${ten}" đã bị ẩn lời giải/đáp án. Chỉ dựa vào bài và kiến thức lớp dưới. ` +
        `Trả lời mọi câu dự đoán và câu tự kiểm tra: ghi đáp án chọn và lí do ngắn. ` +
        `Trả về duy nhất JSON: {"tra_loi_quiz":{"du_doan":"A","cau1":"B"},"ly_do_chon":{"du_doan":"…"}}. ` +
        `Khoá của tra_loi_quiz đặt theo nhãn câu trong bài (cau1, cau2…; câu dự đoán đặt "du_doan").`;
      fs.writeFileSync(path.join(out, `${vai}-1-quiz-mu.txt`), `${blindIns}\n\n=== NỘI DUNG BÀI (HTML) ===\n${blind}`);
      fs.writeFileSync(
        path.join(out, `${vai}-2-doc-day-du.txt`),
        `${prompt}\n\nLưu ý: trong tin nhắn trước bạn đã làm quiz mù; giữ nguyên các đáp án đó trong tra_loi_quiz/ly_do_chon và chỉ góp ý thêm.\n\n=== NỘI DUNG BÀI (HTML, ĐẦY ĐỦ LỜI GIẢI) ===\n${full}`,
      );
      const btmMd = fs.readFileSync(path.join(root, ".claude/skills/soan-bai-tap-mau/references/PROMPT-GEMINI-BAI-TAP-MAU.md"), "utf8");
      const btm = fill(btmMd.split(marker)[1].split("\n---\n")[0].trim());
      fs.writeFileSync(
        path.join(out, `${vai}-3-bai-tap-mau.txt`),
        `Bây giờ thôi đóng vai học sinh. Dựa trên chính bài bạn vừa đọc (không cần gửi lại), hãy làm nhiệm vụ sau.\n\n${btm}`,
      );
      console.log(`Đã xuất ${vai} → ${path.relative(root, out)}/${vai}-1-quiz-mu.txt và ${vai}-2-doc-day-du.txt`);
      continue;
    }
    if (flag("dry-run")) {
      console.log(`[dry-run] ${vai} · prompt ${prompt.length} ký tự · bài đầy đủ ${full.length} · bản mù ${blind.length}`);
      continue;
    }
    console.log(`Vai ${vai}: lượt 1 (làm quiz mù)…`);
    const blindPrompt =
      fill(
        `Bạn là học sinh lớp {LỚP} hồ sơ "{VAI}" (yeu = nền yếu, hay quên; trung-binh = hiểu khi ví dụ rõ, hay nhầm điều kiện; kha = nắm nhanh). ` +
          `Dưới đây là bài "{TÊN BÀI}" đã bị ẩn lời giải/đáp án. Chỉ dựa vào bài và kiến thức lớp dưới. ` +
          `Trả lời mọi câu dự đoán và câu tự kiểm tra: ghi đáp án chọn và lí do ngắn. ` +
          `Trả về duy nhất JSON: {"tra_loi_quiz":{"du_doan":"A","cau1":"B"},"ly_do_chon":{"du_doan":"…"}}. ` +
          `Khoá của tra_loi_quiz đặt theo nhãn câu trong bài (cau1, cau2…; câu dự đoán đặt "du_doan").`,
        vai,
      );
    const step1 = (await callGemini(blindPrompt, blind)) as any;
    console.log(`Vai ${vai}: lượt 2 (đọc đủ + góp ý)…`);
    const withQuiz = `${prompt}\n\nLưu ý: lượt làm quiz mù của bạn đã cho kết quả sau, hãy giữ nguyên trong trường tra_loi_quiz/ly_do_chon và chỉ góp ý thêm.\n${JSON.stringify(step1)}`;
    const step2 = (await callGemini(withQuiz, full)) as any;
    step2.vai = vai;
    step2.tra_loi_quiz = step1.tra_loi_quiz ?? step2.tra_loi_quiz;
    step2.ly_do_chon = step1.ly_do_chon ?? step2.ly_do_chon;
    const file = path.join(dest, `hoc-sinh-${vai}.json`);
    fs.writeFileSync(file, JSON.stringify(step2, null, 2));
    console.log(`  → ${path.relative(root, file)} (${step2.gop_y?.length ?? 0} góp ý)`);
  }
  if (!flag("dry-run"))
    console.log(`\nTiếp: python3 .claude/skills/cap-nhat-bai-hoc-theo-gemini/scripts/gop-phan-hoi.py content/lesson-samples/${bai}`);
}

main().catch((e) => {
  console.error(e.message ?? e);
  process.exit(1);
});
