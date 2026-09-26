<!-- BEGIN:nextjs-agent-rules -->
# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` before writing any code. Heed deprecation notices.
<!-- END:nextjs-agent-rules -->

<!-- BEGIN:thachlab-migrations -->
# Migration Supabase — quy tắc bắt buộc

Hiện trạng dự án: `docs/STATE.md`. Đọc file đó trước khi bắt đầu một đợt việc lớn.

## Agent KHÔNG được tự chạy migration lên production
Mọi thay đổi schema/policy/hàm chỉ được **viết thành file** trong `supabase/migrations/`,
kèm khối rollback ở cuối file (hoặc file `.down.sql` riêng trong `perf/rollback/`).
Không `supabase db push` (thư mục migrations mới, CLI không biết ~99 migration cũ).
Không tự gọi `supabase db query --linked` với lệnh ghi.

## Khi có migration mới đang chờ → tự xuất lệnh cho Thạch chạy
Kết thúc đợt việc, nếu `supabase/migrations/` có file chưa chạy trên production:

1. Cập nhật mảng `FILES` trong `scripts/run-migrations.sh` theo đúng thứ tự chạy.
2. In ra cho Thạch **đúng khối này**, không diễn giải dài:

```
bash scripts/run-migrations.sh
```

3. Kèm 3 dòng: mỗi file làm gì, file nào cần chạy ngoài giờ học sinh làm bài, lệnh rollback nếu hỏng.
4. Ghi các file đang chờ vào mục "ĐANG CHỜ" của `docs/STATE.md`.

Script đã lo: hỏi xác nhận từng file, ghi log `scripts/logs/`, dừng ngay khi lỗi,
nhắc lệnh rollback. `--yes` chạy thẳng, `--only N` chạy riêng một file.

## Vì sao phải là máy của Thạch
Sandbox đám mây và sandbox gắn thiết bị đều bị proxy chặn `*.supabase.co` (403 CONNECT),
và cũng không có `SUPABASE_SERVICE_ROLE_KEY` / mật khẩu DB. Khóa service role không được
đưa vào hội thoại. Claude Code chạy trên macOS có sẵn `.env.local` và CLI đã `link` —
đó là nơi duy nhất chạy được.

## Sau khi migration chạy xong
- Đối chiếu RPC: `npx tsx scripts/perf-compare-rpc.mts`
- Backfill mức độ câu hỏi — **GHI THẬT NGAY, không có dry-run**, tham số chỉ giới hạn số câu:
  `npx tsx scripts/backfill-question-bank-difficulty.mts 20` (thử nhỏ, xem lại UI rồi mới chạy hết)
<!-- END:thachlab-migrations -->
