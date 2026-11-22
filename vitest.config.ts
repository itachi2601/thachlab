import { defineConfig } from "vitest/config";
import path from "node:path";

// Test đơn vị cho hàm thuần (chấm điểm, thang luyện tập, tiến độ, rubric CNC). Không cần DOM/Supabase.
export default defineConfig({
  resolve: { alias: { "@": path.resolve(__dirname) } },
  test: { include: ["tests/**/*.test.ts"], environment: "node" },
});
