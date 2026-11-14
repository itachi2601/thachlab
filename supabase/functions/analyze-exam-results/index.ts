// AI (Claude) phân tích bài làm CẢ LỚP của một đề trước khi giáo viên chữa: đọc số liệu gộp (tỉ lệ đúng
// từng câu, phương án sai được chọn nhiều, ý a–d sai nhiều, đáp số sai hay gặp) rồi trả về:
//   - nhận xét chung 2–3 câu;
//   - chủ đề cần ôn lại, xếp theo mức ưu tiên, kèm lý do + cách ôn + câu minh chứng;
//   - chẩn đoán lỗi hiểu sai cho các câu khó + gợi ý cách chữa trên lớp;
//   - thứ tự chữa gợi ý.
// Chỉ nhận số liệu gộp — client không gửi tên/mã học sinh. Kết quả chỉ là GỢI Ý cho giáo viên.
//
// Gọi thẳng REST /v1/messages (không SDK) như check-exam. Thinking luôn bật trên model 5.x — điều chỉnh
// bằng output_config.effort; đầu ra ép bằng structured outputs; bật fallbacks "default" phòng từ chối.
//
// Dùng chung secret ANTHROPIC_API_KEY với check-exam (đã đặt). Đổi model/độ sâu không cần sửa code:
//   ANALYZE_EXAM_MODEL (mặc định claude-opus-5-5) · ANALYZE_EXAM_EFFORT (low|medium|high, mặc định medium)
// Deploy: supabase functions deploy analyze-exam-results --project-ref jgvbdbpvjdntdgzthumv

import { createClient } from "npm:@supabase/supabase-js@2";

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": Deno.env.get("ALLOWED_ORIGIN") ?? "https://thachlab.id.vn",
  Vary: "Origin",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

const API_URL = "https://api.anthropic.com/v1/messages";
const DEFAULT_MODEL = "claude-opus-5-5";
const MAX_QUESTIONS = 60;
const MAX_PAYLOAD_CHARS = 60_000;
const PRIORITIES = ["cao", "vua", "thap"] as const;

const CALLS_PER_HOUR = Number(Deno.env.get("AI_CALLS_PER_HOUR") ?? "40");
const callLog = new Map<string, number[]>();
function overQuota(userId: string): boolean {
  const now = Date.now();
  const recent = (callLog.get(userId) ?? []).filter((t) => now - t < 3_600_000);
  if (recent.length >= CALLS_PER_HOUR) {
    callLog.set(userId, recent);
    return true;
  }
  recent.push(now);
  callLog.set(userId, recent);
  return false;
}

function jsonResponse(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
  });
}

