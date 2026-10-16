// Chỉ ĐỌC: trạng thái bài học khoá HSG9 + sĩ số lớp 19 + bản tin đã có. Chạy: npx tsx scripts/tra-lich-hsg9.mts
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";

const env = (k: string) => fs.readFileSync(".env.local", "utf8").split("\n").find((l) => l.startsWith(`${k}=`))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"));

const ids = [150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 178];
const { data: ls } = await sb.from("lessons").select("id,title,published").in("id", ids).order("id");
for (const l of ls ?? []) console.log(l.id, l.published ? "HIỆN" : "ẨN ", l.title);
const { count } = await sb.from("user_classes").select("*", { count: "exact", head: true }).eq("class_id", 19).eq("status", "active");
console.log("sĩ số lớp 19:", count);
const { data: c } = await sb.from("classes").select("id,name").eq("id", 19);
console.log(c);
const { data: an } = await sb.from("class_announcements").select("id,kind,created_at,body").eq("class_id", 19).order("id", { ascending: false }).limit(5);
console.log(an);
