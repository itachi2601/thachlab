// Đặt lại mật khẩu tạm cho tài khoản HS Test (chỉ 2 email *.thachlab.local) để thử UI trên dev. Chạy: node --env-file=.env.local scripts/doi-mk-hs-test.mjs
import { createClient } from "@supabase/supabase-js";
import crypto from "node:crypto";
const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY, { auth: { autoRefreshToken: false, persistSession: false } });
const email = process.argv[2] ?? "hs.test1@thachlab.local";
if (!email.endsWith("@thachlab.local")) { console.error("Chỉ đổi cho tài khoản test"); process.exit(1); }
const { data } = await sb.auth.admin.listUsers({ perPage: 1000 });
const u = data.users.find((x) => x.email === email);
if (!u) { console.error("Không thấy", email); process.exit(1); }
const password = "Test-" + crypto.randomBytes(6).toString("base64url");
const { error } = await sb.auth.admin.updateUserById(u.id, { password });
if (error) { console.error(error.message); process.exit(1); }
console.log(`${email}  mật khẩu mới: ${password}`);
