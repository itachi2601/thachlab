/**
 * supabase-js chỉ trả "Edge Function returned a non-2xx status code" khi hàm trả lỗi HTTP; nội dung lỗi thật
 * ({ error: "..." } do hàm viết) nằm trong `error.context` (Response). Đọc ra để giáo viên thấy nguyên nhân.
 */
export async function edgeFunctionErrorMessage(error: unknown, fallback: string): Promise<string> {
  const ctx = (error as { context?: unknown } | null)?.context;
  if (ctx && typeof (ctx as Response).text === "function") {
    try {
      const raw = await (ctx as Response).text();
      try {
        const j = JSON.parse(raw) as { error?: unknown; message?: unknown };
        const m = typeof j.error === "string" ? j.error : typeof j.message === "string" ? j.message : "";
        if (m) return `${m} (HTTP ${(ctx as Response).status})`;
      } catch {
        /* không phải JSON */
      }
      if (raw.trim()) return `${raw.trim().slice(0, 300)} (HTTP ${(ctx as Response).status})`;
    } catch {
      /* body đã đọc */
    }
  }
  return (error as { message?: string } | null)?.message || fallback;
}
