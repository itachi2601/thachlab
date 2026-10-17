#!/usr/bin/env bash
# Kiểm CORS + yêu cầu đăng nhập của các Edge Function sau khi deploy (chỉ đọc, không ghi gì).
BASE="https://jgvbdbpvjdntdgzthumv.supabase.co/functions/v1"
for f in check-exam classify-questions draw-figure hsg-ai-grade import-roster reset-password; do
  echo "== $f"
  echo -n "  OPTIONS (origin thachlab) -> "
  curl -s -o /dev/null -D - -X OPTIONS -H "Origin: https://thachlab.id.vn" \
    -H "Access-Control-Request-Method: POST" "$BASE/$f" | grep -i "^HTTP\|access-control-allow-origin" | tr -d '\r' | tr '\n' ' '
  echo
  echo -n "  POST khong dang nhap      -> "
  curl -s -w " [HTTP %{http_code}]" -X POST -H "Content-Type: application/json" -H "Origin: https://evil.example" -d '{}' "$BASE/$f" | cut -c1-160
  echo
done
