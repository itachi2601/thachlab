// Nội dung tin nhắc 1 lần/ngày (GĐ 2.6 / M4). Hàm thuần, không phụ thuộc Deno -> test được bằng
// `npx tsx scripts/test-push-message.mts`. Quy tắc: ngắn, một lời mời 5 phút, KHÔNG phạt/dọa mất chuỗi.
// Luân phiên 3 mẫu (kiểu Duolingo: mẫu lặp mãi thì nhàm, nhưng không cần bandit khi chưa đủ dữ liệu);
// lâu chưa học thì đổi giọng sang "chờ em quay lại", không tăng áp lực.

export interface DueReminder {
  topic_name: string | null;
  level: string | null; // 'weak' | 'practicing' | null
  inactive_days?: number | null;
  /** Số để chọn mẫu: ngày + id đăng ký -> mỗi ngày một mẫu khác, mỗi thiết bị lệch nhau. */
  seed?: number;
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
  const k = Math.abs(Math.trunc(r.seed ?? 0)) % 3;
  const idle = r.inactive_days ?? 0;
  let body: string;
  if (idle >= 7) {
    body = "ThachLab vẫn chờ em. Khi sẵn sàng, em vào luyện 5 phút nhé.";
  } else if (idle >= 5) {
    body = "Lâu rồi chưa gặp em. Quay lại với 5 phút nhé?";
  } else if (name) {
    const short = name.length > MAX_TOPIC ? name.slice(0, MAX_TOPIC - 1).trimEnd() + "…" : name;
    const dot = r.level === "practicing" ? "🟡" : "🔴";
    body = [`Em còn ${dot} ${short} — 5 phút?`, `${short} đang chờ em. 5 phút thôi nhé?`, `Luyện nhanh ${short}, chỉ 5 phút.`][k];
  } else {
    body = ["Hôm nay luyện 5 phút nhé?", "5 phút luyện tập, em sẵn sàng chưa?", "Một bài ngắn cho hôm nay nhé?"][k];
  }
  return { title: "ThachLab", body, url: "/lop-hoc/", tag: "thachlab-daily" };
}
