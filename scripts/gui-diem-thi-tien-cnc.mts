// Gửi điểm thành phần + lỗi loại trực tiếp của bài thi tiện CNC cho TỪNG SV qua chuông thông báo thachlab (notify_user).
// Mặc định DRY-RUN (chỉ in ai khớp tài khoản, nội dung); thêm --yes mới ghi thật. CHẠY TRÊN MAC (cần service role).
//   npx tsx scripts/gui-diem-thi-tien-cnc.mts "<file.csv>" [--course 10] [--yes]
// CSV là file "Tải CSV" ở docs/cnc-nhap-diem.html: ca,máy,đề,họ tên,8 mức E/G/P/F,4 cột lỗi (x),tổng,xếp loại.
// Ngoài thông báo còn nạp bảng cnc_grades (module tien) để SV mở trang /lop-hoc/cnc/bang-diem/ xem. Chạy lại an toàn (upsert).
// Mỗi SV chỉ nhận điểm của chính mình. SV không khớp đúng 1 tài khoản trong lớp thì bỏ qua và in ra để xử tay.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const args = process.argv.slice(2);
const yes = args.includes("--yes");
const ci = args.indexOf("--course");
const courseId = ci >= 0 ? Number(args[ci + 1]) : 10;
const file = args.find((a, i) => !a.startsWith("--") && args[i - 1] !== "--course");
if (!file) throw new Error("thiếu đường dẫn file CSV");

function envLocal(key: string): string | undefined {
  const line = fs.readFileSync(path.join(root, ".env.local"), "utf8").split("\n").find((l) => l.startsWith(`${key}=`));
  return line ? line.slice(key.length + 1).trim() : undefined;
}
const url = envLocal("NEXT_PUBLIC_SUPABASE_URL");
const key = envLocal("SUPABASE_SERVICE_ROLE_KEY");
if (!url || !key) throw new Error("thiếu khoá Supabase trong .env.local");
const sb = createClient(url, key);

const NAMES = ["Lập trình", "Mô phỏng", "Cài đặt dao, phôi", "Gia công, đo kiểm", "Vận hành, Test Offset MDI", "An toàn lao động", "5S", "Thời gian (45')"];
const MAX = [1.5, 1, 2.5, 2, 1, 1, 0.5, 0.5];
const LV: Record<string, [string, number]> = { E: ["Xuất sắc", 1], G: ["Khá", 0.75], P: ["Đạt", 0.5], F: ["Không đạt", 0] };
const VIOL = ["Đâm dao/va chạm do bấm nhầm", "Vi phạm an toàn nghiêm trọng", "Chạy AUTO khi chưa mô phỏng/Test Offset", "Báo sai kết quả đo"];
const r2 = (x: number) => Math.round(x * 100) / 100;
const fmt = (x: number) => String(r2(x)).replace(".", ",");
// Tên trong hệ thống có thể đảo thứ tự ("Đông Phạm Duy"), thiếu dấu, thiếu họ → so theo tập từ, không phân biệt dấu/thứ tự.
const toks = (s: string) => s.normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/đ/gi, "d").replace(/\*/g, "").toLowerCase().split(/\s+/).filter(Boolean);

const lines = fs.readFileSync(file, "utf8").replace(/^﻿/, "").split(/\r?\n/).filter(Boolean);
const rows = lines.map((l) => l.split(","));

const { data: enr, error: e1 } = await sb.from("course_enrollments").select("student_id").eq("course_id", courseId).eq("status", "active");
if (e1) throw new Error(e1.message);
const ids = (enr ?? []).map((e) => e.student_id as string);
const { data: profs, error: e2 } = await sb.from("profiles").select("id, full_name").in("id", ids);
if (e2) throw new Error(e2.message);
const plist = (profs ?? []).map((p) => ({ id: p.id as string, t: toks(p.full_name ?? "") }));
function find(name: string): string[] {
  const a = toks(name), key = [...a].sort().join(" ");
  const exact = plist.filter((p) => [...p.t].sort().join(" ") === key);
  if (exact.length) return exact.map((p) => p.id);
  // tên hồ sơ thiếu từ (vd thiếu họ) nhưng mọi từ đều nằm trong tên CSV
  return plist.filter((p) => p.t.length >= 2 && p.t.every((w) => a.includes(w))).map((p) => p.id);
}

const KIND = "diem-thi-tien-cnc";
const HREF = "/lop-hoc/cnc/bang-diem/";
let sent = 0, skipped = 0;
for (const c of rows) {
  const name = c[3];
  const levels = c.slice(4, 12);
  if (!levels.some(Boolean) && c[17] === "–") { console.log(`– ${name}: chưa chấm, bỏ qua`); skipped++; continue; }
  const m = find(name);
  if (m.length !== 1) { console.log(`! ${name}: khớp ${m.length} tài khoản trong lớp ${courseId} — BỎ QUA, xử tay`); skipped++; continue; }
  const pts = levels.map((v, k) => (v ? r2(LV[v][1] * MAX[k]) : null));
  const g1 = pts.slice(0, 4).reduce<number>((s, x) => s + (x ?? 0), 0);
  const viol = VIOL.filter((_, k) => c[12 + k] === "x");
  const body =
    "Điểm bài thi tiện CNC của em:\n" +
    levels.map((v, k) => `• ${NAMES[k]}: ${v ? `${LV[v][0]} (${fmt(pts[k] ?? 0)}/${fmt(MAX[k])})` : "chưa chấm"}`).join("\n") +
    `\nI. Kỹ thuật: ${fmt(g1)}/7` + (g1 < 3.5 ? " (dưới 3,5 nên nhóm II tính 0)" : "") +
    `\nLỗi loại trực tiếp: ${viol.length ? viol.join("; ") + " → bài tính Không đạt" : "không vi phạm"}` +
    `\nTổng: ${c[16].replace(".", ",")}/10 · ${c[17]}`;
  console.log(`${yes ? "→ gửi" : "○ sẽ gửi"} ${name}\n${body.replace(/^/gm, "    ")}`);
  if (!yes) continue;
  const g2 = pts.slice(4).reduce<number>((s, x) => s + (x ?? 0), 0);
  const { error: eg } = await sb.from("cnc_grades").upsert({
    course_id: courseId, student_id: m[0], module: "tien", ky_thuat: r2(g1), thanh_phan: r2(g1 >= 3.5 ? g2 : 0),
    total: Number(c[16]), grade: c[17],
    detail: { criteria: levels.map((v, k) => ({ name: NAMES[k], level: v || null, points: pts[k], max: MAX[k] })), violations: viol },
    updated_at: new Date().toISOString(),
  });
  if (eg) throw new Error(`${name}: cnc_grades: ${eg.message}`);
  const { data: dup } = await sb.from("notifications").select("id").eq("user_id", m[0]).eq("kind", KIND).limit(1);
  if (dup?.length) {
    await sb.from("notifications").update({ href: HREF }).eq("user_id", m[0]).eq("kind", KIND);
    console.log("  ≈ đã gửi trước đó, chỉ đổi link + cập nhật bảng điểm"); skipped++; continue;
  }
  const { error } = await sb.rpc("notify_user", { p_user: m[0], p_kind: KIND, p_title: "Điểm thi tiện CNC", p_body: body, p_href: HREF });
  if (error) throw new Error(`${name}: ${error.message}`);
  sent++;
}
console.log(`\n${yes ? "Đã gửi" : "Sẽ gửi"} ${yes ? sent : rows.length - skipped} · bỏ qua ${skipped}`);
