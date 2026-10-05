// Nhắc luyện tập 1 lần/ngày bằng Web Push (GĐ 2.6 / M4). Gọi MỖI GIỜ bởi pg_cron + pg_net (xem
// docs/PUSH-NHAC-HANG-NGAY.md). Mỗi lần: gọi RPC claim_push_reminders_due (chỉ service_role; tự đánh dấu
// last_sent_at nên chạy trùng không nhắc 2 lần), gửi tin, xoá đăng ký hết hạn (404/410).
//
// Secrets bắt buộc (supabase secrets set ...): VAPID_PUBLIC_KEY, VAPID_PRIVATE_KEY, VAPID_SUBJECT (mailto:...),
// PUSH_CRON_SECRET (chuỗi ngẫu nhiên; cron gửi trong header x-cron-secret). SUPABASE_URL và
// SUPABASE_SERVICE_ROLE_KEY được Supabase tự bơm. Deploy bằng --no-verify-jwt vì cron xác thực bằng x-cron-secret.
// KHÔNG typecheck được (supabase/functions nằm ngoài tsconfig, máy không có deno) — phải bấm thử thật sau deploy.

import { createClient } from "npm:@supabase/supabase-js@2";
import webpush from "npm:web-push@3.6.7";
import { buildPushPayload } from "./message.ts";

function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json" } });
}

function safeEqual(a: string, b: string) {
  if (a.length !== b.length) return false;
  let d = 0;
  for (let i = 0; i < a.length; i++) d |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return d === 0;
}

interface DueRow {
  subscription_id: number;
  student_id: string;
  endpoint: string;
  p256dh: string;
  auth_key: string;
  topic_name: string | null;
  level: string | null;
}

Deno.serve(async (req) => {
  if (req.method !== "POST") return json({ error: "method not allowed" }, 405);

  const secret = Deno.env.get("PUSH_CRON_SECRET") ?? "";
  const given = req.headers.get("x-cron-secret") ?? "";
  if (!secret || !safeEqual(secret, given)) return json({ error: "unauthorized" }, 401);

  const pub = Deno.env.get("VAPID_PUBLIC_KEY");
  const priv = Deno.env.get("VAPID_PRIVATE_KEY");
  const subject = Deno.env.get("VAPID_SUBJECT");
  if (!pub || !priv || !subject) return json({ error: "VAPID secrets chưa đặt" }, 500);
  webpush.setVapidDetails(subject, pub, priv);

  const admin = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!, {
    auth: { persistSession: false },
  });

  const { data, error } = await admin.rpc("claim_push_reminders_due");
  if (error) return json({ error: error.message }, 500);
  const rows = (data ?? []) as DueRow[];

  let sent = 0;
  let removed = 0;
  let failed = 0;
  const dead: number[] = [];

  // Gửi theo mẻ nhỏ để không bắn hàng trăm kết nối cùng lúc.
  for (let i = 0; i < rows.length; i += 20) {
    await Promise.all(
      rows.slice(i, i + 20).map(async (r) => {
        const payload = JSON.stringify(buildPushPayload(r));
        try {
          await webpush.sendNotification(
            { endpoint: r.endpoint, keys: { p256dh: r.p256dh, auth: r.auth_key } },
            payload,
            { TTL: 6 * 60 * 60, urgency: "low" }, // hết hạn sau 6 giờ: tin cũ không còn ý nghĩa
          );
          sent++;
        } catch (e) {
          const code = (e as { statusCode?: number }).statusCode;
          if (code === 404 || code === 410) dead.push(r.subscription_id);
          else failed++;
        }
      }),
    );
  }

  if (dead.length) {
    const { error: delErr } = await admin.from("push_subscriptions").delete().in("id", dead);
    if (!delErr) removed = dead.length;
  }

  return json({ due: rows.length, sent, removed, failed });
});
