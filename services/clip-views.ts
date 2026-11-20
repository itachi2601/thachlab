import { getSupabase, supabaseConfigured } from "@/services/supabase";
import { SUPABASE_ANON_KEY, SUPABASE_URL } from "@/lib/supabase-env";
import type { VideoKhungLuot } from "@/components/lessons/VideoThiNghiemKhung";

/**
 * Việc 6 (docs/KE-HOACH-CAI-TIEN-CLIP-2026-11-19.md): ghi MỘT dòng mỗi lượt xem khung video thí nghiệm
 * (migration 20261120120000_lesson_clip_views, RPC log_clip_view). Khung gom sự kiện ở máy khách và chỉ gửi khi
 * xem hết / ẩn tab / rời trang; cùng `luotId` gửi lại thì máy chủ gộp (upsert), nên gửi lặp vô hại.
 *
 * Gửi bằng fetch `keepalive` (sống qua lúc đóng tab, khác supabase-js). Cần access token đọc sẵn: `chuanBiGhiLuotClip`
 * gọi lúc em bấm phát lần đầu (không phải lúc tải trang → không thêm round-trip cho /lop-hoc/bai); getSession chỉ đọc
 * localStorage. Chưa có token thì rơi về supabase-js thường. Lỗi mạng thì bỏ (dữ liệu đo, không làm phiền HS).
 */

let token: string | null = null;
let daNghe = false;

export function chuanBiGhiLuotClip() {
  if (daNghe || typeof window === "undefined" || !supabaseConfigured) return;
  daNghe = true;
  const sb = getSupabase();
  void sb.auth
    .getSession()
    .then(({ data }) => {
      token = data.session?.access_token ?? null;
    })
    .catch(() => undefined);
  sb.auth.onAuthStateChange((_e, s) => {
    token = s?.access_token ?? null;
  });
}

/** JWT còn hạn ≥ 30 giây? Tab để nền lâu thì token cũ hết hạn: rơi về supabase-js (tự làm mới token) thay vì 401. */
function conHan(t: string) {
  try {
    const exp = JSON.parse(atob(t.split(".")[1].replace(/-/g, "+").replace(/_/g, "/"))).exp;
    return typeof exp === "number" && exp * 1000 > Date.now() + 30_000;
  } catch {
    return false;
  }
}

export function logClipView(lessonId: number, l: VideoKhungLuot) {
  if (typeof window === "undefined" || !supabaseConfigured) return;
  const p = { ...l, lessonId };
  if (token && conHan(token)) {
    void fetch(`${SUPABASE_URL}/rest/v1/rpc/log_clip_view`, {
      method: "POST",
      keepalive: true,
      headers: {
        apikey: SUPABASE_ANON_KEY!,
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ p }),
    }).catch(() => undefined);
    return;
  }
  void Promise.resolve(getSupabase().rpc("log_clip_view", { p })).catch(() => undefined);
}
