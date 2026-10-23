#!/usr/bin/env bash
# Build trang tĩnh và force-push lên nhánh `deploy` — Cron Job trên hosting sẽ tự kéo về.
# Nhánh deploy luôn chỉ có đúng 1 commit để repo không phình theo thời gian.
#
# BẢO MẬT — lệnh Cron Job trên DirectAdmin PHẢI là (không phải chỉ reset --hard):
#   git fetch && git reset --hard origin/deploy && git clean -fdx
# `git clean -fdx` là phần bắt buộc: nó xoá mọi file KHÔNG nằm trong git (kể cả file ẩn/gitignore).
# Nếu thiếu dòng này, một file lạ bị ai đó upload thẳng vào thư mục web (qua FTP/cPanel lộ mật
# khẩu, hosting bị dò lỗ hổng...) — ví dụ trang chèn từ khoá cờ bạc/cá độ để SEO bẩn — sẽ tồn tại
# VĨNH VIỄN vì `reset --hard` chỉ ghi đè file git đang quản lý, không đụng tới file ngoài git.
set -euo pipefail

REPO_URL="git@github.com:itachi2601/thachlab.git"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

cd "$ROOT"
npm run build

cd out

# Chặn truy cập metadata git qua web + bật cache dài hạn cho assets đã hash.
# Ảnh (png/jpg/webp/svg/gif) KHÔNG có hash trong tên file → chỉ cache 30 ngày (không phải 1 năm
# như js/css) để không phải đổi tên file mỗi khi sửa. Dù vậy: SỬA một ảnh đã đăng thì PHẢI đổi
# tên file mới, không được ghi đè file cũ — nếu không, trình duyệt học sinh vẫn dùng bản cache cũ
# tối đa 30 ngày dù server đã có ảnh mới (xem mục "Cache ảnh" trong README.md).
#
# Nén nội dung text (html/css/js/json/svg): ưu tiên brotli (mod_brotli) nếu hosting LiteSpeed có
# bật, fallback mod_deflate (gzip) — hỗ trợ rộng rãi hơn trên Apache/LiteSpeed nên chắc ăn hơn.
#
# Ảnh: thêm luôn Cache-Control tường minh qua mod_headers (cùng 30 ngày với ExpiresDefault ở
# trên) — một số CDN/hosting ưu tiên đọc Cache-Control hơn Expires; có cả hai chắc ăn hơn, không
# xung đột (cùng giá trị).
cat > .htaccess <<'EOF'
RedirectMatch 404 /\.git
<IfModule mod_expires.c>
  ExpiresActive On
  <FilesMatch "\.(js|css|woff2?)$">
    ExpiresDefault "access plus 1 year"
  </FilesMatch>
  <FilesMatch "\.(png|jpe?g|webp|svg|gif)$">
    ExpiresDefault "access plus 30 days"
  </FilesMatch>
</IfModule>

