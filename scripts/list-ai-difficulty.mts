// Liệt kê các câu trong ngân hàng đã được AI gắn mức độ (difficulty_source = 'ai').
// CHỈ ĐỌC — không ghi gì vào DB. Dùng để soi lại kết quả backfill trước khi chạy hết.
//
//   npx tsx scripts/list-ai-difficulty.mts            # in ra màn hình
//   npx tsx scripts/list-ai-difficulty.mts --csv      # xuất scripts/data/ai-difficulty.csv
//
// Cần .env.local có NEXT_PUBLIC_SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY.

import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { questionTextForAi } from "@/services/exam-question-text";
import type { ExamQuestion } from "@/features/exams/types";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const LABEL: Record<string, string> = { de: "Dễ", "trung-binh": "Trung bình", kho: "Khó" };

function readEnvLocal(key: string): string | undefined {
  const p = path.resolve(scriptDir, "..", ".env.local");
  if (!fs.existsSync(p)) return undefined;
  const line = fs.readFileSync(p, "utf8").split("\n").find((l) => l.startsWith(`${key}=`));
  return line ? line.slice(key.length + 1).trim() : undefined;
}

async function main() {
  const asCsv = process.argv.includes("--csv");
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL ?? readEnvLocal("NEXT_PUBLIC_SUPABASE_URL");
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY ?? readEnvLocal("SUPABASE_SERVICE_ROLE_KEY");
  if (!url || !key) { console.error("Thiếu NEXT_PUBLIC_SUPABASE_URL hoặc SUPABASE_SERVICE_ROLE_KEY trong .env.local"); process.exit(1); }

  const supabase = createClient(url, key, { auth: { autoRefreshToken: false, persistSession: false } });
  const { data, error } = await supabase
    .from("question_bank")
    .select("id, difficulty, question")
    .eq("difficulty_source", "ai")
    .order("id", { ascending: false })
    .limit(500);
  if (error) { console.error("Lỗi đọc:", error.message); process.exit(1); }

  const rows = (data ?? []) as { id: number; difficulty: string; question: ExamQuestion }[];
  const dem: Record<string, number> = { de: 0, "trung-binh": 0, kho: 0 };
  for (const r of rows) dem[r.difficulty] = (dem[r.difficulty] ?? 0) + 1;

  console.log(`\nTổng ${rows.length} câu do AI gắn.`);
  console.log(`Phân bố: Dễ ${dem.de} · Trung bình ${dem["trung-binh"]} · Khó ${dem.kho}\n`);

  if (asCsv) {
    const esc = (s: string) => `"${s.replace(/"/g, '""')}"`;
    const csv = ["id,muc_do,de_bai", ...rows.map((r) => [r.id, esc(LABEL[r.difficulty] ?? r.difficulty), esc(questionTextForAi(r.question).replace(/\s+/g, " ").trim())].join(","))].join("\n");
    const out = path.resolve(scriptDir, "data", "ai-difficulty.csv");
    fs.mkdirSync(path.dirname(out), { recursive: true });
    fs.writeFileSync(out, "﻿" + csv, "utf8");
    console.log(`Đã ghi ${out}`);
    return;
  }

  for (const r of rows) {
    const txt = questionTextForAi(r.question).replace(/\s+/g, " ").trim();
    console.log(`#${r.id} [${LABEL[r.difficulty] ?? r.difficulty}]`);
    console.log(`  ${txt.slice(0, 260)}${txt.length > 260 ? "…" : ""}\n`);
  }
}

main().catch((e) => { console.error(e instanceof Error ? e.message : String(e)); process.exit(1); });
