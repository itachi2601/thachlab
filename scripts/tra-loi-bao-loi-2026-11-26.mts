// Ghi admin_note/status cho đợt xử lý báo lỗi 26/11/2026.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
const e=(n:string)=>fs.readFileSync(".env.local","utf8").split("\n").find(l=>l.startsWith(n+"="))!.slice(n.length+1).trim();
const sb=createClient(e("NEXT_PUBLIC_SUPABASE_URL"),e("SUPABASE_SERVICE_ROLE_KEY"));
const U:[number,string,string][]=[
 [168,"da_xu_ly","Hình 4 phương án của câu này bị mất và quá nhỏ, thầy đã đổi thành 4 phương án chữ (đáp án vẫn C: khung tịnh tiến trong từ trường đều thì i_c = 0). Cảm ơn em."],
 [175,"da_xu_ly","Thầy đã sửa câu thiếu hình (câu khung dây): nay là 4 phương án chữ. Cảm ơn em."],
 [170,"da_xu_ly","Thầy đã vẽ bổ sung hình nhiệt kế (thang 0–50 °C, mỗi vạch 2 °C) cho câu này. Cảm ơn em."],
 [171,"da_xu_ly","Em phát hiện đúng chỗ thiếu: câu này tách từ câu trước nên mất dữ kiện 'đã nung khí đến 57 °C (330 K)'. Thầy đã bổ sung vào đề. 300 K là nhiệt độ ban đầu; nút bật ở 378,75 K, nên phải đun thêm 378,75 − 330 ≈ 48,8 °C."],
 [172,"da_xu_ly","Đề in nhầm 'không đúng'. Thầy đã sửa thành 'đúng với định luật Charles', đáp án C: V/T = hằng số. Cảm ơn em."],
 [174,"da_xu_ly","Em đúng: (200/18)·6,02·10^23 ≈ 6,69·10^24. Thầy đã sửa ý b thành 'xấp xỉ 6,69·10^24' (vẫn Đúng) và lời giải. Cảm ơn em."],
 [176,"da_xu_ly","Em đúng: p1 = 1,4·10^5 Pa, p2 = p1 − 10^5 = 0,4·10^5 Pa, đáp án D. Thầy đã sửa đáp án và lời giải. Cảm ơn em."],
 [161,"da_xu_ly","Câu định luật III có trong phần luyện tập Bài 15 vì mục ôn gắn cả định luật I–III. Câu và đáp án đúng; thầy ghi nhận để xem lại cách gắn chủ đề."],
 [169,"dang_xu_ly","Ảnh là giao diện chọn đề cũ (ô Tìm đề + danh sách). Bản mới chọn đề bằng thẻ, và từ nay tìm ra đúng 1 đề thì tự chọn đề đó. Con tắt hẳn app rồi mở lại (hoặc tải lại trang) để nhận bản mới."],
 [177,"dang_xu_ly","Các câu Trả bài của Bài 15 không mất: đã được chuyển lên ô 🎯 ở cuối từng mục I–III, mục Trả bài cuối bài chỉ còn 1 câu tổng. Thầy sẽ ghi thêm chỉ dẫn cho dễ thấy."],
 [173,"dang_xu_ly","Em dùng điện thoại gì (iPhone/Android)? Khi bấm nút loa 🔊 to có tiếng không? Nếu dùng iPhone, em kiểm công tắc im lặng bên hông máy giúp thầy."],
 [157,"da_xu_ly","Thầy cảm ơn em 😊"],
 [158,"da_xu_ly","Thầy chào em 😊"],
 [166,"da_xu_ly","Cảm ơn em đã ghé báo 😊"],
];
for(const [id,status,admin_note] of U){const {error}=await sb.from("bug_reports").update({status,admin_note}).eq("id",id);console.log(id,error?.message??"ok");}
