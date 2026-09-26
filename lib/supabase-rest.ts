// Gọi PostgREST bằng fetch thuần — dùng cho các truy vấn ĐỌC đơn giản trên trang công
// khai (ẩn danh), để khỏi phải tải cả @supabase/supabase-js (~211KB) chỉ vì 1-2 câu
// SELECT/RPC không cần tính năng nào khác của SDK (auth, realtime...).
//
// Vẫn gửi đúng header apikey/Authorization như supabase-js làm với anon key, nên KHÔNG
// đổi RLS: PostgREST xử lý y hệt, quyền hạn vẫn do policy trên bảng quyết định.
//
// Chỉ dùng cho trang KHÔNG có AuthProvider (xem components/auth/PublicShell.tsx) — nếu
// trang đã có AuthProvider (đã tải supabase-js rồi) thì cứ dùng getSupabase() cho gọn,
// dùng lại helper này không tiết kiệm gì thêm.
import { SUPABASE_URL, SUPABASE_ANON_KEY, supabaseConfigured } from "./supabase-env";

async function restFetch(path: string, init?: RequestInit): Promise<unknown> {
  if (!supabaseConfigured) {
    throw new Error(
      "Chưa cấu hình Supabase — điền NEXT_PUBLIC_SUPABASE_URL và NEXT_PUBLIC_SUPABASE_ANON_KEY vào .env.local",
    );
  }
  const res = await fetch(`${SUPABASE_URL}/rest/v1/${path}`, {
    ...init,
    headers: {
      apikey: SUPABASE_ANON_KEY!,
      Authorization: `Bearer ${SUPABASE_ANON_KEY}`,
      ...(init?.headers ?? {}),
    },
  });
  if (!res.ok) {
    const body = await res.text().catch(() => "");
    throw new Error(`Supabase REST lỗi ${res.status}: ${body || res.statusText}`);
  }
  return res.json();
}

/** SELECT ẩn danh — `params` là query string PostgREST đã build sẵn (vd qua URLSearchParams). */
export function restSelect(table: string, params: string | URLSearchParams): Promise<unknown> {
  return restFetch(`${table}?${params}`);
}

/** Gọi RPC (SECURITY DEFINER) qua REST — tương đương supabase.rpc(fn, args). */
export function restRpc(fn: string, args: Record<string, unknown>): Promise<unknown> {
  return restFetch(`rpc/${fn}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(args),
  });
}
