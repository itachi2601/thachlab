// Sinh 8 câu luyện tập tự chấm cho các bài HSG 9 còn thiếu bằng Message Batches (giá -50%). KHÔNG ghi DB.
//   npx tsx scripts/batch-luyen-tap-hsg9.mts nop        nộp batch soạn (8 bài) → scripts/data/luyen-tap-hsg9/state.json
//   npx tsx scripts/batch-luyen-tap-hsg9.mts thu        chờ xong → ghi content/hsg9/<cd>/luyen-tap/bundle.json (nháp, chưa đăng)
//   npx tsx scripts/batch-luyen-tap-hsg9.mts kiem       nộp batch giải độc lập (model khác, chỉ thấy đề)
//   npx tsx scripts/batch-luyen-tap-hsg9.mts thu-kiem   so đáp án giải độc lập với đáp án soạn → báo câu lệch
// Đăng (sau khi kiểm xong): npx tsx scripts/upload-lesson.mts content/hsg9/<cd>/luyen-tap/bundle.json --lesson <id> --target luyen_tap
import Anthropic from "@anthropic-ai/sdk";
import fs from "node:fs";

const L = fs.readFileSync(".env.local", "utf8").split("\n");
const key = L.find((l) => l.startsWith("ANTHROPIC_API_KEY="))!.slice(18).trim();
const anth = new Anthropic({ apiKey: key });
const DIR = "scripts/data/luyen-tap-hsg9/";
const STATE = DIR + "state.json";
const STATE_KIEM = DIR + "state-kiem.json";
const GEN_MODEL = "claude-opus-5-5";
const SOLVE_MODEL = "claude-sonnet-5-5";

const BAI: { id: number; cd: string; ten: string; topic: string }[] = [
  { id: 165, cd: "cd05-cong-suat-dien-joule-lenz", ten: "CĐ05 Công suất điện, định luật Joule–Lenz", topic: "Công suất điện và nhiệt lượng Joule–Lenz" },
  { id: 150, cd: "cd15-am-thanh", ten: "CĐ15 Âm thanh", topic: "Âm thanh" },
  { id: 160, cd: "cd00-ky-nang-nen", ten: "CĐ00 Kỹ năng nền", topic: "Kỹ năng nền" },
  { id: 161, cd: "cd01-cong-va-cong-suat", ten: "CĐ01 Công và công suất", topic: "Công và công suất" },
  { id: 166, cd: "cd02-dong-nang-the-nang-co-nang", ten: "CĐ02 Động năng, thế năng, cơ năng", topic: "Động năng, thế năng, cơ năng" },
  { id: 155, cd: "cd10-luc", ten: "CĐ10 Lực", topic: "Lực" },
  { id: 154, cd: "cd11-co-hoc-chat-luu", ten: "CĐ11 Cơ học chất lưu", topic: "Cơ học chất lưu" },
  { id: 162, cd: "cd13-chuyen-dong-va-do-thi", ten: "CĐ13 Chuyển động và đồ thị", topic: "Chuyển động và đồ thị" },
];
const pathBundle = (cd: string) => `content/hsg9/${cd}/luyen-tap/bundle.json`;

const plain = (h: string) =>
  h.replace(/<script[\s\S]*?<\/script>|<style[\s\S]*?<\/style>|<svg[\s\S]*?<\/svg>/g, " ").replace(/<[^>]+>/g, " ").replace(/&nbsp;/g, " ").replace(/\s+/g, " ").trim();

function nguon(cd: string): string {
  const d = `content/hsg9/${cd}/`;
  const f = ["nguon.md", "nguon.txt"].map((x) => d + x).find((x) => fs.existsSync(x));
  const t = f ? fs.readFileSync(f, "utf8") : plain(fs.readFileSync(d + "theory.html", "utf8"));
  return t.slice(0, 14000);
}

// Mẫu định dạng: 1 câu mỗi loại từ bài CĐ03 đã đăng.
const mau = JSON.parse(fs.readFileSync(pathBundle("cd03-dien-tro-dinh-luat-ohm"), "utf8"));
const qs = mau.exam.questions;
const MAU = JSON.stringify([qs[0], qs[4], qs[6]], null, 1);

