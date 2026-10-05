# Nhắc luyện 1 lần/ngày bằng Web Push (GĐ 2.6 / M4) — việc thầy làm trên Mac

Mã đã viết xong, CHƯA chạy/deploy gì. Làm đúng thứ tự (mỗi bước độc lập kiểm được).

## 1. Chạy migration
```
cd /Users/MAC/Projects/thachlab && git pull origin main
bash scripts/run-migrations.sh
```
`20261005160000_push_subscriptions.sql`: tạo bảng `push_subscriptions` + 2 hàm. Chạy lúc nào cũng được (chỉ tạo mới).
Rollback: `supabase db query --linked -f perf/rollback/20261005160000_push_subscriptions.down.sql`.
Sau đó: `node scripts/gen-database-doc.mjs`.

## 2. Sinh khoá VAPID và đặt secrets (khoá KHÔNG vào repo)
```
npx web-push generate-vapid-keys
supabase secrets set VAPID_PUBLIC_KEY=<public> VAPID_PRIVATE_KEY=<private> VAPID_SUBJECT=mailto:itachi2601@gmail.com PUSH_CRON_SECRET=$(openssl rand -hex 24)
```
Khoá công khai cũng đặt cho phía web: thêm `NEXT_PUBLIC_VAPID_PUBLIC_KEY=<public>` vào `.env.local` (và nơi build deploy đọc env) rồi build lại.
Thiếu biến này thẻ "Nhắc luyện" tự ẩn, không lỗi. Đổi khoá VAPID sau này = mọi đăng ký cũ vô hiệu (HS phải bật lại).

## 3. Deploy Edge Function
```
supabase functions deploy send-daily-push --no-verify-jwt
```
`--no-verify-jwt` vì cron xác thực bằng header `x-cron-secret`. Function KHÔNG typecheck được (không có deno) — phải thử thật:
```
curl -s -X POST https://<project-ref>.supabase.co/functions/v1/send-daily-push -H "x-cron-secret: <PUSH_CRON_SECRET>"
```
Kỳ vọng `{"due":0,"sent":0,"removed":0,"failed":0}` khi chưa ai tới giờ. Sai secret -> 401. Nếu lỗi import `npm:web-push`
xem log `supabase functions logs send-daily-push`; phương án thay: `jsr:@negrel/webpush`.

## 4. Đặt lịch (mỗi giờ, pg_cron + pg_net — chạy tay trong SQL editor, KHÔNG nằm trong migration vì chứa secret)
```sql
create extension if not exists pg_net;
select cron.schedule('send-daily-push', '0 * * * *', $$
  select net.http_post(
    url := 'https://<project-ref>.supabase.co/functions/v1/send-daily-push',
    headers := jsonb_build_object('x-cron-secret', '<PUSH_CRON_SECRET>', 'Content-Type', 'application/json'),
    body := '{}'::jsonb);
$$);
```
pg_cron chạy theo UTC; mỗi giờ tròn nên không lệch (hàm tự đổi sang giờ VN). Gỡ lịch: `select cron.unschedule('send-daily-push');`.

## 5. Thử thật
Trên điện thoại (Android Chrome, hoặc iPhone đã thêm vào Màn hình chính): đăng nhập HS -> /tai-khoan -> "Bật nhắc" -> cho phép
thông báo. Ép nhắc ngay: đặt `remind_hour` của dòng mình bằng giờ VN hiện tại rồi gọi curl ở bước 3. Kiểm: chạm tin mở /lop-hoc/.

## Hành vi
- 1 tin/ngày/thiết bị; hàm SQL đánh dấu `last_sent_at` trước khi gửi (gửi lỗi tạm thời = bỏ ngày đó, không gửi bù).
- Không nhắc HS đã luyện hoặc nộp đề hôm nay (ngày VN). Giờ nhắc 6–22h (ngoài khung ngủ).
- Endpoint 404/410 bị xoá khỏi bảng. HS tắt nhắc = xoá dòng + huỷ đăng ký trên thiết bị.
- Nội dung: `Em còn 🔴 <chủ đề yếu nhất> — 5 phút?` (🟡 nếu mới ở mức "cần luyện"); chưa đủ dữ liệu -> "Hôm nay luyện 5 phút nhé?". Test: `npx tsx scripts/test-push-message.mts`.
