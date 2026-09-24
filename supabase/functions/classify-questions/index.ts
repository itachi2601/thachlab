// AI (Claude) gợi ý Chủ đề (yêu cầu cần đạt) + Dạng (lý thuyết/bài tập) cho các câu hỏi còn
// thiếu nhãn khi soạn đề ở trang Đăng đề — chỉ được chọn trong đúng danh mục YCCĐ của bài đang
// soạn (gửi kèm trong `topics`), không tự đặt tên chủ đề mới. Kết quả được trang gọi ghi thẳng
// vào văn bản đề (như khi giáo viên tự chọn ở bảng "Phân loại câu"), không qua bước duyệt riêng.
//
// Cần secret ANTHROPIC_API_KEY (KHÔNG tự có như SUPABASE_* — chạy một lần:
//   supabase secrets set ANTHROPIC_API_KEY=sk-ant-...
// rồi supabase functions deploy classify-questions). Xem docs/deploy-edge-function.md cho các
// bước cài CLI/login/link (dùng chung với mọi Edge Function trong dự án).

import { createClient } from "npm:@supabase/supabase-js@2";
import Anthropic from "npm:@anthropic-ai/sdk";

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

const MODEL = "claude-haiku-4-5";
const MAX_ITEMS = 60;
const FORMS = ["ly_thuyet", "bai_tap"] as const;
type Form = (typeof FORMS)[number];
const DIFFICULTIES = ["de", "trung-binh", "kho"] as const;
type Difficulty = (typeof DIFFICULTIES)[number];

interface Item {
  index: number;
  text: string;
}
interface ResultRow {
  index: number;
  topic?: string;
  form?: Form;
  difficulty?: Difficulty;
}

function jsonResponse(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
  });
}

function buildPrompt(topics: string[], items: Item[]): string {
  const topicList = topics.map((t, i) => `${i + 1}. ${t}`).join("\n");
  const itemList = items.map((it) => `--- Câu (index=${it.index}) ---\n${it.text}`).join("\n\n");
  return (
    `Danh mục yêu cầu cần đạt (chỉ được chọn NGUYÊN VĂN một mục trong danh sách này cho mỗi câu, ` +
    `không tự đặt tên mới, không sửa chính tả):\n${topicList}\n\n` +
    `Phân loại từng câu hỏi Vật lý THPT dưới đây: chọn đúng 1 yêu cầu cần đạt phù hợp nhất trong ` +
    `danh mục trên, xác định "form" là "ly_thuyet" (câu hỏi lý thuyết/khái niệm/định nghĩa, ` +
    `không cần tính toán) hoặc "bai_tap" (câu có số liệu/công thức/tính toán để ra đáp số), và xác định ` +
    `"difficulty" — độ khó với học sinh THPT trung bình — là "de" (nhận biết/áp dụng công thức trực ` +
    `tiếp, 1 bước tính), "trung-binh" (cần 2-3 bước biến đổi hoặc kết hợp 2 khái niệm), hoặc "kho" ` +
    `(nhiều bước, đồ thị/tình huống phức tạp, hoặc dễ nhầm lẫn).\n\n${itemList}`
  );
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS_HEADERS });
  if (req.method !== "POST") return jsonResponse({ error: "method not allowed" }, 405);

  const authHeader = req.headers.get("Authorization") ?? "";
  if (!authHeader) return jsonResponse({ error: "Thiếu đăng nhập." }, 401);

  let body: { topics?: unknown; items?: unknown };
  try {
    body = await req.json();
  } catch {
    return jsonResponse({ error: "Dữ liệu gửi lên không hợp lệ." }, 400);
  }
  const topics = Array.isArray(body.topics)
    ? body.topics.map(String).map((t) => t.trim()).filter(Boolean)
    : [];
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
  if (topics.length === 0 || items.length === 0) {
    return jsonResponse({ error: "Thiếu danh mục chủ đề hoặc danh sách câu hỏi." }, 400);
  }

  const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
  const anonKey = Deno.env.get("SUPABASE_ANON_KEY")!;
  const callerClient = createClient(supabaseUrl, anonKey, {
    global: { headers: { Authorization: authHeader } },
    auth: { persistSession: false },
  });
  const { data: authUser, error: authError } = await callerClient.auth.getUser();
  if (authError || !authUser?.user) return jsonResponse({ error: "Phiên đăng nhập không hợp lệ." }, 401);

  const apiKey = Deno.env.get("ANTHROPIC_API_KEY");
  if (!apiKey) return jsonResponse({ error: "Server chưa cấu hình ANTHROPIC_API_KEY." }, 500);

  try {
    const client = new Anthropic({ apiKey });
    const response = await client.messages.create({
      model: MODEL,
      max_tokens: 4096,
      system:
        "Bạn là trợ lý phân loại câu hỏi trắc nghiệm Vật lý THPT theo yêu cầu cần đạt (YCCĐ). " +
        'Chỉ trả về DUY NHẤT một JSON hợp lệ đúng dạng ' +
        '{"results":[{"index":0,"topic":"...","form":"ly_thuyet","difficulty":"de"}]}, ' +
        "không kèm lời giải thích, không bọc trong markdown code fence.",
      messages: [{ role: "user", content: buildPrompt(topics, items) }],
    });

    const textBlock = response.content.find((b) => b.type === "text") as { type: "text"; text: string } | undefined;
    const raw = textBlock?.text ?? "";
    const start = raw.indexOf("{");
    const end = raw.lastIndexOf("}");
    if (start < 0 || end < 0) return jsonResponse({ error: "AI không trả về JSON hợp lệ." }, 502);
    const parsed = JSON.parse(raw.slice(start, end + 1)) as { results?: unknown };
    const rows = Array.isArray(parsed.results) ? parsed.results : [];

    const topicSet = new Set(topics);
    const validIndexes = new Set(items.map((it) => it.index));
    const results: ResultRow[] = [];
    for (const row of rows) {
      if (!row || typeof row !== "object") continue;
      const r = row as Record<string, unknown>;
      const index = Number(r.index);
      if (!validIndexes.has(index)) continue;
      const out: ResultRow = { index };
      if (typeof r.topic === "string" && topicSet.has(r.topic)) out.topic = r.topic;
      if (typeof r.form === "string" && (FORMS as readonly string[]).includes(r.form)) out.form = r.form as Form;
      if (typeof r.difficulty === "string" && (DIFFICULTIES as readonly string[]).includes(r.difficulty))
        out.difficulty = r.difficulty as Difficulty;
      if (out.topic || out.form || out.difficulty) results.push(out);
    }
    return jsonResponse({ results });
  } catch (cause) {
    return jsonResponse({ error: cause instanceof Error ? cause.message : String(cause) }, 500);
  }
});
