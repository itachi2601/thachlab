// Nội dung tin nhắc 1 lần/ngày (GĐ 2.6 / M4). Hàm thuần, không phụ thuộc Deno -> test được bằng
// `npx tsx scripts/test-push-message.mts`. Quy tắc: ngắn, một lời mời 5 phút, KHÔNG phạt/dọa mất chuỗi.

export interface DueReminder {
  topic_name: string | null;
  level: string | null; // 'weak' | 'practicing' | null
}

export interface PushPayload {
  title: string;
  body: string;
  url: string;
  tag: string;
}

const MAX_TOPIC = 60;

export function buildPushPayload(r: DueReminder): PushPayload {
  const name = (r.topic_name ?? "").replace(/\s+/g, " ").trim();
  let body = "Hôm nay luyện 5 phút nhé?";
  if (name) {
    const short = name.length > MAX_TOPIC ? name.slice(0, MAX_TOPIC - 1).trimEnd() + "…" : name;
    body = `Em còn ${r.level === "practicing" ? "🟡" : "🔴"} ${short} — 5 phút?`;
  }
  return { title: "ThachLab", body, url: "/lop-hoc/", tag: "thachlab-daily" };
}
