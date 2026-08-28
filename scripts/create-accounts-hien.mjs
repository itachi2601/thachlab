// Tạo tài khoản giảng viên (role=admin) + 1 tài khoản sinh viên demo (role=student).
//
// App này export tĩnh (next.config output: "export"), không có server Node.js ở production
// nên không thể có API route dùng service role key. Script này CHỈ chạy cục bộ trên máy bạn:
//
//   SUPABASE_SERVICE_ROLE_KEY=xxx NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co node scripts/create-accounts-hien.mjs
//
// Lấy SUPABASE_SERVICE_ROLE_KEY ở Supabase Dashboard → Settings → API → service_role
// (secret, KHÔNG commit, KHÔNG đưa vào .env.local dùng chung với NEXT_PUBLIC_*, KHÔNG dán vào chat).
//
// Khác với scripts/invite-instructors.mjs (gửi email mời), script này tạo tài khoản kèm
// mật khẩu tạm và in ra console — dùng khi cần có mật khẩu ngay (vd. tài khoản demo) hoặc
// khi không chắc hộp thư sẽ nhận được email mời.

import { createClient } from "@supabase/supabase-js";
import crypto from "node:crypto";

const SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL;
const SERVICE_ROLE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY;
if (!SUPABASE_URL || !SERVICE_ROLE_KEY) {
  console.error("Thiếu NEXT_PUBLIC_SUPABASE_URL hoặc SUPABASE_SERVICE_ROLE_KEY trong biến môi trường.");
  process.exit(1);
}

const ACCOUNTS = [
  { full_name: "Nguyễn Thị Hiền", email: "nguyenthihien@caothang.edu.vn", role: "admin" },
  { full_name: "Học sinh Demo", email: "hocsinh.demo@thachlab.local", role: "student" },
];

function genPassword() {
  return crypto.randomBytes(9).toString("base64").replace(/[+/=]/g, "x") + "!1";
}

const supabase = createClient(SUPABASE_URL, SERVICE_ROLE_KEY, { auth: { autoRefreshToken: false, persistSession: false } });

async function findExistingUserByEmail(email) {
  for (let page = 1; page <= 20; page++) {
    const { data, error } = await supabase.auth.admin.listUsers({ page, perPage: 200 });
    if (error) throw error;
    const found = data.users.find((user) => user.email?.toLowerCase() === email.toLowerCase());
    if (found) return found;
    if (data.users.length < 200) return null;
  }
  return null;
}

async function main() {
  const results = [];
  for (const person of ACCOUNTS) {
    try {
      let userId;
      let password = null;
      const existing = await findExistingUserByEmail(person.email);
      if (existing) {
        userId = existing.id;
        console.log(`= ${person.email} đã có tài khoản, chỉ cập nhật vai trò.`);
      } else {
        password = genPassword();
        const { data, error } = await supabase.auth.admin.createUser({
          email: person.email,
          password,
          email_confirm: true,
          user_metadata: { full_name: person.full_name },
        });
        if (error) throw error;
        userId = data.user.id;
        console.log(`+ Đã tạo ${person.email}`);
      }
      await new Promise((resolve) => setTimeout(resolve, existing ? 0 : 800));
      const { error: updateError } = await supabase
        .from("profiles")
        .update({ full_name: person.full_name, role: person.role })
        .eq("id", userId);
      if (updateError) throw updateError;
      console.log(`  → role=${person.role} cho ${person.full_name}`);
      results.push({ ...person, password });
    } catch (cause) {
      console.error(`! Lỗi với ${person.email}:`, cause instanceof Error ? cause.message : cause);
    }
  }

  console.log("\n=== Thông tin đăng nhập (lưu lại ngay, sẽ không hiện lại) ===");
  for (const r of results) {
    console.log(`${r.full_name} <${r.email}> role=${r.role} password=${r.password ?? "(đã có tài khoản, không đổi mật khẩu)"}`);
  }
}

main();
