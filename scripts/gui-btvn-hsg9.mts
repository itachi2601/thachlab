// Gửi kế hoạch tự học tuần + BTVN cho lớp HSG Vật lí 9 (class 19) từ scripts/data/btvn-hsg9/tuan.json.
// Ghi class_announcements kind='homework' → trigger DB tự đẩy chuông cho học sinh và phụ huynh đã nối.
// Mặc định DRY-RUN, chỉ in nội dung. CHẠY TRÊN MAC (cần service role).
//   npx tsx scripts/gui-btvn-hsg9.mts                # liệt kê các tuần + trạng thái
//   npx tsx scripts/gui-btvn-hsg9.mts --buoi 3       # xem trước bản tin cho buổi 3 (24/10)
//   npx tsx scripts/gui-btvn-hsg9.mts --buoi 3 --yes # gửi thật
//   npx tsx scripts/gui-btvn-hsg9.mts --next [--yes] # tuần có gui_ngay gần nhất chưa gửi
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const plan = JSON.parse(fs.readFileSync(path.join(root, "scripts/data/btvn-hsg9/tuan.json"), "utf8"));
const args = process.argv.slice(2);
const yes = args.includes("--yes");
const buoiArg = args.includes("--buoi") ? Number(args[args.indexOf("--buoi") + 1]) : null;

function envLocal(key: string): string {
  const line = fs.readFileSync(path.join(root, ".env.local"), "utf8").split("\n").find((l) => l.startsWith(`${key}=`));
  if (!line) throw new Error(`thiếu ${key} trong .env.local`);
  return line.slice(key.length + 1).trim();
}
const sb = createClient(envLocal("NEXT_PUBLIC_SUPABASE_URL"), envLocal("SUPABASE_SERVICE_ROLE_KEY"));

const tag = (t: { buoi: number }) => `[HSG9 · Buổi ${t.buoi}]`;

const { data: sent } = await sb.from("class_announcements").select("body").eq("class_id", plan.class_id).eq("kind", "homework").like("body", "[HSG9 · Buổi %");
const isSent = (t: { buoi: number }) => (sent ?? []).some((r) => r.body.startsWith(tag(t)));

const { data: lessons } = await sb.from("lessons").select("id,title,published").in("id", plan.tuan.flatMap((t: any) => t.lessons));
const byId = new Map((lessons ?? []).map((l) => [l.id, l]));

function build(t: any): string {
  const out: string[] = [`${tag(t)} Kế hoạch tự học trước buổi thứ Bảy ${t.ngay}`, `Chủ đề: ${t.chu_de}`, ""];
  const open = t.lessons.filter((id: number) => byId.get(id)?.published);
  const soon = t.lessons.filter((id: number) => byId.has(id) && !byId.get(id)!.published);
  if (open.length) {
    out.push("Bài trên web:");
    for (const id of open) out.push(`- ${byId.get(id)!.title}: /lop-hoc/bai/?id=${id}`);
  }
  if (soon.length) out.push(`(Sắp mở: ${soon.map((id: number) => `bài ${id}`).join(", ")}. Thầy sẽ báo khi mở.)`);
  if (open.length || soon.length) out.push("");
  out.push("Lịch tự học trong tuần (khoảng 1 giờ mỗi ngày):");
  for (const [ngay, viec] of t.tu_hoc) out.push(`- ${ngay}: ${viec}`);
  out.push("", `Bài tập về nhà: ${t.btvn}`, "", "Quy tắc: giải ra giấy trước rồi mới nhập đáp số lên web. Sai ý nào ghi vào sổ lỗi.");
  return out.join("\n");
}

if (buoiArg === null && !args.includes("--next")) {
  for (const t of plan.tuan) console.log(`Buổi ${t.buoi} · T7 ${t.ngay} · gửi ${t.gui_ngay} · ${isSent(t) ? "ĐÃ GỬI" : "chưa gửi"} · ${t.chu_de}`);
  process.exit(0);
}

const t = args.includes("--next")
  ? plan.tuan.filter((x: any) => !isSent(x)).sort((a: any, b: any) => a.gui_ngay.localeCompare(b.gui_ngay))[0]
  : plan.tuan.find((x: any) => x.buoi === buoiArg);
if (!t) throw new Error("không tìm thấy tuần cần gửi");
if (isSent(t)) { console.log(`Buổi ${t.buoi}: đã gửi rồi, bỏ qua.`); process.exit(0); }

const body = build(t);
console.log(`\n${yes ? "GỬI" : "XEM TRƯỚC"} · lớp ${plan.class_id} · dự kiến gửi ngày ${t.gui_ngay}\n${"-".repeat(40)}\n${body}\n${"-".repeat(40)}`);
if (!yes) { console.log("DRY-RUN: thêm --yes để gửi."); process.exit(0); }

const { data: admin } = await sb.from("profiles").select("id").eq("role", "admin").order("created_at").limit(1).single();
if (!admin) throw new Error("không tìm thấy tài khoản admin để làm created_by");
const { data: ins, error } = await sb.from("class_announcements").insert({ class_id: plan.class_id, kind: "homework", body, created_by: admin.id }).select("id").single();
if (error) throw new Error(error.message);
console.log(`✓ đã gửi, announcement ${ins.id}`);
const { count } = await sb.from("notifications").select("*", { count: "exact", head: true }).eq("kind", "homework_posted").gte("created_at", new Date(Date.now() - 60_000).toISOString());
console.log(`  chuông trong 60 giây qua: ${count} thông báo`);
