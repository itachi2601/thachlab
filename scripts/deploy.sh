#!/usr/bin/env bash
# Build trang tĩnh và force-push lên nhánh `deploy` — Cron Job trên hosting
# (chạy `git fetch && git reset --hard origin/deploy` mỗi 10 phút) sẽ tự kéo về.
# Nhánh deploy luôn chỉ có đúng 1 commit để repo không phình theo thời gian.
set -euo pipefail

REPO_URL="https://github.com/itachi2601/thachlab.git"
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

<IfModule mod_brotli.c>
  AddOutputFilterByType BROTLI_COMPRESS text/html text/css application/javascript application/json image/svg+xml
</IfModule>
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css application/javascript application/json image/svg+xml
</IfModule>
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
git add -A
git -c user.name="ThachLab Deploy" -c user.email="deploy@thachlab.id.vn" \
  commit -qm "deploy: $(date '+%Y-%m-%d %H:%M')"
# Bản build ~40MB — bộ đệm HTTP mặc định 1MB làm push đứt giữa chừng (curl 55).
git -c http.postBuffer=524288000 push -f "$REPO_URL" deploy
rm -rf .git

echo "✓ Đã push bản build lên nhánh deploy — hosting sẽ cập nhật trong vòng 10 phút."
