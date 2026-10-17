// AI (Claude, API trên console.anthropic.com) kiểm đề trước khi đăng: với từng câu trắc nghiệm/đúng–sai/
// trả lời ngắn, tự giải rồi đối chiếu với đáp án đã đánh dấu và lời giải; báo câu nghi sai đáp án, sai
// đơn vị/số liệu, lời giải mâu thuẫn, đề thiếu dữ kiện, lỗi chính tả/ký hiệu. Kết quả chỉ là GỢI Ý —
// trang không tự sửa câu nào, giáo viên đọc rồi quyết định.
//
// Gọi thẳng REST /v1/messages (không dùng SDK) để Edge Function không kéo thêm phụ thuộc npm, giống
// classify-questions. Thinking luôn bật trên các model 5.x (không gửi `thinking`, không gửi temperature);
// đầu ra ép bằng structured outputs (output_config.format); bật server-side `fallbacks: "default"`
// phòng khi bộ lọc an toàn từ chối.
//
// Cần secret ANTHROPIC_API_KEY (khoá tạo ở console.anthropic.com):
//   supabase secrets set ANTHROPIC_API_KEY=sk-ant-... --project-ref jgvbdbpvjdntdgzthumv
// Đổi model/độ sâu không cần sửa code: secret CHECK_EXAM_MODEL (mặc định claude-opus-5-5; rẻ hơn:
// claude-sonnet-5-5) và CHECK_EXAM_EFFORT (low|medium|high, mặc định medium).
// Deploy: supabase functions deploy check-exam --project-ref jgvbdbpvjdntdgzthumv

import { createClient } from "npm:@supabase/supabase-js@2";

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

const API_URL = "https://api.anthropic.com/v1/messages";
const DEFAULT_MODEL = "claude-opus-5-5";
const MAX_ITEMS = 30;
const VERDICTS = ["ok", "nghi_ngo", "loi"] as const;
type Verdict = (typeof VERDICTS)[number];

interface Item {
  index: number;
  text: string;
}
interface ResultRow {
  index: number;
  verdict: Verdict;
  note: string;
}

function jsonResponse(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
  });
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS_HEADERS });
  if (req.method !== "POST") return jsonResponse({ error: "method not allowed" }, 405);

  const authHeader = req.headers.get("Authorization") ?? "";
  if (!authHeader) return jsonResponse({ error: "Thiếu đăng nhập." }, 401);

  let body: { items?: unknown };
  try {
    body = await req.json();
  } catch {
    return jsonResponse({ error: "Dữ liệu gửi lên không hợp lệ." }, 400);
  }
  const items: Item[] = Array.isArray(body.items)
    ? body.items
        .filter(
          (it): it is Item =>
            !!it &&
            typeof (it as Item).index === "number" &&
            typeof (it as Item).text === "string" &&
            (it as Item).text.trim().length > 0,
        )
        .slice(0, MAX_ITEMS)
    : [];
  if (items.length === 0) return jsonResponse({ error: "Không có câu hỏi để kiểm." }, 400);

  const callerClient = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_ANON_KEY")!, {
    global: { headers: { Authorization: authHeader } },
    auth: { persistSession: false },
  });
  const { data: authUser, error: authError } = await callerClient.auth.getUser();
  if (authError || !authUser?.user) return jsonResponse({ error: "Phiên đăng nhập không hợp lệ." }, 401);

  const apiKey = Deno.env.get("ANTHROPIC_API_KEY");
  if (!apiKey) return jsonResponse({ error: "Server chưa cấu hình ANTHROPIC_API_KEY." }, 500);
  const model = Deno.env.get("CHECK_EXAM_MODEL") || DEFAULT_MODEL;
  const effort = Deno.env.get("CHECK_EXAM_EFFORT") || "medium";

  const itemList = items.map((it) => `--- Câu (index=${it.index}) ---\n${it.text}`).join("\n\n");
  const prompt =
    "Kiểm từng câu hỏi Vật lý THPT dưới đây. Với mỗi câu: tự giải độc lập (không tin đáp án đã đánh dấu), " +
    "rồi đối chiếu với đáp án đã đánh dấu và lời giải. Đánh giá `verdict`: " +
    '"ok" (đáp án đúng, đề đủ dữ kiện, lời giải khớp), ' +
    '"nghi_ngo" (đề mơ hồ/thiếu dữ kiện, lời giải lệch nhẹ, đơn vị hoặc ký hiệu đáng ngờ, chính tả), ' +
    '"loi" (đáp án đánh dấu sai so với cách giải của bạn, hoặc lời giải mâu thuẫn đáp án, hoặc có hai đáp án đúng/không có đáp án đúng). ' +
    "`note`: một câu tiếng Việt nêu đúng chỗ nghi và đáp án bạn tính ra (nếu khác); câu ok thì để chuỗi rỗng.\n\n" +
    itemList;

  const schema = {
    type: "object",
    properties: {
      results: {
        type: "array",
        items: {
          type: "object",
          properties: {
            index: { type: "integer" },
            verdict: { type: "string", enum: [...VERDICTS] },
            note: { type: "string" },
          },
          required: ["index", "verdict", "note"],
          additionalProperties: false,
        },
      },
    },
    required: ["results"],
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
          "Bạn là giáo viên Vật lý THPT kiểm đề trước khi đăng. Trả về đúng JSON theo schema, mỗi câu một mục.",
        messages: [{ role: "user", content: prompt }],
      }),
    });
    if (!res.ok) {
      return jsonResponse({ error: `Anthropic API lỗi ${res.status}: ${(await res.text()).slice(0, 300)}` }, 502);
    }
    const data = (await res.json()) as {
      stop_reason?: string;
      content?: { type: string; text?: string }[];
    };
    if (data.stop_reason === "refusal") return jsonResponse({ error: "AI từ chối kiểm lô câu này." }, 502);
    const raw = (data.content ?? []).filter((b) => b.type === "text").map((b) => b.text ?? "").join("");
    const start = raw.indexOf("{");
    const end = raw.lastIndexOf("}");
    if (start < 0 || end < 0) return jsonResponse({ error: "AI không trả về JSON hợp lệ." }, 502);
    const parsed = JSON.parse(raw.slice(start, end + 1)) as { results?: unknown };
    const rows = Array.isArray(parsed.results) ? parsed.results : [];

    const validIndexes = new Set(items.map((it) => it.index));
    const results: ResultRow[] = [];
    for (const row of rows) {
      if (!row || typeof row !== "object") continue;
      const r = row as Record<string, unknown>;
      const index = Number(r.index);
      if (!validIndexes.has(index)) continue;
      if (typeof r.verdict !== "string" || !(VERDICTS as readonly string[]).includes(r.verdict)) continue;
      results.push({ index, verdict: r.verdict as Verdict, note: typeof r.note === "string" ? r.note.slice(0, 500) : "" });
    }
    return jsonResponse({ results });
  } catch (cause) {
    return jsonResponse({ error: cause instanceof Error ? cause.message : String(cause) }, 500);
  }
});