const str = (v: unknown, max = 600) => (typeof v === "string" ? v.slice(0, max) : "");

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS_HEADERS });
  if (req.method !== "POST") return jsonResponse({ error: "method not allowed" }, 405);

  const authHeader = req.headers.get("Authorization") ?? "";
  if (!authHeader) return jsonResponse({ error: "Thiếu đăng nhập." }, 401);

  let body: { examTitle?: unknown; attempts?: unknown; questions?: unknown };
  try {
    body = await req.json();
  } catch {
    return jsonResponse({ error: "Dữ liệu gửi lên không hợp lệ." }, 400);
  }
  const questions = Array.isArray(body.questions) ? body.questions.slice(0, MAX_QUESTIONS) : [];
  const attempts = Number(body.attempts) || 0;
  if (questions.length === 0) return jsonResponse({ error: "Đề không có câu hỏi." }, 400);
  if (attempts === 0) return jsonResponse({ error: "Lớp chưa có lượt nộp nào để phân tích." }, 400);
  const dataJson = JSON.stringify(questions);
  if (dataJson.length > MAX_PAYLOAD_CHARS) return jsonResponse({ error: "Đề quá dài để phân tích một lượt." }, 413);

  const callerClient = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_ANON_KEY")!, {
    global: { headers: { Authorization: authHeader } },
    auth: { persistSession: false },
  });
  const { data: authUser, error: authError } = await callerClient.auth.getUser();
  if (authError || !authUser?.user) return jsonResponse({ error: "Phiên đăng nhập không hợp lệ." }, 401);
  const { data: isStaff } = await callerClient.rpc("is_staff");
  if (!isStaff) return jsonResponse({ error: "Chỉ giáo viên/trợ giảng được dùng chức năng AI này." }, 403);
  if (overQuota(authUser.user.id)) return jsonResponse({ error: "Đã quá số lượt AI trong 1 giờ — thử lại sau." }, 429);

  const apiKey = Deno.env.get("ANTHROPIC_API_KEY");
  if (!apiKey) return jsonResponse({ error: "Server chưa cấu hình ANTHROPIC_API_KEY." }, 500);
  const model = Deno.env.get("ANALYZE_EXAM_MODEL") || DEFAULT_MODEL;
  const effort = Deno.env.get("ANALYZE_EXAM_EFFORT") || "medium";

  const prompt =
    `Đề: "${str(body.examTitle, 200)}". Số học sinh đã nộp (lượt gần nhất mỗi em): ${attempts}.\n` +
    "Dưới đây là số liệu gộp cả lớp cho từng câu (JSON). Trường: index (0-based; khi nói với giáo viên dùng " +
    '"Câu index+1"), type, topic (chủ đề đã gắn, có thể rỗng), pct (% cả lớp làm đúng trọn câu), text (đề rút gọn), ' +
    "options[].pct (% chọn mỗi phương án), answer (đáp án đúng), statements[].pctCorrect (% chọn đúng ở mỗi ý a–d), " +
    "wrongAnswers (đáp số sai hay gặp + số em), explanation (lời giải, nếu có).\n\n" +
    "Nhiệm vụ — chuẩn bị cho giáo viên Vật lí THPT TRƯỚC buổi chữa bài:\n" +
    "1) `overview`: 2–3 câu nhận xét chung (lớp vững phần nào, hổng phần nào), cụ thể, không chung chung.\n" +
    "2) `topics`: 2–6 chủ đề CẦN ÔN LẠI, xếp ưu tiên giảm dần. Ưu tiên dùng đúng tên `topic` đã gắn; nếu câu chưa gắn " +
    "chủ đề thì tự đặt tên chủ đề ngắn theo nội dung (theo chương trình GDPT 2018). `priority` cao|vua|thap; `reason` 1 câu " +
    "nêu bằng chứng số liệu; `reviewTip` 1–2 câu gợi ý ôn (kiến thức/công thức/kỹ năng cần nhắc lại); `questionIndexes` các câu minh chứng.\n" +
    "3) `questions`: với các câu pct < 60 (tối đa 8 câu, sai nhiều nhất trước), `misconception` = học sinh nhiều khả năng hiểu sai/" +
    "nhầm ở đâu, suy ra từ phương án nhiễu được chọn hoặc đáp số sai (vd nhầm đơn vị, quên bình phương, nhầm dấu); " +
    "`teachingTip` = cách chữa ngắn trên lớp (câu hỏi gợi mở, hình/ví dụ phản chứng). Không đoán bừa: số liệu không đủ thì nói rõ.\n" +
    "4) `reviewOrder`: thứ tự chữa gợi ý (index), gom câu cùng chủ đề/lỗi gần nhau, bỏ câu ≥ 85% đúng.\n" +
    "Viết tiếng Việt, ngắn gọn, giọng đồng nghiệp; công thức dùng $…$.\n\n" +
    dataJson;

  const schema = {
    type: "object",
    properties: {
      overview: { type: "string" },
      topics: {
        type: "array",
        items: {
          type: "object",
          properties: {
            topic: { type: "string" },
            priority: { type: "string", enum: [...PRIORITIES] },
            reason: { type: "string" },
            reviewTip: { type: "string" },
            questionIndexes: { type: "array", items: { type: "integer" } },
          },
          required: ["topic", "priority", "reason", "reviewTip", "questionIndexes"],
          additionalProperties: false,
        },
      },
      questions: {
        type: "array",
        items: {
          type: "object",
          properties: {
            index: { type: "integer" },
            misconception: { type: "string" },
            teachingTip: { type: "string" },
          },
          required: ["index", "misconception", "teachingTip"],
          additionalProperties: false,
        },
      },
      reviewOrder: { type: "array", items: { type: "integer" } },
    },
    required: ["overview", "topics", "questions", "reviewOrder"],
    additionalProperties: false,
  };

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "x-api-key": apiKey,
        "anthropic-version": "2023-06-01",
        "anthropic-beta": "server-side-fallback-2026-07-01",
      },
      body: JSON.stringify({
        model,
        max_tokens: 16000,
        fallbacks: "default",
        output_config: { effort, format: { type: "json_schema", schema } },
        system:
          "Bạn là tổ trưởng chuyên môn Vật lí THPT, giúp đồng nghiệp chuẩn bị buổi chữa đề. Trả về đúng JSON theo schema.",
        messages: [{ role: "user", content: prompt }],
      }),
    });
    if (!res.ok) {
      return jsonResponse({ error: `Anthropic API lỗi ${res.status}: ${(await res.text()).slice(0, 300)}` }, 502);
    }
    const data = (await res.json()) as { stop_reason?: string; content?: { type: string; text?: string }[] };
    if (data.stop_reason === "refusal") return jsonResponse({ error: "AI từ chối phân tích đề này." }, 502);
    if (data.stop_reason === "max_tokens") return jsonResponse({ error: "AI trả lời quá dài, bị cắt — thử lại." }, 502);
    const raw = (data.content ?? []).filter((b) => b.type === "text").map((b) => b.text ?? "").join("");
    const start = raw.indexOf("{");
    const end = raw.lastIndexOf("}");
    if (start < 0 || end < 0) return jsonResponse({ error: "AI không trả về JSON hợp lệ." }, 502);
    const parsed = JSON.parse(raw.slice(start, end + 1)) as Record<string, unknown>;

    const n = questions.length;
    const validIdx = (v: unknown) => Number.isInteger(v) && (v as number) >= 0 && (v as number) < n;
    const topics = (Array.isArray(parsed.topics) ? parsed.topics : []).slice(0, 8).flatMap((t) => {
      const o = (t ?? {}) as Record<string, unknown>;
      const topic = str(o.topic, 120).trim();
      if (!topic) return [];
      const priority = (PRIORITIES as readonly string[]).includes(o.priority as string) ? o.priority : "vua";
      return [
        {
          topic,
          priority,
          reason: str(o.reason),
          reviewTip: str(o.reviewTip),
          questionIndexes: (Array.isArray(o.questionIndexes) ? o.questionIndexes : []).filter(validIdx).slice(0, 20),
        },
      ];
    });
    const qNotes = (Array.isArray(parsed.questions) ? parsed.questions : []).slice(0, 12).flatMap((q) => {
      const o = (q ?? {}) as Record<string, unknown>;
      if (!validIdx(o.index)) return [];
      return [{ index: o.index as number, misconception: str(o.misconception), teachingTip: str(o.teachingTip) }];
    });
    const reviewOrder = [...new Set((Array.isArray(parsed.reviewOrder) ? parsed.reviewOrder : []).filter(validIdx))];

    return jsonResponse({ overview: str(parsed.overview, 1200), topics, questions: qNotes, reviewOrder, model });
  } catch (cause) {
    return jsonResponse({ error: cause instanceof Error ? cause.message : String(cause) }, 500);
  }
});
