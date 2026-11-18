// Ghi admin_note/status cho đợt xử lý báo lỗi 18/11/2026 (đợt 2 rà soát website).
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
const e=(n:string)=>fs.readFileSync(".env.local","utf8").split("\n").find(l=>l.startsWith(n+"="))!.slice(n.length+1).trim();
const sb=createClient(e("NEXT_PUBLIC_SUPABASE_URL"),e("SUPABASE_SERVICE_ROLE_KEY"));
const U:[number,string,string][]=[
 [140,"da_xu_ly","Bài kiểm tra đã có hộp xác nhận trước khi nộp (cho biết còn bao nhiêu câu chưa làm). Cảm ơn em đã góp ý."],
 [165,"dang_xu_ly","Đã kiểm tra: câu 6 và câu 13 của đề này đang thiếu hình. Thầy sẽ vẽ bổ sung hình rồi cập nhật đề."],
 [155,"dang_xu_ly","Thầy đã ghi nhận lỗi chặng 1 hiện 'chưa làm' dù em đã nộp. Thầy sẽ kiểm tra dữ liệu lượt làm của em; em nhắn thầy tên lớp + giờ em nộp nếu được."],
 [133,"dang_xu_ly","Thầy chưa rõ đơn giá giờ nào chưa đúng (bậc B1/B2/B3? tháng nào?). Con nhắn lại giúp thầy nhé."],
 [145,"dang_xu_ly","Em cho thầy biết đề nào, và em muốn xem đáp án đúng ở đâu (ngay sau khi nộp hay trong mục Kết quả)? Thầy sẽ xem lại."],
 [156,"dang_xu_ly","Em cho thầy biết đề nào chưa có lời giải chi tiết (tên đề + số câu) để thầy bổ sung."],
 [162,"dang_xu_ly","Em cho thầy biết đề/bài nào không xem được đáp án để thầy kiểm tra."],
 [129,"dang_xu_ly","Thầy chưa rõ ý. Em mô tả thêm: ở mục nào, em muốn thấy điều gì sau khi xong 80% mức dễ?"],
 [152,"dang_xu_ly","Thầy đã ghi nhận đề nghị mở mùa mới."],
];
for(const [id,status,admin_note] of U){const {error}=await sb.from("bug_reports").update({status,admin_note}).eq("id",id);console.log(id,error?.message??"ok");}
