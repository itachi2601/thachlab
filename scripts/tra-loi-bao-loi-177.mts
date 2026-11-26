// Đóng báo #177 (26/11/2026) sau khi thêm dòng chỉ dẫn vào Trả bài L11 Bài 15.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
const e=(n:string)=>fs.readFileSync(".env.local","utf8").split("\n").find(l=>l.startsWith(n+"="))!.slice(n.length+1).trim();
const sb=createClient(e("NEXT_PUBLIC_SUPABASE_URL"),e("SUPABASE_SERVICE_ROLE_KEY"));
const {error}=await sb.from("bug_reports").update({status:"da_xu_ly",admin_note:"Các câu Trả bài không mất: câu tự hỏi của từng phần nằm ở ô 🎯 Cần nắm cuối mục I, II, III. Thầy đã thêm dòng chỉ dẫn này vào mục Trả bài. Cảm ơn em."}).eq("id",177);
console.log(177,error?.message??"ok");
