# Cloudflare + giới hạn đăng nhập — hướng dẫn (Đợt 2 rà soát, 17/10/2026)

Việc trong dashboard là của thầy (đổi DNS, đổi cấu hình Auth) — Claude không tự làm. Mã đã sẵn: header bảo mật ở `scripts/deploy.sh` (có hiệu lực từ lần deploy kế tiếp).

## 1. Header bảo mật (đã thêm vào deploy.sh)
Có hiệu lực sau `./scripts/deploy.sh` + cron kéo về. Kiểm: `curl -sI https://thachlab.id.vn | grep -iE "x-content|referrer|x-frame|strict|content-security"`.
- CSP đang là **Report-Only** (không chặn). Mở trang bài học, làm bài, quản trị, nhập đề với DevTools → Console; còn cảnh báo `[Report Only]` nào thì thêm nguồn đó vào `deploy.sh`. Sạch rồi đổi `Content-Security-Policy-Report-Only` → `Content-Security-Policy`.
- HSTS `max-age` 6 tháng, không `includeSubDomains`/`preload` (cố ý, dễ gỡ).
- Nếu thầy nhúng trang vào iframe ở nơi khác (LMS, Google Sites) → báo, vì `X-Frame-Options: SAMEORIGIN` sẽ chặn.

## 2. Cloudflare (gói Free) trước tên miền
1. Đăng ký Cloudflare, thêm `thachlab.id.vn`, đổi nameserver ở nhà đăng ký tên miền (id.vn) sang 2 NS Cloudflare cấp. Giữ nguyên bản ghi A trỏ về hosting; bật proxy (đám mây cam) cho `@` và `www`.
2. SSL/TLS → mode **Full (strict)** (hosting đã có chứng chỉ). Bật *Always Use HTTPS*.
3. Caching: *Browser Cache TTL = Respect Existing Headers* (đã có header riêng). Thêm Cache Rule cho `/_next/static/*` và `/data/*` = Eligible for cache. **Không** cache `/quan-tri/*`.
4. Security → Settings: *Bot Fight Mode* bật; Security Level Medium.
5. WAF → Rate limiting rule (Free có 1 luật): bật cho `thachlab.id.vn` mọi đường dẫn, **ngưỡng cao** (vd 300 yêu cầu/10 giây/IP, hành động Managed Challenge). Chỉ để chặn flood; **đừng đặt thấp** — cả lớp thường dùng chung 1 IP wifi trường.
6. Sau khi bật: kiểm `/`, đăng nhập, một bài học, làm bài, push thông báo (service worker) vẫn chạy. Lỗi thì tắt proxy (đám mây xám) là về như cũ.
7. Lưu ý: LiteSpeed/DirectAdmin sẽ thấy IP của Cloudflare; không ảnh hưởng vì site tĩnh. Supabase vẫn nhận IP thật của học sinh (trình duyệt gọi thẳng Supabase, không qua Cloudflare).

## 3. Supabase Auth — giới hạn đăng nhập (Dashboard → Authentication → Rate Limits)
- Mặc định tính **theo IP**: học sinh một lớp cùng wifi trường dễ chạm trần. Giữ/nâng: *Sign-ups and sign-ins* ≥ 150 / 5 phút / IP; *Token refresh* mặc định; *Email sent* giữ thấp (chống spam email).
- Authentication → Providers/Email: tắt *Enable email signups* nếu không còn cho tự đăng ký (chỉ nếu `/dang-ky` không còn dùng — hỏi lại trước khi tắt). *Minimum password length* = 8.
- Authentication → Attack Protection: bật *Leaked password protection* nếu gói cho phép.

## 4. CAPTCHA đăng nhập — KHUYẾN NGHỊ CHƯA BẬT
- Supabase bắt CAPTCHA token ở **mọi** `signUp`, `signInWithPassword`, `resetPasswordForEmail`. Hiện có 6 chỗ gọi (`app/dang-nhap`, `app/dang-ky`, `services/password-reset.ts` ×2, `parent-links.ts`, `staff-invites.ts`). Bật ở dashboard mà code chưa gửi token = **cả trường không đăng nhập được**.
- `browserslist` hỗ trợ iOS 12/Safari 12; Cloudflare Turnstile không đảm bảo chạy trên máy cũ → có nguy cơ khoá học sinh dùng điện thoại đời cũ.
- Đề xuất: thử Cloudflare WAF + rate limit Auth (mục 2–3) 1–2 tuần, xem log Auth (Dashboard → Logs → Auth) có dò mật khẩu thật không. Chỉ khi có tấn công mới thêm Turnstile, nạp **chỉ ở `/dang-nhap`** qua `NEXT_PUBLIC_TURNSTILE_SITE_KEY`, trong chế độ có fallback, và test iPhone cũ trước.
- Lưu ý cùng loại ở `reset-password` nhánh `claim` (mã đặt lại không giới hạn lần thử) — cần migration Đợt 3, không giải được bằng CAPTCHA.
