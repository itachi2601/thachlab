// AI (Claude) vẽ lại đồ thị / hình minh hoạ cho một câu hỏi trong ngân hàng bị mất hình,
// dựa trên câu dẫn + phương án + lời giải. Trả về SVG để giáo viên XEM TRƯỚC và duyệt trên
// trang /quan-tri/ngan-hang-cau-hoi — server không tự ghi vào ngân hàng.
//
// Khi văn bản không đủ dữ kiện (không biết biên độ/chu kì/hình dạng…, hoặc là ảnh thí nghiệm,
// sơ đồ thực) thì trả status "insufficient" kèm lí do, KHÔNG bịa hình.
//
// Cần secret ANTHROPIC_API_KEY (dùng chung với classify-questions). Deploy:
//   supabase functions deploy draw-figure

import { createClient } from "npm:@supabase/supabase-js@2";
import Anthropic from "npm:@anthropic-ai/sdk";

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

const MODEL = "claude-sonnet-5";
const MAX_TEXT = 6000;

function jsonResponse(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
  });
}

function stripHtml(s: string): string {
  return s
    .replace(/<img[^>]*>/gi, " [ảnh] ")
    .replace(/<svg[\s\S]*?<\/svg>/gi, " [hình] ")
    .replace(/<[^>]+>/g, " ")
    .replace(/&nbsp;/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

const SYSTEM = `Bạn là giáo viên Vật lý THPT kiêm người vẽ hình minh hoạ cho đề trắc nghiệm. Một câu hỏi bị mất hình
(đồ thị / hình vẽ) khi số hoá. Nhiệm vụ: dựng lại ĐÚNG hình đó bằng SVG, dựa trên câu dẫn, các phương án và lời giải.

NGUYÊN TẮC
1. Chỉ vẽ khi văn bản đủ dữ kiện để hình khớp với lời giải (biên độ, chu kì, giá trị ban đầu, chiều, dạng đường,
   số liệu trên trục…). Thiếu dữ kiện, hoặc hình là ảnh chụp thí nghiệm / sơ đồ thiết bị thực / hình phức tạp không
   suy ra được → trả status "insufficient" và nói rõ thiếu gì. KHÔNG bịa số liệu.
2. Hình phải để học sinh GIẢI ĐƯỢC nhưng KHÔNG lộ đáp án: chỉ ghi lên trục các giá trị mà đồ thị gốc chắc chắn có
   (giá trị cực đại, thời điểm cắt trục, toạ độ điểm đặc biệt…), không ghi kết quả câu hỏi (ví dụ câu hỏi chu kì thì
   không ghi "T = 2 s", chỉ đánh dấu các mốc thời gian đủ để tính).
3. Đồ thị phải đúng toán học: dùng <path>/<polyline> với ít nhất 80 điểm tính từ hàm (ví dụ x = A cos(ωt + φ)),
   đúng pha ban đầu và chiều theo lời giải. Trục có mũi tên, nhãn đại lượng và đơn vị (x (cm), t (s), v (cm/s), p, V…).
   Gốc O, vạch chia có số. Đường lưới mờ nếu giúp đọc. Nhiều đồ thị trên cùng hệ trục thì khác màu và có chú thích.
4. Kĩ thuật SVG: một thẻ <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 W H" width="100%" style="max-width:440px;height:auto;display:block;margin:8px auto">
   với W trong 360–480, H trong 200–320. Chữ font-size 12–13, font-family sans-serif. Nét chính stroke-width 2.
   Nền trong suốt; màu chữ/trục dùng "currentColor" để hiện được cả nền tối và nền sáng; đường đồ thị dùng màu
   #2563eb, #dc2626, #16a34a. KHÔNG dùng <script>, <foreignObject>, sự kiện on*, liên kết ngoài, ảnh nhúng.
5. Chỉ dùng công cụ submit_figure để trả lời.`;

interface Body {
  question?: unknown;
  options?: unknown;
  statements?: unknown;
  explanation?: unknown;
}

function buildUserText(b: Body): string {
  const parts: string[] = [];
  parts.push(`CÂU DẪN:\n${stripHtml(String(b.question ?? ""))}`);
  if (Array.isArray(b.options) && b.options.length)
    parts.push(`PHƯƠNG ÁN:\n${b.options.map((o, i) => `${"ABCD"[i] ?? i + 1}. ${stripHtml(String(o))}`).join("\n")}`);
  if (Array.isArray(b.statements) && b.statements.length)
    parts.push(`CÁC Ý ĐÚNG–SAI:\n${b.statements.map((s, i) => `${"abcd"[i] ?? i + 1}) ${stripHtml(String(s))}`).join("\n")}`);
  const ex = stripHtml(String(b.explanation ?? ""));
  parts.push(ex ? `LỜI GIẢI (dùng để lấy số liệu của hình, không lộ vào hình):\n${ex}` : "LỜI GIẢI: (không có)");
  return parts.join("\n\n").slice(0, MAX_TEXT);
}

function sanitizeSvg(svg: string): string | null {
  let s = svg.trim().replace(/^<\?xml[^>]*>\s*/i, "");
  if (!/^<svg[\s>]/i.test(s) || !/<\/svg>\s*$/i.test(s)) return null;
  if (/<script|javascript:|\son[a-z]+\s*=|<foreignObject|<image|href\s*=\s*"(?!#)/i.test(s)) return null;
  if (!/xmlns=/.test(s)) s = s.replace(/^<svg/i, '<svg xmlns="http://www.w3.org/2000/svg"');
  if (!/\sstyle=/.test(s.slice(0, 400)))
    s = s.replace(/^<svg/i, '<svg style="max-width:440px;height:auto;display:block;margin:8px auto"');
  if (!/\swidth=/.test(s.slice(0, 400))) s = s.replace(/^<svg/i, '<svg width="100%"');
  return s;
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS_HEADERS });
  if (req.method !== "POST") return jsonResponse({ error: "method not allowed" }, 405);

  const authHeader = req.headers.get("Authorization") ?? "";
  if (!authHeader) return jsonResponse({ error: "Thiếu đăng nhập." }, 401);

  let body: Body;
  try {
    body = await req.json();
  } catch {
    return jsonResponse({ error: "Dữ liệu gửi lên không hợp lệ." }, 400);
  }
  if (typeof body.question !== "string" || !body.question.trim())
    return jsonResponse({ error: "Thiếu câu dẫn." }, 400);

  const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
  const anonKey = Deno.env.get("SUPABASE_ANON_KEY")!;
  const callerClient = createClient(supabaseUrl, anonKey, {
    global: { headers: { Authorization: authHeader } },
    auth: { persistSession: false },
  });
  const { data: authUser, error: authError } = await callerClient.auth.getUser();
  if (authError || !authUser?.user) return jsonResponse({ error: "Phiên đăng nhập không hợp lệ." }, 401);
  const { data: profile } = await callerClient
    .from("profiles")
    .select("role")
    .eq("id", authUser.user.id)
    .maybeSingle();
  if (!profile || !["admin", "instructor"].includes(String(profile.role)))
    return jsonResponse({ error: "Chỉ giáo viên mới dùng được." }, 403);

  const apiKey = Deno.env.get("ANTHROPIC_API_KEY");
  if (!apiKey) return jsonResponse({ error: "Server chưa cấu hình ANTHROPIC_API_KEY." }, 500);

  try {
    const client = new Anthropic({ apiKey });
    const response = await client.messages.create({
      model: MODEL,
      max_tokens: 8000,
      system: SYSTEM,
      tools: [
        {
          name: "submit_figure",
          description: "Nộp hình đã vẽ, hoặc báo không đủ dữ kiện.",
          input_schema: {
            type: "object",
            properties: {
              status: { type: "string", enum: ["ok", "insufficient"] },
              svg: { type: "string", description: "Mã SVG hoàn chỉnh khi status = ok." },
              summary: {
                type: "string",
                description: "1–2 câu mô tả hình đã vẽ và các số liệu lấy từ đâu (để giáo viên đối chiếu).",
              },
              reason: { type: "string", description: "Khi status = insufficient: thiếu dữ kiện gì." },
            },
            required: ["status"],
          },
        },
      ],
      tool_choice: { type: "tool", name: "submit_figure" },
      messages: [{ role: "user", content: buildUserText(body) }],
    });

    const tool = response.content.find((b) => b.type === "tool_use") as
      | { type: "tool_use"; input: Record<string, unknown> }
      | undefined;
    const input = tool?.input ?? {};
    if (input.status !== "ok") {
      return jsonResponse({
        status: "insufficient",
        reason: typeof input.reason === "string" && input.reason ? input.reason : "AI không đủ dữ kiện để vẽ.",
      });
    }
    const svg = typeof input.svg === "string" ? sanitizeSvg(input.svg) : null;
    if (!svg) return jsonResponse({ status: "insufficient", reason: "AI trả về SVG không hợp lệ." });
    return jsonResponse({ status: "ok", svg, summary: typeof input.summary === "string" ? input.summary : "" });
  } catch (cause) {
    return jsonResponse({ error: cause instanceof Error ? cause.message : String(cause) }, 500);
  }
});
