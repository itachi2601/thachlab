// Chỉ đọc: bảng giá video/thưởng và phiếu video T9–T10. Chạy: node --env-file=.env.local scripts/doc-thuong-tro-giang.mjs
import { createClient } from "@supabase/supabase-js";
const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY, { auth: { persistSession: false } });
console.log("VIDEO_RATES", JSON.stringify((await sb.from("ta_video_rates").select("*")).data));
const { data } = await sb.from("ta_sessions").select("assistant_id,work_date,video_tier,status").eq("session_type", "video").gte("work_date", "2026-09-01");
console.log("VIDEO_SESSIONS", JSON.stringify(data));
