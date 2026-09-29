import { getSupabase } from "@/services/supabase";

// Gọi RPC tổng hợp phía giáo viên (supabase/migrations/20260925130000_perf_rpc_gv.sql)
// theo kiểu "có thì dùng, không thì thôi": trả null khi hàm chưa được tạo trên DB
// (thầy chưa chạy migration → PostgREST trả PGRST202 / Postgres 42883) hoặc khi rpc
// lỗi vì bất kỳ lý do gì — nơi gọi sẽ fallback về đường truy vấn cũ. Hàm nào đã
// biết là chưa có thì nhớ lại trong phiên để khỏi gọi hụt thêm lần nào nữa.

const missingRpcs = new Set<string>();

export function isMissingRpcError(error: unknown): boolean {
  const e = error as { code?: string; message?: string } | null;
  if (!e) return false;
  if (e.code === "PGRST202" || e.code === "42883") return true;
  return /could not find the function|does not exist/i.test(e.message ?? "");
}

/** Có null khi RPC không dùng được; caller phải có đường cũ để thay. */
export async function callClassRpc<T>(name: string, params: Record<string, unknown>): Promise<T | null> {
  if (missingRpcs.has(name)) return null;
  try {
    const { data, error } = await getSupabase().rpc(name, params);
    if (error) {
      if (isMissingRpcError(error)) missingRpcs.add(name);
      return null;
    }
    return (data ?? null) as T | null;
  } catch {
    return null;
  }
}

/** Dùng cho script đối chiếu: quên trạng thái "chưa có" để gọi lại. */
export function resetMissingRpcCache() {
  missingRpcs.clear();
}
