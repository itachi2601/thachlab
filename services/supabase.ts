import { createClient, type SupabaseClient } from "@supabase/supabase-js";
import { SUPABASE_URL, SUPABASE_ANON_KEY, supabaseConfigured } from "@/lib/supabase-env";

// Site xuất tĩnh — mọi truy cập dữ liệu đều từ trình duyệt qua anon key,
// quyền hạn thật sự nằm ở RLS (xem docs/supabase-schema.sql).
// supabaseConfigured đọc từ lib/supabase-env.ts (không import supabase-js) — re-export lại
// ở đây để các file đang import từ "@/services/supabase" không phải sửa gì.
export { supabaseConfigured };

let client: SupabaseClient | null = null;

export function getSupabase(): SupabaseClient {
  if (!supabaseConfigured) {
    throw new Error(
      "Chưa cấu hình Supabase — điền NEXT_PUBLIC_SUPABASE_URL và NEXT_PUBLIC_SUPABASE_ANON_KEY vào .env.local",
    );
  }
  if (!client) client = createClient(SUPABASE_URL!, SUPABASE_ANON_KEY!);
  return client;
}
