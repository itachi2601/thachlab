import { createClient, type SupabaseClient } from "@supabase/supabase-js";

// Site xuất tĩnh — mọi truy cập dữ liệu đều từ trình duyệt qua anon key,
// quyền hạn thật sự nằm ở RLS (xem docs/supabase-schema.sql).
const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
const anonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

export const supabaseConfigured = Boolean(url && anonKey);

let client: SupabaseClient | null = null;

export function getSupabase(): SupabaseClient {
  if (!supabaseConfigured) {
    throw new Error(
      "Chưa cấu hình Supabase — điền NEXT_PUBLIC_SUPABASE_URL và NEXT_PUBLIC_SUPABASE_ANON_KEY vào .env.local",
    );
  }
  if (!client) client = createClient(url!, anonKey!);
  return client;
}
