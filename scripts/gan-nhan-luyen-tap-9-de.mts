// Gắn nhãn topic (YCCĐ) / difficulty / form cho từng câu của 9 đề Luyện tập sinh từ bài tập mẫu/thực hành (15/10/2026)
// để /luyen-tap hiện bộ lọc Phần muốn luyện + Mức độ. Chỉ đụng exams.questions[*].topic/difficulty/form của đúng 9 đề.
//   npx tsx scripts/gan-nhan-luyen-tap-9-de.mts                  # DRY-RUN: in bảng nhãn, kiểm số câu + tên YCCĐ có trong question_topics
//   npx tsx scripts/gan-nhan-luyen-tap-9-de.mts --apply          # sao lưu nguyên văn ra scripts/logs/ rồi ghi, đọc lại đối chiếu
//   npx tsx scripts/gan-nhan-luyen-tap-9-de.mts --undo <backup>  # ghi lại cột questions từ file sao lưu
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
function env(key: string): string | undefined {
  const line = fs.readFileSync(path.resolve(scriptDir, "..", ".env.local"), "utf8").split("\n").find((l) => l.startsWith(`${key}=`));
  return line ? line.slice(key.length + 1).trim() : undefined;
}
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL")!, env("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });
const APPLY = process.argv.includes("--apply");
const UNDO = process.argv.includes("--undo") ? process.argv[process.argv.indexOf("--undo") + 1] : null;
const logs = path.join(scriptDir, "logs");

type D = "de" | "trung-binh" | "kho";
type F = "ly_thuyet" | "bai_tap";
type L = [topic: string, difficulty: D, form: F];

// YCCĐ lấy đúng tên con trong question_topics của bài lý thuyết cùng chương (bài thực hành/bài tập không có YCCĐ riêng).
const T = {
  tesla: "Cảm ứng từ và đơn vị tesla",
  khung: "Lực từ tác dụng lên khung dây. Ngẫu lực từ",
  tayTrai: "Quy tắc bàn tay trái, xác định phương chiều lực từ",
  bil: "Tính lực từ F = BIl·sinθ",
  dl2: "Định luật 2 Newton — bài toán động lực học",
  day: "Lực căng dây — hệ vật nối dây, ròng rọc",
  maSat: "Lực ma sát nghỉ, ma sát trượt và hệ số ma sát",
  nghieng: "Vật trượt trên mặt phẳng nghiêng có ma sát",
  tongHop: "Tổng hợp hai lực đồng quy",
  canBang: "Điều kiện cân bằng của chất điểm",
  moment: "Moment lực và quy tắc moment",
  dacTrung: "Li độ, biên độ, chu kì, tần số, pha ban đầu",
  ptdd: "Viết phương trình dao động điều hoà",
  vaX: "Công thức vận tốc, gia tốc theo li độ",
  wdWt: "Động năng, thế năng của vật dao động",
  baoToan: "Bảo toàn cơ năng trong dao động điều hoà",
  songCoBan: "Bước sóng, chu kì, tần số, tốc độ truyền sóng",
  dacTrungAm: "Đặc trưng vật lí và sinh lí của âm",
  ohm: "Định luật Ohm cho một điện trở",
  rDay: "Điện trở phụ thuộc kích thước và vật liệu dây dẫn",
  rtd: "Điện trở tương đương của đoạn mạch",
  uiHonHop: "Tính U, I trong mạch hỗn hợp",
  dienNang: "Tính điện năng tiêu thụ và tiền điện",
  congSuat: "Công suất điện của dụng cụ và số ghi trên thiết bị",
};

