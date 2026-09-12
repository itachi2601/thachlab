// Tạo tài khoản + hồ sơ cho 6 trợ giảng (module Quản lý trợ giảng).
//
// App này export tĩnh, không có server Node.js ở production nên không thể dùng
// service role key trong app — script này CHỈ chạy cục bộ trên máy bạn,
// SAU KHI đã chạy docs/supabase-migration-tro-giang.sql:
//
//   SUPABASE_SERVICE_ROLE_KEY=xxx NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co node scripts/seed-tro-giang.mjs
//
// Lấy SUPABASE_SERVICE_ROLE_KEY ở Supabase Dashboard → Settings → API → service_role
// (secret, KHÔNG commit, KHÔNG đưa vào .env.local dùng chung với NEXT_PUBLIC_*, KHÔNG dán vào chat).
//
// SỬA LẠI EMAIL THẬT của từng bạn bên dưới trước khi chạy — email đang là placeholder.
// Bậc (tier) mình suy đoán từ đề bài, XÁC NHẬN LẠI trước khi chạy:
//   Hoàng, Mẫn, Tân -> B1 (đề bài không nói rõ bậc)
//   Bảo             -> B3
//   Hiếu, Khánh     -> B3, đơn giá bảo lưu (retained_rate) 65.000đ/giờ quy đổi
//
// Chạy lại an toàn nhiều lần: nếu email đã có tài khoản thì chỉ cập nhật ta_assistants
// (upsert theo user_id), không mời lại.

import { createClient } from "@supabase/supabase-js";

const SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL;
const SERVICE_ROLE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY;
if (!SUPABASE_URL || !SERVICE_ROLE_KEY) {
  console.error("Thiếu NEXT_PUBLIC_SUPABASE_URL hoặc SUPABASE_SERVICE_ROLE_KEY trong biến môi trường.");
  process.exit(1);
}

const ASSISTANTS = [
  { full_name: "Hoàng", short_name: "Hoàng", email: "hoang@thachlab.tro-giang", tier: "B1", retained_rate: null },
  { full_name: "Mẫn", short_name: "Mẫn", email: "man@thachlab.tro-giang", tier: "B1", retained_rate: null },
  { full_name: "Tân", short_name: "Tân", email: "tan@thachlab.tro-giang", tier: "B1", retained_rate: null },
  { full_name: "Bảo", short_name: "Bảo", email: "bao@thachlab.tro-giang", tier: "B3", retained_rate: null },
  { full_name: "Hiếu", short_name: "Hiếu", email: "hieu@thachlab.tro-giang", tier: "B3", retained_rate: 65000 },
  { full_name: "Khánh", short_name: "Khánh", email: "khanh@thachlab.tro-giang", tier: "B3", retained_rate: 65000 },
];

const supabase = createClient(SUPABASE_URL, SERVICE_ROLE_KEY, {
  auth: { autoRefreshToken: false, persistSession: false },
});

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
  for (const ta of ASSISTANTS) {
    try {
      let userId;
      const existing = await findExistingUserByEmail(ta.email);
      if (existing) {
        userId = existing.id;
        console.log(`= ${ta.email} đã có tài khoản, chỉ cập nhật hồ sơ trợ giảng.`);
      } else {
        const { data, error } = await supabase.auth.admin.inviteUserByEmail(ta.email, {
          data: { full_name: ta.full_name },
        });
        if (error) throw error;
        userId = data.user.id;
        console.log(`+ Đã mời ${ta.email}`);
        await new Promise((resolve) => setTimeout(resolve, 800)); // đợi trigger handle_new_user tạo profiles
      }

      const { error: upsertError } = await supabase.from("ta_assistants").upsert(
        {
          user_id: userId,
          full_name: ta.full_name,
          short_name: ta.short_name,
          tier: ta.tier,
          retained_rate: ta.retained_rate,
        },
        { onConflict: "user_id" },
      );
      if (upsertError) throw upsertError;
      console.log(`  → hồ sơ trợ giảng ${ta.short_name} (${ta.tier}${ta.retained_rate ? `, bảo lưu ${ta.retained_rate}đ` : ""})`);
    } catch (cause) {
      console.error(`! Lỗi với ${ta.email}:`, cause instanceof Error ? cause.message : cause);
    }
  }
}

main();
