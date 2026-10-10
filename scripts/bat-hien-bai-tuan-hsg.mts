// Bật Hiện bài 167 (Bài tập tuần này, HSG) và cập nhật nội dung thông báo post đã đăng từ scripts/data/thong-bao-hsg9/*.json.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
const env = Object.fromEntries(fs.readFileSync(".env.local", "utf8").split("\n").filter((l) => l.includes("=")).map((l) => [l.slice(0, l.indexOf("=")), l.slice(l.indexOf("=") + 1).trim()]));
const sb = createClient(env.NEXT_PUBLIC_SUPABASE_URL, env.SUPABASE_SERVICE_ROLE_KEY);
const n = JSON.parse(fs.readFileSync("scripts/data/thong-bao-hsg9/co-hoc-vd-vdc-2026-10-11.json", "utf8"));
const r1 = await sb.from("lessons").update({ published: true }).eq("id", 167).select("id,published");
console.log("lesson", r1.error?.message ?? r1.data);
const r2 = await sb.from("posts").update({ title: n.title, body: n.body_html, content_type: n.content_type }).eq("id", n.posted_id).select("id");
console.log("post", r2.error?.message ?? r2.data);
