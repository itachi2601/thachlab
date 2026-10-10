// AI chấm câu tự luận / trả lời ngắn cho bảng chấm nhanh HSG KHTN 9 (/quan-tri/hsg-cham-bai).
// Nhận lô câu {n, question, reference, max, answer} — KHÔNG nhận tên học sinh — trả điểm + nhận xét.
// Điểm chỉ là gợi ý: trang gọi hiển thị để giáo viên sửa tay trước khi lưu.
//
// Provider chọn theo body.provider: "deepseek" (secret DEEPSEEK_API_KEY, model HSG_GRADE_DEEPSEEK_MODEL,
// mặc định deepseek-flash) hoặc "haiku" (secret ANTHROPIC_API_KEY, model HSG_GRADE_HAIKU_MODEL, mặc định
// claude-haiku-5-5). Deploy: supabase functions deploy hsg-ai-grade (secrets xem docs/deploy-edge-function.md).

import { createClient } from "npm:@supabase/supabase-js@2";

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};
const MAX_ITEMS = 20;

interface Item {
  n: number;
  question: string;
  reference: string;
  max: number;
  answer: string;
}

function jsonResponse(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
  });
}

const SYSTEM =
  "Bạn là giám khảo chấm bài thi Vật lí học sinh giỏi lớp 9 (Việt Nam). Với mỗi câu, so bài làm của học sinh " +
  "với đáp án/biểu điểm tham chiếu và cho điểm trong khoảng [0, max], bước 0,25. Chấm theo từng ý đúng của " +
  "biểu điểm; kết quả cuối đúng nhưng lập luận sai/thiếu thì trừ; đúng hướng nhưng sai số học thì cho điểm " +
  "phần phương pháp. Bài trống hoặc không liên quan → 0. Nhận xét tối đa 25 từ, nêu ý thiếu/sai chính. " +
  'Chỉ trả DUY NHẤT một JSON: {"results":[{"n":1,"got":1.5,"comment":"..."}]}, không markdown.';

function buildPrompt(items: Item[]): string {
  return items
    .map(
      (it) =>
        `--- Câu ${it.n} (điểm tối đa ${it.max}) ---\nĐề: ${it.question}\nĐáp án/biểu điểm: ${it.reference}\nBài làm của học sinh: ${it.answer || "(để trống)"}`,
    )
    .join("\n\n");
}

async function callDeepSeek(prompt: string): Promise<string> {
  const apiKey = Deno.env.get("DEEPSEEK_API_KEY");
  if (!apiKey) throw new Error("Server chưa cấu hình DEEPSEEK_API_KEY.");
  const res = await fetch("https://api.deepseek.com/chat/completions", {
    method: "POST",
    headers: { "content-type": "application/json", authorization: `Bearer ${apiKey}` },
    body: JSON.stringify({
      model: Deno.env.get("HSG_GRADE_DEEPSEEK_MODEL") || "deepseek-flash",
      max_tokens: 4096,
      temperature: 0,
      thinking: { type: "disabled" },
      response_format: { type: "json_object" },
      messages: [
        { role: "system", content: SYSTEM },
        { role: "user", content: prompt + "\n\nTrả về json." },
      ],
    }),
  });
  if (!res.ok) throw new Error(`DeepSeek lỗi ${res.status}: ${(await res.text()).slice(0, 300)}`);
  const data = await res.json();
  return data.choices?.[0]?.message?.content ?? "";
}

async function callHaiku(prompt: string): Promise<string> {
  const apiKey = Deno.env.get("ANTHROPIC_API_KEY");
  if (!apiKey) throw new Error("Server chưa cấu hình ANTHROPIC_API_KEY.");
  const res = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "content-type": "application/json",
      "x-api-key": apiKey,
      "anthropic-version": "2023-06-01",
    },
    body: JSON.stringify({
      model: Deno.env.get("HSG_GRADE_HAIKU_MODEL") || "claude-haiku-5-5",
      max_tokens: 4096,
      system: SYSTEM,
      messages: [{ role: "user", content: prompt }],
    }),
  });
  if (!res.ok) throw new Error(`Anthropic lỗi ${res.status}: ${(await res.text()).slice(0, 300)}`);
  const data = await res.json();
  return (data.content ?? []).map((b: { text?: string }) => b.text ?? "").join("");
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS_HEADERS });
  if (req.method !== "POST") return jsonResponse({ error: "method not allowed" }, 405);
  const authHeader = req.headers.get("Authorization") ?? "";
  if (!authHeader) return jsonResponse({ error: "Thiếu đăng nhập." }, 401);

  let body: { provider?: unknown; items?: unknown };
  try {
    body = await req.json();
  } catch {
    return jsonResponse({ error: "Dữ liệu gửi lên không hợp lệ." }, 400);
  }
  const provider = body.provider === "haiku" ? "haiku" : "deepseek";
  const items: Item[] = (Array.isArray(body.items) ? body.items : [])
    .filter((it): it is Item => !!it && typeof (it as Item).n === "number" && Number((it as Item).max) > 0)
    .slice(0, MAX_ITEMS)
    .map((it) => ({
      n: it.n,
      question: String(it.question ?? "").slice(0, 3000),
      reference: String(it.reference ?? "").slice(0, 3000),
      max: Number(it.max),
      answer: String(it.answer ?? "").slice(0, 6000),
    }));
  if (items.length === 0) return jsonResponse({ error: "Không có câu nào để chấm." }, 400);

  const callerClient = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_ANON_KEY")!, {
    global: { headers: { Authorization: authHeader } },
    auth: { persistSession: false },
  });
  const { data: authUser, error: authError } = await callerClient.auth.getUser();
  if (authError || !authUser?.user) return jsonResponse({ error: "Phiên đăng nhập không hợp lệ." }, 401);
  const { data: isStaff } = await callerClient.rpc("is_staff");
  if (!isStaff) return jsonResponse({ error: "Chỉ giáo viên/trợ giảng được dùng chấm AI." }, 403);

  try {
    const raw = provider === "haiku" ? await callHaiku(buildPrompt(items)) : await callDeepSeek(buildPrompt(items));
    const start = raw.indexOf("{");
    const end = raw.lastIndexOf("}");
    if (start < 0 || end < 0) return jsonResponse({ error: "AI không trả về JSON hợp lệ." }, 502);
    const parsed = JSON.parse(raw.slice(start, end + 1)) as { results?: unknown };
    const maxByN = new Map(items.map((it) => [it.n, it.max]));
    const results = (Array.isArray(parsed.results) ? parsed.results : [])
      .map((r) => r as Record<string, unknown>)
      .filter((r) => maxByN.has(Number(r.n)) && Number.isFinite(Number(r.got)))
      .map((r) => ({
        n: Number(r.n),
        got: Math.min(maxByN.get(Number(r.n))!, Math.max(0, Math.round(Number(r.got) * 4) / 4)),
        comment: String(r.comment ?? "").slice(0, 300),
      }));
    return jsonResponse({ results });
  } catch (cause) {
    return jsonResponse({ error: cause instanceof Error ? cause.message : String(cause) }, 500);
  }
});
