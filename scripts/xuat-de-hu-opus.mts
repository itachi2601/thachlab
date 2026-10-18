// Xuất câu "đề hư" (lint_flags còn cờ) thành lô cho agent Opus sửa đề + viết lời giải.
//   npx tsx scripts/xuat-de-hu-opus.mts [soCau/lo=40] → scripts/data/giai-lai/de-hu/lo-NN.json (+ HUONG-DAN.md)
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import { activeLintFlags } from "../lib/question-lint";
import { dbAnswer } from "./lib/giai-lai-chung.mts";
const L = fs.readFileSync(".env.local", "utf8").split("\n");
const env = (k: string) => L.find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const N = Number(process.argv[2] ?? 40), OUT = "scripts/data/giai-lai/de-hu/"; fs.mkdirSync(OUT, { recursive: true });
const ids: number[] = JSON.parse(fs.readFileSync("scripts/data/gon-ngan-hang/de-hu.json", "utf8")).map((x: any) => x.id);
const rows: any[] = [];
for (let i = 0; i < ids.length; i += 100) { let d: any; for (let t = 0; t < 5; t++) { const r = await sb.from("question_bank").select("id,grade,topic_name,archived,question").in("id", ids.slice(i, i + 100)); if (!r.error) { d = r.data; break; } await new Promise((s) => setTimeout(s, 2000)); } if (!d) throw new Error("timeout"); rows.push(...d); }
const out = rows.filter((r) => !r.archived).sort((a, b) => a.id - b.id).map((r) => ({
  id: r.id, lop: r.grade, chu_de: r.topic_name, loi: activeLintFlags(r.question, r.question.type).map((f) => ({ ma: f.code, cho: f.ctx })), dap_an_db: dbAnswer(r.question), cau_hoi: r.question }));
for (let i = 0; i * N < out.length; i++) fs.writeFileSync(OUT + `lo-${String(i + 1).padStart(2, "0")}.json`, JSON.stringify(out.slice(i * N, (i + 1) * N), null, 1));
const c: Record<string, number> = {}; out.forEach((o) => o.loi.forEach((l) => (c[l.ma] = (c[l.ma] ?? 0) + 1)));
console.log(out.length, "câu →", Math.ceil(out.length / N), "lô", c);