const SYSTEM = `Bạn soạn câu luyện tập tự chấm cho khoá Vật lí HSG KHTN 9 (học sinh lớp 9 giỏi, thi HSG thành phố). Tiếng Việt, công thức LaTeX trong $...$ (dấu thập phân là {,} như "0{,}3"), dùng \\ \\text{V} cho đơn vị. g = 10 m/s². Sai số/làm tròn ghi rõ trong đề. Không chép nguyên văn sách; tự đặt số liệu mới, KHÁC ví dụ trong tài liệu nguồn.
Trả về DUY NHẤT một mảng JSON gồm đúng 8 câu: 4 câu "multiple_choice" (Phần I), 2 câu "true_false" (Phần II, đúng 4 mệnh đề a–d), 2 câu "short_answer" (Phần III, đáp số một số, dấu phẩy thập phân kiểu "0,51").
Định dạng từng loại (giữ đúng tên trường) như mẫu sau:
${MAU}
Quy tắc: multiple_choice có 4 options khác nhau, answer là chỉ số 0–3, distractorNotes là object khoá "A".."D" (trừ chữ đáp án đúng) nêu lỗi tư duy thật của từng phương án nhiễu; trải đáp án đúng ra các vị trí khác nhau. explanation là HTML (<p>…</p>), mỗi ý một thẻ <p>, có đoạn vì sao phương án khác sai / bẫy thường gặp. Mỗi câu có topic (tên dạng ngắn), form ("ly_thuyet" hoặc "bai_tap"), difficulty ("de"|"trung-binh"|"kho"); độ khó trải: 3 dễ, 3 trung bình, 2 khó. Mỗi câu đúng MỘT đáp án, đề đủ dữ kiện, không cần hình vẽ. Tự giải lại từng câu trước khi trả; đáp án phải chính xác. Không thêm chữ nào ngoài JSON.`;

const userGen = (b: (typeof BAI)[number]) =>
  `Bài: ${b.ten}.\nTài liệu nguồn của bài (dàn ý/lý thuyết, dùng để biết phạm vi và ký hiệu):\n\n${nguon(b.cd)}\n\nHãy soạn 8 câu luyện tập.`;

function jsonOf(t: string) {
  const s = t.indexOf("["), e = t.lastIndexOf("]");
  return JSON.parse(t.slice(s, e + 1));
}
function loi(q: any, i: number): string | null {
  const t = q?.type;
  if (!q?.question || !q?.explanation) return `câu ${i + 1}: thiếu đề/lời giải`;
  if (t === "multiple_choice") {
    if (!Array.isArray(q.options) || q.options.length !== 4 || new Set(q.options).size !== 4) return `câu ${i + 1}: options`;
    if (![0, 1, 2, 3].includes(q.answer)) return `câu ${i + 1}: answer`;
  } else if (t === "true_false") {
    if (!Array.isArray(q.statements) || q.statements.length !== 4 || q.statements.some((s: any) => typeof s.answer !== "boolean")) return `câu ${i + 1}: statements`;
  } else if (t === "short_answer") {
    if (typeof q.answer !== "string" || !/^-?\d+(,\d+)?$/.test(q.answer)) return `câu ${i + 1}: answer "${q.answer}"`;
  } else return `câu ${i + 1}: type ${t}`;
  return null;
}

async function cho(file: string) {
  const st = JSON.parse(fs.readFileSync(file, "utf8"));
  for (;;) {
    const b = await anth.messages.batches.retrieve(st.batch_id);
    console.log(b.processing_status, JSON.stringify(b.request_counts));
    if (b.processing_status === "ended") break;
    await new Promise((r) => setTimeout(r, 30000));
  }
  const out: Record<string, string> = {};
  const usage = { in: 0, out: 0 };
  for await (const r of await anth.messages.batches.results(st.batch_id)) {
    if (r.result.type !== "succeeded") { console.log("LỖI", r.custom_id, r.result.type); continue; }
    out[r.custom_id] = r.result.message.content.map((c: any) => c.text ?? "").join("");
    usage.in += r.result.message.usage.input_tokens; usage.out += r.result.message.usage.output_tokens;
  }
  console.log("token vào/ra:", usage.in, usage.out);
  return out;
}

const cmd = process.argv[2];
fs.mkdirSync(DIR, { recursive: true });