const LABELS: Record<number, L[]> = {
  // L12 Bài 11. Thực hành đo độ lớn cảm ứng từ
  903: [
    [T.khung, "de", "ly_thuyet"],
    [T.tayTrai, "trung-binh", "ly_thuyet"],
    [T.khung, "kho", "ly_thuyet"],
    [T.tesla, "trung-binh", "bai_tap"],
    [T.bil, "kho", "bai_tap"],
  ],
  // L10 Bài 20. Ví dụ giải bài toán động lực học
  904: [
    [T.maSat, "kho", "bai_tap"],
    [T.nghieng, "trung-binh", "bai_tap"],
    [T.day, "trung-binh", "ly_thuyet"],
    [T.nghieng, "de", "ly_thuyet"],
    [T.nghieng, "trung-binh", "ly_thuyet"],
    [T.dl2, "kho", "ly_thuyet"],
    [T.maSat, "trung-binh", "bai_tap"],
  ],
  // L10 Bài 22. Thực hành: Tổng hợp lực
  905: [
    [T.canBang, "trung-binh", "ly_thuyet"],
    [T.tongHop, "de", "bai_tap"],
    [T.tongHop, "kho", "bai_tap"],
    [T.tongHop, "kho", "ly_thuyet"],
    [T.tongHop, "trung-binh", "bai_tap"],
    [T.canBang, "de", "ly_thuyet"],
    [T.tongHop, "trung-binh", "ly_thuyet"],
    [T.moment, "trung-binh", "ly_thuyet"],
  ],
  // L11 Bài 4. Bài tập về dao động điều hoà
  906: [
    [T.dacTrung, "trung-binh", "ly_thuyet"],
    [T.vaX, "de", "bai_tap"],
    [T.ptdd, "trung-binh", "bai_tap"],
    [T.dacTrung, "trung-binh", "bai_tap"],
    [T.dacTrung, "kho", "bai_tap"],
  ],
  // L11 Bài 7. Bài tập về sự chuyển hoá năng lượng trong dao động điều hoà
  907: [
    [T.wdWt, "de", "bai_tap"],
    [T.wdWt, "trung-binh", "bai_tap"],
    [T.wdWt, "trung-binh", "ly_thuyet"],
    [T.baoToan, "trung-binh", "bai_tap"],
    [T.baoToan, "kho", "bai_tap"],
  ],
  // L11 Bài 10. Thực hành: Đo tần số của sóng âm
  908: [
    [T.songCoBan, "de", "bai_tap"],
    [T.dacTrungAm, "trung-binh", "bai_tap"],
    [T.dacTrungAm, "kho", "bai_tap"],
    [T.dacTrungAm, "trung-binh", "bai_tap"],
    [T.dacTrungAm, "trung-binh", "bai_tap"],
  ],
  // KHTN 9 Bài 11. Điện trở. Định luật Ohm
  911: [
    [T.ohm, "de", "bai_tap"],
    [T.ohm, "kho", "ly_thuyet"],
    [T.rDay, "de", "bai_tap"],
    [T.ohm, "de", "ly_thuyet"],
    [T.ohm, "trung-binh", "ly_thuyet"],
    [T.ohm, "trung-binh", "ly_thuyet"],
    [T.rDay, "trung-binh", "bai_tap"],
  ],
  // KHTN 9 Bài 12. Đoạn mạch nối tiếp, song song
  912: [
    [T.uiHonHop, "kho", "ly_thuyet"],
    [T.uiHonHop, "trung-binh", "bai_tap"],
    [T.rtd, "trung-binh", "bai_tap"],
    [T.uiHonHop, "de", "ly_thuyet"],
    [T.rtd, "de", "bai_tap"],
    [T.uiHonHop, "de", "ly_thuyet"],
    [T.uiHonHop, "kho", "bai_tap"],
  ],
  // KHTN 9 Bài 13. Năng lượng của dòng điện và công suất điện
  913: [
    [T.congSuat, "kho", "ly_thuyet"],
    [T.congSuat, "de", "bai_tap"],
    [T.dienNang, "trung-binh", "bai_tap"],
    [T.congSuat, "de", "ly_thuyet"],
    [T.dienNang, "trung-binh", "bai_tap"],
    [T.congSuat, "kho", "ly_thuyet"],
    [T.dienNang, "trung-binh", "bai_tap"],
  ],
};
const IDS = Object.keys(LABELS).map(Number);

type Q = Record<string, unknown>;
const strip = (s: unknown) => String(s ?? "").replace(/<[^>]+>/g, "").replace(/\s+/g, " ").slice(0, 70);

