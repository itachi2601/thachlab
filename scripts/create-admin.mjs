// Tạo (hoặc nâng quyền) một tài khoản quản trị role='admin' — chủ trang, thấy cả THPT lẫn CTTC.
//
// App export tĩnh nên không có API route dùng service_role; script này CHỈ chạy cục bộ:
//
//   SUPABASE_SERVICE_ROLE_KEY=xxx node scripts/create-admin.mjs <email> ["Họ và tên"]
//
// (NEXT_PUBLIC_SUPABASE_URL tự đọc từ .env.local; lấy service_role key ở Supabase
// Dashboard → Settings → API → service_role — secret, KHÔNG commit, KHÔNG dán vào chat.)
//
// Email đã có tài khoản  -> chỉ đặt role='admin', không đổi mật khẩu.
// Email chưa có tài khoản -> tạo mới kèm mật khẩu tạm in ra console (đổi sau khi đăng nhập).
//
// Khác scripts/invite-instructors.mjs và panel "mời bằng mã" ở /quan-tri/nhan-su: hai lối đó
// chỉ cấp được role 'instructor'/'tro_giang'; role 'admin' chỉ đặt được bằng service_role.

import { readFileSync } from "node:fs";
import crypto from "node:crypto";
import { createClient } from "@supabase/supabase-js";

function envFromLocalFile(key) {
  try {
    const line = readFileSync(new URL("../.env.local", import.meta.url), "utf8")
      .split("\n")
      .find((l) => l.startsWith(`${key}=`));
    return line ? line.slice(key.length + 1).trim() : undefined;
  } catch {
    return undefined;
  }
}

const [email, fullNameArg] = process.argv.slice(2);
const SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL ?? envFromLocalFile("NEXT_PUBLIC_SUPABASE_URL");
const SERVICE_ROLE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY;

if (!email || !email.includes("@")) {
  console.error('Cách dùng: SUPABASE_SERVICE_ROLE_KEY=xxx node scripts/create-admin.mjs <email> ["Họ và tên"]');
  process.exit(1);
}
if (!SUPABASE_URL || !SERVICE_ROLE_KEY) {
  console.error("Thiếu NEXT_PUBLIC_SUPABASE_URL hoặc SUPABASE_SERVICE_ROLE_KEY.");
  process.exit(1);
}

const fullName = fullNameArg?.trim() || email.split("@")[0];
const supabase = createClient(SUPABASE_URL, SERVICE_ROLE_KEY, {
  auth: { autoRefreshToken: false, persistSession: false },
});

async function findUserByEmail(target) {
  for (let page = 1; page <= 20; page++) {
    const { data, error } = await supabase.auth.admin.listUsers({ page, perPage: 200 });
    if (error) throw error;
    const found = data.users.find((user) => user.email?.toLowerCase() === target.toLowerCase());
    if (found) return found;
    if (data.users.length < 200) return null;
  }
  return null;
}

async function main() {
  const existing = await findUserByEmail(email);
  let userId;
  let password = null;

  if (existing) {
    userId = existing.id;
    console.log(`= ${email} đã có tài khoản, chỉ nâng quyền.`);
  } else {
    password = crypto.randomBytes(9).toString("base64").replace(/[+/=]/g, "x") + "!1";
    const { data, error } = await supabase.auth.admin.createUser({
      email,
      password,
      email_confirm: true,
      user_metadata: { full_name: fullName },
    });
    if (error) throw error;
    userId = data.user.id;
    console.log(`+ Đã tạo tài khoản ${email}`);
    // Chờ trigger on_auth_user_created chèn xong dòng profiles.
    await new Promise((resolve) => setTimeout(resolve, 800));
  }

  const patch = { role: "admin" };
  if (!existing || fullNameArg) patch.full_name = fullName;
  const { error } = await supabase.from("profiles").update(patch).eq("id", userId);
  if (error) throw error;

  console.log(`  → role=admin cho ${fullName} <${email}>`);
  if (password) {
    console.log(`\n=== Lưu lại ngay, sẽ không hiện lại ===\n${email}  mật khẩu tạm: ${password}`);
    console.log("Đăng nhập tại https://thachlab.id.vn/dang-nhap rồi đổi mật khẩu.");
  }
}

main().catch((cause) => {
  console.error("! Lỗi:", cause instanceof Error ? cause.message : cause);
  process.exit(1);
});
