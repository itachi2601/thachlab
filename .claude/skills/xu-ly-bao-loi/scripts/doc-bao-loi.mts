/**
 * Đọc báo lỗi & góp ý (bảng bug_reports) và in BẢNG GỌN đã phân loại + gắn agent đề xuất.
 * CHỈ ĐỌC. Chạy trên Mac: npx tsx .claude/skills/xu-ly-bao-loi/scripts/doc-bao-loi.mts [--status moi|dang_xu_ly|da_xu_ly|all] [--json]
 * Mặc định: status=moi. --json ghi thêm scripts/logs/bao-loi-<ngày>.json để các agent đọc lại không cần gọi DB.
 */
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..", "..", "..", "..");
function env(name: string) {
  if (process.env[name]) return process.env[name];
  const p = path.join(root, ".env.local");
  if (!fs.existsSync(p)) return undefined;
  return fs.readFileSync(p, "utf8").split("\n").find((l) => l.startsWith(`${name}=`))?.slice(name.length + 1).trim();
}
const url = env("NEXT_PUBLIC_SUPABASE_URL"), key = env("SUPABASE_SERVICE_ROLE_KEY");
if (!url || !key) throw new Error("Thiếu NEXT_PUBLIC_SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY");
const sb = createClient(url, key);

const args = process.argv.slice(2);
const status = args.includes("--status") ? args[args.indexOf("--status") + 1] : "moi";

let q = sb.from("bug_reports")
  .select("id,created_at,reporter_name,page_url,category,description,screenshot_path,status,admin_note,exam_id,question_index")
  .order("created_at", { ascending: true });
if (status !== "all") q = q.eq("status", status);
const { data, error } = await q;
if (error) throw error;

type Row = NonNullable<typeof data>[number];
/** Gợi ý nhóm việc + agent. Chỉ là gợi ý đầu; phiên chính chốt lại sau khi đọc. */
function route(r: Row): { nhom: string; agent: string } {
  const d = (r.description ?? "").toLowerCase(), u = r.page_url ?? "";
  if (r.category === "cau_hoi" || r.exam_id != null || /\/kiem-tra\/lam/.test(u))
    return { nhom: "A. Nội dung đề/câu hỏi", agent: "kiem-code (tự giải) → phiên chính sửa qua /quan-tri/sua-de" };
  if (r.category === "de_xuat") return { nhom: "E. Đề xuất tính năng", agent: "KHÔNG sửa — gom lại hỏi thầy" };
  if (r.category === "dang_nhap" || /(mật khẩu|đăng nhập|tài khoản|email)/.test(d))
    return { nhom: "D. Tài khoản/đăng nhập", agent: "kien-truc-du-lieu (nếu RLS/auth) hoặc phiên chính" };
  if (r.category === "diem" || /(điểm|xếp hạng|rank|mất bài|nộp)/.test(d))
    return { nhom: "D. Điểm/rank/nộp bài", agent: "kien-truc-du-lieu (đọc), phiên chính sửa" };
  if (/\/lop-hoc\/bai/.test(u) && /(công thức|đáp án|sai|nhầm|hình)/.test(d))
    return { nhom: "B. Nội dung bài học", agent: "kiem-code (kiểm Vật lí) → phiên chính sửa" };
  if (r.category === "hien_thi" || /(không hiện|vỡ|tràn|điện thoại|chữ nhỏ|nút)/.test(d))
    return { nhom: "C. Giao diện/code", agent: "agent `claude`/phiên chính sửa → kiem-code soát diff" };
  return { nhom: "F. Chưa rõ", agent: "phiên chính đọc ảnh + hỏi lại người báo" };
}

const rows = (data ?? []).map((r) => ({ ...r, ...route(r) }));
const byNhom = new Map<string, typeof rows>();
for (const r of rows) byNhom.set(r.nhom, [...(byNhom.get(r.nhom) ?? []), r]);

console.log(`# Báo lỗi (status=${status}): ${rows.length} mục\n`);
for (const [nhom, list] of [...byNhom].sort()) {
  console.log(`## ${nhom} — ${list.length} mục → ${list[0].agent}`);
  for (const r of list) {
    const ref = r.exam_id != null ? ` [đề ${r.exam_id}${r.question_index != null ? ` câu ${r.question_index + 1}` : ""}]` : "";
    const img = r.screenshot_path ? " 📷" : "";
    console.log(`- #${r.id} ${r.created_at.slice(0, 10)} ${r.page_url}${ref}${img}\n  ${(r.description ?? "").replace(/\s+/g, " ").slice(0, 220)}`);
  }
  console.log();
}
if (args.includes("--json")) {
  const f = path.join(root, "scripts", "logs", `bao-loi-${new Date().toISOString().slice(0, 10)}.json`);
  fs.mkdirSync(path.dirname(f), { recursive: true });
  fs.writeFileSync(f, JSON.stringify(rows, null, 1));
  console.log(`Đã ghi ${f}`);
}
