// Mời hàng loạt giảng viên vào ThachLab và cấp sẵn vai trò "instructor".
//
// App này export tĩnh (next.config output: "export"), không có server Node.js ở production
// nên không thể có API route dùng service role key. Script này CHỈ chạy cục bộ trên máy bạn:
//
//   SUPABASE_SERVICE_ROLE_KEY=xxx NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co node scripts/invite-instructors.mjs
//
// Lấy SUPABASE_SERVICE_ROLE_KEY ở Supabase Dashboard → Settings → API → service_role
// (secret, KHÔNG commit, KHÔNG đưa vào .env.local dùng chung với NEXT_PUBLIC_*, KHÔNG dán vào chat).
// Mỗi người sẽ nhận 1 email mời đặt mật khẩu; sau khi họ nhận lời mời, profiles.role đã sẵn là 'instructor'.

import { createClient } from "@supabase/supabase-js";

const SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL;
const SERVICE_ROLE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY;
if (!SUPABASE_URL || !SERVICE_ROLE_KEY) {
  console.error("Thiếu NEXT_PUBLIC_SUPABASE_URL hoặc SUPABASE_SERVICE_ROLE_KEY trong biến môi trường.");
  process.exit(1);
}

// Danh sách trích từ ảnh giảng viên Khoa Cơ khí bạn gửi. Đã kiểm tra sơ bộ định dạng email —
// 2 dòng đánh dấu NEEDS_FIX bên dưới có vẻ lỗi (đuôi ".ẹh" thay vì ".edu.vn", và có khoảng trắng
// thừa trong địa chỉ) — SỬA LẠI cho đúng trước khi chạy, tránh mời nhầm địa chỉ.
const INSTRUCTORS = [
  { full_name: "Nguyễn Quốc Văn", email: "nqvan@caothang.edu.vn" },
  { full_name: "Nguyễn Văn Vũ", email: "nvvu@caothang.edu.vn" },
  { full_name: "Nguyễn Văn Thông", email: "nvthong@caothang.edu.vn" },
  { full_name: "Dương Văn Ba", email: "dvba@caothang.edu.vn" },
  { full_name: "Trần Trọng Thuyết", email: "ttthuyet@caothang.edu.vn" },
  { full_name: "Ngô Diệu Thạch", email: "ndthach@caothang.edu.vn" },
  { full_name: "Lý Chánh Trung", email: "lychanhtrung@caothang.edu.vn" },
  { full_name: "Nguyễn Tấn Hùng", email: "nguyentanhung@caothang.edu.vn" },
  { full_name: "Nguyễn Thoại Khanh", email: "nguyenthoaikhanh@caothang.edu.vn" }, // NEEDS_FIX: ảnh ghi "@caothang.ẹh" — đã sửa thành .edu.vn, xác nhận lại trước khi chạy
  { full_name: "Đặng Nguyễn Nhân", email: "dangnguyenhan@caothang.edu.vn" }, // NEEDS_FIX: ảnh có khoảng trắng thừa "Dangnguyenhan @caothang.edu.vn" — đã bỏ khoảng trắng, xác nhận lại
  { full_name: "Nguyễn Long Phụng", email: "nlphung@caothang.edu.vn" },
  { full_name: "Lê Đức Phương", email: "leducphuong@caothang.edu.vn" },
  { full_name: "Nguyễn Hải Sơn", email: "nhson@caothang.edu.vn" },
  { full_name: "Nguyễn Đức Tài (81)", email: "nguyenductai81@caothang.edu.vn" },
  { full_name: "Phan Thị Cẩm Thanh", email: "ptcthanh@caothang.edu.vn" },
  { full_name: "Nguyễn Văn Toàn", email: "nguyenvantoan@caothang.edu.vn" },
  { full_name: "Nguyễn Thanh Hơn", email: "nguyenthanhhon@caothang.edu.vn" },
  { full_name: "Nguyễn Quang Tuấn", email: "nguyenquangtuan@caothang.edu.vn" },
  { full_name: "Ngô Ngọc Tuyền", email: "ngongoctuyen@caothang.edu.vn" },
  { full_name: "Đặng Ngọc Lê Văn", email: "dangngoclevan@caothang.edu.vn" },
  { full_name: "Nguyễn Đăng Khoa", email: "nguyendangkhoa@caothang.edu.vn" },
  { full_name: "Nguyễn Đức Tài", email: "nguyenductai91@caothang.edu.vn" },
  { full_name: "Phạm Thế Lam", email: "phamthelam@caothang.edu.vn" },
  { full_name: "Võ Hoàng Khang", email: "vohoangkhang@caothang.edu.vn" },
  { full_name: "Dương Nguyên Trung", email: "duongnguyentrung@caothang.edu.vn" },
];

const supabase = createClient(SUPABASE_URL, SERVICE_ROLE_KEY, { auth: { autoRefreshToken: false, persistSession: false } });

async function findExistingUserByEmail(email) {
  // API admin không có "get by email" trực tiếp nên duyệt trang danh sách người dùng.
  for (let page = 1; page <= 20; page++) {
    const { data, error } = await supabase.auth.admin.listUsers({ page, perPage: 200 });
    if (error) throw error;
    const found = data.users.find((user) => user.email?.toLowerCase() === email.toLowerCase());
    if (found) return found;
    if (data.users.length < 200) return null;
  }
  return null;
}

async function main() {
  for (const person of INSTRUCTORS) {
    try {
      let userId;
      const existing = await findExistingUserByEmail(person.email);
      if (existing) {
        userId = existing.id;
        console.log(`= ${person.email} đã có tài khoản, chỉ cập nhật vai trò.`);
      } else {
        const { data, error } = await supabase.auth.admin.inviteUserByEmail(person.email, {
          data: { full_name: person.full_name },
        });
        if (error) throw error;
        userId = data.user.id;
        console.log(`+ Đã mời ${person.email}`);
      }
      // Trigger handle_new_user tạo profiles ngay khi có user mới; nếu vừa mời thì đợi 1 nhịp.
      await new Promise((resolve) => setTimeout(resolve, existing ? 0 : 800));
      const { error: updateError } = await supabase.from("profiles").update({ role: "instructor" }).eq("id", userId);
      if (updateError) throw updateError;
      console.log(`  → role=instructor cho ${person.full_name}`);
    } catch (cause) {
      console.error(`! Lỗi với ${person.email}:`, cause instanceof Error ? cause.message : cause);
    }
  }
}

main();