<IfModule mod_headers.c>
  # Máy chủ LiteSpeed bỏ qua ExpiresDefault 1 năm ở trên và trả max-age 7 ngày → ép Cache-Control
  # tường minh cho file có hash trong tên (js/css/woff2).
  <FilesMatch "\.(js|css|woff2?)$">
    Header set Cache-Control "public, max-age=31536000, immutable"
  </FilesMatch>
  <FilesMatch "\.(png|jpe?g|webp|svg|gif)$">
    Header set Cache-Control "public, max-age=2592000"
  </FilesMatch>

  # HTML + dữ liệu RSC (__next.*.txt) + sw.js KHÔNG có hash trong tên và tham chiếu tới chunk theo hash:
  # sau deploy chunk cũ bị xoá, nên trang cũ còn nằm trong cache sẽ gọi chunk 404 (log LiteSpeed 23/10/2026).
  # no-cache = luôn hỏi lại máy chủ (vẫn dùng bản cache nếu chưa đổi, nhận 304) nên không tốn băng thông.
  # Đặt SAU các khối js/css để sw.js (đuôi .js) bị ghi đè khỏi "immutable 1 năm".
  <FilesMatch "\.(html|txt)$">
    Header set Cache-Control "no-cache"
  </FilesMatch>
  <FilesMatch "^sw\.js$">
    Header set Cache-Control "no-cache"
  </FilesMatch>

  # Header bảo mật (Đợt 2 rà soát 17/10/2026, docs/RA-SOAT-MA-NGUON-2026-10-17.md mục A7).
  Header always set X-Content-Type-Options "nosniff"
  Header always set Referrer-Policy "strict-origin-when-cross-origin"
  Header always set X-Frame-Options "SAMEORIGIN"
  Header always set Permissions-Policy "camera=(), microphone=(), geolocation=(), payment=()"
  Header always set Strict-Transport-Security "max-age=15552000"
  # CSP ở chế độ Report-Only: CHỈ ghi cảnh báo vào Console trình duyệt, KHÔNG chặn gì. Mở một vài
  # trang (bài học, làm bài, quản trị) với DevTools, nếu không còn cảnh báo "[Report Only]" thì đổi
  # tên header thành Content-Security-Policy để chặn thật. Giữ 'unsafe-inline' vì Next xuất tĩnh
  # chèn script/style inline; siết dần bằng nonce/hash sau.
  Header always set Content-Security-Policy-Report-Only "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob: https:; font-src 'self' data:; media-src 'self' https:; connect-src 'self' https://*.supabase.co wss://*.supabase.co; frame-src https://www.youtube-nocookie.com https://www.youtube.com https://phet.colorado.edu https://drive.google.com https://view.officeapps.live.com; worker-src 'self' blob:; object-src 'none'; base-uri 'self'; form-action 'self'"
</IfModule>

<IfModule mod_brotli.c>
  AddOutputFilterByType BROTLI_COMPRESS text/html text/css application/javascript application/json image/svg+xml
</IfModule>
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css application/javascript application/json image/svg+xml
</IfModule>

# Site 100% tĩnh (output: "export"), không có trang nào cần PHP chạy. Chặn hẳn thực thi PHP
# trong toàn bộ web root: nếu có file .php lạ bị chèn vào (qua FTP/cPanel lộ mật khẩu, ví dụ
# shell chèn trang cờ bạc/spam SEO), file đó vẫn nằm đó nhưng KHÔNG chạy được, chỉ trả về lỗi.
<FilesMatch "\.php$">
  <IfModule mod_authz_core.c>
    Require all denied
  </IfModule>
  <IfModule !mod_authz_core.c>
    Order allow,deny
    Deny from all
  </IfModule>
</FilesMatch>
EOF

# Học liệu tĩnh (public/data → /data/*.json, sinh bởi scripts/build-content.mjs) không có hash
# trong tên file → chỉ cache ngắn để bản build mới lên là học sinh thấy sau tối đa 10 phút.
mkdir -p data
cat > data/.htaccess <<'EOF'
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresDefault "access plus 10 minutes"
</IfModule>
EOF

rm -rf .git
git init -q -b deploy
# Tải commit deploy hiện tại về trước (nông, ~30MB tải xuống) để git chỉ GỬI phần khác biệt
# (thường vài trăm KB) thay vì cả bản build ~30MB mỗi lần — 28/9/2026 push full bị GitHub ngắt
# (HTTP 408) khi mạng yếu (hotspot điện thoại). Không tải được thì vẫn push full như cũ.
git fetch -q --depth=1 "$REPO_URL" deploy 2>/dev/null || echo "(không tải được bản deploy cũ — push full)"
git add -A
# Commit mồ côi (không parent) → nhánh deploy vẫn chỉ có đúng 1 commit.
NEW_COMMIT=$(git -c user.name="ThachLab Deploy" -c user.email="deploy@thachlab.id.vn" \
  commit-tree "$(git write-tree)" -m "deploy: $(date '+%Y-%m-%d %H:%M')")
git update-ref refs/heads/deploy "$NEW_COMMIT"
# Bản build ~40MB — bộ đệm HTTP mặc định 1MB làm push đứt giữa chừng (curl 55).
git -c http.postBuffer=524288000 push -f "$REPO_URL" deploy
rm -rf .git

echo "✓ Đã push bản build lên nhánh deploy — hosting sẽ cập nhật trong khoảng 1–2 phút (cron chạy mỗi phút)."
