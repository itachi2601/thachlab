// Kiểm gói bài học trước khi đăng: npx tsx .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/validate_bundle.mts <bundle.json>
// Dùng đúng validateBundle của trang /quan-tri/nhap-bai (services/lesson-import.ts). Chạy từ gốc repo thachlab.
import fs from "node:fs";
import { validateBundle } from "@/services/lesson-import";

const file = process.argv[2];
if (!file) { console.error("thiếu <bundle.json>"); process.exit(1); }
const r = validateBundle(JSON.parse(fs.readFileSync(file, "utf8")));
console.log(r);
process.exit(r.ok ? 0 : 1);
