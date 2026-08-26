// Nạp 12 ngân hàng câu hỏi CNC (trước đây viết cứng trong services/cnc-lms.ts và
// data/cnc/*.json) vào bảng `exams`, mỗi ngân hàng gắn 1 cnc_key duy nhất.
//
// App này export tĩnh (next.config output: "export"), không có server Node.js ở production
// nên không thể có API route dùng service role key. Script này CHỈ chạy cục bộ trên máy bạn,
// SAU KHI đã chạy docs/supabase-migration-cnc-exam-bank.sql:
//
//   SUPABASE_SERVICE_ROLE_KEY=xxx NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co node scripts/seed-cnc-exam-bank.mjs
//
// Lấy SUPABASE_SERVICE_ROLE_KEY ở Supabase Dashboard → Settings → API → service_role
// (secret, KHÔNG commit, KHÔNG đưa vào .env.local dùng chung với NEXT_PUBLIC_*, KHÔNG dán vào chat).
//
// Chạy lại an toàn nhiều lần (upsert theo cnc_key) — chỉ ghi đè các ngân hàng chưa từng
// được sửa qua trang quản trị "Ngân hàng câu hỏi CNC" kể từ lần chạy trước, nên nếu bạn đã
// cập nhật một ngân hàng qua LaTeX rồi thì đừng chạy lại script này cho ngân hàng đó nữa.

import fs from "node:fs";
import { fileURLToPath } from "node:url";
import { createClient } from "@supabase/supabase-js";

const SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL;
const SERVICE_ROLE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY;
if (!SUPABASE_URL || !SERVICE_ROLE_KEY) {
  console.error("Thiếu NEXT_PUBLIC_SUPABASE_URL hoặc SUPABASE_SERVICE_ROLE_KEY trong biến môi trường.");
  process.exit(1);
}

const seedPath = fileURLToPath(new URL("./data/cnc-exam-bank-seed.json", import.meta.url));
const banks = JSON.parse(fs.readFileSync(seedPath, "utf8"));

const supabase = createClient(SUPABASE_URL, SERVICE_ROLE_KEY);

const { data, error } = await supabase
  .from("exams")
  .upsert(banks, { onConflict: "cnc_key" })
  .select("cnc_key, id");

if (error) {
  console.error("Lỗi khi nạp ngân hàng câu hỏi CNC:", error.message);
  process.exit(1);
}

console.log(`Đã nạp ${data.length} ngân hàng câu hỏi CNC:`);
for (const row of data) console.log(`  - ${row.cnc_key} (exam id ${row.id})`);
