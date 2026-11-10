// Worktree không có .env.local (file gitignore) → dev/build báo "Hệ thống đang được cấu hình".
// Chạy trước dev/build: nếu thiếu, tạo symlink tới .env.local của checkout chính.
import { existsSync, readFileSync, symlinkSync } from "node:fs";
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

// Build tĩnh nhúng NEXT_PUBLIC_* lúc build: thiếu khoá thì web chạy được nhưng mọi trang đòi dữ liệu
// báo "Hệ thống đang được cấu hình" (sự cố 29/10/2026 — bản deploy build ở worktree thiếu .env.local).
if (process.argv.includes("--require")) {
  const need = ["NEXT_PUBLIC_SUPABASE_URL", "NEXT_PUBLIC_SUPABASE_ANON_KEY"];
  const file = existsSync(".env.local") ? readFileSync(".env.local", "utf8") : "";
  const missing = need.filter((k) => !process.env[k] && !new RegExp(`^${k}=\\S`, "m").test(file));
  if (missing.length) {
    console.error(`[env] DỪNG BUILD: thiếu ${missing.join(", ")} — bản build sẽ không kết nối được Supabase.`);
    process.exit(1);
  }
}