async function main() {
  if (UNDO) {
    const bak: { id: number; questions: Q[] }[] = JSON.parse(fs.readFileSync(UNDO, "utf8"));
    for (const b of bak) {
      const { error } = await sb.from("exams").update({ questions: b.questions }).eq("id", b.id);
      console.log(error ? `✗ ${b.id}: ${error.message}` : `↩ ${b.id} đã khôi phục`);
    }
    return;
  }

  const { data: exams, error } = await sb.from("exams").select("id,title,questions").in("id", IDS);
  if (error) throw error;
  const names = [...new Set(Object.values(T))];
  const { data: topics, error: e2 } = await sb.from("question_topics").select("name").in("name", names);
  if (e2) throw e2;
  const known = new Set((topics ?? []).map((t) => t.name));
  const problems: string[] = names.filter((n) => !known.has(n)).map((n) => `YCCĐ không có trong question_topics: ${n}`);

  const next: { id: number; questions: Q[] }[] = [];
  for (const id of IDS) {
    const ex = exams?.find((e) => e.id === id);
    if (!ex) { problems.push(`${id}: không thấy đề`); continue; }
    const qs = ex.questions as Q[];
    const lab = LABELS[id];
    if (qs.length !== lab.length) { problems.push(`${id}: đề có ${qs.length} câu, bảng nhãn ${lab.length}`); continue; }
    console.log(`\n=== ${id} ${ex.title}`);
    const out = qs.map((q, i) => {
      const [topic, difficulty, form] = lab[i];
      for (const k of ["topic", "difficulty"] as const)
        if (q[k] && q[k] !== lab[i][k === "topic" ? 0 : 1]) problems.push(`${id} câu ${i + 1}: đã có ${k}="${q[k]}", không ghi đè`);
      console.log(`  ${String(i + 1).padStart(2)} | ${difficulty.padEnd(10)} | ${form.padEnd(9)} | ${topic} | ${strip(q.question)}`);
      return { ...q, topic, difficulty, form };
    });
    next.push({ id, questions: out });
  }

  if (problems.length) { console.log("\n✗ DỪNG:\n  " + problems.join("\n  ")); process.exit(1); }
  if (!APPLY) { console.log(`\nDRY-RUN: ${next.length} đề sẵn sàng. Thêm --apply để ghi.`); return; }

  fs.mkdirSync(logs, { recursive: true });
  const bakFile = path.join(logs, `gan-nhan-luyen-tap-9-de-backup-${Date.now()}.json`);
  fs.writeFileSync(bakFile, JSON.stringify(exams!.map((e) => ({ id: e.id, questions: e.questions })), null, 1));
  console.log(`\nSao lưu: ${bakFile}`);
  for (const n of next) {
    const { error: e3 } = await sb.from("exams").update({ questions: n.questions }).eq("id", n.id);
    if (e3) { console.log(`✗ ${n.id}: ${e3.message} — dừng`); process.exit(1); }
  }
  // Đọc lại đối chiếu: đủ nhãn, phần còn lại của câu không đổi.
  const { data: after } = await sb.from("exams").select("id,questions").in("id", IDS);
  let bad = 0;
  for (const n of next) {
    const a = after?.find((e) => e.id === n.id)?.questions as Q[] | undefined;
    // jsonb tự sắp lại khoá nên so theo từng khoá, không so chuỗi JSON. Trigger DB tự thêm difficultySource: null
    // vào mỗi câu, nên chỉ so các khoá script đã gửi.
    const same = (x: Q, y: Q) => Object.keys(y).every((k) => JSON.stringify(x[k]) === JSON.stringify(y[k]));
    if (!a || a.length !== n.questions.length || a.some((q, i) => !same(q, n.questions[i]))) { bad++; console.log(`✗ ${n.id}: đọc lại lệch`); }
  }
  console.log(bad ? `✗ ${bad} đề lệch — hoàn tác: --undo ${bakFile}` : `✓ Đã ghi và đọc lại khớp ${next.length} đề.`);
  if (bad) process.exit(1);
}
main().catch((e) => { console.error(e); process.exit(1); });
