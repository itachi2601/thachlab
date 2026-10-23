# Rà soát dự án 22/10 + dọn lint bằng DeepSeek (22–23/10/2026)

**Trạng thái:** xong trên `main`. Lint 94 → 0 lỗi / 20 cảnh báo, `tsc` sạch. Chưa deploy, chưa thử điện thoại.

## Đã làm
- Phản biện `docs/RA-SOAT-DU-AN-2026-10-22.md` → `docs/RA-SOAT-DU-AN-2026-10-22-PHAN-BIEN.md` (§1 khớp, §2 sai/thiếu, §5 nhật ký 5 lượt lint).
  Hai điều quan trọng: (1) `@xmldom/xmldom` KHÔNG chết (3 script dùng) — đừng gỡ; (2) `app/kiem-tra/lam/page.tsx:55` select
  nguyên `exams.questions` (có đáp án) về trình duyệt → P0 #1 phải gồm cả lược đáp án cho HS + RPC/Edge chấm server.
- `scripts/deepseek-sua-lint.mts` (+ `scripts/lib/env.mts` dùng chung readEnvLocal): DeepSeek sửa lint từng file, hàng rào
  eslint + tsc + sanity, dry-run mặc định, `--apply`, nhớ file đã thử, dừng khi cây tụt sau origin/main. 4 lượt / 46 file,
  sai 5 (bỏ nhánh reset, thêm dep làm effect chạy dữ liệu cũ) — `kiem-code` bắt hết, Claude sửa.
- Claude sửa 17 lỗi cuối trong 6 file > 900 dòng (lop-hoc/page 4 effect → render-phase; LessonImporter useMemo grade; …).

## Tiếp tục trên Mac
1. `git pull origin main`; xoá nhánh `deepseek/lint-*` cục bộ nếu còn.
2. Thử `/lop-hoc` trên điện thoại: đổi môn lớp 9 (`?subject=`), link `?chapter=`, nút "Tiếp tục bài" (lastLessonId đọc localStorage lúc khởi tạo).
3. Deploy (`scripts/deploy.sh`), đồng thời đổi `camera=()` → `camera=(self)` trong `Permissions-Policy` (P0 #2, 1 dòng) rồi thử QR trên iPhone + Android.
4. Bật CI gate P0 #4: thêm job `tsc --noEmit` + `eslint --max-warnings 20` + `next build` trước bước gộp trong `.github/workflows/gop-claude-vao-main.yml`.
5. P0 #1 (lược đáp án + chấm server) → agent `kien-truc-du-lieu`, ước 2–3 ngày; `dompurify` → dependencies, `.env.example` (P0 #3, không gỡ xmldom).
6. 4 key đã lộ trong chat 22/10 (service role, Anthropic, Azure Speech, DeepSeek) — đổi nếu chưa.

## Lệnh hay dùng
- `npx tsx scripts/deepseek-sua-lint.mts --limit 3` (dry-run) / `--limit 20 --apply` / `--force` / `--files a,b`; cần `DEEPSEEK_API_KEY`, nên `DEEPSEEK_MAX_TOKENS=32000`.
- Đếm lỗi: `npx eslint app components lib services features hooks -f json` rồi lọc `severity===2`.
