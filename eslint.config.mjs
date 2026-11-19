import { defineConfig, globalIgnores } from "eslint/config";
import nextVitals from "eslint-config-next/core-web-vitals";
import nextTs from "eslint-config-next/typescript";

const eslintConfig = defineConfig([
  ...nextVitals,
  ...nextTs,
  // Biến/tham số đặt tên bắt đầu bằng "_" là cố ý bỏ (vd `{ a: _omit, ...rest }`) — không tính cảnh báo.
  {
    rules: {
      "@typescript-eslint/no-unused-vars": [
        "warn",
        { argsIgnorePattern: "^_", varsIgnorePattern: "^_", caughtErrorsIgnorePattern: "^_", destructuredArrayIgnorePattern: "^_" },
      ],
    },
  },
  // Override default ignores of eslint-config-next.
  globalIgnores([
    // Default ignores of eslint-config-next:
    ".next/**",
    "out/**",
    "build/**",
    "next-env.d.ts",
    ".claude/worktrees/**",
    "scratchpad/**",
    // File tạm sinh ra khi xử lý PDF/đề, không phải code của web.
    "tmp/**",
    // Deno runtime (Supabase Edge Function), không dùng chung linter/tsconfig với Next.js.
    "supabase/functions/**",
  ]),
]);

export default eslintConfig;
