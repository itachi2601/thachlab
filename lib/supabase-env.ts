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

/** Khóa localStorage mặc định của supabase-js: `sb-<ref>-auth-token`. Không import SDK. */
export function supabaseAuthStorageKey(): string | null {
  if (!SUPABASE_URL) return null;
  try {
    const ref = new URL(SUPABASE_URL).hostname.split(".")[0];
    return ref ? `sb-${ref}-auth-token` : null;
  } catch {
    return null;
  }
}

/** true khi trình duyệt còn phiên — trang công khai chỉ tải SDK trong trường hợp này. */
export function hasStoredSupabaseSession(): boolean {
  const key = supabaseAuthStorageKey();
  if (!key || typeof window === "undefined") return false;
  try {
    const raw = window.localStorage.getItem(key);
    return Boolean(raw && raw.length > 2);
  } catch {
    return false;
  }
}
