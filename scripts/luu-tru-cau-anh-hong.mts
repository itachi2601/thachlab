// Lưu trữ (archived=true) các câu ngân hàng thầy chốt bỏ sau đợt kiểm ảnh 10/10/2026: ảnh mất/hỏng không cứu được,
// câu trùng sau khi thay ảnh bằng LaTeX, và 2 đồ thị không vẽ lại. Chỉ ẩn khỏi ngân hàng; đề đã đăng giữ nguyên.
//   npx tsx scripts/luu-tru-cau-anh-hong.mts          # chỉ in
//   npx tsx scripts/luu-tru-cau-anh-hong.mts --ghi    # ghi (ghi sao lưu trạng thái cũ ra scripts/logs/)
// Hoàn tác: đặt lại archived/note từ file sao lưu.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const IDS = [
  // thầy ghi "bỏ câu này" / "mất hình bỏ" khi kiểm mắt (25)
  568879, 596117, 596511, 610076, 611997, 612023, 613728, 623866, 625686, 634945, 659149, 668682, 670997, 671596, 671614, 672522,
  672605, 672648, 672664, 680835, 1176184, 1192678, 1192686, 1192688, 1192693,
  // trùng câu đã thay công thức (giữ #684056 và #1191945)
  1246425, 1254950,
  // đồ thị không vẽ lại
  523830, 674785,
];
const ghi = process.argv.includes("--ghi");
const env = (k: string) => process.env[k] ?? fs.readFileSync(path.resolve(scriptDir, "..", ".env.local"), "utf8").split("\n").find((l) => l.startsWith(`${k}=`))?.slice(k.length + 1).trim();
const supabase = createClient(env("NEXT_PUBLIC_SUPABASE_URL")!, env("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });
const { data, error } = await supabase.from("question_bank").select("id, archived, note").in("id", IDS);
if (error) { console.error(error.message); process.exit(1); }
console.log(`${data!.length}/${IDS.length} câu tìm thấy; đã lưu trữ sẵn: ${data!.filter((r) => r.archived).length}`);
if (!ghi) process.exit(0);
fs.mkdirSync(path.join(scriptDir, "logs"), { recursive: true });
fs.writeFileSync(path.join(scriptDir, "logs", `luu-tru-anh-hong-sao-luu-${new Date().toISOString().replace(/[:.]/g, "-")}.json`), JSON.stringify(data, null, 1));
const { error: e2, count } = await supabase.from("question_bank").update({ archived: true, note: "Lưu trữ 10/10/2026: ảnh hỏng/mất hoặc câu trùng sau khi thay ảnh công thức" }, { count: "exact" }).in("id", IDS);
console.log(e2 ? `LỖI ${e2.message}` : `đã lưu trữ ${count} câu`);
