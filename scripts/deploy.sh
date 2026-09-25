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
cat > .htaccess <<'EOF'
RedirectMatch 404 /\.git
<IfModule mod_expires.c>
  ExpiresActive On
  <FilesMatch "\.(js|css|woff2?)$">
    ExpiresDefault "access plus 1 year"
  </FilesMatch>
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
