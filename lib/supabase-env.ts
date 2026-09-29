// Đọc cấu hình Supabase từ biến môi trường — KHÔNG import @supabase/supabase-js ở đây.
//
// Lý do tách riêng khỏi services/supabase.ts: app/layout.tsx (áp dụng cho MỌI trang, kể
// cả trang công khai chưa đăng nhập) cần domain Supabase để chèn <link rel="preconnect">,
// và vài trang công khai cần kiểm tra "đã cấu hình Supabase chưa" — nếu lấy 2 thứ này từ
// services/supabase.ts thì sẽ kéo theo cả supabase-js/GoTrue (~211KB) dù không dùng tới.
// services/supabase.ts (bản đầy đủ, có getSupabase()) re-export supabaseConfigured từ
// đây để giữ một nguồn sự thật duy nhất.
export const SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL;
export const SUPABASE_ANON_KEY = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

export const supabaseConfigured = Boolean(SUPABASE_URL && SUPABASE_ANON_KEY);
