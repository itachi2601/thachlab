// Tạo 2 tài khoản học sinh THỬ (HS Test 1/2) để thử danh hiệu, khung sưu tập, bảng tuần, phụ đạo.
// Chạy trên Mac:  node --env-file=.env.local scripts/tao-hs-test.mjs
// In mật khẩu tạm ra console (không ghi file). Chạy lại nhiều lần an toàn (có rồi thì chỉ cập nhật hồ sơ/lớp).
// Xoá khi thử xong: node --env-file=.env.local scripts/tao-hs-test.mjs --xoa
import { createClient } from "@supabase/supabase-js";
import crypto from "node:crypto";

const URL = process.env.NEXT_PUBLIC_SUPABASE_URL;
const KEY = process.env.SUPABASE_SERVICE_ROLE_KEY;
if (!URL || !KEY) { console.error("Thiếu NEXT_PUBLIC_SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY"); process.exit(1); }

const ACCOUNTS = [
  { full_name: "HS Test 1", email: "hs.test1@thachlab.local" },
  { full_name: "HS Test 2", email: "hs.test2@thachlab.local" },
];
const sb = createClient(URL, KEY, { auth: { autoRefreshToken: false, persistSession: false } });
const pw = () => crypto.randomBytes(9).toString("base64").replace(/[+/=]/g, "x") + "!1";

async function find(email) {
  for (let page = 1; page <= 20; page++) {
    const { data, error } = await sb.auth.admin.listUsers({ page, perPage: 200 });
    if (error) throw error;
    const u = data.users.find((x) => x.email?.toLowerCase() === email);
    if (u) return u;
    if (data.users.length < 200) return null;
  }
  return null;
}

const xoa = process.argv.includes("--xoa");
const { data: cls } = await sb.from("classes").select("id,name,slug").eq("active", true).order("sort_order");
const lop12 = cls?.find((c) => /12/.test(`${c.name} ${c.slug}`)) ?? cls?.[0];
console.log("Lớp ghi danh:", lop12?.name, lop12?.id);

for (const a of ACCOUNTS) {
  const existing = await find(a.email);
  if (xoa) {
    if (existing) { await sb.auth.admin.deleteUser(existing.id); console.log("- đã xoá", a.email); }
    continue;
  }
  let id, password = null;
  if (existing) { id = existing.id; }
  else {
    password = pw();
    const { data, error } = await sb.auth.admin.createUser({ email: a.email, password, email_confirm: true, user_metadata: { full_name: a.full_name } });
    if (error) { console.error("!", a.email, error.message); continue; }
    id = data.user.id;
    await new Promise((r) => setTimeout(r, 800));
  }
  await sb.from("profiles").update({ full_name: a.full_name, role: "student", track: "THPT" }).eq("id", id);
  if (lop12) await sb.from("user_classes").upsert({ user_id: id, class_id: lop12.id, status: "active" });
  console.log(`${existing ? "=" : "+"} ${a.email}  mật khẩu: ${password ?? "(đã có từ trước — không đổi)"}`);
}
