// CHỈ ĐỌC. Ánh xạ content/lesson-samples/{l9,l10,l11,l12}-*/ → lesson_id (theo bundle.target: lớp + tên bài)
// và so mục Lý thuyết trong DB với (a) bản file TRƯỚC khi chuyển hệ khung, (b) bản file hiện tại.
//   npx tsx scripts/anh-xa-bai-ly-thuyet.mts            → in bảng + ghi scripts/logs/anh-xa-bai-ly-thuyet.json
// Trạng thái: AN_TOAN (DB == bản cũ, ghi đè không mất gì) · DA_GHI (DB == bản mới) · KHAC (DB lệch cả hai, phải xem tay) · KHONG_THAY/TRUNG.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { chuanHoaNgoaiVideo } from "./lib/video-html";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
function env(key: string): string | undefined {
  if (process.env[key]) return process.env[key];
  const p = path.join(root, ".env.local");
  if (!fs.existsSync(p)) return undefined;
  const l = fs.readFileSync(p, "utf8").split("\n").find((x) => x.startsWith(`${key}=`));
  return l ? l.slice(key.length + 1).trim() : undefined;
}
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL")!, env("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });

const COMMIT_DAU: Record<string, string> = { "l11-mo-ta-song": "ac2ea1c85", "l11-": "40a3c958f", "l12-": "7ec7c248b", "l10-": "30b0301f2", "l9-": "30b0301f2" };
const bo = (s: string) => s.normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/đ/g, "d").replace(/Đ/g, "D").toLowerCase()
  .replace(/^\s*bai\s*\d+\s*[.:]\s*/, "").replace(/[^a-z0-9]+/g, " ").trim();
const soLop = (s: string) => (s.match(/(\d+)\s*$/) ?? [])[1];
const norm = (s: string) => chuanHoaNgoaiVideo(s ?? "").replace(/\s+/g, "");
function cu(slug: string): string | null {
  if (slug === "l11-bai-tap-song") return null;
  const c = COMMIT_DAU[slug] ?? COMMIT_DAU[Object.keys(COMMIT_DAU).find((k) => k.endsWith("-") && slug.startsWith(k))!];
  try { return execFileSync("git", ["show", `${c}^:content/lesson-samples/${slug}/theory.html`], { cwd: root, encoding: "utf8", maxBuffer: 1 << 26 }); } catch { return null; }
}

const { data: classes } = await sb.from("classes").select("id,name");
const { data: chapters } = await sb.from("chapter_classes").select("chapter_id,class_id");
const { data: lessons } = await sb.from("lessons").select("id,title,chapter_id");
const { data: items } = await sb.from("lesson_items").select("id,lesson_id,body_html").eq("kind", "ly_thuyet");
const classesOf = new Map<number, number[]>();
for (const c of chapters!) classesOf.set(c.chapter_id, [...(classesOf.get(c.chapter_id) ?? []), c.class_id]);
const itemOf = new Map(items!.map((i) => [i.lesson_id, i]));

const base = path.join(root, "content/lesson-samples");
const out: Record<string, unknown>[] = [];
for (const slug of fs.readdirSync(base).filter((d) => /^(l9|l10|l11|l12)-/.test(d)).sort()) {
  const dir = path.join(base, slug);
  const b = JSON.parse(fs.readFileSync(path.join(dir, "bundle.json"), "utf8"));
  const cls = classes!.filter((c) => soLop(c.name) === soLop(b.target.class_name)).map((c) => c.id);
  const cand = lessons!.filter((l) => bo(l.title) === bo(b.target.lesson_title) && (classesOf.get(l.chapter_id) ?? []).some((x) => cls.includes(x)));
  if (cand.length !== 1) { out.push({ slug, id: null, tt: cand.length ? "TRUNG" : "KHONG_THAY", target: b.target, cand: cand.map((c) => c.id) }); continue; }
  const id = cand[0].id; const it = itemOf.get(id);
  if (!it) { out.push({ slug, id, tt: "KHONG_CO_MUC_LY_THUYET" }); continue; }
  const moi = fs.readFileSync(path.join(dir, "theory.html"), "utf8");
  const c = cu(slug);
  const db = norm(it.body_html);
  let tt = db === norm(moi) ? "DA_GHI" : c && db === norm(c) ? "AN_TOAN" : "KHAC";
  let phienBan = "";
  if (tt === "KHAC") { // thử mọi bản lịch sử của file: DB trùng bản cũ nào thì ghi đè vẫn an toàn (chỉ mất bản mới hơn của chính file này)
    const hs = execFileSync("git", ["log", "--format=%h", "--", `content/lesson-samples/${slug}/theory.html`], { cwd: root, encoding: "utf8" }).split("\n").filter(Boolean);
    for (const h of hs) { try { const v = execFileSync("git", ["show", `${h}:content/lesson-samples/${slug}/theory.html`], { cwd: root, encoding: "utf8", maxBuffer: 1 << 26 }); if (db === norm(v)) { tt = "AN_TOAN_BAN_CU"; phienBan = h; break; } } catch { /* bỏ qua */ } }
  }
  out.push({ slug, id, tt, phienBan, dbLen: it.body_html?.length ?? 0, moiLen: moi.length, cuLen: c?.length ?? null });
}
fs.mkdirSync(path.join(root, "scripts/logs"), { recursive: true });
fs.writeFileSync(path.join(root, "scripts/logs/anh-xa-bai-ly-thuyet.json"), JSON.stringify(out, null, 1));
const dem: Record<string, number> = {};
for (const r of out) { dem[r.tt as string] = (dem[r.tt as string] ?? 0) + 1; if (r.tt !== "AN_TOAN") console.log(r.tt, r.slug, r.id ?? "", JSON.stringify(r.cand ?? "")); }
console.log("Tổng", out.length, dem);
