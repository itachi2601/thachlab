// Đẩy thông báo trong web ra màn hình khoá (Web Push, rung máy). Gọi MỖI PHÚT bởi pg_cron + pg_net
// (xem docs/PUSH-NHAC-HANG-NGAY.md mục "Push thông báo"). Dùng chung secrets với send-daily-push:
// VAPID_PUBLIC_KEY, VAPID_PRIVATE_KEY, VAPID_SUBJECT, PUSH_CRON_SECRET. Deploy bằng --no-verify-jwt.
// RPC claim_notification_pushes tự đánh dấu pushed_at nên chạy trùng không gửi 2 lần.
// KHÔNG typecheck được (không có deno) — phải bấm thử thật sau deploy.

import { createClient } from "npm:@supabase/supabase-js@2";
import webpush from "npm:web-push@3.6.7";

function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json" } });
}

function safeEqual(a: string, b: string) {
  if (a.length !== b.length) return false;
  let d = 0;
  for (let i = 0; i < a.length; i++) d |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return d === 0;
}

interface Row {
  notification_id: number;
  subscription_id: number;
  endpoint: string;
  p256dh: string;
  auth_key: string;
  title: string;
  body: string;
  href: string;
}

Deno.serve(async (req) => {
  if (req.method !== "POST") return json({ error: "method not allowed" }, 405);
  const secret = Deno.env.get("PUSH_CRON_SECRET") ?? "";
  if (!secret || !safeEqual(secret, req.headers.get("x-cron-secret") ?? "")) return json({ error: "unauthorized" }, 401);

  const pub = Deno.env.get("VAPID_PUBLIC_KEY");
  const priv = Deno.env.get("VAPID_PRIVATE_KEY");
  const subject = Deno.env.get("VAPID_SUBJECT");
  if (!pub || !priv || !subject) return json({ error: "VAPID secrets chưa đặt" }, 500);
  webpush.setVapidDetails(subject, pub, priv);

  const admin = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!, {
    auth: { persistSession: false },
  });
  const { data, error } = await admin.rpc("claim_notification_pushes");
  if (error) return json({ error: error.message }, 500);
  const rows = (data ?? []) as Row[];

  let sent = 0;
  let failed = 0;
  const dead: number[] = [];
  for (let i = 0; i < rows.length; i += 20) {
    await Promise.all(
      rows.slice(i, i + 20).map(async (r) => {
        const url = r.href && r.href.startsWith("/") ? r.href : "/thong-bao/";
        const payload = JSON.stringify({
          title: r.title.slice(0, 80),
          body: (r.body ?? "").slice(0, 140),
          url,
          tag: "tb-" + r.notification_id,
          kind: "notification",
        });
        try {
          await webpush.sendNotification({ endpoint: r.endpoint, keys: { p256dh: r.p256dh, auth: r.auth_key } }, payload, {
            TTL: 60 * 60,
            urgency: "high",
          });
          sent++;
        } catch (e) {
          const code = (e as { statusCode?: number }).statusCode;
          if (code === 404 || code === 410) dead.push(r.subscription_id);
          else failed++;
        }
      }),
    );
  }
  if (dead.length) await admin.from("push_subscriptions").delete().in("id", dead);
  return json({ due: rows.length, sent, removed: dead.length, failed });
});