if (cmd === "nop") {
  if (fs.existsSync(STATE)) { console.error("Đã có", STATE, "- xoá nếu muốn nộp lại."); process.exit(1); }
  const batch = await anth.messages.batches.create({
    requests: BAI.map((b) => ({ custom_id: `b${b.id}`, params: { model: GEN_MODEL, max_tokens: 16000, system: SYSTEM, messages: [{ role: "user" as const, content: userGen(b) }] } })),
  });
  fs.writeFileSync(STATE, JSON.stringify({ batch_id: batch.id, at: new Date().toISOString() }));
  console.log("Đã nộp", BAI.length, "bài · batch", batch.id, "\nChạy: npx tsx scripts/batch-luyen-tap-hsg9.mts thu");
} else if (cmd === "thu") {
  const out = await cho(STATE);
  for (const b of BAI) {
    const raw = out[`b${b.id}`];
    if (!raw) { console.log(`✗ ${b.id} ${b.cd}: không có kết quả`); continue; }
    try {
      const arr = jsonOf(raw);
      const errs = arr.map(loi).filter(Boolean) as string[];
      if (arr.length !== 8) errs.push(`có ${arr.length} câu, cần 8`);
      if (errs.length) { fs.writeFileSync(DIR + `loi-${b.id}.txt`, raw); console.log(`✗ ${b.id}: ${errs.join("; ")} (thô: loi-${b.id}.txt)`); continue; }
      const bundle = {
        schema: "thachlab.lesson-bundle/v1", theory_html: "", worked_examples: [],
        exam: { title: `Luyện tập — ${b.ten.replace(/^CĐ\d+ /, "")}`, topic: b.topic, difficulty: "trung-binh", duration_minutes: 20, subject_code: "hsg-vat-ly", questions: arr },
      };
      fs.mkdirSync(`content/hsg9/${b.cd}/luyen-tap`, { recursive: true });
      fs.writeFileSync(pathBundle(b.cd), JSON.stringify(bundle, null, 1));
      console.log(`✓ ${b.id} ${b.cd}: 8 câu → ${pathBundle(b.cd)}`);
    } catch (e: any) { fs.writeFileSync(DIR + `loi-${b.id}.txt`, raw); console.log(`✗ ${b.id}: JSON hỏng (${e.message})`); }
  }
  console.log("Tiếp: npx tsx scripts/batch-luyen-tap-hsg9.mts kiem");
} else if (cmd === "kiem") {
  if (fs.existsSync(STATE_KIEM)) { console.error("Đã có", STATE_KIEM, "- xoá nếu muốn nộp lại."); process.exit(1); }
  const reqs: any[] = [];
  for (const b of BAI) {
    if (!fs.existsSync(pathBundle(b.cd))) continue;
    const qq = JSON.parse(fs.readFileSync(pathBundle(b.cd), "utf8")).exam.questions;
    qq.forEach((q: any, i: number) => {
      const de = q.type === "true_false" ? { question: q.question, statements: q.statements.map((s: any) => s.text) } : q.type === "multiple_choice" ? { question: q.question, options: q.options } : { question: q.question };
      reqs.push({
        custom_id: `b${b.id}c${i}`,
        params: {
          model: SOLVE_MODEL, max_tokens: 6000,
          system: "Bạn là giáo viên Vật lí giải đề độc lập. g = 10 m/s². Giải cẩn thận từng bước rồi kết thúc bằng đúng một dòng: ĐÁP ÁN: <kết quả>. Với trắc nghiệm: một chữ A/B/C/D. Với đúng–sai: bốn chữ Đ hoặc S cho a,b,c,d, ví dụ ĐÁP ÁN: Đ S S Đ. Với đáp số: một số, dấu phẩy thập phân.",
          messages: [{ role: "user", content: JSON.stringify(de) }],
        },
      });
    });
  }
  if (!reqs.length) { console.error("Chưa có bundle.json nào — đợi `thu` in dòng ✓ cho các bài rồi chạy lại."); process.exit(1); }
  const batch = await anth.messages.batches.create({ requests: reqs });
  fs.writeFileSync(STATE_KIEM, JSON.stringify({ batch_id: batch.id, n: reqs.length, at: new Date().toISOString() }));
  console.log("Đã nộp", reqs.length, "câu giải độc lập · batch", batch.id, "\nChạy: npx tsx scripts/batch-luyen-tap-hsg9.mts thu-kiem");
} else if (cmd === "thu-kiem") {
  const out = await cho(STATE_KIEM);
  const chuan = (s: string) => s.replace(/\s+/g, "").replace(/\./g, ",").toUpperCase();
  let lech = 0, tong = 0;
  for (const b of BAI) {
    if (!fs.existsSync(pathBundle(b.cd))) continue;
    const qq = JSON.parse(fs.readFileSync(pathBundle(b.cd), "utf8")).exam.questions;
    qq.forEach((q: any, i: number) => {
      const raw = out[`b${b.id}c${i}`]; tong++;
      const m = raw && [...raw.matchAll(/ĐÁP ÁN:\s*(.+)/g)].pop();
      const got = m ? chuan(m[1]) : "";
      const exp = q.type === "multiple_choice" ? "ABCD"[q.answer] : q.type === "true_false" ? q.statements.map((s: any) => (s.answer ? "Đ" : "S")).join("").toUpperCase() : chuan(q.answer);
      const g = q.type === "true_false" ? got.replace(/[^ĐS]/g, "") : q.type === "multiple_choice" ? got.replace(/[^ABCD]/g, "").slice(0, 1) : got.replace(/[^0-9,\-]/g, "");
      if (g !== exp) { lech++; console.log(`LỆCH ${b.id} câu ${i + 1} (${q.type}): soạn=${exp} · giải độc lập=${g || "?"}`); }
    });
  }
  console.log(`\nKhớp ${tong - lech}/${tong}. Câu lệch: để agent kiem-code giải lại tay rồi sửa bundle.json.`);
} else console.log("Dùng: nop | thu | kiem | thu-kiem");
