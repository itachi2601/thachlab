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

const SYSTEM = `Bạn là giáo viên Vật lý THPT. Một câu trắc nghiệm bị mất hình (đồ thị / hình vẽ) khi số hoá. Nhiệm vụ: dựng lại
ĐÚNG hình đó dựa trên câu dẫn, các phương án và lời giải, rồi nộp bằng công cụ submit_figure.

CÁCH NỘP — ưu tiên theo thứ tự:
A) "figure" (ĐẶC TẢ ĐỒ THỊ, dùng cho mọi đồ thị hàm số: x–t, v–t, a–t, d–t, p–V, p–T, V–T, nhiệt độ–thời gian,
   phóng xạ N–t, i–t, u–t, đồ thị hai đường…). Bạn CHỈ nêu thông số, mã của trang sẽ vẽ chính xác:
   - xLabel/yLabel: "t (s)", "x (cm)"…; xRange/yRange: khoảng vẽ [min, max] (bao trọn đồ thị, chừa lề ~10%).
   - xTicks/yTicks: các vạch chia CÓ GHI SỐ trên đồ thị gốc, dạng [{v: 0.2, label: "0,2"}]; nhãn ghi kiểu Việt Nam
     (dấu phẩy thập phân). Chỉ ghi các giá trị đủ để học sinh giải, KHÔNG ghi kết quả câu hỏi.
   - series: các đường. Loại:
       {type:"sinusoid", A, T, phi, y0, domain:[t0,t1]} với y = A·cos(2π·x/T + phi) + y0, phi tính bằng rad
         (đi qua gốc theo chiều dương ⇒ phi = −π/2 ≈ −1.5708; xuất phát ở biên dương ⇒ phi = 0; ở biên âm ⇒ phi = π;
         qua gốc theo chiều âm ⇒ phi = π/2). Kiểm tra lại: tại x = 0, y = A·cos(phi) + y0 phải đúng với lời giải.
       {type:"polyline", points:[[x,y],…]} cho đồ thị đoạn thẳng / gấp khúc (v–t đều, d–t, nhiệt độ–thời gian…).
       {type:"hyperbola", k, domain:[x0,x1]} cho y = k/x (đẳng nhiệt).
       {type:"exponential", y0, tau, yInf, domain} cho y = y0·e^(−x/tau) + yInf (phóng xạ, phóng điện).
     Mỗi đường có thể kèm label (chú thích khi ≥ 2 đường) và color (#2563eb, #dc2626, #16a34a).
   - points: các điểm được đánh dấu trên đồ thị gốc [{x, y, label?}]; guides: đường gióng nét đứt [{x?} | {y?}].
B) "svg" chỉ khi hình KHÔNG phải đồ thị hàm số (sơ đồ mạch điện đơn giản, hình vẽ vật – lò xo, tia sáng…):
   một thẻ <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 260" width="100%">, chữ font-size 12–13,
   nét stroke-width 2, dùng currentColor cho nét và chữ; KHÔNG <script>, <foreignObject>, on*, link ngoài, ảnh nhúng.

NGUYÊN TẮC
1. Chỉ vẽ khi văn bản đủ dữ kiện để hình khớp với lời giải. Thiếu dữ kiện, hoặc hình là ảnh chụp thí nghiệm / sơ đồ
   thiết bị thực / hình phức tạp không suy ra được → status "insufficient", nói rõ thiếu gì. KHÔNG bịa số liệu.
2. Hình để học sinh GIẢI ĐƯỢC nhưng KHÔNG lộ đáp án: chỉ ghi các giá trị đồ thị gốc chắc chắn có.
3. summary: 1–2 câu nêu hình vẽ gì và số liệu lấy từ đâu (câu dẫn hay lời giải) để giáo viên đối chiếu.`;

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
              figure: {
                type: "object",
                description: "Đặc tả đồ thị hàm số (ưu tiên). Chỉ dùng khi status = ok.",
                properties: {
                  xLabel: { type: "string" },
                  yLabel: { type: "string" },
                  xRange: { type: "array", items: { type: "number" }, minItems: 2, maxItems: 2 },
                  yRange: { type: "array", items: { type: "number" }, minItems: 2, maxItems: 2 },
                  xTicks: { type: "array", items: { type: "object", properties: { v: { type: "number" }, label: { type: "string" } }, required: ["v"] } },
                  yTicks: { type: "array", items: { type: "object", properties: { v: { type: "number" }, label: { type: "string" } }, required: ["v"] } },
                  series: {
                    type: "array",
                    items: {
                      type: "object",
                      properties: {
                        type: { type: "string", enum: ["sinusoid", "polyline", "hyperbola", "exponential"] },
                        A: { type: "number" },
                        T: { type: "number" },
                        phi: { type: "number" },
                        y0: { type: "number" },
                        tau: { type: "number" },
                        yInf: { type: "number" },
                        k: { type: "number" },
                        domain: { type: "array", items: { type: "number" } },
                        points: { type: "array", items: { type: "array", items: { type: "number" } } },
                        label: { type: "string" },
                        color: { type: "string" },
                        dashed: { type: "boolean" },
                      },
                      required: ["type"],
                    },
                  },
                  points: { type: "array", items: { type: "object", properties: { x: { type: "number" }, y: { type: "number" }, label: { type: "string" } }, required: ["x", "y"] } },
                  guides: { type: "array", items: { type: "object", properties: { x: { type: "number" }, y: { type: "number" }, label: { type: "string" } } } },
                },
                required: ["xLabel", "yLabel", "xRange", "yRange", "series"],
              },
              svg: { type: "string", description: "Mã SVG hoàn chỉnh — chỉ khi hình không phải đồ thị hàm số." },
              summary: { type: "string", description: "1–2 câu: hình vẽ gì, số liệu lấy từ đâu." },
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
    let input: Record<string, unknown> = tool?.input ?? {};
    // Đôi khi model bọc toàn bộ kết quả vào trong một khoá (vd { figure: { status, figure } }) — mở ra.
    if (typeof input.status !== "string") {
      for (const v of Object.values(input)) {
        if (v && typeof v === "object" && typeof (v as Record<string, unknown>).status === "string") {
          input = v as Record<string, unknown>;
          break;
        }
      }
    }
    if (input.status !== "ok") {
      const textBlock = response.content.find((b) => b.type === "text") as { type: "text"; text: string } | undefined;
      return jsonResponse({
        status: "insufficient",
        reason:
          typeof input.reason === "string" && input.reason
            ? input.reason
            : `AI không trả lời đúng định dạng (stop_reason=${response.stop_reason}, blocks=${response.content.map((b) => b.type).join(",")}${textBlock ? `, text=${textBlock.text.slice(0, 200)}` : ""}, input=${JSON.stringify(input).slice(0, 400)}).`,
      });
    }
    const summary = typeof input.summary === "string" ? input.summary : "";
    if (input.figure && typeof input.figure === "object" && Array.isArray((input.figure as { series?: unknown }).series))
      return jsonResponse({ status: "ok", figure: input.figure, summary });
    const svg = typeof input.svg === "string" ? sanitizeSvg(input.svg) : null;
    if (!svg) return jsonResponse({ status: "insufficient", reason: "AI trả về hình không hợp lệ." });
    return jsonResponse({ status: "ok", svg, summary });
  } catch (cause) {
    return jsonResponse({ error: cause instanceof Error ? cause.message : String(cause) }, 500);
  }
});
