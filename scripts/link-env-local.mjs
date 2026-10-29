// Worktree không có .env.local (file gitignore) → dev/build báo "Hệ thống đang được cấu hình".
// Chạy trước dev/build: nếu thiếu, tạo symlink tới .env.local của checkout chính.
import { existsSync, symlinkSync } from "node:fs";
import { execSync } from "node:child_process";
import { dirname, join } from "node:path";

if (!existsSync(".env.local")) {
  try {
    const common = execSync("git rev-parse --path-format=absolute --git-common-dir", { encoding: "utf8" }).trim();
    const main = join(dirname(common), ".env.local");
    if (existsSync(main)) {
      symlinkSync(main, ".env.local");
      console.log(`[env] đã link .env.local → ${main}`);
    } else {
      console.warn("[env] KHÔNG tìm thấy .env.local ở checkout chính — Supabase sẽ báo chưa cấu hình.");
    }
  } catch {
    console.warn("[env] thiếu .env.local và không dò được checkout chính.");
  }
}
