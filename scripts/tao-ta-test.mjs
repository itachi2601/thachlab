// Tạo 1 tài khoản TRỢ GIẢNG thử (TA Test) để thử các trang /tro-giang/* bằng đăng nhập thật.
// Chạy trên Mac:  node --env-file=.env.local scripts/tao-ta-test.mjs
// In mật khẩu tạm ra console (không ghi file). Chạy lại an toàn (có rồi thì chỉ cập nhật hồ sơ).
// Xoá khi thử xong:  node --env-file=.env.local scripts/tao-ta-test.mjs --xoa
// Xoá cả phiếu phỏng vấn của TA Test (ta_interviews, ta_sessions... xoá theo khoá ngoại cascade) rồi xoá tài khoản.
import { createClient } from "@supabase/supabase-js";
import crypto from "node:crypto";

const URL = process.env.NEXT_PUBLIC_SUPABASE_URL;
const KEY = process.env.SUPABASE_SERVICE_ROLE_KEY;
if (!URL || !KEY) { console.error("Thiếu NEXT_PUBLIC_SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY"); process.exit(1); }

const EMAIL = "ta.test@thachlab.local";
const NAME = "TA Test";
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
const existing = await find(EMAIL);

if (xoa) {
  if (existing) {
    const { error: e1 } = await sb.from("ta_assistants").delete().eq("user_id", existing.id);
    if (e1) { console.error("! không xoá được hồ sơ trợ giảng:", e1.message); process.exit(1); }
    const { error: e2 } = await sb.auth.admin.deleteUser(existing.id);
    if (e2) { console.error("! không xoá được tài khoản:", e2.message); process.exit(1); }
    console.log("- đã xoá", EMAIL, "và hồ sơ trợ giảng");
  } else console.log("Không có tài khoản", EMAIL);
  process.exit(0);
}

// Role của trợ giảng thật đang có (không đoán tên role).
const { data: real } = await sb.from("ta_assistants").select("user_id").eq("active", true).not("user_id", "is", null).limit(1).maybeSingle();
const { data: realProfile } = real ? await sb.from("profiles").select("role,track").eq("id", real.user_id).maybeSingle() : { data: null };
const role = realProfile?.role ?? "student";
console.log("Role lấy theo trợ giảng thật:", role);

let id, password = null;
if (existing) id = existing.id;
else {
  password = pw();
  const { data, error } = await sb.auth.admin.createUser({ email: EMAIL, password, email_confirm: true, user_metadata: { full_name: NAME } });
  if (error) { console.error("!", EMAIL, error.message); process.exit(1); }
  id = data.user.id;
  await new Promise((r) => setTimeout(r, 800));
}
await sb.from("profiles").update({ full_name: NAME, role, track: realProfile?.track ?? "THPT" }).eq("id", id);
const { data: ta } = await sb.from("ta_assistants").select("id").eq("user_id", id).maybeSingle();
if (!ta) {
  const { error } = await sb.from("ta_assistants").insert({ user_id: id, full_name: NAME, short_name: NAME, tier: "B1", active: true, started_at: new Date().toISOString().slice(0, 10) });
  if (error) { console.error("! không tạo được hồ sơ trợ giảng:", error.message); process.exit(1); }
}
console.log(`${existing ? "=" : "+"} ${EMAIL}  mật khẩu: ${password ?? "(đã có từ trước — không đổi)"}`);
